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
