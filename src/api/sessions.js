import { json, err } from '../lib/http.js';
import { ensureColumns } from '../lib/schema.js';
import { authTeacher, needClass, needSession, needTest, accessibleClasses } from '../lib/access.js';
import { sessionWindow } from '../lib/time.js';
import { loadMcq, scoreMcq, rescoreSession, submitStudent } from '../lib/scoring.js';
import { audit } from '../lib/audit.js';
import { sessionQuestions, mcqOnly, isFrozen } from '../lib/frozen.js';

export { ensureColumns };

// A student who never pressed Submit (closed the browser, phone died, time ran
// out while offline) has saved answers but no score. Once their time is over,
// score those answers on the server so the teacher always sees a result.
// Students with extra minutes are left alone until their own deadline passes.
export async function finalizeSession(env, sessionId, endIso) {
  const ses = await env.DB.prepare('SELECT id, test_id, status FROM test_sessions WHERE id = ?1').bind(sessionId).first();
  if (!ses) return;
  await env.DB.prepare(
    `INSERT INTO results (session_id, student_id, mcq_score, mcq_max)
     SELECT DISTINCT session_id, student_id, 0, 0 FROM responses WHERE session_id = ?1
     ON CONFLICT(session_id, student_id) DO NOTHING`,
  ).bind(sessionId).run();
  const { results: pending } = await env.DB.prepare(
    `SELECT id, student_id, extra_minutes FROM results WHERE session_id = ?1 AND submitted_at IS NULL
       AND (started_at IS NOT NULL OR EXISTS (SELECT 1 FROM responses r WHERE r.session_id = results.session_id AND r.student_id = results.student_id))`,
  ).bind(sessionId).all();
  if (!pending.length) return;
  const now = Date.now();
  const sessionEnd = Date.parse(endIso);
  const due = pending.filter((r) => ses.status === 'closed' || now >= sessionEnd + (r.extra_minutes || 0) * 60000);
  if (!due.length) return;
  const qs = await loadMcq(env, ses.id, ses.test_id);
  const { results: rs } = await env.DB.prepare('SELECT student_id, question_id, selected_index FROM responses WHERE session_id = ?1').bind(sessionId).all();
  const by = {};
  for (const r of rs) (by[r.student_id] ||= {})[r.question_id] = r.selected_index;
  const stamp = new Date(Math.min(sessionEnd, now)).toISOString().replace('T', ' ').slice(0, 19);
  await env.DB.batch(due.map((r) => {
    const { score, max } = scoreMcq(qs, by[r.student_id] || {});
    return env.DB.prepare("UPDATE results SET mcq_score = ?1, mcq_max = ?2, submitted_at = ?3, submit_type = 'auto' WHERE id = ?4")
      .bind(score, max, stamp, r.id);
  }));
}

export async function listSessions(req, env) {
  const t = await authTeacher(req, env);
  if (!t) return err('Not logged in.', 401);
  await ensureColumns(env);
  const mine = await accessibleClasses(env, t);
  const { results } = await env.DB.prepare(
    `SELECT ts.id, ts.class_id, ts.scheduled_start, ts.duration_minutes, ts.scheduled_end, ts.status, ts.pin, ts.integrity_mode, ts.max_violations,
            c.name AS class_name, t.title AS test_title,
            (SELECT COUNT(*) FROM results r WHERE r.session_id = ts.id AND r.submitted_at IS NOT NULL) AS submitted_count,
            (SELECT COUNT(*) FROM students s WHERE s.class_id = ts.class_id) AS total_students,
            (SELECT COUNT(*) FROM results r WHERE r.session_id = ts.id AND r.submitted_at IS NULL
               AND (r.started_at IS NOT NULL OR EXISTS (SELECT 1 FROM responses x WHERE x.session_id = r.session_id AND x.student_id = r.student_id))) AS pending_count
     FROM test_sessions ts
     JOIN classes c ON c.id = ts.class_id
     JOIN tests t ON t.id = ts.test_id
     ORDER BY ts.scheduled_start DESC`,
  ).all();
  for (let i = results.length - 1; i >= 0; i--) if (!mine.has(results[i].class_id)) results.splice(i, 1);
  for (const s of results) {
    s.my_role = mine.get(s.class_id);
    const endIso = s.scheduled_end || new Date(Date.parse(s.scheduled_start) + s.duration_minutes * 60000).toISOString();
    if (sessionWindow({ ...s, scheduled_end: endIso }).phase === 'closed' && s.pending_count > 0) {
      await finalizeSession(env, s.id, endIso);
      s.submitted_count += s.pending_count;
    }
  }
  const withPhase = results.map((s) => {
    const startMs = Date.parse(s.scheduled_start);
    const endMs = s.scheduled_end ? Date.parse(s.scheduled_end) : (startMs + s.duration_minutes * 60000);
    const computedEnd = s.scheduled_end || new Date(endMs).toISOString();
    return {
      ...s,
      scheduled_end: computedEnd,
      phase: sessionWindow({ ...s, scheduled_end: computedEnd }).phase,
    };
  });
  return json({ sessions: withPhase });
}

