// Question bank: grade → lesson → questions. Reuse, tag, add new, import, or build a random test from a lesson.
const LEVEL_KH = { easy: 'ងាយ', medium: 'មធ្យម', hard: 'ពិបាក', pisa: 'PISA' };
const KH_DIGITS = '០១២៣៤៥៦៧៨៩';
const khNum = (n) => String(n).replace(/\d/g, (d) => KH_DIGITS[d]);
const GRADE_KH = (g) => `ថ្នាក់ទី ${khNum(g)}`;
let bankState = { grade: '', lesson: '', level: '', kind: '', topic: '', q: '' };   // grade '' = all, '-' = no grade; lesson '' = all, '-' = no lesson
let CURR = null;

async function loadCurr(force) { if (!CURR || force) CURR = await api('/api/curriculum'); return CURR; }

// grade <select> + lesson <input list> pair used by the question forms
function gradeLessonPicker(g, l, curr) {
  const id = 'lesson-dl-' + Math.random().toString(36).slice(2, 7);
  const grade = h('select', {}, [['', '— ថ្នាក់ —'], ...curr.grades.map((x) => [x, GRADE_KH(x)])].map(([v, t]) => h('option', { value: v, selected: String(g || '') === v ? 'selected' : null }, t)));
  const dl = h('datalist', { id });
  const lesson = h('input', { type: 'text', list: id, placeholder: 'ជ្រើស ឬវាយឈ្មោះមេរៀន', value: l || '' });
  const fill = () => { dl.innerHTML = ''; (curr.lessons[grade.value] || []).forEach((n) => dl.append(h('option', { value: n }))); };
  grade.addEventListener('change', fill); fill();
  return { grade, lesson, dl, get: () => ({ grade: grade.value || null, lesson: lesson.value.trim() || null }) };
}

function bankModal(title, body, wide) {
  const back = h('div', { class: 'modal-back', style: 'align-items:flex-start;overflow:auto;', onclick: (e) => { if (e.target === back) back.remove(); } });
  back.append(h('div', { class: 'modal-box', style: `text-align:left;max-width:${wide ? 720 : 520}px;margin:20px auto;` }, [h('h2', {}, title), body]));
  document.body.append(back);
  return back;
}

