import { json, err } from '../lib/http.js';
import { requireTeacher } from '../lib/session.js';
import { randomKey } from '../lib/crypto.js';

const EXT_BY_TYPE = {
  'image/png': 'png',
  'image/jpeg': 'jpg',
  'image/webp': 'webp',
  'image/svg+xml': 'svg',
};

function bytesToBase64(bytes) {
  let bin = '';
  const chunkSize = 0x8000;
  for (let i = 0; i < bytes.length; i += chunkSize) bin += String.fromCharCode(...bytes.subarray(i, i + chunkSize));
  return btoa(bin);
}

function base64ToBytes(b64) {
  const bin = atob(b64);
  const bytes = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
  return bytes;
}

// Images are small question diagrams (a handful per test), stored directly in
// D1 as base64 — simpler than an R2 bucket and well within D1's free tier at
// this scale, and avoids the one-time "enable R2" step in the Cloudflare
// dashboard that isn't done on this account yet.
export async function upload(req, env) {
  if (!(await requireTeacher(req, env))) return err('Not logged in.', 401);
  const contentType = req.headers.get('Content-Type') || '';
  const ext = EXT_BY_TYPE[contentType];
  if (!ext) return err('Unsupported image type — use PNG, JPEG, WEBP, or SVG.', 400);
  const bytes = new Uint8Array(await req.arrayBuffer());
  const key = `${randomKey()}.${ext}`;
  await env.DB.prepare('INSERT INTO images (key, content_type, data_base64) VALUES (?1, ?2, ?3)')
    .bind(key, contentType, bytesToBase64(bytes)).run();
  return json({ key });
}

// Serving is unauthenticated: question diagrams are not sensitive, and students
// need to load them while taking a test.
export async function serve(req, env, params) {
  const row = await env.DB.prepare('SELECT content_type, data_base64 FROM images WHERE key = ?1').bind(params.key).first();
  if (!row) return err('Image not found.', 404);
  return new Response(base64ToBytes(row.data_base64), {
    headers: { 'Content-Type': row.content_type, 'Cache-Control': 'public, max-age=31536000, immutable' },
  });
}
