const { h, api, showError, fmtDateTime, fmtTimeOnly, fmtClock } = Exam;

function mathEl(tag, attrs, text) {
  const el = h(tag, attrs);
  el.innerHTML = Exam.mathHtml(text);
  return el;
}

// The phone's own clock may be wrong; every countdown uses server time.
let clockSkew = 0;
const now = () => Date.now() + clockSkew;
const syncClock = (serverNow) => { if (serverNow) clockSkew = serverNow - Date.now(); };

const views = ['login', 'home', 'wait', 'test'].reduce((o, n) => ({ ...o, [n]: document.getElementById(`view-${n}`) }), {});
function showView(name) {
  for (const [n, el] of Object.entries(views)) el.hidden = n !== name;
  window.scrollTo(0, 0);
}

let currentStudent = null;
let testState = null;
let timerInterval = null;
let waitInterval = null;
let homeRefresh = null;

const computeGrade = (pct) => Exam.gradeOf(pct);

// ---------- Teacher preview (student.html?preview=TESTID&min=70) ----------
const PREVIEW = new URLSearchParams(location.search).get('preview');

async function bootPreview() {
  let test;
  try { test = await api(`/api/tests/${PREVIEW}`); } catch { return Exam.notify('សូមចូលជាគ្រូសិន ទើបអាចមើលតេស្តនេះបាន។').then(() => { location.href = 'teacher.html'; }); }
  const minutes = Number(new URLSearchParams(location.search).get('min')) || 70;
  currentStudent = { id: 'PREVIEW', name: 'សិស្សសាកល្បង' };
  testState = {
    session_id: null, test_title: test.title, end_at: Date.now() + minutes * 60000, current: 0,
    questions: test.questions.map((q) => ({ id: q.id, stem_text: q.stem_text, image_key: q.image_key, kind: q.kind, points: q.points, options: q.options, selected_index: null })),
  };
  showView('test');
  document.getElementById('preview-banner').hidden = false;
  document.getElementById('timer-title').textContent = test.title;
  document.getElementById('student-badge').textContent = 'របៀបមើលជាសិស្ស';
  renderNav(); renderQuestion(); startTimer();
}

// ---------- Sign in ----------
async function boot() {
  if (PREVIEW) return bootPreview();
  clearInterval(homeRefresh);
  try {
    const data = await api('/api/student/status');
    syncClock(data.server_now);
    currentStudent = { id: data.student_id, name: data.student_name };
    renderHome(data);
  } catch {
    showView('login');
    document.getElementById('login-id').focus();
  }
}

async function doLogin() {
  const id = document.getElementById('login-id').value.trim();
  const card = views.login.querySelector('.auth-card');
  if (!id) return showError(card, 'សូមបញ្ចូលអត្តលេខរបស់អ្នក។');
  try {
    await api('/api/student/login', { method: 'POST', body: { id, dob: document.getElementById('login-dob').value.trim() } });
    boot();
  } catch (e) {
    if (e.data && e.data.need_dob) {
      document.getElementById('dob-wrap').hidden = false;
      document.getElementById('login-dob').focus();
    }
    showError(card, e.message);
  }
}
document.getElementById('login-submit').addEventListener('click', doLogin);
document.getElementById('login-id').addEventListener('keydown', (e) => { if (e.key === 'Enter') doLogin(); });
// Typing only digits shows them as dd/mm/yyyy (10102010 -> 10/10/2010); Khmer digits are converted too.
function formatDob(raw) {
  const digits = String(raw).replace(/[០-៩]/g, (d) => '០១២៣៤៥៦៧៨៩'.indexOf(d)).replace(/\D/g, '').slice(0, 8);
  let out = digits.slice(0, 2);
  if (digits.length > 2) out += `/${digits.slice(2, 4)}`;
  if (digits.length > 4) out += `/${digits.slice(4)}`;
  return out;
}
document.getElementById('login-dob').addEventListener('input', (e) => { e.target.value = formatDob(e.target.value); });
document.getElementById('login-dob').setAttribute('maxlength', '10');
document.getElementById('login-dob').addEventListener('keydown', (e) => { if (e.key === 'Enter') doLogin(); });

