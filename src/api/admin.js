// Teacher management (owner only), invite links, and sharing classes/tests.
import { json, err } from '../lib/http.js';
import { hashSecretValue } from '../lib/crypto.js';
import { createSessionCookie } from '../lib/session.js';
import { ensureColumns } from '../lib/schema.js';
import { authTeacher, needAdmin, needClass, needTest, needLicense, isAdmin, accessibleClasses, accessibleTests } from '../lib/access.js';
import { allow } from '../lib/limits.js';
import { audit } from '../lib/audit.js';
import { notifyOwner } from '../lib/notify.js';

const INVITE_DAYS = 7;

async function sha256Hex(text) {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, '0')).join('');
}
function newToken() {
  const bytes = crypto.getRandomValues(new Uint8Array(24));
  return [...bytes].map((b) => b.toString(16).padStart(2, '0')).join('');
}
async function makeInvite(env, { purpose, teacherId = null, note = '', createdBy, months = 0 }) {
  const token = newToken();
  const expires = new Date(Date.now() + INVITE_DAYS * 86400000).toISOString().replace('T', ' ').slice(0, 19);
  await env.DB.prepare(
    'INSERT INTO invites (token_hash, purpose, teacher_id, note, created_by, expires_at, months) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7)',
  ).bind(await sha256Hex(token), purpose, teacherId, String(note).slice(0, 80), createdBy, expires, Number(months) || 0).run();
  return { token, expires_at: expires };
}

// ---------- owner: manage teachers ----------
export async function listTeachers(req, env) {
  const g = await needAdmin(req, env); if (g.resp) return g.resp;
  const { results } = await env.DB.prepare(
    `SELECT t.id, t.username, t.display_name, t.role, t.active, t.last_login, t.plan, t.license_until, t.contact,
            (SELECT COUNT(*) FROM classes c WHERE c.owner_id = t.id) AS class_count,
            (SELECT COUNT(*) FROM tests x WHERE x.owner_id = t.id) AS test_count
     FROM teachers t ORDER BY t.id`,
  ).all();
  const { results: invites } = await env.DB.prepare(
    `SELECT i.id, i.purpose, i.note, i.created_at, i.expires_at, COALESCE(t.display_name, t.username) AS teacher_name
     FROM invites i LEFT JOIN teachers t ON t.id = i.teacher_id
     WHERE i.used_at IS NULL AND i.expires_at > datetime('now') ORDER BY i.id DESC`,
  ).all();
  return json({ teachers: results, invites });
}

export async function createInvite(req, env) {
  const g = await needAdmin(req, env); if (g.resp) return g.resp;
  const { note, months } = await req.json().catch(() => ({}));
  const inv = await makeInvite(env, { purpose: 'invite', note: note || '', createdBy: g.t.id, months: Number(months) || 0 });
  return json(inv);
}

export async function createResetLink(req, env, params) {
  const g = await needAdmin(req, env); if (g.resp) return g.resp;
  const target = await env.DB.prepare('SELECT id FROM teachers WHERE id = ?1').bind(params.id).first();
  if (!target) return err('Teacher not found.', 404);
  const inv = await makeInvite(env, { purpose: 'reset', teacherId: target.id, createdBy: g.t.id });
  return json(inv);
}

export async function revokeInvite(req, env, params) {
  const g = await needAdmin(req, env); if (g.resp) return g.resp;
  await env.DB.prepare('DELETE FROM invites WHERE id = ?1 AND used_at IS NULL').bind(params.id).run();
  return json({ ok: true });
}

export async function setTeacherActive(req, env, params) {
  const g = await needAdmin(req, env); if (g.resp) return g.resp;
  if (Number(params.id) === g.t.id) return err('មិនអាចបិទគណនីរបស់ខ្លួនឯងបានទេ។', 400);
  const { active } = await req.json();
  await env.DB.prepare('UPDATE teachers SET active = ?1 WHERE id = ?2 AND role <> \'owner\'').bind(active ? 1 : 0, params.id).run();
  return json({ ok: true });
}

// ---------- public: open an invite / reset link ----------
async function loadInvite(env, token) {
  await ensureColumns(env);
  const inv = await env.DB.prepare(
    `SELECT i.id, i.purpose, i.teacher_id, i.note, i.months, t.username, COALESCE(t.display_name, t.username) AS teacher_name
     FROM invites i LEFT JOIN teachers t ON t.id = i.teacher_id
     WHERE i.token_hash = ?1 AND i.used_at IS NULL AND i.expires_at > datetime('now')`,
  ).bind(await sha256Hex(String(token))).first();
  return inv;
}

