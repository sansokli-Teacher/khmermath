const { h, api, typeset, showError, fmtDateTime } = Exam;

const viewSetup = document.getElementById('view-setup');
const viewLogin = document.getElementById('view-login');
const viewDashboard = document.getElementById('view-dashboard');

async function boot() {
  try {
    const { needs_setup } = await api('/api/teacher/setup-status');
    if (needs_setup) { viewSetup.hidden = false; return; }
    await api('/api/teacher/me');
    viewDashboard.hidden = false;
    initDashboard();
  } catch {
    viewLogin.hidden = false;
  }
}

document.getElementById('setup-submit').addEventListener('click', async () => {
  try {
    await api('/api/teacher/setup', { method: 'POST', body: {
      username: document.getElementById('setup-username').value.trim(),
      password: document.getElementById('setup-password').value,
    } });
    location.reload();
  } catch (e) { showError(viewSetup.querySelector('.card'), e.message); }
});

document.getElementById('login-submit').addEventListener('click', async () => {
  try {
    await api('/api/teacher/login', { method: 'POST', body: {
      username: document.getElementById('login-username').value.trim(),
      password: document.getElementById('login-password').value,
    } });
    location.reload();
  } catch (e) { showError(viewLogin.querySelector('.card'), e.message); }
});

document.getElementById('logout-btn').addEventListener('click', async () => {
  await api('/api/teacher/logout', { method: 'POST' });
  location.reload();
});

function initDashboard() {
  const tabs = document.querySelectorAll('.tabs button');
  tabs.forEach((btn) => btn.addEventListener('click', () => {
    tabs.forEach((b) => b.classList.toggle('active', b === btn));
    ['classes', 'tests', 'schedule', 'grading'].forEach((name) => {
      document.getElementById(`tab-${name}`).hidden = name !== btn.dataset.tab;
    });
    render[btn.dataset.tab]();
  }));
  render.classes();
}

const render = {};

// ---------- Classes & students ----------
let selectedClassId = null;

render.classes = async function () {
  const container = document.getElementById('tab-classes');
  container.innerHTML = '';
  if (selectedClassId) return renderRoster(container);

  const { classes } = await api('/api/classes');
  const card = h('div', { class: 'card' }, [
    h('h2', {}, 'ថ្នាក់'),
    ...classes.map((c) => h('div', { class: 'list-item' }, [
      h('div', {}, [h('strong', {}, c.name), h('span', { class: 'muted' }, ` — ថ្នាក់ទី ${c.grade} — សិស្ស ${c.student_count} នាក់`)]),
      h('button', { class: 'secondary', onclick: () => { selectedClassId = c.id; render.classes(); } }, 'មើលបញ្ជីសិស្ស'),
    ])),
  ]);
  const addCard = h('div', { class: 'card' }, [
    h('h3', {}, 'បង្កើតថ្នាក់ថ្មី'),
    h('div', { class: 'row' }, [
      h('input', { type: 'text', id: 'new-class-name', placeholder: 'ឧ. 7NGS-B', style: 'flex:2' }),
      h('input', { type: 'number', id: 'new-class-grade', placeholder: 'ថ្នាក់ទី', style: 'flex:1' }),
      h('button', { onclick: async () => {
        await api('/api/classes', { method: 'POST', body: { name: document.getElementById('new-class-name').value.trim(), grade: Number(document.getElementById('new-class-grade').value) } });
        render.classes();
      } }, 'បង្កើត'),
    ]),
  ]);
  container.append(card, addCard);
};

let editingStudentId = null;

function studentRow(container, cls, s) {
  if (editingStudentId === s.id) {
    const surnameInput = h('input', { type: 'text', value: s.surname, style: 'min-width:0' });
    const firstNameInput = h('input', { type: 'text', value: s.first_name, style: 'min-width:0' });
    return h('tr', {}, [
      h('td', {}, s.id),
      h('td', {}, surnameInput),
      h('td', {}, firstNameInput),
      h('td', { class: 'row' }, [
        h('button', { onclick: async () => {
          await api(`/api/students/${s.id}`, { method: 'PUT', body: { surname: surnameInput.value.trim(), first_name: firstNameInput.value.trim() } });
          editingStudentId = null;
          renderRoster(container);
        } }, 'រក្សាទុក'),
        h('button', { class: 'secondary', onclick: () => { editingStudentId = null; renderRoster(container); } }, 'បោះបង់'),
      ]),
    ]);
  }
  return h('tr', {}, [
    h('td', {}, s.id), h('td', {}, s.surname), h('td', {}, s.first_name),
    h('td', { class: 'row' }, [
      h('button', { class: 'secondary', onclick: () => { editingStudentId = s.id; renderRoster(container); } }, 'កែ'),
      h('button', { class: 'secondary', onclick: async () => {
        const { pin } = await api(`/api/students/${s.id}/reset-pin`, { method: 'POST' });
        await Exam.notify(`PIN ថ្មីសម្រាប់ ${s.surname} ${s.first_name}: ${pin}`);
      } }, 'កំណត់ PIN ថ្មី'),
    ]),
  ]);
}

