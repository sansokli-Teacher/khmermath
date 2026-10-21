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

// the school's timetable: 11 teaching periods (the breaks 2/3, 4/5 and 6/7 are not periods)
export const SCHEDULE = [
  { n: 1, s: '07:30', e: '08:15' }, { n: 2, s: '08:20', e: '09:05' }, { n: 3, s: '09:25', e: '10:10' }, { n: 4, s: '10:15', e: '11:00' },
  { n: 5, s: '12:30', e: '13:15' }, { n: 6, s: '13:20', e: '14:05' }, { n: 7, s: '14:25', e: '15:10' }, { n: 8, s: '15:15', e: '16:00' },
  { n: 9, s: '16:10', e: '16:55' }, { n: 10, s: '17:10', e: '17:55' }, { n: 11, s: '18:10', e: '18:55' },
];
export const PERIODS = SCHEDULE.length;
const mins = (t) => { const [h, m] = t.split(':').map(Number); return h * 60 + m; };
// the period to record attendance for right now: the one running, or - in a break or gap - the next one; before the first: 1; after the last: the last
export function periodAt(d = new Date()) {
  const now = d.getHours() * 60 + d.getMinutes();
  for (const p of SCHEDULE) { if (now <= mins(p.e)) return p.n; }
  return SCHEDULE[SCHEDULE.length - 1].n;
}
export const isLive = (n, d = new Date()) => { const p = SCHEDULE[n - 1], now = d.getHours() * 60 + d.getMinutes(); return !!p && now >= mins(p.s) && now <= mins(p.e); };
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
