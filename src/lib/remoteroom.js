// The logic of one phone-remote room (a projector page + a phone controller), independent of the transport so it can be tested:
// the Durable Object (src/remote_do.js) feeds it WebSocket messages and HTTP polling requests alike.
//   host = the game page on the projector: publishes its state, receives the commands
//   ctl  = the phone: receives the state, sends commands
const MAX_STATE = 40000, MAX_CMDS = 40;
// what a phone may ask the game to do (every number is small)
const CMDS = new Set(['open', 'spin', 'go', 'show', 'ok', 'bad', 'other', 'pick', 'plus', 'sp', 'close', 'score', 'end']);
export function validCmd(c) {
  if (!c || !CMDS.has(c.t)) return null;
  const out = { t: c.t };
  for (const k of ['i', 'k', 'd']) if (c[k] !== undefined) { const n = Number(c[k]); if (!Number.isInteger(n) || Math.abs(n) > 1000) return null; out[k] = n; }
  return out;
}
export const same = (a, b) => { a = String(a || ''); b = String(b || ''); if (!a || a.length !== b.length) return false; let d = 0; for (let i = 0; i < a.length; i++) d |= a.charCodeAt(i) ^ b.charCodeAt(i); return d === 0; };

export class RoomCore {
  // io: { send(role, message), count(role) -> open sockets of that role }
  constructor(io, now = () => Date.now()) { this.io = io; this.now = now; this.m = null; }
  init(host, ctl) { if (this.m) return false; this.m = { host, ctl, state: '', seq: 0, cmds: [], cmdSeq: 0, hostAt: 0, phoneAt: 0 }; return true; }
  role(key) { if (!this.m) return null; return same(this.m.host, key) ? 'host' : same(this.m.ctl, key) ? 'ctl' : null; }
  hostOn() { return this.io.count('host') > 0 || this.now() - this.m.hostAt < 4000; }
  phoneOn() { return this.io.count('ctl') > 0 || this.now() - this.m.phoneAt < 4000; }
  presence() { this.io.send('ctl', { t: 'host', on: this.hostOn() }); this.io.send('host', { t: 'phone', on: this.phoneOn() }); }
  setState(s) {
    if (typeof s !== 'string' || !s || s.length > MAX_STATE) return false;
    this.m.state = s; this.m.seq++; this.io.send('ctl', { t: 'state', s, seq: this.m.seq });
    return true;
  }
  // a phone command: straight to the game page when it is on a live connection, otherwise queued for its next poll
  cmd(c) {
    const k = validCmd(c); if (!k) return { ok: false };
    const id = ++this.m.cmdSeq, live = this.io.count('host') > 0;
    if (live) this.io.send('host', { t: 'cmd', id, c: k });
    else { this.m.cmds.push({ id, c: k }); if (this.m.cmds.length > MAX_CMDS) this.m.cmds = this.m.cmds.slice(-MAX_CMDS); }
    return { ok: true, id, delivered: live || this.hostOn() };
  }
  done(id) { this.io.send('ctl', { t: 'ack', id: Number(id) || 0 }); }
  hello(role) {   // a socket just connected
    if (role === 'ctl') { if (this.m.state) this.io.send('ctl', { t: 'state', s: this.m.state, seq: this.m.seq }); }
    this.presence();
  }
  // ---- HTTP polling fallback ----
  syncHost({ state, ack }) {
    this.m.hostAt = this.now();
    if (state) this.setState(state);
    ack = Number(ack) || 0; this.m.cmds = this.m.cmds.filter((c) => c.id > ack);
    return { cmds: this.m.cmds, phone_on: this.phoneOn(), seq: this.m.seq };
  }
  peek(seq) {
    this.m.phoneAt = this.now();
    const out = { seq: this.m.seq, host_alive: this.hostOn() };
    if (Number(seq) !== this.m.seq && this.m.state) out.state = JSON.parse(this.m.state);
    return out;
  }
}
