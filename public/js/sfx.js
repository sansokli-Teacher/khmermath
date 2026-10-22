// Sound for games & quiz: ONE single unified Main music track and sound effects made with Web Audio (no external audio files, works offline).
// KmSound.loop("main"|vol), KmSound.stop(), KmSound.sfx(name), KmSound.toggle().
(function (g) {
  'use strict';
  var ctx = null, master = null, fx = null, muted = false, cur = null, timer = 0, nextT = 0, step = 0, vol = 1;
  try { muted = localStorage.getItem('km_snd_muted') === '1'; } catch (e) {}
  var hz = function (m) { return 440 * Math.pow(2, (m - 69) / 12); };
  function ensure() {
    if (!ctx) {
      var C = window.AudioContext || window.webkitAudioContext;
      if (!C) return null;
      ctx = new C();
      master = ctx.createGain();
      master.gain.value = muted ? 0 : 0.55;
      master.connect(ctx.destination);
      var dl = ctx.createDelay(1), fb = ctx.createGain(), wet = ctx.createGain();
      dl.delayTime.value = 0.32;
      fb.gain.value = 0.3;
      wet.gain.value = 0.35;
      fx = ctx.createGain();
      fx.connect(dl);
      dl.connect(fb);
      fb.connect(dl);
      dl.connect(wet);
      wet.connect(master);
    }
    if (ctx.state === 'suspended') ctx.resume();
    return ctx;
  }
  function tone(f, t, d, type, v, f2, echo, lp) {
    var o = ctx.createOscillator(), gn = ctx.createGain(), out = gn;
    o.type = type;
    o.frequency.setValueAtTime(f, t);
    if (f2) o.frequency.exponentialRampToValueAtTime(f2, t + d);
    gn.gain.setValueAtTime(0.0001, t);
    gn.gain.exponentialRampToValueAtTime(v, t + 0.012);
    gn.gain.exponentialRampToValueAtTime(0.0001, t + d);
    if (lp) {
      var fl = ctx.createBiquadFilter();
      fl.type = 'lowpass';
      fl.frequency.value = lp;
      gn.connect(fl);
      out = fl;
    }
    o.connect(gn);
    out.connect(master);
    if (echo && fx) out.connect(fx);
    o.start(t);
    o.stop(t + d + 0.03);
  }
  var noiseBuf = null;
  function noise(t, d, v, hp) {
    if (!noiseBuf) {
      noiseBuf = ctx.createBuffer(1, ctx.sampleRate * 0.5, ctx.sampleRate);
      var a = noiseBuf.getChannelData(0);
      for (var i = 0; i < a.length; i++) a[i] = Math.random() * 2 - 1;
    }
    var s = ctx.createBufferSource(), f = ctx.createBiquadFilter(), gn = ctx.createGain();
    s.buffer = noiseBuf;
    f.type = 'highpass';
    f.frequency.value = hp;
    gn.gain.setValueAtTime(v, t);
    gn.gain.exponentialRampToValueAtTime(0.0001, t + d);
    s.connect(f);
    f.connect(gn);
    gn.connect(master);
    s.start(t);
    s.stop(t + d + 0.02);
  }
  function kick(t, v) { tone(150, t, 0.16, 'sine', v, 45); }

  // The ONE signature Main quiz-show theme: warm chord progression + rounded bass + arpeggios + uplifting melody + gentle groove.
  var HOOK_MAIN = [
    81,0,0,81,0,84,0,81, 0,79,0,0,76,0,79,0,
    77,0,0,77,0,81,0,77, 0,76,0,0,72,0,76,0,
    79,0,0,79,0,84,0,79, 0,76,0,0,72,0,76,0,
    74,0,0,74,0,79,0,83, 0,86,0,0,83,0,79,0
  ];
  var MAIN_TRACK = {
    bpm: 130,
    root: [45, 41, 48, 43],
    tri: [[57, 60, 64], [57, 60, 65], [60, 64, 67], [59, 62, 67]],
    hook: HOOK_MAIN,
    hookWave: 'triangle',
    hookVol: 0.085,
    arp: true,
    kick: 'four',
    bassStyle: 'pump'
  };

  function schedule() {
    if (!cur) return;
    var L = MAIN_TRACK, sp = 60 / L.bpm / 4;
    while (nextT < ctx.currentTime + 0.25) {
      var i = step % 64, bar = Math.floor(i / 16), k = i % 16, t = Math.max(nextT, ctx.currentTime), ch = L.tri[bar];
      if (L.hook[i]) tone(hz(L.hook[i]), t, sp * 1.8, L.hookWave, L.hookVol * vol, 0, true, 2800);
      if (L.arp) tone(hz(ch[[0, 1, 2, 1][k % 4]] + 12), t, sp * 0.8, 'triangle', 0.032 * vol, 0, true, 3000);
      if (k === 0) ch.forEach(function (m) { tone(hz(m), t, sp * 15, 'triangle', 0.045 * vol); });   // pad
      if (k % 2 === 0) tone(hz(L.root[bar] + (k % 8 === 6 ? 12 : 0)), t, sp * 1.6, 'sine', 0.18 * vol, 0, false); // rounded bass
      if (k % 4 === 0) kick(t, 0.26 * vol);
      if (k === 4 || k === 12) { noise(t, 0.1, 0.11 * vol, 2000); tone(190, t, 0.07, 'triangle', 0.08 * vol, 120); } // clap / snare
      if (k % 2 === 0) noise(t, 0.03, 0.03 * vol, 8000); else noise(t, 0.07, 0.04 * vol, 6500); // hats
      nextT += sp; step++;
    }
  }

  // ONE Main Sound: whenever loop() is called, it plays the ONE Main sound.
  // If already playing, it maintains playback seamlessly without stuttering or restarting!
  function loop(name, v) {
    if (!ensure()) return;
    vol = v == null ? 1 : v;
    if (cur) return;
    clearInterval(timer);
    cur = 'main';
    step = 0;
    nextT = ctx.currentTime + 0.05;
    schedule();
    timer = setInterval(schedule, 60);
  }

  function stop() {
    clearInterval(timer);
    cur = null;
  }

  function sfx(name) {
    if (!ensure()) return;
    var t = ctx.currentTime + 0.01, seq;
    if (name === 'correct' || name === 'right') {
      [72, 76, 79, 84].forEach(function (m, i) { tone(hz(m), t + i * 0.08, 0.2, 'triangle', 0.28); });
    } else if (name === 'wrong') {
      tone(220, t, 0.32, 'sawtooth', 0.2, 90); tone(165, t + 0.1, 0.35, 'sawtooth', 0.16, 70);
    } else if (name === 'timeup' || name === 'end') {
      [72, 67, 62].forEach(function (m, i) { tone(hz(m), t + i * 0.12, 0.22, 'square', 0.13); });
    } else if (name === 'tick') {
      tone(1100, t, 0.04, 'square', 0.09);
    } else if (name === 'flip') {
      [72, 79, 84].forEach(function (m, i) { tone(hz(m), t + i * 0.04, 0.14, 'triangle', 0.18); });
    } else if (name === 'special') {
      [72, 79, 76, 83].forEach(function (m, i) { tone(hz(m), t + i * 0.05, 0.16, 'triangle', 0.2); });
    } else if (name === 'bomb') {
      tone(120, t, 0.35, 'sawtooth', 0.24, 50); noise(t, 0.35, 0.2, 1200);
    } else if (name === 'join') {
      tone(hz(84), t, 0.12, 'sine', 0.24); tone(hz(91), t + 0.08, 0.16, 'sine', 0.2);
    } else if (name === 'start') {
      tone(220, t, 0.7, 'sawtooth', 0.12, 880); noise(t, 0.7, 0.12, 2500); tone(hz(84), t + 0.7, 0.4, 'triangle', 0.25);
    } else if (name === 'reveal') {
      noise(t, 0.45, 0.16, 1500); [60, 67, 72].forEach(function (m, i) { tone(hz(m), t + 0.3 + i * 0.05, 0.45, 'triangle', 0.16); });
    } else if (name === 'fanfare' || name === 'win') {
      seq = [60, 64, 67, 72, 67, 72, 76, 79];
      seq.forEach(function (m, i) { tone(hz(m), t + i * 0.12, 0.25, 'triangle', 0.18); tone(hz(m - 12), t + i * 0.12, 0.25, 'sine', 0.16); });
      [72, 76, 79, 84].forEach(function (m) { tone(hz(m), t + 1.05, 1.3, 'triangle', 0.2); tone(hz(m - 12), t + 1.05, 1.3, 'sine', 0.16); });
      kick(t + 1.05, 0.38);
    }
  }

  function toggle() {
    muted = !muted;
    try { localStorage.setItem('km_snd_muted', muted ? '1' : '0'); } catch (e) {}
    if (master) master.gain.value = muted ? 0 : 0.55;
    return muted;
  }

  g.KmSound = {
    loop: loop,
    stop: stop,
    sfx: sfx,
    toggle: toggle,
    unlock: ensure,
    state: function () { return ctx ? ctx.state : 'none'; },      // 'running' once the browser lets the page play sound (needs a click or key first)
    muted: function () { return muted; },
    isPlaying: function () { return !!cur; }
  };
})(window);
