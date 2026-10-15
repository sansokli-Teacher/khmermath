const { h, api } = Exam;
const params = new URLSearchParams(location.search);
const TEST_ID = params.get('test');
const LETTERS = ['ក', 'ខ', 'គ', 'ឃ', 'ង', 'ច'];
const LEVEL_LABELS = [['easy', 'កម្រិត ១៖ ចំណេះដឹងមូលដ្ឋាន'], ['medium', 'កម្រិត ២៖ ការគណនា និងអនុវត្ត'], ['hard', 'កម្រិត ៣៖ ការវិភាគ និងដោះស្រាយបញ្ហា'], ['pisa', 'កម្រិត ៤៖ បែប PISA']];
const KH_DIGITS = '០១២៣៤៥៦៧៨៩';
const kh = (n) => String(n).replace(/\d/g, (d) => KH_DIGITS[d]);
const ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV'];

function mathEl(tag, attrs, text) {
  const el = h(tag, attrs);
  el.innerHTML = Exam.mathHtml(text);
  return el;
}

let test = null;
let profile = {};

// "ក) …" lines of a writing question become indented sub-questions, like the NGS template
function splitWriting(stem) {
  const intro = []; const subs = [];
  for (const line of String(stem).split('\n')) {
    const m = line.match(/^\s*([ក-ឃង-ច])\s*[\)\.]\s*(.*)$/);
    if (m) subs.push({ l: m[1], t: m[2] });
    else if (subs.length) subs[subs.length - 1].t += `\n${line}`;
    else intro.push(line);
  }
  return { intro: intro.join('\n').trim(), subs };
}

const logoSrc = () => (profile.logo ? (profile.logo.startsWith('/') ? profile.logo : `/api/images/${profile.logo}`) : '');

function headerEl() {
  const right = [];
  if (profile.website) right.push(h('div', {}, ['Website: ', h('b', {}, h('i', {}, profile.website))]));
  if (profile.facebook) right.push(h('div', {}, ['Facebook: ', h('b', {}, h('i', {}, profile.facebook))]));
  return h('div', { class: 'ph' }, [
    h('div', { class: 'ph-left' }, [logoSrc() ? h('img', { src: logoSrc(), alt: '' }) : null, h('div', {}, profile.school || '')]),
    h('div', { class: 'ph-right' }, right),
  ]);
}
function footerEl() {
  const parts = [];
  if (profile.teacher) parts.push(h('span', { class: 't' }, profile.teacher));
  if (profile.email) parts.push(h('span', {}, ['Email: ', h('b', {}, h('i', {}, profile.email))]));
  if (profile.telegram) parts.push(h('span', {}, ['Telegram: ', h('b', {}, h('i', {}, profile.telegram))]));
  if (profile.tel) parts.push(h('span', {}, `Tel: ${profile.tel}`));
  return h('div', { class: 'pf' }, parts);
}

