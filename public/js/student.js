const { h, showError, fmtDateTime, fmtTimeOnly, fmtClock } = Exam;
const rawApi = Exam.api;
// While an exam is open, a login that expired (or a cookie the phone dropped) must never cost the
// student their answers: sign in again on the spot, then repeat the request.
const api = async (path, opts) => {
  try { return await rawApi(path, opts); } catch (e) {
    if (e.status === 401 && testState && !PREVIEW && !path.startsWith('/api/student/login')) { await reauth(); return rawApi(path, opts); }
    throw e;
  }
};
let reauthPromise = null;
function reauth() {
  if (reauthPromise) return reauthPromise;
  reauthPromise = new Promise((resolve) => {
    const err = h('div', { class: 'error', hidden: 'hidden' });
    const dob = h('input', { type: 'text', class: 'big-input', placeholder: 'ថ្ងៃខែឆ្នាំកំណើត (ឧ. 15032012)', inputmode: 'numeric', maxlength: '10', hidden: 'hidden' });
    dob.addEventListener('input', (e) => { e.target.value = formatDob(e.target.value); });
    const attempt = async () => {
      try {
        await rawApi('/api/student/login', { method: 'POST', body: { id: currentStudent.id, dob: dob.value.trim() } });
        back.remove(); reauthPromise = null; resolve();
      } catch (e) {
        if (e.data && e.data.need_dob) dob.hidden = false;
        err.hidden = false; err.textContent = e.status ? e.message : 'គ្មានអ៊ីនធឺណិត — កំពុងព្យាយាមម្តងទៀត…';
        if (!e.status) setTimeout(attempt, 4000);
      }
    };
    const back = h('div', { class: 'modal-back', style: 'z-index:10002;' }, h('div', { class: 'modal-box' }, [
      h('div', { style: 'font-size:42px;' }, '🔑'), h('h2', {}, 'សូមចូលម្តងទៀត'),
      h('p', { class: 'muted' }, `ការចូលបានផុតកំណត់ ប៉ុន្តែចម្លើយរបស់ប្អូនមិនបាត់ទេ។ ប្រព័ន្ធកំពុងចូលជា ${currentStudent.name} ឡើងវិញ។`),
      dob, err, h('button', { class: 'btn-block', onclick: attempt }, 'ចូលម្តងទៀត និងបន្តប្រឡង'),
    ]));
    document.body.append(back);
    attempt();
  });
  return reauthPromise;
}
// Connection lost outside the exam page (reload, resume): wait and retry, do not show the login form.
let offlineTimer = null;
function showOffline(retry) {
  clearInterval(offlineTimer);
  showView('offline');
  const go = async () => { try { await rawApi('/api/student/status'); clearInterval(offlineTimer); retry(); } catch (e) { if (e.status === 401) { clearInterval(offlineTimer); retry(); } } };
  offlineTimer = setInterval(go, 5000);
  document.getElementById('offline-retry').onclick = go;
}

function mathEl(tag, attrs, text) {
  const el = h(tag, attrs);
  el.innerHTML = Exam.mathHtml(text);
  return el;
}

// The phone's own clock may be wrong; every countdown uses server time.
let clockSkew = 0;
const now = () => Date.now() + clockSkew;
const syncClock = (serverNow) => { if (serverNow) clockSkew = serverNow - Date.now(); };

const views = ['login', 'home', 'wait', 'offline', 'test', 'reader'].reduce((o, n) => ({ ...o, [n]: document.getElementById(`view-${n}`) }), {});
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
    questions: test.questions.map(Exam.withSample).map((q) => ({ id: q.id, stem_text: q.stem_text, image_key: q.image_key, kind: q.kind, points: q.points, options: q.options, selected_index: null })),
  };
  showView('test');
  document.getElementById('preview-banner').hidden = false;
  document.getElementById('timer-title').textContent = test.title;
  document.getElementById('student-badge').textContent = 'របៀបមើលជាសិស្ស';
  applyReader(); renderNav(); renderQuestion(); startTimer();
}

