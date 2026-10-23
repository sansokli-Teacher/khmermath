"""contact sheet of the deck's slides (all steps showing, text fitted like the show does): writes public/_g8_sheet.html  (delete before deploy)
open  http://localhost:8765/_g8_sheet.html#0-5   = slides 0..5"""
import os
HERE = os.path.dirname(__file__)
html = '''<!doctype html><meta charset="utf-8"><title>g8 sheet</title>
<link rel="stylesheet" href="/fonts/kantumruy-pro.css"><link rel="stylesheet" href="/css/teachshow.css"><link rel="stylesheet" href="/katex/katex.min.css">
<style>body{margin:0;background:#888} #g{display:grid;grid-template-columns:repeat(2,964px);gap:8px;padding:8px} .w{position:relative;width:1920px;height:1080px;zoom:.5;overflow:hidden;background:#fff;border:3px solid #222} .w.bad{border-color:red}
.n{position:absolute;right:8px;top:4px;z-index:5;background:#222;color:#fff;font:700 22px system-ui;padding:2px 10px;border-radius:8px}</style>
<div id="g"></div>
<script src="/katex/katex.min.js"></script><script src="/katex/contrib/auto-render.min.js"></script><script src="/js/slides/g8/lesson12.js"></script>
<script>
const S = window.TEACH_SLIDES['8-12'];
const [a, b] = (location.hash.slice(1) || '0-5').split('-').map(Number);
const g = document.getElementById('g');
for (let i = a; i <= Math.min(b, S.length - 1); i++) {
  const s = S[i], w = document.createElement('div'); w.className = 'w';
  const el = document.createElement('div'); el.className = 'ts-slide' + (s.k ? ' ts-' + s.k : '') + (s.c ? ' ts-' + s.c : '') + ' ts-big';
  el.innerHTML = s.html.replace(/max-height:\s*(\d+)vh/g, (m, n) => 'max-height:' + (n * 10.8) + 'px'); const st = document.createElement('div'); st.className = 'ts-stage ts-theme-esc'; st.style.cssText = 'position:absolute;inset:0'; st.append(el); w.append(st);   // vh of the real stage = 10.8px on a 1080px-high slide
  const n = document.createElement('div'); n.className = 'n'; n.textContent = i; w.append(n);
  g.append(w);
  renderMathInElement(el, {delimiters:[{left:'\\\\(',right:'\\\\)',display:false},{left:'\\\\[',right:'\\\\]',display:true}], throwOnError:false});
  // like fitText(0.72)
  const base = parseFloat(getComputedStyle(el).fontSize); let px = base;
  const over = () => el.scrollHeight > el.clientHeight + 2 || el.scrollWidth > el.clientWidth + 2;
  for (let k = 0; k < 30 && over() && px > base * .72; k++) { px *= .94; el.style.fontSize = px + 'px'; }
  if (over()) { w.classList.add('bad'); n.textContent = i + ' ✖ h+' + (el.scrollHeight - el.clientHeight) + ' w+' + (el.scrollWidth - el.clientWidth) + ' font ' + Math.round(px); }
}
</script>'''
open(os.path.join(HERE, '..', '..', 'public', '_g8_sheet.html'), 'w', encoding='utf-8').write(html)
print('ok')
