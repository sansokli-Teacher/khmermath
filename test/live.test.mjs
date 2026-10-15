import test from 'node:test';
import assert from 'node:assert/strict';
import { numericAnswer, parseStudentNumber, classify, isCorrect, points } from '../src/lib/livequiz.js';

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
  assert.equal(num.pub.k, 'num'); assert.ok(isCorrect(num.key, '1500')); assert.ok(isCorrect(num.key, '១៥០០')); assert.ok(!isCorrect(num.key, '1501'));
  assert.equal(classify({ q: 'q', a: '\\(\\frac{1}{2}\\)' }), null);
});

test('speed earns more points but a correct answer is always worth at least half', () => {
  assert.equal(points(true, 0, 30), 1000);
  assert.equal(points(true, 30000, 30), 500);
  assert.equal(points(true, 99999, 30), 500);
  assert.equal(points(false, 100, 30), 0);
  assert.ok(points(true, 5000, 30) > points(true, 20000, 30));
});