// ---------- Sign in ----------
async function boot() {
  if (PREVIEW) return bootPreview();
  stopIntegrity();
  clearInterval(offlineTimer);
  clearInterval(homeRefresh);
  try {
    const data = await api('/api/student/status');
    syncClock(data.server_now);
    currentStudent = { id: data.student_id, name: data.student_name };
    renderHome(data);
  } catch (e) {
    if (e && !e.status) return showOffline(boot);          // no network: not the same as being logged out
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
// Join the live quiz with the code from the teacher (the student's own name is filled in, nothing is put in the address)
async function homeworkCard(holder) {
  try {
    const { games, locked } = await api('/api/student/games');
    if (locked || !games.length) return;
    holder.append(h('div', { class: 'card', style: 'margin:12px 0;border:2px solid #1c7ed6' }, [
      h('div', { style: 'font-weight:700;margin-bottom:6px' }, '📚 កិច្ចការផ្ទះ — ហ្គេមសំណួរ'),
      ...games.map((g) => {
        const dl = new Date(g.deadline).toLocaleString('km-KH', { dateStyle: 'medium', timeStyle: 'short' });
        const btn = g.open ? h('button', { type: 'button', onclick: async () => {
          try {
            const r = await api('/api/student/games/join', { method: 'POST', body: { code: g.code } });
            sessionStorage.setItem('km_live_v1', JSON.stringify({ code: r.code, pid: r.pid, token: r.token, name: r.name, avatar: r.avatar }));
            location.href = '/live';
          } catch (e) { showError(e); }
        } }, g.done ? 'មើលលទ្ធផល' : g.started ? 'បន្តលេង' : 'ចាប់ផ្តើមលេង') : h('span', { class: 'muted' }, 'ផុតកំណត់');
        return h('div', { style: 'display:flex;justify-content:space-between;gap:8px;align-items:center;flex-wrap:wrap;padding:6px 0;border-top:1px solid var(--line)' }, [
          h('div', {}, [h('div', {}, `មេរៀន ${g.lessons.map((n) => (n >= 100 ? `${Math.floor(n / 100) + 7}/${n % 100}` : n)).join(', ')} · ${g.total} សំណួរ`), h('small', { class: 'muted' }, `ផុតកំណត់ ${dl}${g.started ? ` · ពិន្ទុ ${g.score}` : ''}`)]), btn]);
      }),
    ]));
  } catch { /* the home screen works without it */ }
}

function gameCard(studentName) {
  const code = h('input', { type: 'text', inputmode: 'numeric', maxlength: 6, placeholder: 'លេខកូដ ៦ ខ្ទង់', style: 'max-width:180px;text-align:center;letter-spacing:.2em;font-weight:700' });
  const go = () => {
    const c = code.value.replace(/\D/g, '');
    if (c.length !== 6) return code.focus();
    try { sessionStorage.setItem('km_live_name', studentName); } catch {}
    location.href = `/live?c=${c}`;
  };
  code.onkeydown = (e) => { if (e.key === 'Enter') go(); };
  return h('div', { class: 'card', style: 'margin:12px 0' }, [
    h('div', { style: 'font-weight:700;margin-bottom:6px' }, '📱 ចូលហ្គេមសំណួរផ្ទាល់'),
    h('div', { class: 'muted', style: 'margin-bottom:8px' }, 'បើលោកគ្រូអ្នកគ្រូឱ្យលេខកូដ ឬ QR សូមវាយលេខកូដនៅទីនេះ។'),
    h('div', { style: 'display:flex;gap:8px;flex-wrap:wrap' }, [code, h('button', { type: 'button', onclick: go }, 'ចូលលេង')]),
  ]);
}

// ---------- in-page reader: lessons, formulas and PISA practice stay inside this page ----------
let readerUrl = null, readerTimer = null;
function openReader(url, title) {
  const frame = document.getElementById('rd-frame'), loading = document.getElementById('rd-loading');
  readerUrl = url;
  document.getElementById('rd-title').textContent = title;
  loading.hidden = false; loading.textContent = 'កំពុងបើក…';
  frame.onload = () => { clearTimeout(readerTimer); loading.hidden = true; };
  frame.src = url;
  clearTimeout(readerTimer);
  readerTimer = setTimeout(() => { if (!loading.hidden) { loading.textContent = 'ការផ្ទុកយឺត — សូមពិនិត្យអ៊ីនធឺណិត ឬចុច ⟲ ដើម្បីព្យាយាមម្តងទៀត។'; setTimeout(() => { loading.hidden = true; }, 6000); } }, 9000);
  showView('reader');
  try { history.pushState({ reader: 1 }, ''); } catch { /* ignore */ }
}
function closeReader(fromPop) {
  if (views.reader.hidden) return;
  clearTimeout(readerTimer);
  document.getElementById('rd-frame').src = 'about:blank';
  showView('home');
  if (!fromPop) { try { if (history.state && history.state.reader) history.back(); } catch { /* ignore */ } }
}
document.getElementById('rd-close').addEventListener('click', () => closeReader(false));
document.getElementById('rd-reload').addEventListener('click', () => { if (readerUrl) { const l = document.getElementById('rd-loading'); l.hidden = false; l.textContent = 'កំពុងបើក…'; document.getElementById('rd-frame').src = readerUrl; } });
window.addEventListener('popstate', () => closeReader(true));

// ---------- learning + games hub (by the student's grade) ----------
const SITE = 'https://khmermath.org';
const CBA = 'https://cba.khmermath.org';
const GAMES = [
  { style: 'cards', icon: '🃏', name: 'កាតបើក', desc: 'ជ្រើសប្រអប់លេខ ប្រយ័ត្នប្រអប់ពិសេស', img: 'img/play/teamgame.jpg' },
  { style: 'wheel', icon: '🎡', name: 'កង់វិល', desc: 'បង្វិលកង់ ហើយកង់ជ្រើសសំណួរឱ្យ', img: 'img/play/wheel.jpg' },
  { style: 'boat', icon: '🚣', name: 'ប្រណាំងទូកង', desc: 'ឆ្លើយត្រូវ ទូកទៅមុខ ដល់ទីបញ្ចប់មុនគេឈ្នះ', img: 'img/play/boat.jpg' },
];
const khd = (n) => String(n).replace(/\d/g, (d) => '០១២៣៤៥៦៧៨៩'[d]);

let gameBank = null;                       // lessons of the game question bank, loaded once
async function loadGameBank() {
  if (gameBank) return gameBank;
  try { const r = await fetch('/api/game/bank', { cache: 'no-cache' }); if (r.ok) gameBank = await r.json(); } catch { /* the chooser just stays hidden */ }
  if (!gameBank || !gameBank.lessons) { try { const r = await fetch('data/teamgame_g7.json'); if (r.ok) gameBank = await r.json(); } catch { /* ignore */ } }
  return gameBank;
}

function openGame(g, grade, myName) {
  document.querySelectorAll('.gm-back').forEach((e) => e.remove());
  let who = 'solo', count = 2, qn = 10;
  let lessons = [];                          // lessons of this grade, filled in when the bank arrives
  const picked = new Set();                  // empty = every lesson
  const lessonBox = h('div', { class: 'gm-lessons', hidden: true });
  const names = ['ខ្ញុំ', 'មិត្តទី ១', 'មិត្តទី ២', 'មិត្តទី ៣'];
  const body = h('div', { class: 'gm-body' });
  const draw = () => {
    body.innerHTML = '';
    body.append(
      h('div', { class: 'gm-seg', role: 'tablist' }, [
        h('button', { type: 'button', class: who === 'solo' ? 'on' : '', onclick: () => { who = 'solo'; draw(); } }, '👤 លេងម្នាក់ឯង'),
        h('button', { type: 'button', class: who === 'friends' ? 'on' : '', onclick: () => { who = 'friends'; draw(); } }, '👥 លេងជាមួយមិត្ត'),
      ]),
    );
    if (who === 'friends') {
      body.append(
        h('div', { class: 'gm-row' }, [h('span', {}, 'ចំនួនអ្នកលេង'), h('div', { class: 'gm-chips' }, [2, 3, 4].map((n) => h('button', { type: 'button', class: count === n ? 'on' : '', onclick: () => { count = n; draw(); } }, khd(n))))]),
        h('div', { class: 'gm-names' }, [...Array(count).keys()].map((i) => h('input', { type: 'text', maxlength: '20', value: names[i], 'aria-label': `ឈ្មោះអ្នកលេងទី ${i + 1}`, oninput: (e) => { names[i] = e.target.value; } }))),
        h('p', { class: 'muted', style: 'margin:6px 0 0;font-size:13px;' }, 'ប្តូរវេនគ្នាឆ្លើយ — ប្រើទូរស័ព្ទ ឬកុំព្យូទ័រតែមួយជាមួយគ្នា។'),
      );
    }
    body.append(lessonBox);
    body.append(h('div', { class: 'gm-row' }, [h('span', {}, 'ចំនួនសំណួរ'), h('div', { class: 'gm-chips' }, [5, 10, 20].map((n) => h('button', { type: 'button', class: qn === n ? 'on' : '', onclick: () => { qn = n; draw(); } }, khd(n))))]));
  };
  draw();
  const drawLessons = () => {
    lessonBox.innerHTML = '';
    if (!lessons.length) { lessonBox.hidden = true; return; }
    lessonBox.hidden = false;
    const all = picked.size === 0;
    const total = lessons.filter((L) => all || picked.has(L.n)).reduce((t, L) => t + (L.qs ? L.qs.length : 0), 0);
    lessonBox.append(
      h('div', { class: 'gm-row', style: 'margin-bottom:4px;' }, [h('span', {}, 'មេរៀនដែលចង់លេង'), h('span', { class: 'muted', style: 'font-size:13px;font-weight:500;' }, `${all ? 'គ្រប់មេរៀន' : `បានជ្រើស ${khd(picked.size)} មេរៀន`} · ${khd(total)} សំណួរ`)]),
      h('div', { class: 'gm-chips wrap' }, [
        h('button', { type: 'button', class: all ? 'on' : '', onclick: () => { picked.clear(); drawLessons(); } }, 'ទាំងអស់'),
        ...lessons.map((L) => h('button', { type: 'button', class: picked.has(L.n) ? 'on' : '', title: L.title || '', onclick: () => { if (picked.has(L.n)) picked.delete(L.n); else picked.add(L.n); drawLessons(); } }, [`មេរៀនទី ${khd(L.d || L.n)}`, L.title ? h('small', {}, L.title) : null])),
      ]),
    );
  };
  loadGameBank().then((bank) => { if (!bank || !bank.lessons) return; lessons = bank.lessons.filter((L) => (L.g || 7) === grade && L.qs && L.qs.length); drawLessons(); });
  const go = () => {
    const players = who === 'solo' ? [myName || 'ខ្ញុំ'] : names.slice(0, count).map((x, i) => (x || '').trim() || (i ? `មិត្តទី ${khd(i)}` : 'ខ្ញុំ'));
    const l = picked.size && picked.size < lessons.length ? `&l=${[...picked].join(',')}` : '';
    location.href = `teamgame.html?student=1&style=${g.style}&grade=${grade}&n=${qn}${l}&p=${encodeURIComponent(players.join('|'))}`;
  };
  const back = h('div', { class: 'modal-back gm-back', onclick: (e) => { if (e.target === back) back.remove(); } }, [
    h('div', { class: 'modal-box gm-box', role: 'dialog', 'aria-modal': 'true' }, [
      h('div', { class: 'gm-head' }, [h('span', { class: 'gm-ico' }, g.icon), h('div', {}, [h('h2', { style: 'margin:0;' }, g.name), h('p', { class: 'muted', style: 'margin:2px 0 0;' }, `ថ្នាក់ទី ${khd(grade)} · ${g.desc}`)])]),
      body,
      h('div', { class: 'row', style: 'justify-content:flex-end;margin-top:16px;' }, [h('button', { class: 'secondary', onclick: () => back.remove() }, 'បោះបង់'), h('button', { onclick: go }, '▶ ចាប់ផ្ដើមលេង')]),
    ]),
  ]);
  document.body.append(back);
}

function hubSection(data) {
  const g = Number(data.grade) || 0;
  const wrap = h('div', { class: 'hub' });
  if (!g) return wrap;
  const hasLessons = g >= 7 && g <= 9;
  const hasGames = g >= 7 && g <= 9;
  const link = (href, label, title) => h('button', { type: 'button', class: 'btn', onclick: () => openReader(href, title || label) }, label);
  const tile = (icon, title, desc, actions, tone) => h('div', { class: `hub-tile${tone ? ' ' + tone : ''}` }, [h('div', { class: 'hub-ico', 'aria-hidden': 'true' }, icon), h('div', { class: 'hub-t' }, title), h('div', { class: 'hub-d' }, desc), h('div', { class: 'hub-a' }, actions)]);

  wrap.append(h('h2', { class: 'section-title' }, `រៀន និងហ្វឹកហាត់ — ថ្នាក់ទី ${khd(g)}`));
  wrap.append(h('div', { class: 'hub-grid' }, [
    hasLessons
      ? tile('📘', `មេរៀនថ្នាក់ទី ${khd(g)}`, 'មេរៀនគ្រប់ជំពូក មានឧទាហរណ៍ លំហាត់គំរូ និងលំហាត់ប្រតិបត្តិ។', [link(`${SITE}/lesson/g${g}/`, 'បើកមេរៀន →', `មេរៀនថ្នាក់ទី ${khd(g)}`)], 'blue')
      : tile('📘', `មេរៀនថ្នាក់ទី ${khd(g)}`, 'កំពុងរៀបចំ — នឹងមកដល់ឆាប់ៗ។', [h('span', { class: 'chip chip-soon' }, 'ឆាប់ៗនេះ')], 'blue soon'),
    tile('📐', `រូបមន្តថ្នាក់ទី ${khd(g)}`, 'សៀវភៅរូបមន្តសង្ខេប ងាយស្រួលរកមើល និងចងចាំ។', [link(`${SITE}/formular/g${g}/`, 'បើករូបមន្ត →', `រូបមន្តថ្នាក់ទី ${khd(g)}`)], 'teal'),
    tile('🌏', 'PISA TEST (MoEYS)', 'ប្រធានបទតេស្តគំរូ PISA ៣៨ ពីក្រសួងអប់រំ — សម្រាប់គ្រប់ថ្នាក់។', [link(`${CBA}/?nocert=1#moeys`, 'ចាប់ផ្ដើមហាត់ →', 'PISA TEST (MoEYS)')], 'amber'),
    tile('🧠', `PISA ថ្នាក់ទី ${khd(g)}`, 'លំហាត់ PISA តាមថ្នាក់របស់អ្នក — កំពុងរៀបចំ។', [h('span', { class: 'chip chip-soon' }, 'ឆាប់ៗនេះ')], 'violet soon'),
  ]));

  if (hasGames) {
    wrap.append(h('h2', { class: 'section-title' }, 'ហ្គេមគណិតវិទ្យា'));
    wrap.append(h('p', { class: 'muted', style: 'margin:-6px 0 12px;' }, `លេងម្នាក់ឯង ឬជាមួយមិត្ត — សំណួរមេរៀនថ្នាក់ទី ${khd(g)}។`));
    wrap.append(h('div', { class: 'game-grid' }, GAMES.map((gm) => h('button', { type: 'button', class: 'game-tile', onclick: () => openGame(gm, g, data.student_name && !/^សិស្ស \d/.test(data.student_name) ? data.student_name : 'ខ្ញុំ') }, [
      h('img', { src: gm.img, alt: '', loading: 'lazy' }),
      h('span', { class: 'game-ico' }, gm.icon),
      h('span', { class: 'game-name' }, gm.name),
      h('span', { class: 'game-desc' }, gm.desc),
      h('span', { class: 'game-go' }, 'លេង →'),
    ]))));
  }
  return wrap;
}

function renderHome(data) {
  clearInterval(timerInterval);
  clearInterval(waitInterval);
  showView('home');
  document.getElementById('home-name').textContent = data.student_name;
  const av = document.getElementById('home-avatar'); if (av) av.textContent = [...String(data.student_name || '?')][0];
  document.getElementById('home-sub').textContent = `អត្តលេខ ${data.student_id}${data.class_name ? ` · ថ្នាក់ ${data.class_name}` : ''}`;
  const body = document.getElementById('home-body');
  body.innerHTML = '';

  // --- upcoming / open tests first: that is why most students open this page
  body.append(h('h2', { class: 'section-title', style: 'margin-top:4px;' }, 'ការប្រឡងខាងមុខ'));
  if (data.upcoming.length === 0) {
    body.append(h('div', { class: 'empty-card' }, [
      h('div', { class: 'empty-icon' }, '📭'),
      h('div', { style: 'font-weight:600;' }, 'មិនទាន់មានការប្រឡងនៅឡើយទេ'),
      h('div', { class: 'muted' }, 'នៅពេលលោកគ្រូកំណត់ការប្រឡង វានឹងបង្ហាញនៅទីនេះ។'),
    ]));
  }
  for (const s of data.upcoming) body.append(examCard(s));

  body.append(hubSection(data));
  body.append(gameCard(data.student_name));
  const hwHolder = h('div', {}); body.append(hwHolder); homeworkCard(hwHolder);
  body.append(installCard());
  if (data.year) body.append(yearCard(data.year));
  const progressHolder = h('div', {});
  body.append(progressHolder);
  fillProgress(progressHolder);

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

// ---------- progress over the year, practice, install ----------
async function fillProgress(holder) {
  let d;
  try { d = await api('/api/student/progress'); } catch { return; }
  if (!d.exams.length) return;
  const pts = d.exams.filter((e) => e.pct != null);
  const W = 300, H = 70, step = pts.length > 1 ? (W - 20) / (pts.length - 1) : 0;
  const xy = pts.map((e, i) => [10 + i * step, H - 8 - (e.pct / 100) * (H - 16)]);
  const svg = `<svg viewBox="0 0 ${W} ${H}" width="100%" height="${H}" role="img" aria-label="ពិន្ទុតាមការប្រឡង"><line x1="0" y1="${H - 8 - (H - 16) * 0.5}" x2="${W}" y2="${H - 8 - (H - 16) * 0.5}" stroke="#dce1d9" stroke-dasharray="3 4"/>`
    + (xy.length > 1 ? `<polyline fill="none" stroke="#285b55" stroke-width="2.5" points="${xy.map((p) => p.join(',')).join(' ')}"/>` : '')
    + xy.map(([x, y], i) => `<circle cx="${x}" cy="${y}" r="4" fill="#285b55"><title>${String(pts[i].title).replace(/[<&]/g, '')}: ${pts[i].pct}%</title></circle>`).join('') + '</svg>';
  const trend = (t) => {
    const s = t.series.filter((x) => x.pct != null);
    if (s.length < 2) return '';
    const dlt = s[s.length - 1].pct - s[s.length - 2].pct;
    return dlt >= 8 ? ' ↑' : dlt <= -8 ? ' ↓' : ' →';
  };
  const weak = d.topics.slice(0, 6);
  const chart = h('div', {}); chart.innerHTML = svg;
  holder.append(h('div', { class: 'year-card', style: 'margin-top:12px;' }, [
    h('h2', { style: 'margin:0 0 6px;' }, '📚 ការរីកចម្រើនរបស់ខ្ញុំ'),
    h('div', { class: 'muted', style: 'font-size:13px;' }, `ពិន្ទុ ${pts.length} ការប្រឡងចុងក្រោយ (${pts.map((e) => e.pct + '%').join(' → ')})`),
    chart,
    weak.length ? h('div', { style: 'margin-top:8px;' }, [h('div', { style: 'font-weight:700;margin-bottom:4px;' }, 'ប្រធានបទដែលត្រូវរៀនបន្ថែមមុនគេ'), ...weak.map((t) => {
      const col = t.pct >= 70 ? '#16a34a' : t.pct >= 50 ? '#d97706' : '#dc2626';
      return h('div', { class: 'topic-row', style: 'cursor:default;' }, [
        h('div', { style: 'flex:1;min-width:0;font-weight:600;' }, t.name),
        h('div', { class: 'bar', style: 'width:36%;' }, h('div', { class: 'bar-fill', style: `width:${t.pct}%;background:${col};` })),
        h('div', { style: `width:64px;text-align:right;font-weight:700;color:${col};` }, `${t.pct}%${trend(t)}`),
      ]);
    })]) : null,
    d.wrong_count ? h('div', { style: 'margin-top:12px;' }, h('a', { class: 'btn btn-block', href: 'practice.html' }, `🔁 ហាត់សំណួរដែលធ្លាប់ខុស (${d.wrong_count})`)) : null,
  ]));
}

let installEvent = null;
window.addEventListener('beforeinstallprompt', (e) => { e.preventDefault(); installEvent = e; });
function installCard() {
  const standalone = matchMedia('(display-mode: standalone)').matches || navigator.standalone;
  if (standalone) return h('div', {});
  const ios = /iphone|ipad|ipod/i.test(navigator.userAgent);
  const box = h('div', { class: 'callout', style: 'margin-top:14px;' });
  const draw = () => {
    box.innerHTML = '';
    if (installEvent) box.append('📲 ដាក់កម្មវិធីនេះលើអេក្រង់ដើមទូរស័ព្ទ ដើម្បីបើកបានលឿន។ ', h('button', { class: 'btn-sm', onclick: async () => { installEvent.prompt(); await installEvent.userChoice.catch(() => {}); installEvent = null; box.remove(); } }, 'ដំឡើង'));
    else if (ios) box.append('📲 លើ iPhone/iPad៖ ចុចប៊ូតុង «ចែករំលែក» (Share) រួចជ្រើស «Add to Home Screen» ដើម្បីបើកបានលឿន។');
    else box.hidden = true;
  };
  draw(); setTimeout(draw, 1500);
  return box;
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
  const any = y.assessments.some((a) => a.pct != null);
  const body = [
    h('div', { class: 'year-steps' }, steps),
    h('div', { class: 'year-sum' }, [
      tile('មធ្យមភាគប្រចាំខែ', y.monthly_avg),
      tile('ពិន្ទុឆមាសទី១', y.semester1),
      tile('មធ្យមភាគប្រចាំឆ្នាំ', y.year_avg, true),
    ]),
    h('div', { class: 'row', style: 'margin-top:12px;' }, [h('a', { class: 'btn secondary btn-sm', href: 'reportcard.html', target: '_blank' }, '📄 ទាញយកសៀវភៅរបាយការណ៍ (PDF)')]),
  ];
  // nothing to show yet: keep the card folded so the first screen is about the exams
  const det = h('details', { class: 'year-card', style: 'margin-bottom:8px;' }, [
    h('summary', { class: 'year-head' }, [
      h('h2', { style: 'margin:0;' }, `📈 ពិន្ទុឆ្នាំសិក្សា ${y.label}`),
      h('span', { class: 'muted' }, any ? `ឆមាស = មធ្យមខែ ${y.monthly_weight}% + ប្រឡងឆមាស ${y.exam_weight}%` : 'មិនទាន់មានពិន្ទុ — ចុចមើល'),
    ]),
    ...body,
  ]);
  if (any) det.open = true;
  return det;
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
    if (!(s.started && isOpen) && !(await readyCheck(s))) return;
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

// ---------- Before starting: identity, duration, instructions, connection ----------
async function readyCheck(s) {
  const status = (ok, text) => h('div', { class: `ready-row ${ok === true ? 'ok' : ok === false ? 'bad' : 'warn'}` }, [h('span', {}, ok === true ? '✓' : ok === false ? '✗' : '⚠'), h('span', {}, text)]);
  const checks = h('div', { class: 'ready-checks' });
  const t0 = performance.now();
  let net = null, ms = 0;
  try { const d = await api('/api/student/status'); syncClock(d.server_now); ms = Math.round(performance.now() - t0); net = true; } catch { net = false; }
  checks.append(
    status(net ? (ms < 1500 ? true : null) : false, net ? (ms < 1500 ? `ការតភ្ជាប់ល្អ (${ms} ms)` : `ការតភ្ជាប់យឺត (${ms} ms) — ចម្លើយអាចរក្សាទុកយឺត`) : 'មិនអាចតភ្ជាប់ទៅម៉ាស៊ីនមេបានទេ — សូមពិនិត្យអ៊ីនធឺណិត'),
  );
  let store = true; try { localStorage.setItem('exam_probe', '1'); localStorage.removeItem('exam_probe'); } catch { store = false; }
  checks.append(status(store, store ? 'ទូរស័ព្ទអាចរក្សាចម្លើយទុកបណ្ដោះអាសន្នបាន' : 'ទូរស័ព្ទមិនអាចរក្សាចម្លើយទុកបណ្ដោះអាសន្ន (កុំប្រើផ្ទាំង Private)'));
  if (Math.abs(clockSkew) > 120000) checks.append(status(null, 'ម៉ោងលើទូរស័ព្ទមិនត្រឹមត្រូវ — ប្រព័ន្ធនឹងប្រើម៉ោងរបស់ម៉ាស៊ីនមេជំនួស'));
  try {
    if (navigator.getBattery) { const b = await navigator.getBattery(); if (!b.charging && b.level < 0.2) checks.append(status(null, `ថ្មសល់ ${Math.round(b.level * 100)}% — សូមសាកថ្មមុនប្រឡង`)); }
  } catch {}
  return new Promise((resolve) => {
    const finish = (v) => { back.remove(); resolve(v); };
    const back = h('div', { class: 'modal-back', style: 'align-items:flex-start;overflow:auto;' }, h('div', { class: 'modal-box', style: 'margin:auto;max-width:480px;text-align:left;' }, [
      h('h2', { style: 'margin:0 0 4px;text-align:center;' }, 'ត្រៀមខ្លួនមុនប្រឡង'),
      h('div', { class: 'ready-who' }, [h('div', { class: 'muted' }, 'ប្អូនកំពុងចូលប្រឡងក្នុងនាម'), h('div', { class: 'ready-name' }, currentStudent.name), h('div', { class: 'muted' }, `អត្តលេខ ${currentStudent.id}`)]),
      h('div', { class: 'ready-exam' }, [h('b', {}, s.test_title), h('div', { class: 'muted' }, `⏱ ${s.duration_minutes} នាទី · 🏁 បញ្ចប់ ${fmtTimeOnly(s.scheduled_end)}`)]),
      checks,
      h('div', { class: 'ready-rules' }, [
        h('b', {}, 'ណែនាំ'),
        h('ul', {}, [
          h('li', {}, 'ចម្លើយរក្សាទុកដោយស្វ័យប្រវត្តិ។ បើអ៊ីនធឺណិតដាច់ ចម្លើយនៅតែនៅលើទូរស័ព្ទ។'),
          h('li', {}, 'កុំចាកចេញពីទំព័រប្រឡង — លោកគ្រូអ្នកគ្រូនឹងឃើញការកត់ត្រានេះ។'),
          h('li', {}, 'ប្រើតែឧបករណ៍មួយប៉ុណ្ណោះក្នុងការប្រឡងនេះ។'),
          h('li', {}, 'ចុច «បញ្ជូនចម្លើយ» ពេលចប់។ ផ្នែកសរសេរធ្វើលើក្រដាស។'),
        ]),
      ]),
      h('div', { style: 'display:flex;flex-direction:column;gap:10px;margin-top:14px;' }, [
        h('button', { class: 'btn-block', disabled: net ? null : 'disabled', onclick: () => { Integrity.goFullscreen(); finish(true); } }, 'នេះជាខ្ញុំ — ចាប់ផ្តើមប្រឡង'),
        h('button', { class: 'secondary btn-block', onclick: () => finish(false) }, '← ត្រឡប់ក្រោយ'),
      ]),
    ]));
    document.body.append(back);
  });
}

// ---------- Reading comfort: text size and a distraction-free view ----------
let reader = { size: 1, focus: false, nav: false };
try { reader = { ...reader, ...JSON.parse(localStorage.getItem('exam_reader') || '{}') }; } catch {}
function applyReader() {
  const cls = document.body.classList;
  for (let i = 0; i <= 3; i++) cls.toggle(`ts-${i}`, reader.size === i);
  cls.toggle('focus-mode', !!reader.focus);
  cls.toggle('focus-nav-open', !!reader.focus && !!reader.nav);
  const set = (id, v) => { const el = document.getElementById(id); if (el) el.classList.toggle('on', v); };
  set('rd-focus', reader.focus); set('rd-nav', reader.nav);
  const nav = document.getElementById('rd-nav'); if (nav) nav.hidden = !reader.focus;
  try { localStorage.setItem('exam_reader', JSON.stringify(reader)); } catch {}
}
document.getElementById('rd-smaller').onclick = () => { reader.size = Math.max(0, reader.size - 1); applyReader(); };
document.getElementById('rd-bigger').onclick = () => { reader.size = Math.min(3, reader.size + 1); applyReader(); };
document.getElementById('rd-focus').onclick = () => { reader.focus = !reader.focus; reader.nav = false; applyReader(); };
document.getElementById('rd-nav').onclick = () => { reader.nav = !reader.nav; applyReader(); };
applyReader();

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
    if (!e.status) return showOffline(() => loadTest(sessionId));
    await Exam.notify(e.message);
    return boot();
  }
  showView('test');
  document.getElementById('timer-title').textContent = testState.test_title;
  document.getElementById('student-badge').textContent = `${currentStudent.name} (${currentStudent.id})`;
  if (testState.locked) {                      // locked by the teacher: show no questions until unlocked
    lockedNow = true; applyReader(); renderShield(); startTimer(); startHeartbeat(); return;
  }
  lockedNow = false;
  // Answers kept on this phone but never confirmed by the server (e.g. connection dropped): re-send them.
  const saved = readLocal();
  const unsent = new Set(readLocal('pend'));
  pending.clear();
  for (const q of testState.questions) {
    if (q.kind === 'writing') continue;
    const mine = saved[q.id];
    // an answer that was never confirmed by the server wins over an older one the server still has
    if (mine != null && (q.selected_index == null || (unsent.has(q.id) && mine !== q.selected_index))) { q.selected_index = mine; pending.add(q.id); }
  }
  recovered = pending.size;
  flags = new Set(readLocal('flags'));
  setSave(pending.size ? 'busy' : 'ok');
  applyReader();
  renderNav();
  renderQuestion();
  startTimer();
  startHeartbeat();
  startIntegrity();
  if (pending.size) flush();
  if (recovered) { const n = recovered; recovered = 0; Exam.notify(`↺ បានស្ដារចម្លើយ ${n} ដែលមិនទាន់រក្សាទុកទៅម៉ាស៊ីនមេពីទូរស័ព្ទរបស់ប្អូន — កំពុងបញ្ជូនឥឡូវនេះ។`); }
}

// ---------- reliable answer saving ----------
const pending = new Set();
let recovered = 0;
let flushing = false;
let retryTimer = null;
let flags = new Set();
const localKey = (what = 'ans') => `exam_${what}_${testState ? testState.session_id : 'x'}_${currentStudent ? currentStudent.id : 'x'}`;
const LISTS = ['flags', 'pend'];
function readLocal(what = 'ans') { try { return JSON.parse(localStorage.getItem(localKey(what)) || (LISTS.includes(what) ? '[]' : '{}')); } catch { return LISTS.includes(what) ? [] : {}; } }
function writeLocal() {
  try {
    const map = {};
    for (const q of testState.questions) if (q.kind !== 'writing' && q.selected_index != null) map[q.id] = q.selected_index;
    localStorage.setItem(localKey('ans'), JSON.stringify(map));
    localStorage.setItem(localKey('flags'), JSON.stringify([...flags]));
    localStorage.setItem(localKey('pend'), JSON.stringify([...pending]));
  } catch {}
}
function setSave(state) {
  const el = document.getElementById('save-status');
  if (!el) return;
  const offline = navigator.onLine === false;
  el.className = `save-status${state === 'ok' ? '' : state === 'busy' && !offline ? ' busy' : ' bad'}`;
  el.textContent = state === 'ok' ? '✓ រក្សាទុកហើយ' : state === 'busy' && !offline ? '⏳ កំពុងរក្សាទុក…' : `⚠ មិនទាន់រក្សាទុក (${pending.size})`;
  el.title = pending.size ? 'ចុចដើម្បីព្យាយាមរក្សាទុកម្តងទៀត' : '';
  const banner = document.getElementById('save-banner');
  if (!banner) return;
  const waiting = pending.size > 0 && (state === 'bad' || offline);
  banner.hidden = !waiting;
  if (waiting) banner.textContent = offline
    ? `📴 គ្មានអ៊ីនធឺណិត — ចម្លើយ ${pending.size} មិនទាន់ទៅដល់ម៉ាស៊ីនមេ។ ចម្លើយរក្សាទុកលើទូរស័ព្ទហើយ សូមកុំបិទទំព័រ។ ចុចទីនេះដើម្បីព្យាយាមម្តងទៀត។`
    : `⚠ ចម្លើយ ${pending.size} មិនទាន់រក្សាទុកទៅម៉ាស៊ីនមេ — កំពុងព្យាយាមម្តងទៀត។ ចុចទីនេះដើម្បីព្យាយាមឥឡូវនេះ។`;
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
      if (testState.questions.find((x) => x.id === qid).selected_index === q.selected_index) { pending.delete(qid); writeLocal(); }
    } catch (e) {
      if (e.status === 423) { flushing = false; lockedNow = true; renderShield(); return; }   // locked: keep the unsent answers for after unlock
      if (e.status === 403 || e.status === 409) { pending.clear(); setSave('ok'); flushing = false; return; }   // exam over / other device
      failed = true; break;
    }
  }
  flushing = false;
  if (failed || pending.size) { setSave('bad'); retryTimer = setTimeout(flush, 4000); } else { setSave('ok'); writeLocal(); }
}
window.addEventListener('online', () => { if (pending.size) flush(); else if (testState) setSave('ok'); });
window.addEventListener('offline', () => { if (testState && !PREVIEW) setSave(pending.size ? 'bad' : 'ok'); });
window.addEventListener('beforeunload', (e) => { if (testState && !PREVIEW && pending.size) { e.preventDefault(); e.returnValue = ''; } });
for (const id of ['save-status', 'save-banner']) document.getElementById(id).addEventListener('click', () => { if (pending.size) flush(); });

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
      if (r.open && r.locked && !lockedNow) { lockedNow = true; renderShield(); }
      if (r.open && !r.locked && lockedNow) { lockedNow = false; return loadTest(testState.session_id); }   // the teacher unlocked: reload the questions
      if (!r.open) {
        clearInterval(heartbeatTimer); clearInterval(timerInterval);
        await Exam.notify(r.reason === 'device' ? 'ការប្រឡងនេះត្រូវបានបើកលើឧបករណ៍ផ្សេង (លោកគ្រូបានអនុញ្ញាតឱ្យប្តូរ)។ ឧបករណ៍នេះត្រូវបានបិទ។' : r.reason === 'submitted' ? 'ប្អូនបានប្រគល់ការប្រឡងនេះរួចហើយ។' : 'ការប្រឡងត្រូវបានបញ្ចប់។ ចម្លើយរបស់ប្អូនត្រូវបានរក្សាទុក។');
        testState = null; return boot();
      }
      if (r.end_at && r.end_at !== testState.end_at) testState.end_at = r.end_at;
    } catch {}
  }, 12000);
}

