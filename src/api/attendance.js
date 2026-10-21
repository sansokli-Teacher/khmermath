import { json, err } from '../lib/http.js';
import { needClass, TEACH_DENIED } from '../lib/access.js';
import { ensureColumns } from '../lib/schema.js';

const MARKS = new Set(['ok', 'A', 'L']);
export const MAX_PERIOD = 10;   // teaching periods in a school day

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
  return json({ class_id: Number(classId), day, period, rows: results });
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