async function renderRoster(container) {
  const { classes } = await api('/api/classes');
  const cls = classes.find((c) => c.id === selectedClassId);
  const { students } = await api(`/api/classes/${selectedClassId}/students`);

  const card = h('div', { class: 'card' }, [
    h('div', { class: 'row', style: 'justify-content:space-between' }, [
      h('h2', {}, `បញ្ជីសិស្ស — ${cls ? cls.name : ''}`),
      h('button', { class: 'secondary', onclick: () => { selectedClassId = null; render.classes(); } }, '← ត្រឡប់'),
    ]),
    h('table', {}, [
      h('thead', {}, h('tr', {}, [h('th', {}, 'លេខសម្គាល់'), h('th', {}, 'គោត្តនាម'), h('th', {}, 'នាម'), h('th', {}, '')])),
      h('tbody', {}, students.map((s) => studentRow(container, cls, s))),
    ]),
  ]);

  const addOne = h('div', { class: 'card' }, [
    h('h3', {}, 'បញ្ចូលសិស្សម្នាក់'),
    h('div', { class: 'row' }, [
      h('input', { type: 'text', id: 'one-id', placeholder: 'លេខសម្គាល់', style: 'flex:1' }),
      h('input', { type: 'text', id: 'one-surname', placeholder: 'គោត្តនាម', style: 'flex:1' }),
      h('input', { type: 'text', id: 'one-first-name', placeholder: 'នាម', style: 'flex:1' }),
      h('button', { onclick: async () => {
        const { pin } = await api(`/api/classes/${selectedClassId}/students`, { method: 'POST', body: {
          id: document.getElementById('one-id').value.trim(),
          surname: document.getElementById('one-surname').value.trim(),
          first_name: document.getElementById('one-first-name').value.trim(),
        } });
        await Exam.notify(`PIN: ${pin}`);
        renderRoster(container);
      } }, 'បញ្ចូល'),
    ]),
  ]);

  const bulk = h('div', { class: 'card' }, [
    h('h3', {}, 'នាំចូលបញ្ជីសិស្សច្រើននាក់'),
    h('p', { class: 'muted' }, 'សូមចម្លងបញ្ជីរបស់អ្នក ១ ជួរ ១ សិស្ស ជាទម្រង់៖ លេខសម្គាល់, គោត្តនាម, នាម'),
    h('textarea', { id: 'bulk-text', placeholder: '0109293, សុខ, ដារា\n0109294, សុខ, សុភា' }),
    h('div', { class: 'row', style: 'margin-top:8px' }, [
      h('button', { onclick: async () => {
        const lines = document.getElementById('bulk-text').value.split('\n').map((l) => l.trim()).filter(Boolean);
        const parsed = lines.map((line) => {
          const [id, surname, ...rest] = line.split(',');
          return { id: (id || '').trim(), surname: (surname || '').trim(), first_name: rest.join(',').trim() };
        }).filter((s) => s.id && s.surname && s.first_name);
        if (parsed.length === 0) return;
        const { students: created } = await api(`/api/classes/${selectedClassId}/students/bulk`, { method: 'POST', body: { students: parsed } });
        showPinSheet(cls, created);
      } }, 'នាំចូល និងបង្កើត PIN'),
    ]),
  ]);

  container.innerHTML = '';
  container.append(card, addOne, bulk);
}

