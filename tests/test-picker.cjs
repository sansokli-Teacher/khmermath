const { test } = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const path = require('node:path');
const base = path.join(__dirname, '..');
class Element {
  constructor(tag, attrs = {}, children = []) {
    this.tag = tag; this.attrs = attrs; Object.assign(this, attrs);
    this.value = attrs.value ?? ''; this.children = []; this.scrollTop = 0;
    this.classList = { toggle() {} }; this.append(...[children].flat());
    if (tag === 'select') this.value = this.children.find(c => c.selected)?.value ?? this.children[0]?.value ?? '';
  }
  append(...items) { this.children.push(...items.filter(x => x != null)); }
  replaceChildren(...items) { this.children = []; this.append(...items); }
  setCustomValidity(v) { this.validityMessage = v; }
}
const walk = el => [el, ...(el.children || []).flatMap(c => typeof c === 'object' ? walk(c) : [])];
test('cross-lesson selection retains custom points and submits their total', async () => {
  const questions = [1, 2].map(id => ({ id, grade: '11', lesson: `Lesson ${id}`, stem_text: `Question ${id}`, points: 2, kind: 'mcq', options: ['A', 'B'] }));
  let payload;
  const ctx = vm.createContext({
    h: (t, a, c) => new Element(t, a, c), mathEl: (t, a, c) => new Element(t, a, c),
    api: async (url, opts) => { if (opts) { payload = opts.body; return { copied: 2, copied_ids: [1, 2] }; } return { questions }; },
    loadCurr: async () => ({ grades: ['11'], lessons: { 11: ['Lesson 1', 'Lesson 2'] } }),
    Exam: { withSample: q => q, notify: msg => { throw Error(msg); } }, renderTestBuilder: async () => {},
  });
  vm.runInContext(fs.readFileSync(path.join(base, 'public/js/test-picker.js'), 'utf8'), ctx);
  const root = await ctx.buildTestPicker({ id: 4, questions: [{ points: 3, stem_text: 'Existing', options: [] }] }, {});
  const find = fn => walk(root).find(fn);
  const selectLesson = name => find(e => e.tag === 'button' && e.children[0]?.children?.includes(name)).onclick();
  selectLesson('Lesson 1');
  let cb = find(e => e.type === 'checkbox'); cb.checked = true; cb.onchange();
  let points = find(e => e.attrs?.['aria-label'] === 'ពិន្ទុសំណួរ 1'); points.value = '4.5'; points.oninput();
  selectLesson('Lesson 2');
  cb = find(e => e.type === 'checkbox'); cb.checked = true; cb.onchange();
  assert.match(find(e => e.attrs?.class === 'tp-totals').textContent, /9.5/);
  selectLesson('Lesson 1');
  assert.equal(find(e => e.type === 'checkbox').checked, 'checked');
  assert.equal(find(e => e.attrs?.['aria-label'] === 'ពិន្ទុសំណួរ 1').value, 4.5);
  await find(e => e.tag === 'button' && e.children.includes('មើលជាមុន និងរក្សាទុក')).onclick();
  await find(e => e.tag === 'button' && e.children.includes('បន្ថែមទៅតេស្ត')).onclick();
  assert.deepEqual(JSON.parse(JSON.stringify(payload)), { question_ids: [1, 2], points_by_id: { 1: 4.5, 2: 2 } });
});
test('copy endpoint validates scores and capacity before writing; preserves source scores', async () => {
  const source = fs.readFileSync(path.join(base, 'src/api/tests.js'), 'utf8');
  const fn = source.slice(source.indexOf('export async function copyQuestions'), source.indexOf('// build a new draft')).replace('export ', '');
  let writes = [], room = 10;
  const original = { id: 1, points: 2 };
  const ctx = vm.createContext({ needTest: async () => ({ t: {} }), bankRows: async () => [original], questionRoom: async () => room,
    copyInto: async (_, id, q) => writes.push(q), json: x => x, err: (message, status) => ({ status }), limitResponse: () => ({ status: 403 }), TRIAL: { questions: 10 } });
  vm.runInContext(fn, ctx);
  const call = body => ctx.copyQuestions({ json: async () => body }, {}, { testId: 4 });
  assert.equal((await call({ question_ids: [1], points_by_id: { 1: -1 } })).status, 400);
  assert.equal(writes.length, 0);
  room = 0;
  assert.equal((await call({ question_ids: [1] })).status, 403);
  assert.equal(writes.length, 0);
  room = 10;
  assert.equal((await call({ question_ids: [1, 1], points_by_id: { 1: 4.5 } })).copied, 1);
  assert.equal(writes[0].points, 4.5);
  assert.equal(original.points, 2);
});
test('lesson totals group by class and lesson with decimal scores', () => {
  const ctx = vm.createContext({ h: (t, a, c) => new Element(t, a, c) });
  vm.runInContext(fs.readFileSync(path.join(base, 'public/js/test-picker.js'), 'utf8'), ctx);
  const summary = ctx.lessonSelectionSummary([
    { grade: '11', lesson: 'A', points: 2 }, { grade: '11', lesson: 'A', points: 2.5 },
    { grade: '11', lesson: 'B', points: 3 }, { grade: '10', lesson: 'A', points: 1 },
  ]);
  assert.equal(summary.children.length, 3);
  assert.equal(summary.children[0].children[1].children[0], '2 សំណួរ · 4.5 ពិន្ទុ');
});
function pickerHarness(questions, storage = new Map(), teacher = 9) {
  const calls = [], notifications = [];
  const ctx = vm.createContext({
    ME: { id: teacher },
    localStorage: { getItem: k => storage.get(k) || null, setItem: (k, v) => storage.set(k, v) },
    h: (t, a, c) => new Element(t, a, c), mathEl: (t, a, c) => new Element(t, a, c),
    api: async (url, opts) => {
      if (!opts) return { questions };
      calls.push({ url, body: opts.body });
      return url === '/api/tests' ? { id: 88 } : { copied: opts.body.question_ids?.length, copied_ids: opts.body.question_ids };
    },
    loadCurr: async () => ({ grades: ['11'], lessons: { 11: ['A', 'B'] } }),
    Exam: { withSample: q => q, notify: m => notifications.push(m), confirm: async () => true }, renderTestBuilder: async () => {},
  });
  vm.runInContext(fs.readFileSync(path.join(base, 'public/js/test-picker.js'), 'utf8'), ctx);
  return { ctx, calls, notifications, storage };
}
const fixture = [
  { id: 1, grade: '11', lesson: 'A', level: 'easy', stem_text: 'one', points: 2, options: ['a', 'b'], correct_index: 0 },
  { id: 2, grade: '11', lesson: 'A', level: 'hard', stem_text: 'two', points: 3, options: ['a', 'b'], correct_index: 1 },
  { id: 3, grade: '11', lesson: 'B', level: 'easy', stem_text: 'three', points: 4, kind: 'writing', solution_text: 'answer' },
];
const byLabel = (root, label) => walk(root).find(e => e.attrs?.['aria-label'] === label);
const byText = (root, label) => walk(root).find(e => e.tag === 'button' && e.children.includes(label));
function check(root, index) { const cb = walk(root).filter(e => e.type === 'checkbox')[index]; cb.checked = true; cb.onchange(); }
test('draft restores scores, target, title and order after refresh, scoped to teacher', async () => {
  const first = pickerHarness(fixture);
  let root = await first.ctx.buildTestPicker({ questions: [] }, {});
  const title = byLabel(root, 'ចំណងជើងតេស្ត'); title.value = 'October'; title.oninput();
  check(root, 0); check(root, 1);
  const points = byLabel(root, 'ពិន្ទុសំណួរ 1'); points.value = '7.5'; points.oninput();
  byLabel(root, '↑ #2').onclick();
  const target = byLabel(root, 'ពិន្ទុគោលដៅ'); target.value = '50'; target.oninput();
  const second = pickerHarness(fixture, first.storage);
  root = await second.ctx.buildTestPicker({ questions: [] }, {});
  assert.equal(byLabel(root, 'ពិន្ទុសំណួរ 1').value, 7.5);
  assert.equal(byLabel(root, 'ពិន្ទុគោលដៅ').value, 50);
  assert.equal(byLabel(root, 'ចំណងជើងតេស្ត').value, 'October');
  assert.deepEqual(walk(root).filter(e => e.attrs?.['aria-label']?.startsWith('ពិន្ទុសំណួរ ')).map(e => e.attrs['aria-label']), ['ពិន្ទុសំណួរ 2', 'ពិន្ទុសំណួរ 1']);
  const other = pickerHarness(fixture, first.storage, 10);
  const otherRoot = await other.ctx.buildTestPicker({ questions: [] }, {});
  assert.equal(byLabel(otherRoot, 'ពិន្ទុសំណួរ 1'), undefined);
  assert.equal(byLabel(otherRoot, 'ចំណងជើងតេស្ត').value, '');
});
test('random lesson fill respects difficulty, avoids duplicates, and reports shortages', async () => {
  const { ctx, notifications } = pickerHarness(fixture);
  const root = await ctx.buildTestPicker({ questions: [] }, {});
  const level = byLabel(root, 'កម្រិតសំណួរ'); level.value = 'easy'; level.onchange();
  let quantity = byLabel(root, 'ចំនួនសំណួរ A'); quantity.value = '2'; quantity.oninput();
  byText(root, 'ចៃដន្យ').onclick();
  assert.equal(notifications.length, 1);
  assert.equal(byLabel(root, 'ពិន្ទុសំណួរ 1'), undefined);
  quantity.value = '1'; quantity.oninput(); byText(root, 'ចៃដន្យ').onclick();
  assert.ok(byLabel(root, 'ពិន្ទុសំណួរ 1'));
  assert.equal(byLabel(root, 'ពិន្ទុសំណួរ 2'), undefined);
  byText(root, 'ចៃដន្យ').onclick();
  assert.equal(walk(root).filter(e => e.attrs?.['aria-label'] === 'ពិន្ទុសំណួរ 1').length, 1);
});
test('review includes answer key and creation sends reordered scores then clears draft', async () => {
  const { ctx, calls } = pickerHarness(fixture);
  let created;
  const root = await ctx.buildTestPicker({ questions: [] }, {}, { onCreated: id => { created = id; } });
  const title = byLabel(root, 'ចំណងជើងតេស្ត'); title.value = 'My test'; title.oninput();
  check(root, 0); check(root, 1); byLabel(root, '↑ #2').onclick();
  byText(root, 'មើលជាមុន និងរក្សាទុក').onclick();
  assert.equal(byLabel(root, 'មើលតេស្តជាមុន').hidden, false);
  assert.ok(walk(byLabel(root, 'មើលតេស្តជាមុន')).some(e => e.tag === 'summary' && e.children.includes('ចម្លើយ / អត្រាកំណែ')));
  await byText(root, 'បង្កើតតេស្ត').onclick();
  assert.equal(created, 88);
  assert.deepEqual(JSON.parse(JSON.stringify(calls[1].body)), { question_ids: [2, 1], points_by_id: { 1: 2, 2: 3 } });
  assert.deepEqual(JSON.parse(JSON.stringify(ctx.readTestDraft('new'))), {});
});
test('restoration drops inaccessible questions and retains invalid points for correction', () => {
  const { ctx } = pickerHarness(fixture);
  const restored = ctx.restoreTestSelection([[1, null], [999, 3], [2, 5]], fixture);
  assert.deepEqual([...restored.keys()], [1, 2]);
  assert.ok(Number.isNaN(restored.get(1).points));
  assert.equal(restored.get(2).points, 5);
});
test('storage failure leaves selection and score editing usable', async () => {
  const { ctx } = pickerHarness(fixture);
  ctx.localStorage.setItem = () => { throw Error('quota'); };
  const root = await ctx.buildTestPicker({ id: 4, questions: [] }, {});
  check(root, 0);
  assert.ok(byLabel(root, 'ពិន្ទុសំណួរ 1'));
  assert.ok(walk(root).some(e => e.textContent?.includes('មិនអាចរក្សាសម្រាងបាន')));
});
test('saved test filters match class and lesson on the same question grouping', () => {
  const source = fs.readFileSync(path.join(base, 'public/js/teacher.js'), 'utf8');
  const fn = source.slice(source.indexOf('function matchesTestCurriculum('), source.indexOf('render.tests = async function'));
  const ctx = vm.createContext({}); vm.runInContext(fn, ctx);
  const mixed = { curriculum: [{ grade: '11', lesson: 'A' }, { grade: '10', lesson: 'B' }, { grade: '11', lesson: 'C' }] };
  assert.equal(ctx.matchesTestCurriculum(mixed, '11', 'A'), true);
  assert.equal(ctx.matchesTestCurriculum(mixed, '11', 'B'), false);
  assert.equal(ctx.matchesTestCurriculum(mixed, '', 'B'), true);
  assert.equal(ctx.matchesTestCurriculum(mixed, '11', 'C'), true);
  assert.equal(ctx.matchesTestCurriculum({ curriculum: [] }, '-', '-'), true);
  assert.equal(ctx.matchesTestCurriculum({ curriculum: [{ grade: 11, lesson: null }] }, '11', '-'), true);
  assert.equal(ctx.matchesTestCurriculum({ curriculum: [] }, '11', ''), false);
});
