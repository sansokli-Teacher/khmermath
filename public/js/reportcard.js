const { h, api } = Exam;
const params = new URLSearchParams(location.search);
const CLASS_ID = params.get('class');
const KH = '០១២៣៤៥៦៧៨៩';
const kh = (n) => String(n).replace(/\d/g, (d) => KH[d]);
const fmt = (v) => (v == null ? '—' : kh(String(Math.round(v * 10) / 10)));

function page({ name, id, cls, label, rows, comment }) {
  const gradeCell = (v) => { const g = Exam.gradeOf(v); return g ? h('td', { class: 'rc-grade', style: `color:${g.color};` }, `${g.grade} · ${g.label}`) : h('td', {}, '—'); };
  const tr = (title, v, cls2 = '') => h('tr', { class: cls2 }, [h('td', { class: 'l' }, title), h('td', {}, fmt(v)), gradeCell(v)]);
  return h('section', { class: 'rc-page' }, [
    h('div', { class: 'rc-head' }, [
      h('div', {}, [h('div', {}, 'ក្រសួងអប់រំ យុវជន និងកីឡា'), h('div', {}, 'វិទ្យាល័យព្រះស៊ីសុវត្ថិ'), h('div', {}, 'សាលារៀនជំនាន់ថ្មី (NGS)')]),
      h('div', {}, [h('div', {}, 'ព្រះរាជាណាចក្រកម្ពុជា'), h('div', {}, 'ជាតិ សាសនា ព្រះមហាក្សត្រ')]),
    ]),
    h('div', { class: 'rc-title' }, 'សៀវភៅរបាយការណ៍លទ្ធផលសិក្សា'),
    h('div', { class: 'rc-sub' }, `មុខវិជ្ជា គណិតវិទ្យា · ឆ្នាំសិក្សា ${label}`),
    h('div', { class: 'rc-who' }, [h('div', {}, ['ឈ្មោះ៖ ', h('b', {}, name)]), h('div', {}, ['អត្តលេខ៖ ', h('b', {}, id)]), h('div', {}, ['ថ្នាក់៖ ', h('b', {}, cls)]), h('div', {}, ['កាលបរិច្ឆេទ៖ ', h('b', {}, kh(new Date().toLocaleDateString('en-GB')))])]),
    h('table', { class: 'rc-table' }, [
      h('thead', {}, h('tr', {}, [h('th', { style: 'width:46%' }, 'ការវាយតម្លៃ'), h('th', {}, 'ពិន្ទុ (/១០០)'), h('th', {}, 'និទ្ទេស')])),
      h('tbody', {}, rows.map((r) => tr(r.title, r.v, r.cls))),
    ]),
    comment ? h('p', {}, ['មតិយោបល់៖ ', comment]) : null,
    h('div', { class: 'rc-sign' }, [h('div', {}, 'ហត្ថលេខាគ្រូបង្រៀន'), h('div', {}, 'ហត្ថលេខាអាណាព្យាបាល'), h('div', {}, 'បានឃើញ និងឯកភាព នាយកសាលា')]),
    h('div', { class: 'rc-scale' }, 'មាត្រដ្ឋាននិទ្ទេស៖ A ≥85 ល្អប្រសើរ · B ≥75 ល្អណាស់ · C ≥65 ល្អ · D ≥50 មធ្យម · E ≥40 ខ្សោយ · F <40 ធ្លាក់។'),
  ]);
}

const remark = (v) => { const g = Exam.gradeOf(v); return g ? (g.grade <= 'C' ? 'ប្អូនមានលទ្ធផលល្អ សូមបន្តខិតខំ!' : g.grade === 'D' ? 'ប្អូនមានលទ្ធផលមធ្យម គួរខិតខំបន្ថែម។' : 'ប្អូនត្រូវខិតខំរៀនបន្ថែមឱ្យខ្លាំង និងសុំជំនួយពីគ្រូ។') : ''; };

async function init() {
  const out = document.getElementById('cards');
  document.getElementById('print-btn').onclick = () => window.print();
  try {
    if (CLASS_ID) {
      const d = await api(`/api/year/class/${CLASS_ID}`);
      const A = Object.fromEntries(d.assessments.map((a) => [a.key, a]));
      d.students.forEach((s) => out.append(page({
        name: `${s.surname} ${s.first_name}`, id: s.id, cls: d.class.name, label: d.config.label,
        rows: [
          ...['pre', 'm1', 'm2'].map((k) => ({ title: `${A[k].title} — ខែ${A[k].month_label}`, v: s.scores[k] ? s.scores[k].pct : null })),
          { title: 'មធ្យមភាគប្រចាំខែ', v: s.monthly_avg, cls: 'sum' },
          { title: `${A.sem1.title} — ខែ${A.sem1.month_label}`, v: s.scores.sem1 ? s.scores.sem1.pct : null },
          { title: 'ពិន្ទុឆមាសទី១', v: s.semester1, cls: 'sum' },
          { title: `${A.final.title} — ខែ${A.final.month_label}`, v: s.final },
          { title: 'មធ្យមភាគប្រចាំឆ្នាំ', v: s.year_avg, cls: 'big' },
        ],
        comment: remark(s.year_avg ?? s.semester1),
      })));
      if (!d.students.length) out.append(h('p', { class: 'muted', style: 'padding:20px;' }, 'ថ្នាក់នេះមិនទាន់មានសិស្សទេ។'));
    } else {
      const d = await api('/api/student/status');
      const y = d.year; const A = Object.fromEntries(y.assessments.map((a) => [a.key, a]));
      out.append(page({
        name: d.student_name, id: d.student_id, cls: d.class_name, label: y.label,
        rows: [
          ...['pre', 'm1', 'm2'].map((k) => ({ title: `${A[k].title} — ខែ${A[k].month_label}`, v: A[k].pct })),
          { title: 'មធ្យមភាគប្រចាំខែ', v: y.monthly_avg, cls: 'sum' },
          { title: `${A.sem1.title} — ខែ${A.sem1.month_label}`, v: A.sem1.pct },
          { title: 'ពិន្ទុឆមាសទី១', v: y.semester1, cls: 'sum' },
          { title: `${A.final.title} — ខែ${A.final.month_label}`, v: A.final.pct },
          { title: 'មធ្យមភាគប្រចាំឆ្នាំ', v: y.year_avg, cls: 'big' },
        ],
        comment: remark(y.year_avg ?? y.semester1),
      }));
    }
  } catch (e) {
    out.append(h('div', { class: 'error', style: 'margin:20px;' }, e.message));
  }
}
init();
