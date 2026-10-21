// Phone controller for the team game: shows the teams, the board and the open question, and sends the teacher's taps to the game
// that runs on the computer (see js/tgremote.js and src/api/remote.js).
(function () {
  'use strict';
  var root = document.getElementById('rc'), q = new URLSearchParams(location.search), CODE = q.get('c'), KEY = q.get('k');
  var seq = 0, S = null, alive = false, failures = 0, last = '', busy = {}, showScores = false, lastSig = '';
  var esc = function (t) { return String(t == null ? '' : t).replace(/[&<>"]/g, function (m) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[m]; }); };
  var kh = function (n) { return String(n).replace(/\d/g, function (d) { return '០១២៣៤៥៦៧៨៩'[d]; }); };
  if (!CODE || !KEY) { root.innerHTML = '<div class="rc-msg"><h1>Game Remote</h1><p>Open this page by scanning the QR code on the game screen.</p></div>'; return; }

  function send(c) {
    if (navigator.vibrate) try { navigator.vibrate(18); } catch (e) {}
    var k = c.t + (c.i != null ? ':' + c.i : '') + (c.k != null ? ':' + c.k : '');
    if (busy[k]) return; busy[k] = 1; setTimeout(function () { delete busy[k]; }, 450);
    fetch('/api/remote/cmd', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ code: CODE, k: KEY, c: c }) }).catch(function () {});
  }
  window.rcSend = send;

  function poll() {
    fetch('/api/remote/state?c=' + encodeURIComponent(CODE) + '&k=' + encodeURIComponent(KEY) + '&seq=' + seq, { cache: 'no-store' })
      .then(function (r) { if (r.status === 404) throw new Error('gone'); return r.json(); })
      .then(function (d) { failures = 0; alive = !!d.host_alive; if (d.state) { S = d.state; seq = d.seq; } else if (d.seq !== seq) { seq = d.seq; } draw(); setTimeout(poll, 700); })
      .catch(function (e) {
        if (e.message === 'gone') { root.innerHTML = '<div class="rc-msg"><h1>Remote closed</h1><p>This remote link is no longer active. Scan a new QR code on the game screen.</p></div>'; return; }
        failures++; alive = false; draw(); setTimeout(poll, Math.min(4000, 700 + failures * 500));
      });
  }

  function btn(cls, label, c, extra) { return '<button type="button" class="b ' + cls + '" data-c=\'' + esc(JSON.stringify(c)) + '\'' + (extra || '') + '>' + label + '</button>'; }

  function teamsHtml() {
    return '<div class="teams">' + S.teams.map(function (t, i) {
      return '<div class="team' + (i === S.turn && !S.fin ? ' turn' : '') + '" style="--c:' + esc(t.c) + '"><b>' + esc(t.n) + '</b><span>' + kh(S.style === 'boat' ? Math.min(t.st, S.finish) + '/' + S.finish : t.s) + '</span>'
        + (showScores ? '<div class="adj">' + btn('mini', '−', { t: 'score', k: i, d: -1 }) + btn('mini', '+', { t: 'score', k: i, d: 1 }) + '</div>' : '') + '</div>';
    }).join('') + '</div>';
  }
  function pickHtml(card, label) {
    if (!card.pick || !card.pick.length) return '';
    return '<div class="pick"><p>' + label + '</p>' + card.pick.map(function (p) { return btn('pickb', esc(p.n), { t: 'pick', k: p.k }); }).join('') + '</div>';
  }
  function cardHtml(c) {
    if (c.k === 's') {
      return '<div class="card sp"><div class="sic">' + esc(c.icon) + '</div><h2>' + esc(c.name) + '</h2><p>' + esc(c.desc) + '</p>'
        + (c.go ? btn('big ok', 'OK', { t: 'sp' }) : pickHtml(c, 'Choose the team')) + btn('ghost', '✕ Close card', { t: 'close' }) + '</div>';
    }
    var o = c.o ? '<div class="opts">' + c.o.map(function (x, i) { return '<div class="opt' + (i === c.ck ? ' key' : '') + '"><b>' + 'កខគឃ'[i] + '</b><span>' + esc(x) + '</span></div>'; }).join('') + '</div>' : '';
    var timer = c.left !== undefined && (c.left > 0 || c.over) ? '<div class="tm' + (c.over ? ' over' : c.left <= 5 ? ' hot' : '') + '"><span id="tleft">' + (c.over ? '0' : c.left) + '</span><small>s</small></div>' : '';
    return '<div class="card"><div class="chead"><span>' + esc(c.n || '') + '</span>' + timer + '</div>'
      + '<div class="qtext">' + esc(c.q) + '</div>' + (c.fig ? '<p class="note">🖼 The figure is on the screen</p>' : '') + o
      + '<div class="ans"><small>Answer (only you see this)</small><div>' + esc(c.a) + '</div></div>'
      + '<div class="row2">' + btn('' + (c.rev ? ' done' : ''), c.rev ? '👁 Shown' : '👁 Show answer', { t: 'show' }) + btn('', '+15 s', { t: 'plus' }) + '</div>'
      + '<div class="row2">' + btn('ok', '✔ Correct +' + kh(c.p || S.pts), { t: 'ok' }) + btn('bad', '✖ Wrong', { t: 'bad' }) + '</div>'
      + btn('other', 'Other team ✔…', { t: 'other' }) + pickHtml(c, 'Which team answered right?') + btn('ghost', '✕ Close card', { t: 'close' }) + '</div>';
  }
  function boardHtml() {
    if (S.fin) return '';
    var who = S.teams[S.turn] ? S.teams[S.turn].n : '';
    if (S.style === 'wheel') return '<div class="turnbar" style="--c:' + esc(S.teams[S.turn].c) + '">Turn: ' + esc(who) + '</div>' + btn('huge', S.spinning ? '…' : '🎡 SPIN', { t: 'spin' }, S.spinning || !S.rem ? ' disabled' : '') + '<p class="note">' + kh(S.rem) + ' questions left</p>';
    if (S.style === 'boat') return '<div class="turnbar" style="--c:' + esc(S.teams[S.turn].c) + '">Turn: ' + esc(who) + '</div>' + btn('huge', '▶ Next question', { t: 'go' }, !S.rem ? ' disabled' : '') + '<p class="note">' + kh(S.rem) + ' questions left</p>';
    return '<div class="turnbar" style="--c:' + esc(S.teams[S.turn].c) + '">Turn: ' + esc(who) + ' — pick a card</div><div class="grid">' + S.tiles.map(function (t, i) {
      if (t.d) return '<button type="button" class="tile done" disabled style="' + (t.b >= 0 && S.teams[t.b] ? '--c:' + esc(S.teams[t.b].c) : '') + '">' + (t.sp ? '★' : t.r === 'ok' ? '✓' : '✗') + '</button>';
      return btn('tile', kh(i + 1), { t: 'open', i: i });
    }).join('') + '</div>';
  }
  function finalHtml() {
    var top = S.rank[0] ? S.rank[0].s : 0;
    return '<div class="card fin"><h2>🏆 Game over</h2>' + S.rank.map(function (r, i) { return '<div class="rank" style="--c:' + esc(r.c) + '"><span>' + (i === 0 || r.s === top ? '🥇' : kh(i + 1)) + '</span><b>' + esc(r.n) + '</b><em>' + kh(r.s) + '</em></div>'; }).join('')
      + '<p class="note">The result is on the game screen. You can close this page.</p></div>';
  }

  function draw() {
    var banner = alive ? '' : '<div class="off">' + (failures ? 'No connection — retrying…' : 'The game screen is not connected') + '</div>';
    if (!S || S.idle) { root.innerHTML = '<header><b>📱 Game Remote</b><i class="dot ' + (alive ? 'on' : '') + '"></i></header>' + banner + '<div class="rc-msg"><h1>Ready</h1><p>Start the game on the computer. This phone will show the controls.</p></div>'; lastSig = ''; return; }
    var sig = JSON.stringify([S, alive, failures > 0, showScores]);
    var sigNoTimer = JSON.stringify([S.card ? Object.assign({}, S.card, { left: 0, over: 0 }) : null, S.turn, S.teams, S.tiles, S.fin, S.spinning, S.rem, alive, failures > 0, showScores]);
    if (sigNoTimer === lastSig) { var tl = document.getElementById('tleft'); if (tl && S.card) { tl.textContent = S.card.over ? '0' : S.card.left; var tm = tl.parentNode; tm.className = 'tm' + (S.card.over ? ' over' : S.card.left <= 5 ? ' hot' : ''); } return; }
    lastSig = sigNoTimer;
    var body = S.fin ? finalHtml() : S.card ? cardHtml(S.card) : boardHtml();
    root.innerHTML = '<header><b>📱 Game Remote</b><button type="button" class="lnk" id="scoreBtn">' + (showScores ? 'Done' : '± Scores') + '</button><i class="dot ' + (alive ? 'on' : '') + '"></i></header>' + banner + teamsHtml() + '<main>' + body + '</main>'
      + (S.fin ? '' : '<footer>' + btn('end', '■ End game', { t: 'end' }, ' data-confirm="End the game and show the result?"') + '</footer>');
    if (window.renderMathInElement) try { window.renderMathInElement(root, { delimiters: [{ left: '\\(', right: '\\)', display: false }, { left: '\\[', right: '\\]', display: true }], throwOnError: false }); } catch (e) {}
  }

  root.addEventListener('click', function (e) {
    var b = e.target.closest('button'); if (!b) return;
    if (b.id === 'scoreBtn') { showScores = !showScores; lastSig = ''; draw(); return; }
    var c = b.getAttribute('data-c'); if (!c || b.disabled) return;
    var conf = b.getAttribute('data-confirm'); if (conf && !window.confirm(conf)) return;
    send(JSON.parse(c));
  });
  // keep the phone awake while it is the remote
  try { if (navigator.wakeLock) { var lock = function () { navigator.wakeLock.request('screen').catch(function () {}); }; lock(); document.addEventListener('visibilitychange', function () { if (document.visibilityState === 'visible') lock(); }); } } catch (e) {}
  poll();
})();
