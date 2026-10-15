// End-to-end tests of the live quiz API on an in-memory database: solo mode, kick, avatar, homework, lock, history.
import test from 'node:test';
import assert from 'node:assert/strict';
import { makeEnv } from './d1shim.mjs';
import { ensureColumns, _resetSchemaForTests } from '../src/lib/schema.js';
import { createSessionCookie } from '../src/lib/session.js';
import * as live from '../src/api/live.js';
import * as game from '../src/api/game.js';

const bank = { class: 'g7', lessons: [{ n: 1, title: 'A', qs: Array.from({ length: 8 }, (_, i) => ({ t: 'x', q: `q${i}`, lv: 'easy', h: '', s: 'sol', a: `\\(${i + 10}\\)` })) }] };

async function setup() {
  const env = makeEnv(new URL('../schema.sql', import.meta.url).pathname);
  _resetSchemaForTests(); live._resetLiveForTests(); game._resetGameForTests(); game._forgetLock();
  await ensureColumns(env);
  env.SESSION_SECRET = 'test-secret';
  env.ASSETS = { fetch: async () => new Response(JSON.stringify(bank), { headers: { 'Content-Type': 'application/json' } }) };
  env.raw.exec(`INSERT INTO teachers (id, username, password_hash, role) VALUES (1, 'owner', 'x', 'owner')`);
  env.raw.exec(`INSERT INTO classes (id, name, grade, owner_id) VALUES (1, '7A', 7, 1)`);
  env.raw.exec(`INSERT INTO students (id, class_id, surname, first_name) VALUES ('s1', 1, 'A', 'One')`);
  const cookie = async (role, extra) => (await createSessionCookie({ role, ...extra }, env.SESSION_SECRET)).split(';')[0];
  env.tc = await cookie('teacher', { username: 'owner' });
  env.sc = await cookie('student', { id: 's1', name: 'A One', classId: 1 });
  return env;
}
const call = async (fn, env, { method = 'GET', url = 'http://x/api', body, cookie, params } = {}) => {
  const req = new Request(url, { method, headers: { ...(cookie ? { Cookie: cookie } : {}), 'Content-Type': 'application/json' }, body: body ? JSON.stringify(body) : undefined });
  const r = await fn(req, env, params || {});
  return { status: r.status, d: await r.json() };
};
const create = (env, extra = {}) => call(live.create, env, { method: 'POST', cookie: env.tc, body: { lessons: [1], count: 5, secs: 30, ...extra } });
const join = (env, code, name = 'Ann', avatar) => call(live.join, env, { method: 'POST', body: { code, name, avatar } });
const st = (env, c, p) => call(live.state, env, { url: `http://x/api?code=${c}&pid=${p.pid}&token=${p.token}` });
const host = (env, code, body) => call(live.hostAction, env, { method: 'POST', cookie: env.tc, body, params: { code } });

test('self-paced room: lobby first, the teacher starts it, each student plays alone, answers are graded on the server', async () => {
  const env = await setup();
  const { d: room } = await create(env, { mode: 'solo' });
  const a = (await join(env, room.code, 'Ann', '1-2-3-0-1')).d, b = (await join(env, room.code, 'Bob')).d;
  assert.equal((await st(env, room.code, a)).d.phase, 'lobby');
  assert.equal((await host(env, room.code, { a: 'start' })).status, 200);
  let s = (await st(env, room.code, a)).d;
  assert.equal(s.phase, 'question'); assert.equal(s.mode, 'solo'); assert.equal(s.q.k, 'mcq'); assert.equal(s.avatar, '1-2-3-0-1');
  assert.equal('correct' in s.q, false);                                       // phones never receive the answer
  // answering the wrong option scores nothing, then "next" moves on; the other student is unaffected
  const wrong = [0, 1, 2, 3].find((i) => String(i) !== '0');
  await call(live.answer, env, { method: 'POST', body: { code: room.code, pid: a.pid, token: a.token, qi: 0, choice: String(wrong) } });
  s = (await st(env, room.code, a)).d; assert.equal(s.phase, 'reveal');
  await call(live.next, env, { method: 'POST', body: { code: room.code, pid: a.pid, token: a.token } });
  assert.equal((await st(env, room.code, a)).d.qi, 1);
  assert.equal((await st(env, room.code, b)).d.qi, 0);
  // a wrong token cannot read or answer for someone else
  assert.equal((await st(env, room.code, { pid: a.pid, token: 'nope' })).status, 404);
});

test('the teacher can remove a student; the removed phone is told the room is gone', async () => {
  const env = await setup();
  const { d: room } = await create(env, { mode: 'solo' });
  const a = (await join(env, room.code, 'Ann')).d, b = (await join(env, room.code, 'Bob')).d;
  assert.equal((await host(env, room.code, { a: 'kick', pid: a.pid })).status, 200);
  assert.equal((await st(env, room.code, a)).status, 404);
  assert.equal((await st(env, room.code, b)).status, 200);
  const { d: h } = await call(live.hostState, env, { cookie: env.tc, params: { code: room.code } });
  assert.deepEqual(h.plist.map((p) => p.name), ['Bob']);
});

