/* Scan the OMR answer sheets of a paper test: read a photo (or the live camera), show what was read,
   let the teacher fix doubtful answers, then save the score into the session like an online result. */
const { h, api } = Exam;
const params = new URLSearchParams(location.search);
const $ = (id) => document.getElementById(id);
const LET = ['ក', 'ខ', 'គ', 'ឃ', 'ង'];
const KH = '០១២៣៤៥៦៧៨៩';
const kh = (n) => String(n).replace(/\d/g, (d) => KH[d]);

let sessions = [], ses = null, test = null, mcq = [], optCount = 4, roster = new Map();
const scans = [];            // newest first
let seq = 0;

const isRight = (q, sel) => (q.cancelled ? true : sel == null ? false : sel === q.correct_index || (q.alt_correct_index != null && sel === q.alt_correct_index));

// ---------------- session picker ----------------
async function init() {
  let r;
  try { r = await api('/api/sessions'); } catch { Exam.notify('សូមចូលជាគ្រូសិន។').then(() => { location.href = 'teacher.html'; }); return; }
  sessions = r.sessions;
  const onlyTest = Number(params.get('test')) || null;
  const list = sessions.filter((s) => (!onlyTest || s.test_id === onlyTest));
  const pick = $('ses-pick');
  pick.innerHTML = '';
  if (onlyTest) await setupMake(onlyTest);
  if (!list.length) { $('ses-empty').hidden = !!onlyTest; if (onlyTest) $('ses-empty').hidden = true; pick.hidden = true; return; }
  pick.append(h('option', { value: '' }, '— ជ្រើសរើស —'));
  list.forEach((s) => pick.append(h('option', { value: s.id }, `${s.test_title} — ${s.class_name} (${Exam.fmtDateTime(s.scheduled_start)})`)));
  const want = params.get('session') || (list.length === 1 ? String(list[0].id) : '');
  if (want) { pick.value = want; loadSession(want); }
  pick.addEventListener('change', () => loadSession(pick.value));
}

let makeTest = null;
async function setupMake(testId) {
  makeTest = testId;
  let cl = [];
  try { cl = (await api('/api/classes')).classes.filter((c) => c.my_role !== 'view'); } catch {}
  if (!cl.length) return;
  const sel = $('mk-class'); sel.innerHTML = '';
  cl.forEach((c) => sel.append(h('option', { value: c.id }, `${c.name} (${c.student_count} នាក់)`)));
  $('mk').hidden = false;
  $('mk-btn').onclick = async () => {
    try {
      const start = new Date(Date.now() - 10 * 60000).toISOString();     // already over: students cannot start it online
      const r = await api('/api/sessions', { method: 'POST', body: { test_id: testId, class_id: Number(sel.value), scheduled_start: start, duration_minutes: 5 } });
      const lst = (await api('/api/sessions')).sessions;
      sessions = lst;
      const pick = $('ses-pick'); pick.hidden = false; $('ses-empty').hidden = true;
      pick.innerHTML = ''; pick.append(h('option', { value: '' }, '— ជ្រើសរើស —'));
      lst.filter((s) => s.test_id === testId).forEach((s) => pick.append(h('option', { value: s.id }, `${s.test_title} — ${s.class_name} (${Exam.fmtDateTime(s.scheduled_start)})`)));
      pick.value = String(r.id); loadSession(r.id);
    } catch (e) { Exam.notify(e.message); }
  };
}

