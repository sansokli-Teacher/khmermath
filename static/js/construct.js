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
 * the slider (100 by default), kText(state, words) the line under it (words: what the page
 * says for a good or a bad value); fill(state) gives the
 * words for the <span data-fill="KEY"> of the captions when they depend on the state.
 * anim() may return { rulers: [[p, q], ...] } to draw several lines one after another, or
 * { phases: [{ dur, draw(t, drawn, tools) }, ...] } for a movement of its own (the set square).
 * A page may hold several constructions, one shown at a time: a <div class="cx-tabs"> of
 * role="tab" buttons, each naming its .cx by aria-controls (the special angles).
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
  var ease = function (t) { return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2; };
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
    return hinge;
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

  // A set square: its right angle at c, one side of the right angle along w (the edge that is
  // drawn along), the other along p (the edge that rests against the ruler).
  function drawSetSquare(g, c, w, p, lw, lp, alpha) {
    var a = add(c, mul(w, lw)), b = add(c, mul(p, lp)), m = mul(add(add(c, a), b), 1 / 3);
    var grp = el('g', { opacity: alpha == null ? 1 : alpha }, g);
    var pts = function (list) { return list.map(function (x) { return x[0].toFixed(1) + ',' + x[1].toFixed(1); }).join(' '); };
    var inner = [c, a, b].map(function (x) { return add(m, mul(sub(x, m), 0.42)); });
    // one shape with a hole, so that what lies under the hole stays readable
    var ring = function (list) { return 'M' + list.map(function (x) { return x[0].toFixed(1) + ' ' + x[1].toFixed(1); }).join('L') + 'Z'; };
    el('path', { d: ring([c, a, b]) + ring(inner), 'fill-rule': 'evenodd', class: 'cx-sq' }, grp);
    el('polyline', { points: pts([add(c, mul(w, 12)), add(add(c, mul(w, 12)), mul(p, 12)), add(c, mul(p, 12))]), class: 'cx-sq-in' }, grp);
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
  // The parallels are drawn as Grade 7 lesson 14 does: the set square laid on EB, a ruler against
  // its other side, and the set square slid along the ruler to each point.
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
    steps: 7,
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
      return { n: KM_COUNT[n], pts: joinKm(pts), last: stepName(n), first: inner[0], firstImg: img[0],
        more: n > 2 ? ' ធ្វើដូចគ្នាចំពោះចំណុច ' + joinKm(inner.slice(1)) + '៖ បានចំណុច ' + joinKm(img.slice(1)) + '។' : '',
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
      // the set square: its right angle slides on a line perpendicular to EB, behind the points of Ax
      var dot = function (a, b) { return a[0] * b[0] + a[1] * b[1]; };
      var d = [-w[1], w[0]], pd = dot(sub(A, K[n]), d) < 0 ? d : mul(d, -1), back = 1e9, reach = -1e9;
      for (j = 1; j <= n; j++) back = Math.min(back, dot(K[j], w));
      back -= 58;                                            // clear of the names C, D, E ...
      for (j = 1; j < n; j++) reach = Math.max(reach, dot(Kp[j], w));
      var lw = Math.max(210, Math.min(380, reach - back + 16)), lp = lw * 0.56, cor = [null], c0, lo = 1e9, hi = -1e9;
      for (j = 1; j <= n; j++) cor.push(add(K[j], mul(w, back - dot(K[j], w))));
      for (j = 1; j <= n; j++) {
        c0 = dot(sub(cor[j], cor[n]), d);
        lo = Math.min(lo, c0, c0 + dot(pd, d) * lp); hi = Math.max(hi, c0, c0 + dot(pd, d) * lp);
      }
      return { meet: true, n: n, A: A, B: B, X: s.X, u: u, v: v, w: w, nx: nx, nb: nb, K: K, Kp: Kp, st: st,
        Ex: add(A, mul(u, lx + 18)), arcs: arcs, rulers: rulers,
        sq: { cor: cor, pd: pd, lw: lw, lp: lp, r1: add(cor[n], mul(d, lo)), r2: add(cor[n], mul(d, hi)) } };
    },
    draw: function (f, i, g, layer) {
      var ink = layer.ink, marks = layer.marks, n = f.n, j;
      var seg = function (p, q, cls, to) { el('line', { x1: p[0], y1: p[1], x2: q[0], y2: q[1], class: cls }, to || ink); };
      if (i >= 6) {
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
      if (i >= 5) f.rulers.forEach(function (q) { seg(q[0], q[1], 'cx-line cx-line-2'); });
      if (i >= 2) {
        f.arcs.forEach(function (q) { el('path', { d: arcPath(q.c, q.r, q.t1, q.t2), class: 'cx-arc' }, ink); });
        for (j = 1; j <= n; j++) {                           // the name clear of the little arc
          el('circle', { cx: f.K[j][0], cy: f.K[j][1], r: 5, class: 'cx-pt' }, ink);
          label(ink, add(f.K[j], add(mul(f.nx, 27), mul(f.u, -10))), stepName(j), 'cx-label');
        }
      }
      if (i >= 5) for (j = 1; j < n; j++) point(ink, f.Kp[j], stepName(j) + '′', f.nb, 'cx-pt-m');
      point(ink, f.A, 'A', add(mul(f.v, -1), mul(f.nb, 0.35)), null, 'A');
      point(ink, f.B, 'B', add(f.v, mul(f.nb, 0.35)), null, 'B');
      if (i >= 1) {
        el('circle', { cx: f.X[0], cy: f.X[1], r: 7, class: 'cx-handle' }, ink);
        el('circle', { cx: f.X[0], cy: f.X[1], r: 24, class: 'cx-grab', 'data-drag': 'X' }, ink);
      }
      // the ruler and the set square: laid on EB (step 5), left where the last parallel was drawn (step 6)
      if (i === 4 || i === 5) {
        drawRuler(layer.tools, f.sq.r1, f.sq.r2);
        drawSetSquare(layer.tools, f.sq.cor[i === 4 ? n : 1], f.w, f.sq.pd, f.sq.lw, f.sq.lp);
      }
    },
    anim: function (f, i) {
      var q = f.sq, n = f.n, line = function (a, b, to) { el('line', { x1: a[0], y1: a[1], x2: b[0], y2: b[1], class: 'cx-line cx-line-2' }, to); };
      if (i === 1) return { ruler: [f.A, f.Ex] };
      if (i === 2) return { arcs: f.arcs.map(function (a, j) { return j; }) };
      if (i === 3) return { ruler: [f.K[n], f.B] };
      if (i === 4) return { phases: [                         // the set square comes onto EB, then the ruler against it
        { dur: 900, draw: function (t, drawn, tools) { drawSetSquare(tools, add(q.cor[n], mul(q.pd, 46 * (1 - t))), f.w, q.pd, q.lw, q.lp, 0.25 + 0.75 * t); } },
        { dur: 900, draw: function (t, drawn, tools) {
          var off = mul(f.w, -40 * (1 - t)), grp = el('g', { opacity: 0.25 + 0.75 * t }, tools);
          drawRuler(grp, add(q.r1, off), add(q.r2, off));
          drawSetSquare(tools, q.cor[n], f.w, q.pd, q.lw, q.lp);
        } },
      ] };
      if (i === 5) {                                          // slide to each point, draw along the edge
        var phases = [];
        f.rulers.forEach(function (r, k) {
          var j = n - 1 - k, from = q.cor[j + 1], to = q.cor[j];
          var done = function (drawn) { for (var m = 0; m < k; m++) line(f.rulers[m][0], f.rulers[m][1], drawn); };
          phases.push({ dur: 1000, draw: function (t, drawn, tools) {
            done(drawn);
            drawRuler(tools, q.r1, q.r2);
            drawSetSquare(tools, add(from, mul(sub(to, from), t)), f.w, q.pd, q.lw, q.lp);
          } });
          phases.push({ dur: 1000, draw: function (t, drawn, tools) {
            var e = add(r[0], mul(sub(r[1], r[0]), t));
            done(drawn);
            line(r[0], e, drawn);
            drawRuler(tools, q.r1, q.r2);
            drawSetSquare(tools, to, f.w, q.pd, q.lw, q.lp);
            el('circle', { cx: e[0], cy: e[1], r: 4.2, class: 'cx-c-pencil' }, tools);
          } });
        });
        return { phases: phases };
      }
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
  function tick3(g, p, q) {
    var m = mul(add(p, q), 0.5), u = unit(sub(q, p)), n = [u[1], -u[0]];
    [-5, 0, 5].forEach(function (o) {
      var c = add(m, mul(u, o));
      el('line', { x1: c[0] - n[0] * 8, y1: c[1] - n[1] * 8, x2: c[0] + n[0] * 8, y2: c[1] + n[1] * 8, class: 'cx-tick' }, g);
    });
  }

  // The special angles on a ray Ox, with the compass and the ruler only (one page, a tab each).
  // 60°: an arc from O cuts Ox at A, the same opening from A cuts that arc at B, and OAB is an
  // equilateral triangle. 30°: the bisector of that angle (arcs of the same opening from B and
  // from A meet at C). 90°: Ox is extended beyond O, an arc from O cuts the line at P and Q, and
  // arcs of one radius from P and from Q meet at B, so OB is the mediator of PQ. 45°: the
  // bisector of that right angle (the half circle from O cuts Oy at R; arcs from Q and from R).
  function toEdge(p, u, least) {                           // from p along u to just inside the edge of the sheet
    var t = 1e9;
    if (u[0] > 1e-6) t = Math.min(t, (W - 26 - p[0]) / u[0]); else if (u[0] < -1e-6) t = Math.min(t, (26 - p[0]) / u[0]);
    if (u[1] > 1e-6) t = Math.min(t, (H - 26 - p[1]) / u[1]); else if (u[1] < -1e-6) t = Math.min(t, (26 - p[1]) / u[1]);
    return add(p, mul(u, Math.max(t, least || 0)));
  }
  var aimAt = function (from, to) { return Math.atan2(to[1] - from[1], to[0] - from[0]); };
  function rayFrame(s) {
    var u = unit(sub(s.X, s.O)), n = [u[1], -u[0]];        // n: towards the top of the sheet
    return { O: s.O, X: s.X, u: u, n: n, ax: Math.atan2(u[1], u[0]), Ex: toEdge(s.O, u, 240),
      // the direction that makes the angle t with Ox
      dir: function (t) { return add(mul(u, Math.cos(t)), mul(n, Math.sin(t))); } };
  }
  // the handle X only turns the ray Ox: between lo and hi degrees above the horizontal
  function rayLimit(lo, hi) {
    return function (s, key, p) {
      var v = sub(p, s.O), a = Math.atan2(-v[1], v[0]) * 180 / Math.PI;
      return len(v) >= 240 && a >= lo && a <= hi;
    };
  }
  function rayDraw(f, layer, t, name, cls) {               // the ray from O at the angle t, named at its end
    var d = f.dir(t), e = toEdge(f.O, d, 220);
    el('line', { x1: f.O[0], y1: f.O[1], x2: e[0], y2: e[1], class: cls || 'cx-line' }, layer);
    label(layer, add(add(e, mul(d, -14)), mul(f.dir(t + Math.PI / 2), 20)), name, 'cx-label');
    return e;
  }
  function rayGiven(f, ink) {
    el('line', { x1: f.O[0], y1: f.O[1], x2: f.Ex[0], y2: f.Ex[1], class: 'cx-seg' }, ink);
    label(ink, add(add(f.Ex, mul(f.u, -14)), mul(f.n, -22)), 'x', 'cx-label');
  }
  function rayHandle(f, ink) {
    el('circle', { cx: f.X[0], cy: f.X[1], r: 7, class: 'cx-handle' }, ink);
    el('circle', { cx: f.X[0], cy: f.X[1], r: 24, class: 'cx-grab', 'data-drag': 'X' }, ink);
  }
  var arcDraw = function (g, q) { el('path', { d: arcPath(q.c, q.r, q.t1, q.t2), class: 'cx-arc' }, g); };
  var dash = function (g, p, q) { el('line', { x1: p[0], y1: p[1], x2: q[0], y2: q[1], class: 'cx-equal' }, g); };
  var degrees = function (t) { return Math.round(t * 180 / Math.PI) + '°'; };

  function sixty(s) {
    var f = rayFrame(s), R = 180, r = s.k * R, th = 2 * Math.asin(Math.min(1, r / (2 * R)));
    var O = f.O, A = add(O, mul(f.u, R)), B = add(O, mul(f.dir(th), R));
    // C: the third corner of the equilateral triangle on AB, away from O
    var C = add(mul(add(A, B), 0.5), mul(f.dir(th / 2), r * Math.sqrt(3) / 2));
    f.meet = keptK(s.k); f.R = R; f.r = r; f.th = th; f.A = A; f.B = B; f.C = C;
    f.arcs = [
      { c: O, r: R, t1: f.ax + 0.12, t2: f.ax - Math.max(th, Math.PI / 3) - 0.24 },
      { c: A, r: r, t1: aimAt(A, B) + 0.26, t2: aimAt(A, B) - 0.26 },
      { c: B, r: r, t1: aimAt(B, C) - 0.26, t2: aimAt(B, C) + 0.26 },
      { c: A, r: r, t1: aimAt(A, C) + 0.26, t2: aimAt(A, C) - 0.26 },
    ];
    return f;
  }
  // half: the 30° page, which goes on to bisect the angle AOB
  function sixtyDef(half) {
    var last = half ? 6 : 4, lineAt = half ? 5 : 3;
    return {
      steps: last + 1,
      warnFrom: 2,
      start: { O: [half ? 96 : 130, 372], X: [half ? 560 : 580, 372], k: 1 },
      kOk: keptK, kSnap: snapK,
      limit: rayLimit(-8, 28),
      figure: sixty,
      draw: function (f, i, g, layer) {
        var ink = layer.ink, marks = layer.marks, th = half ? f.th / 2 : f.th;
        if (i >= last) {
          sector(marks, f.O, f.ax, -th, 74, 'a');
          if (half) { sector(marks, f.O, f.ax - th, -th, 74, 'b'); dash(marks, f.O, f.B); dash(marks, f.A, f.C); dash(marks, f.B, f.C); }
          else { dash(marks, f.A, f.B); tick(marks, f.O, f.A); tick(marks, f.O, f.B); (f.meet ? tick : tick2)(marks, f.A, f.B); }
          label(marks, add(f.O, mul(f.dir(th / 2), 112)), degrees(th), 'cx-note cx-r');
        }
        rayGiven(f, ink);
        if (i >= lineAt) rayDraw(f, ink, th, half ? 'z' : 'y');
        for (var a = 0; a < Math.min(i, half ? 4 : 2); a++) arcDraw(ink, f.arcs[a]);
        if (i >= 1) point(ink, f.A, 'A', add(mul(f.u, 0.8), mul(f.n, -0.8)));
        if (i >= 2) point(ink, f.B, 'B', f.dir(f.th + Math.PI / 4), half ? null : 'cx-pt-m');
        if (half && i >= 4) point(ink, f.C, 'C', f.dir(f.th / 2 - Math.PI / 2), 'cx-pt-m', null, 27);
        point(ink, f.O, 'O', add(mul(f.u, -0.75), mul(f.n, -0.66)));
        rayHandle(f, ink);
      },
      anim: function (f, i) {
        if (i >= 1 && i < lineAt) return { arcs: [i - 1] };
        if (i === lineAt) return { ruler: [f.O, toEdge(f.O, f.dir(half ? f.th / 2 : f.th), 220)] };
        return null;
      },
    };
  }
  CX['angle-60'] = sixtyDef(false);
  CX['angle-30'] = sixtyDef(true);

  function ninety(s) {
    var f = rayFrame(s), c = 110, r = s.k * 2 * c, meet = r > c + 0.5, h = meet ? Math.sqrt(r * r - c * c) : 0;
    var O = f.O, P = add(O, mul(f.u, -c)), Q = add(O, mul(f.u, c)), B = add(O, mul(f.n, h)), Rp = add(O, mul(f.n, c));
    var r2 = 1.15 * c, C = add(O, mul(f.dir(Math.PI / 4), c * Math.SQRT1_2 + Math.sqrt(r2 * r2 - c * c / 2)));
    var towards = meet ? B : add(O, mul(f.n, r * 0.75));
    f.meet = meet; f.c = c; f.r = r; f.P = P; f.Q = Q; f.B = B; f.Rp = Rp; f.C = C; f.L = add(O, mul(f.u, -c - 64));
    f.arcs = [
      { c: O, r: c, t1: f.ax - 0.3, t2: f.ax + 0.3 },                           // a mark at Q, a mark at P
      { c: O, r: c, t1: f.ax + Math.PI + 0.3, t2: f.ax + Math.PI - 0.3 },
      { c: O, r: c, t1: f.ax + 0.14, t2: f.ax - Math.PI - 0.14 },               // or the half circle through Q, R and P
      { c: P, r: r, t1: aimAt(P, towards) + 0.3, t2: aimAt(P, towards) - 0.3 },
      { c: Q, r: r, t1: aimAt(Q, towards) - 0.3, t2: aimAt(Q, towards) + 0.3 },
      { c: Q, r: r2, t1: aimAt(Q, C) + 0.3, t2: aimAt(Q, C) - 0.3 },
      { c: Rp, r: r2, t1: aimAt(Rp, C) - 0.3, t2: aimAt(Rp, C) + 0.3 },
    ];
    return f;
  }
  // half: the 45° page, which goes on to bisect the right angle xOy
  function ninetyDef(half) {
    var last = half ? 9 : 6, q = Math.PI / 2;
    return {
      steps: last + 1,
      warnFrom: 4,
      start: { O: [half ? 262 : 300, 378], X: [half ? 572 : 590, 378], k: half ? 0.95 : 0.8 },
      limit: rayLimit(-6, 18),
      figure: ninety,
      draw: function (f, i, g, layer) {
        var ink = layer.ink, marks = layer.marks, ok = f.meet, s = 15;
        if (i >= last && ok) {
          if (half) {
            sector(marks, f.O, f.ax, -q / 2, 54, 'a'); sector(marks, f.O, f.ax - q / 2, -q / 2, 54, 'b');
            dash(marks, f.Q, f.C); dash(marks, f.Rp, f.C);
            label(marks, add(f.O, mul(f.dir(q / 4), 84)), '45°', 'cx-note cx-r');
          } else {
            var p1 = add(f.O, mul(f.u, s)), p2 = add(p1, mul(f.n, s)), p3 = add(f.O, mul(f.n, s));
            el('polyline', { points: [p1, p2, p3].map(function (x) { return x.join(','); }).join(' '), class: 'cx-right' }, marks);
            dash(marks, f.P, f.B); dash(marks, f.Q, f.B); tick(marks, f.P, f.O); tick(marks, f.O, f.Q);
            label(marks, add(f.O, add(mul(f.u, 44), mul(f.n, 36))), '90°', 'cx-note cx-r');
          }
        }
        rayGiven(f, ink);
        if (i >= 1) {
          el('line', { x1: f.O[0], y1: f.O[1], x2: f.L[0], y2: f.L[1], class: 'cx-ext' }, ink);
          label(ink, add(add(f.L, mul(f.u, 12)), mul(f.n, -22)), 'x′', 'cx-label');
        }
        if (i >= 5 && ok) rayDraw(f, ink, q, 'y', half ? 'cx-line cx-line-2' : null);      // 45°: Oy is only on the way
        if (half && i >= 8 && ok) rayDraw(f, ink, q / 2, 'z');
        if (i >= 2) { if (half) arcDraw(ink, f.arcs[2]); else { arcDraw(ink, f.arcs[0]); arcDraw(ink, f.arcs[1]); } }
        if (i >= 3) arcDraw(ink, f.arcs[3]);
        if (i >= 4) arcDraw(ink, f.arcs[4]);
        if (half && ok && i >= 6) arcDraw(ink, f.arcs[5]);
        if (half && ok && i >= 7) arcDraw(ink, f.arcs[6]);
        if (i >= 2) {
          point(ink, f.P, 'P', add(mul(f.u, -1), mul(f.n, -0.85)));
          point(ink, f.Q, 'Q', add(f.u, mul(f.n, -0.85)));
        }
        if (i >= 4 && ok) point(ink, f.B, 'B', f.u, half ? null : 'cx-pt-m', null, 24);
        if (half && i >= 5 && ok) point(ink, f.Rp, 'R', add(mul(f.u, -1), mul(f.n, 0.8)), null, null, 24);
        if (half && i >= 7 && ok) point(ink, f.C, 'C', f.dir(-q / 2), 'cx-pt-m', null, 27);
        point(ink, f.O, 'O', mul(f.n, -1));
        rayHandle(f, ink);
      },
      anim: function (f, i) {
        if (i === 1) return { ruler: [f.O, f.L], cls: 'cx-ext' };
        if (i === 2) return { arcs: half ? [2] : [0, 1] };
        if (i === 3 || i === 4) return { arcs: [i] };
        if (!f.meet) return null;
        if (i === 5) return { ruler: [f.O, toEdge(f.O, f.n, 220)], cls: half ? 'cx-line cx-line-2' : null };
        if (half && (i === 6 || i === 7)) return { arcs: [i - 1] };
        if (half && i === 8) return { ruler: [f.O, toEdge(f.O, f.dir(q / 2), 220)] };
        return null;
      },
    };
  }
  CX['angle-90'] = ninetyDef(false);
  CX['angle-45'] = ninetyDef(true);

  // The line d' through A parallel to d (Grade 7, lesson 14 §5.2), one page with two tabs.
  // With the set square: one side of its right angle on d, a ruler against the other side, and
  // the set square slid along the ruler until that side passes through A (two lines perpendicular
  // to one line are parallel). The slider turns the ruler while the set square slides: the ruler
  // that slips. With the compass: AP = PQ = QB = BA, one opening, so APQB is a rhombus.
  var PAR = { C: [320, 285], reach: 270 };
  var dotp = function (a, b) { return a[0] * b[0] + a[1] * b[1]; };
  var turn = function (v, t) { var c = Math.cos(t), k = Math.sin(t); return [v[0] * c - v[1] * k, v[0] * k + v[1] * c]; };
  function parFrame(s) {
    var u = unit(sub(s.D, PAR.C)), n = [u[1], -u[0]], v = sub(s.A, PAR.C);    // n: towards the top of the sheet
    return { A: s.A, D: s.D, u: u, n: n, along: dotp(v, u), dist: dotp(v, n) };
  }
  // A stays above d, where the set square and the arcs have room; the handle D only turns the line
  function parLimit(s, key, p) {
    var f = parFrame(key === 'D' ? { A: s.A, D: p } : { A: p, D: s.D });
    return f.u[0] > 0 && Math.abs(Math.atan2(f.u[1], f.u[0])) <= 0.2 && f.along >= -140 && f.along <= 30 && f.dist >= 70 && f.dist <= 190;
  }
  function parPlace(s, key, p) { return key === 'D' ? add(PAR.C, mul(unit(sub(p, PAR.C)), PAR.reach)) : p; }
  function parGiven(f, ink) {
    var a = add(PAR.C, mul(f.u, -330)), b = add(PAR.C, mul(f.u, 330));
    el('line', { x1: a[0], y1: a[1], x2: b[0], y2: b[1], class: 'cx-seg' }, ink);
    label(ink, add(add(PAR.C, mul(f.u, 236)), mul(f.n, 20)), 'd', 'cx-label');
  }
  function parHandles(f, ink) {
    point(ink, f.A, 'A', add(f.n, mul(f.u, -0.4)), null, 'A');
    el('circle', { cx: f.D[0], cy: f.D[1], r: 7, class: 'cx-handle' }, ink);
    el('circle', { cx: f.D[0], cy: f.D[1], r: 24, class: 'cx-grab', 'data-drag': 'D' }, ink);
  }
  function arrowHead(g, m, w) {                            // the mark of parallel lines
    var b = add(m, mul(w, -11)), t = [-w[1], w[0]];
    el('polyline', { points: [add(b, mul(t, 6)), m, add(b, mul(t, -6))].map(function (x) { return x.join(','); }).join(' '), class: 'cx-par' }, g);
  }
  function rightMark(g, c, a, b) {
    var k = 13, p1 = add(c, mul(a, k)), p2 = add(p1, mul(b, k)), p3 = add(c, mul(b, k));
    el('polyline', { points: [p1, p2, p3].map(function (x) { return x.join(','); }).join(' '), class: 'cx-right' }, g);
  }
  CX['parallel'] = {
    steps: 6,
    warnFrom: 3,
    start: { A: [270, 135], D: [590, 285], k: 0 },
    kScale: 1,
    kOk: function (k) { return k === 0; },
    place: parPlace, limit: parLimit,
    figure: function (s) {
      var f = parFrame(s), u = f.u, n = f.n, lw = 290, lp = 136, phi = s.k * Math.PI / 180;
      var c0 = add(PAR.C, mul(u, -216)), reach = dotp(sub(s.A, c0), turn(n, phi));
      // the tools when the set square has gone the share t of its way along the ruler
      f.at = function (t) {
        var nt = turn(n, phi * t);
        return { c: add(c0, mul(nt, reach * t)), w: turn(u, phi * t), p: mul(nt, -1), r1: add(c0, mul(nt, 218)), r2: add(c0, mul(nt, 30 - lp)) };
      };
      f.meet = s.k === 0; f.c0 = c0; f.lw = lw; f.lp = lp; f.end = f.at(1);
      f.e1 = add(f.end.c, mul(f.end.w, 6)); f.e2 = add(f.end.c, mul(f.end.w, lw - 4));
      return f;
    },
    draw: function (f, i, g, layer) {
      var ink = layer.ink, marks = layer.marks, tools = layer.tools, q = f.at(0);
      if (i >= 5 && f.meet) {                              // both lines are perpendicular to the edge of the ruler
        dash(marks, add(f.c0, mul(f.n, -34)), add(f.end.c, mul(f.n, 34)));
        rightMark(marks, f.c0, f.u, f.n); rightMark(marks, f.end.c, f.u, f.n);
        arrowHead(marks, add(f.c0, mul(f.u, 48)), f.u); arrowHead(marks, add(f.end.c, mul(f.u, 48)), f.u);
      }
      parGiven(f, ink);
      if (i >= 4) {
        el('line', { x1: f.e1[0], y1: f.e1[1], x2: f.e2[0], y2: f.e2[1], class: 'cx-line' }, ink);
        label(ink, add(f.e2, mul(f.end.w, 22)), 'd′', 'cx-label');
      }
      parHandles(f, ink);
      if (i === 3 || i === 4) q = f.end;
      if (i >= 2 && i <= 4) drawRuler(tools, q.r1, q.r2);
      if (i >= 1 && i <= 4) drawSetSquare(tools, q.c, q.w, q.p, f.lw, f.lp);
    },
    anim: function (f, i) {
      var a0 = f.at(0), sq = function (tools, q) { drawSetSquare(tools, q.c, q.w, q.p, f.lw, f.lp); };
      if (i === 1) return { phases: [{ dur: 1000, draw: function (t, drawn, tools) {
        drawSetSquare(tools, add(a0.c, mul(f.n, -46 * (1 - t))), a0.w, a0.p, f.lw, f.lp, 0.25 + 0.75 * t);
      } }] };
      if (i === 2) return { phases: [{ dur: 1000, draw: function (t, drawn, tools) {
        var off = mul(f.u, -40 * (1 - t)), grp = el('g', { opacity: 0.25 + 0.75 * t }, tools);
        drawRuler(grp, add(a0.r1, off), add(a0.r2, off));
        sq(tools, a0);
      } }] };
      if (i === 3) return { phases: [{ dur: 1700, draw: function (t, drawn, tools) {
        var q = f.at(t);
        drawRuler(tools, q.r1, q.r2);
        sq(tools, q);
      } }] };
      if (i === 4) return { phases: [{ dur: 1300, draw: function (t, drawn, tools) {
        var e = add(f.e1, mul(sub(f.e2, f.e1), t));
        el('line', { x1: f.e1[0], y1: f.e1[1], x2: e[0], y2: e[1], class: 'cx-line' }, drawn);
        drawRuler(tools, f.end.r1, f.end.r2);
        sq(tools, f.end);
        el('circle', { cx: e[0], cy: e[1], r: 4.2, class: 'cx-c-pencil' }, tools);
      } }] };
      return null;
    },
  };
  CX['parallel-compass'] = {
    steps: 7,
    warnFrom: 4,
    start: { A: [250, 145], D: [590, 285], k: 1 },
    kOk: keptK, kSnap: snapK,
    place: parPlace, limit: parLimit,
    figure: function (s) {
      var f = parFrame(s), u = f.u, A = s.A, h = f.dist, r = Math.max(h + 35, 150), r2 = s.k * r;
      var foot = add(PAR.C, mul(u, f.along)), P = add(foot, mul(u, -Math.sqrt(r * r - h * h))), Q = add(P, mul(u, r));
      // B: on the arcs of radius r2 from Q and from A, on the side of AQ away from P
      var M = mul(add(A, Q), 0.5), half = len(sub(Q, A)) / 2;
      var B = add(M, mul(unit(sub(M, P)), Math.sqrt(Math.max(r2 * r2 - half * half, 0)))), w = unit(sub(B, A));
      f.meet = keptK(s.k); f.P = P; f.Q = Q; f.B = B; f.w = w;
      f.L1 = toEdge(A, mul(w, -1)); f.L2 = toEdge(A, w);
      f.arcs = [
        { c: A, r: r, t1: aimAt(A, P) + 0.24, t2: aimAt(A, P) - 0.24 },
        { c: P, r: r, t1: aimAt(P, Q) - 0.22, t2: aimAt(P, Q) + 0.22 },
        { c: Q, r: r2, t1: aimAt(Q, B) + 0.26, t2: aimAt(Q, B) - 0.26 },
        { c: A, r: r2, t1: aimAt(A, B) - 0.26, t2: aimAt(A, B) + 0.26 },
      ];
      return f;
    },
    draw: function (f, i, g, layer) {
      var ink = layer.ink, marks = layer.marks, differ = f.meet ? tick : tick2;
      if (i >= 6) {
        dash(marks, f.A, f.P); dash(marks, f.Q, f.B);
        tick(marks, f.A, f.P); tick(marks, f.P, f.Q); differ(marks, f.Q, f.B); differ(marks, f.A, f.B);
        if (f.meet) { arrowHead(marks, add(f.Q, mul(f.u, 46)), f.u); arrowHead(marks, add(f.B, mul(f.w, 46)), f.w); }
      }
      parGiven(f, ink);
      if (i >= 5) {
        el('line', { x1: f.L1[0], y1: f.L1[1], x2: f.L2[0], y2: f.L2[1], class: 'cx-line' }, ink);
        label(ink, add(add(f.L2, mul(f.w, -16)), mul(f.n, 20)), 'd′', 'cx-label');
      }
      for (var a = 0; a < Math.min(i, 4); a++) arcDraw(ink, f.arcs[a]);
      if (i >= 1) point(ink, f.P, 'P', add(mul(f.u, -0.9), mul(f.n, -0.8)), null, null, 22);
      if (i >= 2) point(ink, f.Q, 'Q', add(mul(f.u, 0.8), mul(f.n, -1)), null, null, 22);
      if (i >= 4) point(ink, f.B, 'B', add(f.u, f.n), 'cx-pt-m', null, 24);
      parHandles(f, ink);
    },
    anim: function (f, i) {
      if (i >= 1 && i <= 4) return { arcs: [i - 1] };
      if (i === 5) return { ruler: [f.L1, f.L2] };
      return null;
    },
  };

  // Triangles from given measures (Grade 7 lesson 15 §2.5, Grade 8 lesson 12 §1.2), one page with
  // three tabs, drawn as the books do: a ruler with centimetres, a protractor, a compass.
  // Three sides: AB, then arcs of radius AC from A and BC from B (the slider is BC: no triangle
  // unless |AB - AC| < BC < AB + AC). Two sides and the angle between them: AB, the angle at A
  // with the protractor, C on the ray at AC (the slider is the angle). A side and its two
  // angles: AB, an angle at A and one at B, the rays meet at C (the slider is the angle at B).
  var CM = 36, PR = 100;                                    // one centimetre and the protractor's radius, on the sheet
  var cmText = function (v) { return (Math.round(v * 10) / 10) + ' cm'; };
  var UP = [0, -1], DOWN = [0, 1], RIGHT = [1, 0], LEFT = [-1, 0];
  var segLine = function (g, p, q, cls) { return el('line', { x1: p[0], y1: p[1], x2: q[0], y2: q[1], class: cls }, g); };
  // a ruler with centimetre marks: its zero at p, laid along d, its body on the side nrm of the line
  function drawCmRuler(g, p, d, cm, nrm, alpha) {
    var grp = el('g', { opacity: alpha == null ? 1 : alpha }, g);
    var a = add(p, mul(d, -16)), b = add(p, mul(d, cm * CM + 16)), off = mul(nrm, 4), w = mul(nrm, 38);
    var pts = [add(a, off), add(b, off), add(add(b, off), w), add(add(a, off), w)];
    el('polygon', { points: pts.map(function (x) { return x[0].toFixed(1) + ',' + x[1].toFixed(1); }).join(' '), class: 'cx-ruler' }, grp);
    for (var h = 0; h <= cm * 2; h++) {
      var t = add(add(p, mul(d, h * CM / 2)), off);
      segLine(grp, t, add(t, mul(nrm, h % 2 ? 6 : 11)), 'cx-ruler-tick');
      if (h % 2 === 0) label(grp, add(t, mul(nrm, 23)), String(h / 2), 'cx-ruler-num');
    }
  }
  // a protractor on a horizontal line: its centre at c, its zero along u0, a mark at `mark` degrees
  function prDir(u0, deg) { var t = deg * Math.PI / 180; return add(mul(u0, Math.cos(t)), mul(UP, Math.sin(t))); }
  function drawProtractor(g, c, u0, mark, alpha) {
    var grp = el('g', { opacity: alpha == null ? 1 : alpha }, g), a = add(c, mul(u0, PR)), b = add(c, mul(u0, -PR));
    el('path', { d: 'M' + a.join(' ') + 'A' + PR + ' ' + PR + ' 0 0 ' + (u0[0] < 0 ? 1 : 0) + ' ' + b.join(' ') + 'Z', class: 'cx-pr' }, grp);
    for (var deg = 0; deg <= 180; deg += 5) {
      var d = prDir(u0, deg), rim = add(c, mul(d, PR));
      segLine(grp, rim, add(rim, mul(d, deg % 30 === 0 ? -12 : deg % 10 === 0 ? -8 : -4)), 'cx-pr-tick');
      if (deg % 30 === 0) label(grp, add(add(c, mul(d, PR - 25)), deg % 180 ? [0, 0] : [0, -9]), String(deg), 'cx-pr-num');   // 0 and 180 clear of the zero line
    }
    el('circle', { cx: c[0], cy: c[1], r: 3, class: 'cx-pr-c' }, grp);
    if (mark != null) {
      var m = prDir(u0, mark);
      segLine(grp, add(c, mul(m, PR - 13)), add(c, mul(m, PR + 2)), 'cx-pr-mark');
      label(grp, add(c, mul(m, PR + 30)), mark + '°', 'cx-note cx-r');
    }
  }
  var markAt = function (c, u0, deg) { return add(c, mul(prDir(u0, deg), PR + 8)); };   // the pencil dot beside the rim
  var dot = function (g, p, r) { el('circle', { cx: p[0], cy: p[1], r: r == null ? 3.4 : r, class: 'cx-mark' }, g); };
  function given(g, text) { el('text', { x: 22, y: 30, class: 'cx-given', 'dominant-baseline': 'central' }, g).textContent = text; }
  function wedge(g, c, t0, dt, rho, kind) {                // an angle, filled, without the tick of sector()
    var p1 = onCircle(c, rho, t0), p2 = onCircle(c, rho, t0 + dt);
    var arc = 'A' + rho + ' ' + rho + ' 0 0 ' + (dt > 0 ? 1 : 0) + ' ' + p2.join(' ');
    el('path', { d: 'M' + c.join(' ') + 'L' + p1.join(' ') + arc + 'Z', class: 'cx-sector cx-sector-' + kind }, g);
    el('path', { d: 'M' + p1.join(' ') + arc, class: 'cx-sector-edge cx-sector-edge-' + kind }, g);
  }
  function triFill(g, A, B, C) {
    el('polygon', { points: [A, B, C].map(function (x) { return x[0].toFixed(1) + ',' + x[1].toFixed(1); }).join(' '), class: 'cx-tri' }, g);
  }
  // the name of a side, beside its middle, away from the third corner
  function sideNote(g, p, q, other, text) {
    var m = mul(add(p, q), 0.5), u = unit(sub(q, p)), n = [-u[1], u[0]];
    if (dotp(n, sub(other, m)) > 0) n = mul(n, -1);
    label(g, add(m, mul(n, 16 + 16 * Math.abs(n[0]))), text, 'cx-note');   // further out beside a steep side: the words are wide
  }
  // the ruler comes under the line, then the pencil runs along it from p for `cm` centimetres
  function cmSegmentPhases(p, d, cm, rulerCm, nrm, cls) {
    var q = add(p, mul(d, cm * CM));
    return [
      { dur: 800, draw: function (t, drawn, tools) { drawCmRuler(tools, add(p, mul(nrm, 30 * (1 - t))), d, rulerCm, nrm, 0.25 + 0.75 * t); } },
      { dur: 1100, draw: function (t, drawn, tools) {
        var e = add(p, mul(sub(q, p), t));
        segLine(drawn, p, e, cls);
        drawCmRuler(tools, p, d, rulerCm, nrm);
        el('circle', { cx: e[0], cy: e[1], r: 4.2, class: 'cx-c-pencil' }, tools);
      } },
    ];
  }
  // the compass is opened to `cm` on the ruler (its zero at z), carried to the centre c, turned
  // with the pencil lifted to where the arc starts, and then draws the arc
  function compassPhases(z, cm, rulerCm, c, arc) {
    var r = cm * CM, turnTo = arc.t1;
    while (turnTo > Math.PI) turnTo -= 2 * Math.PI;
    while (turnTo < -Math.PI) turnTo += 2 * Math.PI;
    var ph = [{ dur: 1200, draw: function (t, drawn, tools) {
      drawCmRuler(tools, z, RIGHT, rulerCm, DOWN);
      drawCompass(tools, z, add(z, [Math.max(r * t, 8), 0]));
    } }];
    if (len(sub(c, z)) > 1) ph.push({ dur: 800, draw: function (t, drawn, tools) {
      var o = add(z, mul(sub(c, z), t));
      drawCmRuler(tools, z, RIGHT, rulerCm, DOWN, 1 - t);
      drawCompass(tools, o, add(o, [r, 0]));
    } });
    ph.push({ dur: 700, draw: function (t, drawn, tools) { drawCompass(tools, c, onCircle(c, r, turnTo * t)); } });
    ph.push({ dur: 1000, draw: function (t, drawn, tools) {
      var th = arc.t1 + (arc.t2 - arc.t1) * t;
      el('path', { d: arcPath(c, r, arc.t1, th), class: 'cx-arc' }, drawn);
      drawCompass(tools, c, onCircle(c, r, th));
    } });
    return ph;
  }
  // the protractor comes down on c, then the pencil marks the angle beside its rim
  function protractorPhases(c, u0, deg) {
    var m = markAt(c, u0, deg);
    return [
      { dur: 900, draw: function (t, drawn, tools) { drawProtractor(tools, add(c, [0, -34 * (1 - t)]), u0, null, 0.25 + 0.75 * t); } },
      { dur: 900, draw: function (t, drawn, tools) {
        drawProtractor(tools, c, u0, deg);
        dot(drawn, m, 3.4 * Math.min(1, t * 2));
        el('circle', { cx: m[0], cy: m[1], r: 4.2, class: 'cx-c-pencil', opacity: t < 0.85 ? 1 : 0 }, tools);
      } },
    ];
  }
  var triEnds = function (ink, f) {                         // A and B, named clear of the ruler under AB
    point(ink, f.A, 'A', f.ang > 100 ? [-0.8, 0.6] : [-0.85, -0.55], null, null, 22);   // and of a ray that leans to the left
    point(ink, f.B, 'B', [0.85, -0.55], null, null, 22);
  };

  CX['triangle-sss'] = {
    steps: 6,
    warnFrom: 3,
    start: { k: 3 },
    kScale: 2,
    kOk: function (k) { return k > 1 && k < 11; },
    kText: function (s, words) { return 'BC = ' + cmText(s.k) + ' — ' + words; },
    fill: function (s) { return { bc: String(s.k) }; },
    figure: function (s) {
      var A = [220, 350], ab = 6, ac = 5, bc = s.k, B = add(A, [ab * CM, 0]);
      var meet = bc > Math.abs(ab - ac) && bc < ab + ac, x = (ac * ac + ab * ab - bc * bc) / (2 * ab);
      var C = add(A, [x * CM, -Math.sqrt(Math.max(ac * ac - x * x, 0)) * CM]);
      // where the arcs are drawn: through C, or (no triangle) where they come nearest to each other
      var tA = meet ? aimAt(A, C) : bc >= ab + ac ? Math.PI : 0, tB = meet ? aimAt(B, C) : Math.PI;
      var spread = function (r) { return Math.max(0.16, Math.min(1.1, 55 / r)); }, sA = spread(ac * CM), sB = spread(bc * CM);
      return { meet: meet, A: A, B: B, C: C, ab: ab, ac: ac, bc: bc,
        arcs: [{ c: A, r: ac * CM, t1: tA + sA, t2: tA - sA }, { c: B, r: bc * CM, t1: tB + sB, t2: tB - sB }] };
    },
    draw: function (f, i, g, layer) {
      var ink = layer.ink, marks = layer.marks, tools = layer.tools;
      given(ink, 'AB = ' + cmText(f.ab) + '    AC = ' + cmText(f.ac) + '    BC = ' + cmText(f.bc));
      if (i < 1) return;
      if (i >= 5 && f.meet) {
        triFill(marks, f.A, f.B, f.C);
        sideNote(marks, f.A, f.B, f.C, cmText(f.ab)); sideNote(marks, f.A, f.C, f.B, cmText(f.ac)); sideNote(marks, f.B, f.C, f.A, cmText(f.bc));
      }
      segLine(ink, f.A, f.B, 'cx-seg');
      if (i >= 4 && f.meet) { segLine(ink, f.A, f.C, 'cx-line'); segLine(ink, f.B, f.C, 'cx-line'); }
      [0, 1].forEach(function (j) {
        var q = f.arcs[j], e;
        if (i < j + 2) return;
        arcDraw(ink, q);
        if (i !== j + 2) return;                            // the opening, shown on the step that draws the arc
        e = onCircle(q.c, q.r, (q.t1 + q.t2) / 2 + (f.meet ? (j ? -1 : 1) * Math.min(0.2, 30 / q.r) : 0));
        segLine(marks, q.c, e, 'cx-radius');
        if (f.meet) sideNote(marks, q.c, e, add(q.c, [j ? -40 : 40, 60]), cmText(j ? f.bc : f.ac));
        else sideNote(marks, q.c, add(q.c, mul(sub(e, q.c), 0.7)), add(q.c, [0, -60]), cmText(j ? f.bc : f.ac));   // along AB: under it
      });
      triEnds(ink, f);
      if (i >= 3 && f.meet) point(ink, f.C, 'C', UP, 'cx-pt-m', null, 24);
      if (i === 1) drawCmRuler(tools, f.A, RIGHT, 11, DOWN);
    },
    anim: function (f, i) {
      if (i === 1) return { phases: cmSegmentPhases(f.A, RIGHT, f.ab, 11, DOWN, 'cx-seg') };
      if (i === 2) return { phases: compassPhases(f.A, f.ac, 11, f.A, f.arcs[0]) };
      if (i === 3) return { phases: compassPhases(f.A, f.bc, 11, f.B, f.arcs[1]) };
      if (i === 4 && f.meet) return { rulers: [[f.A, f.C], [f.B, f.C]] };
      return null;
    },
  };

  CX['triangle-sas'] = {
    steps: 7,
    start: { k: 60 },
    kScale: 1,
    kOk: function () { return true; },
    kText: function (s) {
      return '∠A = ' + s.k + '°  →  BC ≈ ' + cmText(Math.sqrt(16 + 36 - 48 * Math.cos(s.k * Math.PI / 180)));
    },
    fill: function (s) { return { a: String(s.k) }; },
    figure: function (s) {
      var A = [230, 372], ab = 4, ac = 6, B = add(A, [ab * CM, 0]), d = prDir(RIGHT, s.k);
      return { meet: true, A: A, B: B, C: add(A, mul(d, ac * CM)), ab: ab, ac: ac, ang: s.k, d: d,
        Ex: add(A, mul(d, (ac + 1.1) * CM)), M: markAt(A, RIGHT, s.k), nr: [d[1], -d[0]] };   // nr: the side of Ax away from B
    },
    draw: function (f, i, g, layer) {
      var ink = layer.ink, marks = layer.marks, tools = layer.tools;
      given(ink, 'AB = ' + cmText(f.ab) + '    ∠A = ' + f.ang + '°    AC = ' + cmText(f.ac));
      if (i < 1) return;
      if (i >= 6) {
        triFill(marks, f.A, f.B, f.C);
        wedge(marks, f.A, 0, -f.ang * Math.PI / 180, 34, 'a');
        label(marks, add(f.A, mul(prDir(RIGHT, f.ang / 2), 56)), f.ang + '°', 'cx-note cx-r');
        sideNote(marks, f.A, f.B, f.C, cmText(f.ab)); sideNote(marks, f.A, f.C, f.B, cmText(f.ac));
      }
      segLine(ink, f.A, f.B, 'cx-seg');
      if (i >= 3) {
        segLine(ink, f.A, f.Ex, 'cx-line cx-line-2');
        label(ink, add(add(f.Ex, mul(f.d, -6)), mul(f.nr, 20)), 'x', 'cx-label');
      }
      if (i >= 5) segLine(ink, f.B, f.C, 'cx-line');
      if (i >= 6) segLine(ink, f.A, f.C, 'cx-line');
      if (i >= 2) dot(ink, f.M);
      triEnds(ink, f);
      if (i >= 4) point(ink, f.C, 'C', mul(f.nr, -1), 'cx-pt-m', null, 24);
      if (i === 1) drawCmRuler(tools, f.A, RIGHT, 5, DOWN);
      if (i === 2) drawProtractor(tools, f.A, RIGHT, f.ang);
      if (i === 4) drawCmRuler(tools, f.A, f.d, 7, f.nr);
    },
    anim: function (f, i) {
      if (i === 1) return { phases: cmSegmentPhases(f.A, RIGHT, f.ab, 5, DOWN, 'cx-seg') };
      if (i === 2) return { phases: protractorPhases(f.A, RIGHT, f.ang) };
      if (i === 3) return { ruler: [f.A, f.Ex], cls: 'cx-line cx-line-2' };
      if (i === 4) return { phases: [
        { dur: 800, draw: function (t, drawn, tools) { drawCmRuler(tools, add(f.A, mul(f.nr, 30 * (1 - t))), f.d, 7, f.nr, 0.25 + 0.75 * t); } },
        { dur: 900, draw: function (t, drawn, tools) {
          drawCmRuler(tools, f.A, f.d, 7, f.nr);
          el('circle', { cx: f.C[0], cy: f.C[1], r: 5 * Math.min(1, t * 2), class: 'cx-pt cx-pt-m' }, drawn);
          el('circle', { cx: f.C[0], cy: f.C[1], r: 4.2, class: 'cx-c-pencil', opacity: t < 0.85 ? 1 : 0 }, tools);
        } },
      ] };
      if (i === 5) return { ruler: [f.B, f.C] };
      return null;
    },
  };

  CX['triangle-asa'] = {
    steps: 7,
    start: { k: 40 },
    kScale: 1,
    kOk: function () { return true; },
    kText: function (s) { return '∠B = ' + s.k + '°  →  ∠C = 180° − 60° − ' + s.k + '° = ' + (120 - s.k) + '°'; },
    fill: function (s) { return { b: String(s.k) }; },
    figure: function (s) {
      var A = [200, 384], ab = 6, a = 60, b = s.k, B = add(A, [ab * CM, 0]), rad = Math.PI / 180;
      var dA = prDir(RIGHT, a), dB = prDir(LEFT, b), ac = ab * Math.sin(b * rad) / Math.sin((a + b) * rad);
      var C = add(A, mul(dA, ac * CM));
      return { meet: true, A: A, B: B, C: C, ab: ab, a: a, b: b, dA: dA, dB: dB,
        Ex: add(C, mul(dA, 46)), Ey: add(C, mul(dB, 46)), MA: markAt(A, RIGHT, a), MB: markAt(B, LEFT, b) };
    },
    draw: function (f, i, g, layer) {
      var ink = layer.ink, marks = layer.marks, tools = layer.tools, rad = Math.PI / 180;
      given(ink, 'AB = ' + cmText(f.ab) + '    ∠A = ' + f.a + '°    ∠B = ' + f.b + '°');
      if (i < 1) return;
      if (i >= 6) {
        triFill(marks, f.A, f.B, f.C);
        wedge(marks, f.A, 0, -f.a * rad, 34, 'a'); wedge(marks, f.B, Math.PI, f.b * rad, 34, 'b');
        label(marks, add(f.A, mul(prDir(RIGHT, f.a / 2), 56)), f.a + '°', 'cx-note cx-r');
        label(marks, add(f.B, mul(prDir(LEFT, f.b / 2), 60)), f.b + '°', 'cx-note cx-r');
        sideNote(marks, f.A, f.B, f.C, cmText(f.ab));
      }
      segLine(ink, f.A, f.B, 'cx-seg');
      if (i >= 3) {
        segLine(ink, f.A, f.Ex, 'cx-line cx-line-2');
        label(ink, add(f.Ex, mul([f.dA[1], -f.dA[0]], 18)), 'x', 'cx-label');
      }
      if (i >= 5) {
        segLine(ink, f.B, f.Ey, 'cx-line cx-line-2');
        label(ink, add(f.Ey, mul([-f.dB[1], f.dB[0]], 18)), 'y', 'cx-label');
      }
      if (i >= 6) { segLine(ink, f.A, f.C, 'cx-line'); segLine(ink, f.B, f.C, 'cx-line'); }
      if (i >= 2) dot(ink, f.MA);
      if (i >= 4) dot(ink, f.MB);
      triEnds(ink, f);
      if (i >= 5) point(ink, f.C, 'C', RIGHT, 'cx-pt-m', null, 26);
      if (i === 1) drawCmRuler(tools, f.A, RIGHT, 7, DOWN);
      if (i === 2) drawProtractor(tools, f.A, RIGHT, f.a);
      if (i === 4) drawProtractor(tools, f.B, LEFT, f.b);
    },
    anim: function (f, i) {
      if (i === 1) return { phases: cmSegmentPhases(f.A, RIGHT, f.ab, 7, DOWN, 'cx-seg') };
      if (i === 2) return { phases: protractorPhases(f.A, RIGHT, f.a) };
      if (i === 3) return { ruler: [f.A, f.Ex], cls: 'cx-line cx-line-2' };
      if (i === 4) return { phases: protractorPhases(f.B, LEFT, f.b) };
      if (i === 5) return { ruler: [f.B, f.Ey], cls: 'cx-line cx-line-2' };
      return null;
    },
  };

  // The circumscribed and the inscribed circle of a triangle (Grade 8, lesson 12), one page with two
  // tabs. Circumscribed: the mediators of AB and of BC meet at O, at the same distance from the
  // three corners; the circle of centre O through A. Inscribed: the bisectors of the angles A and B
  // meet at I, at the same distance from the three sides; that distance is found by the
  // perpendicular ID from I to AB; the circle of centre I and radius ID. The corners are dragged.
  function triangleOf(s) {
    var A = s.A, B = s.B, C = s.C, a = len(sub(B, C)), b = len(sub(C, A)), c = len(sub(A, B));
    var ang = function (x, y, z) { return Math.acos(Math.max(-1, Math.min(1, (y * y + z * z - x * x) / (2 * y * z)))); };
    var d = 2 * (A[0] * (B[1] - C[1]) + B[0] * (C[1] - A[1]) + C[0] * (A[1] - B[1])) || 1e-9;
    var qa = dotp(A, A), qb = dotp(B, B), qc = dotp(C, C);
    var O = [(qa * (B[1] - C[1]) + qb * (C[1] - A[1]) + qc * (A[1] - B[1])) / d, (qa * (C[0] - B[0]) + qb * (A[0] - C[0]) + qc * (B[0] - A[0])) / d];
    var I = mul(add(add(mul(A, a), mul(B, b)), mul(C, c)), 1 / (a + b + c));
    return { A: A, B: B, C: C, a: a, b: b, c: c, O: O, R: len(sub(A, O)), I: I, r: Math.abs(d) / 2 / (a + b + c),
      G: mul(add(add(A, B), C), 1 / 3), least: Math.min(a, b, c), angles: [ang(a, b, c), ang(b, c, a), ang(c, a, b)] };
  }
  function triDrawn(f, ink) {                              // the triangle, its corners named away from its middle
    [[f.A, f.B], [f.B, f.C], [f.C, f.A]].forEach(function (q) { segLine(ink, q[0], q[1], 'cx-seg'); });
  }
  function triCorners(f, ink) {
    ['A', 'B', 'C'].forEach(function (k) { point(ink, f[k], k, sub(f[k], f.G), null, k, 22); });
  }
  var footOn = function (P, A, B) { var u = unit(sub(B, A)); return add(A, mul(u, dotp(sub(P, A), u))); };
  // the compass is opened from its centre to a point, then draws the whole circle
  function circlePhases(c, through, cls) {
    var r = len(sub(through, c)), t0 = aimAt(c, through);
    return [
      { dur: 1000, draw: function (t, drawn, tools) { drawCompass(tools, c, add(c, mul(sub(through, c), Math.max(t, 0.06)))); } },
      { dur: 2400, draw: function (t, drawn, tools) {
        var th = t0 + (2 * Math.PI - 0.002) * t;
        el('path', { d: arcPath(c, r, t0, th), class: cls || 'cx-circle' }, drawn);
        drawCompass(tools, c, onCircle(c, r, th));
      } },
    ];
  }
  // the mediator of PQ with the compass: two marks from P, two from Q, and the line through the
  // crossings, drawn long enough to pass through O
  function mediatorOf(P, Q, O) {
    var M = mul(add(P, Q), 0.5), u = unit(sub(Q, P)), n = [u[1], -u[0]], half = len(sub(Q, P)) / 2, dO = dotp(sub(O, M), n);
    var inside = function (X) { return X[0] > 12 && X[0] < W - 12 && X[1] > 12 && X[1] < H - 12; }, r, h, X1, X2;
    // an opening whose crossings fall on the sheet and clear of O, so that O is not lost among the marks
    [1.25, 1.5, 1.12, 1.75, 1.25].some(function (k) {
      r = k * half; h = Math.sqrt(r * r - half * half); X1 = add(M, mul(n, h)); X2 = add(M, mul(n, -h));
      return Math.abs(h - Math.abs(dO)) >= 26 && inside(X1) && inside(X2);
    });
    var mark = function (c, X, sg) { var t = aimAt(c, X); return { c: c, r: r, t1: t - sg * 0.2, t2: t + sg * 0.2 }; };
    return { M: M, u: u, n: n, arcs: [mark(P, X1, 1), mark(P, X2, 1), mark(Q, X1, -1), mark(Q, X2, -1)],
      e1: add(M, mul(n, Math.max(h + 24, dO + 34))), e2: add(M, mul(n, Math.min(-h - 24, dO - 34))) };
  }
  CX['circumcircle'] = {
    steps: 7,
    start: { A: [200, 330], B: [460, 330], C: [370, 130] },
    presets: {
      acute: function (s) { s.A = [200, 330]; s.B = [460, 330]; s.C = [370, 130]; },
      right: function (s) { s.A = [200, 340]; s.B = [470, 340]; s.C = [200, 160]; },
      obtuse: function (s) { s.A = [210, 220]; s.B = [430, 220]; s.C = [300, 160]; },
    },
    // the triangle stays a triangle, and its circle stays on the sheet
    limit: function (s, key, p) {
      var t = triangleOf({ A: key === 'A' ? p : s.A, B: key === 'B' ? p : s.B, C: key === 'C' ? p : s.C });
      return t.least >= 100 && Math.min.apply(null, t.angles) >= 0.38 &&
        t.O[0] - t.R >= 6 && t.O[0] + t.R <= W - 6 && t.O[1] - t.R >= 6 && t.O[1] + t.R <= H - 6;
    },
    figure: function (s) {
      var f = triangleOf(s);
      f.meet = true; f.m1 = mediatorOf(f.A, f.B, f.O); f.m2 = mediatorOf(f.B, f.C, f.O); f.m3 = mediatorOf(f.C, f.A, f.O);
      f.arcs = f.m1.arcs.concat(f.m2.arcs);
      return f;
    },
    draw: function (f, i, g, layer) {
      var ink = layer.ink, marks = layer.marks;
      if (i >= 6) {
        dash(marks, f.m3.e1, f.m3.e2);                      // the third mediator passes through O too
        [f.A, f.B, f.C].forEach(function (P) { segLine(marks, f.O, P, 'cx-radius'); tick(marks, f.O, P); });
        [f.m1, f.m2, f.m3].forEach(function (m) { rightMark(marks, m.M, m.u, dotp(sub(f.G, m.M), m.n) > 0 ? m.n : mul(m.n, -1)); });
      }
      if (i === 5) segLine(marks, f.O, f.A, 'cx-radius');
      triDrawn(f, ink);
      if (i >= 5) el('circle', { cx: f.O[0], cy: f.O[1], r: f.R, class: 'cx-circle' }, ink);
      if (i >= 2) segLine(ink, f.m1.e1, f.m1.e2, 'cx-line cx-line-2');
      if (i >= 4) segLine(ink, f.m2.e1, f.m2.e2, 'cx-line cx-line-2');
      for (var a = 0; a < (i >= 3 ? 8 : i >= 1 ? 4 : 0); a++) arcDraw(ink, f.arcs[a]);
      triCorners(f, ink);
      if (i >= 4) point(ink, f.O, 'O', [-0.75, -0.66], 'cx-pt-m', null, 22);
    },
    anim: function (f, i) {
      if (i === 1) return { arcs: [0, 1, 2, 3] };
      if (i === 2) return { ruler: [f.m1.e1, f.m1.e2], cls: 'cx-line cx-line-2' };
      if (i === 3) return { arcs: [4, 5, 6, 7] };
      if (i === 4) return { ruler: [f.m2.e1, f.m2.e2], cls: 'cx-line cx-line-2' };
      if (i === 5) return { phases: circlePhases(f.O, f.A) };
      return null;
    },
  };

  // the bisector of the angle at V (its sides towards P and Q) with the compass, as far as past I
  function bisectorOf(V, P, Q, I) {
    var up = unit(sub(P, V)), uq = unit(sub(Q, V)), rho = Math.min(88, 0.42 * Math.min(len(sub(P, V)), len(sub(Q, V))));
    var P1 = add(V, mul(up, rho)), Q1 = add(V, mul(uq, rho)), chord = len(sub(Q1, P1)), r2 = Math.max(0.8 * chord, 40);
    var d = unit(sub(I, V)), T = add(mul(add(P1, Q1), 0.5), mul(d, Math.sqrt(r2 * r2 - chord * chord / 4)));
    var t1 = aimAt(V, P), dt = aimAt(V, Q) - t1;
    while (dt > Math.PI) dt -= 2 * Math.PI;
    while (dt < -Math.PI) dt += 2 * Math.PI;
    var sg = dt > 0 ? 1 : -1, mark = function (c, k) { var t = aimAt(c, T); return { c: c, r: r2, t1: t - k * 0.34, t2: t + k * 0.34 }; };
    return { T: T, d: d, end: add(I, mul(d, 44)),
      arcs: [{ c: V, r: rho, t1: t1 - sg * 0.14, t2: t1 + dt + sg * 0.14 }, mark(P1, 1), mark(Q1, -1)] };
  }
  CX['incircle'] = {
    steps: 9,
    start: { A: [130, 384], B: [530, 384], C: [350, 96] },
    // room for the arcs at each corner, and for the two marks on AB either side of D
    limit: function (s, key, p) {
      var t = triangleOf({ A: key === 'A' ? p : s.A, B: key === 'B' ? p : s.B, C: key === 'C' ? p : s.C });
      var reach = Math.sqrt(28 * t.r + 196) + 14, D = footOn(t.I, t.A, t.B);
      return t.least >= 170 && Math.min.apply(null, t.angles) >= 0.52 && t.r >= 46 &&
        len(sub(D, t.A)) >= reach && len(sub(D, t.B)) >= reach && footOn(t.I, t.A, t.B)[1] <= H - 62;
    },
    figure: function (s) {
      var f = triangleOf(s), u = unit(sub(f.B, f.A)), D = footOn(f.I, f.A, f.B), n = unit(sub(f.I, D));
      var r3 = f.r + 14, hc = Math.sqrt(r3 * r3 - f.r * f.r), U = add(D, mul(u, -hc)), V = add(D, mul(u, hc));
      var r4 = 1.28 * hc, Wp = add(D, mul(n, -Math.sqrt(r4 * r4 - hc * hc)));
      var mark = function (c, r, X, sp) { var t = aimAt(c, X); return { c: c, r: r, t1: t - sp, t2: t + sp }; };
      f.meet = true; f.bA = bisectorOf(f.A, f.B, f.C, f.I); f.bB = bisectorOf(f.B, f.C, f.A, f.I); f.bC = bisectorOf(f.C, f.A, f.B, f.I);
      f.D = D; f.E = footOn(f.I, f.B, f.C); f.F = footOn(f.I, f.C, f.A); f.U = U; f.V = V; f.Wp = Wp; f.u = u; f.n = n;
      f.arcs = f.bA.arcs.concat(f.bB.arcs, [mark(f.I, r3, U, 0.2), mark(f.I, r3, V, 0.2), mark(U, r4, Wp, 0.36), mark(V, r4, Wp, -0.36)]);
      return f;
    },
    draw: function (f, i, g, layer) {
      var ink = layer.ink, marks = layer.marks;
      if (i >= 8) {
        dash(marks, f.C, f.bC.end);                         // the third bisector passes through I too
        [[f.D, f.A, f.B], [f.E, f.B, f.C], [f.F, f.C, f.A]].forEach(function (q) {
          segLine(marks, f.I, q[0], 'cx-radius'); tick(marks, f.I, q[0]);
          rightMark(marks, q[0], unit(sub(q[2], q[1])), unit(sub(f.I, q[0])));
        });
      }
      if (i === 7) segLine(marks, f.I, f.D, 'cx-radius');
      triDrawn(f, ink);
      if (i >= 7) el('circle', { cx: f.I[0], cy: f.I[1], r: f.r, class: 'cx-circle' }, ink);
      if (i >= 2) segLine(ink, f.A, f.bA.end, 'cx-line cx-line-2');
      if (i >= 4) segLine(ink, f.B, f.bB.end, 'cx-line cx-line-2');
      if (i >= 6 && i < 8) segLine(ink, f.I, f.Wp, 'cx-line cx-line-2');
      for (var a = 0; a < (i >= 5 ? 10 : i >= 3 ? 6 : i >= 1 ? 3 : 0); a++) arcDraw(ink, f.arcs[a]);
      triCorners(f, ink);
      if (i >= 6) point(ink, f.D, 'D', add(mul(f.n, -1), mul(f.u, 0.9)), null, null, 22);
      if (i >= 8) {
        point(ink, f.E, 'E', sub(f.E, f.I), null, null, 22);
        point(ink, f.F, 'F', sub(f.F, f.I), null, null, 22);
      }
      if (i >= 4) point(ink, f.I, 'I', [1, -0.1], 'cx-pt-m', null, 24);
    },
    anim: function (f, i) {
      if (i === 1) return { arcs: [0, 1, 2] };
      if (i === 2) return { ruler: [f.A, f.bA.end], cls: 'cx-line cx-line-2' };
      if (i === 3) return { arcs: [3, 4, 5] };
      if (i === 4) return { ruler: [f.B, f.bB.end], cls: 'cx-line cx-line-2' };
      if (i === 5) return { arcs: [6, 7, 8, 9] };
      if (i === 6) return { ruler: [f.I, f.Wp], cls: 'cx-line cx-line-2' };
      if (i === 7) return { phases: circlePhases(f.I, f.D) };
      return null;
    },
  };

  // A tangent to a circle (Grade 9, lesson 13), one page with two tabs. At a point A of the
  // circle: the ray OA is drawn past A, and the perpendicular to it at A is built as for the right
  // angle (marks P and Q either side of A, arcs from P and from Q meeting at B). From a point P
  // outside: M is the middle of OP (its mediator); the circle of centre M through O cuts the
  // given circle at A and B; the angles OAP and OBP stand on a half circle, so they are right.
  var TAN = { O: [300, 240], R: 105, O2: [200, 250], R2: 100 };
  CX['tangent-at'] = {
    steps: 7,
    start: { A: [386, 180] },
    place: function (s, key, p) { return add(TAN.O, mul(unit(sub(p, TAN.O)), TAN.R)); },   // A stays on the circle
    figure: function (s) {
      var O = TAN.O, u = unit(sub(s.A, O)), A = add(O, mul(u, TAN.R)), n = [u[1], -u[0]], c = 60, r = 1.5 * c;
      var P = add(A, mul(u, -c)), Q = add(A, mul(u, c)), B = add(A, mul(n, Math.sqrt(r * r - c * c)));
      var reach = function (d) { return add(A, mul(d, Math.min(190, len(sub(toEdge(A, d), A))))); };
      var ax = Math.atan2(u[1], u[0]);
      return { meet: true, O: O, A: A, u: u, n: n, P: P, Q: Q, B: B, end: add(A, mul(u, c + 36)), T1: reach(mul(n, -1)), T2: reach(n),
        arcs: [
          { c: A, r: c, t1: ax + Math.PI - 0.3, t2: ax + Math.PI + 0.3 }, { c: A, r: c, t1: ax - 0.3, t2: ax + 0.3 },
          { c: P, r: r, t1: aimAt(P, B) - 0.3, t2: aimAt(P, B) + 0.3 }, { c: Q, r: r, t1: aimAt(Q, B) + 0.3, t2: aimAt(Q, B) - 0.3 },
        ] };
    },
    draw: function (f, i, g, layer) {
      var ink = layer.ink, marks = layer.marks;
      if (i >= 6) {
        segLine(marks, f.O, f.A, 'cx-radius');
        rightMark(marks, f.A, mul(f.u, -1), f.n);
        dash(marks, f.P, f.B); dash(marks, f.Q, f.B);
      }
      el('circle', { cx: f.O[0], cy: f.O[1], r: TAN.R, class: 'cx-ring' }, ink);
      if (i >= 1) segLine(ink, f.O, f.end, 'cx-line cx-line-2');
      if (i >= 5) segLine(ink, f.T1, f.T2, 'cx-line');
      for (var a = 0; a < (i >= 4 ? 4 : i >= 3 ? 3 : i >= 2 ? 2 : 0); a++) arcDraw(ink, f.arcs[a]);
      if (i >= 2) {
        point(ink, f.P, 'P', add(mul(f.u, -0.8), mul(f.n, -0.8)), null, null, 23);
        point(ink, f.Q, 'Q', add(mul(f.u, 0.8), mul(f.n, -0.8)), null, null, 23);
      }
      if (i >= 4) point(ink, f.B, 'B', add(f.n, mul(f.u, 0.9)), 'cx-pt-m', null, 23);
      point(ink, f.O, 'O', add(mul(f.u, -0.8), mul(f.n, -0.6)), null, null, 21);
      point(ink, f.A, 'A', add(mul(f.u, 0.5), mul(f.n, -0.9)), null, 'A', 21);
    },
    anim: function (f, i) {
      if (i === 1) return { ruler: [f.O, f.end], cls: 'cx-line cx-line-2' };
      if (i === 2) return { arcs: [0, 1] };
      if (i === 3 || i === 4) return { arcs: [i - 1] };
      if (i === 5) return { ruler: [f.T1, f.T2] };
      return null;
    },
  };
  CX['tangent-from'] = {
    steps: 7,
    start: { P: [500, 220] },
    // P stays outside the circle, and the circle on OP stays on the sheet
    limit: function (s, key, p) {
      var M = mul(add(TAN.O2, p), 0.5), h = len(sub(p, TAN.O2)) / 2;
      return 2 * h >= TAN.R2 + 70 && M[0] - h >= 6 && M[0] + h <= W - 6 && M[1] - h >= 6 && M[1] + h <= H - 6;
    },
    figure: function (s) {
      var O = TAN.O2, R = TAN.R2, P = s.P, d = len(sub(P, O)), e = unit(sub(P, O)), q = [e[1], -e[0]], M = mul(add(O, P), 0.5);
      var along = R * R / d, off = R * Math.sqrt(1 - R * R / (d * d));           // the touching points, from O
      var A = add(O, add(mul(e, along), mul(q, off))), B = add(O, add(mul(e, along), mul(q, -off)));
      var med = mediatorOf(O, P, M), past = function (X) { return add(X, mul(unit(sub(X, P)), 46)); };
      return { meet: true, O: O, P: P, M: M, A: A, B: B, e: e, q: q, half: d / 2, med: med, arcs: med.arcs, EA: past(A), EB: past(B) };
    },
    draw: function (f, i, g, layer) {
      var ink = layer.ink, marks = layer.marks;
      if (i >= 6) {
        [f.A, f.B].forEach(function (X) {
          segLine(marks, f.O, X, 'cx-radius');
          rightMark(marks, X, unit(sub(f.O, X)), unit(sub(f.P, X)));
          tick(marks, f.P, X);
        });
      }
      el('circle', { cx: f.O[0], cy: f.O[1], r: TAN.R2, class: 'cx-ring' }, ink);
      if (i >= 4) el('circle', { cx: f.M[0], cy: f.M[1], r: f.half, class: 'cx-arc' }, ink);
      if (i >= 1) segLine(ink, f.O, f.P, 'cx-line cx-line-2');
      if (i >= 3) segLine(ink, f.med.e1, f.med.e2, 'cx-line cx-line-2');
      if (i >= 5) { segLine(ink, f.P, f.EA, 'cx-line'); segLine(ink, f.P, f.EB, 'cx-line'); }
      if (i >= 2) f.arcs.forEach(function (a) { arcDraw(ink, a); });
      if (i >= 3) point(ink, f.M, 'M', add(mul(f.e, 0.75), mul(f.q, -0.7)), null, null, 22);
      if (i >= 4) {
        point(ink, f.A, 'A', add(mul(f.q, 1), mul(f.e, -0.5)), 'cx-pt-m', null, 23);
        point(ink, f.B, 'B', add(mul(f.q, -1), mul(f.e, -0.5)), 'cx-pt-m', null, 23);
      }
      point(ink, f.O, 'O', mul(f.e, -1), null, null, 21);
      point(ink, f.P, 'P', f.e, null, 'P', 21);
    },
    anim: function (f, i) {
      if (i === 1) return { ruler: [f.O, f.P], cls: 'cx-line cx-line-2' };
      if (i === 2) return { arcs: [0, 1, 2, 3] };
      if (i === 3) return { ruler: [f.med.e1, f.med.e2], cls: 'cx-line cx-line-2' };
      if (i === 4) return { phases: circlePhases(f.M, f.O, 'cx-arc') };
      if (i === 5) return { rulers: [[f.P, f.EA], [f.P, f.EB]] };
      return null;
    },
  };

  // The ellipse from its definition (Grade 12, conics): every point P with PF1 + PF2 = 2a. Two
  // pins at the foci, a string of length 2a tied to them, a pencil that keeps the string taut and
  // goes round. The string is 10 cm; the slider is the distance F1F2 (0: a circle). P is dragged
  // along the curve, and the two lengths are written on the sheet with their sum.
  var EL = { I: [320, 260], a: 5 };
  function ellipseOf(s) {
    var c = s.k / 2, a = EL.a, b = Math.sqrt(a * a - c * c), I = EL.I;
    var at = function (t) { return [I[0] + a * CM * Math.cos(t), I[1] - b * CM * Math.sin(t)]; };
    var t = Math.atan2(-(s.P[1] - I[1]) / b, (s.P[0] - I[0]) / a);
    return { meet: true, a: a, b: b, c: c, I: I, at: at, t: t, P: at(t), F1: [I[0] - c * CM, I[1]], F2: [I[0] + c * CM, I[1]] };
  }
  var cm1 = function (px) { return (Math.round(px / CM * 10) / 10) + ' cm'; };
  function ellipsePath(f, t1, t2) {
    var n = Math.max(2, Math.ceil(Math.abs(t2 - t1) / 0.06)), d = [];
    for (var j = 0; j <= n; j++) { var p = f.at(t1 + (t2 - t1) * j / n); d.push((j ? 'L' : 'M') + p[0].toFixed(1) + ' ' + p[1].toFixed(1)); }
    return d.join('');
  }
  function drawPin(g, p) {
    el('circle', { cx: p[0], cy: p[1], r: 7, class: 'cx-pin' }, g);
    el('circle', { cx: p[0] - 2, cy: p[1] - 2, r: 2, class: 'cx-pin-shine' }, g);
  }
  function drawPencil(g, p) {
    var d = unit([0.42, -0.91]), n = [-d[1], d[0]], q = function (along, side) { return add(add(p, mul(d, along)), mul(n, side)); };
    var pts = function (list) { return list.map(function (x) { return x[0].toFixed(1) + ',' + x[1].toFixed(1); }).join(' '); };
    el('polygon', { points: pts([q(13, -4.5), q(66, -4.5), q(66, 4.5), q(13, 4.5)]), class: 'cx-pencil' }, g);
    el('polygon', { points: pts([p, q(13, -4.5), q(13, 4.5)]), class: 'cx-pencil-tip' }, g);
    el('circle', { cx: p[0], cy: p[1], r: 2.4, class: 'cx-c-needle' }, g);
  }
  // the string from pin to pencil to pin, with the two lengths and their sum written above
  function tautString(g, f, P) {
    el('path', { d: 'M' + f.F1.join(' ') + 'L' + P[0].toFixed(1) + ' ' + P[1].toFixed(1) + 'L' + f.F2.join(' '), class: 'cx-string' }, g);
  }
  function sumNote(g, f, P) {
    var d1 = len(sub(P, f.F1)), d2 = len(sub(P, f.F2));
    el('text', { x: 22, y: 58, class: 'cx-given cx-sum', 'dominant-baseline': 'central' }, g).textContent =
      'PF₁ = ' + cm1(d1) + '    PF₂ = ' + cm1(d2) + '    PF₁ + PF₂ = ' + cm1(d1 + d2);
  }
  // the string hanging loose between the pins: a curve as long as the string
  function slackString(g, f) {
    var L = 2 * f.a * CM, A = f.F1, B = f.F2, mid = mul(add(A, B), 0.5);
    if (f.c === 0) {
      el('path', { d: 'M' + A.join(' ') + 'C' + (A[0] - L * 0.3) + ' ' + (A[1] + L * 0.42) + ' ' + (A[0] + L * 0.3) + ' ' + (A[1] + L * 0.42) + ' ' + A.join(' '), class: 'cx-string' }, g);
      return;
    }
    var lengthFor = function (sag) {
      var prev = A, sum = 0;
      for (var j = 1; j <= 40; j++) {
        var t = j / 40, x = (1 - t) * (1 - t) * A[0] + 2 * t * (1 - t) * mid[0] + t * t * B[0];
        var y = (1 - t) * (1 - t) * A[1] + 2 * t * (1 - t) * (mid[1] + sag) + t * t * B[1];
        sum += Math.hypot(x - prev[0], y - prev[1]); prev = [x, y];
      }
      return sum;
    };
    var lo = 0, hi = 500;
    for (var k = 0; k < 30; k++) { var m = (lo + hi) / 2; if (lengthFor(m) < L) lo = m; else hi = m; }
    el('path', { d: 'M' + A.join(' ') + 'Q' + mid[0] + ' ' + (mid[1] + lo).toFixed(1) + ' ' + B.join(' '), class: 'cx-string' }, g);
  }
  CX['ellipse'] = {
    steps: 6,
    start: { P: [EL.I[0] + 103, EL.I[1] - 118], k: 6 },
    kScale: 1,
    kOk: function () { return true; },
    kText: function (s, words) {
      var b = Math.sqrt(EL.a * EL.a - s.k * s.k / 4);
      return 'F₁F₂ = ' + s.k + ' cm  →  b = ' + (Math.round(b * 100) / 100) + ' cm' + (s.k === 0 ? ' — ' + words : '');
    },
    place: function (s, key, p) { return ellipseOf({ P: p, k: s.k }).P; },     // P stays on the curve
    figure: ellipseOf,
    draw: function (f, i, g, layer) {
      var ink = layer.ink, marks = layer.marks, tools = layer.tools, a = f.a * CM, b = f.b * CM;
      var V1 = f.at(Math.PI), V2 = f.at(0), B1 = f.at(Math.PI / 2), B2 = f.at(-Math.PI / 2);
      given(ink, 'F₁F₂ = 2c = ' + cm1(2 * f.c * CM) + '    ខ្សែ៖ 2a = ' + cm1(2 * a));
      if (i >= 3) sumNote(marks, f, f.P);
      if (i >= 5) {
        dash(marks, V1, V2); dash(marks, B1, B2);
        segLine(marks, f.P, f.F1, 'cx-radius'); segLine(marks, f.P, f.F2, 'cx-radius');
        label(marks, add(f.I, [a * 0.8, -15]), 'a', 'cx-note cx-r');
        label(marks, add(mul(add(f.I, B1), 0.5), [-14, 0]), 'b', 'cx-note cx-r');
        if (f.c) label(marks, add(mul(add(f.I, f.F1), 0.5), [0, 16]), 'c', 'cx-note cx-r');
      }
      if (i >= 4) el('path', { d: ellipsePath(f, 0, 2 * Math.PI) + 'Z', class: 'cx-circle' }, ink);
      if (i >= 5) {
        point(ink, f.I, 'I', [-0.5, -1], null, null, 20);
        point(ink, V1, 'V₁', LEFT, null, null, 24); point(ink, V2, 'V₂', RIGHT, null, null, 24);
        point(ink, B1, 'B₁', [0.75, 1], null, null, 23); point(ink, B2, 'B₂', [0.75, -1], null, null, 23);   // inside: clear of the lines of text
      }
      if (f.c) { point(ink, f.F1, 'F₁', [-0.3, 1], null, null, 24); point(ink, f.F2, 'F₂', [0.3, 1], null, null, 24); }
      else point(ink, f.F1, 'F₁ = F₂', [0, 1], null, null, 24);
      if (i >= 1 && i <= 4) { drawPin(ink, f.F1); drawPin(ink, f.F2); }
      if (i === 2) slackString(tools, f);
      if (i === 3 || i === 4) { tautString(tools, f, f.P); drawPencil(tools, f.P); }
      if (i >= 3) {
        el('circle', { cx: f.P[0], cy: f.P[1], r: 5, class: 'cx-pt cx-pt-m' }, tools);
        label(tools, i >= 5 ? add(f.P, mul(unit(sub(f.P, f.I)), 22)) : add(f.P, [-20, -13]), 'P', 'cx-label');   // beside the pencil
        el('circle', { cx: f.P[0], cy: f.P[1], r: 24, class: 'cx-grab', 'data-drag': 'P' }, tools);
      }
    },
    anim: function (f, i) {
      var fade = function (draw) { return function (t, drawn, tools) { draw(el('g', { opacity: 0.2 + 0.8 * t }, tools), t); }; };
      var hold = function (tools, t) { var P = f.at(t); tautString(tools, f, P); drawPencil(tools, P); sumNote(tools, f, P); return P; };
      if (i === 1) return { phases: [{ dur: 900, draw: function (t, drawn, tools) {
        [f.F1, f.F2].forEach(function (F) { drawPin(el('g', { opacity: t }, drawn), add(F, [0, -26 * (1 - t)])); });
      } }] };
      if (i === 2) return { phases: [{ dur: 1000, draw: fade(function (grp) { slackString(grp, f); }) }] };
      if (i === 3) return { phases: [
        { dur: 800, draw: fade(function (grp) { hold(grp, -Math.PI / 2); }) },                          // the pencil pulls the string tight
        { dur: 1500, draw: function (t, drawn, tools) { hold(tools, -Math.PI / 2 + (f.t + Math.PI / 2) * t); } },
      ] };
      if (i === 4) return { phases: [{ dur: 5600, draw: function (t, drawn, tools) {
        var now = f.t + 2 * Math.PI * t;
        el('path', { d: ellipsePath(f, f.t, now), class: 'cx-circle' }, drawn);
        hold(tools, now);
      } }] };
      return null;
    },
  };

  // ------------------------------------------------ figures of the lessons ---
  // A figure of a lesson, drawn step by step so that students see how it is made, is written as a
  // list: scripted({ steps, start, limit, figure(state), base(f, ink), top(f, ink), script(f) }).
  // script(f) gives, for each step, what that step adds:
  //   ['seg', P, Q, cls]                a line drawn along the ruler
  //   ['arc', {c, r, t1, t2}]           an arc drawn with the compass
  //   ['perp', P, A, B, cls]            the perpendicular from P to the line AB, along a set square slid on AB
  //   ['pt', P, name, dir, cls, dist]   a point and its name, once the step is drawn
  //   ['mark', function (g) { ... }]    marks (ticks, right angles, equal angles), behind the ink
  // The picture of step i is everything up to i; on arriving at a step its lines and arcs are drawn
  // one after another, each with its tool. A new figure is a figure() and this list, nothing more.
  // The perpendicular from P to AB as Grade 7 lesson 14 §5.1 draws it: one side of the right angle of
  // the set square on AB, the set square slid along AB until its other side passes through P.
  function perpPhases(P, A, B, cls) {
    var D = footOn(P, A, B), w = unit(sub(P, D)), far = len(sub(B, D)) > len(sub(A, D)) ? B : A, p = unit(sub(far, D));
    var lw = len(sub(P, D)) + 34, lp = Math.max(70, Math.min(0.62 * lw, len(sub(far, D)) + 30)), from = add(D, mul(p, 58));
    var sq = function (g, c, alpha) { drawSetSquare(g, c, w, p, lw, lp, alpha); };
    return [
      { dur: 700, draw: function (t, drawn, tools) { sq(tools, from, 0.2 + 0.8 * t); } },
      { dur: 900, draw: function (t, drawn, tools) { sq(tools, add(from, mul(sub(D, from), t))); } },
      { dur: 800, draw: function (t, drawn, tools) {
        var e = add(P, mul(sub(D, P), t));
        segLine(drawn, P, e, cls);
        sq(tools, D);
        el('circle', { cx: e[0], cy: e[1], r: 4.2, class: 'cx-c-pencil' }, tools);
      } },
    ];
  }
  function scripted(spec) {
    var inkOf = function (g, it) {
      if (it[0] === 'seg') segLine(g, it[1], it[2], it[3] || 'cx-line');
      else if (it[0] === 'arc') arcDraw(g, it[1]);
      else if (it[0] === 'perp') segLine(g, it[1], footOn(it[1], it[2], it[3]), it[4] || 'cx-perp');
      else if (it[0] === 'circ') el('circle', { cx: it[1][0], cy: it[1][1], r: len(sub(it[2], it[1])), class: 'cx-circle' }, g);
    };
    var drawnWithTool = function (it) { return it[0] === 'seg' || it[0] === 'arc' || it[0] === 'perp' || it[0] === 'circ'; };
    return {
      steps: spec.steps, start: spec.start, limit: spec.limit, place: spec.place, presets: spec.presets,
      figure: function (s) { var f = spec.figure(s); f.meet = true; f.script = spec.script(f); return f; },
      draw: function (f, i, g, layer) {
        var k;
        if (spec.base) spec.base(f, layer.ink, i);
        for (k = 0; k <= i; k++) f.script[k].forEach(function (it) {
          if (it[0] === 'mark') it[1](layer.marks); else if (it[0] !== 'pt') inkOf(layer.ink, it);
        });
        for (k = 0; k <= i; k++) f.script[k].forEach(function (it) {
          if (it[0] === 'pt') point(layer.ink, it[1], it[2], it[3], it[4], null, it[5]);
        });
        if (spec.top) spec.top(f, layer.ink, i);
      },
      anim: function (f, i) {
        var items = f.script[i].filter(drawnWithTool), phases = [];
        items.forEach(function (it, n) {
          var before = function (drawn) { for (var m = 0; m < n; m++) inkOf(drawn, items[m]); };
          if (it[0] === 'seg') phases.push({ dur: 950, draw: function (t, drawn, tools) {
            before(drawn);
            drawRuler(tools, it[1], it[2]);
            segLine(drawn, it[1], add(it[1], mul(sub(it[2], it[1]), t)), it[3] || 'cx-line');
          } });
          else if (it[0] === 'arc') phases.push({ dur: 900, draw: function (t, drawn, tools) {
            var q = it[1], th = q.t1 + (q.t2 - q.t1) * t;
            before(drawn);
            el('path', { d: arcPath(q.c, q.r, q.t1, th), class: 'cx-arc' }, drawn);
            drawCompass(tools, q.c, onCircle(q.c, q.r, th));
          } });
          else if (it[0] === 'circ') circlePhases(it[1], it[2], 'cx-circle').forEach(function (ph) {
            phases.push({ dur: ph.dur, draw: function (t, drawn, tools) { before(drawn); ph.draw(t, drawn, tools); } });
          });
          else perpPhases(it[1], it[2], it[3], it[4] || 'cx-perp').forEach(function (ph) {
            phases.push({ dur: ph.dur, draw: function (t, drawn, tools) { before(drawn); ph.draw(t, drawn, tools); } });
          });
        });
        return phases.length ? { phases: phases } : null;
      },
    };
  }
  // the two halves of the angle at V between VP and VQ, cut by VI: two arcs of one colour
  function halfAngles(g, V, P, Q, I, kind) {
    var turnTo = function (X, t0) { var d = aimAt(V, X) - t0; while (d > Math.PI) d -= 2 * Math.PI; while (d < -Math.PI) d += 2 * Math.PI; return d; };
    var tP = aimAt(V, P), tI = aimAt(V, I);
    wedge(g, V, tP, turnTo(I, tP), 34, kind);
    wedge(g, V, tI, turnTo(Q, tI), 40, kind);
  }
  var rightAt = function (g, D, I, A, B) { rightMark(g, D, unit(sub(I, D)), unit(sub(len(sub(B, D)) > len(sub(A, D)) ? B : A, D))); };

  // Grade 8, lesson 12, a worked example: the bisectors of the angles B and C of the triangle ABC
  // meet at I; the perpendiculars from I to AB, BC and AC meet them at D, E and F. (Then ID = IE = IF,
  // and AI bisects the angle A.)
  CX['g8-l12-incentre'] = scripted({
    steps: 9,
    start: { A: [300, 86], B: [116, 394], C: [550, 394] },
    limit: function (s, key, p) {
      var t = triangleOf({ A: key === 'A' ? p : s.A, B: key === 'B' ? p : s.B, C: key === 'C' ? p : s.C });
      return t.least >= 190 && Math.min.apply(null, t.angles) >= 0.56 && t.r >= 52;
    },
    figure: function (s) {
      var f = triangleOf(s);
      f.bB = bisectorOf(f.B, f.C, f.A, f.I); f.bC = bisectorOf(f.C, f.A, f.B, f.I);
      f.D = footOn(f.I, f.A, f.B); f.E = footOn(f.I, f.B, f.C); f.F = footOn(f.I, f.C, f.A);
      f.past = add(f.I, mul(unit(sub(f.I, f.A)), 46));
      return f;
    },
    base: function (f, ink) { triDrawn(f, ink); },
    top: function (f, ink) { triCorners(f, ink); },
    script: function (f) {
      var arcs = function (b) { return b.arcs.map(function (a) { return ['arc', a]; }); }, aux = 'cx-line cx-line-2';
      var foot = function (X, P, Q, name) {
        return [['perp', f.I, P, Q], ['mark', function (g) { rightAt(g, X, f.I, P, Q); }], ['pt', X, name, sub(X, f.I), null, 22]];
      };
      return [
        [],
        arcs(f.bB),
        [['seg', f.B, f.bB.end, aux], ['mark', function (g) { halfAngles(g, f.B, f.C, f.A, f.I, 'a'); }]],
        arcs(f.bC),
        [['seg', f.C, f.bC.end, aux], ['mark', function (g) { halfAngles(g, f.C, f.A, f.B, f.I, 'a'); }],
          ['pt', f.I, 'I', [0.55, 0.85], 'cx-pt-m', 25]],
        foot(f.D, f.A, f.B, 'D'), foot(f.E, f.B, f.C, 'E'), foot(f.F, f.C, f.A, 'F'),
        [['seg', f.A, f.past, 'cx-line'], ['mark', function (g) {
          [f.D, f.E, f.F].forEach(function (X) { tick(g, f.I, X); });
          halfAngles(g, f.A, f.B, f.C, f.I, 'b');
        }]],
      ];
    },
  });

  // Grade 8, lesson 17 §4.2: the excircles of a triangle. The external bisectors at B and C meet at J,
  // which is also on the internal bisector of A; the perpendiculars from J to the three side lines
  // are equal, so the circle of centre J touches them (the excircle opposite A). The external bisector
  // at A meets those at K and L, the centres of the other two excircles.
  CX['g8-l17-excircle'] = scripted({
    steps: 16,
    start: { A: [297, 127], B: [250, 211], C: [369, 211] },
    limit: function (s, key, p) {
      var t = triangleOf({ A: key === 'A' ? p : s.A, B: key === 'B' ? p : s.B, C: key === 'C' ? p : s.C });
      var ex = excentres(t), ok = Math.min.apply(null, t.angles) >= 0.6 && t.least >= 80;
      ex.forEach(function (e) { if (e.c[0] - e.r < 8 || e.c[0] + e.r > W - 8 || e.c[1] - e.r < 8 || e.c[1] + e.r > H - 8) ok = false; });
      return ok;
    },
    figure: function (s) {
      var f = triangleOf(s), ex = excentres(f), far = function (V, X) { return add(X, mul(unit(sub(X, V)), 42)); };
      f.J = ex[0].c; f.K = ex[1].c; f.L = ex[2].c;
      f.Bx = add(f.B, mul(unit(sub(f.B, f.A)), 95)); f.Cx = add(f.C, mul(unit(sub(f.C, f.A)), 95)); f.Ax = add(f.A, mul(unit(sub(f.A, f.B)), 95));
      f.bB = bisectorOf(f.B, f.C, f.Bx, f.J); f.bC = bisectorOf(f.C, f.B, f.Cx, f.J); f.bA = bisectorOf(f.A, f.C, f.Ax, f.K);
      f.D = footOn(f.J, f.A, f.B); f.E = footOn(f.J, f.A, f.C); f.F = footOn(f.J, f.B, f.C);
      f.Kf = footOn(f.K, f.A, f.C); f.Lf = footOn(f.L, f.A, f.B);
      f.far = far;
      return f;
    },
    base: function (f, ink) { triDrawn(f, ink); },
    top: function (f, ink) { triCorners(f, ink); },
    script: function (f) {
      var arcs = function (b) { return b.arcs.map(function (a) { return ['arc', a]; }); }, aux = 'cx-line cx-line-2';
      var outward = function (X) { return sub(X, f.G); };
      return [
        [],
        [['seg', f.B, f.Bx, 'cx-line'], ['seg', f.C, f.Cx, 'cx-line']],
        arcs(f.bB),
        [['seg', f.B, f.far(f.B, f.J), aux], ['mark', function (g) { halfAngles(g, f.B, f.C, f.Bx, f.J, 'a'); }]],
        arcs(f.bC),
        [['seg', f.C, f.far(f.C, f.J), aux], ['mark', function (g) { halfAngles(g, f.C, f.B, f.Cx, f.J, 'a'); }],
          ['pt', f.J, 'J', DOWN, 'cx-pt-m', 24]],
        [['perp', f.J, f.B, f.C], ['mark', function (g) { rightAt(g, f.F, f.J, f.B, f.C); }], ['pt', f.F, 'F', sub(f.F, f.J), null, 20]],
        [['perp', f.J, f.A, f.B], ['mark', function (g) { rightAt(g, f.D, f.J, f.A, f.B); }], ['pt', f.D, 'D', sub(f.D, f.J), null, 20],
          ['perp', f.J, f.A, f.C], ['mark', function (g) { rightAt(g, f.E, f.J, f.A, f.C); tick(g, f.J, f.D); tick(g, f.J, f.E); tick(g, f.J, f.F); }],
          ['pt', f.E, 'E', sub(f.E, f.J), null, 20]],
        [['circ', f.J, f.F]],
        [['seg', f.A, f.J, aux], ['mark', function (g) { halfAngles(g, f.A, f.B, f.C, f.J, 'b'); }]],
        [['seg', f.A, f.Ax, 'cx-line']].concat(arcs(f.bA)),
        [['seg', f.A, f.far(f.A, f.K), aux], ['seg', f.A, f.far(f.A, f.L), aux], ['mark', function (g) { halfAngles(g, f.A, f.C, f.Ax, f.K, 'a'); }]],
        [['seg', f.C, f.far(f.C, f.K), aux], ['seg', f.B, f.far(f.B, f.L), aux],
          ['pt', f.K, 'K', outward(f.K), 'cx-pt-m', 24], ['pt', f.L, 'L', outward(f.L), 'cx-pt-m', 24]],
        [['perp', f.K, f.A, f.C], ['mark', function (g) { rightAt(g, f.Kf, f.K, f.A, f.C); }], ['circ', f.K, f.Kf]],
        [['perp', f.L, f.A, f.B], ['mark', function (g) { rightAt(g, f.Lf, f.L, f.A, f.B); }], ['circ', f.L, f.Lf]],
        [],
      ];
    },
  });
  // the centres and radii of the three excircles (opposite A, B, C)
  function excentres(t) {
    var a = t.a, b = t.b, c = t.c, s = (a + b + c) / 2, area = t.r * s;
    return [[-a, b, c, area / (s - a)], [a, -b, c, area / (s - b)], [a, b, -c, area / (s - c)]].map(function (w) {
      var k = w[0] + w[1] + w[2];
      return { c: mul(add(add(mul(t.A, w[0]), mul(t.B, w[1])), mul(t.C, w[2])), 1 / k), r: w[3] };
    });
  }

  // Grade 8, lesson 12, a worked example: M is a point of the bisector of the angle XOY; the
  // perpendiculars from M meet OX at A and OY at B. (Then MA = MB.) The handle on OY turns that
  // side; M slides along the bisector.
  var G8B = { O: [90, 402], X: [596, 402], reach: 380 };     // reach: how far along OY its handle sits
  CX['g8-l12-bisector-point'] = scripted({
    steps: 6,
    start: { Y: [334, 111], M: [362, 275] },
    place: function (s, key, p) {
      if (key === 'Y') return add(G8B.O, mul(unit(sub(p, G8B.O)), G8B.reach));
      var d = unit(add(unit(sub(G8B.X, G8B.O)), unit(sub(s.Y, G8B.O))));      // M stays on the bisector
      return add(G8B.O, mul(d, Math.max(150, Math.min(330, dotp(sub(p, G8B.O), d)))));
    },
    limit: function (s, key, p) {
      if (key !== 'Y') return true;
      var v = sub(p, G8B.O), a = Math.atan2(-v[1], v[0]) * 180 / Math.PI;
      return a >= 34 && a <= 100;
    },
    figure: function (s) {
      var O = G8B.O, X = G8B.X, Y = s.Y, d = unit(add(unit(sub(X, O)), unit(sub(Y, O)))), M = add(O, mul(d, len(sub(s.M, O))));
      return { O: O, X: X, Y: Y, M: M, d: d, b: bisectorOf(O, X, Y, M), A: footOn(M, O, X), B: footOn(M, O, Y),
        Ey: toEdge(O, unit(sub(Y, O)), 400) };                 // the side OY runs to the edge of the sheet
    },
    base: function (f, ink) {
      segLine(ink, f.O, f.X, 'cx-seg'); segLine(ink, f.O, f.Ey, 'cx-seg');
      label(ink, add(f.X, [-10, 22]), 'X', 'cx-label');
      label(ink, add(add(f.Ey, mul(unit(sub(f.O, f.Ey)), 16)), mul([-f.d[1], f.d[0]], -24)), 'Y', 'cx-label');
    },
    top: function (f, ink, i) {
      point(ink, f.O, 'O', [-0.8, 0.7], null, null, 22);
      el('circle', { cx: f.Y[0], cy: f.Y[1], r: 7, class: 'cx-handle' }, ink);
      el('circle', { cx: f.Y[0], cy: f.Y[1], r: 24, class: 'cx-grab', 'data-drag': 'Y' }, ink);
      if (i >= 2) el('circle', { cx: f.M[0], cy: f.M[1], r: 24, class: 'cx-grab', 'data-drag': 'M' }, ink);
    },
    script: function (f) {
      return [
        [],
        f.b.arcs.map(function (a) { return ['arc', a]; }),
        [['seg', f.O, f.b.end, 'cx-line cx-line-2'], ['mark', function (g) { halfAngles(g, f.O, f.X, f.Y, f.M, 'a'); }],
          ['pt', f.M, 'M', [0.85, 0.6], 'cx-pt-m', 23]],
        [['perp', f.M, f.O, f.X], ['mark', function (g) { rightAt(g, f.A, f.M, f.O, f.X); }], ['pt', f.A, 'A', DOWN, null, 22]],
        [['perp', f.M, f.O, f.Y], ['mark', function (g) { rightAt(g, f.B, f.M, f.O, f.Y); }], ['pt', f.B, 'B', sub(f.B, f.M), null, 22]],
        [['mark', function (g) { tick(g, f.M, f.A); tick(g, f.M, f.B); }]],
      ];
    },
  });

  // Grade 8, lesson 12, a worked example: OZ bisects the angle XOY; A on OX and B on OY with
  // OA = OB; M on OZ, joined to A and to B. (The triangles OMA and OMB are congruent, so MA = MB.)
  CX['g8-l12-bisector-triangles'] = scripted({
    steps: 6,
    start: { Y: [334, 111], M: [384, 265] },
    place: CX['g8-l12-bisector-point'].place,
    limit: CX['g8-l12-bisector-point'].limit,
    figure: function (s) {
      var O = G8B.O, X = G8B.X, uy = unit(sub(s.Y, O)), d = unit(add([1, 0], uy)), M = add(O, mul(d, len(sub(s.M, O)))), R = 215;
      return { O: O, X: X, Y: s.Y, M: M, d: d, b: bisectorOf(O, X, s.Y, M), A: add(O, [R, 0]), B: add(O, mul(uy, R)),
        Ey: toEdge(O, uy, 400), Ez: add(O, mul(d, 400)), arc: { c: O, r: R, t1: 0.12, t2: Math.atan2(uy[1], uy[0]) - 0.12 } };
    },
    base: function (f, ink) {
      segLine(ink, f.O, f.X, 'cx-seg'); segLine(ink, f.O, f.Ey, 'cx-seg');
      label(ink, add(f.X, [-10, 22]), 'X', 'cx-label');
      label(ink, add(add(f.Ey, mul(unit(sub(f.O, f.Ey)), 16)), mul([-f.d[1], f.d[0]], -24)), 'Y', 'cx-label');
    },
    top: function (f, ink, i) {
      point(ink, f.O, 'O', [-0.8, 0.7], null, null, 22);
      el('circle', { cx: f.Y[0], cy: f.Y[1], r: 7, class: 'cx-handle' }, ink);
      el('circle', { cx: f.Y[0], cy: f.Y[1], r: 24, class: 'cx-grab', 'data-drag': 'Y' }, ink);
      if (i >= 2) label(ink, add(f.Ez, mul([-f.d[1], f.d[0]], 20)), 'Z', 'cx-label');
      if (i >= 4) el('circle', { cx: f.M[0], cy: f.M[1], r: 24, class: 'cx-grab', 'data-drag': 'M' }, ink);
    },
    script: function (f) {
      return [
        [],
        f.b.arcs.map(function (a) { return ['arc', a]; }),
        [['seg', f.O, f.Ez, 'cx-line cx-line-2'], ['mark', function (g) { halfAngles(g, f.O, f.X, f.Y, f.M, 'a'); }]],
        [['arc', f.arc], ['pt', f.A, 'A', [0.5, 1], null, 23], ['pt', f.B, 'B', [f.B[1] - f.O[1], f.O[0] - f.B[0]], null, 23]],
        [['pt', f.M, 'M', [0.9, 0.5], 'cx-pt-m', 23], ['seg', f.M, f.A], ['seg', f.M, f.B]],
        [['mark', function (g) {
          triFill(g, f.O, f.M, f.A); triFill(g, f.O, f.M, f.B);
          tick(g, f.O, f.A); tick(g, f.O, f.B); tick2(g, f.M, f.A); tick2(g, f.M, f.B);
        }]],
      ];
    },
  });


  // Grade 7, lesson 15 §2.4: the sum of the angles of a triangle and the exterior angle. The corners are
  // dragged; the angles are written with the numbers of the triangle on the sheet.
  var turnBy = function (t0, t1) { var d = t1 - t0; while (d > Math.PI) d -= 2 * Math.PI; while (d <= -Math.PI) d += 2 * Math.PI; return d; };
  var wedgeBetween = function (g, V, P, Q, rho, kind) { var t0 = aimAt(V, P); wedge(g, V, t0, turnBy(t0, aimAt(V, Q)), rho, kind); };
  function wholeDegrees(f) {                        // the three angles in whole degrees that still add up to 180
    var d = f.angles.map(function (x) { return x * 180 / Math.PI; }), r = d.map(Math.round), k;
    var diff = r[0] + r[1] + r[2] - 180;
    while (diff !== 0) {
      k = 0; d.forEach(function (x, j) { if ((diff > 0 ? r[j] - x : x - r[j]) > (diff > 0 ? r[k] - d[k] : d[k] - r[k])) k = j; });
      r[k] -= diff > 0 ? 1 : -1; diff += diff > 0 ? -1 : 1;
    }
    return r;
  }
  var triLimit = function (s, key, p) {
    var t = triangleOf({ A: key === 'A' ? p : s.A, B: key === 'B' ? p : s.B, C: key === 'C' ? p : s.C });
    return t.least >= 190 && Math.min.apply(null, t.angles) >= 0.56 && t.r >= 52;
  };
  var triStart = { A: [340, 100], B: [116, 380], C: [560, 380] };

  // Grade 8, lesson 13, Exercise 6.a: construct parallelogram ABCD
  // given AB = 6 cm, AD = 4 cm and angle A = 60°
  CX['g8-l13-parallelogram'] = {
    steps: 7,
    start: { ang: 60, ab: 6, ad: 4 },
    place: function (s, key, p) {
      if (key === 'D') {
        var A = [140, 360];
        var v = sub(p, A);
        var a = Math.atan2(-v[1], v[0]) * 180 / Math.PI;
        s.ang = Math.round(Math.max(35, Math.min(85, a)));
        return p;
      }
      return p;
    },
    limit: function (s, key, p) { return true; },
    figure: function (s) {
      var A = [140, 360], ab = s.ab || 6, ad = s.ad || 4, ang = s.ang || 60;
      var B = add(A, [ab * CM, 0]);
      var d = prDir(RIGHT, ang);
      var nr = [d[1], -d[0]];
      var D = add(A, mul(d, ad * CM));
      var C = add(D, [ab * CM, 0]);
      var Ex = add(A, mul(d, (ad + 1.2) * CM));
      var M = markAt(A, RIGHT, ang);
      var rAB = ab * CM, rAD = ad * CM;
      var tBC = -ang * Math.PI / 180;
      return {
        meet: true, A: A, B: B, C: C, D: D,
        ab: ab, ad: ad, ang: ang, d: d, nr: nr, Ex: Ex, M: M,
        arcD: { c: D, r: rAB, t1: 0.28, t2: -0.28 },
        arcB: { c: B, r: rAD, t1: tBC + 0.28, t2: tBC - 0.28 },
        rAB: rAB, rAD: rAD
      };
    },
    draw: function (f, i, g, layer) {
      var ink = layer.ink, marks = layer.marks, tools = layer.tools;
      var poly = function (g2, pts, attrs) {
        var pStr = pts.map(function (x) { return x[0].toFixed(1) + ',' + x[1].toFixed(1); }).join(' ');
        return el('polygon', Object.assign({ points: pStr }, attrs), g2);
      };

      given(ink, 'AB = ' + cmText(f.ab) + '    AD = ' + cmText(f.ad) + '    ∠A = ' + f.ang + '°');

      if (i === 0) {
        says(marks, 0, 'លំហាត់ ៦.ក ៖ សង់ប្រលេឡូក្រាម ABCD');
        says(marks, 1, '• ជ្រុងបាត AB = ' + f.ab + ' cm');
        says(marks, 2, '• ជ្រុងជាប់ AD = ' + f.ad + ' cm');
        says(marks, 3, '• មុំរួម ∠A = ' + f.ang + '°');
        says(marks, 5, 'ឧបករណ៍ ៖ បន្ទាត់ក្រិត · រ៉ាប់ទ័រ · ដែកឈាន · ខ្មៅដៃ');
        return;
      }

      // Step 1: Draw base AB
      if (i >= 1) {
        segLine(ink, f.A, f.B, 'cx-seg');
        point(ink, f.A, 'A', [-0.8, 0.8], null, null, 22);
        point(ink, f.B, 'B', [0.8, 0.8], null, null, 22);
        label(marks, [(f.A[0] + f.B[0]) / 2, f.A[1] + 22], cmText(f.ab), 'cx-note');
      }
      if (i === 1) {
        drawCmRuler(tools, f.A, RIGHT, 7, DOWN);
      }

      // Step 2: Protractor at A, mark angle, draw ray Ax
      if (i >= 2) {
        dot(ink, f.M);
        segLine(ink, f.A, f.Ex, 'cx-line cx-line-2');
        label(ink, add(add(f.Ex, mul(f.d, -6)), mul(f.nr, 20)), 'x', 'cx-label');
        wedge(marks, f.A, 0, -f.ang * Math.PI / 180, 36, 'a');
        label(marks, add(f.A, mul(prDir(RIGHT, f.ang / 2), 58)), f.ang + '°', 'cx-note cx-r');
      }
      if (i === 2) {
        drawProtractor(tools, f.A, RIGHT, f.ang);
      }

      // Step 3: Measure AD = 4 cm on ray Ax, mark point D
      if (i >= 3) {
        point(ink, f.D, 'D', [-0.9, -0.6], 'cx-pt-m', null, 24);
        sideNote(marks, f.A, f.D, f.B, cmText(f.ad));
      }
      if (i === 3) {
        drawCmRuler(tools, f.A, f.d, 5, f.nr);
      }

      // Step 4: Arc of radius 6 cm from D
      if (i >= 4) {
        arcDraw(ink, f.arcD);
        if (i === 4) {
          label(marks, [f.D[0] + 110, f.D[1] - 22], 'កាំ 6 cm (ស្មើ AB)', 'cx-note');
        }
      }

      // Step 5: Arc of radius 4 cm from B intersecting at C
      if (i >= 5) {
        arcDraw(ink, f.arcB);
        point(ink, f.C, 'C', [0.8, -0.8], 'cx-pt-m', null, 24);
        if (i === 5) {
          label(marks, [f.B[0] + 55, f.B[1] - 65], 'កាំ 4 cm (ស្មើ AD)', 'cx-note');
        }
      }

      // Step 6: Connect DC and BC -> Complete Parallelogram ABCD!
      if (i >= 6) {
        segLine(ink, f.D, f.C, 'cx-line');
        segLine(ink, f.B, f.C, 'cx-line');
        poly(marks, [f.A, f.B, f.C, f.D], { fill: 'rgba(46, 122, 112, 0.14)', stroke: 'none' });

        // Ticks on opposite sides
        tick(marks, f.A, f.B); tick(marks, f.D, f.C);
        tick2(marks, f.A, f.D); tick2(marks, f.B, f.C);

        // Opposite angle marks
        wedge(marks, f.C, Math.PI, -f.ang * Math.PI / 180, 36, 'a');
        label(marks, add(f.C, mul(prDir(LEFT, -f.ang / 2), 58)), f.ang + '°', 'cx-note cx-r');

        // Draggable handle at D
        el('circle', { cx: f.D[0], cy: f.D[1], r: 7, class: 'cx-handle' }, ink);
        el('circle', { cx: f.D[0], cy: f.D[1], r: 24, class: 'cx-grab', 'data-drag': 'D' }, ink);

        says(marks, 0, 'ប្រលេឡូក្រាម ABCD ពេញលេញ ៖');
        says(marks, 1, '• ជ្រុងឈមប៉ុនគ្នា ៖ AB = CD = ' + f.ab + ' cm  ,  AD = BC = ' + f.ad + ' cm');
        says(marks, 2, '• ជ្រុងឈមស្របគ្នា ៖ AB ∥ CD  ,  AD ∥ BC');
        says(marks, 3, '• មុំឈមប៉ុនគ្នា ៖ ∠A = ∠C = ' + f.ang + '°  ,  ∠B = ∠D = ' + (180 - f.ang) + '°');
      }
    },
    anim: function (f, i) {
      if (i === 1) return { phases: cmSegmentPhases(f.A, RIGHT, f.ab, 7, DOWN, 'cx-seg') };
      if (i === 2) return { phases: protractorPhases(f.A, RIGHT, f.ang) };
      if (i === 3) return { phases: [
        { dur: 800, draw: function (t, drawn, tools) {
          drawCmRuler(tools, add(f.A, mul(f.nr, 30 * (1 - t))), f.d, 5, f.nr, 0.25 + 0.75 * t);
        } },
        { dur: 900, draw: function (t, drawn, tools) {
          drawCmRuler(tools, f.A, f.d, 5, f.nr);
          el('circle', { cx: f.D[0], cy: f.D[1], r: 5 * Math.min(1, t * 2), class: 'cx-pt cx-pt-m' }, drawn);
          el('circle', { cx: f.D[0], cy: f.D[1], r: 4.2, class: 'cx-c-pencil', opacity: t < 0.85 ? 1 : 0 }, tools);
        } },
      ] };
      if (i === 4) return { phases: [{ dur: 1000, draw: function (t, drawn, tools) {
        var q = f.arcD, th = q.t1 + (q.t2 - q.t1) * t;
        el('path', { d: arcPath(q.c, q.r, q.t1, th), class: 'cx-arc' }, drawn);
        drawCompass(tools, q.c, onCircle(q.c, q.r, th));
      } }] };
      if (i === 5) return { phases: [{ dur: 1000, draw: function (t, drawn, tools) {
        arcDraw(drawn, f.arcD);
        var q = f.arcB, th = q.t1 + (q.t2 - q.t1) * t;
        el('path', { d: arcPath(q.c, q.r, q.t1, th), class: 'cx-arc' }, drawn);
        drawCompass(tools, q.c, onCircle(q.c, q.r, th));
      } }] };
      if (i === 6) return { phases: [
        { dur: 900, draw: function (t, drawn, tools) {
          drawRuler(tools, f.D, f.C);
          segLine(drawn, f.D, add(f.D, mul(sub(f.C, f.D), t)), 'cx-line');
        } },
        { dur: 900, draw: function (t, drawn, tools) {
          segLine(drawn, f.D, f.C, 'cx-line');
          drawRuler(tools, f.B, f.C);
          segLine(drawn, f.B, add(f.B, mul(sub(f.C, f.B), t)), 'cx-line');
        } }
      ] };
      return null;
    }
  };

  // Grade 8, lesson 13, Mid-segment theorem of a triangle (Diagram 605):
  // DE joins the midpoints D of AB and E of AC; then DE || BC and DE = 1/2 BC.
  CX['g8-l13-midsegment'] = {
    steps: 7,
    start: { A: [280, 100], B: [120, 370], C: [480, 370] },
    place: function (s, key, p) {
      if (key === 'A') {
        s.A = [Math.max(160, Math.min(440, p[0])), Math.max(60, Math.min(190, p[1]))];
      } else if (key === 'B') {
        s.B = [Math.max(50, Math.min(s.C[0] - 160, p[0])), Math.max(280, Math.min(420, p[1]))];
      } else if (key === 'C') {
        s.C = [Math.max(s.B[0] + 160, Math.min(590, p[0])), Math.max(280, Math.min(420, p[1]))];
      }
      return p;
    },
    limit: function (s, key, p) { return true; },
    figure: function (s) {
      var A = s.A, B = s.B, C = s.C;
      var D = mul(add(A, B), 0.5);
      var E = mul(add(A, C), 0.5);
      var vDE = sub(E, D);
      var F = add(E, vDE);
      var dBC = len(sub(C, B)), dDE = len(vDE);
      var cmBC = (Math.round(dBC / CM * 10) / 10).toFixed(1);
      var cmDE = (Math.round(dDE / CM * 10) / 10).toFixed(1);
      return {
        meet: true, A: A, B: B, C: C, D: D, E: E, F: F,
        vDE: vDE, cmBC: cmBC, cmDE: cmDE
      };
    },
    draw: function (f, i, g, layer) {
      var ink = layer.ink, marks = layer.marks, tools = layer.tools;
      var poly = function (g2, pts, attrs) {
        var pStr = pts.map(function (x) { return x[0].toFixed(1) + ',' + x[1].toFixed(1); }).join(' ');
        return el('polygon', Object.assign({ points: pStr }, attrs), g2);
      };

      // Shaded triangle ABC
      poly(ink, [f.A, f.B, f.C], { fill: 'rgba(45, 106, 168, 0.06)', stroke: '#2e7a70', 'stroke-width': '2.5' });

      // Midpoint tick marks on AB and AC
      tick(marks, f.A, f.D); tick(marks, f.D, f.B);
      tick2(marks, f.A, f.E); tick2(marks, f.E, f.C);

      if (i === 0) {
        says(marks, 0, 'ទ្រឹស្ដីបទអង្កត់មធ្យមនៃត្រីកោណ ៖');
        says(marks, 1, '• ត្រីកោណ ABC មាន D ជាចំណុចកណ្ដាលនៃ AB (AD = DB)');
        says(marks, 2, '• E ជាចំណុចកណ្ដាលនៃ AC (AE = EC)');
        says(marks, 4, 'គោលដៅ ៖ ស្រាយបញ្ជាក់ថា DE ∥ BC  និង  DE = ½ BC');
      }

      // Step 1: Draw DE
      if (i >= 1) {
        segLine(ink, f.D, f.E, 'cx-seg');
      }
      if (i === 1) {
        says(marks, 0, 'អង្កត់ DE ភ្ជាប់ចំណុចកណ្ដាលនៃជ្រុងទាំងពីរ');
        says(marks, 1, 'ហៅថា «អង្កត់មធ្យម» (ឬបាតមធ្យម) នៃត្រីកោណ ABC');
      }

      // Step 2: Extend DE to F such that EF = DE
      if (i >= 2) {
        segLine(ink, f.E, f.F, 'cx-line cx-line-2');
        tick(marks, f.D, f.E); tick(marks, f.E, f.F);
        point(ink, f.F, 'F', [1, -0.6], 'cx-pt-m', null, 22);
      }
      if (i === 2) {
        says(marks, 0, 'បន្លាយអង្កត់ DE ឱ្យបានអង្កត់ EF = DE');
        says(marks, 1, 'ដៅចំណុច F ⟹ E ជាចំណុចកណ្ដាលនៃ DF');
      }

      // Step 3: Draw AF, FC, DC
      if (i >= 3) {
        el('line', { x1: f.A[0], y1: f.A[1], x2: f.F[0], y2: f.F[1], class: 'cx-equal' }, ink);
        segLine(ink, f.F, f.C, 'cx-line');
        el('line', { x1: f.D[0], y1: f.D[1], x2: f.C[0], y2: f.C[1], class: 'cx-equal' }, ink);
      }
      if (i === 3) {
        says(marks, 0, 'ភ្ជាប់អង្កត់ AF, FC និង DC');
        says(marks, 1, 'បង្កើតបានចតុកោណ ADCF ដែលមានអង្កត់ទ្រូង AC និង DF');
      }

      // Step 4: Parallelogram ADCF
      if (i === 4) {
        poly(marks, [f.A, f.D, f.C, f.F], { fill: 'rgba(232, 114, 92, 0.16)', stroke: 'none' });
        arrowHead(marks, mul(add(f.A, f.D), 0.5), unit(sub(f.A, f.D)));
        arrowHead(marks, mul(add(f.F, f.C), 0.5), unit(sub(f.F, f.C)));
        says(marks, 0, 'ចតុកោណ ADCF មានអង្កត់ទ្រូង AC និង DF កាត់គ្នាត្រង់ចំណុចកណ្ដាល E ៖');
        says(marks, 1, '⟹ ADCF ជាប្រលេឡូក្រាម');
        says(marks, 2, '⟹ CF ∥ AD  និង  CF = AD');
      }

      // Step 5: Parallelogram BDFC
      if (i === 5) {
        poly(marks, [f.B, f.D, f.F, f.C], { fill: 'rgba(46, 122, 112, 0.18)', stroke: 'none' });
        arrowHead(marks, mul(add(f.D, f.B), 0.5), unit(sub(f.D, f.B)));
        arrowHead(marks, mul(add(f.F, f.C), 0.5), unit(sub(f.F, f.C)));
        says(marks, 0, 'ដោយ AD = DB នាំឱ្យ CF = DB និង CF ∥ DB ៖');
        says(marks, 1, '⟹ ចតុកោណ BDFC មានជ្រុងឈមមួយគូស្របគ្នាផងនិងស្មើគ្នាផង');
        says(marks, 2, '⟹ BDFC ជាប្រលេឡូក្រាម  ⟹  DF ∥ BC  និង  DF = BC');
      }

      // Step 6: Conclusion
      if (i >= 6) {
        poly(marks, [f.B, f.D, f.F, f.C], { fill: 'rgba(46, 122, 112, 0.12)', stroke: 'none' });
        arrowHead(marks, mul(add(f.D, f.E), 0.5), unit(sub(f.E, f.D)));
        arrowHead(marks, mul(add(f.B, f.C), 0.5), unit(sub(f.C, f.B)));
        says(marks, 0, 'សន្និដ្ឋាននៃទ្រឹស្ដីបទ ៖');
        says(marks, 1, '• ដោយ DF ∥ BC  នាំឱ្យ  DE ∥ BC');
        says(marks, 2, '• ដោយ DE = ½ DF  នាំឱ្យ  DE = ½ BC  (ពិត)');
        says(marks, 4, 'ប្រវែងជាក់ស្ដែង ៖  BC = ' + f.cmBC + ' cm  ⟹  DE = ' + f.cmDE + ' cm  (= ½ BC)');
      }

      // Vertices with draggable grab handles
      point(ink, f.A, 'A', [0, -1], null, 'A', 22);
      point(ink, f.B, 'B', [-1, 0.8], null, 'B', 22);
      point(ink, f.C, 'C', [1, 0.8], null, 'C', 22);
      point(ink, f.D, 'D', [-1, 0], 'cx-pt-m', null, 22);
      point(ink, f.E, 'E', [0.8, -0.6], 'cx-pt-m', null, 22);
    },
    anim: function (f, i) {
      if (i === 1) return { ruler: [f.D, f.E], cls: 'cx-seg' };
      if (i === 2) return { ruler: [f.E, f.F], cls: 'cx-line cx-line-2' };
      if (i === 3) return { rulers: [[f.A, f.F], [f.F, f.C], [f.D, f.C]] };
      return null;
    }
  };

  // Grade 8, lesson 13, Flowchart of Quadrilaterals (Diagram 64):
  // Interactive morphing & hierarchy from General Quadrilateral to Square.
  CX['g8-l13-quad-family'] = {
    steps: 7,
    start: {
      step0: { A: [350, 150], B: [530, 130], C: [510, 350], D: [340, 320] },
      step1: { A: [380, 150], B: [500, 150], C: [550, 350], D: [330, 350] },
      step3: { A: [370, 150], B: [530, 150], C: [480, 340], D: [320, 340] },
      step4: { A: [340, 160], B: [520, 160], C: [520, 330], D: [340, 330] },
      step5: { A: [430, 130], B: [535, 240], C: [430, 350], D: [325, 240] },
      step6: { A: [355, 160], B: [505, 160], C: [505, 310], D: [355, 310] }
    },
    limit: function (s, key, p) { return true; },
    figure: function (s) {
      return { meet: true, s: s };
    },
    draw: function (f, i, g, layer) {
      var ink = layer.ink, marks = layer.marks, tools = layer.tools;
      var poly = function (g2, pts, attrs) {
        var pStr = pts.map(function (x) { return x[0].toFixed(1) + ',' + x[1].toFixed(1); }).join(' ');
        return el('polygon', Object.assign({ points: pStr }, attrs), g2);
      };

      if (i === 0) {
        // Step 0: General Quadrilateral
        var A = f.s.step0.A, B = f.s.step0.B, C = f.s.step0.C, D = f.s.step0.D;
        poly(ink, [A, B, C, D], { fill: 'rgba(45, 106, 168, 0.08)', stroke: '#2e7a70', 'stroke-width': '2.5' });
        point(ink, A, 'A', [-0.8, -0.8], null, null, 20);
        point(ink, B, 'B', [0.8, -0.8], null, null, 20);
        point(ink, C, 'C', [0.8, 0.8], null, null, 20);
        point(ink, D, 'D', [-0.8, 0.8], null, null, 20);

        says(marks, 0, '១. ចតុកោណទូទៅ (Quadrilateral) ៖');
        says(marks, 1, '• ជាពហុកោណដែលមាន ៤ ជ្រុង និង ៤ មុំ');
        says(marks, 2, '• ផលបូកមុំក្នុងទាំងបួន ៖ ∠A + ∠B + ∠C + ∠D = 360°');
        says(marks, 4, 'ការវិវត្តបន្ត ៖');
        says(marks, 5, '• បន្ថែមជ្រុងឈម ១ គូស្របគ្នា ⟹ ចតុកោណព្នាយ');
        says(marks, 6, '• បន្ថែមជ្រុងឈម ២ គូស្របគ្នា ⟹ ប្រលេឡូក្រាម');
      } else if (i === 1) {
        // Step 1: Trapezoid
        var A1 = f.s.step1.A, B1 = f.s.step1.B, C1 = f.s.step1.C, D1 = f.s.step1.D;
        poly(ink, [A1, B1, C1, D1], { fill: 'rgba(46, 122, 112, 0.12)', stroke: '#2e7a70', 'stroke-width': '2.5' });
        point(ink, A1, 'A', [-0.8, -0.8], null, null, 20);
        point(ink, B1, 'B', [0.8, -0.8], null, null, 20);
        point(ink, C1, 'C', [0.8, 0.8], null, null, 20);
        point(ink, D1, 'D', [-0.8, 0.8], null, null, 20);

        // Parallel arrows on AB and DC
        arrowHead(marks, mul(add(A1, B1), 0.5), unit(sub(B1, A1)));
        arrowHead(marks, mul(add(D1, C1), 0.5), unit(sub(C1, D1)));

        label(marks, [(A1[0] + B1[0]) / 2, A1[1] - 18], 'បាតតូច b', 'cx-note');
        label(marks, [(D1[0] + C1[0]) / 2, D1[1] + 20], 'បាតធំ B', 'cx-note');

        says(marks, 0, '២. ចតុកោណព្នាយ (Trapezoid) ៖');
        says(marks, 1, '• មានជ្រុងឈមមួយគូស្របគ្នា ៖ AB ∥ CD');
        says(marks, 2, '• AB ជាបាតតូច និង CD ជាបាតធំ');
        says(marks, 3, '• មុំជាប់បាតបន្ថែមគ្នា ៖ ∠A + ∠D = 180°, ∠B + ∠C = 180°');
        says(marks, 5, 'ផ្ទៃក្រឡា ៖  S = ½ (B + b) × h');
      } else if (i === 2) {
        // Step 2: Special Trapezoids (Isosceles & Right)
        // Draw Isosceles Trapezoid
        var tA = [330, 110], tB = [430, 110], tC = [460, 220], tD = [300, 220];
        poly(ink, [tA, tB, tC, tD], { fill: 'rgba(46, 122, 112, 0.12)', stroke: '#2e7a70', 'stroke-width': '2.2' });
        tick(marks, tA, tD); tick(marks, tB, tC);
        label(marks, [380, 238], 'ចតុកោណព្នាយសមបាត', 'cx-label');

        // Draw Right Trapezoid
        var rA = [330, 270], rB = [440, 270], rC = [480, 380], rD = [330, 380];
        poly(ink, [rA, rB, rC, rD], { fill: 'rgba(232, 114, 92, 0.12)', stroke: '#e8725c', 'stroke-width': '2.2' });
        rightMark(marks, rD, [0, -1], [1, 0]);
        rightMark(marks, rA, [1, 0], [0, 1]);
        label(marks, [405, 398], 'ចតុកោណព្នាយកែង', 'cx-label');

        says(marks, 0, '៣. ចតុកោណព្នាយពិសេស ៖');
        says(marks, 1, 'ក. ចតុកោណព្នាយសមបាត ៖');
        says(marks, 2, '• ជ្រុងទ្រេតប៉ុនគ្នា ៖ AD = BC');
        says(marks, 3, '• មុំបាតប៉ុនគ្នា ៖ ∠D = ∠C , ∠A = ∠B');
        says(marks, 4, '• អង្កត់ទ្រូងប៉ុនគ្នា ៖ AC = BD');
        says(marks, 6, 'ខ. ចតុកោណព្នាយកែង ៖');
        says(marks, 7, '• មានជ្រុងទ្រេតមួយកែងនឹងបាតទាំងពីរ');
        says(marks, 8, '• មានមុំកែងពីរជាប់គ្នា (90°)');
      } else if (i === 3) {
        // Step 3: Parallelogram
        var Ap = f.s.step3.A, Bp = f.s.step3.B, Cp = f.s.step3.C, Dp = f.s.step3.D;
        poly(ink, [Ap, Bp, Cp, Dp], { fill: 'rgba(46, 122, 112, 0.14)', stroke: '#2e7a70', 'stroke-width': '2.5' });
        point(ink, Ap, 'A', [-0.8, -0.8], null, null, 20);
        point(ink, Bp, 'B', [0.8, -0.8], null, null, 20);
        point(ink, Cp, 'C', [0.8, 0.8], null, null, 20);
        point(ink, Dp, 'D', [-0.8, 0.8], null, null, 20);

        arrowHead(marks, mul(add(Ap, Bp), 0.5), unit(sub(Bp, Ap)));
        arrowHead(marks, mul(add(Dp, Cp), 0.5), unit(sub(Cp, Dp)));
        arrowHead(marks, mul(add(Ap, Dp), 0.5), unit(sub(Dp, Ap)));
        arrowHead(marks, mul(add(Bp, Cp), 0.5), unit(sub(Cp, Bp)));

        tick(marks, Ap, Bp); tick(marks, Dp, Cp);
        tick2(marks, Ap, Dp); tick2(marks, Bp, Cp);

        says(marks, 0, '៤. ប្រលេឡូក្រាម (Parallelogram) ៖');
        says(marks, 1, '• ជ្រុងឈមស្របគ្នា ២ គូ ៖ AB ∥ CD  និង  AD ∥ BC');
        says(marks, 2, '• ជ្រុងឈមប៉ុនគ្នា ៖ AB = CD  និង  AD = BC');
        says(marks, 3, '• មុំឈមប៉ុនគ្នា ៖ ∠A = ∠C  និង  ∠B = ∠D');
        says(marks, 4, '• អង្កត់ទ្រូងកាត់គ្នាត្រង់ចំណុចកណ្ដាល');
        says(marks, 6, 'ផ្ទៃក្រឡា ៖  S = b × h');
      } else if (i === 4) {
        // Step 4: Rectangle
        var Ar = f.s.step4.A, Br = f.s.step4.B, Cr = f.s.step4.C, Dr = f.s.step4.D;
        poly(ink, [Ar, Br, Cr, Dr], { fill: 'rgba(45, 106, 168, 0.12)', stroke: '#2d6aa8', 'stroke-width': '2.5' });
        point(ink, Ar, 'A', [-0.8, -0.8], null, null, 20);
        point(ink, Br, 'B', [0.8, -0.8], null, null, 20);
        point(ink, Cr, 'C', [0.8, 0.8], null, null, 20);
        point(ink, Dr, 'D', [-0.8, 0.8], null, null, 20);

        rightMark(marks, Ar, [1, 0], [0, 1]);
        rightMark(marks, Br, [0, 1], [-1, 0]);
        rightMark(marks, Cr, [-1, 0], [0, -1]);
        rightMark(marks, Dr, [0, -1], [1, 0]);

        // Diagonals drawn dashed
        el('line', { x1: Ar[0], y1: Ar[1], x2: Cr[0], y2: Cr[1], class: 'cx-equal' }, marks);
        el('line', { x1: Br[0], y1: Br[1], x2: Dr[0], y2: Dr[1], class: 'cx-equal' }, marks);

        says(marks, 0, '៥. ចតុកោណកែង (Rectangle) ៖');
        says(marks, 1, '• ជាប្រលេឡូក្រាមដែលមានមុំកែងមួយ');
        says(marks, 2, '• មុំទាំង ៤ ជាមុំកែង ៖ ∠A = ∠B = ∠C = ∠D = 90°');
        says(marks, 3, '• អង្កត់ទ្រូងទាំងពីរប៉ុនគ្នា ៖ AC = BD');
        says(marks, 5, 'ផ្ទៃក្រឡា ៖  S = a × b  (បណ្ដោយ × ទទឹង)');
      } else if (i === 5) {
        // Step 5: Rhombus
        var As = f.s.step5.A, Bs = f.s.step5.B, Cs = f.s.step5.C, Ds = f.s.step5.D;
        poly(ink, [As, Bs, Cs, Ds], { fill: 'rgba(232, 114, 92, 0.12)', stroke: '#e8725c', 'stroke-width': '2.5' });
        point(ink, As, 'A', [0, -1], null, null, 20);
        point(ink, Bs, 'B', [1, 0], null, null, 20);
        point(ink, Cs, 'C', [0, 1], null, null, 20);
        point(ink, Ds, 'D', [-1, 0], null, null, 20);

        tick(marks, As, Bs); tick(marks, Bs, Cs);
        tick(marks, Cs, Ds); tick(marks, Ds, As);

        // Perpendicular diagonals
        segLine(marks, As, Cs, 'cx-equal');
        segLine(marks, Bs, Ds, 'cx-equal');
        var O = [(As[0] + Cs[0]) / 2, (Bs[1] + Ds[1]) / 2];
        rightMark(marks, O, [0, -1], [1, 0]);

        says(marks, 0, '៦. ចតុកោណស្មើ (Rhombus) ៖');
        says(marks, 1, '• ជាប្រលេឡូក្រាមដែលមានជ្រុងទាំង ៤ ស្មើគ្នា');
        says(marks, 2, '• ជ្រុងទាំង ៤ ប៉ុនគ្នា ៖ AB = BC = CD = DA');
        says(marks, 3, '• អង្កត់ទ្រូងទាំងពីរកែងគ្នា ៖ AC ⊥ BD');
        says(marks, 4, '• អង្កត់ទ្រូងជាកន្លះបន្ទាត់ពុះមុំ');
        says(marks, 6, 'ផ្ទៃក្រឡា ៖  S = ½ × d₁ × d₂');
      } else if (i === 6) {
        // Step 6: Square
        var Aq = f.s.step6.A, Bq = f.s.step6.B, Cq = f.s.step6.C, Dq = f.s.step6.D;
        poly(ink, [Aq, Bq, Cq, Dq], { fill: 'rgba(46, 122, 112, 0.18)', stroke: '#2e7a70', 'stroke-width': '2.6' });
        point(ink, Aq, 'A', [-0.8, -0.8], null, null, 20);
        point(ink, Bq, 'B', [0.8, -0.8], null, null, 20);
        point(ink, Cq, 'C', [0.8, 0.8], null, null, 20);
        point(ink, Dq, 'D', [-0.8, 0.8], null, null, 20);

        // All 4 right marks
        rightMark(marks, Aq, [1, 0], [0, 1]);
        rightMark(marks, Bq, [0, 1], [-1, 0]);
        rightMark(marks, Cq, [-1, 0], [0, -1]);
        rightMark(marks, Dq, [0, -1], [1, 0]);

        // All 4 sides equal
        tick(marks, Aq, Bq); tick(marks, Bq, Cq);
        tick(marks, Cq, Dq); tick(marks, Dq, Aq);

        // Diagonals equal AND perpendicular
        segLine(marks, Aq, Cq, 'cx-equal');
        segLine(marks, Bq, Dq, 'cx-equal');
        var Oq = [(Aq[0] + Cq[0]) / 2, (Aq[1] + Cq[1]) / 2];
        rightMark(marks, Oq, [1, 1], [-1, 1]);

        says(marks, 0, '៧. ការេ (Square) — កំពូលគ្រួសារចតុកោណ ៖');
        says(marks, 1, '• ជាចតុកោណកែងផង និងជាចតុកោណស្មើផង');
        says(marks, 2, '• ជ្រុងទាំង ៤ ប៉ុនគ្នា ៖ AB = BC = CD = DA');
        says(marks, 3, '• មុំទាំង ៤ សុទ្ធតែកែង ៖ 90°');
        says(marks, 4, '• អង្កត់ទ្រូងប៉ុនគ្នាផង និងកែងគ្នាផង (AC = BD, AC ⊥ BD)');
        says(marks, 6, 'ផ្ទៃក្រឡា ៖  S = a²');
      }
    },
    anim: function (f, i) {
      return null;
    }
  };

  // Grade 8, lesson 14, visual proof of the Pythagorean theorem:
  // Four copies of a right-angled triangle with legs a, b and hypotenuse c
  // fit inside a large square of side (a+b), enclosing an inner tilted square IJKL of side c.
  CX['g8-l14-pythagoras'] = {
    steps: 6,
    start: { t: 0.36 },
    place: function (s, key, p) {
      if (key === 'I') {
        var x0 = 380, S = 210;
        var clampedX = Math.max(x0 + 35, Math.min(x0 + S - 35, p[0]));
        var frac = (x0 + S - clampedX) / S;
        s.t = Math.max(0.18, Math.min(0.65, frac));
        return [x0 + S * (1 - s.t), 325];
      }
      return p;
    },
    limit: function (s, key, p) { return true; },
    figure: function (s) {
      var x0 = 380, y0 = 115, S = 210;
      var t = s.t || 0.36;
      var a = t * S, b = (1 - t) * S;
      var c = Math.hypot(a, b);
      var BL = [x0, y0 + S], BR = [x0 + S, y0 + S], TR = [x0 + S, y0], TL = [x0, y0];
      var I = [x0 + b, y0 + S];
      var J = [x0 + S, y0 + S - b];
      var K = [x0 + a, y0];
      var L = [x0, y0 + b];
      return { x0: x0, y0: y0, S: S, a: a, b: b, c: c, t: t,
        BL: BL, BR: BR, TR: TR, TL: TL,
        I: I, J: J, K: K, L: L };
    },
    draw: function (f, i, svg, layer) {
      var ink = layer.ink, marks = layer.marks;
      var poly = function (g, pts, attrs) {
        var pStr = pts.map(function (x) { return x[0].toFixed(1) + ',' + x[1].toFixed(1); }).join(' ');
        var a = Object.assign({ points: pStr }, attrs);
        return el('polygon', a, g);
      };

      if (i === 0) {
        // Step 0: Single right triangle with legs a, b, hypotenuse c on the right side
        var O = [395, 305], P = [395 + f.b, 305], Q = [395 + f.b, 305 - f.a];
        poly(ink, [O, P, Q], { fill: 'rgba(46, 122, 112, 0.22)', stroke: '#2e7a70', 'stroke-width': '2.5' });
        rightMark(marks, P, [-1, 0], [0, -1]);
        label(marks, [(O[0] + P[0]) / 2, O[1] + 24], 'b', 'cx-label');
        label(marks, [P[0] + 18, (P[1] + Q[1]) / 2], 'a', 'cx-label');
        label(marks, [(O[0] + Q[0]) / 2 - 14, (O[1] + Q[1]) / 2 - 12], 'c', 'cx-label');

        says(marks, 0, 'ត្រីកោណកែងមួយមាន ៖');
        says(marks, 1, '• ជ្រុងមុំកែងពីរមានរង្វាស់ a និង b');
        says(marks, 2, '• អ៊ីប៉ូតេនុសមានរង្វាស់ c');
        says(marks, 4, 'គោលដៅ ៖ ស្រាយបញ្ជាក់ថា c² = a² + b²');
        return;
      }

      // Step 1+: Outer square (a+b) x (a+b)
      poly(ink, [f.TL, f.TR, f.BR, f.BL], { fill: 'rgba(45, 106, 168, 0.05)', stroke: '#2e7a70', 'stroke-width': '2.5' });

      says(marks, 0, 'ការេធំមួយមានរង្វាស់ជ្រុង (a + b)');
      says(marks, 1, 'ផ្ទៃការេធំ = (a + b)²');
      says(marks, 2, '             = a² + b² + 2ab');

      if (i >= 2) {
        // Step 2+: Mark points I, J, K, L and segment labels a, b
        point(marks, f.I, 'I', [0, 1], 'cx-pt-m', 'I', 18);
        point(marks, f.J, 'J', [1, 0], 'cx-pt-m', null, 18);
        point(marks, f.K, 'K', [0, -1], 'cx-pt-m', null, 18);
        point(marks, f.L, 'L', [-1, 0], 'cx-pt-m', null, 18);

        label(marks, [(f.BL[0] + f.I[0]) / 2, f.BL[1] + 16], 'b', 'cx-note cx-r');
        label(marks, [(f.I[0] + f.BR[0]) / 2, f.BR[1] + 16], 'a', 'cx-note cx-r');

        label(marks, [f.BR[0] + 16, (f.BR[1] + f.J[1]) / 2], 'b', 'cx-note cx-r');
        label(marks, [f.TR[0] + 16, (f.J[1] + f.TR[1]) / 2], 'a', 'cx-note cx-r');

        label(marks, [(f.TR[0] + f.K[0]) / 2, f.TR[1] - 14], 'b', 'cx-note cx-r');
        label(marks, [(f.K[0] + f.TL[0]) / 2, f.TL[1] - 14], 'a', 'cx-note cx-r');

        label(marks, [f.TL[0] - 16, (f.TL[1] + f.L[1]) / 2], 'b', 'cx-note cx-r');
        label(marks, [f.BL[0] - 16, (f.L[1] + f.BL[1]) / 2], 'a', 'cx-note cx-r');
      }

      if (i >= 3) {
        // Step 3+: Draw the 4 right triangles in the corners
        var triAttr = { fill: 'rgba(46, 122, 112, 0.25)', stroke: '#2e7a70', 'stroke-width': '2' };
        poly(ink, [f.I, f.BR, f.J], triAttr);
        poly(ink, [f.J, f.TR, f.K], triAttr);
        poly(ink, [f.K, f.TL, f.L], triAttr);
        poly(ink, [f.L, f.BL, f.I], triAttr);

        rightMark(marks, f.BR, [-1, 0], [0, -1]);
        rightMark(marks, f.TR, [0, 1], [-1, 0]);
        rightMark(marks, f.TL, [1, 0], [0, 1]);
        rightMark(marks, f.BL, [0, -1], [1, 0]);

        says(marks, 4, 'ត្រីកោណកែង ៤ ប៉ុនគ្នានៅតាមជ្រុង ៖');
        says(marks, 5, 'ផ្ទៃត្រីកោណទាំង ៤ = 4 × (½ab) = 2ab');
      }

      if (i >= 4) {
        // Step 4+: Inner square IJKL
        poly(ink, [f.I, f.J, f.K, f.L], { fill: 'rgba(201, 134, 43, 0.32)', stroke: '#c9862b', 'stroke-width': '2.5' });

        label(marks, [(f.I[0] + f.J[0]) / 2 - 10, (f.I[1] + f.J[1]) / 2 - 10], 'c', 'cx-label');
        label(marks, [(f.J[0] + f.K[0]) / 2 - 10, (f.J[1] + f.K[1]) / 2 + 10], 'c', 'cx-label');
        label(marks, [(f.K[0] + f.L[0]) / 2 + 10, (f.K[1] + f.L[1]) / 2 + 10], 'c', 'cx-label');
        label(marks, [(f.L[0] + f.I[0]) / 2 + 10, (f.L[1] + f.I[1]) / 2 - 10], 'c', 'cx-label');

        label(marks, [(f.x0 + f.S / 2), (f.y0 + f.S / 2)], 'IJKL (c²)', 'cx-label');
        says(marks, 7, 'ចតុកោណ IJKL ជាការេជ្រុង c ៖');
        says(marks, 8, 'ផ្ទៃការេ IJKL = c²');
      }

      if (i >= 5) {
        // Step 5: Full algebraic proof and dynamic live values
        says(marks, 10, 'ផ្ទៃការេ IJKL = ផ្ទៃការេធំ − ផ្ទៃត្រីកោណទាំង ៤');
        says(marks, 11, 'c² = (a² + b² + 2ab) − 2ab');
        says(marks, 12, '⟹  c² = a² + b²  (ទ្រឹស្តីបទពីតាក័រ)');

        var aN = Math.round(f.a / 21);
        var bN = Math.round(f.b / 21);
        var c2N = aN * aN + bN * bN;
        var cN = Math.sqrt(c2N).toFixed(2);
        says(marks, 14, 'សាកល្បង៖ a = ' + aN + ', b = ' + bN + ' ⟹ c² = ' + aN + '² + ' + bN + '² = ' + c2N + ' (c ≈ ' + cN + ')');
      }
    },
    anim: function (f, i) {
      return null;
    }
  };

  // Grade 8, lesson 17, Medians and Centroid G (1. លក្ខណៈមេដ្យាននៃត្រីកោណ):
  // Step-by-step interactive proof showing concurrency at centroid G,
  // the reflection point D, auxiliary parallelogram BDCG, and 2:1 ratio.
  CX['g8-l17-centroid'] = {
    steps: 7,
    start: { A: [280, 80], B: [100, 360], C: [500, 360] },
    place: function (s, key, p) {
      if (key === 'A') {
        s.A = [Math.max(160, Math.min(440, p[0])), Math.max(60, Math.min(160, p[1]))];
      } else if (key === 'B') {
        s.B = [Math.max(50, Math.min(s.C[0] - 160, p[0])), Math.max(300, Math.min(400, p[1]))];
      } else if (key === 'C') {
        s.C = [Math.max(s.B[0] + 160, Math.min(590, p[0])), Math.max(300, Math.min(400, p[1]))];
      }
      return p;
    },
    limit: function (s, key, p) { return true; },
    figure: function (s) {
      var A = s.A, B = s.B, C = s.C;
      var Cp = mul(add(A, B), 0.5);      // Midpoint of AB
      var Bp = mul(add(A, C), 0.5);      // Midpoint of AC
      var Ap = mul(add(B, C), 0.5);      // Midpoint of BC
      var G = mul(add(add(A, B), C), 1 / 3); // Centroid G
      // Point D: reflection of A across G, so G is midpoint of AD
      var D = add(G, sub(G, A));

      var dAA = len(sub(Ap, A));
      var dAG = len(sub(G, A));
      var dGA = len(sub(Ap, G));
      var cmAA = (Math.round(dAA / CM * 10) / 10).toFixed(1);
      var cmAG = (Math.round(dAG / CM * 10) / 10).toFixed(1);
      var cmGA = (Math.round(dGA / CM * 10) / 10).toFixed(1);

      return {
        meet: true, A: A, B: B, C: C,
        Cp: Cp, Bp: Bp, Ap: Ap, G: G, D: D,
        cmAA: cmAA, cmAG: cmAG, cmGA: cmGA
      };
    },
    draw: function (f, i, g, layer) {
      var ink = layer.ink, marks = layer.marks, tools = layer.tools;
      var poly = function (g2, pts, attrs) {
        var pStr = pts.map(function (x) { return x[0].toFixed(1) + ',' + x[1].toFixed(1); }).join(' ');
        return el('polygon', Object.assign({ points: pStr }, attrs), g2);
      };

      // Shaded triangle ABC
      poly(ink, [f.A, f.B, f.C], { fill: 'rgba(46, 122, 112, 0.06)', stroke: '#2e7a70', 'stroke-width': '2.5' });

      // Midpoint tick marks on AB and AC
      tick(marks, f.A, f.Cp); tick(marks, f.Cp, f.B);
      tick2(marks, f.A, f.Bp); tick2(marks, f.Bp, f.C);

      if (i === 0) {
        says(marks, 0, 'លក្ខណៈមេដ្យាន និងទីប្រជុំទម្ងន់នៃត្រីកោណ ៖');
        says(marks, 1, '• ត្រីកោណ ABC មាន C′ ជាចំណុចកណ្ដាលនៃ AB និង B′ ជាចំណុចកណ្ដាលនៃ AC');
        says(marks, 2, '• មេដ្យាន BB′ និង CC′ ប្រសព្វគ្នាត្រង់ចំណុច G');
        says(marks, 4, 'គោលដៅ ៖ បង្ហាញថាមេដ្យាន AA′ កាត់តាម G  ព្រមទាំង GA′ = ⅓ AA′ និង AG = ⅔ AA′');
      }

      // Step 1: Draw medians BB' and CC' intersecting at G
      if (i >= 1) {
        segLine(ink, f.B, f.Bp, 'cx-seg');
        segLine(ink, f.C, f.Cp, 'cx-seg');
        point(ink, f.G, 'G', [1.2, 0.2], 'cx-pt-m', null, 24);
      }
      if (i === 1) {
        says(marks, 0, 'គូសមេដ្យាន BB′ និង CC′ កាត់គ្នាត្រង់ចំណុច G');
        says(marks, 1, 'ចំណុចប្រសព្វ G នេះ ហៅថា «ទីប្រជុំទម្ងន់» (Centroid) នៃត្រីកោណ ABC');
        says(marks, 3, 'ដើម្បីស្រាយបញ្ជាក់ យើងបង្កើតចំណុចឆ្លុះ D នៃកំពូល A ធៀបនឹង G');
      }

      // Step 2: Extend ray AG to D such that GD = AG
      if (i >= 2) {
        segLine(ink, f.A, f.D, 'cx-line cx-line-2');
        point(ink, f.D, 'D', [0, 1.2], 'cx-pt-m', null, 24);
        tick3(marks, f.A, f.G); tick3(marks, f.G, f.D);
      }
      if (i === 2) {
        says(marks, 0, 'តាង D ជាចំណុចឆ្លុះនៃ A ធៀបនឹង G (បន្លាយកាំ AG ឱ្យបាន GD = AG)');
        says(marks, 1, '⟹ G ជាចំណុចកណ្ដាលនៃអង្កត់ AD (AG = GD)');
      }

      // Step 3: Triangle ABD and CG || BD
      if (i >= 3) {
        segLine(ink, f.B, f.D, 'cx-seg');
      }
      if (i === 3) {
        poly(marks, [f.A, f.B, f.D], { fill: 'rgba(232, 114, 92, 0.16)', stroke: 'none' });
        arrowHead(marks, mul(add(f.Cp, f.G), 0.5), unit(sub(f.G, f.Cp)));
        arrowHead(marks, mul(add(f.B, f.D), 0.5), unit(sub(f.D, f.B)));
        says(marks, 0, 'ក្នុងត្រីកោណ ABD (ពណ៌ផ្កាឈូក) ៖');
        says(marks, 1, '• C′ ជាចំណុចកណ្ដាលនៃ AB និង G ជាចំណុចកណ្ដាលនៃ AD');
        says(marks, 2, 'តាមទ្រឹស្ដីបទចំណុចកណ្ដាល ⟹ C′G ∥ BD ឬ CG ∥ BD   (១)');
      }

      // Step 4: Triangle ACD and BG || CD
      if (i >= 4) {
        segLine(ink, f.C, f.D, 'cx-seg');
      }
      if (i === 4) {
        poly(marks, [f.A, f.C, f.D], { fill: 'rgba(201, 134, 43, 0.16)', stroke: 'none' });
        arrowHead(marks, mul(add(f.Bp, f.G), 0.5), unit(sub(f.G, f.Bp)));
        arrowHead(marks, mul(add(f.C, f.D), 0.5), unit(sub(f.D, f.C)));
        says(marks, 0, 'ក្នុងត្រីកោណ ACD (ពណ៌ទឹកក្រូច) ៖');
        says(marks, 1, '• B′ ជាចំណុចកណ្ដាលនៃ AC និង G ជាចំណុចកណ្ដាលនៃ AD');
        says(marks, 2, 'តាមទ្រឹស្ដីបទចំណុចកណ្ដាល ⟹ B′G ∥ CD ឬ BG ∥ CD   (២)');
      }

      // Step 5: Parallelogram BDCG and median AA'
      if (i >= 5) {
        poly(marks, [f.B, f.D, f.C, f.G], { fill: 'rgba(45, 106, 168, 0.14)', stroke: 'none' });
        arrowHead(marks, mul(add(f.B, f.D), 0.5), unit(sub(f.D, f.B)));
        arrowHead(marks, mul(add(f.G, f.C), 0.5), unit(sub(f.C, f.G)));
        arrowHead(marks, mul(add(f.C, f.D), 0.5), unit(sub(f.D, f.C)));
        arrowHead(marks, mul(add(f.G, f.B), 0.5), unit(sub(f.B, f.G)));
        point(ink, f.Ap, "A'", [0, 1.2], 'cx-pt-m');
        tick2(marks, f.B, f.Ap); tick2(marks, f.Ap, f.C);
      }
      if (i === 5) {
        says(marks, 0, 'តាម (១) និង (២) ៖ CG ∥ BD និង BG ∥ CD ⟹ ចតុកោណ BDCG ជាប្រលេឡូក្រាម');
        says(marks, 1, 'អង្កត់ទ្រូងទាំងពីរ BC និង GD កាត់គ្នាត្រង់ចំណុចកណ្ដាលរួម A′');
        says(marks, 2, '⟹ A′ ជាចំណុចកណ្ដាលនៃ BC ដូច្នេះបន្ទាត់ AG កាត់តាម A′');
        says(marks, 3, 'សន្និដ្ឋាន ៖ មេដ្យានទី ៣ AA′ កាត់តាម G ដែរ ⟹ មេដ្យានទាំង ៣ ប្រសព្វគ្នាត្រង់ G តែមួយ!');
      }

      // Step 6: Ratio calculations and live measurement demo
      if (i >= 6) {
        segLine(ink, f.A, f.Ap, 'cx-seg');
        poly(marks, [f.B, f.D, f.C, f.G], { fill: 'rgba(45, 106, 168, 0.10)', stroke: 'none' });
        says(marks, 0, 'ទាញរកសមាមាត្រនៃទីប្រជុំទម្ងន់ G ៖');
        says(marks, 1, '• ក្នុងប្រលេឡូក្រាម BDCG ៖ A′ ជាចំណុចកណ្ដាលនៃ GD ⟹ GD = 2 GA′');
        says(marks, 2, '• ដោយ AG = GD នាំឱ្យ AG = 2 GA′ ⟹ AA′ = AG + GA′ = 3 GA′');
        says(marks, 3, '• នាំឱ្យ GA′ = ⅓ AA′  និង  AG = ⅔ AA′  (បានសម្រាយបញ្ជាក់សព្វគ្រប់!)');
        says(marks, 5, 'រង្វាស់ជាក់ស្ដែង ៖ AA′ = ' + f.cmAA + ' cm  |  AG = ' + f.cmAG + ' cm  |  GA′ = ' + f.cmGA + ' cm');
      }

      // Draggable vertices
      point(ink, f.A, 'A', [0, -1], null, 'A', 22);
      point(ink, f.B, 'B', [-1, 0.8], null, 'B', 22);
      point(ink, f.C, 'C', [1, 0.8], null, 'C', 22);
      point(ink, f.Cp, "C'", [-1.2, -0.2], 'cx-pt-m', null, 22);
      point(ink, f.Bp, "B'", [1.2, -0.2], 'cx-pt-m', null, 22);
    },
    anim: function (f, i) {
      if (i === 1) return { rulers: [[f.B, f.Bp], [f.C, f.Cp]] };
      if (i === 2) return { ruler: [f.A, f.D], cls: 'cx-line cx-line-2' };
      if (i === 3) return { ruler: [f.B, f.D], cls: 'cx-seg' };
      if (i === 4) return { ruler: [f.C, f.D], cls: 'cx-seg' };
      if (i === 6) return { ruler: [f.A, f.Ap], cls: 'cx-seg' };
      return null;
    }
  };


  // ===== The circle (Grade 7, lesson 17), one page with three tabs ====================================
  // #parts: draw a circle and name its parts. #pi: a disc rolled once along a ruler: the circumference
  // is a little more than three diameters. #area: a disc cut in n equal sectors that are laid head to
  // foot make nearly a rectangle with sides pi*R and R.
  var CO = [320, 232], CR = 150;
  var angOf = function (p) { return Math.atan2(p[1] - CO[1], p[0] - CO[0]); };
  CX['circle-parts'] = scripted({
    steps: 6,
    start: { C: [CO[0] + CR * Math.cos(-0.95), CO[1] + CR * Math.sin(-0.95)] },
    place: function (s, key, p) {
      var t = angOf(p);
      if (Math.abs(t) < 0.3) t = t < 0 ? -0.3 : 0.3;
      if (Math.PI - Math.abs(t) < 0.3) t = t < 0 ? -Math.PI + 0.3 : Math.PI - 0.3;
      return onCircle(CO, CR, t);
    },
    figure: function (s) {
      var C = s.C, tC = angOf(C);
      return { O: CO, A: [CO[0] - CR, CO[1]], B: [CO[0] + CR, CO[1]], C: C, tC: tC };
    },
    top: function (f, ink, i) { if (i >= 2) el('circle', { cx: f.C[0], cy: f.C[1], r: 24, class: 'cx-grab', 'data-drag': 'C' }, ink); },
    script: function (f) {
      var mid = function (P, Q, n, d) { var m = mul(add(P, Q), 0.5), u = unit(sub(Q, P)); return add(m, mul([-u[1] * n, u[0] * n], d)); };
      return [
        [['pt', f.O, 'O', [-0.6, 0.9], 'cx-pt-m', 22], ['pt', f.A, 'A', [-1, 0.4], null, 22]],
        [['arc', { c: f.O, r: CR, t1: Math.PI, t2: 3 * Math.PI - 0.003 }]],
        [['seg', f.O, f.C, 'cx-line cx-line-2'], ['pt', f.C, 'C', sub(f.C, f.O), null, 22],
          ['mark', function (g) { label(g, mid(f.O, f.C, -1, 18), 'កាំ OC', 'cx-note'); }]],
        [['seg', f.A, f.B, 'cx-line'], ['pt', f.B, 'B', [1, 0.4], null, 22],
          ['mark', function (g) { label(g, [CO[0] - 70, CO[1] + 24], 'អង្កត់ផ្ចិត AB', 'cx-note'); }]],
        [['seg', f.B, f.C, 'cx-line cx-line-2'],
          ['mark', function (g) { label(g, mid(f.B, f.C, -1, 30), 'អង្កត់ធ្នូ BC', 'cx-note'); }]],
        [['mark', function (g) {
          var t1 = Math.min(0, f.tC), t2 = Math.max(0, f.tC);
          el('path', { d: arcPath(CO, CR, t1, t2), class: 'cx-trace' }, g);
          label(g, add(CO, mul(unit([Math.cos((t1 + t2) / 2), Math.sin((t1 + t2) / 2)]), CR + 34)), 'ធ្នូ BC', 'cx-note');
        }]],
      ];
    },
  });

  // #pi: the disc has diameter k cm; it rolls without slipping one turn along the ruler
  var PIR = { x0: 92, y: 372 };
  CX['circle-pi'] = {
    steps: 5,
    start: { k: 4 },
    kScale: 1,
    kOk: function () { return true; },
    kText: function (s) { return 'អង្កត់ផ្ចិត d = ' + s.k + ' cm  →  បរិមាត្រ p = ' + (Math.round(Math.PI * s.k * 100) / 100) + ' cm  →  p ÷ d = ' + (Math.round(Math.PI * 100) / 100); },
    figure: function (s) {
      var d = s.k * CM;
      return { d: d, R: d / 2, p: Math.PI * d, x0: PIR.x0, y: PIR.y };
    },
    draw: function (f, i, g, layer) {
      var ink = layer.ink, marks = layer.marks, tools = layer.tools, x1 = f.x0 + f.p;
      drawCmRuler(ink, [f.x0, f.y], [1, 0], 14, [0, 1]);
      var disc = function (g2, cx, turn) {
        el('circle', { cx: cx, cy: f.y - f.R, r: f.R, class: 'cx-disc' }, g2);
        var P = add([cx, f.y - f.R], mul([Math.sin(turn), Math.cos(turn)], f.R));
        segLine(g2, [cx, f.y - f.R], P, 'cx-radius');
        el('circle', { cx: P[0], cy: P[1], r: 5.5, class: 'cx-pt cx-pt-m' }, g2);
        return P;
      };
      var cx0 = f.x0 + 0, cx1 = x1;
      if (i === 0) { disc(tools, cx0, 0); label(marks, [f.x0 + f.R, f.y - 2 * f.R - 18], 'd = ' + (f.d / CM) + ' cm', 'cx-note'); }
      else disc(tools, cx1, 0);
      if (i >= 2) {
        segLine(marks, [f.x0, f.y - 3], [x1, f.y - 3], 'cx-trace');
        label(marks, [(f.x0 + x1) / 2, f.y - 2 * f.R - 20], 'បរិមាត្រ p = ' + (Math.round(f.p / CM * 100) / 100) + ' cm', 'cx-note');
      }
      if (i >= 3) {
        for (var j = 0; j < 3; j++) {
          var a = f.x0 + j * f.d, y = f.y - 2 * f.R - 62 + 0;
          el('rect', { x: a + 1, y: 70, width: f.d - 2, height: 26, rx: 4, class: j % 2 ? 'cx-sector cx-sector-b' : 'cx-sector cx-sector-a' }, marks);
          label(marks, [a + f.d / 2, 83], 'd', 'cx-note cx-r');
        }
        var rest = f.p - 3 * f.d;
        el('rect', { x: f.x0 + 3 * f.d + 1, y: 70, width: rest - 2, height: 26, rx: 4, class: 'cx-sector cx-sector-c' }, marks);
        label(marks, [f.x0 + 3 * f.d + rest / 2, 56], '0.14 d', 'cx-note');
        label(marks, [f.x0 + 1.5 * f.d, 108], 'បីដងអង្កត់ផ្ចិត', 'cx-note');
      }
      if (i >= 4) given(marks, 'p ÷ d = ' + (Math.round(f.p / f.d * 100) / 100) + ' ...  =  π   ក្នុងរង្វង់ទាំងអស់');
    },
    anim: function (f, i) {
      if (i !== 1) return null;
      return { phases: [{ dur: 4200, draw: function (t, drawn, tools) {
        var cx = f.x0 + f.p * t, turn = 2 * Math.PI * t;
        segLine(drawn, [f.x0, f.y - 3], [cx, f.y - 3], 'cx-trace');
        el('circle', { cx: cx, cy: f.y - f.R, r: f.R, class: 'cx-disc' }, tools);
        var P = add([cx, f.y - f.R], mul([Math.sin(turn), Math.cos(turn)], f.R));
        segLine(tools, [cx, f.y - f.R], P, 'cx-radius');
        el('circle', { cx: P[0], cy: P[1], r: 5.5, class: 'cx-pt cx-pt-m' }, tools);
      } }] };
    },
  };

  // #area: the disc of radius R in n = 2^(k+1) sectors; they stand alternately point down and point up
  var AR = { R: 92, O: [130, 190], x0: 250, y: 300 };
  CX['circle-area'] = {
    steps: 5,
    start: { k: 3 },
    kScale: 1,
    kOk: function () { return true; },
    kText: function (s) {
      var n = Math.pow(2, s.k + 1);
      return n + ' ចំណែក → រាងចតុកោណកែងប្រហែលវិមាត្រ πR និង R' + (n >= 32 ? ' (ស្ទើរតែពិតប្រាកដ)' : '');
    },
    figure: function (s) {
      var n = Math.pow(2, s.k + 1), th = 2 * Math.PI / n, R = AR.R, hw = R * Math.sin(th / 2), tops = [];
      var secs = [];
      for (var j = 0; j < n; j++) {
        var up = j % 2 === 0, from = -Math.PI / 2 + j * th, centre = from + th / 2;
        var apex = [AR.x0 + 20 + j * hw, up ? AR.y : AR.y - R * Math.cos(th / 2)];
        var target = up ? -Math.PI / 2 : Math.PI / 2;
        secs.push({ j: j, centre: centre, apex: apex, target: target, up: up });
      }
      return { n: n, th: th, R: R, hw: hw, secs: secs, width: n * hw + hw };
    },
    draw: function (f, i, g, layer) {
      var ink = layer.ink, marks = layer.marks, O = AR.O;
      var sector = function (g2, apex, centre, cls) {
        var a1 = centre - f.th / 2, a2 = centre + f.th / 2, p1 = onCircle(apex, f.R, a1);
        el('path', { d: 'M' + apex.join(' ') + 'L' + p1.map(function (x) { return x.toFixed(1); }).join(' ') + arcPath(apex, f.R, a1, a2).replace(/^M[^A]*/, '') + 'Z', class: cls + ' cx-sector-line' }, g2);
      };
      if (i <= 1) {
        el('circle', { cx: O[0], cy: O[1], r: f.R, class: 'cx-disc' }, ink);
        if (i === 1) f.secs.forEach(function (q) { sector(ink, O, q.centre, q.j % 2 ? 'cx-sector cx-sector-b' : 'cx-sector cx-sector-a'); });
        point(ink, O, 'O', [-0.6, 0.9], 'cx-pt-m', null, 20);
        segLine(marks, O, add(O, [f.R, 0]), 'cx-radius'); label(marks, add(O, [f.R / 2, 14]), 'R', 'cx-note cx-r');
      }
      if (i >= 2) {
        f.secs.forEach(function (q) { sector(ink, q.apex, q.target, q.j % 2 ? 'cx-sector cx-sector-b' : 'cx-sector cx-sector-a'); });
      }
      if (i >= 3) {
        var x1 = AR.x0 + 20, x2 = x1 + f.width;
        segLine(marks, [x1, AR.y + 20], [x2, AR.y + 20], 'cx-trace');
        label(marks, [(x1 + x2) / 2, AR.y + 40], 'πR  (កន្លះបរិមាត្រ = πR)', 'cx-note');
        segLine(marks, [x2 + 16, AR.y], [x2 + 16, AR.y - f.R], 'cx-trace');
        label(marks, [x2 + 30, AR.y - f.R / 2], 'R', 'cx-note cx-r');
      }
      if (i >= 4) given(marks, 'S = πR × R = πR²');
    },
    anim: function (f, i) {
      if (i === 2) return { phases: [{ dur: 3200, draw: function (t, drawn, tools) {
        f.secs.forEach(function (q) {
          var d = ((q.target - q.centre + Math.PI) % (2 * Math.PI) + 2 * Math.PI) % (2 * Math.PI) - Math.PI;
          var c = q.centre + d * t, apex = add(AR.O, mul(sub(q.apex, AR.O), t));
          var a1 = c - f.th / 2, a2 = c + f.th / 2, p1 = onCircle(apex, f.R, a1);
          el('path', { d: 'M' + apex.join(' ') + 'L' + p1.map(function (x) { return x.toFixed(1); }).join(' ') + arcPath(apex, f.R, a1, a2).replace(/^M[^A]*/, '') + 'Z',
            class: (q.j % 2 ? 'cx-sector cx-sector-b' : 'cx-sector cx-sector-a') + ' cx-sector-line' }, drawn);
        });
      } }] };
      return null;
    },
  };

  // a line of the working, below the one before it (the lines of the steps so far stay)
  var says = function (g, n, text) { el('text', { x: 22, y: 30 + 24 * n, class: 'cx-given', 'dominant-baseline': 'central' }, g).textContent = text; };
  var deg = function (n) { return n + '°'; };
  CX['g7-l15-angle-sum'] = scripted({
    steps: 5,
    start: triStart,
    limit: triLimit,
    figure: function (s) {
      var f = triangleOf(s), u = unit(sub(f.C, f.B));
      f.X = sub(f.A, mul(u, 210)); f.Y = add(f.A, mul(u, 210)); f.deg = wholeDegrees(f);
      return f;
    },
    base: function (f, ink) { triDrawn(f, ink); },
    top: function (f, ink) { triCorners(f, ink); },
    script: function (f) {
      var dir = function (P, Q) { return unit(add(unit(sub(P, f.A)), unit(sub(Q, f.A)))); };
      var at = function (g, P, Q, text) { label(g, add(f.A, mul(dir(P, Q), 66)), text, 'cx-note'); };
      return [
        [],
        [['seg', f.X, f.Y, 'cx-line cx-line-2'], ['pt', f.X, 'x', [-1, 0], null, 16], ['pt', f.Y, 'y', [1, 0], null, 16]],
        [['mark', function (g) {
          wedgeBetween(g, f.A, f.X, f.B, 36, 'a'); wedgeBetween(g, f.A, f.B, f.C, 42, 'c'); wedgeBetween(g, f.A, f.C, f.Y, 36, 'b');
          at(g, f.X, f.B, 'A₁'); at(g, f.B, f.C, 'A'); at(g, f.C, f.Y, 'A₂');
          says(g, 0, '∠A₁ + ∠A + ∠A₂ = 180°');
        }]],
        [['mark', function (g) {
          wedgeBetween(g, f.B, f.C, f.A, 36, 'a'); wedgeBetween(g, f.C, f.A, f.B, 36, 'b');
          says(g, 1, '∠A₁ = ∠B  ,  ∠A₂ = ∠C');
        }]],
        [['mark', function (g) {
          says(g, 2, '∠A + ∠B + ∠C = ' + deg(f.deg[0]) + ' + ' + deg(f.deg[1]) + ' + ' + deg(f.deg[2]) + ' = 180°');
        }]],
      ];
    },
  });
  CX['g7-l15-exterior-angle'] = scripted({
    steps: 5,
    start: triStart,
    limit: triLimit,
    figure: function (s) {
      var f = triangleOf(s);
      f.x = add(f.C, mul(unit(sub(f.C, f.B)), 70)); f.y = add(f.B, mul(unit(sub(f.B, f.A)), 54)); f.z = add(f.A, mul(unit(sub(f.A, f.C)), 70));
      f.deg = wholeDegrees(f);
      return f;
    },
    base: function (f, ink) { triDrawn(f, ink); },
    top: function (f, ink) { triCorners(f, ink); },
    script: function (f) {
      var aux = 'cx-line cx-line-2';
      return [
        [],
        [['seg', f.C, f.x, aux], ['pt', f.x, 'x', sub(f.x, f.C), null, 16], ['seg', f.B, f.y, aux], ['pt', f.y, 'y', sub(f.y, f.B), null, 16],
          ['seg', f.A, f.z, aux], ['pt', f.z, 'z', sub(f.z, f.A), null, 16]],
        [['mark', function (g) {
          wedgeBetween(g, f.A, f.B, f.C, 40, 'a'); wedgeBetween(g, f.A, f.z, f.B, 40, 'b');
          says(g, 0, '∠A + ∠BAz = 180°');
        }]],
        [['mark', function (g) {
          wedgeBetween(g, f.B, f.C, f.A, 36, 'c'); wedgeBetween(g, f.C, f.A, f.B, 36, 'c');
          says(g, 1, '∠A + ∠B + ∠C = 180°');
        }]],
        [['mark', function (g) {
          says(g, 2, '∠BAz = ∠B + ∠C :  ' + deg(180 - f.deg[0]) + ' = ' + deg(f.deg[1]) + ' + ' + deg(f.deg[2]));
        }]],
      ];
    },
  });

  // ===== The protractor (Grade 7, lesson 13 §2.1), one page with two tabs =============================
  // #measure: the protractor goes on the vertex O, is turned until Ox lies on its 0, and Oy cuts the scale
  // where the measure is. #a150: the ray yx, the protractor with its 0 on yx, a pencil mark at the number,
  // the ray yz through the mark. In both the slider is the angle (5° to 175°), the book's own 50° and 150°
  // to begin with. The protractor has two scales; the numbers are read on the one that starts from 0 on the
  // first ray, so the 0 on the right is lit.
  var PT = { V: [320, 400], R: 190, L: 246 };               // the vertex, the radius of the protractor, the length of the rays
  var ptDir = function (a) { return prDir(RIGHT, a); };
  var ptAt = function (a, r) { return add(PT.V, mul(ptDir(a), r)); };
  var angleKind = function (a) { return a < 90 ? 'មុំស្រួច' : a === 90 ? 'មុំកែង' : 'មុំទាល'; };
  var angleWords = function (a) { return a < 90 ? 'មុំស្រួច  (0° < ∠ < 90°)' : a === 90 ? 'មុំកែង  (∠ = 90°)' : 'មុំទាល  (90° < ∠ < 180°)'; };
  var DEG = Math.PI / 180;
  // the protractor, centre c, turned by `turn` degrees (clockwise): the outer scale from 0 on the right, the
  // inner one from 0 on the left; `lit` lists degrees to mark on the outer scale
  function drawProt(g, c, turn, alpha, lit) {
    var R = PT.R, d, u, rim, low;
    var grp = el('g', { opacity: alpha == null ? 1 : alpha, transform: turn ? 'rotate(' + turn.toFixed(2) + ' ' + c[0] + ' ' + c[1] + ')' : null }, g);
    var half = function (r) { return 'M' + (c[0] + r) + ' ' + c[1] + 'A' + r + ' ' + r + ' 0 0 0 ' + (c[0] - r) + ' ' + c[1]; };
    el('path', { d: half(R) + 'Z', class: 'cx-pr' }, grp);
    el('path', { d: half(R - 42), class: 'cx-pr-line' }, grp);
    el('path', { d: half(16), class: 'cx-pr-line' }, grp);
    for (d = 0; d <= 180; d++) {
      u = ptDir(d); rim = add(c, mul(u, R));
      segLine(grp, rim, add(rim, mul(u, d % 10 === 0 ? -14 : d % 5 === 0 ? -10 : -6)), d % 5 ? 'cx-pr-tick cx-pr-t1' : 'cx-pr-tick');
      if (d % 30 === 0) {
        low = d % 180 ? [0, 0] : [0, -9];                     // 0 and 180 clear of the line they lie on
        label(grp, add(add(c, mul(u, R - 28)), low), String(d), 'cx-pr-num');
        label(grp, add(add(c, mul(u, R - 56)), low), String(180 - d), 'cx-pr-num cx-pr-num2');
      }
    }
    el('circle', { cx: c[0], cy: c[1], r: 3.2, class: 'cx-pr-c' }, grp);
    (lit || []).forEach(function (a) { segLine(grp, add(c, mul(ptDir(a), R - 16)), add(c, mul(ptDir(a), R + 4)), 'cx-pr-mark'); });
  }
  // the protractor comes down on the vertex, a little askew, and is then turned to lie on the first ray
  var protDown = function (V) { return { dur: 900, draw: function (t, drawn, tools) { drawProt(tools, add(V, [0, -40 * (1 - t)]), 22, 0.25 + 0.75 * t); } }; };
  var protTurn = function (V) { return { dur: 900, draw: function (t, drawn, tools) { drawProt(tools, V, 22 * (1 - t), 1, t === 1 ? [0] : null); } }; };
  var protKText = function (name, extra) {
    return function (s) { return '∠' + name + ' = ' + s.k + '°  →  ' + angleKind(s.k) + (extra ? extra(s.k) : ''); };
  };

  CX['protractor-measure'] = {
    steps: 5,
    start: { k: 50 },
    kScale: 1,
    kOk: function () { return true; },
    kText: protKText('xOy'),
    fill: function (s) { return { a: String(s.k) }; },
    figure: function (s) { return { meet: true, a: s.k, V: PT.V, X: ptAt(0, PT.L), Y: ptAt(s.k, PT.L) }; },
    draw: function (f, i, g, layer) {
      var ink = layer.ink, marks = layer.marks, tools = layer.tools, V = f.V, t = f.a * DEG;
      if (i === 4) { given(ink, '∠xOy = ' + f.a + '°'); says(ink, 1, angleWords(f.a)); }
      else given(ink, 'ចូររង្វាស់ ∠xOy');
      segLine(ink, V, f.X, 'cx-seg');
      segLine(ink, V, f.Y, 'cx-line');
      if (i < 3) {
        el('path', { d: arcPath(V, 46, 0, -t), class: 'cx-arc' }, ink);
        label(marks, ptAt(f.a / 2, 74), '?', 'cx-note cx-r');
      } else wedge(marks, V, 0, -t, 58, 'a');
      point(ink, V, 'O', [-0.6, 0.9], 'cx-pt-m', null, 22);
      point(ink, f.X, 'x', [0.85, -0.55], null, null, 22);
      point(ink, f.Y, 'y', ptDir(f.a), null, null, 22);
      if (i === 1) drawProt(tools, V, 22);
      if (i >= 2) drawProt(tools, V, 0, 1, i === 2 ? [0] : [0, f.a]);
      if (i === 2) label(marks, add(V, [PT.R + 24, -14]), '0°', 'cx-note cx-r');
      if (i === 3) label(marks, add(ptAt(f.a, PT.R + 20), mul(ptDir(f.a + 90), 22)), f.a + '°', 'cx-note cx-r');   // beside the ray, clear of its end
      if (i === 4) label(marks, ptAt(f.a / 2, 84), f.a + '°', 'cx-note cx-r');
    },
    anim: function (f, i) {
      if (i === 1) return { phases: [protDown(f.V)] };
      if (i === 2) return { phases: [protTurn(f.V)] };
      if (i === 3) return { phases: [{ dur: 1300, draw: function (t, drawn, tools) {   // the lit stroke runs from 0 up to the reading
        var a = f.a * t;
        if (a > 0.5) wedge(drawn, f.V, 0, -a * DEG, 58, 'a');
        drawProt(tools, f.V, 0, 1, [0, a]);
      } }] };
      return null;
    },
  };

  CX['protractor-150'] = {
    steps: 6,
    start: { k: 150 },
    kScale: 1,
    kOk: function () { return true; },
    kText: protKText('xyz', function (a) { return '  ·  មុំជាប់គ្នា ' + (180 - a) + '°'; }),
    fill: function (s) { return { a: String(s.k), b: String(180 - s.k) }; },
    figure: function (s) {
      return { meet: true, a: s.k, V: PT.V, X: ptAt(0, PT.L), Z: ptAt(s.k, PT.L), M: ptAt(s.k, PT.R + 8) };
    },
    draw: function (f, i, g, layer) {
      var ink = layer.ink, marks = layer.marks, tools = layer.tools, V = f.V, t = f.a * DEG;
      given(ink, (i === 5 ? '' : 'សង់ ') + '∠xyz = ' + f.a + '°');
      if (i === 5) says(ink, 1, 'មុំជាប់គ្នា៖ 180° − ' + f.a + '° = ' + (180 - f.a) + '°');
      if (i >= 1) segLine(ink, V, f.X, 'cx-seg');
      if (i >= 4) segLine(ink, V, f.Z, 'cx-line');
      if (i >= 3) dot(ink, f.M);
      if (i === 5) {
        segLine(ink, V, ptAt(180, PT.L), 'cx-ext');             // yx carried on the other side of y
        wedge(marks, V, 0, -t, 52, 'a');
        label(marks, ptAt(f.a / 2, 80), f.a + '°', 'cx-note cx-r');
        wedge(marks, V, -t, -(Math.PI - t), 36, 'b');
        label(marks, ptAt((f.a + 180) / 2, 62), (180 - f.a) + '°', 'cx-note');
      }
      point(ink, V, 'y', [-0.6, 0.9], 'cx-pt-m', null, 22);
      if (i >= 1) point(ink, f.X, 'x', [0.85, -0.55], null, null, 22);
      if (i >= 4) point(ink, f.Z, 'z', ptDir(f.a), null, null, 22);
      if (i === 2) { drawProt(tools, V, 0, 1, [0]); label(marks, add(V, [PT.R + 24, -14]), '0°', 'cx-note cx-r'); }
      if (i === 3) { drawProt(tools, V, 0, 1, [0, f.a]); label(marks, ptAt(f.a, PT.R + 34), f.a + '°', 'cx-note cx-r'); }
    },
    anim: function (f, i) {
      if (i === 1) return { ruler: [f.V, f.X], cls: 'cx-seg' };
      if (i === 2) return { phases: [protDown(f.V), protTurn(f.V)] };
      if (i === 3) return { phases: [{ dur: 900, draw: function (t, drawn, tools) {   // the pencil presses the paper at the number
        drawProt(tools, f.V, 0, 1, [0, f.a]);
        dot(drawn, f.M, 3.4 * Math.min(1, t * 2));
        el('circle', { cx: f.M[0], cy: f.M[1], r: 4.2, class: 'cx-c-pencil', opacity: t < 0.85 ? 1 : 0 }, tools);
      } }] };
      if (i === 4) return { ruler: [f.V, f.Z], cls: 'cx-line' };
      return null;
    },
  };

  function label(g, at, text, cls) {
    var t = el('text', { x: at[0], y: at[1], class: cls || 'cx-label', 'text-anchor': 'middle', 'dominant-baseline': 'central' }, g);
    t.textContent = text;
    return t;
  }
  // a point with its name pushed out along dir (by dist, 20 if not given)
  function point(g, p, name, dir, cls, drag, dist) {
    el('circle', { cx: p[0], cy: p[1], r: 5, class: 'cx-pt ' + (cls || '') }, g);
    var d = unit(dir || [0, -1]);
    label(g, add(p, mul(d, dist || 20)), name, 'cx-label');
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
      var a = animate && !reduce && def.anim ? def.anim(f, step) : null;
      if (!a) { render(step); return Promise.resolve(); }
      render(step - 1);
      clear(marks); clear(tools);                         // the previous step's hints go
      if (a.phases) {
        return new Promise(function (done) {
          var ph = 0, t0 = null, drawn = el('g', {}, ink);
          function frame(ts) {
            if (t0 == null) t0 = ts;
            var cur = a.phases[ph], t = Math.min(1, (ts - t0) / cur.dur);
            clear(tools); clear(drawn);
            cur.draw(ease(t), drawn, tools);
            if (t < 1) { raf = requestAnimationFrame(frame); return; }
            if (++ph < a.phases.length) { t0 = null; raf = requestAnimationFrame(frame); return; }
            raf = null;
            setTimeout(function () { if (!raf) render(step); done(); }, 350);
          }
          raf = requestAnimationFrame(frame);
        });
      }
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
      var words = ok ? root.getAttribute('data-k-ok') : root.getAttribute('data-k-short');
      kOut.textContent = def.kText ? def.kText(state, words) : words;
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

  // the tools and the small helpers, for the drawing board (static/js/board.js)
  window.KMGeo = { el: el, arcPath: arcPath, drawCompass: drawCompass, drawRuler: drawRuler, drawSetSquare: drawSetSquare,
    add: add, sub: sub, mul: mul, len: len, unit: unit };

  document.querySelectorAll('.cx[data-cx]').forEach(Player);

  // Reached from a picture of a lesson (?from=g8/L12.html#fig-...), the page offers the way back to
  // that picture: the button .cx-back, which the page holds hidden (its words are in the page).
  (function () {
    var back = document.querySelector('.cx-back'), m = /[?&]from=([^&#]*)/.exec(location.search);
    var from = m ? decodeURIComponent(m[1]) : '';
    if (!back) return;
    if (/^g[789]\/L\d\d\.html#fig-[a-z0-9-]+$/.test(from)) back.href = '../lesson/' + from;
    if (!back.getAttribute('href')) return;
    var first = document.querySelector('.cx-section .wrap');
    if (first && back.parentElement !== first) first.insertBefore(back, first.firstChild);
    back.hidden = false;
  })();

  // Several constructions on one page (the special angles): a row of tabs shows one at a time.
  // The address keeps the choice (#a30), so a link can open the page on one of them.
  document.querySelectorAll('.cx-tabs').forEach(function (bar) {
    var tabs = Array.prototype.slice.call(bar.querySelectorAll('[role="tab"]'));
    var pane = function (t) { return document.getElementById(t.getAttribute('aria-controls')); };
    function show(tab, focus) {
      tabs.forEach(function (t) {
        var on = t === tab, p = pane(t), playing = p.querySelector('.cx-play.on');
        t.setAttribute('aria-selected', on ? 'true' : 'false');
        t.tabIndex = on ? 0 : -1;
        if (!on && playing) playing.click();               // a hidden construction stops playing
        p.hidden = !on;
      });
      if (focus) tab.focus();
    }
    tabs.forEach(function (t, j) {
      t.addEventListener('click', function () {
        show(t);
        if (history.replaceState) history.replaceState(null, '', '#' + t.getAttribute('aria-controls'));
      });
      t.addEventListener('keydown', function (e) {
        var to = e.key === 'ArrowRight' ? j + 1 : e.key === 'ArrowLeft' ? j - 1 : null;
        if (to == null) return;
        e.preventDefault();
        tabs[(to + tabs.length) % tabs.length].click();
        tabs[(to + tabs.length) % tabs.length].focus();
      });
    });
    var fromHash = function () {
      var want = tabs.filter(function (t) { return '#' + t.getAttribute('aria-controls') === location.hash; })[0];
      if (want) show(want);
    };
    show(tabs.filter(function (t) { return t.getAttribute('aria-selected') === 'true'; })[0] || tabs[0]);
    fromHash();
    window.addEventListener('hashchange', fromHash);
  });
})();
