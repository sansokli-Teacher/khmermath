// The 10-minute watch: a backup right before an exam, and one alert (not a flood) when the server starts failing.
import test from 'node:test';
import assert from 'node:assert/strict';
import { makeEnv } from './d1shim.mjs';
import { ensureColumns, _resetSchemaForTests } from '../src/lib/schema.js';
import { watch, logError } from '../src/lib/watch.js';

async function setup() {
  const env = makeEnv(new URL('../schema.sql', import.meta.url).pathname);
  env.SESSION_SECRET = 'test-secret-long-enough-for-encryption-123456';
  _resetSchemaForTests(); await ensureColumns(env);
  env.raw.prepare("INSERT INTO teachers (username, password_hash, role) VALUES ('boss', 'x', 'owner')").run();
  env.raw.prepare("INSERT INTO classes (name, grade, owner_id) VALUES ('c', 9, 1)").run();
  env.raw.prepare("INSERT INTO tests (title, status, owner_id, is_bank, is_sample) VALUES ('t', 'draft', 1, 0, 0)").run();
  return env;
}

test('an exam starting in 20 minutes gets its own backup, once', async () => {
  const env = await setup();
  env.raw.prepare("INSERT INTO test_sessions (test_id, class_id, scheduled_start, duration_minutes, pin) VALUES (1, 1, ?, 60, '1')").run(new Date(Date.now() + 20 * 60000).toISOString());
  const a = await watch(env), b = await watch(env);
  assert.deepEqual(a.backups, [1]); assert.deepEqual(b.backups, []);
  assert.equal(env.raw.prepare("SELECT COUNT(*) c FROM backups WHERE reason = 'pre-exam 1'").get().c, 1);
});

test('an exam that is a day away is left alone', async () => {
  const env = await setup();
  env.raw.prepare("INSERT INTO test_sessions (test_id, class_id, scheduled_start, duration_minutes, pin) VALUES (1, 1, ?, 60, '1')").run(new Date(Date.now() + 24 * 3600000).toISOString());
  assert.deepEqual((await watch(env)).backups, []);
});

test('ten server errors in ten minutes raise one alert, then stay quiet for half an hour', async () => {
  const env = await setup();
  for (let i = 0; i < 10; i++) await logError(env, '/api/student/answer', 500, 'D1 error');
  assert.equal((await watch(env)).alert, true);
  assert.equal((await watch(env)).alert, false);
});
