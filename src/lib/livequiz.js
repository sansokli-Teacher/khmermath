// Live quiz on students' phones (Kahoot-style). Pure helpers: which game questions can be graded automatically, how an answer
// is compared, and how many points it earns. The server keeps the correct answer; phones only ever receive the public part.

const strip = (s) => String(s ?? '').replace(/\\\(|\\\)/g, '').replace(/\\[, ;!]/g, '').replace(/\\%/g, '%').replace(/\^\{\\circ\}/g, '°').replace(/\\text\{([^}]*)\}/g, '$1').replace(/[{}]/g, '').replace(/\s+/g, ' ').trim();

// "\(4\,200\) ក្បាល", "\(63^{\circ}\)", "\(25\%\)", "12 នាក់" → 4200, 63, 25, 12 ; fractions / expressions / words → null
export function numericAnswer(a) {
  const t = strip(a);
  const m = /^(-?\d[\d ]*(?:[.,]\d+)?)\s*(%|°|[^\d\s\\=<>+\-*/^()]*(?:\s[^\d\\=<>+\-*/^()]+)*)$/u.exec(t);
  if (!m) return null;
  const n = Number(m[1].replace(/\s/g, '').replace(',', '.'));
  return Number.isFinite(n) ? n : null;
}
export function parseStudentNumber(s) {
  const t = String(s ?? '').replace(/[០-៩]/g, (d) => '០១២៣៤៥៦៧៨៩'.indexOf(d)).replace(/\s/g, '').replace(',', '.').replace(/^−/, '-');
  if (!/^-?\d+(\.\d+)?$/.test(t)) return null;
  return Number(t);
}

// ---- numeric answers become multiple-choice: make three believable wrong options around the right one ----
const TOKEN = /-?\d+(?:(?:\\,|\\ |,| )\d{3})*(?:\.\d+)?/;
function fmtLike(n, dec, sep) {
  let t = Math.abs(n).toFixed(dec);
  let [i, f] = t.split('.');
  if (sep && i.length > 3) i = i.replace(/\B(?=(\d{3})+(?!\d))/g, sep);
  return (n < 0 ? '-' : '') + i + (f ? '.' + f : '');
}
export function numericOptions(a, rand = Math.random) {
  const m = TOKEN.exec(String(a));
  const n = numericAnswer(a);
  if (!m || n === null) return null;
  const dec = (m[0].split('.')[1] || '').length, sep = m[0].includes('\\,') ? '\\,' : m[0].includes(' ') ? ' ' : '', step = dec ? Math.pow(10, -dec) : 1;
  const r = (x) => Number(x.toFixed(dec));
  const tiers = [
    [n + step, n - step, n + 2 * step, n - 2 * step, n + 3 * step],
    [n * 2, n / 2, n + 10 * step, n - 10 * step, -n, n * 1.1, n * 0.9, n + 5 * step],
    [n * 10, n / 10, n + 100 * step, n - 100 * step, n * 3, n + 20 * step],
  ];
  const seen = new Set([fmtLike(n, dec, sep)]), out = [];
  const take = (arr, want) => {
    const pool = arr.map(r).filter((x) => Number.isFinite(x) && (n < 0 || x >= 0) && (dec || Number.isInteger(x)));
    for (let k = pool.length - 1; k > 0; k--) { const j = Math.floor(rand() * (k + 1)); [pool[k], pool[j]] = [pool[j], pool[k]]; }
    for (const x of pool) { const f = fmtLike(x, dec, sep); if (out.length >= want || seen.has(f)) continue; seen.add(f); out.push(f); }
  };
  take(tiers[0], 2); take(tiers[1], 3); take(tiers[2], 3); take(tiers[0], 3);
  for (let k = 4; out.length < 3 && k < 30; k++) take([n + k * step, n - k * step], 3);
  if (out.length < 3) return null;
  const o = out.slice(0, 3).map((f) => String(a).replace(m[0], f));
  const k = Math.floor(rand() * 4);
  o.splice(k, 0, String(a));
  return { o, k };
}

// → { pub, key } or null when the question cannot be graded automatically.
//   pub = what a phone shows; key = what the server compares with.
export function classify(q, rand = Math.random) {
  const base = { q: q.q, ...(q.f ? { f: q.f } : {}) };
  if (Array.isArray(q.o) && q.o.length >= 2 && Number.isInteger(q.k)) {
    return { pub: { ...base, k: 'mcq', o: q.o }, key: { k: 'mcq', correct: q.k, show: q.o[q.k], sol: q.s || '' } };
  }
  if (q.a === 'ពិត' || q.a === 'មិនពិត') {
    return { pub: { ...base, k: 'tf', q: String(q.q).replace(/\s*ពិត ឬ មិនពិត\?\s*$/, '') }, key: { k: 'tf', correct: q.a === 'ពិត' ? 'T' : 'F', show: q.a, sol: q.s || '' } };
  }
  const n = numericAnswer(q.a);
  if (n !== null) {
    const mc = numericOptions(q.a, rand);
    if (mc) return { pub: { ...base, k: 'mcq', o: mc.o }, key: { k: 'mcq', correct: mc.k, show: q.a, sol: q.s || '' } };
    return { pub: { ...base, k: 'num' }, key: { k: 'num', correct: n, show: q.a, sol: q.s || '' } };
  }
  return null;
}

export function isCorrect(key, choice) {
  if (key.k === 'mcq') return Number(choice) === key.correct;
  if (key.k === 'tf') return String(choice) === key.correct;
  const v = parseStudentNumber(choice);
  return v !== null && Math.abs(v - key.correct) < 1e-6 * Math.max(1, Math.abs(key.correct));
}

// 1000 for an instant correct answer down to 500 at the last second; nothing for a wrong one
export function points(correct, ms, secs) {
  if (!correct) return 0;
  const f = Math.min(1, Math.max(0, ms / (secs * 1000)));
  return Math.round(1000 * (1 - f / 2));
}

export function newCode(rand = Math.random) { return String(100000 + Math.floor(rand() * 900000)); }