export async function createSession(req, env) {
  const body = await req.json();
  const g1 = await needClass(req, env, body.class_id, 'edit'); if (g1.resp) return g1.resp;
  const g2 = await needTest(req, env, body.test_id, 'view'); if (g2.resp) return g2.resp;
  await ensureColumns(env);
  const { test_id, class_id, scheduled_start, duration_minutes, scheduled_end, pin } = body;
  const mode = ['log', 'warn', 'lock'].includes(body.integrity_mode) ? body.integrity_mode : 'warn';
  const maxV = Math.max(1, Math.min(20, Number(body.max_violations) || 3));
  if (!test_id || !class_id || !scheduled_start || !duration_minutes) {
    return err('test_id, class_id, scheduled_start, and duration_minutes are required.', 400);
  }
  const endIso = scheduled_end || new Date(Date.parse(scheduled_start) + Number(duration_minutes) * 60000).toISOString();
  const cleanPin = String(pin ?? '').trim();
  if (cleanPin && !/^[0-9A-Za-z]{3,12}$/.test(cleanPin)) return err('PIN must be 3–12 letters or digits.', 400);
  const finalPin = cleanPin || String(Math.floor(1000 + Math.random() * 9000));
  const { meta } = await env.DB.prepare(
    'INSERT INTO test_sessions (test_id, class_id, scheduled_start, duration_minutes, scheduled_end, pin, integrity_mode, max_violations) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8)',
  ).bind(test_id, class_id, scheduled_start, duration_minutes, endIso, finalPin, mode, maxV).run();
  return json({ id: meta.last_row_id, pin: finalPin });
}

export async function getSession(req, env, params) {
  const g = await needSession(req, env, params.sessionId, 'view'); if (g.resp) return g.resp;
  await ensureColumns(env);
  const session = await env.DB.prepare(
    `SELECT ts.id, ts.test_id, ts.class_id, ts.scheduled_start, ts.duration_minutes, ts.scheduled_end, ts.status, ts.pin, ts.integrity_mode, ts.max_violations,
            c.name AS class_name, t.title AS test_title
     FROM test_sessions ts JOIN classes c ON c.id = ts.class_id JOIN tests t ON t.id = ts.test_id
     WHERE ts.id = ?1`,
  ).bind(params.sessionId).first();
  if (!session) return err('Session not found.', 404);
  session.my_role = g.acc;
  session.phase = sessionWindow(session).phase;

  const startMs = Date.parse(session.scheduled_start);
  const endMs = startMs + session.duration_minutes * 60000;
  session.scheduled_end = session.scheduled_end || new Date(endMs).toISOString();

  if (session.phase === 'closed') await finalizeSession(env, session.id, session.scheduled_end);

  const sqs = await sessionQuestions(env, session.id, session.test_id);
  const maxPointsRow = {
    m: mcqOnly(sqs).reduce((t, q) => t + q.points, 0),
    w: sqs.filter((q) => q.kind === 'writing').reduce((t, q) => t + q.points, 0),
  };
  session.frozen = await isFrozen(env, session.id);

  const { results: roster } = await env.DB.prepare(
    `SELECT s.id, s.surname, s.first_name, s.gender,
            r.mcq_score, r.mcq_max, r.writing_score, r.writing_max,
            r.started_at, r.submitted_at, r.submit_type, r.published_at, r.tab_switches, r.violations, r.locked, r.lock_reason, (SELECT COALESCE(SUM(e.dur_ms), 0) FROM exam_events e WHERE e.session_id = ?1 AND e.student_id = s.id AND e.kind IN ('tab_hidden', 'window_blur')) AS away_ms, (SELECT COUNT(*) FROM session_notes n WHERE n.session_id = ?1 AND n.student_id = s.id) AS note_count, r.extra_minutes, r.last_seen, (r.device_id IS NOT NULL) AS has_device,
            (SELECT COUNT(*) FROM responses res WHERE res.session_id = ?1 AND res.student_id = s.id) AS answered_count
     FROM students s
     LEFT JOIN results r ON r.student_id = s.id AND r.session_id = ?1
     WHERE s.class_id = ?2 ORDER BY s.surname, s.first_name`,
  ).bind(params.sessionId, session.class_id).all();

  session.mcq_max = maxPointsRow.m;
  session.writing_max_default = maxPointsRow.w;
  session.roster = roster;
  return json(session);
}

