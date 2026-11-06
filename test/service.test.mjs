// The service API report.khmermath.org uses: make a teacher + classes + students, and a one-minute single-use sign-in link.
import test from 'node:test';
import assert from 'node:assert/strict';
import { makeEnv } from './d1shim.mjs';
import * as service from '../src/api/service.js';
import { hashSecretValue } from '../src/lib/crypto.js';
import { _resetSchemaForTests, ensureColumns } from '../src/lib/schema.js';

const KEY = 'k'.repeat(32);
async function setup(withKey = true) {
  const env = makeEnv(new URL('../schema.sql', import.meta.url).pathname);
  env.SESSION_SECRET = 'test-secret-long-enough-for-encryption-123456';
  if (withKey) env.SERVICE_KEY = KEY;
  _resetSchemaForTests(); await ensureColumns(env);
  const h = await hashSecretValue('pw', 'boss', env.SESSION_SECRET);
  env.raw.prepare("INSERT INTO teachers (username, password_hash, role, display_name, plan) VALUES ('boss', ?, 'owner', 'Boss', 'full')").run(h);
  return env;
}
const req = (url, body, key = KEY) => new Request(url, { method: body ? 'POST' : 'GET', headers: { 'X-Service-Key': key, 'Content-Type': 'application/json' }, body: body ? JSON.stringify(body) : undefined });
const T = { username: 'chaysophea', refId: 'tch-5', displayName: 'ចាយ សុភា', classes: [{ name: '8NGS-B', grade: 8, students: [{ id: '0109293', surname: 'សុខ', firstName: 'ដារ៉ា', gender: 'ស្រី' }, { id: '0109294', surname: 'ចាន់', firstName: 'វិបុល' }] }] };

test('without the key (or with a wrong one) nothing works', async () => {
  const off = await setup(false);
  assert.equal((await service.provision(req('http://x/p', T), off)).status, 404);
  const env = await setup();
  assert.equal((await service.provision(req('http://x/p', T, 'wrong'), env)).status, 403);
  assert.equal(env.raw.prepare('SELECT COUNT(*) n FROM teachers').get().n, 1);
});

test('provision makes the teacher with a one-year full plan, the class and its students', async () => {
  const env = await setup();
  const r = await service.provision(req('http://x/p', T), env); const d = await r.json();
  assert.equal(r.status, 200); assert.equal(d.created, true);
  const t = env.raw.prepare("SELECT * FROM teachers WHERE username = 'chaysophea'").get();
  assert.equal(t.plan, 'full'); assert.equal(t.role, 'teacher'); assert.equal(t.ext_ref, 'report:tch-5');
  const yrs = (new Date(t.license_until.replace(' ', 'T') + 'Z') - Date.now()) / 86400000;
  assert.ok(yrs > 360 && yrs < 370, `about a year, got ${yrs}`);
  assert.equal(d.classes[0].students, 2);
  assert.equal(env.raw.prepare('SELECT COUNT(*) n FROM students').get().n, 2);
});

test('syncing again updates, never duplicates or stacks months', async () => {
  const env = await setup();
  await service.provision(req('http://x/p', T), env);
  const before = env.raw.prepare("SELECT license_until FROM teachers WHERE username = 'chaysophea'").get().license_until;
  const T2 = { ...T, displayName: 'ចាយ សុភា (ថ្មី)', classes: [{ ...T.classes[0], students: [...T.classes[0].students, { id: '0109295', surname: 'លី', firstName: 'សុវណ្ណ' }] }] };
  const d = await (await service.provision(req('http://x/p', T2), env)).json();
  assert.equal(d.created, false); assert.equal(d.classes[0].students, 3);
  assert.equal(env.raw.prepare('SELECT COUNT(*) n FROM teachers').get().n, 2);
  assert.equal(env.raw.prepare('SELECT COUNT(*) n FROM classes').get().n, 1);
  assert.equal(env.raw.prepare("SELECT license_until FROM teachers WHERE username = 'chaysophea'").get().license_until, before);
  assert.equal(env.raw.prepare("SELECT display_name FROM teachers WHERE username = 'chaysophea'").get().display_name, 'ចាយ សុភា (ថ្មី)');
});

