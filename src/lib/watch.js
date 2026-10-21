// What runs every 10 minutes: a backup right before an exam starts, and a message to the owner when the system starts failing.
import { runBackup } from './backup.js';
import { notifyOwner } from './notify.js';

export async function ensureErrorLog(env) {
  await env.DB.prepare('CREATE TABLE IF NOT EXISTS error_log (id INTEGER PRIMARY KEY AUTOINCREMENT, at TEXT NOT NULL DEFAULT (datetime(\'now\')), path TEXT, status INTEGER, message TEXT)').run();
}
// best effort: logging an error must never raise another one
export async function logError(env, path, status, message) {
  try {
    await ensureErrorLog(env);
    await env.DB.prepare('INSERT INTO error_log (path, status, message) VALUES (?1, ?2, ?3)').bind(String(path).slice(0, 120), status, String(message || '').slice(0, 300)).run();
    await env.DB.prepare("DELETE FROM error_log WHERE at < datetime('now', '-3 days')").run();
  } catch { /* nothing more to do */ }
}

export async function watch(env) {
  const out = { backups: [], alert: false };
  // 1. an exam starts within 30 minutes and has no backup of its own yet
  const { results: soon } = await env.DB.prepare(
    "SELECT id FROM test_sessions WHERE status != 'closed' AND scheduled_start > ?1 AND scheduled_start <= ?2",
  ).bind(new Date(Date.now() - 5 * 60000).toISOString(), new Date(Date.now() + 30 * 60000).toISOString()).all();
  for (const s of soon) {
    const done = await env.DB.prepare("SELECT 1 FROM audit_log WHERE action = 'backup' AND detail LIKE ?1").bind(`pre-exam ${s.id}:%`).first();
    if (!done) { await runBackup(env, { reason: `pre-exam ${s.id}` }); out.backups.push(s.id); }
  }
  // 2. the system is failing: 10 or more server errors in the last 10 minutes (at most one message per 30 minutes)
  await ensureErrorLog(env);
  const e = await env.DB.prepare("SELECT COUNT(*) n, MAX(path) p, MAX(message) m FROM error_log WHERE at >= datetime('now', '-10 minutes')").first();
  if (e && e.n >= 10) {
    const last = await env.DB.prepare("SELECT value FROM settings WHERE key = 'last_error_alert'").first();
    if (!last || Date.now() - Number(last.value) > 30 * 60000) {
      await env.DB.prepare("INSERT INTO settings (key, value) VALUES ('last_error_alert', ?1) ON CONFLICT(key) DO UPDATE SET value = ?1").bind(String(Date.now())).run();
      await notifyOwner(env, `⚠️ exam.khmermath.org: ${e.n} server errors in 10 minutes (e.g. ${e.p}: ${String(e.m).slice(0, 120)})`);
      out.alert = true;
    }
  }
  return out;
}
