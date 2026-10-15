// Live quiz on students' phones. A teacher opens a room in the exam system; students join from exam.khmermath.org/live or
// khmermath.org/play/live.html with the 6-digit code. State lives in D1 and phones poll it (no WebSockets needed).
//   teacher (logged in): POST /api/live/create · GET /api/live/host/:code · POST /api/live/host/:code/action
//   students (public, CORS): POST /api/live/join · GET /api/live/state · POST /api/live/answer
import { json, err } from '../lib/http.js';
import { authTeacher } from '../lib/access.js';
import { audit } from '../lib/audit.js';
import { mergeBank } from '../lib/gamebank.js';
import { loadBase, loadEdits, loadCfg, cors } from './game.js';
import { classify, isCorrect, points, newCode } from '../lib/livequiz.js';

let ready = false;
async function ensureTables(env) {
  if (ready) return;
  await env.DB.batch([
    env.DB.prepare(`CREATE TABLE IF NOT EXISTS live_rooms (code TEXT PRIMARY KEY, owner_id INTEGER, title TEXT, secs INTEGER NOT NULL, phase TEXT NOT NULL DEFAULT 'lobby',
      qi INTEGER NOT NULL DEFAULT -1, qstart INTEGER, total INTEGER NOT NULL, created_at INTEGER NOT NULL)`),
    env.DB.prepare('CREATE TABLE IF NOT EXISTS live_qs (code TEXT NOT NULL, qi INTEGER NOT NULL, pub TEXT NOT NULL, key TEXT NOT NULL, PRIMARY KEY (code, qi))'),
    env.DB.prepare('CREATE TABLE IF NOT EXISTS live_players (code TEXT NOT NULL, pid INTEGER NOT NULL, name TEXT NOT NULL, token TEXT NOT NULL, score INTEGER NOT NULL DEFAULT 0, PRIMARY KEY (code, pid))'),
    env.DB.prepare('CREATE TABLE IF NOT EXISTS live_answers (code TEXT NOT NULL, qi INTEGER NOT NULL, pid INTEGER NOT NULL, choice TEXT NOT NULL, ms INTEGER NOT NULL, pts INTEGER, PRIMARY KEY (code, qi, pid))'),
  ]);
  for (const sql of ["ALTER TABLE live_rooms ADD COLUMN mode TEXT NOT NULL DEFAULT 'classic'", 'ALTER TABLE live_players ADD COLUMN cur INTEGER NOT NULL DEFAULT 0', 'ALTER TABLE live_players ADD COLUMN qstart INTEGER', "ALTER TABLE live_players ADD COLUMN avatar TEXT NOT NULL DEFAULT ''"]) {
    try { await env.DB.prepare(sql).run(); } catch { /* column already there */ }
  }
  ready = true;
}
export function _resetLiveForTests() { ready = false; }

const AV = [6, 5, 6, 4, 4];            // background, skin, head-dress, outfit, extra — see public/js/avatar.js
const okAvatar = (a) => { const t = String(a || '').split('-').map(Number); return t.length === 5 && t.every((n, i) => Number.isInteger(n) && n >= 0 && n < AV[i]); };
const DAY = 24 * 3600 * 1000;
const rid = () => Array.from(crypto.getRandomValues(new Uint8Array(12)), (b) => b.toString(16).padStart(2, '0')).join('');
const pubJson = (data, req, status = 200) => json(data, status, cors(req));
const room = (env, code) => env.DB.prepare('SELECT * FROM live_rooms WHERE code = ?1').bind(String(code)).first();
const left = (r) => (r.phase === 'question' ? Math.max(0, r.qstart + r.secs * 1000 - Date.now()) : 0);

async function top(env, code, n) {
  const { results } = await env.DB.prepare('SELECT name, score, avatar FROM live_players WHERE code = ?1 ORDER BY score DESC, pid ASC LIMIT ?2').bind(code, n).all();
  return results;
}