async function loadSession(id) {
  scans.length = 0; $('list').innerHTML = ''; $('summary').hidden = true;
  if (!id) { $('capture').hidden = true; $('ses-info').textContent = ''; return; }
  try {
    ses = await api(`/api/sessions/${id}`);
    test = await api(`/api/tests/${ses.test_id}`);
  } catch (e) { Exam.notify(e.message); return; }
  mcq = test.questions.filter((q) => q.kind !== 'writing').map(Exam.withSample);
  optCount = Math.min(5, Math.max(4, ...mcq.map((q) => q.options.length)));
  roster = new Map(ses.roster.map((s) => [String(s.id), s]));
  const done = ses.roster.filter((s) => s.submitted_at).length;
  $('ses-info').innerHTML = '';
  $('ses-info').append(`${ses.test_title} · ថ្នាក់ ${ses.class_name} · សំណួរពហុជ្រើសរើស ${mcq.length} · សិស្ស ${ses.roster.length} នាក់ · មានលទ្ធផលរួច ${done} នាក់`);
  if (!mcq.length) { $('ses-info').append(h('div', { class: 'scan-warn' }, 'វិញ្ញាសានេះគ្មានសំណួរពហុជ្រើសរើសសម្រាប់ស្កេនទេ។')); $('capture').hidden = true; return; }
  if (mcq.length > OMR.MAX_Q) $('ses-info').append(h('div', { class: 'scan-warn' }, `សន្លឹក OMR ទ្រទ្រង់បានត្រឹម ${OMR.MAX_Q} សំណួរ។`));
  $('capture').hidden = false;
  updateSummary();
}

// ---------------- reading ----------------
function processImage(src, label) {
  const item = { id: ++seq, label, status: 'reading' };
  scans.unshift(item);
  try {
    const res = OMR.scan(src, { nQ: Math.min(mcq.length, OMR.MAX_Q), optCount });
    item.res = res;
    if (!res.ok) {
      item.status = 'bad';
      item.error = res.reason === 'markers' ? 'រកមិនឃើញការ៉េខ្មៅទាំង ៤ ជ្រុងទេ — សូមថតម្តងទៀត ឱ្យឃើញជ្រុងទាំងបួនពេញលេញ និងមិនព្រិល។'
        : 'អានកូដវិញ្ញាសាមិនបាន — សូមថតម្តងទៀតឱ្យច្បាស់ជាងមុន។';
    } else if (res.testId !== ses.test_id) {
      item.status = 'bad';
      item.error = `សន្លឹកនេះជារបស់វិញ្ញាសាលេខ #${res.testId} មិនមែនវិញ្ញាសា #${ses.test_id} របស់សម័យនេះទេ។`;
    } else {
      const order = OMR.mcqOrder(mcq, res.grouped);
      item.order = order;
      item.answers = res.answers.map((a) => a.sel);
      item.flags = res.answers.map((a) => a.flag);
      item.student = roster.has(res.studentId) ? res.studentId : '';
      item.status = 'check';
      item.thumb = drawThumb(res);
    }
  } catch (e) { item.status = 'bad'; item.error = 'មានបញ្ហាក្នុងការអានរូបភាព៖ ' + e.message; }
  renderList();
  if (item.status === 'check' && $('auto-save').checked && isClean(item)) save(item, true);
  return item;
}

const problemIdx = (it) => it.flags.map((f, i) => (f === 'multi' || f === 'unsure' ? i : -1)).filter((i) => i >= 0);
const isClean = (it) => it.student && problemIdx(it).length === 0;

function drawThumb(res) {
  const src = res.canvas, k = Math.min(1, 640 / src.width);
  const cv = document.createElement('canvas'); cv.width = Math.round(src.width * k); cv.height = Math.round(src.height * k);
  const g = cv.getContext('2d'); g.drawImage(src, 0, 0, cv.width, cv.height);
  const rad = res.pxPerMm * k * 2.9;
  const ring = (x, y, col, lw = 2) => { const [px, py] = res.map(x, y); g.beginPath(); g.arc(px * k, py * k, rad, 0, 7); g.strokeStyle = col; g.lineWidth = lw; g.stroke(); };
  res.layout.q.forEach((r, i) => {
    const a = res.answers[i];
    if (a.sel != null) ring(...r.bubbles[a.sel], a.flag === 'unsure' ? '#e08a00' : '#0fbf6b', 3);
    else if (a.flag === 'multi') r.bubbles.forEach((b, j) => { if (a.s[j] >= 0.3) ring(...b, '#ff3b3b', 3); });
  });
  res.idCols.forEach((c, i) => { if (c.sel != null) ring(...res.layout.id[i][c.sel], '#2260d6', 3); });
  return cv;
}

