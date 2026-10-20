const { h, api, showError, fmtDateTime, fmtTimeOnly } = Exam;

// An element whose content is rendered through the math-typing engine
// (js/mathtype.js) — plain Khmer text passes through unchanged, \( \)/\[ \]
// is treated as literal LaTeX, and other math-looking runs (x^2, 3/4, √20…)
// are converted automatically.
function mathEl(tag, attrs, text) {
  const el = h(tag, attrs);
  el.innerHTML = Exam.mathHtml(text);
  return el;
}

const viewSetup = document.getElementById('view-setup');
const viewLogin = document.getElementById('view-login');
const viewDashboard = document.getElementById('view-dashboard');

let ME = null;
const roleLabel = (r) => (r === 'sample' ? 'តេស្តគំរូ' : r === 'owner' ? 'ម្ចាស់ប្រព័ន្ធ' : r === 'editor' ? 'អ្នកកែសម្រួល' : r === 'reviewer' ? 'អ្នកពិនិត្យ' : 'គ្រូ');

async function boot() {
  try {
    const { needs_setup } = await api('/api/teacher/setup-status');
    if (needs_setup) { viewSetup.hidden = false; return; }
    ME = await api('/api/teacher/me');
    viewDashboard.hidden = false;
    initDashboard();
    if (new URLSearchParams(location.search).has('share')) openTestInvitation();
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
  } catch (e) { showError(viewSetup.querySelector('.auth-card'), e.message); }
});

document.getElementById('login-username').addEventListener('keydown', (e) => { if (e.key === 'Enter') document.getElementById('login-password').focus(); });
document.getElementById('login-password').addEventListener('keydown', (e) => { if (e.key === 'Enter') document.getElementById('login-submit').click(); });
document.getElementById('login-submit').addEventListener('click', async () => {
  const btn = document.getElementById('login-submit');
  btn.disabled = true;
  const origText = btn.textContent;
  btn.textContent = 'កំពុងចូល...';
  try {
    await api('/api/teacher/login', { method: 'POST', body: {
      username: document.getElementById('login-username').value.trim(),
      password: document.getElementById('login-password').value,
    } });
    location.reload();
  } catch (e) {
    btn.disabled = false;
    btn.textContent = origText;
    showError(viewLogin.querySelector('.auth-card'), e.message);
  }
});

document.getElementById('logout-btn').addEventListener('click', async () => {
  await api('/api/teacher/logout', { method: 'POST' });
  location.reload();
});

// ---------- licence: lock bar + lock screens ----------
function codeBox(onDone) {
  const input = h('input', { type: 'text', placeholder: 'XXXX-XXXX-XXXX', class: 'code-input', maxlength: '20', autocomplete: 'off' });
  const go = async () => {
    if (!input.value.trim()) return input.focus();
    try {
      await api('/api/license/redeem', { method: 'POST', body: { code: input.value } });
      await Exam.notify('🎉 ដោះសោជោគជ័យ! អ្នកអាចប្រើមុខងារទាំងអស់បានហើយ។');
      location.reload();
    } catch (e) { Exam.notify(e.message); }
  };
  input.addEventListener('keydown', (e) => { if (e.key === 'Enter') go(); });
  return h('div', { class: 'code-row' }, [input, h('button', { onclick: go }, '🔓 ដោះសោ')]);
}

// The teacher picks a plan, leaves a contact, and the owner is told on Telegram; payment + the unlock code go through the owner.
const tgLink = () => h('a', { href: `https://t.me/${ME.telegram}`, target: '_blank', rel: 'noopener', class: 'tg-link' }, `💬 Telegram @${ME.telegram}`);

function requestDialog(key) {
  const P = ME.plans[key];
  document.querySelectorAll('.up-dialog').forEach((d) => d.remove());
  const contact = h('input', { type: 'text', placeholder: 'លេខទូរស័ព្ទ ឬ Telegram របស់អ្នក', value: ME.contact || '', style: 'width:100%;' });
  const msg = h('div', { class: 'muted', style: 'margin-top:10px;' });
  const send = h('button', { onclick: async () => {
    if (!contact.value.trim()) { contact.focus(); return; }
    send.disabled = true;
    try {
      await api('/api/license/request', { method: 'POST', body: { plan: key, contact: contact.value } });
      msg.textContent = '✅ បានផ្ញើសំណើហើយ! ម្ចាស់ប្រព័ន្ធ (@' + ME.telegram + ') នឹងឃើញសំណើរបស់អ្នកភ្លាមៗ ហើយទាក់ទងអ្នក ប្រាប់របៀបបង់ប្រាក់ ហើយផ្ញើកូដដោះសោឱ្យ។ បន្ទាប់មកបញ្ចូលកូដក្នុងប្រអប់ខាងក្រោម។';
    } catch (e) { msg.textContent = e.message; send.disabled = false; }
  } }, '🔓 ស្នើសុំដោះសោ');
  const box = h('div', { class: 'up-dialog' }, [
    h('h3', { style: 'margin:0 0 6px;' }, `គម្រោង ${P.label} — $${P.price}${P.was ? ` (ធម្មតា $${P.was})` : ''}`),
    h('p', { class: 'muted', style: 'margin:0 0 10px;' }, 'បញ្ចូលរបៀបទាក់ទងអ្នក រួចចុច «ស្នើសុំដោះសោ»។ ម្ចាស់ប្រព័ន្ធនឹងប្រាប់របៀបបង់ប្រាក់ ហើយផ្ញើកូដមកអ្នក។'),
    h('p', { style: 'margin:0 0 10px;' }, ['ឬទាក់ទងផ្ទាល់៖ ', tgLink(), ME.contact_text ? ` · ${ME.contact_text}` : '']),
    contact, h('div', { class: 'row', style: 'gap:8px;margin-top:10px;' }, [send, h('button', { class: 'ghost', onclick: () => box.remove() }, 'បិទ')]), msg,
  ]);
  document.querySelector('.up-plans').after(box);
  box.scrollIntoView({ behavior: 'smooth', block: 'center' });
  contact.focus();
}

function pricingCards(trial) {
  const M = ME.plans.month, Y = ME.plans.year, L = ME.trial_limits || {};
  const card = (cls, inner) => h('div', { class: `pc ${cls}` }, inner);
  const li = (t, no) => h('li', { class: no ? 'no' : '' }, t);
  const row = [];
  row.push(card('', [
    h('div', { class: 'name' }, `${M.label}`),
    h('div', { class: 'price' }, [`$${M.price}`]),
    h('div', { class: 'per' }, 'សាកល្បងមួយខែ'),
    h('ul', {}, [li('ថ្នាក់ សិស្ស តេស្ត ប្រឡង មិនកំណត់'), li('ហ្គេមសំណួរផ្ទាល់ពេញលេញ'), li('ពិន្ទុប្រចាំឆ្នាំ & របាយការណ៍'), li('ចែករំលែកតេស្តជាមួយគ្រូ')]),
    h('button', { class: 'btn-pc', onclick: () => requestDialog('month') }, 'ជ្រើស ១ ខែ'),
  ]));
  row.push(card('best', [
    h('div', { class: 'ribbon' }, `🔥 សន្សំ ${Math.round((1 - Y.price / Y.was) * 100)}% · ពេញនិយមបំផុត`),
    h('div', { class: 'name' }, `${Y.label}`),
    h('div', { class: 'price' }, [h('span', { class: 'was' }, `$${Y.was}`), `$${Y.price}`]),
    h('div', { class: 'per' }, `ស្មើត្រឹម $${(Y.price / 12).toFixed(2)} ក្នុងមួយខែ`),
    h('ul', {}, [li('មុខងារទាំងអស់ គ្មានកំណត់'), li('ប្រើពេញមួយឆ្នាំសិក្សា'), li('ការគាំទ្រពីម្ចាស់ប្រព័ន្ធ'), li(`តម្លៃបញ្ចុះពិសេស — សន្សំ $${Y.was - Y.price}`)]),
    h('button', { class: 'btn-pc', onclick: () => requestDialog('year') }, '⭐ ជ្រើស ១ ឆ្នាំ — $' + Y.price),
  ]));
  return h('div', { class: 'pc-row' }, row);
}

function licenseBar() {
  const trial = ME.status === 'trial';
  const until = ME.license_until ? fmtDateTime(ME.license_until) : '';
  const L = ME.trial_limits || {}, U = ME.usage || {};
  const use = (label, used, max) => h('span', { class: `u${used >= max ? ' full' : ''}` }, `${label} ${used}/${max}${used >= max ? ' · ពេញ' : ''}`);
  let card;
  const toggle = () => { card.classList.toggle('open'); toggleBtn.setAttribute('aria-expanded', String(card.classList.contains('open'))); if (card.classList.contains('open')) card.scrollIntoView({ behavior: 'smooth', block: 'start' }); };
  const toggleBtn = h('button', { class: 'up-toggle', type: 'button', 'aria-expanded': 'false', onclick: toggle }, trial ? '⬆ ដំឡើងគណនី' : '⬆ បន្តការប្រើប្រាស់');
  card = h('div', { class: 'up-card' }, [
    h('div', { class: 'up-top' }, [
      h('span', { class: 'up-tag' }, trial ? '🆓 គណនីសាកល្បង' : '🔒 ផុតកំណត់'),
      trial ? h('div', { class: 'up-use' }, [use('ថ្នាក់', U.classes || 0, L.classes), use('សិស្ស', U.students || 0, L.students), use('តេស្ត', U.tests || 0, L.tests), use('ប្រឡង', U.sessions || 0, L.sessions), h('span', { class: 'u' }, `សំណួរ ≤ ${L.questions}/តេស្ត`)])
        : h('div', { class: 'up-note' }, `(${until}) — មើលទិន្នន័យបាន តែមិនអាចកែប្រែបានទេ។`),
      toggleBtn,
    ]),
    h('div', { class: 'up-more' }, [
      h('div', { class: 'up-head' }, [
        h('h2', {}, trial ? 'បើកមុខងារពេញលេញ — គ្មានកំណត់' : 'ការប្រើប្រាស់បានផុតកំណត់'),
        h('p', {}, trial ? 'ឡើងគម្រោងដើម្បីបង្រៀន និងប្រឡងគ្រប់ថ្នាក់របស់អ្នក ដោយគ្មានដែនកំណត់។' : 'បន្តដើម្បីប្រើបានពេញលេញ។'),
      ]),
      h('div', { class: 'up-perks' }, ['ថ្នាក់ និងសិស្សមិនកំណត់', 'តេស្ត និងសំណួរមិនកំណត់', 'ប្រឡងគ្រប់ថ្នាក់ ដាក់ពិន្ទុស្វ័យប្រវត្តិ', 'ពិន្ទុប្រចាំឆ្នាំ ស្ថិតិ A–F', 'ហ្គេមសំណួរផ្ទាល់ពេញលេញ', 'ចែករំលែក និងចម្លងតេស្ត'].map((t) => h('div', {}, t))),
      h('div', { class: 'up-plans' }, [pricingCards(trial)]),
      h('div', { class: 'up-foot' }, [
        h('div', {}, ['សួរ ឬបង់ប្រាក់៖ ', tgLink(), ME.contact_text ? ` · ${ME.contact_text}` : '']),
        h('div', { style: 'margin-top:8px;' }, 'មានកូដដោះសោរួចហើយ?'),
        codeBox(),
      ]),
    ]),
  ]);
  window.openUpgrade = () => { if (!card.classList.contains('open')) toggle(); };
  return card;
}

const LOCK_INFO = {
  classes: ['ថ្នាក់ និងសិស្ស', 'បង្កើតថ្នាក់ បញ្ចូលបញ្ជីសិស្សពី Excel និងគ្រប់គ្រងសិស្ស។'],
  schedule: ['កំណត់ពេលប្រឡង', 'កំណត់ម៉ោង PIN និងរៀបចំប្រឡងឱ្យថ្នាក់ម្នាក់ៗនៅម៉ោងខុសគ្នា។'],
  grading: ['ដាក់ពិន្ទុ & លទ្ធផល', 'មើលលទ្ធផលផ្ទាល់ ដាក់ពិន្ទុសរសេរ ផ្សព្វផ្សាយ និងវិភាគសំណួរ។'],
  year: ['ពិន្ទុប្រចាំឆ្នាំ', 'ពិន្ទុបុរេតេស្ត ប្រចាំខែ ឆមាស និងស្ថិតិ A-F តាមភេទ។'],
  overview: ['សង្ខេបគ្រប់ថ្នាក់', 'ប្រៀបធៀបលទ្ធផលថ្នាក់ផ្សេងៗ។'],
  bank: ['ធនាគារសំណួរ', 'ប្រើសំណួរឡើងវិញ និងបង្កើតតេស្តដោយចៃដន្យតាមកម្រិត និងប្រធានបទ។'],
};
function showLocked(tab) {
  const [title, desc] = LOCK_INFO[tab] || ['', ''];
  const box = document.getElementById(`tab-${tab}`);
  box.innerHTML = '';
  box.append(h('div', { class: 'lock-card' }, [
    h('div', { class: 'lock-icon' }, '🔒'),
    h('h2', {}, title),
    h('p', { class: 'muted' }, desc),
    h('p', {}, `🔓 មុខងារនេះសម្រាប់គណនីពេញលេញ — ១ ឆ្នាំត្រឹម $${ME.plans.year.price} (ធម្មតា $${ME.plans.year.was}) ឬ ១ ខែ $${ME.plans.month.price}។`),
    h('button', { class: 'su-cta', style: 'max-width:320px;margin:0 auto 12px;display:block;', onclick: () => { document.querySelector('[data-tab=classes]').click(); if (window.openUpgrade) window.openUpgrade(); window.scrollTo({ top: 0, behavior: 'smooth' }); } }, '⭐ មើលគម្រោង និងឡើងគម្រោង'),
    h('p', {}, 'មានកូដដោះសោរួចហើយ? បញ្ចូលទីនេះ៖'),
    codeBox(),
    h('p', { class: 'muted', style: 'margin-top:12px;' }, ['ស្នើសុំកូដ៖ ', tgLink()]),
  ]));
}

// ---------- question variants (different numbers per student) ----------
function variantsBlock(getFields, initial = '') {
  const params = h('textarea', { placeholder: 'ឧ.\na = 2..9\nb = 3..9', style: 'min-height:70px;font-family:monospace;' });
  params.value = initial || '';
  const out = h('div', {});
  const box = h('details', { style: 'margin-top:10px;' }, [
    h('summary', { style: 'cursor:pointer;font-weight:600;' }, '🎲 លេខខុសគ្នាសម្រាប់សិស្សម្នាក់ៗ (មិនចាំបាច់)'),
    h('p', { class: 'muted', style: 'margin:6px 0;' }, 'សរសេរ [[a]] ក្នុងអត្ថបទ ឬជម្រើស ហើយកំណត់អថេរខាងក្រោម (a = 2..9 ឬ c = {2,4,5} ឬ d = a + b)។ ជម្រើសអាចជាកន្សោម ឧ. [[a+b]]។ ជម្រើសទី១ ដែលជាចម្លើយត្រឹមត្រូវ ត្រូវតែគណនាតាមអថេរ។'),
    params,
    h('button', { type: 'button', class: 'secondary btn-sm', style: 'margin-top:6px;', onclick: async () => {
      out.innerHTML = '';
      try {
        const f = getFields();
        const r = await api('/api/variants/preview', { method: 'POST', body: { params: params.value, stem_text: f.stem_text, options: f.options, solution_text: f.solution_text, n: 3 } });
        r.samples.forEach((sm, i) => out.append(h('div', { class: 'callout' }, [h('b', {}, `ឧទាហរណ៍ ${i + 1}៖ `), mathEl('span', {}, sm.stem_text), h('div', {}, sm.options.map((o, j) => mathEl('span', { style: 'margin-right:14px;' }, `${['ក', 'ខ', 'គ', 'ឃ', 'ង', 'ច'][j]}. ${o}`)))])));
      } catch (e) { out.append(h('div', { class: 'error' }, e.message)); }
    } }, '👁 មើលឧទាហរណ៍'),
    out,
  ]);
  if (initial) box.open = true;
  return { box, params };
}

// ---------- exam readiness checklist ----------
function showReadiness(rd, { confirmLabel = 'ดำเนินការต่อ', viewOnly = false } = {}) {
  return new Promise((resolve) => {
    const icon = { ok: '✓', warn: '⚠', error: '✗' };
    const done = (v) => { back.remove(); resolve(v); };
    const rows = rd.checks.map((c) => h('div', { class: `ready-row ${c.level === 'ok' ? 'ok' : c.level === 'warn' ? 'warn' : 'bad'}`, style: 'align-items:flex-start;' }, [
      h('span', {}, icon[c.level]), h('div', {}, [h('div', {}, c.title), c.detail ? h('div', { style: 'font-weight:400;font-size:13px;' }, c.detail) : null]),
    ]));
    const verdict = rd.errors ? h('div', { class: 'callout bad' }, `✗ មិនទាន់រួចរាល់ — មានបញ្ហាត្រូវដោះស្រាយ ${rd.errors}`)
      : rd.warnings ? h('div', { class: 'callout warn' }, `⚠ អាចបន្តបាន តែមានចំណុចគួរពិនិត្យ ${rd.warnings}`)
      : h('div', { class: 'callout good' }, '✓ រួចរាល់ទាំងអស់');
    const back = h('div', { class: 'modal-back', style: 'align-items:flex-start;overflow:auto;' }, h('div', { class: 'modal-box', style: 'margin:20px auto;max-width:560px;text-align:left;' }, [
      h('h2', { style: 'margin:0 0 10px;' }, '📋 បញ្ជីពិនិត្យមុនបើកប្រឡង'),
      verdict, h('div', { class: 'ready-checks' }, rows),
      h('div', { class: 'row', style: 'justify-content:flex-end;margin-top:14px;' }, [
        h('button', { class: 'secondary', onclick: () => done(false) }, viewOnly || rd.errors ? 'បិទ' : 'ត្រឡប់ទៅកែ'),
        !viewOnly && !rd.errors ? h('button', { onclick: () => done(true) }, confirmLabel) : null,
      ]),
    ]));
    document.body.append(back);
  });
}

async function downloadBackup() {
  if (typeof XLSX === 'undefined') return Exam.notify('មិនទាន់ដំណើរការបណ្ណាល័យ Excel នៅឡើយទេ។');
  const d = await api('/api/export');
  const wb = XLSX.utils.book_new();
  const sheet = (name, rows) => XLSX.utils.book_append_sheet(wb, XLSX.utils.json_to_sheet(rows.length ? rows : [{ '': '' }]), name);
  const cname = Object.fromEntries(d.classes.map((c) => [c.id, c.name]));
  sheet('Classes', d.classes);
  sheet('Students', d.students.map((s) => ({ class: cname[s.class_id], ...s })));
  sheet('Sessions', d.sessions);
  const sname = Object.fromEntries(d.students.map((s) => [s.id, `${s.surname} ${s.first_name}`]));
  const sess = Object.fromEntries(d.sessions.map((s) => [s.id, `${s.test_title} — ${s.class_name}`]));
  sheet('Results', d.results.map((r) => ({ exam: sess[r.session_id], student: sname[r.student_id], ...r })));
  sheet('Year scores (typed)', d.manual_scores.map((m) => ({ assessment: (d.assessments.find((a) => a.id === m.assessment_id) || {}).title, student: sname[m.student_id], ...m })));
  sheet('Tests', d.tests);
  sheet('Questions', d.questions);
  XLSX.writeFile(wb, `បម្រុងទុក_${new Date().toISOString().slice(0, 10)}.xlsx`);
}

function initDashboard() {
  const bk = document.getElementById('backup-btn');
  if (bk) bk.onclick = () => downloadBackup().catch((e) => Exam.notify(e.message));
  if (ME.status === 'trial') for (const k of ['year', 'overview']) render[k] = () => showLocked(k);   // everything else works, within the free-trial limits
  if (ME.status === 'trial' || ME.status === 'expired') {
    const dash = document.getElementById('view-dashboard');
    dash.insertBefore(licenseBar(), dash.querySelector('.tabs'));
  }
  const badge = document.getElementById('teacher-username-badge');
  if (badge) badge.textContent = `${ME.display_name} · ${ME.role === 'owner' ? 'ម្ចាស់ប្រព័ន្ធ' : ME.status === 'trial' ? 'សាកល្បង 🔒' : ME.status === 'expired' ? 'ផុតកំណត់ ⏰' : `គ្រូ${ME.license_until ? ` · ដល់ ${fmtDateTime(ME.license_until).split(',')[0]}` : ''}`}`;
  if (ME.role !== 'owner') { const tb = document.querySelector('[data-tab="teachers"]'); if (tb) tb.hidden = true; }
  else startRequestBadge();
  const tabs = document.querySelectorAll('.tabs button');
  tabs.forEach((btn) => btn.addEventListener('click', () => {
    tabs.forEach((b) => b.classList.toggle('active', b === btn));
    document.querySelectorAll('[id^="tab-"]').forEach((el) => { el.hidden = el.id !== `tab-${btn.dataset.tab}`; });
    render[btn.dataset.tab]();
  }));
  render.classes();
  initTeachMode();
}

const render = {};

// ---------- Classes & students ----------
let selectedClassId = null;

