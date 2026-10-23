// The lesson typed at the head of a period is stored per class + day + period and comes back with the attendance.
import test from 'node:test';
import assert from 'node:assert/strict';
import { makeEnv } from './d1shim.mjs';
import * as att from '../src/api/attendance.js';
import { hashSecretValue } from '../src/lib/crypto.js';
import { createSessionCookie } from '../src/lib/session.js';
import { _resetSchemaForTests, ensureColumns } from '../src/lib/schema.js';

async function setup() {
  const env = makeEnv(new URL('../schema.sql', import.meta.url).pathname);
  env.SESSION_SECRET = 'test-secret-long-enough-for-encryption-123456';
  _resetSchemaForTests();
  await ensureColumns(env);
  env.raw.prepare("INSERT INTO teachers (username, password_hash, role, plan, active) VALUES ('boss', ?, 'owner', 'full', 1)").run(await hashSecretValue('pw123456', 'boss', env.SESSION_SECRET));
  env.raw.prepare("INSERT INTO classes (name, grade, owner_id) VALUES ('7NGS-B', 7, 1)").run();
  env.raw.prepare("INSERT INTO students (id, class_id, surname, first_name) VALUES ('s1', 1, 'A', 'One')").run();
  return env;
}
const call = async (fn, env, { body, query } = {}) => {
  const ck = (await createSessionCookie({ role: 'teacher', username: 'boss' }, env.SESSION_SECRET)).split(';')[0];
  const r = await fn({ url: 'http://x/?' + new URLSearchParams(query || {}), headers: { get: (k) => (k.toLowerCase() === 'cookie' ? ck : null) }, async json() { return body; } }, env, {});
  return { status: r.status, d: await r.json() };
};

test('subject and lesson of a period are saved, overwritten and read back with the attendance', async () => {
  const env = await setup();
  const q = { class_id: 1, day: '2026-10-23', period: 3 };
  assert.deepEqual((await call(att.getAttendance, env, { query: q })).d.info, { subject: null, topic: null });
  assert.equal((await call(att.saveAttendanceInfo, env, { body: { ...q, subject: 'គណិតវិទ្យា', topic: 'ចំនួនគត់' } })).status, 200);
  assert.equal((await call(att.saveAttendanceInfo, env, { body: { ...q, subject: 'គណិតវិទ្យា', topic: 'ប្រភាគ' } })).status, 200);
  assert.deepEqual((await call(att.getAttendance, env, { query: q })).d.info, { subject: 'គណិតវិទ្យា', topic: 'ប្រភាគ' });
  assert.deepEqual((await call(att.getAttendance, env, { query: { ...q, period: 4 } })).d.info, { subject: null, topic: null });   // another period is untouched
  assert.equal((await call(att.saveAttendanceInfo, env, { body: { class_id: 1, day: 'bad', period: 1 } })).status, 400);
});

test('the day view lists each recorded period with its lesson, absent and late students', async () => {
  const env = await setup();
  env.raw.prepare("INSERT INTO students (id, class_id, surname, first_name) VALUES ('s2', 1, 'B', 'Two'), ('s3', 1, 'C', 'Three')").run();
  const ins = env.raw.prepare("INSERT INTO attendance (class_id, day, period, student_id, mark) VALUES (1, '2026-10-22', ?, ?, ?)");
  ins.run(1, 's1', 'ok'); ins.run(1, 's2', 'A'); ins.run(1, 's3', 'L'); ins.run(3, 's1', 'A'); ins.run(3, 's2', 'ok');
  await call(att.saveAttendanceInfo, env, { body: { class_id: 1, day: '2026-10-22', period: 5, subject: 'គណិតវិទ្យា', topic: 'ប្រភាគ' } });   // a lesson typed, attendance not taken yet
  const d = (await call(att.getAttendanceDay, env, { query: { class_id: 1, day: '2026-10-22' } })).d;
  assert.deepEqual(d.periods.map((p) => p.period), [1, 3, 5]);
  assert.deepEqual(d.periods[0].absent, ['B Two']); assert.deepEqual(d.periods[0].late, ['C Three']); assert.equal(d.periods[0].present, 1);
  assert.equal(d.periods[1].absent[0], 'A One');
  assert.equal(d.periods[2].recorded, false); assert.equal(d.periods[2].topic, 'ប្រភាគ');
  assert.deepEqual((await call(att.getAttendanceDay, env, { query: { class_id: 1, day: '2026-10-21' } })).d.periods, []);
});