function examDoc(o) {
  const { minutes, date, space } = o;
  const mcq = test.questions.filter((q) => q.kind !== 'writing');
  const writing = test.questions.filter((q) => q.kind === 'writing');
  const mcqPts = mcq.reduce((a, q) => a + q.points, 0), wPts = writing.reduce((a, q) => a + q.points, 0);
  const kids = [];
  kids.push(h('div', { class: 'etitle' }, [
    h('div', { class: 't1' }, test.title),
    date ? h('div', { class: 't2' }, `សម័យប្រឡង ${date}`) : null,
    h('div', { class: 't3' }, `វិញ្ញាសា ${profile.subject || 'គណិតវិទ្យា'}`),
  ]));
  kids.push(h('div', { class: 'p-meta' }, [h('span', {}, ['រយៈពេល៖ ', h('b', {}, `${kh(minutes)} នាទី`)]), h('span', {}, ['ពិន្ទុសរុប៖ ', h('b', {}, `${kh(mcqPts + wPts)} ពិន្ទុ`)])]));
  kids.push(h('div', { class: 'p-student' }, [
    h('div', { class: 'f wide' }, ['ឈ្មោះ៖ ', h('i', { class: 'p-line' })]),
    h('div', { class: 'f' }, ['ថ្នាក់៖ ', h('i', { class: 'p-line' })]),
    h('div', { class: 'f' }, ['លេខ៖ ', h('i', { class: 'p-line' })]),
  ]));
  kids.push(h('div', { class: 'p-instr' }, `សម្គាល់៖ សូមអានសំណួរឱ្យបានល្អិតល្អន់។ ${mcq.length ? `ផ្នែក ក ជ្រើសរើសចម្លើយត្រឹមត្រូវ (${kh(mcqPts)} ពិន្ទុ)។ ` : ''}${writing.length ? `ផ្នែក ខ សរសេរចម្លើយលើក្រដាសឆ្លើយ ដោយបង្ហាញវិធីដោះស្រាយ (${kh(wPts)} ពិន្ទុ)។ ` : ''}មិនអនុញ្ញាតឱ្យប្រើទូរស័ព្ទ ឬម៉ាស៊ីនគិតលេខទេ។`));

  const tagged = mcq.some((q) => q.level);
  const grouped = !!(o.group && tagged);
  const optCount = Math.min(5, Math.max(4, ...mcq.map((q) => q.options.length)));
  if (mcq.length) {
    kids.push(h('div', { class: 'p-part' }, [`ផ្នែក ក · ពហុជ្រើសរើស `, h('small', {}, `(${kh(mcq.length)} សំណួរ × ${kh(mcq[0].points)} ពិន្ទុ)`)]));
    let no = 0;
    const drawQ = (q) => {
      const i = no++;
      const long = q.options.some((x) => x.length > 22);
      kids.push(h('div', { class: 'p-q' }, [
        h('div', { class: 'n' }, `${kh(i + 1)}.`),
        h('div', {}, [
          mathEl('div', { class: 'p-stem' }, q.stem_text),
          q.image_key ? h('img', { src: `/api/images/${q.image_key}`, alt: '' }) : null,
          h('div', { class: `p-opts${long ? ' two' : ''}` }, q.options.map((x, j) => h('div', { class: 'p-opt' }, [h('b', {}, `${LETTERS[j]}.`), mathEl('span', {}, x)]))),
        ]),
      ]));
    };
    if (grouped) {
      LEVEL_LABELS.forEach(([lv, label]) => {
        const grp = mcq.filter((q) => q.level === lv);
        if (!grp.length) return;
        kids.push(h('div', { class: 'p-lvl' }, `${label} (${kh(grp.length)} សំណួរ × ${kh(grp[0].points)} ពិន្ទុ)`));
        grp.forEach(drawQ);
      });
      mcq.filter((q) => !q.level).forEach(drawQ);
    } else mcq.forEach(drawQ);
  }
  if (writing.length) {
    kids.push(h('div', { class: 'p-part' }, [`ផ្នែក ខ · សរសេរ `, h('small', {}, `(${kh(writing.length)} សំណួរ · ${kh(wPts)} ពិន្ទុ)`)]));
    writing.forEach((q, i) => {
      const { intro, subs } = splitWriting(q.stem_text);
      kids.push(h('div', { class: 'wblock' }, [
        h('div', { class: 'sect' }, [h('span', { class: 'rn' }, `${ROMAN[i] || i + 1}.`), h('span', { class: 'sc' }, `(${kh(q.points)}ពិន្ទុ)`), mathEl('span', { class: 'st' }, intro || (subs.length ? '' : q.stem_text))]),
        ...subs.map((s) => h('div', { class: 'sq' }, [h('span', { class: 'n' }, `${s.l}.`), mathEl('span', { class: 't' }, s.t)])),
        q.image_key ? h('img', { src: `/api/images/${q.image_key}`, alt: '' }) : null,
        (space && !o.omr) ? h('div', { class: 'p-space', style: `height:${Math.max(24, q.points * 4.5)}mm;` }) : null,
      ]));
    });
  }
  if (o.omr && mcq.length) {
    kids.push(h('div', { class: 'pt-break' }));
    kids.push(OMR.sheetEl(h, { nQ: mcq.length, optCount, idDigits: o.idDigits, testId: test.id, grouped, letters: 'khmer', title: test.title, subtitle: 'សន្លឹកចម្លើយ OMR' }));
  }
  if (o.omr && writing.length) {
    kids.push(h('div', { class: 'pt-break' }));
    kids.push(h('div', { class: 'pt-title' }, [h('div', { class: 'a' }, 'សន្លឹកសរសេរចម្លើយ'), h('div', { class: 'b' }, test.title)]));
    kids.push(h('div', { class: 'p-student' }, [
      h('div', { class: 'f wide' }, ['ឈ្មោះ៖ ', h('i', { class: 'p-line' })]),
      h('div', { class: 'f' }, ['ថ្នាក់៖ ', h('i', { class: 'p-line' })]),
      h('div', { class: 'f' }, ['លេខ៖ ', h('i', { class: 'p-line' })]),
    ]));
    kids.push(h('div', { class: 'pt-note' }, 'បង្ហាញវិធីដោះស្រាយឱ្យបានច្បាស់ ហើយសរសេរឯកតា។'));
    writing.forEach((q, i) => {
      kids.push(h('div', { class: 'pt-ans-q' }, [
        h('div', {}, `${ROMAN[i] || i + 1}.  (${kh(q.points)} ពិន្ទុ)`),
        h('div', { class: 'pt-lines' }, [...Array(Math.min(8, Math.max(3, Math.round(q.points / 2)))).keys()].map(() => h('i'))),
        h('div', { class: 'pt-lines-score' }, `ពិន្ទុ: ______/${kh(q.points)}`),
      ]));
    });
  }
  const spacer = () => h('tr', {}, h('td', {}));
  const flow = h('table', { class: 'flow' }, [h('thead', {}, spacer()), h('tfoot', {}, spacer()), h('tbody', {}, h('tr', {}, h('td', {}, kids)))]);
  return h('div', { class: 'sheet' }, [headerEl(), flow, footerEl()]);
}

