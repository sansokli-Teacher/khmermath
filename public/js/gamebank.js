// «សំណួរហ្គេម» tab: see every question of the team game, fix the wrong ones, hide bad ones, and choose which lessons
// the game offers (on exam.khmermath.org and on khmermath.org — both read the same bank from /api/game/bank).
// Only the owner can change things; other teachers can look.
let gbLesson = 1, gbFilter = 'all', gbData = null;

const gbKh = (n) => String(n).replace(/\d/g, (d) => '០១២៣៤៥៦៧៨៩'[d]);
const gbMath = (el, text) => { el.textContent = text; Exam.typeset(el); return el; };
const gbLv = { easy: 'ងាយ', medium: 'មធ្យម', hard: 'ពិបាក' };
const GB_SYMBOLS = [['\\(  \\)', 'គណិត'], ['\\frac{a}{b}', 'ប្រភាគ'], ['\\sqrt{ }', '√'], ['^{2}', 'x²'], ['\\times', '×'], ['\\div', '÷'], ['\\leq', '≤'], ['\\geq', '≥'], ['^{\\circ}', '°'], ['\\angle', '∠'], ['\\parallel', '∥'], ['\\perp', '⊥'], ['\\pi', 'π'], ['\\,', 'ចន្លោះ']];

render.gamebank = async function () {
  const root = document.getElementById('tab-gamebank');
  root.innerHTML = '';
  try { gbData = await api('/api/game/admin'); } catch (e) { return root.appendChild(h('div', { class: 'error' }, e.message)); }
  const can = gbData.can_edit;
  if (!gbData.lessons.some((L) => L.n === gbLesson)) gbLesson = gbData.lessons[0].n;

  root.appendChild(h('div', { class: 'card' }, [
    h('h3', { style: 'margin-top:0' }, 'សំណួរហ្គេមក្រុម'),
    h('p', { class: 'muted' }, 'នេះជាធនាគារសំណួរតែមួយ ដែលហ្គេមនៅ exam.khmermath.org និង khmermath.org ប្រើទាំងពីរ។ ពេលអ្នករក្សាទុកការកែ ហ្គេមទាំងពីរទទួលបានការកែភ្លាម (ក្នុងរយៈពេលតិចជាង ១ នាទី)។' + (can ? '' : ' (គ្រូដទៃអាចមើលបានតែប៉ុណ្ណោះ មានតែម្ចាស់ប្រព័ន្ធទេដែលកែបាន។)')),
  ]));

  // ---- which lessons the games offer ----
  const on = h('input', { type: 'checkbox' }); on.checked = gbData.config.enabled; on.disabled = !can;
  const boxes = gbData.lessons.map((L) => {
    const cb = h('input', { type: 'checkbox' }); cb.checked = gbData.config.lessons === null ? true : gbData.config.lessons.includes(L.n); cb.disabled = !can;
    const fixed = L.qs.filter((q) => q.edited).length, hid = L.qs.filter((q) => q.off).length;
    const lab = h('label', { style: 'display:grid;grid-template-columns:22px 1fr;gap:2px 8px;align-items:center;padding:8px 10px;border:1px solid var(--line);border-radius:10px;background:#fff' }, [
      cb, h('span', {}, [h('b', {}, `មេរៀនទី ${gbKh(L.n)} `), L.title]),
      h('span'), h('small', { class: 'muted' }, `${gbKh(L.qs.length)} សំណួរ${fixed ? ` · កែរួច ${gbKh(fixed)}` : ''}${hid ? ` · លាក់ ${gbKh(hid)}` : ''}`),
    ]);
    return { cb, lab };
  });
  const GB_GAMES = [['cards', '🃏 កាតបើក'], ['wheel', '🎡 កង់វិល'], ['boat', '🚣 ប្រណាំងទូកង'], ['live', '📱 សំណួរផ្ទាល់លើទូរស័ព្ទ'], ['bingo', '🎯 ប៊ីងហ្គោ']];
  const gcb = {};
  const gamesCard = h('div', { class: 'card' }, [
    h('h3', { style: 'margin-top:0' }, 'ហ្គេមដែលបើកឱ្យសិស្សលេងនៅ khmermath.org'),
    h('p', { class: 'muted' }, 'គ្រូ (នៅក្នុង exam.khmermath.org) អាចលេងបានគ្រប់ហ្គេមជានិច្ច។ ការបិទនៅទីនេះ គឺបិទចំពោះទំព័រសាធារណៈនៅ khmermath.org ប៉ុណ្ណោះ។'),
    h('div', { style: 'display:flex;flex-wrap:wrap;gap:8px' }, GB_GAMES.map(([k, label]) => {
      const cb = h('input', { type: 'checkbox' }); cb.checked = gbData.config.games ? gbData.config.games[k] !== false : true; cb.disabled = !can; gcb[k] = cb;
      return h('label', { style: 'display:flex;gap:8px;align-items:center;padding:8px 12px;border:1px solid var(--line);border-radius:10px;background:#fff' }, [cb, label]);
    })),
  ]);
  root.appendChild(gamesCard);
  const cfgCard = h('div', { class: 'card' }, [
    h('h3', { style: 'margin-top:0' }, 'មេរៀនដែលអនុញ្ញាតឱ្យលេង'),
    h('label', { style: 'display:flex;gap:8px;align-items:center;margin-bottom:10px' }, [on, h('b', {}, 'បើកហ្គេម (បិទទាំងអស់ពេលមិនចង់ឱ្យសិស្សលេង)')]),
    h('div', { style: 'display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:8px' }, boxes.map((b) => b.lab)),
  ]);
  if (can) {
    const all = h('button', { class: 'secondary btn-sm', type: 'button' }, 'ជ្រើសទាំងអស់'); all.onclick = () => boxes.forEach((b) => { b.cb.checked = true; });
    const none = h('button', { class: 'secondary btn-sm', type: 'button' }, 'មិនជ្រើសទាំងអស់'); none.onclick = () => boxes.forEach((b) => { b.cb.checked = false; });
    const save = h('button', { type: 'button' }, 'រក្សាទុកការកំណត់ (មេរៀន និងហ្គេម)');
    save.onclick = async () => {
      const lessons = gbData.lessons.filter((L, i) => boxes[i].cb.checked).map((L) => L.n);
      try { await api('/api/game/config', { method: 'POST', body: { enabled: on.checked, lessons, games: Object.fromEntries(Object.entries(gcb).map(([k, c]) => [k, c.checked])) } }); Exam.notify(`បានរក្សាទុក។ ហ្គេមផ្តល់ ${lessons.length} មេរៀន។`); render.gamebank(); } catch (e) { Exam.notify(e.message); }
    };
    cfgCard.appendChild(h('div', { class: 'row', style: 'margin-top:12px;gap:8px;flex-wrap:wrap' }, [save, all, none]));
  }
  root.appendChild(cfgCard);

  // ---- the questions ----
  const sel = h('select', { 'aria-label': 'មេរៀន' }, gbData.lessons.map((L) => h('option', { value: L.n }, `មេរៀនទី ${gbKh(L.n)} · ${L.title}`)));
  sel.value = gbLesson; sel.onchange = () => { gbLesson = Number(sel.value); render.gamebank(); };
  const flt = h('select', { 'aria-label': 'តម្រង' }, [['all', 'សំណួរទាំងអស់'], ['edited', 'ដែលបានកែ'], ['off', 'ដែលបានលាក់'], ['fig', 'ដែលមានរូប']].map(([v, t]) => h('option', { value: v }, t)));
  flt.value = gbFilter; flt.onchange = () => { gbFilter = flt.value; render.gamebank(); };
  const L = gbData.lessons.find((x) => x.n === gbLesson);
  const list = h('div', { style: 'display:flex;flex-direction:column;gap:10px;margin-top:12px' });
  L.qs.filter((q) => gbFilter === 'all' || (gbFilter === 'edited' && q.edited) || (gbFilter === 'off' && q.off) || (gbFilter === 'fig' && q.f)).forEach((q) => list.appendChild(gbRow(L, q, can)));
  root.appendChild(h('div', { class: 'card' }, [h('div', { class: 'row', style: 'gap:10px;flex-wrap:wrap;align-items:center' }, [h('b', {}, 'កែសំណួរ'), sel, flt]), list]));
  Exam.typeset(root);
};