async function logoutStudent() {
  try { await api('/api/student/logout', { method: 'POST' }); } catch {}
  currentStudent = null;
  testState = null;
  clearInterval(timerInterval);
  clearInterval(waitInterval);
  clearInterval(homeRefresh);
  document.getElementById('login-id').value = '';
  document.getElementById('login-dob').value = '';
  document.getElementById('dob-wrap').hidden = true;
  showView('login');
}
document.getElementById('home-logout').onclick = logoutStudent;

// ---------- Home ----------
function renderHome(data) {
  clearInterval(timerInterval);
  clearInterval(waitInterval);
  showView('home');
  document.getElementById('home-name').textContent = data.student_name;
  document.getElementById('home-sub').textContent = `អត្តលេខ ${data.student_id}${data.class_name ? ` · ថ្នាក់ ${data.class_name}` : ''}`;
  const body = document.getElementById('home-body');
  body.innerHTML = '';

  if (data.year) body.append(yearCard(data.year));

  // --- upcoming / open tests
  body.append(h('h2', { class: 'section-title' }, 'ការប្រឡងខាងមុខ'));
  if (data.upcoming.length === 0) {
    body.append(h('div', { class: 'empty-card' }, [
      h('div', { class: 'empty-icon' }, '📭'),
      h('div', { style: 'font-weight:600;' }, 'មិនទាន់មានការប្រឡងនៅឡើយទេ'),
      h('div', { class: 'muted' }, 'នៅពេលលោកគ្រូកំណត់ការប្រឡង វានឹងបង្ហាញនៅទីនេះ។'),
    ]));
  }
  for (const s of data.upcoming) body.append(examCard(s));

  // --- past results
  body.append(h('h2', { class: 'section-title', style: 'margin-top:28px;' }, 'លទ្ធផលពីមុន'));
  if (data.history.length === 0) {
    body.append(h('div', { class: 'empty-card' }, [
      h('div', { class: 'empty-icon' }, '📊'),
      h('div', { class: 'muted' }, 'មិនទាន់មានលទ្ធផលនៅឡើយទេ។'),
    ]));
  }
  for (const s of data.history) body.append(historyCard(s));

  // Refresh the list when a test is about to start / results get published.
  homeRefresh = setInterval(async () => {
    if (views.home.hidden || document.hidden || body.querySelector('input:focus')) return;
    try { const d = await api('/api/student/status'); syncClock(d.server_now); renderHome(d); } catch {}
  }, 30000);
}