// ------------------------------------------------------------------ teacher
export async function create(req, env) {
  const t = await authTeacher(req, env);
  if (!t) return err('Not logged in.', 401);
  await ensureTables(env);
  const cfg = await loadCfg(env);
  if (cfg.games.live === false) return err('ហ្គេមនេះត្រូវបានបិទ។ សូមបើកវាក្នុង «សំណួរហ្គេម» ជាមុនសិន។', 403);
  const b = await req.json();
  const lessons = Array.isArray(b.lessons) ? b.lessons.map(Number) : [];
  const mode = b.mode === 'solo' ? 'solo' : 'classic';
  const want = Math.max(3, Math.min(40, Number(b.count) || 15)), secs = [15, 20, 30, 45, 60, 90].includes(Number(b.secs)) ? Number(b.secs) : 30;
  const [base, edits] = await Promise.all([loadBase(req, env), loadEdits(env)]);
  const bank = mergeBank(base, edits, { enabled: true, lessons: lessons.length ? lessons : null });
  const pool = [];
  for (const L of bank.lessons) for (const q of L.qs) { const c = classify(q); if (c) pool.push(c); }
  if (pool.length < 3) return err('មេរៀនដែលបានជ្រើសមានសំណួរតិចពេក (ត្រូវការយ៉ាងតិច ៣ សំណួរដែលពិនិត្យដោយស្វ័យប្រវត្តិបាន)។', 400);
  for (let i = pool.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [pool[i], pool[j]] = [pool[j], pool[i]]; }
  const picked = pool.slice(0, want);
  // tidy: forget rooms older than two days
  const old = Date.now() - 2 * DAY;
  await env.DB.batch(['live_answers', 'live_players', 'live_qs'].map((tb) => env.DB.prepare(`DELETE FROM ${tb} WHERE code IN (SELECT code FROM live_rooms WHERE created_at < ?1)`).bind(old))
    .concat([env.DB.prepare('DELETE FROM live_rooms WHERE created_at < ?1').bind(old)]));
  let code = newCode();
  for (let k = 0; k < 8 && (await room(env, code)); k++) code = newCode();
  await env.DB.batch([
    env.DB.prepare('INSERT INTO live_rooms (code, owner_id, title, secs, total, created_at, mode, phase, qi) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9)').bind(code, t.id, String(b.title || '').slice(0, 80), secs, picked.length, Date.now(), mode, 'lobby', mode === 'solo' ? 0 : -1),
    ...picked.map((c, i) => env.DB.prepare('INSERT INTO live_qs (code, qi, pub, key) VALUES (?1, ?2, ?3, ?4)').bind(code, i, JSON.stringify(c.pub), JSON.stringify(c.key))),
  ]);
  await audit(env, t, 'live.create', `room ${code}, ${picked.length} questions`);
  return json({ code, total: picked.length, secs, available: pool.length, mode });
}

async function mine(req, env, code) {
  const t = await authTeacher(req, env);
  if (!t) return { resp: err('Not logged in.', 401) };
  await ensureTables(env);
  const r = await room(env, code);
  if (!r || (r.owner_id !== t.id && t.role !== 'owner')) return { resp: err('រកមិនឃើញបន្ទប់។', 404) };
  return { t, r };
}

export async function hostState(req, env, params) {
  const g = await mine(req, env, params.code); if (g.resp) return g.resp;
  const r = g.r;
  const players = (await env.DB.prepare('SELECT pid, name, score, avatar FROM live_players WHERE code = ?1 ORDER BY pid').bind(r.code).all()).results;
  if (r.mode === 'solo') {
    const { results } = await env.DB.prepare('SELECT pid, name, score, cur, avatar FROM live_players WHERE code = ?1 ORDER BY score DESC, pid ASC').bind(r.code).all();
    return json({ code: r.code, mode: 'solo', phase: r.phase, total: r.total, secs: r.secs, players: results.length, finished: results.filter((p) => p.cur >= r.total).length, board: results.slice(0, 200), plist: results.map((p) => ({ pid: p.pid, name: p.name, avatar: p.avatar })) });
  }
  const out = { code: r.code, mode: 'classic', phase: r.phase, qi: r.qi, total: r.total, secs: r.secs, left: left(r), players: players.length, names: players.map((p) => p.name), plist: players.map((p) => ({ pid: p.pid, name: p.name, avatar: p.avatar })), top: await top(env, r.code, 10) };
  if (r.phase === 'end') out.board = await top(env, r.code, 200);
  if (r.qi >= 0 && r.phase !== 'lobby' && r.phase !== 'end') {
    const q = await env.DB.prepare('SELECT pub, key FROM live_qs WHERE code = ?1 AND qi = ?2').bind(r.code, r.qi).first();
    out.q = JSON.parse(q.pub);
    out.answered = (await env.DB.prepare('SELECT COUNT(*) n FROM live_answers WHERE code = ?1 AND qi = ?2').bind(r.code, r.qi).first()).n;
    if (r.phase === 'reveal') {
      const key = JSON.parse(q.key);
      out.reveal = { show: key.show, sol: key.sol, correct: key.correct, k: key.k };
      const { results } = await env.DB.prepare('SELECT choice, COUNT(*) n, SUM(CASE WHEN pts > 0 THEN 1 ELSE 0 END) ok FROM live_answers WHERE code = ?1 AND qi = ?2 GROUP BY choice').bind(r.code, r.qi).all();
      out.dist = results;
    }
  }
  return json(out);
}