function gbRow(L, q, can) {
  const badges = [q.f ? '🖼 មានរូប' : '', q.edited ? '✎ កែរួច' : '', q.off ? '🚫 លាក់' : '', q.stale ? '⚠ សំណួរដើមបានប្តូរ (ការកែមិនប្រើ)' : '', gbLv[q.lv] || ''].filter(Boolean);
  const body = h('div', { style: 'min-width:0' }, [
    gbMath(h('div', { style: 'font-weight:600;line-height:1.7' }), q.q),
    q.o ? h('div', { style: 'display:grid;grid-template-columns:1fr 1fr;gap:4px 12px;margin-top:4px;font-size:15px' }, q.o.map((o, k) => gbMath(h('div', { style: k === q.k ? 'color:#14532d;font-weight:700' : '' }, ''), `${'កខគឃ'[k]}. ${o}${k === q.k ? ' ✓' : ''}`))) : gbMath(h('div', { style: 'color:#14532d;font-weight:700;margin-top:4px' }), `ចម្លើយ៖ ${q.a}`),
    h('small', { class: 'muted' }, badges.join(' · ')),
  ]);
  const btns = h('div', { style: 'display:flex;gap:6px;flex-wrap:wrap;align-items:start' }, [h('button', { class: 'secondary btn-sm', type: 'button', onclick: () => gbEdit(L, q, can) }, can ? '✎ កែ' : '👁 មើល')]);
  if (can) btns.appendChild(h('button', { class: 'secondary btn-sm', type: 'button', onclick: async () => { await gbSave(L, q, gbFields(q), !q.off); } }, q.off ? 'បង្ហាញវិញ' : 'លាក់'));
  return h('div', { style: `display:grid;grid-template-columns:44px 1fr auto;gap:10px;padding:10px 12px;border:1px solid var(--line);border-radius:12px;background:${q.off ? '#f6f6f6' : '#fff'};${q.off ? 'opacity:.7' : ''}` }, [
    h('b', { style: 'font-size:18px;color:var(--brand)' }, gbKh(q.i + 1)), body, btns]);
}

