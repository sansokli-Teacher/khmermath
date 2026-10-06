import { json, err } from '../lib/http.js';
import { requireTeacher } from '../lib/session.js';
import { ensureColumns } from './sessions.js';

export async function listTests(req, env) {
  if (!(await requireTeacher(req, env))) return err('Not logged in.', 401);
  await ensureColumns(env);
  const { results } = await env.DB.prepare(
    `SELECT t.id, t.title, t.status, COUNT(q.id) AS question_count, SUM(CASE WHEN q.kind = 'writing' THEN 1 ELSE 0 END) AS writing_count
     FROM tests t LEFT JOIN test_questions q ON q.test_id = t.id
     GROUP BY t.id ORDER BY t.created_at DESC`,
  ).all();
  return json({ tests: results });
}

export async function createTest(req, env) {
  if (!(await requireTeacher(req, env))) return err('Not logged in.', 401);
  const { title } = await req.json();
  if (!title) return err('title is required.', 400);
  const { meta } = await env.DB.prepare('INSERT INTO tests (title) VALUES (?1)').bind(title).run();
  return json({ id: meta.last_row_id, title, status: 'draft' });
}

export async function getTest(req, env, params) {
  if (!(await requireTeacher(req, env))) return err('Not logged in.', 401);
  await ensureColumns(env);
  const test = await env.DB.prepare('SELECT id, title, status FROM tests WHERE id = ?1').bind(params.testId).first();
  if (!test) return err('Test not found.', 404);
  const { results } = await env.DB.prepare(
    'SELECT id, order_no, stem_text, image_key, options_json, correct_index, points, kind, solution_text FROM test_questions WHERE test_id = ?1 ORDER BY order_no',
  ).bind(params.testId).all();
  test.questions = results.map((q) => ({ ...q, options: JSON.parse(q.options_json), options_json: undefined }));
  return json(test);
}

export async function updateTest(req, env, params) {
  if (!(await requireTeacher(req, env))) return err('Not logged in.', 401);
  const { title, status } = await req.json();
  await env.DB.prepare('UPDATE tests SET title = COALESCE(?1, title), status = COALESCE(?2, status) WHERE id = ?3')
    .bind(title ?? null, status ?? null, params.testId).run();
  return json({ ok: true });
}

export async function addQuestion(req, env, params) {
  if (!(await requireTeacher(req, env))) return err('Not logged in.', 401);
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
  if (!(await requireTeacher(req, env))) return err('Not logged in.', 401);
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
  if (!(await requireTeacher(req, env))) return err('Not logged in.', 401);
  await env.DB.prepare('DELETE FROM test_questions WHERE id = ?1').bind(params.questionId).run();
  return json({ ok: true });
}

export async function deleteTest(req, env, params) {
  if (!(await requireTeacher(req, env))) return err('Not logged in.', 401);
  await env.DB.prepare('DELETE FROM test_questions WHERE test_id = ?1').bind(params.testId).run();
  await env.DB.prepare('DELETE FROM test_sessions WHERE test_id = ?1').bind(params.testId).run();
  const result = await env.DB.prepare('DELETE FROM tests WHERE id = ?1').bind(params.testId).run();
  if (!result.meta.rows_written) return err('Test not found.', 404);
  return json({ ok: true });
}

export async function duplicateTest(req, env, params) {
  if (!(await requireTeacher(req, env))) return err('Not logged in.', 401);
  await ensureColumns(env);
  const test = await env.DB.prepare('SELECT title FROM tests WHERE id = ?1').bind(params.testId).first();
  if (!test) return err('Test not found.', 404);
  const newTitle = `${test.title} (ចម្លង)`;
  const { meta } = await env.DB.prepare('INSERT INTO tests (title, status) VALUES (?1, ?2)').bind(newTitle, 'draft').run();
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
