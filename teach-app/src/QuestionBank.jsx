import { useEffect, useMemo, useRef, useState } from 'react';
import { api, kh, loadScript } from './api.js';
import Modal from './Modal.jsx';

// The game question bank in teaching mode: the list of questions, ✎ Edit and 🗑 Delete (hide). The owner changes the shared bank;
// every other teacher changes their own copy only (the server decides), and a deleted question can be restored.
const LV = { easy: 'ងាយ', medium: 'មធ្យម', hard: 'ពិបាក' };
const SYMBOLS = [['\\(  \\)', 'គណិត'], ['\\frac{a}{b}', 'ប្រភាគ'], ['\\sqrt{ }', '√'], ['^{2}', 'x²'], ['\\times', '×'], ['\\div', '÷'], ['\\leq', '≤'], ['\\geq', '≥'], ['^{\\circ}', '°'], ['\\angle', '∠'], ['\\parallel', '∥']];

function Tex({ text, className, as: Tag = 'div' }) {
  const ref = useRef(null);
  useEffect(() => {
    const el = ref.current; if (!el) return;
    el.textContent = text || '';
    Promise.all([loadScript('/katex/katex.min.js')]).then(() => loadScript('/katex/contrib/auto-render.min.js')).then(() => {
      if (window.renderMathInElement && ref.current) window.renderMathInElement(ref.current, { delimiters: [{ left: '\\(', right: '\\)', display: false }, { left: '\\[', right: '\\]', display: true }], throwOnError: false });
    }).catch(() => {});
  }, [text]);
  return <Tag ref={ref} className={className} />;
}

const fieldsOf = (q) => ({ t: q.t, q: q.q, lv: q.lv, h: q.h || '', s: q.s || '', a: q.a, o: q.o, k: q.k });

function Editor({ lesson, q, onClose, onSaved }) {
  const [f, setF] = useState(() => ({ ...fieldsOf(q), o: q.o ? q.o.slice() : null }));
  const [err, setErr] = useState('');
  const [busy, setBusy] = useState(false);
  const last = useRef(null);
  const set = (k, v) => setF((x) => ({ ...x, [k]: v }));
  const insert = (ins) => {
    const el = last.current; if (!el) return;
    const a = el.selectionStart ?? el.value.length, b = el.selectionEnd ?? a;
    const v = el.value.slice(0, a) + ins + el.value.slice(b);
    const [key, idx] = el.dataset.k.split(':');
    if (key === 'o') setF((x) => { const o = x.o.slice(); o[+idx] = v; return { ...x, o }; }); else set(key, v);
  };
  const save = async (off) => {
    setBusy(true); setErr('');
    try {
      const fields = { t: f.t, q: f.q, lv: f.lv, h: f.h, s: f.s };
      if (f.o) { fields.o = f.o; fields.k = f.k; } else fields.a = f.a;
      await api('/api/game/question', { method: 'POST', body: { lesson: lesson.n, i: q.i, fields, off: off ?? q.off } });
      onSaved();
    } catch (e) { setErr(e.message); setBusy(false); }
  };
  const reset = async () => { try { await api('/api/game/reset', { method: 'POST', body: { lesson: lesson.n, i: q.i } }); onSaved(); } catch (e) { setErr(e.message); } };
  const focus = (e) => { last.current = e.target; };
  return (
    <Modal title={`✎ សំណួរទី ${kh(q.i + 1)}`} sub={lesson.title} onClose={onClose} wide>
      <div className="qb-edit">
        <div className="qb-form">
          <p className="muted">{'សរសេរគណិតវិទ្យាក្នុង \\( … \\) ឧ. \\(\\frac{3}{4}\\)'}</p>
          <div className="qb-sym">{SYMBOLS.map(([ins, lab]) => <button key={lab} type="button" title={ins} onClick={() => insert(ins)}>{lab}</button>)}</div>
          <label>សំណួរ<textarea rows="4" data-k="q" value={f.q} onFocus={focus} onChange={(e) => set('q', e.target.value)} /></label>
          {f.o ? (
            <div className="qb-opts"><b>ជម្រើស (ចុចរង្វង់ដើម្បីជ្រើសចម្លើយត្រឹមត្រូវ)</b>
              {f.o.map((o, i) => (
                <div key={i} className="qb-opt"><input type="radio" name="qb-k" checked={f.k === i} onChange={() => set('k', i)} /><span>{'កខគឃ'[i]}</span>
                  <input type="text" data-k={`o:${i}`} value={o} onFocus={focus} onChange={(e) => setF((x) => { const n = x.o.slice(); n[i] = e.target.value; return { ...x, o: n }; })} /></div>
              ))}
            </div>
          ) : <label>ចម្លើយ<input type="text" data-k="a" value={f.a} onFocus={focus} onChange={(e) => set('a', e.target.value)} /></label>}
          <label>ដំណោះស្រាយ<textarea rows="3" data-k="s" value={f.s} onFocus={focus} onChange={(e) => set('s', e.target.value)} /></label>
          <label>គន្លឹះ<input type="text" data-k="h" value={f.h} onFocus={focus} onChange={(e) => set('h', e.target.value)} /></label>
          <div className="qb-two">
            <label>ផ្នែក<input type="text" value={f.t} onChange={(e) => set('t', e.target.value)} /></label>
            <label>កម្រិត<select value={f.lv} onChange={(e) => set('lv', e.target.value)}>{Object.keys(LV).map((v) => <option key={v} value={v}>{LV[v]}</option>)}</select></label>
          </div>
        </div>
        <div className="qb-prev">
          <b>មើលជាមុន</b>
          <Tex text={f.q} className="qb-pq" />
          {q.f && <div className="qb-fig" dangerouslySetInnerHTML={{ __html: q.f }} />}
          {f.o ? <div className="qb-pgrid">{f.o.map((o, i) => <div key={i} className={`qb-po${f.k === i ? ' ok' : ''}`}><Tex as="span" text={`${'កខគឃ'[i]}. ${o}`} /></div>)}</div> : <div className="qb-po ok"><Tex as="span" text={`ចម្លើយ៖ ${f.a}`} /></div>}
          {f.s && <Tex text={`ដំណោះស្រាយ៖ ${f.s}`} className="muted" />}
        </div>
      </div>
      {err && <p className="alert">{err}</p>}
      <div className="gw-bar">
        {(q.edited || q.stale) ? <button className="btn ghost" onClick={reset}>↺ ត្រឡប់ទៅសំណួរដើម</button> : <span />}
        <span className="qb-actions"><button className="btn ghost" onClick={onClose}>បោះបង់</button><button className="btn primary" disabled={busy} onClick={() => save()}>រក្សាទុក</button></span>
      </div>
    </Modal>
  );
}