const gbFields = (q) => ({ t: q.t, q: q.q, lv: q.lv, h: q.h || '', s: q.s || '', a: q.a, o: q.o, k: q.k });

async function gbSave(L, q, fields, off) {
  try { await api('/api/game/question', { method: 'POST', body: { lesson: L.n, i: q.i, fields, off: !!off } }); await render.gamebank(); } catch (e) { Exam.notify(e.message); }
}

function gbEdit(L, q, can) {
  const f = gbFields(q);
  let last = null;
  const mk = (tag, val, extra = {}) => { const el = h(tag, { style: 'width:100%', ...extra }); el.value = val; el.disabled = !can; el.addEventListener('focus', () => { last = el; }); el.addEventListener('input', preview); return el; };
  const q_ = mk('textarea', f.q, { rows: '4' });
  const s_ = mk('textarea', f.s, { rows: '3' });
  const h_ = mk('input', f.h, { type: 'text' });
  const t_ = mk('input', f.t, { type: 'text' });
  const lv = h('select', { disabled: can ? null : 'disabled' }, ['easy', 'medium', 'hard'].map((v) => h('option', { value: v }, gbLv[v]))); lv.value = f.lv; lv.disabled = !can;
  const opts = f.o ? f.o.map((o) => mk('input', o, { type: 'text' })) : [];
  const radios = f.o ? f.o.map((_, k) => { const r = h('input', { type: 'radio', name: 'gb-k' }); r.checked = k === f.k; r.disabled = !can; r.addEventListener('change', preview); return r; }) : [];
  const a_ = f.o ? null : mk('input', f.a, { type: 'text' });
  const off = h('input', { type: 'checkbox' }); off.checked = q.off; off.disabled = !can;

  const pv = h('div', { class: 'card', style: 'margin:0;background:#fbfdff' });
  function preview() {
    pv.innerHTML = '';
    pv.appendChild(h('small', { class: 'muted' }, `មេរៀនទី ${gbKh(L.n)} · ${t_.value}`));
    pv.appendChild(gbMath(h('div', { style: 'font-weight:700;font-size:18px;line-height:1.8;margin:6px 0' }), q_.value));
    if (q.f) { const fg = h('div', { style: 'text-align:center;margin:6px 0' }); fg.innerHTML = q.f; const sv = fg.querySelector('svg'); if (sv) sv.style.cssText = 'max-width:100%;height:150px;background:#fff;border:1px solid #e1e8f0;border-radius:10px'; pv.appendChild(fg); }
    if (f.o) pv.appendChild(h('div', { style: 'display:grid;grid-template-columns:1fr 1fr;gap:6px' }, opts.map((o, k) => gbMath(h('div', { style: `padding:6px 10px;border:2px solid ${radios[k].checked ? '#2f9e44' : '#e1e8f0'};border-radius:10px;background:${radios[k].checked ? '#d3f9d8' : '#fff'}` }), `${'កខគឃ'[k]}. ${o.value}`))));
    else pv.appendChild(gbMath(h('div', { style: 'padding:8px 12px;border:2px dashed #2f9e44;border-radius:10px;background:#ebfbee;font-weight:700' }), `ចម្លើយ៖ ${a_.value}`));
    if (s_.value) pv.appendChild(gbMath(h('div', { class: 'muted', style: 'margin-top:8px' }), `ដំណោះស្រាយ៖ ${s_.value}`));
  }

  const bar = h('div', { style: 'display:flex;flex-wrap:wrap;gap:4px;margin:6px 0' }, GB_SYMBOLS.map(([ins, lab]) => h('button', { type: 'button', class: 'secondary btn-sm', title: ins, onclick: () => { if (!last || !can) return; const st = last.selectionStart ?? last.value.length, en = last.selectionEnd ?? st; last.setRangeText(ins, st, en, 'end'); last.focus(); preview(); } }, lab)));
  const field = (label, el) => h('label', { style: 'display:block;margin-top:10px' }, [h('b', { style: 'font-size:14px' }, label), el]);
  const form = h('div', {}, [
    can ? h('p', { class: 'muted', style: 'margin:0' }, 'សរសេរគណិតវិទ្យាក្នុង \\( … \\) ឧ. \\(\\frac{3}{4}\\) ។ ប៊ូតុងខាងក្រោមជួយបញ្ចូលរូបមន្ត។') : null,
    can ? bar : null,
    field('សំណួរ', q_),
    f.o ? h('div', { style: 'margin-top:10px' }, [h('b', { style: 'font-size:14px' }, 'ជម្រើស (ចុចរង្វង់ដើម្បីជ្រើសចម្លើយត្រឹមត្រូវ)'), ...opts.map((o, k) => h('div', { style: 'display:grid;grid-template-columns:24px 28px 1fr;gap:6px;align-items:center;margin-top:4px' }, [radios[k], h('b', {}, 'កខគឃ'[k]), o]))]) : field('ចម្លើយ', a_),
    field('ដំណោះស្រាយ (បង្ហាញពេលបង្ហាញចម្លើយ)', s_),
    field('គន្លឹះ', h_), field('ផ្នែក', t_),
    h('label', { style: 'display:flex;gap:10px;align-items:center;margin-top:10px' }, ['កម្រិត', lv, h('label', { style: 'display:flex;gap:6px;align-items:center;margin-left:14px' }, [off, 'លាក់សំណួរនេះពីហ្គេម'])]),
    q.edited || q.stale ? h('small', { class: 'muted', style: 'display:block;margin-top:8px' }, ['សំណួរដើម៖ ', gbMath(h('span'), q.orig.q)]) : null,
  ]);
  const overlay = h('div', { style: 'position:fixed;inset:0;background:rgba(15,23,28,.5);z-index:60;display:flex;align-items:flex-start;justify-content:center;padding:16px;overflow:auto' });
  const close = () => overlay.remove();
  const actions = h('div', { class: 'row', style: 'justify-content:flex-end;gap:8px;margin-top:14px;flex-wrap:wrap' }, [
    can && (q.edited || q.stale) ? h('button', { class: 'secondary', type: 'button', onclick: async () => { if (!(await Exam.modal('ត្រឡប់ទៅសំណួរដើមវិញ?'))) return; try { await api('/api/game/reset', { method: 'POST', body: { lesson: L.n, i: q.i } }); close(); render.gamebank(); } catch (e) { Exam.notify(e.message); } } }, 'ត្រឡប់ទៅដើម') : null,
    h('button', { class: 'secondary', type: 'button', onclick: close }, can ? 'បោះបង់' : 'បិទ'),
    can ? h('button', { type: 'button', onclick: async () => {
      const fields = { t: t_.value, q: q_.value, lv: lv.value, h: h_.value, s: s_.value };
      if (f.o) { fields.o = opts.map((o) => o.value); fields.k = radios.findIndex((r) => r.checked); } else fields.a = a_.value;
      try { await api('/api/game/question', { method: 'POST', body: { lesson: L.n, i: q.i, fields, off: off.checked } }); close(); render.gamebank(); } catch (e) { Exam.notify(e.message); }
    } }, 'រក្សាទុក') : null,
  ]);
  overlay.appendChild(h('div', { class: 'card', style: 'max-width:1100px;width:100%;margin:0 auto;display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:18px' }, [
    h('div', {}, [h('h3', { style: 'margin:0 0 4px' }, `មេរៀនទី ${gbKh(L.n)} · សំណួរទី ${gbKh(q.i + 1)}`), form, actions]),
    h('div', {}, [h('b', {}, 'មើលជាមុន'), pv]),
  ]));
  overlay.addEventListener('click', (e) => { if (e.target === overlay) close(); });
  document.body.appendChild(overlay);
  if (window.matchMedia('(max-width: 900px)').matches) overlay.firstChild.style.gridTemplateColumns = '1fr';
  preview();
}
