// Small shared helpers — no framework, plain globals (matches the rest of the khmermath.org tooling).
const Exam = {};

Exam.api = async function (path, options = {}) {
  const res = await fetch(path, {
    method: options.method || 'GET',
    credentials: 'include',
    headers: options.body instanceof ArrayBuffer || options.body instanceof Blob
      ? { 'Content-Type': options.contentType || 'application/octet-stream' }
      : options.body ? { 'Content-Type': 'application/json' } : {},
    body: options.body
      ? (options.body instanceof ArrayBuffer || options.body instanceof Blob ? options.body : JSON.stringify(options.body))
      : undefined,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || `Request failed (${res.status})`);
  return data;
};

Exam.h = function (tag, attrs = {}, children = []) {
  const el = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === 'class') el.className = v;
    else if (k.startsWith('on') && typeof v === 'function') el.addEventListener(k.slice(2), v);
    else if (v !== null && v !== undefined) el.setAttribute(k, v);
  }
  for (const child of [].concat(children)) {
    if (child === null || child === undefined) continue;
    el.appendChild(typeof child === 'string' ? document.createTextNode(child) : child);
  }
  return el;
};

Exam.typeset = function (el) {
  if (window.renderMathInElement) {
    window.renderMathInElement(el, { delimiters: [{ left: '\\(', right: '\\)', display: false }, { left: '\\[', right: '\\]', display: true }] });
  }
};

Exam.showError = function (container, message) {
  const existing = container.querySelector('.error');
  if (existing) existing.remove();
  if (!message) return;
  container.prepend(Exam.h('div', { class: 'error' }, message));
};

Exam.fmtClock = function (ms) {
  const total = Math.max(0, Math.floor(ms / 1000));
  const h = String(Math.floor(total / 3600)).padStart(2, '0');
  const m = String(Math.floor((total % 3600) / 60)).padStart(2, '0');
  const s = String(total % 60).padStart(2, '0');
  return `${h}:${m}:${s}`;
};

Exam.fmtDateTime = function (iso) {
  const d = new Date(iso);
  return d.toLocaleString('km-KH', { dateStyle: 'medium', timeStyle: 'short' });
};

// In-page replacement for window.alert/confirm: native dialogs look out of
// place on a phone-based exam page and block script execution while open.
Exam.modal = function (message, { okOnly = false } = {}) {
  return new Promise((resolve) => {
    function finish(result) { overlay.remove(); resolve(result); }
    const overlay = Exam.h('div', {
      style: 'position:fixed;inset:0;background:rgba(15,23,28,.45);display:flex;align-items:center;justify-content:center;z-index:50;padding:20px;',
      onclick: (e) => { if (e.target === overlay) finish(false); },
    }, [
      Exam.h('div', { class: 'card', style: 'max-width:360px;margin:0;' }, [
        Exam.h('p', { style: 'margin:0 0 16px;white-space:pre-wrap;' }, message),
        Exam.h('div', { class: 'row', style: 'justify-content:flex-end' }, [
          okOnly ? null : Exam.h('button', { class: 'secondary', onclick: () => finish(false) }, 'បោះបង់'),
          Exam.h('button', { onclick: () => finish(true) }, 'យល់ព្រម'),
        ]),
      ]),
    ]);
    document.body.append(overlay);
  });
};
Exam.confirm = (message) => Exam.modal(message);
Exam.notify = (message) => Exam.modal(message, { okOnly: true });
