import { json, err } from '../lib/http.js';
import { requireTeacher } from '../lib/session.js';
import { sessionWindow } from '../lib/time.js';

let columnsChecked = false;
export async function ensureColumns(env) {
  if (columnsChecked) return;
  try { await env.DB.prepare("ALTER TABLE results ADD COLUMN started_at TEXT").run(); } catch {}
  try { await env.DB.prepare("ALTER TABLE results ADD COLUMN submit_type TEXT").run(); } catch {}
  try { await env.DB.prepare("ALTER TABLE test_sessions ADD COLUMN scheduled_end TEXT").run(); } catch {}
  try { await env.DB.prepare("ALTER TABLE test_sessions ADD COLUMN pin TEXT").run(); } catch {}
  try { await env.DB.prepare("ALTER TABLE test_questions ADD COLUMN kind TEXT NOT NULL DEFAULT 'mcq'").run(); } catch {}
  try { await env.DB.prepare("ALTER TABLE test_questions ADD COLUMN solution_text TEXT").run(); } catch {}
  try { await env.DB.prepare("ALTER TABLE results ADD COLUMN tab_switches INTEGER NOT NULL DEFAULT 0").run(); } catch {}
  columnsChecked = true;
}

// A student who never pressed Submit (closed the browser, phone died, time ran
// out while offline) has saved answers but no score. Once the session is over,
// score those answers on the server so the teacher always sees a result.
export async function finalizeSession(env, sessionId, endIso) {
  await env.DB.prepare(
    `INSERT INTO results (session_id, student_id, mcq_score, mcq_max)
     SELECT DISTINCT session_id, student_id, 0, 0 FROM responses WHERE session_id = ?1
     ON CONFLICT(session_id, student_id) DO NOTHING`,
  ).bind(sessionId).run();
  await env.DB.prepare(
    `UPDATE results SET
       mcq_score = COALESCE((SELECT SUM(q.points) FROM responses r
                             JOIN test_questions q ON q.id = r.question_id AND q.correct_index = r.selected_index AND q.kind <> 'writing'
                             WHERE r.session_id = results.session_id AND r.student_id = results.student_id), 0),
       mcq_max = (SELECT COALESCE(SUM(q.points), 0) FROM test_questions q
                  JOIN test_sessions ts ON ts.test_id = q.test_id WHERE ts.id = results.session_id AND q.kind <> 'writing'),
       submitted_at = datetime(?2),
       submit_type = 'auto'
     WHERE session_id = ?1 AND submitted_at IS NULL
       AND (started_at IS NOT NULL OR EXISTS (SELECT 1 FROM responses r WHERE r.session_id = results.session_id AND r.student_id = results.student_id))`,
  ).bind(sessionId, new Date(Math.min(Date.parse(endIso), Date.now())).toISOString()).run();
}

