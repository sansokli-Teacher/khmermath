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

// → { pub, key } or null when the question cannot be graded automatically.
//   pub = what a phone shows; key = what the server compares with.
export function classify(q) {
  const base = { q: q.q, ...(q.f ? { f: q.f } : {}) };
  if (Array.isArray(q.o) && q.o.length >= 2 && Number.isInteger(q.k)) {
    return { pub: { ...base, k: 'mcq', o: q.o }, key: { k: 'mcq', correct: q.k, show: q.o[q.k], sol: q.s || '' } };
  }
  if (q.a === 'ពិត' || q.a === 'មិនពិត') {
    return { pub: { ...base, k: 'tf', q: String(q.q).replace(/\s*ពិត ឬ មិនពិត\?\s*$/, '') }, key: { k: 'tf', correct: q.a === 'ពិត' ? 'T' : 'F', show: q.a, sol: q.s || '' } };
  }
  const n = numericAnswer(q.a);
  if (n !== null) return { pub: { ...base, k: 'num' }, key: { k: 'num', correct: n, show: q.a, sol: q.s || '' } };
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
