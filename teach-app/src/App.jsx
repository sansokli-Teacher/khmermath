import { useEffect, useState } from 'react';

const reduced = () => window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
import { api, kh, gradeOf } from './api.js';
import Attendance from './Attendance.jsx';
import Lessons from './Lessons.jsx';
import Wheel from './Wheel.jsx';
import Modal from './Modal.jsx';
import Clock from './Clock.jsx';
import GameWizard from './GameWizard.jsx';
import QuestionBank from './QuestionBank.jsx';

const HUES = { 7: ['#2a6df0', '#5b3fe0'], 8: ['#0e9f8a', '#1565c0'], 9: ['#e8590c', '#c2255c'], 10: ['#7048e8', '#ae3ec9'], 11: ['#f08c00', '#e8590c'], 12: ['#d6336c', '#862e9c'] };
const hue = (c) => HUES[parseInt(gradeOf(c), 10)] || HUES[7];

export default function App() {
  const [me, setMe] = useState(null);
  const [classes, setClasses] = useState(null);
  const [sheet, setSheet] = useState(null); // class whose actions are open
  const [view, setView] = useState(null); // { type: 'att' | 'lessons' | 'wheel', cls }
  const [wizard, setWizard] = useState(null); // { cls? } while the game wizard is open
  const [activeId, setActiveId] = useState(() => { try { return localStorage.getItem('teach_active_class'); } catch { return null; } });   // the class the teacher is working with: the game uses it, so it is not asked again
  const remember = (c) => { setActiveId(String(c.id)); try { localStorage.setItem('teach_active_class', String(c.id)); } catch { /* storage blocked */ } };
  const [bankOpen, setBankOpen] = useState(false);
  const [students, setStudents] = useState([]);
  const [error, setError] = useState('');
  const [fs, setFs] = useState(!!document.fullscreenElement);
  const [anim, setAnim] = useState(() => (reduced() ? '' : 'vanish-in'));

  // Leave teaching mode: vanish out, then go back to the dashboard (which vanishes in).
  const leave = (e) => {
    e.preventDefault();
    const href = e.currentTarget.href;
    try { sessionStorage.setItem('km_vanish', '1'); } catch { /* storage blocked */ }
    if (reduced()) { location.href = href; return; }
    setAnim('vanish-out');
    setTimeout(() => { location.href = href; }, 800);
  };

  useEffect(() => {
    (async () => {
      try {
        const who = await api('/api/teacher/me');
        setMe(who);
        if (!who.teach_allowed) { setError('ម៉ូដបង្រៀនមិនទាន់បើកសម្រាប់គណនីរបស់អ្នកទេ។ សូមទាក់ទងម្ចាស់ប្រព័ន្ធ។'); return; }
        const list = (await api('/api/classes')).classes;
        setClasses(list);
        if (new URLSearchParams(location.search).get('back') === 'game') {                 // coming back from the game: open the same class again
          let id = null; try { id = localStorage.getItem('teach_active_class'); } catch { /* storage blocked */ }
          const c = list.find((x) => String(x.id) === String(id));
          if (c) setSheet(c);
          history.replaceState(null, '', location.pathname);
        }
      } catch (e) {
        if (e.status === 401) location.href = '/teacher';
        else setError(e.message);
      }
    })();
    const onFs = () => setFs(!!document.fullscreenElement);
    document.addEventListener('fullscreenchange', onFs);
    return () => document.removeEventListener('fullscreenchange', onFs);
  }, []);

  useEffect(() => {
    if (!view) return undefined;
    let live = true;
    setStudents([]);
    api(`/api/classes/${view.cls.id}/students`).then((d) => { if (live) setStudents(d.students || []); }).catch((e) => setError(e.message));
    return () => { live = false; };
  }, [view && view.cls.id]); // eslint-disable-line react-hooks/exhaustive-deps

  const toggleFs = () => (document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen().catch(() => {}));

  if (error) return <div className="boot"><p>{error}</p><a className="btn ghost" href="/teacher?classic=1">← ត្រឡប់ទៅផ្ទាំងគ្រូ</a></div>;
  if (!classes) return <div className="boot"><div className="spinner" /><p>កំពុងផ្ទុក…</p></div>;
  const hello = me && (me.display_name || me.username);
  const activeClass = classes.find((c) => String(c.id) === String(activeId)) || undefined;

  return (
    <div className={`home ${anim}`} onAnimationEnd={(e) => { if (e.target === e.currentTarget) setAnim((a) => (a === 'vanish-out' ? a : '')); }}>
      <header className="top">
        <a className="brand" href="/teacher?classic=1" title="ចេញពីម៉ូដបង្រៀន" onClick={leave}>
          <span className="brand-mark">∑</span>
          <span className="brand-t"><b>KhmerMath</b><small>ម៉ូដបង្រៀន</small></span>
        </a>
        <Clock compact />
        <div className="top-r">
          <button className="icon-btn" onClick={toggleFs} aria-label="ពេញអេក្រង់" title="ពេញអេក្រង់">{fs ? '🗗' : '⛶'}</button>
          <a className="icon-btn txt" href="/teacher?classic=1" onClick={leave}>ចាកចេញ</a>
        </div>
      </header>

      <main className="wrap">
        <section>
          <div className="sec-hd"><h1>សួស្តី {hello} 👋</h1><p>ជ្រើសថ្នាក់ដើម្បីចាប់ផ្តើមបង្រៀន</p></div>
          {classes.length ? (
            <ul className="class-grid">
              {classes.map((c, i) => (
                <li key={c.id} style={{ '--i': i }}>
                  <button className="class-card" style={{ '--a': hue(c)[0], '--b': hue(c)[1] }} onClick={() => { remember(c); setSheet(c); }}>
                    <span className="cc-g">ទី {kh(gradeOf(c))}</span>
                    <span className="cc-go" aria-hidden="true">›</span>
                    <b className="cc-n">{c.name}</b>
                    <span className="cc-c">👥 {kh(c.student_count)} សិស្ស</span>
                  </button>
                </li>
              ))}
            </ul>
          ) : (
            <div className="empty slim"><span>🏫</span><p>មិនទាន់មានថ្នាក់ទេ។ សូមបង្កើតថ្នាក់នៅផ្ទាំងគ្រូសិន។</p><a className="btn primary" href="/teacher?classic=1">ទៅបង្កើតថ្នាក់</a></div>
          )}
        </section>

        <section>
          <div className="sec-hd"><h2>🎮 ម៉ូដហ្គេម</h2><p>លេងជាក្រុមជាមួយសិស្សក្នុងថ្នាក់</p></div>
          <ul className="game-row">
            <li style={{ '--i': 0 }}>
              <button className="tool t-cards" disabled={!classes.length} onClick={() => setWizard({ cls: activeClass })}>
                <span className="tool-ic" aria-hidden="true">🎮</span><b>លេងហ្គេម</b><small>{activeClass ? `ថ្នាក់ ${activeClass.name} · មេរៀន ហ្គេម ក្រុម` : 'ជ្រើសថ្នាក់ មេរៀន ហ្គេម ក្រុម'}</small>
              </button>
            </li>
            <li style={{ '--i': 1 }}>
              <button className="tool t-qwheel" onClick={() => setBankOpen(true)}>
                <span className="tool-ic" aria-hidden="true">📚</span><b>សំណួរហ្គេម</b><small>មើលបញ្ជី កែ ឬលុបសំណួរ</small>
              </button>
            </li>
          </ul>
        </section>
      </main>

      {sheet && !view && (
        <Modal title={`ថ្នាក់ ${sheet.name}`} sub={`ថ្នាក់ទី ${kh(gradeOf(sheet))} · ${kh(sheet.student_count)} សិស្ស`} onClose={() => setSheet(null)}>
          <div className="act-row">
            <button className="act att" onClick={() => setView({ type: 'att', cls: sheet })}><span>✋</span><b>វត្តមាន</b><small>ចុះឈ្មោះសិស្សថ្ងៃនេះ</small></button>
            <button className="act les" onClick={() => setView({ type: 'lessons', cls: sheet })}><span>📖</span><b>ស្លាយមេរៀន</b><small>ជ្រើសមេរៀន និងផ្នែក</small></button>
            <button className="act game" onClick={() => { const c = sheet; remember(c); setSheet(null); setWizard({ cls: c }); }}><span>🎮</span><b>ហ្គេម</b><small>លេងជាក្រុមជាមួយមេរៀន</small></button>
            <button className="act spin" onClick={() => setView({ type: 'wheel', cls: sheet })}><span>🎡</span><b>កង់ចាប់ឈ្មោះ</b><small>ចាប់ឈ្មោះ ឬបែងចែកក្រុម</small></button>
          </div>
        </Modal>
      )}

      {view && view.type === 'att' && (
        <Modal title={`វត្តមាន · ${view.cls.name}`} onClose={() => setView(null)} wide>
          <Attendance cls={view.cls} students={students} />
        </Modal>
      )}
      {view && view.type === 'lessons' && (
        <Modal title={`ស្លាយមេរៀន · ${view.cls.name}`} sub={`ថ្នាក់ទី ${kh(gradeOf(view.cls))}`} onClose={() => setView(null)} wide>
          <Lessons cls={view.cls} students={students} />
        </Modal>
      )}
      {view && view.type === 'wheel' && (
        <div className="screen">
          <header className="screen-hd"><button className="back" onClick={() => setView(null)}>← {view.cls.name}</button><h2>🎡 កង់ចាប់ឈ្មោះ</h2></header>
          <Wheel cls={view.cls} students={students} />
        </div>
      )}

      {bankOpen && <QuestionBank onClose={() => setBankOpen(false)} />}
      {wizard && <GameWizard classes={classes} cls={wizard.cls} onClose={() => setWizard(null)} />}
    </div>
  );
}