test('an expired plan is renewed on sync; a taken username or the owner is never taken over', async () => {
  const env = await setup();
  await service.provision(req('http://x/p', T), env);
  env.raw.prepare("UPDATE teachers SET license_until = '2020-01-01 00:00:00' WHERE username = 'chaysophea'").run();
  await service.provision(req('http://x/p', T), env);
  assert.ok(env.raw.prepare("SELECT license_until FROM teachers WHERE username = 'chaysophea'").get().license_until > '2026');
  const clash = await service.provision(req('http://x/p', { ...T, username: 'boss', refId: 'tch-9' }), env);
  assert.equal(clash.status, 409);
  assert.equal((await service.sso(req('http://x/s', { refId: 'nobody' }), env)).status, 404);
});

test("a student already in another teacher's class is skipped, not moved", async () => {
  const env = await setup();
  await service.provision(req('http://x/p', T), env);
  const other = { username: 'otherteach', refId: 'tch-6', displayName: 'Other', classes: [{ name: '8NGS-B', grade: 8, students: [{ id: '0109293', surname: 'X', firstName: 'Y' }, { id: '0200000', surname: 'Z', firstName: 'W' }] }] };
  const d = await (await service.provision(req('http://x/p', other), env)).json();
  assert.deepEqual(d.classes[0].skipped, ['0109293']); assert.equal(d.classes[0].students, 1);
  assert.equal(env.raw.prepare("SELECT surname FROM students WHERE id = '0109293'").get().surname, 'សុខ');
});

test('the sign-in link signs the teacher in once, then is dead; a tampered one fails', async () => {
  const env = await setup();
  await service.provision(req('http://x/p', T), env);
  const { url } = await (await service.sso(req('https://exam.test/s', { refId: 'tch-5' }), env)).json();
  assert.match(url, /^https:\/\/exam\.test\/api\/sso\?t=/);
  const ok = await service.ssoLogin(new Request(url), env);
  assert.equal(ok.status, 302); assert.equal(ok.headers.get('Location'), '/teacher'); assert.match(ok.headers.get('Set-Cookie'), /^exam_teacher=/);
  assert.equal((await service.ssoLogin(new Request(url), env)).status, 403);
  const { url: u2 } = await (await service.sso(req('https://exam.test/s', { refId: 'tch-5' }), env)).json();
  assert.equal((await service.ssoLogin(new Request(u2.slice(0, -3) + 'abc'), env)).status, 403);
});