// ---------- Exam integrity: shield, warnings, lock ----------
let awayNow = false, needFs = false, lockedNow = false, fsBroken = false, shieldOn = false;
const integrityOn = () => !PREVIEW && testState && ((testState.integrity && testState.integrity.mode) || 'warn') !== 'log';

function renderShield() {
  const el = document.getElementById('shield');
  const on = !!testState && !views.test.hidden && (lockedNow || (integrityOn() && (awayNow || needFs)));
  if (on) {
    const icon = document.getElementById('shield-icon'), title = document.getElementById('shield-title'), text = document.getElementById('shield-text'), btn = document.getElementById('shield-btn');
    btn.hidden = true;
    if (lockedNow) {
      icon.textContent = '🔒'; title.textContent = 'ការប្រឡងត្រូវបានជាប់សោ';
      text.textContent = 'ប្រព័ន្ធបានកត់ត្រាសកម្មភាពមិនប្រក្រតី។ សូមលើកដៃហៅលោកគ្រូអ្នកគ្រូ — ចម្លើយដែលបានរក្សាទុកមិនបាត់ទេ។ ការប្រឡងនឹងបន្តដោយស្វ័យប្រវត្តិពេលលោកគ្រូដោះសោ។';
    } else if (awayNow) {
      icon.textContent = '⏸'; title.textContent = 'សូមត្រឡប់មកទំព័រប្រឡង';
      text.textContent = 'សំណួរត្រូវបានលាក់ពេលប្អូនចាកចេញពីទំព័រ។ ការចាកចេញត្រូវបានកត់ត្រាជូនលោកគ្រូអ្នកគ្រូ។';
    } else {
      icon.textContent = '⛶'; title.textContent = 'សូមបើកពេញអេក្រង់ដើម្បីបន្ត';
      text.textContent = 'ការប្រឡងនេះតម្រូវឱ្យប្រើពេញអេក្រង់។ ការចេញពីពេញអេក្រង់ត្រូវបានកត់ត្រា។';
      btn.hidden = false; btn.textContent = 'បើកពេញអេក្រង់';
      btn.onclick = async () => { if (!(await Integrity.goFullscreen())) fsBroken = true; needFs = false; renderShield(); };
    }
    document.getElementById('question-area').innerHTML = '';     // nothing for a page-reading tool to see
  }
  el.hidden = !on;
  const was = shieldOn;
  shieldOn = on;
  if (was && !on && testState && testState.questions.length) { renderQuestion(); renderNav(); }
}

