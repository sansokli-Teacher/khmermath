// Name wheel for the teacher: picks a student from one of the teacher's own classes (no second list to keep).
// Gender comes from the class roster. Absent / already-picked marks are remembered per class in this browser only.
const WHEEL_PALETTES = {
  a: ['ពណ៌ស្រស់', ['#e8590c', '#1c7ed6', '#2f9e44', '#ae3ec9', '#f08c00', '#0c8599', '#d6336c', '#5f3dc4']],
  b: ['ទឹកសមុទ្រ', ['#0b7285', '#1971c2', '#1098ad', '#3b5bdb', '#0c8599', '#364fc7', '#1864ab', '#0b7285']],
  c: ['ភ្លើងក្ដៅ', ['#e8590c', '#f08c00', '#e03131', '#c2255c', '#d9480f', '#c92a2a', '#e67700', '#a61e4d']],
  d: ['ព្រៃបៃតង', ['#2b8a3e', '#2f9e44', '#087f5b', '#5c940d', '#0b7285', '#66a80f', '#099268', '#37b24d']],
  e: ['ជាតិខ្មែរ', ['#032ea1', '#e00025', '#032ea1', '#e00025', '#032ea1', '#e00025']],
};
// settings are shared by all classes and kept in this browser
const wheelSettings = (() => {
  let s = { dur: 5, theme: 'a', fw: true, mystery: false, speak: false };
  try { s = Object.assign(s, JSON.parse(localStorage.getItem('exam_wheel_set'))); } catch {}
  return s;
})();
const wheelSaveSettings = () => { try { localStorage.setItem('exam_wheel_set', JSON.stringify(wheelSettings)); } catch {} };
let wheelClassId = null;

