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
 * arriving at a step. limit(state, key, p) may refuse a drag and place(state, key, p)
 * may move it (a point kept on a line); warnFrom is the first step at which the
 * warning is shown, when figure().meet is false. The slider is good when k > 0.5,
 * or when kOk(k) says so; kSnap(value) may pull the slider onto a value. A button
 * with data-preset="NAME" in the page runs presets.NAME(state) (a ready-made case).
 * The slider may count something else than a share: kScale is what one unit of k is on
 * the slider (100 by default), kText(state) the line under it; fill(state) gives the
 * words for the <span data-fill="KEY"> of the captions when they depend on the state.
 * anim() may return { rulers: [[p, q], ...] } to draw several lines one after another.
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

  // the same opening kept (k = 1), for the constructions that carry a length with the compass
  var keptK = function (k) { return Math.abs(k - 1) < 0.005; };
  var snapK = function (v) { return Math.abs(v - 100) <= 2 ? 100 : v; };
  // a filled angle from direction t0, turning by dt, with its edge and one tick
  function sector(g, c, t0, dt, rho, kind) {
    var p1 = onCircle(c, rho, t0), p2 = onCircle(c, rho, t0 + dt);
    var arc = 'A' + rho + ' ' + rho + ' 0 ' + (Math.abs(dt) > Math.PI ? 1 : 0) + ' ' + (dt > 0 ? 1 : 0) + ' ' + p2.join(' ');
    el('path', { d: 'M' + c.join(' ') + 'L' + p1.join(' ') + arc + 'Z', class: 'cx-sector cx-sector-' + kind }, g);
    el('path', { d: 'M' + p1.join(' ') + arc, class: 'cx-sector-edge cx-sector-edge-' + kind }, g);
    var m1 = onCircle(c, rho - 7, t0 + dt / 2), m2 = onCircle(c, rho + 7, t0 + dt / 2);
    el('line', { x1: m1[0], y1: m1[1], x2: m2[0], y2: m2[1], class: 'cx-tick' }, g);
  }
  function tick(g, p, q) {
    var m = mul(add(p, q), 0.5), u = unit(sub(q, p)), n = [u[1], -u[0]];
    el('line', { x1: m[0] - n[0] * 8, y1: m[1] - n[1] * 8, x2: m[0] + n[0] * 8, y2: m[1] + n[1] * 8, class: 'cx-tick' }, g);
  }

  // A segment A'B' on the line xy as long as AB (Grade 7, lesson 12): open the compass on
  // AB, mark A' on the line, and with the same opening cut the line at B'.
  CX['copy-segment'] = {
    steps: 5,
    warnFrom: 3,
    start: { A: [160, 212], B: [356, 178], P: [168, 350], k: 1 },
    kOk: keptK, kSnap: snapK,
    place: function (s, key, p) { return key === 'P' ? [Math.max(60, Math.min(430, p[0])), s.P[1]] : p; },
    limit: function (s, key, p) {
      if (key === 'P') return true;
      var d = len(sub(p, s[key === 'A' ? 'B' : 'A']));
      return d >= 90 && d <= 300 && p[1] >= 170 && p[1] <= 262;      // room for the compass above, the line xy below
    },
    figure: function (s) {
      var A = s.A, B = s.B, AB = len(sub(B, A)), r = s.k * AB, u = unit(sub(B, A)), n = [u[1], -u[0]];
      if (n[1] > 0) n = mul(n, -1);
      var P = [Math.max(44, Math.min(s.P[0], 600 - r)), s.P[1]], Q = [P[0] + r, P[1]];
      return { meet: keptK(s.k), r: r, A: A, B: B, u: u, n: n, P: P, Q: Q, arcs: [{ c: P, r: r, t1: -0.34, t2: 0.34 }] };
    },
    draw: function (f, i, g, layer) {
      var ink = layer.ink, marks = layer.marks, y = f.P[1];
      el('line', { x1: 30, y1: y, x2: W - 30, y2: y, class: 'cx-seg' }, ink);
      label(ink, [40, y + 24], 'x', 'cx-label'); label(ink, [W - 40, y + 24], 'y', 'cx-label');
      el('line', { x1: f.A[0], y1: f.A[1], x2: f.B[0], y2: f.B[1], class: 'cx-seg' }, ink);
      if (i >= 3) el('path', { d: arcPath(f.P, f.r, -0.34, 0.34), class: 'cx-arc' }, ink);
      if (i >= 4) {
        el('line', { x1: f.P[0], y1: y, x2: f.Q[0], y2: y, class: 'cx-line' }, ink);
        tick(marks, f.A, f.B); tick(marks, f.P, f.Q);
        label(marks, [(f.P[0] + f.Q[0]) / 2, y - 30], f.meet ? 'A′B′ = AB' : 'A′B′ ≠ AB', 'cx-note cx-r');
      }
      point(ink, f.A, 'A', mul(f.u, -1), null, 'A');
      point(ink, f.B, 'B', f.u, null, 'B');
      if (i >= 2) point(ink, f.P, 'A′', [0, 1], null, 'P');
      if (i >= 3) point(ink, f.Q, 'B′', [0.8, 0.9], 'cx-pt-m');
      if (i === 1) drawCompass(layer.tools, f.A, f.B);
    },
    anim: function (f, i) { return i === 3 ? { arcs: [0] } : null; },
  };

  // An angle zAt equal to the angle xOy (Grade 7, lesson 13): an arc from O cuts the sides
  // at M and N; the same arc from A cuts At at B; an arc from B of radius MN cuts it at C.
  CX['copy-angle'] = {
    steps: 8,
    warnFrom: 5,
    start: { O: [84, 318], Y: [216, 161], A: [372, 318], T: [600, 318], k: 1 },
    kOk: keptK, kSnap: snapK,
    // the angle stays between 25° and 110°; the ray At within 30° of the horizontal
    limit: function (s, key, p) {
      var v = sub(p, key === 'Y' ? s.O : s.A), ang = Math.atan2(-v[1], v[0]) * 180 / Math.PI;
      return key === 'Y' ? len(v) >= 170 && ang >= 25 && ang <= 110 : len(v) >= 190 && Math.abs(ang) <= 30;
    },
    figure: function (s) {
      var O = s.O, A = s.A, R = 132, ux = [1, 0], uy = unit(sub(s.Y, O)), ut = unit(sub(s.T, A));
      var turn = Math.atan2(uy[1], uy[0]), sg = turn > 0 ? 1 : -1, at = Math.atan2(ut[1], ut[0]);
      var M = add(O, mul(ux, R)), N = add(O, mul(uy, R)), MN = len(sub(N, M)), r = s.k * MN;
      var beta = 2 * Math.asin(Math.min(1, r / (2 * R))), B = add(A, mul(ut, R)), C = onCircle(A, R, at + sg * beta);
      var uz = unit(sub(C, A)), toC = Math.atan2(C[1] - B[1], C[0] - B[0]);
      return {
        meet: keptK(s.k), O: O, A: A, M: M, N: N, B: B, C: C, Y: s.Y, T: s.T, R: R, r: r,
        ux: ux, uy: uy, ut: ut, uz: uz, turn: turn, sg: sg, at: at, beta: beta,
        Ex: add(O, mul(ux, 214)), Ey: add(O, mul(uy, len(sub(s.Y, O)) + 18)),
        Et: add(A, mul(ut, len(sub(s.T, A)) + 18)), Ez: add(A, mul(uz, 200)),
        arcs: [
          { c: O, r: R, t1: -sg * 0.18, t2: turn + sg * 0.18 },
          { c: A, r: R, t1: at - sg * 0.18, t2: at + sg * (Math.max(Math.abs(turn), beta) + 0.3) },
          { c: B, r: r, t1: toC + sg * 0.36, t2: toC - sg * 0.36 },
        ],
      };
    },
    draw: function (f, i, g, layer) {
      var ink = layer.ink, marks = layer.marks, sg = f.sg;
      var out = function (u, side) { return [-side * sg * u[1], side * sg * u[0]]; };   // side 1: beyond the second side of the angle
      if (i >= 7) {
        sector(marks, f.O, 0, f.turn, 74, 'a');
        sector(marks, f.A, f.at, sg * f.beta, 74, f.meet ? 'a' : 'b');
        [[f.M, f.N], [f.B, f.C]].forEach(function (q) { el('line', { x1: q[0][0], y1: q[0][1], x2: q[1][0], y2: q[1][1], class: 'cx-equal' }, marks); });
      }
      [[f.Ex, 'x', out(f.ux, -1)], [f.Ey, 'y', out(f.uy, 1)]].forEach(function (q) {
        el('line', { x1: f.O[0], y1: f.O[1], x2: q[0][0], y2: q[0][1], class: 'cx-seg' }, ink);
        label(ink, add(add(q[0], mul(unit(sub(f.O, q[0])), 10)), mul(q[2], 28)), q[1], 'cx-label');
      });
      if (i >= 2) {
        el('line', { x1: f.A[0], y1: f.A[1], x2: f.Et[0], y2: f.Et[1], class: 'cx-line' }, ink);
        label(ink, add(add(f.Et, mul(f.ut, -8)), mul(out(f.ut, -1), 28)), 't', 'cx-label');
      }
      if (i >= 6) {
        el('line', { x1: f.A[0], y1: f.A[1], x2: f.Ez[0], y2: f.Ez[1], class: 'cx-line' }, ink);
        label(ink, add(add(f.Ez, mul(f.uz, -8)), mul(out(f.uz, 1), 20)), 'z', 'cx-label');
      }
      if (i >= 1) el('path', { d: arcPath(f.arcs[0].c, f.R, f.arcs[0].t1, f.arcs[0].t2), class: 'cx-arc' }, ink);
      if (i >= 3) el('path', { d: arcPath(f.arcs[1].c, f.R, f.arcs[1].t1, f.arcs[1].t2), class: 'cx-arc' }, ink);
      if (i >= 5) el('path', { d: arcPath(f.arcs[2].c, f.r, f.arcs[2].t1, f.arcs[2].t2), class: 'cx-arc' }, ink);
      if (i === 4) el('line', { x1: f.M[0], y1: f.M[1], x2: f.N[0], y2: f.N[1], class: 'cx-radius' }, marks);
      if (i >= 1) { point(ink, f.M, 'M', out(f.ux, -1)); point(ink, f.N, 'N', out(f.uy, 1)); }
      if (i >= 3) point(ink, f.B, 'B', out(f.ut, -1));
      if (i >= 5) point(ink, f.C, 'C', add(out(f.uz, 1), mul(f.uz, 0.5)), 'cx-pt-m');
      point(ink, f.O, 'O', [-0.75, 0.66]);
      if (i >= 2) point(ink, f.A, 'A', [-0.75, 0.66]);
      // the handles: Oy turns the angle, At turns the copy
      [['Y', f.Y, 0], ['T', f.T, 2]].forEach(function (q) {
        if (i < q[2]) return;
        el('circle', { cx: q[1][0], cy: q[1][1], r: 7, class: 'cx-handle' }, ink);
        el('circle', { cx: q[1][0], cy: q[1][1], r: 24, class: 'cx-grab', 'data-drag': q[0] }, ink);
      });
      if (i === 4) drawCompass(layer.tools, f.M, f.N);
    },
    anim: function (f, i) {
      if (i === 1) return { arcs: [0] };
      if (i === 2) return { ruler: [f.A, f.Et] };
      if (i === 3) return { arcs: [1] };
      if (i === 5) return { arcs: [2] };
      if (i === 6) return { ruler: [f.A, f.Ez] };
      return null;
    },
  };

  // The line d' through A perpendicular to d (Grade 7, lesson 14, with the compass instead of
  // the set square): an arc from A cuts d at P and Q; arcs of one radius from P and from Q
  // meet at B; AB is perpendicular to d. A may lie on d: then P and Q are on either side of it.
  var PERP = { C: [320, 250], half: 110, reach: 270 };
  function perpFrame(s) {
    var u = unit(sub(s.D, PERP.C)), n = [u[1], -u[0]];
    if (n[1] > 0) n = mul(n, -1);                        // n points to the top of the sheet
    var v = sub(s.A, PERP.C);
    return { u: u, n: n, along: v[0] * u[0] + v[1] * u[1], dist: v[0] * n[0] + v[1] * n[1] };
  }
  CX['perpendicular'] = {
    steps: 6,
    warnFrom: 3,
    start: { A: [296, 96], D: [590, 250], k: 0.8 },
    presets: {
      off: function (s) { var f = perpFrame(s); s.A = add(add(PERP.C, mul(f.u, -24)), mul(f.n, 150)); },
      on: function (s) { var f = perpFrame(s); s.A = add(PERP.C, mul(f.u, -24)); },
    },
    // A snaps onto d when it comes close; the handle D only turns the line
    place: function (s, key, p) {
      if (key === 'D') return add(PERP.C, mul(unit(sub(p, PERP.C)), PERP.reach));
      var f = perpFrame({ A: p, D: s.D });
      return Math.abs(f.dist) < 13 ? add(PERP.C, mul(f.u, f.along)) : p;
    },
    limit: function (s, key, p) {
      var t = key === 'D' ? { A: s.A, D: p } : { A: p, D: s.D }, f = perpFrame(t);
      return f.u[0] > 0 && Math.abs(Math.atan2(f.u[1], f.u[0])) <= 0.56 && Math.abs(f.along) <= 150 && Math.abs(f.dist) <= 190;
    },
    figure: function (s) {
      var fr = perpFrame(s), u = fr.u, n = fr.n, on = Math.abs(fr.dist) < 0.5, c = PERP.half;
      var H = add(PERP.C, mul(u, fr.along)), A = on ? H : s.A;
      var side = on ? -1 : (fr.dist > 0 ? 1 : -1);          // A's side of d; B goes to the other side
      var nA = mul(n, side), nB = mul(n, -side);
      var P = add(H, mul(u, -c)), Q = add(H, mul(u, c)), R = on ? c : Math.hypot(c, fr.dist);
      var r = s.k * 2 * c, meet = r > c + 0.5, h = meet ? Math.sqrt(r * r - c * c) : 0, B = add(H, mul(nB, h));
      var aim = function (from, to) { return Math.atan2(to[1] - from[1], to[0] - from[0]); };
      var fix = function (t, ref) { while (t - ref > Math.PI) t -= 2 * Math.PI; while (ref - t > Math.PI) t += 2 * Math.PI; return t; };
      var tP = aim(A, P), tQ = fix(aim(A, Q), tP), sg = tQ > tP ? 1 : -1;
      // the arc from A: one sweep through P and Q, or (A on d) a short mark at each
      var first = on ? [{ c: A, r: R, t1: tP - 0.3, t2: tP + 0.3 }, { c: A, r: R, t1: tQ - 0.3, t2: tQ + 0.3 }]
        : [{ c: A, r: R, t1: tP - sg * 0.16, t2: tQ + sg * 0.16 }];
      var towards = meet ? B : add(H, mul(nB, r * 0.75));
      var hi = Math.max(on ? 0 : Math.abs(fr.dist), 0) + 46, lo = h + 46;
      return {
        meet: meet, on: on, A: A, H: H, P: P, Q: Q, B: B, D: s.D, u: u, n: n, nA: nA, nB: nB, r: r, R: R,
        d1: add(PERP.C, mul(u, -330)), d2: add(PERP.C, mul(u, 330)),
        e1: add(H, mul(nA, hi)), e2: add(H, mul(nB, lo)),
        nFirst: first.length,
        arcs: first.concat([
          { c: P, r: r, t1: aim(P, towards) - 0.4, t2: aim(P, towards) + 0.4 },
          { c: Q, r: r, t1: aim(Q, towards) + 0.4, t2: aim(Q, towards) - 0.4 },
        ]),
      };
    },
    draw: function (f, i, g, layer) {
      var ink = layer.ink, marks = layer.marks, k = f.nFirst;
      var arc = function (q) { el('path', { d: arcPath(q.c, q.r, q.t1, q.t2), class: 'cx-arc' }, ink); };
      if (i >= 5 && f.meet) {
        [f.P, f.Q].forEach(function (X) {
          el('line', { x1: X[0], y1: X[1], x2: f.B[0], y2: f.B[1], class: 'cx-equal' }, marks);
          if (!f.on) el('line', { x1: X[0], y1: X[1], x2: f.A[0], y2: f.A[1], class: 'cx-equal' }, marks);
        });
        var m = f.on ? f.nB : f.nA, s = 13, p1 = add(f.H, mul(f.u, s)), p2 = add(p1, mul(m, s)), p3 = add(f.H, mul(m, s));
        el('polyline', { points: [p1, p2, p3].map(function (x) { return x.join(','); }).join(' '), class: 'cx-right' }, marks);
        tick(marks, f.P, f.H); tick(marks, f.H, f.Q);
      }
      el('line', { x1: f.d1[0], y1: f.d1[1], x2: f.d2[0], y2: f.d2[1], class: 'cx-seg' }, ink);
      label(ink, add(add(PERP.C, mul(f.u, -292)), mul(f.n, 20)), 'd', 'cx-label');
      if (i >= 4 && f.meet) {
        el('line', { x1: f.e1[0], y1: f.e1[1], x2: f.e2[0], y2: f.e2[1], class: 'cx-line' }, ink);
        label(ink, add(add(f.e2, mul(f.nB, -12)), mul(f.u, 24)), 'd′', 'cx-label');
      }
      if (i >= 1) for (var a = 0; a < k; a++) arc(f.arcs[a]);
      if (i >= 2) arc(f.arcs[k]);
      if (i >= 3) arc(f.arcs[k + 1]);
      if (i >= 1) {
        var off = mul(f.nB, f.on ? -0.8 : 0.9);              // clear of the arc through P and Q
        point(ink, f.P, 'P', add(mul(f.u, -0.9), off));
        point(ink, f.Q, 'Q', add(mul(f.u, 0.9), off));
      }
      if (i >= 3 && f.meet) point(ink, f.B, 'B', add(f.u, mul(f.nB, 0.3)), 'cx-pt-m');
      if (i >= 5 && f.meet && !f.on) point(ink, f.H, 'H', add(mul(f.u, -1), mul(f.nA, 0.9)), 'cx-pt-m');
      point(ink, f.A, 'A', f.on ? add(mul(f.u, -0.45), mul(f.nA, 1)) : add(mul(f.u, -1), mul(f.nA, 0.3)), null, 'A');
      el('circle', { cx: f.D[0], cy: f.D[1], r: 7, class: 'cx-handle' }, ink);
      el('circle', { cx: f.D[0], cy: f.D[1], r: 24, class: 'cx-grab', 'data-drag': 'D' }, ink);
    },
    anim: function (f, i) {
      var k = f.nFirst;
      if (i === 1) return { arcs: k === 2 ? [0, 1] : [0] };
      if (i === 2) return { arcs: [k] };
      if (i === 3) return { arcs: [k + 1] };
      if (i === 4 && f.meet) return { ruler: [f.e1, f.e2] };
      return null;
    },
  };

  // AB divided into n equal parts (Grade 9, lesson 15, Thales): n equal steps C, D, E ... on a
  // ray Ax; the last point is joined to B; the parallels through the others cut AB at C', D' ...
  var KM_COUNT = ['', '', 'ពីរ', 'បី', 'បួន', 'ប្រាំ', 'ប្រាំមួយ'];
  var kmDigits = function (n) { return String(n).replace(/\d/g, function (d) { return '០១២៣៤៥៦៧៨៩'[d]; }); };
  var joinKm = function (a) { return a.length < 2 ? a.join('') : a.slice(0, -1).join(', ') + ' និង ' + a[a.length - 1]; };
  var stepName = function (j) { return 'CDEFGH'[j - 1]; };
  function divideOk(A, B, X) {
    var a = sub(B, A), b = sub(X, A), la = len(a), lb = len(b);
    var ang = Math.acos(Math.max(-1, Math.min(1, (a[0] * b[0] + a[1] * b[1]) / (la * lb)))) * 180 / Math.PI;
    return la >= 170 && lb >= 200 && ang >= 20 && ang <= 140;
  }
  CX['divide-segment'] = {
    steps: 6,
    start: { A: [96, 344], B: [540, 344], X: [398, 96], k: 3 },
    kScale: 1,
    kOk: function () { return true; },
    kText: function (s) { return 'ចែកជា ' + kmDigits(s.k) + ' ចំណែកប៉ុនគ្នា'; },
    fill: function (s) {
      var n = s.k, pts = [], inner = [], img = [], eq = ['A' + stepName(1) + '′'];
      for (var j = 1; j <= n; j++) pts.push(stepName(j));
      for (j = n - 1; j >= 1; j--) { inner.push(stepName(j)); img.push(stepName(j) + '′'); }
      for (j = 1; j < n; j++) eq.push(stepName(j) + '′' + (j === n - 1 ? 'B' : stepName(j + 1) + '′'));
      var steps = ['A' + stepName(1)];
      for (j = 1; j < n; j++) steps.push(stepName(j) + stepName(j + 1));
      return { n: KM_COUNT[n], pts: joinKm(pts), last: stepName(n), inner: joinKm(inner), images: joinKm(img),
        eq: eq.join(' = '), steps: steps.join(' = ') };
    },
    limit: function (s, key, p) {
      return divideOk(key === 'A' ? p : s.A, key === 'B' ? p : s.B, key === 'X' ? p : s.X);
    },
    figure: function (s) {
      var A = s.A, B = s.B, n = s.k, u = unit(sub(s.X, A)), lx = len(sub(s.X, A)), v = unit(sub(B, A));
      var st = Math.max(26, Math.min(84, (lx - 34) / n)), K = [A], Kp = [A], arcs = [], rulers = [];
      var side = u[0] * v[1] - u[1] * v[0] > 0 ? 1 : -1;       // which side of Ax the point B is on
      var nx = mul([-u[1], u[0]], -side), nb = mul([-v[1], v[0]], side);   // away from B; away from Ax
      var ta = Math.atan2(u[1], u[0]);
      for (var j = 1; j <= n; j++) {
        K.push(add(A, mul(u, st * j)));
        Kp.push(add(A, mul(sub(B, A), j / n)));
        arcs.push({ c: K[j - 1], r: st, t1: ta - 0.24, t2: ta + 0.24 });
      }
      var w = unit(sub(B, K[n]));                             // the direction of EB and of every parallel
      for (j = n - 1; j >= 1; j--) rulers.push([add(K[j], mul(w, -18)), add(Kp[j], mul(w, 18))]);
      return { meet: true, n: n, A: A, B: B, X: s.X, u: u, v: v, w: w, nx: nx, nb: nb, K: K, Kp: Kp, st: st,
        Ex: add(A, mul(u, lx + 18)), arcs: arcs, rulers: rulers };
    },
    draw: function (f, i, g, layer) {
      var ink = layer.ink, marks = layer.marks, n = f.n, j;
      var seg = function (p, q, cls, to) { el('line', { x1: p[0], y1: p[1], x2: q[0], y2: q[1], class: cls }, to || ink); };
      if (i >= 5) {
        for (j = 1; j <= n; j++) { tick(marks, f.K[j - 1], f.K[j]); tick2(marks, f.Kp[j - 1], f.Kp[j]); }
        for (j = 1; j <= n; j++) {                           // an arrow head on each parallel
          var m = add(mul(add(f.K[j], f.Kp[j]), 0.5), mul(f.w, 5)), b = add(m, mul(f.w, -11)), t = [-f.w[1], f.w[0]];
          el('polyline', { points: [add(b, mul(t, 6)), m, add(b, mul(t, -6))].map(function (x) { return x.join(','); }).join(' '), class: 'cx-par' }, marks);
        }
      }
      seg(f.A, f.B, 'cx-seg');
      if (i >= 1) {
        seg(f.A, f.Ex, 'cx-line');
        label(ink, add(add(f.Ex, mul(f.u, -6)), mul(f.nx, 28)), 'x', 'cx-label');
      }
      if (i >= 3) seg(f.K[n], f.B, 'cx-line');
      if (i >= 4) f.rulers.forEach(function (q) { seg(q[0], q[1], 'cx-line cx-line-2'); });
      if (i >= 2) {
        f.arcs.forEach(function (q) { el('path', { d: arcPath(q.c, q.r, q.t1, q.t2), class: 'cx-arc' }, ink); });
        for (j = 1; j <= n; j++) {                           // the name clear of the little arc
          el('circle', { cx: f.K[j][0], cy: f.K[j][1], r: 5, class: 'cx-pt' }, ink);
          label(ink, add(f.K[j], add(mul(f.nx, 27), mul(f.u, -10))), stepName(j), 'cx-label');
        }
      }
      if (i >= 4) for (j = 1; j < n; j++) point(ink, f.Kp[j], stepName(j) + '′', f.nb, 'cx-pt-m');
      point(ink, f.A, 'A', add(mul(f.v, -1), mul(f.nb, 0.35)), null, 'A');
      point(ink, f.B, 'B', add(f.v, mul(f.nb, 0.35)), null, 'B');
      if (i >= 1) {
        el('circle', { cx: f.X[0], cy: f.X[1], r: 7, class: 'cx-handle' }, ink);
        el('circle', { cx: f.X[0], cy: f.X[1], r: 24, class: 'cx-grab', 'data-drag': 'X' }, ink);
      }
    },
    anim: function (f, i) {
      if (i === 1) return { ruler: [f.A, f.Ex] };
      if (i === 2) return { arcs: f.arcs.map(function (q, j) { return j; }) };
      if (i === 3) return { ruler: [f.K[f.n], f.B] };
      if (i === 4 && f.rulers.length) return { rulers: f.rulers, cls: 'cx-line cx-line-2' };
      return null;
    },
  };
  function tick2(g, p, q) {
    var m = mul(add(p, q), 0.5), u = unit(sub(q, p)), n = [u[1], -u[0]];
    [-3, 3].forEach(function (o) {
      var c = add(m, mul(u, o));
      el('line', { x1: c[0] - n[0] * 8, y1: c[1] - n[1] * 8, x2: c[0] + n[0] * 8, y2: c[1] + n[1] * 8, class: 'cx-tick' }, g);
    });
  }

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
    var step = 0, playing = false, timer = null, raf = null, kScale = def.kScale || 100;
    // the words of the captions that depend on the state (how many parts, which letters)
    function refill() {
      if (!def.fill) return;
      var words = def.fill(state);
      Array.prototype.forEach.call(root.querySelectorAll('[data-fill]'), function (e) {
        var w = words[e.getAttribute('data-fill')];
        if (w != null) e.textContent = w;
      });
    }
    refill();

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
        var lines = a.rulers || (a.ruler ? [a.ruler] : null);
        var t0 = null, dur = a.arcs ? (a.arcs.length > 3 ? 750 : 1100) : 1000, part = 0;
        var parts = a.arcs ? a.arcs.slice() : lines.map(function (q, j) { return j; });
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
            for (var jj = 0; jj < part; jj++) el('line', { x1: lines[jj][0][0], y1: lines[jj][0][1], x2: lines[jj][1][0], y2: lines[jj][1][1], class: a.cls || 'cx-line' }, drawn);
            var p = lines[part][0], q2 = lines[part][1], e = add(p, mul(sub(q2, p), ease(t)));
            drawRuler(tools, p, q2);
            el('line', { x1: p[0], y1: p[1], x2: e[0], y2: e[1], class: a.cls || 'cx-line' }, drawn);
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
      if (slider) { slider.value = Math.round(state.k * kScale); showK(); }
      go(0, false);
    });
    Array.prototype.forEach.call(root.querySelectorAll('[data-preset]'), function (b) {
      b.addEventListener('click', function () {
        var set = def.presets && def.presets[b.getAttribute('data-preset')];
        if (!set) return;
        stopPlay(); stopAnim();
        set(state);
        render(step);
      });
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
      if (def.kSnap) slider.value = def.kSnap(+slider.value);
      state.k = slider.value / kScale;
      var ok = def.kOk ? def.kOk(state.k) : state.k > 0.5;
      kOut.textContent = def.kText ? def.kText(state) : ok ? root.getAttribute('data-k-ok') : root.getAttribute('data-k-short');
      kOut.classList.toggle('bad', !ok);
      refill();
    }
    if (slider) {
      slider.value = Math.round(state.k * kScale);
      showK();
      slider.addEventListener('input', function () { stopPlay(); stopAnim(); showK(); caption(); render(step); });
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
      if (def.place) p = def.place(state, dragging, p);
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
