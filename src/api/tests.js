import { json, err } from '../lib/http.js';
import { ensureColumns } from '../lib/schema.js';
import { authTeacher, needTest, needQuestion, needLicense, needAdmin, accessibleTests, lockedResponse } from '../lib/access.js';

export async function listTests(req, env) {
  const t = await authTeacher(req, env);
  if (!t) return err('Not logged in.', 401);
  const mine = await accessibleTests(env, t);
  const { results } = await env.DB.prepare(
    `SELECT x.id, x.title, x.status, x.owner_id, x.is_sample, COALESCE(o.display_name, o.username) AS owner_name,
            COUNT(q.id) AS question_count, SUM(CASE WHEN q.kind = 'writing' THEN 1 ELSE 0 END) AS writing_count,
            COALESCE(SUM(q.points), 0) AS total_points,
            (SELECT COUNT(*) FROM test_sessions s WHERE s.test_id = x.id) AS session_count,
            (SELECT COUNT(*) FROM question_notes n JOIN test_questions nq ON nq.id = n.question_id WHERE nq.test_id = x.id AND n.resolved = 0) AS open_notes
     FROM tests x LEFT JOIN test_questions q ON q.test_id = x.id LEFT JOIN teachers o ON o.id = x.owner_id
     GROUP BY x.id ORDER BY x.created_at DESC`,
  ).all();
  return json({ tests: results.filter((x) => mine.has(x.id)).map((x) => ({ ...x, my_role: mine.get(x.id) })) });
}

export async function createTest(req, env) {
  const g0 = await needLicense(req, env); if (g0.resp) return g0.resp;
  const t = g0.t;
  const { title } = await req.json();
  if (!title) return err('title is required.', 400);
  const { meta } = await env.DB.prepare('INSERT INTO tests (title, owner_id) VALUES (?1, ?2)').bind(title, t.id).run();
  return json({ id: meta.last_row_id, title, status: 'draft' });
}

export async function getTest(req, env, params) {
  const g = await needTest(req, env, params.testId, 'view'); if (g.resp) return g.resp;
  await ensureColumns(env);
  const test = await env.DB.prepare('SELECT id, title, status FROM tests WHERE id = ?1').bind(params.testId).first();
  if (!test) return err('Test not found.', 404);
  const { results } = await env.DB.prepare(
    'SELECT id, order_no, stem_text, image_key, options_json, correct_index, points, kind, solution_text FROM test_questions WHERE test_id = ?1 ORDER BY order_no',
  ).bind(params.testId).all();
  const { results: notes } = await env.DB.prepare(
    `SELECT n.id, n.question_id, n.body, n.resolved, n.created_at, n.teacher_id, COALESCE(t.display_name, t.username) AS author
     FROM question_notes n JOIN test_questions q ON q.id = n.question_id LEFT JOIN teachers t ON t.id = n.teacher_id
     WHERE q.test_id = ?1 ORDER BY n.id`,
  ).bind(params.testId).all();
  const showcase = g.acc === 'sample';   // sample tests never reveal the answer key
  test.questions = results.map((q) => ({
    ...q, options: JSON.parse(q.options_json), options_json: undefined,
    correct_index: showcase ? null : q.correct_index, solution_text: showcase ? null : q.solution_text,
    notes: showcase ? [] : notes.filter((n) => n.question_id === q.id),
  }));
  test.my_role = g.acc;
  test.my_id = g.t.id;
  return json(test);
}

export async function updateTest(req, env, params) {
  const g = await needTest(req, env, params.testId, 'edit'); if (g.resp) return g.resp;
  const { title, status } = await req.json();
  await env.DB.prepare('UPDATE tests SET title = COALESCE(?1, title), status = COALESCE(?2, status) WHERE id = ?3')
    .bind(title ?? null, status ?? null, params.testId).run();
  return json({ ok: true });
}

export async function addQuestion(req, env, params) {
  const g = await needTest(req, env, params.testId, 'edit'); if (g.resp) return g.resp;
  await ensureColumns(env);
  const { stem_text, options, correct_index, points, image_key, kind, solution_text } = await req.json();
  const isWriting = kind === 'writing';
  if (!stem_text) return err('stem_text is required.', 400);
  if (!isWriting) {
    if (!Array.isArray(options) || options.length < 2) return err('stem_text and at least two options are required.', 400);
    if (!Number.isInteger(correct_index) || correct_index < 0 || correct_index >= options.length) {
      return err('correct_index must point at one of the options.', 400);
    }
  }
  const { results } = await env.DB.prepare('SELECT COALESCE(MAX(order_no), 0) AS m FROM test_questions WHERE test_id = ?1')
    .bind(params.testId).all();
  const orderNo = results[0].m + 1;
  const { meta } = await env.DB.prepare(
    'INSERT INTO test_questions (test_id, order_no, stem_text, image_key, options_json, correct_index, points, kind, solution_text) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9)',
  ).bind(params.testId, orderNo, stem_text, image_key || null, JSON.stringify(isWriting ? [] : options), isWriting ? 0 : correct_index, points || 1, isWriting ? 'writing' : 'mcq', solution_text || null).run();
  return json({ id: meta.last_row_id, order_no: orderNo });
}

export async function updateQuestion(req, env, params) {
  const g = await needQuestion(req, env, params.questionId, 'edit'); if (g.resp) return g.resp;
  await ensureColumns(env);
  const { stem_text, options, correct_index, points, image_key, solution_text } = await req.json();
  await env.DB.prepare(
    `UPDATE test_questions SET
       solution_text = COALESCE(?7, solution_text),
       stem_text = COALESCE(?1, stem_text),
       options_json = COALESCE(?2, options_json),
       correct_index = COALESCE(?3, correct_index),
       points = COALESCE(?4, points),
       image_key = COALESCE(?5, image_key)
     WHERE id = ?6`,
  ).bind(stem_text ?? null, options ? JSON.stringify(options) : null, correct_index ?? null, points ?? null, image_key ?? null, params.questionId, solution_text ?? null).run();
  return json({ ok: true });
}

