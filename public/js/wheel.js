// Name wheel for the teacher: picks a student from one of the teacher's own classes (no second list to keep).
// Which students are absent / already picked is remembered per class in this browser only.
const WHEEL_COLORS = ['#e8590c', '#1c7ed6', '#2f9e44', '#ae3ec9', '#f08c00', '#0c8599', '#d6336c', '#5f3dc4'];
let wheelClassId = null;

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
  const people = students.map((s) => ({ id: s.id, n: `${s.surname || ''} ${s.first_name || ''}`.trim() }));

  const KEY = `exam_wheel_${wheelClassId}`;
  let mem = { off: [], done: [] };
  try { mem = Object.assign(mem, JSON.parse(localStorage.getItem(KEY))); } catch {}
  const save = () => { try { localStorage.setItem(KEY, JSON.stringify(mem)); } catch {} };
  let noRepeat = true, sound = true, spinning = false, angle = 0, frozen = null, current = null, audio = null;
  const eligible = () => people.filter((p) => !mem.off.includes(p.id) && !(noRepeat && mem.done.includes(p.id)));

  const canvas = h('canvas', { width: '720', height: '720', 'aria-label': 'កង់ឈ្មោះសិស្ស' });
  const ctx = canvas.getContext('2d');
  const spinBtn = h('button', { class: 'wheel-hub', 'aria-label': 'បង្វិលកង់' }, 'បង្វិល');
  const msg = h('div', { class: 'notice', hidden: '' });
  const winner = h('b', {});
  const result = h('div', { class: 'wheel-result', role: 'status', hidden: '' }, [h('small', {}, 'សិស្សដែលត្រូវបានជ្រើស'), winner]);
  const chips = h('div', { class: 'wheel-chips' });
  const count = h('span', { class: 'muted' });

  function draw() {
    const list = frozen || eligible(), n = list.length, W = canvas.width, c = W / 2, r = c - 6;
    ctx.clearRect(0, 0, W, W); ctx.save(); ctx.translate(c, c); ctx.rotate(angle);
    if (!n) { ctx.beginPath(); ctx.arc(0, 0, r, 0, 7); ctx.fillStyle = '#cfd6dd'; ctx.fill(); }
    else {
      const a = Math.PI * 2 / n;
      for (let i = 0; i < n; i++) {
        ctx.beginPath(); ctx.moveTo(0, 0); ctx.arc(0, 0, r, i * a - Math.PI / 2 - a / 2, i * a - Math.PI / 2 + a / 2); ctx.closePath();
        ctx.fillStyle = WHEEL_COLORS[i % WHEEL_COLORS.length]; ctx.fill();
        if (n > 1) { ctx.strokeStyle = 'rgba(255,255,255,.7)'; ctx.lineWidth = 2; ctx.stroke(); }
        ctx.save(); ctx.rotate(i * a - Math.PI / 2);
        ctx.font = `600 ${Math.max(14, Math.min(38, Math.floor(r * a * 0.6)))}px "Kantumruy Pro", "Noto Sans Khmer", sans-serif`;
        ctx.fillStyle = '#fff'; ctx.textAlign = 'right'; ctx.textBaseline = 'middle'; ctx.shadowColor = 'rgba(0,0,0,.35)'; ctx.shadowBlur = 3;
        let name = list[i].n; const maxW = r * 0.66;
        while (ctx.measureText(name).width > maxW && name.length > 2) name = name.slice(0, -1);
        if (name !== list[i].n) name += '…';
        ctx.fillText(name, r - 18, 0); ctx.restore();
      }
    }
    ctx.restore();
  }
  const redraw = () => { frozen = null; draw(); };
  function beep(freqs) {
    if (!sound) return;
    try {
      audio = audio || new (window.AudioContext || window.webkitAudioContext)();
      freqs.forEach((f, i) => { const o = audio.createOscillator(), g = audio.createGain(), t = audio.currentTime + i * 0.13;
        o.frequency.value = f; g.gain.setValueAtTime(freqs.length > 1 ? 0.08 : 0.04, t); g.gain.exponentialRampToValueAtTime(0.001, t + (freqs.length > 1 ? 0.3 : 0.03));
        o.connect(g); g.connect(audio.destination); o.start(t); o.stop(t + 0.32); });
    } catch {}
  }
  function refresh() {
    const list = eligible();
    msg.hidden = !!list.length || spinning;
    msg.textContent = !people.length ? 'ថ្នាក់នេះមិនទាន់មានសិស្សទេ។ សូមបញ្ចូលសិស្សនៅក្នុង «ថ្នាក់ និងសិស្ស»។'
      : noRepeat && people.some((p) => !mem.off.includes(p.id)) ? 'សិស្សទាំងអស់ត្រូវបានជ្រើសហើយ។ ចុច «ចាប់ផ្ដើមជុំថ្មី»។' : 'សិស្សទាំងអស់អវត្តមាន។';
    spinBtn.disabled = spinning || !list.length;
    chips.innerHTML = '';
    for (const p of people) {
      const off = mem.off.includes(p.id), done = noRepeat && mem.done.includes(p.id);
      chips.appendChild(h('button', { type: 'button', class: `wheel-chip secondary${off ? ' off' : ''}${done ? ' done' : ''}`, title: off ? 'អវត្តមាន — ចុចដើម្បីដាក់ចូលវិញ' : 'ចុចដើម្បីសម្គាល់ថាអវត្តមាន',
        onclick: () => { mem.off = off ? mem.off.filter((x) => x !== p.id) : [...mem.off, p.id]; save(); refresh(); redraw(); } }, p.n));
    }
    count.textContent = people.length ? `(${people.length - mem.off.length}/${people.length})` : '';
  }
  function spin() {
    if (spinning) return;
    const list = eligible(), n = list.length; if (!n) return;
    frozen = list; result.hidden = true; current = null;
    const pick = Math.floor(Math.random() * n), a = Math.PI * 2 / n, target = -(pick * a + (Math.random() - 0.5) * a * 0.7);
    const from = angle, norm = ((target - from) % (Math.PI * 2) + Math.PI * 2) % (Math.PI * 2);
    const to = from + (5 + Math.floor(Math.random() * 3)) * Math.PI * 2 + norm, dur = 4600 + Math.random() * 1200, t0 = performance.now();
    let last = -1; spinning = true; spinBtn.disabled = true; msg.hidden = true;
    const frame = (now) => {
      const t = Math.min(1, (now - t0) / dur); angle = from + (to - from) * (1 - Math.pow(1 - t, 4)); draw();
      const sl = Math.floor(((-angle % (Math.PI * 2)) + Math.PI * 2 + a / 2) / a); if (sl !== last) { last = sl; beep([900]); }
      if (t < 1) return requestAnimationFrame(frame);
      spinning = false; angle = to % (Math.PI * 2); draw(); current = list[pick];
      if (noRepeat && !mem.done.includes(current.id)) mem.done.push(current.id); save();
      winner.textContent = current.n; result.hidden = false; beep([523, 659, 784]); refresh();
    };
    requestAnimationFrame(frame);
  }
  spinBtn.onclick = spin;

  const stage = h('div', { class: 'wheel-stage' }, [
    h('div', { class: 'wheel-box' }, [h('div', { class: 'wheel-pointer' }), canvas, spinBtn]),
    msg, result,
    h('div', { class: 'row wheel-tools' }, [
      h('button', { class: 'btn-sm', onclick: spin }, 'បង្វិលម្ដងទៀត'),
      h('button', { class: 'secondary btn-sm', onclick: () => { if (!current) return; mem.off.push(current.id); mem.done = mem.done.filter((x) => x !== current.id); save(); current = null; result.hidden = true; refresh(); redraw(); } }, 'អវត្តមាន — ដកចេញ'),
      h('button', { class: 'secondary btn-sm', onclick: () => { if (document.fullscreenElement) document.exitFullscreen(); else if (stage.requestFullscreen) stage.requestFullscreen(); } }, 'ពេញអេក្រង់'),
      h('button', { class: 'secondary btn-sm', onclick: (e) => { sound = !sound; e.target.textContent = `សំឡេង៖ ${sound ? 'បើក' : 'បិទ'}`; } }, 'សំឡេង៖ បើក'),
      h('button', { class: 'secondary btn-sm', onclick: (e) => { noRepeat = !noRepeat; e.target.textContent = `មិនជ្រើសម្ដងទៀត៖ ${noRepeat ? 'បើក' : 'បិទ'}`; refresh(); redraw(); } }, 'មិនជ្រើសម្ដងទៀត៖ បើក'),
      h('button', { class: 'secondary btn-sm', onclick: () => { mem.done = []; save(); current = null; result.hidden = true; refresh(); redraw(); } }, 'ចាប់ផ្ដើមជុំថ្មី'),
    ]),
  ]);
  const side = h('div', { class: 'card' }, [
    h('label', {}, 'ថ្នាក់'), sel,
    h('h3', { style: 'margin-top:16px' }, ['សិស្ស ', count]),
    h('p', { class: 'muted', style: 'font-size:14px' }, 'ចុចលើឈ្មោះដើម្បីសម្គាល់ថាអវត្តមាន (មិនចូលកង់)។ បញ្ជីមកពី «ថ្នាក់ និងសិស្ស»។'),
    chips,
  ]);
  root.appendChild(h('div', { class: 'wheel-layout' }, [stage, side]));
  refresh(); draw();
  if (document.fonts && document.fonts.load) document.fonts.load('600 20px "Kantumruy Pro"').then(() => { if (!spinning) redraw(); });
};
