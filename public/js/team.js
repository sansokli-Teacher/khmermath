// Team features: owner's teacher list + invite links, and the "share" dialog.
const ROLE_NAMES = { reviewer: 'អ្នកពិនិត្យ (មើលបាន + ផ្តល់ចំណាំ)', editor: 'អ្នកកែសម្រួល (មើល + កែ + ដាក់ពិន្ទុ)' };

function inviteUrl(token) {
  return `${location.origin}/invite.html?token=${token}`;
}

async function copyText(text) {
  try { await navigator.clipboard.writeText(text); return true; } catch { return false; }
}

// A one-time link box with a copy button.
function linkBox(url, caption) {
  const input = h('input', { type: 'text', value: url, readonly: 'readonly', style: 'font-family:monospace;font-size:13px;' });
  input.addEventListener('focus', () => input.select());
  return h('div', { class: 'notice' }, [
    h('div', { style: 'font-weight:600;margin-bottom:6px;' }, caption),
    h('div', { class: 'row', style: 'flex-wrap:nowrap;' }, [
      input,
      h('button', { onclick: async (e) => { input.select(); const ok = await copyText(url); e.target.textContent = ok ? '✓ បានចម្លង' : 'ចុច Ctrl+C'; } }, '📋 ចម្លង'),
    ]),
    h('div', { class: 'muted', style: 'margin-top:6px;' }, 'តំណនេះប្រើបានតែម្តង ហើយផុតកំណត់ក្នុង ៧ ថ្ងៃ។ ផ្ញើទៅគ្រូតាម Telegram ឬ Messenger។ តំណនេះនឹងមិនបង្ហាញម្តងទៀតទេ។'),
  ]);
}

