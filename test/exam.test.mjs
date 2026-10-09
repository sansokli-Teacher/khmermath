// Run: node --test test/        (Node 22+)
import test from 'node:test';
import assert from 'node:assert/strict';
import { makeEnv } from './d1shim.mjs';
import { ensureColumns, _resetSchemaForTests } from '../src/lib/schema.js';
import { sessionQuestions, syncKeyToFrozen, isFrozen } from '../src/lib/frozen.js';
import { rescoreSession } from '../src/lib/scoring.js';
import { checkReadiness } from '../src/lib/readiness.js';
import { runBackup, getBackupFile } from '../src/lib/backup.js';
import { gunzipJson, validateBackup, planRestore, applyRestore } from '../src/lib/restore.js';

async function seed() {
  const env = makeEnv(new URL('../schema.sql', import.meta.url).pathname);
  _resetSchemaForTests();
  await ensureColumns(env);
  const r = env.raw;
  r.exec(`INSERT INTO teachers (id, username, password_hash) VALUES (1, 'owner', 'x')`);
  r.exec(`INSERT INTO classes (id, name, grade, owner_id) VALUES (1, '7A', 7, 1)`);
  r.exec(`INSERT INTO students (id, class_id, surname, first_name) VALUES ('s1',1,'A','One'),('s2',1,'B','Two'),('s3',1,'C','Three')`);
  r.exec(`INSERT INTO tests (id, title, owner_id) VALUES (1, 'Monthly', 1)`);
  r.exec(`INSERT INTO test_questions (id, test_id, order_no, stem_text, options_json, correct_index, points) VALUES
    (1,1,1,'1+1?','["1","2","3"]',1,1),
    (2,1,2,'2+2? ដូចក្នុងរូប','["3","4","5"]',1,2)`);
  r.exec(`INSERT INTO test_questions (id, test_id, order_no, stem_text, options_json, correct_index, points, kind) VALUES (3,1,3,'Prove','[]',0,5,'writing')`);
  r.exec(`INSERT INTO test_sessions (id, test_id, class_id, scheduled_start, duration_minutes, scheduled_end, pin) VALUES (1,1,1,'2026-10-01T01:00:00Z',60,'2026-10-01T02:00:00Z','1234')`);
  return env;
}
const attempt = (env) => {
  env.raw.exec(`INSERT INTO results (session_id, student_id, mcq_score, mcq_max, started_at, submitted_at) VALUES (1,'s1',0,0,datetime('now'),datetime('now')),(1,'s2',0,0,datetime('now'),datetime('now'))`);
  env.raw.exec(`INSERT INTO responses (session_id, student_id, question_id, selected_index) VALUES (1,'s1',1,1),(1,'s1',2,1),(1,'s2',1,0),(1,'s2',2,1)`);
};

test('questions stay live until a student starts, then freeze', async () => {
  const env = await seed();
  assert.equal((await sessionQuestions(env, 1, 1))[0].stem_text, '1+1?');
  env.raw.exec(`UPDATE test_questions SET stem_text = 'fixed typo' WHERE id = 1`);
  assert.equal((await sessionQuestions(env, 1, 1))[0].stem_text, 'fixed typo');   // before the exam: edits count
  assert.equal(await isFrozen(env, 1), false);
  attempt(env);
  assert.equal((await sessionQuestions(env, 1, 1))[0].stem_text, 'fixed typo');
  assert.equal(await isFrozen(env, 1), true);
  env.raw.exec(`UPDATE test_questions SET stem_text = 'edited after exam', options_json = '["x","y"]', correct_index = 0 WHERE id = 1`);
  const q = (await sessionQuestions(env, 1, 1))[0];
  assert.equal(q.stem_text, 'fixed typo');                                        // history unchanged
  assert.equal(q.correct_index, 1);
});

test('rescoring uses the frozen copy; a deliberate key correction reaches it', async () => {
  const env = await seed();
  attempt(env);
  await sessionQuestions(env, 1, 1);                                              // freezes
  env.raw.exec(`UPDATE test_questions SET correct_index = 0 WHERE id = 1`);       // silent edit of the live question
  await rescoreSession(env, 1);
  const score = (id) => env.raw.prepare(`SELECT mcq_score, mcq_max FROM results WHERE student_id = ?`).get(id);
  assert.deepEqual({ ...score('s1') }, { mcq_score: 3, mcq_max: 3 });             // unchanged: still marked against the frozen key
  assert.deepEqual({ ...score('s2') }, { mcq_score: 2, mcq_max: 3 });
  await syncKeyToFrozen(env, 1, { correct_index: 0 });                            // teacher's deliberate correction
  await rescoreSession(env, 1);
  assert.equal(score('s1').mcq_score, 2);
  assert.equal(score('s2').mcq_score, 3);
});

