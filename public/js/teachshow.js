// Classroom slideshow: ink, movable spin (¼), timer, calculator.
(function () {
  const kh = (n) => String(n ?? '').replace(/\d/g, (d) => '០១២៣៤៥៦៧៨៩'[d]);
  let root, stage, slideEl, ink, ctx, i = 0, slides = [], students = [];
  let tool = 'none', color = '#e03131', size = 4, drawing = false, cur = null, spot = null, stamp = '✔';
  let offTools = null, meta = { grade: '', lesson: '' }, lensPin = false, toolSetter = null, lensIco = null, lens = null, lensIn = null, lensClone = null, lensRaf = 0, lensGo = { x: 0, y: 0, z: 1 }, lensNow = { x: 0, y: 0, z: 1 }, lensOn = false, lensZoom = 2.2;
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
    if (!depth) { if (slides[i] && slideEl && slideEl.innerHTML) slides[i]._ink = strokes; lensOff(); lensClone = null; } // remember what was written on the slide we leave
    i = Math.max(0, Math.min(slides.length - 1, n));
    const s = slides[i] || { html: '' };
    slideEl.className = 'ts-slide' + (s.k ? ` ts-${s.k}` : '') + (s.c ? ` ts-${s.c}` : '');
    slideEl.innerHTML = s.html || '';
    math(slideEl);
    const fits = fitText(0.72);
    if (!fits && (depth || 0) < 4 && splitSlide(i)) return show(i, (depth || 0) + 1);
    if (!fits) fitText(0.4);
    s._fs = slideEl.style.fontSize;
    const lab = root.querySelector('.ts-page');
    if (lab) lab.textContent = `${kh(i + 1)} / ${kh(slides.length)}`;
    strokes = s._ink || []; undoS = []; redoS = []; cur = null;
    redraw(); syncUndo();
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
        el.innerHTML = sl.html || '';
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
    const r = ink.getBoundingClientRect();
    hand.style.left = (e.clientX - r.left - 8) + 'px';
    hand.style.top = (e.clientY - r.top - 88) + 'px';
    hand.hidden = false;
  }

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
    window.addEventListener('pointerup', () => { if (hand) hand.classList.remove('writing'); });
    const down = (e) => {
      if (e.button && e.button !== 0) return;
      const p = pos(e);
      closeMenus();
      if (tool === 'zoom') {
        if (lensOn || lensPin) { lensPin = !lensPin; lens.classList.toggle('pin', lensPin); if (!lensPin) lensMove(e); }
        return;
      }
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
    const rl = document.createElement('div');
    rl.className = 'ts-rs ts-rl'; rl.title = 'ប្ដូរទំហំ';
    el.append(bar, inner, rs, rl);
    stage.append(el);
    drag(el, bar);
    resize(el, rs);
    resizeLeft(el, rl);
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
      if (e.buttons === 0) { dragging = false; return; }
      const s = stage.getBoundingClientRect();
      el.style.left = Math.max(0, Math.min(s.width - 80, e.clientX - s.left - ox)) + 'px';
      el.style.top = Math.max(0, Math.min(s.height - 40, e.clientY - s.top - oy)) + 'px';
    });
    bar.addEventListener('pointerup', () => { dragging = false; });
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
      el.style.height = Math.max(140, sh + (e.clientY - sy)) + 'px';
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
      el.style.height = Math.max(140, sh + (e.clientY - sy)) + 'px';
    });
    handle.addEventListener('pointerup', () => { on = false; });
    handle.addEventListener('pointercancel', () => { on = false; });
    handle.addEventListener('lostpointercapture', () => { on = false; });
  }

  // ---- Spin: wheel of the class list (one student or a group), pop-up result, sound and fireworks ----
  let audio = null;
  const snd = {
    ctx() { try { audio = audio || new (window.AudioContext || window.webkitAudioContext)(); if (audio.state === 'suspended') audio.resume(); } catch { audio = null; } return audio; },
    tick(on) { const c = on && this.ctx(); if (!c) return; const o = c.createOscillator(), g = c.createGain(); o.type = 'square'; o.frequency.value = 880; g.gain.setValueAtTime(.05, c.currentTime); g.gain.exponentialRampToValueAtTime(.0001, c.currentTime + .05); o.connect(g).connect(c.destination); o.start(); o.stop(c.currentTime + .06); },
    fanfare(on) { const c = on && this.ctx(); if (!c) return; [523, 659, 784, 1047, 1319].forEach((f, k) => { const o = c.createOscillator(), g = c.createGain(), t = c.currentTime + k * .11; o.type = 'triangle'; o.frequency.value = f; g.gain.setValueAtTime(.0001, t); g.gain.exponentialRampToValueAtTime(.18, t + .02); g.gain.exponentialRampToValueAtTime(.0001, t + .5); o.connect(g).connect(c.destination); o.start(t); o.stop(t + .55); }); },
    beep(on, hi) { const c = on && this.ctx(); if (!c) return; const o = c.createOscillator(), g = c.createGain(), t = c.currentTime; o.type = 'sine'; o.frequency.value = hi ? 1175 : 784; g.gain.setValueAtTime(.0001, t); g.gain.exponentialRampToValueAtTime(.3, t + .01); g.gain.exponentialRampToValueAtTime(.0001, t + .22); o.connect(g).connect(c.destination); o.start(t); o.stop(t + .25); },
    alarm(on) { const c = on && this.ctx(); if (!c) return; [0, .16].forEach((d) => { const o = c.createOscillator(), g = c.createGain(), t = c.currentTime + d; o.type = 'square'; o.frequency.value = 988; g.gain.setValueAtTime(.0001, t); g.gain.exponentialRampToValueAtTime(.12, t + .01); g.gain.exponentialRampToValueAtTime(.0001, t + .13); o.connect(g).connect(c.destination); o.start(t); o.stop(t + .15); }); },
    boom(on) { const c = on && this.ctx(); if (!c) return; const n = c.sampleRate * .35, buf = c.createBuffer(1, n, c.sampleRate), d = buf.getChannelData(0); for (let k = 0; k < n; k++) d[k] = (Math.random() * 2 - 1) * Math.pow(1 - k / n, 3); const src = c.createBufferSource(), f = c.createBiquadFilter(), g = c.createGain(); src.buffer = buf; f.type = 'lowpass'; f.frequency.value = 900; g.gain.value = .5; src.connect(f).connect(g).connect(c.destination); src.start(); },
  };

  function miniSpin(names, cname) {
    const wrap = document.createElement('div');
    wrap.className = 'sp';
    const bar = document.createElement('div'); bar.className = 'sp-bar';
    const modeBtns = [['one', 'ម្នាក់ៗ'], ['group', 'ក្រុម']].map(([m, t]) => { const b = document.createElement('button'); b.type = 'button'; b.textContent = t; b.dataset.m = m; return b; });
    const gsel = document.createElement('select'); gsel.title = 'ចំនួនក្រុម';
    [2, 3, 4, 5, 6, 7, 8, 9, 10, 12].forEach((n) => gsel.append(new Option(`${kh(n)} ក្រុម`, n)));
    gsel.value = 6;
    const dvd = document.createElement('button'); dvd.type = 'button'; dvd.className = 'sp-dvd'; dvd.textContent = 'ចែកក្រុម'; dvd.title = 'ចែកថ្នាក់ជាក្រុមៗ ហើយបង្ហាញទាំងអស់';
    const rep = document.createElement('label'); rep.className = 'sp-chk'; rep.innerHTML = '<input type="checkbox" checked><span>មិនជាន់</span>';
    const snb = document.createElement('button'); snb.type = 'button'; snb.className = 'sp-snd'; snb.textContent = '🔊'; snb.title = 'សំឡេង';
    const rst = document.createElement('button'); rst.type = 'button'; rst.className = 'sp-rst'; rst.textContent = '↺'; rst.title = 'ចាប់ផ្ដើមឡើងវិញ';
    bar.append(...modeBtns, gsel, dvd, rep, snb, rst);
    const stageW = document.createElement('div'); stageW.className = 'sp-wheel';
    const cv = document.createElement('canvas'); cv.width = 640; cv.height = 640;
    const hub = document.createElement('button'); hub.type = 'button'; hub.className = 'sp-hub'; hub.textContent = 'SPIN';
    const disc = document.createElement('div'); disc.className = 'sp-disc';
    disc.append(cv, hub); stageW.append(disc);
    const info = document.createElement('div'); info.className = 'sp-info';
    const pop = document.createElement('div'); pop.className = 'sp-pop'; pop.hidden = true;
    const fw = document.createElement('canvas'); fw.className = 'sp-fw';
    // simple by default: only the wheel; the options live behind a small gear
    bar.hidden = true;
    const gear = document.createElement('button'); gear.type = 'button'; gear.className = 'sp-gear'; gear.textContent = '⚙'; gear.title = 'ជម្រើស';
    gear.onclick = () => { bar.hidden = !bar.hidden; gear.classList.toggle('on', !bar.hidden); };
    wrap.append(bar, stageW, info, pop, fw, gear);
    const c = cv.getContext('2d');
    const pal = ['#e8590c', '#1c7ed6', '#2f9e44', '#ae3ec9', '#f08c00', '#0c8599', '#d6336c', '#5f3dc4', '#c92a2a', '#087f5b'];
    const st = { mode: 'one', sound: true, ang: 0, spin: false, used: new Set(), groups: [] };
    const roster = names.length ? names.slice() : ['សិស្ស ក', 'សិស្ស ខ', 'សិស្ស គ', 'សិស្ស ឃ'];
    const shuffle = (a) => { a = a.slice(); for (let k = a.length - 1; k > 0; k--) { const j = Math.floor(Math.random() * (k + 1)); [a[k], a[j]] = [a[j], a[k]]; } return a; };
    const makeGroups = () => { const n = Math.max(1, Math.min(+gsel.value || 6, roster.length)), g = Array.from({ length: n }, () => []); shuffle(roster).forEach((nm, k) => g[k % n].push(nm)); st.groups = g; };
    makeGroups();
    // what is on the wheel right now
    const items = () => {
      const noRep = rep.querySelector('input').checked;
      if (st.mode === 'one') return roster.map((n, k) => ({ id: 'o' + k, label: n, members: [n] })).filter((x) => !(noRep && st.used.has(x.id)));
      return st.groups.map((g, k) => ({ id: 'g' + k, label: `ក្រុម ${kh(k + 1)}`, members: g })).filter((x) => !(noRep && st.used.has(x.id)));
    };
    let list = items();
    const refresh = () => {
      list = items();
      modeBtns.forEach((b) => b.classList.toggle('on', b.dataset.m === st.mode));
      gsel.style.display = st.mode === 'group' ? '' : 'none';
      const total = st.mode === 'one' ? roster.length : st.groups.length;
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

    // ---- fireworks (canvas over the whole spin window) ----
    let fwRaf = 0, parts = [], fwEnd = 0, nextBurst = 0;
    function fireworks(ms) {
      const r = wrap.getBoundingClientRect(), dpr = Math.min(2, window.devicePixelRatio || 1);
      fw.width = Math.floor(r.width * dpr); fw.height = Math.floor(r.height * dpr);
      const fc = fw.getContext('2d'); fc.setTransform(dpr, 0, 0, dpr, 0, 0);
      parts = []; fwEnd = performance.now() + ms; nextBurst = 0;
      cancelAnimationFrame(fwRaf);
      const burst = () => {
        const x = r.width * (.15 + Math.random() * .7), y = r.height * (.12 + Math.random() * .5), hue = Math.random() * 360, n = 46;
        for (let k = 0; k < n; k++) { const a = Math.PI * 2 * k / n + Math.random() * .2, v = 1.6 + Math.random() * 3.2; parts.push({ x, y, vx: Math.cos(a) * v, vy: Math.sin(a) * v, life: 1, hue: hue + Math.random() * 40, w: 2 + Math.random() * 2 }); }
        snd.boom(st.sound);
      };
      const loop = (now) => {
        fc.clearRect(0, 0, r.width, r.height);
        if (now < fwEnd && now >= nextBurst) { burst(); nextBurst = now + 380 + Math.random() * 260; }
        parts.forEach((q) => { q.x += q.vx; q.y += q.vy; q.vy += .045; q.vx *= .992; q.life -= .011; fc.globalAlpha = Math.max(0, q.life); fc.fillStyle = `hsl(${q.hue} 95% 60%)`; fc.beginPath(); fc.arc(q.x, q.y, q.w, 0, Math.PI * 2); fc.fill(); });
        fc.globalAlpha = 1;
        parts = parts.filter((q) => q.life > 0);
        if (now < fwEnd || parts.length) fwRaf = requestAnimationFrame(loop); else fc.clearRect(0, 0, r.width, r.height);
      };
      fwRaf = requestAnimationFrame(loop);
    }

    // ---- result pop-up, sized from the spin window ----
    const showPop = (it) => {
      const noRep = rep.querySelector('input').checked;
      if (noRep) st.used.add(it.id);
      pop.hidden = false;
      const group = st.mode === 'group';
      pop.innerHTML = `<div class="pp-card"><div class="pp-k">${group ? '🎉 ក្រុមដែលត្រូវបានជ្រើស' : '🎉 សិស្សដែលត្រូវបានជ្រើស'}</div>
        <div class="pp-name">${esc(it.label)}</div>
        ${group ? `<ul class="pp-mem">${it.members.map((m) => `<li>${esc(m)}</li>`).join('')}</ul>` : ''}
        <div class="pp-act"><button type="button" class="pp-ok">បិទ</button><button type="button" class="pp-again">បង្វិលម្ដងទៀត</button></div></div>`;
      pop.querySelector('.pp-ok').onclick = () => { pop.hidden = true; refresh(); };
      pop.querySelector('.pp-again').onclick = () => { pop.hidden = true; refresh(); hub.click(); };
      snd.fanfare(st.sound);
      fireworks(3200);
    };
    const esc = (t) => String(t).replace(/[&<>]/g, (m) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[m]));

    // divide the whole class into groups and show every group at once
    const showGroups = (again) => {
      if (again) makeGroups();
      pop.hidden = false;
      pop.innerHTML = `<div class="pp-card pp-all"><div class="pp-k">👥 ចែកជា ${kh(st.groups.length)} ក្រុម</div>
        <div class="pp-grid">${st.groups.map((g, k) => `<div class="pp-g"><b>ក្រុម ${kh(k + 1)}</b><ul>${g.map((m) => `<li>${esc(m)}</li>`).join('')}</ul></div>`).join('')}</div>
        <div class="pp-act"><button type="button" class="pp-ok">បិទ</button><button type="button" class="pp-again">ចែកម្ដងទៀត</button></div></div>`;
      pop.querySelector('.pp-ok').onclick = () => { pop.hidden = true; st.used.clear(); refresh(); };
      pop.querySelector('.pp-again').onclick = () => showGroups(true);
      if (again) snd.tick(st.sound);
    };
    dvd.onclick = () => { if (st.spin) return; if (st.mode !== 'group') { st.mode = 'group'; st.used.clear(); st.ang = 0; } showGroups(false); refresh(); };

    hub.onclick = () => {
      if (st.spin || !list.length) return;
      pop.hidden = true; snd.ctx();
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
    modeBtns.forEach((b) => { b.onclick = () => { if (st.spin) return; st.mode = b.dataset.m; st.used.clear(); st.ang = 0; pop.hidden = true; refresh(); }; });
    gsel.onchange = () => { if (st.spin) return; makeGroups(); st.used.clear(); refresh(); };
    rep.querySelector('input').onchange = refresh;
    snb.onclick = () => { st.sound = !st.sound; snb.textContent = st.sound ? '🔊' : '🔇'; };
    rst.onclick = () => { if (st.spin) return; st.used.clear(); if (st.mode === 'group') makeGroups(); pop.hidden = true; refresh(); };
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
    end.append(toolsMenu(), mk('ts-fs', '⛶', toggleFs), mk('ts-exit', '✕', close));
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
      toolSetter = setTool;
      tool = id; spot = null; laser = []; if (!lensPin) lensOff();
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
        if (f) { f.hidden = !f.hidden; if (!f.hidden) stage.append(f); it.classList.toggle('on', !f.hidden); }
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
    let w, h, body = '';
    if (kind === 'ruler') {
      w = Math.round(CM * 15 + 24); h = 66;
      body += `<rect x="1" y="1" width="${w - 2}" height="${h - 2}" rx="6" fill="rgba(255,236,160,.93)" stroke="#a88a2a" stroke-width="2"/>`;
      for (let mm = 0; mm <= 150; mm++) {
        const x = 12 + mm * CM / 10, len = mm % 10 === 0 ? 22 : mm % 5 === 0 ? 15 : 9;
        body += `<line x1="${x}" y1="2" x2="${x}" y2="${2 + len}" stroke="#5a4a10" stroke-width="${mm % 10 === 0 ? 1.6 : 1}"/>`;
        if (mm % 10 === 0) body += `<text x="${x}" y="40" font-size="14" font-weight="700" text-anchor="middle" fill="#3b300a">${mm / 10}</text>`;
      }
      body += `<text x="${w - 30}" y="58" font-size="12" fill="#5a4a10">cm</text>`;
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
    } else {
      const a = kind === 'set45' ? 300 : 210, b = kind === 'set45' ? 300 : 364; // legs
      w = a + 20; h = b + 20;
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
    return { svg, w, h };
  }

  function addInstrument(kind) {
    const { svg, w, h } = instSVG(kind);
    const el = document.createElement('div');
    el.className = 'ts-inst';
    el.style.width = w + 'px'; el.style.height = h + 'px';
    el.append(svg);
    const rot = document.createElement('button'); rot.type = 'button'; rot.className = 'ts-irot'; rot.textContent = '↻'; rot.title = 'បង្វិល';
    const x = document.createElement('button'); x.type = 'button'; x.className = 'ts-ix'; x.textContent = '✕'; x.title = 'ដកចេញ';
    el.append(rot, x);
    let px = Math.max(10, (stage.clientWidth - w) / 2 - 80 + Math.random() * 40), py = Math.max(10, (stage.clientHeight - h) / 2 + Math.random() * 40), ang = 0;
    const apply = () => { el.style.left = px + 'px'; el.style.top = py + 'px'; el.style.transform = `rotate(${ang}deg)`; };
    apply();
    stage.append(el);
    x.onclick = () => el.remove();
    let mode = null, sx = 0, sy = 0, bx = 0, by = 0, a0 = 0, g0 = 0, cxp = 0, cyp = 0;
    el.addEventListener('pointerdown', (e) => {
      if (e.target === x) return;
      el.setPointerCapture(e.pointerId);
      stage.append(el); // bring to front
      if (e.target === rot) {
        mode = 'rot';
        const r = el.getBoundingClientRect(); cxp = r.left + r.width / 2; cyp = r.top + r.height / 2;
        a0 = Math.atan2(e.clientY - cyp, e.clientX - cxp); g0 = ang;
      } else { mode = 'move'; sx = e.clientX; sy = e.clientY; bx = px; by = py; }
      e.preventDefault();
    });
    el.addEventListener('pointermove', (e) => {
      if (!mode) return;
      if (mode === 'move') { px = bx + e.clientX - sx; py = by + e.clientY - sy; }
      else { ang = g0 + (Math.atan2(e.clientY - cyp, e.clientX - cxp) - a0) * 180 / Math.PI; if (e.shiftKey) ang = Math.round(ang / 15) * 15; }
      apply();
    });
    const up = () => { mode = null; };
    el.addEventListener('pointerup', up); el.addEventListener('pointercancel', up);
    el.addEventListener('wheel', (e) => { e.preventDefault(); ang += (e.deltaY < 0 ? 1 : -1) * (e.shiftKey ? 5 : 1); apply(); }, { passive: false });
    return el;
  }

  function geoBox() {
    const box = document.createElement('div');
    box.className = 'ts-geo';
    box.innerHTML = '<p class="gh">ចុចដើម្បីដាក់លើស្លាយ · អូសដើម្បីផ្លាស់ទី · ↻ ឬកង់កណ្ដុរដើម្បីបង្វិល</p>';
    [['ruler', '📏', 'Ruler', 'បន្ទាត់'], ['protractor', '◠', 'Protractor', 'ម៉ែត្រមុំ'], ['set45', '◣', 'Set square 45°', 'ក្រដាសត្រីកោណ 45°'], ['set60', '◺', 'Set square 30°–60°', 'ក្រដាសត្រីកោណ 30°–60°']].forEach(([k, ic, en, km]) => {
      const b = document.createElement('button'); b.type = 'button';
      b.innerHTML = `<span class="gi">${ic}</span><span><b>${en}</b><small>${km}</small></span>`;
      b.onclick = () => addInstrument(k);
      box.append(b);
    });
    const clr = document.createElement('button'); clr.type = 'button'; clr.className = 'gclr';
    clr.textContent = 'ដកឧបករណ៍ទាំងអស់ចេញ';
    clr.onclick = () => stage.querySelectorAll('.ts-inst').forEach((n) => n.remove());
    box.append(clr);
    return box;
  }

  function open(opt) {
    slides = ((window.TEACH_SLIDES && window.TEACH_SLIDES[`${opt.grade}-${opt.lesson}`]) || []).map((x) => ({ ...x }));
    strokes = []; undoS = []; redoS = []; cur = null; i = 0; slideEl = null;
    if (!slides.length) return Exam.notify('មិនទាន់មានស្លាយ។');
    students = (opt.students || []).map((s) => `${s.surname || ''} ${s.first_name || ''}`.trim()).filter(Boolean);
    close();
    tool = 'none'; // always start as the plain mouse; pick a pen when you want to write
    meta = { grade: opt.grade, lesson: opt.lesson, cname: opt.className || '' };
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
    makeFloat('wspin', 'Spin' + (meta.cname ? ' · ' + meta.cname : ''), miniSpin(students, meta.cname), { x: '52%', y: '3%', w: '40%', h: '92%' }).hidden = true;
    makeFloat('wtime', 'Timer', timerBox(), { x: '64%', y: '3%', w: '300px' }).hidden = true;
    makeFloat('wcalc', 'Calculator', calcBox(), { x: '60%', y: '40%', w: '260px' }).hidden = true;
    makeFloat('wgeo', 'Geometry', geoBox(), { x: '62%', y: '6%', w: '300px' }).hidden = true;
    ctx = ink.getContext('2d');
    bindInk();
    penPalette();
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
    if (offTools) { offTools(); offTools = null; }
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
