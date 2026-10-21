import test from 'node:test';
import assert from 'node:assert/strict';
import { makeEnv } from './d1shim.mjs';
import * as teacher from '../src/api/teacher.js';
import * as admin from '../src/api/admin.js';
import * as attendance from '../src/api/attendance.js';
import { hashSecretValue } from '../src/lib/crypto.js';
import { createSessionCookie } from '../src/lib/session.js';
import { _resetSchemaForTests, ensureColumns } from '../src/lib/schema.js';

async function setup() {
  const env = makeEnv(new URL('../schema.sql', import.meta.url).pathname);
  env.SESSION_SECRET = 'test-secret-long-enough-for-encryption-123456';
  _resetSchemaForTests();
  await ensureColumns(env);
  for (const [u, role] of [['boss', 'owner'], ['adm', 'admin'], ['tea', 'teacher']]) {
    env.raw.prepare("INSERT INTO teachers (username, password_hash, role, plan, active) VALUES (?, ?, ?, 'full', 1)")
      .run(u, await hashSecretValue('pw123456', u, env.SESSION_SECRET), role);
  }
  env.raw.prepare("INSERT INTO classes (name, grade, owner_id) VALUES ('c', 7, (SELECT id FROM teachers WHERE username = 'tea'))").run();
  return env;
}
const as = async (env, username, body = {}, url = 'http://x/') => {
  const ck = (await createSessionCookie({ role: 'teacher', username }, env.SESSION_SECRET)).split(';')[0];
  return { url, headers: { get: (k) => (k.toLowerCase() === 'cookie' ? ck : null) }, async json() { return body; } };
};
const me = async (env, u) => (await teacher.me(await as(env, u), env)).json();

test('teaching mode: owner and admin always, a teacher only once the owner allows it', async () => {
  const env = await setup();
  assert.equal((await me(env, 'boss')).teach_allowed, true);
  assert.equal((await me(env, 'adm')).teach_allowed, true);
  assert.equal((await me(env, 'tea')).teach_allowed, false);

  const tid = env.raw.prepare("SELECT id FROM teachers WHERE username = 'tea'").get().id;
  const denied = await admin.setTeachAccess(await as(env, 'tea', { allowed: true }), env, { id: tid });
  assert.equal(denied.status, 403);                                    // a teacher cannot grant themselves
  assert.equal((await me(env, 'tea')).teach_allowed, false);

  const ok = await admin.setTeachAccess(await as(env, 'boss', { allowed: true }), env, { id: tid });
  assert.equal(ok.status, 200);
  assert.equal((await me(env, 'tea')).teach_allowed, true);

  await admin.setTeachAccess(await as(env, 'boss', { allowed: false }), env, { id: tid });
  assert.equal((await me(env, 'tea')).teach_allowed, false);
});

test('attendance (teaching-mode data) is refused for a teacher without teaching mode', async () => {
  const env = await setup();
  const cid = env.raw.prepare('SELECT id FROM classes').get().id;
  const url = `http://x/api/attendance?class_id=${cid}&day=2026-10-20&period=1`;
  assert.equal((await attendance.getAttendance(await as(env, 'tea', {}, url), env)).status, 403);
  assert.equal((await attendance.saveAttendance(await as(env, 'tea', { class_id: cid, day: '2026-10-20', rows: [] }), env)).status, 403);
  assert.equal((await attendance.getAttendance(await as(env, 'boss', {}, url), env)).status, 200);
});

test('attendance keeps ten teaching periods a day apart (period 9 and 10 are not folded into 8)', async () => {
  const env = await setup();
  const cid = env.raw.prepare('SELECT id FROM classes').get().id;
  env.raw.prepare("INSERT INTO students (id, class_id, surname, first_name) VALUES ('s1', ?, 'A', 'One')").run(cid);
  const save = async (period, mark) => (await attendance.saveAttendance(await as(env, 'boss', { class_id: cid, day: '2026-10-20', period, rows: [{ student_id: 's1', mark }] }), env)).status;
  assert.equal(await save(8, 'ok'), 200); assert.equal(await save(9, 'L'), 200); assert.equal(await save(10, 'A'), 200);
  const get = async (period) => (await (await attendance.getAttendance(await as(env, 'boss', {}, `http://x/api/attendance?class_id=${cid}&day=2026-10-20&period=${period}`), env)).json());
  assert.equal((await get(8)).rows[0].mark, 'ok'); assert.equal((await get(9)).rows[0].mark, 'L'); assert.equal((await get(10)).rows[0].mark, 'A');
  assert.equal((await get(10)).period, 10);
  assert.equal((await get(99)).period, 10);                           // anything beyond the last period is the last period
});
