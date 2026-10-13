/* khmermath.org — «អាលីដាតសាមញ្ញពីរ៉ាប៉ទ័រ» (construct/alidade-diy.html).
   Part A: how to build it (five steps, the pieces move into place).
   Part B: use it. The protractor turns as a whole (base); the card strip with the straw turns on it (arm).
   Bearings are degrees clockwise from north. The straw looks along  base + side * arm. */
(function () {
  'use strict';
  var bsvg = document.getElementById('d-build');
  if (!bsvg) return;
  var NS = 'http://www.w3.org/2000/svg', RAD = Math.PI / 180, KH = '០១២៣៤៥៦៧៨៩';
  function kh(s) { return String(s).replace(/\d/g, function (d) { return KH[d]; }).replace('.', ','); }
  function norm(a) { return ((a % 360) + 360) % 360; }
  function diff(a, b) { var d = norm(a - b); return d > 180 ? d - 360 : d; }
  function el(parent, tag, attrs, text) {
    var e = document.createElementNS(NS, tag);
    for (var k in attrs) e.setAttribute(k, attrs[k]);
    if (text != null) e.textContent = text;
    if (parent) parent.appendChild(e);
    return e;
  }
  function $(id) { return document.getElementById(id); }
  var root = document.querySelector('.al');

  /* ---------- the pieces, drawn once ---------- */
  function protractor(g, r, side, labels) {
    // a half disc whose 0° is straight up and whose scale runs clockwise (side = 1) or anticlockwise (side = -1)
    var pts = [];
    for (var t = 0; t <= 180; t += 5) pts.push([side * Math.sin(t * RAD) * r, -Math.cos(t * RAD) * r]);
    el(g, 'path', { d: 'M0 ' + (-r) + ' ' + pts.map(function (p) { return 'L' + p[0].toFixed(1) + ' ' + p[1].toFixed(1); }).join(' ') + ' L0 ' + r + 'Z',
      fill: 'rgba(214,232,247,.72)', stroke: '#456a8a', 'stroke-width': 1.6, 'stroke-linejoin': 'round' });
    el(g, 'path', { d: 'M' + (side * 22) + ' 0a22 22 0 0 ' + (side > 0 ? 0 : 1) + ' ' + (-side * 22) + ' -22', fill: 'none', stroke: '#456a8a', 'stroke-width': .8 });
    for (t = 0; t <= 180; t += 2) {
      var big = t % 10 === 0, mid = t % 5 === 0, r1 = r - (big ? 11 : mid ? 7 : 4);
      el(g, 'line', { x1: side * Math.sin(t * RAD) * r1, y1: -Math.cos(t * RAD) * r1, x2: side * Math.sin(t * RAD) * (r - 1), y2: -Math.cos(t * RAD) * (r - 1), stroke: '#2c4a63', 'stroke-width': big ? 1 : .6 });
      if (labels && t % 30 === 0) el(g, 'text', { x: side * Math.sin(t * RAD) * (r - 21), y: -Math.cos(t * RAD) * (r - 21) + 3, 'text-anchor': 'middle', 'font-size': r > 80 ? 9.5 : 8, fill: '#1f3b52' }, kh(t));
    }
    el(g, 'circle', { cx: 0, cy: 0, r: 3, fill: '#fff', stroke: '#2c4a63' });
  }
  function arm(g, len, back) {
    // the card strip along local north, with the straw on it; (0,0) is the pin
    el(g, 'rect', { x: -7, y: -len, width: 14, height: len + back, rx: 2, fill: '#c9a46a', stroke: '#8a6a30', 'stroke-width': 1.2 });
    var s = el(g, 'g', {});
    el(s, 'rect', { x: -3.4, y: -len + 2, width: 6.8, height: len - 14, rx: 3, fill: '#e8f2ff', stroke: '#2f7bbf', 'stroke-width': 1.1 });
    for (var y = -len + 10; y < -16; y += 14) el(s, 'rect', { x: -3.4, y: y, width: 6.8, height: 5, fill: '#e8453c', opacity: .85 });
    el(g, 'rect', { x: -8, y: -len * .72, width: 16, height: 5, fill: 'rgba(255,255,255,.7)', stroke: '#b9b9b9', 'stroke-width': .5 });
    el(g, 'rect', { x: -8, y: -26, width: 16, height: 5, fill: 'rgba(255,255,255,.7)', stroke: '#b9b9b9', 'stroke-width': .5 });
  }
  function pin(g) {
    el(g, 'circle', { cx: 0, cy: 0, r: 5, fill: '#9aa5b1', stroke: '#4c5866', 'stroke-width': 1.5 });
    el(g, 'circle', { cx: -1.4, cy: -1.4, r: 1.6, fill: '#e1e7ee' });
  }

  /* ---------- A. how to build ---------- */
  var B = {};
  var stage = el(bsvg, 'g', {});
  B.board = el(stage, 'rect', { x: 16, y: 8, width: 400, height: 284, rx: 8, fill: '#bd9a62', stroke: '#8a6a30', 'stroke-width': 2 });
  B.boardT = el(stage, 'text', { x: 30, y: 284, 'font-size': 13, fill: '#3a2b10', 'font-weight': 700 }, 'ក្ដារ / សៀវភៅ (ដេកស្មើ)');
  B.prot = el(stage, 'g', {});
  protractor(B.prot, 110, 1, true);
  B.arm = el(stage, 'g', {});
  B.pin = el(stage, 'g', {}); pin(B.pin);
  B.sight = el(stage, 'line', { x1: 0, y1: -155, x2: 0, y2: -250, stroke: '#e8710a', 'stroke-width': 2, 'stroke-dasharray': '6 5' });
  B.lbl = el(stage, 'g', { 'font-size': 14, 'font-weight': 700, fill: '#132238' });
  var BL = {};
  [['prot', 'រ៉ាប៉ទ័រ'], ['strip', 'បន្ទះកាតុង'], ['straw', 'បំពង់ផឹក'], ['pin', 'ម្ជុល'], ['tape', 'ស្កុត']].forEach(function (a) { BL[a[0]] = el(B.lbl, 'text', { x: 0, y: 0, 'text-anchor': 'middle' }, a[1]); });

  var bstep = 0, bt = ['រៀបចំសម្ភារៈ', 'ភ្ជាប់បំពង់នឹងបន្ទះ', 'ធ្វើអ័ក្សបង្វិល', 'ដាក់ឱ្យដេកលើក្ដារ', 'ប្រើ'];
  function setT(node, x, y, rot) {
    node.style.transition = 'transform .9s cubic-bezier(.4,.1,.2,1), opacity .5s';
    node.style.transform = 'translate(' + x + 'px,' + y + 'px) rotate(' + (rot || 0) + 'deg)';
  }
  // the straw is a separate group so it can sit beside the strip in step 1
  (function splitStraw() {
    // rebuild the arm as strip + straw in two groups
    while (B.arm.firstChild) B.arm.removeChild(B.arm.firstChild);
    el(B.arm, 'rect', { x: -7, y: -150, width: 14, height: 162, rx: 2, fill: '#c9a46a', stroke: '#8a6a30', 'stroke-width': 1.2 });
    B.strawG = el(B.arm, 'g', {});
    el(B.strawG, 'rect', { x: -3.4, y: -148, width: 6.8, height: 136, rx: 3, fill: '#e8f2ff', stroke: '#2f7bbf', 'stroke-width': 1.1 });
    for (var y = -140; y < -16; y += 14) el(B.strawG, 'rect', { x: -3.4, y: y, width: 6.8, height: 5, fill: '#e8453c', opacity: .85 });
    B.tape1 = el(B.arm, 'rect', { x: -9, y: -118, width: 18, height: 8, fill: '#f1d46a', opacity: 0 });
    B.tape2 = el(B.arm, 'rect', { x: -9, y: -28, width: 18, height: 8, fill: '#f1d46a', opacity: 0 });
    el(B.arm, 'circle', { cx: 0, cy: 0, r: 3, fill: '#6b5226' });                  // the hole for the pin
  })();
  function show(i) {
    bstep = i;
    var cx = 170, cy = 150;                                                         // the protractor's centre once assembled
    B.board.style.transition = B.boardT.style.transition = 'opacity .5s';
    B.board.style.opacity = B.boardT.style.opacity = i >= 3 ? 1 : 0;
    if (i <= 1) {
      setT(B.prot, 150, 150, 0);
      setT(B.arm, 360, 215, 90);                                                    // the strip lies flat, pointing right
      setT(B.pin, 560, 90, 0);
      B.strawG.style.transition = 'transform .9s'; B.strawG.style.transform = i === 0 ? 'translate(-26px,0)' : 'translate(0,0)';
    } else {
      B.strawG.style.transform = 'translate(0,0)';
      setT(B.prot, cx, cy, 0);
      setT(B.arm, cx, cy, i === 4 ? 52 : 24);
      setT(B.pin, cx, cy, 0);
    }
    var t = i >= 1 ? 1 : 0;
    B.tape1.style.transition = B.tape2.style.transition = 'opacity .5s'; B.tape1.style.opacity = B.tape2.style.opacity = t;
    B.pin.style.opacity = 1;
    B.sight.style.transition = 'opacity .5s'; B.sight.style.opacity = i === 4 ? 1 : 0;
    B.sight.setAttribute('transform', '');
    $('d-bt').textContent = 'ជំហានទី ' + kh(i + 1); $('d-bs').textContent = bt[i];
    Array.prototype.forEach.call($('d-bsteps').children, function (li, j) { li.classList.toggle('on', j === i); });
    $('d-bprev').disabled = i === 0; $('d-bnext').disabled = i === 4;
    // labels follow their pieces
    var L = i <= 1 ? { prot: [150, 280], strip: [440, 250], straw: [440, 168], pin: [560, 118], tape: [-400, -400] }
                   : { prot: [cx + 70, 284], strip: [cx + 150, cy - 70], straw: [cx - 70, 40], pin: [cx - 42, cy + 24], tape: [-400, -400] };
    if (i === 1) { L.straw = [-400, -400]; L.tape = [480, 190]; }
    if (i === 3 || i === 4) { L.tape = [-400, -400]; }
    for (var k in BL) { BL[k].setAttribute('x', L[k][0]); BL[k].setAttribute('y', L[k][1]); }
    B.lbl.style.opacity = i === 4 ? 0 : 1;
    // the arm shown on the board in step 4 aims the sight line; draw it with the same rotation
    if (i === 4) { B.sight.style.transform = 'translate(' + cx + 'px,' + cy + 'px) rotate(52deg)'; } else B.sight.style.transform = 'translate(' + cx + 'px,' + cy + 'px) rotate(24deg)';
  }
  $('d-bprev').addEventListener('click', function () { if (bstep > 0) show(bstep - 1); });
  $('d-bnext').addEventListener('click', function () { if (bstep < 4) show(bstep + 1); });
  Array.prototype.forEach.call($('d-bsteps').children, function (li, j) { li.style.cursor = 'pointer'; li.addEventListener('click', function () { show(j); }); });
  // the first draw must not animate from the corner
  [B.prot, B.arm, B.pin].forEach(function (n) { n.style.transition = 'none'; });
  show(0);

  /* ---------- B. use it ---------- */
  var TOL = 0.8;
  var base = 0, armA = 0, side = 1, st = 1, locked = false;
  var tg = { P: { b: 0, d: 1 }, Q: { b: 60, d: 1 } };
  function newTargets() {
    var p = Math.floor(Math.random() * 360), g = 25 + Math.floor(Math.random() * 126), sgn = Math.random() < .5 ? 1 : -1;
    tg.P = { b: p, d: .85 + Math.random() * .5 };
    tg.Q = { b: norm(p + sgn * g), d: .85 + Math.random() * .5 };
  }
  newTargets();
  function look() { return norm(base + side * armA); }

  var top = $('d-top'), topProtG, topProt, topArm, topLine, tT = {}, topNames;
  function buildTop() {
    if (topProt) top.removeChild(topProt);
    topProt = el(null, 'g', {});
    protractor(topProt, 110, side, true);
    top.insertBefore(topProt, topArm || null);
  }
  (function () {
    el(top, 'circle', { cx: 0, cy: 0, r: 138, fill: '#e3efd0' });
    el(top, 'rect', { x: -138, y: -138, width: 276, height: 276, fill: 'none' });
    ['P', 'Q'].forEach(function (k) {
      var g = el(top, 'g', {});
      el(g, 'line', { x1: 0, y1: 0, x2: 0, y2: -6, stroke: '#6b4a1c', 'stroke-width': 2 });
      el(g, 'path', { d: 'M0 -6l9 3.5-9 3.5z', fill: '#d6423a' });
      el(g, 'text', { x: 0, y: 13, 'text-anchor': 'middle', 'font-size': 13, fill: '#132238', class: 'al-it' }, k);
      tT[k] = g;
    });
    topLine = el(top, 'line', { x1: 0, y1: 0, x2: 0, y2: -138, stroke: '#e8710a', 'stroke-dasharray': '4 4', 'stroke-width': 1.2 });
    topArm = el(top, 'g', {}); arm(topArm, 128, 16);
    var pg = el(top, 'g', {}); pin(pg);
    topNames = el(top, 'g', {});
    buildTop();
  })();

  var eye = $('d-eye'), eyeScene, eyeTag, PXD = 13;
  (function () {
    var defs = el(eye, 'defs', {});
    var cp = el(defs, 'clipPath', { id: 'd-clip' }); el(cp, 'circle', { cx: 210, cy: 140, r: 122 });
    eyeScene = el(eye, 'g', { 'clip-path': 'url(#d-clip)' });
    el(eye, 'circle', { cx: 210, cy: 140, r: 130, fill: 'none', stroke: '#e8f2ff', 'stroke-width': 14 });
    el(eye, 'circle', { cx: 210, cy: 140, r: 137, fill: 'none', stroke: '#2f7bbf', 'stroke-width': 2 });
    el(eye, 'circle', { cx: 210, cy: 140, r: 123, fill: 'none', stroke: '#2f7bbf', 'stroke-width': 1.5 });
    eye._hair = el(eye, 'line', { x1: 210, y1: 18, x2: 210, y2: 262, stroke: '#e03a2e', 'stroke-width': 1.5 });
    eyeTag = el(eye, 'text', { x: 210, y: 276, 'text-anchor': 'middle', 'font-size': 15, fill: '#7fe0a8', 'font-weight': 700 }, '');
  })();
  function drawEye() {
    var phi = look();
    while (eyeScene.firstChild) eyeScene.removeChild(eyeScene.firstChild);
    el(eyeScene, 'rect', { x: 0, y: 0, width: 420, height: 140, fill: '#cfe6f5' });
    el(eyeScene, 'rect', { x: 0, y: 140, width: 420, height: 140, fill: '#b9d889' });
    function ex(b) { return 210 + diff(b, phi) * PXD; }
    for (var i = 0; i < 40; i++) {
      var b = i * 9 + (i * 7 % 4), x = ex(b); if (x < -40 || x > 460) continue;
      var s = .8 + ((i * 5) % 6) / 10;
      el(eyeScene, 'rect', { x: x - 2.5 * s, y: 142, width: 5 * s, height: 20 * s, fill: '#7a5230' });
      el(eyeScene, 'circle', { cx: x, cy: 134, r: 18 * s, fill: '#3f8f4e' });
    }
    for (i = 0; i < 12; i++) {
      x = ex(i * 31 + 5); if (x < -140 || x > 560) continue;
      el(eyeScene, 'path', { d: 'M' + (x - 120) + ' 140Q' + x + ' ' + (140 - (50 + (i % 3) * 14)) + ' ' + (x + 120) + ' 140Z', fill: '#9bbf8a', opacity: .8 });
    }
    ['P', 'Q'].forEach(function (k) {
      var xx = ex(tg[k].b); if (xx < -30 || xx > 450) return;
      var h = 120 / tg[k].d, base0 = 205;
      el(eyeScene, 'line', { x1: xx, y1: base0, x2: xx, y2: base0 - h, stroke: '#5a3b16', 'stroke-width': 5 });
      el(eyeScene, 'path', { d: 'M' + xx + ' ' + (base0 - h) + 'l32 12-32 12z', fill: '#d6423a' });
      el(eyeScene, 'text', { x: xx - 12, y: base0 - h + 8, 'text-anchor': 'middle', 'font-size': 20, fill: '#132238', class: 'al-it' }, k);
    });
  }

  function say(t, cls) { var m = $('d-msg'); m.textContent = t; m.className = 'al-msg' + (cls ? ' ' + cls : ''); }
  function draw() {
    var phi = look(), hit = null;
    $('d-base').value = norm(base); $('d-arm').value = armA;
    $('d-deg').textContent = kh(Math.round(armA)) + '°';
    topProt.setAttribute('transform', 'rotate(' + base.toFixed(2) + ')');
    topArm.setAttribute('transform', 'rotate(' + phi.toFixed(2) + ')');
    topLine.setAttribute('transform', 'rotate(' + phi.toFixed(2) + ')');
    ['P', 'Q'].forEach(function (k) {
      tT[k].setAttribute('transform', 'translate(' + (Math.sin(tg[k].b * RAD) * 125).toFixed(1) + ',' + (-Math.cos(tg[k].b * RAD) * 125).toFixed(1) + ')');
      var on = Math.abs(diff(phi, tg[k].b)) <= TOL; if (on) hit = k;
      tT[k].querySelector('path').setAttribute('fill', on ? '#1b8a5a' : '#d6423a');
    });
    eye._hair.setAttribute('stroke', hit ? '#1fbf75' : '#e03a2e');
    eyeTag.textContent = hit ? 'ត្រូវនឹង ' + hit + ' ✓' : '';
    var lock = $('d-lock'); lock.hidden = !hit; if (hit) lock.textContent = 'បំពង់ត្រូវនឹង ' + hit + ' ✓';
    // names of the parts on the plan
    while (topNames.firstChild) topNames.removeChild(topNames.firstChild);
    if ($('d-names').checked) {
      var a = phi * RAD, ux = Math.sin(a), uy = -Math.cos(a);
      [['បំពង់ផឹក', ux * 100, uy * 100, -130, -112, 'start'], ['បន្ទះកាតុង', -ux * 10 + 0, -uy * 10, 130, -112, 'end'],
       ['រ៉ាប៉ទ័រ', Math.sin((base + side * 100) * RAD) * 88, -Math.cos((base + side * 100) * RAD) * 88, 130, 124, 'end'], ['ម្ជុល', 0, 0, -130, 124, 'start']].forEach(function (l) {
        el(topNames, 'line', { x1: l[1], y1: l[2], x2: l[3] + (l[5] === 'start' ? 44 : -44), y2: l[4] - 4, stroke: '#7b8794', 'stroke-width': .8 });
        el(topNames, 'circle', { cx: l[1], cy: l[2], r: 2, fill: '#132238' });
        el(topNames, 'text', { x: l[3], y: l[4], 'text-anchor': l[5], 'font-size': 11.5, fill: '#132238', 'font-weight': 700 }, l[0]);
      });
    }
    $('d-flip').disabled = locked; $('d-base').disabled = locked;
    drawEye();
  }
  function setBase(v) { if (locked) return; base = norm(v); draw(); }
  function setArm(v) { armA = Math.max(0, Math.min(180, v)); draw(); }
  function stageText() { $('d-stage').textContent = kh(st) + (st === 1 ? ' — ដាក់ ០° ឱ្យត្រូវ P' : ' — វាស់ទៅ Q'); }

  $('d-base').addEventListener('input', function () { setBase(parseFloat(this.value)); });
  $('d-arm').addEventListener('input', function () { setArm(parseFloat(this.value)); });
  Array.prototype.forEach.call(document.querySelectorAll('.al-turn [data-t]'), function (b) {
    b.addEventListener('click', function () {
      var d = parseFloat(b.getAttribute('data-d'));
      if (b.getAttribute('data-t') === 'base') setBase(base + d); else setArm(armA + d);
    });
  });
  $('d-zero').addEventListener('click', function () { setArm(0); });
  $('d-flip').addEventListener('click', function () { side = -side; buildTop(); draw(); say('បានត្រឡប់រ៉ាប៉ទ័រ៖ ឥឡូវលេខកើនទៅម្ខាងទៀត។'); });
  $('d-names').addEventListener('change', draw);

  function reset(newT) {
    if (newT) newTargets();
    st = 1; locked = false; armA = 0; $('d-ok2').disabled = true; $('d-ok1').disabled = false; $('d-ang').textContent = '—';
    stageText(); draw();
    say('ជំហានទី ១៖ ដាក់បន្ទះត្រង់ ០° រួចបង្វិលរ៉ាប៉ទ័រទាំងមូល ឱ្យបំពង់ត្រូវនឹង P។');
  }
  $('d-new').addEventListener('click', function () { reset(true); });
  $('d-reset').addEventListener('click', function () { reset(false); });

  $('d-ok1').addEventListener('click', function () {
    if (armA > .5) { say('ជាមុនសិន បន្ទះត្រូវត្រង់លេខ ០° (ចុច «បន្ទះត្រង់ ០°»)។', 'bad'); return; }
    var off = diff(base, tg.P.b);
    if (Math.abs(off) > TOL) { say('បំពង់មិនទាន់ត្រូវនឹង P ទេ៖ បង្វិលរ៉ាប៉ទ័របន្តិចទៅ' + (off > 0 ? 'ឆ្វេង' : 'ស្ដាំ') + 'ទៀត។', 'bad'); return; }
    var rel = side * diff(tg.Q.b, base);
    if (rel < 0) { say('Q នៅម្ខាងទៀតនៃគែមត្រង់ ដូច្នេះលេខរ៉ាប៉ទ័រមិនទៅដល់ទេ៖ ចុច «ត្រឡប់រ៉ាប៉ទ័រ ⇄» មុនកត់ ហើយរៀបឱ្យត្រូវ P ឡើងវិញ។', 'bad'); return; }
    st = 2; locked = true; $('d-ok1').disabled = true; $('d-ok2').disabled = false; stageText(); draw();
    say('ល្អ! រ៉ាប៉ទ័រត្រូវបានចាក់សោ (កុំរំកិលវា)។ ជំហានទី ២៖ បង្វិលបន្ទះឱ្យបំពង់ត្រូវនឹង Q រួចចុច «អានមុំ POQ»។', 'ok');
  });
  $('d-ok2').addEventListener('click', function () {
    var off = diff(look(), tg.Q.b);
    if (Math.abs(off) > TOL) { say('បំពង់មិនទាន់ត្រូវនឹង Q ទេ៖ បង្វិលបន្ទះបន្តិចទៀត។', 'bad'); return; }
    var got = Math.round(armA), real = Math.abs(diff(tg.Q.b, tg.P.b)), e = Math.abs(got - real);
    $('d-ang').textContent = kh(got) + '°';
    say('∠POQ = ' + kh(got) + '° (ចម្លើយពិត ≈ ' + kh(real.toFixed(1)) + '°' + (e <= 1.6 ? ' — វាស់បានល្អណាស់!' : ' — សាកល្បងម្ដងទៀតឱ្យត្រូវជាងនេះ') + ')។ ចុច «គោលដៅថ្មី» ដើម្បីហាត់ទៀត។', e <= 1.6 ? 'ok' : 'bad');
  });

  // dragging on the plan view: the strip follows the finger near it, the protractor elsewhere
  var drag = null;
  function pt(e) {
    var r = top.getBoundingClientRect(), vb = top.viewBox.baseVal;
    return { x: vb.x + (e.clientX - r.left) / r.width * vb.width, y: vb.y + (e.clientY - r.top) / r.height * vb.height };
  }
  function ang(p) { return Math.atan2(p.x, -p.y) / RAD; }
  top.addEventListener('pointerdown', function (e) {
    var p = pt(e), a = ang(p), r = Math.hypot(p.x, p.y), toStrip = Math.abs(diff(a, look())) * RAD * Math.max(r, 1);
    drag = (toStrip < 22 || locked) ? { k: 'arm' } : { k: 'base', a0: a, b0: base };
    if (locked && r < 8) drag = null;
    if (!drag) return;
    root.classList.add('dragging');
    try { top.setPointerCapture(e.pointerId); } catch (x) { /* ignore */ }
    e.preventDefault();
  });
  top.addEventListener('pointermove', function (e) {
    if (!drag) return;
    var a = ang(pt(e));
    if (drag.k === 'arm') {
      var rel = side * diff(a, base);
      setArm(rel < -90 ? 180 : rel < 0 ? 0 : rel);
    } else setBase(drag.b0 + diff(a, drag.a0));
  });
  function end() { drag = null; root.classList.remove('dragging'); }
  top.addEventListener('pointerup', end); top.addEventListener('pointercancel', end);
  top.addEventListener('keydown', function (e) {
    var s = e.shiftKey ? 5 : 1;
    if (e.key === 'ArrowRight' || e.key === 'ArrowUp') setArm(armA + s);
    else if (e.key === 'ArrowLeft' || e.key === 'ArrowDown') setArm(armA - s);
    else return;
    e.preventDefault();
  });
  // dragging the straw view turns the strip as well
  var lastX = null;
  eye.addEventListener('pointerdown', function (e) { lastX = e.clientX; try { eye.setPointerCapture(e.pointerId); } catch (x) { /* ignore */ } e.preventDefault(); });
  eye.addEventListener('pointermove', function (e) {
    if (lastX == null) return;
    var k = eye.viewBox.baseVal.width / eye.getBoundingClientRect().width, d = (e.clientX - lastX) * k / PXD;
    lastX = e.clientX;
    setArm(armA - side * d);                                           // dragging the picture right turns the straw left
  });
  eye.addEventListener('pointerup', function () { lastX = null; }); eye.addEventListener('pointercancel', function () { lastX = null; });

  reset(false);
})();
