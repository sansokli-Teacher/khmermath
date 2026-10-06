import { json, err } from '../lib/http.js';
import { authTeacher, needClass, needStudent, classAccess, accessibleClasses } from '../lib/access.js';

export async function listClasses(req, env) {
  const t = await authTeacher(req, env);
  if (!t) return err('Not logged in.', 401);
  const mine = await accessibleClasses(env, t);
  const { results } = await env.DB.prepare(
    `SELECT c.id, c.name, c.grade, c.owner_id, COUNT(s.id) AS student_count,
            COALESCE(o.display_name, o.username) AS owner_name
     FROM classes c LEFT JOIN students s ON s.class_id = c.id LEFT JOIN teachers o ON o.id = c.owner_id
     GROUP BY c.id ORDER BY c.grade, c.name`,
  ).all();
  return json({ classes: results.filter((c) => mine.has(c.id)).map((c) => ({ ...c, my_role: mine.get(c.id) })) });
}

export async function createClass(req, env) {
  const t = await authTeacher(req, env);
  if (!t) return err('Not logged in.', 401);
  const { name, grade } = await req.json();
  if (!name || !grade) return err('name and grade are required.', 400);
  const { meta } = await env.DB.prepare('INSERT INTO classes (name, grade, owner_id) VALUES (?1, ?2, ?3)').bind(name, grade, t.id).run();
  return json({ id: meta.last_row_id, name, grade });
}

export async function listStudents(req, env, params) {
  const g = await needClass(req, env, params.classId, 'view'); if (g.resp) return g.resp;
  const { results } = await env.DB.prepare(
    'SELECT id, surname, first_name, gender, dob FROM students WHERE class_id = ?1 ORDER BY surname, first_name',
  ).bind(params.classId).all();
  return json({ students: results });
}

// Student ids are global (students log in with the id alone). A teacher may not
// take over an id that already belongs to a class she cannot edit.
async function makeStudent(env, t, classId, id, surname, firstName, gender = null, dob = null) {
  const cleanId = String(id).trim();
  const existing = await env.DB.prepare('SELECT class_id FROM students WHERE id = ?1').bind(cleanId).first();
  if (existing && existing.class_id !== Number(classId)) {
    const acc = await classAccess(env, t, existing.class_id);
    if (acc !== 'owner' && acc !== 'editor') return { conflict: cleanId };
  }
  const cleanSurname = String(surname).trim();
  const cleanFirst = String(firstName).trim();
  const cleanGender = gender ? String(gender).trim() : null;
  const cleanDob = dob ? String(dob).trim() : null;

  await env.DB.prepare(
    'INSERT INTO students (id, class_id, surname, first_name, gender, dob) VALUES (?1, ?2, ?3, ?4, ?5, ?6) ' +
    'ON CONFLICT(id) DO UPDATE SET class_id = ?2, surname = ?3, first_name = ?4, gender = ?5, dob = ?6',
  ).bind(cleanId, classId, cleanSurname, cleanFirst, cleanGender, cleanDob).run();

  return { id: cleanId, surname: cleanSurname, first_name: cleanFirst, gender: cleanGender, dob: cleanDob };
}

export async function addStudent(req, env, params) {
  const g = await needClass(req, env, params.classId, 'edit'); if (g.resp) return g.resp;
  const { id, surname, first_name, gender, dob } = await req.json();
  if (!id || !surname || !first_name) return err('id, surname, and first_name are required.', 400);
  const student = await makeStudent(env, g.t, params.classId, id, surname, first_name, gender, dob);
  if (student.conflict) return err(`អត្តលេខ ${student.conflict} មានក្នុងថ្នាក់របស់គ្រូផ្សេងរួចហើយ។`, 409);
  return json(student);
}

// Edits an existing student's surname, first name, gender, or dob.
export async function updateStudent(req, env, params) {
  const g = await needStudent(req, env, params.studentId, 'edit'); if (g.resp) return g.resp;
  const { id, surname, first_name, gender, dob } = await req.json();
  if (!surname || !first_name) return err('surname and first_name are required.', 400);
  if (id && String(id) !== params.studentId) return err("Changing a student's ID is not supported — add them again under the new ID instead.", 400);
  const result = await env.DB.prepare(
    'UPDATE students SET surname = ?1, first_name = ?2, gender = ?3, dob = ?4 WHERE id = ?5'
  ).bind(
    String(surname).trim(),
    String(first_name).trim(),
    gender ? String(gender).trim() : null,
    dob ? String(dob).trim() : null,
    params.studentId
  ).run();
  if (!result.meta.rows_written) return err('Student not found.', 404);
  return json({ ok: true });
}

export async function deleteStudent(req, env, params) {
  const g = await needStudent(req, env, params.studentId, 'edit'); if (g.resp) return g.resp;
  const result = await env.DB.prepare('DELETE FROM students WHERE id = ?1').bind(params.studentId).run();
  if (!result.meta.rows_written) return err('Student not found.', 404);
  return json({ ok: true });
}

// Bulk-imports a roster from Excel, CSV, or text paste
export async function importRoster(req, env, params) {
  const g = await needClass(req, env, params.classId, 'edit'); if (g.resp) return g.resp;
  const { students } = await req.json();
  if (!Array.isArray(students) || students.length === 0) return err('students[] is required.', 400);
  const created = [];
  const skipped = [];
  for (const s of students) {
    if (!s.id || !s.surname || !s.first_name) continue;
    const r = await makeStudent(env, g.t, params.classId, s.id, s.surname, s.first_name, s.gender, s.dob);
    if (r.conflict) skipped.push(r.conflict); else created.push(r);
  }
  return json({ students: created, skipped });
}

export async function deleteClass(req, env, params) {
  const g = await needClass(req, env, params.classId, 'own'); if (g.resp) return g.resp;
  const classId = params.classId;
  await env.DB.prepare('DELETE FROM students WHERE class_id = ?1').bind(classId).run();
  await env.DB.prepare('DELETE FROM test_sessions WHERE class_id = ?1').bind(classId).run();
  await env.DB.prepare("DELETE FROM shares WHERE resource_type = 'class' AND resource_id = ?1").bind(classId).run();
  const result = await env.DB.prepare('DELETE FROM classes WHERE id = ?1').bind(classId).run();
  if (!result.meta.rows_written) return err('Class not found.', 404);
  return json({ ok: true });
}
