import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { api, kh, fullName, todayISO } from './api.js';

const MARKS = [
  { m: 'ok', t: 'មាន', cls: 'ok' },
  { m: 'A', t: 'អវត្តមាន', cls: 'ab' },
  { m: 'L', t: 'យឺត', cls: 'late' },
];

const blank = { mark: 'ok', note: '' };
const snap = (students, rows) => JSON.stringify(students.map((s) => { const r = rows[s.id] || blank; return [s.id, r.mark, r.note]; }));

export default function Attendance({ cls, students }) {
  const [day, setDay] = useState(todayISO());
  const [period, setPeriod] = useState(1);
  const [rows, setRows] = useState({});
  const [saved, setSaved] = useState('');
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

  const dirty = state === 'ready' && snap(students, rows) !== saved;

  useEffect(() => {
    if (!dirty) return undefined;
    const warn = (e) => { e.preventDefault(); e.returnValue = ''; };
    window.addEventListener('beforeunload', warn);
    return () => window.removeEventListener('beforeunload', warn);
  }, [dirty]);

  const set = (id, patch) => setRows((r) => ({ ...r, [id]: { ...(r[id] || blank), ...patch } }));
  const markAll = (mark) => setRows(Object.fromEntries(students.map((s) => [s.id, { ...(rows[s.id] || blank), mark }])));
  const guard = (fn) => () => { if (!dirty || window.confirm('មានការផ្លាស់ប្តូរមិនទាន់ចុះ។ បោះបង់ការផ្លាស់ប្តូរ?')) fn(); };

  const count = useMemo(() => {
    const c = { ok: 0, A: 0, L: 0 };
    students.forEach((s) => { c[(rows[s.id] || blank).mark] += 1; });
    return c;
  }, [students, rows]);

  async function save() {
    setState('saving');
    try {
      await api('/api/attendance', {
        method: 'POST',
        body: { class_id: cls.id, day, period, rows: students.map((s) => ({ student_id: String(s.id), ...(rows[s.id] || blank) })) },
      });
      setSaved(snap(students, rows));
      setState('ready');
    } catch (e) {
      setErr(e.message);
      setState('error');
    }
  }

  const shown = students.map((s, i) => ({ s, i })).filter(({ s }) => filter === 'all' || (rows[s.id] || blank).mark === filter);
  if (!students.length) return <div className="empty slim"><span>👥</span><p>ថ្នាក់នេះមិនទាន់មានសិស្សទេ។</p></div>;

  return (
    <div className="att">
      <div className="att-top">
        <div className="field">
          <label htmlFor="att-day">ថ្ងៃ</label>
          <input id="att-day" type="date" value={day} onChange={(e) => { const v = e.target.value || todayISO(); if (!dirty || window.confirm('មានការផ្លាស់ប្តូរមិនទាន់ចុះ។ បោះបង់ការផ្លាស់ប្តូរ?')) setDay(v); }} />
        </div>
        <div className="field grow">
          <label>ម៉ោងសិក្សា</label>
          <div className="periods">
            {Array.from({ length: 8 }, (_, i) => i + 1).map((n) => (
              <button key={n} className={`period${n === period ? ' on' : ''}`} onClick={guard(() => setPeriod(n))}>{kh(n)}</button>
            ))}
          </div>
        </div>
        <button className="btn ghost" onClick={() => markAll('ok')}>✓ មានវត្តមានទាំងអស់</button>
      </div>

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
              <li key={s.id} className={`stu m-${r.mark}`}>
                <span className="stu-n">{kh(i + 1)}</span>
                <div className="stu-who"><b>{fullName(s)}</b><small>{s.id}</small></div>
                <div className="seg" role="group" aria-label={`វត្តមាន ${fullName(s)}`}>
                  {MARKS.map((x) => (
                    <button key={x.m} className={`${x.cls}${r.mark === x.m ? ' on' : ''}`} aria-pressed={r.mark === x.m} onClick={() => set(s.id, { mark: x.m })}>{x.t}</button>
                  ))}
                </div>
                <button className={`note-btn${r.note ? ' has' : ''}`} title="កំណត់ចំណាំ" aria-label="កំណត់ចំណាំ" onClick={() => setNoteOpen((o) => ({ ...o, [s.id]: !open }))}>✎</button>
                {open && <input className="note" type="text" maxLength={400} placeholder="កំណត់ចំណាំ…" value={r.note} onChange={(e) => set(s.id, { note: e.target.value })} autoFocus={!r.note} />}
              </li>
            );
          })}
          {!shown.length && <li className="none">មិនមានសិស្សក្នុងតម្រងនេះទេ។</li>}
        </ul>
      )}

      <div className={`savebar${dirty ? ' show' : ''}`} role="status">
        <span>{dirty ? 'មានការផ្លាស់ប្តូរមិនទាន់រក្សាទុក' : 'បានរក្សាទុករួចរាល់'}</span>
        <button className="btn primary" disabled={!dirty || state === 'saving'} onClick={save}>{state === 'saving' ? 'កំពុងរក្សាទុក…' : 'ចុះវត្តមាន'}</button>
      </div>
    </div>
  );
}
