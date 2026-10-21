// Small shared helpers — no framework, plain globals (matches the rest of the khmermath.org tooling).
const Exam = {};

// One id per browser, so an exam started on one phone cannot be silently continued on another.
Exam.deviceId = function () {
  try {
    let d = localStorage.getItem('exam_device');
    if (!d) { d = (crypto.randomUUID ? crypto.randomUUID() : String(Math.random()).slice(2) + Date.now()); localStorage.setItem('exam_device', d); }
    return d;
  } catch { return 'nostorage'; }
};

Exam.api = async function (path, options = {}) {
  const res = await fetch(path, {
    method: options.method || 'GET',
    credentials: 'include',
    headers: {
      'X-Device': Exam.deviceId(),
      ...(options.body instanceof ArrayBuffer || options.body instanceof Blob
        ? { 'Content-Type': options.contentType || 'application/octet-stream' }
        : options.body ? { 'Content-Type': 'application/json' } : {}),
    },
    body: options.body
      ? (options.body instanceof ArrayBuffer || options.body instanceof Blob ? options.body : JSON.stringify(options.body))
      : undefined,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) { const e = new Error(data.error || `Request failed (${res.status})`); e.data = data; e.status = res.status; throw e; }
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
    el.appendChild(child instanceof Node ? child : document.createTextNode(String(child)));
  }
  return el;
};

// A question with variants shows one sample set of numbers where a single fixed version is needed (paper, preview).
Exam.withSample = (q) => (q.sample ? { ...q, ...q.sample } : q);

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
  if (!iso) return '—';
  let s = String(iso).trim();
  if (!s.includes('T') && s.includes(' ')) {
    s = s.replace(' ', 'T') + (s.includes('Z') ? '' : 'Z');
  }
  const d = new Date(s);
  if (isNaN(d.getTime())) return iso;
  return Exam.khDate(d) + ' · ' + Exam.khTime(d);
};

// Khmer dates and times written out ourselves: many browsers have no km-KH locale data and fall back to English («Oct 21, 2026, 7:14 AM»)
Exam.khDigits = (v) => String(v).replace(/\d/g, (c) => '០១២៣៤៥៦៧៨៩'[c]);
Exam.khDate = (d) => `${Exam.khDigits(d.getDate())} ${['មករា', 'កុម្ភៈ', 'មីនា', 'មេសា', 'ឧសភា', 'មិថុនា', 'កក្កដា', 'សីហា', 'កញ្ញា', 'តុលា', 'វិច្ឆិកា', 'ធ្នូ'][d.getMonth()]} ${Exam.khDigits(d.getFullYear())}`;
Exam.khTime = (d) => {
  const h = d.getHours(), h12 = h % 12 || 12, part = h < 12 ? 'ព្រឹក' : h < 17 ? 'រសៀល' : 'ល្ងាច';
  return `${Exam.khDigits(h12)}:${Exam.khDigits(String(d.getMinutes()).padStart(2, '0'))} ${part}`;
};

Exam.fmtTimeOnly = function (iso) {
  if (!iso) return '—';
  let s = String(iso).trim();
  if (!s.includes('T') && s.includes(' ')) {
    s = s.replace(' ', 'T') + (s.includes('Z') ? '' : 'Z');
  }
  const d = new Date(s);
  if (isNaN(d.getTime())) return iso;
  return Exam.khTime(d);
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

// One grading scale for the whole site (A ≥ 85 … F < 40), used for single exams,
// semester scores and the yearly statistics.
Exam.GRADES = ['A', 'B', 'C', 'D', 'E', 'F'];
Exam.gradeOf = function (pct) {
  if (pct == null || isNaN(pct)) return null;
  const p = Math.round(pct);
  if (p >= 85) return { grade: 'A', label: 'ល្អប្រសើរ', color: '#16a34a' };
  if (p >= 75) return { grade: 'B', label: 'ល្អណាស់', color: '#2563eb' };
  if (p >= 65) return { grade: 'C', label: 'ល្អ', color: '#0891b2' };
  if (p >= 50) return { grade: 'D', label: 'មធ្យម', color: '#d97706' };
  if (p >= 40) return { grade: 'E', label: 'ខ្សោយ', color: '#ea580c' };
  return { grade: 'F', label: 'ធ្លាក់', color: '#dc2626' };
};

// Installable app: register the (tiny) service worker.
if ('serviceWorker' in navigator && location.protocol === 'https:') {
  window.addEventListener('load', () => navigator.serviceWorker.register('/sw.js').catch(() => {}));
}

// 👁 show/hide button on every password box (also on boxes that appear later, e.g. in dialogs).
(function () {
  function addEye(input) {
    if (input.dataset.eye || input.closest('.pw-wrap') || input.id === 'f-pass') return;
    input.dataset.eye = '1';
    const wrap = document.createElement('div'); wrap.className = 'pw-wrap'; wrap.style.display = input.style.display || 'block';
    input.parentNode.insertBefore(wrap, input); wrap.appendChild(input);
    input.style.paddingRight = '44px'; input.style.width = '100%'; input.style.boxSizing = 'border-box';
    const b = document.createElement('button'); b.type = 'button'; b.className = 'pw-eye'; b.setAttribute('aria-label', 'បង្ហាញ/លាក់ពាក្យសម្ងាត់'); b.textContent = '👁';
    b.addEventListener('click', () => { const show = input.type === 'password'; input.type = show ? 'text' : 'password'; b.textContent = show ? '🙈' : '👁'; input.focus(); });
    wrap.appendChild(b);
  }
  const scan = (root) => (root || document).querySelectorAll('input[type=password]').forEach(addEye);
  const start = () => { scan(); new MutationObserver((m) => { for (const x of m) for (const n of x.addedNodes) if (n.nodeType === 1) { if (n.matches && n.matches('input[type=password]')) addEye(n); else scan(n); } }).observe(document.body, { childList: true, subtree: true }); };
  if (document.body) start(); else document.addEventListener('DOMContentLoaded', start);
})();
