// WCAG contrast gate. Reads tools/contrast_pairs.json and exits 1 if any pair is under its min ratio.
import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const file = join(dirname(fileURLToPath(import.meta.url)), 'contrast_pairs.json');
const pairs = JSON.parse(readFileSync(file, 'utf8'));

function channel(c) {
  const v = c / 255;
  return v <= 0.04045 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4;
}
function lum(hex) {
  const h = hex.replace('#', '');
  const n = h.length === 3 ? h.split('').map((c) => c + c).join('') : h;
  const r = parseInt(n.slice(0, 2), 16);
  const g = parseInt(n.slice(2, 4), 16);
  const b = parseInt(n.slice(4, 6), 16);
  return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b);
}
function ratio(fg, bg) {
  const a = lum(fg);
  const b = lum(bg);
  const hi = Math.max(a, b);
  const lo = Math.min(a, b);
  return (hi + 0.05) / (lo + 0.05);
}

let failed = 0;
for (const pair of pairs) {
  const got = ratio(pair.fg, pair.bg);
  const ok = got + 1e-9 >= pair.min;
  const line = `${ok ? 'ok  ' : 'FAIL'} ${pair.name}: ${got.toFixed(2)} (need ${pair.min})`;
  if (ok) console.log(line);
  else { console.error(line); failed += 1; }
}
if (failed) {
  console.error(`${failed} pair${failed === 1 ? '' : 's'} below target`);
  process.exit(1);
}
console.log(`${pairs.length} pairs pass`);
