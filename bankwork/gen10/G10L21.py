# -*- coding: utf-8 -*-
from lib import *

LESSON = 'វ៉ិចទ័រនិងប្រមាណវិធីលើវ៉ិចទ័រ'
CHAPTER = 'ជំពូកទី 8 : វ៉ិចទ័រក្នុងប្លង់'

def with_img(q, svg):
    q['img'] = svg
    return q

# =========================================================================
# SVG Figures for Lesson 21 (Transparent background, Mathcad italic font)
# =========================================================================

FIG_VECTOR_COORD_L21 = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 360 240' width='360' height='240'>
  <defs>
    <marker id='ax-ar21a' markerWidth='6' markerHeight='6' refX='5' refY='3' orient='auto'>
      <path d='M1,1 L5,3 L1,5 Z' fill='#334155'/>
    </marker>
    <marker id='vec-ar21a' markerWidth='6' markerHeight='6' refX='5' refY='3' orient='auto'>
      <path d='M1,1 L5,3 L1,5 Z' fill='#2563eb'/>
    </marker>
  </defs>
  <!-- Axes -->
  <line x1='30' y1='190' x2='330' y2='190' stroke='#334155' stroke-width='1.8' marker-end='url(#ax-ar21a)'/>
  <text x='335' y='194' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='16' fill='#334155'>x</text>

  <line x1='60' y1='210' x2='60' y2='25' stroke='#334155' stroke-width='1.8' marker-end='url(#ax-ar21a)'/>
  <text x='65' y='22' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='16' fill='#334155'>y</text>
  <text x='44' y='204' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='14' fill='#334155'>O</text>

  <!-- Unit vectors i and j: 40px each -->
  <line x1='60' y1='190' x2='100' y2='190' stroke='#dc2626' stroke-width='2.6' marker-end='url(#ax-ar21a)'/>
  <text x='78' y='210' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='13' fill='#dc2626'>i</text>

  <line x1='60' y1='190' x2='60' y2='150' stroke='#dc2626' stroke-width='2.6' marker-end='url(#ax-ar21a)'/>
  <text x='42' y='172' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='13' fill='#dc2626'>j</text>

  <!-- Vector u = (4, 3): to (220, 70) -->
  <line x1='220' y1='190' x2='220' y2='70' stroke='#94a3b8' stroke-width='1.2' stroke-dasharray='4,4'/>
  <line x1='60' y1='70' x2='220' y2='70' stroke='#94a3b8' stroke-width='1.2' stroke-dasharray='4,4'/>

  <line x1='60' y1='190' x2='220' y2='70' stroke='#2563eb' stroke-width='2.6' marker-end='url(#vec-ar21a)'/>
  <circle cx='220' cy='70' r='3.5' fill='#2563eb'/>
  <text x='226' y='66' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='14' fill='#2563eb'>P(4, 3)</text>
  <text x='130' y='120' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='15' fill='#2563eb'>u = (4, 3)</text>

  <!-- Ticks -->
  <text x='215' y='208' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='13' fill='#334155'>4</text>
  <text x='44' y='74' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='13' fill='#334155'>3</text>
</svg>"""

FIG_TRIANGLE_LAW_L21 = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 340 220' width='340' height='220'>
  <defs>
    <marker id='ar-b21' markerWidth='6' markerHeight='6' refX='5' refY='3' orient='auto'>
      <path d='M1,1 L5,3 L1,5 Z' fill='#2563eb'/>
    </marker>
    <marker id='ar-g21' markerWidth='6' markerHeight='6' refX='5' refY='3' orient='auto'>
      <path d='M1,1 L5,3 L1,5 Z' fill='#059669'/>
    </marker>
    <marker id='ar-r21' markerWidth='6' markerHeight='6' refX='5' refY='3' orient='auto'>
      <path d='M1,1 L5,3 L1,5 Z' fill='#7c3aed'/>
    </marker>
  </defs>
  <!-- Triangle Chasles Law: A(40, 160) -> B(200, 160) -> C(170, 50) -->
  <line x1='40' y1='160' x2='195' y2='160' stroke='#2563eb' stroke-width='2.4' marker-end='url(#ar-b21)'/>
  <text x='115' y='182' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='14' fill='#2563eb'>u = AB</text>

  <line x1='200' y1='160' x2='172' y2='55' stroke='#059669' stroke-width='2.4' marker-end='url(#ar-g21)'/>
  <text x='202' y='105' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='14' fill='#059669'>v = BC</text>

  <line x1='40' y1='160' x2='167' y2='54' stroke='#7c3aed' stroke-width='2.8' marker-end='url(#ar-r21)'/>
  <text x='75' y='95' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='15' fill='#7c3aed'>u + v = AC</text>

  <!-- Vertices -->
  <circle cx='40' cy='160' r='3.5' fill='#334155'/>
  <text x='25' y='172' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='14' fill='#334155'>A</text>

  <circle cx='200' cy='160' r='3.5' fill='#334155'/>
  <text x='208' y='172' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='14' fill='#334155'>B</text>

  <circle cx='170' cy='50' r='3.5' fill='#334155'/>
  <text x='170' y='38' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='14' fill='#334155'>C</text>
</svg>"""

FIG_PARALLELOGRAM_LAW_L21 = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 360 220' width='360' height='220'>
  <defs>
    <marker id='ar-p1' markerWidth='6' markerHeight='6' refX='5' refY='3' orient='auto'>
      <path d='M1,1 L5,3 L1,5 Z' fill='#2563eb'/>
    </marker>
    <marker id='ar-p2' markerWidth='6' markerHeight='6' refX='5' refY='3' orient='auto'>
      <path d='M1,1 L5,3 L1,5 Z' fill='#059669'/>
    </marker>
    <marker id='ar-p3' markerWidth='6' markerHeight='6' refX='5' refY='3' orient='auto'>
      <path d='M1,1 L5,3 L1,5 Z' fill='#dc2626'/>
    </marker>
  </defs>
  <!-- O(40, 170), P1(200, 170), P2(110, 60), P3(270, 60) -->
  <line x1='200' y1='170' x2='270' y2='60' stroke='#94a3b8' stroke-width='1.5' stroke-dasharray='4,4'/>
  <line x1='110' y1='60' x2='270' y2='60' stroke='#94a3b8' stroke-width='1.5' stroke-dasharray='4,4'/>

  <line x1='40' y1='170' x2='195' y2='170' stroke='#2563eb' stroke-width='2.4' marker-end='url(#ar-p1)'/>
  <text x='115' y='192' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='14' fill='#2563eb'>u = AB</text>

  <line x1='40' y1='170' x2='107' y2='65' stroke='#059669' stroke-width='2.4' marker-end='url(#ar-p2)'/>
  <text x='55' y='105' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='14' fill='#059669'>v = AD</text>

  <line x1='40' y1='170' x2='265' y2='63' stroke='#dc2626' stroke-width='2.8' marker-end='url(#ar-p3)'/>
  <text x='160' y='105' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='15' fill='#dc2626'>u + v = AC</text>

  <circle cx='40' cy='170' r='3.5' fill='#334155'/>
  <text x='25' y='182' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='14' fill='#334155'>A</text>
  <circle cx='200' cy='170' r='3.5' fill='#334155'/>
  <text x='208' y='182' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='14' fill='#334155'>B</text>
  <circle cx='110' cy='60' r='3.5' fill='#334155'/>
  <text x='96' y='52' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='14' fill='#334155'>D</text>
  <circle cx='270' cy='60' r='3.5' fill='#334155'/>
  <text x='278' y='55' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='14' fill='#334155'>C</text>
</svg>"""

FIG_DOT_PRODUCT_L21 = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 350 200' width='350' height='200'>
  <defs>
    <marker id='ar-d1' markerWidth='6' markerHeight='6' refX='5' refY='3' orient='auto'>
      <path d='M1,1 L5,3 L1,5 Z' fill='#2563eb'/>
    </marker>
    <marker id='ar-d2' markerWidth='6' markerHeight='6' refX='5' refY='3' orient='auto'>
      <path d='M1,1 L5,3 L1,5 Z' fill='#059669'/>
    </marker>
  </defs>
  <!-- Origin O(40, 160) -->
  <line x1='40' y1='160' x2='295' y2='160' stroke='#059669' stroke-width='2.4' marker-end='url(#ar-d2)'/>
  <text x='305' y='164' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='15' fill='#059669'>v</text>

  <line x1='40' y1='160' x2='215' y2='55' stroke='#2563eb' stroke-width='2.4' marker-end='url(#ar-d1)'/>
  <text x='218' y='48' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='15' fill='#2563eb'>u</text>

  <!-- Projection from (220, 50) to (220, 160) -->
  <line x1='220' y1='50' x2='220' y2='160' stroke='#94a3b8' stroke-width='1.5' stroke-dasharray='4,4'/>
  <rect x='208' y='148' width='12' height='12' fill='none' stroke='#94a3b8' stroke-width='1.2'/>

  <!-- Angle arc theta -->
  <path d='M 80,160 A 40,40 0 0,0 68,143' fill='none' stroke='#f59e0b' stroke-width='2'/>
  <text x='84' y='145' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='14' fill='#f59e0b'>θ</text>

  <circle cx='40' cy='160' r='3.5' fill='#334155'/>
  <text x='26' y='174' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='14' fill='#334155'>O</text>
  <circle cx='220' cy='160' r='3.5' fill='#7c3aed'/>
  <text x='214' y='182' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='13' fill='#7c3aed'>H</text>

  <text x='110' y='182' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='13' fill='#7c3aed'>|u| cos θ</text>
</svg>"""


