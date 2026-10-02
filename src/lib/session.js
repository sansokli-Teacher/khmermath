// Signed session cookies (HMAC-SHA256), no external JWT library.
// Teacher and student each get their own cookie name so a teacher previewing
// the student view in another tab of the same browser doesn't log themselves
// out of the dashboard (and vice versa).
import { timingSafeEqual } from './crypto.js';

const COOKIE_NAMES = { teacher: 'exam_teacher', student: 'exam_student' };
const MAX_AGE_SECONDS = 60 * 60 * 12; // 12h — long enough to cover a 2h test plus setup time

function toBase64Url(bytes) {
  let bin = '';
  for (const b of bytes) bin += String.fromCharCode(b);
  return btoa(bin).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

function fromBase64Url(str) {
  const padded = str.replace(/-/g, '+').replace(/_/g, '/');
  const bin = atob(padded + '='.repeat((4 - (padded.length % 4)) % 4));
  const bytes = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
  return bytes;
}

async function hmac(secret, message) {
  const key = await crypto.subtle.importKey(
    'raw', new TextEncoder().encode(secret), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign'],
  );
  const sig = await crypto.subtle.sign('HMAC', key, new TextEncoder().encode(message));
  return toBase64Url(new Uint8Array(sig));
}

export async function createSessionCookie(payload, secret) {
  const name = COOKIE_NAMES[payload.role];
  const body = toBase64Url(new TextEncoder().encode(JSON.stringify({ ...payload, exp: Date.now() + MAX_AGE_SECONDS * 1000 })));
  const sig = await hmac(secret, body);
  return `${name}=${body}.${sig}; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=${MAX_AGE_SECONDS}`;
}

export function clearSessionCookie(role) {
  return `${COOKIE_NAMES[role]}=; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=0`;
}

function readCookie(req, name) {
  const header = req.headers.get('Cookie') || '';
  const match = header.split(';').map((p) => p.trim()).find((p) => p.startsWith(`${name}=`));
  return match ? match.slice(name.length + 1) : null;
}

async function getSessionFor(req, role, secret) {
  const token = readCookie(req, COOKIE_NAMES[role]);
  if (!token) return null;
  const [body, sig] = token.split('.');
  if (!body || !sig) return null;
  const expected = await hmac(secret, body);
  if (!timingSafeEqual(sig, expected)) return null;
  try {
    const payload = JSON.parse(new TextDecoder().decode(fromBase64Url(body)));
    if (!payload.exp || Date.now() > payload.exp || payload.role !== role) return null;
    return payload;
  } catch {
    return null;
  }
}

export async function requireTeacher(req, env) {
  return getSessionFor(req, 'teacher', env.SESSION_SECRET);
}

export async function requireStudent(req, env) {
  return getSessionFor(req, 'student', env.SESSION_SECRET);
}
