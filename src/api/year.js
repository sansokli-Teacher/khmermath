// Yearly gradebook: five assessments per class (pre-test, two monthly tests, the
// semester exam and the final). Pre-test and monthly tests are read from the exam
// sessions they are linked to; the semester exam and final are typed in by hand.
import { json, err } from '../lib/http.js';
import { finalizeIfClosed, ensureColumns } from './sessions.js';
import { needClass, classAccess } from '../lib/access.js';

let ready = false;
async function ensureYear(env) {
  await ensureColumns(env);
  if (ready) return;
  await env.DB.batch([
    env.DB.prepare(`CREATE TABLE IF NOT EXISTS assessments (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      class_id INTEGER NOT NULL,
      key TEXT NOT NULL,            -- pre | m1 | m2 | sem1 | final
      title TEXT NOT NULL,
      month_label TEXT NOT NULL DEFAULT '',
      kind TEXT NOT NULL,           -- online | manual
      session_id INTEGER,
      max_score REAL NOT NULL DEFAULT 100,
      in_monthly INTEGER NOT NULL DEFAULT 0,
      published INTEGER NOT NULL DEFAULT 0,
      order_no INTEGER NOT NULL,
      UNIQUE(class_id, key)
    )`),
    env.DB.prepare(`CREATE TABLE IF NOT EXISTS manual_scores (
      assessment_id INTEGER NOT NULL,
      student_id TEXT NOT NULL,
      score REAL,
      PRIMARY KEY (assessment_id, student_id)
    )`),
  ]);
  ready = true;
}

const DEFAULTS = [
  ['pre', 'បុរេតេស្ត', 'តុលា', 'online', 0],
  ['m1', 'ប្រឡងប្រចាំខែ', 'វិច្ឆិកា', 'online', 1],
  ['m2', 'ប្រឡងប្រចាំខែ', 'ធ្នូ', 'online', 1],
  ['sem1', 'ប្រឡងឆមាសទី១', 'មករា', 'manual', 0],
  ['final', 'ប្រឡងបញ្ចប់ឆ្នាំ', 'កុម្ភៈ', 'manual', 0],
];
const DEFAULT_CONFIG = { label: '២០២៦–២០២៧', monthly_weight: 50, exam_weight: 50 };

// Weights and year label are per class owner; the original shared setting is the fallback.
async function getConfig(env, ownerId) {
  const row = (ownerId != null && await env.DB.prepare('SELECT value FROM settings WHERE key = ?1').bind(`year_config_${ownerId}`).first())
    || await env.DB.prepare("SELECT value FROM settings WHERE key = 'year_config'").first();
  try { return { ...DEFAULT_CONFIG, ...(row ? JSON.parse(row.value) : {}) }; } catch { return { ...DEFAULT_CONFIG }; }
}

async function loadAssessments(env, classId) {
  await ensureYear(env);
  let { results } = await env.DB.prepare('SELECT * FROM assessments WHERE class_id = ?1 ORDER BY order_no').bind(classId).all();
  if (results.length === 0) {
    await env.DB.batch(DEFAULTS.map(([key, title, month, kind, inMonthly], i) => env.DB.prepare(
      'INSERT OR IGNORE INTO assessments (class_id, key, title, month_label, kind, in_monthly, order_no) VALUES (?1,?2,?3,?4,?5,?6,?7)',
    ).bind(classId, key, title, month, kind, inMonthly, i + 1)));
    ({ results } = await env.DB.prepare('SELECT * FROM assessments WHERE class_id = ?1 ORDER BY order_no').bind(classId).all());
  }
  return results;
}

const round1 = (x) => (x == null ? null : Math.round(x * 10) / 10);

// Percent score (0–100) of one student in one assessment, plus raw display value.
function scoreOf(a, studentId, data) {
  if (a.kind === 'manual') {
    const v = data.manual[`${a.id}:${studentId}`];
    if (v == null) return null;
    return { pct: a.max_score > 0 ? (v / a.max_score) * 100 : null, raw: v, max: a.max_score };
  }
  const r = data.results[`${a.session_id}:${studentId}`];
  if (!r || !r.submitted_at) return null;
  const testMax = data.testMax[a.session_id] || 0;
  const hasW = r.writing_score != null && r.writing_max != null;
  const max = testMax + (hasW ? r.writing_max : 0);
  if (max <= 0) return null;
  const raw = r.mcq_score + (hasW ? r.writing_score : 0);
  return { pct: (raw / max) * 100, raw, max, published: !!r.published_at };
}

