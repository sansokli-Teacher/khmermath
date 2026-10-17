import { GRADES, CHAPTERS, chapterOf, loadCurriculum } from '../lib/curriculum.js';
import { json, err } from '../lib/http.js';
import { ensureColumns } from '../lib/schema.js';
import { rescoreSession } from '../lib/scoring.js';
import { audit } from '../lib/audit.js';
import { syncKeyToFrozen, frozenCountForTest } from '../lib/frozen.js';
import { checkTemplate, sampleFor, hasVariants } from '../lib/variants.js';
import { authTeacher, needTest, needQuestion, needLicense, needAdmin, accessibleTests, lockedResponse, limitResponse, trialUsage } from '../lib/access.js';
import { TRIAL } from '../lib/plans.js';

export async function listTests(req, env) {
  const t = await authTeacher(req, env);
  if (!t) return err('Not logged in.', 401);
  await ensureColumns(env);
  const mine = await accessibleTests(env, t);
  const { results } = await env.DB.prepare(
    `SELECT x.id, x.title, x.status, x.owner_id, x.is_sample, COALESCE(o.display_name, o.username) AS owner_name,
            COUNT(q.id) AS question_count, SUM(CASE WHEN q.kind = 'writing' THEN 1 ELSE 0 END) AS writing_count,
            COALESCE(SUM(q.points), 0) AS total_points,
            (SELECT COUNT(*) FROM test_sessions s WHERE s.test_id = x.id) AS session_count,
            (SELECT COUNT(*) FROM question_notes n JOIN test_questions nq ON nq.id = n.question_id WHERE nq.test_id = x.id AND n.resolved = 0) AS open_notes
     FROM tests x LEFT JOIN test_questions q ON q.test_id = x.id LEFT JOIN teachers o ON o.id = x.owner_id
     WHERE x.is_bank = 0
     GROUP BY x.id ORDER BY x.created_at DESC`,
  ).all();
  return json({ tests: results.filter((x) => mine.has(x.id)).map((x) => ({ ...x, my_role: mine.get(x.id) })) });
}

export async function createTest(req, env) {
  const g0 = await needLicense(req, env, true); if (g0.resp) return g0.resp;
  const t = g0.t;
  if (t.status === 'trial' && (await trialUsage(env, t)).tests >= TRIAL.tests) return limitResponse('តេស្ត', TRIAL.tests);
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
    'SELECT id, order_no, stem_text, image_key, options_json, correct_index, alt_correct_index, cancelled, shuffle, topic, level, grade, lesson, points, kind, solution_text, params FROM test_questions WHERE test_id = ?1 ORDER BY order_no',
  ).bind(params.testId).all();
  const { results: notes } = await env.DB.prepare(
    `SELECT n.id, n.question_id, n.body, n.resolved, n.created_at, n.teacher_id, COALESCE(t.display_name, t.username) AS author
     FROM question_notes n JOIN test_questions q ON q.id = n.question_id LEFT JOIN teachers t ON t.id = n.teacher_id
     WHERE q.test_id = ?1 ORDER BY n.id`,
  ).bind(params.testId).all();
  const showcase = g.acc === 'sample';   // sample tests never reveal the answer key
  test.questions = results.map((q) => ({
    ...q, options: JSON.parse(q.options_json), options_json: undefined,
    sample: hasVariants(q) && !showcase ? sampleFor(q, `paper:${params.testId}`) : undefined,   // what paper / preview shows for a question with variants
    correct_index: showcase ? null : q.correct_index, alt_correct_index: showcase ? null : q.alt_correct_index, solution_text: showcase ? null : q.solution_text,
    notes: showcase ? [] : notes.filter((n) => n.question_id === q.id),
  }));
  const sub = await env.DB.prepare(
    'SELECT COUNT(*) AS n FROM results r JOIN test_sessions s ON s.id = r.session_id WHERE s.test_id = ?1 AND r.submitted_at IS NOT NULL',
  ).bind(params.testId).first();
  test.submissions = sub.n;
  test.frozen_sessions = await frozenCountForTest(env, params.testId);
  test.my_role = g.acc;
  test.my_id = g.t.id;
  return json(test);
}

