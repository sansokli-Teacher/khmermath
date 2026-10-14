/* khmermath.org — «កង់ចាប់ឈ្មោះ». Classes and student lists live in this browser's localStorage
   (key km_wheel_v1); the export/import buttons move them to another device.
   A student is {n: full name, g: 'm'|'f'|undefined, off: absent, done: already picked}. */
(function () {
  'use strict';
  var KEY = 'km_wheel_v1';
  var PALETTES = {
    a: ['ពណ៌ស្រស់', ['#e8590c', '#1c7ed6', '#2f9e44', '#ae3ec9', '#f08c00', '#0c8599', '#d6336c', '#5f3dc4']],
    b: ['ទឹកសមុទ្រ', ['#0b7285', '#1971c2', '#1098ad', '#3b5bdb', '#0c8599', '#364fc7', '#1864ab', '#0b7285']],
    c: ['ភ្លើងក្ដៅ', ['#e8590c', '#f08c00', '#e03131', '#c2255c', '#d9480f', '#c92a2a', '#e67700', '#a61e4d']],
    d: ['ព្រៃបៃតង', ['#2b8a3e', '#2f9e44', '#087f5b', '#5c940d', '#0b7285', '#66a80f', '#099268', '#37b24d']],
    e: ['ជាតិខ្មែរ', ['#032ea1', '#e00025', '#032ea1', '#e00025', '#032ea1', '#e00025']]
  };
  function colors() { return (PALETTES[S().theme] || PALETTES.a)[1]; }
  var $ = function (id) { return document.getElementById(id); };
  var canvas = $('wh-canvas'); if (!canvas) return;
  var ctx = canvas.getContext('2d');

  var state = load();
  var wl = null;                                          // slices frozen at spin time, so the picked slice stays under the pointer
  var angle = 0, spinning = false, current = null;       // current: the student last picked
  var sound = true, noRepeat = true, audio = null, clickMode = 'off', lastGroups = '', ord = null, histTally = false, pendingReveal = false;
  function S() { return state.set || (state.set = { dur: 5, theme: 'a', fw: true, mystery: false, speak: false }); }

  function uid() { return 'c' + Date.now().toString(36) + Math.random().toString(36).slice(2, 6); }
  function load() {
    try {
      var s = JSON.parse(localStorage.getItem(KEY));
      if (s && s.classes && s.classes.length) return s;
    } catch (e) {}
    var id = uid();
    return { v: 1, active: id, noRepeat: true, sound: true, classes: [{ id: id, name: 'ថ្នាក់ទី ៧ក', students: [] }] };
  }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) {} }
  function cls() {
    for (var i = 0; i < state.classes.length; i++) if (state.classes[i].id === state.active) return state.classes[i];
    state.active = state.classes[0].id; return state.classes[0];
  }
  function eligible() {
    var f = $('wh-gfilter').value;
    var list = cls().students.filter(function (s) { return !s.off && !(noRepeat && s.done) && (!f || s.g === f); });
    if (ord) list.sort(function (a, b) { return (ord[a.n] || 0) - (ord[b.n] || 0); });
    return list;
  }
  function present() { return cls().students.filter(function (s) { return !s.off; }); }
  function clean(n) { return String(n || '').replace(/ /g, ' ').replace(/\s+/g, ' ').trim(); }
  function shuffle(a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  var G_WORD = { m: 'ប្រុស', f: 'ស្រី' };

  /* One pasted line -> {n, g}. Excel gives "surname<TAB>first name"; both parts are kept.
     A leading number ("1." / "2)" / "3<TAB>") and a trailing «ប្រុស»/«ស្រី» (when the name has 2+ words) are recognised. */
  function parseLine(line) {
    var t = line.replace(/ /g, ' ').replace(/^\s*[\d០-៩]+(?:\t|\s*[.)\-:។]\s+)/, '');
    var words = clean(t).split(' ').filter(Boolean), g;
    if (words.length >= 3 && (words[words.length - 1] === 'ប្រុស' || words[words.length - 1] === 'ស្រី')) {
      g = words.pop() === 'ប្រុស' ? 'm' : 'f';
    }
    var n = words.join(' ');
    return n ? { n: n, g: g } : null;
  }

  /* ---------- drawing ---------- */
  function redraw() { wl = null; draw(); }
  function draw() {
    var list = wl || eligible(), n = list.length, W = canvas.width, c = W / 2, r = c - 6;
    ctx.clearRect(0, 0, W, W);
    ctx.save(); ctx.translate(c, c); ctx.rotate(angle);
    if (!n) {
      ctx.beginPath(); ctx.arc(0, 0, r, 0, 7); ctx.fillStyle = '#cfd6dd'; ctx.fill();
    } else {
      var a = Math.PI * 2 / n;
      for (var i = 0; i < n; i++) {
        ctx.beginPath(); ctx.moveTo(0, 0); ctx.arc(0, 0, r, i * a - Math.PI / 2 - a / 2, i * a - Math.PI / 2 + a / 2); ctx.closePath();
        ctx.fillStyle = colors()[i % colors().length]; ctx.fill();
        if (n > 1) { ctx.strokeStyle = 'rgba(255,255,255,.7)'; ctx.lineWidth = 2; ctx.stroke(); }
        ctx.save(); ctx.rotate(i * a - Math.PI / 2);
        var size = Math.max(13, Math.min(36, Math.floor(r * a * 0.6)));
        ctx.font = '600 ' + size + 'px "Kantumruy Pro", sans-serif';
        ctx.fillStyle = '#fff'; ctx.textAlign = 'right'; ctx.textBaseline = 'middle';
        ctx.shadowColor = 'rgba(0,0,0,.35)'; ctx.shadowBlur = 3;
        var name = list[i].n, maxW = r * 0.7;
        while (ctx.measureText(name).width > maxW && name.length > 2) name = name.slice(0, -1);
        if (name !== list[i].n) name += '…';
        ctx.fillText(name, r - 16, 0);
        ctx.restore();
      }
    }
    ctx.restore();
  }

  /* ---------- sound + fireworks ---------- */
  function tone(freqs, vol, len) {
    if (!sound) return;
    try {
      audio = audio || new (window.AudioContext || window.webkitAudioContext)();
      freqs.forEach(function (f, i) {
        var o = audio.createOscillator(), g = audio.createGain(), t = audio.currentTime + i * 0.13;
        o.frequency.value = f; g.gain.setValueAtTime(vol, t); g.gain.exponentialRampToValueAtTime(0.001, t + len);
        o.connect(g); g.connect(audio.destination); o.start(t); o.stop(t + len + 0.02);
      });
    } catch (e) {}
  }
  var fwRun = 0;
  function fireworks() {
    var cv = $('wh-fw'), reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduce) return;
    var dpr = Math.min(2, window.devicePixelRatio || 1), W = cv.clientWidth, H = cv.clientHeight;
    cv.width = W * dpr; cv.height = H * dpr;
    var g = cv.getContext('2d'); g.setTransform(dpr, 0, 0, dpr, 0, 0);
    var parts = [], end = performance.now() + 3600, nextBurst = 0, id = ++fwRun, hues = [8, 40, 52, 130, 190, 280, 330];
    function burst(x, y) {
      var hue = hues[Math.floor(Math.random() * hues.length)], n = 46;
      for (var i = 0; i < n; i++) {
        var a = Math.PI * 2 * i / n + Math.random() * 0.2, v = 2.2 + Math.random() * 3.6;
        parts.push({ x: x, y: y, vx: Math.cos(a) * v, vy: Math.sin(a) * v, life: 1, hue: hue + Math.random() * 25 - 12 });
      }
    }
    (function frame(now) {
      if (id !== fwRun) return;
      g.globalCompositeOperation = 'destination-out'; g.fillStyle = 'rgba(0,0,0,.22)'; g.fillRect(0, 0, W, H);
      g.globalCompositeOperation = 'lighter';
      if (now < end && now > nextBurst) { burst(W * (0.12 + Math.random() * 0.76), H * (0.1 + Math.random() * 0.45)); nextBurst = now + 260 + Math.random() * 260; }
      parts = parts.filter(function (p) { return p.life > 0.02; });
      parts.forEach(function (p) {
        p.x += p.vx; p.y += p.vy; p.vy += 0.06; p.vx *= 0.985; p.vy *= 0.985; p.life -= 0.013;
        g.fillStyle = 'hsla(' + p.hue + ',100%,60%,' + Math.max(0, p.life) + ')';
        g.beginPath(); g.arc(p.x, p.y, 2.6, 0, 7); g.fill();
      });
      if (now < end || parts.length) requestAnimationFrame(frame); else g.clearRect(0, 0, W, H);
    })(performance.now());
  }
  function stopFireworks() { fwRun++; var cv = $('wh-fw'); cv.getContext('2d').clearRect(0, 0, cv.width, cv.height); }

  /* ---------- spinning ---------- */
  function spin() {
    if (spinning) return;
    var list = eligible(), n = list.length; if (!n) return;
    wl = list; closePop();
    var pick = Math.floor(Math.random() * n), a = Math.PI * 2 / n;
    var target = -(pick * a + (Math.random() - 0.5) * a * 0.7);   // slice `pick` is centred at pick*a from the top; land inside it
    var turns = 5 + Math.floor(Math.random() * 3);
    var from = angle, norm = ((target - from) % (Math.PI * 2) + Math.PI * 2) % (Math.PI * 2);
    var to = from + turns * Math.PI * 2 + norm, dur = S().dur * 1000 * (0.9 + Math.random() * 0.2), t0 = performance.now(), lastSlice = -1;
    spinning = true; $('wh-spin').disabled = true;
    (function frame(now) {
      var t = Math.min(1, (now - t0) / dur), e = 1 - Math.pow(1 - t, 4);
      angle = from + (to - from) * e; draw();
      var sl = Math.floor(((-angle % (Math.PI * 2)) + Math.PI * 2 + a / 2) / a); if (sl !== lastSlice) { lastSlice = sl; tone([900], 0.04, 0.025); }
      if (t < 1) return requestAnimationFrame(frame);
      spinning = false; $('wh-spin').disabled = false; angle = to % (Math.PI * 2); draw();
      finish(list[pick]);
    })(t0);
  }
  function finish(student) {
    current = student; if (noRepeat) current.done = true;
    var c = cls(); (c.hist = c.hist || []).push({ n: current.n, t: Date.now() }); if (c.hist.length > 300) c.hist.shift();
    save(); renderChips(); refreshEmpty(); renderHist();
    pendingReveal = !!S().mystery; openPop();
    if (!pendingReveal) celebrate();
  }
  function celebrate() {
    if (S().fw) { tone([523, 659, 784, 1047], 0.08, 0.3); fireworks(); }
    if (S().speak) say();
  }
  function openPop() {
    var n = cls().hist ? cls().hist.length : 1;
    $('wh-winner').textContent = pendingReveal ? '?' : current.n;
    $('wh-popsmall').textContent = 'សិស្សដែលត្រូវបានជ្រើស · លើកទី ' + khNum(n);
    $('wh-reveal').hidden = !pendingReveal; $('wh-again').hidden = pendingReveal; $('wh-absent').hidden = pendingReveal;
    $('wh-say').hidden = pendingReveal || !voiceKm;
    $('wh-pop').hidden = false; (pendingReveal ? $('wh-reveal') : $('wh-again')).focus({ preventScroll: true });
  }
  function reveal() {
    pendingReveal = false; $('wh-winner').textContent = current.n; $('wh-reveal').hidden = true; $('wh-again').hidden = false; $('wh-absent').hidden = false;
    $('wh-say').hidden = !voiceKm; celebrate();
  }
  function closePop() { $('wh-pop').hidden = true; pendingReveal = false; stopFireworks(); if (window.speechSynthesis) speechSynthesis.cancel(); }
  var voiceKm = null;
  function findVoice() {
    if (!window.speechSynthesis) return;
    voiceKm = speechSynthesis.getVoices().filter(function (v) { return /^km/i.test(v.lang); })[0] || null;
    $('wh-speakrow').hidden = !voiceKm;
  }
  function say() {
    if (!voiceKm || !current) return;
    try { speechSynthesis.cancel(); var u = new SpeechSynthesisUtterance(current.n); u.voice = voiceKm; u.lang = voiceKm.lang; speechSynthesis.speak(u); } catch (e) {}
  }

  /* ---------- history (who has been picked) ---------- */
  function histCounts(h) { var cnt = {}; h.forEach(function (x) { cnt[x.n] = (cnt[x.n] || 0) + 1; }); return cnt; }
  function renderHist() {
    var ol = $('wh-hist'), h = cls().hist || []; ol.innerHTML = ''; ol.className = 'wh-hist' + (histTally ? ' tally' : '');
    $('wh-hcount').textContent = h.length ? '(' + h.length + ')' : '';
    if (histTally) {
      var cnt = histCounts(h);
      Object.keys(cnt).sort(function (a, b) { return cnt[b] - cnt[a]; }).forEach(function (n) {
        var li = document.createElement('li'), b = document.createElement('span'); li.textContent = n; b.className = 'cnt'; b.textContent = cnt[n] + ' ដង'; li.appendChild(b); ol.appendChild(li);
      });
    } else {
      h.slice().reverse().forEach(function (x, i) {
        var li = document.createElement('li'), t = new Date(x.t), sm = document.createElement('small');
        li.value = h.length - i; li.textContent = x.n; sm.textContent = ('0' + t.getHours()).slice(-2) + ':' + ('0' + t.getMinutes()).slice(-2); li.appendChild(sm); ol.appendChild(li);
      });
    }
  }

  /* ---------- groups ---------- */
  function makeGroups() {
    var people = present(); if (!people.length) return null;
    var mode = $('wh-gmode').value, num = Math.max(1, Math.floor(+$('wh-gnum').value) || 1);
    var count = mode === 'k' ? Math.ceil(people.length / num) : Math.min(num, people.length);
    var groups = []; for (var i = 0; i < count; i++) groups.push([]);
    var hasG = people.some(function (p) { return p.g; });
    var order = $('wh-gbal').checked && hasG
      ? shuffle(people.filter(function (p) { return p.g === 'f'; })).concat(shuffle(people.filter(function (p) { return p.g === 'm'; })), shuffle(people.filter(function (p) { return !p.g; })))
      : shuffle(people);
    order.forEach(function (p, i) { groups[i % count].push(p); });   // dealing round-robin keeps sizes within 1 and spreads each gender
    return groups;
  }
  function showGroups(groups, title) {
    var box = $('wh-groups'); box.innerHTML = ''; box.hidden = false; lastGroups = '';
    groups.forEach(function (g, i) {
      var d = document.createElement('div'), h = document.createElement('b'), ul = document.createElement('ol');
      d.className = 'wh-g'; h.textContent = (title || 'ក្រុមទី ') + (title ? '' : khNum(i + 1)) + ' · ' + khNum(g.length) + ' នាក់';
      g.forEach(function (p) { var li = document.createElement('li'); li.textContent = (p.g ? (p.g === 'f' ? '♀ ' : '♂ ') : '') + p.n; ul.appendChild(li); });
      d.appendChild(h); d.appendChild(ul); box.appendChild(d);
      lastGroups += h.textContent + '\n' + g.map(function (p, k) { return (k + 1) + '. ' + p.n; }).join('\n') + '\n\n';
    });
    $('wh-copy').hidden = false;
  }
  function khNum(n) { return String(n).replace(/\d/g, function (d) { return '០១២៣៤៥៦៧៨៩'[d]; }); }

  /* ---------- UI ---------- */
  function refreshEmpty() {
    var c = cls(), list = eligible(), box = $('wh-empty'), msg = '';
    if (!c.students.length) msg = 'ថ្នាក់នេះមិនទាន់មានសិស្សទេ។ សូមបន្ថែមឈ្មោះ ឬចុច «កែបញ្ជីឈ្មោះ» ដើម្បីបិទភ្ជាប់បញ្ជី។';
    else if (!list.length) msg = $('wh-gfilter').value && !c.students.some(function (s) { return s.g === $('wh-gfilter').value; }) ? 'មិនទាន់បានកំណត់ភេទសិស្សទេ។ ចុច «ចុចឈ្មោះ៖ កំណត់ភេទ» ហើយចុចលើឈ្មោះ។'
      : noRepeat ? 'សិស្សទាំងអស់ត្រូវបានជ្រើសហើយ។ ចុច «ចាប់ផ្ដើមជុំថ្មី» ដើម្បីចាប់ផ្ដើមម្ដងទៀត។' : 'សិស្សទាំងអស់អវត្តមាន។';
    box.textContent = msg; box.hidden = !msg; $('wh-spin').disabled = spinning || !list.length;
  }
  function renderChips() {
    var c = cls(), ul = $('wh-chips'); ul.innerHTML = '';
    c.students.forEach(function (s) {
      var li = document.createElement('li'), b = document.createElement('button');
      b.type = 'button'; b.textContent = (s.g ? (s.g === 'f' ? '♀ ' : '♂ ') : '') + s.n;
      b.className = (s.off ? 'off ' : '') + (s.done && noRepeat ? 'done ' : '') + (s.g ? 'g-' + s.g : '');
      b.addEventListener('click', function () {
        if (clickMode === 'g') s.g = s.g === 'm' ? 'f' : s.g === 'f' ? undefined : 'm';   // none -> boy -> girl -> none
        else s.off = !s.off;
        save(); renderChips(); refreshEmpty(); redraw();
      });
      li.appendChild(b); ul.appendChild(li);
    });
    var p = present(), m = p.filter(function (s) { return s.g === 'm'; }).length, f = p.filter(function (s) { return s.g === 'f'; }).length;
    $('wh-count').textContent = c.students.length ? '(' + p.length + '/' + c.students.length + ')' : '';
    $('wh-gsum').textContent = c.students.length ? 'ប្រុស ' + m + ' · ស្រី ' + f + (p.length - m - f ? ' · មិនទាន់កំណត់ ' + (p.length - m - f) : '') : '';
    $('wh-modehint').textContent = clickMode === 'g' ? 'ចុចលើឈ្មោះម្ដងៗ៖ ប្រុស ♂ → ស្រី ♀ → មិនកំណត់។' : 'ចុចលើឈ្មោះដើម្បីសម្គាល់ថាអវត្តមាន (មិនចូលកង់)។';
  }
  function renderClasses() {
    var sel = $('wh-class'); sel.innerHTML = '';
    state.classes.forEach(function (c) {
      var o = document.createElement('option'); o.value = c.id; o.textContent = c.name + ' (' + c.students.length + ')'; sel.appendChild(o);
    });
    sel.value = state.active;
  }
  function renderAll() { renderClasses(); renderChips(); refreshEmpty(); renderHist(); redraw(); $('wh-groups').hidden = true; $('wh-copy').hidden = true; }
  function setFlag(btn, on, label) { btn.setAttribute('aria-pressed', on ? 'true' : 'false'); btn.textContent = label + (on ? ': បើក' : ': បិទ'); }
  function setMode(m) {
    clickMode = m; $('wh-mode-off').setAttribute('aria-pressed', m === 'off'); $('wh-mode-g').setAttribute('aria-pressed', m === 'g'); renderChips();
  }

  $('wh-spin').addEventListener('click', spin);
  $('wh-again').addEventListener('click', spin);
  $('wh-close').addEventListener('click', closePop);
  $('wh-pop').addEventListener('click', function (e) { if (e.target === this) closePop(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !$('wh-pop').hidden) closePop(); });
  $('wh-absent').addEventListener('click', function () {
    if (!current) return; current.off = true; current.done = false; var hh = cls().hist; if (hh && hh.length && hh[hh.length - 1].n === current.n) hh.pop(); save(); current = null; closePop(); renderChips(); refreshEmpty(); renderHist(); redraw();
  });
  $('wh-gfilter').addEventListener('change', function () { refreshEmpty(); redraw(); });
  $('wh-mode-off').addEventListener('click', function () { setMode('off'); });
  $('wh-mode-g').addEventListener('click', function () { setMode('g'); });
  $('wh-class').addEventListener('change', function () { state.active = this.value; current = null; closePop(); save(); renderAll(); });
  $('wh-newclass').addEventListener('click', function () {
    var name = clean(prompt('ឈ្មោះថ្នាក់ថ្មី (ឧ. ថ្នាក់ទី ៩ខ)')); if (!name) return;
    var c = { id: uid(), name: name, students: [] }; state.classes.push(c); state.active = c.id; save(); renderAll();
    $('wh-edit').click();
  });
  $('wh-rename').addEventListener('click', function () {
    var c = cls(), name = clean(prompt('ឈ្មោះថ្នាក់', c.name)); if (!name) return; c.name = name; save(); renderClasses();
  });
  $('wh-delclass').addEventListener('click', function () {
    var c = cls();
    if (!confirm('លុបថ្នាក់ «' + c.name + '» និងបញ្ជីសិស្សទាំង ' + c.students.length + ' នាក់?')) return;
    state.classes = state.classes.filter(function (x) { return x !== c; });
    if (!state.classes.length) state.classes.push({ id: uid(), name: 'ថ្នាក់ថ្មី', students: [] });
    state.active = state.classes[0].id; current = null; closePop(); save(); renderAll();
  });
  $('wh-addform').addEventListener('submit', function (e) {
    e.preventDefault(); var inp = $('wh-addname'), p = parseLine(inp.value); if (!p) return;
    cls().students.push(p); inp.value = ''; save(); renderAll(); inp.focus();
  });
  $('wh-edit').addEventListener('click', function () {
    $('wh-text').value = cls().students.map(function (s) { return s.n + (s.g ? ' ' + G_WORD[s.g] : ''); }).join('\n');
    $('wh-editor').hidden = false; $('wh-text').focus();
  });
  $('wh-cancel').addEventListener('click', function () { $('wh-editor').hidden = true; });
  $('wh-save').addEventListener('click', function () {
    var c = cls(), old = {}; c.students.forEach(function (s) { old[s.n] = s; });
    var seen = {}, out = [];
    $('wh-text').value.split(/\r?\n/).forEach(function (line) {
      var p = parseLine(line); if (!p || seen[p.n]) return; seen[p.n] = 1;
      var prev = old[p.n]; if (prev) { if (p.g) prev.g = p.g; out.push(prev); } else out.push(p);   // keep absent/done marks of names that were already there
    });
    c.students = out; $('wh-editor').hidden = true; current = null; closePop(); save(); renderAll();
  });
  $('wh-reset').addEventListener('click', function () {
    cls().students.forEach(function (s) { s.done = false; }); current = null; closePop(); save(); renderChips(); refreshEmpty(); redraw();
  });
  $('wh-sound').addEventListener('click', function () { sound = !sound; state.sound = sound; save(); setFlag(this, sound, 'សំឡេង'); });
  $('wh-norepeat').addEventListener('click', function () { noRepeat = !noRepeat; state.noRepeat = noRepeat; save(); setFlag(this, noRepeat, 'មិនជ្រើសម្ដងទៀត'); renderChips(); refreshEmpty(); redraw(); });
  $('wh-full').addEventListener('click', function () {
    var st = $('wh-stage');
    if (document.fullscreenElement) document.exitFullscreen();
    else if (st.requestFullscreen) st.requestFullscreen();
  });
  if (!document.fullscreenEnabled) $('wh-full').hidden = true;

  $('wh-group').addEventListener('click', function () {
    var g = makeGroups(); if (!g) { $('wh-groups').hidden = false; $('wh-groups').textContent = 'មិនទាន់មានសិស្សទេ។'; return; }
    showGroups(g);
  });
  $('wh-order').addEventListener('click', function () {
    var p = shuffle(present()); if (!p.length) return;
    var box = $('wh-groups'); box.innerHTML = ''; box.hidden = false;
    var d = document.createElement('div'), h = document.createElement('b'), ol = document.createElement('ol');
    d.className = 'wh-g'; h.textContent = 'លំដាប់ចៃដន្យ · ' + khNum(p.length) + ' នាក់'; d.appendChild(h);
    p.forEach(function (s) { var li = document.createElement('li'); li.textContent = s.n; ol.appendChild(li); });
    d.appendChild(ol); box.appendChild(d);
    lastGroups = h.textContent + '\n' + p.map(function (s, k) { return (k + 1) + '. ' + s.n; }).join('\n') + '\n';
    $('wh-copy').hidden = false;
  });
  $('wh-copy').addEventListener('click', function () {
    var btn = this, done = function (ok) { btn.textContent = ok ? 'បានចម្លង ✓' : 'ចម្លងមិនបាន'; setTimeout(function () { btn.textContent = 'ចម្លងលទ្ធផល'; }, 1600); };
    if (navigator.clipboard) navigator.clipboard.writeText(lastGroups).then(function () { done(true); }, function () { done(false); }); else done(false);
  });

  $('wh-reveal').addEventListener('click', reveal);
  $('wh-say').addEventListener('click', say);
  $('wh-shuffle').addEventListener('click', function () {
    ord = {}; cls().students.forEach(function (x) { ord[x.n] = Math.random(); }); redraw();
  });
  $('wh-hview').addEventListener('click', function () {
    histTally = !histTally; this.setAttribute('aria-pressed', histTally); this.textContent = histTally ? 'មើលតាមលំដាប់ពេល' : 'សរុបតាមចំនួនដង'; renderHist();
  });
  $('wh-hcopy').addEventListener('click', function () {
    var btn = this, h = cls().hist || [], txt;
    if (histTally) { var cnt = histCounts(h); txt = Object.keys(cnt).sort(function (a, b) { return cnt[b] - cnt[a]; }).map(function (n) { return n + '\t' + cnt[n]; }).join('\n'); }
    else txt = h.map(function (x, i) { return (i + 1) + '. ' + x.n; }).join('\n');
    var done = function (ok) { btn.textContent = ok ? 'បានចម្លង ✓' : 'ចម្លងមិនបាន'; setTimeout(function () { btn.textContent = 'ចម្លង'; }, 1600); };
    if (navigator.clipboard) navigator.clipboard.writeText(txt).then(function () { done(true); }, function () { done(false); }); else done(false);
  });
  $('wh-hclear').addEventListener('click', function () {
    var c = cls(); if (!(c.hist || []).length || !confirm('សម្អាតលទ្ធផលទាំងអស់ក្នុងថ្នាក់នេះ?')) return;
    c.hist = []; save(); renderHist();
  });
  $('wh-dur').addEventListener('input', function () { S().dur = +this.value; $('wh-durv').textContent = khNum(this.value); save(); });
  $('wh-theme').addEventListener('change', function () { S().theme = this.value; save(); draw(); });
  $('wh-fwon').addEventListener('change', function () { S().fw = this.checked; save(); });
  $('wh-mystery').addEventListener('change', function () { S().mystery = this.checked; save(); });
  $('wh-speak').addEventListener('change', function () { S().speak = this.checked; save(); });
  document.addEventListener('keydown', function (e) {
    var inField = /^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName || '') || (e.target.tagName === 'BUTTON' && e.code === 'Space');
    if ((e.code === 'Enter' && (e.ctrlKey || e.metaKey)) || (e.code === 'Space' && !inField && e.target === document.body)) {
      e.preventDefault(); if (!$('wh-pop').hidden && pendingReveal) reveal(); else spin();
    }
  });

  $('wh-export').addEventListener('click', function () {
    var blob = new Blob([JSON.stringify(state, null, 1)], { type: 'application/json' }), a = document.createElement('a');
    a.href = URL.createObjectURL(blob); a.download = 'khmermath-kong-classes.json'; document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
  });
  $('wh-import').addEventListener('click', function () { $('wh-file').click(); });
  $('wh-file').addEventListener('change', function () {
    var f = this.files[0]; this.value = ''; if (!f) return;
    var r = new FileReader();
    r.onload = function () {
      try {
        var s = JSON.parse(r.result);
        if (!s || !Array.isArray(s.classes)) throw 0;
        var ok = s.classes.filter(function (c) { return c && c.name && Array.isArray(c.students); });
        if (!ok.length) throw 0;
        if (!confirm('នាំចូលថ្នាក់ ' + ok.length + ' ហើយជំនួសបញ្ជីបច្ចុប្បន្ន?')) return;
        ok.forEach(function (c) { c.id = c.id || uid(); c.students = c.students.filter(function (x) { return x && x.n; }); });
        state = { v: 1, active: ok[0].id, noRepeat: s.noRepeat !== false, sound: s.sound !== false, set: s.set || state.set, classes: ok };
        noRepeat = state.noRepeat; sound = state.sound; setFlag($('wh-sound'), sound, 'សំឡេង'); setFlag($('wh-norepeat'), noRepeat, 'មិនជ្រើសម្ដងទៀត');
        save(); renderAll();
      } catch (e) { alert('ឯកសារនេះមិនមែនជាឯកសារបម្រុងរបស់កង់ឈ្មោះទេ។'); }
    };
    r.readAsText(f);
  });

  noRepeat = state.noRepeat !== false; sound = state.sound !== false;
  (function initSettings() {
    var set = S(), sel = $('wh-theme');
    Object.keys(PALETTES).forEach(function (k) { var o = document.createElement('option'); o.value = k; o.textContent = PALETTES[k][0]; sel.appendChild(o); });
    sel.value = set.theme; $('wh-dur').value = set.dur; $('wh-durv').textContent = khNum(set.dur);
    $('wh-fwon').checked = set.fw !== false; $('wh-mystery').checked = !!set.mystery; $('wh-speak').checked = !!set.speak;
    if (window.speechSynthesis) { findVoice(); if (speechSynthesis.addEventListener) speechSynthesis.addEventListener('voiceschanged', findVoice); }
  })();
  setFlag($('wh-sound'), sound, 'សំឡេង'); setFlag($('wh-norepeat'), noRepeat, 'មិនជ្រើសម្ដងទៀត');
  renderAll();
  if (document.fonts && document.fonts.load) document.fonts.load('600 20px "Kantumruy Pro"').then(redraw);
})();
