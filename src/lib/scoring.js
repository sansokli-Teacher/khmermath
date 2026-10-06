// One place that decides what counts as correct, so submit, auto-finalize,
// re-scoring, reviews and statistics can never disagree.
//   q.cancelled          -> everybody gets the points (question withdrawn)
//   q.alt_correct_index  -> a second accepted answer
export function isRight(q, sel) {
  if (q.cancelled) return true;
  if (sel == null) return false;
  return sel === q.correct_index || (q.alt_correct_index != null && sel === q.alt_correct_index);
}

export function scoreMcq(questions, selectedByQuestion) {
  let score = 0, max = 0;
  for (const q of questions) {
    max += q.points;
    if (isRight(q, selectedByQuestion[q.id])) score += q.points;
  }
  return { score, max };
}

export async function loadMcq(env, testId) {
  const { results } = await env.DB.prepare(
    "SELECT id, correct_index, alt_correct_index, cancelled, points FROM test_questions WHERE test_id = ?1 AND kind <> 'writing'",
  ).bind(testId).all();
  return results;
}

async function answersOf(env, sessionId) {
  const { results } = await env.DB.prepare('SELECT student_id, question_id, selected_index FROM responses WHERE session_id = ?1').bind(sessionId).all();
  const by = {};
  for (const r of results) (by[r.student_id] ||= {})[r.question_id] = r.selected_index;
  return by;
}

// Re-score every submitted student of a session with the current answer key.
export async function rescoreSession(env, sessionId) {
  const ses = await env.DB.prepare('SELECT test_id FROM test_sessions WHERE id = ?1').bind(sessionId).first();
  if (!ses) return { changed: 0, total: 0 };
  const qs = await loadMcq(env, ses.test_id);
  const by = await answersOf(env, sessionId);
  const { results: rows } = await env.DB.prepare(
    'SELECT id, student_id, mcq_score, mcq_max FROM results WHERE session_id = ?1 AND submitted_at IS NOT NULL',
  ).bind(sessionId).all();
  const stmts = [];
  for (const r of rows) {
    const { score, max } = scoreMcq(qs, by[r.student_id] || {});
    if (score !== r.mcq_score || max !== r.mcq_max) {
      stmts.push(env.DB.prepare('UPDATE results SET mcq_score = ?1, mcq_max = ?2 WHERE id = ?3').bind(score, max, r.id));
    }
  }
  if (stmts.length) await env.DB.batch(stmts);
  return { changed: stmts.length, total: rows.length };
}

// Score and submit one student from the answers saved on the server.
export async function submitStudent(env, session, studentId, submitType) {
  const qs = await loadMcq(env, session.test_id);
  const { results: rs } = await env.DB.prepare('SELECT question_id, selected_index FROM responses WHERE session_id = ?1 AND student_id = ?2')
    .bind(session.id, studentId).all();
  const { score, max } = scoreMcq(qs, Object.fromEntries(rs.map((r) => [r.question_id, r.selected_index])));
  await env.DB.prepare(
    `INSERT INTO results (session_id, student_id, mcq_score, mcq_max, submitted_at, submit_type)
     VALUES (?1, ?2, ?3, ?4, datetime('now'), ?5)
     ON CONFLICT(session_id, student_id) DO UPDATE SET mcq_score = ?3, mcq_max = ?4, submitted_at = datetime('now'), submit_type = ?5`,
  ).bind(session.id, studentId, score, max, submitType).run();
  return { score, max };
}