export async function deleteQuestion(req, env, params) {
  const g = await needQuestion(req, env, params.questionId, 'edit'); if (g.resp) return g.resp;
  await env.DB.prepare('DELETE FROM test_questions WHERE id = ?1').bind(params.questionId).run();
  return json({ ok: true });
}

export async function deleteTest(req, env, params) {
  const g = await needTest(req, env, params.testId, 'own'); if (g.resp) return g.resp;
  await env.DB.prepare('DELETE FROM question_notes WHERE question_id IN (SELECT id FROM test_questions WHERE test_id = ?1)').bind(params.testId).run();
  await env.DB.prepare("DELETE FROM shares WHERE resource_type = 'test' AND resource_id = ?1").bind(params.testId).run();
  await env.DB.prepare('DELETE FROM test_questions WHERE test_id = ?1').bind(params.testId).run();
  await env.DB.prepare('DELETE FROM test_sessions WHERE test_id = ?1').bind(params.testId).run();
  const result = await env.DB.prepare('DELETE FROM tests WHERE id = ?1').bind(params.testId).run();
  if (!result.meta.rows_written) return err('Test not found.', 404);
  return json({ ok: true });
}

export async function duplicateTest(req, env, params) {
  const g = await needTest(req, env, params.testId, 'view'); if (g.resp) return g.resp;
  if (!g.t.licensed) return lockedResponse(g.t);
  await ensureColumns(env);
  const test = await env.DB.prepare('SELECT title FROM tests WHERE id = ?1').bind(params.testId).first();
  if (!test) return err('Test not found.', 404);
  const newTitle = `${test.title} (ចម្លង)`;
  const { meta } = await env.DB.prepare('INSERT INTO tests (title, status, owner_id) VALUES (?1, ?2, ?3)').bind(newTitle, 'draft', g.t.id).run();
  const newTestId = meta.last_row_id;

  const { results: questions } = await env.DB.prepare(
    'SELECT order_no, stem_text, image_key, options_json, correct_index, points, kind, solution_text FROM test_questions WHERE test_id = ?1 ORDER BY order_no'
  ).bind(params.testId).all();

  for (const q of questions) {
    await env.DB.prepare(
      'INSERT INTO test_questions (test_id, order_no, stem_text, image_key, options_json, correct_index, points, kind, solution_text) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9)'
    ).bind(newTestId, q.order_no, q.stem_text, q.image_key, q.options_json, q.correct_index, q.points, q.kind, q.solution_text).run();
  }

  return json({ id: newTestId, title: newTitle });
}

// ---- reviewer notes on a question (any teacher with access to the test may write one)
export async function addNote(req, env, params) {
  const g = await needQuestion(req, env, params.questionId, 'view'); if (g.resp) return g.resp;
  const { body } = await req.json();
  const text = String(body || '').trim();
  if (!text) return err('សូមសរសេរចំណាំ។', 400);
  if (text.length > 1000) return err('ចំណាំវែងពេក (អតិបរមា ១០០០ តួ)។', 400);
  const { meta } = await env.DB.prepare('INSERT INTO question_notes (question_id, teacher_id, body) VALUES (?1, ?2, ?3)')
    .bind(g.q.id, g.t.id, text).run();
  return json({ id: meta.last_row_id });
}

async function loadNote(env, t, noteId) {
  const n = await env.DB.prepare(
    'SELECT n.id, n.teacher_id, q.test_id FROM question_notes n JOIN test_questions q ON q.id = n.question_id WHERE n.id = ?1',
  ).bind(noteId).first();
  return n;
}

export async function resolveNote(req, env, params) {
  const t = await authTeacher(req, env);
  if (!t) return err('Not logged in.', 401);
  const n = await loadNote(env, t, params.noteId);
  if (!n) return err('Note not found.', 404);
  const g = await needTest(req, env, n.test_id, 'view'); if (g.resp) return g.resp;
  // The author, or anyone who can edit the test, may mark a note done.
  if (n.teacher_id !== t.id && g.acc === 'reviewer') return err('អ្នកមិនមានសិទ្ធិទេ។', 403);
  const { resolved } = await req.json();
  await env.DB.prepare('UPDATE question_notes SET resolved = ?1 WHERE id = ?2').bind(resolved ? 1 : 0, n.id).run();
  return json({ ok: true });
}

export async function deleteNote(req, env, params) {
  const t = await authTeacher(req, env);
  if (!t) return err('Not logged in.', 401);
  const n = await loadNote(env, t, params.noteId);
  if (!n) return err('Note not found.', 404);
  const g = await needTest(req, env, n.test_id, 'view'); if (g.resp) return g.resp;
  if (n.teacher_id !== t.id && g.acc !== 'owner') return err('អ្នកមិនមានសិទ្ធិទេ។', 403);
  await env.DB.prepare('DELETE FROM question_notes WHERE id = ?1').bind(n.id).run();
  return json({ ok: true });
}

// Owner only: mark a test as a showcase "sample" visible (read-only) to every teacher.
export async function setSample(req, env, params) {
  const g = await needAdmin(req, env); if (g.resp) return g.resp;
  const { is_sample } = await req.json();
  await env.DB.prepare('UPDATE tests SET is_sample = ?1 WHERE id = ?2').bind(is_sample ? 1 : 0, params.testId).run();
  return json({ ok: true });
}
