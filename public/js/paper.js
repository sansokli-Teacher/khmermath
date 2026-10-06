const { h, api } = Exam;
const params = new URLSearchParams(location.search);
const TEST_ID = params.get('test');
const LETTERS = ['ក', 'ខ', 'គ', 'ឃ', 'ង', 'ច'];
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
  kids.push(h('div', { class: 'p-meta' }, [h('span', {}, `រយៈពេល៖ ${kh(minutes)} នាទី`), h('span', {}, `ពិន្ទុសរុប៖ ${kh(mcqPts + wPts)} ពិន្ទុ`)]));
  kids.push(h('div', { class: 'p-student' }, [
    h('div', {}, ['ឈ្មោះ៖ ', h('span', { class: 'p-line', style: 'display:inline-block;width:78%;' })]),
    h('div', {}, ['ថ្នាក់៖ ', h('span', { class: 'p-line', style: 'display:inline-block;width:60%;' })]),
    h('div', {}, ['លេខ៖ ', h('span', { class: 'p-line', style: 'display:inline-block;width:60%;' })]),
  ]));
  kids.push(h('div', { class: 'p-instr' }, `សូមអានសំណួរឱ្យបានល្អិតល្អន់។ ${mcq.length ? `ផ្នែក ក ជ្រើសរើសចម្លើយត្រឹមត្រូវ (${kh(mcqPts)} ពិន្ទុ)។ ` : ''}${writing.length ? `ផ្នែក ខ សរសេរចម្លើយលើក្រដាសឆ្លើយ ដោយបង្ហាញវិធីដោះស្រាយ (${kh(wPts)} ពិន្ទុ)។ ` : ''}មិនអនុញ្ញាតឱ្យប្រើទូរស័ព្ទ ឬម៉ាស៊ីនគណនាទេ។`));

  if (mcq.length) {
    kids.push(h('div', { class: 'p-part' }, [`ផ្នែក ក · ពហុជ្រើសរើស `, h('small', {}, `(${kh(mcq.length)} សំណួរ × ${kh(mcq[0].points)} ពិន្ទុ)`)]));
    mcq.forEach((q, i) => {
      const long = q.options.some((x) => x.length > 22);
      kids.push(h('div', { class: 'p-q' }, [
        h('div', { class: 'n' }, `${kh(i + 1)}.`),
        h('div', {}, [
          mathEl('div', { class: 'p-stem' }, q.stem_text),
          q.image_key ? h('img', { src: `/api/images/${q.image_key}`, alt: '' }) : null,
          h('div', { class: `p-opts${long ? ' two' : ''}` }, q.options.map((x, j) => h('div', { class: 'p-opt' }, [h('b', {}, `${LETTERS[j]}.`), mathEl('span', {}, x)]))),
        ]),
      ]));
    });
  }
  if (writing.length) {
    kids.push(h('div', { class: 'p-part' }, [`ផ្នែក ខ · សរសេរ `, h('small', {}, `(${kh(writing.length)} សំណួរ · ${kh(wPts)} ពិន្ទុ)`)]));
    writing.forEach((q, i) => {
      const { intro, subs } = splitWriting(q.stem_text);
      kids.push(h('div', { class: 'wblock' }, [
        h('div', { class: 'sect' }, [h('span', { class: 'rn' }, `${ROMAN[i] || i + 1}.`), h('span', { class: 'sc' }, `(${kh(q.points)}ពិន្ទុ)`), mathEl('span', { class: 'st' }, intro || (subs.length ? '' : q.stem_text))]),
        ...subs.map((s) => h('div', { class: 'sq' }, [h('span', { class: 'n' }, `${s.l}.`), mathEl('span', { class: 't' }, s.t)])),
        q.image_key ? h('img', { src: `/api/images/${q.image_key}`, alt: '' }) : null,
        space ? h('div', { class: 'p-space', style: `height:${Math.max(24, q.points * 4.5)}mm;` }) : null,
      ]));
    });
  }
  const spacer = () => h('tr', {}, h('td', {}));
  const flow = h('table', { class: 'flow' }, [h('thead', {}, spacer()), h('tfoot', {}, spacer()), h('tbody', {}, h('tr', {}, h('td', {}, kids)))]);
  return h('div', { class: 'sheet' }, [headerEl(), flow, footerEl()]);
}