function compute(assessments, studentId, data, cfg, teacherView) {
  const scores = {};
  const visible = {};
  for (const a of assessments) {
    const sc = scoreOf(a, studentId, data);
    scores[a.key] = sc;
    visible[a.key] = teacherView || !!a.published || !!(sc && sc.published);
    if (!teacherView && !visible[a.key]) scores[a.key] = null;
  }
  const monthly = assessments.filter((a) => a.in_monthly);
  const present = monthly.filter((a) => scores[a.key] && scores[a.key].pct != null);
  const monthlyAvg = present.length ? present.reduce((t, a) => t + scores[a.key].pct, 0) / present.length : null;

  const exam = assessments.find((a) => a.key === 'sem1');
  const examPct = exam && scores.sem1 ? scores.sem1.pct : null;
  // A student must not see a semester score built from a month still hidden from them.
  const hiddenMonth = !teacherView && monthly.some((a) => !visible[a.key] && scoreOf(a, studentId, data));
  let semester1 = null;
  if (examPct != null && !hiddenMonth) {
    const mw = Number(cfg.monthly_weight) || 0;
    const ew = Number(cfg.exam_weight) || 0;
    semester1 = monthlyAvg == null || mw + ew === 0 ? examPct : (mw * monthlyAvg + ew * examPct) / (mw + ew);
  }
  const finalPct = scores.final ? scores.final.pct : null;
  const yearAvg = semester1 != null && finalPct != null ? (semester1 + finalPct) / 2 : null;
  return {
    scores: Object.fromEntries(Object.entries(scores).map(([k, v]) => [k, v && { pct: round1(v.pct), raw: v.raw, max: v.max }])),
    monthly_avg: round1(monthlyAvg), semester1: round1(semester1), final: round1(finalPct), year_avg: round1(yearAvg),
  };
}

async function loadData(env, assessments, studentIds) {
  const sessionIds = [...new Set(assessments.filter((a) => a.kind === 'online' && a.session_id).map((a) => a.session_id))];
  for (const id of sessionIds) await finalizeIfClosed(env, id);
  const data = { results: {}, manual: {}, testMax: {} };
  if (sessionIds.length) {
    const ph = sessionIds.map(() => '?').join(',');
    const { results } = await env.DB.prepare(
      `SELECT session_id, student_id, mcq_score, writing_score, writing_max, submitted_at, published_at FROM results WHERE session_id IN (${ph})`,
    ).bind(...sessionIds).all();
    for (const r of results) data.results[`${r.session_id}:${r.student_id}`] = r;
    const { results: maxes } = await env.DB.prepare(
      `SELECT ts.id AS session_id, COALESCE(SUM(q.points), 0) AS m FROM test_sessions ts
       LEFT JOIN test_questions q ON q.test_id = ts.test_id AND q.kind <> 'writing' WHERE ts.id IN (${ph}) GROUP BY ts.id`,
    ).bind(...sessionIds).all();
    for (const m of maxes) data.testMax[m.session_id] = m.m;
  }
  const manualIds = assessments.filter((a) => a.kind === 'manual').map((a) => a.id);
  if (manualIds.length) {
    const ph = manualIds.map(() => '?').join(',');
    const { results } = await env.DB.prepare(`SELECT assessment_id, student_id, score FROM manual_scores WHERE assessment_id IN (${ph})`).bind(...manualIds).all();
    for (const r of results) data.manual[`${r.assessment_id}:${r.student_id}`] = r.score;
  }
  return data;
}

// ---- teacher
export async function getYear(req, env, params) {
  const g = await needClass(req, env, params.classId, 'view'); if (g.resp) return g.resp;
  const classId = Number(params.classId);
  const cls = await env.DB.prepare('SELECT id, name, grade, owner_id FROM classes WHERE id = ?1').bind(classId).first();
  if (!cls) return err('Class not found.', 404);
  const cfg = await getConfig(env, cls.owner_id);
  const assessments = await loadAssessments(env, classId);
  const { results: students } = await env.DB.prepare(
    'SELECT id, surname, first_name, gender FROM students WHERE class_id = ?1 ORDER BY surname, first_name',
  ).bind(classId).all();
  const data = await loadData(env, assessments);
  const { results: sessions } = await env.DB.prepare(
    `SELECT ts.id, ts.scheduled_start, t.title FROM test_sessions ts JOIN tests t ON t.id = ts.test_id
     WHERE ts.class_id = ?1 ORDER BY ts.scheduled_start DESC`,
  ).bind(classId).all();
  return json({
    class: cls, config: cfg, sessions, my_role: g.acc,
    assessments: assessments.map((a) => ({ id: a.id, key: a.key, title: a.title, month_label: a.month_label, kind: a.kind, session_id: a.session_id, max_score: a.max_score, in_monthly: a.in_monthly, published: a.published })),
    students: students.map((s) => ({ ...s, ...compute(assessments, s.id, data, cfg, true) })),
  });
}

