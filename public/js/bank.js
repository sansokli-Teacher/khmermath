// Question bank (reuse + random test builder) and Excel import of questions.
const LEVEL_KH = { easy: 'ងាយ', medium: 'មធ្យម', hard: 'ពិបាក' };
let bankFilter = { topic: '', level: '', kind: '', q: '' };

render.bank = async function () {
  const container = document.getElementById('tab-bank');
  container.innerHTML = '';
  const [{ questions }, { tests }] = await Promise.all([api('/api/bank'), api('/api/tests')]);
  const editable = tests.filter((t) => (t.my_role === 'owner' || t.my_role === 'editor') && !t.is_sample);
  const topics = [...new Set(questions.map((q) => q.topic).filter(Boolean))].sort();
  const selected = new Set();

  // ---- overview matrix: topic × level
  const cell = (tp, lv) => questions.filter((q) => (tp === null ? true : (q.topic || '') === tp) && (lv === null ? true : q.level === lv)).length;
  const rowsTopics = [...topics, ''];
  const matrix = h('div', { style: 'overflow-x:auto;' }, h('table', {}, [
    h('thead', {}, h('tr', {}, ['ប្រធានបទ', 'ងាយ', 'មធ្យម', 'ពិបាក', 'មិនកំណត់កម្រិត', 'សរុប'].map((x) => h('th', {}, x)))),
    h('tbody', {}, rowsTopics.filter((tp) => cell(tp, null)).map((tp) => h('tr', {}, [
      h('td', {}, tp || h('span', { class: 'muted' }, '(មិនទាន់កំណត់ប្រធានបទ)')),
      ...['easy', 'medium', 'hard'].map((lv) => h('td', {}, cell(tp, lv) || '—')),
      h('td', {}, questions.filter((q) => (q.topic || '') === tp && !q.level).length || '—'),
      h('td', {}, h('strong', {}, cell(tp, null))),
    ]))),
  ]));

  container.append(h('div', { class: 'card' }, [
    h('h2', {}, `🗂 ធនាគារសំណួរ (${questions.length})`),
    h('p', { class: 'muted' }, 'សំណួរទាំងអស់ពីតេស្តរបស់អ្នក — ប្រើឡើងវិញក្នុងតេស្តថ្មី ឬឱ្យប្រព័ន្ធជ្រើសចៃដន្យតាមកម្រិត។ ដាក់ «ប្រធានបទ» និង «កម្រិត» ពេលកែសំណួរ ដើម្បីឱ្យធនាគារមានប្រយោជន៍។'),
    questions.length ? matrix : h('p', { class: 'muted' }, 'មិនទាន់មានសំណួរទេ — បង្កើតតេស្តជាមុនសិន។'),
  ]));

  // ---- random generator
  const title = h('input', { type: 'text', placeholder: 'ចំណងជើងតេស្តថ្មី ឧ. ប្រឡងប្រចាំខែធ្នូ ថ្នាក់ទី ៧', style: 'flex:1;min-width:240px;' });
  const num = (v) => h('input', { type: 'number', min: '0', max: '100', value: String(v), style: 'width:80px;' });
  const nEasy = num(4), nMed = num(12), nHard = num(4);
  const kind = h('select', { style: 'width:auto;' }, [h('option', { value: 'mcq' }, 'ពហុជ្រើសរើសប៉ុណ្ណោះ'), h('option', { value: 'all' }, 'ទាំងពហុជ្រើសរើស និងសរសេរ')]);
  const chosenTopics = new Set();
  const topicChips = h('div', { class: 'filter-bar', style: 'margin-top:8px;' }, topics.map((tp) => {
    const b = h('button', { class: 'filter-pill', onclick: () => { chosenTopics.has(tp) ? chosenTopics.delete(tp) : chosenTopics.add(tp); b.classList.toggle('on'); } }, tp);
    return b;
  }));
  container.append(h('div', { class: 'card' }, [
    h('h2', {}, '🎲 បង្កើតតេស្តពីធនាគារដោយចៃដន្យ'),
    h('div', { class: 'row' }, [title]),
    h('div', { class: 'row', style: 'margin-top:10px;' }, [h('span', {}, 'ងាយ'), nEasy, h('span', {}, 'មធ្យម'), nMed, h('span', {}, 'ពិបាក'), nHard, kind]),
    topics.length ? h('div', {}, [h('label', {}, 'ជ្រើសរើសប្រធានបទ (មិនជ្រើស = ទាំងអស់)'), topicChips]) : null,
    h('div', { class: 'row', style: 'margin-top:12px;' }, [h('button', { onclick: async () => {
      if (!title.value.trim()) return title.focus();
      try {
        const r = await api('/api/bank/generate', { method: 'POST', body: { title: title.value, counts: { easy: Number(nEasy.value), medium: Number(nMed.value), hard: Number(nHard.value) }, topics: [...chosenTopics], kind: kind.value } });
        const short = Object.entries(r.shortage).map(([l, n]) => `${LEVEL_KH[l]} ខ្វះ ${n}`).join(' · ');
        await Exam.notify(`✅ បានបង្កើតតេស្តព្រាងមាន ${r.picked} សំណួរ។${short ? `\nចំណាំ៖ ${short}` : ''}`);
        selectedTestId = r.id;
        document.querySelector('[data-tab=tests]').click();
      } catch (e) { Exam.notify(e.message); }
    } }, '🎲 បង្កើតតេស្ត')]),
  ]));

  // ---- browse + copy
  const list = h('div', { class: 'test-list' });
  const bar = h('div', { class: 'bank-bar' });
  const targetSel = h('select', { style: 'width:auto;max-width:260px;' }, editable.map((t) => h('option', { value: t.id }, t.title)));
  const countLbl = h('b', {}, '0');
  const addBtn = h('button', { disabled: 'disabled', onclick: async () => {
    if (!targetSel.value) return Exam.notify('សូមបង្កើតតេស្តមួយជាមុនសិន។');
    try { const r = await api(`/api/tests/${targetSel.value}/questions/copy`, { method: 'POST', body: { question_ids: [...selected] } }); await Exam.notify(`✅ បានថែម ${r.copied} សំណួរ។`); selected.clear(); draw(); } catch (e) { Exam.notify(e.message); }
  } }, '➕ ថែមទៅតេស្ត');
  bar.append(h('span', {}, ['បានជ្រើស ', countLbl, ' សំណួរ']), targetSel, addBtn);
  const f = bankFilter;
  const fTopic = h('select', { style: 'width:auto;' }, [h('option', { value: '' }, 'គ្រប់ប្រធានបទ'), ...topics.map((t) => h('option', { value: t, selected: f.topic === t ? 'selected' : null }, t))]);
  const fLevel = h('select', { style: 'width:auto;' }, [['', 'គ្រប់កម្រិត'], ['easy', 'ងាយ'], ['medium', 'មធ្យម'], ['hard', 'ពិបាក']].map(([v, l]) => h('option', { value: v, selected: f.level === v ? 'selected' : null }, l)));
  const fKind = h('select', { style: 'width:auto;' }, [['', 'គ្រប់ប្រភេទ'], ['mcq', 'ពហុជ្រើសរើស'], ['writing', 'សរសេរ']].map(([v, l]) => h('option', { value: v, selected: f.kind === v ? 'selected' : null }, l)));
  const fQ = h('input', { type: 'text', placeholder: '🔍 ស្វែងរក…', value: f.q, style: 'max-width:220px;' });
  function draw() {
    Object.assign(bankFilter, { topic: fTopic.value, level: fLevel.value, kind: fKind.value, q: fQ.value });
    const q = fQ.value.trim().toLowerCase();
    const rows = questions.filter((x) => (!fTopic.value || x.topic === fTopic.value) && (!fLevel.value || x.level === fLevel.value) && (!fKind.value || x.kind === fKind.value) && (!q || x.stem_text.toLowerCase().includes(q)));
    list.innerHTML = '';
    if (!rows.length) list.append(h('div', { class: 'empty-card' }, h('div', { class: 'muted' }, 'រកមិនឃើញសំណួរទេ។')));
    rows.slice(0, 200).forEach((x) => {
      const cb = h('input', { type: 'checkbox', style: 'width:20px;height:20px;flex:none;', checked: selected.has(x.id) ? 'checked' : null, onchange: () => { cb.checked ? selected.add(x.id) : selected.delete(x.id); upd(); } });
      list.append(h('label', { class: 'bank-item' }, [
        cb,
        h('div', { style: 'min-width:0;flex:1;' }, [
          mathEl('div', { class: 'bank-stem' }, x.stem_text),
          h('div', { class: 'test-chips' }, [
            x.kind === 'writing' ? h('span', { class: 'chip chip-soon' }, '✎ សរសេរ') : h('span', { class: 'chip chip-plain' }, 'ពហុជ្រើសរើស'),
            x.topic ? h('span', { class: 'chip chip-plain' }, x.topic) : null,
            x.level ? h('span', { class: `chip ${x.level === 'hard' ? 'chip-closed' : 'chip-open'}` }, LEVEL_KH[x.level]) : null,
            x.image_key ? h('span', { class: 'chip chip-plain' }, '🖼 រូបភាព') : null,
            h('span', { class: 'chip chip-plain' }, `${x.points} ពិន្ទុ`),
            h('span', { class: 'muted', style: 'font-size:12px;' }, x.test_title),
          ]),
        ]),
      ]));
    });
    if (rows.length > 200) list.append(h('p', { class: 'muted' }, `បង្ហាញ ២០០ ដំបូង ក្នុងចំណោម ${rows.length} — សូមត្រងបន្ថែម។`));
    upd();
  }
  function upd() { countLbl.textContent = String(selected.size); addBtn.disabled = !selected.size; }
  [fTopic, fLevel, fKind].forEach((el) => el.addEventListener('change', draw));
  fQ.addEventListener('input', draw);
  container.append(h('div', { class: 'card' }, [h('div', { class: 'row' }, [h('h2', { style: 'margin:0;margin-right:auto;' }, 'ស្វែងរក និងជ្រើសរើសសំណួរ'), fTopic, fLevel, fKind, fQ])]), bar, list);
  draw();
};

