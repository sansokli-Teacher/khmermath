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
  var TEACHER = 'លោកគ្រូ សាន សុខលី';
  function S() { return state.set || (state.set = { dur: 5, theme: 'a', fw: true, mystery: false, speak: false }); }
  function teacher() { return clean(S().teacher || ''); }   // only what the teacher typed; the default name is just a hint in the box

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
        // the label starts inside the wheel (left-aligned) and runs outward, centred in the band between the hub and the rim:
        // Safari ignores textAlign='right' for some text, which pushed names off the rim (white on white)
        var rim = r - 14, inner = r * 0.27, band = rim - inner;
        var size = Math.max(13, Math.min(40, Math.floor((inner + band / 2) * a * 0.72)));
        ctx.font = '600 ' + size + 'px "Kantumruy Pro", sans-serif';
        ctx.fillStyle = '#fff'; ctx.textAlign = 'left'; ctx.textBaseline = 'middle';
        ctx.shadowColor = 'rgba(0,0,0,.35)'; ctx.shadowBlur = 3;
        var name = list[i].n, w = ctx.measureText(name).width;
        if (w > band && w > 0) { size = Math.max(11, Math.floor(size * band / w)); ctx.font = '600 ' + size + 'px "Kantumruy Pro", sans-serif'; w = ctx.measureText(name).width; }
        ctx.fillText(name, inner + (w > 0 && w < band ? (band - w) / 2 : 0), 0, band);
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
  var fwSides = false, fwParts = [], fwEnd = 0, fwOn = false, fwNext = 0, fwRandom = false, fwDim = null, fwHues = [8, 40, 52, 130, 190, 280, 330];
  function reduceMotion() { return window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches; }
  function fwBurst(x, y, n) {
    var hue = fwHues[Math.floor(Math.random() * fwHues.length)];
    for (var i = 0; i < n; i++) {
      var a = Math.PI * 2 * i / n + Math.random() * 0.2, v = 2.2 + Math.random() * 3.6;
      fwParts.push({ x: x, y: y, vx: Math.cos(a) * v, vy: Math.sin(a) * v, life: 1, hue: hue + Math.random() * 25 - 12 });
    }
  }
  function fwFrame(now) {
    if (!fwOn) return;
    var g = fwDim.g, W = fwDim.W, H = fwDim.H;
    g.globalCompositeOperation = 'destination-out'; g.fillStyle = 'rgba(0,0,0,.22)'; g.fillRect(0, 0, W, H);
    g.globalCompositeOperation = 'lighter';
    if (fwRandom && now < fwEnd && now > fwNext) { fwBurst(fwSides ? W * (Math.random() < 0.5 ? 0.02 + Math.random() * 0.14 : 0.84 + Math.random() * 0.14) : W * (0.12 + Math.random() * 0.76), H * (0.1 + Math.random() * 0.5), 46); fwNext = now + 260 + Math.random() * 260; }
    fwParts = fwParts.filter(function (p) { return p.life > 0.02; });
    fwParts.forEach(function (p) {
      p.x += p.vx; p.y += p.vy; p.vy += 0.06; p.vx *= 0.985; p.vy *= 0.985; p.life -= 0.013;
      g.fillStyle = 'hsla(' + p.hue + ',100%,60%,' + Math.max(0, p.life) + ')';
      g.beginPath(); g.arc(p.x, p.y, 2.6, 0, 7); g.fill();
    });
    if (now < fwEnd || fwParts.length) requestAnimationFrame(fwFrame); else { fwOn = false; fwRandom = false; g.clearRect(0, 0, W, H); }
  }
  function fwStart() {
    if (fwOn) return;
    var cv = $('wh-fw'), dpr = Math.min(2, window.devicePixelRatio || 1), W = cv.clientWidth, H = cv.clientHeight;
    cv.width = W * dpr; cv.height = H * dpr;
    var g = cv.getContext('2d'); g.setTransform(dpr, 0, 0, dpr, 0, 0);
    fwDim = { g: g, W: W, H: H }; fwOn = true; fwParts = []; requestAnimationFrame(fwFrame);
  }
  function fireworks(sides) { if (reduceMotion()) return; $('wh-fw').classList.toggle('behind', !!sides); fwSides = !!sides; fwStart(); fwRandom = true; fwNext = 0; fwEnd = performance.now() + (sides ? 2600 : 3600); }   // sides: keep bursts in the margins so they never cover the group names
  function miniBurst(x, y) { if (reduceMotion()) return; $('wh-fw').classList.remove('behind'); fwStart(); fwBurst(x, y, 22); fwEnd = Math.max(fwEnd, performance.now() + 700); }
  function stopFireworks() { fwOn = false; fwRandom = false; fwParts = []; var cv = $('wh-fw'); cv.getContext('2d').clearRect(0, 0, cv.width, cv.height); }

  /* drum roll (noise bursts that speed up) and cymbal crash */
  function noise(t, len, type, freq, vol) {
    var buf = audio.createBuffer(1, Math.max(1, Math.floor(audio.sampleRate * len)), audio.sampleRate), d = buf.getChannelData(0);
    for (var i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
    var src = audio.createBufferSource(), f = audio.createBiquadFilter(), g = audio.createGain();
    src.buffer = buf; f.type = type; f.frequency.value = freq; g.gain.setValueAtTime(vol, t); g.gain.exponentialRampToValueAtTime(0.001, t + len);
    src.connect(f); f.connect(g); g.connect(audio.destination); src.start(t);
  }
  function drumRoll(ms) {
    if (!sound) return;
    try {
      audio = audio || new (window.AudioContext || window.webkitAudioContext)();
      var t = audio.currentTime, end = t + ms / 1000, gap = 0.12;
      while (t < end - 0.05) { noise(t, 0.05, 'lowpass', 500 + Math.random() * 200, 0.22); t += gap; gap = Math.max(0.03, gap * 0.93); }
    } catch (e) {}
  }
  function cymbal() {
    if (!sound) return;
    try { audio = audio || new (window.AudioContext || window.webkitAudioContext)(); noise(audio.currentTime, 0.7, 'highpass', 5000, 0.18); tone([784, 988], 0.07, 0.35); } catch (e) {}
  }

  /* ---------- spinning ---------- */
  function spin() {
    if (spinning) return;
    var list = eligible(), n = list.length; if (!n) return;
    wl = list; closePop(); $('wh-last').hidden = true;
    var pick = Math.floor(Math.random() * n), a = Math.PI * 2 / n;
    var target = -(pick * a + (Math.random() - 0.5) * a * 0.7);   // slice `pick` is centred at pick*a from the top; land inside it
    var turns = 5 + Math.floor(Math.random() * 3);
    var from = angle, norm = ((target - from) % (Math.PI * 2) + Math.PI * 2) % (Math.PI * 2);
    var to = from + turns * Math.PI * 2 + norm, dur = S().dur * 1000 * (0.9 + Math.random() * 0.2), t0 = performance.now(), lastSlice = -1;
    spinning = true; $('wh-spin').disabled = true;
    try { if (window.KmSound && sound) { KmSound.unlock(); KmSound.loop('question', 0.32); } } catch (e) {}
    (function frame(now) {
      var t = Math.min(1, (now - t0) / dur), e = 1 - Math.pow(1 - t, 4);
      angle = from + (to - from) * e; draw();
      var sl = Math.floor(((-angle % (Math.PI * 2)) + Math.PI * 2 + a / 2) / a); if (sl !== lastSlice) { lastSlice = sl; tone([900], 0.04, 0.025); }
      if (t < 1) return requestAnimationFrame(frame);
      spinning = false; $('wh-spin').disabled = false; angle = to % (Math.PI * 2); draw();
      try { if (window.KmSound && sound) { KmSound.stop(); KmSound.sfx('reveal'); } } catch (e) {}
      finish(list[pick]);
    })(t0);
  }
  function showLast(on) {
    var el = $('wh-last'); el.hidden = !on || !current; if (el.hidden) return;
    el.innerHTML = ''; el.appendChild(document.createTextNode('សិស្សដែលត្រូវបានជ្រើសចុងក្រោយ៖')); var b = document.createElement('b'); b.textContent = current.n; el.appendChild(b);
  }
  function finish(student) {
    current = student; if (noRepeat) current.done = true;
    try {
      var c = cls(); (c.hist = c.hist || []).push({ n: current.n, t: Date.now() }); if (c.hist.length > 300) c.hist.shift();
      save(); renderChips(); refreshEmpty(); renderHist();
    } catch (e) {}
    pendingReveal = !!S().mystery; showLast(!pendingReveal); openPop();       // the name is shown first, effects after
    try { if (!pendingReveal) celebrate(); } catch (e) {}
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
    pendingReveal = false; showLast(true); $('wh-winner').textContent = current.n; $('wh-reveal').hidden = true; $('wh-again').hidden = false; $('wh-absent').hidden = false;
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

  /* ---------- Excel (.xlsx) export: a small writer, no library ---------- */
  var CRC = null;
  function crc32(b) {
    if (!CRC) { CRC = []; for (var n = 0; n < 256; n++) { var c = n; for (var k = 0; k < 8; k++) c = c & 1 ? 0xEDB88320 ^ (c >>> 1) : c >>> 1; CRC[n] = c >>> 0; } }
    var x = 0xFFFFFFFF; for (var i = 0; i < b.length; i++) x = CRC[(x ^ b[i]) & 255] ^ (x >>> 8); return (x ^ 0xFFFFFFFF) >>> 0;
  }
  function zipStore(files) {                       // files: [{name, data: Uint8Array}] -> Uint8Array (no compression)
    var enc = new TextEncoder(), parts = [], central = [], off = 0;
    files.forEach(function (f) {
      var nm = enc.encode(f.name), crc = crc32(f.data), h = new DataView(new ArrayBuffer(30));
      h.setUint32(0, 0x04034b50, true); h.setUint16(4, 20, true); h.setUint16(6, 0x0800, true); h.setUint16(10, 0, true); h.setUint16(12, 33, true);
      h.setUint32(14, crc, true); h.setUint32(18, f.data.length, true); h.setUint32(22, f.data.length, true); h.setUint16(26, nm.length, true);
      parts.push(new Uint8Array(h.buffer), nm, f.data);
      var d = new DataView(new ArrayBuffer(46));
      d.setUint32(0, 0x02014b50, true); d.setUint16(4, 20, true); d.setUint16(6, 20, true); d.setUint16(8, 0x0800, true); d.setUint16(12, 0, true); d.setUint16(14, 33, true);
      d.setUint32(16, crc, true); d.setUint32(20, f.data.length, true); d.setUint32(24, f.data.length, true); d.setUint16(28, nm.length, true); d.setUint32(42, off, true);
      central.push(new Uint8Array(d.buffer), nm);
      off += 30 + nm.length + f.data.length;
    });
    var csize = central.reduce(function (a, b) { return a + b.length; }, 0), e = new DataView(new ArrayBuffer(22));
    e.setUint32(0, 0x06054b50, true); e.setUint16(8, files.length, true); e.setUint16(10, files.length, true); e.setUint32(12, csize, true); e.setUint32(16, off, true);
    var all = parts.concat(central, [new Uint8Array(e.buffer)]), tot = all.reduce(function (a, b) { return a + b.length; }, 0), out = new Uint8Array(tot), p = 0;
    all.forEach(function (b) { out.set(b, p); p += b.length; }); return out;
  }
  function xesc(t) { return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function colName(i) { var s = ''; for (i++; i > 0; i = Math.floor((i - 1) / 26)) s = String.fromCharCode(65 + (i - 1) % 26) + s; return s; }
  function sheetXml(sh) {
    var rows = sh.rows.map(function (row, r) {
      return '<row r="' + (r + 1) + '">' + row.map(function (v, c) {
        var ref = colName(c) + (r + 1), st = r === 0 ? ' s="1"' : '';
        return typeof v === 'number' ? '<c r="' + ref + '"' + st + '><v>' + v + '</v></c>' : '<c r="' + ref + '"' + st + ' t="inlineStr"><is><t xml:space="preserve">' + xesc(v) + '</t></is></c>';
      }).join('') + '</row>';
    }).join('');
    var cols = '<cols>' + (sh.widths || []).map(function (w, i) { return '<col min="' + (i + 1) + '" max="' + (i + 1) + '" width="' + w + '" customWidth="1"/>'; }).join('') + '</cols>';
    return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">' + cols + '<sheetData>' + rows + '</sheetData></worksheet>';
  }
  function buildXlsx(sheets) {
    var enc = new TextEncoder(), X = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>', f = [];
    var ns = 'xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"', rel = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships';
    f.push(['[Content_Types].xml', X + '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>' + sheets.map(function (s, i) { return '<Override PartName="/xl/worksheets/sheet' + (i + 1) + '.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'; }).join('') + '</Types>']);
    f.push(['_rels/.rels', X + '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="' + rel + '/officeDocument" Target="xl/workbook.xml"/></Relationships>']);
    f.push(['xl/workbook.xml', X + '<workbook ' + ns + ' xmlns:r="' + rel + '"><sheets>' + sheets.map(function (s, i) { return '<sheet name="' + xesc(s.name) + '" sheetId="' + (i + 1) + '" r:id="rId' + (i + 1) + '"/>'; }).join('') + '</sheets></workbook>']);
    f.push(['xl/_rels/workbook.xml.rels', X + '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + sheets.map(function (s, i) { return '<Relationship Id="rId' + (i + 1) + '" Type="' + rel + '/worksheet" Target="worksheets/sheet' + (i + 1) + '.xml"/>'; }).join('') + '<Relationship Id="rId' + (sheets.length + 1) + '" Type="' + rel + '/styles" Target="styles.xml"/></Relationships>']);
    f.push(['xl/styles.xml', X + '<styleSheet ' + ns + '><fonts count="2"><font><sz val="11"/><name val="Calibri"/></font><font><b/><sz val="11"/><name val="Calibri"/></font></fonts><fills count="2"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill></fills><borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders><cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs><cellXfs count="2"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/><xf numFmtId="0" fontId="1" fillId="0" borderId="0" xfId="0" applyFont="1"/></cellXfs><cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles></styleSheet>']);
    sheets.forEach(function (s, i) { f.push(['xl/worksheets/sheet' + (i + 1) + '.xml', sheetXml(s)]); });
    return zipStore(f.map(function (x) { return { name: x[0], data: enc.encode(x[1]) }; }));
  }
  function download(bytes, name) {
    var a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([bytes], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' }));
    a.download = name; document.body.appendChild(a); a.click(); a.remove(); setTimeout(function () { URL.revokeObjectURL(a.href); }, 1500);
  }
  function stamp(t) { var d = new Date(t), z = function (n) { return ('0' + n).slice(-2); }; return d.getFullYear() + '-' + z(d.getMonth() + 1) + '-' + z(d.getDate()) + ' ' + z(d.getHours()) + ':' + z(d.getMinutes()); }
  function classSheets(c, tag) {
    var hist = c.hist || [], by = {}; c.students.forEach(function (s) { by[s.n] = s; });
    var cnt = histCounts(hist);
    var a = [['ល.រ', 'ឈ្មោះសិស្ស', 'ភេទ', 'កាលបរិច្ឆេទ និងម៉ោង']].concat(hist.map(function (x, i) { return [i + 1, x.n, by[x.n] && by[x.n].g ? G_WORD[by[x.n].g] : '', stamp(x.t)]; }));
    var b = [['ល.រ', 'ឈ្មោះសិស្ស', 'ភេទ', 'ចំនួនដងដែលត្រូវបានជ្រើស', 'វត្តមាន']].concat(c.students.map(function (s, i) { return [i + 1, s.n, s.g ? G_WORD[s.g] : '', cnt[s.n] || 0, s.off ? 'អវត្តមាន' : 'មាន']; }));
    return [{ name: tag + 'សរុប', rows: b, widths: [6, 30, 8, 22, 12] }, { name: tag + 'តាមលំដាប់', rows: a, widths: [6, 30, 8, 22] }];
  }
  function sheetName(n, used) { var b = clean(n).replace(/[\\\/?*\[\]:]/g, '').slice(0, 31) || 'Sheet', k = 1, out = b; while (used[out]) out = b.slice(0, 28) + '_' + (++k); used[out] = 1; return out; }
  function exportXlsx(all) {
    var list = all ? state.classes : [cls()], sheets = [], used = {};
    list.forEach(function (c) {
      classSheets(c, all ? '' : '').forEach(function (sh, i) { sheets.push({ name: sheetName(all ? c.name + (i ? ' ·លំដាប់' : ' ·សរុប') : sh.name, used), rows: sh.rows, widths: sh.widths }); });
    });
    var d = new Date(), z = function (n) { return ('0' + n).slice(-2); };
    download(buildXlsx(sheets), 'កង់ឈ្មោះ-' + (all ? 'គ្រប់ថ្នាក់' : clean(cls().name).replace(/[\\/:*?"<>|]/g, '')) + '-' + d.getFullYear() + z(d.getMonth() + 1) + z(d.getDate()) + '.xlsx');
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
    try { localStorage.setItem('km_wheel_last_groups', JSON.stringify({ t: Date.now(), cls: cls().name, groups: groups.map(function (g) { return g.map(function (p) { return p.n; }); }) })); } catch (e) {}   // for ហ្គេមក្រុម
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
  /* ---------- result picture (PNG) with khmermath.org branding ---------- */
  var FONT = '"Kantumruy Pro", "Noto Sans Khmer", sans-serif';
  function rr(g, x, y, w, h, r, tl, tr, br, bl) {            // rounded rectangle path (each corner radius optional)
    tl = tl === undefined ? r : tl; tr = tr === undefined ? r : tr; br = br === undefined ? r : br; bl = bl === undefined ? r : bl;
    g.beginPath(); g.moveTo(x + tl, y); g.lineTo(x + w - tr, y); g.quadraticCurveTo(x + w, y, x + w, y + tr); g.lineTo(x + w, y + h - br);
    g.quadraticCurveTo(x + w, y + h, x + w - br, y + h); g.lineTo(x + bl, y + h); g.quadraticCurveTo(x, y + h, x, y + h - bl); g.lineTo(x, y + tl); g.quadraticCurveTo(x, y, x + tl, y); g.closePath();
  }
  function posterCanvas(o) {                                  // o: {heading, sub, groups:[{title, items:[{n,g}]}], colors}
    var W = 1600, pad = 56, gap = 26, n = o.groups.length, cols = n <= 1 ? 1 : n <= 4 ? 2 : 3;
    var cw = (W - pad * 2 - gap * (cols - 1)) / cols, headH = 80, lineH = 46, cpad = 18, bannerH = 250, footH = 110;
    var rows = []; for (var i = 0; i < n; i += cols) rows.push(o.groups.slice(i, i + cols));
    var rowH = rows.map(function (r) { return headH + Math.max.apply(null, r.map(function (g) { return g.items.length; })) * lineH + cpad * 2; });
    var H = bannerH + 40 + rowH.reduce(function (a, b) { return a + b; }, 0) + gap * (rows.length - 1) + 40 + footH, dpr = 2;
    var cv = document.createElement('canvas'); cv.width = W * dpr; cv.height = H * dpr; var g = cv.getContext('2d'); g.scale(dpr, dpr);
    var bg = g.createLinearGradient(0, 0, 0, H); bg.addColorStop(0, '#eaf5f2'); bg.addColorStop(1, '#fdf6e8'); g.fillStyle = bg; g.fillRect(0, 0, W, H);
    // banner
    var bn = g.createLinearGradient(0, 0, W, bannerH); bn.addColorStop(0, '#1f6f66'); bn.addColorStop(0.6, '#2d8f7e'); bn.addColorStop(1, '#3aa68f');
    g.fillStyle = bn; g.fillRect(0, 0, W, bannerH);
    for (var k = 0; k < 46; k++) {                           // confetti
      var seed = (k * 9301 + 49297) % 233280 / 233280, seed2 = (k * 7919 + 1237) % 10007 / 10007;
      g.fillStyle = ['#ffd43b', '#ff8787', '#74c0fc', '#b2f2bb', '#ffffff'][k % 5]; g.globalAlpha = 0.55;
      g.save(); g.translate(seed * W, seed2 * bannerH); g.rotate(k); g.fillRect(-7, -3, 14, 6); g.restore();
    }
    g.globalAlpha = 1; g.textAlign = 'center'; g.textBaseline = 'middle';
    g.fillStyle = '#fff'; g.font = '700 70px ' + FONT; g.fillText(o.heading, W / 2, o.teacher ? 84 : 98);
    g.font = '500 33px ' + FONT; g.globalAlpha = 0.92; g.fillText(o.sub, W / 2, o.teacher ? 154 : 178);
    if (o.teacher) { g.font = '600 34px ' + FONT; g.globalAlpha = 1; g.fillText('គ្រូបង្រៀន៖ ' + o.teacher, W / 2, 204); }
    g.globalAlpha = 1;
    // cards
    var y = bannerH + 40;
    rows.forEach(function (r, ri) {
      r.forEach(function (grp, ci) {
        var x = pad + ci * (cw + gap), h = rowH[ri], col = o.colors[(ri * cols + ci) % o.colors.length];
        g.save(); g.shadowColor = 'rgba(0,0,0,.18)'; g.shadowBlur = 22; g.shadowOffsetY = 8; g.fillStyle = '#fff'; rr(g, x, y, cw, h, 22); g.fill(); g.restore();
        g.fillStyle = col; rr(g, x, y, cw, headH, 22, 22, 22, 0, 0); g.fill();
        g.fillStyle = '#fff'; g.textAlign = 'left'; g.font = '700 36px ' + FONT; g.fillText(grp.title, x + 26, y + headH / 2 + 2);
        g.textAlign = 'right'; g.font = '500 28px ' + FONT; g.globalAlpha = 0.9; g.fillText(khNum(grp.items.length) + ' នាក់', x + cw - 24, y + headH / 2 + 2); g.globalAlpha = 1;
        grp.items.forEach(function (it, i) {
          var ty = y + headH + cpad + i * lineH + lineH / 2;
          g.textAlign = 'left'; g.fillStyle = col; g.font = '700 26px ' + FONT; g.fillText(khNum(i + 1) + '.', x + 24, ty);
          var dx = x + 76;
          if (it.g) { g.fillStyle = it.g === 'f' ? '#d6336c' : '#1c7ed6'; g.beginPath(); g.arc(dx + 8, ty, 8, 0, 7); g.fill(); dx += 28; }
          var size = 33; g.font = '500 ' + size + 'px ' + FONT; while (g.measureText(it.n).width > x + cw - 20 - dx && size > 12) { size -= 2; g.font = '500 ' + size + 'px ' + FONT; }
          g.fillStyle = '#1b2733'; g.fillText(it.n, dx, ty);
        });
      });
      y += rowH[ri] + gap;
    });
    // footer brand
    var fy = H - footH / 2 - 6;
    g.strokeStyle = 'rgba(31,111,102,.25)'; g.lineWidth = 2; g.beginPath(); g.moveTo(pad, H - footH); g.lineTo(W - pad, H - footH); g.stroke();
    g.fillStyle = '#12263a'; rr(g, W / 2 - 215, fy - 30, 60, 60, 14); g.fill();
    g.fillStyle = '#fff'; g.textAlign = 'center'; g.font = '700 38px ' + FONT; g.fillText('√', W / 2 - 185, fy + 2);
    g.fillStyle = '#e0a13a'; rr(g, W / 2 - 172, fy - 4, 14, 14, 3); g.fill();
    g.textAlign = 'left'; g.fillStyle = '#1f6f66'; g.font = '700 42px ' + FONT; g.fillText('khmermath.org', W / 2 - 140, fy - 2);
    g.fillStyle = '#5b6b7b'; g.font = '500 24px ' + FONT; g.fillText('កង់ចាប់ឈ្មោះ · គណិតវិទ្យាខ្មែរ', W / 2 - 140, fy + 34);
    return cv;
  }
  function khDate() { var d = new Date(); return khNum(d.getDate() + '/' + (d.getMonth() + 1) + '/' + d.getFullYear()); }
  var lastBlocks = null;
  function isPhone() { return (window.matchMedia && matchMedia('(pointer: coarse)').matches) || /Android|iPhone|iPad|iPod|Mobile|FBAN|FBAV|Telegram|Line\//i.test(navigator.userAgent); }
  function saveBlob(blob, name) {
    var a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = name; document.body.appendChild(a); a.click(); a.remove(); setTimeout(function () { URL.revokeObjectURL(a.href); }, 4000);
  }
  function savePicture(blob, name) {
    if (!isPhone()) return saveBlob(blob, name);
    var old = document.getElementById('wh-pv'); if (old) old.remove();      // phones: preview with long-press save + share button (in-app browsers often block downloads)
    var url = URL.createObjectURL(blob), box = document.createElement('div'), p = document.createElement('p'), img = document.createElement('img'), row = document.createElement('div');
    box.id = 'wh-pv'; box.className = 'wh-pv'; p.textContent = 'ចុចសង្កត់លើរូបភាព រួចជ្រើស «រក្សាទុករូបភាព» ឬប្រើប៊ូតុងខាងលើ។'; img.src = url; img.alt = 'លទ្ធផលបែងចែកក្រុម'; row.className = 'wh-row';
    function btn(t, cls, f) { var b = document.createElement('button'); b.type = 'button'; b.className = 'btn btn-sm ' + cls; b.textContent = t; b.addEventListener('click', f); row.appendChild(b); }
    var file = null; try { file = new File([blob], name, { type: 'image/png' }); } catch (e) {}
    if (file && navigator.canShare && navigator.canShare({ files: [file] })) btn('ចែករំលែក / រក្សាទុក', 'btn-primary', function () { navigator.share({ files: [file], title: 'khmermath.org' }).catch(function () {}); });
    btn('ទាញយក', 'btn-ghost', function () { saveBlob(blob, name); });
    btn('បិទ', 'btn-ghost', function () { box.remove(); URL.revokeObjectURL(url); });
    var x = document.createElement('button'); x.type = 'button'; x.className = 'wh-x wh-x-pv'; x.setAttribute('aria-label', 'បិទ'); x.textContent = '✕';
    x.addEventListener('click', function () { box.remove(); URL.revokeObjectURL(url); });
    box.addEventListener('click', function (e) { if (e.target === box) { box.remove(); URL.revokeObjectURL(url); } });
    box.appendChild(x); box.appendChild(p); box.appendChild(img); box.appendChild(row); document.body.appendChild(box);
  }
  function downloadPoster() {
    if (!lastBlocks) return;
    var single = lastBlocks.length === 1 && /^លំដាប់/.test(lastBlocks[0].title), total = lastBlocks.reduce(function (a, b) { return a + b.list.length; }, 0), btn = $('wh-gpng');
    var make = function () {
      var cv = posterCanvas({
        heading: single ? 'លំដាប់ចៃដន្យ' : 'បែងចែកក្រុមរួចរាល់!',
        sub: cls().name + '  ·  ' + khNum(total) + ' នាក់  ·  ' + khDate(), teacher: teacher(), colors: colors(),
        groups: lastBlocks.map(function (b) { return { title: single ? 'លំដាប់' : b.title.split(' · ')[0], items: b.list.map(function (p) { return { n: p.n, g: p.g }; }) }; })
      });
      cv.toBlob(function (b) {
        var z = function (x) { return ('0' + x).slice(-2); }, d = new Date(), name = 'khmermath-' + (single ? 'order' : 'groups') + '-' + d.getFullYear() + z(d.getMonth() + 1) + z(d.getDate()) + '.png';
        btn.textContent = '⬇ ទាញយក PNG';
        if (!b) { alert('មិនអាចបង្កើតរូបភាពបានទេ។'); return; }
        savePicture(b, name);
      }, 'image/png');
    };
    btn.textContent = 'កំពុងបង្កើត…';
    (document.fonts && document.fonts.load ? Promise.all([document.fonts.load('700 30px "Kantumruy Pro"', 'សិស្សក'), document.fonts.load('500 30px "Kantumruy Pro"', 'សិស្សក')]) : Promise.resolve()).then(make, make);
  }

  /* popup: one drum roll per group - only that card shuffles, then it locks with a crash and a firework */
  var gRun = 0, gAgain = null, gSkip = false;
  function makeCard(b, i) {
    var d = document.createElement('div'), h = document.createElement('b'), ol = document.createElement('ol');
    d.className = 'wh-g wait'; d.style.setProperty('--i', i); d.style.setProperty('--gc', colors()[i % colors().length]); h.textContent = b.title; d.appendChild(h); d.appendChild(ol); d._ol = ol; return d;
  }
  function setNames(card, list, ph) {
    card._ol.innerHTML = '';
    list.forEach(function (p) { var li = document.createElement('li'); li.textContent = ph ? '• • •' : (p.g ? (p.g === 'f' ? '♀ ' : '♂ ') : '') + p.n; if (ph) li.className = 'ph'; card._ol.appendChild(li); });
  }
  function groupPop(blocks, again) {
    gAgain = again; gSkip = false; var id = ++gRun, box = $('wh-ggrid'), n = blocks.length, reduce = reduceMotion();
    var cards = blocks.map(makeCard), sizes = blocks.map(function (b) { return b.list.length; });
    var remaining = [].concat.apply([], blocks.map(function (b) { return b.list; }));
    var per = reduce ? 0 : Math.max(900, Math.min(1800, 12000 / n)), pause = reduce ? 0 : 450;
    lastBlocks = blocks; $('wh-gcardbox').classList.remove('final'); $('wh-gsub').hidden = true; $('wh-gbrand').hidden = true; $('wh-gpng').hidden = true;
    closePop(); stopFireworks(); box.innerHTML = ''; box.className = 'wh-ggrid cols-' + (n <= 1 ? 1 : n <= 4 ? 2 : 3); cards.forEach(function (c, i) { setNames(c, blocks[i].list, true); box.appendChild(c); });
    $('wh-gpop').hidden = false; ['wh-gagain', 'wh-gcopy2'].forEach(function (b) { $(b).disabled = true; }); $('wh-gskip').hidden = n < 2;
    var cur = -1, phase = 'start', t0 = 0, last = 0;
    function lock(i, burst) {
      var card = cards[i]; card.className = 'wh-g done'; setNames(card, blocks[i].list, false);
      var ids = {}; blocks[i].list.forEach(function (p) { ids[p.n] = 1; }); remaining = remaining.filter(function (p) { return !ids[p.n]; });
      if (burst) { cymbal(); var r = card.getBoundingClientRect(); if (S().fw) miniBurst(r.right - 28, r.top + 22); }
    }
    function finale() {
      var total = blocks.reduce(function (a, b) { return a + b.list.length; }, 0), single = n === 1 && /^លំដាប់/.test(blocks[0].title);
      $('wh-gsmall').textContent = (single ? 'លំដាប់ចៃដន្យ' : 'បែងចែកក្រុមរួចរាល់!') + ' 🎉'; $('wh-gcardbox').classList.add('final');
      $('wh-gsub').textContent = cls().name + ' · ' + khNum(total) + ' នាក់ · ' + khDate() + (teacher() ? '\nគ្រូបង្រៀន៖ ' + teacher() : ''); $('wh-gsub').hidden = false; $('wh-gbrand').hidden = false; $('wh-gpng').hidden = false;
      $('wh-gskip').hidden = true;
      ['wh-gagain', 'wh-gcopy2'].forEach(function (b) { $(b).disabled = false; });
      if (S().fw) { tone([523, 659, 784, 1047], 0.08, 0.3); fireworks(true); }
      $('wh-gagain').focus({ preventScroll: true });
    }
    $('wh-gskip').onclick = function () { gSkip = true; };
    (function frame(now) {
      if (id !== gRun) return;
      if (gSkip) { for (var k = Math.max(cur, 0); k < n; k++) if (cards[k].className !== 'wh-g done') lock(k, false); return finale(); }
      if (phase === 'start' || (phase === 'pause' && now - t0 >= pause)) {
        cur++; if (cur >= n) return finale();
        phase = 'roll'; t0 = now; cards[cur].className = 'wh-g active';
        $('wh-gsmall').textContent = 'កំពុងបែងចែក ក្រុមទី ' + khNum(cur + 1) + '…';
        cards[cur].scrollIntoView({ block: 'nearest' }); drumRoll(per);
      }
      if (phase === 'roll') {
        if (now - t0 >= per) { lock(cur, true); phase = 'pause'; t0 = now; }
        else if (now - last > 80) { last = now; setNames(cards[cur], shuffle(remaining).slice(0, sizes[cur]), false); }
      }
      requestAnimationFrame(frame);
    })(performance.now());
  }
  function closeGroupPop() { gRun++; gSkip = true; $('wh-gpop').hidden = true; stopFireworks(); }
  function khNum(n) { return String(n).replace(/\d/g, function (d) { return '០១២៣៤៥៦៧៨៩'[d]; }); }

  /* ---------- gender panel: a row per student with ប្រុស / ស្រី buttons ---------- */
  function renderGenderPanel() {
    var c = cls(), ul = $('wh-glist'), todo = c.students.filter(function (s) { return !s.g; }).length;
    $('wh-gphint').textContent = todo ? 'នៅសល់ ' + khNum(todo) + ' នាក់ មិនទាន់កំណត់ភេទ។ ចុច «ប្រុស» ឬ «ស្រី» នៅមុខឈ្មោះនីមួយៗ (ចុចម្ដងទៀតដើម្បីលុប)។' : 'បានកំណត់ភេទគ្រប់គ្នាហើយ ✓';
    ul.innerHTML = '';
    c.students.forEach(function (s, i) {
      var li = document.createElement('li'), nm = document.createElement('span'), gb = document.createElement('span');
      li.className = s.g ? '' : 'todo'; nm.className = 'nm'; gb.className = 'gb';
      var no = document.createElement('small'); no.textContent = khNum(i + 1) + '.'; nm.appendChild(no); nm.appendChild(document.createTextNode(s.n));
      [['m', 'ប្រុស'], ['f', 'ស្រី']].forEach(function (x) {
        var b = document.createElement('button'); b.type = 'button'; b.className = x[0]; b.textContent = x[1]; b.setAttribute('aria-pressed', s.g === x[0] ? 'true' : 'false');
        b.addEventListener('click', function () { s.g = s.g === x[0] ? undefined : x[0]; save(); renderGenderPanel(); renderChips(); refreshEmpty(); redraw(); });
        gb.appendChild(b);
      });
      li.appendChild(nm); li.appendChild(gb); ul.appendChild(li);
    });
  }
  function openGenderPanel(scroll) {
    if (!cls().students.length) return;
    renderGenderPanel(); $('wh-gpanel').hidden = false; if (scroll) $('wh-gpanel').scrollIntoView({ block: 'nearest', behavior: 'smooth' });
  }

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
  function renderAll() { renderClasses(); renderChips(); refreshEmpty(); renderHist(); redraw(); $('wh-groups').hidden = true; $('wh-copy').hidden = true; $('wh-gpanel').hidden = true; }
  function setFlag(btn, on, label) { btn.setAttribute('aria-pressed', on ? 'true' : 'false'); btn.textContent = label + (on ? ': បើក' : ': បិទ'); }
  function setMode(m) {
    clickMode = m; $('wh-mode-off').setAttribute('aria-pressed', m === 'off'); $('wh-mode-g').setAttribute('aria-pressed', m === 'g'); renderChips();
  }

  $('wh-spin').addEventListener('click', spin);
  $('wh-again').addEventListener('click', spin);
  $('wh-close').addEventListener('click', closePop);
  $('wh-x1').addEventListener('click', closePop);
  $('wh-x2').addEventListener('click', function () { closeGroupPop(); });
  $('wh-pop').addEventListener('click', function (e) { if (e.target === this) closePop(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { if (!$('wh-gpop').hidden) closeGroupPop(); else if (!$('wh-pop').hidden) closePop(); } });
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
  $('wh-setg').addEventListener('click', function () { openGenderPanel(true); });
  $('wh-gdone').addEventListener('click', function () { $('wh-gpanel').hidden = true; });
  $('wh-cancel').addEventListener('click', function () { $('wh-editor').hidden = true; });
  $('wh-save').addEventListener('click', function () {
    var c = cls(), old = {}; c.students.forEach(function (s) { old[s.n] = s; });
    var seen = {}, out = [];
    $('wh-text').value.split(/\r?\n/).forEach(function (line) {
      var p = parseLine(line); if (!p || seen[p.n]) return; seen[p.n] = 1;
      var prev = old[p.n]; if (prev) { if (p.g) prev.g = p.g; out.push(prev); } else out.push(p);   // keep absent/done marks of names that were already there
    });
    c.students = out; $('wh-editor').hidden = true; current = null; closePop(); save(); renderAll();
    if (out.some(function (x) { return !x.g; })) openGenderPanel(true); else $('wh-gpanel').hidden = true;   // right after pasting: ask for each name's gender
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
    runGroups();
  });
  function runGroups() {
    var g = makeGroups(); if (!g) { $('wh-groups').hidden = false; $('wh-groups').textContent = 'មិនទាន់មានសិស្សទេ។'; return; }
    showGroups(g);
    groupPop(g.map(function (x, i) { return { title: 'ក្រុមទី ' + khNum(i + 1) + ' · ' + khNum(x.length) + ' នាក់', list: x }; }), runGroups);
  }
  $('wh-gagain').addEventListener('click', function () { if (gAgain) gAgain(); });
  $('wh-gclose').addEventListener('click', closeGroupPop);
  $('wh-gpng').addEventListener('click', downloadPoster);
  $('wh-gpop').addEventListener('click', function (e) { if (e.target === this) closeGroupPop(); });
  $('wh-gcopy2').addEventListener('click', function () { $('wh-copy').click(); var b = this; b.textContent = 'បានចម្លង ✓'; setTimeout(function () { b.textContent = 'ចម្លង'; }, 1600); });
  $('wh-order').addEventListener('click', function () {
    var p = shuffle(present()); if (!p.length) return;
    var box = $('wh-groups'); box.innerHTML = ''; box.hidden = false;
    var d = document.createElement('div'), h = document.createElement('b'), ol = document.createElement('ol');
    d.className = 'wh-g'; h.textContent = 'លំដាប់ចៃដន្យ · ' + khNum(p.length) + ' នាក់'; d.appendChild(h);
    p.forEach(function (s) { var li = document.createElement('li'); li.textContent = s.n; ol.appendChild(li); });
    d.appendChild(ol); box.appendChild(d);
    lastGroups = h.textContent + '\n' + p.map(function (s, k) { return (k + 1) + '. ' + s.n; }).join('\n') + '\n';
    $('wh-copy').hidden = false;
    groupPop([{ title: 'លំដាប់ចៃដន្យ · ' + khNum(p.length) + ' នាក់', list: p }], function () { $('wh-order').click(); });
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
  $('wh-hxlsx').addEventListener('click', function () { exportXlsx(false); });
  $('wh-hxall').addEventListener('click', function () { exportXlsx(true); });
  $('wh-teacher').addEventListener('input', function () { S().teacher = this.value; save(); });
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
    $('wh-teacher').value = set.teacher || ''; $('wh-teacher').placeholder = TEACHER;
    $('wh-fwon').checked = set.fw !== false; $('wh-mystery').checked = !!set.mystery; $('wh-speak').checked = !!set.speak;
    if (window.speechSynthesis) { findVoice(); if (speechSynthesis.addEventListener) speechSynthesis.addEventListener('voiceschanged', findVoice); }
  })();
  setFlag($('wh-sound'), sound, 'សំឡេង'); setFlag($('wh-norepeat'), noRepeat, 'មិនជ្រើសម្ដងទៀត');
  renderAll();
  if (document.fonts && document.fonts.load) Promise.all([document.fonts.load('600 20px "Kantumruy Pro"', 'សិស្សក'), document.fonts.load('700 30px "Kantumruy Pro"', 'សិស្សក'), document.fonts.load('500 30px "Kantumruy Pro"', 'សិស្សក')]).then(redraw, redraw);
})();
