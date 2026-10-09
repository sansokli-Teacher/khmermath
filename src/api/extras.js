// Practice + progress for students; suspicion indicators, fast writing marking, image cleanup and
// backup self-check for teachers/owner.
import { json, err } from '../lib/http.js';
import { requireStudent } from '../lib/session.js';
import { needSession, needAdmin } from '../lib/access.js';
import { ensureColumns } from '../lib/schema.js';
import { sessionQuestions, mcqOnly } from '../lib/frozen.js';
import { instantiate } from '../lib/variants.js';
import { isRight } from '../lib/scoring.js';
import { audit } from '../lib/audit.js';
import { selfCheck } from '../lib/restore.js';

// ---------- students ----------
async function publishedAttempts(env, studentId, order, limit) {
  const { results } = await env.DB.prepare(
    `SELECT r.session_id, r.mcq_score, r.mcq_max, r.writing_score, r.writing_max, ts.test_id, ts.scheduled_start, t.title
     FROM results r JOIN test_sessions ts ON ts.id = r.session_id JOIN tests t ON t.id = ts.test_id
     WHERE r.student_id = ?1 AND r.published_at IS NOT NULL AND r.submitted_at IS NOT NULL
     ORDER BY ts.scheduled_start ${order} LIMIT ${limit}`,
  ).bind(studentId).all();
  return results;
}
async function answersOf(env, sessionId, studentId) {
  const { results } = await env.DB.prepare('SELECT question_id, selected_index FROM responses WHERE session_id = ?1 AND student_id = ?2').bind(sessionId, studentId).all();
  return Object.fromEntries(results.map((r) => [r.question_id, r.selected_index]));
}

// Questions this student got wrong (or left blank) in exams whose results are published.
export async function practice(req, env) {
  const stu = await requireStudent(req, env);
  if (!stu) return err('Not logged in.', 401);
  await ensureColumns(env);
  const items = [];
  const out = () => json({ student_id: stu.id, items });
  for (const a of await publishedAttempts(env, stu.id, 'DESC', 12)) {
    const chosen = await answersOf(env, a.session_id, stu.id);
    for (const q0 of mcqOnly(await sessionQuestions(env, a.session_id, a.test_id))) {
      if (q0.cancelled || isRight(q0, chosen[q0.id] ?? null)) continue;
      const q = instantiate(q0, a.session_id, stu.id);
      items.push({
        key: `${a.session_id}:${q0.id}`, test_title: a.title, date: a.scheduled_start, topic: q0.topic, level: q0.level,
        stem_text: q.stem_text, image_key: q.image_key, options: JSON.parse(q.options_json),
        correct_index: q0.correct_index, alt_correct_index: q0.alt_correct_index, solution_text: q.solution_text,
        blank: chosen[q0.id] == null,
      });
      if (items.length >= 300) return out();
    }
  }
  return out();
}

// Scores over time, overall and per topic, from published results only.
export async function progress(req, env) {
  const stu = await requireStudent(req, env);
  if (!stu) return err('Not logged in.', 401);
  await ensureColumns(env);
  const attempts = (await publishedAttempts(env, stu.id, 'DESC', 24)).reverse();
  const exams = [], topics = {};
  let wrongCount = 0;
  for (const a of attempts.slice(-12)) {
    const ch = await answersOf(env, a.session_id, stu.id);
    for (const q of mcqOnly(await sessionQuestions(env, a.session_id, a.test_id))) if (!q.cancelled && !isRight(q, ch[q.id] ?? null)) wrongCount++;
  }
  for (const a of attempts) {
    const total = (a.mcq_score ?? 0) + (a.writing_score ?? 0), max = (a.mcq_max ?? 0) + (a.writing_max ?? 0);
    exams.push({ session_id: a.session_id, title: a.title, date: a.scheduled_start, pct: max > 0 ? Math.round((total / max) * 100) : null });
    const chosen = await answersOf(env, a.session_id, stu.id);
    const per = {};
    for (const q of mcqOnly(await sessionQuestions(env, a.session_id, a.test_id))) {
      if (!q.topic || q.cancelled) continue;
      const t = (per[q.topic] ||= { e: 0, p: 0 });
      t.p += q.points; if (isRight(q, chosen[q.id] ?? null)) t.e += q.points;
    }
    for (const [name, t] of Object.entries(per)) {
      const x = (topics[name] ||= { name, earned: 0, possible: 0, series: [] });
      x.earned += t.e; x.possible += t.p;
      x.series.push({ date: a.scheduled_start, pct: t.p ? Math.round((t.e / t.p) * 100) : null });
    }
  }
  const list = Object.values(topics).map((t) => ({ ...t, pct: t.possible ? Math.round((t.earned / t.possible) * 100) : null })).sort((a, b) => (a.pct ?? 0) - (b.pct ?? 0));
  return json({ exams, topics: list, wrong_count: wrongCount });
}