// ---------- Excel import of questions (used in the test builder) ----------
const KH_LETTERS = { 'ក': 0, 'ខ': 1, 'គ': 2, 'ឃ': 3, 'ង': 4, 'ច': 5 };
function importQuestionsCard(test, container) {
  const status = h('div', { class: 'muted', style: 'margin-top:8px;' });
  const file = h('input', { type: 'file', accept: '.xlsx,.xls,.csv' });
  const levelOf = (v) => { const s = String(v || '').trim().toLowerCase(); return { 'ងាយ': 'easy', easy: 'easy', 'មធ្យម': 'medium', medium: 'medium', 'ពិបាក': 'hard', hard: 'hard' }[s] || null; };
  const pick = (r, ...names) => { for (const k of Object.keys(r)) { const nk = k.trim().toLowerCase(); if (names.includes(nk)) return r[k]; } return ''; };
  function toQuestion(r) {
    const writing = /writing|សរសេរ/i.test(String(pick(r, 'kind', 'type', 'ប្រភេទ')));
    const stem = String(pick(r, 'question', 'stem', 'សំណួរ')).trim();
    const opts = ['a', 'b', 'c', 'd', 'e', 'f'].map((l, i) => String(pick(r, l, ['ក', 'ខ', 'គ', 'ឃ', 'ង', 'ច'][i])).trim()).filter((x) => x !== '');
    let ci = -1;
    const c = String(pick(r, 'correct', 'answer', 'ចម្លើយ')).trim();
    if (/^[a-fA-F]$/.test(c)) ci = c.toLowerCase().charCodeAt(0) - 97; else if (c in KH_LETTERS) ci = KH_LETTERS[c]; else if (/^[1-6]$/.test(c)) ci = Number(c) - 1;
    return { kind: writing ? 'writing' : 'mcq', stem_text: stem, options: writing ? [] : opts, correct_index: ci, points: Number(pick(r, 'points', 'point', 'ពិន្ទុ')) || undefined,
      topic: String(pick(r, 'topic', 'ប្រធានបទ')).trim(), level: levelOf(pick(r, 'level', 'កម្រិត')), solution_text: String(pick(r, 'solution', 'ចម្លើយគំរូ')).trim() };
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
      renderTestBuilder(container);
    } catch (e) { status.textContent = e.message; }
  });
  const template = () => {
    const rows = [
      { kind: 'mcq', question: 'គណនា \\(2+3\\) ។', A: '4', B: '5', C: '6', D: '7', correct: 'B', points: 2, topic: 'ចំនួន', level: 'easy', solution: '' },
      { kind: 'writing', question: 'ដោះស្រាយ \\(x+2=5\\) ។', A: '', B: '', C: '', D: '', correct: '', points: 5, topic: 'ពីជគណិត', level: 'medium', solution: '\\(x=3\\) (៥ ពិន្ទុ)' },
    ];
    const wb = XLSX.utils.book_new(); XLSX.utils.book_append_sheet(wb, XLSX.utils.json_to_sheet(rows), 'Questions'); XLSX.writeFile(wb, 'គំរូនាំចូលសំណួរ.xlsx');
  };
  return h('div', { class: 'card' }, [
    h('h3', {}, '📥 នាំចូលសំណួរច្រើនក្នុងពេលតែមួយពី Excel'),
    h('p', { class: 'muted' }, 'ទាញយកគំរូ បំពេញសំណួរ (kind=mcq ឬ writing · question · A–F · correct · points · topic · level · solution) រួចជ្រើសឯកសារ។ អាចសរសេរគណិតជា \\(…\\) ។'),
    h('div', { class: 'row' }, [h('button', { class: 'secondary btn-sm', onclick: template }, '⬇ ទាញយកគំរូ Excel'), file]),
    status,
  ]);
}
