# -*- coding: utf-8 -*-
from lib import *
import math

LESSON = 'អនុគមន៍និងក្រាបអនុគមន៍'
CHAPTER = 'ជំពូកទី 6 : អនុគមន៍'

def with_img(q, svg):
    q['img'] = svg
    return q

# =========================================================================
# SVG Figures for Lesson 16 (Transparent background, Mathcad italic font)
# =========================================================================

FIG_ARROW_MAP = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 360 220' width='360' height='220'>
  <!-- Set A -->
  <ellipse cx='80' cy='110' rx='55' ry='90' fill='#eff6ff' stroke='#2563eb' stroke-width='2.5'/>
  <text x='80' y='35' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='18' font-weight='bold' fill='#1d4ed8' text-anchor='middle'>A</text>
  
  <!-- Set B -->
  <ellipse cx='280' cy='110' rx='55' ry='90' fill='#fef2f2' stroke='#dc2626' stroke-width='2.5'/>
  <text x='280' y='35' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='18' font-weight='bold' fill='#dc2626' text-anchor='middle'>B</text>

  <!-- Elements of A -->
  <circle cx='80' cy='60' r='3.5' fill='#1e293b'/>
  <text x='62' y='65' font-family="'Times New Roman', serif" font-size='15' fill='#1e293b'>1</text>
  
  <circle cx='80' cy='95' r='3.5' fill='#1e293b'/>
  <text x='62' y='100' font-family="'Times New Roman', serif" font-size='15' fill='#1e293b'>2</text>
  
  <circle cx='80' cy='130' r='3.5' fill='#1e293b'/>
  <text x='62' y='135' font-family="'Times New Roman', serif" font-size='15' fill='#1e293b'>3</text>
  
  <circle cx='80' cy='165' r='3.5' fill='#1e293b'/>
  <text x='62' y='170' font-family="'Times New Roman', serif" font-size='15' fill='#1e293b'>4</text>

  <!-- Elements of B -->
  <circle cx='280' cy='60' r='3.5' fill='#1e293b'/>
  <text x='298' y='65' font-family="'Times New Roman', serif" font-size='15' fill='#1e293b'>1</text>
  
  <circle cx='280' cy='95' r='3.5' fill='#1e293b'/>
  <text x='298' y='100' font-family="'Times New Roman', serif" font-size='15' fill='#1e293b'>4</text>
  
  <circle cx='280' cy='130' r='3.5' fill='#1e293b'/>
  <text x='298' y='135' font-family="'Times New Roman', serif" font-size='15' fill='#1e293b'>9</text>
  
  <circle cx='280' cy='165' r='3.5' fill='#1e293b'/>
  <text x='298' y='170' font-family="'Times New Roman', serif" font-size='15' fill='#1e293b'>16</text>

  <!-- Arrows -->
  <defs>
    <marker id='arr' markerWidth='8' markerHeight='8' refX='6' refY='4' orient='auto'>
      <path d='M1,1 L7,4 L1,7 Z' fill='#2563eb'/>
    </marker>
  </defs>
  <line x1='88' y1='60' x2='272' y2='60' stroke='#2563eb' stroke-width='2' marker-end='url(#arr)'/>
  <line x1='88' y1='95' x2='272' y2='95' stroke='#2563eb' stroke-width='2' marker-end='url(#arr)'/>
  <line x1='88' y1='130' x2='272' y2='130' stroke='#2563eb' stroke-width='2' marker-end='url(#arr)'/>
  <line x1='88' y1='165' x2='272' y2='165' stroke='#2563eb' stroke-width='2' marker-end='url(#arr)'/>

  <!-- Function label -->
  <text x='180' y='50' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='16' fill='#1e293b' text-anchor='middle'>f(x) = x&#178;</text>
</svg>"""

FIG_PARABOLA_INTERCEPTS = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 340 240' width='340' height='240'>
  <!-- Axes -->
  <defs>
    <marker id='ax-arr' markerWidth='6' markerHeight='6' refX='5' refY='3' orient='auto'>
      <path d='M1,1 L5,3 L1,5 Z' fill='#334155'/>
    </marker>
  </defs>
  <line x1='30' y1='170' x2='310' y2='170' stroke='#334155' stroke-width='1.8' marker-end='url(#ax-arr)'/>
  <text x='315' y='174' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='16' fill='#334155'>x</text>
  
  <line x1='170' y1='220' x2='170' y2='25' stroke='#334155' stroke-width='1.8' marker-end='url(#ax-arr)'/>
  <text x='175' y='22' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='16' fill='#334155'>y</text>
  <text x='156' y='185' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='14' fill='#334155'>O</text>

  <!-- Parabola y = x^2 - 4: Scale: 1 unit = 25px. Origin at (170, 70)? No, vertex at (170, 210) (y=-4), x-intercepts at -2 (120, 170) and +2 (220, 170) -->
  <path d='M 105,45 Q 170,235 235,45' fill='none' stroke='#2563eb' stroke-width='2.8'/>

  <!-- Key points -->
  <circle cx='170' cy='210' r='4' fill='#dc2626'/>
  <text x='178' y='215' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='13' fill='#dc2626'>(0, -4)</text>

  <circle cx='120' cy='170' r='4' fill='#dc2626'/>
  <text x='85' y='163' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='13' fill='#dc2626'>(-2, 0)</text>

  <circle cx='220' cy='170' r='4' fill='#dc2626'/>
  <text x='225' y='163' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='13' fill='#dc2626'>(2, 0)</text>

  <!-- Curve equation -->
  <text x='240' y='75' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='15' fill='#2563eb'>y = x&#178; - 4</text>
</svg>"""

