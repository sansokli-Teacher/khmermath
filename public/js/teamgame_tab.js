// «ហ្គេមក្រុម» tab: pick one of the teacher's own classes, split its students into teams, and open the team game with those teams.
// The roster comes from the class itself (no second list to keep). Students marked absent in the name wheel stay out of the teams.
let tgClassId = null, tgTeams = 4, tgSkipAbsent = true;

const tgShuffle = (a) => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
const tgKh = (n) => String(n).replace(/\d/g, (d) => '០១២៣៤៥៦៧៨៩'[d]);

// round-robin over a shuffled list keeps the team sizes within one student of each other
function tgSplit(names, n) {
  const teams = Array.from({ length: n }, () => []);
  tgShuffle(names).forEach((nm, i) => teams[i % n].push(nm));
  return teams;
}

// the three games the lobby offers (same questions, same lessons)
const TG_STYLES = [
  { k: 'cards', ic: '🃏', t: 'កាតបើក', d: 'ក្រុមផ្លាស់វេនជ្រើសប្រអប់លេខ ប្រយ័ត្នប្រអប់ពិសេស', img: 'img/play/teamgame.jpg' },
  { k: 'wheel', ic: '🎡', t: 'កង់វិល', d: 'បង្វិលកង់ ហើយកង់ជ្រើសសំណួរឱ្យ', img: 'img/play/wheel.jpg' },
  { k: 'boat', ic: '🚣', t: 'ប្រណាំងទូកង', d: 'ឆ្លើយត្រូវ ទូកទៅមុខ ដល់ទីបញ្ចប់មុនគេឈ្នះ', img: 'img/play/boat.jpg' },
];
const TG_COLORS = ['#e8590c', '#1c7ed6', '#2f9e44', '#ae3ec9', '#f08c00', '#0c8599', '#d6336c', '#5f3dc4'];
let tgStyle = 'cards', tgQn = 20, tgNoTeam = false;
let tgBank = null;

