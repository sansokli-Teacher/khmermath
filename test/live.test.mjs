import test from 'node:test';
import assert from 'node:assert/strict';
import { numericAnswer, numericOptions, parseStudentNumber, classify, isCorrect, points } from '../src/lib/livequiz.js';

test('only answers that are one plain number are graded as numbers', () => {
  assert.equal(numericAnswer('\\(4\\,200\\) ក្បាល'), 4200);
  assert.equal(numericAnswer('\\(63^{\\circ}\\)'), 63);
  assert.equal(numericAnswer('\\(25\\%\\)'), 25);
  assert.equal(numericAnswer('\\(-7\\)'), -7);
  assert.equal(numericAnswer('\\(2.54\\)'), 2.54);
  assert.equal(numericAnswer('12 នាក់'), 12);
  assert.equal(numericAnswer('\\(\\frac{3}{4}\\)'), null);
  assert.equal(numericAnswer('\\(x=5\\)'), null);
  assert.equal(numericAnswer('\\(3+4\\)'), null);
  assert.equal(numericAnswer('ត្រីកោណ'), null);
});

test('student numbers: Khmer digits, comma decimals, spaces', () => {
  assert.equal(parseStudentNumber('១២៥'), 125);
  assert.equal(parseStudentNumber(' 2,54 '), 2.54);
  assert.equal(parseStudentNumber('1 200'), 1200);
  assert.equal(parseStudentNumber('abc'), null);
});

test('questions are classified for automatic grading and answers compared', () => {
  const mcq = classify({ q: 'q', o: ['a', 'b', 'c', 'd'], k: 2, a: 'c' });
  assert.equal(mcq.pub.k, 'mcq'); assert.equal(mcq.pub.o.length, 4); assert.equal('correct' in mcq.pub, false);
  assert.ok(isCorrect(mcq.key, 2)); assert.ok(!isCorrect(mcq.key, 1));
  const tf = classify({ q: 'x ពិត ឬ មិនពិត?', a: 'មិនពិត' });
  assert.equal(tf.pub.k, 'tf'); assert.equal(tf.pub.q, 'x'); assert.ok(isCorrect(tf.key, 'F')); assert.ok(!isCorrect(tf.key, 'T'));
  const num = classify({ q: 'q', a: '\\(1\\,500\\) ដើម' });
  assert.equal(num.pub.k, 'mcq'); assert.equal(num.pub.o.length, 4); assert.equal(num.pub.o[num.key.correct], '\\(1\\,500\\) ដើម');
  assert.equal(new Set(num.pub.o).size, 4); assert.ok(isCorrect(num.key, num.key.correct)); assert.ok(!isCorrect(num.key, (num.key.correct + 1) % 4));
  assert.equal(classify({ q: 'q', a: '\\(\\frac{1}{2}\\)' }), null);
});

test('speed earns more points but a correct answer is always worth at least half', () => {
  assert.equal(points(true, 0, 30), 1000);
  assert.equal(points(true, 30000, 30), 500);
  assert.equal(points(true, 99999, 30), 500);
  assert.equal(points(false, 100, 30), 0);
  assert.ok(points(true, 5000, 30) > points(true, 20000, 30));
});

test('numeric answers get four different believable options that keep the unit and style', () => {
  for (const a of ['\\(25\\%\\)', '\\(63^{\\circ}\\)', '\\(2.54\\)', '12 នាក់', '\\(-7\\)', '\\(0\\)', '\\(1\\)', '\\(125\\,000\\) រៀល']) {
    for (let i = 0; i < 40; i++) {
      const r = numericOptions(a);
      assert.equal(r.o.length, 4, a); assert.equal(new Set(r.o).size, 4, a); assert.equal(r.o[r.k], a);
      for (const x of r.o) assert.equal(numericAnswer(x) !== null, true, x);
    }
  }
  assert.ok(numericOptions('\\(5\\)').o.every((x) => !/-/.test(x)));
  assert.ok(numericOptions('\\(2.54\\)').o.every((x) => /\.\d\d/.test(x)));
});