// Teacher answer key (អត្រាកំណែ): same header and footer as the paper, an answer grid for the multiple-choice part,
// then every written question with its figure and the solution, one step per line.
function answerDoc(o) {
  const { minutes } = o;
  const mcq = test.questions.filter((q) => q.kind !== 'writing');
  const writing = test.questions.filter((q) => q.kind === 'writing');
  const mcqPts = mcq.reduce((a, q) => a + q.points, 0), wPts = writing.reduce((a, q) => a + q.points, 0);
  const grouped = !!(o.group && mcq.some((q) => q.level));
  const ordered = OMR.mcqOrder(mcq, grouped);                    // same numbering as the printed paper
  const kids = [];
  kids.push(h('div', { class: 'etitle' }, [
    h('div', { class: 't1' }, 'អត្រាកំណែ'),
    h('div', { class: 't3' }, `វិញ្ញាសា ${profile.subject || 'គណិតវិទ្យា'} · ${test.title}`),
  ]));
  kids.push(h('div', { class: 'p-meta' }, [
    h('span', {}, ['រយៈពេល៖ ', h('b', {}, `${kh(minutes)} នាទី`)]),
    h('span', {}, ['ពិន្ទុសរុប៖ ', h('b', {}, `${kh(mcqPts + wPts)} ពិន្ទុ`)]),
    h('span', {}, [profile.group || 'ក្រុមគ្រូគណិតវិទ្យា', ' · ', h('b', {}, `ឆ្នាំ ${kh(new Date().getFullYear())}`)]),
  ]));
  if (mcq.length) {
    kids.push(h('div', { class: 'p-part' }, [`ផ្នែក ក · ចម្លើយពហុជ្រើសរើស `, h('small', {}, `(${kh(mcq.length)} សំណួរ · ${kh(mcqPts)} ពិន្ទុ)`)]));
    const cells = ordered.map((q, i) => h('div', { class: `ak-cell${q.cancelled ? ' cancelled' : ''}${i % 5 === 4 ? ' g5' : ''}` }, [
      h('span', { class: 'n' }, kh(i + 1)),
      h('span', { class: 'a' }, LETTERS[q.correct_index] + (q.alt_correct_index != null ? `/${LETTERS[q.alt_correct_index]}` : '')),
    ]));
    kids.push(h('div', { class: 'ak-grid' }, cells));
    if (ordered.some((q) => q.cancelled)) kids.push(h('div', { class: 'ak-note' }, 'សំណួរដែលមានសញ្ញាសម្គាល់ត្រូវបានលុបចោល — សិស្សទាំងអស់ទទួលបានពិន្ទុ។'));
  }
  if (writing.length) {
    kids.push(h('div', { class: 'p-part' }, [`ផ្នែក ខ · ចម្លើយសរសេរ `, h('small', {}, `(${kh(writing.length)} សំណួរ · ${kh(wPts)} ពិន្ទុ)`)]));
    writing.forEach((q, i) => {
      const lines = String(q.solution_text || '(មិនទាន់មានចម្លើយគំរូ)').split('\n').filter((ln) => ln.trim());
      const stem = h('div', { class: 'ak-stem' });
      stem.innerHTML = Exam.mathHtml(String(q.stem_text || '').trim());
      kids.push(h('div', { class: 'ak-item' }, [
        h('div', { class: 'ak-h' }, [h('b', {}, `${ROMAN[i] || i + 1}.`), `  លំហាត់ទី${kh(i + 1)}`, h('span', { class: 'pts' }, `${kh(q.points)} ពិន្ទុ`)]),
        stem,
        q.image_key ? h('img', { class: 'ak-img', src: `/api/images/${q.image_key}`, alt: '' }) : null,
        h('div', { class: 'ak-sol' }, [
          h('div', { class: 'ak-sol-t' }, 'ចម្លើយគំរូ'),
          ...lines.map((ln) => {
            if (/^\s*ដូចនេះ/.test(ln)) return mathEl('div', { class: 'ans-box' }, ln.trim());
            const m = ln.match(/^\s*([ក-ឃង-ច])\s*[\)\.]\s*(.*)$/);
            const el = h('div', { class: `ans-line${m ? ' sub' : ''}` });
            el.innerHTML = (m ? `<span class="lbl">${m[1]}.</span> ` : '') + Exam.mathHtml(m ? m[2] : ln);
            return el;
          }),
        ]),
      ]));
    });
  }
  const spacer = () => h('tr', {}, h('td', {}));
  const flow = h('table', { class: 'flow' }, [h('thead', {}, spacer()), h('tfoot', {}, spacer()), h('tbody', {}, h('tr', {}, h('td', {}, kids)))]);
  return h('div', { class: 'sheet key-doc' }, [headerEl(), flow, footerEl()]);
}

