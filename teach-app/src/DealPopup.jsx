import { useEffect, useRef, useState } from 'react';
import { kh } from './api.js';

// The «divide groups» pop-up: a banner, then each group is filled one by one (names shuffle, then lock with a crash and a burst),
// fireworks and a fanfare at the end. Same look as the Spin's divide-groups pop-up.
const shuffle = (a) => { const r = a.slice(); for (let i = r.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [r[i], r[j]] = [r[j], r[i]]; } return r; };
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const calm = () => window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
let audio = null;
function beep(freqs, vol, len, gap = 0.12) {
  try {
    audio = audio || new (window.AudioContext || window.webkitAudioContext)();
    freqs.forEach((f, i) => { const o = audio.createOscillator(), g = audio.createGain(), t = audio.currentTime + i * gap; o.frequency.value = f; g.gain.setValueAtTime(vol, t); g.gain.exponentialRampToValueAtTime(0.001, t + len); o.connect(g); g.connect(audio.destination); o.start(t); o.stop(t + len + 0.02); });
  } catch { /* no audio */ }
}
function makeFx(cv) {
  const r = cv.parentElement.getBoundingClientRect(), dpr = Math.min(2, window.devicePixelRatio || 1);
  cv.width = r.width * dpr; cv.height = r.height * dpr;
  const g = cv.getContext('2d'); g.setTransform(dpr, 0, 0, dpr, 0, 0);
  let parts = [], on = false, until = 0, next = 0, raf = 0, dead = false;
  const hues = [8, 40, 52, 130, 190, 280, 330];
  const burst = (x, y, n) => { const hu = hues[Math.floor(Math.random() * hues.length)]; for (let i = 0; i < n; i++) { const a = Math.PI * 2 * i / n + Math.random() * 0.2, v = 2.2 + Math.random() * 3.6; parts.push({ x, y, vx: Math.cos(a) * v, vy: Math.sin(a) * v, life: 1, h: hu + Math.random() * 30, w: 2 + Math.random() * 2 }); } };
  const loop = (now) => {
    if (dead) return;
    g.globalCompositeOperation = 'destination-out'; g.fillStyle = 'rgba(0,0,0,.22)'; g.fillRect(0, 0, r.width, r.height); g.globalCompositeOperation = 'lighter';
    if (now < until && now >= next) { burst(r.width * (0.12 + Math.random() * 0.76), r.height * (0.1 + Math.random() * 0.5), 46); next = now + 380 + Math.random() * 260; }
    parts.forEach((q) => { q.x += q.vx; q.y += q.vy; q.vy += 0.05; q.vx *= 0.99; q.life -= 0.012; g.globalAlpha = Math.max(0, q.life); g.fillStyle = `hsl(${q.h} 95% 60%)`; g.beginPath(); g.arc(q.x, q.y, q.w, 0, Math.PI * 2); g.fill(); });
    g.globalAlpha = 1; g.globalCompositeOperation = 'source-over'; parts = parts.filter((q) => q.life > 0);
    if (now < until || parts.length) raf = requestAnimationFrame(loop); else { on = false; g.clearRect(0, 0, r.width, r.height); }
  };
  const start = () => { if (!on) { on = true; raf = requestAnimationFrame(loop); } };
  return {
    show(ms) { until = performance.now() + ms; start(); },
    burstAt(x, y) { burst(x, y, 30); start(); },
    stop() { dead = true; cancelAnimationFrame(raf); },
  };
}

export default function DealPopup({ teams, colors, cname, onAgain, onClose }) {
  const n = teams.length;
  const [rows, setRows] = useState(() => teams.map((t) => ({ st: 'wait', names: t.map(() => '• • •') })));
  const [title, setTitle] = useState('កំពុងបែងចែកក្រុម…');
  const [done, setDone] = useState(false);
  const cv = useRef(null), grid = useRef(null), skip = useRef(false), cardRefs = useRef([]);
  const total = teams.reduce((a, t) => a + t.length, 0), d = new Date();
  const date = `${kh(d.getDate())}/${kh(d.getMonth() + 1)}/${kh(d.getFullYear())}`;

  useEffect(() => {
    let dead = false;
    const fx = cv.current ? makeFx(cv.current) : null;
    const patch = (i, row) => setRows((rs) => rs.map((x, k) => (k === i ? row : x)));
    (async () => {
      const quiet = calm(), per = quiet ? 0 : Math.max(800, Math.min(1500, 9000 / Math.max(1, n)));
      let remaining = teams.flat();
      const lock = (i, effects) => {
        patch(i, { st: 'done', names: teams[i] });
        const ids = new Set(teams[i]); remaining = remaining.filter((m) => !ids.has(m));
        if (effects && fx) { beep([160, 120, 90], 0.14, 0.25, 0.05); const el = cardRefs.current[i], w = cv.current.getBoundingClientRect(); if (el) { const r = el.getBoundingClientRect(); fx.burstAt(r.right - w.left - 30, r.top - w.top + 26); } }
      };
      for (let i = 0; i < n && !dead; i++) {
        if (skip.current || quiet) { lock(i, false); continue; }
        setTitle(`កំពុងបែងចែក ក្រុមទី ${kh(i + 1)}…`); patch(i, { st: 'active', names: teams[i].map(() => '• • •') });
        const el = cardRefs.current[i], gr = grid.current; if (el && gr) gr.scrollTo({ top: Math.max(0, el.offsetTop - gr.offsetTop - 8), behavior: 'smooth' });
        const t0 = performance.now();
        while (performance.now() - t0 < per && !skip.current && !dead) { patch(i, { st: 'active', names: shuffle(remaining).slice(0, teams[i].length) }); beep([700], 0.03, 0.02); await sleep(80); }
        if (dead) return;
        lock(i, !skip.current); if (!skip.current) await sleep(380);
      }
      if (dead) return;
      setTitle('បែងចែកក្រុមរួចរាល់! 🎉'); setDone(true); beep([523, 659, 784, 1047], 0.12, 0.3); if (fx) fx.show(3600);
    })();
    const onKey = (e) => { if (e.key === 'Escape') onClose(); };
    window.addEventListener('keydown', onKey);
    return () => { dead = true; if (fx) fx.stop(); window.removeEventListener('keydown', onKey); };
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <div className="dp-back" onMouseDown={(e) => { if (e.target === e.currentTarget) onClose(); }}>
      <div className="dp-card" role="dialog" aria-modal="true" aria-label="បែងចែកក្រុម">
        <div className="dp-ban"><b>{title}</b><small>{cname}{cname ? ' · ' : ''}{kh(total)} នាក់ · {date}</small></div>
        <div className="dp-grid" ref={grid}>
          {rows.map((r, k) => (
            <div key={k} ref={(el) => { cardRefs.current[k] = el; }} className={`dp-g ${r.st}`} style={{ '--c': colors[k % colors.length] }}>
              <div className="dp-gh"><b>ក្រុម {kh(k + 1)}</b><span>{kh(teams[k].length)} នាក់</span></div>
              <ol>{r.names.map((m, i) => <li key={i} className={r.st === 'done' ? '' : 'ph'}>{m}</li>)}</ol>
            </div>
          ))}
        </div>
        <div className="dp-act">
          {!done && <button type="button" className="dp-skip" onClick={() => { skip.current = true; }}>រំលង ▶▶</button>}
          {done && <button type="button" className="dp-again" onClick={onAgain}>🔀 ចែកម្ដងទៀត</button>}
          <button type="button" className="dp-ok" onClick={onClose}>បិទ</button>
        </div>
        <canvas ref={cv} className="dp-fw" aria-hidden="true" />
      </div>
    </div>
  );
}
