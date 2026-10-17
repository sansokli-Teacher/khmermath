// Frozen question sets. Once students have started an exam session, the questions
// they saw (wording, options, picture, key, marks) are copied into session_questions
// so later edits to the test cannot silently change that session's reviews or scores.
// A deliberate answer-key correction goes through syncKeyToFrozen().

const COLS = 'order_no, kind, stem_text, image_key, options_json, correct_index, alt_correct_index, cancelled, points, solution_text, topic, level, shuffle, params';

export async function isFrozen(env, sessionId) {
  return !!(await env.DB.prepare('SELECT 1 AS x FROM session_questions WHERE session_id = ?1 LIMIT 1').bind(sessionId).first());
}

export async function ensureFrozen(env, sessionId) {
  if (await isFrozen(env, sessionId)) return;
  await env.DB.prepare(
    `INSERT OR IGNORE INTO session_questions (session_id, question_id, ${COLS})
     SELECT s.id, q.id, ${COLS.split(', ').map((c) => 'q.' + c).join(', ')}
     FROM test_sessions s JOIN test_questions q ON q.test_id = s.test_id WHERE s.id = ?1`,
  ).bind(sessionId).run();
}

async function hasAttempts(env, sessionId) {
  return !!(await env.DB.prepare(
    `SELECT 1 AS x FROM results WHERE session_id = ?1 AND (started_at IS NOT NULL OR submitted_at IS NOT NULL)
     UNION SELECT 1 FROM responses WHERE session_id = ?1 LIMIT 1`,
  ).bind(sessionId).first());
}

// The questions of a session, in printed order. Frozen copy once anyone has started;
// the live test before that (so teachers can still fix typos before the exam).
export async function sessionQuestions(env, sessionId, testId) {
  if (!(await isFrozen(env, sessionId)) && (await hasAttempts(env, sessionId))) await ensureFrozen(env, sessionId);
  if (await isFrozen(env, sessionId)) {
    const { results } = await env.DB.prepare(
      `SELECT sq.question_id AS id, ${COLS.split(', ').map((c) => 'sq.' + c).join(', ')}, tq.lesson, tq.grade
       FROM session_questions sq
       LEFT JOIN test_questions tq ON tq.id = sq.question_id
       WHERE sq.session_id = ?1 ORDER BY sq.order_no, sq.question_id`,
    ).bind(sessionId).all();
    return results;
  }
  const { results } = await env.DB.prepare(`SELECT id, ${COLS}, lesson, grade FROM test_questions WHERE test_id = ?1 ORDER BY order_no, id`).bind(testId).all();
  return results;
}

export const mcqOnly = (qs) => qs.filter((q) => q.kind !== 'writing');

// A teacher's deliberate key correction (right answer, second accepted answer, withdrawn
// question, worked solution) reaches the frozen copies of that question.
export async function syncKeyToFrozen(env, questionId, fields) {
  const cols = ['correct_index', 'alt_correct_index', 'cancelled', 'solution_text'].filter((c) => c in fields);
  if (!cols.length) return 0;
  const sets = cols.map((c, i) => `${c} = ?${i + 2}`).join(', ');
  const r = await env.DB.prepare(`UPDATE session_questions SET ${sets} WHERE question_id = ?1`).bind(questionId, ...cols.map((c) => fields[c])).run();
  return r.meta.changes ?? r.meta.rows_written ?? 0;
}

export async function frozenCountForTest(env, testId) {
  const r = await env.DB.prepare(
    'SELECT COUNT(DISTINCT sq.session_id) AS n FROM session_questions sq JOIN test_sessions s ON s.id = sq.session_id WHERE s.test_id = ?1',
  ).bind(testId).first();
  return r ? r.n : 0;
}
