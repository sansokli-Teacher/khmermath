// Teaching-mode class room: attendance (OK / A / L) + lesson slides.
(function () {
  const { h, api } = Exam;
  const kh = (n) => String(n ?? '').replace(/\d/g, (d) => '០១២៣៤៥៦៧៨៩'[d]);
  const today = () => {
    const d = new Date();
    const p = (n) => String(n).padStart(2, '0');
    return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}`;
  };

  let roomOn = false;
  let cls = null;
  let hostEl = null;
  let day = today();
  let period = 1;
  let students = [];
  let rows = {};
  let saved = {};
  let dirty = false;
  let loading = false;
  let job = 0;
  let errText = '';

  const keyOf = (id) => {
    const k = String(id);
    return rows[k] || (rows[k] = { mark: 'ok', note: '' });
  };
  const snap = () => JSON.stringify(students.map((s) => { const r = keyOf(s.id); return [s.id, r.mark, r.note]; }));
  const isDirty = () => snap() !== saved;

  async function loadMarks() {
    loading = true;
    errText = '';
    try {
      const data = await api(`/api/attendance?class_id=${encodeURIComponent(cls.id)}&day=${day}&period=${period}`);
      rows = {};
      for (const r of data.rows || []) rows[String(r.student_id)] = { mark: r.mark || 'ok', note: r.note || '' };
      students.forEach((s) => keyOf(s.id));
      saved = snap();
      dirty = false;
    } catch (e) {
      errText = e.message || 'មិនអាចផ្ទុកវត្តមានបានទេ។';
    }
    loading = false;
  }

  function paintMarks(list) {
    list.querySelectorAll('[data-sid]').forEach((el) => {
      const r = keyOf(el.dataset.sid);
      el.querySelectorAll('[data-m]').forEach((b) => b.classList.toggle('on', b.dataset.m === r.mark));
    });
  }

  function attList() {
    const box = h('div', { class: 'att-list' });
    students.forEach((s, i) => {
      const r = keyOf(s.id);
      const note = h('input', { type: 'text', class: 'att-note', placeholder: 'កំណត់ចំណាំ…', value: r.note, maxlength: '400' });
      note.value = r.note;
      note.oninput = () => { r.note = note.value; dirty = isDirty(); saveBtnState(); };
      const btns = ['ok', 'A', 'L'].map((m) => h('button', {
        type: 'button',
        class: `att-m att-${m}${r.mark === m ? ' on' : ''}`,
        'data-m': m,
        onclick: () => {
          r.mark = m;
          row.querySelectorAll('[data-m]').forEach((b) => b.classList.toggle('on', b.dataset.m === m));
          dirty = isDirty();
          saveBtnState();
        },
      }, m === 'ok' ? 'OK' : m));
      const row = h('div', { class: 'att-row', 'data-sid': s.id }, [
        h('span', { class: 'att-n' }, kh(i + 1)),
        h('div', { class: 'att-who' }, [
          h('b', {}, `${s.surname || ''} ${s.first_name || ''}`.trim()),
          h('span', { class: 'muted' }, s.id),
        ]),
        h('div', { class: 'att-marks' }, btns),
        note,
      ]);
      box.append(row);
    });
    return box;
  }

  let saveBtn;
  function saveBtnState() {
    if (!saveBtn) return;
    saveBtn.disabled = loading;
    saveBtn.textContent = dirty ? 'ចុះវត្តមាន' : 'រក្សាទុកវត្តមាន';
  }

  async function submitAtt() {
    saveBtn.disabled = true;
    try {
      await api('/api/attendance', {
        method: 'POST',
        body: {
          class_id: cls.id,
          day,
          period,
          rows: students.map((s) => ({ student_id: String(s.id), mark: keyOf(s.id).mark, note: keyOf(s.id).note })),
        },
      });
      saved = snap();
      dirty = false;
      Exam.notify('បានចុះវត្តមាន។');
    } catch (e) { Exam.notify(e.message); }
    saveBtnState();
  }

  function gradeKey(c) {
    const raw = String((c && c.grade) || '').trim();
    const digits = raw.replace(/[០១២៣៤៥៦៧៨៩]/g, (d) => String('០១២៣៤៥៦៧៨៩'.indexOf(d))).replace(/\D/g, '');
    return digits || raw;
  }

  function openSlides(grade, lesson, title) {
    const key = `${grade}-${lesson}`;
    const slides = window.TEACH_SLIDES && window.TEACH_SLIDES[key];
    if (!window.TeachShow || !slides || !slides.length) {
      Exam.notify('មិនទាន់មានស្លាយសម្រាប់មេរៀននេះទេ។');
      return;
    }
    window.TeachShow.open({
      grade,
      lesson,
      title,
      className: cls.name,
      students,
    });
  }

  function lessonCard() {
    const grade = gradeKey(cls);
    const lessons = (window.TEACH_LESSONS && window.TEACH_LESSONS[grade]) || [];
    const readyKey = window.TEACH_SLIDES && window.TEACH_SLIDES[`${grade}-1`] ? `${grade}-1` : (window.TEACH_SLIDES && window.TEACH_SLIDES['7-1'] ? '7-1' : '');
    const [g, n] = readyKey ? readyKey.split('-') : ['7', '1'];
    const title = (window.TEACH_LESSONS && window.TEACH_LESSONS[g] && window.TEACH_LESSONS[g][Number(n) - 1]) || 'ចំនួនគត់';
    const openMain = h('button', {
      type: 'button',
      class: 'slide-open',
      onclick: () => openSlides(Number(g), Number(n), title),
    }, [
      h('span', { class: 'slide-open-k' }, 'PowerPoint'),
      h('b', {}, 'បើកស្លាយ'),
      h('span', {}, `${title} · មេរៀនទី ${kh(n)}`),
    ]);
    const rest = lessons.length ? lessons.map((name, i) => {
      const key = `${grade}-${i + 1}`;
      const ready = !!(window.TEACH_SLIDES && window.TEACH_SLIDES[key]);
      return h('button', {
        type: 'button',
        class: `teach-lesson${ready ? '' : ' off'}`,
        onclick: () => openSlides(Number(grade) || 7, i + 1, name),
      }, [
        h('span', { class: 'teach-lesson-n' }, `មេរៀនទី ${kh(i + 1)}`),
        h('b', {}, name),
        h('span', { class: 'muted' }, ready ? 'ចុចបើកស្លាយ' : 'មេរៀននេះមិនទាន់មានស្លាយ'),
      ]);
    }) : [h('p', { class: 'muted' }, 'ស្លាយដែលបើកបានឥឡូវគឺមេរៀនចំនួនគត់ ថ្នាក់ទី ៧។')];
    return h('section', { class: 'desk-card desk-slides' }, [
      h('div', { class: 'desk-hd' }, [h('h3', {}, 'ស្លាយមេរៀន'), h('span', {}, 'ប៊ិច · កង់ · ម៉ោង · ម៉ាស៊ីនគិត')]),
      openMain,
      h('div', { class: 'teach-lessons' }, rest),
    ]);
  }

  function paint() {
    const host = hostEl || document.getElementById('teach-work');
    if (!host || !cls) return;
    host.innerHTML = '';
    const dayIn = h('input', { type: 'date', value: day });
    dayIn.onchange = async () => { day = dayIn.value || today(); await loadMarks(); paint(); };
    const periods = h('div', { class: 'att-periods' }, Array.from({ length: 8 }, (_, i) => {
      const n = i + 1;
      return h('button', {
        type: 'button',
        class: `att-period${n === period ? ' on' : ''}`,
        onclick: async () => { period = n; await loadMarks(); paint(); },
      }, kh(n));
    }));
    saveBtn = h('button', { type: 'button', class: 'att-save', onclick: submitAtt }, 'ចុះវត្តមាន');
    const att = h('section', { class: 'desk-card desk-att' }, [
      h('div', { class: 'desk-hd' }, [
        h('h3', {}, 'វត្តមាន'),
        h('span', {}, `${kh(students.length)} សិស្ស`),
      ]),
      h('div', { class: 'att-bar' }, [
        h('label', {}, ['ថ្ងៃ', dayIn]),
        h('div', { class: 'att-period-wrap' }, [h('span', { class: 'att-period-lab' }, 'ម៉ោង'), periods]),
      ]),
      h('p', { class: 'att-hint' }, 'OK មានវត្តមាន · A អវត្តមាន · L យឺត។ ប្តូរសញ្ញារួចចុច «ចុះវត្តមាន»។'),
      errText ? h('p', { class: 'att-err' }, errText) : null,
      students.length ? attList() : h('p', { class: 'att-empty' }, 'ថ្នាក់នេះមិនទាន់មានសិស្សទេ។'),
      h('div', { class: 'att-foot' }, saveBtn),
    ]);
    host.append(att, lessonCard());
    saveBtnState();
    const title = document.getElementById('workspace-title');
    if (title) title.textContent = cls.name;
    const now = document.getElementById('teach-now-name');
    if (now) now.textContent = cls.name;
    const meta = document.getElementById('teach-now-meta');
    if (meta) meta.textContent = `ថ្នាក់ទី ${kh(cls.grade)} · សិស្ស ${kh(students.length)} នាក់`;
  }

  async function mount(c, host) {
    if (!c) return;
    const n = ++job;
    const switched = !cls || String(cls.id) !== String(c.id);
    cls = c;
    roomOn = true;
    hostEl = host || document.getElementById('teach-work') || hostEl;
    if (hostEl) hostEl.innerHTML = '<p class="teach-loading">កំពុងផ្ទុកវត្តមាន និងស្លាយ…</p>';
    if (switched) { day = today(); period = 1; rows = {}; students = []; }
    try {
      students = (await api(`/api/classes/${c.id}/students`)).students || [];
    } catch (e) {
      students = [];
      errText = e.message || 'មិនអាចផ្ទុកបញ្ជីសិស្សបានទេ។';
    }
    if (n !== job) return;
    await loadMarks();
    if (n !== job) return;
    paint();
  }

  async function open(c) { return mount(c); }

  function close() {
    roomOn = false;
    cls = null;
  }

  window.TeachRoom = {
    open,
    mount,
    close,
    isOpen: () => roomOn,
    class: () => cls,
    students: () => students,
  };
})();
