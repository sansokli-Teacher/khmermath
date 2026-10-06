// Who may see or change what. Every teacher-facing endpoint goes through here.
//   admin  (teachers.role = 'owner')   — everything
//   owner  of a class/test              — everything on it, can share it
//   editor (shared)                      — view + change
//   reviewer (shared)                    — view only (+ can leave notes on questions)
import { err } from './http.js';
import { requireTeacher } from './session.js';
import { ensureColumns } from './schema.js';

export async function authTeacher(req, env) {
  const session = await requireTeacher(req, env);
  if (!session) return null;
  await ensureColumns(env);
  const row = await env.DB.prepare(
    'SELECT id, username, role, display_name, active FROM teachers WHERE username = ?1',
  ).bind(session.username).first();
  if (!row || !row.active) return null;
  return { id: row.id, username: row.username, role: row.role, display_name: row.display_name || row.username };
}

export const isAdmin = (t) => t.role === 'owner';

const RANK = { reviewer: 1, editor: 2, owner: 3 };

async function accessTo(env, t, type, id, ownerId) {
  if (isAdmin(t) || ownerId === t.id) return 'owner';
  const sh = await env.DB.prepare(
    'SELECT role FROM shares WHERE resource_type = ?1 AND resource_id = ?2 AND teacher_id = ?3',
  ).bind(type, id, t.id).first();
  return sh ? sh.role : null;
}

export async function classAccess(env, t, classId) {
  const c = await env.DB.prepare('SELECT id, owner_id FROM classes WHERE id = ?1').bind(classId).first();
  if (!c) return null;
  return accessTo(env, t, 'class', c.id, c.owner_id);
}

export async function testAccess(env, t, testId) {
  const x = await env.DB.prepare('SELECT id, owner_id FROM tests WHERE id = ?1').bind(testId).first();
  if (!x) return null;
  return accessTo(env, t, 'test', x.id, x.owner_id);
}

// level: 'view' | 'edit' | 'own'
const NEED = { view: 1, edit: 2, own: 3 };
function check(acc, level) {
  return acc != null && RANK[acc] >= NEED[level];
}
function denied(acc) {
  if (acc == null) return err('រកមិនឃើញ ឬអ្នកមិនមានសិទ្ធិចូលមើលទេ។', 404);
  return err('អ្នកមានសិទ្ធិមើលតែប៉ុណ្ណោះ (អ្នកពិនិត្យ) មិនអាចកែប្រែបានទេ។', 403);
}

// Each helper resolves to {t, acc} on success or {resp} (a ready Response) on failure.
export async function needClass(req, env, classId, level) {
  const t = await authTeacher(req, env);
  if (!t) return { resp: err('Not logged in.', 401) };
  const acc = await classAccess(env, t, Number(classId));
  return check(acc, level) ? { t, acc } : { resp: denied(acc) };
}

export async function needTest(req, env, testId, level) {
  const t = await authTeacher(req, env);
  if (!t) return { resp: err('Not logged in.', 401) };
  const acc = await testAccess(env, t, Number(testId));
  return check(acc, level) ? { t, acc } : { resp: denied(acc) };
}

export async function needSession(req, env, sessionId, level) {
  const t = await authTeacher(req, env);
  if (!t) return { resp: err('Not logged in.', 401) };
  const ses = await env.DB.prepare('SELECT id, class_id, test_id FROM test_sessions WHERE id = ?1').bind(Number(sessionId)).first();
  if (!ses) return { resp: err('Session not found.', 404) };
  const acc = await classAccess(env, t, ses.class_id);
  // Running a session needs 'edit' on the class; just reading it needs 'view'.
  return check(acc, level) ? { t, acc, ses } : { resp: denied(acc) };
}

export async function needQuestion(req, env, questionId, level) {
  const t = await authTeacher(req, env);
  if (!t) return { resp: err('Not logged in.', 401) };
  const q = await env.DB.prepare('SELECT id, test_id FROM test_questions WHERE id = ?1').bind(Number(questionId)).first();
  if (!q) return { resp: err('Question not found.', 404) };
  const acc = await testAccess(env, t, q.test_id);
  return check(acc, level) ? { t, acc, q } : { resp: denied(acc) };
}

export async function needStudent(req, env, studentId, level) {
  const t = await authTeacher(req, env);
  if (!t) return { resp: err('Not logged in.', 401) };
  const s = await env.DB.prepare('SELECT id, class_id FROM students WHERE id = ?1').bind(String(studentId)).first();
  if (!s) return { resp: err('Student not found.', 404) };
  const acc = await classAccess(env, t, s.class_id);
  return check(acc, level) ? { t, acc, s } : { resp: denied(acc) };
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
    `SELECT x.id, x.owner_id, (SELECT role FROM shares s WHERE s.resource_type='test' AND s.resource_id=x.id AND s.teacher_id=?1) AS shared_role FROM tests x`,
  ).bind(t.id).all();
  const map = new Map();
  for (const x of results) {
    const acc = isAdmin(t) || x.owner_id === t.id ? 'owner' : x.shared_role;
    if (acc) map.set(x.id, acc);
  }
  return map;
}
