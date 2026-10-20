import { json, err } from '../lib/http.js';
import { hashSecretValue, verifySecretValue } from '../lib/crypto.js';
import { createSessionCookie, clearSessionCookie } from '../lib/session.js';
import { ensureColumns } from '../lib/schema.js';
import { authTeacher, trialUsage } from '../lib/access.js';
import { allow, clientIp } from '../lib/limits.js';
import { audit } from '../lib/audit.js';
import { notifyOwner } from '../lib/notify.js';
import { TRIAL, PLANS, OWNER_TELEGRAM } from '../lib/plans.js';

export async function setupStatus(req, env) {
  const { results } = await env.DB.prepare('SELECT COUNT(*) AS n FROM teachers').all();
  return json({ needs_setup: results[0].n === 0 });
}

// One-time setup: creates the first account, which is the owner. Refuses once any
// teacher exists; every later teacher joins through an invite link.
export async function setup(req, env) {
  const { results } = await env.DB.prepare('SELECT COUNT(*) AS n FROM teachers').all();
  if (results[0].n > 0) return err('A teacher account already exists.', 403);
  const { username, password } = await req.json();
  if (!username || !password || password.length < 6) {
    return err('Username and a password of at least 6 characters are required.', 400);
  }
  await ensureColumns(env);
  const hash = await hashSecretValue(password, username, env.SESSION_SECRET);
  await env.DB.prepare("INSERT INTO teachers (username, password_hash, role, display_name) VALUES (?1, ?2, 'owner', ?1)").bind(username, hash).run();
  const cookie = await createSessionCookie({ role: 'teacher', username }, env.SESSION_SECRET);
  return json({ ok: true }, 200, { 'Set-Cookie': cookie });
}

const EMAIL_RE = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$/;
const USERNAME_RE = /^[A-Za-z0-9_.\-+]{3,30}$/;

// Contact is free text and unverified, so it must never outrank a real username/email match
// (otherwise someone could sign up with contact = "victim" and shadow the victim's account).
const IDENT_RANK = `CASE WHEN LOWER(username) = LOWER(?1) THEN 0
                         WHEN email IS NOT NULL AND LOWER(email) = LOWER(?1) THEN 1
                         WHEN LOWER(username) = LOWER(?2) THEN 2 ELSE 3 END`;

export function isValidEmail(s) {
  if (!s || typeof s !== 'string') return false;
  const str = s.trim();
  return str.length >= 5 && str.length <= 80 && EMAIL_RE.test(str);
}

export function isValidUsername(s) {
  if (!s || typeof s !== 'string') return false;
  return USERNAME_RE.test(s.trim());
}

export async function login(req, env) {
  await ensureColumns(env);
  const { username, password } = await req.json();
  const rawIdent = String(username || '').trim();
  if (!rawIdent) return err('សូមបញ្ចូលឈ្មោះអ្នកប្រើ ឬអ៊ីមែល។', 400);

  if (!(await allow(env, `login:${clientIp(req)}:${rawIdent.toLowerCase()}`, 10, 600))) {
    return err('ព្យាយាមចូលច្រើនដងពេក។ សូមរង់ចាំ ១០ នាទី ហើយសាកល្បងម្តងទៀត។', 429);
  }

  const noAt = rawIdent.replace(/@/g, '');
  const row = await env.DB.prepare(
    `SELECT username, password_hash, active 
     FROM teachers 
     WHERE LOWER(username) = LOWER(?1) 
        OR (email IS NOT NULL AND LOWER(email) = LOWER(?1))
        OR (contact IS NOT NULL AND LOWER(contact) = LOWER(?1))
        OR (LOWER(username) = LOWER(?2) AND ?1 LIKE '%@%')
     ORDER BY ${IDENT_RANK}, id ASC LIMIT 1`
  ).bind(rawIdent, noAt).first();

  if (!row) return err('ឈ្មោះអ្នកប្រើ ឬពាក្យសម្ងាត់មិនត្រឹមត្រូវទេ។', 401);
  const ok = await verifySecretValue(password, row.username, env.SESSION_SECRET, row.password_hash);
  if (!ok) return err('ឈ្មោះអ្នកប្រើ ឬពាក្យសម្ងាត់មិនត្រឹមត្រូវទេ។', 401);
  if (!row.active) return err('គណនីនេះត្រូវបានបិទ។ សូមទាក់ទងម្ចាស់ប្រព័ន្ធ។', 403);
  await env.DB.prepare("UPDATE teachers SET last_login = datetime('now') WHERE username = ?1").bind(row.username).run();
  const cookie = await createSessionCookie({ role: 'teacher', username: row.username }, env.SESSION_SECRET);
  return json({ ok: true }, 200, { 'Set-Cookie': cookie });
}

