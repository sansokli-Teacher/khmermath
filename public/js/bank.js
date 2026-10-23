// Question bank: grade → lesson → questions. Reuse, tag, add new, import, or build a random test from a lesson.
const LEVEL_KH = { easy: 'ងាយ', medium: 'មធ្យម', hard: 'ពិបាក', pisa: 'បែប PISA' };
const KH_DIGITS = '០១២៣៤៥៦៧៨៩';
const khNum = (n) => String(n ?? '').replace(/\d/g, (d) => KH_DIGITS[d]);
if (typeof globalThis !== 'undefined') {
  if (!globalThis.kh) globalThis.kh = khNum;
  if (!globalThis.mathEl) {
    globalThis.mathEl = function (tag, attrs, text) {
      const el = h(tag, attrs);
      el.innerHTML = typeof Exam !== 'undefined' && Exam.mathHtml ? Exam.mathHtml(text) : String(text ?? '');
      return el;
    };
  }
}
const GRADE_KH = (g) => {
  if (g === 'NGS') return 'តម្រង់ទិសសិស្ស NGS ២០២៦-២០២៧';
  if (g === '11SC') return 'ថ្នាក់ទី ១១ (វិទ្យាសាស្ត្រពិត)';
  if (g === '11SS') return 'ថ្នាក់ទី ១១ (វិទ្យាសាស្ត្រសង្គម)';
  if (g === '12SC') return 'ថ្នាក់ទី ១២ (វិទ្យាសាស្ត្រពិត)';
  if (g === '12SS') return 'ថ្នាក់ទី ១២ (វិទ្យាសាស្ត្រសង្គម)';
  return `ថ្នាក់ទី ${khNum(g)}`;
};
const bankGradesOf = (curr) => curr.bankGrades || curr.grades || [];
const canBankDelete = () => typeof ME !== 'undefined' && ME && (ME.role === 'owner' || ME.role === 'admin');
let bankState = { grade: '', chapter: '', lesson: '', level: '', kind: '', topic: '', q: '', mine: null };   // grade '' = all, '-' = no grade; lesson '' = all, '-' = no lesson
let CURR = null;
const bankSelected = new Set();   // question ids ticked for a test: kept while the teacher moves between lessons and grades

async function loadCurr(force) { if (!CURR || force) CURR = await api('/api/curriculum'); return CURR; }

// grade <select> + chapter + lesson picker used by question forms
function gradeLessonPicker(g, l, curr, ch) {
  const id = 'lesson-dl-' + Math.random().toString(36).slice(2, 7);
  const chId = 'chapter-dl-' + Math.random().toString(36).slice(2, 7);
  const grade = h('select', {}, [['', '— ថ្នាក់ —'], ...bankGradesOf(curr).map((x) => [x, GRADE_KH(x)])].map(([v, t]) => h('option', { value: v, selected: String(g || '') === v ? 'selected' : null }, t)));
  const dl = h('datalist', { id });
  const chDl = h('datalist', { id: chId });
  const chapter = h('input', { type: 'text', list: chId, placeholder: 'ជំពូក (មិនចាំបាច់)', value: ch || '' });
  const lesson = h('input', { type: 'text', list: id, placeholder: 'ជ្រើស ឬវាយឈ្មោះមេរៀន', value: l || '' });
  const fill = () => {
    dl.innerHTML = ''; chDl.innerHTML = '';
    (curr.lessons[grade.value] || []).forEach((n) => dl.append(h('option', { value: n })));
    ((curr.chapters && curr.chapters[grade.value]) || []).forEach((c) => chDl.append(h('option', { value: c.name })));
  };
  lesson.addEventListener('change', () => {
    const val = lesson.value.trim();
    if (val && !chapter.value.trim() && curr.chapters && curr.chapters[grade.value]) {
      const found = curr.chapters[grade.value].find((c) => c.lessons.includes(val));
      if (found) chapter.value = found.name;
    }
  });
  grade.addEventListener('change', fill); fill();
  return { grade, chapter, chDl, lesson, dl, get: () => ({ grade: grade.value || null, chapter: chapter.value.trim() || null, lesson: lesson.value.trim() || null }) };
}

function bankModal(title, body, wide) {
  const back = h('div', { class: 'modal-back', style: 'align-items:flex-start;overflow:auto;', onclick: (e) => { if (e.target === back) back.remove(); } });
  const headerEl = typeof title === 'string' ? h('h2', {}, title) : title;
  back.append(h('div', { class: 'modal-box', style: `text-align:left;max-width:${wide ? 720 : 520}px;margin:20px auto;` }, [headerEl, body]));
  document.body.append(back);
  return back;
}

