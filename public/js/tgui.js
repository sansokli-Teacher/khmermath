/* ហ្គេមក្រុម — the simple setup screen: picture cards for the game style, a +/- team stepper, question-count chips and a
   one-line summary beside the big Start button. It only drives the existing form fields, so all the game logic stays in teamgame.js. */
(function () {
  'use strict';
  var $ = function (id) { return document.getElementById(id); };
  if (!$('gx-styles')) return;
  var KH = '០១២៣៤៥៦៧៨៩', kh = function (n) { return String(n).replace(/\d/g, function (d) { return KH[d]; }); };
  var NAME = { cards: 'កាតបើក', wheel: 'កង់វិល', boat: 'ប្រណាំងទូកង' };
  function fire(el) { el.dispatchEvent(new Event('change', { bubbles: true })); }

  // style picture cards
  var styleSel = $('tg-style'), styleBtns = Array.prototype.slice.call(document.querySelectorAll('.gx-style'));
  styleBtns.forEach(function (b) { b.addEventListener('click', function () { if (b.disabled) return; styleSel.value = b.getAttribute('data-style'); fire(styleSel); sync(); }); });

  // team stepper
  var nIn = $('tg-nteams');
  function setN(v) { nIn.value = Math.max(2, Math.min(8, v)); fire(nIn); sync(); }
  $('gx-minus').addEventListener('click', function () { setN((parseInt(nIn.value, 10) || 4) - 1); });
  $('gx-plus').addEventListener('click', function () { setN((parseInt(nIn.value, 10) || 4) + 1); });

  // question-count chips + a box for any number
  var qn = $('tg-qn'), qc = $('gx-qcustom');
  qc.addEventListener('input', function () {
    var v = parseInt(qc.value, 10); if (!(v >= 1)) return; v = Math.min(200, v); var o = Array.prototype.filter.call(qn.options, function (x) { return x.value === String(v); })[0];
    if (!o) { o = document.createElement('option'); o.value = String(v); o.textContent = kh(v) + ' សំណួរ'; qn.insertBefore(o, qn.options[qn.options.length - 1]); }
    qn.value = String(v); fire(qn); sync();
  });
  Array.prototype.forEach.call($('gx-qn').querySelectorAll('button'), function (b) { b.addEventListener('click', function () { qn.value = b.getAttribute('data-v'); fire(qn); sync(); }); });

  function selectedLessons() { return document.querySelectorAll('#tg-lessons .tg-lesson.on').length; }
  function sync() {
    var st = styleSel.value;
    styleBtns.forEach(function (b) {
      var opt = Array.prototype.filter.call(styleSel.options, function (o) { return o.value === b.getAttribute('data-style'); })[0];
      b.disabled = !!(opt && opt.disabled); b.classList.toggle('on', b.getAttribute('data-style') === st); b.setAttribute('aria-pressed', b.getAttribute('data-style') === st ? 'true' : 'false');
    });
    var nt = $('tg-noteam').checked; $('gx-stepper').style.display = nt ? 'none' : ''; $('tg-teamlist').hidden = nt;
    $('gx-n').textContent = kh(nIn.value || 4);
    if (nt && styleSel.value !== 'cards') { styleSel.value = 'cards'; fire(styleSel); }
    styleBtns.forEach(function (b) { if (nt && b.getAttribute('data-style') !== 'cards') { b.disabled = true; b.title = 'ត្រូវការយ៉ាងតិចពីរក្រុម'; } else b.title = ''; });
    var std = Array.prototype.some.call($('gx-qn').children, function (b) { return b.getAttribute && b.getAttribute('data-v') === qn.value; }); if (document.activeElement !== qc) qc.value = std ? '' : (qn.value === '0' ? '' : qn.value);
    Array.prototype.forEach.call($('gx-qn').children, function (b) { if (b.getAttribute('data-v') !== null) b.classList.toggle('on', b.getAttribute('data-v') === qn.value); });
    $('gx-finishrow').hidden = st !== 'boat';
    var cls = $('tg-class'); if (cls && cls.parentNode) cls.parentNode.hidden = cls.options.length <= 1;
    var custom = document.querySelector('input[name="tg-mode"]:checked');
    var parts = [NAME[st] || '', nt ? 'គ្មានក្រុម' : kh(nIn.value || 4) + ' ក្រុម'];
    if (custom && custom.value === 'custom') { var c = $('tg-cards') ? $('tg-cards').children.length : 0; parts.push(kh(c) + ' កាត'); }
    else { parts.push('មេរៀន ' + kh(selectedLessons())); parts.push(qn.value === '0' ? 'សំណួរទាំងអស់' : kh(qn.value) + ' សំណួរ'); }
    $('gx-sum').textContent = parts.join(' · ');
  }
  var setup = $('tg-setup');
  ['click', 'change', 'input'].forEach(function (ev) { setup.addEventListener(ev, function () { setTimeout(sync, 0); }); });
  new MutationObserver(function () { sync(); }).observe(styleSel, { attributes: true, subtree: true, attributeFilter: ['disabled'] });
  new MutationObserver(function () { sync(); }).observe($('tg-lessons'), { childList: true, subtree: true, attributes: true, attributeFilter: ['class'] });
  sync();
})();
