import { json, err } from '../lib/http.js';
import { authTeacher, needClass, needStudent, needLicense, classAccess, accessibleClasses, limitResponse, trialUsage } from '../lib/access.js';
import { TRIAL } from '../lib/plans.js';

export async function listClasses(req, env) {
  const t = await authTeacher(req, env);
  if (!t) return err('Not logged in.', 401);
  const mine = await accessibleClasses(env, t);
  const { results } = await env.DB.prepare(
    `SELECT c.id, c.name, c.grade, c.owner_id, c.require_dob, COUNT(s.id) AS student_count,
            COALESCE(o.display_name, o.username) AS owner_name
     FROM classes c LEFT JOIN students s ON s.class_id = c.id LEFT JOIN teachers o ON o.id = c.owner_id
     GROUP BY c.id ORDER BY c.grade, c.name`,
  ).all();
  return json({ classes: results.filter((c) => mine.has(c.id)).map((c) => ({ ...c, my_role: mine.get(c.id) })) });
}

export async function createClass(req, env) {
  const g0 = await needLicense(req, env, true); if (g0.resp) return g0.resp;
  const t = g0.t;
  if (t.status === 'trial' && (await trialUsage(env, t)).classes >= TRIAL.classes) return limitResponse('ថ្នាក់', TRIAL.classes);
  const { name, grade } = await req.json();
  if (!name || !grade) return err('name and grade are required.', 400);
  const { meta } = await env.DB.prepare('INSERT INTO classes (name, grade, owner_id) VALUES (?1, ?2, ?3)').bind(name, grade, t.id).run();
  return json({ id: meta.last_row_id, name, grade });
}

export async function listStudents(req, env, params) {
  const g = await needClass(req, env, params.classId, 'view'); if (g.resp) return g.resp;
  const { results } = await env.DB.prepare(
    `SELECT s.id, s.surname, s.first_name, s.gender, s.dob, p.updated_at AS photo_v FROM students s
     LEFT JOIN student_photos p ON p.student_id = s.id WHERE s.class_id = ?1 ORDER BY s.surname, s.first_name`,
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
  if (g.t.status === 'trial' && (await trialUsage(env, g.t)).students >= TRIAL.students) return limitResponse('សិស្ស', TRIAL.students);
  const student = await makeStudent(env, g.t, params.classId, id, surname, first_name, gender, dob);
  if (student.conflict) return err(`អត្តលេខ ${student.conflict} មានក្នុងថ្នាក់របស់គ្រូផ្សេងរួចហើយ។`, 409);
  return json(student);
}

// Edits an existing student's surname, first name, gender, or dob.
export async function updateStudent(req, env, params) {
  const g = await needStudent(req, env, params.studentId, 'edit'); if (g.resp) return g.resp;
  const { id, surname, first_name, gender, dob } = await req.json();
  if (!surname || !first_name) return err('surname and first_name are required.', 400);
  const oldId = params.studentId;
  const newId = id === undefined || id === null ? oldId : String(id).trim();
  if (!newId || newId.length > 40 || /\s/.test(newId)) return err('Student ID must be 1-40 characters with no spaces.', 400);
  const update = env.DB.prepare('UPDATE students SET surname = ?1, first_name = ?2, gender = ?3, dob = ?4 WHERE id = ?5').bind(
    String(surname).trim(), String(first_name).trim(), gender ? String(gender).trim() : null, dob ? String(dob).trim() : null, oldId);
  if (newId === oldId) {
    const result = await update.run();
    if (!result.meta.rows_written) return err('Student not found.', 404);
    return json({ ok: true });
  }
  // A new ID: it must be free, and every table that points at the old one is moved over in the same batch (all or nothing).
  if (await env.DB.prepare('SELECT 1 FROM students WHERE id = ?1').bind(newId).first()) return err(`ID ${newId} is already used by another student.`, 409);
  let tables = [];
  try {
    // every table that has a student_id column (looked up with PRAGMA table_info, which D1 allows)
    const { results: all } = await env.DB.prepare("SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%' AND name NOT LIKE '_cf_%'").all();
    const names = all.map((x) => x.name).filter((n) => /^[A-Za-z0-9_]+$/.test(n));
    const infos = await env.DB.batch(names.map((n) => env.DB.prepare(`PRAGMA table_info(${n})`)));
    tables = names.filter((n, i) => (infos[i].results || []).some((c) => c.name === 'student_id'));
  } catch (e) { return err('Could not look up the tables that use student IDs: ' + (e && e.message ? e.message : e), 500); }
  const stmts = [env.DB.prepare('PRAGMA defer_foreign_keys = true'), update.bind(
    String(surname).trim(), String(first_name).trim(), gender ? String(gender).trim() : null, dob ? String(dob).trim() : null, oldId),
    env.DB.prepare('UPDATE students SET id = ?1 WHERE id = ?2').bind(newId, oldId),
    ...tables.map((t) => env.DB.prepare(`UPDATE ${t} SET student_id = ?1 WHERE student_id = ?2`).bind(newId, oldId))];
  try { await env.DB.batch(stmts); } catch (e) { return err('Could not change the ID: ' + (e && e.message ? e.message : e), 500); }
  return json({ ok: true, id: newId, tables: tables.length });
}

export async function deleteStudent(req, env, params) {
  const g = await needStudent(req, env, params.studentId, 'edit'); if (g.resp) return g.resp;
  await env.DB.prepare('DELETE FROM student_photos WHERE student_id = ?1').bind(params.studentId).run();   // a deleted student's photo goes too
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
  let room = Infinity;
  if (g.t.status === 'trial') {
    room = TRIAL.students - (await trialUsage(env, g.t)).students;
    if (room <= 0) return limitResponse('សិស្ស', TRIAL.students);
  }
  for (const s of students) {
    if (created.length >= room) { skipped.push(`${s.id} (លើសកំណត់សាកល្បង)`); continue; }
    if (!s.id || !s.surname || !s.first_name) continue;
    const r = await makeStudent(env, g.t, params.classId, s.id, s.surname, s.first_name, s.gender, s.dob);
    if (r.conflict) skipped.push(r.conflict); else created.push(r);
  }
  return json({ students: created, skipped });
}

export async function deleteClass(req, env, params) {
  const g = await needClass(req, env, params.classId, 'own'); if (g.resp) return g.resp;
  const classId = params.classId;
  await env.DB.prepare('DELETE FROM student_photos WHERE student_id IN (SELECT id FROM students WHERE class_id = ?1)').bind(classId).run();
  await env.DB.prepare('DELETE FROM students WHERE class_id = ?1').bind(classId).run();
  await env.DB.prepare('DELETE FROM test_sessions WHERE class_id = ?1').bind(classId).run();
  await env.DB.prepare("DELETE FROM shares WHERE resource_type = 'class' AND resource_id = ?1").bind(classId).run();
  const result = await env.DB.prepare('DELETE FROM classes WHERE id = ?1').bind(classId).run();
  if (!result.meta.rows_written) return err('Class not found.', 404);
  return json({ ok: true });
}

export async function classSettings(req, env, params) {
  const g = await needClass(req, env, params.classId, 'edit'); if (g.resp) return g.resp;
  const { require_dob } = await req.json();
  await env.DB.prepare('UPDATE classes SET require_dob = ?1 WHERE id = ?2').bind(require_dob ? 1 : 0, params.classId).run();
  return json({ ok: true });
}