export async function hostAction(req, env, params) {
  const g = await mine(req, env, params.code); if (g.resp) return g.resp;
  const r = g.r, body = await req.json(), a = body.a, now = Date.now();
  if (a === 'kick') {
    const pid = Number(body.pid);
    await env.DB.batch([env.DB.prepare('DELETE FROM live_answers WHERE code = ?1 AND pid = ?2').bind(r.code, pid), env.DB.prepare('DELETE FROM live_players WHERE code = ?1 AND pid = ?2').bind(r.code, pid)]);
    return json({ ok: true });
  }
  if (r.mode === 'solo' && a === 'start' && r.phase === 'lobby') {
    await env.DB.batch([env.DB.prepare("UPDATE live_rooms SET phase = 'open' WHERE code = ?1").bind(r.code), env.DB.prepare('UPDATE live_players SET cur = 0, qstart = ?2 WHERE code = ?1').bind(r.code, now)]);
    return json({ ok: true });
  }
  if (r.mode === 'solo' && a !== 'end') return err('សកម្មភាពនេះមិនអាចធ្វើបានក្នុងរបៀបលេងដោយខ្លួនឯងទេ។', 409);
  if (a === 'start' && r.phase === 'lobby') {
    await env.DB.prepare("UPDATE live_rooms SET phase = 'question', qi = 0, qstart = ?2 WHERE code = ?1").bind(r.code, now).run();
  } else if (a === 'reveal' && r.phase === 'question') {
    // grade every answer once, add the points, then show the result
    const key = JSON.parse((await env.DB.prepare('SELECT key FROM live_qs WHERE code = ?1 AND qi = ?2').bind(r.code, r.qi).first()).key);
    const { results } = await env.DB.prepare('SELECT pid, choice, ms FROM live_answers WHERE code = ?1 AND qi = ?2 AND pts IS NULL').bind(r.code, r.qi).all();
    const stmts = [];
    for (const x of results) {
      const p = points(isCorrect(key, x.choice), x.ms, r.secs);
      stmts.push(env.DB.prepare('UPDATE live_answers SET pts = ?4 WHERE code = ?1 AND qi = ?2 AND pid = ?3').bind(r.code, r.qi, x.pid, p));
      if (p) stmts.push(env.DB.prepare('UPDATE live_players SET score = score + ?3 WHERE code = ?1 AND pid = ?2').bind(r.code, x.pid, p));
    }
    stmts.push(env.DB.prepare("UPDATE live_rooms SET phase = 'reveal' WHERE code = ?1").bind(r.code));
    await env.DB.batch(stmts);
  } else if (a === 'next' && r.phase === 'reveal') {
    if (r.qi + 1 >= r.total) await env.DB.prepare("UPDATE live_rooms SET phase = 'end' WHERE code = ?1").bind(r.code).run();
    else await env.DB.prepare("UPDATE live_rooms SET phase = 'question', qi = qi + 1, qstart = ?2 WHERE code = ?1").bind(r.code, now).run();
  } else if (a === 'end') {
    await env.DB.prepare("UPDATE live_rooms SET phase = 'end' WHERE code = ?1").bind(r.code).run();
  } else return err('សកម្មភាពនេះមិនអាចធ្វើបានក្នុងដំណាក់កាលបច្ចុប្បន្នទេ។', 409);
  return json({ ok: true });
}

// ------------------------------------------------------------------ students (public)
export async function join(req, env) {
  await ensureTables(env);
  const b = await req.json().catch(() => ({}));
  const code = String(b.code || '').replace(/\D/g, '');
  let name = String(b.name || '').replace(/\s+/g, ' ').trim().slice(0, 24);
  if (!/^\d{6}$/.test(code)) return pubJson({ error: 'លេខកូដមិនត្រឹមត្រូវ។' }, req, 400);
  if (!name) return pubJson({ error: 'សូមបញ្ចូលឈ្មោះ។' }, req, 400);
  const cfg = await loadCfg(env);
  if (cfg.games.live === false) return pubJson({ error: 'គ្រូបានបិទហ្គេមនេះ។' }, req, 403);
  const r = await room(env, code);
  if (!r || Date.now() - r.created_at > DAY) return pubJson({ error: 'រកមិនឃើញបន្ទប់។ សូមពិនិត្យលេខកូដ។' }, req, 404);
  if (r.phase === 'end') return pubJson({ error: 'ហ្គេមនេះបានបញ្ចប់ហើយ។' }, req, 409);
  const ps = (await env.DB.prepare('SELECT pid, name FROM live_players WHERE code = ?1').bind(code).all()).results;
  if (ps.length >= 150) return pubJson({ error: 'បន្ទប់ពេញហើយ។' }, req, 409);
  const taken = new Set(ps.map((p) => p.name));
  if (taken.has(name)) { let k = 2; while (taken.has(`${name} ${k}`)) k++; name = `${name} ${k}`; }
  const pid = ps.reduce((m, p) => Math.max(m, p.pid), 0) + 1, token = rid();
  await env.DB.prepare('INSERT INTO live_players (code, pid, name, token, cur, qstart, avatar) VALUES (?1, ?2, ?3, ?4, 0, ?5, ?6)').bind(code, pid, name, token, Date.now(), okAvatar(b.avatar) ? b.avatar : '').run();
  return pubJson({ pid, token, name, mode: r.mode }, req);
}

