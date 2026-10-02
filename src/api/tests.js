import { json, err } from '../lib/http.js';
import { requireTeacher } from '../lib/session.js';

export async function listTests(req, env) {
  if (!(await requireTeacher(req, env))) return err('Not logged in.', 401);
  const { results } = await env.DB.prepare(
    `SELECT t.id, t.title, t.status, COUNT(q.id) AS question_count
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
  const test = await env.DB.prepare('SELECT id, title, status FROM tests WHERE id = ?1').bind(params.testId).first();
  if (!test) return err('Test not found.', 404);
  const { results } = await env.DB.prepare(
    'SELECT id, order_no, stem_text, image_key, options_json, correct_index, points FROM test_questions WHERE test_id = ?1 ORDER BY order_no',
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
  const { stem_text, options, correct_index, points, image_key } = await req.json();
  if (!stem_text || !Array.isArray(options) || options.length < 2) {
    return err('stem_text and at least two options are required.', 400);
  }
  if (!Number.isInteger(correct_index) || correct_index < 0 || correct_index >= options.length) {
    return err('correct_index must point at one of the options.', 400);
  }
  const { results } = await env.DB.prepare('SELECT COALESCE(MAX(order_no), 0) AS m FROM test_questions WHERE test_id = ?1')
    .bind(params.testId).all();
  const orderNo = results[0].m + 1;
  const { meta } = await env.DB.prepare(
    'INSERT INTO test_questions (test_id, order_no, stem_text, image_key, options_json, correct_index, points) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7)',
  ).bind(params.testId, orderNo, stem_text, image_key || null, JSON.stringify(options), correct_index, points || 1).run();
  return json({ id: meta.last_row_id, order_no: orderNo });
}

export async function updateQuestion(req, env, params) {
  if (!(await requireTeacher(req, env))) return err('Not logged in.', 401);
  const { stem_text, options, correct_index, points, image_key } = await req.json();
  await env.DB.prepare(
    `UPDATE test_questions SET
       stem_text = COALESCE(?1, stem_text),
       options_json = COALESCE(?2, options_json),
       correct_index = COALESCE(?3, correct_index),
       points = COALESCE(?4, points),
       image_key = COALESCE(?5, image_key)
     WHERE id = ?6`,
  ).bind(stem_text ?? null, options ? JSON.stringify(options) : null, correct_index ?? null, points ?? null, image_key ?? null, params.questionId).run();
  return json({ ok: true });
}

export async function deleteQuestion(req, env, params) {
  if (!(await requireTeacher(req, env))) return err('Not logged in.', 401);
  await env.DB.prepare('DELETE FROM test_questions WHERE id = ?1').bind(params.questionId).run();
  return json({ ok: true });
}
