import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { api, kh, fullName, todayISO, SCHEDULE, periodAt, isLive } from './api.js';

const MARKS = [
  { m: 'ok', t: 'មាន', cls: 'ok' },
  { m: 'A', t: 'អវត្តមាន', cls: 'ab' },
  { m: 'L', t: 'យឺត', cls: 'late' },
];

const blank = { mark: 'ok', note: '' };
const snap = (students, rows) => JSON.stringify(students.map((s) => { const r = rows[s.id] || blank; return [s.id, r.mark, r.note]; }));

export default function Attendance({ cls, students }) {
  const [day, setDay] = useState(todayISO());
  const [period, setPeriod] = useState(() => periodAt());      // opens on the period that is running now
  const [editing, setEditing] = useState(false);                // after submitting, the list is locked until the teacher presses «កែប្រែ»
  const [rows, setRows] = useState({});
  const [saved, setSaved] = useState('');
  const [recorded, setRecorded] = useState(true); // false = nothing stored yet for this day + period
  const [flash, setFlash] = useState(false);
  const [state, setState] = useState('loading'); // loading | ready | saving | error
  const [err, setErr] = useState('');
  const [noteOpen, setNoteOpen] = useState({});
  const [filter, setFilter] = useState('all');
  const job = useRef(0);

  const load = useCallback(async () => {
    const n = ++job.current;
    setState('loading');
    setErr('');
    try {
      const data = await api(`/api/attendance?class_id=${cls.id}&day=${day}&period=${period}`);
      if (n !== job.current) return;
      const next = {};
      for (const r of data.rows || []) next[String(r.student_id)] = { mark: r.mark || 'ok', note: r.note || '' };
      setRows(next);
      setRecorded((data.rows || []).length > 0);
      setEditing(false);
      setSaved(snap(students, next));
      setNoteOpen({});
      setState('ready');
    } catch (e) {
      if (n !== job.current) return;
      setErr(e.message || 'មិនអាចផ្ទុកវត្តមានបានទេ។');
      setState('error');
    }
  }, [cls.id, day, period, students]);

  useEffect(() => { load(); }, [load]);

  const loaded = state !== 'loading';
  const changed = loaded && snap(students, rows) !== saved;
  // Everyone defaults to present, so a period with no record yet still has to be submitted.
  const unsaved = loaded && (changed || !recorded);

  useEffect(() => {
    if (!changed) return undefined;
    const warn = (e) => { e.preventDefault(); e.returnValue = ''; };
    window.addEventListener('beforeunload', warn);
    return () => window.removeEventListener('beforeunload', warn);
  }, [changed]);

  const locked = loaded && recorded && !editing && !changed;
  const set = (id, patch) => { if (locked) return; setRows((r) => ({ ...r, [id]: { ...(r[id] || blank), ...patch } })); };
  const markAll = (mark) => { if (locked) return; setRows(Object.fromEntries(students.map((s) => [s.id, { ...(rows[s.id] || blank), mark }]))); };
  const guard = (fn) => () => { if (!changed || window.confirm('មានការផ្លាស់ប្តូរមិនទាន់ចុះ។ បោះបង់ការផ្លាស់ប្តូរ?')) fn(); };

  const count = useMemo(() => {
    const c = { ok: 0, A: 0, L: 0 };
    students.forEach((s) => { c[(rows[s.id] || blank).mark] += 1; });
    return c;
  }, [students, rows]);

  async function save() {
    setState('saving');
    setErr('');
    try {
      await api('/api/attendance', {
        method: 'POST',
        body: { class_id: cls.id, day, period, rows: students.map((s) => ({ student_id: String(s.id), ...(rows[s.id] || blank) })) },
      });
      setSaved(snap(students, rows));
      setRecorded(true);
      setEditing(false);
      setState('ready');
      setFlash(true);
      setTimeout(() => setFlash(false), 2500);
    } catch (e) {
      setErr(e.message || 'មិនអាចរក្សាទុកបានទេ។');
      setState('ready');
    }
  }

  const shown = students.map((s, i) => ({ s, i })).filter(({ s }) => filter === 'all' || (rows[s.id] || blank).mark === filter);
  if (!students.length) return <div className="empty slim"><span>👥</span><p>ថ្នាក់នេះមិនទាន់មានសិស្សទេ។</p></div>;

  return (
    <div className="att">
      <div className="att-top">
        <div className="field">
          <label htmlFor="att-day">ថ្ងៃ</label>
          <input id="att-day" type="date" value={day} onChange={(e) => { const v = e.target.value || todayISO(); if (!changed || window.confirm('មានការផ្លាស់ប្តូរមិនទាន់ចុះ។ បោះបង់ការផ្លាស់ប្តូរ?')) setDay(v); }} />
        </div>
        <div className="field grow">
          <label>ម៉ោងសិក្សា</label>
          <div className="periods">
            {SCHEDULE.map(({ n, s, e }) => (
              <button key={n} className={`period${n === period ? ' on' : ''}${day === todayISO() && isLive(n) ? ' live' : ''}`} onClick={guard(() => setPeriod(n))} title={`${s}–${e}`}>
                <b>{kh(n)}</b><small>{s}–{e}</small>
              </button>
            ))}
          </div>
        </div>
        <button className="btn ghost" disabled={locked} onClick={() => markAll('ok')}>✓ មានវត្តមានទាំងអស់</button>
      </div>
      {locked && (
        <div className="att-done" role="status">
          <span>✓ បានចុះវត្តមានម៉ោងទី {kh(period)} ({SCHEDULE[period - 1].s}–{SCHEDULE[period - 1].e}) រួចរាល់</span>
          <button className="btn primary" onClick={() => setEditing(true)}>✎ កែប្រែ</button>
        </div>
      )}

      <div className="stats">
        {[{ k: 'all', t: 'សរុប', n: students.length, c: 'all' }, ...MARKS.map((x) => ({ k: x.m, t: x.t, n: count[x.m], c: x.cls }))].map((x) => (
          <button key={x.k} className={`stat ${x.c}${filter === x.k ? ' on' : ''}`} onClick={() => setFilter(x.k)}>
            <b>{kh(x.n)}</b><span>{x.t}</span>
          </button>
        ))}
      </div>

      {state === 'loading' && <div className="skeleton-grid">{students.slice(0, 8).map((s) => <div key={s.id} className="sk" />)}</div>}
      {state === 'error' && <p className="alert">{err} <button className="link" onClick={load}>សាកម្តងទៀត</button></p>}

      {state !== 'loading' && (
        <ul className="roster">
          {shown.map(({ s, i }) => {
            const r = rows[s.id] || blank;
            const open = noteOpen[s.id] || !!r.note;
            return (
              <li key={s.id} className={`stu m-${r.mark}${locked ? ' locked' : ''}`}>
                <span className="stu-n">{kh(i + 1)}</span>
                <div className="stu-who"><b>{fullName(s)}</b><small>{s.id}</small></div>
                <div className="seg" role="group" aria-label={`វត្តមាន ${fullName(s)}`}>
                  {MARKS.map((x) => (
                    <button key={x.m} className={`${x.cls}${r.mark === x.m ? ' on' : ''}`} aria-pressed={r.mark === x.m} disabled={locked} onClick={() => set(s.id, { mark: x.m })}>{x.t}</button>
                  ))}
                </div>
                <button className={`note-btn${r.note ? ' has' : ''}`} title="កំណត់ចំណាំ" aria-label="កំណត់ចំណាំ" disabled={locked} onClick={() => setNoteOpen((o) => ({ ...o, [s.id]: !open }))}>✎</button>
                {open && <input className="note" type="text" maxLength={400} placeholder="កំណត់ចំណាំ…" value={r.note} readOnly={locked} onChange={(e) => set(s.id, { note: e.target.value })} autoFocus={!r.note && !locked} />}
              </li>
            );
          })}
          {!shown.length && <li className="none">មិនមានសិស្សក្នុងតម្រងនេះទេ។</li>}
        </ul>
      )}

      <div className={`savebar${unsaved ? ' show' : ''}${err ? ' err' : ''}${flash ? ' ok' : ''}`} role="status">
        <span>
          {err ? `⚠ ${err}`
            : flash ? '✓ បានចុះវត្តមានរួចរាល់'
            : changed ? 'មានការផ្លាស់ប្តូរមិនទាន់រក្សាទុក'
            : !recorded ? 'មិនទាន់បានចុះវត្តមានសម្រាប់ម៉ោងនេះ — ចុច «ចុះវត្តមាន» ដើម្បីរក្សាទុក'
            : 'បានរក្សាទុករួចរាល់ — ចុច «កែប្រែ» ដើម្បីកែ'}
        </span>
        <button className="btn primary" disabled={!unsaved || state === 'saving'} onClick={save}>{state === 'saving' ? 'កំពុងរក្សាទុក…' : err ? 'សាកម្តងទៀត' : 'ចុះវត្តមាន'}</button>
      </div>
    </div>
  );
}
