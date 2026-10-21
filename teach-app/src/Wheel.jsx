import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { api, kh, fullName, todayISO } from './api.js';

const SONGS = [
  { id: '', t: 'គ្មានបទ (សំឡេងចុច)' },
  { id: '/audio/kamlang-chet.mp3', t: 'កម្លាំងចិត្តក្នុងការប្រឡង' },
  { id: '/audio/kamlang-siksa.mp3', t: 'កម្លាំងចិត្តសិក្សា' },
];
const COLORS = ['#e8590c', '#1c7ed6', '#2f9e44', '#ae3ec9', '#d6336c', '#0c8599', '#f08c00', '#5f3dc4', '#c92a2a', '#087f5b'];
const TAU = Math.PI * 2;

const genderOf = (g) => (/^(ស្រី|f|female|girl)$/i.test(String(g || '').trim()) ? 'f' : /^(ប្រុស|m|male|boy)$/i.test(String(g || '').trim()) ? 'm' : '');
const shuffle = (a) => { const r = a.slice(); for (let i = r.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [r[i], r[j]] = [r[j], r[i]]; } return r; };

function loadMem(key) {
  const base = { off: [], done: [], hist: [] };
  try { return Object.assign(base, JSON.parse(localStorage.getItem(key))); } catch { return base; }
}

function drawWheel(canvas, items, rot) {
  const size = canvas.clientWidth;
  const dpr = Math.min(2, window.devicePixelRatio || 1);
  if (canvas.width !== Math.round(size * dpr)) { canvas.width = Math.round(size * dpr); canvas.height = Math.round(size * dpr); }
  const ctx = canvas.getContext('2d');
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  ctx.clearRect(0, 0, size, size);
  const c = size / 2;
  const R = c - 6;
  if (!items.length) {
    ctx.fillStyle = '#1b2756'; ctx.beginPath(); ctx.arc(c, c, R, 0, TAU); ctx.fill();
    return;
  }
  const arc = TAU / items.length;
  const fs = Math.max(12, Math.min(28, (R * arc) * 0.55, R / 9));
  ctx.save();
  ctx.translate(c, c);
  ctx.rotate(rot);
  items.forEach((it, i) => {
    ctx.beginPath(); ctx.moveTo(0, 0); ctx.arc(0, 0, R, i * arc, (i + 1) * arc); ctx.closePath();
    ctx.fillStyle = COLORS[i % COLORS.length]; ctx.fill();
    ctx.strokeStyle = 'rgba(255,255,255,.55)'; ctx.lineWidth = 2; ctx.stroke();
    ctx.save();
    ctx.rotate((i + 0.5) * arc);
    ctx.textAlign = 'right'; ctx.textBaseline = 'middle';
    ctx.fillStyle = '#fff'; ctx.font = `700 ${fs}px 'Kantumruy Pro', sans-serif`;
    ctx.shadowColor = 'rgba(0,0,0,.35)'; ctx.shadowBlur = 3;
    let t = it.n;
    const max = R - 70;
    while (t.length > 2 && ctx.measureText(t).width > max) t = t.slice(0, -2) + '…';
    ctx.fillText(t, R - 16, 0);
    ctx.restore();
  });
  ctx.restore();
}

