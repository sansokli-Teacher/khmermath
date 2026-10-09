// Exam integrity (student side). A web page cannot block an operating-system screenshot or an
// AI overlay, so this layer (1) makes copying/selecting/printing hard, (2) hides the questions
// whenever the exam page is not in front, (3) reports everything to the server so the teacher
// has a timeline, and (4) lets the server warn or lock the student.
const Integrity = (() => {
  let sid = null, cfg = { mode: 'warn', max: 3 }, hooks = {}, running = false;
  let queue = [], flushTimer = null, hiddenAt = 0, blurAt = 0, wasFs = false, base = null, bc = null, devOpen = false;
  const timers = [], offs = [];

  const log = (kind, detail, dur) => {
    if (!running) return;
    if (queue.length < 200) queue.push({ kind, detail: detail || null, dur_ms: dur || null, t: Date.now() });
    clearTimeout(flushTimer);
    flushTimer = setTimeout(flush, 1500);
  };
  async function flush(keepalive) {
    clearTimeout(flushTimer);
    if (!sid || !queue.length) return null;
    const events = queue.splice(0, 40);
    try {
      const res = await fetch('/api/student/events', {
        method: 'POST', credentials: 'include', keepalive: !!keepalive,
        headers: { 'Content-Type': 'application/json', 'X-Device': Exam.deviceId() },
        body: JSON.stringify({ session_id: sid, events }),
      });
      if (res.status === 401) { queue.unshift(...events); flushTimer = setTimeout(flush, 8000); return null; }   // logged out: keep them until the student signs in again
      const d = await res.json().catch(() => null);
      if (d && d.violations != null && hooks.onState) hooks.onState(d);
      if (queue.length) flushTimer = setTimeout(flush, 500);
      return d;
    } catch { queue.unshift(...events); flushTimer = setTimeout(flush, 5000); return null; }
  }

  function on(target, type, fn, opts) { target.addEventListener(type, fn, opts); offs.push(() => target.removeEventListener(type, fn, opts)); }
  const fsEl = () => document.fullscreenElement || document.webkitFullscreenElement || null;
  const isTouch = () => matchMedia('(pointer: coarse)').matches;

  function start(sessionId, config, h) {
    stop();
    sid = sessionId; cfg = config || cfg; hooks = h || {}; running = true;
    base = { w: innerWidth, h: innerHeight, land: innerWidth >= innerHeight };
    wasFs = !!fsEl();
    log('start', navigator.userAgent.slice(0, 100));

    on(document, 'visibilitychange', () => {
      if (document.hidden) { hiddenAt = Date.now(); if (hooks.onAway) hooks.onAway(true); }
      else if (hiddenAt) { const d = Date.now() - hiddenAt; hiddenAt = 0; log('tab_hidden', null, d); if (hooks.onAway) hooks.onAway(false, d); flush(); }
    });
    on(window, 'blur', () => { if (!document.hidden && !blurAt) { blurAt = Date.now(); if (hooks.onAway) hooks.onAway(true); } });
    on(window, 'focus', () => {
      if (blurAt) { const d = Date.now() - blurAt; blurAt = 0; log('window_blur', null, d); if (hooks.onAway) hooks.onAway(false, d); flush(); }
    });
    on(window, 'pagehide', () => flush(true));
    on(window, 'online', () => log('online'));
    on(window, 'offline', () => log('offline'));

    const fsChange = () => {
      const now = !!fsEl();
      if (wasFs && !now) { log('fullscreen_exit'); if (hooks.onFullscreen) hooks.onFullscreen(false); flush(); }
      if (!wasFs && now) { log('fullscreen_enter'); if (hooks.onFullscreen) hooks.onFullscreen(true); }
      wasFs = now;
    };
    on(document, 'fullscreenchange', fsChange); on(document, 'webkitfullscreenchange', fsChange);

    // split-screen / floating window: the window gets much smaller without the phone being turned
    let rz = null;
    on(window, 'orientationchange', () => setTimeout(() => { base = { w: innerWidth, h: innerHeight, land: innerWidth >= innerHeight }; }, 600));
    on(window, 'resize', () => {
      clearTimeout(rz);
      rz = setTimeout(() => {
        const land = innerWidth >= innerHeight;
        if (land !== base.land) { base = { w: innerWidth, h: innerHeight, land }; return; }
        if (document.activeElement && /INPUT|TEXTAREA/.test(document.activeElement.tagName)) return;
        if (innerWidth < base.w * 0.75 || innerHeight < base.h * 0.7) { log('split_view', `${innerWidth}x${innerHeight} from ${base.w}x${base.h}`); flush(); }
        base = { w: Math.max(innerWidth, base.w * 0.9), h: Math.max(innerHeight, base.h * 0.9), land };   // allow growing back
      }, 700);
    });

    for (const t of ['copy', 'cut']) on(document, t, (e) => { e.preventDefault(); log(t); });
    on(document, 'contextmenu', (e) => { e.preventDefault(); log('contextmenu'); });
    on(document, 'dragstart', (e) => e.preventDefault());
    on(document, 'selectstart', (e) => { if (!/INPUT|TEXTAREA/.test((e.target.tagName || ''))) e.preventDefault(); });
    on(window, 'beforeprint', () => log('print'));
    on(document, 'keydown', (e) => {
      const k = (e.key || '').toLowerCase(), mod = e.ctrlKey || e.metaKey;
      let combo = null;
      if (e.key === 'PrintScreen') combo = 'PrintScreen';
      else if (e.metaKey && e.shiftKey && ['3', '4', '5', 's'].includes(k)) combo = `Meta+Shift+${k}`;
      else if (e.key === 'F12' || (mod && e.shiftKey && ['i', 'j', 'c'].includes(k)) || (e.metaKey && e.altKey && ['i', 'j', 'c'].includes(k))) combo = 'DevTools';
      else if (mod && ['p', 's', 'u', 'a', 'c', 'x'].includes(k)) combo = `${e.ctrlKey ? 'Ctrl' : 'Cmd'}+${k.toUpperCase()}`;
      if (combo) { e.preventDefault(); if (e.key === 'PrintScreen') { try { navigator.clipboard.writeText(' '); } catch {} } log('shortcut', combo); flush(); }
    });
    on(document, 'keyup', (e) => { if (e.key === 'PrintScreen') { try { navigator.clipboard.writeText(' '); } catch {} log('shortcut', 'PrintScreen'); } });

    // developer tools docked to the window (desktop only)
    if (!isTouch()) timers.push(setInterval(() => {
      const open = !fsEl() && (outerWidth - innerWidth > 220 || outerHeight - innerHeight > 280);
      if (open && !devOpen) log('devtools', `${outerWidth - innerWidth}x${outerHeight - innerHeight}`);
      devOpen = open;
    }, 2500));

    // the same exam open in a second tab of this browser
    try {
      bc = new BroadcastChannel(`exam-${sid}`);
      const me = Math.random().toString(36).slice(2);
      bc.onmessage = (m) => {
        if (m.data && m.data.from !== me) { if (m.data.t === 'hello') bc.postMessage({ t: 'here', from: me }); else if (m.data.t === 'here') log('second_tab'); }
      };
      bc.postMessage({ t: 'hello', from: me });
    } catch {}
    timers.push(setInterval(() => flush(), 15000));
  }

  function stop() {
    running = false;
    for (const o of offs.splice(0)) o();
    for (const t of timers.splice(0)) clearInterval(t);
    clearTimeout(flushTimer);
    try { if (bc) bc.close(); } catch {} bc = null;
    queue = []; sid = null;
  }

  // a faint tiled "NAME · ID" over the exam: a leaked screenshot shows whose it is
  function watermark(text) {
    unwatermark();
    const safe = String(text).replace(/[<>&"']/g, '');
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="520" height="340"><text x="30" y="190" transform="rotate(-22 260 170)" font-family="sans-serif" font-size="13" fill="rgba(20,40,35,0.035)">${safe}</text></svg>`;
    const el = document.createElement('div');
    el.id = 'exam-watermark';
    el.style.cssText = `position:fixed;inset:0;z-index:40;pointer-events:none;background-image:url("data:image/svg+xml;utf8,${encodeURIComponent(svg)}");background-repeat:repeat;`;
    document.body.append(el);
  }
  function unwatermark() { const el = document.getElementById('exam-watermark'); if (el) el.remove(); }

  async function goFullscreen() {
    const el = document.documentElement;
    const fn = el.requestFullscreen || el.webkitRequestFullscreen;
    if (!fn) return false;
    try { await fn.call(el); return true; } catch { return false; }
  }
  const fullscreenSupported = () => !!(document.documentElement.requestFullscreen || document.documentElement.webkitRequestFullscreen);

  return { start, stop, flush, watermark, unwatermark, goFullscreen, fullscreenSupported, isFullscreen: () => !!fsEl(), log };
})();
