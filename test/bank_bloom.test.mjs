import test from 'node:test';
import assert from 'node:assert/strict';
import { makeEnv } from './d1shim.mjs';
import { ensureColumns, _resetSchemaForTests } from '../src/lib/schema.js';
import { createSessionCookie } from '../src/lib/session.js';
import { listBank, getTest, copyQuestions, duplicateTest } from '../src/api/tests.js';

async function setup() {
  const env = makeEnv(new URL('../schema.sql', import.meta.url).pathname);
  _resetSchemaForTests();
  await ensureColumns(env);
  env.SESSION_SECRET = 'test-bank-bloom';
  env.raw.exec(`INSERT INTO teachers(id,username,password_hash,role,plan,active) VALUES
    (1,'owner','x','owner','full',1),(3,'alice','x','teacher','full',1);
    INSERT INTO tests(id,title,owner_id,is_bank) VALUES(10,'bank',1,1),(20,'Alice test',3,0);
    INSERT INTO test_questions(id,test_id,order_no,stem_text,options_json,correct_index,points,level,bloom) VALUES
      (101,10,1,'Tagged','["a","b","c","d"]',0,2,'medium','Analyze'),
      (102,10,2,'Old untagged','["a","b","c","d"]',1,1,'easy',NULL);`);
  env.cookies = {};
  for (const username of ['owner', 'alice']) env.cookies[username] = (await createSessionCookie({ role: 'teacher', username }, env.SESSION_SECRET)).split(';')[0];
  return env;
}

async function call(fn, env, username, { method = 'GET', body, params } = {}) {
  const req = new Request('https://test.local/api', { method, headers: { Cookie: env.cookies[username], 'Content-Type': 'application/json' }, ...(body ? { body: JSON.stringify(body) } : {}) });
  const response = await fn(req, env, params || {});
  return { status: response.status, data: await response.json() };
}

test('the bank list and the test view carry the Bloom level (null for older questions)', async () => {
  const env = await setup();
  const bank = await call(listBank, env, 'owner');
  assert.equal(bank.status, 200);
  const byId = Object.fromEntries(bank.data.questions.map((q) => [q.id, q]));
  assert.equal(byId[101].bloom, 'Analyze');
  assert.equal(byId[102].bloom, null);
  const t = await call(getTest, env, 'owner', { params: { testId: 10 } });
  assert.equal(t.data.questions.find((q) => q.id === 101).bloom, 'Analyze');
});

test('copying a bank question into a test, and duplicating a test, keep the Bloom level', async () => {
  const env = await setup();
  const c = await call(copyQuestions, env, 'alice', { method: 'POST', body: { question_ids: [101, 102] }, params: { testId: 20 } });
  assert.equal(c.status, 200);
  assert.equal(c.data.copied, 2);
  const rows = env.raw.prepare('SELECT stem_text, bloom FROM test_questions WHERE test_id = 20 ORDER BY order_no').all();
  assert.deepEqual(rows.map((r) => r.bloom), ['Analyze', null]);
  const d = await call(duplicateTest, env, 'alice', { method: 'POST', params: { testId: 20 } });
  assert.equal(d.status, 200);
  const copy = env.raw.prepare('SELECT bloom FROM test_questions WHERE test_id = ? ORDER BY order_no').all(d.data.id);
  assert.deepEqual(copy.map((r) => r.bloom), ['Analyze', null]);
});
