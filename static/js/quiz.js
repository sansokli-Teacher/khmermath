/* "Test yourself" boxes on a lesson page: questions come from the JSON in #qz-data. */
(function () {
  'use strict';
  var node = document.getElementById('qz-data');
  var boxes = document.querySelectorAll('.qz');
  if (!node || !boxes.length) return;
  var data;
  try { data = JSON.parse(node.textContent); } catch (e) { return; }
  var KH = '០១២៣៤៥៦៧៨៩';
  var LEVEL = { easy: 'ងាយ', medium: 'មធ្យម', hard: 'ពិបាក', pisa: 'PISA' };
  var store = {};
  var key = 'qz:' + location.pathname;
  try { store = JSON.parse(localStorage.getItem(key) || '{}'); } catch (e) { store = {}; }
  function save() { try { localStorage.setItem(key, JSON.stringify(store)); } catch (e) { /* private mode: fine */ } }
  function kh(n) { return String(n).replace(/\d/g, function (d) { return KH[d]; }); }
  function el(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }
  function digits(s) {                       // "1 190", "1,190", "១១៩០ ក្បាល" -> 1190
    s = String(s).replace(/[០-៩]/g, function (d) { return KH.indexOf(d); });
    var neg = /^\s*[-−–]/.test(s);
    s = s.replace(/[^0-9]/g, '');
    return s === '' ? null : (neg ? -1 : 1) * parseInt(s, 10);
  }
  function math(root) {
    if (window.renderMathInElement) {
      window.renderMathInElement(root, { delimiters: [{ left: '\\(', right: '\\)', display: false }], throwOnError: false, strict: 'ignore' });
    }
  }

  function build(box) {
    var sec = box.getAttribute('data-sec');
    var qs = data.filter(function (q) { return q.sec === sec; });
    var list = box.querySelector('.qz-list');
    var score = box.querySelector('.qz-score');
    function tally() {
      var ok = 0, done = 0;
      qs.forEach(function (q) { var s = store[q.no]; if (s) { done++; if (s.ok) ok++; } });
      score.textContent = 'ត្រឹមត្រូវ ' + kh(ok) + ' / ' + kh(qs.length) + (done < qs.length ? ' · បានធ្វើ ' + kh(done) : ' ✓');
    }
    qs.forEach(function (q, i) {
      var item = el('div', 'qz-q');
      item.appendChild(el('div', 'qz-top', '<span class="qz-n">' + kh(i + 1) + '</span><span class="qz-lv qz-lv-' + q.level + '">' + LEVEL[q.level] + '</span>'));
      item.appendChild(el('p', 'qz-stem', q.stem));
      var body = el('div', 'qz-body');
      var input = null, choice = null;
      if (q.type === 'num') {
        var row = el('div', 'qz-row');
        input = el('input', 'qz-in'); input.type = 'text'; input.setAttribute('inputmode', 'numeric'); input.setAttribute('autocomplete', 'off');
        input.setAttribute('aria-label', 'ចម្លើយ'); input.placeholder = 'វាយចម្លើយ';
        row.appendChild(input);
        if (q.unit) row.appendChild(el('span', 'qz-unit', q.unit));
        body.appendChild(row);
      } else {
        var opts = q.type === 'tf' ? ['ពិត', 'មិនពិត'] : q.options;
        var grp = el('div', 'qz-opts'); grp.setAttribute('role', 'radiogroup');
        opts.forEach(function (t, k) {
          var lab = el('label', 'qz-opt');
          var r = el('input'); r.type = 'radio'; r.name = 'qz' + q.no; r.value = k;
          r.addEventListener('change', function () { choice = k; });
          lab.appendChild(r); lab.appendChild(el('span', 'qz-ot', t));
          grp.appendChild(lab);
        });
        body.appendChild(grp);
      }
      item.appendChild(body);
      var bar = el('div', 'qz-bar');
      var check = el('button', 'qz-btn qz-go', 'ពិនិត្យ'); check.type = 'button';
      var hintB = el('button', 'qz-btn qz-ghost', 'គន្លឹះ'); hintB.type = 'button';
      var retry = el('button', 'qz-btn qz-ghost', 'ធ្វើម្ដងទៀត'); retry.type = 'button'; retry.hidden = true;
      bar.appendChild(check); bar.appendChild(hintB); bar.appendChild(retry);
      item.appendChild(bar);
      var hint = el('div', 'qz-hint', '<b>គន្លឹះ៖</b> ' + q.hint); hint.hidden = true;
      var fb = el('div', 'qz-fb'); fb.hidden = true; fb.setAttribute('aria-live', 'polite');
      item.appendChild(hint); item.appendChild(fb);

      function lock(on) {
        item.querySelectorAll('input').forEach(function (x) { x.disabled = on; });
        check.hidden = on; retry.hidden = !on;
      }
      function show(ok) {
        item.classList.toggle('qz-ok', ok); item.classList.toggle('qz-bad', !ok);
        fb.innerHTML = '<b>' + (ok ? '✓ ត្រឹមត្រូវ' : '✗ មិនត្រឹមត្រូវ') + '</b>' +
          (ok ? '' : (q.type === 'num' ? ' · ចម្លើយ៖ <b>' + q.answer.toLocaleString('en').replace(/,/g, ' ') + (q.unit ? ' ' + q.unit : '') + '</b>' : '')) +
          '<div class="qz-sol"><b>ដំណោះស្រាយ៖</b> ' + q.sol + '</div>';
        fb.hidden = false; math(fb);
        lock(true);
      }
      function mark(opt) {   // after a choice, show which option was right
        var labs = item.querySelectorAll('.qz-opt');
        labs.forEach(function (l, k) { l.classList.toggle('qz-right', k === opt); });
      }
      check.addEventListener('click', function () {
        var ok;
        if (q.type === 'num') {
          var v = digits(input.value);
          if (v === null) { input.focus(); return; }
          ok = v === q.answer;
          store[q.no] = { ok: ok, v: input.value };
        } else {
          if (choice === null) return;
          var right = q.type === 'tf' ? (q.answer ? 0 : 1) : q.answer;
          ok = choice === right;
          mark(right);
          store[q.no] = { ok: ok, c: choice };
        }
        save(); show(ok); tally();
      });
      if (input) input.addEventListener('keydown', function (e) { if (e.key === 'Enter') check.click(); });
      hintB.addEventListener('click', function () { hint.hidden = !hint.hidden; });
      retry.addEventListener('click', function () {
        delete store[q.no]; save();
        item.classList.remove('qz-ok', 'qz-bad'); fb.hidden = true; lock(false);
        item.querySelectorAll('.qz-opt').forEach(function (l) { l.classList.remove('qz-right'); l.querySelector('input').checked = false; });
        choice = null; if (input) { input.value = ''; input.focus(); }
        tally();
      });
      // restore an earlier answer
      var s = store[q.no];
      if (s) {
        if (q.type === 'num') input.value = s.v || '';
        else { var rs = item.querySelectorAll('.qz-opt input'); if (rs[s.c]) rs[s.c].checked = true; choice = s.c; mark(q.type === 'tf' ? (q.answer ? 0 : 1) : q.answer); }
        show(s.ok);
      }
      list.appendChild(item);
    });
    var reset = box.querySelector('.qz-reset');
    if (reset && !box.__reset) {
      box.__reset = true;
      reset.addEventListener('click', function () {
        qs.forEach(function (q) { delete store[q.no]; }); save();
        list.innerHTML = ''; build(box);
      });
    }
    tally();
    math(list);
  }
  boxes.forEach(build);
})();
