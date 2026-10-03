const { h, api, showError, fmtDateTime, fmtClock } = Exam;

function mathEl(tag, attrs, text) {
  const el = h(tag, attrs);
  el.innerHTML = Exam.mathHtml(text);
  return el;
}

const viewLogin = document.getElementById('view-login');
const viewStatus = document.getElementById('view-status');
const viewTest = document.getElementById('view-test');

function showView(name) {
  viewLogin.hidden = name !== 'login';
  viewStatus.hidden = name !== 'status';
  viewTest.hidden = name !== 'test';
}

let currentStudent = null;

async function boot() {
  try {
    const data = await api('/api/student/status');
    currentStudent = { id: data.student_id, name: data.student_name };
    renderStatus(data);
  } catch {
    showView('login');
  }
}

document.getElementById('login-submit').addEventListener('click', async () => {
  const id = document.getElementById('login-id').value.trim();
  const pin = document.getElementById('login-pin').value.trim();
  if (!id || !pin) {
    showError(viewLogin.querySelector('.card'), 'សូមបញ្ចូលលេខសម្គាល់សិស្ស និង PIN។');
    return;
  }
  try {
    await api('/api/student/login', { method: 'POST', body: { id, pin } });
    boot();
  } catch (e) {
    showError(viewLogin.querySelector('.card'), e.message);
  }
});

async function logoutStudent() {
  try {
    await api('/api/student/logout', { method: 'POST' });
  } catch {}
  currentStudent = null;
  testState = null;
  clearInterval(timerInterval);
  showView('login');
}

const logoutBtn = document.getElementById('student-logout-btn');
if (logoutBtn) logoutBtn.onclick = logoutStudent;

function computeGrade(pct) {
  if (pct >= 85) return { grade: 'A', label: 'ល្អប្រសើរ (A)', color: '#16a34a' };
  if (pct >= 75) return { grade: 'B', label: 'ល្អណាស់ (B)', color: '#2563eb' };
  if (pct >= 65) return { grade: 'C', label: 'ល្អ (C)', color: '#0891b2' };
  if (pct >= 50) return { grade: 'D', label: 'មធ្យម (D)', color: '#d97706' };
  if (pct >= 40) return { grade: 'E', label: 'ខ្សោយ (E)', color: '#ea580c' };
  return { grade: 'F', label: 'ធ្លាក់ (F)', color: '#dc2626' };
}

function renderStatus(data) {
  if (data.phase === 'open') return loadTest();

  showView('status');
  viewStatus.innerHTML = '';

  const studentInfoBox = data.student_name ? h('div', {
    style: 'background:#fff;border:1px solid var(--line);border-radius:10px;padding:12px 18px;margin-bottom:16px;display:flex;align-items:center;justify-content:space-between;width:100%;max-width:480px;'
  }, [
    h('div', {}, [
      h('div', { class: 'muted', style: 'font-size:13px;' }, 'គណនីសិស្ស'),
      h('strong', { style: 'font-size:16px;' }, data.student_name),
      h('span', { class: 'muted', style: 'font-size:13px;' }, ` (អត្តលេខ: ${data.student_id})`),
    ]),
    h('button', { class: 'secondary btn-sm', onclick: logoutStudent }, 'ចាកចេញ'),
  ]) : null;

  const messages = {
    none: ['មិនមានការប្រឡងកំណត់ពេលទេ', 'បច្ចុប្បន្នមិនមានការប្រឡងកំណត់ពេលសម្រាប់ថ្នាក់របស់អ្នកនៅឡើយទេ។'],
    upcoming: [data.test_title || 'ការប្រឡងនឹងមកដល់', `ការប្រឡងនឹងចាប់ផ្តើមនៅ ${fmtDateTime(data.scheduled_start)} (រយៈពេល ${data.duration_minutes} នាទី)`],
    submitted: [data.test_title || 'បានបញ្ជូនចម្លើយ', 'អ្នកបានបញ្ជូនចម្លើយរួចរាល់ហើយ។ សូមរង់ចាំលោកគ្រូប្រកាសលទ្ធផល។'],
    missed: [data.test_title || 'ការប្រឡងបានបញ្ចប់', 'ការប្រឡងនេះបានបិទ ហើយអ្នកមិនបានចូលរួមប្រឡងទេ។'],
  };

  const card = h('div', { class: 'card', style: 'max-width:480px;width:100%;text-align:center;padding:24px 16px;' });

  if (data.phase === 'published') {
    const total = data.mcq_score + (data.writing_score ?? 0);
    const max = data.mcq_max + (data.writing_max ?? 0);
    const pct = max > 0 ? Math.round((total / max) * 100) : 0;
    const g = computeGrade(pct);

    card.append(
      h('h2', { style: 'margin-bottom:6px;' }, data.test_title),
      h('div', { class: 'muted', style: 'margin-bottom:14px;' }, 'លទ្ធផលពិន្ទុរបស់អ្នក'),
      h('div', { class: 'big-score' }, `${total} / ${max}`),
      h('div', { style: `font-size:16px;font-weight:700;color:${g.color};margin:6px 0 14px;` }, `និទ្ទេស ${g.label} (${pct}%)`),
      h('div', { style: 'background:var(--bg);border-radius:8px;padding:12px;margin:12px 0;text-align:left;font-size:15px;' }, [
        h('div', { class: 'list-item' }, [h('span', {}, 'ពិន្ទុពហុជ្រើសរើស (MCQ):'), h('strong', {}, `${data.mcq_score} / ${data.mcq_max}`)]),
        data.writing_score != null ? h('div', { class: 'list-item' }, [h('span', {}, 'ពិន្ទុសរសេរដៃ (Writing):'), h('strong', {}, `${data.writing_score} / ${data.writing_max}`)]): null,
      ].filter(Boolean)),
      h('div', { class: 'row', style: 'justify-content:center;margin-top:16px;' }, [
        h('button', { class: 'secondary', onclick: logoutStudent }, 'ចាកចេញពីគណនី'),
      ])
    );
  } else {
    const [title, sub] = messages[data.phase] || ['', ''];
    card.append(
      h('h2', {}, title),
      h('p', { class: 'muted', style: 'margin:12px 0 20px;' }, sub),
      data.phase === 'upcoming' ? h('button', { onclick: () => location.reload() }, '🔄 ពិនិត្យឡើងវិញ') : null,
    );
  }

  if (studentInfoBox) viewStatus.append(studentInfoBox);
  viewStatus.append(card);
}

