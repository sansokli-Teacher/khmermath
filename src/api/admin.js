// Teacher management (owner only), invite links, and sharing classes/tests.
import { json, err } from '../lib/http.js';
import { hashSecretValue } from '../lib/crypto.js';
import { createSessionCookie } from '../lib/session.js';
import { ensureColumns } from '../lib/schema.js';
import { authTeacher, needAdmin, needClass, needTest, isAdmin } from '../lib/access.js';

const INVITE_DAYS = 7;

async function sha256Hex(text) {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, '0')).join('');
}
function newToken() {
  const bytes = crypto.getRandomValues(new Uint8Array(24));
  return [...bytes].map((b) => b.toString(16).padStart(2, '0')).join('');
}
async function makeInvite(env, { purpose, teacherId = null, note = '', createdBy }) {
  const token = newToken();
  const expires = new Date(Date.now() + INVITE_DAYS * 86400000).toISOString().replace('T', ' ').slice(0, 19);
  await env.DB.prepare(
    'INSERT INTO invites (token_hash, purpose, teacher_id, note, created_by, expires_at) VALUES (?1, ?2, ?3, ?4, ?5, ?6)',
  ).bind(await sha256Hex(token), purpose, teacherId, String(note).slice(0, 80), createdBy, expires).run();
  return { token, expires_at: expires };
}

// ---------- owner: manage teachers ----------
export async function listTeachers(req, env) {
  const g = await needAdmin(req, env); if (g.resp) return g.resp;
  const { results } = await env.DB.prepare(
    `SELECT t.id, t.username, t.display_name, t.role, t.active, t.last_login,
            (SELECT COUNT(*) FROM classes c WHERE c.owner_id = t.id) AS class_count,
            (SELECT COUNT(*) FROM tests x WHERE x.owner_id = t.id) AS test_count
     FROM teachers t ORDER BY t.id`,
  ).all();
  const { results: invites } = await env.DB.prepare(
    `SELECT i.id, i.purpose, i.note, i.created_at, i.expires_at, COALESCE(t.display_name, t.username) AS teacher_name
     FROM invites i LEFT JOIN teachers t ON t.id = i.teacher_id
     WHERE i.used_at IS NULL AND i.expires_at > datetime('now') ORDER BY i.id DESC`,
  ).all();
  return json({ teachers: results, invites });
}

export async function createInvite(req, env) {
  const g = await needAdmin(req, env); if (g.resp) return g.resp;
  const { note } = await req.json().catch(() => ({}));
  const inv = await makeInvite(env, { purpose: 'invite', note: note || '', createdBy: g.t.id });
  return json(inv);
}

export async function createResetLink(req, env, params) {
  const g = await needAdmin(req, env); if (g.resp) return g.resp;
  const target = await env.DB.prepare('SELECT id FROM teachers WHERE id = ?1').bind(params.id).first();
  if (!target) return err('Teacher not found.', 404);
  const inv = await makeInvite(env, { purpose: 'reset', teacherId: target.id, createdBy: g.t.id });
  return json(inv);
}

export async function revokeInvite(req, env, params) {
  const g = await needAdmin(req, env); if (g.resp) return g.resp;
  await env.DB.prepare('DELETE FROM invites WHERE id = ?1 AND used_at IS NULL').bind(params.id).run();
  return json({ ok: true });
}

export async function setTeacherActive(req, env, params) {
  const g = await needAdmin(req, env); if (g.resp) return g.resp;
  if (Number(params.id) === g.t.id) return err('មិនអាចបិទគណនីរបស់ខ្លួនឯងបានទេ។', 400);
  const { active } = await req.json();
  await env.DB.prepare('UPDATE teachers SET active = ?1 WHERE id = ?2 AND role <> \'owner\'').bind(active ? 1 : 0, params.id).run();
  return json({ ok: true });
}

// ---------- public: open an invite / reset link ----------
async function loadInvite(env, token) {
  await ensureColumns(env);
  const inv = await env.DB.prepare(
    `SELECT i.id, i.purpose, i.teacher_id, i.note, t.username, COALESCE(t.display_name, t.username) AS teacher_name
     FROM invites i LEFT JOIN teachers t ON t.id = i.teacher_id
     WHERE i.token_hash = ?1 AND i.used_at IS NULL AND i.expires_at > datetime('now')`,
  ).bind(await sha256Hex(String(token))).first();
  return inv;
}

export async function inviteInfo(req, env, params) {
  const inv = await loadInvite(env, params.token);
  if (!inv) return err('តំណភ្ជាប់នេះមិនត្រឹមត្រូវ ឬបានផុតកំណត់ហើយ។ សូមសុំតំណថ្មីពីម្ចាស់ប្រព័ន្ធ។', 404);
  return json({ purpose: inv.purpose, note: inv.note, username: inv.username, teacher_name: inv.teacher_name });
}

