"""sheet of ALL the lesson's figures at full size: writes public/_g13_sheet.html (delete before deploy)"""
import os, sys
HERE = os.path.dirname(__file__); sys.path.insert(0, HERE)
import geo13 as G
def one(f, *a):
    r = f(*a)
    return r[0] if isinstance(r, tuple) else r
items = []
for n in ('chord_perp', 'chord_perp_ex', 'chord_ex2', 'chord_ex3', 'chord_prac1', 'equal_chords', 'chord_dist_ex1', 'chord_dist_ex2', 'chord_dist_ex3', 'chord_prac2', 'tangent_slide', 'tangent_rule', 'tangent_TA', 'tangent_prac',
          'tangent_parallel_chord', 'tangents_slide', 'two_tangents_ex1', 'two_tangents_ex2', 'tangents_practice', 'circ_quad', 'incircle_isosceles', 'positions_slide', 'common_tangent_ex2', 'tangent_circles_prac', 'circle_tangent_demo_wheel', 'vocab'):
    items.append((n, one(getattr(G, n))))
for d in (330, 158, 100, 42, 20):
    items.append((f'common_tangents d={d}', one(G.common_tangents_fig, d)))
for k in 'abcdef': items.append((f'ex1{k}', one(G.ex1, k)))
for k in 'abcd': items.append((f'ex2{k}', one(G.ex2, k)))
for k in 'ab': items.append((f'ex3{k}', one(G.ex3, k)))
for n in ('ex4', 'ex5', 'ex6', 'ex7', 'ex8', 'ex9', 'ex10', 'ex11', 'ex12', 'ex13'): items.append((n, one(getattr(G, n))))
body = ''.join(f'<div class="c"><b>{n}</b>{s}</div>' for n, s in items)
html = f'''<!doctype html><meta charset="utf-8"><title>g13 figures</title><link rel="stylesheet" href="/katex/katex.min.css"><link rel="stylesheet" href="/css/teachshow.css">
<style>body{{margin:0;padding:8px;background:#fff;font-family:system-ui}} .g{{display:grid;grid-template-columns:repeat(2,1fr);gap:8px}} .c{{border:1px solid #bbb;padding:4px}} .c b{{font-size:16px;color:#c00}} svg{{width:100%;height:auto;max-height:none!important}}</style>
<div class="g ts-slide ts-big" style="position:static;padding:0;overflow:visible">{body}</div>
<script>var only=decodeURIComponent(location.hash.slice(1)).split(',').filter(Boolean);if(only.length)document.querySelectorAll('.c').forEach(function(e){{if(only.indexOf(e.querySelector('b').textContent)<0)e.style.display='none'}})</script><script src="/katex/katex.min.js"></script><script src="/katex/contrib/auto-render.min.js"></script>
<script>renderMathInElement(document.body,{{delimiters:[{{left:'\\\\(',right:'\\\\)',display:false}}],throwOnError:false}})</script>'''
open(os.path.join(HERE, '..', '..', 'public', '_g13_sheet.html'), 'w', encoding='utf-8').write(html)
print('figures', len(items))
