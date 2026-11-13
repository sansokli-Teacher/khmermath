# -*- coding: utf-8 -*-
"""python3 make_review.py G12L01 OUTDIR  -> OUTDIR/index.html : the whole lesson set rendered for a human check (KaTeX + SVG)."""
import sys, importlib, html, collections
sys.path.insert(0, '.')
name, out = sys.argv[1], sys.argv[2]
mod = importlib.import_module('gen12sc.' + name)
C = mod.cands()
LV = {'easy': 'ងាយ', 'medium': 'មធ្យម', 'hard': 'ពិបាក', 'pisa': 'PISA'}
rows = []
for n, q in enumerate(C, 1):
    opts = ''
    if q['kind'] == 'mcq':
        letters = 'កខគឃ'
        opts = '<ol class="o">' + ''.join('<li class="%s"><b>%s.</b> %s</li>' % ('ok' if i == 0 else '', letters[i], html.escape(o)) for i, o in enumerate(q['options'])) + '</ol>'
    img = ('<div class="img">%s</div>' % q['img']) if q.get('img') else ''
    sol = html.escape(q['sol']).replace('\n', '<br>')
    rows.append('<section><h3>#%d <span class="t %s">%s · %s</span> <span class="b">Bloom: %s</span></h3><p>%s</p>%s%s<div class="s"><b>%s</b><br>%s</div></section>' % (
        n, q['level'], 'MCQ' if q['kind'] == 'mcq' else 'ឆ្លើយតប ៥ ពិន្ទុ', LV[q['level']], q['bloom'], html.escape(q['stem']), img, opts,
        'ដំណោះស្រាយ' if q['kind'] == 'mcq' else 'គ្រោងពិន្ទុ', sol))
summ = collections.Counter(q['bloom'] for q in C)
page = '''<!doctype html><meta charset="utf-8"><title>%s review</title>
<link rel="stylesheet" href="katex/katex.min.css">
<style>body{font:16px/1.6 "Noto Sans Khmer","Khmer OS",sans-serif;max-width:900px;margin:20px auto;padding:0 14px;color:#1e293b}
section{border:1px solid #cbd5e1;border-radius:10px;padding:10px 16px;margin:14px 0}h3{margin:0 0 6px;font-size:15px}
.t{background:#e0e7ff;border-radius:6px;padding:1px 8px}.t.hard{background:#fee2e2}.t.pisa{background:#dcfce7}.t.medium{background:#fef3c7}
.b{float:right;color:#7c3aed}.o{list-style:none;padding:0;margin:6px 0}.o li{padding:3px 8px;border-radius:6px}.o li.ok{background:#dcfce7}
.s{background:#f1f5f9;border-radius:8px;padding:8px 12px;margin-top:8px;font-size:14px}.img{margin:8px 0;background:#fff;padding:4px;display:inline-block;border:1px dashed #cbd5e1}</style>
<h2>%s — %d សំណួរ</h2><p>Bloom: %s</p>%s
<script src="katex/katex.min.js"></script><script src="katex/contrib/auto-render.min.js"></script>
<script>renderMathInElement(document.body,{delimiters:[{left:"\\\\(",right:"\\\\)",display:false},{left:"\\\\[",right:"\\\\]",display:true}],throwOnError:false});</script>''' % (
    name, name, len(C), ', '.join('%s %d' % kv for kv in summ.items()), '\n'.join(rows))
open(out + '/index.html', 'w', encoding='utf-8').write(page)
print('wrote', out + '/index.html')
