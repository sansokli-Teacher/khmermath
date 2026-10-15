/* khmermath.org — «ប៊ីងហ្គោគណិតវិទ្យា» (play/bingo.html; the same file runs on exam.khmermath.org).
   The teacher picks lessons, a grid size and how many cards; every student gets a printed card of ANSWERS. The teacher calls the
   questions one by one on the projector, students solve and mark the answer on their card, and the teacher can check any card.
   Cards are generated from (seed, card number), so a card can always be re-created to check it. Nothing is stored on a server. */
(function () {
  'use strict';
  var $ = function (id) { return document.getElementById(id); };
  if (!$('bg')) return;
  var KEY = 'km_bingo_v1';
  var BANK_URLS = window.TG_URLS || ['https://exam.khmermath.org/api/game/bank', '../static/data/teamgame_g7.json'];
  var BANK = null, S = null;                           // S = the current session {seed, n, size, cards, lessons, order[], called[]}
  var khNum = function (n) { return String(n).replace(/\d/g, function (d) { return '០១២៣៤៥៦៧៨៩'[d]; }); };
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text !== undefined) e.textContent = text; return e; }
  function load(k, d) { try { var v = JSON.parse(localStorage.getItem(k)); return v === null ? d : v; } catch (e) { return d; } }
  function put(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  function typeset(node) { var go = function () { if (window.renderMathInElement) try { renderMathInElement(node, { delimiters: [{ left: '\\(', right: '\\)', display: false }], throwOnError: false }); } catch (e) {} }; if (window.renderMathInElement) go(); else window.addEventListener('load', go); }

  /* ---------- seeded random ---------- */
  function rng(seedStr) {
    var h = 1779033703 ^ seedStr.length;
    for (var i = 0; i < seedStr.length; i++) { h = Math.imul(h ^ seedStr.charCodeAt(i), 3432918353); h = (h << 13) | (h >>> 19); }
    var a = (h = Math.imul(h ^ (h >>> 16), 2246822507)) ^ (h >>> 13);
    return function () { a |= 0; a = (a + 0x6D2B79F5) | 0; var t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  }
  function shuffled(arr, r) { var a = arr.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(r() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  function newSeed() { return Math.random().toString(36).slice(2, 7).toUpperCase(); }

  /* ---------- the answers a bingo card can hold: short, distinct ---------- */
  function visibleLen(a) { return String(a || '').replace(/\\\(|\\\)/g, '').replace(/\\(text|frac|sqrt|times|div|leq|geq|circ)/g, 'x').replace(/[{}\\,]/g, '').length; }
  function norm(a) { return String(a || '').replace(/\\,|\\ |\s/g, ''); }
  function pool(lessons) {
    var out = [], seen = {};
    ((BANK && BANK.lessons) || []).forEach(function (L) {
      if (lessons.indexOf(L.n) < 0) return;
      L.qs.forEach(function (q, i) {
        var key = norm(q.a);
        if (!q.a || q.a === 'ពិត' || q.a === 'មិនពិត' || visibleLen(q.a) > 16 || seen[key]) return;
        seen[key] = 1; out.push({ id: L.n + ':' + i, q: q.q, a: q.a, f: q.f || '', o: q.o || null, s: q.s || '', n: L.n });
      });
    });
    return out;
  }

  /* ---------- a card = a seeded sample of the answers being called ---------- */
  function cardCells(sess, no, items) {
    var cells = sess.size * sess.size, free = sess.size % 2 === 1, r = rng(sess.seed + ':' + no);
    var pick = shuffled(sess.order, r).slice(0, free ? cells - 1 : cells), mid = (cells - 1) / 2, out = [];
    for (var i = 0, k = 0; i < cells; i++) out.push(free && i === mid ? { free: true } : { id: pick[k++] });
    return out;
  }
  function lines(size) {
    var L = [], i, j, d1 = [], d2 = [];
    for (i = 0; i < size; i++) { var row = [], col = []; for (j = 0; j < size; j++) { row.push(i * size + j); col.push(j * size + i); } L.push(row, col); d1.push(i * size + i); d2.push(i * size + (size - 1 - i)); }
    L.push(d1, d2); return L;
  }
  function itemById(items, id) { for (var i = 0; i < items.length; i++) if (items[i].id === id) return items[i]; return null; }

  function drawCard(sess, no, items, called, opts) {
    opts = opts || {};
    var card = el('div', 'bg-card'), head = el('div', 'bg-chead'), g = el('div', 'bg-grid g' + sess.size), cells = cardCells(sess, no, items), mark = {};
    head.appendChild(el('b', '', 'ប៊ីងហ្គោគណិតវិទ្យា')); head.appendChild(el('span', 'bg-no', 'កាត #' + no));
    card.appendChild(head);
    cells.forEach(function (c, i) {
      var cell = el('div', 'bg-cell');
      if (c.free) { cell.classList.add('free'); cell.textContent = '★'; if (opts.check) mark[i] = 1; }
      else { var it = itemById(items, c.id); cell.textContent = it ? it.a : '?'; if (it && it.a.length > 11) cell.classList.add('long'); if (opts.check && called.indexOf(c.id) >= 0) { cell.classList.add('hit'); mark[i] = 1; } }
      g.appendChild(cell);
    });
    card.appendChild(g);
    card.appendChild(el('div', 'bg-foot', 'គូសចម្លើយត្រឹមត្រូវ · បានមួយជួរ = ប៊ីងហ្គោ! · កូដ ' + sess.seed));
    var res = null;
    if (opts.check) {
      var win = lines(sess.size).filter(function (ln) { return ln.every(function (ix) { return mark[ix]; }); });
      res = { lines: win.length, full: Object.keys(mark).length === cells.length };
      win.forEach(function (ln) { ln.forEach(function (ix) { g.children[ix].classList.add('win'); }); });
    }
    typeset(card);
    return { node: card, res: res };
  }

  /* ---------- setup ---------- */
  function renderLessons() {
    var box = $('bg-lessons'); box.innerHTML = '';
    var ls = (BANK && BANK.lessons) || [];
    if (!ls.length) { box.appendChild(el('small', 'bg-hint', BANK === null ? 'កំពុងផ្ទុក…' : BANK.closed ? 'គ្រូបានបិទហ្គេមនេះជាបណ្តោះអាសន្ន។' : 'គ្រូមិនទាន់បើកមេរៀនណាមួយទេ។')); return; }
    var cfg = load(KEY + '_cfg', { lessons: [1] });
    var lastG = 0;
    ls.forEach(function (L) {
      if ((L.g || 7) !== lastG) { lastG = L.g || 7; var hd = el('h3', 'bg-grade', 'ថ្នាក់ទី ' + khNum(lastG)); box.appendChild(hd); }
      var lab = el('label', 'bg-lesson'), cb = el('input'); cb.type = 'checkbox'; cb.value = L.n; cb.checked = cfg.lessons.indexOf(L.n) >= 0; lab.classList.toggle('on', cb.checked);
      cb.addEventListener('change', function () { lab.classList.toggle('on', cb.checked); updateInfo(); });
      lab.appendChild(cb); lab.appendChild(el('b', '', 'មេរៀនទី ' + khNum(L.d || L.n))); lab.appendChild(el('span', '', L.title)); box.appendChild(lab);
    });
    updateInfo();
  }
  function chosen() { return Array.prototype.map.call($('bg-lessons').querySelectorAll('input:checked'), function (c) { return +c.value; }); }
  function updateInfo() {
    var size = +$('bg-size').value, items = pool(chosen()), need = size * size - (size % 2 ? 1 : 0), info = $('bg-info');
    $('bg-calls').max = items.length; var def = Math.min(items.length, Math.max(need + 6, Math.round(need * 1.6)));
    if (!+$('bg-calls').value || +$('bg-calls').value > items.length) $('bg-calls').value = def;
    info.textContent = 'សំណួរដែលអាចបង្កើតកាតបាន៖ ' + khNum(items.length) + (items.length < need + 2 ? ' — តិចពេក សូមជ្រើសមេរៀនបន្ថែម (ត្រូវការយ៉ាងតិច ' + khNum(need + 2) + ')' : '');
    $('bg-make').disabled = items.length < need + 2;
  }
  function make() {
    var size = +$('bg-size').value, lessons = chosen(), items = pool(lessons), need = size * size - (size % 2 ? 1 : 0);
    var calls = Math.max(need + 2, Math.min(items.length, +$('bg-calls').value || need + 6)), seed = newSeed(), r = rng(seed + ':pool');
    var order = shuffled(items.map(function (x) { return x.id; }), r).slice(0, calls);
    S = { seed: seed, size: size, n: Math.max(1, Math.min(100, +$('bg-n').value || 30)), lessons: lessons, order: order, called: [], at: 0, items: items.filter(function (x) { return order.indexOf(x.id) >= 0; }) };
    put(KEY + '_cfg', { lessons: lessons }); put(KEY, S); show('print');
  }

  /* ---------- views ---------- */
  var views = ['setup', 'print', 'call'];
  function show(v) {
    views.forEach(function (x) { $('bg-v-' + x).hidden = x !== v; });
    $('bg').classList.toggle('bg-live', v === 'call'); document.documentElement.classList.toggle('bg-noscroll', v === 'call');
    if (v === 'print') renderPrint(); if (v === 'call') renderCall();
    window.scrollTo(0, 0);
  }
  function renderPrint() {
    $('bg-printinfo').textContent = 'កាត ' + khNum(S.n) + ' សន្លឹក · តារាង ' + khNum(S.size) + '×' + khNum(S.size) + ' · សំណួរត្រូវហៅ ' + khNum(S.order.length) + ' · កូដ ' + S.seed;
    var box = $('bg-cards'); box.innerHTML = ''; box.className = 'bg-cards s' + S.size;
    for (var i = 1; i <= S.n; i++) box.appendChild(drawCard(S, i, S.items, [], {}).node);
  }
  function renderCall() {
    var cur = S.called.length ? itemById(S.items, S.called[S.called.length - 1]) : null, rest = S.order.length - S.called.length;
    $('bg-count').textContent = khNum(S.called.length) + ' / ' + khNum(S.order.length);
    var q = $('bg-q'); q.innerHTML = ''; $('bg-ans').hidden = true;
    if (cur) {
      q.appendChild(el('div', 'bg-qt', cur.q));
      if (cur.f) { var fg = el('div', 'bg-fig'); fg.innerHTML = cur.f; q.appendChild(fg); }
      if (cur.o) { var ol = el('div', 'bg-opts'); cur.o.forEach(function (o, k) { var d = el('div', 'bg-o'); d.appendChild(el('b', '', 'កខគឃ'[k])); d.appendChild(el('span', '', o)); ol.appendChild(d); }); q.appendChild(ol); }
      $('bg-ans').textContent = cur.a; if (cur.s) { var sl = el('div', 'bg-sol', cur.s); $('bg-ans').appendChild(sl); }
      typeset(q); typeset($('bg-ans'));
    } else q.appendChild(el('div', 'bg-qt', 'ចុច «សំណួរបន្ទាប់» ដើម្បីចាប់ផ្តើមហៅ។'));
    $('bg-show').hidden = !cur; $('bg-next').disabled = rest <= 0; $('bg-next').textContent = rest <= 0 ? '🏁 ហៅអស់ហើយ' : '▶ សំណួរបន្ទាប់';
    $('bg-undo').disabled = !S.called.length;
    var hist = $('bg-hist'); hist.innerHTML = '';
    S.called.slice().reverse().forEach(function (id, k) { var it = itemById(S.items, id), c = el('span', 'bg-chip' + (k === 0 ? ' now' : ''), it ? it.a : '?'); hist.appendChild(c); }); typeset(hist);
    $('bg-check-out').innerHTML = '';
  }
  function checkCard() {
    var no = parseInt($('bg-cardno').value, 10), out = $('bg-check-out'); out.innerHTML = '';
    if (!no || no < 1 || no > S.n) { out.appendChild(el('p', 'bg-hint', 'សូមបញ្ចូលលេខកាតពី ១ ដល់ ' + khNum(S.n))); return; }
    var d = drawCard(S, no, S.items, S.called, { check: true });
    var msg = d.res.full ? '🏆 ពេញតារាង!' : d.res.lines ? '🎉 ប៊ីងហ្គោ! (' + khNum(d.res.lines) + ' ជួរ)' : 'មិនទាន់ជា ប៊ីងហ្គោទេ';
    var t = el('div', 'bg-verdict ' + (d.res.lines ? 'ok' : 'no'), msg); out.appendChild(t); out.appendChild(d.node);
  }
  // Sound for the caller screen: music while calling, a "reveal" sting on each question, fanfare at the end (sfx.js, original tracks).
  var bgSnd = true; try { bgSnd = localStorage.getItem('bg_snd') !== '0'; } catch (e) {}
  function bgAudio(fn) { try { if (window.KmSound && bgSnd) fn(); } catch (e) {} }
  function next() {
    if (S.called.length >= S.order.length) return;
    S.called.push(S.order[S.called.length]); put(KEY, S); renderCall();
    bgAudio(function () { KmSound.unlock(); if (S.called.length >= S.order.length) { KmSound.stop(); KmSound.sfx('fanfare'); } else { KmSound.loop('lobby', 0.28); KmSound.sfx('reveal'); } });
  }
  (function () {
    var ctl = document.getElementById('bg-ctl') || (document.getElementById('bg-next') && document.getElementById('bg-next').parentNode);
    if (!ctl || !window.KmSound) return;
    var b = document.createElement('button'); b.type = 'button'; b.className = 'btn btn-ghost'; b.title = 'សំឡេង / តន្ត្រី';
    var paint = function () { b.textContent = bgSnd ? '🔊' : '🔇'; };
    b.addEventListener('click', function () { bgSnd = !bgSnd; try { localStorage.setItem('bg_snd', bgSnd ? '1' : '0'); } catch (e) {} if (!bgSnd) KmSound.stop(); else { KmSound.unlock(); KmSound.sfx('tick'); } paint(); });
    paint(); ctl.appendChild(b);
  })();

  /* ---------- wiring ---------- */
  $('bg-size').addEventListener('change', function () { $('bg-calls').value = ''; updateInfo(); });
  $('bg-calls').addEventListener('change', updateInfo);
  $('bg-make').addEventListener('click', make);
  $('bg-print').addEventListener('click', function () { window.print(); });
  $('bg-tocall').addEventListener('click', function () { show('call'); });
  $('bg-toprint').addEventListener('click', function () { show('print'); });
  $('bg-newgame').addEventListener('click', function () { try { if (window.KmSound) KmSound.stop(); } catch (e) {} show('setup'); });
  $('bg-next').addEventListener('click', next);
  $('bg-show').addEventListener('click', function () { $('bg-ans').hidden = !$('bg-ans').hidden; });
  $('bg-undo').addEventListener('click', function () { if (S.called.length) { S.called.pop(); put(KEY, S); renderCall(); } });
  $('bg-check').addEventListener('click', checkCard);
  $('bg-cardno').addEventListener('keydown', function (e) { if (e.key === 'Enter') checkCard(); });
  $('bg-full').addEventListener('click', function () { var st = $('bg'); if (document.fullscreenElement) document.exitFullscreen(); else if (st.requestFullscreen) st.requestFullscreen(); });
  $('bg-resume').addEventListener('click', function () { var s = load(KEY, null); if (!s) return; S = s; show(S.called.length ? 'call' : 'print'); });
  if (!document.fullscreenEnabled) $('bg-full').hidden = true;

  (function init() {
    var saved = load(KEY, null); $('bg-resume').hidden = !(saved && saved.order);
    var i = 0;
    (function nextUrl() {
      if (i >= BANK_URLS.length) { BANK = { lessons: [] }; renderLessons(); return; }
      fetch(BANK_URLS[i++], { cache: 'no-cache' }).then(function (r) { if (!r.ok) throw 0; return r.json(); }).then(function (d) {
        if (!d || !d.lessons) throw 0; BANK = d;
        if (!window.TG_NOGATE && d.games && d.games.bingo === false) { $('bg-v-setup').innerHTML = ''; $('bg-v-setup').appendChild(el('p', 'bg-hint', 'គ្រូបានបិទហ្គេមប៊ីងហ្គោជាបណ្តោះអាសន្ន។')); return; }
        renderLessons();
      }).catch(nextUrl);
    })();
  })();
})();