export async function closeSession(req, env, params) {
  const g = await needSession(req, env, params.sessionId, 'edit'); if (g.resp) return g.resp;
  await env.DB.prepare("UPDATE test_sessions SET status = 'closed' WHERE id = ?1").bind(params.sessionId).run();
  return json({ ok: true });
}

export async function setWritingScore(req, env, params) {
  const g = await needSession(req, env, params.sessionId, 'edit'); if (g.resp) return g.resp;
  await ensureColumns(env);
  const { student_id, writing_score, writing_max } = await req.json();
  if (!student_id) return err('student_id is required.', 400);
  const existing = await env.DB.prepare('SELECT id FROM results WHERE session_id = ?1 AND student_id = ?2')
    .bind(params.sessionId, student_id).first();
  if (!existing) {
    await env.DB.prepare(
      'INSERT INTO results (session_id, student_id, mcq_score, mcq_max, writing_score, writing_max) VALUES (?1, ?2, 0, 0, ?3, ?4)',
    ).bind(params.sessionId, student_id, writing_score, writing_max).run();
  } else {
    await env.DB.prepare('UPDATE results SET writing_score = ?1, writing_max = ?2 WHERE id = ?3')
      .bind(writing_score, writing_max, existing.id).run();
  }
  return json({ ok: true });
}

export async function publishSession(req, env, params) {
  const g = await needSession(req, env, params.sessionId, 'edit'); if (g.resp) return g.resp;
  await ensureColumns(env);
  await audit(env, g.t, 'session.publish', `session ${g.ses.id}`);
  const ses = await env.DB.prepare('SELECT * FROM test_sessions WHERE id = ?1').bind(params.sessionId).first();
  if (!ses) return err('Session not found.', 404);
  const endIso = ses.scheduled_end || new Date(Date.parse(ses.scheduled_start) + ses.duration_minutes * 60000).toISOString();
  await finalizeSession(env, ses.id, endIso);
  await env.DB.prepare("UPDATE results SET published_at = datetime('now') WHERE session_id = ?1").bind(params.sessionId).run();
  return json({ ok: true });
}

export async function deleteSession(req, env, params) {
  const g = await needSession(req, env, params.sessionId, 'edit'); if (g.resp) return g.resp;
  await env.DB.prepare('DELETE FROM responses WHERE session_id = ?1').bind(params.sessionId).run();
  await env.DB.prepare('DELETE FROM results WHERE session_id = ?1').bind(params.sessionId).run();
  await env.DB.prepare('DELETE FROM session_questions WHERE session_id = ?1').bind(params.sessionId).run();
  await env.DB.prepare('DELETE FROM exam_events WHERE session_id = ?1').bind(params.sessionId).run();
  await env.DB.prepare('DELETE FROM session_notes WHERE session_id = ?1').bind(params.sessionId).run();
  const result = await env.DB.prepare('DELETE FROM test_sessions WHERE id = ?1').bind(params.sessionId).run();
  if (!result.meta.rows_written) return err('Session not found.', 404);
  return json({ ok: true });
}

