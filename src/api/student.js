import { json, err } from '../lib/http.js';
import { createSessionCookie, clearSessionCookie, requireStudent } from '../lib/session.js';
import { needSession } from '../lib/access.js';
import { ensureColumns } from '../lib/schema.js';
import { allow } from '../lib/limits.js';
import { isRight, submitStudent } from '../lib/scoring.js';
import { studentYear } from './year.js';
import { sessionQuestions, ensureFrozen } from '../lib/frozen.js';

export { ensureColumns };

// ---------- time windows (with per-student extra minutes) ----------
function endOf(s) {
  return s.scheduled_end ? Date.parse(s.scheduled_end) : Date.parse(s.scheduled_start) + s.duration_minutes * 60000;
}
function windowFor(ses, extraMin = 0) {
  const start = Date.parse(ses.scheduled_start);
  const end = endOf(ses) + (extraMin || 0) * 60000;
  const now = Date.now();
  let phase;
  if (ses.status === 'closed') phase = 'closed';
  else if (now < start) phase = 'upcoming';
  else if (now < end) phase = 'open';
  else phase = 'closed';
  return { start, end, now, phase };
}
const SUBMIT_GRACE_MS = 5000; // forgive a submit that was already in flight when the clock hit zero

// ---------- login (ID only; optionally ID + date of birth, per class) ----------
const KH_DIGITS = '០១២៣៤៥៦៧៨៩';
const toAscii = (s) => String(s || '').replace(/[០-៩]/g, (d) => String(KH_DIGITS.indexOf(d)));
// All the (year, day, month) readings a typed or stored date could have. Day and month are
// compared as an unordered pair, so 10/03/2012 and 03/10/2012 both match.
function dobKeys(input) {
  const raw = toAscii(input).trim();
  const keys = new Set();
  const add = (y, a, b) => {
    y = Number(y); a = Number(a); b = Number(b);
    if (y < 100) y += y > 40 ? 1900 : 2000;
    if (y < 1900 || y > 2100 || a < 1 || b < 1 || a > 31 || b > 31) return;
    keys.add(`${y}-${Math.min(a, b)}-${Math.max(a, b)}`);
  };
  const groups = raw.match(/\d+/g) || [];
  if (groups.length >= 3) {
    const [x, y, z] = groups;
    if (x.length === 4 || Number(x) > 31) add(x, y, z);       // 2012-03-10
    else add(z, x, y);                                        // 10/03/2012, 10-03-12
  } else if (groups.length >= 1) {
    const d = groups.join('');                                  // 10102010 or '1010 2010'
    if (d.length === 8) { add(d.slice(4), d.slice(0, 2), d.slice(2, 4)); add(d.slice(0, 4), d.slice(4, 6), d.slice(6)); }   // 10032012 or 20120310
    else if (d.length === 6) add(d.slice(4), d.slice(0, 2), d.slice(2, 4));                                                  // 100312
    else if (d.length === 5 && Number(d) > 20000 && Number(d) < 80000) {                                                      // Excel date number
      const dt = new Date(Math.round((Number(d) - 25569) * 86400000));
      add(dt.getUTCFullYear(), dt.getUTCDate(), dt.getUTCMonth() + 1);
    }
  }
  return keys;
}
const dobMatches = (typed, stored) => { const t = dobKeys(typed); for (const k of dobKeys(stored)) if (t.has(k)) return true; return false; };

export async function login(req, env) {
  await ensureColumns(env);
  const { id, dob } = await req.json();
  if (!id) return err('សូមបញ្ចូលអត្តលេខសិស្ស។', 400);
  const student = await env.DB.prepare(
    'SELECT s.id, s.surname, s.first_name, s.class_id, s.dob, c.require_dob FROM students s JOIN classes c ON c.id = s.class_id WHERE s.id = ?1',
  ).bind(String(id).trim()).first();
  if (!student) return err('រកមិនឃើញអត្តលេខនេះទេ។ សូមពិនិត្យម្តងទៀត។', 401);
  if (student.require_dob && dobKeys(student.dob).size) {
    if (!dob) return json({ error: 'សូមបញ្ចូលថ្ងៃខែឆ្នាំកំណើតរបស់អ្នក។', need_dob: true }, 401);
    if (!(await allow(env, `dob:${student.id}`, 8, 600))) return err('ព្យាយាមច្រើនដងពេក។ សូមរង់ចាំ ១០ នាទី។', 429);
    if (!dobMatches(dob, student.dob)) return json({ error: 'ថ្ងៃខែឆ្នាំកំណើតមិនត្រឹមត្រូវទេ។', need_dob: true }, 401);
  }
  const fullName = `${student.surname} ${student.first_name}`;
  const cookie = await createSessionCookie(
    { role: 'student', id: student.id, name: fullName, classId: student.class_id }, env.SESSION_SECRET,
  );
  return json({ ok: true, name: fullName }, 200, { 'Set-Cookie': cookie });
}

