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
  const reqData = await api('/api/admin/unlock-requests').catch(() => ({ requests: [], pending: 0 }));
  container.append(requestsCard(reqData, () => render.teachers()));

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
  const previousFocus = document.activeElement;
  const previousOverflow = document.body.style.overflow;
  const close = () => { back.remove(); document.body.style.overflow = previousOverflow; previousFocus?.focus(); };
  const back = h('div', { class: 'modal-back share-back', onclick: e => { if (e.target === back) close(); } });
  const box = h('div', { class: 'modal-box share-dialog', role: 'dialog', 'aria-modal': 'true', 'aria-labelledby': 'share-dialog-title' });
  const status = h('p', { class: 'share-status', role: 'status', 'aria-live': 'polite' });
  const report = (message, error = false) => { status.textContent = message; status.classList.toggle('is-error', error); };
  const role = h('select', { id: 'share-role' }, Object.entries(ROLE_NAMES).map(([v, l]) => h('option', { value: v }, l)));
  const roleHint = h('p', { class: 'share-help' });
  const updateHint = () => { roleHint.textContent = role.value === 'editor' ? 'អាចមើល និងកែសម្រួល។ ជ្រើសសិទ្ធិនេះសម្រាប់គ្រូដែលធ្វើការជាមួយអ្នក។' : 'អាចមើល និងផ្តល់ចំណាំ។ មិនអាចកែសំណួរបានទេ។'; };
  role.addEventListener('change', updateHint); updateHint();
  const q = h('input', { id: 'share-username', type: 'text', placeholder: 'ឧ. sokli', autocomplete: 'off', autocapitalize: 'none', spellcheck: 'false', 'aria-label': 'ឈ្មោះអ្នកប្រើប្រាស់', 'aria-describedby': 'share-search-help' });
  const results = h('div', { class: 'share-results', 'aria-live': 'polite' });
  const current = h('div', { class: 'share-people' });
  const count = h('span', { class: 'share-count' }, '0');
  let sharedIds = new Set(), searchVersion = 0;
  async function drawCurrent() {
    const { shares } = await api(`/api/shares?type=${type}&id=${id}`);
    sharedIds = new Set(shares.map(s => s.teacher_id)); count.textContent = String(shares.length);
    current.replaceChildren();
    if (!shares.length) current.append(h('p', { class: 'share-empty' }, 'មានតែអ្នកប៉ុណ្ណោះដែលអាចចូលមើល។'));
    shares.forEach(s => {
      const permission = h('select', { 'aria-label': `សិទ្ធិ ${s.username}`, onchange: async () => {
        const before = s.role; permission.disabled = true;
        try { await api('/api/shares', { method: 'POST', body: { type, id, teacher_id: s.teacher_id, role: permission.value } }); s.role = permission.value; report('បានកែសិទ្ធិរួចរាល់។'); }
        catch(e) { permission.value = before; report(e.message, true); }
        finally { permission.disabled = false; }
      } }, Object.entries(ROLE_NAMES).map(([v]) => h('option', { value: v, selected: v === s.role ? 'selected' : null }, v === 'reviewer' ? 'អ្នកពិនិត្យ' : 'អ្នកកែសម្រួល')));
      const remove = h('button', { class: 'secondary share-remove', 'aria-label': `ដកសិទ្ធិ ${s.username}`, onclick: async () => {
        remove.disabled = true;
        try { await api('/api/shares/remove', { method: 'POST', body: { type, id, teacher_id: s.teacher_id } }); await drawCurrent(); report(`បានដកសិទ្ធិ ${s.username}។`); }
        catch(e) { report(e.message, true); remove.disabled = false; }
      } }, 'ដកចេញ');
      current.append(h('div', { class: 'share-person' }, [h('div', { class: 'share-person-name' }, [h('strong', {}, s.name), h('small', {}, `@${s.username}`)]), h('div', { class: 'share-person-actions' }, [permission, remove])]));
    });
  }
  const search = h('button', { onclick: runSearch }, 'ស្វែងរក');
  async function runSearch() {
    const version = ++searchVersion, username = q.value.trim();
    results.replaceChildren();
    if (!username) { q.focus(); return; }
    search.disabled = true; search.textContent = 'កំពុងស្វែងរក…';
    try {
      const { teachers } = await api(`/api/teachers/search?q=${encodeURIComponent(username)}`);
      if (version !== searchVersion || q.value.trim() !== username) return;
      if (!teachers.length) results.append(h('p', { class: 'share-empty' }, 'រកមិនឃើញ។ សូមពិនិត្យ username ពេញរបស់គ្រូ។'));
      teachers.forEach(t => {
        const add = h('button', { class: 'btn-sm', disabled: sharedIds.has(t.id) ? 'disabled' : null, onclick: async () => {
          add.disabled = true;
          try { await api('/api/shares', { method: 'POST', body: { type, id, teacher_id: t.id, role: role.value } }); await drawCurrent(); results.replaceChildren(); q.value = ''; report(`បានចែករំលែកជាមួយ ${t.username}។`); q.focus(); }
          catch(e) { report(e.message, true); add.disabled = false; }
        } }, sharedIds.has(t.id) ? 'មានសិទ្ធិរួចហើយ' : '+ បន្ថែម');
        results.append(h('div', { class: 'share-person' }, [h('div', { class: 'share-person-name' }, [h('strong', {}, t.name), h('small', {}, `@${t.username}`)]), add]));
      });
    } catch(e) { if (version === searchVersion) report(e.message, true); }
    finally { search.disabled = false; search.textContent = 'ស្វែងរក'; }
  }
  q.addEventListener('input', () => { searchVersion++; results.replaceChildren(); });
  q.addEventListener('keydown', e => { if (e.key === 'Enter') { e.preventDefault(); runSearch(); } });
  const links = h('div', { class: 'share-links' });
  const linkSlot = h('div', { class: 'share-link-slot' });
  async function drawLinks() {
    if (type !== 'test') return;
    try {
      const data = await api(`/api/share-links?test_id=${id}`);
      links.replaceChildren(...data.links.map(link => {
        const revoke = h('button', { class: 'secondary share-remove', onclick: async () => {
          revoke.disabled = true;
          try { await api(`/api/share-links/${link.id}`, { method: 'DELETE' }); linkSlot.replaceChildren(); await drawLinks(); report('បានដកតំណអញ្ជើញ។'); }
          catch(e) { report(e.message, true); revoke.disabled = false; }
        } }, 'ដកតំណចេញ');
        return h('div', { class: 'share-person' }, [h('div', { class: 'share-person-name' }, [h('strong', {}, link.role === 'editor' ? 'អ្នកកែសម្រួល' : 'អ្នកពិនិត្យ'), h('small', {}, `ផុតកំណត់ ${fmtDateTime(link.expires_at)}`)]), revoke]);
      }));
    } catch(e) { report(e.message, true); }
  }
  const linkButton = h('button', { class: 'secondary', onclick: async () => {
    linkButton.disabled = true;
    try {
      const data = await api('/api/share-links', { method: 'POST', body: { test_id: id, role: role.value } });
      const input = h('input', { type: 'text', readonly: 'readonly', value: `${location.origin}/teacher.html?share=${data.token}`, 'aria-label': 'តំណអញ្ជើញ', onfocus: e => e.target.select() });
      const copy = h('button', { onclick: async () => { const ok = await copyText(input.value); if (ok) report('បានចម្លងតំណ។ ផ្ញើទៅគ្រូដែលអ្នកចង់អញ្ជើញ។'); else { input.focus(); input.select(); report('សូមចម្លងតំណពីប្រអប់ខាងលើ។'); } } }, 'ចម្លងតំណ');
      linkSlot.replaceChildren(h('div', { class: 'share-search-row' }, [input, copy]));
      await drawLinks(); report('តំណរួចរាល់។ ប្រើបានម្ដង ហើយផុតកំណត់ក្នុង ៧ ថ្ងៃ។');
    } catch(e) { report(e.message, true); }
    finally { linkButton.disabled = false; }
  } }, 'បង្កើតតំណអញ្ជើញ');
  const usernamePane = h('section', { class: 'share-method', id: 'share-username-pane' }, [h('label', { for: 'share-username' }, 'ឈ្មោះអ្នកប្រើប្រាស់ពេញ'), h('div', { class: 'share-search-row' }, [q, search]), h('p', { id: 'share-search-help', class: 'share-help' }, 'ស្វែងរកតាម username ពេញ។ បញ្ជីគណនីគ្រូទាំងអស់មិនត្រូវបានបង្ហាញទេ។'), results]);
  const linkPane = h('section', { class: 'share-method', id: 'share-link-pane', hidden: 'hidden' }, [h('p', { class: 'share-help' }, 'គ្រូដែលទទួលតំណត្រូវចូលគណនី និងទទួលការអញ្ជើញ។ តំណប្រើបានម្ដង និងមានសុពលភាព ៧ ថ្ងៃ។'), linkButton, linkSlot, links]);
  const methodButtons = [];
  const methods = h('div', { class: 'share-methods', 'aria-label': 'វិធីចែករំលែក' }, ['តាម username', 'តាមតំណអញ្ជើញ'].slice(0, type === 'test' ? 2 : 1).map((label, index) => {
    const button = h('button', { class: index === 0 ? 'active' : '', 'aria-pressed': String(index === 0), 'aria-controls': index ? 'share-link-pane' : 'share-username-pane', onclick: () => {
      usernamePane.hidden = index !== 0; linkPane.hidden = index === 0;
      methodButtons.forEach((b, i) => { b.classList.toggle('active', i === index); b.setAttribute('aria-pressed', String(i === index)); });
      if (index === 0) q.focus();
    } }, label); methodButtons.push(button); return button;
  }));
  box.append(h('header', { class: 'share-header' }, [h('div', {}, [h('h2', { id: 'share-dialog-title' }, 'ចែករំលែក'), h('p', { class: 'share-resource', title }, title)]), h('button', { class: 'secondary share-close', 'aria-label': 'បិទការចែករំលែក', onclick: close }, '×')]),
    h('div', { class: 'share-body' }, [h('section', { class: 'share-permission' }, [h('label', { for: 'share-role' }, 'សិទ្ធិសម្រាប់ការចែករំលែកថ្មី'), role, roleHint]), methods, usernamePane, type === 'test' ? linkPane : null,
      h('section', { class: 'share-access' }, [h('h3', {}, ['អ្នកដែលមានសិទ្ធិចូល ', count]), current])]),
    h('footer', { class: 'share-footer' }, [status, h('button', { class: 'secondary', onclick: close }, 'រួចរាល់')]));
  box.addEventListener('keydown', e => {
    if (e.key === 'Escape') { e.preventDefault(); close(); }
    if (e.key !== 'Tab') return;
    const focusable = [...box.querySelectorAll('button:not(:disabled),input:not(:disabled),select:not(:disabled),[tabindex="0"]')].filter(el => el.getClientRects().length);
    const first = focusable[0], last = focusable[focusable.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  });
  back.append(box); document.body.append(back); document.body.style.overflow = 'hidden'; q.focus();
  drawLinks(); drawCurrent().catch(e => report(e.message, true));
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

// Restore: always verify first (writes nothing), then put back only the rows that are missing.
function restoreCard(backups) {
  const pick = h('select', { style: 'min-width:220px;' }, [
    ...backups.map((b) => h('option', { value: b.id }, `${fmtDateTime(b.at)} (ទុកក្នុងប្រព័ន្ធ)`)),
    h('option', { value: 'file' }, 'ឯកសារ .json.gz ពីកុំព្យូទ័រ/Telegram…'),
  ]);
  const file = h('input', { type: 'file', accept: '.gz,.json.gz,application/gzip', hidden: 'hidden' });
  const out = h('div', {});
  pick.onchange = () => { file.hidden = pick.value !== 'file'; };
  file.hidden = pick.value !== 'file';
  let last = null;
  const request = async (what) => {
    const confirmQ = what === 'apply' ? 'confirm=RESTORE' : '';
    if (pick.value === 'file') {
      if (!file.files[0]) throw new Error('សូមជ្រើសរើសឯកសារបម្រុងទុកជាមុន។');
      return api(`/api/admin/restore/${what}?${confirmQ}`, { method: 'POST', body: await file.files[0].arrayBuffer(), contentType: 'application/gzip' });
    }
    return api(`/api/admin/restore/${what}?backup_id=${pick.value}&${confirmQ}`, { method: 'POST' });
  };
  const KH = { classes: 'ថ្នាក់', students: 'សិស្ស', tests: 'តេស្ត', test_questions: 'សំណួរ', test_sessions: 'ការប្រឡង', session_questions: 'សំណួរដែលបានរក្សា', results: 'លទ្ធផល', responses: 'ចម្លើយ', writing_marks: 'ពិន្ទុសរសេរ', assessments: 'ការវាយតម្លៃឆ្នាំ', manual_scores: 'ពិន្ទុដោយដៃ', question_notes: 'កំណត់សម្គាល់', shares: 'ការចែករំលែក' };
  const verify = h('button', { class: 'secondary', onclick: async (e) => {
    e.target.disabled = true; out.innerHTML = '';
    try {
      last = await request('verify');
      const rows = last.tables.filter((t) => t.in_backup || t.in_live);
      out.append(
        h('p', { class: 'muted' }, `ការបម្រុងទុកនេះបង្កើតនៅ ${fmtDateTime(last.exported_at)} — ការផ្ទៀងផ្ទាត់មិនបានកែអ្វីទេ។`),
        h('table', {}, [h('thead', {}, h('tr', {}, ['តារាង', 'ក្នុងការបម្រុងទុក', 'ក្នុងប្រព័ន្ធឥឡូវ', 'បាត់ (អាចស្ដារ)', 'មិនអាចស្ដារ'].map((x) => h('th', {}, x)))),
          h('tbody', {}, rows.map((t) => h('tr', {}, [h('td', {}, KH[t.table] || t.table), h('td', {}, t.in_backup), h('td', {}, t.in_live), h('td', { style: t.missing ? 'font-weight:700;color:#8a5a0d;' : '' }, t.missing), h('td', {}, t.orphans || '—')])))]),
        last.total_missing
          ? h('div', { style: 'margin-top:12px;' }, [h('div', { class: 'callout warn' }, `អាចស្ដារបាន ${last.total_missing} ជួរដែលបាត់។ ជួរដែលមានស្រាប់នឹងមិនត្រូវបានប៉ះពាល់ទេ — ប្រព័ន្ធនឹងបម្រុងទុកថ្មីមួយជាមុនសិន។`),
              h('button', { class: 'danger', onclick: async (ev) => {
                if (!(await Exam.confirm(`ស្ដារ ${last.total_missing} ជួរដែលបាត់ពីការបម្រុងទុកនេះ? សកម្មភាពនេះបន្ថែមតែទិន្នន័យដែលបាត់ ហើយមិនលុប ឬសរសេរជាន់អ្វីទេ។`))) return;
                ev.target.disabled = true;
                try {
                  const r = await request('apply');
                  await Exam.notify(`✅ បានស្ដារ ${r.total_inserted} ជួរ${r.images ? ` និងរូបភាព ${r.images}` : ''}។ (ប្រព័ន្ធបានបម្រុងទុកថ្មីមួយមុនស្ដារ)`);
                  verify.click();
                } catch (er) { ev.target.disabled = false; Exam.notify(er.message); }
              } }, '♻ ស្ដារទិន្នន័យដែលបាត់')])
          : h('div', { class: 'callout good' }, '✓ គ្មានអ្វីបាត់ទេ — ទិន្នន័យទាំងអស់នៅក្នុងការបម្រុងទុកមាននៅក្នុងប្រព័ន្ធរួចហើយ។'),
      );
    } catch (er) { out.append(h('div', { class: 'error' }, er.message)); }
    e.target.disabled = false;
  } }, '🔍 ផ្ទៀងផ្ទាត់ (មិនកែអ្វីទេ)');
  return h('div', { style: 'margin-top:18px;' }, [
    h('h3', {}, '♻ ស្ដារទិន្នន័យពីការបម្រុងទុក'),
    h('p', { class: 'muted' }, 'ប្រើពេលលុបថ្នាក់ សិស្ស ឬលទ្ធផលដោយចៃដន្យ។ ជំហានទី១ «ផ្ទៀងផ្ទាត់» បង្ហាញអ្វីដែលបាត់ ដោយមិនកែអ្វីទាំងអស់។ ការស្ដារបន្ថែមតែជួរដែលបាត់ ហើយមិនសរសេរជាន់ការងារថ្មីៗទេ។ ដើម្បីត្រឡប់ទាំងមូលទៅម៉ោងមុន សូមមើលឯកសារ RESTORE.md។'),
    h('div', { class: 'row' }, [pick, file, verify]),
    out,
  ]);
}

// Housekeeping: prove the backup works, and free space taken by pictures nobody uses.
function maintenanceCard() {
  const out = h('div', {});
  return h('div', { style: 'margin-top:18px;' }, [
    h('h3', {}, '🧰 ថែទាំប្រព័ន្ធ'),
    h('div', { class: 'row', style: 'gap:8px;flex-wrap:wrap;' }, [
      h('button', { class: 'secondary', onclick: async () => {
        out.innerHTML = '';
        try {
          const r = await api('/api/admin/backup-check', { method: 'POST' });
          out.append(h('div', { class: `callout ${r.ok ? 'good' : 'bad'}` }, r.ok ? `✓ ការបម្រុងទុកចុងក្រោយ (${fmtDateTime(r.at)}) អាចអានបាន — សិស្ស ${r.tables.students}, លទ្ធផល ${r.tables.results}។ ប្រព័ន្ធពិនិត្យដោយស្វ័យប្រវត្តិរៀងរាល់សប្តាហ៍។` : `✗ មានបញ្ហា៖ ${r.problem}`));
        } catch (e) { out.append(h('div', { class: 'error' }, e.message)); }
      } }, '✅ ពិនិត្យថាការបម្រុងទុកអាចប្រើបាន'),
      h('button', { class: 'secondary', onclick: async () => {
        out.innerHTML = '';
        try {
          const r = await api('/api/admin/images/unused');
          out.append(h('div', { class: 'callout' }, `រូបភាពសរុប ${r.total} (${r.total_kb} KB) · មិនប្រើ ${r.unused} (${r.unused_kb} KB)`),
            r.unused ? h('button', { class: 'danger btn-sm', onclick: async () => { if (!(await Exam.confirm(`លុបរូបភាពមិនប្រើ ${r.unused}? រូបភាពដែលសំណួរ ឬវិញ្ញាបនបត្រកំពុងប្រើ មិនត្រូវបានលុបទេ។`))) return; const d = await api('/api/admin/images/cleanup', { method: 'POST' }); out.append(h('div', { class: 'callout good' }, `✓ បានលុប ${d.deleted}`)); } }, '🗑 លុបរូបភាពមិនប្រើ') : null);
        } catch (e) { out.append(h('div', { class: 'error' }, e.message)); }
      } }, '🖼 ពិនិត្យរូបភាពមិនប្រើ'),
    ]),
    out,
  ]);
}

async function settingsCard() {
  const st = await api('/api/admin/settings');
  const open = h('input', { type: 'checkbox', checked: st.signup_open ? 'checked' : null, style: 'width:18px;height:18px;' });
  const contact = h('input', { type: 'text', value: st.contact_text, placeholder: 'ឧ. Telegram @yourname · 012 345 678', style: 'flex:1;min-width:220px;' });
  const tgToken = h('input', { type: 'password', placeholder: st.telegram_set ? '•••••• (បានកំណត់ — វាយថ្មីដើម្បីប្តូរ)' : 'Bot token ពី @BotFather', style: 'flex:1;min-width:200px;', autocomplete: 'off' });
  const tgChat = h('input', { type: 'text', value: st.telegram_chat_id, placeholder: 'Chat ID របស់អ្នក', style: 'width:170px;' });
  const { backups } = await api('/api/admin/backups');
  const backupBox = h('div', {});
  const drawBackups = (list) => {
    backupBox.innerHTML = '';
    backupBox.append(list.length
      ? h('div', {}, list.map((b) => h('div', { class: 'list-item' }, [h('span', {}, `${fmtDateTime(b.at)} · ${b.reason === 'weekly' ? 'ស្វ័យប្រវត្តិ' : 'ដោយដៃ'} · ${Math.round(b.size_bytes / 1024)} KB`), h('a', { class: 'btn secondary btn-sm', href: `/api/admin/backups/${b.id}/download` }, '⬇ ទាញយក')])))
      : h('p', { class: 'muted' }, 'មិនទាន់មានការបម្រុងទុកទេ — ចុច «បម្រុងទុកឥឡូវនេះ»។'));
  };
  drawBackups(backups);
  const backupCard = [
    h('h3', { style: 'margin-top:18px;' }, '💾 ការបម្រុងទុកទាំងប្រព័ន្ធ'),
    h('p', { class: 'muted' }, 'ប្រព័ន្ធបម្រុងទុកដោយស្វ័យប្រវត្តិរៀងរាល់ថ្ងៃចន្ទ ម៉ោង ៣ ព្រឹក (រក្សាទុក ៤ ច្បាប់ចុងក្រោយ)។ បើបានកំណត់ Telegram ឯកសារពេញលេញ (រួមទាំងរូបភាព) នឹងផ្ញើមកអ្នកផង។ ឯកសារ .json.gz ជាច្បាប់ចម្លងទិន្នន័យទាំងអស់ លើកលែងពាក្យសម្ងាត់។'),
    h('button', { onclick: async (e) => {
      e.target.disabled = true; e.target.textContent = '⏳ កំពុងបម្រុងទុក…';
      try { const r = await api('/api/admin/backup-now', { method: 'POST' }); const d = await api('/api/admin/backups'); drawBackups(d.backups); Exam.notify(`✅ បានបម្រុងទុក (${r.size_kb} KB)${r.telegram ? ' និងផ្ញើទៅ Telegram' : ''}${r.stored ? '' : ' — ធំពេកសម្រាប់ទុកក្នុងប្រព័ន្ធ សូមប្រើ Telegram'}។`); }
      catch (er) { Exam.notify(er.message); }
      e.target.disabled = false; e.target.textContent = '💾 បម្រុងទុកឥឡូវនេះ';
    } }, '💾 បម្រុងទុកឥឡូវនេះ'),
    backupBox,
    restoreCard(backups),
    maintenanceCard(),
  ];
  return h('div', { class: 'card' }, [
    h('h2', {}, '⚙ ការកំណត់'),
    h('label', { class: 'setup-check', style: 'margin:0 0 12px;' }, [open, ' អនុញ្ញាតឱ្យគ្រូចុះឈ្មោះដោយខ្លួនឯង (បង្កើតគណនីសាកល្បង)']),
    h('label', {}, 'ព័ត៌មានទំនាក់ទំនងដើម្បីស្នើសុំកូដ (បង្ហាញដល់គ្រូដែលមិនទាន់ដោះសោ)'),
    h('div', { class: 'row' }, [contact, h('button', { onclick: async () => {
      await api('/api/admin/settings', { method: 'POST', body: { signup_open: open.checked, contact_text: contact.value } });
      Exam.notify('បានរក្សាទុក។');
    } }, 'រក្សាទុក')]),
    h('h3', { style: 'margin-top:18px;' }, '🔔 ការជូនដំណឹងតាម Telegram (ជម្រើស)'),
    h('p', { class: 'muted' }, 'ទទួលសារពេលមានគ្រូចុះឈ្មោះថ្មី ឬដោះសោដោយកូដ។ បង្កើត Bot ជាមួយ @BotFather, ផ្ញើ /start ទៅ Bot, ហើយយក Chat ID ពី @userinfobot។'),
    h('div', { class: 'row' }, [tgToken, tgChat,
      h('button', { onclick: async () => {
        await api('/api/admin/settings', { method: 'POST', body: { telegram_token: tgToken.value, telegram_chat_id: tgChat.value } });
        tgToken.value = '';
        Exam.notify('បានរក្សាទុក។ ចុច «សាកល្បងផ្ញើ» ដើម្បីពិនិត្យ។');
      } }, 'រក្សាទុក'),
      h('button', { class: 'secondary', onclick: async () => { try { await api('/api/admin/telegram-test', { method: 'POST' }); Exam.notify('✅ បានផ្ញើសារសាកល្បងហើយ។'); } catch (e) { Exam.notify(e.message); } } }, 'សាកល្បងផ្ញើ'),
    ]),
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

// ---------- unlock requests (owner) ----------
function requestsCard(data, reload) {
  const PLAN = { month: ['១ ខែ', '$2.99', 1], year: ['១ ឆ្នាំ', '$15', 12] };
  const pending = data.requests.filter((r) => r.status === 'pending');
  const card = h('div', { class: 'card req-card' }, [
    h('h2', {}, ['🔔 សំណើសុំដោះសោ ', pending.length ? h('span', { class: 'req-badge inline' }, pending.length) : h('span', { class: 'muted' }, '(គ្មានសំណើថ្មី)')]),
  ]);
  if (!data.requests.length) { card.append(h('p', { class: 'muted' }, 'នៅពេលគ្រូសាកល្បងចុច «ស្នើសុំដោះសោ» ឈ្មោះគាត់នឹងបង្ហាញទីនេះ ជាមួយសញ្ញាក្រហម។')); return card; }
  for (const r of data.requests.slice(0, 20)) {
    if (r.plan === 'reset') { card.append(resetRow(r, reload)); continue; }
    const pl = PLAN[r.plan] || [r.plan, '', 1];
    const isPending = r.status === 'pending';
    const tg = /^@?[A-Za-z0-9_]{4,}$/.test(r.contact || '') ? h('a', { href: `https://t.me/${r.contact.replace('@', '')}`, target: '_blank', rel: 'noopener' }, `💬 ${r.contact}`) : (r.contact || '—');
    card.append(h('div', { class: `list-item req-row${isPending ? ' is-new' : ''}` }, [
      h('div', {}, [
        h('b', {}, r.name), ` (@${r.username}) `,
        h('span', { class: `badge ${isPending ? 'warn' : 'upcoming'}` }, isPending ? 'រង់ចាំ' : r.status === 'done' ? 'ដោះសោរួច' : 'ច្រានចោល'),
        h('div', { class: 'muted' }, ['គម្រោង ', h('b', {}, `${pl[0]} ${pl[1]}`), ' · ទាក់ទង៖ ', tg, ` · ${fmtDateTime(r.created_at)}`]),
      ]),
      isPending ? h('div', { class: 'row', style: 'gap:6px;' }, [
        h('button', { onclick: async () => {
          if (!confirm(`ដោះសោ ${r.name} ${pl[0]}? (សូមប្រាកដថាបានទទួលប្រាក់ ${pl[1]} ហើយ)`)) return;
          await api(`/api/admin/teachers/${r.teacher_id}/license`, { method: 'POST', body: { action: 'grant', months: pl[2] } });
          if (window.refreshRequestBadge) window.refreshRequestBadge(); reload();
        } }, `✅ ដោះសោ ${pl[0]}`),
        h('button', { class: 'ghost', onclick: async () => { await api(`/api/admin/unlock-requests/${r.id}/dismiss`, { method: 'POST' }); if (window.refreshRequestBadge) window.refreshRequestBadge(); reload(); } }, 'ច្រានចោល'),
      ]) : null,
    ]));
  }
  return card;
}

// A teacher who forgot the password: the owner makes a one-time reset link and sends it (Telegram etc.).
function resetRow(r, reload) {
  const isPending = r.status === 'pending';
  const slot = h('div', {});
  return h('div', { class: `list-item req-row${isPending ? ' is-new' : ''}`, style: 'flex-wrap:wrap;' }, [
    h('div', {}, [
      h('b', {}, r.name), ` (@${r.username}) `,
      h('span', { class: `badge ${isPending ? 'warn' : 'upcoming'}` }, isPending ? '🔑 ភ្លេចពាក្យសម្ងាត់' : 'បានដោះស្រាយ'),
      h('div', { class: 'muted' }, ['ទាក់ទង៖ ', r.contact || '—', ` · ${fmtDateTime(r.created_at)}`]),
    ]),
    isPending ? h('div', { class: 'row', style: 'gap:6px;' }, [
      h('button', { onclick: async () => {
        const x = await api(`/api/admin/teachers/${r.teacher_id}/reset-link`, { method: 'POST' });
        slot.innerHTML = ''; slot.append(linkBox(inviteUrl(x.token), `តំណកំណត់ពាក្យសម្ងាត់ថ្មីសម្រាប់ ${r.name} — ផ្ញើទៅគាត់`));
        await api(`/api/admin/unlock-requests/${r.id}/dismiss`, { method: 'POST' }).catch(() => {});
        if (window.refreshRequestBadge) window.refreshRequestBadge();
      } }, '🔑 បង្កើតតំណកំណត់ថ្មី'),
    ]) : null,
    slot,
  ]);
}


// A sharing link grants access only after the signed-in teacher accepts it.
async function openTestInvitation() {
  const token = new URLSearchParams(location.search).get('share');
  if (!token) return;
  const clear = () => { const url = new URL(location.href); url.searchParams.delete('share'); history.replaceState(null, '', url); };
  try {
    const data = await api(`/api/share-invitation/${encodeURIComponent(token)}`);
    const back = h('div', { class: 'modal-back' });
    const accept = h('button', { onclick: async () => {
      accept.disabled = true;
      try {
        const result = await api(`/api/share-invitation/${encodeURIComponent(token)}`, { method: 'POST' });
        clear(); back.remove(); selectedTestId = result.test_id;
        document.querySelector('[data-tab=tests]').click();
      } catch (e) { Exam.notify(e.message); }
      finally { accept.disabled = false; }
    } }, 'ទទួលការអញ្ជើញ');
    back.append(h('div', { class: 'modal-box' }, [h('h2', {}, 'ការអញ្ជើញចែករំលែកតេស្ត'),
      h('p', {}, data.title), h('p', {}, ROLE_NAMES[data.role]),
      h('div', { class: 'row' }, [h('button', { class: 'secondary', onclick: () => { clear(); back.remove(); } }, 'បោះបង់'), accept])]));
    document.body.append(back);
  } catch (e) { clear(); Exam.notify(e.message); }
}