function showPinSheet(cls, created) {
  const win = window.open('', '_blank');
  win.document.write(`<html lang="km"><head><meta charset="UTF-8"><title>PIN — ${cls ? cls.name : ''}</title>
    <style>body{font-family:sans-serif;padding:20px}table{border-collapse:collapse;width:100%}td,th{border:1px solid #999;padding:6px 10px;text-align:left}</style>
    </head><body><h2>PIN សម្រាប់ថ្នាក់ ${cls ? cls.name : ''}</h2><table><tr><th>លេខសម្គាល់</th><th>គោត្តនាម</th><th>នាម</th><th>PIN</th></tr>${
      created.map((s) => `<tr><td>${s.id}</td><td>${s.surname}</td><td>${s.first_name}</td><td>${s.pin}</td></tr>`).join('')
    }</table></body></html>`);
  win.document.close();
}

// ---------- Tests ----------
let selectedTestId = null;

render.tests = async function () {
  const container = document.getElementById('tab-tests');
  container.innerHTML = '';
  if (selectedTestId) return renderTestBuilder(container);

  const { tests } = await api('/api/tests');
  const card = h('div', { class: 'card' }, [
    h('h2', {}, 'តេស្ត'),
    ...tests.map((t) => h('div', { class: 'list-item' }, [
      h('div', {}, [h('strong', {}, t.title), h('span', { class: `badge ${t.status}` }, t.status === 'ready' ? 'រួចរាល់' : 'សម្រាង'), h('span', { class: 'muted' }, ` ${t.question_count} សំណួរ`)]),
      h('button', { class: 'secondary', onclick: () => { selectedTestId = t.id; render.tests(); } }, 'កែសម្រួល'),
    ])),
  ]);
  const addCard = h('div', { class: 'card' }, [
    h('h3', {}, 'បង្កើតតេស្តថ្មី'),
    h('div', { class: 'row' }, [
      h('input', { type: 'text', id: 'new-test-title', placeholder: 'ចំណងជើងតេស្ត', style: 'flex:1' }),
      h('button', { onclick: async () => {
        const t = await api('/api/tests', { method: 'POST', body: { title: document.getElementById('new-test-title').value.trim() } });
        selectedTestId = t.id; render.tests();
      } }, 'បង្កើត'),
    ]),
  ]);
  container.append(card, addCard);
};

async function renderTestBuilder(container) {
  const test = await api(`/api/tests/${selectedTestId}`);
  container.innerHTML = '';

  const header = h('div', { class: 'card' }, [
    h('div', { class: 'row', style: 'justify-content:space-between' }, [
      h('h2', {}, test.title),
      h('button', { class: 'secondary', onclick: () => { selectedTestId = null; render.tests(); } }, '← ត្រឡប់'),
    ]),
    h('div', { class: 'row' }, [
      h('span', { class: `badge ${test.status}` }, test.status === 'ready' ? 'រួចរាល់' : 'សម្រាង'),
      test.status !== 'ready'
        ? h('button', { onclick: async () => { await api(`/api/tests/${test.id}`, { method: 'PUT', body: { status: 'ready' } }); renderTestBuilder(container); } }, 'សម្គាល់ថារួចរាល់')
        : h('button', { class: 'secondary', onclick: async () => { await api(`/api/tests/${test.id}`, { method: 'PUT', body: { status: 'draft' } }); renderTestBuilder(container); } }, 'ត្រឡប់ទៅសម្រាង'),
    ]),
  ]);

  const list = h('div', { class: 'card' }, [
    h('h3', {}, `សំណួរ (${test.questions.length})`),
    ...test.questions.map((q, i) => h('div', { class: 'question-card' }, [
      h('div', { class: 'row', style: 'justify-content:space-between' }, [
        h('strong', {}, `${i + 1}.`),
        h('button', { class: 'danger', onclick: async () => { if (await Exam.confirm('លុបសំណួរនេះ?')) { await api(`/api/questions/${q.id}`, { method: 'DELETE' }); renderTestBuilder(container); } } }, 'លុប'),
      ]),
      h('div', { class: 'katex-src' }, q.stem_text),
      q.image_key ? h('img', { src: `/api/images/${q.image_key}` }) : null,
      h('div', { class: 'radio-list' }, q.options.map((opt, idx) => h('div', { class: `radio-opt${idx === q.correct_index ? ' selected' : ''}` }, [
        h('span', {}, idx === q.correct_index ? '✓' : '○'), h('span', { class: 'opt-body' }, opt),
      ]))),
      h('div', { class: 'muted' }, `${q.points} ពិន្ទុ`),
    ])),
  ]);

  container.append(header, list, buildQuestionForm(test, container));
  typeset(list);
}