async function player(env, code, pid, token) {
  const p = await env.DB.prepare('SELECT pid, name, score, token, cur, qstart, avatar FROM live_players WHERE code = ?1 AND pid = ?2').bind(code, Number(pid)).first();
  return p && p.token === token ? p : null;
}


async function soloState(req, env, r, p) {
  const code = r.code, over = r.phase === 'end' || (r.phase !== 'lobby' && p.cur >= r.total);
  if (r.phase === 'lobby') return pubJson({ mode: 'solo', phase: 'lobby', total: r.total, secs: r.secs, name: p.name, avatar: p.avatar, score: 0, qi: 0, players: (await env.DB.prepare('SELECT COUNT(*) n FROM live_players WHERE code = ?1').bind(code).first()).n }, req);
  const out = { avatar: p.avatar, mode: 'solo', phase: over ? 'end' : 'question', qi: p.cur, total: r.total, secs: r.secs, name: p.name, score: p.score };
  const better = await env.DB.prepare('SELECT COUNT(*) n FROM live_players WHERE code = ?1 AND score > ?2').bind(code, p.score).first();
  out.rank = better.n + 1; out.players = (await env.DB.prepare('SELECT COUNT(*) n FROM live_players WHERE code = ?1').bind(code).first()).n;
  if (over) { out.top = await top(env, code, 5); return pubJson(out, req); }
  const q = await env.DB.prepare('SELECT pub, key FROM live_qs WHERE code = ?1 AND qi = ?2').bind(code, p.cur).first();
  out.q = JSON.parse(q.pub);
  let a = await env.DB.prepare('SELECT choice, pts FROM live_answers WHERE code = ?1 AND qi = ?2 AND pid = ?3').bind(code, p.cur, p.pid).first();
  const used = Date.now() - (p.qstart || Date.now());
  if (!a && used > r.secs * 1000 + 1500) {          // the time ran out without an answer
    await env.DB.prepare("INSERT OR IGNORE INTO live_answers (code, qi, pid, choice, ms, pts) VALUES (?1, ?2, ?3, '', ?4, 0)").bind(code, p.cur, p.pid, used).run();
    a = { choice: '', pts: 0 };
  }
  out.left = Math.max(0, (p.qstart || 0) + r.secs * 1000 - Date.now());
  if (a) {
    const key = JSON.parse(q.key);
    out.phase = 'reveal'; out.answered = true;
    out.reveal = { show: key.show, sol: key.sol, mine: a.choice, pts: a.pts || 0, right: (a.pts || 0) > 0, correct: key.correct, k: key.k, timeout: a.choice === '' };
  }
  return pubJson(out, req);
}

export async function next(req, env) {
  await ensureTables(env);
  const b = await req.json().catch(() => ({}));
  const code = String(b.code || ''), r = await room(env, code), p = r && (await player(env, code, b.pid, b.token));
  if (!r || !p || r.mode !== 'solo') return pubJson({ error: 'gone' }, req, 404);
  const a = await env.DB.prepare('SELECT 1 x FROM live_answers WHERE code = ?1 AND qi = ?2 AND pid = ?3').bind(code, p.cur, p.pid).first();
  if (a && p.cur < r.total) await env.DB.prepare('UPDATE live_players SET cur = ?3, qstart = ?4 WHERE code = ?1 AND pid = ?2 AND cur = ?5').bind(code, p.pid, p.cur + 1, Date.now(), p.cur).run();
  return pubJson({ ok: true }, req);
}