export default function Wheel({ cls, students }) {
  const KEY = `exam_wheel_${cls.id}`;
  const people = useMemo(() => students.map((s) => ({ id: String(s.id), n: fullName(s), g: genderOf(s.gender) })), [students]);
  const [mem, setMem] = useState(() => loadMem(KEY));
  const [mode, setMode] = useState('one'); // one | group
  const [groupN, setGroupN] = useState(6);
  const [groups, setGroups] = useState([]);
  const [noRepeat, setNoRepeat] = useState(true);
  const [gender, setGender] = useState('');
  const [song, setSong] = useState(() => localStorage.getItem('teach_wheel_song') || '');
  const [winner, setWinner] = useState(null);
  const [spinning, setSpinning] = useState(false);
  const full = false;
  const [absentSynced, setAbsentSynced] = useState(false);
  const canvasRef = useRef(null);
  const rotRef = useRef(0);
  const audioRef = useRef(null);
  const actx = useRef(null);
  const raf = useRef(0);
  const fwCv = useRef(null);
  const fwRaf = useRef(0);
  const [board, setBoard] = useState(false);   // every group at once

  // fireworks over the whole screen (glowing, fading trails like the old name wheel)
  const fireworks = (ms = 3200) => {
    const cv = fwCv.current;
    if (!cv || (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches)) return;
    const W2 = window.innerWidth, H2 = window.innerHeight, dpr = Math.min(2, window.devicePixelRatio || 1);
    cv.width = W2 * dpr; cv.height = H2 * dpr;
    const g = cv.getContext('2d'); g.setTransform(dpr, 0, 0, dpr, 0, 0);
    let parts = []; const end = performance.now() + ms; let next = 0; const hues = [8, 40, 52, 130, 190, 280, 330];
    const burst = (x, y) => { const h = hues[Math.floor(Math.random() * hues.length)]; for (let i = 0; i < 46; i++) { const a = TAU * i / 46 + Math.random() * 0.2, v = 2.2 + Math.random() * 3.6; parts.push({ x, y, vx: Math.cos(a) * v, vy: Math.sin(a) * v, life: 1, h: h + Math.random() * 30, w: 2 + Math.random() * 2 }); } };
    const loop = (now) => {
      g.globalCompositeOperation = 'destination-out'; g.fillStyle = 'rgba(0,0,0,.22)'; g.fillRect(0, 0, W2, H2); g.globalCompositeOperation = 'lighter';
      if (now < end && now >= next) { burst(W2 * (0.12 + Math.random() * 0.76), H2 * (0.1 + Math.random() * 0.5)); next = now + 380 + Math.random() * 260; }
      parts.forEach((q) => { q.x += q.vx; q.y += q.vy; q.vy += 0.05; q.vx *= 0.99; q.life -= 0.012; g.globalAlpha = Math.max(0, q.life); g.fillStyle = `hsl(${q.h} 95% 60%)`; g.beginPath(); g.arc(q.x, q.y, q.w, 0, TAU); g.fill(); });
      g.globalAlpha = 1; g.globalCompositeOperation = 'source-over';
      parts = parts.filter((q) => q.life > 0);
      if (now < end || parts.length) fwRaf.current = requestAnimationFrame(loop); else g.clearRect(0, 0, W2, H2);
    };
    cancelAnimationFrame(fwRaf.current); fwRaf.current = requestAnimationFrame(loop);
  };
  const fanfare = () => {
    try {
      actx.current = actx.current || new (window.AudioContext || window.webkitAudioContext)();
      [523, 659, 784, 1047].forEach((f, i) => { const o = actx.current.createOscillator(), g = actx.current.createGain(), t = actx.current.currentTime + i * 0.12; o.frequency.value = f; g.gain.setValueAtTime(0.12, t); g.gain.exponentialRampToValueAtTime(0.001, t + 0.3); o.connect(g); g.connect(actx.current.destination); o.start(t); o.stop(t + 0.32); });
    } catch { /* no audio */ }
  };

  useEffect(() => { setMem(loadMem(KEY)); setWinner(null); setGroups([]); setAbsentSynced(false); }, [KEY]);
  const saveMem = (m) => { setMem(m); try { localStorage.setItem(KEY, JSON.stringify(m)); } catch { /* storage blocked */ } };

  const makeGroups = useCallback(() => {
    const here = people.filter((p) => !mem.off.includes(p.id));
    const n = Math.max(1, Math.min(groupN, here.length || 1));
    const pal = shuffle(COLORS);   // a new random colour set for every deal
    const gs = Array.from({ length: n }, (_, i) => ({ id: `g${i}`, n: `ក្រុមទី ${kh(i + 1)}`, people: [], c: pal[i % pal.length] }));
    shuffle(here).forEach((p, i) => gs[i % n].people.push(p));
    setGroups(gs);
    saveMem({ ...mem, doneG: [] });
    setWinner(null);
  }, [people, mem, groupN]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => { if (mode === 'group' && !groups.length && people.length) makeGroups(); }, [mode, groups.length, people.length, makeGroups]);

  // Mark today's absent students (from attendance) as away, once per class.
  const syncAbsent = async () => {
    try {
      const out = new Set();
      for (let p = 1; p <= 8; p++) {
        const d = await api(`/api/attendance?class_id=${cls.id}&day=${todayISO()}&period=${p}`);
        (d.rows || []).forEach((r) => { if (r.mark === 'A') out.add(String(r.student_id)); });
      }
      saveMem({ ...mem, off: [...out] });
      setAbsentSynced(true);
    } catch { /* attendance optional */ }
  };

  const items = useMemo(() => {
    if (mode === 'group') return groups.filter((g) => !(noRepeat && (mem.doneG || []).includes(g.id)));
    return people.filter((p) => !mem.off.includes(p.id) && !(noRepeat && mem.done.includes(p.id)) && (!gender || p.g === gender));
  }, [mode, groups, people, mem, noRepeat, gender]);

  const rootRef = useRef(null);
  useEffect(() => {
    const draw = () => canvasRef.current && drawWheel(canvasRef.current, items, rotRef.current);
    draw();
    const ro = new ResizeObserver(draw);
    if (canvasRef.current) ro.observe(canvasRef.current);
    return () => ro.disconnect();
  }, [items, full]);

  useEffect(() => () => { cancelAnimationFrame(raf.current); cancelAnimationFrame(fwRaf.current); if (audioRef.current) audioRef.current.pause(); }, []);

  const tick = () => {
    try {
      actx.current = actx.current || new (window.AudioContext || window.webkitAudioContext)();
      const o = actx.current.createOscillator(); const g = actx.current.createGain();
      o.frequency.value = 900; g.gain.value = 0.04; o.connect(g); g.connect(actx.current.destination);
      o.start(); o.stop(actx.current.currentTime + 0.025);
    } catch { /* no audio */ }
  };

  const spin = () => {
    if (spinning || !items.length) return;
    setWinner(null);
    const idx = Math.floor(Math.random() * items.length);
    const arc = TAU / items.length;
    const target = (-Math.PI / 2 - (idx + 0.5) * arc + (Math.random() - 0.5) * arc * 0.7);
    const from = rotRef.current;
    const mod = (x) => ((x % TAU) + TAU) % TAU;
    const to = from + 6 * TAU + mod(target - from);
    const dur = 4600 + Math.random() * 1200;
    const t0 = performance.now();
    let lastSlice = -1;
    setSpinning(true);
    if (song) {
      if (!audioRef.current || audioRef.current.dataset.src !== song) { if (audioRef.current) audioRef.current.pause(); audioRef.current = new Audio(song); audioRef.current.dataset.src = song; audioRef.current.loop = true; }
      audioRef.current.currentTime = 0; audioRef.current.play().catch(() => {});
    }
    const step = (now) => {
      const p = Math.min(1, (now - t0) / dur);
      const e = 1 - Math.pow(1 - p, 4);
      rotRef.current = from + (to - from) * e;
      drawWheel(canvasRef.current, items, rotRef.current);
      const s = Math.floor(mod(-Math.PI / 2 - rotRef.current) / arc);
      if (s !== lastSlice) { lastSlice = s; if (!song) tick(); }
      if (p < 1) { raf.current = requestAnimationFrame(step); return; }
      if (audioRef.current) audioRef.current.pause();
      const w = items[idx];
      setSpinning(false);
      setWinner(w); fanfare(); fireworks(3200);
      if (mode === 'group') saveMem({ ...mem, doneG: [...(mem.doneG || []), w.id] });
      else saveMem({ ...mem, done: [...mem.done, w.id], hist: [...mem.hist, { n: w.n, t: Date.now() }].slice(-300) });
    };
    raf.current = requestAnimationFrame(step);
  };

  const toggleOff = (id) => { saveMem({ ...mem, off: mem.off.includes(id) ? mem.off.filter((x) => x !== id) : [...mem.off, id] }); if (mode === 'group') setGroups([]); };
  const divide = () => { makeGroups(); setBoard(true); fanfare(); fireworks(2600); };
  const reset = () => { saveMem({ ...mem, done: [], doneG: [] }); setWinner(null); };
  const changeSong = (v) => { setSong(v); try { localStorage.setItem('teach_wheel_song', v); } catch { /* noop */ } };

  useEffect(() => {
    const onKey = (e) => { if (e.code === 'Space' && e.target === document.body && !e.repeat) { e.preventDefault(); spin(); } };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  });

  const hist = [...mem.hist].reverse().slice(0, 8);

  return (
    <div className={`wheel${full ? ' full' : ''}`} ref={rootRef}>
      <div className="wheel-stage">
        <div className="wheel-box">
          <canvas ref={canvasRef} className="wheel-canvas" aria-label="កង់ឈ្មោះសិស្ស" />
          <button className="hub" onClick={spin} disabled={spinning || !items.length}>SPIN</button>
        </div>
        {mode === 'group' && groups.length > 0 && (
          <div className="wheel-dealt">
            {groups.map((g, k) => (
              <div key={g.id} className={`dealt-g${(mem.doneG || []).includes(g.id) ? ' done' : ''}`} style={{ '--c': g.c || COLORS[k % COLORS.length] }}>
                <b>{g.n}</b> <small>{kh(g.people.length)} នាក់</small>
                <span>{g.people.map((p) => p.n).join(' · ')}</span>
              </div>
            ))}
          </div>
        )}
        {!items.length && <p className="wheel-empty">{mode === 'one' ? 'សិស្សត្រូវបានជ្រើសអស់ហើយ។' : 'ក្រុមទាំងអស់ត្រូវបានជ្រើសហើយ។'} <button className="link" onClick={reset}>ចាប់ផ្តើមឡើងវិញ</button></p>}
      </div>

      <aside className="wheel-side">
        <div className="seg2" role="tablist">
          <button className={mode === 'one' ? 'on' : ''} onClick={() => { setMode('one'); setWinner(null); }}>🎡 ម្នាក់ៗ</button>
          <button className={mode === 'group' ? 'on' : ''} onClick={() => { setMode('group'); setWinner(null); }}>👥 ក្រុម</button>
        </div>

        {mode === 'group' && (
          <div className="row">
            <label htmlFor="gn">ចំនួនក្រុម</label>
            <input id="gn" type="number" min="1" max="20" value={groupN} onChange={(e) => { setGroupN(Math.max(1, Math.min(20, Number(e.target.value) || 1))); setGroups([]); }} />
            <button className="btn primary sm" onClick={divide}>👥 ចែកក្រុម</button>
          </div>
        )}

        <div className="wheel-btns">
          <button className="btn primary grow" onClick={spin} disabled={spinning || !items.length}>បង្វិលកង់</button>
          <button className="btn ghost" onClick={reset}>↺</button>
        </div>

        <div className="away2">
          <div className="away2-h"><b>✕ អវត្តមាន ({kh(mem.off.length)}) — ចុចឈ្មោះដើម្បីគូស</b><button className="btn ghost sm" onClick={syncAbsent}>ពីវត្តមានថ្ងៃនេះ</button></div>
          <div className="chips2">{people.map((p) => <button key={p.id} className={`chip2${mem.off.includes(p.id) ? ' off' : ''}`} onClick={() => toggleOff(p.id)}>{p.n}</button>)}</div>
        </div>

        <details className="more">
          <summary>ជម្រើសបន្ថែម</summary>
          {mode === 'one' && (
            <div className="row">
              <label>ភេទ</label>
              <div className="chips">
                {[['', 'ទាំងអស់'], ['f', '♀ ស្រី'], ['m', '♂ ប្រុស']].map(([v, t]) => <button key={v} className={gender === v ? 'on' : ''} onClick={() => setGender(v)}>{t}</button>)}
              </div>
            </div>
          )}
          <label className="check"><input type="checkbox" checked={noRepeat} onChange={(e) => setNoRepeat(e.target.checked)} /> មិនជ្រើសម្តងទៀត</label>
          <div className="row">
            <label htmlFor="song">🎵 បទ</label>
            <select id="song" value={song} onChange={(e) => changeSong(e.target.value)}>
              {SONGS.map((s) => <option key={s.id} value={s.id}>{s.t}</option>)}
            </select>
          </div>
        </details>

        {hist.length > 0 && (
          <div className="hist"><h4>បានជ្រើសថ្មីៗ</h4><ol>{hist.map((x, i) => <li key={x.t + i}>{x.n}</li>)}</ol></div>
        )}
      </aside>

      {board && (
        <div className="win" role="dialog" aria-label="ក្រុម" onClick={() => setBoard(false)}>
          <div className="win-card board" onClick={(e) => e.stopPropagation()}>
            <p>👥 បែងចែកក្រុមរួចរាល់! · {kh(groups.reduce((n, g) => n + g.people.length, 0))} នាក់</p>
            <div className="board-grid">
              {groups.map((g, k) => (
                <div className="board-g" key={g.id} style={{ '--c': g.c || COLORS[k % COLORS.length] }}>
                  <b>{g.n}</b><span>{kh(g.people.length)} នាក់</span>
                  <ol>{g.people.map((p) => <li key={p.id}>{p.n}</li>)}</ol>
                </div>
              ))}
            </div>
            <div className="wheel-btns">
              <button className="btn primary" onClick={() => { makeGroups(); fanfare(); fireworks(2600); }}>ចែកម្តងទៀត</button>
              <button className="btn ghost" onClick={() => setBoard(false)}>បិទ</button>
            </div>
          </div>
        </div>
      )}

      {winner && (
        <div className="win" role="dialog" aria-label="លទ្ធផល" onClick={() => setWinner(null)}>
          <div className="win-card" onClick={(e) => e.stopPropagation()}>
            <p>🎉 {mode === 'group' ? 'ក្រុមដែលត្រូវបានជ្រើស' : 'សិស្សដែលត្រូវបានជ្រើស'}</p>
            <h2>{winner.n}</h2>
            {winner.people && <ul className="win-members">{winner.people.map((p) => <li key={p.id}>{p.n}</li>)}</ul>}
            <div className="wheel-btns">
              <button className="btn primary" onClick={() => { setWinner(null); setTimeout(spin, 50); }}>បង្វិលម្តងទៀត</button>
              {!winner.people && <button className="btn ghost absent-btn" onClick={() => { toggleOff(winner.id); setWinner(null); }}>✕ អវត្តមាន</button>}
              <button className="btn ghost" onClick={() => setWinner(null)}>បិទ</button>
            </div>
          </div>
        </div>
      )}
      <canvas ref={fwCv} className="wheel-fw" aria-hidden="true" />
    </div>
  );
}
