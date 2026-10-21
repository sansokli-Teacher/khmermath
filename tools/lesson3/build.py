"""Build the Grade 7 Lesson 3 deck -> public/js/slides/g7/lesson3.js
   python3 tools/lesson3/build.py
The book text comes from base_deck.json (generated from Lesson/G7/lesson3.tex by tools/make_g7_slides.py, then frozen here);
this script adds the pictures the book only describes (the «% Diagram:» notes in the .tex), lays the dense slides out again,
and rebuilds the exercise solutions as clean split slides. Every number shown is computed here, never typed twice."""
import json, os, re, sys
HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', 'lesson2'))
from vis3 import *
from lib import stepify, slide, key, ex, prac, sol, m, dm, p, hl, fig, rvd
from tidy_sol import rebuild

OUT = os.path.join(HERE, '..', '..', 'public', 'js', 'slides', 'g7', 'lesson3.js')
base = json.load(open(os.path.join(HERE, 'base_deck.json'), encoding='utf-8'))


def K(i):                                           # the small heading line of base slide i (1-based)
    mt = re.search(r'<p class="ts-kicker">(.*?)</p>', base[i - 1]['html'])
    return mt.group(1) if mt else ''


after, replace = {}, {}

# ---------------------------------------------------------------- 1. notation
after[4] = [ex(K(4), 'ទែម៉ូម៉ែត្រ', fig(thermometer()))]
after[6] = [key(K(6), 'បន្ទាត់ចំនួន', fig(number_line_concept(), 'ក្រិតឯកតាស្មើៗគ្នានៅលើបន្ទាត់ដែលមានទិសដៅ'))]

replace[7] = [prac(K(7), 'លំហាត់គំរូ', p('ខាងក្រោមជាប្រាក់ខាតនិងប្រាក់ចំណេញគិតជាម៉ឺនរៀលក្នុងហាងប្តូរប្រាក់មួយ ។ ពិពណ៌នាជួរឈរសម្រាប់ថ្ងៃព្រហស្បតិ៍និងថ្ងៃសៅរ៍ ។') + fig(week_chart()))]

# ---------------------------------------------------------------- 2. absolute value, order
after[13] = [ex(K(13), 'ចម្ងាយពីគល់ 0', p('ចម្ងាយពី ' + m('3') + ' ទៅ ' + m('0') + ' ស្មើនឹង 3 ឯកតា ហើយចម្ងាយពី ' + m('-3') + ' ទៅ ' + m('0') + ' ក៏ស្មើនឹង 3 ឯកតាដែរ ។') + fig(abs_distance()))]
after[18] = [ex(K(18), 'ប្រៀបធៀបលើបន្ទាត់ចំនួន', fig(order_line()))]

# ---------------------------------------------------------------- 3. opposites, plotting
after[25] = [ex(K(25), 'ចំនួនផ្ទុយ', p(m('-2') + ' ជាចំនួនផ្ទុយនៃ ' + m('2') + ' ។ ចំនួនផ្ទុយនៅឆ្ងាយពីគល់ ' + m('0') + ' ស្មើគ្នា តែនៅសងខាងគល់ ។') + fig(opposite_line()))]
after[30] = [ex(K(30), 'ដៅចំណុច A(4) និង B(−3)', fig(plot_points({'A': 4, 'B': -3}, -5, 5)))]