async function renderPinCard() {
  const { has_pin } = await api('/api/settings/pin');
  return h('div', { class: 'card' }, [
    h('h3', {}, 'កូដសម្ងាត់សិស្ស (PIN)'),
    h('p', { class: 'muted' }, 'សិស្សគ្រប់គ្នាប្រើ PIN តែមួយរួមគ្នានេះ (បូកនឹងលេខសម្គាល់ផ្ទាល់ខ្លួន) ដើម្បីចូលធ្វើតេស្ត។ លោកគ្រូជាអ្នកកំណត់ និងអាចផ្លាស់ប្តូរបានគ្រប់ពេល។'),
    h('p', {}, has_pin ? h('span', { class: 'badge ready' }, 'បានកំណត់ PIN ហើយ') : h('span', { class: 'badge draft' }, 'មិនទាន់កំណត់ PIN ទេ')),
    h('div', { class: 'row' }, [
      h('input', { type: 'text', id: 'shared-pin', placeholder: 'ឧ. 2025', inputmode: 'numeric', style: 'flex:1' }),
      h('button', { onclick: async () => {
        const pin = document.getElementById('shared-pin').value.trim();
        try {
          await api('/api/settings/pin', { method: 'POST', body: { pin } });
          await Exam.notify('បានកំណត់ PIN ថ្មីរួចរាល់។ សូមប្រាប់សិស្សទាំងអស់ពី PIN នេះ។');
          render.classes();
        } catch (e) { await Exam.notify(e.message); }
      } }, 'កំណត់ PIN'),
    ]),
  ]);
}