// ---------------- list ----------------
function scoreOf(it) {
  let s = 0, m = 0;
  it.order.forEach((q, i) => { m += q.points; if (isRight(q, it.answers[i])) s += q.points; });
  return { s, m };
}

function renderList() {
  const list = $('list'); list.innerHTML = '';
  scans.forEach((it) => list.append(card(it)));
  updateSummary();
}

function card(it) {
  const cls = it.status === 'saved' ? 'saved' : it.status === 'bad' ? 'bad' : 'check';
  const box = h('div', { class: `sc-item ${cls}` });
  if (it.status === 'bad') {
    box.append(h('div', { class: 'sc-body', style: 'grid-template-columns:1fr;' }, [
      h('div', { class: 'sc-status bad' }, `✗ ${it.label}`), h('div', {}, it.error),
      h('div', { class: 'sc-row' }, [h('button', { class: 'secondary btn-sm', onclick: () => { scans.splice(scans.indexOf(it), 1); renderList(); } }, 'លុប')]),
    ]));
    return box;
  }
  const { s, m } = scoreOf(it);
  const stuSel = h('select', { onchange: (e) => { it.student = e.target.value; if (it.status === 'saved') it.status = 'check'; renderList(); } }, [
    h('option', { value: '' }, it.res.studentId.includes('?') ? `— ជ្រើសសិស្ស (អានបាន ${it.res.studentId}) —` : `— មិនមានសិស្សលេខ ${it.res.studentId} ក្នុងថ្នាក់នេះ —`),
    ...ses.roster.map((r) => h('option', { value: r.id }, `${r.surname} ${r.first_name} (${r.id})${r.submitted_at ? ' ✓' : ''}`)),
  ]);
  stuSel.value = it.student || '';
  const probs = problemIdx(it), blanks = it.flags.filter((f) => f === 'blank').length;
  const already = it.student && roster.get(it.student) && roster.get(it.student).submitted_at && it.status !== 'saved';
  const thumb = it.thumb;
  thumb.className = 'sc-thumb';
  thumb.onclick = () => { const ov = h('div', { class: 'zoom-ov', onclick: () => ov.remove() }); const c = document.createElement('canvas'); c.width = it.res.canvas.width; c.height = it.res.canvas.height; c.getContext('2d').drawImage(drawThumbFull(it.res), 0, 0); ov.append(c); document.body.append(ov); };
  const status = it.status === 'saved' ? h('div', { class: 'sc-status ok' }, '✓ បានរក្សាទុករួច')
    : !it.student ? h('div', { class: 'sc-status warn' }, '⚠ ត្រូវជ្រើសសិស្ស')
      : probs.length ? h('div', { class: 'sc-status warn' }, `⚠ ត្រូវពិនិត្យ ${probs.length} សំណួរ`) : h('div', { class: 'sc-status warn' }, 'រួចរាល់ — មិនទាន់រក្សាទុក');
  box.append(h('div', { class: 'sc-body' }, [
    thumb,
    h('div', { class: 'sc-main' }, [
      status,
      stuSel,
      h('div', { class: 'sc-score' }, [`${kh(s)} / ${kh(m)}`, h('small', {}, ` ពិន្ទុពហុជ្រើសរើស · ទទេ ${kh(blanks)}`)]),
      probs.length ? h('div', { class: 'sc-flags' }, `⚠ សំណួរគូសច្រើន/មិនច្បាស់៖ ${probs.map((i) => i + 1).join(', ')} — សូមកែខាងក្រោម`) : null,
      already ? h('div', { class: 'sc-flags' }, 'សិស្សនេះមានលទ្ធផលរួចហើយ — ការរក្សាទុកនឹងជំនួសលទ្ធផលចាស់។') : null,
      h('div', { class: 'sc-row' }, [
        it.status === 'saved' ? null : h('button', { onclick: () => save(it, false) }, '💾 រក្សាទុក'),
        it.status === 'saved' && (ses.writing_max_default || 0) > 0 ? h('button', { class: 'secondary btn-sm', onclick: () => writingMarks(it) }, '✎ ពិន្ទុសរសេរ') : null,
        it.status === 'saved' ? h('button', { class: 'secondary btn-sm', onclick: () => undo(it) }, '↩ ដកចេញ') : null,
        h('button', { class: 'secondary btn-sm', onclick: () => { scans.splice(scans.indexOf(it), 1); renderList(); } }, 'លុប'),
      ]),
    ]),
  ]));
  box.append(h('details', { class: 'sc-edit', open: probs.length > 0 }, [
    h('summary', {}, 'ពិនិត្យ / កែចម្លើយ'),
    h('div', { class: 'sc-grid' }, it.order.map((q, i) => h('div', { class: `sc-q${it.flags[i] === 'multi' || it.flags[i] === 'unsure' ? ' flag' : ''}` }, [
      h('b', {}, String(i + 1)),
      ...[...Array(Math.max(optCount, q.options.length)).keys()].map((k) => h('button', {
        class: `${it.answers[i] === k ? 'on' : ''}${q.correct_index === k ? ' right' : ''}`,
        title: q.correct_index === k ? 'ចម្លើយត្រឹមត្រូវ' : '',
        onclick: () => { it.answers[i] = it.answers[i] === k ? null : k; it.flags[i] = 'edited'; if (it.status === 'saved') it.status = 'check'; renderList(); },
      }, LET[k])),
    ]))),
  ]));
  return box;
}

