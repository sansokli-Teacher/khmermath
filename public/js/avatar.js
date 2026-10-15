// Khmer-style cartoon avatars for the live quiz. An avatar is a code "bg-skin-head-outfit-extra", e.g. "2-1-3-0-1".
// KmAvatar.svg(code, px) → <svg> string. Same file is used on exam.khmermath.org and khmermath.org.
(function (g) {
  'use strict';
  var BG = ['#4dabf7', '#51cf66', '#9775fa', '#ffa94d', '#ff6b6b', '#3bc9db'];
  var SKIN = ['#fbd5b0', '#f2bf8f', '#d99a68', '#b9784a', '#8d5a36'];
  var OUT = [null, ['#b3262d', '#f2b632'], ['#5b2a86', '#f2b632'], ['#1f7a4d', '#f2b632']];
  var HAIR = '#1b1b1b', GOLD = '#f2b632', GOLDD = '#b8860b';
  var N = { bg: ['ពណ៌ ១', 'ពណ៌ ២', 'ពណ៌ ៣', 'ពណ៌ ៤', 'ពណ៌ ៥', 'ពណ៌ ៦'], skin: ['សម្បុរ ១', 'សម្បុរ ២', 'សម្បុរ ៣', 'សម្បុរ ៤', 'សម្បុរ ៥'],
    head: ['សក់ខ្លី', 'សក់ក្រង់ និងផ្កាចំប៉ី', 'មកុដ', 'ក្រមាក្បាល', 'មួកចំការ', 'ក្បាលអប្សរា'], outfit: ['ឯកសណ្ឋានសិស្ស', 'អាវក្រហមមាស', 'អាវស្វាយមាស', 'អាវបៃតងមាស'], acc: ['គ្មាន', 'ក្រមា', 'វ៉ែនតា', 'ខ្សែក'] };
  var SIZES = [6, 5, 6, 4, 4];

  function parse(code) { var t = String(code || '').split('-').map(Number); if (t.length !== 5 || t.some(function (n, i) { return !(n >= 0 && n < SIZES[i]); })) return null; return t; }
  function random() { return SIZES.map(function (n) { return Math.floor(Math.random() * n); }).join('-'); }
  function fromName(name) { var h = 0; for (var i = 0; i < name.length; i++) h = (h * 31 + name.charCodeAt(i)) >>> 0; return SIZES.map(function (n) { var v = h % n; h = Math.floor(h / n) + 7; return v; }).join('-'); }

  function svg(code, px) {
    var a = parse(code) || parse(fromName(String(code || 'x')) ); if (!a) a = [0, 0, 0, 0, 0];
    var bg = BG[a[0]], skin = SKIN[a[1]], head = a[2], outfit = a[3], acc = a[4], o = OUT[outfit];
    var s = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="' + px + '" height="' + px + '" role="img" aria-hidden="true">';
    s += '<defs><clipPath id="kmc"><circle cx="50" cy="50" r="50"/></clipPath><pattern id="kmk" width="6" height="6" patternUnits="userSpaceOnUse"><rect width="6" height="6" fill="#c8202e"/><path d="M0 3H6M3 0V6" stroke="#fff" stroke-width="1.1"/></pattern></defs>';
    s += '<g clip-path="url(#kmc)"><rect width="100" height="100" fill="' + bg + '"/>';
    // long hair behind the shoulders (girls' styles)
    if (head === 1 || head === 5) s += '<path d="M30 44 Q22 72 32 86 L42 70 L40 46 Z M70 44 Q78 72 68 86 L58 70 L60 46 Z" fill="' + HAIR + '"/>';
    // body
    if (outfit === 0) s += '<path d="M10 100 Q12 71 50 69 Q88 71 90 100 Z" fill="#fafafa" stroke="#cfd6df" stroke-width="1"/><path d="M41 70 L50 81 L59 70" fill="none" stroke="#cfd6df" stroke-width="1.5"/><path d="M47.5 79 L52.5 79 L54 93 L50 97 L46 93 Z" fill="#1c4fa8"/>';
    else s += '<path d="M10 100 Q12 71 50 69 Q88 71 90 100 Z" fill="' + o[0] + '"/><path d="M38 70 Q50 86 62 70" fill="none" stroke="' + o[1] + '" stroke-width="3.2"/><circle cx="50" cy="90" r="2.4" fill="' + o[1] + '"/><circle cx="38" cy="94" r="2" fill="' + o[1] + '"/><circle cx="62" cy="94" r="2" fill="' + o[1] + '"/>';
    // neck, ears, head
    s += '<rect x="43" y="58" width="14" height="16" rx="4" fill="' + skin + '"/><path d="M43 66 Q50 72 57 66 L57 70 L43 70 Z" fill="#000" opacity=".08"/>';
    s += '<circle cx="31" cy="48" r="4.2" fill="' + skin + '"/><circle cx="69" cy="48" r="4.2" fill="' + skin + '"/><ellipse cx="50" cy="46" rx="19" ry="21" fill="' + skin + '"/>';
    // face
    s += '<circle cx="43" cy="47" r="2.1" fill="#222"/><circle cx="57" cy="47" r="2.1" fill="#222"/><circle cx="43.7" cy="46.3" r=".7" fill="#fff"/><circle cx="57.7" cy="46.3" r=".7" fill="#fff"/>';
    s += '<path d="M39 42 Q43 40 47 42 M53 42 Q57 40 61 42" stroke="#3a2a20" stroke-width="1.3" fill="none" stroke-linecap="round"/>';
    s += '<path d="M44 55.5 Q50 61 56 55.5" stroke="#8a3030" stroke-width="1.8" fill="none" stroke-linecap="round"/><circle cx="37.5" cy="53" r="3.2" fill="#ff7a7a" opacity=".3"/><circle cx="62.5" cy="53" r="3.2" fill="#ff7a7a" opacity=".3"/>';
    // extras that sit on the body / face
    if (acc === 1) s += '<path d="M32 70 Q50 84 68 70 L66 79 Q50 92 34 79 Z" fill="url(#kmk)" stroke="#8f1620" stroke-width=".6"/><path d="M60 80 L71 84 L67 99 L58 92 Z" fill="url(#kmk)" stroke="#8f1620" stroke-width=".6"/>';
    if (acc === 3) s += '<path d="M37 71 Q50 90 63 71" fill="none" stroke="' + GOLD + '" stroke-width="2"/><circle cx="50" cy="85" r="3" fill="' + GOLD + '" stroke="' + GOLDD + '" stroke-width=".8"/>';
    // hair cap (all styles but the hat and crown-over-hair use it)
    var cap = '<path d="M29.5 46 Q27 20 50 20 Q73 20 70.5 46 Q66 33 50 32 Q34 33 29.5 46 Z" fill="' + HAIR + '"/>';
    if (head === 0) s += cap;
    if (head === 1) {
      s += cap + '<circle cx="50" cy="16" r="8" fill="' + HAIR + '"/>';
      for (var k = 0; k < 5; k++) s += '<ellipse cx="66" cy="22" rx="3" ry="5.4" fill="#fffdf5" stroke="#e6d9a8" stroke-width=".5" transform="rotate(' + (k * 72) + ' 66 27)"/>';
      s += '<circle cx="66" cy="27" r="2.3" fill="' + GOLD + '"/>';
    }
    if (head === 2) {
      s += cap + '<path d="M32 33 L34 22 L40 29 L44 14 L47 21 L50 3 L53 21 L56 14 L60 29 L66 22 L68 33 Q50 28 32 33 Z" fill="' + GOLD + '" stroke="' + GOLDD + '" stroke-width="1"/><rect x="31.5" y="31" width="37" height="5.5" rx="2" fill="' + GOLD + '" stroke="' + GOLDD + '" stroke-width="1"/><circle cx="50" cy="33.8" r="2.3" fill="#d6336c"/><circle cx="40" cy="33.8" r="1.5" fill="#1c7ed6"/><circle cx="60" cy="33.8" r="1.5" fill="#1c7ed6"/>';
    }
    if (head === 3) s += cap + '<path d="M29.5 37 Q50 27 70.5 37 L70.5 43 Q50 33 29.5 43 Z" fill="url(#kmk)" stroke="#8f1620" stroke-width=".6"/><path d="M69 38 L77 36 L75 46 L68 43 Z" fill="url(#kmk)" stroke="#8f1620" stroke-width=".6"/><path d="M71 43 L78 52 L72 54 L68 45 Z" fill="url(#kmk)" stroke="#8f1620" stroke-width=".6"/>';
    if (head === 4) s += '<ellipse cx="50" cy="33" rx="34" ry="8" fill="#d9b25f" stroke="#a67c2e" stroke-width="1"/><path d="M33 33 Q35 12 50 12 Q65 12 67 33 Z" fill="#e8c77a" stroke="#a67c2e" stroke-width="1"/><path d="M34.5 27 Q50 20 65.5 27" fill="none" stroke="#c8202e" stroke-width="3"/>';
    if (head === 5) {
      s += cap + '<path d="M31 35 Q50 26 69 35 L67 29 L61 31 L57 17 L50 4 L43 17 L39 31 L33 29 Z" fill="' + GOLD + '" stroke="' + GOLDD + '" stroke-width="1"/><path d="M44 28 L50 12 L56 28" fill="none" stroke="' + GOLDD + '" stroke-width="1"/><ellipse cx="50" cy="6" rx="2.6" ry="5" fill="#ff8fab"/><circle cx="30" cy="49" r="3" fill="' + GOLD + '" stroke="' + GOLDD + '" stroke-width=".7"/><circle cx="70" cy="49" r="3" fill="' + GOLD + '" stroke="' + GOLDD + '" stroke-width=".7"/><circle cx="50" cy="32" r="2" fill="#d6336c"/>';
    }
    if (acc === 2) s += '<circle cx="43" cy="47" r="6" fill="none" stroke="#333" stroke-width="1.4"/><circle cx="57" cy="47" r="6" fill="none" stroke="#333" stroke-width="1.4"/><path d="M49 47 H51" stroke="#333" stroke-width="1.4"/>';
    return s + '</g></svg>';
  }
  g.KmAvatar = { svg: svg, random: random, parse: parse, sizes: SIZES, names: N, colors: { bg: BG, skin: SKIN } };
})(window);
