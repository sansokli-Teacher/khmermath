const { h, api, fmtDateTime } = Exam;
const params = new URLSearchParams(location.search);
const SESSION = params.get('session');
const STUDENT = params.get('student');       // set when the teacher opens a student's report
const LETTERS = ['ក', 'ខ', 'គ', 'ឃ', 'ង', 'ច'];
const KH = '០១២៣៤៥៦៧៨៩';
const kh = (n) => String(n).replace(/\d/g, (d) => KH[d]);

function mathEl(tag, attrs, text) {
  const el = h(tag, attrs);
  el.innerHTML = Exam.mathHtml(text);
  return el;
}

function render(r) {
  const report = document.getElementById('report');
  report.innerHTML = '';
  const mcq = r.questions.filter((q) => q.kind === 'mcq');
  const writing = r.questions.filter((q) => q.kind === 'writing');
  const right = mcq.filter((q) => q.correct).length;
  const blank = mcq.filter((q) => q.selected_index == null).length;
  const wrong = mcq.length - right - blank;
  const wScore = r.writing_score, wMax = r.writing_max;
  const total = r.mcq_score + (wScore ?? 0);
  const max = r.mcq_max + (wMax ?? 0);
  const pct = max > 0 ? Math.round((total / max) * 100) : 0;
  const g = Exam.gradeOf(pct);
  const wrongNos = mcq.map((q, i) => (q.correct ? null : i + 1)).filter(Boolean);

  report.append(
    h('div', { class: 'rp-head' }, [
      h('div', {}, [h('div', {}, 'ក្រសួងអប់រំ យុវជន និងកីឡា'), h('div', {}, 'វិទ្យាល័យព្រះស៊ីសុវត្ថិ · សាលារៀនជំនាន់ថ្មី (NGS)')]),
      h('div', { style: 'text-align:right;' }, [h('div', {}, 'ព្រះរាជាណាចក្រកម្ពុជា'), h('div', {}, 'ជាតិ សាសនា ព្រះមហាក្សត្រ')]),
    ]),
    h('h1', { class: 'rp-title' }, 'របាយការណ៍លទ្ធផលប្រឡង'),
    h('div', { class: 'rp-sub' }, r.test_title),
    h('div', { class: 'rp-who' }, [
      h('span', {}, ['ឈ្មោះ៖ ', h('b', {}, r.student.name)]),
      h('span', {}, ['អត្តលេខ៖ ', h('b', {}, r.student.id)]),
      h('span', {}, ['ថ្នាក់៖ ', h('b', {}, r.class_name)]),
      h('span', {}, ['កាលបរិច្ឆេទ៖ ', h('b', {}, fmtDateTime(r.date))]),
    ]),
    h('div', { class: 'rp-score' }, [
      h('div', { class: 'rp-big' }, [h('span', {}, String(total)), h('span', { class: 'rp-of' }, ` / ${max}`)]),
      h('div', { class: 'rp-grade', style: `background:${g.color}1a;color:${g.color};` }, [h('div', { class: 'rp-gl' }, g.grade), h('div', {}, `${g.label} · ${pct}%`)]),
    ]),
    h('div', { class: 'rp-tiles' }, [
      h('div', { class: 'rp-tile good' }, [h('b', {}, `${right}`), ' ត្រូវ']),
      h('div', { class: 'rp-tile bad' }, [h('b', {}, `${wrong}`), ' ខុស']),
      h('div', { class: 'rp-tile' }, [h('b', {}, `${blank}`), ' មិនបានឆ្លើយ']),
      h('div', { class: 'rp-tile' }, ['ផ្នែក ក ', h('b', {}, `${r.mcq_score}/${r.mcq_max}`)]),
      writing.length ? h('div', { class: 'rp-tile' }, ['ផ្នែក ខ ', h('b', {}, wScore != null ? `${wScore}/${wMax}` : '—')]) : null,
    ]),
    wrongNos.length
      ? h('div', { class: 'rp-review' }, [h('b', {}, 'សំណួរផ្នែក ក ដែលគួរពិនិត្យឡើងវិញ៖ '), wrongNos.map((n) => kh(n)).join(' · ')])
      : h('div', { class: 'rp-review ok' }, '🎉 ផ្នែក ក ត្រូវទាំងអស់!'),
  );

  // ----- by topic: where was I strong / weak?
  const byTopic = {};
  for (const q of mcq) {
    if (!q.topic) continue;
    const t = (byTopic[q.topic] ||= { right: 0, total: 0 });
    t.total += 1; if (q.correct) t.right += 1;
  }
  const topicRows = Object.entries(byTopic).map(([name, t]) => ({ name, ...t, pct: Math.round((t.right / t.total) * 100) })).sort((a, b) => a.pct - b.pct);
  if (topicRows.length) {
    const weak = topicRows.filter((t) => t.pct < 60);
    report.append(h('div', { class: 'rp-topics' }, [
      h('div', { class: 'rp-part', style: 'margin-top:16px;' }, 'ប្រធានបទ — ខ្លាំង និងខ្សោយ'),
      ...topicRows.map((t) => {
        const col = t.pct >= 70 ? '#16a34a' : t.pct >= 50 ? '#d97706' : '#dc2626';
        return h('div', { class: 'rp-topic' }, [
          h('div', { style: 'flex:1;min-width:0;' }, t.name),
          h('div', { class: 'bar', style: 'width:34%;' }, h('div', { class: 'bar-fill', style: `width:${t.pct}%;background:${col};` })),
          h('div', { style: `width:84px;text-align:right;font-weight:700;color:${col};` }, `${t.right}/${t.total} · ${t.pct}%`),
        ]);
      }),
      weak.length ? h('div', { class: 'rp-review' }, [h('b', {}, '📌 គួររៀនឡើងវិញ៖ '), weak.map((t) => t.name).join(' · ')]) : null,
    ]));
  }
  const wrongQs = mcq.filter((q) => !q.correct);
  if (wrongQs.length) {
    report.append(h('div', { class: 'no-print', style: 'margin:14px 0 4px;' }, h('button', { onclick: () => practice(wrongQs) }, `🔁 ហាត់សំណួរដែលខុស (${wrongQs.length})`)));
  }

  const list = h('div', { id: 'rp-list' });
  if (mcq.length) list.append(h('div', { class: 'rp-part' }, 'ផ្នែក ក · ពហុជ្រើសរើស'));
  mcq.forEach((q, i) => {
    const state = q.selected_index == null ? 'blank' : q.correct ? 'right' : 'wrong';
    list.append(h('div', { class: `rp-q ${state}`, 'data-state': state }, [
      h('div', { class: 'rp-qhead' }, [
        h('span', { class: 'rp-no' }, kh(i + 1)),
        h('span', { class: `rp-badge ${state}` }, q.cancelled ? `សំណួរត្រូវបានបោះបង់ — ទទួលពិន្ទុ +${q.points}` : state === 'right' ? `✓ ត្រូវ +${q.points}` : state === 'wrong' ? '✗ ខុស' : '— មិនបានឆ្លើយ'),
      ]),
      mathEl('div', { class: 'rp-stem' }, q.stem_text),
      q.image_key ? h('img', { src: `/api/images/${q.image_key}`, alt: '' }) : null,
      h('div', { class: 'rp-opts' }, q.options.map((o, j) => {
        const isRight = j === q.correct_index, isMine = j === q.selected_index;
        return h('div', { class: `rp-opt${isRight ? ' is-right' : ''}${isMine && !isRight ? ' is-wrong' : ''}` }, [
          h('b', {}, `${LETTERS[j]}.`), mathEl('span', {}, o),
          isMine ? h('em', {}, isRight ? ' ← ចម្លើយរបស់ប្អូន ✓' : ' ← ចម្លើយរបស់ប្អូន ✗') : (isRight ? h('em', {}, ' ← ចម្លើយត្រឹមត្រូវ') : null),
        ]);
      })),
    ]));
  });
  if (writing.length) {
    list.append(h('div', { class: 'rp-part' }, ['ផ្នែក ខ · សរសេរ ', h('small', {}, wScore != null ? `(ពិន្ទុរបស់ប្អូន ${wScore}/${wMax})` : '')]));
    writing.forEach((q, i) => list.append(h('div', { class: 'rp-q writing', 'data-state': 'writing' }, [
      h('div', { class: 'rp-qhead' }, [h('span', { class: 'rp-no' }, `ខ${kh(i + 1)}`), h('span', { class: `rp-badge${q.mark != null ? ' right' : ''}` }, q.mark != null ? `ពិន្ទុរបស់ប្អូន ${q.mark} / ${q.points}` : `${q.points} ពិន្ទុ`)]),
      mathEl('div', { class: 'rp-stem' }, q.stem_text),
      q.image_key ? h('img', { src: `/api/images/${q.image_key}`, alt: '' }) : null,
      q.solution_text ? h('div', { class: 'rp-sol' }, [h('b', {}, 'ចម្លើយគំរូ និងការដាក់ពិន្ទុ៖'), mathEl('div', { class: 'rp-soltext' }, q.solution_text)]) : null,
    ])));
  }
  report.append(list);
  report.append(h('div', { class: 'rp-foot' }, 'របាយការណ៍នេះបង្កើតដោយប្រព័ន្ធប្រឡង exam.khmermath.org'));
}