export async function logout() {
  return json({ ok: true }, 200, { 'Set-Cookie': clearSessionCookie('teacher') });
}

export async function me(req, env) {
  const t = await authTeacher(req, env);
  if (!t) return err('Not logged in.', 401);
  const contact = await env.DB.prepare("SELECT value FROM settings WHERE key = 'contact_text'").first();
  return json({
    id: t.id, username: t.username, role: t.role, display_name: t.display_name,
    status: t.status, licensed: t.licensed, license_until: t.license_until, contact_text: contact ? contact.value : '',
    contact: (await env.DB.prepare('SELECT contact FROM teachers WHERE id = ?1').bind(t.id).first() || {}).contact || '',
    telegram: OWNER_TELEGRAM, pending_requests: t.role === 'owner' ? ((await env.DB.prepare("SELECT COUNT(*) AS n FROM unlock_requests WHERE status = 'pending'").first().catch(() => null)) || { n: 0 }).n : 0,
    plans: PLANS, trial_limits: TRIAL, usage: t.status === 'trial' ? await trialUsage(env, t).catch(() => null) : null,
  });
}

// Open sign-up. New accounts start locked (trial): they can look around the sample test
// but need an unlock code from the owner for anything real.
export async function signup(req, env) {
  await ensureColumns(env);
  const open = await env.DB.prepare("SELECT value FROM settings WHERE key = 'signup_open'").first();
  if (open && open.value === '0') return err('ការចុះឈ្មោះបានបិទជាបណ្តោះអាសន្ន។ សូមទាក់ទងម្ចាស់ប្រព័ន្ធ។', 403);

  const { username, display_name, password, contact, email } = await req.json();
  const rawIdent = String(username || '').trim();
  const rawEmail = String(email || '').trim();
  const rawContact = String(contact || '').trim().slice(0, 80);
  const name = String(display_name || '').trim().slice(0, 60);

  if (!name) return err('សូមបញ្ចូលឈ្មោះរបស់អ្នក។', 400);

  let uname = '';
  let emailVal = null;

  if (rawIdent.includes('@')) {
    if (!isValidEmail(rawIdent)) {
      return err('ទម្រង់អ៊ីមែលមិនត្រឹមត្រូវទេ។ (ឧ. teacher@gmail.com)', 400);
    }
    uname = rawIdent.toLowerCase();
    emailVal = uname;
  } else {
    if (!isValidUsername(rawIdent)) {
      return err('ឈ្មោះអ្នកប្រើត្រូវមាន ៣–៣០ តួ (អក្សរឡាតាំង លេខ _ . - ឬលេខទូរស័ព្ទ)។', 400);
    }
    uname = rawIdent.toLowerCase();
    if (rawEmail) {
      if (!isValidEmail(rawEmail)) return err('ទម្រង់អ៊ីមែលមិនត្រឹមត្រូវទេ។ (ឧ. teacher@gmail.com)', 400);
      emailVal = rawEmail.toLowerCase();
    } else if (isValidEmail(rawContact)) {
      emailVal = rawContact.toLowerCase();
    }
  }

  if (!password || password.length < 6) return err('ពាក្យសម្ងាត់ត្រូវមានយ៉ាងតិច ៦ តួអក្សរ។', 400);

  // Check if username or email is already in use
  const taken = await env.DB.prepare(
    `SELECT 1 FROM teachers 
     WHERE LOWER(username) = LOWER(?1) 
        OR (email IS NOT NULL AND LOWER(email) = LOWER(?1))
        OR (?2 IS NOT NULL AND (LOWER(username) = LOWER(?2) OR (email IS NOT NULL AND LOWER(email) = LOWER(?2))))
     LIMIT 1`
  ).bind(uname, emailVal).first();

  if (taken) {
    return err('ឈ្មោះអ្នកប្រើ ឬអ៊ីមែលនេះមានគេប្រើរួចហើយ។ សូមជ្រើសរើសឈ្មោះផ្សេង ឬចូលប្រើ។', 409);
  }

  // Only real sign-ups count (mistyped forms must not lock people out); a school shares one IP, so allow plenty.
  if (!(await allow(env, `signup:${clientIp(req)}`, 30, 3600))) {
    return err('ចុះឈ្មោះច្រើនពេកពីបណ្តាញនេះ។ សូមសាកល្បងម្តងទៀតក្រោយ ១ ម៉ោង ឬទាក់ទងម្ចាស់ប្រព័ន្ធ។', 429);
  }

  const hash = await hashSecretValue(password, uname, env.SESSION_SECRET);
  await env.DB.prepare(
    `INSERT INTO teachers (username, password_hash, role, display_name, plan, contact, email, created_at, last_login) 
     VALUES (?1, ?2, 'teacher', ?3, 'trial', ?4, ?5, datetime('now'), datetime('now'))`
  ).bind(uname, hash, name, rawContact, emailVal).run();

  await audit(env, null, 'signup', `${uname} (${name})`);
  await notifyOwner(env, `🆕 គ្រូចុះឈ្មោះថ្មី៖ ${name} (${uname})${rawContact ? ` · ${rawContact}` : ''}`);
  const cookie = await createSessionCookie({ role: 'teacher', username: uname }, env.SESSION_SECRET);
  return json({ ok: true }, 200, { 'Set-Cookie': cookie });
}

