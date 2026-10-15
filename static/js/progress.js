/* khmermath.org — remembers, on this device only, which lessons, formula books, games and constructions a student has opened.
   Nothing is sent anywhere. Also registers the offline service worker. */
(function () {
  'use strict';
  var script = document.currentScript, root = new URL('../../', script.src).pathname, KEY = 'km_progress_v1', data = { seen: {}, last: null };
  try { var d = JSON.parse(localStorage.getItem(KEY)); if (d && d.seen) data = d; } catch (e) {}
  var rel = location.pathname.indexOf(root) === 0 ? location.pathname.slice(root.length) : location.pathname.replace(/^\//, '');
  rel = rel.replace(/index\.html$/, '');
  function save() { try { localStorage.setItem(KEY, JSON.stringify(data)); } catch (e) {} }
  var tracked = /^(lesson|formular|play|construct)\//.test(rel) && !/^(lesson|formular|play|construct)\/(g\d+\/)?$/.test(rel) || /^(play|construct)\/[\w-]+\.html$/.test(rel);
  if (tracked && !/^play\/index\.html$/.test(rel)) {
    data.seen[rel] = Date.now();
    if (/^lesson\//.test(rel)) data.last = { u: rel, t: (document.title || rel).replace(/\s*[—|-]\s*KhmerMath.*$/, ''), at: Date.now() };
    save();
  }
  // tick the links that were already opened
  function mark() {
    var as = document.querySelectorAll('main a[href]');
    for (var i = 0; i < as.length; i++) {
      var a = as[i], u; try { u = new URL(a.getAttribute('href'), location.href); } catch (e) { continue; }
      if (u.origin !== location.origin) continue;
      var p = u.pathname.indexOf(root) === 0 ? u.pathname.slice(root.length) : u.pathname.replace(/^\//, ''); p = p.replace(/index\.html$/, '');
      if (data.seen[p] && !a.querySelector('.km-done') && /^(lesson|formular|play|construct)\//.test(p)) { var s = document.createElement('span'); s.className = 'km-done'; s.title = 'បានបើកអានរួច'; s.textContent = '✓'; a.appendChild(s); }
    }
  }
  mark();
  // home page: "continue where you stopped"
  var slot = document.getElementById('km-continue');
  if (slot && data.last) { var a = document.createElement('a'); a.className = 'btn btn-primary'; a.href = root + data.last.u; a.textContent = '▶ បន្តមេរៀនចុងក្រោយ៖ ' + data.last.t; slot.appendChild(a); slot.hidden = false; }
  var n = Object.keys(data.seen).filter(function (k) { return /^lesson\//.test(k); }).length, c = document.getElementById('km-count'); if (c && n) { c.textContent = 'អ្នកបានបើកមេរៀន ' + String(n).replace(/\d/g, function (d) { return '០១២៣៤៥៦៧៨៩'[d]; }) + ' រួចហើយ'; }
  // offline: pages already visited keep working without internet
  if ('serviceWorker' in navigator && location.protocol === 'https:') navigator.serviceWorker.register(root + 'sw.js').catch(function () {});
})();
