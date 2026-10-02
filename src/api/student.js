import { json, err } from '../lib/http.js';
import { verifySecretValue } from '../lib/crypto.js';
import { createSessionCookie, clearSessionCookie, requireStudent } from '../lib/session.js';
import { sessionWindow } from '../lib/time.js';

const SUBMIT_GRACE_MS = 5000; // forgive a submit that was already in flight when the clock hit zero

export async function login(req, env) {
  const { id, pin } = await req.json();
  if (!id || !pin) return err('id and pin are required.', 400);
  const student = await env.DB.prepare('SELECT id, surname, first_name, class_id, pin_hash FROM students WHERE id = ?1').bind(String(id)).first();
  if (!student) return err('Incorrect ID or PIN.', 401);
  const ok = await verifySecretValue(pin, student.id, env.SESSION_SECRET, student.pin_hash);
  if (!ok) return err('Incorrect ID or PIN.', 401);
  const fullName = `${student.surname} ${student.first_name}`;
  const cookie = await createSessionCookie(
    { role: 'student', id: student.id, name: fullName, classId: student.class_id }, env.SESSION_SECRET,
  );
  return json({ ok: true, name: fullName }, 200, { 'Set-Cookie': cookie });
}

export async function logout() {
  return json({ ok: true }, 200, { 'Set-Cookie': clearSessionCookie('student') });
}

// Picks the one session a student currently cares about: an open one first,
// otherwise the soonest upcoming one, otherwise the most recently closed one.
async function findRelevantSession(env, classId) {
  const { results } = await env.DB.prepare(
    `SELECT ts.*, t.title AS test_title FROM test_sessions ts JOIN tests t ON t.id = ts.test_id
     WHERE ts.class_id = ?1 ORDER BY ts.scheduled_start DESC`,
  ).bind(classId).all();
  if (results.length === 0) return null;
  const withWindow = results.map((s) => ({ ...s, window: sessionWindow(s) }));
  return (
    withWindow.find((s) => s.window.phase === 'open') ||
    withWindow.filter((s) => s.window.phase === 'upcoming').sort((a, b) => a.window.start - b.window.start)[0] ||
    withWindow[0]
  );
}

export async function status(req, env) {
  const session = await requireStudent(req, env);
  if (!session) return err('Not logged in.', 401);
  const relevant = await findRelevantSession(env, session.classId);
  if (!relevant) return json({ phase: 'none' });

  const result = await env.DB.prepare('SELECT mcq_score, mcq_max, writing_score, writing_max, submitted_at, published_at FROM results WHERE session_id = ?1 AND student_id = ?2')
    .bind(relevant.id, session.id).first();

  if (result) {
    if (result.published_at) {
      return json({
        phase: 'published', test_title: relevant.test_title,
        mcq_score: result.mcq_score, mcq_max: result.mcq_max,
        writing_score: result.writing_score, writing_max: result.writing_max,
      });
    }
    return json({ phase: 'submitted', test_title: relevant.test_title });
  }

  if (relevant.window.phase === 'open') {
    return json({ phase: 'open', session_id: relevant.id, test_title: relevant.test_title, end_at: relevant.window.end });
  }
  if (relevant.window.phase === 'upcoming') {
    return json({ phase: 'upcoming', test_title: relevant.test_title, scheduled_start: relevant.scheduled_start, duration_minutes: relevant.duration_minutes });
  }
  return json({ phase: 'missed', test_title: relevant.test_title });
}

async function loadOpenSessionForStudent(env, studentSession) {
  const relevant = await findRelevantSession(env, studentSession.classId);
  if (!relevant || relevant.window.phase !== 'open') return null;
  const already = await env.DB.prepare('SELECT id FROM results WHERE session_id = ?1 AND student_id = ?2 AND submitted_at IS NOT NULL')
    .bind(relevant.id, studentSession.id).first();
  if (already) return null;
  return relevant;
}

export async function getTest(req, env) {
  const studentSession = await requireStudent(req, env);
  if (!studentSession) return err('Not logged in.', 401);
  const relevant = await loadOpenSessionForStudent(env, studentSession);
  if (!relevant) return err('No test is open for you right now.', 403);

  const { results: questions } = await env.DB.prepare(
    'SELECT id, stem_text, image_key, options_json FROM test_questions WHERE test_id = ?1 ORDER BY order_no',
  ).bind(relevant.test_id).all();

  const { results: saved } = await env.DB.prepare('SELECT question_id, selected_index FROM responses WHERE session_id = ?1 AND student_id = ?2')
    .bind(relevant.id, studentSession.id).all();
  const savedByQuestion = Object.fromEntries(saved.map((r) => [r.question_id, r.selected_index]));

  return json({
    session_id: relevant.id,
    test_title: relevant.test_title,
    end_at: relevant.window.end,
    questions: questions.map((q) => ({
      id: q.id, stem_text: q.stem_text, image_key: q.image_key,
      options: JSON.parse(q.options_json), selected_index: savedByQuestion[q.id] ?? null,
    })),
  });
}

export async function answer(req, env) {
  const studentSession = await requireStudent(req, env);
  if (!studentSession) return err('Not logged in.', 401);
  const relevant = await loadOpenSessionForStudent(env, studentSession);
  if (!relevant) return err('This test is not open anymore.', 403);
  const { question_id, selected_index } = await req.json();
  const question = await env.DB.prepare('SELECT id FROM test_questions WHERE id = ?1 AND test_id = ?2').bind(question_id, relevant.test_id).first();
  if (!question) return err('That question is not part of this test.', 400);
  await env.DB.prepare(
    `INSERT INTO responses (session_id, student_id, question_id, selected_index) VALUES (?1, ?2, ?3, ?4)
     ON CONFLICT(session_id, student_id, question_id) DO UPDATE SET selected_index = ?4, answered_at = datetime('now')`,
  ).bind(relevant.id, studentSession.id, question_id, selected_index).run();
  return json({ ok: true });
}

export async function submit(req, env) {
  const studentSession = await requireStudent(req, env);
  if (!studentSession) return err('Not logged in.', 401);
  const relevant = await loadOpenSessionForStudent(env, studentSession);
  if (!relevant) return err('This test is not open anymore.', 403);
  if (Date.now() > relevant.window.end + SUBMIT_GRACE_MS) return err('Time is up.', 403);

  const { results: questions } = await env.DB.prepare('SELECT id, correct_index, points FROM test_questions WHERE test_id = ?1')
    .bind(relevant.test_id).all();
  const { results: responses } = await env.DB.prepare('SELECT question_id, selected_index FROM responses WHERE session_id = ?1 AND student_id = ?2')
    .bind(relevant.id, studentSession.id).all();
  const selectedByQuestion = Object.fromEntries(responses.map((r) => [r.question_id, r.selected_index]));

  let mcqScore = 0;
  let mcqMax = 0;
  for (const q of questions) {
    mcqMax += q.points;
    if (selectedByQuestion[q.id] === q.correct_index) mcqScore += q.points;
  }

  await env.DB.prepare(
    `INSERT INTO results (session_id, student_id, mcq_score, mcq_max, submitted_at) VALUES (?1, ?2, ?3, ?4, datetime('now'))
     ON CONFLICT(session_id, student_id) DO UPDATE SET mcq_score = ?3, mcq_max = ?4, submitted_at = datetime('now')`,
  ).bind(relevant.id, studentSession.id, mcqScore, mcqMax).run();

  return json({ ok: true, mcq_score: mcqScore, mcq_max: mcqMax });
}