function yearCard(y) {
  const pill = (v) => {
    const g = computeGrade(v);
    return g ? h('span', { class: 'chip', style: `background:${g.color}1a;color:${g.color};` }, `${g.grade} · ${g.label}`) : null;
  };
  const steps = y.assessments.map((a) => {
    const has = a.pct != null;
    return h('div', { class: `year-step${has ? '' : ' is-empty'}` }, [
      h('div', { class: 'year-month' }, `ខែ${a.month_label}`),
      h('div', { class: 'year-title' }, a.title),
      h('div', { class: 'year-score', style: has ? `color:${computeGrade(a.pct).color};` : '' }, has ? String(Math.round(a.pct * 10) / 10) : '—'),
      has ? pill(a.pct) : h('span', { class: 'muted', style: 'font-size:12px;' }, 'មិនទាន់មាន'),
    ]);
  });
  const tile = (label, v, alt) => {
    const g = computeGrade(v);
    return h('div', { class: `year-sum-tile${alt ? ' alt' : ''}${v == null ? ' is-empty' : ''}` }, [
      h('div', { class: 'lbl' }, label),
      h('div', { class: 'val' }, v == null ? '—' : String(Math.round(v * 10) / 10)),
      h('div', { class: 'gr' }, g ? `${g.grade} · ${g.label}` : 'មិនទាន់មាន'),
    ]);
  };
  return h('div', { class: 'year-card', style: 'margin-bottom:8px;' }, [
    h('div', { class: 'year-head' }, [
      h('h2', { style: 'margin:0;' }, `📈 ពិន្ទុឆ្នាំសិក្សា ${y.label}`),
      h('span', { class: 'muted' }, `ឆមាស = មធ្យមខែ ${y.monthly_weight}% + ប្រឡងឆមាស ${y.exam_weight}%`),
    ]),
    h('div', { class: 'year-steps' }, steps),
    h('div', { class: 'year-sum' }, [
      tile('មធ្យមភាគប្រចាំខែ', y.monthly_avg),
      tile('ពិន្ទុឆមាសទី១', y.semester1),
      tile('មធ្យមភាគប្រចាំឆ្នាំ', y.year_avg, true),
    ]),
    h('div', { class: 'row', style: 'margin-top:12px;' }, [h('a', { class: 'btn secondary btn-sm', href: 'reportcard.html', target: '_blank' }, '📄 ទាញយកសៀវភៅរបាយការណ៍ (PDF)')]),
  ]);
}

function examCard(s) {
  const isOpen = s.phase === 'open';
  const pinInput = h('input', {
    type: 'text', class: 'pin-input', placeholder: 'PIN', autocomplete: 'off', maxlength: '12',
    inputmode: 'text', 'aria-label': 'PIN ការប្រឡង',
  });
  const card = h('div', { class: `exam-card${isOpen ? ' is-open' : ''}` }, [
    h('div', { class: 'exam-card-head' }, [
      h('div', { class: 'exam-title' }, s.test_title),
      isOpen
        ? h('span', { class: 'chip chip-open' }, '● កំពុងបើក')
        : h('span', { class: 'chip chip-soon' }, 'នឹងមកដល់'),
    ]),
    h('div', { class: 'exam-meta' }, [
      h('span', {}, `📅 ${fmtDateTime(s.scheduled_start)}`),
      h('span', {}, `⏱ ${s.duration_minutes} នាទី`),
      h('span', {}, `🏁 បញ្ចប់ ${fmtTimeOnly(s.scheduled_end)}`),
    ]),
  ]);

  const go = async (withPin) => {
    showError(card, '');
    try {
      const res = await api('/api/student/start', { method: 'POST', body: { session_id: s.session_id, pin: withPin } });
      syncClock(res.server_now);
      if (res.waiting) return showWaiting(s, withPin, res.start_at);
      loadTest(s.session_id);
    } catch (e) { showError(card, e.message); }
  };

  if (s.started && isOpen) {
    card.append(h('button', { class: 'btn-block', onclick: () => go('') }, 'បន្តការប្រឡង →'));
  } else {
    card.append(h('div', { class: 'pin-row' }, [
      pinInput,
      h('button', { onclick: () => go(pinInput.value) }, isOpen ? 'ចូលប្រឡង' : 'បញ្ចូល PIN'),
    ]));
    pinInput.addEventListener('keydown', (e) => { if (e.key === 'Enter') go(pinInput.value); });
    card.append(h('div', { class: 'muted pin-hint' }, isOpen
      ? 'សូមសួរ PIN ពីលោកគ្រូ រួចបញ្ចូលដើម្បីចាប់ផ្តើម។'
      : 'អាចបញ្ចូល PIN ទុកជាមុន — ការប្រឡងនឹងបើកដោយខ្លួនឯងពេលដល់ម៉ោង។'));
  }
  return card;
}

