/* khmermath.org — «ហ្គេមក្រុម» (play/teamgame.html): a classroom team game.
   The board is a grid of picture cards (names hidden). A team picks a card, it pops up with fireworks and shows its name,
   an optional question and answer. Some cards hide a special power-up. Everything stays in this browser. */
(function () {
  'use strict';
  var $ = function (id) { return document.getElementById(id); };
  if (!$('tg')) return;
  var GAME = 'km_tg_game_v2', SETS = 'km_tg_sets_v2', CFG = 'km_tg_cfg_v2';
  var COLORS = ['#e8590c', '#1c7ed6', '#2f9e44', '#ae3ec9', '#f08c00', '#0c8599', '#d6336c', '#5f3dc4'];
  var FACES = [['#ff6b81', '#e8456b'], ['#2fd4a0', '#2fa66b'], ['#ffb347', '#ff8a3d'], ['#4dabf7', '#1c7ed6'], ['#b57cf5', '#8a4fe0'], ['#ff7eb3', '#e0518c']];
  var SPECIALS = {
    bomb:  { icon: '💣', name: 'គ្រាប់បែក!', desc: 'ក្រុមដែលជ្រើសបាត់ពិន្ទុទាំងអស់ (ត្រឡប់ទៅ ០)។' },
    double:{ icon: '✖២', name: 'ពិន្ទុទ្វេដង!', desc: 'ពិន្ទុរបស់ក្រុមនេះកើនឡើងទ្វេដង។' },
    swap:  { icon: '🔄', name: 'ប្តូរពិន្ទុ!', desc: 'ជ្រើសក្រុមមួយ ដើម្បីប្តូរពិន្ទុជាមួយ។' },
    gift:  { icon: '🎁', name: 'អំណោយ!', desc: 'ទទួលបានពិន្ទុបន្ថែមទ្វេដងនៃពិន្ទុកាត។' },
    steal: { icon: '🕵', name: 'លួចពិន្ទុ!', desc: 'ជ្រើសក្រុមមួយ ដើម្បីលួចយកពិន្ទុរបស់គេ។' },
    skip:  { icon: '⏭', name: 'បាត់វេន!', desc: 'ក្រុមនេះបាត់វេន គ្មានពិន្ទុ។' }
  };

  var BOAT_SP = {                                    // special boxes during the boat race
    bomb: { icon: '🪨', name: 'ជាប់ថ្ម!', desc: 'ទូកត្រឡប់ក្រោយ ២ ជំហាន។' },
    double: { icon: '🚀', name: 'បោះអុំលឿន!', desc: 'ទូកទៅមុខបន្ថែម ២ ជំហាន។' },
    gift: { icon: '🎁', name: 'ខ្យល់អំណោយ!', desc: 'ទូកទៅមុខបន្ថែម ២ ជំហាន។' }
  };

  /* ---------- ready-made card sets ---------- */
  function svg(inner) { return 'data:image/svg+xml;utf8,' + encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect x="4" y="4" width="92" height="92" rx="18" fill="#fff"/>' + inner + '</svg>'); }
  var S1 = 'stroke="#1b2733" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"';
  var PICS = {
    bisector: svg('<path d="M18 76H86M18 76L78 26" ' + S1 + '/><path d="M18 76L86 49" stroke="#e8590c" stroke-width="3.5" stroke-dasharray="6 5" fill="none"/><path d="M40 76A22 22 0 0 1 38.5 69M36.5 67A22 22 0 0 1 35 60" stroke="#1c7ed6" stroke-width="3" fill="none"/>'),
    triangle: svg('<path d="M50 20L84 78H16Z" ' + S1 + '/><circle cx="50" cy="20" r="3.5" fill="#e8590c"/><circle cx="84" cy="78" r="3.5" fill="#e8590c"/><circle cx="16" cy="78" r="3.5" fill="#e8590c"/>'),
    circle: svg('<circle cx="50" cy="50" r="31" ' + S1 + '/><path d="M50 50L76 34" stroke="#e8590c" stroke-width="3.5" fill="none"/><circle cx="50" cy="50" r="3.5" fill="#1b2733"/>'),
    parallel: svg('<path d="M14 34H86M14 66H86" ' + S1 + '/><path d="M30 84L70 16" stroke="#e8590c" stroke-width="3.5" fill="none"/>'),
    pyth: svg('<path d="M24 74V30H72Z" ' + S1 + '/><path d="M24 74H34V64H24" stroke="#1c7ed6" stroke-width="2.5" fill="none"/><text x="14" y="56" font-size="14" font-family="sans-serif" fill="#e8590c">a</text><text x="44" y="86" font-size="14" font-family="sans-serif" fill="#e8590c">b</text><text x="52" y="46" font-size="14" font-family="sans-serif" fill="#e8590c">c</text>'),
    bars: svg('<path d="M18 80H84" ' + S1 + '/><rect x="24" y="52" width="12" height="28" fill="#4dabf7"/><rect x="44" y="30" width="12" height="50" fill="#ff6b81"/><rect x="64" y="42" width="12" height="38" fill="#2fd4a0"/>'),
    line: svg('<path d="M12 56H88M82 50L88 56L82 62" ' + S1 + '/><path d="M26 50V62M44 50V62M62 50V62" ' + S1 + '/><circle cx="44" cy="56" r="4.5" fill="#e8590c"/><text x="20" y="42" font-size="13" font-family="sans-serif" fill="#1b2733">-1</text><text x="41" y="42" font-size="13" font-family="sans-serif" fill="#1b2733">0</text><text x="60" y="42" font-size="13" font-family="sans-serif" fill="#1b2733">1</text>')
  };
  var PACKS = {
    math: ['គណិតវិទ្យា', [
      { n: 'ចំនួនគត់', img: PICS.line, q: 'ចំនួនគត់មានអ្វីខ្លះ?', a: '… −២, −១, ០, ១, ២ …' },
      { n: '√២', img: '√២', q: 'តម្លៃប្រហែលនៃ √២?', a: '១,៤១៤…' },
      { n: 'កន្លះបន្ទាត់ពុះមុំ', img: PICS.bisector, q: 'កន្លះបន្ទាត់ពុះមុំជាអ្វី?', a: 'កន្លះបន្ទាត់ចែកមុំជាពីរស្មើគ្នា' },
      { n: 'ត្រីកោណ', img: PICS.triangle, q: 'ផលបូកមុំក្នុងត្រីកោណ?', a: '១៨០°' },
      { n: 'រង្វង់', img: PICS.circle, q: 'រូបមន្តបរិមាត្ររង្វង់?', a: 'C = ២πr' },
      { n: 'បន្ទាត់ស្របគ្នា', img: PICS.parallel, q: 'បន្ទាត់ពីរស្របគ្នាមានលក្ខណៈអ្វី?', a: 'មិនកាត់គ្នាទេ' },
      { n: 'ទ្រឹស្តីបទពីតាហ្គោរ', img: PICS.pyth, q: 'ចូរសរសេរទ្រឹស្តីបទ', a: 'a² + b² = c²' },
      { n: 'ស្ថិតិ', img: PICS.bars, q: 'មធ្យមភាគនៃ ២, ៤, ៦?', a: '៤' },
      { n: 'ប្រភាគ', img: '½', q: '១/២ + ១/៤ = ?', a: '៣/៤' },
      { n: 'ភាគរយ', img: '%', q: '១០% នៃ ២០០ = ?', a: '២០' },
      { n: 'ស្វ័យគុណ', img: '២³', q: '២³ = ?', a: '៨' },
      { n: 'សមីការ', img: 'x+២=៥', q: 'ដោះស្រាយ x + ២ = ៥', a: 'x = ៣' }
    ]],
    fruit: ['ផ្លែឈើខ្មែរ', [['ស្វាយ', '🥭'], ['ចេក', '🍌'], ['ដូង', '🥥'], ['ក្រូច', '🍊'], ['ម្នាស់', '🍍'], ['ឪឡឹក', '🍉'], ['ទំពាំងបាយជូរ', '🍇'], ['ស្ត្របឺរី', '🍓'], ['ប៉ោម', '🍎'], ['ក្រូចឆ្មារ', '🍋'], ['ត្រឡាច', '🍈'], ['ផ្លែប៉េស', '🍑']].map(function (x) { return { n: x[0], img: x[1] }; })],
    animal: ['សត្វ', [['ឆ្កែ', '🐶'], ['ឆ្មា', '🐱'], ['ដំរី', '🐘'], ['ត្រី', '🐟'], ['ក្របី', '🐃'], ['គោ', '🐄'], ['មាន់', '🐔'], ['ទា', '🦆'], ['ជ្រូក', '🐖'], ['ខ្លា', '🐯'], ['ស្វា', '🐒'], ['សេះ', '🐴'], ['កង្កែប', '🐸'], ['ក្រពើ', '🐊']].map(function (x) { return { n: x[0], img: x[1] }; })],
    number: ['លេខ', Array.apply(null, Array(12)).map(function (_, i) { var k = String(i + 1).replace(/\d/g, function (d) { return '០១២៣៤៥៦៧៨៩'[d]; }); return { n: k, img: k }; })]
  };

  var G = null, hist = [], cards = [], audio = null, timerId = 0, openTileIdx = -1, pendingFile = -1;
  var BANK = null, mode = 'lesson', selLessons = [1], curClass = 7;   // curClass: 7, 8 or 9 (lessons are numbered 1.., 101.., 201..)                                  // lesson question bank (static/data/teamgame_g7.json)
  var lastScores = null, lastTurn = -1, lastDone = -1, boardIn = false, flipping = false, flipBtn = null;   // animation bookkeeping

  /* ---------- helpers ---------- */
  function khNum(n) { return String(n).replace(/\d/g, function (d) { return '០១២៣៤៥៦៧៨៩'[d]; }); }
  function enNum(s) { return String(s).replace(/[០-៩]/g, function (d) { return '០១២៣៤៥៦៧៨៩'.indexOf(d); }); }
  function shuffle(a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  function load(k, d) { try { var v = JSON.parse(localStorage.getItem(k)); return v === null ? d : v; } catch (e) { return d; } }
  function put(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); return true; } catch (e) { return false; } }
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text !== undefined) e.textContent = text; return e; }
  function clean(s) { return String(s || '').replace(/ /g, ' ').replace(/\s+/g, ' ').trim(); }
  function reduceMotion() { return window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches; }
  function tweenNum(node, from, to) {                // count a score up/down instead of jumping
    if (reduceMotion() || from === to) { node.textContent = khNum(to); return; }
    var t0 = performance.now(), d = 650;
    (function step(now) { var k = Math.min(1, (now - t0) / d), e = 1 - Math.pow(1 - k, 3); node.textContent = khNum(Math.round(from + (to - from) * e)); if (k < 1 && node.isConnected) requestAnimationFrame(step); else node.textContent = khNum(to); })(t0);
  }
  function typeset(node) {                          // KaTeX: maths is set in italic with Latin digits
    var go = function () { if (window.renderMathInElement) try { renderMathInElement(node, { delimiters: [{ left: '\\(', right: '\\)', display: false }], throwOnError: false }); } catch (e) {} };
    if (window.renderMathInElement) go(); else window.addEventListener('load', go);
  }
  function sndOn() { return $('tg-sound').checked && !(G && G.mute); }
  function isPic(s) { return /^(data:image|https?:)/.test(s || ''); }
  function picNode(img, cls) {                       // a picture: uploaded/drawn image, or text/emoji shown big
    var box = el('span', 'tg-pic ' + (cls || ''));
    if (isPic(img)) { var i = el('img'); i.src = img; i.alt = ''; i.draggable = false; box.appendChild(i); }
    else box.textContent = img || '';
    if (!isPic(img) && String(img || '').length > 3) box.classList.add('long');
    return box;
  }

  /* ---------- sound ---------- */
  // Background music + effects: the same original quiz-show tracks as the live quiz (sfx.js, made for this site).
  function bgm(name, v) { try { if (!window.KmSound) return; if (sndOn()) KmSound.loop(name, v); else KmSound.stop(); } catch (e) {} }
  function kmfx(name) { try { if (window.KmSound && sndOn()) { KmSound.sfx(name); return true; } } catch (e) {} return false; }
  function tone(freqs, vol, len, type) {
    if (!sndOn()) return;
    try {
      audio = audio || new (window.AudioContext || window.webkitAudioContext)();
      freqs.forEach(function (f, i) {
        var o = audio.createOscillator(), g = audio.createGain(), t = audio.currentTime + i * 0.13;
        o.type = type || 'sine'; o.frequency.value = f; g.gain.setValueAtTime(vol, t); g.gain.exponentialRampToValueAtTime(0.001, t + len);
        o.connect(g); g.connect(audio.destination); o.start(t); o.stop(t + len + 0.02);
      });
    } catch (e) {}
  }
  var sfx = {
    flip: function () { tone([523, 784, 1047], 0.07, 0.16); },
    right: function () { if (!kmfx('correct')) tone([660, 880, 1100], 0.08, 0.2); },
    wrong: function () { if (!kmfx('wrong')) tone([200, 150], 0.09, 0.28, 'square'); },
    bomb: function () { tone([120, 90, 60], 0.14, 0.35, 'sawtooth'); },
    special: function () { tone([523, 784, 659, 988], 0.07, 0.18); },
    tick: function () { tone([900], 0.05, 0.05); },
    end: function () { if (!kmfx('timeup')) tone([880, 880, 880], 0.1, 0.12, 'square'); },
    win: function () { try { if (window.KmSound) KmSound.stop(); } catch (e) {} if (!kmfx('fanfare')) tone([523, 659, 784, 1047, 1319], 0.08, 0.3); }
  };

  /* ---------- fireworks ---------- */
  var fwParts = [], fwEnd = 0, fwOn = false, fwNext = 0, fwRandom = false, fwDim = null, fwHues = [8, 40, 52, 130, 190, 280, 330];
  function fwBurst(x, y, n) {
    var hue = fwHues[Math.floor(Math.random() * fwHues.length)];
    for (var i = 0; i < n; i++) { var a = Math.PI * 2 * i / n + Math.random() * 0.2, v = 2.2 + Math.random() * 3.6; fwParts.push({ x: x, y: y, vx: Math.cos(a) * v, vy: Math.sin(a) * v, life: 1, hue: hue + Math.random() * 25 - 12 }); }
  }
  function fwFrame(now) {
    if (!fwOn) return;
    var g = fwDim.g, W = fwDim.W, H = fwDim.H;
    g.globalCompositeOperation = 'destination-out'; g.fillStyle = 'rgba(0,0,0,.22)'; g.fillRect(0, 0, W, H); g.globalCompositeOperation = 'lighter';
    if (fwRandom && now < fwEnd && now > fwNext) { fwBurst(W * (Math.random() < 0.5 ? 0.04 + Math.random() * 0.2 : 0.76 + Math.random() * 0.2), H * (0.1 + Math.random() * 0.55), 46); fwNext = now + 220 + Math.random() * 220; }
    fwParts = fwParts.filter(function (p) { return p.life > 0.02; });
    fwParts.forEach(function (p) { p.x += p.vx; p.y += p.vy; p.vy += 0.06; p.vx *= 0.985; p.vy *= 0.985; p.life -= 0.013; g.fillStyle = 'hsla(' + p.hue + ',100%,60%,' + Math.max(0, p.life) + ')'; g.beginPath(); g.arc(p.x, p.y, 2.6, 0, 7); g.fill(); });
    if (now < fwEnd || fwParts.length) requestAnimationFrame(fwFrame); else { fwOn = false; fwRandom = false; g.clearRect(0, 0, W, H); }
  }
  function fwStart() {
    if (fwOn) return;
    var cv = $('tg-fw'), dpr = Math.min(2, window.devicePixelRatio || 1), W = cv.clientWidth, H = cv.clientHeight;
    cv.width = W * dpr; cv.height = H * dpr; var g = cv.getContext('2d'); g.setTransform(dpr, 0, 0, dpr, 0, 0);
    fwDim = { g: g, W: W, H: H }; fwOn = true; fwParts = []; requestAnimationFrame(fwFrame);
  }
  function fireworks(ms) { if (reduceMotion()) return; fwStart(); fwRandom = true; fwNext = 0; fwEnd = performance.now() + (ms || 3200); }
  function miniBurst(x, y) { if (reduceMotion()) return; fwStart(); fwBurst(x, y, 30); fwEnd = Math.max(fwEnd, performance.now() + 800); }
  function stopFw() { fwOn = false; fwRandom = false; fwParts = []; var cv = $('tg-fw'); cv.getContext('2d').clearRect(0, 0, cv.width, cv.height); }

  /* ---------- no-team mode: the teacher calls a student to pick a number, the whole class is one "team" ---------- */
  function noTeam() { var c = $('tg-noteam'); return !!(c && c.checked); }
  function setQn(v) { var sel = $('tg-qn'); v = String(v); if (![].some.call(sel.options, function (o) { return o.value === v; })) { var o = document.createElement('option'); o.value = v; o.textContent = khNum(v) + ' សំណួរ'; sel.insertBefore(o, sel.options[sel.options.length - 1]); } sel.value = v; }
  /* ---------- setup: teams ---------- */
  var teamNames = [], teamMembers = [];
  function renderTeamSetup() {
    var n = noTeam() ? 0 : Math.max(2, Math.min(8, parseInt($('tg-nteams').value, 10) || 2)), box = $('tg-teamlist'); box.innerHTML = '';
    for (var i = 0; i < n; i++) {
      (function (i) {
        var row = el('div', 'tg-team'), dot = el('span', 'dot'), inp = el('input'), mem = el('small', 'mem');
        dot.style.background = COLORS[i % COLORS.length]; inp.type = 'text'; inp.maxLength = 30; inp.value = teamNames[i] || ('ក្រុមទី ' + khNum(i + 1)); inp.setAttribute('aria-label', 'ឈ្មោះក្រុមទី ' + (i + 1));
        inp.addEventListener('input', function () { teamNames[i] = inp.value; saveCfg(); });
        mem.textContent = (teamMembers[i] && teamMembers[i].length) ? teamMembers[i].length + ' នាក់៖ ' + teamMembers[i].join(', ') : '';
        row.appendChild(dot); row.appendChild(inp); row.appendChild(mem); box.appendChild(row);
      })(i);
    }
  }
  function checkImport() {
    var g = load('km_wheel_last_groups', null);
    if (g && g.groups && g.groups.length) { $('tg-import').hidden = false; $('tg-importhint').hidden = false; $('tg-importhint').textContent = 'មានលទ្ធផលបែងចែកក្រុមចុងក្រោយពីកង់ចាប់ឈ្មោះ៖ ' + (g.cls || '') + ' (' + khNum(g.groups.length) + ' ក្រុម)។'; }
  }

  /* ---------- setup: cards ---------- */
  function resize(file, cb) {                         // shrink an uploaded picture so it fits in localStorage
    var fr = new FileReader();
    fr.onload = function () {
      var im = new Image();
      im.onload = function () {
        var m = 260, k = Math.min(1, m / Math.max(im.width, im.height)), c = document.createElement('canvas'); c.width = Math.round(im.width * k); c.height = Math.round(im.height * k);
        c.getContext('2d').drawImage(im, 0, 0, c.width, c.height); cb(c.toDataURL(/png|gif|svg/.test(file.type) ? 'image/png' : 'image/jpeg', 0.82));
      };
      im.onerror = function () { cb(null); }; im.src = fr.result;
    };
    fr.readAsDataURL(file);
  }
  function renderCards() {
    var box = $('tg-cards'); box.innerHTML = '';
    cards.forEach(function (c, i) {
      var row = el('div', 'tg-crow'), thumb = el('div', 'tg-cthumb'), f1 = el('div', 'tg-cf'), f2 = el('div', 'tg-cf'), f3 = el('div', 'tg-cf tg-cf-wide');
      function refreshThumb() { thumb.innerHTML = ''; thumb.style.background = 'linear-gradient(160deg,' + FACES[i % FACES.length][0] + ',' + FACES[i % FACES.length][1] + ')'; thumb.appendChild(picNode(c.img, 'sm')); }
      refreshThumb();
      function field(parent, label, key, ph, cls) {
        var l = el('label', '', label), inp = el('input'); inp.type = 'text'; inp.value = c[key] || ''; inp.placeholder = ph || ''; if (cls) inp.className = cls;
        inp.addEventListener('input', function () { c[key] = inp.value; if (key === 'img') refreshThumb(); saveCfg(); }); l.appendChild(inp); parent.appendChild(l); return inp;
      }
      field(f1, 'ឈ្មោះកាត', 'n', 'ឧ. ចំនួនគត់');
      var imgIn = field(f2, 'រូបភាព (emoji ឬអក្សរ)', 'img', 'ឧ. 🥭 ឬ √២');
      var has = isPic(c.img);
      if (has) { imgIn.readOnly = true; imgIn.value = '🖼 បានផ្ទុករូបភាពរួចហើយ'; }
      var up = el('button', 'btn btn-ghost btn-sm', has ? '⬆ ប្តូររូបភាព' : '⬆ ផ្ទុកឡើងរូបថត'); up.type = 'button'; up.addEventListener('click', function () { pendingFile = i; $('tg-file').click(); }); f2.appendChild(up);
      if (has) { var clr = el('button', 'btn btn-ghost btn-sm', '✕ លុបរូបភាព'); clr.type = 'button'; clr.addEventListener('click', function () { c.img = ''; renderCards(); saveCfg(); }); f2.appendChild(clr); }
      field(f3, 'សំណួរ (ជម្រើស)', 'q', 'សំណួរដែលនឹងបង្ហាញ'); field(f3, 'ចម្លើយ (ជម្រើស)', 'a', 'ចម្លើយ'); field(f3, 'ពិន្ទុ (ជម្រើស)', 'p', 'លំនាំដើម').type = 'number';
      var del = el('button', 'tg-cdel', '✕'); del.type = 'button'; del.setAttribute('aria-label', 'លុបកាត'); del.addEventListener('click', function () { cards.splice(i, 1); renderCards(); saveCfg(); });
      row.appendChild(thumb); row.appendChild(f1); row.appendChild(f2); row.appendChild(f3); row.appendChild(del); box.appendChild(row);
      imgIn.addEventListener('input', function () { /* thumb refreshed in field() */ });
    });
    var n = cards.filter(function (c) { return clean(c.n); }).length;
    $('tg-qcount').textContent = n ? khNum(n) + ' កាត' : 'មិនទាន់មានកាត';
  }
  function parsePaste(text) {
    return text.split(/\r?\n/).map(function (line) {
      var parts = (line.indexOf('|') >= 0 ? line.split('|') : line.split('\t')).map(clean); if (!parts[0]) return null;
      var p = parts[4] ? parseInt(enNum(parts[4]), 10) : 0;
      return { n: parts[0], img: parts[1] || '', q: parts[2] || '', a: parts[3] || '', p: p > 0 ? p : '' };
    }).filter(Boolean);
  }
  function useCards(list) { cards = list.map(function (c) { return { n: c.n || '', img: c.img || '', q: c.q || '', a: c.a || '', p: c.p || '' }; }); renderCards(); saveCfg(); }
  function renderPacks() {
    var box = $('tg-packs'); box.innerHTML = ''; box.appendChild(el('small', 'tg-hint', 'ចាប់ផ្ដើមពីកាតគំរូ៖'));
    Object.keys(PACKS).forEach(function (k) {
      var b = el('button', 'btn btn-ghost btn-sm', PACKS[k][0]); b.type = 'button';
      b.addEventListener('click', function () { if (cards.some(function (c) { return clean(c.n); }) && !confirm('ជំនួសកាតបច្ចុប្បន្នដោយកាតគំរូ «' + PACKS[k][0] + '»?')) return; useCards(PACKS[k][1]); });
      box.appendChild(b);
    });
  }
  function renderSets() {
    var sel = $('tg-sets'), sets = load(SETS, []); sel.innerHTML = '<option value="">— សំណុំកាតដែលបានរក្សាទុក —</option>';
    sets.forEach(function (s, i) { var o = el('option', '', s.name + ' (' + s.cards.length + ')'); o.value = i; sel.appendChild(o); });
  }
  function saveCfg() {
    var ok = put(CFG, { nt: noTeam(), n: $('tg-nteams').value, names: teamNames, members: teamMembers, cards: cards, mode: mode, lessons: selLessons, qn: $('tg-qn').value, pts: $('tg-pts').value, style: $('tg-style').value, finish: $('tg-finish').value, timer: $('tg-timer').value, face: $('tg-face').value, sp: $('tg-special').checked, nsp: $('tg-nspecial').value, snd: $('tg-sound').checked });
    if (!ok) $('tg-qcount').textContent += ' (ទំហំផ្ទុកពេញ — សូមកាត់បន្ថយរូបថត)';
  }
  function loadCfg() {
    var c = load(CFG, null); if (!c) { useCards(PACKS.math[1]); return; }
    mode = c.mode || 'lesson'; selLessons = c.lessons || [1]; if (c.qn) setQn(c.qn); if ($('tg-noteam')) $('tg-noteam').checked = !!c.nt; $('tg-nteams').value = c.n || 4; teamNames = c.names || []; teamMembers = c.members || []; cards = (c.cards || []).slice();
    $('tg-pts').value = c.pts || 10; $('tg-style').value = c.style || 'cards'; $('tg-finish').value = c.finish || 8; $('tg-timer').value = c.timer || '0'; $('tg-face').value = c.face || 'img'; $('tg-special').checked = c.sp !== false; $('tg-nspecial').value = c.nsp === undefined ? 3 : c.nsp; $('tg-sound').checked = c.snd !== false;
    if (!cards.length) cards = PACKS.math[1].slice();
  }

  /* ---------- game ---------- */
  function startGame() {
    var n = noTeam() ? 1 : Math.max(2, Math.min(8, parseInt($('tg-nteams').value, 10) || 2)), pts = Math.max(1, parseInt($('tg-pts').value, 10) || 10), tiles, face = $('tg-face').value;
    if (mode === 'lesson') {
      var pool = [];
      ((BANK && BANK.lessons) || []).forEach(function (L) { if (selLessons.indexOf(L.n) >= 0) pool = pool.concat(L.qs.map(function (q) { return { n: lessonName(L) + ' · ' + q.t, q: q.q, o: q.o || null, ck: q.k, f: q.f || '', a: q.a, s: q.s || '', h: q.h || '' }; })); });
      if (!pool.length) { $('tg-lessonhint').textContent = 'សូមជ្រើសមេរៀនយ៉ាងហោចណាស់ ១ ជាមុនសិន។'; return; }
      var want = parseInt($('tg-qn').value, 10) || pool.length; pool = shuffle(pool).slice(0, want); face = 'num';
      tiles = pool.map(function (c) { return { k: 'q', n: c.n, img: '', q: c.q, o: c.o, ck: c.ck, f: c.f, a: c.a, s: c.s, h: c.h, p: pts, lq: 1 }; });
    } else {
      var list = cards.filter(function (c) { return clean(c.n); });
      if (!list.length) { $('tg-qcount').textContent = 'សូមបន្ថែមកាតយ៉ាងហោចណាស់ ១ ជាមុនសិន។'; return; }
      tiles = list.map(function (c) { return { k: 'q', n: clean(c.n), img: c.img || '', q: clean(c.q), a: clean(c.a), p: parseInt(c.p, 10) > 0 ? parseInt(c.p, 10) : pts }; });
    }
    if ($('tg-special').checked && !noTeam()) {            // swap / steal / bomb need other teams, so no special cards without teams
      var keys = Object.keys(SPECIALS), cnt = Math.max(0, Math.min(12, parseInt($('tg-nspecial').value, 10) || 0)), deck = [];
      while (deck.length < cnt) deck = deck.concat(shuffle(keys));
      deck.slice(0, cnt).forEach(function (sp) { var src = tiles[Math.floor(Math.random() * tiles.length)]; tiles.push({ k: 's', sp: sp, img: src.img }); });   // a special card wears an ordinary picture
    }
    G = { style: noTeam() ? 'cards' : $('tg-style').value, finish: Math.max(3, Math.min(30, parseInt($('tg-finish').value, 10) || 8)), teams: [], tiles: shuffle(tiles), turn: 0, pts: pts, timer: parseInt($('tg-timer').value, 10) || 0, face: face, mute: false, finished: false };
    for (var i = 0; i < n; i++) G.teams.push({ name: noTeam() ? 'ថ្នាក់ទាំងមូល' : clean(teamNames[i]) || ('ក្រុមទី ' + khNum(i + 1)), color: COLORS[i % COLORS.length], score: 0, members: teamMembers[i] || [] });
    hist = []; lastScores = null; saveCfg(); saveGame(); showPlay();
  }
  function saveGame() { if (G) put(GAME, G); }
  function snapshot() { hist.push(JSON.stringify(G)); if (hist.length > 40) hist.shift(); }
  function showPlay() { bgm('lobby', 0.3); lastTurn = -1; boardIn = true; $('tg').classList.add('tg-live'); document.documentElement.classList.add('tg-noscroll'); $('tg-setup').hidden = true; $('tg-play').hidden = false; $('tg-sndbtn').textContent = G.mute ? '🔇' : '🔊'; $('tg-board').innerHTML = ''; $('tg-board').removeAttribute('data-boat'); renderAll(); window.scrollTo(0, 0); }
  function showSetup() { try { if (window.KmSound) KmSound.stop(); } catch (e) {} stopTimer(); closePop(); $('tg').classList.remove('tg-live'); document.documentElement.classList.remove('tg-noscroll'); if (document.fullscreenElement) document.exitFullscreen(); $('tg-play').hidden = true; $('tg-setup').hidden = false; refreshResume(); }
  function refreshResume() { var g = load(GAME, null); $('tg-resume').hidden = !(g && g.tiles && !g.finished && g.tiles.some(function (t) { return !t.done; })); }
  function remaining() { return G.tiles.filter(function (t) { return !t.done; }).length; }

  function renderAll() { renderScore(); renderBoard(); renderTurn(); $('tg-undo').disabled = !hist.length; }
  function renderTurn() {
    var box = $('tg-turn'); box.innerHTML = '';
    if (G.finished) { box.appendChild(el('b', '', 'ហ្គេមបានបញ្ចប់')); return; }
    if (G.teams.length === 1) { box.appendChild(el('b', '', '🙋 សិស្សជ្រើសលេខ')); box.appendChild(el('small', '', ' · នៅសល់ ' + khNum(remaining()) + ' កាត')); return; }
    var dot = el('span', 'dot'); dot.style.background = G.teams[G.turn].color; box.appendChild(dot);
    box.appendChild(document.createTextNode('វេនរបស់ ')); box.appendChild(el('b', '', G.teams[G.turn].name)); box.appendChild(el('small', '', ' · នៅសល់ ' + khNum(remaining()) + ' កាត'));
    if (lastTurn !== -1 && lastTurn !== G.turn && !reduceMotion()) {            // a banner sweeps across when the turn changes
      var bn = el('div', 'tg-banner'); bn.style.setProperty('--c', G.teams[G.turn].color); bn.appendChild(el('span', '', 'វេនរបស់ ')); bn.appendChild(el('b', '', G.teams[G.turn].name));
      bn.addEventListener('animationend', function () { bn.remove(); }); $('tg-stage').appendChild(bn);
    }
    lastTurn = G.turn;
  }
  function renderScore() {
    var box = $('tg-score'); box.innerHTML = ''; box.className = 'tg-score n' + G.teams.length;
    var prev = lastScores && lastScores.length === G.teams.length ? lastScores : null, top = Math.max.apply(null, G.teams.map(function (t) { return t.score; }));
    G.teams.forEach(function (t, i) {
      var c = el('div', 'tg-tc' + (i === G.turn && !G.finished ? ' turn' : '')); c.style.setProperty('--c', t.color);
      var crown = G.teams.length > 1 && top > 0 && t.score === top;
      var h = el('div', 'tg-tn', (crown ? '👑 ' : '') + t.name), s = el('div', 'tg-ts'), ctl = el('div', 'tg-tctl');
      if (crown) c.classList.add('lead');
      var minus = el('button', '', '−'), plus = el('button', '', '+'); minus.type = plus.type = 'button'; minus.setAttribute('aria-label', 'ដកពិន្ទុ'); plus.setAttribute('aria-label', 'បន្ថែមពិន្ទុ');
      minus.addEventListener('click', function () { snapshot(); t.score -= G.pts; saveGame(); renderAll(); });
      plus.addEventListener('click', function () { snapshot(); t.score += G.pts; saveGame(); renderAll(); });
      var from = prev ? prev[i] : t.score; tweenNum(s, from, t.score);
      if (prev && from !== t.score) {
        s.classList.add('bump'); var d = t.score - from, fl = el('div', 'tg-delta ' + (d > 0 ? 'pos' : 'neg'), (d > 0 ? '+' : '−') + khNum(Math.abs(d)));
        fl.addEventListener('animationend', function () { fl.remove(); }); c.appendChild(fl);
      }
      ctl.appendChild(minus); ctl.appendChild(plus); c.appendChild(h); c.appendChild(s); c.appendChild(ctl); box.appendChild(c);
    });
    lastScores = G.teams.map(function (t) { return t.score; });
  }
  function renderBoard() {
    var box = $('tg-board'), n = G.tiles.length;
    if (G.style === 'boat') return renderBoat(box);
    box.innerHTML = '';
    if (G.style === 'wheel') return renderWheel(box);
    box.removeAttribute('style'); box.className = 'tg-board c' + (n <= 9 ? 3 : n <= 16 ? 4 : 5) + (boardIn ? ' in' : '');
    var avail = box.getBoundingClientRect(), ratio = avail.width && avail.height ? avail.width / avail.height : 1.6, cols = Math.max(2, Math.min(n, Math.ceil(Math.sqrt(n * ratio / 1.2)))), rows = Math.ceil(n / cols);
    while (cols > 2 && (cols - 1) * rows >= n) cols--;
    box.style.setProperty('--cols', cols); box.style.setProperty('--rows', rows);
    G.tiles.forEach(function (t, i) {
      var b = el('button', 'tg-tile' + (t.done ? ' done' : '') + (i === lastDone ? ' just' : '')); b.type = 'button'; b.style.setProperty('--d', Math.min(i * 40, 900) + 'ms'); var f = FACES[i % FACES.length]; b.style.setProperty('--f1', f[0]); b.style.setProperty('--f2', f[1]);
      if (t.done) {
        b.disabled = true; var mark = t.k === 's' ? SPECIALS[t.sp].icon : (t.res === 'ok' ? '✓' : '✗'); b.appendChild(el('span', 'tg-mark', mark));
        if (t.k === 'q') b.appendChild(el('span', 'tg-doneName', t.n)); if (t.by !== undefined && t.by !== null && G.teams[t.by]) b.style.setProperty('--f2', G.teams[t.by].color);
      } else {
        if (G.face === 'num' || !t.img) b.appendChild(el('span', 'tg-pic num', String(i + 1))); else b.appendChild(picNode(t.img));
        b.addEventListener('click', function () {
          if (openTileIdx >= 0 || flipping || G.finished) return;
          if (reduceMotion()) return openTile(i, b);
          flipping = true; b.classList.add('flip'); setTimeout(function () { flipping = false; openTile(i, b); }, 300);   // the tile turns over, then the card pops up
        });
      }
      b.setAttribute('aria-label', 'កាតទី ' + (i + 1)); if (t.done && t.k === 'q' && t.lq) { var dn = b.querySelector('.tg-doneName'); if (dn) dn.remove(); } box.appendChild(b);
    });
    boardIn = false; lastDone = -1;
  }

  /* ---------- boat race: every team has a long boat; a correct answer paddles it forward, the first to the finish line wins ---------- */
  function steps(tm) { return Math.floor(Math.max(0, tm.score) / G.pts + 1e-9); }
  function boatSvg(color) {
    var rowers = '', x;
    for (x = 44; x <= 176; x += 22) rowers += '<circle cx="' + x + '" cy="22" r="7" fill="#ffd8a8" stroke="#5c3b1e" stroke-width="2"/><path d="M' + x + ' 29V38" stroke="#5c3b1e" stroke-width="3"/><path d="M' + (x + 4) + ' 30L' + (x + 24) + ' 50" stroke="#8a5a2b" stroke-width="3" stroke-linecap="round"/>';
    return '<svg viewBox="0 0 230 64" aria-hidden="true">' + rowers + '<path d="M4 34Q30 54 112 54Q190 54 226 22L214 18Q184 40 112 41Q44 41 18 24Z" fill="' + color + '" stroke="#3a2a14" stroke-width="3" stroke-linejoin="round"/><path d="M226 22Q232 10 222 6" fill="none" stroke="#3a2a14" stroke-width="3" stroke-linecap="round"/><path d="M60 46H168" stroke="#fff" stroke-width="3" stroke-dasharray="8 6" opacity=".7"/></svg>';
  }
  function renderBoat(box) {
    var n = G.teams.length;
    if (box.getAttribute('data-boat') !== String(n)) {
      box.innerHTML = ''; box.className = 'tg-board tg-boatmode'; box.removeAttribute('style'); box.setAttribute('data-boat', String(n));
      var river = el('div', 'tg-river'); river.style.setProperty('--n', n);
      G.teams.forEach(function (tm, i) {
        var lane = el('div', 'tg-lane'), name = el('div', 'tg-lname', tm.name), track = el('div', 'tg-track'), boat = el('div', 'tg-boat'), flag = el('div', 'tg-flag', '🏁'), cnt = el('b', 'tg-lcount', '');
        lane.style.setProperty('--c', tm.color); boat.innerHTML = boatSvg(tm.color); track.appendChild(flag); track.appendChild(boat); lane.appendChild(name); lane.appendChild(track); lane.appendChild(cnt); river.appendChild(lane);
      });
      box.appendChild(river);
      var go = el('button', 'tg-go-q', ''); go.type = 'button';
      go.addEventListener('click', function () {
        if (openTileIdx >= 0 || G.finished) return;
        var rem = []; G.tiles.forEach(function (t, i) { if (!t.done) rem.push(i); });
        if (!rem.length) return; sfx.special(); openTile(rem[Math.floor(Math.random() * rem.length)], null);
      });
      box.appendChild(go);
    }
    var lanes = box.querySelectorAll('.tg-lane');
    G.teams.forEach(function (tm, i) {
      var st = Math.min(steps(tm), G.finish), lane = lanes[i];
      lane.classList.toggle('turn', i === G.turn && !G.finished); lane.querySelector('.tg-boat').style.setProperty('--p', st / G.finish);
      lane.querySelector('.tg-lcount').textContent = khNum(Math.min(steps(tm), G.finish)) + '/' + khNum(G.finish);
    });
    var gb = box.querySelector('.tg-go-q'); gb.disabled = !!G.finished; gb.textContent = G.finished ? '🏁' : '▶ ចេញសំណួរសម្រាប់ ' + G.teams[G.turn].name;
    gb.style.setProperty('--c', G.teams[G.turn].color);
  }

  /* ---------- spin style: a wheel picks the next question (same teams, scores, special boxes and questions as the cards) ---------- */
  var wAng = 0, spinning = false, WCOL = ['#ff6b81', '#2fd4a0', '#ffb347', '#4dabf7', '#b57cf5', '#ff7eb3'];
  function renderWheel(box) {
    box.className = 'tg-board tg-wheelmode'; box.removeAttribute('style');
    var rem = []; G.tiles.forEach(function (t, i) { if (!t.done) rem.push(i); });
    var wrap = el('div', 'tg-wheel'), cv = el('canvas', 'tg-wcanvas'), ptr = el('div', 'tg-ptr'), btn = el('button', 'tg-spin', G.finished || !rem.length ? '✓' : 'ស្ពីន!');
    btn.type = 'button'; btn.setAttribute('aria-label', 'វិលកង់'); wrap.appendChild(cv); wrap.appendChild(ptr); wrap.appendChild(btn); box.appendChild(wrap);
    function draw() {
      var s = parseFloat(cv.style.width) || 300, dpr = cv.width / s, c = cv.getContext('2d'), R = cv.width / 2, n = Math.max(1, rem.length), seg = Math.PI * 2 / n;
      c.setTransform(1, 0, 0, 1, 0, 0); c.clearRect(0, 0, cv.width, cv.height); c.translate(R, R);
      c.beginPath(); c.arc(0, 0, R * 0.985, 0, 7); c.fillStyle = '#243447'; c.fill();
      rem.forEach(function (idx, k) {
        var a0 = wAng + k * seg - Math.PI / 2 * 0, a1 = a0 + seg; c.beginPath(); c.moveTo(0, 0); c.arc(0, 0, R * 0.93, a0, a1); c.closePath();
        c.fillStyle = WCOL[k % WCOL.length]; c.fill(); c.lineWidth = Math.max(1.5, R * 0.012); c.strokeStyle = '#fff'; c.stroke();
        c.save(); c.rotate(a0 + seg / 2); c.fillStyle = '#fff'; c.textAlign = 'right'; c.textBaseline = 'middle'; c.shadowColor = 'rgba(0,0,0,.35)'; c.shadowBlur = 4 * dpr;
        c.font = '800 ' + Math.max(10 * dpr, Math.min(R * 0.14, R * 0.93 * seg * 0.45)) + 'px "Kantumruy Pro", sans-serif'; c.fillText(String(idx + 1), R * 0.88, 0); c.restore();
      });
      for (var k2 = 0; k2 < n; k2++) { var a = wAng + k2 * seg; c.beginPath(); c.arc(Math.cos(a) * R * 0.955, Math.sin(a) * R * 0.955, R * 0.017, 0, 7); c.fillStyle = '#ffe066'; c.fill(); }
    }
    function fit() {
      var r = box.getBoundingClientRect(), side = Math.max(200, Math.floor(Math.min(r.width, r.height)) - 14), dpr = Math.min(2, window.devicePixelRatio || 1);
      wrap.style.width = wrap.style.height = side + 'px'; cv.style.width = cv.style.height = side + 'px'; cv.width = cv.height = Math.round(side * dpr); draw();
    }
    fit(); window.__tgFit = fit;
    function atPointer() { var n = rem.length, seg = Math.PI * 2 / n, x = ((-Math.PI / 2 - wAng) % (Math.PI * 2) + Math.PI * 2) % (Math.PI * 2); return Math.floor(x / seg) % n; }
    btn.addEventListener('click', function () {
      if (spinning || openTileIdx >= 0 || G.finished || !rem.length) return;
      var n = rem.length, seg = Math.PI * 2 / n, k = Math.floor(Math.random() * n), jit = (Math.random() - 0.5) * seg * 0.7;
      var base = -Math.PI / 2 - (k + 0.5) * seg + jit, cur = ((wAng % (Math.PI * 2)) + Math.PI * 2) % (Math.PI * 2), turns = 4 + Math.floor(Math.random() * 3);
      var delta = ((((base - cur) % (Math.PI * 2)) + Math.PI * 2) % (Math.PI * 2)) + turns * Math.PI * 2, start = wAng, t0 = performance.now(), dur = 4200 + Math.random() * 1200, last = atPointer();
      var done = function () { wAng = start + delta; draw(); spinning = false; setTimeout(function () { sfx.flip(); openTile(rem[k], null); }, 380); };
      spinning = true; btn.disabled = true; sfx.special();
      if (reduceMotion()) return done();
      (function step(now) {
        var p = Math.min(1, (now - t0) / dur), e = 1 - Math.pow(1 - p, 3); wAng = start + delta * e; draw();
        var seg2 = atPointer(); if (seg2 !== last) { last = seg2; sfx.tick(); }
        if (p < 1) requestAnimationFrame(step); else done();
      })(t0);
    });
  }
  window.addEventListener('resize', function () { if (G && G.style === 'wheel' && window.__tgFit && !$('tg-play').hidden && !spinning) window.__tgFit(); });

  /* ---------- card popup ---------- */
  function stopTimer() { if (timerId) { clearInterval(timerId); timerId = 0; } }
  function closePop() { stopTimer(); if (flipBtn) { flipBtn.classList.remove('flip'); flipBtn = null; } $('tg-pop').hidden = true; openTileIdx = -1; stopFw(); if (G && !G.finished && !$('tg-play').hidden) bgm('lobby', 0.3); }
  function teamBtns(card, label, exclude, cb) {
    var wrap = el('div', 'tg-pick'); wrap.appendChild(el('small', '', label));
    G.teams.forEach(function (t, i) { if (i === exclude) return; var b = el('button', 'tg-pickbtn', t.name); b.type = 'button'; b.style.setProperty('--c', t.color); b.addEventListener('click', function () { cb(i); }); wrap.appendChild(b); });
    card.appendChild(wrap); return wrap;
  }
  function finishTurn(tileIdx, res, by, afterFn) {
    var t = G.tiles[tileIdx]; lastDone = tileIdx; t.done = true; t.res = res; t.by = by; if (afterFn) afterFn();
    if (remaining() === 0 || (G.style === 'boat' && G.teams.some(function (tm) { return steps(tm) >= G.finish; }))) { closePop(); saveGame(); renderAll(); return setTimeout(finishGame, G.style === 'boat' ? 1300 : 350); }
    G.turn = (G.turn + 1) % G.teams.length; saveGame(); closePop(); renderAll();
  }
  function openTile(i, tileBtn) {
    if (G.finished || openTileIdx >= 0) return;
    var t = G.tiles[i], team = G.teams[G.turn], card = $('tg-card'); openTileIdx = i; flipBtn = tileBtn; card.innerHTML = ''; card.className = 'tg-card'; card.style.setProperty('--c', team.color);
    var f = FACES[i % FACES.length]; card.style.setProperty('--f1', f[0]); card.style.setProperty('--f2', f[1]);
    var x = el('button', 'tg-x', '✕'); x.type = 'button'; x.setAttribute('aria-label', 'បិទ (ទុកកាតវិញ)'); x.addEventListener('click', closePop); card.appendChild(x);
    var head = el('div', 'tg-chead'); head.appendChild(el('span', 'tg-cn', 'កាតទី ' + khNum(i + 1))); head.appendChild(el('span', 'tg-cteam', team.name)); card.appendChild(head);
    sfx.flip(); fireworks(1800);                                        // the card pops up with fireworks
    bgm('question', 0.42);                                              // quiz-show music while the question is open
    if (t.k === 'q') {
      if (t.lq) card.classList.add('lq');
      else { var face = el('div', 'tg-cface'); face.appendChild(picNode(t.img, 'big')); card.appendChild(face); }
      card.appendChild(el('div', 'tg-name', t.n));
      var host = card;                                                       // with a figure the card is split: drawing on one side, question + answers on the other
      if (t.f) {
        var split = el('div', 'tg-split'), fg = el('div', 'tg-fig'), rc = el('div', 'tg-rc'); fg.innerHTML = t.f;   // inline SVG from our own question bank
        split.appendChild(fg); split.appendChild(rc); card.appendChild(split); host = rc; card.classList.add('hasfig');
      }
      if (t.q) host.appendChild(el('div', 'tg-q', t.q));
      if (t.o) { var ol = el('div', 'tg-opt'); t.o.forEach(function (o, k) { var li = el('div', 'tg-o' + (k === t.ck ? ' key' : '')); li.appendChild(el('b', '', 'កខគឃ'[k])); li.appendChild(el('span', '', o)); ol.appendChild(li); }); host.appendChild(ol); }
      var ans = el('div', 'tg-a' + (t.o ? ' tg-a-mcq' : ''), t.o ? '' : (t.a || '')); ans.hidden = true; if (t.a) host.appendChild(ans);
      if (t.s) { var sol = el('div', 'tg-sol', t.s); sol.hidden = true; ans.appendChild(sol); }
      typeset(card);
      if (G.timer) {
        var tm = el('div', 'tg-timer'), tn = el('span', '', khNum(G.timer)), left = G.timer; tm.appendChild(tn); card.appendChild(tm);
        stopTimer(); timerId = setInterval(function () { left--; tn.textContent = khNum(Math.max(0, left)); tm.style.setProperty('--p', Math.max(0, left) / G.timer * 100 + '%'); if (left <= 5 && left > 0) { tm.classList.add('hot'); sfx.tick(); } if (left <= 0) { stopTimer(); tm.classList.add('over'); sfx.end(); } }, 1000);
      }
      var acts = el('div', 'tg-acts');
      if (t.a) { var show = el('button', 'btn btn-ghost btn-sm', 'បង្ហាញចម្លើយ'); show.type = 'button'; show.addEventListener('click', function () { ans.hidden = !ans.hidden; card.classList.toggle('revealed', !ans.hidden); if (!ans.hidden && t.s && !ans.dataset.m) { ans.dataset.m = 1; var sl = ans.querySelector('.tg-sol'); if (sl) sl.hidden = false; } show.textContent = ans.hidden ? 'បង្ហាញចម្លើយ' : 'លាក់ចម្លើយ'; }); acts.appendChild(show); }
      var ok = el('button', 'btn btn-primary btn-sm', '✔ ត្រឹមត្រូវ +' + khNum(t.p)); ok.type = 'button';
      ok.addEventListener('click', function () { snapshot(); sfx.right(); var r = card.getBoundingClientRect(); miniBurst(r.left + r.width / 2, r.top + 80); finishTurn(i, 'ok', G.turn, function () { team.score += t.p; }); });
      var bad = el('button', 'btn btn-ghost btn-sm', '✖ មិនត្រូវ'); bad.type = 'button'; bad.addEventListener('click', function () { snapshot(); sfx.wrong(); finishTurn(i, 'bad', G.turn); });
      var other = el('button', 'btn btn-ghost btn-sm', 'ក្រុមផ្សេងឆ្លើយត្រូវ…'); other.type = 'button'; var pickBox = null;
      other.addEventListener('click', function () {
        if (pickBox) { pickBox.remove(); pickBox = null; return; }
        pickBox = teamBtns(card, 'ឱ្យពិន្ទុទៅក្រុម៖', G.turn, function (k) { snapshot(); sfx.right(); finishTurn(i, 'ok', k, function () { G.teams[k].score += t.p; }); });
      });
      acts.appendChild(ok); acts.appendChild(bad); if (G.teams.length > 1) acts.appendChild(other); card.appendChild(acts);
    } else {
      var sp = SPECIALS[t.sp]; if (G.style === 'boat' && BOAT_SP[t.sp]) sp = BOAT_SP[t.sp]; sfx[t.sp === 'bomb' ? 'bomb' : 'special']();
      card.classList.add('special', 'sp-' + t.sp); card.appendChild(el('div', 'tg-sicon', sp.icon)); card.appendChild(el('div', 'tg-sname', sp.name)); card.appendChild(el('div', 'tg-sdesc', sp.desc));
      var acts2 = el('div', 'tg-acts'), go = el('button', 'btn btn-primary btn-sm', 'យល់ព្រម'); go.type = 'button'; acts2.appendChild(go); card.appendChild(acts2);
      var apply = function (fn) { snapshot(); finishTurn(i, 'sp', G.turn, fn); };
      if (t.sp === 'bomb') go.addEventListener('click', function () { apply(function () { team.score = G.style === 'boat' ? Math.max(0, team.score - 2 * G.pts) : 0; }); });
      else if (t.sp === 'double') go.addEventListener('click', function () { apply(function () { team.score = G.style === 'boat' ? team.score + 2 * G.pts : (team.score > 0 ? team.score * 2 : team.score + G.pts); }); });
      else if (t.sp === 'gift') go.addEventListener('click', function () { apply(function () { team.score += G.pts * 2; }); });
      else if (t.sp === 'skip') go.addEventListener('click', function () { apply(); });
      else {
        go.hidden = true;
        teamBtns(card, t.sp === 'swap' ? 'ប្តូរពិន្ទុជាមួយក្រុម៖' : 'លួចពិន្ទុពីក្រុម៖', G.turn, function (k) {
          apply(function () {
            var o = G.teams[k];
            if (t.sp === 'swap') { var tmp = team.score; team.score = o.score; o.score = tmp; }
            else { var take = Math.min(Math.max(o.score, 0), G.pts); o.score -= take; team.score += take; }
          });
        });
      }
    }
    $('tg-pop').hidden = false;
  }

  /* ---------- finish ---------- */
  function ranking() { return G.teams.map(function (t, i) { return { t: t, i: i }; }).sort(function (a, b) { return b.t.score - a.t.score; }); }
  function finishGame() {
    G.finished = true; saveGame(); closePop(); renderTurn();
    var card = $('tg-card'), rk = ranking(), top = rk[0].t.score, medals = ['🥇', '🥈', '🥉'];
    card.innerHTML = ''; card.className = 'tg-card final'; card.style.setProperty('--c', rk[0].t.color);
    var x = el('button', 'tg-x', '✕'); x.type = 'button'; x.setAttribute('aria-label', 'បិទ'); x.addEventListener('click', function () { closePop(); card.className = 'tg-card'; }); card.appendChild(x);
    card.appendChild(el('div', 'tg-title', 'ហ្គេមបានបញ្ចប់! 🎉'));
    var winners = rk.filter(function (r) { return r.t.score === top; }).map(function (r) { return r.t.name; });
    card.appendChild(el('div', 'tg-winner', (winners.length > 1 ? 'ជ័យលាភីរួម៖ ' : 'ក្រុមឈ្នះ៖ ') + winners.join(' · ')));
    var places = [], pl = 0, pv = null; rk.forEach(function (r, k) { if (r.t.score !== pv) { pl = k; pv = r.t.score; } places.push(pl); });
    var pod = el('div', 'tg-podium'), podRows = rk.slice(0, 3).map(function (r, k) { return { r: r, place: places[k] }; });
    var podOrder = podRows.length === 3 ? [podRows[1], podRows[0], podRows[2]] : podRows.length === 2 ? [podRows[1], podRows[0]] : podRows;
    podOrder.forEach(function (x) {
      var col = el('div', 'tg-pcol'); col.style.setProperty('--c', x.r.t.color); col.style.setProperty('--h', [100, 74, 56][x.place] + '%'); col.style.setProperty('--d', (2 - x.place) * 0.35 + 's');
      col.appendChild(el('div', 'tg-pname', x.r.t.name)); col.appendChild(el('b', 'tg-pscore', khNum(x.r.t.score)));
      var bar = el('div', 'tg-pbar'); bar.appendChild(el('span', '', medals[x.place] || khNum(x.place + 1))); col.appendChild(bar); pod.appendChild(col);
    });
    card.appendChild(pod);
    var list = el('ol', 'tg-rank');
    rk.forEach(function (r, k) {
      if (k < 3) return; var place = places[k];
      var li = el('li'); li.style.setProperty('--c', r.t.color); li.appendChild(el('span', 'm', medals[place] || khNum(place + 1) + '.')); li.appendChild(el('span', 'n', r.t.name)); li.appendChild(el('b', 's', khNum(r.t.score))); list.appendChild(li);
    });
    if (list.children.length) card.appendChild(list);
    var acts = el('div', 'tg-acts'), png = el('button', 'btn btn-primary btn-sm', '⬇ ទាញយក PNG'), again = el('button', 'btn btn-ghost btn-sm', 'លេងម្ដងទៀត'), close = el('button', 'btn btn-ghost btn-sm', 'បិទ');
    [png, again, close].forEach(function (b) { b.type = 'button'; acts.appendChild(b); }); card.appendChild(acts);
    png.addEventListener('click', downloadResult); again.addEventListener('click', function () { card.className = 'tg-card'; startGame(); });
    close.addEventListener('click', function () { closePop(); card.className = 'tg-card'; });
    $('tg-pop').hidden = false; sfx.win(); fireworks(4200);
  }
  var FONT = '"Kantumruy Pro", "Noto Sans Khmer", sans-serif';
  function rr(g, x, y, w, h, r, tl, tr, br, bl) {
    tl = tl === undefined ? r : tl; tr = tr === undefined ? r : tr; br = br === undefined ? r : br; bl = bl === undefined ? r : bl;
    g.beginPath(); g.moveTo(x + tl, y); g.lineTo(x + w - tr, y); g.quadraticCurveTo(x + w, y, x + w, y + tr); g.lineTo(x + w, y + h - br); g.quadraticCurveTo(x + w, y + h, x + w - br, y + h);
    g.lineTo(x + bl, y + h); g.quadraticCurveTo(x, y + h, x, y + h - bl); g.lineTo(x, y + tl); g.quadraticCurveTo(x, y, x + tl, y); g.closePath();
  }
  function resultCanvas() {
    var rk = ranking(), W = 1600, rowH = 120, H = 280 + rk.length * (rowH + 18) + 140, dpr = 2, cv = document.createElement('canvas');
    cv.width = W * dpr; cv.height = H * dpr; var g = cv.getContext('2d'); g.scale(dpr, dpr);
    var bg = g.createLinearGradient(0, 0, 0, H); bg.addColorStop(0, '#eaf5f2'); bg.addColorStop(1, '#fdf6e8'); g.fillStyle = bg; g.fillRect(0, 0, W, H);
    var bn = g.createLinearGradient(0, 0, W, 240); bn.addColorStop(0, '#1f6f66'); bn.addColorStop(0.6, '#2d8f7e'); bn.addColorStop(1, '#3aa68f'); g.fillStyle = bn; g.fillRect(0, 0, W, 240);
    g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillStyle = '#fff'; g.font = '700 70px ' + FONT; g.fillText('លទ្ធផលហ្គេមក្រុម 🏆', W / 2, 96);
    var d = new Date(); g.font = '500 32px ' + FONT; g.globalAlpha = 0.92; g.fillText(khNum(d.getDate() + '/' + (d.getMonth() + 1) + '/' + d.getFullYear()) + '  ·  ' + khNum(G.tiles.length) + ' កាត', W / 2, 176); g.globalAlpha = 1;
    var y = 280, medals = ['🥇', '🥈', '🥉'], place = 0, prev = null;
    rk.forEach(function (r, k) {
      if (r.t.score !== prev) { place = k; prev = r.t.score; }
      g.save(); g.shadowColor = 'rgba(0,0,0,.16)'; g.shadowBlur = 18; g.shadowOffsetY = 6; g.fillStyle = '#fff'; rr(g, 60, y, W - 120, rowH, 22); g.fill(); g.restore();
      g.fillStyle = r.t.color; rr(g, 60, y, 26, rowH, 22, 22, 0, 0, 22); g.fill();
      g.textAlign = 'center'; g.font = '700 54px ' + FONT; g.fillStyle = '#1b2733'; g.fillText(medals[place] || khNum(place + 1) + '.', 150, y + rowH / 2 + 2);
      g.textAlign = 'left'; g.font = '700 46px ' + FONT; var nm = r.t.name, sz = 46; while (g.measureText(nm).width > 900 && sz > 20) { sz -= 2; g.font = '700 ' + sz + 'px ' + FONT; }
      g.fillStyle = '#1b2733'; g.fillText(nm, 220, y + (r.t.members.length ? 44 : rowH / 2 + 2));
      if (r.t.members.length) { g.font = '500 26px ' + FONT; g.fillStyle = '#5b6b7b'; var ms = r.t.members.join(' · '); while (g.measureText(ms).width > 1000 && ms.length > 6) ms = ms.slice(0, -2); g.fillText(ms, 220, y + 86); }
      g.textAlign = 'right'; g.font = '700 64px ' + FONT; g.fillStyle = r.t.color; g.fillText(khNum(r.t.score), W - 100, y + rowH / 2 + 2);
      y += rowH + 18;
    });
    var fy = H - 70; g.strokeStyle = 'rgba(31,111,102,.25)'; g.lineWidth = 2; g.beginPath(); g.moveTo(60, H - 130); g.lineTo(W - 60, H - 130); g.stroke();
    g.fillStyle = '#12263a'; rr(g, W / 2 - 215, fy - 30, 60, 60, 14); g.fill(); g.fillStyle = '#fff'; g.textAlign = 'center'; g.font = '700 38px ' + FONT; g.fillText('√', W / 2 - 185, fy + 2);
    g.fillStyle = '#e0a13a'; rr(g, W / 2 - 172, fy - 4, 14, 14, 3); g.fill();
    g.textAlign = 'left'; g.fillStyle = '#1f6f66'; g.font = '700 42px ' + FONT; g.fillText('khmermath.org', W / 2 - 140, fy - 2); g.fillStyle = '#5b6b7b'; g.font = '500 24px ' + FONT; g.fillText('ហ្គេមក្រុម · គណិតវិទ្យាខ្មែរ', W / 2 - 140, fy + 34);
    return cv;
  }
  function saveBlob(blob, name) { var a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = name; document.body.appendChild(a); a.click(); a.remove(); setTimeout(function () { URL.revokeObjectURL(a.href); }, 4000); }
  function isPhone() { return (window.matchMedia && matchMedia('(pointer: coarse)').matches) || /Android|iPhone|iPad|iPod|Mobile|FBAN|FBAV|Telegram|Line\//i.test(navigator.userAgent); }
  function downloadResult() {
    var go = function () {
      resultCanvas().toBlob(function (b) {
        if (!b) return; var d = new Date(), z = function (x) { return ('0' + x).slice(-2); }, name = 'khmermath-teamgame-' + d.getFullYear() + z(d.getMonth() + 1) + z(d.getDate()) + '.png';
        if (!isPhone()) return saveBlob(b, name);
        var old = $('tg-pv'); if (old) old.remove();
        var url = URL.createObjectURL(b), box = el('div', 'tg-pv'), x = el('button', 'tg-x tg-xpv', '✕'), row = el('div', 'tg-acts'), img = el('img'), p = el('p', '', 'ចុចសង្កត់លើរូបភាព រួចជ្រើស «រក្សាទុករូបភាព» ឬប្រើប៊ូតុងខាងលើ។');
        box.id = 'tg-pv'; img.src = url; x.type = 'button'; var close = function () { box.remove(); URL.revokeObjectURL(url); }; x.addEventListener('click', close);
        var file = null; try { file = new File([b], name, { type: 'image/png' }); } catch (e) {}
        if (file && navigator.canShare && navigator.canShare({ files: [file] })) { var sh = el('button', 'btn btn-primary btn-sm', 'ចែករំលែក / រក្សាទុក'); sh.type = 'button'; sh.addEventListener('click', function () { navigator.share({ files: [file], title: 'khmermath.org' }).catch(function () {}); }); row.appendChild(sh); }
        var dl = el('button', 'btn btn-ghost btn-sm', 'ទាញយក'); dl.type = 'button'; dl.addEventListener('click', function () { saveBlob(b, name); }); row.appendChild(dl);
        box.appendChild(x); box.appendChild(row); box.appendChild(p); box.appendChild(img); document.body.appendChild(box);
      }, 'image/png');
    };
    (document.fonts && document.fonts.load ? Promise.all([document.fonts.load('700 40px "Kantumruy Pro"', 'សិស្សក'), document.fonts.load('500 30px "Kantumruy Pro"', 'សិស្សក')]) : Promise.resolve()).then(go, go);
  }

  /* ---------- wiring ---------- */
  $('tg-nteams').addEventListener('change', function () { renderTeamSetup(); saveCfg(); });
  if ($('tg-noteam')) $('tg-noteam').addEventListener('change', function () { renderTeamSetup(); saveCfg(); });
  $('tg-sound').addEventListener('change', function () { if (!sndOn()) { try { if (window.KmSound) KmSound.stop(); } catch (e) {} } else if (G && !G.finished && !$('tg-play').hidden) bgm(openTileIdx >= 0 ? 'question' : 'lobby', openTileIdx >= 0 ? 0.42 : 0.3); });
  ['tg-noteam', 'tg-pts', 'tg-style', 'tg-finish', 'tg-timer', 'tg-face', 'tg-special', 'tg-nspecial', 'tg-sound'].forEach(function (id) { $(id).addEventListener('change', saveCfg); });
  $('tg-addcard').addEventListener('click', function () { cards.push({ n: '', img: '', q: '', a: '', p: '' }); renderCards(); saveCfg(); var rows = document.querySelectorAll('.tg-crow'); if (rows.length) { var last = rows[rows.length - 1]; last.scrollIntoView({ block: 'center' }); var inp = last.querySelector('input'); if (inp) inp.focus(); } });
  $('tg-clearcards').addEventListener('click', function () { if (cards.length && !confirm('លុបកាតទាំងអស់?')) return; cards = []; renderCards(); saveCfg(); });
  $('tg-pastebtn').addEventListener('click', function () { $('tg-pastebox').hidden = !$('tg-pastebox').hidden; if (!$('tg-pastebox').hidden) $('tg-questions').focus(); });
  $('tg-pastecancel').addEventListener('click', function () { $('tg-pastebox').hidden = true; });
  $('tg-pasteadd').addEventListener('click', function () {
    var add = parsePaste($('tg-questions').value); if (!add.length) return;
    cards = cards.filter(function (c) { return clean(c.n) || clean(c.img) || clean(c.q); }).concat(add); $('tg-questions').value = ''; $('tg-pastebox').hidden = true; renderCards(); saveCfg();
  });
  $('tg-file').addEventListener('change', function () {
    var f = this.files[0]; this.value = ''; if (!f || pendingFile < 0) return; var i = pendingFile; pendingFile = -1;
    resize(f, function (data) { if (!data) return alert('មិនអាចអានរូបភាពនេះបានទេ។'); cards[i].img = data; renderCards(); saveCfg(); });
  });
  $('tg-save').addEventListener('click', function () {
    var list = cards.filter(function (c) { return clean(c.n); }); if (!list.length) return;
    var name = clean(prompt('ឈ្មោះសំណុំកាត (ឧ. មេរៀនទី ១៤)')); if (!name) return;
    var sets = load(SETS, []).filter(function (s) { return s.name !== name; }); sets.push({ name: name, cards: list }); if (!put(SETS, sets)) alert('ទំហំផ្ទុកពេញ — សូមលុបសំណុំចាស់ ឬកាត់បន្ថយរូបថត។'); renderSets();
  });
  $('tg-load').addEventListener('click', function () { var i = $('tg-sets').value; if (i === '') return; var s = load(SETS, [])[+i]; if (s) useCards(s.cards); });
  $('tg-delset').addEventListener('click', function () {
    var i = $('tg-sets').value; if (i === '') return; var sets = load(SETS, []); if (!sets[+i] || !confirm('លុប «' + sets[+i].name + '»?')) return; sets.splice(+i, 1); put(SETS, sets); renderSets();
  });
  $('tg-import').addEventListener('click', function () {
    var g = load('km_wheel_last_groups', null); if (!g || !g.groups) return;
    var gr = g.groups.slice(0, 8); $('tg-nteams').value = Math.max(2, gr.length); teamNames = []; teamMembers = [];
    gr.forEach(function (m, i) { teamNames[i] = 'ក្រុមទី ' + khNum(i + 1); teamMembers[i] = m; });
    renderTeamSetup(); saveCfg();
  });
  $('tg-start').addEventListener('click', startGame);
  $('tg-resume').addEventListener('click', function () { var g = load(GAME, null); if (!g) return; G = g; hist = []; showPlay(); });
  $('tg-back').addEventListener('click', showSetup);
  $('tg-undo').addEventListener('click', function () { if (!hist.length) return; closePop(); G = JSON.parse(hist.pop()); saveGame(); renderAll(); });
  $('tg-end').addEventListener('click', function () { if (G.finished || confirm('បញ្ចប់ហ្គេមឥឡូវនេះ ហើយបង្ហាញលទ្ធផល?')) finishGame(); });
  $('tg-sndbtn').addEventListener('click', function () { G.mute = !G.mute; this.setAttribute('aria-pressed', !G.mute); this.textContent = G.mute ? '🔇' : '🔊'; saveGame(); });
  $('tg-full').addEventListener('click', function () { var st = $('tg'); if (document.fullscreenElement) document.exitFullscreen(); else if (st.requestFullscreen) st.requestFullscreen(); });
  if (!document.fullscreenEnabled) $('tg-full').hidden = true;
  $('tg-pop').addEventListener('click', function (e) { if (e.target === this && !$('tg-card').classList.contains('final')) closePop(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !$('tg-pop').hidden) { closePop(); $('tg-card').className = 'tg-card'; } });

  function applyMode() {
    $('tg-lessonbox').hidden = mode !== 'lesson'; $('tg-custom').hidden = mode === 'lesson';
    document.querySelectorAll('input[name="tg-mode"]').forEach(function (r) { r.checked = r.value === mode; });
    $('tg-face').closest('label').hidden = mode === 'lesson';
  }
  function lessonName(L) { return 'មេរៀនទី ' + khNum(L.d || L.n); }
  function inClass(L) { return (L.g || 7) === curClass; }
  function pickClass(c, keep) {                       // switch grade: show that grade's lessons, make sure one is ticked
    curClass = c; $('tg-class').value = String(c);
    var mine = ((BANK && BANK.lessons) || []).filter(inClass);
    if (!keep || !mine.some(function (L) { return selLessons.indexOf(L.n) >= 0; })) { if (mine.length) selLessons = [mine[0].n]; }
    renderLessons(); saveCfg();
  }
  function renderLessons() {
    var box = $('tg-lessons'); box.innerHTML = ''; var ls = ((BANK && BANK.lessons) || []).filter(inClass);
    if (!ls.length) box.appendChild(el('small', 'tg-hint', BANK === null ? 'កំពុងផ្ទុក…' : BANK.closed ? 'គ្រូបានបិទហ្គេមនេះជាបណ្តោះអាសន្ន។' : 'គ្រូមិនទាន់បើកមេរៀនណាមួយទៀត។'));
    ls.forEach(function (L) {
      var lab = el('label', 'tg-lesson'), cb = el('input'); cb.type = 'checkbox'; cb.checked = selLessons.indexOf(L.n) >= 0;
      cb.addEventListener('change', function () { var all = (BANK && BANK.lessons) || []; selLessons = all.filter(function (x) { return x.n === L.n ? cb.checked : selLessons.indexOf(x.n) >= 0; }).map(function (x) { return x.n; }); lab.classList.toggle('on', cb.checked); saveCfg(); });
      lab.classList.toggle('on', cb.checked); lab.appendChild(cb); lab.appendChild(el('b', '', lessonName(L))); lab.appendChild(el('span', '', L.title)); lab.appendChild(el('small', '', khNum(L.qs.length) + ' សំណួរ')); box.appendChild(lab);
    });
  }
  // The question bank lives on exam.khmermath.org (teachers fix questions and choose the lessons there); the copy shipped with this
  // page is the fallback when that is unreachable.
  // the teacher (in exam.khmermath.org) chooses which game styles students may play here; the teacher's own copy (exam site) ignores this
  function applyGames(g) {
    if (window.TG_NOGATE || !g) return;
    var sel = $('tg-style'), open = 0;
    Array.prototype.forEach.call(sel.options, function (o) { o.disabled = g[o.value] === false; if (!o.disabled) open++; });
    if (open && sel.options[sel.selectedIndex].disabled) for (var i = 0; i < sel.options.length; i++) if (!sel.options[i].disabled) { sel.value = sel.options[i].value; break; }
    $('tg-start').disabled = !open;
    if (!open) $('tg-lessonhint').textContent = 'គ្រូបានបិទហ្គេមនេះជាបណ្តោះអាសន្ន។';
  }
  var BANK_URLS = window.TG_URLS || ['https://exam.khmermath.org/api/game/bank', '../static/data/teamgame_g7.json'];
  function loadBank() {
    var i = 0;
    (function next() {
      if (i >= BANK_URLS.length) { BANK = { lessons: [] }; renderLessons(); return; }
      fetch(BANK_URLS[i++], { cache: 'no-cache' }).then(function (r) { if (!r.ok) throw 0; return r.json(); }).then(function (d) {
        if (!d || !d.lessons) throw 0;
        BANK = d; if (!selLessons.length || !d.lessons.some(function (L) { return selLessons.indexOf(L.n) >= 0; })) selLessons = d.lessons.length ? [d.lessons[0].n] : [];
        var first = d.lessons.filter(function (L) { return selLessons.indexOf(L.n) >= 0; })[0]; curClass = first ? (first.g || 7) : 7; $('tg-class').value = String(curClass);
        renderLessons(); applyGames(d.games);
      }).catch(next);
    })();
  }
  document.querySelectorAll('input[name="tg-mode"]').forEach(function (r) { r.addEventListener('change', function () { if (r.checked) { mode = r.value; applyMode(); saveCfg(); } }); });
  $('tg-qn').addEventListener('change', saveCfg);
  $('tg-alllessons').addEventListener('click', function () { if (BANK) selLessons = BANK.lessons.filter(inClass).map(function (L) { return L.n; }); renderLessons(); saveCfg(); });
  $('tg-class').addEventListener('change', function () { pickClass(parseInt($('tg-class').value, 10) || 7, false); });
  loadCfg(); (function () { var m = /[?&]style=(wheel|cards|boat)/.exec(location.search); if (m) $('tg-style').value = m[1]; })(); applyMode(); loadBank(); renderTeamSetup(); renderPacks(); renderCards(); renderSets(); checkImport(); refreshResume();
  if (/[?&]import=1/.test(location.search) && !$('tg-import').hidden) $('tg-import').click();   // opened from the teacher dashboard: teams come from the class
})();
