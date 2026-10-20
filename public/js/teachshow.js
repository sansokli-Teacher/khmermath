// Classroom slideshow: ink, movable spin (¼), timer, calculator.
(function () {
  const kh = (n) => String(n ?? '').replace(/\d/g, (d) => '០១២៣៤៥៦៧៨៩'[d]);
  let root, stage, slideEl, ink, ctx, i = 0, slides = [], students = [];
  let tool = 'pen', color = '#e03131', size = 4, drawing = false, cur = null, spot = null, stamp = '✔';
  let laser = [], laserRaf = 0;
  let strokes = [], undoS = [], redoS = [], palette = null;
  let floats = [];

  function math(el) {
    if (window.renderMathInElement) {
      try { renderMathInElement(el, { throwOnError: false, strict: false, macros: { '\\arc': '\\overset{\\frown}{#1}' }, delimiters: [{ left: '\\(', right: '\\)', display: false }, { left: '\\[', right: '\\]', display: true }] }); } catch {}
    }
  }

  function show(n, depth) {
    i = Math.max(0, Math.min(slides.length - 1, n));
    const s = slides[i] || { html: '' };
    slideEl.className = 'ts-slide' + (s.k ? ` ts-${s.k}` : '') + (s.c ? ` ts-${s.c}` : '');
    slideEl.innerHTML = s.html || '';
    math(slideEl);
    const fits = fitText(0.72);
    if (!fits && (depth || 0) < 4 && splitSlide(i)) return show(i, (depth || 0) + 1);
    if (!fits) fitText(0.4);
    const lab = root.querySelector('.ts-page');
    if (lab) lab.textContent = `${kh(i + 1)} / ${kh(slides.length)}`;
    clearInk(false);
  }

  // a slide that is too long is cut into two pages (title kept on both)
  function splitSlide(idx) {
    const s = slides[idx];
    const box = document.createElement('div');
    box.innerHTML = s.html;
    const nodes = [...box.childNodes].filter((n) => n.nodeType === 1 || (n.textContent || '').trim());
    const isHead = (n) => n.nodeType === 1 && (n.matches('h1,h2') || n.classList.contains('ts-kicker'));
    const head = nodes.filter(isHead), body = nodes.filter((n) => !isHead(n));
    if (body.length < 2) return false;
    const cut = Math.ceil(body.length / 2);
    const out = (arr) => head.concat(arr).map((n) => (n.nodeType === 1 ? n.outerHTML : n.textContent)).join('');
    const a = { ...s, html: out(body.slice(0, cut)) };
    const b = { ...s, html: out(body.slice(cut)) };
    delete a.c; delete b.c;
    slides.splice(idx, 1, a, b);
    return true;
  }

  // shrink the text (down to `floor` of its size) until the slide fits; true if it fits
  function fitText(floor) {
    if (!slideEl) return true;
    slideEl.style.fontSize = '';
    const base = parseFloat(getComputedStyle(slideEl).fontSize) || 24;
    let px = base;
    const over = () => slideEl.scrollHeight > slideEl.clientHeight + 2 || slideEl.scrollWidth > slideEl.clientWidth + 2;
    for (let k = 0; k < 30 && over() && px > base * (floor || 0.72); k++) {
      px *= 0.94;
      slideEl.style.fontSize = px + 'px';
    }
    return !over();
  }

  function fitInk() {
    const r = stage.getBoundingClientRect();
    const dpr = Math.min(2, window.devicePixelRatio || 1);
    ink.width = Math.floor(r.width * dpr);
    ink.height = Math.floor(r.height * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    redraw();
  }

  function clearInk(user) {
    if (!ctx) return;
    if (user) { if (strokes.length) { undoS.push({ del: strokes }); redoS = []; } strokes = []; }
    else { strokes = []; undoS = []; redoS = []; }
    cur = null;
    redraw();
    syncUndo();
  }

  function pos(e) {
    const r = ink.getBoundingClientRect();
    return { x: e.clientX - r.left, y: e.clientY - r.top };
  }

  function paint(st) {
    ctx.save();
    ctx.lineCap = 'round'; ctx.lineJoin = 'round';
    ctx.strokeStyle = st.c; ctx.fillStyle = st.c; ctx.lineWidth = st.w;
    if (st.t === 'hi') { ctx.globalAlpha = .35; ctx.lineWidth = st.w * 4; ctx.lineCap = 'butt'; }
    if (st.t === 'stamp') {
      ctx.font = '700 46px "Times New Roman", system-ui, sans-serif';
      ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      ctx.fillText(st.ch, st.p[0].x, st.p[0].y);
    } else if (st.t === 'pen' || st.t === 'hi') {
      ctx.beginPath();
      st.p.forEach((q, k) => (k ? ctx.lineTo(q.x, q.y) : ctx.moveTo(q.x, q.y)));
      if (st.p.length === 1) ctx.lineTo(st.p[0].x + .1, st.p[0].y);
      ctx.stroke();
    } else {
      const [a, b] = [st.p[0], st.p[st.p.length - 1]];
      ctx.beginPath();
      if (st.t === 'rect') ctx.rect(a.x, a.y, b.x - a.x, b.y - a.y);
      else if (st.t === 'ellipse') ctx.ellipse((a.x + b.x) / 2, (a.y + b.y) / 2, Math.abs(b.x - a.x) / 2, Math.abs(b.y - a.y) / 2, 0, 0, Math.PI * 2);
      else {
        ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y);
        if (st.t === 'arrow') {
          const ang = Math.atan2(b.y - a.y, b.x - a.x), h = 10 + st.w * 3;
          ctx.moveTo(b.x, b.y); ctx.lineTo(b.x - h * Math.cos(ang - .45), b.y - h * Math.sin(ang - .45));
          ctx.moveTo(b.x, b.y); ctx.lineTo(b.x - h * Math.cos(ang + .45), b.y - h * Math.sin(ang + .45));
        }
      }
      ctx.stroke();
    }
    ctx.restore();
  }

  function redraw() {
    if (!ctx) return;
    const r = ink.getBoundingClientRect();
    ctx.clearRect(0, 0, r.width, r.height);
    strokes.forEach(paint);
    if (cur) paint(cur);
    if (tool === 'laser' && laser.length) {
      const now = performance.now();
      laser.forEach((q, k) => {
        const age = Math.min(1, (now - q.t) / 700);
        ctx.save();
        ctx.globalAlpha = (1 - age) * (k === laser.length - 1 ? 1 : .6);
        ctx.fillStyle = color === '#ffffff' ? '#ff2d2d' : color;
        ctx.shadowColor = ctx.fillStyle; ctx.shadowBlur = 18;
        ctx.beginPath(); ctx.arc(q.x, q.y, (k === laser.length - 1 ? 9 : 6) * (1 - age * .6), 0, Math.PI * 2); ctx.fill();
        ctx.restore();
      });
    }
    if (tool === 'spot' && spot) {
      ctx.save();
      ctx.fillStyle = 'rgba(0,0,0,.72)';
      ctx.beginPath(); ctx.rect(0, 0, r.width, r.height);
      ctx.arc(spot.x, spot.y, 110, 0, Math.PI * 2, true);
      ctx.fill('evenodd');
      ctx.restore();
    }
  }

  function near(st, p) {
    const pts = st.t === 'pen' || st.t === 'hi' || st.t === 'stamp' ? st.p : [st.p[0], st.p[st.p.length - 1]];
    if (st.t === 'stamp') return Math.hypot(pts[0].x - p.x, pts[0].y - p.y) < 34;
    if (pts.length === 1) return Math.hypot(pts[0].x - p.x, pts[0].y - p.y) < 14;
    const xs = pts.map((q) => q.x), ys = pts.map((q) => q.y);
    if (st.t === 'pen' || st.t === 'hi') return pts.some((q, k) => k && distSeg(p, pts[k - 1], q) < 14);
    if (st.t === 'line' || st.t === 'arrow') return distSeg(p, pts[0], pts[1]) < 14;
    const x0 = Math.min(...xs), x1 = Math.max(...xs), y0 = Math.min(...ys), y1 = Math.max(...ys);
    const inside = p.x > x0 - 10 && p.x < x1 + 10 && p.y > y0 - 10 && p.y < y1 + 10;
    return inside && (p.x < x0 + 10 || p.x > x1 - 10 || p.y < y0 + 10 || p.y > y1 - 10);
  }
  function distSeg(p, a, b) {
    const dx = b.x - a.x, dy = b.y - a.y, l = dx * dx + dy * dy || 1;
    const t = Math.max(0, Math.min(1, ((p.x - a.x) * dx + (p.y - a.y) * dy) / l));
    return Math.hypot(p.x - (a.x + t * dx), p.y - (a.y + t * dy));
  }

  function undo() {
    const a = undoS.pop(); if (!a) return;
    if (a.add) strokes = strokes.filter((x) => x !== a.add); else strokes = strokes.concat(a.del);
    redoS.push(a); redraw(); syncUndo();
  }
  function redo() {
    const a = redoS.pop(); if (!a) return;
    if (a.add) strokes.push(a.add); else strokes = strokes.filter((x) => !a.del.includes(x));
    undoS.push(a); redraw(); syncUndo();
  }
  function syncUndo() {
    if (!palette) return;
    palette.querySelector('[data-a=undo]').disabled = !undoS.length;
    palette.querySelector('[data-a=redo]').disabled = !redoS.length;
    palette.querySelector('[data-a=clear]').disabled = !strokes.length;
  }

  function laserTick() {
    laserRaf = 0;
    const now = performance.now();
    laser = laser.filter((q) => now - q.t < 700);
    redraw();
    if (tool === 'laser' && laser.length) laserRaf = requestAnimationFrame(laserTick);
  }

  const SHAPES = ['pen', 'hi', 'line', 'arrow', 'rect', 'ellipse'];
  function bindInk() {
    const down = (e) => {
      if (e.button && e.button !== 0) return;
      const p = pos(e);
      closeMenus();
      if (tool === 'laser') { laser.push({ ...p, t: performance.now() }); if (!laserRaf) laserRaf = requestAnimationFrame(laserTick); }
      else if (tool === 'spot') { spot = p; drawing = true; redraw(); }
      else if (tool === 'stamp') {
        const st = { t: 'stamp', c: color, w: size, ch: stamp, p: [p] };
        strokes.push(st); undoS.push({ add: st }); redoS = []; redraw(); syncUndo();
      } else if (tool === 'erase') { drawing = true; eraseAt(p); }
      else { drawing = true; cur = { t: tool, c: color, w: size, p: [p] }; }
      ink.setPointerCapture && ink.setPointerCapture(e.pointerId);
      e.preventDefault();
    };
    const move = (e) => {
      if (tool === 'laser') {
        laser.push({ ...pos(e), t: performance.now() });
        if (laser.length > 40) laser.shift();
        if (!laserRaf) laserRaf = requestAnimationFrame(laserTick);
        return;
      }
      if (tool === 'spot' && !drawing) return;
      if (!drawing) return;
      const p = pos(e);
      if (tool === 'spot') { spot = p; redraw(); }
      else if (tool === 'erase') eraseAt(p);
      else if (cur) {
        if (cur.t === 'pen' || cur.t === 'hi') cur.p.push(p); else cur.p = [cur.p[0], p];
        redraw();
      }
      e.preventDefault();
    };
    const up = () => {
      if (!drawing) return;
      drawing = false;
      if (cur) { strokes.push(cur); undoS.push({ add: cur }); redoS = []; cur = null; redraw(); syncUndo(); }
    };
    function eraseAt(p) {
      const hit = strokes.filter((st) => near(st, p));
      if (!hit.length) return;
      strokes = strokes.filter((st) => !hit.includes(st));
      undoS.push({ del: hit }); redoS = []; redraw(); syncUndo();
    }
    ink.addEventListener('pointerdown', down);
    ink.addEventListener('pointermove', move);
    window.addEventListener('pointerup', up);
  }

  function makeFloat(kind, title, body, opt) {
    const el = document.createElement('div');
    el.className = `ts-float ts-${kind}`;
    el.style.left = opt.x;
    el.style.top = opt.y;
    el.style.width = opt.w;
    if (opt.h) el.style.height = opt.h;
    const xbtn = document.createElement('button');
    xbtn.type = 'button'; xbtn.className = 'ts-fx'; xbtn.textContent = '✕';
    xbtn.onclick = () => { el.hidden = true; };
    const bar = document.createElement('div');
    bar.className = 'ts-fbar';
    bar.innerHTML = `<b>${title}</b>`;
    bar.append(xbtn);
    const inner = document.createElement('div');
    inner.className = 'ts-fin';
    inner.append(body);
    const rs = document.createElement('div');
    rs.className = 'ts-rs';
    el.append(bar, inner, rs);
    stage.append(el);
    drag(el, bar);
    resize(el, rs);
    floats.push(el);
    return el;
  }

  function drag(el, bar) {
    let ox = 0, oy = 0, dragging = false;
    bar.addEventListener('pointerdown', (e) => {
      if (e.target.closest('button,input,select')) return;
      dragging = true;
      const r = el.getBoundingClientRect(), s = stage.getBoundingClientRect();
      ox = e.clientX - r.left; oy = e.clientY - r.top;
      bar.setPointerCapture(e.pointerId);
      e.preventDefault();
    });
    bar.addEventListener('pointermove', (e) => {
      if (!dragging) return;
      const s = stage.getBoundingClientRect();
      el.style.left = Math.max(0, Math.min(s.width - 80, e.clientX - s.left - ox)) + 'px';
      el.style.top = Math.max(0, Math.min(s.height - 40, e.clientY - s.top - oy)) + 'px';
    });
    bar.addEventListener('pointerup', () => { dragging = false; });
  }

  function resize(el, handle) {
    let sx = 0, sy = 0, sw = 0, sh = 0, on = false;
    handle.addEventListener('pointerdown', (e) => {
      on = true;
      const r = el.getBoundingClientRect();
      sx = e.clientX; sy = e.clientY; sw = r.width; sh = r.height;
      handle.setPointerCapture(e.pointerId);
      e.preventDefault(); e.stopPropagation();
    });
    handle.addEventListener('pointermove', (e) => {
      if (!on) return;
      el.style.width = Math.max(180, sw + (e.clientX - sx)) + 'px';
      el.style.height = Math.max(140, sh + (e.clientY - sy)) + 'px';
    });
    handle.addEventListener('pointerup', () => { on = false; });
  }

  function miniSpin(names) {
    const wrap = document.createElement('div');
    wrap.className = 'ts-spin';
    const cv = document.createElement('canvas');
    cv.width = 360; cv.height = 360;
    const hub = document.createElement('button');
    hub.type = 'button'; hub.className = 'ts-hub'; hub.textContent = 'បង្វិល';
    const out = document.createElement('div');
    out.className = 'ts-spin-out';
    wrap.append(cv, hub, out);
    const c = cv.getContext('2d');
    let ang = 0, spin = false, list = names.slice();
    const pal = ['#e8590c', '#1c7ed6', '#2f9e44', '#ae3ec9', '#f08c00', '#0c8599', '#d6336c', '#5f3dc4'];
    function draw() {
      const n = list.length || 1, W = cv.width, r = W / 2 - 4, a = Math.PI * 2 / n;
      c.clearRect(0, 0, W, W); c.save(); c.translate(W / 2, W / 2); c.rotate(ang);
      for (let k = 0; k < n; k++) {
        c.beginPath(); c.moveTo(0, 0); c.arc(0, 0, r, k * a - Math.PI / 2 - a / 2, k * a - Math.PI / 2 + a / 2); c.closePath();
        c.fillStyle = pal[k % pal.length]; c.fill();
        c.save(); c.rotate(k * a - Math.PI / 2);
        c.fillStyle = '#fff'; c.font = '600 16px Kantumruy Pro, sans-serif'; c.textAlign = 'left'; c.textBaseline = 'middle';
        c.fillText(list[k] || '—', r * 0.28, 0, r * 0.62);
        c.restore();
      }
      c.restore();
    }
    hub.onclick = () => {
      if (spin || !list.length) return;
      const pick = Math.floor(Math.random() * list.length);
      const a = Math.PI * 2 / list.length;
      const from = ang, to = from + Math.PI * 8 - (pick * a);
      const t0 = performance.now(); spin = true;
      const frame = (now) => {
        const t = Math.min(1, (now - t0) / 2800);
        ang = from + (to - from) * (1 - Math.pow(1 - t, 3)); draw();
        if (t < 1) return requestAnimationFrame(frame);
        spin = false; out.textContent = list[pick];
      };
      requestAnimationFrame(frame);
    };
    draw();
    return wrap;
  }

  function timerBox() {
    const wrap = document.createElement('div');
    wrap.className = 'ts-timer';
    let left = 300, run = false, t0 = 0, remain0 = 0, scale = 1;
    const face = document.createElement('div');
    face.className = 'ts-tface';
    const fmt = () => {
      const s = Math.max(0, Math.round(left));
      face.textContent = `${String(Math.floor(s / 60)).padStart(2, '0')}:${String(s % 60).padStart(2, '0')}`;
    };
    fmt();
    let raf;
    const tick = (now) => {
      if (!run) return;
      left = Math.max(0, remain0 - (now - t0) / 1000);
      fmt();
      if (left <= 0) { run = false; face.classList.add('done'); return; }
      raf = requestAnimationFrame(tick);
    };
    const row = document.createElement('div');
    row.className = 'ts-trow';
    const btn = (lab, fn) => { const b = document.createElement('button'); b.type = 'button'; b.textContent = lab; b.onclick = fn; return b; };
    const start = btn('ចាប់ផ្ដើម', () => {
      if (run) { run = false; return; }
      face.classList.remove('done');
      run = true; t0 = performance.now(); remain0 = left;
      raf = requestAnimationFrame(tick);
    });
    row.append(
      btn('−១នាទី', () => { left = Math.max(10, left - 60); fmt(); remain0 = left; t0 = performance.now(); }),
      btn('+១នាទី', () => { left += 60; fmt(); remain0 = left; t0 = performance.now(); }),
      start,
      btn('កំណត់ឡើងវិញ', () => { run = false; left = 300; fmt(); face.classList.remove('done'); }),
    );
    const sz = document.createElement('input');
    sz.type = 'range'; sz.min = '0.7'; sz.max = '2.2'; sz.step = '0.1'; sz.value = '1';
    sz.oninput = () => { scale = +sz.value; face.style.transform = `scale(${scale})`; };
    wrap.append(face, row, sz);
    return wrap;
  }

  function calcBox() {
    const wrap = document.createElement('div');
    wrap.className = 'ts-calc';
    const scr = document.createElement('input');
    scr.type = 'text'; scr.readOnly = true; scr.value = '0';
    let cur = '0', op = null, acc = null, fresh = true;
    const put = (v) => { scr.value = v; };
    const keys = ['7', '8', '9', '÷', '4', '5', '6', '×', '1', '2', '3', '−', '0', '.', '±', '+', '√', 'C', '='];
    const grid = document.createElement('div');
    grid.className = 'ts-ckeys';
    const apply = () => {
      const b = parseFloat(cur);
      if (acc == null || !op) { acc = b; return; }
      if (op === '+') acc += b;
      else if (op === '−') acc -= b;
      else if (op === '×') acc *= b;
      else if (op === '÷') acc = b === 0 ? NaN : acc / b;
      cur = String(acc);
      put(cur);
    };
    keys.forEach((k) => {
      const b = document.createElement('button');
      b.type = 'button'; b.textContent = k;
      b.onclick = () => {
        if (/^\d$/.test(k) || k === '.') {
          if (fresh) { cur = k === '.' ? '0.' : k; fresh = false; } else if (!(k === '.' && cur.includes('.'))) cur += k;
          put(cur); return;
        }
        if (k === 'C') { cur = '0'; acc = null; op = null; fresh = true; put(cur); return; }
        if (k === '±') { cur = String(-(parseFloat(cur) || 0)); put(cur); return; }
        if (k === '√') { cur = String(Math.sqrt(Math.abs(parseFloat(cur) || 0))); put(cur); acc = parseFloat(cur); fresh = true; return; }
        if (k === '=') { apply(); op = null; fresh = true; return; }
        apply(); op = k; fresh = true;
      };
      grid.append(b);
    });
    wrap.append(scr, grid);
    return wrap;
  }

  function toolbar() {
    const bar = document.createElement('div');
    bar.className = 'ts-bar';
    const mk = (cls, lab, fn) => { const b = document.createElement('button'); b.type = 'button'; b.className = cls; b.textContent = lab; b.onclick = fn; return b; };
    const nav = document.createElement('div');
    nav.className = 'ts-nav';
    nav.append(
      mk('', '←', () => show(i - 1)),
      Object.assign(document.createElement('span'), { className: 'ts-page', textContent: '' }),
      mk('', '→', () => show(i + 1)),
    );
    const end = document.createElement('div');
    end.className = 'ts-wid';
    end.append(mk('ts-fs', '⛶', toggleFs), mk('ts-exit', '✕', close));
    bar.append(nav, end);
    return bar;
  }

  // Zoom-style "Draw" toolbar: a bar you can drag, with drop-down menus
  const ICONS = { none: '☝', pen: '✎', hi: '🖍', line: '／', arrow: '➚', rect: '▭', ellipse: '◯', erase: '⌫', stamp: '✔', spot: '◉', draw: '✎' };
  const NAMES = { pen: 'ប៊ិច', hi: 'គំនូស', line: 'បន្ទាត់', arrow: 'ព្រួញ', rect: 'ចតុកោណ', ellipse: 'ពងក្រពើ' };
  const COLORS = ['#e03131', '#1c7ed6', '#2f9e44', '#f08c00', '#212529', '#ffffff'];
  const STAMPS = ['✔', '✘', '★', '♥', '?', '➜'];

  function closeMenus() { if (palette) palette.querySelectorAll('.ts-menu').forEach((m) => { m.hidden = true; }); }

  function penPalette() {
    const el = document.createElement('div');
    el.className = 'ts-pen';
    el.style.left = '12px';
    const grip = document.createElement('div');
    grip.className = 'ts-pgrip'; grip.title = 'អូសដើម្បីផ្លាស់ទី';
    const gl = document.createElement('span'); gl.className = 'gl'; gl.textContent = '⋮⋮';
    const gb = document.createElement('div'); gb.className = 'gb';
    const pref = (() => { try { return JSON.parse(localStorage.getItem('ts_pen') || '{}'); } catch { return {}; } })();
    let scale = pref.scale || 1, vert = !!pref.vert, where = 'bottom';
    const save = () => { try { localStorage.setItem('ts_pen', JSON.stringify({ scale, vert })); } catch { /* ignore */ } };
    const gbtn = (t, title, fn) => { const b = document.createElement('button'); b.type = 'button'; b.textContent = t; b.title = title; b.onclick = (ev) => { ev.stopPropagation(); fn(); }; gb.append(b); return b; };
    const apply = () => {
      el.classList.toggle('vert', vert);
      el.style.transform = `scale(${scale})`;
      el.style.transformOrigin = 'top left';
    };
    const place = (w) => {
      where = w;
      if (w === 'left' || w === 'right') vert = true; else vert = false;
      apply(); save();
      requestAnimationFrame(() => {
        const r = el.getBoundingClientRect(), W = stage.clientWidth, H = stage.clientHeight;
        const x = w === 'left' ? 12 : w === 'right' ? W - r.width - 90 : (W - r.width) / 2;
        const y = w === 'top' ? 12 : w === 'bottom' ? H - r.height - 14 : (H - r.height) / 2;
        el.style.left = Math.max(0, x) + 'px'; el.style.top = Math.max(0, y) + 'px';
      });
    };
    const order = ['bottom', 'top', 'left', 'right'];
    gbtn('⇄', 'ផ្ដេក / បញ្ឈរ', () => { vert = !vert; apply(); save(); keepInside(); });
    gbtn('⤒', 'ប្ដូរទីតាំង (ក្រោម/លើ/ឆ្វេង/ស្តាំ)', () => place(order[(order.indexOf(where) + 1) % order.length]));
    gbtn('A−', 'តូចជាង', () => { scale = Math.max(.7, +(scale - .15).toFixed(2)); apply(); save(); keepInside(); });
    gbtn('A+', 'ធំជាង', () => { scale = Math.min(1.6, +(scale + .15).toFixed(2)); apply(); save(); keepInside(); });
    gbtn('–', 'លាក់', () => hide());
    grip.append(gl, gb);
    const keepInside = () => requestAnimationFrame(() => {
      const r = el.getBoundingClientRect(), s = stage.getBoundingClientRect();
      el.style.left = Math.max(0, Math.min(s.width - r.width, r.left - s.left)) + 'px';
      el.style.top = Math.max(0, Math.min(s.height - r.height, r.top - s.top)) + 'px';
    });
    const pill = document.createElement('button');
    pill.type = 'button'; pill.className = 'ts-pill'; pill.textContent = '✎'; pill.title = 'បង្ហាញឧបករណ៍គូស'; pill.hidden = true;
    const hide = () => {
      closeMenus();
      const r = el.getBoundingClientRect(), s = stage.getBoundingClientRect();
      pill.style.left = Math.max(0, Math.min(s.width - 52, r.left - s.left)) + 'px';
      pill.style.top = Math.max(0, Math.min(s.height - 52, r.top - s.top)) + 'px';
      el.hidden = true; pill.hidden = false;
    };
    pill.onclick = () => { pill.hidden = true; el.hidden = false; keepInside(); };
    stage.append(pill);
    const row = document.createElement('div');
    row.className = 'ts-prow';
    const mkBtn = (a, icon, label, fn) => {
      const b = document.createElement('button');
      b.type = 'button'; b.dataset.a = a;
      b.innerHTML = `<span class="ic">${icon}</span><small>${label}</small>`;
      b.onclick = (ev) => { ev.stopPropagation(); fn(b); };
      return b;
    };
    const menu = (cls) => { const m = document.createElement('div'); m.className = 'ts-menu ' + cls; m.hidden = true; return m; };
    const toggle = (m) => {
      const was = !m.hidden; closeMenus(); m.hidden = was;
      if (!m.hidden) { // open upward when the bar is low, otherwise downward
        const r = el.getBoundingClientRect(), s = stage.getBoundingClientRect();
        m.classList.toggle('down', r.top - s.top < 230);
        m.classList.toggle('rt', r.left - s.left > s.width / 2);
      }
    };
    const setTool = (id) => {
      tool = id; spot = null; laser = [];
      ink.style.pointerEvents = id === 'none' ? 'none' : 'auto';
      ink.style.cursor = id === 'erase' ? 'cell' : id === 'spot' || id === 'laser' ? 'none' : 'crosshair';
      row.querySelectorAll('[data-a]').forEach((x) => x.classList.toggle('on', x.dataset.a === id || (x.dataset.a === 'draw' && SHAPES.includes(id))));
      redraw();
    };

    // Draw (shapes) menu
    const drawMenu = menu('m-draw');
    SHAPES.forEach((id) => {
      const b = document.createElement('button'); b.type = 'button';
      b.innerHTML = `<span class="ic">${ICONS[id]}</span> ${NAMES[id]}`;
      b.onclick = (ev) => { ev.stopPropagation(); setTool(id); const d = row.querySelector('[data-a=draw]'); d.dataset.last = id; d.querySelector('.ic').textContent = ICONS[id]; closeMenus(); };
      drawMenu.append(b);
    });
    // Stamp menu
    const stampMenu = menu('m-stamp');
    STAMPS.forEach((ch) => {
      const b = document.createElement('button'); b.type = 'button'; b.className = 'stp'; b.textContent = ch;
      b.onclick = (ev) => { ev.stopPropagation(); stamp = ch; setTool('stamp'); row.querySelector('[data-a=stamp] .ic').textContent = ch; closeMenus(); };
      stampMenu.append(b);
    });
    // Format menu: colour + thickness
    const fmtMenu = menu('m-fmt');
    const cw = document.createElement('div'); cw.className = 'cw';
    COLORS.forEach((col) => {
      const b = document.createElement('button'); b.type = 'button'; b.className = 'ts-col'; b.style.background = col; b.title = col;
      b.onclick = (ev) => { ev.stopPropagation(); color = col; cw.querySelectorAll('.ts-col').forEach((x) => x.classList.toggle('on', x === b)); sw.style.background = col; if (['none', 'erase', 'spot'].includes(tool)) setTool('pen'); };
      if (col === color) b.classList.add('on');
      cw.append(b);
    });
    const lw = document.createElement('div'); lw.className = 'lw';
    [2, 4, 8, 14].forEach((w) => {
      const b = document.createElement('button'); b.type = 'button'; b.className = 'lwb'; b.title = w + 'px';
      b.innerHTML = `<i style="height:${w}px"></i>`;
      b.onclick = (ev) => { ev.stopPropagation(); size = w; lw.querySelectorAll('.lwb').forEach((x) => x.classList.toggle('on', x === b)); };
      if (w === size) b.classList.add('on');
      lw.append(b);
    });
    fmtMenu.append(cw, lw);

    let sw;
    const bMouse = mkBtn('none', ICONS.none, 'ចុច', () => setTool('none'));
    const bLaser = mkBtn('laser', '●', 'ចង្អុល', () => setTool('laser'));
    const bDraw = mkBtn('draw', ICONS.pen, 'គូស', () => { if (SHAPES.includes(tool)) toggle(drawMenu); else setTool(row.querySelector('[data-a=draw]').dataset.last || 'pen'); });
    const bStamp = mkBtn('stamp', stamp, 'ត្រា', () => { if (tool === 'stamp') toggle(stampMenu); else { setTool('stamp'); } });
    const bSpot = mkBtn('spot', ICONS.spot, 'ភ្លើង', () => setTool('spot'));
    const bErase = mkBtn('erase', ICONS.erase, 'លុប', () => setTool('erase'));
    const bFmt = mkBtn('fmt', '<i class="sw"></i>', 'ពណ៌', () => toggle(fmtMenu));
    sw = bFmt.querySelector('.sw'); sw.style.background = color;
    // small arrow buttons to open the menus of draw / stamp
    const caret = (btn, m) => { const c = document.createElement('em'); c.textContent = '▾'; c.onclick = (ev) => { ev.stopPropagation(); toggle(m); }; btn.append(c); };
    caret(bDraw, drawMenu); caret(bStamp, stampMenu);
    const bUndo = mkBtn('undo', '↶', 'ត្រឡប់', undo);
    const bRedo = mkBtn('redo', '↷', 'ធ្វើវិញ', redo);
    const bClear = mkBtn('clear', '🗑', 'សម្អាត', () => clearInk(true));
    row.append(bMouse, bLaser, bDraw, bStamp, bSpot, bErase, bFmt, bUndo, bRedo, bClear);
    el.append(grip, row, drawMenu, stampMenu, fmtMenu);
    stage.append(el);
    palette = el;
    setTool(tool);
    syncUndo();
    apply();
    place(vert ? 'left' : 'bottom');
    drag(el, grip);
    return el;
  }

  // movable tools on the right corner
  function dock() {
    const d = document.createElement('div');
    d.className = 'ts-dock';
    const items = [['wspin', '🎡', 'កង់ចាប់ឈ្មោះ'], ['wtime', '⏱', 'ម៉ោង'], ['wcalc', '∑', 'ម៉ាស៊ីនគិតលេខ']];
    items.forEach(([cls, ic, t]) => {
      const b = document.createElement('button');
      b.type = 'button'; b.title = t; b.innerHTML = `<span>${ic}</span><small>${t.split(' ')[0]}</small>`;
      b.onclick = () => { const f = root.querySelector('.ts-float.ts-' + cls); if (f) { f.hidden = !f.hidden; if (!f.hidden) stage.append(f); b.classList.toggle('on', !f.hidden); } };
      d.append(b);
    });
    stage.append(d);
  }

  function open(opt) {
    slides = [...((window.TEACH_SLIDES && window.TEACH_SLIDES[`${opt.grade}-${opt.lesson}`]) || [])];
    if (!slides.length) return Exam.notify('មិនទាន់មានស្លាយ។');
    students = (opt.students || []).map((s) => `${s.surname || ''} ${s.first_name || ''}`.trim()).filter(Boolean);
    close();
    root = document.getElementById('teach-show');
    root.hidden = false;
    root.innerHTML = '';
    document.body.classList.add('teach-show-on');
    root.append(toolbar());
    stage = document.createElement('div');
    stage.className = 'ts-stage';
    slideEl = document.createElement('div');
    slideEl.className = 'ts-slide';
    ink = document.createElement('canvas');
    ink.className = 'ts-ink';
    stage.append(slideEl, ink);
    root.append(stage);
    const names = students.length ? students : ['សិស្ស ក', 'សិស្ស ខ', 'សិស្ស គ'];
    makeFloat('wspin', 'កង់ចាប់ឈ្មោះ', miniSpin(names), { x: '60%', y: '4%', w: '28%', h: '78%' }).hidden = true;
    makeFloat('wtime', 'ម៉ោង', timerBox(), { x: '62%', y: '4%', w: '24%' }).hidden = true;
    makeFloat('wcalc', 'ម៉ាស៊ីនគិតលេខ', calcBox(), { x: '60%', y: '40%', w: '260px' }).hidden = true;
    ctx = ink.getContext('2d');
    bindInk();
    penPalette();
    dock();
    requestAnimationFrame(() => { fitInk(); show(opt.start || 0); });
    window.addEventListener('resize', onResize);
    window.addEventListener('keydown', keys);
  }

  function onResize() { fitInk(); show(i); }

  function keys(e) {
    if (root && root.hidden) return;
    if (e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === ' ') { e.preventDefault(); show(i + 1); }
    if (e.key === 'ArrowLeft' || e.key === 'PageUp') { e.preventDefault(); show(i - 1); }
    if (e.key === 'Escape') close();
  }

  function toggleFs() {
    try {
      if (document.fullscreenElement) document.exitFullscreen();
      else (root.requestFullscreen || root.webkitRequestFullscreen || (() => {})).call(root);
    } catch (e) { /* not supported (e.g. iPhone) */ }
  }

  function close() {
    try { if (document.fullscreenElement) document.exitFullscreen(); } catch (e) { /* ignore */ }
    window.removeEventListener('keydown', keys);
    window.removeEventListener('resize', onResize);
    document.body.classList.remove('teach-show-on');
    if (root) { root.hidden = true; root.innerHTML = ''; }
    floats = [];
    palette = null;
  }

  window.TeachShow = { open, close, isOpen: () => root && !root.hidden };
})();
