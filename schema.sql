-- Exam Khmer — D1 schema.
-- Apply with: npx wrangler d1 execute exam-khmer --remote --file schema.sql

-- Question images, stored as base64 in D1 (no R2 bucket needed — R2 requires a
-- one-time "enable" step in the Cloudflare dashboard that we're skipping for now).
CREATE TABLE IF NOT EXISTS images (
  key TEXT PRIMARY KEY,
  content_type TEXT NOT NULL,
  data_base64 TEXT NOT NULL
);

-- One shared value the teacher sets (currently just the one student login
-- PIN, used by every student) — a tiny key/value table rather than a column
-- on some other table, so more settings can be added later without another
-- migration.
CREATE TABLE IF NOT EXISTS settings (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL
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

-- Login is id + the one shared PIN in `settings` (not a per-student PIN).
CREATE TABLE IF NOT EXISTS students (
  id TEXT PRIMARY KEY,      -- the existing student id, e.g. "0109293"
  class_id INTEGER NOT NULL REFERENCES classes(id),
  surname TEXT NOT NULL,    -- គោត្តនាម (Family name / Surname)
  first_name TEXT NOT NULL, -- នាម (First name / Given name)
  gender TEXT,              -- ភេទ (optional: e.g. "ប្រុស", "ស្រី", "M", "F")
  dob TEXT                  -- ថ្ងៃខែឆ្នាំកំណើត (optional: e.g. "YYYY-MM-DD")
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

-- Questions as they were when an exam session started (see src/lib/frozen.js).
CREATE TABLE IF NOT EXISTS session_questions (
  session_id INTEGER NOT NULL,
  question_id INTEGER NOT NULL,
  order_no INTEGER NOT NULL,
  kind TEXT NOT NULL DEFAULT 'mcq',
  stem_text TEXT NOT NULL,
  image_key TEXT,
  options_json TEXT NOT NULL,
  correct_index INTEGER NOT NULL,
  alt_correct_index INTEGER,
  cancelled INTEGER NOT NULL DEFAULT 0,
  points REAL NOT NULL DEFAULT 1,
  solution_text TEXT,
  topic TEXT,
  level TEXT,
  shuffle INTEGER NOT NULL DEFAULT 0,
  params TEXT,
  frozen_at TEXT NOT NULL DEFAULT (datetime('now')),
  PRIMARY KEY (session_id, question_id)
);

CREATE TABLE IF NOT EXISTS exam_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id INTEGER NOT NULL,
  student_id TEXT NOT NULL,
  at TEXT NOT NULL DEFAULT (datetime('now')),
  kind TEXT NOT NULL,
  detail TEXT,
  dur_ms INTEGER,
  counted INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_events_session ON exam_events(session_id, student_id, id);
CREATE TABLE IF NOT EXISTS session_notes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id INTEGER NOT NULL,
  student_id TEXT NOT NULL,
  teacher_id INTEGER,
  author TEXT,
  body TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
-- (policy columns on test_sessions / results are added by ensureColumns in src/lib/schema.js)
