"""contact sheet of the lesson's figures: writes public/_g13_sheet.html (delete before deploy); open http://localhost:8799/_g13_sheet.html"""
import os, sys
HERE = os.path.dirname(__file__); sys.path.insert(0, HERE)
import geo13 as G
figs = [(n, getattr(G, n)) for n in sys.argv[1:]] or [(n, getattr(G, n)) for n in (
    'chord_perp', 'chord_perp_ex', 'chord_ex2', 'chord_ex3', 'chord_prac1', 'equal_chords', 'chord_dist_ex1', 'chord_dist_ex2', 'chord_dist_ex3', 'chord_prac2',
    'tangent_slide', 'tangent_TA', 'tangent_parallel_chord', 'tangents_slide', 'two_tangents_ex1', 'two_tangents_ex2', 'tangents_practice', 'circ_quad', 'incircle_isosceles',
    'common_tangent_ex2', 'tangent_circles_prac', 'circle_tangent_demo_wheel')]
body = ''.join(f'<div class="c"><b>{n}</b>{f()}</div>' for n, f in figs)
html = f'''<!doctype html><meta charset="utf-8"><title>g13 figures</title><link rel="stylesheet" href="/katex/katex.min.css"><link rel="stylesheet" href="/css/teachshow.css">
<style>body{{margin:0;padding:12px;background:#fff;font-family:system-ui}} .g{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}} .c{{border:1px solid #ccc;padding:4px}} svg{{width:100%;height:auto;max-height:none!important}}</style>
<div class="g ts-slide ts-big" style="position:static;padding:0;overflow:visible">{body}</div>
<script src="/katex/katex.min.js"></script><script src="/katex/contrib/auto-render.min.js"></script>
<script>renderMathInElement(document.body,{{delimiters:[{{left:'\\\\(',right:'\\\\)',display:false}}],throwOnError:false}})</script>'''
open(os.path.join(HERE, '..', '..', 'public', '_g13_sheet.html'), 'w', encoding='utf-8').write(html)
print('ok', len(figs))