export async function inviteInfo(req, env, params) {
  const inv = await loadInvite(env, params.token);
  if (!inv) return err('តំណភ្ជាប់នេះមិនត្រឹមត្រូវ ឬបានផុតកំណត់ហើយ។ សូមសុំតំណថ្មីពីម្ចាស់ប្រព័ន្ធ។', 404);
  return json({ purpose: inv.purpose, note: inv.note, username: inv.username, teacher_name: inv.teacher_name });
}

export async function acceptInvite(req, env, params) {
  const inv = await loadInvite(env, params.token);
  if (!inv) return err('តំណភ្ជាប់នេះមិនត្រឹមត្រូវ ឬបានផុតកំណត់ហើយ។', 404);
  const { username, display_name, password } = await req.json();
  if (!password || password.length < 6) return err('ពាក្យសម្ងាត់ត្រូវមានយ៉ាងតិច ៦ តួអក្សរ។', 400);

  let finalUsername;
  if (inv.purpose === 'reset') {
    finalUsername = inv.username;
    const hash = await hashSecretValue(password, finalUsername, env.SESSION_SECRET);
    await env.DB.prepare('UPDATE teachers SET password_hash = ?1 WHERE id = ?2').bind(hash, inv.teacher_id).run();
  } else {
    finalUsername = String(username || '').trim();
    if (!/^[A-Za-z0-9_.\-]{3,30}$/.test(finalUsername)) return err('ឈ្មោះអ្នកប្រើត្រូវមាន ៣–៣០ តួ (អក្សរឡាតាំង លេខ _ . -)។', 400);
    const name = String(display_name || '').trim().slice(0, 60);
    if (!name) return err('សូមបញ្ចូលឈ្មោះរបស់អ្នក។', 400);
    const taken = await env.DB.prepare('SELECT 1 FROM teachers WHERE username = ?1').bind(finalUsername).first();
    if (taken) return err('ឈ្មោះអ្នកប្រើនេះមានគេប្រើរួចហើយ។ សូមជ្រើសរើសឈ្មោះផ្សេង។', 409);
    const hash = await hashSecretValue(password, finalUsername, env.SESSION_SECRET);
    // An invite from the owner comes with full access (for N months, or without end).
    const until = inv.months > 0 ? addMonths(null, inv.months) : null;
    await env.DB.prepare("INSERT INTO teachers (username, password_hash, role, display_name, plan, license_until, created_at, last_login) VALUES (?1, ?2, 'teacher', ?3, 'full', ?4, datetime('now'), datetime('now'))")
      .bind(finalUsername, hash, name, until).run();
  }
  await env.DB.prepare("UPDATE invites SET used_at = datetime('now') WHERE id = ?1").bind(inv.id).run();
  const cookie = await createSessionCookie({ role: 'teacher', username: finalUsername }, env.SESSION_SECRET);
  return json({ ok: true }, 200, { 'Set-Cookie': cookie });
}

// ---------- search + sharing ----------
export async function searchTeachers(req, env) {
  const g0 = await needLicense(req, env); if (g0.resp) return g0.resp;
  const t = g0.t;
  const q = (new URL(req.url).searchParams.get('q') || '').trim();
  const like = `%${q.replace(/[%_]/g, '')}%`;
  const { results } = await env.DB.prepare(
    `SELECT id, username, COALESCE(display_name, username) AS name FROM teachers
     WHERE active = 1 AND id <> ?1 AND (username LIKE ?2 OR display_name LIKE ?2) ORDER BY name LIMIT 10`,
  ).bind(t.id, like).all();
  return json({ teachers: results });
}

async function needResource(req, env, type, id, level) {
  return type === 'class' ? needClass(req, env, id, level) : needTest(req, env, id, level);
}

export async function listShares(req, env) {
  const url = new URL(req.url);
  const type = url.searchParams.get('type'), id = Number(url.searchParams.get('id'));
  if (!['class', 'test'].includes(type)) return err('type must be class or test.', 400);
  const g = await needResource(req, env, type, id, 'own'); if (g.resp) return g.resp;
  const { results } = await env.DB.prepare(
    `SELECT s.teacher_id, s.role, t.username, COALESCE(t.display_name, t.username) AS name
     FROM shares s JOIN teachers t ON t.id = s.teacher_id WHERE s.resource_type = ?1 AND s.resource_id = ?2 ORDER BY name`,
  ).bind(type, id).all();
  return json({ shares: results });
}

