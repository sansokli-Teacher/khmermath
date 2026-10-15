// The team-game question bank. The base bank is public/data/teamgame_g7.json (22 lessons x 20 questions); teachers fix wrong
// questions here, and each fix is stored as an "edit" keyed by (lesson, index). Merging base + edits gives the bank that both
// exam.khmermath.org and khmermath.org play. An edit remembers a hash of the base question it was made on: if the base
// question is later regenerated with different text, the edit is flagged stale and is NOT applied to the game.

export const EDITABLE = ['t', 'q', 'lv', 'h', 's', 'a', 'o', 'k'];
export const LEVELS = ['easy', 'medium', 'hard'];

export function hashStr(s) {
  let h = 5381;
  for (let i = 0; i < s.length; i++) h = ((h << 5) + h + s.charCodeAt(i)) | 0;
  return (h >>> 0).toString(36);
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
      if (admin) {
        q.i = i; q.edited = !!applied; q.stale = stale; q.off = off;
        q.orig = { t: bq.t, q: bq.q, lv: bq.lv, h: bq.h, s: bq.s, a: bq.a, o: bq.o, k: bq.k };
      }
      qs.push(q);
    });
    lessons.push({ n: L.n, ...(L.g ? { g: L.g, d: L.d } : {}), title: L.title, qs, ...(admin ? { enabled: on } : {}) });
  }
  return { class: base.class, lessons };
}
