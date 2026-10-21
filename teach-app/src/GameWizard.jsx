import { useEffect, useMemo, useState } from 'react';
import { api, kh, gradeOf, fullName } from './api.js';
import Modal from './Modal.jsx';
import QuestionBank from './QuestionBank.jsx';
import DealPopup from './DealPopup.jsx';

// «ហ្គេម» in teaching mode: class → lesson → game style → teams → ▶ Start.
// The lesson defaults to the one last taught in that class; absent students (crossed out in the Spin) stay out of the teams.
const STYLES = [
  { k: 'cards', ic: '🃏', t: 'កាតបើក', d: 'ក្រុមផ្លាស់វេនជ្រើសប្រអប់លេខ', img: '/img/play/teamgame.jpg' },
  { k: 'wheel', ic: '🎡', t: 'កង់វិល', d: 'បង្វិលកង់ ហើយកង់ជ្រើសសំណួរឱ្យ', img: '/img/play/wheel.jpg' },
  { k: 'boat', ic: '🚣', t: 'ប្រណាំងទូកង', d: 'ឆ្លើយត្រូវ ទូកទៅមុខ', img: '/img/play/boat.jpg' },
];
const OTHERS = [
  { k: 'live', ic: '📱', t: 'សំណួរផ្ទាល់', d: 'សិស្សឆ្លើយលើទូរស័ព្ទ', href: (c) => `/teacher?classic=1&tool=live&class=${c.id}` },
  { k: 'bingo', ic: '🎯', t: 'ប៊ីងហ្គោ', d: 'បោះពុម្ពកាតចម្លើយ', href: () => '/bingo.html' },
];
const QN = [5, 10, 15, 20];
const shuffle = (a) => { const r = a.slice(); for (let i = r.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [r[i], r[j]] = [r[j], r[i]]; } return r; };
const lastKey = (id) => `teach_last_lesson_${id}`;

export function rememberLesson(cls, grade, n) { try { localStorage.setItem(lastKey(cls.id), JSON.stringify({ grade: Number(grade), n })); } catch { /* storage blocked */ } }

async function loadBank() {
  for (const u of ['/api/game/bank', '/data/teamgame_g7.json']) {
    try { const r = await fetch(u); if (r.ok) { const d = await r.json(); if (d && d.lessons) return d.lessons; } } catch { /* try the next */ }
  }
  return [];
}