export async function updateTest(req, env, params) {
  const g = await needTest(req, env, params.testId, 'edit'); if (g.resp) return g.resp;
  let { title, status } = await req.json();
  if (title !== undefined && title !== null) { title = String(title).trim().slice(0, 150); if (!title) return err('title is required.', 400); }
  await env.DB.prepare('UPDATE tests SET title = COALESCE(?1, title), status = COALESCE(?2, status) WHERE id = ?3')
    .bind(title ?? null, status ?? null, params.testId).run();
  return json({ ok: true });
}

const questionRoom = async (env, t, testId) => (t.status === 'trial'
  ? TRIAL.questions - (await env.DB.prepare('SELECT COUNT(*) AS n FROM test_questions WHERE test_id = ?1').bind(testId).first()).n
  : Infinity);

export async function addQuestion(req, env, params) {
  const g = await needTest(req, env, params.testId, 'edit'); if (g.resp) return g.resp;
  await ensureColumns(env);
  if ((await questionRoom(env, g.t, params.testId)) <= 0) return limitResponse('សំណួរក្នុងមួយតេស្ត', TRIAL.questions);
  const { stem_text, options, correct_index, points, image_key, kind, solution_text, topic, level, shuffle, grade, lesson, chapter, params: tplParams } = await req.json();
  const isWriting = kind === 'writing';
  if (!stem_text) return err('stem_text is required.', 400);
  if (!isWriting) {
    if (!Array.isArray(options) || options.length < 2) return err('stem_text and at least two options are required.', 400);
    if (!Number.isInteger(correct_index) || correct_index < 0 || correct_index >= options.length) {
      return err('correct_index must point at one of the options.', 400);
    }
  }
  const tpl = !isWriting && tplParams && String(tplParams).trim() ? String(tplParams).trim() : null;
  if (tpl) { try { checkTemplate({ params: tpl, stem_text, options_json: JSON.stringify(options), solution_text }); } catch (e) { return err(e.message, 400); } }
  const { results } = await env.DB.prepare('SELECT COALESCE(MAX(order_no), 0) AS m FROM test_questions WHERE test_id = ?1')
    .bind(params.testId).all();
  const orderNo = results[0].m + 1;
  const gr = cleanGrade(grade);
  const ls = cleanLesson(lesson);
  const ch = cleanChapter(chapter) || chapterOf(gr, ls);
  const { meta } = await env.DB.prepare(
    'INSERT INTO test_questions (test_id, order_no, stem_text, image_key, options_json, correct_index, points, kind, solution_text, topic, level, shuffle, grade, lesson, chapter, params) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10, ?11, ?12, ?13, ?14, ?15, ?16)',
  ).bind(params.testId, orderNo, stem_text, image_key || null, JSON.stringify(isWriting ? [] : options), isWriting ? 0 : correct_index, points || 1, isWriting ? 'writing' : 'mcq', solution_text || null, topic || null, level || null, shuffle ? 1 : 0, gr, ls, ch, tpl).run();
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
  if (b.points !== undefined) { const p = Number(b.points); if (!(p > 0 && p <= 100)) return err('points must be above 0 and at most 100.', 400); put('points', Math.round(p * 100) / 100); }
  if (b.solution_text !== undefined) put('solution_text', b.solution_text ? String(b.solution_text) : null);
  if (b.image_key !== undefined) put('image_key', b.image_key || null);        // null/'' removes the picture
  if (b.topic !== undefined) put('topic', b.topic ? String(b.topic).trim().slice(0, 60) : null);
  if (b.grade !== undefined) put('grade', cleanGrade(b.grade));
  if (b.lesson !== undefined) put('lesson', cleanLesson(b.lesson));
  if (b.chapter !== undefined) put('chapter', cleanChapter(b.chapter));
  else if (b.lesson !== undefined || b.grade !== undefined) {
    const gVal = b.grade !== undefined ? cleanGrade(b.grade) : cur.grade;
    const lVal = b.lesson !== undefined ? cleanLesson(b.lesson) : cur.lesson;
    const autoCh = chapterOf(gVal, lVal);
    if (autoCh) put('chapter', autoCh);
  }
  if (b.level !== undefined) put('level', ['easy', 'medium', 'hard', 'pisa'].includes(b.level) ? b.level : null);
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
  if (b.params !== undefined && !isWriting) {
    const tpl = b.params && String(b.params).trim() ? String(b.params).trim() : null;
    if (tpl) {
      try {
        checkTemplate({ id: cur.id, params: tpl, stem_text: b.stem_text !== undefined ? String(b.stem_text) : cur.stem_text, options_json: b.options !== undefined ? JSON.stringify(b.options) : cur.options_json, solution_text: b.solution_text !== undefined ? b.solution_text : cur.solution_text });
      } catch (e) { return err(e.message, 400); }
    }
    put('params', tpl);
  }
  if (!sets.length) return json({ ok: true });
  await env.DB.prepare(`UPDATE test_questions SET ${sets.join(', ')} WHERE id = ?${sets.length + 1}`).bind(...vals, g.q.id).run();
  const keyChanged = ['correct_index', 'alt_correct_index', 'cancelled', 'options'].some((k) => b[k] !== undefined);
  const { results } = await env.DB.prepare(
    `SELECT COUNT(*) AS n FROM results r JOIN test_sessions s ON s.id = r.session_id WHERE s.test_id = ?1 AND r.submitted_at IS NOT NULL`,
  ).bind(g.q.test_id).all();
  if (keyChanged) await audit(env, g.t, 'question.key_changed', `question ${g.q.id} (test ${g.q.test_id})`);
  // A key correction (not a rewording of the options) also reaches the frozen copies used by past sessions.
  const keyFields = {};
  const optionsSame = b.options === undefined || JSON.stringify(b.options.map((o) => String(o))) === cur.options_json;
  if (optionsSame) {
    for (const c of ['correct_index', 'alt_correct_index', 'cancelled', 'solution_text']) {
      const i = sets.findIndex((x) => x.startsWith(c + ' ='));
      if (i >= 0) keyFields[c] = vals[i];
    }
  }
  const synced = await syncKeyToFrozen(env, g.q.id, keyFields);
  const frozenSessions = await frozenCountForTest(env, g.q.test_id);
  return json({ ok: true, key_changed: keyChanged, submissions: results[0].n, frozen_sessions: frozenSessions, synced_to_frozen: synced });
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
  const used = await env.DB.prepare('SELECT 1 AS x FROM responses WHERE question_id = ?1 LIMIT 1').bind(params.questionId).first();
  if (used) return err('សំណួរនេះមានសិស្សបានឆ្លើយរួចហើយ មិនអាចលុបបានទេ។ សូមប្រើ «បោះបង់សំណួរ» ជំនួស។', 409);
  await env.DB.prepare('DELETE FROM test_questions WHERE id = ?1').bind(params.questionId).run();
  return json({ ok: true });
}

