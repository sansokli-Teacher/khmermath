// Exam integrity: what the student's browser reports, what the system does about it,
// and what the teacher sees. A web page cannot stop an operating-system screenshot or an
// AI overlay, so this is deterrence + detection + a record — see the policy per session:
//   log   — record only
//   warn  — record, and show the student a warning each time
//   lock  — record, warn, and hide the questions after max_violations incidents until the
//           teacher unlocks the student
import { json, err } from '../lib/http.js';
import { requireStudent } from '../lib/session.js';
import { needSession } from '../lib/access.js';
import { ensureColumns } from '../lib/schema.js';
import { allow } from '../lib/limits.js';
import { audit } from '../lib/audit.js';

// kind -> does this one count as an incident? (true | min duration in ms | false = log only)
const COUNTS = {
  tab_hidden: 2000, window_blur: 4000, fullscreen_exit: true, split_view: true, copy: true, cut: true,
  contextmenu: true, shortcut: true, print: true, devtools: true, second_tab: true, drag: true, selection: false, second_device: false,
  online: false, offline: false, fullscreen_enter: false, focus_back: false, start: false, resume: false,
};
export const KINDS = Object.keys(COUNTS);
const GAP_MS = 3000;   // one action often fires several events (blur + hidden): count once

export function counts(kind, dur) {
  const rule = COUNTS[kind];
  if (rule === true) return true;
  if (typeof rule === 'number') return (dur || 0) >= rule;
  return false;
}

// Whether one reported event is an incident, once we know what device it came from. A phone fires «contextmenu» on any long press and
// «split_view» when its keyboard or browser bar changes the window height; those are not cheating (6 of 36 students were locked by them on exam day).
const MOBILE = /Mobile|Android|iPhone|iPad|iPod/i;
export function countsEvent(kind, dur, detail, ua) {
  if (!counts(kind, dur)) return false;
  const mobile = MOBILE.test(String(ua || ''));
  if (kind === 'contextmenu' && mobile) return false;
  if (kind === 'split_view') {                                   // «WxH from WxH»: only a real narrowing of the window counts
    const m = /(\d+)x(\d+) from (\d+)x(\d+)/.exec(String(detail || ''));
    if (m && !(Number(m[1]) < Number(m[3]) * 0.75)) return false;
  }
  return true;
}

async function studentSession(req, env) {
  const s = await requireStudent(req, env);
  if (!s) return null;
  await ensureColumns(env);
  return s;
}

export async function postEvents(req, env) {
  const stu = await studentSession(req, env);
  if (!stu) return err('Not logged in.', 401);
  const body = await req.json().catch(() => ({}));
  const sessionId = Number(body.session_id);
  const ses = await env.DB.prepare('SELECT id, class_id, integrity_mode, max_violations FROM test_sessions WHERE id = ?1 AND class_id = ?2').bind(sessionId, stu.classId).first();
  const res = ses && await env.DB.prepare('SELECT id, violations, lock_base, locked, submitted_at FROM results WHERE session_id = ?1 AND student_id = ?2').bind(sessionId, stu.id).first();
  if (!res || res.submitted_at) return json({ ok: true });
  if (!(await allow(env, `ev:${sessionId}:${stu.id}`, 120, 60))) return json({ ok: true, throttled: true });

  const ua = req.headers.get('User-Agent') || '';
  const list = (Array.isArray(body.events) ? body.events : []).slice(0, 40);
  const last = await env.DB.prepare('SELECT at FROM exam_events WHERE session_id = ?1 AND student_id = ?2 AND counted = 1 ORDER BY id DESC LIMIT 1').bind(sessionId, stu.id).first();
  let lastCounted = last ? Date.parse(last.at.replace(' ', 'T') + 'Z') : 0;
  let violations = res.violations;
  const stmts = [];
  for (const e of list) {
    const kind = String(e.kind || '');
    if (!KINDS.includes(kind)) continue;
    const dur = Math.max(0, Math.min(Number(e.dur_ms) || 0, 6 * 3600 * 1000));
    // the client's own timestamp is trusted only within a minute of now (a phone clock can be wrong)
    const t = Number(e.t) && Math.abs(Date.now() - Number(e.t)) < 60000 ? Number(e.t) : Date.now();
    let counted = 0;
    if (countsEvent(kind, dur, e.detail, ua) && t - lastCounted >= GAP_MS) { counted = 1; lastCounted = t; violations++; }
    stmts.push(env.DB.prepare('INSERT INTO exam_events (session_id, student_id, at, kind, detail, dur_ms, counted) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7)')
      .bind(sessionId, stu.id, new Date(t).toISOString().replace('T', ' ').slice(0, 19), kind, e.detail ? String(e.detail).slice(0, 120) : null, dur || null, counted));
  }
  let locked = !!res.locked;
  if (!locked && ses.integrity_mode === 'lock' && violations - res.lock_base >= ses.max_violations) {
    locked = true;
    stmts.push(env.DB.prepare("UPDATE results SET locked = 1, lock_reason = ?3 WHERE session_id = ?1 AND student_id = ?2").bind(sessionId, stu.id, `${violations - res.lock_base} incidents`));
    stmts.push(env.DB.prepare("INSERT INTO exam_events (session_id, student_id, kind, detail) VALUES (?1, ?2, 'locked', ?3)").bind(sessionId, stu.id, `auto-lock after ${violations - res.lock_base} incidents`));
  }
  if (violations !== res.violations) stmts.push(env.DB.prepare('UPDATE results SET violations = ?3 WHERE session_id = ?1 AND student_id = ?2').bind(sessionId, stu.id, violations));
  if (stmts.length) await env.DB.batch(stmts);
  return json({ ok: true, violations, since_unlock: violations - res.lock_base, max: ses.max_violations, mode: ses.integrity_mode, locked });
}

