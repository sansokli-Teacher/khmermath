import { json, err } from '../lib/http.js';
import { requireTeacher } from '../lib/session.js';
import { sessionWindow } from '../lib/time.js';

let columnsChecked = false;
async function ensureColumns(env) {
  if (columnsChecked) return;
  try { await env.DB.prepare("ALTER TABLE results ADD COLUMN started_at TEXT").run(); } catch {}
  try { await env.DB.prepare("ALTER TABLE results ADD COLUMN submit_type TEXT").run(); } catch {}
  try { await env.DB.prepare("ALTER TABLE test_sessions ADD COLUMN scheduled_end TEXT").run(); } catch {}
  columnsChecked = true;
}

export async function listSessions(req, env) {
  if (!(await requireTeacher(req, env))) return err('Not logged in.', 401);
  await ensureColumns(env);
  const { results } = await env.DB.prepare(
    `SELECT ts.id, ts.scheduled_start, ts.duration_minutes, ts.scheduled_end, ts.status,
            c.name AS class_name, t.title AS test_title
     FROM test_sessions ts
     JOIN classes c ON c.id = ts.class_id
     JOIN tests t ON t.id = ts.test_id
     ORDER BY ts.scheduled_start DESC`,
  ).all();
  const withPhase = results.map((s) => {
    const startMs = Date.parse(s.scheduled_start);
    const endMs = startMs + s.duration_minutes * 60000;
    const computedEnd = s.scheduled_end || new Date(endMs).toISOString();
    return {
      ...s,
      scheduled_end: computedEnd,
      phase: sessionWindow(s).phase,
    };
  });
  return json({ sessions: withPhase });
}

export async function createSession(req, env) {
  if (!(await requireTeacher(req, env))) return err('Not logged in.', 401);
  await ensureColumns(env);
  const { test_id, class_id, scheduled_start, duration_minutes, scheduled_end } = await req.json();
  if (!test_id || !class_id || !scheduled_start || !duration_minutes) {
    return err('test_id, class_id, scheduled_start, and duration_minutes are required.', 400);
  }
  const endIso = scheduled_end || new Date(Date.parse(scheduled_start) + Number(duration_minutes) * 60000).toISOString();
  const { meta } = await env.DB.prepare(
    'INSERT INTO test_sessions (test_id, class_id, scheduled_start, duration_minutes, scheduled_end) VALUES (?1, ?2, ?3, ?4, ?5)',
  ).bind(test_id, class_id, scheduled_start, duration_minutes, endIso).run();
  return json({ id: meta.last_row_id });
}

export async function getSession(req, env, params) {
  if (!(await requireTeacher(req, env))) return err('Not logged in.', 401);
  await ensureColumns(env);
  const session = await env.DB.prepare(
    `SELECT ts.id, ts.test_id, ts.class_id, ts.scheduled_start, ts.duration_minutes, ts.scheduled_end, ts.status,
            c.name AS class_name, t.title AS test_title
     FROM test_sessions ts JOIN classes c ON c.id = ts.class_id JOIN tests t ON t.id = ts.test_id
     WHERE ts.id = ?1`,
  ).bind(params.sessionId).first();
  if (!session) return err('Session not found.', 404);
  session.phase = sessionWindow(session).phase;

  const startMs = Date.parse(session.scheduled_start);
  const endMs = startMs + session.duration_minutes * 60000;
  session.scheduled_end = session.scheduled_end || new Date(endMs).toISOString();

  const maxPointsRow = await env.DB.prepare('SELECT COALESCE(SUM(points), 0) AS m FROM test_questions WHERE test_id = ?1')
    .bind(session.test_id).first();

  const { results: roster } = await env.DB.prepare(
    `SELECT s.id, s.surname, s.first_name, s.gender,
            r.mcq_score, r.mcq_max, r.writing_score, r.writing_max,
            r.started_at, r.submitted_at, r.submit_type, r.published_at,
            (SELECT COUNT(*) FROM responses res WHERE res.session_id = ?1 AND res.student_id = s.id) AS answered_count
     FROM students s
     LEFT JOIN results r ON r.student_id = s.id AND r.session_id = ?1
     WHERE s.class_id = ?2 ORDER BY s.surname, s.first_name`,
  ).bind(params.sessionId, session.class_id).all();

  session.mcq_max = maxPointsRow.m;
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
