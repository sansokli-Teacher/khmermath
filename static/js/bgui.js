/* ប៊ីងហ្គោ — simple setup: size and card-count chips plus a one-line summary. Drives the existing fields only. */
(function () {
  'use strict';
  var $ = function (id) { return document.getElementById(id); };
  if (!$('bgx-sizes')) return;
  var KH = '០១២៣៤៥៦៧៨៩', kh = function (n) { return String(n).replace(/\d/g, function (d) { return KH[d]; }); };
  var size = $('bg-size'), nIn = $('bg-n');
  function fire(el) { el.dispatchEvent(new Event('change', { bubbles: true })); el.dispatchEvent(new Event('input', { bubbles: true })); }
  Array.prototype.forEach.call($('bgx-sizes').children, function (b) { b.addEventListener('click', function () { size.value = b.getAttribute('data-v'); fire(size); sync(); }); });
  Array.prototype.forEach.call($('bgx-n').children, function (b) { b.addEventListener('click', function () { nIn.value = b.getAttribute('data-v'); fire(nIn); sync(); }); });
  function sync() {
    Array.prototype.forEach.call($('bgx-sizes').children, function (b) { b.classList.toggle('on', b.getAttribute('data-v') === size.value); });
    Array.prototype.forEach.call($('bgx-n').children, function (b) { b.classList.toggle('on', b.getAttribute('data-v') === String(nIn.value)); });
    var lessons = document.querySelectorAll('#bg-lessons .bg-lesson.on').length, s = size.value;
    $('bgx-sum').textContent = 'តារាង ' + kh(s) + '×' + kh(s) + ' · ' + kh(nIn.value || 0) + ' កាត · មេរៀន ' + kh(lessons);
    $('bg-make').disabled = $('bg-make').disabled;   // the page script decides when there are too few answers
  }
  var root = $('bg-v-setup');
  ['click', 'change', 'input'].forEach(function (ev) { root.addEventListener(ev, function () { setTimeout(sync, 0); }); });
  new MutationObserver(sync).observe($('bg-lessons'), { childList: true, subtree: true, attributes: true, attributeFilter: ['class'] });
  sync();
})();
