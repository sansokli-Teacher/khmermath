"""Build the hand-designed Grade 7 Lesson 1 deck -> public/js/slides/g7l01.js
   python3 tools/lesson1/build.py"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import part_a, part_b, part_c, part_d
from lib import stepify, merge_slides

OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'public', 'js', 'slides', 'g7l01.js')
slides = part_a.build() + part_b.build() + part_c.build() + part_d.build()
# short neighbouring slides (a lone ជាទូទៅ / សម្គាល់ card, one-line examples) are combined; each later part rises in on the next press of →.
# numbers are slide numbers in the deck before merging; SKIP_MERGE="11,57" leaves those groups alone (used when one does not fit)
# (the school/teacher branding slide is slide 1, the lesson cover slide 2, so these numbers are one higher than before it existed)
GROUPS = [(12, 13), (23, 24), (40, 41), (58, 59), (84, 85), (86, 87, 88), (91, 92), (93, 94)]   # (111, 112) was tried: a 3D cube plus a card does not fit on one page
skip = {int(x) for x in os.environ.get('SKIP_MERGE', '').split(',') if x.strip()}
by_first = {g[0]: g for g in GROUPS if g[0] not in skip}
merged, drop = [], set()
for n, x in enumerate(slides, 1):
    if n in drop:
        continue
    g = by_first.get(n)
    if g:
        parts = [slides[k - 1] for k in g]
        assert all(slides[k - 1].get('html', '').split('</p>')[0] == parts[0]['html'].split('</p>')[0] for k in g), f'group {g}: different sections'
        merged.append(merge_slides(parts))
        drop.update(g[1:])
    else:
        merged.append(x)
slides = merged
# an exercise and its answer on ONE slide: the question stays, the answer rises in on the next press of →
for title in ['លំហាត់ទី ៥']:
    for i, x in enumerate(slides):
        if f'<h2>{title}</h2>' in x.get('html', '') and i + 1 < len(slides) and f'<h2>ចម្លើយ{title}</h2>' in slides[i + 1].get('html', ''):
            slides[i:i + 2] = [merge_slides([x, slides[i + 1]])]
            break
slides = [stepify(x) if x.get('k') == 'sol' else x for x in slides]   # solutions appear line by line
old = open(OUT, encoding='utf8').read()
head = old.split('\n// Slides generated')[0].split('\nwindow.TEACH_SLIDES')[0]
js = (head + '\n\n// Hand-designed deck for Grade 7 Lesson 1: tools/lesson1/*.py — do not edit by hand.\n'
      + "window.TEACH_SLIDES = window.TEACH_SLIDES || {};\n"
      + "window.TEACH_SLIDES['7-1'] = " + json.dumps(slides, ensure_ascii=False) + ';\n')
open(OUT, 'w', encoding='utf8').write(js)
print(len(slides), 'slides ->', os.path.abspath(OUT), len(js) // 1024, 'KB')
