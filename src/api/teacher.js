import { json, err } from '../lib/http.js';
import { hashSecretValue, verifySecretValue } from '../lib/crypto.js';
import { createSessionCookie, clearSessionCookie } from '../lib/session.js';
import { ensureColumns } from '../lib/schema.js';
import { authTeacher } from '../lib/access.js';

export async function setupStatus(req, env) {
  const { results } = await env.DB.prepare('SELECT COUNT(*) AS n FROM teachers').all();
  return json({ needs_setup: results[0].n === 0 });
}

// One-time setup: creates the first account, which is the owner. Refuses once any
// teacher exists; every later teacher joins through an invite link.
export async function setup(req, env) {
  const { results } = await env.DB.prepare('SELECT COUNT(*) AS n FROM teachers').all();
  if (results[0].n > 0) return err('A teacher account already exists.', 403);
  const { username, password } = await req.json();
  if (!username || !password || password.length < 6) {
    return err('Username and a password of at least 6 characters are required.', 400);
  }
  await ensureColumns(env);
  const hash = await hashSecretValue(password, username, env.SESSION_SECRET);
  await env.DB.prepare("INSERT INTO teachers (username, password_hash, role, display_name) VALUES (?1, ?2, 'owner', ?1)").bind(username, hash).run();
  const cookie = await createSessionCookie({ role: 'teacher', username }, env.SESSION_SECRET);
  return json({ ok: true }, 200, { 'Set-Cookie': cookie });
}

export async function login(req, env) {
  await ensureColumns(env);
  const { username, password } = await req.json();
  const row = await env.DB.prepare('SELECT username, password_hash, active FROM teachers WHERE username = ?1').bind(username).first();
  if (!row) return err('Incorrect username or password.', 401);
  const ok = await verifySecretValue(password, row.username, env.SESSION_SECRET, row.password_hash);
  if (!ok) return err('Incorrect username or password.', 401);
  if (!row.active) return err('គណនីនេះត្រូវបានបិទ។ សូមទាក់ទងម្ចាស់ប្រព័ន្ធ។', 403);
  await env.DB.prepare("UPDATE teachers SET last_login = datetime('now') WHERE username = ?1").bind(row.username).run();
  const cookie = await createSessionCookie({ role: 'teacher', username: row.username }, env.SESSION_SECRET);
  return json({ ok: true }, 200, { 'Set-Cookie': cookie });
}

export async function logout() {
  return json({ ok: true }, 200, { 'Set-Cookie': clearSessionCookie('teacher') });
}

export async function me(req, env) {
  const t = await authTeacher(req, env);
  if (!t) return err('Not logged in.', 401);
  return json({ id: t.id, username: t.username, role: t.role, display_name: t.display_name });
}

export async function changePassword(req, env) {
  const t = await authTeacher(req, env);
  if (!t) return err('Not logged in.', 401);
  const { current_password, new_password } = await req.json();
  if (!new_password || new_password.length < 6) {
    return err('ពាក្យសម្ងាត់ថ្មីត្រូវមានយ៉ាងតិច ៦ តួអក្សរ។', 400);
  }
  const teacher = await env.DB.prepare('SELECT username, password_hash FROM teachers WHERE id = ?1').bind(t.id).first();
  const ok = await verifySecretValue(current_password, teacher.username, env.SESSION_SECRET, teacher.password_hash);
  if (!ok) return err('ពាក្យសម្ងាត់បច្ចុប្បន្នមិនត្រឹមត្រូវទេ។', 401);

  const newHash = await hashSecretValue(new_password, teacher.username, env.SESSION_SECRET);
  await env.DB.prepare('UPDATE teachers SET password_hash = ?1 WHERE id = ?2').bind(newHash, t.id).run();
  return json({ ok: true });
}
