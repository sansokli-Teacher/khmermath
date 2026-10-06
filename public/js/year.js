// Yearly gradebook for the teacher: setup, score table, grade statistics.
let yearClassId = null;      // a class id, or 'all' (statistics only)
let yearMeasure = 'semester1';

const isGirl = (g) => /^(ស្រី|f|female|girl)$/i.test(String(g || '').trim());
const isBoy = (g) => /^(ប្រុស|m|male|boy)$/i.test(String(g || '').trim());
const fmtPct = (v) => (v == null ? '—' : String(Math.round(v * 10) / 10));

function yearMeasures(assessments) {
  const a = Object.fromEntries(assessments.map((x) => [x.key, x]));
  const lbl = (k) => (a[k] ? `${a[k].title} (${a[k].month_label})` : k);
  return [
    { key: 'pre', label: lbl('pre'), get: (s) => s.scores.pre?.pct },
    { key: 'm1', label: lbl('m1'), get: (s) => s.scores.m1?.pct },
    { key: 'm2', label: lbl('m2'), get: (s) => s.scores.m2?.pct },
    { key: 'monthly_avg', label: 'មធ្យមភាគប្រចាំខែ', get: (s) => s.monthly_avg },
    { key: 'sem1', label: lbl('sem1'), get: (s) => s.scores.sem1?.pct },
    { key: 'semester1', label: 'ពិន្ទុឆមាសទី១', get: (s) => s.semester1 },
    { key: 'final', label: lbl('final'), get: (s) => s.final },
    { key: 'year_avg', label: 'មធ្យមភាគប្រចាំឆ្នាំ', get: (s) => s.year_avg },
  ];
}

// grade × (total / girls / boys) for one measure
function gradeStats(students, measure) {
  const rows = Object.fromEntries(Exam.GRADES.map((g) => [g, { total: 0, girls: 0, boys: 0 }]));
  const vals = []; const girlVals = [];
  let missing = 0;
  for (const s of students) {
    const v = measure.get(s);
    if (v == null) { missing++; continue; }
    vals.push(v);
    const g = Exam.gradeOf(v).grade;
    rows[g].total++;
    if (isGirl(s.gender)) { rows[g].girls++; girlVals.push(v); } else if (isBoy(s.gender)) rows[g].boys++;
  }
  const n = vals.length;
  const pass = vals.filter((v) => Math.round(v) >= 50).length;
  const passGirls = girlVals.filter((v) => Math.round(v) >= 50).length;
  return {
    rows, n, missing, pass, passGirls, girlsN: girlVals.length,
    avg: n ? vals.reduce((a, b) => a + b, 0) / n : null,
    max: n ? Math.max(...vals) : null, min: n ? Math.min(...vals) : null,
  };
}

async function loadYearData(classId) {
  if (classId === 'all') {
    const { classes } = await api('/api/classes');
    const all = await Promise.all(classes.map((c) => api(`/api/year/class/${c.id}`)));
    return {
      class: { name: 'គ្រប់ថ្នាក់' },
      assessments: all[0] ? all[0].assessments : [],
      students: all.flatMap((d) => d.students.map((s) => ({ ...s, class_name: d.class.name }))),
      sessions: [], config: all[0] ? all[0].config : {}, readOnly: true,
    };
  }
  return api(`/api/year/class/${classId}`);
}

