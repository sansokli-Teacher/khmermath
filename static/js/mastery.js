/* Mastery marks, on this device only (nothing is sent anywhere).
   quiz.js writes km_mastery_v1 {lesson path: {pct, ok, total}} when a student finishes a lesson's check.
   Here: the "next lesson" button says what is still needed (a soft gate: it always stays clickable), the lesson list
   shows a trophy on mastered lessons, and the step tracker at the top of a lesson ticks the steps already done.
   Add ?teacher=1 to a link to see every lesson as open. */
(function () {
  'use strict';
  var PASS = 0.8, KH = '០១២៣៤៥៦៧៨៩';
  var me = document.currentScript, root = '/';
  try { root = new URL('../../', me.src).pathname; } catch (e) { /* keep '/' */ }
  var teacher = /[?&]teacher=1\b/.test(location.search);
  function kh(n) { return String(n).replace(/\d/g, function (d) { return KH[d]; }); }
  function relOf(href) {
    var u; try { u = new URL(href, location.href); } catch (e) { return null; }
    if (u.origin !== location.origin) return null;
    var p = u.pathname.indexOf(root) === 0 ? u.pathname.slice(root.length) : u.pathname.replace(/^\//, '');
    return p.replace(/index\.html$/, '');
  }
  function load() { try { return JSON.parse(localStorage.getItem('km_mastery_v1') || '{}'); } catch (e) { return {}; } }
  var hasQuiz = !!document.getElementById('qz-data');

  function apply() {
    var all = load(), here = relOf(location.href), mine = all[here];

    // 1) the "next lesson" button
    var next = document.querySelector('.ls-pager a.next');
    if (next && hasQuiz && !teacher) {
      var old = next.querySelector('.ls-gate'); if (old) old.remove();
      next.classList.remove('ls-open', 'ls-wait');
      var note = document.createElement('span'); note.className = 'ls-gate';
      if (mine && mine.pct >= PASS) { next.classList.add('ls-open'); note.textContent = '🏆 បំពេញរួច ' + kh(Math.round(mine.pct * 100)) + '%'; }
      else { next.classList.add('ls-wait'); note.textContent = '🔒 ត្រូវការ ៨០% លើសំណួរពិនិត្យ · អាចរំលងបាន'; }
      next.appendChild(note);
    }

    // 2) trophies on the lesson list
    document.querySelectorAll('a.ls-card').forEach(function (a) {
      var m = all[relOf(a.getAttribute('href'))];
      var old = a.querySelector('.ls-trophy'); if (old) old.remove();
      if (m && m.pct >= PASS) { var t = document.createElement('span'); t.className = 'ls-trophy'; t.title = 'បំពេញមេរៀនហើយ'; t.textContent = '🏆'; a.appendChild(t); }
    });

    // 3) the step tracker
    var steps = document.querySelectorAll('.km-steps [data-step]');
    steps.forEach(function (li) {
      var k = li.getAttribute('data-step');
      if (k === 'quiz') li.classList.toggle('done', !!(mine && mine.pct >= PASS));
    });
  }
  apply();
  window.addEventListener('km-mastery', apply);
  window.addEventListener('storage', apply);
})();
