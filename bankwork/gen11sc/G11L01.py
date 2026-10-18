# -*- coding: utf-8 -*-
"""
KhmerMath Question Bank: Grade 11 Science (SC)
Chapter 1: ស្វ៊ីតនិងអនុមានរួមគណិតវិទ្យា
Lesson 1: ស្វ៊ីតចំនួនពិត (Real Sequences)
Reference textbook: Lesson/G11/SC/p1-c1-l1.tex
Adheres to IMAGE_STYLE_GUIDE.md (clean vector illustrations, isolated, no background rect, flat colors, Mathcad italic font)

Target matrix:
  MCQ:     easy=10, medium=14, hard=7, pisa=5  (36 total)
  Writing: easy=1,  medium=4,  hard=4, pisa=5  (14 total, rubrics sum to 5)
  Total: 50 questions
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib import *

LESSON = 'ស្វ៊ីតចំនួនពិត'
CHAPTER = 'ជំពូកទី 1 : ស្វ៊ីតនិងអនុមានរួមគណិតវិទ្យា'

# =============================================================================
# SVG Vector Illustrations (Adhering strictly to IMAGE_STYLE_GUIDE.md)
# - Isolated, transparent background (NO <rect fill='#ffffff'/>)
# - Math variables in Mathcad UniMath Italic
# - Numbers and units in Times New Roman upright
# =============================================================================

# 1. Sequence Mapping f: N -> R
FIG_SEQUENCE_MAPPING = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 520 200' width='520' height='200'>
  <!-- Domain Set N (Left) -->
  <rect x='50' y='30' width='130' height='150' rx='24' fill='none' stroke='#2563eb' stroke-width='2'/>
  <text x='115' y='22' text-anchor='middle' font-family="'Times New Roman', serif" font-size='14' font-weight='bold' fill='#2563eb'>ដែនកំណត់ ℕ (n)</text>
  
  <circle cx='115' cy='55' r='4' fill='#2563eb'/>
  <text x='100' y='59' text-anchor='end' font-family="'Times New Roman', serif" font-size='14' font-weight='bold' fill='#1e293b'>1</text>

  <circle cx='115' cy='85' r='4' fill='#2563eb'/>
  <text x='100' y='89' text-anchor='end' font-family="'Times New Roman', serif" font-size='14' font-weight='bold' fill='#1e293b'>2</text>

  <circle cx='115' cy='115' r='4' fill='#2563eb'/>
  <text x='100' y='119' text-anchor='end' font-family="'Times New Roman', serif" font-size='14' font-weight='bold' fill='#1e293b'>3</text>

  <text x='115' y='142' text-anchor='middle' font-family="'Times New Roman', serif" font-size='16' fill='#64748b'>⋮</text>

  <circle cx='115' cy='160' r='4' fill='#2563eb'/>
  <text x='100' y='164' text-anchor='end' font-family="'Mathcad UniMath Italic', serif" font-style='italic' font-size='14' fill='#1e293b'>n</text>

  <!-- Co-Domain Set R (Right) -->
  <rect x='340' y='30' width='130' height='150' rx='24' fill='none' stroke='#059669' stroke-width='2'/>
  <text x='405' y='22' text-anchor='middle' font-family="'Times New Roman', serif" font-size='14' font-weight='bold' fill='#059669'>សំណុំចុង ℝ (a<tspan font-family="'Mathcad UniMath Italic', serif" font-style='italic'>_n</tspan>)</text>

  <circle cx='405' cy='55' r='4' fill='#059669'/>
  <text x='420' y='60' text-anchor='start' font-family="'Times New Roman', serif" font-size='14' font-weight='bold' fill='#1e293b'>a<tspan font-size='11' font-family="'Mathcad UniMath Italic', serif" font-style='italic'>_1</tspan></text>

  <circle cx='405' cy='85' r='4' fill='#059669'/>
  <text x='420' y='90' text-anchor='start' font-family="'Times New Roman', serif" font-size='14' font-weight='bold' fill='#1e293b'>a<tspan font-size='11' font-family="'Mathcad UniMath Italic', serif" font-style='italic'>_2</tspan></text>

  <circle cx='405' cy='115' r='4' fill='#059669'/>
  <text x='420' y='120' text-anchor='start' font-family="'Times New Roman', serif" font-size='14' font-weight='bold' fill='#1e293b'>a<tspan font-size='11' font-family="'Mathcad UniMath Italic', serif" font-style='italic'>_3</tspan></text>

  <text x='405' y='142' text-anchor='middle' font-family="'Times New Roman', serif" font-size='16' fill='#64748b'>⋮</text>

  <circle cx='405' cy='160' r='4' fill='#059669'/>
  <text x='420' y='165' text-anchor='start' font-family="'Times New Roman', serif" font-size='14' font-weight='bold' fill='#1e293b'>a<tspan font-size='11' font-family="'Mathcad UniMath Italic', serif" font-style='italic'>_n</tspan></text>

  <!-- Mapping Arrows -->
  <defs>
    <marker id='arr' viewBox='0 0 10 10' refX='6' refY='5' markerWidth='6' markerHeight='6' orient='auto-start-reverse'>
      <path d='M 0 1 L 8 5 L 0 9 z' fill='#6366f1'/>
    </marker>
  </defs>

  <path d='M 125 55 C 220 40, 300 40, 395 55' fill='none' stroke='#6366f1' stroke-width='1.8' marker-end='url(#arr)'/>
  <path d='M 125 85 C 220 75, 300 75, 395 85' fill='none' stroke='#6366f1' stroke-width='1.8' marker-end='url(#arr)'/>
  <path d='M 125 115 C 220 110, 300 110, 395 115' fill='none' stroke='#6366f1' stroke-width='1.8' marker-end='url(#arr)'/>
  <path d='M 125 160 C 220 160, 300 160, 395 160' fill='none' stroke='#6366f1' stroke-width='1.8' marker-end='url(#arr)'/>

  <!-- Function Label -->
  <rect x='220' y='80' width='80' height='32' rx='6' fill='#f8fafc' stroke='#6366f1' stroke-width='1.5'/>
  <text x='260' y='101' text-anchor='middle' font-family="'Times New Roman', serif" font-size='13' font-weight='bold' fill='#4338ca'>f(n) = a<tspan font-family="'Mathcad UniMath Italic', serif" font-style='italic'>_n</tspan></text>
</svg>"""

