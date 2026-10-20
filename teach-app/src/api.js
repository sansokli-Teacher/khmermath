// Same-origin JSON API (session cookie). Mirrors Exam.api in public/js/common.js.
export async function api(path, { method = 'GET', body } = {}) {
  const res = await fetch(path, {
    method,
    credentials: 'include',
    headers: body ? { 'Content-Type': 'application/json' } : {},
    body: body ? JSON.stringify(body) : undefined,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const e = new Error(data.error || `Request failed (${res.status})`);
    e.status = res.status;
    throw e;
  }
  return data;
}

const KH = '០១២៣៤៥៦៧៨៩';
export const kh = (n) => String(n ?? '').replace(/\d/g, (d) => KH[d]);
export const fromKh = (s) => String(s ?? '').replace(/[០-៩]/g, (d) => String(KH.indexOf(d)));
export const gradeOf = (c) => fromKh(c && c.grade).replace(/\D/g, '') || String((c && c.grade) || '');
export const fullName = (s) => `${s.surname || ''} ${s.first_name || ''}`.trim();

export const todayISO = () => {
  const d = new Date();
  const p = (n) => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}`;
};

const loaded = new Map();
export function loadScript(src) {
  if (!loaded.has(src)) {
    loaded.set(src, new Promise((resolve, reject) => {
      const s = document.createElement('script');
      s.src = src;
      s.onload = resolve;
      s.onerror = () => { loaded.delete(src); reject(new Error(`Cannot load ${src}`)); };
      document.head.append(s);
    }));
  }
  return loaded.get(src);
}
