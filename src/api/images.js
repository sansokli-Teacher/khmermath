import { json, err } from '../lib/http.js';
import { requireTeacher } from '../lib/session.js';
import { randomKey } from '../lib/crypto.js';

const EXT_BY_TYPE = {
  'image/png': 'png',
  'image/jpeg': 'jpg',
  'image/webp': 'webp',
  'image/svg+xml': 'svg',
};

// Teacher uploads a question image (a geometry diagram, etc). The body is the
// raw image bytes; Content-Type says what it is.
export async function upload(req, env) {
  if (!(await requireTeacher(req, env))) return err('Not logged in.', 401);
  const contentType = req.headers.get('Content-Type') || '';
  const ext = EXT_BY_TYPE[contentType];
  if (!ext) return err('Unsupported image type — use PNG, JPEG, WEBP, or SVG.', 400);
  const key = `${randomKey()}.${ext}`;
  await env.IMAGES.put(key, req.body, { httpMetadata: { contentType } });
  return json({ key });
}

// Serving is unauthenticated: question diagrams are not sensitive, and students
// need to load them while taking a test.
export async function serve(req, env, params) {
  const object = await env.IMAGES.get(params.key);
  if (!object) return err('Image not found.', 404);
  return new Response(object.body, {
    headers: {
      'Content-Type': object.httpMetadata?.contentType || 'application/octet-stream',
      'Cache-Control': 'public, max-age=31536000, immutable',
    },
  });
}