// ---------- download an exercise book: chosen lessons or the whole book of a grade, as PDF or Word ----------
function openExport(questions, curr, S) {
  let grade = S.grade && S.grade !== '-' ? S.grade : (bankGradesOf(curr).find((g) => questions.some((q) => q.grade === g)) || bankGradesOf(curr)[0]);
  const picked = new Set();                    // 1-based lesson numbers
  const levels = new Set(['easy', 'medium', 'hard', 'pisa']);
  let kind = 'all', ans = 'none', newpage = false, title = '';
  const body = h('div', { class: 'ex-body' });
  const box = h('div', {}, [body]);
  const lessonList = () => (curr.lessons[grade] || []);
  const countOf = (name) => questions.filter((q) => q.grade === grade && q.lesson === name && (kind === 'all' || (kind === 'mcq' ? q.kind !== 'writing' : q.kind === 'writing')) && levels.has(q.level || '') ).length;
  const url = (extra = '') => {
    const p = new URLSearchParams({ bank: '1', grade });
    if (picked.size) p.set('lessons', [...picked].sort((a, b) => a - b).join(','));
    if (levels.size < 4) p.set('levels', [...levels].join(','));
    if (kind !== 'all') p.set('kind', kind);
    if (title.trim()) p.set('title', title.trim());
    if (ans === 'key') p.set('key', '1');
    if (ans === 'both') p.set('ans', 'both');
    if (newpage) p.set('newpage', '1');
    return `paper.html?${p}${extra}`;
  };
  const draw = () => {
    body.innerHTML = '';
    const ls = lessonList();
    const sel = picked.size ? [...picked] : ls.map((_, i) => i + 1);
    const total = sel.reduce((t, i) => t + countOf(ls[i - 1]), 0);
    const pages = Math.max(1, Math.ceil(total / 5.5));
    const chips = (items, on, set) => h('div', { class: 'ex-chips' }, items.map(([v, l]) => h('button', { type: 'button', class: on(v) ? 'on' : '', onclick: () => { set(v); draw(); } }, l)));
    body.append(
      h('label', {}, 'ថ្នាក់'),
      h('select', { onchange: (e) => { grade = e.target.value; picked.clear(); draw(); } }, bankGradesOf(curr).map((g) => h('option', { value: g, selected: g === grade ? 'selected' : null }, `${GRADE_KH(g)} (${questions.filter((q) => q.grade === g).length} សំណួរ)`))),
      h('div', { class: 'ex-lhead' }, [
        h('label', { style: 'margin:0;' }, 'មេរៀនដែលចង់បាន'),
        h('div', { class: 'row', style: 'gap:6px;' }, [
          h('button', { type: 'button', class: `secondary btn-sm${picked.size === 0 ? ' on' : ''}`, onclick: () => { picked.clear(); draw(); } }, '📚 សៀវភៅទាំងមូល'),
          h('button', { type: 'button', class: 'secondary btn-sm', onclick: () => { ls.forEach((_, i) => { if (countOf(ls[i])) picked.add(i + 1); }); draw(); } }, 'ជ្រើសទាំងអស់'),
        ]),
      ]),
      h('div', { class: 'ex-lessons' }, ls.length ? (
        curr.chapters && curr.chapters[grade] ? curr.chapters[grade].flatMap((c) => {
          const chLessons = c.lessons.map((name) => {
            const i = ls.indexOf(name);
            if (i < 0) return null;
            const n = countOf(name), on = picked.size === 0 ? false : picked.has(i + 1);
            return h('button', { type: 'button', class: `ex-l${on ? ' on' : ''}${n ? '' : ' empty'}`, disabled: n ? null : 'disabled', onclick: () => { if (picked.has(i + 1)) picked.delete(i + 1); else picked.add(i + 1); draw(); } }, [
              h('b', {}, khNum(i + 1)), h('span', { class: 'nm' }, name), h('small', {}, n ? `${khNum(n)} សំណួរ` : 'គ្មាន'),
            ]);
          }).filter(Boolean);
          return [
            h('div', { style: 'grid-column:1/-1;font-weight:700;font-size:13px;color:#047857;margin-top:10px;padding:4px 2px;border-bottom:1px solid #e2e8f0;' }, c.name),
            ...chLessons
          ];
        }) : ls.map((name, i) => {
          const n = countOf(name), on = picked.size === 0 ? false : picked.has(i + 1);
          return h('button', { type: 'button', class: `ex-l${on ? ' on' : ''}${n ? '' : ' empty'}`, disabled: n ? null : 'disabled', onclick: () => { if (picked.has(i + 1)) picked.delete(i + 1); else picked.add(i + 1); draw(); } }, [
            h('b', {}, khNum(i + 1)), h('span', { class: 'nm' }, name), h('small', {}, n ? `${khNum(n)} សំណួរ` : 'គ្មាន'),
          ]);
        })
      ) : [h('p', { class: 'muted' }, 'ថ្នាក់នេះមិនទាន់មានមេរៀនទេ។')]),
      h('label', {}, 'កម្រិត'),
      chips([['easy', 'ងាយ'], ['medium', 'មធ្យម'], ['hard', 'ពិបាក'], ['pisa', 'បែប PISA']], (v) => levels.has(v), (v) => { if (levels.has(v)) { if (levels.size > 1) levels.delete(v); } else levels.add(v); }),
      h('label', {}, 'ប្រភេទសំណួរ'),
      chips([['all', 'ទាំងអស់'], ['mcq', 'ពហុជ្រើសរើស'], ['writing', 'សរសេរ']], (v) => kind === v, (v) => { kind = v; }),
      h('label', {}, 'ឯកសារ'),
      chips([['none', '📄 សំណួរតែប៉ុណ្ណោះ (សម្រាប់សិស្ស)'], ['both', '📘 សំណួរ + ចម្លើយ ក្នុងឯកសារតែមួយ'], ['key', '✅ ចម្លើយតែប៉ុណ្ណោះ (សម្រាប់គ្រូ)']], (v) => ans === v, (v) => { ans = v; }),
      h('label', { class: 'ex-chk' }, [h('input', { type: 'checkbox', checked: newpage ? 'checked' : null, onchange: (e) => { newpage = e.target.checked; } }), 'ចាប់ផ្តើមមេរៀននីមួយៗលើទំព័រថ្មី']),
      h('label', {}, 'ចំណងជើង (មិនចាំបាច់)'),
      h('input', { type: 'text', placeholder: `លំហាត់គណិតវិទ្យា ${GRADE_KH(grade)}…`, value: title, oninput: (e) => { title = e.target.value; } }),
      h('div', { class: `ex-sum${total ? '' : ' none'}` }, total
        ? [h('b', {}, `${khNum(sel.filter((i) => countOf(ls[i - 1])).length)} មេរៀន · ${khNum(total)} សំណួរ`), ` · ប្រហែល ${khNum(pages)} ទំព័រ A4`, pages > 80 ? h('div', { class: 'muted' }, '⏳ សៀវភៅធំ — PDF ប្រើពេលយូរ (ប្រហែលមួយនាទី ឬច្រើនជាងនេះ)។ Word លឿនជាង។') : null]
        : 'គ្មានសំណួរតាមជម្រើសនេះទេ។'),
      h('div', { class: 'row ex-actions' }, [
        h('button', { class: 'secondary', onclick: () => m.remove() }, 'បិទ'),
        h('button', { class: 'secondary', disabled: total ? null : 'disabled', onclick: () => window.open(url(), '_blank') }, '👁 មើលជាមុន'),
        h('button', { class: 'secondary', disabled: total ? null : 'disabled', onclick: () => window.open(url('&docx=1'), '_blank') }, '📝 Word'),
        h('button', { disabled: total ? null : 'disabled', onclick: () => window.open(url('&autopdf=1'), '_blank') }, '⬇ PDF'),
      ]),
    );
  };
  const m = bankModal('📥 ទាញយកលំហាត់', box, true);
  draw();
}


let activeViewerModal = null;

