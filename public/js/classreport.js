// One printable page per exam session: how the class did, where it was weak, and every student's score.
const { h, api, fmtDateTime } = Exam;
const SESSION = new URLSearchParams(location.search).get('session');
const KH = '០១២៣៤៥៦៧៨៩';
const kh = (n) => String(n).replace(/\d/g, (d) => KH[d]);
const isRight = (q, v) => (q.cancelled ? true : v != null && (v === q.correct_index || (q.alt_correct_index != null && v === q.alt_correct_index)));
const mathEl = (tag, attrs, text) => { const el = h(tag, attrs); el.innerHTML = Exam.mathHtml(text); return el; };

(async () => {
  const report = document.getElementById('report');
  try {
    const [s, a] = await Promise.all([api(`/api/sessions/${SESSION}`), api(`/api/sessions/${SESSION}/analysis`)]);
    const rows = s.roster.filter((r) => r.submitted_at).map((r) => {
      const total = (r.mcq_score ?? 0) + (r.writing_score ?? 0), max = s.mcq_max + (r.writing_max ?? 0);
      return { ...r, total, max, pct: max ? Math.round((total / max) * 100) : 0 };
    }).sort((x, y) => y.pct - x.pct);
    const n = rows.length, pcts = rows.map((r) => r.pct);
    const avg = n ? Math.round(pcts.reduce((x, y) => x + y, 0) / n) : 0;
    const sorted = [...pcts].sort((x, y) => x - y);
    const median = n ? (n % 2 ? sorted[(n - 1) / 2] : Math.round((sorted[n / 2 - 1] + sorted[n / 2]) / 2)) : 0;
    const dist = Object.fromEntries(Exam.GRADES.map((g) => [g, 0]));
    for (const r of rows) dist[Exam.gradeOf(r.pct).grade]++;
    const maxDist = Math.max(1, ...Object.values(dist));
    const qstats = a.questions.filter((q) => !q.cancelled).map((q) => {
      const ok = rows.filter((r) => a.answers[r.id] && isRight(q, a.answers[r.id][q.id])).length;
      return { q, pct: n ? Math.round((ok / n) * 100) : 0 };
    }).sort((x, y) => x.pct - y.pct);
    const topics = {};
    for (const { q } of qstats) if (q.topic) for (const r of rows) { const t = (topics[q.topic] ||= { e: 0, p: 0 }); t.p += q.points; if (a.answers[r.id] && isRight(q, a.answers[r.id][q.id])) t.e += q.points; }
    const weak = Object.entries(topics).map(([name, t]) => ({ name, pct: t.p ? Math.round((t.e / t.p) * 100) : 0 })).sort((x, y) => x.pct - y.pct).filter((t) => t.pct < 65).slice(0, 5);
    const needHelp = rows.filter((r) => r.pct < 50);

    document.title = `របាយការណ៍ថ្នាក់ — ${s.class_name}`;
    report.append(
      h('h1', { class: 'rp-title' }, 'របាយការណ៍លទ្ធផលថ្នាក់'),
      h('div', { class: 'rp-sub' }, `${s.test_title} · ថ្នាក់ ${s.class_name} · ${fmtDateTime(s.scheduled_start)}`),
      h('div', { class: 'rp-tiles' }, [
        h('div', { class: 'rp-tile' }, [h('b', {}, kh(n)), ` / ${kh(s.roster.length)} បានប្រឡង`]), h('div', { class: 'rp-tile' }, ['មធ្យម ', h('b', {}, `${kh(avg)}%`)]),
        h('div', { class: 'rp-tile' }, ['មេដ្យាន ', h('b', {}, `${kh(median)}%`)]), h('div', { class: 'rp-tile good' }, ['ខ្ពស់បំផុត ', h('b', {}, `${kh(sorted[n - 1] ?? 0)}%`)]),
        h('div', { class: 'rp-tile bad' }, ['ទាបបំផុត ', h('b', {}, `${kh(sorted[0] ?? 0)}%`)]), h('div', { class: 'rp-tile' }, ['ជាប់ (≥៥០%) ', h('b', {}, `${kh(n - needHelp.length)}`)]),
      ]),
      h('div', { class: 'rp-part' }, 'ការបែងចែកនិទ្ទេស'),
      ...Exam.GRADES.map((g) => { const c = Exam.gradeOf({ A: 90, B: 80, C: 70, D: 55, E: 45, F: 10 }[g]).color; return h('div', { class: 'rp-topic' }, [h('div', { style: 'width:30px;font-weight:700;' }, g), h('div', { class: 'bar', style: 'flex:1;' }, h('div', { class: 'bar-fill', style: `width:${(dist[g] / maxDist) * 100}%;background:${c};` })), h('div', { style: 'width:60px;text-align:right;font-weight:700;' }, `${kh(dist[g])} នាក់`)]); }),
      h('div', { class: 'rp-part' }, 'សំណួរដែលសិស្សឆ្លើយខុសច្រើនបំផុត'),
      ...qstats.slice(0, 5).map(({ q, pct }) => h('div', { class: 'rp-topic' }, [h('div', { style: 'width:36px;font-weight:700;' }, kh(q.order_no)), mathEl('div', { style: 'flex:1;min-width:0;' }, String(q.stem_text).slice(0, 110)), h('div', { style: 'width:64px;text-align:right;font-weight:700;color:#b42318;' }, `${kh(pct)}%`)])),
      weak.length ? h('div', {}, [h('div', { class: 'rp-part' }, 'ប្រធានបទដែលត្រូវពន្យល់ឡើងវិញ'), ...weak.map((t) => h('div', { class: 'rp-topic' }, [h('div', { style: 'flex:1;' }, t.name), h('div', { style: 'font-weight:700;color:#b42318;' }, `${kh(t.pct)}%`)]))]) : null,
      h('div', { class: 'rp-part' }, 'ពិន្ទុសិស្សម្នាក់ៗ'),
      h('table', {}, [
        h('thead', {}, h('tr', {}, ['លំដាប់', 'អត្តលេខ', 'ឈ្មោះ', 'ក', 'ខ', 'សរុប', '%', 'និទ្ទេស'].map((t) => h('th', {}, t)))),
        h('tbody', {}, rows.map((r, i) => h('tr', { style: r.pct < 50 ? 'background:#fdecec;' : '' }, [h('td', {}, kh(i + 1)), h('td', {}, r.id), h('td', {}, `${r.surname} ${r.first_name}`), h('td', {}, `${r.mcq_score}/${s.mcq_max}`), h('td', {}, r.writing_score != null ? `${r.writing_score}/${r.writing_max}` : '—'), h('td', {}, `${r.total}/${r.max}`), h('td', {}, `${r.pct}%`), h('td', {}, Exam.gradeOf(r.pct).grade)]))),
      ]),
      s.roster.length - n ? h('p', { class: 'muted' }, `អវត្តមាន / មិនបានប្រគល់៖ ${s.roster.filter((r) => !r.submitted_at).map((r) => `${r.surname} ${r.first_name}`).join(' · ')}`) : null,
      h('div', { class: 'rp-foot' }, 'បង្កើតដោយប្រព័ន្ធប្រឡង exam.khmermath.org'),
    );
  } catch (e) { report.append(h('div', { class: 'error' }, e.status === 401 ? 'សូមចូលជាគ្រូជាមុនសិន។' : e.message)); }
})();
