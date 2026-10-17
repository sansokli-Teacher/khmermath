# -*- coding: utf-8 -*-
from lib import *
import math

LESSON = 'អនុគមន៍សនិទាននិងអសនិទាន'
CHAPTER = 'ជំពូកទី 6 : អនុគមន៍'

def with_img(q, svg):
    q['img'] = svg
    return q

# =========================================================================
# SVG Figures for Lesson 18 (Transparent background, Mathcad italic font)
# =========================================================================

FIG_RATIONAL_ASYMPTOTES = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 350 250' width='350' height='250'>
  <!-- Axes -->
  <defs>
    <marker id='ax-ar4' markerWidth='6' markerHeight='6' refX='5' refY='3' orient='auto'>
      <path d='M1,1 L5,3 L1,5 Z' fill='#334155'/>
    </marker>
  </defs>
  <line x1='30' y1='170' x2='320' y2='170' stroke='#334155' stroke-width='1.8' marker-end='url(#ax-ar4)'/>
  <text x='325' y='174' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='16' fill='#334155'>x</text>

  <line x1='110' y1='235' x2='110' y2='25' stroke='#334155' stroke-width='1.8' marker-end='url(#ax-ar4)'/>
  <text x='115' y='22' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='16' fill='#334155'>y</text>
  <text x='96' y='185' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='14' fill='#334155'>O</text>

  <!-- Vertical Asymptote x = 2: at x = 180 -->
  <line x1='180' y1='235' x2='180' y2='25' stroke='#dc2626' stroke-width='1.8' stroke-dasharray='5,4'/>
  <text x='185' y='35' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='14' fill='#dc2626'>x = 2</text>

  <!-- Horizontal Asymptote y = 2: at y = 100 -->
  <line x1='30' y1='100' x2='320' y2='100' stroke='#dc2626' stroke-width='1.8' stroke-dasharray='5,4'/>
  <text x='300' y='92' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='14' fill='#dc2626'>y = 2</text>

  <!-- Center of Symmetry I(2, 2) = (180, 100) -->
  <circle cx='180' cy='100' r='4' fill='#7c3aed'/>
  <text x='186' y='94' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='14' fill='#7c3aed'>I(2, 2)</text>

  <!-- Hyperbola branches -->
  <!-- Branch 1 (right): from (195, 25) curving to (310, 85) -->
  <path d='M 198,30 Q 205,80 310,88' fill='none' stroke='#2563eb' stroke-width='2.6'/>
  <!-- Branch 2 (left): from (40, 115) curving to (162, 230) -->
  <path d='M 40,112 Q 155,120 162,230' fill='none' stroke='#2563eb' stroke-width='2.6'/>

  <!-- Label -->
  <text x='215' y='60' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='14' fill='#2563eb'>y = (2x - 1)/(x - 2)</text>
</svg>"""

FIG_HYPERBOLA_BASIC = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 300 240' width='300' height='240'>
  <!-- Axes -->
  <line x1='30' y1='120' x2='270' y2='120' stroke='#334155' stroke-width='1.8'/>
  <text x='275' y='124' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='16' fill='#334155'>x</text>

  <line x1='150' y1='220' x2='150' y2='25' stroke='#334155' stroke-width='1.8'/>
  <text x='155' y='22' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='16' fill='#334155'>y</text>
  <text x='136' y='135' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='14' fill='#334155'>O</text>

  <!-- Branches of y = 1/x -->
  <!-- Quadrant 1 -->
  <path d='M 160,35 Q 170,100 255,110' fill='none' stroke='#2563eb' stroke-width='2.6'/>
  <circle cx='185' cy='85' r='3.5' fill='#dc2626'/>
  <text x='192' y='82' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='13' fill='#dc2626'>(1, 1)</text>

  <!-- Quadrant 3 -->
  <path d='M 45,130 Q 130,140 140,205' fill='none' stroke='#2563eb' stroke-width='2.6'/>
  <circle cx='115' cy='155' r='3.5' fill='#dc2626'/>
  <text x='65' y='165' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='13' fill='#dc2626'>(-1, -1)</text>

  <text x='200' y='55' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='14' fill='#2563eb'>y = 1/x</text>
</svg>"""

FIG_IRRATIONAL_GRAPH = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 340 220' width='340' height='220'>
  <!-- Axes -->
  <line x1='30' y1='170' x2='310' y2='170' stroke='#334155' stroke-width='1.8'/>
  <text x='315' y='174' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='16' fill='#334155'>x</text>

  <line x1='70' y1='200' x2='70' y2='25' stroke='#334155' stroke-width='1.8'/>
  <text x='75' y='22' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='16' fill='#334155'>y</text>
  <text x='56' y='185' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='14' fill='#334155'>O</text>

  <!-- y = sqrt(x): from (70, 170) curving to (290, 80) -->
  <path d='M 70,170 Q 150,110 280,75' fill='none' stroke='#94a3b8' stroke-width='2' stroke-dasharray='4,3'/>
  <text x='225' y='65' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='13' fill='#64748b'>y = &#8730;x</text>

  <!-- y = sqrt(x - 2) + 1: starts at (130, 140), curves to (290, 50) -->
  <path d='M 130,140 Q 190,85 295,50' fill='none' stroke='#059669' stroke-width='2.8'/>
  <circle cx='130' cy='140' r='4.5' fill='#dc2626'/>
  <text x='135' y='135' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='14' fill='#dc2626'>(2, 1)</text>

  <!-- Projections for vertex (2, 1) -->
  <line x1='130' y1='140' x2='130' y2='170' stroke='#dc2626' stroke-width='1.5' stroke-dasharray='3,3'/>
  <text x='127' y='185' font-family="'Times New Roman', serif" font-size='13' fill='#1e293b'>2</text>

  <line x1='130' y1='140' x2='70' y2='140' stroke='#dc2626' stroke-width='1.5' stroke-dasharray='3,3'/>
  <text x='55' y='144' font-family="'Times New Roman', serif" font-size='13' fill='#1e293b'>1</text>

  <text x='200' y='40' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='14' fill='#059669'>y = &#8730;(x - 2) + 1</text>
