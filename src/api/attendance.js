import { json, err } from '../lib/http.js';
import { needClass, TEACH_DENIED } from '../lib/access.js';
import { ensureColumns } from '../lib/schema.js';

const MARKS = new Set(['ok', 'A', 'L']);
export const MAX_PERIOD = 11;   // teaching periods in a school day (the school timetable has 11)

export async function getAttendance(req, env) {
  const url = new URL(req.url);
  const classId = url.searchParams.get('class_id');
  const day = String(url.searchParams.get('day') || '').slice(0, 10);
  const period = Math.max(1, Math.min(MAX_PERIOD, Number(url.searchParams.get('period')) || 1));
  if (!classId || !/^\d{4}-\d{2}-\d{2}$/.test(day)) return err('class_id and day are required.', 400);
  await ensureColumns(env);
  const g = await needClass(req, env, classId, 'view'); if (g.resp) return g.resp;
  if (!g.t.teach) return err(TEACH_DENIED, 403);
  const { results } = await env.DB.prepare(
    'SELECT student_id, mark, note FROM attendance WHERE class_id = ?1 AND day = ?2 AND period = ?3',
  ).bind(Number(classId), day, period).all();
  const info = await env.DB.prepare('SELECT subject, topic FROM attendance_info WHERE class_id = ?1 AND day = ?2 AND period = ?3').bind(Number(classId), day, period).first();
  return json({ class_id: Number(classId), day, period, rows: results, info: info || { subject: null, topic: null } });
}

// The subject and the lesson planned for one period of one class: typed at the head of the period, saved on its own.
export async function saveAttendanceInfo(req, env) {
  const body = await req.json();
  const classId = Number(body.class_id);
  const day = String(body.day || '').slice(0, 10);
  const period = Math.max(1, Math.min(MAX_PERIOD, Number(body.period) || 1));
  if (!classId || !/^\d{4}-\d{2}-\d{2}$/.test(day)) return err('class_id and day are required.', 400);
  await ensureColumns(env);
  const g = await needClass(req, env, classId, 'edit'); if (g.resp) return g.resp;
  if (!g.t.teach) return err(TEACH_DENIED, 403);
  const subject = String(body.subject || '').trim().slice(0, 80) || null;
  const topic = String(body.topic || '').trim().slice(0, 300) || null;
  await env.DB.prepare(
    `INSERT INTO attendance_info (class_id, day, period, subject, topic, updated_at) VALUES (?1, ?2, ?3, ?4, ?5, datetime('now'))
     ON CONFLICT(class_id, day, period) DO UPDATE SET subject = excluded.subject, topic = excluded.topic, updated_at = excluded.updated_at`,
  ).bind(classId, day, period, subject, topic).run();
  return json({ ok: true });
}

export async function saveAttendance(req, env) {
  const body = await req.json();
  const classId = Number(body.class_id);
  const day = String(body.day || '').slice(0, 10);
  const period = Math.max(1, Math.min(MAX_PERIOD, Number(body.period) || 1));
  const rows = Array.isArray(body.rows) ? body.rows : [];
  if (!classId || !/^\d{4}-\d{2}-\d{2}$/.test(day)) return err('class_id and day are required.', 400);
  await ensureColumns(env);
  const g = await needClass(req, env, classId, 'edit'); if (g.resp) return g.resp;
  if (!g.t.teach) return err(TEACH_DENIED, 403);
  const ids = new Set((await env.DB.prepare('SELECT id FROM students WHERE class_id = ?1').bind(classId).all()).results.map((s) => String(s.id)));
  const stmts = [
    env.DB.prepare('DELETE FROM attendance WHERE class_id = ?1 AND day = ?2 AND period = ?3').bind(classId, day, period),
  ];
  for (const r of rows) {
    const sid = String(r.student_id || r.id || '').trim();
    if (!ids.has(sid)) continue;
    const mark = MARKS.has(r.mark) ? r.mark : 'ok';
    const note = String(r.note || '').slice(0, 400);
    stmts.push(env.DB.prepare(
      'INSERT INTO attendance (class_id, day, period, student_id, mark, note) VALUES (?1, ?2, ?3, ?4, ?5, ?6)',
    ).bind(classId, day, period, sid, mark, note));
  }
  await env.DB.batch(stmts);
  return json({ ok: true, saved: stmts.length - 1, day, period });
}

// Everything recorded for one class on one day: per period the lesson note, who was absent / late, and how many were present.
export async function getAttendanceDay(req, env) {
  const url = new URL(req.url);
  const classId = Number(url.searchParams.get('class_id'));
  const day = String(url.searchParams.get('day') || '').slice(0, 10);
  if (!classId || !/^\d{4}-\d{2}-\d{2}$/.test(day)) return err('class_id and day are required.', 400);
  await ensureColumns(env);
  const g = await needClass(req, env, classId, 'view'); if (g.resp) return g.resp;
  if (!g.t.teach) return err(TEACH_DENIED, 403);
  const { results: rows } = await env.DB.prepare(
    `SELECT a.period, a.mark, a.note, a.student_id, s.surname, s.first_name FROM attendance a LEFT JOIN students s ON s.id = a.student_id
     WHERE a.class_id = ?1 AND a.day = ?2 ORDER BY a.period, s.rowid`).bind(classId, day).all();
  const { results: infos } = await env.DB.prepare('SELECT period, subject, topic FROM attendance_info WHERE class_id = ?1 AND day = ?2').bind(classId, day).all();
  const by = new Map();
  const slot = (p) => { if (!by.has(p)) by.set(p, { period: p, recorded: false, subject: null, topic: null, present: 0, absent: [], late: [] }); return by.get(p); };
  for (const r of rows) {
    const s = slot(r.period); s.recorded = true;
    const name = `${r.surname || ''} ${r.first_name || ''}`.trim() || r.student_id;
    if (r.mark === 'A') s.absent.push(name); else if (r.mark === 'L') s.late.push(name); else s.present++;
  }
  for (const i of infos) { const s = slot(i.period); s.subject = i.subject; s.topic = i.topic; }
  return json({ class_id: classId, day, periods: [...by.values()].sort((x, y) => x.period - y.period) });
}
