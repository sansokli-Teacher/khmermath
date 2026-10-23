import { useCallback, useEffect, useState } from 'react';
import { api, kh, todayISO, SCHEDULE } from './api.js';
import { attendanceReport } from './report.js';

const shift = (iso, n) => { const [y, m, d] = iso.split('-').map(Number); const t = new Date(y, m - 1, d + n); const p = (x) => String(x).padStart(2, '0'); return `${t.getFullYear()}-${p(t.getMonth() + 1)}-${p(t.getDate())}`; };
const copyText = async (text) => {
  try { await navigator.clipboard.writeText(text); }
  catch { const t = document.createElement('textarea'); t.value = text; document.body.append(t); t.select(); try { document.execCommand('copy'); } catch { /* nothing else to try */ } t.remove(); }
};

// Everything recorded on one day, period by period: read it again, correct the lesson note, copy the message, or jump to a period to fix its attendance.
export default function AttendanceDay({ cls, day, onDay, teacher, subject, onEdit }) {
  const [data, setData] = useState(null);
  const [err, setErr] = useState('');
  const [topics, setTopics] = useState({});
  const [copied, setCopied] = useState('');
  const [withTopic, setWithTopic] = useState(true);

  const load = useCallback(async () => {
    setErr('');
    try {
      const d = await api(`/api/attendance/day?class_id=${cls.id}&day=${day}`);
      setData(d);
      setTopics(Object.fromEntries(d.periods.map((p) => [p.period, p.topic || ''])));
    } catch (e) { setErr(e.message || 'មិនអាចផ្ទុកបានទេ។'); }
  }, [cls.id, day]);
  useEffect(() => { setData(null); load(); }, [load]);

  const reportOf = (p) => attendanceReport({ day, className: cls.name, subject: p.subject || subject, period: p.period, absent: p.absent, teacher, topic: topics[p.period] ?? p.topic ?? '', withTopic });
  const copy = async (key, text) => { await copyText(text); setCopied(key); setTimeout(() => setCopied(''), 2200); };
  const saveTopic = async (p) => {
    if ((topics[p.period] || '') === (p.topic || '')) return;
    try { await api('/api/attendance/info', { method: 'POST', body: { class_id: cls.id, day, period: p.period, subject: p.subject || subject, topic: topics[p.period] || '' } }); load(); }
    catch (e) { setErr(e.message || 'មិនអាចរក្សាទុកបានទេ។'); }
  };

  const total = data ? data.periods.reduce((n, p) => n + p.absent.length, 0) : 0;
  return (
    <div className="att-day">
      <div className="att-day-nav">
        <button className="btn ghost" onClick={() => onDay(shift(day, -1))} aria-label="ថ្ងៃមុន">‹</button>
        <input type="date" value={day} onChange={(e) => onDay(e.target.value || todayISO())} aria-label="ថ្ងៃ" />
        <button className="btn ghost" onClick={() => onDay(shift(day, 1))} aria-label="ថ្ងៃបន្ទាប់">›</button>
        <button className={`btn ghost${day === shift(todayISO(), -1) ? ' on' : ''}`} onClick={() => onDay(shift(todayISO(), -1))}>ម្សិលមិញ</button>
        <button className={`btn ghost${day === todayISO() ? ' on' : ''}`} onClick={() => onDay(todayISO())}>ថ្ងៃនេះ</button>
      </div>
      {err && <p className="alert">{err} <button className="link" onClick={load}>សាកម្តងទៀត</button></p>}
      {!data && !err && <div className="skeleton-grid"><div className="sk" /><div className="sk" /></div>}
      {data && !data.periods.length && <div className="empty slim"><span>📅</span><p>ថ្ងៃដែលបានជ្រើសមិនទាន់មានកំណត់ត្រាទេ។ ចុច «✎ ចុះវត្តមាន» ដើម្បីចុះសម្រាប់ថ្ងៃនេះ ឬជ្រើសថ្ងៃផ្សេង។</p></div>}
      {data && data.periods.length > 0 && (
        <>
          <div className="att-day-sum">
            <span>{kh(data.periods.length)} ម៉ោង · អវត្តមានសរុប <b>{kh(total)}</b> ដង</span>
            <label className="chk"><input type="checkbox" checked={withTopic} onChange={(e) => setWithTopic(e.target.checked)} /> បញ្ចូលមេរៀន</label>
            <button className="btn primary" onClick={() => copy('all', data.periods.map(reportOf).join('\n\n'))}>{copied === 'all' ? '✓ បានចម្លង' : '📋 ចម្លងគ្រប់ម៉ោង'}</button>
          </div>
          <ul className="att-day-list">
            {data.periods.map((p) => {
              const sc = SCHEDULE[p.period - 1];
              return (
                <li key={p.period} className={`att-day-card${p.recorded ? '' : ' none'}`}>
                  <div className="att-day-h">
                    <b>ម៉ោងទី {kh(p.period)}</b><small>{sc ? `${sc.s}–${sc.e}` : ''}</small>
                    <span className={`tag ${p.recorded ? 'ok' : 'warn'}`}>{p.recorded ? `អវត្តមាន ${kh(p.absent.length)}${p.late.length ? ` · យឺត ${kh(p.late.length)}` : ''} · មាន ${kh(p.present)}` : 'មិនទាន់ចុះវត្តមាន'}</span>
                  </div>
                  <div className="field">
                    <label htmlFor={`dt-${p.period}`}>បង្រៀន ({p.subject || subject})</label>
                    <input id={`dt-${p.period}`} type="text" maxLength={300} placeholder="ឧ. ចំនួនគត់" value={topics[p.period] ?? ''} onChange={(e) => setTopics((t) => ({ ...t, [p.period]: e.target.value }))} onBlur={() => saveTopic(p)} />
                  </div>
                  {p.absent.length > 0 && <p className="att-day-names"><b>អវត្តមាន ៖</b> {p.absent.map((n, i) => `${kh(i + 1)}. ${n}`).join(' · ')}</p>}
                  {p.late.length > 0 && <p className="att-day-names"><b>យឺត ៖</b> {p.late.join(' · ')}</p>}
                  <div className="att-day-act">
                    <button className="btn ghost" onClick={() => copy(p.period, reportOf(p))}>{copied === p.period ? '✓ បានចម្លង' : '📋 ចម្លង'}</button>
                    <button className="btn primary" onClick={() => onEdit(p.period)}>✎ កែវត្តមាន</button>
                  </div>
                </li>
              );
            })}
          </ul>
        </>
      )}
    </div>
  );
}
