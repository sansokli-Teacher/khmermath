// Per-teacher "paper profile": the header and footer printed on exam papers and answer sheets.
import { json, err } from '../lib/http.js';
import { authTeacher, needLicense } from '../lib/access.js';

export const PAPER_FIELDS = ['school', 'group', 'subject', 'website', 'facebook', 'teacher', 'email', 'telegram', 'tel', 'logo'];
const EMPTY = Object.fromEntries(PAPER_FIELDS.map((f) => [f, '']));
EMPTY.subject = 'គណិតវិទ្យា';

async function load(env, teacherId) {
  const row = await env.DB.prepare('SELECT value FROM settings WHERE key = ?1').bind(`paper_profile_${teacherId}`).first();
  try { return { ...EMPTY, ...(row ? JSON.parse(row.value) : {}) }; } catch { return { ...EMPTY }; }
}

export async function getPaperProfile(req, env) {
  const t = await authTeacher(req, env);
  if (!t) return err('Not logged in.', 401);
  const profile = await load(env, t.id);
  if (!profile.teacher && !profile.school) profile.teacher = t.display_name ? `បង្រៀនដោយ ${t.display_name}` : '';
  return json({ profile });
}

export async function setPaperProfile(req, env) {
  const g = await needLicense(req, env); if (g.resp) return g.resp;
  const body = await req.json();
  const clean = {};
  for (const f of PAPER_FIELDS) clean[f] = String(body[f] ?? '').trim().slice(0, 140);
  if (clean.logo && !/^(\/ngs\.png|[A-Za-z0-9._-]{6,80})$/.test(clean.logo)) clean.logo = '';
  await env.DB.prepare('INSERT INTO settings (key, value) VALUES (?1, ?2) ON CONFLICT(key) DO UPDATE SET value = ?2')
    .bind(`paper_profile_${g.t.id}`, JSON.stringify(clean)).run();
  return json({ ok: true, profile: clean });
}
