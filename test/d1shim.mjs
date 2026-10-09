// Minimal D1 look-alike over node:sqlite, so the real library code can be tested offline.
import { DatabaseSync } from 'node:sqlite';
import { readFileSync } from 'node:fs';

// D1 uses ?1 ?2 numbered parameters; node:sqlite treats those as *named*, so map them to :p1 :p2.
const toNamed = (sql, v) => {
  const used = new Set([...sql.matchAll(/\?(\d+)/g)].map((m) => Number(m[1])));
  const obj = {};
  for (const n of used) obj[`p${n}`] = v[n - 1] ?? null;
  return [sql.replace(/\?(\d+)/g, ':p$1'), used.size ? [obj] : []];
};
class Stmt {
  constructor(db, sql) { this.db = db; this.sql = sql; this.v = []; }
  _p() { const [sql, args] = toNamed(this.sql, this.v); return [this.db.prepare(sql), args]; }
  bind(...v) { this.v = v.map((x) => (x === undefined ? null : x)); return this; }
  _run() {
    const [st, a] = this._p();
    if (/^\s*(SELECT|PRAGMA|WITH)/i.test(this.sql)) return { results: st.all(...a), meta: { changes: 0 } };   // D1's batch returns rows for reads
    const r = st.run(...a); return { results: [], meta: { changes: Number(r.changes), rows_written: Number(r.changes), last_row_id: Number(r.lastInsertRowid) } }; }
  async run() { return this._run(); }
  async first() { const [st, a] = this._p(); return st.get(...a) ?? null; }
  async all() { const [st, a] = this._p(); return { results: st.all(...a), meta: {} }; }
}
export function makeEnv(schemaPath) {
  const db = new DatabaseSync(':memory:');
  db.exec('PRAGMA foreign_keys = ON');
  db.exec(readFileSync(schemaPath, 'utf8'));
  const DB = {
    prepare: (sql) => new Stmt(db, sql),
    async batch(stmts) { db.exec('BEGIN'); try { const out = stmts.map((s) => s._run()); db.exec('COMMIT'); return out; } catch (e) { db.exec('ROLLBACK'); throw e; } },
  };
  return { DB, raw: db };
}