function integrityChip(d) {
  const chip = document.getElementById('integrity-chip');
  if (!d || !integrityOn() || !d.violations) { chip.hidden = true; return; }
  chip.hidden = false;
  chip.textContent = d.mode === 'lock' ? `🚨 ${d.since_unlock}/${d.max}` : `🚨 ${d.violations}`;
  chip.title = 'សកម្មភាពមិនប្រក្រតីដែលបានកត់ត្រា';
}

const integrityHooks = {
  onAway: async (away, dur) => {
    awayNow = away && integrityOn();
    if (away) { if (testState && !PREVIEW) api('/api/student/left-page', { method: 'POST', body: { session_id: testState.session_id } }).catch(() => {}); renderShield(); return; }
    const d = await Integrity.flush();
    renderShield();
    if (integrityOn() && dur >= 2000 && !lockedNow) {
      const lim = d && d.mode === 'lock' ? ` (${d.since_unlock}/${d.max}) — ដល់ ${d.max} ការប្រឡងនឹងជាប់សោ` : '';
      Exam.notify(`⚠️ ប្អូនបានចាកចេញពីទំព័រប្រឡង ${Math.round(dur / 1000)} វិនាទី។ លោកគ្រូអ្នកគ្រូនឹងឃើញការកត់ត្រានេះ${lim}។ សូមកុំបើកកម្មវិធីផ្សេង កុំថតអេក្រង់ ឬប្រើ AI ពេលប្រឡង។`);
    }
  },
  onFullscreen: (on) => { needFs = !on && Integrity.fullscreenSupported() && !fsBroken; renderShield(); },
  onState: (d) => {
    integrityChip(d);
    if (d.locked && !lockedNow) { lockedNow = true; renderShield(); }
  },
};
function startIntegrity() {
  if (PREVIEW || !testState) return;
  Integrity.watermark(`${currentStudent.name} · ${currentStudent.id}`);
  Integrity.start(testState.session_id, testState.integrity, integrityHooks);
  needFs = integrityOn() && Integrity.fullscreenSupported() && !Integrity.isFullscreen() && !fsBroken;
  renderShield();
}
function stopIntegrity() {
  Integrity.stop(); Integrity.unwatermark();
  awayNow = needFs = lockedNow = false; shieldOn = false;
  document.getElementById('shield').hidden = true;
  document.getElementById('integrity-chip').hidden = true;
  try { if (document.fullscreenElement) document.exitFullscreen(); else if (document.webkitFullscreenElement) document.webkitExitFullscreen(); } catch {}
}

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
  let wNo = 0;
  testState.questions.forEach((q, i) => {
    const writing = q.kind === 'writing';
    if (writing) wNo++;
    if (!writing && q.selected_index != null) answered++;
    nav.append(h('button', {
      class: `${q.selected_index != null ? 'answered ' : ''}${writing ? 'writing ' : ''}${flags.has(q.id) ? 'flagged ' : ''}${i === testState.current ? 'current' : ''}`,
      title: writing ? 'សំណួរសរសេរ' : '',
      onclick: () => { testState.current = i; renderQuestion(); renderNav(); },
    }, writing ? `✎${wNo}` : String(i + 1 - (wNo)))); // numbering of multiple-choice questions skips written ones
  });
  const cur = nav.querySelector('.current');
  if (cur && nav.scrollWidth > nav.clientWidth + 2) nav.scrollLeft = cur.offsetLeft - (nav.clientWidth - cur.offsetWidth) / 2;
  document.getElementById('progress-fill').style.width = `${mcqTotal ? (answered / mcqTotal) * 100 : 0}%`;
}

