// Dashboard home (top of the classes tab): welcome banner, numbers, class cards with progress,
// a month calendar of exam dates and the latest tests. Uses only data the API already returns.
window.DashHome = (function () {
  const KH = (n) => String(n ?? '').replace(/\d/g, (d) => '០១២៣៤៥៦៧៨៩'[d]);
  const MONTHS = ['មករា', 'កុម្ភៈ', 'មីនា', 'មេសា', 'ឧសភា', 'មិថុនា', 'កក្កដា', 'សីហា', 'កញ្ញា', 'តុលា', 'វិច្ឆិកា', 'ធ្នូ'];
  const DAYS = ['អា', 'ច', 'អ', 'ពុ', 'ព្រ', 'សុ', 'ស'];
  const TINTS = [['#7a6df0', '#5a4bd6'], ['#d07a1c', '#b86400'], ['#e0506b', '#bf3050'], ['#1f9e83', '#0c7a63']];
  const ymd = (d) => `${d.getFullYear()}-${d.getMonth()}-${d.getDate()}`;

  async function build({ classes, ME, h, goTab, openClass }) {
    const [tr, sr] = await Promise.allSettled([Exam.api ? Exam.api('/api/tests') : fetch('/api/tests').then((r) => r.json()), Exam.api ? Exam.api('/api/sessions') : fetch('/api/sessions').then((r) => r.json())]);
    const tests = tr.status === 'fulfilled' ? (tr.value.tests || []) : [];
    const sessions = sr.status === 'fulfilled' ? (sr.value.sessions || []) : [];
    const open = sessions.filter((s) => s.phase === 'open').length;
    const upcoming = sessions.filter((s) => s.phase === 'upcoming').length;
    const students = classes.reduce((a, c) => a + (c.student_count || 0), 0);
    const ready = tests.filter((t) => t.status === 'ready').length;

    // ---- banner ----
    const name = (ME && (ME.display_name || ME.username)) || '';
    const sub = open || upcoming
      ? `ឥឡូវនេះមាន ${open} ការប្រឡងកំពុងដំណើរការ និង ${upcoming} ការប្រឡងនឹងមកដល់។`
      : 'ត្រៀមខ្លួនសម្រាប់មេរៀន និងការប្រឡងថ្មី — រៀបចំតេស្ត ហើយកំណត់ពេលប្រឡងឱ្យថ្នាក់របស់អ្នក។';
    const art = h('div', { class: 'hm-banner-art', 'aria-hidden': 'true' });
    art.innerHTML = '<svg viewBox="0 0 220 150"><g transform="rotate(-8 110 80)"><rect x="40" y="70" width="140" height="30" rx="6" fill="#4b55d6"/><rect x="46" y="76" width="128" height="18" rx="3" fill="#e9ecff"/><rect x="30" y="38" width="150" height="34" rx="6" fill="#ee4b3f"/><rect x="38" y="44" width="134" height="20" rx="3" fill="#fff3ef"/><path d="M130 38v26l7-6 7 6V38z" fill="#c92c24"/></g><circle cx="190" cy="30" r="14" fill="#fff" opacity=".18"/><circle cx="26" cy="120" r="9" fill="#fff" opacity=".18"/></svg>';
    const banner = h('section', { class: 'hm-banner' }, [
      h('div', { class: 'hm-banner-copy' }, [
        h('h2', {}, `សួស្តី ${name}! 👋`),
        h('p', {}, sub),
        h('button', { type: 'button', class: 'hm-cta', onclick: () => goTab(open || upcoming ? 'schedule' : 'tests') }, open || upcoming ? 'ទៅកាន់ការប្រឡង →' : 'ទៅកាន់តេស្ត →'),
      ]),
      art,
    ]);

    // ---- numbers ----
    const tile = (v, label, ico) => h('div', { class: 'hm-stat' }, [h('span', { class: 'hm-stat-ico', 'aria-hidden': 'true' }, ico), h('div', {}, [h('div', { class: 'stat-val' }, String(v)), h('div', { class: 'hm-stat-l' }, label)])]);
    const stats = h('div', { class: 'hm-stats' }, [
      tile(classes.length, 'ថ្នាក់', '🏫'), tile(students, 'សិស្សសរុប', '🧑‍🎓'), tile(ready, 'តេស្តរួចរាល់', '📝'), tile(open + upcoming, 'ការប្រឡងសកម្ម', '📅'),
    ]);

    // ---- class cards ----
    const cards = classes.map((c, i) => {
      const mine = sessions.filter((s) => s.class_id === c.id);
      const done = mine.filter((s) => s.phase === 'closed').length;
      const pct = mine.length ? Math.round((done / mine.length) * 100) : 0;
      const [a, b] = TINTS[i % TINTS.length];
      return h('button', { type: 'button', class: 'hm-class', style: `--a:${a};--b:${b}`, onclick: () => openClass(c) }, [
        h('div', { class: 'hm-class-top' }, [h('span', { class: 'hm-class-grade' }, KH(c.grade)), h('span', { class: 'hm-class-tag' }, `ថ្នាក់ទី ${KH(c.grade)}`)]),
        h('div', { class: 'hm-class-body' }, [
          h('b', {}, c.name),
          h('div', { class: 'hm-class-meta' }, [h('span', {}, `🧑‍🎓 ${c.student_count} នាក់`), h('span', {}, `📅 ${mine.length} ប្រឡង`)]),
          h('div', { class: 'hm-bar', role: 'progressbar', 'aria-valuenow': String(pct), 'aria-valuemin': '0', 'aria-valuemax': '100', 'aria-label': 'ការប្រឡងបានបញ្ចប់' }, [h('i', { style: `width:${pct}%` })]),
          h('div', { class: 'hm-class-foot' }, [h('span', {}, `បានបញ្ចប់ ${done}/${mine.length}`), h('span', {}, `${pct}%`)]),
        ]),
      ]);
    });
    const classSec = h('section', {}, [
      h('div', { class: 'hm-sec-h' }, [h('h3', {}, 'ថ្នាក់របស់ខ្ញុំ')]),
      classes.length ? h('div', { class: 'hm-classes' }, cards) : h('div', { class: 'hm-empty' }, 'មិនទាន់មានថ្នាក់ទេ — បង្កើតថ្នាក់ថ្មីខាងក្រោម។'),
    ]);

    // ---- calendar ----
    let cur = new Date(); cur.setDate(1);
    let picked = null;
    const days = new Map();
    sessions.forEach((s) => { const d = new Date(s.scheduled_start); const k = ymd(d); (days.get(k) || days.set(k, []).get(k)).push(s); });
    const calHead = h('div', { class: 'hm-cal-h' });
    const calGrid = h('div', { class: 'hm-cal-g' });
    const list = h('div', { class: 'hm-agenda' });
    const fmtT = (iso) => { const d = new Date(iso); return `${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`; };
    function drawList() {
      list.innerHTML = '';
      let rows;
      if (picked) rows = (days.get(picked) || []);
      else rows = sessions.filter((s) => s.phase !== 'closed').sort((x, y) => new Date(x.scheduled_start) - new Date(y.scheduled_start)).slice(0, 4);
      list.append(h('div', { class: 'hm-agenda-t' }, picked ? 'ការប្រឡងនៅថ្ងៃដែលបានជ្រើស' : 'ការប្រឡងនឹងមកដល់'));
      if (!rows.length) list.append(h('div', { class: 'hm-muted' }, picked ? 'គ្មានការប្រឡងនៅថ្ងៃនេះ។' : 'មិនទាន់មានការប្រឡងនឹងមកដល់។'));
      rows.forEach((s) => { const d = new Date(s.scheduled_start); list.append(h('button', { type: 'button', class: 'hm-ag', onclick: () => goTab('schedule') }, [
        h('span', { class: 'hm-ag-d' }, [h('b', {}, KH(d.getDate())), h('small', {}, MONTHS[d.getMonth()])]),
        h('span', { class: 'hm-ag-m' }, [h('b', {}, s.test_title), h('small', {}, `${s.class_name} · ${fmtT(s.scheduled_start)}`)]),
      ])); });
    }
    function drawCal() {
      calHead.innerHTML = ''; calGrid.innerHTML = '';
      calHead.append(
        h('button', { type: 'button', class: 'hm-nav', 'aria-label': 'ខែមុន', onclick: () => { cur.setMonth(cur.getMonth() - 1); drawCal(); } }, '‹'),
        h('b', {}, `${MONTHS[cur.getMonth()]} ${KH(cur.getFullYear())}`),
        h('button', { type: 'button', class: 'hm-nav', 'aria-label': 'ខែបន្ទាប់', onclick: () => { cur.setMonth(cur.getMonth() + 1); drawCal(); } }, '›'),
      );
      DAYS.forEach((d) => calGrid.append(h('span', { class: 'hm-dow' }, d)));
      const first = cur.getDay(), total = new Date(cur.getFullYear(), cur.getMonth() + 1, 0).getDate(), today = ymd(new Date());
      for (let i = 0; i < first; i++) calGrid.append(h('span', {}));
      for (let d = 1; d <= total; d++) {
        const k = `${cur.getFullYear()}-${cur.getMonth()}-${d}`;
        const n = (days.get(k) || []).length;
        calGrid.append(h('button', { type: 'button', class: `hm-day${k === today ? ' today' : ''}${k === picked ? ' on' : ''}${n ? ' has' : ''}`, 'aria-label': `${d} ${MONTHS[cur.getMonth()]}${n ? ` — ${n} ការប្រឡង` : ''}`, onclick: () => { picked = picked === k ? null : k; drawCal(); drawList(); } }, KH(d)));
      }
    }
    drawCal(); drawList();
    const calCard = h('section', { class: 'hm-card' }, [calHead, calGrid, list]);

    // ---- recent tests ----
    const recent = tests.slice(0, 4).map((t) => {
      const ss = sessions.filter((s) => s.test_id === t.id).sort((x, y) => new Date(y.scheduled_start) - new Date(x.scheduled_start));
      const s = ss[0];
      const pct = s && s.total_students ? Math.round((s.submitted_count / s.total_students) * 100) : 0;
      return h('button', { type: 'button', class: 'hm-test', onclick: () => goTab('tests') }, [
        h('div', { class: 'hm-test-t' }, [h('b', {}, t.title), h('span', { 'aria-hidden': 'true' }, '↗')]),
        h('small', {}, s ? `${s.class_name} · ប្រគល់ ${s.submitted_count}/${s.total_students || 0}` : `${t.question_count} សំណួរ · មិនទាន់ប្រឡង`),
        h('div', { class: 'hm-bar sm' }, [h('i', { style: `width:${pct}%` })]),
        h('span', { class: 'hm-pct' }, `${pct}%`),
      ]);
    });
    const testCard = h('section', { class: 'hm-card' }, [
      h('div', { class: 'hm-sec-h' }, [h('h3', {}, 'តេស្តថ្មីៗ'), h('button', { type: 'button', class: 'hm-link', onclick: () => goTab('tests') }, 'មើលទាំងអស់')]),
      recent.length ? h('div', { class: 'hm-tests' }, recent) : h('div', { class: 'hm-muted' }, 'មិនទាន់មានតេស្តទេ។'),
    ]);

    return h('div', { class: 'hm-grid' }, [h('div', { class: 'hm-main' }, [banner, stats, classSec]), h('aside', { class: 'hm-side' }, [calCard, testCard])]);
  }
  return { build };
})();
