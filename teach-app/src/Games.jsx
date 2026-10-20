import { api, gradeOf, fullName } from './api.js';

export const GAMES = [
  { k: 'cards', ic: '🃏', t: 'កាតបើក', d: 'ហ្គេមសំណួរជាក្រុម', style: 'cards' },
  { k: 'qwheel', ic: '🎲', t: 'កង់វិលសំណួរ', d: 'បង្វិលកង់ជ្រើសសំណួរ', style: 'wheel' },
  { k: 'boat', ic: '🚣', t: 'ប្រណាំងទូកង', d: 'ឆ្លើយត្រូវ ទូកទៅមុខ', style: 'boat' },
  { k: 'live', ic: '📱', t: 'សំណួរផ្ទាល់', d: 'សិស្សឆ្លើយលើទូរស័ព្ទ', href: (c) => `/teacher?classic=1&tool=live&class=${c.id}` },
  { k: 'bingo', ic: '🎯', t: 'ប៊ីងហ្គោ', d: 'បោះពុម្ពកាតចម្លើយ', href: () => '/bingo.html' },
];

// Team games use the team-game page; the roster is split into shuffled teams (as in the classic dashboard).
export async function launchGame(game, cls) {
  if (game.href) { location.href = game.href(cls); return; }
  const { students } = await api(`/api/classes/${cls.id}/students`);
  const names = students.map(fullName).filter(Boolean);
  if (!names.length) throw new Error('ថ្នាក់នេះមិនទាន់មានសិស្សទេ។');
  const n = Math.min(4, Math.max(2, names.length));
  const teams = Array.from({ length: n }, () => []);
  const sh = names.slice();
  for (let i = sh.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [sh[i], sh[j]] = [sh[j], sh[i]]; }
  sh.forEach((nm, i) => teams[i % n].push(nm));
  try { localStorage.setItem('km_wheel_last_groups', JSON.stringify({ cls: cls.name, groups: teams })); } catch { /* storage blocked */ }
  location.href = `/teamgame.html?import=1&style=${game.style}&grade=${parseInt(gradeOf(cls), 10) || 7}`;
}
