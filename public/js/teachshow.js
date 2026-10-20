// Classroom slideshow: ink, movable spin (¼), timer, calculator.
(function () {
  const kh = (n) => String(n ?? '').replace(/\d/g, (d) => '០១២៣៤៥៦៧៨៩'[d]);
  let root, stage, slideEl, ink, ctx, i = 0, slides = [], students = [];
  let tool = 'pen', color = '#e03131', size = 4, drawing = false, cur = null, spot = null, stamp = '✔';
  let lensIco = null, lens = null, lensIn = null, lensClone = null, lensRaf = 0, lensGo = { x: 0, y: 0, z: 1 }, lensNow = { x: 0, y: 0, z: 1 }, lensOn = false, lensZoom = 2.2;
  let sizeSetter = null, toastEl = null, toastT = 0;
  let laser = [], laserRaf = 0, penKind = 'ball', hand = null;
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
    return { x: e.clientX - r.left, y: e.clientY - r.top, t: performance.now() };
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
    } else if (st.t === 'pen' && st.k && st.k !== 'ball') {
      paintPen(st);
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

  const rnd = (n) => { const x = Math.sin(n * 12.9898) * 43758.5453; return x - Math.floor(x); };
  // pen types: marker (broad, soft), brush (width follows speed), pencil (grainy), chalk (dusty)
  function paintPen(st) {
    const pts = st.p, w = st.w, k = st.k;
    const path = () => { ctx.beginPath(); pts.forEach((q, i) => (i ? ctx.lineTo(q.x, q.y) : ctx.moveTo(q.x, q.y))); if (pts.length === 1) ctx.lineTo(pts[0].x + .1, pts[0].y); };
    if (k === 'marker') { ctx.globalAlpha = .78; ctx.lineWidth = w * 2.4; path(); ctx.stroke(); return; }
    if (k === 'brush') {
      if (pts.length === 1) { ctx.beginPath(); ctx.arc(pts[0].x, pts[0].y, w * .8, 0, Math.PI * 2); ctx.fill(); return; }
      let cw = w * 1.2;
      for (let i = 1; i < pts.length; i++) {
        const a = pts[i - 1], b = pts[i], v = Math.hypot(b.x - a.x, b.y - a.y) / Math.max(1, (b.t || 0) - (a.t || 0));
        const target = w * Math.max(.4, Math.min(1.9, 1.9 - v * 1.1));
        cw += (target - cw) * .35;
        ctx.lineWidth = cw; ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
      }
      return;
    }
    if (k === 'pencil') {
      ctx.globalAlpha = .62; ctx.lineWidth = Math.max(1, w * .75); path(); ctx.stroke();
      ctx.globalAlpha = .35;
      pts.forEach((q, i) => { for (let j = 0; j < 3; j++) { const a = rnd(i * 7 + j), b = rnd(i * 13 + j + 5); ctx.fillRect(q.x + (a - .5) * w * 1.3, q.y + (b - .5) * w * 1.3, 1.2, 1.2); } });
      return;
    }
    if (k === 'chalk') {
      ctx.globalAlpha = .5; ctx.lineWidth = w * 1.1; path(); ctx.stroke();
      ctx.globalAlpha = .55;
      pts.forEach((q, i) => { for (let j = 0; j < 5; j++) { const a = rnd(i * 3 + j), b = rnd(i * 11 + j + 2); ctx.beginPath(); ctx.arc(q.x + (a - .5) * w * 1.6, q.y + (b - .5) * w * 1.6, .6 + rnd(i + j) * 1.1, 0, Math.PI * 2); ctx.fill(); } });
    }
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
  function sizeToast() {
    if (!toastEl) { toastEl = document.createElement('div'); toastEl.className = 'ts-toast'; stage.append(toastEl); }
    toastEl.textContent = `ទំហំក្បាលប៊ិច ${kh(size)}`;
    const d = document.createElement('i'); d.style.width = d.style.height = Math.max(2, size) + 'px'; d.style.background = color === '#ffffff' ? '#ccc' : color;
    toastEl.append(d);
    toastEl.classList.add('on'); clearTimeout(toastT);
    toastT = setTimeout(() => toastEl && toastEl.classList.remove('on'), 1100);
  }

  // rectangular magnifier: the text under the pointer grows smoothly inside a lens that follows the mouse
  const LW = 420, LH = 230;
  function lensBuild() {
    if (!lens) {
      lens = document.createElement('div'); lens.className = 'ts-lens';
      lensIn = document.createElement('div'); lensIn.className = 'ts-lens-in';
      lens.append(lensIn); stage.append(lens);
      lensIco = document.createElement('img'); lensIco.className = 'ts-lens-ico'; lensIco.src = '/img/magnifier.png'; lensIco.alt = ''; stage.append(lensIco);
    }
    lensIn.innerHTML = '';
    lensClone = slideEl.cloneNode(true);
    lensClone.removeAttribute('id');
    lensIn.style.width = slideEl.clientWidth + 'px'; lensIn.style.height = slideEl.clientHeight + 'px';
    lensIn.append(lensClone);
  }
  function lensMove(e) {
    if (tool !== 'zoom') return;
    if (!lens || !lensClone || lensClone.innerHTML !== slideEl.innerHTML) lensBuild();
    const r = ink.getBoundingClientRect();
    lensGo.x = e.clientX - r.left; lensGo.y = e.clientY - r.top; lensGo.z = lensZoom;
    if (!lensOn) { lensOn = true; lensNow.x = lensGo.x; lensNow.y = lensGo.y; lensNow.z = 1; lens.classList.add('on'); lensIco.classList.add('on'); }
    if (!lensRaf) lensRaf = requestAnimationFrame(lensTick);
  }
  function lensOff() {
    lensOn = false; if (lens) { lens.classList.remove('on'); lensIco.classList.remove('on'); }
  }
  function lensTick() {
    lensRaf = 0;
    if (!lens) return;
    const k = .22; // easing: the lens glides after the mouse and the zoom eases in/out
    const tz = lensOn ? lensGo.z : 1;
    lensNow.x += (lensGo.x - lensNow.x) * k; lensNow.y += (lensGo.y - lensNow.y) * k; lensNow.z += (tz - lensNow.z) * .16;
    lens.style.width = LW + 'px'; lens.style.height = LH + 'px';
    lens.style.left = (lensNow.x - LW / 2) + 'px'; lens.style.top = (lensNow.y - LH / 2) + 'px';
    lensIco.style.left = (lensNow.x + LW / 2 - 30) + 'px'; lensIco.style.top = (lensNow.y + LH / 2 - 30) + 'px';
    lensIn.style.transform = `translate(${LW / 2 - lensNow.x * lensNow.z}px, ${LH / 2 - lensNow.y * lensNow.z}px) scale(${lensNow.z})`;
    const moving = Math.abs(lensGo.x - lensNow.x) + Math.abs(lensGo.y - lensNow.y) > .3 || Math.abs(tz - lensNow.z) > .01;
    if (moving || lensOn) lensRaf = requestAnimationFrame(lensTick);
  }

  const HAND_TOOLS = ['pen', 'hi', 'line', 'arrow', 'rect', 'ellipse'];
  function makeHand() {
    const h = document.createElement('div');
    h.className = 'ts-hand'; h.hidden = true;
    h.innerHTML = '<img src="/img/hand.png" alt="" draggable="false">';
    stage.append(h);
    return h;
  }
  function handMove(e) {
    if (!hand) return;
    if (!HAND_TOOLS.includes(tool) || e.pointerType === 'touch') { hand.hidden = true; return; }
    const r = ink.getBoundingClientRect();
    hand.style.left = (e.clientX - r.left - 8) + 'px';
    hand.style.top = (e.clientY - r.top - 88) + 'px';
    hand.hidden = false;
  }

  function bindInk() {
    hand = makeHand();
    ink.addEventListener('wheel', (e) => { if (tool === 'zoom') { e.preventDefault(); lensZoom = Math.max(1.4, Math.min(4.5, lensZoom + (e.deltaY < 0 ? .25 : -.25))); lensGo.z = lensZoom; if (!lensRaf) lensRaf = requestAnimationFrame(lensTick); return; } if (sizeSetter && HAND_TOOLS.includes(tool)) { e.preventDefault(); sizeSetter(size + (e.deltaY < 0 ? 1 : -1), true); } }, { passive: false });
    ink.addEventListener('pointermove', lensMove);
    ink.addEventListener('pointerenter', lensMove);
    ink.addEventListener('pointerleave', lensOff);
    ink.addEventListener('pointermove', handMove);
    ink.addEventListener('pointerenter', handMove);
    ink.addEventListener('pointerleave', () => { if (hand) hand.hidden = true; });
    ink.addEventListener('pointerdown', () => { if (hand) hand.classList.add('writing'); });
    window.addEventListener('pointerup', () => { if (hand) hand.classList.remove('writing'); });
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
      else { drawing = true; cur = { t: tool, c: color, w: size, k: penKind, p: [p] }; }
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
    const row = document.createElement('div');
    row.className = 'ts-prow';
    const grip = document.createElement('div');
    grip.className = 'ts-pgrip'; grip.title = 'អូសដើម្បីផ្លាស់ទី: លើ · ក្រោម · ឆ្វេង · ស្តាំ';
    grip.innerHTML = '<span class="gl"><i></i><i></i><i></i><i></i><i></i><i></i></span>';
    let edge = 'top';
    try { edge = localStorage.getItem('ts_pen_edge') || 'top'; } catch { /* ignore */ }
    const M = 12, RESERVE = 88; // margin; space kept free for the tool dock on the right
    const header = () => root.querySelector('.ts-bar');
    // put the bar on an edge: top = inside the header, others float in the slide area
    const place = (w, animate) => {
      edge = w;
      const vert = w === 'left' || w === 'right';
      el.classList.toggle('vert', vert);
      el.classList.toggle('floating', w !== 'top');
      closeMenus();
      if (w === 'top') {
        el.style.left = el.style.top = '';
        header().insertBefore(el, header().querySelector('.ts-wid'));
      } else {
        if (el.parentNode !== stage) stage.append(el);
        el.classList.toggle('glide', !!animate);
        const W = stage.clientWidth, H = stage.clientHeight, bw = el.offsetWidth, bh = el.offsetHeight;
        const x = w === 'left' ? M : w === 'right' ? W - bw - M - RESERVE + 14 : (W - bw) / 2;
        const y = w === 'bottom' ? H - bh - M : Math.max(M, (H - bh) / 2);
        el.style.left = Math.max(0, x) + 'px'; el.style.top = Math.max(0, y) + 'px';
      }
      try { localStorage.setItem('ts_pen_edge', w); } catch { /* ignore */ }
    };
    const nearest = (x, y, w, h) => {
      const W = stage.clientWidth, H = stage.clientHeight;
      const d = { top: y + 56, left: x, right: W - RESERVE - (x + w), bottom: H - (y + h) }; // +56: header counts as a close edge
      const k = Object.keys(d).sort((a, b) => d[a] - d[b])[0];
      return d[k] < 90 ? k : null;
    };
    const zone = document.createElement('div');
    zone.className = 'ts-snapzone'; zone.hidden = true;
    stage.append(zone);
    const showZone = (w) => {
      if (!w) { zone.hidden = true; return; }
      const W = stage.clientWidth, H = stage.clientHeight, t = 54;
      Object.assign(zone.style, w === 'left' ? { left: '6px', top: '12%', width: t + 'px', height: '76%' }
        : w === 'right' ? { left: (W - RESERVE - t + 8) + 'px', top: '12%', width: t + 'px', height: '76%' }
          : w === 'top' ? { left: '14%', top: '4px', width: '72%', height: '44px' }
            : { left: '14%', top: (H - t - 6) + 'px', width: '72%', height: t + 'px' });
      zone.hidden = false;
    };
    let ox = 0, oy = 0, moving = false, target = null;
    grip.addEventListener('pointerdown', (e) => {
      closeMenus();
      const r = el.getBoundingClientRect(), s0 = stage.getBoundingClientRect();
      if (el.parentNode !== stage) { // lift it out of the header so it can travel
        el.classList.add('floating'); stage.append(el);
        el.style.left = (r.left - s0.left) + 'px'; el.style.top = (r.top - s0.top) + 'px';
      }
      moving = true; el.classList.remove('glide'); el.classList.add('dragging');
      const r2 = el.getBoundingClientRect();
      ox = e.clientX - r2.left; oy = e.clientY - r2.top;
      grip.setPointerCapture(e.pointerId);
      e.preventDefault();
    });
    grip.addEventListener('pointermove', (e) => {
      if (!moving) return;
      const s0 = stage.getBoundingClientRect(), r = el.getBoundingClientRect();
      const x = e.clientX - s0.left - ox, y = e.clientY - s0.top - oy;
      el.style.left = Math.max(0, Math.min(s0.width - r.width, x)) + 'px';
      el.style.top = Math.max(-50, Math.min(s0.height - r.height, y)) + 'px';
      target = nearest(x, y, r.width, r.height);
      showZone(target);
    });
    const end = () => {
      if (!moving) return;
      moving = false; el.classList.remove('dragging'); zone.hidden = true;
      if (target) place(target, true);
      else { // dropped in the open: stay put, keep fully visible
        const r = el.getBoundingClientRect(), s0 = stage.getBoundingClientRect();
        el.style.left = Math.max(0, Math.min(s0.width - r.width, r.left - s0.left)) + 'px';
        el.style.top = Math.max(0, Math.min(s0.height - r.height, r.top - s0.top)) + 'px';
      }
      target = null;
    };
    grip.addEventListener('pointerup', end);
    grip.addEventListener('pointercancel', end);
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
      if (!m.hidden) m.dataset.dir = { top: 'down', bottom: 'up', left: 'right', right: 'left' }[edge];
    };
    const setTool = (id) => {
      tool = id; spot = null; laser = []; lensOff();
      ink.style.pointerEvents = id === 'none' ? 'none' : 'auto';
      ink.style.cursor = id === 'erase' ? 'cell' : id === 'laser' || id === 'zoom' || HAND_TOOLS.includes(id) ? 'none' : 'crosshair';
      if (hand && !HAND_TOOLS.includes(id)) hand.hidden = true;
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
      b.onclick = (ev) => { ev.stopPropagation(); color = col; showDot(); cw.querySelectorAll('.ts-col').forEach((x) => x.classList.toggle('on', x === b)); sw.style.background = col; if (['none', 'erase', 'zoom'].includes(tool)) setTool('pen'); };
      if (col === color) b.classList.add('on');
      cw.append(b);
    });
    const lw = document.createElement('div'); lw.className = 'lw';
    const dot = document.createElement('i'); dot.className = 'dot';
    const rng = document.createElement('input'); rng.type = 'range'; rng.min = 1; rng.max = 30; rng.value = size; rng.title = 'ទំហំប៊ិច';
    const showDot = () => { dot.style.width = dot.style.height = Math.max(2, size) + 'px'; dot.style.background = color === '#ffffff' ? '#ccc' : color; };
    const tip = document.createElement('input'); tip.type = 'range'; tip.min = 1; tip.max = 30; tip.value = size; tip.className = 'ts-tip'; tip.title = 'ទំហំក្បាលប៊ិច';
    const setSize = (v, say) => {
      size = Math.max(1, Math.min(30, Math.round(v)));
      rng.value = tip.value = size; showDot();
      if (say) sizeToast();
    };
    sizeSetter = setSize;
    rng.oninput = () => setSize(+rng.value);
    tip.oninput = () => setSize(+tip.value);
    tip.onclick = (ev) => ev.stopPropagation();
    rng.onclick = (ev) => ev.stopPropagation();
    const lab = document.createElement('small'); lab.textContent = 'ទំហំក្បាលប៊ិច';
    lw.append(lab, rng, Object.assign(document.createElement('div'), { className: 'dotbox' }));
    lw.querySelector('.dotbox').append(dot); showDot();
    const kinds = document.createElement('div'); kinds.className = 'kinds';
    [['ball', '✒', 'ប៊ិចទូទៅ'], ['marker', '🖊', 'ម៉ាកឃ័រ'], ['brush', '🖌', 'ជក់'], ['pencil', '✏', 'ខ្មៅដៃ'], ['chalk', '▒', 'ដីស']].forEach(([id, ic, t]) => {
      const b = document.createElement('button'); b.type = 'button'; b.className = 'kb' + (id === penKind ? ' on' : ''); b.title = t;
      b.innerHTML = `<span>${ic}</span><small>${t}</small>`;
      b.onclick = (ev) => { ev.stopPropagation(); penKind = id; kinds.querySelectorAll('.kb').forEach((x) => x.classList.toggle('on', x === b)); if (tool !== 'pen') setTool('pen'); };
      kinds.append(b);
    });
    fmtMenu.append(kinds, cw, lw);

    let sw;
    const bMouse = mkBtn('none', ICONS.none, 'ចុច', () => setTool('none'));
    const bLaser = mkBtn('laser', '●', 'ចង្អុល', () => setTool('laser'));
    const bDraw = mkBtn('draw', ICONS.pen, 'គូស', () => { if (SHAPES.includes(tool)) toggle(drawMenu); else setTool(row.querySelector('[data-a=draw]').dataset.last || 'pen'); });
    const bStamp = mkBtn('stamp', stamp, 'ត្រា', () => { if (tool === 'stamp') toggle(stampMenu); else { setTool('stamp'); } });
    const bSpot = mkBtn('zoom', '<img class="mi" src="/img/magnifier.png" alt="" draggable="false">', 'ពង្រីក', () => setTool('zoom'));
    const bErase = mkBtn('erase', ICONS.erase, 'លុប', () => setTool('erase'));
    const bFmt = mkBtn('fmt', '<i class="sw"></i>', 'ពណ៌', () => toggle(fmtMenu));
    sw = bFmt.querySelector('.sw'); sw.style.background = color;
    // small arrow buttons to open the menus of draw / stamp
    const caret = (btn, m) => { const c = document.createElement('em'); c.textContent = '▾'; c.onclick = (ev) => { ev.stopPropagation(); toggle(m); }; btn.append(c); };
    caret(bDraw, drawMenu); caret(bStamp, stampMenu);
    const bUndo = mkBtn('undo', '↶', 'ត្រឡប់', undo);
    const bRedo = mkBtn('redo', '↷', 'ធ្វើវិញ', redo);
    const bClear = mkBtn('clear', '🗑', 'សម្អាត', () => clearInk(true));
    const tipWrap = document.createElement('label'); tipWrap.className = 'ts-tipw'; tipWrap.title = 'ទំហំក្បាលប៊ិច'; tipWrap.append(Object.assign(document.createElement('i'), { className: 'tdot' }), tip);
    row.append(bMouse, bLaser, bDraw, bStamp, bSpot, bErase, bFmt, tipWrap, bUndo, bRedo, bClear);
    el.append(grip, row, drawMenu, stampMenu, fmtMenu);
    header().insertBefore(el, header().querySelector('.ts-wid'));
    palette = el;
    requestAnimationFrame(() => place(edge));
    window.addEventListener('resize', () => { if (el.isConnected) place(edge); });
    palette = el;
    setTool(tool);
    syncUndo();
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
    if ((e.key === '[' || e.key === ']') && sizeSetter) sizeSetter(size + (e.key === ']' ? 1 : -1), true);
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