render.year = async function () {
  const container = document.getElementById('tab-year');
  container.innerHTML = '';
  const { classes } = await api('/api/classes');
  if (classes.length === 0) {
    container.append(h('div', { class: 'card' }, h('p', { class: 'muted' }, 'សូមបង្កើតថ្នាក់ជាមុនសិន។')));
    return;
  }
  if (yearClassId == null) yearClassId = classes[0].id;

  const picker = h('select', { style: 'max-width:260px;' }, [
    ...classes.map((c) => h('option', { value: c.id, selected: String(yearClassId) === String(c.id) ? 'selected' : null }, c.name)),
    h('option', { value: 'all', selected: yearClassId === 'all' ? 'selected' : null }, 'គ្រប់ថ្នាក់ (ស្ថិតិរួម)'),
  ]);
  picker.onchange = () => { yearClassId = picker.value === 'all' ? 'all' : Number(picker.value); render.year(); };
  container.append(h('div', { class: 'card no-print' }, [
    h('div', { class: 'row', style: 'justify-content:space-between;' }, [
      h('div', {}, [h('h2', { style: 'margin:0;' }, 'ពិន្ទុប្រចាំឆ្នាំសិក្សា'), h('div', { class: 'muted' }, 'បុរេតេស្ត · ប្រចាំខែ · ឆមាស · បញ្ចប់ឆ្នាំ')]),
      picker,
    ]),
  ]));

  const data = await loadYearData(yearClassId);
  const measures = yearMeasures(data.assessments);

  if (!data.readOnly) {
    container.append(setupCard(data));
    container.append(scoreTable(data));
  }
  container.append(statsCard(data, measures));
};

function setupCard(data) {
  const sessionOptions = (sel) => [
    h('option', { value: '' }, '— មិនទាន់ភ្ជាប់ —'),
    ...data.sessions.map((s) => h('option', { value: s.id, selected: Number(sel) === s.id ? 'selected' : null }, `${s.title} · ${fmtDateTime(s.scheduled_start)}`)),
  ];
  const rows = data.assessments.map((a) => {
    const title = h('input', { type: 'text', value: a.title, style: 'min-width:160px;' });
    const month = h('input', { type: 'text', value: a.month_label, style: 'width:90px;' });
    const src = a.kind === 'online'
      ? h('select', { style: 'min-width:220px;' }, sessionOptions(a.session_id))
      : h('input', { type: 'number', value: a.max_score, title: 'ពិន្ទុអតិបរមា', style: 'width:80px;' });
    const inMonthly = h('input', { type: 'checkbox', checked: a.in_monthly ? 'checked' : null });
    const published = h('input', { type: 'checkbox', checked: a.published ? 'checked' : null });
    const save = h('button', { class: 'secondary btn-sm', onclick: async () => {
      try {
        await api(`/api/year/assessment/${a.id}`, { method: 'POST', body: {
          title: title.value, month_label: month.value,
          session_id: a.kind === 'online' ? src.value : null,
          max_score: a.kind === 'manual' ? src.value : a.max_score,
          in_monthly: inMonthly.checked, published: published.checked,
        } });
        await Exam.notify('បានរក្សាទុក។');
        render.year();
      } catch (e) { Exam.notify(e.message); }
    } }, 'រក្សាទុក');
    const field = (lbl, el) => h('div', { class: 'setup-field' }, [h('label', {}, lbl), el]);
    return h('div', { class: 'setup-row' }, [
      h('div', { class: 'setup-kind' }, h('span', { class: 'badge draft' }, a.kind === 'online' ? 'ក្នុងប្រព័ន្ធ' : 'វាយដោយដៃ')),
      field('ឈ្មោះ', title), field('ខែ', month),
      field(a.kind === 'online' ? 'ភ្ជាប់ទៅការប្រឡង' : 'ពិន្ទុអតិបរមា', src),
      a.kind === 'online' ? h('label', { class: 'setup-check' }, [inMonthly, ' រាប់ក្នុងមធ្យមខែ']) : null,
      h('label', { class: 'setup-check' }, [published, ' ផ្សាយឱ្យសិស្ស']),
      save,
    ]);
  });
  const label = h('input', { type: 'text', value: data.config.label, style: 'width:140px;' });
  const mw = h('input', { type: 'number', value: data.config.monthly_weight, style: 'width:80px;' });
  const ew = h('input', { type: 'number', value: data.config.exam_weight, style: 'width:80px;' });

  const body = h('div', { style: 'margin-top:12px;' }, [
    ...rows,
    h('div', { class: 'row', style: 'margin-top:14px;' }, [
      h('span', {}, 'ឆ្នាំសិក្សា'), label,
      h('span', { style: 'margin-left:10px;' }, 'ឆមាស = មធ្យមខែ'), mw, h('span', {}, '% + ប្រឡងឆមាស'), ew, h('span', {}, '%'),
      h('button', { onclick: async () => {
        try {
          await api('/api/year/config', { method: 'POST', body: { label: label.value, monthly_weight: mw.value, exam_weight: ew.value } });
          await Exam.notify('បានរក្សាទុក។');
          render.year();
        } catch (e) { Exam.notify(e.message); }
      } }, 'រក្សាទុកការកំណត់'),
    ]),
    h('p', { class: 'muted', style: 'margin-top:10px;' }, 'ប្រឡងក្នុងប្រព័ន្ធ៖ ភ្ជាប់ទៅការប្រឡងដែលបានកំណត់ពេល ហើយពិន្ទុនឹងមកដោយស្វ័យប្រវត្តិ។ ប្រឡងវាយដោយដៃ៖ បញ្ចូលក្នុងតារាងខាងក្រោម។ សិស្សឃើញពិន្ទុតែពេលលោកគ្រូ «ផ្សាយ» ប៉ុណ្ណោះ។'),
  ]);
  const card = h('div', { class: 'card no-print' }, [
    h('div', { class: 'row', style: 'justify-content:space-between;' }, [h('h2', { style: 'margin:0;' }, '⚙ ការកំណត់ឆ្នាំសិក្សា'), h('button', { class: 'secondary btn-sm', onclick: () => { body.hidden = !body.hidden; } }, 'បង្ហាញ/លាក់')]),
    body,
  ]);
  // Collapse once the five assessments are set up.
  body.hidden = data.assessments.filter((a) => a.kind === 'online').every((a) => a.session_id);
  return card;
}

