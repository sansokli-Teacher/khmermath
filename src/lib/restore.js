// Restore from a whole-system backup (see backup.js). The safe mode only puts back
// rows that are MISSING from the live database — it never overwrites or deletes
// anything, so it can recover accidentally deleted classes, students, sessions and
// results without undoing newer work. Always verify first (dry run), and a fresh
// backup is taken automatically before anything is written.
// For rolling the *whole* database back in time, see RESTORE.md (D1 Time Travel).
import { ensureColumns } from './schema.js';
import { runBackup } from './backup.js';

// [table, primary key columns, [[fk column, parent table, parent column]]] — parents first.
const PLAN = [
  ['classes', ['id'], []],
  ['students', ['id'], [['class_id', 'classes', 'id']]],
  ['tests', ['id'], []],
  ['test_questions', ['id'], [['test_id', 'tests', 'id']]],
  ['test_sessions', ['id'], [['test_id', 'tests', 'id'], ['class_id', 'classes', 'id']]],
  ['session_questions', ['session_id', 'question_id'], []],
  ['results', ['id'], [['session_id', 'test_sessions', 'id'], ['student_id', 'students', 'id']]],
  ['responses', ['id'], [['session_id', 'test_sessions', 'id'], ['student_id', 'students', 'id'], ['question_id', 'test_questions', 'id']]],
  ['writing_marks', ['session_id', 'student_id', 'question_id'], []],
  ['assessments', ['id'], []],
  ['manual_scores', ['assessment_id', 'student_id'], []],
  ['question_notes', ['id'], []],
  ['exam_events', ['id'], []],
  ['session_notes', ['id'], []],
  ['shares', ['id'], []],
];

export async function gunzipJson(bytes) {
  const stream = new Blob([bytes]).stream().pipeThrough(new DecompressionStream('gzip'));
  return JSON.parse(await new Response(stream).text());
}

export function validateBackup(b) {
  if (!b || typeof b !== 'object' || b.app !== 'exam.khmermath.org' || !b.tables || typeof b.tables !== 'object') {
    throw new Error('នេះមិនមែនជាឯកសារបម្រុងទុករបស់ប្រព័ន្ធប្រឡងទេ។');
  }
  for (const [name, rows] of Object.entries(b.tables)) if (!Array.isArray(rows)) throw new Error(`តារាង ${name} ខូច។`);
  return b;
}

const keyOf = (row, cols) => cols.map((c) => String(row[c])).join('\u0001');

async function tableExists(env, name) {
  return !!(await env.DB.prepare("SELECT 1 AS x FROM sqlite_master WHERE type = 'table' AND name = ?1").bind(name).first());
}
async function liveColumns(env, name) {
  const { results } = await env.DB.prepare(`PRAGMA table_info(${name})`).all();
  return results.map((r) => r.name);
}
async function livePks(env, name, pk) {
  if (!(await tableExists(env, name))) return new Set();
  const { results } = await env.DB.prepare(`SELECT ${pk.join(', ')} FROM ${name}`).all();
  return new Set(results.map((r) => keyOf(r, pk)));
}

// What would a restore do? Nothing is written.
export async function planRestore(env, backup) {
  await ensureColumns(env);
  const ids = {};                                        // parent id sets: live ∪ backup
  for (const [name, pk] of PLAN) {
    ids[name] = await livePks(env, name, pk);
    for (const r of backup.tables[name] || []) ids[name].add(keyOf(r, pk));
  }
  const tables = [];
  for (const [name, pk, fks] of PLAN) {
    const rows = backup.tables[name] || [];
    const live = await livePks(env, name, pk);
    let missing = 0, orphans = 0;
    for (const r of rows) {
      if (live.has(keyOf(r, pk))) continue;
      if (fks.some(([col, parent]) => r[col] != null && !ids[parent].has(String(r[col])))) { orphans++; continue; }
      missing++;
    }
    tables.push({ table: name, in_backup: rows.length, in_live: live.size, missing, orphans });
  }
  return { exported_at: backup.exported_at, tables, total_missing: tables.reduce((t, x) => t + x.missing, 0), total_orphans: tables.reduce((t, x) => t + x.orphans, 0) };
}

export async function applyRestore(env, backup, { backupFirst = true } = {}) {
  await ensureColumns(env);
  if (backupFirst) await runBackup(env, { reason: 'before-restore' });
  const ids = {};
  for (const [name, pk] of PLAN) {
    ids[name] = await livePks(env, name, pk);
    for (const r of backup.tables[name] || []) ids[name].add(keyOf(r, pk));
  }
  const out = [];
  for (const [name, pk, fks] of PLAN) {
    if (!(await tableExists(env, name))) { out.push({ table: name, inserted: 0, skipped: 0 }); continue; }
    const cols = await liveColumns(env, name);
    const live = await livePks(env, name, pk);
    const stmts = [];
    let skipped = 0;
    for (const r of backup.tables[name] || []) {
      if (live.has(keyOf(r, pk))) continue;
      if (fks.some(([col, parent]) => r[col] != null && !ids[parent].has(String(r[col])))) { skipped++; continue; }
      const use = cols.filter((c) => c in r);
      stmts.push(env.DB.prepare(`INSERT OR IGNORE INTO ${name} (${use.join(', ')}) VALUES (${use.map((_, i) => `?${i + 1}`).join(', ')})`).bind(...use.map((c) => r[c] ?? null)));
    }
    let inserted = 0;
    for (let i = 0; i < stmts.length; i += 40) {
      const res = await env.DB.batch(stmts.slice(i, i + 40));
      inserted += res.reduce((t, x) => t + (x.meta.changes || 0), 0);
    }
    out.push({ table: name, inserted, skipped });
  }
  // pictures, when the backup carries them (full backups from Telegram do; the stored slim one does not)
  let images = 0;
  for (const im of backup.tables.images || []) {
    if (!im.data_base64) continue;
    const r = await env.DB.prepare('INSERT OR IGNORE INTO images (key, content_type, data_base64) VALUES (?1, ?2, ?3)').bind(im.key, im.content_type, im.data_base64).run();
    images += r.meta.changes || 0;
  }
  await env.DB.prepare("INSERT INTO audit_log (action, detail) VALUES ('restore', ?1)")
    .bind(`from backup ${backup.exported_at}: ${out.map((t) => `${t.table}+${t.inserted}`).join(' ')} images+${images}`).run();
  return { tables: out, images, total_inserted: out.reduce((t, x) => t + x.inserted, 0) };
}

// Is the newest stored backup actually usable? Run weekly after the backup itself, and on demand.
export async function selfCheck(env) {
  await ensureColumns(env);
  const row = await env.DB.prepare('SELECT id, at, data_b64 FROM backups ORDER BY id DESC LIMIT 1').first();
  if (!row) return { ok: false, problem: 'no stored backup' };
  try {
    const bin = atob(row.data_b64); const bytes = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
    const backup = validateBackup(await gunzipJson(bytes));
    const plan = await planRestore(env, backup);
    const inBackup = Object.fromEntries(plan.tables.map((t) => [t.table, t.in_backup]));
    const live = await env.DB.prepare('SELECT (SELECT COUNT(*) FROM students) AS s, (SELECT COUNT(*) FROM results) AS r').first();
    if (live.s > 0 && !inBackup.students) return { ok: false, id: row.id, at: row.at, problem: 'backup has no students but the live system does' };
    return { ok: true, id: row.id, at: row.at, tables: inBackup, missing_from_live: plan.total_missing };
  } catch (e) { return { ok: false, id: row.id, at: row.at, problem: String(e.message || e) }; }
}