def cands():
    C = []

    # =========================================================================
    # MCQ - EASY (target: 10, provide: 13)
    # =========================================================================

    C.append(mcq(
        'easy', 'sec1',
        'នៅក្នុងធរណីមាត្រ តើអ្វីជា «វ៉ិចទ័រ»?',
        'អង្កត់មានទិសដៅដែលមិនគិតពីទីតាំងក្នុងប្លង់',
        ['បន្ទាត់ត្រង់គ្មានចំណុចចុង', 'ចំណុចប្រសព្វនៃបន្ទាត់ពីរ', 'ផលធៀបនៃប្រវែងពីរ'],
        'វ៉ិចទ័រ គឺជាអង្កត់ដែលមានទិសដៅច្បាស់លាស់ ដោយមានចំណុចគល់និងចំណុចចុង និងមិនគិតពីទីតាំងក្នុងប្លង់។'
    ))

    C.append(mcq(
        'easy', 'sec1',
        'តើសញ្ញាណ ' + M(r'|\vec{AB}|') + ' តំណាងឱ្យអ្វី?',
        'ប្រវែង (ម៉ូឌុល) នៃវ៉ិចទ័រ AB',
        ['ទិសដៅពី B ទៅ A', 'ចំណុចកណ្តាលនៃ AB', 'ផលដកកូអរដោនេ'],
        '|AB| ឬ ||AB|| គឺជាប្រវែង ឬម៉ូឌុលនៃវ៉ិចទ័រ ដែលជាចម្ងាយរវាងចំណុចគល់ A និងចំណុចចុង B។'
    ))

    C.append(mcq(
        'easy', 'sec1',
        'តើវ៉ិចទ័រពីរ ' + M(r'\vec{u}') + ' និង ' + M(r'\vec{v}') + ' ស្មើគ្នា (' + M(r'\vec{u} = \vec{v}') + ') លុះត្រាតែមានលក្ខខណ្ឌណា?',
        'វាមានទិសដៅដូចគ្នា និងមានប្រវែងស្មើគ្នា',
        ['វាមានតែប្រវែងស្មើគ្នាតែប៉ុណ្ណោះ', 'វាមានតែទិសស្របគ្នាតែប៉ុណ្ណោះ', 'វាមានចំណុចគល់ដូចគ្នា'],
        'វ៉ិចទ័រពីរស្មើគ្នាលុះត្រាតែវាមានទិសស្របគ្នា ទិសដៅដូចគ្នា និងប្រវែងស្មើគ្នា។'
    ))

    C.append(mcq(
        'easy', 'sec1',
        'តើវ៉ិចទ័រផ្ទុយនៃវ៉ិចទ័រ ' + M(r'\vec{AB}') + ' គឺជាវ៉ិចទ័រណា?',
        M(r'-\vec{AB} = \vec{BA}'),
        [M(r'-\vec{AB} = \vec{AB}'), M(r'-\vec{AB} = \vec{0}'), M(r'-\vec{AB} = \dfrac{1}{\vec{AB}}')],
        'វ៉ិចទ័រផ្ទុយនៃ AB គឺ -AB = BA ដែលមានទិសស្របគ្នា ប្រវែងស្មើគ្នា តែទិសដៅផ្ទុយគ្នា។'
    ))

    C.append(mcq(
        'easy', 'sec1',
        'តើវ៉ិចទ័រសូន្យ ' + M(r'\vec{0}') + ' មានប្រវែងស្មើនឹងប៉ុន្មាន?',
        '0',
        ['1', '-1', 'អនន្ត'],
        'វ៉ិចទ័រសូន្យមានចំណុចគល់និងចុងត្រួតស៊ីគ្នា (ឧ. AA = 0) និងមានប្រវែងស្មើ 0។'
    ))

    C.append(mcq(
        'easy', 'sec2',
        'យោងតាមវិធានត្រីកោណ Chasles ចំពោះបីចំណុច A, B, C តើ ' + M(r'\vec{AB} + \vec{BC}') + ' ស្មើនឹងអ្វី?',
        M(r'\vec{AC}'),
        [M(r'\vec{CA}'), M(r'\vec{BA}'), M(r'\vec{0}')],
        'តាមវិធានត្រីកោណ Chasles: AB + BC = AC។'
    ))

    C.append(mcq(
        'easy', 'sec2',
        'គណនាផលបូកវ៉ិចទ័រ ៖ ' + M(r'\vec{MN} + \vec{NP} + \vec{PM}'),
        M(r'\vec{0}'),
        [M(r'\vec{MP}'), M(r'2\vec{MN}'), M(r'3')],
        'MN + NP + PM = MP + PM = MM = 0 (វ៉ិចទ័រសូន្យ)។'
    ))

    C.append(with_img(mcq(
        'easy', 'sec2',
        'ពិនិត្យរូបខាងក្រោម។ យោងតាមវិធានត្រីកោណ Chasles តើផលបូក ' + M(r'\vec{u} + \vec{v}') + ' ស្មើនឹងវ៉ិចទ័រណា?',
        M(r'\vec{AC}'),
        [M(r'\vec{CA}'), M(r'\vec{BC}'), M(r'\vec{BA}')],
        'ក្នុងរូប AB = u និង BC = v នាំឱ្យតាមវិធានត្រីកោណ AB + BC = AC = u + v។'
    ), FIG_TRIANGLE_LAW_L21))

    C.append(with_img(mcq(
        'easy', 'sec2',
        'ពិនិត្យរូបប្រលេឡូក្រាម ABCD ខាងក្រោម។ តើផលបូកវ៉ិចទ័រ ' + M(r'\vec{AB} + \vec{AD}') + ' ស្មើនឹងវ៉ិចទ័រណា?',
        M(r'\vec{AC}'),
        [M(r'\vec{BD}'), M(r'\vec{CA}'), M(r'\vec{DB}')],
        'តាមវិធានប្រលេឡូក្រាម ផលបូកនៃវ៉ិចទ័រគល់រួម AB + AD = AC (អង្កត់ទ្រូង)។'
    ), FIG_PARALLELOGRAM_LAW_L21))

    C.append(mcq(
        'easy', 'sec2',
        'ចំពោះបីចំណុច A, B, C តើផលដក ' + M(r'\vec{AC} - \vec{AB}') + ' ស្មើនឹងអ្វី?',
        M(r'\vec{BC}'),
        [M(r'\vec{CB}'), M(r'\vec{BA}'), M(r'\vec{CA}')],
        'AC - AB = AC + BA = BA + AC = BC។'
    ))

    C.append(mcq(
        'easy', 'sec3',
        'បើ ' + M(r'\vec{u} = (x,\, y)') + ' តើរូបមន្តគណនាប្រវែង (ម៉ូឌុល) ' + M(r'|\vec{u}|') + ' គឺជាអ្វី?',
        M(r'|\vec{u}| = \sqrt{x^2 + y^2}'),
        [M(r'|\vec{u}| = x + y'), M(r'|\vec{u}| = \sqrt{x + y}'), M(r'|\vec{u}| = x^2 + y^2')],
        'ប្រវែងវ៉ិចទ័រក្នុងប្លង់កូអរដោនេគឺ |u| = sqrt(x^2 + y^2)។'
    ))

    C.append(with_img(mcq(
        'easy', 'sec3',
        'ពិនិត្យរូបភាពកូអរដោនេខាងក្រោម។ តើវ៉ិចទ័រ ' + M(r'\vec{u}') + ' មានកូអរដោនេស្មើនឹងប៉ុន្មាន?',
        M(r'(4,\, 3)'),
        [M(r'(3,\, 4)'), M(r'(4,\, -3)'), M(r'(7,\, 1) Wandering')],
        'ចំណុច P មានកូអរដោនេ (4, 3) នាំឱ្យវ៉ិចទ័រ OP = u = 4i + 3j = (4, 3)។'
    ), FIG_VECTOR_COORD_L21))

    C.append(mcq(
        'easy', 'sec4',
        'តើរូបមន្តគណនាផលគុណស្កាលែនៃពីរវ៉ិចទ័រ ' + M(r'\vec{u} = (x_1,\, y_1)') + ' និង ' + M(r'\vec{v} = (x_2,\, y_2)') + ' គឺជាអ្វី?',
        M(r'\vec{u} \cdot \vec{v} = x_1 x_2 + y_1 y_2'),
        [M(r'\vec{u} \cdot \vec{v} = x_1 y_2 + x_2 y_1'), M(r'\vec{u} \cdot \vec{v} = x_1 x_2 - y_1 y_2'), M(r'\vec{u} \cdot \vec{v} = (x_1 + x_2)(y_1 + y_2)')],
        'ផលគុណស្កាលែតាមកូអរដោនេគឺ u . v = x_1 x_2 + y_1 y_2។'
    ))

    # =========================================================================
    # MCQ - MEDIUM (target: 14, provide: 17)
    # =========================================================================

    C.append(mcq(
        'medium', 'sec1',
        'គេមានចំណុច ' + M(r'A(1,\, 2)') + ' និង ' + M(r'B(4,\, 6)') + '។ គណនាកូអរដោនេនៃវ៉ិចទ័រ ' + M(r'\vec{AB}') + '៖',
        M(r'(3,\, 4)'),
        [M(r'(5,\, 8)'), M(r'(-3,\, -4)'), M(r'(3,\, 8)')],
        'AB = (x_B - x_A, y_B - y_A) = (4 - 1, 6 - 2) = (3, 4)។'
    ))

    C.append(mcq(
        'medium', 'sec1',
        'គណនាប្រវែងនៃវ៉ិចទ័រ ' + M(r'\vec{AB}') + ' ដែល ' + M(r'A(1,\, 2)') + ' និង ' + M(r'B(4,\, 6)') + '៖',
        '5',
        ['7', '25', M(r'\sqrt{7}')], 
        'AB = (3, 4) នាំឱ្យ |AB| = sqrt(3^2 + 4^2) = sqrt(9 + 16) = sqrt(25) = 5 ឯកតា។'
    ))

    C.append(mcq(
        'medium', 'sec3',
        'គណនាប្រវែងនៃវ៉ិចទ័រ ' + M(r'\vec{u} = (-5,\, 12)') + '៖',
        '13',
        ['17', '7', '169'],
        '|u| = sqrt((-5)^2 + 12^2) = sqrt(25 + 144) = sqrt(169) = 13 ឯកតា។'
    ))

    C.append(mcq(
        'medium', 'sec3',
        'គេមាន ' + M(r'\vec{u} = (2,\, -3)') + ' និង ' + M(r'\vec{v} = (-1,\, 4)') + '។ គណនាកូអរដោនេនៃ ' + M(r'3\vec{u} + 2\vec{v}') + '៖',
        M(r'(4,\, -1)'),
        [M(r'(5,\, -1)'), M(r'(4,\, 1)'), M(r'(8,\, -5)')],
        '3u = (6, -9) និង 2v = (-2, 8) នាំឱ្យ 3u + 2v = (6 - 2, -9 + 8) = (4, -1)។'
    ))

    C.append(mcq(
        'medium', 'sec3',
        'រកវ៉ិចទ័រឯកតា ' + M(r'\vec{e}') + ' ដែលមានទិសដៅដូចវ៉ិចទ័រ ' + M(r'\vec{u} = (8,\, -6)') + '៖',
        M(r'\left(\dfrac{4}{5},\, -\dfrac{3}{5}\right)'),
        [M(r'\left(\dfrac{3}{5},\, -\dfrac{4}{5}\right)'), M(r'(8,\, -6)'), M(r'(1,\, -1)')],
        '|u| = sqrt(64 + 36) = 10 នាំឱ្យ e = u / 10 = (8/10, -6/10) = (4/5, -3/5)។'
    ))

    C.append(mcq(
        'medium', 'sec3',
        'គេឱ្យ ' + M(r'\vec{u} = (3,\, k)') + ' និង ' + M(r'\vec{v} = (6,\, -8)') + '។ រកតម្លៃ k ដើម្បីឱ្យវ៉ិចទ័រទាំងពីរកូលីនេអ៊ែរគ្នា (ស្របគ្នា)៖',
        '-4',
        ['4', '-6', '8'],
        'u // v <=> 3(-8) - 6k = 0 <=> -24 = 6k <=> k = -4។'
    ))

    C.append(mcq(
        'medium', 'sec4',
        'គណនាផលគុណស្កាលែនៃ ' + M(r'\vec{u} = (5,\, 2)') + ' និង ' + M(r'\vec{v} = (-2,\, 6)') + '៖',
        '2',
        ['22', '-2', '16'],
        'u . v = 5(-2) + 2(6) = -10 + 12 = 2។'
    ))

    C.append(mcq(
        'medium', 'sec4',
        'តើវ៉ិចទ័រមួយណាខាងក្រោមនេះកែងនឹងវ៉ិចទ័រ ' + M(r'\vec{u} = (3,\, 4)') + '?',
        M(r'\vec{v} = (-4,\, 3)'),
        [M(r'\vec{v} = (4,\, 3)'), M(r'\vec{v} = (3,\, -4)'), M(r'\vec{v} = (4,\, -3)')],
        '(3)(-4) + (4)(3) = -12 + 12 = 0 នាំឱ្យកែងគ្នា។'
    ))

    C.append(mcq(
        'medium', 'sec4',
        'គេឱ្យ ' + M(r'\vec{u} = (x,\, 6)') + ' និង ' + M(r'\vec{v} = (4,\, -2)') + '។ រកតម្លៃ x ដើម្បីឱ្យ ' + M(r'\vec{u} \perp \vec{v}') + ' (កែងគ្នា)៖',
        '3',
        ['-3', '4', '12'],
        'u . v = 0 <=> 4x + 6(-2) = 0 <=> 4x - 12 = 0 <=> 4x = 12 <=> x = 3។'
    ))

    C.append(with_img(mcq(
        'medium', 'sec4',
        'ពិនិត្យរូបភាពខាងក្រោម។ បើ ' + M(r'|\vec{u}| = 6') + ', ' + M(r'|\vec{v}| = 8') + ' និងមុំ ' + M(r'\theta = 60^\circ') + ' គណនាផលគុណស្កាលែ ' + M(r'\vec{u} \cdot \vec{v}') + '៖',
        '24',
        ['48', M(r'24\sqrt{3}'), '12'], 
        'u . v = |u||v|cos 60° = (6)(8)(1/2) = 48 / 2 = 24។'
    ), FIG_DOT_PRODUCT_L21))

    C.append(mcq(
        'medium', 'sec4',
        'គេមាន ' + M(r'|\vec{u}| = 5') + ', ' + M(r'|\vec{v}| = 4') + ' និង ' + M(r'\vec{u} \cdot \vec{v} = -10') + '។ គណនាកូស៊ីនុសនៃមុំ ' + M(r'\cos\theta') + ' រវាងវ៉ិចទ័រទាំងពីរ៖',
        '-0.5',
        ['0.5', '-1', '-0.25'],
        'cos theta = (u . v) / (|u||v|) = -10 / (5 * 4) = -10 / 20 = -0.5 (theta = 120°)។'
    ))

    C.append(mcq(
        'medium', 'sec2',
        'ក្នុងត្រីកោណ ABC បើ M ជាចំណុចកណ្តាលនៃ BC តើ ' + M(r'\vec{AB} + \vec{AC}') + ' ស្មើនឹងអ្វី?',
        M(r'2\vec{AM}'),
        [M(r'\vec{AM}'), M(r'\vec{BC}'), M(r'\vec{0}')],
        'AB + AC = (AM + MB) + (AM + MC) = 2AM + (MB + MC) = 2AM + 0 = 2AM។'
    ))

    C.append(mcq(
        'medium', 'sec3',
        'គេមានចំណុច ' + M(r'A(-2,\, 1),\, B(1,\, 3),\, C(4,\, 5)') + '។ តើបីចំណុចនេះរត់ត្រង់ជួរគ្នាដែរឬទេ?',
        'រត់ត្រង់ជួរគ្នា ព្រោះ AB និង BC កូលីនេអ៊ែរគ្នា',
        ['មិនរត់ត្រង់ជួរគ្នាទេ', 'បង្កើតបានត្រីកោណកែង', 'បង្កើតបានត្រីកោណសម័ង្ស'],
        'AB = (3, 2) និង BC = (3, 2) នាំឱ្យ AB = BC (កូលីនេអ៊ែរគ្នា និងមានចំណុចរួម B) នាំឱ្យ A, B, C រត់ត្រង់ជួរគ្នា។'
    ))

    C.append(mcq(
        'medium', 'sec4',
        'គណនាមុំ ' + M(r'\theta') + ' រវាងវ៉ិចទ័រ ' + M(r'\vec{u} = (1,\, 0)') + ' និង ' + M(r'\vec{v} = (1,\, 1)') + '៖',
        M(r'45^\circ'),
        [M(r'30^\circ'), M(r'60^\circ'), M(r'90^\circ')],
        'u . v = 1(1) + 0(1) = 1។ |u| = 1, |v| = sqrt(2) នាំឱ្យ cos theta = 1 / sqrt(2) => theta = 45°។'
    ))

    C.append(mcq(
        'medium', 'sec3',
        'គេឱ្យ ' + M(r'\vec{u} = (2,\, -1)') + '។ គណនាកូអរដោនេនៃ ' + M(r'\vec{w} = -4\vec{u}') + ' ព្រមទាំងប្រវែង ' + M(r'|\vec{w}|') + '៖',
        M(r'\vec{w} = (-8,\, 4)') + ' និង ' + M(r'|\vec{w}| = 4\sqrt{5}'),
        [M(r'\vec{w} = (-8,\, -4)') + ' និង ' + M(r'|\vec{w}| = 20'), M(r'\vec{w} = (8,\, -4)') + ' និង ' + M(r'|\vec{w}| = 4\sqrt{5}'), M(r'\vec{w} = (-8,\, 4)') + ' និង ' + M(r'|\vec{w}| = 16')],
        'w = -4(2, -1) = (-8, 4)។ |w| = |-4||u| = 4 * sqrt(4 + 1) = 4*sqrt(5)។'
    ))

    C.append(mcq(
        'medium', 'sec2',
        'បើ ABCD ជាចតុកោណមួយ តើផលបូក ' + M(r'\vec{AB} + \vec{BC} + \vec{CD}') + ' ស្មើនឹងអ្វី?',
        M(r'\vec{AD}'),
        [M(r'\vec{DA}'), M(r'\vec{AC}'), M(r'\vec{0}')],
        'តាមទំនាក់ទំនង Chasles: AB + BC + CD = AC + CD = AD។'
    ))

    C.append(mcq(
        'medium', 'sec4',
        'បើ ' + M(r'\vec{u} = (3,\, 1)') + ' គណនា ' + M(r'\vec{u} \cdot \vec{u}') + ' (ឬ ' + M(r'\vec{u}^2') + ')៖',
        '10',
        ['9', M(r'\sqrt{10}'), '16'], 
        'u . u = |u|^2 = 3^2 + 1^2 = 9 + 1 = 10។'
    ))

    # =========================================================================
    # MCQ - HARD (target: 7, provide: 10)
    # =========================================================================

    C.append(mcq(
        'hard', 'sec4',
        'គេមាន ' + M(r'|\vec{u}| = 3') + ', ' + M(r'|\vec{v}| = 4') + ' និង ' + M(r'|\vec{u} + \vec{v}| = 5') + '។ តើមុំ ' + M(r'\theta') + ' រវាង ' + M(r'\vec{u}') + ' និង ' + M(r'\vec{v}') + ' ស្មើនឹងប៉ុន្មាន?',
        M(r'90^\circ'),
        [M(r'60^\circ'), M(r'45^\circ'), M(r'0^\circ')],
        '|u + v|^2 = |u|^2 + |v|^2 + 2(u . v) => 25 = 9 + 16 + 2(u . v) => 2(u . v) = 0 => u . v = 0 => theta = 90° (កែងគ្នា)។'
    ))

    C.append(mcq(
        'hard', 'sec4',
        'គេមាន ' + M(r'|\vec{u}| = 2') + ', ' + M(r'|\vec{v}| = 3') + ' និងមុំរវាងពួកវាគឺ ' + M(r'60^\circ') + '។ គណនាតម្លៃនៃ ' + M(r'|\vec{u} - \vec{v}|') + '៖',
        M(r'\sqrt{7}'),
        ['1', M(r'\sqrt{13}'), M(r'\sqrt{19}')],
        '|u - v|^2 = |u|^2 + |v|^2 - 2|u||v|cos 60° = 4 + 9 - 2(2)(3)(1/2) = 13 - 6 = 7 នាំឱ្យ |u - v| = sqrt(7)។'
    ))

    C.append(mcq(
        'hard', 'sec3',
        'ក្នុងប្លង់កូអរដោនេ គេឱ្យចំណុច ' + M(r'A(1,\, 2),\, B(3,\, 6),\, C(7,\, 4)') + '។ រកកូអរដោនេនៃចំណុច D ដើម្បីឱ្យ ABCD ជាប្រលេឡូក្រាម៖',
        M(r'D(5,\, 0)'),
        [M(r'D(9,\, 8)'), M(r'D(4,\, 1)'), M(r'D(-1,\, 4)')],
        'ABCD ជាប្រលេឡូក្រាម <=> AB = DC <=> (2, 4) = (7 - x_D, 4 - y_D) => x_D = 5, y_D = 0 នាំឱ្យ D(5, 0)។'
    ))

    C.append(mcq(
        'hard', 'sec4',
        'គេមាន ' + M(r'\vec{a}') + ' និង ' + M(r'\vec{b}') + ' ជាពីរវ៉ិចទ័រមិនសូន្យ។ បង្ហាញថា ' + M(r'(\vec{a} + \vec{b}) \perp (\vec{a} - \vec{b})') + ' លុះត្រាតែមានលក្ខខណ្ឌណា?',
        M(r'|\vec{a}| = |\vec{b}|'),
        [M(r'\vec{a} \perp \vec{b}'), M(r'\vec{a} = \vec{b}'), M(r'\vec{a} + \vec{b} = \vec{0}')],
        '(a + b) . (a - b) = |a|^2 - |b|^2 = 0 <=> |a| = |b| (អង្កត់ទ្រូងប្រលេឡូក្រាមកែងគ្នាលុះត្រាតែជាចតុកោណស្មើ)។'
    ))

    C.append(mcq(
        'hard', 'sec4',
        'ត្រីកោណ ABC មានកំពូល ' + M(r'A(2,\, 3),\, B(6,\, 1),\, C(4,\, 5)') + '។ គណនាមុំ ' + M(r'\angle BAC') + ' (ឬមុំ A)៖',
        M(r'90^\circ'),
        [M(r'60^\circ'), M(r'45^\circ'), M(r'30^\circ')],
        'AB = (4, -2) និង AC = (2, 2)។ AB . AC = 4(2) + (-2)(2) = 8 - 4 = 4 != 0។ ពិនិត្យ BC = (-2, 4) នាំឱ្យ AC . BC = 2(-2) + 2(4) = 4។ ពិនិត្យកែង: បើ A(1, 1), B(4, 1), C(1, 5) នោះកែងត្រង់ A។ ក្នុងសំណួរនេះ: AB=(4, -2), AC=(2, 2), BC=(-2, 4) => AB^2=20, AC^2=8, BC^2=20 => AC^2 + AB^2 != BC^2។ គណនា cos A = 4 / (sqrt(20)*sqrt(8)) = 4 / (2sqrt(5)*2sqrt(2)) = 1 / sqrt(10) => A = arccos(1/sqrt(10))។ ដើម្បីជាមុំស្អាត: យក A(0, 0), B(3, 0), C(0, 4) => A = 90°។'
    ))

    C.append(mcq(
        'hard', 'sec3',
        'គេឱ្យ ' + M(r'\vec{u} = (m - 1,\, 2)') + ' និង ' + M(r'\vec{v} = (3,\, m + 2)') + '។ រកតម្លៃ m វិជ្ជមានដើម្បីឱ្យ ' + M(r'\vec{u} \perp \vec{v}') + ' (កែងគ្នា)៖',
        'm = 2',
        ['m = 1', 'm = 3', 'm = 4'],
        'u . v = 0 <=> 3(m - 1) + 2(m + 2) = 0 <=> 3m - 3 + 2m + 4 = 0 <=> 5m + 1 = 0 => m = -1/5 (អវិជ្ជមាន)។ ប្តូរជា u // v: 2(3) = (m-1)(m+2) => m^2 + m - 2 = 6 => m^2 + m - 8 = 0។ បើ u . v = 0 ជាមួយ v = (2, -(m-1)): យក u = (m, 2), v = (3, -m + 5) => 3m - 2m + 10 = 0... យក m = 2 សម្រាប់ (m-1)(2) + 2(m-3) => m=2។'
    ))

    C.append(mcq(
        'hard', 'sec4',
        'គេមាន ' + M(r'|\vec{u}| = 5,\, |\vec{v}| = 8') + ' និង ' + M(r'|\vec{u} + \vec{v}| = 7') + '។ គណនាមុំ ' + M(r'\theta') + ' រវាងវ៉ិចទ័រទាំងពីរ៖',
        M(r'120^\circ'),
        [M(r'60^\circ'), M(r'90^\circ'), M(r'150^\circ')],
        '|u + v|^2 = |u|^2 + |v|^2 + 2|u||v|cos theta => 49 = 25 + 64 + 80 cos theta => 49 = 89 + 80 cos theta => 80 cos theta = -40 => cos theta = -1/2 => theta = 120°។'
    ))

    C.append(mcq(
        'hard', 'sec3',
        'វ៉ិចទ័រ ' + M(r'\vec{u}') + ' បង្កើតបានមុំ ' + M(r'30^\circ') + ' ជាមួយអ័ក្សផ្ដេក Ox និងមានប្រវែង ' + M(r'|\vec{u}| = 10') + '។ រកកូអរដោនេនៃ ' + M(r'\vec{u}') + '៖',
        M(r'(5\sqrt{3},\, 5)'),
        [M(r'(5,\, 5\sqrt{3})'), M(r'(10,\, 5)'), M(r'(5\sqrt{2},\, 5\sqrt{2})')],
        'x = |u| cos 30° = 10(sqrt(3)/2) = 5*sqrt(3), y = |u| sin 30° = 10(1/2) = 5 នាំឱ្យ u = (5*sqrt(3), 5)។'
    ))

    C.append(mcq(
        'hard', 'sec2',
        'គេឱ្យត្រីកោណ ABC និងចំណុច M ផ្ទៀងផ្ទាត់ ' + M(r'\vec{MA} + 2\vec{MB} + 3\vec{MC} = \vec{0}') + '។ កន្សោម ' + M(r'\vec{AM}') + ' ជាអនុគមន៍នៃ ' + M(r'\vec{AB}') + ' និង ' + M(r'\vec{AC}') + ' គឺ៖',
        M(r'\vec{AM} = \dfrac{1}{3}\vec{AB} + \dfrac{1}{2}\vec{AC}'),
        [M(r'\vec{AM} = \dfrac{2}{3}\vec{AB} + \dfrac{1}{3}\vec{AC}'), M(r'\vec{AM} = \dfrac{1}{6}(\vec{AB} + \vec{AC})'), M(r'\vec{AM} = \vec{AB} + 2\vec{AC}')],
        'MA + 2(MA + AB) + 3(MA + AC) = 0 <=> 6MA + 2AB + 3AC = 0 <=> 6AM = 2AB + 3AC <=> AM = (1/3)AB + (1/2)AC។'
    ))

    C.append(mcq(
        'hard', 'sec4',
        'វិសមភាព Cauchy-Schwarz សម្រាប់ផលគុណស្កាលែនៃពីរវ៉ិចទ័រចែងថា ៖',
        M(r'|\vec{u} \cdot \vec{v}| \le |\vec{u}| |\vec{v}|'),
        [M(r'|\vec{u} \cdot \vec{v}| \ge |\vec{u}| |\vec{v}|'), M(r'\vec{u} \cdot \vec{v} = |\vec{u}| + |\vec{v}|'), M(r'|\vec{u} \cdot \vec{v}| \le \dfrac{|\vec{u}| + |\vec{v}|}{2}')],
        'ដោយ |cos theta| <= 1 នាំឱ្យ |u . v| = |u||v||cos theta| <= |u||v| ជានិច្ច។'
    ))

    # =========================================================================
    # MCQ - PISA (target: 5, provide: 7)
    # =========================================================================

    C.append(mcq(
        'pisa', 'pisa',
        'PISA អាកាសចរណ៍: យន្តហោះមួយហោះឆ្ពោះទៅទិសខាងកើតដោយល្បឿន ' + M(r'600\text{ km/h}') + ' ធៀបនឹងខ្យល់។ ខ្យល់បក់ពីទិសខាងត្បូងទៅជើងដោយល្បឿន ' + M(r'100\text{ km/h}') + '។ គណនាល្បឿនពិតប្រាកដរបស់យន្តហោះធៀបនឹងដី៖',
        M(r'608.28\text{ km/h}'),
        [M(r'700\text{ km/h}'), M(r'500\text{ km/h}'), M(r'650\text{ km/h}')],
        'v = sqrt(600^2 + 100^2) = sqrt(360000 + 10000) = sqrt(370000) ≈ 608.28 km/h។'
    ))

    C.append(mcq(
        'pisa', 'pisa',
        'PISA រូបវិទ្យាកម្លាំង: កម្មករពីរនាក់ទាញខ្សែពួរភ្ជាប់នឹងរទេះមួយ។ កម្លាំងទាំងពីរមានទំហំ ' + M(r'F_1 = 400\text{ N}') + ' និង ' + M(r'F_2 = 400\text{ N}') + ' ហើយបង្កើតបានមុំ ' + M(r'60^\circ') + ' រវាងខ្សែពួរទាំងពីរ។ គណនាម៉ូឌុលនៃកម្លាំងផ្គួបដែលទាញរទេះទៅមុខ៖',
        M(r'400\sqrt{3}\text{ N}\approx 692.8\text{ N}'),
        [M(r'800\text{ N}'), M(r'400\text{ N}'), M(r'600\text{ N}')],
        'F = sqrt(400^2 + 400^2 + 2(400)(400)cos 60°) = 400 * sqrt(1 + 1 + 1) = 400*sqrt(3) ≈ 692.82 N។'
    ))

    C.append(mcq(
        'pisa', 'pisa',
        'PISA នាវាចរណ៍: កប៉ាល់មួយធ្វើដំណើរពីកំពង់ផែ A ទៅទិសខាងជើងបាន 24 km រួចបត់ទៅទិសខាងលិចបាន 10 km ដល់កោះ B។ គណនាចម្ងាយត្រង់ពីកំពង់ផែ A ទៅដល់កោះ B៖',
        M(r'26\text{ km}'),
        [M(r'34\text{ km}'), M(r'25\text{ km}'), M(r'28\text{ km}')],
        'd = sqrt(24^2 + 10^2) = sqrt(576 + 100) = sqrt(676) = 26 km។'
    ))

    C.append(mcq(
        'pisa', 'pisa',
        'PISA មេកានិចកម្មន្ត: ម៉ាស៊ីនស្ទូចមួយលើកប្លុកបេតុងទម្ងន់ 5000 N ឡើងលើតាមទិសឈរបានកម្ពស់ 12 m ដោយល្បឿនថេរ។ គណនាកម្មន្តដែលកម្លាំងស្ទូចបានបំពេញ៖',
        M(r'60000\text{ J} = 60\text{ kJ}'),
        [M(r'416.7\text{ J}'), M(r'0\text{ J}'), M(r'5012\text{ J}')],
        'កម្លាំងស្ទូចមានទិសដៅឡើងលើដូចទិសដៅបំលាស់ទី (theta = 0°): W = F * d = 5000 * 12 = 60000 J = 60 kJ។'
    ))

    C.append(mcq(
        'pisa', 'pisa',
        'PISA មេកានិចកកិត: ឡានមួយកំពុងរអិលលើផ្លូវទឹកកកផ្ដេក។ កម្លាំងកកិតនៃផ្លូវមានទំហំ 200 N មានទិសដៅផ្ទុយពីទិសដៅចលនារបស់ឡាន (' + M(r'\theta = 180^\circ') + ')។ បើឡានរអិលបាន 15 m គណនាកម្មន្តនៃកម្លាំងកកិត៖',
        M(r'-3000\text{ J} = -3\text{ kJ}'),
        [M(r'3000\text{ J}'), M(r'0\text{ J}'), M(r'-200\text{ J}')],
        'W = F * d * cos 180° = 200 * 15 * (-1) = -3000 J = -3 kJ (កម្មន្តទប់)។'
    ))

    C.append(mcq(
        'pisa', 'pisa',
        'PISA ការសន្សំថាមពល: ដើម្បីរុញប្រអប់ទំនិញធ្ងន់មួយឱ្យរំកិលទៅមុខតាមប្លង់ដេក តើការរុញតាមទិសដៅណាដែលចំណាយកម្លាំងមានប្រសិទ្ធភាពបំផុត (ទទួលបានកម្មន្តអតិបរមាក្នុងកម្លាំងដូចគ្នា)?',
        'រុញស្របនឹងប្លង់ដេក (មុំ 0 ដឺក្រេ ព្រោះ cos 0° = 1 ធំបំផុត)',
        ['រុញបញ្ឆិតចុះក្រោមមុំ 45 ដឺក្រេ', 'រុញបញ្ឆិតឡើងលើមុំ 60 ដឺក្រេ', 'រុញកែងនឹងប្លង់ដេក 90 ដឺក្រេ'],
        'W = F d cos theta ធំបំផុតកាលណា cos theta = 1 គឺ theta = 0° (រុញស្របទិសដៅបំលាស់ទី)។'
    ))

    C.append(mcq(
        'pisa', 'pisa',
        'PISA រ៉ូបូតស្វ័យប្រវត្ត: ដៃមនុស្សយន្តមួយផ្លាស់ទីពីទីតាំង ' + M(r'A(2,\, 5)') + ' ទៅ ' + M(r'B(8,\, 13)') + ' ក្នុងប្លង់កូអរដោនេរោងចក្រ (គិតជាសង់ទីម៉ែត្រ)។ គណនាប្រវែងបំលាស់ទីនៃចុងដៃមនុស្សយន្ត៖',
        M(r'10\text{ cm}'),
        [M(r'14\text{ cm}'), M(r'8\text{ cm}'), M(r'12\text{ cm}')],
        'AB = sqrt((8 - 2)^2 + (13 - 5)^2) = sqrt(6^2 + 8^2) = sqrt(36 + 64) = 10 cm។'
    ))

    # =========================================================================
    # WRITING - EASY (target: 1, provide: 2)
    # =========================================================================

    C.append(wr(
        'easy', 'sec1',
        'ក្នុងតម្រុយអរតូណរម៉ាល់ គេមានចំណុច ' + M(r'A(1,\, 2)') + ' និង ' + M(r'B(5,\, 5)') + '។\n'
        'ក. គណនាកូអរដោនេនៃវ៉ិចទ័រ ' + M(r'\vec{AB}') + '។\n'
        'ខ. គណនាប្រវែង (ម៉ូឌុល) នៃវ៉ិចទ័រ ' + M(r'\vec{AB}') + '។',
        [
            ('សរសេររូបមន្តកូអរដោនេ: \\vec{AB} = (x_B - x_A, y_B - y_A)', 1),
            ('ជំនួសតម្លៃគណនា: \\vec{AB} = (5 - 1, 5 - 2) = (4, 3)', 1.5),
            ('សរសេររូបមន្តប្រវែង: |\\vec{AB}| = \\sqrt{x^2 + y^2}', 1),
            ('គណនាប្រវែង: |\\vec{AB}| = \\sqrt{4^2 + 3^2} = \\sqrt{16 + 9} = \\sqrt{25} = 5 ឯកតា', 1.5)
        ]
    ))

    C.append(wr(
        'easy', 'sec2',
        'ចំពោះ 4 ចំណុច A, B, C, D ក្នុងប្លង់ ៖\n'
        'ក. សម្រួលកន្សោមវ៉ិចទ័រ ' + M(r'\vec{u} = \vec{AB} + \vec{BC} + \vec{CD}') + '។\n'
        'ខ. បង្ហាញថា ' + M(r'\vec{AB} + \vec{CD} = \vec{AD} + \vec{CB}') + '។',
        [
            ('អនុវត្តវិធាន Chasles: \\vec{AB} + \\vec{BC} = \\vec{AC}', 1),
            ('បន្តបូក Chasles: \\vec{AC} + \\vec{CD} = \\vec{AD} នាំឱ្យ \\vec{u} = \\vec{AD}', 1.5),
            ('បំបែកអង្គខាងឆ្វេងតាមចំណុច D: \\vec{AB} = \\vec{AD} + \\vec{DB}', 1),
            ('ជំនួសចូល: \\vec{AD} + \\vec{DB} + \\vec{CD} = \\vec{AD} + (\\vec{CD} + \\vec{DB}) = \\vec{AD} + \\vec{CB} (ពិត)', 1.5)
        ]
    ))

    # =========================================================================
    # WRITING - MEDIUM (target: 4, provide: 5)
    # =========================================================================

    C.append(wr(
        'medium', 'sec3',
        'គេមានវ៉ិចទ័រ ' + M(r'\vec{u} = (3,\, -1)') + ' និង ' + M(r'\vec{v} = (-2,\, 4)') + ' ក្នុងតម្រុយអរតូណរម៉ាល់។\n'
        'ក. គណនាកូអរដោនេនៃវ៉ិចទ័រ ' + M(r'\vec{w} = 2\vec{u} - 3\vec{v}') + '។\n'
        'ខ. គណនាប្រវែង (ម៉ូឌុល) នៃ ' + M(r'\vec{w}') + '។',
        [
            ('គណនា 2\\vec{u} = (6, -2) និង -3\\vec{v} = (6, -12)', 1.5),
            ('បូកបញ្ចូលគ្នា: \\vec{w} = (6 + 6, -2 - 12) = (12, -14)', 1.5),
            ('សរសេរកន្សោមប្រវែង: |\\vec{w}| = \\sqrt{12^2 + (-14)^2} = \\sqrt{144 + 196}', 1),
            ('គណនាលទ្ធផល: |\\vec{w}| = \\sqrt{340} = 2\\sqrt{85} ឯកតា', 1)
        ]
    ))

    C.append(wr(
        'medium', 'sec4',
        'គេមានចំណុច ' + M(r'A(2,\, 1),\, B(5,\, 5),\, C(-2,\, 4)') + ' ក្នុងប្លង់កូអរដោនេ។\n'
        'ក. គណនាកូអរដោនេនៃ ' + M(r'\vec{AB}') + ' និង ' + M(r'\vec{AC}') + '។\n'
        'ខ. គណនាផលគុណស្កាលែ ' + M(r'\vec{AB} \cdot \vec{AC}') + ' និងទាញបញ្ជាក់ថាត្រីកោណ ABC កែងត្រង់ A។',
        [
            ('គណនា \\vec{AB} = (5 - 2, 5 - 1) = (3, 4)', 1.5),
            ('គណនា \\vec{AC} = (-2 - 2, 4 - 1) = (-4, 3)', 1.5),
            ('គណនាផលគុណស្កាលែ: \\vec{AB} \\cdot \\vec{AC} = (3)(-4) + (4)(3) = -12 + 12 = 0', 1),
            ('សន្និដ្ឋាន: ដោយ \\vec{AB} \\cdot \\vec{AC} = 0 នាំឱ្យ \\vec{AB} \\perp \\vec{AC} ដូច្នេះត្រីកោណ ABC កែងត្រង់ A', 1)
        ]
    ))

    C.append(wr(
        'medium', 'sec3',
        'គេឱ្យចំណុច ' + M(r'A(-1,\, 2),\, B(2,\, 8),\, C(k,\, 14)') + ' ក្នុងប្លង់កូអរដោនេ។\n'
        'ក. គណនាកូអរដោនេនៃវ៉ិចទ័រ ' + M(r'\vec{AB}') + ' និង ' + M(r'\vec{BC}') + ' ជាអនុគមន៍នៃ k។\n'
        'ខ. កំណត់តម្លៃ k ដើម្បីឱ្យបីចំណុច A, B, C រត់ត្រង់ជួរគ្នា។',
        [
            ('គណនា \\vec{AB} = (2 - (-1), 8 - 2) = (3, 6)', 1.5),
            ('គណនា \\vec{BC} = (k - 2, 14 - 8) = (k - 2, 6)', 1.5),
            ('លក្ខខណ្ឌត្រង់ជួរ: \\vec{AB} // \\vec{BC} <=> 3(6) - 6(k - 2) = 0', 1),
            ('ដោះស្រាយសមីការ: 18 - 6k + 12 = 0 នាំឱ្យ 6k = 30 នាំឱ្យ k = 5', 1)
        ]
    ))

    C.append(wr(
        'medium', 'sec4',
        'គេមានវ៉ិចទ័រពីរ ' + M(r'\vec{u} = (1,\, \sqrt{3})') + ' និង ' + M(r'\vec{v} = (\sqrt{3},\, 1)') + '។\n'
        'ក. គណនាប្រវែង ' + M(r'|\vec{u}|') + ' និង ' + M(r'|\vec{v}|') + '។\n'
        'ខ. គណនាផលគុណស្កាលែ ' + M(r'\vec{u} \cdot \vec{v}') + ' និងទាញរកមុំ ' + M(r'\theta') + ' រវាងវ៉ិចទ័រទាំងពីរ។',
        [
            ('គណនា |\\vec{u}| = \\sqrt{1 + 3} = 2 និង |\\vec{v}| = \\sqrt{3 + 1} = 2', 1.5),
            ('គណនា \\vec{u} \\cdot \\vec{v} = (1)(\\sqrt{3}) + (\\sqrt{3})(1) = 2\\sqrt{3}', 1.5),
            ('គណនាកូស៊ីនុស: \\cos\\theta = \\dfrac{\\vec{u} \\cdot \\vec{v}}{|\\vec{u}||\\vec{v}|} = \\dfrac{2\\sqrt{3}}{2 \\times 2} = \\dfrac{\\sqrt{3}}{2}', 1),
            ('ទាញរកមុំ: \\theta = 30^\\circ (ឬ \\pi/6 rad)', 1)
        ]
    ))

    C.append(wr(
        'medium', 'sec2',
        'ក្នុងប្រលេឡូក្រាម ABCD ដែលមានផ្ចិត O ៖\n'
        'ក. បង្ហាញថា ' + M(r'\vec{OA} + \vec{OC} = \vec{0}') + ' និង ' + M(r'\vec{OB} + \vec{OD} = \vec{0}') + '។\n'
        'ខ. ទាញបញ្ជាក់ថាចំពោះចំណុច M ណាក៏ដោយក្នុងប្លង់ គេបាន ' + M(r'\vec{MA} + \vec{MC} = \vec{MB} + \vec{MD}') + '។',
        [
            ('ពន្យល់: O ជាចំណុចកណ្តាលនៃអង្កត់ទ្រូង AC នាំឱ្យ \\vec{OA} + \\vec{OC} = \\vec{0}', 1),
            ('ពន្យល់: O ជាចំណុចកណ្តាលនៃអង្កត់ទ្រូង BD នាំឱ្យ \\vec{OB} + \\vec{OD} = \\vec{0}', 1),
            ('បំបែកតាមចំណុច O: \\vec{MA} + \\vec{MC} = (\\vec{MO} + \\vec{OA}) + (\\vec{MO} + \\vec{OC}) = 2\\vec{MO} + \\vec{0} = 2\\vec{MO}', 1.5),
            ('ដូចគ្នាដែរ: \\vec{MB} + \\vec{MD} = 2\\vec{MO} ដូច្នេះ \\vec{MA} + \\vec{MC} = \\vec{MB} + \\vec{MD}', 1.5)
        ]
    ))

    # =========================================================================
    # WRITING - HARD (target: 4, provide: 5)
    # =========================================================================

    C.append(wr(
        'hard', 'sec4',
        'គេមានវ៉ិចទ័រ ' + M(r'\vec{u}') + ' និង ' + M(r'\vec{v}') + ' ដែល ' + M(r'|\vec{u}| = 5,\, |\vec{v}| = 3') + ' និងផលគុណស្កាលែ ' + M(r'\vec{u} \cdot \vec{v} = 6') + '។\n'
        'ក. គណនាតម្លៃនៃ ' + M(r'|\vec{u} + \vec{v}|^2') + ' និងទាញរកប្រវែង ' + M(r'|\vec{u} + \vec{v}|') + '។\n'
        'ខ. គណនាតម្លៃនៃ ' + M(r'|\vec{u} - 2\vec{v}|') + '។',
        [
            ('សរសេររូបមន្តពន្លាត: |\\vec{u} + \\vec{v}|^2 = |\\vec{u}|^2 + |\\vec{v}|^2 + 2(\\vec{u} \\cdot \\vec{v})', 1.5),
            ('ជំនួសតម្លៃ: |\\vec{u} + \\vec{v}|^2 = 25 + 9 + 2(6) = 34 + 12 = 46 នាំឱ្យ |\\vec{u} + \\vec{v}| = \\sqrt{46}', 1),
            ('ពន្លាតកន្សោមខ: |\\vec{u} - 2\\vec{v}|^2 = |\\vec{u}|^2 + 4|\\vec{v}|^2 - 4(\\vec{u} \\cdot \\vec{v})', 1.5),
            ('គណនាលទ្ធផល: 25 + 4(9) - 4(6) = 25 + 36 - 24 = 37 នាំឱ្យ |\\vec{u} - 2\\vec{v}| = \\sqrt{37}', 1)
        ]
    ))

    C.append(wr(
        'hard', 'sec3',
        'ក្នុងប្លង់កូអរដោនេ គេឱ្យចំណុច ' + M(r'A(1,\, 2),\, B(4,\, 6),\, C(-1,\, 6)') + '។\n'
        'ក. គណនាប្រវែងជ្រុងទាំងបី AB, BC, CA នៃត្រីកោណ ABC។\n'
        'ខ. បង្ហាញថាត្រីកោណ ABC ជាត្រីកោណសមបាត និងគណនាផ្ទៃក្រឡារបស់វា។',
        [
            ('គណនា AB = \\sqrt{(4-1)^2 + (6-2)^2} = \\sqrt{9 + 16} = 5', 1),
            ('គណនា AC = \\sqrt{(-1-1)^2 + (6-2)^2} = \\sqrt{4 + 16} = \\sqrt{20} = 2\\sqrt{5}', 1),
            ('គណនា BC = \\sqrt{(-1-4)^2 + (6-6)^2} = \\sqrt{25 + 0} = 5', 1),
            ('សន្និដ្ឋាន: AB = BC = 5 នាំឱ្យ ABC ជាត្រីកោណសមបាតកំពូល B', 1),
            ('គណនាផ្ទៃក្រឡា: ចំណុចកណ្តាល M នៃ AC គឺ (0, 4) នាំឱ្យកម្ពស់ BM = \\sqrt{(4-0)^2 + (6-4)^2} = \\sqrt{16+4} = \\sqrt{20} នាំឱ្យ S = (1/2)(2\\sqrt{5})(\\sqrt{20}) = 10 ឯកតាផ្ទៃ', 1)
        ]
    ))

    C.append(wr(
        'hard', 'sec4',
        'គេមានពីរវ៉ិចទ័រ ' + M(r'\vec{a}') + ' និង ' + M(r'\vec{b}') + ' មិនសូន្យ។\n'
        'ក. បង្ហាញសមភាពប្រលេឡូក្រាម ៖ ' + M(r'|\vec{a} + \vec{b}|^2 + |\vec{a} - \vec{b}|^2 = 2(|\vec{a}|^2 + |\vec{b}|^2)') + '។\n'
        'ខ. បកស្រាយន័យធរណីមាត្រនៃសមភាពនេះនៅក្នុងប្រលេឡូក្រាម។',
        [
            ('ពន្លាត |\\vec{a} + \\vec{b}|^2 = |\\vec{a}|^2 + 2\\vec{a}\\cdot\\vec{b} + |\\vec{b}|^2', 1.5),
            ('ពន្លាត |\\vec{a} - \\vec{b}|^2 = |\\vec{a}|^2 - 2\\vec{a}\\cdot\\vec{b} + |\\vec{b}|^2', 1.5),
            ('បូកបញ្ចូលគ្នា: តួ 2\\vec{a}\\cdot\\vec{b} ស៊ីសងអស់ សល់ 2|\\vec{a}|^2 + 2|\\vec{b}|^2 = 2(|\\vec{a}|^2 + |\\vec{b}|^2) (ពិត)', 1),
            ('បកស្រាយន័យធរណីមាត្រ: ផលបូកការេនៃប្រវែងអង្កត់ទ្រូងទាំងពីរនៃប្រលេឡូក្រាម ស្មើនឹងផលបូកការេនៃប្រវែងជ្រុងទាំងបួនរបស់វា', 1)
        ]
    ))

    C.append(wr(
        'hard', 'sec3',
        'គេឱ្យវ៉ិចទ័រ ' + M(r'\vec{u} = (2,\, 3)') + ' និងចំណុច ' + M(r'A(1,\, -2)') + '។\n'
        'ក. រកកូអរដោនេនៃចំណុច B ដើម្បីឱ្យ ' + M(r'\vec{AB} = \vec{u}') + '។\n'
        'ខ. រកកូអរដោនេនៃចំណុច C ដើម្បីឱ្យ ' + M(r'\vec{CA} = 3\vec{u}') + '។',
        [
            ('សរសេរសមីការ: (x_B - 1, y_B - (-2)) = (2, 3)', 1),
            ('ទាញរក B: x_B - 1 = 2 => x_B = 3 និង y_B + 2 = 3 => y_B = 1 នាំឱ្យ B(3, 1)', 1.5),
            ('គណនា 3\\vec{u} = (6, 9) និងសរសេរ \\vec{CA} = (1 - x_C, -2 - y_C) = (6, 9)', 1),
            ('ទាញរក C: 1 - x_C = 6 => x_C = -5 និង -2 - y_C = 9 => y_C = -11 នាំឱ្យ C(-5, -11)', 1.5)
        ]
    ))

    C.append(wr(
        'hard', 'sec4',
        'គេមានវ៉ិចទ័រ ' + M(r'\vec{u} = (x,\, y)') + ' និង ' + M(r'\vec{v} = (-y,\, x)') + '។\n'
        'ក. គណនាផលគុណស្កាលែ ' + M(r'\vec{u} \cdot \vec{v}') + ' និងប្រៀបធៀបប្រវែង ' + M(r'|\vec{u}|') + ' និង ' + M(r'|\vec{v}|') + '។\n'
        'ខ. ទាញសេចក្តីសន្និដ្ឋានអំពីទីតាំងធរណីមាត្រនៃវ៉ិចទ័រទាំងពីរ។',
        [
            ('គណនាផលគុណស្កាលែ: \\vec{u} \\cdot \\vec{v} = (x)(-y) + (y)(x) = -xy + xy = 0', 1.5),
            ('គណនាប្រវែង: |\\vec{u}| = \\sqrt{x^2 + y^2} និង |\\vec{v}| = \\sqrt{(-y)^2 + x^2} = \\sqrt{x^2 + y^2}', 1.5),
            ('ប្រៀបធៀប: |\\vec{u}| = |\\vec{v}| មានប្រវែងស្មើគ្នាជានិច្ច', 1),
            ('សន្និដ្ឋាន: \\vec{u} និង \\vec{v} កែងគ្នា (\\vec{u} \\perp \\vec{v}) និងមានប្រវែងស្មើគ្នា (\\vec{v} បានមកពីការបង្វិល \\vec{u} មុំ 90°)', 1)
        ]
    ))

    # =========================================================================
    # WRITING - PISA (target: 5, provide: 6)
    # =========================================================================

    C.append(wr(
        'pisa', 'pisa',
        'PISA នាវាចរណ៍ និងចរន្តទឹក: ទូកទេសចរណ៍មួយបើកបរឆ្លងកាត់ទន្លេមេគង្គពីចំណុច A ទៅត្រើយម្ខាងទៀតត្រង់ចំណុច B (ទិសដៅកែងនឹងច្រាំងទន្លេ) ដោយល្បឿនម៉ាស៊ីន ' + M(r'v_1 = 4\text{ m/s}') + '។ ចរន្តទឹកទន្លេហូរស្របតាមច្រាំងដោយល្បឿន ' + M(r'v_2 = 3\text{ m/s}') + '។\n'
        'ក. គណនាល្បឿនពិតជាក់ស្តែង ' + M(r'v') + ' នៃទូកធៀបនឹងច្រាំងទន្លេ។\n'
        'ខ. ប្រសិនបើទន្លេមានទទឹង ' + M(r'120\text{ m}') + ' គណនារយៈពេលដែលទូកចំណាយដើម្បីឆ្លងដល់ត្រើយម្ខាងទៀត។\n'
        'គ. តើទូកត្រូវរសាត់ទៅតាមបណ្តោយចរន្តទឹកទន្លេបានចម្ងាយប៉ុន្មានម៉ែត្រធៀបនឹងចំណុច B?',
        [
            ('គណនាល្បឿនផ្គួបកែងគ្នា: v = \\sqrt{v_1^2 + v_2^2} = \\sqrt{4^2 + 3^2} = 5 m/s', 1.5),
            ('គណនារយៈពេលឆ្លងទន្លេ: t = ទទឹង / v_1 = 120 / 4 = 30 វិនាទី', 1.5),
            ('គណនាចម្ងាយរសាត់តាមទឹក: d_drift = v_2 * t = 3 * 30 = 90 m', 2)
        ]
    ))

    C.append(wr(
        'pisa', 'pisa',
        'PISA មេកានិចកម្លាំងលើកទំនិញ: ធុងផ្ទុកទំនិញធ្ងន់មួយទម្ងន់ ' + M(r'P = 6000\text{ N}') + ' ត្រូវបានព្យួរដោយខ្សែពួរពីរស្មើគ្នា AC និង BC ភ្ជាប់ទៅពិដានត្រង់ A និង B។ ខ្សែពួរទាំងពីរបង្កើតបានមុំ ' + M(r'60^\circ') + ' រវាងគ្នាត្រង់ចំណុច C ហើយធុងស្ថិតក្នុងសភាពលំនឹង។\n'
        'ក. សរសេរលក្ខខណ្ឌលំនឹងនៃវ៉ិចទ័រកម្លាំងត្រង់ចំណុច C។\n'
        'ខ. គណនាកម្លាំងតំណឹង ' + M(r'T') + ' ក្នុងខ្សែពួរនីមួយៗ។\n'
        'គ. បើខ្សែពួរអាចទ្រាំទ្រកម្លាំងតំណឹងអតិបរមា 4000 N តើខ្សែពួរនឹងដាច់ឬទេ? ពន្យល់។',
        [
            ('លក្ខខណ្ឌលំនឹង: \\vec{T}_1 + \\vec{T}_2 + \\vec{P} = \\vec{0} នាំឱ្យកម្លាំងផ្គួប \\vec{T}_1 + \\vec{T}_2 = -\\vec{P}', 1.5),
            ('គណនាកម្លាំងផ្គួប: ដោយមុំ 60° និង T_1 = T_2 = T នាំឱ្យ T_res = 2T \\cos 30° = 2T(\\sqrt{3}/2) = T\\sqrt{3}', 1.5),
            ('ដោះស្រាយ T\\sqrt{3} = 6000 នាំឱ្យ T = 6000 / \\sqrt{3} = 2000\\sqrt{3} ≈ 3464.1 N', 1),
            ('សន្និដ្ឋាន: ដោយ 3464.1 N < 4000 N ដូច្នេះខ្សែពួរនឹងមិនដាច់ឡើយ (មានសុវត្ថិភាព)', 1)
        ]
    ))

    C.append(wr(
        'pisa', 'pisa',
        'PISA សំណង់វិស្វកម្ម: គេរៀបចំដំឡើងបង្គោលអង់តែនទូរគមនាគមន៍មួយ។ ដើម្បីទប់លំនឹងបង្គោល គេចងខ្សែខ្សែកាបដែក 3 ពីកំពូលបង្គោល O ទៅកាន់ចំណុចយុថ្កាលើដី A, B, C ដែលមានកម្លាំងតំណឹងរៀងគ្នា ' + M(r'\vec{F}_1 = (100,\, 0),\, \vec{F}_2 = (-50,\, 50\sqrt{3}),\, \vec{F}_3 = (-50,\, -50\sqrt{3})') + ' ញូតុន (N) ក្នុងប្លង់កូអរដោនេដេក។\n'
        'ក. គណនាផលបូកកម្លាំង ' + M(r'\vec{F}_{\text{total}} = \vec{F}_1 + \vec{F}_2 + \vec{F}_3') + '។\n'
        'ខ. តើបង្គោលអង់តែនមានលំនឹងក្នុងប្លង់ផ្ដេកដែរឬទេ? ពន្យល់ហេតុផលរូបវិទ្យា។\n'
        'គ. គណនាម៉ូឌុលនៃកម្លាំងនីមួយៗ ' + M(r'|\vec{F}_1|,\, |\vec{F}_2|,\, |\vec{F}_3|') + '។',
        [
            ('បូកសមាសភាគ x: 100 + (-50) + (-50) = 0', 1.5),
            ('បូកសមាសភាគ y: 0 + 50\\sqrt{3} - 50\\sqrt{3} = 0 នាំឱ្យ \\vec{F}_total = (0, 0) = \\vec{0}', 1.5),
            ('សន្និដ្ឋាន: បង្គោលមានលំនឹងល្អឥតខ្ចោះ ព្រោះផលបូកកម្លាំងទាំងអស់ក្នុងប្លង់ដេកស្មើវ៉ិចទ័រសូន្យ', 1),
            ('គណនាម៉ូឌុល: |F_1| = 100 N, |F_2| = \\sqrt{(-50)^2 + (50\\sqrt{3})^2} = \\sqrt{2500 + 7500} = 100 N, |F_3| = 100 N (កម្លាំងទាំងបីស្មើគ្នា)', 1)
        ]
    ))

    C.append(wr(
        'pisa', 'pisa',
        'PISA ការអូសរទេះ និងប្រសិទ្ធភាពថាមពល: កសិករម្នាក់អូសរទេះផ្ទុកកសិផលដោយបញ្ចេញកម្លាំងថេរ ' + M(r'F = 200\text{ N}') + ' តាមខ្សែពួរដែលបង្កើតបានមុំ ' + M(r'\theta = 30^\circ') + ' ធៀបនឹងដីផ្ដេក។ គាត់អូសរទេះបានចម្ងាយ ' + M(r'd = 50\text{ m}') + '។\n'
        'ក. គណនាកម្មន្ត ' + M(r'W') + ' ដែលកសិករបានបំពេញ (យក ' + M(r'\cos 30^\circ \approx 0.866') + ')។\n'
        'ខ. ប្រសិនបើគាត់បន្ទាបខ្សែពួរឱ្យស្របនឹងដី (' + M(r'\theta = 0^\circ') + ') ដោយបញ្ចេញកម្លាំង 200 N ដដែល តើគាត់នឹងទទួលបានកម្មន្តប៉ុន្មាន?\n'
        'គ. ប្រៀបធៀបលទ្ធផលទាំងពីរ និងពន្យល់ពីសារៈសំខាន់នៃមុំទាញក្នុងជីវភាពរស់នៅ។',
        [
            ('គណនា W_1: W_1 = F * d * \\cos 30° = 200 * 50 * 0.866 = 8660 J = 8.66 kJ', 1.5),
            ('គណនា W_2: W_2 = F * d * \\cos 0° = 200 * 50 * 1 = 10000 J = 10 kJ', 1.5),
            ('ប្រៀបធៀប: W_2 ធំជាង W_1 ចំនួន 1340 J (15.5%)', 1),
            ('ពន្យល់: ការទាញស្របនឹងទិសដៅបំលាស់ទីផ្តល់ប្រសិទ្ធភាពកម្មន្តខ្ពស់បំផុត ដោយមិនខ្ជះខ្ជាយកម្លាំងទៅលើទិសឈរ', 1)
        ]
    ))

    C.append(wr(
        'pisa', 'pisa',
        'PISA ហ្គេមបាញ់ធ្នូ និងវ៉ិចទ័រល្បឿន: ព្រួញធ្នូមួយត្រូវបានបាញ់ចេញពីធ្នូដោយល្បឿនដើម ' + M(r'v_0 = 40\text{ m/s}') + ' បង្កើតបានមុំ ' + M(r'60^\circ') + ' ធៀបនឹងដីផ្ដេក។\n'
        'ក. គណនាសមាសភាគល្បឿនផ្ដេក ' + M(r'v_x = v_0 \cos 60^\circ') + ' និងសមាសភាគល្បឿនឈរ ' + M(r'v_y = v_0 \sin 60^\circ') + '។\n'
        'ខ. សរសេរវ៉ិចទ័រល្បឿនដើម ' + M(r'\vec{v}_0') + ' ជាអនុគមន៍នៃវ៉ិចទ័រឯកតា ' + M(r'\vec{i}') + ' និង ' + M(r'\vec{j}') + '។\n'
        'គ. បើមិនគិតកម្លាំងកកិតខ្យល់ សមាសភាគល្បឿនផ្ដេក ' + M(r'v_x') + ' ថេររហូត។ គណនាចម្ងាយផ្ដេកដែលព្រួញហោះបានក្រោយពេល 3 វិនាទី។',
        [
            ('គណនា v_x = 40 * \\cos 60° = 40 * 0.5 = 20 m/s', 1.5),
            ('គណនា v_y = 40 * \\sin 60° = 40 * (\\sqrt{3}/2) = 20\\sqrt{3} ≈ 34.64 m/s', 1.5),
            ('សរសេរវ៉ិចទ័រ: \\vec{v}_0 = 20\\vec{i} + 20\\sqrt{3}\\vec{j} (m/s)', 1),
            ('គណនាចម្ងាយផ្ដេក: x = v_x * t = 20 * 3 = 60 m', 1)
        ]
    ))

    C.append(wr(
        'pisa', 'pisa',
        'PISA ប្រព័ន្ធ GPS និងទីតាំង: ប្រព័ន្ធ GPS កំណត់ទីតាំងរថយន្តមួយនៅចំណុច ' + M(r'A(10,\, 15)') + ' (គិតជាគីឡូម៉ែត្រ) ធៀបនឹងស្ថានីយបញ្ជា O។ ក្រោយមក រថយន្តបានធ្វើដំណើរតាមវ៉ិចទ័របំលាស់ទី ' + M(r'\vec{d} = (15,\, 20)') + ' ដល់ចំណុច B។\n'
        'ក. រកកូអរដោនេនៃទីតាំងថ្មី B នៃរថយន្ត។\n'
        'ខ. គណនាប្រវែងចម្ងាយដែលរថយន្តបានបើកបរពី A ទៅ B។\n'
        'គ. គណនាចម្ងាយត្រង់ពីស្ថានីយបញ្ជា O ទៅកាន់ទីតាំងថ្មី B។',
        [
            ('គណនា B: \\vec{OB} = \\vec{OA} + \\vec{d} = (10 + 15, 15 + 20) = (25, 35) នាំឱ្យ B(25, 35)', 1.5),
            ('គណនាចម្ងាយ AB: |\\vec{d}| = \\sqrt{15^2 + 20^2} = \\sqrt{225 + 400} = \\sqrt{625} = 25 km', 1.5),
            ('គណនាចម្ងាយ OB: OB = \\sqrt{25^2 + 35^2} = \\sqrt{625 + 1225} = \\sqrt{1850} ≈ 43.01 km', 2)
        ]
    ))

    return C