// ---------- Taking the test ----------
let testState = null;
let timerInterval = null;

async function loadTest() {
  const data = await api('/api/student/test');
  testState = { ...data, current: 0 };
  showView('test');
  document.getElementById('timer-title').textContent = data.test_title;
  const badgeEl = document.getElementById('student-badge');
  if (badgeEl && currentStudent) {
    badgeEl.textContent = `${currentStudent.name} (${currentStudent.id})`;
  }
  renderNav();
  renderQuestion();
  startTimer();
}

function startTimer() {
  clearInterval(timerInterval);
  const bar = document.getElementById('timer-bar');
  const tick = () => {
    const remaining = testState.end_at - Date.now();
    document.getElementById('timer-clock').textContent = fmtClock(remaining);
    bar.classList.toggle('low', remaining < 5 * 60 * 1000);
    if (remaining <= 0) {
      clearInterval(timerInterval);
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
  testState.questions.forEach((q, i) => {
    nav.append(h('button', {
      class: `${q.selected_index != null ? 'answered ' : ''}${i === testState.current ? 'current' : ''}`,
      onclick: () => { testState.current = i; renderQuestion(); renderNav(); },
    }, String(i + 1)));
  });
}

function renderQuestion() {
  const area = document.getElementById('question-area');
  const q = testState.questions[testState.current];
  area.innerHTML = '';

  const totalQ = testState.questions.length;
  const currQ = testState.current + 1;

  const card = h('div', { class: 'question-card' }, [
    h('div', { class: 'row', style: 'justify-content:space-between;margin-bottom:8px;' }, [
      h('span', { class: 'muted', style: 'font-weight:600;' }, `សំណួរទី ${currQ} / ${totalQ}`),
      q.selected_index != null
        ? h('span', { class: 'badge ready', style: 'font-size:11px;' }, '✓ បានឆ្លើយ')
        : h('span', { class: 'badge draft', style: 'font-size:11px;' }, 'មិនទាន់ឆ្លើយ'),
    ]),
    mathEl('div', { style: 'font-size:17px;font-weight:500;margin:6px 0 12px;' }, q.stem_text),
    q.image_key ? h('div', { style: 'text-align:center;margin:10px 0;' }, [h('img', { src: `/api/images/${q.image_key}`, style: 'max-height:300px;border-radius:8px;' })]) : null,
    h('div', { class: 'radio-list' }, q.options.map((opt, idx) => h('label', { class: `radio-opt${q.selected_index === idx ? ' selected' : ''}` }, [
      h('input', { type: 'radio', name: 'opt', checked: q.selected_index === idx ? 'checked' : null, onchange: () => selectAnswer(q, idx) }),
      mathEl('span', { class: 'opt-body' }, opt),
    ]))),
  ]);

  const navRow = h('div', { class: 'row', style: 'justify-content:space-between;margin-top:12px;' }, [
    testState.current > 0
      ? h('button', { class: 'secondary', onclick: () => { testState.current--; renderQuestion(); renderNav(); } }, '← សំណួរមុន')
      : h('span', {}),
    testState.current < totalQ - 1
      ? h('button', { onclick: () => { testState.current++; renderQuestion(); renderNav(); } }, 'សំណួរខាងមុខ →')
      : h('button', { style: 'background:var(--good);', onclick: submitPrompt }, 'បញ្ជូនចម្លើយ ✓'),
  ]);

  area.append(card, navRow);
}

async function selectAnswer(q, idx) {
  q.selected_index = idx;
  renderQuestion();
  renderNav();
  try {
    await api('/api/student/answer', { method: 'POST', body: { question_id: q.id, selected_index: idx } });
  } catch {}
}

function submitPrompt() {
  const unanswered = testState.questions.filter((q) => q.selected_index == null).length;
  const msg = unanswered > 0
    ? `អ្នកនៅសល់សំណួរចំនួន ${unanswered} មិនទាន់ឆ្លើយ។ តើអ្នកពិតជាចង់បញ្ជូនចម្លើយឥឡូវនេះឬ?`
    : 'តើអ្នកពិតជាចង់បញ្ជូនចម្លើយប្រឡងឥឡូវនេះឬ?';
  if (confirm(msg)) doSubmit(false);
}

document.getElementById('submit-btn').addEventListener('click', submitPrompt);

async function doSubmit(auto) {
  clearInterval(timerInterval);
  try {
    await api('/api/student/submit', { method: 'POST' });
  } catch (e) {
    if (!auto) await Exam.notify(e.message);
  }
  boot();
}

boot();
