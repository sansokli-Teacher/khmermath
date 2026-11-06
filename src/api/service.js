// Service API for report.khmermath.org (the school's control room). It is NOT for browsers: every call carries the shared
// key in `X-Service-Key` (secret SERVICE_KEY, set with `wrangler secret put SERVICE_KEY`; without it the whole API is off).
//   POST /api/service/provision  make or update a teacher (full plan), their classes and the students of each class
//   POST /api/service/sso        a one-minute sign-in link for that teacher (opened from the "Tests & exams" card)
//   GET  /api/sso?t=...          the link itself: checks the signature, sets the teacher cookie, goes to /teacher
import { json, err } from '../lib/http.js';
import { hashSecretValue, timingSafeEqual, randomKey } from '../lib/crypto.js';
import { createSessionCookie } from '../lib/session.js';
import { ensureColumns } from '../lib/schema.js';
import { allow } from '../lib/limits.js';
import { audit } from '../lib/audit.js';
import { sessionQuestions, mcqOnly } from '../lib/frozen.js';
import { isRight } from '../lib/scoring.js';

const USERNAME = /^[A-Za-z0-9_.\-]{3,30}$/;
const SSO_SECONDS = 60;
const b64u = (bytes) => btoa(String.fromCharCode(...bytes)).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
const clip = (v, n) => String(v == null ? '' : v).trim().slice(0, n);