# ---------------------------------------------------------------- 4. addition and subtraction (the book's marbles and number-line figures)
KA = K(37)
replace[37] = [
    ex(KA, 'ឧទាហរណ៍ 1 ៖ ' + '3 + 4', p('ឃ្លីបូក 3 គ្រាប់ និងឃ្លីបូក 4 គ្រាប់ → ឃ្លីបូកទាំងអស់ 7 គ្រាប់ ។ ដូច្នេះ ' + m(f'3+4={3+4}')) + fig(addition_same(3, 4))),
    ex(KA, 'ឧទាហរណ៍ 2 ៖ (−4) + (−1)', p('ឃ្លីដក 4 គ្រាប់ និងឃ្លីដក 1 គ្រាប់ → ឃ្លីដកទាំងអស់ 5 គ្រាប់ ។ ដូច្នេះ ' + m(f'(-4)+(-1)={-4-1}')) + fig(addition_same(-4, -1))),
]
replace[38] = [
    ex(K(38), 'ឧទាហរណ៍ 3 ៖ 4 + (−2)', p('ឃ្លីបូក 1 និងឃ្លីដក 1 ស្មើនឹងសូន្យ (គូសូន្យ) ។ ឃ្លីបូក 2 ដែលនៅសល់ជាចម្លើយ ។ ដូច្នេះ ' + m(f'4+(-2)={4-2}')) + fig(zero_pairs_add(4, 2))),
    key(K(38), 'វិធាននៃវិធីបូក',
        rvd(1, p(hl('១.', RED) + ' ផលបូកពីរចំនួនគត់រ៉ឺឡាទីបវិជ្ជមាន ជាចំនួនវិជ្ជមាន ហើយផលបូកស្មើនឹងផលបូកតម្លៃដាច់ខាតនៃចំនួនទាំងពីរ ។'))
        + rvd(2, p(hl('២.', RED) + ' ផលបូកពីរចំនួនគត់រ៉ឺឡាទីបអវិជ្ជមាន ជាចំនួនអវិជ្ជមាននៃផលបូកតម្លៃដាច់ខាតនៃចំនួនទាំងពីរ ។'))
        + rvd(3, p(hl('៣.', RED) + ' ផលបូកនៃពីរចំនួនគត់រ៉ឺឡាទីបមានសញ្ញាផ្ទុយគ្នា មានសញ្ញាដូចតួដែលមានតម្លៃដាច់ខាតធំជាងគេ ហើយផលបូកស្មើនឹងផលដកតម្លៃដាច់ខាតនៃចំនួនទាំងពីរ ។'))),
]
KS = K(44)
replace[44] = [ex(KS, 'ឧទាហរណ៍ 1 និង 2 ៖ យកចេញ', p('យកឃ្លីបូក 2 គ្រាប់ចេញពី 4 គ្រាប់ រួចយកឃ្លីដក 2 គ្រាប់ចេញពី 8 គ្រាប់ ។') + fig(subtract_two()))]
replace[45] = [
    ex(K(45), 'ឧទាហរណ៍ 3 ៖ 6 − (−3)', p('គ្មានឃ្លីដកសម្រាប់យកចេញ ត្រូវបន្ថែមគូសូន្យ 3 គូ រួចយកឃ្លីដក 3 គ្រាប់ចេញ ។ ដូច្នេះ ' + m(f'6-(-3)={6+3}')) + fig(subtract_zero_pairs())),
    key(K(45), 'វិធាននៃវិធីដក',
        rvd(1, dm('6-(-3)=6-(-3)+(-3)+(+3)=6+(+3)') + dm('(-5)-(+2)=(-5)-(+2)+(+2)+(-2)=(-5)+(-2)'))
        + rvd(2, p(hl('ដើម្បីដកចំនួនគត់រ៉ឺឡាទីប គេត្រូវបូកចំនួននោះជាមួយចំនួនផ្ទុយរបស់វា ។', RED)) + dm('a-b=a+(-b)'))),
    ex(K(45), 'ឧទាហរណ៍ ៖ ដកជាការបូកចំនួនផ្ទុយ',
       rvd(1, dm(f'(-3)-(7)=(-3)+(-7)={-3-7}')) + rvd(2, dm(f'(-11)-(-5)=(-11)+(5)={-11+5}'))
       + rvd(3, p('ជាទូទៅ ៖') + dm('+(+a)=a,\\quad -(-a)=a,\\quad +(-a)=-a,\\quad -(+a)=-a'))),
]

# ---------------------------------------------------------------- 5. multiplication and division
after[55] = [
    key(K(55), 'វិធាននៃវិធីគុណ', fig(sign_grid('×'))),
    ex(K(55), 'តើហេតុអ្វី (−)×(−) = (+) ?', p('សង្កេតលំនាំ ៖ ផលគុណកើនឡើងម្ដងបី ៣ នៅពេលកត្តាទីពីរថយចុះម្ដងមួយ ។') + fig(pattern_mult())),
]
after[61] = [key(K(61), 'វិធាននៃវិធីចែក', fig(sign_grid('÷')))]

