import test from 'node:test';
import assert from 'node:assert/strict';
import { makeEnv } from './d1shim.mjs';
import { ensureColumns, _resetSchemaForTests } from '../src/lib/schema.js';
import { createSessionCookie } from '../src/lib/session.js';
import { deleteQuestion, deleteBankQuestions } from '../src/api/tests.js';

async function setup() {
  const env = makeEnv(new URL('../schema.sql', import.meta.url).pathname);
  _resetSchemaForTests();
  await ensureColumns(env);
  env.SESSION_SECRET = 'test-bank-delete';
  env.raw.exec(`INSERT INTO teachers(id,username,password_hash,role,plan,active) VALUES
    (1,'owner','x','owner','full',1),(2,'staff','x','admin','full',1),(3,'alice','x','teacher','full',1);
    INSERT INTO tests(id,title,owner_id,is_bank) VALUES(10,'bank',1,1),(20,'Alice test',3,0);
    INSERT INTO test_questions(id,test_id,order_no,stem_text,options_json,correct_index,points) VALUES
      (101,10,1,'NGS Q1','["a","b","c","d"]',0,1),
      (102,10,2,'NGS Q2','["a","b","c","d"]',1,1),
      (201,20,1,'Alice Q','["a","b","c","d"]',0,1);`);
  env.cookies = {};
  for (const username of ['owner', 'staff', 'alice']) {
    env.cookies[username] = (await createSessionCookie({ role: 'teacher', username }, env.SESSION_SECRET)).split(';')[0];
  }
  return env;
}

async function call(fn, env, username, { method = 'POST', body, params } = {}) {
  const req = new Request('https://test.local/api', {
    method,
    headers: { Cookie: env.cookies[username], 'Content-Type': 'application/json' },
    ...(body ? { body: JSON.stringify(body) } : {}),
  });
  const response = await fn(req, env, params || {});
  return { status: response.status, data: await response.json() };
}

test('regular teacher cannot delete the shared question bank', async () => {
  const env = await setup();
  assert.equal((await call(deleteQuestion, env, 'alice', { method: 'DELETE', params: { questionId: 101 } })).status, 404);
  assert.equal((await call(deleteBankQuestions, env, 'alice', { body: { question_ids: [101] } })).status, 403);
  assert.equal(env.raw.prepare('SELECT COUNT(*) AS n FROM test_questions WHERE id = 101').get().n, 1);
});

test('owner and admin can delete shared bank questions', async () => {
  const env = await setup();
  const ownerDel = await call(deleteQuestion, env, 'owner', { method: 'DELETE', params: { questionId: 101 } });
  assert.equal(ownerDel.status, 200);
  const staffDel = await call(deleteQuestion, env, 'staff', { method: 'DELETE', params: { questionId: 102 } });
  assert.equal(staffDel.status, 200);
  assert.equal(env.raw.prepare('SELECT COUNT(*) AS n FROM test_questions WHERE id IN (101,102)').get().n, 0);
});

test('admin bulk-delete only removes bank questions, not another teacher test', async () => {
  const env = await setup();
  const r = await call(deleteBankQuestions, env, 'staff', { body: { question_ids: [101, 201] } });
  assert.equal(r.status, 200);
  assert.equal(r.data.deleted, 1);
  assert.equal(r.data.skipped, 1);
  assert.equal(env.raw.prepare('SELECT COUNT(*) AS n FROM test_questions WHERE id = 101').get().n, 0);
  assert.equal(env.raw.prepare('SELECT COUNT(*) AS n FROM test_questions WHERE id = 201').get().n, 1);
});
