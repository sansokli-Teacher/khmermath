import { json, err } from '../lib/http.js';
import { hashSecretValue, verifySecretValue } from '../lib/crypto.js';
import { createSessionCookie, clearSessionCookie, requireTeacher } from '../lib/session.js';

export async function setupStatus(req, env) {
  const { results } = await env.DB.prepare('SELECT COUNT(*) AS n FROM teachers').all();
  return json({ needs_setup: results[0].n === 0 });
}

// One-time setup: creates the first (and, for now, only) teacher account.
// Refuses once a teacher already exists, so this can't be re-run by someone
// who just finds the URL later.
export async function setup(req, env) {
  const { results } = await env.DB.prepare('SELECT COUNT(*) AS n FROM teachers').all();
  if (results[0].n > 0) return err('A teacher account already exists.', 403);
  const { username, password } = await req.json();
  if (!username || !password || password.length < 6) {
    return err('Username and a password of at least 6 characters are required.', 400);
  }
  const hash = await hashSecretValue(password, username, env.SESSION_SECRET);
  await env.DB.prepare('INSERT INTO teachers (username, password_hash) VALUES (?1, ?2)').bind(username, hash).run();
  const cookie = await createSessionCookie({ role: 'teacher', username }, env.SESSION_SECRET);
  return json({ ok: true }, 200, { 'Set-Cookie': cookie });
}

export async function login(req, env) {
  const { username, password } = await req.json();
  const row = await env.DB.prepare('SELECT username, password_hash FROM teachers WHERE username = ?1').bind(username).first();
  if (!row) return err('Incorrect username or password.', 401);
  const ok = await verifySecretValue(password, row.username, env.SESSION_SECRET, row.password_hash);
  if (!ok) return err('Incorrect username or password.', 401);
  const cookie = await createSessionCookie({ role: 'teacher', username: row.username }, env.SESSION_SECRET);
  return json({ ok: true }, 200, { 'Set-Cookie': cookie });
}

export async function logout() {
  return json({ ok: true }, 200, { 'Set-Cookie': clearSessionCookie('teacher') });
}

export async function me(req, env) {
  const session = await requireTeacher(req, env);
  if (!session) return err('Not logged in.', 401);
  return json({ username: session.username });
}

export async function changePassword(req, env) {
  const session = await requireTeacher(req, env);
  if (!session) return err('Not logged in.', 401);
  const { current_password, new_password } = await req.json();
  if (!new_password || new_password.length < 6) {
    return err('ពាក្យសម្ងាត់ថ្មីត្រូវមានយ៉ាងតិច ៦ តួអក្សរ។', 400);
  }
  const teacher = await env.DB.prepare('SELECT username, password_hash FROM teachers WHERE username = ?1')
    .bind(session.username).first();
  const ok = await verifySecretValue(current_password, teacher.username, env.SESSION_SECRET, teacher.password_hash);
  if (!ok) return err('ពាក្យសម្ងាត់បច្ចុប្បន្នមិនត្រឹមត្រូវទេ។', 401);

  const newHash = await hashSecretValue(new_password, teacher.username, env.SESSION_SECRET);
  await env.DB.prepare('UPDATE teachers SET password_hash = ?1 WHERE username = ?2').bind(newHash, teacher.username).run();
  return json({ ok: true });
}
