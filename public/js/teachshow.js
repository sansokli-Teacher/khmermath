// Classroom slideshow: ink, movable spin (¼), timer, calculator.
(function () {
  const kh = (n) => String(n ?? '').replace(/\d/g, (d) => '០១២៣៤៥៦៧៨៩'[d]);
  let root, stage, slideEl, ink, ctx, i = 0, slides = [], students = [];
  let tool = 'pen', color = '#e03131', size = 3, drawing = false, last = null;
  let floats = [];

  function math(el) {
    if (window.renderMathInElement) {
      try { renderMathInElement(el, { throwOnError: false, strict: false, macros: { '\\arc': '\\overset{\\frown}{#1}' }, delimiters: [{ left: '\\(', right: '\\)', display: false }, { left: '\\[', right: '\\]', display: true }] }); } catch {}
    }
  }

  function show(n) {
    i = Math.max(0, Math.min(slides.length - 1, n));
    const s = slides[i] || { html: '' };
    slideEl.className = 'ts-slide' + (s.k ? ` ts-${s.k}` : '');
    slideEl.innerHTML = s.html || '';
    math(slideEl);
    const lab = root.querySelector('.ts-page');
    if (lab) lab.textContent = `${kh(i + 1)} / ${kh(slides.length)}`;
    clearInk(false);
  }

  function fitInk() {
    const r = stage.getBoundingClientRect();
    const dpr = Math.min(2, window.devicePixelRatio || 1);
    ink.width = Math.floor(r.width * dpr);
    ink.height = Math.floor(r.height * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
  }

  function clearInk(all) {
    if (!ctx) return;
    ctx.clearRect(0, 0, ink.width, ink.height);
  }

  function pos(e) {
    const r = ink.getBoundingClientRect();
    const p = e.touches ? e.touches[0] : e;
    return { x: p.clientX - r.left, y: p.clientY - r.top };
  }

  function drawTo(p) {
    if (!last) { last = p; return; }
    ctx.globalCompositeOperation = tool === 'erase' ? 'destination-out' : 'source-over';
    ctx.strokeStyle = color;
    ctx.lineWidth = tool === 'erase' ? 22 : tool === 'hi' ? 18 : size;
    ctx.globalAlpha = tool === 'hi' ? 0.35 : 1;
    ctx.beginPath();
    ctx.moveTo(last.x, last.y);
    ctx.lineTo(p.x, p.y);
    ctx.stroke();
    ctx.globalAlpha = 1;
    last = p;
  }

  function bindInk() {
    const down = (e) => { if (e.button && e.button !== 0) return; drawing = true; last = pos(e); e.preventDefault(); };
    const move = (e) => { if (!drawing) return; drawTo(pos(e)); e.preventDefault(); };
    const up = () => { drawing = false; last = null; };
    ink.addEventListener('pointerdown', down);
    window.addEventListener('pointermove', move);
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
    const tools = bar.appendChild(document.createElement('div'));
    tools.className = 'ts-tools';
    [['pen', 'ប៊ិច'], ['hi', 'គំនូស'], ['erase', 'ជ័រលុប']].forEach(([id, lab]) => {
      const b = mk(id === 'pen' ? 'on' : '', lab, () => {
        tool = id;
        tools.querySelectorAll('button').forEach((x) => x.classList.remove('on'));
        b.classList.add('on');
      });
      tools.append(b);
    });
    ['#e03131', '#1c7ed6', '#2f9e44', '#f08c00', '#212529', '#ffffff'].forEach((col) => {
      const b = document.createElement('button');
      b.type = 'button'; b.className = 'ts-col'; b.style.background = col;
      b.onclick = () => { color = col; tool = tool === 'erase' ? 'pen' : tool; };
      tools.append(b);
    });
    tools.append(mk('', 'សម្អាត', () => clearInk(true)));
    const nav = document.createElement('div');
    nav.className = 'ts-nav';
    nav.append(
      mk('', '←', () => show(i - 1)),
      Object.assign(document.createElement('span'), { className: 'ts-page', textContent: '' }),
      mk('', '→', () => show(i + 1)),
    );
    const widgets = document.createElement('div');
    widgets.className = 'ts-wid';
    const spinF = () => root.querySelector('.ts-spin') && root.querySelector('.ts-spin').closest('.ts-float');
    widgets.append(
      mk('', '🎡 កង់', () => { const f = root.querySelector('.ts-float.ts-wspin'); if (f) f.hidden = !f.hidden; }),
      mk('', '⏱ ម៉ោង', () => { const f = root.querySelector('.ts-float.ts-wtime'); if (f) f.hidden = !f.hidden; }),
      mk('', '∑ ម៉ាស៊ីនគិត', () => { const f = root.querySelector('.ts-float.ts-wcalc'); if (f) f.hidden = !f.hidden; }),
      mk('ts-fs', '⛶', toggleFs),
      mk('ts-exit', '✕', close),
    );
    bar.append(tools, nav, widgets);
    return bar;
  }

  function open(opt) {
    slides = (window.TEACH_SLIDES && window.TEACH_SLIDES[`${opt.grade}-${opt.lesson}`]) || [];
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
    makeFloat('wspin', 'កង់ចាប់ឈ្មោះ', miniSpin(names), { x: '74%', y: '12%', w: '24%', h: '72%' }).hidden = true;
    makeFloat('wtime', 'ម៉ោង', timerBox(), { x: '74%', y: '2%', w: '22%' }).hidden = true;
    makeFloat('wcalc', 'ម៉ាស៊ីនគិតលេខ', calcBox(), { x: '4%', y: '58%', w: '260px' }).hidden = true;
    ctx = ink.getContext('2d');
    bindInk();
    requestAnimationFrame(() => { fitInk(); show(opt.start || 0); });
    window.addEventListener('resize', fitInk);
    window.addEventListener('keydown', keys);
  }

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
    window.removeEventListener('resize', fitInk);
    document.body.classList.remove('teach-show-on');
    if (root) { root.hidden = true; root.innerHTML = ''; }
    floats = [];
  }

  window.TeachShow = { open, close, isOpen: () => root && !root.hidden };
})();
