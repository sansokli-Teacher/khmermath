// Teacher side of the live quiz: open a room, show the code on the projector, run the questions, see the podium.
let lvLessons = null, lvLast = null;
const lvKh = (n) => String(n).replace(/\d/g, (d) => '០១២៣៤៥៦៧៨៩'[d]);
// lessons are numbered 1.. (grade 7), 101.. (grade 8), 201.. (grade 9): show them as "8/3" in short lists
const lvLn = (n) => (n >= 100 ? `${lvKh(Math.floor(n / 100) + 7)}/${lvKh(n % 100)}` : lvKh(n));
const LV_COL = ['#e03131', '#1c7ed6', '#f08c00', '#2f9e44', '#ae3ec9', '#0c8599'];

render.live = async function () {
  const root = document.getElementById('tab-live');
  root.innerHTML = '';
  let data;
  try { data = await api('/api/game/admin'); } catch (e) { return root.appendChild(h('div', { class: 'error' }, e.message)); }
  const lessons = data.lessons;
  if (lvLessons === null) lvLessons = lessons.map((L) => L.n).slice(0, 1);
  const closed = data.config.games && data.config.games.live === false;

  root.appendChild(h('div', { class: 'card' }, [
    h('h3', { style: 'margin-top:0' }, '📱 ហ្គេមសំណួរផ្ទាល់លើទូរស័ព្ទសិស្ស'),
    h('p', { class: 'muted' }, 'សិស្សម្នាក់ៗចូលលេងលើទូរស័ព្ទរបស់ខ្លួនដោយលេខកូដ ៦ ខ្ទង់។ លោកគ្រូអ្នកគ្រូបង្ហាញសំណួរលើអេក្រង់ធំ សិស្សទាំងអស់ឆ្លើយក្នុងពេលតែមួយ ឆ្លើយត្រូវនិងលឿនបានពិន្ទុច្រើន។ ប្រើសំណួរក្នុង «សំណួរហ្គេម» ដូចគ្នា (ការកែក៏មានផលដែរ)។ សំណួរដែលអាចពិនិត្យដោយស្វ័យប្រវត្តិបាន (ជ្រើសរើស ពិត/មិនពិត និងចម្លើយជាចំនួន) ប៉ុណ្ណោះដែលត្រូវបានប្រើ។'),
    closed ? h('p', { class: 'error' }, 'ហ្គេមនេះត្រូវបានបិទ — សូមបើកក្នុង «សំណួរហ្គេម» ជាមុនសិន។') : null,
  ]));

  let classes = [];
  try { classes = (await api('/api/classes')).classes || []; } catch { classes = []; }
  if (!document.getElementById('lvx-css')) {
    const st = document.createElement('style'); st.id = 'lvx-css';
    st.textContent = `
.lvx { display: flex; flex-direction: column; gap: 14px; padding-bottom: 80px; }
.lvx-step { background: #fff; border: 1px solid var(--line); border-radius: 18px; padding: 16px 18px; box-shadow: 0 6px 18px rgba(16,42,67,.06); }
.lvx-step h3 { margin: 0 0 12px; display: flex; align-items: center; gap: 10px; font-size: 18px; }
.lvx-n { width: 30px; height: 30px; border-radius: 50%; display: inline-grid; place-items: center; background: var(--teal, #1f6f66); color: #fff; font-size: 15px; }
.lvx-modes { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
.lvx-mode { display: flex; flex-direction: column; align-items: center; gap: 4px; padding: 16px 10px; border-radius: 16px; border: 3px solid var(--line); background: #f7f9fb; cursor: pointer; font: inherit; color: inherit; text-align: center; }
.lvx-mode.on { border-color: var(--teal, #1f6f66); background: #e6f4f1; box-shadow: 0 0 0 3px #e6f4f1; }
.lvx-mode:disabled { opacity: .4; cursor: not-allowed; }
.lvx-ic { font-size: 38px; line-height: 1.1; } .lvx-mode b { font-size: 18px; } .lvx-mode small { color: #5f6f81; line-height: 1.5; }
.lvx-hw { display: flex; flex-wrap: wrap; gap: 10px 16px; align-items: center; margin-top: 12px; padding: 10px 12px; border-radius: 12px; background: #f1f6ff; }
.lvx-lessons { display: grid; grid-template-columns: repeat(auto-fill, minmax(230px, 1fr)); gap: 8px; }
.lvx-grade { grid-column: 1 / -1; margin: 8px 0 0; color: var(--teal, #1f6f66); border-bottom: 2px solid #e6f4f1; }
.lvx-lesson { display: flex; gap: 8px; align-items: center; padding: 9px 12px; border-radius: 12px; border: 2px solid var(--line); background: #f7f9fb; cursor: pointer; }
.lvx-lesson.on { border-color: var(--teal, #1f6f66); background: #e6f4f1; }
.lvx-lab { font-weight: 700; margin: 4px 0 6px; color: #3b4a5c; }
.lvx-chips { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 8px; }
.lvx-chips button { height: 44px; padding: 0 16px; border-radius: 99px; border: 2px solid var(--line); background: #f7f9fb; font: inherit; font-weight: 700; cursor: pointer; color: #3b4a5c; }
.lvx-chips button.on { background: var(--teal, #1f6f66); border-color: var(--teal, #1f6f66); color: #fff; }
.lvx-bar { position: sticky; bottom: 0; z-index: 20; display: flex; align-items: center; justify-content: space-between; gap: 12px; flex-wrap: wrap; padding: 12px 16px; border-radius: 16px 16px 0 0; background: #fff; border: 1px solid var(--line); box-shadow: 0 -8px 24px rgba(16,42,67,.14); }
.lvx-sum { font-weight: 700; color: #3b4a5c; }
.lvx-go { font-size: 19px; padding: 12px 30px; border-radius: 99px; }
@media (max-width: 700px) { .lvx-modes { grid-template-columns: 1fr; } .lvx-mode { flex-direction: row; text-align: left; gap: 12px; } .lvx-mode small { display: none; } }`;
    document.head.appendChild(st);
  }

  // ---- 1. how to play: three picture cards ----
  let modeVal = 'classic';
  const MODES = [['classic', '👩‍🏫', 'បែបថ្នាក់', 'គ្រូចេញសំណួរម្តងមួយៗលើអេក្រង់ធំ សិស្សទាំងអស់ឆ្លើយព្រមគ្នា'], ['solo', '🧘', 'បែបសុខសាន្ត', 'សិស្សលេងតាមល្បឿនខ្លួន គ្មានគ្រូគ្រប់គ្រង'], ['hw', '📚', 'កិច្ចការផ្ទះ', 'ឱ្យថ្នាក់មួយលេងមុនថ្ងៃផុតកំណត់ ពិន្ទុត្រូវរក្សាទុក']];
  const modeBtns = MODES.map(([v, ic, t, d]) => {
    const b = h('button', { type: 'button', class: 'lvx-mode', onclick: () => { modeVal = v; sync(); } }, [h('span', { class: 'lvx-ic' }, ic), h('b', {}, t), h('small', {}, d)]);
    b.dataset.v = v; return b;
  });
  if (!classes.length) modeBtns[2].disabled = true;

  // ---- 2. lessons as chips ----
  const boxes = lessons.map((L) => {
    const cb = h('input', { type: 'checkbox' }); cb.checked = lvLessons.includes(L.n);
    const lab = h('label', { class: 'lvx-lesson' + (cb.checked ? ' on' : '') }, [cb, h('span', {}, [h('b', {}, `មេរៀនទី ${lvKh(L.d || L.n)} `), L.title])]);
    lab.dataset.g = String(L.g || 7);
    cb.onchange = () => { lvLessons = lessons.filter((x, i) => boxes[i].cb.checked).map((x) => x.n); lab.classList.toggle('on', cb.checked); sync(); };
    return { cb, lab };
  });
  const all = h('button', { class: 'secondary btn-sm', type: 'button', onclick: () => { boxes.forEach((b) => { b.cb.checked = true; b.lab.classList.add('on'); }); lvLessons = lessons.map((x) => x.n); sync(); } }, 'ជ្រើសទាំងអស់');
  const none = h('button', { class: 'secondary btn-sm', type: 'button', onclick: () => { boxes.forEach((b) => { b.cb.checked = false; b.lab.classList.remove('on'); }); lvLessons = []; sync(); } }, 'មិនជ្រើស');

  // ---- 3. how many questions, how long ----
  let countVal = 15, secsVal = 30;
  const chips = (vals, get, set, fmt) => { const row = h('div', { class: 'lvx-chips' }); vals.forEach((v) => row.appendChild(h('button', { type: 'button', 'data-v': v, onclick: () => { set(v); sync(); } }, fmt(v)))); row.paint = () => [...row.children].forEach((b) => b.classList.toggle('on', Number(b.dataset.v) === get())); return row; };
  const countRow = chips([10, 15, 20, 30], () => countVal, (v) => { countVal = v; }, (v) => `${lvKh(v)} សំណួរ`);
  const secsRow = chips([15, 20, 30, 45, 60], () => secsVal, (v) => { secsVal = v; }, (v) => `${lvKh(v)} វិនាទី`);

  // homework: class + deadline
  const hwClass = h('select', {}, classes.map((c) => h('option', { value: c.id }, c.name)));
  const dl = new Date(Date.now() + 3 * 86400000); dl.setHours(20, 0, 0, 0);
  const hwDate = h('input', { type: 'datetime-local', value: new Date(dl - dl.getTimezoneOffset() * 60000).toISOString().slice(0, 16) });
  const hwBox = h('div', { class: 'lvx-hw' }, [h('label', {}, ['ថ្នាក់ ', hwClass]), h('label', {}, ['ផុតកំណត់ ', hwDate]), h('small', { class: 'muted' }, 'សិស្សចូលតាមគណនីខ្លួននៅ exam.khmermath.org/student ហើយឃើញកិច្ចការនៅទីនោះ។')]);

  const go = h('button', { type: 'button', class: 'lvx-go' }, '▶ បង្កើតបន្ទប់');
  const sum = h('div', { class: 'lvx-sum' });
  function sync() {
    modeBtns.forEach((b) => b.classList.toggle('on', b.dataset.v === modeVal));
    countRow.paint(); secsRow.paint(); hwBox.style.display = modeVal === 'hw' ? '' : 'none';
    const m = MODES.find((x) => x[0] === modeVal);
    sum.textContent = `${m[1]} ${m[2]} · មេរៀន ${lvKh(lvLessons.length)} · ${lvKh(countVal)} សំណួរ · ${lvKh(secsVal)} វិនាទី`;
    go.disabled = !!closed || !lvLessons.length;
    go.textContent = modeVal === 'hw' ? '📚 ចេញកិច្ចការផ្ទះ' : '▶ បង្កើតបន្ទប់';
  }
  go.onclick = async () => {
    if (!lvLessons.length) return Exam.notify('សូមជ្រើសមេរៀនយ៉ាងហោចណាស់ ១។');
    go.disabled = true;
    try {
      const body = { lessons: lvLessons, count: countVal, secs: secsVal, mode: modeVal === 'classic' ? 'classic' : 'solo' };
      if (modeVal === 'hw') { body.class_id = Number(hwClass.value); body.deadline = new Date(hwDate.value).getTime(); }
      const r = await api('/api/live/create', { method: 'POST', body });
      lvLast = r.code;
      if (r.homework) { Exam.notify('បានបង្កើតកិច្ចការផ្ទះ — សិស្សឃើញវានៅក្នុងគណនីរបស់ខ្លួន។'); render.live(); } else lvHost(r.code);
    } catch (e) { Exam.notify(e.message); } finally { sync(); }
  };
  const step = (n, title, ...kids) => h('section', { class: 'lvx-step' }, [h('h3', {}, [h('span', { class: 'lvx-n' }, n), ' ', title]), ...kids]);
  root.appendChild(h('div', { class: 'lvx' }, [
    step('១', 'ជ្រើសរបៀបលេង', h('div', { class: 'lvx-modes' }, modeBtns), hwBox),
    step('២', 'ជ្រើសមេរៀន', h('div', { class: 'lvx-lessons' }, boxes.flatMap((b, i) => { const gg = b.lab.dataset.g; return i === 0 || boxes[i - 1].lab.dataset.g !== gg ? [h('h4', { class: 'lvx-grade' }, `ថ្នាក់ទី ${lvKh(gg)}`), b.lab] : [b.lab]; })), h('div', { class: 'row', style: 'gap:8px;margin-top:8px' }, [all, none])),
    step('៣', 'ចំនួនសំណួរ និងម៉ោង', h('div', { class: 'lvx-lab' }, 'ចំនួនសំណួរ'), countRow, h('div', { class: 'lvx-lab' }, 'ម៉ោងក្នុងមួយសំណួរ'), secsRow),
    h('div', { class: 'lvx-bar' }, [sum, h('div', { class: 'row', style: 'gap:8px;align-items:center' }, [lvLast ? h('button', { class: 'secondary btn-sm', type: 'button', onclick: () => lvHost(lvLast) }, `បើកបន្ទប់ ${lvLast} វិញ`) : null, go])]),
  ]));
  sync();

  // ---- history of every room: results survive after the room closes ----
  const hist = h('div', { class: 'card' }, [h('h3', { style: 'margin-top:0' }, '📊 ប្រវត្តិហ្គេម និងលទ្ធផល'), h('p', { class: 'muted' }, 'កំពុងផ្ទុក…')]);
  root.appendChild(hist);
  try {
    const { rooms } = await api('/api/live/history');
    hist.lastChild.remove();
    if (!rooms.length) hist.appendChild(h('p', { class: 'muted' }, 'មិនទាន់មានហ្គេមនៅឡើយទេ។'));
    else hist.appendChild(h('div', { style: 'overflow:auto' }, [h('table', { class: 'tbl', style: 'width:100%' }, [
      h('thead', {}, [h('tr', {}, ['ថ្ងៃ', 'កូដ', 'របៀប', 'ថ្នាក់/មេរៀន', 'អ្នកលេង', 'ពិន្ទុមធ្យម', ''].map((x) => h('th', {}, x)))]),
      h('tbody', {}, rooms.map((r) => h('tr', {}, [
        h('td', {}, new Date(r.created_at).toLocaleString('km-KH', { dateStyle: 'short', timeStyle: 'short' })), h('td', {}, r.code),
        h('td', {}, (r.mode === 'solo' ? (r.class_id ? '📚 កិច្ចការផ្ទះ' : '🧘 សុខសាន្ត') : '👩‍🏫 ថ្នាក់') + (r.over ? '' : ' · កំពុងបើក')),
        h('td', {}, `${r.class_name ? r.class_name + ' · ' : ''}មេរៀន ${(r.lessons || []).map(lvLn).join(', ')}`),
        h('td', {}, `${lvKh(r.players)}${r.mode === 'solo' ? ` (ចប់ ${lvKh(r.finished)})` : ''}`), h('td', {}, lvKh(r.avg_score)),
        h('td', {}, h('button', { class: 'secondary btn-sm', type: 'button', onclick: () => lvResults(r.code) }, 'មើលលទ្ធផល')),
      ]))),
    ])]));
  } catch (e) { hist.lastChild.textContent = e.message; }
};