function historyCard(s) {
  const head = h('div', { class: 'exam-card-head' }, [
    h('div', { class: 'exam-title' }, s.test_title),
    h('span', { class: 'muted', style: 'white-space:nowrap;' }, fmtDateTime(s.scheduled_start)),
  ]);
  if (s.state === 'published') {
    const total = s.mcq_score + (s.writing_score ?? 0);
    const max = s.mcq_max + (s.writing_max ?? 0);
    const pct = max > 0 ? Math.round((total / max) * 100) : 0;
    const g = computeGrade(pct);
    return h('div', { class: 'score-card' }, [
      head,
      h('div', { class: 'score-row' }, [
        h('div', { class: 'score-big' }, [h('span', {}, String(total)), h('span', { class: 'score-max' }, ` / ${max}`)]),
        h('div', { class: 'grade-pill', style: `background:${g.color}1a;color:${g.color};` }, [
          h('div', { class: 'grade-letter' }, g.grade), h('div', { class: 'grade-label' }, g.label),
        ]),
      ]),
      h('div', { class: 'bar' }, h('div', { class: 'bar-fill', style: `width:${pct}%;background:${g.color};` })),
      h('div', { class: 'score-detail' }, [
        h('span', {}, `${pct}%`),
        h('span', {}, `ពហុជ្រើសរើស ${s.mcq_score}/${s.mcq_max}`),
        s.writing_score != null ? h('span', {}, `សរសេរ ${s.writing_score}/${s.writing_max}`) : null,
      ]),
      h('div', { class: 'row', style: 'margin-top:12px;' }, [
        h('a', { class: 'btn secondary btn-sm', href: `review.html?session=${s.session_id}` }, '🔍 មើលចម្លើយត្រូវ/ខុស'),
        h('a', { class: 'btn btn-sm', href: `review.html?session=${s.session_id}&print=1`, title: 'រក្សាទុកជា PDF' }, '📄 ទាញយករបាយការណ៍ PDF'),
      ]),
    ]);
  }
  const text = s.state === 'pending' ? ['⏳ បានប្រគល់ — រង់ចាំលោកគ្រូប្រកាសលទ្ធផល', 'chip-soon'] : ['អវត្តមាន — មិនបានចូលប្រឡង', 'chip-closed'];
  return h('div', { class: 'score-card' }, [head, h('div', { style: 'margin-top:8px;' }, h('span', { class: `chip ${text[1]}` }, text[0]))]);
}

// ---------- Waiting for the start time ----------
function showWaiting(s, pin, startAt) {
  showView('wait');
  document.getElementById('wait-title').textContent = s.test_title;
  document.getElementById('wait-start').textContent = `ចាប់ផ្តើម៖ ${fmtDateTime(new Date(startAt).toISOString())}`;
  const countEl = document.getElementById('wait-count');
  clearInterval(waitInterval);
  let starting = false;
  const tick = async () => {
    const left = startAt - now();
    countEl.textContent = fmtClock(left);
    if (left <= 0 && !starting) {
      starting = true;
      try {
        const res = await api('/api/student/start', { method: 'POST', body: { session_id: s.session_id, pin } });
        syncClock(res.server_now);
        if (!res.waiting) { clearInterval(waitInterval); return loadTest(s.session_id); }
      } catch (e) {
        clearInterval(waitInterval);
        await Exam.notify(e.message);
        return boot();
      }
      starting = false; // clock skew: server said "not yet" — try again next tick
    }
  };
  tick();
  waitInterval = setInterval(tick, 1000);
}
document.getElementById('wait-cancel').onclick = () => { clearInterval(waitInterval); boot(); };

// ---------- Taking the test ----------
async function loadTest(sessionId) {
  clearInterval(waitInterval);
  try {
    const data = await api(`/api/student/test?session_id=${sessionId}`);
    syncClock(data.server_now);
    testState = { ...data, current: 0 };
  } catch (e) {
    await Exam.notify(e.message);
    return boot();
  }
  showView('test');
  document.getElementById('timer-title').textContent = testState.test_title;
  document.getElementById('student-badge').textContent = `${currentStudent.name} (${currentStudent.id})`;
  // Answers kept on this phone but never confirmed by the server (e.g. connection dropped): re-send them.
  const saved = readLocal();
  pending.clear();
  for (const q of testState.questions) {
    if (q.kind === 'writing') continue;
    if (q.selected_index == null && saved[q.id] != null) { q.selected_index = saved[q.id]; pending.add(q.id); }
  }
  flags = new Set(readLocal('flags'));
  setSave(pending.size ? 'busy' : 'ok');
  renderNav();
  renderQuestion();
  startTimer();
  startHeartbeat();
  if (pending.size) flush();
}

