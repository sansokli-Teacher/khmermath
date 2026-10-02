// Typing mathematics in a text field — ported from the PISA CBA app's
// js/mathtype.js (same project family, same approach).
//
// A teacher can type plain text — 3/4, x^2, 2^(n+1), √20, π — and it renders
// as real math automatically wherever it's displayed. They can also paste
// ready-made LaTeX wrapped in \( \) or \[ \]; that is rendered literally,
// untouched by the plain-text parser, so both styles of input work side by
// side in the same field.
(function () {
  'use strict';
  const { h } = Exam;

  const latin = (str) => String(str == null ? '' : str).replace(/[០-៩]/g, (c) => String(c.charCodeAt(0) - 0x17e0));

  // A run of characters that could belong to a piece of mathematics.
  const RUN = /[0-9០-៩A-Za-z.,+\-−×÷*·/^()[\]=<>≤≥≠≈±π√°%²³ ]+/g;
  // Only draw a run as math when doing so would change something: a
  // fraction, a power, a root, or π next to a number/letter.
  const WORTH = (t) => /[/^√π²³]|sqrt/.test(t) && /[0-9០-៩A-Za-zπ]/.test(t);
  const OPS = {
    '×': '\\times ', '*': '\\times ', '·': '\\cdot ', '÷': '\\div ', '−': '-', '≤': '\\le ', '≥': '\\ge ',
    '≠': '\\ne ', '≈': '\\approx ', '±': '\\pm ', '%': '\\%', '<': '<', '>': '>', '=': '=', '+': '+', '-': '-',
  };
  const LONE = { '^': '\\text{\\textasciicircum}', '°': '{}^{\\circ}', '²': '{}^{2}', '³': '{}^{3}' };

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
      if (c === '(' || c === '[') {
        i++;
        const close = c === '(' ? ')' : ']';
        const inner = join(group(close));
        return { tex: '\\left' + c + inner + '\\right' + close, inner, atom: true };
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
        } else if (peek() === '²' || peek() === '³') {
          a.tex = '{' + a.tex + '}^{' + (peek() === '²' ? 2 : 3) + '}';
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
  // no explicit \( \) / \[ \] delimiters; everything else stays escaped text.
  function autoHtml(segment) {
    let out = '';
    let last = 0;
    segment.replace(RUN, (run, at) => {
      const lead = run.length - run.trimStart().length;
      const body = run.trim().replace(/[.,]$/, '');
      if (!WORTH(body)) return run;
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

  // Full text → safe HTML. Explicit \( \) / \[ \] are literal LaTeX (for a
  // teacher who pastes ready-made LaTeX); everything else is auto-converted
  // plain-text math. Always returns a string — plain Khmer text with nothing
  // mathematical in it just comes back escaped, unchanged.
  Exam.mathHtml = function (text) {
    const t = String(text == null ? '' : text);
    if (!window.katex) return plainHtml(t);
    const DELIM = /\\\((.+?)\\\)|\\\[(.+?)\\\]/gs;
    let out = '';
    let last = 0;
    t.replace(DELIM, (match, inline, block, offset) => {
      out += autoHtml(t.slice(last, offset));
      try {
        out += window.katex.renderToString(inline != null ? inline : block, { throwOnError: false, strict: 'ignore', displayMode: block != null });
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
    ['<span class="mk-frac"><i>a</i><i>b</i></span>', 'ប្រភាគ', '(|)/()'],
    ['x<sup>2</sup>', 'ការេ', '^2'],
    ['x<sup>n</sup>', 'ស្វ័យគុណ', '^(|)'],
    ['√', 'ឫសការេ', '√(|)'],
    ['π', 'ភី', 'π'],
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
      const has = /[/^√π²³]|sqrt|\\\(|\\\[/.test(field.value);
      pv.hidden = !has;
      if (has) pv.innerHTML = '<span class="mpv-lbl">ទម្រង់គណិតវិទ្យា៖</span> ' + Exam.mathHtml(field.value);
    };
    field.addEventListener('input', draw);
    draw();
    return pv;
  };
})();