async function hmac(secret, text) {
  const key = await crypto.subtle.importKey('raw', new TextEncoder().encode(secret), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  return b64u(new Uint8Array(await crypto.subtle.sign('HMAC', key, new TextEncoder().encode(text))));
}

// The service key, or nothing: with no key configured the endpoints answer 404 as if they did not exist.
async function needService(req, env) {
  if (!env.SERVICE_KEY || env.SERVICE_KEY.length < 24) return { resp: err('Not found.', 404) };
  const given = req.headers.get('X-Service-Key') || '';
  if (!timingSafeEqual(await hmac('svc', given), await hmac('svc', env.SERVICE_KEY))) {
    if (!(await allow(env, 'svc-bad', 20, 600))) return { resp: err('Too many attempts.', 429) };
    return { resp: err('Not allowed.', 403) };
  }
  return {};
}

function untilFor(row, months) {
  // from the current end (renewing early never loses time), or from now
  const cur = row && row.plan === 'full' && row.license_until ? new Date(row.license_until.replace(' ', 'T') + 'Z') : null;
  const base = cur && cur > new Date() ? cur : new Date();
  base.setUTCMonth(base.getUTCMonth() + months);
  return base.toISOString().replace('T', ' ').slice(0, 19);
}

const hasLicense = (row) => row.plan === 'full' && (!row.license_until || new Date(row.license_until.replace(' ', 'T') + 'Z') > new Date());

export async function provision(req, env) {
  const g = await needService(req, env); if (g.resp) return g.resp;
  await ensureColumns(env);
  const body = await req.json().catch(() => ({}));
  const username = clip(body.username, 30);
  const refId = clip(body.refId, 60);                       // the teacher's id in report: how an account is found again
  const name = clip(body.displayName, 60);
  const months = Math.min(Math.max(parseInt(body.months, 10) || 12, 1), 36);
  if (!USERNAME.test(username)) return err('username must be 3-30 letters, digits or _ . -', 400);
  if (!name) return err('displayName is required.', 400);
  if (!refId) return err('refId is required.', 400);

  const tag = `report:${refId}`;
  let t = await env.DB.prepare('SELECT id, username, role, plan, license_until FROM teachers WHERE ext_ref = ?1').bind(tag).first();
  let created = false;
  if (!t) {
    const same = await env.DB.prepare('SELECT id FROM teachers WHERE username = ?1 COLLATE NOCASE').bind(username).first();
    // a name already used by a different account (even the owner's) is never taken over
    if (same) return err('That username already belongs to another exam account.', 409);
    // an account nobody can sign in to with a password: the teacher comes in through the link, and may set a password later (reset link)
    const hash = await hashSecretValue(randomKey(), username, env.SESSION_SECRET);
    await env.DB.prepare("INSERT INTO teachers (username, password_hash, role, display_name, plan, license_until, ext_ref, created_at) VALUES (?1, ?2, 'teacher', ?3, 'full', ?4, ?5, datetime('now'))")
      .bind(username, hash, name, untilFor(null, months), tag).run();
    t = await env.DB.prepare('SELECT id, username, role, plan, license_until FROM teachers WHERE username = ?1').bind(username).first();
    created = true;
    await audit(env, null, 'service.teacher', `${username} ← ${tag}, ${months} months`);
  } else {
    if (t.role === 'owner' || t.role === 'admin') return err('Not allowed for this account.', 403);
    await env.DB.prepare('UPDATE teachers SET display_name = ?1, active = 1 WHERE id = ?2').bind(name, t.id).run();
    // the plan is given once, or again when it has run out: syncing a roster never stacks extra months
    if (!hasLicense(t) || body.renew === true) {
      await env.DB.prepare("UPDATE teachers SET plan = 'full', license_until = ?1 WHERE id = ?2").bind(untilFor(t, months), t.id).run();
      await audit(env, null, 'service.license', `${t.username}: +${months} months`);
    }
  }
  const lic = await env.DB.prepare('SELECT license_until FROM teachers WHERE id = ?1').bind(t.id).first();

  const out = [];
  for (const c of (Array.isArray(body.classes) ? body.classes : []).slice(0, 30)) {
    const cname = clip(c && c.name, 30);
    const grade = parseInt(c && c.grade, 10);
    if (!cname || !(grade >= 1 && grade <= 12)) { out.push({ name: cname, error: 'name and grade (1-12) are required' }); continue; }
    let cls = await env.DB.prepare('SELECT id FROM classes WHERE owner_id = ?1 AND name = ?2').bind(t.id, cname).first();
    if (!cls) {
      const r = await env.DB.prepare('INSERT INTO classes (name, grade, owner_id) VALUES (?1, ?2, ?3)').bind(cname, grade, t.id).run();
      cls = { id: r.meta.last_row_id };
    }
    let added = 0; const skipped = [];
    for (const s of (Array.isArray(c.students) ? c.students : []).slice(0, 200)) {
      const id = clip(s && s.id, 20), surname = clip(s && s.surname, 60), first = clip(s && s.firstName, 60);
      if (!id || !surname || !first) { skipped.push(id || '?'); continue; }
      // student ids are global (a student signs in with the id): never move one out of a class this teacher does not own
      const ex = await env.DB.prepare('SELECT s.class_id, c.owner_id FROM students s JOIN classes c ON c.id = s.class_id WHERE s.id = ?1').bind(id).first();
      if (ex && ex.class_id !== cls.id && ex.owner_id !== t.id) { skipped.push(id); continue; }
      await env.DB.prepare('INSERT INTO students (id, class_id, surname, first_name, gender, dob) VALUES (?1, ?2, ?3, ?4, ?5, ?6) ON CONFLICT(id) DO UPDATE SET class_id = ?2, surname = ?3, first_name = ?4, gender = ?5')
        .bind(id, cls.id, surname, first, clip(s.gender, 10) || null, clip(s.dob, 20) || null).run();
      added++;
    }
    out.push({ name: cname, examClassId: cls.id, students: added, skipped });
  }
  return json({ ok: true, created, teacherId: t.id, username: t.username, licenseUntil: lic.license_until, classes: out });
}

export async function sso(req, env) {
  const g = await needService(req, env); if (g.resp) return g.resp;
  const { refId } = await req.json().catch(() => ({}));
  const t = await env.DB.prepare('SELECT username, active, role FROM teachers WHERE ext_ref = ?1').bind(`report:${clip(refId, 60)}`).first();
  if (!t) return err('No exam account for this teacher yet.', 404);
  if (!t.active || t.role === 'owner' || t.role === 'admin') return err('Not allowed for this account.', 403);
  const body = b64u(new TextEncoder().encode(JSON.stringify({ u: t.username, n: randomKey().slice(0, 12), exp: Date.now() + SSO_SECONDS * 1000 })));
  const sig = await hmac(env.SESSION_SECRET + ':sso', body);
  return json({ url: `${new URL(req.url).origin}/api/sso?t=${body}.${sig}`, expiresIn: SSO_SECONDS });
}

export async function ssoLogin(req, env) {
  const tok = new URL(req.url).searchParams.get('t') || '';
  const [body, sig] = tok.split('.');
  const bad = () => new Response('តំណភ្ជាប់នេះផុតកំណត់ហើយ។ សូមចុចប៊ូតុងម្ដងទៀតពី report.khmermath.org', { status: 403, headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
  if (!body || !sig || !timingSafeEqual(sig, await hmac(env.SESSION_SECRET + ':sso', body))) return bad();
  let p; try { p = JSON.parse(new TextDecoder().decode(Uint8Array.from(atob(body.replace(/-/g, '+').replace(/_/g, '/')), (c) => c.charCodeAt(0)))); } catch { return bad(); }
  if (!p || !p.u || Date.now() > p.exp) return bad();
  // single use: the same link cannot be opened twice
  if (!(await allow(env, `sso:${p.n}`, 1, 120))) return bad();
  const t = await env.DB.prepare("SELECT username, active, role FROM teachers WHERE username = ?1 AND ext_ref LIKE 'report:%'").bind(p.u).first();
  if (!t || !t.active || t.role === 'owner' || t.role === 'admin') return bad();
  await env.DB.prepare("UPDATE teachers SET last_login = datetime('now') WHERE username = ?1").bind(t.username).run();
  const cookie = await createSessionCookie({ role: 'teacher', username: t.username }, env.SESSION_SECRET);
  return new Response(null, { status: 302, headers: { Location: '/teacher', 'Set-Cookie': cookie, 'Cache-Control': 'no-store' } });
}

// ---- results, read-only: what the teacher's classes sat, and one session's scores ----
async function teacherOf(env, refId) {
  return env.DB.prepare("SELECT id, active, role FROM teachers WHERE ext_ref = ?1").bind(`report:${clip(refId, 60)}`).first();
}

// POST /api/service/sessions {refId}: the newest test sessions in classes this teacher owns
export async function sessions(req, env) {
  const g = await needService(req, env); if (g.resp) return g.resp;
  await ensureColumns(env);
  const { refId } = await req.json().catch(() => ({}));
  const t = await teacherOf(env, refId);
  if (!t) return json({ sessions: [] });
  const { results } = await env.DB.prepare(
    `SELECT ts.id, ts.scheduled_start AS start, ts.status, c.name AS className, x.title,
            (SELECT COUNT(*) FROM results r WHERE r.session_id = ts.id AND r.submitted_at IS NOT NULL) AS submitted,
            (SELECT COUNT(*) FROM students s WHERE s.class_id = ts.class_id) AS roster
     FROM test_sessions ts JOIN classes c ON c.id = ts.class_id JOIN tests x ON x.id = ts.test_id
     WHERE c.owner_id = ?1 ORDER BY ts.scheduled_start DESC LIMIT 40`,
  ).bind(t.id).all();
  return json({ sessions: results });
}

// POST /api/service/results {refId, sessionId}: every student who handed in, with the MCQ and writing parts as the class report has them.
// A writing part that is not marked yet is null (and counted in `writingPending`), never 0.
export async function sessionResults(req, env) {
  const g = await needService(req, env); if (g.resp) return g.resp;
  await ensureColumns(env);
  const { refId, sessionId } = await req.json().catch(() => ({}));
  const t = await teacherOf(env, refId);
  if (!t) return err('No exam account for this teacher yet.', 404);
  const s = await env.DB.prepare(
    `SELECT ts.id, ts.scheduled_start AS start, c.name AS className, x.title FROM test_sessions ts JOIN classes c ON c.id = ts.class_id JOIN tests x ON x.id = ts.test_id
     WHERE ts.id = ?1 AND c.owner_id = ?2`,
  ).bind(Number(sessionId) || 0, t.id).first();
  if (!s) return err('Session not found.', 404);
  const { results: rows } = await env.DB.prepare(
    `SELECT st.id, st.surname, st.first_name AS firstName, r.mcq_score AS mcq, r.mcq_max AS mcqMax, r.writing_score AS writing, r.writing_max AS writingMax
     FROM results r JOIN students st ON st.id = r.student_id WHERE r.session_id = ?1 AND r.submitted_at IS NOT NULL ORDER BY st.surname, st.first_name`,
  ).bind(s.id).all();
  const mx = (k) => rows.reduce((m, r) => Math.max(m, Number(r[k]) || 0), 0);
  const hasWriting = rows.some((r) => r.writingMax != null && Number(r.writingMax) > 0);
  return json({
    sessionId: s.id, className: s.className, title: s.title, start: s.start,
    mcqMax: mx('mcqMax'), writingMax: hasWriting ? mx('writingMax') : null,
    writingPending: hasWriting ? rows.filter((r) => r.writing == null).length : 0,
    rows: rows.map((r) => ({ id: r.id, surname: r.surname, first: r.firstName, mcq: r.mcq, writing: hasWriting ? r.writing : null })),
  });
}

// POST /api/service/topics {refId, className, limit}: where a class is weak, by topic, from the closed questions of its newest tests.
// Per topic: the points earned out of the points possible for the class, and the same for each student. Writing questions and withdrawn
// ones are left out; questions with no topic are only counted (`untagged`). Only this teacher's own class.
export async function topics(req, env) {
  const g = await needService(req, env); if (g.resp) return g.resp;
  await ensureColumns(env);
  const { refId, className, limit } = await req.json().catch(() => ({}));
  const t = await teacherOf(env, refId);
  if (!t) return json({ sessions: [], topics: [], untagged: 0 });
  const { results: ses } = await env.DB.prepare(
    `SELECT ts.id, ts.test_id, ts.scheduled_start AS start, x.title FROM test_sessions ts JOIN classes c ON c.id = ts.class_id JOIN tests x ON x.id = ts.test_id
     WHERE c.owner_id = ?1 AND c.name = ?2 AND EXISTS (SELECT 1 FROM results r WHERE r.session_id = ts.id AND r.submitted_at IS NOT NULL)
     ORDER BY ts.scheduled_start DESC LIMIT ?3`,
  ).bind(t.id, clip(className, 80), Math.min(12, Math.max(1, Number(limit) || 6))).all();
  const by = {}; let untagged = 0;
  for (const s of ses) {
    const qs = mcqOnly(await sessionQuestions(env, s.id, s.test_id)).filter((q) => !q.cancelled);
    const { results: done } = await env.DB.prepare('SELECT student_id FROM results WHERE session_id = ?1 AND submitted_at IS NOT NULL').bind(s.id).all();
    const { results: rs } = await env.DB.prepare('SELECT student_id, question_id, selected_index FROM responses WHERE session_id = ?1').bind(s.id).all();
    const chosen = {};
    for (const r of rs) (chosen[r.student_id] ||= {})[r.question_id] = r.selected_index;
    for (const q of qs) {
      const name = clip(q.topic, 60);
      if (!name) { untagged++; continue; }
      const row = (by[name] ||= { name, questions: 0, students: {} });
      row.questions++;
      for (const d of done) {
        const st = (row.students[d.student_id] ||= { id: d.student_id, earned: 0, possible: 0 });
        const pts = Number(q.points) || 1;
        st.possible += pts; if (isRight(q, (chosen[d.student_id] || {})[q.id] ?? null)) st.earned += pts;
      }
    }
  }
  const list = Object.values(by).map((r) => {
    const students = Object.values(r.students);
    const earned = students.reduce((n, x) => n + x.earned, 0), possible = students.reduce((n, x) => n + x.possible, 0);
    return { name: r.name, questions: r.questions, pct: possible ? Math.round((earned / possible) * 1000) / 10 : null, students };
  }).filter((r) => r.pct !== null).sort((a, b) => a.pct - b.pct);
  return json({ sessions: ses.map((s) => ({ id: s.id, title: s.title, start: s.start })), topics: list, untagged });
}