// ---------- View modal to see the "real question" (full stem, image, choices with correct answer, solution/rubric) ----------
function openQuestionViewer(q, onEdit, nav = null, onDelete = null) {
  if (activeViewerModal) {
    try { activeViewerModal.remove(); } catch {}
    activeViewerModal = null;
  }

  const letters = ['ក', 'ខ', 'គ', 'ឃ', 'ង', 'ច'];
  const isWriting = q.kind === 'writing';
  const hasImg = Boolean(q.image_key);
  const opts = Array.isArray(q.options) ? q.options : (typeof q.options_json === 'string' ? JSON.parse(q.options_json || '[]') : []);

  let m;
  const copyId = () => {
    navigator.clipboard?.writeText(String(q.id));
    Exam.notify(`✓ បានចម្លង ID #${q.id}`);
  };

  const copyFullQuestion = () => {
    let text = `[ID #${q.id}] ${q.stem_text}
`;
    if (!isWriting && opts.length) {
      opts.forEach((o, i) => {
        text += `${letters[i] || i + 1}. ${o}${i === q.correct_index ? ' (✓)' : ''}
`;
      });
    }
    if (q.solution_text) {
      text += `
💡 ដំណោះស្រាយ៖
${q.solution_text}
`;
    }
    navigator.clipboard?.writeText(text);
    Exam.notify(`✓ បានចម្លងសំណួរ និងចម្លើយ!`);
  };

  // Fixed Header: Title + Tap-to-Copy #ID Badge + Navigation (❮ 12/50 ❯) + Close (✕)
  const titleRow = h('div', { class: 'qv-header' }, [
    h('div', { class: 'qv-title-left' }, [
      h('span', { class: 'qv-title-text' }, '👁 មើលសំណួរ'),
      h('button', {
        type: 'button',
        class: 'qv-id-badge',
        title: 'ចុចដើម្បីចម្លង ID',
        onclick: (e) => { e.stopPropagation(); copyId(); }
      }, [`#${q.id}`, h('span', { class: 'qv-copy-icon' }, '📋')])
    ]),

    // Carousel Navigation
    nav ? h('div', { class: 'qv-nav' }, [
      h('button', {
        type: 'button',
        class: 'qv-nav-arrow',
        disabled: !nav.hasPrev,
        title: 'សំណួរមុន (Arrow Left)',
        onclick: (e) => { e.stopPropagation(); nav.prev(); }
      }, '❮'),
      h('span', { class: 'qv-nav-counter' }, `${kh(nav.current)}/${kh(nav.total)}`),
      h('button', {
        type: 'button',
        class: 'qv-nav-arrow',
        disabled: !nav.hasNext,
        title: 'សំណួរបន្ទាប់ (Arrow Right)',
        onclick: (e) => { e.stopPropagation(); nav.next(); }
      }, '❯'),
    ]) : null,

    // Close button
    h('button', {
      type: 'button',
      class: 'qv-close-btn',
      title: 'បិទ (Esc)',
      onclick: () => m && m.remove()
    }, '✕')
  ]);

  // Independently scrollable body
  const scrollBody = h('div', { class: 'qv-scroll-body' }, [
    // Subtitle breadcrumb
    (q.grade || q.chapter || q.lesson) ? h('div', { class: 'qv-breadcrumb' }, [
      q.grade ? h('span', { class: 'qv-crumb-grade' }, `ថ្នាក់ទី ${kh(q.grade)}`) : null,
      (q.grade && (q.chapter || q.lesson)) ? h('span', { class: 'qv-crumb-sep' }, '·') : null,
      q.chapter ? h('span', { class: 'qv-crumb-chapter', style: 'color:#047857;font-weight:600;' }, q.chapter) : null,
      (q.chapter && q.lesson) ? h('span', { class: 'qv-crumb-sep' }, '·') : null,
      q.lesson ? h('span', { class: 'qv-crumb-lesson' }, `មេរៀន ៖ ${q.lesson}`) : null,
    ]) : null,

    // Chips tags
    h('div', { class: 'qv-tags' }, [
      isWriting ? h('span', { class: 'chip chip-soon' }, '✎ សរសេរ') : h('span', { class: 'chip chip-plain' }, 'ពហុជ្រើសរើស'),
      q.level ? h('span', { class: `chip ${q.level === 'hard' ? 'chip-closed' : q.level === 'pisa' ? 'chip-soon' : 'chip-open'}` }, `កម្រិត ៖ ${LEVEL_KH[q.level] || q.level}`) : null,
      h('span', { class: 'chip chip-plain' }, `${kh(q.points)} ពិន្ទុ`),
      (q.topic && q.topic !== q.lesson) ? h('span', { class: 'chip chip-plain' }, `ប្រធានបទ ៖ ${q.topic}`) : null,
      hasImg ? h('span', { class: 'chip', style: 'background:#f0fdf4;color:#166534;border:1px solid #bbf7d0;font-family:ui-monospace,monospace;' }, `🖼 ${q.image_key}`) : null,
      q.test_title ? h('span', { class: 'muted', style: 'font-size:12px;' }, q.test_title) : null,
    ]),

    // Stem Box
    h('div', { class: 'qv-stem-card' }, [
      h('div', { class: 'qv-stem-top' }, [
        h('span', { class: 'qv-stem-lbl' }, '📖 តួសំណួរ ៖'),
        h('button', {
          type: 'button',
          class: 'qv-copy-stem-btn',
          title: 'ចម្លងសំណួរ និងចម្លើយទាំងអស់',
          onclick: copyFullQuestion
        }, '📋 ចម្លងសំណួរ')
      ]),
      mathEl('div', { class: 'qv-stem-text' }, q.stem_text)
    ]),

    // Image if present
    hasImg ? h('div', { class: 'qv-img-card' }, [
      h('img', {
        src: '/api/images/' + encodeURIComponent(q.image_key),
        alt: q.image_key,
        class: 'qv-img'
      }),
      h('div', { class: 'qv-img-toolbar' }, [
        h('span', { class: 'qv-img-key' }, q.image_key),
        h('button', {
          type: 'button',
          class: 'secondary btn-sm',
          style: 'padding:3px 8px;font-size:11px;',
          onclick: () => {
            navigator.clipboard?.writeText(q.image_key);
            Exam.notify(`បានចម្លងឈ្មោះរូបភាព៖ ${q.image_key}`);
          }
        }, '📋 ចម្លងឈ្មោះ'),
        h('a', {
          href: '/api/images/' + encodeURIComponent(q.image_key),
          target: '_blank',
          class: 'qv-img-zoom-link'
        }, '↗ មើលទំហំពេញ')
      ])
    ]) : null,

    // Real Options (MCQ)
    !isWriting ? h('div', { class: 'qv-choices-card' }, [
      h('div', { class: 'qv-choices-title' }, 'ជម្រើសចម្លើយ ៖'),
      ...opts.map((opt, idx) => {
        const isCorrect = idx === q.correct_index;
        const isAlt = idx === q.alt_correct_index;
        const cardClass = isCorrect ? 'qv-choice is-correct' : isAlt ? 'qv-choice is-alt' : 'qv-choice';
        const letterClass = isCorrect ? 'qv-letter is-correct' : isAlt ? 'qv-letter is-alt' : 'qv-letter';

        return h('div', { class: cardClass }, [
          h('div', { class: letterClass }, isCorrect ? '✓' : isAlt ? '✓' : letters[idx] || String(idx + 1)),
          mathEl('div', { class: 'qv-choice-text' }, opt),
          isCorrect ? h('span', { class: 'qv-choice-tag correct' }, 'ចម្លើយត្រឹមត្រូវ ✓') : null,
          isAlt ? h('span', { class: 'qv-choice-tag alt' }, 'ទទួលយកបាន ✓') : null,
        ]);
      })
    ]) : null,

    // Solution / Explanation
    q.solution_text ? h('div', { class: isWriting ? 'qv-sol-card writing' : 'qv-sol-card mcq' }, [
      h('div', { class: 'qv-sol-head' }, [
        h('span', { class: 'qv-sol-icon' }, isWriting ? '📝' : '💡'),
        h('b', { class: 'qv-sol-title' }, isWriting ? 'ដំណោះស្រាយ និងរបៀបដាក់ពិន្ទុ (Rubric) ៖' : 'ការពន្យល់ និងដំណោះស្រាយ (Explanation) ៖')
      ]),
      mathEl('div', { class: 'qv-sol-content' }, q.solution_text)
    ]) : null,
  ]);

  // Fixed Bottom Action Bar
  const footerActions = h('div', { class: 'qv-footer-actions' }, [
    onEdit ? h('button', {
      type: 'button',
      class: 'qv-btn-edit',
      onclick: () => { m && m.remove(); onEdit(); }
    }, '✏️ កែសំណួរនេះ') : null,
    onDelete ? h('button', {
      type: 'button',
      class: 'danger qv-btn-delete',
      onclick: async () => { if (await onDelete()) m && m.remove(); }
    }, '🗑 លុបសំណួរ') : null,
    h('button', {
      type: 'button',
      class: 'secondary qv-btn-copy',
      onclick: copyId
    }, '📋 ចម្លង ID'),
    h('button', {
      type: 'button',
      class: 'secondary qv-btn-close',
      onclick: () => m && m.remove()
    }, 'បិទ')
  ]);

  const body = h('div', { class: 'question-viewer' }, [
    scrollBody,
    footerActions
  ]);

  m = bankModal(titleRow, body, true);
  activeViewerModal = m;

  // Keyboard navigation support
  const onKey = (e) => {
    if (e.key === 'Escape') { m.remove(); }
    else if (e.key === 'ArrowLeft' && nav && nav.hasPrev) { nav.prev(); }
    else if (e.key === 'ArrowRight' && nav && nav.hasNext) { nav.next(); }
  };
  window.addEventListener('keydown', onKey);
  const origRemove = m.remove.bind(m);
  m.remove = () => {
    window.removeEventListener('keydown', onKey);
    if (activeViewerModal === m) activeViewerModal = null;
    origRemove();
  };

  return m;
}

