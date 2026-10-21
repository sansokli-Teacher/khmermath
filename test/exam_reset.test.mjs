// Teacher tools during an exam: a double-fired «+5'» counts once, and resetting a submitted student after the exam time
// needs (and applies) the minutes the teacher gives; students who are not reset stay finished.
import test from 'node:test';
import assert from 'node:assert/strict';
import { makeEnv } from './d1shim.mjs';
import * as sessions from '../src/api/sessions.js';
import { hashSecretValue } from '../src/lib/crypto.js';
import { createSessionCookie } from '../src/lib/session.js';
import { _resetSchemaForTests, ensureColumns } from '../src/lib/schema.js';

async function setup({ endedMinutesAgo = 0 } = {}) {
  const env = makeEnv(new URL('../schema.sql', import.meta.url).pathname);
  env.SESSION_SECRET = 'test-secret-long-enough-for-encryption-123456';
  _resetSchemaForTests();
  await ensureColumns(env);
  env.raw.prepare("INSERT INTO teachers (username, password_hash, role, plan, active) VALUES ('boss', ?, 'owner', 'full', 1)").run(await hashSecretValue('pw123456', 'boss', env.SESSION_SECRET));
  env.raw.prepare("INSERT INTO classes (name, grade, owner_id) VALUES ('c', 9, 1)").run();
  env.raw.prepare("INSERT INTO students (id, class_id, surname, first_name) VALUES ('s1', 1, 'A', 'One'), ('s2', 1, 'B', 'Two')").run();
  env.raw.prepare("INSERT INTO tests (title, status, owner_id, is_bank, is_sample) VALUES ('t', 'draft', 1, 0, 0)").run();
  const end = Date.now() - endedMinutesAgo * 60000, start = end - 60 * 60000;
  env.raw.prepare("INSERT INTO test_sessions (test_id, class_id, scheduled_start, duration_minutes, scheduled_end, pin) VALUES (1, 1, ?, 60, ?, '1')").run(new Date(start).toISOString(), new Date(end).toISOString());
  const st = new Date(start + 60000).toISOString().replace('T', ' ').slice(0, 19), sub = new Date(end - 20 * 60000).toISOString().replace('T', ' ').slice(0, 19);
  env.raw.prepare("INSERT INTO results (session_id, student_id, mcq_score, mcq_max, started_at, submitted_at, submit_type) VALUES (1, 's1', 5, 10, ?, ?, 'manual'), (1, 's2', 6, 10, ?, ?, 'manual')").run(st, sub, st, sub);
  return env;
}
const call = async (fn, env, body) => {
  const ck = (await createSessionCookie({ role: 'teacher', username: 'boss' }, env.SESSION_SECRET)).split(';')[0];
  const r = await fn({ url: 'http://x/', headers: { get: (k) => (k.toLowerCase() === 'cookie' ? ck : null) }, async json() { return body; } }, env, { sessionId: '1' });
  return { status: r.status, d: await r.json() };
};
const row = (env, id) => env.raw.prepare('SELECT submitted_at, extra_minutes FROM results WHERE session_id = 1 AND student_id = ?').get(id);

test('a double-fired +5 minutes is counted once', async () => {
  const env = await setup();
  const a = await call(sessions.extendSession, env, { student_id: 's1', minutes: 5 });
  const b = await call(sessions.extendSession, env, { student_id: 's1', minutes: 5 });
  assert.equal(a.d.extra_minutes, 5); assert.equal(b.d.extra_minutes, 5); assert.equal(b.d.duplicate, true);
  assert.equal(row(env, 's1').extra_minutes, 5);
});

test('reset while the exam is still running re-opens the student without touching the clock', async () => {
  const env = await setup({ endedMinutesAgo: -30 });          // ends in 30 minutes
  const r = await call(sessions.resetStudentSession, env, { student_id: 's1' });
  assert.equal(r.status, 200);
  assert.equal(row(env, 's1').submitted_at, null); assert.equal(row(env, 's1').extra_minutes, 0);
  assert.ok(row(env, 's2').submitted_at);                       // the other student stays finished
});

test('reset after the exam time needs minutes, then the student gets exactly that time from now; the others stay finished', async () => {
  const env = await setup({ endedMinutesAgo: 15 });
  const refused = await call(sessions.resetStudentSession, env, { student_id: 's1' });
  assert.equal(refused.status, 409); assert.ok(row(env, 's1').submitted_at);   // nothing changed
  const ok = await call(sessions.resetStudentSession, env, { student_id: 's1', minutes: 10 });
  assert.equal(ok.status, 200);
  assert.equal(row(env, 's1').submitted_at, null);
  const left = Date.parse(ok.d.until) - Date.now();
  assert.ok(left > 9 * 60000 && left <= 11 * 60000, `about 10 minutes left, got ${left / 60000}`);
  assert.ok([25, 26].includes(row(env, 's1').extra_minutes));    // 15 minutes since the end + 10 more (rounded up to a whole minute)
  assert.ok(row(env, 's2').submitted_at);
});

import * as integrity from '../src/api/integrity.js';

test('a long press on a phone and a keyboard resizing the window are not incidents; the same on a desktop still are', () => {
  const phone = 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 Chrome/155 Mobile Safari/537.36', desktop = 'Mozilla/5.0 (Windows NT 10.0) Chrome/155';
  assert.equal(integrity.countsEvent('contextmenu', 0, null, phone), false);
  assert.equal(integrity.countsEvent('contextmenu', 0, null, desktop), true);
  assert.equal(integrity.countsEvent('split_view', 0, '390x500 from 390x800', phone), false);       // only the height changed
  assert.equal(integrity.countsEvent('split_view', 0, '250x800 from 390x800', phone), true);        // the width really shrank
  assert.equal(integrity.countsEvent('fullscreen_exit', 0, null, phone), true);
  assert.equal(integrity.countsEvent('tab_hidden', 500, null, phone), false);                       // short glance away
});

test('unlocking gives the locked minutes back once, and «unlock all» does it for everyone', async () => {
  const env = await setup({ endedMinutesAgo: -30 });
  env.raw.prepare("UPDATE results SET submitted_at = NULL, submit_type = NULL, locked = 1")
    .run();
  const at = new Date(Date.now() - 7 * 60000).toISOString().replace('T', ' ').slice(0, 19);
  env.raw.prepare("INSERT INTO exam_events (session_id, student_id, at, kind, detail) VALUES (1, 's1', ?, 'locked', 'auto'), (1, 's2', ?, 'locked', 'auto')").run(at, at);
  const one = await call(integrity.lockStudent, env, { student_id: 's1', locked: false });
  assert.ok([7, 8].includes(one.d.given_back));                    // 7 minutes, rounded up to a whole minute
  assert.equal(row(env, 's1').extra_minutes, one.d.given_back);
  const all = await call(integrity.unlockAll, env, {});
  assert.equal(all.d.count, 1);                                   // s1 was already unlocked
  assert.ok([7, 8].includes(row(env, 's2').extra_minutes));
  assert.equal(env.raw.prepare('SELECT COUNT(*) c FROM results WHERE locked = 1').get().c, 0);
});
