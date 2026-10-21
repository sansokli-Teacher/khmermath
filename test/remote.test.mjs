// The phone remote relay: a teacher opens a room, the game page (host key) publishes its state and gets the phone's commands, the phone (ctl key) reads the state.
import test from 'node:test';
import assert from 'node:assert/strict';
import { makeEnv } from './d1shim.mjs';
import { ensureColumns, _resetSchemaForTests } from '../src/lib/schema.js';
import { createSessionCookie } from '../src/lib/session.js';
import * as remote from '../src/api/remote.js';

async function setup() {
  const env = makeEnv(new URL('../schema.sql', import.meta.url).pathname);
  _resetSchemaForTests(); remote._resetRemoteForTests();
  await ensureColumns(env);
  env.SESSION_SECRET = 'test-secret';
  env.raw.exec(`INSERT INTO teachers (id, username, password_hash, role) VALUES (1, 'owner', 'x', 'owner')`);
  env.tc = (await createSessionCookie({ role: 'teacher', username: 'owner' }, env.SESSION_SECRET)).split(';')[0];
  return env;
}
const call = async (fn, env, { method = 'GET', url = 'http://x/api', body, cookie } = {}) => {
  const req = new Request(url, { method, headers: { ...(cookie ? { Cookie: cookie } : {}), 'Content-Type': 'application/json' }, body: body ? JSON.stringify(body) : undefined });
  const r = await fn(req, env, {});
  return { status: r.status, d: await r.json() };
};

test('only a logged-in teacher can open a room; the phone link and the game page use different keys', async () => {
  const env = await setup();
  assert.equal((await call(remote.create, env, { method: 'POST' })).status, 401);
  const { d } = await call(remote.create, env, { method: 'POST', cookie: env.tc });
  assert.match(d.code, /^[A-Z0-9]{6}$/); assert.notEqual(d.host, d.ctl);
  // the phone key cannot publish, the game key cannot be used as a phone
  assert.equal((await call(remote.sync, env, { method: 'POST', body: { code: d.code, host: d.ctl } })).status, 404);
  assert.equal((await call(remote.state, env, { url: `http://x/api?c=${d.code}&k=${d.host}` })).status, 404);
});

test('state flows from the game to the phone and commands flow back, each delivered once', async () => {
  const env = await setup();
  const { d: room } = await call(remote.create, env, { method: 'POST', cookie: env.tc });
  const phone = (seq = 0) => call(remote.state, env, { url: `http://x/api?c=${room.code}&k=${room.ctl}&seq=${seq}` });
  assert.equal((await phone()).d.host_alive, false);                                   // nothing published yet
  const s1 = await call(remote.sync, env, { method: 'POST', body: { code: room.code, host: room.host, state: JSON.stringify({ turn: 1 }), ack: 0 } });
  assert.deepEqual(s1.d.cmds, []);
  const p1 = (await phone()).d;
  assert.equal(p1.host_alive, true); assert.deepEqual(p1.state, { turn: 1 });
  assert.equal((await phone(p1.seq)).d.state, undefined);                              // unchanged: no state sent again
  const c1 = await call(remote.cmd, env, { method: 'POST', body: { code: room.code, k: room.ctl, c: { t: 'open', i: 3 } } });
  await call(remote.cmd, env, { method: 'POST', body: { code: room.code, k: room.ctl, c: { t: 'ok' } } });
  const s2 = await call(remote.sync, env, { method: 'POST', body: { code: room.code, host: room.host, ack: 0 } });
  assert.deepEqual(s2.d.cmds.map((x) => x.c), [{ t: 'open', i: 3 }, { t: 'ok' }]);
  assert.ok(s2.d.cmds[0].id === c1.d.id);
  const s3 = await call(remote.sync, env, { method: 'POST', body: { code: room.code, host: room.host, ack: s2.d.cmds[1].id } });
  assert.deepEqual(s3.d.cmds, []);                                                     // acknowledged commands are not delivered twice
  assert.ok((await call(remote.sync, env, { method: 'POST', body: { code: room.code, host: room.host, ack: 0 } })).d.phone_at > 0);
});

test('a phone can only send the known commands with small numbers', async () => {
  const env = await setup();
  const { d: room } = await call(remote.create, env, { method: 'POST', cookie: env.tc });
  const send = (c) => call(remote.cmd, env, { method: 'POST', body: { code: room.code, k: room.ctl, c } });
  assert.equal((await send({ t: 'drop-table' })).status, 400);
  assert.equal((await send({ t: 'open', i: 'x' })).status, 400);
  assert.equal((await send({ t: 'score', k: 1, d: 1 })).status, 200);
  assert.equal((await call(remote.cmd, env, { method: 'POST', body: { code: room.code, k: 'wrong', c: { t: 'ok' } } })).status, 404);
});
