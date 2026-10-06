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
  const inviteMonths = monthsSelect('ការប្រើប្រាស់ពេញលេញ', true);
  const linkSlot = h('div', {});
  const inviteCard = h('div', { class: 'card' }, [
    h('h2', {}, '➕ អញ្ជើញគ្រូថ្មី'),
    h('p', { class: 'muted' }, 'បង្កើតតំណអញ្ជើញ ១ ដង ផ្ញើទៅគ្រូ ហើយគ្រូជ្រើសរើសឈ្មោះអ្នកប្រើ និងពាក្យសម្ងាត់ដោយខ្លួនឯង។ មិនត្រូវការអ៊ីមែលទេ។ មានតែអ្នកដែលអ្នកអញ្ជើញប៉ុណ្ណោះដែលអាចចូលបាន។'),
    h('div', { class: 'row' }, [
      note,
      inviteMonths,
      h('button', { onclick: async () => {
        try {
          const inv = await api('/api/admin/invites', { method: 'POST', body: { note: note.value, months: Number(inviteMonths.value) } });
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
      h('thead', {}, h('tr', {}, ['ឈ្មោះ', 'ឈ្មោះអ្នកប្រើ', 'ការប្រើប្រាស់', 'ថ្នាក់', 'តេស្ត', 'ចូលចុងក្រោយ', 'ស្ថានភាព', ''].map((x) => h('th', {}, x)))),
      h('tbody', {}, list.map((t) => h('tr', {}, [
        h('td', {}, [h('strong', {}, t.display_name || t.username), t.role === 'owner' ? h('span', { class: 'badge upcoming', style: 'margin-left:6px;' }, 'ម្ចាស់') : null]),
        h('td', { class: 'muted' }, [t.username, t.contact ? h('div', { style: 'font-size:12px;' }, `📞 ${t.contact}`) : null]),
        h('td', {}, licenseChip(t)),
        h('td', {}, t.class_count), h('td', {}, t.test_count),
        h('td', { class: 'muted', style: 'white-space:nowrap;' }, t.last_login ? fmtDateTime(t.last_login) : '—'),
        h('td', {}, h('span', { class: `badge ${t.active ? 'ready' : 'closed'}` }, t.active ? 'ប្រើបាន' : 'ត្រូវបានបិទ')),
        h('td', {}, t.role === 'owner' ? null : h('div', { class: 'row', style: 'gap:4px;flex-wrap:wrap;min-width:150px;' }, [
          h('button', { class: 'secondary btn-sm', title: 'ផ្តល់ ឬបន្ថែមការប្រើប្រាស់', onclick: () => grantDialog(t) }, '🔓 ដោះសោ'),
          t.plan === 'full' ? h('button', { class: 'secondary btn-sm', title: 'ចាក់សោវិញ', onclick: async () => {
            if (!(await Exam.confirm(`ចាក់សោគណនី ${t.display_name || t.username} វិញ? គាត់នឹងត្រឡប់ទៅជាគណនីសាកល្បង (ទិន្នន័យនៅរក្សាទុក)។`))) return;
            await api(`/api/admin/teachers/${t.id}/license`, { method: 'POST', body: { action: 'lock' } }); render.teachers();
          } }, '🔒') : null,
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
  container.append(codesCard(), inviteCard, h('div', { class: 'card' }, [
    h('div', { class: 'row', style: 'justify-content:space-between;' }, [h('h2', { style: 'margin:0;' }, `គ្រូបង្រៀន (${teachers.length})`), search]),
    rowsBox,
  ]), await settingsCard(), await auditCard());
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


// ---------- licence helpers (owner) ----------
const MONTH_LABELS = { 1: '១ ខែ', 3: '៣ ខែ', 6: '៦ ខែ', 12: '១២ ខែ (១ ឆ្នាំ)', 24: '២៤ ខែ (២ ឆ្នាំ)', 0: 'មិនកំណត់ (ពេញមួយជីវិត)' };
function monthsSelect(lifetimeLabel, withLifetime = true) {
  const opts = [1, 3, 6, 12, 24].map((m) => h('option', { value: m }, MONTH_LABELS[m]));
  if (withLifetime) opts.push(h('option', { value: 0 }, lifetimeLabel === 'ការប្រើប្រាស់ពេញលេញ' ? MONTH_LABELS[0] : lifetimeLabel));
  const sel = h('select', { style: 'width:auto;min-width:170px;' }, opts);
  sel.value = '12';
  return sel;
}

function licenseChip(t) {
  if (t.role === 'owner') return h('span', { class: 'chip chip-open' }, '★ ម្ចាស់');
  const now = new Date().toISOString().replace('T', ' ').slice(0, 19);
  if (t.plan !== 'full') return h('span', { class: 'chip chip-closed' }, '🔒 សាកល្បង');
  if (t.license_until && t.license_until <= now) return h('span', { class: 'chip', style: 'background:#fdeaea;color:#a52a2a;' }, `⏰ ផុត ${fmtDateTime(t.license_until).split(',')[0]}`);
  return h('span', { class: 'chip chip-open' }, t.license_until ? `🔓 ដល់ ${fmtDateTime(t.license_until).split(',')[0]}` : '🔓 ពេញមួយជីវិត');
}

async function grantDialog(t) {
  const back = h('div', { class: 'modal-back', onclick: (e) => { if (e.target === back) back.remove(); } });
  const sel = monthsSelect('', true);
  back.append(h('div', { class: 'modal-box', style: 'text-align:left;max-width:420px;' }, [
    h('h2', {}, `🔓 ដោះសោ — ${t.display_name || t.username}`),
    h('p', { class: 'muted' }, 'រយៈពេលនឹងត្រូវបន្ថែមពីថ្ងៃផុតកំណត់បច្ចុប្បន្ន (បើនៅមានសុពលភាព)។'),
    sel,
    h('div', { class: 'row', style: 'margin-top:16px;justify-content:flex-end;' }, [
      h('button', { class: 'secondary', onclick: () => back.remove() }, 'បោះបង់'),
      h('button', { onclick: async () => {
        await api(`/api/admin/teachers/${t.id}/license`, { method: 'POST', body: { action: 'grant', months: Number(sel.value) } });
        back.remove(); render.teachers();
      } }, 'យល់ព្រម'),
    ]),
  ]));
  document.body.append(back);
}

function codesCard() {
  const sel = monthsSelect('', true);
  const count = h('input', { type: 'number', value: '1', min: '1', max: '30', style: 'width:80px;' });
  const note = h('input', { type: 'text', placeholder: 'កំណត់សម្គាល់ (ឧ. គ្រូ សុភា)', style: 'flex:1;min-width:160px;' });
  const fresh = h('div', {});
  const table = h('div', { style: 'overflow-x:auto;margin-top:12px;' });

  async function loadCodes() {
    const { codes } = await api('/api/admin/codes');
    table.innerHTML = '';
    if (!codes.length) return;
    table.append(h('table', {}, [
      h('thead', {}, h('tr', {}, ['កូដ', 'រយៈពេល', 'កំណត់សម្គាល់', 'ស្ថានភាព', ''].map((x) => h('th', {}, x)))),
      h('tbody', {}, codes.map((c) => h('tr', {}, [
        h('td', {}, h('span', { class: 'pin-chip', style: c.used_at ? 'opacity:.45;' : '' }, c.code)),
        h('td', {}, MONTH_LABELS[c.months] || `${c.months} ខែ`),
        h('td', { class: 'muted' }, c.note || ''),
        h('td', {}, c.used_at ? h('span', { class: 'chip chip-closed' }, `បានប្រើ · ${c.used_by_name} · ${fmtDateTime(c.used_at).split(',')[0]}`) : h('span', { class: 'chip chip-open' }, 'មិនទាន់ប្រើ')),
        h('td', {}, c.used_at ? null : h('div', { class: 'row', style: 'gap:4px;flex-wrap:nowrap;' }, [
          h('button', { class: 'secondary btn-sm', onclick: async (e) => { await copyText(c.code); e.target.textContent = '✓'; } }, '📋'),
          h('button', { class: 'danger btn-sm', onclick: async () => { await api(`/api/admin/codes/${c.id}`, { method: 'DELETE' }); loadCodes(); } }, 'លុប'),
        ])),
      ]))),
    ]));
  }

  const card = h('div', { class: 'card' }, [
    h('h2', {}, '🎟 កូដដោះសោ'),
    h('p', { class: 'muted' }, 'បង្កើតកូដឱ្យគ្រូដែលបានទិញ។ កូដនីមួយៗប្រើបានតែម្តង ហើយដោះសោគណនីគ្រូតាមរយៈពេលដែលបានជ្រើស។'),
    h('div', { class: 'row' }, [
      sel, h('span', { class: 'muted' }, 'ចំនួន'), count, note,
      h('button', { onclick: async () => {
        try {
          const r = await api('/api/admin/codes', { method: 'POST', body: { months: Number(sel.value), count: Number(count.value), note: note.value } });
          fresh.innerHTML = '';
          const text = r.codes.join('\n');
          fresh.append(h('div', { class: 'notice' }, [
            h('div', { style: 'font-weight:600;margin-bottom:6px;' }, `✅ បានបង្កើត ${r.codes.length} កូដ (${MONTH_LABELS[r.months]})`),
            ...r.codes.map((c) => h('div', {}, h('span', { class: 'pin-chip' }, c))),
            h('button', { style: 'margin-top:8px;', onclick: async (e) => { await copyText(text); e.target.textContent = '✓ បានចម្លង'; } }, '📋 ចម្លងទាំងអស់'),
          ]));
          note.value = '';
          loadCodes();
        } catch (e) { Exam.notify(e.message); }
      } }, '＋ បង្កើតកូដ'),
    ]),
    fresh, table,
  ]);
  loadCodes();
  return card;
}

async function settingsCard() {
  const st = await api('/api/admin/settings');
  const open = h('input', { type: 'checkbox', checked: st.signup_open ? 'checked' : null, style: 'width:18px;height:18px;' });
  const contact = h('input', { type: 'text', value: st.contact_text, placeholder: 'ឧ. Telegram @yourname · 012 345 678', style: 'flex:1;min-width:220px;' });
  return h('div', { class: 'card' }, [
    h('h2', {}, '⚙ ការកំណត់'),
    h('label', { class: 'setup-check', style: 'margin:0 0 12px;' }, [open, ' អនុញ្ញាតឱ្យគ្រូចុះឈ្មោះដោយខ្លួនឯង (បង្កើតគណនីសាកល្បង)']),
    h('label', {}, 'ព័ត៌មានទំនាក់ទំនងដើម្បីស្នើសុំកូដ (បង្ហាញដល់គ្រូដែលមិនទាន់ដោះសោ)'),
    h('div', { class: 'row' }, [contact, h('button', { onclick: async () => {
      await api('/api/admin/settings', { method: 'POST', body: { signup_open: open.checked, contact_text: contact.value } });
      Exam.notify('បានរក្សាទុក។');
    } }, 'រក្សាទុក')]),
  ]);
}

async function auditCard() {
  const { log } = await api('/api/admin/audit');
  const body = h('div', { hidden: 'hidden', style: 'overflow-x:auto;margin-top:10px;' }, h('table', {}, [
    h('thead', {}, h('tr', {}, ['ពេលវេលា', 'អ្នកធ្វើ', 'សកម្មភាព', 'ព័ត៌មាន'].map((x) => h('th', {}, x)))),
    h('tbody', {}, log.map((r) => h('tr', {}, [h('td', { class: 'muted', style: 'white-space:nowrap;' }, fmtDateTime(r.at)), h('td', {}, r.who || '—'), h('td', {}, h('code', {}, r.action)), h('td', { class: 'muted' }, r.detail || '')]))),
  ]));
  return h('div', { class: 'card' }, [
    h('div', { class: 'row', style: 'justify-content:space-between;' }, [h('h2', { style: 'margin:0;' }, `🧾 កំណត់ហេតុសកម្មភាព (${log.length})`), h('button', { class: 'secondary btn-sm', onclick: () => { body.hidden = !body.hidden; } }, 'បង្ហាញ/លាក់')]),
    body,
  ]);
}