export async function listSessions(req, env) {
  if (!(await requireTeacher(req, env))) return err('Not logged in.', 401);
  await ensureColumns(env);
  const { results } = await env.DB.prepare(
    `SELECT ts.id, ts.scheduled_start, ts.duration_minutes, ts.scheduled_end, ts.status, ts.pin,
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
  for (const s of results) {
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
  if (!(await requireTeacher(req, env))) return err('Not logged in.', 401);
  await ensureColumns(env);
  const { test_id, class_id, scheduled_start, duration_minutes, scheduled_end, pin } = await req.json();
  if (!test_id || !class_id || !scheduled_start || !duration_minutes) {
    return err('test_id, class_id, scheduled_start, and duration_minutes are required.', 400);
  }
  const endIso = scheduled_end || new Date(Date.parse(scheduled_start) + Number(duration_minutes) * 60000).toISOString();
  const cleanPin = String(pin ?? '').trim();
  if (cleanPin && !/^[0-9A-Za-z]{3,12}$/.test(cleanPin)) return err('PIN must be 3–12 letters or digits.', 400);
  const finalPin = cleanPin || String(Math.floor(1000 + Math.random() * 9000));
  const { meta } = await env.DB.prepare(
    'INSERT INTO test_sessions (test_id, class_id, scheduled_start, duration_minutes, scheduled_end, pin) VALUES (?1, ?2, ?3, ?4, ?5, ?6)',
  ).bind(test_id, class_id, scheduled_start, duration_minutes, endIso, finalPin).run();
  return json({ id: meta.last_row_id, pin: finalPin });
}

export async function getSession(req, env, params) {
  if (!(await requireTeacher(req, env))) return err('Not logged in.', 401);
  await ensureColumns(env);
  const session = await env.DB.prepare(
    `SELECT ts.id, ts.test_id, ts.class_id, ts.scheduled_start, ts.duration_minutes, ts.scheduled_end, ts.status, ts.pin,
            c.name AS class_name, t.title AS test_title
     FROM test_sessions ts JOIN classes c ON c.id = ts.class_id JOIN tests t ON t.id = ts.test_id
     WHERE ts.id = ?1`,
  ).bind(params.sessionId).first();
  if (!session) return err('Session not found.', 404);
  session.phase = sessionWindow(session).phase;

  const startMs = Date.parse(session.scheduled_start);
  const endMs = startMs + session.duration_minutes * 60000;
  session.scheduled_end = session.scheduled_end || new Date(endMs).toISOString();

  if (session.phase === 'closed') await finalizeSession(env, session.id, session.scheduled_end);

  const maxPointsRow = await env.DB.prepare('SELECT COALESCE(SUM(CASE WHEN kind = \'writing\' THEN 0 ELSE points END), 0) AS m, COALESCE(SUM(CASE WHEN kind = \'writing\' THEN points ELSE 0 END), 0) AS w FROM test_questions WHERE test_id = ?1')
    .bind(session.test_id).first();

  const { results: roster } = await env.DB.prepare(
    `SELECT s.id, s.surname, s.first_name, s.gender,
            r.mcq_score, r.mcq_max, r.writing_score, r.writing_max,
            r.started_at, r.submitted_at, r.submit_type, r.published_at, r.tab_switches,
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
  if (!(await requireTeacher(req, env))) return err('Not logged in.', 401);
  await env.DB.prepare("UPDATE test_sessions SET status = 'closed' WHERE id = ?1").bind(params.sessionId).run();
  return json({ ok: true });
}

export async function setWritingScore(req, env, params) {
  if (!(await requireTeacher(req, env))) return err('Not logged in.', 401);
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
  if (!(await requireTeacher(req, env))) return err('Not logged in.', 401);
  await ensureColumns(env);
  const ses = await env.DB.prepare('SELECT * FROM test_sessions WHERE id = ?1').bind(params.sessionId).first();
  if (!ses) return err('Session not found.', 404);
  const endIso = ses.scheduled_end || new Date(Date.parse(ses.scheduled_start) + ses.duration_minutes * 60000).toISOString();
  await finalizeSession(env, ses.id, endIso);
  await env.DB.prepare("UPDATE results SET published_at = datetime('now') WHERE session_id = ?1").bind(params.sessionId).run();
  return json({ ok: true });
}

export async function deleteSession(req, env, params) {
  if (!(await requireTeacher(req, env))) return err('Not logged in.', 401);
  await env.DB.prepare('DELETE FROM responses WHERE session_id = ?1').bind(params.sessionId).run();
  await env.DB.prepare('DELETE FROM results WHERE session_id = ?1').bind(params.sessionId).run();
  const result = await env.DB.prepare('DELETE FROM test_sessions WHERE id = ?1').bind(params.sessionId).run();
  if (!result.meta.rows_written) return err('Session not found.', 404);
  return json({ ok: true });
}

export async function setWritingScoresBulk(req, env, params) {
  if (!(await requireTeacher(req, env))) return err('Not logged in.', 401);
  await ensureColumns(env);
  const { scores } = await req.json();
  if (!Array.isArray(scores)) return err('scores array is required.', 400);

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
  if (!(await requireTeacher(req, env))) return err('Not logged in.', 401);
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
  if (!(await requireTeacher(req, env))) return err('Not logged in.', 401);
  await ensureColumns(env);
  const ses = await env.DB.prepare('SELECT id, test_id FROM test_sessions WHERE id = ?1').bind(params.sessionId).first();
  if (!ses) return err('Session not found.', 404);
  const { results: qs } = await env.DB.prepare(
    "SELECT id, order_no, stem_text, options_json, correct_index, points FROM test_questions WHERE test_id = ?1 AND kind <> 'writing' ORDER BY order_no",
  ).bind(ses.test_id).all();
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
    return { id: q.id, order_no: q.order_no, stem_text: q.stem_text, options, correct_index: q.correct_index, points: q.points, counts, answered };
  });
  return json({ questions, answers, student_count: Object.keys(answers).length });
}

// One row per session with class-level statistics, for the "all classes" page.
export async function overview(req, env) {
  if (!(await requireTeacher(req, env))) return err('Not logged in.', 401);
  await ensureColumns(env);
  const { results } = await env.DB.prepare(
    `SELECT ts.id, ts.scheduled_start, ts.scheduled_end, ts.duration_minutes, ts.status,
            c.name AS class_name, t.id AS test_id, t.title AS test_title,
            (SELECT COALESCE(SUM(points), 0) FROM test_questions q WHERE q.test_id = t.id AND q.kind <> 'writing') AS mcq_max,
            (SELECT COUNT(*) FROM students s WHERE s.class_id = ts.class_id) AS total_students
     FROM test_sessions ts JOIN classes c ON c.id = ts.class_id JOIN tests t ON t.id = ts.test_id
     ORDER BY ts.scheduled_start DESC`,
  ).all();
  const { results: rs } = await env.DB.prepare(
    `SELECT session_id, mcq_score, writing_score, writing_max FROM results WHERE submitted_at IS NOT NULL`,
  ).all();
  const bySession = {};
  for (const r of rs) (bySession[r.session_id] ||= []).push(r);
  const sessions = results.map((s) => {
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
  if (!(await requireTeacher(req, env))) return err('Not logged in.', 401);
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
