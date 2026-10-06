import { json, err } from '../lib/http.js';
import { createSessionCookie, clearSessionCookie, requireStudent } from '../lib/session.js';
import { needSession } from '../lib/access.js';
import { sessionWindow } from '../lib/time.js';
import { ensureColumns } from './sessions.js';
import { studentYear } from './year.js';

const SUBMIT_GRACE_MS = 5000; // forgive a submit that was already in flight when the clock hit zero

// Students sign in with their ID alone. The PIN lives on each test session and
// is asked for when the student starts that test.
export async function login(req, env) {
  const { id } = await req.json();
  if (!id) return err('សូមបញ្ចូលអត្តលេខសិស្ស។', 400);
  const student = await env.DB.prepare(
    'SELECT s.id, s.surname, s.first_name, s.class_id FROM students s WHERE s.id = ?1',
  ).bind(String(id).trim()).first();
  if (!student) return err('រកមិនឃើញអត្តលេខនេះទេ។ សូមពិនិត្យម្តងទៀត។', 401);
  const fullName = `${student.surname} ${student.first_name}`;
  const cookie = await createSessionCookie(
    { role: 'student', id: student.id, name: fullName, classId: student.class_id }, env.SESSION_SECRET,
  );
  return json({ ok: true, name: fullName }, 200, { 'Set-Cookie': cookie });
}

export async function logout() {
  return json({ ok: true }, 200, { 'Set-Cookie': clearSessionCookie('student') });
}

function endOf(s) {
  return s.scheduled_end ? Date.parse(s.scheduled_end) : Date.parse(s.scheduled_start) + s.duration_minutes * 60000;
}

// Everything the student's home page needs: what is coming up, and past scores.
export async function status(req, env) {
  const session = await requireStudent(req, env);
  if (!session) return err('Not logged in.', 401);
  await ensureColumns(env);
  const cls = await env.DB.prepare('SELECT name FROM classes WHERE id = ?1').bind(session.classId).first();
  const { results: rows } = await env.DB.prepare(
    `SELECT ts.id, ts.scheduled_start, ts.scheduled_end, ts.duration_minutes, ts.status,
            t.title AS test_title,
            r.mcq_score, r.mcq_max, r.writing_score, r.writing_max, r.started_at, r.submitted_at, r.published_at
     FROM test_sessions ts
     JOIN tests t ON t.id = ts.test_id
     LEFT JOIN results r ON r.session_id = ts.id AND r.student_id = ?2
     WHERE ts.class_id = ?1
     ORDER BY ts.scheduled_start DESC`,
  ).bind(session.classId, session.id).all();

  const upcoming = [];
  const history = [];
  for (const r of rows) {
    const phase = sessionWindow(r).phase;
    const base = {
      session_id: r.id, test_title: r.test_title,
      scheduled_start: r.scheduled_start, scheduled_end: new Date(endOf(r)).toISOString(),
      duration_minutes: r.duration_minutes,
    };
    if (r.submitted_at && r.published_at) {
      history.push({ ...base, state: 'published', mcq_score: r.mcq_score, mcq_max: r.mcq_max, writing_score: r.writing_score, writing_max: r.writing_max });
    } else if (r.submitted_at || (phase === 'closed' && r.started_at)) {
      history.push({ ...base, state: 'pending' });
    } else if (phase === 'closed') {
      history.push({ ...base, state: 'missed' });
    } else {
      upcoming.push({ ...base, phase, started: !!r.started_at });
    }
  }
  upcoming.sort((a, b) => Date.parse(a.scheduled_start) - Date.parse(b.scheduled_start));
  return json({
    student_id: session.id, student_name: session.name, class_name: cls ? cls.name : '',
    server_now: Date.now(), upcoming, history,
    year: await studentYear(env, session).catch(() => null),
  });
}

