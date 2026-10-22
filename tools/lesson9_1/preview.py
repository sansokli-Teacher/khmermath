# Contact sheet of the Grade 9 Lesson 1 figures: python3 tools/lesson9_1/preview.py -> public/_sheet91.html
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import vis9
figs = []
for name in vis9.PREVIEW:
    r = getattr(vis9, name)()
    figs.append((name, r if isinstance(r, str) else r[0]))
cards = ''.join(f'<div class="c"><div class="n">{n}</div>{svg}</div>' for n, svg in figs)
html = '''<!doctype html><meta charset="utf-8"><style>
body{background:#eef2f7;padding:16px;font-family:sans-serif} .g{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}
.c{background:#fff;border-radius:12px;padding:10px;box-shadow:0 2px 8px #0002} .n{font:600 13px monospace;color:#888} svg{width:100%;height:auto;max-height:none!important}</style><div class="g">''' + cards + '</div>'
open(os.path.join(os.path.dirname(__file__), '..', '..', 'public', '_sheet91.html'), 'w', encoding='utf-8').write(html)
print(len(figs), 'figures')