// ---------- teachers: indicators that something may be wrong (never proof) ----------
const ms = (s) => (s ? Date.parse(String(s).replace(' ', 'T') + 'Z') : NaN);

export async function suspicion(req, env, params) {
  const g = await needSession(req, env, params.sessionId, 'view'); if (g.resp) return g.resp;
  await ensureColumns(env);
  const ses = await env.DB.prepare('SELECT id, test_id, duration_minutes FROM test_sessions WHERE id = ?1').bind(g.ses.id).first();
  const qs = mcqOnly(await sessionQuestions(env, ses.id, ses.test_id)).filter((q) => !q.cancelled);
  const { results: rows } = await env.DB.prepare(
    `SELECT st.id, st.surname, st.first_name, r.started_at, r.submitted_at, r.mcq_score, r.mcq_max, r.violations, r.tab_switches
     FROM results r JOIN students st ON st.id = r.student_id WHERE r.session_id = ?1 AND r.submitted_at IS NOT NULL`,
  ).bind(ses.id).all();
  const { results: rs } = await env.DB.prepare('SELECT student_id, question_id, selected_index FROM responses WHERE session_id = ?1').bind(ses.id).all();
  const ans = {};
  for (const r of rs) (ans[r.student_id] ||= {})[r.question_id] = r.selected_index;
  const name = Object.fromEntries(rows.map((r) => [r.id, `${r.surname} ${r.first_name}`]));

  // 1) finished very early with a good score
  const fast = [];
  for (const r of rows) {
    const spent = (ms(r.submitted_at) - ms(r.started_at)) / 60000;
    const pct = r.mcq_max ? r.mcq_score / r.mcq_max : 0;
    if (Number.isFinite(spent) && spent >= 0 && spent < ses.duration_minutes * 0.25 && pct >= 0.6 && qs.length >= 10) {
      fast.push({ id: r.id, name: name[r.id], minutes: Math.round(spent), of: ses.duration_minutes, pct: Math.round(pct * 100) });
    }
  }

  // 2) pairs who gave the *same wrong answer* on most of the questions both got wrong
  const wrongOf = (sid) => { const o = {}; for (const q of qs) { const v = ans[sid]?.[q.id]; if (v != null && !isRight(q, v)) o[q.id] = v; } return o; };
  const wrong = Object.fromEntries(rows.map((r) => [r.id, wrongOf(r.id)]));
  const pairs = [];
  for (let i = 0; i < rows.length; i++) for (let j = i + 1; j < rows.length; j++) {
    const a = wrong[rows[i].id], b = wrong[rows[j].id];
    let both = 0, same = 0;
    for (const qid of Object.keys(a)) if (qid in b) { both++; if (a[qid] === b[qid]) same++; }
    if (both >= 6 && same >= 5 && same / both >= 0.8) pairs.push({ a: rows[i].id, b: rows[j].id, a_name: name[rows[i].id], b_name: name[rows[j].id], both_wrong: both, same_wrong: same });
  }
  pairs.sort((x, y) => y.same_wrong - x.same_wrong);

  // 3) many incidents during the exam
  const incidents = rows.filter((r) => (r.violations || 0) >= 2).map((r) => ({ id: r.id, name: name[r.id], violations: r.violations, tab_switches: r.tab_switches || 0, pct: r.mcq_max ? Math.round((r.mcq_score / r.mcq_max) * 100) : null }))
    .sort((x, y) => y.violations - x.violations);
  return json({ students: rows.length, questions: qs.length, fast, pairs: pairs.slice(0, 20), incidents });
}

