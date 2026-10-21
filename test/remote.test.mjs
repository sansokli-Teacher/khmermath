// The phone remote room logic (src/lib/remoteroom.js): state flows from the game to the phone, commands flow back, both over a live
// link (sockets) and over the HTTP polling fallback.
import test from 'node:test';
import assert from 'node:assert/strict';
import { RoomCore, validCmd } from '../src/lib/remoteroom.js';

function room() {
  const sock = { host: [], ctl: [] }, sent = [];
  let t = 100000;
  const core = new RoomCore({ count: (r) => sock[r].length, send: (r, m) => sent.push([r, m]) }, () => t);
  core.init('HK', 'CK');
  return { core, sock, sent, tick: (ms) => { t += ms; } };
}

test('keys: the phone key and the game key are different roles', () => {
  const { core } = room();
  assert.equal(core.role('HK'), 'host'); assert.equal(core.role('CK'), 'ctl'); assert.equal(core.role('x'), null); assert.equal(core.role(''), null);
  assert.equal(core.init('a', 'b'), false);          // a room is created once
});

test('over a live link: state goes to the phone at once, a command goes to the game at once and is acknowledged', () => {
  const { core, sock, sent } = room();
  sock.host.push(1); sock.ctl.push(1);
  core.setState(JSON.stringify({ turn: 1 }));
  assert.deepEqual(sent.pop(), ['ctl', { t: 'state', s: '{"turn":1}', seq: 1 }]);
  const r = core.cmd({ t: 'open', i: 3 });
  assert.equal(r.ok, true); assert.equal(r.delivered, true);
  assert.deepEqual(sent.pop(), ['host', { t: 'cmd', id: r.id, c: { t: 'open', i: 3 } }]);
  core.done(r.id);
  assert.deepEqual(sent.pop(), ['ctl', { t: 'ack', id: r.id }]);
  assert.deepEqual(core.m.cmds, []);                 // nothing queued: it was delivered
});

test('over HTTP polling: commands wait for the game page and are delivered once', () => {
  const { core, tick } = room();
  assert.equal(core.peek(0).host_alive, false);
  core.syncHost({ state: JSON.stringify({ a: 1 }), ack: 0 });
  const p = core.peek(0); assert.equal(p.host_alive, true); assert.deepEqual(p.state, { a: 1 });
  assert.equal(core.peek(p.seq).state, undefined);   // unchanged: not sent again
  const a = core.cmd({ t: 'open', i: 3 }), b = core.cmd({ t: 'ok' });
  assert.equal(a.delivered, true);                   // the game page polled a moment ago
  const s1 = core.syncHost({ ack: 0 });
  assert.deepEqual(s1.cmds.map((x) => x.c), [{ t: 'open', i: 3 }, { t: 'ok' }]);
  assert.deepEqual(core.syncHost({ ack: b.id }).cmds, []);
  tick(9000); assert.equal(core.hostOn(), false);    // the game page went quiet
  assert.equal(core.cmd({ t: 'ok' }).delivered, false);
});

test('a phone can only send the known commands with small numbers', () => {
  assert.equal(validCmd({ t: 'drop-table' }), null);
  assert.equal(validCmd({ t: 'open', i: 'x' }), null);
  assert.equal(validCmd({ t: 'open', i: 5000 }), null);
  assert.deepEqual(validCmd({ t: 'score', k: 1, d: -1, evil: 'x' }), { t: 'score', k: 1, d: -1 });
  assert.equal(room().core.cmd({ t: 'nope' }).ok, false);
});

test('presence is announced to the other side', () => {
  const { core, sock, sent } = room();
  sock.ctl.push(1); sock.host.push(1);
  core.hello('ctl');
  assert.deepEqual(sent.filter(([r, m]) => m.t === 'host' || m.t === 'phone').map(([r, m]) => [r, m.t, m.on]), [['ctl', 'host', true], ['host', 'phone', true]]);
});
