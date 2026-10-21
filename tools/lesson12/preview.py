# A contact sheet of every Lesson 12 figure, to look at them side by side: python3 tools/lesson12/preview.py  ->  public/_sheet12.html (not committed)
import os, sys, importlib
HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)
mods = [importlib.import_module(m) for m in sys.argv[1:] or ['vis12a']]
figs = []
for m in mods:
    for name in getattr(m, 'PREVIEW', []):
        fn = getattr(m, name)
        r = fn()
        figs.append((name, r[0] if isinstance(r, tuple) else r))
cards = ''.join(f'<div class="c"><div class="n">{n}</div>{svg}</div>' for n, svg in figs)
html = f'''<!doctype html><meta charset="utf-8"><link rel="stylesheet" href="/css/app.css"><style>
body{{background:#eef2f7;padding:16px;font-family:'Kantumruy Pro',sans-serif}} .g{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}}
.c{{background:#fff;border-radius:12px;padding:10px;box-shadow:0 2px 8px #0002}} .n{{font:600 13px monospace;color:#888}} svg{{width:100%;height:auto;max-height:none!important}}</style><div class="g">{cards}</div>'''
open(os.path.join(HERE, '..', '..', 'public', '_sheet12.html'), 'w', encoding='utf-8').write(html)
print(len(figs), 'figures')
