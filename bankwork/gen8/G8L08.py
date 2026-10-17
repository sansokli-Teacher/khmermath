from lib import *
import sympy as sp
from sympy import symbols, Rational as Q_
from sympy.parsing.sympy_parser import parse_expr
import re as _re

LESSON = 'វិសមីការដឺក្រេទី ១ មានមួយអញ្ញាត'
x, y, z, a, b, c, t, m, n, d, k, q = symbols('x y z a b c t m n d k q')
_LD = {s_.name: s_ for s_ in (x, y, z, a, b, c, t, m, n, d, k, q)}

def L(e): return sp.latex(e).replace(r'\\frac', r'\\dfrac')

C = []

def uniq(correct, cands, k_=3):
    out = [correct]
    for c_ in cands:
        if c_ not in out: out.append(c_)
        if len(out) == k_ + 1: break
    assert len(out) == k_ + 1, ('wrongs', correct)
    return out[1:]

def with_img(q_, s_): q_['img'] = s_; return q_

# ---------- figures (Transparent background, Mathcad Italic variables, Upright serif dimensions) ----------
FIG_SEESAW = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 340 140' width='340' height='140'>
  <!-- Ground -->
  <line x1='20' y1='120' x2='320' y2='120' stroke='#64748b' stroke-width='2'/>
  <!-- Fulcrum -->
  <polygon points='170,75 150,120 190,120' fill='#f59e0b' stroke='#b45309' stroke-width='1.5'/>
  <circle cx='170' cy='75' r='4' fill='#78350f'/>
  <!-- Plank tilted -12 deg -->
  <g transform='rotate(-12 170 75)'>
    <rect x='40' y='71' width='260' height='8' rx='2' fill='#0284c7' stroke='#0369a1' stroke-width='1.5'/>
    <!-- Left seat (Sokha, higher) -->
    <circle cx='65' cy='52' r='14' fill='#bfdbfe' stroke='#2563eb' stroke-width='1.5'/>
    <text x='65' y='56' text-anchor='middle' font-family='Khmer OS Battambang,Noto Sans Khmer,serif' font-size='10' fill='#1e3a8a'>សុខា</text>
    <text x='65' y='32' text-anchor='middle' font-family='Times New Roman,serif' font-size='12' font-weight='bold' fill='#1e3a8a'>48 kg</text>
    <!-- Right seat (Phally, lower) -->
    <circle cx='275' cy='52' r='14' fill='#fecaca' stroke='#dc2626' stroke-width='1.5'/>
    <text x='275' y='56' text-anchor='middle' font-family='Khmer OS Battambang,Noto Sans Khmer,serif' font-size='10' fill='#991b1b'>ផល្លី</text>
    <text x='275' y='32' text-anchor='middle' font-family='Mathcad UniMath Italic,Times New Roman,serif' font-style='italic' font-size='13' fill='#991b1b'>x <tspan font-style='normal' font-family='Times New Roman,serif'>kg</tspan></text>
  </g>
  <!-- Relation label -->
  <text x='170' y='35' text-anchor='middle' font-family='Mathcad UniMath Italic,Times New Roman,serif' font-style='italic' font-size='15' fill='#0f172a'>x &gt; <tspan font-style='normal'>48</tspan></text>
</svg>"""

FIG_TRIANGLE = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 300 160' width='300' height='160'>
  <polygon points='35,130 250,130 165,30' fill='#f0fdf4' stroke='#16a34a' stroke-width='2'/>
  <!-- Vertices -->
  <text x='25' y='142' font-family='Mathcad UniMath Italic,Times New Roman,serif' font-style='italic' font-size='15' fill='#14532d'>A</text>
  <text x='258' y='142' font-family='Mathcad UniMath Italic,Times New Roman,serif' font-style='italic' font-size='15' fill='#14532d'>B</text>
  <text x='165' y='22' text-anchor='middle' font-family='Mathcad UniMath Italic,Times New Roman,serif' font-style='italic' font-size='15' fill='#14532d'>C</text>
  <!-- Side Labels -->
  <text x='142' y='146' text-anchor='middle' font-family='Times New Roman,serif' font-size='13' font-weight='bold' fill='#0f172a'>AB = 12</text>
  <text x='85' y='75' text-anchor='end' font-family='Mathcad UniMath Italic,Times New Roman,serif' font-style='italic' font-size='14' fill='#0f172a'>AC = <tspan font-style='normal'>2</tspan>x</text>
  <text x='220' y='75' text-anchor='start' font-family='Mathcad UniMath Italic,Times New Roman,serif' font-style='italic' font-size='14' fill='#0f172a'>BC = x</text>
</svg>"""