export async function setWritingScoresBulk(req, env, params) {
  const g = await needSession(req, env, params.sessionId, 'edit'); if (g.resp) return g.resp;
  await ensureColumns(env);
  const { scores } = await req.json();
  if (!Array.isArray(scores)) return err('scores array is required.', 400);
  await audit(env, g.t, 'session.writing_bulk', `session ${g.ses.id}, ${scores.length} students`);

  const statements = [];
  for (const s of scores) {
    if (!s.student_id) continue;
    statements.push(
      env.DB.prepare(
        `INSERT INTO results (session_id, student_id, mcq_score, mcq_max, writing_score, writing_max)
         VALUES (?1, ?2, 0, 0, ?3, ?4)
         ON CONFLICT(session_id, student_id) DO UPDATE SET writing_score = ?3, writing_max = ?4`
      ).bind(params.sessionId, s.student_id, s.writing_score ?? null, s.writing_max ?? null)
    );
  }
  if (statements.length > 0) {
    await env.DB.batch(statements);
  }
  return json({ ok: true, count: statements.length });
}

export async function resetStudentSession(req, env, params) {
  const g = await needSession(req, env, params.sessionId, 'edit'); if (g.resp) return g.resp;
  await ensureColumns(env);
  const { student_id } = await req.json();
  if (!student_id) return err('student_id is required.', 400);

  // Clear submitted_at and submit_type so the student can re-enter their open test
  // Previously saved answers in `responses` table are preserved so they don't lose work!
  await env.DB.prepare(
    "UPDATE results SET submitted_at = NULL, submit_type = NULL WHERE session_id = ?1 AND student_id = ?2"
  ).bind(params.sessionId, student_id).run();

  return json({ ok: true });
}

// Per-question statistics and every student's answers, for the teacher's review.
export async function sessionAnalysis(req, env, params) {
  const g = await needSession(req, env, params.sessionId, 'view'); if (g.resp) return g.resp;
  await ensureColumns(env);
  const ses = await env.DB.prepare('SELECT id, test_id FROM test_sessions WHERE id = ?1').bind(params.sessionId).first();
  if (!ses) return err('Session not found.', 404);
  const qs = mcqOnly(await sessionQuestions(env, ses.id, ses.test_id));
  const { results: rs } = await env.DB.prepare(
    'SELECT student_id, question_id, selected_index FROM responses WHERE session_id = ?1',
  ).bind(ses.id).all();
  const answers = {};
  for (const r of rs) (answers[r.student_id] ||= {})[r.question_id] = r.selected_index;
  const questions = qs.map((q) => {
    const options = JSON.parse(q.options_json);
    const counts = options.map(() => 0);
    let answered = 0;
    for (const a of Object.values(answers)) {
      const v = a[q.id];
      if (v != null && counts[v] != null) { counts[v]++; answered++; }
    }
    return { id: q.id, order_no: q.order_no, stem_text: q.stem_text, options, correct_index: q.correct_index, alt_correct_index: q.alt_correct_index, cancelled: q.cancelled, points: q.points, topic: q.topic, level: q.level, counts, answered };
  });
  return json({ questions, answers, student_count: Object.keys(answers).length });
}

// One row per session with class-level statistics, for the "all classes" page.
export async function overview(req, env) {
  const t = await authTeacher(req, env);
  if (!t) return err('Not logged in.', 401);
  await ensureColumns(env);
  const mine = await accessibleClasses(env, t);
  const { results } = await env.DB.prepare(
    `SELECT ts.id, ts.class_id, ts.scheduled_start, ts.scheduled_end, ts.duration_minutes, ts.status,
            c.name AS class_name, t.id AS test_id, t.title AS test_title,
            COALESCE((SELECT SUM(sq.points) FROM session_questions sq WHERE sq.session_id = ts.id AND sq.kind <> 'writing'),
                     (SELECT SUM(points) FROM test_questions q WHERE q.test_id = t.id AND q.kind <> 'writing'), 0) AS mcq_max,
            (SELECT COUNT(*) FROM students s WHERE s.class_id = ts.class_id) AS total_students
     FROM test_sessions ts JOIN classes c ON c.id = ts.class_id JOIN tests t ON t.id = ts.test_id
     ORDER BY ts.scheduled_start DESC`,
  ).all();
  const { results: rs } = await env.DB.prepare(
    `SELECT session_id, mcq_score, writing_score, writing_max FROM results WHERE submitted_at IS NOT NULL`,
  ).all();
  const bySession = {};
  for (const r of rs) (bySession[r.session_id] ||= []).push(r);
  const sessions = results.filter((s) => mine.has(s.class_id)).map((s) => {
    const endIso = s.scheduled_end || new Date(Date.parse(s.scheduled_start) + s.duration_minutes * 60000).toISOString();
    const phase = sessionWindow({ ...s, scheduled_end: endIso }).phase;
    const pcts = (bySession[s.id] || []).map((r) => {
      const max = s.mcq_max + (r.writing_max ?? 0);
      return max > 0 ? ((r.mcq_score + (r.writing_score ?? 0)) / max) * 100 : 0;
    });
    const n = pcts.length;
    return {
      ...s, scheduled_end: endIso, phase, submitted: n,
      avg_pct: n ? Math.round(pcts.reduce((a, b) => a + b, 0) / n) : null,
      max_pct: n ? Math.round(Math.max(...pcts)) : null,
      min_pct: n ? Math.round(Math.min(...pcts)) : null,
      pass_count: pcts.filter((p) => p >= 50).length,
    };
  });
  return json({ sessions });
}