render.bank = async function () {
  const container = document.getElementById('tab-bank');
  container.innerHTML = '';
  const [{ questions }, { tests }, curr] = await Promise.all([api('/api/bank'), api('/api/tests'), loadCurr(true)]);
  const editable = tests.filter((t) => (t.my_role === 'owner' || t.my_role === 'editor') && !t.is_sample);
  const selected = new Set();
  const S = bankState;
  const topics = [...new Set(questions.map((q) => q.topic).filter(Boolean))].sort();
  const reload = () => render.bank();

  // lessons per grade: the curriculum list first, then any other lesson names found on questions
  const lessonsOf = (g) => {
    const base = curr.lessons[g] || [];
    const extra = [...new Set(questions.filter((q) => q.grade === g && q.lesson && !base.includes(q.lesson)).map((q) => q.lesson))];
    return [...base, ...extra];
  };
  const count = (fn) => questions.filter(fn).length;

  // ---------- header + grade tabs
  const gradePill = (val, label, n) => h('button', { class: `filter-pill${S.grade === val ? ' on' : ''}`, onclick: () => { Object.assign(S, { grade: val, lesson: '' }); reload(); } }, [label, ' ', h('span', { class: 'pill-n' }, String(n))]);
  const pills = h('div', { class: 'filter-bar' }, [
    gradePill('', 'ទាំងអស់', questions.length),
    ...curr.grades.map((g) => gradePill(g, GRADE_KH(g), count((q) => q.grade === g))),
    gradePill('-', 'មិនទាន់កំណត់ថ្នាក់', count((q) => !q.grade)),
  ]);
  container.append(h('div', { class: 'card' }, [
    h('h2', {}, `🗂 ធនាគារសំណួរ (${questions.length})`),
    h('p', { class: 'muted' }, 'រៀបតាមថ្នាក់ → មេរៀន។ បន្ថែមសំណួរចូលមេរៀន រួចពេលបង្កើតតេស្ត គ្រាន់តែជ្រើសរើសពីមេរៀន ឬផ្នែកដែលចង់បាន។ សំណួរចាស់ៗពីតេស្តរបស់លោកគ្រូក៏នៅទីនេះដែរ — ជ្រើសរើសពួកវា រួចចុច «🏷 ដាក់ក្នុងមេរៀន»។'),
    pills,
  ]));

  // ---------- lesson sidebar
  const showLessons = S.grade && S.grade !== '-';
  const inGrade = (q) => !S.grade || (S.grade === '-' ? !q.grade : q.grade === S.grade);
  const side = h('div', { class: 'card', style: 'padding:10px;align-self:start;' });
  if (showLessons) {
    const lessonBtn = (val, label, qs) => {
      const lv = (l) => qs.filter((q) => q.level === l).length;
      return h('button', { class: `lesson-btn${S.lesson === val ? ' on' : ''}`, onclick: () => { S.lesson = val; reload(); } }, [
        h('span', { class: 'lesson-name' }, label),
        h('span', { class: 'lesson-n' }, qs.length ? `${qs.length}` : '—'),
        qs.length ? h('span', { class: 'lesson-lv' }, `ង ${lv('easy')} · ម ${lv('medium')} · ព ${lv('hard')} · PISA ${lv('pisa')}`) : null,
      ]);
    };
    const gq = questions.filter(inGrade);
    side.append(h('div', { class: 'lesson-title' }, GRADE_KH(S.grade)), lessonBtn('', 'មេរៀនទាំងអស់', gq));
    lessonsOf(S.grade).forEach((name, i) => side.append(lessonBtn(name, `${khNum(i + 1)}. ${name}`, gq.filter((q) => q.lesson === name))));
    side.append(lessonBtn('-', 'មិនទាន់កំណត់មេរៀន', gq.filter((q) => !q.lesson)));
    side.append(h('button', { class: 'secondary btn-sm', style: 'margin-top:8px;width:100%;', onclick: () => {
      const inp = h('input', { type: 'text', placeholder: 'ឈ្មោះមេរៀនថ្មី' });
      const m = bankModal(`＋ មេរៀនថ្មី — ${GRADE_KH(S.grade)}`, h('div', {}, [inp, h('div', { class: 'row', style: 'justify-content:flex-end;margin-top:14px;' }, [
        h('button', { class: 'secondary', onclick: () => m.remove() }, 'បោះបង់'),
        h('button', { onclick: async () => {
          if (!inp.value.trim()) return inp.focus();
          try { await api('/api/curriculum/lesson', { method: 'POST', body: { grade: S.grade, name: inp.value.trim() } }); S.lesson = inp.value.trim(); m.remove(); reload(); } catch (e) { Exam.notify(e.message); }
        } }, 'បន្ថែម')])]));
      inp.focus();
    } }, '＋ បន្ថែមមេរៀន'));
  }

  // ---------- right side: filters, actions, list
  const list = h('div', { class: 'test-list' });
  const countLbl = h('b', {}, '0');
  const targetSel = h('select', { style: 'width:auto;max-width:240px;' }, editable.map((t) => h('option', { value: t.id }, t.title)));
  const addBtn = h('button', { disabled: 'disabled', onclick: async () => {
    if (!targetSel.value) return Exam.notify('សូមបង្កើតតេស្តមួយជាមុនសិន។');
    try { const r = await api(`/api/tests/${targetSel.value}/questions/copy`, { method: 'POST', body: { question_ids: [...selected] } }); await Exam.notify(`✅ បានថែម ${r.copied} សំណួរទៅតេស្ត។`); selected.clear(); draw(); } catch (e) { Exam.notify(e.message); }
  } }, '➕ ថែមទៅតេស្ត');
  const tagBtn = h('button', { class: 'secondary', disabled: 'disabled', onclick: () => {
    const gl = gradeLessonPicker(S.grade && S.grade !== '-' ? S.grade : '', showLessons && S.lesson && S.lesson !== '-' ? S.lesson : '', curr);
    const box = h('div', {}, [h('p', { class: 'muted' }, `ដាក់ ${selected.size} សំណួរក្នុង៖`), h('label', {}, 'ថ្នាក់'), gl.grade, h('label', {}, 'មេរៀន'), gl.lesson, gl.dl,
      h('div', { class: 'row', style: 'justify-content:flex-end;margin-top:14px;' }, [
        h('button', { class: 'secondary', onclick: () => m.remove() }, 'បោះបង់'),
        h('button', { onclick: async () => {
          try { const r = await api('/api/bank/tag', { method: 'POST', body: { question_ids: [...selected], ...gl.get() } }); m.remove(); await Exam.notify(`✅ បានដាក់ ${r.tagged} សំណួរក្នុងមេរៀន។`); reload(); } catch (e) { Exam.notify(e.message); }
        } }, 'រក្សាទុក')])]);
    const m = bankModal('🏷 ដាក់ក្នុងមេរៀន', box);
  } }, '🏷 ដាក់ក្នុងមេរៀន');
  const bar = h('div', { class: 'bank-bar' }, [h('span', {}, ['បានជ្រើស ', countLbl, ' សំណួរ']), tagBtn, targetSel, addBtn]);

  const fLevel = h('select', { style: 'width:auto;' }, [['', 'គ្រប់កម្រិត'], ['easy', 'ងាយ'], ['medium', 'មធ្យម'], ['hard', 'ពិបាក'], ['pisa', 'PISA']].map(([v, l]) => h('option', { value: v, selected: S.level === v ? 'selected' : null }, l)));
  const fKind = h('select', { style: 'width:auto;' }, [['', 'គ្រប់ប្រភេទ'], ['mcq', 'ពហុជ្រើសរើស'], ['writing', 'សរសេរ']].map(([v, l]) => h('option', { value: v, selected: S.kind === v ? 'selected' : null }, l)));
  const fTopic = topics.length ? h('select', { style: 'width:auto;' }, [h('option', { value: '' }, 'គ្រប់ប្រធានបទ'), ...topics.map((t) => h('option', { value: t, selected: S.topic === t ? 'selected' : null }, t))]) : null;
  const fQ = h('input', { type: 'text', placeholder: '🔍 ស្វែងរក…', value: S.q, style: 'max-width:200px;' });

  const bankId = async () => (await api('/api/bank/home')).id;
  const presetGrade = () => (S.grade && S.grade !== '-' ? S.grade : '');
  const presetLesson = () => (showLessons && S.lesson && S.lesson !== '-' ? S.lesson : '');
  const newBtn = h('button', { onclick: async () => {
    const id = await bankId(); const holder = h('div', {});
    const m = bankModal('➕ សំណួរថ្មីក្នុងធនាគារ', holder, true);
    holder.append(await buildQuestionForm({ id }, holder, { grade: presetGrade(), lesson: presetLesson(), onDone: () => { m.remove(); reload(); } }));
  } }, '➕ សំណួរថ្មី');
  const importBtn = h('button', { class: 'secondary', onclick: async () => {
    const id = await bankId(); const holder = h('div', {});
    const m = bankModal('📥 នាំចូលសំណួរពី Excel', holder, true);
    holder.append(h('p', { class: 'muted' }, 'ដាក់ជួរ grade (ថ្នាក់) និង lesson (មេរៀន) ក្នុង Excel ដើម្បីឱ្យសំណួរចូលមេរៀនត្រឹមត្រូវ។'), importQuestionsCard({ id }, holder, () => { m.remove(); reload(); }));
  } }, '📥 នាំចូល Excel');
  const selAll = h('button', { class: 'secondary btn-sm', onclick: () => { const rows = visible(); const all = rows.every((x) => selected.has(x.id)); rows.forEach((x) => (all ? selected.delete(x.id) : selected.add(x.id))); draw(); } }, '☑ ជ្រើសទាំងអស់ដែលបង្ហាញ');

  const visible = () => {
    const q = fQ.value.trim().toLowerCase();
    return questions.filter((x) => inGrade(x)
      && (!showLessons || !S.lesson || (S.lesson === '-' ? !x.lesson : x.lesson === S.lesson))
      && (!fLevel.value || x.level === fLevel.value) && (!fKind.value || x.kind === fKind.value) && (!fTopic || !fTopic.value || x.topic === fTopic.value)
      && (!q || x.stem_text.toLowerCase().includes(q)));
  };
  function draw() {
    Object.assign(S, { level: fLevel.value, kind: fKind.value, topic: fTopic ? fTopic.value : '', q: fQ.value });
    const rows = visible();
    list.innerHTML = '';
    if (!rows.length) list.append(h('div', { class: 'empty-card' }, h('div', { class: 'muted' }, questions.length ? 'មិនមានសំណួរក្នុងផ្នែកនេះទេ — ចុច «➕ សំណួរថ្មី» ឬ «📥 នាំចូល Excel»។' : 'មិនទាន់មានសំណួរទេ — ចុច «➕ សំណួរថ្មី» ឬបង្កើតតេស្តជាមុនសិន។')));
    rows.slice(0, 200).forEach((x) => {
      const cb = h('input', { type: 'checkbox', style: 'width:20px;height:20px;flex:none;', checked: selected.has(x.id) ? 'checked' : null, onchange: () => { cb.checked ? selected.add(x.id) : selected.delete(x.id); upd(); } });
      list.append(h('label', { class: 'bank-item' }, [
        cb,
        h('div', { style: 'min-width:0;flex:1;' }, [
          mathEl('div', { class: 'bank-stem' }, x.stem_text),
          h('div', { class: 'test-chips' }, [
            x.kind === 'writing' ? h('span', { class: 'chip chip-soon' }, '✎ សរសេរ') : h('span', { class: 'chip chip-plain' }, 'ពហុជ្រើសរើស'),
            x.grade && S.grade === '' ? h('span', { class: 'chip chip-plain' }, GRADE_KH(x.grade)) : null,
            x.lesson && !(showLessons && S.lesson === x.lesson) ? h('span', { class: 'chip chip-plain' }, x.lesson) : null,
            x.topic ? h('span', { class: 'chip chip-plain' }, x.topic) : null,
            x.level ? h('span', { class: `chip ${x.level === 'hard' ? 'chip-closed' : x.level === 'pisa' ? 'chip-soon' : 'chip-open'}` }, LEVEL_KH[x.level]) : null,
            x.image_key ? h('span', { class: 'chip chip-plain' }, '🖼 រូបភាព') : null,
            h('span', { class: 'chip chip-plain' }, `${x.points} ពិន្ទុ`),
            h('span', { class: 'muted', style: 'font-size:12px;' }, x.test_title),
          ]),
        ]),
        h('button', { class: 'secondary btn-sm', onclick: (e) => { e.preventDefault(); e.stopPropagation(); openQuestionEditor(x, { id: x.test_id, submissions: 0 }, null, reload); } }, '✏️'),
      ]));
    });
    if (rows.length > 200) list.append(h('p', { class: 'muted' }, `បង្ហាញ ២០០ ដំបូង ក្នុងចំណោម ${rows.length} — សូមត្រងបន្ថែម។`));
    upd();
  }
  function upd() { countLbl.textContent = String(selected.size); addBtn.disabled = !selected.size; tagBtn.disabled = !selected.size; }
  [fLevel, fKind, fTopic].forEach((el) => el && el.addEventListener('change', draw));
  fQ.addEventListener('input', draw);

  // ---------- random generator for the chosen grade / lesson
  const gen = (() => {
    const title = h('input', { type: 'text', placeholder: 'ចំណងជើងតេស្តថ្មី ឧ. ប្រឡងមេរៀន ១៣–១៩ ថ្នាក់ទី ៧', style: 'flex:1;min-width:240px;' });
    const num = (v) => h('input', { type: 'number', min: '0', max: '100', value: String(v), style: 'width:80px;' });
    const nEasy = num(4), nMed = num(12), nHard = num(4), nPisa = num(0);
    const kind = h('select', { style: 'width:auto;' }, [h('option', { value: 'mcq' }, 'ពហុជ្រើសរើសប៉ុណ្ណោះ'), h('option', { value: 'all' }, 'ទាំងពហុជ្រើសរើស និងសរសេរ')]);
    const chosen = new Set(showLessons && S.lesson && S.lesson !== '-' ? [S.lesson] : []);
    const chips = showLessons ? h('div', { class: 'filter-bar', style: 'margin-top:8px;' }, lessonsOf(S.grade).filter((n) => count((q) => q.grade === S.grade && q.lesson === n)).map((n) => {
      const b = h('button', { class: `filter-pill${chosen.has(n) ? ' on' : ''}`, onclick: () => { chosen.has(n) ? chosen.delete(n) : chosen.add(n); b.classList.toggle('on'); } }, n); return b;
    })) : null;
    return h('details', { class: 'card' }, [
      h('summary', { style: 'cursor:pointer;font-weight:700;' }, `🎲 បង្កើតតេស្តចៃដន្យពីធនាគារ${S.grade && S.grade !== '-' ? ` (${GRADE_KH(S.grade)})` : ''}`),
      h('div', { class: 'row', style: 'margin-top:10px;' }, [title]),
      h('div', { class: 'row', style: 'margin-top:10px;' }, [h('span', {}, 'ងាយ'), nEasy, h('span', {}, 'មធ្យម'), nMed, h('span', {}, 'ពិបាក'), nHard, h('span', {}, 'PISA'), nPisa, kind]),
      showLessons ? h('div', {}, [h('label', {}, 'ជ្រើសមេរៀន (មិនជ្រើស = ទាំងអស់ក្នុងថ្នាក់នេះ)'), chips]) : h('p', { class: 'muted' }, 'ជ្រើសថ្នាក់ខាងលើ ដើម្បីជ្រើសតាមមេរៀន។'),
      h('div', { class: 'row', style: 'margin-top:12px;' }, [h('button', { onclick: async () => {
        if (!title.value.trim()) return title.focus();
        try {
          const r = await api('/api/bank/generate', { method: 'POST', body: { title: title.value, counts: { easy: Number(nEasy.value), medium: Number(nMed.value), hard: Number(nHard.value), pisa: Number(nPisa.value) }, grade: showLessons ? S.grade : '', lessons: [...chosen], kind: kind.value } });
          const short = Object.entries(r.shortage).map(([l, n]) => `${LEVEL_KH[l]} ខ្វះ ${n}`).join(' · ');
          await Exam.notify(`✅ បានបង្កើតតេស្តព្រាងមាន ${r.picked} សំណួរ។${short ? `\nចំណាំ៖ ${short}` : ''}`);
          selectedTestId = r.id;
          document.querySelector('[data-tab=tests]').click();
        } catch (e) { Exam.notify(e.message); }
      } }, '🎲 បង្កើតតេស្ត')]),
    ]);
  })();

  const main = h('div', { style: 'min-width:0;' }, [
    h('div', { class: 'card' }, [h('div', { class: 'row' }, [h('h2', { style: 'margin:0;margin-right:auto;' }, showLessons ? (S.lesson && S.lesson !== '-' ? S.lesson : GRADE_KH(S.grade)) : 'សំណួរ'), newBtn, importBtn]),
      h('div', { class: 'row', style: 'margin-top:10px;' }, [fLevel, fKind, fTopic, fQ, selAll])]),
    gen, bar, list,
  ]);
  container.append(showLessons ? h('div', { class: 'bank-layout' }, [side, main]) : main);
  draw();
};

