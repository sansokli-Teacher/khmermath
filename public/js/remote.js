// Phone controller for the team game: shows the teams, the board and the open question, and sends the teacher's taps to the game that
// runs on the computer (js/tgremote.js ↔ js/rcnet.js ↔ src/remote_do.js). Every tap reacts at once on the phone (pressed state,
// vibration, "sending…"), and is confirmed when the game screen has carried it out.
(function () {
  'use strict';
  var root = document.getElementById('rc'), q = new URLSearchParams(location.search), CODE = q.get('c'), KEY = q.get('k');
  var esc = function (t) { return String(t == null ? '' : t).replace(/[&<>"']/g, function (m) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[m]; }); };
  var kh = function (n) { return String(n).replace(/\d/g, function (d) { return '០១២៣៤៥៦៧៨៩'[d]; }); };
  var FACES = [['#ff6b81', '#e8456b'], ['#2fd4a0', '#2fa66b'], ['#ffb347', '#ff8a3d'], ['#4dabf7', '#1c7ed6'], ['#b57cf5', '#8a4fe0'], ['#ff7eb3', '#e0518c']];
  if (!CODE || !KEY) { root.innerHTML = '<div class="msg"><h1>Game Remote</h1><p>Open this page by scanning the QR code on the game screen.</p></div>'; return; }

  var S = null, hostOn = false, linkM = 'wait', net = null, pending = {}, idKey = {}, cidKey = {}, cidN = 0, menu = '', showScores = false, opening = '', openingAt = 0, saving = 0, shown = {}, ring = {}, lastSig = '', toastT = 0, gone = false;

  // ---------- feedback ----------
  function toast(text, kind) {
    var t = document.getElementById('toast'); if (!t) return;
    t.textContent = text; t.className = 'toast show ' + (kind || ''); clearTimeout(toastT); toastT = setTimeout(function () { t.className = 'toast'; }, kind === 'bad' ? 2800 : 1100);
  }
  function buzz(p) { if (navigator.vibrate) try { navigator.vibrate(p); } catch (e) {} }
  var keyOf = function (c) { return c.t + ':' + (c.i != null ? c.i : c.k != null ? c.k : ''); };

  function send(c, el) {
    var key = keyOf(c);
    if (pending[key] && Date.now() - pending[key] < 600) return;        // double tap
    pending[key] = Date.now(); buzz(18);
    if (el) el.classList.add('sending');
    var cid = ++cidN; cidKey[cid] = key;
    // optimistic changes: the screen answers before the game screen does
    if (c.t === 'open') { opening = 'card ' + kh(c.i + 1); openingAt = Date.now(); }
    else if (c.t === 'spin') { opening = 'Spinning…'; openingAt = Date.now(); }
    else if (c.t === 'go') { opening = 'Next question…'; openingAt = Date.now(); }
    else if (c.t === 'show' && S && S.card) shown[S.card.i] = revealed(S.card) ? 0 : 1;   // show / hide: the phone answers before the screen does
    else if (c.t === 'ok' || c.t === 'bad' || c.t === 'pick' || c.t === 'sp') { saving = Date.now(); }
    net.cmd(c, cid);
    setTimeout(function () {                                           // nothing came back: say so
      if (pending[key]) { delete pending[key]; if (opening && c.t === 'open') opening = ''; saving = 0; toast('No answer from the game screen — is it open?', 'bad'); lastSig = ''; draw(); }
    }, 3200);
    if (c.t === 'open' || c.t === 'spin' || c.t === 'go' || c.t === 'show' || saving) { lastSig = ''; draw(); }
  }
  function sent(cid, r) {
    var key = cidKey[cid]; if (!key) return;
    if (!r.ok) { delete pending[key]; toast('Could not send', 'bad'); lastSig = ''; draw(); return; }
    idKey[r.id] = key;
    if (r.delivered === false) { toast('The game screen is offline', 'bad'); }
    if (linkM !== 'live') { setTimeout(function () { clearKey(key); }, 500); }   // polling: no ack message, the next state shows the result
  }
  function clearKey(key, flash) {
    delete pending[key];
    var el = root.querySelector('[data-k="' + key + '"]'); if (el) { el.classList.remove('sending'); if (flash !== false) { el.classList.add('flash'); setTimeout(function () { el.classList.remove('flash'); }, 450); } }
  }
  function acked(id) { var key = idKey[id]; if (!key) return; delete idKey[id]; clearKey(key); }

  // ---------- link ----------
  net = new RcNet({
    role: 'ctl', code: CODE, key: KEY,
    onState: function (s) {
      S = s;
      if (!s.card) { shown = {}; ring = {}; }
      else if (shown[s.card.i] !== undefined && !!shown[s.card.i] === !!s.card.rev) delete shown[s.card.i];   // the screen caught up
      if (s.card || s.fin) { opening = ''; } if (!s.card) saving = 0;
      if (opening && Date.now() - openingAt > 5000) opening = '';
      draw();
    },
    onHost: function (on) { hostOn = on; lastSig = ''; draw(); },
    onLink: function (m) { linkM = m; lastSig = ''; draw(); },
    onSent: sent, onAck: acked,
    onGone: function () { gone = true; root.innerHTML = '<div class="msg"><h1>Remote closed</h1><p>This remote link is no longer active. Scan a new QR code on the game screen.</p></div>'; net.close(); },
  });

  // is the answer shown on the screen? (the phone's own tap counts until the screen confirms it)
  function revealed(c) { return shown[c.i] !== undefined ? !!shown[c.i] : !!c.rev; }

  // ---------- pieces ----------
  function btn(cls, label, c, extra) {
    var key = keyOf(c), on = pending[key] ? ' sending' : '';
    return '<button type="button" class="b ' + cls + on + '" data-k="' + esc(key) + '" data-c=\'' + esc(JSON.stringify(c)) + '\'' + (extra || '') + '><span>' + label + '</span></button>';
  }
  function chipHtml() {
    var live = linkM === 'live', txt = !hostOn ? 'Game screen offline' : live ? 'Live' : linkM === 'poll' ? 'Connected' : 'Connecting…';
    return '<span class="chip ' + (hostOn && linkM !== 'wait' ? (live ? 'live' : 'poll') : 'off') + '"><i></i>' + txt + '</span>';
  }
  function teamsHtml() {
    return '<div class="teams">' + S.teams.map(function (t, i) {
      var turn = i === S.turn && !S.fin;
      return '<div class="team' + (turn ? ' turn' : '') + '" style="--c:' + esc(t.c) + '">' + (turn ? '<em>TURN</em>' : '') + '<b>' + esc(t.n) + '</b><span>' + kh(S.style === 'boat' ? Math.min(t.st, S.finish) + '/' + S.finish : t.s) + '</span>'
        + (showScores ? '<div class="adj">' + btn('mini', '−', { t: 'score', k: i, d: -1 }) + btn('mini', '+', { t: 'score', k: i, d: 1 }) + '</div>' : '') + '</div>';
    }).join('') + '</div>';
  }
  function overlayHtml() { return opening ? '<div class="busy"><div class="spin"></div><b>' + esc(opening) + '</b></div>' : ''; }
  function pickHtml(card, label) {
    return '<div class="pick"><p>' + label + '</p>' + card.pick.map(function (p) { return btn('pickb', esc(p.n), { t: 'pick', k: p.k }); }).join('') + btn('ghost', 'បោះបង់', { t: 'other' }) + '</div>';
  }
  function ringHtml(c) {
    var left = c.over ? 0 : c.left, total = Math.max(ring[c.i] || 0, left, 1); ring[c.i] = total;
    var C = 2 * Math.PI * 26, off = C * (1 - left / total);
    return '<div class="ring' + (c.over ? ' over' : left <= 5 ? ' hot' : '') + '"><svg viewBox="0 0 64 64"><circle cx="32" cy="32" r="26" class="bg"/><circle cx="32" cy="32" r="26" class="fg" id="ringfg" stroke-dasharray="' + C.toFixed(1) + '" stroke-dashoffset="' + off.toFixed(1) + '"/></svg><b id="tleft">' + left + '</b></div>';
  }
  function boardHtml() {
    var who = S.teams[S.turn], bar = '<div class="turnbar" style="--c:' + esc(who.c) + '"><small>Now playing</small><b>' + esc(who.n) + '</b></div>';
    if (S.style === 'wheel') return bar + '<div class="center">' + btn('huge', S.spinning || opening ? 'Spinning…' : '🎡<br>SPIN', { t: 'spin' }, S.spinning || !S.rem || opening ? ' disabled' : '') + '<p class="note">' + kh(S.rem) + ' questions left</p></div>';
    if (S.style === 'boat') return bar + '<div class="center">' + btn('huge', opening ? 'Loading…' : '▶<br>Next question', { t: 'go' }, !S.rem || opening ? ' disabled' : '') + '<p class="note">' + kh(S.rem) + ' questions left</p></div>';
    return bar + '<p class="hint">Tap a card to open it on the screen</p><div class="grid">' + S.tiles.map(function (t, i) {
      if (t.d) return '<div class="tile done" style="' + (t.b >= 0 && S.teams[t.b] ? '--c:' + esc(S.teams[t.b].c) : '') + '">' + (t.sp ? '★' : t.r === 'ok' ? '✓' : '✗') + '</div>';
      var f = FACES[i % FACES.length];
      return btn('tile', kh(i + 1), { t: 'open', i: i }, ' style="--f1:' + f[0] + ';--f2:' + f[1] + '"' + (opening ? ' disabled' : ''));
    }).join('') + '</div>';
  }
  function questionHtml(c) {
    var opts = c.o ? '<div class="opts">' + c.o.map(function (x, i) { return '<div class="opt' + (i === c.ck ? ' key' : '') + '"><b>' + 'កខគឃ'[i] + '</b><span>' + esc(x) + '</span>' + (i === c.ck ? '<i>✓</i>' : '') + '</div>'; }).join('') + '</div>' : '';
    var rev = revealed(c), dis = saving ? ' disabled' : '';
    var top = '<div class="qtop"><div><small>' + esc(c.n || '') + '</small></div>' + (c.left !== undefined ? ringHtml(c) : '') + '</div>';
    var ans = '<div class="ans' + (rev ? ' on' : '') + '"><small>' + (rev ? '✓ ចម្លើយ — កំពុងបង្ហាញលើអេក្រង់' : 'ចម្លើយ — មានតែលោកគ្រូអ្នកគ្រូឃើញ') + '</small><div>' + esc(c.a) + '</div>' + (c.s ? '<small class="sol">' + esc(c.s) + '</small>' : '') + '</div>';
    var body = '<div class="qscroll">' + ans + '<div class="qtext">' + esc(c.q) + '</div>' + (c.fig ? '<p class="note">🖼 រូបភាពនៅលើអេក្រង់</p>' : '') + opts + '</div>';
    var dock = c.pick && c.pick.length ? '<div class="dock">' + pickHtml(c, 'ក្រុមណាឆ្លើយត្រូវ?') + '</div>'
      : '<div class="dock"><div class="row3">' + btn('soft' + (rev ? ' on' : ''), rev ? '🙈 លាក់ចម្លើយ' : '👁 បង្ហាញចម្លើយ', { t: 'show' }) + btn('soft', '+15 s', { t: 'plus' }) + btn('soft', 'ក្រុមផ្សេងឆ្លើយត្រូវ…', { t: 'other' }) + '</div>'
        + '<div class="row2">' + btn('bad', '✖ មិនត្រូវ', { t: 'bad' }, dis) + btn('ok', '✔ ត្រឹមត្រូវ +' + kh(c.p || S.pts), { t: 'ok' }, dis) + '</div></div>';
    return '<section class="qwrap">' + top + body + '</section>' + dock + (saving ? '<div class="busy light"><div class="spin"></div><b>Saving…</b></div>' : '');
  }
  function specialHtml(c) {
    return '<section class="sp"><div class="sic">' + esc(c.icon) + '</div><h2>' + esc(c.name) + '</h2><p>' + esc(c.desc) + '</p>'
      + (c.pick && c.pick.length ? pickHtml(c, 'ជ្រើសរើសក្រុម') : c.go ? btn('big ok', 'យល់ព្រម', { t: 'sp' }) : '') + btn('ghost', '✕ បិទកាត', { t: 'close' }) + '</section>';
  }
  function finalHtml() {
    var top = S.rank[0] ? S.rank[0].s : 0;
    return '<section class="fin"><div class="trophy">🏆</div><h2>Game over</h2>' + S.rank.map(function (r, i) { return '<div class="rank" style="--c:' + esc(r.c) + '"><span>' + (r.s === top ? '🥇' : kh(i + 1)) + '</span><b>' + esc(r.n) + '</b><em>' + kh(r.s) + '</em></div>'; }).join('') + '<p class="note">The result is on the game screen. You can close this page.</p></section>';
  }
  function sheetHtml() {
    if (menu === 'menu') return '<div class="sheet-back" data-close="1"><div class="sheet"><i class="grip"></i><h3>Menu</h3>' + '<button type="button" class="b soft" data-act="scores"><span>± ' + (showScores ? 'Hide score buttons' : 'Adjust scores') + '</span></button>' + '<button type="button" class="b endb" data-act="end"><span>■ End the game</span></button>' + '<button type="button" class="b ghost" data-close="1"><span>Close</span></button></div></div>';
    if (menu === 'end') return '<div class="sheet-back" data-close="1"><div class="sheet"><i class="grip"></i><h3>End the game?</h3><p class="note">The result is shown on the game screen.</p>' + btn('endb', '■ Yes, end the game', { t: 'end' }) + '<button type="button" class="b ghost" data-close="1"><span>Keep playing</span></button></div></div>';
    return '';
  }

  // ---------- draw ----------
  function draw() {
    if (gone) return;
    if (!S || S.idle) {
      var sigI = 'idle' + hostOn + linkM; if (sigI === lastSig) return; lastSig = sigI;
      root.innerHTML = '<header class="top"><b>📱 Game Remote</b>' + chipHtml() + '</header><div class="msg"><div class="pulse">🎮</div><h1>Ready</h1><p>' + (hostOn ? 'Start the game on the computer. This phone will show the controls.' : 'Waiting for the game screen…') + '</p></div><div id="toast" class="toast"></div>';
      return;
    }
    var c = S.card;
    var sig = JSON.stringify([c ? Object.assign({}, c, { left: 0, over: 0 }) : null, S.turn, S.teams, S.tiles, S.fin, S.spinning, S.rem, hostOn, linkM, showScores, menu, opening, saving > 0, c ? shown[c.i] : -1, Object.keys(pending).join()]);
    if (sig === lastSig) { // only the clock moved
      var tl = document.getElementById('tleft'), fg = document.getElementById('ringfg');
      if (tl && c && c.left !== undefined) {
        var left = c.over ? 0 : c.left, total = Math.max(ring[c.i] || 0, left, 1); ring[c.i] = total; tl.textContent = left;
        if (fg) fg.setAttribute('stroke-dashoffset', (2 * Math.PI * 26 * (1 - left / total)).toFixed(1));
        var rg = tl.parentNode; rg.className = 'ring' + (c.over ? ' over' : left <= 5 ? ' hot' : '');
      }
      return;
    }
    var scr = S.fin ? 'fin' : c ? 'card' + c.i : 'board', scroll = window.scrollY, fresh = scr !== root.getAttribute('data-scr');
    lastSig = sig;
    var body = S.fin ? finalHtml() : c ? (c.k === 's' ? specialHtml(c) : questionHtml(c)) : boardHtml();
    root.setAttribute('data-scr', scr);
    root.className = (c && c.k === 'q' ? 'has-dock ' : '') + (fresh ? 'enter' : '');
    root.innerHTML = '<header class="top"><b>📱 Game Remote</b>' + chipHtml() + '<button type="button" class="menu" data-act="menu" aria-label="Menu">⋯</button></header>'
      + (hostOn ? '' : '<div class="off">The game screen is not connected. Open the game on the computer.</div>') + teamsHtml() + '<main>' + body + '</main>' + overlayHtml() + sheetHtml() + '<div id="toast" class="toast"></div>';
    if (!fresh) window.scrollTo(0, scroll);
    if (window.renderMathInElement) try { window.renderMathInElement(root, { delimiters: [{ left: '\\(', right: '\\)', display: false }, { left: '\\[', right: '\\]', display: true }], throwOnError: false }); } catch (e) {}
  }

  // ---------- taps ----------
  root.addEventListener('click', function (e) {
    var close = e.target.closest('[data-close]'); if (close && (e.target === close || close.classList.contains('b'))) { menu = ''; lastSig = ''; draw(); return; }
    var a = e.target.closest('[data-act]');
    if (a) { var act = a.getAttribute('data-act'); if (act === 'menu') menu = 'menu'; else if (act === 'scores') { showScores = !showScores; menu = ''; } else if (act === 'end') menu = 'end'; lastSig = ''; draw(); return; }
    var b = e.target.closest('button[data-c]'); if (!b || b.disabled) return;
    var c = JSON.parse(b.getAttribute('data-c'));
    if (c.t === 'end') menu = '';
    send(c, b);
  });
  // keep the phone awake while it is the remote
  try { if (navigator.wakeLock) { var lock = function () { navigator.wakeLock.request('screen').catch(function () {}); }; lock(); document.addEventListener('visibilitychange', function () { if (document.visibilityState === 'visible') lock(); }); } } catch (e) {}
  draw();
})();
