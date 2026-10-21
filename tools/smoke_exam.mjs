// End-to-end smoke test of an exam day against a running server (local `wrangler dev` or a staging copy; never point it at the live site):
//   node tools/smoke_exam.mjs http://localhost:8799 teacherUser teacherPass classId studentId testId
// Teacher schedules → student logs in, starts, answers, is locked by the teacher → teacher unlocks (time given back) → student submits → result is there.
const [base = 'http://localhost:8799', tu = 'auditfull', tp = 'password123', classId = '6', studentId = 'A101', testId = '20'] = process.argv.slice(2);
if (/exam\.khmermath\.org/.test(base)) { console.error('Refusing to run against the live site.'); process.exit(1); }
const jar = { t: '', s: '' };
const call = async (who, method, path, body) => {
  const r = await fetch(base + path, { method, headers: { 'content-type': 'application/json', cookie: jar[who] }, body: body ? JSON.stringify(body) : undefined });
  const sc = r.headers.getSetCookie ? r.headers.getSetCookie() : []; if (sc.length) jar[who] = sc.map((c) => c.split(';')[0]).join('; ');
  const d = await r.json().catch(() => ({})); return { s: r.status, d };
};
let fails = 0; const ok = (c, m) => { console.log(c ? '  ✓' : '  ✗', m); if (!c) fails++; };
const T = (m, p, b) => call('t', m, p, b), S = (m, p, b) => call('s', m, p, b);

console.log('teacher schedules the exam');
ok((await T('POST', '/api/teacher/login', { username: tu, password: tp })).s === 200, 'teacher login');
const ses = await T('POST', '/api/sessions', { test_id: Number(testId), class_id: Number(classId), scheduled_start: new Date(Date.now() - 60000).toISOString(), duration_minutes: 30, pin: '4321', integrity_mode: 'lock', max_violations: 3 });
ok(ses.s === 200 && ses.d.id, `session ${ses.d.id} created`);
const sid = ses.d.id;
console.log('student takes it');
ok((await S('POST', '/api/student/login', { id: studentId })).s === 200, 'student login');
ok((await S('POST', '/api/student/start', { session_id: sid, pin: '0000' })).s === 401, 'wrong PIN refused');
ok((await S('POST', '/api/student/start', { session_id: sid, pin: '4321' })).d.ok, 'PIN accepted, test started');
const qs = await S('GET', `/api/student/test?session_id=${sid}`);
const mcq = (qs.d.questions || []).filter((q) => q.kind !== 'writing');
ok(mcq.length > 0, `${mcq.length} questions loaded`);
ok((await S('POST', '/api/student/answer', { session_id: sid, question_id: mcq[0].id, selected_index: 1 })).s === 200, 'answer saved');
ok((await S('GET', `/api/student/heartbeat?session_id=${sid}`)).d.open === true, 'heartbeat open');
console.log('three incidents lock the student; a phone long-press does not count');
const ev = (kind, detail) => S('POST', '/api/student/events', { session_id: sid, events: [{ kind, detail, t: Date.now() }] });
await ev('contextmenu');                                    // node's fetch sends no phone user agent, so this one counts like a desktop right-click
let last; for (const k of ['shortcut', 'copy']) { await new Promise((r) => setTimeout(r, 3100)); last = await ev(k, 'x'); }
ok(last.d.locked === true, 'locked after 3 incidents');
ok((await S('GET', `/api/student/heartbeat?session_id=${sid}`)).d.locked === true, 'student sees the lock');
console.log('teacher unlocks: the locked minutes come back');
const un = await T('POST', `/api/sessions/${sid}/lock`, { student_id: studentId, locked: false });
ok(un.d.ok && un.d.given_back >= 1, `unlocked, ${un.d.given_back} min given back`);
console.log('student submits');
const sub = await S('POST', '/api/student/submit', { session_id: sid });
ok(sub.s === 200, 'submitted');
ok((await S('POST', '/api/student/answer', { session_id: sid, question_id: mcq[0].id, selected_index: 2 })).s !== 200, 'no answers accepted after submitting');
console.log('teacher resets an accidental submit');
ok((await T('POST', `/api/sessions/${sid}/reset-student`, { student_id: studentId })).s === 200, 'reset while the exam is open');
console.log(fails ? `\n${fails} check(s) FAILED` : '\nall checks passed'); process.exit(fails ? 1 : 0);