render.classes = async function () {
  const container = document.getElementById('tab-classes');
  container.innerHTML = '';
  if (selectedClassId) return renderRoster(container);


  const { classes } = await api('/api/classes');
  const card = h('div', { class: 'card' }, [
    h('h2', {}, 'ថ្នាក់'),
    ...classes.map((c) => h('div', { class: 'list-item' }, [
      h('div', {}, [h('strong', {}, c.name), h('span', { class: 'muted' }, ` — ថ្នាក់ទី ${c.grade} — សិស្ស ${c.student_count} នាក់`),
        c.owner_id !== ME.id ? h('span', { class: `badge ${c.my_role === 'reviewer' ? 'draft' : 'upcoming'}`, style: 'margin-left:6px;' }, `${c.my_role === 'owner' ? 'ម្ចាស់ប្រព័ន្ធ' : roleLabel(c.my_role)} · ${c.owner_name || ''}`) : null]),
      h('div', { class: 'row', style: 'gap:6px;' }, [
        h('button', { class: 'secondary btn-sm', onclick: () => { selectedClassId = c.id; render.classes(); } }, 'មើលបញ្ជីសិស្ស'),
        c.my_role === 'owner' ? h('button', { class: 'secondary btn-sm', onclick: () => openShareDialog('class', c.id, `ថ្នាក់ ${c.name}`) }, '👥 ចែករំលែក') : null,
        c.my_role !== 'owner' ? null : h('button', { class: 'danger btn-sm', onclick: async () => {
          if (!confirm(`តើលោកគ្រូពិតជាចង់លុបថ្នាក់ «${c.name}» និងទិន្នន័យសិស្សទាំងអស់ក្នុងថ្នាក់នេះឬ?`)) return;
          try {
            await api(`/api/classes/${c.id}`, { method: 'DELETE' });
            render.classes();
          } catch (e) { Exam.notify(e.message); }
        } }, 'លុបថ្នាក់'),
      ]),
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

let teachClassId = null;
const teachKh = (n) => String(n ?? '').replace(/\d/g, (d) => '០១២៣៤៥៦៧៨៩'[d]);
const teachOn = () => localStorage.getItem('exam_teach_mode') === '1';

let teachBusy = false;

function playMagic(name) {
  const el = document.getElementById('dashboard-content');
  if (!el || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return Promise.resolve();
  return new Promise((resolve) => {
    let done = false;
    const finish = () => {
      if (done) return;
      done = true;
      el.classList.remove('magictime', 'vanishIn', 'vanishOut');
      el.removeEventListener('animationend', finish);
      resolve();
    };
    el.classList.remove('magictime', 'vanishIn', 'vanishOut');
    void el.offsetWidth;
    el.classList.add('magictime', name);
    el.addEventListener('animationend', finish);
    setTimeout(finish, 1000);
  });
}

function commitTeachMode(on) {
  localStorage.setItem('exam_teach_mode', on ? '1' : '0');
  document.body.classList.toggle('teach-mode', on);
  document.body.classList.remove('teach-tool');
  const btn = document.getElementById('teach-mode-btn');
  if (btn) {
    btn.classList.toggle('on', on);
    btn.setAttribute('aria-pressed', String(on));
  }
  const back = document.getElementById('teach-back');
  if (back) back.hidden = true;
  const title = document.getElementById('workspace-title');
  if (on) {
    if (title) title.textContent = 'ម៉ូដបង្រៀន';
    document.querySelectorAll('[id^="tab-"]').forEach((el) => { el.hidden = el.id !== 'tab-teach'; });
    render.teach();
  } else {
    const cls = document.querySelector('[data-tab="classes"]');
    if (cls) cls.click();
  }
}

async function applyTeachMode(on, animate = true) {
  if (teachBusy) return;
  if (on === teachOn() && document.body.classList.contains('teach-mode') === on) return;
  teachBusy = true;
  if (animate) await playMagic('vanishOut');
  commitTeachMode(on);
  if (animate) await playMagic('vanishIn');
  teachBusy = false;
}

function openTeachTool(tab) {
  document.body.classList.add('teach-tool');
  const back = document.getElementById('teach-back');
  if (back) back.hidden = false;
  if (typeof wheelClassId !== 'undefined') wheelClassId = teachClassId;
  if (typeof tgClassId !== 'undefined') tgClassId = teachClassId;
  const b = document.querySelector(`[data-tab="${tab}"]`);
  if (b) b.click();
}

async function teachLaunchGame(style) {
  if (!teachClassId) return Exam.notify('សូមជ្រើសថ្នាក់ជាមុនសិន។');
  try {
    const { classes } = await api('/api/classes');
    const cls = classes.find((c) => c.id === teachClassId) || classes[0];
    const { students } = await api(`/api/classes/${teachClassId}/students`);
    const names = students.map((s) => `${s.surname || ''} ${s.first_name || ''}`.trim()).filter(Boolean);
    if (!names.length) return Exam.notify('ថ្នាក់នេះមិនទាន់មានសិស្សទេ។');
    const n = Math.min(4, Math.max(2, names.length));
    const teams = Array.from({ length: n }, () => []);
    const sh = names.slice();
    for (let i = sh.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [sh[i], sh[j]] = [sh[j], sh[i]];
    }
    sh.forEach((nm, i) => teams[i % n].push(nm));
    try { localStorage.setItem('km_wheel_last_groups', JSON.stringify({ cls: cls.name, groups: teams })); } catch {}
    const g = parseInt(cls.grade, 10) || 7;
    location.href = `teamgame.html?import=1&style=${style}&grade=${g}`;
  } catch (e) { Exam.notify(e.message); }
}

render.teach = async function () {
  const root = document.getElementById('tab-teach');
  if (!root) return;
  root.innerHTML = '';
  const tb = document.getElementById('teach-back');
  if (tb && !document.body.classList.contains('teach-tool')) tb.hidden = true;
  let classes = [];
  try { classes = (await api('/api/classes')).classes || []; } catch (e) {
    return root.append(h('div', { class: 'error' }, e.message));
  }
  if (teachClassId == null || !classes.some((c) => c.id === teachClassId)) teachClassId = classes[0] ? classes[0].id : null;

  const home = h('div', { class: 'teach-home' });
  root.append(home);

  if (!classes.length) {
    home.append(h('div', { class: 'teach-empty' }, [
      h('span', { class: 'teach-empty-ic' }, '🏫'),
      h('b', {}, 'មិនទាន់មានថ្នាក់ទេ'),
      h('p', {}, 'បិទម៉ូដបង្រៀនដើម្បីបង្កើតថ្នាក់។'),
    ]));
    return;
  }

  const sel = classes.find((c) => c.id === teachClassId) || classes[0];
  const pickClass = (c) => {
    teachClassId = c.id;
    home.querySelectorAll('.teach-class').forEach((el) => el.classList.toggle('on', el.dataset.id === String(c.id)));
    const name = document.getElementById('teach-now-name');
    if (name) name.textContent = c.name;
    const mark = document.getElementById('teach-now-mark');
    if (mark) mark.textContent = teachKh(c.grade);
    if (window.TeachRoom) window.TeachRoom.mount(c);
  };
  home.append(h('div', { class: 'teach-hero' }, [
    h('div', { class: 'teach-hero-copy' }, [
      h('p', { class: 'teach-kicker' }, 'កំពុងបង្រៀន'),
      h('h2', { id: 'teach-now-name' }, sel.name),
      h('p', { class: 'teach-hero-meta', id: 'teach-now-meta' }, `ថ្នាក់ទី ${teachKh(sel.grade)} · សិស្ស ${teachKh(sel.student_count)} នាក់`),
    ]),
    h('div', { class: 'teach-hero-mark', id: 'teach-now-mark', 'aria-hidden': 'true' }, teachKh(sel.grade)),
  ]));

  home.append(h('div', { class: 'teach-rail' }, classes.map((c) => h('button', {
    type: 'button',
    class: `teach-class${c.id === teachClassId ? ' on' : ''}`,
    'data-id': c.id,
    onclick: () => pickClass(c),
  }, [
    h('span', { class: 'teach-grade' }, `ទី ${teachKh(c.grade)}`),
    h('b', {}, c.name),
    h('span', { class: 'teach-count' }, `${teachKh(c.student_count)} សិស្ស`),
  ]))));

  const work = h('div', { id: 'teach-work', class: 'teach-desk' });
  home.append(work);
  if (window.TeachRoom) window.TeachRoom.mount(sel, work);

  const tools = [
    { k: 'spin', ic: '🎡', t: 'កង់ចាប់ឈ្មោះ', d: 'ចាប់ឈ្មោះសិស្សក្នុងថ្នាក់', go: () => openTeachTool('wheel') },
    { k: 'cards', ic: '🃏', t: 'កាតបើក', d: 'ហ្គេមសំណួរជាក្រុម', go: () => teachLaunchGame('cards') },
    { k: 'qwheel', ic: '🎲', t: 'កង់វិលសំណួរ', d: 'បង្វិលកង់ជ្រើសសំណួរ', go: () => teachLaunchGame('wheel') },
    { k: 'boat', ic: '🚣', t: 'ប្រណាំងទូកង', d: 'ឆ្លើយត្រូវ ទូកទៅមុខ', go: () => teachLaunchGame('boat') },
    { k: 'live', ic: '📱', t: 'សំណួរផ្ទាល់', d: 'សិស្សឆ្លើយលើទូរស័ព្ទ', go: () => openTeachTool('live') },
    { k: 'bingo', ic: '🎯', t: 'ប៊ីងហ្គោ', d: 'បោះពុម្ពកាតចម្លើយ', go: () => { location.href = 'bingo.html'; } },
  ];
  home.append(
    h('div', { class: 'teach-sec' }, [h('h2', { class: 'teach-h' }, 'សម្ភារបង្រៀន')]),
    h('div', { class: 'teach-tools' }, tools.map((x, i) => h('button', {
      type: 'button',
      class: `teach-tile t-${x.k}`,
      style: `--i:${i}`,
      onclick: x.go,
    }, [
      h('span', { class: 'teach-ic', 'aria-hidden': 'true' }, x.ic),
      h('b', {}, x.t),
      h('span', { class: 'teach-tile-d' }, x.d),
    ]))),
  );
};

function initTeachMode() {
  const btn = document.getElementById('teach-mode-btn');
  const back = document.getElementById('teach-back');
  if (btn) btn.addEventListener('click', () => applyTeachMode(!teachOn(), true));
  if (back) back.addEventListener('click', () => {
    if (window.TeachShow && window.TeachShow.isOpen()) { window.TeachShow.close(); return; }
    if (window.TeachRoom && window.TeachRoom.isOpen() && !document.body.classList.contains('teach-tool')) {
      return;
    }
    if (window.TeachRoom && window.TeachRoom.isOpen()) window.TeachRoom.close();
    document.body.classList.remove('teach-tool');
    back.hidden = true;
    document.querySelectorAll('[id^="tab-"]').forEach((el) => { el.hidden = el.id !== 'tab-teach'; });
    const title = document.getElementById('workspace-title');
    if (title) title.textContent = 'ម៉ូដបង្រៀន';
    render.teach();
  });
  if (teachOn()) applyTeachMode(true, false);
}

let editingStudentId = null;

function downloadSampleExcel() {
  if (typeof XLSX === 'undefined') {
    Exam.notify('មិនទាន់ដំណើរការបណ្ណាល័យ Excel នៅឡើយទេ។');
    return;
  }
  const headers = ['អត្តលេខ', 'គោត្តនាម', 'នាម', 'ភេទ', 'ថ្ងៃខែឆ្នាំកំណើត'];
  const sampleData = [
    headers,
    ['010901', 'សុខ', 'ដារា', 'ប្រុស', '2010-04-15'],
    ['010902', 'ចាន់', 'សុភា', 'ស្រី', '2010-08-20'],
    ['010903', 'កែវ', 'វិសាល', 'ប្រុស', '2010-01-05'],
    ['010904', 'ម៉ៅ', 'ធីតា', 'ស្រី', '2010-11-12'],
  ];
  const ws = XLSX.utils.aoa_to_sheet(sampleData);
  ws['!cols'] = [{ wch: 14 }, { wch: 14 }, { wch: 14 }, { wch: 10 }, { wch: 18 }];
  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, ws, 'បញ្ជីសិស្ស');
  XLSX.writeFile(wb, 'គំរូបញ្ជីឈ្មោះសិស្ស.xlsx');
}

function parseExcelRows(rawRows) {
  if (!rawRows || rawRows.length === 0) return [];

  function norm(str) {
    return String(str || '').replace(/[​‌‍﻿]/g, '').trim().toLowerCase();
  }

  let headerIndex = -1;
  let idCol = -1, surnameCol = -1, firstNameCol = -1, fullNameCol = -1, genderCol = -1, dobCol = -1;

  for (let r = 0; r < Math.min(rawRows.length, 15); r++) {
    const row = rawRows[r].map(norm);
    const hasId = row.some((c) => c.includes('អត្តលេខ') || c.includes('សម្គាល់') || c === 'id' || c.includes('student'));
    const hasName = row.some((c) => c.includes('នាម') || c.includes('ឈ្មោះ') || c.includes('name'));
    if (hasId || hasName) {
      headerIndex = r;
      row.forEach((cell, cIdx) => {
        if (cell.includes('អត្តលេខ') || cell.includes('សម្គាល់') || cell === 'id' || cell.includes('student id')) idCol = cIdx;
        else if (cell.includes('គោត្តនាម និងនាម') || cell.includes('គោត្តនាម-នាម') || cell.includes('ឈ្មោះពេញ') || cell === 'fullname' || cell === 'full name' || cell === 'ឈ្មោះ') fullNameCol = cIdx;
        else if (cell.includes('គោត្តនាម') || cell.includes('ត្រកូល') || cell === 'surname' || cell === 'last name' || cell === 'family name') surnameCol = cIdx;
        else if (cell.includes('នាម') || cell === 'first name' || cell === 'firstname' || cell === 'given name') firstNameCol = cIdx;
        else if (cell.includes('ភេទ') || cell === 'sex' || cell === 'gender') genderCol = cIdx;
        else if (cell.includes('កំណើត') || cell === 'dob' || cell.includes('birth')) dobCol = cIdx;
      });
      break;
    }
  }

  let dataRows = [];
  if (headerIndex >= 0) {
    dataRows = rawRows.slice(headerIndex + 1);
  } else {
    idCol = 0; surnameCol = 1; firstNameCol = 2; genderCol = 3; dobCol = 4;
    dataRows = rawRows;
  }

  const students = [];
  for (const row of dataRows) {
    if (!row || row.length === 0) continue;
    const getVal = (col) => (col >= 0 && col < row.length ? String(row[col] || '').trim() : '');

    let id = getVal(idCol);
    let surname = getVal(surnameCol);
    let firstName = getVal(firstNameCol);
    let fullName = getVal(fullNameCol);
    let gender = getVal(genderCol);
    let dob = getVal(dobCol);

    if (!id && row[0]) {
      const first = String(row[0]).trim();
      if (/^\w+$/.test(first) && first !== 'ល.រ' && first !== 'no') id = first;
    }

    if ((!surname || !firstName) && fullName) {
      const parts = fullName.split(/\s+/).filter(Boolean);
      if (parts.length >= 2) {
        surname = parts[0];
        firstName = parts.slice(1).join(' ');
      } else if (parts.length === 1) {
        surname = parts[0];
        firstName = parts[0];
      }
    }

    if (gender) {
      const gNorm = gender.toLowerCase();
      if (gNorm === 'm' || gNorm === 'male' || gNorm === 'ប្រុស' || gNorm === 'ប') gender = 'ប្រុស';
      else if (gNorm === 'f' || gNorm === 'female' || gNorm === 'ស្រី' || gNorm === 'ស') gender = 'ស្រី';
    }

    if (id && surname && firstName) {
      students.push({
        id: String(id).trim(),
        surname: String(surname).trim(),
        first_name: String(firstName).trim(),
        gender: gender || '',
        dob: dob || '',
      });
    }
  }
  return students;
}

function studentRow(container, cls, s) {
  if (editingStudentId === s.id) {
    const surnameInput = h('input', { type: 'text', value: s.surname || '', style: 'min-width:0;width:100%' });
    const firstNameInput = h('input', { type: 'text', value: s.first_name || '', style: 'min-width:0;width:100%' });
    const genderSelect = h('select', { style: 'min-width:0;width:100%' }, [
      h('option', { value: '', selected: !s.gender }, '— មិនបញ្ជាក់ —'),
      h('option', { value: 'ប្រុស', selected: s.gender === 'ប្រុស' }, 'ប្រុស'),
      h('option', { value: 'ស្រី', selected: s.gender === 'ស្រី' }, 'ស្រី'),
    ]);
    const dobInput = h('input', { type: 'text', value: s.dob || '', placeholder: 'YYYY-MM-DD', style: 'min-width:0;width:100%' });

    return h('tr', {}, [
      h('td', {}, h('strong', {}, s.id)),
      h('td', {}, surnameInput),
      h('td', {}, firstNameInput),
      h('td', {}, genderSelect),
      h('td', {}, dobInput),
      h('td', { class: 'row', style: 'gap:4px' }, [
        h('button', { class: 'btn-sm', onclick: async () => {
          const surname = surnameInput.value.trim();
          const first_name = firstNameInput.value.trim();
          if (!surname || !first_name) return Exam.notify('សូមបញ្ចូលគោត្តនាម និងនាម។');
          try {
            await api(`/api/students/${s.id}`, {
              method: 'PUT',
              body: {
                surname,
                first_name,
                gender: genderSelect.value.trim(),
                dob: dobInput.value.trim(),
              },
            });
            editingStudentId = null;
            renderRoster(container);
          } catch (e) {
            Exam.notify(e.message);
          }
        } }, 'រក្សាទុក'),
        h('button', { class: 'btn-sm secondary', onclick: () => { editingStudentId = null; renderRoster(container); } }, 'បោះបង់'),
      ]),
    ]);
  }

  const genderBadge = s.gender === 'ប្រុស'
    ? h('span', { class: 'badge-gender m' }, 'ប្រុស')
    : s.gender === 'ស្រី'
    ? h('span', { class: 'badge-gender f' }, 'ស្រី')
    : h('span', { class: 'muted' }, s.gender || '—');

  return h('tr', {}, [
    h('td', {}, h('strong', {}, s.id)),
    h('td', {}, s.surname),
    h('td', {}, s.first_name),
    h('td', {}, genderBadge),
    h('td', { class: 'muted' }, s.dob || '—'),
    h('td', { class: 'row', style: 'gap:4px' }, [
      h('button', { class: 'btn-sm secondary', onclick: () => { editingStudentId = s.id; renderRoster(container); } }, 'កែ'),
      h('button', { class: 'btn-sm danger', onclick: async () => {
        if (!confirm(`តើលោកគ្រូពិតជាចង់លុបសិស្ស «${s.surname} ${s.first_name}» (${s.id}) ឬ?`)) return;
        try {
          await api(`/api/students/${s.id}`, { method: 'DELETE' });
          renderRoster(container);
        } catch (e) {
          Exam.notify(e.message);
        }
      } }, 'លុប'),
    ]),
  ]);
}

async function renderRoster(container) {
  const { classes } = await api('/api/classes');
  const cls = classes.find((c) => c.id === selectedClassId);
  const { students } = await api(`/api/classes/${selectedClassId}/students`);

  const dobBox = cls && cls.my_role !== 'reviewer' && cls.my_role !== 'sample' ? h('label', { class: 'dob-toggle', title: 'សិស្សត្រូវវាយថ្ងៃកំណើតបន្ថែមលើអត្តលេខ ដើម្បីចូលមើលលទ្ធផល' }, [
    h('input', { type: 'checkbox', checked: cls.require_dob ? 'checked' : null, style: 'width:18px;height:18px;', onchange: async (e) => {
      try { await api(`/api/classes/${cls.id}/settings`, { method: 'POST', body: { require_dob: e.target.checked } }); } catch (er) { e.target.checked = !e.target.checked; Exam.notify(er.message); }
    } }),
    ' 🔐 សិស្សត្រូវវាយថ្ងៃកំណើតពេលចូល',
  ]) : null;
  const card = h('div', { class: 'card' }, [
    h('div', { class: 'row', style: 'justify-content:space-between' }, [
      h('h2', {}, `បញ្ជីសិស្ស — ${cls ? cls.name : ''} (សរុប ${students.length} នាក់)`),
      h('button', { class: 'secondary', onclick: () => { selectedClassId = null; render.classes(); } }, '← ត្រឡប់'),
    ]),
    dobBox,
    h('table', {}, [
      h('thead', {}, h('tr', {}, [
        h('th', {}, 'លេខសម្គាល់'),
        h('th', {}, 'គោត្តនាម'),
        h('th', {}, 'នាម'),
        h('th', {}, 'ភេទ'),
        h('th', {}, 'ថ្ងៃកំណើត'),
        h('th', {}, 'សកម្មភាព'),
      ])),
      h('tbody', {}, students.length === 0
        ? [h('tr', {}, [h('td', { colspan: 6, style: 'text-align:center;padding:24px;color:var(--muted);' }, 'មិនទាន់មានសិស្សក្នុងថ្នាក់នេះនៅឡើយទេ។ សូមបញ្ចូលដោយដៃ ឬ Upload Excel ខាងក្រោម។')])]
        : students.map((s) => studentRow(container, cls, s))),
    ]),
  ]);

  const addOne = h('div', { class: 'card' }, [
    h('h3', {}, 'បញ្ចូលសិស្សម្នាក់ដោយដៃ'),
    h('div', { class: 'row' }, [
      h('input', { type: 'text', id: 'one-id', placeholder: 'លេខសម្គាល់ * (ឧ. 0109293)', style: 'flex:1.2;min-width:130px;' }),
      h('input', { type: 'text', id: 'one-surname', placeholder: 'គោត្តនាម * (ឧ. សុខ)', style: 'flex:1.2;min-width:130px;' }),
      h('input', { type: 'text', id: 'one-first-name', placeholder: 'នាម * (ឧ. ដារា)', style: 'flex:1.2;min-width:130px;' }),
    ]),
    h('div', { class: 'row', style: 'margin-top:8px;' }, [
      h('select', { id: 'one-gender', style: 'flex:1;min-width:120px;' }, [
        h('option', { value: '' }, '-- ភេទ (ស្រេចចិត្ត) --'),
        h('option', { value: 'ប្រុស' }, 'ប្រុស'),
        h('option', { value: 'ស្រី' }, 'ស្រី'),
      ]),
      h('input', { type: 'text', id: 'one-dob', placeholder: 'ថ្ងៃខែឆ្នាំកំណើត (ស្រេចចិត្ត ឧ. 2010-04-15)', style: 'flex:1.5;min-width:160px;' }),
      h('button', { onclick: async () => {
        const id = document.getElementById('one-id').value.trim();
        const surname = document.getElementById('one-surname').value.trim();
        const first_name = document.getElementById('one-first-name').value.trim();
        const gender = document.getElementById('one-gender').value.trim();
        const dob = document.getElementById('one-dob').value.trim();
        if (!id || !surname || !first_name) {
          return Exam.notify('សូមបញ្ចូលលេខសម្គាល់ គោត្តនាម និងនាមសិស្ស។');
        }
        try {
          await api(`/api/classes/${selectedClassId}/students`, {
            method: 'POST',
            body: { id, surname, first_name, gender, dob },
          });
          await Exam.notify(`បានបញ្ចូលសិស្ស «${surname} ${first_name}» ដោយជោគជ័យ។`);
          renderRoster(container);
        } catch (e) {
          Exam.notify(e.message);
        }
      } }, 'បញ្ចូលសិស្ស'),
    ]),
  ]);

  // Excel Upload section
  let excelParsed = null;
  const excelPreviewBox = h('div', { class: 'preview-box', hidden: true });
  const fileInput = h('input', { type: 'file', accept: '.xlsx,.xls,.csv', style: 'display:none;' });

  const dropzoneEl = h('div', { class: 'dropzone' }, [
    h('span', { class: 'dropzone-icon' }, '📊'),
    h('div', { style: 'font-weight:600;' }, 'ចុចទីនេះ ឬទាញទម្លាក់ឯកសារ Excel (.xlsx, .xls) ឬ .csv មកទីនេះ'),
    h('div', { class: 'muted', style: 'font-size:13px;margin-top:4px;' }, 'ប្រព័ន្ធនឹងអានជួរឈរ អត្តលេខ, គោត្តនាម, នាម, ភេទ, ថ្ងៃកំណើត ដោយស្វ័យប្រវត្តិ'),
  ]);

  function handleFile(file) {
    if (!file) return;
    if (typeof XLSX === 'undefined') {
      return Exam.notify('បណ្ណាល័យអាន Excel មិនទាន់ផ្ទុកពេញលេញនៅឡើយ។ សូម refresh ទំព័រ។');
    }
    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const data = new Uint8Array(e.target.result);
        const wb = XLSX.read(data, { type: 'array', cellDates: true });
        const sheetName = wb.SheetNames[0];
        const sheet = wb.Sheets[sheetName];
        const rawRows = XLSX.utils.sheet_to_json(sheet, { header: 1, defval: '', raw: false });
        const students = parseExcelRows(rawRows);

        if (students.length === 0) {
          return Exam.notify('មិនអាចស្វែងរកទិន្នន័យសិស្សក្នុងឯកសារនេះទេ។ សូមពិនិត្យមើលជួរឈរ អត្តលេខ គោត្តនាម នាម។');
        }

        excelParsed = students;
        excelPreviewBox.hidden = false;
        excelPreviewBox.innerHTML = '';
        excelPreviewBox.append(
          h('div', { class: 'notice' }, `✅ រកឃើញសិស្សចំនួន ${students.length} នាក់ ពីឯកសារ «${file.name}»`),
          h('table', { style: 'margin-top:8px' }, [
            h('thead', {}, h('tr', {}, [
              h('th', {}, 'ល.រ'),
              h('th', {}, 'អត្តលេខ'),
              h('th', {}, 'គោត្តនាម'),
              h('th', {}, 'នាម'),
              h('th', {}, 'ភេទ'),
              h('th', {}, 'ថ្ងៃកំណើត'),
            ])),
            h('tbody', {}, students.slice(0, 10).map((s, idx) => h('tr', {}, [
              h('td', { class: 'muted' }, idx + 1),
              h('td', {}, h('strong', {}, s.id)),
              h('td', {}, s.surname),
              h('td', {}, s.first_name),
              h('td', {}, s.gender ? (s.gender === 'ប្រុស' ? h('span', { class: 'badge-gender m' }, 'ប្រុស') : h('span', { class: 'badge-gender f' }, 'ស្រី')) : '—'),
              h('td', { class: 'muted' }, s.dob || '—'),
            ]))),
          ]),
          students.length > 10 ? h('p', { class: 'muted', style: 'text-align:center;margin:6px 0;' }, `... និងសិស្ស ${students.length - 10} នាក់ទៀត ...`) : '',
          h('div', { class: 'row', style: 'margin-top:12px;justify-content:flex-end;' }, [
            h('button', { onclick: async () => {
              try {
                const { students: created } = await api(`/api/classes/${selectedClassId}/students/bulk`, {
                  method: 'POST',
                  body: { students: excelParsed },
                });
                await Exam.notify(`បានបញ្ចូលសិស្សចំនួន ${created.length} នាក់ដោយជោគជ័យ!`);
                renderRoster(container);
              } catch (e) {
                Exam.notify(e.message);
              }
            } }, `💾 រក្សាទុកចូលក្នុងថ្នាក់ (${students.length} នាក់)`),
            h('button', { class: 'secondary', onclick: () => {
              excelParsed = null;
              excelPreviewBox.hidden = true;
              excelPreviewBox.innerHTML = '';
            } }, 'បោះបង់'),
          ]),
        );
      } catch (err) {
        Exam.notify('កំហុសក្នុងការអានឯកសារ Excel៖ ' + err.message);
      }
    };
    reader.readAsArrayBuffer(file);
  }

  dropzoneEl.onclick = () => fileInput.click();
  fileInput.onchange = (e) => {
    if (e.target.files && e.target.files[0]) handleFile(e.target.files[0]);
  };
  dropzoneEl.ondragover = (e) => { e.preventDefault(); dropzoneEl.classList.add('dragover'); };
  dropzoneEl.ondragleave = () => dropzoneEl.classList.remove('dragover');
  dropzoneEl.ondrop = (e) => {
    e.preventDefault();
    dropzoneEl.classList.remove('dragover');
    if (e.dataTransfer.files && e.dataTransfer.files[0]) handleFile(e.dataTransfer.files[0]);
  };

  const excelCard = h('div', { class: 'card' }, [
    h('div', { class: 'row', style: 'justify-content:space-between;align-items:flex-start;' }, [
      h('div', {}, [
        h('h3', {}, 'នាំចូលតាមឯកសារ Excel / CSV (.xlsx, .xls, .csv)'),
        h('p', { class: 'muted', style: 'margin:2px 0 8px;' }, 'គាំទ្រជួរឈរ៖ អត្តលេខ, គោត្តនាម, នាម (និងស្រេចចិត្ត៖ ភេទ, ថ្ងៃខែឆ្នាំកំណើត)។'),
      ]),
      h('button', { class: 'secondary btn-sm', onclick: downloadSampleExcel }, '📥 ទាញយកគំរូ Excel (.xlsx)'),
    ]),
    fileInput,
    dropzoneEl,
    excelPreviewBox,
  ]);

  const bulk = h('div', { class: 'card' }, [
    h('h3', {}, 'ឬចម្លងបិទភ្ជាប់អត្ថបទ (Copy & Paste)'),
    h('p', { class: 'muted' }, 'ចម្លង ១ ជួរ ១ សិស្ស៖ លេខសម្គាល់  គោត្តនាម  នាម  [ភេទ]  [ថ្ងៃកំណើត] (ដកឃ្លា ថេប ឬសញ្ញាក្បៀស , — អាចចម្លងផ្ទាល់ពី Excel)'),
    h('textarea', { id: 'bulk-text', placeholder: '0109293\tសុខ\tដារា\tប្រុស\t2010-04-15\n0109294, ចាន់, សុភា, ស្រី, 2010-08-20' }),
    h('div', { class: 'row', style: 'margin-top:8px' }, [
      h('button', { onclick: async () => {
        const raw = document.getElementById('bulk-text').value;
        const lines = raw.replace(/[​‌‍﻿]/g, '').split('\n').map((l) => l.trim()).filter(Boolean);
        const parsed = lines.map((line) => {
          const parts = (line.includes(',') ? line.split(',') : line.split(/\t+|\s{2,}|\s+/)).map((p) => p.trim()).filter(Boolean);
          const [id, surname, firstName, gender, ...rest] = parts;
          let dob = rest.join(' ');
          let cleanGender = gender || '';
          if (cleanGender && (cleanGender === 'M' || cleanGender === 'm' || cleanGender === 'ប្រុស')) cleanGender = 'ប្រុស';
          else if (cleanGender && (cleanGender === 'F' || cleanGender === 'f' || cleanGender === 'ស្រី')) cleanGender = 'ស្រី';
          else if (cleanGender && /^\d{4}/.test(cleanGender)) {
            dob = cleanGender + (dob ? ' ' + dob : '');
            cleanGender = '';
          }
          return { id: id || '', surname: surname || '', first_name: firstName || '', gender: cleanGender, dob: dob || '' };
        }).filter((s) => s.id && s.surname && s.first_name);

        if (parsed.length === 0) return Exam.notify('មិនមានទិន្នន័យត្រឹមត្រូវសម្រាប់នាំចូលទេ។');
        try {
          const { students: created } = await api(`/api/classes/${selectedClassId}/students/bulk`, { method: 'POST', body: { students: parsed } });
          document.getElementById('bulk-text').value = '';
          await Exam.notify(`បានបញ្ចូលសិស្សចំនួន ${created.length} នាក់ដោយជោគជ័យ។`);
          renderRoster(container);
        } catch (e) {
          Exam.notify(e.message);
        }
      } }, 'នាំចូល'),
    ]),
  ]);

  container.innerHTML = '';
  if (cls && cls.my_role === 'reviewer') {
    card.classList.add('readonly');
    container.append(h('div', { class: 'notice' }, '👁 អ្នកជាអ្នកពិនិត្យ — មើលបានតែមិនអាចកែប្រែបញ្ជីសិស្សបានទេ។'), card);
    return;
  }
  container.append(card, addOne, excelCard, bulk);
}

// ---------- Tests ----------
let selectedTestId = null;
let testFilter = 'all';
let testSearch = '';

render.tests = async function () {
  const container = document.getElementById('tab-tests');
  container.innerHTML = '';
  if (selectedTestId) return renderTestBuilder(container);

  const { tests } = await api('/api/tests');

  const goSchedule = (id) => {
    document.querySelectorAll('.tabs button').forEach((b) => b.classList.toggle('active', b.dataset.tab === 'schedule'));
    document.querySelectorAll('[id^="tab-"]').forEach((el) => { el.hidden = el.id !== 'tab-schedule'; });
    render.schedule(id);
  };
  const closeMenus = () => document.querySelectorAll('.menu-pop').forEach((m) => m.remove());
  document.addEventListener('click', closeMenus, { once: true });

  function testCard(t) {
    const mcq = t.question_count - (t.writing_count || 0);
    const shared = t.owner_id !== ME.id;
    const canEdit = (t.my_role === 'owner' || t.my_role === 'editor') && (ME.licensed || ME.status === 'trial');
    const isSample = t.my_role === 'sample';
    const licensed = ME.licensed, mayWork = ME.licensed || ME.status === 'trial';

    const menuBtn = h('button', { class: 'icon-btn', title: 'ជម្រើសផ្សេងទៀត', 'aria-label': 'ជម្រើសផ្សេងទៀត' }, '⋯');
    menuBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      const open = menuBtn.parentElement.querySelector('.menu-pop');
      closeMenus();
      if (open) return;
      const item = (label, fn, cls = '') => h('button', { class: `menu-item ${cls}`, onclick: (ev) => { ev.stopPropagation(); closeMenus(); fn(); } }, label);
      const pop = h('div', { class: 'menu-pop' }, [
        item('📝 ទាញយកជា Word (.docx)', () => window.open(`paper.html?test=${t.id}&docx=1`, '_blank')),
        licensed || ME.role === 'owner' ? item('📋 ចម្លងតេស្តនេះ', async () => {
          try { const copy = await api(`/api/tests/${t.id}/duplicate`, { method: 'POST' }); await Exam.notify(`បានចម្លងជា «${copy.title}»`); render.tests(); }
          catch (er) { Exam.notify(er.message); }
        }) : null,
        ME.role === 'owner' ? item(t.is_sample ? '⭐ ដកចេញពីតេស្តគំរូ' : '⭐ កំណត់ជាតេស្តគំរូ (គ្រូទាំងអស់ឃើញ)', async () => {
          await api(`/api/tests/${t.id}/sample`, { method: 'POST', body: { is_sample: !t.is_sample } }); render.tests();
        }) : null,
        t.my_role === 'owner' && ME.licensed ? item('👥 ចែករំលែកជាមួយគ្រូ', () => openShareDialog('test', t.id, t.title)) : null,
        t.my_role === 'owner' && (ME.licensed || ME.status === 'trial') ? h('div', { class: 'menu-sep' }) : null,
        t.my_role === 'owner' && (ME.licensed || ME.status === 'trial') ? item('🗑 លុបតេស្ត', async () => {
          if (!confirm(`តើពិតជាចង់លុបតេស្ត «${t.title}» និងសំណួរទាំងអស់ក្នុងតេស្តនេះឬ?`)) return;
          try { await api(`/api/tests/${t.id}`, { method: 'DELETE' }); render.tests(); } catch (er) { Exam.notify(er.message); }
        }, 'danger') : null,
      ]);
      menuBtn.parentElement.append(pop);
    });

    return h('div', { class: `test-card${t.status === 'ready' ? '' : ' is-draft'}` }, [
      h('div', { class: 'test-icon' }, t.writing_count ? '📝' : '✅'),
      h('div', { class: 'test-main' }, [
        h('div', { class: 'test-title' }, t.title),
        h('div', { class: 'test-chips' }, [
          h('span', { class: `chip ${t.status === 'ready' ? 'chip-open' : 'chip-closed'}` }, t.status === 'ready' ? '● រួចរាល់' : '○ សម្រាង'),
          h('span', { class: 'chip chip-plain' }, `${mcq} ពហុជ្រើសរើស`),
          t.writing_count ? h('span', { class: 'chip chip-plain' }, `✎ ${t.writing_count} សរសេរ`) : null,
          h('span', { class: 'chip chip-plain' }, `${t.total_points} ពិន្ទុ`),
          t.session_count ? h('span', { class: 'chip chip-plain' }, `📅 បានប្រឡង ${t.session_count} ដង`) : null,
          isSample ? h('span', { class: 'chip chip-soon' }, '⭐ តេស្តគំរូ') : null,
          shared && !isSample ? h('span', { class: `chip ${t.my_role === 'reviewer' ? 'chip-closed' : 'chip-soon'}` }, t.my_role === 'owner' ? `👤 ដោយ ${t.owner_name || ''}` : `👥 ${roleLabel(t.my_role)} · ${t.owner_name || ''}`) : null,
          t.open_notes ? h('span', { class: 'chip chip-soon' }, `💬 ${t.open_notes} ចំណាំ`) : null,
        ]),
      ]),
      h('div', { class: 'test-actions' }, [
        h('button', { class: 'btn-primary-sm', onclick: () => { selectedTestId = t.id; render.tests(); } }, canEdit ? '✏️ កែសម្រួល' : isSample ? '⭐ មើលតេស្តគំរូ' : t.my_role === 'owner' ? '🔍 មើល' : '🔍 ពិនិត្យ'),
        mayWork && !isSample || ME.role === 'owner' ? h('button', { class: 'btn-go', title: 'កំណត់ពេលប្រឡងឱ្យថ្នាក់', onclick: () => goSchedule(t.id) }, '📅 ប្រឡង') : null,
        h('button', { class: 'icon-btn', title: 'មើលជាសិស្ស', 'aria-label': 'មើលជាសិស្ស', onclick: () => window.open(`student.html?preview=${t.id}`, '_blank') }, '👁'),
        h('button', { class: 'icon-btn', title: 'បោះពុម្ព / PDF', 'aria-label': 'PDF', onclick: () => window.open(`paper.html?test=${t.id}`, '_blank') }, '📄'),
        h('div', { class: 'menu-wrap' }, [menuBtn]),
      ]),
    ]);
  }

  // header: title, search, filter tabs, new-test button
  const search = h('input', { type: 'text', placeholder: '🔍 ស្វែងរកតេស្ត…', class: 'tests-search', value: testSearch });
  const listBox = h('div', { class: 'test-list' });
  const filters = [['all', 'ទាំងអស់'], ['ready', 'រួចរាល់'], ['draft', 'សម្រាង'], ['mine', 'របស់ខ្ញុំ'], ['shared', 'ចែករំលែកជាមួយខ្ញុំ']];
  const filterBar = h('div', { class: 'filter-bar' });

  function draw() {
    const q = testSearch.trim().toLowerCase();
    const list = tests.filter((t) => {
      if (q && !t.title.toLowerCase().includes(q)) return false;
      if (testFilter === 'ready') return t.status === 'ready';
      if (testFilter === 'draft') return t.status !== 'ready';
      if (testFilter === 'mine') return t.owner_id === ME.id;
      if (testFilter === 'shared') return t.owner_id !== ME.id;
      return true;
    });
    filterBar.innerHTML = '';
    for (const [k, label] of filters) {
      const n = tests.filter((t) => (k === 'all' ? true : k === 'ready' ? t.status === 'ready' : k === 'draft' ? t.status !== 'ready' : k === 'mine' ? t.owner_id === ME.id : t.owner_id !== ME.id)).length;
      if (k === 'shared' && !tests.some((t) => t.owner_id !== ME.id)) continue;
      if (k === 'mine' && !tests.some((t) => t.owner_id !== ME.id)) continue;
      filterBar.append(h('button', { class: `filter-pill${testFilter === k ? ' on' : ''}`, onclick: () => { testFilter = k; draw(); } }, [label, h('span', { class: 'pill-n' }, String(n))]));
    }
    listBox.innerHTML = '';
    if (!list.length) {
      listBox.append(h('div', { class: 'empty-card' }, [h('div', { class: 'empty-icon' }, '🗂'), h('div', { class: 'muted' }, tests.length ? 'រកមិនឃើញតេស្តដែលត្រូវនឹងការស្វែងរកទេ។' : (ME.licensed || ME.status === 'trial') ? 'មិនទាន់មានតេស្តទេ — ចុច «＋ តេស្តថ្មី» ដើម្បីចាប់ផ្តើម។' : 'មិនទាន់មានតេស្តគំរូទេ។ សូមរង់ចាំម្ចាស់ប្រព័ន្ធបន្ថែម។')]));
    }
    list.forEach((t) => listBox.append(testCard(t)));
  }
  search.addEventListener('input', () => { testSearch = search.value; draw(); });

  const newTitle = h('input', { type: 'text', placeholder: 'ចំណងជើងតេស្តថ្មី ឧ. ប្រឡងប្រចាំខែវិច្ឆិកា ថ្នាក់ទី ៧', style: 'flex:1;min-width:220px;' });
  const createNew = async () => {
    if (!newTitle.value.trim()) return newTitle.focus();
    const t = await api('/api/tests', { method: 'POST', body: { title: newTitle.value.trim() } });
    selectedTestId = t.id; render.tests();
  };
  newTitle.addEventListener('keydown', (e) => { if (e.key === 'Enter') createNew(); });
  const newRow = h('div', { class: 'new-test-row', hidden: 'hidden' }, [newTitle, h('button', { onclick: createNew }, 'បង្កើត'), h('button', { class: 'secondary', onclick: () => { newRow.hidden = true; } }, 'បោះបង់')]);

  container.append(h('div', { class: 'card tests-head' }, [
    h('div', { class: 'tests-head-top' }, [
      h('div', {}, [h('h2', { style: 'margin:0;' }, 'តេស្ត'), h('div', { class: 'muted' }, `សរុប ${tests.length} តេស្ត`)]),
      h('div', { class: 'row', style: 'gap:8px;' }, [search, h('button', { onclick: () => { if (!ME.licensed && ME.status !== 'trial') return Exam.notify('🔒 ត្រូវដោះសោគណនីសិន ទើបអាចបង្កើតតេស្តបាន។ សូមបញ្ចូលកូដពីម្ចាស់ប្រព័ន្ធ។'); newRow.hidden = false; newTitle.focus(); } }, (ME.licensed || ME.status === 'trial') ? '＋ តេស្តថ្មី' : '🔒 តេស្តថ្មី')]),
    ]),
    newRow,
    filterBar,
  ]), listBox);
  draw();
};

// re-draws the test editor but keeps the teacher where they were (after save / delete / note)
async function renderTestBuilder(container) {
  const same = container.dataset.tb === String(selectedTestId);
  const y = window.scrollY;
  await drawTestBuilder(container);
  container.dataset.tb = String(selectedTestId);
  if (same) window.scrollTo(0, y);
}

async function drawTestBuilder(container) {
  const test = await api(`/api/tests/${selectedTestId}`);
  container.innerHTML = '';

  const mayRename = (test.my_role === 'owner' || test.my_role === 'editor') && (ME.licensed || ME.status === 'trial');
  const rename = async () => {
    const inp = h('input', { type: 'text', value: test.title, maxlength: '150' });
    const back = h('div', { class: 'modal-back', onclick: (e) => { if (e.target === back) back.remove(); } });
    const save = async () => {
      if (!inp.value.trim()) return inp.focus();
      try { await api(`/api/tests/${test.id}`, { method: 'PUT', body: { title: inp.value.trim() } }); back.remove(); renderTestBuilder(container); } catch (e) { Exam.notify(e.message); }
    };
    inp.addEventListener('keydown', (e) => { if (e.key === 'Enter') save(); });
    back.append(h('div', { class: 'modal-box', style: 'text-align:left;max-width:520px;' }, [h('h2', {}, '✏️ ប្តូរឈ្មោះតេស្ត'), inp,
      h('div', { class: 'row', style: 'justify-content:flex-end;margin-top:14px;' }, [h('button', { class: 'secondary', onclick: () => back.remove() }, 'បោះបង់'), h('button', { onclick: save }, 'រក្សាទុក')])]));
    document.body.append(back); inp.focus(); inp.select();
  };
  const header = h('div', { class: 'card' }, [
    h('div', { class: 'row', style: 'justify-content:space-between' }, [
      h('h2', {}, [test.title, mayRename ? h('button', { class: 'secondary btn-sm', style: 'margin-left:10px;vertical-align:middle;', title: 'ប្តូរឈ្មោះតេស្ត', onclick: rename }, '✏️ ប្តូរឈ្មោះ') : null]),
      h('button', { class: 'secondary', onclick: () => { selectedTestId = null; container.dataset.tb = ''; render.tests(); } }, '← ត្រឡប់'),
    ]),
    h('div', { class: 'row' }, [
      h('button', { class: 'secondary', onclick: () => window.open(`student.html?preview=${test.id}`, '_blank') }, '👁 មើលជាសិស្ស'),
      h('button', { class: 'secondary', onclick: () => window.open(`paper.html?test=${test.id}`, '_blank') }, '📄 វិញ្ញាសា PDF'),
      h('button', { class: 'secondary', onclick: () => window.open(`paper.html?test=${test.id}&docx=1`, '_blank') }, '📝 Word'),
      h('span', { class: `badge ${test.status}` }, test.status === 'ready' ? 'រួចរាល់' : 'សម្រាង'),
      test.status !== 'ready'
        ? h('button', { onclick: async () => { await api(`/api/tests/${test.id}`, { method: 'PUT', body: { status: 'ready' } }); renderTestBuilder(container); } }, 'សម្គាល់ថារួចរាល់')
        : h('button', { class: 'secondary', onclick: async () => { await api(`/api/tests/${test.id}`, { method: 'PUT', body: { status: 'draft' } }); renderTestBuilder(container); } }, 'ត្រឡប់ទៅសម្រាង'),
    ]),
  ]);

  const mcqQs = test.questions.filter((q) => q.kind !== 'writing');
  const wQs = test.questions.filter((q) => q.kind === 'writing');
  const sum = (a) => a.reduce((t, q) => t + q.points, 0);
  const list = h('div', { class: 'card' }, [
    h('h3', {}, `សំណួរ (${test.questions.length}) — ពហុជ្រើសរើស ${mcqQs.length} សំណួរ ${sum(mcqQs)} ពិន្ទុ · សរសេរ ${wQs.length} សំណួរ ${sum(wQs)} ពិន្ទុ · សរុប ${sum(test.questions)} ពិន្ទុ`),
    ...test.questions.map((q, i) => h('div', { class: 'question-card' }, [
      h('div', { class: 'row', style: 'justify-content:space-between' }, [
        h('div', {}, [h('strong', {}, `${i + 1}.`), h('span', { class: 'chip chip-plain', style: 'margin-left:6px;font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-weight:700;color:#1e40af;background:#eff6ff;border:1px solid #bfdbfe;' }, `#${q.id}`), (q.kind === 'writing' ? h('span', { class: 'badge upcoming', style: 'margin-left:8px;' }, '✎ សរសេរ') : null), q.cancelled ? h('span', { class: 'badge closed', style: 'margin-left:8px;' }, 'បានបោះបង់') : null, q.topic ? h('span', { class: 'chip chip-plain', style: 'margin-left:8px;' }, q.topic) : null, q.lesson ? h('span', { class: 'chip chip-plain', style: 'margin-left:4px;' }, `${q.grade ? 'ថ្នាក់ ' + q.grade + ' · ' : ''}${q.lesson}`) : null, q.level ? h('span', { class: 'chip chip-plain', style: 'margin-left:4px;' }, { easy: 'ងាយ', medium: 'មធ្យម', hard: 'ពិបាក', pisa: 'បែប PISA' }[q.level]) : null, q.alt_correct_index != null ? h('span', { class: 'chip chip-soon', style: 'margin-left:4px;' }, 'ទទួលចម្លើយ២') : null]),
        h('div', { class: 'row', style: 'gap:6px;' }, [
          h('button', { class: 'secondary btn-sm', onclick: () => openQuestionEditor(q, test, container) }, '✏️ កែ'),
          h('button', { class: 'danger btn-sm', onclick: async () => { if (await Exam.confirm('លុបសំណួរនេះ?')) { await api(`/api/questions/${q.id}`, { method: 'DELETE' }); renderTestBuilder(container); } } }, 'លុប'),
        ]),
      ]),
      mathEl('div', {}, Exam.withSample(q).stem_text),
      q.params ? h('div', { class: 'callout', style: 'margin:6px 0;' }, '🎲 សំណួរមានអថេរ — សិស្សម្នាក់ៗទទួលលេខខុសគ្នា (កំពុងបង្ហាញឧទាហរណ៍មួយ)') : null,
      q.image_key ? h('img', { src: `/api/images/${q.image_key}` }) : null,
      q.kind === 'writing'
        ? (q.solution_text ? mathEl('div', { class: 'p-key', style: 'white-space:pre-line;margin-top:8px;padding:6px 10px;background:#f1f6ff;border-left:4px solid #2260d6;' }, q.solution_text) : null)
        : h('div', { class: 'radio-list' }, Exam.withSample(q).options.map((opt, idx) => h('div', { class: `radio-opt${idx === q.correct_index ? ' selected' : ''}` }, [
            h('span', {}, idx === q.correct_index ? '✓' : '○'), mathEl('span', { class: 'opt-body' }, opt),
          ]))),
      h('div', { class: 'muted' }, `${q.points} ពិន្ទុ`),
      notesBlock(q, test, container),
    ])),
  ]);

  const canEdit = (test.my_role === 'owner' || test.my_role === 'editor') && (ME.licensed || ME.status === 'trial');
  if (!canEdit) {
    container.append(h('div', { class: 'notice' }, test.my_role === 'sample' ? '⭐ នេះជាតេស្តគំរូ — សាកល្បងជាសិស្ស និងមើលទម្រង់វិញ្ញាសាបាន (ចម្លើយត្រឹមត្រូវត្រូវបានលាក់)។' : '👁 អ្នកជាអ្នកពិនិត្យ — អាចមើល សាកល្បងជាសិស្ស និងសរសេរចំណាំលើសំណួរបាន តែមិនអាចកែប្រែបានទេ។'), header, list);
    if (test.my_role === 'sample') list.querySelectorAll('.notes').forEach((n) => n.parentElement.remove());
    list.querySelectorAll('button.danger').forEach((b) => b.remove());
    header.querySelectorAll('button').forEach((b) => { if (/សម្រាង|រួចរាល់/.test(b.textContent)) b.remove(); });
    return;
  }
  const topics = [...new Set(test.questions.map((q) => q.topic).filter(Boolean))];
  const dl = h('datalist', { id: 'topic-list' }, topics.map((t) => h('option', { value: t })));
  const warn = test.submissions ? h('div', { class: 'callout warn', style: 'margin-bottom:12px;' }, `⚠ តេស្តនេះមានសិស្ស ${test.submissions} នាក់បានប្រគល់រួចហើយ — ការកែសំណួរ ឬចម្លើយអាចប៉ះពាល់ពិន្ទុ។`) : null;
  container.append(warn, dl, header, list, await buildQuestionForm(test, container), importQuestionsCard(test, container));
}

async function buildQuestionForm(test, container, opts = {}) {
  const done = opts.onDone || (() => renderTestBuilder(container));
  const curr = await loadCurr();
  const gl = gradeLessonPicker(opts.grade, opts.lesson, curr, opts.chapter);
  const optionInputs = [0, 1, 2, 3].map((i) => h('input', { type: 'text', placeholder: `ជម្រើស ${i + 1}`, 'data-opt': i }));
  const correctSelect = h('select', { id: 'q-correct' }, optionInputs.map((_, i) => h('option', { value: i }, `ជម្រើស ${i + 1} ត្រឹមត្រូវ`)));
  const stemInput = h('textarea', { id: 'q-stem', placeholder: 'ឧ. បើ x + 3 = 7 តម្លៃ x គឺ? (សរសេរធម្មតា ដូចជា x^2, 3/4, √20 ឬបិទភ្ជាប់ LaTeX ក្នុង \\( \\))' });
  const pointsInput = h('input', { type: 'number', id: 'q-points', value: '1', style: 'width:90px' });
  const fileInput = h('input', { type: 'file', id: 'q-image', accept: 'image/png,image/jpeg,image/webp,image/svg+xml' });

  // One toolbar serves the stem and every option — it writes into whichever
  // of these fields was focused last.
  let mathTarget = stemInput;
  const trackFocus = (f) => f.addEventListener('focus', () => { mathTarget = f; });
  trackFocus(stemInput);
  optionInputs.forEach(trackFocus);
  const mathBar = Exam.mathBar(() => mathTarget);

  const topicInput = h('input', { type: 'text', list: 'topic-list', placeholder: 'ឧ. ប្រភាគ' });
  const levelInput = h('select', {}, [['', '— មិនកំណត់ —'], ['easy', 'ងាយ'], ['medium', 'មធ្យម'], ['hard', 'ពិបាក'], ['pisa', 'បែប PISA']].map(([v, l]) => h('option', { value: v }, l)));
  const shuffleInput = h('input', { type: 'checkbox', style: 'width:18px;height:18px;' });
  const kindSelect = h('select', { id: 'q-kind' }, [
    h('option', { value: 'mcq' }, 'ពហុជ្រើសរើស (ផ្នែក ក — ប្រព័ន្ធដាក់ពិន្ទុដោយស្វ័យប្រវត្តិ)'),
    h('option', { value: 'writing' }, 'សរសេរ (ផ្នែក ខ — សិស្សសរសេរលើក្រដាស លោកគ្រូដាក់ពិន្ទុ)'),
  ]);
  const solutionInput = h('textarea', { id: 'q-solution', placeholder: 'ចម្លើយគំរូ និងរបៀបដាក់ពិន្ទុ (បង្ហាញក្នុង PDF សម្រាប់គ្រូប៉ុណ្ណោះ)' });
  const mcqSolution = h('textarea', { placeholder: 'ឧ. 3 + 4 = 7 ដូច្នេះចម្លើយគឺ ខ' });
  const addVariants = variantsBlock(() => ({ stem_text: stemInput.value, options: optionInputs.map((i) => i.value.trim()).filter(Boolean), solution_text: mcqSolution.value }));
  const mcqBlock = h('div', {}, [
    h('label', {}, 'ជម្រើសចម្លើយ'),
    ...optionInputs.flatMap((inp) => [inp, Exam.mathPreview(inp)]),
    h('label', {}, 'ជម្រើសត្រឹមត្រូវ'),
    correctSelect,
    h('label', {}, 'ការពន្យល់ចម្លើយ (សិស្សឃើញក្រោយប្រកាសលទ្ធផល — មិនចាំបាច់)'),
    mcqSolution,
    addVariants.box,
  ]);
  const writingBlock = h('div', { hidden: 'hidden' }, [h('label', {}, 'ចម្លើយគំរូ / របៀបដាក់ពិន្ទុ'), solutionInput]);
  kindSelect.onchange = () => { mcqBlock.hidden = kindSelect.value === 'writing'; writingBlock.hidden = kindSelect.value !== 'writing'; };

  return h('div', { class: 'card' }, [
    h('h3', {}, 'បញ្ចូលសំណួរថ្មី'),
    h('label', {}, 'ប្រភេទសំណួរ'),
    kindSelect,
    h('label', {}, 'អត្ថបទសំណួរ — សរសេរគណិតវិទ្យាធម្មតា ឬបិទភ្ជាប់ LaTeX'),
    mathBar,
    stemInput,
    Exam.mathPreview(stemInput),
    h('label', {}, 'រូបភាព (មិនចាំបាច់)'),
    fileInput,
    mcqBlock,
    writingBlock,
    h('label', {}, 'ពិន្ទុ'),
    pointsInput,
    h('div', { class: 'row', style: 'gap:14px;align-items:flex-end;' }, [
      h('div', { style: 'flex:1;min-width:150px;' }, [h('label', {}, 'មុខវិជ្ជា / ប្រធានបទ'), topicInput]),
      h('div', {}, [h('label', {}, 'កម្រិត'), levelInput]),
      h('label', { style: 'display:flex;gap:8px;align-items:center;color:var(--ink);' }, [shuffleInput, 'លាយជម្រើសចម្លើយ']),
    ]),
    h('div', { class: 'row', style: 'gap:14px;align-items:flex-end;' }, [
      h('div', {}, [h('label', {}, 'ថ្នាក់'), gl.grade]),
      h('div', { style: 'flex:1;min-width:180px;' }, [h('label', {}, 'ជំពូក'), gl.chapter, gl.chDl]),
      h('div', { style: 'flex:1;min-width:180px;' }, [h('label', {}, 'មេរៀន'), gl.lesson, gl.dl])
    ]),
    h('div', { class: 'row', style: 'margin-top:12px' }, [
      h('button', { onclick: async () => {
        const isWriting = kindSelect.value === 'writing';
        const options = optionInputs.map((i) => i.value.trim()).filter(Boolean);
        if (!stemInput.value.trim() || (!isWriting && options.length < 2)) { await Exam.notify('សូមបញ្ចូលអត្ថបទសំណួរ និងយ៉ាងតិចជម្រើសចម្លើយពីរ'); return; }
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
          kind: isWriting ? 'writing' : 'mcq', solution_text: isWriting ? solutionInput.value.trim() : (mcqSolution.value.trim() || null),
          topic: topicInput.value.trim(), level: levelInput.value, shuffle: shuffleInput.checked && !isWriting, params: isWriting ? null : addVariants.params.value.trim() || null, ...gl.get(),
        } });
        done();
      } }, 'បញ្ចូលសំណួរ'),
    ]),
  ]);
}