export async function updateSessionPin(req, env, params) {
  const g = await needSession(req, env, params.sessionId, 'edit'); if (g.resp) return g.resp;
  await ensureColumns(env);
  const { pin } = await req.json();
  const clean = String(pin ?? '').trim();
  if (!/^[0-9A-Za-z]{3,12}$/.test(clean)) return err('PIN must be 3–12 letters or digits.', 400);
  await env.DB.prepare('UPDATE test_sessions SET pin = ?1 WHERE id = ?2').bind(clean, params.sessionId).run();
  return json({ ok: true, pin: clean });
}

// Score unsubmitted students if the session is over (used by the yearly gradebook).
export async function finalizeIfClosed(env, sessionId) {
  await ensureColumns(env);
  const ses = await env.DB.prepare('SELECT * FROM test_sessions WHERE id = ?1').bind(sessionId).first();
  if (!ses) return;
  const endIso = ses.scheduled_end || new Date(Date.parse(ses.scheduled_start) + ses.duration_minutes * 60000).toISOString();
  if (sessionWindow({ ...ses, scheduled_end: endIso }).phase === 'closed') await finalizeSession(env, ses.id, endIso);
}

// ---------- exam-day controls ----------
const iso = (ms) => new Date(ms).toISOString();

// Give the whole class more time, or one student (extra minutes on top of the end time).
export async function extendSession(req, env, params) {
  const g = await needSession(req, env, params.sessionId, 'edit'); if (g.resp) return g.resp;
  const { minutes, student_id } = await req.json();
  const m = Math.round(Number(minutes));
  if (!(m >= 1 && m <= 240)) return err('minutes must be between 1 and 240.', 400);
  if (student_id) {
    const stu = await env.DB.prepare('SELECT id FROM students WHERE id = ?1 AND class_id = ?2').bind(String(student_id), g.ses.class_id).first();
    if (!stu) return err('Student not found.', 404);
    await env.DB.prepare(
      `INSERT INTO results (session_id, student_id, mcq_score, mcq_max, extra_minutes) VALUES (?1, ?2, 0, 0, ?3)
       ON CONFLICT(session_id, student_id) DO UPDATE SET extra_minutes = extra_minutes + ?3`,
    ).bind(g.ses.id, stu.id, m).run();
    await audit(env, g.t, 'session.extend_student', `session ${g.ses.id}, ${stu.id} +${m}m`);
    return json({ ok: true });
  }
  const ses = await env.DB.prepare('SELECT * FROM test_sessions WHERE id = ?1').bind(g.ses.id).first();
  if (ses.status === 'closed') return err('ការប្រឡងនេះត្រូវបានបិទដោយដៃ។', 400);
  const end = ses.scheduled_end ? Date.parse(ses.scheduled_end) : Date.parse(ses.scheduled_start) + ses.duration_minutes * 60000;
  await env.DB.prepare('UPDATE test_sessions SET scheduled_end = ?1, duration_minutes = duration_minutes + ?2 WHERE id = ?3')
    .bind(iso(end + m * 60000), m, ses.id).run();
  await audit(env, g.t, 'session.extend', `session ${ses.id} +${m}m`);
  return json({ ok: true });
}