function drawThumbFull(res) {            // larger version for the zoom view
  const src = res.canvas, cv = document.createElement('canvas'); cv.width = src.width; cv.height = src.height;
  const g = cv.getContext('2d'); g.drawImage(src, 0, 0);
  const rad = res.pxPerMm * 2.9;
  const ring = (x, y, col) => { const [px, py] = res.map(x, y); g.beginPath(); g.arc(px, py, rad, 0, 7); g.strokeStyle = col; g.lineWidth = 3; g.stroke(); };
  res.layout.q.forEach((r, i) => { const a = res.answers[i]; if (a.sel != null) ring(...r.bubbles[a.sel], '#0fbf6b'); else if (a.flag === 'multi') r.bubbles.forEach((b, j) => { if (a.s[j] >= 0.3) ring(...b, '#ff3b3b'); }); });
  res.idCols.forEach((c, i) => { if (c.sel != null) ring(...res.layout.id[i][c.sel], '#2260d6'); });
  return cv;
}

async function save(it, quiet) {
  if (!it.student) return Exam.notify('សូមជ្រើសរើសសិស្សសិន។');
  const answers = {};
  it.order.forEach((q, i) => { answers[q.id] = it.answers[i]; });
  try {
    const r = await api(`/api/sessions/${ses.id}/omr`, { method: 'POST', body: { student_id: it.student, answers } });
    it.status = 'saved'; it.saved = r;
    const rec = roster.get(it.student); if (rec) { rec.submitted_at = rec.submitted_at || 'now'; }
    const real = ses.roster.find((r) => String(r.id) === String(it.student)); if (real) real.submitted_at = real.submitted_at || 'now';
    if (!quiet && navigator.vibrate) navigator.vibrate(60);
  } catch (e) { if (!quiet) Exam.notify(e.message); else it.error = e.message; }
  renderList();
}

function updateMissing() {
  const el = $('missing');
  if (!ses) { el.hidden = true; return; }
  const doneIds = new Set(scans.filter((s) => s.status === 'saved').map((s) => s.student));
  const miss = ses.roster.filter((r) => !r.submitted_at && !doneIds.has(String(r.id)));
  const all = ses.roster.length;
  el.hidden = !scans.length;
  el.innerHTML = '';
  el.append(h('summary', {}, `មិនទាន់ស្កេន ${miss.length} / ${all} នាក់`),
    miss.length ? h('div', { class: 'scan-info', style: 'margin-top:8px;' }, miss.map((r) => `${r.surname} ${r.first_name} (${r.id})`).join(' · ')) : h('div', { class: 'sc-status ok', style: 'margin-top:8px;' }, '✓ សិស្សទាំងអស់មានលទ្ធផលរួចហើយ'));
}