// ---------- teacher ----------
export async function setIntegrity(req, env, params) {
  const g = await needSession(req, env, params.sessionId, 'edit'); if (g.resp) return g.resp;
  await ensureColumns(env);
  const { mode, max_violations } = await req.json();
  if (!['log', 'warn', 'lock'].includes(mode)) return err('mode must be log, warn or lock.', 400);
  const max = Math.max(1, Math.min(20, Number(max_violations) || 3));
  await env.DB.prepare('UPDATE test_sessions SET integrity_mode = ?1, max_violations = ?2 WHERE id = ?3').bind(mode, max, g.ses.id).run();
  await audit(env, g.t, 'session.integrity', `session ${g.ses.id}: ${mode}/${max}`);
  return json({ ok: true, mode, max_violations: max });
}

export async function lockStudent(req, env, params) {
  const g = await needSession(req, env, params.sessionId, 'edit'); if (g.resp) return g.resp;
  await ensureColumns(env);
  const body = await req.json();
  const { student_id, locked, note } = body;
  if (!student_id) return err('student_id is required.', 400);
  const row = await env.DB.prepare('SELECT violations FROM results WHERE session_id = ?1 AND student_id = ?2').bind(g.ses.id, student_id).first();
  if (!row) return err('Student has not started.', 404);
  const who = g.t.display_name || g.t.username;
  let given = 0;
  if (locked) {
    await env.DB.batch([
      env.DB.prepare("UPDATE results SET locked = 1, lock_reason = ?3 WHERE session_id = ?1 AND student_id = ?2").bind(g.ses.id, student_id, `by ${who}`),
      env.DB.prepare("INSERT INTO exam_events (session_id, student_id, kind, detail) VALUES (?1, ?2, 'locked', ?3)").bind(g.ses.id, student_id, `locked by ${who}`),
    ]);
  } else {
    given = body.compensate === false ? 0 : await giveBackLockedTime(env, g.ses.id, student_id);
    await env.DB.batch([
      env.DB.prepare("UPDATE results SET locked = 0, lock_reason = NULL, lock_base = violations WHERE session_id = ?1 AND student_id = ?2").bind(g.ses.id, student_id),
      env.DB.prepare("INSERT INTO exam_events (session_id, student_id, kind, detail) VALUES (?1, ?2, 'unlocked', ?3)").bind(g.ses.id, student_id, `unlocked by ${who}${note ? ': ' + String(note).slice(0, 80) : ''}`),
    ]);
  }
  await audit(env, g.t, locked ? 'session.lock' : 'session.unlock', `session ${g.ses.id}, ${student_id}`);
  return json({ ok: true, ...(locked ? {} : { given_back: typeof given === 'number' ? given : 0 }) });
}