function setFilter(mode) {
  const list = document.getElementById('rp-list');
  if (!list) return;
  list.dataset.filter = mode;
  for (const id of ['all', 'wrong', 'right']) document.getElementById(`filter-${id}`).classList.toggle('is-on', id === mode);
}

async function init() {
  if (STUDENT) document.getElementById('back-link').href = 'teacher.html';
  try {
    const r = STUDENT ? await api(`/api/sessions/${SESSION}/review/${encodeURIComponent(STUDENT)}`) : await api(`/api/student/review?session_id=${SESSION}`);
    document.title = `របាយការណ៍ — ${r.student.name}`;
    render(r);
    setFilter('all');
    // «ទាញយក PDF» from the student home opens the print dialog once images have loaded.
    if (params.get('print') === '1') {
      const imgs = [...document.images].filter((i) => !i.complete);
      await Promise.all(imgs.map((i) => new Promise((ok) => { i.onload = i.onerror = ok; })));
      setTimeout(() => window.print(), 400);
    }
  } catch (e) {
    document.getElementById('report').append(h('div', { class: 'error' }, e.message));
  }
  document.getElementById('print-btn').onclick = () => window.print();
  for (const id of ['all', 'wrong', 'right']) document.getElementById(`filter-${id}`).onclick = () => setFilter(id);
}
init();