const tplValue = () => document.getElementById('opt-tpl').value;
const pageOptions = () => ({
  minutes: Number(document.getElementById('opt-min').value) || 70,
  date: document.getElementById('opt-date').value.trim(),
  space: document.getElementById('opt-space').checked,
  subtitle: document.getElementById('opt-sub').value.trim(),
  omr: document.getElementById('opt-omr').checked,
  group: document.getElementById('opt-group').checked,
  idDigits: Math.min(12, Math.max(1, Number(document.getElementById('opt-iddigits').value) || 7)),
});

function render() {
  const o = pageOptions();
  const tpl = tplValue();
  document.getElementById('opt-sub').hidden = tpl !== 'pretest';
  document.getElementById('lbl-iddigits').hidden = !document.getElementById('opt-omr').checked;
  const answers = document.getElementById('opt-key').checked;
  const sheet = document.getElementById('sheet');
  sheet.innerHTML = '';
  // template 2 puts its footer into @page margin boxes, built from this teacher's details
  let st = document.getElementById('pt-page-style');
  if (!st) { st = document.createElement('style'); st.id = 'pt-page-style'; document.head.append(st); }
  st.textContent = tpl === 'pretest' ? window.PaperPT.pageStyle(profile) : '';
  if (tpl === 'pretest') {
    const mcq = test.questions.filter((q) => q.kind !== 'writing'), writing = test.questions.filter((q) => q.kind === 'writing');
    const ctx = { h, mathEl, kh, test, profile, mcq, writing, splitWriting, logoSrc,
      mcqPts: mcq.reduce((a, q) => a + q.points, 0), wPts: writing.reduce((a, q) => a + q.points, 0) };
    sheet.append(answers ? window.PaperPT.keyDoc(ctx, o) : window.PaperPT.examDoc(ctx, o));
    window.__diagramsReady = restyleDiagrams(sheet);
    fitPreview();
    return;
  }
  sheet.append(answers ? answerDoc(o) : examDoc(o));
  window.__diagramsReady = restyleDiagrams(sheet);
  fitOptions(sheet);
  fitPreview();
}

// Scale the A4 page to the space available: whole page visible on a phone (pinch to zoom), centred next to the options on a computer.
function fitPreview() {
  const stage = document.getElementById('stage'), sheet = document.getElementById('sheet');
  if (!stage || !sheet) return;
  const cs = getComputedStyle(stage);
  const avail = stage.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
  const page = 210 / 25.4 * 96;                          // A4 width in CSS px
  sheet.style.zoom = String(Math.min(1, Math.max(0.3, avail / (page + 8))));
}
window.addEventListener('resize', () => { fitPreview(); });
window.addEventListener('beforeprint', () => { document.getElementById('sheet').style.zoom = '1'; });
window.addEventListener('afterprint', fitPreview);