export default function QuestionBank({ lesson: firstLesson, onClose }) {
  const [data, setData] = useState(null);
  const [n, setN] = useState(firstLesson || null);
  const [filter, setFilter] = useState('all');
  const [edit, setEdit] = useState(null);
  const [sure, setSure] = useState(null);
  const [err, setErr] = useState('');
  const load = () => api('/api/game/admin').then((d) => { setData(d); setN((cur) => (cur && d.lessons.some((L) => L.n === cur) ? cur : d.lessons[0] && d.lessons[0].n)); }).catch((e) => setErr(e.message));
  useEffect(() => { load(); }, []); // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => { if (!sure) return undefined; const t = setTimeout(() => setSure(null), 3500); return () => clearTimeout(t); }, [sure]);
  const L = data && data.lessons.find((x) => x.n === n);
  const qs = useMemo(() => (L ? L.qs.filter((q) => filter === 'all' || (filter === 'edited' && q.edited) || (filter === 'off' && q.off) || (filter === 'fig' && q.f)) : []), [L, filter]);
  const label = (x) => `${x.g && x.g !== 7 ? `ថ្នាក់ទី ${kh(x.g)} · ` : ''}មេរៀនទី ${kh(x.d || x.n)} · ${x.title}`;
  const toggle = async (q) => {
    try { await api('/api/game/question', { method: 'POST', body: { lesson: L.n, i: q.i, fields: fieldsOf(q), off: !q.off } }); setSure(null); await load(); } catch (e) { setErr(e.message); }
  };
  return (
    <Modal title="📚 សំណួរហ្គេម" sub={data ? (data.is_owner ? 'ការកែ ឬលុបរបស់អ្នក (ជាម្ចាស់) ប៉ះពាល់គ្រូទាំងអស់ និងសិស្ស' : 'ការកែ និងការលុបរបស់អ្នកប្រើតែក្នុងហ្គេមរបស់អ្នកប៉ុណ្ណោះ — អាចស្ដារវិញបាន') : ''} onClose={onClose} wide>
      {err && <p className="alert">{err}</p>}
      {!data ? <div className="spinner" /> : (
        <>
          <div className="qb-top">
            <select value={n || ''} onChange={(e) => setN(Number(e.target.value))} aria-label="មេរៀន">{data.lessons.map((x) => <option key={x.n} value={x.n}>{label(x)}</option>)}</select>
            <select value={filter} onChange={(e) => setFilter(e.target.value)} aria-label="តម្រង">
              <option value="all">សំណួរទាំងអស់</option><option value="edited">ដែលបានកែ</option><option value="off">ដែលបានលុប</option><option value="fig">ដែលមានរូប</option>
            </select>
            <span className="muted">{kh(qs.length)} សំណួរ</span>
          </div>
          <div className="qb-list">
            {qs.map((q) => (
              <div key={q.i} className={`qb-row${q.off ? ' off' : ''}`}>
                <b className="qb-n">{kh(q.i + 1)}</b>
                <div className="qb-body">
                  <Tex text={q.q} className="qb-q" />
                  {q.o && <div className="qb-og">{q.o.map((o, k) => <Tex key={k} text={`${'កខគឃ'[k]}. ${o}${k === q.k ? ' ✓' : ''}`} className={k === q.k ? 'ok' : ''} />)}</div>}
                  <small className="muted">{[q.mine ? '👤 របស់ខ្ញុំ' : '', q.edited ? '✎ កែរួច' : '', q.off ? '🗑 បានលុប' : '', q.f ? '🖼 មានរូប' : '', LV[q.lv] || ''].filter(Boolean).join(' · ')}</small>
                </div>
                <div className="qb-btns">
                  <button className="btn ghost sm" onClick={() => setEdit(q)}>✎ កែ</button>
                  {q.off ? <button className="btn ghost sm" onClick={() => toggle(q)}>↩ ស្ដារវិញ</button>
                    : sure === q.i ? <button className="btn primary sm qb-del" onClick={() => toggle(q)}>បញ្ជាក់លុប?</button>
                    : <button className="btn ghost sm" onClick={() => setSure(q.i)}>🗑 លុប</button>}
                </div>
              </div>
            ))}
            {!qs.length && <p className="muted">មិនមានសំណួរទេ។</p>}
          </div>
        </>
      )}
      {edit && L && <Editor lesson={L} q={edit} onClose={() => setEdit(null)} onSaved={() => { setEdit(null); load(); }} />}
    </Modal>
  );
}