const whGender = (g) => (/^(ស្រី|f|female|girl)$/i.test(String(g || '').trim()) ? 'f' : /^(ប្រុស|m|male|boy)$/i.test(String(g || '').trim()) ? 'm' : '');
const whShuffle = (a) => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
// Excel export of the picked-student results (SheetJS is already loaded on the teacher page).
const whSheetName = (n, used) => { const b = String(n).replace(/[\\/?*[\]:]/g, '').slice(0, 28) || 'Sheet'; let out = b, k = 1; while (used[out]) out = `${b}_${++k}`; used[out] = 1; return out; };
function whAddSheets(wb, used, label, people, mem) {
  const cnt = {}; for (const x of mem.hist || []) cnt[x.n] = (cnt[x.n] || 0) + 1;
  const gw = (g) => (g === 'f' ? 'ស្រី' : g === 'm' ? 'ប្រុស' : '');
  const by = {}; people.forEach((p) => { by[p.n] = p; });
  const pad = (n) => String(n).padStart(2, '0');
  const stamp = (t) => { const d = new Date(t); return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`; };
  const sum = XLSX.utils.aoa_to_sheet([['ល.រ', 'លេខសម្គាល់', 'ឈ្មោះសិស្ស', 'ភេទ', 'ចំនួនដងដែលត្រូវបានជ្រើស', 'វត្តមាន'],
    ...people.map((p, i) => [i + 1, p.id, p.n, gw(p.g), cnt[p.n] || 0, (mem.off || []).includes(p.id) ? 'អវត្តមាន' : 'មាន'])]);
  sum['!cols'] = [{ wch: 6 }, { wch: 12 }, { wch: 30 }, { wch: 8 }, { wch: 22 }, { wch: 12 }];
  const ord = XLSX.utils.aoa_to_sheet([['ល.រ', 'ឈ្មោះសិស្ស', 'ភេទ', 'កាលបរិច្ឆេទ និងម៉ោង'],
    ...(mem.hist || []).map((x, i) => [i + 1, x.n, by[x.n] ? gw(by[x.n].g) : '', stamp(x.t)])]);
  ord['!cols'] = [{ wch: 6 }, { wch: 30 }, { wch: 8 }, { wch: 22 }];
  XLSX.utils.book_append_sheet(wb, sum, whSheetName(label ? `${label} សរុប` : 'សរុប', used));
  XLSX.utils.book_append_sheet(wb, ord, whSheetName(label ? `${label} លំដាប់` : 'តាមលំដាប់', used));
}
const whKh = (n) => String(n).replace(/\d/g, (d) => '០១២៣៤៥៦៧៨៩'[d]);

render.wheel = async function () {
  const root = document.getElementById('tab-wheel');
  root.innerHTML = '';
  let classes;
  try { ({ classes } = await api('/api/classes')); } catch (e) { return root.appendChild(h('div', { class: 'error' }, e.message)); }
  if (!classes.length) return root.appendChild(h('div', { class: 'card' }, 'មិនទាន់មានថ្នាក់ទេ។ សូមបង្កើតថ្នាក់ និងបញ្ចូលសិស្សនៅក្នុង «ថ្នាក់ និងសិស្ស» ជាមុនសិន។'));
  if (!classes.some((c) => c.id === wheelClassId)) wheelClassId = classes[0].id;

  const sel = h('select', { 'aria-label': 'ថ្នាក់' }, classes.map((c) => h('option', { value: c.id }, c.name)));
  sel.value = wheelClassId;
  sel.onchange = () => { wheelClassId = Number(sel.value) || sel.value; render.wheel(); };
  const { students } = await api(`/api/classes/${wheelClassId}/students`);
  const people = students.map((s) => ({ id: s.id, n: `${s.surname || ''} ${s.first_name || ''}`.trim(), g: whGender(s.gender) }));

  const KEY = `exam_wheel_${wheelClassId}`;
  let mem = { off: [], done: [], hist: [] };
  try { mem = Object.assign(mem, JSON.parse(localStorage.getItem(KEY))); } catch {}
  const save = () => { try { localStorage.setItem(KEY, JSON.stringify(mem)); } catch {} };
  let noRepeat = true, sound = true, spinning = false, angle = 0, frozen = null, current = null, audio = null, lastText = '', gFilter = '', ord = null, pendingReveal = false, tally = false, voiceKm = null;
  const isOff = (p) => mem.off.includes(p.id);
  const eligible = () => {
    const l = people.filter((p) => !isOff(p) && !(noRepeat && mem.done.includes(p.id)) && (!gFilter || p.g === gFilter));
    return ord ? l.sort((a, b) => (ord[a.id] || 0) - (ord[b.id] || 0)) : l;
  };
  const present = () => people.filter((p) => !isOff(p));
  const mark = (p) => (p.g === 'f' ? '♀ ' : p.g === 'm' ? '♂ ' : '');

  const canvas = h('canvas', { width: '720', height: '720', 'aria-label': 'កង់ឈ្មោះសិស្ស' });
  const ctx = canvas.getContext('2d');
  const fw = h('canvas', { class: 'wheel-fw', 'aria-hidden': 'true' });
  const spinBtn = h('button', { class: 'wheel-hub', 'aria-label': 'បង្វិលកង់' }, 'បង្វិល');
  const msg = h('div', { class: 'notice', hidden: '' });
  const winner = h('b', {});
  const againBtn = h('button', { class: 'btn-sm' }, 'បង្វិលម្ដងទៀត');
  const absentBtn = h('button', { class: 'secondary btn-sm' }, 'អវត្តមាន — ដកចេញ');
  const closeBtn = h('button', { class: 'secondary btn-sm' }, 'បិទ');
  const revealBtn = h('button', { class: 'btn-sm', hidden: '' }, 'បង្ហាញឈ្មោះ');
  const sayBtn = h('button', { class: 'secondary btn-sm', hidden: '' }, '🔊 អាន');
  const popSmall = h('small', {}, 'សិស្សដែលត្រូវបានជ្រើស');
  const pop = h('div', { class: 'wheel-pop', role: 'dialog', 'aria-modal': 'true', hidden: '' },
    h('div', { class: 'wheel-pop-card' }, [popSmall, winner, h('div', { class: 'row wheel-tools' }, [revealBtn, sayBtn, againBtn, absentBtn, closeBtn])]));
  const chips = h('div', { class: 'wheel-chips' });
  const count = h('span', { class: 'muted' });
  const gsum = h('p', { class: 'muted', style: 'font-size:14px;margin:0' });
  const groupsBox = h('div', { class: 'wheel-groups', hidden: '' });
  const copyBtn = h('button', { class: 'secondary btn-sm', hidden: '' }, 'ចម្លងលទ្ធផល');
  const speakRow = h('label', { class: 'wheel-chk', hidden: '' });

  function draw() {
    const list = frozen || eligible(), n = list.length, W = canvas.width, c = W / 2, r = c - 6;
    ctx.clearRect(0, 0, W, W); ctx.save(); ctx.translate(c, c); ctx.rotate(angle);
    if (!n) { ctx.beginPath(); ctx.arc(0, 0, r, 0, 7); ctx.fillStyle = '#cfd6dd'; ctx.fill(); }
    else {
      const a = Math.PI * 2 / n;
      for (let i = 0; i < n; i++) {
        ctx.beginPath(); ctx.moveTo(0, 0); ctx.arc(0, 0, r, i * a - Math.PI / 2 - a / 2, i * a - Math.PI / 2 + a / 2); ctx.closePath();
        const pal = (WHEEL_PALETTES[wheelSettings.theme] || WHEEL_PALETTES.a)[1]; ctx.fillStyle = pal[i % pal.length]; ctx.fill();
        if (n > 1) { ctx.strokeStyle = 'rgba(255,255,255,.7)'; ctx.lineWidth = 2; ctx.stroke(); }
        ctx.save(); ctx.rotate(i * a - Math.PI / 2);
        ctx.font = `600 ${Math.max(13, Math.min(36, Math.floor(r * a * 0.6)))}px "Kantumruy Pro", "Noto Sans Khmer", sans-serif`;
        ctx.fillStyle = '#fff'; ctx.textAlign = 'right'; ctx.textBaseline = 'middle'; ctx.shadowColor = 'rgba(0,0,0,.35)'; ctx.shadowBlur = 3;
        let name = list[i].n; const maxW = r * 0.7;
        while (ctx.measureText(name).width > maxW && name.length > 2) name = name.slice(0, -1);
        if (name !== list[i].n) name += '…';
        ctx.fillText(name, r - 16, 0); ctx.restore();
      }
    }
    ctx.restore();
  }
  const redraw = () => { frozen = null; draw(); };
  function beep(freqs, vol, len) {
    if (!sound) return;
    try {
      audio = audio || new (window.AudioContext || window.webkitAudioContext)();
      freqs.forEach((f, i) => { const o = audio.createOscillator(), g = audio.createGain(), t = audio.currentTime + i * 0.13;
        o.frequency.value = f; g.gain.setValueAtTime(vol, t); g.gain.exponentialRampToValueAtTime(0.001, t + len);
        o.connect(g); g.connect(audio.destination); o.start(t); o.stop(t + len + 0.02); });
    } catch {}
  }
  let fwRun = 0;
  function fireworks() {
    if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    const dpr = Math.min(2, window.devicePixelRatio || 1), W = fw.clientWidth, H = fw.clientHeight;
    fw.width = W * dpr; fw.height = H * dpr;
    const g = fw.getContext('2d'); g.setTransform(dpr, 0, 0, dpr, 0, 0);
    let parts = [], nextBurst = 0; const end = performance.now() + 3600, id = ++fwRun, hues = [8, 40, 52, 130, 190, 280, 330];
    const burst = (x, y) => { const hue = hues[Math.floor(Math.random() * hues.length)]; for (let i = 0; i < 46; i++) { const a = Math.PI * 2 * i / 46 + Math.random() * 0.2, v = 2.2 + Math.random() * 3.6; parts.push({ x, y, vx: Math.cos(a) * v, vy: Math.sin(a) * v, life: 1, hue: hue + Math.random() * 25 - 12 }); } };
    const frame = (now) => {
      if (id !== fwRun) return;
      g.globalCompositeOperation = 'destination-out'; g.fillStyle = 'rgba(0,0,0,.22)'; g.fillRect(0, 0, W, H); g.globalCompositeOperation = 'lighter';
      if (now < end && now > nextBurst) { burst(W * (0.12 + Math.random() * 0.76), H * (0.1 + Math.random() * 0.45)); nextBurst = now + 260 + Math.random() * 260; }
      parts = parts.filter((p) => p.life > 0.02);
      for (const p of parts) { p.x += p.vx; p.y += p.vy; p.vy += 0.06; p.vx *= 0.985; p.vy *= 0.985; p.life -= 0.013; g.fillStyle = `hsla(${p.hue},100%,60%,${Math.max(0, p.life)})`; g.beginPath(); g.arc(p.x, p.y, 2.6, 0, 7); g.fill(); }
      if (now < end || parts.length) requestAnimationFrame(frame); else g.clearRect(0, 0, W, H);
    };
    requestAnimationFrame(frame);
  }
  const closePop = () => { pop.hidden = true; pendingReveal = false; fwRun++; fw.getContext('2d').clearRect(0, 0, fw.width, fw.height); if (window.speechSynthesis) speechSynthesis.cancel(); };
  const findVoice = () => { if (window.speechSynthesis) voiceKm = speechSynthesis.getVoices().find((v) => /^km/i.test(v.lang)) || null; speakRow.hidden = !voiceKm; };
  const say = () => { if (!voiceKm || !current) return; try { speechSynthesis.cancel(); const u = new SpeechSynthesisUtterance(current.n); u.voice = voiceKm; u.lang = voiceKm.lang; speechSynthesis.speak(u); } catch {} };
  const celebrate = () => { if (wheelSettings.fw) { beep([523, 659, 784, 1047], 0.08, 0.3); fireworks(); } if (wheelSettings.speak) say(); };
  const openPop = () => {
    winner.textContent = pendingReveal ? '?' : current.n; popSmall.textContent = `សិស្សដែលត្រូវបានជ្រើស · លើកទី ${whKh(mem.hist.length)}`;
    revealBtn.hidden = !pendingReveal; againBtn.hidden = pendingReveal; absentBtn.hidden = pendingReveal; sayBtn.hidden = pendingReveal || !voiceKm;
    pop.hidden = false; (pendingReveal ? revealBtn : againBtn).focus({ preventScroll: true });
  };
  const reveal = () => { pendingReveal = false; winner.textContent = current.n; revealBtn.hidden = true; againBtn.hidden = false; absentBtn.hidden = false; sayBtn.hidden = !voiceKm; celebrate(); };
  const finish = (student) => {
    current = student; if (noRepeat && !mem.done.includes(current.id)) mem.done.push(current.id);
    mem.hist.push({ n: current.n, t: Date.now() }); if (mem.hist.length > 300) mem.hist.shift(); save();
    renderHist(); refresh(); pendingReveal = !!wheelSettings.mystery; openPop(); if (!pendingReveal) celebrate();
  };
  const histCounts = () => { const c = {}; for (const x of mem.hist) c[x.n] = (c[x.n] || 0) + 1; return c; };
  const histList = h('ol', { class: 'wheel-hist' });
  const histCount = h('span', { class: 'muted' });
  function renderHist() {
    histList.innerHTML = ''; histList.classList.toggle('tally', tally);
    histCount.textContent = mem.hist.length ? `(${mem.hist.length})` : '';
    if (!mem.hist.length) return histList.appendChild(h('li', { class: 'muted', style: 'list-style:none' }, 'មិនទាន់មានលទ្ធផលទេ។'));
    if (tally) { const c = histCounts(); Object.keys(c).sort((a, b) => c[b] - c[a]).forEach((n) => histList.appendChild(h('li', {}, [n, h('span', { class: 'cnt' }, `${c[n]} ដង`)]))); }
    else [...mem.hist].reverse().forEach((x, i) => { const t = new Date(x.t); histList.appendChild(h('li', { value: String(mem.hist.length - i) }, [x.n, h('small', { class: 'muted' }, ` ${String(t.getHours()).padStart(2, '0')}:${String(t.getMinutes()).padStart(2, '0')}`)])); });
  }

  function refresh() {
    const list = eligible();
    msg.hidden = !!list.length || spinning;
    msg.textContent = !people.length ? 'ថ្នាក់នេះមិនទាន់មានសិស្សទេ។ សូមបញ្ចូលសិស្សនៅក្នុង «ថ្នាក់ និងសិស្ស»។'
      : gFilter && !people.some((p) => p.g === gFilter) ? 'មិនទាន់មានភេទនេះក្នុងបញ្ជីថ្នាក់ទេ។ សូមកំណត់ភេទសិស្សនៅក្នុង «ថ្នាក់ និងសិស្ស»។'
      : noRepeat && people.some((p) => !isOff(p)) ? 'សិស្សទាំងអស់ត្រូវបានជ្រើសហើយ។ ចុច «ចាប់ផ្ដើមជុំថ្មី»។' : 'សិស្សទាំងអស់អវត្តមាន។';
    spinBtn.disabled = spinning || !list.length;
    chips.innerHTML = '';
    for (const p of people) {
      const off = isOff(p), done = noRepeat && mem.done.includes(p.id);
      chips.appendChild(h('button', { type: 'button', class: `wheel-chip secondary${off ? ' off' : ''}${done ? ' done' : ''}${p.g ? ` g-${p.g}` : ''}`, title: off ? 'អវត្តមាន — ចុចដើម្បីដាក់ចូលវិញ' : 'ចុចដើម្បីសម្គាល់ថាអវត្តមាន',
        onclick: () => { mem.off = off ? mem.off.filter((x) => x !== p.id) : [...mem.off, p.id]; save(); refresh(); redraw(); } }, mark(p) + p.n));
    }
    const pr = present(), m = pr.filter((p) => p.g === 'm').length, f = pr.filter((p) => p.g === 'f').length;
    count.textContent = people.length ? `(${pr.length}/${people.length})` : '';
    gsum.textContent = people.length ? `ប្រុស ${m} · ស្រី ${f}${pr.length - m - f ? ` · មិនទាន់កំណត់ភេទ ${pr.length - m - f}` : ''}` : '';
  }
  function spin() {
    if (spinning) return;
    const list = eligible(), n = list.length; if (!n) return;
    frozen = list; closePop(); current = null;
    const pick = Math.floor(Math.random() * n), a = Math.PI * 2 / n, target = -(pick * a + (Math.random() - 0.5) * a * 0.7);
    const from = angle, norm = ((target - from) % (Math.PI * 2) + Math.PI * 2) % (Math.PI * 2);
    const to = from + (5 + Math.floor(Math.random() * 3)) * Math.PI * 2 + norm, dur = wheelSettings.dur * 1000 * (0.9 + Math.random() * 0.2), t0 = performance.now();
    let last = -1; spinning = true; spinBtn.disabled = true; msg.hidden = true;
    const frame = (now) => {
      const t = Math.min(1, (now - t0) / dur); angle = from + (to - from) * (1 - Math.pow(1 - t, 4)); draw();
      const sl = Math.floor(((-angle % (Math.PI * 2)) + Math.PI * 2 + a / 2) / a); if (sl !== last) { last = sl; beep([900], 0.04, 0.025); }
      if (t < 1) return requestAnimationFrame(frame);
      spinning = false; angle = to % (Math.PI * 2); draw(); finish(list[pick]);
    };
    requestAnimationFrame(frame);
  }
  spinBtn.onclick = spin; againBtn.onclick = spin; closeBtn.onclick = closePop; revealBtn.onclick = reveal; sayBtn.onclick = say;
  pop.addEventListener('click', (e) => { if (e.target === pop) closePop(); });
  pop.addEventListener('keydown', (e) => { if (e.key === 'Escape') closePop(); });
  absentBtn.onclick = () => { if (!current) return; mem.off.push(current.id); mem.done = mem.done.filter((x) => x !== current.id); const l = mem.hist[mem.hist.length - 1]; if (l && l.n === current.n) mem.hist.pop(); save(); current = null; closePop(); renderHist(); refresh(); redraw(); };

  // ---- groups / random order ----
  const gMode = h('select', { 'aria-label': 'របៀបបែងចែក' }, [h('option', { value: 'n' }, 'ចំនួនក្រុម'), h('option', { value: 'k' }, 'សិស្សក្នុងមួយក្រុម')]);
  const gNum = h('input', { type: 'number', min: '1', max: '60', value: '4', 'aria-label': 'ចំនួន', style: 'width:90px;flex:none' });
  const gBal = h('input', { type: 'checkbox', checked: 'checked', style: 'width:20px;height:20px;flex:none' });
  const showBlocks = (blocks) => {
    groupsBox.innerHTML = ''; groupsBox.hidden = false; lastText = '';
    for (const b of blocks) {
      groupsBox.appendChild(h('div', { class: 'wheel-g' }, [h('b', {}, b.title), h('ol', {}, b.people.map((p) => h('li', {}, mark(p) + p.n)))]));
      lastText += `${b.title}\n${b.people.map((p, i) => `${i + 1}. ${p.n}`).join('\n')}\n\n`;
    }
    copyBtn.hidden = false;
  };
  // popup: names shuffle between the group cards, then the real groups appear one by one with fireworks
  const gSmall = h('small', {}, 'កំពុងបែងចែកក្រុម…');
  const gGrid = h('div', { class: 'wheel-ggrid' });
  const gAgain = h('button', { class: 'btn-sm' }, 'បែងចែកម្ដងទៀត');
  const gCopy = h('button', { class: 'secondary btn-sm' }, 'ចម្លង');
  const gClose = h('button', { class: 'secondary btn-sm' }, 'បិទ');
  const gPop = h('div', { class: 'wheel-pop', role: 'dialog', 'aria-modal': 'true', hidden: '' }, h('div', { class: 'wheel-pop-card wheel-gcard' }, [gSmall, gGrid, h('div', { class: 'row wheel-tools' }, [gAgain, gCopy, gClose])]));
  let gRun = 0, gRedo = null;
  const fillCards = (blocks, cls) => {
    gGrid.innerHTML = ''; gGrid.className = `wheel-ggrid${cls ? ` ${cls}` : ''}`;
    blocks.forEach((b, i) => { const d = h('div', { class: 'wheel-g' }, [h('b', {}, b.title), h('ol', {}, b.people.map((p) => h('li', {}, mark(p) + p.n)))]); d.style.setProperty('--i', i); gGrid.appendChild(d); });
  };
  const closeGroupPop = () => { gRun++; gPop.hidden = true; fwRun++; fw.getContext('2d').clearRect(0, 0, fw.width, fw.height); };
  const groupPop = (blocks, redo) => {
    gRedo = redo; const id = ++gRun, sizes = blocks.map((b) => b.people.length), pool = blocks.flatMap((b) => b.people);
    const reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
    closePop(); gPop.hidden = false; gSmall.textContent = 'កំពុងបែងចែកក្រុម…'; gAgain.disabled = true; gCopy.disabled = true;
    const t0 = performance.now(), DUR = reduce ? 0 : 2600; let last = 0;
    const frame = (now) => {
      if (id !== gRun) return;
      if (now - t0 >= DUR) {
        fillCards(blocks, 'reveal'); gSmall.textContent = 'បែងចែកក្រុមរួចរាល់! 🎉'; gAgain.disabled = false; gCopy.disabled = false;
        if (wheelSettings.fw) { beep([523, 659, 784, 1047], 0.08, 0.3); fireworks(); }
        return gAgain.focus({ preventScroll: true });
      }
      if (now - last > 95) { last = now; const sh = whShuffle(pool); let at = 0; fillCards(blocks.map((b, i) => { const l = sh.slice(at, at + sizes[i]); at += sizes[i]; return { title: b.title, people: l }; }), 'rolling'); beep([480 + Math.random() * 500], 0.025, 0.04); }
      requestAnimationFrame(frame);
    };
    requestAnimationFrame(frame);
  };
  gAgain.onclick = () => gRedo && gRedo(); gClose.onclick = closeGroupPop; gCopy.onclick = () => { copyBtn.click(); gCopy.textContent = 'បានចម្លង ✓'; setTimeout(() => { gCopy.textContent = 'ចម្លង'; }, 1600); };
  gPop.addEventListener('click', (e) => { if (e.target === gPop) closeGroupPop(); });
  gPop.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeGroupPop(); });
  const makeGroups = () => {
    const pr = present(); if (!pr.length) { groupsBox.hidden = false; groupsBox.textContent = 'មិនទាន់មានសិស្សទេ។'; return; }
    const num = Math.max(1, Math.floor(+gNum.value) || 1), cnt = gMode.value === 'k' ? Math.ceil(pr.length / num) : Math.min(num, pr.length);
    const groups = Array.from({ length: cnt }, () => []);
    const order = gBal.checked && pr.some((p) => p.g)
      ? [...whShuffle(pr.filter((p) => p.g === 'f')), ...whShuffle(pr.filter((p) => p.g === 'm')), ...whShuffle(pr.filter((p) => !p.g))] : whShuffle(pr);
    order.forEach((p, i) => groups[i % cnt].push(p));   // round-robin: sizes differ by at most 1 and each gender is spread out
    const blocks = groups.map((g, i) => ({ title: `ក្រុមទី ${whKh(i + 1)} · ${whKh(g.length)} នាក់`, people: g }));
    showBlocks(blocks); groupPop(blocks, makeGroups);
  };
  const makeOrder = () => { const pr = whShuffle(present()); if (!pr.length) return; const blocks = [{ title: `លំដាប់ចៃដន្យ · ${whKh(pr.length)} នាក់`, people: pr }]; showBlocks(blocks); groupPop(blocks, makeOrder); };
  copyBtn.onclick = async () => { let ok = false; try { await navigator.clipboard.writeText(lastText); ok = true; } catch {} copyBtn.textContent = ok ? 'បានចម្លង ✓' : 'ចម្លងមិនបាន'; setTimeout(() => { copyBtn.textContent = 'ចម្លងលទ្ធផល'; }, 1600); };

  const gSel = h('select', { 'aria-label': 'កង់ជ្រើសពី', style: 'width:auto;min-width:150px' }, [h('option', { value: '' }, 'សិស្សទាំងអស់'), h('option', { value: 'm' }, 'តែប្រុស'), h('option', { value: 'f' }, 'តែស្រី')]);
  gSel.onchange = () => { gFilter = gSel.value; refresh(); redraw(); };

  const durV = h('b', {}, whKh(wheelSettings.dur));
  const durIn = h('input', { type: 'range', min: '2', max: '15', step: '1', value: String(wheelSettings.dur), style: 'padding:0;border:0;accent-color:var(--brand)' });
  durIn.oninput = () => { wheelSettings.dur = +durIn.value; durV.textContent = whKh(durIn.value); wheelSaveSettings(); };
  const themeSel = h('select', {}, Object.keys(WHEEL_PALETTES).map((k) => h('option', { value: k }, WHEEL_PALETTES[k][0])));
  themeSel.value = wheelSettings.theme; themeSel.onchange = () => { wheelSettings.theme = themeSel.value; wheelSaveSettings(); draw(); };
  const chk = (key, label, wrap) => { const i = h('input', { type: 'checkbox', style: 'width:20px;height:20px;flex:none' }); i.checked = !!wheelSettings[key]; i.onchange = () => { wheelSettings[key] = i.checked; wheelSaveSettings(); }; (wrap || h('label', { class: 'wheel-chk' })).append(i, label); return wrap || i.parentElement; };
  speakRow.append(); chk('speak', ' អានឈ្មោះឱ្យលឺ', speakRow);
  const settingsCard = h('div', { class: 'card' }, [
    h('h3', {}, 'ការកំណត់កង់'),
    h('label', { style: 'font-weight:400' }, ['រយៈពេលបង្វិល៖ ', durV, ' វិនាទី']), durIn,
    h('label', { style: 'font-weight:400;margin-top:8px;display:block' }, 'ពណ៌កង់'), themeSel,
    chk('fw', ' កាំជ្រួច និងសំឡេងអបអរ'), chk('mystery', ' លាក់ឈ្មោះសិស្សរហូតដល់ចុច «បង្ហាញឈ្មោះ»'), speakRow,
    h('p', { class: 'muted', style: 'font-size:14px;margin:8px 0 0' }, 'ផ្លូវកាត់៖ Space ឬ Ctrl+Enter ដើម្បីបង្វិល · Esc ដើម្បីបិទ'),
  ]);
  const stage = h('div', { class: 'wheel-stage' }, [
    h('div', { class: 'wheel-box' }, [h('div', { class: 'wheel-pointer' }), canvas, spinBtn]),
    msg,
    h('div', { class: 'row wheel-tools' }, [
      h('button', { class: 'secondary btn-sm', onclick: () => { if (document.fullscreenElement) document.exitFullscreen(); else if (stage.requestFullscreen) stage.requestFullscreen(); } }, 'ពេញអេក្រង់'),
      h('button', { class: 'secondary btn-sm', onclick: (e) => { sound = !sound; e.target.textContent = `សំឡេង៖ ${sound ? 'បើក' : 'បិទ'}`; } }, 'សំឡេង៖ បើក'),
      h('button', { class: 'secondary btn-sm', onclick: (e) => { noRepeat = !noRepeat; e.target.textContent = `មិនជ្រើសម្ដងទៀត៖ ${noRepeat ? 'បើក' : 'បិទ'}`; refresh(); redraw(); } }, 'មិនជ្រើសម្ដងទៀត៖ បើក'),
      h('button', { class: 'secondary btn-sm', onclick: () => { mem.done = []; save(); current = null; closePop(); refresh(); redraw(); } }, 'ចាប់ផ្ដើមជុំថ្មី'),
      h('button', { class: 'secondary btn-sm', onclick: () => { ord = {}; people.forEach((p) => { ord[p.id] = Math.random(); }); redraw(); } }, 'លាយលំដាប់កង់'),
    ]),
    h('div', { class: 'row wheel-tools', style: 'align-items:center' }, [h('span', {}, 'កង់ជ្រើសពី៖'), gSel]),
    fw, pop, gPop,
  ]);
  const side = h('div', {}, [
    h('div', { class: 'card' }, [
      h('label', {}, 'ថ្នាក់'), sel,
      h('h3', { style: 'margin-top:16px' }, ['សិស្ស ', count]),
      gsum,
      h('p', { class: 'muted', style: 'font-size:14px' }, 'ចុចលើឈ្មោះដើម្បីសម្គាល់ថាអវត្តមាន (មិនចូលកង់)។ ឈ្មោះ និងភេទមកពី «ថ្នាក់ និងសិស្ស»។'),
      chips,
    ]),
    settingsCard,
    h('div', { class: 'card' }, [
      h('div', { class: 'row', style: 'justify-content:space-between' }, [h('h3', { style: 'margin:0' }, ['លទ្ធផលដែលបានជ្រើស ', histCount]),
        h('button', { class: 'secondary btn-sm', onclick: (e) => { tally = !tally; e.target.textContent = tally ? 'មើលតាមលំដាប់ពេល' : 'សរុបតាមចំនួនដង'; renderHist(); } }, 'សរុបតាមចំនួនដង')]),
      histList,
      h('div', { class: 'row' }, [
        h('button', { class: 'secondary btn-sm', onclick: async (e) => { const c = histCounts(); const txt = tally ? Object.keys(c).sort((a, b) => c[b] - c[a]).map((n) => `${n}\t${c[n]}`).join('\n') : mem.hist.map((x, i) => `${i + 1}. ${x.n}`).join('\n'); let ok = false; try { await navigator.clipboard.writeText(txt); ok = true; } catch {} e.target.textContent = ok ? 'បានចម្លង ✓' : 'ចម្លងមិនបាន'; setTimeout(() => { e.target.textContent = 'ចម្លង'; }, 1600); } }, 'ចម្លង'),
        h('button', { class: 'btn-sm', onclick: () => {
          if (!window.XLSX) return Exam.notify('មិនអាចបើកកម្មវិធី Excel បានទេ។');
          const wb = XLSX.utils.book_new(); whAddSheets(wb, {}, '', people, mem);
          XLSX.writeFile(wb, `កង់ឈ្មោះ-${(classes.find((c) => c.id === wheelClassId) || {}).name || 'ថ្នាក់'}-${new Date().toISOString().slice(0, 10).replace(/-/g, '')}.xlsx`);
        } }, 'ទាញយក Excel'),
        h('button', { class: 'secondary btn-sm', onclick: async (e) => {
          if (!window.XLSX) return Exam.notify('មិនអាចបើកកម្មវិធី Excel បានទេ។');
          e.target.disabled = true;
          try {
            const wb = XLSX.utils.book_new(), used = {};
            for (const c of classes) {
              const { students: st } = await api(`/api/classes/${c.id}/students`);
              let m = { off: [], done: [], hist: [] }; try { m = Object.assign(m, JSON.parse(localStorage.getItem(`exam_wheel_${c.id}`))); } catch {}
              whAddSheets(wb, used, c.name, st.map((s) => ({ id: s.id, n: `${s.surname || ''} ${s.first_name || ''}`.trim(), g: whGender(s.gender) })), m);
            }
            XLSX.writeFile(wb, `កង់ឈ្មោះ-គ្រប់ថ្នាក់-${new Date().toISOString().slice(0, 10).replace(/-/g, '')}.xlsx`);
          } catch (er) { Exam.notify(er.message); }
          e.target.disabled = false;
        } }, 'Excel គ្រប់ថ្នាក់'),
        h('button', { class: 'secondary btn-sm', onclick: async () => { if (!mem.hist.length || !(await Exam.confirm('សម្អាតលទ្ធផលទាំងអស់ក្នុងថ្នាក់នេះ?'))) return; mem.hist = []; save(); renderHist(); } }, 'សម្អាតលទ្ធផល'),
      ]),
    ]),
    h('div', { class: 'card' }, [
      h('h3', {}, 'បែងចែកក្រុម'),
      h('div', { class: 'row' }, [gMode, gNum]),
      h('label', { style: 'display:flex;gap:8px;align-items:flex-start;margin:10px 0;font-weight:400' }, [gBal, 'លាយប្រុស និងស្រីឱ្យស្មើគ្នាក្នុងក្រុម']),
      h('div', { class: 'row' }, [h('button', { class: 'btn-sm', onclick: makeGroups }, 'បែងចែកក្រុម'), h('button', { class: 'secondary btn-sm', onclick: makeOrder }, 'លំដាប់ចៃដន្យ')]),
      groupsBox, copyBtn,
    ]),
  ]);
  root.appendChild(h('div', { class: 'wheel-layout' }, [stage, side]));
  if (window.speechSynthesis) { findVoice(); if (speechSynthesis.addEventListener) speechSynthesis.addEventListener('voiceschanged', findVoice); }
  if (window.wheelKeyHandler) document.removeEventListener('keydown', window.wheelKeyHandler);
  window.wheelKeyHandler = (e) => {
    if (document.getElementById('tab-wheel').hidden || !document.getElementById('tab-wheel').contains(canvas)) return;
    const tag = e.target.tagName || '';
    if ((e.code === 'Enter' && (e.ctrlKey || e.metaKey)) || (e.code === 'Space' && e.target === document.body && !/INPUT|TEXTAREA|SELECT/.test(tag))) { e.preventDefault(); if (!pop.hidden && pendingReveal) reveal(); else spin(); }
  };
  document.addEventListener('keydown', window.wheelKeyHandler);
  renderHist(); refresh(); draw();
  if (document.fonts && document.fonts.load) document.fonts.load('600 20px "Kantumruy Pro"').then(() => { if (!spinning) redraw(); });
};