function scoreTable(data) {
  const A = Object.fromEntries(data.assessments.map((a) => [a.key, a]));
  const manualInputs = [];
  const manualCell = (s, key) => {
    const sc = s.scores[key];
    const inp = h('input', { type: 'number', value: sc ? sc.raw : '', step: 'any', style: 'width:72px;padding:6px 8px;', 'data-student': s.id, 'data-key': key });
    manualInputs.push(inp);
    return h('td', {}, [inp, h('span', { class: 'muted' }, ` /${A[key].max_score}`)]);
  };
  const pctCell = (v, strong) => {
    const g = Exam.gradeOf(v);
    return h('td', { style: strong ? 'font-weight:700;background:#f4f8ff;' : '' }, v == null ? '—' : [fmtPct(v), g ? h('span', { class: 'muted', style: `margin-left:5px;color:${g.color};font-weight:700;` }, g.grade) : null]);
  };
  const head = ['ល.រ', 'អត្តលេខ', 'ឈ្មោះសិស្ស', 'ភេទ',
    `${A.pre.month_label}`, `${A.m1.month_label}`, `${A.m2.month_label}`, 'មធ្យមខែ',
    `ប្រឡងឆមាស (${A.sem1.month_label})`, 'ពិន្ទុឆមាសទី១', `បញ្ចប់ឆ្នាំ (${A.final.month_label})`, 'មធ្យមឆ្នាំ'];
  const rows = data.students.map((s, i) => h('tr', {}, [
    h('td', { class: 'muted' }, i + 1), h('td', {}, h('strong', {}, s.id)), h('td', {}, `${s.surname} ${s.first_name}`), h('td', {}, s.gender || '—'),
    pctCell(s.scores.pre?.pct), pctCell(s.scores.m1?.pct), pctCell(s.scores.m2?.pct), pctCell(s.monthly_avg, true),
    manualCell(s, 'sem1'), pctCell(s.semester1, true), manualCell(s, 'final'), pctCell(s.year_avg, true),
  ]));
  const save = h('button', { onclick: async () => {
    try {
      for (const key of ['sem1', 'final']) {
        const scores = manualInputs.filter((i) => i.dataset.key === key).map((i) => ({ student_id: i.dataset.student, score: i.value === '' ? null : Number(i.value) }));
        await api(`/api/year/assessment/${A[key].id}/scores`, { method: 'POST', body: { scores } });
      }
      await Exam.notify('បានរក្សាទុកពិន្ទុរួចរាល់!');
      render.year();
    } catch (e) { Exam.notify(e.message); }
  } }, '💾 រក្សាទុកពិន្ទុ');
  return h('div', { class: 'card', style: 'overflow-x:auto;' }, [
    h('h2', {}, `តារាងពិន្ទុ — ${data.class.name}`),
    data.students.length === 0 ? h('p', { class: 'muted' }, 'ថ្នាក់នេះមិនទាន់មានសិស្សទេ។') : h('table', {}, [
      h('thead', {}, h('tr', {}, head.map((t) => h('th', {}, t)))), h('tbody', {}, rows),
    ]),
    h('div', { class: 'row no-print', style: 'margin-top:14px;justify-content:flex-end;' }, [
      h('button', { class: 'secondary', onclick: () => window.print() }, '🖨 បោះពុម្ព'),
      save,
    ]),
  ]);
}

