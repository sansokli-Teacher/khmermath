// "Is this exam ready to open?" — the same checks run before scheduling a session
// (from the form values) and on an existing session. Each check is ok | warn | error;
// errors block scheduling, warnings ask the teacher to confirm.
import { sessionQuestions } from './frozen.js';

const DIAGRAM_WORDS = /រូប(?:ភាព|ខាង|នេះ)|តារាង|ក្រាហ្វ|ដ្យាក្រាម|figure|diagram|graph|chart|table|ដូចក្នុងរូប/i;
const nums = (list) => list.map((n) => n).join(', ');

export async function checkReadiness(env, { testId, classId, startIso, endIso, durationMin, pin, sessionId = null }) {
  const checks = [];
  const add = (id, level, title, detail = '') => checks.push({ id, level, title, detail });

  // ---- questions
  const qs = sessionId
    ? await sessionQuestions(env, sessionId, testId)
    : (await env.DB.prepare(
      'SELECT id, order_no, kind, stem_text, image_key, options_json, correct_index, alt_correct_index, cancelled, points, solution_text FROM test_questions WHERE test_id = ?1 ORDER BY order_no, id',
    ).bind(testId).all()).results;
  const mcq = qs.filter((q) => q.kind !== 'writing');
  const writing = qs.filter((q) => q.kind === 'writing');
  const no = new Map(qs.map((q, i) => [q.id, i + 1]));

  if (!qs.length) add('questions', 'error', 'តេស្តនេះមិនមានសំណួរទេ', 'សូមបន្ថែមសំណួរជាមុនសិន។');
  else add('questions', 'ok', `មានសំណួរ ${qs.length} (ពហុជ្រើសរើស ${mcq.length} · សរសេរ ${writing.length})`);

  // invalid answer choices
  const badChoices = [], dupChoices = [];
  for (const q of mcq) {
    let opts = [];
    try { opts = JSON.parse(q.options_json); } catch {}
    const blank = opts.some((o) => !String(o).trim());
    const outOfRange = !Number.isInteger(q.correct_index) || q.correct_index < 0 || q.correct_index >= opts.length;
    const altBad = q.alt_correct_index != null && (q.alt_correct_index < 0 || q.alt_correct_index >= opts.length || q.alt_correct_index === q.correct_index);
    if (opts.length < 2 || blank || outOfRange || altBad) badChoices.push(no.get(q.id));
    else if (new Set(opts.map((o) => String(o).trim())).size < opts.length) dupChoices.push(no.get(q.id));
  }
  if (badChoices.length) add('choices', 'error', 'ជម្រើសចម្លើយមិនត្រឹមត្រូវ', `សំណួរទី ${nums(badChoices)} — ជម្រើសទទេ តិចជាង ២ ឬចម្លើយត្រឹមត្រូវមិននៅក្នុងបញ្ជី។`);
  else if (mcq.length) add('choices', 'ok', 'ជម្រើសចម្លើយ និងចម្លើយត្រឹមត្រូវ គ្រប់សំណួរ');
  if (dupChoices.length) add('dup-choices', 'warn', 'មានជម្រើសចម្លើយស្ទួន', `សំណួរទី ${nums(dupChoices)}`);

  // pictures
  const withImg = qs.filter((q) => q.image_key);
  let missingImg = [];
  if (withImg.length) {
    const keys = [...new Set(withImg.map((q) => q.image_key))];
    const { results } = await env.DB.prepare(`SELECT key FROM images WHERE key IN (${keys.map(() => '?').join(',')})`).bind(...keys).all();
    const have = new Set(results.map((r) => r.key));
    missingImg = withImg.filter((q) => !have.has(q.image_key)).map((q) => no.get(q.id));
  }
  if (missingImg.length) add('images', 'error', 'រូបភាពបាត់ពីប្រព័ន្ធ', `សំណួរទី ${nums(missingImg)} — សូមបញ្ចូលរូបភាពឡើងវិញ។`);
  else if (withImg.length) add('images', 'ok', `រូបភាព ${withImg.length} សំណួរ មានគ្រប់`);
  const maybeDiagram = qs.filter((q) => !q.image_key && !q.cancelled && DIAGRAM_WORDS.test(q.stem_text) && !/\\begin\{|<table|\|---/.test(q.stem_text)).map((q) => no.get(q.id));
  if (maybeDiagram.length) add('diagram', 'warn', 'ប្រហែលជាខ្វះរូប/តារាង', `សំណួរទី ${nums(maybeDiagram)} និយាយពីរូប ឬតារាង តែមិនមានរូបភាពភ្ជាប់។`);

  // marks
  const sum = (a) => a.filter((q) => !q.cancelled).reduce((t, q) => t + Number(q.points || 0), 0);
  const badPts = qs.filter((q) => !(Number(q.points) > 0)).map((q) => no.get(q.id));
  if (badPts.length) add('marks', 'error', 'ពិន្ទុសំណួរមិនត្រឹមត្រូវ', `សំណួរទី ${nums(badPts)} ត្រូវមានពិន្ទុលើសពី ០។`);
  else if (qs.length) add('marks', 'ok', `ពិន្ទុសរុប ${sum(qs)} (ផ្នែក ក ${sum(mcq)} · ផ្នែក ខ ${sum(writing)})`);
  const cancelled = qs.filter((q) => q.cancelled).length;
  if (cancelled) add('cancelled', 'warn', `មានសំណួរបោះបង់ ${cancelled}`, 'សិស្សទាំងអស់នឹងទទួលពិន្ទុសំណួរទាំងនោះ។');
  const noGuide = writing.filter((q) => !q.solution_text).map((q) => no.get(q.id));
  if (noGuide.length) add('guide', 'warn', 'សំណួរសរសេរមិនទាន់មានចម្លើយគំរូ', `សំណួរទី ${nums(noGuide)}`);
  if (mcq.length) {
    const withSol = mcq.filter((q) => q.solution_text && String(q.solution_text).trim()).length;
    add('explain', withSol ? 'ok' : 'warn', `ការពន្យល់ចម្លើយ ${withSol}/${mcq.length}`, withSol ? '' : 'សិស្សនឹងមិនឃើញការពន្យល់ក្រោយប្រកាសលទ្ធផលទេ។');
  }

  // ---- roster
  const cls = classId ? await env.DB.prepare('SELECT id, name, require_dob FROM classes WHERE id = ?1').bind(classId).first() : null;
  if (!cls) add('roster', 'error', 'រកមិនឃើញថ្នាក់');
  else {
    const r = await env.DB.prepare("SELECT COUNT(*) AS n, SUM(CASE WHEN dob IS NULL OR TRIM(dob) = '' THEN 1 ELSE 0 END) AS no_dob FROM students WHERE class_id = ?1").bind(classId).first();
    if (!r.n) add('roster', 'error', `ថ្នាក់ ${cls.name} មិនមានសិស្សទេ`, 'សូមបន្ថែមបញ្ជីសិស្សជាមុនសិន។');
    else add('roster', 'ok', `ថ្នាក់ ${cls.name} មានសិស្ស ${r.n} នាក់`);
    if (cls.require_dob && r.no_dob) add('dob', 'warn', `សិស្ស ${r.no_dob} នាក់មិនមានថ្ងៃកំណើត`, 'ថ្នាក់នេះតម្រូវឱ្យបញ្ចូលថ្ងៃកំណើតពេលចូល — ពួកគេនឹងចូលមិនបាន ឬចូលដោយគ្មានការផ្ទៀងផ្ទាត់។');
  }

  // ---- timing
  const start = Date.parse(startIso), end = Date.parse(endIso);
  const dur = Number(durationMin) || (end - start) / 60000;
  if (!Number.isFinite(start) || !Number.isFinite(end) || end <= start) add('timing', 'error', 'ម៉ោងចាប់ផ្តើម/បញ្ចប់មិនត្រឹមត្រូវ');
  else {
    const now = Date.now();
    if (end <= now) add('timing', 'error', 'ម៉ោងបញ្ចប់បានកន្លងផុតហើយ', 'សិស្សនឹងមិនអាចចូលប្រឡងបានទេ។');
    else if (start < now - 5 * 60000) add('timing', 'warn', 'ម៉ោងចាប់ផ្តើមបានកន្លងផុតហើយ', 'ការប្រឡងនឹងបើកភ្លាមៗ។');
    else if (dur < 10 || dur > 300) add('timing', 'warn', `រយៈពេល ${Math.round(dur)} នាទី មិនធម្មតា`);
    else add('timing', 'ok', `រយៈពេល ${Math.round(dur)} នាទី`);
    if (classId) {
      const { results } = await env.DB.prepare(
        `SELECT s.id, s.test_id, s.scheduled_start, s.scheduled_end, s.duration_minutes FROM test_sessions s WHERE s.class_id = ?1 AND s.status <> 'closed' AND (?2 IS NULL OR s.id <> ?2)`,
      ).bind(classId, sessionId).all();
      const clash = results.filter((s) => {
        const a = Date.parse(s.scheduled_start), b = s.scheduled_end ? Date.parse(s.scheduled_end) : a + s.duration_minutes * 60000;
        return a < end && b > start;
      });
      if (clash.length) add('clash', 'warn', 'ម៉ោងជាន់ការប្រឡងមួយទៀតរបស់ថ្នាក់នេះ');
      if (results.some((s) => s.test_id === Number(testId) && Date.parse(s.scheduled_start) > Date.now() - 86400000)) add('dup', 'warn', 'តេស្តនេះត្រូវបានកំណត់ពេលឱ្យថ្នាក់នេះរួចហើយ');
    }
  }

  // ---- PIN
  const p = String(pin ?? '').trim();
  if (!/^[0-9A-Za-z]{3,12}$/.test(p)) add('pin', 'error', 'PIN មិនត្រឹមត្រូវ', 'ត្រូវមានអក្សរ ឬលេខ ៣–១២ តួ។');
  else add('pin', 'ok', 'មាន PIN សម្រាប់សិស្ស');

  const errors = checks.filter((c) => c.level === 'error').length;
  const warnings = checks.filter((c) => c.level === 'warn').length;
  return { checks, errors, warnings, ready: errors === 0, totals: { mcq_points: sum(mcq), writing_points: sum(writing), mcq_count: mcq.length, writing_count: writing.length } };
}
