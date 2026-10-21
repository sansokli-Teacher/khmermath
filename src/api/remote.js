// Phone remote for the team game. The computer (projector) runs the game and publishes its state; a phone opened from a QR code / link
// shows a controller and sends commands back. Nothing needs a login on the phone: each room has two secret keys,
//   host key — held by the projector page: publishes the state, receives the commands
//   ctl key  — in the phone link: reads the state, sends commands
//   POST /api/remote/create   teacher — open a room                         -> { code, host, ctl }
//   POST /api/remote/sync     host    — { code, host, state?, ack }         -> { cmds, phone_at }
//   GET  /api/remote/state    phone   — ?c=CODE&k=CTL&seq=N                 -> { seq, state?, host_alive }
//   POST /api/remote/cmd      phone   — { code, k, c: { t, ... } }          -> { ok }
import { json, err } from '../lib/http.js';
import { authTeacher } from '../lib/access.js';

let ready = false;
export function _resetRemoteForTests() { ready = false; }
async function ensure(env) {
  if (ready) return;
  await env.DB.prepare(`CREATE TABLE IF NOT EXISTS remote_rooms (
    code TEXT PRIMARY KEY, host_key TEXT NOT NULL, ctl_key TEXT NOT NULL, owner_id INTEGER, state TEXT NOT NULL DEFAULT '', state_seq INTEGER NOT NULL DEFAULT 0,
    cmds TEXT NOT NULL DEFAULT '[]', cmd_seq INTEGER NOT NULL DEFAULT 0, host_at INTEGER NOT NULL DEFAULT 0, phone_at INTEGER NOT NULL DEFAULT 0, created_at INTEGER NOT NULL)`).run();
  ready = true;
}
const hex = (n) => Array.from(crypto.getRandomValues(new Uint8Array(n)), (b) => b.toString(16).padStart(2, '0')).join('');
const ALPHA = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
const newCode = () => Array.from(crypto.getRandomValues(new Uint8Array(6)), (b) => ALPHA[b % ALPHA.length]).join('');
const same = (a, b) => { a = String(a || ''); b = String(b || ''); if (a.length !== b.length || !a) return false; let d = 0; for (let i = 0; i < a.length; i++) d |= a.charCodeAt(i) ^ b.charCodeAt(i); return d === 0; };
const TTL = 12 * 3600 * 1000, MAX_STATE = 40000, MAX_CMDS = 40;
// what a phone may ask the game to do (every field is a small number)
const CMDS = new Set(['open', 'spin', 'go', 'show', 'ok', 'bad', 'other', 'pick', 'plus', 'sp', 'close', 'score', 'end']);

export async function create(req, env) {
  const t = await authTeacher(req, env); if (!t) return err('Not logged in.', 401);
  await ensure(env);
  const now = Date.now();
  await env.DB.prepare('DELETE FROM remote_rooms WHERE created_at < ?1').bind(now - TTL).run();
  await env.DB.prepare('DELETE FROM remote_rooms WHERE owner_id = ?1 AND code NOT IN (SELECT code FROM remote_rooms WHERE owner_id = ?1 ORDER BY created_at DESC LIMIT 4)').bind(t.id).run();
  for (let k = 0; k < 5; k++) {
    const code = newCode(), host = hex(16), ctl = hex(16);
    try {
      await env.DB.prepare('INSERT INTO remote_rooms (code, host_key, ctl_key, owner_id, created_at) VALUES (?1, ?2, ?3, ?4, ?5)').bind(code, host, ctl, t.id, now).run();
      return json({ code, host, ctl });
    } catch { /* code collision: try another */ }
  }
  return err('Could not open a room.', 500);
}

async function room(env, code) {
  await ensure(env);
  return env.DB.prepare('SELECT * FROM remote_rooms WHERE code = ?1').bind(String(code || '').toUpperCase().slice(0, 12)).first();
}

export async function sync(req, env) {
  const b = await req.json().catch(() => ({}));
  const r = await room(env, b.code);
  if (!r || !same(r.host_key, b.host)) return err('Unknown room.', 404);
  const now = Date.now(), ack = Number(b.ack) || 0;
  let cmds = []; try { cmds = JSON.parse(r.cmds); } catch { cmds = []; }
  const left = cmds.filter((c) => c.id > ack);
  const hasState = typeof b.state === 'string' && b.state.length > 0 && b.state.length <= MAX_STATE;
  await env.DB.prepare('UPDATE remote_rooms SET host_at = ?2, state = CASE WHEN ?3 = 1 THEN ?4 ELSE state END, state_seq = state_seq + ?3, cmds = ?5 WHERE code = ?1')
    .bind(r.code, now, hasState ? 1 : 0, hasState ? b.state : '', JSON.stringify(left)).run();
  return json({ cmds: left, phone_at: r.phone_at, seq: r.state_seq + (hasState ? 1 : 0) });
}

export async function state(req, env) {
  const u = new URL(req.url);
  const r = await room(env, u.searchParams.get('c'));
  if (!r || !same(r.ctl_key, u.searchParams.get('k'))) return err('Unknown room.', 404);
  const now = Date.now(), seq = Number(u.searchParams.get('seq')) || 0;
  if (now - r.phone_at > 3000) await env.DB.prepare('UPDATE remote_rooms SET phone_at = ?2 WHERE code = ?1').bind(r.code, now).run();
  const out = { seq: r.state_seq, host_alive: now - r.host_at < 7000 };
  if (seq !== r.state_seq && r.state) out.state = JSON.parse(r.state);
  return json(out, 200, { 'Cache-Control': 'no-store' });
}

export async function cmd(req, env) {
  const b = await req.json().catch(() => ({}));
  const r = await room(env, b.code);
  if (!r || !same(r.ctl_key, b.k)) return err('Unknown room.', 404);
  const c = b.c || {};
  if (!CMDS.has(c.t)) return err('Bad command.', 400);
  const clean = { t: c.t };
  for (const k of ['i', 'k', 'd']) if (c[k] !== undefined) { const n = Number(c[k]); if (!Number.isInteger(n) || Math.abs(n) > 1000) return err('Bad command.', 400); clean[k] = n; }
  let cmds = []; try { cmds = JSON.parse(r.cmds); } catch { cmds = []; }
  const id = r.cmd_seq + 1;
  cmds.push({ id, c: clean }); if (cmds.length > MAX_CMDS) cmds = cmds.slice(-MAX_CMDS);
  await env.DB.prepare('UPDATE remote_rooms SET cmds = ?2, cmd_seq = ?3 WHERE code = ?1').bind(r.code, JSON.stringify(cmds), id).run();
  return json({ ok: true, id });
}