export async function logout() {
  return json({ ok: true }, 200, { 'Set-Cookie': clearSessionCookie('student') });
}

// ---------- home ----------
export async function status(req, env) {
  const session = await requireStudent(req, env);
  if (!session) return err('Not logged in.', 401);
  await ensureColumns(env);
  const cls = await env.DB.prepare('SELECT name FROM classes WHERE id = ?1').bind(session.classId).first();
  const { results: rows } = await env.DB.prepare(
    `SELECT ts.id, ts.scheduled_start, ts.scheduled_end, ts.duration_minutes, ts.status,
            t.title AS test_title,
            r.mcq_score, r.mcq_max, r.writing_score, r.writing_max, r.started_at, r.submitted_at, r.published_at, r.extra_minutes
     FROM test_sessions ts
     JOIN tests t ON t.id = ts.test_id
     LEFT JOIN results r ON r.session_id = ts.id AND r.student_id = ?2
     WHERE ts.class_id = ?1
     ORDER BY ts.scheduled_start DESC`,
  ).bind(session.classId, session.id).all();

  const upcoming = [];
  const history = [];
  for (const r of rows) {
    const phase = windowFor(r, r.extra_minutes).phase;
    const base = {
      session_id: r.id, test_title: r.test_title,
      scheduled_start: r.scheduled_start, scheduled_end: new Date(endOf(r) + (r.extra_minutes || 0) * 60000).toISOString(),
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
// their class, be open (counting their own extra minutes), have been unlocked with
// its PIN, not be submitted, and be on the device that started it.
async function loadActiveSession(env, studentSession, sessionId, graceMs = 0, deviceId = null) {
  if (!sessionId) return null;
  const ses = await env.DB.prepare(
    `SELECT ts.*, t.title AS test_title FROM test_sessions ts JOIN tests t ON t.id = ts.test_id
     WHERE ts.id = ?1 AND ts.class_id = ?2`,
  ).bind(sessionId, studentSession.classId).first();
  if (!ses) return null;
  const result = await env.DB.prepare(
    'SELECT started_at, submitted_at, extra_minutes, device_id, locked FROM results WHERE session_id = ?1 AND student_id = ?2',
  ).bind(ses.id, studentSession.id).first();
  if (!result || !result.started_at || result.submitted_at) return null;
  if (result.device_id && deviceId && result.device_id !== deviceId) return null;
  const window = windowFor(ses, result.extra_minutes);
  const inGrace = graceMs > 0 && ses.status !== 'closed' && Date.now() < window.end + graceMs;
  if (window.phase !== 'open' && !inGrace) return null;
  return { ...ses, window, locked: !!result.locked };
}

const deviceOf = (req) => req.headers.get('X-Device') || null;

// ---------- start (PIN, waiting, device lock) ----------
export async function start(req, env) {
  const studentSession = await requireStudent(req, env);
  if (!studentSession) return err('Not logged in.', 401);
  await ensureColumns(env);
  const { session_id, pin } = await req.json();
  const device = deviceOf(req);
  const ses = await env.DB.prepare(
    'SELECT * FROM test_sessions WHERE id = ?1 AND class_id = ?2',
  ).bind(session_id, studentSession.classId).first();
  if (!ses) return err('រកមិនឃើញការប្រឡងនេះទេ។', 404);

  const result = await env.DB.prepare(
    'SELECT id, started_at, submitted_at, extra_minutes, device_id FROM results WHERE session_id = ?1 AND student_id = ?2',
  ).bind(ses.id, studentSession.id).first();
  if (result && result.submitted_at) return err('អ្នកបានប្រគល់ការប្រឡងនេះរួចហើយ។', 403);

  const window = windowFor(ses, result ? result.extra_minutes : 0);
  // A student who already entered the PIN (e.g. refreshed the page or the phone
  // restarted) may resume without typing it again — on the same device.
  const alreadyUnlocked = result && result.started_at;
  if (alreadyUnlocked && result.device_id && device && result.device_id !== device) {
    return json({ error: 'ការប្រឡងនេះកំពុងបើកលើឧបករណ៍ផ្សេង។ សូមសុំលោកគ្រូអ្នកគ្រូអនុញ្ញាតឱ្យប្តូរឧបករណ៍។', device: true }, 409);
  }
  if (!alreadyUnlocked) {
    const expected = ses.pin == null ? '' : String(ses.pin).trim().toLowerCase();
    if (expected) {
      if (!(await allow(env, `pin:${ses.id}:${studentSession.id}`, 12, 600))) return err('បញ្ចូល PIN ច្រើនដងពេក។ សូមរង់ចាំ ១០ នាទី ឬសួរលោកគ្រូ។', 429);
      if (String(pin ?? '').trim().toLowerCase() !== expected) return err('PIN មិនត្រឹមត្រូវទេ។ សូមសួរលោកគ្រូ។', 401);
    }
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

  await ensureFrozen(env, ses.id);   // from the first start on, everyone sees the same fixed questions
  if (!result) {
    await env.DB.prepare(
      "INSERT INTO results (session_id, student_id, mcq_score, mcq_max, started_at, device_id, last_seen) VALUES (?1, ?2, 0, 0, datetime('now'), ?3, datetime('now'))",
    ).bind(ses.id, studentSession.id, device).run();
  } else if (!result.started_at) {
    await env.DB.prepare("UPDATE results SET started_at = datetime('now'), device_id = ?2, last_seen = datetime('now') WHERE id = ?1").bind(result.id, device).run();
  } else if (!result.device_id && device) {
    await env.DB.prepare('UPDATE results SET device_id = ?2 WHERE id = ?1').bind(result.id, device).run();
  }
  return json({ ok: true, waiting: false, server_now: Date.now() });
}

// ---------- shuffling ----------
function rng(seedText) {
  let h = 2166136261;
  for (const ch of seedText) { h ^= ch.charCodeAt(0); h = Math.imul(h, 16777619) >>> 0; }
  return () => { h = (Math.imul(h ^ (h >>> 15), 2246822507) + 0x6D2B79F5) >>> 0; return h / 4294967296; };
}
function seededShuffle(items, seedText) {
  const rand = rng(seedText);
  const a = items.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(rand() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}
// displayed option j shows real option perm[j]
function optionPerm(n, sessionId, studentId, questionId) {
  return seededShuffle([...Array(n).keys()], `opt:${sessionId}:${studentId}:${questionId}`);
}

// ---------- the test ----------
export async function getTest(req, env) {
  const studentSession = await requireStudent(req, env);
  if (!studentSession) return err('Not logged in.', 401);
  await ensureColumns(env);
  const sessionId = Number(new URL(req.url).searchParams.get('session_id'));
  const active = await loadActiveSession(env, studentSession, sessionId, 0, deviceOf(req));
  if (!active) return err('No test is open for you right now.', 403);
  const integrity = { mode: active.integrity_mode || 'warn', max: active.max_violations || 3 };
  if (active.locked) return json({ session_id: active.id, test_title: active.test_title, end_at: active.window.end, server_now: Date.now(), locked: true, integrity, questions: [] });

  const orderedQuestions = (await sessionQuestions(env, active.id, active.test_id))
    .sort((a, b) => (a.kind === 'writing') - (b.kind === 'writing') || a.order_no - b.order_no);
  // Each student sees the multiple-choice questions in their own fixed order (same
  // every reload); the writing section keeps its printed order after them.
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
    integrity,
    questions: questions.map((q) => {
      let options = JSON.parse(q.options_json);
      let sel = savedByQuestion[q.id] ?? null;
      if (q.kind !== 'writing' && q.shuffle && options.length > 1) {
        const perm = optionPerm(options.length, active.id, studentSession.id, q.id);
        options = perm.map((i) => options[i]);
        sel = sel == null ? null : perm.indexOf(sel);
      }
      return { id: q.id, stem_text: q.stem_text, image_key: q.image_key, kind: q.kind, points: q.points, options, selected_index: sel };
    }),
  });
}

// Light poll while taking the test: has the teacher extended the time, submitted for
// the student, or closed the exam? Also tells the teacher the student is online.
export async function heartbeat(req, env) {
  const studentSession = await requireStudent(req, env);
  if (!studentSession) return err('Not logged in.', 401);
  const sessionId = Number(new URL(req.url).searchParams.get('session_id'));
  const active = await loadActiveSession(env, studentSession, sessionId, SUBMIT_GRACE_MS, deviceOf(req));
  if (!active) return json({ open: false, server_now: Date.now() });
  await env.DB.prepare(
    "UPDATE results SET last_seen = datetime('now') WHERE session_id = ?1 AND student_id = ?2 AND (last_seen IS NULL OR last_seen < datetime('now', '-40 seconds'))",
  ).bind(active.id, studentSession.id).run();
  return json({ open: true, locked: active.locked, end_at: active.window.end, server_now: Date.now() });
}

// The student's page reports each time it was left (tab switch, app switch).
export async function leftPage(req, env) {
  const studentSession = await requireStudent(req, env);
  if (!studentSession) return err('Not logged in.', 401);
  const { session_id } = await req.json().catch(() => ({}));
  const active = await loadActiveSession(env, studentSession, Number(session_id), 0, deviceOf(req));
  if (!active) return json({ ok: true });
  await ensureColumns(env);
  await env.DB.prepare('UPDATE results SET tab_switches = tab_switches + 1 WHERE session_id = ?1 AND student_id = ?2')
    .bind(active.id, studentSession.id).run();
  return json({ ok: true });
}

async function questionMap(env, sessionId, testId) {
  const results = (await sessionQuestions(env, sessionId, testId)).filter((q) => q.kind !== 'writing');
  return Object.fromEntries(results.map((q) => [q.id, { n: JSON.parse(q.options_json).length, shuffle: q.shuffle }]));
}
function realIndex(q, displayed, sessionId, studentId, questionId) {
  if (!Number.isInteger(displayed) || displayed < 0 || displayed >= q.n) return null;
  return q.shuffle ? optionPerm(q.n, sessionId, studentId, questionId)[displayed] : displayed;
}

export async function answer(req, env) {
  const studentSession = await requireStudent(req, env);
  if (!studentSession) return err('Not logged in.', 401);
  await ensureColumns(env);
  const { session_id, question_id, selected_index } = await req.json();
  const active = await loadActiveSession(env, studentSession, Number(session_id), SUBMIT_GRACE_MS, deviceOf(req));
  if (!active) return err('This test is not open anymore.', 403);
  if (active.locked) return json({ error: 'locked', locked: true }, 423);
  const qm = await questionMap(env, active.id, active.test_id);
  const q = qm[question_id];
  if (!q) return err('That question is not part of this test.', 400);
  const real = realIndex(q, Number(selected_index), active.id, studentSession.id, Number(question_id));
  if (real == null) return err('Invalid option.', 400);
  await env.DB.prepare(
    `INSERT INTO responses (session_id, student_id, question_id, selected_index) VALUES (?1, ?2, ?3, ?4)
     ON CONFLICT(session_id, student_id, question_id) DO UPDATE SET selected_index = ?4, answered_at = datetime('now')`,
  ).bind(active.id, studentSession.id, question_id, real).run();
  return json({ ok: true, end_at: active.window.end });
}

// Submit. The page also sends every answer it knows about, so a save that failed
// earlier on a bad connection is not lost.
export async function submit(req, env) {
  const studentSession = await requireStudent(req, env);
  if (!studentSession) return err('Not logged in.', 401);
  await ensureColumns(env);
  let body = {};
  try { body = await req.json(); } catch {}
  const active = await loadActiveSession(env, studentSession, Number(body.session_id), SUBMIT_GRACE_MS, deviceOf(req));
  if (!active) return err('This test is not open anymore.', 403);
  const submitType = body.submit_type === 'auto' ? 'auto' : 'manual';

  if (body.answers && typeof body.answers === 'object') {
    const qm = await questionMap(env, active.id, active.test_id);
    const stmts = [];
    for (const [qid, displayed] of Object.entries(body.answers)) {
      const q = qm[qid];
      if (!q) continue;
      const real = realIndex(q, Number(displayed), active.id, studentSession.id, Number(qid));
      if (real == null) continue;
      stmts.push(env.DB.prepare(
        `INSERT INTO responses (session_id, student_id, question_id, selected_index) VALUES (?1, ?2, ?3, ?4)
         ON CONFLICT(session_id, student_id, question_id) DO UPDATE SET selected_index = ?4, answered_at = datetime('now')`,
      ).bind(active.id, studentSession.id, Number(qid), real));
    }
    if (stmts.length) await env.DB.batch(stmts);
  }
  await submitStudent(env, active, studentSession.id, submitType);
  return json({ ok: true, submit_type: submitType });
}

// ---------- review of a published attempt ----------
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

  const qs = await sessionQuestions(env, sessionId, ses.test_id);
  const { results: rs } = await env.DB.prepare('SELECT question_id, selected_index FROM responses WHERE session_id = ?1 AND student_id = ?2')
    .bind(sessionId, studentId).all();
  const chosen = Object.fromEntries(rs.map((r) => [r.question_id, r.selected_index]));
  const { results: wm } = await env.DB.prepare('SELECT question_id, score FROM writing_marks WHERE session_id = ?1 AND student_id = ?2').bind(sessionId, studentId).all();
  const marks = Object.fromEntries(wm.map((m) => [m.question_id, m.score]));

  const questions = qs.map((q) => {
    if (q.kind === 'writing') {
      return { id: q.id, order_no: q.order_no, kind: 'writing', stem_text: q.stem_text, image_key: q.image_key, points: q.points, solution_text: q.solution_text, topic: q.topic, mark: marks[q.id] ?? null };
    }
    const sel = chosen[q.id] ?? null;
    return {
      id: q.id, order_no: q.order_no, kind: 'mcq', stem_text: q.stem_text, image_key: q.image_key,
      options: JSON.parse(q.options_json), selected_index: sel, correct_index: q.correct_index, alt_correct_index: q.alt_correct_index,
      cancelled: q.cancelled, points: q.points, topic: q.topic, level: q.level, solution_text: q.solution_text, correct: isRight(q, sel),
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
