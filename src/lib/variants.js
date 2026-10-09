// Question variants: the same question with different numbers for every student, so a
// screenshot or a neighbour's answer does not help. The teacher writes the question once:
//
//   Stem:      [[a]] + [[b]] = ?
//   Options:   [[a+b]]  /  [[a+b+1]]  /  [[a*b]]  /  [[a-b]]      (first one is the right answer if correct_index = 0)
//   Variables: a = 2..9
//              b = 3..9
//              c = {2,4,5}          (pick one of a list)
//              d = a + b            (computed from earlier variables)
//
// Everything is derived from a seed (session, student, question), so the student's exam,
// their review and the teacher's view of that student always show the same numbers.

const KH_DIGITS = '០១២៣៤៥៦៧៨៩';
export const hasVariants = (q) => !!(q && q.params && String(q.params).trim());

function rng(seedText) {
  let h = 2166136261;
  for (const ch of seedText) { h ^= ch.charCodeAt(0); h = Math.imul(h, 16777619) >>> 0; }
  return () => { h = (Math.imul(h ^ (h >>> 15), 2246822507) + 0x6D2B79F5) >>> 0; return h / 4294967296; };
}

// ---- tiny arithmetic evaluator: numbers, variables, + - * / ^ and parentheses (no eval)
function tokenize(src) {
  const out = [], re = /\s*(?:(\d+(?:\.\d+)?)|([A-Za-z_][A-Za-z0-9_]*)|(.))/gy;
  let m;
  while (re.lastIndex < src.length && (m = re.exec(src))) {
    if (m[1] !== undefined) out.push({ t: 'n', v: parseFloat(m[1]) });
    else if (m[2] !== undefined) out.push({ t: 'v', v: m[2] });
    else if (m[3] !== undefined && m[3].trim()) out.push({ t: 'o', v: m[3] });
  }
  return out;
}
export function evaluate(src, vars) {
  const toks = tokenize(src); let i = 0;
  const peek = () => toks[i], next = () => toks[i++];
  function primary() {
    const t = next();
    if (!t) throw new Error(`កន្សោម «${src}» មិនពេញលេញ`);
    if (t.t === 'n') return t.v;
    if (t.t === 'v') { if (!(t.v in vars)) throw new Error(`មិនស្គាល់អថេរ «${t.v}»`); return vars[t.v]; }
    if (t.v === '(') { const v = sum(); const c = next(); if (!c || c.v !== ')') throw new Error(`កន្សោម «${src}» ខ្វះ )`); return v; }
    if (t.v === '-') return -power();
    if (t.v === '+') return power();
    throw new Error(`សញ្ញា «${t.v}» មិនត្រឹមត្រូវក្នុង «${src}»`);
  }
  function power() { const b = primary(); if (peek() && peek().v === '^') { next(); return Math.pow(b, power()); } return b; }
  function product() { let v = power(); while (peek() && (peek().v === '*' || peek().v === '/' || peek().v === '×' || peek().v === '÷')) { const o = next().v; const r = power(); if ((o === '/' || o === '÷') && r === 0) throw new Error('ចែកនឹងសូន្យ'); v = (o === '*' || o === '×') ? v * r : v / r; } return v; }
  function sum() { let v = product(); while (peek() && (peek().v === '+' || peek().v === '-')) { const o = next().v; const r = product(); v = o === '+' ? v + r : v - r; } return v; }
  const v = sum();
  if (i < toks.length) throw new Error(`កន្សោម «${src}» មានតួអក្សរលើស`);
  return v;
}

export function parseParams(text) {
  const defs = [];
  for (const raw of String(text || '').split(/\n|;/)) {
    const line = raw.trim();
    if (!line) continue;
    const m = line.match(/^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+)$/);
    if (!m) throw new Error(`បន្ទាត់អថេរមិនត្រឹមត្រូវ៖ «${line}» (ឧ. a = 2..9)`);
    const [, name, rhs] = m;
    let r;
    if ((r = rhs.match(/^(-?\d+)\s*\.\.\s*(-?\d+)$/))) {
      const lo = Number(r[1]), hi = Number(r[2]);
      if (hi < lo) throw new Error(`ចន្លោះ «${line}» ត្រូវតែពីតូចទៅធំ`);
      defs.push({ name, kind: 'range', lo, hi });
    } else if ((r = rhs.match(/^\{(.+)\}$/))) {
      const list = r[1].split(',').map((x) => Number(x.trim()));
      if (!list.length || list.some((x) => !Number.isFinite(x))) throw new Error(`បញ្ជី «${line}» ត្រូវមានតែលេខ`);
      defs.push({ name, kind: 'list', list });
    } else {
      defs.push({ name, kind: 'expr', expr: rhs });
    }
  }
  return defs;
}

export function fmtNumber(v) {
  if (!Number.isFinite(v)) throw new Error('លទ្ធផលមិនមែនជាលេខ');
  const r = Math.round(v * 10000) / 10000;
  return String(Object.is(r, -0) ? 0 : r);
}

function fill(text, vars) {
  if (text == null) return text;
  return String(text).replace(/\[\[([^\]]+)\]\]/g, (_, expr) => fmtNumber(evaluate(expr, vars)));
}

function draw(defs, rand) {
  const vars = {};
  for (const d of defs) {
    if (d.kind === 'range') vars[d.name] = d.lo + Math.floor(rand() * (d.hi - d.lo + 1));
    else if (d.kind === 'list') vars[d.name] = d.list[Math.floor(rand() * d.list.length)];
    else vars[d.name] = evaluate(d.expr, vars);
  }
  return vars;
}

// Returns the question with its numbers filled in for this student.
export function instantiate(q, sessionId, studentId, salt = '') {
  if (!hasVariants(q)) return q;
  const defs = parseParams(q.params);
  let best = null;
  for (let attempt = 0; attempt < 40; attempt++) {
    const vars = draw(defs, rng(`var:${salt}${sessionId}:${studentId}:${q.id}:${attempt}`));
    let opts = [];
    try { opts = JSON.parse(q.options_json || '[]').map((o) => fill(o, vars)); } catch {}
    const out = { ...q, stem_text: fill(q.stem_text, vars), options_json: JSON.stringify(opts), solution_text: fill(q.solution_text, vars), vars };
    if (!best) best = out;
    if (new Set(opts).size === opts.length) return out;      // the choices must stay different from each other
  }
  return best;
}

// Used when a teacher saves a question: catches typos before a student ever sees them.
export function checkTemplate(q) {
  const out = instantiate({ ...q, id: q.id || 0 }, 0, 'check');
  return { sample: { stem_text: out.stem_text, options: JSON.parse(out.options_json), solution_text: out.solution_text } };
}
export const sampleFor = (q, key) => {
  const out = instantiate(q, 0, key);
  return { stem_text: out.stem_text, options: JSON.parse(out.options_json), solution_text: out.solution_text };
};
export const _KH = KH_DIGITS;
