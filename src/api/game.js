// Team-game question bank: public read for the games, owner-only edits.
//   GET  /api/game/bank       public — the bank both games play (enabled lessons, fixes applied, hidden questions removed)
//   GET  /api/game/admin      teacher — everything, for the editor
//   POST /api/game/question   owner  — save a fix to one question  { lesson, i, fields, off }
//   POST /api/game/reset      owner  — remove the fix (back to the base question)  { lesson, i }
//   POST /api/game/config     owner  — which lessons the games offer + a master switch  { enabled, lessons }
import { json, err } from '../lib/http.js';
import { authTeacher, needAdmin } from '../lib/access.js';
import { audit } from '../lib/audit.js';
import { mergeBank, cleanEdit, baseKey } from '../lib/gamebank.js';

let tableReady = false;
async function ensureTable(env) {
  if (tableReady) return;
  await env.DB.batch([
    env.DB.prepare(`CREATE TABLE IF NOT EXISTS game_edits (
      lesson INTEGER NOT NULL, idx INTEGER NOT NULL, bq TEXT NOT NULL, data TEXT NOT NULL, off INTEGER NOT NULL DEFAULT 0,
      updated_at TEXT NOT NULL DEFAULT (datetime('now')), updated_by TEXT, PRIMARY KEY (lesson, idx))`),
  ]);
  tableReady = true;
}
export function _resetGameForTests() { tableReady = false; }

async function loadBase(req, env) {
  const r = await env.ASSETS.fetch(new Request(new URL('/data/teamgame_g7.json', req.url)));
  if (!r.ok) throw new Error('Question bank file is missing.');
  return r.json();
}
async function loadEdits(env) {
  await ensureTable(env);
  const { results } = await env.DB.prepare('SELECT lesson, idx, bq, data, off, updated_at FROM game_edits').all();
  const m = new Map();
  for (const r of results) m.set(`${r.lesson}:${r.idx}`, { bq: r.bq, data: JSON.parse(r.data), off: !!r.off, at: r.updated_at });
  return m;
}
async function loadCfg(env) {
  const row = await env.DB.prepare("SELECT value FROM settings WHERE key = 'game_config'").first();
  let c = {};
  try { c = row ? JSON.parse(row.value) : {}; } catch { c = {}; }
  return { enabled: c.enabled !== false, lessons: Array.isArray(c.lessons) ? c.lessons : null };
}

// khmermath.org plays the same bank, so it may read it from the browser
const ORIGINS = ['https://khmermath.org', 'https://www.khmermath.org'];
function cors(req) {
  const o = req.headers.get('Origin');
  return o && ORIGINS.includes(o) ? { 'Access-Control-Allow-Origin': o, Vary: 'Origin' } : { Vary: 'Origin' };
}

export async function bank(req, env) {
  const [base, edits, cfg] = await Promise.all([loadBase(req, env), loadEdits(env), loadCfg(env)]);
  const out = mergeBank(base, edits, cfg);
  out.closed = !cfg.enabled;
  return json(out, 200, { 'Cache-Control': 'public, max-age=20', ...cors(req) });
}

export async function admin(req, env) {
  const t = await authTeacher(req, env);
  if (!t) return err('Not logged in.', 401);
  const [base, edits, cfg] = await Promise.all([loadBase(req, env), loadEdits(env), loadCfg(env)]);
  const out = mergeBank(base, edits, cfg, { admin: true });
  out.config = { enabled: cfg.enabled, lessons: cfg.lessons };
  out.can_edit = t.role === 'owner';
  return json(out);
}

async function target(req, env, b) {
  const lesson = Number(b.lesson), i = Number(b.i);
  const base = await loadBase(req, env);
  const L = base.lessons.find((x) => x.n === lesson);
  const q = L && Number.isInteger(i) ? L.qs[i] : null;
  return q ? { lesson, i, q } : null;
}

export async function saveQuestion(req, env) {
  const g = await needAdmin(req, env); if (g.resp) return g.resp;
  const b = await req.json();
  const tg = await target(req, env, b);
  if (!tg) return err('រកមិនឃើញសំណួរ។', 404);
  const { data, error } = cleanEdit(b.fields, tg.q);
  if (error) return err(error, 400);
  await ensureTable(env);
  await env.DB.prepare(
    `INSERT INTO game_edits (lesson, idx, bq, data, off, updated_at, updated_by) VALUES (?1, ?2, ?3, ?4, ?5, datetime('now'), ?6)
     ON CONFLICT(lesson, idx) DO UPDATE SET bq = ?3, data = ?4, off = ?5, updated_at = datetime('now'), updated_by = ?6`,
  ).bind(tg.lesson, tg.i, baseKey(tg.q), JSON.stringify(data), b.off ? 1 : 0, g.t.username).run();
  await audit(env, g.t, 'game.edit', `lesson ${tg.lesson} q${tg.i + 1}${b.off ? ' (hidden)' : ''}`);
  return json({ ok: true });
}

export async function resetQuestion(req, env) {
  const g = await needAdmin(req, env); if (g.resp) return g.resp;
  const b = await req.json();
  await ensureTable(env);
  await env.DB.prepare('DELETE FROM game_edits WHERE lesson = ?1 AND idx = ?2').bind(Number(b.lesson), Number(b.i)).run();
  await audit(env, g.t, 'game.reset', `lesson ${b.lesson} q${Number(b.i) + 1}`);
  return json({ ok: true });
}

export async function saveConfig(req, env) {
  const g = await needAdmin(req, env); if (g.resp) return g.resp;
  const b = await req.json();
  const lessons = Array.isArray(b.lessons) ? [...new Set(b.lessons.map(Number).filter((n) => Number.isInteger(n) && n >= 1 && n <= 99))].sort((a, c) => a - c) : null;
  const value = JSON.stringify({ enabled: b.enabled !== false, lessons });
  await env.DB.prepare("INSERT INTO settings (key, value) VALUES ('game_config', ?1) ON CONFLICT(key) DO UPDATE SET value = ?1").bind(value).run();
  await audit(env, g.t, 'game.config', value);
  return json({ ok: true });
}