const LETTERS = ['ក', 'ខ', 'គ', 'ឃ', 'ង', 'ច'];

function renderQuestion() {
  const area = document.getElementById('question-area');
  const q = testState.questions[testState.current];
  if (!q || lockedNow || shieldOn) return;
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
  const all = testState ? testState.questions : [];
  const mcqs = all.filter((q) => q.kind !== 'writing');
  const hasWriting = all.some((q) => q.kind === 'writing');
  const unansweredQs = mcqs.filter((q) => q.selected_index == null);
  const flaggedQs = mcqs.filter((q) => flags.has(q.id));
  const unanswered = unansweredQs.length;
  const total = mcqs.length;
  const answered = total - unanswered;

  const oldModal = document.getElementById('submit-modal');
  if (oldModal) oldModal.remove();

  const remainingMins = Math.max(0, Math.floor(remaining / 60000));
  const remainingSecs = Math.max(0, Math.floor((remaining % 60000) / 1000));
  const modal = h('div', { id: 'submit-modal', class: 'modal-back', style: 'align-items:flex-start;overflow:auto;' });
  // numbered buttons that jump back to the question
  const jump = (q) => h('button', { class: 'review-chip', onclick: () => { modal.remove(); testState.current = all.indexOf(q); renderQuestion(); renderNav(); } }, String(all.indexOf(q) + 1));
  const group = (title, cls, list) => list.length ? h('div', { class: `review-group ${cls}` }, [h('div', { class: 'review-title' }, `${title} (${list.length})`), h('div', { class: 'review-chips' }, list.map(jump))]) : null;

  const box = h('div', { class: 'modal-box', style: 'margin:auto;max-width:480px;' }, [
    h('div', { style: 'font-size:42px;margin-bottom:8px;' }, unanswered > 0 ? '⚠️' : '📝'),
    h('h2', { style: 'margin:0 0 10px;' }, 'ពិនិត្យមុនប្រគល់វិញ្ញាសា'),
    remaining > 60000 ? h('div', { class: 'callout warn' }, `⏱ ពេលវេលានៅសល់៖ ${remainingMins} នាទី ${remainingSecs} វិនាទី`) : null,
    h('div', { class: 'review-summary' }, [
      h('div', { class: 'review-stat good' }, [h('b', {}, String(answered)), ' បានឆ្លើយ']),
      h('div', { class: `review-stat ${unanswered ? 'bad' : ''}` }, [h('b', {}, String(unanswered)), ' មិនទាន់ឆ្លើយ']),
      h('div', { class: `review-stat ${flaggedQs.length ? 'warn' : ''}` }, [h('b', {}, String(flaggedQs.length)), ' បានចំណាំ 🚩']),
    ]),
    group('សំណួរមិនទាន់ឆ្លើយ — ចុចលេខដើម្បីត្រឡប់ទៅឆ្លើយ', 'bad', unansweredQs),
    group('សំណួរដែលបានចំណាំ', 'warn', flaggedQs),
    pending.size ? h('div', { class: 'callout bad' }, `⚠ ចម្លើយ ${pending.size} មិនទាន់រក្សាទុកទៅម៉ាស៊ីនមេ — ប្រព័ន្ធនឹងបញ្ជូនជាមួយការប្រគល់។`) : null,
    unanswered === 0 && !flaggedQs.length ? h('div', { class: 'callout good' }, `✓ ប្អូនបានឆ្លើយគ្រប់ទាំង ${total} សំណួរហើយ!`) : null,
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
  if (PREVIEW) { clearInterval(timerInterval); await Exam.notify('នេះគ្រាន់តែជាការមើលសាកល្បង — គ្មានអ្វីត្រូវបានបញ្ជូនទេ។'); location.href = 'student.html'; return; }
  clearInterval(timerInterval);
  clearInterval(heartbeatTimer);
  const sessionId = testState && testState.session_id;
  // give pending saves a few seconds, then send everything we know in the submit itself
  if (pending.size) await Promise.race([flush(), new Promise((r) => setTimeout(r, 6000))]);
  const answers = {};
  for (const q of testState.questions) if (q.kind !== 'writing' && q.selected_index != null) answers[q.id] = q.selected_index;
  const send = () => api('/api/student/submit', { method: 'POST', body: { session_id: sessionId, submit_type: auto ? 'auto' : 'manual', answers } });
  const refused = (e) => e.status && e.status < 500 && e.status !== 429 && e.status !== 401;
  let done = false;
  const giveUpAt = Date.now() + (auto ? 45000 : 25000);
  for (let attempt = 0; !done; attempt++) {
    try { await send(); done = true; }
    catch (e) {
      if (refused(e)) { if (!auto) await Exam.notify(e.message); break; }               // refused (e.g. already submitted)
      if (Date.now() > giveUpAt) break;
      await new Promise((r) => setTimeout(r, Math.min(1500 * (attempt + 1), 5000)));    // network trouble: try again
    }
  }
  if (!done) {
    // Never throw the answers away: they stay on the phone, and the teacher can reopen the exam for this student.
    await Exam.notify(auto
      ? '⚠ ពេលវេលាអស់ ប៉ុន្តែបញ្ជូនចម្លើយមិនបានទេ (គ្មានអ៊ីនធឺណិត)។ ចម្លើយរបស់ប្អូននៅលើទូរស័ព្ទនៅឡើយ។ សូមប្រាប់លោកគ្រូអ្នកគ្រូភ្លាមៗ ហើយកុំបិទទំព័រ ឬលុបទិន្នន័យទូរស័ព្ទ។'
      : 'មិនអាចបញ្ជូនបានទេ — សូមពិនិត្យអ៊ីនធឺណិត ហើយចុចបញ្ជូនម្តងទៀត។ ចម្លើយរបស់ប្អូនត្រូវបានរក្សាទុកលើទូរស័ព្ទ។');
    if (!auto) { startTimer(); startHeartbeat(); return; }
    const banner = document.getElementById('save-banner');
    banner.hidden = false; banner.textContent = '⏳ កំពុងរង់ចាំអ៊ីនធឺណិតដើម្បីបញ្ជូនចម្លើយ — កុំបិទទំព័រ។ ប្រាប់លោកគ្រូអ្នកគ្រូ។';
    const retry = setInterval(async () => {
      try { await send(); clearInterval(retry); banner.hidden = true; try { for (const k of ['ans', 'flags', 'pend']) localStorage.removeItem(localKey(k)); } catch {} testState = null; boot(); }
      catch (e) { if (refused(e)) { clearInterval(retry); banner.textContent = '⚠ ម៉ាស៊ីនមេមិនទទួលចម្លើយទៀតទេ — សូមប្រាប់លោកគ្រូអ្នកគ្រូឱ្យបន្ថែមពេលឱ្យប្អូន។ ចម្លើយនៅលើទូរស័ព្ទ។'; } }
    }, 8000);
    return;
  }
  try { for (const k of ['ans', 'flags', 'pend']) localStorage.removeItem(localKey(k)); } catch {}
  testState = null;
  boot();
}

boot();
