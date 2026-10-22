// Classroom slideshow: ink, movable spin (¼), timer, calculator.
(function () {
  const kh = (n) => String(n ?? '').replace(/\d/g, (d) => '០១២៣៤៥៦៧៨៩'[d]);
  let root, stage, slideEl, ink, ctx, i = 0, slides = [], students = [];
  let inkR = null;       // the ink canvas's box while a stroke is being drawn (reading it on every pen event would force a layout each time)
  let tool = 'none', color = '#e03131', size = 4, drawing = false, cur = null, spot = null, stamp = '✔';
  let clockT = 0, geoColor = '#212529', geoSize = 2, colorSetter = null, offTools = null, meta = { grade: '', lesson: '' }, lensPin = false, toolSetter = null, lensIco = null, lens = null, lensIn = null, lensClone = null, lensRaf = 0, lensGo = { x: 0, y: 0, z: 1 }, lensNow = { x: 0, y: 0, z: 1 }, lensOn = false, lensZoom = 2.2;
  let sizeSetter = null, toastEl = null, toastT = 0;
  let laser = [], laserRaf = 0, penKind = 'ball', hand = null;
  let strokes = [], undoS = [], redoS = [], palette = null;
  let baseCv = null, baseList = [], lastPenAt = -1e9, eraseR = 14, hoverP = null, penErase = false, downType = '';   // pen: committed-ink cache, palm rejection, eraser size and ring
  let stepNow = 0, stepLevels = [];   // step-by-step reveal: how many steps are showing, and the distinct data-step values on this slide
  let floats = [];


  // ---- live widgets -----------------------------------------------------------------------------
  // A <div data-widget="name"> inside a slide is handed to widgets[name](el) once the slide is on screen; what it returns is
  // called when the slide is left, so animations stop. (Slides are plain HTML, so anything that moves has to live here.)
  let widgetStops = [];
  const widgets = {};
  function stopWidgets() { widgetStops.forEach((f) => { try { f(); } catch (e) { /* ignore */ } }); widgetStops = []; }
  function startWidgets() {
    stopWidgets();
    if (!slideEl) return;
    slideEl.querySelectorAll('[data-widget]').forEach((el) => {
      const make = widgets[el.dataset.widget];
      if (make) { const stop = make(el); if (stop) widgetStops.push(stop); }
    });
  }

  // Marbles in a plate (Lesson 1, 5.2: "more than 80, fewer than 90, equal to 7 times the sum of its digits").
  // The teacher picks a number of marbles, they pop into the plate, and ▶ makes them roll around inside it.
  widgets.marbles = function (el) {
    const R = 150, r = 12, SIZE = 2 * R + 20, C = SIZE / 2;
    const COLORS = ['#e03131', '#1c7ed6', '#2f9e44', '#f08c00', '#ae3ec9', '#0ca678'];
    let n = 81, balls = [], playing = false, raf = 0, alive = true;
    el.innerHTML = '';
    const mk = (tag, cls, txt) => { const e = document.createElement(tag); if (cls) e.className = cls; if (txt != null) e.textContent = txt; return e; };
    const chips = mk('div', 'mb-chips'), body = mk('div', 'mb-body'), cv = mk('canvas', 'mb-cv'), side = mk('div', 'mb-side');
    const info = mk('div', 'mb-info'), ctl = mk('div', 'mb-ctl');
    const playB = mk('button', 'mb-btn go', '▶ លេង'), resetB = mk('button', 'mb-btn', '↺ ចាក់ម្តងទៀត');
    playB.type = resetB.type = 'button';
    ctl.append(playB, resetB); side.append(info, ctl); body.append(cv, side); el.append(chips, body);
    const dpr = Math.min(2, window.devicePixelRatio || 1);
    cv.width = cv.height = Math.round(SIZE * dpr);
    const ctx = cv.getContext('2d');
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    function spawn(count) {           // hex-packed start so nothing overlaps, then a random choice of spots
      const d = 2 * r + 2, pts = [];
      for (let j = -8; j <= 8; j++) for (let i = -8; i <= 8; i++) {
        const x = i * d + (j % 2 ? d / 2 : 0), y = j * d * 0.866;
        if (Math.hypot(x, y) <= R - r - 2) pts.push([x, y]);
      }
      for (let k = pts.length - 1; k > 0; k--) { const q = Math.floor(Math.random() * (k + 1)); [pts[k], pts[q]] = [pts[q], pts[k]]; }
      const t0 = performance.now();
      balls = pts.slice(0, count).map((p, k) => ({ x: C + p[0], y: C + p[1], vx: 0, vy: 0, c: COLORS[Math.floor(Math.random() * COLORS.length)], t: t0 + k * 14, s: 0 }));
    }
    function step() {
      // no gravity: like a lottery drum, every marble keeps bouncing at about the same lively speed, so they spread over the whole plate
      for (let sub = 0; sub < 2; sub++) {
        for (const b of balls) {
          const sp = Math.hypot(b.vx, b.vy) || 0.01;
          const k = 1 + 0.04 * (2.4 / sp - 1);                       // gently pull the speed towards 2.4
          b.vx = b.vx * k + (Math.random() - 0.5) * 0.1; b.vy = b.vy * k + (Math.random() - 0.5) * 0.1;
          b.x += b.vx; b.y += b.vy;
          const dx = b.x - C, dy = b.y - C, dist = Math.hypot(dx, dy);
          if (dist > R - r) {                                       // bounce off the rim
            const nx = dx / dist, ny = dy / dist, dot = b.vx * nx + b.vy * ny;
            b.x = C + nx * (R - r); b.y = C + ny * (R - r);
            if (dot > 0) {                                          // leave the rim at a random inward angle, so they cross and mix
              const a = Math.atan2(-ny, -nx) + (Math.random() - 0.5) * 2.2, v = 1.8 + Math.random() * 1.4;
              b.vx = Math.cos(a) * v; b.vy = Math.sin(a) * v;
            }
          }
        }
        for (let i = 0; i < balls.length; i++) for (let j = i + 1; j < balls.length; j++) {
          const a = balls[i], b = balls[j], dx = b.x - a.x, dy = b.y - a.y, d2 = dx * dx + dy * dy;
          if (d2 > 0 && d2 < 4 * r * r) {
            const d = Math.sqrt(d2), nx = dx / d, ny = dy / d, push = (2 * r - d) / 2;
            a.x -= nx * push; a.y -= ny * push; b.x += nx * push; b.y += ny * push;
            const rv = (b.vx - a.vx) * nx + (b.vy - a.vy) * ny;
            if (rv < 0) { const j2 = -1.0 * rv / 2; a.vx -= j2 * nx; a.vy -= j2 * ny; b.vx += j2 * nx; b.vy += j2 * ny; }
          }
        }
      }
    }
    function draw() {
      ctx.clearRect(0, 0, SIZE, SIZE);
      const g = ctx.createRadialGradient(C, C - 30, 20, C, C, R + 6);
      g.addColorStop(0, '#f4f8fb'); g.addColorStop(1, '#cfdde8');
      ctx.beginPath(); ctx.arc(C, C, R + 6, 0, 6.2832); ctx.fillStyle = g; ctx.fill();
      ctx.lineWidth = 7; ctx.strokeStyle = '#1f4a5f'; ctx.stroke();
      const now = performance.now();
      for (const b of balls) {
        const k = Math.max(0, Math.min(1, (now - b.t) / 260)); b.s = k;
        if (!k) continue;
        const ease = k < 1 ? 1 - Math.pow(1 - k, 3) : 1;                          // pop in: grow with a little overshoot
        const rr = r * ease * (k < 1 ? 1 + 0.25 * Math.sin(k * Math.PI) : 1);
        const gr = ctx.createRadialGradient(b.x - rr * 0.35, b.y - rr * 0.35, rr * 0.1, b.x, b.y, rr);
        gr.addColorStop(0, '#fff'); gr.addColorStop(0.25, b.c); gr.addColorStop(1, '#00000055');
        ctx.beginPath(); ctx.arc(b.x, b.y, Math.max(0.1, rr), 0, 6.2832); ctx.fillStyle = gr; ctx.fill();
      }
    }
    function say() {
      const t = Math.floor(n / 10), u = n % 10, sum = t + u, ok = 7 * sum === n;
      info.innerHTML = `<div>កូនឃ្លី <b>${n}</b> គ្រាប់</div><div>ផលបូកតួលេខ <b>${t} + ${u} = ${sum}</b></div><div>7 × ${sum} = <b>${7 * sum}</b></div>`
        + `<div class="mb-v ${ok ? 'ok' : 'no'}">${ok ? '✓ ស្មើនឹង ' + n + ' — ត្រូវហើយ!' : '✗ ' + 7 * sum + ' មិនស្មើ ' + n}</div>`;
      chips.querySelectorAll('button').forEach((b) => b.classList.toggle('on', Number(b.dataset.n) === n));
    }
    function pick(v) { n = v; spawn(n); say(); draw(); }
    for (let v = 81; v <= 89; v++) { const b = mk('button', 'mb-chip', String(v)); b.type = 'button'; b.dataset.n = String(v); b.onclick = () => pick(v); chips.append(b); }
    playB.onclick = () => { playing = !playing; playB.textContent = playing ? '⏸ ឈប់' : '▶ លេង'; playB.classList.toggle('on', playing); if (playing) balls.forEach((b) => { const a = Math.random() * 6.2832; b.vx = Math.cos(a) * 2.4; b.vy = Math.sin(a) * 2.4; }); };
    resetB.onclick = () => pick(n);
    function loop() {
      if (!alive) return;
      const animating = balls.some((b) => b.s < 1);
      if (playing) step();
      if (playing || animating) draw();
      raf = requestAnimationFrame(loop);
    }
    pick(n);
    raf = requestAnimationFrame(loop);
    return () => { alive = false; cancelAnimationFrame(raf); };
  };

  // The calculator (Tools → Calculator) opens by itself on slides that carry <div data-widget="calc">, so the teacher can show the
  // key presses live; it is put away again when the slide is left, unless the teacher had opened it before.
  widgets.calc = function () {
    const f = root && root.querySelector('.ts-float.ts-wcalc');
    if (!f) return null;
    const menuItem = root.querySelector('.ts-tmenu button[data-w="wcalc"]');
    const wasHidden = f.hidden;
    if (!f.dataset.placed) { f.style.left = '64%'; f.style.top = '3%'; f.style.width = '270px'; f.dataset.placed = '1'; }   // right side, clear of the slide text and the page pill
    f.hidden = false; stage.append(f);
    if (menuItem) menuItem.classList.add('on');
    return () => { if (wasHidden) { f.hidden = true; if (menuItem) menuItem.classList.remove('on'); } };
  };

  function math(el) {
    if (window.renderMathInElement) {
      try { renderMathInElement(el, { throwOnError: false, strict: false, macros: { '\\arc': '\\overset{\\frown}{#1}' }, delimiters: [{ left: '\\(', right: '\\)', display: false }, { left: '\\[', right: '\\]', display: true }] }); } catch {}
    }
  }

  // definition / general / note / theorem slides: the heading becomes a gold title with a fading line on a dark rounded card
  function cardify(html) {
    const box = document.createElement('div'); box.innerHTML = html;
    const h2 = box.querySelector(':scope > h2'); if (!h2) return html;
    const kick = box.querySelector(':scope > .ts-kicker');
    const card = document.createElement('div'); card.className = 'ts-card';
    const head = document.createElement('div'); head.className = 'ts-card-h'; head.innerHTML = `<span>${h2.innerHTML}</span><i></i>`;
    const body = document.createElement('div'); body.className = 'ts-card-b';
    [...box.childNodes].forEach((n) => { if (n !== kick && n !== h2) body.append(n); });
    // the new word being defined ("ហៅថា ___") gets a special highlight
    body.innerHTML = body.innerHTML.replace(/(ហៅថា\s*)([^\s។,;<\\&]+)/g, '$1<mark class="term">$2</mark>');
    card.append(head, body); box.innerHTML = ''; if (kick) box.append(kick); box.append(card);
    return box.innerHTML;
  }

  function show(n, depth, atEnd) {
    if (!depth) { if (slides[i] && slideEl && slideEl.innerHTML) slides[i]._ink = strokes; lensOff(); lensClone = null; } // remember what was written on the slide we leave
    i = Math.max(0, Math.min(slides.length - 1, n));
    const s = slides[i] || { html: '' };
    slideEl.className = 'ts-slide' + (s.k ? ` ts-${s.k}` : '') + (s.c ? ` ts-${s.c}` : '') + (BIG_TEXT ? ' ts-big' : '');
    slideEl.innerHTML = s.k === 'key' ? cardify(s.html || '') : (s.html || '');
    math(slideEl);
    fillMeta();
    const fits = fitText(0.72);
    if (!fits && (depth || 0) < 4 && splitSlide(i)) return show(i, (depth || 0) + 1, atEnd);
    if (!fits) fitText(0.4);
    s._fs = slideEl.style.fontSize;
    setupSteps(atEnd);   // after fitting, so the layout is measured with everything showing and nothing jumps when a step appears
    startWidgets();
    pageLabel();
    strokes = s._ink || []; undoS = []; redoS = []; cur = null;
    redraw(); syncUndo();
  }

  // ---- step-by-step reveal ------------------------------------------------------------------
  // Mark anything in a slide with data-step="n": it stays hidden until the n-th press of → (or the next click).
  // data-until="n" does the opposite: the element is hidden again from step n on (a borrowed ten that is broken up).
  // Hidden elements keep their space, so the slide never reflows while the teacher reveals it.
  function setupSteps(atEnd) {
    const vals = [...slideEl.querySelectorAll('[data-step],[data-until]')].flatMap((el) => [el.dataset.step, el.dataset.until]).filter((v) => v != null && v !== '').map(Number);
    stepLevels = [...new Set(vals)].sort((a, b) => a - b).filter((v) => v > 0);
    stepNow = atEnd ? stepLevels.length : 0;
    applySteps();
  }
  function applySteps() {
    const cur = stepNow ? stepLevels[stepNow - 1] : 0;   // the data-step value that is showing now
    slideEl.querySelectorAll('[data-step],[data-until]').forEach((el) => {
      const a = el.dataset.step != null ? Number(el.dataset.step) : 0;
      const u = el.dataset.until != null ? Number(el.dataset.until) : Infinity;
      el.classList.toggle('rv-hide', a > cur || u <= cur);
      el.classList.toggle('rv-now', a > 0 && a === cur && stepNow > 0);   // what was just revealed gets a soft highlight
    });
    // data-now="n": marks the part (e.g. a whole column of a sum) that step n is about, so it is tinted only while that step shows
    slideEl.querySelectorAll('[data-now]').forEach((el) => el.classList.toggle('rv-on', stepNow > 0 && Number(el.dataset.now) === cur));
  }
  function pageLabel() {
    const lab = root && root.querySelector('.ts-page');
    if (!lab) return;
    lab.textContent = `${kh(i + 1)} / ${kh(slides.length)}` + (stepLevels.length ? ` · ${kh(stepNow)}/${kh(stepLevels.length)}` : '');
  }
  // → / next click: reveal the next step first, then move on; ← takes a step back, then lands on the finished previous slide
  function nextStep() {
    if (stepNow < stepLevels.length) { stepNow++; applySteps(); pageLabel(); } else show(i + 1);
  }
  function prevStep() {
    if (stepNow > 0) { stepNow--; applySteps(); pageLabel(); } else show(i - 1, 0, true);
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
    delete a.c; delete b.c; delete a._ink; delete b._ink;
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
    const r = inkR || ink.getBoundingClientRect();
    const q = { x: e.clientX - r.left, y: e.clientY - r.top, t: performance.now() };
    if (e.pointerType === 'pen' && e.pressure > 0) q.pr = e.pressure;          // a pen reports how hard it is pressed; mouse and touch do not
    return q;
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
    } else if (st.t === 'point') {
      ctx.beginPath(); ctx.arc(st.p[0].x, st.p[0].y, Math.max(4.5, st.w * 1.3), 0, Math.PI * 2); ctx.fill();
    } else if (st.t === 'pen' && st.k && st.k !== 'ball') {
      paintPen(st);
    } else if (st.t === 'pen' && st.p.some((q) => q.pr != null)) {
      pressureStroke(st);
    } else if (st.t === 'pen' || st.t === 'hi') {
      ctx.beginPath(); curve(st.p); ctx.stroke();
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
    if (st.label) { // measurement text (length in cm, angle in degrees, point name)
      ctx.font = '700 19px "Kantumruy Pro", sans-serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.globalAlpha = 1;
      const m = ctx.measureText(st.label.text);
      ctx.fillStyle = 'rgba(255,255,255,.94)'; ctx.fillRect(st.label.x - m.width / 2 - 7, st.label.y - 14, m.width + 14, 28);
      ctx.strokeStyle = st.c; ctx.lineWidth = 1.5; ctx.strokeRect(st.label.x - m.width / 2 - 7, st.label.y - 14, m.width + 14, 28);
      ctx.fillStyle = st.c; ctx.fillText(st.label.text, st.label.x, st.label.y);
    }
    ctx.restore();
  }

  // a stroke as a smooth curve through the middle of each pair of points (not a jagged polyline)
  function curve(pts) {
    if (pts.length < 3) { pts.forEach((q, k) => (k ? ctx.lineTo(q.x, q.y) : ctx.moveTo(q.x, q.y))); if (pts.length === 1) ctx.lineTo(pts[0].x + .1, pts[0].y); return; }
    ctx.moveTo(pts[0].x, pts[0].y);
    for (let k = 1; k < pts.length - 1; k++) ctx.quadraticCurveTo(pts[k].x, pts[k].y, (pts[k].x + pts[k + 1].x) / 2, (pts[k].y + pts[k + 1].y) / 2);
    const l = pts[pts.length - 1]; ctx.lineTo(l.x, l.y);
  }
  // pen with pressure: the line gets thicker the harder the pen is pressed, eased so it does not jump
  function pressureStroke(st) {
    const pts = st.p, wOf = (q) => st.w * (0.35 + 1.3 * (q.pr == null ? 0.5 : q.pr));
    if (pts.length === 1) { ctx.beginPath(); ctx.arc(pts[0].x, pts[0].y, wOf(pts[0]) / 2, 0, Math.PI * 2); ctx.fill(); return; }
    let pw = wOf(pts[0]);
    for (let k = 1; k < pts.length; k++) {
      const a = k === 1 ? pts[0] : { x: (pts[k - 1].x + pts[k].x) / 2, y: (pts[k - 1].y + pts[k].y) / 2 };
      const b = k === pts.length - 1 ? pts[k] : { x: (pts[k].x + pts[k + 1].x) / 2, y: (pts[k].y + pts[k + 1].y) / 2 };
      pw += (wOf(pts[k]) - pw) * .4; ctx.lineWidth = pw;
      ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.quadraticCurveTo(pts[k].x, pts[k].y, b.x, b.y); ctx.stroke();
    }
    st._pw = pw;
  }

  // live pen stroke: only the points that arrived since the last frame are painted (same curve and widths as the final repaint, so nothing changes when the pen lifts)
  function plainPen(st) { return st.t === 'pen' && (!st.k || st.k === 'ball'); }
  function liveSegments(st) {
    const pts = st.p, n = pts.length, wOf = (q) => st.w * (0.35 + 1.3 * (q.pr == null ? 0.5 : q.pr)), press = pts.some((q) => q.pr != null);
    ctx.save(); ctx.lineCap = 'round'; ctx.lineJoin = 'round'; ctx.strokeStyle = st.c; ctx.fillStyle = st.c;
    if (n === 1) { ctx.beginPath(); ctx.arc(pts[0].x, pts[0].y, (press ? wOf(pts[0]) : st.w) / 2, 0, Math.PI * 2); ctx.fill(); ctx.restore(); return; }
    if (st._k == null) { st._k = 1; st._pw = press ? wOf(pts[0]) : st.w; }
    const mid = (a, b) => ({ x: (a.x + b.x) / 2, y: (a.y + b.y) / 2 });
    for (let k = st._k; k < n - 1; k++) {                                   // segments whose end is already known
      const a = k === 1 ? pts[0] : mid(pts[k - 1], pts[k]), b = mid(pts[k], pts[k + 1]);
      if (press) st._pw += (wOf(pts[k]) - st._pw) * .4;
      ctx.lineWidth = press ? st._pw : st.w; ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.quadraticCurveTo(pts[k].x, pts[k].y, b.x, b.y); ctx.stroke();
      st._k = k + 1;
    }
    const a = n >= 3 ? mid(pts[n - 2], pts[n - 1]) : pts[0], l = pts[n - 1];   // the head: a short straight lead-in so the line reaches the pen tip; the final repaint replaces it
    ctx.lineWidth = press ? st._pw + (wOf(l) - st._pw) * .4 : st.w; ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(l.x, l.y); ctx.stroke();
    ctx.restore();
  }

  const rnd = (n) => { const x = Math.sin(n * 12.9898) * 43758.5453; return x - Math.floor(x); };
  // pen types: marker (broad, soft), brush (width follows speed), pencil (grainy), chalk (dusty)
  function paintPen(st) {
    const pts = st.p, w = st.w, k = st.k;
    const path = () => { ctx.beginPath(); curve(pts); };
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
    // finished strokes are painted once into a cache and reused while the pen moves; only the stroke being drawn is repainted
    const same = baseCv && baseCv.width === ink.width && baseCv.height === ink.height && baseList.length === strokes.length && baseList.every((x, k) => x === strokes[k]);
    if (!same) {
      baseCv = baseCv || document.createElement('canvas'); baseCv.width = ink.width; baseCv.height = ink.height;
      const real = ctx, dpr = ink.width / Math.max(1, r.width);
      ctx = baseCv.getContext('2d'); ctx.setTransform(dpr, 0, 0, dpr, 0, 0); ctx.clearRect(0, 0, r.width, r.height);
      strokes.forEach(paint); ctx = real; baseList = strokes.slice();
    }
    ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.clearRect(0, 0, ink.width, ink.height); ctx.drawImage(baseCv, 0, 0); ctx.restore();
    if (cur) { paint(cur); if (plainPen(cur)) { cur._k = Math.max(1, cur.p.length - 1); } }
    if ((tool === 'erase' || penErase) && hoverP) {                                // the eraser's size, so the teacher sees what will be rubbed out
      ctx.save(); ctx.strokeStyle = 'rgba(30,41,59,.85)'; ctx.lineWidth = 1.5; ctx.setLineDash([4, 3]);
      ctx.beginPath(); ctx.arc(hoverP.x, hoverP.y, eraseR, 0, Math.PI * 2); ctx.stroke(); ctx.restore();
    }
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

  function near(st, p, rad) {
    const R = rad || 14;
    const pts = st.t === 'pen' || st.t === 'hi' || st.t === 'stamp' || st.t === 'point' ? st.p : [st.p[0], st.p[st.p.length - 1]];
    if (st.t === 'stamp') return Math.hypot(pts[0].x - p.x, pts[0].y - p.y) < R + 20;
    if (st.t === 'point') return Math.hypot(pts[0].x - p.x, pts[0].y - p.y) < R + 8;
    if (pts.length === 1) return Math.hypot(pts[0].x - p.x, pts[0].y - p.y) < R;
    const xs = pts.map((q) => q.x), ys = pts.map((q) => q.y);
    if (st.t === 'pen' || st.t === 'hi') return pts.some((q, k) => k && distSeg(p, pts[k - 1], q) < R);
    if (st.t === 'line' || st.t === 'arrow') return distSeg(p, pts[0], pts[1]) < R;
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
  function say(msg) {
    if (!toastEl) { toastEl = document.createElement('div'); toastEl.className = 'ts-toast'; stage.append(toastEl); }
    toastEl.textContent = msg; toastEl.classList.add('on'); clearTimeout(toastT);
    toastT = setTimeout(() => toastEl && toastEl.classList.remove('on'), 2200);
  }

  // html2canvas drops list markers, so write them into the text before taking the picture
  function bakeMarkers(root) {
    root.querySelectorAll('ol, ul').forEach((l) => {
      let n = 0;
      [...l.children].forEach((li) => {
        if (li.tagName !== 'LI' || li.classList.contains('lab')) return;
        n += 1;
        const m = document.createElement('span');
        m.textContent = l.tagName === 'OL' ? `${n}.\u00a0` : '•\u00a0';
        m.style.cssText = 'display:inline-block;min-width:1.4em;margin-left:-1.4em;text-align:right;padding-right:.25em';
        li.insertBefore(m, li.firstChild);
        li.style.listStyle = 'none';
      });
      l.style.listStyle = 'none';
    });
  }

  // where the writing and the text really are on a slide (so the export can drop the empty space and enlarge the text)
  function contentBox(el, st, w, h) {
    const o = el.getBoundingClientRect();
    let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
    const add = (l, t, r, b) => { x0 = Math.min(x0, l); y0 = Math.min(y0, t); x1 = Math.max(x1, r); y1 = Math.max(y1, b); };
    const tw = document.createTreeWalker(el, NodeFilter.SHOW_TEXT), rg = document.createRange();
    while (tw.nextNode()) {
      const n = tw.currentNode;
      if (!n.textContent.trim() || n.parentElement.closest('.katex-mathml')) continue;
      rg.selectNodeContents(n);
      [...rg.getClientRects()].forEach((r) => { if (r.width > 0 && r.height > 0) add(r.left - o.left, r.top - o.top, r.right - o.left, r.bottom - o.top); });
    }
    el.querySelectorAll('img,svg,table,canvas,.ts-axis').forEach((e) => {
      const r = e.getBoundingClientRect(); if (r.width > 0) add(r.left - o.left, r.top - o.top, r.right - o.left, r.bottom - o.top);
    });
    (st || []).forEach((q) => q.p.forEach((pt) => { const m = (q.t === 'stamp' ? 30 : q.w * (q.t === 'hi' ? 3 : 1.6)) + 6; add(pt.x - m, pt.y - m, pt.x + m, pt.y + m); }));
    if (x1 < x0) return { x: 0, y: 0, w, h };
    const pad = 36;
    const x = Math.max(0, x0 - pad), y = Math.max(0, y0 - pad);
    return { x, y, w: Math.min(w, x1 + pad) - x, h: Math.min(h, y1 + pad) - y };
  }

  // exports are 16:9 (1920x1080): the slide content is cropped to what is on it, enlarged, and centred with margins left and right
  function widen(src, w, h, box, bg) {
    const W = 1920, H = 1080, MX = 210, MY = 50;
    const out = document.createElement('canvas'); out.width = W; out.height = H;
    const c = out.getContext('2d');
    c.fillStyle = bg && !/rgba\(0, 0, 0, 0\)|transparent/.test(bg) ? bg : '#ffffff'; c.fillRect(0, 0, W, H);
    const b = box || { x: 0, y: 0, w, h };
    const k = Math.min((W - 2 * MX) / b.w, (H - 2 * MY) / b.h, 2.2);
    const dw = b.w * k, dh = b.h * k, r = src.width / w;
    c.imageSmoothingQuality = 'high';
    c.drawImage(src, b.x * r, b.y * r, b.w * r, b.h * r, (W - dw) / 2, (H - dh) / 2, dw, dh);
    return out;
  }

  // html2canvas drops list markers, so write them into the text before taking the picture
  function bakeMarkers(root) {
    root.querySelectorAll('ol, ul').forEach((l) => {
      let n = 0;
      [...l.children].forEach((li) => {
        if (li.tagName !== 'LI' || li.classList.contains('lab')) return;
        n += 1;
        const m = document.createElement('span');
        m.textContent = l.tagName === 'OL' ? `${n}.\u00a0` : '•\u00a0';
        m.style.cssText = 'display:inline-block;min-width:1.4em;margin-left:-1.4em;text-align:right;padding-right:.25em';
        li.insertBefore(m, li.firstChild);
        li.style.listStyle = 'none';
      });
      l.style.listStyle = 'none';
    });
  }

  // exports are 16:9 (1920x1080): the slide is centred with white margins on the left and right
  function widen(src, w, h) {
    const W = 1920, H = 1080, MX = 120, MY = 36;
    const out = document.createElement('canvas'); out.width = W; out.height = H;
    const c = out.getContext('2d');
    c.fillStyle = '#ffffff'; c.fillRect(0, 0, W, H);
    const k = Math.min((W - 2 * MX) / w, (H - 2 * MY) / h);
    const dw = w * k, dh = h * k;
    c.imageSmoothingQuality = 'high';
    c.drawImage(src, (W - dw) / 2, (H - dh) / 2, dw, dh);
    c.font = '700 30px "Times New Roman", serif'; c.fillStyle = 'rgba(15,81,115,.8)'; c.textBaseline = 'alphabetic';
    c.fillText('khmermath.org', 40, H - 28);                      // the same site label on every exported picture / PDF / PowerPoint page
    return out;
  }

  // save the current slide, with everything written on it, as a PNG the teacher can hand out
  let saving = false;
  async function saveImage() {
    if (saving) return;
    saving = true; say('កំពុងរៀបចំរូបភាព…');
    try {
      if (!window.html2canvas) {
        await new Promise((ok, no) => { const sc = document.createElement('script'); sc.src = '/js/html2canvas.min.js'; sc.onload = ok; sc.onerror = no; document.head.append(sc); });
      }
      const w = slideEl.clientWidth, h = slideEl.clientHeight;
      const holder = document.createElement('div');
      holder.style.cssText = `position:fixed;left:0;top:0;width:${w}px;height:${h}px;z-index:-1;pointer-events:none;background:#fff`;
      const copy = slideEl.cloneNode(true);
      copy.style.position = 'relative'; copy.style.inset = 'auto'; copy.style.width = w + 'px'; copy.style.height = h + 'px'; copy.style.overflow = 'hidden';
      holder.append(copy); document.body.append(holder);
      bakeMarkers(copy);
      const box = contentBox(copy, strokes, w, h), bg = getComputedStyle(copy).backgroundColor;
      const scale = 2;
      let base;
      try { base = await window.html2canvas(holder, { backgroundColor: '#ffffff', scale, useCORS: true, logging: false }); }
      finally { holder.remove(); }
      const out = document.createElement('canvas');
      out.width = base.width; out.height = base.height;
      const c2 = out.getContext('2d');
      c2.drawImage(base, 0, 0);
      c2.drawImage(ink, 0, 0, ink.width, ink.height, 0, 0, out.width, out.height); // pen strokes on top
      const wide = widen(out, w, h, box, bg);
      const name = `grade${meta.grade}-lesson${meta.lesson}-slide${i + 1}.png`;
      const a = document.createElement('a');
      a.download = name; a.href = wide.toDataURL('image/png');
      document.body.append(a); a.click(); a.remove();
      say('✓ បានរក្សាទុករូបភាព ' + name);
    } catch (err) {
      say('រក្សាទុករូបភាពមិនបានសម្រេច');
    } finally { saving = false; }
  }

  // one PDF with every slide that has writing on it
  let pdfBusy = false;
  async function savePdf() {
    if (pdfBusy) return;
    if (slides[i]) slides[i]._ink = strokes;
    const list = slides.filter((x) => x._ink && x._ink.length);
    if (!list.length) { say('មិនទាន់មានស្លាយណាដែលបានសរសេរទេ'); return; }
    pdfBusy = true;
    try {
      const need = (src, ok) => ok() ? Promise.resolve() : new Promise((res, rej) => { const sc = document.createElement('script'); sc.src = src; sc.onload = res; sc.onerror = rej; document.head.append(sc); });
      await need('/js/html2canvas.min.js', () => window.html2canvas);
      await need('/js/jspdf.umd.min.js', () => window.jspdf);
      const w = slideEl.clientWidth, h = slideEl.clientHeight;
      const doc = new window.jspdf.jsPDF({ orientation: 'landscape', unit: 'px', format: [960, 540], compress: true });
      for (let k = 0; k < list.length; k++) {
        say(`កំពុងបង្កើត PDF… ${kh(k + 1)}/${kh(list.length)}`);
        const sl = list[k];
        const holder = document.createElement('div');
        holder.style.cssText = `position:fixed;left:0;top:0;width:${w}px;height:${h}px;z-index:-1;pointer-events:none;background:#fff`;
        const el = document.createElement('div');
        el.className = 'ts-slide' + (sl.k ? ` ts-${sl.k}` : '') + (sl.c ? ` ts-${sl.c}` : '');
        el.style.cssText = `position:relative;width:${w}px;height:${h}px;overflow:hidden;font-size:${sl._fs || ''}`;
        el.innerHTML = sl.k === 'key' ? cardify(sl.html || '') : (sl.html || '');
        holder.append(el); document.body.append(holder);
        math(el);
        bakeMarkers(el);
        const box = contentBox(el, sl._ink, w, h), bg = getComputedStyle(el).backgroundColor;
        let base;
        try { base = await window.html2canvas(holder, { backgroundColor: '#ffffff', scale: 2, useCORS: true, logging: false }); }
        finally { holder.remove(); }
        const out = document.createElement('canvas');
        out.width = base.width; out.height = base.height;
        const c2 = out.getContext('2d');
        c2.drawImage(base, 0, 0);
        const keep = ctx; ctx = c2; c2.save(); c2.scale(out.width / w, out.height / h);
        try { sl._ink.forEach(paint); } finally { c2.restore(); ctx = keep; }
        if (k) doc.addPage([960, 540], 'landscape');
        doc.addImage(widen(out, w, h, box, bg).toDataURL('image/jpeg', .92), 'JPEG', 0, 0, 960, 540);
      }
      const name = `grade${meta.grade}-lesson${meta.lesson}-annotated.pdf`;
      doc.save(name);
      say(`✓ បានរក្សាទុក PDF ${kh(list.length)} ស្លាយ`);
    } catch (err) {
      say('បង្កើត PDF មិនបានសម្រេច');
    } finally { pdfBusy = false; }
  }

  // ---- download slides as PDF or PowerPoint (⬇ in the header): the whole lesson, one part, or just this slide -------------------------
  // Every slide is drawn to a 16:9 picture (the same way as the pen-toolbar PDF), then packed into a PDF (jsPDF) or a .pptx (PptxGenJS).
  // In the .pptx each slide is a picture, so it looks exactly like the screen but the text cannot be edited.
  const loadOnce = (src, ok) => (ok() ? Promise.resolve() : new Promise((res, rej) => { const sc = document.createElement('script'); sc.src = src; sc.onload = res; sc.onerror = () => rej(new Error('load ' + src)); document.head.append(sc); }));

  // what can be downloaded: the lesson, each numbered part (and the exercises) found by their title slides, and the slide on screen
  function exportScopes() {
    const out = [{ id: 'all', file: 'full-lesson', label: 'ទាំងមេរៀន', from: 0, to: slides.length }];
    const heads = [];
    slides.forEach((s, k) => {
      if (s.k !== 'title' || !s.html) return;
      const m = s.html.match(/<h1>\s*(\d+)\.\s*([^<]+?)\s*<\/h1>/);
      if (m) heads.push({ k, file: `part${m[1]}`, label: `ផ្នែកទី ${kh(m[1])} · ${m[2]}` });
      else if (/<h1>\s*លំហាត់\s*<\/h1>/.test(s.html)) heads.push({ k, file: 'exercises', label: 'លំហាត់' });
    });
    let endAt = slides.findIndex((s) => s.k === 'title' && /<h1>\s*ចប់មេរៀន\s*<\/h1>/.test(s.html || ''));
    if (endAt < 0) endAt = slides.length;
    heads.forEach((h, n) => out.push({ id: `p${n}`, file: h.file, label: h.label, from: h.k, to: n + 1 < heads.length ? heads[n + 1].k : endAt }));
    out.push({ id: 'cur', file: `slide${i + 1}`, label: `ស្លាយនេះតែមួយ (ស្លាយទី ${kh(i + 1)})`, from: i, to: i + 1 });
    return out;
  }

  // one slide -> a 1920x1080 canvas, with its steps all showing and (optionally) what the teacher wrote on it
  async function slideCanvas(sl, w, h, withInk) {
    const holder = document.createElement('div');
    holder.style.cssText = `position:fixed;left:0;top:0;width:${w}px;z-index:-1;pointer-events:none;background:#fff`;
    if (themeCls) holder.className = themeCls;                    // the lesson's look (purple) must be on the exported picture too
    const el = document.createElement('div');
    el.className = 'ts-slide' + (sl.k ? ` ts-${sl.k}` : '') + (sl.c ? ` ts-${sl.c}` : '');
    el.style.cssText = `position:relative;inset:auto;width:${w}px;min-height:${h}px;height:auto;overflow:visible;font-size:${sl._fs || ''}`;
    el.innerHTML = sl.k === 'key' ? cardify(sl.html || '') : (sl.html || '');
    holder.append(el); document.body.append(holder);
    math(el); fillMeta(el); bakeMarkers(el);
    const H = Math.max(h, el.scrollHeight);                      // a slide that is longer than the screen is shrunk to fit, not cut
    holder.style.height = H + 'px';
    let base;
    try { base = await window.html2canvas(holder, { backgroundColor: '#ffffff', scale: 2, useCORS: true, logging: false }); }
    finally { holder.remove(); }
    const out = document.createElement('canvas');
    out.width = base.width; out.height = base.height;
    const c2 = out.getContext('2d');
    c2.drawImage(base, 0, 0);
    if (withInk && sl._ink && sl._ink.length) {
      const keep = ctx; ctx = c2; c2.save(); c2.scale(out.width / w, out.height / H);
      try { sl._ink.forEach(paint); } finally { c2.restore(); ctx = keep; }
    }
    return widen(out, w, H);
  }

  function openExport() {
    if (!root || root.querySelector('.ts-exp')) return;
    if (slides[i]) slides[i]._ink = strokes;
    const scopes = exportScopes();
    const mk = (tag, cls, txt) => { const e = document.createElement(tag); if (cls) e.className = cls; if (txt != null) e.textContent = txt; return e; };
    const back = mk('div', 'ts-exp'), card = mk('div', 'ts-exp-card');
    const sel = mk('select', 'ts-exp-sel');
    scopes.forEach((s) => { const o = mk('option', '', s.id === 'all' ? `${s.label}  (${kh(s.to - s.from)} ស្លាយ)` : `${s.label}  (${kh(s.to - s.from)})`); sel.append(o); });
    const fmts = mk('div', 'ts-exp-fmt');
    const radio = (val, label, on) => { const l = mk('label'); const r = mk('input'); r.type = 'radio'; r.name = 'ts-exp-fmt'; r.value = val; r.checked = on; l.append(r, document.createTextNode(' ' + label)); return l; };
    fmts.append(radio('pdf', 'PDF', true), radio('pptx', 'PowerPoint (.pptx)', false));
    const inkL = mk('label', 'ts-exp-ink'); const inkC = mk('input'); inkC.type = 'checkbox'; inkC.checked = true; inkL.append(inkC, document.createTextNode(' រួមទាំងអ្វីដែលបានសរសេរលើស្លាយ'));
    const note = mk('p', 'ts-exp-note', 'ក្នុង PowerPoint ស្លាយនីមួយៗជារូបភាព (មើលដូចលើអេក្រង់ តែមិនអាចកែអក្សរបាន) ។');
    const status = mk('p', 'ts-exp-status', ''), bar = mk('div', 'ts-exp-bar'), fill = mk('i'); bar.append(fill);
    const go = mk('button', 'ts-exp-go', '⬇ ទាញយក'), close2 = mk('button', 'ts-exp-close', 'បិទ');
    go.type = close2.type = 'button';
    const row = mk('div', 'ts-exp-row'); row.append(go, close2);
    card.append(mk('h3', '', 'ទាញយកស្លាយ'), mk('label', 'ts-exp-l', 'ជ្រើសរើសផ្នែក'), sel, mk('label', 'ts-exp-l', 'ទម្រង់ឯកសារ'), fmts, inkL, note, status, bar, row);
    back.append(card); root.append(back);
    let busy = false, cancel = false;
    const shut = () => { cancel = true; back.remove(); };
    close2.onclick = shut;
    back.addEventListener('keydown', (e) => { e.stopPropagation(); if (e.key === 'Escape') shut(); });
    back.addEventListener('pointerdown', (e) => { if (e.target === back && !busy) shut(); });
    go.onclick = async () => {
      if (busy) return;
      busy = true; cancel = false; go.disabled = true; sel.disabled = true; close2.textContent = 'បោះបង់';
      const sc = scopes[sel.selectedIndex], fmt = fmts.querySelector('input:checked').value;
      try {
        status.textContent = 'កំពុងរៀបចំ…';
        const file = await buildExport(sc, fmt, inkC.checked, (k, n) => {
          status.textContent = `កំពុងបង្កើត… ${kh(k + 1)} / ${kh(n)}`; fill.style.width = `${Math.round((k / n) * 100)}%`;
        }, () => cancel);
        if (!file) return;                                       // cancelled
        status.textContent = 'កំពុងរក្សាទុកឯកសារ…';
        downloadFile(file.name, file.blob);
        fill.style.width = '100%';
        status.textContent = `✓ រួចរាល់ ${kh(file.count)} ស្លាយ — ${file.name}`;
        close2.textContent = 'បិទ';
      } catch (err) {
        status.textContent = 'ទាញយកមិនបានសម្រេច — សូមសាកល្បងម្តងទៀត ។';
      } finally { busy = false; go.disabled = false; sel.disabled = false; }
    };
    sel.focus();
  }

  // build the file in memory: { name, blob, count } (null when cancelled). fmt = 'pdf' | 'pptx'
  async function buildExport(sc, fmt, withInk, progress, cancelled) {
    const list = slides.slice(sc.from, sc.to);
    await loadOnce('/js/html2canvas.min.js', () => window.html2canvas);
    if (fmt === 'pdf') await loadOnce('/js/jspdf.umd.min.js', () => window.jspdf); else await loadOnce('/js/pptxgen.bundle.js', () => window.PptxGenJS);
    const w = slideEl.clientWidth, h = slideEl.clientHeight;
    const doc = fmt === 'pdf' ? new window.jspdf.jsPDF({ orientation: 'landscape', unit: 'px', format: [960, 540], compress: true }) : null;
    const pptx = fmt === 'pptx' ? new window.PptxGenJS() : null;
    if (pptx) { pptx.layout = 'LAYOUT_16x9'; pptx.title = `${meta.cname || ''} ${sc.label}`.trim(); }
    for (let k = 0; k < list.length; k++) {
      if (cancelled && cancelled()) return null;
      if (progress) progress(k, list.length);
      const url = (await slideCanvas(list[k], w, h, withInk)).toDataURL('image/jpeg', 0.9);
      if (doc) { if (k) doc.addPage([960, 540], 'landscape'); doc.addImage(url, 'JPEG', 0, 0, 960, 540); }
      else pptx.addSlide().addImage({ data: url, x: 0, y: 0, w: 10, h: 5.625 });
      await new Promise((r) => setTimeout(r, 0));                // let the page breathe between slides
    }
    if (cancelled && cancelled()) return null;
    const name = `grade${meta.grade}-lesson${meta.lesson}-${sc.file}.${fmt}`;
    const blob = doc ? doc.output('blob') : await pptx.write({ outputType: 'blob' });
    return { name, blob, count: list.length };
  }
  function downloadFile(name, blob) {
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob); a.download = name;
    document.body.append(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(a.href), 60000);
  }

  function sizeToast() {
    if (!toastEl) { toastEl = document.createElement('div'); toastEl.className = 'ts-toast'; stage.append(toastEl); }
    toastEl.textContent = `ទំហំក្បាលប៊ិច ${kh(size)}`;
    const d = document.createElement('i'); d.style.width = d.style.height = Math.max(2, size) + 'px'; d.style.background = color === '#ffffff' ? '#ccc' : color;
    toastEl.append(d);
    toastEl.classList.add('on'); clearTimeout(toastT);
    toastT = setTimeout(() => toastEl && toastEl.classList.remove('on'), 1100);
  }

  // rectangular magnifier: the text under the pointer grows smoothly inside a lens that follows the mouse
  let LW = 640, LH = 350;
  const lensSize = () => { const w = stage.clientWidth; LW = Math.round(Math.min(500, Math.max(300, w * .36))); LH = Math.round(LW * .55); };
  function lensBuild() {
    lensSize();
    if (!lens) {
      lens = document.createElement('div'); lens.className = 'ts-lens';
      lensIn = document.createElement('div'); lensIn.className = 'ts-lens-in';
      lens.append(lensIn); stage.append(lens);
      lens.addEventListener('click', () => { // click the pinned lens to release it, then zoom somewhere else
        if (!lensPin) return;
        lensPin = false; lens.classList.remove('pin');
        if (toolSetter) toolSetter('zoom');
      });
      lens.addEventListener('dblclick', lensKill);
      lensIco = document.createElement('img'); lensIco.className = 'ts-lens-ico'; lensIco.src = '/img/magnifier.png'; lensIco.alt = ''; stage.append(lensIco);
    }
    lensIn.innerHTML = '';
    lensClone = slideEl.cloneNode(true);
    lensClone.removeAttribute('id');
    lensIn.style.width = slideEl.clientWidth + 'px'; lensIn.style.height = slideEl.clientHeight + 'px';
    lensIn.append(lensClone);
  }
  function lensMove(e) {
    if (tool !== 'zoom' || lensPin) return;
    if (!lens || !lensClone || lensClone.innerHTML !== slideEl.innerHTML) lensBuild();
    const r = ink.getBoundingClientRect();
    lensGo.x = e.clientX - r.left; lensGo.y = e.clientY - r.top; lensGo.z = lensZoom;
    if (!lensOn) { lensOn = true; lensNow.x = lensGo.x; lensNow.y = lensGo.y; lensNow.z = 1; lens.classList.add('on'); lensIco.classList.add('on'); }
    if (!lensRaf) lensRaf = requestAnimationFrame(lensTick);
  }
  function lensKill() { // remove the zoom completely
    lensOff();
    if (tool === 'zoom' && toolSetter) toolSetter('none');
  }
  function lensOff(keep) {
    if (keep === true && lensPin) return;
    lensPin = false; if (lens) lens.classList.remove('pin');
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
    handAt = { x: e.clientX, y: e.clientY };
    hand.hidden = false;
    if (!handRaf) handRaf = requestAnimationFrame(() => {                              // the on-screen pen cursor moves once per frame, not once per pen event
      handRaf = 0; if (!handAt) return;
      const r = inkR || ink.getBoundingClientRect();
      hand.style.left = (handAt.x - r.left - 8) + 'px'; hand.style.top = (handAt.y - r.top - 88) + 'px';
    });
  }
  let handAt = null, handRaf = 0;

  function bindInk() {
    hand = makeHand();
    ink.addEventListener('wheel', (e) => { if (tool === 'zoom') { e.preventDefault(); lensZoom = Math.max(1.4, Math.min(4.5, lensZoom + (e.deltaY < 0 ? .25 : -.25))); lensGo.z = lensZoom; if (!lensRaf) lensRaf = requestAnimationFrame(lensTick); return; } if (sizeSetter && HAND_TOOLS.includes(tool)) { e.preventDefault(); sizeSetter(size + (e.deltaY < 0 ? 1 : -1), true); } }, { passive: false });
    ink.addEventListener('dblclick', () => { if (tool === 'zoom') lensKill(); });
    ink.addEventListener('pointermove', lensMove);
    ink.addEventListener('pointerenter', lensMove);
    ink.addEventListener('pointerleave', () => lensOff(true));
    ink.addEventListener('pointermove', handMove);
    ink.addEventListener('pointerenter', handMove);
    ink.addEventListener('pointerleave', () => { if (hand) hand.hidden = true; });
    ink.addEventListener('pointerdown', () => { if (hand) hand.classList.add('writing'); });
    window.addEventListener('pointerup', () => { inkR = null; if (hand) hand.classList.remove('writing'); });
    window.addEventListener('pointercancel', () => { inkR = null; });
    ink.addEventListener('contextmenu', (e) => e.preventDefault());              // the pen's side button must not open a menu
    ink.addEventListener('pointermove', (e) => {
      if (e.pointerType === 'pen') lastPenAt = performance.now();
      if (tool === 'erase' || penErase) { hoverP = pos(e); redraw(); }
    });
    ink.addEventListener('pointerleave', () => { if (hoverP) { hoverP = null; redraw(); } });
    const down = (e) => {
      if (e.pointerType === 'pen') lastPenAt = performance.now();
      if (e.pointerType === 'touch' && performance.now() - lastPenAt < 2500) { e.preventDefault(); return; }   // a resting palm is not writing
      const eraserEnd = e.pointerType === 'pen' && (e.button === 5 || (e.buttons & 34) !== 0);                 // eraser end (32) or side button (2)
      if (e.button && e.button !== 0 && !eraserEnd) return;
      downType = e.pointerType;
      inkR = ink.getBoundingClientRect();
      const p = pos(e);
      closeMenus();
      if (eraserEnd) { penErase = true; drawing = true; eraseAt(p); ink.setPointerCapture && ink.setPointerCapture(e.pointerId); e.preventDefault(); return; }
      if (tool === 'zoom') {
        if (lensOn || lensPin) { lensPin = !lensPin; lens.classList.toggle('pin', lensPin); if (!lensPin) lensMove(e); }
        return;
      }
      if (tool === 'laser') { laser.push({ ...p, t: performance.now() }); if (!laserRaf) laserRaf = requestAnimationFrame(laserTick); }
      else if (tool === 'spot') { spot = p; drawing = true; redraw(); }
      else if (tool === 'stamp') {
        const st = { t: 'stamp', c: color, w: size, ch: stamp, p: [p] };
        strokes.push(st); undoS.push({ add: st }); redoS = []; redraw(); syncUndo();
      } else if (tool === 'point') { // a labelled point: A, B, C ...
        const n = strokes.filter((q) => q.t === 'point').length, letter = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[n % 26] + (n >= 26 ? String(Math.floor(n / 26)) : '');
        const st = { t: 'point', c: geoColor, w: Math.max(2, geoSize), p: [p], label: { text: letter, x: p.x + 20, y: p.y - 20 } };
        strokes.push(st); undoS.push({ add: st }); redoS = []; redraw(); syncUndo();
      } else if (tool === 'gpen') { drawing = true; cur = { t: 'pen', c: geoColor, w: geoSize, k: 'ball', p: [p] };
      } else if (tool === 'erase') { drawing = true; eraseAt(p); }
      else { drawing = true; cur = { t: tool, c: color, w: size, k: penKind, p: [p] }; }
      ink.setPointerCapture && ink.setPointerCapture(e.pointerId);
      e.preventDefault();
    };
    // tablet jitter and pressure noise are filtered as the points arrive: slow movement is smoothed more, fast movement follows the pen closely
    function ingest(q) {
      const l = cur.p[cur.p.length - 1];
      if (!l) { cur.p.push(q); return; }
      const d = Math.hypot(q.x - l.x, q.y - l.y);
      if (d <= 0.6) return;
      const a = Math.min(1, 0.45 + d * 0.07);
      const s = { x: l.x + (q.x - l.x) * a, y: l.y + (q.y - l.y) * a, t: q.t };
      if (q.pr != null) s.pr = l.pr == null ? q.pr : l.pr + (q.pr - l.pr) * 0.3;
      cur.p.push(s);
    }
    let frameQ = 0;
    function framePaint() {                                                        // one paint per screen frame, however many pen events arrived
      if (frameQ) return;
      frameQ = requestAnimationFrame(() => { frameQ = 0; if (!cur) return; if (plainPen(cur)) liveSegments(cur); else redraw(); });
    }
    const move = (e) => {
      if (tool === 'laser') {
        laser.push({ ...pos(e), t: performance.now() });
        if (laser.length > 40) laser.shift();
        if (!laserRaf) laserRaf = requestAnimationFrame(laserTick);
        return;
      }
      if (tool === 'spot' && !drawing) return;
      if (!drawing) return;
      if (downType && e.pointerType !== downType) return;                          // another finger/pen touching must not bend this stroke
      const p = pos(e);
      if (tool === 'spot') { spot = p; redraw(); }
      else if (tool === 'erase' || penErase) { eraseAt(p); hoverP = p; }
      else if (cur) {
        if (cur.t === 'pen' || cur.t === 'hi') {
          // a pen reports many points between two frames: keep them all, so fast strokes stay smooth
          const evs = (e.getCoalescedEvents && e.getCoalescedEvents()) || [];
          (evs.length ? evs : [e]).forEach((ev) => ingest(pos(ev)));
          framePaint();
        } else { cur.p = [cur.p[0], p]; redraw(); }
      }
      e.preventDefault();
    };
    const up = (e) => {
      if (!drawing) return;
      if (e && downType && e.pointerType && e.pointerType !== downType) return;
      inkR = null; drawing = false; downType = ''; if (penErase) { penErase = false; redraw(); return; }
      if (cur && (cur.t === 'pen' || cur.t === 'hi') && e && e.clientX != null) {
        const q = pos(e), l = cur.p[cur.p.length - 1];
        if (l && Math.hypot(q.x - l.x, q.y - l.y) > 0.3) { q.pr = l.pr; cur.p.push(q); }
      }
      if (frameQ) { cancelAnimationFrame(frameQ); frameQ = 0; }
      if (cur) { delete cur._k; delete cur._pw; strokes.push(cur); undoS.push({ add: cur }); redoS = []; cur = null; redraw(); syncUndo(); }
    };
    function eraseAt(p) {
      const hit = strokes.filter((st) => near(st, p, eraseR));
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
    if (opt.autoh) el.dataset.autoh = '1'; // height follows the content (e.g. the calculator zooms with its width)
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
    const rl = document.createElement('div');
    rl.className = 'ts-rs ts-rl'; rl.title = 'ប្ដូរទំហំ';
    el.append(bar, inner, rs, rl);
    stage.append(el);
    drag(el, bar, opt.inside);
    resize(el, rs);
    resizeLeft(el, rl);
    floats.push(el);
    return el;
  }

  function drag(el, bar, inside) {   // inside: keep the whole window on the slide (the calculator has no title bar to grab if it hangs off the edge)
    let ox = 0, oy = 0, dragging = false;
    bar.addEventListener('pointerdown', (e) => {
      if (e.target.closest('button,input,select,.ts-rs')) return;
      dragging = true;
      const r = el.getBoundingClientRect(), s = stage.getBoundingClientRect();
      ox = e.clientX - r.left; oy = e.clientY - r.top;
      bar.setPointerCapture(e.pointerId);
      e.preventDefault();
    });
    bar.addEventListener('pointermove', (e) => {
      if (!dragging) return;
      if (e.buttons === 0) { dragging = false; return; }
      const s = stage.getBoundingClientRect();
      const maxL = inside ? s.width - el.offsetWidth : s.width - 80, maxT = inside ? s.height - el.offsetHeight : s.height - 40;
      el.style.left = Math.max(0, Math.min(maxL, e.clientX - s.left - ox)) + 'px';
      el.style.top = Math.max(0, Math.min(maxT, e.clientY - s.top - oy)) + 'px';
    });
    bar.addEventListener('pointerup', () => { dragging = false; stage.scrollTop = 0; stage.scrollLeft = 0; });   // focusing a key must never scroll the slide away
    bar.addEventListener('pointercancel', () => { dragging = false; });
    bar.addEventListener('lostpointercapture', () => { dragging = false; });
  }

  // bottom-left corner: grows to the left and down
  function resizeLeft(el, handle) {
    let sx = 0, sy = 0, sw = 0, sh = 0, sl = 0, on = false;
    handle.addEventListener('pointerdown', (e) => {
      on = true; sx = e.clientX; sy = e.clientY; sw = el.offsetWidth; sh = el.offsetHeight; sl = el.offsetLeft;
      handle.setPointerCapture(e.pointerId);
      e.preventDefault(); e.stopPropagation();
    });
    handle.addEventListener('pointermove', (e) => {
      if (!on) return;
      if (e.buttons === 0) { on = false; return; }
      const w = Math.max(180, sw - (e.clientX - sx));
      el.style.width = w + 'px';
      el.style.left = Math.max(0, sl + (sw - w)) + 'px';
      if (!el.dataset.autoh) el.style.height = Math.max(140, sh + (e.clientY - sy)) + 'px'; else el.style.height = '';
    });
    const stop = () => { on = false; };
    handle.addEventListener('pointerup', stop); handle.addEventListener('pointercancel', stop); handle.addEventListener('lostpointercapture', stop);
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
      if (e.buttons === 0) { on = false; return; }
      el.style.width = Math.max(180, sw + (e.clientX - sx)) + 'px';
      if (!el.dataset.autoh) el.style.height = Math.max(140, sh + (e.clientY - sy)) + 'px'; else el.style.height = '';
    });
    handle.addEventListener('pointerup', () => { on = false; });
    handle.addEventListener('pointercancel', () => { on = false; });
    handle.addEventListener('lostpointercapture', () => { on = false; });
  }

  // ---- group poster (same design as the khmermath.org name wheel): download PNG / copy image for Telegram ----
  const PFONT = '"Kantumruy Pro", "Noto Sans Khmer", sans-serif';
  const PPAL = ['#e8590c', '#1c7ed6', '#2f9e44', '#ae3ec9', '#f08c00', '#0c8599', '#d6336c', '#5f3dc4'];
  const teacherName = () => { try { return String((JSON.parse(localStorage.getItem('exam_wheel_set') || '{}')).teacher || '').replace(/\s+/g, ' ').trim(); } catch { return ''; } };
  const khDate = () => { const d = new Date(); return kh(`${d.getDate()}/${d.getMonth() + 1}/${d.getFullYear()}`); };
  const rrect = (g, x, y, w, h2, r, tl = r, tr = r, br = r, bl = r) => {
    g.beginPath(); g.moveTo(x + tl, y); g.lineTo(x + w - tr, y); g.quadraticCurveTo(x + w, y, x + w, y + tr); g.lineTo(x + w, y + h2 - br);
    g.quadraticCurveTo(x + w, y + h2, x + w - br, y + h2); g.lineTo(x + bl, y + h2); g.quadraticCurveTo(x, y + h2, x, y + h2 - bl); g.lineTo(x, y + tl); g.quadraticCurveTo(x, y, x + tl, y); g.closePath();
  };
  function posterCanvas(o) {
    const FONT = PFONT, rr = rrect, whKh = kh;
    const W = 1600, pad = 56, gap = 26, n = o.groups.length, cols = n <= 1 ? 1 : n <= 4 ? 2 : 3;
    const cw = (W - pad * 2 - gap * (cols - 1)) / cols, headH = 80, lineH = 46, cpad = 18, bannerH = 250, footH = 110, dpr = 2;
    const rows = []; for (let i = 0; i < n; i += cols) rows.push(o.groups.slice(i, i + cols));
    const rowH = rows.map((r) => headH + Math.max(...r.map((x) => x.items.length)) * lineH + cpad * 2);
    const H = bannerH + 40 + rowH.reduce((a, b) => a + b, 0) + gap * (rows.length - 1) + 40 + footH;
    const cv = document.createElement('canvas'); cv.width = W * dpr; cv.height = H * dpr; const g = cv.getContext('2d'); g.scale(dpr, dpr);
    const bg = g.createLinearGradient(0, 0, 0, H); bg.addColorStop(0, '#eaf5f2'); bg.addColorStop(1, '#fdf6e8'); g.fillStyle = bg; g.fillRect(0, 0, W, H);
    const bn = g.createLinearGradient(0, 0, W, bannerH); bn.addColorStop(0, '#1f6f66'); bn.addColorStop(0.6, '#2d8f7e'); bn.addColorStop(1, '#3aa68f'); g.fillStyle = bn; g.fillRect(0, 0, W, bannerH);
    for (let k = 0; k < 46; k++) { const a = (k * 9301 + 49297) % 233280 / 233280, b = (k * 7919 + 1237) % 10007 / 10007;
      g.fillStyle = ['#ffd43b', '#ff8787', '#74c0fc', '#b2f2bb', '#ffffff'][k % 5]; g.globalAlpha = 0.55; g.save(); g.translate(a * W, b * bannerH); g.rotate(k); g.fillRect(-7, -3, 14, 6); g.restore(); }
    g.globalAlpha = 1; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillStyle = '#fff';
    g.font = `700 70px ${FONT}`; g.fillText(o.heading, W / 2, o.teacher ? 84 : 98); g.font = `500 33px ${FONT}`; g.globalAlpha = 0.92; g.fillText(o.sub, W / 2, o.teacher ? 154 : 178); g.globalAlpha = 1;
    if (o.teacher) { g.font = `600 34px ${FONT}`; g.fillText(`គ្រូបង្រៀន៖ ${o.teacher}`, W / 2, 204); }
    let y = bannerH + 40;
    rows.forEach((r, ri) => {
      r.forEach((grp, ci) => {
        const x = pad + ci * (cw + gap), h2 = rowH[ri], col = o.colors[(ri * cols + ci) % o.colors.length];
        g.save(); g.shadowColor = 'rgba(0,0,0,.18)'; g.shadowBlur = 22; g.shadowOffsetY = 8; g.fillStyle = '#fff'; rr(g, x, y, cw, h2, 22); g.fill(); g.restore();
        g.fillStyle = col; rr(g, x, y, cw, headH, 22, 22, 22, 0, 0); g.fill();
        g.fillStyle = '#fff'; g.textAlign = 'left'; g.font = `700 36px ${FONT}`; g.fillText(grp.title, x + 26, y + headH / 2 + 2);
        g.textAlign = 'right'; g.font = `500 28px ${FONT}`; g.globalAlpha = 0.9; g.fillText(`${whKh(grp.items.length)} នាក់`, x + cw - 24, y + headH / 2 + 2); g.globalAlpha = 1;
        grp.items.forEach((it, i) => {
          const ty = y + headH + cpad + i * lineH + lineH / 2; g.textAlign = 'left'; g.fillStyle = col; g.font = `700 26px ${FONT}`; g.fillText(`${whKh(i + 1)}.`, x + 24, ty);
          const dx = x + 76; let size = 33; g.font = `500 ${size}px ${FONT}`; while (g.measureText(it.n).width > x + cw - 20 - dx && size > 12) { size -= 2; g.font = `500 ${size}px ${FONT}`; }
          g.fillStyle = '#1b2733'; g.fillText(it.n, dx, ty);
        });
      });
      y += rowH[ri] + gap;
    });
    const fy = H - footH / 2 - 6;
    g.strokeStyle = 'rgba(31,111,102,.25)'; g.lineWidth = 2; g.beginPath(); g.moveTo(pad, H - footH); g.lineTo(W - pad, H - footH); g.stroke();
    g.fillStyle = '#12263a'; rr(g, W / 2 - 215, fy - 30, 60, 60, 14); g.fill();
    g.fillStyle = '#fff'; g.textAlign = 'center'; g.font = `700 38px ${FONT}`; g.fillText('√', W / 2 - 185, fy + 2);
    g.fillStyle = '#e0a13a'; rr(g, W / 2 - 172, fy - 4, 14, 14, 3); g.fill();
    g.textAlign = 'left'; g.fillStyle = '#1f6f66'; g.font = `700 42px ${FONT}`; g.fillText('khmermath.org', W / 2 - 140, fy - 2);
    g.fillStyle = '#5b6b7b'; g.font = `500 24px ${FONT}`; g.fillText('កង់ចាប់ឈ្មោះ · គណិតវិទ្យាខ្មែរ', W / 2 - 140, fy + 34);
    return cv;
  }
  // picture of the groups as a PNG blob
  async function posterBlob(groups, heading, cname) {
    try { if (document.fonts && document.fonts.load) await Promise.all([document.fonts.load('700 30px "Kantumruy Pro"', 'សិស្សក'), document.fonts.load('500 30px "Kantumruy Pro"', 'សិស្សក')]); } catch { /* fonts fall back */ }
    const total = groups.reduce((a, b) => a + b.items.length, 0);
    const cv = posterCanvas({ heading, sub: `${cname ? cname + '  ·  ' : ''}${kh(total)} នាក់  ·  ${khDate()}`, teacher: teacherName(), colors: PPAL, groups });
    return new Promise((res, rej) => cv.toBlob((b) => (b ? res(b) : rej(new Error('no image'))), 'image/png'));
  }
  const saveBlob = (blob, name) => { const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = name; document.body.appendChild(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(a.href), 4000); };
  const stamp14 = () => { const d = new Date(), z = (x) => String(x).padStart(2, '0'); return `${d.getFullYear()}${z(d.getMonth() + 1)}${z(d.getDate())}`; };

  // ---- Spin: wheel of the class list (one student or a group), pop-up result, sound and fireworks ----
  let audio = null;
  const snd = {
    ctx() { try { audio = audio || new (window.AudioContext || window.webkitAudioContext)(); if (audio.state === 'suspended') audio.resume(); } catch { audio = null; } return audio; },
    tick(on) { const c = on && this.ctx(); if (!c) return; const o = c.createOscillator(), g = c.createGain(); o.type = 'square'; o.frequency.value = 880; g.gain.setValueAtTime(.05, c.currentTime); g.gain.exponentialRampToValueAtTime(.0001, c.currentTime + .05); o.connect(g).connect(c.destination); o.start(); o.stop(c.currentTime + .06); },
    fanfare(on) { const c = on && this.ctx(); if (!c) return; [523, 659, 784, 1047, 1319].forEach((f, k) => { const o = c.createOscillator(), g = c.createGain(), t = c.currentTime + k * .11; o.type = 'triangle'; o.frequency.value = f; g.gain.setValueAtTime(.0001, t); g.gain.exponentialRampToValueAtTime(.18, t + .02); g.gain.exponentialRampToValueAtTime(.0001, t + .5); o.connect(g).connect(c.destination); o.start(t); o.stop(t + .55); }); },
    beep(on, hi) { const c = on && this.ctx(); if (!c) return; const o = c.createOscillator(), g = c.createGain(), t = c.currentTime; o.type = 'sine'; o.frequency.value = hi ? 1175 : 784; g.gain.setValueAtTime(.0001, t); g.gain.exponentialRampToValueAtTime(.3, t + .01); g.gain.exponentialRampToValueAtTime(.0001, t + .22); o.connect(g).connect(c.destination); o.start(t); o.stop(t + .25); },
    alarm(on) { const c = on && this.ctx(); if (!c) return; [0, .16].forEach((d) => { const o = c.createOscillator(), g = c.createGain(), t = c.currentTime + d; o.type = 'square'; o.frequency.value = 988; g.gain.setValueAtTime(.0001, t); g.gain.exponentialRampToValueAtTime(.12, t + .01); g.gain.exponentialRampToValueAtTime(.0001, t + .13); o.connect(g).connect(c.destination); o.start(t); o.stop(t + .15); }); },
    roll(on, ms) { // drum roll: quick soft taps that speed up
      if (!on || !this.ctx()) return () => {};
      let stopped = false, k = 0; const t0 = performance.now();
      const hit = () => { if (stopped) return; const c = audio, o = c.createOscillator(), g = c.createGain(), t = c.currentTime; o.type = 'triangle'; o.frequency.setValueAtTime(190 + Math.random() * 40, t); o.frequency.exponentialRampToValueAtTime(90, t + .06); g.gain.setValueAtTime(.18, t); g.gain.exponentialRampToValueAtTime(.0001, t + .08); o.connect(g).connect(c.destination); o.start(t); o.stop(t + .1); const p = (performance.now() - t0) / ms; if (p < 1) setTimeout(hit, Math.max(34, 95 - 60 * p)); };
      hit(); return () => { stopped = true; };
    },
    crash(on) { const c = on && this.ctx(); if (!c) return; const n = c.sampleRate * .9, buf = c.createBuffer(1, n, c.sampleRate), d = buf.getChannelData(0); for (let k = 0; k < n; k++) d[k] = (Math.random() * 2 - 1) * Math.pow(1 - k / n, 2.2); const src = c.createBufferSource(), f = c.createBiquadFilter(), g = c.createGain(); src.buffer = buf; f.type = 'highpass'; f.frequency.value = 3800; g.gain.value = .3; src.connect(f).connect(g).connect(c.destination); src.start(); [784, 1047].forEach((fr, i) => { const o = c.createOscillator(), og = c.createGain(), t = c.currentTime + i * .05; o.type = 'triangle'; o.frequency.value = fr; og.gain.setValueAtTime(.0001, t); og.gain.exponentialRampToValueAtTime(.12, t + .01); og.gain.exponentialRampToValueAtTime(.0001, t + .45); o.connect(og).connect(c.destination); o.start(t); o.stop(t + .5); }); },
    boom(on) { const c = on && this.ctx(); if (!c) return; const n = c.sampleRate * .35, buf = c.createBuffer(1, n, c.sampleRate), d = buf.getChannelData(0); for (let k = 0; k < n; k++) d[k] = (Math.random() * 2 - 1) * Math.pow(1 - k / n, 3); const src = c.createBufferSource(), f = c.createBiquadFilter(), g = c.createGain(); src.buffer = buf; f.type = 'lowpass'; f.frequency.value = 900; g.gain.value = .5; src.connect(f).connect(g).connect(c.destination); src.start(); },
  };

  function miniSpin(names, cname) {
    const wrap = document.createElement('div');
    wrap.className = 'sp';
    const bar = document.createElement('div'); bar.className = 'sp-bar';
    const modeBtns = [['one', 'ម្នាក់ៗ'], ['group', 'ក្រុម']].map(([m, t]) => { const b = document.createElement('button'); b.type = 'button'; b.textContent = t; b.dataset.m = m; return b; });
    const gsel = document.createElement('select'); gsel.title = 'ចំនួនសិស្សក្នុងមួយក្រុម';
    [2, 3, 4, 5, 6, 7, 8, 9, 10].forEach((n) => gsel.append(new Option(`${kh(n)} នាក់/ក្រុម`, n)));
    gsel.value = 6;
    const dvd = document.createElement('button'); dvd.type = 'button'; dvd.className = 'sp-dvd'; dvd.textContent = '👥 ចែកក្រុម'; dvd.title = 'ចែកថ្នាក់ជាក្រុមៗ ហើយបង្ហាញទាំងអស់';
    const rep = document.createElement('label'); rep.className = 'sp-chk'; rep.innerHTML = '<input type="checkbox" checked><span>មិនជាន់</span>';
    const snb = document.createElement('button'); snb.type = 'button'; snb.className = 'sp-snd'; snb.textContent = '🔊'; snb.title = 'សំឡេង';
    const rst = document.createElement('button'); rst.type = 'button'; rst.className = 'sp-rst'; rst.textContent = '↺'; rst.title = 'ចាប់ផ្ដើមឡើងវិញ';
    bar.append(rep, snb, rst);
    const abBtn = document.createElement('button'); abBtn.type = 'button'; abBtn.className = 'sp-ab'; abBtn.textContent = '✕ អវត្តមាន'; abBtn.title = 'គូសឈ្មោះសិស្សដែលអវត្តមាន';
    const modes = document.createElement('div'); modes.className = 'sp-modes'; modes.append(...modeBtns, gsel, dvd, abBtn);
    const stageW = document.createElement('div'); stageW.className = 'sp-wheel';
    const cv = document.createElement('canvas'); cv.width = 640; cv.height = 640;
    const hub = document.createElement('button'); hub.type = 'button'; hub.className = 'sp-hub'; hub.textContent = 'SPIN';
    const disc = document.createElement('div'); disc.className = 'sp-disc';
    disc.append(cv, hub); stageW.append(disc);
    const info = document.createElement('div'); info.className = 'sp-info';
    const pop = document.createElement('div'); pop.className = 'sp-pop'; pop.hidden = true;
    // vanish in / vanish out for the pop-ups
    let popT = 0;
    const calmMotion = () => window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
    const openPop = () => { clearTimeout(popT); pop.classList.remove('vout'); pop.hidden = false; pop.classList.remove('vin'); void pop.offsetWidth; if (!calmMotion()) pop.classList.add('vin'); };
    const closePop = (instant) => {
      if (pop.hidden) return;
      clearTimeout(popT);
      if (instant || calmMotion()) { pop.hidden = true; pop.classList.remove('vin', 'vout'); return; }
      pop.classList.remove('vin'); pop.classList.add('vout');
      popT = setTimeout(() => { pop.hidden = true; pop.classList.remove('vout'); }, 430);
    };
    const fw = document.createElement('canvas'); fw.className = 'sp-fw';
    // simple by default: only the wheel; the options live behind a small gear
    bar.hidden = true;
    const gear = document.createElement('button'); gear.type = 'button'; gear.className = 'sp-gear'; gear.textContent = '⚙'; gear.title = 'ជម្រើស';
    gear.onclick = () => { bar.hidden = !bar.hidden; gear.classList.toggle('on', !bar.hidden); };
    // choose the class first (the teacher's own classes), then spin: picking one loads its students onto the wheel
    const crow = document.createElement('div'); crow.className = 'sp-cls';
    const csel = document.createElement('select'); csel.title = 'ជ្រើសថ្នាក់';
    csel.append(new Option('— ជ្រើសថ្នាក់ —', ''));
    crow.append(Object.assign(document.createElement('span'), { textContent: 'ថ្នាក់' }), csel);
    const rp = document.createElement('div'); rp.className = 'sp-roster'; rp.hidden = true;
    const dealt = document.createElement('div'); dealt.className = 'sp-dealt'; dealt.hidden = true;
    wrap.append(crow, modes, bar, stageW, info, dealt, pop, fw, gear, rp);
    const c = cv.getContext('2d');
    const pal = ['#e8590c', '#1c7ed6', '#2f9e44', '#ae3ec9', '#f08c00', '#0c8599', '#d6336c', '#5f3dc4', '#c92a2a', '#087f5b'];
    const st = { mode: 'one', sound: true, ang: 0, spin: false, used: new Set(), groups: [] };
    const absent = new Set();   // students the teacher crossed out: they leave the wheel and the groups
    let roster = names.length ? names.slice() : ['សិស្ស ក', 'សិស្ស ខ', 'សិស្ស គ', 'សិស្ស ឃ'];
    const shuffle = (a) => { a = a.slice(); for (let k = a.length - 1; k > 0; k--) { const j = Math.floor(Math.random() * (k + 1)); [a[k], a[j]] = [a[j], a[k]]; } return a; };
    const live = () => roster.filter((n) => !absent.has(n));
    const makeGroups = () => { st.dealt = false; for (let k = PPAL.length - 1; k > 0; k--) { const j = Math.floor(Math.random() * (k + 1)); [PPAL[k], PPAL[j]] = [PPAL[j], PPAL[k]]; }   // a new random colour set for every deal
      const size = +gsel.value || 6, R = live(), n = Math.max(1, Math.ceil(R.length / size)), g = Array.from({ length: n }, () => []); shuffle(R).forEach((nm, k) => g[k % n].push(nm)); st.groups = g; };
    makeGroups();
    // what is on the wheel right now
    const items = () => {
      const noRep = rep.querySelector('input').checked;
      if (st.mode === 'one') return live().map((n) => ({ id: 'o:' + n, label: n, members: [n] })).filter((x) => !(noRep && st.used.has(x.id)));
      return st.groups.map((g, k) => ({ id: 'g' + k, label: `ក្រុម ${kh(k + 1)}`, members: g })).filter((x) => !(noRep && st.used.has(x.id)));
    };
    let list = items();
    const refresh = () => {
      list = items();
      modeBtns.forEach((b) => b.classList.toggle('on', b.dataset.m === st.mode));
      gsel.style.display = dvd.style.display = st.mode === 'group' ? '' : 'none';
      dealt.hidden = !(st.mode === 'group' && st.dealt);
      if (!dealt.hidden) dealt.innerHTML = st.groups.map((g, k) => `<div class="sp-dg" style="--c:${PPAL[k % PPAL.length]}"><b>ក្រុម ${kh(k + 1)}</b> <span>${esc(g.join(' · '))}</span></div>`).join('');
      abBtn.textContent = absent.size ? `✕ អវត្តមាន ${kh(absent.size)}` : '✕ អវត្តមាន';
      const total = st.mode === 'one' ? live().length : st.groups.length;
      info.textContent = `${cname ? cname + ' · ' : ''}${st.mode === 'one' ? 'សិស្ស' : 'ក្រុម'} ${kh(list.length)}/${kh(total)}${list.length ? '' : ' — អស់ហើយ ចុច ↺'}`;
      draw();
    };
    function draw() {
      const n = list.length || 1, W = cv.width, r = W / 2 - 6, a = Math.PI * 2 / n;
      c.clearRect(0, 0, W, W); c.save(); c.translate(W / 2, W / 2); c.rotate(st.ang);
      for (let k = 0; k < n; k++) {
        c.beginPath(); c.moveTo(0, 0); c.arc(0, 0, r, k * a - Math.PI / 2 - a / 2, k * a - Math.PI / 2 + a / 2); c.closePath();
        c.fillStyle = list.length ? pal[k % pal.length] : '#6b7a89'; c.fill();
        c.strokeStyle = 'rgba(255,255,255,.55)'; c.lineWidth = 2; c.stroke();
        if (!list.length) continue;
        c.save(); c.rotate(k * a - Math.PI / 2);
        const fs = Math.max(13, Math.min(46, (Math.PI * 2 * r * 0.62 / n) * 0.72));
        c.fillStyle = '#fff'; c.font = `800 ${fs}px "Kantumruy Pro", "Khmer OS Battambang", sans-serif`; c.textAlign = 'left'; c.textBaseline = 'middle';
        c.shadowColor = 'rgba(0,0,0,.35)'; c.shadowBlur = 3;
        c.fillText(list[k].label, r * 0.3, 0, r * 0.66);
        c.restore();
      }
      c.restore();
    }

    // ---- fireworks (canvas over the whole spin window; also works full screen) ----
    let fwRaf = 0, parts = [], fwUntil = 0, nextBurst = 0, fwBox = { w: 0, h: 0 }, fc = null;
    const fwSize = () => {
      const r = fw.parentElement.getBoundingClientRect(), dpr = Math.min(2, window.devicePixelRatio || 1);
      const w = Math.floor(r.width * dpr), h = Math.floor(r.height * dpr);
      if (fw.width !== w || fw.height !== h) { fw.width = w; fw.height = h; }
      fc = fw.getContext('2d'); fc.setTransform(dpr, 0, 0, dpr, 0, 0); fwBox = { w: r.width, h: r.height };
    };
    const addBurst = (x, y, n = 46) => {
      const hue = [8, 40, 52, 130, 190, 280, 330][Math.floor(Math.random() * 7)];
      for (let k = 0; k < n; k++) { const a = Math.PI * 2 * k / n + Math.random() * .2, v = 2.2 + Math.random() * 3.6; parts.push({ x, y, vx: Math.cos(a) * v, vy: Math.sin(a) * v, life: 1, hue: hue + Math.random() * 40, w: 2 + Math.random() * 2 }); }
    };
    const fwLoop = (now) => {
      fwRaf = 0;
      fc.globalCompositeOperation = 'destination-out'; fc.fillStyle = 'rgba(0,0,0,.22)'; fc.fillRect(0, 0, fwBox.w, fwBox.h); fc.globalCompositeOperation = 'lighter';
      if (now < fwUntil && now >= nextBurst) { addBurst(fwBox.w * (.15 + Math.random() * .7), fwBox.h * (.12 + Math.random() * .5)); snd.boom(st.sound); nextBurst = now + 380 + Math.random() * 260; }
      parts.forEach((q) => { q.x += q.vx; q.y += q.vy; q.vy += .045; q.vx *= .992; q.life -= .011; fc.globalAlpha = Math.max(0, q.life); fc.fillStyle = `hsl(${q.hue} 95% 60%)`; fc.beginPath(); fc.arc(q.x, q.y, q.w, 0, Math.PI * 2); fc.fill(); });
      fc.globalAlpha = 1; fc.globalCompositeOperation = 'source-over';
      parts = parts.filter((q) => q.life > 0);
      if (now < fwUntil || parts.length) fwRaf = requestAnimationFrame(fwLoop); else fc.clearRect(0, 0, fwBox.w, fwBox.h);
    };
    function fireworks(ms) { fwSize(); fwUntil = performance.now() + ms; nextBurst = 0; if (!fwRaf) fwRaf = requestAnimationFrame(fwLoop); }
    // a small burst at one card when its group locks in
    const burstAt = (el) => {
      fwSize(); const r = el.getBoundingClientRect(), w = fw.parentElement.getBoundingClientRect();
      addBurst(r.right - w.left - 30, r.top - w.top + 26, 30); snd.boom(st.sound);
      if (!fwRaf) fwRaf = requestAnimationFrame(fwLoop);
    };

    // ---- result pop-up, sized from the spin window ----
    const showPop = (it) => {
      const noRep = rep.querySelector('input').checked;
      if (noRep) st.used.add(it.id);
      openPop(); pop.classList.remove('big');
      const group = st.mode === 'group';
      pop.innerHTML = `<div class="pp-card"><div class="pp-k">${group ? '🎉 ក្រុមដែលត្រូវបានជ្រើស' : '🎉 សិស្សដែលត្រូវបានជ្រើស'}</div>
        <div class="pp-name">${esc(it.label)}</div>
        ${group ? `<ul class="pp-mem">${it.members.map((m) => `<li>${esc(m)}</li>`).join('')}</ul>` : ''}
        <div class="pp-act">${group ? '<button type="button" class="pp-png">⬇ ទាញយក PNG</button><button type="button" class="pp-copy">📋 ចម្លងរូបភាព</button>' : ''}${group ? '' : '<button type="button" class="pp-abs">✕ អវត្តមាន</button>'}<button type="button" class="pp-again">បង្វិលម្ដងទៀត</button><button type="button" class="pp-ok">បិទ</button></div></div>`;
      pop.querySelector('.pp-ok').onclick = () => { closePop(); refresh(); };
      const pa = pop.querySelector('.pp-abs'); if (pa) pa.onclick = () => { absent.add(it.members[0]); st.used.delete(it.id); closePop(true); refresh(); };
      pop.querySelector('.pp-again').onclick = () => { closePop(true); refresh(); hub.click(); };
      if (group) wirePoster([{ title: it.label, items: it.members.map((n) => ({ n })) }], 'ក្រុមដែលត្រូវបានជ្រើស', 'group');
      snd.fanfare(st.sound);
      fireworks(3200);
    };
    const esc = (t) => String(t).replace(/[&<>]/g, (m) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[m]));

    // divide the whole class into groups and show every group at once
    // download the poster / copy it to the clipboard so it can be pasted straight into Telegram
    const wirePoster = (groups, heading, tag) => {
      const png = pop.querySelector('.pp-png'), cp = pop.querySelector('.pp-copy');
      const flash = (b, t, back) => { b.textContent = t; setTimeout(() => { b.textContent = back; }, 2400); };
      png.onclick = async () => {
        png.textContent = 'កំពុងបង្កើត…';
        try { saveBlob(await posterBlob(groups, heading, cname), `khmermath-${tag}-${stamp14()}.png`); flash(png, '✓ បានទាញយក', '⬇ ទាញយក PNG'); }
        catch { flash(png, 'មិនអាចបង្កើតរូបបាន', '⬇ ទាញយក PNG'); }
      };
      cp.onclick = async () => {
        cp.textContent = 'កំពុងចម្លង…';
        try {
          if (!navigator.clipboard || !window.ClipboardItem) throw new Error('unsupported');
          await navigator.clipboard.write([new ClipboardItem({ 'image/png': posterBlob(groups, heading, cname) })]);
          flash(cp, '✓ បានចម្លង — ចុច Paste ក្នុង Telegram', '📋 ចម្លងរូបភាព');
        } catch { flash(cp, 'ចម្លងមិនបាន — សូមប្រើ ទាញយក', '📋 ចម្លងរូបភាព'); }
      };
    };
    let gRun = 0;
    // full screen shows only the group pop-up; the Spin window itself keeps its size
    let fsRoot = null;
    const exitFull = () => {
      if (!fsRoot) return;
      const r = fsRoot; fsRoot = null;
      if (document.fullscreenElement) { try { document.exitFullscreen(); } catch { /* ignore */ } }
      const back = () => { wrap.append(pop, fw); r.remove(); pop.classList.remove('full'); };
      if (calmMotion()) return back();
      r.classList.add('vout'); setTimeout(back, 400);
    };
    const enterFull = () => {
      fsRoot = document.createElement('div'); fsRoot.className = 'sp-fsroot';
      root.append(fsRoot); fsRoot.append(pop, fw); pop.classList.add('full'); if (!calmMotion()) fsRoot.classList.add('vin');
      try { (fsRoot.requestFullscreen || fsRoot.webkitRequestFullscreen).call(fsRoot); } catch { /* the fixed overlay still fills the window */ }
    };
    const toggleFull = () => (fsRoot ? exitFull() : enterFull());
    document.addEventListener('fullscreenchange', () => { if (fsRoot && !document.fullscreenElement) exitFull(); });
    const showGroups = (again) => {
      if (again) makeGroups();
      st.dealt = true; refresh();   // the groups stay listed under the wheel after the banner is closed
      const id = ++gRun, n = st.groups.length, calm = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
      openPop(); pop.classList.add('big');
      const total = st.groups.reduce((a, g) => a + g.length, 0), tch = teacherName();
      pop.innerHTML = `<div class="pp-card pp-all"><div class="pp-ban"><b class="pp-title">កំពុងបែងចែកក្រុម…</b><small>${esc(cname || '')}${cname ? ' · ' : ''}${kh(total)} នាក់ · ${khDate()}</small>${tch ? `<small>គ្រូបង្រៀន៖ ${esc(tch)}</small>` : ''}<button type="button" class="pp-fs" title="ពេញអេក្រង់">⛶</button></div>
        <div class="pp-grid">${st.groups.map((g, k) => `<div class="pp-g wait" style="--c:${PPAL[k % PPAL.length]}"><div class="pp-gh"><b>ក្រុម ${kh(k + 1)}</b><span>${kh(g.length)} នាក់</span></div><ol>${g.map(() => '<li class="ph">• • •</li>').join('')}</ol></div>`).join('')}</div>
        <div class="pp-act"><button type="button" class="pp-skip">រំលង ▶▶</button><button type="button" class="pp-png" hidden>⬇ ទាញយក PNG</button><button type="button" class="pp-copy" hidden>📋 ចម្លងរូបភាព</button><button type="button" class="pp-again" hidden>ចែកម្ដងទៀត</button><button type="button" class="pp-ok">បិទ</button></div></div>`;
      const q = (c) => pop.querySelector(c), cards = [...pop.querySelectorAll('.pp-g')], title = q('.pp-title');
      q('.pp-ok').onclick = () => { gRun++; stopRoll(); exitFull(); closePop(); st.used.clear(); refresh(); };
      q('.pp-again').onclick = () => showGroups(true);
      q('.pp-fs').onclick = toggleFull;
      wirePoster(st.groups.map((g, k) => ({ title: `ក្រុម ${kh(k + 1)}`, items: g.map((nm) => ({ n: nm })) })), 'បែងចែកក្រុមរួចរាល់!', 'groups');
      const fill = (card, names) => { card.querySelector('ol').innerHTML = names.map((m) => `<li>${esc(m)}</li>`).join(''); };
      let remaining = st.groups.flat(), cur = -1, phase = 'start', t0 = 0, last = 0, skip = false, stopRollFn = null;
      const stopRoll = () => { if (stopRollFn) { stopRollFn(); stopRollFn = null; } };
      q('.pp-skip').onclick = () => { skip = true; };
      const per = calm ? 0 : Math.max(800, Math.min(1500, 9000 / n)), pause = calm ? 0 : 380;
      const lock = (i, fx) => {
        const card = cards[i]; card.className = 'pp-g done'; fill(card, st.groups[i]);
        const ids = new Set(st.groups[i]); remaining = remaining.filter((m) => !ids.has(m));
        if (fx) { snd.crash(st.sound); burstAt(card); }
      };
      const finale = () => {
        stopRoll(); title.textContent = 'បែងចែកក្រុមរួចរាល់! 🎉';
        pop.querySelector('.pp-skip').hidden = true; ['.pp-png', '.pp-copy', '.pp-again'].forEach((c) => { q(c).hidden = false; });
        snd.fanfare(st.sound); fireworks(3600);
      };
      const frame = (now) => {
        if (id !== gRun) { stopRoll(); return; }
        if (skip) { for (let k = Math.max(cur, 0); k < n; k++) if (cards[k].className !== 'pp-g done') lock(k, false); return finale(); }
        if (phase === 'start' || (phase === 'pause' && now - t0 >= pause)) {
          cur++; if (cur >= n) return finale();
          phase = 'roll'; t0 = now; cards[cur].className = 'pp-g active'; title.textContent = `កំពុងបែងចែក ក្រុមទី ${kh(cur + 1)}…`;
          { const gr = q('.pp-grid'); gr.scrollTo({ top: Math.max(0, cards[cur].offsetTop - gr.offsetTop - 8), behavior: 'smooth' }); } // scroll only the list, never the page
          stopRoll(); stopRollFn = snd.roll(st.sound, per);
        }
        if (phase === 'roll') {
          if (now - t0 >= per) { stopRoll(); lock(cur, true); phase = 'pause'; t0 = now; }
          else if (now - last > 80) { last = now; fill(cards[cur], shuffle(remaining).slice(0, st.groups[cur].length)); }
        }
        requestAnimationFrame(frame);
      };
      if (calm) { cards.forEach((c, i) => lock(i, false)); finale(); } else requestAnimationFrame(frame);
    };
    dvd.onclick = () => { if (st.spin) return; if (st.mode !== 'group') { st.mode = 'group'; st.used.clear(); st.ang = 0; } showGroups(true); refresh(); };

    hub.onclick = () => {
      if (st.spin || !list.length) return;
      closePop(true); snd.ctx();
      const pick = Math.floor(Math.random() * list.length), it = list[pick], a = Math.PI * 2 / list.length;
      const TAU = Math.PI * 2, from = st.ang, target = -pick * a;
      const to = from + ((((target - from) % TAU) + TAU) % TAU) + TAU * (5 + Math.floor(Math.random() * 3));
      const t0 = performance.now(), dur = 4200; st.spin = true; hub.disabled = true;
      let lastSlice = Math.floor((from + a / 2) / a);
      const frame = (now) => {
        const t = Math.min(1, (now - t0) / dur);
        st.ang = from + (to - from) * (1 - Math.pow(1 - t, 4)); draw();
        const sl = Math.floor((st.ang + a / 2) / a);
        if (sl !== lastSlice) { lastSlice = sl; snd.tick(st.sound); }
        if (t < 1) return requestAnimationFrame(frame);
        st.spin = false; hub.disabled = false; st.ang = ((st.ang % TAU) + TAU) % TAU;
        showPop(it);
      };
      requestAnimationFrame(frame);
    };
    modeBtns.forEach((b) => { b.onclick = () => { if (st.spin) return; st.mode = b.dataset.m; st.used.clear(); st.ang = 0; closePop(true); refresh(); }; });
    gsel.onchange = () => { if (st.spin) return; makeGroups(); st.used.clear(); refresh(); };
    rep.querySelector('input').onchange = refresh;
    snb.onclick = () => { st.sound = !st.sound; snb.textContent = st.sound ? '🔊' : '🔇'; };
    rst.onclick = () => { if (st.spin) return; st.used.clear(); if (st.mode === 'group') makeGroups(); closePop(true); refresh(); };
    fetch('/api/classes').then((r) => (r.ok ? r.json() : null)).then((d) => {
      ((d && d.classes) || []).forEach((k) => csel.append(new Option(k.name, k.id)));
      const cur = [...csel.options].find((o) => o.value && o.text === cname); if (cur) csel.value = cur.value;
    }).catch(() => {});
    // the roster panel: tap a name to cross it out (absent) or bring it back
    const drawRoster = () => {
      rp.innerHTML = '';
      const hd = document.createElement('div'); hd.className = 'sp-rh'; hd.innerHTML = `<b>ចុចឈ្មោះដែលអវត្តមាន</b><span>${kh(absent.size)}/${kh(roster.length)}</span>`;
      const box = document.createElement('div'); box.className = 'sp-rc';
      roster.forEach((n) => {
        const b = document.createElement('button'); b.type = 'button'; b.className = 'sp-chip' + (absent.has(n) ? ' off' : ''); b.textContent = n;
        b.onclick = () => { if (absent.has(n)) absent.delete(n); else absent.add(n); if (st.mode === 'group') makeGroups(); drawRoster(); refresh(); };
        box.append(b);
      });
      const ok = document.createElement('button'); ok.type = 'button'; ok.className = 'sp-rok'; ok.textContent = 'រួចរាល់';
      ok.onclick = () => { rp.hidden = true; };
      rp.append(hd, box, ok);
    };
    abBtn.onclick = () => { if (st.spin) return; closePop(true); drawRoster(); rp.hidden = false; };
    csel.onchange = async () => {
      if (st.spin || !csel.value) return;
      try {
        const r = await fetch(`/api/classes/${csel.value}/students`), d = await r.json();
        const nm = ((d && d.students) || []).map((s) => `${s.surname || ''} ${s.first_name || ''}`.trim()).filter(Boolean);
        cname = csel.options[csel.selectedIndex].text;
        const t = wrap.closest('.ts-float') && wrap.closest('.ts-float').querySelector('.ts-fbar b'); if (t) t.textContent = `Spin · ${cname}`;
        roster = nm.length ? nm : ['(ថ្នាក់នេះមិនទាន់មានសិស្ស)']; absent.clear(); rp.hidden = true;
        st.used.clear(); st.ang = 0; closePop(true); makeGroups(); refresh();
      } catch { info.textContent = 'ទាញបញ្ជីសិស្សមិនបាន'; }
    };
    refresh();
    return wrap;
  }

  // ---- Timer: hourglass + stopwatch dial (red wedge = time left), presets, alarm ----
  function timerBox() {
    const wrap = document.createElement('div');
    wrap.className = 'tm';
    const CX = 150, CY = 190, RF = 94; // dial centre and face radius
    let ticks = '';
    for (let k = 0; k < 60; k++) {
      const major = k % 5 === 0, a = k * Math.PI / 30, r1 = 88, r2 = r1 - (major ? 17 : 9), w = major ? 6.5 : 3.6;
      ticks += `<line x1="${CX + r1 * Math.sin(a)}" y1="${CY - r1 * Math.cos(a)}" x2="${CX + r2 * Math.sin(a)}" y2="${CY - r2 * Math.cos(a)}" stroke="${major ? '#2b73a3' : '#4b93bd'}" stroke-width="${w}" stroke-linecap="butt"/>`;
    }
    let ridges = '';
    for (let k = 0; k < 5; k++) ridges += `<rect x="${133 + k * 8.6}" y="20" width="3.4" height="22" rx="1.2" fill="rgba(255,255,255,.5)"/>`;
    ridges += `<text class="tm-cm" x="120" y="42" text-anchor="middle" font-size="26" font-weight="800" fill="#fff">−</text><text class="tm-cp" x="180" y="42" text-anchor="middle" font-size="26" font-weight="800" fill="#fff">+</text><line x1="150" y1="18" x2="150" y2="46" stroke="rgba(255,255,255,.28)" stroke-width="1.5"/>`;
    wrap.innerHTML = `<svg viewBox="0 0 300 330" class="tm-svg" aria-hidden="true">
      <defs>
        <linearGradient id="tmBody" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4ba0c9"/><stop offset="1" stop-color="#21588a"/></linearGradient>
        <linearGradient id="tmBtn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3f93bd"/><stop offset="1" stop-color="#2a6b99"/></linearGradient>
        <linearGradient id="tmCore" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3d93bd"/><stop offset="1" stop-color="#235b88"/></linearGradient>
      </defs>
      <g class="tm-side" transform="rotate(45 ${CX} ${CY})"><title>ប៊ូតុងចំហៀង៖ ចាប់ផ្ដើម / ឈប់</title><g class="pb"><rect x="141" y="54" width="18" height="30" fill="#2a6592"/><rect x="128" y="36" width="44" height="26" rx="7" fill="url(#tmBtn)"/></g><rect x="120" y="28" width="60" height="58" fill="transparent"/></g>
      <g class="tm-crown"><title>ប៊ូតុងលើ៖ ចុចខាងស្តាំ (+) បន្ថែមម៉ោង · ចុចខាងឆ្វេង (−) ដកម៉ោង · កង់កណ្ដុរ</title><rect x="138" y="44" width="24" height="40" fill="#2a6592"/>
      <rect x="108" y="14" width="84" height="40" rx="8" fill="url(#tmBtn)"/>
      ${ridges}<rect x="104" y="10" width="92" height="48" fill="transparent"/></g>
      <circle cx="${CX + 3}" cy="${CY + 7}" r="124" fill="rgba(0,0,0,.14)"/>
      <circle cx="${CX}" cy="${CY}" r="122" fill="url(#tmBody)"/>
      <circle cx="${CX}" cy="${CY}" r="106" fill="#2b6a97"/>
      <circle cx="${CX}" cy="${CY}" r="${RF}" fill="#fff"/>
      <path class="tm-wedge" d="M${CX} ${CY}" fill="#8fc4e8"/>
      ${ticks}
      <circle cx="${CX}" cy="${CY}" r="58" fill="url(#tmCore)"/>
      <text class="tm-num" x="${CX}" y="${CY + 12}" text-anchor="middle" fill="#fff" font-size="56" font-weight="800">5</text>
      <text class="tm-unit" x="${CX}" y="${CY + 38}" text-anchor="middle" fill="#fff" font-size="19" font-weight="700">នាទី</text>
      <text class="tm-state" x="${CX}" y="${CY - 33}" text-anchor="middle" fill="#fff" font-size="15" opacity=".8">▶</text>
      <circle class="tm-core" cx="${CX}" cy="${CY}" r="58" fill="transparent"><title>ចុចដើម្បីចាប់ផ្ដើម / ឈប់</title></circle>
    </svg>`;
    const q = (c) => wrap.querySelector(c);
    const wedge = q('.tm-wedge'), num = q('.tm-num'), unit = q('.tm-unit'), stateEl = q('.tm-state'), core = q('.tm-core');
    const digital = document.createElement('div'); digital.className = 'tm-dig';
    let total = 300, left = 300, run = false, t0 = 0, remain0 = 0, raf = 0, alarmT = 0, lastBeep = -1;
    const paint = () => {
      const f = total > 0 ? Math.max(0, Math.min(1, left / total)) : 0, th = f * Math.PI * 2;
      if (f >= .9995) wedge.setAttribute('d', `M${CX - RF} ${CY} a${RF} ${RF} 0 1 0 ${2 * RF} 0 a${RF} ${RF} 0 1 0 ${-2 * RF} 0Z`);
      else if (f <= 0) wedge.setAttribute('d', `M${CX} ${CY}`);
      else wedge.setAttribute('d', `M${CX} ${CY} L${CX} ${CY - RF} A${RF} ${RF} 0 ${th > Math.PI ? 1 : 0} 1 ${CX + RF * Math.sin(th)} ${CY - RF * Math.cos(th)} Z`);
      stateEl.textContent = run ? '❚❚' : '▶';
      const sec = Math.max(0, Math.ceil(left));
      if (sec >= 60) { num.textContent = Math.ceil(left / 60); unit.textContent = 'នាទី'; } else { num.textContent = sec; unit.textContent = 'វិនាទី'; }
      num.setAttribute('font-size', String(num.textContent).length > 2 ? 40 : 52);
      digital.textContent = `${String(Math.floor(sec / 60)).padStart(2, '0')}:${String(sec % 60).padStart(2, '0')}`;
    };
    const stop = () => { run = false; cancelAnimationFrame(raf); paint(); startBtn.textContent = left <= 0 ? '▶ ចាប់ផ្ដើម' : '▶ បន្ត'; };
    const tick = (now) => {
      if (!run) return;
      left = Math.max(0, remain0 - (now - t0) / 1000);
      paint();
      const cs = Math.ceil(left); // beep once a second for the last 5 seconds
      if (cs >= 1 && cs <= 5 && cs !== lastBeep) { lastBeep = cs; snd.beep(true, cs === 1); wrap.classList.remove('last'); void wrap.offsetWidth; wrap.classList.add('last'); }
      if (left <= 0) { run = false; paint(); startBtn.textContent = '▶ ចាប់ផ្ដើម'; wrap.classList.add('done'); [0, 450, 900].forEach((d) => setTimeout(() => snd.alarm(true), d)); return; }
      raf = requestAnimationFrame(tick);
    };
    const setTotal = (sec) => { lastBeep = -1; wrap.classList.remove('last'); run = false; cancelAnimationFrame(raf); total = left = sec; wrap.classList.remove('done'); startBtn.textContent = '▶ ចាប់ផ្ដើម'; paint(); };
    const btn = (lab, fn, cls) => { const b = document.createElement('button'); b.type = 'button'; b.textContent = lab; if (cls) b.className = cls; b.onclick = fn; return b; };
    const startBtn = btn('▶ ចាប់ផ្ដើម', () => {
      if (run) { stop(); return; }
      if (left <= 0) { left = total; wrap.classList.remove('done'); }
      lastBeep = -1; run = true; t0 = performance.now(); remain0 = left; startBtn.textContent = '❚❚ ផ្អាក';
      snd.ctx(); raf = requestAnimationFrame(tick);
    }, 'go');
    const presets = document.createElement('div'); presets.className = 'tm-pre';
    [['10វិ', 10], ['30វិ', 30], ['1', 60], ['3', 180], ['5', 300], ['10', 600], ['15', 900], ['20', 1200], ['30', 1800], ['45', 2700], ['50', 3000], ['60', 3600]].forEach(([t, sec]) => presets.append(btn(t, () => setTotal(sec))));
    // any length: minutes and seconds, Enter or កំណត់
    const cust = document.createElement('div'); cust.className = 'tm-cust';
    const mk = (ph, max) => { const i = document.createElement('input'); i.type = 'number'; i.min = '0'; i.max = String(max); i.placeholder = ph; i.inputMode = 'numeric'; return i; };
    const inM = mk('នាទី', 600), inS = mk('វិនាទី', 59);
    const ok = btn('កំណត់', () => { const sec = Math.round((parseFloat(inM.value) || 0) * 60 + (parseFloat(inS.value) || 0)); if (sec >= 5 && sec <= 36000) { setTotal(sec); inM.value = inS.value = ''; } });
    [inM, inS].forEach((i) => { i.onkeydown = (e) => { e.stopPropagation(); if (e.key === 'Enter') ok.click(); }; });
    cust.append(inM, Object.assign(document.createElement('b'), { textContent: ':' }), inS, Object.assign(ok, { className: 'ok' }));
    const adj = (d) => { if (run) { remain0 = Math.max(5, remain0 + d); total = Math.max(5, total + d); t0 = performance.now(); left = remain0; } else { setTotal(Math.max(5, total + d)); } paint(); };
    const row = document.createElement('div'); row.className = 'tm-row';
    row.append(btn('−១ នាទី', () => adj(-60)), startBtn, btn('+១ នាទី', () => adj(60)), btn('↺', () => setTotal(total), 'rst'));
    const row2 = document.createElement('div'); row2.className = 'tm-row'; row2.style.marginTop = '6px';
    row2.append(btn('−៣០ វិ', () => adj(-30)), btn('+៣០ វិ', () => adj(30)));
    const lab = document.createElement('div'); lab.className = 'tm-lab'; lab.textContent = 'នាទី៖';
    const pr = document.createElement('div'); pr.className = 'tm-prw'; pr.append(lab, presets);
    const more = document.createElement('div'); more.className = 'tm-more'; more.hidden = true;
    more.append(row, pr, cust, row2);
    const moreBtn = document.createElement('button'); moreBtn.type = 'button'; moreBtn.className = 'tm-morebtn'; moreBtn.textContent = '⚙'; moreBtn.title = 'ជម្រើសបន្ថែម';
    moreBtn.onclick = () => { more.hidden = !more.hidden; moreBtn.classList.toggle('on', !more.hidden); };
    wrap.append(digital, moreBtn, more);
    const hint = document.createElement('div'); hint.className = 'tm-hint';
    hint.textContent = 'ប៊ូតុងលើ៖ ស្តាំ + បន្ថែម · ឆ្វេង − ដក (ចុចជាប់ = លឿន) · ប៊ូតុងចំហៀង = ចាប់ផ្ដើម/ឈប់';
    // real-device buttons: crown on top sets the time, button on the side starts / stops
    const crown = q('.tm-crown'), side = q('.tm-side');
    const crownStep = (dir) => {
      const step = dir > 0 ? (total < 60 ? 10 : 60) : (total <= 60 ? 10 : 60);
      const next = Math.max(10, Math.min(36000, total + dir * step));
      setTotal(next); snd.tick(true);
    };
    let holdT = 0, holdI = 0;
    const holdStop = () => { clearTimeout(holdT); clearInterval(holdI); holdT = holdI = 0; crown.classList.remove('down'); };
    crown.addEventListener('pointerdown', (e) => {
      e.preventDefault(); crown.setPointerCapture && crown.setPointerCapture(e.pointerId);
      holdStop();
      const rc = crown.getBoundingClientRect();
      const dir = e.shiftKey || e.button === 2 || e.clientX < rc.left + rc.width / 2 ? -1 : 1; // left half withdraws, right half adds
      crown.classList.add('down'); crownStep(dir);
      holdT = setTimeout(() => { if (!crown.matches(':active')) return holdStop(); holdI = setInterval(() => { if (!crown.isConnected || !crown.matches(':active')) return holdStop(); crownStep(dir); }, 110); }, 450);
    });
    ['pointerup', 'pointercancel', 'lostpointercapture'].forEach((ev) => crown.addEventListener(ev, holdStop));
    window.addEventListener('pointerup', holdStop); window.addEventListener('blur', holdStop);
    crown.addEventListener('contextmenu', (e) => e.preventDefault());
    crown.addEventListener('wheel', (e) => { e.preventDefault(); crownStep(e.deltaY < 0 ? 1 : -1); }, { passive: false });
    side.addEventListener('pointerdown', (e) => { e.preventDefault(); side.classList.add('down'); startBtn.click(); snd.tick(true); });
    core.addEventListener('pointerdown', (e) => { e.preventDefault(); core.classList.add('down'); startBtn.click(); snd.tick(true); });
    const coreUp = () => core.classList.remove('down');
    core.addEventListener('pointerup', coreUp); core.addEventListener('pointercancel', coreUp); core.addEventListener('pointerleave', coreUp);
    const sideUp = () => side.classList.remove('down');
    side.addEventListener('pointerup', sideUp); side.addEventListener('pointercancel', sideUp); side.addEventListener('pointerleave', sideUp);
    paint();
    return wrap;
  }

  // ---- Calculator: expression display, % ( ) √ x² xʸ π sin cos tan log ln, keyboard, no eval ----
  function calcEval(src, deg) {
    const s = src.replace(/×/g, '*').replace(/÷/g, '/').replace(/−/g, '-').replace(/π/g, '(3.141592653589793)').replace(/√/g, 'sqrt').replace(/\s+/g, '');
    let i = 0;
    const open = (s.match(/\(/g) || []).length - (s.match(/\)/g) || []).length, t = s + ')'.repeat(Math.max(0, open));
    const peek = () => t[i];
    const num = () => { const m = /^(\d+\.?\d*|\.\d+)(e[+-]?\d+)?/i.exec(t.slice(i)); if (!m) throw new Error('num'); i += m[0].length; return parseFloat(m[0]); };
    const fn = { sin: (x) => Math.sin(deg ? x * Math.PI / 180 : x), cos: (x) => Math.cos(deg ? x * Math.PI / 180 : x), tan: (x) => Math.tan(deg ? x * Math.PI / 180 : x), log: Math.log10, ln: Math.log, sqrt: Math.sqrt };
    const expr = () => { let v = term(); while (peek() === '+' || peek() === '-') { const o = t[i++]; const r = term(); v = o === '+' ? v + r : v - r; } return v; };
    const term = () => {
      let v = factor();
      for (;;) {
        const c = peek();
        if (c === '*' || c === '/') { i++; const r = factor(); v = c === '*' ? v * r : v / r; }
        else if (c === '(' || /[a-z]/i.test(c || '')) { v *= factor(); } // 2(3) and 2sin(30)
        else break;
      }
      return v;
    };
    const factor = () => { const b = unary(); if (peek() === '^') { i++; return Math.pow(b, factor()); } return b; };
    const unary = () => { if (peek() === '-') { i++; return -unary(); } if (peek() === '+') { i++; return unary(); } return post(); };
    const post = () => { let v = primary(); while (peek() === '%') { i++; v /= 100; } return v; };
    const primary = () => {
      const c = peek();
      if (c === '(') { i++; const v = expr(); if (peek() !== ')') throw new Error('par'); i++; return v; }
      const m = /^[a-z]+/i.exec(t.slice(i));
      if (m) {
        const name = m[0].toLowerCase(); i += m[0].length;
        if (name === 'ans') return calcEval.ans || 0;
        if (!fn[name]) throw new Error('fn');
        if (peek() !== '(') throw new Error('par'); i++; const v = expr(); if (peek() !== ')') throw new Error('par'); i++; return fn[name](v);
      }
      return num();
    };
    const v = expr(); if (i < t.length) throw new Error('syntax');
    if (!Number.isFinite(v)) throw new Error('math');
    return v;
  }
  const calcFmt = (v) => { const r = Number(v.toPrecision(12)); const t = String(r); return t.length > 14 ? r.toExponential(6).replace(/\.?0+e/, 'e') : t; };

  // ---- Problem card (Tools → កាតលំហាត់): a card laid over the slide that the teacher writes a new problem on (group work, a quick
  // extra question ...). Type in the card; 👁 shows it typeset (maths goes between \( and \), e.g. \(x^2+3x=10\)); ⛶ makes it fill the slide.
  // The text is kept in this browser (localStorage), so the card is still there when the teacher comes back.
  // the cursor goes into the card as soon as it opens, so the teacher can type straight away
  function focusCard(f) {
    if (!f || f.hidden || !f.classList.contains('ts-wcard')) return;
    const t = f.querySelector('.cd-edit');
    if (t && !t.hidden) setTimeout(() => { try { t.focus({ preventScroll: true }); } catch (e) { t.focus(); } }, 0);
  }
  // header button 🃏: show / hide the card (kept in step with the Tools menu entry)
  function toggleCard() {
    const f = root && root.querySelector('.ts-float.ts-wcard');
    if (!f) return;
    f.hidden = !f.hidden;
    if (!f.hidden) stage.append(f);
    const mi = root.querySelector('.ts-tmenu button[data-w="wcard"]');
    if (mi) mi.classList.toggle('on', !f.hidden);
    focusCard(f);
  }

  function cardBox() {
    const mk = (tag, cls, txt) => { const e = document.createElement(tag); if (cls) e.className = cls; if (txt != null) e.textContent = txt; return e; };
    const KEY = 'ts_card_v1';
    let saved = {};
    try { saved = JSON.parse(localStorage.getItem(KEY) || '{}') || {}; } catch (e) { saved = {}; }
    const wrap = mk('div', 'cd');
    const title = mk('input', 'cd-title'); title.type = 'text'; title.placeholder = 'ចំណងជើង'; title.value = saved.t != null ? saved.t : 'លំហាត់ក្រុម';
    const edit = mk('textarea', 'cd-edit'); edit.placeholder = 'វាយលំហាត់នៅទីនេះ…   (គណិតសរសេរក្នុង \\( … \\) ឧ. \\(x^2+3x=10\\))'; edit.value = saved.b || '';
    const view = mk('div', 'cd-view'); view.hidden = true;
    let fs = saved.s || 34, showing = false;
    const apply = () => { edit.style.fontSize = view.style.fontSize = fs + 'px'; };
    const save = () => { try { localStorage.setItem(KEY, JSON.stringify({ t: title.value, b: edit.value, s: fs })); } catch (e) { /* storage blocked */ } };
    const esc = (t) => t.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    const bar = mk('div', 'cd-bar');
    const btn = (label, tip, fn) => { const b = mk('button', 'cd-btn', label); b.type = 'button'; b.title = tip; b.onclick = fn; return b; };
    const viewB = btn('👁 បង្ហាញ', 'បង្ហាញជាគណិត / កែប្រែ', () => {
      showing = !showing;
      if (showing) { view.innerHTML = esc(edit.value).replace(/\n/g, '<br>'); math(view); }
      edit.hidden = showing; view.hidden = !showing;
      viewB.textContent = showing ? '✎ កែ' : '👁 បង្ហាញ';
    });
    bar.append(
      btn('A−', 'អក្សរតូចជាង', () => { fs = Math.max(18, fs - 4); apply(); save(); }),
      btn('A+', 'អក្សរធំជាង', () => { fs = Math.min(110, fs + 4); apply(); save(); }),
      viewB,
      btn('⛶ ពេញ', 'ពេញស្លាយ / តូចវិញ', () => { const f = wrap.closest('.ts-float'); if (f) f.classList.toggle('full'); }),
      btn('🗑 សម្អាត', 'លុបអត្ថបទ', () => { edit.value = ''; view.innerHTML = ''; save(); edit.focus(); }),
    );
    title.addEventListener('input', save); edit.addEventListener('input', save);
    ['keydown', 'keyup', 'keypress'].forEach((t) => wrap.addEventListener(t, (e) => e.stopPropagation()));   // typing must not turn the slides (arrows, space, [ ]) or trigger shortcuts
    wrap.append(title, edit, view, bar);
    apply();
    return wrap;
  }

  // ---- who is teaching: <b data-ts="teacher"> / <b data-ts="class"> on the cover slide are filled in here ----
  let coverTeacher = null;                                   // null = not asked yet; '' = asked, nothing found
  function fillMeta(target) {
    const host = target || slideEl;
    if (!host) return;
    host.querySelectorAll('[data-ts]').forEach((el) => {
      const k = el.dataset.ts;
      el.textContent = k === 'class' ? (meta.cname || '—') : k === 'teacher' ? (meta.teacher || coverTeacher || '—') : '';
    });
  }
  function loadTeacher() {
    if (coverTeacher !== null || meta.teacher) return;
    coverTeacher = '';
    const get = (u) => fetch(u, { credentials: 'include' }).then((r) => (r.ok ? r.json() : null)).catch(() => null);
    get('/api/profile/paper').then((d) => {
      const fromProfile = d && d.profile && d.profile.teacher ? String(d.profile.teacher).replace(/^\s*បង្រៀនដោយ\s*/, '').trim() : '';
      if (fromProfile) return fromProfile;
      return get('/api/teacher/me').then((m) => (m && (m.display_name || m.username)) || '');
    }).then((name) => { coverTeacher = name || ''; fillMeta(); });
  }

  // a short key click for the calculator (synthesised, no audio file); silent when the site's sound is muted (km_snd_muted)
  let tickCtx = null;
  function calcTick() {
    try { if (localStorage.getItem('km_snd_muted') === '1') return; } catch (e) { /* storage blocked: play */ }
    const AC = window.AudioContext || window.webkitAudioContext;
    if (!AC) return;
    try {
      tickCtx = tickCtx || new AC();
      if (tickCtx.state === 'suspended') tickCtx.resume();
      const t = tickCtx.currentTime, o = tickCtx.createOscillator(), g = tickCtx.createGain();
      o.type = 'triangle';
      o.frequency.setValueAtTime(1500, t); o.frequency.exponentialRampToValueAtTime(700, t + 0.05);
      g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(0.22, t + 0.004); g.gain.exponentialRampToValueAtTime(0.0001, t + 0.07);
      o.connect(g); g.connect(tickCtx.destination);
      o.start(t); o.stop(t + 0.08);
    } catch (e) { /* no audio available */ }
  }

  function calcBox() {
    const wrap = document.createElement('div');
    wrap.className = 'cl'; wrap.tabIndex = 0;
    const exprEl = document.createElement('div'); exprEl.className = 'cl-expr';
    const resEl = document.createElement('div'); resEl.className = 'cl-res'; resEl.textContent = '0';
    const screen = document.createElement('div'); screen.className = 'cl-screen'; screen.append(exprEl, resEl);
    let ex = '', done = false, deg = true;
    const show = () => { exprEl.textContent = ex || ' '; };
    const live = () => { // result preview while typing
      if (!ex) { resEl.textContent = '0'; return; }
      try { resEl.textContent = calcFmt(calcEval(ex, deg)); resEl.classList.remove('err'); } catch { /* keep last result while the expression is unfinished */ }
    };
    const add = (tok) => {
      if (done) { ex = /^[+×÷−^%]/.test(tok) ? 'Ans' : ''; done = false; }
      ex += tok; show(); live();
    };
    const back = () => { if (done) { ex = ''; done = false; } ex = ex.replace(/(sin\(|cos\(|tan\(|log\(|ln\(|√\(|Ans|.)$/, ''); show(); live(); };
    const clear = () => { ex = ''; done = false; resEl.classList.remove('err'); resEl.textContent = '0'; show(); };
    const equals = () => {
      if (!ex) return;
      try { const v = calcEval(ex, deg); calcEval.ans = v; const txt = calcFmt(v); exprEl.textContent = ex + ' ='; resEl.textContent = txt; resEl.classList.remove('err'); ex = txt; done = true; }
      catch { resEl.textContent = 'កំហុស'; resEl.classList.add('err'); }
    };
    const neg = () => { if (done) done = false; ex = ex.startsWith('−') ? ex.slice(1) : '−' + ex; show(); live(); };
    const K = (label, fn, cls) => { const b = document.createElement('button'); b.type = 'button'; b.textContent = label; if (cls) b.className = cls; b.onclick = () => { fn(); wrap.focus(); }; return b; };
    const sci = document.createElement('div'); sci.className = 'cl-sci'; sci.hidden = true;
    [['sin', () => add('sin(')], ['cos', () => add('cos(')], ['tan', () => add('tan(')], ['log', () => add('log(')], ['ln', () => add('ln(')],
      ['(', () => add('(')], [')', () => add(')')], ['x²', () => add('^2')], ['xʸ', () => add('^')], ['π', () => add('π')], ['√', () => add('√(')], ['Ans', () => add('Ans')]].forEach(([l, f]) => sci.append(K(l, f)));
    const mode = document.createElement('div'); mode.className = 'cl-mode';
    const fx = K('fx', () => { sci.hidden = !sci.hidden; fx.classList.toggle('on', !sci.hidden); }, 'tg');
    const dg = K('DEG', () => { deg = !deg; dg.textContent = deg ? 'DEG' : 'RAD'; live(); }, 'tg'); dg.title = 'ដឺក្រេ / រ៉ាដ្យង់';
    mode.append(fx, dg);
    const pad = document.createElement('div'); pad.className = 'cl-pad';
    [['C', clear, 'fn'], ['⌫', back, 'fn'], ['%', () => add('%'), 'fn'], ['÷', () => add('÷'), 'op'],
      ['7', () => add('7')], ['8', () => add('8')], ['9', () => add('9')], ['×', () => add('×'), 'op'],
      ['4', () => add('4')], ['5', () => add('5')], ['6', () => add('6')], ['−', () => add('−'), 'op'],
      ['1', () => add('1')], ['2', () => add('2')], ['3', () => add('3')], ['+', () => add('+'), 'op'],
      ['±', neg, 'fn'], ['0', () => add('0')], ['.', () => add('.')], ['=', equals, 'eq']].forEach(([l, f, c]) => pad.append(K(l, f, c)));
    wrap.append(screen, mode, sci, pad);
    // keyboard (digits, + - * / ^ ( ) . % Enter Backspace Esc) while the calculator has focus
    wrap.addEventListener('keydown', (e) => {
      const k = e.key; let used = true;
      if (/^[0-9]$/.test(k)) add(k);
      else if (k === '.' || k === ',') add('.');
      else if (k === '+') add('+'); else if (k === '-') add('−'); else if (k === '*' || k === 'x') add('×'); else if (k === '/') add('÷');
      else if (k === '^') add('^'); else if (k === '(' || k === ')') add(k); else if (k === '%') add('%');
      else if (k === 'Enter' || k === '=') equals(); else if (k === 'Backspace') back(); else if (k === 'Escape' || k === 'Delete') clear();
      else used = false;
      if (used) { e.preventDefault(); e.stopPropagation(); }
    });
    return wrap;
  }

  function toolbar() {
    const bar = document.createElement('div');
    bar.className = 'ts-bar';
    const mk = (cls, lab, fn) => { const b = document.createElement('button'); b.type = 'button'; b.className = cls; b.textContent = lab; b.onclick = fn; return b; };
    const nav = document.createElement('div');
    nav.className = 'ts-nav';
    nav.append(
      mk('', '←', () => prevStep()),
      Object.assign(document.createElement('span'), { className: 'ts-page', textContent: '' }),
      mk('', '→', () => nextStep()),
    );
    const end = document.createElement('div');
    end.className = 'ts-wid';
    const dl = mk('ts-dl', '⬇', openExport); dl.title = 'ទាញយកស្លាយជា PDF ឬ PowerPoint (ទាំងមេរៀន ឬមួយផ្នែក)';
    end.append(toolsMenu(), dl, mk('ts-fs', '⛶', toggleFs), mk('ts-exit', '✕', close));
    bar.append(end);
    bar._nav = nav;   // the page / arrows sit in the bottom-right corner of the slide (added to the stage in open())
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
      toolSetter = setTool;
      tool = id; spot = null; laser = []; if (!lensPin) lensOff();
      ink.style.pointerEvents = id === 'none' ? 'none' : 'auto';
      ink.style.cursor = id === 'point' || id === 'gpen' ? 'crosshair' : id === 'erase' ? 'none' : id === 'laser' || id === 'zoom' || HAND_TOOLS.includes(id) ? 'none' : 'crosshair';
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
    colorSetter = (col) => { color = col; showDot(); const i = COLORS.indexOf(col); [...cw.children].forEach((x2, k) => x2.classList.toggle('on', k === i)); sw.style.background = col; };
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
    const bSpot = mkBtn('zoom', '<img class="mi" src="/img/magnifier.png" alt="" draggable="false">', 'ពង្រីក', () => setTool(tool === 'zoom' ? 'none' : 'zoom'));
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
    const bPdf = mkBtn('pdf', '<b class="pdfi">PDF</b>', 'PDF', savePdf);
    bPdf.title = 'រក្សាទុកស្លាយដែលបានសរសេរទាំងអស់ជា PDF មួយ';
    const bSave = mkBtn('save', '💾', 'រក្សាទុក', saveImage);
    bSave.title = 'រក្សាទុកជារូបភាព (PNG)';
    row.append(bMouse, bLaser, bDraw, bStamp, bSpot, bErase, bFmt, tipWrap, bUndo, bRedo, bClear, bSave, bPdf);
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
  // ---- Tools drop-down in the header: Spin, Timer, Calculator, Geometry ----
  const TOOL_ITEMS = [
    ['wspin', '🎡', 'Spin', 'កង់ចាប់ឈ្មោះ'],
    ['wtime', '⏱', 'Timer', 'ម៉ោង'],
    ['wcalc', '∑', 'Calculator', 'ម៉ាស៊ីនគិតលេខ'],
    ['wcard', '🃏', 'Problem card', 'កាតលំហាត់'],
    ['wgeo', '📐', 'Geometry', 'ឧបករណ៍ធរណីមាត្រ'],
  ];
  function toolsMenu() {
    const wrap = document.createElement('div');
    wrap.className = 'ts-tools';
    const btn = document.createElement('button');
    btn.type = 'button'; btn.className = 'ts-tbtn'; btn.innerHTML = '🧰 Tools <em>▾</em>';
    const menu = document.createElement('div');
    menu.className = 'ts-tmenu'; menu.hidden = true;
    TOOL_ITEMS.forEach(([cls, ic, en, km]) => {
      const it = document.createElement('button');
      it.type = 'button'; it.dataset.w = cls;
      it.innerHTML = `<span class="ti">${ic}</span><span class="tt"><b>${en}</b><small>${km}</small></span><i class="tick">✓</i>`;
      it.onclick = (ev) => {
        ev.stopPropagation();
        const f = root.querySelector('.ts-float.ts-' + cls);
        if (f) { f.hidden = !f.hidden; if (!f.hidden) stage.append(f); it.classList.toggle('on', !f.hidden); focusCard(f); }
        menu.hidden = true;
      };
      menu.append(it);
    });
    btn.onclick = (ev) => {
      ev.stopPropagation();
      menu.querySelectorAll('[data-w]').forEach((x) => { const f = root.querySelector('.ts-float.ts-' + x.dataset.w); x.classList.toggle('on', !!f && !f.hidden); });
      menu.hidden = !menu.hidden;
    };
    const away = (ev) => { if (!wrap.contains(ev.target)) menu.hidden = true; };
    document.addEventListener('pointerdown', away);
    offTools = () => document.removeEventListener('pointerdown', away);
    wrap.append(btn, menu);
    return wrap;
  }

  // ---- Geometry: ruler, protractor and set squares that you can drag and turn ----
  const CM = 37.8; // px per cm
  function instSVG(kind) {
    const ns = 'http://www.w3.org/2000/svg';
    let w, h, body = '', edges = [];
    if (kind === 'ruler') {
      w = Math.round(CM * 15 + 24); h = 66;
      body += `<rect x="1" y="1" width="${w - 2}" height="${h - 2}" rx="6" fill="rgba(255,236,160,.93)" stroke="#a88a2a" stroke-width="2"/>`;
      for (let mm = 0; mm <= 150; mm++) {
        const x = 12 + mm * CM / 10, len = mm % 10 === 0 ? 22 : mm % 5 === 0 ? 15 : 9;
        body += `<line x1="${x}" y1="2" x2="${x}" y2="${2 + len}" stroke="#5a4a10" stroke-width="${mm % 10 === 0 ? 1.6 : 1}"/>`;
        if (mm % 10 === 0) body += `<text x="${x}" y="40" font-size="14" font-weight="700" text-anchor="middle" fill="#3b300a">${mm / 10}</text>`;
      }
      body += `<text x="${w - 30}" y="58" font-size="12" fill="#5a4a10">cm</text>`;
      edges = [[[0, 1], [w, 1]]];
    } else if (kind === 'protractor') {
      const R = 190; w = R * 2 + 20; h = R + 34;
      const cx = w / 2, cy = R + 12;
      body += `<path d="M${cx - R} ${cy} A${R} ${R} 0 0 1 ${cx + R} ${cy} Z" fill="rgba(170,215,255,.55)" stroke="#2b6aa6" stroke-width="2"/>`;
      body += `<path d="M${cx - R * .55} ${cy} A${R * .55} ${R * .55} 0 0 1 ${cx + R * .55} ${cy}" fill="none" stroke="#2b6aa6" stroke-width="1"/>`;
      for (let d = 0; d <= 180; d++) {
        const a = Math.PI - d * Math.PI / 180, big = d % 10 === 0, mid = d % 5 === 0, L = big ? 22 : mid ? 15 : 9;
        const x1 = cx + R * Math.cos(a), y1 = cy - R * Math.sin(a), x2 = cx + (R - L) * Math.cos(a), y2 = cy - (R - L) * Math.sin(a);
        body += `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="#14406b" stroke-width="${big ? 1.5 : .8}"/>`;
        if (big) {
          const tx = cx + (R - 36) * Math.cos(a), ty = cy - (R - 36) * Math.sin(a);
          body += `<text x="${tx}" y="${ty + 4}" font-size="11" font-weight="700" text-anchor="middle" fill="#14406b">${d}</text>`;
          const ux = cx + (R * .55 - 14) * Math.cos(a), uy = cy - (R * .55 - 14) * Math.sin(a);
          body += `<text x="${ux}" y="${uy + 3}" font-size="9" text-anchor="middle" fill="#2b6aa6">${180 - d}</text>`;
        }
      }
      body += `<line x1="${cx - 14}" y1="${cy}" x2="${cx + 14}" y2="${cy}" stroke="#c0392b" stroke-width="2"/><line x1="${cx}" y1="${cy - 14}" x2="${cx}" y2="${cy}" stroke="#c0392b" stroke-width="2"/>`;
      edges = [[[cx - R, cy], [cx + R, cy]]];
    } else {
      const a = kind === 'set45' ? 300 : 210, b = kind === 'set45' ? 300 : 364; // legs
      w = a + 20; h = b + 20;
      edges = [[[10, h - 10], [10 + a, h - 10]], [[10, h - 10], [10, h - 10 - b]], [[10 + a, h - 10], [10, h - 10 - b]]];
      body += `<polygon points="10,${h - 10} ${10 + a},${h - 10} 10,${h - 10 - b}" fill="rgba(160,235,185,.6)" stroke="#2e8b57" stroke-width="2.2" stroke-linejoin="round"/>`;
      const ix = 52, iy = kind === 'set45' ? 52 : 70, iw = a - 110, ih = b - 130;
      if (kind === 'set45') body += `<polygon points="${ix},${h - 10 - iy} ${ix + iw * .55},${h - 10 - iy} ${ix},${h - 10 - iy - iw * .55}" fill="rgba(255,255,255,.7)" stroke="#2e8b57"/>`;
      else body += `<polygon points="${ix},${h - 10 - iy} ${ix + iw * .5},${h - 10 - iy} ${ix},${h - 10 - iy - ih * .6}" fill="rgba(255,255,255,.7)" stroke="#2e8b57"/>`;
      for (let mm = 0; mm <= (a - 20) / (CM / 10); mm++) { // cm scale along the base
        const x = 10 + mm * CM / 10, L = mm % 10 === 0 ? 14 : mm % 5 === 0 ? 10 : 6;
        body += `<line x1="${x}" y1="${h - 10}" x2="${x}" y2="${h - 10 - L}" stroke="#1f5e3c" stroke-width="1"/>`;
        if (mm % 10 === 0 && mm) body += `<text x="${x}" y="${h - 28}" font-size="11" text-anchor="middle" fill="#1f5e3c">${mm / 10}</text>`;
      }
      body += `<text x="${kind === 'set45' ? 24 : 24}" y="${h - 18}" font-size="11" fill="#1f5e3c">90°</text>`;
    }
    const svg = document.createElementNS(ns, 'svg');
    svg.setAttribute('viewBox', `0 0 ${w} ${h}`); svg.setAttribute('width', w); svg.setAttribute('height', h);
    svg.innerHTML = body;
    return { svg, w, h, edges };
  }

  function addInstrument(kind) {
    const { svg, w, h, edges } = instSVG(kind);
    const el = document.createElement('div');
    el.className = 'ts-inst';
    el.style.width = w + 'px'; el.style.height = h + 'px';
    el.append(svg);
    const hb = (cls, txt, title) => { const b = document.createElement('button'); b.type = 'button'; b.className = cls; b.textContent = txt; b.title = title; return b; };
    const rot = hb('ts-irot', '↻', 'បង្វិល'), x = hb('ts-ix', '✕', 'ដកចេញ'), mv = hb('ts-imv', '✥', 'អូសដើម្បីផ្លាស់ទី'), sc = hb('ts-isc', '⤡', 'អូសដើម្បីពង្រីក / បង្រួម'), ed = hb('ts-ied', '✎', 'គូសបន្ទាត់តាមគែម');
    el.append(rot, x, mv, sc, ed);
    let px = Math.max(10, (stage.clientWidth - w) / 2 - 80 + Math.random() * 40), py = Math.max(10, (stage.clientHeight - h) / 2 + Math.random() * 40), ang = 0, zoom = 1, edgeMode = false;
    const apply = () => { el.style.left = px + 'px'; el.style.top = py + 'px'; el.style.transform = `rotate(${ang}deg) scale(${zoom})`; el.style.setProperty('--inv', String(1 / zoom)); };
    apply();
    stage.append(el);
    x.onclick = () => el.remove();
    ed.onclick = (ev) => { ev.stopPropagation(); edgeMode = !edgeMode; el.classList.toggle('edge', edgeMode); };
    // local <-> stage coordinates of this (turned, scaled) instrument
    const centre = () => ({ x: px + w / 2, y: py + h / 2 });
    const toWorld = (lx, ly) => { const c = centre(), r = ang * Math.PI / 180, dx = (lx - w / 2) * zoom, dy = (ly - h / 2) * zoom; return { x: c.x + dx * Math.cos(r) - dy * Math.sin(r), y: c.y + dx * Math.sin(r) + dy * Math.cos(r) }; };
    const toLocal = (wx, wy) => { const c = centre(), r = -ang * Math.PI / 180, ux = wx - c.x, uy = wy - c.y; return [(ux * Math.cos(r) - uy * Math.sin(r)) / zoom + w / 2, (ux * Math.sin(r) + uy * Math.cos(r)) / zoom + h / 2]; };
    const proj = (edge, lx, ly) => { const [[ax, ay], [bx2, by2]] = edge, dx = bx2 - ax, dy = by2 - ay; return Math.max(0, Math.min(1, ((lx - ax) * dx + (ly - ay) * dy) / (dx * dx + dy * dy))); };
    const edgeDist = (edge, lx, ly) => { const t = proj(edge, lx, ly), [[ax, ay], [bx2, by2]] = edge; return Math.hypot(lx - (ax + t * (bx2 - ax)), ly - (ay + t * (by2 - ay))); };
    const stageXY = (e) => { const r = ink.getBoundingClientRect(); return [e.clientX - r.left, e.clientY - r.top]; };
    let mode = null, sx = 0, sy = 0, bx = 0, by = 0, a0 = 0, g0 = 0, cxp = 0, cyp = 0, d0 = 1, z0 = 1, edge = null, t0 = 0;
    const penTool = () => HAND_TOOLS.includes(tool) || tool === 'gpen' || tool === 'point';
    const isProt = kind === 'protractor', PR = 190, pcx = w / 2, pcy = PR + 12; // protractor centre (local)
    const badge = document.createElement('div'); badge.className = 'ts-ibadge'; badge.hidden = true; el.append(badge);
    el.addEventListener('pointerdown', (e) => {
      if (e.target === x || e.target === ed) return;
      el.setPointerCapture(e.pointerId);
      stage.append(el); // bring to front
      const [wx, wy] = stageXY(e), [lx, ly] = toLocal(wx, wy), draw = edgeMode || penTool();
      const handle = e.target === rot || e.target === sc || e.target === mv;
      const near = draw && !handle && edges.slice().sort((p, q) => edgeDist(p, lx, ly) - edgeDist(q, lx, ly))[0];
      if (e.target === rot) {
        mode = 'rot';
        const r = el.getBoundingClientRect(); cxp = r.left + r.width / 2; cyp = r.top + r.height / 2;
        a0 = Math.atan2(e.clientY - cyp, e.clientX - cxp); g0 = ang;
      } else if (e.target === sc) {
        mode = 'scale';
        const r = el.getBoundingClientRect(); cxp = r.left + r.width / 2; cyp = r.top + r.height / 2;
        d0 = Math.hypot(e.clientX - cxp, e.clientY - cyp) || 1; z0 = zoom;
      } else if (isProt && draw && !handle && Math.hypot(lx - pcx, ly - pcy) > 26 && ly < pcy - 8 && Math.hypot(lx - pcx, ly - pcy) < PR + 6) {
        mode = 'ray'; // a ray from the protractor centre; its angle is written on the slide
      } else if (near && (edgeMode || edgeDist(near, lx, ly) <= 20 / zoom)) {
        edge = near; t0 = proj(edge, lx, ly); mode = 'edge';
      } else { mode = 'move'; sx = e.clientX; sy = e.clientY; bx = px; by = py; }
      e.preventDefault();
    });
    el.addEventListener('pointermove', (e) => {
      if (!mode) { // protractor: show the angle under the pointer
        if (isProt && e.target !== rot && e.target !== x) {
          const [wx, wy] = stageXY(e), [lx, ly] = toLocal(wx, wy), dx = lx - pcx, dy = pcy - ly;
          if (dy > 4 && Math.hypot(dx, dy) < PR) { badge.hidden = false; badge.textContent = Math.round(180 - Math.atan2(dy, dx) * 180 / Math.PI) + '°'; badge.style.left = lx + 'px'; badge.style.top = (ly - 26) + 'px'; badge.style.transform = `translate(-50%,-50%) rotate(${-ang}deg) scale(${1 / zoom})`; } else badge.hidden = true;
        }
        return;
      }
      if (mode === 'move') { px = bx + e.clientX - sx; py = by + e.clientY - sy; apply(); }
      else if (mode === 'rot') { ang = g0 + (Math.atan2(e.clientY - cyp, e.clientX - cxp) - a0) * 180 / Math.PI; if (e.shiftKey) ang = Math.round(ang / 15) * 15; apply(); }
      else if (mode === 'scale') { zoom = Math.max(.4, Math.min(2.6, z0 * (Math.hypot(e.clientX - cxp, e.clientY - cyp) / d0))); apply(); }
      else if (mode === 'ray') {
        const [wx, wy] = stageXY(e), [lx, ly] = toLocal(wx, wy);
        let ux = lx - pcx, uy = ly - pcy; const L = Math.hypot(ux, uy) || 1; ux /= L; uy /= L;
        if (uy > -0.02) uy = -0.02;
        const len = PR, phi = Math.atan2(-uy, ux), deg = 180 - phi * 180 / Math.PI;
        const A = toWorld(pcx, pcy), B = toWorld(pcx + ux * len, pcy + uy * len), Lb = toWorld(pcx + ux * (len + 26 / zoom), pcy + uy * (len + 26 / zoom));
        cur = { t: 'line', c: geoColor, w: geoSize, p: [A, B], label: { text: Math.round(deg) + '°', x: Lb.x, y: Lb.y } }; redraw();
      } else if (mode === 'edge') { // a straight line along the edge, from where you pressed to where you are
        const [wx, wy] = stageXY(e), [lx, ly] = toLocal(wx, wy), t1 = proj(edge, lx, ly), [[ax, ay], [bx2, by2]] = edge;
        // the pen sits just outside the instrument's edge, so the line stays visible next to it
        let nx = -(by2 - ay), ny = bx2 - ax; const nl = Math.hypot(nx, ny) || 1; nx /= nl; ny /= nl;
        if (nx * ((ax + bx2) / 2 - w / 2) + ny * ((ay + by2) / 2 - h / 2) < 0) { nx = -nx; ny = -ny; }
        const off = (geoSize / 2 + 1.5) / zoom, ox = nx * off, oy = ny * off;
        const A = toWorld(ax + t0 * (bx2 - ax) + ox, ay + t0 * (by2 - ay) + oy), B = toWorld(ax + t1 * (bx2 - ax) + ox, ay + t1 * (by2 - ay) + oy);
        const lenCm = Math.hypot(B.x - A.x, B.y - A.y) / (CM * zoom), mid = toWorld(ax + (t0 + t1) / 2 * (bx2 - ax) + nx * (off + 24 / zoom), ay + (t0 + t1) / 2 * (by2 - ay) + ny * (off + 24 / zoom));
        cur = { t: 'line', c: geoColor, w: geoSize, p: [A, B], label: { text: lenCm.toFixed(1) + ' cm', x: mid.x, y: mid.y } }; redraw();
      }
    });
    const up = () => {
      if ((mode === 'edge' || mode === 'ray') && cur && cur.t === 'line') {
        if (Math.hypot(cur.p[1].x - cur.p[0].x, cur.p[1].y - cur.p[0].y) > 3) { strokes.push(cur); undoS.push({ add: cur }); redoS = []; syncUndo(); }
        cur = null; redraw();
      }
      mode = null;
    };
    el.addEventListener('pointerup', up); el.addEventListener('pointercancel', up);
    el.addEventListener('pointerleave', () => { badge.hidden = true; });
    el.addEventListener('wheel', (e) => { e.preventDefault(); if (e.ctrlKey) { zoom = Math.max(.4, Math.min(2.6, zoom * (e.deltaY < 0 ? 1.06 : .94))); } else { ang += (e.deltaY < 0 ? 1 : -1) * (e.shiftKey ? 5 : 1); } apply(); }, { passive: false });
    return el;
  }

  // Compass (ដែកឈាន): move the needle, set the radius, drag the pencil to draw an arc or a circle
  function addCompass() {
    const o = document.createElement('div'); o.className = 'ts-cmp';
    const ns = 'http://www.w3.org/2000/svg', svg = document.createElementNS(ns, 'svg');
    svg.setAttribute('width', '100%'); svg.setAttribute('height', '100%'); o.append(svg);
    const mk = (cls, t, title) => { const b = document.createElement('button'); b.type = 'button'; b.className = 'ts-ch ' + cls; b.textContent = t; b.title = title; o.append(b); return b; };
    const bP = mk('p', '✥', 'អូសដើម្បីផ្លាស់ទី (ម្ជុល)'), bQ = mk('q', '✎', 'អូសដើម្បីគូសធ្នូ ឬរង្វង់'), bH = mk('h', '↔', 'អូសដើម្បីកែកាំ'), bX = mk('x', '✕', 'ដកចេញ');
    let P = { x: Math.max(180, stage.clientWidth * 0.34), y: stage.clientHeight * 0.62 }, r = 150, phi = -0.45;
    const geo = () => {
      const Q = { x: P.x + r * Math.cos(phi), y: P.y + r * Math.sin(phi) }, leg = r * 0.75 + 120, hgt = Math.sqrt(Math.max(1, leg * leg - (r / 2) * (r / 2)));
      let nx = -Math.sin(phi), ny = Math.cos(phi); if (ny > 0) { nx = -nx; ny = -ny; }
      return { Q, H: { x: (P.x + Q.x) / 2 + nx * hgt, y: (P.y + Q.y) / 2 + ny * hgt } };
    };
    const place = (b, pt) => { b.style.left = pt.x + 'px'; b.style.top = pt.y + 'px'; };
    const paintC = () => {
      const { Q, H } = geo(), cm = (r / CM).toFixed(1);
      svg.innerHTML = `<line x1="${P.x}" y1="${P.y}" x2="${H.x}" y2="${H.y}" stroke="#8a97a6" stroke-width="9" stroke-linecap="round"/><line x1="${Q.x}" y1="${Q.y}" x2="${H.x}" y2="${H.y}" stroke="#8a97a6" stroke-width="9" stroke-linecap="round"/>
        <line x1="${P.x}" y1="${P.y}" x2="${P.x + (H.x - P.x) * .12}" y2="${P.y + (H.y - P.y) * .12}" stroke="#444" stroke-width="3" stroke-linecap="round"/>
        <line x1="${Q.x}" y1="${Q.y}" x2="${Q.x + (H.x - Q.x) * .12}" y2="${Q.y + (H.y - Q.y) * .12}" stroke="${geoColor}" stroke-width="5" stroke-linecap="round"/>
        <circle cx="${H.x}" cy="${H.y}" r="12" fill="#2b73a3" stroke="#fff" stroke-width="3"/><circle cx="${P.x}" cy="${P.y}" r="4" fill="#222"/>
        <text x="${(P.x + Q.x) / 2}" y="${(P.y + Q.y) / 2 - 12}" text-anchor="middle" font-size="18" font-weight="700" fill="#0f5173" stroke="#fff" stroke-width="4" paint-order="stroke">r = ${cm} cm</text>`;
      place(bP, P); place(bQ, Q); place(bH, H); place(bX, { x: H.x + 26, y: H.y - 26 });
    };
    const xy = (e) => { const b = ink.getBoundingClientRect(); return { x: e.clientX - b.left, y: e.clientY - b.top }; };
    const grab = (btn, start, move, end) => {
      btn.addEventListener('pointerdown', (e) => { btn.setPointerCapture(e.pointerId); stage.append(o); start(e); btn._on = true; e.preventDefault(); });
      btn.addEventListener('pointermove', (e) => { if (btn._on) { if (e.buttons === 0) { btn._on = false; end && end(); return; } move(e); } });
      const stop = () => { if (btn._on) { btn._on = false; end && end(); } };
      btn.addEventListener('pointerup', stop); btn.addEventListener('pointercancel', stop); btn.addEventListener('lostpointercapture', stop);
    };
    let off = { x: 0, y: 0 };
    grab(bP, (e) => { const p = xy(e); off = { x: p.x - P.x, y: p.y - P.y }; }, (e) => { const p = xy(e); P = { x: p.x - off.x, y: p.y - off.y }; paintC(); });
    grab(bH, () => {}, (e) => { const p = xy(e); r = Math.max(30, Math.min(700, 2 * ((p.x - P.x) * Math.cos(phi) + (p.y - P.y) * Math.sin(phi)))); paintC(); });
    let lastPhi = 0;
    grab(bQ, () => { lastPhi = phi; cur = { t: 'pen', c: geoColor, w: geoSize, k: 'ball', p: [geo().Q] }; redraw(); }, (e) => {
      const p = xy(e), target = Math.atan2(p.y - P.y, p.x - P.x);
      let d = target - lastPhi; while (d > Math.PI) d -= 2 * Math.PI; while (d < -Math.PI) d += 2 * Math.PI;
      const n = Math.max(1, Math.ceil(Math.abs(d) / 0.04));
      for (let k = 1; k <= n; k++) { const ph = lastPhi + d * k / n; cur.p.push({ x: P.x + r * Math.cos(ph), y: P.y + r * Math.sin(ph), t: performance.now() }); }
      lastPhi = lastPhi + d; phi = lastPhi; paintC(); redraw();
    }, () => { if (cur && cur.t === 'pen') { if (cur.p.length > 2) { strokes.push(cur); undoS.push({ add: cur }); redoS = []; syncUndo(); } cur = null; redraw(); } });
    bX.onclick = () => o.remove();
    stage.append(o); paintC();
    return o;
  }

  function geoBox() {
    const box = document.createElement('div');
    box.className = 'ts-geo';
    const pen = document.createElement('div'); pen.className = 'gpen';
    const lab = document.createElement('div'); lab.className = 'gl'; lab.textContent = 'ប៊ិចធរណីមាត្រ (ដាច់ពីប៊ិចសរសេរ)';
    const tb = (txt, tl, id) => { const b = document.createElement('button'); b.type = 'button'; b.className = 'gt'; b.dataset.t = id; b.textContent = txt; b.title = tl; b.onclick = () => { if (toolSetter) toolSetter(tool === id ? 'none' : id); sync(); }; return b; };
    const penB = tb('✎ ប៊ិចគូស', 'ប៊ិចស្តើងសម្រាប់គូសរូបធរណីមាត្រ (មានពណ៌ និងទំហំផ្ទាល់ខ្លួន)', 'gpen'), ptB = tb('● ចំណុច A B C', 'ដាក់ចំណុចមានអក្សរ A B C', 'point');
    const sync = () => { [penB, ptB].forEach((b) => b.classList.toggle('on', tool === b.dataset.t)); };
    box.addEventListener('pointerenter', sync);
    const cr = document.createElement('div'); cr.className = 'gcol';
    const GC = ['#212529', '#e03131', '#1c7ed6', '#2f9e44', '#f08c00', '#ae3ec9'];
    GC.forEach((c) => { const b = document.createElement('button'); b.type = 'button'; b.className = 'gc' + (c === geoColor ? ' on' : ''); b.style.background = c; b.title = c; b.onclick = () => { geoColor = c; cr.querySelectorAll('.gc').forEach((x2) => x2.classList.toggle('on', x2 === b)); if (tool === 'none' && toolSetter) toolSetter('gpen'); sync(); }; cr.append(b); });
    const sr = document.createElement('input'); sr.type = 'range'; sr.min = 1; sr.max = 10; sr.value = geoSize; sr.title = 'ទំហំប៊ិចធរណីមាត្រ'; sr.oninput = () => { geoSize = +sr.value; };
    pen.append(lab, penB, ptB, cr, sr);
    box.append(pen);
    box.insertAdjacentHTML('beforeend', '<p class="gh">ចុចឧបករណ៍ដើម្បីដាក់លើស្លាយ · ✥ ផ្លាស់ទី · ↻ បង្វិល · ⤡ ពង្រីក · ជ្រើសប៊ិច ហើយអូសតាមគែមឧបករណ៍ដើម្បីគូសត្រង់ និងបង្ហាញប្រវែង · លើម៉ែត្រមុំ៖ អូសដើម្បីគូសកាំរស្មី និងបង្ហាញមុំ</p>');
    [['ruler', '📏', 'Ruler', 'បន្ទាត់'], ['protractor', '◠', 'Protractor', 'ម៉ែត្រមុំ'], ['compass', '◔', 'Compass', 'ដែកឈាន'], ['set45', '◣', 'Set square 45°', 'ក្រដាសត្រីកោណ 45°'], ['set60', '◺', 'Set square 30°–60°', 'ក្រដាសត្រីកោណ 30°–60°']].forEach(([k, ic, en, km]) => {
      const b = document.createElement('button'); b.type = 'button';
      b.innerHTML = `<span class="gi">${ic}</span><span><b>${en}</b><small>${km}</small></span>`;
      b.onclick = () => { if (tool === 'none' && toolSetter) toolSetter('gpen'); (k === 'compass' ? addCompass : addInstrument)(k); };
      box.append(b);
    });
    const clr = document.createElement('button'); clr.type = 'button'; clr.className = 'gclr';
    clr.textContent = 'ដកឧបករណ៍ទាំងអស់ចេញ';
    clr.onclick = () => stage.querySelectorAll('.ts-inst, .ts-cmp').forEach((n) => n.remove());
    box.append(clr);
    return box;
  }

  // ---- lesson looks: a lesson listed here is shown in the "purple" look of the teacher's own decks (cream card on a lavender band, blue
  // headings, blue outlined boxes) and gets a branded cover slide in front of the lesson's own slides. To give another lesson the same
  // look, add it here ("grade-lesson": { name, en: English subtitle for the cover }).
  // (Lesson 2 tried this look and went back to the Lesson 1 design, so nothing uses it right now.)
  const LESSON_THEMES = {};
  // lessons whose generated deck gets the same first slide as Lesson 1: the school (logo, name), the teacher, the class, the school year.
  // The lesson's own cover (title + objectives) then comes second, exactly like Lesson 1. Add "grade-lesson" keys to give more lessons this.
  const BRANDED_LESSONS = new Set(['7-2', '7-3', '7-12', '9-1']);
  const BIG_TEXT_LESSONS = new Set(['9-1']);   // decks checked for overflow at the larger projector text size
  let BIG_TEXT = false;
  function brandSlide() {
    return {
      k: 'title', c: 'brand',
      html: '<img class="bd-logo" src="/ngs.png" alt="">'
        + '<div class="bd-name">វិទ្យាល័យព្រះស៊ីសុវត្ថិ</div><div class="bd-sub">(សាលារៀនជំនាន់ថ្មី)</div>'
        + '<div class="bd-info"><div><small>គ្រូបង្រៀន</small><b data-ts="teacher"></b></div>'
        + '<div><small>ថ្នាក់</small><b data-ts="class"></b></div><div><small>ឆ្នាំសិក្សា</small><b>២០២៦-២០២៧</b></div></div>',
    };
  }
  let themeCls = '';                                          // 'ts-theme-purple' while a themed lesson is open
  function purpleCover(theme, opt) {
    const star = (x, y, s, c) => `<path d="M${x} ${y - s} Q${x} ${y} ${x + s} ${y} Q${x} ${y} ${x} ${y + s} Q${x} ${y} ${x - s} ${y} Q${x} ${y} ${x} ${y - s}Z" fill="${c}"/>`;
    const deco = '<svg class="pp-deco" viewBox="0 0 1000 560" aria-hidden="true">'
      + star(900, 110, 26, '#ffd84a') + star(955, 205, 14, '#ffd84a') + star(70, 440, 22, '#ffd84a') + star(150, 90, 16, '#9b72c0')
      + star(520, 505, 18, '#9b72c0') + star(880, 470, 24, '#9b72c0')
      + '<g fill="none" stroke="#9b72c0" stroke-width="5" stroke-linecap="round"><path d="M330 120 l34 14"/><path d="M326 150 l38 -4"/><path d="M700 130 l36 -12"/></g>'
      + '<g font-family="Times New Roman,serif" font-weight="700" fill="#9b72c0" opacity=".55" font-size="64"><text x="60" y="190">÷</text><text x="885" y="330">√</text><text x="120" y="330">×</text></g></svg>';
    const html = deco
      + '<div class="pp-top"><img class="pp-logo" src="/ngs.png" alt=""><div class="pp-school">វិទ្យាល័យព្រះស៊ីសុវត្ថិ<br><span>សាលារៀនជំនាន់ថ្មី</span></div></div>'
      + `<div class="pp-pill">Grade ${opt.grade}</div>`
      + `<div class="pp-title">${opt.title || ''}</div>`
      + `<div class="pp-en">${theme.en || ''}</div>`
      + '<div class="pp-by">បង្រៀនដោយ : <b data-ts="teacher"></b></div>'
      + '<div class="pp-meta">ថ្នាក់ <b data-ts="class"></b> &nbsp;·&nbsp; ឆ្នាំសិក្សា <b>២០២៦-២០២៧</b></div>';
    return { k: 'title', c: 'pp-cover', html };
  }

  function open(opt) {
    slides = ((window.TEACH_SLIDES && window.TEACH_SLIDES[`${opt.grade}-${opt.lesson}`]) || []).map((x) => ({ ...x }));
    strokes = []; undoS = []; redoS = []; cur = null; i = 0; slideEl = null;
    if (!slides.length) return Exam.notify('មិនទាន់មានស្លាយ។');
    const lessonKey = `${opt.grade}-${opt.lesson}`;
    BIG_TEXT = BIG_TEXT_LESSONS.has(lessonKey);
    const theme = LESSON_THEMES[lessonKey] || null, branded = BRANDED_LESSONS.has(lessonKey);
    const pre = (theme ? 1 : 0) + (branded ? 1 : 0);                // pre = slides added in front of the lesson's own slides
    themeCls = theme ? `ts-theme-${theme.name}` : '';
    if (branded) slides.unshift(brandSlide());
    if (theme) slides.unshift(purpleCover(theme, opt));
    students = (opt.students || []).map((s) => `${s.surname || ''} ${s.first_name || ''}`.trim()).filter(Boolean);
    close();
    tool = 'none'; // always start as the plain mouse; pick a pen when you want to write
    meta = { grade: opt.grade, lesson: opt.lesson, cname: opt.className || '', teacher: opt.teacher || '' };
    loadTeacher();
    root = document.getElementById('teach-show');
    root.hidden = false;
    root.innerHTML = '';
    document.body.classList.add('teach-show-on');
    const tbar = toolbar();
    root.append(tbar);
    stage = document.createElement('div');
    stage.className = 'ts-stage' + (themeCls ? ` ${themeCls}` : '');
    slideEl = document.createElement('div');
    slideEl.className = 'ts-slide';
    ink = document.createElement('canvas');
    ink.className = 'ts-ink';
    const wm = document.createElement('div'); wm.className = 'ts-wm'; wm.textContent = 'khmermath.org';   // site label, bottom-left of every slide
    stage.append(slideEl, ink, wm, tbar._nav);
    root.append(stage);
    const names = students.length ? students : ['សិស្ស ក', 'សិស្ស ខ', 'សិស្ស គ'];
    { // Spin starts about a quarter of the slide in size, in the top-right corner
      const sw = stage.clientWidth, sh = stage.clientHeight, w = Math.round(Math.min(Math.max(sw * 0.3, 340), 480)), h = Math.round(Math.min(sh - 16, w * 1.12));
      makeFloat('wspin', 'Spin' + (meta.cname ? ' · ' + meta.cname : ''), miniSpin(students, meta.cname), { x: (sw - w - 10) + 'px', y: '8px', w: w + 'px', h: h + 'px' }).hidden = true;
    }
    makeFloat('wtime', 'Timer', timerBox(), { x: '64%', y: '3%', w: '300px' }).hidden = true;
    { const calc = makeFloat('wcalc', 'Calculator', calcBox(), { x: '30%', y: '8%', w: '300px', autoh: true, inside: true }); calc.hidden = true; drag(calc, calc, true); calc.addEventListener('pointerdown', (e) => { if (e.target.closest('.cl button')) calcTick(); }); calc.addEventListener('keydown', (e) => { if (e.key.length === 1 || ['Enter', 'Backspace', 'Delete'].includes(e.key)) calcTick(); }); }   // grab the slim header or any part of the body that is not a key; every key click ticks
    makeFloat('wcard', 'កាតលំហាត់', cardBox(), { x: '7%', y: '8%', w: '86%', h: '76%', inside: true }).hidden = true;
    makeFloat('wgeo', 'Geometry', geoBox(), { x: '62%', y: '6%', w: '300px' }).hidden = true;
    // small clock in the right corner: click to hide, click to show
    {
      const ck = document.createElement('button'); ck.type = 'button'; ck.className = 'ts-clock'; ck.title = 'ចុចដើម្បីលាក់ / បង្ហាញម៉ោង';
      let shown = true; try { shown = localStorage.getItem('ts_clock') !== '0'; } catch { /* default shown */ }
      const tick = () => { const d = new Date(), h = d.getHours() % 12 || 12, ap = d.getHours() < 12 ? 'AM' : 'PM'; ck.innerHTML = shown ? `<b>${h}:${String(d.getMinutes()).padStart(2, '0')}</b><i>${ap}</i>` : '<span>🕒</span>'; ck.classList.toggle('off', !shown); };
      ck.onclick = () => { shown = !shown; try { localStorage.setItem('ts_clock', shown ? '1' : '0'); } catch { /* ignore */ } tick(); };
      tick(); clearInterval(clockT); clockT = setInterval(tick, 5000);
      tbar.prepend(ck);   // the clock lives in the header bar, top-left
    }
    ctx = ink.getContext('2d', { desynchronized: true });   // lower latency for the pen where the browser supports it
    bindInk();
    penPalette();
    requestAnimationFrame(() => { fitInk(); show(opt.start ? opt.start + pre : 0); });   // opt.start counts the lesson's own slides, so skip the cover we put in front
    window.addEventListener('resize', onResize);
    window.addEventListener('keydown', keys);
  }

  function onResize() { const keep = stepNow; fitInk(); show(i); stepNow = Math.min(keep, stepLevels.length); applySteps(); pageLabel(); }   // a resize must not hide what was already revealed

  function keys(e) {
    if (root && root.hidden) return;
    if (/INPUT|TEXTAREA|SELECT/.test((e.target && e.target.tagName) || '')) return;     // typing in a box is not a clicker press
    const blank = stage && stage.querySelector('.ts-blank');
    if (e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === ' ') { e.preventDefault(); if (blank) blank.remove(); else nextStep(); }
    if (e.key === 'ArrowLeft' || e.key === 'PageUp') { e.preventDefault(); if (blank) blank.remove(); else prevStep(); }
    if ((e.key === '[' || e.key === ']') && tool === 'erase') { eraseR = Math.max(6, Math.min(60, eraseR + (e.key === ']' ? 4 : -4))); redraw(); }
    else if ((e.key === '[' || e.key === ']') && sizeSetter) sizeSetter(size + (e.key === ']' ? 1 : -1), true);
    // presenter-clicker keys: «black screen» (B or .), «white screen» (W or ,), «start» (F5)
    if (['b', 'B', '.', 'w', 'W', ','].includes(e.key) && stage) {
      e.preventDefault();
      if (blank) blank.remove();
      else { const el = document.createElement('div'); el.className = 'ts-blank'; el.style.cssText = `position:absolute;inset:0;z-index:60;background:${/[bB.]/.test(e.key) ? '#000' : '#fff'}`; el.onclick = () => el.remove(); stage.append(el); }
    }
    if (e.key === 'F5') { e.preventDefault(); if (!document.fullscreenElement) toggleFs(); }
    // Esc closes the lesson only when pressed twice, so a clicker's «end» button cannot end the class by accident
    if (e.key === 'Escape') {
      if (blank) return blank.remove();
      if (performance.now() - escAt < 2000) close(); else { escAt = performance.now(); Exam.notify('ចុច Esc ម្តងទៀតដើម្បីបិទមេរៀន'); }
    }
  }
  let escAt = -9999;

  function toggleFs() {
    try {
      if (document.fullscreenElement) document.exitFullscreen();
      else (root.requestFullscreen || root.webkitRequestFullscreen || (() => {})).call(root);
    } catch (e) { /* not supported (e.g. iPhone) */ }
  }

  function close() {
    clearInterval(clockT); clockT = 0;
    stopWidgets();
    if (offTools) { offTools(); offTools = null; }
    try { if (document.fullscreenElement) document.exitFullscreen(); } catch (e) { /* ignore */ }
    window.removeEventListener('keydown', keys);
    window.removeEventListener('resize', onResize);
    document.body.classList.remove('teach-show-on');
    if (root) { root.hidden = true; root.innerHTML = ''; }
    floats = [];
    palette = null;
  }

  window.TeachShow = { open, close, isOpen: () => root && !root.hidden, exportScopes, buildExport };   // exportScopes/buildExport: also used by the tests
})();