// per-question results (what to re-teach) + every student's score
async function lvResults(code) {
  let d; try { d = await api(`/api/live/history/${code}`); } catch (e) { return Exam.notify(e.message); }
  document.querySelectorAll('.lvr').forEach((e) => e.remove());
  const ov = h('div', { class: 'lvr', style: 'position:fixed;inset:0;z-index:85;background:rgba(10,20,30,.55);display:flex;align-items:flex-start;justify-content:center;overflow:auto;padding:20px' });
  const box = h('div', { class: 'card', style: 'width:min(980px,100%);margin:0' });
  const qs = [...d.questions].sort((a, b) => (a.pct ?? 101) - (b.pct ?? 101));
  const mathCell = (t) => { const e = h('span', {}); e.innerHTML = Exam.mathHtml(t); return e; };
  box.appendChild(h('div', { style: 'display:flex;justify-content:space-between;gap:10px;align-items:center' }, [h('h3', { style: 'margin:0' }, `លទ្ធផលបន្ទប់ ${code}`), h('div', { style: 'display:flex;gap:8px' }, [
    h('button', { class: 'secondary btn-sm', type: 'button', onclick: () => {
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, XLSX.utils.aoa_to_sheet([['ល.រ', 'ឈ្មោះ', 'អត្តលេខ', 'ពិន្ទុ', 'សំណួរដែលបានធ្វើ'], ...d.players.map((p, i) => [i + 1, p.name, p.student_id || '', p.score, p.cur])]), 'សិស្ស');
      XLSX.utils.book_append_sheet(wb, XLSX.utils.aoa_to_sheet([['សំណួរ', 'ចម្លើយត្រឹមត្រូវ', 'បានឆ្លើយ', 'ត្រូវ', '% ត្រូវ', 'វិនាទីមធ្យម'], ...d.questions.map((q) => [q.q, q.show, q.answered, q.right, q.pct ?? '', q.avg_sec ?? ''])]), 'សំណួរ');
      XLSX.writeFile(wb, `លទ្ធផលហ្គេម_${code}.xlsx`); } }, '⬇ Excel'),
    h('button', { class: 'secondary btn-sm', type: 'button', onclick: () => ov.remove() }, '✕ បិទ')])]));
  box.appendChild(h('h4', {}, 'សំណួរដែលសិស្សធ្វើខុសច្រើនបំផុត (ត្រូវរៀនឡើងវិញ)'));
  box.appendChild(h('div', { style: 'overflow:auto' }, [h('table', { class: 'tbl', style: 'width:100%' }, [
    h('thead', {}, [h('tr', {}, ['%ត្រូវ', 'សំណួរ', 'ចម្លើយត្រឹមត្រូវ', 'ឆ្លើយ'].map((x) => h('th', {}, x)))]),
    h('tbody', {}, qs.map((q) => h('tr', {}, [h('td', { style: `font-weight:800;color:${q.pct == null ? '#888' : q.pct < 50 ? '#c92a2a' : q.pct < 75 ? '#e67700' : '#2b8a3e'}` }, q.pct == null ? '—' : `${lvKh(q.pct)}%`), h('td', {}, mathCell(q.q)), h('td', {}, mathCell(q.show)), h('td', {}, lvKh(q.answered))]))),
  ])]));
  box.appendChild(h('h4', {}, 'ពិន្ទុរបស់សិស្ស'));
  box.appendChild(h('div', { style: 'overflow:auto' }, [h('table', { class: 'tbl', style: 'width:100%' }, [
    h('thead', {}, [h('tr', {}, ['#', 'ឈ្មោះ', 'អត្តលេខ', 'ពិន្ទុ', 'បានធ្វើ'].map((x) => h('th', {}, x)))]),
    h('tbody', {}, d.players.map((p, i) => h('tr', {}, [h('td', {}, lvKh(i + 1)), h('td', {}, [lvAv(p, 24), ' ', p.name]), h('td', {}, p.student_id || '—'), h('td', {}, lvKh(p.score)), h('td', {}, `${lvKh(p.cur)}/${lvKh(d.room.total)}`)]))),
  ])]));
  ov.appendChild(box); document.body.appendChild(ov);
}

