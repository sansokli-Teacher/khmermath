// Micro-interactions for the teacher dashboard (see css/skin.css):
//   Exam.success(msg)  — toast whose circle draws, then the tick (470 ms)
//   rolling numbers    — any .stat-val / [data-roll] with a plain number rolls digit by digit, 100 ms apart
//   pull to refresh    — touch only: the list follows the finger at 35%
//   Live pill          — jumps to the live-quiz tab
(function () {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  Exam.success = function (message) {
    document.querySelectorAll('.skin-toast').forEach((n) => n.remove());
    const t = document.createElement('div');
    t.className = 'skin-toast'; t.setAttribute('role', 'status');
    t.innerHTML = '<svg viewBox="0 0 30 30" aria-hidden="true"><circle class="ring" cx="15" cy="15" r="12"/><path class="tick" d="M9 15.5l4 4 8-9"/></svg><span></span>';
    t.lastChild.textContent = message;
    document.body.append(t);
    setTimeout(() => { t.classList.add('out'); setTimeout(() => t.remove(), 320); }, 2200);
  };

  // ---- rolling number ----
  function roll(el) {
    const text = el.textContent.trim();
    if (el.dataset.rolled === text || !/^[\d.,%]+$/.test(text) || !/\d/.test(text)) return;
    el.dataset.rolled = text;
    el.setAttribute('aria-label', text);
    const wrap = document.createElement('span'); wrap.className = 'roll'; wrap.setAttribute('aria-hidden', 'true');
    const strips = [];
    [...text].forEach((ch) => {
      if (/\d/.test(ch)) {
        const col = document.createElement('span'); col.className = 'roll-col';
        const strip = document.createElement('span');
        strip.innerHTML = '0123456789'.split('').map((d) => `<i>${d}</i>`).join('');
        col.append(strip); wrap.append(col); strips.push([strip, +ch]);
      } else { const s = document.createElement('span'); s.textContent = ch; wrap.append(s); }
    });
    el.textContent = ''; el.append(wrap);
    if (reduce) { strips.forEach(([s, d]) => { s.style.transform = `translateY(${-d * 1.25}em)`; s.style.transition = 'none'; }); return; }
    requestAnimationFrame(() => requestAnimationFrame(() => strips.forEach(([s, d], i) => {
      s.style.transitionDelay = `${i * 100}ms`; s.style.transform = `translateY(${-d * 1.25}em)`;
    })));
  }
  const scan = (root) => (root.querySelectorAll ? root.querySelectorAll('.stat-val, [data-roll]') : []).forEach(roll);
  new MutationObserver((muts) => {
    for (const m of muts) m.addedNodes.forEach((n) => { if (n.nodeType === 1) { if (n.matches && n.matches('.stat-val, [data-roll]')) roll(n); scan(n); } });
  }).observe(document.body, { childList: true, subtree: true });

  // ---- Live pill ----
  document.addEventListener('click', (e) => {
    if (!e.target.closest('#live-pill')) return;
    const b = document.querySelector('.teacher-navigation [data-tab="live"]'); if (b) b.click();
  });

  // ---- pull to refresh (touch screens only; re-opens the current tab) ----
  if (matchMedia('(pointer: coarse)').matches) {
    const ind = document.createElement('div'); ind.className = 'ptr'; ind.textContent = '↻'; document.body.append(ind);
    let y0 = null, dy = 0;
    const content = () => document.getElementById('dashboard-content');
    document.addEventListener('touchstart', (e) => { y0 = (window.scrollY <= 0 && e.touches.length === 1 && !e.target.closest('input,textarea,select,.modal-back')) ? e.touches[0].clientY : null; dy = 0; }, { passive: true });
    document.addEventListener('touchmove', (e) => {
      if (y0 == null) return;
      dy = e.touches[0].clientY - y0;
      if (dy <= 0) { y0 = null; return; }
      if (e.cancelable) e.preventDefault();
      const pull = dy * 0.35;                       // finger 100% → list 35%
      const c = content(); if (c) { c.style.transition = 'none'; c.style.transform = `translateY(${pull}px)`; }
      ind.style.opacity = Math.min(1, pull / 30); ind.style.transform = `translateY(${Math.min(pull, 60)}px) rotate(${pull * 4}deg)`;
    }, { passive: false });
    const release = () => {
      if (y0 == null) return;
      const c = content(), go = dy * 0.35 > 28; y0 = null;
      if (c) { c.style.transition = 'transform .45s var(--spring)'; c.style.transform = ''; }
      if (go) {
        ind.classList.add('spin');
        const b = document.querySelector('.teacher-navigation button.active'); if (b) b.click();
        setTimeout(() => { ind.classList.remove('spin'); ind.style.opacity = 0; ind.style.transform = ''; }, 800);
      } else { ind.style.opacity = 0; ind.style.transform = ''; }
    };
    document.addEventListener('touchend', release); document.addEventListener('touchcancel', release);
  }
})();
