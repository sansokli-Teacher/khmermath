// Shared lesson summary for bank selections and test drafts.
function lessonSelectionSummary(questions) {
  const groups = new Map();
  for (const q of questions) {
    const key = JSON.stringify([q.grade || '', q.lesson || '']);
    if (!groups.has(key)) groups.set(key, { grade: q.grade, lesson: q.lesson, count: 0, points: 0 });
    const group = groups.get(key);
    group.count++;
    group.points += Number.isFinite(Number(q.points)) ? Number(q.points) : 0;
  }
  return h('div', { class: 'tp-lesson-summary', 'aria-label': 'សរុបតាមមេរៀន' }, [...groups.values()].map(g =>
    h('div', { class: 'tp-lesson-total' }, [h('span', {}, `${g.grade ? 'ថ្នាក់ទី ' + g.grade + ' · ' : ''}${g.lesson || 'មិនទាន់កំណត់មេរៀន'}`), h('strong', {}, `${g.count} សំណួរ · ${Math.round(g.points * 10000) / 10000} ពិន្ទុ`)])));
}
// Only IDs and teacher-entered settings are stored, scoped to the signed-in teacher.
function testDraftKey(name) {
  return `exam-test-draft:v1:${typeof ME !== 'undefined' && ME ? ME.id : 'guest'}:${name}`;
}
function readTestDraft(name) {
  try { return JSON.parse(localStorage.getItem(testDraftKey(name)) || 'null'); } catch { return null; }
}
function writeTestDraft(name, value) {
  try { localStorage.setItem(testDraftKey(name), JSON.stringify(value)); return true; } catch { return false; }
}
function restoreTestSelection(saved, questions) {
  const byId = new Map(questions.map(q => [q.id, q]));
  const selected = new Map();
  for (const item of Array.isArray(saved) ? saved : []) {
    if (!Array.isArray(item)) continue;
    const [id, points] = item, q = byId.get(id);
    if (q) selected.set(id, { ...q, points: typeof points === 'number' && Number.isFinite(points) && points > 0 ? points : NaN });
  }
  return selected;
}
function moveTestSelection(selected, id, direction) {
  const entries = [...selected], index = entries.findIndex(([key]) => key === id), next = index + direction;
  if (index < 0 || next < 0 || next >= entries.length) return;
  [entries[index], entries[next]] = [entries[next], entries[index]];
  selected.clear(); entries.forEach(([key, value]) => selected.set(key, value));
}
function randomTestQuestions(pool, count, random = Math.random) {
  const shuffled = [...pool];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled.slice(0, count);
}
async function buildTestPicker(test, container, options = {}) {
  const isNew = !test.id, draftName = isNew ? 'new' : `test-${test.id}`;
  const root = h('section', { class: 'test-picker card' });
  root.append(h('p', {}, 'កំពុងផ្ទុកធនាគារសំណួរ…'));
  let questions, curr;
  try { [{ questions }, curr] = await Promise.all([api('/api/bank'), loadCurr()]); }
  catch (e) {
    root.replaceChildren(h('p', { role: 'alert' }, e.message), h('button', { onclick: async () => root.replaceWith(await buildTestPicker(test, container, options)) }, 'ព្យាយាមម្ដងទៀត'));
    return root;
  }
  const stored = readTestDraft(draftName) || {};
  const keyOf = q => JSON.stringify([q.kind || 'mcq', q.stem_text, q.options]);
  const existing = new Set(test.questions.map(keyOf));
  const grades = [...new Set([...curr.grades, ...questions.map(q => q.grade).filter(Boolean)].map(String))];
  if (questions.some(q => !q.grade)) grades.push('');
  const state = {
    grade: grades.includes(stored.grade) ? stored.grade : String(test.questions.find(q => q.grade)?.grade || options.grade || grades[0] || ''),
    lesson: typeof stored.lesson === 'string' ? stored.lesson : null,
    selected: restoreTestSelection(stored.selected, questions),
    target: Number(stored.target) > 0 ? Number(stored.target) : 100,
    title: typeof stored.title === 'string' ? stored.title : '',
    quantities: stored.quantities && typeof stored.quantities === 'object' ? stored.quantities : {},
    draftId: Number.isInteger(stored.draftId) ? stored.draftId : null,
  };
  for (const q of questions) if (options.seed?.has(q.id) && !state.selected.has(q.id)) state.selected.set(q.id, { ...q, points: Number(q.points) > 0 ? Number(q.points) : 1 });
  for (const [id, q] of state.selected) if (existing.has(keyOf(q))) state.selected.delete(id);
  let busy = false, limit = 30;
  const side = h('nav', { class: 'tp-lessons', 'aria-label': 'មេរៀន' });
  const bank = h('div', { class: 'tp-bank', tabindex: '0', 'aria-label': 'ធនាគារសំណួរ' });
  const basket = h('aside', { class: 'tp-basket' });
  const lessonTotals = h('div');
  const totals = h('div', { class: 'tp-totals', role: 'status', 'aria-live': 'polite' });
  const draftStatus = h('small', { class: 'muted', role: 'status' });
  const progress = h('progress', { max: state.target, value: 0, 'aria-label': 'ពិន្ទុសរុបធៀបនឹងគោលដៅ' });
  const targetStatus = h('div', { role: 'status', 'aria-live': 'polite' });
  const preview = h('section', { class: 'tp-preview', hidden: 'hidden', 'aria-label': 'មើលតេស្តជាមុន' });
  const persist = () => {
    const ok = writeTestDraft(draftName, { ...state, selected: [...state.selected].map(([id, q]) => [id, q.points]) });
    draftStatus.textContent = ok ? 'បានរក្សាសម្រាងក្នុងកម្មវិធីរុករកនេះ' : 'មិនអាចរក្សាសម្រាងបាន — សូមរក្សាទុកតេស្តមុនចាកចេញ។';
  };
  const invalidate = () => { preview.hidden = true; persist(); };
  const title = h('input', { type: 'text', maxlength: '150', value: state.title, placeholder: 'ចំណងជើងតេស្តថ្មី', 'aria-label': 'ចំណងជើងតេស្ត', oninput: () => { state.title = title.value; invalidate(); } });
  const target = h('input', { type: 'number', min: '0.01', step: 'any', value: state.target, 'aria-label': 'ពិន្ទុគោលដៅ', oninput: () => { state.target = Number(target.value); updateTotal(); } });
  const grade = h('select', { 'aria-label': 'ថ្នាក់', onchange: () => { state.grade = grade.value; state.lesson = null; limit = 30; draw(); } }, grades.map(g => h('option', { value: g, selected: state.grade === g ? 'selected' : null }, g ? `ថ្នាក់ទី ${g}` : 'មិនទាន់កំណត់ថ្នាក់')));
  const search = h('input', { type: 'search', placeholder: 'ស្វែងរកសំណួរ…', 'aria-label': 'ស្វែងរកសំណួរ', oninput: () => { limit = 30; drawBank(); } });
  const kind = h('select', { 'aria-label': 'ប្រភេទសំណួរ', onchange: () => { limit = 30; drawBank(); } }, [['', 'គ្រប់ប្រភេទ'], ['mcq', 'ពហុជ្រើសរើស'], ['writing', 'សរសេរ']].map(([value, label]) => h('option', { value }, label)));
  const level = h('select', { 'aria-label': 'កម្រិតសំណួរ', onchange: () => { limit = 30; drawBank(); } }, [['', 'គ្រប់កម្រិត'], ['easy', 'ងាយ'], ['medium', 'មធ្យម'], ['hard', 'ពិបាក'], ['pisa', 'PISA']].map(([value, label]) => h('option', { value }, label)));
  const score = n => String(Math.round(n * 10000) / 10000);
  const savedTotal = test.questions.reduce((n, q) => n + Number(q.points), 0);
  const totalScore = () => savedTotal + [...state.selected.values()].reduce((n, q) => n + (Number.isFinite(q.points) ? q.points : 0), 0);
  const valid = () => {
    if (!state.selected.size) return false;
    if (isNew && !title.value.trim()) { title.focus(); return false; }
    if (!Number.isFinite(state.target) || state.target <= 0) { target.focus(); return false; }
    if (state.selected.size > 200) { Exam.notify('សូមជ្រើសយ៉ាងច្រើន ២០០ សំណួរក្នុងមួយលើក។'); return false; }
    if ([...state.selected.values()].some(q => !Number.isFinite(q.points) || q.points <= 0)) { Exam.notify('សូមកំណត់ពិន្ទុធំជាង ០ សម្រាប់គ្រប់សំណួរ។'); return false; }
    return true;
  };
  const controls = h('fieldset', { class: 'tp-controls' });
  const save = h('button', { onclick: async () => {
    if (busy || !valid()) return;
    busy = true; controls.disabled = true; save.disabled = true;
    try {
      let id = test.id || state.draftId;
      if (!id) { id = (await api('/api/tests', { method: 'POST', body: { title: title.value.trim() } })).id; state.draftId = id; persist(); }
      else if (isNew) await api(`/api/tests/${id}`, { method: 'PUT', body: { title: title.value.trim() } });
      const ids = [...state.selected.keys()];
      const result = await api(`/api/tests/${id}/questions/copy`, { method: 'POST', body: { question_ids: ids, points_by_id: Object.fromEntries([...state.selected].map(([qid, q]) => [qid, q.points])) } });
      for (const qid of result.copied_ids || ids.slice(0, result.copied)) state.selected.delete(qid);
      state.draftId = null; persist();
      if (isNew) { writeTestDraft(draftName, {}); await options.onCreated?.(id, ids); }
      else await renderTestBuilder(container);
    } catch (e) { Exam.notify(e.message); }
    finally { busy = false; controls.disabled = false; save.disabled = !state.selected.size; }
  } }, isNew ? 'បង្កើតតេស្ត' : 'បន្ថែមទៅតេស្ត');
  const review = h('button', { onclick: () => {
    if (!valid()) return;
    const all = [...test.questions, ...state.selected.values()];
    preview.replaceChildren(h('h2', {}, isNew ? title.value.trim() : test.title), lessonSelectionSummary(all), h('p', {}, `${all.length} សំណួរ · ${score(totalScore())} / ${score(state.target)} ពិន្ទុ`),
      h('p', { class: 'muted' }, 'ពិនិត្យសំណួរ និងចម្លើយ មុនរក្សាទុក។'),
      ...all.map((q, i) => {
        const sample = Exam.withSample(q);
        return h('article', { class: 'tp-question' }, [h('strong', {}, `${i + 1}. (${q.points} ពិន្ទុ)`), mathEl('div', {}, sample.stem_text), q.image_key ? h('img', { src: `/api/images/${q.image_key}`, alt: 'រូបភាពសំណួរ' }) : null,
          ...(sample.options || []).map((opt, j) => mathEl('div', { class: 'tp-option' }, `${j + 1}. ${opt}`)),
          h('details', {}, [h('summary', {}, 'ចម្លើយ / អត្រាកំណែ'), q.kind !== 'writing' ? mathEl('div', {}, sample.options?.[sample.correct_index ?? q.correct_index] || '—') : null, q.alt_correct_index != null ? mathEl('div', {}, sample.options?.[q.alt_correct_index] || '—') : null, mathEl('div', {}, sample.solution_text || q.solution_text || '—')])]);
      }), h('div', { class: 'row' }, [h('button', { class: 'secondary', onclick: () => { preview.hidden = true; } }, 'ត្រឡប់ទៅកែ'), save]));
    preview.hidden = false; preview.scrollIntoView?.({ behavior: 'smooth', block: 'start' });
  } }, 'មើលជាមុន និងរក្សាទុក');
  function updateTotal() {
    lessonTotals.replaceChildren(lessonSelectionSummary([...state.selected.values()]));
    totals.textContent = `ក្នុងតេស្ត ${test.questions.length} · ជ្រើសថ្មី ${state.selected.size} · ពិន្ទុសរុប ${score(totalScore())}`;
    const difference = Math.round((state.target - totalScore()) * 10000) / 10000;
    const validTarget = Number.isFinite(state.target) && state.target > 0;
    progress.max = validTarget ? state.target : 100; progress.value = totalScore();
    targetStatus.textContent = validTarget ? `${score(totalScore())} / ${score(state.target)} · ${difference === 0 ? 'គ្រប់ពិន្ទុគោលដៅ ✓' : difference > 0 ? 'ខ្វះ ' + score(difference) : 'លើស ' + score(-difference)}` : 'សូមកំណត់ពិន្ទុគោលដៅធំជាង ០';
    targetStatus.className = validTarget && difference === 0 ? 'tp-target-met' : 'tp-target-pending';
    review.disabled = busy || !state.selected.size;
    invalidate();
  }
  function drawBasket() {
    basket.replaceChildren(h('h3', {}, `សំណួរដែលបានជ្រើស (${state.selected.size})`), lessonTotals, h('p', { class: 'muted' }, 'កំណត់ពិន្ទុ និងរៀបលំដាប់សំណួរថ្មី។'));
    if (!state.selected.size) basket.append(h('p', { class: 'tp-empty' }, 'ជ្រើសសំណួរពីមេរៀនណាមួយ។ អ្នកអាចបន្តជ្រើសពីមេរៀនផ្សេងបាន។'));
    const ids = [...state.selected.keys()];
    for (const [id, q] of state.selected) {
      const points = h('input', { type: 'number', min: '0.01', step: 'any', value: Number.isFinite(q.points) ? q.points : '', 'aria-label': `ពិន្ទុសំណួរ ${id}`, oninput: () => { q.points = points.value === '' ? NaN : Number(points.value); points.setCustomValidity(Number.isFinite(q.points) && q.points > 0 ? '' : 'សូមបញ្ចូលពិន្ទុធំជាង ០'); updateTotal(); } });
      const move = (direction, label) => h('button', { class: 'secondary btn-sm', 'aria-label': `${label} #${id}`, disabled: (direction < 0 ? ids[0] === id : ids[ids.length - 1] === id) ? 'disabled' : null, onclick: () => { moveTestSelection(state.selected, id, direction); drawBasket(); } }, label);
      basket.append(h('div', { class: 'tp-picked' }, [h('small', {}, `${ids.indexOf(id) + 1}. ${q.grade || '—'} · ${q.lesson || 'មិនទាន់កំណត់មេរៀន'}`), mathEl('div', { class: 'tp-snippet' }, q.stem_text), h('div', { class: 'row' }, [h('label', {}, ['ពិន្ទុ ', points]), move(-1, '↑'), move(1, '↓'), h('button', { class: 'secondary btn-sm', 'aria-label': `ដកសំណួរ ${id}`, onclick: () => { state.selected.delete(id); draw(); } }, 'ដកចេញ')])]));
    }
    updateTotal();
  }
  const matchesFilters = q => (!kind.value || (q.kind === 'writing' ? 'writing' : 'mcq') === kind.value) && (!level.value || q.level === level.value);
  function drawLessons() {
    const qs = questions.filter(q => String(q.grade || '') === state.grade);
    const lessons = [...new Set([...(curr.lessons[state.grade] || []), ...qs.map(q => q.lesson || '')])];
    side.replaceChildren(h('h3', {}, '១. ជ្រើសមេរៀន'), h('p', { class: 'muted' }, 'កំណត់ចំនួន រួចជ្រើសដោយដៃ ឬបំពេញចៃដន្យតាមប្រភេទ និងកម្រិតខាងលើ។'));
    for (const lesson of [null, ...lessons]) {
      const pool = lesson === null ? qs : qs.filter(q => (q.lesson || '') === lesson);
      const picked = pool.filter(q => state.selected.has(q.id)).length;
      side.append(h('button', { class: `tp-lesson${state.lesson === lesson ? ' active' : ''}`, 'aria-pressed': String(state.lesson === lesson), onclick: () => { state.lesson = lesson; limit = 30; drawLessons(); drawBank(); bank.scrollTop = 0; persist(); } }, [h('span', {}, lesson === null ? 'មេរៀនទាំងអស់' : lesson || 'មិនទាន់កំណត់មេរៀន'), h('small', {}, `សរុប ${pool.length} · ជ្រើស ${picked}`)]));
      if (lesson === null) continue;
      const key = JSON.stringify([state.grade, lesson]);
      const quantity = h('input', { type: 'number', min: '1', max: '200', step: '1', value: state.quantities[key] || '', placeholder: 'ចំនួន', 'aria-label': `ចំនួនសំណួរ ${lesson || 'មិនទាន់កំណត់មេរៀន'}`, oninput: () => { state.quantities[key] = quantity.value; persist(); } });
      side.append(h('div', { class: 'tp-quantity' }, [quantity, h('button', { class: 'secondary btn-sm', onclick: () => {
        const wanted = Number(quantity.value);
        if (!Number.isInteger(wanted) || wanted < 1 || wanted > 200) return Exam.notify('សូមកំណត់ចំនួនពី ១ ដល់ ២០០។');
        const current = pool.filter(q => state.selected.has(q.id)).length;
        if (wanted <= current) return Exam.notify(`បានជ្រើស ${current} សំណួររួចហើយ។ អ្នកអាចដកសំណួរដោយដៃ។`);
        const candidates = pool.filter(q => !state.selected.has(q.id) && !existing.has(keyOf(q)) && matchesFilters(q));
        const need = wanted - current;
        if (candidates.length < need) return Exam.notify(`មានសំណួរត្រូវតាមតម្រងតែ ${candidates.length} សំណួរ។ ត្រូវការបន្ថែម ${need}។`);
        if (state.selected.size + need > 200) return Exam.notify('សូមជ្រើសយ៉ាងច្រើន ២០០ សំណួរក្នុងមួយលើក។');
        randomTestQuestions(candidates, need).forEach(q => state.selected.set(q.id, { ...q, points: Number(q.points) > 0 ? Number(q.points) : 1 }));
        draw();
      } }, 'ចៃដន្យ')]));
    }
  }
  function drawBank() {
    const term = search.value.trim().toLowerCase();
    const filtered = questions.filter(q => String(q.grade || '') === state.grade && (state.lesson === null || (q.lesson || '') === state.lesson) && matchesFilters(q) && (!term || `${q.stem_text} ${q.id} ${q.lesson || ''}`.toLowerCase().includes(term)));
    bank.replaceChildren(h('h3', {}, `២. ជ្រើសសំណួរ (${filtered.length})`));
    if (!filtered.length) bank.append(h('p', { class: 'tp-empty' }, 'រកមិនឃើញសំណួរ។ សូមជ្រើសមេរៀនផ្សេង ឬប្តូរការស្វែងរក។'));
    for (const q of filtered.slice(0, limit)) {
      const added = existing.has(keyOf(q)), selected = state.selected.has(q.id);
      const checkbox = h('input', { type: 'checkbox', checked: selected || added ? 'checked' : null, disabled: added ? 'disabled' : null, onchange: () => {
        if (checkbox.checked) state.selected.set(q.id, { ...q, points: Number(q.points) > 0 ? Number(q.points) : 1 }); else state.selected.delete(q.id);
        card.classList.toggle('is-selected', checkbox.checked); drawLessons(); drawBasket();
      } });
      const card = h('article', { class: `tp-question${selected || added ? ' is-selected' : ''}` }, [h('label', { class: 'tp-select' }, [checkbox, `#${q.id} · ${q.kind === 'writing' ? 'សរសេរ' : 'ពហុជ្រើសរើស'} · ${q.points} ពិន្ទុ`, added ? ' · ក្នុងតេស្តរួចហើយ' : '']), mathEl('div', {}, Exam.withSample(q).stem_text), q.image_key ? h('img', { src: `/api/images/${q.image_key}`, loading: 'lazy', alt: 'រូបភាពសំណួរ' }) : null, ...(Exam.withSample(q).options || []).map((opt, i) => mathEl('div', { class: 'tp-option' }, `${i + 1}. ${opt}`))]);
      bank.append(card);
    }
    if (filtered.length > limit) bank.append(h('button', { class: 'secondary', onclick: () => { const y = bank.scrollTop; limit += 30; drawBank(); bank.scrollTop = y; } }, `បង្ហាញបន្ថែម (${filtered.length - limit})`));
  }
  function draw() { drawLessons(); drawBank(); drawBasket(); }
  const reset = h('button', { class: 'secondary', onclick: async () => {
    if (!await Exam.confirm('ដកការជ្រើសសំណួរថ្មីទាំងអស់?')) return;
    state.selected.clear(); state.quantities = {}; draw();
  } }, 'ដកការជ្រើសទាំងអស់');
  controls.append(h('div', { class: 'tp-heading' }, [h('h2', {}, 'បង្កើតតេស្តតាមថ្នាក់'), isNew ? title : null, h('p', { class: 'muted' }, 'ជ្រើសថ្នាក់ → ជ្រើសសំណួរ → កំណត់ពិន្ទុ និងលំដាប់ → ពិនិត្យមុនរក្សាទុក'), draftStatus]), h('div', { class: 'tp-toolbar' }, [h('label', {}, ['ថ្នាក់ ', grade]), search, kind, level, h('label', {}, ['ពិន្ទុគោលដៅ ', target])]), h('div', { class: 'tp-layout' }, [side, bank, basket]), h('div', { class: 'tp-footer' }, [h('div', {}, [totals, progress, targetStatus]), h('div', { class: 'row' }, [reset, review])]), preview);
  root.replaceChildren(controls);
  draw();
  return root;
}