// ---------- Schedule ----------
function timeToMinutes(tStr) {
  const clean = (tStr || '').trim().toLowerCase().replace(/[^0-9:]/g, '');
  if (!clean) return 0;
  if (clean.includes(':')) {
    const parts = clean.split(':');
    return (parseInt(parts[0], 10) || 0) * 60 + (parseInt(parts[1], 10) || 0);
  }
  return (parseInt(clean, 10) || 0) * 60;
}

function minutesToTime(mins) {
  let m = mins % (24 * 60);
  if (m < 0) m += 24 * 60;
  const h = Math.floor(m / 60);
  const min = m % 60;
  return `${String(h).padStart(2, '0')}:${String(min).padStart(2, '0')}`;
}

function parseScheduleDateTime(dateVal, timeVal) {
  let hours = 8, minutes = 0;
  const t = (timeVal || '').trim().toLowerCase();
  const isPm = t.includes('pm') || t.includes('រសៀល') || t.includes('ល្ងាច');
  const isAm = t.includes('am') || t.includes('ព្រឹក');
  const clean = t.replace(/[^0-9:]/g, '');
  if (clean.includes(':')) {
    const parts = clean.split(':');
    hours = parseInt(parts[0], 10) || 0;
    minutes = parseInt(parts[1], 10) || 0;
  } else if (clean.length > 0) {
    hours = parseInt(clean, 10) || 0;
  }
  if (isPm && hours < 12) hours += 12;
  if (isAm && hours === 12) hours = 0;
  const hStr = String(hours).padStart(2, '0');
  const mStr = String(minutes).padStart(2, '0');
  return new Date(`${dateVal}T${hStr}:${mStr}:00`);
}

