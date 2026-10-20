// Presentation-only navigation. Existing data-tab handlers own rendering and access.
(() => {
  const nav = document.getElementById('teacher-navigation');
  const toggle = document.getElementById('nav-toggle');
  if (!nav || !toggle) return;
  const title = document.getElementById('workspace-title');
  const mobileTitle = document.getElementById('mobile-section');
  const buttons = [...nav.querySelectorAll('[data-tab]')];
  const close = () => {
    nav.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
  };
  const dashboard = document.getElementById('view-dashboard');
  const sync = () => {
    if (dashboard.hidden || document.body.classList.contains('teach-mode')) return;
    const active = buttons.find((button) => button.classList.contains('active'));
    buttons.forEach((button) => {
      if (button === active) button.setAttribute('aria-current', 'page');
      else button.removeAttribute('aria-current');
    });
    if (active) {
      const label = active.textContent.trim();
      title.textContent = label;
      mobileTitle.textContent = label;
      document.title = `${label} — Exam Khmer`;
    }
  };
  toggle.addEventListener('click', () => {
    const open = !nav.classList.contains('is-open');
    nav.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', String(open));
  });
  nav.addEventListener('click', (event) => {
    if (!event.target.closest('[data-tab]')) return;
    // Do not leave keyboard focus inside a menu that has just been hidden.
    if (matchMedia('(max-width: 800px)').matches) {
      close();
      toggle.focus({ preventScroll: true });
    }
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && nav.classList.contains('is-open')) {
      close(); toggle.focus({ preventScroll: true });
    }
  });
  // Some existing flows activate a section programmatically (e.g. schedule a test).
  new MutationObserver(sync).observe(nav, { subtree: true, attributes: true, attributeFilter: ['class'] });
  new MutationObserver(sync).observe(dashboard, { attributes: true, attributeFilter: ['hidden'] });
  sync();
})();

// ---- user menu, avatar, grouped captions and the phone bottom bar (presentation only) ----
(() => {
  const chip = document.getElementById('user-chip'), pop = document.getElementById('user-pop');
  const badge = document.getElementById('teacher-username-badge');
  if (chip && pop) {
    const close = () => { pop.hidden = true; chip.setAttribute('aria-expanded', 'false'); };
    chip.addEventListener('click', (e) => { e.stopPropagation(); pop.hidden = !pop.hidden; chip.setAttribute('aria-expanded', String(!pop.hidden)); });
    document.addEventListener('click', (e) => { if (!pop.hidden && !e.target.closest('.user-menu')) close(); });
    pop.addEventListener('click', () => setTimeout(close, 0));
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && !pop.hidden) { close(); chip.focus(); } });
  }
  const syncUser = () => {
    if (!badge) return;
    const full = badge.textContent.trim();
    if (!full) return;
    const name = full.split(' · ')[0].trim();
    const nm = document.getElementById('user-name'), av = document.getElementById('user-avatar');
    if (nm) nm.textContent = name;
    if (av) av.textContent = [...name][0] || 'គ';
    const eb = document.querySelector('.dashboard-header .eyebrow'); if (eb) eb.textContent = `សួស្តី ${name} 👋`;
  };
  if (badge) { new MutationObserver(syncUser).observe(badge, { childList: true, characterData: true, subtree: true }); syncUser(); }

  const nav = document.getElementById('teacher-navigation');
  if (!nav) return;
  // hide a caption when none of the buttons under it is visible (e.g. the owner-only group)
  const tidyCaptions = () => {
    let cap = null, any = false;
    const flush = () => { if (cap && cap.hidden !== !any) cap.hidden = !any; };
    for (const el of nav.children) {
      if (el.classList.contains('nav-caption')) { flush(); cap = el; any = false; }
      else if (el.matches('button[data-tab]') && !el.hidden) any = true;
    }
    flush();
  };
  new MutationObserver(tidyCaptions).observe(nav, { subtree: true, attributes: true, attributeFilter: ['hidden'] });
  tidyCaptions();

  // phone: bottom bar with the four main places and a "more" sheet holding the full menu
  const main = [['classes', 'ថ្នាក់'], ['tests', 'តេស្ត'], ['schedule', 'ប្រឡង'], ['grading', 'ពិន្ទុ']];
  const bar = document.createElement('div');
  bar.className = 'bottom-bar'; bar.id = 'bottom-bar'; bar.setAttribute('role', 'navigation'); bar.setAttribute('aria-label', 'មុខងារសំខាន់');
  const icon = (tab) => { const src = nav.querySelector(`[data-tab="${tab}"] svg`); return src ? src.outerHTML : ''; };
  main.forEach(([tab, label]) => {
    const b = document.createElement('button'); b.type = 'button'; b.dataset.go = tab;
    b.innerHTML = `${icon(tab)}<span>${label}</span>`;
    b.addEventListener('click', () => { nav.classList.remove('is-open'); const src = nav.querySelector(`[data-tab="${tab}"]`); if (src) src.click(); window.scrollTo({ top: 0 }); });
    bar.append(b);
  });
  const more = document.createElement('button'); more.type = 'button'; more.className = 'more';
  more.innerHTML = '<svg class="ui-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg><span>ម៉ឺនុយ</span>';
  more.addEventListener('click', () => { const open = !nav.classList.contains('is-open'); nav.classList.toggle('is-open', open); document.body.classList.toggle('sheet-open', open); });
  bar.append(more);
  document.body.append(bar);
  const scrim = document.createElement('div'); scrim.className = 'sheet-scrim'; scrim.addEventListener('click', () => { nav.classList.remove('is-open'); document.body.classList.remove('sheet-open'); });
  document.body.append(scrim);
  nav.addEventListener('click', (e) => { if (e.target.closest('[data-tab]')) { nav.classList.remove('is-open'); document.body.classList.remove('sheet-open'); window.scrollTo({ top: 0 }); } });
  const dash = document.getElementById('view-dashboard');
  const syncBar = () => {
    const active = nav.querySelector('button.active');
    bar.hidden = dash.hidden;
    bar.querySelectorAll('[data-go]').forEach((b) => b.classList.toggle('on', !!active && active.dataset.tab === b.dataset.go));
    more.classList.toggle('on', !!active && !main.some(([t]) => t === active.dataset.tab));
  };
  new MutationObserver(syncBar).observe(nav, { subtree: true, attributes: true, attributeFilter: ['class'] });
  new MutationObserver(syncBar).observe(dash, { attributes: true, attributeFilter: ['hidden'] });
  syncBar();
})();
