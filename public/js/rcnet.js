// Link between the projector page (role 'host') and the phone (role 'ctl') of the game remote.
// A WebSocket is the normal link (messages arrive at once). When a network blocks it, the same pages talk over plain HTTP polling,
// and try the WebSocket again now and then. Both pages use the same object; the server keeps them in step either way.
(function () {
  'use strict';
  function RcNet(o) {
    var self = this, ws = null, mode = 'ws', fails = 0, closed = false, wsOpen = false, ack = 0, lastState = '', pending = '', seq = 0;
    var pingT = 0, pollT = 0, retryT = 0, inflight = false, cidMap = {}, lastPhone = null, lastHost = null;
    var base = (location.protocol === 'https:' ? 'wss://' : 'ws://') + location.host + '/api/remote/ws?c=' + encodeURIComponent(o.code) + '&k=' + encodeURIComponent(o.key);
    function link() { if (o.onLink) o.onLink(wsOpen ? 'live' : mode === 'poll' ? 'poll' : 'wait'); }
    function msg(m) {
      if (m.t === 'state') { if (o.onState) { try { o.onState(JSON.parse(m.s), m.seq); } catch (e) {} } }
      else if (m.t === 'cmd') { if (o.onCmd) o.onCmd(m.id, m.c); }
      else if (m.t === 'ack') { if (o.onAck) o.onAck(m.id); }
      else if (m.t === 'sent') { if (o.onSent) o.onSent(m.cid, m); }
      else if (m.t === 'host') { if (o.onHost) o.onHost(!!m.on); }
      else if (m.t === 'phone') { if (o.onPhone) o.onPhone(!!m.on); }
    }
    function startPing() { stopPing(); pingT = setInterval(function () { try { if (ws && ws.readyState === 1) ws.send('ping'); } catch (e) {} }, 20000); }
    function stopPing() { if (pingT) clearInterval(pingT); pingT = 0; }

    function openWs() {
      if (closed) return;
      var opened = false;
      try { ws = new WebSocket(base); } catch (e) { return startPolling(); }
      ws.onopen = function () {
        opened = true; wsOpen = true; fails = 0; mode = 'ws'; stopPolling(); startPing(); link();
        if (o.role === 'host' && lastState) { try { ws.send(JSON.stringify({ t: 'state', s: lastState })); } catch (e) {} }
      };
      ws.onmessage = function (e) { if (e.data === 'pong') return; try { msg(JSON.parse(e.data)); } catch (x) {} };
      ws.onclose = function () {
        wsOpen = false; stopPing(); link();
        if (closed) return;
        if (!opened) { fails++; if (fails >= 2) return startPolling(); }
        setTimeout(openWs, Math.min(3000, 300 * (fails + 1)));
      };
      ws.onerror = function () { /* onclose follows */ };
    }

    // ---- HTTP fallback ----
    function post(path, body) {
      return fetch(path, { method: 'POST', credentials: 'include', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) }).then(function (r) { return r.json().then(function (d) { if (!r.ok) { var e = new Error(d.error || 'failed'); e.status = r.status; throw e; } return d; }); });
    }
    function pollOnce() {
      if (closed || inflight || wsOpen) return;
      inflight = true;
      var p;
      if (o.role === 'host') {
        var st = pending; pending = '';
        p = post('/api/remote/sync', { code: o.code, host: o.key, state: st || undefined, ack: ack }).then(function (d) {
          if (o.onPhone) { var on = !!d.phone_on; if (on !== lastPhone) { lastPhone = on; o.onPhone(on); } }
          (d.cmds || []).forEach(function (c) { if (c.id > ack && o.onCmd) { o.onCmd(c.id, c.c); } });
        }).catch(function (e) { if (st) pending = pending || st; throw e; });
      } else {
        p = fetch('/api/remote/state?c=' + encodeURIComponent(o.code) + '&k=' + encodeURIComponent(o.key) + '&seq=' + seq, { cache: 'no-store' }).then(function (r) { if (r.status === 404) { var e = new Error('gone'); e.status = 404; throw e; } return r.json(); }).then(function (d) {
          if (d.state && o.onState) { seq = d.seq; o.onState(d.state, d.seq); } else if (d.seq !== undefined) seq = d.seq;
          if (o.onHost) { var on = !!d.host_alive; if (on !== lastHost) { lastHost = on; o.onHost(on); } }
        });
      }
      p.then(function () { link(); }, function (e) { if (e && e.status === 404 && o.onGone) o.onGone(); }).then(function () { inflight = false; });
    }
    function startPolling() {
      if (closed || pollT) return;
      mode = 'poll'; link(); pollT = setInterval(pollOnce, o.pollMs || 350); pollOnce();
      if (!retryT) retryT = setInterval(function () { if (!wsOpen && !closed) { var old = ws; try { if (old) old.onclose = null; if (old) old.close(); } catch (e) {} fails = 0; openWs(); } }, 25000);
    }
    function stopPolling() { if (pollT) clearInterval(pollT); pollT = 0; if (retryT) clearInterval(retryT); retryT = 0; }

    // ---- what the pages call ----
    this.pushState = function (s) {   // host: the game state as a JSON string
      lastState = s; pending = s;
      if (wsOpen) { try { ws.send(JSON.stringify({ t: 'state', s: s })); pending = ''; } catch (e) {} }
    };
    this.done = function (id) {       // host: a command was carried out
      if (id > ack) ack = id;
      if (wsOpen) { try { ws.send(JSON.stringify({ t: 'done', id: id })); } catch (e) {} } else if (o.onAck) { /* polling: the phone learns from the next state */ }
    };
    this.cmd = function (c, cid) {    // phone: a command; the answer comes back through onSent(cid, {ok, id, delivered}) and later onAck(id)
      if (wsOpen) { try { ws.send(JSON.stringify({ t: 'cmd', c: c, cid: cid })); return; } catch (e) {} }
      post('/api/remote/cmd', { code: o.code, k: o.key, c: c }).then(function (d) { if (o.onSent) o.onSent(cid, d); }, function () { if (o.onSent) o.onSent(cid, { ok: false }); });
    };
    this.mode = function () { return wsOpen ? 'live' : mode === 'poll' ? 'poll' : 'wait'; };
    this.close = function () { closed = true; stopPing(); stopPolling(); try { if (ws) ws.close(); } catch (e) {} };
    if (/[?&]nows=1/.test(location.search)) startPolling(); else openWs();   // ?nows=1 forces the HTTP fallback (for testing / blocked networks)
    setTimeout(function () { if (!wsOpen && !pollT && !closed) { /* slow to connect: keep trying quietly */ link(); } }, 1500);
  }
  window.RcNet = RcNet;
})();
