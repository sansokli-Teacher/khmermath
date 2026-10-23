import { json, err } from '../lib/http.js';
import { needStudent } from '../lib/access.js';
import { ensureColumns } from '../lib/schema.js';

// Student photos are personal data of children: they are kept in their own table, are never public, and only a
// signed-in teacher who may see that student's class can read one. The browser sends a small JPEG (about 300 px).
const MAX_BYTES = 250 * 1024;
const TYPES = new Set(['image/jpeg', 'image/png', 'image/webp']);

function bytesToBase64(bytes) {
  let bin = '';
  for (let i = 0; i < bytes.length; i += 0x8000) bin += String.fromCharCode(...bytes.subarray(i, i + 0x8000));
  return btoa(bin);
}
function base64ToBytes(b64) {
  const bin = atob(b64); const out = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
  return out;
}

export async function uploadPhoto(req, env, params) {
  await ensureColumns(env);
  const g = await needStudent(req, env, params.studentId, 'edit'); if (g.resp) return g.resp;
  const type = (req.headers.get('Content-Type') || '').split(';')[0].trim();
  if (!TYPES.has(type)) return err('Use a JPEG, PNG or WEBP picture.', 400);
  const bytes = new Uint8Array(await req.arrayBuffer());
  if (!bytes.length) return err('The picture is empty.', 400);
  if (bytes.length > MAX_BYTES) return err('The picture is too large (over 250 KB) — the page shrinks it first; try another picture.', 413);
  const v = Date.now();
  await env.DB.prepare(
    `INSERT INTO student_photos (student_id, content_type, data_base64, updated_at) VALUES (?1, ?2, ?3, ?4)
     ON CONFLICT(student_id) DO UPDATE SET content_type = excluded.content_type, data_base64 = excluded.data_base64, updated_at = excluded.updated_at`,
  ).bind(String(params.studentId), type, bytesToBase64(bytes), v).run();
  return json({ ok: true, v });
}

export async function servePhoto(req, env, params) {
  await ensureColumns(env);
  const g = await needStudent(req, env, params.studentId, 'view'); if (g.resp) return g.resp;
  const row = await env.DB.prepare('SELECT content_type, data_base64 FROM student_photos WHERE student_id = ?1').bind(String(params.studentId)).first();
  if (!row) return err('No photo.', 404);
  return new Response(base64ToBytes(row.data_base64), { headers: { 'Content-Type': row.content_type, 'Cache-Control': 'private, max-age=86400' } });   // the page adds ?v= so a new picture is fetched at once
}

export async function deletePhoto(req, env, params) {
  await ensureColumns(env);
  const g = await needStudent(req, env, params.studentId, 'edit'); if (g.resp) return g.resp;
  await env.DB.prepare('DELETE FROM student_photos WHERE student_id = ?1').bind(String(params.studentId)).run();
  return json({ ok: true });
}