// ---------- teachers: mark one writing question down the whole class ----------
export async function writingGrid(req, env, params) {
  const g = await needSession(req, env, params.sessionId, 'edit'); if (g.resp) return g.resp;
  await ensureColumns(env);
  const { question_id, scores } = await req.json();
  const wq = (await sessionQuestions(env, g.ses.id, g.ses.test_id)).filter((q) => q.kind === 'writing');
  const q = wq.find((x) => x.id === Number(question_id));
  if (!q) return err('Not a writing question of this exam.', 400);
  const max = wq.reduce((t, x) => t + x.points, 0);
  const stmts = [], students = [];
  for (const [sid, val] of Object.entries(scores || {})) {
    students.push(sid);
    if (val === '' || val === null) { stmts.push(env.DB.prepare('DELETE FROM writing_marks WHERE session_id = ?1 AND student_id = ?2 AND question_id = ?3').bind(g.ses.id, sid, q.id)); continue; }
    const v = Number(val);
    if (!(v >= 0 && v <= q.points)) return err(`ពិន្ទុត្រូវនៅចន្លោះ 0 ដល់ ${q.points}។`, 400);
    stmts.push(env.DB.prepare('INSERT INTO writing_marks (session_id, student_id, question_id, score) VALUES (?1, ?2, ?3, ?4) ON CONFLICT(session_id, student_id, question_id) DO UPDATE SET score = ?4').bind(g.ses.id, sid, q.id, v));
  }
  if (stmts.length) await env.DB.batch(stmts);
  const totalSql = '(SELECT SUM(score) FROM writing_marks WHERE session_id = ?1 AND student_id = ?2)';
  const totals = students.map((sid) => env.DB.prepare(
    `INSERT INTO results (session_id, student_id, mcq_score, mcq_max, writing_score, writing_max) VALUES (?1, ?2, 0, 0, ${totalSql}, ?3)
     ON CONFLICT(session_id, student_id) DO UPDATE SET writing_score = ${totalSql}, writing_max = ?3`,
  ).bind(g.ses.id, sid, max));
  for (let i = 0; i < totals.length; i += 40) await env.DB.batch(totals.slice(i, i + 40));
  await audit(env, g.t, 'session.writing_grid', `session ${g.ses.id}, question ${q.id}: ${students.length} students`);
  return json({ ok: true, count: students.length });
}

// ---------- owner: unused pictures + backup self-check ----------
const UNUSED = `FROM images i WHERE NOT EXISTS (SELECT 1 FROM test_questions q WHERE q.image_key = i.key)
  AND NOT EXISTS (SELECT 1 FROM session_questions s WHERE s.image_key = i.key)
  AND NOT EXISTS (SELECT 1 FROM settings x WHERE instr(x.value, i.key) > 0)
  AND (i.created_at IS NULL OR i.created_at < datetime('now', '-3 days'))`;
export async function unusedImages(req, env) {
  const g = await needAdmin(req, env); if (g.resp) return g.resp;
  await ensureColumns(env);
  const r = await env.DB.prepare(`SELECT COUNT(*) AS n, COALESCE(SUM(length(i.data_base64)), 0) AS bytes ${UNUSED}`).first();
  const all = await env.DB.prepare('SELECT COUNT(*) AS n, COALESCE(SUM(length(data_base64)), 0) AS bytes FROM images').first();
  return json({ unused: r.n, unused_kb: Math.round(r.bytes / 1024), total: all.n, total_kb: Math.round(all.bytes / 1024) });
}
export async function cleanupImages(req, env) {
  const g = await needAdmin(req, env); if (g.resp) return g.resp;
  await ensureColumns(env);
  const r = await env.DB.prepare(`DELETE FROM images WHERE key IN (SELECT i.key ${UNUSED})`).run();
  await audit(env, g.t, 'images.cleanup', `${r.meta.changes ?? 0} deleted`);
  return json({ ok: true, deleted: r.meta.changes ?? 0 });
}
export async function backupSelfCheck(req, env) {
  const g = await needAdmin(req, env); if (g.resp) return g.resp;
  return json(await selfCheck(env));
}

// Sample numbers for a question with variables, so the teacher sees what students will get.
export async function variantPreview(req, env) {
  const { authTeacher } = await import('../lib/access.js');
  const t = await authTeacher(req, env);
  if (!t) return err('Not logged in.', 401);
  const b = await req.json();
  try {
    const samples = [];
    for (let i = 0; i < Math.min(Number(b.n) || 3, 6); i++) {
      const o = instantiate({ id: 0, params: b.params, stem_text: b.stem_text || '', options_json: JSON.stringify(b.options || []), solution_text: b.solution_text || null }, 0, `preview${i}`);
      samples.push({ stem_text: o.stem_text, options: JSON.parse(o.options_json), solution_text: o.solution_text });
    }
    return json({ samples });
  } catch (e) { return err(e.message, 400); }
}