render.schedule = async function (preSelectedTestId = null) {
  const container = document.getElementById('tab-schedule');
  container.innerHTML = '';
  const [{ tests }, { classes }, { sessions }] = await Promise.all([api('/api/tests'), api('/api/classes'), api('/api/sessions')]);

  const list = h('div', { class: 'card' }, [
    h('h2', {}, 'ការប្រឡងដែលបានកំណត់ពេល'),
    sessions.length === 0 ? h('p', { class: 'muted' }, 'មិនទាន់មានការកំណត់ពេលប្រឡងនៅឡើយទេ។') : null,
    ...sessions.map((s) => h('div', { class: 'list-item' }, [
      h('div', {}, [
        h('div', { class: 'row', style: 'gap:8px;align-items:center;flex-wrap:wrap;' }, [
          h('strong', {}, `${s.test_title} — ${s.class_name}`),
          h('span', { class: `badge ${s.phase}` }, s.phase === 'open' ? 'កំពុងប្រឡង' : s.phase === 'upcoming' ? 'នឹងមកដល់' : 'បានបិទ'),
          (s.submitted_count > 0)
            ? h('span', { class: 'badge ready' }, `✓ បានប្រគល់ ${s.submitted_count}/${s.total_students || 0} នាក់`)
            : h('span', { class: 'badge draft' }, `មិនទាន់មានសិស្សប្រគល់`),
        ]),
        h('div', { class: 'muted', style: 'margin-top:4px;' }, `📅 ចាប់ផ្តើម៖ ${fmtDateTime(s.scheduled_start)} ➔ ម៉ោងបញ្ចប់៖ ${s.scheduled_end ? fmtDateTime(s.scheduled_end) : '—'} (${s.duration_minutes} នាទី)`),
        s.my_role === 'reviewer' ? null : h('div', { style: 'margin-top:6px;' }, [
          h('span', { class: 'muted' }, 'PIN សម្រាប់សិស្ស៖ '),
          s.pin ? h('span', { class: 'pin-chip' }, [s.pin]) : h('span', { class: 'badge draft' }, 'មិនមាន PIN'),
          h('button', { class: 'secondary btn-sm', style: 'margin-left:8px;', onclick: async () => {
            const next = prompt('PIN ថ្មី (អក្សរ ឬលេខ ៣–១២ តួ)៖', s.pin || '');
            if (next == null) return;
            try { await api(`/api/sessions/${s.id}/pin`, { method: 'POST', body: { pin: next } }); render.schedule(); }
            catch (e) { Exam.notify(e.message); }
          } }, 'ប្តូរ PIN'),
        ]),
      ]),
      h('div', { class: 'row', style: 'gap:6px;' }, [
        s.my_role === 'reviewer' ? null : h('button', { class: 'secondary btn-sm', title: 'កំណត់ពេលតេស្តនេះម្តងទៀត (ថ្នាក់ផ្សេង ឬប្រឡងជួសជុល)', onclick: () => { render.schedule(s.test_id); document.getElementById('sch-test')?.scrollIntoView({ behavior: 'smooth' }); } }, '↻ ប្រើម្តងទៀត'),
        h('button', { class: 'secondary btn-sm', title: 'ពិនិត្យថាតើការប្រឡងនេះរួចរាល់ឬនៅ', onclick: async () => {
          try { showReadiness(await api(`/api/sessions/${s.id}/readiness`), { viewOnly: true }); } catch (e) { Exam.notify(e.message); }
        } }, '📋 ពិនិត្យ'),
        h('button', { class: 'secondary btn-sm', onclick: () => {
          selectedSessionId = s.id;
          const tabs = document.querySelectorAll('.tabs button');
          tabs.forEach((b) => b.classList.toggle('active', b.dataset.tab === 'grading'));
          document.querySelectorAll('[id^="tab-"]').forEach((el) => { el.hidden = el.id !== 'tab-grading'; });
          render.grading();
        } }, 'ដាក់ពិន្ទុ'),
        s.my_role === 'reviewer' ? null : h('button', { class: 'danger btn-sm', onclick: async () => {
          if (!confirm(`តើលោកគ្រូពិតជាចង់លុបការកំណត់ពេលប្រឡង «${s.test_title} — ${s.class_name}» ឬ?`)) return;
          try {
            await api(`/api/sessions/${s.id}`, { method: 'DELETE' });
            render.schedule();
          } catch (e) { Exam.notify(e.message); }
        } }, 'លុប'),
      ]),
    ])),
  ]);

  const now = new Date();
  const pad = (n) => String(n).padStart(2, '0');
  const todayYMD = `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}`;
  const tomorrow = new Date(now.getTime() + 24 * 60 * 60 * 1000);
  const tomorrowYMD = `${tomorrow.getFullYear()}-${pad(tomorrow.getMonth() + 1)}-${pad(tomorrow.getDate())}`;
  let defStartH = now.getHours() + 1;
  if (defStartH >= 24) defStartH = 8;
  const defStartTime = `${pad(defStartH)}:00`;
  const defEndTime = minutesToTime(timeToMinutes(defStartTime) + 120);

  const dateInput = h('input', { type: 'date', id: 'sch-date', value: todayYMD, style: 'width: 100%;' });
  const startTimeInput = h('input', {
    type: 'text', id: 'sch-start-time', value: defStartTime, placeholder: '08:00',
    style: 'font-weight:600; font-family:monospace;'
  });
  const endTimeInput = h('input', {
    type: 'text', id: 'sch-end-time', value: defEndTime, placeholder: '10:00',
    style: 'font-weight:600; font-family:monospace;'
  });
  const durationInput = h('input', { type: 'number', id: 'sch-duration', value: '120' });

  // Sync Start Time, End Time and Duration:
  startTimeInput.addEventListener('input', () => {
    const sMins = timeToMinutes(startTimeInput.value);
    const dur = Number(durationInput.value) || 120;
    endTimeInput.value = minutesToTime(sMins + dur);
  });
  durationInput.addEventListener('input', () => {
    const sMins = timeToMinutes(startTimeInput.value);
    const dur = Number(durationInput.value) || 0;
    if (dur > 0) endTimeInput.value = minutesToTime(sMins + dur);
  });
  endTimeInput.addEventListener('input', () => {
    const sMins = timeToMinutes(startTimeInput.value);
    const eMins = timeToMinutes(endTimeInput.value);
    let diff = eMins - sMins;
    if (diff <= 0) diff += 24 * 60;
    if (diff > 0 && diff <= 1440) durationInput.value = diff;
  });

  const setSchedulePreset = (dStr, sStr, eStr, dur) => {
    dateInput.value = dStr;
    startTimeInput.value = sStr;
    endTimeInput.value = eStr;
    durationInput.value = dur;
  };

  const shortcuts = h('div', { class: 'time-shortcuts' }, [
    h('button', { type: 'button', class: 'time-pill', onclick: () => {
      const curTime = `${pad(now.getHours())}:${pad(now.getMinutes())}`;
      setSchedulePreset(todayYMD, curTime, minutesToTime(timeToMinutes(curTime) + 120), 120);
    } }, '⚡ ឥឡូវនេះ (120 នាទី)'),
    h('button', { type: 'button', class: 'time-pill', onclick: () => setSchedulePreset(todayYMD, '08:00', '10:00', 120) }, 'ថ្ងៃនេះ 08:00 — 10:00'),
    h('button', { type: 'button', class: 'time-pill', onclick: () => setSchedulePreset(todayYMD, '14:00', '16:00', 120) }, 'ថ្ងៃនេះ 14:00 — 16:00'),
    h('button', { type: 'button', class: 'time-pill', onclick: () => setSchedulePreset(tomorrowYMD, '08:00', '10:00', 120) }, 'ថ្ងៃស្អែក 08:00 — 10:00'),
    h('button', { type: 'button', class: 'time-pill', onclick: () => setSchedulePreset(tomorrowYMD, '14:00', '16:00', 120) }, 'ថ្ងៃស្អែក 14:00 — 16:00'),
  ]);

  const integritySelect = h('select', { id: 'sch-integrity', style: 'min-width:260px;' }, [
    h('option', { value: 'lock', selected: 'selected' }, '🔒 តឹងរ៉ឹង — ជាប់សោ រហូតលោកគ្រូដោះសោ'),
    h('option', { value: 'warn' }, '⚠ ព្រមាន — លាក់សំណួរ ព្រមាន និងកត់ត្រា'),
    h('option', { value: 'log' }, '📝 កត់ត្រាតែប៉ុណ្ណោះ (មិនរំខានសិស្ស)'),
  ]);
  const maxViolInput = h('input', { type: 'number', id: 'sch-maxv', value: '3', min: '1', max: '20', style: 'width:70px;' });
  const randomPin = () => String(Math.floor(1000 + Math.random() * 9000));
  const pinInput = h('input', { type: 'text', id: 'sch-pin', value: randomPin(), maxlength: '12', style: 'font-weight:700;font-family:monospace;letter-spacing:3px;font-size:18px;' });

  const testOptions = tests.length === 0
    ? [h('option', { value: '', disabled: true, selected: true }, 'គ្មានតេស្តនៅឡើយទេ — សូមបង្កើតតេស្តជាមុនសិន')]
    : tests.map((t) => {
        const isSel = preSelectedTestId ? Number(t.id) === Number(preSelectedTestId) : false;
        const qCount = t.question_count != null ? `(${t.question_count} សំណួរ)` : '';
        const statusText = t.status === 'ready' ? '✓ រួចរាល់' : '✎ ព្រាង';
        return h('option', { value: t.id, selected: isSel ? true : null }, `${t.title} ${qCount} — ${statusText}`);
      });

  const form = h('div', { class: 'card' }, [
    h('h3', {}, 'កំណត់ពេលប្រឡងថ្មី'),
    tests.length === 0 ? h('p', { class: 'muted' }, 'សូមបង្កើតតេស្ត ១ នៅផ្ទាំង «តេស្ត» ជាមុនសិន។') : null,
    h('label', {}, 'តេស្ត (ជ្រើសរើសតេស្តចាស់ ឬតេស្តថ្មីដែលបានបង្កើត)'),
    h('select', { id: 'sch-test' }, testOptions),
    h('label', {}, 'ថ្នាក់'),
    h('select', { id: 'sch-class' }, classes.filter((c) => c.my_role !== 'reviewer').map((c) => h('option', { value: c.id }, c.name))),
    h('label', {}, 'កាលបរិច្ឆេទប្រឡង (Date)'),
    dateInput,
    h('div', { class: 'row', style: 'gap: 12px; margin-top: 8px;' }, [
      h('div', { style: 'flex: 1; min-width: 140px;' }, [
        h('label', { style: 'margin-top:0;' }, 'ម៉ោងចាប់ផ្តើម (Start Time)'),
        startTimeInput,
      ]),
      h('div', { style: 'flex: 1; min-width: 140px;' }, [
        h('label', { style: 'margin-top:0;' }, 'ម៉ោងបញ្ចប់ (End Time)'),
        endTimeInput,
      ]),
      h('div', { style: 'width: 130px;' }, [
        h('label', { style: 'margin-top:0;' }, 'រយៈពេល (នាទី)'),
        durationInput,
      ]),
    ]),
    shortcuts,
    h('label', {}, 'ការការពារភាពស្មោះត្រង់ (ចាកចេញពីទំព័រ ថតអេក្រង់ ប្រើ AI…)'),
    h('div', { class: 'row', style: 'gap:10px;align-items:center;flex-wrap:wrap;' }, [
      integritySelect,
      h('span', { class: 'muted' }, 'ជាប់សោបន្ទាប់ពី'), maxViolInput, h('span', { class: 'muted' }, 'លើកដែលមិនប្រក្រតី'),
    ]),
    h('label', {}, 'PIN សម្រាប់ការប្រឡងនេះ (សិស្សវាយ PIN នេះដើម្បីចូលប្រឡង)'),
    h('div', { class: 'row', style: 'flex-wrap:nowrap;' }, [
      pinInput,
      h('button', { type: 'button', class: 'secondary', title: 'ចៃដន្យ', onclick: () => { pinInput.value = randomPin(); } }, '🎲 ថ្មី'),
    ]),
    h('div', { class: 'row', style: 'margin-top:16px' }, [
      h('button', { onclick: async () => {
        const testId = Number(document.getElementById('sch-test').value);
        const classId = Number(document.getElementById('sch-class').value);
        if (!testId) { await Exam.notify('សូមជ្រើសរើសតេស្ត'); return; }
        if (!classId) { await Exam.notify('សូមជ្រើសរើសថ្នាក់'); return; }

        const dateVal = dateInput.value.trim();
        const startVal = startTimeInput.value.trim();
        const endVal = endTimeInput.value.trim();
        if (!dateVal || !startVal) { await Exam.notify('សូមបញ្ចូលថ្ងៃ និងម៉ោងចាប់ផ្តើម'); return; }

        const startDt = parseScheduleDateTime(dateVal, startVal);
        let endDt = endVal ? parseScheduleDateTime(dateVal, endVal) : new Date(startDt.getTime() + (Number(durationInput.value) || 120) * 60000);
        if (endDt <= startDt) {
          endDt = new Date(endDt.getTime() + 24 * 60 * 60 * 1000);
        }
        if (isNaN(startDt.getTime()) || isNaN(endDt.getTime())) {
          await Exam.notify('ម៉ោងមិនត្រឹមត្រូវទេ។ ឧទាហរណ៍៖ 08:00 ឬ 14:30');
          return;
        }

        const dur = Number(durationInput.value) || Math.round((endDt.getTime() - startDt.getTime()) / 60000) || 120;

        try {
          const rd = await api(`/api/readiness?${new URLSearchParams({ test_id: testId, class_id: classId, start: startDt.toISOString(), end: endDt.toISOString(), duration: dur, pin: pinInput.value.trim() })}`);
          if (!(await showReadiness(rd, { confirmLabel: 'កំណត់ពេលប្រឡង' }))) return;
        } catch (e) { return Exam.notify(e.message); }

        // If the selected test was a draft, promote it to ready so students can take it
        const targetTest = tests.find((t) => t.id === testId);
        if (targetTest && targetTest.status !== 'ready') {
          try {
            await api(`/api/tests/${testId}`, { method: 'PUT', body: { status: 'ready' } });
          } catch {}
        }

        await api('/api/sessions', { method: 'POST', body: {
          test_id: testId,
          class_id: classId,
          scheduled_start: startDt.toISOString(),
          scheduled_end: endDt.toISOString(),
          duration_minutes: dur,
          pin: pinInput.value.trim(),
          integrity_mode: integritySelect.value, max_violations: Number(maxViolInput.value) || 3,
        } });
        await Exam.notify('បានកំណត់ពេលប្រឡងជោគជ័យ! សូមប្រាប់សិស្សពី PIN: ' + pinInput.value.trim());
        render.schedule();
      } }, 'កំណត់ពេល'),
    ]),
  ]);

  container.append(list, form);
};

// ---------- Grading ----------
let selectedSessionId = null;

