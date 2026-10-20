import test from 'node:test';
import assert from 'node:assert/strict';
import { makeEnv } from './d1shim.mjs';
import * as teacher from '../src/api/teacher.js';
import { hashSecretValue } from '../src/lib/crypto.js';
import { _resetSchemaForTests, ensureColumns } from '../src/lib/schema.js';

function makeRequest(body, ip = '127.0.0.1') {
  return {
    headers: new Map([['cf-connecting-ip', ip]]),
    async json() { return body; },
  };
}

async function initEnv() {
  const env = makeEnv(new URL('../schema.sql', import.meta.url).pathname);
  env.SESSION_SECRET = 'test-secret-long-enough-for-encryption-123456';
  _resetSchemaForTests();
  await ensureColumns(env);
  return env;
}

test('signup with username and login with case-insensitive username', async () => {
  const env = await initEnv();

  // Signup
  const res = await teacher.signup(
    makeRequest({ display_name: 'គ្រូ សុភា', username: 'sopha123', password: 'password123' }, '10.0.0.1'),
    env
  );
  assert.equal(res.status, 200);
  assert.ok(res.headers.get('Set-Cookie'));

  // Login exact case
  const loginRes = await teacher.login(
    makeRequest({ username: 'sopha123', password: 'password123' }, '10.0.0.1'),
    env
  );
  assert.equal(loginRes.status, 200);

  // Login uppercase / mixed case
  const loginResUpper = await teacher.login(
    makeRequest({ username: 'Sopha123', password: 'password123' }, '10.0.0.1'),
    env
  );
  assert.equal(loginResUpper.status, 200);
});

test('signup with email and login with email (case-insensitive)', async () => {
  const env = await initEnv();

  // Signup with email
  const res = await teacher.signup(
    makeRequest({ display_name: 'គ្រូ ចាន់ណា', username: 'channa.math@gmail.com', password: 'password123' }, '10.0.0.2'),
    env
  );
  assert.equal(res.status, 200);
  const data = await res.json();
  assert.equal(data.ok, true);

  // Verify email column was saved
  const row = env.raw.prepare("SELECT username, email FROM teachers WHERE email = 'channa.math@gmail.com'").get();
  assert.ok(row);
  assert.equal(row.username, 'channa.math@gmail.com');
  assert.equal(row.email, 'channa.math@gmail.com');

  // Login with lowercase email
  const loginRes = await teacher.login(
    makeRequest({ username: 'channa.math@gmail.com', password: 'password123' }, '10.0.0.2'),
    env
  );
  assert.equal(loginRes.status, 200);

  // Login with mixed case email
  const loginResUpper = await teacher.login(
    makeRequest({ username: 'Channa.MATH@Gmail.Com', password: 'password123' }, '10.0.0.2'),
    env
  );
  assert.equal(loginResUpper.status, 200);
});

test('signup with phone number and optional contact', async () => {
  const env = await initEnv();

  const res = await teacher.signup(
    makeRequest({ display_name: 'លោកគ្រូ រតនា', username: '012345678', contact: 'Telegram @rathana', password: 'mypassword' }, '10.0.0.3'),
    env
  );
  assert.equal(res.status, 200);

  const loginRes = await teacher.login(
    makeRequest({ username: '012345678', password: 'mypassword' }, '10.0.0.3'),
    env
  );
  assert.equal(loginRes.status, 200);
});

test('login to legacy account where @ was stripped upon signup', async () => {
  const env = await initEnv();

  // Simulate an existing legacy row where @ was stripped: 'hengkanitha2222gmail.com'
  const legacyHash = await hashSecretValue('mypassword123', 'hengkanitha2222gmail.com', env.SESSION_SECRET);
  env.raw.prepare("INSERT INTO teachers (username, password_hash, role, display_name, plan, active) VALUES ('hengkanitha2222gmail.com', ?, 'teacher', 'Heng Kanitha', 'full', 1)")
    .run(legacyHash);

  // Teacher attempts to log in with their real email with @
  const loginRes = await teacher.login(
    makeRequest({ username: 'hengkanitha2222@gmail.com', password: 'mypassword123' }, '10.0.0.4'),
    env
  );
  assert.equal(loginRes.status, 200);
  assert.ok(loginRes.headers.get('Set-Cookie'));
});

test('signup validations reject invalid emails, short passwords, duplicate users', async () => {
  const env = await initEnv();

  // Invalid email (missing domain)
  const badEmail = await teacher.signup(
    makeRequest({ display_name: 'Test', username: 'invalid-email@', password: 'password123' }, '10.0.0.5'),
    env
  );
  assert.equal(badEmail.status, 400);

  // Invalid username (too short)
  const shortUser = await teacher.signup(
    makeRequest({ display_name: 'Test', username: 'ab', password: 'password123' }, '10.0.0.5'),
    env
  );
  assert.equal(shortUser.status, 400);

  // Short password (< 6 chars)
  const shortPass = await teacher.signup(
    makeRequest({ display_name: 'Test', username: 'validuser', password: '123' }, '10.0.0.5'),
    env
  );
  assert.equal(shortPass.status, 400);

  // Successful signup
  const okSignup = await teacher.signup(
    makeRequest({ display_name: 'Test', username: 'teacher1', password: 'password123' }, '10.0.0.5'),
    env
  );
  assert.equal(okSignup.status, 200);

  // Duplicate username (409)
  const dupSignup = await teacher.signup(
    makeRequest({ display_name: 'Test 2', username: 'TEACHER1', password: 'password123' }, '10.0.0.5'),
    env
  );
  assert.equal(dupSignup.status, 409);
});

test('forgot password works with username or email', async () => {
  const env = await initEnv();

  // Create a teacher
  await teacher.signup(
    makeRequest({ display_name: 'គ្រូ វិសាល', username: 'visal@school.edu.kh', password: 'password123' }, '10.0.0.6'),
    env
  );

  // Forgot password using email
  const forgotRes = await teacher.forgotPassword(
    makeRequest({ username: 'VISAL@school.edu.kh', contact: '012999888' }, '10.0.0.6'),
    env
  );
  assert.equal(forgotRes.status, 200);

  // Verify unlock request created
  const reqRow = env.raw.prepare("SELECT * FROM unlock_requests WHERE plan = 'reset'").get();
  assert.ok(reqRow);
  assert.equal(reqRow.contact, '012999888');
});

test('a later signup whose contact mimics a username cannot shadow the real account', async () => {
  const env = await initEnv();
  await teacher.signup(makeRequest({ display_name: 'Victim', username: 'victim', password: 'victim-pass1' }, '10.0.1.1'), env);
  await teacher.signup(makeRequest({ display_name: 'Mallory', username: 'mallory', password: 'mallory-pass1', contact: 'victim' }, '10.0.1.2'), env);

  const ok = await teacher.login(makeRequest({ username: 'victim', password: 'victim-pass1' }, '10.0.1.3'), env);
  assert.equal(ok.status, 200);
  const cookie = ok.headers.get('Set-Cookie');
  assert.match(cookie, /./);
  const bad = await teacher.login(makeRequest({ username: 'victim', password: 'mallory-pass1' }, '10.0.1.4'), env);
  assert.equal(bad.status, 401);
});