// ---------- reliable answer saving ----------
const pending = new Set();
let flushing = false;
let retryTimer = null;
let flags = new Set();
const localKey = (what = 'ans') => `exam_${what}_${testState ? testState.session_id : 'x'}_${currentStudent ? currentStudent.id : 'x'}`;
function readLocal(what = 'ans') { try { return JSON.parse(localStorage.getItem(localKey(what)) || (what === 'flags' ? '[]' : '{}')); } catch { return what === 'flags' ? [] : {}; } }
function writeLocal() {
  try {
    const map = {};
    for (const q of testState.questions) if (q.kind !== 'writing' && q.selected_index != null) map[q.id] = q.selected_index;
    localStorage.setItem(localKey('ans'), JSON.stringify(map));
    localStorage.setItem(localKey('flags'), JSON.stringify([...flags]));
  } catch {}
}
function setSave(state) {
  const el = document.getElementById('save-status');
  if (!el) return;
  el.className = `save-status${state === 'ok' ? '' : state === 'busy' ? ' busy' : ' bad'}`;
  el.textContent = state === 'ok' ? '✓ រក្សាទុកហើយ' : state === 'busy' ? '⏳ កំពុងរក្សាទុក…' : `⚠ មិនទាន់រក្សាទុក (${pending.size}) — កំពុងព្យាយាម`;
}
async function flush() {
  if (PREVIEW || flushing || !testState) return;
  flushing = true;
  clearTimeout(retryTimer);
  let failed = false;
  for (const qid of [...pending]) {
    const q = testState.questions.find((x) => x.id === qid);
    if (!q || q.selected_index == null) { pending.delete(qid); continue; }
    try {
      const r = await api('/api/student/answer', { method: 'POST', body: { session_id: testState.session_id, question_id: qid, selected_index: q.selected_index } });
      if (r.end_at) testState.end_at = r.end_at;
      // only forget it if the student did not change their mind meanwhile
      if (testState.questions.find((x) => x.id === qid).selected_index === q.selected_index) pending.delete(qid);
    } catch (e) {
      if (e.status === 403 || e.status === 409) { pending.clear(); setSave('ok'); flushing = false; return; }   // exam over / other device
      failed = true; break;
    }
  }
  flushing = false;
  if (failed || pending.size) { setSave('bad'); retryTimer = setTimeout(flush, 4000); } else setSave('ok');
}
window.addEventListener('online', () => { if (pending.size) flush(); });

// Poll lightly: picks up extra time from the teacher, and tells the teacher we are online.
let heartbeatTimer = null;
function startHeartbeat() {
  clearInterval(heartbeatTimer);
  if (PREVIEW) return;
  heartbeatTimer = setInterval(async () => {
    if (!testState) return clearInterval(heartbeatTimer);
    try {
      const r = await api(`/api/student/heartbeat?session_id=${testState.session_id}`);
      syncClock(r.server_now);
      if (!r.open) {
        clearInterval(heartbeatTimer); clearInterval(timerInterval);
        await Exam.notify('ការប្រឡងត្រូវបានបញ្ចប់។ ចម្លើយរបស់ប្អូនត្រូវបានរក្សាទុក។');
        testState = null; return boot();
      }
      if (r.end_at && r.end_at !== testState.end_at) testState.end_at = r.end_at;
    } catch {}
  }, 45000);
}

