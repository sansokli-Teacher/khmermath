// Adds the suggested answer time `tm` to every question of the static bank (public/data/teamgame_g7.json), so the game still has
// per-question times when it plays the built-in copy (offline / exam-day lock). The live bank recomputes them on the server.
import fs from 'node:fs';
import { suggestTime } from '../src/lib/gamebank.js';
const p = new URL('../public/data/teamgame_g7.json', import.meta.url);
const d = JSON.parse(fs.readFileSync(p, 'utf8'));
let n = 0;
for (const L of d.lessons) for (const q of L.qs) { q.tm = suggestTime(q); n++; }
fs.writeFileSync(p, JSON.stringify(d));
console.log(n, 'questions now carry tm');