// ---------- practice: retry the questions I got wrong (nothing is saved or scored) ----------
function practice(questions) {
  let i = 0, rightCount = 0;
  const back = h('div', { class: 'modal-back', style: 'align-items:flex-start;overflow:auto;' });
  const box = h('div', { class: 'modal-box', style: 'text-align:left;max-width:600px;margin:18px auto;' });
  back.append(box);
  document.body.append(back);
  function show() {
    box.innerHTML = '';
    if (i >= questions.length) {
      box.append(
        h('div', { style: 'text-align:center;' }, [
          h('div', { style: 'font-size:46px;' }, rightCount === questions.length ? '🎉' : '💪'),
          h('h2', {}, `ហាត់រួចរាល់៖ ត្រូវ ${rightCount} / ${questions.length}`),
          h('p', { class: 'muted' }, rightCount === questions.length ? 'អស្ចារ្យណាស់!' : 'បន្តហាត់ម្តងទៀតដើម្បីឱ្យចាំ។'),
          h('div', { class: 'row', style: 'justify-content:center;' }, [h('button', { onclick: () => { i = 0; rightCount = 0; show(); } }, '🔁 ហាត់ម្តងទៀត'), h('button', { class: 'secondary', onclick: () => back.remove() }, 'បិទ')]),
        ]),
      );
      return;
    }
    const q = questions[i];
    let answered = false;
    const opts = h('div', { class: 'radio-list' });
    q.options.forEach((o, j) => {
      const el = h('label', { class: 'radio-opt', onclick: () => {
        if (answered) return; answered = true;
        const good = j === q.correct_index || j === q.alt_correct_index;
        if (good) rightCount++;
        [...opts.children].forEach((c, k) => { if (k === q.correct_index || k === q.alt_correct_index) c.classList.add('selected'); else if (k === j) c.style.cssText = 'border-color:var(--bad);background:var(--bad-soft);'; });
        fb.textContent = good ? '✓ ត្រឹមត្រូវ!' : `✗ មិនទាន់ត្រូវ — ចម្លើយត្រឹមត្រូវគឺ ${LETTERS[q.correct_index]}`;
        fb.style.color = good ? 'var(--good)' : 'var(--bad)';
        next.hidden = false;
      } }, [h('span', { class: 'opt-letter' }, LETTERS[j]), mathEl('span', { class: 'opt-body' }, o)]);
      opts.append(el);
    });
    const fb = h('div', { style: 'font-weight:700;margin:8px 0;min-height:24px;' });
    const next = h('button', { hidden: 'hidden', onclick: () => { i++; show(); } }, i + 1 < questions.length ? 'សំណួរបន្ទាប់ →' : 'មើលលទ្ធផល');
    box.append(
      h('div', { class: 'row', style: 'justify-content:space-between;' }, [h('b', {}, `ហាត់ ${i + 1} / ${questions.length}`), h('button', { class: 'secondary btn-sm', onclick: () => back.remove() }, '✕')]),
      mathEl('div', { class: 'rp-stem', style: 'font-size:18px;margin:10px 0;' }, q.stem_text),
      q.image_key ? h('img', { src: `/api/images/${q.image_key}`, style: 'max-width:100%;max-height:220px;display:block;margin:6px 0;' }) : null,
      opts, fb, next,
    );
  }
  show();
}
