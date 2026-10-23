// The attendance message a teacher copies to the class group / office after each period.
const KH_DIGITS = '០១២៣៤៥៦៧៨៩';
const khn = (n) => String(n ?? '').replace(/\d/g, (d) => KH_DIGITS[d]);
const DAYS = ['អាទិត្យ', 'ច័ន្ទ', 'អង្គារ', 'ពុធ', 'ព្រហស្បតិ៍', 'សុក្រ', 'សៅរ៍'];
const MONTHS = ['មករា', 'កុម្ភៈ', 'មីនា', 'មេសា', 'ឧសភា', 'មិថុនា', 'កក្កដា', 'សីហា', 'កញ្ញា', 'តុលា', 'វិច្ឆិកា', 'ធ្នូ'];

/** day = 'YYYY-MM-DD'; absent = the names of the absent students, in roll order */
export function attendanceReport({ day, className, subject, period, absent = [], teacher = '', topic = '', withTopic = true }) {
  const [y, m, d] = String(day).split('-').map(Number);
  const date = new Date(y, m - 1, d);
  const head = `ថ្ងៃ${DAYS[date.getDay()]} ទី ${khn(d)} ខែ ${MONTHS[m - 1]} ឆ្នាំ${khn(y)}`;
  const lines = [
    head,
    `- ថ្នាក់ ${className || ''}`.trimEnd(),
    `-មុខវិជ្ជា៖ ${subject || ''}`.trimEnd(),
    ...(withTopic && topic && topic.trim() ? [`-មេរៀន៖ ${topic.trim()}`] : []),
    `-ម៉ោងទី៖ ${khn(period)}`,
    `-សិស្សអវត្តមាន :  ${khn(absent.length)} នាក់`,
    'ឈ្មោះ៖',
    ...(absent.length ? absent.map((n, i) => `${khn(i + 1)}. ${n}`) : ['គ្មាន']),
    `បង្រៀនដោយ៖ ${teacher || ''}`.trimEnd(),
  ];
  return lines.join('\n');
}