// ក ខ គ ឃ always share one line: if a row is too wide at 13pt, shrink it a little (down to 10.5pt);
// only when it still cannot fit does it fall back to two columns.
function fitOptions(root) {
  const run = () => root.querySelectorAll('.p-opts').forEach((row) => {
    row.style.fontSize = ''; row.classList.remove('fit2');
    let pt = 13;
    while (row.scrollWidth > row.clientWidth + 1 && pt > 10.5) { pt -= 0.5; row.style.fontSize = `${pt}pt`; }
    if (row.scrollWidth > row.clientWidth + 1) { row.style.fontSize = ''; row.classList.add('fit2'); }
  });
  run();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(run);
}

// Diagram labels (points, vertices, variables) are set in Mathcad UniMath italic like the maths in the text;
// numbers, units and Khmer words stay upright in Times New Roman. SVG only — PNG/JPG cannot be restyled.
const MATH_LABEL = /^([A-Z]{1,3}|[a-z])['\u2032]?[0-9]?$/;
async function restyleDiagrams(root) {
  for (const img of root.querySelectorAll('img[src^="/api/images/"][src$=".svg"]')) {
    const src = img.getAttribute('src');
    try {
      const doc = new DOMParser().parseFromString(await (await fetch(src)).text(), 'image/svg+xml');
      const svg = doc.documentElement;
      if (svg.nodeName !== 'svg') continue;
      svg.setAttribute('font-family', "'Times New Roman', serif");
      for (const t of svg.querySelectorAll('text')) {
        if (MATH_LABEL.test(t.textContent.trim())) { t.setAttribute('font-family', "'Mathcad UniMath Italic','Mathcad UniMath','Times New Roman',serif"); t.setAttribute('font-style', 'italic'); t.removeAttribute('font-weight'); }
        else t.setAttribute('font-family', "'Times New Roman', serif");
      }
      const url = URL.createObjectURL(new Blob([new XMLSerializer().serializeToString(svg)], { type: 'image/svg+xml' }));
      img.src = url;
    } catch { /* keep the original picture */ }
  }
}

// ---------- header / footer details (per teacher) ----------
function openProfile() {
  const F = [
    ['school', 'ឈ្មោះសាលា (ក្បាលទំព័រ)', 'ឧ. វិទ្យាល័យព្រះស៊ីសុវត្ថិ សាលាជំនាន់ថ្មី (NGS)'],
    ['website', 'Website', 'www.example.edu.kh'], ['facebook', 'Facebook', 'ឈ្មោះទំព័រ'],
    ['teacher', 'ជើងទំព័រ — ឈ្មោះគ្រូ', 'ឧ. បង្រៀនដោយ សាន សុខលី'], ['email', 'Email', ''], ['telegram', 'Telegram', '@username'], ['tel', 'ទូរស័ព្ទ', '012 345 678'],
    ['group', 'ក្រុមគ្រូ (សន្លឹកចម្លើយ)', 'ក្រុមគ្រូគណិតវិទ្យា'], ['subject', 'មុខវិជ្ជា', 'គណិតវិទ្យា'],
  ];
  const inputs = {};
  const back = h('div', { class: 'modal-back', style: 'align-items:flex-start;overflow:auto;', onclick: (e) => { if (e.target === back) back.remove(); } });
  const logoState = { v: profile.logo || '' };
  const logoPrev = h('img', { style: 'height:46px;display:block;', alt: '' });
  const setLogo = () => { logoPrev.style.display = logoState.v ? 'block' : 'none'; logoPrev.src = logoState.v ? (logoState.v.startsWith('/') ? logoState.v : `/api/images/${logoState.v}`) : ''; };
  setLogo();
  const file = h('input', { type: 'file', accept: 'image/png,image/jpeg,image/webp', onchange: async () => {
    const f = file.files[0]; if (!f) return;
    try { const r = await api('/api/images', { method: 'POST', body: await f.arrayBuffer(), contentType: f.type }); logoState.v = r.key; setLogo(); } catch (e) { Exam.notify(e.message); }
  } });
  back.append(h('div', { class: 'modal-box', style: 'text-align:left;max-width:560px;margin:20px auto;' }, [
    h('h2', {}, '⚙ ក្បាលទំព័រ និងជើងទំព័រ'),
    h('p', { class: 'muted' }, 'នេះគឺជាព័ត៌មានដែលបោះពុម្ពលើវិញ្ញាសា និងសន្លឹកចម្លើយរបស់អ្នក។ ទុកទទេប្រសិនបើមិនចង់បង្ហាញ។'),
    ...F.flatMap(([k, label, ph]) => { inputs[k] = h('input', { type: 'text', value: profile[k] || '', placeholder: ph }); return [h('label', {}, label), inputs[k]]; }),
    h('label', {}, 'រូបសញ្ញាសាលា (Logo)'), logoPrev,
    h('div', { class: 'row', style: 'margin-top:6px;' }, [file, h('button', { class: 'secondary btn-sm', onclick: () => { logoState.v = '/ngs.png'; setLogo(); } }, 'ប្រើរូបសញ្ញា NGS'), h('button', { class: 'danger btn-sm', onclick: () => { logoState.v = ''; setLogo(); } }, 'ដករូបចេញ')]),
    h('div', { class: 'row', style: 'justify-content:flex-end;margin-top:16px;' }, [
      h('button', { class: 'secondary', onclick: () => back.remove() }, 'បោះបង់'),
      h('button', { onclick: async () => {
        try {
          const body = Object.fromEntries(Object.entries(inputs).map(([k, el]) => [k, el.value])); body.logo = logoState.v;
          const r = await api('/api/profile/paper', { method: 'POST', body });
          profile = r.profile; back.remove(); render();
        } catch (e) { Exam.notify(e.message); }
      } }, 'រក្សាទុក'),
    ]),
  ]));
  document.body.append(back);
}

async function init() {
  if (!TEST_ID) { document.getElementById('sheet').textContent = 'រកមិនឃើញតេស្តទេ។'; return; }
  try {
    test = await api(`/api/tests/${TEST_ID}`);
    test.questions = test.questions.map(Exam.withSample);
    profile = (await api('/api/profile/paper')).profile;
  } catch {
    await Exam.notify('សូមចូលជាគ្រូសិន ទើបអាចមើលវិញ្ញាសាបាន។');
    location.href = 'teacher.html';
    return;
  }
  document.title = test.title;
  if (params.get('min')) document.getElementById('opt-min').value = params.get('min');
  if (params.get('key') === '1') document.getElementById('opt-key').checked = true;
  try { const t = params.get('tpl') || localStorage.getItem('paper_tpl'); if (t === 'pretest' || t === 'exam') document.getElementById('opt-tpl').value = t; } catch {}
  document.getElementById('opt-tpl').addEventListener('change', () => { try { localStorage.setItem('paper_tpl', tplValue()); } catch {} });
  for (const id of ['opt-tpl', 'opt-sub', 'opt-omr', 'opt-group', 'opt-key', 'opt-space', 'opt-min', 'opt-date', 'opt-iddigits']) document.getElementById(id).addEventListener('input', render);
  if (window.innerWidth <= 860) document.getElementById('side-opts').open = false;   // phone: keep the page itself in view
  document.getElementById('print-btn').onclick = () => window.print();
  const pdfBtn = document.getElementById('pdf-btn');
  pdfBtn.onclick = async () => {
    const label = pdfBtn.textContent; pdfBtn.disabled = true; pdfBtn.textContent = '⏳ កំពុងរៀបចំ…';
    try {
      await window.PdfExport.download({
        sheet: document.querySelector('#sheet > .sheet'), title: test.title, ready: window.__diagramsReady,
        onProgress: (i, n) => { pdfBtn.textContent = `⏳ ទំព័រ ${i}/${n}`; },
      });
    } catch (e) { Exam.notify(`មិនអាចបង្កើត PDF បានទេ៖ ${e.message}`); }
    pdfBtn.disabled = false; pdfBtn.textContent = label;
  };
  document.getElementById('scan-link').href = `scan.html?test=${test.id}`;
  document.getElementById('profile-btn').onclick = openProfile;
  const toWord = async (btn) => {
    const label = btn ? btn.textContent : '';
    if (btn) { btn.disabled = true; btn.textContent = '⏳ កំពុងបង្កើត Word…'; }
    try {
      await window.ExamDocx.download(test, {
        ...pageOptions(), tpl: tplValue(), answers: document.getElementById('opt-key').checked, profile,
      });
    } catch (e) { Exam.notify(`មិនអាចបង្កើតឯកសារ Word បានទេ៖ ${e.message}`); }
    if (btn) { btn.disabled = false; btn.textContent = label; }
  };
  document.getElementById('docx-btn').onclick = (e) => toWord(e.currentTarget);
  if (!test.questions.every((q) => q.kind === 'writing' || q.correct_index != null)) document.getElementById('opt-key').closest('label').hidden = true;
  render();
  if (params.get('docx') === '1') toWord(document.getElementById('docx-btn'));   // opened from the ⋯ menu
}
init();
