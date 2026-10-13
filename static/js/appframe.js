/* khmermath.org — the frame of a page of content/construct/apps/: the app tells the page its height. */
(function () {
  'use strict';
  var f = document.querySelector('.app-frame');
  if (!f) return;
  addEventListener('message', function (e) {
    if (!e.data || typeof e.data.kmFrameH !== 'number' || e.source !== f.contentWindow) return;
    f.style.height = Math.min(Math.max(e.data.kmFrameH, 320), 4000) + 'px';
  });
})();
