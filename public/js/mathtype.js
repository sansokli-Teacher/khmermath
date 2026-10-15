// Typing mathematics in a text field — ported from the PISA CBA app's
// js/mathtype.js with enhanced math mode, equation recognition, and root support.
//
// A teacher can type plain text — 3/4, x^2, 2^(n+1), √20, ∛8, ⁿ√x, π, n + 9 = 21 —
// and it renders as real math automatically wherever displayed, while keeping
// Khmer sentences (e.g. រក n ដើម្បីឱ្យ n + 9 = 21) in plain Khmer font.
// They can also wrap in $ $ / $$ $$ or \( \) / \[ \] for explicit math mode.
(function () {
  'use strict';
  const { h } = Exam;

  const latin = (str) => String(str == null ? '' : str).replace(/[០-៩]/g, (c) => String(c.charCodeAt(0) - 0x17e0));

  // A run of characters that could belong to a piece of mathematics.
  const RUN = /[0-9០-៩A-Za-z.,+\-−×÷*·/^()[\]=<>≤≥≠≈±π√∛∜ⁿ°%²³⁴ ]+/g;

  // Common measurement units that should remain plain text when standalone
  const PLAIN_WORDS = new Set(['cm', 'mm', 'km', 'dm', 'm', 'kg', 'g', 'mg', 's', 'h', 'mn', 'l', 'ml', 'ha']);

  // Determines whether a run of characters contains genuine mathematical content
  function isWorth(t) {
    const clean = t.trim().replace(/^[.,;:!?]+|[.,;:!?]+$/g, '');
    if (!clean) return false;
    if (PLAIN_WORDS.has(clean.toLowerCase())) return false;

    // 1. Definite math symbols: roots, fractions, exponents, Greek, degrees
    if (/[/^√∛∜π²³⁴°]|sqrt|cbrt|ⁿ√/.test(clean)) return true;

    // 2. Comparison and equality operators (e.g. n + 9 = 21, x = 5, y <= 10)
    if (/[=<>≤≥≠≈±]/.test(clean) && /[0-9០-៩A-Za-z]/.test(clean)) return true;

    // 3. Arithmetic operators between numbers/letters (e.g. n + 9, 2x - 3)
    if (/[+\-−×÷*·]/.test(clean) && /[0-9០-៩A-Za-z]/.test(clean)) return true;

    // 4. Function call notation, e.g. f(x), g(n), P(A)
    if (/^[A-Za-z]\([0-9០-៩A-Za-z+\-/*= ]+\)$/.test(clean)) return true;

    // 5. Standalone single Latin letter variables: x, n, y, z, a, b, etc.
    if (/^[a-zA-Z]$/.test(clean)) return true;

    // 6. Letter with numerical coefficient: 2x, 5n, 3y, etc.
    if (/^\d+[a-zA-Z]$/.test(clean)) return true;

    return false;
  }

  const OPS = {
    '×': '\\times ', '*': '\\times ', '·': '\\cdot ', '÷': '\\div ', '−': '-', '≤': '\\le ', '≥': '\\ge ',
    '≠': '\\ne ', '≈': '\\approx ', '±': '\\pm ', '%': '\\%', '<': '<', '>': '>', '=': '=', '+': '+', '-': '-',
  };
  const LONE = { '^': '\\text{\\textasciicircum}', '°': '{}^{\\circ}', '²': '{}^{2}', '³': '{}^{3}', '⁴': '{}^{4}' };

  // Recursive-descent parser over one run: an atom is a number, a word, π, a
  // bracketed group, or a root, with any powers after it; a/b takes the atom
  // before and the atom after the slash.
  function toTex(src) {
    const s = latin(src);
    let i = 0;
    const peek = () => s[i];
    const skip = () => { while (s[i] === ' ') i++; };
    const join = (items) => items.map((x) => x.tex).join('');

    function group(close) {
      const items = seq(close);
      if (s[i] === close) i++;
      return items;
    }

    function primary() {
      skip();
      const c = peek();
      if (!c) return null;

      if (c === '(' || c === '[') {
        i++;
        const close = c === '(' ? ')' : ']';
        const inner = join(group(close));
        return { tex: '\\left' + c + inner + '\\right' + close, inner, atom: true };
      }

      // Cube root: ∛ or cbrt or ³√
      if (c === '∛' || s.startsWith('cbrt', i) || s.startsWith('³√', i)) {
        i += c === '∛' ? 1 : (s.startsWith('cbrt', i) ? 4 : 2);
        skip();
        const arg = peek() === '(' ? (i++, join(group(')'))) : (primary() || { tex: '' }).tex;
        return { tex: '\\sqrt[3]{' + arg + '}', atom: true };
      }

      // Fourth root: ∜ or ⁴√
      if (c === '∜' || s.startsWith('⁴√', i)) {
        i += c === '∜' ? 1 : 2;
        skip();
        const arg = peek() === '(' ? (i++, join(group(')'))) : (primary() || { tex: '' }).tex;
        return { tex: '\\sqrt[4]{' + arg + '}', atom: true };
      }

      // N-th root: ⁿ√
      if (s.startsWith('ⁿ√', i)) {
        i += 2;
        skip();
        const arg = peek() === '(' ? (i++, join(group(')'))) : (primary() || { tex: '' }).tex;
        return { tex: '\\sqrt[n]{' + arg + '}', atom: true };
      }

      // Root notation if pasted as \sqrt[n]{...}
      if (s.startsWith('\\sqrt[', i)) {
        const closeB = s.indexOf(']', i + 6);
        if (closeB !== -1) {
          const deg = s.slice(i + 6, closeB);
          i = closeB + 1;
          skip();
          let arg = '';
          if (peek() === '{') {
            i++;
            const closeBrace = s.indexOf('}', i);
            if (closeBrace !== -1) {
              arg = s.slice(i, closeBrace);
              i = closeBrace + 1;
            }
          } else if (peek() === '(') {
            i++;
            arg = join(group(')'));
          } else {
            arg = (primary() || { tex: '' }).tex;
          }
          return { tex: '\\sqrt[' + deg + ']{' + arg + '}', atom: true };
        }
      }

      // Square root: √ or sqrt or \sqrt{...}
      if (s.startsWith('\\sqrt{', i)) {
        i += 6;
        const closeBrace = s.indexOf('}', i);
        if (closeBrace !== -1) {
          const arg = s.slice(i, closeBrace);
          i = closeBrace + 1;
          return { tex: '\\sqrt{' + arg + '}', atom: true };
        }
      }
      if (c === '√' || s.startsWith('sqrt', i)) {
        i += c === '√' ? 1 : 4;
        skip();
        const arg = peek() === '(' ? (i++, join(group(')'))) : (primary() || { tex: '' }).tex;
        return { tex: '\\sqrt{' + arg + '}', atom: true };
      }

      if (c === 'π') { i++; return { tex: '\\pi ', atom: true }; }

      let m = /^\d+(?:[.,]\d+)*/.exec(s.slice(i)) || /^\.\d+/.exec(s.slice(i));
      if (m) { i += m[0].length; return { tex: m[0].replace(/,/g, '{,}'), atom: true }; }

      m = /^[A-Za-z]+/.exec(s.slice(i));
      if (m) {
        i += m[0].length;
        return { tex: m[0] === 'pi' ? '\\pi ' : m[0], atom: true };
      }
      return null;
    }

    function atom() {
      const a = primary();
      if (!a) return null;
      for (;;) {
        if (peek() === '^') {
          i++;
          skip();
          let e;
          if (peek() === '(') { i++; e = join(group(')')); } else {
            const neg = peek() === '-' || peek() === '−' ? (i++, '-') : '';
            const p = primary();
            e = neg + (p ? p.tex : '');
          }
          a.tex = '{' + a.tex + '}^{' + e + '}';
          a.inner = null;
        } else if (peek() === '²' || peek() === '³' || peek() === '⁴') {
          const exp = peek() === '²' ? 2 : (peek() === '³' ? 3 : 4);
          a.tex = '{' + a.tex + '}^{' + exp + '}';
          a.inner = null;
          i++;
        } else if (peek() === '°') {
          a.tex += '^{\\circ}';
          a.inner = null;
          i++;
        } else return a;
      }
    }

    function seq(close) {
      const items = [];
      while (i < s.length && s[i] !== close) {
        const c = s[i];
        if (c === ' ') { i++; items.push({ tex: ' ' }); continue; }
        if (c === '/') {
          i++;
          let k = items.length - 1;
          while (k >= 0 && items[k].tex === ' ') k--;
          const num = k >= 0 && items[k].atom ? items[k] : null;
          const save = i;
          const den = atom();
          if (num && den) {
            items.splice(k);
            items.push({ tex: '\\frac{' + (num.inner != null ? num.inner : num.tex) + '}{' + (den.inner != null ? den.inner : den.tex) + '}', atom: true });
          } else {
            i = save;
            items.push({ tex: '/' });
          }
          continue;
        }
        const a = atom();
        if (a) { items.push(a); continue; }
        items.push({ tex: OPS[c] != null ? OPS[c] : LONE[c] != null ? LONE[c] : c });
        i++;
      }
      return items;
    }
    return join(seq(null)).trim();
  }
  Exam.mathTex = toTex;

  const esc = (t) => String(t).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const plainHtml = (t) => esc(t).replace(/\n/g, '<br>');

  // Auto-converts "worthwhile" plain-text math runs within a segment that has
  // no explicit delimiters; everything else stays escaped text.
  function autoHtml(segment) {
    let out = '';
    let last = 0;
    segment.replace(RUN, (run, at) => {
      const lead = run.length - run.trimStart().length;
      const body = run.trim().replace(/[.,;:!?]+$/, '');
      if (!isWorth(body)) return run;
      const start = at + lead;
      out += plainHtml(segment.slice(last, start));
      try {
        out += window.katex.renderToString(toTex(body), { throwOnError: false, strict: 'ignore' });
      } catch {
        out += esc(body);
      }
      last = start + body.length;
      return run;
    });
    out += plainHtml(segment.slice(last));
    return out;
  }

  // Full text -> safe HTML. Delimiters $$ $$, $ $, \[ \], \( \) are literal LaTeX / explicit math;
  // everything else is auto-converted plain-text math runs while preserving Khmer text.
  Exam.mathHtml = function (text) {
    const t = String(text == null ? '' : text);
    if (!window.katex) return plainHtml(t);
    const DELIM = /\$\$(.+?)\$\$|\$([^$\n]+?)\$|\\\[(.+?)\\\]|\\\((.+?)\\\)/gs;
    let out = '';
    let last = 0;
    t.replace(DELIM, (match, block1, inline1, block2, inline2, offset) => {
      const block = block1 || block2;
      const inline = inline1 || inline2;
      out += autoHtml(t.slice(last, offset));
      try {
        const tex = inline != null ? inline : block;
        out += window.katex.renderToString(tex, { throwOnError: false, strict: 'ignore', displayMode: Boolean(block) });
      } catch {
        out += esc(match);
      }
      last = offset + match.length;
      return match;
    });
    out += autoHtml(t.slice(last));
    return out;
  };

  // ------------------------------------------------------------ toolbar ---
  // [label as HTML, Khmer name/tooltip, text to insert; «|» marks the caret]
  const KEYS = [
    ['<i>f</i>(<i>x</i>)', 'គណិតវិទ្យា ($...$ Math Mode)', '$|$'],
    ['<span class="mk-frac"><i>a</i><i>b</i></span>', 'ប្រភាគ (Fraction)', '(|)/()'],
    ['<i>x</i><sup>2</sup>', 'ការេ (Square: ^2)', '^2'],
    ['<i>x</i><sup><i>n</i></sup>', 'ស្វ័យគុណ (Power: ^n)', '^(|)'],
    ['√', 'ឫសការេ (Square root: √)', '√(|)'],
    ['∛', 'ឫសគូប (Cube root: ∛)', '∛(|)'],
    ['<sup><i>n</i></sup>√', 'ឫសទី n (n-th root: ⁿ√)', 'ⁿ√(|)'],
    ['π', 'ភី (pi)', 'π'],
    ['×', 'គុណ', '×'],
    ['÷', 'ចែក', '÷'],
    ['±', 'បូក ឬដក', '±'],
    ['≤', 'តូចជាង ឬស្មើ', '≤'],
    ['≥', 'ធំជាង ឬស្មើ', '≥'],
    ['≠', 'មិនស្មើ', '≠'],
    ['≈', 'ប្រហែលស្មើ', '≈'],
    ['°', 'ដឺក្រេ', '°'],
  ];

  function insert(field, tpl) {
    if (!field) return;
    const a = field.selectionStart != null ? field.selectionStart : field.value.length;
    const b = field.selectionEnd != null ? field.selectionEnd : a;
    const sel = field.value.slice(a, b);
    let text = tpl.replace('|', '');
    let caret = tpl.indexOf('|') >= 0 ? tpl.indexOf('|') : text.length;
    if (sel && tpl.indexOf('|') >= 0) {
      text = tpl.replace('|', sel);
      const second = text.indexOf('()', tpl.indexOf('|') + sel.length);
      caret = second >= 0 ? second + 1 : text.length;
    }
    field.focus();
    field.setRangeText(text, a, b, 'end');
    field.setSelectionRange(a + caret, a + caret);
    field.dispatchEvent(new Event('input', { bubbles: true }));
  }

  // ---- extra symbols (LaTeX), grouped. «|» marks where the caret goes. Outside a \( \) / $ $ region they are wrapped in \( \) automatically. ----
  const SETS = [
    ['កាល់គុល', [
      ['\\int', 'អាំងតេក្រាលឥតកំណត់ ∫', '\\int | \\,dx'],
      ['\\int_a^b', 'អាំងតេក្រាលកំណត់ ∫ពី a ដល់ b', '\\int_{a}^{b} | \\,dx'],
      ['\\oint', 'អាំងតេក្រាលបិទ ∮', '\\oint |'],
      ['\\lim_{x\\to a}', 'លីមីត lim', '\\lim_{x \\to |} '],
      ['\\lim_{x\\to\\infty}', 'លីមីតនៅអនន្ត', '\\lim_{x \\to \\infty} |'],
      ['\\sum', 'ផលបូក Σ', '\\sum_{i=1}^{n} |'],
      ['\\prod', 'ផលគុណ Π', '\\prod_{i=1}^{n} |'],
      ['\\frac{d}{dx}', 'ដេរីវេ d/dx', '\\dfrac{d}{dx}(|)'],
      ["f'(x)", 'ដេរីវេ f′(x)', "f'(|)"],
      ['\\frac{\\partial}{\\partial x}', 'ដេរីវេដោយផ្នែក ∂', '\\dfrac{\\partial |}{\\partial x}'],
      ['\\infty', 'អនន្ត ∞', '\\infty '],
      ['\\Delta', 'ដែលតា Δ', '\\Delta '],
      ['\\nabla', 'ណាប្លា ∇', '\\nabla '],
      ['\\log_a', 'លោការីតគោល a', '\\log_{|}(\\,)'],
      ['\\ln', 'លោការីតនេពែ ln', '\\ln |'],
      ['e^{x}', 'e ស្វ័យគុណ', 'e^{|}'],
      ['\\sin', 'sin', '\\sin |'], ['\\cos', 'cos', '\\cos |'], ['\\tan', 'tan', '\\tan |'], ['\\cot', 'cot', '\\cot |'],
      ['\\left|x\\right|', 'តម្លៃដាច់ខាត |x|', '\\left| | \\right|'],
      ['\\lfloor x\\rfloor', 'ផ្នែកគត់ ⌊x⌋', '\\lfloor | \\rfloor'],
    ]],
    ['វ៉ិចទ័រ & ម៉ាទ្រីស', [
      ['\\vec{v}', 'វ៉ិចទ័រ v⃗', '\\vec{|}'],
      ['\\overrightarrow{AB}', 'វ៉ិចទ័រ AB (ព្រួញធំ)', '\\overrightarrow{|}'],
      ['\\overline{AB}', 'អង្កត់ត្រង់ AB (ឆ្នូតលើ)', '\\overline{|}'],
      ['\\widehat{ABC}', 'មុំ / ធ្នូ (មួក)', '\\widehat{|}'],
      ['\\|\\vec{v}\\|', 'ម៉ូឌុលវ៉ិចទ័រ ‖v⃗‖', '\\left\\|\\vec{|}\\right\\|'],
      ['\\vec{a}\\cdot\\vec{b}', 'ផលគុណស្កាឡែរ a⃗·b⃗', '\\vec{|}\\cdot\\vec{}'],
      ['\\vec{a}\\times\\vec{b}', 'ផលគុណវ៉ិចទ័រ a⃗×b⃗', '\\vec{|}\\times\\vec{}'],
      ['\\begin{pmatrix}a\\\\b\\end{pmatrix}', 'វ៉ិចទ័រជួរឈរ', '\\begin{pmatrix} | \\\\ \\end{pmatrix}'],
      ['\\begin{pmatrix}a&b\\\\c&d\\end{pmatrix}', 'ម៉ាទ្រីស 2×2', '\\begin{pmatrix} | & \\\\ & \\end{pmatrix}'],
      ['\\begin{vmatrix}a&b\\\\c&d\\end{vmatrix}', 'ដេទែមីណង់ 2×2', '\\begin{vmatrix} | & \\\\ & \\end{vmatrix}'],
      ['\\begin{cases}x\\\\y\\end{cases}', 'ប្រព័ន្ធសមីការ / ក្នុងករណី', '\\begin{cases} | \\\\ \\end{cases}'],
      ['\\binom{n}{k}', 'បន្សំ C(n,k)', '\\binom{|}{}'],
      ['n!', 'ហ្វាក់តូរីយែល n!', '|!'],
    ]],
    ['ធរណីមាត្រ', [
      ['\\angle', 'មុំ ∠', '\\angle '],
      ['\\triangle', 'ត្រីកោណ △', '\\triangle '],
      ['\\perp', 'កែង ⟂', '\\perp '],
      ['\\parallel', 'ស្រប ∥', '\\parallel '],
      ['\\cong', 'ដូចគ្នាទាំងអស់ ≅', '\\cong '],
      ['\\sim', 'ដូចគ្នា (រាងដូច) ∼', '\\sim '],
      ['\\overset{\\frown}{AB}', 'ធ្នូ AB', '\\overset{\\frown}{|}'],
      ['\\circ', 'ដឺក្រេ °', '^{\\circ}'],
      ["{}'", 'មីនុត ′', "'"],
      ["{}''", 'សេកុង ″', "''"],
      ['\\odot', 'រង្វង់ ⊙', '\\odot '],
      ['\\square', 'ការ៉េ □', '\\square '],
    ]],
    ['សំណុំ & តក្កវិជ្ជា', [
      ['\\in', 'ជាធាតុនៃ ∈', '\\in '], ['\\notin', 'មិនមែនជាធាតុនៃ ∉', '\\notin '],
      ['\\subset', 'សំណុំរងពិត ⊂', '\\subset '], ['\\subseteq', 'សំណុំរង ⊆', '\\subseteq '],
      ['\\cup', 'ប្រជុំ ∪', '\\cup '], ['\\cap', 'ប្រសព្វ ∩', '\\cap '], ['\\emptyset', 'សំណុំទទេ ∅', '\\emptyset '],
      ['\\mathbb{R}', 'ចំនួនពិត ℝ', '\\mathbb{R}'], ['\\mathbb{N}', 'ចំនួនធម្មជាតិ ℕ', '\\mathbb{N}'],
      ['\\mathbb{Z}', 'ចំនួនគត់ ℤ', '\\mathbb{Z}'], ['\\mathbb{Q}', 'ចំនួនសនិទាន ℚ', '\\mathbb{Q}'], ['\\mathbb{C}', 'ចំនួនកុំផ្លិច ℂ', '\\mathbb{C}'],
      ['\\forall', 'គ្រប់ ∀', '\\forall '], ['\\exists', 'មាន ∃', '\\exists '],
      ['\\Rightarrow', 'នាំឱ្យ ⇒', '\\Rightarrow '], ['\\Leftrightarrow', 'សមមូល ⇔', '\\Leftrightarrow '],
      ['\\neg', 'ប្រកែក ¬', '\\neg '], ['\\wedge', 'និង ∧', '\\wedge '], ['\\vee', 'ឬ ∨', '\\vee '],
      ['\\{\\ \\}', 'សំណុំ { }', '\\{ | \\}'],
    ]],
    ['អក្សរក្រិក', ['alpha', 'beta', 'gamma', 'delta', 'epsilon', 'theta', 'lambda', 'mu', 'rho', 'sigma', 'tau', 'varphi', 'omega', 'Delta', 'Sigma', 'Omega', 'Pi', 'Theta']
      .map((n) => ['\\' + n, n, '\\' + n + ' '])],
    ['ព្រួញ & ផ្សេងៗ', [
      ['\\rightarrow', 'ព្រួញស្តាំ →', '\\rightarrow '], ['\\leftarrow', 'ព្រួញឆ្វេង ←', '\\leftarrow '],
      ['\\leftrightarrow', 'ព្រួញទ្វេ ↔', '\\leftrightarrow '], ['\\uparrow', '↑', '\\uparrow '], ['\\downarrow', '↓', '\\downarrow '],
      ['\\therefore', 'ដូចនេះ ∴', '\\therefore '], ['\\because', 'ព្រោះ ∵', '\\because '],
      ['\\propto', 'សមាមាត្រនឹង ∝', '\\propto '], ['\\equiv', 'សមមូល ≡', '\\equiv '],
      ['\\ll', 'តូចជាងឆ្ងាយ ≪', '\\ll '], ['\\gg', 'ធំជាងឆ្ងាយ ≫', '\\gg '], ['\\cdots', 'ចំណុចបន្ត ⋯', '\\cdots '],
      ['\\dfrac{a}{b}', 'ប្រភាគធំ', '\\dfrac{|}{}'],
      ['x_{n}', 'សន្ទស្សន៍ក្រោម x₍ₙ₎', '_{|}'], ['x^{n}', 'ស្វ័យគុណ xⁿ', '^{|}'],
      ['\\underline{x}', 'គូសក្រោម', '\\underline{|}'], ['\\text{ក}', 'អត្ថបទខ្មែរក្នុងរូបមន្ត', '\\text{|}'],
      ['\\%', 'ភាគរយ %', '\\%'], ['\\mathrm{cm}^2', 'cm²', '\\mathrm{cm}^{2}'], ['\\mathrm{m}^3', 'm³', '\\mathrm{m}^{3}'],
    ]],
  ];

  // Is the caret inside an open \( .. \), \[ .. \], $ .. $ or $$ .. $$ ?
  function insideMath(v, pos) {
    let close = null;
    for (let i = 0; i < pos; i++) {
      if (close) {
        if (v.startsWith(close, i)) { i += close.length - 1; close = null; }
        continue;
      }
      if (v.startsWith('\\(', i)) { close = '\\)'; i += 1; }
      else if (v.startsWith('\\[', i)) { close = '\\]'; i += 1; }
      else if (v.startsWith('$$', i)) { close = '$$'; i += 1; }
      else if (v[i] === '$') { close = '$'; }
    }
    return !!close;
  }

  function insertTex(field, tpl) {
    if (!field) return;
    const a = field.selectionStart != null ? field.selectionStart : field.value.length;
    const b = field.selectionEnd != null ? field.selectionEnd : a;
    const sel = field.value.slice(a, b);
    const bar = tpl.indexOf('|');
    let body = tpl.replace('|', sel);
    let caret = bar >= 0 ? bar + sel.length : body.length;
    if (!insideMath(field.value, a)) { body = '\\(' + body + '\\)'; caret += 2; }
    field.focus();
    field.setRangeText(body, a, b, 'end');
    field.setSelectionRange(a + caret, a + caret);
    field.dispatchEvent(new Event('input', { bubbles: true }));
  }

  // A toolbar whose buttons insert into whatever field getTarget() currently
  // returns — lets one toolbar serve several fields (e.g. a stem + options).
  Exam.mathBar = function (getTarget) {
    const bar = h('div', { class: 'mathbar' });
    KEYS.forEach(([label, name, tpl]) => {
      const b = h('button', {
        type: 'button', class: 'mk', title: name, 'aria-label': name,
        onmousedown: (e) => e.preventDefault(),
        onclick: () => insert(getTarget(), tpl),
      });
      b.innerHTML = label;
      bar.append(b);
    });
    // more symbols: vectors, integrals, limits, sets, Greek letters…
    const panel = h('div', { class: 'mk-more', hidden: true });
    const grid = h('div', { class: 'mk-grid' });
    const tabs = h('div', { class: 'mk-tabs', role: 'tablist' });
    const render = (idx) => {
      [...tabs.children].forEach((t, i) => { t.classList.toggle('on', i === idx); t.setAttribute('aria-selected', String(i === idx)); });
      grid.innerHTML = '';
      SETS[idx][1].forEach(([tex, name, tpl]) => {
        const k = h('button', { type: 'button', class: 'mk mk-tex', title: name, 'aria-label': name, onmousedown: (e) => e.preventDefault(), onclick: () => insertTex(getTarget(), tpl) });
        try { k.innerHTML = window.katex ? window.katex.renderToString(tex, { throwOnError: false, strict: 'ignore' }) : tex; } catch { k.textContent = name; }
        grid.append(k);
      });
    };
    SETS.forEach(([title], i) => tabs.append(h('button', { type: 'button', class: 'mk-tab', role: 'tab', onmousedown: (e) => e.preventDefault(), onclick: () => render(i) }, title)));
    panel.append(tabs, grid);
    render(0);
    const more = h('button', { type: 'button', class: 'mk mk-morebtn', title: 'និមិត្តសញ្ញាគណិតវិទ្យាច្រើនទៀត', 'aria-expanded': 'false', onmousedown: (e) => e.preventDefault(), onclick: () => { panel.hidden = !panel.hidden; more.setAttribute('aria-expanded', String(!panel.hidden)); more.classList.toggle('on', !panel.hidden); } }, '∫ ∑ lim … ច្រើនទៀត ▾');
    bar.append(more, panel);
    return bar;
  };

  // A live preview under a field, showing what its current value renders as.
  Exam.mathPreview = function (field) {
    const pv = h('div', { class: 'mpv' });
    pv.hidden = true;
    const draw = () => {
      const val = (field.value || '').trim();
      const has = /[/^√∛∜π²³⁴°]|sqrt|cbrt|ⁿ√|\\\(|\\\[|\$|[=<>≤≥≠≈±]|\b[a-zA-Z]\b/.test(val);
      pv.hidden = !has;
      if (has) pv.innerHTML = '<span class="mpv-lbl">ទម្រង់គណិតវិទ្យា៖</span> ' + Exam.mathHtml(field.value);
    };
    field.addEventListener('input', draw);
    draw();
    return pv;
  };
})();
