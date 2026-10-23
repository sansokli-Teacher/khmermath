// Test editor: drag-and-drop order, and setting many scores at once.
import test from 'node:test';
import assert from 'node:assert/strict';
import { makeEnv } from './d1shim.mjs';
import * as tests from '../src/api/tests.js';
import { hashSecretValue } from '../src/lib/crypto.js';
import { createSessionCookie } from '../src/lib/session.js';
import { _resetSchemaForTests, ensureColumns } from '../src/lib/schema.js';

async function setup() {
  const env = makeEnv(new URL('../schema.sql', import.meta.url).pathname);
  env.SESSION_SECRET = 'test-secret-long-enough-for-encryption-123456';
  _resetSchemaForTests();
  await ensureColumns(env);
  env.raw.prepare("INSERT INTO teachers (username, password_hash, role, plan, active) VALUES ('boss', ?, 'owner', 'full', 1)").run(await hashSecretValue('pw123456', 'boss', env.SESSION_SECRET));
  env.raw.prepare("INSERT INTO tests (title, status, owner_id, is_bank, is_sample) VALUES ('t', 'draft', 1, 0, 0)").run();
  for (let i = 1; i <= 3; i++) env.raw.prepare("INSERT INTO test_questions (test_id, order_no, stem_text, options_json, correct_index, points) VALUES (1, ?, ?, '[\"a\",\"b\"]', 0, 1)").run(i, 'q' + i);
  return env;
}
const call = async (fn, env, body) => {
  const ck = (await createSessionCookie({ role: 'teacher', username: 'boss' }, env.SESSION_SECRET)).split(';')[0];
  const r = await fn({ url: 'http://x/', headers: { get: (k) => (k.toLowerCase() === 'cookie' ? ck : null) }, async json() { return body; } }, env, { testId: '1' });
  return { status: r.status, d: await r.json() };
};
const order = (env) => env.raw.prepare('SELECT id FROM test_questions WHERE test_id = 1 ORDER BY order_no, id').all().map((r) => r.id);

test('reorder stores the new order', async () => {
  const env = await setup();
  assert.equal((await call(tests.reorderQuestions, env, { ids: [3, 1, 2] })).status, 200);
  assert.deepEqual(order(env), [3, 1, 2]);
});

test('reorder refuses a list that is not exactly the test\'s questions', async () => {
  const env = await setup();
  assert.equal((await call(tests.reorderQuestions, env, { ids: [3, 1] })).status, 400);
  assert.equal((await call(tests.reorderQuestions, env, { ids: [3, 1, 99] })).status, 400);
  assert.deepEqual(order(env), [1, 2, 3]);
});

test('bulk points sets every score or none', async () => {
  const env = await setup();
  assert.equal((await call(tests.setQuestionPoints, env, { points: { 1: 40, 2: 30, 3: 30 } })).status, 200);
  assert.deepEqual(env.raw.prepare('SELECT points FROM test_questions ORDER BY id').all().map((r) => r.points), [40, 30, 30]);
  assert.equal((await call(tests.setQuestionPoints, env, { points: { 1: 5, 2: 0 } })).status, 400);
  assert.equal((await call(tests.setQuestionPoints, env, { points: { 1: 5, 77: 2 } })).status, 400);
  assert.equal(env.raw.prepare('SELECT points FROM test_questions WHERE id = 1').get().points, 40);
});