export async function changePassword(req, env) {
  const t = await authTeacher(req, env);
  if (!t) return err('Not logged in.', 401);
  const { current_password, new_password } = await req.json();
  if (!new_password || new_password.length < 6) {
    return err('ពាក្យសម្ងាត់ថ្មីត្រូវមានយ៉ាងតិច ៦ តួអក្សរ។', 400);
  }
  const teacher = await env.DB.prepare('SELECT username, password_hash FROM teachers WHERE id = ?1').bind(t.id).first();
  const ok = await verifySecretValue(current_password, teacher.username, env.SESSION_SECRET, teacher.password_hash);
  if (!ok) return err('ពាក្យសម្ងាត់បច្ចុប្បន្នមិនត្រឹមត្រូវទេ។', 401);

  const newHash = await hashSecretValue(new_password, teacher.username, env.SESSION_SECRET);
  await env.DB.prepare('UPDATE teachers SET password_hash = ?1 WHERE id = ?2').bind(newHash, t.id).run();
  return json({ ok: true });
}

// A trial teacher asks the owner for an unlock code; the owner is told on Telegram and replies with a code after payment.
export async function requestUnlock(req, env) {
  const t = await authTeacher(req, env);
  if (!t) return err('Not logged in.', 401);
  const { plan, contact, note } = await req.json();
  const p = PLANS[plan];
  if (!p) return err('សូមជ្រើសរើសគម្រោង។', 400);
  if (!(await allow(env, `unlockreq:${t.id}`, 5, 86400))) return err('អ្នកបានស្នើសុំច្រើនដងហើយ។ ម្ចាស់ប្រព័ន្ធនឹងទាក់ទងអ្នកឆាប់ៗ។', 429);
  const how = String(contact || '').trim().slice(0, 80);
  if (how) await env.DB.prepare('UPDATE teachers SET contact = ?1 WHERE id = ?2').bind(how, t.id).run();
  await ensureColumns(env);
  await env.DB.prepare("DELETE FROM unlock_requests WHERE teacher_id = ?1 AND status = 'pending'").bind(t.id).run();
  await env.DB.prepare('INSERT INTO unlock_requests (teacher_id, plan, contact, note) VALUES (?1, ?2, ?3, ?4)').bind(t.id, plan, how, String(note || '').slice(0, 200)).run();
  await audit(env, t, 'license.request', `${plan} $${p.price}`);
  const sent = await notifyOwner(env, `💳 ស្នើសុំដោះសោ៖ ${t.display_name} (@${t.username}) · គម្រោង ${p.label} $${p.price}${how ? ` · ${how}` : ''}${note ? ` · ${String(note).slice(0, 120)}` : ''}`);
  return json({ ok: true, notified: sent });
}