// Warn and log when the student leaves the test page (other tab or app).
let leftCount = 0;
document.addEventListener('visibilitychange', () => {
  if (!testState || views.test.hidden || PREVIEW) return;
  if (document.hidden) {
    leftCount++;
    api('/api/student/left-page', { method: 'POST', body: { session_id: testState.session_id } }).catch(() => {});
  } else {
    Exam.notify(`⚠️ ប្អូនបានចាកចេញពីទំព័រប្រឡង (${leftCount} ដង)។ លោកគ្រូនឹងឃើញការកត់ត្រានេះ។ សូមកុំបើកកម្មវិធីផ្សេងពេលកំពុងប្រឡង។`);
  }
});

function startTimer() {
  clearInterval(timerInterval);
  const bar = document.getElementById('timer-bar');
  const clockEl = document.getElementById('timer-clock');
  const tick = () => {
    const remaining = testState.end_at - now();
    clockEl.textContent = fmtClock(remaining);
    bar.classList.toggle('low', remaining < 5 * 60 * 1000);
    if (remaining <= 0) {
      clearInterval(timerInterval);
      if (PREVIEW) { clockEl.textContent = '00:00:00'; return; }
      Exam.notify('ពេលវេលាប្រឡងបានបញ្ចប់! ប្រព័ន្ធនឹងបញ្ជូនចម្លើយរបស់អ្នកដោយស្វ័យប្រវត្តិ។');
      doSubmit(true);
    }
  };
  tick();
  timerInterval = setInterval(tick, 1000);
}

function renderNav() {
  const nav = document.getElementById('question-nav');
  nav.innerHTML = '';
  let answered = 0;
  const mcqTotal = testState.questions.filter((q) => q.kind !== 'writing').length;
  testState.questions.forEach((q, i) => {
    const writing = q.kind === 'writing';
    if (!writing && q.selected_index != null) answered++;
    nav.append(h('button', {
      class: `${q.selected_index != null ? 'answered ' : ''}${writing ? 'writing ' : ''}${flags.has(q.id) ? 'flagged ' : ''}${i === testState.current ? 'current' : ''}`,
      title: writing ? 'សំណួរសរសេរ' : '',
      onclick: () => { testState.current = i; renderQuestion(); renderNav(); },
    }, writing ? `✎${i + 1 - mcqTotal}` : String(i + 1)));
  });
  document.getElementById('progress-fill').style.width = `${mcqTotal ? (answered / mcqTotal) * 100 : 0}%`;
}

const LETTERS = ['ក', 'ខ', 'គ', 'ឃ', 'ង', 'ច'];

