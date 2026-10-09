// Load test: N students take a 20-question exam at the same moment.
//   TEACHER_USER=owner TEACHER_PASS=... node test/load.mjs <base-url> [students=40] [questions=20]
// Creates a scratch class/test/session, runs every student through login → start → test → answers →
// heartbeats → submit, reports latency and errors, then deletes everything it created.
const [base = 'http://localhost:8799', nArg = '40', qArg = '20'] = process.argv.slice(2);
const N = Number(nArg), Q = Number(qArg), tag = `LOAD${Date.now().toString(36).slice(-4)}`;
const lat = {}; const errors = [];

class Client {
  constructor(device) { this.cookies = {}; this.device = device; }
  async call(path, { method = 'GET', body } = {}) {
    const t0 = performance.now();
    const res = await fetch(base + path, { method, headers: { 'Content-Type': 'application/json', 'X-Device': this.device, Cookie: Object.entries(this.cookies).map(([k, v]) => `${k}=${v}`).join('; ') }, body: body ? JSON.stringify(body) : undefined });
    for (const c of res.headers.getSetCookie?.() || []) { const [kv] = c.split(';'); const i = kv.indexOf('='); this.cookies[kv.slice(0, i)] = kv.slice(i + 1); }
    const data = await res.json().catch(() => ({}));
    const key = `${method} ${path.replace(/\/\d+/g, '/:id').replace(/\?.*/, '')}`;
    (lat[key] ||= []).push(performance.now() - t0);
    if (!res.ok) { const e = new Error(`${key} → ${res.status} ${data.error || ''}`); e.status = res.status; throw e; }
    return data;
  }
}
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const pct = (a, p) => { const s = [...a].sort((x, y) => x - y); return s[Math.min(s.length - 1, Math.floor(s.length * p))]; };

const teacher = new Client('teacher');
await teacher.call('/api/teacher/login', { method: 'POST', body: { username: process.env.TEACHER_USER, password: process.env.TEACHER_PASS } });
const cls = await teacher.call('/api/classes', { method: 'POST', body: { name: tag, grade: 7 } });
for (let i = 1; i <= N; i++) await teacher.call(`/api/classes/${cls.id}/students`, { method: 'POST', body: { id: `${tag}${String(i).padStart(3, '0')}`, surname: 'Load', first_name: String(i) } });
const test = await teacher.call('/api/tests', { method: 'POST', body: { title: `${tag} test` } });
for (let q = 1; q <= Q; q++) await teacher.call(`/api/tests/${test.id}/questions`, { method: 'POST', body: { stem_text: `Q${q}: ${q} + 1 = ?`, options: [String(q), String(q + 1), String(q + 2), String(q + 3)], correct_index: 1, points: 1, shuffle: q % 2 === 0, solution_text: 'x' } });
const start = new Date(Date.now() - 60000).toISOString(), end = new Date(Date.now() + 3600000).toISOString();
const ses = await teacher.call('/api/sessions', { method: 'POST', body: { test_id: test.id, class_id: cls.id, scheduled_start: start, scheduled_end: end, duration_minutes: 60, pin: '4321', integrity_mode: 'warn' } });
console.log(`seeded ${tag}: ${N} students × ${Q} questions, session ${ses.id}`);

async function student(i) {
  const id = `${tag}${String(i).padStart(3, '0')}`, c = new Client(`dev-${tag}-${i}`);
  try {
    await sleep(Math.random() * 3000);                                       // everybody types the PIN within ~3 seconds
    await c.call('/api/student/login', { method: 'POST', body: { id } });
    await c.call('/api/student/status');
    await c.call('/api/student/start', { method: 'POST', body: { session_id: ses.id, pin: '4321' } });
    const t = await c.call(`/api/student/test?session_id=${ses.id}`);
    const hb = setInterval(() => c.call(`/api/student/heartbeat?session_id=${ses.id}`).catch((e) => errors.push(e.message)), 4000);
    for (const q of t.questions) { await sleep(150 + Math.random() * 600); await c.call('/api/student/answer', { method: 'POST', body: { session_id: ses.id, question_id: q.id, selected_index: Math.floor(Math.random() * q.options.length) } }); }
    await c.call('/api/student/events', { method: 'POST', body: { session_id: ses.id, events: [{ kind: 'tab_hidden', dur_ms: 3000 }] } });
    clearInterval(hb);
    await c.call('/api/student/submit', { method: 'POST', body: { session_id: ses.id, submit_type: 'manual' } });
  } catch (e) { errors.push(`${id}: ${e.message}`); }
}
const t0 = performance.now();
await Promise.all(Array.from({ length: N }, (_, i) => student(i + 1)));
const secs = ((performance.now() - t0) / 1000).toFixed(1);

const roster = await teacher.call(`/api/sessions/${ses.id}`);
const submitted = roster.roster.filter((r) => r.submitted_at).length;
console.log(`\nfinished in ${secs}s — submitted ${submitted}/${N}, errors ${errors.length}`);
console.log('\nendpoint'.padEnd(44), 'n'.padStart(5), 'p50'.padStart(7), 'p95'.padStart(7), 'max'.padStart(7), ' (ms)');
for (const [k, a] of Object.entries(lat).sort()) console.log(k.padEnd(43), String(a.length).padStart(5), pct(a, .5).toFixed(0).padStart(7), pct(a, .95).toFixed(0).padStart(7), Math.max(...a).toFixed(0).padStart(7));
if (errors.length) console.log('\nfirst errors:\n' + errors.slice(0, 8).join('\n'));

await teacher.call(`/api/sessions/${ses.id}`, { method: 'DELETE' }).catch((e) => console.log('cleanup session:', e.message));
await teacher.call(`/api/tests/${test.id}`, { method: 'DELETE' }).catch((e) => console.log('cleanup test:', e.message));
await teacher.call(`/api/classes/${cls.id}`, { method: 'DELETE' }).catch((e) => console.log('cleanup class:', e.message));
process.exit(errors.length || submitted !== N ? 1 : 0);
