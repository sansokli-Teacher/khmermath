"""Build the hand-designed Grade 7 Lesson 2 deck -> public/js/slides/g7/lesson2.js
   python3 tools/lesson2/build.py
Same style as Lesson 1 (tools/lesson1): the slideshow adds the school / teacher slide in front; every part opens with a picture;
solutions and examples appear step by step; part 7 is «លំហាត់»."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import part2_a, part2_b, part2_c
from lib import stepify

OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'public', 'js', 'slides', 'g7', 'lesson2.js')
slides = part2_a.build() + part2_b.build() + part2_c.build()
slides = [stepify(x) if x.get('k') == 'sol' else x for x in slides]      # solutions appear line by line
js = ('// Hand-designed deck for Grade 7 Lesson 2: tools/lesson2/*.py — do not edit by hand.\n'
      + "window.TEACH_SLIDES = window.TEACH_SLIDES || {};\n"
      + "window.TEACH_SLIDES['7-2'] = " + json.dumps(slides, ensure_ascii=False) + ';\n')
open(OUT, 'w', encoding='utf8').write(js)
print(len(slides), 'slides ->', os.path.abspath(OUT), len(js) // 1024, 'KB')