async function writingMarks(it) {
  let data;
  try { data = await api(`/api/sessions/${ses.id}/writing-marks`); } catch (e) { return Exam.notify(e.message); }
  if (!data.questions.length) return Exam.notify('វិញ្ញាសានេះគ្មានសំណួរសរសេរទេ។');
  const mine = Object.fromEntries(data.marks.filter((m) => String(m.student_id) === String(it.student)).map((m) => [m.question_id, m.score]));
  const inputs = data.questions.map((q, i) => h('input', { type: 'number', min: 0, max: q.points, step: 0.5, value: mine[q.id] ?? '', style: 'width:80px;' }));
  const stu = roster.get(it.student);
  const ov = h('div', { class: 'zoom-ov', style: 'align-items:flex-start;' });
  const box = h('div', { class: 'scan-card', style: 'max-width:520px;width:100%;margin:20px auto;max-height:92vh;overflow:auto;' }, [
    h('div', { class: 'scan-lbl' }, `✎ ពិន្ទុសរសេរ — ${stu ? `${stu.surname} ${stu.first_name}` : it.student}`),
    ...data.questions.map((q, i) => h('div', { class: 'sc-row' }, [h('span', { style: 'flex:1;' }, `សំណួរទី ${i + 1} (អតិបរមា ${q.points})`), inputs[i]])),
    h('div', { class: 'sc-row', style: 'position:sticky;bottom:0;background:#fff;padding:8px 0;' }, [
      h('button', { onclick: async () => {
        const marks = {}; data.questions.forEach((q, i) => { marks[q.id] = inputs[i].value === '' ? '' : Number(inputs[i].value); });
        try { await api(`/api/sessions/${ses.id}/writing-marks`, { method: 'POST', body: { student_id: it.student, marks } }); ov.remove(); } catch (e) { Exam.notify(e.message); }
      } }, '💾 រក្សាទុកពិន្ទុ'),
      h('button', { class: 'secondary', onclick: () => ov.remove() }, 'បិទ'),
    ]),
  ]);
  ov.append(box); document.body.append(ov); inputs[0].focus();
}

async function undo(it) {
  if (!(await Exam.confirm('ដកលទ្ធផលស្កេនរបស់សិស្សនេះចេញពីប្រព័ន្ធ?'))) return;
  try { await api(`/api/sessions/${ses.id}/omr/${encodeURIComponent(it.student)}`, { method: 'DELETE' }); } catch (e) { return Exam.notify(e.message); }
  const rec = roster.get(it.student); if (rec) rec.submitted_at = null;
  const real = ses.roster.find((r) => String(r.id) === String(it.student)); if (real) real.submitted_at = null;
  it.status = 'check'; renderList();
}

function updateSummary() {
  updateMissing();
  const el = $('summary'); el.innerHTML = '';
  if (!scans.length) { el.hidden = true; return; }
  el.hidden = false;
  const saved = scans.filter((s) => s.status === 'saved').length, check = scans.filter((s) => s.status === 'check').length, bad = scans.filter((s) => s.status === 'bad').length;
  el.append(h('span', { class: 'chip' }, `ស្កេនសរុប ${scans.length}`), h('span', { class: 'chip ok' }, `✓ រក្សាទុក ${saved}`));
  if (check) el.append(h('span', { class: 'chip warn' }, `⚠ ត្រូវពិនិត្យ ${check}`), h('button', { class: 'btn-sm', onclick: () => scans.filter((s) => s.status === 'check' && s.student).forEach((s) => save(s, true)) }, '💾 រក្សាទុកទាំងអស់ដែលរួចរាល់'));
  if (bad) el.append(h('span', { class: 'chip warn' }, `✗ អានមិនបាន ${bad}`));
  if (saved) el.append(h('a', { class: 'btn secondary btn-sm', href: 'teacher.html' }, 'មើលលទ្ធផលក្នុងផ្ទាំងគ្រូ'));
}

