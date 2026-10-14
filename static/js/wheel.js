/* khmermath.org — «កង់ចាប់ឈ្មោះ». Classes and student lists live in this browser's localStorage
   (key km_wheel_v1); the export/import buttons move them to another device. */
(function () {
  'use strict';
  var KEY = 'km_wheel_v1';
  var COLORS = ['#e8590c', '#1c7ed6', '#2f9e44', '#ae3ec9', '#f08c00', '#0c8599', '#d6336c', '#5f3dc4'];
  var $ = function (id) { return document.getElementById(id); };
  var canvas = $('wh-canvas'); if (!canvas) return;
  var ctx = canvas.getContext('2d');

  var state = load();
  var wl = null;                                          // slices frozen at spin time, so the picked slice stays under the pointer
  var angle = 0, spinning = false, current = null;       // current: the student last picked
  var sound = true, noRepeat = true, audio = null;

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
    return cls().students.filter(function (s) { return !s.off && !(noRepeat && s.done); });
  }
  function clean(n) { return String(n || '').replace(/\s+/g, ' ').trim(); }

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
        ctx.fillStyle = COLORS[i % COLORS.length]; ctx.fill();
        if (n > 1) { ctx.strokeStyle = 'rgba(255,255,255,.7)'; ctx.lineWidth = 2; ctx.stroke(); }
        // label runs along the radius, reading outwards
        ctx.save(); ctx.rotate(i * a - Math.PI / 2);
        var size = Math.max(14, Math.min(38, Math.floor(r * a * 0.6)));
        ctx.font = '600 ' + size + 'px "Kantumruy Pro", sans-serif';
        ctx.fillStyle = '#fff'; ctx.textAlign = 'right'; ctx.textBaseline = 'middle';
        ctx.shadowColor = 'rgba(0,0,0,.35)'; ctx.shadowBlur = 3;
        var name = list[i].n, maxW = r * 0.66;
        while (ctx.measureText(name).width > maxW && name.length > 2) name = name.slice(0, -1);
        if (name !== list[i].n) name += '…';
        ctx.fillText(name, r - 18, 0);
        ctx.restore();
      }
    }
    ctx.restore();
  }

  /* ---------- spinning ---------- */
  function tick() {
    if (!sound) return;
    try {
      audio = audio || new (window.AudioContext || window.webkitAudioContext)();
      var o = audio.createOscillator(), g = audio.createGain();
      o.frequency.value = 900; g.gain.value = 0.04; o.connect(g); g.connect(audio.destination);
      o.start(); o.stop(audio.currentTime + 0.025);
    } catch (e) {}
  }
  function fanfare() {
    if (!sound) return;
    try {
      audio = audio || new (window.AudioContext || window.webkitAudioContext)();
      [523, 659, 784].forEach(function (f, i) {
        var o = audio.createOscillator(), g = audio.createGain(), t = audio.currentTime + i * 0.13;
        o.frequency.value = f; g.gain.setValueAtTime(0.08, t); g.gain.exponentialRampToValueAtTime(0.001, t + 0.3);
        o.connect(g); g.connect(audio.destination); o.start(t); o.stop(t + 0.32);
      });
    } catch (e) {}
  }

  function spin() {
    if (spinning) return;
    var list = eligible(), n = list.length; if (!n) return;
    wl = list;
    $('wh-result').hidden = true; current = null;
    var pick = Math.floor(Math.random() * n), a = Math.PI * 2 / n;
    // slice `pick` is centred at pick*a from the top; bring it under the pointer, with a little jitter inside the slice
    var jitter = (Math.random() - 0.5) * a * 0.7;
    var target = -(pick * a + jitter);
    var turns = 5 + Math.floor(Math.random() * 3);
    var from = angle, norm = ((target - from) % (Math.PI * 2) + Math.PI * 2) % (Math.PI * 2);
    var to = from + turns * Math.PI * 2 + norm, dur = 4600 + Math.random() * 1200, t0 = performance.now(), lastSlice = -1;
    spinning = true; $('wh-spin').disabled = true;
    (function frame(now) {
      var t = Math.min(1, (now - t0) / dur), e = 1 - Math.pow(1 - t, 4);
      angle = from + (to - from) * e; draw();
      var sl = Math.floor(((-angle % (Math.PI * 2)) + Math.PI * 2 + a / 2) / a); if (sl !== lastSlice) { lastSlice = sl; tick(); }
      if (t < 1) return requestAnimationFrame(frame);
      spinning = false; $('wh-spin').disabled = false; angle = to % (Math.PI * 2); draw();
      current = list[pick]; if (noRepeat) current.done = true; save(); fanfare(); showResult(); renderChips();
    })(t0);
  }
  function showResult() {
    $('wh-winner').textContent = current.n; $('wh-result').hidden = false;
    $('wh-spin').textContent = 'បង្វិល'; refreshEmpty(); draw();
  }

  /* ---------- UI ---------- */
  function refreshEmpty() {
    var c = cls(), list = eligible(), box = $('wh-empty');
    var msg = '';
    if (!c.students.length) msg = 'ថ្នាក់នេះមិនទាន់មានសិស្សទេ។ សូមបន្ថែមឈ្មោះ ឬចុច «កែបញ្ជីឈ្មោះ» ដើម្បីបិទភ្ជាប់បញ្ជី។';
    else if (!list.length) msg = noRepeat ? 'សិស្សទាំងអស់ត្រូវបានជ្រើសហើយ។ ចុច «ចាប់ផ្ដើមជុំថ្មី» ដើម្បីចាប់ផ្ដើមម្ដងទៀត។' : 'សិស្សទាំងអស់អវត្តមាន។';
    box.textContent = msg; box.hidden = !msg; $('wh-spin').disabled = spinning || !list.length;
  }
  function renderChips() {
    var c = cls(), ul = $('wh-chips'); ul.innerHTML = '';
    c.students.forEach(function (s, i) {
      var li = document.createElement('li'), b = document.createElement('button');
      b.type = 'button'; b.textContent = s.n;
      b.className = (s.off ? 'off ' : '') + (s.done && noRepeat ? 'done' : '');
      b.title = s.off ? 'អវត្តមាន — ចុចដើម្បីដាក់ចូលវិញ' : 'ចុចដើម្បីសម្គាល់ថាអវត្តមាន';
      b.addEventListener('click', function () { s.off = !s.off; save(); renderChips(); refreshEmpty(); redraw(); });
      li.appendChild(b); ul.appendChild(li);
    });
    var present = c.students.filter(function (s) { return !s.off; }).length;
    $('wh-count').textContent = c.students.length ? '(' + present + '/' + c.students.length + ')' : '';
  }
  function renderClasses() {
    var sel = $('wh-class'); sel.innerHTML = '';
    state.classes.forEach(function (c) {
      var o = document.createElement('option'); o.value = c.id; o.textContent = c.name + ' (' + c.students.length + ')'; sel.appendChild(o);
    });
    sel.value = state.active;
  }
  function renderAll() { renderClasses(); renderChips(); refreshEmpty(); redraw(); }
  function setFlag(btn, on, label) { btn.setAttribute('aria-pressed', on ? 'true' : 'false'); btn.textContent = label + (on ? ': បើក' : ': បិទ'); }

  $('wh-spin').addEventListener('click', spin);
  $('wh-again').addEventListener('click', spin);
  $('wh-absent').addEventListener('click', function () {
    if (!current) return; current.off = true; current.done = false; save(); current = null; $('wh-result').hidden = true; renderChips(); refreshEmpty(); redraw();
  });
  $('wh-class').addEventListener('change', function () { state.active = this.value; current = null; $('wh-result').hidden = true; save(); renderAll(); });
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
    state.active = state.classes[0].id; current = null; $('wh-result').hidden = true; save(); renderAll();
  });
  $('wh-addform').addEventListener('submit', function (e) {
    e.preventDefault(); var inp = $('wh-addname'), n = clean(inp.value); if (!n) return;
    cls().students.push({ n: n }); inp.value = ''; save(); renderAll(); inp.focus();
  });
  $('wh-edit').addEventListener('click', function () {
    $('wh-text').value = cls().students.map(function (s) { return s.n; }).join('\n'); $('wh-editor').hidden = false; $('wh-text').focus();
  });
  $('wh-cancel').addEventListener('click', function () { $('wh-editor').hidden = true; });
  $('wh-save').addEventListener('click', function () {
    var c = cls(), old = {}; c.students.forEach(function (s) { old[s.n] = s; });
    var seen = {}, out = [];
    $('wh-text').value.split(/\r?\n/).forEach(function (line) {
      var n = clean(line.split('\t')[0].replace(/^[\d\s.\-)]+(?=\D)/, '')) || clean(line); // drop "1." / "12)" numbering
      if (n && !seen[n]) { seen[n] = 1; out.push(old[n] || { n: n }); }
    });
    c.students = out; $('wh-editor').hidden = true; current = null; $('wh-result').hidden = true; save(); renderAll();
  });
  $('wh-reset').addEventListener('click', function () {
    cls().students.forEach(function (s) { s.done = false; }); current = null; $('wh-result').hidden = true; save(); renderChips(); refreshEmpty(); redraw();
  });
  $('wh-sound').addEventListener('click', function () { sound = !sound; state.sound = sound; save(); setFlag(this, sound, 'សំឡេង'); });
  $('wh-norepeat').addEventListener('click', function () { noRepeat = !noRepeat; state.noRepeat = noRepeat; save(); setFlag(this, noRepeat, 'មិនជ្រើសម្ដងទៀត'); renderChips(); refreshEmpty(); redraw(); });
  $('wh-full').addEventListener('click', function () {
    var st = $('wh-stage');
    if (document.fullscreenElement) document.exitFullscreen();
    else if (st.requestFullscreen) st.requestFullscreen();
  });
  if (!document.fullscreenEnabled) $('wh-full').hidden = true;

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
        state = { v: 1, active: ok[0].id, noRepeat: s.noRepeat !== false, sound: s.sound !== false, classes: ok };
        noRepeat = state.noRepeat; sound = state.sound; setFlag($('wh-sound'), sound, 'សំឡេង'); setFlag($('wh-norepeat'), noRepeat, 'មិនជ្រើសម្ដងទៀត');
        save(); renderAll();
      } catch (e) { alert('ឯកសារនេះមិនមែនជាឯកសារបម្រុងរបស់កង់ឈ្មោះទេ។'); }
    };
    r.readAsText(f);
  });

  noRepeat = state.noRepeat !== false; sound = state.sound !== false;
  setFlag($('wh-sound'), sound, 'សំឡេង'); setFlag($('wh-norepeat'), noRepeat, 'មិនជ្រើសម្ដងទៀត');
  renderAll();
  if (document.fonts && document.fonts.load) document.fonts.load('600 20px "Kantumruy Pro"').then(redraw);
})();