function statsCard(data, measures) {
  const measure = measures.find((m) => m.key === yearMeasure) || measures[5];
  const pick = h('select', { style: 'max-width:340px;' }, measures.map((m) => h('option', { value: m.key, selected: m.key === measure.key ? 'selected' : null }, m.label)));
  pick.onchange = () => { yearMeasure = pick.value; render.year(); };
  const st = gradeStats(data.students, measure);
  const girlsTotal = data.students.filter((s) => isGirl(s.gender)).length;
  const unknownGender = data.students.filter((s) => !isGirl(s.gender) && !isBoy(s.gender)).length;
  const maxRow = Math.max(1, ...Exam.GRADES.map((g) => st.rows[g].total));

  const rows = Exam.GRADES.map((g) => {
    const r = st.rows[g]; const info = Exam.gradeOf({ A: 90, B: 80, C: 70, D: 55, E: 45, F: 0 }[g]);
    return h('tr', {}, [
      h('td', {}, h('span', { class: 'grade-dot', style: `background:${info.color};` }, g)),
      h('td', { style: 'font-weight:700;' }, r.total),
      h('td', { style: 'color:#db2777;font-weight:700;' }, r.girls),
      h('td', { style: 'color:#0284c7;font-weight:700;' }, r.boys),
      h('td', { class: 'muted' }, st.n ? `${Math.round((r.total / st.n) * 100)}%` : '—'),
      h('td', { style: 'width:34%;' }, h('div', { class: 'gbar' }, [
        h('div', { class: 'gbar-g', style: `width:${(r.girls / maxRow) * 100}%;` }),
        h('div', { class: 'gbar-b', style: `width:${(r.boys / maxRow) * 100}%;` }),
        h('div', { class: 'gbar-o', style: `width:${((r.total - r.girls - r.boys) / maxRow) * 100}%;` }),
      ])),
    ]);
  });

  const stat = (label, value) => h('div', { class: 'stat-tile' }, [h('div', { class: 'stat-val' }, value), h('div', { class: 'muted' }, label)]);
  const exportBtn = h('button', { class: 'secondary btn-sm', onclick: () => exportYearExcel(data, measures) }, '📥 ទាញយក Excel ទាំងឆ្នាំ');
  return h('div', { class: 'card' }, [
    h('div', { class: 'row no-print', style: 'justify-content:space-between;' }, [h('h2', { style: 'margin:0;' }, '📊 ស្ថិតិនិទ្ទេស A · B · C … តាមភេទ'), exportBtn]),
    h('div', { class: 'row no-print', style: 'margin:10px 0;' }, [h('span', { class: 'muted' }, 'ពិន្ទុ៖'), pick]),
    h('h3', { class: 'print-only' }, `${data.class.name} — ${measure.label}`),
    h('div', { class: 'stat-grid' }, [
      stat('សិស្សមានពិន្ទុ', `${st.n} / ${data.students.length}`),
      stat('មធ្យមភាគ', fmtPct(st.avg)),
      stat('ខ្ពស់បំផុត / ទាបបំផុត', st.n ? `${fmtPct(st.max)} / ${fmtPct(st.min)}` : '—'),
      stat('ជាប់ (≥50)', st.n ? `${st.pass} (${Math.round((st.pass / st.n) * 100)}%)` : '—'),
      stat(`ស្រីជាប់ (ស្រីសរុប ${girlsTotal})`, st.girlsN ? `${st.passGirls} / ${st.girlsN}` : '—'),
    ]),
    st.n === 0 ? h('p', { class: 'muted' }, 'មិនទាន់មានពិន្ទុសម្រាប់ប្រភេទនេះទេ។') : h('div', { style: 'overflow-x:auto;' }, h('table', {}, [
      h('thead', {}, h('tr', {}, ['និទ្ទេស', 'សរុប', 'ស្រី', 'ប្រុស', '%', ''].map((t) => h('th', {}, t)))),
      h('tbody', {}, rows),
    ])),
    h('div', { class: 'muted', style: 'margin-top:8px;' }, [
      h('span', { style: 'color:#ec6aa8;' }, '■ '), 'ស្រី', h('span', { style: 'color:#4aa3e0;margin-left:10px;' }, '■ '), 'ប្រុស', h('span', { style: 'color:#a9b6c6;margin-left:10px;' }, '■ '), 'មិនបញ្ជាក់ភេទ',
      st.missing ? `  ·  ${st.missing} នាក់មិនទាន់មានពិន្ទុ` : '',
      unknownGender ? `  ·  ${unknownGender} នាក់មិនបានបញ្ជាក់ភេទ` : '',
      '  ·  និទ្ទេស៖ A ≥85 · B ≥75 · C ≥65 · D ≥50 · E ≥40 · F <40',
    ]),
  ]);
}

