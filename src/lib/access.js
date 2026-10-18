// Who may see or change what. Every teacher-facing endpoint goes through here.
//   admin (teachers.role = 'owner') — class administration; tests remain private
//   owner  of a class/test              — everything on it, can share it
//   editor (shared)                      — view + change
//   reviewer (shared)                    — view only (+ can leave notes on questions)
//   sample                               — the owner's showcase tests: view only, answers hidden
// On top of that, a teacher whose account is not unlocked (trial, or licence
// expired) is limited to *viewing*: any change is refused with HTTP 402.
import { json, err } from './http.js';
import { requireTeacher } from './session.js';
import { ensureColumns } from './schema.js';
import { TRIAL, PLANS } from './plans.js';

function nowStamp() { return new Date().toISOString().replace('T', ' ').slice(0, 19); }

export async function authTeacher(req, env) {
  const session = await requireTeacher(req, env);
  if (!session) return null;
  await ensureColumns(env);
  const row = await env.DB.prepare(
    'SELECT id, username, role, display_name, active, plan, license_until FROM teachers WHERE username = ?1',
  ).bind(session.username).first();
  if (!row || !row.active) return null;
  const owner = row.role === 'owner';
  const inDate = !row.license_until || row.license_until > nowStamp();
  const licensed = owner || (row.plan === 'full' && inDate);
  const status = owner ? 'owner' : licensed ? 'full' : row.plan === 'trial' ? 'trial' : 'expired';
  return {
    id: row.id, username: row.username, role: row.role, display_name: row.display_name || row.username,
    plan: row.plan, license_until: row.license_until, licensed, status,
  };
}

export const isAdmin = (t) => t.role === 'owner';

const RANK = { sample: 1, reviewer: 1, editor: 2, owner: 3 };
const NEED = { view: 1, edit: 2, own: 3 };

export function lockedResponse(t) {
  const msg = t && t.status === 'expired'
    ? 'ការប្រើប្រាស់របស់អ្នកបានផុតកំណត់ — អ្នកអាចមើលទិន្នន័យបាន តែមិនអាចកែប្រែបានទេ។ សូមបញ្ចូលកូដថ្មីដើម្បីបន្ត។'
    : 'គណនីសាកល្បង — មុខងារនេះត្រូវការកូដដោះសោពីម្ចាស់ប្រព័ន្ធ។';
  return json({ error: msg, locked: true, status: t ? t.status : 'trial' }, 402);
}

async function accessTo(env, t, type, id, ownerId, isSample = 0) {
  if (isAdmin(t) || ownerId === t.id) return 'owner';
  const sh = await env.DB.prepare(
    'SELECT role FROM shares WHERE resource_type = ?1 AND resource_id = ?2 AND teacher_id = ?3',
  ).bind(type, id, t.id).first();
  if (sh) return sh.role;
  return isSample ? 'sample' : null;
}

export async function classAccess(env, t, classId) {
  const c = await env.DB.prepare('SELECT id, owner_id FROM classes WHERE id = ?1').bind(classId).first();
  if (!c) return null;
  return accessTo(env, t, 'class', c.id, c.owner_id);
}

export async function testAccess(env, t, testId) {
  const x = await env.DB.prepare('SELECT id, owner_id, is_sample FROM tests WHERE id = ?1').bind(testId).first();
  if (!x) return null;
  // Personal tests require ownership or an explicit share, including for admins.
  if (x.owner_id === t.id) return 'owner';
  const share = await env.DB.prepare("SELECT role FROM shares WHERE resource_type = 'test' AND resource_id = ?1 AND teacher_id = ?2").bind(x.id, t.id).first();
  return share?.role || null;
}

// A free trial account may do real work on what it owns, up to the TRIAL limits (see plans.js).
export function limitResponse(what, max) {
  return json({
    error: `គណនីសាកល្បងឥតគិតថ្លៃអនុញ្ញាតត្រឹម ${max} ${what}។ ដើម្បីបន្ត សូមដោះសោគណនី (១ ឆ្នាំ $${PLANS.year.price} · ១ ខែ $${PLANS.month.price})។`,
    locked: true, limit: true, status: 'trial',
  }, 402);
}

export async function trialUsage(env, t) {
  const one = async (sql) => (await env.DB.prepare(sql).bind(t.id).first()).n;
  return {
    classes: await one('SELECT COUNT(*) AS n FROM classes WHERE owner_id = ?1'),
    students: await one('SELECT COUNT(*) AS n FROM students s JOIN classes c ON c.id = s.class_id WHERE c.owner_id = ?1'),
    tests: await one('SELECT COUNT(*) AS n FROM tests WHERE owner_id = ?1 AND is_bank = 0'),
    sessions: await one('SELECT COUNT(*) AS n FROM test_sessions s JOIN classes c ON c.id = s.class_id WHERE c.owner_id = ?1'),
  };
}

