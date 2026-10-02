import { json, err } from '../lib/http.js';
import { requireTeacher } from '../lib/session.js';

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
  const { results } = await env.DB.prepare(
    'SELECT id, surname, first_name FROM students WHERE class_id = ?1 ORDER BY surname, first_name',
  ).bind(params.classId).all();
  return json({ students: results });
}

async function makeStudent(env, classId, id, surname, firstName) {
  await env.DB.prepare(
    'INSERT INTO students (id, class_id, surname, first_name) VALUES (?1, ?2, ?3, ?4) ' +
    'ON CONFLICT(id) DO UPDATE SET class_id = ?2, surname = ?3, first_name = ?4',
  ).bind(id, classId, surname, firstName).run();
  return { id, surname, first_name: firstName };
}

export async function addStudent(req, env, params) {
  if (!(await requireTeacher(req, env))) return err('Not logged in.', 401);
  const { id, surname, first_name } = await req.json();
  if (!id || !surname || !first_name) return err('id, surname, and first_name are required.', 400);
  const student = await makeStudent(env, params.classId, String(id), surname, first_name);
  return json(student);
}

// Edits an existing student's surname/first name. Changing the id moves the
// row to a new primary key, so responses/results tied to the old id
// (referenced by student_id) would be orphaned — refuse that case rather
// than silently losing history.
export async function updateStudent(req, env, params) {
  if (!(await requireTeacher(req, env))) return err('Not logged in.', 401);
  const { id, surname, first_name } = await req.json();
  if (!surname || !first_name) return err('surname and first_name are required.', 400);
  if (id && String(id) !== params.studentId) return err('Changing a student\'s ID is not supported — add them again under the new ID instead.', 400);
  const result = await env.DB.prepare('UPDATE students SET surname = ?1, first_name = ?2 WHERE id = ?3')
    .bind(surname, first_name, params.studentId).run();
  if (!result.meta.rows_written) return err('Student not found.', 404);
  return json({ ok: true });
}

// Bulk-imports a roster (e.g. pasted from the teacher's own list, or straight
// from a spreadsheet).
export async function importRoster(req, env, params) {
  if (!(await requireTeacher(req, env))) return err('Not logged in.', 401);
  const { students } = await req.json();
  if (!Array.isArray(students) || students.length === 0) return err('students[] is required.', 400);
  const created = [];
  for (const s of students) {
    if (!s.id || !s.surname || !s.first_name) continue;
    created.push(await makeStudent(env, params.classId, String(s.id), s.surname, s.first_name));
  }
  return json({ students: created });
}
