// Exam-day safety: readiness checklist, publish preview, backup restore.
import { json, err } from '../lib/http.js';
import { ensureColumns } from '../lib/schema.js';
import { needClass, needTest, needSession, needAdmin } from '../lib/access.js';
import { checkReadiness } from '../lib/readiness.js';
import { sessionQuestions, mcqOnly } from '../lib/frozen.js';
import { finalizeSession } from './sessions.js';
import { sessionWindow } from '../lib/time.js';
import { getBackupFile } from '../lib/backup.js';
import { audit } from '../lib/audit.js';
import { gunzipJson, validateBackup, planRestore, applyRestore } from '../lib/restore.js';

// Before scheduling: values come from the form.
export async function readiness(req, env) {
  const q = new URL(req.url).searchParams;
  const g1 = await needClass(req, env, Number(q.get('class_id')), 'view'); if (g1.resp) return g1.resp;
  const g2 = await needTest(req, env, Number(q.get('test_id')), 'view'); if (g2.resp) return g2.resp;
  const start = q.get('start'), dur = Number(q.get('duration')) || 0;
  const end = q.get('end') || new Date(Date.parse(start) + dur * 60000).toISOString();
  return json(await checkReadiness(env, { testId: Number(q.get('test_id')), classId: Number(q.get('class_id')), startIso: start, endIso: end, durationMin: dur, pin: q.get('pin') }));
}

// An already scheduled session.
export async function sessionReadiness(req, env, params) {
  const g = await needSession(req, env, params.sessionId, 'view'); if (g.resp) return g.resp;
  await ensureColumns(env);
  const s = await env.DB.prepare('SELECT * FROM test_sessions WHERE id = ?1').bind(g.ses.id).first();
  const end = s.scheduled_end || new Date(Date.parse(s.scheduled_start) + s.duration_minutes * 60000).toISOString();
  return json(await checkReadiness(env, { testId: s.test_id, classId: s.class_id, startIso: s.scheduled_start, endIso: end, durationMin: s.duration_minutes, pin: s.pin, sessionId: s.id }));
}

// What publishing will show students, before it happens.
export async function publishPreview(req, env, params) {
  const g = await needSession(req, env, params.sessionId, 'view'); if (g.resp) return g.resp;
  await ensureColumns(env);
  const s = await env.DB.prepare('SELECT * FROM test_sessions WHERE id = ?1').bind(g.ses.id).first();
  const end = s.scheduled_end || new Date(Date.parse(s.scheduled_start) + s.duration_minutes * 60000).toISOString();
  if (sessionWindow({ ...s, scheduled_end: end }).phase === 'closed') await finalizeSession(env, s.id, end);
  const qs = await sessionQuestions(env, s.id, s.test_id);
  const mcq = mcqOnly(qs);
  const hasWriting = qs.some((q) => q.kind === 'writing');
  const mcqMax = mcq.reduce((t, q) => t + q.points, 0);
  const { results: roster } = await env.DB.prepare(
    `SELECT st.id, st.surname, st.first_name, r.mcq_score, r.writing_score, r.writing_max, r.submitted_at, r.published_at
     FROM students st LEFT JOIN results r ON r.student_id = st.id AND r.session_id = ?1 WHERE st.class_id = ?2 ORDER BY st.surname, st.first_name`,
  ).bind(s.id, s.class_id).all();
  const submitted = roster.filter((r) => r.submitted_at);
  const students = submitted.map((r) => {
    const total = (r.mcq_score ?? 0) + (r.writing_score ?? 0);
    const max = mcqMax + (r.writing_max ?? 0);
    return { id: r.id, name: `${r.surname} ${r.first_name}`, total, max, pct: max > 0 ? Math.round((total / max) * 100) : 0, writing_missing: hasWriting && r.writing_score == null, published: !!r.published_at };
  });
  const pcts = students.map((x) => x.pct);
  return json({
    session_id: s.id, phase: sessionWindow({ ...s, scheduled_end: end }).phase,
    class_size: roster.length, submitted: submitted.length, absent: roster.length - submitted.length,
    already_published: students.filter((x) => x.published).length,
    writing_missing: students.filter((x) => x.writing_missing).length, has_writing: hasWriting,
    mcq_total: mcq.length, mcq_with_explanation: mcq.filter((q) => q.solution_text && String(q.solution_text).trim()).length,
    cancelled: qs.filter((q) => q.cancelled).length,
    avg_pct: pcts.length ? Math.round(pcts.reduce((a, b) => a + b, 0) / pcts.length) : null,
    min_pct: pcts.length ? Math.min(...pcts) : null, max_pct: pcts.length ? Math.max(...pcts) : null,
    students,
  });
}

// ---------- restore (owner only) ----------
async function loadBackup(req, env) {
  const id = Number(new URL(req.url).searchParams.get('backup_id'));
  let bytes;
  if (id) {
    const f = await getBackupFile(env, id);
    if (!f) throw new Error('រកមិនឃើញការបម្រុងទុកនេះទេ។');
    bytes = f.bytes;
  } else {
    bytes = new Uint8Array(await req.arrayBuffer());
    if (!bytes.length) throw new Error('សូមជ្រើសរើសឯកសារបម្រុងទុក (.json.gz)។');
  }
  try { return validateBackup(await gunzipJson(bytes)); }
  catch (e) { throw new Error(e.message && /បម្រុងទុក|តារាង/.test(e.message) ? e.message : 'ឯកសារបម្រុងទុកមិនអាចអានបានទេ។'); }
}
export async function restoreVerify(req, env) {
  const g = await needAdmin(req, env); if (g.resp) return g.resp;
  try { return json(await planRestore(env, await loadBackup(req, env))); } catch (e) { return err(e.message, 400); }
}
export async function restoreApply(req, env) {
  const g = await needAdmin(req, env); if (g.resp) return g.resp;
  if (new URL(req.url).searchParams.get('confirm') !== 'RESTORE') return err('Missing confirmation.', 400);
  try { return json({ ok: true, ...(await applyRestore(env, await loadBackup(req, env))) }); } catch (e) { return err(e.message, 400); }
}

// Take results back off the students' screens (e.g. published too early).
export async function unpublishSession(req, env, params) {
  const g = await needSession(req, env, params.sessionId, 'edit'); if (g.resp) return g.resp;
  await ensureColumns(env);
  const r = await env.DB.prepare('UPDATE results SET published_at = NULL WHERE session_id = ?1 AND published_at IS NOT NULL').bind(g.ses.id).run();
  await audit(env, g.t, 'session.unpublish', `session ${g.ses.id}`);
  return json({ ok: true, count: r.meta.changes ?? 0 });
}
