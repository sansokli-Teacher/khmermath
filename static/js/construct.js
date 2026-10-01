/* khmermath.org — geometric constructions (construct/*.html), step by step.
 *
 * A page holds <div class="cx" data-cx="NAME"> with an <ol class="cx-steps"> of
 * captions, written in the page so the Khmer text is edited there. This file
 * draws the figure for each step on an SVG «sheet of paper»: a compass that
 * swings to draw each arc, a ruler for each line. Students step through it
 * (or play it all), drag the given points, and change the compass opening to
 * see when the construction fails.
 *
 * A construction is CX[NAME] = { steps, start, figure(state), draw(f, i, …), anim(f, i) }:
 * start holds the points students may drag and the compass opening k; figure() works
 * out the geometry; draw() shows step i; anim() names the arcs or the line to animate on
 * arriving at a step. limit(state, key, p) may refuse a drag; warnFrom is the first
 * step at which «the arcs do not meet» is shown.
 */
(function () {
  'use strict';
  var NS = 'http://www.w3.org/2000/svg';
  var W = 640, H = 460;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function el(tag, attrs, parent) {
    var e = document.createElementNS(NS, tag);
    for (var k in attrs) if (attrs[k] != null) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  }
  var add = function (a, b) { return [a[0] + b[0], a[1] + b[1]]; };
  var sub = function (a, b) { return [a[0] - b[0], a[1] - b[1]]; };
  var mul = function (a, k) { return [a[0] * k, a[1] * k]; };
  var len = function (a) { return Math.hypot(a[0], a[1]); };
  var unit = function (a) { var l = len(a) || 1; return [a[0] / l, a[1] / l]; };
  var onCircle = function (c, r, t) { return [c[0] + r * Math.cos(t), c[1] + r * Math.sin(t)]; };
  function arcPath(c, r, t1, t2) {
    var p = onCircle(c, r, t1), q = onCircle(c, r, t2);
    return 'M' + p[0].toFixed(1) + ' ' + p[1].toFixed(1) + 'A' + r.toFixed(1) + ' ' + r.toFixed(1) + ' 0 ' +
      (Math.abs(t2 - t1) > Math.PI ? 1 : 0) + ' ' + (t2 > t1 ? 1 : 0) + ' ' + q[0].toFixed(1) + ' ' + q[1].toFixed(1);
  }

  // ------------------------------------------------------- the tools ---
  // A compass seen from above: needle at c, pencil at e, legs meeting at a hinge.
  function drawCompass(g, c, e) {
    var r = len(sub(e, c)), legs = Math.max(r * 0.58 + 46, r / 2 + 24);
    var mid = mul(add(c, e), 0.5), d = unit(sub(e, c)), n = [d[1], -d[0]];
    if (n[1] > 0) n = mul(n, -1);                       // hinge towards the top of the sheet
    var hinge = add(mid, mul(n, Math.sqrt(Math.max(legs * legs - r * r / 4, 0))));
    var top = add(hinge, mul(n, 26));
    el('line', { x1: hinge[0], y1: hinge[1], x2: top[0], y2: top[1], class: 'cx-c-handle' }, g);
    el('line', { x1: hinge[0], y1: hinge[1], x2: c[0], y2: c[1], class: 'cx-c-leg' }, g);
    el('line', { x1: hinge[0], y1: hinge[1], x2: e[0], y2: e[1], class: 'cx-c-leg' }, g);
    el('circle', { cx: c[0], cy: c[1], r: 3.2, class: 'cx-c-needle' }, g);
    el('circle', { cx: e[0], cy: e[1], r: 4.2, class: 'cx-c-pencil' }, g);
    el('circle', { cx: hinge[0], cy: hinge[1], r: 6, class: 'cx-c-hinge' }, g);
  }
  // A ruler laid along p→q, set a little to one side of the line it draws.
  function drawRuler(g, p, q) {
    var d = unit(sub(q, p)), n = [-d[1], d[0]], a = add(p, mul(d, -46)), b = add(q, mul(d, 46));
    var off = mul(n, 4), w = mul(n, 34);
    var pts = [add(a, off), add(b, off), add(add(b, off), w), add(add(a, off), w)];
    el('polygon', { points: pts.map(function (x) { return x.join(','); }).join(' '), class: 'cx-ruler' }, g);
    var L = len(sub(b, a));
    for (var s = 0; s <= L; s += 14) {
      var t = add(add(a, off), mul(d, s)), k = s % 70 === 0 ? 12 : 7;
      el('line', { x1: t[0], y1: t[1], x2: t[0] + n[0] * k, y2: t[1] + n[1] * k, class: 'cx-ruler-tick' }, g);
    }
  }

  // ----------------------------------------------- the constructions ---
  var CX = {};

  // Perpendicular bisector of AB: arcs of the same radius from A and from B
  // meet at P and Q; the line PQ cuts AB at its midpoint M, at right angles.
  CX['segment-bisector'] = {
    steps: 7,
    start: { A: [170, 248], B: [470, 248], k: 0.72 },
    limit: function (s, key, p) { return len(sub(p, s[key === 'A' ? 'B' : 'A'])) >= 90; },
    figure: function (s) {
      var A = s.A, B = s.B, AB = len(sub(B, A)), r = s.k * AB, M = mul(add(A, B), 0.5);
      var u = unit(sub(B, A)), n = [u[1], -u[0]];
      if (n[1] > 0) n = mul(n, -1);
      var meet = r > AB / 2 + 0.5, h = meet ? Math.sqrt(r * r - AB * AB / 4) : 0;
      var P = add(M, mul(n, h)), Q = add(M, mul(n, -h));
      // arcs around where they meet (or, too short, around the middle of AB)
      var spread = 0.42;
      var aim = function (from, to) { return Math.atan2(to[1] - from[1], to[0] - from[0]); };
      var tAP = meet ? aim(A, P) : aim(A, M) - 0.9, tAQ = meet ? aim(A, Q) : aim(A, M) + 0.9;
      var tBP = meet ? aim(B, P) : aim(B, M) + 0.9, tBQ = meet ? aim(B, Q) : aim(B, M) - 0.9;
      var fix = function (t, ref) { while (t - ref > Math.PI) t -= 2 * Math.PI; while (ref - t > Math.PI) t += 2 * Math.PI; return t; };
      tAQ = fix(tAQ, tAP); tBQ = fix(tBQ, tBP);
      return {
        meet: meet, r: r, A: A, B: B, M: M, P: P, Q: Q, n: n, u: u,
        arcs: [
          { c: A, t1: tAP - spread, t2: tAP + spread }, { c: A, t1: tAQ - spread, t2: tAQ + spread },
          { c: B, t1: tBP + spread, t2: tBP - spread }, { c: B, t1: tBQ + spread, t2: tBQ - spread },
        ],
      };
    },
    // what step i shows; anim(i) returns the animation to play on arriving there
    draw: function (f, i, g, layer) {
      var ink = layer.ink, marks = layer.marks;
      el('line', { x1: f.A[0], y1: f.A[1], x2: f.B[0], y2: f.B[1], class: 'cx-seg' }, ink);
      if (i === 1) {                                     // the opening: more than half of AB
        el('line', { x1: f.A[0], y1: f.A[1], x2: f.A[0] + f.u[0] * f.r, y2: f.A[1] + f.u[1] * f.r, class: 'cx-radius' }, marks);
        var half = add(f.A, mul(f.u, len(sub(f.B, f.A)) / 2));
        el('line', { x1: half[0] + f.n[0] * 9, y1: half[1] + f.n[1] * 9, x2: half[0] - f.n[0] * 9, y2: half[1] - f.n[1] * 9, class: 'cx-half' }, marks);
        label(marks, add(half, mul(f.n, 26)), '½AB', 'cx-note');
        label(marks, add(add(f.A, mul(f.u, f.r / 2)), mul(f.n, -22)), 'r', 'cx-note cx-r');
      }
      var nArcs = i >= 3 ? 4 : i >= 2 ? 2 : 0;
      for (var a = 0; a < nArcs; a++) el('path', { d: arcPath(f.arcs[a].c, f.r, f.arcs[a].t1, f.arcs[a].t2), class: 'cx-arc' }, ink);
      if (i >= 4 && f.meet) {
        point(ink, f.P, 'P', add(mul(f.u, 1.1), mul(f.n, 0.35))); point(ink, f.Q, 'Q', add(mul(f.u, 1.1), mul(f.n, -0.35)));
      }
      if (i >= 5 && f.meet) {
        var e1 = add(f.P, mul(f.n, 40)), e2 = add(f.Q, mul(f.n, -40));
        el('line', { x1: e1[0], y1: e1[1], x2: e2[0], y2: e2[1], class: 'cx-line' }, ink);
      }
      if (i >= 6 && f.meet) {
        ['A', 'B'].forEach(function (k) {
          [f.P, f.Q].forEach(function (X) { el('line', { x1: X[0], y1: X[1], x2: f[k][0], y2: f[k][1], class: 'cx-equal' }, marks); });
        });
        var s = 13, c = f.M, p1 = add(c, mul(f.u, s)), p2 = add(p1, mul(f.n, s)), p3 = add(c, mul(f.n, s));
        el('polyline', { points: [p1, p2, p3].map(function (x) { return x.join(','); }).join(' '), class: 'cx-right' }, marks);
        [mul(add(f.A, f.M), 0.5), mul(add(f.M, f.B), 0.5)].forEach(function (t) {
          el('line', { x1: t[0] - f.n[0] * 7, y1: t[1] - f.n[1] * 7, x2: t[0] + f.n[0] * 7, y2: t[1] + f.n[1] * 7, class: 'cx-tick' }, marks);
        });
        point(ink, f.M, 'M', add(mul(f.u, 0.9), mul(f.n, -0.9)), 'cx-pt-m');
      }
      point(ink, f.A, 'A', mul(f.u, -1), null, 'A');
      point(ink, f.B, 'B', f.u, null, 'B');
      if (i === 1) drawCompass(layer.tools, f.A, add(f.A, mul(f.u, f.r)));
    },
    anim: function (f, i) {
      if (i === 2) return { arcs: [0, 1] };
      if (i === 3) return { arcs: [2, 3] };
      if (i === 5 && f.meet) return { ruler: [add(f.P, mul(f.n, 40)), add(f.Q, mul(f.n, -40))] };
      return null;
    },
  };

  // Bisector of the angle xOy (Grade 7, lesson 13): an arc from O meets the sides at A
  // and B; arcs of one radius from B and from A meet at t; Ot bisects the angle.
  CX['angle-bisector'] = {
    steps: 6,
    warnFrom: 3,
    start: { O: [150, 362], X: [540, 362], Y: [395, 112], k: 0.8 },
    // the sides stay long enough to carry the arc, and the angle between 25° and 160°
    limit: function (s, key, p) {
      var a = sub(p, s.O), b = sub(s[key === 'X' ? 'Y' : 'X'], s.O);
      var ang = Math.acos(Math.max(-1, Math.min(1, (a[0] * b[0] + a[1] * b[1]) / (len(a) * len(b))))) * 180 / Math.PI;
      return len(a) >= 190 && ang >= 25 && ang <= 160;
    },
    figure: function (s) {
      var O = s.O, ux = unit(sub(s.X, O)), uy = unit(sub(s.Y, O)), R = 165;
      var A = add(O, mul(ux, R)), B = add(O, mul(uy, R)), AB = len(sub(B, A)), r = s.k * AB;
      var M = mul(add(A, B), 0.5), d = unit(sub(M, O)), meet = r > AB / 2 + 0.5;
      var h = meet ? Math.sqrt(r * r - AB * AB / 4) : 0, T = add(M, mul(d, h));
      var wA = unit(sub(ux, mul(d, ux[0] * d[0] + ux[1] * d[1])));      // away from the bisector, on A's side
      var aim = function (from, to) { return Math.atan2(to[1] - from[1], to[0] - from[0]); };
      var ax = Math.atan2(ux[1], ux[0]), turn = Math.atan2(uy[1], uy[0]) - ax;
      while (turn > Math.PI) turn -= 2 * Math.PI;
      while (turn < -Math.PI) turn += 2 * Math.PI;
      var sg = turn > 0 ? 1 : -1, towards = meet ? T : add(M, mul(d, r * 0.75));
      // a ray is drawn from O to just inside the edge of the sheet
      var edge = function (u) {
        var t = 1e9;
        if (u[0] > 1e-6) t = Math.min(t, (W - 26 - O[0]) / u[0]); else if (u[0] < -1e-6) t = Math.min(t, (26 - O[0]) / u[0]);
        if (u[1] > 1e-6) t = Math.min(t, (H - 26 - O[1]) / u[1]); else if (u[1] < -1e-6) t = Math.min(t, (26 - O[1]) / u[1]);
        return add(O, mul(u, Math.max(t, R + 40)));
      };
      return {
        meet: meet, r: r, R: R, O: O, A: A, B: B, M: M, T: T, d: d, ux: ux, uy: uy, wA: wA, ax: ax, turn: turn,
        X: s.X, Y: s.Y, Ex: edge(ux), Ey: edge(uy), Et: edge(d),
        arcs: [
          { c: O, r: R, t1: ax - sg * 0.2, t2: ax + turn + sg * 0.2 },
          { c: B, r: r, t1: aim(B, towards) - sg * 0.42, t2: aim(B, towards) + sg * 0.42 },
          { c: A, r: r, t1: aim(A, towards) + sg * 0.42, t2: aim(A, towards) - sg * 0.42 },
        ],
      };
    },
    draw: function (f, i, g, layer) {
      var ink = layer.ink, marks = layer.marks, wB = mul(f.wA, -1);
      if (i >= 5 && f.meet) {                             // the two equal angles
        var rho = 86, half = f.turn / 2, sw = f.turn > 0 ? 1 : 0;
        [[f.ax, 'a'], [f.ax + half, 'b']].forEach(function (q) {
          var p1 = onCircle(f.O, rho, q[0]), p2 = onCircle(f.O, rho, q[0] + half);
          el('path', { d: 'M' + f.O.join(' ') + 'L' + p1.join(' ') + 'A' + rho + ' ' + rho + ' 0 0 ' + sw + ' ' + p2.join(' ') + 'Z', class: 'cx-sector cx-sector-' + q[1] }, marks);
          el('path', { d: 'M' + p1.join(' ') + 'A' + rho + ' ' + rho + ' 0 0 ' + sw + ' ' + p2.join(' '), class: 'cx-sector-edge cx-sector-edge-' + q[1] }, marks);
          var m1 = onCircle(f.O, rho - 7, q[0] + half / 2), m2 = onCircle(f.O, rho + 7, q[0] + half / 2);
          el('line', { x1: m1[0], y1: m1[1], x2: m2[0], y2: m2[1], class: 'cx-tick' }, marks);
        });
        [f.A, f.B].forEach(function (P) { el('line', { x1: P[0], y1: P[1], x2: f.T[0], y2: f.T[1], class: 'cx-equal' }, marks); });
      }
      [[f.Ex, 'x', f.wA], [f.Ey, 'y', wB]].forEach(function (q) {
        el('line', { x1: f.O[0], y1: f.O[1], x2: q[0][0], y2: q[0][1], class: 'cx-seg' }, ink);
        label(ink, add(add(q[0], mul(unit(sub(f.O, q[0])), 14)), mul(q[2], 17)), q[1], 'cx-label');
      });
      for (var a = 0; a < Math.min(i, 3); a++) el('path', { d: arcPath(f.arcs[a].c, f.arcs[a].r, f.arcs[a].t1, f.arcs[a].t2), class: 'cx-arc' }, ink);
      if (i >= 4 && f.meet) el('line', { x1: f.O[0], y1: f.O[1], x2: f.Et[0], y2: f.Et[1], class: 'cx-line' }, ink);
      if (i >= 1) { point(ink, f.A, 'A', add(f.wA, mul(f.ux, 0.25))); point(ink, f.B, 'B', add(wB, mul(f.uy, 0.25))); }
      if (i >= 3 && f.meet) {
        el('circle', { cx: f.T[0], cy: f.T[1], r: 5, class: 'cx-pt cx-pt-m' }, ink);
        label(ink, add(f.T, add(mul(f.wA, 24), mul(f.d, 20))), 't', 'cx-label');
      }
      point(ink, f.O, 'O', mul(f.d, -1));
      // the handles that turn the sides
      [['X', f.X], ['Y', f.Y]].forEach(function (q) {
        el('circle', { cx: q[1][0], cy: q[1][1], r: 7, class: 'cx-handle' }, ink);
        el('circle', { cx: q[1][0], cy: q[1][1], r: 24, class: 'cx-grab', 'data-drag': q[0] }, ink);
      });
    },
    anim: function (f, i) {
      if (i >= 1 && i <= 3) return { arcs: [i - 1] };
      if (i === 4 && f.meet) return { ruler: [f.O, f.Et] };
      return null;
    },
  };

  function label(g, at, text, cls) {
    var t = el('text', { x: at[0], y: at[1], class: cls || 'cx-label', 'text-anchor': 'middle', 'dominant-baseline': 'central' }, g);
    t.textContent = text;
    return t;
  }
  // a point with its name pushed out along dir
  function point(g, p, name, dir, cls, drag) {
    el('circle', { cx: p[0], cy: p[1], r: 5, class: 'cx-pt ' + (cls || '') }, g);
    var d = unit(dir || [0, -1]);
    label(g, add(p, mul(d, 20)), name, 'cx-label');
    if (drag) el('circle', { cx: p[0], cy: p[1], r: 22, class: 'cx-grab', 'data-drag': drag }, g);
  }

  // ---------------------------------------------------------- player ---
  function Player(root) {
    var def = CX[root.getAttribute('data-cx')];
    if (!def) return;
    var stage = root.querySelector('.cx-stage');
    var items = Array.prototype.slice.call(root.querySelectorAll('.cx-steps li'));
    var now = root.querySelector('.cx-now');
    var warn = root.querySelector('.cx-warn');
    var slider = root.querySelector('.cx-k');
    var kOut = root.querySelector('.cx-k-out');
    var btn = function (sel) { return root.querySelector(sel); };
    var fresh = function () {
      var s = {};
      for (var key in def.start) s[key] = Array.isArray(def.start[key]) ? def.start[key].slice() : def.start[key];
      return s;
    };
    var state = fresh();
    var step = 0, playing = false, timer = null, raf = null;

    var svg = el('svg', { viewBox: '0 0 ' + W + ' ' + H, class: 'cx-svg', role: 'img', 'aria-label': root.getAttribute('data-label') || '' });
    stage.innerHTML = '';
    stage.appendChild(svg);
    var paper = el('g', {}, svg), marks = el('g', {}, svg), ink = el('g', {}, svg), tools = el('g', {}, svg);
    // squared paper
    for (var x = 20; x < W; x += 20) el('line', { x1: x, y1: 0, x2: x, y2: H, class: 'cx-grid' + (x % 100 === 0 ? ' b' : '') }, paper);
    for (var y = 20; y < H; y += 20) el('line', { x1: 0, y1: y, x2: W, y2: y, class: 'cx-grid' + (y % 100 === 0 ? ' b' : '') }, paper);

    function clear(g) { while (g.firstChild) g.removeChild(g.firstChild); }
    function render(i, upTo) {
      clear(marks); clear(ink); clear(tools);
      var f = def.figure(state);
      def.draw(f, i, svg, { ink: ink, marks: marks, tools: tools });
      warn.hidden = f.meet || i < (def.warnFrom || 2);
      return f;
    }
    function caption() {
      items.forEach(function (li, j) {
        li.classList.toggle('on', j === step);
        li.classList.toggle('done', j < step);
        li.setAttribute('aria-current', j === step ? 'step' : 'false');
      });
      now.innerHTML = '<b>' + km(step + 1) + '/' + km(def.steps) + '</b> ' + items[step].innerHTML;
      btn('.cx-prev').disabled = step === 0;
      btn('.cx-next').disabled = step === def.steps - 1;
    }
    function stopAnim() { if (raf) cancelAnimationFrame(raf); raf = null; }
    // go to step i; animate the new shapes when moving forward one step
    function go(i, animate) {
      stopAnim();
      step = Math.max(0, Math.min(def.steps - 1, i));
      caption();
      var f = def.figure(state);
      var a = animate && !reduce ? def.anim(f, step) : null;
      if (!a) { render(step); return Promise.resolve(); }
      render(step - 1);
      clear(marks); clear(tools);                         // the previous step's hints go
      return new Promise(function (done) {
        var t0 = null, dur = a.arcs ? 1100 : 1000, part = 0;
        var parts = a.arcs ? a.arcs.slice() : [0];
        var drawn = el('g', {}, ink);
        function frame(ts) {
          if (t0 == null) t0 = ts;
          var t = Math.min(1, (ts - t0) / dur);
          clear(tools); clear(drawn);
          if (a.arcs) {
            for (var j = 0; j < part; j++) { var q = f.arcs[parts[j]]; el('path', { d: arcPath(q.c, q.r || f.r, q.t1, q.t2), class: 'cx-arc' }, drawn); }
            var arc = f.arcs[parts[part]], th = arc.t1 + (arc.t2 - arc.t1) * ease(t);
            var rr = arc.r || f.r;
            el('path', { d: arcPath(arc.c, rr, arc.t1, th), class: 'cx-arc' }, drawn);
            drawCompass(tools, arc.c, onCircle(arc.c, rr, th));
          } else {
            var p = a.ruler[0], q2 = a.ruler[1], e = add(p, mul(sub(q2, p), ease(t)));
            drawRuler(tools, p, q2);
            el('line', { x1: p[0], y1: p[1], x2: e[0], y2: e[1], class: 'cx-line' }, drawn);
          }
          if (t < 1) { raf = requestAnimationFrame(frame); return; }
          if (++part < parts.length) { t0 = null; raf = requestAnimationFrame(frame); return; }
          raf = null;
          setTimeout(function () { if (!raf) render(step); done(); }, a.arcs ? 250 : 450);
        }
        raf = requestAnimationFrame(frame);
      });
    }
    var ease = function (t) { return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2; };
    var km = function (n) { return String(n).replace(/\d/g, function (d) { return '០១២៣៤៥៦៧៨៩'[d]; }); };

    function stopPlay() {
      playing = false; clearTimeout(timer);
      btn('.cx-play').classList.remove('on');
      btn('.cx-play span').textContent = btn('.cx-play').getAttribute('data-play');
    }
    function play() {
      if (playing) { stopPlay(); return; }
      playing = true;
      btn('.cx-play').classList.add('on');
      btn('.cx-play span').textContent = btn('.cx-play').getAttribute('data-pause');
      var next = function () {
        if (!playing) return;
        if (step >= def.steps - 1) { stopPlay(); return; }
        go(step + 1, true).then(function () {
          if (!playing) return;
          if (step >= def.steps - 1) stopPlay(); else timer = setTimeout(next, 1500);
        });
      };
      if (step >= def.steps - 1) go(0, false).then(function () { timer = setTimeout(next, 900); });
      else next();
    }

    btn('.cx-prev').addEventListener('click', function () { stopPlay(); go(step - 1, false); });
    btn('.cx-next').addEventListener('click', function () { stopPlay(); go(step + 1, true); });
    btn('.cx-play').addEventListener('click', play);
    btn('.cx-reset').addEventListener('click', function () {
      stopPlay();
      state = fresh();
      if (slider) { slider.value = Math.round(state.k * 100); showK(); }
      go(0, false);
    });
    items.forEach(function (li, j) {
      li.tabIndex = 0;
      li.addEventListener('click', function () { stopPlay(); go(j, j === step + 1); });
      li.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); li.click(); } });
    });
    root.addEventListener('keydown', function (e) {
      if (e.target.closest('input')) return;
      if (e.key === 'ArrowRight') { e.preventDefault(); btn('.cx-next').click(); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); btn('.cx-prev').click(); }
    });

    // the compass opening, as a share of AB
    function showK() {
      if (!slider) return;
      state.k = slider.value / 100;
      var ok = state.k > 0.5;
      kOut.textContent = ok ? root.getAttribute('data-k-ok') : root.getAttribute('data-k-short');
      kOut.classList.toggle('bad', !ok);
    }
    if (slider) {
      slider.value = Math.round(state.k * 100);
      showK();
      slider.addEventListener('input', function () { stopPlay(); stopAnim(); showK(); render(step); });
    }

    // drag A or B (mouse, finger or pen)
    var dragging = null;
    function toSvg(e) {
      var pt = svg.createSVGPoint(); pt.x = e.clientX; pt.y = e.clientY;
      var p = pt.matrixTransform(svg.getScreenCTM().inverse());
      return [Math.max(30, Math.min(W - 30, p.x)), Math.max(30, Math.min(H - 30, p.y))];
    }
    svg.addEventListener('pointerdown', function (e) {
      var g = e.target.getAttribute && e.target.getAttribute('data-drag');
      if (!g) return;
      e.preventDefault();
      stopPlay(); stopAnim();
      dragging = g;
      svg.setPointerCapture(e.pointerId);
      root.classList.add('dragging');
    });
    svg.addEventListener('pointermove', function (e) {
      if (!dragging) return;
      var p = toSvg(e);
      if (def.limit && !def.limit(state, dragging, p)) return;
      state[dragging] = p;
      render(step);
    });
    var end = function () { dragging = null; root.classList.remove('dragging'); };
    svg.addEventListener('pointerup', end);
    svg.addEventListener('pointercancel', end);

    go(0, false);
  }

  document.querySelectorAll('.cx[data-cx]').forEach(Player);
})();