function exportSessionToExcel(session) {
  if (typeof XLSX === 'undefined') {
    Exam.notify('មិនទាន់ដំណើរការបណ្ណាល័យ Excel នៅឡើយទេ។');
    return;
  }
  const headers = ['ល.រ', 'អត្តលេខ', 'គោត្តនាម', 'នាម', 'ភេទ', 'ពេលចូលប្រឡង', 'ពេលប្រគល់', 'របៀបប្រគល់', 'ពិន្ទុ MCQ', 'ពិន្ទុសរសេរ', 'ពិន្ទុសរុប', 'ពិន្ទុអតិបរមា', 'ភាគរយ', 'និទ្ទេស'];
  const rows = [headers];

  session.roster.forEach((s, idx) => {
    const mcq = s.submitted_at ? (s.mcq_score ?? 0) : 0;
    const writing = s.writing_score != null ? s.writing_score : 0;
    const writingMax = s.writing_max != null ? s.writing_max : 0;
    const total = mcq + writing;
    const maxTotal = (session.mcq_max || 0) + writingMax;
    const pct = maxTotal > 0 ? Math.round((total / maxTotal) * 100) : 0;

    let grade = 'F';
    if (pct >= 85) grade = 'A';
    else if (pct >= 75) grade = 'B';
    else if (pct >= 65) grade = 'C';
    else if (pct >= 50) grade = 'D';
    else if (pct >= 40) grade = 'E';

    let submitLabel = 'មិនបានចូល';
    if (s.submitted_at) {
      submitLabel = s.submit_type === 'auto' ? 'ស្វ័យប្រវត្តិ (Auto-submit)' : s.submit_type === 'paper' ? 'ស្កេនក្រដាស (OMR)' : 'ដាក់ផ្ទាល់ (Manual)';
    } else if (s.started_at) {
      submitLabel = `កំពុងប្រឡង (${s.answered_count || 0} សំណួរ)`;
    }

    rows.push([
      idx + 1,
      s.id,
      s.surname,
      s.first_name,
      s.gender || '—',
      s.started_at ? fmtDateTime(s.started_at) : '—',
      s.submitted_at ? fmtDateTime(s.submitted_at) : (s.started_at ? 'កំពុងប្រឡង' : '—'),
      submitLabel,
      s.submitted_at ? mcq : '—',
      s.writing_score != null ? writing : '—',
      s.submitted_at || s.writing_score != null ? total : '—',
      maxTotal,
      (s.submitted_at || s.writing_score != null) ? `${pct}%` : '—',
      (s.submitted_at || s.writing_score != null) ? grade : '—',
    ]);
  });

  const ws = XLSX.utils.aoa_to_sheet(rows);
  ws['!cols'] = [
    { wch: 6 }, { wch: 14 }, { wch: 14 }, { wch: 14 }, { wch: 8 },
    { wch: 18 }, { wch: 18 }, { wch: 22 },
    { wch: 12 }, { wch: 14 }, { wch: 12 }, { wch: 14 }, { wch: 10 }, { wch: 8 }
  ];
  const wb = XLSX.utils.book_new();
  const cleanTitle = (session.class_name || 'លទ្ធផល').replace(/[\/:*?"<>|]/g, '_');
  XLSX.utils.book_append_sheet(wb, ws, cleanTitle);
  XLSX.writeFile(wb, `លទ្ធផល_${session.test_title}_${session.class_name}.xlsx`);
}

render.grading = async function () {
  const container = document.getElementById('tab-grading');
  container.innerHTML = '';
  if (selectedSessionId) return renderGradingSession(container);

  const { sessions } = await api('/api/sessions');
  const card = h('div', { class: 'card' }, [
    h('h2', {}, 'ជ្រើសរើសការប្រឡងសម្រាប់ដាក់ពិន្ទុ'),
    sessions.length === 0 ? h('p', { class: 'muted' }, 'មិនទាន់មានការកំណត់ពេលប្រឡងនៅឡើយទេ។') : null,
    ...sessions.map((s) => h('div', { class: 'list-item' }, [
      h('div', {}, [
        h('div', { class: 'row', style: 'gap:8px;align-items:center;flex-wrap:wrap;' }, [
          h('strong', {}, `${s.test_title} — ${s.class_name}`),
          h('span', { class: `badge ${s.phase}` }, s.phase === 'open' ? 'កំពុងប្រឡង' : s.phase === 'upcoming' ? 'នឹងមកដល់' : 'បានបិទ'),
          (s.submitted_count > 0)
            ? h('span', { class: 'badge ready' }, `✓ បានប្រគល់ ${s.submitted_count}/${s.total_students || 0} នាក់`)
            : h('span', { class: 'badge draft' }, `មិនទាន់មានសិស្សប្រគល់`),
        ]),
        h('div', { class: 'muted', style: 'margin-top:4px;' }, `📅 ចាប់ផ្តើម៖ ${fmtDateTime(s.scheduled_start)} ➔ ម៉ោងបញ្ចប់៖ ${s.scheduled_end ? fmtDateTime(s.scheduled_end) : '—'} (${s.duration_minutes} នាទី)`),
      ]),
      h('button', { class: 'secondary btn-sm', onclick: () => { selectedSessionId = s.id; render.grading(); } }, 'បើកដាក់ពិន្ទុ'),
    ])),
  ]);
  container.append(card);
};

render.overview = async function () {
  const container = document.getElementById('tab-overview');
  container.innerHTML = '';
  const { sessions } = await api('/api/overview');
  if (sessions.length === 0) {
    container.append(h('div', { class: 'card' }, h('p', { class: 'muted' }, 'មិនទាន់មានការប្រឡងនៅឡើយទេ។')));
    return;
  }
  const byTest = {};
  for (const s of sessions) (byTest[s.test_title] ||= []).push(s);
  const phaseLabel = (p) => (p === 'open' ? 'កំពុងប្រឡង' : p === 'upcoming' ? 'នឹងមកដល់' : 'បានបិទ');
  for (const [title, list] of Object.entries(byTest)) {
    const tot = list.reduce((a, s) => a + s.submitted, 0);
    const avgAll = tot ? Math.round(list.reduce((a, s) => a + (s.avg_pct || 0) * s.submitted, 0) / tot) : null;
    container.append(h('div', { class: 'card', style: 'overflow-x:auto;' }, [
      h('h2', {}, title),
      h('div', { class: 'muted', style: 'margin-bottom:8px;' }, avgAll == null ? 'មិនទាន់មានលទ្ធផល' : `មធ្យមភាគរួម ${avgAll}% (សិស្សបានប្រគល់ ${tot} នាក់)`),
      h('table', {}, [
        h('thead', {}, h('tr', {}, ['ថ្នាក់', 'ពេលប្រឡង', 'ស្ថានភាព', 'ប្រគល់', 'មធ្យមភាគ', 'ខ្ពស់បំផុត', 'ទាបបំផុត', 'ជាប់ (≥50%)', ''].map((t) => h('th', {}, t)))),
        h('tbody', {}, list.map((s) => h('tr', {}, [
          h('td', {}, h('strong', {}, s.class_name)),
          h('td', { style: 'white-space:nowrap;' }, fmtDateTime(s.scheduled_start)),
          h('td', {}, h('span', { class: `badge ${s.phase}` }, phaseLabel(s.phase))),
          h('td', {}, `${s.submitted}/${s.total_students}`),
          h('td', {}, s.avg_pct == null ? '—' : `${s.avg_pct}%`),
          h('td', {}, s.max_pct == null ? '—' : `${s.max_pct}%`),
          h('td', {}, s.min_pct == null ? '—' : `${s.min_pct}%`),
          h('td', {}, s.submitted ? `${s.pass_count}/${s.submitted}` : '—'),
          h('td', {}, h('button', { class: 'secondary btn-sm', onclick: () => {
            selectedSessionId = s.id;
            document.querySelector('.tabs button[data-tab="grading"]').click();
          } }, 'បើក')),
        ]))),
      ]),
    ]));
  }
};

let gradingRefreshTimer = null;

async function renderAnalysis(session) {
  const data = await api(`/api/sessions/${session.id}/analysis`);
  const letters = ['ក', 'ខ', 'គ', 'ឃ', 'ង', 'ច'];
  const isRight = (q, v) => (q.cancelled ? true : v != null && (v === q.correct_index || (q.alt_correct_index != null && v === q.alt_correct_index)));
  const students = session.roster.filter((s) => s.submitted_at && data.answers[s.id]);
  const n = students.length;

  // ----- per-question statistics: % right, discrimination (top vs bottom 27%), warnings
  const ranked = [...students].sort((x, y) => (y.mcq_score || 0) - (x.mcq_score || 0));
  const k = Math.max(1, Math.round(ranked.length * 0.27));
  const upper = ranked.slice(0, k), lower = ranked.slice(-k);
  const stats = data.questions.map((q) => {
    const rightN = students.filter((s) => isRight(q, data.answers[s.id][q.id])).length;
    const pct = n ? Math.round((rightN / n) * 100) : null;
    const rate = (grp) => (grp.length ? grp.filter((s) => isRight(q, data.answers[s.id][q.id])).length / grp.length : 0);
    const disc = n >= 12 ? rate(upper) - rate(lower) : null;
    const flags = [];
    if (q.cancelled) flags.push(['បានបោះបង់', 'chip-closed']);
    else if (pct != null && n >= 8) {
      if (pct < 25) flags.push(['⚠ ពិបាកពេក', 'chip-soon']);
      if (pct > 95) flags.push(['ងាយពេក', 'chip-plain']);
      if (disc != null && disc < 0.1 && pct >= 25 && pct <= 95) flags.push(['⚠ ពុំញែកសិស្សពូកែ/ខ្សោយ', 'chip-soon']);
      const wrongTop = q.counts.map((c, i) => [c, i]).filter(([, i]) => i !== q.correct_index && i !== q.alt_correct_index).sort((a, b) => b[0] - a[0])[0];
      if (wrongTop && wrongTop[0] > (q.counts[q.correct_index] || 0)) flags.push([`🔍 ពិនិត្យចម្លើយ — ជម្រើស ${letters[wrongTop[1]]} ត្រូវបានជ្រើសច្រើនជាង`, 'chip-soon']);
    }
    return { q, pct, disc, flags, rightN };
  });

  let sortMode = 'order';
  const qBody = h('tbody', {});
  function drawQuestions() {
    const rows = [...stats];
    if (sortMode === 'hard') rows.sort((a, b) => (a.pct ?? 101) - (b.pct ?? 101));
    qBody.innerHTML = '';
    rows.forEach(({ q, pct, disc, flags }) => {
      const color = pct == null ? 'var(--muted)' : pct >= 70 ? '#16a34a' : pct >= 40 ? '#d97706' : '#dc2626';
      qBody.append(h('tr', {}, [
        h('td', {}, q.order_no),
        mathEl('td', { style: 'max-width:300px;' }, q.stem_text),
        h('td', { style: 'white-space:nowrap;' }, q.options.map((_, i) =>
          h('span', { style: `margin-right:8px;${i === q.correct_index || i === q.alt_correct_index ? 'font-weight:700;color:#16a34a;' : ''}` }, `${letters[i] || i + 1}:${q.counts[i]}`))),
        h('td', { style: `font-weight:700;color:${color};white-space:nowrap;` }, pct == null ? '—' : `${pct}%`),
        h('td', { class: 'muted' }, disc == null ? '—' : disc.toFixed(2)),
        h('td', {}, h('div', { class: 'test-chips' }, flags.map(([t, c]) => h('span', { class: `chip ${c}` }, t)))),
      ]));
    });
  }
  const questionsCard = h('div', { class: 'card no-print', style: 'overflow-x:auto;' }, [
    h('div', { class: 'row', style: 'justify-content:space-between;' }, [
      h('h2', { style: 'margin:0;' }, '📊 ការវិភាគសំណួរ'),
      h('a', { class: 'btn secondary btn-sm', target: '_blank', href: `classreport.html?session=${session.id}` }, '🖨 របាយការណ៍ថ្នាក់'),
      h('div', { class: 'row', style: 'gap:6px;' }, [
        h('button', { class: 'secondary btn-sm', onclick: () => { sortMode = 'order'; drawQuestions(); } }, 'តាមលំដាប់'),
        h('button', { class: 'secondary btn-sm', onclick: () => { sortMode = 'hard'; drawQuestions(); } }, 'ពិបាកបំផុតមុន'),
      ]),
    ]),
    h('p', { class: 'muted' }, `% = សិស្សឆ្លើយត្រូវ (${n} នាក់ដែលបានប្រគល់)។ D = ភាពខុសគ្នារវាងសិស្សពូកែ ២៧% និងខ្សោយ ២៧% — ប្រសិនបើ D ទាបជិត ០ ឬអវិជ្ជមាន សំណួរនេះអាចមានបញ្ហា។`),
    h('table', {}, [
      h('thead', {}, h('tr', {}, ['ល.រ', 'សំណួរ', 'ចំនួនជ្រើសតាមជម្រើស', '% ត្រូវ', 'D', 'ចំណាំ'].map((t) => h('th', {}, t)))),
      qBody,
    ]),
  ]);
  drawQuestions();

  // ----- topic report: where is the class weak?
  const topics = {};
  for (const q of data.questions) {
    if (!q.topic || q.cancelled) continue;
    const t = (topics[q.topic] ||= { possible: 0, earned: 0, per: {} });
    for (const s of students) {
      const p = (t.per[s.id] ||= { possible: 0, earned: 0 });
      p.possible += q.points;
      if (isRight(q, data.answers[s.id][q.id])) { p.earned += q.points; t.earned += q.points; }
      t.possible += q.points;
    }
  }
  const topicRows = Object.entries(topics).map(([name, t]) => {
    const pct = t.possible ? Math.round((t.earned / t.possible) * 100) : 0;
    const weak = students.filter((s) => { const p = t.per[s.id]; return p && p.possible && p.earned / p.possible < 0.5; });
    return { name, pct, weak };
  }).sort((a, b) => a.pct - b.pct);
  const topicCard = topicRows.length ? h('div', { class: 'card no-print' }, [
    h('h2', {}, '📚 ចំណុចខ្សោយតាមប្រធានបទ'),
    h('p', { class: 'muted' }, 'រៀបតាមប្រធានបទដែលថ្នាក់ធ្វើបានតិចជាងគេមុន។ ចុចលើឈ្មោះដើម្បីឃើញសិស្សដែលទទួលបានក្រោម ៥០% ក្នុងប្រធានបទនោះ។'),
    ...topicRows.map((t) => {
      const col = t.pct >= 70 ? '#16a34a' : t.pct >= 50 ? '#d97706' : '#dc2626';
      const detail = h('div', { class: 'muted', hidden: 'hidden', style: 'margin:4px 0 10px;' }, t.weak.length ? `សិស្សដែលត្រូវការជំនួយ (${t.weak.length}): ${t.weak.map((s) => `${s.surname} ${s.first_name}`).join(' · ')}` : 'គ្មានសិស្សណាក្រោម ៥០% ទេ 🎉');
      return h('div', {}, [
        h('div', { class: 'topic-row', onclick: () => { detail.hidden = !detail.hidden; } }, [
          h('div', { style: 'flex:1;min-width:0;font-weight:600;' }, t.name),
          h('div', { class: 'bar', style: 'width:38%;' }, h('div', { class: 'bar-fill', style: `width:${t.pct}%;background:${col};` })),
          h('div', { style: `width:48px;text-align:right;font-weight:700;color:${col};` }, `${t.pct}%`),
          h('span', { class: `chip ${t.weak.length ? 'chip-soon' : 'chip-open'}`, style: 'margin-left:8px;' }, `${t.weak.length} នាក់`),
        ]),
        detail,
      ]);
    }),
  ]) : null;

  // ----- one student's answers
  const select = h('select', {}, [
    h('option', { value: '' }, '— ជ្រើសរើសសិស្ស —'),
    ...session.roster.filter((s) => data.answers[s.id]).map((s) => h('option', { value: s.id }, `${s.surname} ${s.first_name} (${s.id})`)),
  ]);
  const detail = h('div', { style: 'margin-top:10px;overflow-x:auto;' });
  select.onchange = () => {
    detail.innerHTML = '';
    const a = data.answers[select.value];
    if (!a) return;
    detail.append(h('table', {}, [
      h('thead', {}, h('tr', {}, ['ល.រ', 'សំណួរ', 'ចម្លើយសិស្ស', 'ចម្លើយត្រឹមត្រូវ', ''].map((t) => h('th', {}, t)))),
      h('tbody', {}, data.questions.map((q) => {
        const v = a[q.id];
        const ok = isRight(q, v);
        return h('tr', {}, [
          h('td', {}, q.order_no),
          mathEl('td', { style: 'max-width:300px;' }, q.stem_text),
          h('td', {}, v == null ? h('span', { class: 'muted' }, 'មិនបានឆ្លើយ') : letters[v] || String(v + 1)),
          h('td', {}, `${letters[q.correct_index] || String(q.correct_index + 1)}${q.alt_correct_index != null ? ` / ${letters[q.alt_correct_index]}` : ''}`),
          h('td', { style: `font-weight:700;color:${ok ? '#16a34a' : '#dc2626'};` }, ok ? '✓' : '✗'),
        ]);
      })),
    ]));
  };
  const studentCard = h('div', { class: 'card no-print', style: 'overflow-x:auto;' }, [h('h3', {}, 'ចម្លើយរបស់សិស្សម្នាក់ៗ'), select, detail]);

  return h('div', {}, [topicCard, questionsCard, studentCard]);
}

async function renderGradingSession(container) {
  const session = await api(`/api/sessions/${selectedSessionId}`);
  container.innerHTML = '';
  clearInterval(gradingRefreshTimer);
  if (session.phase === 'open') {
    // Watch the class live while the test is running.
    gradingRefreshTimer = setInterval(() => {
      if (!document.body.contains(container) || !selectedSessionId || !document.getElementById('bulk-writing-max')) {
        return clearInterval(gradingRefreshTimer);
      }
      renderGradingSession(container);
    }, 15000);
  }

  const totalStudents = session.roster.length;
  const participated = session.roster.filter((s) => s.submitted_at != null).length;
  const inProgress = session.roster.filter((s) => s.started_at != null && s.submitted_at == null).length;
  const publishedCount = session.roster.filter((s) => s.published_at != null).length;

  const headerCard = h('div', { class: 'card print-keep' }, [
    h('div', { class: 'row', style: 'justify-content:space-between;align-items:flex-start;' }, [
      h('div', {}, [
        h('h2', { style: 'margin-bottom:4px;' }, `${session.test_title} — ${session.class_name}`),
        h('div', { class: 'muted' }, `សម័យប្រឡង៖ ចាប់ផ្តើម ${fmtDateTime(session.scheduled_start)} ➔ ម៉ោងបញ្ចប់៖ ${session.scheduled_end ? fmtDateTime(session.scheduled_end) : '—'} (${session.duration_minutes} នាទី) · ពិន្ទុ MCQ អតិបរមា: ${session.mcq_max} ពិន្ទុ`),
        h('div', { class: 'row', style: 'margin-top:6px;gap:8px;' }, [
          session.pin ? h('span', { class: 'pin-chip no-print' }, [`PIN ${session.pin}`]) : null,
          h('span', { class: 'badge draft' }, `សិស្សសរុប៖ ${totalStudents} នាក់`),
          h('span', { class: 'badge ready' }, `បានប្រគល់៖ ${participated} នាក់`),
          inProgress > 0 ? h('span', { class: 'badge open' }, `កំពុងប្រឡង៖ ${inProgress} នាក់`) : null,
          publishedCount > 0 ? h('span', { class: 'badge' }, `បានប្រកាសលទ្ធផល៖ ${publishedCount} នាក់`) : null,
        ].filter(Boolean)),
      ]),
      h('button', { class: 'secondary no-print', style: 'font-weight:600;padding:6px 12px;', onclick: () => { selectedSessionId = null; render.grading(); } }, '← ត្រឡប់ទៅជ្រើសរើសសម័យប្រឡង'),
    ]),
  ]);

  // Where each student is in the marking workflow.
  const hasWriting = (session.writing_max_default || 0) > 0;
  const stageOf = (s) => (!s.submitted_at ? (s.started_at ? 'live' : 'absent')
    : s.published_at ? 'published' : (hasWriting && s.writing_score == null) ? 'needs' : 'ready');
  const STAGES = [
    ['needs', '✎ ត្រូវដាក់ពិន្ទុ', 'warn', 'បានប្រគល់ តែមិនទាន់មានពិន្ទុសរសេរ'],
    ['ready', '👁 ត្រៀមពិនិត្យ', 'ready', 'ពិន្ទុគ្រប់ហើយ រង់ចាំពិនិត្យ និងផ្សព្វផ្សាយ'],
    ['published', '📢 បានផ្សព្វផ្សាយ', 'open', 'សិស្សមើលឃើញលទ្ធផលហើយ'],
    ['live', '⏳ កំពុងប្រឡង', 'draft', 'មិនទាន់ប្រគល់'],
    ['absent', '— មិនបានចូល', 'draft', 'មិនទាន់ចូលប្រឡង'],
  ];
  const counts = Object.fromEntries(STAGES.map(([k]) => [k, session.roster.filter((s) => stageOf(s) === k).length]));
  const submittedN = counts.needs + counts.ready + counts.published;
  let stageFilter = null;
  const applyStageFilter = () => {
    tableCard.querySelectorAll('tbody tr').forEach((tr) => { tr.hidden = !!stageFilter && tr.dataset.stage !== stageFilter; });
    stageCard.querySelectorAll('.stage-chip').forEach((b) => b.classList.toggle('on', b.dataset.stage === stageFilter));
  };
  const seg = (k, color) => counts[k] ? h('div', { style: `flex:${counts[k]};background:${color};` }) : null;
  const stageCard = h('div', { class: 'card no-print stage-card' }, [
    h('div', { class: 'row', style: 'justify-content:space-between;align-items:center;' }, [
      h('h3', { style: 'margin:0;' }, 'ដំណើរការដាក់ពិន្ទុ'),
      h('span', { class: 'muted' }, submittedN ? `បានផ្សព្វផ្សាយ ${counts.published}/${submittedN}` : 'មិនទាន់មានសិស្សប្រគល់'),
    ]),
    h('div', { class: 'stage-bar' }, [seg('published', '#2e8b57'), seg('ready', '#2b6cb0'), seg('needs', '#d99a22'), seg('live', '#9aa5a0'), seg('absent', '#d9dedb')]),
    h('div', { class: 'row', style: 'gap:8px;flex-wrap:wrap;' }, STAGES.map(([k, label, , tip]) => h('button', {
      class: 'secondary btn-sm stage-chip', 'data-stage': k, title: tip, disabled: counts[k] ? null : 'disabled',
      onclick: () => { stageFilter = stageFilter === k ? null : k; applyStageFilter(); },
    }, `${label} · ${counts[k]}`))),
    counts.needs ? h('div', { class: 'callout warn', style: 'margin:10px 0 0;' }, `ជំហានបន្ទាប់៖ ដាក់ពិន្ទុសរសេរឱ្យសិស្ស ${counts.needs} នាក់ (ចុចប៊ូតុង «ត្រូវដាក់ពិន្ទុ» ដើម្បីបង្ហាញតែពួកគេ)។`)
      : counts.ready ? h('div', { class: 'callout good', style: 'margin:10px 0 0;' }, `ជំហានបន្ទាប់៖ មើលជាមុន រួចផ្សព្វផ្សាយលទ្ធផលឱ្យសិស្ស ${counts.ready} នាក់។`) : null,
  ]);

  const toolsCard = h('div', { class: 'card no-print' }, [
    h('div', { class: 'row', style: 'justify-content:space-between;align-items:center;' }, [
      h('div', { class: 'row', style: 'align-items:center;gap:8px;' }, [
        h('label', { style: 'margin:0;font-weight:600;' }, 'ពិន្ទុសរសេរអតិបរមា (Max Writing Points):'),
        h('input', { type: 'number', id: 'bulk-writing-max', placeholder: 'ឧ. 50', value: session.writing_max_default || '', style: 'width:90px;' }),
        h('button', { class: 'secondary btn-sm', onclick: () => {
          const val = document.getElementById('bulk-writing-max').value.trim();
          if (!val) return Exam.notify('សូមបញ្ចូលលេខពិន្ទុអតិបរមា។');
          const maxInputs = tableCard.querySelectorAll('.writing-max-input');
          maxInputs.forEach((inp) => { inp.value = val; });
          Exam.notify(`បានអនុវត្តពិន្ទុអតិបរមា ${val} ដល់សិស្សទាំងអស់។`);
        } }, 'អនុវត្តទាំងអស់'),
      ]),
      h('div', { class: 'row', style: 'gap:8px;' }, [
        session.phase !== 'closed' ? h('button', { class: 'secondary btn-sm', title: 'បន្ថែមពេលឱ្យថ្នាក់ទាំងមូល', onclick: async () => {
          const m = Number(prompt('បន្ថែមពេលប៉ុន្មាននាទីឱ្យថ្នាក់ទាំងមូល?', '5'));
          if (!m) return;
          try { await api(`/api/sessions/${selectedSessionId}/extend`, { method: 'POST', body: { minutes: m } }); await Exam.notify(`បានបន្ថែម ${m} នាទី។`); refresh(); } catch (e) { Exam.notify(e.message); }
        } }, '⏱ បន្ថែមពេលថ្នាក់') : null,
        h('button', { class: 'secondary btn-sm', title: 'គណនាពិន្ទុឡើងវិញតាមចម្លើយត្រឹមត្រូវបច្ចុប្បន្ន', onclick: async () => {
          try { const r = await api(`/api/sessions/${selectedSessionId}/rescore`, { method: 'POST' }); await Exam.notify(`បានគណនាឡើងវិញ៖ ផ្លាស់ប្តូរ ${r.changed} នាក់ ក្នុងចំណោម ${r.total}។`); refresh(); } catch (e) { Exam.notify(e.message); }
        } }, '🔄 រាប់ពិន្ទុឡើងវិញ'),
        h('a', { class: 'btn secondary btn-sm', href: `scan.html?session=${selectedSessionId}`, title: 'ស្កេនសន្លឹកចម្លើយ OMR នៃតេស្តលើក្រដាស' }, '📷 ស្កេនសន្លឹក OMR'),
        h('button', { class: 'secondary btn-sm', onclick: () => window.print() }, '🖨 បោះពុម្ពតារាងពិន្ទុ'),
        h('button', { class: 'secondary btn-sm', onclick: () => exportSessionToExcel(session) }, '📥 ទាញយកលទ្ធផលជា Excel (.xlsx)'),
      ]),
    ]),
  ]);

  const refresh = () => renderGradingSession(container);
  const liveButtons = (s) => {
    if (s.submitted_at || !(s.started_at || s.extra_minutes)) return [];
    const mini = 'padding:4px 8px;font-size:12px;';
    return [
      h('button', { class: 'secondary btn-sm', style: mini, title: 'បន្ថែមពេល ៥ នាទីឱ្យសិស្សនេះ', onclick: async () => { await api(`/api/sessions/${selectedSessionId}/extend`, { method: 'POST', body: { student_id: s.id, minutes: 5 } }); refresh(); } }, "+5'"),
      s.started_at ? h('button', { class: 'secondary btn-sm', style: mini, title: 'បញ្ជូនចម្លើយជំនួសសិស្ស', onclick: async () => {
        if (!(await Exam.confirm(`បញ្ជូនចម្លើយដែលបានរក្សាទុករបស់ ${s.surname} ${s.first_name} ជំនួសគាត់ឥឡូវនេះ?`))) return;
        try { await api(`/api/sessions/${selectedSessionId}/force-submit`, { method: 'POST', body: { student_id: s.id } }); refresh(); } catch (e) { Exam.notify(e.message); }
      } }, '⏹') : null,
      s.has_device ? h('button', { class: 'secondary btn-sm', style: mini, title: 'អនុញ្ញាតឱ្យសិស្សបន្តលើទូរស័ព្ទផ្សេង', onclick: async () => { await api(`/api/sessions/${selectedSessionId}/reset-device`, { method: 'POST', body: { student_id: s.id } }); Exam.notify('សិស្សអាចបន្តលើឧបករណ៍ផ្សេងបានហើយ។'); } }, '📱') : null,
    ].filter(Boolean);
  };

  const rows = session.roster.map((s, idx) => {
    const total = (s.mcq_score ?? 0) + (s.writing_score ?? 0);
    const maxTotal = session.mcq_max + (s.writing_max ?? 0);
    const pct = maxTotal > 0 ? Math.round((total / maxTotal) * 100) : 0;

    let grade = 'F';
    if (pct >= 85) grade = 'A';
    else if (pct >= 75) grade = 'B';
    else if (pct >= 65) grade = 'C';
    else if (pct >= 50) grade = 'D';
    else if (pct >= 40) grade = 'E';

    let statusBadge;
    if (s.submitted_at) {
      if (s.submit_type === 'auto') {
        statusBadge = h('span', { class: 'badge warn', title: 'ប្រព័ន្ធបញ្ជូនស្វ័យប្រវត្តដោយសារអស់ម៉ោង' }, '⏱ ផុតម៉ោង (Auto)');
      } else {
        statusBadge = h('span', { class: 'badge ready', title: 'សិស្សបានចុចប្រគល់ដោយខ្លួនឯង' }, '✓ ដាក់ផ្ទាល់ (Manual)');
      }
    } else if (s.started_at) {
      const seen = s.last_seen ? Date.parse(s.last_seen.replace(' ', 'T') + 'Z') : 0;
      const online = Date.now() - seen < 150000;
      statusBadge = h('span', { class: `badge ${online ? 'open' : 'warn'}`, title: online ? 'កំពុងតភ្ជាប់' : 'ហាក់បីដូចជាបាត់ការតភ្ជាប់' }, `${online ? '🟢' : '🟠'} កំពុងប្រឡង (${s.answered_count || 0})${s.extra_minutes ? ` · +${s.extra_minutes}'` : ''}`);
    } else {
      statusBadge = h('span', { class: 'badge draft' }, '⚪ មិនទាន់ចូល');
    }

    const resetBtn = s.submitted_at ? h('button', {
      class: 'secondary btn-sm',
      style: 'color:var(--warn);border-color:var(--warn);padding:4px 8px;font-size:12px;',
      title: 'អនុញ្ញាតឱ្យសិស្សចូលប្រឡងបន្តឡើងវិញ ប្រសិនបើសិស្សច្រឡំចុច Submit',
      onclick: async () => {
        if (!confirm(`តើលោកគ្រូពិតជាចង់អនុញ្ញាតឱ្យសិស្ស «${s.surname} ${s.first_name}» ចូលប្រឡងបន្តឡើងវិញឬ?

(ចម្លើយដែលសិស្សបានជ្រើសរើសពីមុន នៅតែរក្សាទុកដដែល ដោយសិស្សគ្រាន់តែចូលទៅធ្វើបន្ត)`)) return;
        try {
          await api(`/api/sessions/${selectedSessionId}/reset-student`, {
            method: 'POST',
            body: { student_id: s.id },
          });
          await Exam.notify(`បានអនុញ្ញាតឱ្យសិស្ស «${s.surname} ${s.first_name}» ចូលប្រឡងបន្តជោគជ័យ!`);
          renderGradingSession(container);
        } catch (e) {
          Exam.notify(e.message);
        }
      }
    }, '🔄 Reset') : null;

    const reportBtn = s.submitted_at ? h('a', { class: 'btn secondary btn-sm', style: 'padding:4px 8px;font-size:12px;', target: '_blank', href: `review.html?session=${selectedSessionId}&student=${encodeURIComponent(s.id)}`, title: 'របាយការណ៍ត្រូវ/ខុស របស់សិស្សនេះ' }, '📄') : null;

    return h('tr', { 'data-stage': stageOf(s) }, [
      h('td', { class: 'muted' }, idx + 1),
      h('td', {}, h('strong', {}, s.id)),
      h('td', {}, `${s.surname} ${s.first_name}`),
      h('td', { style: 'font-size:13px;white-space:nowrap;' }, s.started_at ? fmtTimeOnly(s.started_at) : h('span', { class: 'muted' }, '—')),
      h('td', { style: 'font-size:13px;white-space:nowrap;' }, s.submitted_at ? fmtTimeOnly(s.submitted_at) : (s.started_at ? h('span', { style: 'color:var(--brand);' }, 'កំពុងធ្វើ...') : h('span', { class: 'muted' }, '—'))),
      h('td', {}, statusBadge),
      h('td', { class: 'no-print', style: (s.tab_switches || 0) >= 3 ? 'color:#dc2626;font-weight:700;' : '' }, s.tab_switches ? `${s.tab_switches} ដង` : '—'),
      h('td', { class: 'no-print' }, (s.started_at || s.violations || s.note_count) ? h('button', {
        class: `secondary btn-sm incident-btn${s.locked ? ' locked' : s.violations >= 3 ? ' hot' : ''}`,
        title: 'មើលកំណត់ហេតុសកម្មភាព និងកំណត់ចំណាំ',
        onclick: () => openActivity(session, s, () => renderGradingSession(container)),
      }, `${s.locked ? '🔒 ' : s.violations ? '🚨 ' : '📋 '}${s.violations || 0}${s.away_ms ? ` · ${fmtAway(s.away_ms)}` : ''}${s.note_count ? ` · 📝${s.note_count}` : ''}`) : h('span', { class: 'muted' }, '—')),
      h('td', {}, s.submitted_at ? `${s.mcq_score} / ${session.mcq_max}` : h('span', { class: 'muted' }, '—')),
      h('td', {}, h('input', {
        type: 'number',
        value: s.writing_score ?? '',
        'data-student': s.id,
        class: 'writing-input',
        placeholder: '0',
        style: 'width:65px;padding:6px 6px;',
      })),
      h('td', {}, h('input', {
        type: 'number',
        value: s.writing_max ?? (session.writing_max_default || ''),
        'data-student-max': s.id,
        class: 'writing-max-input',
        placeholder: '50',
        style: 'width:65px;padding:6px 6px;',
      })),
      h('td', {}, (s.submitted_at || s.writing_score != null) ? h('strong', {}, String(total)) : '—'),
      h('td', {}, (s.submitted_at || s.writing_score != null) ? h('span', { class: `badge ${grade === 'F' ? 'closed' : 'ready'}` }, `${grade} (${pct}%)`) : '—'),
      h('td', { class: 'no-print' }, h('div', { class: 'row', style: 'gap:4px;flex-wrap:wrap;min-width:130px;' }, [
        ...liveButtons(s), reportBtn,
        session.writing_max_default && s.submitted_at ? h('button', { class: 'secondary btn-sm', style: 'padding:4px 8px;font-size:12px;', title: 'ដាក់ពិន្ទុសរសេរតាមសំណួរនីមួយៗ', onclick: () => openWritingMarks(session, s, () => renderGradingSession(container)) }, '✎') : null,
        resetBtn || (s.published_at ? h('span', { class: 'badge ready' }, 'ផ្សាយហើយ') : null),
      ])),
    ]);
  });

  const tableCard = h('div', { class: 'card', style: 'overflow-x:auto;' }, [
    h('table', {}, [
      h('thead', {}, h('tr', {}, [
        h('th', {}, 'ល.រ'),
        h('th', {}, 'អត្តលេខ'),
        h('th', {}, 'ឈ្មោះសិស្ស'),
        h('th', {}, 'ពេលចូល'),
        h('th', {}, 'ពេលប្រគល់'),
        h('th', {}, 'របៀបប្រគល់'),
        h('th', { class: 'no-print' }, 'ចាកចេញទំព័រ'),
        h('th', { class: 'no-print' }, 'សកម្មភាពគួរឱ្យសង្ស័យ'),
        h('th', {}, 'MCQ'),
        h('th', {}, 'សរសេរដៃ'),
        h('th', {}, 'សរសេរ (Max)'),
        h('th', {}, 'សរុប'),
        h('th', {}, 'និទ្ទេស'),
        h('th', {}, 'សកម្មភាព'),
      ])),
      h('tbody', {}, rows),
    ]),
    h('div', { class: 'row no-print', style: 'margin-top:16px;justify-content:flex-end;gap:10px;' }, [
      h('button', { onclick: async () => {
        const inputs = tableCard.querySelectorAll('.writing-input');
        const scores = [];
        for (const input of inputs) {
          const id = input.dataset.student;
          const maxInput = tableCard.querySelector(`.writing-max-input[data-student-max="${id}"]`);
          if (input.value !== '') {
            scores.push({
              student_id: id,
              writing_score: Number(input.value),
              writing_max: maxInput && maxInput.value !== '' ? Number(maxInput.value) : null,
            });
          }
        }
        if (scores.length === 0) return Exam.notify('មិនទាន់មានពិន្ទុសរសេរដែលត្រូវរក្សាទុកទេ។');
        try {
          const res = await api(`/api/sessions/${selectedSessionId}/writing-bulk`, {
            method: 'POST',
            body: { scores },
          });
          await Exam.notify(`បានរក្សាទុកពិន្ទុសរសេររបស់សិស្សចំនួន ${res.count} នាក់ដោយជោគជ័យ!`);
          renderGradingSession(container);
        } catch (e) {
          Exam.notify(e.message);
        }
      } }, '💾 រក្សាទុកពិន្ទុសរសេរ'),
      session.phase === 'closed'
        ? h('div', { class: 'row', style: 'gap:8px;' }, [
            publishedCount ? h('button', { class: 'secondary', onclick: async () => {
              if (!(await Exam.confirm('ដកលទ្ធផលចេញពីអេក្រង់សិស្ស? សិស្សនឹងលែងឃើញពិន្ទុរហូតដល់ផ្សព្វផ្សាយម្តងទៀត។'))) return;
              await api(`/api/sessions/${selectedSessionId}/unpublish`, { method: 'POST' });
              renderGradingSession(container);
            } }, '↩ ដកលទ្ធផលចេញ') : null,
            h('button', { class: 'secondary', onclick: () => openPublishPreview(selectedSessionId, () => renderGradingSession(container)) }, '👁 មើលជាមុន និងផ្សព្វផ្សាយ'),
          ])
        : h('button', { class: 'danger', onclick: async () => {
            if (!confirm('តើអ្នកពិតជាចង់បិទការប្រឡងនេះមុនពេលកំណត់ឬ?')) return;
            await api(`/api/sessions/${selectedSessionId}/close`, { method: 'POST' });
            await Exam.notify('បានបិទការប្រឡងជោគជ័យ!');
            renderGradingSession(container);
          } }, '🔒 បិទការប្រឡងឥឡូវនេះ'),
    ]),
  ]);

  if (session.my_role === 'reviewer') {
    tableCard.querySelectorAll('button').forEach((b) => b.remove());
    tableCard.querySelectorAll('input').forEach((i) => { i.disabled = true; });
    toolsCard.querySelectorAll('input, button:not([onclick*="Excel"])').forEach((b) => { if (!/Excel|PDF|បោះពុម្ព/.test(b.textContent)) b.disabled = true; });
    container.append(h('div', { class: 'notice' }, '👁 អ្នកជាអ្នកពិនិត្យ — មើលបានតែមិនអាចដាក់ពិន្ទុ ឬផ្សព្វផ្សាយលទ្ធផលបានទេ។'));
  }
  const polMode = h('select', {}, [['lock', '🔒 តឹងរ៉ឹង (ជាប់សោ)'], ['warn', '⚠ ព្រមាន'], ['log', '📝 កត់ត្រាតែប៉ុណ្ណោះ']].map(([v, l]) => h('option', { value: v, selected: session.integrity_mode === v ? 'selected' : null }, l)));
  const polMax = h('input', { type: 'number', min: '1', max: '20', value: session.max_violations || 3, style: 'width:70px;' });
  const lockedCount = session.roster.filter((x) => x.locked).length;
  const integrityCard = h('div', { class: 'card no-print' }, [
    h('div', { class: 'row', style: 'gap:10px;align-items:center;flex-wrap:wrap;' }, [
      h('strong', {}, '🛡 ការការពារភាពស្មោះត្រង់'), polMode, h('span', { class: 'muted' }, 'ជាប់សោបន្ទាប់ពី'), polMax, h('span', { class: 'muted' }, 'លើក'),
      h('button', { class: 'secondary btn-sm', onclick: async () => { try { await api(`/api/sessions/${selectedSessionId}/integrity`, { method: 'POST', body: { mode: polMode.value, max_violations: Number(polMax.value) } }); Exam.notify('បានរក្សាទុក — មានអនុភាពភ្លាមៗលើសិស្សដែលកំពុងប្រឡង។'); } catch (e) { Exam.notify(e.message); } } }, 'រក្សាទុក'),
      lockedCount ? h('span', { class: 'badge warn' }, `🔒 កំពុងជាប់សោ ${lockedCount} នាក់ — ចុចលើជួររបស់គេដើម្បីដោះសោ`) : null,
    ]),
  ]);
  container.append(headerCard, stageCard, integrityCard, toolsCard, tableCard);
  if (hasWriting && session.my_role !== 'reviewer' && session.roster.some((r) => r.submitted_at)) {
    try { container.append(await writingGridCard(session, refresh)); } catch { /* optional */ }
  }
  container.append(suspicionCard(session));
  try { container.append(await renderAnalysis(session)); } catch (e) { /* analysis is optional */ }
}

// ---------- mark one writing question down the whole class ----------
async function writingGridCard(session, onDone) {
  const d = await api(`/api/sessions/${session.id}/writing-marks`);
  const card = h('div', { class: 'card no-print' });
  if (!d.questions.length) return card;
  const students = session.roster.filter((s) => s.submitted_at);
  const marks = {};
  for (const m of d.marks) (marks[m.question_id] ||= {})[m.student_id] = m.score;
  let qi = 0;
  const draw = () => {
    const q = d.questions[qi];
    card.innerHTML = '';
    const inputs = students.map((s) => h('input', { type: 'number', step: '0.25', min: '0', max: String(q.points), inputmode: 'decimal', 'data-s': s.id, value: marks[q.id] && marks[q.id][s.id] != null ? marks[q.id][s.id] : '', style: 'width:80px;' }));
    const count = h('span', { class: 'muted' }, '');
    const update = () => { const n = inputs.filter((i) => i.value !== '').length; count.textContent = `បានដាក់ ${n}/${students.length} នាក់`; };
    inputs.forEach((inp, i) => {
      inp.addEventListener('input', update);
      inp.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === 'ArrowDown') { e.preventDefault(); (inputs[i + 1] || inp).focus(); (inputs[i + 1] || inp).select(); } else if (e.key === 'ArrowUp') { e.preventDefault(); (inputs[i - 1] || inp).focus(); } });
    });
    update();
    card.append(
      h('h2', { style: 'margin:0 0 6px;' }, '✎ ដាក់ពិន្ទុសរសេរតាមសំណួរ (លឿនជាង)'),
      h('p', { class: 'muted', style: 'margin:0 0 8px;' }, 'ដាក់ពិន្ទុសំណួរមួយ ឱ្យសិស្សទាំងអស់ជាប់គ្នា — ចុច Enter ដើម្បីទៅសិស្សបន្ទាប់។ ពិន្ទុសរុបត្រូវបានគណនាឱ្យដោយស្វ័យប្រវត្តិ។'),
      h('div', { class: 'row', style: 'gap:6px;flex-wrap:wrap;margin-bottom:8px;' }, d.questions.map((x, i) => h('button', { class: `secondary btn-sm${i === qi ? ' on' : ''}`, onclick: () => { qi = i; draw(); } }, `សំណួរ ${i + 1} (${x.points} ពិន្ទុ)`))),
      mathEl('div', { class: 'callout', style: 'white-space:pre-line;' }, q.stem_text),
      q.solution_text ? mathEl('div', { class: 'callout good', style: 'white-space:pre-line;' }, `ចម្លើយគំរូ៖ ${q.solution_text}`) : null,
      h('div', { style: 'max-height:380px;overflow:auto;border:1px solid var(--line);border-radius:6px;' }, h('table', {}, [
        h('thead', {}, h('tr', {}, ['ឈ្មោះ', `ពិន្ទុ (0–${q.points})`].map((t) => h('th', {}, t)))),
        h('tbody', {}, students.map((s, i) => h('tr', {}, [h('td', {}, `${s.surname} ${s.first_name}`), h('td', {}, inputs[i])]))),
      ])),
      h('div', { class: 'row', style: 'justify-content:space-between;margin-top:10px;' }, [count, h('button', { onclick: async () => {
        const scores = {}; for (const inp of inputs) scores[inp.dataset.s] = inp.value;
        try { await api(`/api/sessions/${session.id}/writing-grid`, { method: 'POST', body: { question_id: q.id, scores } }); await Exam.notify('បានរក្សាទុកពិន្ទុសំណួរនេះ។'); onDone(); } catch (e) { Exam.notify(e.message); }
      } }, '💾 រក្សាទុកសំណួរនេះ')]),
    );
  };
  draw();
  return card;
}

