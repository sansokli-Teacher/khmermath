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

  var mode = 'ai', sound = true, holes, score, turn, busy, over, token = 0, skips = 0, handMode = true, release = null, handN = 0, grabbed = null;
  var match = false, dead = [], reserve = [0, 0], round = 1, totals = null, matchOver = false;
  var NODEAD = [];
  var cells = [], arrs = [], ac = null, handEl = null, roundEl = document.getElementById('bk-round'), nextBtn = document.getElementById('bk-nextround'), endBtn = document.getElementById('bk-endmatch');

  function owner(i) { return i < 5 ? 0 : 1; }
  function nameOf(p) { return p === 0 ? 'អ្នកលេងទី ១' : (mode === 'ai' ? 'កុំព្យូទ័រ' : 'អ្នកលេងទី ២'); }

  /* ---- rules: one whole turn, as a list of events ---- */
  function sim(h0, start, dir, dd) {
    dd = dd || NODEAD;
    var h = h0.slice(), ev = [], gain = 0, n = h[start], pos = start, guard = 0;
    /* the next hole that is alive: a dead hole is skipped, as if it were not on the board */
    function nl(q) { var g = 0; do { q = (q + dir + 10) % 10; } while (dd[q] && ++g < 10); return q; }
    h[start] = 0; ev.push({ t: 'take', i: start });
    for (;;) {
      while (n > 0) { pos = nl(pos); h[pos]++; n--; ev.push({ t: 'drop', i: pos }); }
      if (++guard > 200) break;
      var nx = nl(pos);
      if (h[nx] > 0) { n = h[nx]; h[nx] = 0; pos = nx; ev.push({ t: 'take', i: nx }); continue; }
      var nn = nl(nx);
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
        var r = sim(h, m, d, dead), opp = 0;
        legal(r.holes, 0).forEach(function (m2) { [1, -1].forEach(function (d2) { opp = Math.max(opp, sim(r.holes, m2, d2, dead).gain); }); });
        var v = r.gain - opp + Math.random() * 0.5;
        if (v > best) { best = v; pick = [m, d]; }
      });
    });
    return pick;
  }

  /* ---- drawing ---- */
  function build() {
    boardEl.textContent = '';
    cells = []; arrs = [];
    [[9, 8, 7, 6, 5], [0, 1, 2, 3, 4]].forEach(function (row) {
      row.forEach(function (i) {
        var w = document.createElement('div'); w.className = 'bk-cell';
        var b = document.createElement('button');
        b.type = 'button'; b.className = 'bk-hole' + (i === 4 || i === 9 ? ' chi' : '');
        b.innerHTML = '<span class="bk-seeds"></span><span class="bk-n"></span>';
        b.addEventListener('click', function () {
          if (release && pendingI === i) { var r = release; release = null; r(); } else holeTap(i);
        });
        w.appendChild(b);
        arrs[i] = [-1, 1].map(function (side) {
          var a = document.createElement('button');
          a.type = 'button'; a.className = 'bk-arr ' + (side < 0 ? 'l' : 'r');
          a.textContent = side < 0 ? '◀' : '▶';
          a.setAttribute('aria-label', 'ចាក់គ្រាប់ទៅ' + (side < 0 ? 'ឆ្វេង' : 'ស្ដាំ'));
          /* the ring runs 0→9 left to right along the bottom and right to left along the top */
          a.addEventListener('click', function () { choose(i, i < 5 ? side : -side); });
          w.appendChild(a); return a;
        });
        boardEl.appendChild(w); cells[i] = b;
      });
    });
    handEl = document.createElement('div');
    handEl.className = 'bk-hand'; handEl.hidden = true;
    handEl.innerHTML = '<span class="bk-hand-ic" aria-hidden="true">✋</span><b class="bk-hand-n"></b>';
    boardEl.appendChild(handEl);
  }
  var pendingI = -1;
  function handTo(i, n) {
    var br = boardEl.getBoundingClientRect(), cr = cells[i].getBoundingClientRect();
    handEl.hidden = false;
    handEl.style.transform = 'translate(' + (cr.left - br.left + cr.width * 0.5) + 'px,' + (cr.top - br.top + cr.height * 0.45) + 'px)';
    handEl.querySelector('.bk-hand-n').textContent = n > 0 ? km(n) : '';
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
      var mine = !busy && !over && owner(i) === turn && (mode === 'two' || turn === 0);
      var can = mine && n > 0 && !grabbed;
      var held = mine && grabbed && grabbed.i === i;
      c.classList.toggle('dead', !!dead[i]);
      c.classList.toggle('can', can);
      c.disabled = !(c.classList.contains('next') || can || held);
      arrs[i][0].hidden = arrs[i][1].hidden = !held;
      c.setAttribute('aria-label', 'រន្ធ ' + km((i % 5) + 1) + (i === 4 || i === 9 ? ' (ក្បាលឈីមឿង)' : '') + (dead[i] ? ' រន្ធងាប់' : ' មានគ្រាប់ ' + km(n)));
    }
    root.querySelector('[data-score="0"]').textContent = km(score[0]);
    root.querySelector('[data-score="1"]').textContent = km(score[1]);
    root.querySelectorAll('.bk-pl').forEach(function (e) {
      var p = +e.dataset.pl;
      e.classList.toggle('on', !over && p === turn);
      e.querySelector('.bk-name').textContent = nameOf(p);
      var d = 0; for (var q = p * 5; q < p * 5 + 5; q++) if (dead[q]) d++;
      e.querySelector('[data-extra]').textContent = match ? ((d ? 'រន្ធងាប់ ' + km(d) : '') + (d && reserve[p] ? ' · ' : '') + (reserve[p] ? 'ទុក ' + km(reserve[p]) + ' គ្រាប់' : '')) : '';
    });
    roundEl.hidden = !match; roundEl.textContent = 'ជុំទី ' + km(round);
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
  async function run(i, dir, g) {
    var my = token, r = sim(g ? g.base : holes, i, dir, dead), who = turn;
    var manual = handMode && (mode === 'two' || who === 0);
    busy = true; handN = g ? g.n : 0; draw();
    say(nameOf(who) + ' កំពុងចាក់គ្រាប់…');
    for (var k = g ? 1 : 0; k < r.ev.length; k++) {
      var e = r.ev[k], c = cells[e.i];
      handTo(e.i, handN);
      await sleep(STEP * 0.6);
      if (my !== token) return;
      if (e.t === 'take') {
        handN = holes[e.i]; holes[e.i] = 0; tone(300, .12); c.classList.add('hit');
        handTo(e.i, handN);
      } else if (e.t === 'drop') {
        if (manual) {
          say('ចុចរន្ធដែលភ្លឺ ដើម្បីដាក់គ្រាប់ ១ ពីក្នុងដៃ (នៅសល់ ' + km(handN) + ')។');
          pendingI = e.i; c.classList.add('next'); c.disabled = false;
          await new Promise(function (res) { release = res; });
          pendingI = -1; c.classList.remove('next');
          if (my !== token) return;
        }
        holes[e.i]++; handN--; tone(520 + (holes[e.i] % 5) * 40, .1); c.classList.add('hit');
        handTo(e.i, handN);
      } else {
        score[who] += e.n; holes[e.i] = 0; tone(760, .35); c.classList.add('cap'); say(nameOf(who) + ' ចាប់បានគ្រាប់ ' + km(e.n) + '!');
      }
      draw();
      await sleep(e.t === 'cap' ? STEP * 2 : STEP * 0.6);
      if (my !== token) return;
      c.classList.remove('hit', 'cap');
    }
    handEl.hidden = true;
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
    say((pre || '') + (mode === 'ai' && turn === 1 ? 'កុំព្យូទ័រកំពុងគិត…' : 'ដល់វេន' + nameOf(turn) + '។ ចុចរន្ធមួយនៅខាងអ្នក ដើម្បីឱ្យដៃចាប់យកគ្រាប់។'));
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
    var res = nameOf(0) + ' ' + km(a) + ' គ្រាប់ · ' + nameOf(1) + ' ' + km(b) + ' គ្រាប់។ ';
    tone(660, .5);
    if (!match) return say('ល្បែងចប់។ ' + res + (a === b ? 'ស្មើគ្នា!' : nameOf(a > b ? 0 : 1) + ' ឈ្នះ!'));
    totals = [score[0] + reserve[0], score[1] + reserve[1]];
    var lost = totals[0] < 5 ? 0 : totals[1] < 5 ? 1 : -1;   /* fewer seeds than the Kbal Chi Mueng needs */
    if (lost >= 0) {
      matchOver = true;
      return say('ជុំទី ' + km(round) + ' ចប់។ ' + res + nameOf(lost) + ' មានគ្រាប់តិចជាង ៥ មិនអាចបំពេញក្បាលឈីមឿងបាន ដូច្នេះ' + nameOf(1 - lost) + ' ឈ្នះទាំងស្រុង!');
    }
    say('ជុំទី ' + km(round) + ' ចប់។ ' + res + (a === b ? 'ស្មើគ្នា។ ' : nameOf(a > b ? 0 : 1) + ' ឈ្នះជុំនេះ។ ') + 'ចុច «ជុំបន្ទាប់» ដើម្បីបំពេញរន្ធឡើងវិញពីគ្រាប់ដែលមាន។');
    nextBtn.hidden = false; endBtn.hidden = false;
  }
  /* a round starts from what each player holds: the Kbal Chi Mueng first (5), then the holes next to it (4 each);
     a hole that cannot be filled is dead, and what is left over (under 4) is kept for a later round */
  function fill(avail) {
    holes = []; dead = [];
    for (var i = 0; i < 10; i++) { holes[i] = 0; dead[i] = false; }
    [0, 1].forEach(function (p) {
      var order = p === 0 ? [4, 3, 2, 1, 0] : [9, 8, 7, 6, 5], t = avail[p];
      order.forEach(function (idx, k) {
        var need = k === 0 ? 5 : 4;
        if (t >= need) { holes[idx] = need; t -= need; } else dead[idx] = true;
      });
      reserve[p] = t;
    });
  }
  function nextRound() {
    if (!over || matchOver || !totals) return;
    token++; round++; nextBtn.hidden = true; endBtn.hidden = true;
    var first = score[0] === score[1] ? (Math.random() < 0.5 ? 0 : 1) : (score[0] > score[1] ? 0 : 1);   /* the winner of the last round */
    fill(totals); score = [0, 0]; over = false; busy = false; skips = 0; grabbed = null; turn = first;
    next('ជុំទី ' + km(round) + ' ចាប់ផ្ដើម។ ' + nameOf(turn) + ' លេងមុន។ ');
  }
  async function holeTap(i) {
    if (busy || over || owner(i) !== turn || (mode === 'ai' && turn === 1)) return;
    if (grabbed) {                    /* tap the held hole again: put the seeds back */
      if (grabbed.i !== i) return;
      holes[i] = grabbed.n; grabbed = null; handEl.hidden = true; tone(300, .1); draw();
      return say('ដាក់គ្រាប់ត្រឡប់វិញហើយ។ ជ្រើសរន្ធមួយទៀត។');
    }
    if (!holes[i]) return;
    var my = token, n = holes[i], base = holes.slice();
    busy = true; draw();
    handTo(i, 0);
    await sleep(STEP * 0.7);
    if (my !== token) return;
    holes[i] = 0; grabbed = { i: i, n: n, base: base }; busy = false;
    tone(300, .12); handTo(i, n); draw();
    say('ដៃកាន់គ្រាប់ ' + km(n) + ' ហើយ។ ចុចព្រួញ ◀ ឬ ▶ ដើម្បីជ្រើសទិស (ចុចរន្ធម្ដងទៀតដើម្បីដាក់ត្រឡប់វិញ)។');
  }
  function choose(i, dir) {
    if (busy || over || !grabbed || grabbed.i !== i) return;
    var g = grabbed; grabbed = null;
    run(i, dir, g);
  }
  function start() {
    token++;
    round = 1; matchOver = false; totals = null; reserve = [0, 0]; nextBtn.hidden = true; endBtn.hidden = true;
    fill([21, 21]); score = [0, 0]; busy = false; over = false; skips = 0; pendingI = -1; grabbed = null;
    if (release) { var r = release; release = null; r(); }
    if (handEl) handEl.hidden = true;
    cells.forEach(function (c) { c.classList.remove('next', 'hit', 'cap'); });
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
  var hb = root.querySelector('[data-act="hand"]');
  hb.addEventListener('click', function () {
    handMode = !handMode; hb.setAttribute('aria-pressed', handMode); hb.textContent = 'ដាក់គ្រាប់៖ ' + (handMode ? 'ដោយដៃខ្លួនឯង' : 'ស្វ័យប្រវត្តិ');
  });
  nextBtn.addEventListener('click', nextRound);
  endBtn.addEventListener('click', function () {
    if (!over || matchOver || !totals) return;
    matchOver = true; nextBtn.hidden = true; endBtn.hidden = true;
    var a = totals[0], b = totals[1];
    say('ចប់ល្បែងនៅជុំទី ' + km(round) + '។ គ្រាប់សរុប៖ ' + nameOf(0) + ' ' + km(a) + ' · ' + nameOf(1) + ' ' + km(b) + '។ ' + (a === b ? 'ស្មើគ្នា!' : nameOf(a > b ? 0 : 1) + ' ឈ្នះ!'));
  });
  var mb = root.querySelector('[data-act="match"]');
  mb.addEventListener('click', function () {
    match = !match; mb.setAttribute('aria-pressed', match); mb.textContent = 'ច្រើនជុំ៖ ' + (match ? 'បើក' : 'បិទ'); start();
  });
  root.querySelector('[data-act="new"]').addEventListener('click', start);
  var sb = root.querySelector('[data-act="sound"]');
  sb.addEventListener('click', function () {
    sound = !sound; sb.setAttribute('aria-pressed', sound); sb.textContent = 'សំឡេង៖ ' + (sound ? 'បើក' : 'បិទ');
  });
  build(); start();
})();
