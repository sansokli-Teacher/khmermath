// Student side of the live quiz (phones). One file for exam.khmermath.org/live and khmermath.org/play/live.html:
// window.LIVE_API is '' on the exam site and 'https://exam.khmermath.org' on khmermath.org.
(function () {
  'use strict';
  var $ = function (id) { return document.getElementById(id); };
  if (!$('lv')) return;
  var API = window.LIVE_API || '', SK = 'km_live_v1', me = null, st = null, recvAt = 0, timerId = 0, pollId = 0, lastKey = '', sent = {};
  var khNum = function (n) { return String(n).replace(/\d/g, function (d) { return '០១២៣៤៥៦៧៨៩'[d]; }); };
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text !== undefined) e.textContent = text; return e; }
  function typeset(node) { var go = function () { if (window.renderMathInElement) try { renderMathInElement(node, { delimiters: [{ left: '\\(', right: '\\)', display: false }], throwOnError: false }); } catch (e) {} }; if (window.renderMathInElement) go(); else window.addEventListener('load', go); }
  function api(path, body) {
    var opt = body ? { method: 'POST', body: JSON.stringify(body) } : {};      // text/plain (no custom header) keeps cross-site requests free of a preflight
    return fetch(API + path, opt).then(function (r) { return r.json().catch(function () { return {}; }).then(function (d) { if (!r.ok) { var e = new Error(d.error || 'error'); e.status = r.status; throw e; } return d; }); });
  }
  function show(v) { ['join', 'play'].forEach(function (x) { $('lv-' + x).hidden = x !== v; }); }
  function saveMe() { try { sessionStorage.setItem(SK, JSON.stringify(me)); } catch (e) {} }

  /* ---------- join ---------- */
  $('lv-go').addEventListener('click', function () {
    var code = $('lv-code').value.replace(/\D/g, ''), name = $('lv-name').value.trim(), msg = $('lv-msg');
    msg.textContent = '';
    if (code.length !== 6) { msg.textContent = 'សូមបញ្ចូលលេខកូដ ៦ ខ្ទង់។'; return; }
    if (!name) { msg.textContent = 'សូមបញ្ចូលឈ្មោះរបស់អ្នក។'; return; }
    $('lv-go').disabled = true;
    api('/api/live/join', { code: code, name: name }).then(function (d) { me = { code: code, pid: d.pid, token: d.token, name: d.name }; saveMe(); start(); })
      .catch(function (e) { msg.textContent = e.message; }).then(function () { $('lv-go').disabled = false; });
  });
  $('lv-leave').addEventListener('click', function () { try { sessionStorage.removeItem(SK); } catch (e) {} me = null; clearTimeout(pollId); clearInterval(timerId); show('join'); });

  /* ---------- play ---------- */
  function start() { show('play'); lastKey = ''; poll(); }
  function poll() {
    clearTimeout(pollId);
    api('/api/live/state?code=' + me.code + '&pid=' + me.pid + '&token=' + me.token).then(function (d) { st = d; recvAt = performance.now(); $('lv-net').hidden = true; render(); })
      .catch(function (e) { if (e.status === 404) { try { sessionStorage.removeItem(SK); } catch (x) {} me = null; show('join'); $('lv-msg').textContent = 'បន្ទប់នេះបានបិទហើយ។'; return; } $('lv-net').hidden = false; })
      .then(function () { if (me) pollId = setTimeout(poll, st && st.phase === 'question' && !st.answered ? 900 : 1600); });
  }
  function remaining() { return Math.max(0, st.left - (performance.now() - recvAt)); }
  function tick() {
    if (!st || st.phase !== 'question') return;
    var r = remaining(); $('lv-time').textContent = khNum(Math.ceil(r / 1000)); $('lv-bar').style.width = (100 * r / (st.secs * 1000)) + '%';
    $('lv-bar').classList.toggle('hot', r < 6000);
  }
  function render() {
    $('lv-who').textContent = me.name + ' · ' + khNum(st.score) + ' ពិន្ទុ';
    var body = $('lv-body'), key = st.phase + ':' + st.qi + ':' + (st.answered ? 1 : 0) + ':' + (st.reveal ? 1 : 0);
    if (key === lastKey) { tick(); return; }                 // nothing visible changed: keep the screen (and the typed answer) as it is
    lastKey = key; body.innerHTML = ''; clearInterval(timerId); $('lv-timer').hidden = st.phase !== 'question';
    if (st.phase === 'lobby') {
      body.appendChild(el('div', 'lv-big', '✓')); body.appendChild(el('h2', '', 'អ្នកបានចូលរួមហើយ!')); body.appendChild(el('p', 'lv-sub', 'រង់ចាំគ្រូចាប់ផ្តើមហ្គេម… មានអ្នកលេង ' + khNum(st.players) + ' នាក់'));
    } else if (st.phase === 'question') {
      var hd = el('div', 'lv-qn', 'សំណួរ ' + khNum(st.qi + 1) + ' / ' + khNum(st.total)); body.appendChild(hd);
      var q = el('div', 'lv-q', st.q.q); body.appendChild(q);
      if (st.q.f) { var f = el('div', 'lv-fig'); f.innerHTML = st.q.f; body.appendChild(f); }
      if (st.answered) { body.appendChild(el('div', 'lv-big', '✔')); body.appendChild(el('h2', '', 'បានផ្ញើចម្លើយ')); body.appendChild(el('p', 'lv-sub', 'រង់ចាំអ្នកដទៃ និងលទ្ធផល…')); }
      else if (st.q.k === 'mcq') { var g = el('div', 'lv-opts'); st.q.o.forEach(function (o, i) { var b = el('button', 'lv-opt c' + i); b.type = 'button'; b.appendChild(el('b', '', 'កខគឃចឆជ'[i])); b.appendChild(el('span', '', o)); b.addEventListener('click', function () { send(String(i)); }); g.appendChild(b); }); body.appendChild(g); }
      else if (st.q.k === 'tf') { var g2 = el('div', 'lv-opts two'); [['T', 'ពិត', 'c1'], ['F', 'មិនពិត', 'c0']].forEach(function (x) { var b = el('button', 'lv-opt ' + x[2], x[1]); b.type = 'button'; b.addEventListener('click', function () { send(x[0]); }); g2.appendChild(b); }); body.appendChild(g2); }
      else { var row = el('div', 'lv-num'), inp = el('input'); inp.type = 'text'; inp.setAttribute('inputmode', 'decimal'); inp.placeholder = 'វាយចម្លើយជាលេខ'; var b3 = el('button', 'lv-send', 'ផ្ញើ'); b3.type = 'button'; b3.addEventListener('click', function () { if (inp.value.trim()) send(inp.value.trim()); }); inp.addEventListener('keydown', function (e) { if (e.key === 'Enter') b3.click(); }); row.appendChild(inp); row.appendChild(b3); body.appendChild(row); }
      typeset(body); tick(); timerId = setInterval(tick, 250);
    } else if (st.phase === 'reveal') {
      var r = st.reveal; body.appendChild(el('div', 'lv-big ' + (r.right ? 'ok' : 'no'), r.right ? '✔' : (st.answered ? '✖' : '⏱')));
      body.appendChild(el('h2', '', r.right ? 'ត្រឹមត្រូវ! +' + khNum(r.pts) : (st.answered ? 'មិនត្រឹមត្រូវ' : 'អស់ពេលហើយ')));
      var ans = el('div', 'lv-ans'); ans.appendChild(el('small', '', 'ចម្លើយត្រឹមត្រូវ')); ans.appendChild(el('div', 'lv-ansv', r.show)); if (r.sol) ans.appendChild(el('div', 'lv-sol', r.sol)); body.appendChild(ans);
      body.appendChild(el('p', 'lv-sub', 'ចំណាត់ថ្នាក់ទី ' + khNum(st.rank) + ' ក្នុង ' + khNum(st.players) + ' នាក់')); typeset(body);
    } else if (st.phase === 'end') {
      body.appendChild(el('div', 'lv-big', st.rank <= 3 ? ['🥇', '🥈', '🥉'][st.rank - 1] : '🎉')); body.appendChild(el('h2', '', 'ហ្គេមបានបញ្ចប់!'));
      body.appendChild(el('p', 'lv-sub', 'អ្នកទទួលបាន ' + khNum(st.score) + ' ពិន្ទុ · ចំណាត់ថ្នាក់ទី ' + khNum(st.rank) + ' ក្នុង ' + khNum(st.players) + ' នាក់'));
      var tp = el('ol', 'lv-top'); (st.top || []).forEach(function (p) { var li = el('li'); li.appendChild(el('span', '', p.name)); li.appendChild(el('b', '', khNum(p.score))); tp.appendChild(li); }); body.appendChild(tp);
    }
  }
  function send(choice) {
    var k = st.qi; if (sent[k]) return; sent[k] = 1; st.answered = true; lastKey = ''; render();
    api('/api/live/answer', { code: me.code, pid: me.pid, token: me.token, qi: k, choice: choice }).catch(function (e) { if (e.status !== 409) { sent[k] = 0; } });
  }

  /* ---------- start ---------- */
  var c = /[?&]c=(\d{6})/.exec(location.search); if (c) $('lv-code').value = c[1];
  try { var saved = JSON.parse(sessionStorage.getItem(SK)); if (saved && saved.pid) { me = saved; start(); } } catch (e) {}
})();
