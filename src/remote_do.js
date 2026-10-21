// One Durable Object per phone-remote room (see src/lib/remoteroom.js for the logic and src/api/remote.js for the routes).
// WebSockets (hibernating) give an instant link between the projector page and the phone; plain HTTP requests are accepted too, for
// networks that block WebSockets.
import { RoomCore } from './lib/remoteroom.js';

const TTL = 12 * 3600 * 1000;
const J = (d, status = 200) => new Response(JSON.stringify(d), { status, headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' } });

export class RemoteRoom {
  constructor(ctx, env) {
    this.ctx = ctx; this.env = env;
    this.core = new RoomCore({
      count: (role) => this.ctx.getWebSockets(role).filter((w) => w !== this.closing).length,
      send: (role, msg) => { const s = JSON.stringify(msg); for (const ws of this.ctx.getWebSockets(role)) { try { ws.send(s); } catch { /* closed */ } } },
    });
    try { this.ctx.setWebSocketAutoResponse(new WebSocketRequestResponsePair('ping', 'pong')); } catch { /* not available */ }
    this.ready = this.ctx.blockConcurrencyWhile(async () => { const m = await this.ctx.storage.get('m'); if (m) this.core.m = m; });
  }
  async save() { const m = { ...this.core.m, state: '', cmds: [] }; await this.ctx.storage.put('m', m); }   // keys only: state and queue are rebuilt by the game page

  async fetch(req) {
    await this.ready;
    const u = new URL(req.url), p = u.pathname;
    if (p === '/init') {
      const b = await req.json();
      if (!this.core.init(b.host, b.ctl)) return J({ error: 'exists' }, 409);
      await this.save(); await this.ctx.storage.setAlarm(Date.now() + TTL);
      return J({ ok: true });
    }
    if (!this.core.m) return J({ error: 'Unknown room.' }, 404);
    if (p === '/ws') {
      if (req.headers.get('Upgrade') !== 'websocket') return J({ error: 'Expected a WebSocket.' }, 426);
      const role = this.core.role(u.searchParams.get('k'));
      if (!role) return J({ error: 'Unknown room.' }, 404);
      const pair = new WebSocketPair();
      this.ctx.acceptWebSocket(pair[1], [role]);
      this.core.hello(role);
      return new Response(null, { status: 101, webSocket: pair[0] });
    }
    if (p === '/sync' && req.method === 'POST') {
      const b = await req.json().catch(() => ({}));
      if (this.core.role(b.host) !== 'host') return J({ error: 'Unknown room.' }, 404);
      const first = !this.core.m.hostAt, out = this.core.syncHost(b);
      if (first) this.core.presence();            // the game page just appeared (over HTTP): tell the phone
      return J(out);
    }
    if (p === '/state') {
      if (this.core.role(u.searchParams.get('k')) !== 'ctl') return J({ error: 'Unknown room.' }, 404);
      const was = this.core.phoneOn(), out = this.core.peek(u.searchParams.get('seq'));
      if (!was) this.core.presence();               // the phone just appeared (over HTTP): tell the game page
      return J(out);
    }
    if (p === '/cmd' && req.method === 'POST') {
      const b = await req.json().catch(() => ({}));
      if (this.core.role(b.k) !== 'ctl') return J({ error: 'Unknown room.' }, 404);
      const r = this.core.cmd(b.c);
      return r.ok ? J(r) : J({ error: 'Bad command.' }, 400);
    }
    return J({ error: 'Not found.' }, 404);
  }

  async webSocketMessage(ws, data) {
    await this.ready;
    let m; try { m = JSON.parse(data); } catch { return; }
    const role = this.ctx.getTags(ws)[0];
    if (role === 'host') {
      if (m.t === 'state') this.core.setState(m.s);
      else if (m.t === 'done') this.core.done(m.id);
    } else if (role === 'ctl') {
      if (m.t === 'cmd') {
        const r = this.core.cmd(m.c);
        try { ws.send(JSON.stringify({ t: 'sent', cid: m.cid, ok: r.ok, id: r.id, delivered: r.delivered })); } catch { /* closed */ }
      }
    }
  }
  async webSocketClose(ws) { this.closing = ws; try { ws.close(); } catch { /* already closed */ } this.core.presence(); this.closing = null; }
  async webSocketError(ws) { this.closing = ws; this.core.presence(); this.closing = null; }
  async alarm() {
    for (const ws of this.ctx.getWebSockets()) { try { ws.close(1000, 'expired'); } catch { /* closed */ } }
    await this.ctx.storage.deleteAll(); this.core.m = null;
  }
}