export async function acceptInvite(req, env, params) {
  const inv = await loadInvite(env, params.token);
  if (!inv) return err('តំណភ្ជាប់នេះមិនត្រឹមត្រូវ ឬបានផុតកំណត់ហើយ។', 404);
  const { username, display_name, password } = await req.json();
  if (!password || password.length < 6) return err('ពាក្យសម្ងាត់ត្រូវមានយ៉ាងតិច ៦ តួអក្សរ។', 400);

  let finalUsername;
  if (inv.purpose === 'reset') {
    finalUsername = inv.username;
    const hash = await hashSecretValue(password, finalUsername, env.SESSION_SECRET);
    await env.DB.prepare('UPDATE teachers SET password_hash = ?1 WHERE id = ?2').bind(hash, inv.teacher_id).run();
  } else {
    finalUsername = String(username || '').trim();
    if (!/^[A-Za-z0-9_.\-]{3,30}$/.test(finalUsername)) return err('ឈ្មោះអ្នកប្រើត្រូវមាន ៣–៣០ តួ (អក្សរឡាតាំង លេខ _ . -)។', 400);
    const name = String(display_name || '').trim().slice(0, 60);
    if (!name) return err('សូមបញ្ចូលឈ្មោះរបស់អ្នក។', 400);
    const taken = await env.DB.prepare('SELECT 1 FROM teachers WHERE username = ?1').bind(finalUsername).first();
    if (taken) return err('ឈ្មោះអ្នកប្រើនេះមានគេប្រើរួចហើយ។ សូមជ្រើសរើសឈ្មោះផ្សេង។', 409);
    const hash = await hashSecretValue(password, finalUsername, env.SESSION_SECRET);
    await env.DB.prepare("INSERT INTO teachers (username, password_hash, role, display_name, last_login) VALUES (?1, ?2, 'teacher', ?3, datetime('now'))")
      .bind(finalUsername, hash, name).run();
  }
  await env.DB.prepare("UPDATE invites SET used_at = datetime('now') WHERE id = ?1").bind(inv.id).run();
  const cookie = await createSessionCookie({ role: 'teacher', username: finalUsername }, env.SESSION_SECRET);
  return json({ ok: true }, 200, { 'Set-Cookie': cookie });
}

// ---------- search + sharing ----------
export async function searchTeachers(req, env) {
  const t = await authTeacher(req, env);
  if (!t) return err('Not logged in.', 401);
  const q = (new URL(req.url).searchParams.get('q') || '').trim();
  const like = `%${q.replace(/[%_]/g, '')}%`;
  const { results } = await env.DB.prepare(
    `SELECT id, username, COALESCE(display_name, username) AS name FROM teachers
     WHERE active = 1 AND id <> ?1 AND (username LIKE ?2 OR display_name LIKE ?2) ORDER BY name LIMIT 10`,
  ).bind(t.id, like).all();
  return json({ teachers: results });
}

async function needResource(req, env, type, id, level) {
  return type === 'class' ? needClass(req, env, id, level) : needTest(req, env, id, level);
}

export async function listShares(req, env) {
  const url = new URL(req.url);
  const type = url.searchParams.get('type'), id = Number(url.searchParams.get('id'));
  if (!['class', 'test'].includes(type)) return err('type must be class or test.', 400);
  const g = await needResource(req, env, type, id, 'own'); if (g.resp) return g.resp;
  const { results } = await env.DB.prepare(
    `SELECT s.teacher_id, s.role, t.username, COALESCE(t.display_name, t.username) AS name
     FROM shares s JOIN teachers t ON t.id = s.teacher_id WHERE s.resource_type = ?1 AND s.resource_id = ?2 ORDER BY name`,
  ).bind(type, id).all();
  return json({ shares: results });
}

export async function setShare(req, env) {
  const { type, id, teacher_id, role } = await req.json();
  if (!['class', 'test'].includes(type)) return err('type must be class or test.', 400);
  if (!['reviewer', 'editor'].includes(role)) return err('role must be reviewer or editor.', 400);
  const g = await needResource(req, env, type, Number(id), 'own'); if (g.resp) return g.resp;
  if (Number(teacher_id) === g.t.id) return err('មិនអាចចែករំលែកទៅខ្លួនឯងបានទេ។', 400);
  const target = await env.DB.prepare('SELECT id FROM teachers WHERE id = ?1 AND active = 1').bind(Number(teacher_id)).first();
  if (!target) return err('រកមិនឃើញគ្រូនេះទេ។', 404);
  await env.DB.prepare(
    `INSERT INTO shares (resource_type, resource_id, teacher_id, role) VALUES (?1, ?2, ?3, ?4)
     ON CONFLICT(resource_type, resource_id, teacher_id) DO UPDATE SET role = ?4`,
  ).bind(type, Number(id), target.id, role).run();
  return json({ ok: true });
}

// The owner of the resource removes someone, or a co-teacher removes herself.
export async function removeShare(req, env) {
  const { type, id, teacher_id } = await req.json();
  if (!['class', 'test'].includes(type)) return err('type must be class or test.', 400);
  const t = await authTeacher(req, env);
  if (!t) return err('Not logged in.', 401);
  if (Number(teacher_id) !== t.id) {
    const g = await needResource(req, env, type, Number(id), 'own'); if (g.resp) return g.resp;
  }
  await env.DB.prepare('DELETE FROM shares WHERE resource_type = ?1 AND resource_id = ?2 AND teacher_id = ?3')
    .bind(type, Number(id), Number(teacher_id)).run();
  return json({ ok: true });
}
