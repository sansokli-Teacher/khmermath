// Whole-system backup: every table except secrets, as a gzipped JSON file.
//  - a snapshot (without pictures) is kept in the database, newest 4
//  - the full file (with pictures) is sent to the owner's Telegram chat when configured
// Runs weekly from a cron trigger and on demand from the owner's settings.
import { ensureColumns } from './schema.js';

const TABLES = [
  ['teachers', 'id, username, role, display_name, active, plan, license_until, contact, last_login'],   // never password hashes
  ['classes', '*'], ['students', '*'], ['tests', '*'], ['test_questions', '*'], ['test_sessions', '*'],
  ['results', '*'], ['responses', '*'], ['writing_marks', '*'], ['assessments', '*'], ['manual_scores', '*'],
  ['session_questions', '*'], ['shares', '*'], ['question_notes', '*'], ['license_codes', '*'],
];
const SECRET_SETTINGS = ['telegram_token', 'student_pin_hash'];

async function gzip(text) {
  const stream = new Blob([text]).stream().pipeThrough(new CompressionStream('gzip'));
  return new Uint8Array(await new Response(stream).arrayBuffer());
}
function toBase64(bytes) {
  let bin = ''; const chunk = 0x8000;
  for (let i = 0; i < bytes.length; i += chunk) bin += String.fromCharCode(...bytes.subarray(i, i + chunk));
  return btoa(bin);
}

export async function buildBackup(env, { withImages }) {
  await ensureColumns(env);
  const out = { exported_at: new Date().toISOString(), app: 'exam.khmermath.org', tables: {} };
  for (const [name, cols] of TABLES) {
    try { out.tables[name] = (await env.DB.prepare(`SELECT ${cols} FROM ${name}`).all()).results; } catch { out.tables[name] = []; }
  }
  const settings = (await env.DB.prepare('SELECT key, value FROM settings').all()).results;
  out.tables.settings = settings.filter((s) => !SECRET_SETTINGS.includes(s.key));
  out.tables.audit_log = (await env.DB.prepare('SELECT * FROM audit_log ORDER BY id DESC LIMIT 500').all()).results;
  if (withImages) out.tables.images = (await env.DB.prepare('SELECT * FROM images').all()).results;
  else out.tables.images = (await env.DB.prepare('SELECT key, content_type FROM images').all()).results;   // list only
  return out;
}

async function sendTelegram(env, bytes, filename, caption) {
  try {
    const { results } = await env.DB.prepare("SELECT key, value FROM settings WHERE key IN ('telegram_token', 'telegram_chat_id')").all();
    const m = Object.fromEntries(results.map((r) => [r.key, r.value]));
    if (!m.telegram_token || !m.telegram_chat_id) return false;
    const form = new FormData();
    form.append('chat_id', m.telegram_chat_id);
    form.append('caption', caption);
    form.append('document', new Blob([bytes], { type: 'application/gzip' }), filename);
    const res = await fetch(`https://api.telegram.org/bot${m.telegram_token}/sendDocument`, { method: 'POST', body: form, signal: AbortSignal.timeout(20000) });
    return res.ok;
  } catch { return false; }
}

export async function runBackup(env, { reason = 'manual' } = {}) {
  await ensureColumns(env);
  const stamp = new Date().toISOString().slice(0, 16).replace(/[:T]/g, '-');
  const full = await gzip(JSON.stringify(await buildBackup(env, { withImages: true })));
  const slim = await gzip(JSON.stringify(await buildBackup(env, { withImages: false })));
  let stored = false;
  if (slim.length <= 1_300_000) {                         // keep under D1's 2 MB row limit once base64-encoded
    await env.DB.prepare('INSERT INTO backups (reason, size_bytes, data_b64) VALUES (?1, ?2, ?3)').bind(reason, slim.length, toBase64(slim)).run();
    await env.DB.prepare('DELETE FROM backups WHERE id NOT IN (SELECT id FROM backups ORDER BY id DESC LIMIT 4)').run();
    stored = true;
  }
  const sent = await sendTelegram(env, full, `exam-backup-${stamp}.json.gz`, `💾 Backup ${stamp} (${reason}) — ${(full.length / 1024).toFixed(0)} KB`);
  await env.DB.prepare("INSERT INTO audit_log (action, detail) VALUES ('backup', ?1)").bind(`${reason}: ${(full.length / 1024).toFixed(0)} KB, stored=${stored}, telegram=${sent}`).run();
  return { size_kb: Math.round(full.length / 1024), stored, telegram: sent };
}

export async function listBackups(env) {
  await ensureColumns(env);
  return (await env.DB.prepare('SELECT id, at, reason, size_bytes FROM backups ORDER BY id DESC').all()).results;
}

export async function getBackupFile(env, id) {
  const row = await env.DB.prepare('SELECT at, data_b64 FROM backups WHERE id = ?1').bind(id).first();
  if (!row) return null;
  const bin = atob(row.data_b64);
  const bytes = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
  return { at: row.at, bytes };
}
