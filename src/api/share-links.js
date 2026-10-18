import { json, err } from '../lib/http.js';
import { authTeacher, needTest } from '../lib/access.js';

async function setup(env) {
  await env.DB.prepare(`CREATE TABLE IF NOT EXISTS test_share_links (
    id INTEGER PRIMARY KEY AUTOINCREMENT, token_hash TEXT NOT NULL UNIQUE,
    test_id INTEGER NOT NULL, created_by INTEGER NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('reviewer','editor')),
    expires_at TEXT NOT NULL, used_by INTEGER, revoked INTEGER NOT NULL DEFAULT 0
  )`).run();
}
async function hash(token) {
  const bytes = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(token));
  return [...new Uint8Array(bytes)].map(b => b.toString(16).padStart(2, '0')).join('');
}
export async function create(req, env) {
  const { test_id, role = 'reviewer' } = await req.json();
  const g = await needTest(req, env, test_id, 'own'); if (g.resp) return g.resp;
  if (!['reviewer', 'editor'].includes(role)) return err('Invalid role.', 400);
  await setup(env);
  const token = [...crypto.getRandomValues(new Uint8Array(24))].map(b => b.toString(16).padStart(2, '0')).join('');
  const expires_at = new Date(Date.now() + 7 * 86400000).toISOString();
  await env.DB.prepare('INSERT INTO test_share_links(token_hash,test_id,created_by,role,expires_at) VALUES(?1,?2,?3,?4,?5)').bind(await hash(token), Number(test_id), g.t.id, role, expires_at).run();
  return json({ token, expires_at });
}
export async function list(req, env) {
  const id = Number(new URL(req.url).searchParams.get('test_id'));
  const g = await needTest(req, env, id, 'own'); if (g.resp) return g.resp;
  await setup(env);
  const { results } = await env.DB.prepare('SELECT id,role,expires_at FROM test_share_links WHERE test_id=?1 AND used_by IS NULL AND revoked=0 AND expires_at>?2').bind(id, new Date().toISOString()).all();
  return json({ links: results });
}
export async function revoke(req, env, params) {
  const t = await authTeacher(req, env); if (!t) return err('Not logged in.', 401);
  await setup(env);
  const link = await env.DB.prepare('SELECT test_id FROM test_share_links WHERE id=?1').bind(Number(params.id)).first();
  if (!link) return err('Not found.', 404);
  const g = await needTest(req, env, link.test_id, 'own'); if (g.resp) return g.resp;
  await env.DB.prepare('UPDATE test_share_links SET revoked=1 WHERE id=?1').bind(Number(params.id)).run();
  return json({ ok: true });
}
async function load(env, token) {
  await setup(env);
  if (!/^[a-f0-9]{48}$/.test(token || '')) return null;
  return env.DB.prepare(`SELECT l.id,l.test_id,l.role,x.title,x.owner_id FROM test_share_links l
    JOIN tests x ON x.id=l.test_id AND x.owner_id=l.created_by
    JOIN teachers t ON t.id=l.created_by AND t.active=1
    WHERE l.token_hash=?1 AND l.revoked=0 AND l.used_by IS NULL AND l.expires_at>?2`)
    .bind(await hash(token), new Date().toISOString()).first();
}
export async function info(req, env, params) {
  const t = await authTeacher(req, env); if (!t) return err('Not logged in.', 401);
  const link = await load(env, params.token);
  return link ? json({ title: link.title, role: link.role }) : err('តំណបានប្រើរួច ផុតកំណត់ ឬត្រូវបានដកចេញ។', 404);
}
export async function accept(req, env, params) {
  const t = await authTeacher(req, env); if (!t) return err('Not logged in.', 401);
  const link = await load(env, params.token);
  if (!link) return err('តំណបានប្រើរួច ផុតកំណត់ ឬត្រូវបានដកចេញ។', 404);
  if (link.owner_id === t.id) return err('នេះជាតេស្តរបស់អ្នកផ្ទាល់។', 400);
  const now = new Date().toISOString();
  // Atomic grant and consume; only the first recipient can use the link.
  const result = await env.DB.batch([
    env.DB.prepare(`INSERT INTO shares(resource_type,resource_id,teacher_id,role)
      SELECT 'test',test_id,?1,role FROM test_share_links
      WHERE id=?2 AND used_by IS NULL AND revoked=0 AND expires_at>?3
      ON CONFLICT(resource_type,resource_id,teacher_id) DO UPDATE SET role=
        CASE WHEN shares.role='editor' THEN 'editor' ELSE excluded.role END`).bind(t.id, link.id, now),
    env.DB.prepare('UPDATE test_share_links SET used_by=?1 WHERE id=?2 AND used_by IS NULL AND revoked=0 AND expires_at>?3').bind(t.id, link.id, now),
  ]);
  if (!result[1].meta.changes) return err('តំណនេះត្រូវបានប្រើរួចហើយ។', 409);
  return json({ test_id: link.test_id });
}