function buildQuestionForm(test, container) {
  const optionInputs = [0, 1, 2, 3].map((i) => h('input', { type: 'text', placeholder: `ជម្រើស ${i + 1}`, 'data-opt': i }));
  const correctSelect = h('select', { id: 'q-correct' }, optionInputs.map((_, i) => h('option', { value: i }, `ជម្រើស ${i + 1} ត្រឹមត្រូវ`)));
  const stemInput = h('textarea', { id: 'q-stem', placeholder: 'ឧ. បើ x + 3 = 7 តម្លៃ x គឺ \\(x = ?\\)' });
  const pointsInput = h('input', { type: 'number', id: 'q-points', value: '1', style: 'width:90px' });
  const fileInput = h('input', { type: 'file', id: 'q-image', accept: 'image/png,image/jpeg,image/webp,image/svg+xml' });

  return h('div', { class: 'card' }, [
    h('h3', {}, 'បញ្ចូលសំណួរថ្មី'),
    h('label', {}, 'អត្ថបទសំណួរ (អាចបញ្ចូលគណិតវិទ្យាជាមួយ \\( \\) )'),
    stemInput,
    h('label', {}, 'រូបភាព (មិនចាំបាច់)'),
    fileInput,
    h('label', {}, 'ជម្រើសចម្លើយ'),
    ...optionInputs,
    h('label', {}, 'ជម្រើសត្រឹមត្រូវ'),
    correctSelect,
    h('label', {}, 'ពិន្ទុ'),
    pointsInput,
    h('div', { class: 'row', style: 'margin-top:12px' }, [
      h('button', { onclick: async () => {
        const options = optionInputs.map((i) => i.value.trim()).filter(Boolean);
        if (options.length < 2 || !stemInput.value.trim()) { await Exam.notify('សូមបញ្ចូលអត្ថបទសំណួរ និងយ៉ាងតិចជម្រើសចម្លើយពីរ'); return; }
        let image_key = null;
        const file = fileInput.files[0];
        if (file) {
          const buf = await file.arrayBuffer();
          const res = await api('/api/images', { method: 'POST', body: buf, contentType: file.type });
          image_key = res.key;
        }
        await api(`/api/tests/${test.id}/questions`, { method: 'POST', body: {
          stem_text: stemInput.value.trim(), options, correct_index: Number(correctSelect.value),
          points: Number(pointsInput.value) || 1, image_key,
        } });
        renderTestBuilder(container);
      } }, 'បញ្ចូលសំណួរ'),
    ]),
  ]);
}

// ---------- Schedule ----------
render.schedule = async function () {
  const container = document.getElementById('tab-schedule');
  container.innerHTML = '';
  const [{ tests }, { classes }, { sessions }] = await Promise.all([api('/api/tests'), api('/api/classes'), api('/api/sessions')]);
  const readyTests = tests.filter((t) => t.status === 'ready');

  const list = h('div', { class: 'card' }, [
    h('h2', {}, 'ការប្រឡងដែលបានកំណត់ពេល'),
    ...sessions.map((s) => h('div', { class: 'list-item' }, [
      h('div', {}, [h('strong', {}, `${s.test_title} — ${s.class_name}`), h('div', { class: 'muted' }, `${fmtDateTime(s.scheduled_start)} · ${s.duration_minutes} នាទី`)]),
      h('span', { class: `badge ${s.phase}` }, s.phase === 'open' ? 'កំពុងប្រឡង' : s.phase === 'upcoming' ? 'នឹងមកដល់' : 'បានបិទ'),
    ])),
  ]);

  const form = h('div', { class: 'card' }, [
    h('h3', {}, 'កំណត់ពេលប្រឡងថ្មី'),
    readyTests.length === 0 ? h('p', { class: 'muted' }, 'សូមបង្កើតតេស្ត ១ ហើយសម្គាល់ថារួចរាល់ជាមុនសិន។') : null,
    h('label', {}, 'តេស្ត'),
    h('select', { id: 'sch-test' }, readyTests.map((t) => h('option', { value: t.id }, t.title))),
    h('label', {}, 'ថ្នាក់'),
    h('select', { id: 'sch-class' }, classes.map((c) => h('option', { value: c.id }, c.name))),
    h('label', {}, 'ថ្ងៃ និងម៉ោងចាប់ផ្តើម'),
    h('input', { type: 'datetime-local', id: 'sch-start' }),
    h('label', {}, 'រយៈពេល (នាទី)'),
    h('input', { type: 'number', id: 'sch-duration', value: '120' }),
    h('div', { class: 'row', style: 'margin-top:12px' }, [
      h('button', { onclick: async () => {
        const startLocal = document.getElementById('sch-start').value;
        if (!startLocal) { await Exam.notify('សូមជ្រើសរើសថ្ងៃ និងម៉ោង'); return; }
        await api('/api/sessions', { method: 'POST', body: {
          test_id: Number(document.getElementById('sch-test').value),
          class_id: Number(document.getElementById('sch-class').value),
          scheduled_start: new Date(startLocal).toISOString(),
          duration_minutes: Number(document.getElementById('sch-duration').value),
        } });
        render.schedule();
      } }, 'កំណត់ពេល'),
    ]),
  ]);

  container.append(list, form);
};

