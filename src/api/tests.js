import { json, err } from '../lib/http.js';
import { ensureColumns } from '../lib/schema.js';
import { rescoreSession } from '../lib/scoring.js';
import { audit } from '../lib/audit.js';
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
    'SELECT id, order_no, stem_text, image_key, options_json, correct_index, alt_correct_index, cancelled, shuffle, topic, level, points, kind, solution_text FROM test_questions WHERE test_id = ?1 ORDER BY order_no',
  ).bind(params.testId).all();
  const { results: notes } = await env.DB.prepare(
    `SELECT n.id, n.question_id, n.body, n.resolved, n.created_at, n.teacher_id, COALESCE(t.display_name, t.username) AS author
     FROM question_notes n JOIN test_questions q ON q.id = n.question_id LEFT JOIN teachers t ON t.id = n.teacher_id
     WHERE q.test_id = ?1 ORDER BY n.id`,
  ).bind(params.testId).all();
  const showcase = g.acc === 'sample';   // sample tests never reveal the answer key
  test.questions = results.map((q) => ({
    ...q, options: JSON.parse(q.options_json), options_json: undefined,
    correct_index: showcase ? null : q.correct_index, alt_correct_index: showcase ? null : q.alt_correct_index, solution_text: showcase ? null : q.solution_text,
    notes: showcase ? [] : notes.filter((n) => n.question_id === q.id),
  }));
  const sub = await env.DB.prepare(
    'SELECT COUNT(*) AS n FROM results r JOIN test_sessions s ON s.id = r.session_id WHERE s.test_id = ?1 AND r.submitted_at IS NOT NULL',
  ).bind(params.testId).first();
  test.submissions = sub.n;
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
  const { stem_text, options, correct_index, points, image_key, kind, solution_text, topic, level, shuffle } = await req.json();
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
    'INSERT INTO test_questions (test_id, order_no, stem_text, image_key, options_json, correct_index, points, kind, solution_text, topic, level, shuffle) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10, ?11, ?12)',
  ).bind(params.testId, orderNo, stem_text, image_key || null, JSON.stringify(isWriting ? [] : options), isWriting ? 0 : correct_index, points || 1, isWriting ? 'writing' : 'mcq', solution_text || null, topic || null, level || null, shuffle ? 1 : 0).run();
  return json({ id: meta.last_row_id, order_no: orderNo });
}

export async function updateQuestion(req, env, params) {
  const g = await needQuestion(req, env, params.questionId, 'edit'); if (g.resp) return g.resp;
  await ensureColumns(env);
  const b = await req.json();
  const cur = await env.DB.prepare('SELECT * FROM test_questions WHERE id = ?1').bind(g.q.id).first();
  const isWriting = cur.kind === 'writing';
  const sets = []; const vals = [];
  const put = (col, v) => { sets.push(`${col} = ?${sets.length + 1}`); vals.push(v); };
  if (b.stem_text !== undefined) { if (!String(b.stem_text).trim()) return err('stem_text is required.', 400); put('stem_text', String(b.stem_text).trim()); }
  if (b.points !== undefined) { const p = Number(b.points); if (!(p > 0 && p <= 100)) return err('points must be between 1 and 100.', 400); put('points', Math.round(p)); }
  if (b.solution_text !== undefined) put('solution_text', b.solution_text ? String(b.solution_text) : null);
  if (b.image_key !== undefined) put('image_key', b.image_key || null);        // null/'' removes the picture
  if (b.topic !== undefined) put('topic', b.topic ? String(b.topic).trim().slice(0, 60) : null);
  if (b.level !== undefined) put('level', ['easy', 'medium', 'hard'].includes(b.level) ? b.level : null);
  if (!isWriting) {
    const options = b.options !== undefined ? b.options : JSON.parse(cur.options_json);
    if (!Array.isArray(options) || options.length < 2 || options.some((o) => !String(o).trim())) return err('At least two non-empty options are required.', 400);
    const correct = b.correct_index !== undefined ? Number(b.correct_index) : cur.correct_index;
    if (!Number.isInteger(correct) || correct < 0 || correct >= options.length) return err('correct_index must point at one of the options.', 400);
    let alt = b.alt_correct_index !== undefined ? b.alt_correct_index : cur.alt_correct_index;
    if (alt === '' || alt === undefined) alt = null;
    if (alt !== null) { alt = Number(alt); if (!Number.isInteger(alt) || alt < 0 || alt >= options.length || alt === correct) alt = null; }
    if (b.options !== undefined) put('options_json', JSON.stringify(options.map((o) => String(o))));
    if (b.correct_index !== undefined) put('correct_index', correct);
    if (b.alt_correct_index !== undefined || b.options !== undefined || b.correct_index !== undefined) put('alt_correct_index', alt);
    if (b.cancelled !== undefined) put('cancelled', b.cancelled ? 1 : 0);
    if (b.shuffle !== undefined) put('shuffle', b.shuffle ? 1 : 0);
  }
  if (!sets.length) return json({ ok: true });
  await env.DB.prepare(`UPDATE test_questions SET ${sets.join(', ')} WHERE id = ?${sets.length + 1}`).bind(...vals, g.q.id).run();
  const keyChanged = ['correct_index', 'alt_correct_index', 'cancelled', 'options'].some((k) => b[k] !== undefined);
  const { results } = await env.DB.prepare(
    `SELECT COUNT(*) AS n FROM results r JOIN test_sessions s ON s.id = r.session_id WHERE s.test_id = ?1 AND r.submitted_at IS NOT NULL`,
  ).bind(g.q.test_id).all();
  if (keyChanged) await audit(env, g.t, 'question.key_changed', `question ${g.q.id} (test ${g.q.test_id})`);
  return json({ ok: true, key_changed: keyChanged, submissions: results[0].n });
}

// Apply the current answer key to every session of this test.
export async function rescoreTest(req, env, params) {
  const g = await needTest(req, env, params.testId, 'edit'); if (g.resp) return g.resp;
  const { results: sessions } = await env.DB.prepare('SELECT id FROM test_sessions WHERE test_id = ?1').bind(params.testId).all();
  let changed = 0, total = 0;
  for (const s of sessions) { const r = await rescoreSession(env, s.id); changed += r.changed; total += r.total; }
  await audit(env, g.t, 'test.rescore', `test ${params.testId}: ${changed}/${total} changed`);
  return json({ ok: true, sessions: sessions.length, changed, total });
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
    'SELECT order_no, stem_text, image_key, options_json, correct_index, alt_correct_index, points, kind, solution_text, topic, level, shuffle FROM test_questions WHERE test_id = ?1 ORDER BY order_no'
  ).bind(params.testId).all();

  for (const q of questions) {
    await env.DB.prepare(
      'INSERT INTO test_questions (test_id, order_no, stem_text, image_key, options_json, correct_index, alt_correct_index, points, kind, solution_text, topic, level, shuffle) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10, ?11, ?12, ?13)'
    ).bind(newTestId, q.order_no, q.stem_text, q.image_key, q.options_json, q.correct_index, q.alt_correct_index, q.points, q.kind, q.solution_text, q.topic, q.level, q.shuffle).run();
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
