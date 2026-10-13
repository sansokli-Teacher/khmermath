/* khmermath.org — «អាលីដាត»: a simulator of the sighting bar (construct/alidade.html).
   One state (phi = the bar's direction, degrees clockwise from north) drawn three ways:
   the real instrument in 3D, the plan view with the graduated circle, and the view through the eye hole.
   Everything the student can drag turns the same bar. */
(function () {
  'use strict';
  var root = document.getElementById('al');
  if (!root) return;

  var NS = 'http://www.w3.org/2000/svg';
  var RAD = Math.PI / 180;
  var KH = '០១២៣៤៥៦៧៨៩';
  function kh(s) { return String(s).replace(/\d/g, function (d) { return KH[d]; }).replace('.', ','); }
  function norm(a) { return ((a % 360) + 360) % 360; }
  function diff(a, b) { var d = norm(a - b); return d > 180 ? d - 360 : d; }   // signed, -180..180
  function el(parent, tag, attrs, text) {
    var e = document.createElementNS(NS, tag);
    for (var k in attrs) e.setAttribute(k, attrs[k]);
    if (text != null) e.textContent = text;
    if (parent) parent.appendChild(e);
    return e;
  }
  function $(id) { return document.getElementById(id); }

  var TOL = 0.7;                       // how close the hair must be to the target (degrees)
  var phi = 20;
  var tg = { P: { b: 60, d: 1 }, Q: { b: 140, d: 1.2 } };
  var rec = { P: null, Q: null };
  var busy = false;                    // the guided demo is running

  function newTargets() {
    var p = Math.floor(Math.random() * 360), g = 25 + Math.floor(Math.random() * 126);
    if (Math.random() < .5) g = -g;
    tg.P = { b: p, d: 0.85 + Math.random() * .5 };
    tg.Q = { b: norm(p + g), d: 0.85 + Math.random() * .5 };
    rec.P = rec.Q = null;
  }
  newTargets();

  /* ---------- plan view ---------- */
  var top = $('al-top'), topBar, topLine, topSector, topMarks = {}, topTarget = {};
  (function buildTop() {
    el(top, 'circle', { cx: 0, cy: 0, r: 130, fill: '#e3efd0' });
    el(top, 'circle', { cx: 0, cy: 0, r: 100, fill: '#fffdf3', stroke: '#7a5a22', 'stroke-width': 2 });
    el(top, 'circle', { cx: 0, cy: 0, r: 70, fill: 'none', stroke: '#d9cfae' });
    topSector = el(top, 'path', { d: '', fill: 'rgba(232,113,10,.22)', stroke: 'none' });
    var g = el(top, 'g', {});
    for (var a = 0; a < 360; a += 2) {
      var long = a % 10 === 0, mid = a % 5 === 0, r1 = long ? 86 : (mid ? 91 : 94);
      var s = Math.sin(a * RAD), c = -Math.cos(a * RAD);
      el(g, 'line', { x1: s * r1, y1: c * r1, x2: s * 100, y2: c * 100, stroke: '#7a5a22', 'stroke-width': long ? 1.2 : .7 });
    }
    for (a = 0; a < 360; a += 30) {
      el(g, 'text', { x: Math.sin(a * RAD) * 76, y: -Math.cos(a * RAD) * 76 + 3.5, 'text-anchor': 'middle', 'font-size': 10, fill: '#5a4216' }, kh(a));
    }
    el(top, 'text', { x: 0, y: -108, 'text-anchor': 'middle', 'font-size': 9, fill: '#7a5a22', 'font-weight': 700 }, 'ទិសសូន្យ ០°');
    ['P', 'Q'].forEach(function (k) {
      var m = el(top, 'g', {});
      topMarks[k] = el(m, 'line', { x1: 0, y1: 0, x2: 0, y2: 0, stroke: '#e8710a', 'stroke-width': 2.2 });
      var t = el(top, 'g', {});
      el(t, 'line', { x1: 0, y1: 0, x2: 0, y2: -6, stroke: '#6b4a1c', 'stroke-width': 2 });
      el(t, 'path', { d: 'M0 -6l9 3.5-9 3.5z', fill: '#d6423a' });
      el(t, 'text', { x: 0, y: 12, 'text-anchor': 'middle', 'font-size': 13, fill: '#132238', class: 'al-it' }, k);
      topTarget[k] = t;
    });
    topLine = el(top, 'line', { x1: 0, y1: 0, x2: 0, y2: -125, stroke: '#e8710a', 'stroke-dasharray': '4 4', 'stroke-width': 1.3 });
    topBar = el(top, 'g', {});
    el(topBar, 'rect', { x: -9, y: -100, width: 18, height: 200, rx: 3, fill: '#d9a35a', stroke: '#8a5a1c', 'stroke-width': 1.5 });
    el(topBar, 'rect', { x: -4, y: 66, width: 8, height: 22, fill: '#2b1d0c' });                    // the eye-end plate
    el(topBar, 'rect', { x: -9, y: -92, width: 18, height: 5, fill: '#2b1d0c' });                   // the slit plate
    el(topBar, 'line', { x1: 0, y1: -92, x2: 0, y2: -87, stroke: '#e03a2e', 'stroke-width': 1.4 }); // the hair
    el(topBar, 'path', { d: 'M0 -100 l-5 12 h10z', fill: '#d6423a' });                               // the pointer
    el(top, 'circle', { cx: 0, cy: 0, r: 5, fill: '#9aa5b1', stroke: '#4c5866', 'stroke-width': 1.5 });
    el(top, 'text', { x: 9, y: 16, 'font-size': 13, fill: '#132238', class: 'al-it' }, 'O');
  })();

  /* ---------- the view through the eye hole ---------- */
  var eye = $('al-eye'), eyeScene, eyeHair, eyeTag, PX = 15;       // 15 px per degree: 40° across
  var HILLS = [[10, 38], [40, 26], [95, 44], [150, 30], [205, 40], [250, 28], [300, 46], [335, 30]];
  var TREES = [[22, .9], [78, 1.2], [118, .8], [172, 1.1], [228, .9], [262, 1.3], [318, 1], [350, 1.1]];
  (function buildEye() {
    el(eye, 'rect', { x: 0, y: 0, width: 600, height: 120, fill: '#cfe6f5' });
    el(eye, 'rect', { x: 0, y: 120, width: 600, height: 100, fill: '#b9d889' });
    eyeScene = el(eye, 'g', {});
    var frame = el(eye, 'g', { 'pointer-events': 'none' });
    el(frame, 'path', { d: 'M0 0H600V220H0Z M18 14V206H582V14Z', 'fill-rule': 'evenodd', fill: '#6b4a1c' });
    el(frame, 'rect', { x: 18, y: 14, width: 564, height: 192, fill: 'none', stroke: '#2b1d0c', 'stroke-width': 2 });
    eyeHair = el(frame, 'line', { x1: 300, y1: 14, x2: 300, y2: 206, stroke: '#e03a2e', 'stroke-width': 1.6 });
    el(frame, 'text', { x: 300, y: 10, 'text-anchor': 'middle', 'font-size': 10, fill: '#fff', class: 'al-it' }, 'Z');
    el(frame, 'text', { x: 300, y: 217, 'text-anchor': 'middle', 'font-size': 10, fill: '#fff', class: 'al-it' }, 'Z′');
    eyeTag = el(frame, 'text', { x: 312, y: 36, 'font-size': 15, fill: '#14653f', 'font-weight': 700 }, '');
  })();

  function eyeX(b) { return 300 + diff(b, phi) * PX; }
  function drawEye() {
    while (eyeScene.firstChild) eyeScene.removeChild(eyeScene.firstChild);
    HILLS.forEach(function (h) {
      var x = eyeX(h[0]); if (x < -120 || x > 720) return;
      el(eyeScene, 'path', { d: 'M' + (x - 110) + ' 120Q' + x + ' ' + (120 - h[1] * 2.2) + ' ' + (x + 110) + ' 120Z', fill: '#9bbf8a' });
    });
    TREES.forEach(function (t) {
      var x = eyeX(t[0]); if (x < -30 || x > 630) return;
      var s = t[1] * 14;
      el(eyeScene, 'rect', { x: x - 2 * t[1], y: 122, width: 4 * t[1], height: 14 * t[1], fill: '#7a5230' });
      el(eyeScene, 'circle', { cx: x, cy: 118, r: s, fill: '#3f8f4e' });
    });
    ['P', 'Q'].forEach(function (k) {
      var x = eyeX(tg[k].b); if (x < -30 || x > 630) return;
      var h = 105 / tg[k].d, base = 150 + (1 - 1 / tg[k].d) * 30;
      el(eyeScene, 'line', { x1: x, y1: base, x2: x, y2: base - h, stroke: '#5a3b16', 'stroke-width': 4 });
      el(eyeScene, 'path', { d: 'M' + x + ' ' + (base - h) + 'l26 10-26 10z', fill: '#d6423a' });
      el(eyeScene, 'text', { x: x, y: base - h - 7, 'text-anchor': 'middle', 'font-size': 18, fill: '#132238', class: 'al-it' }, k);
    });
  }

  /* ---------- the real instrument in 3D ---------- */
  var real = $('al-3d'), names = $('al-names');
  var CY = -28 * RAD, CP = 30 * RAD, SC = 98, OX = 200, OYY = 190;
  function P3(x, y, z) {
    var X = x * Math.cos(CY) - y * Math.sin(CY), Y = x * Math.sin(CY) + y * Math.cos(CY);
    return { x: OX + SC * X, y: OYY - SC * (z * Math.cos(CP) + Y * Math.sin(CP)), d: Y * Math.cos(CP) - z * Math.sin(CP) };
  }
  function pts(a) { return a.map(function (p) { return p.x.toFixed(1) + ',' + p.y.toFixed(1); }).join(' '); }

  function drawReal() {
    while (real.firstChild) real.removeChild(real.firstChild);
    var s = Math.sin(phi * RAD), c = Math.cos(phi * RAD);
    function W(sv, v, z) { return P3(sv * s + v * c, sv * c - v * s, z); }   // bar coordinates -> world -> screen

    // ground shadow and the three legs
    var sh = []; for (var a = 0; a < 360; a += 10) sh.push(P3(Math.sin(a * RAD) * 1.25, Math.cos(a * RAD) * 1.25, -.95));
    el(real, 'polygon', { points: pts(sh), fill: 'rgba(60,70,40,.18)' });
    [0, 120, 240].forEach(function (a) {
      var f = P3(Math.sin((a + 20) * RAD) * 1.05, Math.cos((a + 20) * RAD) * 1.05, -.95), t = P3(0, 0, -.1);
      el(real, 'line', { x1: t.x, y1: t.y, x2: f.x, y2: f.y, stroke: '#6b4a1c', 'stroke-width': 5, 'stroke-linecap': 'round' });
    });
    // the graduated circle
    var ring = []; for (a = 0; a < 360; a += 6) ring.push(P3(Math.sin(a * RAD), Math.cos(a * RAD), 0));
    var rim = []; for (a = 0; a < 360; a += 6) rim.push(P3(Math.sin(a * RAD), Math.cos(a * RAD), -.05));
    el(real, 'polygon', { points: pts(rim), fill: '#b89a62' });
    el(real, 'polygon', { points: pts(ring), fill: '#fffdf3', stroke: '#7a5a22', 'stroke-width': 1.6 });
    for (a = 0; a < 360; a += 10) {
      var r1 = a % 30 === 0 ? .84 : .91, p1 = P3(Math.sin(a * RAD) * r1, Math.cos(a * RAD) * r1, 0), p2 = P3(Math.sin(a * RAD), Math.cos(a * RAD), 0);
      el(real, 'line', { x1: p1.x, y1: p1.y, x2: p2.x, y2: p2.y, stroke: '#7a5a22', 'stroke-width': a % 30 === 0 ? 1.4 : .8 });
    }
    [[0, '០°'], [90, '៩០°'], [180, '១៨០°'], [270, '២៧០°']].forEach(function (l) {
      var p = P3(Math.sin(l[0] * RAD) * .7, Math.cos(l[0] * RAD) * .7, 0);
      el(real, 'text', { x: p.x, y: p.y + 3, 'text-anchor': 'middle', 'font-size': 10, fill: '#5a4216' }, l[1]);
    });
    // lower part of the axis
    var o0 = P3(0, 0, 0), o1 = P3(0, 0, .13), o2 = P3(0, 0, .6);
    el(real, 'line', { x1: o0.x, y1: o0.y, x2: o1.x, y2: o1.y, stroke: '#8a95a1', 'stroke-width': 6, 'stroke-linecap': 'round' });

    // the bar and its two plates, drawn far to near
    var polys = [];
    function quad(p, fill, stroke, bias) {
      polys.push({ p: p, fill: fill, stroke: stroke, d: p.reduce(function (t, q) { return t + q.d; }, 0) / p.length + (bias || 0) });
    }
    var L = 1.05, w = .07, z0 = .13, z1 = .19;
    quad([W(-L, -w, z1), W(L, -w, z1), W(L, w, z1), W(-L, w, z1)], '#e6b872', '#8a5a1c');
    quad([W(-L, -w, z0), W(L, -w, z0), W(L, -w, z1), W(-L, -w, z1)], '#c48d45', '#8a5a1c');
    quad([W(-L, w, z0), W(L, w, z0), W(L, w, z1), W(-L, w, z1)], '#c48d45', '#8a5a1c');
    quad([W(L, -w, z0), W(L, w, z0), W(L, w, z1), W(L, -w, z1)], '#b57d38', '#8a5a1c');
    quad([W(-L, -w, z0), W(-L, w, z0), W(-L, w, z1), W(-L, -w, z1)], '#b57d38', '#8a5a1c');
    // eye plate (with the small round hole) at the back end
    var se = -1.0, he = .55;
    quad([W(se, -.13, z1), W(se, .13, z1), W(se, .13, .8), W(se, -.13, .8)], '#8a6230', '#4a3210', -.01);
    var hole = []; for (a = 0; a < 360; a += 30) hole.push(W(se, Math.sin(a * RAD) * .04, he + Math.cos(a * RAD) * .04));
    quad(hole, '#171007', '#171007', -.02);
    // slit plate with the hair ZZ' at the front end
    var sf = 1.0;
    quad([W(sf, -.15, z1), W(sf, .15, z1), W(sf, .15, .88), W(sf, -.15, .88)], '#8a6230', '#4a3210', -.01);
    quad([W(sf, -.055, .3), W(sf, .055, .3), W(sf, .055, .8), W(sf, -.055, .8)], '#f2f7ff', '#4a3210', -.02);
    polys.sort(function (m, n) { return n.d - m.d; });
    polys.forEach(function (q) { el(real, 'polygon', { points: pts(q.p), fill: q.fill, stroke: q.stroke, 'stroke-width': 1.1, 'stroke-linejoin': 'round' }); });
    var h1 = W(sf, 0, .3), h2 = W(sf, 0, .8);
    el(real, 'line', { x1: h1.x, y1: h1.y, x2: h2.x, y2: h2.y, stroke: '#e03a2e', 'stroke-width': 1.6 });
    // red pointer on the circle, and the line of sight
    var t1 = W(.8, -.05, z1 + .003), t2 = W(.8, .05, z1 + .003), t3 = W(1.0, 0, z1 + .003);
    el(real, 'polygon', { points: pts([t1, t2, t3]), fill: '#d6423a' });
    var e1 = W(se, 0, he), e2 = W(1.45, 0, he);
    el(real, 'line', { x1: e1.x, y1: e1.y, x2: e2.x, y2: e2.y, stroke: '#e8710a', 'stroke-width': 1.5, 'stroke-dasharray': '5 4' });
    // upper part of the axis, on top of the bar
    var a1 = P3(0, 0, z1), a2 = P3(0, 0, .6);
    el(real, 'line', { x1: a1.x, y1: a1.y, x2: a2.x, y2: a2.y, stroke: '#8a95a1', 'stroke-width': 6, 'stroke-linecap': 'round' });
    el(real, 'circle', { cx: a2.x, cy: a2.y, r: 5, fill: '#aeb8c3', stroke: '#5b6672' });
    el(real, 'text', { x: a2.x + 9, y: a2.y - 3, 'font-size': 14, fill: '#132238', class: 'al-it' }, 'x');
    el(real, 'text', { x: o0.x + 8, y: o0.y + 16, 'font-size': 14, fill: '#132238', class: 'al-it' }, 'y');

    if (names.checked) {
      var L1 = [
        ['រន្ធភ្នែក', W(se, 0, he), 14, 40],
        ['បន្ទះឈើ', W(-.35, w, z0 + .03), 14, 90],
        ['អ័ក្សឈរ xy', P3(0, 0, .42), 14, 140],
        ['រង្វង់ចែកមុំ', P3(-Math.sin(CY) * -.9, -Math.cos(CY) * .9, 0), 14, 195]
      ], R1 = [
        ['ខ្សែឆ្មារ ZZ′', W(sf, 0, .7), 386, 40],
        ['ម្ជុលបង្ហាញលេខ', W(.9, 0, z1), 386, 98]
      ];
      L1.forEach(function (l) { label(l, 'start'); });
      R1.forEach(function (l) { label(l, 'end'); });
    }
    function label(l, anchor) {
      el(real, 'line', { x1: l[1].x, y1: l[1].y, x2: l[2] + (anchor === 'start' ? 64 : -64), y2: l[3] - 4, stroke: '#7b8794', 'stroke-width': .8 });
      el(real, 'circle', { cx: l[1].x, cy: l[1].y, r: 2.2, fill: '#132238' });
      el(real, 'text', { x: l[2], y: l[3], 'text-anchor': anchor, 'font-size': 12.5, fill: '#132238', 'font-weight': 600 }, l[0]);
    }
  }

  /* ---------- state -> screen ---------- */
  function draw() {
    var f = Math.round(norm(phi)) % 360;
    $('al-deg').textContent = kh(f) + '°';
    $('al-range').value = norm(phi);
    topBar.setAttribute('transform', 'rotate(' + phi.toFixed(2) + ')');
    topLine.setAttribute('transform', 'rotate(' + phi.toFixed(2) + ')');
    var hit = null;
    ['P', 'Q'].forEach(function (k) {
      var b = tg[k].b, s = Math.sin(b * RAD), c = -Math.cos(b * RAD);
      topTarget[k].setAttribute('transform', 'translate(' + (s * 118).toFixed(1) + ',' + (c * 118).toFixed(1) + ')');
      var on = Math.abs(diff(phi, b)) <= TOL;
      if (on) hit = k;
      topTarget[k].setAttribute('opacity', on ? 1 : .9);
      topTarget[k].querySelector('path').setAttribute('fill', on ? '#1b8a5a' : '#d6423a');
      var r = rec[k];
      topMarks[k].setAttribute('x2', r == null ? 0 : (Math.sin(r * RAD) * 100).toFixed(1));
      topMarks[k].setAttribute('y2', r == null ? 0 : (-Math.cos(r * RAD) * 100).toFixed(1));
    });
    if (rec.P != null && rec.Q != null) {
      var a1 = rec.P, a2 = rec.Q, d = diff(a2, a1), lg = Math.abs(d) > 180 ? 1 : 0, sw = d > 0 ? 1 : 0;
      topSector.setAttribute('d', 'M0 0L' + (Math.sin(a1 * RAD) * 60).toFixed(1) + ' ' + (-Math.cos(a1 * RAD) * 60).toFixed(1) +
        'A60 60 0 ' + lg + ' ' + sw + ' ' + (Math.sin(a2 * RAD) * 60).toFixed(1) + ' ' + (-Math.cos(a2 * RAD) * 60).toFixed(1) + 'Z');
    } else topSector.setAttribute('d', '');
    eyeHair.setAttribute('stroke', hit ? '#1fbf75' : '#e03a2e');
    eyeHair.setAttribute('stroke-width', hit ? 3 : 1.6);
    eyeTag.textContent = hit ? 'ត្រូវនឹង ' + hit + ' ✓' : '';
    var lock = $('al-lock');
    lock.hidden = !hit;
    if (hit) lock.textContent = 'ខ្សែឆ្មារត្រូវនឹង ' + hit + ' ✓';
    drawEye();
    drawReal();
  }

  function turnTo(v) { phi = norm(v); draw(); }
  function table() {
    $('al-aP').textContent = rec.P == null ? '—' : kh(rec.P) + '°';
    $('al-aQ').textContent = rec.Q == null ? '—' : kh(rec.Q) + '°';
    var out = $('al-ang');
    if (rec.P == null || rec.Q == null) { out.textContent = '—'; return; }
    var d = Math.abs(rec.Q - rec.P); if (d > 180) d = 360 - d;
    out.textContent = kh(d) + '°';
  }
  function say(t, cls) { var m = $('al-msg'); m.textContent = t; m.className = 'al-msg' + (cls ? ' ' + cls : ''); }
  function trueAngle() { var d = Math.abs(diff(tg.Q.b, tg.P.b)); return d; }

  function record(k) {
    var off = diff(phi, tg[k].b);
    if (Math.abs(off) > TOL) {
      say('ខ្សែឆ្មារមិនទាន់ត្រូវនឹង ' + k + ' ទេ៖ មើលតាមរន្ធ រួចបង្វិលបន្តិចទៅ' + (off > 0 ? 'ឆ្វេង' : 'ស្ដាំ') + 'ទៀត។', 'bad');
      return;
    }
    rec[k] = Math.round(norm(phi)) % 360;
    table(); draw();
    if (rec.P != null && rec.Q != null) {
      var d = Math.abs(rec.Q - rec.P); if (d > 180) d = 360 - d;
      var e = Math.abs(d - trueAngle());
      say('∠POQ = ' + kh(d) + '° (ចម្លើយពិតនៃដំណាក់នេះ ≈ ' + kh(trueAngle().toFixed(1)) + '°' +
        (e <= 1.6 ? ' — វាស់បានល្អណាស់!' : ' — ព្យាយាមម្ដងទៀតឱ្យត្រូវខ្សែឆ្មារជាងនេះ') + ')។ ចុច «គោលដៅថ្មី» ដើម្បីហាត់ទៀត។', e <= 1.6 ? 'ok' : 'bad');
    } else say('បានកត់ទិស ' + k + ' = ' + kh(rec[k]) + '°។ ឥឡូវបង្វិលទៅ' + (k === 'P' ? ' Q' : ' P') + ' រួចកត់ទិសនោះ។', 'ok');
  }
  $('al-recP').addEventListener('click', function () { record('P'); });
  $('al-recQ').addEventListener('click', function () { record('Q'); });
  $('al-new').addEventListener('click', function () {
    newTargets(); phi = norm(phi); table(); draw();
    say('គោលដៅថ្មីហើយ។ បង្វិលបន្ទះឈើ ឱ្យខ្សែឆ្មារត្រូវនឹង P រួចកត់ទិស។');
  });
  names.addEventListener('change', drawReal);

  /* ---------- turning it by hand ---------- */
  $('al-range').addEventListener('input', function () { turnTo(parseFloat(this.value)); });
  Array.prototype.forEach.call(root.querySelectorAll('.al-turn [data-d]'), function (b) {
    b.addEventListener('click', function () { turnTo(phi + parseFloat(b.getAttribute('data-d'))); });
  });
  function drag(svg, fromPointer) {
    var last = null;
    svg.addEventListener('pointerdown', function (e) {
      if (busy) return;
      last = fromPointer(e, null); root.classList.add('dragging');
      try { svg.setPointerCapture(e.pointerId); } catch (x) { /* ignore */ }
      e.preventDefault();
    });
    svg.addEventListener('pointermove', function (e) {
      if (last == null || busy) return;
      last = fromPointer(e, last);
    });
    function end() { last = null; root.classList.remove('dragging'); }
    svg.addEventListener('pointerup', end); svg.addEventListener('pointercancel', end);
    svg.addEventListener('keydown', function (e) {
      if (busy) return;
      var k = e.key, st = e.shiftKey ? 5 : 1;
      if (k === 'ArrowRight' || k === 'ArrowUp') turnTo(phi + st);
      else if (k === 'ArrowLeft' || k === 'ArrowDown') turnTo(phi - st);
      else return;
      e.preventDefault();
    });
  }
  function svgPoint(svg, e) {
    var r = svg.getBoundingClientRect(), vb = svg.viewBox.baseVal;
    return { x: vb.x + (e.clientX - r.left) / r.width * vb.width, y: vb.y + (e.clientY - r.top) / r.height * vb.height, k: vb.width / r.width };
  }
  drag(top, function (e) {                                  // the bar follows the finger around O
    var p = svgPoint(top, e);
    turnTo(Math.atan2(p.x, -p.y) / RAD);
    return true;
  });
  drag(eye, function (e, last) {                            // dragging the scene turns the head
    var p = svgPoint(eye, e);
    if (last && last !== true) turnTo(phi - (p.x - last.x) / PX);
    return p;
  });
  drag(real, function (e, last) {
    var p = svgPoint(real, e);
    if (last && last !== true) turnTo(phi + (p.x - last.x) * .6);
    return p;
  });

  /* ---------- the guided demo ---------- */
  var steps = Array.prototype.slice.call($('al-steps').children), stopFlag = false;
  function mark(i) { steps.forEach(function (li, j) { li.classList.toggle('on', j === i); }); }
  function fill(k, v) { Array.prototype.forEach.call($('al-steps').querySelectorAll('[data-f="' + k + '"]'), function (n) { n.textContent = v == null ? '—' : kh(v); }); }
  function wait(ms) { return new Promise(function (ok) { setTimeout(ok, ms); }); }
  function sweep(to, ms) {
    return new Promise(function (ok) {
      var from = phi, d = diff(to, from), t0 = performance.now();
      (function f(now) {
        if (stopFlag) return ok();
        var t = Math.min(1, (now - t0) / ms), e = t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
        phi = norm(from + d * e); draw();
        if (t < 1) requestAnimationFrame(f); else ok();
      })(t0);
    });
  }
  async function demo() {
    busy = true; stopFlag = false; root.classList.add('demoing');
    $('al-play').hidden = true; $('al-stop').hidden = false;
    newTargets(); table(); fill('a'); fill('b'); fill('c');
    var P = Math.round(tg.P.b), Q = Math.round(tg.Q.b);
    tg.P.b = P; tg.Q.b = Q;                                 // whole degrees, so the reading is exact
    var d = Math.abs(diff(Q, P));
    mark(0); say('ដាក់អាលីដាតឱ្យអ័ក្សឈរត្រង់ ហើយរង្វង់ចែកមុំដេក។'); draw(); await wait(1600);
    if (!stopFlag) { mark(1); say('មើលតាមរន្ធ ហើយបង្វិលបន្ទះឈើរហូតខ្សែឆ្មារត្រូវនឹង P។'); await sweep(P, 3200); await wait(700); }
    if (!stopFlag) { mark(2); rec.P = P; table(); fill('a', P); draw(); say('ម្ជុលបង្ហាញលេខ ' + kh(P) + '° ត្រង់ P។', 'ok'); await wait(1900); }
    if (!stopFlag) { mark(3); say('បង្វិលបន្តទៅ Q ឱ្យខ្សែឆ្មារត្រូវនឹង Q។'); await sweep(Q, 3600); await wait(700); }
    if (!stopFlag) { rec.Q = Q; table(); fill('b', Q); draw(); say('ម្ជុលបង្ហាញលេខ ' + kh(Q) + '° ត្រង់ Q។', 'ok'); await wait(1900); }
    if (!stopFlag) { mark(4); fill('c', d); say('∠POQ = ' + kh(d) + '° (ផលដកនៃលេខទាំងពីរ)។ ឥឡូវសាកល្បងខ្លួនឯង៖ ចុច «គោលដៅថ្មី» ហើយបង្វិលដោយដៃ។', 'ok'); await wait(600); }
    busy = false; root.classList.remove('demoing');
    $('al-play').hidden = false; $('al-stop').hidden = true; $('al-play').textContent = '▶ មើលគំរូម្ដងទៀត';
    if (stopFlag) { mark(-1); say('បានបញ្ឈប់។ បង្វិលដោយដៃបាន។'); }
  }
  $('al-play').addEventListener('click', demo);
  $('al-stop').addEventListener('click', function () { stopFlag = true; });

  table(); draw();
})();