// Answer sheet in the "អត្រាកំណែ" style: school block, centred title, two columns, boxed conclusions
function answerDoc(o) {
  const { minutes } = o;
  const mcq = test.questions.filter((q) => q.kind !== 'writing');
  const writing = test.questions.filter((q) => q.kind === 'writing');
  const mcqPts = mcq.reduce((a, q) => a + q.points, 0), wPts = writing.reduce((a, q) => a + q.points, 0);
  const year = kh(new Date().getFullYear());
  const kids = [];
  kids.push(h('table', { class: 'ans-head' }, h('tbody', {}, [
    h('tr', {}, [h('td', {}, profile.school || ''), h('td', {}, `${profile.group || 'ក្រុមគ្រូគណិតវិទ្យា'} ឆ្នាំ ${year}`)]),
    h('tr', {}, [h('td', {}, `មុខវិជ្ជា៖ ${profile.subject || 'គណិតវិទ្យា'}`), h('td', {}, `រយៈពេល៖ ${kh(minutes)} នាទី (ពិន្ទុ៖ ${kh(mcqPts + wPts)})`)]),
  ])));
  kids.push(h('div', { class: 'ans-title' }, [h('div', {}, 'អត្រាកំណែ'), h('div', {}, `វិញ្ញាសា៖ ${profile.subject || 'គណិតវិទ្យា'}`), h('div', { style: 'font-size:12pt;' }, test.title)]));
  const cols = [];
  if (mcq.length) {
    cols.push(h('div', { class: 'ans-ex' }, [
      h('h4', {}, `ផ្នែក ក · ពហុជ្រើសរើស (${kh(mcqPts)}ពិន្ទុ)`),
      h('div', { class: 'ans-mcq' }, mcq.map((q, i) => h('span', {}, [`${kh(i + 1)}. `, h('b', {}, LETTERS[q.correct_index] + (q.alt_correct_index != null ? `/${LETTERS[q.alt_correct_index]}` : ''))]))),
    ]));
  }
  writing.forEach((q, i) => {
    const lines = String(q.solution_text || '(មិនទាន់មានចម្លើយគំរូ)').split('\n');
    cols.push(h('div', { class: 'ans-ex' }, [
      h('h4', {}, `លំហាត់ទី${kh(i + 1)} (${kh(q.points)}ពិន្ទុ)`),
      ...lines.map((ln) => {
        if (/^\s*ដូចនេះ/.test(ln)) return mathEl('div', { class: 'ans-box' }, ln.trim());
        const m = ln.match(/^\s*([ក-ឃង-ច])\s*[\)\.]\s*(.*)$/);
        const el = h('div', { class: 'ans-line' });
        el.innerHTML = (m ? `<span class="lbl">${m[1]}.</span> ` : '') + Exam.mathHtml(m ? m[2] : ln);
        return el;
      }),
    ]));
  });
  kids.push(h('div', { class: 'ans-cols' }, cols));
  return h('div', { class: 'sheet answers-doc' }, kids);
}

const tplValue = () => document.getElementById('opt-tpl').value;
const pageOptions = () => ({
  minutes: Number(document.getElementById('opt-min').value) || 70,
  date: document.getElementById('opt-date').value.trim(),
  space: document.getElementById('opt-space').checked,
  subtitle: document.getElementById('opt-sub').value.trim(),
  omr: document.getElementById('opt-omr').checked,
  group: document.getElementById('opt-group').checked,
});

function render() {
  const o = pageOptions();
  const tpl = tplValue();
  for (const id of ['opt-sub', 'lbl-omr', 'lbl-group']) document.getElementById(id).hidden = tpl !== 'pretest';
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
    return;
  }
  sheet.append(answers ? answerDoc(o) : examDoc(o));
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
  for (const id of ['opt-tpl', 'opt-sub', 'opt-omr', 'opt-group', 'opt-key', 'opt-space', 'opt-min', 'opt-date']) document.getElementById(id).addEventListener('input', render);
  document.getElementById('print-btn').onclick = () => window.print();
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
