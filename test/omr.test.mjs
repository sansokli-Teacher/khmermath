import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';

const ctx = { window: {}, document: {} };
vm.createContext(ctx);
vm.runInContext(fs.readFileSync(new URL('../public/js/omr.js', import.meta.url), 'utf8'), ctx);
const OMR = ctx.window.OMR;

test('sheet code round-trips test id, grouping and id length, and rejects a flipped bit', () => {
  for (const [id, grouped, d] of [[3, false, 7], [6, true, 7], [16383, true, 12], [0, false, 1]]) {
    const bits = OMR.codeBits(id, grouped, d);
    assert.equal(bits.length, 20);
    assert.deepEqual({ ...OMR.parseBits(bits) }, { testId: id, grouped, idDigits: d });
    const bad = bits.slice(); bad[5] ^= 1;
    assert.equal(OMR.parseBits(bad), null);
  }
});

test('printed question order: grouped by level when tagged, original order otherwise', () => {
  const qs = [{ id: 1, level: 'hard' }, { id: 2, level: 'easy' }, { id: 3 }, { id: 4, level: 'easy' }, { id: 5, level: 'pisa' }];
  assert.deepEqual([...OMR.mcqOrder(qs, true).map((q) => q.id)], [2, 4, 1, 5, 3]);
  assert.deepEqual([...OMR.mcqOrder(qs, false).map((q) => q.id)], [1, 2, 3, 4, 5]);
  assert.deepEqual([...OMR.mcqOrder([{ id: 1 }, { id: 2 }], true).map((q) => q.id)], [1, 2]);   // nothing tagged -> unchanged
});

test('layout fits the sheet: 100 questions in 5 columns, every bubble inside 180 x 236 mm', () => {
  const L = OMR.layout(100, 5, 12);
  assert.equal(L.q.length, 100);
  for (const r of L.q) for (const [x, y] of r.bubbles) { assert.ok(x > 10 && x < 178 && y > 100 && y < 226, `${x},${y}`); }
  for (const col of L.id) for (const [x, y] of col) assert.ok(x < 100 && y < 95);
});
