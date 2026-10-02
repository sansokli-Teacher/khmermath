const { h, api, typeset, showError, fmtDateTime, fmtClock } = Exam;

const viewLogin = document.getElementById('view-login');
const viewStatus = document.getElementById('view-status');
const viewTest = document.getElementById('view-test');

function showView(name) {
  viewLogin.hidden = name !== 'login';
  viewStatus.hidden = name !== 'status';
  viewTest.hidden = name !== 'test';
}

async function boot() {
  try {
    const data = await api('/api/student/status');
    renderStatus(data);
  } catch {
    showView('login');
  }
}

document.getElementById('login-submit').addEventListener('click', async () => {
  try {
    await api('/api/student/login', { method: 'POST', body: {
      id: document.getElementById('login-id').value.trim(),
      pin: document.getElementById('login-pin').value.trim(),
    } });
    boot();
  } catch (e) { showError(viewLogin.querySelector('.card'), e.message); }
});

function renderStatus(data) {
  if (data.phase === 'open') return loadTest();

  showView('status');
  viewStatus.innerHTML = '';
  const messages = {
    none: ['មិនមានការប្រឡងកំណត់ពេលសម្រាប់ថ្នាក់របស់អ្នកទេ។', ''],
    upcoming: [`${data.test_title}`, `ការប្រឡងនឹងចាប់ផ្តើមនៅ ${fmtDateTime(data.scheduled_start)} (${data.duration_minutes} នាទី)`],
    submitted: [data.test_title, 'អ្នកបានបញ្ជូនចម្លើយរួចរាល់។ សូមរង់ចាំគ្រូប្រកាសលទ្ធផល។'],
    missed: [data.test_title, 'ការប្រឡងនេះបានបិទ ហើយអ្នកមិនបានបញ្ជូនចម្លើយទេ។'],
  };
  if (data.phase === 'published') {
    const total = data.mcq_score + (data.writing_score ?? 0);
    const max = data.mcq_max + (data.writing_max ?? 0);
    viewStatus.append(
      h('h2', {}, data.test_title),
      h('div', { class: 'big-score' }, `${total} / ${max}`),
      h('p', { class: 'muted' }, `ពហុជ្រើសរើស៖ ${data.mcq_score} / ${data.mcq_max}` + (data.writing_score != null ? ` — សរសេរ៖ ${data.writing_score} / ${data.writing_max}` : '')),
    );
    return;
  }
  const [title, sub] = messages[data.phase] || ['', ''];
  viewStatus.append(h('h2', {}, title), h('p', { class: 'muted' }, sub));
}

// ---------- Taking the test ----------
let testState = null;
let timerInterval = null;

async function loadTest() {
  const data = await api('/api/student/test');
  testState = { ...data, current: 0 };
  showView('test');
  document.getElementById('timer-title').textContent = data.test_title;
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
    if (remaining <= 0) { clearInterval(timerInterval); doSubmit(true); }
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
  const card = h('div', { class: 'question-card' }, [
    h('div', { class: 'muted' }, `សំណួរទី ${testState.current + 1} / ${testState.questions.length}`),
    h('div', { class: 'katex-src' }, q.stem_text),
    q.image_key ? h('img', { src: `/api/images/${q.image_key}` }) : null,
    h('div', { class: 'radio-list' }, q.options.map((opt, idx) => h('label', { class: `radio-opt${q.selected_index === idx ? ' selected' : ''}` }, [
      h('input', { type: 'radio', name: 'opt', checked: q.selected_index === idx ? 'checked' : null, onchange: () => selectAnswer(q, idx) }),
      h('span', { class: 'opt-body' }, opt),
    ]))),
  ]);
  const nextBtn = testState.current < testState.questions.length - 1
    ? h('div', { class: 'row', style: 'justify-content:flex-end' }, h('button', { class: 'secondary', onclick: () => { testState.current++; renderQuestion(); renderNav(); } }, 'បន្ទាប់ →'))
    : null;
  area.append(card);
  if (nextBtn) area.append(nextBtn);
  typeset(card);
}

async function selectAnswer(q, idx) {
  q.selected_index = idx;
  renderQuestion();
  renderNav();
  try { await api('/api/student/answer', { method: 'POST', body: { question_id: q.id, selected_index: idx } }); } catch {}
}

document.getElementById('submit-btn').addEventListener('click', async () => {
  const unanswered = testState.questions.filter((q) => q.selected_index == null).length;
  const msg = unanswered > 0 ? `អ្នកមិនទាន់ឆ្លើយចំនួន ${unanswered} សំណួរ។ ចុងបញ្ជូនឡើយ?` : 'បញ្ជូនចម្លើយឥឡូវ?';
  if (await Exam.confirm(msg)) doSubmit(false);
});

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