function exportYearExcel(data, measures) {
  if (typeof XLSX === 'undefined') return Exam.notify('មិនទាន់ដំណើរការបណ្ណាល័យ Excel នៅឡើយទេ។');
  const wb = XLSX.utils.book_new();
  const multi = data.students.some((s) => s.class_name);
  const head = [...(multi ? ['ថ្នាក់'] : []), 'ល.រ', 'អត្តលេខ', 'គោត្តនាម', 'នាម', 'ភេទ', ...measures.map((m) => m.label), 'និទ្ទេសឆមាសទី១', 'និទ្ទេសប្រចាំឆ្នាំ'];
  const rows = [head];
  data.students.forEach((s, i) => {
    rows.push([
      ...(multi ? [s.class_name] : []), i + 1, s.id, s.surname, s.first_name, s.gender || '—',
      ...measures.map((m) => { const v = m.get(s); return v == null ? '' : Math.round(v * 10) / 10; }),
      Exam.gradeOf(s.semester1)?.grade || '', Exam.gradeOf(s.year_avg)?.grade || '',
    ]);
  });
  XLSX.utils.book_append_sheet(wb, XLSX.utils.aoa_to_sheet(rows), 'ពិន្ទុ');

  const stat = [['ពិន្ទុ', 'និទ្ទេស', 'សរុប', 'ស្រី', 'ប្រុស']];
  for (const m of measures) {
    const st = gradeStats(data.students, m);
    for (const g of Exam.GRADES) stat.push([m.label, g, st.rows[g].total, st.rows[g].girls, st.rows[g].boys]);
  }
  XLSX.utils.book_append_sheet(wb, XLSX.utils.aoa_to_sheet(stat), 'ស្ថិតិនិទ្ទេស');
  XLSX.writeFile(wb, `ពិន្ទុប្រចាំឆ្នាំ_${data.class.name}.xlsx`);
}
