/* khmermath.org — math in the apps of content/construct/apps/ is set like the lessons:
   variables in italic math (KaTeX_Math), numbers, signs and units upright (KaTeX_Main), the area 𝒜 in
   the calligraphic letter (KaTeX_Caligraphic, \mathcal{A} of the book) — never in the Khmer font.
   The app writes plain text; this script finds the math in every text node, in the HTML and in the SVG,
   and again after each change the app makes. Khmer words keep the Khmer font; a run of math next to them
   gets Latin digits, as in the lessons. Subscripts: 𝒜₁, 𝒜_B, 𝒜_ចម្រៀក (up to the next space). */
(function () {
  'use strict';
  var BASE = (function () {
    var s = document.currentScript && document.currentScript.src;
    return s ? s.replace(/js\/mathfix\.js.*$/, 'katex/fonts/') : '/static/katex/fonts/';
  })();
  function face(fam, file, w, st) {
    return "@font-face{font-family:'" + fam + "';src:url('" + BASE + file + ".woff2') format('woff2');font-weight:" + w + ";font-style:" + st + ";font-display:swap}";
  }
  var css = face('KMmath', 'KaTeX_Math-Italic', 400, 'italic') + face('KMmath', 'KaTeX_Math-BoldItalic', 700, 'italic') +
    face('KMmain', 'KaTeX_Main-Regular', 400, 'normal') + face('KMmain', 'KaTeX_Main-Bold', 700, 'normal') +
    face('KMcal', 'KaTeX_Caligraphic-Regular', 400, 'normal') + face('KMcal', 'KaTeX_Caligraphic-Bold', 700, 'normal') +
    ".mf .mv{font-family:'KMmath','Times New Roman','STIX Two Text',serif!important;font-style:italic!important}" +
    ".mf .mn{font-family:'KMmain','Times New Roman','STIX Two Text',serif!important;font-style:normal!important}" +
    ".mf .mc{font-family:'KMcal','Times New Roman',serif!important;font-style:normal!important}" +
    ".mf sub.ms{font-size:.72em;line-height:0;vertical-align:-.25em}";
  var st = document.createElement('style');
  st.textContent = css;
  document.head.appendChild(st);

  var KHD = '០១២៣៤៥៦៧៨៩', SUBD = '₀₁₂₃₄₅₆₇₈₉';
  var SVGNS = 'http://www.w3.org/2000/svg';
  // prose = Khmer letters and signs (not the Khmer digits); everything else is a candidate for math
  var SPLIT = /(𝒜_(?:[ក-៟]+|△[A-Za-z]*|[A-Za-z]+))|((?:(?!𝒜_(?:[ក-៟]|△|[A-Za-z]))[^ក-៟៰-៿])+)/g;
  var TRIG = /[A-Za-z=+−×÷<>≠≈≤≥∥⊥∠△°²³½¼¾π√θαβφΔ∘′″%𝒜]/;
  var UNIT = /^(?:cm|mm|dm|km|kg|ha|sin|cos|tan)(?![A-Za-z])/;
  var TOKEN = /𝒜([₀-₉]+)?|[A-Za-zθαβφΔπ][′']*([₀-₉]+)?|[^A-Za-zθαβφΔπ𝒜₀-₉]+|[₀-₉]+/g;

  function toLatin(s) { return s.replace(/[០-៩]/g, function (c) { return KHD.indexOf(c); }); }
  function subOf(s) { return s.replace(/[₀-₉]/g, function (c) { return SUBD.indexOf(c); }); }

  function build(pieces, svg) {
    var wrap = svg ? document.createElementNS(SVGNS, 'tspan') : document.createElement('span');
    wrap.setAttribute('class', 'mf');
    function add(cls, txt, sub) {
      var e;
      if (sub) {
        if (svg) {
          e = document.createElementNS(SVGNS, 'tspan');
          e.setAttribute('class', cls);
          e.setAttribute('dy', '0.28em');
          e.setAttribute('font-size', '72%');
        } else { e = document.createElement('sub'); e.className = 'ms ' + cls; }
        e.textContent = txt;
        wrap.appendChild(e);
        if (svg) {
          var back = document.createElementNS(SVGNS, 'tspan');
          back.setAttribute('dy', '-0.28em'); back.setAttribute('font-size', '1');
          back.textContent = '​';
          wrap.appendChild(back);
        }
        return;
      }
      if (!cls) { wrap.appendChild(document.createTextNode(txt)); return; }
      e = svg ? document.createElementNS(SVGNS, 'tspan') : document.createElement('span');
      e.setAttribute('class', cls);
      e.textContent = txt;
      wrap.appendChild(e);
    }
    pieces.forEach(function (p) { add(p[0], p[1], p[2]); });
    return wrap;
  }

  function mathPieces(run) {
    var out = [], m;
    TOKEN.lastIndex = 0;
    var s = toLatin(run);
    while ((m = TOKEN.exec(s))) {
      var t = m[0];
      if (t.indexOf('𝒜') === 0) {
        out.push(['mc', 'A']);
        if (m[1]) out.push(['mn', subOf(m[1]), true]);
      } else if (/^[A-Za-zθαβφΔπ]/.test(t)) {
        var u = UNIT.exec(s.slice(m.index));
        if (u && (/^(?:sin|cos|tan)$/.test(u[0]) || /[0-9)]$/.test(s.slice(0, m.index).replace(/\s+$/, '')))) {
          out.push(['mn', u[0]]); TOKEN.lastIndex = m.index + u[0].length; continue;
        }
        var base = t.replace(/[₀-₉]+$/, '');
        out.push(['mv', base]);
        if (m[2]) out.push(['mv', subOf(m[2]), true]);
      } else if (/^[₀-₉]+$/.test(t)) {
        out.push(['mn', subOf(t), true]);
      } else {
        out.push(['mn', t]);
      }
    }
    return out;
  }

  function convert(text, svg, force) {
    var pieces = [], any = false, m;
    SPLIT.lastIndex = 0;
    var last = 0;
    while ((m = SPLIT.exec(text))) {
      if (m.index > last) pieces.push(['', text.slice(last, m.index)]);
      last = SPLIT.lastIndex;
      if (m[1]) {                                      // 𝒜 with a subscript word
        any = true;
        pieces.push(['mc', 'A']);
        pieces.push(['', m[1].slice(3), true]);
        continue;
      }
      var run = m[2], lead = /^\s*/.exec(run)[0], trail = /\s*$/.exec(run)[0];
      var core = run.slice(lead.length, run.length - trail.length);
      var tail = '';
      var k = /[.,;:]+$/.exec(core);
      if (k) { tail = k[0]; core = core.slice(0, core.length - tail.length); }
      if (!core || !(TRIG.test(core) || ((svg || force) && /[0-9០-៩]/.test(core)))) { pieces.push(['', run]); continue; }
      any = true;
      if (lead) pieces.push(['', lead]);
      mathPieces(core).forEach(function (p) { pieces.push(p); });
      if (tail || trail) pieces.push(['', tail + trail]);
    }
    if (last < text.length) pieces.push(['', text.slice(last)]);
    return any ? build(pieces, svg) : null;
  }

  var SKIP = /^(?:SCRIPT|STYLE|TEXTAREA|TITLE|NOSCRIPT|OPTION)$/;
  function inMf(n) {
    for (var e = n.parentNode; e && e.nodeType === 1; e = e.parentNode) {
      if (e.classList && (e.classList.contains('mf') || e.classList.contains('no-mf'))) return true;
      if (e.nodeName === 'HEAD') return true;
    }
    return false;
  }
  function fixText(n) {
    var p = n.parentNode;
    if (!p || SKIP.test(p.nodeName) || !n.nodeValue || !n.nodeValue.trim() || inMf(n)) return;
    var svg = p.namespaceURI === SVGNS && p.nodeName !== 'foreignObject';
    var r = convert(n.nodeValue, svg, !svg && !!(p.closest && p.closest('.tex')));
    if (r) p.replaceChild(r, n);
  }
  function walk(node) {
    if (node.nodeType === 3) { fixText(node); return; }
    if (node.nodeType !== 1 || SKIP.test(node.nodeName)) return;
    if (node.classList && (node.classList.contains('mf') || node.classList.contains('no-mf'))) return;
    var kids = Array.prototype.slice.call(node.childNodes);
    for (var i = 0; i < kids.length; i++) walk(kids[i]);
  }

  function start() {
    walk(document.body);
    new MutationObserver(function (list) {
      for (var i = 0; i < list.length; i++) {
        var r = list[i];
        if (r.type === 'characterData') { fixText(r.target); continue; }
        for (var j = 0; j < r.addedNodes.length; j++) walk(r.addedNodes[j]);
      }
    }).observe(document.body, { childList: true, characterData: true, subtree: true });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
