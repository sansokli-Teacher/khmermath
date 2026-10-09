# Restoring exam.khmermath.org

Three levels, from gentlest to most drastic. Try them in this order.

## 1. Put back rows that were deleted (in the app, owner only)

Settings → **♻ ស្ដារទិន្នន័យពីការបម្រុងទុក**

1. Pick a stored backup (newest 4 are kept) **or** upload a `.json.gz` file (the full file Telegram sends every Monday, which also contains pictures).
2. **🔍 ផ្ទៀងផ្ទាត់** — a dry run. Writes nothing. Shows, per table, how many rows are in the backup, in the live system, and how many are *missing* (restorable) or *orphaned* (their parent class/student/session is gone from both, so they are skipped).
3. **♻ ស្ដារទិន្នន័យដែលបាត់** — inserts only the missing rows. It never overwrites or deletes anything, so work done since the backup is untouched. A fresh backup (`before-restore`) is taken first and the action is recorded in the audit log.

Repeating step 3 is safe: the second run inserts 0 rows.

What it cannot do: undo *edits* (an existing row keeps its current values), restore teacher accounts / password hashes / licence codes (deliberately left out of backups), or restore pictures from the stored copy (stored copies are slim; use the Telegram file for pictures).

## 2. Roll the whole database back in time (Cloudflare D1 Time Travel)

D1 keeps 30 days of point-in-time history. From `~/Exam_Khmer`:

```sh
npx wrangler d1 time-travel info exam-khmer                      # shows the current bookmark
npx wrangler d1 time-travel restore exam-khmer --timestamp=2026-10-09T08:00:00Z
```

This replaces the **entire** database with how it was at that moment — including students' answers submitted since. Do it only when level 1 is not enough, and never in the middle of an exam. `restore` prints the previous bookmark; keep it, because restoring to that bookmark undoes the rollback.

## 3. Rebuild from a file by hand

`.json.gz` → `gunzip` → one JSON object `{ exported_at, tables: { students: [...], ... } }`. Rows can be re-inserted with `INSERT OR IGNORE` in this order: classes, students, tests, test_questions, test_sessions, session_questions, results, responses, writing_marks.

## Testing the restore

`npm test` runs `test/exam.test.mjs` against a real SQLite copy of the schema (Node 22+): it takes a real backup, deletes students/results/answers, edits another row, then checks that verify writes nothing, apply restores exactly the missing rows, newer edits survive, a second apply inserts nothing, and orphaned rows are skipped rather than failing. Run it before each deploy. Do a real dry run (step 1.2) once a month on production: it proves the stored backup can be read.
