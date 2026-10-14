/* khmermath.org — «ហ្គេមក្រុម» (play/teamgame.html): a Baamboozle-style classroom quiz.
   Teams take turns picking numbered tiles; a tile hides a question or a special power-up. Everything stays in this browser. */
(function () {
  'use strict';
  var $ = function (id) { return document.getElementById(id); };
  if (!$('tg')) return;
  var GAME = 'km_tg_game_v1', SETS = 'km_tg_sets_v1', CFG = 'km_tg_cfg_v1';
  var COLORS = ['#e8590c', '#1c7ed6', '#2f9e44', '#ae3ec9', '#f08c00', '#0c8599', '#d6336c', '#5f3dc4'];
  var SPECIALS = {
    bomb:  { icon: '💣', name: 'គ្រាប់បែក!', desc: 'ក្រុមដែលជ្រើសបាត់ពិន្ទុទាំងអស់ (ត្រឡប់ទៅ ០)។' },
    double:{ icon: '✖២', name: 'ពិន្ទុទ្វេដង!', desc: 'ពិន្ទុរបស់ក្រុមនេះកើនឡើងទ្វេដង។' },
    swap:  { icon: '🔄', name: 'ប្តូរពិន្ទុ!', desc: 'ជ្រើសក្រុមមួយ ដើម្បីប្តូរពិន្ទុជាមួយ។' },
    gift:  { icon: '🎁', name: 'អំណោយ!', desc: 'ទទួលបានពិន្ទុបន្ថែមទ្វេដងនៃពិន្ទុសំណួរ។' },
    steal: { icon: '🕵', name: 'លួចពិន្ទុ!', desc: 'ជ្រើសក្រុមមួយ ដើម្បីលួចយកពិន្ទុរបស់គេ។' },
    skip:  { icon: '⏭', name: 'បាត់វេន!', desc: 'ក្រុមនេះបាត់វេន គ្មានពិន្ទុ។' }
  };
  var G = null, hist = [], teamNames = [], teamMembers = [], audio = null, timerId = 0, openTileIdx = -1;

  /* ---------- helpers ---------- */
  function khNum(n) { return String(n).replace(/\d/g, function (d) { return '០១២៣៤៥៦៧៨៩'[d]; }); }
  function enNum(s) { return String(s).replace(/[០-៩]/g, function (d) { return '០១២៣៤៥៦៧៨៩'.indexOf(d); }); }
  function shuffle(a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  function load(k, d) { try { var v = JSON.parse(localStorage.getItem(k)); return v === null ? d : v; } catch (e) { return d; } }
  function put(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text !== undefined) e.textContent = text; return e; }
  function clean(s) { return String(s || '').replace(/ /g, ' ').replace(/\s+/g, ' ').trim(); }
  function reduceMotion() { return window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches; }
  function sndOn() { return $('tg-sound').checked && !(G && G.mute); }

  /* ---------- sound ---------- */
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
    flip: function () { tone([440, 660], 0.06, 0.12); },
    right: function () { tone([660, 880, 1100], 0.08, 0.2); },
    wrong: function () { tone([200, 150], 0.09, 0.28, 'square'); },
    bomb: function () { tone([120, 90, 60], 0.14, 0.35, 'sawtooth'); },
    special: function () { tone([523, 784, 659, 988], 0.07, 0.18); },
    tick: function () { tone([900], 0.05, 0.05); },
    end: function () { tone([880, 880, 880], 0.1, 0.12, 'square'); },
    win: function () { tone([523, 659, 784, 1047, 1319], 0.08, 0.3); }
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
    if (fwRandom && now < fwEnd && now > fwNext) { fwBurst(W * (0.1 + Math.random() * 0.8), H * (0.1 + Math.random() * 0.5), 46); fwNext = now + 240 + Math.random() * 240; }
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

  /* ---------- setup ---------- */
  function parseQuestions(text) {
    return text.split(/\r?\n/).map(function (line) {
      var parts = (line.indexOf('|') >= 0 ? line.split('|') : line.split('\t')).map(clean);
      if (!parts[0]) return null;
      var p = parts[2] ? parseInt(enNum(parts[2]), 10) : 0;
      return { q: parts[0].replace(/^[\d០-៩]+\s*[.)\-:]\s+/, ''), a: parts[1] || '', p: p > 0 ? p : 0 };
    }).filter(Boolean);
  }
  function renderTeamSetup() {
    var n = Math.max(2, Math.min(8, parseInt($('tg-nteams').value, 10) || 2)), box = $('tg-teamlist'); box.innerHTML = '';
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
  function updateQCount() {
    var qs = parseQuestions($('tg-questions').value); $('tg-qcount').textContent = qs.length ? khNum(qs.length) + ' សំណួរ' : 'មិនទាន់មានសំណួរ';
  }
  function saveCfg() {
    put(CFG, { n: $('tg-nteams').value, names: teamNames, members: teamMembers, q: $('tg-questions').value, pts: $('tg-pts').value, timer: $('tg-timer').value, sp: $('tg-special').checked, nsp: $('tg-nspecial').value, snd: $('tg-sound').checked });
  }
  function loadCfg() {
    var c = load(CFG, null); if (!c) return;
    $('tg-nteams').value = c.n || 4; teamNames = c.names || []; teamMembers = c.members || []; $('tg-questions').value = c.q || '';
    $('tg-pts').value = c.pts || 10; $('tg-timer').value = c.timer || '0'; $('tg-special').checked = c.sp !== false; $('tg-nspecial').value = c.nsp === undefined ? 3 : c.nsp; $('tg-sound').checked = c.snd !== false;
  }
  function renderSets() {
    var sel = $('tg-sets'), sets = load(SETS, []); sel.innerHTML = '<option value="">— សំណួរដែលបានរក្សាទុក —</option>';
    sets.forEach(function (s, i) { var o = el('option', '', s.name + ' (' + parseQuestions(s.text).length + ')'); o.value = i; sel.appendChild(o); });
  }
  function checkImport() {
    var g = load('km_wheel_last_groups', null);
    if (g && g.groups && g.groups.length) { $('tg-import').hidden = false; $('tg-importhint').hidden = false; $('tg-importhint').textContent = 'មានលទ្ធផលបែងចែកក្រុមចុងក្រោយពីកង់ចាប់ឈ្មោះ៖ ' + (g.cls || '') + ' (' + khNum(g.groups.length) + ' ក្រុម)។'; }
  }

  /* ---------- game ---------- */
  function startGame() {
    var qs = parseQuestions($('tg-questions').value), n = Math.max(2, Math.min(8, parseInt($('tg-nteams').value, 10) || 2));
    if (!qs.length) { $('tg-qcount').textContent = 'សូមវាយសំណួរយ៉ាងហោចណាស់ ១ ជាមុនសិន។'; $('tg-questions').focus(); return; }
    var pts = Math.max(1, parseInt($('tg-pts').value, 10) || 10), tiles = qs.map(function (q) { return { k: 'q', q: q.q, a: q.a, p: q.p || pts }; });
    if ($('tg-special').checked) {
      var keys = Object.keys(SPECIALS), cnt = Math.max(0, Math.min(12, parseInt($('tg-nspecial').value, 10) || 0)), deck = [];
      while (deck.length < cnt) deck = deck.concat(shuffle(keys));
      deck.slice(0, cnt).forEach(function (sp) { tiles.push({ k: 's', sp: sp }); });
    }
    G = { teams: [], tiles: shuffle(tiles), turn: 0, pts: pts, timer: parseInt($('tg-timer').value, 10) || 0, mute: false, finished: false, startedAt: Date.now() };
    for (var i = 0; i < n; i++) G.teams.push({ name: clean(teamNames[i]) || ('ក្រុមទី ' + khNum(i + 1)), color: COLORS[i % COLORS.length], score: 0, members: teamMembers[i] || [] });
    hist = []; saveCfg(); saveGame(); showPlay();
  }
  function saveGame() { if (G) put(GAME, G); }
  function snapshot() { hist.push(JSON.stringify(G)); if (hist.length > 40) hist.shift(); }
  function showPlay() { $('tg-setup').hidden = true; $('tg-play').hidden = false; renderAll(); window.scrollTo({ top: $('tg').offsetTop - 70, behavior: 'smooth' }); }
  function showSetup() { stopTimer(); closePop(); $('tg-play').hidden = true; $('tg-setup').hidden = false; refreshResume(); }
  function refreshResume() { var g = load(GAME, null); $('tg-resume').hidden = !(g && g.tiles && !g.finished && g.tiles.some(function (t) { return !t.done; })); }
  function remaining() { return G.tiles.filter(function (t) { return !t.done; }).length; }

  function renderAll() { renderScore(); renderBoard(); renderTurn(); $('tg-undo').disabled = !hist.length; }
  function renderTurn() {
    var box = $('tg-turn'); box.innerHTML = '';
    if (G.finished) { box.appendChild(el('b', '', 'ហ្គេមបានបញ្ចប់')); return; }
    var t = G.teams[G.turn], dot = el('span', 'dot'); dot.style.background = t.color;
    box.appendChild(dot); box.appendChild(document.createTextNode('វេនរបស់ ')); box.appendChild(el('b', '', t.name));
    box.appendChild(el('small', '', ' · នៅសល់ ' + khNum(remaining()) + ' ប្រអប់'));
  }
  function renderScore() {
    var box = $('tg-score'); box.innerHTML = ''; box.className = 'tg-score n' + G.teams.length;
    G.teams.forEach(function (t, i) {
      var c = el('div', 'tg-tc' + (i === G.turn && !G.finished ? ' turn' : '')); c.style.setProperty('--c', t.color);
      var h = el('div', 'tg-tn', t.name), s = el('div', 'tg-ts', khNum(t.score)), ctl = el('div', 'tg-tctl');
      var minus = el('button', '', '−'), plus = el('button', '', '+'); minus.type = plus.type = 'button'; minus.setAttribute('aria-label', 'ដកពិន្ទុ'); plus.setAttribute('aria-label', 'បន្ថែមពិន្ទុ');
      minus.addEventListener('click', function () { snapshot(); t.score -= G.pts; saveGame(); renderAll(); });
      plus.addEventListener('click', function () { snapshot(); t.score += G.pts; saveGame(); renderAll(); });
      ctl.appendChild(minus); ctl.appendChild(plus); c.appendChild(h);
      if (t.members && t.members.length) c.appendChild(el('div', 'tg-tm', t.members.join(' · ')));
      c.appendChild(s); c.appendChild(ctl); box.appendChild(c);
    });
  }
  function renderBoard() {
    var box = $('tg-board'); box.innerHTML = '';
    G.tiles.forEach(function (t, i) {
      var b = el('button', 'tg-tile' + (t.done ? ' done' : '')); b.type = 'button'; b.style.setProperty('--tc', COLORS[i % COLORS.length]);
      if (t.done) { b.disabled = true; b.textContent = t.k === 's' ? SPECIALS[t.sp].icon : (t.res === 'ok' ? '✓' : '✗'); if (t.by !== undefined && t.by !== null && G.teams[t.by]) b.style.setProperty('--tc', G.teams[t.by].color); }
      else { b.textContent = khNum(i + 1); b.addEventListener('click', function () { openTile(i); }); }
      b.setAttribute('aria-label', 'ប្រអប់ទី ' + (i + 1)); box.appendChild(b);
    });
  }

  /* ---------- tile popup ---------- */
  function stopTimer() { if (timerId) { clearInterval(timerId); timerId = 0; } }
  function closePop() { stopTimer(); $('tg-pop').hidden = true; openTileIdx = -1; }
  function teamBtns(card, label, exclude, cb) {
    var wrap = el('div', 'tg-pick'); wrap.appendChild(el('small', '', label));
    G.teams.forEach(function (t, i) { if (i === exclude) return; var b = el('button', 'tg-pickbtn', t.name); b.type = 'button'; b.style.setProperty('--c', t.color); b.addEventListener('click', function () { cb(i); }); wrap.appendChild(b); });
    card.appendChild(wrap); return wrap;
  }
  function finishTurn(tileIdx, res, by, afterFn) {
    var t = G.tiles[tileIdx]; t.done = true; t.res = res; t.by = by;
    if (afterFn) afterFn();
    if (remaining() === 0) { closePop(); saveGame(); renderAll(); return setTimeout(finishGame, 350); }
    G.turn = (G.turn + 1) % G.teams.length; saveGame(); closePop(); renderAll();
  }
  function openTile(i) {
    if (G.finished || openTileIdx >= 0) return;
    var t = G.tiles[i], team = G.teams[G.turn], card = $('tg-card'); openTileIdx = i; card.innerHTML = ''; card.className = 'tg-card'; card.style.setProperty('--c', team.color);
    sfx.flip();
    var x = el('button', 'tg-x', '✕'); x.type = 'button'; x.setAttribute('aria-label', 'បិទ (ទុកប្រអប់វិញ)'); x.addEventListener('click', closePop); card.appendChild(x);
    var head = el('div', 'tg-chead'); head.appendChild(el('span', 'tg-cn', 'ប្រអប់ទី ' + khNum(i + 1))); head.appendChild(el('span', 'tg-cteam', team.name)); card.appendChild(head);
    if (t.k === 'q') {
      card.appendChild(el('div', 'tg-q', t.q));
      var ans = el('div', 'tg-a', t.a || '(គ្មានចម្លើយដែលបានកត់ត្រា)'); ans.hidden = true; card.appendChild(ans);
      if (G.timer) {
        var tm = el('div', 'tg-timer', khNum(G.timer)), left = G.timer; card.appendChild(tm);
        stopTimer(); timerId = setInterval(function () { left--; tm.textContent = khNum(Math.max(0, left)); if (left <= 5 && left > 0) { tm.classList.add('hot'); sfx.tick(); } if (left <= 0) { stopTimer(); tm.classList.add('over'); sfx.end(); } }, 1000);
      }
      var acts = el('div', 'tg-acts'), show = el('button', 'btn btn-ghost btn-sm', 'បង្ហាញចម្លើយ'); show.type = 'button'; show.addEventListener('click', function () { ans.hidden = !ans.hidden; show.textContent = ans.hidden ? 'បង្ហាញចម្លើយ' : 'លាក់ចម្លើយ'; });
      var ok = el('button', 'btn btn-primary btn-sm', '✔ ត្រឹមត្រូវ +' + khNum(t.p)); ok.type = 'button';
      ok.addEventListener('click', function () { snapshot(); sfx.right(); var r = card.getBoundingClientRect(); miniBurst(r.left + r.width / 2, r.top + 60); finishTurn(i, 'ok', G.turn, function () { team.score += t.p; }); });
      var bad = el('button', 'btn btn-ghost btn-sm', '✖ មិនត្រូវ'); bad.type = 'button'; bad.addEventListener('click', function () { snapshot(); sfx.wrong(); finishTurn(i, 'bad', G.turn); });
      var other = el('button', 'btn btn-ghost btn-sm', 'ក្រុមផ្សេងឆ្លើយត្រូវ…'); other.type = 'button';
      var pickBox = null; other.addEventListener('click', function () {
        if (pickBox) { pickBox.remove(); pickBox = null; return; }
        pickBox = teamBtns(card, 'ឱ្យពិន្ទុទៅក្រុម៖', G.turn, function (k) { snapshot(); sfx.right(); finishTurn(i, 'ok', k, function () { G.teams[k].score += t.p; }); });
      });
      acts.appendChild(show); acts.appendChild(ok); acts.appendChild(bad); acts.appendChild(other); card.appendChild(acts);
    } else {
      var sp = SPECIALS[t.sp]; sfx[t.sp === 'bomb' ? 'bomb' : 'special']();
      card.classList.add('special'); card.appendChild(el('div', 'tg-sicon', sp.icon)); card.appendChild(el('div', 'tg-sname', sp.name)); card.appendChild(el('div', 'tg-sdesc', sp.desc));
      var acts2 = el('div', 'tg-acts'), go = el('button', 'btn btn-primary btn-sm', 'យល់ព្រម'); go.type = 'button'; acts2.appendChild(go); card.appendChild(acts2);
      var apply = function (fn) { snapshot(); finishTurn(i, 'sp', G.turn, fn); };
      if (t.sp === 'bomb') go.addEventListener('click', function () { apply(function () { team.score = 0; }); });
      else if (t.sp === 'double') go.addEventListener('click', function () { apply(function () { team.score = team.score > 0 ? team.score * 2 : team.score + G.pts; }); });
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
    var list = el('ol', 'tg-rank'), place = 0, prev = null;
    rk.forEach(function (r, k) {
      if (r.t.score !== prev) { place = k; prev = r.t.score; }
      var li = el('li'); li.style.setProperty('--c', r.t.color); li.appendChild(el('span', 'm', medals[place] || khNum(place + 1) + '.')); li.appendChild(el('span', 'n', r.t.name)); li.appendChild(el('b', 's', khNum(r.t.score))); list.appendChild(li);
    });
    card.appendChild(list);
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
    var d = new Date(); g.font = '500 32px ' + FONT; g.globalAlpha = 0.92; g.fillText(khNum(d.getDate() + '/' + (d.getMonth() + 1) + '/' + d.getFullYear()) + '  ·  ' + khNum(G.tiles.length) + ' ប្រអប់', W / 2, 176); g.globalAlpha = 1;
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
  $('tg-questions').addEventListener('input', function () { updateQCount(); saveCfg(); });
  ['tg-pts', 'tg-timer', 'tg-special', 'tg-nspecial', 'tg-sound'].forEach(function (id) { $(id).addEventListener('change', saveCfg); });
  $('tg-sample').addEventListener('click', function () {
    $('tg-questions').value = 'តើ ៧ × ៨ ស្មើប៉ុន្មាន? | ៥៦\nផលបូកមុំក្នុងត្រីកោណស្មើប៉ុន្មានដឺក្រេ? | ១៨០°\nចំនួនបឋមតូចបំផុតគឺអ្វី? | ២\nតម្លៃនៃ √៨១ ស្មើប៉ុន្មាន? | ៩\nរង្វាស់ជ្រុងម្ខាងនៃការ៉េមានក្រឡាផ្ទៃ ៦៤ cm² ស្មើប៉ុន្មាន? | ៨ cm\nបូក៖ ១/២ + ១/៤ = ? | ៣/៤\nតើ ១៥% នៃ ២០០ ស្មើប៉ុន្មាន? | ៣០\nដោះស្រាយ៖ ២x + ៣ = ១១ | x = ៤\nចំនួនជ្រុងនៃឆកោនមានប៉ុន្មាន? | ៦\nតើ ២³ ស្មើប៉ុន្មាន? | ៨ | ១៥';
    updateQCount(); saveCfg();
  });
  $('tg-save').addEventListener('click', function () {
    var text = $('tg-questions').value; if (!parseQuestions(text).length) return;
    var name = clean(prompt('ឈ្មោះសំណួរដែលត្រូវរក្សាទុក (ឧ. មេរៀនទី ១៤)')); if (!name) return;
    var sets = load(SETS, []).filter(function (s) { return s.name !== name; }); sets.push({ name: name, text: text }); put(SETS, sets); renderSets();
  });
  $('tg-load').addEventListener('click', function () {
    var i = $('tg-sets').value; if (i === '') return; var s = load(SETS, [])[+i]; if (!s) return; $('tg-questions').value = s.text; updateQCount(); saveCfg();
  });
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
  $('tg-full').addEventListener('click', function () { var st = $('tg-stage'); if (document.fullscreenElement) document.exitFullscreen(); else if (st.requestFullscreen) st.requestFullscreen(); });
  if (!document.fullscreenEnabled) $('tg-full').hidden = true;
  $('tg-pop').addEventListener('click', function (e) { if (e.target === this && !$('tg-card').classList.contains('final')) closePop(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !$('tg-pop').hidden) { closePop(); $('tg-card').className = 'tg-card'; } });

  loadCfg(); renderTeamSetup(); updateQCount(); renderSets(); checkImport(); refreshResume();
})();