FIG_INVERSE_REFLECT = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 320 240' width='320' height='240'>
  <!-- Axes -->
  <defs>
    <marker id='ax-ar2' markerWidth='6' markerHeight='6' refX='5' refY='3' orient='auto'>
      <path d='M1,1 L5,3 L1,5 Z' fill='#475569'/>
    </marker>
  </defs>
  <line x1='30' y1='170' x2='290' y2='170' stroke='#475569' stroke-width='1.8' marker-end='url(#ax-ar2)'/>
  <text x='295' y='174' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='16' fill='#475569'>x</text>

  <line x1='120' y1='220' x2='120' y2='25' stroke='#475569' stroke-width='1.8' marker-end='url(#ax-ar2)'/>
  <text x='125' y='22' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='16' fill='#475569'>y</text>
  <text x='106' y='185' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='14' fill='#475569'>O</text>

  <!-- Line of symmetry y = x: passes through (120, 170) and (210, 80) -->
  <line x1='50' y1='240' x2='250' y2='40' stroke='#94a3b8' stroke-width='1.8' stroke-dasharray='5,4'/>
  <text x='245' y='35' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='14' fill='#64748b'>y = x</text>

  <!-- f(x) = 2x - 1: passes through (120, 195) and (165, 125) and (190, 75) -->
  <line x1='90' y1='235' x2='205' y2='45' stroke='#2563eb' stroke-width='2.6'/>
  <text x='210' y='60' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='14' fill='#2563eb'>f(x) = 2x - 1</text>

  <!-- f^(-1)(x) = (x + 1)/2: passes through (120, 145) and (165, 125) and (230, 95) -->
  <line x1='55' y1='205' x2='265' y2='100' stroke='#dc2626' stroke-width='2.6'/>
  <text x='195' y='130' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='14' fill='#dc2626'>f &#8315;&#185;(x)</text>

  <!-- Intersection point (1, 1) = (165, 125) -->
  <circle cx='165' cy='125' r='4' fill='#1e293b'/>
  <text x='140' y='115' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='13' fill='#1e293b'>(1, 1)</text>