test('results: a teacher sees only their own sessions; unmarked writing is null, not 0', async () => {
  const env = await setup();
  await service.provision(req('http://x/p', T), env);
  await service.provision(req('http://x/p', { username: 'otherteach', refId: 'tch-6', displayName: 'O', classes: [{ name: '9NGS-A', grade: 9, students: [{ id: '0300000', surname: 'Q', firstName: 'R' }] }] }), env);
  const r = env.raw;
  r.prepare("INSERT INTO tests (title) VALUES ('Quiz 1')").run();
  const cid = (n) => r.prepare('SELECT id FROM classes WHERE name = ?').get(n).id;
  r.prepare("INSERT INTO test_sessions (test_id, class_id, scheduled_start, duration_minutes) VALUES (1, ?, '2026-11-01T01:00:00Z', 40)").run(cid('8NGS-B'));
  r.prepare("INSERT INTO test_sessions (test_id, class_id, scheduled_start, duration_minutes) VALUES (1, ?, '2026-11-02T01:00:00Z', 40)").run(cid('9NGS-A'));
  r.prepare("INSERT INTO results (session_id, student_id, mcq_score, mcq_max, writing_score, writing_max, submitted_at) VALUES (1, '0109293', 18, 25, 14, 25, '2026-11-01T01:30:00Z')").run();
  r.prepare("INSERT INTO results (session_id, student_id, mcq_score, mcq_max, writing_score, writing_max, submitted_at) VALUES (1, '0109294', 20, 25, NULL, 25, '2026-11-01T01:31:00Z')").run();
  r.prepare("INSERT INTO students (id, class_id, surname, first_name) VALUES ('0109295', ?, 'ល', 'ម')").run(cid('8NGS-B'));
  r.prepare("INSERT INTO results (session_id, student_id, mcq_score, mcq_max, submitted_at) VALUES (1, '0109295', 1, 25, NULL)").run();
  const list = await (await service.sessions(req('http://x/s', { refId: 'tch-5' }), env)).json();
  assert.equal(list.sessions.length, 1); assert.equal(list.sessions[0].className, '8NGS-B'); assert.equal(list.sessions[0].submitted, 2);
  const d = await (await service.sessionResults(req('http://x/r', { refId: 'tch-5', sessionId: 1 }), env)).json();
  assert.equal(d.published, 0); assert.equal(d.rows.every((x) => x.published === false), true);   // not announced yet
  assert.equal(list.sessions[0].published, 0);
  assert.equal(d.rows.length, 2); assert.equal(d.mcqMax, 25); assert.equal(d.writingMax, 25); assert.equal(d.writingPending, 1);
  assert.equal(d.rows.find((x) => x.id === '0109294').writing, null);
  assert.equal((await service.sessionResults(req('http://x/r', { refId: 'tch-5', sessionId: 2 }), env)).status, 404);   // someone else's session
  r.prepare("UPDATE results SET published_at = '2026-11-02 01:00:00' WHERE session_id = 1").run();   // the teacher announces the results
  const d2 = await (await service.sessionResults(req('http://x/r', { refId: 'tch-5', sessionId: 1 }), env)).json();
  assert.equal(d2.published, 2); assert.equal(d2.rows.every((x) => x.published), true);
  assert.equal((await (await service.sessions(req('http://x/s', { refId: 'tch-5' }), env)).json()).sessions[0].published, 2);
});

test('topics: class and student scores by topic; withdrawn, writing and untagged questions left out; only own class', async () => {
  const env = await setup();
  await service.provision(req('http://x/p', T), env);
  const r = env.raw;
  r.prepare("INSERT INTO tests (title) VALUES ('Quiz 1')").run();
  const cid = r.prepare("SELECT id FROM classes WHERE name = '8NGS-B'").get().id;
  r.prepare("INSERT INTO test_sessions (test_id, class_id, scheduled_start, duration_minutes) VALUES (1, ?, '2026-11-01T01:00:00Z', 40)").run(cid);
  const q = (no, topic, kind = 'mcq', cancelled = 0) => r.prepare("INSERT INTO test_questions (test_id, order_no, stem_text, options_json, correct_index, points, kind, topic, cancelled) VALUES (1, ?, 's', '[\"a\",\"b\"]', 0, 1, ?, ?, ?)").run(no, kind, topic, cancelled);
  q(1, 'Fractions'); q(2, 'Fractions'); q(3, 'Geometry'); q(4, null); q(5, 'Geometry', 'writing'); q(6, 'Geometry', 'mcq', 1);
  for (const id of ['0109293', '0109294']) r.prepare("INSERT INTO results (session_id, student_id, mcq_score, mcq_max, submitted_at) VALUES (1, ?, 0, 4, '2026-11-01T01:30:00Z')").run(id);
  const ans = (sid, qno, sel) => r.prepare('INSERT INTO responses (session_id, student_id, question_id, selected_index) VALUES (1, ?, ?, ?)').run(sid, r.prepare('SELECT id FROM test_questions WHERE order_no = ?').get(qno).id, sel);
  ans('0109293', 1, 0); ans('0109293', 2, 0); ans('0109293', 3, 1);   // Fractions 2/2, Geometry 0/1
  ans('0109294', 1, 1); ans('0109294', 2, 0); ans('0109294', 3, 1);   // Fractions 1/2, Geometry 0/1
  const d = await (await service.topics(req('http://x/t', { refId: 'tch-5', className: '8NGS-B' }), env)).json();
  assert.deepEqual(d.topics.map((x) => [x.name, x.pct]), [['Geometry', 0], ['Fractions', 75]]);   // weakest first
  assert.equal(d.untagged, 1);
  assert.equal(d.topics[1].students.find((s) => s.id === '0109294').earned, 1);
  assert.equal((await (await service.topics(req('http://x/t', { refId: 'tch-5', className: '9NGS-A' }), env)).json()).topics.length, 0);
  assert.equal((await service.topics(req('http://x/t', { refId: 'tch-5', className: '8NGS-B' }, 'bad'), env)).status, 403);
});