export async function setShare(req, env) {
  const { type, id, teacher_id, role } = await req.json();
  if (!['class', 'test'].includes(type)) return err('type must be class or test.', 400);
  if (!['reviewer', 'editor'].includes(role)) return err('role must be reviewer or editor.', 400);
  const g = await needResource(req, env, type, Number(id), 'own'); if (g.resp) return g.resp;
  if (Number(teacher_id) === g.t.id) return err('មិនអាចចែករំលែកទៅខ្លួនឯងបានទេ។', 400);
  const target = await env.DB.prepare('SELECT id FROM teachers WHERE id = ?1 AND active = 1').bind(Number(teacher_id)).first();
  if (!target) return err('រកមិនឃើញគ្រូនេះទេ។', 404);
  await env.DB.prepare(
    `INSERT INTO shares (resource_type, resource_id, teacher_id, role) VALUES (?1, ?2, ?3, ?4)
     ON CONFLICT(resource_type, resource_id, teacher_id) DO UPDATE SET role = ?4`,
  ).bind(type, Number(id), target.id, role).run();
  return json({ ok: true });
}

// The owner of the resource removes someone, or a co-teacher removes herself.
export async function removeShare(req, env) {
  const { type, id, teacher_id } = await req.json();
  if (!['class', 'test'].includes(type)) return err('type must be class or test.', 400);
  const t = await authTeacher(req, env);
  if (!t) return err('Not logged in.', 401);
  if (Number(teacher_id) !== t.id) {
    const g = await needResource(req, env, type, Number(id), 'own'); if (g.resp) return g.resp;
  }
  await env.DB.prepare('DELETE FROM shares WHERE resource_type = ?1 AND resource_id = ?2 AND teacher_id = ?3')
    .bind(type, Number(id), Number(teacher_id)).run();
  return json({ ok: true });
}

// ---------- licence: unlock codes ----------
const CODE_ALPHABET = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';   // no 0/O/1/I confusion
function newCode() {
  const bytes = crypto.getRandomValues(new Uint8Array(12));
  const chars = [...bytes].map((b) => CODE_ALPHABET[b % CODE_ALPHABET.length]);
  return [chars.slice(0, 4), chars.slice(4, 8), chars.slice(8, 12)].map((g) => g.join('')).join('-');
}
const normCode = (c) => String(c || '').toUpperCase().replace(/[^A-Z0-9]/g, '').replace(/(.{4})(.{4})(.{4})/, '$1-$2-$3');

// Extends from the current end date (or from now), so renewing early never loses time.
function addMonths(fromStamp, months) {
  const base = fromStamp && new Date(fromStamp.replace(' ', 'T') + 'Z') > new Date() ? new Date(fromStamp.replace(' ', 'T') + 'Z') : new Date();
  base.setUTCMonth(base.getUTCMonth() + months);
  return base.toISOString().replace('T', ' ').slice(0, 19);
}

export async function createCodes(req, env) {
  const g = await needAdmin(req, env); if (g.resp) return g.resp;
  const { months, count, note } = await req.json();
  const m = Number(months);
  if (![0, 1, 3, 6, 12, 24].includes(m)) return err('months must be 0 (lifetime), 1, 3, 6, 12 or 24.', 400);
  const n = Math.min(Math.max(Number(count) || 1, 1), 30);
  const made = [];
  for (let i = 0; i < n; i++) {
    const code = newCode();
    await env.DB.prepare('INSERT INTO license_codes (code, months, note, created_by) VALUES (?1, ?2, ?3, ?4)')
      .bind(code, m, String(note || '').slice(0, 80), g.t.id).run();
    made.push(code);
  }
  await audit(env, g.t, 'codes.create', `${n} × ${m || 'lifetime'} months — ${note || ''}`);
  return json({ codes: made, months: m });
}

export async function listCodes(req, env) {
  const g = await needAdmin(req, env); if (g.resp) return g.resp;
  const { results } = await env.DB.prepare(
    `SELECT c.id, c.code, c.months, c.note, c.created_at, c.used_at,
            COALESCE(t.display_name, t.username) AS used_by_name, t.username AS used_by_username
     FROM license_codes c LEFT JOIN teachers t ON t.id = c.used_by ORDER BY c.id DESC LIMIT 200`,
  ).all();
  return json({ codes: results });
}

