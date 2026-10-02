-- Exam Khmer — D1 schema.
-- Apply with: npx wrangler d1 execute exam-khmer --remote --file schema.sql

-- Question images, stored as base64 in D1 (no R2 bucket needed — R2 requires a
-- one-time "enable" step in the Cloudflare dashboard that we're skipping for now).
CREATE TABLE IF NOT EXISTS images (
  key TEXT PRIMARY KEY,
  content_type TEXT NOT NULL,
  data_base64 TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS teachers (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS classes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,       -- e.g. "7NGS-B"
  grade INTEGER NOT NULL    -- e.g. 7
);

CREATE TABLE IF NOT EXISTS students (
  id TEXT PRIMARY KEY,      -- the existing student id, e.g. "0109293"
  class_id INTEGER NOT NULL REFERENCES classes(id),
  name TEXT NOT NULL,
  pin_hash TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_students_class ON students(class_id);

CREATE TABLE IF NOT EXISTS tests (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'draft',  -- draft | ready
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS test_questions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  test_id INTEGER NOT NULL REFERENCES tests(id),
  order_no INTEGER NOT NULL,
  stem_text TEXT NOT NULL,       -- may contain inline \( \) math, rendered client-side with KaTeX
  image_key TEXT,                -- R2 object key, or NULL
  options_json TEXT NOT NULL,    -- JSON array of option strings (may contain \( \) math)
  correct_index INTEGER NOT NULL,
  points INTEGER NOT NULL DEFAULT 1
);
CREATE INDEX IF NOT EXISTS idx_questions_test ON test_questions(test_id, order_no);

-- A test_session is one scheduled run of a test for one class (same test can run
-- for 7NGS-B on Monday and 7NGS-CO on Wednesday as two separate sessions).
CREATE TABLE IF NOT EXISTS test_sessions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  test_id INTEGER NOT NULL REFERENCES tests(id),
  class_id INTEGER NOT NULL REFERENCES classes(id),
  scheduled_start TEXT NOT NULL,   -- ISO 8601 UTC
  duration_minutes INTEGER NOT NULL,
  status TEXT NOT NULL DEFAULT 'scheduled'  -- scheduled | closed
);
CREATE INDEX IF NOT EXISTS idx_sessions_class ON test_sessions(class_id);

CREATE TABLE IF NOT EXISTS responses (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id INTEGER NOT NULL REFERENCES test_sessions(id),
  student_id TEXT NOT NULL REFERENCES students(id),
  question_id INTEGER NOT NULL REFERENCES test_questions(id),
  selected_index INTEGER NOT NULL,
  answered_at TEXT NOT NULL DEFAULT (datetime('now')),
  UNIQUE(session_id, student_id, question_id)
);

CREATE TABLE IF NOT EXISTS results (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id INTEGER NOT NULL REFERENCES test_sessions(id),
  student_id TEXT NOT NULL REFERENCES students(id),
  mcq_score INTEGER NOT NULL DEFAULT 0,
  mcq_max INTEGER NOT NULL DEFAULT 0,
  writing_score INTEGER,
  writing_max INTEGER,
  submitted_at TEXT,
  published_at TEXT,
  UNIQUE(session_id, student_id)
);