// The session a student is allowed to be answering right now: it must belong to
// their class, be open, have been unlocked with its PIN, and not be submitted.
async function loadActiveSession(env, studentSession, sessionId, graceMs = 0) {
  if (!sessionId) return null;
  const ses = await env.DB.prepare(
    `SELECT ts.*, t.title AS test_title FROM test_sessions ts JOIN tests t ON t.id = ts.test_id
     WHERE ts.id = ?1 AND ts.class_id = ?2`,
  ).bind(sessionId, studentSession.classId).first();
  if (!ses) return null;
  const window = sessionWindow(ses);
  const inGrace = graceMs > 0 && ses.status !== 'closed' && Date.now() < window.end + graceMs;
  if (window.phase !== 'open' && !inGrace) return null;
  const result = await env.DB.prepare(
    'SELECT started_at, submitted_at FROM results WHERE session_id = ?1 AND student_id = ?2',
  ).bind(ses.id, studentSession.id).first();
  if (!result || !result.started_at || result.submitted_at) return null;
  return { ...ses, window };
}

// Student types the test's PIN. Wrong PIN -> error. Before the start time ->
// "waiting". Once open (and PIN right) the test is unlocked for this student.
export async function start(req, env) {
  const studentSession = await requireStudent(req, env);
  if (!studentSession) return err('Not logged in.', 401);
  await ensureColumns(env);
  const { session_id, pin } = await req.json();
  const ses = await env.DB.prepare(
    'SELECT * FROM test_sessions WHERE id = ?1 AND class_id = ?2',
  ).bind(session_id, studentSession.classId).first();
  if (!ses) return err('រកមិនឃើញការប្រឡងនេះទេ។', 404);

  const result = await env.DB.prepare(
    'SELECT id, started_at, submitted_at FROM results WHERE session_id = ?1 AND student_id = ?2',
  ).bind(ses.id, studentSession.id).first();
  if (result && result.submitted_at) return err('អ្នកបានប្រគល់ការប្រឡងនេះរួចហើយ។', 403);

  const window = sessionWindow(ses);
  // A student who already entered the PIN (e.g. refreshed the page or the phone
  // restarted) may resume without typing it again.
  const alreadyUnlocked = result && result.started_at;
  if (!alreadyUnlocked) {
    const expected = ses.pin == null ? '' : String(ses.pin).trim().toLowerCase();
    if (expected && String(pin ?? '').trim().toLowerCase() !== expected) return err('PIN មិនត្រឹមត្រូវទេ។ សូមសួរលោកគ្រូ។', 401);
  }
  if (window.phase === 'closed') return err('ការប្រឡងនេះបានបិទហើយ។', 403);
  if (!alreadyUnlocked) {
    // The class owner's licence must be active to start a *new* attempt.
    const owner = await env.DB.prepare(
      `SELECT t.role, t.plan, t.license_until FROM classes c JOIN teachers t ON t.id = c.owner_id WHERE c.id = ?1`,
    ).bind(ses.class_id).first();
    const stamp = new Date().toISOString().replace('T', ' ').slice(0, 19);
    if (owner && owner.role !== 'owner' && !(owner.plan === 'full' && (!owner.license_until || owner.license_until > stamp))) {
      return err('ការប្រឡងនេះត្រូវបានផ្អាកជាបណ្តោះអាសន្ន។ សូមប្រាប់លោកគ្រូអ្នកគ្រូ។', 403);
    }
  }
  if (window.phase === 'upcoming') {
    return json({ ok: true, waiting: true, start_at: window.start, server_now: Date.now() });
  }

  if (!result) {
    await env.DB.prepare(
      "INSERT INTO results (session_id, student_id, mcq_score, mcq_max, started_at) VALUES (?1, ?2, 0, 0, datetime('now'))",
    ).bind(ses.id, studentSession.id).run();
  } else if (!result.started_at) {
    await env.DB.prepare("UPDATE results SET started_at = datetime('now') WHERE id = ?1").bind(result.id).run();
  }
  return json({ ok: true, waiting: false, server_now: Date.now() });
}