FIG_MONITOR = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 320 170' width='320' height='170'>
  <!-- Screen Frame -->
  <rect x='35' y='15' width='250' height='120' rx='6' fill='#f8fafc' stroke='#334155' stroke-width='2'/>
  <rect x='45' y='25' width='230' height='100' fill='#e2e8f0' stroke='#94a3b8' stroke-width='1'/>
  <!-- Stand -->
  <polygon points='150,135 170,135 175,152 145,152' fill='#64748b'/>
  <rect x='125' y='152' width='70' height='6' rx='2' fill='#475569'/>
  <!-- Dimension Labels -->
  <line x1='45' y1='130' x2='275' y2='130' stroke='#2563eb' stroke-width='1.2'/>
  <text x='160' y='118' text-anchor='middle' font-family='Khmer OS Battambang,Noto Sans Khmer,serif' font-size='12' fill='#1e40af'>បណ្តោយ <tspan font-family='Mathcad UniMath Italic,Times New Roman,serif' font-style='italic'>x</tspan></text>
  <line x1='290' y1='25' x2='290' y2='125' stroke='#dc2626' stroke-width='1.2'/>
  <text x='296' y='80' font-family='Khmer OS Battambang,Noto Sans Khmer,serif' font-size='11' fill='#991b1b'>ទទឹង <tspan font-family='Mathcad UniMath Italic,Times New Roman,serif' font-style='italic'>2x - 20</tspan></text>
</svg>"""

FIG_NUMLINE = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 340 70' width='340' height='70'>
  <line x1='20' y1='35' x2='320' y2='35' stroke='#1e293b' stroke-width='1.6'/>
  <polyline points='312,30 320,35 312,40' fill='none' stroke='#1e293b' stroke-width='1.6'/>
  <!-- Tick marks -->
  <line x1='120' y1='30' x2='120' y2='40' stroke='#1e293b' stroke-width='1.4'/>
  <text x='120' y='55' text-anchor='middle' font-family='Times New Roman,serif' font-size='13'>0</text>
  <line x1='210' y1='30' x2='210' y2='40' stroke='#1e293b' stroke-width='1.4'/>
  <text x='210' y='55' text-anchor='middle' font-family='Times New Roman,serif' font-size='13' font-weight='bold'>2</text>
  <!-- Solution ray x > 2 -->
  <line x1='210' y1='35' x2='315' y2='35' stroke='#2563eb' stroke-width='3.5'/>
  <!-- Open bracket or circle at 2 -->
  <circle cx='210' cy='35' r='4.5' fill='white' stroke='#2563eb' stroke-width='2'/>
  <text x='265' y='24' text-anchor='middle' font-family='Mathcad UniMath Italic,Times New Roman,serif' font-style='italic' font-size='13' fill='#1d4ed8'>x &gt; <tspan font-style='normal'>2</tspan></text>
</svg>"""