// ---- the «divide groups» pop-up: a banner, then each group is filled one by one (names shuffle, then lock with a crash and a burst) ----
let tgAudio = null, tgRun = 0;
const tgEsc = (t) => String(t).replace(/[&<>]/g, (m) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[m]));
function tgBeep(freqs, vol, len, gap) {
  try {
    tgAudio = tgAudio || new (window.AudioContext || window.webkitAudioContext)();
    freqs.forEach((f, i) => { const o = tgAudio.createOscillator(), g = tgAudio.createGain(), t = tgAudio.currentTime + i * (gap || 0.12); o.frequency.value = f; g.gain.setValueAtTime(vol, t); g.gain.exponentialRampToValueAtTime(0.001, t + len); o.connect(g); g.connect(tgAudio.destination); o.start(t); o.stop(t + len + 0.02); });
  } catch {}
}
function tgFireworks(cv, ms, burstsOnly) {
  if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const r = cv.parentElement.getBoundingClientRect(), dpr = Math.min(2, window.devicePixelRatio || 1);
  cv.width = r.width * dpr; cv.height = r.height * dpr; const g = cv.getContext('2d'); g.setTransform(dpr, 0, 0, dpr, 0, 0);
  let parts = [], next = 0; const end = performance.now() + ms, hues = [8, 40, 52, 130, 190, 280, 330];
  const burst = (x, y, n) => { const hu = hues[Math.floor(Math.random() * hues.length)]; for (let i = 0; i < n; i++) { const a = Math.PI * 2 * i / n + Math.random() * 0.2, v = 2.2 + Math.random() * 3.6; parts.push({ x, y, vx: Math.cos(a) * v, vy: Math.sin(a) * v, life: 1, h: hu + Math.random() * 30, w: 2 + Math.random() * 2 }); } };
  cv._burst = (x, y) => { burst(x, y, 30); if (!cv._on) loop(performance.now()); };
  const loop = (now) => {
    cv._on = true;
    g.globalCompositeOperation = 'destination-out'; g.fillStyle = 'rgba(0,0,0,.22)'; g.fillRect(0, 0, r.width, r.height); g.globalCompositeOperation = 'lighter';
    if (!burstsOnly && now < end && now >= next) { burst(r.width * (0.12 + Math.random() * 0.76), r.height * (0.1 + Math.random() * 0.5), 46); next = now + 380 + Math.random() * 260; }
    parts.forEach((q) => { q.x += q.vx; q.y += q.vy; q.vy += 0.05; q.vx *= 0.99; q.life -= 0.012; g.globalAlpha = Math.max(0, q.life); g.fillStyle = `hsl(${q.h} 95% 60%)`; g.beginPath(); g.arc(q.x, q.y, q.w, 0, Math.PI * 2); g.fill(); });
    g.globalAlpha = 1; g.globalCompositeOperation = 'source-over'; parts = parts.filter((q) => q.life > 0);
    if ((!burstsOnly && now < end) || parts.length) requestAnimationFrame(loop); else { cv._on = false; g.clearRect(0, 0, r.width, r.height); }
  };
  if (!burstsOnly) requestAnimationFrame(loop);
}
function tgDealPopup({ teams, colors, cname, redeal }) {
  const id = ++tgRun, n = teams.length, calm = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('.tgp-back').forEach((e) => e.remove());
  const total = teams.reduce((a, t) => a + t.length, 0), d = new Date();
  const date = `${tgKh(d.getDate())}/${tgKh(d.getMonth() + 1)}/${tgKh(d.getFullYear())}`;
  const back = h('div', { class: 'tgp-back' });
  back.innerHTML = `<div class="tgp-card" role="dialog" aria-modal="true"><div class="tgp-ban"><b class="tgp-title">កំពុងបែងចែកក្រុម…</b><small>${tgEsc(cname)}${cname ? ' · ' : ''}${tgKh(total)} នាក់ · ${date}</small></div>
    <div class="tgp-grid">${teams.map((t, k) => `<div class="tgp-g wait" style="--c:${colors[k % colors.length]}"><div class="tgp-gh"><b>ក្រុម ${tgKh(k + 1)}</b><span>${tgKh(t.length)} នាក់</span></div><ol>${t.map(() => '<li class="ph">• • •</li>').join('')}</ol></div>`).join('')}</div>
    <div class="tgp-act"><button type="button" class="tgp-skip">រំលង ▶▶</button><button type="button" class="tgp-again" hidden>🔀 ចែកម្ដងទៀត</button><button type="button" class="tgp-ok">បិទ</button></div><canvas class="tgp-fw" aria-hidden="true"></canvas></div>`;
  document.body.appendChild(back);
  const q = (c) => back.querySelector(c), cards = [...back.querySelectorAll('.tgp-g')], title = q('.tgp-title'), fw = q('.tgp-fw');
  const close = () => { tgRun++; back.remove(); document.removeEventListener('keydown', onKey); };
  const onKey = (e) => { if (e.key === 'Escape') close(); };
  document.addEventListener('keydown', onKey);
  back.onmousedown = (e) => { if (e.target === back) close(); };
  q('.tgp-ok').onclick = close;
  q('.tgp-again').onclick = () => { close(); redeal(); };
  const fill = (card, names) => { card.querySelector('ol').innerHTML = names.map((m) => `<li>${tgEsc(m)}</li>`).join(''); };
  const shuf = (a) => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  let remaining = teams.flat(), cur = -1, phase = 'start', t0 = 0, last = 0, skip = false;
  const per = calm ? 0 : Math.max(800, Math.min(1500, 9000 / Math.max(1, n))), pause = calm ? 0 : 380;
  q('.tgp-skip').onclick = () => { skip = true; };
  const lock = (i, fx) => {
    const card = cards[i]; card.className = 'tgp-g done'; fill(card, teams[i]);
    const ids = new Set(teams[i]); remaining = remaining.filter((m) => !ids.has(m));
    if (fx) { tgBeep([160, 120, 90], 0.14, 0.25, 0.05); const r = card.getBoundingClientRect(), w = fw.getBoundingClientRect(); tgFireworks(fw, 0, true); if (fw._burst) fw._burst(r.right - w.left - 30, r.top - w.top + 26); }
  };
  const finale = () => { title.textContent = 'បែងចែកក្រុមរួចរាល់! 🎉'; q('.tgp-skip').hidden = true; q('.tgp-again').hidden = false; tgBeep([523, 659, 784, 1047], 0.12, 0.3); tgFireworks(fw, 3600); };
  const frame = (now) => {
    if (id !== tgRun) return;
    if (skip) { for (let k = Math.max(cur, 0); k < n; k++) if (cards[k].className !== 'tgp-g done') lock(k, false); return finale(); }
    if (phase === 'start' || (phase === 'pause' && now - t0 >= pause)) {
      cur++; if (cur >= n) return finale();
      phase = 'roll'; t0 = now; cards[cur].className = 'tgp-g active'; title.textContent = `កំពុងបែងចែក ក្រុមទី ${tgKh(cur + 1)}…`;
      const gr = q('.tgp-grid'); gr.scrollTo({ top: Math.max(0, cards[cur].offsetTop - gr.offsetTop - 8), behavior: 'smooth' });
    }
    if (phase === 'roll') {
      if (now - t0 >= per) { lock(cur, true); phase = 'pause'; t0 = now; }
      else if (now - last > 80) { last = now; fill(cards[cur], shuf(remaining).slice(0, teams[cur].length)); tgBeep([700], 0.03, 0.02); }
    }
    requestAnimationFrame(frame);
  };
  if (calm) { cards.forEach((c, i) => lock(i, false)); finale(); } else requestAnimationFrame(frame);
}
async function tgLoadBank() {
  if (tgBank) return tgBank;
  for (const u of ['/api/game/bank', 'data/teamgame_g7.json']) {
    try { const r = await fetch(u); if (r.ok) { const d = await r.json(); if (d && d.lessons) return (tgBank = d.lessons); } } catch {}
  }
  return (tgBank = []);
}

