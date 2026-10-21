import test from 'node:test';
import assert from 'node:assert/strict';
import { mergeBank, cleanEdit, baseKey, overlayEdits, suggestTime } from '../src/lib/gamebank.js';

const base = { class: 'g7', lessons: [
  { n: 1, title: 'A', qs: [{ t: 'x', q: 'one \\(1\\)', lv: 'easy', h: '', s: 's', a: '\\(2\\)', o: ['\\(1\\)', '\\(2\\)', '\\(3\\)', '\\(4\\)'], k: 1 }, { t: 'x', q: 'two', lv: 'easy', h: '', s: '', a: '5' }] },
  { n: 2, title: 'B', qs: [{ t: 'y', q: 'three', lv: 'hard', h: '', s: '', a: '7' }] },
] };

test('a fix is applied to both games, a hidden question is dropped, a disabled lesson is not offered', () => {
  const edits = new Map([
    ['1:1', { bq: baseKey(base.lessons[0].qs[1]), data: { q: 'two fixed', a: '6', t: 'x', lv: 'easy', h: '', s: '' }, off: false }],
    ['1:0', { bq: baseKey(base.lessons[0].qs[0]), data: {}, off: true }],
  ]);
  const pub = mergeBank(base, edits, { enabled: true, lessons: [1] });
  assert.equal(pub.lessons.length, 1);
  assert.equal(pub.lessons[0].qs.length, 1);
  assert.equal(pub.lessons[0].qs[0].q, 'two fixed');
  assert.equal(pub.lessons[0].qs[0].a, '6');
  const adm = mergeBank(base, edits, { enabled: true, lessons: [1] }, { admin: true });
  assert.equal(adm.lessons.length, 2);
  assert.equal(adm.lessons[1].enabled, false);
  assert.equal(adm.lessons[0].qs[0].off, true);
  assert.equal(adm.lessons[0].qs[1].edited, true);
  assert.equal(adm.lessons[0].qs[1].orig.q, 'two');
});

test('an edit made on a different base question is stale and ignored', () => {
  const edits = new Map([['2:0', { bq: 'something-else', data: { q: 'zzz', a: '1', t: 'y', lv: 'hard', h: '', s: '' }, off: false }]]);
  const pub = mergeBank(base, edits, { enabled: true, lessons: null });
  assert.equal(pub.lessons[1].qs[0].q, 'three');
  const adm = mergeBank(base, edits, { enabled: true, lessons: null }, { admin: true });
  assert.equal(adm.lessons[1].qs[0].stale, true);
});

test('the master switch closes the game for everyone', () => {
  assert.equal(mergeBank(base, new Map(), { enabled: false, lessons: null }).lessons.length, 0);
});

test('cleanEdit keeps the answer in step with the chosen option and rejects bad input', () => {
  const b = base.lessons[0].qs[0];
  const ok = cleanEdit({ q: 'q', o: ['a', 'b', 'c', 'd'], k: 2, lv: 'hard' }, b);
  assert.equal(ok.data.a, 'c'); assert.equal(ok.data.k, 2); assert.equal(ok.data.lv, 'hard');
  assert.ok(cleanEdit({ q: '', o: ['a', 'b', 'c', 'd'], k: 0 }, b).error);
  assert.ok(cleanEdit({ q: 'q', o: ['a', 'a', 'c', 'd'], k: 0 }, b).error);
  assert.ok(cleanEdit({ q: 'q', o: ['a', 'b', 'c'], k: 0 }, b).error);
  assert.ok(cleanEdit({ q: 'q', o: ['a', 'b', 'c', 'd'], k: 9 }, b).error);
  assert.ok(cleanEdit({ q: 'q', a: '' }, base.lessons[0].qs[1]).error);
  assert.equal(cleanEdit({ q: 'q', a: ' 9 ' }, base.lessons[0].qs[1]).data.a, '9');
});

test("a teacher's own fix and delete sit on top of the shared bank and are flagged mine", () => {
  const shared = new Map([['1:1', { bq: baseKey(base.lessons[0].qs[1]), data: { q: 'shared fix', a: '6', t: 'x', lv: 'easy', h: '', s: '' }, off: false }]]);
  const mine = new Map([
    ['1:1', { bq: baseKey(base.lessons[0].qs[1]), data: { q: 'my fix', a: '6', t: 'x', lv: 'easy', h: '', s: '' }, off: false }],
    ['1:0', { bq: baseKey(base.lessons[0].qs[0]), data: {}, off: true }],
  ]);
  const edits = overlayEdits(shared, mine);
  const pub = mergeBank(base, edits, { enabled: true, lessons: null });
  assert.equal(pub.lessons[0].qs.length, 1);          // the question I deleted is gone from my games
  assert.equal(pub.lessons[0].qs[0].q, 'my fix');     // my fix wins over the shared one
  const adm = mergeBank(base, edits, { enabled: true, lessons: null }, { admin: true });
  assert.equal(adm.lessons[0].qs[0].mine, true);
  assert.equal(adm.lessons[0].qs[1].mine, true);
  // other teachers still see the shared bank
  assert.equal(mergeBank(base, shared, { enabled: true, lessons: null }).lessons[0].qs[1].q, 'shared fix');
  assert.equal(mergeBank(base, shared, { enabled: true, lessons: null }).lessons[0].qs.length, 2);
});

test('every question gets an answer time: suggested from the question, or the teacher\'s own', () => {
  const short = { q: 'recall', lv: 'easy', s: 'x', o: ['a', 'b', 'c', 'd'] };
  const long = { q: 'long \\(1\\times 2 = 2\\) '.repeat(8), lv: 'hard', s: 'a = b = c = d = e', a: '1' };
  assert.equal(suggestTime(short), 15);
  assert.ok(suggestTime(long) > suggestTime(short));
  const pub = mergeBank(base, new Map(), { enabled: true, lessons: null });
  assert.ok(pub.lessons[0].qs.every((q) => q.tm >= 15 && q.tm <= 180));
  const own = new Map([['1:1', { bq: baseKey(base.lessons[0].qs[1]), data: { q: 'two', a: '6', t: 'x', lv: 'easy', h: '', s: '', tm: 75 }, off: false }]]);
  const adm = mergeBank(base, own, { enabled: true, lessons: null }, { admin: true });
  assert.equal(adm.lessons[0].qs[1].tm, 75);
  assert.equal(adm.lessons[0].qs[1].tmSet, true);
  assert.equal(adm.lessons[0].qs[0].tmSet, false);
  assert.equal(cleanEdit({ q: 'x', a: '1', t: 'y', tm: '' }, { t: 'y', lv: 'easy' }).data.tm, 0);
  assert.ok(cleanEdit({ q: 'x', a: '1', t: 'y', tm: 2 }, { t: 'y', lv: 'easy' }).error);
});
