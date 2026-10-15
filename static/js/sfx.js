// Sound for the live quiz: original music loops and sound effects made with Web Audio (no audio files, nothing copied,
// works offline). KmSound.loop('lobby'|'question', vol), KmSound.stop(), KmSound.sfx(name), KmSound.toggle().
(function (g) {
  'use strict';
  var ctx = null, master = null, muted = false, cur = null, timer = 0, nextT = 0, step = 0, vol = 1;
  try { muted = localStorage.getItem('km_snd_muted') === '1'; } catch (e) {}
  var hz = function (m) { return 440 * Math.pow(2, (m - 69) / 12); };
  function ensure() {
    if (!ctx) { var C = window.AudioContext || window.webkitAudioContext; if (!C) return null; ctx = new C(); master = ctx.createGain(); master.gain.value = muted ? 0 : 0.55; master.connect(ctx.destination); }
    if (ctx.state === 'suspended') ctx.resume();
    return ctx;
  }
  function tone(f, t, d, type, v, f2) {
    var o = ctx.createOscillator(), gn = ctx.createGain(); o.type = type; o.frequency.setValueAtTime(f, t); if (f2) o.frequency.exponentialRampToValueAtTime(f2, t + d);
    gn.gain.setValueAtTime(0.0001, t); gn.gain.exponentialRampToValueAtTime(v, t + 0.012); gn.gain.exponentialRampToValueAtTime(0.0001, t + d);
    o.connect(gn); gn.connect(master); o.start(t); o.stop(t + d + 0.03);
  }
  var noiseBuf = null;
  function noise(t, d, v, hp) {
    if (!noiseBuf) { noiseBuf = ctx.createBuffer(1, ctx.sampleRate * 0.5, ctx.sampleRate); var a = noiseBuf.getChannelData(0); for (var i = 0; i < a.length; i++) a[i] = Math.random() * 2 - 1; }
    var s = ctx.createBufferSource(), f = ctx.createBiquadFilter(), gn = ctx.createGain(); s.buffer = noiseBuf; f.type = 'highpass'; f.frequency.value = hp;
    gn.gain.setValueAtTime(v, t); gn.gain.exponentialRampToValueAtTime(0.0001, t + d); s.connect(f); f.connect(gn); gn.connect(master); s.start(t); s.stop(t + d + 0.02);
  }
  function kick(t, v) { tone(150, t, 0.16, 'sine', v, 45); }

  // 16-step patterns: lobby = happy pentatonic bounce, question = driving minor arpeggio
  var LOOPS = {
    lobby: { bpm: 112, lead: [72, 0, 76, 0, 79, 0, 76, 72, 74, 0, 79, 0, 81, 0, 79, 74], bass: [48, 0, 0, 0, 55, 0, 0, 0, 45, 0, 0, 0, 53, 0, 0, 0], kick: [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], hat: [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0], wave: 'triangle' },
    question: { bpm: 132, lead: [69, 72, 76, 72, 69, 72, 76, 81, 67, 71, 74, 71, 67, 71, 74, 79], bass: [45, 0, 45, 0, 45, 0, 45, 0, 43, 0, 43, 0, 43, 0, 43, 0], kick: [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0], hat: [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1], wave: 'square' },
  };
  function schedule() {
    if (!cur) return;
    var L = LOOPS[cur], sp = 60 / L.bpm / 4;
    while (nextT < ctx.currentTime + 0.25) {
      var i = step % 16, t = Math.max(nextT, ctx.currentTime);
      if (L.lead[i]) tone(hz(L.lead[i]), t, sp * 1.8, L.wave, 0.07 * vol);
      if (L.bass[i]) tone(hz(L.bass[i]), t, sp * 3, 'sine', 0.2 * vol);
      if (L.kick[i]) kick(t, 0.28 * vol);
      if (L.hat[i]) noise(t, 0.04, 0.05 * vol, 7000);
      nextT += sp; step++;
    }
  }
  function loop(name, v) {
    if (!ensure()) return;
    if (cur === name) { vol = v == null ? 1 : v; return; }
    clearInterval(timer); cur = name; vol = v == null ? 1 : v; step = 0; nextT = ctx.currentTime + 0.05; schedule(); timer = setInterval(schedule, 60);
  }
  function stop() { clearInterval(timer); cur = null; }
  function sfx(name) {
    if (!ensure()) return; var t = ctx.currentTime + 0.01, seq;
    if (name === 'correct') { [72, 76, 79, 84].forEach(function (m, i) { tone(hz(m), t + i * 0.09, 0.22, 'triangle', 0.3); }); }
    else if (name === 'wrong') { tone(220, t, 0.35, 'sawtooth', 0.22, 90); tone(165, t + 0.12, 0.4, 'sawtooth', 0.18, 70); }
    else if (name === 'timeup') { [72, 67, 62].forEach(function (m, i) { tone(hz(m), t + i * 0.14, 0.25, 'square', 0.14); }); }
    else if (name === 'tick') { tone(1100, t, 0.05, 'square', 0.1); }
    else if (name === 'join') { tone(hz(84), t, 0.12, 'sine', 0.25); tone(hz(91), t + 0.08, 0.16, 'sine', 0.22); }
    else if (name === 'start') { tone(220, t, 0.7, 'sawtooth', 0.12, 880); noise(t, 0.7, 0.12, 2500); tone(hz(84), t + 0.7, 0.4, 'triangle', 0.25); }
    else if (name === 'reveal') { noise(t, 0.45, 0.18, 1500); [60, 67, 72].forEach(function (m, i) { tone(hz(m), t + 0.3 + i * 0.05, 0.5, 'triangle', 0.18); }); }
    else if (name === 'fanfare') {
      seq = [60, 64, 67, 72, 67, 72, 76, 79]; seq.forEach(function (m, i) { tone(hz(m), t + i * 0.13, 0.28, 'square', 0.12); tone(hz(m - 12), t + i * 0.13, 0.28, 'triangle', 0.18); });
      [72, 76, 79, 84].forEach(function (m) { tone(hz(m), t + 1.1, 1.4, 'triangle', 0.16); tone(hz(m - 12), t + 1.1, 1.4, 'sine', 0.14); }); kick(t + 1.1, 0.4);
    }
  }
  function toggle() { muted = !muted; try { localStorage.setItem('km_snd_muted', muted ? '1' : '0'); } catch (e) {} if (master) master.gain.value = muted ? 0 : 0.55; return muted; }
  g.KmSound = { loop: loop, stop: stop, sfx: sfx, toggle: toggle, unlock: ensure, muted: function () { return muted; } };
})(window);
