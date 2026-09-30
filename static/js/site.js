/* khmermath.org — menus, mobile navigation, light/dark theme. */
(function () {
  'use strict';
  var body = document.body;
  var nav = document.getElementById('main-nav');
  var toggle = document.querySelector('.menu-toggle');
  var items = Array.prototype.slice.call(document.querySelectorAll('.nav-item.has-menu'));
  var desktop = window.matchMedia('(min-width: 961px)');
  var hover = window.matchMedia('(hover: hover)');

  function setOpen(item, open) {
    item.classList.toggle('open', open);
    var btn = item.querySelector('.nav-link');
    if (btn) btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  }
  function closeAll(except) {
    items.forEach(function (it) { if (it !== except) setOpen(it, false); });
  }

  items.forEach(function (item) {
    var btn = item.querySelector('.nav-link');
    var timer;
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      var open = !item.classList.contains('open');
      closeAll(item);
      setOpen(item, open);
    });
    // desktop: open on hover, with a short delay on leave so the pointer can cross the gap
    item.addEventListener('mouseenter', function () {
      if (!desktop.matches || !hover.matches) return;
      clearTimeout(timer);
      closeAll(item);
      setOpen(item, true);
    });
    item.addEventListener('mouseleave', function () {
      if (!desktop.matches || !hover.matches) return;
      timer = setTimeout(function () { setOpen(item, false); }, 140);
    });
  });

  document.addEventListener('click', function (e) {
    if (desktop.matches && !e.target.closest('.nav-item.has-menu')) closeAll();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    var open = items.filter(function (it) { return it.classList.contains('open'); })[0];
    if (open) { setOpen(open, false); open.querySelector('.nav-link').focus(); }
    else if (body.classList.contains('nav-open')) setMobile(false);
  });

  function setMobile(open) {
    body.classList.toggle('nav-open', open);
    if (toggle) toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    if (!open) closeAll();
  }
  if (toggle) toggle.addEventListener('click', function () { setMobile(!body.classList.contains('nav-open')); });
  if (nav) nav.addEventListener('click', function (e) {
    if (e.target.closest('a') && !desktop.matches) setMobile(false);
  });
  desktop.addEventListener('change', function () { setMobile(false); closeAll(); });

  // theme: the choice is remembered on this device only
  var root = document.documentElement;
  var themeBtn = document.querySelector('.theme-toggle');
  if (themeBtn) themeBtn.addEventListener('click', function () {
    var dark = root.getAttribute('data-theme') === 'dark' ||
      (!root.getAttribute('data-theme') && window.matchMedia('(prefers-color-scheme: dark)').matches);
    var next = dark ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem('km-theme', next); } catch (err) { /* storage unavailable */ }
  });
})();