export async function deleteCode(req, env, params) {
  const g = await needAdmin(req, env); if (g.resp) return g.resp;
  await env.DB.prepare('DELETE FROM license_codes WHERE id = ?1 AND used_at IS NULL').bind(params.id).run();
  return json({ ok: true });
}

// A teacher redeems a code and is unlocked.
export async function redeemCode(req, env) {
  const t = await authTeacher(req, env);
  if (!t) return err('Not logged in.', 401);
  if (!(await allow(env, `redeem:${t.id}`, 8, 3600))) return err('សាកល្បងច្រើនដងពេក។ សូមរង់ចាំមួយម៉ោង។', 429);
  const { code } = await req.json();
  const c = normCode(code);
  const row = await env.DB.prepare('SELECT id, months FROM license_codes WHERE code = ?1 AND used_at IS NULL').bind(c).first();
  if (!row) return err('កូដមិនត្រឹមត្រូវ ឬត្រូវបានប្រើរួចហើយ។', 404);
  let until = null;
  const cur = await env.DB.prepare('SELECT plan, license_until FROM teachers WHERE id = ?1').bind(t.id).first();
  const lifetimeAlready = cur.plan === 'full' && !cur.license_until;
  if (row.months > 0) until = lifetimeAlready ? null : addMonths(cur.plan === 'full' ? cur.license_until : null, row.months);
  // claim the code first so two simultaneous redeems cannot both win
  const claim = await env.DB.prepare("UPDATE license_codes SET used_by = ?1, used_at = datetime('now') WHERE id = ?2 AND used_at IS NULL").bind(t.id, row.id).run();
  if (!claim.meta.rows_written) return err('កូដនេះត្រូវបានប្រើរួចហើយ។', 409);
  await env.DB.prepare("UPDATE teachers SET plan = 'full', license_until = ?1 WHERE id = ?2").bind(until, t.id).run();
  await audit(env, t, 'license.redeem', `${c} → ${until || 'lifetime'}`);
  await notifyOwner(env, `🔓 ${t.display_name} (@${t.username}) បានដោះសោដោយកូដ ${c} — ${until ? `ដល់ ${until.slice(0, 10)}` : 'ពេញមួយជីវិត'}`);
  return json({ ok: true, license_until: until });
}

// Owner: unlock N months (0 = lifetime) or lock an account again.
export async function setLicense(req, env, params) {
  const g = await needAdmin(req, env); if (g.resp) return g.resp;
  const { action, months } = await req.json();
  const target = await env.DB.prepare('SELECT id, plan, license_until, role FROM teachers WHERE id = ?1').bind(params.id).first();
  if (!target) return err('Teacher not found.', 404);
  if (target.role === 'owner') return err('ម្ចាស់ប្រព័ន្ធមិនត្រូវការកូដទេ។', 400);
  if (action === 'lock') {
    await env.DB.prepare("UPDATE teachers SET plan = 'trial', license_until = NULL WHERE id = ?1").bind(target.id).run();
  } else {
    const m = Number(months) || 0;
    const until = m > 0 ? addMonths(target.plan === 'full' ? target.license_until : null, m) : null;
    await env.DB.prepare("UPDATE teachers SET plan = 'full', license_until = ?1 WHERE id = ?2").bind(until, target.id).run();
  }
  await audit(env, g.t, 'license.set', `teacher ${target.id}: ${action === 'lock' ? 'lock' : `${months || 'lifetime'} months`}`);
  return json({ ok: true });
}

// Owner: settings (open sign-up on/off, contact text shown to locked teachers).
export async function getAdminSettings(req, env) {
  const g = await needAdmin(req, env); if (g.resp) return g.resp;
  const rows = await env.DB.prepare("SELECT key, value FROM settings WHERE key IN ('signup_open', 'contact_text', 'telegram_token', 'telegram_chat_id')").all();
  const m = Object.fromEntries(rows.results.map((r) => [r.key, r.value]));
  return json({ signup_open: m.signup_open !== '0', contact_text: m.contact_text || '', telegram_set: !!m.telegram_token, telegram_chat_id: m.telegram_chat_id || '' });
}

