// Phone remote for the team game. The computer (projector) runs the game and publishes its state; a phone opened from a QR code / link
// shows a controller and sends commands back. Every room is one Durable Object (src/remote_do.js); nothing needs a login on the phone:
// each room has two secret keys,
//   host key — held by the projector page: publishes the state, receives the commands
//   ctl key  — in the phone link: reads the state, sends commands
//   POST /api/remote/create          teacher — open a room                       -> { code, host, ctl }
//   GET  /api/remote/ws?c=&k=        WebSocket (host or phone, by key)           (live link, instant)
//   POST /api/remote/sync            host    — { code, host, state?, ack }       -> { cmds, phone_on }   (polling fallback)
//   GET  /api/remote/state?c=&k=&seq phone                                       -> { seq, state?, host_alive }   (polling fallback)
//   POST /api/remote/cmd             phone   — { code, k, c: { t, ... } }        -> { ok, id }           (polling fallback)
import { json, err } from '../lib/http.js';
import { authTeacher } from '../lib/access.js';

const hex = (n) => Array.from(crypto.getRandomValues(new Uint8Array(n)), (b) => b.toString(16).padStart(2, '0')).join('');
const ALPHA = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
const newCode = () => Array.from(crypto.getRandomValues(new Uint8Array(6)), (b) => ALPHA[b % ALPHA.length]).join('');
const stub = (env, code) => env.REMOTE.get(env.REMOTE.idFromName(String(code || '').toUpperCase().slice(0, 12)));
const to = (env, code, path, req, body) => stub(env, code).fetch(new Request(`https://room${path}`, body === undefined ? req : { method: 'POST', headers: { 'Content-Type': 'application/json' }, body }));

export async function create(req, env) {
  const t = await authTeacher(req, env); if (!t) return err('Not logged in.', 401);
  if (!env.REMOTE) return err('Phone remote is not available on this server.', 503);
  for (let k = 0; k < 5; k++) {
    const code = newCode(), host = hex(16), ctl = hex(16);
    const r = await to(env, code, '/init', req, JSON.stringify({ host, ctl }));
    if (r.ok) return json({ code, host, ctl });
  }
  return err('Could not open a room.', 500);
}

export async function ws(req, env) {
  const u = new URL(req.url);
  if (!env.REMOTE) return err('Phone remote is not available on this server.', 503);
  return to(env, u.searchParams.get('c'), `/ws?k=${encodeURIComponent(u.searchParams.get('k') || '')}`, req);
}
export async function sync(req, env) {
  const b = await req.json().catch(() => ({}));
  return to(env, b.code, '/sync', req, JSON.stringify(b));
}
export async function state(req, env) {
  const u = new URL(req.url);
  return to(env, u.searchParams.get('c'), `/state?k=${encodeURIComponent(u.searchParams.get('k') || '')}&seq=${encodeURIComponent(u.searchParams.get('seq') || '0')}`, req);
}
export async function cmd(req, env) {
  const b = await req.json().catch(() => ({}));
  return to(env, b.code, '/cmd', req, JSON.stringify(b));
}
