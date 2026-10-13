/* khmermath.org — soft sound for the construction animations (the pages of construct/ and the apps of construct/apps/).
   Made with the Web Audio API, no files. The pages need no change: this script listens to what the animation does.
   The sound is OFF until the student presses the speaker button (the choice is kept in localStorage 'km-sound' = '1').
   - a line or arc being drawn  : a very soft brush of air that follows the drawing
   - a point / mark appears     : one gentle marimba note (pentatonic, so it never sounds wrong)
   - the drawing finishes       : a slightly longer marimba note
   - a step button is pressed   : a quiet wood-block tick
   A little reverb and a low-pass filter keep everything round, never sharp. */
(function () {
  'use strict';
  var on = false;
  try { on = localStorage.getItem('km-sound') === '1'; } catch (e) { /* no storage */ }
  var ctx = null, master = null, dry = null, wet = null, air = null, held = false;
  var lastNote = 0, burstStart = 0, burstEnd = 0, endTimer = 0, quietTimer = 0, noteI = 0;
  var SCALE = [523.25, 587.33, 659.25, 783.99, 880, 1046.5, 1174.7];            // C major pentatonic: C D E G A C D

  function ac() {
    if (!on) return null;
    try {
      if (!ctx) {
        var A = window.AudioContext || window.webkitAudioContext;
        if (!A) return null;
        ctx = new A();
        var lp = ctx.createBiquadFilter(); lp.type = 'lowpass'; lp.frequency.value = 5200; lp.Q.value = .5;
        var comp = ctx.createDynamicsCompressor(); comp.threshold.value = -18; comp.ratio.value = 4;
        master = ctx.createGain(); master.gain.value = .55;
        dry = ctx.createGain(); dry.gain.value = .85; wet = ctx.createGain(); wet.gain.value = .22;
        var rv = ctx.createConvolver(), n = Math.floor(ctx.sampleRate * 1.1), buf = ctx.createBuffer(2, n, ctx.sampleRate);
        for (var c = 0; c < 2; c++) { var d = buf.getChannelData(c); for (var i = 0; i < n; i++) d[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / n, 3); }
        rv.buffer = buf;
        master.connect(dry); master.connect(rv); rv.connect(wet);
        dry.connect(lp); wet.connect(lp); lp.connect(comp); comp.connect(ctx.destination);
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
  function note(f, d, v) {                                     // a marimba-like pluck: a soft sine with a quiet overtone
    var c = ac(); if (!c) return;
    var t = c.currentTime;
    [[1, 1], [4, .18]].forEach(function (p) {
      var o = c.createOscillator(), g = c.createGain();
      o.type = 'sine'; o.frequency.value = f * p[0];
      env(g, t, .006, v * p[1], d / p[0] * (p[0] === 1 ? 1 : .5));
      o.connect(g); g.connect(master); o.start(t); o.stop(t + d + .1);
    });
  }
  function woodTick(v) {
    var c = ac(); if (!c) return;
    var t = c.currentTime, o = c.createOscillator(), g = c.createGain();
    o.type = 'sine'; o.frequency.setValueAtTime(760, t); o.frequency.exponentialRampToValueAtTime(520, t + .05);
    env(g, t, .003, v, .07); o.connect(g); g.connect(master); o.start(t); o.stop(t + .12);
  }
  function startAir() {
    var c = ac(); if (!c || air) return;
    var n = c.sampleRate * 3, b = c.createBuffer(1, n, c.sampleRate), x = b.getChannelData(0), p = 0;
    for (var i = 0; i < n; i++) { p = .985 * p + (Math.random() * 2 - 1) * .12; x[i] = p; }           // brown-ish noise: soft, no hiss
    var s = c.createBufferSource(); s.buffer = b; s.loop = true;
    var fl = c.createBiquadFilter(); fl.type = 'lowpass'; fl.frequency.value = 1500; fl.Q.value = .4;
    var g = c.createGain(); g.gain.value = 0;
    s.connect(fl); fl.connect(g); g.connect(master); s.start();
    air = g;
  }
  function airTo(level, tc) {
    if (!air || !ctx) return;
    var t = ctx.currentTime;
    air.gain.cancelScheduledValues(t); air.gain.setTargetAtTime(level, t, tc || .12);
  }
  function nextNote() { noteI = (noteI + 1 + Math.floor(Math.random() * 2)) % SCALE.length; return SCALE[noteI]; }

  /* what the animation does to the figure */
  var DRAW = { d: 1, points: 1, x2: 1, y2: 1, 'stroke-dashoffset': 1, 'stroke-dasharray': 1 };
  var obs = new MutationObserver(function (list) {
    if (!on || held || document.hidden) return;
    var w = 0, adds = 0;
    for (var i = 0; i < list.length; i++) {
      var r = list[i], tg = r.target;
      if (r.type === 'attributes') {
        if (tg.ownerSVGElement || tg.nodeName === 'svg') w += DRAW[r.attributeName] ? 1 : .25;
      } else if (r.type === 'childList' && (tg.ownerSVGElement || tg.nodeName === 'svg' || tg.namespaceURI === 'http://www.w3.org/2000/svg')) {
        for (var j = 0; j < r.addedNodes.length; j++) {
          var a = r.addedNodes[j];
          if (a.nodeName === 'circle' && a.getAttribute && +a.getAttribute('r') > 0 && +a.getAttribute('r') < 9) adds++;
          w += .5;
        }
      }
    }
    if (w < .5) return;
    var now = performance.now();
    if (!burstStart || now - burstEnd > 600) burstStart = now;
    burstEnd = now;
    startAir();
    airTo(Math.min(.06, .014 + w * .0015), .09);                        // very quiet and smooth
    clearTimeout(quietTimer); quietTimer = setTimeout(function () { airTo(0, .1); }, 200);
    clearTimeout(endTimer);
    endTimer = setTimeout(function () {
      if (burstEnd - burstStart > 450) note(nextNote(), .9, .13);       // the drawing is done
      burstStart = 0;
    }, 520);
    if (adds && now - lastNote > 380) { lastNote = now; note(nextNote(), .5, .11); }
  });

  /* gestures: nothing plays before the first click; no brush sound while a finger or the mouse is dragging */
  var AREA = '.cx, .al, .app-container, .cx-board, .cx-side';
  document.addEventListener('pointerdown', function () { ac(); held = true; airTo(0, .05); }, true);
  document.addEventListener('pointerup', function () { held = false; }, true);
  document.addEventListener('pointercancel', function () { held = false; }, true);
  document.addEventListener('click', function (e) {
    var t = e.target;
    if (!on || !t.closest || !t.closest(AREA) || t.id === 'kmSnd') return;
    if (t.closest('button, [role=tab], [role=button], .cx-steps li, .step-chip, summary, a.btn')) { ac(); woodTick(.07); }
  }, true);

  function mount() {
    var b = document.createElement('button');
    b.type = 'button'; b.id = 'kmSnd';
    var framed = window.parent !== window;
    b.style.cssText = 'position:fixed;z-index:60;' + (framed ? 'top:6px;right:6px;' : 'bottom:14px;left:14px;') +
      'min-width:42px;height:40px;padding:0 12px;border-radius:20px;border:1.5px solid rgba(0,0,0,.22);background:rgba(255,255,255,.94);color:#132238;font:700 14px system-ui,sans-serif;line-height:1;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,.15)';
    function paint() {
      b.textContent = on ? '🔊' : '🔇 បើកសំឡេង';
      b.setAttribute('aria-label', on ? 'បិទសំឡេង' : 'បើកសំឡេង'); b.title = on ? 'បិទសំឡេង' : 'បើកសំឡេង';
    }
    paint();
    b.addEventListener('click', function (e) {
      e.stopPropagation();
      on = !on; try { localStorage.setItem('km-sound', on ? '1' : '0'); } catch (x) { /* no storage */ }
      paint();
      if (on) { ac(); note(659.25, .6, .12); } else airTo(0, .05);
    });
    document.body.appendChild(b);
  }
  function start() {
    mount();
    obs.observe(document.body, { subtree: true, childList: true, attributes: true, attributeFilter: ['d', 'points', 'x', 'y', 'x1', 'y1', 'x2', 'y2', 'cx', 'cy', 'r', 'rx', 'ry', 'width', 'height', 'transform', 'stroke-dashoffset', 'stroke-dasharray', 'opacity'] });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
