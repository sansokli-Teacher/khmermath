"""Build the hand-designed Grade 7 Lesson 1 deck -> public/js/slides/g7l01.js
   python3 tools/lesson1/build.py"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import part_a, part_b, part_c, part_d
from lib import stepify

OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'public', 'js', 'slides', 'g7l01.js')
slides = part_a.build() + part_b.build() + part_c.build() + part_d.build()
slides = [stepify(x) if x.get('k') == 'sol' else x for x in slides]   # solutions appear line by line
old = open(OUT, encoding='utf8').read()
head = old.split('\n// Slides generated')[0].split('\nwindow.TEACH_SLIDES')[0]
js = (head + '\n\n// Hand-designed deck for Grade 7 Lesson 1: tools/lesson1/*.py — do not edit by hand.\n'
      + "window.TEACH_SLIDES = window.TEACH_SLIDES || {};\n"
      + "window.TEACH_SLIDES['7-1'] = " + json.dumps(slides, ensure_ascii=False) + ';\n')
open(OUT, 'w', encoding='utf8').write(js)
print(len(slides), 'slides ->', os.path.abspath(OUT), len(js) // 1024, 'KB')