// ---------- Grading ----------
let selectedSessionId = null;

render.grading = async function () {
  const container = document.getElementById('tab-grading');
  container.innerHTML = '';
  if (selectedSessionId) return renderGradingSession(container);

  const { sessions } = await api('/api/sessions');
  const card = h('div', { class: 'card' }, [
    h('h2', {}, 'ជ្រើសរើសការប្រឡងសម្រាប់ដាក់ពិន្ទុ'),
    ...sessions.map((s) => h('div', { class: 'list-item' }, [
      h('div', {}, [h('strong', {}, `${s.test_title} — ${s.class_name}`), h('div', { class: 'muted' }, fmtDateTime(s.scheduled_start))]),
      h('button', { class: 'secondary', onclick: () => { selectedSessionId = s.id; render.grading(); } }, 'បើក'),
    ])),
  ]);
  container.append(card);
};

async function renderGradingSession(container) {
  const session = await api(`/api/sessions/${selectedSessionId}`);
  container.innerHTML = '';

  const rows = session.roster.map((s) => {
    const total = (s.mcq_score ?? 0) + (s.writing_score ?? 0);
    return h('tr', {}, [
      h('td', {}, `${s.surname} ${s.first_name}`),
      h('td', {}, s.submitted_at ? `${s.mcq_score} / ${session.mcq_max}` : h('span', { class: 'muted' }, 'មិនបានប្រឡង')),
      h('td', {}, h('input', { type: 'number', value: s.writing_score ?? '', 'data-student': s.id, class: 'writing-input' })),
      h('td', {}, h('input', { type: 'number', value: s.writing_max ?? '', 'data-student-max': s.id, class: 'writing-max-input' })),
      h('td', {}, s.submitted_at && s.writing_score != null ? String(total) : '—'),
      h('td', {}, s.published_at ? h('span', { class: 'badge ready' }, 'បង្ហាញហើយ') : h('span', { class: 'muted' }, '—')),
    ]);
  });

  const card = h('div', { class: 'card' }, [
    h('div', { class: 'row', style: 'justify-content:space-between' }, [
      h('h2', {}, `${session.test_title} — ${session.class_name}`),
      h('button', { class: 'secondary', onclick: () => { selectedSessionId = null; render.grading(); } }, '← ត្រឡប់'),
    ]),
    h('table', {}, [
      h('thead', {}, h('tr', {}, [h('th', {}, 'សិស្ស'), h('th', {}, 'ពហុជ្រើសរើស'), h('th', {}, 'សរសេរ (ពិន្ទុ)'), h('th', {}, 'សរសេរ (ពិន្ទុខ្ពស់)'), h('th', {}, 'សរុប'), h('th', {}, 'ស្ថានភាព')])),
      h('tbody', {}, rows),
    ]),
    h('div', { class: 'row', style: 'margin-top:14px' }, [
      h('button', { onclick: async () => {
        const inputs = card.querySelectorAll('.writing-input');
        for (const input of inputs) {
          const id = input.dataset.student;
          const maxInput = card.querySelector(`.writing-max-input[data-student-max="${id}"]`);
          if (input.value === '') continue;
          await api(`/api/sessions/${selectedSessionId}/writing`, { method: 'POST', body: {
            student_id: id, writing_score: Number(input.value), writing_max: Number(maxInput.value) || null,
          } });
        }
        renderGradingSession(container);
      } }, 'រក្សាទុកពិន្ទុសរសេរ'),
      h('button', { class: 'secondary', onclick: async () => { await api(`/api/sessions/${selectedSessionId}/publish`, { method: 'POST' }); renderGradingSession(container); } }, 'បង្ហាញលទ្ធផលដល់សិស្ស'),
    ]),
  ]);
  container.append(card);
}

boot();