# 2. Monotonic Sequences: Increasing and Decreasing Graphs
FIG_MONOTONIC_GRAPH = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 520 200' width='520' height='200'>
  <!-- Left Graph: Increasing a_n = n/(n+1) -->
  <line x1='40' y1='170' x2='230' y2='170' stroke='#334155' stroke-width='1.5'/>
  <polygon points='230,170 223,166 223,174' fill='#334155'/>
  <text x='230' y='185' font-family="'Mathcad UniMath Italic', serif" font-style='italic' font-size='13' fill='#334155'>n</text>

  <line x1='50' y1='180' x2='50' y2='30' stroke='#334155' stroke-width='1.5'/>
  <polygon points='50,30 46,37 54,37' fill='#334155'/>
  <text x='35' y='35' font-family="'Mathcad UniMath Italic', serif" font-style='italic' font-size='13' fill='#334155'>a<tspan font-size='10'>_n</tspan></text>

  <text x='135' y='22' text-anchor='middle' font-family="'Times New Roman', serif" font-size='12' font-weight='bold' fill='#2563eb'>ស្វ៊ីតកើន: a<tspan font-family="'Mathcad UniMath Italic', serif" font-style='italic'>_n</tspan> = n/(n+1)</text>

  <line x1='50' y1='60' x2='220' y2='60' stroke='#94a3b8' stroke-width='1' stroke-dasharray='3,3'/>
  <text x='45' y='64' text-anchor='end' font-family="'Times New Roman', serif" font-size='11' fill='#64748b'>1</text>

  <path d='M 75 115 Q 120 75 210 68' fill='none' stroke='#93c5fd' stroke-width='1.5' stroke-dasharray='2,2'/>
  <circle cx='75' cy='115' r='4' fill='#2563eb'/>
  <text x='75' y='183' text-anchor='middle' font-family="'Times New Roman', serif" font-size='11' fill='#475569'>1</text>

  <circle cx='105' cy='97' r='4' fill='#2563eb'/>
  <text x='105' y='183' text-anchor='middle' font-family="'Times New Roman', serif" font-size='11' fill='#475569'>2</text>

  <circle cx='135' cy='88' r='4' fill='#2563eb'/>
  <text x='135' y='183' text-anchor='middle' font-family="'Times New Roman', serif" font-size='11' fill='#475569'>3</text>

  <circle cx='165' cy='82' r='4' fill='#2563eb'/>
  <text x='165' y='183' text-anchor='middle' font-family="'Times New Roman', serif" font-size='11' fill='#475569'>4</text>

  <circle cx='195' cy='78' r='4' fill='#2563eb'/>
  <text x='195' y='183' text-anchor='middle' font-family="'Times New Roman', serif" font-size='11' fill='#475569'>5</text>

  <!-- Right Graph: Decreasing a_n = 1/n -->
  <line x1='300' y1='170' x2='490' y2='170' stroke='#334155' stroke-width='1.5'/>
  <polygon points='490,170 483,166 483,174' fill='#334155'/>
  <text x='490' y='185' font-family="'Mathcad UniMath Italic', serif" font-style='italic' font-size='13' fill='#334155'>n</text>

  <line x1='310' y1='180' x2='310' y2='30' stroke='#334155' stroke-width='1.5'/>
  <polygon points='310,30 306,37 314,37' fill='#334155'/>
  <text x='295' y='35' font-family="'Mathcad UniMath Italic', serif" font-style='italic' font-size='13' fill='#334155'>a<tspan font-size='10'>_n</tspan></text>

  <text x='395' y='22' text-anchor='middle' font-family="'Times New Roman', serif" font-size='12' font-weight='bold' fill='#dc2626'>ស្វ៊ីតចុះ: a<tspan font-family="'Mathcad UniMath Italic', serif" font-style='italic'>_n</tspan> = 1/n</text>

  <path d='M 335 60 Q 370 125 470 155' fill='none' stroke='#fca5a5' stroke-width='1.5' stroke-dasharray='2,2'/>
  <circle cx='335' cy='60' r='4' fill='#dc2626'/>
  <text x='335' y='183' text-anchor='middle' font-family="'Times New Roman', serif" font-size='11' fill='#475569'>1</text>

  <circle cx='365' cy='115' r='4' fill='#dc2626'/>
  <text x='365' y='183' text-anchor='middle' font-family="'Times New Roman', serif" font-size='11' fill='#475569'>2</text>

  <circle cx='395' cy='133' r='4' fill='#dc2626'/>
  <text x='395' y='183' text-anchor='middle' font-family="'Times New Roman', serif" font-size='11' fill='#475569'>3</text>

  <circle cx='425' cy='142' r='4' fill='#dc2626'/>
  <text x='425' y='183' text-anchor='middle' font-family="'Times New Roman', serif" font-size='11' fill='#475569'>4</text>

  <circle cx='455' cy='148' r='4' fill='#dc2626'/>
  <text x='455' y='183' text-anchor='middle' font-family="'Times New Roman', serif" font-size='11' fill='#475569'>5</text>
</svg>"""

# 3. Bouncing Ball Motion Model (Textbook Section 2 Model 2)
FIG_BOUNCING_BALL = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 520 220' width='520' height='220'>
  <!-- Ground line -->
  <line x1='30' y1='180' x2='490' y2='180' stroke='#334155' stroke-width='3'/>
  <line x1='30' y1='185' x2='490' y2='185' stroke='#94a3b8' stroke-width='1' stroke-dasharray='4,4'/>
  <text x='490' y='175' text-anchor='end' font-family="'Times New Roman', serif" font-size='12' fill='#64748b'>ដី (Ground)</text>

  <!-- Initial Drop from 6m -->
  <circle cx='60' cy='30' r='9' fill='#ef4444' stroke='#b91c1c' stroke-width='1.5'/>
  <line x1='60' y1='39' x2='60' y2='178' stroke='#ef4444' stroke-width='2' stroke-dasharray='4,3'/>
  <line x1='45' y1='30' x2='45' y2='180' stroke='#2563eb' stroke-width='1.5'/>
  <polygon points='45,30 42,37 48,37' fill='#2563eb'/>
  <polygon points='45,180 42,173 48,173' fill='#2563eb'/>
  <text x='38' y='110' text-anchor='end' font-family="'Times New Roman', serif" font-size='13' font-weight='bold' fill='#2563eb'>6 m</text>

  <!-- Rebound 1 (Peak at 4m) -->
  <path d='M 60 180 Q 120 70 180 180' fill='none' stroke='#0891b2' stroke-width='2.5'/>
  <circle cx='120' cy='75' r='8' fill='#0891b2'/>
  <line x1='120' y1='83' x2='120' y2='180' stroke='#0891b2' stroke-width='1' stroke-dasharray='3,3'/>
  <text x='120' y='60' text-anchor='middle' font-family="'Times New Roman', serif" font-size='12' font-weight='bold' fill='#0891b2'>លើកទី 1: a<tspan font-family="'Mathcad UniMath Italic', serif" font-style='italic'>_1</tspan> = 4 m</text>

  <!-- Rebound 2 (Peak at 8/3m) -->
  <path d='M 180 180 Q 240 100 300 180' fill='none' stroke='#059669' stroke-width='2'/>
  <circle cx='240' cy='105' r='7' fill='#059669'/>
  <line x1='240' y1='112' x2='240' y2='180' stroke='#059669' stroke-width='1' stroke-dasharray='3,3'/>
  <text x='240' y='92' text-anchor='middle' font-family="'Times New Roman', serif" font-size='12' font-weight='bold' fill='#059669'>លើកទី 2: a<tspan font-family="'Mathcad UniMath Italic', serif" font-style='italic'>_2</tspan> = 8/3 m</text>

  <!-- Rebound 3 (Peak at 16/9m) -->
  <path d='M 300 180 Q 355 125 410 180' fill='none' stroke='#7c3aed' stroke-width='2'/>
  <circle cx='355' cy='130' r='6' fill='#7c3aed'/>
  <line x1='355' y1='136' x2='355' y2='180' stroke='#7c3aed' stroke-width='1' stroke-dasharray='3,3'/>
  <text x='355' y='118' text-anchor='middle' font-family="'Times New Roman', serif" font-size='12' font-weight='bold' fill='#7c3aed'>លើកទី 3: a<tspan font-family="'Mathcad UniMath Italic', serif" font-style='italic'>_3</tspan> = 16/9 m</text>

  <!-- Ratio formula box -->
  <rect x='340' y='18' width='165' height='46' rx='6' fill='none' stroke='#64748b' stroke-width='1.5'/>
  <text x='422' y='36' text-anchor='middle' font-family="'Times New Roman', serif" font-size='12' fill='#334155'>ផលធៀបលោត = 2/3</text>
  <text x='422' y='53' text-anchor='middle' font-family="'Times New Roman', serif" font-size='12' font-weight='bold' fill='#2563eb'>a<tspan font-family="'Mathcad UniMath Italic', serif" font-style='italic'>_n</tspan> = 6 × (2/3)<tspan font-family="'Mathcad UniMath Italic', serif" font-style='italic'>ⁿ</tspan></text>
</svg>"""


