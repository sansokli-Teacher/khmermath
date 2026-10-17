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

render.teamgame = async function () {
  const root = document.getElementById('tab-teamgame');
  root.innerHTML = '';
  let classes;
  try { ({ classes } = await api('/api/classes')); } catch (e) { return root.appendChild(h('div', { class: 'error' }, e.message)); }

  const intro = h('div', { class: 'card' }, [
    h('h3', { style: 'margin-top:0' }, 'ហ្គេមក្រុមសម្រាប់ថ្នាក់រៀន'),
    h('p', { class: 'muted' }, 'ជ្រើសថ្នាក់ ចែកសិស្សជាក្រុម រួចលេងហ្គេមសំណួរគណិតវិទ្យាថ្នាក់ទី ៧ (មេរៀនទី ១–២២) ឬ ថ្នាក់ទី ៨ (មេរៀនទី ១–១៩)។ ក្នុងមួយមេរៀនមាន ២០ សំណួរ ព្រមទាំងរូបធរណីមាត្រច្បាស់ៗ។ មានបីស្ទីលដែលប្រើសំណួរដូចគ្នា៖ «កាតបើក» (ជ្រើសប្រអប់លេខ) «កង់វិល» (បង្វិលកង់ជ្រើសសំណួរ) និង «ប្រណាំងទូកង» (ឆ្លើយត្រូវ ទូកទៅមុខ)។ ហ្គេមបង្ហាញពេញអេក្រង់ ដោយមិនចាំបាច់រមូរ។'),
  ]);
  root.appendChild(intro);

  const hubAfter = () => {
    // the two other games, which do not need teams
    root.appendChild(h('div', { class: 'card' }, [
      h('h3', { style: 'margin-top:0' }, 'ហ្គេមផ្សេងទៀត (ប្រើសំណួរដូចគ្នា)'),
      h('div', { style: 'display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px' }, [
        h('div', { style: 'border:1px solid var(--line);border-radius:12px;padding:12px;background:#fff' }, [h('b', {}, '📱 សំណួរផ្ទាល់លើទូរស័ព្ទ'), h('p', { class: 'muted', style: 'margin:6px 0 10px' }, 'សិស្សទាំងអស់ឆ្លើយលើទូរស័ព្ទក្នុងពេលតែមួយ ឆ្លើយលឿនបានពិន្ទុច្រើន មានតារាងចំណាត់ថ្នាក់ផ្ទាល់។'), h('button', { type: 'button', onclick: () => document.querySelector('[data-tab="live"]').click() }, 'បើកបន្ទប់ →')]),
        h('div', { style: 'border:1px solid var(--line);border-radius:12px;padding:12px;background:#fff' }, [h('b', {}, '🎯 ប៊ីងហ្គោគណិតវិទ្យា'), h('p', { class: 'muted', style: 'margin:6px 0 10px' }, 'បោះពុម្ពកាតចម្លើយឱ្យសិស្សម្នាក់មួយសន្លឹក ហៅសំណួរម្តងមួយៗ សិស្សដោះស្រាយ រួចគូសចម្លើយលើកាត។ មិនត្រូវការទូរស័ព្ទ។'), h('a', { class: 'btn', href: 'bingo.html' }, 'បង្កើតកាត →')]),
      ]),
    ]));
    };
  if (!classes.length) {
    root.appendChild(h('div', { class: 'card' }, [
      h('p', {}, 'មិនទាន់មានថ្នាក់ទេ។ អ្នកអាចលេងដោយបង្កើតក្រុមដោយខ្លួនឯង ឬបង្កើតថ្នាក់ និងបញ្ចូលសិស្សនៅក្នុង «ថ្នាក់ និងសិស្ស» ជាមុន។'),
      h('a', { class: 'btn', href: 'teamgame.html' }, '▶ លេងហ្គេមដោយមិនមានថ្នាក់'),
    ]));
    hubAfter();
    return;
  }
  if (!classes.some((c) => c.id === tgClassId)) tgClassId = classes[0].id;

  const card = h('div', { class: 'card' });
  root.appendChild(card);

  let tgGrade = (classes.find((c) => c.id === tgClassId) || {}).grade || 7;
  const sel = h('select', { 'aria-label': 'ថ្នាក់' }, classes.map((c) => h('option', { value: c.id }, c.name)));
  sel.value = tgClassId;
  const gradeSel = h('select', { 'aria-label': 'កម្រិតថ្នាក់សំណួរ' }, [
    h('option', { value: '7' }, 'ថ្នាក់ទី ៧ (មេរៀន ១–២២)'),
    h('option', { value: '8' }, 'ថ្នាក់ទី ៨ (មេរៀន ១–១៩)'),
    h('option', { value: '9' }, 'ថ្នាក់ទី ៩ (មេរៀន ១–១៩)'),
    h('option', { value: '10' }, 'ថ្នាក់ទី ១០ (មេរៀន ១–២០)'),
  ]);
  gradeSel.value = String(tgGrade);
  gradeSel.onchange = () => { tgGrade = parseInt(gradeSel.value, 10) || 7; };

  const num = h('input', { type: 'number', min: '2', max: '8', value: String(tgTeams), 'aria-label': 'ចំនួនក្រុម', style: 'width:90px' });
  const absent = h('input', { type: 'checkbox', id: 'tg-skip' }); absent.checked = tgSkipAbsent;
  const preview = h('div', { class: 'tg-prev', style: 'display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:10px;margin-top:14px' });
  const info = h('p', { class: 'muted' });
  let people = [], teams = [];

  const COLORS = ['#e8590c', '#1c7ed6', '#2f9e44', '#ae3ec9', '#f08c00', '#0c8599', '#d6336c', '#5f3dc4'];
  function draw() {
    tgTeams = Math.max(2, Math.min(8, parseInt(num.value, 10) || 4)); num.value = tgTeams;
    let off = [];
    try { off = (JSON.parse(localStorage.getItem(`exam_wheel_${tgClassId}`)) || {}).off || []; } catch {}
    const names = people.filter((p) => !(absent.checked && off.includes(p.id))).map((p) => p.n);
    teams = tgSplit(names, tgTeams);
    info.textContent = `សិស្ស ${tgKh(names.length)} នាក់${absent.checked && off.length ? ` (មិនរួមអ្នកអវត្តមាន ${tgKh(people.length - names.length)} នាក់)` : ''} → ${tgKh(tgTeams)} ក្រុម`;
    preview.innerHTML = '';
    teams.forEach((m, i) => preview.appendChild(h('div', { style: `border-left:8px solid ${COLORS[i % COLORS.length]};background:#f7f9fc;border-radius:10px;padding:8px 12px` }, [
      h('b', {}, `ក្រុមទី ${tgKh(i + 1)} `), h('span', { class: 'muted' }, `(${tgKh(m.length)} នាក់)`),
      h('div', { style: 'font-size:14px;line-height:1.6;margin-top:4px' }, m.join(', ') || '—'),
    ])));
  }

  async function loadClass() {
    const { students } = await api(`/api/classes/${tgClassId}/students`);
    people = students.map((s) => ({ id: s.id, n: `${s.surname || ''} ${s.first_name || ''}`.trim() })).filter((p) => p.n);
    draw();
  }

  sel.onchange = () => {
    tgClassId = Number(sel.value) || sel.value;
    const curC = classes.find((c) => c.id === tgClassId);
    if (curC && curC.grade) { tgGrade = curC.grade; gradeSel.value = String(tgGrade); }
    loadClass();
  };
  num.onchange = draw;
  absent.onchange = () => { tgSkipAbsent = absent.checked; draw(); };

  const again = h('button', { class: 'secondary', type: 'button' }, '🔀 ចែកក្រុមម្តងទៀត');
  again.onclick = draw;
  const launch = (style) => () => {
    if (!teams.length || !teams.some((t) => t.length)) return Exam.notify('ថ្នាក់នេះមិនទាន់មានសិស្សទេ។');
    const cls = (classes.find((c) => c.id === tgClassId) || {}).name || '';
    try { localStorage.setItem('km_wheel_last_groups', JSON.stringify({ cls, groups: teams })); } catch {}
    location.href = `teamgame.html?import=1&style=${style}&grade=${tgGrade}`;
  };
  const play = h('button', { type: 'button' }, '▶ កាតបើក'); play.onclick = launch('cards');
  const spin = h('button', { type: 'button', style: 'background:#e8590c' }, '🎡 កង់វិល'); spin.onclick = launch('wheel');
  const boat = h('button', { type: 'button', style: 'background:#1c7ed6' }, '🚣 ប្រណាំងទូកង'); boat.onclick = launch('boat');

  card.appendChild(h('div', { class: 'row', style: 'gap:12px;align-items:end;flex-wrap:wrap' }, [
    h('label', {}, ['ថ្នាក់', h('br'), sel]),
    h('label', {}, ['កម្រិតសំណួរ', h('br'), gradeSel]),
    h('label', {}, ['ចំនួនក្រុម', h('br'), num]),
    h('label', { style: 'display:flex;gap:6px;align-items:center' }, [absent, 'មិនរួមសិស្សអវត្តមាន']),
    again, play, spin, boat,
    h('a', { class: 'btn secondary', href: 'teamgame.html', style: 'background:#fff;color:var(--brand);border:1px solid #bcd0f3' }, 'លេងដោយមិនមានថ្នាក់'),
  ]));
  card.appendChild(info);
  card.appendChild(preview);
  hubAfter();
  await loadClass();
};
