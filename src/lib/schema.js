// Lazy schema upgrades. Every API module calls ensureColumns() before touching
// columns/tables that were added after the first deploy; it is cheap after the
// first call in an isolate and safe to run repeatedly.
let done = false;

export async function ensureColumns(env) {
  if (done) return;
  const alters = [
    'ALTER TABLE results ADD COLUMN started_at TEXT',
    'ALTER TABLE results ADD COLUMN submit_type TEXT',
    'ALTER TABLE test_sessions ADD COLUMN scheduled_end TEXT',
    'ALTER TABLE test_sessions ADD COLUMN pin TEXT',
    'ALTER TABLE results ADD COLUMN tab_switches INTEGER NOT NULL DEFAULT 0',
    "ALTER TABLE test_questions ADD COLUMN kind TEXT NOT NULL DEFAULT 'mcq'",
    'ALTER TABLE test_questions ADD COLUMN solution_text TEXT',
    "ALTER TABLE teachers ADD COLUMN role TEXT NOT NULL DEFAULT 'teacher'",
    'ALTER TABLE teachers ADD COLUMN display_name TEXT',
    'ALTER TABLE teachers ADD COLUMN active INTEGER NOT NULL DEFAULT 1',
    'ALTER TABLE teachers ADD COLUMN last_login TEXT',
    'ALTER TABLE classes ADD COLUMN owner_id INTEGER',
    'ALTER TABLE tests ADD COLUMN owner_id INTEGER',
    // licensing: existing accounts stay 'full'; self-signups are created as 'trial'
    "ALTER TABLE teachers ADD COLUMN plan TEXT NOT NULL DEFAULT 'full'",
    'ALTER TABLE teachers ADD COLUMN license_until TEXT',
    'ALTER TABLE teachers ADD COLUMN contact TEXT',
    'ALTER TABLE teachers ADD COLUMN created_at TEXT',
    'ALTER TABLE tests ADD COLUMN is_sample INTEGER NOT NULL DEFAULT 0',
    'ALTER TABLE invites ADD COLUMN months INTEGER',
  ];
  for (const sql of alters) { try { await env.DB.prepare(sql).run(); } catch {} }

  await env.DB.batch([
    // One-time invite / password-reset links. Only a hash of the token is stored.
    env.DB.prepare(`CREATE TABLE IF NOT EXISTS invites (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      token_hash TEXT NOT NULL UNIQUE,
      purpose TEXT NOT NULL DEFAULT 'invite',   -- invite | reset
      teacher_id INTEGER,                        -- set for reset links
      note TEXT,
      created_by INTEGER NOT NULL,
      created_at TEXT NOT NULL DEFAULT (datetime('now')),
      expires_at TEXT NOT NULL,
      used_at TEXT
    )`),
    // Unlock codes the owner generates and hands out.
    env.DB.prepare(`CREATE TABLE IF NOT EXISTS license_codes (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      code TEXT NOT NULL UNIQUE,
      months INTEGER NOT NULL DEFAULT 0,         -- 0 = lifetime
      note TEXT,
      created_by INTEGER NOT NULL,
      created_at TEXT NOT NULL DEFAULT (datetime('now')),
      used_by INTEGER,
      used_at TEXT
    )`),
    // Simple fixed-window rate limiting (login, sign-up, codes, PIN guesses).
    env.DB.prepare(`CREATE TABLE IF NOT EXISTS rate_limits (
      key TEXT PRIMARY KEY,
      count INTEGER NOT NULL,
      window_start INTEGER NOT NULL
    )`),
    // Who changed what (scores, answer keys, licences).
    env.DB.prepare(`CREATE TABLE IF NOT EXISTS audit_log (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      at TEXT NOT NULL DEFAULT (datetime('now')),
      teacher_id INTEGER,
      action TEXT NOT NULL,
      detail TEXT
    )`),
    // A class or test shared with another teacher.
    env.DB.prepare(`CREATE TABLE IF NOT EXISTS shares (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      resource_type TEXT NOT NULL,               -- class | test
      resource_id INTEGER NOT NULL,
      teacher_id INTEGER NOT NULL,
      role TEXT NOT NULL,                        -- reviewer | editor
      created_at TEXT NOT NULL DEFAULT (datetime('now')),
      UNIQUE(resource_type, resource_id, teacher_id)
    )`),
    // Reviewer comments on a question.
    env.DB.prepare(`CREATE TABLE IF NOT EXISTS question_notes (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      question_id INTEGER NOT NULL,
      teacher_id INTEGER NOT NULL,
      body TEXT NOT NULL,
      resolved INTEGER NOT NULL DEFAULT 0,
      created_at TEXT NOT NULL DEFAULT (datetime('now'))
    )`),
  ]);

  // The existing account becomes the owner; everything created before teams
  // existed belongs to the owner.
  await env.DB.prepare("UPDATE teachers SET role = 'owner' WHERE id = (SELECT MIN(id) FROM teachers) AND NOT EXISTS (SELECT 1 FROM teachers WHERE role = 'owner')").run();
  await env.DB.prepare("UPDATE classes SET owner_id = (SELECT id FROM teachers WHERE role = 'owner' ORDER BY id LIMIT 1) WHERE owner_id IS NULL").run();
  await env.DB.prepare("UPDATE tests SET owner_id = (SELECT id FROM teachers WHERE role = 'owner' ORDER BY id LIMIT 1) WHERE owner_id IS NULL").run();
  done = true;
}
