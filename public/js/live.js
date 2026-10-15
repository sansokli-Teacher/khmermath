// Student side of the live quiz (phones). One file for exam.khmermath.org/live and khmermath.org/play/live.html:
// window.LIVE_API is '' on the exam site and 'https://exam.khmermath.org' on khmermath.org.
// Two modes (chosen by the teacher when the room is made): classic = the teacher runs every question; solo = each student goes at their own pace.
(function () {
  'use strict';
  var $ = function (id) { return document.getElementById(id); };
  if (!$('lv')) return;
  var API = window.LIVE_API || '', SK = 'km_live_v1', me = null, st = null, recvAt = 0, timerId = 0, pollId = 0, lastKey = '', sent = {}, fsTried = false;
  var SHAPES = ['▲', '◆', '●', '■', '★', '⬟'];
  var khNum = function (n) { return String(n).replace(/\d/g, function (d) { return '០១២៣៤៥៦៧៨៩'[d]; }); };
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text !== undefined) e.textContent = text; return e; }
  function typeset(node) { var go = function () { if (window.renderMathInElement) try { renderMathInElement(node, { delimiters: [{ left: '\\(', right: '\\)', display: false }], throwOnError: false }); } catch (e) {} }; if (window.renderMathInElement) go(); else window.addEventListener('load', go); }
  function api(path, body) {
    var opt = body ? { method: 'POST', body: JSON.stringify(body) } : {};      // text/plain (no custom header) keeps cross-site requests free of a preflight
    return fetch(API + path, opt).then(function (r) { return r.json().catch(function () { return {}; }).then(function (d) { if (!r.ok) { var e = new Error(d.error || 'error'); e.status = r.status; throw e; } return d; }); });
  }
  function saveMe() { try { sessionStorage.setItem(SK, JSON.stringify(me)); } catch (e) {} }

  /* ---------- full-screen game mode: nothing of the page around it is shown ---------- */
  function setFull(on) {
    $('lv').classList.toggle('lv-full', on); document.documentElement.classList.toggle('lv-lock', on); document.body.classList.toggle('lv-lock', on);
    $('lv-join').hidden = on; $('lv-play').hidden = !on;
    if (on && !fsTried) { fsTried = true; var d = document.documentElement; try { (d.requestFullscreen || d.webkitRequestFullscreen || function () { return Promise.reject(); }).call(d, { navigationUI: 'hide' }); } catch (e) {} }
    if (!on) { try { if (document.fullscreenElement) document.exitFullscreen(); } catch (e) {} fsTried = false; }
  }

  /* ---------- join ---------- */
  function join() {
    var code = $('lv-code').value.replace(/\D/g, ''), name = $('lv-name').value.trim(), msg = $('lv-msg');
    msg.textContent = '';
    if (code.length !== 6) { msg.textContent = 'សូមបញ្ចូលលេខកូដ ៦ ខ្ទង់។'; return; }
    if (!name) { msg.textContent = 'សូមបញ្ចូលឈ្មោះរបស់អ្នក។'; return; }
    $('lv-go').disabled = true;
    api('/api/live/join', { code: code, name: name }).then(function (d) { me = { code: code, pid: d.pid, token: d.token, name: d.name }; saveMe(); start(); })
      .catch(function (e) { msg.textContent = e.message; }).then(function () { $('lv-go').disabled = false; });
  }
  $('lv-go').addEventListener('click', join);
  $('lv-name').addEventListener('keydown', function (e) { if (e.key === 'Enter') join(); });
  $('lv-leave').addEventListener('click', function () { if (!confirm('ចាកចេញពីហ្គេម?')) return; try { sessionStorage.removeItem(SK); } catch (e) {} me = null; clearTimeout(pollId); clearInterval(timerId); setFull(false); });

  /* ---------- play ---------- */
  function start() { setFull(true); lastKey = ''; st = null; poll(); }
  function poll() {
    clearTimeout(pollId);
    api('/api/live/state?code=' + me.code + '&pid=' + me.pid + '&token=' + me.token).then(function (d) { st = d; recvAt = performance.now(); $('lv-net').hidden = true; render(); })
      .catch(function (e) { if (e.status === 404) { try { sessionStorage.removeItem(SK); } catch (x) {} me = null; setFull(false); $('lv-msg').textContent = 'បន្ទប់នេះបានបិទហើយ។'; return; } $('lv-net').hidden = false; })
      .then(function () { if (me) pollId = setTimeout(poll, st && st.mode === 'solo' ? (st.phase === 'question' ? 4000 : 6000) : (st && st.phase === 'question' && !st.answered ? 900 : 1600)); });
  }
  function remaining() { return Math.max(0, st.left - (performance.now() - recvAt)); }
  function tick() {
    if (!st || st.phase !== 'question') return;
    var r = remaining(); $('lv-time').textContent = khNum(Math.ceil(r / 1000)); $('lv-bar').style.width = (100 * r / (st.secs * 1000)) + '%';
    $('lv-bar').classList.toggle('hot', r < 6000);
    if (r <= 0 && st.mode === 'solo' && !st.answered && !tick.asked) { tick.asked = true; setTimeout(poll, 1700); }   // let the server record the timeout
  }
  function render() {
    $('lv-score').textContent = khNum(st.score);
    $('lv-qn').textContent = st.phase === 'lobby' || st.phase === 'end' || st.phase === 'open' ? me.name : khNum(st.qi + 1) + '/' + khNum(st.total);
    var body = $('lv-body'), key = st.phase + ':' + st.qi + ':' + (st.answered ? 1 : 0) + ':' + (st.reveal ? 1 : 0);
    if (key === lastKey) { tick(); return; }                 // nothing visible changed: keep the screen (and the typed answer) as it is
    lastKey = key; tick.asked = false; body.innerHTML = ''; clearInterval(timerId);
    $('lv-timer').classList.toggle('off', st.phase !== 'question');
    $('lv-bar').style.width = '100%'; $('lv-bar').classList.remove('hot');
    var stage = el('div', 'lv-stage'), ans = el('div', 'lv-answers');
    body.appendChild(stage); body.appendChild(ans);
    if (st.phase === 'lobby') {
      stage.appendChild(el('div', 'lv-emoji', '✓')); stage.appendChild(el('h2', '', 'អ្នកបានចូលរួមហើយ!')); stage.appendChild(el('p', 'lv-sub', 'រង់ចាំគ្រូចាប់ផ្តើមហ្គេម… មានអ្នកលេង ' + khNum(st.players) + ' នាក់'));
    } else if (st.phase === 'question') {
      var q = el('div', 'lv-q', st.q.q); stage.appendChild(q);
      if (st.q.f) { var f = el('div', 'lv-fig'); f.innerHTML = st.q.f; stage.appendChild(f); }
      if (st.answered) { stage.appendChild(el('div', 'lv-emoji', '✔')); stage.appendChild(el('p', 'lv-sub', 'បានផ្ញើចម្លើយ — រង់ចាំអ្នកដទៃ…')); }
      else if (st.q.k === 'mcq') { ans.classList.add(st.q.o.length > 4 ? 'g6' : 'g4'); st.q.o.forEach(function (o, i) { var b = el('button', 'lv-opt c' + i); b.type = 'button'; b.appendChild(el('i', '', SHAPES[i])); b.appendChild(el('span', '', o)); b.addEventListener('click', function () { send(String(i)); }); ans.appendChild(b); }); }
      else if (st.q.k === 'tf') { ans.classList.add('g2'); [['T', 'ពិត', 'c1', '✓'], ['F', 'មិនពិត', 'c0', '✕']].forEach(function (x) { var b = el('button', 'lv-opt ' + x[2]); b.type = 'button'; b.appendChild(el('i', '', x[3])); b.appendChild(el('span', '', x[1])); b.addEventListener('click', function () { send(x[0]); }); ans.appendChild(b); }); }
      else { ans.classList.add('gnum'); var inp = el('input'); inp.type = 'text'; inp.setAttribute('inputmode', 'decimal'); inp.setAttribute('autocomplete', 'off'); inp.placeholder = 'វាយចម្លើយជាលេខ'; var b3 = el('button', 'lv-send', 'ផ្ញើ'); b3.type = 'button'; b3.addEventListener('click', function () { if (inp.value.trim()) send(inp.value.trim()); }); inp.addEventListener('keydown', function (e) { if (e.key === 'Enter') b3.click(); }); ans.appendChild(inp); ans.appendChild(b3); }
      timerId = setInterval(tick, 250);
    } else if (st.phase === 'reveal') {
      var r = st.reveal;
      stage.appendChild(el('div', 'lv-emoji ' + (r.right ? 'ok' : 'no'), r.right ? '✔' : (r.timeout || !r.mine ? '⏱' : '✖')));
      stage.appendChild(el('h2', '', r.right ? 'ត្រឹមត្រូវ! +' + khNum(r.pts) : (r.timeout || !r.mine ? 'អស់ពេលហើយ' : 'មិនត្រឹមត្រូវ')));
      var a = el('div', 'lv-ans'); a.appendChild(el('small', '', 'ចម្លើយត្រឹមត្រូវ')); a.appendChild(el('div', 'lv-ansv', r.show)); if (r.sol) a.appendChild(el('div', 'lv-sol', r.sol)); stage.appendChild(a);
      stage.appendChild(el('p', 'lv-sub', 'ចំណាត់ថ្នាក់ទី ' + khNum(st.rank) + ' ក្នុង ' + khNum(st.players) + ' នាក់'));
      if (st.mode === 'solo') { ans.classList.add('gone'); var nb = el('button', 'lv-send big', st.qi + 1 >= st.total ? '🏆 មើលលទ្ធផល' : 'សំណួរបន្ទាប់ ▶'); nb.type = 'button'; nb.addEventListener('click', function () { nb.disabled = true; api('/api/live/next', { code: me.code, pid: me.pid, token: me.token }).catch(function () {}).then(function () { sent = {}; poll(); }); }); ans.appendChild(nb); }
    } else if (st.phase === 'end') {
      stage.appendChild(el('div', 'lv-emoji', st.rank <= 3 ? ['🥇', '🥈', '🥉'][st.rank - 1] : '🎉')); stage.appendChild(el('h2', '', 'ហ្គេមបានបញ្ចប់!'));
      stage.appendChild(el('p', 'lv-sub', 'អ្នកទទួលបាន ' + khNum(st.score) + ' ពិន្ទុ · ចំណាត់ថ្នាក់ទី ' + khNum(st.rank) + ' ក្នុង ' + khNum(st.players) + ' នាក់'));
      var tp = el('ol', 'lv-top'); (st.top || []).forEach(function (p) { var li = el('li'); li.appendChild(el('span', '', p.name)); li.appendChild(el('b', '', khNum(p.score))); tp.appendChild(li); }); stage.appendChild(tp);
      if (st.mode === 'solo') { stage.appendChild(el('p', 'lv-sub small', 'ចំណាត់ថ្នាក់នឹងបន្តផ្លាស់ប្តូរ នៅពេលមិត្តភក្តិលេងចប់។')); }
    }
    typeset(body); tick();
  }
  function send(choice) {
    var k = st.qi; if (sent[k]) return; sent[k] = 1; st.answered = true; lastKey = '';
    api('/api/live/answer', { code: me.code, pid: me.pid, token: me.token, qi: k, choice: choice })
      .then(function () { if (st.mode === 'solo') poll(); })
      .catch(function (e) { if (e.status !== 409) { sent[k] = 0; st.answered = false; lastKey = ''; render(); } else if (st.mode === 'solo') poll(); });
    if (st.mode === 'solo') { var o = $('lv-body'); o.innerHTML = ''; o.appendChild(el('div', 'lv-stage')).appendChild(el('div', 'lv-emoji', '…')); } else render();
  }

  /* ---------- start ---------- */
  var c = /[?&]c=(\d{6})/.exec(location.search); if (c) $('lv-code').value = c[1];
  try { var nm = sessionStorage.getItem('km_live_name'); if (nm) { $('lv-name').value = nm; } } catch (e) {}
  try { var saved = JSON.parse(sessionStorage.getItem(SK)); if (saved && saved.pid && (!c || saved.code === c[1])) { me = saved; start(); } } catch (e) {}
})();