export async function state(req, env) {
  await ensureTables(env);
  const u = new URL(req.url), code = u.searchParams.get('code') || '';
  const r = await room(env, code), p = r && (await player(env, code, u.searchParams.get('pid'), u.searchParams.get('token')));
  if (!r || !p) return pubJson({ error: 'gone' }, req, 404);
  if (r.mode === 'solo') return soloState(req, env, r, p);
  const out = { avatar: p.avatar, mode: 'classic', phase: r.phase, qi: r.qi, total: r.total, secs: r.secs, left: left(r), name: p.name, score: p.score };
  const better = await env.DB.prepare('SELECT COUNT(*) n FROM live_players WHERE code = ?1 AND score > ?2').bind(code, p.score).first();
  out.rank = better.n + 1; out.players = (await env.DB.prepare('SELECT COUNT(*) n FROM live_players WHERE code = ?1').bind(code).first()).n;
  if (r.phase === 'question' || r.phase === 'reveal') {
    const q = await env.DB.prepare('SELECT pub, key FROM live_qs WHERE code = ?1 AND qi = ?2').bind(code, r.qi).first();
    out.q = JSON.parse(q.pub);
    const a = await env.DB.prepare('SELECT choice, pts FROM live_answers WHERE code = ?1 AND qi = ?2 AND pid = ?3').bind(code, r.qi, p.pid).first();
    out.answered = !!a;
    if (r.phase === 'reveal') {
      const key = JSON.parse(q.key);
      out.reveal = { show: key.show, sol: key.sol, mine: a ? a.choice : null, pts: a ? a.pts || 0 : 0, right: a ? (a.pts || 0) > 0 : false, correct: key.correct, k: key.k };
    }
  }
  if (r.phase === 'end' || r.phase === 'reveal') out.top = await top(env, code, 5);
  return pubJson(out, req);
}

export async function answer(req, env) {
  await ensureTables(env);
  const b = await req.json().catch(() => ({}));
  const code = String(b.code || ''), r = await room(env, code), p = r && (await player(env, code, b.pid, b.token));
  if (!r || !p) return pubJson({ error: 'gone' }, req, 404);
  if (r.mode === 'solo') {
    if (r.phase === 'end' || Number(b.qi) !== p.cur || p.cur >= r.total) return pubJson({ error: 'late' }, req, 409);
    const ms = Date.now() - (p.qstart || Date.now());
    const choice = String(b.choice ?? '').slice(0, 40);
    if (!choice) return pubJson({ error: 'empty' }, req, 400);
    const have = await env.DB.prepare('SELECT 1 x FROM live_answers WHERE code = ?1 AND qi = ?2 AND pid = ?3').bind(code, p.cur, p.pid).first();
    if (have) return pubJson({ ok: true }, req);
    const key = JSON.parse((await env.DB.prepare('SELECT key FROM live_qs WHERE code = ?1 AND qi = ?2').bind(code, p.cur).first()).key);
    const pts = ms > r.secs * 1000 + 1500 ? 0 : points(isCorrect(key, choice), Math.max(0, ms), r.secs);
    const stmts = [env.DB.prepare('INSERT OR IGNORE INTO live_answers (code, qi, pid, choice, ms, pts) VALUES (?1, ?2, ?3, ?4, ?5, ?6)').bind(code, p.cur, p.pid, choice, Math.max(0, ms), pts)];
    if (pts) stmts.push(env.DB.prepare('UPDATE live_players SET score = score + ?3 WHERE code = ?1 AND pid = ?2').bind(code, p.pid, pts));
    await env.DB.batch(stmts);
    return pubJson({ ok: true }, req);
  }
  if (r.phase !== 'question' || Number(b.qi) !== r.qi) return pubJson({ error: 'late' }, req, 409);
  const ms = Date.now() - r.qstart;
  if (ms > r.secs * 1000 + 1500) return pubJson({ error: 'late' }, req, 409);
  const choice = String(b.choice ?? '').slice(0, 40);
  if (!choice) return pubJson({ error: 'empty' }, req, 400);
  await env.DB.prepare('INSERT OR IGNORE INTO live_answers (code, qi, pid, choice, ms) VALUES (?1, ?2, ?3, ?4, ?5)').bind(code, r.qi, p.pid, choice, Math.max(0, ms)).run();
  return pubJson({ ok: true }, req);
}

export async function setAvatar(req, env) {
  await ensureTables(env);
  const b = await req.json().catch(() => ({}));
  const code = String(b.code || ''), r = await room(env, code), p = r && (await player(env, code, b.pid, b.token));
  if (!r || !p) return pubJson({ error: 'gone' }, req, 404);
  if (!okAvatar(b.avatar)) return pubJson({ error: 'bad' }, req, 400);
  await env.DB.prepare('UPDATE live_players SET avatar = ?3 WHERE code = ?1 AND pid = ?2').bind(code, p.pid, b.avatar).run();
  return pubJson({ ok: true }, req);
}