render.teamgame = async function () {
  const root = document.getElementById('tab-teamgame');
  root.innerHTML = '';
  let classes;
  try { ({ classes } = await api('/api/classes')); } catch (e) { return root.appendChild(h('div', { class: 'error' }, e.message)); }

  const hubAfter = () => {
    // the two other games, which do not need teams
    root.appendChild(h('div', { class: 'tgl-more' }, [
      h('h3', {}, 'ហ្គេមផ្សេងទៀត'),
      h('div', { class: 'tgl-more-g' }, [
        h('div', { class: 'tgl-o' }, [h('b', {}, '📱 សំណួរផ្ទាល់លើទូរស័ព្ទ'), h('p', {}, 'សិស្សទាំងអស់ឆ្លើយលើទូរស័ព្ទក្នុងពេលតែមួយ ឆ្លើយលឿនបានពិន្ទុច្រើន មានតារាងចំណាត់ថ្នាក់ផ្ទាល់។'), h('button', { type: 'button', onclick: () => document.querySelector('[data-tab="live"]').click() }, 'បើកបន្ទប់ →')]),
        h('div', { class: 'tgl-o' }, [h('b', {}, '🎯 ប៊ីងហ្គោគណិតវិទ្យា'), h('p', {}, 'បោះពុម្ពកាតចម្លើយឱ្យសិស្សម្នាក់មួយសន្លឹក ហៅសំណួរម្តងមួយៗ សិស្សដោះស្រាយ រួចគូសចម្លើយលើកាត។ មិនត្រូវការទូរស័ព្ទ។'), h('a', { class: 'btn', href: 'bingo.html' }, 'បង្កើតកាត →')]),
      ]),
    ]));
  };
  if (!classes.length) {
    root.appendChild(h('div', { class: 'tgl' }, [
      h('p', {}, 'មិនទាន់មានថ្នាក់ទេ។ អ្នកអាចលេងដោយបង្កើតក្រុមដោយខ្លួនឯង ឬបង្កើតថ្នាក់ និងបញ្ចូលសិស្សនៅក្នុង «ថ្នាក់ និងសិស្ស» ជាមុន។'),
      h('a', { class: 'btn', href: 'teamgame.html' }, '▶ លេងហ្គេមដោយមិនមានថ្នាក់'),
    ]));
    hubAfter();
    return;
  }
  if (!classes.some((c) => c.id === tgClassId)) tgClassId = classes[0].id;

  const lobby = h('div', { class: 'tgl' });
  root.appendChild(lobby);
  const curCls = () => classes.find((c) => c.id === tgClassId) || classes[0];
  const gradeNow = () => parseInt(String(curCls().grade).replace(/[^\d]/g, ''), 10) || 7;
  let people = [], teams = [], lessons = [], picked = [];

  // ---- 1 · class + lessons ----
  const sel = h('select', { 'aria-label': 'ថ្នាក់' }, classes.map((c) => h('option', { value: c.id }, c.name)));
  sel.value = tgClassId;
  const lessonBox = h('div', { class: 'tgl-lessons' });
  const qnBox = h('div', { class: 'tgl-chips' });
  const allBtn = h('button', { type: 'button', class: 'tgl-ghost' }, 'ជ្រើសទាំងអស់');
  function drawLessons() {
    lessonBox.innerHTML = '';
    if (!lessons.length) { lessonBox.appendChild(h('p', { class: 'tgl-hint' }, `មិនទាន់មានសំណួរហ្គេមសម្រាប់ថ្នាក់ទី ${tgKh(gradeNow())} ទេ។`)); return; }
    let last = null; try { last = JSON.parse(localStorage.getItem(`teach_last_lesson_${tgClassId}`)); } catch {}
    const lastN = last && last.grade === gradeNow() ? (gradeNow() === 7 ? last.n : 100 * (gradeNow() - 7) + last.n) : null;
    lessons.forEach((L) => {
      const on = picked.includes(L.n);
      const b = h('button', { type: 'button', class: 'tgl-lesson' + (on ? ' on' : '') }, [h('span', {}, L.title), L.n === lastN ? h('small', {}, 'បានបង្រៀនចុងក្រោយ') : null]);
      b.onclick = () => { picked = on ? (picked.length > 1 ? picked.filter((x) => x !== L.n) : picked) : [...picked, L.n]; drawLessons(); drawBar(); };
      lessonBox.appendChild(b);
    });
  }
  const qIn = h('input', { type: 'number', min: '1', max: '100', 'aria-label': 'វាយចំនួនសំណួរ', placeholder: 'វាយចំនួន' });
  qIn.oninput = () => { const v = parseInt(qIn.value, 10); if (v >= 1) { tgQn = Math.min(100, v); drawQn(true); drawBar(); } };
  function drawQn(typing) {
    qnBox.innerHTML = '';
    [5, 10, 15, 20].forEach((n) => { const b = h('button', { type: 'button', class: tgQn === n ? 'on' : '' }, tgKh(n)); b.onclick = () => { tgQn = n; drawQn(); drawBar(); }; qnBox.appendChild(b); });
    if (!typing) qIn.value = [5, 10, 15, 20].includes(tgQn) ? '' : String(tgQn);
    qIn.classList.toggle('on', ![5, 10, 15, 20].includes(tgQn));
    qnBox.appendChild(qIn);
  }
  allBtn.onclick = () => { picked = lessons.map((L) => L.n); drawLessons(); drawBar(); };
  async function loadLessons() {
    lessons = (await tgLoadBank()).filter((L) => (L.g || 7) === gradeNow()).sort((a, b) => a.n - b.n);
    let last = null; try { last = JSON.parse(localStorage.getItem(`teach_last_lesson_${tgClassId}`)); } catch {}
    const want = last && last.grade === gradeNow() ? (gradeNow() === 7 ? last.n : 100 * (gradeNow() - 7) + last.n) : null;
    const hit = lessons.find((L) => L.n === want) || lessons[0];
    picked = hit ? [hit.n] : [];
    drawLessons(); drawBar();
  }

  // ---- 2 · game ----
  const styleBox = h('div', { class: 'tgl-styles' });
  function drawStyles() {
    styleBox.innerHTML = '';
    TG_STYLES.forEach((g) => {
      const b = h('button', { type: 'button', class: 'tgl-style' + (tgStyle === g.k ? ' on' : '') }, [
        h('img', { src: g.img, alt: '', loading: 'lazy' }), h('b', {}, `${g.ic} ${g.t}`), h('small', {}, g.d), h('i', { 'aria-hidden': 'true' }, '✓'),
      ]);
      b.onclick = () => { tgStyle = g.k; drawStyles(); drawBar(); };
      styleBox.appendChild(b);
    });
  }

  // ---- 3 · teams ----
  const out = h('output', {}, tgKh(tgTeams));
  const minus = h('button', { type: 'button', 'aria-label': 'បន្ថយ' }, '−');
  const plus = h('button', { type: 'button', 'aria-label': 'បន្ថែម' }, '+');
  const again = h('button', { type: 'button', class: 'tgl-deal' }, '👥 ចែកក្រុម');
  const absent = h('input', { type: 'checkbox', id: 'tg-skip' }); absent.checked = tgSkipAbsent;
  const noTeam = h('input', { type: 'checkbox' }); noTeam.checked = tgNoTeam;
  const info = h('p', { class: 'tgl-info' });
  const preview = h('div', { class: 'tgl-teams' });
  function draw() {
    for (let k = TG_COLORS.length - 1; k > 0; k--) { const j = Math.floor(Math.random() * (k + 1)); [TG_COLORS[k], TG_COLORS[j]] = [TG_COLORS[j], TG_COLORS[k]]; }   // a new random colour set for every deal
    tgTeams = Math.max(2, Math.min(8, tgTeams));
    out.textContent = tgKh(tgTeams); minus.disabled = tgTeams <= 2 || tgNoTeam; plus.disabled = tgTeams >= 8 || tgNoTeam; again.disabled = tgNoTeam;
    let off = [];
    try { off = (JSON.parse(localStorage.getItem(`exam_wheel_${tgClassId}`)) || {}).off || []; } catch {}
    const names = people.filter((p) => !(absent.checked && off.includes(p.id))).map((p) => p.n);
    teams = tgSplit(names, Math.min(tgTeams, Math.max(1, names.length)));
    info.textContent = tgNoTeam ? `សិស្ស ${tgKh(names.length)} នាក់ · លេងដោយគ្មានក្រុម` : `សិស្ស ${tgKh(names.length)} នាក់${absent.checked && off.length ? ` (មិនរួមអ្នកអវត្តមាន ${tgKh(people.length - names.length)} នាក់)` : ''} → ${tgKh(teams.length)} ក្រុម`;
    preview.innerHTML = ''; preview.hidden = tgNoTeam;
    teams.forEach((m, i) => preview.appendChild(h('div', { class: 'tgl-team', style: `--c:${TG_COLORS[i % TG_COLORS.length]}` }, [
      h('div', { class: 'tgl-th' }, [h('b', {}, `ក្រុមទី ${tgKh(i + 1)}`), h('span', {}, `${tgKh(m.length)} នាក់`)]),
      h('p', {}, m.join(' · ') || '—'),
    ])));
    drawBar();
  }
  minus.onclick = () => { tgTeams--; draw(); }; plus.onclick = () => { tgTeams++; draw(); };
  const deal = () => { draw(); if (teams.some((t) => t.length)) tgDealPopup({ teams, colors: TG_COLORS.slice(), cname: curCls().name, redeal: deal }); else Exam.notify('ថ្នាក់នេះមិនទាន់មានសិស្សទេ។'); };
  again.onclick = deal;
  absent.onchange = () => { tgSkipAbsent = absent.checked; draw(); };
  noTeam.onchange = () => { tgNoTeam = noTeam.checked; draw(); };

  // ---- start bar ----
  const sum = h('div', { class: 'tgl-sum' });
  const go = h('button', { type: 'button', class: 'tgl-go' }, '▶ ចាប់ផ្ដើមហ្គេម');
  function drawBar() {
    const g = TG_STYLES.find((x) => x.k === tgStyle);
    sum.textContent = [curCls().name, picked.length ? `${tgKh(picked.length)} មេរៀន` : null, g.t, tgNoTeam ? 'គ្មានក្រុម' : `${tgKh(teams.length)} ក្រុម`, `${tgKh(tgQn)} សំណួរ`].filter(Boolean).join(' · ');
    go.disabled = !picked.length;
  }
  go.onclick = () => {
    if (!tgNoTeam && !teams.some((t) => t.length)) return Exam.notify('ថ្នាក់នេះមិនទាន់មានសិស្សទេ។');
    try { localStorage.setItem('km_wheel_last_groups', JSON.stringify({ cls: curCls().name, groups: teams })); } catch {}
    location.href = `teamgame.html?wiz=1&import=1&style=${tgStyle}&grade=${gradeNow()}&l=${picked.join(',')}&n=${tgQn}${tgNoTeam ? '&nt=1' : ''}`;
  };

  const step = (n, title, body, right) => h('section', { class: 'tgl-step' }, [h('div', { class: 'tgl-sh' }, [h('span', { class: 'tgl-n' }, tgKh(n)), h('h3', {}, title), right || null]), body]);
  lobby.append(
    step(1, 'ថ្នាក់ និងមេរៀន', h('div', { class: 'tgl-body' }, [
      h('label', { class: 'tgl-f' }, [h('span', {}, 'ថ្នាក់'), sel]),
      lessonBox,
      h('div', { class: 'tgl-qn' }, [h('span', {}, 'ចំនួនសំណួរ'), qnBox]),
    ]), allBtn),
    step(2, 'ជ្រើសហ្គេម', styleBox),
    step(3, 'ក្រុម', h('div', { class: 'tgl-body' }, [
      h('div', { class: 'tgl-trow' }, [
        h('div', { class: 'tgl-stepper' }, [minus, out, plus]), again,
        h('label', { class: 'tgl-sw' }, [absent, h('span', {}, 'មិនរួមសិស្សអវត្តមាន')]),
        h('label', { class: 'tgl-sw' }, [noTeam, h('span', {}, '🙋 លេងដោយគ្មានក្រុម')]),
      ]),
      info, preview,
    ])),
    h('div', { class: 'tgl-bar' }, [sum, h('a', { class: 'tgl-link', href: 'teamgame.html' }, 'លេងដោយមិនមានថ្នាក់'), go]),
  );
  sel.onchange = () => { tgClassId = Number(sel.value) || sel.value; loadClass(); loadLessons(); };
  async function loadClass() {
    const { students } = await api(`/api/classes/${tgClassId}/students`);
    people = students.map((s) => ({ id: s.id, n: `${s.surname || ''} ${s.first_name || ''}`.trim() })).filter((p) => p.n);
    draw();
  }
  drawStyles(); drawQn(); hubAfter();
  await Promise.all([loadClass(), loadLessons()]);
};
