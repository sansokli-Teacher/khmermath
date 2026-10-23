// Student photos: private to teachers who may see the class, follow an ID change, and disappear with the student.
import test from 'node:test';
import assert from 'node:assert/strict';
import { makeEnv } from './d1shim.mjs';
import * as photos from '../src/api/photos.js';
import * as classes from '../src/api/classes.js';
import { hashSecretValue } from '../src/lib/crypto.js';
import { createSessionCookie } from '../src/lib/session.js';
import { _resetSchemaForTests, ensureColumns } from '../src/lib/schema.js';

async function setup() {
  const env = makeEnv(new URL('../schema.sql', import.meta.url).pathname);
  env.SESSION_SECRET = 'test-secret-long-enough-for-encryption-123456';
  _resetSchemaForTests();
  await ensureColumns(env);
  const h = await hashSecretValue('pw123456', 'x', env.SESSION_SECRET);
  const ins = env.raw.prepare("INSERT INTO teachers (username, password_hash, role, plan, active) VALUES (?, ?, ?, 'full', 1)");
  ins.run('boss', h, 'owner'); ins.run('other', h, 'teacher');
  env.raw.prepare("INSERT INTO classes (name, grade, owner_id) VALUES ('7NGS-B', 7, 2)").run();   // owned by the ordinary teacher "other"
  env.raw.prepare("INSERT INTO students (id, class_id, surname, first_name) VALUES ('s1', 1, 'A', 'One')").run();
  return env;
}
const JPEG = new Uint8Array([0xff, 0xd8, 0xff, 0xe0, 1, 2, 3, 4, 5]);
const call = async (fn, env, user, { type = 'image/jpeg', body = JPEG, id = 's1', json: jb } = {}) => {
  const ck = (await createSessionCookie({ role: 'teacher', username: user }, env.SESSION_SECRET)).split(';')[0];
  const req = { url: 'http://x/', headers: { get: (k) => (k.toLowerCase() === 'cookie' ? ck : k.toLowerCase() === 'content-type' ? type : null) }, async arrayBuffer() { return body.buffer.slice(body.byteOffset, body.byteOffset + body.byteLength); }, async json() { return jb; } };
  return fn(req, env, { studentId: id, classId: '1' });
};

test('the class owner stores and reads a photo; the list says a photo exists', async () => {
  const env = await setup();
  assert.equal((await call(photos.uploadPhoto, env, 'other')).status, 200);
  const r = await call(photos.servePhoto, env, 'other');
  assert.equal(r.status, 200); assert.equal(r.headers.get('Content-Type'), 'image/jpeg');
  assert.deepEqual(new Uint8Array(await r.arrayBuffer()), JPEG);
  const list = await (await call(classes.listStudents, env, 'other')).json();
  assert.ok(list.students[0].photo_v);
});

test('a teacher who cannot see the class cannot read or replace the photo', async () => {
  const env = await setup();
  await call(photos.uploadPhoto, env, 'other');
  env.raw.prepare("INSERT INTO teachers (username, password_hash, role, plan, active) VALUES ('stranger', 'x', 'teacher', 'full', 1)").run();
  assert.notEqual((await call(photos.servePhoto, env, 'stranger')).status, 200);
  assert.notEqual((await call(photos.uploadPhoto, env, 'stranger')).status, 200);
});

test('only pictures, and not huge ones', async () => {
  const env = await setup();
  assert.equal((await call(photos.uploadPhoto, env, 'other', { type: 'text/html' })).status, 400);
  assert.equal((await call(photos.uploadPhoto, env, 'other', { body: new Uint8Array(300 * 1024) })).status, 413);
});

test('the photo follows an ID change and is removed with the student', async () => {
  const env = await setup();
  await call(photos.uploadPhoto, env, 'other');
  const r = await call(classes.updateStudent, env, 'other', { json: { id: '0109293', surname: 'A', first_name: 'One' } });
  assert.equal(r.status, 200);
  assert.equal((await call(photos.servePhoto, env, 'other', { id: '0109293' })).status, 200);
  assert.equal((await call(classes.deleteStudent, env, 'other', { id: '0109293' })).status, 200);
  assert.equal(env.raw.prepare('SELECT COUNT(*) n FROM student_photos').get().n, 0);
});
