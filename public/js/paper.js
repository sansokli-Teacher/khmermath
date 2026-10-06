const { h, api } = Exam;
const params = new URLSearchParams(location.search);
const TEST_ID = params.get('test');
const LETTERS = ['ក', 'ខ', 'គ', 'ឃ', 'ង', 'ច'];
const KH_DIGITS = '០១២៣៤៥៦៧៨៩';
const kh = (n) => String(n).replace(/\d/g, (d) => KH_DIGITS[d]);

function mathEl(tag, attrs, text) {
  const el = h(tag, attrs);
  el.innerHTML = Exam.mathHtml(text);
  return el;
}

let test = null;

function render() {
  const showKey = document.getElementById('opt-key').checked;
  const space = document.getElementById('opt-space').checked;
  const minutes = Number(document.getElementById('opt-min').value) || 70;
  const date = document.getElementById('opt-date').value.trim();
  const sheet = document.getElementById('sheet');
  sheet.innerHTML = '';

  const mcq = test.questions.filter((q) => q.kind !== 'writing');
  const writing = test.questions.filter((q) => q.kind === 'writing');
  const mcqPts = mcq.reduce((a, q) => a + q.points, 0);
  const wPts = writing.reduce((a, q) => a + q.points, 0);

  sheet.append(
    h('div', { class: 'p-head' }, [
      h('div', { class: 'l' }, [h('div', {}, 'ក្រសួងអប់រំ យុវជន និងកីឡា'), h('div', {}, 'វិទ្យាល័យព្រះស៊ីសុវត្ថិ'), h('div', {}, 'សាលារៀនជំនាន់ថ្មី (NGS)')]),
      h('div', { class: 'r' }, [h('div', {}, 'ព្រះរាជាណាចក្រកម្ពុជា'), h('div', {}, 'ជាតិ សាសនា ព្រះមហាក្សត្រ')]),
    ]),
    h('div', { class: 'p-title' }, test.title),
    h('div', { class: 'p-meta' }, [
      h('span', {}, 'មុខវិជ្ជា៖ គណិតវិទ្យា'),
      h('span', {}, `រយៈពេល៖ ${kh(minutes)} នាទី`),
      h('span', {}, `ពិន្ទុសរុប៖ ${kh(mcqPts + wPts)} ពិន្ទុ`),
      date ? h('span', {}, date) : null,
    ]),
    h('div', { class: 'p-student' }, [
      h('div', {}, ['ឈ្មោះ៖ ', h('span', { class: 'p-line', style: 'display:inline-block;width:78%;' })]),
      h('div', {}, ['ថ្នាក់៖ ', h('span', { class: 'p-line', style: 'display:inline-block;width:60%;' })]),
      h('div', {}, ['លេខ៖ ', h('span', { class: 'p-line', style: 'display:inline-block;width:60%;' })]),
    ]),
    h('div', { class: 'p-instr' }, `សូមអានសំណួរឱ្យបានល្អិតល្អន់។ ផ្នែក ក ជ្រើសរើសចម្លើយត្រឹមត្រូវ (${kh(mcqPts)} ពិន្ទុ)។ ផ្នែក ខ សរសេរចម្លើយលើក្រដាសឆ្លើយ ដោយបង្ហាញវិធីដោះស្រាយ (${kh(wPts)} ពិន្ទុ)។ មិនអនុញ្ញាតឱ្យប្រើទូរស័ព្ទ ឬម៉ាស៊ីនគណនាទេ។`),
  );

  if (mcq.length) {
    sheet.append(h('div', { class: 'p-part' }, [`ផ្នែក ក · ពហុជ្រើសរើស `, h('small', {}, `(${kh(mcq.length)} សំណួរ × ${kh(mcq[0].points)} ពិន្ទុ)`)]));
    mcq.forEach((q, i) => {
      const long = q.options.some((o) => o.length > 22);
      sheet.append(h('div', { class: 'p-q' }, [
        h('div', { class: 'n' }, `${kh(i + 1)}.`),
        h('div', {}, [
          mathEl('div', { class: 'p-stem' }, q.stem_text),
          q.image_key ? h('img', { src: `/api/images/${q.image_key}`, alt: '' }) : null,
          h('div', { class: `p-opts${long ? ' two' : ''}` }, q.options.map((o, j) => h('div', { class: 'p-opt' }, [h('b', {}, `${LETTERS[j]}.`), mathEl('span', {}, o)]))),
        ]),
      ]));
    });
  }

  if (writing.length) {
    sheet.append(h('div', { class: 'p-part' }, [`ផ្នែក ខ · សរសេរ `, h('small', {}, `(${kh(writing.length)} សំណួរ · ${kh(wPts)} ពិន្ទុ)`)]));
    writing.forEach((q, i) => {
      sheet.append(h('div', { class: 'p-q' }, [
        h('div', { class: 'n' }, `${kh(i + 1)}.`),
        h('div', {}, [
          h('div', { style: 'display:flex;justify-content:space-between;gap:10px;' }, [mathEl('div', { class: 'p-stem' }, q.stem_text), h('span', { class: 'p-pts' }, `(${kh(q.points)} ពិន្ទុ)`)]),
          q.image_key ? h('img', { src: `/api/images/${q.image_key}`, alt: '' }) : null,
          space ? h('div', { class: 'p-space', style: `height:${Math.max(28, q.points * 5)}mm;` }) : null,
        ]),
      ]));
    });
  }

  const hasKey = mcq.every((q) => q.correct_index != null);
  if (showKey && hasKey) {
    sheet.append(h('div', { class: 'p-pagebreak' }), h('div', { class: 'p-title' }, `ចម្លើយ — ${test.title}`));
    if (mcq.length) {
      sheet.append(h('div', { class: 'p-part' }, 'ផ្នែក ក · ចម្លើយពហុជ្រើសរើស'));
      const perRow = 10;
      const rows = [];
      for (let i = 0; i < mcq.length; i += perRow) {
        const slice = mcq.slice(i, i + perRow);
        rows.push(h('tr', {}, slice.map((_, k) => h('th', {}, kh(i + k + 1)))));
        rows.push(h('tr', {}, slice.map((q) => h('td', {}, LETTERS[q.correct_index]))));
      }
      sheet.append(h('table', { class: 'p-keytable' }, h('tbody', {}, rows)));
    }
    if (writing.length) {
      sheet.append(h('div', { class: 'p-part' }, 'ផ្នែក ខ · ចម្លើយ និងការដាក់ពិន្ទុ'));
      writing.forEach((q, i) => sheet.append(h('div', { class: 'p-q' }, [
        h('div', { class: 'n' }, `${kh(i + 1)}.`),
        h('div', {}, [
          h('div', { class: 'p-pts' }, `(${kh(q.points)} ពិន្ទុ)`),
          q.solution_text ? mathEl('div', { class: 'p-key' }, q.solution_text) : h('div', { class: 'muted' }, 'មិនទាន់មានចម្លើយគំរូ'),
        ]),
      ])));
    }
  }
}

async function init() {
  if (!TEST_ID) { document.getElementById('sheet').textContent = 'រកមិនឃើញតេស្តទេ។'; return; }
  try {
    test = await api(`/api/tests/${TEST_ID}`);
  } catch {
    await Exam.notify('សូមចូលជាគ្រូសិន ទើបអាចមើលវិញ្ញាសាបាន។');
    location.href = 'teacher.html';
    return;
  }
  document.title = test.title;
  if (params.get('min')) document.getElementById('opt-min').value = params.get('min');
  if (params.get('key') === '1') document.getElementById('opt-key').checked = true;
  for (const id of ['opt-key', 'opt-space', 'opt-min', 'opt-date']) document.getElementById(id).addEventListener('input', render);
  document.getElementById('print-btn').onclick = () => window.print();
  const toWord = async (btn) => {
    const label = btn ? btn.textContent : '';
    if (btn) { btn.disabled = true; btn.textContent = '⏳ កំពុងបង្កើត Word…'; }
    try {
      await window.ExamDocx.download(test, {
        minutes: Number(document.getElementById('opt-min').value) || 70, date: document.getElementById('opt-date').value.trim(),
        showKey: document.getElementById('opt-key').checked, space: document.getElementById('opt-space').checked,
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
