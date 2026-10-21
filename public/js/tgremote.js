// Phone remote, projector side. «📱 Remote» opens a room, shows a QR code and a link; the phone controller (remote.html) then drives this
// game page. The page publishes its state to the relay (/api/remote/*) and carries out the commands the phone sends.
(function () {
  'use strict';
  var $ = function (id) { return document.getElementById(id); };
  var KEY = 'km_tg_remote_v1', room = null, net = null, phoneOn = false, linkMode = 'wait', lastSent = '', lastPush = 0, timer = 0, modal = null, autoAsked = false;
  try { room = JSON.parse(sessionStorage.getItem(KEY)); } catch (e) { room = null; }
  if (window.TG_STUDENT || !$('tg-remote')) { if ($('tg-remote')) $('tg-remote').hidden = true; return; }

  function save() { try { if (room) sessionStorage.setItem(KEY, JSON.stringify(room)); else sessionStorage.removeItem(KEY); } catch (e) {} }
  function post(path, body) {
    return fetch(path, { method: 'POST', credentials: 'include', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) }).then(function (r) { return r.json().then(function (d) { if (!r.ok) { var e = new Error(d.error || 'Request failed'); e.status = r.status; throw e; } return d; }); });
  }
  function link() { return location.origin + '/remote.html?c=' + room.code + '&k=' + room.ctl; }
  function connected() { return !!room && phoneOn; }

  function paintBtn() {
    var b = $('tg-remote'); if (!b) return;
    b.textContent = room ? (connected() ? '📱 Remote ●' : '📱 Remote ○') : '📱 Remote';
    b.classList.toggle('rc-on', !!room && connected());
    if (modal) {
      var st = modal.querySelector('.rc-status'); if (st) { st.textContent = connected() ? '📱 Phone connected ✓' : 'Waiting for the phone…'; st.className = 'rc-status ' + (connected() ? 'ok' : ''); }
      if (connected() && !modal._closing) { modal._closing = true; var m = modal; setTimeout(function () { if (modal === m) closeModal(); }, 1600); }   // the phone is paired: get the panel out of the way of the game
    }
  }

  // publish the game state when it changes (about 4 times a second is plenty); the link itself is instant
  function tick() {
    if (!room || !net) return;
    var S = null; try { S = window.TGX ? window.TGX.state() : { idle: 1 }; } catch (e) { S = { idle: 1 }; }
    var s = JSON.stringify(S), now = Date.now();
    if (s !== lastSent || now - lastPush > 4000) { lastSent = s; lastPush = now; net.pushState(s); }
  }
  function connect() {
    if (net || !room) return;
    net = new RcNet({
      role: 'host', code: room.code, key: room.host,
      onCmd: function (id, c) { try { window.TGX && window.TGX.run(c); } catch (e) {} net.done(id); setTimeout(tick, 60); },   // do what the phone asked, answer at once, then publish the result
      onPhone: function (on) { phoneOn = on; paintBtn(); },
      onLink: function (m) { linkMode = m; paintBtn(); },
      onGone: function () { stop(); },
    });
    timer = setInterval(tick, 250); tick();
  }
  function stop() { if (timer) clearInterval(timer); timer = 0; if (net) net.close(); net = null; room = null; phoneOn = false; lastSent = ''; save(); paintBtn(); if (modal) { modal.remove(); modal = null; } }

  function qr(url, size) {
    var q = qrcode(0, 'M'); q.addData(url); q.make();
    var box = document.createElement('div'); box.className = 'rc-qr'; box.style.width = box.style.height = size + 'px';
    box.innerHTML = q.createSvgTag({ cellSize: 4, margin: 0, scalable: true });
    var sv = box.querySelector('svg'); if (sv) { sv.style.width = '100%'; sv.style.height = '100%'; }
    return box;
  }
  function closeModal() { if (modal) { modal.remove(); modal = null; } }
  function openModal() {
    closeModal();
    modal = document.createElement('div'); modal.className = 'rc-back';
    var card = document.createElement('div'); card.className = 'rc-card'; card.setAttribute('role', 'dialog'); card.setAttribute('aria-label', 'Phone remote');
    card.innerHTML = '<button type="button" class="rc-x" aria-label="Close">✕</button><h2>📱 Control from your phone</h2><p class="rc-sub">Scan the QR code with the phone camera. The game stays on this screen; the phone becomes the remote.</p><div class="rc-body"></div><div class="rc-status"></div>'
      + '<div class="rc-linkrow"><input class="rc-link" readonly><button type="button" class="rc-copy">Copy link</button></div><div class="rc-act"><button type="button" class="rc-stop">Stop remote</button><button type="button" class="rc-done">Done</button></div>';
    modal.appendChild(card); document.body.appendChild(modal);
    card.querySelector('.rc-body').appendChild(qr(link(), 260));
    var inp = card.querySelector('.rc-link'); inp.value = link(); inp.addEventListener('focus', function () { inp.select(); });
    card.querySelector('.rc-copy').onclick = function () { var b = this; (navigator.clipboard ? navigator.clipboard.writeText(link()) : Promise.reject()).then(function () { b.textContent = 'Copied ✓'; }, function () { inp.select(); b.textContent = 'Press Ctrl/Cmd+C'; }); setTimeout(function () { b.textContent = 'Copy link'; }, 2200); };
    card.querySelector('.rc-x').onclick = card.querySelector('.rc-done').onclick = closeModal;
    card.querySelector('.rc-stop').onclick = stop;
    modal.onmousedown = function (e) { if (e.target === modal) closeModal(); };
    paintBtn();
  }

  function begin() {
    if (room) { connect(); openModal(); return; }
    post('/api/remote/create', {}).then(function (d) { room = d; lastSent = ''; save(); connect(); openModal(); }).catch(function (e) { alert(e.status === 401 ? 'Please log in as a teacher first.' : e.message); });
  }
  $('tg-remote').addEventListener('click', begin);
  if (room) { connect(); paintBtn(); }
  // opened from the games wizard with «control from phone» on: show the QR as soon as the game starts
  if (/[?&]remote=1/.test(location.search)) {
    var w = setInterval(function () { if (window.TGX && window.TGX.active() && !autoAsked) { autoAsked = true; clearInterval(w); if (!room) begin(); else openModal(); } }, 400);
  }
})();
