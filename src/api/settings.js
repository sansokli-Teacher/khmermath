import { json, err } from '../lib/http.js';
import { needAdmin } from '../lib/access.js';
import { hashSecretValue } from '../lib/crypto.js';

// The one shared student login PIN (every student uses the same PIN, set by
// the teacher, alongside their own individual id). Stored hashed, like the
// teacher's own password — the teacher only ever sets/replaces it, never
// reads it back, so a hash is no less convenient and keeps the DB from
// holding a readable copy of a secret every student in the school knows.
export async function getPinStatus(req, env) {
  { const g = await needAdmin(req, env); if (g.resp) return g.resp; }
  const row = await env.DB.prepare("SELECT value FROM settings WHERE key = 'student_pin_hash'").first();
  return json({ has_pin: !!row });
}

export async function setPin(req, env) {
  { const g = await needAdmin(req, env); if (g.resp) return g.resp; }
  const { pin } = await req.json();
  if (!pin || !/^\d{4,8}$/.test(pin)) return err('PIN must be 4 to 8 digits.', 400);
  const hash = await hashSecretValue(pin, 'student_pin', env.SESSION_SECRET);
  await env.DB.prepare(
    "INSERT INTO settings (key, value) VALUES ('student_pin_hash', ?1) ON CONFLICT(key) DO UPDATE SET value = ?1",
  ).bind(hash).run();
  return json({ ok: true });
}