// Teacher submits a student's saved answers on their behalf (e.g. phone died).
export async function forceSubmit(req, env, params) {
  const g = await needSession(req, env, params.sessionId, 'edit'); if (g.resp) return g.resp;
  const { student_id } = await req.json();
  const row = await env.DB.prepare('SELECT submitted_at FROM results WHERE session_id = ?1 AND student_id = ?2').bind(g.ses.id, String(student_id)).first();
  if (row && row.submitted_at) return err('សិស្សនេះបានប្រគល់រួចហើយ។', 400);
  const r = await submitStudent(env, g.ses, String(student_id), 'forced');
  await audit(env, g.t, 'session.force_submit', `session ${g.ses.id}, ${student_id}, ${r.score}/${r.max}`);
  return json({ ok: true, score: r.score, max: r.max });
}

// Lets a student continue on a different phone (clears the device lock).
export async function resetDevice(req, env, params) {
  const g = await needSession(req, env, params.sessionId, 'edit'); if (g.resp) return g.resp;
  const { student_id } = await req.json();
  await env.DB.prepare('UPDATE results SET device_id = NULL WHERE session_id = ?1 AND student_id = ?2').bind(g.ses.id, String(student_id)).run();
  return json({ ok: true });
}

// Re-score after the answer key changed.
export async function rescoreOne(req, env, params) {
  const g = await needSession(req, env, params.sessionId, 'edit'); if (g.resp) return g.resp;
  const r = await rescoreSession(env, g.ses.id);
  await audit(env, g.t, 'session.rescore', `session ${g.ses.id}: ${r.changed}/${r.total} changed`);
  return json({ ok: true, ...r });
}

// ---------- per-question writing marks ----------
export async function getWritingMarks(req, env, params) {
  const g = await needSession(req, env, params.sessionId, 'view'); if (g.resp) return g.resp;
  await ensureColumns(env);
  const qs = (await sessionQuestions(env, g.ses.id, g.ses.test_id)).filter((q) => q.kind === 'writing').map((q) => ({ id: q.id, order_no: q.order_no, stem_text: q.stem_text, points: q.points, solution_text: q.solution_text }));
  const { results: marks } = await env.DB.prepare('SELECT student_id, question_id, score FROM writing_marks WHERE session_id = ?1').bind(g.ses.id).all();
  return json({ questions: qs, marks });
}

export async function setWritingMarks(req, env, params) {
  const g = await needSession(req, env, params.sessionId, 'edit'); if (g.resp) return g.resp;
  const { student_id, marks } = await req.json();
  const qs = (await sessionQuestions(env, g.ses.id, g.ses.test_id)).filter((q) => q.kind === 'writing');
  const byId = Object.fromEntries(qs.map((q) => [q.id, q]));
  const stmts = [];
  let total = 0;
  for (const [qid, val] of Object.entries(marks || {})) {
    const q = byId[qid];
    if (!q) continue;
    if (val === '' || val === null) { stmts.push(env.DB.prepare('DELETE FROM writing_marks WHERE session_id = ?1 AND student_id = ?2 AND question_id = ?3').bind(g.ses.id, student_id, q.id)); continue; }
    const v = Number(val);
    if (!(v >= 0 && v <= q.points)) return err(`ពិន្ទុសំណួរមួយត្រូវនៅចន្លោះ 0 ដល់ ${q.points}។`, 400);
    total += v;
    stmts.push(env.DB.prepare('INSERT INTO writing_marks (session_id, student_id, question_id, score) VALUES (?1, ?2, ?3, ?4) ON CONFLICT(session_id, student_id, question_id) DO UPDATE SET score = ?4').bind(g.ses.id, student_id, q.id, v));
  }
  const max = qs.reduce((t, q) => t + q.points, 0);
  stmts.push(env.DB.prepare(
    `INSERT INTO results (session_id, student_id, mcq_score, mcq_max, writing_score, writing_max) VALUES (?1, ?2, 0, 0, ?3, ?4)
     ON CONFLICT(session_id, student_id) DO UPDATE SET writing_score = ?3, writing_max = ?4`,
  ).bind(g.ses.id, student_id, total, max));
  await env.DB.batch(stmts);
  await audit(env, g.t, 'session.writing_marks', `session ${g.ses.id}, ${student_id}: ${total}/${max}`);
  return json({ ok: true, writing_score: total, writing_max: max });
}