test('retest: a new test on the weak topics from the teacher\'s own questions, unseen ones first, set for the class now; trend per topic', async () => {
  const env = await setup();
  await service.provision(req('http://x/p', T), env);
  const r = env.raw;
  const owner = r.prepare("SELECT id FROM teachers WHERE username = 'chaysophea'").get().id;
  const cid = r.prepare("SELECT id FROM classes WHERE name = '8NGS-B'").get().id;
  r.prepare("INSERT INTO tests (title, owner_id) VALUES ('Old', ?)").run(owner);                 // test 1: sat by the class
  r.prepare("INSERT INTO tests (title, owner_id) VALUES ('Bank', ?)").run(owner);                // test 2: spare questions, never sat
  const q = (tid, no, stem, topic, kind = 'mcq') => r.prepare("INSERT INTO test_questions (test_id, order_no, stem_text, options_json, correct_index, points, kind, topic) VALUES (?, ?, ?, '[\"a\",\"b\"]', 0, 1, ?, ?)").run(tid, no, stem, kind, topic);
  q(1, 1, 'seen-frac', 'Fractions'); q(2, 1, 'new-frac-1', 'Fractions'); q(2, 2, 'new-frac-2', 'Fractions'); q(2, 3, 'seen-frac', 'Fractions'); q(2, 4, 'writing-frac', 'Fractions', 'writing');
  r.prepare("INSERT INTO test_sessions (test_id, class_id, scheduled_start, duration_minutes) VALUES (1, ?, '2026-11-01T01:00:00Z', 40)").run(cid);
  r.prepare("INSERT INTO results (session_id, student_id, mcq_score, mcq_max, submitted_at) VALUES (1, '0109293', 0, 1, '2026-11-01T01:30:00Z')").run();
  const d = await (await service.retest(req('http://x/rt', { refId: 'tch-5', className: '8NGS-B', topics: ['Fractions', 'Geometry'], perTopic: 2, minutes: 25 }), env)).json();
  assert.equal(d.created, true); assert.equal(d.questions, 2); assert.deepEqual(d.missing, ['Geometry']);
  const stems = r.prepare('SELECT stem_text FROM test_questions WHERE test_id = ? ORDER BY order_no').all(d.testId).map((x) => x.stem_text);
  assert.deepEqual([...stems].sort(), ['new-frac-1', 'new-frac-2']);                                          // unseen first; no writing; no duplicates
  const s = r.prepare('SELECT * FROM test_sessions WHERE id = ?').get(d.sessionId);
  assert.equal(s.class_id, cid); assert.equal(s.duration_minutes, 25); assert.ok(Date.parse(s.scheduled_start) <= Date.now());   // open now
  assert.equal(r.prepare('SELECT status FROM tests WHERE id = ?').get(d.testId).status, 'ready');
  // nothing found: nothing created; someone else's class / no topics refused
  const none = await (await service.retest(req('http://x/rt', { refId: 'tch-5', className: '8NGS-B', topics: ['Nope'] }), env)).json();
  assert.equal(none.created, false);
  assert.equal((await service.retest(req('http://x/rt', { refId: 'tch-5', className: '9NGS-A', topics: ['Fractions'] }), env)).status, 404);
  assert.equal((await service.retest(req('http://x/rt', { refId: 'tch-5', className: '8NGS-B', topics: [] }), env)).status, 400);
  assert.equal((await service.retest(req('http://x/rt', { refId: 'tch-5', className: '8NGS-B', topics: ['Fractions'] }, 'bad'), env)).status, 403);
  // the trend: the class sat the old test only → one point
  const tp = await (await service.topics(req('http://x/t', { refId: 'tch-5', className: '8NGS-B' }), env)).json();
  assert.equal(tp.topics[0].trend.length, 1);
});
