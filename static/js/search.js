/* khmermath.org — site search. One small index file (static/data/search.json) is fetched the first time the box is opened. */
(function () {
  'use strict';
  var script = document.currentScript, root = new URL('../../', script.src).href, idx = null, loading = null, ov = null, input, list, active = -1, shown = [];
  var norm = function (s) { return String(s || '').toLowerCase().replace(/[​\s]+/g, ' ').trim(); };
  function load() { if (idx) return Promise.resolve(); if (!loading) loading = fetch(root + 'static/data/search.json').then(function (r) { return r.json(); }).then(function (d) { idx = d.map(function (p) { p.n = norm(p.t + ' ' + p.d + ' ' + p.h + ' ' + p.x); p.nt = norm(p.t); return p; }); }); return loading; }
  function score(p, terms) {
    var s = 0;
    for (var i = 0; i < terms.length; i++) { var t = terms[i]; if (p.n.indexOf(t) < 0) return 0; s += p.nt.indexOf(t) >= 0 ? 10 : (p.h && norm(p.h).indexOf(t) >= 0 ? 4 : 1); }
    return s;
  }
  function snippet(p, term) { var k = norm(p.x).indexOf(term); if (k < 0) return p.d || ''; var x = norm(p.x); return (k > 30 ? '…' : '') + x.slice(Math.max(0, k - 30), k + 90) + '…'; }
  function run() {
    var q = norm(input.value); list.innerHTML = ''; shown = []; active = -1;
    if (q.length < 1) { list.innerHTML = '<p class="srch-hint">វាយពាក្យដើម្បីស្វែងរក — មេរៀន រូបមន្ត សំណង់ ល្បែង…</p>'; return; }
    var terms = q.split(' ');
    shown = idx.map(function (p) { return { p: p, s: score(p, terms) }; }).filter(function (r) { return r.s > 0; }).sort(function (a, b) { return b.s - a.s; }).slice(0, 12);
    if (!shown.length) { list.innerHTML = '<p class="srch-hint">រកមិនឃើញលទ្ធផលទេ។</p>'; return; }
    shown.forEach(function (r, i) {
      var a = document.createElement('a'); a.href = root + r.p.u; a.className = 'srch-item'; a.setAttribute('role', 'option');
      var t = document.createElement('b'); t.textContent = r.p.t; var s = document.createElement('small'); s.textContent = snippet(r.p, terms[0]); var k = document.createElement('em'); k.textContent = r.p.k;
      a.appendChild(k); a.appendChild(t); a.appendChild(s); list.appendChild(a);
    });
  }
  function open() {
    if (!ov) {
      ov = document.createElement('div'); ov.className = 'srch'; ov.hidden = true;
      ov.innerHTML = '<div class="srch-box" role="dialog" aria-label="ស្វែងរក"><div class="srch-row"><input type="search" class="srch-input" placeholder="ស្វែងរកមេរៀន រូបមន្ត…" autocomplete="off"><button type="button" class="srch-x" aria-label="បិទ">✕</button></div><div class="srch-list" role="listbox"></div></div>';
      document.body.appendChild(ov); input = ov.querySelector('input'); list = ov.querySelector('.srch-list');
      ov.addEventListener('click', function (e) { if (e.target === ov || e.target.classList.contains('srch-x')) close(); });
      input.addEventListener('input', function () { load().then(run); });
      input.addEventListener('keydown', function (e) {
        var items = list.querySelectorAll('.srch-item');
        if (e.key === 'ArrowDown' || e.key === 'ArrowUp') { e.preventDefault(); if (!items.length) return; active = (active + (e.key === 'ArrowDown' ? 1 : -1) + items.length) % items.length; items.forEach(function (x, i) { x.classList.toggle('on', i === active); }); items[active].scrollIntoView({ block: 'nearest' }); }
        else if (e.key === 'Enter' && items.length) { location.href = (items[active] || items[0]).href; }
        else if (e.key === 'Escape') close();
      });
    }
    ov.hidden = false; document.documentElement.classList.add('srch-lock'); input.value = ''; list.innerHTML = '<p class="srch-hint">កំពុងផ្ទុក…</p>'; input.focus(); load().then(run);
  }
  function close() { ov.hidden = true; document.documentElement.classList.remove('srch-lock'); }
  document.addEventListener('click', function (e) { var b = e.target.closest && e.target.closest('.search-toggle'); if (b) { e.preventDefault(); open(); } });
  document.addEventListener('keydown', function (e) { if ((e.key === '/' && !/input|textarea|select/i.test((e.target.tagName || ''))) || ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k')) { e.preventDefault(); open(); } });
})();