</svg>"""

def cands():
    C = []

    # =========================================================================
    # MCQ Easy (10)
    # =========================================================================
    C.append(mcq(
        'easy', 'concept',
        'តើលក្ខខណ្ឌណាបញ្ជាក់ថាទំនាក់ទំនងពីសំណុំ ' + M(r'A') + ' ទៅសំណុំ ' + M(r'B') + ' ជាអនុគមន៍?',
        'ធាតុនីមួយៗនៃ A ត្រូវផ្គូផ្គងនឹងធាតុតែមួយគត់នៃ B',
        ['ធាតុមួយនៃ A អាចផ្គូផ្គងនឹងធាតុច្រើននៃ B', 'គ្រប់ធាតុនៃ B ត្រូវតែមានរូបភាព', 'ធាតុទាំងអស់នៃ A ត្រូវផ្គូផ្គងនឹងធាតុដូចគ្នាតែមួយ'],
        'តាមនិយមន័យ អនុគមន៍ពី A ទៅ B គឺជាក្បួនដែលភ្ជាប់ធាតុនីមួយៗ x នៃ A ទៅនឹងធាតុតែមួយគត់ y នៃ B។'
    ))

    C.append(with_img(mcq(
        'easy', 'concept',
        'តាមដ្យាក្រាមព្រួញខាងក្រោម តើកន្សោមតំណាងឱ្យអនុគមន៍ ' + M(r'f') + ' ពីសំណុំ ' + M(r'A') + ' ទៅសំណុំ ' + M(r'B') + ' គឺជាអ្វី?',
        M(r'f(x) = x^2'),
        [M(r'f(x) = 2x'), M(r'f(x) = x + 3'), M(r'f(x) = 2^x')],
        'ធាតុ 1 ទៅ 1, 2 ទៅ 4, 3 ទៅ 9, 4 ទៅ 16 ត្រូវនឹងរូបមន្ត f(x) = x^2។'
    ), FIG_ARROW_MAP))

    C.append(mcq(
        'easy', 'eval',
        'គេឱ្យអនុគមន៍ ' + M(r'f(x) = 4x - 7') + '។ គណនាតម្លៃនៃ ' + M(r'f(3)') + '៖',
        M(r'5'),
        [M(r'12'), M(r'-7'), M(r'9')],
        'f(3) = 4(3) - 7 = 12 - 7 = 5។'
    ))

    C.append(mcq(
        'easy', 'eval',
        'គេឱ្យអនុគមន៍ ' + M(r'f(x) = 2x^2 + 5x - 3') + '។ គណនា ' + M(r'f(-1)') + '៖',
        M(r'-6'),
        [M(r'4'), M(r'0'), M(r'-10')],
        'f(-1) = 2(-1)^2 + 5(-1) - 3 = 2(1) - 5 - 3 = -6។'
    ))

    C.append(mcq(
        'easy', 'domain',
        'តើដែនកំណត់នៃអនុគមន៍ពហុធា ' + M(r'P(x) = 3x^2 - 2x + 1') + ' គឺជាអ្វី?',
        M(r'D = \mathbb{R}'),
        [M(r'D = \mathbb{R} \setminus \{0\}'), M(r'D = [0, +\infty)'), M(r'D = \mathbb{R}^*')],
        'អនុគមន៍ពហុធាកំណត់បានចំពោះគ្រប់ x ជាចំនួនពិត ដូច្នេះ D = R។'
    ))

    C.append(mcq(
        'easy', 'domain',
        'រកដែនកំណត់នៃអនុគមន៍ ' + M(r'f(x) = \dfrac{5}{x - 4}') + '៖',
        M(r'D = \mathbb{R} \setminus \{4\}'),
        [M(r'D = \mathbb{R}'), M(r'D = \mathbb{R} \setminus \{-4\}'), M(r'D = (4, +\infty)')],
        r'អនុគមន៍មានន័យកាលណាភាគបែងខុសពីសូន្យ៖ x - 4 \neq 0 \Leftrightarrow x \neq 4។'
    ))

    C.append(mcq(
        'easy', 'domain',
        'រកដែនកំណត់នៃអនុគមន៍ប្រភាគ ' + M(r'f(x) = \dfrac{x + 2}{2x - 6}') + '៖',
        M(r'D = \mathbb{R} \setminus \{3\}'),
        [M(r'D = \mathbb{R} \setminus \{-2\}'), M(r'D = \mathbb{R}'), M(r'D = (3, +\infty)')],
        r'2x - 6 \neq 0 \Leftrightarrow 2x \neq 6 \Leftrightarrow x \neq 3 នាំឱ្យ D = \mathbb{R} \setminus \{3\}។'
    ))

    C.append(mcq(
        'easy', 'intercept',
        'រកកូអរដោនេចំណុចកាត់អ័ក្សអរដោនេ ' + M(r'(Oy)') + ' នៃក្រាប ' + M(r'y = 3x^2 - 4x + 6') + '៖',
        M(r'(0, 6)'),
        [M(r'(6, 0)'), M(r'(0, -4)'), M(r'(0, 3)')],
        'ជំនួស x = 0 នាំឱ្យ y = 3(0)^2 - 4(0) + 6 = 6។ ចំណុចកាត់គឺ (0, 6)។'
    ))

    C.append(mcq(
        'easy', 'intercept',
        'រកកូអរដោនេចំណុចកាត់អ័ក្សអាប់ស៊ីស ' + M(r'(Ox)') + ' នៃបន្ទាត់ ' + M(r'y = 2x - 8') + '៖',
        M(r'(4, 0)'),
        [M(r'(0, -8)'), M(r'(-4, 0)'), M(r'(8, 0)')],
        r'កាត់អ័ក្ស Ox កាលណា y = 0 \Leftrightarrow 2x - 8 = 0 \Leftrightarrow x = 4។'
    ))

    C.append(mcq(
        'easy', 'symmetry',
        'ក្រាបនៃអនុគមន៍គូមានលក្ខណៈធរណីមាត្រឆ្លុះធៀបនឹងអ្វី?',
        'អ័ក្សអរដោនេ (Oy)',
        ['គល់កូអរដោនេ O', 'អ័ក្សអាប់ស៊ីស (Ox)', 'បន្ទាត់ y = x'],
        'អនុគមន៍គូផ្ទៀងផ្ទាត់ f(-x) = f(x) នាំឱ្យក្រាបរបស់វាឆ្លុះធៀបនឹងអ័ក្សឈរ Oy។'
    ))

    # =========================================================================
    # MCQ Medium (14)
    # =========================================================================
    C.append(mcq(
        'medium', 'domain',
        'រកដែនកំណត់នៃអនុគមន៍ ' + M(r'f(x) = \sqrt{3x - 12}') + '៖',
        M(r'D = [4, +\infty)'),
        [M(r'D = (4, +\infty)'), M(r'D = [12, +\infty)'), M(r'D = (-\infty, 4]')],
        r'3x - 12 \ge 0 \Leftrightarrow 3x \ge 12 \Leftrightarrow x \ge 4 នាំឱ្យ D = [4, +\infty)។'
    ))

    C.append(mcq(
        'medium', 'domain',
        'រកដែនកំណត់នៃអនុគមន៍ ' + M(r'f(x) = \sqrt{25 - x^2}') + '៖',
        M(r'[-5, 5]'),
        [M(r'(-\infty, -5] \cup [5, +\infty)'), M(r'[0, 5]'), M(r'(-5, 5)')],
        r'25 - x^2 \ge 0 \Leftrightarrow x^2 \le 25 \Leftrightarrow -5 \le x \le 5 នាំឱ្យ D = [-5, 5]។'
    ))

    C.append(mcq(
        'medium', 'range',
        'រកសំណុំរូបភាព ' + M(r'R_f') + ' នៃអនុគមន៍ ' + M(r'f(x) = x^2 + 5') + ' ចំពោះ ' + M(r'x \in \mathbb{R}') + '៖',
        M(r'[5, +\infty)'),
        [M(r'\mathbb{R}'), M(r'[0, +\infty)'), M(r'(5, +\infty)')],
        r'ដោយ x^2 \ge 0 ចំពោះគ្រប់ x នាំឱ្យ x^2 + 5 \ge 5 ដូច្នេះ R_f = [5, +\infty)។'
    ))

    C.append(mcq(
        'medium', 'range',
        'រកសំណុំរូបភាព ' + M(r'R_f') + ' នៃអនុគមន៍ ' + M(r'f(x) = -x^2 + 4') + ' ចំពោះ ' + M(r'x \in \mathbb{R}') + '៖',
        M(r'(-\infty, 4]'),
        [M(r'[4, +\infty)'), M(r'(-\infty, 0]'), M(r'\mathbb{R}')],
        r'ដោយ -x^2 \le 0 នាំឱ្យ -x^2 + 4 \le 4 ដូច្នេះ R_f = (-\infty, 4]។'
    ))

    C.append(mcq(
        'medium', 'compose',
        'គេឱ្យ ' + M(r'f(x) = 3x + 2') + ' និង ' + M(r'g(x) = x^2 - 1') + '។ រកកន្សោម ' + M(r'(f \circ g)(x)') + '៖',
        M(r'3x^2 - 1'),
        [M(r'3x^2 + 2'), M(r'9x^2 + 12x + 3'), M(r'3x^2 + 1')],
        r'(f \circ g)(x) = f(g(x)) = 3(x^2 - 1) + 2 = 3x^2 - 3 + 2 = 3x^2 - 1។'
    ))

    C.append(mcq(
        'medium', 'compose',
        'គេឱ្យ ' + M(r'f(x) = 2x') + ' និង ' + M(r'g(x) = x + 5') + '។ រកកន្សោម ' + M(r'(g \circ f)(x)') + '៖',
        M(r'2x + 5'),
        [M(r'2x + 10'), M(r'x + 10'), M(r'2x^2 + 5')],
        r'(g \circ f)(x) = g(f(x)) = g(2x) = 2x + 5។'
    ))

    C.append(mcq(
        'medium', 'compose',
        'គេឱ្យ ' + M(r'f(x) = x^2 + 1') + ' និង ' + M(r'g(x) = 2x - 3') + '។ គណនាតម្លៃនៃ ' + M(r'(f \circ g)(2)') + '៖',
        M(r'2'),
        [M(r'5'), M(r'1'), M(r'10')],
        r'g(2) = 2(2) - 3 = 1 នាំឱ្យ (f \circ g)(2) = f(1) = 1^2 + 1 = 2។'
    ))

    C.append(mcq(
        'medium', 'inverse',
        'រកអនុគមន៍ច្រាស ' + M(r'f^{-1}(x)') + ' នៃ ' + M(r'f(x) = 2x + 6') + '៖',
        M(r'f^{-1}(x) = \dfrac{x - 6}{2}'),
        [M(r'f^{-1}(x) = \dfrac{x + 6}{2}'), M(r'f^{-1}(x) = 2x - 6'), M(r'f^{-1}(x) = \dfrac{2}{x - 6}')],
        r'y = 2x + 6 \Leftrightarrow 2x = y - 6 \Leftrightarrow x = \dfrac{y - 6}{2} នាំឱ្យ f^{-1}(x) = \dfrac{x - 6}{2}។'
    ))

    C.append(mcq(
        'medium', 'inverse',
        'រកអនុគមន៍ច្រាស ' + M(r'f^{-1}(x)') + ' នៃ ' + M(r'f(x) = \dfrac{x - 3}{4}') + '៖',
        M(r'f^{-1}(x) = 4x + 3'),
        [M(r'f^{-1}(x) = 4x - 3'), M(r'f^{-1}(x) = \dfrac{x + 3}{4}'), M(r'f^{-1}(x) = \dfrac{4}{x - 3}')],
        r'y = \dfrac{x - 3}{4} \Leftrightarrow x - 3 = 4y \Leftrightarrow x = 4y + 3 នាំឱ្យ f^{-1}(x) = 4x + 3។'
    ))

    C.append(mcq(
        'medium', 'parity',
        'តើអនុគមន៍ ' + M(r'f(x) = x^5 - 3x^3 + 2x') + ' ជាប្រភេទអនុគមន៍អ្វី?',
        'អនុគមន៍សេស (Odd function)',
        ['អនុគមន៍គូ (Even function)', 'មិនគូមិនសេស', 'អនុគមន៍ថេរ'],
        'f(-x) = (-x)^5 - 3(-x)^3 + 2(-x) = -x^5 + 3x^3 - 2x = -f(x) នាំឱ្យ f ជាអនុគមន៍សេស។'
    ))

    C.append(mcq(
        'medium', 'parity',
        'តើអនុគមន៍ ' + M(r'f(x) = 2x^4 - 7x^2 + 1') + ' ជាប្រភេទអនុគមន៍អ្វី?',
        'អនុគមន៍គូ (Even function)',
        ['អនុគមន៍សេស (Odd function)', 'មិនគូមិនសេស', 'អនុគមន៍លីនេអ៊ែរ'],
        'f(-x) = 2(-x)^4 - 7(-x)^2 + 1 = 2x^4 - 7x^2 + 1 = f(x) នាំឱ្យ f ជាអនុគមន៍គូ។'
    ))

    C.append(mcq(
        'medium', 'parity',
        'តើអនុគមន៍ ' + M(r'f(x) = x^2 + 2x - 1') + ' ជាប្រភេទអនុគមន៍អ្វី?',
        'មិនគូមិនសេស (Neither even nor odd)',
        ['អនុគមន៍គូ', 'អនុគមន៍សេស', 'អនុគមន៍ថេរ'],
        'f(-x) = x^2 - 2x - 1 ខុសពី f(x) និងខុសពី -f(x) ដូច្នេះមិនគូមិនសេសទេ។'
    ))

    C.append(mcq(
        'medium', 'concept',
        'តើការធ្វើតេស្តបន្ទាត់ឈរ (Vertical Line Test) ប្រើសម្រាប់អ្វី?',
        'ពិនិត្យថាតើក្រាបដែលបានឱ្យជាក្រាបនៃអនុគមន៍ឬមិនមែន',
        ['ពិនិត្យរកអនុគមន៍ច្រាស', 'ពិនិត្យរកចំណុចកាត់អ័ក្ស Ox', 'ពិនិត្យភាពជាអនុគមន៍គូ'],
        'បើបន្ទាត់ឈរនីមួយៗកាត់ក្រាបត្រង់យ៉ាងច្រើនមួយចំណុច នោះក្រាបជាតំណាងអនុគមន៍។'
    ))

    C.append(mcq(
        'medium', 'domain',
        'រកដែនកំណត់នៃអនុគមន៍ ' + M(r'f(x) = \dfrac{1}{\sqrt{x - 2}}') + '៖',
        M(r'(2, +\infty)'),
        [M(r'[2, +\infty)'), M(r'(-\infty, 2)'), M(r'\mathbb{R} \setminus \{2\}')],
        r'កន្សោមក្រោមរ៉ាឌីកាល់នៅភាគបែងត្រូវតែវិជ្ជមានដាច់ខាត៖ x - 2 > 0 \Leftrightarrow x > 2 នាំឱ្យ D = (2, +\infty)។'
    ))

    # =========================================================================
    # MCQ Hard (7)
    # =========================================================================
    C.append(mcq(
        'hard', 'domain',
        'រកដែនកំណត់នៃអនុគមន៍ ' + M(r'f(x) = \sqrt{\dfrac{x - 1}{x + 3}}') + '៖',
        M(r'(-\infty, -3) \cup [1, +\infty)'),
        [M(r'[-3, 1]'), M(r'(-3, 1]'), M(r'(-\infty, -3] \cup [1, +\infty)')],
        r'លក្ខខណ្ឌ៖ (x - 1)/(x + 3) \ge 0 និង x + 3 \neq 0។ តាមតារាងសញ្ញា ផលចែកវិជ្ជមានកាលណា x < -3 ឬ x \ge 1។'
    ))

    C.append(mcq(
        'hard', 'inverse',
        'រកអនុគមន៍ច្រាស ' + M(r'f^{-1}(x)') + ' នៃអនុគមន៍សនិទាន ' + M(r'f(x) = \dfrac{2x + 1}{x - 3}') + '៖',
        M(r'f^{-1}(x) = \dfrac{3x + 1}{x - 2}'),
        [M(r'f^{-1}(x) = \dfrac{x - 3}{2x + 1}'), M(r'f^{-1}(x) = \dfrac{3x - 1}{x + 2}'), M(r'f^{-1}(x) = \dfrac{2x - 1}{x + 3}')],
        r'y = \dfrac{2x + 1}{x - 3} \Leftrightarrow y(x - 3) = 2x + 1 \Leftrightarrow yx - 2x = 3y + 1 \Leftrightarrow x(y - 2) = 3y + 1 \Leftrightarrow x = \dfrac{3y + 1}{y - 2}។'
    ))

    C.append(mcq(
        'hard', 'param',
        'រកតម្លៃ ' + M(r'm') + ' ដើម្បីឱ្យអនុគមន៍ ' + M(r'f(x) = x^2 + 2(m - 1)x + 4') + ' វិជ្ជមានជានិច្ចចំពោះគ្រប់ ' + M(r'x \in \mathbb{R}') + '៖',
        M(r'-1 < m < 3'),
        [M(r'm < -1 \text{ ឬ } m > 3'), M(r'-3 < m < 1'), M(r'm > 3')],
        r'f(x) > 0 ជានិច្ចលុះត្រាតែ a = 1 > 0 និង \Delta\' = (m - 1)^2 - 4 < 0 \Leftrightarrow (m - 1 - 2)(m - 1 + 2) < 0 \Leftrightarrow (m - 3)(m + 1) < 0 \Leftrightarrow -1 < m < 3។'
    ))

    C.append(mcq(
        'hard', 'compose',
        'គេឱ្យ ' + M(r'f(x) = \dfrac{1}{1 - x}') + ' ចំពោះ ' + M(r'x \neq 0, 1') + '។ រកកន្សោមនៃ ' + M(r'(f \circ f)(x)') + '៖',
        M(r'\dfrac{x - 1}{x}'),
        [M(r'\dfrac{1}{x}'), M(r'\dfrac{x}{x - 1}'), M(r'x')],
        r'(f \circ f)(x) = f\left(\dfrac{1}{1 - x}\right) = \dfrac{1}{1 - \frac{1}{1 - x}} = \dfrac{1}{\frac{1 - x - 1}{1 - x}} = \dfrac{1 - x}{-x} = \dfrac{x - 1}{x}។'
    ))

    C.append(mcq(
        'hard', 'parity',
        'បើ ' + M(r'f') + ' ជាអនុគមន៍សេសកំណត់លើ ' + M(r'\mathbb{R}') + ' តើតម្លៃនៃ ' + M(r'f(x) + f(-x)') + ' ស្មើនឹងប៉ុន្មាន?',
        M(r'0'),
        [M(r'2f(x)'), M(r'-2f(x)'), M(r'1')],
        'ដោយ f ជាអនុគមន៍សេស នាំឱ្យ f(-x) = -f(x)។ ដូច្នេះ f(x) + f(-x) = f(x) - f(x) = 0 ជានិច្ច។'
    ))

    C.append(mcq(
        'hard', 'parity',
        'បើ ' + M(r'f') + ' ជាអនុគមន៍សេស និង ' + M(r'g') + ' ជាអនុគមន៍គូ (ដែល ' + M(r'g(x) \neq 0') + ') តើអនុគមន៍ ' + M(r'h(x) = \dfrac{f(x)}{g(x)}') + ' ជាប្រភេទអនុគមន៍អ្វី?',
        'អនុគមន៍សេស',
        ['អនុគមន៍គូ', 'មិនគូមិនសេស', 'អនុគមន៍ថេរ'],
        r'h(-x) = \dfrac{f(-x)}{g(-x)} = \dfrac{-f(x)}{g(x)} = -h(x) នាំឱ្យ h ជាអនុគមន៍សេស។'
    ))

    C.append(with_img(mcq(
        'hard', 'inverse',
        'ក្រាបខាងក្រោមបង្ហាញពីអនុគមន៍ ' + M(r'f(x) = 2x - 1') + ' និងអនុគមន៍ច្រាស ' + M(r'f^{-1}(x)') + '។ រកកូអរដោនេចំណុចប្រសព្វរវាងក្រាបទាំងពីរ៖',
        M(r'(1, 1)'),
        [M(r'(0, 0)'), M(r'(2, 2)'), M(r'(-1, -1)')],
        r'ចំណុចប្រសព្វស្ថិតនៅលើបន្ទាត់ y = x៖ 2x - 1 = x \Leftrightarrow x = 1 \Rightarrow y = 1។ ចំណុចប្រសព្វគឺ (1, 1)។'
    ), FIG_INVERSE_REFLECT))

    # =========================================================================
    # MCQ PISA (5)
    # =========================================================================
    C.append(mcq(
        'pisa', 'pisa',
        'ក្រុមហ៊ុនជួលរថយន្តមួយគិតថ្លៃសេវា ' + M(r'C(d) = 30 + 0.25d') + ' (គិតជាដុល្លារ) ដែល ' + M(r'd') + ' ជាចម្ងាយធ្វើដំណើរគិតជាគីឡូម៉ែត្រ។ បើអតិថិជនម្នាក់បង់ប្រាក់អស់ ' + M(r'65') + ' ដុល្លារ តើគាត់បានធ្វើដំណើរចម្ងាយប៉ុន្មាន?',
        '140 km',
        ['120 km', '150 km', '160 km'],
        '30 + 0.25d = 65 <=> 0.25d = 35 <=> d = 35 / 0.25 = 140 km។'
    ))

    C.append(mcq(
        'pisa', 'pisa',
        'រូបមន្តបំប្លែងសីតុណ្ហភាពពីអង្សាសេ ' + M(r'C') + ' ទៅអង្សាហ្វារិនហៃ ' + M(r'F') + ' គឺ ' + M(r'F(C) = \dfrac{9}{5}C + 32') + '។ តើអនុគមន៍ច្រាស ' + M(r'C(F)') + ' សម្រាប់បំប្លែងពី F មក C វិញគឺជាអ្វី?',
        M(r'C(F) = \dfrac{5}{9}(F - 32)'),
        [M(r'C(F) = \dfrac{9}{5}(F - 32)'), M(r'C(F) = \dfrac{5}{9}F - 32'), M(r'C(F) = \dfrac{5}{9}(F + 32)')],
        r'F - 32 = \dfrac{9}{5}C \Leftrightarrow C = \dfrac{5}{9}(F - 32)។'
    ))

    C.append(mcq(
        'pisa', 'pisa',
        'ចំនួនបាក់តេរីក្នុងមន្ទីរពិសោធន៍កើនឡើងទ្វេដងរៀងរាល់មួយម៉ោងម្តងតាមអនុគមន៍ ' + M(r'N(t) = 500 \cdot 2^t') + ' ដែល t ជាពេលវេលាគិតជាម៉ោង។ តើក្រោយរយៈពេល ' + M(r'4') + ' ម៉ោង ចំនួនបាក់តេរីមានប៉ុន្មាន?',
        '8000',
        ['4000', '2000', '16000'],
        'N(4) = 500 * 2^4 = 500 * 16 = 8000។'
    ))

    C.append(mcq(
        'pisa', 'pisa',
        'សិប្បកម្មមួយផលិតទំនិញ x គ្រឿងដោយមានថ្លៃដើមសរុប ' + M(r'C(x) = 1500 + 45x') + ' (ដុល្លារ) និងចំណូលពីការលក់ ' + M(r'R(x) = 75x') + ' (ដុល្លារ)។ រកចំនួនផលិតផល x ដើម្បីឱ្យសិប្បកម្មរួចដើម (Break-even point)៖',
        '50 គ្រឿង',
        ['40 គ្រឿង', '60 គ្រឿង', '30 គ្រឿង'],
        'រួចដើមកាលណា R(x) = C(x) <=> 75x = 1500 + 45x <=> 30x = 1500 <=> x = 50 គ្រឿង។'
    ))

    C.append(mcq(
        'pisa', 'pisa',
        'ដ្រូនមួយហោះធ្លាក់ចុះពីលើអាកាសមកដីតាមអនុគមន៍កម្ពស់ ' + M(r'h(t) = 120 - 4t') + ' (h គិតជាម៉ែត្រ, t ជាវិនាទី)។ តើរយៈពេលប៉ុន្មានវិនាទីទើបដ្រូនធ្លាក់ចុះដល់ដី?',
        '30 វិនាទី',
        ['20 វិនាទី', '40 វិនាទី', '25 វិនាទី'],
        'ធ្លាក់ដល់ដីកាលណា h(t) = 0 <=> 120 - 4t = 0 <=> 4t = 120 <=> t = 30 វិនាទី។'
    ))

    # =========================================================================
    # Writing Easy (1)
    # =========================================================================
    C.append(wr(
        'easy', 'eval',
        'គេឱ្យអនុគមន៍ ' + M(r'f(x) = 3x^2 - 2x + 1') + '។\n'
        'ក. គណនាតម្លៃនៃ ' + M(r'f(-2)') + '។\n'
        'ខ. គណនាតម្លៃនៃ ' + M(r'f(0)') + '។\n'
        'គ. គណនាតម្លៃនៃ ' + M(r'f(3)') + '។',
        [
            ('គណនា f(-2) = 3(-2)^2 - 2(-2) + 1 = 3(4) + 4 + 1 = 17', 2),
            ('គណនា f(0) = 3(0)^2 - 2(0) + 1 = 1', 1),
            ('គណនា f(3) = 3(3)^2 - 2(3) + 1 = 3(9) - 6 + 1 = 22', 2)
        ]
    ))

    # =========================================================================
    # Writing Medium (4)
    # =========================================================================
    C.append(wr(
        'medium', 'domain',
        'រកដែនកំណត់នៃបណ្តាអនុគមន៍ខាងក្រោម៖\n'
        'ក. ' + M(r'f(x) = \dfrac{2x + 5}{x^2 - 9}') + '\n'
        'ខ. ' + M(r'g(x) = \sqrt{4 - 2x}') + '។',
        [
            ('កំណត់លក្ខខណ្ឌភាគបែង f: x^2 - 9 ≠ 0 នាំឱ្យ x ≠ 3 និង x ≠ -3', 1.5),
            ('សន្និដ្ឋានដែនកំណត់ f: D_f = R \\ {-3, 3}', 1),
            ('កំណត់លក្ខខណ្ឌក្រោមរ៉ាឌីកាល់ g: 4 - 2x ≥ 0 នាំឱ្យ 2x ≤ 4 ឬ x ≤ 2', 1.5),
            ('សន្និដ្ឋានដែនកំណត់ g: D_g = (-∞, 2]', 1)
        ]
    ))

    C.append(wr(
        'medium', 'parity',
        'សិក្សាភាពជាអនុគមន៍គូ ឬសេស នៃបណ្តាអនុគមន៍ខាងក្រោម៖\n'
        'ក. ' + M(r'f(x) = x^3 - 5x') + '\n'
        'ខ. ' + M(r'g(x) = 4x^4 - 2x^2 + 3') + '។',
        [
            ('គណនា f(-x) = (-x)^3 - 5(-x) = -x^3 + 5x = -(x^3 - 5x) = -f(x)', 1.5),
            ('សន្និដ្ឋាន f(x) ជាអនុគមន៍សេស', 1),
            ('គណនា g(-x) = 4(-x)^4 - 2(-x)^2 + 3 = 4x^4 - 2x^2 + 3 = g(x)', 1.5),
            ('សន្និដ្ឋាន g(x) ជាអនុគមន៍គូ', 1)
        ]
    ))

    C.append(wr(
        'medium', 'compose',
        'គេឱ្យអនុគមន៍ពីរ ' + M(r'f(x) = 2x - 1') + ' និង ' + M(r'g(x) = 3x + 4') + '។\n'
        'ក. រកកន្សោមអនុគមន៍បណ្ដាក់ ' + M(r'(f \circ g)(x)') + '។\n'
        'ខ. រកកន្សោមអនុគមន៍បណ្ដាក់ ' + M(r'(g \circ f)(x)') + '។\n'
        'គ. ផ្ទៀងផ្ទាត់ថាតើ ' + M(r'(f \circ g)(x) = (g \circ f)(x)') + ' ឬទេ?',
        [
            ('គណនា (f ∘ g)(x) = f(3x + 4) = 2(3x + 4) - 1 = 6x + 8 - 1 = 6x + 7', 2),
            ('គណនា (g ∘ f)(x) = g(2x - 1) = 3(2x - 1) + 4 = 6x - 3 + 4 = 6x + 1', 2),
            ('សន្និដ្ឋានថាមិនស្មើគ្នាទេ: (f ∘ g)(x) ≠ (g ∘ f)(x) ព្រោះ 6x + 7 ≠ 6x + 1', 1)
        ]
    ))

    C.append(wr(
        'medium', 'inverse',
        'គេឱ្យអនុគមន៍ ' + M(r'f(x) = \dfrac{3x - 2}{5}') + '។\n'
        'ក. រកកន្សោមអនុគមន៍ច្រាស ' + M(r'f^{-1}(x)') + '។\n'
        'ខ. គណនា ' + M(r'(f \circ f^{-1})(x)') + ' ដើម្បីផ្ទៀងផ្ទាត់លទ្ធផល។',
        [
            ('តាង y = (3x - 2)/5 នាំឱ្យ 5y = 3x - 2 ឬ 3x = 5y + 2', 1.5),
            ('ទាញរក x = (5y + 2)/3 ដូច្នេះ f^(-1)(x) = (5x + 2)/3', 1.5),
            ('គណនា (f ∘ f^(-1))(x) = f((5x + 2)/3) = (3 * (5x + 2)/3 - 2) / 5', 1),
            ('សម្រួលកន្សោម: (5x + 2 - 2) / 5 = 5x / 5 = x ពិត', 1)
        ]
    ))

    # =========================================================================
    # Writing Hard (4)
    # =========================================================================
    C.append(wr(
        'hard', 'domain',
        'រកដែនកំណត់នៃអនុគមន៍ ' + M(r'f(x) = \dfrac{\sqrt{x^2 - 5x + 6}}{x - 4}') + '។',
        [
            ('កំណត់លក្ខខណ្ឌក្រោមរ៉ាឌីកាល់: x^2 - 5x + 6 ≥ 0', 1.5),
            ('រកឫសសមីការ x^2 - 5x + 6 = 0: x = 2 និង x = 3 នាំឱ្យ x ≤ 2 ឬ x ≥ 3', 1.5),
            ('កំណត់លក្ខខណ្ឌភាគបែង: x - 4 ≠ 0 នាំឱ្យ x ≠ 4', 1),
            ('សន្និដ្ឋានដែនកំណត់ចុងក្រោយ: D = (-∞, 2] ∪ [3, 4) ∪ (4, +∞)', 1)
        ]
    ))

    C.append(wr(
        'hard', 'inverse',
        'គេឱ្យអនុគមន៍ ' + M(r'f(x) = \dfrac{2x - 1}{x + 3}') + '។\n'
        'ក. រកដែនកំណត់នៃ ' + M(r'f') + '។\n'
        'ខ. រកកន្សោមអនុគមន៍ច្រាស ' + M(r'f^{-1}(x)') + ' និងដែនកំណត់របស់វា។\n'
        'គ. កំណត់កូអរដោនេចំណុចប្រសព្វរវាងក្រាបទាំងពីរនៅលើបន្ទាត់ ' + M(r'y = x') + '។',
        [
            ('ដែនកំណត់ f: x + 3 ≠ 0 នាំឱ្យ D_f = R \\ {-3}', 1),
            ('ទាញរក f^(-1): y(x + 3) = 2x - 1 នាំឱ្យ yx - 2x = -3y - 1 ឬ x(y - 2) = -3y - 1 នាំឱ្យ f^(-1)(x) = (-3x - 1)/(x - 2) = (3x + 1)/(2 - x)', 1.5),
            ('ដែនកំណត់ f^(-1): D_(f^-1) = R \\ {2}', 0.5),
            ('ដោះស្រាយសមីការប្រសព្វ f(x) = x: (2x - 1)/(x + 3) = x នាំឱ្យ x^2 + 3x = 2x - 1 ឬ x^2 + x + 1 = 0', 1),
            ('គណនា Delta = 1 - 4 = -3 < 0 សមីការគ្មានឫសពិត នាំឱ្យក្រាបទាំងពីរមិនប្រសព្វគ្នា', 1)
        ]
    ))

    C.append(wr(
        'hard', 'param',
        'គេឱ្យអនុគមន៍លីនេអ៊ែរ ' + M(r'f(x) = ax + b') + ' (ដែល ' + M(r'a \neq 0') + ')។\n'
        'ក. កំណត់តម្លៃ ' + M(r'a') + ' និង ' + M(r'b') + ' ដោយដឹងថា ' + M(r'f(1) = 5') + ' និង ' + M(r'f^{-1}(3) = -1') + '។\n'
        'ខ. សរសេរសមីការអនុគមន៍ ' + M(r'f(x)') + ' និង ' + M(r'f^{-1}(x)') + '។',
        [
            ('បកប្រែ f^(-1)(3) = -1 ទៅជា f(-1) = 3', 1.5),
            ('បង្កើតប្រព័ន្ធសមីការ: a(1) + b = 5 និង a(-1) + b = 3', 1.5),
            ('ដោះស្រាយប្រព័ន្ធសមីការ: បូកអង្គនិងអង្គ 2b = 8 នាំឱ្យ b = 4 រួចទាញបាន a = 1', 1),
            ('សរសេរចម្លើយ: f(x) = x + 4 និង f^(-1)(x) = x - 4', 1)
        ]
    ))

    C.append(wr(
        'hard', 'parity',
        'សិក្សាភាពគូ-សេសនៃអនុគមន៍ខាងក្រោម៖\n'
        'ក. ' + M(r'f(x) = \dfrac{x^3 + x}{|x| + 1}') + '\n'
        'ខ. ' + M(r'g(x) = \sqrt{x^2 + 1} + x^2') + '។',
        [
            ('ពិនិត្យ f(-x): f(-x) = ((-x)^3 + (-x)) / (|-x| + 1) = (-x^3 - x) / (|x| + 1)', 1.5),
            ('ទាញសញ្ញាដកជាកត្តា: f(-x) = -(x^3 + x) / (|x| + 1) = -f(x) នាំឱ្យ f ជាអនុគមន៍សេស', 1),
            ('ពិនិត្យ g(-x): g(-x) = sqrt((-x)^2 + 1) + (-x)^2 = sqrt(x^2 + 1) + x^2 = g(x)', 1.5),
            ('សន្និដ្ឋាន: g(x) ជាអនុគមន៍គូ', 1)
        ]
    ))

    # =========================================================================
    # Writing PISA (5)
    # =========================================================================
    C.append(wr(
        'pisa', 'pisa',
        'ក្រុមហ៊ុនទូរស័ព្ទមួយផ្តល់គម្រោងសេវាប្រចាំខែ ' + M(r'C(m) = 12 + 0.05m') + ' (គិតជាដុល្លារ) ដែល ' + M(r'm') + ' ជាចំនួននាទីហៅចេញលើសកំណត់។\n'
        'ក. បើលោក សុខ ប្រើអស់ ' + M(r'180') + ' នាទីលើស តើគាត់ត្រូវបង់ប្រាក់ប៉ុន្មាន?\n'
        'ខ. រកអនុគមន៍ច្រាស ' + M(r'm(C)') + ' ដែលកំណត់ចំនួននាទីហៅចេញជាអនុគមន៍នៃប្រាក់ត្រូវបង់។\n'
        'គ. បើខែនេះលោក សុខ ត្រូវបង់ប្រាក់ ' + M(r'24.50') + ' ដុល្លារ តើគាត់បានប្រើប្រាស់អស់ប៉ុន្មាននាទីលើស?',
        [
            ('គណនា C(180) = 12 + 0.05(180) = 12 + 9 = 21 ដុល្លារ', 1.5),
            ('ទាញរកអនុគមន៍ច្រាស: C - 12 = 0.05m នាំឱ្យ m = (C - 12) / 0.05 = 20(C - 12) = 20C - 240', 2),
            ('គណនាចំនួននាទីសម្រាប់ C = 24.50: m = 20(24.50 - 12) = 20(12.50) = 250 នាទី', 1.5)
        ]
    ))

    C.append(wr(
        'pisa', 'pisa',
        'រោងចក្រខ្នាតតូចមួយផលិតកាតាបសិស្ស។ ថ្លៃដើមផលិតសរុបប្រចាំថ្ងៃគឺ ' + M(r'C(x) = 300 + 8x') + ' (ដុល្លារ) និងចំណូលពីការលក់គឺ ' + M(r'R(x) = 14x') + ' (ដុល្លារ) ដែល ' + M(r'x') + ' ជាចំនួនកាតាបដែលបានផលិតនិងលក់ដាច់។\n'
        'ក. សរសេរកន្សោមអនុគមន៍ប្រាក់ចំណេញ ' + M(r'P(x) = R(x) - C(x)') + '។\n'
        'ខ. រកចំនួនកាតាបដែលត្រូវលក់ដើម្បីឱ្យរោងចក្ររួចដើម (Break-even point)។\n'
        'គ. គណនាប្រាក់ចំណេញបើរោងចក្រផលិតនិងលក់បាន ' + M(r'120') + ' កាតាបក្នុងមួយថ្ងៃ។',
        [
            ('សរសេរកន្សោម P(x) = 14x - (300 + 8x) = 14x - 8x - 300 = 6x - 300', 1.5),
            ('កំណត់ចំណុចរួចដើម: P(x) = 0 នាំឱ្យ 6x - 300 = 0 ឬ 6x = 300 នាំឱ្យ x = 50 កាតាប', 2),
            ('គណនាប្រាក់ចំណេញ: P(120) = 6(120) - 300 = 720 - 300 = 420 ដុល្លារ', 1.5)
        ]
    ))

    C.append(wr(
        'pisa', 'pisa',
        'ការប្តូរប្រាក់ពីប្រាក់ដុល្លារ ' + M(r'x') + ' (USD) ទៅជាប្រាក់រៀលតាមអត្រាការប្រាក់ ' + M(r'f(x) = 4100x') + ' (KHR)។ ភ្នាក់ងារប្តូរប្រាក់កាត់កម្រៃជើងសារ 2% លើប្រាក់រៀលដែលទទួលបាន គឺ ' + M(r'g(y) = 0.98y') + '។\n'
        'ក. រកអនុគមន៍បណ្ដាក់ ' + M(r'(g \circ f)(x)') + ' ដែលកំណត់ប្រាក់រៀលសុទ្ធទទួលបានពីប្រាក់ដុល្លារ ' + M(r'x') + '។\n'
        'ខ. គណនាប្រាក់រៀលសុទ្ធដែលទទួលបានបើភ្ញៀវទេសចរប្តូរប្រាក់ ' + M(r'250') + ' ដុល្លារ។\n'
        'គ. រកអនុគមន៍ច្រាស ' + M(r'(g \circ f)^{-1}') + ' ដើម្បីគណនាចំនួនដុល្លារដែលត្រូវការដើម្បីទទួលបានប្រាក់រៀលសុទ្ធ ' + M(r'4,018,000\text{ KHR}') + '។',
        [
            ('គណនា (g ∘ f)(x) = g(4100x) = 0.98 * 4100x = 4018x (KHR)', 1.5),
            ('គណនាប្រាក់រៀលពី 250 ដុល្លារ: (g ∘ f)(250) = 4018 * 250 = 1,004,500 KHR', 1.5),
            ('ទាញរកអនុគមន៍ច្រាស: x = y / 4018', 1),
            ('គណនាប្រាក់ដុល្លារ: x = 4018000 / 4018 = 1000 USD', 1)
        ]
    ))

    C.append(wr(
        'pisa', 'pisa',
        'នៅក្នុងរូបវិទ្យា អាំងតង់ស៊ីតេពន្លឺ ' + M(r'I') + ' ពីប្រភពពន្លឺមួយថយចុះតាមចម្ងាយ ' + M(r'd') + ' (ម៉ែត្រ) តាមអនុគមន៍ ' + M(r'I(d) = \dfrac{100}{d^2}') + ' (គិតជា ' + M(r'\text{W/m}^2') + ', ចំពោះ ' + M(r'd > 0') + ')។\n'
        'ក. គណនាអាំងតង់ស៊ីតេពន្លឺនៅចម្ងាយ ' + M(r'd = 2\text{ m}') + ' និង ' + M(r'd = 5\text{ m}') + '។\n'
        'ខ. រកអនុគមន៍ច្រាស ' + M(r'd(I)') + ' កំណត់ចម្ងាយតាមអាំងតង់ស៊ីតេពន្លឺ។\n'
        'គ. តើនៅចម្ងាយប៉ុន្មានម៉ែត្រទើបអាំងតង់ស៊ីតេពន្លឺធ្លាក់ចុះមកត្រឹម ' + M(r'4\text{ W/m}^2') + '?',
        [
            ('គណនា I(2) = 100 / 2^2 = 100 / 4 = 25 W/m^2 និង I(5) = 100 / 5^2 = 100 / 25 = 4 W/m^2', 2),
            ('ទាញរក d(I): I = 100 / d^2 នាំឱ្យ d^2 = 100 / I ឬ d = 10 / sqrt(I) (ដោយ d > 0)', 1.5),
            ('គណនាចម្ងាយសម្រាប់ I = 4: d = 10 / sqrt(4) = 10 / 2 = 5 m', 1.5)
        ]
    ))

    C.append(wr(
        'pisa', 'pisa',
        'ហាងទំនិញមួយផ្តល់ការបញ្ចុះតម្លៃពីរប្រភេទ៖ ប័ណ្ណបញ្ចុះតម្លៃ 20 ដុល្លារ ' + M(r'f(x) = x - 20') + ' និងការបញ្ចុះតម្លៃ 10% គឺ ' + M(r'g(x) = 0.90x') + ' (ចំពោះទំនិញតម្លៃដើម x ដុល្លារ, ' + M(r'x \ge 50') + ')។\n'
        'ក. រកកន្សោម ' + M(r'(f \circ g)(x)') + ' (ចុះ 10% សិន ទើបបញ្ចុះ 20 ដុល្លារតាមក្រោយ)។\n'
        'ខ. រកកន្សោម ' + M(r'(g \circ f)(x)') + ' (បញ្ចុះ 20 ដុល្លារសិន ទើបចុះ 10% តាមក្រោយ)។\n'
        'គ. តើវិធីបញ្ចុះតម្លៃមួយណាផ្តល់តម្លៃទាបជាង (ចំណេញជាង) ដល់អតិថិជន? ចូរពន្យល់ដោយគណនាផលដក។',
        [
            ('គណនា (f ∘ g)(x) = f(0.90x) = 0.90x - 20', 1.5),
            ('គណនា (g ∘ f)(x) = g(x - 20) = 0.90(x - 20) = 0.90x - 18', 1.5),
            ('ប្រៀបធៀបផលដក: (g ∘ f)(x) - (f ∘ g)(x) = (0.90x - 18) - (0.90x - 20) = 2 ដុល្លារ', 1),
            ('សន្និដ្ឋាន: វិធី (f ∘ g)(x) ផ្តល់តម្លៃទាបជាង 2 ដុល្លារ ដូច្នេះវិធី (f ∘ g) ចំណេញជាង', 1)
        ]
    ))

    return C
