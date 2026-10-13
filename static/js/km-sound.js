/* khmermath.org — sound for the construction animations (the pages of construct/ and the apps of construct/apps/).
   Made with the Web Audio API, no files. The pages need no change: this script listens to what the animation does.
   - pencil / compass drawing  : a soft scratch while the figure changes (arcs, lines, moving tools), a small "tok" when it stops
   - a point or a mark appears : a short "pop"
   - a step button is pressed  : a wooden "tick"
   The sound waits for the first click (browsers require it) and can be muted with the 🔊 button; the choice is kept
   (localStorage 'km-sound', the same key as the spinner and the dice). */
(function () {
  'use strict';
  var on = true;
  try { on = localStorage.getItem('km-sound') !== '0'; } catch (e) { /* no storage */ }
  var ctx = null, master = null, scratch = null, held = false, lastPop = 0, burstStart = 0, burstEnd = 0, endTimer = 0, decayTimer = 0;

  function ac() {
    if (!on) return null;
    try {
      if (!ctx) {
        var A = window.AudioContext || window.webkitAudioContext;
        if (!A) return null;
        ctx = new A(); master = ctx.createGain(); master.gain.value = .5; master.connect(ctx.destination);
      }
      if (ctx.state === 'suspended') ctx.resume();
      return ctx;
    } catch (e) { return null; }
  }
  function env(g, t, a, peak, d) {
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(Math.max(peak, 0.0002), t + a);
    g.gain.exponentialRampToValueAtTime(0.0001, t + a + d);
  }
  function tone(f, d, v, type, f2) {
    var c = ac(); if (!c) return;
    var t = c.currentTime, o = c.createOscillator(), g = c.createGain();
    o.type = type || 'sine'; o.frequency.setValueAtTime(f, t);
    if (f2) o.frequency.exponentialRampToValueAtTime(f2, t + d);
    env(g, t, .004, v, d); o.connect(g); g.connect(master); o.start(t); o.stop(t + d + .05);
  }
  function tap(f, v) {                       // a short dull knock, like a pencil on wood
    var c = ac(); if (!c) return;
    var t = c.currentTime, n = Math.floor(c.sampleRate * .035), b = c.createBuffer(1, n, c.sampleRate), x = b.getChannelData(0);
    for (var i = 0; i < n; i++) x[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / n, 3);
    var s = c.createBufferSource(); s.buffer = b;
    var fl = c.createBiquadFilter(); fl.type = 'bandpass'; fl.frequency.value = f; fl.Q.value = 2.2;
    var g = c.createGain(); g.gain.value = v; s.connect(fl); fl.connect(g); g.connect(master); s.start(t);
  }
  function startScratch() {
    var c = ac(); if (!c || scratch) return;
    var n = c.sampleRate * 2, b = c.createBuffer(1, n, c.sampleRate), x = b.getChannelData(0), p = 0;
    for (var i = 0; i < n; i++) { var w = Math.random() * 2 - 1; p = .55 * p + w; x[i] = p * .5; }   // a little darker than white noise
    var s = c.createBufferSource(); s.buffer = b; s.loop = true;
    var fl = c.createBiquadFilter(); fl.type = 'bandpass'; fl.frequency.value = 2600; fl.Q.value = .7;
    var g = c.createGain(); g.gain.value = 0;
    s.connect(fl); fl.connect(g); g.connect(master); s.start();
    scratch = { g: g, f: fl };
  }
  function scratchTo(level) {
    if (!scratch || !ctx) return;
    var t = ctx.currentTime;
    scratch.g.gain.cancelScheduledValues(t);
    scratch.g.gain.setTargetAtTime(level, t, .025);
    if (level > 0) scratch.f.frequency.setTargetAtTime(2000 + Math.random() * 2400, t, .05);
  }

  /* what the animation does to the figure */
  var obs = new MutationObserver(function (list) {
    if (!on || held || document.hidden) return;
    var w = 0, pops = 0;
    for (var i = 0; i < list.length; i++) {
      var r = list[i], tg = r.target;
      if (r.type === 'attributes') {
        if (tg.ownerSVGElement || tg.nodeName === 'svg') w++;
      } else if (r.type === 'childList' && (tg.ownerSVGElement || tg.nodeName === 'svg' || tg.namespaceURI === 'http://www.w3.org/2000/svg')) {
        w += r.addedNodes.length;
        for (var j = 0; j < r.addedNodes.length; j++) {
          var a = r.addedNodes[j];
          if (a.nodeName === 'circle' && a.getAttribute && +a.getAttribute('r') > 0 && +a.getAttribute('r') < 9) pops++;
        }
      }
    }
    if (!w) return;
    var now = performance.now();
    if (!burstStart || now - burstEnd > 500) burstStart = now;
    burstEnd = now;
    startScratch();
    if (ctx) { scratchTo(Math.min(.32, .09 + w * .008)); }
    clearTimeout(decayTimer); decayTimer = setTimeout(function () { scratchTo(0); }, 140);
    clearTimeout(endTimer);
    endTimer = setTimeout(function () { if (burstEnd - burstStart > 350) tap(900, .5); burstStart = 0; }, 420);
    if (pops && now - lastPop > 90) { lastPop = now; tone(520, .09, .16, 'sine', 700); }
  });

  /* gestures: unlock the sound, tick on the step buttons, no scratch while a finger or the mouse is dragging */
  var AREA = '.cx, .al, .app-container, .cx-board, .cx-side';
  document.addEventListener('pointerdown', function (e) { ac(); held = true; scratchTo(0); }, true);
  document.addEventListener('pointerup', function () { held = false; }, true);
  document.addEventListener('pointercancel', function () { held = false; }, true);
  document.addEventListener('keydown', function () { ac(); }, true);
  document.addEventListener('click', function (e) {
    var t = e.target;
    if (!t.closest || !t.closest(AREA) || t.id === 'kmSnd') return;
    if (t.closest('button, [role=tab], [role=button], .cx-steps li, .step-chip, summary, a.btn')) { ac(); tap(1300, .8); tone(740, .05, .05, 'triangle'); }
  }, true);

  function mount() {
    var b = document.createElement('button');
    b.type = 'button'; b.id = 'kmSnd';
    var framed = window.parent !== window;
    b.style.cssText = 'position:fixed;z-index:60;' + (framed ? 'top:6px;right:6px;' : 'bottom:14px;left:14px;') +
      'width:42px;height:42px;border-radius:50%;border:1.5px solid rgba(0,0,0,.22);background:rgba(255,255,255,.92);font-size:20px;line-height:1;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,.15)';
    function paint() { b.textContent = on ? '🔊' : '🔇'; b.setAttribute('aria-label', on ? 'បិទសំឡេង' : 'បើកសំឡេង'); b.title = on ? 'បិទសំឡេង' : 'បើកសំឡេង'; }
    paint();
    b.addEventListener('click', function (e) {
      e.stopPropagation();
      on = !on; try { localStorage.setItem('km-sound', on ? '1' : '0'); } catch (x) { /* no storage */ }
      paint(); if (on) { ac(); tap(1300, .8); } else scratchTo(0);
    });
    document.body.appendChild(b);
  }
  function start() {
    mount();
    obs.observe(document.body, { subtree: true, childList: true, attributes: true, attributeFilter: ['d', 'points', 'x', 'y', 'x1', 'y1', 'x2', 'y2', 'cx', 'cy', 'r', 'rx', 'ry', 'width', 'height', 'transform', 'stroke-dashoffset', 'stroke-dasharray', 'opacity'] });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