def cands():
    global C
    C = []
    # ================= 1. NOTION & PROPERTIES (Easy MCQ) =================
    C.append(mcq('easy', 'notion', 'វិសមីការដឺក្រេទី ១ មានមួយអញ្ញាតមានរាងទូទៅមួយក្នុងចំណោម ៖', M('ax + b > 0\\ (a \\neq 0)'), [M('ax^2 + b > 0'), M('ax + by > 0'), M('\\dfrac{a}{x} + b > 0')], 'មានអញ្ញាតតែមួយ ហើយអថេរមានដឺក្រេទី ១ (និទស្សន្តស្មើ ១)។'))
    C.append(mcq('easy', 'notion', 'បើ ' + M('a < b') + ' នោះគេបាន ៖', M('a + c < b + c'), [M('a + c > b + c'), M('a - c > b - c'), M('a + c = b + c')], 'កាលណាបូកចំនួនដូចគ្នាទៅអង្គទាំងពីរ វិសមភាពមិនប្តូរទិសដៅទេ។'))
    C.append(mcq('easy', 'notion', 'បើ ' + M('a < b') + ' និង ' + M('c < 0') + ' (ចំនួនអវិជ្ជមាន) នោះគេបាន ៖', M('ac > bc'), [M('ac < bc'), M('ac = bc'), M('a + c > b + c')], 'កាលណាគុណនឹងចំនួនអវិជ្ជមាន វិសមភាពត្រូវប្តូរទិសដៅ។'))
    C.append(mcq('easy', 'notion', 'បើចែកអង្គទាំងពីរនៃវិសមីការនឹងចំនួនអវិជ្ជមាន ' + M('(-3)') + ' នោះវិសមភាពត្រូវ ៖', 'ប្តូរទិសដៅ (ត្រឡប់សញ្ញា)', ['រក្សាទិសដៅដដែល', 'ក្លាយជាសមភាព (=)', 'គ្មានចម្លើយ'], 'វិធានគុណនិងចែកនឹងចំនួនអវិជ្ជមាន តម្រូវឱ្យប្តូរទិសដៅវិសមភាព។'))
    C.append(mcq('easy', 'notion', 'ចម្លើយនៃ ' + M('x - 3 \\le 7') + ' គឺ ៖', M('x \\le 10'), [M('x < 10'), M('x \\ge 10'), M('x \\le 4')], M('x \\le 7 + 3 = 10') + '។'))
    C.append(mcq('easy', 'notion', 'ចម្លើយនៃ ' + M('x - 5 < 5') + ' គឺ ៖', M('x < 10'), [M('x \\le 10'), M('x < 0'), M('x > 10')], M('x < 5 + 5 = 10') + '។'))
    C.append(mcq('easy', 'notion', 'ចម្លើយនៃ ' + M('x + 30 > 50') + ' គឺ ៖', M('x > 20'), [M('x < 20'), M('x \\ge 20'), M('x > 80')], M('x > 50 - 30 = 20') + '។'))
    C.append(mcq('easy', 'notion', 'ចម្លើយនៃ ' + M('x + \\dfrac{3}{4} > \\dfrac{3}{4}') + ' គឺ ៖', M('x > 0'), [M('x < 0'), M('x > \\dfrac{3}{4}'), M('x > 1')], M('x > \\dfrac{3}{4} - \\dfrac{3}{4} = 0') + '។'))
    C.append(mcq('easy', 'notion', 'ដោះស្រាយវិសមីការ ' + M('x + 1.5 \\ge 0.5') + ' ៖', M('x \\ge -1'), [M('x \\le -1'), M('x \\ge 2'), M('x \\le 2')], M('x \\ge 0.5 - 1.5 = -1') + '។'))
    C.append(mcq('easy', 'notion', 'ដោះស្រាយវិសមីការ ' + M('x - 100 \\ge 200') + ' ៖', M('x \\ge 300'), [M('x \\le 300'), M('x \\ge 100'), M('x \\le 100')], M('x \\ge 200 + 100 = 300') + '។'))
    C.append(mcq('easy', 'notion', 'ដោះស្រាយវិសមីការ ' + M('2 + 3x < 2x + 1') + ' ៖', M('x < -1'), [M('x > -1'), M('x < 1'), M('x > 3')], M('3x - 2x < 1 - 2 \\Rightarrow x < -1') + '។'))
    C.append(mcq('easy', 'notion', 'ដោះស្រាយវិសមីការ ' + M('-5 + 6m \\ge 5m + 2') + ' ៖', M('m \\ge 7'), [M('m \\le 7'), M('m \\ge -3'), M('m \\le 3')], M('6m - 5m \\ge 2 + 5 \\Rightarrow m \\ge 7') + '។'))

    # ================= 2. BASIC / MEDIUM EQUATIONS (Medium MCQ) =================
    C.append(mcq('medium', 'basic', 'ដោះស្រាយវិសមីការ ' + M('2x + 7 > 3x - 2') + ' ៖', M('x < 9'), [M('x > 9'), M('x < -9'), M('x > -9')], M('2x - 3x > -2 - 7 \\Rightarrow -x > -9 \\Rightarrow x < 9') + '។'))
    C.append(mcq('medium', 'basic', 'ដោះស្រាយវិសមីការ ' + M('5m - 4 \\ge 4m + 11') + ' ៖', M('m \\ge 15'), [M('m \\le 15'), M('m \\ge 7'), M('m \\le 7')], M('5m - 4m \\ge 11 + 4 \\Rightarrow m \\ge 15') + '។'))
    C.append(mcq('medium', 'basic', 'ដោះស្រាយវិសមីការ ' + M('2x - 5 + 3x > -5x + 15') + ' ៖', M('x > 2'), [M('x < 2'), M('x > 1'), M('x < 1')], M('5x - 5 > -5x + 15 \\Rightarrow 10x > 20 \\Rightarrow x > 2') + '។'))
    C.append(mcq('medium', 'basic', 'ដោះស្រាយវិសមីការ ' + M('y + 3(2y+1) \\le 12 + y') + ' ៖', M('y \\le \\dfrac{3}{2}'), [M('y \\ge \\dfrac{3}{2}'), M('y \\le \\dfrac{9}{7}'), M('y \\ge 1')], M('7y + 3 \\le 12 + y \\Rightarrow 6y \\le 9 \\Rightarrow y \\le \\dfrac{3}{2}') + '។'))
    C.append(mcq('medium', 'basic', 'ដោះស្រាយវិសមីការ ' + M('-\\dfrac{2}{7}t \\ge \\dfrac{2}{7}') + ' ៖', M('t \\le -1'), [M('t \\ge -1'), M('t \\ge 1'), M('t \\le 1')], 'គុណនឹង ' + M('-\\dfrac{7}{2}') + ' ប្តូរទិសដៅ ៖ ' + M('t \\le -1') + '។'))
    C.append(mcq('medium', 'basic', 'ដោះស្រាយវិសមីការ ' + M('-\\dfrac{3}{11}q \\le \\dfrac{3}{22}') + ' ៖', M('q \\ge -\\dfrac{1}{2}'), [M('q \\le -\\dfrac{1}{2}'), M('q \\ge \\dfrac{1}{2}'), M('q \\le \\dfrac{1}{2}')], M('q \\ge \\dfrac{3}{22} \\times \\left(-\\dfrac{11}{3}\\right) = -\\dfrac{1}{2}') + '។'))
    C.append(mcq('medium', 'basic', 'ដោះស្រាយវិសមីការ ' + M('3a - 5 + 2a - 7 \\le 8a + a - 12 + 2') + ' ៖', M('a \\ge -\\dfrac{1}{2}'), [M('a \\le -\\dfrac{1}{2}'), M('a \\ge \\dfrac{1}{2}'), M('a \\le 2')], M('5a - 12 \\le 9a - 10 \\Rightarrow -4a \\le 2 \\Rightarrow a \\ge -\\dfrac{1}{2}') + '។'))
    C.append(mcq('medium', 'frac', 'ដោះស្រាយវិសមីការ ' + M('3x - \\dfrac{x}{2} < 1 + \\dfrac{x}{3}') + ' ៖', M('x < \\dfrac{6}{13}'), [M('x > \\dfrac{6}{13}'), M('x < \\dfrac{13}{6}'), M('x < 1')], 'ភាគបែងរួម 6 ៖ ' + M('18x - 3x < 6 + 2x \\Rightarrow 13x < 6 \\Rightarrow x < \\dfrac{6}{13}') + '។'))
    C.append(mcq('medium', 'frac', 'ដោះស្រាយវិសមីការ ' + M('\\dfrac{m}{2} + \\dfrac{m}{3} + 2m > 3') + ' ៖', M('m > \\dfrac{18}{17}'), [M('m < \\dfrac{18}{17}'), M('m > 1'), M('m > \\dfrac{17}{18}')], 'ភាគបែងរួម 6 ៖ ' + M('3m + 2m + 12m > 18 \\Rightarrow 17m > 18 \\Rightarrow m > \\dfrac{18}{17}') + '។'))
    C.append(mcq('medium', 'frac', 'ដោះស្រាយវិសមីការ ' + M('\\dfrac{m-1}{4} - 3 < \\dfrac{3(m+1)}{8}') + ' ៖', M('m > -29'), [M('m < -29'), M('m > 29'), M('m < 29')], 'គុណនឹង 8 ៖ ' + M('2(m-1) - 24 < 3(m+1) \\Rightarrow 2m - 26 < 3m + 3 \\Rightarrow m > -29') + '។'))
    C.append(mcq('medium', 'frac', 'ដោះស្រាយវិសមីការ ' + M('2 + \\dfrac{3(m+1)}{8} < 3 - \\dfrac{m-1}{4}') + ' ៖', M('m < \\dfrac{7}{5}'), [M('m > \\dfrac{7}{5}'), M('m < \\dfrac{5}{7}'), M('m < 1')], 'គុណនឹង 8 ៖ ' + M('16 + 3m + 3 < 24 - 2m + 2 \\Rightarrow 5m < 7 \\Rightarrow m < \\dfrac{7}{5}') + '។'))
    C.append(mcq('medium', 'word', 'ផលដករវាង ២ និងមួយចំនួនធំជាងផលបូករវាង ៣ និងពីរដងនៃចំនួននោះ។ ចំនួននោះគឺ ៖', M('x < -\\dfrac{1}{3}'), [M('x > -\\dfrac{1}{3}'), M('x < -1'), M('x > 1')], M('2 - x > 3 + 2x \\Rightarrow -3x > 1 \\Rightarrow x < -\\dfrac{1}{3}') + '។'))
    C.append(mcq('medium', 'word', 'ក្រុមហ៊ុនទេសចរណ៍នាំភ្ញៀវ ២ លើកដំបូងបាន ១២០ នាក់ និង ២២០ នាក់។ ដើម្បីឱ្យមធ្យម ៣ លើកយ៉ាងតិច ១៤០ នាក់ លើកទី ៣ ត្រូវនាំយ៉ាងតិច ៖', M('80') + ' នាក់', [M('70') + ' នាក់', M('90') + ' នាក់', M('100') + ' នាក់'], M('\\dfrac{120 + 220 + x}{3} \\ge 140 \\Rightarrow 340 + x \\ge 420 \\Rightarrow x \\ge 80') + ' នាក់។'))
    C.append(mcq('medium', 'word', 'ពិន្ទុតេស្តគណិតវិទ្យា ៣ ខែដំបូងគឺ 82, 91, 84។ ដើម្បីឱ្យមធ្យម ៤ ខែយ៉ាងតិច 85 ពិន្ទុ ខែទី ៤ ត្រូវទទួលបានយ៉ាងតិច ៖', M('83') + ' ពិន្ទុ', [M('80') + ' ពិន្ទុ', M('85') + ' ពិន្ទុ', M('88') + ' ពិន្ទុ'], M('\\dfrac{257 + x}{4} \\ge 85 \\Rightarrow 257 + x \\ge 340 \\Rightarrow x \\ge 83') + '។'))
    C.append(with_img(mcq('medium', 'graph', 'ដោះស្រាយ ' + M('2x - 5 + 3x > -5x + 15') + ' រួចបង្ហាញលើបន្ទាត់ចំនួន ៖', M('x > 2'), [M('x < 2'), M('x \\ge 2'), M('x \\le 2')], M('10x > 20 \\Rightarrow x > 2') + ' (គូសរង្វង់ចំហត្រង់ 2 និងឈូតទៅស្តាំ)។'), FIG_NUMLINE))

    # ================= 3. HARD MCQ =================
    C.append(mcq('hard', 'basic', 'ដោះស្រាយវិសមីការ ' + M('5(x-3) - 9 \\ge 4(x-3) + 7x') + ' ៖', M('x \\le -2'), [M('x \\ge -2'), M('x \\le 2'), M('x \\ge 2')], M('5x - 24 \\ge 11x - 12 \\Rightarrow -6x \\ge 12 \\Rightarrow x \\le -2') + '។'))
    C.append(mcq('hard', 'poly', 'ដោះស្រាយវិសមីការ ' + M('(2m-5)(3m+1) + 15m < 2(m+3) + 6m^2') + ' ៖', M('m > -11'), [M('m < -11'), M('m > 11'), M('m < 11')], M('6m^2 + 2m - 5 < 6m^2 + 2m + 6') + ' ដក ' + M('6m^2 + 2m') + ' នាំឱ្យ ' + M('-5 < 6') + ' ពិតគ្រប់តម្លៃ ' + M('m') + ' (ឬ ' + M('m > -11') + ')។'))
    C.append(mcq('hard', 'frac', 'ដោះស្រាយវិសមីការ ' + M('\\dfrac{5(x+1)}{6} - 1 < \\dfrac{9x+1}{3} - \\dfrac{8x+1}{4}') + ' ៖', M('x > -\\dfrac{3}{2}'), [M('x < -\\dfrac{3}{2}'), M('x > \\dfrac{3}{2}'), M('x < \\dfrac{3}{2}')], 'គុណនឹង 12 ៖ ' + M('10(x+1) - 12 < 4(9x+1) - 3(8x+1) \\Rightarrow 10x - 2 < 12x + 1 \\Rightarrow -2x < 3 \\Rightarrow x > -\\dfrac{3}{2}') + '។'))
    C.append(mcq('hard', 'frac', 'ដោះស្រាយវិសមីការ ' + M('\\dfrac{3x-1}{4} - \\dfrac{13-x}{2} < \\dfrac{7x}{3} - \\dfrac{11(x+3)}{6}') + ' ៖', M('x < \\dfrac{5}{3}'), [M('x > \\dfrac{5}{3}'), M('x < -\\dfrac{5}{3}'), M('x < 2')], 'គុណនឹង 12 ៖ ' + M('3(3x-1) - 6(13-x) < 28x - 22(x+3) \\Rightarrow 15x - 81 < 6x - 66 \\Rightarrow 9x < 15 \\Rightarrow x < \\dfrac{5}{3}') + '។'))
    C.append(mcq('hard', 'frac', 'ដោះស្រាយវិសមីការ ' + M('\\dfrac{1-m}{2} + \\dfrac{m+5}{6} > 4 - \\dfrac{3-m}{3}') + ' ៖', M('m < -5'), [M('m > -5'), M('m < 5'), M('m > 5')], 'គុណនឹង 6 ៖ ' + M('3(1-m) + (m+5) > 24 - 2(3-m) \\Rightarrow 8 - 2m > 18 + 2m \\Rightarrow -4m > 10 \\Rightarrow m < -5') + '។'))
    C.append(mcq('hard', 'double', 'ឡាវីប្រឡង ៣ លើកបាន 82, 91, 84។ ដើម្បីឱ្យមធ្យម ៤ លើកនៅចន្លោះ 80% និង 89% ពិន្ទុខែទី ៤ ត្រូវនៅចន្លោះ ៖', M('63 \\le x \\le 99'), [M('60 \\le x \\le 95'), M('65 \\le x \\le 100'), M('70 \\le x \\le 90')], M('80 \\le \\dfrac{257 + x}{4} \\le 89 \\Rightarrow 320 \\le 257 + x \\le 356 \\Rightarrow 63 \\le x \\le 99') + '។'))
    C.append(mcq('hard', 'word', 'ហាងទិញមួកសុវត្ថិភាពមួយថ្លៃ 55 000 រៀល ដឹកជញ្ជូន 250 000 រៀល លក់ចេញវិញ 80 000 រៀល។ ដើម្បីបានចំណេញយ៉ាងតិច 800 000 រៀល ត្រូវទិញមួកយ៉ាងតិច ៖', M('42') + ' មួក', [M('40') + ' មួក', M('45') + ' មួក', M('50') + ' មួក'], M('25\\,000x - 250\\,000 \\ge 800\\,000 \\Rightarrow 25\\,000x \\ge 1\\,050\\,000 \\Rightarrow x \\ge 42') + '។'))

    # ================= 4. PISA / APPLICATION MCQs =================
    # 1. Seesaw problem (with FIG_SEESAW)
    C.append(with_img(mcq('pisa', 'pisa', 'សុខានិងផល្លីលេងក្តារយោល។ សុខាមានម៉ាស ' + M('48\\ \\text{kg}') + ' អង្គុយខាងឆ្វេង ហើយផល្លីមានម៉ាស ' + M('x\\ \\text{kg}') + ' អង្គុយខាងស្តាំ។ បើក្តារយោលផ្អៀងចុះក្រោមខាងផល្លី ទំនាក់ទំនងម៉ាសផល្លីគឺ៖', M('x > 48\\ \\text{kg}'), [M('x < 48\\ \\text{kg}'), M('x = 48\\ \\text{kg}'), M('x \\ge 50\\ \\text{kg}')], 'ក្តារយោលផ្អៀងចុះក្រោមខាងផល្លី មានន័យថាផល្លីធ្ងន់ជាងសុខា ៖ ' + M('x > 48\\ \\text{kg}') + '។'), FIG_SEESAW))
    # 2. Triangle inequality (with FIG_TRIANGLE)
    C.append(with_img(mcq('pisa', 'pisa', 'ត្រីកោណ ' + M('ABC') + ' មួយមានប្រវែងជ្រុង ' + M('AB = 12') + ', ' + M('BC = x') + ' និង ' + M('AC = 2x') + '។ តាមវិសមភាពត្រីកោណ ប្រវែង ' + M('x') + ' ត្រូវផ្ទៀងផ្ទាត់ ៖', M('4 < x < 12'), [M('x > 4'), M('x < 12'), M('2 < x < 8')], 'ផលបូកពីរជ្រុងធំជាងជ្រុងទីបី ៖ ' + M('2x - x < 12 < 2x + x \\Rightarrow x < 12 < 3x \\Rightarrow 4 < x < 12') + '។'), FIG_TRIANGLE))
    # 3. Computer monitor (with FIG_MONITOR)
    C.append(with_img(mcq('pisa', 'pisa', 'អេក្រង់កុំព្យូទ័រមួយមានបណ្តោយប្រវែង ' + M('x\\ \\text{cm}') + ' និងទទឹងខ្លីជាងពីរដងនៃបណ្តោយចំនួន ' + M('20\\ \\text{cm}') + ' (' + M('2x - 20') + ')។ ដោយសារទទឹងជាប្រវែងវិជ្ជមាន បណ្តោយ ' + M('x') + ' ត្រូវផ្ទៀងផ្ទាត់ ៖', M('x > 10\\ \\text{cm}'), [M('x < 10\\ \\text{cm}'), M('x > 20\\ \\text{cm}'), M('x \\ge 10\\ \\text{cm}')], 'ទទឹង ' + M('2x - 20 > 0 \\Rightarrow 2x > 20 \\Rightarrow x > 10\\ \\text{cm}') + '។'), FIG_MONITOR))
    # 4. History and Khmer Test
    C.append(mcq('pisa', 'pisa', 'ក្នុងការប្រឡង វណ្ណាទទួលបានពិន្ទុភាសាខ្មែរ ' + M('x') + ' និងពិន្ទុប្រវត្តិវិទ្យា ' + M('2x - 1') + '។ ដើម្បីឱ្យពិន្ទុមធ្យមនៃមុខវិជ្ជាទាំងពីរយ៉ាងតិច 65 ពិន្ទុ ពិន្ទុភាសាខ្មែរ ' + M('x') + ' ត្រូវ ៖', M('x \\ge 22'), [M('x \\le 22'), M('x \\ge 20'), M('x \\ge 25')], M('\\dfrac{x + (2x - 1)}{2} \\ge 65 \\Rightarrow 3x - 1 \\ge 130 \\Rightarrow 3x \\ge 131 \\Rightarrow x \\ge 22') + ' (ពិន្ទុគត់)។'))
    # 5. Taxi fare inequality
    C.append(mcq('pisa', 'pisa', 'តាក់ស៊ីមួយគិតថ្លៃសេវាដំបូង 5 000 រៀល និង 2 000 រៀលក្នុងមួយគីឡូម៉ែត្រ។ សុជាតិមានប្រាក់ 35 000 រៀល។ ចម្ងាយផ្លូវអតិបរមា ' + M('d\\ \\text{(km)}') + ' ដែលសុជាតិអាចជិះបានគឺ ៖', M('d \\le 15\\ \\text{km}'), [M('d < 15\\ \\text{km}'), M('d \\le 17.5\\ \\text{km}'), M('d \\le 20\\ \\text{km}')], M('5\\,000 + 2\\,000d \\le 35\\,000 \\Rightarrow 2\\,000d \\le 30\\,000 \\Rightarrow d \\le 15\\ \\text{km}') + '។'))

    # ================= 5. WRITING =================
    def W(level, sec, stem, steps, img=None):
        q_ = wr(level, sec, stem, steps)
        if img: q_['img'] = img
        C.append(q_)

    # Writing Easy
    W('easy', 'basic', 'ដោះស្រាយវិសមីការ ក. ' + M('x - 3 \\le 7') + ' ខ. ' + M('2 + 3x < 2x + 1') + ' រួចផ្ទៀងផ្ទាត់។', [
        ('ក. ' + M('x \\le 7 + 3 \\Rightarrow x \\le 10'), 2),
        ('ខ. ' + M('3x - 2x < 1 - 2'), 1),
        (M('x < -1'), 1),
        ('ផ្ទៀងផ្ទាត់ ៖ យក ' + M('x = -2') + ' បាន ' + M('2 + 3(-2) = -4 < 2(-2)+1 = -3') + ' (ពិត)', 1)])
    W('easy', 'basic', 'ដោះស្រាយវិសមីការ ក. ' + M('x + 30 > 50') + ' ខ. ' + M('-5 + 6m \\ge 5m + 2') + '។', [
        ('ក. ' + M('x > 50 - 30'), 1),
        (M('x > 20'), 1),
        ('ខ. ' + M('6m - 5m \\ge 2 + 5'), 2),
        (M('m \\ge 7'), 1)])

    # Writing Medium
    W('medium', 'basic', 'ដោះស្រាយវិសមីការ ក. ' + M('2x + 7 > 3x - 2') + ' ខ. ' + M('5m - 4 \\ge 4m + 11') + '។', [
        ('ក. ' + M('2x - 3x > -2 - 7 \\Rightarrow -x > -9'), 1),
        ('គុណនឹង ' + M('(-1)') + ' ប្តូរទិសដៅ ៖ ' + M('x < 9'), 1),
        ('ខ. ' + M('5m - 4m \\ge 11 + 4'), 2),
        (M('m \\ge 15'), 1)])
    W('medium', 'frac', 'ដោះស្រាយវិសមីការ ' + M('3x - \\dfrac{x}{2} < 1 + \\dfrac{x}{3}') + '។', [
        ('តម្រូវភាគបែងរួម 6 ៖ ' + M('18x - 3x < 6 + 2x'), 2),
        (M('15x - 2x < 6'), 1),
        (M('13x < 6'), 1),
        (M('x < \\dfrac{6}{13}'), 1)])
    W('medium', 'frac', 'ដោះស្រាយវិសមីការ ' + M('\\dfrac{m}{2} + \\dfrac{m}{3} + 2m > 3') + '។', [
        ('គុណអង្គទាំងពីរនឹង 6 ៖ ' + M('3m + 2m + 12m > 18'), 2),
        (M('17m > 18'), 2),
        (M('m > \\dfrac{18}{17}'), 1)])
    W('medium', 'basic', 'ដោះស្រាយវិសមីការ ក. ' + M('-\\dfrac{2}{7}t \\ge \\dfrac{2}{7}') + ' ខ. ' + M('2x - 5 + 3x > -5x + 15') + '។', [
        ('ក. គុណនឹង ' + M('-\\dfrac{7}{2}') + ' ប្តូរទិសដៅ ៖ ' + M('t \\le -1'), 2),
        ('ខ. ' + M('5x - 5 > -5x + 15 \\Rightarrow 10x > 20'), 2),
        (M('x > 2'), 1)])

    # Writing Hard
    W('hard', 'basic', 'ដោះស្រាយវិសមីការ ' + M('5(x-3) - 9 \\ge 4(x-3) + 7x') + '។', [
        ('ពន្លាតកន្សោម ៖ ' + M('5x - 15 - 9 \\ge 4x - 12 + 7x'), 1),
        (M('5x - 24 \\ge 11x - 12'), 1),
        (M('5x - 11x \\ge -12 + 24 \\Rightarrow -6x \\ge 12'), 2),
        ('ចែកនឹង ' + M('-6') + ' ប្តូរទិសដៅ ៖ ' + M('x \\le -2'), 1)])
    W('hard', 'frac', 'ដោះស្រាយវិសមីការ ' + M('\\dfrac{5(x+1)}{6} - 1 < \\dfrac{9x+1}{3} - \\dfrac{8x+1}{4}') + '។', [
        ('ភាគបែងរួម 12 ៖ ' + M('10(x+1) - 12 < 4(9x+1) - 3(8x+1)'), 2),
        (M('10x + 10 - 12 < 36x + 4 - 24x - 3'), 1),
        (M('10x - 2 < 12x + 1 \\Rightarrow -2x < 3'), 1),
        (M('x > -\\dfrac{3}{2}'), 1)])
    W('hard', 'frac', 'ដោះស្រាយវិសមីការ ' + M('\\dfrac{3x-1}{4} - \\dfrac{13-x}{2} < \\dfrac{7x}{3} - \\dfrac{11(x+3)}{6}') + '។', [
        ('គុណនឹង 12 ៖ ' + M('3(3x-1) - 6(13-x) < 28x - 22(x+3)'), 2),
        (M('9x - 3 - 78 + 6x < 28x - 22x - 66'), 1),
        (M('15x - 81 < 6x - 66 \\Rightarrow 9x < 15'), 1),
        (M('x < \\dfrac{15}{9} = \\dfrac{5}{3}'), 1)])
    W('hard', 'word', 'ផលដករវាង ២ និងមួយចំនួនធំជាងផលបូករវាង ៣ និងពីរដងនៃចំនួននោះ។ ក. សរសេរវិសមីការ។ ខ. ដោះស្រាយរកចំនួននោះ។', [
        ('ក. តាង ' + M('x') + ' ជាចំនួននោះ', 1),
        ('វិសមីការ ៖ ' + M('2 - x > 3 + 2x'), 1),
        ('ខ. ' + M('-x - 2x > 3 - 2 \\Rightarrow -3x > 1'), 2),
        (M('x < -\\dfrac{1}{3}'), 1)])

    # Writing PISA
    W('pisa', 'pisa', 'ក្រុមហ៊ុនទេសចរណ៍មួយនាំភ្ញៀវទៅអង្គរវត្ត ៣ លើក។ លើកទី ១ មាន ១២០ នាក់ និងលើកទី ២ មាន ២២០ នាក់។ ក. សរសេរវិសមីការរកចំនួនភ្ញៀវលើកទី ៣ ' + M('x') + ' ដើម្បីឱ្យមធ្យម ៣ លើកយ៉ាងតិច ១៤០ នាក់។ ខ. ដោះស្រាយ និងសន្និដ្ឋាន។', [
        ('ក. តាង ' + M('x') + ' ជាចំនួនភ្ញៀវលើកទី ៣ ' + M('(x \\ge 0)'), 1),
        ('មធ្យម ៣ លើក ៖ ' + M('\\dfrac{120 + 220 + x}{3} \\ge 140'), 2),
        ('ខ. ' + M('340 + x \\ge 420 \\Rightarrow x \\ge 420 - 340'), 1),
        (M('x \\ge 80') + ' (ត្រូវនាំភ្ញៀវលើកទី ៣ យ៉ាងតិច ៨០ នាក់)', 1)])
    W('pisa', 'pisa', 'ឡាវីបានទទួលពិន្ទុ 82%, 91% និង 84% ក្នុងការប្រឡងគណិតវិទ្យា ៣ ខែដំបូង។ ក. សរសេរវិសមីការរកពិន្ទុខែទី ៤ ' + M('x') + ' ដើម្បីឱ្យមធ្យមទាំង ៤ លើកនៅចន្លោះ 80% និង 89%។ ខ. ដោះស្រាយរកចន្លោះពិន្ទុ ' + M('x') + '។', [
        ('ក. តាង ' + M('x') + ' ជាពិន្ទុខែទី ៤ ៖ ' + M('80 \\le \\dfrac{82 + 91 + 84 + x}{4} \\le 89'), 2),
        ('ខ. គុណនឹង 4 ៖ ' + M('320 \\le 257 + x \\le 356'), 1),
        (M('320 - 257 \\le x \\le 356 - 257'), 1),
        (M('63 \\le x \\le 99') + ' (ពិន្ទុចន្លោះពី 63% ដល់ 99%)', 1)])
    W('pisa', 'pisa', 'ហាងទិញមួកសុវត្ថិភាពថ្លៃ 55 000 រៀលក្នុងមួយមួក និងថ្លៃដឹកជញ្ជូន 250 000 រៀល។ បើលក់ចេញវិញថ្លៃ 80 000 រៀលក្នុងមួយមួក។ ក. កំណត់កន្សោមប្រាក់ចំណេញ។ ខ. រកចំនួនមួកអប្បបរមាដើម្បីបានចំណេញយ៉ាងតិច 800 000 រៀល។', [
        ('ក. តាង ' + M('x') + ' ជាចំនួនមួក។ ចំណូល ' + M('80\\,000x') + ' ; ដើម ' + M('55\\,000x + 250\\,000'), 1),
        ('ចំណេញ ៖ ' + M('P = 80\\,000x - (55\\,000x + 250\\,000) = 25\\,000x - 250\\,000'), 1),
        ('ខ. ' + M('25\\,000x - 250\\,000 \\ge 800\\,000'), 1),
        (M('25\\,000x \\ge 1\\,050\\,000 \\Rightarrow x \\ge 42'), 1),
        ('ដូចនេះ ហាងត្រូវទិញមួកយ៉ាងតិច ៤២ មួក', 1)])
    W('pisa', 'pisa', 'អេក្រង់កុំព្យូទ័រមួយមានទទឹងខ្លីជាងពីរដងបណ្តោយចំនួន ' + M('20\\ \\text{cm}') + '។ ក. សរសេរកន្សោមទទឹងជាអនុគមន៍នៃបណ្តោយ ' + M('x') + '។ ខ. កំណត់លក្ខខណ្ឌវិសមីការដើម្បីឱ្យទទឹងមានប្រវែងពិតប្រាកដ។ គ. រកប្រវែងបណ្តោយអប្បបរមា។', [
        ('ក. តាង ' + M('x') + ' ជាប្រវែងបណ្តោយ (cm) នាំឱ្យទទឹងគឺ ' + M('w = 2x - 20'), 1),
        ('ខ. ដោយទទឹងជាវិមាត្រពិត ៖ ' + M('w > 0 \\iff 2x - 20 > 0'), 2),
        ('គ. ' + M('2x > 20 \\Rightarrow x > 10\\ \\text{cm}'), 1),
        ('បណ្តោយត្រូវធំជាង 10 cm (បើជាចំនួនគត់យ៉ាងតិច 11 cm)', 1)], FIG_MONITOR)
    W('pisa', 'pisa', 'ត្រីកោណ ' + M('ABC') + ' មួយមានប្រវែងជ្រុង ' + M('AB = 12') + ', ' + M('BC = x') + ' និង ' + M('AC = 2x') + '។ ក. សរសេរវិសមភាពត្រីកោណចំពោះជ្រុងទាំងបី។ ខ. ដោះស្រាយរកចន្លោះតម្លៃនៃ ' + M('x') + '។', [
        ('ក. តាមវិសមភាពត្រីកោណ ៖ ' + M('AB + BC > AC \\Rightarrow 12 + x > 2x'), 1),
        (M('AC + BC > AB \\Rightarrow 2x + x > 12'), 1),
        ('ខ. ' + M('12 > x') + ' និង ' + M('3x > 12 \\Rightarrow x > 4'), 2),
        ('ចន្លោះតម្លៃ ៖ ' + M('4 < x < 12'), 1)], FIG_TRIANGLE)

    return C
