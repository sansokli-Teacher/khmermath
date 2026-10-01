/* Formula books: maths, search, lesson menu, print. */
(function () {
  'use strict';
  var main = document.querySelector('.fx-main');
  if (!main) return;

  if (window.renderMathInElement) {
    window.renderMathInElement(main, {
      delimiters: [
        { left: '\\[', right: '\\]', display: true },
        { left: '\\(', right: '\\)', display: false },
      ],
      macros: { '\\arc': '\\overset{\\frown}{#1}', '\\overparen': '\\overset{\\frown}{#1}' },
      throwOnError: false,
      strict: 'ignore',
    });
  }

  // A formula in a line of text that is wider than its place and cannot break (one long integral)
  // would push the page sideways on a phone: it becomes a strip that scrolls on its own. Inside a
  // narrow column beside a picture (.mp) the book lets a formula run over, and so does the page.
  function fitMaths() {
    Array.prototype.forEach.call(main.querySelectorAll('.mi'), function (m) {
      if (m.classList.contains('mi-wide') || m.closest('.mp')) return;
      var box = m.parentElement.getBoundingClientRect();
      var over = Array.prototype.some.call(m.getClientRects(), function (r) { return r.right > box.right + 1; });
      if (over) m.classList.add('mi-wide');
    });
  }
  fitMaths();
  var fitTimer;
  window.addEventListener('resize', function () { clearTimeout(fitTimer); fitTimer = setTimeout(fitMaths, 200); });

  // search: show the topics whose text (Khmer or English, formulas included) contains the words typed
  var input = document.getElementById('fx-q');
  var lessons = Array.prototype.slice.call(main.querySelectorAll('.fx-lesson'));
  var tocItems = Array.prototype.slice.call(document.querySelectorAll('.fx-toc li'));
  var empty = main.querySelector('.fx-empty');
  var norm = function (t) { return t.replace(/[​‌‍]/g, '').toLowerCase(); };
  var index = lessons.map(function (l) {
    return {
      lesson: l,
      title: norm(l.querySelector('.fx-lh').textContent),
      topics: Array.prototype.slice.call(l.querySelectorAll('.fx-topic')).map(function (t) {
        return { el: t, text: norm(t.textContent) };
      }),
    };
  });
  var timer;
  function search() {
    var words = norm(input.value).split(/\s+/).filter(Boolean);
    var any = false;
    index.forEach(function (L, k) {
      var titleHit = words.length && words.every(function (w) { return L.title.indexOf(w) >= 0; });
      var shown = 0;
      L.topics.forEach(function (t) {
        var hit = !words.length || titleHit || words.every(function (w) { return t.text.indexOf(w) >= 0; });
        t.el.hidden = !hit;
        if (hit) shown++;
      });
      L.lesson.hidden = shown === 0;
      if (tocItems[k]) tocItems[k].classList.toggle('dim', shown === 0);
      if (shown) any = true;
    });
    if (empty) empty.hidden = any;
  }
  if (input) input.addEventListener('input', function () { clearTimeout(timer); timer = setTimeout(search, 120); });

  // lesson menu: mark the lesson being read
  var links = Array.prototype.slice.call(document.querySelectorAll('.fx-toc a'));
  if (links.length && 'IntersectionObserver' in window) {
    var byId = {};
    links.forEach(function (a) { byId[a.getAttribute('href').slice(1)] = a; });
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting || !byId[en.target.id]) return;
        links.forEach(function (a) { a.classList.remove('here'); });
        var a = byId[en.target.id];
        a.classList.add('here');
        // keep the marked lesson visible inside the menu box, without moving the page
        var box = a.closest('.fx-toc');
        var desk = !window.matchMedia('(max-width: 960px)').matches;
        if (desk && (a.offsetTop < box.scrollTop || a.offsetTop + a.offsetHeight > box.scrollTop + box.clientHeight)) {
          box.scrollTop = a.offsetTop - box.clientHeight / 2;
        } else if (!desk) {
          box.querySelector('ol').scrollLeft = a.parentNode.offsetLeft - 12;
        }
      });
    }, { rootMargin: '-20% 0px -70% 0px' });
    lessons.forEach(function (l) { obs.observe(l); });
  }

  var printBtn = document.querySelector('.fx-print');
  if (printBtn) printBtn.addEventListener('click', function () { window.print(); });
})();