// "Forgot password" for teachers: the owner is notified (red counter) and sends a one-time reset link.
// Always answers ok, so nobody can use it to find out which usernames exist.
export async function forgotPassword(req, env) {
  await ensureColumns(env);
  const { username, contact } = await req.json();
  const rawIdent = String(username || '').trim();
  if (!rawIdent) return err('សូមបញ្ចូលឈ្មោះអ្នកប្រើ ឬអ៊ីមែល។', 400);
  if (!(await allow(env, `forgot:${clientIp(req)}`, 6, 3600))) return err('សំណើច្រើនពេក។ សូមរង់ចាំមួយម៉ោង ឬទាក់ទងម្ចាស់ប្រព័ន្ធ។', 429);
  const noAt = rawIdent.replace(/@/g, '');
  const t = await env.DB.prepare(
    `SELECT id, username, display_name, role FROM teachers 
     WHERE (LOWER(username) = LOWER(?1) 
        OR (email IS NOT NULL AND LOWER(email) = LOWER(?1))
        OR (contact IS NOT NULL AND LOWER(contact) = LOWER(?1))
        OR (LOWER(username) = LOWER(?2) AND ?1 LIKE '%@%'))
       AND active = 1 
     ORDER BY ${IDENT_RANK}, id ASC LIMIT 1`
  ).bind(rawIdent, noAt).first();
  if (t && t.role !== 'owner') {
    const how = String(contact || '').trim().slice(0, 80);
    await env.DB.prepare("DELETE FROM unlock_requests WHERE teacher_id = ?1 AND plan = 'reset' AND status = 'pending'").bind(t.id).run();
    await env.DB.prepare("INSERT INTO unlock_requests (teacher_id, plan, contact) VALUES (?1, 'reset', ?2)").bind(t.id, how).run();
    await notifyOwner(env, `🔑 ភ្លេចពាក្យសម្ងាត់៖ ${t.display_name || t.username} (@${t.username})${how ? ` · ${how}` : ''}`);
  }
  return json({ ok: true });
}

// Owner recovery. Works only if the owner has set the Cloudflare secret OWNER_RECOVERY_CODE
// (`npx wrangler secret put OWNER_RECOVERY_CODE`); without it this route stays closed.
export async function ownerReset(req, env) {
  if (!env.OWNER_RECOVERY_CODE || env.OWNER_RECOVERY_CODE.length < 12) return err('មិនទាន់បានបើកការស្តារម្ចាស់ប្រព័ន្ធទេ។', 404);
  if (!(await allow(env, `ownerreset:${clientIp(req)}`, 5, 3600))) return err('ព្យាយាមច្រើនពេក។ សូមរង់ចាំមួយម៉ោង។', 429);
  const { username, code, password } = await req.json();
  const a = new TextEncoder().encode(String(code || '')), b = new TextEncoder().encode(env.OWNER_RECOVERY_CODE);
  let diff = a.length ^ b.length;
  for (let i = 0; i < b.length; i++) diff |= (a[i] || 0) ^ b[i];
  const row = await env.DB.prepare("SELECT id, username FROM teachers WHERE username = ?1 AND role = 'owner'").bind(String(username || '').trim()).first();
  if (diff !== 0 || !row) return err('កូដស្តារ ឬឈ្មោះអ្នកប្រើមិនត្រឹមត្រូវទេ។', 403);
  if (!password || password.length < 10) return err('ពាក្យសម្ងាត់ថ្មីត្រូវមានយ៉ាងតិច ១០ តួអក្សរ។', 400);
  const hash = await hashSecretValue(password, row.username, env.SESSION_SECRET);
  await env.DB.prepare('UPDATE teachers SET password_hash = ?1, active = 1 WHERE id = ?2').bind(hash, row.id).run();
  await audit(env, null, 'owner.recover', row.username);
  await notifyOwner(env, '⚠️ ពាក្យសម្ងាត់ម្ចាស់ប្រព័ន្ធត្រូវបានកំណត់ថ្មីតាមកូដស្តារ។');
  return json({ ok: true });
}