# ---------------------------------------------------------------- 6. order of operations
steps = [('6 + 4 \\times (8-5) \\div 2', ''), ('= 6 + 4 \\times 3 \\div 2', 'គណនាក្នុងវង់ក្រចក'), ('= 6 + 12 \\div 2', 'គុណមុន (ពីឆ្វេងទៅស្តាំ)'), ('= 6 + 6', 'ចែក'), ('= 12', 'បូក')]
assert 6 + 4 * (8 - 5) // 2 == 12


def orow(f, note=''):                                    # a formula and, on its right, which rule was used
    return ('<div style="display:flex;align-items:center;gap:36px;margin:6px 0">'
            + f'<div style="min-width:46%">{dm(f)}</div>' + (f'<div style="font-size:.9em">{hl("→ " + note, BLUE)}</div>' if note else '') + '</div>')


after[81] = [
    key(K(81), 'លំដាប់ប្រមាណវិធី', fig(order_ladder())),
    ex(K(81), 'ឧទាហរណ៍ ៖ ប្រើលំដាប់ទាំងបី', orow(*steps[0]) + ''.join(rvd(i, orow(f, note)) for i, (f, note) in enumerate(steps) if i)),
]

# ---------------------------------------------------------------- 7. exercise 2: points A, B, C, D and their distances
EX2 = {'B': -6, 'A': -4, 'C': 3, 'D': 5}
AB, AC, BC = abs(EX2['B'] - EX2['A']), abs(EX2['C'] - EX2['A']), abs(EX2['C'] - EX2['B'])
assert (AB, AC, BC) == (2, 7, 9)
KX = '2. ដំណោះស្រាយ'
replace[106] = [
    sol('ចម្លើយ', 'ដំណោះស្រាយ លំហាត់ទី ២ (១/២)', p('ដៅចំណុចលើបន្ទាត់ចំនួន ៖') + fig(plot_points(EX2, -7, 6))),
    sol('ចម្លើយ', 'ដំណោះស្រាយ លំហាត់ទី ២ (២/២)',
        rvd(1, p(hl('AB', PURPLE) + ' ៖ A និង B នៅខាងឆ្វេងគល់ទាំងពីរ') + dm(f'AB=|{-6}|-|{-4}|={abs(-6)}-{abs(-4)}={AB}'))
        + rvd(2, p(hl('AC', ORANGE) + ' ៖ A និង C នៅសងខាងគល់') + dm(f'AC=|{-4}|+|{3}|={abs(-4)}+{abs(3)}={AC}'))
        + rvd(3, p(hl('BC', GREEN) + ' ៖ B និង C នៅសងខាងគល់') + dm(f'BC=|{-6}|+|{3}|={abs(-6)}+{abs(3)}={BC}'))),
]

# the exercises are the 8th part of the lesson board: a numbered title slide so «ផ្នែក ៨» opens them
EXI = next(n for n, x in enumerate(base, 1) if x.get('k') == 'title' and '<h1>លំហាត់</h1>' in x['html'])
nex = sum(1 for x in base if x['html'].count('<h2>លំហាត់ទី ') and x.get('k') == 'prac')
replace[EXI] = [{'k': 'title', 'html': f'<h1>8. លំហាត់</h1><p class="ts-sub">{str(nex).translate(str.maketrans("0123456789", "០១២៣៤៥៦៧៨៩"))} លំហាត់</p>'}]

# ---------------------------------------------------------------- assemble
out = []
for n, s_ in enumerate(base, 1):
    out.extend(replace.get(n, [s_]))
    out.extend(after.get(n, []))
out = rebuild(out)                                                    # exercise solutions: one group of sub-questions per slide
out = [stepify(x) if x.get('k') == 'sol' and 'data-step' not in x['html'] else x for x in out]
js = ('// Hand-designed deck for Grade 7 Lesson 3: tools/lesson3/*.py — do not edit by hand.\n'
      + "window.TEACH_SLIDES = window.TEACH_SLIDES || {};\n"
      + "window.TEACH_SLIDES['7-3'] = " + json.dumps(out, ensure_ascii=False) + ';\n')
open(OUT, 'w', encoding='utf8').write(js)
print(len(base), '->', len(out), 'slides ->', os.path.abspath(OUT), len(js) // 1024, 'KB')