export async function updateAssessment(req, env, params) {
  await ensureYear(env);
  const b = await req.json();
  const a = await env.DB.prepare('SELECT * FROM assessments WHERE id = ?1').bind(params.id).first();
  if (!a) return err('Assessment not found.', 404);
  const g = await needClass(req, env, a.class_id, 'edit'); if (g.resp) return g.resp;
  const max = b.max_score == null ? a.max_score : Number(b.max_score);
  if (!(max > 0)) return err('max_score must be above 0.', 400);
  await env.DB.prepare(
    'UPDATE assessments SET title = ?1, month_label = ?2, session_id = ?3, max_score = ?4, in_monthly = ?5, published = ?6 WHERE id = ?7',
  ).bind(
    String(b.title ?? a.title).trim() || a.title, String(b.month_label ?? a.month_label).trim(),
    a.kind === 'online' ? (b.session_id ? Number(b.session_id) : null) : null,
    max, b.in_monthly ? 1 : 0, b.published ? 1 : 0, a.id,
  ).run();
  return json({ ok: true });
}

export async function saveScores(req, env, params) {
  await ensureYear(env);
  const a = await env.DB.prepare('SELECT * FROM assessments WHERE id = ?1').bind(params.id).first();
  if (a) { const g = await needClass(req, env, a.class_id, 'edit'); if (g.resp) return g.resp; }
  if (!a || a.kind !== 'manual') return err('This assessment does not take typed scores.', 400);
  const { scores } = await req.json();
  if (!Array.isArray(scores)) return err('scores array is required.', 400);
  const stmts = [];
  for (const s of scores) {
    if (!s.student_id) continue;
    if (s.score === null || s.score === '' || s.score === undefined) {
      stmts.push(env.DB.prepare('DELETE FROM manual_scores WHERE assessment_id = ?1 AND student_id = ?2').bind(a.id, s.student_id));
      continue;
    }
    const v = Number(s.score);
    if (!Number.isFinite(v) || v < 0 || v > a.max_score) return err(`Score for ${s.student_id} must be between 0 and ${a.max_score}.`, 400);
    stmts.push(env.DB.prepare(
      'INSERT INTO manual_scores (assessment_id, student_id, score) VALUES (?1, ?2, ?3) ON CONFLICT(assessment_id, student_id) DO UPDATE SET score = ?3',
    ).bind(a.id, s.student_id, v));
  }
  if (stmts.length) await env.DB.batch(stmts);
  return json({ ok: true, count: stmts.length });
}

export async function setConfig(req, env) {
  const b = await req.json();
  const g = await needClass(req, env, b.class_id, 'own'); if (g.resp) return g.resp;
  const cls = await env.DB.prepare('SELECT owner_id FROM classes WHERE id = ?1').bind(Number(b.class_id)).first();
  const cfg = {
    label: String(b.label ?? DEFAULT_CONFIG.label).trim() || DEFAULT_CONFIG.label,
    monthly_weight: Math.max(0, Number(b.monthly_weight) || 0),
    exam_weight: Math.max(0, Number(b.exam_weight) || 0),
  };
  if (cfg.monthly_weight + cfg.exam_weight <= 0) return err('Weights must add up to more than 0.', 400);
  await env.DB.prepare(
    'INSERT INTO settings (key, value) VALUES (?1, ?2) ON CONFLICT(key) DO UPDATE SET value = ?2',
  ).bind(`year_config_${cls.owner_id}`, JSON.stringify(cfg)).run();
  return json({ ok: true, config: cfg });
}

// ---- student: only scores the teacher has released
export async function studentYear(env, student) {
  const own = await env.DB.prepare('SELECT owner_id FROM classes WHERE id = ?1').bind(student.classId).first();
  const cfg = await getConfig(env, own ? own.owner_id : null);
  const assessments = await loadAssessments(env, student.classId);
  const data = await loadData(env, assessments);
  const c = compute(assessments, student.id, data, cfg, false);
  return {
    label: cfg.label, monthly_weight: cfg.monthly_weight, exam_weight: cfg.exam_weight,
    assessments: assessments.map((a) => ({ key: a.key, title: a.title, month_label: a.month_label, in_monthly: a.in_monthly, ...(c.scores[a.key] || { pct: null }) })),
    monthly_avg: c.monthly_avg, semester1: c.semester1, final: c.final, year_avg: c.year_avg,
  };
}
