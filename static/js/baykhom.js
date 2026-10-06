/* khmermath.org — «ល្បែងបាយខុំ» (play/baykhom.html). Ten holes in a ring; player 0 owns 0-4 (bottom,
   left to right, the Kbal Chi Mueng is 4), player 1 owns 5-9 (top; 9 is the Chi Mueng, drawn on the left).
   Sowing goes 0→9→0, i.e. counter-clockwise on screen. */
(function () {
  'use strict';
  var root = document.getElementById('bk');
  if (!root) return;
  var boardEl = document.getElementById('bk-board'), msgEl = document.getElementById('bk-msg');
  var KM = '០១២៣៤៥៦៧៨៩';
  function km(n) { return String(n).replace(/\d/g, function (d) { return KM[d]; }); }
  function sleep(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var STEP = reduce ? 60 : 340;

  var mode = 'ai', sound = true, holes, score, turn, busy, over, token = 0, picked = -1, skips = 0;
  var cells = [], ac = null, dirEl = document.getElementById('bk-dir');

  function owner(i) { return i < 5 ? 0 : 1; }
  function nameOf(p) { return p === 0 ? 'អ្នកលេងទី ១' : (mode === 'ai' ? 'កុំព្យូទ័រ' : 'អ្នកលេងទី ២'); }

  /* ---- rules: one whole turn, as a list of events ---- */
  function sim(h0, start, dir) {
    var h = h0.slice(), ev = [], gain = 0, n = h[start], pos = start, guard = 0;
    h[start] = 0; ev.push({ t: 'take', i: start });
    for (;;) {
      while (n > 0) { pos = (pos + dir + 10) % 10; h[pos]++; n--; ev.push({ t: 'drop', i: pos }); }
      if (++guard > 200) break;
      var nx = (pos + dir + 10) % 10;
      if (h[nx] > 0) { n = h[nx]; h[nx] = 0; pos = nx; ev.push({ t: 'take', i: nx }); continue; }
      var nn = (nx + dir + 10) % 10;
      if (h[nn] > 0) { gain = h[nn]; h[nn] = 0; ev.push({ t: 'cap', i: nn, n: gain }); }
      break;
    }
    return { ev: ev, holes: h, gain: gain };
  }
  function legal(h, p) { var r = []; for (var i = p * 5; i < p * 5 + 5; i++) if (h[i] > 0) r.push(i); return r; }

  function aiMove(h) {
    var best = -1e9, pick = null;
    legal(h, 1).forEach(function (m) {
      [1, -1].forEach(function (d) {
        var r = sim(h, m, d), opp = 0;
        legal(r.holes, 0).forEach(function (m2) { [1, -1].forEach(function (d2) { opp = Math.max(opp, sim(r.holes, m2, d2).gain); }); });
        var v = r.gain - opp + Math.random() * 0.5;
        if (v > best) { best = v; pick = [m, d]; }
      });
    });
    return pick;
  }

  /* ---- drawing ---- */
  function build() {
    boardEl.textContent = '';
    cells = [];
    [[9, 8, 7, 6, 5], [0, 1, 2, 3, 4]].forEach(function (row) {
      row.forEach(function (i) {
        var b = document.createElement('button');
        b.type = 'button'; b.className = 'bk-hole' + (i === 4 || i === 9 ? ' chi' : '');
        b.innerHTML = '<span class="bk-seeds"></span><span class="bk-n"></span>';
        b.addEventListener('click', function () { choose(i); });
        boardEl.appendChild(b); cells[i] = b;
      });
    });
  }
  function seedHTML(n) {
    var s = '', k = Math.min(n, 16);
    for (var j = 0; j < k; j++) {
      var a = j * 2.39996, r = 38 * Math.sqrt((j + 0.5) / 16);
      s += '<i class="bk-seed" style="left:' + (50 + r * Math.cos(a) - 8.5).toFixed(1) + '%;top:' + (50 + r * Math.sin(a) - 8.5).toFixed(1) + '%"></i>';
    }
    return s;
  }
  function draw() {
    for (var i = 0; i < 10; i++) {
      var c = cells[i], n = holes[i];
      c.querySelector('.bk-seeds').innerHTML = seedHTML(n);
      c.querySelector('.bk-n').textContent = km(n);
      var can = !busy && !over && owner(i) === turn && n > 0 && (mode === 'two' || turn === 0);
      c.classList.toggle('can', can);
      c.classList.toggle('sel', i === picked);
      c.disabled = !can;
      c.setAttribute('aria-label', 'រន្ធ ' + km((i % 5) + 1) + (i === 4 || i === 9 ? ' (ក្បាលឈីមឿង)' : '') + ' មានគ្រាប់ ' + km(n));
    }
    root.querySelector('[data-score="0"]').textContent = km(score[0]);
    root.querySelector('[data-score="1"]').textContent = km(score[1]);
    root.querySelectorAll('.bk-pl').forEach(function (e) {
      var p = +e.dataset.pl;
      e.classList.toggle('on', !over && p === turn);
      e.querySelector('.bk-name').textContent = nameOf(p);
    });
  }
  function say(t) { msgEl.textContent = t; }

  /* ---- sound ---- */
  function tone(f, d) {
    if (!sound) return;
    try {
      ac = ac || new (window.AudioContext || window.webkitAudioContext)();
      var o = ac.createOscillator(), g = ac.createGain();
      o.frequency.value = f; o.type = 'triangle';
      g.gain.setValueAtTime(0.12, ac.currentTime); g.gain.exponentialRampToValueAtTime(0.001, ac.currentTime + d);
      o.connect(g); g.connect(ac.destination); o.start(); o.stop(ac.currentTime + d);
    } catch (e) {}
  }

  /* ---- a turn ---- */
  async function run(i, dir) {
    var my = token, r = sim(holes, i, dir);
    busy = true; picked = -1; dirEl.hidden = true;
    var who = turn;
    say(nameOf(who) + ' កំពុងចាក់គ្រាប់…');
    for (var k = 0; k < r.ev.length; k++) {
      var e = r.ev[k], c = cells[e.i];
      if (e.t === 'take') { holes[e.i] = 0; tone(300, .12); c.classList.add('hit'); }
      else if (e.t === 'drop') { holes[e.i]++; tone(520 + (holes[e.i] % 5) * 40, .1); c.classList.add('hit'); }
      else { score[who] += e.n; holes[e.i] = 0; tone(760, .35); c.classList.add('cap'); say(nameOf(who) + ' ចាប់បានគ្រាប់ ' + km(e.n) + '!'); }
      draw();
      await sleep(e.t === 'cap' ? STEP * 2 : STEP);
      if (my !== token) return;
      c.classList.remove('hit', 'cap');
    }
    holes = r.holes.slice();
    turn = 1 - turn; busy = false;
    if (!legal(holes, turn).length) {
      /* a side with no seeds cannot move: the other player moves again, until seeds arrive */
      if (!legal(holes, 1 - turn).length || ++skips > 15) return finish();
      turn = 1 - turn;
      next('ខាង' + nameOf(1 - turn) + 'គ្មានគ្រាប់ ' + nameOf(turn) + ' ត្រូវលេងម្ដងទៀត។ ');
      return;
    }
    skips = 0;
    next();
  }
  function next(pre) {
    draw();
    say((pre || '') + (mode === 'ai' && turn === 1 ? 'កុំព្យូទ័រកំពុងគិត…' : 'ដល់វេន' + nameOf(turn) + '។ ជ្រើសរន្ធមួយនៅខាងអ្នក ដែលមានគ្រាប់។'));
    if (mode === 'ai' && turn === 1) {
      var my = token; busy = true; draw();
      sleep(reduce ? 100 : 900).then(function () { if (my === token) { busy = false; var m = aiMove(holes); run(m[0], m[1]); } });
    }
  }
  function finish() {
    over = true; busy = false;
    for (var i = 0; i < 10; i++) { score[owner(i)] += holes[i]; holes[i] = 0; }
    draw();
    var a = score[0], b = score[1];
    say('ល្បែងចប់។ ' + nameOf(0) + ' ' + km(a) + ' គ្រាប់ · ' + nameOf(1) + ' ' + km(b) + ' គ្រាប់។ ' +
        (a === b ? 'ស្មើគ្នា!' : nameOf(a > b ? 0 : 1) + ' ឈ្នះ!'));
    tone(660, .5);
  }
  function choose(i) {
    if (busy || over || owner(i) !== turn || !holes[i]) return;
    if (mode === 'ai' && turn === 1) return;
    picked = i; draw();
    dirEl.hidden = false;
    say('ជ្រើសទិសដែលត្រូវចាក់គ្រាប់។');
  }
  function start() {
    token++;
    holes = [4, 4, 4, 4, 5, 4, 4, 4, 4, 5]; score = [0, 0]; busy = false; over = false; picked = -1; skips = 0;
    dirEl.hidden = true;
    turn = Math.random() < 0.5 ? 0 : 1;   /* the draw: who plays first */
    next('ចាប់ឆ្នោតបាន ' + nameOf(turn) + ' លេងមុន។ ');
  }

  root.querySelectorAll('[data-mode]').forEach(function (b) {
    b.addEventListener('click', function () {
      mode = b.dataset.mode;
      root.querySelectorAll('[data-mode]').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      start();
    });
  });
  dirEl.querySelectorAll('[data-dir]').forEach(function (b) {
    b.addEventListener('click', function () { if (picked >= 0 && !busy) run(picked, +b.dataset.dir); });
  });
  root.querySelector('[data-act="new"]').addEventListener('click', start);
  var sb = root.querySelector('[data-act="sound"]');
  sb.addEventListener('click', function () {
    sound = !sound; sb.setAttribute('aria-pressed', sound); sb.textContent = 'សំឡេង៖ ' + (sound ? 'បើក' : 'បិទ');
  });
  build(); start();
})();
