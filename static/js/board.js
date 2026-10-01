/* khmermath.org — «ក្ដារខៀនធរណីមាត្រ» (construct/board.html): a sheet of squared paper
 * with a ruler and a compass that are used like the real ones.
 *
 * The page holds the buttons and every Khmer word (the hints are data-hint on the
 * buttons); this file draws the sheet and the tools, with the helpers of construct.js
 * (window.KMGeo, loaded before this file).
 *
 * One unit of the sheet is one CSS pixel, so that a handle is as large under a finger
 * as it is drawn; 40 units are 1 cm on the ruler. The drawing is
 *   doc = { pts: [{ p, name }], segs: [{ a, b, full }], arcs: [{ c, r, t1, t2 }] }
 * (full: the whole line through a and b; an arc runs from angle t1 up to t2). Every
 * change goes through commit(), which keeps the history for undo and redo. The ink is
 * drawn with attributes and not with classes: the picture that is saved is this SVG
 * without the tools, and a picture does not read the style sheet.
 *
 * Handles and new points go to the points and crossings near them (snap()); the ruler
 * draws on the line through its two marks exactly, so a line laid on two crossings
 * passes through them.
 */
(function () {
  'use strict';
  var root = document.getElementById('board'), G = window.KMGeo;
  if (!root || !G) return;
  var el = G.el, add = G.add, sub = G.sub, mul = G.mul, len = G.len, unit = G.unit;
  var CM = 40, SNAP = 14, KEY = 'km-board-v1', TAU = 2 * Math.PI;
  var RW = 58, EXT = 60, GRIP = 34;          // the ruler: width, length beyond its marks, where the knobs sit
  var PAPER = '#fffefa', INK = '#132238', BLUE = '#2d6aa8';

  var doc = { pts: [], segs: [], arcs: [] };
  var st = { tool: 'point', cmode: 'set', grid: true, marks: true, dots: true, full: true, ruler: null, compass: null };
  var hist = [], hi = 0, cands = [], W = 0, H = 0;
  var drag = null, mark = null, sel = -1;

  var stage = root.querySelector('.bd-stage');
  var hint = root.querySelector('.bd-hint');
  var nameForm = root.querySelector('.bd-name'), nameIn = nameForm.querySelector('input');
  var confirmBox = root.querySelector('.bd-confirm');
  var q = function (s) { return root.querySelector(s); };
  var all = function (s) { return Array.prototype.slice.call(root.querySelectorAll(s)); };

  var svg = el('svg', { class: 'bd-svg', role: 'img', 'aria-label': root.getAttribute('data-label') || '' });
  stage.innerHTML = '';
  stage.appendChild(svg);
  var paper = el('g', {}, svg), ink = el('g', {}, svg), live = el('g', {}, svg), tools = el('g', {}, svg);
  function clear(g) { while (g.firstChild) g.removeChild(g.firstChild); }

  var dot = function (a, b) { return a[0] * b[0] + a[1] * b[1]; };
  var cross = function (a, b) { return a[0] * b[1] - a[1] * b[0]; };
  var ang = function (c, p) { return Math.atan2(p[1] - c[1], p[0] - c[0]); };
  var polar = function (c, r, t) { return [c[0] + r * Math.cos(t), c[1] + r * Math.sin(t)]; };
  var inView = function (p) { return p[0] >= 0 && p[0] <= W && p[1] >= 0 && p[1] <= H; };
  var clamp = function (p) { return [Math.min(Math.max(p[0], 6), W - 6), Math.min(Math.max(p[1], 6), H - 6)]; };
  var f1 = function (x) { return x.toFixed(1); };

  // ------------------------------------------------ crossings, snapping ---
  function inSeg(s, t) {
    if (s.full) return true;
    var e = 1.5 / len(sub(s.b, s.a));
    return t >= -e && t <= 1 + e;
  }
  function onArc(a, t) {
    var span = a.t2 - a.t1, slack = 2 / a.r;
    if (span >= TAU - 1e-3) return true;
    var x = (t - a.t1) % TAU;
    if (x < 0) x += TAU;
    return x <= span + slack || x >= TAU - slack;
  }
  function lineLine(s1, s2) {
    var d1 = sub(s1.b, s1.a), d2 = sub(s2.b, s2.a), den = cross(d1, d2);
    if (Math.abs(den) < 1e-6 * len(d1) * len(d2)) return [];
    var w = sub(s2.a, s1.a), t = cross(w, d2) / den, u = cross(w, d1) / den;
    return inSeg(s1, t) && inSeg(s2, u) ? [add(s1.a, mul(d1, t))] : [];
  }
  function lineArc(s, a) {
    var d = sub(s.b, s.a), L = len(d), u = mul(d, 1 / L), w = sub(a.c, s.a);
    var tm = dot(w, u), h2 = a.r * a.r - (dot(w, w) - tm * tm);
    if (h2 < -a.r) return [];                              // more than half a pixel away from touching
    var h = Math.sqrt(Math.max(h2, 0));
    return [tm - h, tm + h].map(function (t) { return inSeg(s, t / L) ? add(s.a, mul(u, t)) : null; })
      .filter(function (p) { return p && onArc(a, ang(a.c, p)); });
  }
  function arcArc(a, b) {
    var w = sub(b.c, a.c), d = len(w);
    if (d < 1e-6 || d > a.r + b.r + 0.5 || d < Math.abs(a.r - b.r) - 0.5) return [];
    var x = (d * d + a.r * a.r - b.r * b.r) / (2 * d), h = Math.sqrt(Math.max(a.r * a.r - x * x, 0));
    var u = mul(w, 1 / d), m = add(a.c, mul(u, x)), n = [-u[1], u[0]];
    return [add(m, mul(n, h)), add(m, mul(n, -h))].filter(function (p) { return onArc(a, ang(a.c, p)) && onArc(b, ang(b.c, p)); });
  }
  // where a handle may go: the named points first (k: 0), then ends and crossings (k: 1; x: a crossing)
  function findCands() {
    var out = [], S = doc.segs, A = doc.arcs, i, j;
    var put = function (p) { out.push({ p: p, k: 1 }); };
    var meet = function (p) { out.push({ p: p, k: 1, x: 1 }); };
    doc.pts.forEach(function (o) { out.push({ p: o.p, k: 0 }); });
    S.forEach(function (s) { if (!s.full) { put(s.a); put(s.b); } });
    for (i = 0; i < S.length; i++) {
      for (j = i + 1; j < S.length; j++) lineLine(S[i], S[j]).forEach(meet);
      for (j = 0; j < A.length; j++) lineArc(S[i], A[j]).forEach(meet);
    }
    for (i = 0; i < A.length; i++) for (j = i + 1; j < A.length; j++) arcArc(A[i], A[j]).forEach(meet);
    cands = out;
  }
  // the place for p: a point or a crossing within SNAP, else the nearest spot on a line or an arc
  function snap(p) {
    var best = null, bd = SNAP, bk = 9;
    cands.forEach(function (c) {
      var d = len(sub(c.p, p));
      if (d <= SNAP && (c.k < bk || (c.k === bk && d < bd))) { best = c.p; bd = d; bk = c.k; }
    });
    if (best) return { p: best.slice(), hit: true };
    var near = null, nd = 10;
    var take = function (x) { var d = len(sub(x, p)); if (d < nd) { near = x; nd = d; } };
    doc.segs.forEach(function (s) {
      var L = len(sub(s.b, s.a)), u = unit(sub(s.b, s.a)), t = dot(sub(p, s.a), u);
      if (!s.full) t = Math.min(Math.max(t, 0), L);
      take(add(s.a, mul(u, t)));
    });
    doc.arcs.forEach(function (a) { var t = ang(a.c, p); if (onArc(a, t)) take(polar(a.c, a.r, t)); });
    return near ? { p: near, hit: true } : { p: p, hit: false };
  }

  // ------------------------------------------------------------ the ink ---
  function drawPaper() {
    clear(paper);
    var thin = '', bold = '', x, y;
    for (x = 20; x < W; x += 20) { if (x % 100) thin += 'M' + x + ' 0V' + H; else bold += 'M' + x + ' 0V' + H; }
    for (y = 20; y < H; y += 20) { if (y % 100) thin += 'M0 ' + y + 'H' + W; else bold += 'M0 ' + y + 'H' + W; }
    el('path', { d: thin, stroke: '#e3ebf3', 'stroke-width': 1, fill: 'none' }, paper);
    el('path', { d: bold, stroke: '#cfdbe8', 'stroke-width': 1, fill: 'none' }, paper);
    paper.style.display = st.grid ? '' : 'none';
  }
  function inkSeg(g, a, b, full) {
    if (full) { var d = unit(sub(b, a)); a = add(a, mul(d, -4000)); b = add(b, mul(d, 4000)); }
    el('line', { x1: f1(a[0]), y1: f1(a[1]), x2: f1(b[0]), y2: f1(b[1]), stroke: INK, 'stroke-width': 2.6, 'stroke-linecap': 'round' }, g);
  }
  function inkArc(g, c, r, t1, t2) {
    var look = { fill: 'none', stroke: BLUE, 'stroke-width': 2.2, 'stroke-linecap': 'round' };
    if (t2 - t1 >= TAU - 1e-3) { look.cx = f1(c[0]); look.cy = f1(c[1]); look.r = f1(r); el('circle', look, g); return; }
    var p = polar(c, r, t1), e = polar(c, r, t2);
    look.d = 'M' + f1(p[0]) + ' ' + f1(p[1]) + 'A' + f1(r) + ' ' + f1(r) + ' 0 ' + (t2 - t1 > Math.PI ? 1 : 0) + ' 1 ' + f1(e[0]) + ' ' + f1(e[1]);
    el('path', look, g);
  }
  function renderInk() {
    clear(ink);
    doc.segs.forEach(function (s) { inkSeg(ink, s.a, s.b, s.full); });
    doc.arcs.forEach(function (a) { inkArc(ink, a.c, a.r, a.t1, a.t2); });
    doc.pts.forEach(function (o, i) {
      el('circle', { cx: f1(o.p[0]), cy: f1(o.p[1]), r: 4.5, fill: i === sel ? '#c9862b' : INK }, ink);
      var t = el('text', { x: f1(o.p[0] + 12), y: f1(o.p[1] - 13), fill: INK, stroke: PAPER, 'stroke-width': 5, 'stroke-linejoin': 'round',
        'paint-order': 'stroke', 'font-family': "'Times New Roman', 'STIX Two Text', serif", 'font-size': 21, 'font-style': 'italic', 'font-weight': 700,
        'text-anchor': 'middle', 'dominant-baseline': 'central' }, ink);
      t.textContent = o.name;
    });
  }

  // ---------------------------------------------------------- the tools ---
  function rulerFrame() {
    var a = st.ruler.a, b = st.ruler.b, d = unit(sub(b, a));
    return { a: a, b: b, d: d, n: [-d[1], d[0]], L: len(sub(b, a)) };
  }
  function drawRulerTool() {
    var f = rulerFrame(), a = f.a, b = f.b, d = f.d, n = f.n, L = f.L;
    var p0 = add(a, mul(d, -EXT)), p1 = add(b, mul(d, EXT));
    var pts = [p0, p1, add(p1, mul(n, RW)), add(p0, mul(n, RW))].map(function (x) { return f1(x[0]) + ',' + f1(x[1]); }).join(' ');
    el('polygon', { points: pts, class: 'cx-ruler bd-ruler', 'data-h': 'rbody' }, tools);
    if (st.marks) {
      var deg = Math.atan2(d[1], d[0]) * 180 / Math.PI + (d[0] < 0 ? 180 : 0);
      for (var s = 0; s <= L + EXT - 8; s += CM / 2) {
        var t = add(a, mul(d, s)), cm = s % CM === 0, k = cm ? 14 : 8;
        el('line', { x1: f1(t[0]), y1: f1(t[1]), x2: f1(t[0] + n[0] * k), y2: f1(t[1] + n[1] * k), class: 'cx-ruler-tick' }, tools);
        if (cm) {
          var at = add(t, mul(n, 24));
          el('text', { x: f1(at[0]), y: f1(at[1]), class: 'bd-num', transform: 'rotate(' + f1(deg) + ' ' + f1(at[0]) + ' ' + f1(at[1]) + ')' }, tools).textContent = s / CM;
        }
      }
    }
    el('line', { x1: f1(p0[0]), y1: f1(p0[1]), x2: f1(p1[0]), y2: f1(p1[1]), class: 'bd-edge-line' }, tools);
    var e0 = add(p0, mul(n, -8)), e1 = add(p1, mul(n, -8));
    el('line', { x1: f1(e0[0]), y1: f1(e0[1]), x2: f1(e1[0]), y2: f1(e1[1]), class: 'bd-edge', 'data-h': 'redge' }, tools);
    // the knobs sit on the ruler, away from its edge, so that the edge stays free to draw along
    var apart = Math.max(0, (50 - L) / 2);
    [['ra', a, -apart], ['rb', b, apart]].forEach(function (o) {
      var g = add(add(o[1], mul(n, GRIP)), mul(d, o[2]));
      el('circle', { cx: f1(o[1][0]), cy: f1(o[1][1]), r: 4, class: 'bd-anchor' }, tools);
      el('line', { x1: f1(o[1][0]), y1: f1(o[1][1]), x2: f1(g[0]), y2: f1(g[1]), class: 'bd-stem' }, tools);
      el('circle', { cx: f1(g[0]), cy: f1(g[1]), r: 13, class: 'bd-grip' }, tools);
      el('circle', { cx: f1(g[0]), cy: f1(g[1]), r: 22, class: 'bd-hit', 'data-h': o[0] }, tools);
    });
  }
  function drawCompassTool() {
    var c = st.compass.c, e = st.compass.e, on = st.cmode === 'draw';
    var hinge = G.drawCompass(tools, c, e);
    if (st.marks) {
      var m = mul(add(c, e), 0.5);
      el('text', { x: f1(m[0]), y: f1(Math.max(c[1], e[1]) + 30), class: 'bd-open' }, tools).textContent = 'r = ' + (len(sub(e, c)) / CM).toFixed(1) + ' cm';
    }
    el('circle', { cx: f1(c[0]), cy: f1(c[1]), r: 15, class: 'bd-ring' }, tools);
    el('circle', { cx: f1(e[0]), cy: f1(e[1]), r: 15, class: 'bd-ring bd-ring-p' + (on ? ' on' : '') }, tools);
    el('circle', { cx: f1(c[0]), cy: f1(c[1]), r: 22, class: 'bd-hit', 'data-h': 'needle' }, tools);
    el('circle', { cx: f1(hinge[0]), cy: f1(hinge[1]), r: 22, class: 'bd-hit', 'data-h': 'hinge' }, tools);
    el('circle', { cx: f1(e[0]), cy: f1(e[1]), r: 22, class: 'bd-hit', 'data-h': 'pencil' }, tools);
  }
  // the crossings, as blue dots: where the ruler, the needle or a new point can be put exactly.
  // They belong to the tools, not to the picture, and a crossing that has a name is not shown twice.
  function drawCrossings() {
    var seen = doc.pts.map(function (o) { return o.p; });
    cands.forEach(function (c) {
      if (!c.x || !inView(c.p) || seen.some(function (s) { return len(sub(s, c.p)) < 2; })) return;
      seen.push(c.p);
      el('circle', { cx: f1(c.p[0]), cy: f1(c.p[1]), r: 5, class: 'bd-cross' }, tools);
    });
  }
  function renderTools() {
    clear(tools);
    if (st.tool === 'ruler') drawRulerTool();
    if (st.tool === 'compass') drawCompassTool();
    if (st.dots && st.tool !== 'name') drawCrossings();             // on top: a crossing stays blue under the ruler's mark
    if (mark) el('circle', { cx: f1(mark[0]), cy: f1(mark[1]), r: 9, class: 'bd-snap' }, tools);
  }
  // a tool that was never placed, or is in use and off the sheet (a smaller sheet), goes to its first place
  function placeTools() {
    var r = st.ruler, c = st.compass, y = Math.round(H * 0.62 / 20) * 20, x = Math.max(60, Math.round(W * 0.16 / 20) * 20);
    if (!r || !r.a || !r.b || (st.tool === 'ruler' && !(inView(r.a) && inView(r.b)))) st.ruler = { a: [x, y], b: [Math.min(x + 240, W - 70), y] };
    if (!c || !c.c || !c.e || (st.tool === 'compass' && !(inView(c.c) && inView(c.e)))) st.compass = { c: [x + 20, y - 100], e: [x + 100, y - 100] };
  }

  // -------------------------------------------- history, keeping, state ---
  function save() {
    try { localStorage.setItem(KEY, JSON.stringify({ doc: doc, st: st })); } catch (x) { /* works without it */ }
  }
  function load() {
    try {
      var o = JSON.parse(localStorage.getItem(KEY));
      if (o && o.doc && Array.isArray(o.doc.pts) && Array.isArray(o.doc.segs) && Array.isArray(o.doc.arcs)) doc = o.doc;
      if (o && o.st) for (var k in st) if (o.st[k] != null && typeof o.st[k] === typeof (st[k] == null ? {} : st[k])) st[k] = o.st[k];
    } catch (x) { /* a fresh sheet */ }
  }
  function changed() { findCands(); renderInk(); renderTools(); buttons(); save(); }
  function commit(change) {
    change();
    hist = hist.slice(0, hi + 1);
    hist.push(JSON.stringify(doc));
    hi = hist.length - 1;
    changed();
  }
  function travel(by) {
    if (hi + by < 0 || hi + by >= hist.length) return;
    hi += by;
    doc = JSON.parse(hist[hi]);
    pick(-1);
    changed();
  }
  function nextName() {
    var used = {}, i, p;
    doc.pts.forEach(function (o) { used[o.name] = 1; });
    for (p = 0; p < 4; p++) for (i = 0; i < 26; i++) {
      var s = String.fromCharCode(65 + i) + '′′′'.slice(0, p);
      if (!used[s]) return s;
    }
    return '?';
  }

  function buttons() {
    q('[data-act="undo"]').disabled = hi === 0;
    q('[data-act="redo"]').disabled = hi === hist.length - 1;
    q('[data-act="clear"]').disabled = !(doc.pts.length || doc.segs.length || doc.arcs.length);
  }
  function setTool(tool) {
    st.tool = tool;
    all('.bd-tool').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-tool') === tool)); });
    all('[data-cmode]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-cmode') === st.cmode)); });
    all('.bd-opt[data-for]').forEach(function (o) { o.hidden = o.getAttribute('data-for') !== tool; });
    confirmBox.hidden = true;
    var src = tool === 'compass' ? q('[data-cmode="' + st.cmode + '"]') : q('.bd-tool[data-tool="' + tool + '"]');
    hint.textContent = src.getAttribute('data-hint') || '';
    root.setAttribute('data-tool', tool);
    mark = null;
    pick(-1);
    placeTools();
    renderTools();
    save();
    size();
  }
  // the board takes the whole window (the way it opens), or sits in the page
  function setFull(on) {
    st.full = !!on;
    root.classList.toggle('full', st.full);
    document.documentElement.classList.toggle('bd-full-on', st.full);
    var b = q('[data-act="full"]'), word = b.getAttribute(st.full ? 'data-on' : 'data-off');
    b.setAttribute('aria-pressed', String(st.full));
    b.setAttribute('aria-label', word);
    b.querySelector('.bd-lbl').textContent = word;
    W = 0;
    size();
    save();
  }
  // the point whose name is being changed
  function pick(i) {
    var was = sel;
    sel = i;
    nameIn.disabled = nameForm.querySelector('button').disabled = i < 0;
    nameIn.value = i < 0 ? '' : doc.pts[i].name;
    if (was !== sel) renderInk();
  }

  // ------------------------------------------------------ taking a drag ---
  function toSvg(e) {
    var r = svg.getBoundingClientRect();
    return [(e.clientX - r.left) * W / r.width, (e.clientY - r.top) * H / r.height];
  }
  // along the ruler's edge: t counted from its first mark, pulled onto what lies on the edge
  function snapT(f, t) {
    var best = null, bd = SNAP;
    var see = function (tc) { var d = Math.abs(tc - t); if (d <= bd) { best = tc; bd = d; } };
    see(0); see(f.L);
    cands.forEach(function (c) { var w = sub(c.p, f.a); if (Math.abs(cross(w, f.d)) < 1.5) see(dot(w, f.d)); });
    return Math.min(Math.max(best == null ? t : best, -EXT), f.L + EXT);
  }
  function moveCompass(to) {
    var v = sub(st.compass.e, st.compass.c), s = snap(clamp(to));
    st.compass.c = s.p;
    st.compass.e = add(s.p, v);                          // the opening is kept
    mark = s.hit ? s.p : null;
    keepPencil();
  }
  // the pencil stays on the sheet, where it can be taken again: the compass turns about its needle, its opening kept
  function keepPencil() {
    var c = st.compass, r = len(sub(c.e, c.c)), t = ang(c.c, c.e), i, e;
    var inside = function (p) { return p[0] >= 10 && p[0] <= W - 10 && p[1] >= 10 && p[1] <= H - 10; };
    for (i = 1; i <= 24 && !inside(c.e); i++) {
      e = polar(c.c, r, t + (i % 2 ? 1 : -1) * Math.ceil(i / 2) * TAU / 24);
      if (inside(e)) c.e = e;
    }
  }
  var HANDLES = {
    ra: { start: function (d, p) { d.off = sub(st.ruler.a, p); d.end = 'a'; }, move: moveEnd },
    rb: { start: function (d, p) { d.off = sub(st.ruler.b, p); d.end = 'b'; }, move: moveEnd },
    rbody: {
      start: function (d, p) { d.last = p; },
      move: function (d, p) {
        var by = sub(p, d.last), a = add(st.ruler.a, by), b = add(st.ruler.b, by);
        if (!inView(a) || !inView(b)) return;
        st.ruler.a = a; st.ruler.b = b; d.last = p;
      },
    },
    redge: {
      start: function (d, p) { var f = rulerFrame(); d.t0 = d.t1 = snapT(f, dot(sub(p, f.a), f.d)); },
      move: function (d, p) {
        var f = rulerFrame();
        d.t1 = snapT(f, dot(sub(p, f.a), f.d));
        clear(live);
        inkSeg(live, add(f.a, mul(f.d, d.t0)), add(f.a, mul(f.d, d.t1)));
      },
      end: function (d) {
        var f = rulerFrame();
        if (Math.abs(d.t1 - d.t0) < 4) return;
        commit(function () { doc.segs.push({ a: add(f.a, mul(f.d, d.t0)), b: add(f.a, mul(f.d, d.t1)), full: 0 }); });
      },
    },
    needle: { start: function (d, p) { d.off = sub(st.compass.c, p); }, move: function (d, p) { moveCompass(add(p, d.off)); } },
    hinge: { start: function (d, p) { d.off = sub(st.compass.c, p); }, move: function (d, p) { moveCompass(add(p, d.off)); } },
    pencil: {
      start: function (d, p) {
        var c = st.compass;
        d.off = sub(c.e, p);
        d.draw = st.cmode === 'draw';
        d.r = len(sub(c.e, c.c));
        d.t = d.lo = d.hi = ang(c.c, c.e);
      },
      move: function (d, p) {
        var c = st.compass, to = add(p, d.off);
        if (!d.draw) {                                   // open or close the compass
          var s = snap(clamp(to));
          if (len(sub(s.p, c.c)) < 8) return;
          c.e = s.p;
          mark = s.hit ? s.p : null;
          return;
        }
        var turn = ang(c.c, to) - d.t;                   // swing: the pencil keeps its distance
        turn -= TAU * Math.round(turn / TAU);
        d.t += turn;
        d.lo = Math.min(d.lo, d.t); d.hi = Math.max(d.hi, d.t);
        if (d.hi - d.lo > TAU) d.hi = d.lo + TAU;
        c.e = polar(c.c, d.r, d.t);
        clear(live);
        inkArc(live, c.c, d.r, d.lo, d.hi);
      },
      end: function (d) {
        if (!d.draw || (d.hi - d.lo) * d.r < 4) return;
        var c = st.compass.c.slice();
        commit(function () { doc.arcs.push({ c: c, r: d.r, t1: d.lo, t2: d.hi }); });
      },
    },
  };
  function moveEnd(d, p) {
    var s = snap(clamp(add(p, d.off))), other = st.ruler[d.end === 'a' ? 'b' : 'a'];
    if (len(sub(s.p, other)) < 16) return;
    st.ruler[d.end] = s.p;
    mark = s.hit ? s.p : null;
  }

  svg.addEventListener('pointerdown', function (e) {
    var h = e.target.getAttribute('data-h');
    if (!h || drag || (e.pointerType === 'mouse' && e.button !== 0)) return;
    e.preventDefault();
    drag = { h: HANDLES[h], id: e.pointerId };
    try { svg.setPointerCapture(e.pointerId); } catch (x) { /* an old browser */ }
    root.classList.add('dragging');
    drag.h.start(drag, toSvg(e));
  });
  svg.addEventListener('pointermove', function (e) {
    if (!drag || e.pointerId !== drag.id) return;
    drag.h.move(drag, toSvg(e));
    renderTools();
  });
  function drop(e, done) {
    if (!drag || e.pointerId !== drag.id) return;
    var d = drag;
    drag = null; mark = null;
    root.classList.remove('dragging');
    clear(live);
    if (done && d.h.end) d.h.end(d);
    keepPencil();
    renderTools();
    save();
  }
  svg.addEventListener('pointerup', function (e) { drop(e, true); });
  svg.addEventListener('pointercancel', function (e) { drop(e, false); });
  // a finger on a handle moves the tool, not the page
  svg.addEventListener('touchstart', function (e) { if (e.target.getAttribute('data-h')) e.preventDefault(); }, { passive: false });

  svg.addEventListener('click', function (e) {
    var p = toSvg(e);
    if (st.tool === 'point') {
      var s = snap(p);
      if (doc.pts.some(function (o) { return len(sub(o.p, s.p)) < 1; })) return;
      commit(function () { doc.pts.push({ p: s.p, name: nextName() }); });
    } else if (st.tool === 'name') {
      var best = -1, bd = 26;
      doc.pts.forEach(function (o, i) { var d = len(sub(o.p, p)); if (d < bd) { best = i; bd = d; } });
      pick(best);
      if (best >= 0) { nameIn.focus(); nameIn.select(); }
    }
  });
  nameForm.addEventListener('submit', function (e) {
    e.preventDefault();
    var name = nameIn.value.trim(), i = sel;
    if (i < 0 || !name) return;
    if (name !== doc.pts[i].name) commit(function () { doc.pts[i].name = name; });
    nameIn.blur();
    pick(-1);
  });

  // ------------------------------------------------------- the picture ---
  function savePicture() {
    var xml = new XMLSerializer(), was = sel;
    if (was >= 0) pick(-1);
    var src = '<svg xmlns="http://www.w3.org/2000/svg" width="' + W + '" height="' + H + '" viewBox="0 0 ' + W + ' ' + H + '">' +
      '<rect width="' + W + '" height="' + H + '" fill="' + PAPER + '"/>' + (st.grid ? xml.serializeToString(paper) : '') + xml.serializeToString(ink) + '</svg>';
    var img = new Image();
    img.onload = function () {
      var k = 2, cv = document.createElement('canvas');
      cv.width = W * k; cv.height = H * k;
      cv.getContext('2d').drawImage(img, 0, 0, W * k, H * k);
      cv.toBlob(function (blob) {
        if (!blob) return;
        var a = document.createElement('a'), url = URL.createObjectURL(blob);
        a.href = url;
        a.download = root.getAttribute('data-file') || 'board.png';
        document.body.appendChild(a);
        a.click();
        a.remove();
        setTimeout(function () { URL.revokeObjectURL(url); }, 4000);
      }, 'image/png');
    };
    img.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(src);
  }

  // ------------------------------------------------------- the buttons ---
  var ACTS = {
    undo: function () { travel(-1); },
    redo: function () { travel(1); },
    clear: function () { confirmBox.hidden = false; size(); },
    'clear-no': function () { confirmBox.hidden = true; size(); },
    full: function () { setFull(!st.full); },
    'clear-yes': function () {
      confirmBox.hidden = true;
      pick(-1);
      commit(function () { doc = { pts: [], segs: [], arcs: [] }; });
      size();
    },
    line: function () {
      var r = st.ruler;
      commit(function () { doc.segs.push({ a: r.a.slice(), b: r.b.slice(), full: 1 }); });
    },
    save: savePicture,
  };
  root.addEventListener('click', function (e) {
    var b = e.target.closest('button');
    if (!b || b.disabled) return;
    if (b.hasAttribute('data-tool')) setTool(b.getAttribute('data-tool'));
    else if (b.hasAttribute('data-cmode')) { st.cmode = b.getAttribute('data-cmode'); setTool('compass'); }
    else if (ACTS[b.getAttribute('data-act')]) ACTS[b.getAttribute('data-act')]();
  });
  all('[data-sw]').forEach(function (box) {
    box.addEventListener('change', function () {
      st[box.getAttribute('data-sw')] = box.checked;
      paper.style.display = st.grid ? '' : 'none';
      renderTools();
      save();
    });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && st.full && !/^(INPUT|TEXTAREA)$/.test(e.target.tagName)) { setFull(false); return; }
    if (!(e.ctrlKey || e.metaKey) || /^(INPUT|TEXTAREA)$/.test(e.target.tagName)) return;
    var k = e.key.toLowerCase();
    if (k === 'z') { e.preventDefault(); travel(e.shiftKey ? 1 : -1); }
    if (k === 'y') { e.preventDefault(); travel(1); }
  });

  // --------------------------------------------------------- the sheet ---
  // In the page the sheet is as wide as the page and its height is settled once (the bars of a
  // phone come and go); in the whole window it is what the bars above and below leave.
  function size() {
    var w = Math.round(stage.clientWidth);
    var h = st.full ? Math.round(stage.clientHeight) : Math.max(380, Math.min(640, Math.round(window.innerHeight * 0.72)));
    if (!w || !h || (w === W && (!st.full || h === H))) return;
    W = w; H = h;
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
    drawPaper();
    placeTools();
    renderTools();
  }

  load();
  hist = [JSON.stringify(doc)];
  all('[data-sw]').forEach(function (box) { box.checked = !!st[box.getAttribute('data-sw')]; });
  setFull(st.full);
  findCands();
  renderInk();
  buttons();
  setTool(q('.bd-tool[data-tool="' + st.tool + '"]') ? st.tool : 'point');
  window.addEventListener('resize', size);
  if (window.ResizeObserver) new ResizeObserver(size).observe(stage);
})();