// While a student was locked their clock kept running; unlocking gives that time back (1–30 minutes, once per lock).
export async function giveBackLockedTime(env, sessionId, studentId) {
  const ev = await env.DB.prepare("SELECT at FROM exam_events WHERE session_id = ?1 AND student_id = ?2 AND kind = 'locked' ORDER BY id DESC LIMIT 1").bind(sessionId, studentId).first();
  if (!ev) return 0;
  const since = Math.ceil((Date.now() - Date.parse(ev.at.replace(' ', 'T') + 'Z')) / 60000);
  const m = Math.max(1, Math.min(30, since));
  await env.DB.prepare('UPDATE results SET extra_minutes = extra_minutes + ?3 WHERE session_id = ?1 AND student_id = ?2').bind(sessionId, studentId, m).run();
  return m;
}

// Unlock every locked student of a session in one go (each gets their locked minutes back).
export async function unlockAll(req, env, params) {
  const g = await needSession(req, env, params.sessionId, 'edit'); if (g.resp) return g.resp;
  await ensureColumns(env);
  const { results } = await env.DB.prepare('SELECT student_id FROM results WHERE session_id = ?1 AND locked = 1 AND submitted_at IS NULL').bind(g.ses.id).all();
  const who = g.t.display_name || g.t.username;
  let minutes = 0;
  for (const r of results) {
    minutes += await giveBackLockedTime(env, g.ses.id, r.student_id);
    await env.DB.batch([
      env.DB.prepare("UPDATE results SET locked = 0, lock_reason = NULL, lock_base = violations WHERE session_id = ?1 AND student_id = ?2").bind(g.ses.id, r.student_id),
      env.DB.prepare("INSERT INTO exam_events (session_id, student_id, kind, detail) VALUES (?1, ?2, 'unlocked', ?3)").bind(g.ses.id, r.student_id, `unlocked by ${who} (all)`),
    ]);
  }
  await audit(env, g.t, 'session.unlock_all', `session ${g.ses.id}, ${results.length} students`);
  return json({ ok: true, count: results.length, minutes });
}


export async function studentActivity(req, env, params) {
  const g = await needSession(req, env, params.sessionId, 'view'); if (g.resp) return g.resp;
  await ensureColumns(env);
  const sid = new URL(req.url).searchParams.get('student_id');
  if (!sid) return err('student_id is required.', 400);
  const [{ results: events }, { results: notes }, res] = await Promise.all([
    env.DB.prepare('SELECT id, at, kind, detail, dur_ms, counted FROM exam_events WHERE session_id = ?1 AND student_id = ?2 ORDER BY id').bind(g.ses.id, sid).all(),
    env.DB.prepare('SELECT id, author, body, created_at FROM session_notes WHERE session_id = ?1 AND student_id = ?2 ORDER BY id').bind(g.ses.id, sid).all(),
    env.DB.prepare('SELECT violations, locked, lock_reason, tab_switches, started_at, submitted_at FROM results WHERE session_id = ?1 AND student_id = ?2').bind(g.ses.id, sid).first(),
  ]);
  return json({ events, notes, result: res });
}

export async function addSessionNote(req, env, params) {
  const g = await needSession(req, env, params.sessionId, 'edit'); if (g.resp) return g.resp;
  await ensureColumns(env);
  const { student_id, body } = await req.json();
  const text = String(body || '').trim().slice(0, 600);
  if (!student_id || !text) return err('student_id and body are required.', 400);
  await env.DB.prepare('INSERT INTO session_notes (session_id, student_id, teacher_id, author, body) VALUES (?1, ?2, ?3, ?4, ?5)')
    .bind(g.ses.id, student_id, g.t.id, g.t.display_name || g.t.username, text).run();
  return json({ ok: true });
}

export async function deleteSessionNote(req, env, params) {
  const g = await needSession(req, env, params.sessionId, 'edit'); if (g.resp) return g.resp;
  await env.DB.prepare('DELETE FROM session_notes WHERE id = ?1 AND session_id = ?2').bind(Number(params.noteId), g.ses.id).run();
  return json({ ok: true });
}
