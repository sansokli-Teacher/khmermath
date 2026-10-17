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

    // Question statistics
    const qstats = a.questions.filter((q) => !q.cancelled).map((q) => {
      const ok = rows.filter((r) => a.answers[r.id] && isRight(q, a.answers[r.id][q.id])).length;
      return { q, pct: n ? Math.round((ok / n) * 100) : 0 };
    }).sort((x, y) => x.pct - y.pct);

    // 1. Learning Gap Analysis by Lesson
    const lessons = {};
    for (const { q } of qstats) {
      const lName = q.lesson || (q.topic ? `ប្រធានបទ ៖ ${q.topic}` : 'ផ្សេងៗ');
      const l = (lessons[lName] ||= { name: lName, e: 0, p: 0, qCount: 0 });
      l.qCount++;
      for (const r of rows) {
        l.p += q.points;
        if (a.answers[r.id] && isRight(q, a.answers[r.id][q.id])) l.e += q.points;
      }
    }
    const lessonList = Object.values(lessons).map((l) => ({
      ...l,
      pct: l.p ? Math.round((l.e / l.p) * 100) : 0
    })).sort((x, y) => x.pct - y.pct);

    // 2. Cognitive Difficulty Levels Breakdown
    const LEVEL_MAP = { easy: 'ងាយ', medium: 'មធ្យម', hard: 'ពិបាក', pisa: 'បែប PISA' };
    const levels = {};
    for (const { q } of qstats) {
      const lvKey = q.level || 'other';
      const lvName = LEVEL_MAP[lvKey] || lvKey;
      const lv = (levels[lvKey] ||= { key: lvKey, name: lvName, e: 0, p: 0, qCount: 0 });
      lv.qCount++;
      for (const r of rows) {
        lv.p += q.points;
        if (a.answers[r.id] && isRight(q, a.answers[r.id][q.id])) lv.e += q.points;
      }
    }
    const levelList = ['easy', 'medium', 'hard', 'pisa'].filter((k) => levels[k]).map((k) => ({
      ...levels[k],
      pct: levels[k].p ? Math.round((levels[k].e / levels[k].p) * 100) : 0
    }));

    // Weak topics & students needing support
    const topics = {};
    for (const { q } of qstats) if (q.topic) for (const r of rows) { const t = (topics[q.topic] ||= { e: 0, p: 0 }); t.p += q.points; if (a.answers[r.id] && isRight(q, a.answers[r.id][q.id])) t.e += q.points; }
    const weak = Object.entries(topics).map(([name, t]) => ({ name, pct: t.p ? Math.round((t.e / t.p) * 100) : 0 })).sort((x, y) => x.pct - y.pct).filter((t) => t.pct < 65).slice(0, 5);
    const needHelp = rows.filter((r) => r.pct < 50);

    // Wire CSV export button
    const exportBtn = document.getElementById('btn-export-csv');
    if (exportBtn) {
      exportBtn.onclick = () => {
        const header = ['លំដាប់', 'អត្តលេខ', 'ត្រកូល', 'ឈ្មោះ', 'ពិន្ទុ_MCQ', 'ពិន្ទុ_Writing', 'ពិន្ទុ_សរុប', 'ភាគរយ', 'និទ្ទេស'];
        const csvLines = [header.join(',')];
        rows.forEach((r, idx) => {
          csvLines.push([
            idx + 1,
            `"${r.id}"`,
            `"${r.surname || ''}"`,
            `"${r.first_name || ''}"`,
            r.mcq_score ?? 0,
            r.writing_score != null ? r.writing_score : '',
            r.total,
            `${r.pct}%`,
            Exam.gradeOf(r.pct).grade
          ].join(','));
        });
        const blob = new Blob(['\uFEFF' + csvLines.join('\n')], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const aEl = document.createElement('a');
        aEl.href = url;
        aEl.download = `ពិន្ទុ_${s.class_name}_${s.test_title.replace(/[^a-zA-Z0-9ก-๛]/g, '_')}.csv`;
        aEl.click();
        URL.revokeObjectURL(url);
      };
    }

    document.title = `របាយការណ៍ថ្នាក់ — ${s.class_name}`;
    report.append(
      h('h1', { class: 'rp-title' }, 'របាយការណ៍លទ្ធផលថ្នាក់'),
      h('div', { class: 'rp-sub' }, `${s.test_title} · ថ្នាក់ ${s.class_name} · ${fmtDateTime(s.scheduled_start)}`),
      h('div', { class: 'rp-tiles' }, [
        h('div', { class: 'rp-tile' }, [h('b', {}, kh(n)), ` / ${kh(s.roster.length)} បានប្រឡង`]), h('div', { class: 'rp-tile' }, ['មធ្យម ', h('b', {}, `${kh(avg)}%`)]),
        h('div', { class: 'rp-tile' }, ['មេដ្យាន ', h('b', {}, `${kh(median)}%`)]), h('div', { class: 'rp-tile good' }, ['ខ្ពស់បំផុត ', h('b', {}, `${kh(sorted[n - 1] ?? 0)}%`)]),
        h('div', { class: 'rp-tile bad' }, ['ទាបបំផុត ', h('b', {}, `${kh(sorted[0] ?? 0)}%`)]), h('div', { class: 'rp-tile' }, ['ជាប់ (≥៥០%) ', h('b', {}, `${kh(n - needHelp.length)}`)]),
      ]),

      // Grade Distribution
      h('div', { class: 'rp-part' }, 'ការបែងចែកនិទ្ទេស'),
      ...Exam.GRADES.map((g) => { const c = Exam.gradeOf({ A: 90, B: 80, C: 70, D: 55, E: 45, F: 10 }[g]).color; return h('div', { class: 'rp-topic' }, [h('div', { style: 'width:30px;font-weight:700;' }, g), h('div', { class: 'bar', style: 'flex:1;' }, h('div', { class: 'bar-fill', style: `width:${(dist[g] / maxDist) * 100}%;background:${c};` })), h('div', { style: 'width:60px;text-align:right;font-weight:700;' }, `${kh(dist[g])} នាក់`)]); }),

      // 1. Learning Gap by Lesson
      h('div', { class: 'rp-part' }, ['📊 ការវិភាគគម្លាតចំណេះដឹងតាមមេរៀន (Learning Gap)', h('small', { style: 'margin-left:8px;' }, '— តម្រៀបតាមមេរៀនដែលសិស្សខ្សោយបំផុត')]),
      ...lessonList.map((l) => {
        const barColor = l.pct < 50 ? '#dc2626' : l.pct < 70 ? '#f59e0b' : '#16a34a';
        const statusLabel = l.pct < 50 ? 'ត្រូវពង្រឹង ⚠️' : l.pct < 70 ? 'មធ្យម' : 'ល្អ ✓';
        return h('div', { class: 'rp-topic', style: 'padding:8px 6px;align-items:center;' }, [
          h('div', { style: 'flex:1;min-width:0;font-weight:600;' }, [
            l.name,
            h('small', { class: 'muted', style: 'margin-left:8px;' }, `(${kh(l.qCount)} សំណួរ)`)
          ]),
          h('div', { class: 'bar', style: 'flex:1;max-width:180px;height:12px;background:#e2e8f0;border-radius:6px;overflow:hidden;margin:0 12px;' }, [
            h('div', { class: 'bar-fill', style: `width:${l.pct}%;background:${barColor};height:100%;` })
          ]),
          h('div', { style: `width:60px;text-align:right;font-weight:700;color:${barColor};` }, `${kh(l.pct)}%`),
          h('span', { class: `chip ${l.pct < 50 ? 'chip-closed' : l.pct < 70 ? 'chip-soon' : 'chip-open'}`, style: 'margin-left:8px;font-size:11px;' }, statusLabel)
        ]);
      }),

      // 2. Cognitive Difficulty Levels
      levelList.length ? h('div', {}, [
        h('div', { class: 'rp-part' }, '🧠 ការវិភាគតាមកម្រិតពិបាក (Cognitive Levels)'),
        ...levelList.map((lv) => {
          const barColor = lv.pct < 50 ? '#dc2626' : lv.pct < 70 ? '#f59e0b' : '#2563eb';
          return h('div', { class: 'rp-topic', style: 'align-items:center;' }, [
            h('div', { style: 'width:120px;font-weight:700;' }, lv.name),
            h('div', { class: 'bar', style: 'flex:1;height:12px;background:#e2e8f0;border-radius:6px;overflow:hidden;margin:0 12px;' }, [
              h('div', { class: 'bar-fill', style: `width:${lv.pct}%;background:${barColor};height:100%;` })
            ]),
            h('div', { style: `width:64px;text-align:right;font-weight:700;color:${barColor};` }, `${kh(lv.pct)}%`)
          ]);
        })
      ]) : null,

      // Hardest questions
      h('div', { class: 'rp-part' }, 'សំណួរដែលសិស្សឆ្លើយខុសច្រើនបំផុត'),
      ...qstats.slice(0, 5).map(({ q, pct }) => h('div', { class: 'rp-topic' }, [h('div', { style: 'width:36px;font-weight:700;' }, kh(q.order_no)), mathEl('div', { style: 'flex:1;min-width:0;' }, String(q.stem_text).slice(0, 110)), h('div', { style: 'width:64px;text-align:right;font-weight:700;color:#b42318;' }, `${kh(pct)}%`)])),

      // Pedagogical Insights
      (lessonList.some((l) => l.pct < 60) || needHelp.length) ? h('div', { style: 'margin:20px 0;padding:14px 18px;border-radius:12px;background:#fefce8;border:1.5px solid #fde047;' }, [
        h('b', { style: 'display:block;margin-bottom:8px;font-size:15px;color:#854d0e;' }, '💡 អនុសាសន៍គរុកោសល្យ និងសកម្មភាពពង្រឹង (Pedagogical Insights) ៖'),
        h('ul', { style: 'margin:0;padding-left:20px;line-height:1.7;color:#713f12;font-size:14px;' }, [
          lessonList.find((l) => l.pct < 60) ? h('li', {}, [
            'មេរៀនដែលត្រូវបង្រៀនពង្រឹងឡើងវិញជាបន្ទាន់ ៖ ',
            h('strong', {}, lessonList.filter((l) => l.pct < 60).map((l) => `${l.name} (${kh(l.pct)}%)`).join(' · '))
          ]) : null,
          needHelp.length ? h('li', {}, [
            `សិស្សដែលត្រូវការការយកចិត្តទុកដាក់ពិសេស (ពិន្ទុ < ៥០%) មាន ${kh(needHelp.length)} នាក់ ៖ `,
            h('span', { style: 'font-weight:600;' }, needHelp.map((r) => `${r.surname} ${r.first_name} (${kh(r.pct)}%)`).join(', '))
          ]) : h('li', {}, 'សិស្សទាំងអស់ប្រឡងជាប់ចាប់ពី ៥០% ឡើងទៅ។ ល្អណាស់!'),
        ].filter(Boolean))
      ]) : null,

      // Students table
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