render.teachers = async function () {
  const container = document.getElementById('tab-teachers');
  container.innerHTML = '';
  const { teachers, invites } = await api('/api/admin/teachers');

  const note = h('input', { type: 'text', placeholder: 'ឈ្មោះគ្រូ ឬកំណត់សម្គាល់ (មិនចាំបាច់) ឧ. គ្រូ សុភា ថ្នាក់ទី ៩', style: 'flex:1;min-width:220px;' });
  const linkSlot = h('div', {});
  const inviteCard = h('div', { class: 'card' }, [
    h('h2', {}, '➕ អញ្ជើញគ្រូថ្មី'),
    h('p', { class: 'muted' }, 'បង្កើតតំណអញ្ជើញ ១ ដង ផ្ញើទៅគ្រូ ហើយគ្រូជ្រើសរើសឈ្មោះអ្នកប្រើ និងពាក្យសម្ងាត់ដោយខ្លួនឯង។ មិនត្រូវការអ៊ីមែលទេ។ មានតែអ្នកដែលអ្នកអញ្ជើញប៉ុណ្ណោះដែលអាចចូលបាន។'),
    h('div', { class: 'row' }, [
      note,
      h('button', { onclick: async () => {
        try {
          const inv = await api('/api/admin/invites', { method: 'POST', body: { note: note.value } });
          linkSlot.innerHTML = '';
          linkSlot.append(linkBox(inviteUrl(inv.token), '✅ តំណអញ្ជើញរួចរាល់'));
          setTimeout(() => refreshPending(), 0);
        } catch (e) { Exam.notify(e.message); }
      } }, 'បង្កើតតំណអញ្ជើញ'),
    ]),
    linkSlot,
  ]);

  const pendingBox = h('div', {});
  function drawPending(list) {
    pendingBox.innerHTML = '';
    if (!list.length) return;
    pendingBox.append(h('h3', { style: 'margin-top:14px;' }, 'តំណដែលមិនទាន់ប្រើ'));
    list.forEach((i) => pendingBox.append(h('div', { class: 'list-item' }, [
      h('div', {}, [
        h('span', { class: `badge ${i.purpose === 'reset' ? 'warn' : 'upcoming'}` }, i.purpose === 'reset' ? `កំណត់ពាក្យសម្ងាត់ថ្មី · ${i.teacher_name || ''}` : 'អញ្ជើញ'),
        h('span', { style: 'margin-left:8px;' }, i.note || ''),
        h('span', { class: 'muted', style: 'margin-left:8px;' }, `ផុតកំណត់ ${fmtDateTime(i.expires_at)}`),
      ]),
      h('button', { class: 'danger btn-sm', onclick: async () => { await api(`/api/admin/invites/${i.id}`, { method: 'DELETE' }); refreshPending(); } }, 'បោះបង់'),
    ])));
  }
  async function refreshPending() { const d = await api('/api/admin/teachers'); drawPending(d.invites); }
  drawPending(invites);
  inviteCard.append(pendingBox);

  const search = h('input', { type: 'text', placeholder: '🔍 ស្វែងរកគ្រូ…', style: 'max-width:260px;' });
  const rowsBox = h('div', { style: 'overflow-x:auto;' });
  function drawRows() {
    const q = search.value.trim().toLowerCase();
    const list = teachers.filter((t) => !q || `${t.display_name || ''} ${t.username}`.toLowerCase().includes(q));
    rowsBox.innerHTML = '';
    rowsBox.append(h('table', {}, [
      h('thead', {}, h('tr', {}, ['ឈ្មោះ', 'ឈ្មោះអ្នកប្រើ', 'ថ្នាក់', 'តេស្ត', 'ចូលចុងក្រោយ', 'ស្ថានភាព', ''].map((x) => h('th', {}, x)))),
      h('tbody', {}, list.map((t) => h('tr', {}, [
        h('td', {}, [h('strong', {}, t.display_name || t.username), t.role === 'owner' ? h('span', { class: 'badge upcoming', style: 'margin-left:6px;' }, 'ម្ចាស់') : null]),
        h('td', { class: 'muted' }, t.username),
        h('td', {}, t.class_count), h('td', {}, t.test_count),
        h('td', { class: 'muted', style: 'white-space:nowrap;' }, t.last_login ? fmtDateTime(t.last_login) : '—'),
        h('td', {}, h('span', { class: `badge ${t.active ? 'ready' : 'closed'}` }, t.active ? 'ប្រើបាន' : 'ត្រូវបានបិទ')),
        h('td', {}, t.role === 'owner' ? null : h('div', { class: 'row', style: 'gap:4px;flex-wrap:nowrap;' }, [
          h('button', { class: 'secondary btn-sm', title: 'បង្កើតតំណកំណត់ពាក្យសម្ងាត់ថ្មី', onclick: async () => {
            const r = await api(`/api/admin/teachers/${t.id}/reset-link`, { method: 'POST' });
            const box = linkBox(inviteUrl(r.token), `តំណកំណត់ពាក្យសម្ងាត់ថ្មីសម្រាប់ ${t.display_name || t.username}`);
            linkSlot.innerHTML = ''; linkSlot.append(box); box.scrollIntoView({ behavior: 'smooth', block: 'center' });
            refreshPending();
          } }, '🔑 កំណត់ថ្មី'),
          h('button', { class: `btn-sm ${t.active ? 'danger' : 'secondary'}`, onclick: async () => {
            if (t.active && !(await Exam.confirm(`បិទគណនីរបស់ ${t.display_name || t.username}? គាត់នឹងមិនអាចចូលបានទេ ប៉ុន្តែទិន្នន័យនៅរក្សាទុក។`))) return;
            await api(`/api/admin/teachers/${t.id}/active`, { method: 'POST', body: { active: !t.active } });
            render.teachers();
          } }, t.active ? 'បិទគណនី' : 'បើកវិញ'),
        ])),
      ]))),
    ]));
  }
  search.addEventListener('input', drawRows);
  drawRows();
  container.append(inviteCard, h('div', { class: 'card' }, [
    h('div', { class: 'row', style: 'justify-content:space-between;' }, [h('h2', { style: 'margin:0;' }, `គ្រូបង្រៀន (${teachers.length})`), search]),
    rowsBox,
  ]));
};

