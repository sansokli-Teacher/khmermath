// Practice: the questions this student got wrong in published exams, again, with the explanation.
// Nothing is scored or sent to the teacher. A question is "mastered" after two right answers in a row
// (remembered on this phone only), and then drops out of the list.
const { h, api } = Exam;
const LETTERS = ['ក', 'ខ', 'គ', 'ឃ', 'ង', 'ច'];
const main = document.getElementById('pr-main');
let all = [], topic = '', studentId = 'x', state = {};
const key = () => `exam_practice_${studentId}`;
const load = () => { try { state = JSON.parse(localStorage.getItem(key()) || '{}'); } catch { state = {}; } };
const save = () => { try { localStorage.setItem(key(), JSON.stringify(state)); } catch {} };
const mathEl = (tag, attrs, text) => { const el = h(tag, attrs); el.innerHTML = Exam.mathHtml(text); return el; };
const mastered = (q) => (state[q.key] || 0) >= 2;

function shuffle(a) { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; }

function home() {
  const open = all.filter((q) => !mastered(q));
  const topics = [...new Set(open.map((q) => q.topic || '—'))];
  const pool = open.filter((q) => !topic || (q.topic || '—') === topic);
  document.getElementById('pr-sub').textContent = `${open.length} សំណួររង់ចាំ · ${all.length - open.length} ចាំបានហើយ ✓`;
  main.innerHTML = '';
  if (!all.length) { main.append(h('div', { class: 'empty-card' }, [h('div', { class: 'empty-icon' }, '🎉'), h('div', { style: 'font-weight:600;' }, 'មិនមានសំណួរខុសត្រូវហាត់ទេ'), h('div', { class: 'muted' }, 'បន្ទាប់ពីលោកគ្រូប្រកាសលទ្ធផល សំណួរដែលប្អូនធ្លាប់ខុសនឹងបង្ហាញនៅទីនេះ។')])); return; }
  main.append(
    h('div', { class: 'card' }, [
      h('h2', {}, 'ជ្រើសប្រធានបទ'),
      h('div', { class: 'row', style: 'gap:8px;flex-wrap:wrap;' }, [
        h('button', { class: `secondary btn-sm${!topic ? ' on' : ''}`, onclick: () => { topic = ''; home(); } }, `ទាំងអស់ (${open.length})`),
        ...topics.map((t) => h('button', { class: `secondary btn-sm${topic === t ? ' on' : ''}`, onclick: () => { topic = t; home(); } }, `${t} (${open.filter((q) => (q.topic || '—') === t).length})`)),
      ]),
      h('div', { style: 'margin-top:14px;' }, pool.length ? h('button', { class: 'btn-block', onclick: () => run(shuffle(pool).slice(0, 10)) }, `▶ ចាប់ផ្តើមហាត់ ${Math.min(10, pool.length)} សំណួរ`) : h('div', { class: 'callout good' }, '✓ ចាំបានអស់ហើយ!')),
    ]),
    h('p', { class: 'muted', style: 'margin-top:10px;' }, 'ឆ្លើយត្រូវពីរដងជាប់គ្នា សំណួរនោះនឹងចាត់ទុកថាចាំបាន។ ពិន្ទុនេះមិនបញ្ជូនទៅលោកគ្រូទេ។'),
  );
}

function run(list) {
  let i = 0, right = 0;
  function show() {
    main.innerHTML = '';
    if (i >= list.length) {
      main.append(h('div', { class: 'card', style: 'text-align:center;' }, [
        h('div', { style: 'font-size:46px;' }, right === list.length ? '🎉' : '💪'),
        h('h2', {}, `ត្រូវ ${right} / ${list.length}`),
        h('div', { class: 'row', style: 'justify-content:center;' }, [h('button', { onclick: home }, 'ត្រឡប់ទៅបញ្ជី'), h('button', { class: 'secondary', onclick: () => run(shuffle(all.filter((q) => !mastered(q) && (!topic || (q.topic || '—') === topic))).slice(0, 10)) }, '🔁 ហាត់បន្ត')]),
      ]));
      return;
    }
    const q = list[i];
    let done = false;
    const opts = h('div', { class: 'radio-list' });
    const fb = h('div', { style: 'font-weight:700;margin:10px 0;min-height:24px;' });
    const sol = h('div', { class: 'callout', style: 'white-space:pre-line;', hidden: 'hidden' });
    const next = h('button', { hidden: 'hidden', onclick: () => { i++; show(); } }, i + 1 < list.length ? 'បន្ទាប់ →' : 'មើលលទ្ធផល');
    q.options.forEach((o, j) => opts.append(h('label', { class: 'radio-opt', onclick: () => {
      if (done) return; done = true;
      const ok = j === q.correct_index || j === q.alt_correct_index;
      if (ok) right++;
      state[q.key] = ok ? (state[q.key] || 0) + 1 : 0; save();
      [...opts.children].forEach((c, k) => { if (k === q.correct_index || k === q.alt_correct_index) c.classList.add('selected'); else if (k === j) c.style.cssText = 'border-color:var(--bad);background:var(--bad-soft);'; });
      fb.textContent = ok ? (state[q.key] >= 2 ? '✓ ត្រឹមត្រូវ — ចាំបានហើយ!' : '✓ ត្រឹមត្រូវ!') : `✗ មិនទាន់ត្រូវ — ចម្លើយត្រឹមត្រូវគឺ ${LETTERS[q.correct_index]}`;
      fb.style.color = ok ? 'var(--good)' : 'var(--bad)';
      if (q.solution_text) { sol.innerHTML = Exam.mathHtml('💡 ' + q.solution_text); sol.hidden = false; }
      next.hidden = false;
    } }, [h('span', { class: 'opt-letter' }, LETTERS[j]), mathEl('span', { class: 'opt-body' }, o)])));
    main.append(h('div', { class: 'question-card' }, [
      h('div', { class: 'row', style: 'justify-content:space-between;' }, [h('span', { class: 'q-count' }, `${i + 1} / ${list.length}`), q.topic ? h('span', { class: 'chip chip-plain' }, q.topic) : null]),
      mathEl('div', { class: 'q-stem' }, q.stem_text),
      q.image_key ? h('div', { style: 'text-align:center;margin:10px 0;' }, h('img', { src: `/api/images/${q.image_key}`, style: 'max-height:260px;max-width:100%;' })) : null,
      opts, fb, sol, h('div', { style: 'margin-top:8px;' }, next),
    ]));
  }
  show();
}

(async () => {
  try {
    const d = await api('/api/student/practice');
    all = d.items; studentId = d.student_id; load();
    home();
  } catch (e) {
    main.append(h('div', { class: 'error' }, e.status === 401 ? 'សូមចូលជាមុនសិន។' : e.message), h('a', { class: 'btn', href: 'student.html' }, 'ទៅទំព័រចូល'));
  }
})();