render.bank = async function () {
  const container = document.getElementById('tab-bank');
  container.innerHTML = '';
  // «ថ្នាក់ខ្ញុំ» downloads only the grades this teacher taught last time (remembered here); a new grade triggers one full download
  let hint = ''; try { if (localStorage.getItem('bank_mine') !== '0') hint = localStorage.getItem('bank_my_grades') || ''; } catch {}
  if (bankState.mine === false) hint = '';
  let [{ questions: allQuestions }, { tests }, curr, classRes] = await Promise.all([api(hint ? `/api/bank?grades=${encodeURIComponent(hint)}` : '/api/bank'), api('/api/tests'), loadCurr(true), api('/api/classes').catch(() => ({ classes: [] }))]);
  // «ថ្នាក់ខ្ញុំ»: the bank opens on the grades this teacher teaches; «គ្រប់ថ្នាក់» shows every grade (tests can mix grades)
  const myClasses = (classRes.classes || []).filter((c) => bankGradesOf(curr).includes(String(c.grade)));
  const myGrades = [...new Set(myClasses.map((c) => String(c.grade)))].sort((a, b) => Number(a) - Number(b));
  try { localStorage.setItem('bank_my_grades', myGrades.join(',')); } catch {}
  if (hint && myGrades.some((g) => !hint.split(',').includes(g))) allQuestions = (await api('/api/bank')).questions;   // a grade not downloaded yet
  if (bankState.mine === null) { let v = null; try { v = localStorage.getItem('bank_mine'); } catch {} bankState.mine = v === null ? myGrades.length > 0 : v === '1'; }
  const mineOn = bankState.mine && myGrades.length > 0 && bankState.grade !== '-';
  if (mineOn && bankState.grade && !myGrades.includes(bankState.grade)) Object.assign(bankState, { grade: '', chapter: '', lesson: '' });
  const questions = mineOn ? allQuestions.filter((q) => !q.grade || myGrades.includes(String(q.grade))) : allQuestions;
  const setMine = (v) => { bankState.mine = v; try { localStorage.setItem('bank_mine', v ? '1' : '0'); } catch {} if (v && bankState.grade && !myGrades.includes(bankState.grade)) Object.assign(bankState, { grade: '', chapter: '', lesson: '' }); render.bank(); };
  const editable = tests.filter((t) => (t.my_role === 'owner' || t.my_role === 'editor') && !t.is_sample);
  const selected = bankSelected;
  if (!hint) { const have = new Set(allQuestions.map((q) => q.id)); [...selected].forEach((id) => { if (!have.has(id)) selected.delete(id); }); }   // (only when every grade was downloaded)   // forget questions that were deleted
  const S = bankState;
  // What's new in the shared library since this teacher last looked (ids only grow, so "bigger than last seen" = added since).
  let seenMax = 0; try { seenMax = Number(localStorage.getItem('bank_seen_max') || 0); } catch {}
  const sharedQs = questions.filter((q) => q.shared);
  const maxShared = sharedQs.reduce((m, q) => Math.max(m, q.id), 0);
  const isNew = (q) => q.shared && seenMax > 0 && q.id > seenMax;
  const newCount = sharedQs.filter(isNew).length;
  if (seenMax === 0 && maxShared) { try { localStorage.setItem('bank_seen_max', String(maxShared)); } catch {} }
  const topics = [...new Set(questions.map((q) => q.topic).filter(Boolean))].sort();
  const reload = async () => { const y = window.scrollY; await render.bank(); window.scrollTo(0, y); };   // stay where the teacher was

  // lessons per grade: the curriculum list first, then any other lesson names found on questions
  const lessonsOf = (g) => {
    const base = curr.lessons[g] || [];
    const extra = [...new Set(questions.filter((q) => q.grade === g && q.lesson && !base.includes(q.lesson)).map((q) => q.lesson))];
    return [...base, ...extra];
  };
  const count = (fn) => questions.filter(fn).length;

  // ---------- header + grade tabs
  const gradePill = (val, label, n) => h('button', { class: `filter-pill${S.grade === val ? ' on' : ''}`, onclick: () => { Object.assign(S, { grade: val, chapter: '', lesson: '' }); reload(); } }, [label, ' ', h('span', { class: 'pill-n' }, String(n))]);
  const pills = h('div', { class: 'filter-bar' }, [
    myGrades.length ? h('button', { class: `filter-pill scope-pill${mineOn ? ' on' : ''}`, title: 'បង្ហាញតែថ្នាក់ដែលខ្ញុំបង្រៀន', onclick: () => setMine(true) }, '⭐ ថ្នាក់ខ្ញុំ') : null,
    myGrades.length ? h('button', { class: `filter-pill scope-pill${!mineOn ? ' on' : ''}`, title: 'បង្ហាញគ្រប់ថ្នាក់', onclick: () => setMine(false) }, '🌐 គ្រប់ថ្នាក់') : null,
    gradePill('', mineOn ? 'ទាំងអស់ (ថ្នាក់ខ្ញុំ)' : 'ទាំងអស់', questions.length),
    ...(mineOn ? myGrades : bankGradesOf(curr)).map((g) => gradePill(g, GRADE_KH(g), count((q) => q.grade === g))),
    mineOn ? null : gradePill('-', 'មិនទាន់កំណត់ថ្នាក់', count((q) => !q.grade)),
  ].filter(Boolean));
  const classChips = mineOn && myClasses.length ? h('div', { class: 'row', style: 'gap:6px;flex-wrap:wrap;margin-top:8px;align-items:center;' }, [
    h('span', { class: 'muted', style: 'font-size:12px;' }, 'ថ្នាក់របស់ខ្ញុំ ៖'),
    ...myClasses.map((c) => h('button', { type: 'button', class: `chip chip-plain class-chip${S.grade === String(c.grade) ? ' on' : ''}`, style: 'cursor:pointer;', title: `ទៅកាន់ ${GRADE_KH(String(c.grade))}`,
      onclick: () => { Object.assign(S, { grade: String(c.grade), chapter: '', lesson: '' }); reload(); } }, `${c.name} · ${GRADE_KH(String(c.grade))}`)),
  ]) : null;
  if (newCount) container.append(h('div', { class: 'card', style: 'background:#fff4dc;border:1px solid #f1d28a;display:flex;gap:12px;align-items:center;flex-wrap:wrap;' }, [
    h('div', { style: 'flex:1;min-width:200px;' }, [h('b', {}, `🆕 ឃ្លាំងសំណួររួមមាន ${newCount} សំណួរថ្មី`), h('div', { class: 'muted' }, 'ម្ចាស់ប្រព័ន្ធទើបបន្ថែម — មើលសំណួរដែលមានស្លាក «🆕 ថ្មី» ខាងក្រោម។')]),
    h('button', { class: 'secondary', onclick: () => { try { localStorage.setItem('bank_seen_max', String(maxShared)); } catch {} render.bank(); } }, '✓ បានមើលហើយ'),
  ]));
  container.append(h('div', { class: 'card' }, [
    h('div', { class: 'row', style: 'justify-content:space-between;align-items:center;gap:10px;' }, [
      h('h2', { style: 'margin:0;' }, `🗂 ធនាគារសំណួរ (${questions.length}${mineOn ? (hint ? ' · ថ្នាក់ខ្ញុំ' : ` ក្នុងចំណោម ${allQuestions.length}`) : ''})`),
      h('button', { class: 'no-phone', onclick: () => openExport(questions, curr, S) }, '📥 ទាញយកលំហាត់ជា PDF / Word'),
    ]),
    h('p', { class: 'muted' }, 'រៀបតាមថ្នាក់ → ជំពូក → មេរៀន។ បន្ថែមសំណួរចូលជំពូក និងមេរៀន រួចពេលបង្កើតតេស្ត គ្រាន់តែជ្រើសរើសពីមេរៀន ឬផ្នែកដែលចង់បាន។'),
    pills,
    classChips,
  ]));

  // ---------- lesson sidebar (grouped by chapter when available)
  const showLessons = S.grade && S.grade !== '-';
  const inGrade = (q) => !S.grade || (S.grade === '-' ? !q.grade : q.grade === S.grade);
  const side = h('div', { class: 'card bank-side', style: 'padding:10px;' });
  if (showLessons) {
    const lv = (qs, l) => qs.filter((q) => q.level === l).length;
    const lessonBtn = (val, label, qs) => {
      return h('button', { class: `lesson-btn${S.lesson === val ? ' on' : ''}`, onclick: () => { S.lesson = val; reload(); } }, [
        h('span', { class: 'lesson-name' }, label),
        h('span', { class: 'lesson-n' }, qs.length ? `${khNum(qs.length)}` : '—'),
        qs.length ? h('span', { class: 'lesson-lv' }, `ង ${lv(qs, 'easy')} · ម ${lv(qs, 'medium')} · ព ${lv(qs, 'hard')} · PISA ${lv(qs, 'pisa')}`) : null,
      ]);
    };
    const gq = questions.filter(inGrade);
    const allOn = !S.chapter && !S.lesson;
    side.append(h('div', { class: 'lesson-title' }, GRADE_KH(S.grade)), h('button', {
      class: `lesson-btn${allOn ? ' on' : ''}`,
      onclick: () => { S.chapter = ''; S.lesson = ''; reload(); }
    }, [
      h('span', { class: 'lesson-name' }, 'សំណួរទាំងអស់'),
      h('span', { class: 'lesson-n' }, gq.length ? `${khNum(gq.length)}` : '—'),
      gq.length ? h('span', { class: 'lesson-lv' }, `ង ${lv(gq, 'easy')} · ម ${lv(gq, 'medium')} · ព ${lv(gq, 'hard')} · PISA ${lv(gq, 'pisa')}`) : null,
    ]));

    const chList = (curr.chapters && curr.chapters[S.grade]) || null;
    if (chList && chList.length) {
      const placedLessons = new Set();
      chList.forEach((c) => {
        const cq = gq.filter((q) => (q.chapter === c.name || (!q.chapter && c.lessons.includes(q.lesson))));
        const chActive = S.chapter === c.name && !S.lesson;
        const chBtn = h('button', {
          type: 'button',
          class: `chapter-btn${chActive ? ' on' : ''}`,
          title: `ចុចដើម្បីមើលសំណួរទាំងអស់ក្នុង ${c.name}`,
          onclick: () => {
            S.chapter = (S.chapter === c.name && !S.lesson) ? '' : c.name;
            S.lesson = '';
            reload();
          }
        }, [
          h('span', { class: 'chapter-title' }, c.name),
          h('span', { class: 'chapter-n' }, cq.length ? `${khNum(cq.length)}` : '—')
        ]);

        const lesBtns = c.lessons.map((lesName, li) => {
          placedLessons.add(lesName);
          const lq = cq.filter((q) => q.lesson === lesName);
          const on = S.lesson === lesName;
          return h('button', {
            type: 'button',
            class: `lesson-btn${on ? ' on' : ''}`,
            onclick: () => {
              S.chapter = c.name;
              S.lesson = lesName;
              reload();
            }
          }, [
            h('span', { class: 'lesson-name' }, `${khNum(li + 1)}. ${lesName}`),
            h('span', { class: 'lesson-n' }, lq.length ? `${khNum(lq.length)}` : '—'),
            lq.length ? h('span', { class: 'lesson-lv' }, `ង ${lv(lq, 'easy')} · ម ${lv(lq, 'medium')} · ព ${lv(lq, 'hard')} · PISA ${lv(lq, 'pisa')}`) : null,
          ]);
        });

        const chGroup = h('div', { class: 'chapter-group' }, [
          chBtn,
          h('div', { class: 'chapter-lessons' }, lesBtns)
        ]);
        side.append(chGroup);
      });

      const otherLessons = lessonsOf(S.grade).filter((n) => !placedLessons.has(n));
      if (otherLessons.length) {
        side.append(h('div', { class: 'muted', style: 'font-size:12px;margin:10px 0 4px 8px;font-weight:700;' }, 'មេរៀនផ្សេងៗ'));
        otherLessons.forEach((name, i) => side.append(lessonBtn(name, `${khNum(i + 1)}. ${name}`, gq.filter((q) => q.lesson === name))));
      }
    } else {
      lessonsOf(S.grade).forEach((name, i) => side.append(lessonBtn(name, `${khNum(i + 1)}. ${name}`, gq.filter((q) => q.lesson === name))));
    }

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
  let page = 1;   // current page of the question list
  const countLbl = h('b', {}, '0');
  const targetSel = h('select', { style: 'width:auto;max-width:170px;' }, editable.map((t) => h('option', { value: t.id }, t.title)));
  const addBtn = h('button', { class: 'btn-sm', disabled: 'disabled', onclick: async () => {
    if (!targetSel.value) return Exam.notify('សូមបង្កើតតេស្តមួយជាមុនសិន។');
    try { const r = await api(`/api/tests/${targetSel.value}/questions/copy`, { method: 'POST', body: { question_ids: [...selected] } }); await Exam.notify(`✅ បានថែម ${r.copied} សំណួរទៅតេស្ត។`); selected.clear(); draw(); } catch (e) { Exam.notify(e.message); }
  } }, '➕ ថែមទៅតេស្ត');
  const tagBtn = h('button', { class: 'secondary btn-sm', disabled: 'disabled', onclick: () => {
    const gl = gradeLessonPicker(S.grade && S.grade !== '-' ? S.grade : '', showLessons && S.lesson && S.lesson !== '-' ? S.lesson : '', curr, showLessons && S.chapter ? S.chapter : '');
    const box = h('div', {}, [h('p', { class: 'muted' }, `ដាក់ ${selected.size} សំណួរក្នុង៖`),
      h('label', {}, 'ថ្នាក់'), gl.grade,
      h('label', {}, 'ជំពូក'), gl.chapter, gl.chDl,
      h('label', {}, 'មេរៀន'), gl.lesson, gl.dl,
      h('div', { class: 'row', style: 'justify-content:flex-end;margin-top:14px;' }, [
        h('button', { class: 'secondary', onclick: () => m.remove() }, 'បោះបង់'),
        h('button', { onclick: async () => {
          try { const r = await api('/api/bank/tag', { method: 'POST', body: { question_ids: [...selected], ...gl.get() } }); m.remove(); await Exam.notify(`✅ បានដាក់ ${r.tagged} សំណួរក្នុងមេរៀន។`); reload(); } catch (e) { Exam.notify(e.message); }
        } }, 'រក្សាទុក')])]);
    const m = bankModal('🏷 ដាក់ក្នុងមេរៀន', box);
  } }, '🏷 ដាក់ក្នុងមេរៀន');
  const paperBtn = h('button', {
    class: 'btn-sm bank-bar-go',
    disabled: !selected.size,
    onclick: () => {
      if (!selected.size) return;
      const selArr = [...selected];
      const pickedQs = questions.filter((q) => selected.has(q.id));
      const mcqCount = pickedQs.filter((q) => q.kind !== 'writing').length;
      const wCount = pickedQs.filter((q) => q.kind === 'writing').length;
      const totalPts = pickedQs.reduce((a, q) => a + (q.points || 1), 0);

      // a test made from questions of any lesson or grade: the default title says which ones
      const grades = [...new Set(pickedQs.map((q) => q.grade).filter(Boolean))];
      const lessonsPicked = [...new Set(pickedQs.map((q) => q.lesson).filter(Boolean))];
      const gradeText = grades.length ? (grades.length === 1 ? `ថ្នាក់ទី ${khNum(grades[0])}` : `ថ្នាក់ទី ${grades.map(khNum).join(' · ')}`) : '';
      const lessonText = lessonsPicked.length === 1 ? `មេរៀន ${lessonsPicked[0]}` : lessonsPicked.length ? `${khNum(lessonsPicked.length)} មេរៀន` : '';
      const defaultTitle = `វិញ្ញាសា${gradeText ? ' ' + gradeText : ''}${lessonText ? ' ' + lessonText : ''} (${khNum(selArr.length)} សំណួរ · ${khNum(totalPts)} ពិន្ទុ)`;

      const titleInp = h('input', { type: 'text', value: defaultTitle, style: 'width:100%;margin-top:4px;' });
      // what the test is made of: one line per grade + lesson
      const groups = new Map();
      pickedQs.forEach((q) => { const k = `${q.grade ? GRADE_KH(q.grade) : 'មិនទាន់កំណត់ថ្នាក់'} · ${q.lesson || 'មិនទាន់កំណត់មេរៀន'}`; groups.set(k, (groups.get(k) || 0) + 1); });
      const breakdown = h('div', { style: 'max-height:150px;overflow:auto;border:1px solid #e2e8f0;border-radius:10px;padding:6px 10px;margin-top:8px;font-size:13px;' },
        [...groups.entries()].map(([k, n]) => h('div', { style: 'display:flex;justify-content:space-between;gap:10px;padding:2px 0;' }, [h('span', {}, k), h('b', {}, `${khNum(n)} សំណួរ`)])));

      const box = h('div', { style: 'text-align:left;' }, [
        h('div', { class: 'row', style: 'gap:8px;flex-wrap:wrap;margin:0 0 10px;' }, [
          h('span', { class: 'chip chip-plain' }, `${khNum(selArr.length)} សំណួរ`),
          h('span', { class: 'chip chip-open' }, `${khNum(totalPts)} ពិន្ទុ`),
          mcqCount ? h('span', { class: 'chip chip-plain' }, `ពហុជ្រើសរើស ${khNum(mcqCount)}`) : null,
          wCount ? h('span', { class: 'chip chip-soon' }, `សរសេរ ${khNum(wCount)}`) : null,
          grades.length > 1 ? h('span', { class: 'chip chip-plain' }, `${khNum(grades.length)} ថ្នាក់`) : null,
        ]),
        h('p', { class: 'muted', style: 'margin-top:0;' }, 'បង្កើតវិញ្ញាសាពីសំណួរដែលបានជ្រើស (អាចមកពីមេរៀន និងថ្នាក់ផ្សេងៗគ្នា)។'),
        breakdown,
        h('label', { style: 'font-weight:600;display:block;margin-top:12px;' }, 'ចំណងជើងវិញ្ញាសា'),
        titleInp,
        h('p', { class: 'muted', style: 'font-size:12px;margin-top:10px;' }, 'បន្ទាប់ពីបង្កើត អ្នកនឹងទៅកាន់ផ្នែក «តេស្ត» ដើម្បីពិនិត្យ កែពិន្ទុ និងថែមសំណួរបន្ថែមពីធនាគារ មុនពេលបោះពុម្ព ឬទាញយក PDF / Word។'),
        h('div', { class: 'row', style: 'justify-content:flex-end;gap:8px;margin-top:18px;' }, [
          h('button', { class: 'secondary', onclick: () => m.remove() }, 'បោះបង់'),
          h('button', {
            style: 'background:#16a34a;color:#fff;font-weight:600;',
            onclick: async () => {
              const ttl = titleInp.value.trim() || defaultTitle;
              try {
                const newTest = await api('/api/tests', { method: 'POST', body: { title: ttl } });
                const r = await api(`/api/tests/${newTest.id}/questions/copy`, { method: 'POST', body: { question_ids: selArr } });
                m.remove();
                selected.clear();
                if (r.copied < selArr.length) await Exam.notify(`⚠ បានថែមតែ ${khNum(r.copied)} ក្នុងចំណោម ${khNum(selArr.length)} សំណួរ (ដល់កម្រិតកំណត់នៃគម្រោង)។`);
                else Exam.notify(`✅ បានបង្កើតវិញ្ញាសា «${ttl}» — ${khNum(r.copied)} សំណួរ`);
                selectedTestId = newTest.id;                                   // open it in the «តេស្ត» tab, in this same page
                const tab = document.querySelector('.tabs button[data-tab="tests"], [data-tab="tests"]');
                if (tab) tab.click(); else render.tests();
              } catch (e) {
                Exam.notify(e.message);
              }
            }
          }, '📄 បង្កើត រួចពិនិត្យក្នុងតេស្ត →')
        ])
      ]);
      const m = bankModal('📄 បង្កើតវិញ្ញាសាភ្លាមៗ', box);
    }
  }, [h('span', {}, '📄'), ' បង្កើតវិញ្ញាសាភ្លាមៗ']);
  const delSelBtn = canBankDelete() ? h('button', {
    class: 'danger btn-sm',
    disabled: 'disabled',
    onclick: async () => {
      if (!selected.size) return;
      if (!(await Exam.confirm(`លុបសំណួរ ${selected.size} ពីធនាគារសំណួរ?\nសកម្មភាពនេះមិនអាចត្រឡប់វិញបានទេ។`))) return;
      try {
        const r = await api('/api/bank/delete', { method: 'POST', body: { question_ids: [...selected] } });
        selected.clear();
        await Exam.notify(`✅ បានលុប ${r.deleted} សំណួរ។${r.blocked ? ` មិនអាចលុប ${r.blocked} (មានសិស្សឆ្លើយរួច)` : ''}`);
        await reload();
      } catch (e) { Exam.notify(e.message); }
    }
  }, '🗑 លុបដែលបានជ្រើស') : null;
  const ptsLbl = h('b', {}, '0');
  const clearBtn = h('button', { class: 'secondary btn-sm', title: 'ដកការជ្រើសរើសទាំងអស់ (រួមទាំងមេរៀន និងថ្នាក់ផ្សេងទៀត)', onclick: () => { selected.clear(); draw(); } }, '✕ ដកការជ្រើស');
  const bar = h('div', { class: 'bank-bar' }, [h('span', { class: 'bank-bar-count' }, ['បានជ្រើស ', countLbl, ' សំណួរ · ', ptsLbl, ' ពិន្ទុ']), clearBtn, paperBtn, tagBtn, delSelBtn, targetSel, addBtn].filter(Boolean));

  const fLevel = h('select', { style: 'width:auto;' }, [['', 'គ្រប់កម្រិត'], ['easy', 'ងាយ'], ['medium', 'មធ្យម'], ['hard', 'ពិបាក'], ['pisa', 'បែប PISA']].map(([v, l]) => h('option', { value: v, selected: S.level === v ? 'selected' : null }, l)));
  const fKind = h('select', { style: 'width:auto;' }, [['', 'គ្រប់ប្រភេទ'], ['mcq', 'ពហុជ្រើសរើស'], ['writing', 'សរសេរ']].map(([v, l]) => h('option', { value: v, selected: S.kind === v ? 'selected' : null }, l)));
  const fTopic = topics.length ? h('select', { style: 'width:auto;' }, [h('option', { value: '' }, 'គ្រប់ប្រធានបទ'), ...topics.map((t) => h('option', { value: t, selected: S.topic === t ? 'selected' : null }, t))]) : null;
  const fQ = h('input', { type: 'text', placeholder: '🔍 ស្វែងរក…', value: S.q, style: 'max-width:200px;' });

  const bankId = async () => (await api('/api/bank/home')).id;
  const presetGrade = () => (S.grade && S.grade !== '-' ? S.grade : '');
  const presetLesson = () => (showLessons && S.lesson && S.lesson !== '-' ? S.lesson : '');
  const newBtn = h('button', { onclick: async () => {
    const id = await bankId(); const holder = h('div', {});
    const m = bankModal('➕ សំណួរថ្មីក្នុងធនាគារ', holder, true);
    holder.append(await buildQuestionForm({ id }, holder, { grade: presetGrade(), chapter: (showLessons && S.chapter ? S.chapter : ''), lesson: presetLesson(), onDone: () => { m.remove(); reload(); } }));
  } }, '➕ សំណួរថ្មី');
  const importBtn = h('button', { class: 'secondary', onclick: async () => {
    const id = await bankId(); const holder = h('div', {});
    const m = bankModal('📥 នាំចូលសំណួរពី Excel', holder, true);
    holder.append(h('p', { class: 'muted' }, 'ដាក់ជួរ grade (ថ្នាក់) និង lesson (មេរៀន) ក្នុង Excel ដើម្បីឱ្យសំណួរចូលមេរៀនត្រឹមត្រូវ។'), importQuestionsCard({ id }, holder, () => { m.remove(); reload(); }));
  } }, '📥 នាំចូល Excel');
  const selAll = h('button', { class: 'secondary btn-sm', onclick: () => { const rows = visible(); const all = rows.every((x) => selected.has(x.id)); rows.forEach((x) => (all ? selected.delete(x.id) : selected.add(x.id))); draw(); } }, '☑ ជ្រើសទាំងអស់ដែលបង្ហាញ');

  const visible = () => {
    const q = fQ.value.trim().toLowerCase();
    const inChapter = (x) => {
      if (!S.chapter) return true;
      if (x.chapter) return x.chapter === S.chapter;
      const chObj = (curr.chapters && curr.chapters[S.grade] || []).find((c) => c.name === S.chapter);
      return chObj ? chObj.lessons.includes(x.lesson) : false;
    };
    return questions.filter((x) => inGrade(x)
      && (!showLessons || inChapter(x))
      && (!showLessons || !S.lesson || (S.lesson === '-' ? !x.lesson : x.lesson === S.lesson))
      && (!fLevel.value || x.level === fLevel.value) && (!fKind.value || x.kind === fKind.value) && (!fTopic || !fTopic.value || x.topic === fTopic.value)
      && (!q || x.stem_text.toLowerCase().includes(q)));
  };
  function draw() {
    Object.assign(S, { level: fLevel.value, kind: fKind.value, topic: fTopic ? fTopic.value : '', q: fQ.value });
    const rows = visible();
    list.innerHTML = '';
    if (!rows.length) list.append(h('div', { class: 'empty-card' }, h('div', { class: 'muted' }, questions.length ? 'មិនមានសំណួរក្នុងផ្នែកនេះទេ — ចុច «➕ សំណួរថ្មី» ឬ «📥 នាំចូល Excel»។' : 'មិនទាន់មានសំណួរទេ — ចុច «➕ សំណួរថ្មី» ឬបង្កើតតេស្តជាមុនសិន។')));
    const PER = 20;   // questions per page: a short page draws fast (every stem is maths-typeset)
    const pages = Math.max(1, Math.ceil(rows.length / PER));
    if (page > pages) page = pages;
    const start = (page - 1) * PER;
    const pager = () => rows.length <= PER ? null : h('div', { class: 'bank-pager' }, [
      h('button', { class: 'secondary btn-sm', disabled: page <= 1 ? 'disabled' : null, onclick: () => { page--; draw(); window.scrollTo({ top: 0 }); } }, '‹'),
      ...[...new Set([1, 2, page - 1, page, page + 1, pages - 1, pages])].filter((n) => n >= 1 && n <= pages).sort((a, b) => a - b).flatMap((n, i, arr) => [
        i && n - arr[i - 1] > 1 ? h('span', { class: 'muted' }, '…') : null,
        h('button', { class: `btn-sm${n === page ? '' : ' secondary'}`, onclick: () => { page = n; draw(); window.scrollTo({ top: 0 }); } }, khNum(n)),
      ]).filter(Boolean),
      h('button', { class: 'secondary btn-sm', disabled: page >= pages ? 'disabled' : null, onclick: () => { page++; draw(); window.scrollTo({ top: 0 }); } }, '›'),
      h('span', { class: 'muted', style: 'font-size:12px;' }, `${khNum(start + 1)}–${khNum(Math.min(rows.length, start + PER))} / ${khNum(rows.length)}`),
    ]);
    const topPager = pager(); if (topPager) list.append(topPager);
        rows.slice(start, start + PER).forEach((x, i) => { const idx = start + i;
      const cb = h('input', { type: 'checkbox', style: 'width:20px;height:20px;flex:none;cursor:pointer;margin-top:3px;', checked: selected.has(x.id) ? 'checked' : null, onchange: (e) => { e.target.checked ? selected.add(x.id) : selected.delete(x.id); upd(); } });
      const canEdit = !x.shared || (typeof ME !== 'undefined' && ME && ME.role === 'owner');
      const onEdit = canEdit ? () => openQuestionEditor(x, { id: x.test_id, submissions: 0 }, null, reload) : null;
      const deleteOne = async (q) => {
        if (!canBankDelete()) return false;
        if (!(await Exam.confirm(`លុបសំណួរ #${q.id} ពីធនាគារសំណួរ?\nសកម្មភាពនេះមិនអាចត្រឡប់វិញបានទេ។`))) return false;
        try {
          await api(`/api/questions/${q.id}`, { method: 'DELETE' });
          await Exam.notify('✅ បានលុបសំណួរពីធនាគារ។');
          await reload();
          return true;
        } catch (e) { Exam.notify(e.message); return false; }
      };
      const openViewer = (targetIdx = idx) => {
        const targetQ = rows[targetIdx];
        if (!targetQ) return;
        const nav = {
          current: targetIdx + 1,
          total: rows.length,
          hasPrev: targetIdx > 0,
          hasNext: targetIdx < rows.length - 1,
          prev: () => openViewer(targetIdx - 1),
          next: () => openViewer(targetIdx + 1)
        };
        const canEditTarget = !targetQ.shared || (typeof ME !== 'undefined' && ME && ME.role === 'owner');
        const onEditTarget = canEditTarget ? () => openQuestionEditor(targetQ, { id: targetQ.test_id, submissions: 0 }, null, reload) : null;
        const onDeleteTarget = canBankDelete() ? () => deleteOne(targetQ) : null;
        return openQuestionViewer(targetQ, onEditTarget, nav, onDeleteTarget);
      };

      const viewBtn = h('button', {
        type: 'button',
        class: 'secondary btn-sm',
        title: 'មើលសំណួរពេញលេញ និងចម្លើយ',
        onclick: (e) => { e.preventDefault(); e.stopPropagation(); openViewer(idx); }
      }, '👁 មើល');

      const editBtn = canEdit
        ? h('button', {
            type: 'button',
            class: 'secondary btn-sm',
            title: 'កែសំណួរ',
            onclick: (e) => { e.preventDefault(); e.stopPropagation(); onEdit(); }
          }, '✏️')
        : (x.shared ? h('span', { class: `chip ${isNew(x) ? 'chip-closed' : 'chip-plain'}`, title: 'សំណួររួមរបស់ប្រព័ន្ធ — ចម្លងទៅតេស្តរបស់អ្នកបាន' }, (isNew(x) ? '🆕 ថ្មី' : '🌐 រួម')) : null);
      const delBtn = canBankDelete()
        ? h('button', {
            type: 'button',
            class: 'danger btn-sm',
            title: 'លុបសំណួរពីធនាគារ',
            onclick: (e) => { e.preventDefault(); e.stopPropagation(); deleteOne(x); }
          }, '🗑')
        : null;

      list.append(h('div', { class: 'bank-item', style: 'display:flex;gap:12px;align-items:flex-start;' }, [
        h('label', { style: 'display:flex;align-items:center;cursor:pointer;flex:none;' }, cb),
        h('div', { style: 'min-width:0;flex:1;' }, [
          mathEl('div', { class: 'bank-stem', style: 'cursor:pointer;line-height:1.6;', title: 'ចុចដើម្បីមើលសំណួរ និងចម្លើយ', onclick: () => openViewer(idx) }, x.stem_text),
          x.image_key ? h('div', { style: 'margin:8px 0;display:flex;align-items:center;gap:10px;flex-wrap:wrap;' }, [
            h('img', {
              src: '/api/images/' + encodeURIComponent(x.image_key),
              alt: x.image_key,
              loading: 'lazy',
              style: 'max-height:160px;max-width:260px;display:block;border-radius:6px;border:1px solid var(--line,#e2e8f0);background:#ffffff;padding:4px;object-fit:contain;cursor:pointer;',
              onclick: (e) => { e.preventDefault(); e.stopPropagation(); openViewer(idx); }
            }),
            h('div', { style: 'font-size:12px;color:#64748b;display:flex;flex-direction:column;gap:3px;' }, [
              h('span', { style: 'font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-weight:600;color:#0369a1;' }, x.image_key),
              h('button', {
                type: 'button',
                class: 'secondary btn-sm',
                style: 'padding:2px 8px;font-size:11px;width:fit-content;',
                onclick: (e) => {
                  e.preventDefault(); e.stopPropagation();
                  navigator.clipboard?.writeText(x.image_key);
                  Exam.notify(`បានចម្លងឈ្មោះរូប៖ ${x.image_key}`);
                }
              }, '📋 ចម្លងឈ្មោះរូប')
            ])
          ]) : null,
          h('div', { class: 'test-chips', style: 'margin-top:6px;display:flex;flex-wrap:wrap;gap:5px;align-items:center;' }, [
            h('span', { class: 'chip chip-plain', style: 'font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-weight:700;color:#1e40af;background:#eff6ff;border:1px solid #bfdbfe;' }, `#${x.id}`),
            x.kind === 'writing' ? h('span', { class: 'chip chip-soon' }, '✎ សរសេរ') : h('span', { class: 'chip chip-plain' }, 'ពហុជ្រើសរើស'),
            x.grade && S.grade === '' ? h('span', { class: 'chip chip-plain' }, GRADE_KH(x.grade)) : null,
            x.chapter && !(showLessons && S.chapter === x.chapter) ? h('span', { class: 'chip chip-plain', style: 'color:#047857;background:#ecfdf5;border:1px solid #a7f3d0;font-weight:600;' }, x.chapter) : null,
            x.lesson && !(showLessons && S.lesson === x.lesson) ? h('span', { class: 'chip chip-plain' }, x.lesson) : null,
            x.topic ? h('span', { class: 'chip chip-plain' }, x.topic) : null,
            x.level ? h('span', { class: `chip ${x.level === 'hard' ? 'chip-closed' : x.level === 'pisa' ? 'chip-soon' : 'chip-open'}` }, LEVEL_KH[x.level]) : null,
            x.image_key ? h('span', { class: 'chip chip-plain', style: 'color:#0369a1;background:#f0f9ff;border:1px solid #bae6fd;font-family:ui-monospace,SFMono-Regular,Consolas,monospace;', title: x.image_key }, `🖼 ${x.image_key}`) : null,
            h('span', { class: 'chip chip-plain' }, `${x.points} ពិន្ទុ`),
            h('span', { class: 'muted', style: 'font-size:12px;' }, x.test_title),
          ]),
        ]),
        h('div', { class: 'row', style: 'gap:6px;align-items:center;flex-shrink:0;' }, [
          viewBtn,
          editBtn,
          delBtn
        ]),
      ]));
    });
    const botPager = pager(); if (botPager) list.append(botPager);
    upd();
  }
  function upd() {
    const n = selected.size;
    const pts = questions.filter((q) => selected.has(q.id)).reduce((a, q) => a + (q.points || 1), 0);
    countLbl.textContent = String(n);
    ptsLbl.textContent = String(pts);
    addBtn.disabled = !n; tagBtn.disabled = !n; paperBtn.disabled = !n; clearBtn.disabled = !n; if (delSelBtn) delSelBtn.disabled = !n;
  }
  [fLevel, fKind, fTopic].forEach((el) => el && el.addEventListener('change', () => { page = 1; draw(); }));
  fQ.addEventListener('input', () => { page = 1; draw(); });

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
      h('div', { class: 'row', style: 'margin-top:10px;' }, [h('span', {}, 'ងាយ'), nEasy, h('span', {}, 'មធ្យម'), nMed, h('span', {}, 'ពិបាក'), nHard, h('span', {}, 'បែប PISA'), nPisa, kind]),
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
    h('div', { class: 'card' }, [h('div', { class: 'row' }, [h('h2', { style: 'margin:0;margin-right:auto;' }, showLessons ? (S.lesson && S.lesson !== '-' ? S.lesson : (S.chapter ? S.chapter : GRADE_KH(S.grade))) : 'សំណួរ'), newBtn, importBtn]),
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
      topic: String(pick(r, 'topic', 'ប្រធានបទ')).trim(), grade: String(pick(r, 'grade', 'ថ្នាក់')).replace(/\D/g, ''), chapter: String(pick(r, 'chapter', 'ជំពូក')).trim(), lesson: String(pick(r, 'lesson', 'មេរៀន')).trim(), level: levelOf(pick(r, 'level', 'កម្រិត')), solution_text: String(pick(r, 'solution', 'ចម្លើយគំរូ')).trim() };
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


// ---------- add more questions to an existing test, picked from the whole bank (any grade, any lesson) ----------
async function openBankPicker(test, onDone) {
  const [{ questions }, curr] = await Promise.all([api('/api/bank'), loadCurr()]);
  const have = new Set((test.questions || []).map((q) => String(q.stem_text || '').trim()));
  const pick = new Set();
  const F = { grade: '', lesson: '', level: '', kind: '', q: '' };
  const holder = h('div', {});
  const m = bankModal(`➕ ថែមសំណួរពីធនាគារ — ${test.title}`, holder, true);
  const gradeSel = h('select', { style: 'width:auto;' }, [h('option', { value: '' }, 'គ្រប់ថ្នាក់'), ...bankGradesOf(curr).map((g) => h('option', { value: g }, GRADE_KH(g)))]);
  const lessonSel = h('select', { style: 'width:auto;max-width:260px;' });
  const levelSel = h('select', { style: 'width:auto;' }, [['', 'គ្រប់កម្រិត'], ['easy', 'ងាយ'], ['medium', 'មធ្យម'], ['hard', 'ពិបាក'], ['pisa', 'បែប PISA']].map(([v, l]) => h('option', { value: v }, l)));
  const kindSel = h('select', { style: 'width:auto;' }, [['', 'គ្រប់ប្រភេទ'], ['mcq', 'ពហុជ្រើសរើស'], ['writing', 'សរសេរ']].map(([v, l]) => h('option', { value: v }, l)));
  const search = h('input', { type: 'text', placeholder: '🔍 ស្វែងរក…', style: 'max-width:180px;' });
  const list = h('div', { style: 'max-height:52vh;overflow:auto;margin-top:10px;display:flex;flex-direction:column;gap:6px;' });
  const info = h('b', {}, '0');
  const addBtn = h('button', { disabled: 'disabled', style: 'background:#16a34a;color:#fff;font-weight:600;' }, '➕ ថែមទៅតេស្ត');
  const fillLessons = () => {
    lessonSel.innerHTML = '';
    lessonSel.append(h('option', { value: '' }, 'គ្រប់មេរៀន'));
    const pool = gradeSel.value ? [gradeSel.value] : bankGradesOf(curr);
    const names = [...new Set(pool.flatMap((g) => (curr.lessons[g] || []).concat(questions.filter((q) => q.grade === g && q.lesson).map((q) => q.lesson))))];
    names.forEach((n) => lessonSel.append(h('option', { value: n }, n)));
  };
  const rows = () => {
    const t = search.value.trim().toLowerCase();
    return questions.filter((q) => (!gradeSel.value || q.grade === gradeSel.value) && (!lessonSel.value || q.lesson === lessonSel.value)
      && (!levelSel.value || q.level === levelSel.value) && (!kindSel.value || (kindSel.value === 'writing' ? q.kind === 'writing' : q.kind !== 'writing'))
      && (!t || String(q.stem_text).toLowerCase().includes(t)));
  };
  const status = () => {
    const pts = questions.filter((q) => pick.has(q.id)).reduce((a, q) => a + (q.points || 1), 0);
    info.textContent = `${khNum(pick.size)} សំណួរ · ${khNum(pts)} ពិន្ទុ`;
    addBtn.disabled = !pick.size;
  };
  const draw = () => {
    list.innerHTML = '';
    const r = rows();
    if (!r.length) list.append(h('p', { class: 'muted' }, 'មិនមានសំណួរតាមលក្ខខណ្ឌនេះទេ។'));
    r.slice(0, 150).forEach((q) => {
      const dup = have.has(String(q.stem_text || '').trim());
      const cb = h('input', { type: 'checkbox', style: 'width:20px;height:20px;flex:none;margin-top:3px;', checked: pick.has(q.id) ? 'checked' : null, disabled: dup ? 'disabled' : null,
        onchange: (e) => { e.target.checked ? pick.add(q.id) : pick.delete(q.id); status(); } });
      list.append(h('label', { style: `display:flex;gap:10px;align-items:flex-start;border:1px solid #e2e8f0;border-radius:10px;padding:8px 10px;${dup ? 'opacity:.5;' : 'cursor:pointer;'}` }, [
        cb,
        h('div', { style: 'flex:1;min-width:0;' }, [
          mathEl('div', { style: 'display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;line-height:1.5;' }, q.stem_text),
          h('div', { class: 'muted', style: 'font-size:12px;margin-top:2px;' }, [q.grade ? GRADE_KH(q.grade) : 'មិនទាន់កំណត់ថ្នាក់', q.lesson ? ` · ${q.lesson}` : '', q.level ? ` · ${LEVEL_KH[q.level] || q.level}` : '', ` · ${khNum(q.points || 1)} ពិន្ទុ`, dup ? ' · ✓ មានក្នុងតេស្តរួចហើយ' : ''].join('')),
        ]),
      ]));
    });
    if (r.length > 150) list.append(h('p', { class: 'muted' }, `បង្ហាញ ១៥០ ដំបូង ក្នុងចំណោម ${khNum(r.length)} — សូមត្រងបន្ថែម។`));
    status();
  };
  gradeSel.addEventListener('change', () => { fillLessons(); draw(); });
  [lessonSel, levelSel, kindSel].forEach((el) => el.addEventListener('change', draw));
  search.addEventListener('input', draw);
  addBtn.onclick = async () => {
    try {
      addBtn.disabled = true;
      const r = await api(`/api/tests/${test.id}/questions/copy`, { method: 'POST', body: { question_ids: [...pick] } });
      m.remove();
      await Exam.notify(r.copied < pick.size ? `⚠ បានថែម ${khNum(r.copied)} ក្នុងចំណោម ${khNum(pick.size)} សំណួរ (ដល់កម្រិតកំណត់នៃគម្រោង)។` : `✅ បានថែម ${khNum(r.copied)} សំណួរទៅតេស្ត។`);
      if (onDone) onDone();
    } catch (e) { addBtn.disabled = false; Exam.notify(e.message); }
  };
  fillLessons();
  holder.append(
    h('div', { class: 'row', style: 'gap:8px;flex-wrap:wrap;' }, [gradeSel, lessonSel, levelSel, kindSel, search]),
    list,
    h('div', { class: 'bp-foot' }, [
      h('div', { class: 'bp-count' }, ['បានជ្រើស ', info]),
      h('div', { class: 'bp-btns' }, [h('button', { class: 'secondary', onclick: () => m.remove() }, 'បោះបង់'), addBtn]),
    ]),
  );
  draw();
}
