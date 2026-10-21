// The team-game question bank. The base bank is public/data/teamgame_g7.json (22 lessons x 20 questions); teachers fix wrong
// questions here, and each fix is stored as an "edit" keyed by (lesson, index). Merging base + edits gives the bank that both
// exam.khmermath.org and khmermath.org play. An edit remembers a hash of the base question it was made on: if the base
// question is later regenerated with different text, the edit is flagged stale and is NOT applied to the game.

export const EDITABLE = ['t', 'q', 'lv', 'h', 's', 'a', 'o', 'k', 'tm'];
export const LEVELS = ['easy', 'medium', 'hard'];

export function hashStr(s) {
  let h = 5381;
  for (let i = 0; i < s.length; i++) h = ((h << 5) + h + s.charCodeAt(i)) | 0;
  return (h >>> 0).toString(36);
}
// ---- answer time per question (seconds): reading + working + answering, x level, + a figure, snapped to a few easy tiers ----
// (bankwork/game_timer_analysis.py is the same model in Python; a teacher can override any question with their own `tm`)
const TM_TIERS = [15, 20, 30, 45, 60, 90, 120, 150, 180];
const TM_LV = { easy: 0.85, medium: 1.0, hard: 1.3, pisa: 1.5 };
const tmClean = (s) => String(s || '').replace(/\\(?:text|mathrm)\{([^}]*)\}/g, '$1').replace(/\\[()[\]]/g, '');
const tmSteps = (sol) => { const s = String(sol || ''); return (s.match(/=/g) || []).length + 0.5 * (s.match(/\\(?:times|div|frac|sqrt|cdot|pm)|[+×÷]/g) || []).length; };
export function suggestTime(q) {
  const mcq = Array.isArray(q.o) && q.o.length > 0;
  let read = 0.09 * tmClean(q.q).length;
  if (mcq) read += 0.05 * q.o.reduce((a, o) => a + tmClean(o).length, 0);
  const n = tmSteps(q.s), work = n === 0 ? 6 : 10 + 7 * Math.min(n, 8), ans = mcq ? 3 : 6;
  let t = (read + work + ans) * (TM_LV[q.lv] || 1) + (q.f ? 8 : 0);
  t = Math.max(15, Math.min(180, t));
  return TM_TIERS.reduce((b, x) => (Math.abs(x - t) < Math.abs(b - t) ? x : b), TM_TIERS[0]);
}
export const baseKey = (q) => hashStr(String(q.q || '') + '|' + String(q.a || ''));

// Validates what a teacher typed for one question; returns { data } (only the fields that may be stored) or { error }.
export function cleanEdit(input, base) {
  const f = input || {};
  const out = {};
  const str = (v, max, name, req) => {
    const s = String(v ?? '').replace(/\r/g, '').trim();
    if (req && !s) throw new Error(`${name} មិនអាចទទេបានទេ។`);
    if (s.length > max) throw new Error(`${name} វែងពេក (អតិបរមា ${max} តួ)។`);
    return s;
  };
  try {
    out.q = str(f.q, 2000, 'សំណួរ', true);
    out.t = str(f.t ?? base.t, 120, 'ផ្នែក', true);
    out.h = str(f.h, 1000, 'គន្លឹះ', false);
    out.s = str(f.s, 2000, 'ដំណោះស្រាយ', false);
    out.lv = LEVELS.includes(f.lv) ? f.lv : base.lv;
    const tm = f.tm === undefined || f.tm === null || f.tm === '' ? 0 : Number(f.tm);   // 0 = automatic (suggested) time
    if (!Number.isInteger(tm) || tm < 0 || tm > 600 || (tm > 0 && tm < 5)) throw new Error('ម៉ោងត្រូវនៅចន្លោះ ៥–៦០០ វិនាទី (ទុកទទេ = ស្វ័យប្រវត្តិ)។');
    out.tm = tm;
    if (Array.isArray(base.o)) {
      const o = Array.isArray(f.o) ? f.o.map((x) => str(x, 300, 'ជម្រើស', true)) : null;
      if (!o || o.length !== base.o.length) throw new Error(`ត្រូវមានជម្រើស ${base.o.length}។`);
      if (new Set(o).size !== o.length) throw new Error('ជម្រើសពីរមិនត្រូវដូចគ្នាទេ។');
      const k = Number(f.k);
      if (!Number.isInteger(k) || k < 0 || k >= o.length) throw new Error('សូមជ្រើសចម្លើយត្រឹមត្រូវ។');
      out.o = o; out.k = k; out.a = o[k];
    } else {
      out.a = str(f.a, 400, 'ចម្លើយ', true);
    }
  } catch (e) { return { error: e.message }; }
  return { data: out };
}

// A teacher's own fixes/deletes sit on top of the shared edits and win over them; each one is flagged `mine` so the editor can show it.
export function overlayEdits(shared, mine) {
  const m = new Map(shared);
  for (const [k, v] of mine) m.set(k, { ...v, mine: true });
  return m;
}

// base: { class, lessons:[{n,title,qs:[...]}] }, edits: Map("lesson:i" -> {bq, data, off}), cfg: { enabled, lessons }
export function mergeBank(base, edits, cfg, { admin = false } = {}) {
  const enabled = cfg.enabled !== false;
  const allow = Array.isArray(cfg.lessons) ? new Set(cfg.lessons.map(Number)) : null;
  const lessons = [];
  for (const L of base.lessons) {
    const on = enabled && (!allow || allow.has(L.n));
    if (!admin && !on) continue;
    const qs = [];
    L.qs.forEach((bq, i) => {
      const e = edits.get(`${L.n}:${i}`);
      const stale = !!e && e.bq !== baseKey(bq);
      const applied = e && !stale ? e.data : null;
      const off = !!(e && !stale && e.off);
      if (!admin && off) return;
      const q = { ...bq, ...(applied || {}) };
      const own = applied && applied.tm > 0 ? applied.tm : 0;
      q.tm = own || suggestTime(q);              // the time the game gives this question
      if (admin) {
        q.i = i; q.edited = !!applied; q.stale = stale; q.off = off; q.mine = !!(e && e.mine); q.tmSet = !!own; q.tmAuto = suggestTime(q);
        q.orig = { t: bq.t, q: bq.q, lv: bq.lv, h: bq.h, s: bq.s, a: bq.a, o: bq.o, k: bq.k };
      }
      qs.push(q);
    });
    lessons.push({ n: L.n, ...(L.g ? { g: L.g, d: L.d } : {}), title: L.title, qs, ...(admin ? { enabled: on } : {}) });
  }
  return { class: base.class, lessons };
}
