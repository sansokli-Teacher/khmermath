/* Textbook lessons: maths and the "in this lesson" menu. */
(function () {
  'use strict';
  var paper = document.querySelector('.ls-paper') || document.querySelector('.legend');
  if (window.renderMathInElement && paper) {
    window.renderMathInElement(paper, {
      delimiters: [
        { left: '\\[', right: '\\]', display: true },
        { left: '\\(', right: '\\)', display: false },
      ],
      macros: { '\\arc': '\\overset{\\frown}{#1}', '\\overparen': '\\overset{\\frown}{#1}' },
      throwOnError: false,
      strict: 'ignore',
    });
  }

  // mark the section being read, and keep it visible in the menu without moving the page
  var links = Array.prototype.slice.call(document.querySelectorAll('.ls-toc a'));
  if (!links.length || !('IntersectionObserver' in window)) return;
  var byId = {};
  links.forEach(function (a) { byId[a.getAttribute('href').slice(1)] = a; });
  var heads = links.map(function (a) { return document.getElementById(a.getAttribute('href').slice(1)); }).filter(Boolean);
  var obs = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (!en.isIntersecting || !byId[en.target.id]) return;
      links.forEach(function (a) { a.classList.remove('here'); });
      var a = byId[en.target.id];
      a.classList.add('here');
      var list = a.closest('.ls-toc');
      if (window.matchMedia('(max-width: 960px)').matches) {
        list.scrollLeft = a.parentNode.offsetLeft - 12;
      } else {
        var box = a.closest('.ls-side-box');
        if (a.offsetTop < box.scrollTop || a.offsetTop + a.offsetHeight > box.scrollTop + box.clientHeight) {
          box.scrollTop = a.offsetTop - box.clientHeight / 2;
        }
      }
    });
  }, { rootMargin: '-15% 0px -75% 0px' });
  heads.forEach(function (h) { obs.observe(h); });
})();
