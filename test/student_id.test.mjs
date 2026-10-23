// A teacher can correct a student's ID: it must be free, and everything the student already has (results, ...) moves to the new ID.
import test from 'node:test';
import assert from 'node:assert/strict';
import { makeEnv } from './d1shim.mjs';
import * as classes from '../src/api/classes.js';
import { hashSecretValue } from '../src/lib/crypto.js';
import { createSessionCookie } from '../src/lib/session.js';
import { _resetSchemaForTests, ensureColumns } from '../src/lib/schema.js';

async function setup() {
  const env = makeEnv(new URL('../schema.sql', import.meta.url).pathname);
  env.SESSION_SECRET = 'test-secret-long-enough-for-encryption-123456';
  _resetSchemaForTests();
  await ensureColumns(env);
  env.raw.prepare("INSERT INTO teachers (username, password_hash, role, plan, active) VALUES ('boss', ?, 'owner', 'full', 1)").run(await hashSecretValue('pw123456', 'boss', env.SESSION_SECRET));
  env.raw.prepare("INSERT INTO classes (name, grade, owner_id) VALUES ('c', 9, 1)").run();
  env.raw.prepare("INSERT INTO students (id, class_id, surname, first_name) VALUES ('s1', 1, 'A', 'One'), ('s2', 1, 'B', 'Two')").run();
  env.raw.prepare("INSERT INTO tests (title, status, owner_id, is_bank, is_sample) VALUES ('t', 'draft', 1, 0, 0)").run();
  env.raw.prepare("INSERT INTO test_sessions (test_id, class_id, scheduled_start, duration_minutes, scheduled_end, pin) VALUES (1, 1, '2026-01-01T00:00:00Z', 60, '2026-01-01T01:00:00Z', '1')").run();
  env.raw.prepare("INSERT INTO results (session_id, student_id, mcq_score, mcq_max) VALUES (1, 's1', 5, 10)").run();
  return env;
}
const put = async (env, id, body) => {
  const ck = (await createSessionCookie({ role: 'teacher', username: 'boss' }, env.SESSION_SECRET)).split(';')[0];
  const r = await classes.updateStudent({ url: 'http://x/', headers: { get: (k) => (k.toLowerCase() === 'cookie' ? ck : null) }, async json() { return body; } }, env, { studentId: id });
  return { status: r.status, d: await r.json() };
};

test('changing a student ID moves the student and their results', async () => {
  const env = await setup();
  const r = await put(env, 's1', { id: '0109293', surname: 'A', first_name: 'One' });
  assert.equal(r.status, 200); assert.equal(r.d.id, '0109293');
  assert.equal(env.raw.prepare("SELECT COUNT(*) n FROM students WHERE id = 's1'").get().n, 0);
  assert.equal(env.raw.prepare("SELECT surname FROM students WHERE id = '0109293'").get().surname, 'A');
  assert.equal(env.raw.prepare("SELECT COUNT(*) n FROM results WHERE student_id = '0109293'").get().n, 1);
  assert.equal(env.raw.prepare("SELECT COUNT(*) n FROM results WHERE student_id = 's1'").get().n, 0);
});

test('an ID already used by another student is refused and nothing changes', async () => {
  const env = await setup();
  const r = await put(env, 's1', { id: 's2', surname: 'A', first_name: 'One' });
  assert.equal(r.status, 409);
  assert.equal(env.raw.prepare("SELECT COUNT(*) n FROM results WHERE student_id = 's1'").get().n, 1);
});

test('an ID with spaces is refused; the same ID just saves the other fields', async () => {
  const env = await setup();
  assert.equal((await put(env, 's1', { id: 'a b', surname: 'A', first_name: 'One' })).status, 400);
  const ok = await put(env, 's1', { id: 's1', surname: 'Z', first_name: 'One' });
  assert.equal(ok.status, 200);
  assert.equal(env.raw.prepare("SELECT surname FROM students WHERE id = 's1'").get().surname, 'Z');
});