export default function GameWizard({ classes, cls: given, style: preStyle, onClose }) {
  const [cls, setCls] = useState(given || (classes.length === 1 ? classes[0] : null));
  const [step, setStep] = useState(0);            // 0 class · 1 lesson · 2 style · 3 teams
  const [bank, setBank] = useState(null);
  const [students, setStudents] = useState(null);
  const [picked, setPicked] = useState([]);
  const [qn, setQn] = useState(20);
  const [style, setStyle] = useState(preStyle || 'cards');
  const [nTeams, setNTeams] = useState(4);
  const [noTeam, setNoTeam] = useState(false);
  const [deal, setDeal] = useState(0);            // bump to deal the teams again
  const [err, setErr] = useState('');
  const [bankOpen, setBankOpen] = useState(false);
  const [popup, setPopup] = useState(false);        // the divide-groups pop-up

  const grade = cls ? parseInt(gradeOf(cls), 10) || 7 : 7;
  useEffect(() => { loadBank().then(setBank); }, []);
  useEffect(() => {
    if (!cls) return undefined;
    let live = true; setStudents(null);
    api(`/api/classes/${cls.id}/students`).then((d) => live && setStudents(d.students || [])).catch((e) => live && setErr(e.message));
    return () => { live = false; };
  }, [cls]);

  const lessons = useMemo(() => (bank || []).filter((L) => (L.g || 7) === grade).sort((a, b) => a.n - b.n), [bank, grade]);
  // the lesson last taught in this class, when the bank has it; otherwise the first one
  useEffect(() => {
    if (!cls || !lessons.length) return;
    let last = null; try { last = JSON.parse(localStorage.getItem(lastKey(cls.id))); } catch { /* none */ }
    const want = last && last.grade === grade ? (grade === 7 ? last.n : 100 * (grade - 7) + last.n) : null;
    const hit = lessons.find((L) => L.n === want);
    setPicked([(hit || lessons[0]).n]);
  }, [cls, lessons]); // eslint-disable-line react-hooks/exhaustive-deps
  const wasLast = useMemo(() => {
    if (!cls) return null; try { const l = JSON.parse(localStorage.getItem(lastKey(cls.id))); return l && l.grade === grade ? (grade === 7 ? l.n : 100 * (grade - 7) + l.n) : null; } catch { return null; }
  }, [cls, grade]);

  // students present today: the Spin remembers who was crossed out
  const absentIds = useMemo(() => { if (!cls) return []; try { return (JSON.parse(localStorage.getItem(`exam_wheel_${cls.id}`)) || {}).off || []; } catch { return []; } }, [cls]);
  const present = useMemo(() => (students || []).filter((s) => !absentIds.includes(String(s.id))), [students, absentIds]);
  const teams = useMemo(() => {
    const names = present.map(fullName).filter(Boolean);
    const n = Math.max(1, Math.min(nTeams, names.length || 1));
    const t = Array.from({ length: n }, () => []);
    shuffle(names).forEach((nm, i) => t[i % n].push(nm));
    return t;
  }, [present, nTeams, deal]); // eslint-disable-line react-hooks/exhaustive-deps

  const palette = useMemo(() => shuffle(['#e8590c', '#1c7ed6', '#2f9e44', '#ae3ec9', '#f08c00', '#0c8599', '#d6336c', '#5f3dc4']), [deal]);   // new random colours for every deal
  const other = OTHERS.find((o) => o.k === style);
  const lastStep = other ? 2 : 3;
  const styleName = (STYLES.find((s) => s.k === style) || other || {}).t;
  const summary = cls ? [cls.name, picked.length ? `${kh(picked.length)} មេរៀន` : null, styleName, step >= 3 ? (noTeam ? 'គ្មានក្រុម' : `${kh(teams.length)} ក្រុម`) : null, !other && step >= 2 ? `${qn} សំណួរ`.replace(/\d+/, (d) => kh(d)) : null].filter(Boolean).join(' · ') : '';

  const start = () => {
    if (other) { location.href = other.href(cls); return; }
    if (!present.length && !noTeam) { setErr('ថ្នាក់នេះមិនទាន់មានសិស្សទេ។'); return; }
    try { localStorage.setItem('km_wheel_last_groups', JSON.stringify({ cls: cls.name, groups: teams })); } catch { /* storage blocked */ }
    location.href = `/teamgame.html?from=teach&wiz=1&import=1&style=${style}&grade=${grade}&l=${picked.join(',')}&n=${qn}${noTeam ? '&nt=1' : ''}`;
  };
  const next = () => { setErr(''); if (step === lastStep) start(); else setStep(step + 1); };
  const togglePick = (n) => setPicked((p) => (p.includes(n) ? (p.length > 1 ? p.filter((x) => x !== n) : p) : [...p, n]));
  const canNext = step === 0 ? !!cls : step === 1 ? picked.length > 0 : true;
  const steps = ['ថ្នាក់', 'មេរៀន', 'ហ្គេម', 'ក្រុម'];

  return (
    <Modal title="🎮 លេងហ្គេមជាមួយថ្នាក់" sub={summary || 'ជ្រើសថ្នាក់ មេរៀន ហ្គេម ហើយចាប់ផ្ដើម'} onClose={onClose} wide>
      <ol className="gw-steps">{steps.map((t, i) => (i === 3 && other ? null : <li key={t} className={i === step ? 'on' : i < step ? 'done' : ''}><span>{kh(i + 1)}</span>{t}</li>))}</ol>

      {step === 0 && (
        <ul className="pick-list">{classes.map((c) => <li key={c.id}><button onClick={() => { setCls(c); setStep(1); }}><b>{c.name}</b><small>{kh(c.student_count)} សិស្ស</small></button></li>)}</ul>
      )}

      {step === 1 && (
        <div className="gw-pane">
          <div className="gw-row"><b>មេរៀនដែលត្រូវលេង</b><span className="gw-tools"><button className="btn ghost sm" onClick={() => setBankOpen(true)}>✎ សំណួរ</button><button className="btn ghost sm" onClick={() => setPicked(lessons.map((L) => L.n))}>ជ្រើសទាំងអស់</button></span></div>
          {!bank ? <div className="spinner" /> : !lessons.length ? <p className="muted">មិនទាន់មានសំណួរហ្គេមសម្រាប់ថ្នាក់ទី {kh(grade)} ទេ។</p> : (
            <div className="gw-lessons">{lessons.map((L) => (
              <button key={L.n} className={`gw-lesson${picked.includes(L.n) ? ' on' : ''}`} onClick={() => togglePick(L.n)}>
                <span>{L.title}</span>{L.n === wasLast && <small>បានបង្រៀនចុងក្រោយ</small>}
              </button>))}
            </div>
          )}
          <div className="gw-row"><b>ចំនួនសំណួរ</b><div className="chips">{QN.map((n) => <button key={n} className={qn === n ? 'on' : ''} onClick={() => setQn(n)}>{kh(n)}</button>)}<input className={`qtype${QN.includes(qn) ? '' : ' on'}`} type="number" min="1" max="100" placeholder="វាយចំនួន" aria-label="វាយចំនួនសំណួរ" value={QN.includes(qn) ? '' : qn} onChange={(e) => { const v = parseInt(e.target.value, 10); if (v >= 1) setQn(Math.min(100, v)); }} /></div></div>
        </div>
      )}

      {step === 2 && (
        <div className="gw-pane">
          <div className="gw-styles">{STYLES.map((s) => (
            <button key={s.k} className={`gw-style${style === s.k ? ' on' : ''}`} onClick={() => setStyle(s.k)}>
              <img src={s.img} alt="" loading="lazy" /><b>{s.ic} {s.t}</b><small>{s.d}</small>
            </button>))}
          </div>
          <p className="gw-sub">ហ្គេមផ្សេងទៀត</p>
          <div className="gw-others">{OTHERS.map((o) => (
            <button key={o.k} className={`gw-other${style === o.k ? ' on' : ''}`} onClick={() => setStyle(o.k)}><span>{o.ic}</span><b>{o.t}</b><small>{o.d}</small></button>))}
          </div>
        </div>
      )}

      {step === 3 && !other && (
        <div className="gw-pane">
          <div className="gw-mode" role="radiogroup" aria-label="របៀបលេង">
            <button type="button" role="radio" aria-checked={!noTeam} className={!noTeam ? 'on' : ''} onClick={() => setNoTeam(false)}><b>👥 លេងជាក្រុម</b><small>ចែកសិស្សជាក្រុម ហើយប្រកួតគ្នា</small></button>
            <button type="button" role="radio" aria-checked={noTeam} className={noTeam ? 'on' : ''} onClick={() => setNoTeam(true)}><b>🙋 លេងម្នាក់ៗ</b><small>លោកគ្រូអ្នកគ្រូហៅសិស្សម្នាក់ៗ មិនមានក្រុម</small></button>
          </div>
          {students && absentIds.length > 0 && <p className="gw-note">✕ មិនដាក់សិស្សអវត្តមាន {kh(students.length - present.length)} នាក់ (ដែលបានគូសក្នុងកង់ចាប់ឈ្មោះ)</p>}
          {noTeam ? (
            <p className="gw-solo">សិស្សទាំង {kh(present.length)} នាក់លេងជាមួយគ្នា — ចុច «ចាប់ផ្ដើមហ្គេម» ដើម្បីបន្ត។ ចង់លេងជាក្រុម សូមចុច «👥 លេងជាក្រុម» ខាងលើ។</p>
          ) : (
            <>
              <div className="gw-row">
                <b>ចំនួនក្រុម</b>
                <div className="gw-stepper"><button disabled={nTeams <= 2} onClick={() => setNTeams(nTeams - 1)}>−</button><output>{kh(teams.length)}</output><button disabled={nTeams >= 8} onClick={() => setNTeams(nTeams + 1)}>+</button></div>
                <button className="btn primary" onClick={() => { setDeal(deal + 1); setPopup(true); }}>👥 ចែកក្រុម</button>
              </div>
              <div className="gw-teams">{teams.map((t, i) => (
                <div key={i} className="gw-team" style={{ borderTop: `6px solid ${palette[i % palette.length]}` }}><b style={{ color: palette[i % palette.length] }}>ក្រុមទី {kh(i + 1)} <small>{kh(t.length)} នាក់</small></b><span>{t.join(' · ')}</span></div>))}
              </div>
            </>
          )}
        </div>
      )}

      {err && <p className="alert">{err}</p>}
      {popup && !noTeam && <DealPopup key={deal} teams={teams} colors={palette} cname={cls ? cls.name : ''} onAgain={() => setDeal((d) => d + 1)} onClose={() => setPopup(false)} />}
      {bankOpen && <QuestionBank lesson={picked[0]} onClose={() => { setBankOpen(false); loadBank().then(setBank); }} />}
      <div className="gw-bar">
        <button className="btn ghost" onClick={() => (step > 0 && !(step === 1 && given) ? setStep(step - 1) : onClose())}>{step > 0 && !(step === 1 && given) ? '← ថយក្រោយ' : 'បោះបង់'}</button>
        {step > 0 && <button className="btn primary big" disabled={!canNext || (step >= 1 && students === null && step === 3)} onClick={next}>{step === lastStep ? '▶ ចាប់ផ្ដើមហ្គេម' : 'បន្ទាប់ →'}</button>}
      </div>
    </Modal>
  );
}