function lvAv(p, px) { const a = h('span', { style: `width:${px}px;height:${px}px;border-radius:50%;overflow:hidden;line-height:0;flex:none;display:inline-block` }); a.innerHTML = KmAvatar.svg(p.avatar || p.name, px); return a; }
function lvChip(p, kick) {
  const c = h('span', { style: 'display:inline-flex;align-items:center;gap:8px;padding:4px 6px 4px 4px;border-radius:99px;background:#1c3247;font-weight:700' });
  const a = h('span', { style: 'width:44px;height:44px;border-radius:50%;overflow:hidden;line-height:0;flex:none' }); a.innerHTML = KmAvatar.svg(p.avatar || p.name, 44); c.appendChild(a);
  c.appendChild(h('span', {}, p.name));
  if (kick) { const x = h('button', { type: 'button', title: 'ដកចេញ', style: 'border:0;background:#c92a2a;color:#fff;border-radius:50%;width:24px;height:24px;cursor:pointer;font-size:12px;padding:0', onclick: () => lvKick(p) }, '✕'); c.appendChild(x); }
  return c;
}
let lvKickFn = null;
function lvKick(p) { if (lvKickFn && confirm(`ដក «${p.name}» ចេញពីហ្គេម?`)) lvKickFn(p.pid); }