test('readiness catches bad choices, missing pictures and a bad PIN', async () => {
  const env = await seed();
  env.raw.exec(`UPDATE test_questions SET correct_index = 7 WHERE id = 1`);
  env.raw.exec(`UPDATE test_questions SET image_key = 'gone' WHERE id = 2`);
  const r = await checkReadiness(env, { testId: 1, classId: 1, startIso: new Date(Date.now() + 3600e3).toISOString(), endIso: new Date(Date.now() + 7200e3).toISOString(), durationMin: 60, pin: '!' });
  const level = (id) => r.checks.find((c) => c.id === id)?.level;
  assert.equal(level('choices'), 'error');
  assert.equal(level('images'), 'error');
  assert.equal(level('pin'), 'error');
  assert.equal(level('roster'), 'ok');
  assert.equal(r.ready, false);
  env.raw.exec(`UPDATE test_questions SET correct_index = 1, image_key = NULL WHERE id IN (1,2)`);
  const ok = await checkReadiness(env, { testId: 1, classId: 1, startIso: new Date(Date.now() + 3600e3).toISOString(), endIso: new Date(Date.now() + 7200e3).toISOString(), durationMin: 60, pin: '4321' });
  assert.equal(ok.ready, true);
  assert.ok(ok.checks.some((c) => c.id === 'diagram' && c.level === 'warn'));     // "ដូចក្នុងរូប" with no picture
});

test('restore: verify is read-only, apply puts back only what is missing, and is repeatable', async () => {
  const env = await seed();
  attempt(env);
  await sessionQuestions(env, 1, 1);
  await runBackup(env, { reason: 'test' });
  const file = await getBackupFile(env, 1);
  const backup = validateBackup(await gunzipJson(file.bytes));

  // disaster: a student, their results and answers vanish; another row is edited since
  env.raw.exec(`DELETE FROM responses WHERE student_id = 's2'`);
  env.raw.exec(`DELETE FROM results WHERE student_id = 's2'`);
  env.raw.exec(`DELETE FROM students WHERE id = 's3'`);
  env.raw.exec(`UPDATE students SET first_name = 'Edited' WHERE id = 's1'`);

  const plan = await planRestore(env, backup);
  const miss = Object.fromEntries(plan.tables.map((t) => [t.table, t.missing]));
  assert.equal(miss.students, 1); assert.equal(miss.results, 1); assert.equal(miss.responses, 2);
  assert.equal(env.raw.prepare('SELECT COUNT(*) AS n FROM students').get().n, 2);   // verify wrote nothing

  const done = await applyRestore(env, backup);
  assert.equal(done.total_inserted, 4);
  assert.equal(env.raw.prepare('SELECT COUNT(*) AS n FROM students').get().n, 3);
  assert.equal(env.raw.prepare('SELECT COUNT(*) AS n FROM responses').get().n, 4);
  assert.equal(env.raw.prepare(`SELECT first_name FROM students WHERE id = 's1'`).get().first_name, 'Edited');   // newer work untouched

  assert.equal((await planRestore(env, backup)).total_missing, 0);
  assert.equal((await applyRestore(env, backup, { backupFirst: false })).total_inserted, 0);
});

test('restore skips rows whose parent no longer exists instead of failing', async () => {
  const env = await seed();
  attempt(env);
  await runBackup(env, { reason: 'test' });
  const backup = validateBackup(await gunzipJson((await getBackupFile(env, 1)).bytes));
  backup.tables.students = backup.tables.students.filter((s) => s.id !== 's2');   // pretend the backup lacks s2's profile
  env.raw.exec(`DELETE FROM responses WHERE student_id = 's2'`);
  env.raw.exec(`DELETE FROM results WHERE student_id = 's2'`);
  env.raw.exec(`DELETE FROM students WHERE id = 's2'`);
  const done = await applyRestore(env, backup, { backupFirst: false });
  assert.equal(done.tables.find((t) => t.table === 'results').skipped, 1);
  assert.equal(env.raw.prepare('SELECT COUNT(*) AS n FROM results').get().n, 1);
});