test('avatars: only valid codes are stored, and a student can change theirs', async () => {
  const env = await setup();
  const { d: room } = await create(env, { mode: 'solo' });
  const a = (await join(env, room.code, 'Ann', 'bad-code')).d;
  assert.equal((await st(env, room.code, a)).d.avatar, '');
  const set = (avatar) => call(live.setAvatar, env, { method: 'POST', body: { code: room.code, pid: a.pid, token: a.token, avatar } });
  assert.equal((await set('9-9-9-9-9')).status, 400);
  assert.equal((await set('5-4-5-3-3')).status, 200);
  assert.equal((await st(env, room.code, a)).d.avatar, '5-4-5-3-3');
});

test('40 students joining in the same instant all get a seat', async () => {
  const env = await setup();
  const { d: room } = await create(env, { mode: 'classic' });
  const rs = await Promise.all(Array.from({ length: 40 }, (_, i) => join(env, room.code, `P${i}`)));
  assert.ok(rs.every((r) => r.status === 200));
  assert.equal(new Set(rs.map((r) => r.d.pid)).size, 40);
});

test('exam-day lock closes the live quiz and the public bank', async () => {
  const env = await setup();
  const { d: room } = await create(env, { mode: 'classic' });
  env.raw.exec(`INSERT INTO settings (key, value) VALUES ('game_config', '{"locked":true}')`); game._forgetLock();
  assert.equal((await join(env, room.code)).status, 503);
  assert.equal((await create(env)).status, 403);
  const b = await game.bank(new Request('http://x/api/game/bank'), env);
  assert.equal(b.status, 503);
});

test('homework: only the class can join, once, and the result is kept in the history', async () => {
  const env = await setup();
  const hw = await create(env, { mode: 'solo', class_id: 1, deadline: Date.now() + 86400000 });
  assert.equal(hw.status, 200); assert.equal(hw.d.homework, true);
  assert.equal((await join(env, hw.d.code)).status, 403);                        // not through the public door
  const g = (await call(live.studentGames, env, { cookie: env.sc })).d.games; assert.equal(g.length, 1);
  const j1 = (await call(live.studentJoin, env, { method: 'POST', cookie: env.sc, body: { code: hw.d.code } })).d;
  const j2 = (await call(live.studentJoin, env, { method: 'POST', cookie: env.sc, body: { code: hw.d.code } })).d;
  assert.equal(j1.pid, j2.pid);
  for (let i = 0; i < 12; i++) {
    const s = (await st(env, hw.d.code, j1)).d;
    if (s.phase === 'end') break;
    if (s.phase === 'question') await call(live.answer, env, { method: 'POST', body: { code: hw.d.code, pid: j1.pid, token: j1.token, qi: s.qi, choice: '0' } });
    else await call(live.next, env, { method: 'POST', body: { code: hw.d.code, pid: j1.pid, token: j1.token } });
  }
  const det = (await call(live.historyDetail, env, { cookie: env.tc, params: { code: hw.d.code } })).d;
  assert.equal(det.players[0].student_id, 's1'); assert.equal(det.questions.length, 5);
  assert.ok(det.questions.every((q) => q.answered === 1));
  const hist = (await call(live.history, env, { cookie: env.tc })).d.rooms;
  assert.equal(hist[0].class_name, '7A'); assert.equal(hist[0].finished, 1);
  // after the deadline the student can no longer answer
  env.raw.exec(`UPDATE live_rooms SET deadline = ${Date.now() - 1000} WHERE code = '${hw.d.code}'`);
  assert.equal((await call(live.studentJoin, env, { method: 'POST', cookie: env.sc, body: { code: hw.d.code } })).status, 409);
});

test('a classroom shares one IP, but guessing room codes is limited', async () => {
  const env = await setup();
  const calls = [];
  for (let i = 0; i < 45; i++) calls.push((await join(env, '000000')).status);
  assert.ok(calls.includes(429)); assert.equal(calls[0], 404);
});

test('backup + restore bring back live-quiz history and question fixes', async () => {
  const { buildBackup } = await import('../src/lib/backup.js');
  const { planRestore, applyRestore } = await import('../src/lib/restore.js');
  const env = await setup();
  const { d: room } = await create(env, { mode: 'solo' });
  await join(env, room.code, 'Ann');
  env.raw.exec(`INSERT INTO game_edits (lesson, idx, bq, data, off) VALUES (1, 0, 'x', '{"q":"fixed"}', 0)`);
  const full = await buildBackup(env, { withImages: true }), slim = await buildBackup(env, { withImages: false });
  assert.equal(full.tables.live_rooms.length, 1); assert.equal(full.tables.live_players.length, 1); assert.equal(full.tables.live_qs.length, 5);
  assert.equal(full.tables.game_edits.length, 1);
  assert.equal(slim.tables.live_rooms, undefined);                       // the slim copy stays small
  assert.equal(slim.tables.game_edits.length, 1);
  env.raw.exec('DELETE FROM live_players; DELETE FROM live_qs; DELETE FROM live_rooms; DELETE FROM game_edits');
  const plan = await planRestore(env, full);
  assert.equal(plan.tables.find((t) => t.table === 'live_rooms').missing, 1);
  await applyRestore(env, full, { backupFirst: false });
  assert.equal(env.raw.prepare('SELECT COUNT(*) n FROM live_rooms').get().n, 1);
  assert.equal(env.raw.prepare('SELECT COUNT(*) n FROM live_players').get().n, 1);
  assert.equal(env.raw.prepare('SELECT COUNT(*) n FROM game_edits').get().n, 1);
});