// ---------- Share a class or a test with another teacher ----------
async function openShareDialog(type, id, title) {
  const back = h('div', { class: 'modal-back', onclick: (e) => { if (e.target === back) back.remove(); } });
  const box = h('div', { class: 'modal-box', style: 'text-align:left;max-width:520px;' });
  back.append(box);
  document.body.append(back);

  const role = h('select', {}, Object.entries(ROLE_NAMES).map(([v, l]) => h('option', { value: v }, l)));
  const q = h('input', { type: 'text', placeholder: '🔍 វាយឈ្មោះគ្រូ ដើម្បីស្វែងរក…' });
  const results = h('div', {});
  const current = h('div', {});

  async function drawCurrent() {
    const { shares } = await api(`/api/shares?type=${type}&id=${id}`);
    current.innerHTML = '';
    current.append(h('h3', { style: 'margin:14px 0 4px;' }, 'អ្នកដែលមានសិទ្ធិចូល'));
    if (!shares.length) current.append(h('p', { class: 'muted' }, 'មិនទាន់បានចែករំលែកជាមួយអ្នកណាទេ។'));
    shares.forEach((s) => current.append(h('div', { class: 'list-item' }, [
      h('div', {}, [h('strong', {}, s.name), h('span', { class: 'muted' }, ` (${s.username})`)]),
      h('div', { class: 'row', style: 'gap:6px;flex-wrap:nowrap;' }, [
        h('select', { style: 'width:auto;padding:5px 8px;font-size:13px;', onchange: async (e) => { await api('/api/shares', { method: 'POST', body: { type, id, teacher_id: s.teacher_id, role: e.target.value } }); } },
          Object.entries(ROLE_NAMES).map(([v, l]) => h('option', { value: v, selected: v === s.role ? 'selected' : null }, v === 'reviewer' ? 'អ្នកពិនិត្យ' : 'អ្នកកែសម្រួល'))),
        h('button', { class: 'danger btn-sm', onclick: async () => { await api('/api/shares/remove', { method: 'POST', body: { type, id, teacher_id: s.teacher_id } }); drawCurrent(); } }, 'ដកចេញ'),
      ]),
    ])));
  }

  async function runSearch() {
    const { teachers } = await api(`/api/teachers/search?q=${encodeURIComponent(q.value.trim())}`);
    results.innerHTML = '';
    if (!teachers.length) { results.append(h('p', { class: 'muted' }, 'រកមិនឃើញគ្រូទេ។ គ្រូត្រូវតែបានចូលប្រើប្រព័ន្ធជាមុន (ដោយតំណអញ្ជើញ)។')); return; }
    teachers.forEach((t) => results.append(h('div', { class: 'list-item' }, [
      h('div', {}, [h('strong', {}, t.name), h('span', { class: 'muted' }, ` (${t.username})`)]),
      h('button', { class: 'btn-sm', onclick: async () => {
        try { await api('/api/shares', { method: 'POST', body: { type, id, teacher_id: t.id, role: role.value } }); await drawCurrent(); results.innerHTML = ''; q.value = ''; }
        catch (e) { Exam.notify(e.message); }
      } }, '+ បន្ថែម'),
    ])));
  }
  let timer = null;
  q.addEventListener('input', () => { clearTimeout(timer); timer = setTimeout(runSearch, 250); });

  box.append(
    h('div', { class: 'row', style: 'justify-content:space-between;' }, [h('h2', { style: 'margin:0;' }, `👥 ចែករំលែក — ${title}`), h('button', { class: 'secondary btn-sm', onclick: () => back.remove() }, '✕')]),
    h('p', { class: 'muted' }, type === 'test'
      ? 'គ្រូដែលអ្នកបន្ថែមអាចមើល សាកល្បងជាសិស្ស បោះពុម្ពវិញ្ញាសា និងសរសេរចំណាំអំពីកំហុស។'
      : 'គ្រូដែលអ្នកបន្ថែមអាចមើលបញ្ជីសិស្ស លទ្ធផល និងពិន្ទុរបស់ថ្នាក់នេះ។'),
    h('label', {}, 'សិទ្ធិ'), role,
    h('label', {}, 'ស្វែងរកគ្រូ'), q, results, current,
  );
  runSearch();
  drawCurrent();
}