export async function deleteTest(req, env, params) {
  const g = await needTest(req, env, params.testId, 'own'); if (g.resp) return g.resp;
  await ensureColumns(env);
  const id = params.testId;
  const sess = '(SELECT id FROM test_sessions WHERE test_id = ?1)';
  const qs = '(SELECT id FROM test_questions WHERE test_id = ?1)';
  // children first (responses/results point at sessions, students and questions)
  await env.DB.batch([
    env.DB.prepare(`DELETE FROM responses WHERE session_id IN ${sess} OR question_id IN ${qs}`).bind(id),
    env.DB.prepare(`DELETE FROM results WHERE session_id IN ${sess}`).bind(id),
    env.DB.prepare(`DELETE FROM writing_marks WHERE session_id IN ${sess} OR question_id IN ${qs}`).bind(id),
    env.DB.prepare(`DELETE FROM session_questions WHERE session_id IN ${sess}`).bind(id),
    env.DB.prepare(`DELETE FROM exam_events WHERE session_id IN ${sess}`).bind(id),
    env.DB.prepare(`DELETE FROM session_notes WHERE session_id IN ${sess}`).bind(id),
    env.DB.prepare(`DELETE FROM question_notes WHERE question_id IN ${qs}`).bind(id),
    env.DB.prepare("DELETE FROM shares WHERE resource_type = 'test' AND resource_id = ?1").bind(id),
    env.DB.prepare('DELETE FROM test_questions WHERE test_id = ?1').bind(id),
    env.DB.prepare('DELETE FROM test_sessions WHERE test_id = ?1').bind(id),
  ]);
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
    'SELECT order_no, stem_text, image_key, options_json, correct_index, alt_correct_index, points, kind, solution_text, topic, level, shuffle, grade, lesson, params FROM test_questions WHERE test_id = ?1 ORDER BY order_no'
  ).bind(params.testId).all();

  for (const q of questions) {
    await env.DB.prepare(
      'INSERT INTO test_questions (test_id, order_no, stem_text, image_key, options_json, correct_index, alt_correct_index, points, kind, solution_text, topic, level, shuffle, grade, lesson, params) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10, ?11, ?12, ?13, ?14, ?15, ?16)'
    ).bind(newTestId, q.order_no, q.stem_text, q.image_key, q.options_json, q.correct_index, q.alt_correct_index, q.points, q.kind, q.solution_text, q.topic, q.level, q.shuffle, q.grade, q.lesson, q.params ?? null).run();
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

// ---------- question bank: every question from tests this teacher owns or can edit ----------
// includeShared: every teacher can also use the owner's question bank (the owner's hidden "🗂 ឃ្លាំងសំណួរ" test) —
// read-only: they can search and copy questions into their own tests, never change them.
async function bankRows(env, t, { dedupe = true, includeShared = false } = {}) {
  const mine = await accessibleTests(env, t);
  const ids = [...mine.entries()].filter(([, r]) => r === 'owner' || r === 'editor').map(([id]) => id);
  if (includeShared && t.role !== 'owner') {
    const { results: lib } = await env.DB.prepare("SELECT x.id FROM tests x JOIN teachers o ON o.id = x.owner_id WHERE x.is_bank = 1 AND o.role = 'owner'").all();
    for (const r of lib) if (!ids.includes(r.id)) ids.push(r.id);
  }
  if (!ids.length) return [];
  const sharedIds = new Set(ids.filter((id) => !mine.has(id) || !['owner', 'editor'].includes(mine.get(id))));
  const { results: raw } = await env.DB.prepare(
    `SELECT q.id, q.test_id, x.title AS test_title, q.stem_text, q.image_key, q.options_json, q.correct_index, q.alt_correct_index, q.points, q.kind,
            q.topic, q.level, q.grade, q.lesson, q.chapter, q.shuffle, q.solution_text, q.cancelled, q.params
     FROM test_questions q JOIN tests x ON x.id = q.test_id WHERE q.test_id IN (${ids.map(() => '?').join(',')}) ORDER BY q.test_id DESC, q.order_no`,
  ).bind(...ids).all();
  const results = raw.map((q) => (sharedIds.has(q.test_id) ? { ...q, shared: 1, test_title: 'ឃ្លាំងសំណួររួម' } : q));
  if (!dedupe) return results.filter((q) => !q.cancelled);
  // the same question often lives in several tests (copies) — show it once, preferring the tagged copy
  const byKey = new Map();
  for (const q of results) {
    if (q.cancelled) continue;
    const k = `${q.kind}|${q.stem_text}|${q.options_json}`;
    const cur = byKey.get(k);
    const sc = (x) => (x.topic ? 1 : 0) + (x.level ? 1 : 0) + (x.grade ? 2 : 0) + (x.lesson ? 2 : 0) + (x.chapter ? 2 : 0);
    if (!cur || sc(q) > sc(cur)) byKey.set(k, q);
  }
  return [...byKey.values()];
}

// The questions of one grade (whole book) or of chosen lessons, in lesson order, for the PDF / Word «exercise book».
// GET /api/bank/export?grade=7&lessons=1,2,5&levels=easy,medium&kind=all|mcq|writing&title=…
export async function exportBank(req, env) {
  const g0 = await needLicense(req, env, true); if (g0.resp) return g0.resp;
  await ensureColumns(env);
  const u = new URL(req.url);
  const grade = u.searchParams.get('grade') || '';
  if (!/^(7|8|9|10|11|12)$/.test(grade)) return err('សូមជ្រើសថ្នាក់។', 400);
  const curr = (await loadCurriculum(env, g0.t.id)).lessons[grade] || [];
  const wantIdx = new Set((u.searchParams.get('lessons') || '').split(',').map((x) => Number(x)).filter((x) => x >= 1));
  const levels = new Set((u.searchParams.get('levels') || '').split(',').filter(Boolean));
  const kind = u.searchParams.get('kind') || 'all';
  const rows = (await bankRows(env, g0.t, { includeShared: true })).filter((q) => q.grade === grade)
    .filter((q) => (kind === 'mcq' ? q.kind !== 'writing' : kind === 'writing' ? q.kind === 'writing' : true))
    .filter((q) => !levels.size || levels.has(q.level || ''));
  const idxOf = (name) => { const i = curr.indexOf(name); return i >= 0 ? i + 1 : 0; };
  const groups = new Map();
  for (const q of rows) {
    const idx = idxOf(q.lesson);
    if (wantIdx.size && !wantIdx.has(idx)) continue;
    const key = idx || `x:${q.lesson || ''}`;
    if (!groups.has(key)) groups.set(key, { idx, name: q.lesson || 'មិនទាន់កំណត់មេរៀន', questions: [] });
    groups.get(key).questions.push(q);
  }
  let list = [...groups.values()].sort((a, b) => (a.idx || 999) - (b.idx || 999));
  let total = list.reduce((t, g) => t + g.questions.length, 0);
  const trialCap = g0.t.status === 'trial' ? 20 : null;       // a free trial shows a sample of the book
  let left = trialCap;
  list = list.map((g) => {
    const qs = g.questions.sort((a, b) => a.id - b.id).filter(() => (left === null ? true : left-- > 0));
    return { ...g, questions: qs.map((q) => ({
      id: q.id, stem_text: q.stem_text, image_key: q.image_key, options: JSON.parse(q.options_json), correct_index: q.correct_index, alt_correct_index: q.alt_correct_index,
      points: q.points, kind: q.kind, solution_text: q.solution_text, level: q.level, lesson: q.lesson, chapter: q.chapter, grade: q.grade, cancelled: q.cancelled,
      sample: hasVariants(q) ? sampleFor(q, `bank:${q.id}`) : undefined,
    })) };
  }).filter((g) => g.questions.length);
  const given = list.reduce((t, g) => t + g.questions.length, 0);
  return json({ grade, groups: list, total, given, trial_limited: !!trialCap && total > given, whole_book: !wantIdx.size });
}

export async function listBank(req, env) {
  const g0 = await needLicense(req, env, true); if (g0.resp) return g0.resp;
  await ensureColumns(env);
  const rows = await bankRows(env, g0.t, { includeShared: true });
  return json({ questions: rows.map((q) => ({ ...q, options: JSON.parse(q.options_json), options_json: undefined })) });
}

async function copyInto(env, testId, q) {
  const { results } = await env.DB.prepare('SELECT COALESCE(MAX(order_no), 0) AS m FROM test_questions WHERE test_id = ?1').bind(testId).all();
  await env.DB.prepare(
    `INSERT INTO test_questions (test_id, order_no, stem_text, image_key, options_json, correct_index, alt_correct_index, points, kind, solution_text, topic, level, shuffle, grade, lesson, chapter, params)
     VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10, ?11, ?12, ?13, ?14, ?15, ?16, ?17)`,
  ).bind(testId, results[0].m + 1, q.stem_text, q.image_key, q.options_json, q.correct_index, q.alt_correct_index, q.points, q.kind, q.solution_text, q.topic, q.level, q.shuffle, q.grade || null, q.lesson || null, q.chapter || null, q.params ?? null).run();
}

// copy chosen questions into a test
export async function copyQuestions(req, env, params) {
  const g = await needTest(req, env, params.testId, 'edit'); if (g.resp) return g.resp;
  const { question_ids } = await req.json();
  if (!Array.isArray(question_ids) || !question_ids.length) return err('question_ids is required.', 400);
  const bank = await bankRows(env, g.t, { dedupe: false, includeShared: true });
  const byId = new Map(bank.map((q) => [q.id, q]));
  let n = 0;
  const room = await questionRoom(env, g.t, params.testId);
  if (room <= 0) return limitResponse('សំណួរក្នុងមួយតេស្ត', TRIAL.questions);
  for (const id of question_ids.slice(0, Math.min(200, room))) { const q = byId.get(Number(id)); if (q) { await copyInto(env, Number(params.testId), q); n++; } }
  return json({ ok: true, copied: n });
}

// build a new draft test by picking random questions per difficulty
export async function generateTest(req, env) {
  const g0 = await needLicense(req, env, true); if (g0.resp) return g0.resp;
  await ensureColumns(env);
  if (g0.t.status === 'trial' && (await trialUsage(env, g0.t)).tests >= TRIAL.tests) return limitResponse('តេស្ត', TRIAL.tests);
  const { title, counts, topics, kind, grade, lessons } = await req.json();
  if (!title || !String(title).trim()) return err('title is required.', 400);
  const bank = (await bankRows(env, g0.t, { includeShared: true })).filter((q) => (kind === 'writing' ? q.kind === 'writing' : kind === 'all' ? true : q.kind !== 'writing'))
    .filter((q) => !topics || !topics.length || topics.includes(q.topic))
    .filter((q) => !grade || q.grade === String(grade))
    .filter((q) => !Array.isArray(lessons) || !lessons.length || lessons.includes(q.lesson));
  const shuffle = (a) => { const b = a.slice(); for (let i = b.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [b[i], b[j]] = [b[j], b[i]]; } return b; };
  const picked = []; const shortage = {};
  for (const lvl of ['easy', 'medium', 'hard', 'pisa']) {
    const want = Math.min(Math.max(Number(counts && counts[lvl]) || 0, 0), 100);
    const pool = shuffle(bank.filter((q) => q.level === lvl));
    picked.push(...pool.slice(0, want));
    if (pool.length < want) shortage[lvl] = want - pool.length;
  }
  if (g0.t.status === 'trial') picked.splice(TRIAL.questions);
  if (!picked.length) return err('មិនមានសំណួរគ្រប់គ្រាន់ក្នុងធនាគារតាមលក្ខខណ្ឌនេះទេ។', 400);
  const { meta } = await env.DB.prepare('INSERT INTO tests (title, owner_id) VALUES (?1, ?2)').bind(String(title).trim(), g0.t.id).run();
  for (const q of picked) await copyInto(env, meta.last_row_id, q);
  await audit(env, g0.t, 'bank.generate', `test ${meta.last_row_id}: ${picked.length} questions`);
  return json({ ok: true, id: meta.last_row_id, picked: picked.length, shortage });
}

// import many questions at once (from the Excel template)
export async function bulkAdd(req, env, params) {
  const g = await needTest(req, env, params.testId, 'edit'); if (g.resp) return g.resp;
  await ensureColumns(env);
  const { questions } = await req.json();
  if (!Array.isArray(questions) || !questions.length) return err('questions[] is required.', 400);
  if (questions.length > 200) return err('នាំចូលបានអតិបរមា ២០០ សំណួរម្តង។', 400);
  const room = await questionRoom(env, g.t, params.testId);
  if (room <= 0) return limitResponse('សំណួរក្នុងមួយតេស្ត', TRIAL.questions);
  if (questions.length > room) questions.length = room;
  const { results } = await env.DB.prepare('SELECT COALESCE(MAX(order_no), 0) AS m FROM test_questions WHERE test_id = ?1').bind(params.testId).all();
  let order = results[0].m;
  const stmts = []; const bad = [];
  questions.forEach((q, i) => {
    const writing = q.kind === 'writing';
    const stem = String(q.stem_text || '').trim();
    const opts = Array.isArray(q.options) ? q.options.map((o) => String(o).trim()).filter(Boolean) : [];
    if (!stem || (!writing && (opts.length < 2 || !Number.isInteger(q.correct_index) || q.correct_index < 0 || q.correct_index >= opts.length))) { bad.push(i + 1); return; }
    order += 1;
    const gr = cleanGrade(q.grade);
    const ls = cleanLesson(q.lesson);
    const ch = cleanChapter(q.chapter) || chapterOf(gr, ls);
    stmts.push(env.DB.prepare(
      `INSERT INTO test_questions (test_id, order_no, stem_text, options_json, correct_index, points, kind, solution_text, topic, level, shuffle, grade, lesson, chapter)
       VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10, ?11, ?12, ?13, ?14)`,
    ).bind(params.testId, order, stem, JSON.stringify(writing ? [] : opts), writing ? 0 : q.correct_index, Math.max(0.25, Math.round((Number(q.points) || (writing ? 5 : 1)) * 100) / 100),
      writing ? 'writing' : 'mcq', q.solution_text ? String(q.solution_text) : null, q.topic ? String(q.topic).slice(0, 60) : null,
      ['easy', 'medium', 'hard', 'pisa'].includes(q.level) ? q.level : null, writing ? 0 : (q.shuffle ? 1 : 0), gr, ls, ch));
  });
  if (stmts.length) await env.DB.batch(stmts);
  await audit(env, g.t, 'questions.import', `test ${params.testId}: ${stmts.length} added, ${bad.length} skipped`);
  return json({ ok: true, added: stmts.length, skipped: bad });
}

const cleanGrade = (g) => (GRADES.includes(String(g || '').trim()) ? String(g).trim() : null);
const cleanLesson = (l) => (l ? String(l).trim().slice(0, 120) || null : null);
const cleanChapter = (c) => (c ? String(c).trim().slice(0, 120) || null : null);

// lesson list per grade (defaults + this teacher's own additions)
export async function getCurriculum(req, env) {
  const g0 = await needLicense(req, env, true); if (g0.resp) return g0.resp;
  const { lessons, chapters } = await loadCurriculum(env, g0.t.id);
  return json({ grades: GRADES, lessons, chapters });
}

export async function addLesson(req, env) {
  const g0 = await needLicense(req, env); if (g0.resp) return g0.resp;
  const { grade, name } = await req.json();
  const gr = cleanGrade(grade); const nm = cleanLesson(name);
  if (!gr || !nm) return err('grade and name are required.', 400);
  const { extra, lessons } = await loadCurriculum(env, g0.t.id);
  if (!lessons[gr].includes(nm)) (extra[gr] ||= []).push(nm);
  await env.DB.prepare('INSERT INTO settings (key, value) VALUES (?1, ?2) ON CONFLICT(key) DO UPDATE SET value = ?2').bind(`curriculum_${g0.t.id}`, JSON.stringify(extra)).run();
  return json({ ok: true });
}

// put many bank questions into a grade / lesson (also tags identical copies in the teacher's other tests)
export async function tagQuestions(req, env) {
  const g0 = await needLicense(req, env); if (g0.resp) return g0.resp;
  await ensureColumns(env);
  const b = await req.json();
  if (!Array.isArray(b.question_ids) || !b.question_ids.length) return err('question_ids is required.', 400);
  const bank = await bankRows(env, g0.t, { dedupe: false });
  const byId = new Map(bank.map((q) => [q.id, q]));
  const keyOf = (q) => `${q.kind}|${q.stem_text}|${q.options_json}`;
  const wanted = new Set(b.question_ids.slice(0, 500).map(Number).filter((id) => byId.has(id)).map((id) => keyOf(byId.get(id))));
  const gr = b.grade === undefined ? undefined : cleanGrade(b.grade);
  const ls = b.lesson === undefined ? undefined : cleanLesson(b.lesson);
  const ch = b.chapter === undefined ? (ls && gr ? chapterOf(gr, ls) : undefined) : cleanChapter(b.chapter);
  const stmts = [];
  for (const q of bank) {
    if (!wanted.has(keyOf(q))) continue;
    const sets = []; const vals = [];
    if (gr !== undefined) { sets.push(`grade = ?${sets.length + 1}`); vals.push(gr); }
    if (ls !== undefined) { sets.push(`lesson = ?${sets.length + 1}`); vals.push(ls); }
    if (ch !== undefined) { sets.push(`chapter = ?${sets.length + 1}`); vals.push(ch); }
    if (b.level !== undefined) { sets.push(`level = ?${sets.length + 1}`); vals.push(['easy', 'medium', 'hard', 'pisa'].includes(b.level) ? b.level : null); }
    if (!sets.length) continue;
    stmts.push(env.DB.prepare(`UPDATE test_questions SET ${sets.join(', ')} WHERE id = ?${sets.length + 1}`).bind(...vals, q.id));
  }
  for (let i = 0; i < stmts.length; i += 50) await env.DB.batch(stmts.slice(i, i + 50));
  await audit(env, g0.t, 'bank.tag', `${wanted.size} questions → grade ${b.grade ?? '-'} / ${b.lesson ?? '-'}`);
  return json({ ok: true, tagged: wanted.size });
}

// Each teacher has one hidden "bank" test that holds questions written straight into the question bank.
export async function bankHome(req, env) {
  const g0 = await needLicense(req, env); if (g0.resp) return g0.resp;
  await ensureColumns(env);
  let row = await env.DB.prepare('SELECT id FROM tests WHERE owner_id = ?1 AND is_bank = 1').bind(g0.t.id).first();
  if (!row) {
    const { meta } = await env.DB.prepare("INSERT INTO tests (title, owner_id, is_bank, status) VALUES ('🗂 ឃ្លាំងសំណួរ', ?1, 1, 'draft')").bind(g0.t.id).run();
    row = { id: meta.last_row_id };
  }
  return json({ id: row.id });
}