def with_img(q, svg):
    q['img'] = svg
    return q


def writing(level, sec, stem, steps):
    return wr(level, sec, stem, steps)


def cands():
    C = []

    # =========================================================================
    # 1. MCQ - EASY (10 items)
    # =========================================================================
    C.append(with_img(mcq(
        'easy', 'sec1_def',
        'តាមនិយមន័យ ស្វ៊ីតនៃចំនួនពិត គឺជាអនុគមន៍លេខដែលកំណត់ពី ៖',
        M(r'\mathbb{N} \to \mathbb{R}'),
        [
            M(r'\mathbb{R} \to \mathbb{N}'),
            M(r'\mathbb{Z} \to \mathbb{Q}'),
            M(r'\mathbb{R} \to \mathbb{R}')
        ],
        'ស្វ៊ីតចំនួនពិតគឺជាអនុគមន៍កំណត់ពីសំណុំចំនួនគត់ធម្មជាតិ ' + M(r'\mathbb{N}') + ' ទៅសំណុំចំនួនពិត ' + M(r'\mathbb{R}') + '។'
    ), FIG_SEQUENCE_MAPPING))

    C.append(mcq(
        'easy', 'sec1_finite',
        'ក្នុងចំណោមស្វ៊ីតខាងក្រោម តើស្វ៊ីតមួយណាជា «ស្វ៊ីតរាប់អស់» (Finite Sequence)?',
        M('1, 3, 5, 7, 9, 11, 13, 15'),
        [
            M(r'1, 2, 3, 4, 5, \dots'),
            M(r'2, 4, 6, 8, \dots'),
            M(r'1, \dfrac{1}{2}, \dfrac{1}{4}, \dots')
        ],
        'ស្វ៊ីតរាប់អស់គឺជាស្វ៊ីតដែលមានចំនួនតួកំណត់ និងមានតួចុងក្រោយជាក់លាក់។'
    ))

    C.append(mcq(
        'easy', 'sec1_eval_lin',
        'គេមានស្វ៊ីត ' + M('a_n = 2n + 1') + '។ គណនាតម្លៃនៃតួទី 3 (' + M('a_3') + ') ៖',
        M('7'),
        [M('5'), M('9'), M('6')],
        'ជំនួស ' + M('n = 3') + ' គេបាន ' + M('a_3 = 2(3) + 1 = 6 + 1 = 7') + '។'
    ))

    C.append(mcq(
        'easy', 'sec1_eval_lin2',
        'គេមានស្វ៊ីត ' + M('a_n = 3n - 2') + '។ គណនាតម្លៃនៃតួទី 4 (' + M('a_4') + ') ៖',
        M('10'),
        [M('12'), M('8'), M('14')],
        'ជំនួស ' + M('n = 4') + ' គេបាន ' + M('a_4 = 3(4) - 2 = 12 - 2 = 10') + '។'
    ))

    C.append(mcq(
        'easy', 'sec1_eval_frac',
        'គេមានស្វ៊ីត ' + M(r'a_n = \dfrac{1}{n+1}') + '។ គណនាតម្លៃនៃតួទី 3 (' + M('a_3') + ') ៖',
        M(r'\dfrac{1}{4}'),
        [M(r'\dfrac{1}{3}'), M(r'\dfrac{1}{5}'), M(r'\dfrac{3}{4}')],
        'ជំនួស ' + M('n = 3') + ' គេបាន ' + M(r'a_3 = \dfrac{1}{3+1} = \dfrac{1}{4}') + '។'
    ))

    C.append(mcq(
        'easy', 'sec2_square',
        'ស្វ៊ីតនៃចំនួនការេ ' + M(r'1, 4, 9, 16, 25, \dots') + ' មានតួទី ' + M('n') + ' ស្មើនឹង ៖',
        M('a_n = n^2'),
        [M('a_n = 2n'), M('a_n = 2^n'), M('a_n = n^3')],
        'តួនីមួយៗជាការេនៃចំនួនគត់ធម្មជាតិ ' + M(r'1^2, 2^2, 3^2, \dots') + ' នាំឱ្យ ' + M('a_n = n^2') + '។'
    ))

    C.append(mcq(
        'easy', 'sec2_even',
        'ស្វ៊ីតនៃចំនួនគត់គូ ' + M(r'2, 4, 6, 8, 10, \dots') + ' មានតួទី ' + M('n') + ' ស្មើនឹង ៖',
        M('a_n = 2n'),
        [M('a_n = 2n - 1'), M('a_n = 2n + 1'), M('a_n = n^2')],
        'តួនីមួយៗគឺ 2 គុណនឹង ' + M('n') + ' នាំឱ្យ ' + M('a_n = 2n') + '។'
    ))

    C.append(mcq(
        'easy', 'sec3_def_inc',
        'ស្វ៊ីត ' + M('(a_n)') + ' ជា «ស្វ៊ីតកើន» លុះត្រាតែចំពោះគ្រប់ ' + M(r'n \in \mathbb{N}') + ' ៖',
        M(r'a_{n+1} \ge a_n'),
        [
            M(r'a_{n+1} \le a_n'),
            M(r'a_{n+1} < a_n'),
            M(r'a_{n+1} = -a_n')
        ],
        'ស្វ៊ីតកើនកាលណាតួបន្ទាប់ធំជាងឬស្មើនឹងតួមុនជានិច្ច ' + M(r'a_{n+1} \ge a_n') + '។'
    ))

    C.append(mcq(
        'easy', 'sec3_def_dec',
        'ស្វ៊ីត ' + M('(a_n)') + ' ជា «ស្វ៊ីតចុះ» លុះត្រាតែចំពោះគ្រប់ ' + M(r'n \in \mathbb{N}') + ' ៖',
        M(r'a_{n+1} \le a_n'),
        [
            M(r'a_{n+1} \ge a_n'),
            M(r'a_{n+1} > a_n'),
            M('a_{n+1} = a_n + 1')
        ],
        'ស្វ៊ីតចុះកាលណាតួបន្ទាប់តូចជាងឬស្មើនឹងតួមុនជានិច្ច ' + M(r'a_{n+1} \le a_n') + '។'
    ))

    C.append(mcq(
        'easy', 'sec3_def_mono',
        'ស្វ៊ីត ' + M('(a_n)') + ' មួយត្រូវបានហៅថា «ស្វ៊ីតម៉ូណូតូន» កាលណា ៖',
        'វាជាស្វ៊ីតកើន ឬជាស្វ៊ីតចុះ',
        [
            'វាមានតួទាំងអស់ជាចំនួនវិជ្ជមាន',
            'វាជាស្វ៊ីតរាប់អស់',
            'វាមានតួឆ្លាស់សញ្ញា'
        ],
        'តាមនិយមន័យ ស្វ៊ីតម៉ូណូតូនគឺជាស្វ៊ីតដែលកើន ឬជាស្វ៊ីតចុះ។'
    ))

    # =========================================================================
    # 2. MCQ - MEDIUM (14 items)
    # =========================================================================
    C.append(mcq(
        'medium', 'sec1_alt_term',
        'គេមានស្វ៊ីត ' + M(r'a_n = \dfrac{(-1)^{n+1}}{n+1}') + '។ គណនាតម្លៃនៃតួទី 4 (' + M('a_4') + ') ៖',
        M(r'-\dfrac{1}{5}'),
        [
            M(r'\dfrac{1}{5}'),
            M(r'-\dfrac{1}{4}'),
            M(r'\dfrac{1}{4}')
        ],
        'ជំនួស ' + M('n = 4') + ' គេបាន ' + M(r'a_4 = \dfrac{(-1)^5}{4+1} = -\dfrac{1}{5}') + '។'
    ))

    C.append(mcq(
        'medium', 'sec1_eval_frac5',
        'គេមានស្វ៊ីត ' + M(r'a_n = \dfrac{n}{n+1}') + '។ គណនាតម្លៃនៃតួទី 5 (' + M('a_5') + ') ៖',
        M(r'\dfrac{5}{6}'),
        [
            M(r'\dfrac{6}{5}'),
            M(r'\dfrac{4}{5}'),
            M(r'\dfrac{5}{7}')
        ],
        'ជំនួស ' + M('n = 5') + ' គេបាន ' + M(r'a_5 = \dfrac{5}{5+1} = \dfrac{5}{6}') + '។'
    ))

    C.append(mcq(
        'medium', 'sec2_quad_pattern',
        'កំណត់តួទី ' + M('n') + ' នៃស្វ៊ីត ' + M(r'3, 8, 15, 24, 35, \dots') + ' ៖',
        M('a_n = n(n+2)'),
        [
            M('a_n = n(n+1)'),
            M('a_n = 2n^2 + 1'),
            M('a_n = n^2 + 1')
        ],
        'តួនីមួយៗគឺ ' + M(r'1(3)=3, 2(4)=8, 3(5)=15, \dots') + ' នាំឱ្យ ' + M('a_n = n(n+2) = n^2 + 2n') + '។'
    ))

    C.append(mcq(
        'medium', 'sec2_cube_term',
        'ស្វ៊ីតនៃចំនួនគូប ' + M(r'1, 8, 27, 64, \dots') + ' មានតួទី 5 ស្មើនឹង ៖',
        M('125'),
        [M('100'), M('81'), M('216')],
        'តួទី 5 គឺ ' + M('5^3 = 125') + '។'
    ))

    C.append(mcq(
        'medium', 'sec2_frac_pattern1',
        'កំណត់តួទី ' + M('n') + ' នៃស្វ៊ីត ' + M(r'\dfrac{2}{3}, \dfrac{3}{4}, \dfrac{4}{5}, \dfrac{5}{6}, \dots') + ' ៖',
        M(r'a_n = \dfrac{n+1}{n+2}'),
        [
            M(r'a_n = \dfrac{n}{n+1}'),
            M(r'a_n = \dfrac{n+2}{n+1}'),
            M(r'a_n = \dfrac{n+1}{n+3}')
        ],
        'ភាគយកគឺ ' + M('n+1') + ' ហើយភាគបែងគឺ ' + M('n+2') + ' នាំឱ្យ ' + M(r'a_n = \dfrac{n+1}{n+2}') + '។'
    ))

    C.append(mcq(
        'medium', 'sec2_arith_pos',
        'កំណត់តួទី ' + M('n') + ' នៃស្វ៊ីត ' + M(r'5, 7, 9, 11, 13, \dots') + ' ៖',
        M('a_n = 2n + 3'),
        [
            M('a_n = 2n + 5'),
            M('a_n = 2n + 1'),
            M('a_n = 3n + 2')
        ],
        'ផលសង ' + M('d = 2') + ' នាំឱ្យ ' + M('a_n = 5 + 2(n - 1) = 2n + 3') + '។'
    ))

    C.append(mcq(
        'medium', 'sec2_arith_neg',
        'កំណត់តួទី ' + M('n') + ' នៃស្វ៊ីត ' + M(r'16, 13, 10, 7, 4, \dots') + ' ៖',
        M('a_n = 19 - 3n'),
        [
            M('a_n = 16 - 3n'),
            M('a_n = 19 + 3n'),
            M('a_n = 13 - 3n')
        ],
        'ផលសង ' + M('d = -3') + ' នាំឱ្យ ' + M('a_n = 16 - 3(n - 1) = 19 - 3n') + '។'
    ))

    C.append(mcq(
        'medium', 'sec3_diff_lin',
        'ពិនិត្យស្វ៊ីត ' + M('a_n = 5n - 3') + '។ គណនាផលសង ' + M('a_{n+1} - a_n') + ' ដើម្បីបង្ហាញអថេរភាព ៖',
        M('a_{n+1} - a_n = 5 > 0') + ' (ស្វ៊ីតកើន)',
        [
            M('a_{n+1} - a_n = -5 < 0') + ' (ស្វ៊ីតចុះ)',
            M('a_{n+1} - a_n = 2 > 0') + ' (ស្វ៊ីតកើន)',
            M('a_{n+1} - a_n = 0') + ' (ស្វ៊ីតថេរ)'
        ],
        'ផលសង ' + M('a_{n+1} - a_n = [5(n+1)-3] - (5n-3) = 5 > 0') + ' នាំឱ្យវាជាស្វ៊ីតកើន។'
    ))

    C.append(mcq(
        'medium', 'sec3_lin_dec',
        'ពិនិត្យស្វ៊ីត ' + M('b_n = 20 - 4n') + '។ តើស្វ៊ីតនេះជាស្វ៊ីតប្រភេទណា?',
        'ស្វ៊ីតចុះ',
        [
            'ស្វ៊ីតកើន',
            'ស្វ៊ីតថេរ',
            'មិនមែនជាស្វ៊ីតម៉ូណូតូន'
        ],
        'ផលសង ' + M('b_{n+1} - b_n = -4 < 0') + ' នាំឱ្យវាជាស្វ៊ីតចុះ។'
    ))

    C.append(with_img(mcq(
        'medium', 'sec3_frac_dec',
        'ពិនិត្យស្វ៊ីត ' + M(r'c_n = \dfrac{1}{n+3}') + ' ចំពោះ ' + M(r'n \ge 1') + '។ តើស្វ៊ីតនេះជាស្វ៊ីតប្រភេទណា?',
        'ស្វ៊ីតចុះ',
        [
            'ស្វ៊ីតកើន',
            'ស្វ៊ីតថេរ',
            'ស្វ៊ីតឆ្លាស់'
        ],
        'ផលសង ' + M(r'c_{n+1} - c_n = \dfrac{1}{n+4} - \dfrac{1}{n+3} = -\dfrac{1}{(n+3)(n+4)} < 0') + ' នាំឱ្យវាជាស្វ៊ីតចុះ។'
    ), FIG_MONOTONIC_GRAPH))

    C.append(mcq(
        'medium', 'sec3_homographic_inc',
        'ពិនិត្យស្វ៊ីត ' + M(r'a_n = \dfrac{2n+1}{n+3}') + '។ តើស្វ៊ីតនេះជាស្វ៊ីតម៉ូណូតូនដែរឬទេ?',
        'ជាស្វ៊ីតម៉ូណូតូនកើន',
        [
            'ជាស្វ៊ីតម៉ូណូតូនចុះ',
            'មិនមែនជាស្វ៊ីតម៉ូណូតូនទេ',
            'ជាស្វ៊ីតថេរ'
        ],
        'ផលសង ' + M(r'a_{n+1} - a_n = \dfrac{5}{(n+3)(n+4)} > 0') + ' នាំឱ្យជាស្វ៊ីតកើន ដូចនេះវាជាស្វ៊ីតម៉ូណូតូន។'
    ))

    C.append(mcq(
        'medium', 'sec3_alt_not_mono',
        'តើស្វ៊ីត ' + M(r'a_n = (-1)^n \dfrac{1}{n}') + ' (' + M(r'-1, \dfrac{1}{2}, -\dfrac{1}{3}, \dfrac{1}{4}, \dots') + ') ជាស្វ៊ីតម៉ូណូតូនដែរឬទេ?',
        'មិនមែនទេ ព្រោះតួឆ្លាស់សញ្ញា',
        [
            'ជាស្វ៊ីតម៉ូណូតូនកើន',
            'ជាស្វ៊ីតម៉ូណូតូនចុះ',
            'ជាស្វ៊ីតថេរ'
        ],
        'ស្វ៊ីតឆ្លាស់សញ្ញាមិនកើន មិនចុះ ដូច្នេះមិនមែនជាស្វ៊ីតម៉ូណូតូនឡើយ។'
    ))

    C.append(mcq(
        'medium', 'sec2_arith_neg2',
        'កំណត់តួទី ' + M('n') + ' នៃស្វ៊ីត ' + M(r'-3, -1, 1, 3, 5, \dots') + ' ៖',
        M('a_n = 2n - 5'),
        [
            M('a_n = 2n - 3'),
            M('a_n = 2n - 1'),
            M('a_n = 3n - 6')
        ],
        'ផលសង ' + M('d = 2') + ' នាំឱ្យ ' + M('a_n = -3 + 2(n - 1) = 2n - 5') + '។'
    ))

    C.append(mcq(
        'medium', 'sec1_pow_eval',
        'គេមានស្វ៊ីត ' + M('b_n = 2^{-n+2}') + '។ គណនាតម្លៃនៃតួទី 3 (' + M('b_3') + ') ៖',
        M(r'\dfrac{1}{2}'),
        [
            M('1'),
            M(r'\dfrac{1}{4}'),
            M('2')
        ],
        'ជំនួស ' + M('n = 3') + ' នាំឱ្យ ' + M(r'b_3 = 2^{-3+2} = 2^{-1} = \dfrac{1}{2}') + '។'
    ))

    # =========================================================================
    # 3. MCQ - HARD (7 items)
    # =========================================================================
    C.append(mcq(
        'hard', 'sec1_recur_sq',
        'ស្វ៊ីតកំណត់ដោយ ' + M('a_1 = 2') + ' និង ' + M('a_{n+1} = a_n^2') + '។ រកតម្លៃនៃតួទី 4 (' + M('a_4') + ') ៖',
        M('256'),
        [M('16'), M('64'), M('512')],
        'គណនាតាមលំដាប់ ' + M('a_1 = 2, a_2 = 2^2 = 4, a_3 = 4^2 = 16, a_4 = 16^2 = 256') + '។'
    ))

    C.append(mcq(
        'hard', 'sec3_ratio_exp_n',
        'គេមានស្វ៊ីត ' + M(r'a_n = \dfrac{2^n}{n}') + ' ចំពោះ ' + M(r'n \ge 1') + '។ គណនាផលធៀប ' + M(r'\dfrac{a_{n+1}}{a_n}') + ' ៖',
        M(r'\dfrac{2n}{n+1}'),
        [
            M(r'\dfrac{2(n+1)}{n}'),
            M(r'\dfrac{n}{n+1}'),
            M(r'\dfrac{2}{n+1}')
        ],
        'ផលធៀប ' + M(r'\dfrac{a_{n+1}}{a_n} = \dfrac{\frac{2^{n+1}}{n+1}}{\frac{2^n}{n}} = \dfrac{2^{n+1}}{2^n} \times \dfrac{n}{n+1} = \dfrac{2n}{n+1}') + '។'
    ))

    C.append(mcq(
        'hard', 'sec3_recur_inc',
        'ស្វ៊ីត ' + M('(a_n)') + ' កំណត់ដោយ ' + M('a_1 = 1') + ' និង ' + M('a_{n+1} = a_n^2 + a_n + 1') + '។ តើ ' + M('(a_n)') + ' មានអថេរភាពដូចម្តេច?',
        'ជាស្វ៊ីតកើនដាច់ខាត (' + M('a_{n+1} - a_n = a_n^2 + 1 > 0') + ')',
        [
            'ជាស្វ៊ីតចុះ (' + M('a_{n+1} < a_n') + ')',
            'ជាស្វ៊ីតថេរ (' + M('a_{n+1} = a_n') + ')',
            'មិនអាចកំណត់បាន'
        ],
        'ផលសង ' + M(r'a_{n+1} - a_n = a_n^2 + 1 \ge 1 > 0') + ' ចំពោះគ្រប់ ' + M(r'n \in \mathbb{N}') + ' នាំឱ្យវាជាស្វ៊ីតកើនដាច់ខាត។'
    ))

    C.append(mcq(
        'hard', 'sec3_quad_frac_dec',
        'ពិនិត្យស្វ៊ីត ' + M(r'a_n = \dfrac{n}{n^2+1}') + ' ចំពោះ ' + M(r'n \ge 1') + '។ តើស្វ៊ីតនេះមានអថេរភាពយ៉ាងដូចម្តេច?',
        'ជាស្វ៊ីតចុះចំពោះគ្រប់ ' + M(r'n \ge 1'),
        [
            'ជាស្វ៊ីតកើនចំពោះគ្រប់ ' + M(r'n \ge 1'),
            'ជាស្វ៊ីតថេរ',
            'កើនហើយចុះ'
        ],
        'ផលសង ' + M(r'a_{n+1} - a_n = \dfrac{1 - n - n^2}{(n^2+1)((n+1)^2+1)} < 0') + ' ចំពោះគ្រប់ ' + M(r'n \ge 1') + ' នាំឱ្យជាស្វ៊ីតចុះ។'
    ))

    C.append(mcq(
        'hard', 'sec2_pyramid_sum',
        'គេមានស្វ៊ីតនៃផលបូកការេ ' + M(r'1, 5, 14, 30, 55, \dots') + '។ រកតម្លៃនៃតួបន្ទាប់ (តួទី 6) ៖',
        M('91'),
        [M('85'), M('90'), M('96')],
        'ផលសងតួបន្តបន្ទាប់គឺ ' + M(r'4, 9, 16, 25') + ' (ការេនៃចំនួនគត់)។ ផលសងបន្ទាប់គឺ ' + M('6^2 = 36') + ' នាំឱ្យ ' + M('a_6 = 55 + 36 = 91') + '។'
    ))

    C.append(mcq(
        'hard', 'sec3_cubic_diff',
        'ស្វ៊ីត ' + M('a_n = n^3 + 4n - 5') + '។ គណនាផលសង ' + M('a_{n+1} - a_n') + ' ៖',
        M('3n^2 + 3n + 5'),
        [
            M('3n^2 + 4'),
            M('3n^2 + 3n + 4'),
            M('n^2 + 4n')
        ],
        'ផលសង ' + M('(n+1)^3 - n^3 = 3n^2 + 3n + 1') + ' ហើយ ' + M('4(n+1) - 4n = 4') + ' នាំឱ្យ ' + M('a_{n+1} - a_n = 3n^2 + 3n + 5 > 0') + '។'
    ))

    C.append(mcq(
        'hard', 'sec3_ratio_fact',
        'ស្វ៊ីត ' + M(r'a_n = \dfrac{3^n}{n!}') + '។ គណនាផលធៀប ' + M(r'\dfrac{a_{n+1}}{a_n}') + ' ៖',
        M(r'\dfrac{3}{n+1}'),
        [
            M(r'\dfrac{3}{n}'),
            M(r'\dfrac{3n}{n+1}'),
            M(r'\dfrac{1}{n+1}')
        ],
        'ផលធៀប ' + M(r'\dfrac{a_{n+1}}{a_n} = \dfrac{\frac{3^{n+1}}{(n+1)!}}{\frac{3^n}{n!}} = \dfrac{3^{n+1}}{3^n} \times \dfrac{n!}{(n+1)!} = \dfrac{3}{n+1}') + '។'
    ))

    # =========================================================================
    # 4. MCQ - PISA (5 items)
    # =========================================================================
    C.append(with_img(mcq(
        'pisa', 'pisa_ball_drop',
        'បាល់មួយទម្លាក់ពីកម្ពស់ ' + M(r'6\text{ m}') + ' ហើយពេលធ្លាក់ដល់ដី វាតែងតែលោតឡើងវិញបាន ' + M(r'\dfrac{2}{3}') + ' នៃកម្ពស់ធ្លាក់។ គណនាកម្ពស់បាល់លោតឡើងលើកទី 3 (' + M('a_3') + ') ៖',
        M(r'\dfrac{16}{9}\text{ m}'),
        [
            M(r'\dfrac{8}{3}\text{ m}'),
            M(r'4\text{ m}'),
            M(r'\dfrac{32}{27}\text{ m}')
        ],
        'កម្ពស់លោតលើកទី 3 គឺ ' + M(r'a_3 = 6 \times \left(\dfrac{2}{3}\right)^3 = 6 \times \dfrac{8}{27} = \dfrac{16}{9}\text{ m}') + ' (ប្រហែល ' + M(r'1.78\text{ m}') + ')។'
    ), FIG_BOUNCING_BALL))

    C.append(mcq(
        'pisa', 'pisa_bacteria',
        'បាក់តេរីមួយប្រភេទបំបែកខ្លួនទ្វេដងរៀងរាល់ 1 ម៉ោង។ ដំបូងមាន 100 កោសិកា។ ចំនួនបាក់តេរីនៅម៉ោងទី ' + M('n') + ' គឺ ' + M(r'a_n = 100 \times 2^n') + '។ នៅម៉ោងទី 5 ចំនួនបាក់តេរីកើនដល់ ៖',
        '3,200 កោសិកា',
        [
            '1,600 កោសិកា',
            '6,400 កោសិកា',
            '1,000 កោសិកា'
        ],
        'ចំនួនបាក់តេរី ' + M(r'a_5 = 100 \times 2^5 = 100 \times 32 = 3\,200') + ' កោសិកា។'
    ))

    C.append(mcq(
        'pisa', 'pisa_piggy_bank',
        'សុខាសន្សំប្រាក់ក្នុងកូនជ្រូក៖ ខែទី 1 សន្សំ 10,000 រៀល ហើយខែនីមួយៗបន្ទាប់សន្សំបន្ថែម 5,000 រៀលលើខែមុន (' + M(r'a_n = 5\,000n + 5\,000') + ')។ នៅខែទី 12 សុខាសន្សំប្រាក់ក្នុងខែនោះបានចំនួន ៖',
        '65,000 រៀល',
        [
            '60,000 រៀល',
            '70,000 រៀល',
            '55,000 រៀល'
        ],
        'ប្រាក់សន្សំក្នុងខែទី 12 គឺ ' + M(r'a_{12} = 5\,000(12) + 5\,000 = 60\,000 + 5\,000 = 65\,000') + ' រៀល។'
    ))

    C.append(mcq(
        'pisa', 'pisa_car_depreciation',
        'រថយន្តមួយទិញក្នុងតម្លៃ 20,000 ដុល្លារ ($)។ តម្លៃរបស់វាថយចុះ 10% រៀងរាល់ឆ្នាំ (នៅសល់ 90% នៃឆ្នាំមុន)។ តម្លៃរថយន្តនៅចុងឆ្នាំទី 2 គឺ ៖',
        '16,200 ដុល្លារ',
        [
            '18,000 ដុល្លារ',
            '16,000 ដុល្លារ',
            '14,400 ដុល្លារ'
        ],
        'ចុងឆ្នាំទី 1 តម្លៃនៅសល់ ' + M(r'20\,000 \times 0.9 = 18\,000') + '$។ ចុងឆ្នាំទី 2 តម្លៃនៅសល់ ' + M(r'18\,000 \times 0.9 = 16\,200') + '$។'
    ))

    C.append(mcq(
        'pisa', 'pisa_water_cooling',
        'សីតុណ្ហភាពទឹកក្តៅដែលត្រជាក់ចុះក្នុងបន្ទប់កំណត់ដោយ ' + M(r'T_n = 20 + 60(0.8)^n\ (^\circ\text{C})') + ' នៅនាទីទី ' + M('n') + '។ នៅនាទីទី 2 សីតុណ្ហភាពទឹកគឺ ៖',
        M(r'58.4^\circ\text{C}'),
        [
            M(r'68.0^\circ\text{C}'),
            M(r'50.0^\circ\text{C}'),
            M(r'48.4^\circ\text{C}')
        ],
        'សីតុណ្ហភាព ' + M(r'T_2 = 20 + 60(0.8)^2 = 20 + 60(0.64) = 20 + 38.4 = 58.4^\circ\text{C}') + '។'
    ))

    # =========================================================================
    # 5. WRITING - EASY (1 item)
    # =========================================================================
    C.append(writing(
        'easy', 'sec1_write_terms',
        'គេមានស្វ៊ីត ' + M('a_n = 3n + 2') + '។ ចូរគណនាបួនតួដំបូងនៃស្វ៊ីតនេះ (' + M('a_1, a_2, a_3, a_4') + ')។',
        [
            ('គណនាតួទី 1: a_1 = 3(1) + 2 = 5', 1),
            ('គណនាតួទី 2: a_2 = 3(2) + 2 = 8', 1),
            ('គណនាតួទី 3: a_3 = 3(3) + 2 = 11', 1),
            ('គណនាតួទី 4: a_4 = 3(4) + 2 = 14', 1),
            ('សន្និដ្ឋានបួនតួដំបូងនៃស្វ៊ីតគឺ 5, 8, 11, 14', 1)
        ]
    ))

    # =========================================================================
    # 6. WRITING - MEDIUM (4 items)
    # =========================================================================
    C.append(writing(
        'medium', 'sec2_write_formula',
        'កំណត់រូបមន្តតួទី ' + M('n') + ' (' + M('a_n') + ') នៃស្វ៊ីត ' + M(r'5, 8, 11, 14, 17, \dots') + ' ចំពោះគ្រប់ ' + M(r'n \in \mathbb{N}') + '។',
        [
            ('កំណត់តួដំបូង a_1 = 5', 1),
            ('គណនាផលសងរវាងពីរបន្តបន្ទាប់ d = 8 - 5 = 11 - 8 = 3', 1),
            ('សរសេររូបមន្តទូទៅ a_n = a_1 + (n - 1)d', 1),
            ('ជំនួសតម្លៃ a_n = 5 + 3(n - 1)', 1),
            ('សម្រួលកន្សោមបាន a_n = 3n + 2', 1)
        ]
    ))

    C.append(writing(
        'medium', 'sec3_write_dec_proof',
        'បង្ហាញថាស្វ៊ីត ' + M('(a_n)') + ' ដែល ' + M(r'a_n = \dfrac{1}{n+3}') + ' ជាស្វ៊ីតចុះចំពោះគ្រប់ ' + M(r'n \in \mathbb{N}') + '។',
        [
            ('កំណត់កន្សោម a_{n+1} = 1/(n+4)', 1),
            ('បង្កើតផលសង a_{n+1} - a_n = 1/(n+4) - 1/(n+3)', 1),
            ('តម្រូវភាគបែងរួម (n+3)(n+4)', 1),
            ('គណនាផលសងបាន (n+3 - (n+4))/((n+3)(n+4)) = -1/((n+3)(n+4))', 1),
            ('ដោយ -1 < 0 និង (n+3)(n+4) > 0 នាំឱ្យ a_{n+1} - a_n < 0 ដូច្នេះវាជាស្វ៊ីតចុះ', 1)
        ]
    ))

    C.append(writing(
        'medium', 'sec3_write_inc_proof',
        'បង្ហាញថាស្វ៊ីត ' + M('(b_n)') + ' ដែល ' + M(r'b_n = \dfrac{2n+1}{n+3}') + ' ជាស្វ៊ីតកើនចំពោះគ្រប់ ' + M(r'n \in \mathbb{N}') + '។',
        [
            ('កំណត់កន្សោម b_{n+1} = (2(n+1)+1)/((n+1)+3) = (2n+3)/(n+4)', 1),
            ('បង្កើតផលសង b_{n+1} - b_n = (2n+3)/(n+4) - (2n+1)/(n+3)', 1),
            ('តម្រូវភាគបែងរួមបាន [(2n+3)(n+3) - (2n+1)(n+4)] / [(n+3)(n+4)]', 1),
            ('ពន្លាតផលគុណភាគយក (2n^2 + 9n + 9) - (2n^2 + 9n + 4) = 5', 1),
            ('ផលសងស្មើ 5/((n+3)(n+4)) > 0 នាំឱ្យ b_{n+1} > b_n ដូច្នេះជាស្វ៊ីតកើន', 1)
        ]
    ))

    C.append(writing(
        'medium', 'sec3_write_ratio_mono',
        'សិក្សាភាពម៉ូណូតូននៃស្វ៊ីត ' + M(r'a_n = \dfrac{n}{n+1}') + ' ចំពោះគ្រប់ ' + M(r'n \in \mathbb{N}') + ' តាមវិធីផលធៀប ' + M(r'\dfrac{a_{n+1}}{a_n}') + '។',
        [
            ('បញ្ជាក់ថា a_n = n/(n+1) > 0 ចំពោះគ្រប់ n >= 1', 1),
            ('សរសេរកន្សោម a_{n+1} = (n+1)/(n+2) > 0', 1),
            ('បង្កើតផលធៀប a_{n+1}/a_n = [(n+1)/(n+2)] * [(n+1)/n] = (n+1)^2 / (n(n+2))', 1),
            ('ប្រៀបធៀប (n+1)^2 = n^2 + 2n + 1 > n^2 + 2n នាំឱ្យ a_{n+1}/a_n > 1', 1),
            ('សន្និដ្ឋានថា a_{n+1} > a_n នាំឱ្យស្វ៊ីតជាស្វ៊ីតកើន ដូចនេះវាជាស្វ៊ីតម៉ូណូតូន', 1)
        ]
    ))

    # =========================================================================
    # 7. WRITING - HARD (4 items)
    # =========================================================================
    C.append(writing(
        'hard', 'sec3_write_recur_induction',
        'គេមានស្វ៊ីត ' + M('(a_n)') + ' ដែល ' + M('a_1 = 1') + ' និង ' + M('a_{n+1} = a_n^2 + a_n + 1') + '។\n' +
        'ក. បង្ហាញថា ' + M('(a_n)') + ' ជាស្វ៊ីតកើន។\n' +
        'ខ. បង្ហាញថាចំពោះគ្រប់ ' + M(r'n \in \mathbb{N}') + ', ' + M(r'a_n \ge n') + '។',
        [
            ('គណនាផលសង a_{n+1} - a_n = a_n^2 + a_n + 1 - a_n = a_n^2 + 1', 1),
            ('ដោយ a_n^2 >= 0 នាំឱ្យ a_n^2 + 1 >= 1 > 0 នាំឱ្យ a_{n+1} > a_n ដូច្នេះជាស្វ៊ីតកើន', 1),
            ('ផ្ទៀងផ្ទាត់ចំពោះ n = 1: a_1 = 1 >= 1 (ពិត)', 1),
            ('ឧបមាថាពិតដល់ n = k គឺ a_k >= k', 1),
            ('ចំពោះ n = k+1: a_{k+1} = a_k^2 + a_k + 1 >= k^2 + k + 1 > k + 1 នាំឱ្យពិតចំពោះគ្រប់ n', 1)
        ]
    ))

    C.append(writing(
        'hard', 'sec3_write_cubic_proof',
        'បង្ហាញថាស្វ៊ីត ' + M('a_n = n^3 + 4n - 5') + ' ជាស្វ៊ីតកើនដាច់ខាតចំពោះគ្រប់ ' + M(r'n \in \mathbb{N}') + '។',
        [
            ('សរសេរកន្សោម a_{n+1} = (n+1)^3 + 4(n+1) - 5', 1),
            ('បង្កើតផលសង a_{n+1} - a_n = [(n+1)^3 - n^3] + [4(n+1) - 4n]', 1),
            ('ពន្លាត (n+1)^3 - n^3 = 3n^2 + 3n + 1', 1),
            ('គណនាផលបូក 3n^2 + 3n + 1 + 4 = 3n^2 + 3n + 5', 1),
            ('ដោយ n >= 1 នាំឱ្យ 3n^2 + 3n + 5 > 0 ដូច្នេះ a_{n+1} > a_n ជាស្វ៊ីតកើនដាច់ខាត', 1)
        ]
    ))

    C.append(writing(
        'hard', 'sec1_write_tower_formula',
        'គេមានស្វ៊ីតកំណត់ដោយ ' + M('a_1 = 2') + ' និង ' + M('a_{n+1} = a_n^2') + '។ រករូបមន្តតួទី ' + M('n') + ' (' + M('a_n') + ') នៃស្វ៊ីតនេះ។',
        [
            ('គណនាតួដំបូង a_1 = 2 = 2^{2^0}', 1),
            ('គណនាតួទីពីរ a_2 = a_1^2 = 2^2 = 2^{2^1} = 4', 1),
            ('គណនាតួទីបី a_3 = a_2^2 = (2^2)^2 = 2^4 = 2^{2^2} = 16', 1),
            ('គណនាតួទីបួន a_4 = a_3^2 = (2^4)^2 = 2^8 = 2^{2^3} = 256', 1),
            ('តាមលំនាំ និទស្សន្តគឺ 2^{n-1} ដូច្នេះរូបមន្តតួទី n គឺ a_n = 2^{2^{n-1}}', 1)
        ]
    ))

    C.append(writing(
        'hard', 'sec3_write_exp_proof',
        'បង្ហាញថាស្វ៊ីត ' + M(r'a_n = \dfrac{2^n}{n}') + ' ជាស្វ៊ីតកើនចំពោះគ្រប់ ' + M(r'n \ge 1') + '។',
        [
            ('បញ្ជាក់ថាគ្រប់តួ a_n = 2^n / n > 0 ចំពោះគ្រប់ n >= 1', 1),
            ('បង្កើតផលធៀប a_{n+1} / a_n = [2^{n+1} / (n+1)] / [2^n / n]', 1),
            ('សម្រួលកន្សោមបាន [2^{n+1}/2^n] * [n/(n+1)] = 2n / (n+1)', 1),
            ('ពិនិត្យវិសមភាព 2n - (n+1) = n - 1 >= 0 ចំពោះគ្រប់ n >= 1 នាំឱ្យ 2n >= n+1', 1),
            ('ដូច្នេះ a_{n+1}/a_n >= 1 នាំឱ្យ a_{n+1} >= a_n ដូចនេះវាជាស្វ៊ីតកើន', 1)
        ]
    ))

    # =========================================================================
    # 8. WRITING - PISA (5 items)
    # =========================================================================
    C.append(with_img(writing(
        'pisa', 'pisa_write_ball',
        'បាល់មួយត្រូវបានទម្លាក់ពីកម្ពស់ ' + M(r'6\text{ m}') + '។ រាល់ពេលធ្លាក់ដល់ដី វាតែងតែលោតឡើងលើវិញបាន ' + M(r'\dfrac{2}{3}') + ' នៃកម្ពស់ធ្លាក់។\n' +
        'ក. កំណត់រូបមន្តកម្ពស់បាល់ពេលលោតឡើងលើកទី ' + M('n') + ' (' + M('a_n') + ')។\n' +
        'ខ. គណនាកម្ពស់បាល់ពេលលោតឡើងលើកទី 3 (' + M('a_3') + ')។',
        [
            ('គណនាកម្ពស់លោតលើកទី 1: a_1 = 6 * (2/3) = 4 m', 1),
            ('គណនាកម្ពស់លោតលើកទី 2: a_2 = 4 * (2/3) = 6 * (2/3)^2 = 8/3 m', 1),
            ('សន្និដ្ឋានរូបមន្តកម្ពស់លោតលើកទី n: a_n = 6 * (2/3)^n m', 1),
            ('គណនាកម្ពស់លោតលើកទី 3: a_3 = 6 * (2/3)^3 = 6 * (8/27) = 16/9 m', 1),
            ('បំប្លែងតម្លៃជាប្រភាគ និងទសភាគ: 16/9 m ប្រហែល 1.78 m', 1)
        ]
    ), FIG_BOUNCING_BALL))

    C.append(writing(
        'pisa', 'pisa_write_population',
        'ទីក្រុងមួយមានប្រជាជនបច្ចុប្បន្ន 500,000 នាក់។ តាមការព្យាករណ៍ ចំនួនប្រជាជនកើនឡើង 2% រៀងរាល់ឆ្នាំ។\n' +
        'ក. សរសេររូបមន្តចំនួនប្រជាជនក្រោយ ' + M('n') + ' ឆ្នាំ (' + M('P_n') + ')។\n' +
        'ខ. គណនាចំនួនប្រជាជនក្រោយរយៈពេល 2 ឆ្នាំ។',
        [
            ('កំណត់កត្តាកំណើនប្រចាំឆ្នាំ: 1 + 2% = 1 + 0.02 = 1.02', 1),
            ('គណនាចំនួនប្រជាជនក្រោយ 1 ឆ្នាំ: P_1 = 500,000 * 1.02 = 510,000 នាក់', 1),
            ('សរសេររូបមន្តចំនួនប្រជាជនក្រោយ n ឆ្នាំ: P_n = 500,000 * (1.02)^n នាក់', 1),
            ('គណនាចំនួនប្រជាជនក្រោយ 2 ឆ្នាំ: P_2 = 500,000 * (1.02)^2 = 520,200 នាក់', 1),
            ('សន្និដ្ឋានចំនួនប្រជាជនកើនឡើងបាន 20,200 នាក់ក្នុងរយៈពេល 2 ឆ្នាំ', 1)
        ]
    ))

    C.append(writing(
        'pisa', 'pisa_write_pond',
        'ក្រុមកម្មករជីកស្រះមួយ៖ ថ្ងៃទី 1 ជីកបាន ' + M(r'12\text{ m}^3') + ' ថ្ងៃទី 2 បាន ' + M(r'15\text{ m}^3') + ' ថ្ងៃទី 3 បាន ' + M(r'18\text{ m}^3') + '។\n' +
        'ក. កំណត់រូបមន្តបរិមាណដីជីកបាននៅថ្ងៃទី ' + M('n') + ' (' + M('V_n') + ')។\n' +
        'ខ. គណនាបរិមាណដីដែលជីកបាននៅថ្ងៃទី 10។',
        [
            ('កំណត់បរិមាណដីថ្ងៃដំបូង V_1 = 12 m^3 និងកំណើនប្រចាំថ្ងៃ d = 15 - 12 = 3 m^3', 1),
            ('សរសេររូបមន្តទូទៅ V_n = V_1 + (n - 1)d', 1),
            ('ជំនួសតម្លៃ V_n = 12 + 3(n - 1) = 3n + 9 m^3', 1),
            ('គណនាបរិមាណដីនៅថ្ងៃទី 10: V_{10} = 3(10) + 9 = 39 m^3', 1),
            ('សន្និដ្ឋាននៅថ្ងៃទី 10 ជីកបាន 39 ម៉ែត្រគូប', 1)
        ]
    ))

    C.append(writing(
        'pisa', 'pisa_write_medicine',
        'អ្នកជំងឺម្នាក់បានលេបថ្នាំមួយគ្រាប់ទំហំ ' + M(r'500\text{ mg}') + '។ រៀងរាល់ 4 ម៉ោង បរិមាណថ្នាំក្នុងឈាមថយចុះ 30% (នៅសល់ 70%)។\n' +
        'ក. សរសេររូបមន្តបរិមាណថ្នាំដែលនៅសល់ក្រោយពេលលេបបាន ' + M('4n') + ' ម៉ោង (' + M('M_n') + ')។\n' +
        'ខ. គណនាបរិមាណថ្នាំដែលនៅសល់ក្រោយពេលលេបបាន 8 ម៉ោង។',
        [
            ('កំណត់បរិមាណដើម 500 mg និងអត្រានៅសល់ 1 - 0.30 = 0.70', 1),
            ('គណនាបរិមាណក្រោយ 4 ម៉ោង (n=1): M_1 = 500 * 0.7 = 350 mg', 1),
            ('សរសេររូបមន្តក្រោយ 4n ម៉ោង: M_n = 500 * (0.7)^n mg', 1),
            ('ក្រោយ 8 ម៉ោងត្រូវនឹង n = 2: M_2 = 500 * (0.7)^2 = 500 * 0.49 = 245 mg', 1),
            ('សន្និដ្ឋានបរិមាណថ្នាំនៅសល់ក្រោយ 8 ម៉ោងគឺ 245 mg', 1)
        ]
    ))

    C.append(writing(
        'pisa', 'pisa_write_tree',
        'កូនឈើមួយដើមពេលដាំមានកម្ពស់ ' + M(r'1.2\text{ m}') + ' ហើយជារៀងរាល់ខែវាលូតលាស់ខ្ពស់ជាងមុន ' + M(r'0.15\text{ m}') + '។\n' +
        'ក. សរសេររូបមន្តកម្ពស់ដើមឈើនៅខែទី ' + M('n') + ' (' + M('H_n') + ')។\n' +
        'ខ. តើក្រោយពេលដាំបានប៉ុន្មានខែ ទើបដើមឈើនោះមានកម្ពស់ឡើងដល់ ' + M(r'3.0\text{ m}') + '?',
        [
            ('កំណត់កម្ពស់ដើម H_0 = 1.2 m និងកំណើនប្រចាំខែ 0.15 m', 1),
            ('សរសេររូបមន្តកម្ពស់នៅខែទី n: H_n = 1.2 + 0.15n (m)', 1),
            ('គណនាកម្ពស់ឡើងដល់ 3 m: កំណត់សមីការ 1.2 + 0.15n = 3.0', 1),
            ('ដោះស្រាយសមីការ: 0.15n = 3.0 - 1.2 = 1.8 នាំឱ្យ n = 1.8 / 0.15', 1),
            ('គណនាបាន n = 12 ដូច្នេះត្រូវការរយៈពេល 12 ខែ (1 ឆ្នាំ)', 1)
        ]
    ))

    return C