export async function setAdminSettings(req, env) {
  const g = await needAdmin(req, env); if (g.resp) return g.resp;
  const b = await req.json();
  const put = (k, v) => env.DB.prepare('INSERT INTO settings (key, value) VALUES (?1, ?2) ON CONFLICT(key) DO UPDATE SET value = ?2').bind(k, v);
  const stmts = [];
  if (b.signup_open !== undefined) stmts.push(put('signup_open', b.signup_open ? '1' : '0'));
  if (b.contact_text !== undefined) stmts.push(put('contact_text', String(b.contact_text).slice(0, 200)));
  if (b.telegram_token) stmts.push(put('telegram_token', String(b.telegram_token).trim().slice(0, 200)));     // write-only: never sent back
  if (b.telegram_chat_id !== undefined) stmts.push(put('telegram_chat_id', String(b.telegram_chat_id).trim().slice(0, 40)));
  if (stmts.length) await env.DB.batch(stmts);
  return json({ ok: true });
}

export async function listAudit(req, env) {
  const g = await needAdmin(req, env); if (g.resp) return g.resp;
  const { results } = await env.DB.prepare(
    `SELECT a.id, a.at, a.action, a.detail, COALESCE(t.display_name, t.username) AS who
     FROM audit_log a LEFT JOIN teachers t ON t.id = a.teacher_id ORDER BY a.id DESC LIMIT 200`,
  ).all();
  return json({ log: results });
}

// ---------- backup / export of everything this teacher can see ----------
export async function exportData(req, env) {
  const t = await authTeacher(req, env);
  if (!t) return err('Not logged in.', 401);
  const myClasses = await accessibleClasses(env, t);
  const myTests = await accessibleTests(env, t);
  const classIds = [...myClasses.keys()];
  const testIds = [...myTests.entries()].filter(([, r]) => r === 'owner' || r === 'editor').map(([id]) => id);
  const ph = (arr) => (arr.length ? arr.map(() => '?').join(',') : 'NULL');
  const q = async (sql, ...binds) => (await env.DB.prepare(sql).bind(...binds).all()).results;

  const classes = await q(`SELECT id, name, grade FROM classes WHERE id IN (${ph(classIds)})`, ...classIds);
  const students = await q(`SELECT id, class_id, surname, first_name, gender, dob FROM students WHERE class_id IN (${ph(classIds)}) ORDER BY class_id, surname`, ...classIds);
  const sessions = await q(
    `SELECT s.id, s.class_id, c.name AS class_name, x.title AS test_title, s.scheduled_start, s.scheduled_end, s.duration_minutes, s.status
     FROM test_sessions s JOIN classes c ON c.id = s.class_id JOIN tests x ON x.id = s.test_id WHERE s.class_id IN (${ph(classIds)}) ORDER BY s.scheduled_start`, ...classIds);
  const sessionIds = sessions.map((x) => x.id);
  const results = await q(
    `SELECT session_id, student_id, mcq_score, mcq_max, writing_score, writing_max, started_at, submitted_at, submit_type, published_at, tab_switches
     FROM results WHERE session_id IN (${ph(sessionIds)})`, ...sessionIds);
  const assessments = await q(`SELECT id, class_id, key, title, month_label, kind, session_id, max_score FROM assessments WHERE class_id IN (${ph(classIds)})`, ...classIds).catch(() => []);
  const aIds = assessments.map((a) => a.id);
  const manual = await q(`SELECT assessment_id, student_id, score FROM manual_scores WHERE assessment_id IN (${ph(aIds)})`, ...aIds).catch(() => []);
  const tests = await q(`SELECT id, title, status FROM tests WHERE id IN (${ph(testIds)})`, ...testIds);
  const questions = await q(
    `SELECT test_id, order_no, kind, stem_text, options_json, correct_index, points, topic, level, solution_text FROM test_questions WHERE test_id IN (${ph(testIds)}) ORDER BY test_id, order_no`, ...testIds);
  return json({ exported_at: new Date().toISOString(), teacher: t.display_name, classes, students, sessions, results, assessments, manual_scores: manual, tests, questions });
}

export async function telegramTest(req, env) {
  const g = await needAdmin(req, env); if (g.resp) return g.resp;
  const ok = await notifyOwner(env, '✅ ការជូនដំណឹង Telegram ដំណើរការ — ប្រព័ន្ធប្រឡងគណិតវិទ្យា');
  return ok ? json({ ok: true }) : err('ផ្ញើមិនបានទេ។ សូមពិនិត្យ Bot token និង Chat ID (ហើយបាន /start ជាមួយ Bot ជាមុន)។', 400);
}
