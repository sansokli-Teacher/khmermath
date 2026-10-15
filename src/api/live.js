// Live quiz on students' phones. A teacher opens a room in the exam system; students join from exam.khmermath.org/live or
// khmermath.org/play/live.html with the 6-digit code. State lives in D1 and phones poll it (no WebSockets needed).
//   teacher (logged in): POST /api/live/create · GET /api/live/host/:code · POST /api/live/host/:code/action
//   students (public, CORS): POST /api/live/join · GET /api/live/state · POST /api/live/answer
import { json, err } from '../lib/http.js';
import { authTeacher, classAccess } from '../lib/access.js';
import { requireStudent } from '../lib/session.js';
import { audit } from '../lib/audit.js';
import { mergeBank } from '../lib/gamebank.js';
import { loadBase, loadEdits, loadCfg, cors, isLocked } from './game.js';
import { allow, clientIp } from '../lib/limits.js';
import { classify, isCorrect, points, newCode } from '../lib/livequiz.js';

let ready = false;
export async function ensureTables(env) {
  if (ready) return;
  await env.DB.batch([
    env.DB.prepare(`CREATE TABLE IF NOT EXISTS live_rooms (code TEXT PRIMARY KEY, owner_id INTEGER, title TEXT, secs INTEGER NOT NULL, phase TEXT NOT NULL DEFAULT 'lobby',
      qi INTEGER NOT NULL DEFAULT -1, qstart INTEGER, total INTEGER NOT NULL, created_at INTEGER NOT NULL)`),
    env.DB.prepare('CREATE TABLE IF NOT EXISTS live_qs (code TEXT NOT NULL, qi INTEGER NOT NULL, pub TEXT NOT NULL, key TEXT NOT NULL, PRIMARY KEY (code, qi))'),
    env.DB.prepare('CREATE TABLE IF NOT EXISTS live_players (code TEXT NOT NULL, pid INTEGER NOT NULL, name TEXT NOT NULL, token TEXT NOT NULL, score INTEGER NOT NULL DEFAULT 0, PRIMARY KEY (code, pid))'),
    env.DB.prepare('CREATE TABLE IF NOT EXISTS live_answers (code TEXT NOT NULL, qi INTEGER NOT NULL, pid INTEGER NOT NULL, choice TEXT NOT NULL, ms INTEGER NOT NULL, pts INTEGER, PRIMARY KEY (code, qi, pid))'),
  ]);
  for (const sql of ["ALTER TABLE live_rooms ADD COLUMN mode TEXT NOT NULL DEFAULT 'classic'", 'ALTER TABLE live_players ADD COLUMN cur INTEGER NOT NULL DEFAULT 0', 'ALTER TABLE live_players ADD COLUMN qstart INTEGER', "ALTER TABLE live_players ADD COLUMN avatar TEXT NOT NULL DEFAULT ''", 'ALTER TABLE live_rooms ADD COLUMN lessons TEXT', 'ALTER TABLE live_rooms ADD COLUMN class_id INTEGER', 'ALTER TABLE live_rooms ADD COLUMN deadline INTEGER', 'ALTER TABLE live_players ADD COLUMN student_id TEXT']) {
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
const closedByDeadline = (r) => !!r.deadline && Date.now() > r.deadline;
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
  if (cfg.locked) return err('ហ្គេមផ្ទាល់ត្រូវបានបិទដោយ «ថ្ងៃប្រឡង»។ សូមបិទការចាក់សោនៅ «សំណួរហ្គេម» ជាមុនសិន។', 403);
  if (cfg.games.live === false) return err('ហ្គេមនេះត្រូវបានបិទ។ សូមបើកវាក្នុង «សំណួរហ្គេម» ជាមុនសិន។', 403);
  const b = await req.json();
  const lessons = Array.isArray(b.lessons) ? b.lessons.map(Number) : [];
  const mode = b.mode === 'solo' ? 'solo' : 'classic';
  let classId = null, deadline = null;                       // homework: a self-paced room for one class, open until a deadline
  if (mode === 'solo' && b.class_id) {
    classId = Number(b.class_id);
    if (!(await classAccess(env, t, classId))) return err('អ្នកមិនមានសិទ្ធិលើថ្នាក់នេះទេ។', 403);
    deadline = Number(b.deadline);
    if (!Number.isFinite(deadline) || deadline < Date.now() + 60000 || deadline > Date.now() + 60 * DAY) return err('កាលបរិច្ឆេទផុតកំណត់មិនត្រឹមត្រូវ (ត្រូវនៅអនាគត ក្នុងរយៈ ៦០ ថ្ងៃ)។', 400);
  }
  const want = Math.max(3, Math.min(40, Number(b.count) || 15)), secs = [15, 20, 30, 45, 60, 90].includes(Number(b.secs)) ? Number(b.secs) : 30;
  const [base, edits] = await Promise.all([loadBase(req, env), loadEdits(env)]);
  const bank = mergeBank(base, edits, { enabled: true, lessons: lessons.length ? lessons : null });
  const pool = [];
  for (const L of bank.lessons) for (const q of L.qs) { const c = classify(q); if (c) pool.push(c); }
  if (pool.length < 3) return err('មេរៀនដែលបានជ្រើសមានសំណួរតិចពេក (ត្រូវការយ៉ាងតិច ៣ សំណួរដែលពិនិត្យដោយស្វ័យប្រវត្តិបាន)។', 400);
  for (let i = pool.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [pool[i], pool[j]] = [pool[j], pool[i]]; }
  const picked = pool.slice(0, want);
  // tidy: rooms are kept as the game history for about a year
  const old = Date.now() - 400 * DAY;
  await env.DB.batch(['live_answers', 'live_players', 'live_qs'].map((tb) => env.DB.prepare(`DELETE FROM ${tb} WHERE code IN (SELECT code FROM live_rooms WHERE created_at < ?1)`).bind(old))
    .concat([env.DB.prepare('DELETE FROM live_rooms WHERE created_at < ?1').bind(old)]));
  let code = newCode();
  for (let k = 0; k < 8 && (await room(env, code)); k++) code = newCode();
  await env.DB.batch([
    env.DB.prepare('INSERT INTO live_rooms (code, owner_id, title, secs, total, created_at, mode, phase, qi, lessons, class_id, deadline) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10, ?11, ?12)').bind(code, t.id, String(b.title || '').slice(0, 80), secs, picked.length, Date.now(), mode, deadline ? 'open' : 'lobby', mode === 'solo' ? 0 : -1, JSON.stringify(lessons), classId, deadline),
    ...picked.map((c, i) => env.DB.prepare('INSERT INTO live_qs (code, qi, pub, key) VALUES (?1, ?2, ?3, ?4)').bind(code, i, JSON.stringify(c.pub), JSON.stringify(c.key))),
  ]);
  await audit(env, t, 'live.create', `room ${code}, ${picked.length} questions`);
  return json({ code, total: picked.length, secs, available: pool.length, mode, homework: !!deadline });
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

// grade every answer once (nobody is scored before the reveal) and add the points
async function gradePending(env, r) {
  const key = JSON.parse((await env.DB.prepare('SELECT key FROM live_qs WHERE code = ?1 AND qi = ?2').bind(r.code, r.qi).first()).key);
  const { results } = await env.DB.prepare('SELECT pid, choice, ms FROM live_answers WHERE code = ?1 AND qi = ?2 AND pts IS NULL').bind(r.code, r.qi).all();
  const stmts = [];
  for (const x of results) {
    const p = points(isCorrect(key, x.choice), x.ms, r.secs);
    stmts.push(env.DB.prepare('UPDATE live_answers SET pts = ?4 WHERE code = ?1 AND qi = ?2 AND pid = ?3').bind(r.code, r.qi, x.pid, p));
    if (p) stmts.push(env.DB.prepare('UPDATE live_players SET score = score + ?3 WHERE code = ?1 AND pid = ?2').bind(r.code, x.pid, p));
  }
  if (stmts.length) await env.DB.batch(stmts);
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
    await gradePending(env, r);
    await env.DB.prepare("UPDATE live_rooms SET phase = 'reveal' WHERE code = ?1").bind(r.code).run();
  } else if (a === 'next' && r.phase === 'reveal') {
    if (r.qi + 1 >= r.total) await env.DB.prepare("UPDATE live_rooms SET phase = 'end' WHERE code = ?1").bind(r.code).run();
    else await env.DB.prepare("UPDATE live_rooms SET phase = 'question', qi = qi + 1, qstart = ?2 WHERE code = ?1").bind(r.code, now).run();
  } else if (a === 'end') {
    if (r.mode === 'classic' && r.phase === 'question') await gradePending(env, r);        // the question on screen still counts
    await env.DB.prepare("UPDATE live_rooms SET phase = 'end' WHERE code = ?1").bind(r.code).run();
  } else return err('សកម្មភាពនេះមិនអាចធ្វើបានក្នុងដំណាក់កាលបច្ចុប្បន្នទេ។', 409);
  return json({ ok: true });
}

// ------------------------------------------------------------------ students (public)
export async function join(req, env) {
  if (await isLocked(env)) return pubJson({ error: 'ហ្គេមផ្ទាល់ត្រូវបានបិទជាបណ្តោះអាសន្ន (ថ្ងៃប្រឡង)។' }, req, 503);
  await ensureTables(env);
  const b = await req.json().catch(() => ({}));
  const code = String(b.code || '').replace(/\D/g, '');
  let name = String(b.name || '').replace(/\s+/g, ' ').trim().slice(0, 24);
  if (!/^\d{6}$/.test(code)) return pubJson({ error: 'លេខកូដមិនត្រឹមត្រូវ។' }, req, 400);
  if (!name) return pubJson({ error: 'សូមបញ្ចូលឈ្មោះ។' }, req, 400);
  const cfg = await loadCfg(env);
  if (cfg.games.live === false) return pubJson({ error: 'គ្រូបានបិទហ្គេមនេះ។' }, req, 403);
  const r = await room(env, code);
  if (!r || Date.now() - r.created_at > DAY) {
    // a whole class shares one school IP, so only wrong codes count — 40 misses per 10 minutes is far above any honest typo rate
    if (!(await allow(env, `livejoin:${clientIp(req)}`, 40, 600))) return pubJson({ error: 'សាកល្បងច្រើនពេកហើយ។ សូមរង់ចាំបន្តិចសិន។' }, req, 429);
    return pubJson({ error: 'រកមិនឃើញបន្ទប់។ សូមពិនិត្យលេខកូដ។' }, req, 404);
  }
  if (r.phase === 'end' || closedByDeadline(r)) return pubJson({ error: 'ហ្គេមនេះបានបញ្ចប់ហើយ។' }, req, 409);
  if (r.class_id) return pubJson({ error: 'នេះជាកិច្ចការផ្ទះ — សូមចូលតាមគណនីសិស្សនៅ exam.khmermath.org/student។' }, req, 403);
  const ps = (await env.DB.prepare('SELECT pid, name FROM live_players WHERE code = ?1').bind(code).all()).results;
  if (ps.length >= 150) return pubJson({ error: 'បន្ទប់ពេញហើយ។' }, req, 409);
  const taken = new Set(ps.map((p) => p.name));
  if (taken.has(name)) { let k = 2; while (taken.has(`${name} ${k}`)) k++; name = `${name} ${k}`; }
  // The next number is chosen inside the INSERT itself, so a whole class tapping "join" in the same second cannot collide.
  const token = rid();
  await env.DB.prepare(`INSERT INTO live_players (code, pid, name, token, cur, qstart, avatar)
    SELECT ?1, COALESCE(MAX(pid), 0) + 1, ?2, ?3, 0, ?4, ?5 FROM live_players WHERE code = ?1`).bind(code, name, token, Date.now(), okAvatar(b.avatar) ? b.avatar : '').run();
  const pid = (await env.DB.prepare('SELECT pid FROM live_players WHERE code = ?1 AND token = ?2').bind(code, token).first()).pid;
  return pubJson({ pid, token, name, mode: r.mode }, req);
}

async function player(env, code, pid, token) {
  const p = await env.DB.prepare('SELECT pid, name, score, token, cur, qstart, avatar FROM live_players WHERE code = ?1 AND pid = ?2').bind(code, Number(pid)).first();
  return p && p.token === token ? p : null;
}


async function soloState(req, env, r, p) {
  const code = r.code, over = r.phase === 'end' || closedByDeadline(r) || (r.phase !== 'lobby' && p.cur >= r.total);
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
  if (await isLocked(env)) return pubJson({ error: 'ហ្គេមផ្ទាល់ត្រូវបានបិទជាបណ្តោះអាសន្ន (ថ្ងៃប្រឡង)។' }, req, 503);
  await ensureTables(env);
  const b = await req.json().catch(() => ({}));
  const code = String(b.code || ''), r = await room(env, code), p = r && (await player(env, code, b.pid, b.token));
  if (!r || !p || r.mode !== 'solo') return pubJson({ error: 'gone' }, req, 404);
  const a = await env.DB.prepare('SELECT 1 x FROM live_answers WHERE code = ?1 AND qi = ?2 AND pid = ?3').bind(code, p.cur, p.pid).first();
  if (a && p.cur < r.total) await env.DB.prepare('UPDATE live_players SET cur = ?3, qstart = ?4 WHERE code = ?1 AND pid = ?2 AND cur = ?5').bind(code, p.pid, p.cur + 1, Date.now(), p.cur).run();
  return pubJson({ ok: true }, req);
}

export async function state(req, env) {
  if (await isLocked(env)) return pubJson({ error: 'ហ្គេមផ្ទាល់ត្រូវបានបិទជាបណ្តោះអាសន្ន (ថ្ងៃប្រឡង)។' }, req, 503);
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
  if (await isLocked(env)) return pubJson({ error: 'ហ្គេមផ្ទាល់ត្រូវបានបិទជាបណ្តោះអាសន្ន (ថ្ងៃប្រឡង)។' }, req, 503);
  await ensureTables(env);
  const b = await req.json().catch(() => ({}));
  const code = String(b.code || ''), r = await room(env, code), p = r && (await player(env, code, b.pid, b.token));
  if (!r || !p) return pubJson({ error: 'gone' }, req, 404);
  if (r.mode === 'solo') {
    if (r.phase === 'end' || closedByDeadline(r) || Number(b.qi) !== p.cur || p.cur >= r.total) return pubJson({ error: 'late' }, req, 409);
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
  if (await isLocked(env)) return pubJson({ error: 'ហ្គេមផ្ទាល់ត្រូវបានបិទជាបណ្តោះអាសន្ន (ថ្ងៃប្រឡង)។' }, req, 503);
  await ensureTables(env);
  const b = await req.json().catch(() => ({}));
  const code = String(b.code || ''), r = await room(env, code), p = r && (await player(env, code, b.pid, b.token));
  if (!r || !p) return pubJson({ error: 'gone' }, req, 404);
  if (!okAvatar(b.avatar)) return pubJson({ error: 'bad' }, req, 400);
  await env.DB.prepare('UPDATE live_players SET avatar = ?3 WHERE code = ?1 AND pid = ?2').bind(code, p.pid, b.avatar).run();
  return pubJson({ ok: true }, req);
}

// ------------------------------------------------------------------ history (teacher)
export async function history(req, env) {
  const t = await authTeacher(req, env);
  if (!t) return err('Not logged in.', 401);
  await ensureTables(env);
  const admin = t.role === 'owner' || t.role === 'admin';
  const { results } = await env.DB.prepare(`SELECT r.code, r.mode, r.title, r.total, r.secs, r.phase, r.created_at, r.deadline, r.lessons, r.class_id, c.name AS class_name,
      (SELECT COUNT(*) FROM live_players p WHERE p.code = r.code) AS players,
      (SELECT COALESCE(AVG(score), 0) FROM live_players p WHERE p.code = r.code) AS avg_score,
      (SELECT COUNT(*) FROM live_players p WHERE p.code = r.code AND p.cur >= r.total) AS finished
    FROM live_rooms r LEFT JOIN classes c ON c.id = r.class_id WHERE (?1 = 1 OR r.owner_id = ?2) ORDER BY r.created_at DESC LIMIT 80`).bind(admin ? 1 : 0, t.id).all();
  return json({ rooms: results.map((r) => ({ ...r, lessons: r.lessons ? JSON.parse(r.lessons) : [], avg_score: Math.round(r.avg_score), over: r.phase === 'end' || closedByDeadline(r) })) });
}

export async function historyDetail(req, env, params) {
  const g = await mine(req, env, params.code); if (g.resp) return g.resp;
  const r = g.r;
  const players = (await env.DB.prepare('SELECT pid, name, avatar, student_id, score, cur FROM live_players WHERE code = ?1 ORDER BY score DESC, pid').bind(r.code).all()).results;
  const qs = (await env.DB.prepare('SELECT qi, pub, key FROM live_qs WHERE code = ?1 ORDER BY qi').bind(r.code).all()).results;
  const agg = (await env.DB.prepare('SELECT qi, COUNT(*) n, SUM(CASE WHEN pts > 0 THEN 1 ELSE 0 END) ok, SUM(CASE WHEN choice = \'\' THEN 1 ELSE 0 END) timeout, AVG(ms) ms FROM live_answers WHERE code = ?1 GROUP BY qi').bind(r.code).all()).results;
  const dist = (await env.DB.prepare('SELECT qi, choice, COUNT(*) n FROM live_answers WHERE code = ?1 GROUP BY qi, choice').bind(r.code).all()).results;
  const byQ = new Map(agg.map((a) => [a.qi, a]));
  const questions = qs.map((q) => {
    const pub = JSON.parse(q.pub), key = JSON.parse(q.key), a = byQ.get(q.qi) || { n: 0, ok: 0, timeout: 0, ms: 0 };
    return { qi: q.qi, q: pub.q, kind: pub.k, options: pub.o || null, correct: key.correct, show: key.show, answered: a.n, right: a.ok || 0, timeout: a.timeout || 0, pct: a.n ? Math.round(100 * (a.ok || 0) / a.n) : null, avg_sec: a.n ? Math.round(a.ms / 100) / 10 : null,
      dist: dist.filter((d) => d.qi === q.qi).map((d) => ({ choice: d.choice, n: d.n })) };
  });
  return json({ room: { code: r.code, mode: r.mode, total: r.total, secs: r.secs, created_at: r.created_at, deadline: r.deadline, lessons: r.lessons ? JSON.parse(r.lessons) : [], class_id: r.class_id }, players, questions });
}

// ------------------------------------------------------------------ homework (student account)
export async function studentGames(req, env) {
  const s = await requireStudent(req, env);
  if (!s) return err('Not logged in.', 401);
  await ensureTables(env);
  if (await isLocked(env)) return json({ games: [], locked: true });
  const { results } = await env.DB.prepare(`SELECT r.code, r.title, r.total, r.secs, r.deadline, r.lessons,
      (SELECT cur FROM live_players p WHERE p.code = r.code AND p.student_id = ?2) AS cur,
      (SELECT score FROM live_players p WHERE p.code = r.code AND p.student_id = ?2) AS score
    FROM live_rooms r WHERE r.class_id = ?1 AND r.deadline > ?3 AND r.phase != 'end' ORDER BY r.deadline`).bind(s.classId, s.id, Date.now() - 7 * DAY).all();
  return json({ games: results.map((r) => ({ ...r, lessons: r.lessons ? JSON.parse(r.lessons) : [], open: r.deadline > Date.now(), started: r.cur != null, done: r.cur != null && r.cur >= r.total })) });
}

export async function studentJoin(req, env) {
  const s = await requireStudent(req, env);
  if (!s) return err('Not logged in.', 401);
  await ensureTables(env);
  if (await isLocked(env)) return err('ហ្គេមត្រូវបានបិទជាបណ្តោះអាសន្ន (ថ្ងៃប្រឡង)។', 503);
  const b = await req.json().catch(() => ({}));
  const code = String(b.code || ''), r = await room(env, code);
  if (!r || r.class_id !== s.classId) return err('រកមិនឃើញកិច្ចការនេះទេ។', 404);
  if (r.phase === 'end' || closedByDeadline(r)) return err('កិច្ចការនេះផុតកំណត់ហើយ។', 409);
  let p = await env.DB.prepare('SELECT pid, token, name, avatar FROM live_players WHERE code = ?1 AND student_id = ?2').bind(code, s.id).first();
  if (!p) {
    const token = rid();
    await env.DB.prepare(`INSERT INTO live_players (code, pid, name, token, cur, qstart, avatar, student_id)
      SELECT ?1, COALESCE(MAX(pid), 0) + 1, ?2, ?3, 0, ?4, ?5, ?6 FROM live_players WHERE code = ?1`).bind(code, String(s.name).slice(0, 24), token, Date.now(), okAvatar(b.avatar) ? b.avatar : '', s.id).run();
    p = await env.DB.prepare('SELECT pid, token, name, avatar FROM live_players WHERE code = ?1 AND token = ?2').bind(code, token).first();
  }
  return json({ code, pid: p.pid, token: p.token, name: p.name, avatar: p.avatar });
}