function renderQuestion() {
  const area = document.getElementById('question-area');
  const q = testState.questions[testState.current];
  area.innerHTML = '';

  const totalQ = testState.questions.length;
  const currQ = testState.current + 1;
  const mcqTotal = testState.questions.filter((x) => x.kind !== 'writing').length;

  if (q.kind === 'writing') {
    const no = currQ - mcqTotal;
    const wTotal = totalQ - mcqTotal;
    area.append(h('div', { class: 'question-card writing-card' }, [
      h('div', { class: 'row', style: 'justify-content:space-between;margin-bottom:8px;' }, [
        h('span', { class: 'q-count' }, `ផ្នែក ខ · សំណួរសរសេរទី ${no} / ${wTotal}`),
        h('span', { class: 'chip chip-soon' }, `${q.points} ពិន្ទុ`),
      ]),
      mathEl('div', { class: 'q-stem' }, q.stem_text),
      q.image_key ? h('div', { style: 'text-align:center;margin:10px 0;' }, [h('img', { src: `/api/images/${q.image_key}`, style: 'max-height:300px;border-radius:8px;' })]) : null,
      h('div', { class: 'callout warn', style: 'margin-top:12px;' }, '✎ សរសេរចម្លើយលើក្រដាសឆ្លើយរបស់ប្អូន ដោយបង្ហាញវិធីដោះស្រាយឱ្យបានច្បាស់លាស់។ មិនត្រូវវាយចម្លើយក្នុងកម្មវិធីនេះទេ។'),
    ]));
    area.append(questionNavRow(totalQ));
    return;
  }

  const card = h('div', { class: 'question-card' }, [
    h('div', { class: 'row', style: 'justify-content:space-between;margin-bottom:8px;' }, [
      h('span', { class: 'q-count' }, `ផ្នែក ក · សំណួរទី ${currQ} / ${mcqTotal}`),
      h('div', { class: 'row', style: 'gap:6px;' }, [
        h('button', { class: `flag-btn${flags.has(q.id) ? ' on' : ''}`, title: 'ចំណាំសំណួរនេះដើម្បីត្រឡប់មកមើលវិញ', onclick: () => toggleFlag(q) }, flags.has(q.id) ? '🚩 បានចំណាំ' : '🏳 ចំណាំ'),
        q.selected_index != null
          ? h('span', { class: 'chip chip-open' }, '✓ បានឆ្លើយ')
          : h('span', { class: 'chip chip-closed' }, 'មិនទាន់ឆ្លើយ'),
      ]),
    ]),
    mathEl('div', { class: 'q-stem' }, q.stem_text),
    q.image_key ? h('div', { style: 'text-align:center;margin:10px 0;' }, [h('img', { src: `/api/images/${q.image_key}`, style: 'max-height:300px;border-radius:8px;' })]) : null,
    h('div', { class: 'radio-list' }, q.options.map((opt, idx) => h('label', { class: `radio-opt${q.selected_index === idx ? ' selected' : ''}` }, [
      h('span', { class: 'opt-letter' }, LETTERS[idx] || String(idx + 1)),
      h('input', { type: 'radio', name: 'opt', checked: q.selected_index === idx ? 'checked' : null, onchange: () => selectAnswer(q, idx) }),
      mathEl('span', { class: 'opt-body' }, opt),
    ]))),
  ]);

  area.append(card, questionNavRow(totalQ));
}

function questionNavRow(totalQ) {
  return h('div', { class: 'row', style: 'justify-content:space-between;margin-top:12px;' }, [
    testState.current > 0
      ? h('button', { class: 'secondary', onclick: () => { testState.current--; renderQuestion(); renderNav(); } }, '← សំណួរមុន')
      : h('span', {}),
    testState.current < totalQ - 1
      ? h('button', { onclick: () => { testState.current++; renderQuestion(); renderNav(); } }, 'សំណួរបន្ទាប់ →')
      : h('button', { class: 'good', onclick: submitPrompt }, 'បញ្ជូនចម្លើយ ✓'),
  ]);
}

async function selectAnswer(q, idx) {
  q.selected_index = idx;
  renderQuestion();
  renderNav();
  if (PREVIEW) return;
  writeLocal();
  pending.add(q.id);
  setSave('busy');
  flush();
}

function toggleFlag(q) {
  if (flags.has(q.id)) flags.delete(q.id); else flags.add(q.id);
  if (!PREVIEW) writeLocal();
  renderQuestion(); renderNav();
}

