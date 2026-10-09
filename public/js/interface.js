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
    if (dashboard.hidden) return;
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
