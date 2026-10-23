// A teacher writes their own name; the owner can correct anybody's; an admin cannot rename the owner.
import test from 'node:test';
import assert from 'node:assert/strict';
import { makeEnv } from './d1shim.mjs';
import * as teacher from '../src/api/teacher.js';
import * as admin from '../src/api/admin.js';
import { hashSecretValue } from '../src/lib/crypto.js';
import { createSessionCookie } from '../src/lib/session.js';
import { _resetSchemaForTests, ensureColumns } from '../src/lib/schema.js';

async function setup() {
  const env = makeEnv(new URL('../schema.sql', import.meta.url).pathname);
  env.SESSION_SECRET = 'test-secret-long-enough-for-encryption-123456';
  _resetSchemaForTests();
  await ensureColumns(env);
  const ins = env.raw.prepare("INSERT INTO teachers (username, password_hash, role, display_name, plan, active) VALUES (?, ?, ?, ?, 'full', 1)");
  const h = await hashSecretValue('pw123456', 'x', env.SESSION_SECRET);
  ins.run('boss', h, 'owner', 'SAN SOKLI'); ins.run('tea', h, 'teacher', 'Tea'); ins.run('adm', h, 'admin', 'Adm');
  return env;
}
const call = async (fn, env, user, body, params = {}) => {
  const ck = (await createSessionCookie({ role: 'teacher', username: user }, env.SESSION_SECRET)).split(';')[0];
  const r = await fn({ url: 'http://x/', headers: { get: (k) => (k.toLowerCase() === 'cookie' ? ck : null) }, async json() { return body; } }, env, params);
  return { status: r.status, d: await r.json() };
};
const nameOf = (env, u) => env.raw.prepare('SELECT display_name FROM teachers WHERE username = ?').get(u).display_name;

test('a teacher can write their own name in Khmer', async () => {
  const env = await setup();
  const r = await call(teacher.updateMyProfile, env, 'boss', { display_name: '  សាន   សុខលី ' });
  assert.equal(r.status, 200); assert.equal(nameOf(env, 'boss'), 'សាន សុខលី');
  assert.equal((await call(teacher.updateMyProfile, env, 'boss', { display_name: '   ' })).status, 400);
  assert.equal(nameOf(env, 'boss'), 'សាន សុខលី');
});

test('the owner renames another user; an admin cannot rename the owner; an ordinary teacher cannot rename anyone', async () => {
  const env = await setup();
  const id = (u) => String(env.raw.prepare('SELECT id FROM teachers WHERE username = ?').get(u).id);
  assert.equal((await call(admin.setTeacherName, env, 'boss', { display_name: 'គ្រូ ទី' }, { id: id('tea') })).status, 200);
  assert.equal(nameOf(env, 'tea'), 'គ្រូ ទី');
  assert.equal((await call(admin.setTeacherName, env, 'adm', { display_name: 'X' }, { id: id('boss') })).status, 403);
  assert.equal(nameOf(env, 'boss'), 'SAN SOKLI');
  assert.notEqual((await call(admin.setTeacherName, env, 'tea', { display_name: 'Y' }, { id: id('adm') })).status, 200);
  assert.equal(nameOf(env, 'adm'), 'Adm');
});