// ---------- indicators that something may be wrong ----------
function suspicionCard(session) {
  const out = h('div', {});
  return h('div', { class: 'card no-print' }, [
    h('div', { class: 'row', style: 'justify-content:space-between;' }, [h('h2', { style: 'margin:0;' }, '🔎 សូចនាករគួរឱ្យសង្ស័យ'), h('button', { class: 'secondary btn-sm', onclick: async (e) => {
      e.target.disabled = true; out.innerHTML = '';
      try {
        const d = await api(`/api/sessions/${session.id}/suspicion`);
        out.append(h('div', { class: 'callout warn' }, 'នេះគ្រាន់តែជាសញ្ញាប្រាប់ឱ្យពិនិត្យបន្ត មិនមែនជាភស្តុតាងទេ។ សិស្សពូកែអាចចប់លឿន ហើយសិស្សអង្គុយជិតគ្នាអាចខុសដូចគ្នាដោយចៃដន្យ។ សូមសួរសិស្សបន្ថែមមុនសម្រេចចិត្ត។'));
        const sec = (title, rows, line) => out.append(h('h3', { style: 'margin:12px 0 4px;' }, `${title} (${rows.length})`), rows.length ? h('div', {}, rows.map((r) => h('div', { class: 'callout', style: 'font-weight:500;' }, line(r)))) : h('div', { class: 'muted' }, 'មិនមានទេ។'));
        sec('ប្រគល់លឿនខុសធម្មតា ហើយពិន្ទុល្អ', d.fast, (r) => `${r.name} — ប្រើ ${r.minutes} នាទី ក្នុង ${r.of} នាទី · ពិន្ទុ ${r.pct}%`);
        sec('ឆ្លើយខុសដូចគ្នាច្រើនពេក', d.pairs, (r) => `${r.a_name} និង ${r.b_name} — ខុសដូចគ្នា ${r.same_wrong} ក្នុងចំណោមសំណួរដែលទាំងពីរខុស ${r.both_wrong}`);
        sec('សកម្មភាពមិនប្រក្រតីច្រើនពេលប្រឡង', d.incidents, (r) => `${r.name} — ${r.violations} លើក · ប្តូរផ្ទាំង ${r.tab_switches} ដង${r.pct != null ? ` · ពិន្ទុ ${r.pct}%` : ''}`);
      } catch (er) { out.append(h('div', { class: 'error' }, er.message)); }
      e.target.disabled = false;
    } }, 'ពិនិត្យឥឡូវនេះ')]),
    out,
  ]);
}

// ---------- activity during the exam ----------
const fmtAway = (ms) => (ms >= 60000 ? `${Math.floor(ms / 60000)}ន ${Math.round((ms % 60000) / 1000)}វ` : `${Math.round(ms / 1000)}វ`);
const EVENT_LABEL = {
  start: ['▶', 'ចាប់ផ្តើមប្រឡង'], tab_hidden: ['🔀', 'ប្តូរផ្ទាំង/កម្មវិធី'], window_blur: ['🪟', 'ចុចក្រៅទំព័រប្រឡង (អាចជា AI popup)'],
  fullscreen_exit: ['⛶', 'ចេញពីពេញអេក្រង់'], fullscreen_enter: ['⛶', 'ចូលពេញអេក្រង់'], split_view: ['◧', 'បែងចែកអេក្រង់/បង្រួមផ្ទាំង'],
  copy: ['📋', 'ព្យាយាមចម្លង'], cut: ['📋', 'ព្យាយាមកាត់'], contextmenu: ['🖱', 'ចុចស្តាំ/ចុចយូរ'], shortcut: ['⌨', 'ប៊ូតុងថតអេក្រង់/បោះពុម្ព/DevTools'],
  print: ['🖨', 'ព្យាយាមបោះពុម្ព'], devtools: ['🛠', 'បើក Developer Tools'], second_tab: ['🗗', 'បើកការប្រឡងក្នុងផ្ទាំងទីពីរ'], drag: ['✋', 'អូសអត្ថបទ'],
  second_device: ['📱', 'មានឧបករណ៍ផ្សេងព្យាយាមចូលប្រឡងជំនួស (ត្រូវបានបដិសេធ)'], online: ['🟢', 'មានអ៊ីនធឺណិតវិញ'], offline: ['🔴', 'ដាច់អ៊ីនធឺណិត'], focus_back: ['↩', 'ត្រឡប់មកវិញ'], locked: ['🔒', 'ជាប់សោ'], unlocked: ['🔓', 'ដោះសោ'],
};
async function openActivity(session, stu, onDone) {
  let d;
  try { d = await api(`/api/sessions/${session.id}/activity?student_id=${encodeURIComponent(stu.id)}`); } catch (e) { return Exam.notify(e.message); }
  const canEdit = session.my_role !== 'reviewer';
  const back = h('div', { class: 'modal-back', style: 'align-items:flex-start;overflow:auto;' });
  const close = () => { back.remove(); onDone(); };
  const reopen = () => { back.remove(); openActivity(session, stu, onDone); };
  const counted = d.events.filter((e) => e.counted).length;
  const away = d.events.filter((e) => e.kind === 'tab_hidden' || e.kind === 'window_blur').reduce((t, e) => t + (e.dur_ms || 0), 0);
  const note = h('textarea', { placeholder: 'កំណត់ចំណាំរបស់អ្នកត្រួតពិនិត្យ ឧ. «ឃើញកំពុងមើលទូរស័ព្ទទីពីរ ម៉ោង 9:12»', style: 'min-height:60px;' });
  back.append(h('div', { class: 'modal-box', style: 'margin:20px auto;max-width:640px;text-align:left;' }, [
    h('h2', { style: 'margin:0 0 4px;' }, `📋 ${stu.surname} ${stu.first_name}`),
    h('div', { class: 'muted', style: 'margin-bottom:10px;' }, `${session.test_title} · ${session.class_name}`),
    h('div', { class: 'review-summary' }, [
      h('div', { class: `review-stat ${counted ? 'bad' : 'good'}` }, [h('b', {}, String(counted)), 'ការរំលោភ']),
      h('div', { class: 'review-stat' }, [h('b', {}, away ? fmtAway(away) : '0'), 'ពេលចាកចេញសរុប']),
      h('div', { class: `review-stat ${d.result && d.result.locked ? 'warn' : ''}` }, [h('b', {}, d.result && d.result.locked ? '🔒' : '—'), d.result && d.result.locked ? 'កំពុងជាប់សោ' : 'មិនជាប់សោ']),
    ]),
    canEdit ? h('div', { class: 'row', style: 'gap:8px;margin-bottom:10px;' }, [
      d.result && d.result.locked
        ? h('button', { onclick: async () => { await api(`/api/sessions/${session.id}/lock`, { method: 'POST', body: { student_id: stu.id, locked: false } }); reopen(); } }, '🔓 ដោះសោឱ្យបន្តប្រឡង')
        : (stu.started_at && !stu.submitted_at ? h('button', { class: 'danger', onclick: async () => { await api(`/api/sessions/${session.id}/lock`, { method: 'POST', body: { student_id: stu.id, locked: true } }); reopen(); } }, '🔒 ចាក់សោសិស្សនេះ') : null),
    ]) : null,
    h('h3', {}, 'កំណត់ហេតុសកម្មភាព'),
    d.events.length ? h('div', { style: 'max-height:280px;overflow:auto;border:1px solid var(--line);border-radius:6px;' }, h('table', {}, [
      h('thead', {}, h('tr', {}, ['ម៉ោង', 'សកម្មភាព', 'រយៈពេល', ''].map((x) => h('th', {}, x)))),
      h('tbody', {}, d.events.map((e) => { const [ic, lb] = EVENT_LABEL[e.kind] || ['•', e.kind]; return h('tr', { style: e.counted ? 'background:#fdecec;' : '' }, [
        h('td', { style: 'white-space:nowrap;' }, fmtTimeOnly(e.at)), h('td', {}, [`${ic} ${lb}`, e.detail ? h('div', { class: 'muted', style: 'font-size:12px;' }, e.detail) : null]),
        h('td', {}, e.dur_ms ? fmtAway(e.dur_ms) : ''), h('td', {}, e.counted ? h('span', { class: 'badge closed' }, 'រាប់') : ''),
      ]); })),
    ])) : h('p', { class: 'muted' }, 'មិនមានសកម្មភាពមិនប្រក្រតីត្រូវបានកត់ត្រាទេ។'),
    h('h3', { style: 'margin-top:14px;' }, 'កំណត់ចំណាំ'),
    ...d.notes.map((n) => h('div', { class: 'callout', style: 'display:flex;justify-content:space-between;gap:8px;' }, [h('div', {}, [h('div', {}, n.body), h('div', { class: 'muted', style: 'font-size:12px;font-weight:400;' }, `${n.author || ''} · ${fmtDateTime(n.created_at)}`)]),
      canEdit ? h('button', { class: 'secondary btn-sm', onclick: async () => { await api(`/api/sessions/${session.id}/notes/${n.id}`, { method: 'DELETE' }); reopen(); } }, '✕') : null])),
    canEdit ? h('div', {}, [note, h('div', { class: 'row', style: 'justify-content:flex-end;margin-top:6px;' }, [h('button', { class: 'secondary btn-sm', onclick: async () => { if (!note.value.trim()) return; await api(`/api/sessions/${session.id}/notes`, { method: 'POST', body: { student_id: stu.id, body: note.value } }); reopen(); } }, '＋ បន្ថែមចំណាំ')])]) : null,
    h('div', { class: 'row', style: 'justify-content:space-between;margin-top:14px;' }, [h('button', { class: 'secondary', onclick: () => window.print() }, '🖨 បោះពុម្ព'), h('button', { onclick: close }, 'បិទ')]),
  ]));
  document.body.append(back);
}

