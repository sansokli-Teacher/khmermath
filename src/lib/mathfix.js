// A lost backslash (\alpha, \tan, \times, \frac, \text ... written without escaping) turns into a hidden control character (BEL, tab, form feed ...)
// and the maths then fails to show. Anything saved through the test and bank API is repaired here, so the damage can not come back.
const MAP = { '\x07': '\\a', '\x08': '\\b', '\x09': '\\t', '\x0b': '\\v', '\x0c': '\\f' };
export const fixControlChars = (s) => (typeof s === 'string' ? s.replace(/[\x07\x08\x09\x0b\x0c]/g, (c) => MAP[c]) : s);
export function cleanDeep(v) {
  if (typeof v === 'string') return fixControlChars(v);
  if (Array.isArray(v)) return v.map(cleanDeep);
  if (v && typeof v === 'object') { const o = {}; for (const k of Object.keys(v)) o[k] = cleanDeep(v[k]); return o; }
  return v;
}
// a request whose json() comes back repaired
export function repairedJson(req) {
  return new Proxy(req, {
    get(t, k) {
      if (k === 'json') return async () => cleanDeep(await t.json());
      const v = t[k];
      return typeof v === 'function' ? v.bind(t) : v;
    },
  });
}