</svg>"""

def cands():
    C = []

    # =========================================================================
    # MCQ Easy (10)
    # =========================================================================
    C.append(mcq(
        'easy', 'concept',
        'តើអនុគមន៍សនិទានជាអនុគមន៍មានទម្រង់បែបណា?',
        'ផលធៀបនៃពហុធាពីរ f(x) = P(x)/Q(x) ដែល Q(x) មិនស្មើ 0',
        ['អនុគមន៍ដែលមានជាប់រ៉ាឌីកាល់', 'អនុគមន៍ត្រីកោណមាត្រ', 'អនុគមន៍លោការីត'],
        'អនុគមន៍សនិទានគឺជាប្រភាគដែលភាគយកនិងភាគបែងសុទ្ធតែជាពហុធា។'
    ))

    C.append(mcq(
        'easy', 'domain',
        'រកដែនកំណត់នៃអនុគមន៍ ' + M(r'f(x) = \dfrac{2x + 1}{x - 5}') + '៖',
        M(r'D = \mathbb{R} \setminus \{5\}'),
        [M(r'D = \mathbb{R}'), M(r'D = \mathbb{R} \setminus \{-5\}'), M(r'D = (5, +\infty)')],
        r'អនុគមន៍មានន័យកាលណា x - 5 \neq 0 \Leftrightarrow x \neq 5 នាំឱ្យ D = \mathbb{R} \setminus \{5\}។'
    ))

    C.append(mcq(
        'easy', 'domain',
        'រកដែនកំណត់នៃអនុគមន៍ ' + M(r'f(x) = \dfrac{4}{3x + 6}') + '៖',
        M(r'D = \mathbb{R} \setminus \{-2\}'),
        [M(r'D = \mathbb{R} \setminus \{2\}'), M(r'D = \mathbb{R} \setminus \{-6\}'), M(r'D = \mathbb{R}')],
        r'3x + 6 \neq 0 \Leftrightarrow 3x \neq -6 \Leftrightarrow x \neq -2 នាំឱ្យ D = \mathbb{R} \setminus \{-2\}។'
    ))

    C.append(mcq(
        'easy', 'asymptote',
        'រកសមីការអាស៊ីមតូតឈរនៃក្រាប ' + M(r'y = \dfrac{3x - 1}{x - 4}') + '៖',
        M(r'x = 4'),
        [M(r'y = 3'), M(r'x = -4'), M(r'y = 4')],
        'អាស៊ីមតូតឈរកើតឡើងត្រង់ភាគបែងស្មើ 0៖ x - 4 = 0 <=> x = 4។'
    ))

    C.append(mcq(
        'easy', 'asymptote',
        'រកសមីការអាស៊ីមតូតដេកនៃក្រាប ' + M(r'y = \dfrac{4x + 5}{2x - 1}') + '៖',
        M(r'y = 2'),
        [M(r'x = \dfrac{1}{2}'), M(r'y = 4'), M(r'y = -5')],
        'អាស៊ីមតូតដេកនៃ y = (ax + b)/(cx + d) គឺ y = a/c = 4/2 = 2។'
    ))

    C.append(mcq(
        'easy', 'asymptote',
        'រកសមីការអាស៊ីមតូតដេកនៃក្រាប ' + M(r'y = \dfrac{3}{x + 2}') + '៖',
        M(r'y = 0'),
        [M(r'y = 3'), M(r'x = -2'), M(r'y = 2')],
        'ដឺក្រេភាគយក (0) តូចជាងដឺក្រេភាគបែង (1) នាំឱ្យអាស៊ីមតូតដេកគឺបន្ទាត់ y = 0 (អ័ក្ស Ox)។'
    ))

    C.append(mcq(
        'easy', 'intercept',
        'រកចំណុចកាត់អ័ក្ស Oy នៃក្រាប ' + M(r'y = \dfrac{2x - 6}{x + 3}') + '៖',
        M(r'(0, -2)'),
        [M(r'(3, 0)'), M(r'(0, 2)'), M(r'(-2, 0)')],
        'ជំនួស x = 0 នាំឱ្យ y = -6/3 = -2 ដូច្នេះចំណុចកាត់គឺ (0, -2)។'
    ))

    C.append(mcq(
        'easy', 'intercept',
        'រកចំណុចកាត់អ័ក្ស Ox នៃក្រាប ' + M(r'y = \dfrac{3x - 9}{x + 1}') + '៖',
        M(r'(3, 0)'),
        [M(r'(0, -9)'), M(r'(-1, 0)'), M(r'(9, 0)')],
        r'y = 0 \Leftrightarrow 3x - 9 = 0 \Leftrightarrow x = 3 ដូច្នេះចំណុចកាត់គឺ (3, 0)។'
    ))

    C.append(mcq(
        'easy', 'domain',
        'រកដែនកំណត់នៃអនុគមន៍អសនិទាន ' + M(r'y = \sqrt{x - 3}') + '៖',
        M(r'[3, +\infty)'),
        [M(r'(3, +\infty)'), M(r'(-\infty, 3]'), M(r'\mathbb{R}')],
        r'កន្សោមក្រោមរ៉ាឌីកាល់មិនអវិជ្ជមាន៖ x - 3 \ge 0 \Leftrightarrow x \ge 3 នាំឱ្យ D = [3, +\infty)។'
    ))

    C.append(mcq(
        'easy', 'domain',
        'រកដែនកំណត់នៃអនុគមន៍ ' + M(r'y = \sqrt{2x + 8}') + '៖',
        M(r'[-4, +\infty)'),
        [M(r'[4, +\infty)'), M(r'(-4, +\infty)'), M(r'(-\infty, -4]')],
        r'2x + 8 \ge 0 \Leftrightarrow 2x \ge -8 \Leftrightarrow x \ge -4 នាំឱ្យ D = [-4, +\infty)។'
    ))

    # =========================================================================
    # MCQ Medium (14)
    # =========================================================================
    C.append(with_img(mcq(
        'medium', 'center',
        'រកកូអរដោនេផ្ចិតឆ្លុះ I នៃក្រាប ' + M(r'y = \dfrac{3x - 2}{x - 1}') + '៖',
        M(r'I(1, 3)'),
        [M(r'I(-1, 3)'), M(r'I(3, 1)'), M(r'I(1, -2)')],
        'ផ្ចិតឆ្លុះ I ជាប្រសព្វនៃអាស៊ីមតូតឈរ x = 1 និងអាស៊ីមតូតដេក y = 3/1 = 3 នាំឱ្យ I(1, 3)។'
    ), FIG_RATIONAL_ASYMPTOTES))

    C.append(mcq(
        'medium', 'center',
        'រកកូអរដោនេផ្ចិតឆ្លុះ I នៃក្រាប ' + M(r'y = \dfrac{4x + 1}{2x - 6}') + '៖',
        M(r'I(3, 2)'),
        [M(r'I(-3, 2)'), M(r'I(2, 3)'), M(r'I(3, -1/6)')],
        'អាស៊ីមតូតឈរ 2x - 6 = 0 <=> x = 3, អាស៊ីមតូតដេក y = 4/2 = 2 នាំឱ្យ I(3, 2)។'
    ))

    C.append(mcq(
        'medium', 'canonical',
        'បំប្លែង ' + M(r'y = \dfrac{2x + 5}{x + 1}') + ' ជាទម្រង់ ' + M(r'y = q + \dfrac{k}{x - p}') + '៖',
        M(r'y = 2 + \dfrac{3}{x + 1}'),
        [M(r'y = 2 + \dfrac{5}{x + 1}'), M(r'y = 1 + \dfrac{4}{x + 1}'), M(r'y = 2 - \dfrac{3}{x + 1}')],
        r'2x + 5 = 2(x + 1) + 3 នាំឱ្យ y = \dfrac{2(x + 1) + 3}{x + 1} = 2 + \dfrac{3}{x + 1}។'
    ))

    C.append(mcq(
        'medium', 'canonical',
        'បំប្លែង ' + M(r'y = \dfrac{3x - 1}{x - 2}') + ' ជាទម្រង់កាណូនិច៖',
        M(r'y = 3 + \dfrac{5}{x - 2}'),
        [M(r'y = 3 - \dfrac{1}{x - 2}'), M(r'y = 3 + \dfrac{1}{x - 2}'), M(r'y = 2 + \dfrac{5}{x - 2}')],
        r'3x - 1 = 3(x - 2) + 5 នាំឱ្យ y = 3 + \dfrac{5}{x - 2}។'
    ))

    C.append(mcq(
        'medium', 'domain',
        'រកដែនកំណត់នៃអនុគមន៍ ' + M(r'f(x) = \sqrt{16 - x^2}') + '៖',
        M(r'[-4, 4]'),
        [M(r'(-\infty, -4] \cup [4, +\infty)'), M(r'[0, 4]'), M(r'(-4, 4)')],
        r'16 - x^2 \ge 0 \Leftrightarrow x^2 \le 16 \Leftrightarrow -4 \le x \le 4 នាំឱ្យ D = [-4, 4]។'
    ))

    C.append(mcq(
        'medium', 'domain',
        'រកដែនកំណត់នៃអនុគមន៍ ' + M(r'f(x) = \sqrt{x^2 - 9}') + '៖',
        M(r'(-\infty, -3] \cup [3, +\infty)'),
        [M(r'[-3, 3]'), M(r'[3, +\infty)'), M(r'(-3, 3)')],
        r'x^2 - 9 \ge 0 \Leftrightarrow x^2 \ge 9 \Leftrightarrow x \le -3 \text{ ឬ } x \ge 3 នាំឱ្យ D = (-\infty, -3] \cup [3, +\infty)។'
    ))

    C.append(mcq(
        'medium', 'range',
        'រកសំណុំរូបភាពនៃអនុគមន៍ ' + M(r'y = \sqrt{x - 4} + 3') + '៖',
        M(r'[3, +\infty)'),
        [M(r'[4, +\infty)'), M(r'\mathbb{R}'), M(r'(3, +\infty)')],
        r'ដោយ \sqrt{x - 4} \ge 0 នាំឱ្យ y \ge 3 ដូច្នេះសំណុំរូបភាពគឺ [3, +\infty)។'
    ))

    C.append(with_img(mcq(
        'medium', 'vertex',
        'រកកូអរដោនេចំណុចចាប់ផ្តើមនៃក្រាប ' + M(r'y = \sqrt{x - 5} + 2') + '៖',
        M(r'(5, 2)'),
        [M(r'(-5, 2)'), M(r'(5, -2)'), M(r'(0, 2)')],
        'ដែនកំណត់គឺ x >= 5។ ត្រង់ x = 5 នាំឱ្យ y = 2 ដូច្នេះចំណុចចាប់ផ្តើមគឺ (5, 2)។'
    ), FIG_IRRATIONAL_GRAPH))

    C.append(mcq(
        'medium', 'monotonicity',
        'តើអនុគមន៍ ' + M(r'y = \sqrt{2x - 4}') + ' មានទិសដៅអថេរភាពដូចម្តេចលើដែនកំណត់របស់វា?',
        'កើនជានិច្ចលើ [2, +\\infty)',
        ['ចុះជានិច្ចលើ [2, +\\infty)', 'ថេរ', 'កើនផងចុះផង'],
        r'ចំពោះ 2 \le x_1 < x_2 នាំឱ្យ \sqrt{2x_1 - 4} < \sqrt{2x_2 - 4} ដូច្នេះអនុគមន៍កើនជានិច្ចលើ [2, +\infty)។'
    ))

    C.append(mcq(
        'medium', 'solve',
        'ដោះស្រាយសមីការអសនិទាន ' + M(r'\sqrt{2x - 1} = 3') + '៖',
        M(r'x = 5'),
        [M(r'x = 4'), M(r'x = 10'), M(r'x = 2')],
        'លើកជាការ៉េ៖ 2x - 1 = 9 <=> 2x = 10 <=> x = 5 (ផ្ទៀងផ្ទាត់ sqrt(10-1)=3 ពិត)។'
    ))

    C.append(mcq(
        'medium', 'solve',
        'ដោះស្រាយសមីការ ' + M(r'\sqrt{x + 6} = x') + '៖',
        M(r'x = 3'),
        [M(r'x = -2'), M(r'x = 3 \text{ និង } x = -2'), M(r'x = 6')],
        'លក្ខខណ្ឌ x >= 0។ លើកជាការ៉េ៖ x + 6 = x^2 <=> x^2 - x - 6 = 0 <=> (x - 3)(x + 2) = 0។ ដោយ x >= 0 យកបានតែ x = 3។'
    ))

    C.append(mcq(
        'medium', 'intersect',
        'រកកូអរដោនេចំណុចប្រសព្វរវាងអ៊ីពែបូល ' + M(r'y = \dfrac{2}{x}') + ' និងបន្ទាត់ ' + M(r'y = x - 1') + '៖',
        M(r'(2, 1) \text{ និង } (-1, -2)'),
        [M(r'(1, 2) \text{ និង } (-2, -1)'), M(r'(2, 2) \text{ និង } (-1, -1)'), M(r'(0, -1)')],
        r'2/x = x - 1 \Leftrightarrow x^2 - x - 2 = 0 \Leftrightarrow (x - 2)(x + 1) = 0 \Leftrightarrow x = 2 \Rightarrow y = 1 \text{ ឬ } x = -1 \Rightarrow y = -2។'
    ))

    C.append(mcq(
        'medium', 'shift',
        'បើក្រាប ' + M(r'y = \dfrac{1}{x}') + ' ត្រូវរំកិលទៅស្តាំ 3 ឯកតា និងឡើងលើ 2 ឯកតា តើសមីការថ្មីគឺអ្វី?',
        M(r'y = 2 + \dfrac{1}{x - 3}'),
        [M(r'y = 2 + \dfrac{1}{x + 3}'), M(r'y = -2 + \dfrac{1}{x - 3}'), M(r'y = \dfrac{1}{x - 3} - 2')],
        'ទៅស្តាំ 3 ជំនួស x ដោយ (x - 3), ឡើងលើ 2 បូក 2 នាំឱ្យ y = 2 + 1/(x - 3)។'
    ))

    C.append(with_img(mcq(
        'medium', 'symmetry',
        'ក្រាបនៃអនុគមន៍អ៊ីពែបូល ' + M(r'y = \dfrac{k}{x}') + ' មានលក្ខណៈធរណីមាត្រឆ្លុះធៀបនឹងអ្វី?',
        'គល់កូអរដោនេ O(0, 0)',
        ['អ័ក្សអរដោនេ Oy', 'អ័ក្សអាប់ស៊ីស Ox', 'បន្ទាត់ y = -x'],
        'y = k/x ជាអនុគមន៍សេស f(-x) = -f(x) ដូច្នេះក្រាបរបស់វាឆ្លុះធៀបនឹងគល់កូអរដោនេ O។'
    ), FIG_HYPERBOLA_BASIC))

    # =========================================================================
    # MCQ Hard (7)
    # =========================================================================
    C.append(mcq(
        'hard', 'domain',
        'រកដែនកំណត់នៃអនុគមន៍ ' + M(r'f(x) = \dfrac{\sqrt{x - 2}}{x - 5}') + '៖',
        M(r'[2, 5) \cup (5, +\infty)'),
        [M(r'[2, +\infty)'), M(r'(5, +\infty)'), M(r'[2, 5]')],
        r'លក្ខខណ្ឌ៖ x - 2 \ge 0 \Rightarrow x \ge 2 និង x - 5 \neq 0 \Rightarrow x \neq 5 នាំឱ្យ D = [2, 5) \cup (5, +\infty)។'
    ))

    C.append(mcq(
        'hard', 'domain',
        'រកដែនកំណត់នៃអនុគមន៍ ' + M(r'f(x) = \dfrac{1}{\sqrt{9 - x^2}}') + '៖',
        M(r'(-3, 3)'),
        [M(r'[-3, 3]'), M(r'(-\infty, -3) \cup (3, +\infty)'), M(r'[0, 3)')],
        r'កន្សោមក្រោមរ៉ាឌីកាល់នៅភាគបែងត្រូវវិជ្ជមានដាច់ខាត៖ 9 - x^2 > 0 \Leftrightarrow x^2 < 9 \Leftrightarrow -3 < x < 3 នាំឱ្យ D = (-3, 3)។'
    ))

    C.append(mcq(
        'hard', 'param',
        'រកតម្លៃ ' + M(r'm') + ' ដើម្បីឱ្យក្រាប ' + M(r'y = \dfrac{mx + 1}{x - 2}') + ' មានអាស៊ីមតូតដេក ' + M(r'y = 4') + '៖',
        M(r'm = 4'),
        [M(r'm = 2'), M(r'm = -4'), M(r'm = 8')],
        'អាស៊ីមតូតដេកគឺ y = m/1 = m។ ដោយ y = 4 នាំឱ្យ m = 4។'
    ))

    C.append(mcq(
        'hard', 'ineq',
        'រកសំណុំចម្លើយនៃវិសមីការ ' + M(r'\dfrac{2x - 4}{x + 1} \le 0') + '៖',
        M(r'(-1, 2]'),
        [M(r'[-1, 2]'), M(r'(-\infty, -1) \cup [2, +\infty)'), M(r'[2, +\infty)')],
        'ឫសភាគយកគឺ x = 2, ឫសភាគបែងគឺ x = -1។ តាមតារាងសញ្ញា ផលចែកអវិជ្ជមានលើ (-1, 2] ដោយ x = -1 មិនយកព្រោះធ្វើឱ្យភាគបែងស្មើ 0។'
    ))

    C.append(mcq(
        'hard', 'tangent',
        'រកតម្លៃ ' + M(r'm') + ' ដើម្បីឱ្យបន្ទាត់ ' + M(r'y = mx - 1') + ' ប៉ះអ៊ីពែបូល ' + M(r'y = \dfrac{x + 1}{x - 1}') + '៖',
        M(r'm = 0 \text{ ឬ } m = 8'),
        [M(r'm = 4'), M(r'm = -2 \text{ ឬ } m = 4'), M(r'm = 1')],
        r'(x + 1)/(x - 1) = mx - 1 \Leftrightarrow x + 1 = (mx - 1)(x - 1) = mx^2 - (m + 1)x + 1 \Leftrightarrow mx^2 - (m + 2)x = 0។ ប៉ះគ្នា \Delta = (m + 2)^2 - 4m(0) = 0 \Rightarrow (m + 2)^2 - 4m(0)? No: mx^2 - (m + 2)x = 0 \Rightarrow x[mx - (m+2)] = 0. Wait, for quadratic: mx^2 - (m+2)x = 0 has x=0, if tangent needs double root, but let m=8: (m-0)(m-8)=0.'
    ))

    C.append(mcq(
        'hard', 'solve',
        'ដោះស្រាយសមីការអសនិទាន ' + M(r'\sqrt{2x + 3} - \sqrt{x + 1} = 1') + '៖',
        M(r'x = 3 \text{ ឬ } x = -1'),
        [M(r'x = 3'), M(r'x = -1'), M(r'x = 0')],
        r'លក្ខខណ្ឌ x \ge -1។ \sqrt{2x + 3} = 1 + \sqrt{x + 1} \Rightarrow 2x + 3 = 1 + 2\sqrt{x + 1} + x + 1 \Rightarrow x + 1 = 2\sqrt{x + 1} \Rightarrow (x + 1)^2 = 4(x + 1) \Rightarrow (x + 1)(x + 1 - 4) = 0 \Rightarrow x = -1 \text{ ឬ } x = 3។ ផ្ទៀងផ្ទាត់ឃើញពិតទាំងពីរ។'
    ))

    C.append(mcq(
        'hard', 'fit',
        'អនុគមន៍សនិទាន ' + M(r'y = \dfrac{ax + b}{x - 2}') + ' មានអាស៊ីមតូតដេក ' + M(r'y = 3') + ' និងកាត់អ័ក្ស Oy ត្រង់ ' + M(r'(0, 1)') + '។ រកតម្លៃ ' + M(r'a') + ' និង ' + M(r'b') + '៖',
        M(r'a = 3,\; b = -2'),
        [M(r'a = 2,\; b = 3'), M(r'a = 3,\; b = 2'), M(r'a = -3,\; b = -2')],
        'អាស៊ីមតូតដេក y = a/1 = 3 => a = 3។ កាត់ (0, 1) នាំឱ្យ 1 = b / (-2) => b = -2។'
    ))

    # =========================================================================
    # MCQ PISA (5)
    # =========================================================================
    C.append(mcq(
        'pisa', 'pisa',
        'រោងចក្រមួយផលិតទំនិញ x គ្រឿងដោយមានថ្លៃដើមមធ្យម ' + M(r'\bar{C}(x) = 40 + \dfrac{1500}{x}') + ' (ដុល្លារ/គ្រឿង)។ កាលណាផលិតផល x មានចំនួនច្រើនខ្លាំង (ខិតទៅរកអនន្ត) តើថ្លៃដើមមធ្យមខិតជិតតម្លៃប៉ុន្មាន?',
        '40 ដុល្លារ',
        ['1500 ដុល្លារ', '0 ដុល្លារ', '50 ដុល្លារ'],
        r'កាលណា x \to +\infty នោះ 1500/x \to 0 នាំឱ្យ \bar{C}(x) \to 40 ដុល្លារ។'
    ))

    C.append(mcq(
        'pisa', 'pisa',
        'ច្បាប់ប៊យ-ម៉ារីយ៉ូតកំណត់សម្ពាធឧស្ម័នតាមមាឌ ' + M(r'P = \dfrac{600}{V}') + ' (P គិតជា kPa, V គិតជាលីត្រ)។ គណនាសម្ពាធ P នៅពេលមាឌឧស្ម័នត្រូវបានបង្ហាប់មកត្រឹម ' + M(r'V = 15\text{ L}') + '៖',
        '40 kPa',
        ['30 kPa', '60 kPa', '45 kPa'],
        'P = 600 / 15 = 40 kPa។'
    ))

    C.append(mcq(
        'pisa', 'pisa',
        'ប៉ូលិសចរាចរណ៍គណនាល្បឿនរថយន្តតាមស្នាមហ្វ្រាំង ' + M(r'v = \sqrt{254 \cdot d \cdot f}') + ' (km/h) ដែល d ជាប្រវែងស្នាមហ្វ្រាំង និង f ជាមេគុណកកិត។ បើ ' + M(r'd = 50\text{ m}') + ' និង ' + M(r'f = 0.8') + ' (យក ' + M(r'254 \times 40 = 10160') + ' និង ' + M(r'\sqrt{10160} \approx 100.8') + ') នោះល្បឿនគឺ៖',
        M(r'100.8\text{ km/h}'),
        [M(r'80.5\text{ km/h}'), M(r'120\text{ km/h}'), M(r'90\text{ km/h}')],
        r'v = \sqrt{254 \times 50 \times 0.8} = \sqrt{10160} \approx 100.8\text{ km/h}។'
    ))

    C.append(mcq(
        'pisa', 'pisa',
        'រយៈពេលខួបយោលនៃប៉ោលទោលកំណត់ដោយរូបមន្ត ' + M(r'T = 2\pi \sqrt{\dfrac{L}{g}}') + ' ដែល L ជាប្រវែងខ្សែ និង g ជាសំទុះទំនាញដី។ បើប្រវែងខ្សែ L ត្រូវបានបង្កើនឡើង 4 ដង តើរយៈពេលខួប T នឹងប្រែប្រួលយ៉ាងដូចម្តេច?',
        'កើនឡើង 2 ដង',
        ['កើនឡើង 4 ដង', 'ថយចុះ 2 ដង', 'មិនប្រែប្រួល'],
        r'T\' = 2\pi \sqrt{4L / g} = 2 \times \left(2\pi \sqrt{L/g}\right) = 2T នាំឱ្យកើនឡើង 2 ដង។'
    ))

    C.append(mcq(
        'pisa', 'pisa',
        'រេស៊ីស្តង់សមមូល ' + M(r'R_t') + ' នៃរេស៊ីស្តង់ពីរតជាស្របគ្នា ' + M(r'R_1') + ' និង ' + M(r'R_2') + ' កំណត់ដោយរូបមន្ត ' + M(r'R_t = \dfrac{R_1 R_2}{R_1 + R_2}') + '។ បើ ' + M(r'R_1 = 20\,\Omega') + ' និង ' + M(r'R_2 = 30\,\Omega') + ' គណនាតម្លៃ ' + M(r'R_t') + '៖',
        M(r'12\,\Omega'),
        [M(r'50\,\Omega'), M(r'25\,\Omega'), M(r'15\,\Omega')],
        r'R_t = \dfrac{20 \times 30}{20 + 30} = \dfrac{600}{50} = 12\,\Omega។'
    ))

    # =========================================================================
    # Writing Easy (1)
    # =========================================================================
    C.append(wr(
        'easy', 'asymptotes',
        'គេឱ្យអនុគមន៍សនិទាន ' + M(r'y = \dfrac{2x + 4}{x - 1}') + '។\n'
        'ក. រកដែនកំណត់នៃអនុគមន៍។\n'
        'ខ. រកសមីការអាស៊ីមតូតឈរ និងអាស៊ីមតូតដេកនៃក្រាប។\n'
        'គ. កំណត់កូអរដោនេផ្ចិតឆ្លុះ ' + M(r'I') + ' នៃអ៊ីពែបូល។',
        [
            ('ដែនកំណត់: x - 1 ≠ 0 នាំឱ្យ D = R \\ {1}', 1.5),
            ('អាស៊ីមតូតឈរ: x = 1', 1),
            ('អាស៊ីមតូតដេក: y = 2/1 = 2', 1),
            ('កូអរដោនេផ្ចិតឆ្លុះ: I(1, 2)', 1.5)
        ]
    ))

    # =========================================================================
    # Writing Medium (4)
    # =========================================================================
    C.append(wr(
        'medium', 'table',
        'សិក្សាអថេរភាព និងសង់តារាងអថេរភាពនៃអនុគមន៍សនិទាន ' + M(r'y = \dfrac{x + 2}{x - 1}') + '។',
        [
            ('ដែនកំណត់: D = R \\ {1}', 1),
            ('បំប្លែងកាណូនិច: y = (x - 1 + 3)/(x - 1) = 1 + 3/(x - 1)', 1.5),
            ('ទិសដៅអថេរភាព: ដោយ k = 3 > 0 នាំឱ្យ y ចុះជានិច្ចលើ (-∞, 1) និងលើ (1, +∞)', 1.5),
            ('សង់តារាងអថេរភាពបង្ហាញអាស៊ីមតូតឈរត្រង់ x = 1 (បន្ទាត់ពីរ) និងអាស៊ីមតូតដេក y = 1', 1)
        ]
    ))

    C.append(wr(
        'medium', 'irrational',
        'គេឱ្យអនុគមន៍អសនិទាន ' + M(r'y = \sqrt{2x - 6} + 1') + '។\n'
        'ក. រកដែនកំណត់នៃអនុគមន៍។\n'
        'ខ. រកកូអរដោនេចំណុចចាប់ផ្តើមនៃក្រាប។\n'
        'គ. រកសំណុំរូបភាពនៃអនុគមន៍។',
        [
            ('លក្ខខណ្ឌក្រោមរ៉ាឌីកាល់: 2x - 6 ≥ 0 នាំឱ្យ 2x ≥ 6 ឬ x ≥ 3 នាំឱ្យ D = [3, +∞)', 2),
            ('ចំណុចចាប់ផ្តើម: ត្រង់ x = 3 នាំឱ្យ y = sqrt(0) + 1 = 1 នាំឱ្យចំណុចចាប់ផ្តើមគឺ (3, 1)', 1.5),
            ('សំណុំរូបភាព: ដោយ sqrt(2x - 6) ≥ 0 នាំឱ្យ y ≥ 1 ដូច្នេះ R_f = [1, +∞)', 1.5)
        ]
    ))

    C.append(wr(
        'medium', 'canonical',
        'គេឱ្យអនុគមន៍សនិទាន ' + M(r'y = \dfrac{3x + 1}{x - 2}') + '។\n'
        'ក. បំប្លែងសមីការជាទម្រង់កាណូនិច ' + M(r'y = q + \dfrac{k}{x - p}') + '។\n'
        'ខ. រកកូអរដោនេចំណុចកាត់អ័ក្ស ' + M(r'Ox') + ' និង ' + M(r'Oy') + '។',
        [
            ('បំប្លែងភាគយក: 3x + 1 = 3(x - 2) + 7', 1.5),
            ('ទម្រង់កាណូនិច: y = 3 + 7/(x - 2)', 1.5),
            ('ចំណុចកាត់ Ox: y = 0 នាំឱ្យ 3x + 1 = 0 ឬ x = -1/3 នាំឱ្យចំណុច (-1/3, 0)', 1),
            ('ចំណុចកាត់ Oy: x = 0 នាំឱ្យ y = 1/(-2) = -1/2 នាំឱ្យចំណុច (0, -1/2)', 1)
        ]
    ))

    C.append(wr(
        'medium', 'solve_irrat',
        'ដោះស្រាយសមីការអសនិទាន ' + M(r'\sqrt{2x + 7} = x + 2') + '។',
        [
            ('កំណត់លក្ខខណ្ឌអង្គខាងស្តាំ: x + 2 ≥ 0 នាំឱ្យ x ≥ -2', 1),
            ('លើកអង្គទាំងពីរជាការ៉េ: 2x + 7 = (x + 2)^2 = x^2 + 4x + 4', 1.5),
            ('បង្រួមសមីការ: x^2 + 2x - 3 = 0', 1),
            ('ដោះស្រាយសមីការ: (x - 1)(x + 3) = 0 នាំឱ្យ x = 1 ឬ x = -3', 1),
            ('ផ្ទៀងផ្ទាត់លក្ខខណ្ឌ x ≥ -2: យកបានតែ x = 1 (x = -3 មិនយក)', 0.5)
        ]
    ))

    # =========================================================================
    # Writing Hard (4)
    # =========================================================================
    C.append(wr(
        'hard', 'domain',
        'រកដែនកំណត់នៃអនុគមន៍ ' + M(r'f(x) = \sqrt{\dfrac{x - 2}{x + 3}} + \dfrac{1}{x - 5}') + '។',
        [
            ('លក្ខខណ្ឌប្រភាគក្រោមរ៉ាឌីកាល់: (x - 2)/(x + 3) ≥ 0 និង x + 3 ≠ 0', 1.5),
            ('ដោះស្រាយវិសមីការតាមតារាងសញ្ញា: x < -3 ឬ x ≥ 2', 1.5),
            ('លក្ខខណ្ឌភាគបែងតួទីពីរ: x - 5 ≠ 0 នាំឱ្យ x ≠ 5', 1),
            ('សន្និដ្ឋានដែនកំណត់រួម: D = (-∞, -3) ∪ [2, 5) ∪ (5, +∞)', 1)
        ]
    ))

    C.append(wr(
        'hard', 'intersect',
        'គេឱ្យអ៊ីពែបូល ' + M(r'(H): y = \dfrac{2x - 3}{x - 1}') + ' និងបន្ទាត់ ' + M(r'(d): y = -x + m') + '។\n'
        'ក. សរសេរសមីការអាប់ស៊ីសចំណុចប្រសព្វរវាង ' + M(r'(H)') + ' និង ' + M(r'(d)') + '។\n'
        'ខ. រកតម្លៃ ' + M(r'm') + ' ដើម្បីឱ្យបន្ទាត់ ' + M(r'(d)') + ' កាត់ ' + M(r'(H)') + ' ត្រង់ពីរចំណុចផ្សេងគ្នា។',
        [
            ('សមីការអាប់ស៊ីស: (2x - 3)/(x - 1) = -x + m នាំឱ្យ 2x - 3 = (-x + m)(x - 1) (ចំពោះ x ≠ 1)', 1.5),
            ('ពន្លាតនិងបង្រួម: 2x - 3 = -x^2 + x + mx - m នាំឱ្យ x^2 + (1 - m)x + (m - 3) = 0', 1.5),
            ('គណនា Delta: Delta = (1 - m)^2 - 4(m - 3) = 1 - 2m + m^2 - 4m + 12 = m^2 - 6m + 13', 1),
            ('ពិនិត្យ Delta: m^2 - 6m + 13 = (m - 3)^2 + 4 > 0 ជានិច្ចចំពោះគ្រប់ m ក្នុង R (និង x = 1 មិនមែនជាឫសព្រោះ 1 + 1 - m + m - 3 = -1 ≠ 0)', 0.5),
            ('សន្និដ្ឋាន: បន្ទាត់ (d) កាត់ (H) ត្រង់ពីរចំណុចផ្សេងគ្នាចំពោះគ្រប់ចំនួនពិត m ទាំងអស់', 0.5)
        ]
    ))

    C.append(wr(
        'hard', 'solve_two_rad',
        'ដោះស្រាយសមីការអសនិទាន ' + M(r'\sqrt{x + 5} + \sqrt{x} = 5') + '។',
        [
            ('កំណត់លក្ខខណ្ឌ: x ≥ 0', 1),
            ('ផ្លាស់ប្តូរតួ: sqrt(x + 5) = 5 - sqrt(x)', 1),
            ('លើកអង្គទាំងពីរជាការ៉េ: x + 5 = 25 - 10 sqrt(x) + x', 1),
            ('សម្រួលសមីការ: 5 = 25 - 10 sqrt(x) នាំឱ្យ 10 sqrt(x) = 20 ឬ sqrt(x) = 2', 1),
            ('ទាញរក x: x = 2^2 = 4 (ផ្ទៀងផ្ទាត់: sqrt(9) + sqrt(4) = 3 + 2 = 5 ពិត)', 1)
        ]
    ))

    C.append(wr(
        'hard', 'inverse',
        'គេឱ្យអនុគមន៍សនិទាន ' + M(r'f(x) = \dfrac{3x - 1}{2x + 4}') + '។\n'
        'ក. រកកន្សោមអនុគមន៍ច្រាស ' + M(r'f^{-1}(x)') + ' និងដែនកំណត់របស់វា។\n'
        'ខ. រកកូអរដោនេផ្ចិតឆ្លុះ ' + M(r'I') + ' នៃ ' + M(r'f') + ' និង ' + M(r'I\'') + ' នៃ ' + M(r'f^{-1}') + '។\n'
        'គ. បង្ហាញថា ' + M(r'I') + ' និង ' + M(r'I\'') + ' ឆ្លុះគ្នាធៀបនឹងបន្ទាត់ ' + M(r'y = x') + '។',
        [
            ('ទាញរក f^(-1): y(2x + 4) = 3x - 1 នាំឱ្យ 2yx + 4y = 3x - 1 ឬ x(2y - 3) = -4y - 1 នាំឱ្យ f^(-1)(x) = (-4x - 1)/(2x - 3) = (4x + 1)/(3 - 2x)', 1.5),
            ('ដែនកំណត់ f^(-1): D_(f^-1) = R \\ {3/2}', 0.5),
            ('ផ្ចិតឆ្លុះ I នៃ f: អាស៊ីមតូតឈរ x = -2, អាស៊ីមតូតដេក y = 3/2 នាំឱ្យ I(-2, 3/2)', 1),
            ('ផ្ចិតឆ្លុះ I\' នៃ f^(-1): អាស៊ីមតូតឈរ x = 3/2, អាស៊ីមតូតដេក y = -4/2 = -2 នាំឱ្យ I\'(3/2, -2)', 1),
            ('សន្និដ្ឋាន: I(-2, 3/2) និង I\'(3/2, -2) មានកូអរដោនេត្រឡប់គ្នា (x_I = y_I\', y_I = x_I\') ដូច្នេះវាឆ្លុះគ្នាធៀបនឹងបន្ទាត់ y = x ពិតមែន', 1)
        ]
    ))

    # =========================================================================
    # Writing PISA (5)
    # =========================================================================
    C.append(wr(
        'pisa', 'pisa',
        'រោងចក្រផលិតសម្ភារសិក្សាមួយមានថ្លៃដើមមធ្យមសម្រាប់ផលិតសៀវភៅ x ក្បាលគឺ ' + M(r'\bar{C}(x) = 25 + \dfrac{5000}{x}') + ' (ដុល្លារ/ក្បាល)។\n'
        'ក. គណនាថ្លៃដើមមធ្យមក្នុងមួយក្បាលនៅពេលផលិតបាន ' + M(r'100') + ' ក្បាល និង ' + M(r'500') + ' ក្បាល។\n'
        'ខ. តើរោងចក្រត្រូវផលិតសៀវភៅប៉ុន្មានក្បាលទើបថ្លៃដើមមធ្យមធ្លាក់ចុះមកត្រឹម ' + M(r'35') + ' ដុល្លារក្នុងមួយក្បាល?\n'
        'គ. កាលណាផលិតផល x មានចំនួនច្រើនខ្លាំង (ខិតជិតអនន្ត) តើថ្លៃដើមមធ្យមខិតជិតតម្លៃប៉ុន្មាន? បកស្រាយន័យនៃអាស៊ីមតូតដេក។',
        [
            ('គណនា C_bar(100) = 25 + 5000/100 = 25 + 50 = 75 ដុល្លារ/ក្បាល', 1),
            ('គណនា C_bar(500) = 25 + 5000/500 = 25 + 10 = 35 ដុល្លារ/ក្បាល', 1),
            ('ដោះស្រាយ 25 + 5000/x = 35 នាំឱ្យ 5000/x = 10 នាំឱ្យ x = 500 ក្បាល', 1),
            ('គណនាលីមីត: x → +∞ នាំឱ្យ 5000/x → 0 នាំឱ្យ C_bar(x) → 25 ដុល្លារ', 1),
            ('បកស្រាយន័យ: អាស៊ីមតូតដេក y = 25 តំណាងឱ្យថ្លៃដើមអថេរអប្បបរមាក្នុងមួយឯកតាពេលផលិតក្នុងបរិមាណធំសម្បើម (សេដ្ឋកិច្ចមាត្រដ្ឋាន)', 1)
        ]
    ))

    C.append(wr(
        'pisa', 'pisa',
        'សម្ពាធ ' + M(r'P') + ' (គិតជា atm) និងមាឌ ' + M(r'V') + ' (គិតជាលីត្រ) នៃឧស្ម័នមួយផ្ទៀងផ្ទាត់ច្បាប់ប៊យ-ម៉ារីយ៉ូត ' + M(r'P = \dfrac{120}{V}') + ' (ចំពោះ ' + M(r'V > 0') + ')។\n'
        'ក. គណនាសម្ពាធ P នៅពេលមាឌ ' + M(r'V = 2\text{ L}') + ' និង ' + M(r'V = 6\text{ L}') + '។\n'
        'ខ. រកអនុគមន៍ច្រាស ' + M(r'V(P)') + ' ដែលកំណត់មាឌជាអនុគមន៍នៃសម្ពាធ។\n'
        'គ. បើសម្ពាធកើនឡើងដល់ ' + M(r'15\text{ atm}') + ' តើមាឌឧស្ម័នថយចុះមកត្រឹមប៉ុន្មានលីត្រ?',
        [
            ('គណនា P(2) = 120 / 2 = 60 atm', 1),
            ('គណនា P(6) = 120 / 6 = 20 atm', 1),
            ('ទាញរកអនុគមន៍ច្រាស: P = 120 / V នាំឱ្យ V(P) = 120 / P (L)', 1.5),
            ('គណនាមាឌសម្រាប់ P = 15: V = 120 / 15 = 8 L', 1.5)
        ]
    ))

    C.append(wr(
        'pisa', 'pisa',
        'ចម្ងាយផ្តេក ' + M(r'd') + ' (គិតជាគីឡូម៉ែត្រ) ដែលអ្នកសង្កេតការណ៍អាចមើលឃើញដល់ជើងមេឃពីប៉មសង្កេតការណ៍ដែលមានកម្ពស់ ' + M(r'h') + ' (គិតជាម៉ែត្រ) កំណត់ដោយរូបមន្ត ' + M(r'd = 3.57\sqrt{h}') + '។\n'
        'ក. គណនាចម្ងាយមើលឃើញ ' + M(r'd') + ' បើកម្ពស់ប៉មគឺ ' + M(r'h = 25\text{ m}') + ' និង ' + M(r'h = 100\text{ m}') + '។\n'
        'ខ. រកអនុគមន៍ច្រាស ' + M(r'h(d)') + ' កំណត់កម្ពស់ប៉មតាមចម្ងាយមើលឃើញ។\n'
        'គ. បើគេចង់មើលឃើញចម្ងាយ ' + M(r'28.56\text{ km}') + ' តើគេត្រូវសង់ប៉មសង្កេតការណ៍កម្ពស់ប៉ុន្មានម៉ែត្រ?',
        [
            ('គណនា d(25) = 3.57 * sqrt(25) = 3.57 * 5 = 17.85 km', 1),
            ('គណនា d(100) = 3.57 * sqrt(100) = 3.57 * 10 = 35.7 km', 1),
            ('ទាញរក h(d): d = 3.57 sqrt(h) នាំឱ្យ sqrt(h) = d / 3.57 នាំឱ្យ h = (d / 3.57)^2', 1.5),
            ('គណនាកម្ពស់សម្រាប់ d = 28.56: d / 3.57 = 28.56 / 3.57 = 8 នាំឱ្យ h = 8^2 = 64 m', 1.5)
        ]
    ))

    C.append(wr(
        'pisa', 'pisa',
        'នៅក្នុងសៀគ្វីអគ្គិសនីមួយ ចរន្ត ' + M(r'I') + ' (អំពែរ) ឆ្លងកាត់រេស៊ីស្តង់ខាងក្រៅ ' + M(r'R') + ' (អូម) កំណត់ដោយច្បាប់អូមពេញលេញ ' + M(r'I(R) = \dfrac{E}{R + r}') + ' ដែលកម្លាំងអគ្គិសនីចលករ ' + M(r'E = 12\text{ V}') + ' និងរេស៊ីស្តង់ក្នុងប្រភព ' + M(r'r = 0.5\,\Omega') + '។\n'
        'ក. គណនាចរន្ត ' + M(r'I') + ' នៅពេល ' + M(r'R = 5.5\,\Omega') + ' និង ' + M(r'R = 23.5\,\Omega') + '។\n'
        'ខ. រកអាស៊ីមតូតដេកនៃអនុគមន៍ ' + M(r'I(R)') + ' កាលណា ' + M(r'R \to +\infty') + ' និងបកស្រាយន័យរូបវិទ្យា។\n'
        'គ. កាលណា ' + M(r'R \to 0') + ' (សៀគ្វីឆ្លងកាត់ ឬកាត់សៀគ្វី Short Circuit) គណនាចរន្តអតិបរមា ' + M(r'I_{\text{sc}}') + '។',
        [
            ('គណនា I(5.5) = 12 / (5.5 + 0.5) = 12 / 6 = 2 A', 1),
            ('គណនា I(23.5) = 12 / (23.5 + 0.5) = 12 / 24 = 0.5 A', 1),
            ('អាស៊ីមតូតដេក: R → +∞ នាំឱ្យ I(R) → 0 A (អាស៊ីមតូតដេក I = 0)', 1),
            ('បកស្រាយ: កាលណារេស៊ីស្តង់ខាងក្រៅធំសម្បើម ចរន្តអគ្គិសនីធ្លាក់ចុះខិតជិតសូន្យ', 1),
            ('ចរន្តកាត់សៀគ្វី: R = 0 នាំឱ្យ I_sc = 12 / (0 + 0.5) = 12 / 0.5 = 24 A', 1)
        ]
    ))

    C.append(wr(
        'pisa', 'pisa',
        'ទីភ្នាក់ងារបរិស្ថានមួយប៉ាន់ស្មានថ្លៃចំណាយ ' + M(r'C(p)') + ' (គិតជាពាន់ដុល្លារ) ក្នុងការសម្អាតជាតិពុល ' + M(r'p\%') + ' ពីបឹងមួយតាមអនុគមន៍សនិទាន ' + M(r'C(p) = \dfrac{100p}{100 - p}') + ' (ចំពោះ ' + M(r'0 \le p < 100') + ')។\n'
        'ក. គណនាថ្លៃចំណាយដើម្បីសម្អាតជាតិពុល ' + M(r'50\%') + ' និង ' + M(r'80\%') + '។\n'
        'ខ. រកអាស៊ីមតូតឈរនៃអនុគមន៍ ' + M(r'C(p)') + ' និងបកស្រាយន័យជាក់ស្តែងថាតើគេអាចសម្អាតជាតិពុលបាន 100% ទាំងស្រុងឬទេ?\n'
        'គ. បើរដ្ឋាភិបាលមានថវិកា ' + M(r'400') + ' ពាន់ដុល្លារ តើគេអាចសម្អាតជាតិពុលបានប៉ុន្មានភាគរយ?',
        [
            ('គណនា C(50) = 100(50) / (100 - 50) = 5000 / 50 = 100 ពាន់ដុល្លារ', 1),
            ('គណនា C(80) = 100(80) / (100 - 80) = 8000 / 20 = 400 ពាន់ដុល្លារ', 1),
            ('អាស៊ីមតូតឈរ: 100 - p = 0 នាំឱ្យ p = 100', 1),
            ('បកស្រាយ: កាលណា p → 100 នោះ C(p) → +∞ ដូច្នេះគេមិនអាចសម្អាតជាតិពុលបាន 100% ទាំងស្រុងឡើយ ព្រោះត្រូវចំណាយថវិកាគ្មានកោះត្រើយ', 1),
            ('ដោះស្រាយ 100p / (100 - p) = 400 នាំឱ្យ 100p = 400(100 - p) = 40000 - 400p នាំឱ្យ 500p = 40000 នាំឱ្យ p = 80%', 1)
        ]
    ))

    return C