function seededShuffle(items, seedText) {
  let h = 2166136261;
  for (const ch of seedText) { h ^= ch.charCodeAt(0); h = Math.imul(h, 16777619) >>> 0; }
  const rand = () => { h = (Math.imul(h ^ (h >>> 15), 2246822507) + 0x6D2B79F5) >>> 0; return h / 4294967296; };
  const a = items.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(rand() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

export async function getTest(req, env) {
  const studentSession = await requireStudent(req, env);
  if (!studentSession) return err('Not logged in.', 401);
  await ensureColumns(env);
  const sessionId = Number(new URL(req.url).searchParams.get('session_id'));
  const active = await loadActiveSession(env, studentSession, sessionId);
  if (!active) return err('No test is open for you right now.', 403);

  const { results: orderedQuestions } = await env.DB.prepare(
    "SELECT id, stem_text, image_key, options_json, kind, points FROM test_questions WHERE test_id = ?1 ORDER BY CASE WHEN kind = 'writing' THEN 1 ELSE 0 END, order_no",
  ).bind(active.test_id).all();
  // Each student sees the questions in their own fixed order (same every time
  // they reload), so neighbours cannot copy by question number.
  // Multiple-choice questions are shuffled per student; the writing section keeps
  // its printed order after them.
  const questions = [
    ...seededShuffle(orderedQuestions.filter((q) => q.kind !== 'writing'), `${active.id}:${studentSession.id}`),
    ...orderedQuestions.filter((q) => q.kind === 'writing'),
  ];

  const { results: saved } = await env.DB.prepare('SELECT question_id, selected_index FROM responses WHERE session_id = ?1 AND student_id = ?2')
    .bind(active.id, studentSession.id).all();
  const savedByQuestion = Object.fromEntries(saved.map((r) => [r.question_id, r.selected_index]));

  return json({
    session_id: active.id,
    test_title: active.test_title,
    end_at: active.window.end,
    server_now: Date.now(),
    questions: questions.map((q) => ({
      id: q.id, stem_text: q.stem_text, image_key: q.image_key, kind: q.kind, points: q.points,
      options: JSON.parse(q.options_json), selected_index: savedByQuestion[q.id] ?? null,
    })),
  });
}

// The student's page reports each time it was left (tab switch, app switch).
export async function leftPage(req, env) {
  const studentSession = await requireStudent(req, env);
  if (!studentSession) return err('Not logged in.', 401);
  const { session_id } = await req.json().catch(() => ({}));
  const active = await loadActiveSession(env, studentSession, Number(session_id));
  if (!active) return json({ ok: true });
  await ensureColumns(env);
  await env.DB.prepare('UPDATE results SET tab_switches = tab_switches + 1 WHERE session_id = ?1 AND student_id = ?2')
    .bind(active.id, studentSession.id).run();
  return json({ ok: true });
}

export async function answer(req, env) {
  const studentSession = await requireStudent(req, env);
  if (!studentSession) return err('Not logged in.', 401);
  await ensureColumns(env);
  const { session_id, question_id, selected_index } = await req.json();
  const active = await loadActiveSession(env, studentSession, Number(session_id));
  if (!active) return err('This test is not open anymore.', 403);
  const question = await env.DB.prepare("SELECT id FROM test_questions WHERE id = ?1 AND test_id = ?2 AND kind <> 'writing'").bind(question_id, active.test_id).first();
  if (!question) return err('That question is not part of this test.', 400);
  await env.DB.prepare(
    `INSERT INTO responses (session_id, student_id, question_id, selected_index) VALUES (?1, ?2, ?3, ?4)
     ON CONFLICT(session_id, student_id, question_id) DO UPDATE SET selected_index = ?4, answered_at = datetime('now')`,
  ).bind(active.id, studentSession.id, question_id, selected_index).run();
  return json({ ok: true });
}

export async function submit(req, env) {
  const studentSession = await requireStudent(req, env);
  if (!studentSession) return err('Not logged in.', 401);
  await ensureColumns(env);
  let body = {};
  try { body = await req.json(); } catch {}
  const active = await loadActiveSession(env, studentSession, Number(body.session_id), SUBMIT_GRACE_MS);
  if (!active) return err('This test is not open anymore.', 403);
  const submitType = body.submit_type === 'auto' ? 'auto' : 'manual';

  const { results: questions } = await env.DB.prepare("SELECT id, correct_index, points FROM test_questions WHERE test_id = ?1 AND kind <> 'writing'")
    .bind(active.test_id).all();
  const { results: responses } = await env.DB.prepare('SELECT question_id, selected_index FROM responses WHERE session_id = ?1 AND student_id = ?2')
    .bind(active.id, studentSession.id).all();
  const selectedByQuestion = Object.fromEntries(responses.map((r) => [r.question_id, r.selected_index]));

  let mcqScore = 0;
  let mcqMax = 0;
  for (const q of questions) {
    mcqMax += q.points;
    if (selectedByQuestion[q.id] === q.correct_index) mcqScore += q.points;
  }

  await env.DB.prepare(
    `INSERT INTO results (session_id, student_id, mcq_score, mcq_max, submitted_at, submit_type)
     VALUES (?1, ?2, ?3, ?4, datetime('now'), ?5)
     ON CONFLICT(session_id, student_id) DO UPDATE SET mcq_score = ?3, mcq_max = ?4, submitted_at = datetime('now'), submit_type = ?5`,
  ).bind(active.id, studentSession.id, mcqScore, mcqMax, submitType).run();

  return json({ ok: true, submit_type: submitType });
}

// Per-question review of one student's attempt: what they chose, what was right.
async function buildReview(env, sessionId, studentId, { onlyIfPublished }) {
  await ensureColumns(env);
  const ses = await env.DB.prepare(
    `SELECT ts.id, ts.test_id, ts.class_id, ts.scheduled_start, t.title AS test_title, c.name AS class_name
     FROM test_sessions ts JOIN tests t ON t.id = ts.test_id JOIN classes c ON c.id = ts.class_id WHERE ts.id = ?1`,
  ).bind(sessionId).first();
  if (!ses) return { error: err('រកមិនឃើញការប្រឡងនេះទេ។', 404) };
  const stu = await env.DB.prepare('SELECT id, surname, first_name, gender, class_id FROM students WHERE id = ?1').bind(studentId).first();
  if (!stu || stu.class_id !== ses.class_id) return { error: err('រកមិនឃើញសិស្សក្នុងថ្នាក់នេះទេ។', 404) };
  const result = await env.DB.prepare(
    'SELECT mcq_score, mcq_max, writing_score, writing_max, submitted_at, published_at FROM results WHERE session_id = ?1 AND student_id = ?2',
  ).bind(sessionId, studentId).first();
  if (!result || !result.submitted_at) return { error: err('សិស្សនេះមិនបានប្រគល់ការប្រឡងនេះទេ។', 404) };
  if (onlyIfPublished && !result.published_at) return { error: err('លទ្ធផលមិនទាន់ត្រូវបានប្រកាសនៅឡើយទេ។', 403) };

  const { results: qs } = await env.DB.prepare(
    'SELECT id, order_no, stem_text, image_key, options_json, correct_index, points, kind, solution_text FROM test_questions WHERE test_id = ?1 ORDER BY order_no',
  ).bind(ses.test_id).all();
  const { results: rs } = await env.DB.prepare('SELECT question_id, selected_index FROM responses WHERE session_id = ?1 AND student_id = ?2')
    .bind(sessionId, studentId).all();
  const chosen = Object.fromEntries(rs.map((r) => [r.question_id, r.selected_index]));

  const questions = qs.map((q) => {
    if (q.kind === 'writing') {
      return { id: q.id, order_no: q.order_no, kind: 'writing', stem_text: q.stem_text, image_key: q.image_key, points: q.points, solution_text: q.solution_text };
    }
    const sel = chosen[q.id] ?? null;
    return {
      id: q.id, order_no: q.order_no, kind: 'mcq', stem_text: q.stem_text, image_key: q.image_key,
      options: JSON.parse(q.options_json), selected_index: sel, correct_index: q.correct_index,
      points: q.points, correct: sel === q.correct_index,
    };
  });
  return {
    review: {
      test_title: ses.test_title, class_name: ses.class_name, date: ses.scheduled_start,
      student: { id: stu.id, name: `${stu.surname} ${stu.first_name}` },
      mcq_score: result.mcq_score, mcq_max: result.mcq_max,
      writing_score: result.writing_score, writing_max: result.writing_max,
      questions,
    },
  };
}

export async function review(req, env) {
  const studentSession = await requireStudent(req, env);
  if (!studentSession) return err('Not logged in.', 401);
  const sessionId = Number(new URL(req.url).searchParams.get('session_id'));
  const { error, review: r } = await buildReview(env, sessionId, studentSession.id, { onlyIfPublished: true });
  return error || json(r);
}

export async function teacherReview(req, env, params) {
  const g = await needSession(req, env, params.sessionId, 'view'); if (g.resp) return g.resp;
  const { error, review: r } = await buildReview(env, Number(params.sessionId), params.studentId, { onlyIfPublished: false });
  return error || json(r);
}
