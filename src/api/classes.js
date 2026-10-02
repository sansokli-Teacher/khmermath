import { json, err } from '../lib/http.js';
import { requireTeacher } from '../lib/session.js';
import { hashSecretValue, randomPin } from '../lib/crypto.js';

export async function listClasses(req, env) {
  if (!(await requireTeacher(req, env))) return err('Not logged in.', 401);
  const { results } = await env.DB.prepare(
    `SELECT c.id, c.name, c.grade, COUNT(s.id) AS student_count
     FROM classes c LEFT JOIN students s ON s.class_id = c.id
     GROUP BY c.id ORDER BY c.grade, c.name`,
  ).all();
  return json({ classes: results });
}

export async function createClass(req, env) {
  if (!(await requireTeacher(req, env))) return err('Not logged in.', 401);
  const { name, grade } = await req.json();
  if (!name || !grade) return err('name and grade are required.', 400);
  const { meta } = await env.DB.prepare('INSERT INTO classes (name, grade) VALUES (?1, ?2)').bind(name, grade).run();
  return json({ id: meta.last_row_id, name, grade });
}

export async function listStudents(req, env, params) {
  if (!(await requireTeacher(req, env))) return err('Not logged in.', 401);
  const { results } = await env.DB.prepare('SELECT id, name FROM students WHERE class_id = ?1 ORDER BY name').bind(params.classId).all();
  return json({ students: results });
}

async function makeStudent(env, classId, id, name, secret) {
  const pin = randomPin(4);
  const pinHash = await hashSecretValue(pin, id, secret);
  await env.DB.prepare(
    'INSERT INTO students (id, class_id, name, pin_hash) VALUES (?1, ?2, ?3, ?4) ' +
    'ON CONFLICT(id) DO UPDATE SET class_id = ?2, name = ?3',
  ).bind(id, classId, name, pinHash).run();
  return { id, name, pin };
}

// Adds one student, returning the plain PIN once so the teacher can hand it out.
export async function addStudent(req, env, params) {
  if (!(await requireTeacher(req, env))) return err('Not logged in.', 401);
  const { id, name } = await req.json();
  if (!id || !name) return err('id and name are required.', 400);
  const student = await makeStudent(env, params.classId, String(id), name, env.SESSION_SECRET);
  return json(student);
}

// Bulk-imports a roster (e.g. pasted from the teacher's own list), generating a
// PIN for every student and returning the full list so it can be printed once
// and handed out.
export async function importRoster(req, env, params) {
  if (!(await requireTeacher(req, env))) return err('Not logged in.', 401);
  const { students } = await req.json();
  if (!Array.isArray(students) || students.length === 0) return err('students[] is required.', 400);
  const created = [];
  for (const s of students) {
    if (!s.id || !s.name) continue;
    created.push(await makeStudent(env, params.classId, String(s.id), s.name, env.SESSION_SECRET));
  }
  return json({ students: created });
}

export async function resetPin(req, env, params) {
  if (!(await requireTeacher(req, env))) return err('Not logged in.', 401);
  const pin = randomPin(4);
  const pinHash = await hashSecretValue(pin, params.studentId, env.SESSION_SECRET);
  const result = await env.DB.prepare('UPDATE students SET pin_hash = ?1 WHERE id = ?2').bind(pinHash, params.studentId).run();
  if (!result.meta.rows_written) return err('Student not found.', 404);
  return json({ id: params.studentId, pin });
}