// ---------------- files ----------------
$('file-in').addEventListener('change', async (e) => {
  for (const f of e.target.files) {
    const url = URL.createObjectURL(f);
    try {
      const img = new Image(); img.src = url; await img.decode();
      await new Promise((r) => setTimeout(r, 20));       // let the UI paint between big images
      processImage(img, f.name);
    } catch { scans.unshift({ id: ++seq, label: f.name, status: 'bad', error: 'បើករូបភាពមិនបាន។' }); renderList(); }
    URL.revokeObjectURL(url);
  }
  e.target.value = '';
});

// ---------------- live camera (auto-scan) ----------------
let stream = null, timer = null, last = null, cool = 0, recent = new Map();
async function openCam() {
  try { stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: { ideal: 'environment' }, width: { ideal: 1920 }, height: { ideal: 1080 } }, audio: false }); }
  catch { return Exam.notify('មិនអាចបើកកាមេរ៉ាបានទេ។ សូមអនុញ្ញាតកាមេរ៉ា ឬប្រើប៊ូតុង «ជ្រើសរូប» ជំនួស។'); }
  const v = $('cam-v'); v.srcObject = stream; $('cam').hidden = false; last = null;
  timer = setInterval(tick, 650);
}
function closeCam() { clearInterval(timer); if (stream) stream.getTracks().forEach((t) => t.stop()); stream = null; $('cam').hidden = true; }
function tick() {
  const v = $('cam-v');
  if (!v.videoWidth || Date.now() < cool) return;
  let res;
  try { res = OMR.scan(v, { nQ: Math.min(mcq.length, OMR.MAX_Q), optCount }); } catch { return; }
  const msg = $('cam-msg');
  if (!res.ok) { msg.className = 'cam-msg'; msg.textContent = res.reason === 'markers' ? 'ដាក់សន្លឹកឱ្យឃើញការ៉េខ្មៅទាំង ៤ ជ្រុង' : 'កំពុងអាន… ថតឱ្យច្បាស់ជាងមុន'; last = null; return; }
  if (res.testId !== ses.test_id) { msg.className = 'cam-msg'; msg.textContent = `សន្លឹកនេះជារបស់វិញ្ញាសា #${res.testId}`; return; }
  const sig = res.studentId + '|' + res.answers.map((a) => (a.sel == null ? '-' : a.sel)).join('');
  msg.className = 'cam-msg good'; msg.textContent = 'បានឃើញសន្លឹក — សូមកាន់ឱ្យនឹង…';
  if (last === sig && !res.studentId.includes('?')) {
    if (recent.has(res.studentId) && Date.now() - recent.get(res.studentId) < 8000) return;
    recent.set(res.studentId, Date.now()); cool = Date.now() + 1800; last = null;
    const cv = document.createElement('canvas'); cv.width = v.videoWidth; cv.height = v.videoHeight; cv.getContext('2d').drawImage(v, 0, 0);
    if (navigator.vibrate) navigator.vibrate(80);
    msg.textContent = `✓ បានស្កេនសិស្សលេខ ${res.studentId}`;
    processImage(cv, `ស្កេន ${res.studentId}`);
  } else last = sig;
}
$('cam-btn').addEventListener('click', openCam);
$('cam-close').addEventListener('click', closeCam);
$('cam-snap').addEventListener('click', () => {
  const v = $('cam-v'); if (!v.videoWidth) return;
  const cv = document.createElement('canvas'); cv.width = v.videoWidth; cv.height = v.videoHeight; cv.getContext('2d').drawImage(v, 0, 0);
  processImage(cv, 'ថតដោយដៃ'); cool = Date.now() + 1500;
});

init();
