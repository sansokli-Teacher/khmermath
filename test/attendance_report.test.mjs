import test from 'node:test';
import assert from 'node:assert/strict';
import { attendanceReport } from '../teach-app/src/report.js';

test('the report follows the teacher\'s format', () => {
  const r = attendanceReport({ day: '2026-10-23', className: '7NGS-B', subject: 'គណិតវិទ្យា', period: 3, absent: ['សុខ ចាន់', 'ដារា ឡុង'], teacher: 'សាន សុខលី' });
  assert.equal(r, [
    'ថ្ងៃសុក្រ ទី ២៣ ខែ តុលា ឆ្នាំ២០២៦',
    '- ថ្នាក់ 7NGS-B',
    '-មុខវិជ្ជា៖ គណិតវិទ្យា',
    '-ម៉ោងទី៖ ៣',
    '-សិស្សអវត្តមាន :  ២ នាក់',
    'ឈ្មោះ៖',
    '១. សុខ ចាន់',
    '២. ដារា ឡុង',
    'បង្រៀនដោយ៖ សាន សុខលី',
  ].join('\n'));
});

test('the planned lesson is a line of its own, and nobody absent says so', () => {
  const r = attendanceReport({ day: '2026-10-19', className: '9NGS-X', subject: 'គណិតវិទ្យា', period: 1, absent: [], teacher: 'T', topic: ' ចំនួនគត់ ' });
  assert.match(r, /^ថ្ងៃច័ន្ទ ទី ១៩ ខែ តុលា/);
  assert.match(r, /\n-មេរៀន៖ ចំនួនគត់\n/);
  assert.match(r, /-សិស្សអវត្តមាន :  ០ នាក់\nឈ្មោះ៖\nគ្មាន\n/);
  assert.doesNotMatch(attendanceReport({ day: '2026-10-19', period: 1, topic: 'x', withTopic: false }), /មេរៀន៖/);
});