// ---------- publish preview ----------
async function openPublishPreview(sessionId, onDone) {
  let pv;
  try { pv = await api(`/api/sessions/${sessionId}/publish-preview`); } catch (e) { return Exam.notify(e.message); }
  const tile = (n, label, cls = '') => h('div', { class: `review-stat ${cls}` }, [h('b', {}, String(n)), label]);
  const gradeOf = (p) => Exam.gradeOf(p);
  const ack = h('input', { type: 'checkbox', style: 'width:18px;height:18px;' });
  const back = h('div', { class: 'modal-back', style: 'align-items:flex-start;overflow:auto;' });
  const publishBtn = h('button', { disabled: pv.writing_missing ? 'disabled' : null, onclick: async () => {
    try {
      await api(`/api/sessions/${sessionId}/publish`, { method: 'POST' });
      back.remove();
      await Exam.notify(`បានផ្សព្វផ្សាយលទ្ធផលឱ្យសិស្ស ${pv.submitted} នាក់ជោគជ័យ!`);
      onDone();
    } catch (e) { Exam.notify(e.message); }
  } }, '📢 ផ្សព្វផ្សាយឥឡូវនេះ');
  ack.onchange = () => { publishBtn.disabled = !ack.checked; };
  back.append(h('div', { class: 'modal-box', style: 'margin:20px auto;max-width:640px;text-align:left;' }, [
    h('h2', { style: 'margin:0 0 10px;' }, '👁 មើលជាមុនមុនផ្សព្វផ្សាយ'),
    h('div', { class: 'review-summary' }, [
      tile(pv.submitted, 'បានប្រគល់', 'good'), tile(pv.absent, 'អវត្តមាន', pv.absent ? 'warn' : ''),
      tile(pv.avg_pct == null ? '—' : pv.avg_pct + '%', 'មធ្យម'), tile(pv.min_pct == null ? '—' : `${pv.min_pct}–${pv.max_pct}%`, 'ទាបបំផុត–ខ្ពស់បំផុត'),
    ]),
    pv.phase !== 'closed' ? h('div', { class: 'callout warn' }, '⚠ ការប្រឡងនៅមិនទាន់បិទ — សិស្សដែលមិនទាន់ប្រគល់នឹងត្រូវបានរាប់ពិន្ទុតាមចម្លើយដែលមាន។') : null,
    pv.writing_missing ? h('div', { class: 'callout bad' }, `✗ សិស្ស ${pv.writing_missing} នាក់មិនទាន់មានពិន្ទុសរសេរ — ពួកគេនឹងឃើញតែពិន្ទុ MCQ។`) : null,
    pv.already_published ? h('div', { class: 'callout' }, `សិស្ស ${pv.already_published} នាក់បានឃើញលទ្ធផលរួចហើយ។`) : null,
    pv.cancelled ? h('div', { class: 'callout' }, `មានសំណួរបោះបង់ ${pv.cancelled} — សិស្សទទួលពិន្ទុសំណួរទាំងនោះ។`) : null,
    h('div', { class: 'callout' + (pv.mcq_with_explanation ? '' : ' warn') }, `ការពន្យល់ចម្លើយ MCQ៖ ${pv.mcq_with_explanation}/${pv.mcq_total} សំណួរ — សិស្សនឹងឃើញការពន្យល់ក្រោយប្រកាស។`),
    h('p', { class: 'muted', style: 'margin:8px 0;' }, 'ចុច «មើលដូចសិស្ស» ដើម្បីបើករបាយការណ៍ដូចអ្វីដែលសិស្សនឹងឃើញយ៉ាងពិតប្រាកដ។'),
    h('div', { style: 'max-height:260px;overflow:auto;border:1px solid var(--line);border-radius:6px;' }, h('table', {}, [
      h('thead', {}, h('tr', {}, ['ឈ្មោះ', 'ពិន្ទុ', 'និទ្ទេស', ''].map((x) => h('th', {}, x)))),
      h('tbody', {}, pv.students.map((s) => { const g = gradeOf(s.pct); return h('tr', {}, [
        h('td', {}, [s.name, s.writing_missing ? h('span', { class: 'badge warn', style: 'margin-left:6px;' }, 'គ្មានពិន្ទុសរសេរ') : null]),
        h('td', {}, `${s.total}/${s.max}`), h('td', {}, g ? `${g.grade} (${s.pct}%)` : '—'),
        h('td', {}, h('a', { class: 'btn secondary btn-sm', target: '_blank', href: `review.html?session=${sessionId}&student=${encodeURIComponent(s.id)}` }, '👁 មើលដូចសិស្ស')),
      ]); })),
    ])),
    pv.writing_missing ? h('label', { style: 'display:flex;gap:8px;align-items:center;margin-top:12px;color:var(--ink);' }, [ack, 'ខ្ញុំយល់ព្រមផ្សព្វផ្សាយទាំងមិនទាន់មានពិន្ទុសរសេរគ្រប់គ្នា']) : null,
    h('div', { class: 'row', style: 'justify-content:flex-end;margin-top:14px;' }, [h('button', { class: 'secondary', onclick: () => back.remove() }, 'បោះបង់'), publishBtn]),
  ]));
  document.body.append(back);
}

boot();


// ---- reviewer notes under each question
function notesBlock(q, test, container) {
  const canResolve = test.my_role === 'owner' || test.my_role === 'editor';
  const open = (q.notes || []).filter((n) => !n.resolved).length;
  const wrap = h('div', { class: 'notes' }, []);
  for (const n of q.notes || []) {
    wrap.append(h('div', { class: `note${n.resolved ? ' done' : ''}` }, [
      h('div', {}, [h('b', {}, n.author), h('span', { class: 'muted' }, ` · ${fmtDateTime(n.created_at)}`), n.resolved ? h('span', { class: 'badge ready', style: 'margin-left:6px;' }, 'បានដោះស្រាយ') : null]),
      h('div', { style: 'white-space:pre-line;' }, n.body),
      h('div', { class: 'row', style: 'gap:6px;margin-top:4px;' }, [
        (canResolve || n.teacher_id === test.my_id)
          ? h('button', { class: 'secondary btn-sm', onclick: async () => { await api(`/api/notes/${n.id}/resolve`, { method: 'POST', body: { resolved: !n.resolved } }); renderTestBuilder(container); } }, n.resolved ? '↩ បើកវិញ' : '✓ ដោះស្រាយរួច')
          : null,
        (test.my_role === 'owner' || n.teacher_id === test.my_id)
          ? h('button', { class: 'note-del btn-sm', onclick: async () => { await api(`/api/notes/${n.id}`, { method: 'DELETE' }); renderTestBuilder(container); } }, 'លុប')
          : null,
      ]),
    ]));
  }
  const input = h('input', { type: 'text', placeholder: '💬 សរសេរចំណាំ ឬកំហុសដែលបានឃើញ…', style: 'flex:1;min-width:200px;' });
  const add = async () => {
    if (!input.value.trim()) return;
    try { await api(`/api/questions/${q.id}/notes`, { method: 'POST', body: { body: input.value } }); renderTestBuilder(container); }
    catch (e) { Exam.notify(e.message); }
  };
  input.addEventListener('keydown', (e) => { if (e.key === 'Enter') add(); });
  wrap.append(h('div', { class: 'row', style: 'margin-top:6px;' }, [input, h('button', { class: 'secondary btn-sm', onclick: add }, 'ផ្ញើចំណាំ')]));
  return h('div', {}, [open ? h('div', { class: 'badge warn', style: 'margin-top:6px;' }, `💬 ${open} ចំណាំមិនទាន់ដោះស្រាយ`) : null, wrap]);
}


// ---- per-question writing marks
async function openWritingMarks(session, student, done) {
  const { questions, marks } = await api(`/api/sessions/${selectedSessionId}/writing-marks`);
  const mine = Object.fromEntries(marks.filter((m) => m.student_id === student.id).map((m) => [m.question_id, m.score]));
  const inputs = questions.map((q) => h('input', { type: 'number', min: '0', max: String(q.points), step: 'any', value: mine[q.id] ?? '', style: 'width:90px;', 'data-q': q.id }));
  const total = h('strong', {}, '');
  const recount = () => { total.textContent = String(inputs.reduce((t, i) => t + (Number(i.value) || 0), 0)); };
  inputs.forEach((i) => i.addEventListener('input', recount));
  recount();
  const back = h('div', { class: 'modal-back', onclick: (e) => { if (e.target === back) back.remove(); } });
  back.append(h('div', { class: 'modal-box', style: 'text-align:left;max-width:460px;' }, [
    h('h2', {}, `✎ ពិន្ទុសរសេរ — ${student.surname} ${student.first_name}`),
    ...questions.map((q, i) => h('div', { class: 'list-item' }, [h('span', {}, `សំណួរ ខ${i + 1}  (ពេញ ${q.points})`), inputs[i]])),
    h('div', { class: 'list-item' }, [h('span', {}, 'សរុប'), h('span', {}, [total, ` / ${questions.reduce((t, q) => t + q.points, 0)}`])]),
    h('div', { class: 'row', style: 'justify-content:flex-end;margin-top:14px;' }, [
      h('button', { class: 'secondary', onclick: () => back.remove() }, 'បោះបង់'),
      h('button', { onclick: async () => {
        const body = { student_id: student.id, marks: Object.fromEntries(inputs.map((i) => [i.dataset.q, i.value])) };
        try { await api(`/api/sessions/${selectedSessionId}/writing-marks`, { method: 'POST', body }); back.remove(); done(); } catch (e) { Exam.notify(e.message); }
      } }, 'រក្សាទុក'),
    ]),
  ]));
  document.body.append(back);
}

// ---- edit an existing question (stem, options, answer key, tags, picture)
async function openQuestionEditor(q, test, container, onDone) {
  const done = onDone || (() => renderTestBuilder(container));
  const curr = await loadCurr();
  const gl = gradeLessonPicker(q.grade, q.lesson, curr, q.chapter);
  const isWriting = q.kind === 'writing';
  const stem = h('textarea', { style: 'min-height:90px;' }); stem.value = q.stem_text;
  const optInputs = (q.options || []).map((o) => { const i = h('input', { type: 'text' }); i.value = o; return i; });
  while (!isWriting && optInputs.length < 4) optInputs.push(h('input', { type: 'text', placeholder: 'ជម្រើសបន្ថែម' }));
  const letters = ['ក', 'ខ', 'គ', 'ឃ', 'ង', 'ច'];
  const correct = h('select', {}, optInputs.map((_, i) => h('option', { value: i, selected: i === q.correct_index ? 'selected' : null }, `ជម្រើស ${letters[i] || i + 1}`)));
  const alt = h('select', {}, [h('option', { value: '' }, '— គ្មាន —'), ...optInputs.map((_, i) => h('option', { value: i, selected: q.alt_correct_index === i ? 'selected' : null }, `ជម្រើស ${letters[i] || i + 1}`))]);
  const points = h('input', { type: 'number', value: q.points, style: 'width:90px;' });
  const topic = h('input', { type: 'text', list: 'topic-list', placeholder: 'ឧ. ប្រភាគ', value: q.topic || '' });
  const level = h('select', {}, [['', '— មិនកំណត់ —'], ['easy', 'ងាយ'], ['medium', 'មធ្យម'], ['hard', 'ពិបាក'], ['pisa', 'បែប PISA']].map(([v, l]) => h('option', { value: v, selected: (q.level || '') === v ? 'selected' : null }, l)));
  const shuffle = h('input', { type: 'checkbox', checked: q.shuffle ? 'checked' : null, style: 'width:18px;height:18px;' });
  const cancelled = h('input', { type: 'checkbox', checked: q.cancelled ? 'checked' : null, style: 'width:18px;height:18px;' });
  const solution = h('textarea', { style: 'min-height:70px;' }); solution.value = q.solution_text || '';
  const removeImg = h('input', { type: 'checkbox', style: 'width:18px;height:18px;' });
  const file = h('input', { type: 'file', accept: 'image/png,image/jpeg,image/webp,image/svg+xml' });
  const editVariants = variantsBlock(() => ({ stem_text: stem.value, options: optInputs.map((i) => i.value.trim()).filter(Boolean), solution_text: solution.value }), q.params || '');

  let target = stem; const track = (f) => f.addEventListener('focus', () => { target = f; });
  track(stem); optInputs.forEach(track);
  const back = h('div', { class: 'modal-back', style: 'align-items:flex-start;overflow:auto;', onclick: (e) => { if (e.target === back) back.remove(); } });
  const box = h('div', { class: 'modal-box', style: 'text-align:left;max-width:640px;margin:20px auto;' }, [
    h('div', { class: 'row', style: 'justify-content:space-between;align-items:center;margin-bottom:12px;' }, [h('h2', { style: 'margin:0;' }, '✏️ កែសំណួរ'), h('span', { class: 'chip chip-plain', style: 'font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-weight:700;color:#1e40af;background:#eff6ff;border:1px solid #bfdbfe;font-size:14px;' }, `ID: ${q.id}`)]),
    h('label', {}, 'អត្ថបទសំណួរ'), Exam.mathBar(() => target), stem, Exam.mathPreview(stem),
    q.image_key ? h('div', {}, [h('img', { src: `/api/images/${q.image_key}`, style: 'max-height:120px;display:block;margin:8px 0;' }), h('label', { style: 'display:flex;gap:8px;align-items:center;' }, [removeImg, 'ដករូបភាពនេះចេញ'])]) : null,
    h('label', {}, q.image_key ? 'ប្តូររូបភាពថ្មី (មិនចាំបាច់)' : 'រូបភាព (មិនចាំបាច់)'), file,
    !isWriting ? h('div', {}, [
      h('label', {}, 'ជម្រើសចម្លើយ (ទុកទទេដើម្បីមិនប្រើ)'), ...optInputs.flatMap((i) => [i, Exam.mathPreview(i)]),
      h('div', { class: 'row', style: 'gap:14px;align-items:flex-end;' }, [
        h('div', { style: 'flex:1;min-width:160px;' }, [h('label', {}, 'ចម្លើយត្រឹមត្រូវ'), correct]),
        h('div', { style: 'flex:1;min-width:160px;' }, [h('label', {}, 'ចម្លើយទី២ ដែលទទួលយក (មិនចាំបាច់)'), alt]),
      ]),
      h('label', { style: 'display:flex;gap:8px;align-items:center;margin-top:12px;color:var(--ink);' }, [shuffle, 'លាយលំដាប់ជម្រើសចម្លើយសម្រាប់សិស្សម្នាក់ៗ']),
      h('label', {}, 'ការពន្យល់ចម្លើយ (សិស្សឃើញក្រោយប្រកាសលទ្ធផល — មិនចាំបាច់)'), solution,
      editVariants.box,
    ]) : h('div', {}, [h('label', {}, 'ចម្លើយគំរូ / របៀបដាក់ពិន្ទុ'), solution]),
    h('div', { class: 'row', style: 'gap:14px;align-items:flex-end;margin-top:6px;' }, [
      h('div', {}, [h('label', {}, 'ពិន្ទុ'), points]),
      h('div', { style: 'flex:1;min-width:140px;' }, [h('label', {}, 'មុខវិជ្ជា / ប្រធានបទ'), topic]),
      h('div', {}, [h('label', {}, 'កម្រិត'), level]),
    ]),
    h('div', { class: 'row', style: 'gap:14px;align-items:flex-end;' }, [
      h('div', {}, [h('label', {}, 'ថ្នាក់'), gl.grade]),
      h('div', { style: 'flex:1;min-width:180px;' }, [h('label', {}, 'ជំពូក'), gl.chapter, gl.chDl]),
      h('div', { style: 'flex:1;min-width:180px;' }, [h('label', {}, 'មេរៀន'), gl.lesson, gl.dl])
    ]),
    !isWriting ? h('label', { style: 'display:flex;gap:8px;align-items:center;margin-top:12px;color:#a52a2a;' }, [cancelled, 'បោះបង់សំណួរនេះ — ឱ្យពិន្ទុដល់សិស្សទាំងអស់']) : null,
    test.frozen_sessions ? h('div', { class: 'callout', style: 'margin-top:12px;' }, `🔒 មានការប្រឡង ${test.frozen_sessions} ដែលបានចាប់ផ្តើមរួច ហើយបានរក្សាសំណួរដើមទុក។ ការកែអត្ថបទ ឬជម្រើស នឹងមិនប៉ះពាល់ការប្រឡងទាំងនោះទេ។ ការកែចម្លើយត្រឹមត្រូវ ឬបោះបង់សំណួរ (ដោយមិនប្តូរជម្រើស) នឹងអនុវត្តលើការប្រឡងទាំងនោះដែរ។`) : null,
    test.submissions ? h('div', { class: 'callout warn', style: 'margin-top:12px;' }, `⚠ តេស្តនេះមានសិស្ស ${test.submissions} នាក់បានប្រគល់រួចហើយ។ បើប្តូរចម្លើយត្រឹមត្រូវ ប្រព័ន្ធនឹងសួរឱ្យរាប់ពិន្ទុឡើងវិញ។`) : null,
    h('div', { class: 'row', style: 'justify-content:flex-end;margin-top:16px;' }, [
      h('button', { class: 'secondary', onclick: () => back.remove() }, 'បោះបង់'),
      h('button', { onclick: async () => {
        try {
          const body = { stem_text: stem.value, points: Number(points.value), topic: topic.value, level: level.value, ...gl.get() };
          body.solution_text = solution.value;
          if (!isWriting) {
            const options = optInputs.map((i) => i.value.trim());
            const used = options.map((o, i) => [o, i]).filter(([o]) => o);
            // keep indexes stable: drop only trailing empty options
            let last = options.length; while (last > 0 && !options[last - 1]) last--;
            const opts = options.slice(0, last);
            if (opts.some((o) => !o)) return Exam.notify('សូមកុំទុកជម្រើសទទេនៅចន្លោះ។ ជម្រើសទទេអាចនៅខាងចុងបានតែប៉ុណ្ណោះ។');
            body.options = opts; body.correct_index = Number(correct.value); body.alt_correct_index = alt.value === '' ? null : Number(alt.value);
            body.shuffle = shuffle.checked; body.cancelled = cancelled.checked; body.params = editVariants.params.value.trim();
          }
          if (removeImg.checked) body.image_key = null;
          if (file.files[0]) { const f = file.files[0]; body.image_key = (await api('/api/images', { method: 'POST', body: await f.arrayBuffer(), contentType: f.type })).key; }
          const r = await api(`/api/questions/${q.id}`, { method: 'PUT', body });
          back.remove();
          if (r.key_changed && r.submissions > 0 && await Exam.confirm(`ចម្លើយត្រឹមត្រូវត្រូវបានផ្លាស់ប្តូរ។ រាប់ពិន្ទុឡើងវិញសម្រាប់សិស្ស ${r.submissions} នាក់ដែលបានប្រគល់រួចហើយឬ?`)) {
            const rs = await api(`/api/tests/${test.id}/rescore`, { method: 'POST' });
            await Exam.notify(`បានគណនាឡើងវិញ៖ ពិន្ទុរបស់សិស្ស ${rs.changed} នាក់ត្រូវបានកែ។`);
          }
          done();
        } catch (e) { Exam.notify(e.message); }
      } }, 'រក្សាទុក'),
    ]),
  ]);
  back.append(box);
  document.body.append(back);
}

// Owner: red counter on the "Teachers" tab (and the page title) while teachers are waiting to be unlocked.
function setRequestBadge(n) {
  const tb = document.querySelector('[data-tab="teachers"]'); if (!tb) return;
  let b = tb.querySelector('.req-badge');
  if (!n) { if (b) b.remove(); document.title = document.title.replace(/^\(\d+\) /, ''); return; }
  if (!b) { b = h('span', { class: 'req-badge' }); tb.append(b); }
  b.textContent = n;
  document.title = `(${n}) ` + document.title.replace(/^\(\d+\) /, '');
}
let lastPending = null;
async function pollRequests() {
  try {
    const d = await api('/api/admin/unlock-requests');
    if (lastPending !== null && d.pending > lastPending) { try { new Audio('data:audio/wav;base64,UklGRiQAAABXQVZFZm10IBAAAAABAAEAESsAABErAAABAAgAZGF0YQAAAAA=').play(); } catch {} }
    lastPending = d.pending; setRequestBadge(d.pending);
  } catch {}
}
function startRequestBadge() { pollRequests(); setInterval(pollRequests, 45000); window.refreshRequestBadge = pollRequests; }