function lvQr(code, size) {
  const url = `${location.origin}/live?c=${code}`;
  const q = qrcode(0, 'M'); q.addData(url); q.make();
  const box = h('div', { style: `background:#fff;padding:10px;border-radius:14px;width:${size}px;height:${size}px;box-sizing:border-box;line-height:0` });
  box.innerHTML = q.createSvgTag({ cellSize: 4, margin: 0, scalable: true });
  const sv = box.querySelector('svg'); if (sv) { sv.style.width = '100%'; sv.style.height = '100%'; }
  return box;
}

function lvHost(code) {
  document.querySelectorAll('.lvh').forEach((e) => e.remove());
  const ov = h('div', { class: 'lvh', style: 'position:fixed;inset:0;z-index:80;background:#10202f;color:#fff;display:flex;flex-direction:column;overflow:auto' });
  const top = h('div', { style: 'display:flex;justify-content:space-between;align-items:center;gap:10px;padding:10px 18px;background:#0b1620' });
  const info = h('b', { style: 'font-size:18px' });
  const close = h('button', { class: 'secondary btn-sm', type: 'button' }, '✕ បិទទំព័រនេះ (ហ្គេមនៅតែដំណើរការ)');
  const slot = h('span', { style: 'display:flex;gap:8px;margin-left:auto' });
  top.appendChild(info); top.appendChild(slot); top.appendChild(close);
  const main = h('div', { style: 'flex:1;display:flex;flex-direction:column;align-items:center;justify-content:safe center;gap:16px;padding:18px;text-align:center' });
  ov.appendChild(top); ov.appendChild(main); document.body.appendChild(ov);
  let endPlayed = false, lastPlayers = 0, soloStarted = false, lastSec = -1;
  KmSound.unlock();
  let alive = true, st = null, busy = false, lastKey = '', t0 = 0;
  let iv = 0;
  close.onclick = () => { KmSound.stop(); alive = false; clearInterval(iv); ov.remove(); };
  const act = async (a) => { if (busy) return; busy = true; try { await api(`/api/live/host/${code}/action`, { method: 'POST', body: { a } }); } catch (e) { Exam.notify(e.message); } busy = false; poll(true); };

  lvKickFn = (pid) => api(`/api/live/host/${code}/action`, { method: 'POST', body: { a: 'kick', pid } }).then(() => poll()).catch((e) => Exam.notify(e.message));
  const btn = (label, fn, extra = '') => h('button', { type: 'button', style: `font-size:22px;padding:14px 34px;border-radius:16px;${extra}`, onclick: fn }, label);

  function topButtons() {
    slot.innerHTML = '';
    const sb = h('button', { type: 'button', title: 'សំឡេង', style: 'border:0;background:#1c3247;color:#fff;border-radius:10px;padding:7px 12px;font-size:16px;cursor:pointer' }, KmSound.muted() ? '🔇' : '🔊');
    sb.onclick = () => { sb.textContent = KmSound.toggle() ? '🔇' : '🔊'; }; slot.appendChild(sb);
    const mk = (label, bg, fn) => slot.appendChild(h('button', { type: 'button', style: `background:${bg};color:#fff;border:0;border-radius:10px;padding:7px 16px;font-weight:800;font-size:15px;cursor:pointer`, onclick: fn }, label));
    if (st.phase === 'lobby') { mk('▶ ចាប់ផ្តើមហ្គេម', '#2f9e44', () => act('start')); mk('■ បិទបន្ទប់', '#c92a2a', () => { if (confirm('បិទបន្ទប់នេះ?')) act('end'); }); }
    else if (st.mode === 'solo' && st.phase !== 'end') mk('■ បញ្ចប់ហ្គេម', '#c92a2a', () => { if (confirm('បញ្ចប់ហ្គេមសម្រាប់សិស្សទាំងអស់?')) act('end'); });
    else if (st.phase !== 'end') mk('■ បញ្ចប់ហ្គេម', '#c92a2a', () => { if (confirm('បញ្ចប់ហ្គេមឥឡូវនេះ?')) act('end'); });
  }
  function drawSolo() {
    topButtons();
    if (!soloStarted) { soloStarted = true; KmSound.sfx('start'); }
    if (st.phase !== 'end') KmSound.loop('question', 0.7);
    info.textContent = `បន្ទប់ ${st.code} · បែបសុខសាន្ត · ${lvKh(st.players)} នាក់ · ចប់ ${lvKh(st.finished)}`;
    main.dataset.q = ''; main.innerHTML = '';
    if (st.phase === 'end') { st.board = st.board; return drawEnd(); }
    const row = h('div', { style: 'display:flex;gap:24px;align-items:flex-start;justify-content:center;flex-wrap:wrap;width:min(1100px,96vw)' });
    const left = h('div', { style: 'display:flex;flex-direction:column;gap:10px;align-items:center' });
    left.appendChild(lvQr(st.code, 200)); left.appendChild(h('div', { style: 'font-size:46px;font-weight:900;letter-spacing:.1em;background:#fff;color:#10202f;border-radius:14px;padding:2px 18px' }, st.code));
    left.appendChild(h('div', { style: 'opacity:.8;font-size:15px;max-width:240px' }, 'សិស្សស្កែន QR ឬវាយលេខកូដ ហើយលេងបានតាមល្បឿនខ្លួន'));
    left.appendChild(btn('■ បញ្ចប់ហ្គេម', () => { if (confirm('បញ្ចប់ហ្គេមសម្រាប់សិស្សទាំងអស់?')) act('end'); }, 'background:#e03131;color:#fff;border:0;font-size:18px;padding:10px 22px'));
    const board = h('div', { style: 'flex:1;min-width:300px;display:flex;flex-direction:column;gap:6px;text-align:left' });
    board.appendChild(h('div', { style: 'font-size:22px;font-weight:800' }, '🏆 ចំណាត់ថ្នាក់ផ្ទាល់'));
    (st.board.length ? st.board.slice(0, 12) : []).forEach((p, i) => board.appendChild(h('div', { style: 'position:relative;padding:8px 12px;border-radius:10px;background:#1c3247;overflow:hidden;display:flex;justify-content:space-between;gap:10px' }, [h('div', { style: `position:absolute;left:0;top:0;bottom:0;width:${Math.round(100 * p.cur / st.total)}%;background:#2b5a3a;opacity:.7` }), h('span', { style: 'position:relative;display:inline-flex;align-items:center;gap:8px' }, [lvAv(p, 30), `${lvKh(i + 1)}. ${p.name}`]), h('span', { style: 'position:relative' }, [h('small', { style: 'opacity:.8' }, `${lvKh(p.cur)}/${lvKh(st.total)}  `), h('b', {}, lvKh(p.score)), ' ', h('button', { type: 'button', title: 'ដកចេញ', style: 'border:0;background:#c92a2a;color:#fff;border-radius:50%;width:22px;height:22px;cursor:pointer;font-size:11px;padding:0;margin-left:6px', onclick: () => lvKick(p) }, '✕')])])));
    if (!st.board.length) board.appendChild(h('div', { style: 'opacity:.7' }, 'កំពុងរង់ចាំសិស្សចូល…'));
    row.appendChild(left); row.appendChild(board); main.appendChild(row);
  }
  function draw() {
    topButtons();
    if (st.mode === 'solo' && st.phase !== 'lobby') return drawSolo();
    const key = [st.phase, st.qi, st.players, st.answered, st.phase === 'lobby' ? st.plist.map((p) => p.pid + p.avatar).join(',') : ''].join('|');
    info.textContent = `បន្ទប់ ${st.code} · ${st.mode === 'solo' ? 'បែបសុខសាន្ត · ' : ''}${lvKh(st.players)} នាក់` + (st.qi >= 0 && st.phase !== 'lobby' && st.phase !== 'end' ? ` · សំណួរ ${lvKh(st.qi + 1)}/${lvKh(st.total)}` : '');
    if (key === lastKey && st.phase !== 'question') return;
    if (st.phase === 'question') {                                  // keep the question on screen; only the counters change
      if (main.dataset.q !== String(st.qi)) { lastKey = ''; }
      if (main.dataset.q === String(st.qi)) { const a = main.querySelector('.lv-ans-n'); if (a) a.textContent = `ឆ្លើយរួច ${lvKh(st.answered)} / ${lvKh(st.players)}`; lvTick(); return; }
    }
    lastKey = key; main.innerHTML = ''; main.dataset.q = '';
    setTimeout(() => { if (window.renderMathInElement) try { renderMathInElement(main, { delimiters: [{ left: '\\(', right: '\\)', display: false }], throwOnError: false }); } catch (e) {} }, 0);
    if (st.phase === 'lobby') {
      KmSound.loop('lobby', 1); if (st.players > lastPlayers) KmSound.sfx('join'); lastPlayers = st.players;
      const row = h('div', { style: 'display:flex;gap:28px;align-items:center;justify-content:center;flex-wrap:wrap' });
      row.appendChild(lvQr(st.code, Math.min(300, Math.round(innerHeight * 0.4))));
      const side = h('div', { style: 'display:flex;flex-direction:column;gap:10px;align-items:center' });
      side.appendChild(h('div', { style: 'opacity:.85;font-size:20px' }, 'ស្កែន QR ឬចូលទៅ exam.khmermath.org/live'));
      side.appendChild(h('div', { style: 'font-size:clamp(56px,11vw,130px);font-weight:900;letter-spacing:.1em;line-height:1;background:#fff;color:#10202f;border-radius:20px;padding:8px 28px' }, st.code));
      side.appendChild(h('div', { style: 'opacity:.7;font-size:16px' }, 'ឬ khmermath.org/play/live.html (ឥតគិតថ្លៃ មិនចាំបាច់ចូលគណនី)'));
      row.appendChild(side); main.appendChild(row);
      main.appendChild(h('div', { style: 'display:flex;flex-wrap:wrap;gap:10px;justify-content:center;max-width:1100px' }, st.plist.map((p) => lvChip(p, true))));
      main.appendChild(h('div', { style: 'font-size:22px' }, `អ្នកលេង ${lvKh(st.players)} នាក់`));
      const brow = h('div', { style: 'display:flex;gap:12px;flex-wrap:wrap;justify-content:center' });
      brow.appendChild(btn('▶ ចាប់ផ្តើមហ្គេម', () => act('start'), 'background:#2f9e44;color:#fff;border:0'));
      brow.appendChild(btn('■ បិទបន្ទប់', () => { if (confirm('បិទបន្ទប់នេះ?')) act('end'); }, 'background:#e03131;color:#fff;border:0;font-size:18px;padding:14px 22px'));
      main.appendChild(brow);
    } else if (st.phase === 'question' || st.phase === 'reveal') {
      main.dataset.q = st.phase === 'question' ? String(st.qi) : '';
      const q = st.q, rv = st.reveal;
      lastSec = -1; KmSound.loop('question', 1); if (st.phase === 'reveal') KmSound.sfx('reveal');
      const qd = h('div', { style: 'font-size:clamp(24px,4.2vw,50px);font-weight:700;line-height:1.55;max-width:1100px' }); qd.textContent = q.q; main.appendChild(qd);
      if (q.f) { const f = h('div', {}); f.innerHTML = q.f; const sv = f.querySelector('svg'); if (sv) sv.style.cssText = 'height:30vh;max-width:90vw;background:#fff;border-radius:14px;padding:4px'; main.appendChild(f); }
      if (q.k === 'mcq' || q.k === 'tf') {
        const opts = q.k === 'mcq' ? q.o.map((o, i) => [String(i), o]) : [['T', 'ពិត'], ['F', 'មិនពិត']];
        const g = h('div', { style: 'display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;width:min(1100px,96vw)' });
        opts.forEach(([v, text], i) => {
          const ok = rv && String(rv.correct) === v, n = rv ? ((st.dist || []).find((d) => d.choice === v) || { n: 0 }).n : null;
          const c = h('div', { style: `display:flex;justify-content:space-between;align-items:center;gap:10px;padding:14px 18px;border-radius:16px;font-size:clamp(18px,2.6vw,32px);font-weight:800;background:${LV_COL[q.k === 'tf' ? (v === 'T' ? 1 : 0) : i % 6]};${rv && !ok ? 'opacity:.35;' : ''}${ok ? 'outline:6px solid #fff;' : ''}` });
          const t = h('span', { style: 'text-align:left' }); t.textContent = (q.k === 'mcq' ? 'កខគឃចឆជ'[i] + '. ' : '') + text; c.appendChild(t);
          if (rv) c.appendChild(h('b', {}, `${ok ? '✔ ' : ''}${lvKh(n)}`));
          g.appendChild(c);
        });
        main.appendChild(g);
      }
      if (st.phase === 'question') {
        main.appendChild(h('div', { class: 'lv-ans-n', style: 'font-size:24px;font-weight:800' }, `ឆ្លើយរួច ${lvKh(st.answered)} / ${lvKh(st.players)}`));
        main.appendChild(h('div', { class: 'lv-clock', style: 'font-size:56px;font-weight:900' }));
        main.appendChild(btn('បង្ហាញចម្លើយ', () => act('reveal'), 'background:#f08c00;color:#fff;border:0'));
        t0 = performance.now(); main.dataset.q = String(st.qi); main.dataset.left = String(st.left); lvTick();
      } else {
        const a = h('div', { style: 'font-size:clamp(24px,4vw,46px);font-weight:900;color:#69db7c' }); a.textContent = '✔ ' + rv.show; main.appendChild(a);
        if (rv.sol) { const s = h('div', { style: 'font-size:20px;opacity:.9;max-width:900px' }); s.textContent = rv.sol; main.appendChild(s); }
        if (q.k === 'num') main.appendChild(h('div', { style: 'font-size:20px' }, `ឆ្លើយត្រូវ ${lvKh((st.dist || []).reduce((s, d) => s + (d.ok || 0), 0))} / ${lvKh(st.answered)} នាក់`));
        main.appendChild(h('ol', { style: 'list-style:none;margin:0;padding:0;display:flex;gap:10px;flex-wrap:wrap;justify-content:center' }, st.top.slice(0, 5).map((p, i) => h('li', { style: 'padding:8px 16px;border-radius:12px;background:#1c3247;font-size:20px' }, `${['🥇', '🥈', '🥉', '4.', '5.'][i]} ${p.name} · ${lvKh(p.score)}`))));
        main.appendChild(btn(st.qi + 1 >= st.total ? '🏆 លទ្ធផលចុងក្រោយ' : 'សំណួរបន្ទាប់ ▶', () => act('next'), 'background:#2f9e44;color:#fff;border:0'));
      }
    } else if (st.phase === 'end') {
      drawEnd();
    }
  }
  function drawEnd() {
    main.innerHTML = ''; if (!endPlayed) { endPlayed = true; KmSound.stop(); KmSound.sfx('fanfare'); }
      main.appendChild(h('div', { style: 'font-size:clamp(34px,6vw,64px);font-weight:900' }, '🏆 លទ្ធផលចុងក្រោយ'));
      const pod = h('div', { style: 'display:flex;align-items:flex-end;gap:14px;justify-content:center;height:34vh;min-height:200px' });
      const ord = [1, 0, 2].filter((i) => st.board[i]);
      ord.forEach((i) => { const p = st.board[i]; pod.appendChild(h('div', { style: 'display:flex;flex-direction:column;align-items:center;justify-content:flex-end;width:min(26vw,220px)' }, [lvAv(p, 64), h('div', { style: 'font-size:22px;font-weight:800;overflow-wrap:anywhere' }, p.name), h('div', { style: 'font-size:28px' }, lvKh(p.score)), h('div', { style: `width:100%;height:${[100, 72, 52][i]}%;min-height:60px;background:${['#f08c00', '#adb5bd', '#c2763b'][i]};border-radius:12px 12px 0 0;font-size:44px;font-weight:900;color:#fff;display:grid;place-items:center` }, ['🥇', '🥈', '🥉'][i])])); });
      main.appendChild(pod);
      main.appendChild(h('div', { style: 'max-width:700px;width:92vw;display:grid;grid-template-columns:1fr 1fr;gap:6px;text-align:left' }, st.board.slice(3, 23).map((p, i) => h('div', { style: 'padding:6px 12px;border-radius:10px;background:#1c3247;display:flex;justify-content:space-between' }, [h('span', {}, `${lvKh(i + 4)}. ${p.name}`), h('b', {}, lvKh(p.score))]))));
      const dl = h('button', { class: 'secondary', type: 'button', onclick: () => { const wb = XLSX.utils.book_new(); XLSX.utils.book_append_sheet(wb, XLSX.utils.aoa_to_sheet([['ល.រ', 'ឈ្មោះ', 'ពិន្ទុ'], ...st.board.map((p, i) => [i + 1, p.name, p.score])]), 'Live'); XLSX.writeFile(wb, `ហ្គេមផ្ទាល់_${code}.xlsx`); } }, '⬇ ទាញយក Excel');
      main.appendChild(dl);
  }
  function lvTick() {
    const c = main.querySelector('.lv-clock'); if (!c || st.phase !== 'question') return;
    const r = Math.max(0, st.left - (performance.now() - t0)); c.textContent = lvKh(Math.ceil(r / 1000)); { const sec = Math.ceil(r / 1000); if (sec !== lastSec) { lastSec = sec; if (sec > 0 && sec <= 5) KmSound.sfx('tick'); } } c.style.color = r < 6000 ? '#ff8787' : '#fff';
    if (r <= 0 && !busy) act('reveal');                                // time is up: show the answer
  }
  async function poll(now) {
    if (!alive) return;
    try { st = await api(`/api/live/host/${code}`); t0 = performance.now(); draw(); } catch (e) { if (e.status === 404) { main.innerHTML = ''; main.appendChild(h('p', {}, 'រកមិនឃើញបន្ទប់នេះទេ។')); return; } }
    if (alive) setTimeout(poll, st && st.phase === 'question' ? 1200 : 1800);
  }
  iv = setInterval(() => { if (!alive) return; lvTick(); }, 300);
  poll();
}
