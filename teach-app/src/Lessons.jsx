import { useEffect, useState } from 'react';
import { kh, gradeOf, loadScript } from './api.js';

// Grade 7 lessons + their parts come from public/data/lessons_g7.json (built from the lesson sources).
// Lesson 1 has a hand-made deck; every other lesson gets a board with one slide per part to draw on.
function boardDeck(n, lesson) {
  const title = { k: 'title', html: `<p class="ts-kicker">ថ្នាក់ទី ៧ · មេរៀនទី ${kh(n)}</p><h1>${lesson.t}</h1><p class="ts-sub">${kh(lesson.p.length)} ផ្នែក</p>` };
  const parts = lesson.p.map((p, i) => ({ html: `<p class="ts-kicker">ផ្នែកទី ${kh(i + 1)}</p><h2>${p}</h2>` }));
  return [title, ...parts];
}

export default function Lessons({ cls, students, onBack }) {
  const grade = gradeOf(cls);
  const [data, setData] = useState(null);
  const [ready, setReady] = useState(false);
  const [pick, setPick] = useState(null);
  const [err, setErr] = useState('');

  useEffect(() => {
    let live = true;
    Promise.all([
      grade === '7' ? fetch('/data/lessons_g7.json?v=2').then((r) => r.json()) : Promise.resolve({}),
      Promise.all([loadScript('/katex/katex.min.js'), loadScript('/js/common.js')])
        .then(() => loadScript('/katex/contrib/auto-render.min.js'))
        .then(() => loadScript('/js/slides/g7l01.js?v=20261020h'))
        .then(() => loadScript('/js/teachshow.js?v=20261022e')),
    ]).then(([d]) => { if (live) { setData(d); setReady(true); } }).catch((e) => live && setErr(e.message));
    return () => { live = false; };
  }, [grade]);

  if (err) return <p className="alert">{err}</p>;
  if (!ready) return <div className="skeleton-grid">{[1, 2, 3, 4, 5, 6].map((n) => <div key={n} className="sk" />)}</div>;
  const nums = Object.keys(data).map(Number).sort((a, b) => a - b);
  if (!nums.length) return <div className="empty slim"><span>📖</span><p>មិនទាន់មានមេរៀនសម្រាប់ថ្នាក់ទី {kh(grade)} ទេ។</p></div>;

  const hasDeck = (n) => (grade === '7' && n > 1) || !!(window.TEACH_SLIDES && window.TEACH_SLIDES[`${grade}-${n}`]);
  const start = async (n, partIdx) => {
    const lesson = data[n];
    if (n > 1 && grade === '7') { try { await loadScript(`/js/slides/g7/lesson${n}.js?v=20261020h`); } catch { /* falls back to the part board */ } }
    const key = `${grade}-${n}`;
    window.TEACH_SLIDES = window.TEACH_SLIDES || {};
    const real = !!window.TEACH_SLIDES[key] && !window.TEACH_SLIDES[key].board;
    if (!window.TEACH_SLIDES[key]) { window.TEACH_SLIDES[key] = boardDeck(n, lesson); window.TEACH_SLIDES[key].board = true; }
    let startAt = 0;
    if (partIdx != null) {
      if (!real) startAt = partIdx + 1;
      else {
        const hit = window.TEACH_SLIDES[key].findIndex((s) => s.k === 'title' && s.html && s.html.includes(`<h1>`) && s.html.includes(lesson.p[partIdx]));
        startAt = hit > 0 ? hit : 0;
      }
    }
    window.TeachShow.open({ grade: Number(grade), lesson: n, title: lesson.t, className: cls.name, students, start: startAt });
  };

  if (pick) {
    const l = data[pick];
    return (
      <div className="lesson-detail">
        <button className="back" onClick={() => setPick(null)}>← មេរៀនទាំងអស់</button>
        <div className="ld-hero">
          <span className="lesson-n big">{kh(pick)}</span>
          <div><p className="kicker">មេរៀនទី {kh(pick)}</p><h3>{l.t}</h3><small>{kh(l.p.length)} ផ្នែក{hasDeck(pick) ? ' · មានស្លាយរួចរាល់' : ' · ក្តារសរសេរតាមផ្នែក'}</small></div>
          <button className="btn primary big" onClick={() => start(pick)}>▶ ចាប់ផ្តើមបង្រៀន</button>
        </div>
        <ol className="parts">
          {l.p.map((p, i) => (
            <li key={p}><button onClick={() => start(pick, i)}><span className="part-n">{kh(i + 1)}</span><b>{p}</b><span className="go" aria-hidden="true">▶</span></button></li>
          ))}
          {!l.p.length && <li className="none">មេរៀននេះមិនទាន់មានផ្នែកទេ។</li>}
        </ol>
      </div>
    );
  }

  return (
    <div className="lessons">
      <p className="lead">{kh(nums.length)} មេរៀន · ចុចមេរៀនដើម្បីមើលផ្នែក និងចាប់ផ្តើមបង្រៀន</p>
      <ul className="lesson-grid">
        {nums.map((n) => (
          <li key={n}>
            <button className={`lesson${hasDeck(n) ? ' ready' : ''}`} onClick={() => setPick(n)}>
              <span className="lesson-n">{kh(n)}</span>
              <span className="lesson-t"><b>{data[n].t}</b><small>{kh(data[n].p.length)} ផ្នែក{hasDeck(n) ? ' · មានស្លាយ' : ''}</small></span>
              <span className="lesson-go" aria-hidden="true">›</span>
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