function submitPrompt() {
  const remaining = testState ? testState.end_at - now() : 0;
  const mcqs = testState ? testState.questions.filter((q) => q.kind !== 'writing') : [];
  const hasWriting = testState ? testState.questions.some((q) => q.kind === 'writing') : false;
  const unanswered = mcqs.filter((q) => q.selected_index == null).length;
  const total = mcqs.length;
  const answered = total - unanswered;

  const oldModal = document.getElementById('submit-modal');
  if (oldModal) oldModal.remove();

  const remainingMins = Math.max(0, Math.floor(remaining / 60000));
  const remainingSecs = Math.max(0, Math.floor((remaining % 60000) / 1000));

  const modal = h('div', { id: 'submit-modal', class: 'modal-back' });
  const box = h('div', { class: 'modal-box' }, [
    h('div', { style: 'font-size:42px;margin-bottom:8px;' }, unanswered > 0 ? '⚠️' : '📝'),
    h('h2', { style: 'margin:0 0 10px;' }, 'បញ្ជាក់ការប្រគល់វិញ្ញាសា'),
    remaining > 60000 ? h('div', { class: 'callout warn' }, `⏱ ពេលវេលានៅសល់៖ ${remainingMins} នាទី ${remainingSecs} វិនាទី`) : null,
    unanswered > 0
      ? h('div', { class: 'callout bad' }, `ប្អូនឆ្លើយបាន ${answered}/${total} — នៅសល់ ${unanswered} សំណួរមិនទាន់ឆ្លើយ!`)
      : h('div', { class: 'callout good' }, `✓ ប្អូនបានឆ្លើយគ្រប់ទាំង ${total} សំណួរហើយ!`),
    flags.size ? h('div', { class: 'callout warn' }, `🚩 ប្អូនមាន ${flags.size} សំណួរដែលបានចំណាំទុក — ត្រឡប់មកមើលវិញមុនប្រគល់?`) : null,
    hasWriting ? h('div', { class: 'callout warn' }, '✎ កុំភ្លេចប្រគល់ក្រដាសឆ្លើយផ្នែកសរសេរ ជូនលោកគ្រូ/អ្នកគ្រូ។') : null,
    h('p', { class: 'muted', style: 'margin:12px 0 18px;' }, 'នៅពេលប្រគល់ហើយ ប្អូនមិនអាចត្រឡប់មកកែចម្លើយបានទៀតទេ។'),
    h('div', { style: 'display:flex;flex-direction:column;gap:10px;' }, [
      h('button', { class: 'btn-block', onclick: () => modal.remove() }, '← បន្តធ្វើតេស្តទៀត'),
      h('button', { class: 'danger btn-block', onclick: () => { modal.remove(); doSubmit(false); } }, 'ខ្ញុំយល់ព្រមប្រគល់វិញ្ញាសា'),
    ]),
  ]);
  modal.append(box);
  document.body.append(modal);
}

document.getElementById('submit-btn').addEventListener('click', submitPrompt);

async function doSubmit(auto) {
  if (PREVIEW) { await Exam.notify('នេះគ្រាន់តែជាការមើលសាកល្បង — គ្មានអ្វីត្រូវបានបញ្ជូនទេ។'); return; }
  clearInterval(timerInterval);
  clearInterval(heartbeatTimer);
  const sessionId = testState && testState.session_id;
  // give pending saves a few seconds, then send everything we know in the submit itself
  if (pending.size) await Promise.race([flush(), new Promise((r) => setTimeout(r, 6000))]);
  const answers = {};
  for (const q of testState.questions) if (q.kind !== 'writing' && q.selected_index != null) answers[q.id] = q.selected_index;
  let done = false;
  for (let attempt = 0; attempt < 4 && !done; attempt++) {
    try {
      await api('/api/student/submit', { method: 'POST', body: { session_id: sessionId, submit_type: auto ? 'auto' : 'manual', answers } });
      done = true;
    } catch (e) {
      if (e.status && e.status < 500 && e.status !== 429) { if (!auto) await Exam.notify(e.message); break; }   // refused (e.g. already submitted)
      await new Promise((r) => setTimeout(r, 1500));                                                             // network trouble: try again
    }
  }
  if (!done && !auto) await Exam.notify('មិនអាចបញ្ជូនបានទេ — សូមពិនិត្យអ៊ីនធឺណិត ហើយចុចបញ្ជូនម្តងទៀត។ ចម្លើយរបស់ប្អូនត្រូវបានរក្សាទុកលើទូរស័ព្ទ។');
  if (!done && !auto) { startTimer(); startHeartbeat(); return; }
  try { localStorage.removeItem(localKey('ans')); localStorage.removeItem(localKey('flags')); } catch {}
  testState = null;
  boot();
}

boot();