function denied(acc) {
  if (acc == null) return err('រកមិនឃើញ ឬអ្នកមិនមានសិទ្ធិចូលមើលទេ។', 404);
  if (acc === 'sample') return err('នេះជាតេស្តគំរូ — មើលបានតែប៉ុណ្ណោះ។', 403);
  return err('អ្នកមានសិទ្ធិមើលតែប៉ុណ្ណោះ (អ្នកពិនិត្យ) មិនអាចកែប្រែបានទេ។', 403);
}

// Returns a ready Response when the request must be refused, else null.
function gate(t, acc, level) {
  if (acc == null || RANK[acc] < NEED[level]) return denied(acc);
  if (NEED[level] > 1 && !t.licensed && !(t.status === 'trial' && acc === 'owner')) return lockedResponse(t);
  return null;
}

// trialOk: free-trial accounts may use this feature (the endpoint enforces the TRIAL limits itself).
export async function needLicense(req, env, trialOk = false) {
  const t = await authTeacher(req, env);
  if (!t) return { resp: err('Not logged in.', 401) };
  if (!t.licensed && !(trialOk && t.status === 'trial')) return { resp: lockedResponse(t) };
  return { t };
}

export async function needClass(req, env, classId, level) {
  const t = await authTeacher(req, env);
  if (!t) return { resp: err('Not logged in.', 401) };
  const acc = await classAccess(env, t, Number(classId));
  const r = gate(t, acc, level);
  return r ? { resp: r } : { t, acc };
}

export async function needTest(req, env, testId, level) {
  const t = await authTeacher(req, env);
  if (!t) return { resp: err('Not logged in.', 401) };
  const acc = await testAccess(env, t, Number(testId));
  const r = gate(t, acc, level);
  return r ? { resp: r } : { t, acc };
}

export async function needSession(req, env, sessionId, level) {
  const t = await authTeacher(req, env);
  if (!t) return { resp: err('Not logged in.', 401) };
  const ses = await env.DB.prepare('SELECT id, class_id, test_id FROM test_sessions WHERE id = ?1').bind(Number(sessionId)).first();
  if (!ses) return { resp: err('Session not found.', 404) };
  const acc = await classAccess(env, t, ses.class_id);
  const r = gate(t, acc, level);
  return r ? { resp: r } : { t, acc, ses };
}

export async function needQuestion(req, env, questionId, level) {
  const t = await authTeacher(req, env);
  if (!t) return { resp: err('Not logged in.', 401) };
  const q = await env.DB.prepare('SELECT id, test_id FROM test_questions WHERE id = ?1').bind(Number(questionId)).first();
  if (!q) return { resp: err('Question not found.', 404) };
  const acc = await testAccess(env, t, q.test_id);
  // Notes are for real co-teachers; sample viewers cannot write them.
  if (acc === 'sample' && level !== 'view') return { resp: denied(acc) };
  const r = acc === 'sample' && level === 'view' ? denied(acc) : gate(t, acc, level);
  return r ? { resp: r } : { t, acc, q };
}

export async function needStudent(req, env, studentId, level) {
  const t = await authTeacher(req, env);
  if (!t) return { resp: err('Not logged in.', 401) };
  const s = await env.DB.prepare('SELECT id, class_id FROM students WHERE id = ?1').bind(String(studentId)).first();
  if (!s) return { resp: err('Student not found.', 404) };
  const acc = await classAccess(env, t, s.class_id);
  const r = gate(t, acc, level);
  return r ? { resp: r } : { t, acc, s };
}

export async function needAdmin(req, env) {
  const t = await authTeacher(req, env);
  if (!t) return { resp: err('Not logged in.', 401) };
  if (!isAdmin(t)) return { resp: err('សម្រាប់ម្ចាស់ប្រព័ន្ធតែប៉ុណ្ណោះ។', 403) };
  return { t };
}

// All class ids / test ids this teacher may at least view, with their access level.
export async function accessibleClasses(env, t) {
  const { results } = await env.DB.prepare(
    `SELECT c.id, c.owner_id, (SELECT role FROM shares s WHERE s.resource_type='class' AND s.resource_id=c.id AND s.teacher_id=?1) AS shared_role FROM classes c`,
  ).bind(t.id).all();
  const map = new Map();
  for (const c of results) {
    const acc = isAdmin(t) || c.owner_id === t.id ? 'owner' : c.shared_role;
    if (acc) map.set(c.id, acc);
  }
  return map;
}

export async function accessibleTests(env, t) {
  const { results } = await env.DB.prepare(
    `SELECT x.id, x.owner_id, x.is_sample, (SELECT role FROM shares s WHERE s.resource_type='test' AND s.resource_id=x.id AND s.teacher_id=?1) AS shared_role FROM tests x`,
  ).bind(t.id).all();
  const map = new Map();
  for (const x of results) {
    const acc = x.owner_id === t.id ? 'owner' : x.shared_role;
    if (acc) map.set(x.id, acc);
  }
  return map;
}