// ---------- Excel import of questions (used in the test builder) ----------
const KH_LETTERS = { 'ក': 0, 'ខ': 1, 'គ': 2, 'ឃ': 3, 'ង': 4, 'ច': 5 };
function importQuestionsCard(test, container, onDone) {
  const status = h('div', { class: 'muted', style: 'margin-top:8px;' });
  const file = h('input', { type: 'file', accept: '.xlsx,.xls,.csv' });
  const levelOf = (v) => { const s = String(v || '').trim().toLowerCase(); return { 'ងាយ': 'easy', easy: 'easy', 'មធ្យម': 'medium', medium: 'medium', 'ពិបាក': 'hard', hard: 'hard', pisa: 'pisa' }[s] || null; };
  const pick = (r, ...names) => { for (const k of Object.keys(r)) { const nk = k.trim().toLowerCase(); if (names.includes(nk)) return r[k]; } return ''; };
  function toQuestion(r) {
    const writing = /writing|សរសេរ/i.test(String(pick(r, 'kind', 'type', 'ប្រភេទ')));
    const stem = String(pick(r, 'question', 'stem', 'សំណួរ')).trim();
    const opts = ['a', 'b', 'c', 'd', 'e', 'f'].map((l, i) => String(pick(r, l, ['ក', 'ខ', 'គ', 'ឃ', 'ង', 'ច'][i])).trim()).filter((x) => x !== '');
    let ci = -1;
    const c = String(pick(r, 'correct', 'answer', 'ចម្លើយ')).trim();
    if (/^[a-fA-F]$/.test(c)) ci = c.toLowerCase().charCodeAt(0) - 97; else if (c in KH_LETTERS) ci = KH_LETTERS[c]; else if (/^[1-6]$/.test(c)) ci = Number(c) - 1;
    return { kind: writing ? 'writing' : 'mcq', stem_text: stem, options: writing ? [] : opts, correct_index: ci, points: Number(pick(r, 'points', 'point', 'ពិន្ទុ')) || undefined,
      topic: String(pick(r, 'topic', 'ប្រធានបទ')).trim(), grade: String(pick(r, 'grade', 'ថ្នាក់')).replace(/\D/g, ''), lesson: String(pick(r, 'lesson', 'មេរៀន')).trim(), level: levelOf(pick(r, 'level', 'កម្រិត')), solution_text: String(pick(r, 'solution', 'ចម្លើយគំរូ')).trim() };
  }
  file.addEventListener('change', async () => {
    if (!file.files[0]) return;
    try {
      const wb = XLSX.read(await file.files[0].arrayBuffer(), { type: 'array' });
      const rows = XLSX.utils.sheet_to_json(wb.Sheets[wb.SheetNames[0]], { defval: '' });
      const qs = rows.map(toQuestion).filter((q) => q.stem_text);
      const bad = qs.filter((q) => q.kind === 'mcq' && (q.options.length < 2 || q.correct_index < 0 || q.correct_index >= q.options.length));
      if (!qs.length) return (status.textContent = 'រកមិនឃើញសំណួរក្នុងឯកសារទេ។ សូមប្រើគំរូ Excel។');
      if (!(await Exam.confirm(`នាំចូល ${qs.length - bad.length} សំណួរ${bad.length ? ` (រំលង ${bad.length} ដែលមិនពេញលេញ)` : ''} ទៅតេស្តនេះ?`))) return;
      const r = await api(`/api/tests/${test.id}/questions/bulk`, { method: 'POST', body: { questions: qs } });
      await Exam.notify(`✅ បាននាំចូល ${r.added} សំណួរ។`);
      (onDone || (() => renderTestBuilder(container)))();
    } catch (e) { status.textContent = e.message; }
  });
  const template = () => {
    const rows = [
      { kind: 'mcq', question: 'គណនា \\(2+3\\) ។', A: '4', B: '5', C: '6', D: '7', correct: 'B', points: 2, topic: 'ចំនួន', level: 'easy', grade: 7, lesson: 'ប្រភាគ', solution: '' },
      { kind: 'writing', question: 'ដោះស្រាយ \\(x+2=5\\) ។', A: '', B: '', C: '', D: '', correct: '', points: 5, topic: 'ពីជគណិត', level: 'medium', grade: 7, lesson: 'សមីការដឺក្រេទីមួយមានមួយអញ្ញាត', solution: '\\(x=3\\) (៥ ពិន្ទុ)' },
    ];
    const wb = XLSX.utils.book_new(); XLSX.utils.book_append_sheet(wb, XLSX.utils.json_to_sheet(rows), 'Questions'); XLSX.writeFile(wb, 'គំរូនាំចូលសំណួរ.xlsx');
  };
  return h('div', { class: 'card' }, [
    h('h3', {}, '📥 នាំចូលសំណួរច្រើនក្នុងពេលតែមួយពី Excel'),
    h('p', { class: 'muted' }, 'ទាញយកគំរូ បំពេញសំណួរ (kind=mcq ឬ writing · question · A–F · correct · points · topic · level · grade · lesson · solution) រួចជ្រើសឯកសារ។ អាចសរសេរគណិតជា \\(…\\) ។'),
    h('div', { class: 'row' }, [h('button', { class: 'secondary btn-sm', onclick: template }, '⬇ ទាញយកគំរូ Excel'), file]),
    status,
  ]);
}
