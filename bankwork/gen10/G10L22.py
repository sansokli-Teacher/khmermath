# -*- coding: utf-8 -*-
from lib import *

LESSON = 'ការអនុវត្តវ៉ិចទ័រ'
CHAPTER = 'ជំពូកទី 8 : វ៉ិចទ័រក្នុងប្លង់'

def with_img(q, svg):
    q['img'] = svg
    return q

# =========================================================================
# SVG Figures for Lesson 22 (Transparent background, Mathcad italic font)
# =========================================================================

FIG_SECTION_POINT_L22 = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 360 220' width='360' height='220'>
  <defs>
    <marker id='ar-s1' markerWidth='6' markerHeight='6' refX='5' refY='3' orient='auto'>
      <path d='M1,1 L5,3 L1,5 Z' fill='#2563eb'/>
    </marker>
    <marker id='ar-s2' markerWidth='6' markerHeight='6' refX='5' refY='3' orient='auto'>
      <path d='M1,1 L5,3 L1,5 Z' fill='#059669'/>
    </marker>
    <marker id='ar-s3' markerWidth='6' markerHeight='6' refX='5' refY='3' orient='auto'>
      <path d='M1,1 L5,3 L1,5 Z' fill='#dc2626'/>
    </marker>
  </defs>
  <!-- O(40, 180), A(90, 50), B(310, 100), C = (A + 2B)/3 = (236.7, 83.3) -->
  <line x1='40' y1='180' x2='87' y2='55' stroke='#2563eb' stroke-width='2.4' marker-end='url(#ar-s1)'/>
  <text x='50' y='110' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='15' fill='#2563eb'>a</text>

  <line x1='40' y1='180' x2='305' y2='102' stroke='#059669' stroke-width='2.4' marker-end='url(#ar-s2)'/>
  <text x='180' y='160' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='15' fill='#059669'>b</text>

  <line x1='40' y1='180' x2='233' y2='86' stroke='#dc2626' stroke-width='2.6' marker-end='url(#ar-s3)'/>
  <text x='140' y='115' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='15' fill='#dc2626'>c</text>

  <!-- Segment AB -->
  <line x1='90' y1='50' x2='310' y2='100' stroke='#94a3b8' stroke-width='1.8'/>
  <text x='155' y='64' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='13' fill='#475569'>m</text>
  <text x='270' y='86' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='13' fill='#475569'>n</text>

  <circle cx='40' cy='180' r='3.5' fill='#334155'/>
  <text x='25' y='194' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='14' fill='#334155'>O</text>
  <circle cx='90' cy='50' r='3.5' fill='#334155'/>
  <text x='80' y='40' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='14' fill='#334155'>A(a)</text>
  <circle cx='310' cy='100' r='3.5' fill='#334155'/>
  <text x='315' y='105' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='14' fill='#334155'>B(b)</text>
  <circle cx='236.7' cy='83.3' r='4' fill='#dc2626'/>
  <text x='235' y='72' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='14' fill='#dc2626'>C(c)</text>
</svg>"""

FIG_CENTROID_L22 = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 350 220' width='350' height='220'>
  <!-- Triangle A(175, 30), B(40, 180), C(310, 180) -->
  <!-- Midpoints: L on BC = (175, 180), M on AC = (242.5, 105), N on AB = (107.5, 105) -->
  <!-- Centroid G = (175, 130) -->
  <polygon points='175,30 40,180 310,180' fill='#93c5fd' fill-opacity='0.25' stroke='#2563eb' stroke-width='2'/>

  <!-- Medians -->
  <line x1='175' y1='30' x2='175' y2='180' stroke='#7c3aed' stroke-width='1.5' stroke-dasharray='4,4'/>
  <line x1='40' y1='180' x2='242.5' y2='105' stroke='#7c3aed' stroke-width='1.5' stroke-dasharray='4,4'/>
  <line x1='310' y1='180' x2='107.5' y2='105' stroke='#7c3aed' stroke-width='1.5' stroke-dasharray='4,4'/>

  <circle cx='175' cy='30' r='3.5' fill='#334155'/>
  <text x='170' y='20' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='14' fill='#334155'>A(a)</text>

  <circle cx='40' cy='180' r='3.5' fill='#334155'/>
  <text x='20' y='195' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='14' fill='#334155'>B(b)</text>

  <circle cx='310' cy='180' r='3.5' fill='#334155'/>
  <text x='315' y='195' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='14' fill='#334155'>C(c)</text>

  <circle cx='175' cy='130' r='4.5' fill='#dc2626'/>
  <text x='184' y='132' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='14' fill='#dc2626'>G(g)</text>
</svg>"""

FIG_LINE_CIRCLE_L22 = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 360 210' width='360' height='210'>
  <defs>
    <marker id='ar-lc' markerWidth='6' markerHeight='6' refX='5' refY='3' orient='auto'>
      <path d='M1,1 L5,3 L1,5 Z' fill='#2563eb'/>
    </marker>
  </defs>
  <!-- Circle with center C(230, 105), radius R = 60 -->
  <circle cx='230' cy='105' r='60' fill='#a7f3d0' fill-opacity='0.3' stroke='#059669' stroke-width='2'/>
  <circle cx='230' cy='105' r='3.5' fill='#059669'/>
  <text x='236' y='115' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='13' fill='#059669'>C(c)</text>

  <!-- Radius line to P(276, 66) -->
  <line x1='230' y1='105' x2='276' y2='66' stroke='#dc2626' stroke-width='1.8'/>
  <circle cx='276' cy='66' r='3.5' fill='#dc2626'/>
  <text x='284' y='65' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='13' fill='#dc2626'>P(r)</text>
  <text x='245' y='80' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='13' fill='#dc2626'>R</text>

  <!-- Line (L) on left -->
  <line x1='30' y1='170' x2='150' y2='40' stroke='#2563eb' stroke-width='2.2'/>
  <circle cx='70' cy='126.7' r='3.5' fill='#2563eb'/>
  <text x='48' y='125' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='13' fill='#2563eb'>A(a)</text>

  <!-- Direction vector u -->
  <line x1='70' y1='126.7' x2='110' y2='83.3' stroke='#7c3aed' stroke-width='2.6' marker-end='url(#ar-lc)'/>
  <text x='96' y='96' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='13' fill='#7c3aed'>u</text>
  <text x='155' y='45' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='14' fill='#2563eb'>(L)</text>
</svg>"""

FIG_RESULTANT_FORCE_L22 = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 350 200' width='350' height='200'>
  <defs>
    <marker id='ar-f1' markerWidth='6' markerHeight='6' refX='5' refY='3' orient='auto'>
      <path d='M1,1 L5,3 L1,5 Z' fill='#2563eb'/>
    </marker>
    <marker id='ar-f2' markerWidth='6' markerHeight='6' refX='5' refY='3' orient='auto'>
      <path d='M1,1 L5,3 L1,5 Z' fill='#059669'/>
    </marker>
    <marker id='ar-fr' markerWidth='6' markerHeight='6' refX='5' refY='3' orient='auto'>
      <path d='M1,1 L5,3 L1,5 Z' fill='#dc2626'/>
    </marker>
  </defs>
  <!-- Object box at O(50, 150) -->
  <rect x='30' y='130' width='40' height='40' fill='#e2e8f0' stroke='#64748b' stroke-width='1.5' rx='3'/>
  <circle cx='50' cy='150' r='3.5' fill='#334155'/>

  <!-- F1 to (230, 150) -->
  <line x1='50' y1='150' x2='225' y2='150' stroke='#2563eb' stroke-width='2.4' marker-end='url(#ar-f1)'/>
  <text x='140' y='172' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='14' fill='#2563eb'>F1</text>

  <!-- F2 to (160, 50) -->
  <line x1='50' y1='150' x2='155' y2='55' stroke='#059669' stroke-width='2.4' marker-end='url(#ar-f2)'/>
  <text x='85' y='95' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='14' fill='#059669'>F2</text>

  <!-- Parallelogram lines to (340, 50) -->
  <line x1='230' y1='150' x2='340' y2='50' stroke='#94a3b8' stroke-width='1.5' stroke-dasharray='4,4'/>
  <line x1='160' y1='50' x2='340' y2='50' stroke='#94a3b8' stroke-width='1.5' stroke-dasharray='4,4'/>

  <!-- Resultant F -->
  <line x1='50' y1='150' x2='335' y2='53' stroke='#dc2626' stroke-width='2.8' marker-end='url(#ar-fr)'/>
  <text x='210' y='95' font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Cambria Math', 'Times New Roman', serif" font-style='italic' font-size='15' fill='#dc2626'>F = F1 + F2</text>
</svg>"""


def cands():
    C = []

    # =========================================================================
    # MCQ - EASY (target: 10, provide: 13)
    # =========================================================================

    C.append(mcq(
        'easy', 'sec1',
        'បើគេយក O ជាគល់នៃប្លង់ តើវ៉ិចទ័រទីតាំងនៃចំណុច P កំណត់ដោយអ្វី?',
        M(r'\vec{OP} = \vec{p}'),
        [M(r'\vec{PO} = \vec{p}'), M(r'P = O'), M(r'\vec{p} = 0')],
        'វ៉ិចទ័រទីតាំងនៃចំណុច P ដែលមាន O ជាគល់ គឺវ៉ិចទ័រ OP = p កំណត់សរសេរ P(p)។'
    ))

    C.append(mcq(
        'easy', 'sec1',
        'បើ ' + M(r'A(\vec{a})') + ' និង ' + M(r'B(\vec{b})') + ' ជាចំណុចពីរក្នុងប្លង់ តើ ' + M(r'\vec{AB}') + ' ស្មើនឹងអ្វី?',
        M(r'\vec{b} - \vec{a}'),
        [M(r'\vec{a} - \vec{b}'), M(r'\vec{a} + \vec{b}'), M(r'\vec{a} \cdot \vec{b}')],
        'AB = OB - OA = b - a (វ៉ិចទ័រទីតាំងចុងដកវ៉ិចទ័រទីតាំងគល់)។'
    ))

    C.append(mcq(
        'easy', 'sec1',
        'បើ M ជាចំណុចកណ្តាលនៃអង្កត់ AB ដែល ' + M(r'A(\vec{a})') + ' និង ' + M(r'B(\vec{b})') + ' នោះវ៉ិចទ័រទីតាំង ' + M(r'\vec{m}') + ' នៃ M គឺ៖',
        M(r'\vec{m} = \dfrac{\vec{a} + \vec{b}}{2}'),
        [M(r'\vec{m} = \dfrac{\vec{b} - \vec{a}}{2}'), M(r'\vec{m} = \vec{a} + \vec{b}'), M(r'\vec{m} = 2(\vec{a} + \vec{b})')],
        'វ៉ិចទ័រទីតាំងចំណុចកណ្តាល M គឺ m = (a + b) / 2។'
    ))

    C.append(with_img(mcq(
        'easy', 'sec1',
        'ពិនិត្យរូបភាពខាងក្រោម។ ចំណុច C ចែកអង្កត់ AB ខាងក្នុងតាមផលធៀប ' + M(r'm : n') + '។ តើរូបមន្តវ៉ិចទ័រទីតាំង ' + M(r'\vec{c}') + ' គឺ៖',
        M(r'\vec{c} = \dfrac{m\vec{b} + n\vec{a}}{m + n}'),
        [M(r'\vec{c} = \dfrac{m\vec{a} + n\vec{b}}{m + n}'), M(r'\vec{c} = \dfrac{m\vec{b} - n\vec{a}}{m - n}'), M(r'\vec{c} = \dfrac{\vec{a} + \vec{b}}{m + n}')],
        'រូបមន្តចំណុចចែកក្នុង: c = (m*b + n*a) / (m + n)។'
    ), FIG_SECTION_POINT_L22))

    C.append(with_img(mcq(
        'easy', 'sec2',
        'ពិនិត្យរូបភាពត្រីកោណ ABC ខាងក្រោម។ តើវ៉ិចទ័រទីតាំងនៃទីប្រជុំទម្ងន់ G កំណត់ដោយរូបមន្តណា?',
        M(r'\vec{g} = \dfrac{\vec{a} + \vec{b} + \vec{c}}{3}'),
        [M(r'\vec{g} = \dfrac{\vec{a} + \vec{b} + \vec{c}}{2}'), M(r'\vec{g} = \vec{a} + \vec{b} + \vec{c}'), M(r'\vec{g} = \dfrac{2\vec{a} + \vec{b} + \vec{c}}{4}')],
        'ទីប្រជុំទម្ងន់ G នៃត្រីកោណ ABC មានវ៉ិចទ័រទីតាំង g = (a + b + c) / 3។'
    ), FIG_CENTROID_L22))

    C.append(mcq(
        'easy', 'sec2',
        'បើ G ជាទីប្រជុំទម្ងន់នៃត្រីកោណ ABC តើផលបូក ' + M(r'\vec{GA} + \vec{GB} + \vec{GC}') + ' ស្មើនឹងអ្វី?',
        M(r'\vec{0}'),
        [M(r'3\vec{OG}'), M(r'\vec{AB} + \vec{BC}'), M(r'1')],
        'លក្ខណៈគ្រឹះនៃទីប្រជុំទម្ងន់ត្រីកោណគឺ GA + GB + GC = 0។'
    ))

    C.append(with_img(mcq(
        'easy', 'sec3',
        'ពិនិត្យរូបភាពខាងក្រោម។ សមីការវ៉ិចទ័រនៃរង្វង់ដែលមានផ្ចិត ' + M(r'C(\vec{c})') + ' និងកាំ ' + M(r'R') + ' គឺ៖',
        M(r'|\vec{r} - \vec{c}| = R'),
        [M(r'|\vec{r} + \vec{c}| = R'), M(r'\vec{r} \cdot \vec{c} = R^2'), M(r'|\vec{r}| = R')],
        'ចម្ងាយពីផ្ចិត C(c) ទៅចំណុច P(r) លើរង្វង់ស្មើកាំ R នាំឱ្យ |r - c| = R (ឬ (r - c)^2 = R^2)។'
    ), FIG_LINE_CIRCLE_L22))

    C.append(mcq(
        'easy', 'sec3',
        'បន្ទាត់ L កាត់តាមចំណុច ' + M(r'A(\vec{a})') + ' ហើយស្របនឹងវ៉ិចទ័រប្រាប់ទិស ' + M(r'\vec{u}') + '។ សមីការវ៉ិចទ័រនៃបន្ទាត់ L គឺ៖',
        M(r'\vec{r} = \vec{a} + t\vec{u}\quad (t \in \mathbb{R})'),
        [M(r'\vec{r} = t\vec{a} + \vec{u}'), M(r'\vec{r} = \vec{a} \cdot \vec{u}'), M(r'\vec{r} = \vec{a} - t\vec{u}^2')],
        'សមីការវ៉ិចទ័រនៃបន្ទាត់កាត់តាម A(a) ស្របនឹង u គឺ r = a + t*u។'
    ))

    C.append(mcq(
        'easy', 'sec3',
        'រកវ៉ិចទ័រណរម៉ាល់ (កែង) ' + M(r'\vec{n}') + ' នៃបន្ទាត់ ' + M(r'3x - 4y + 1 = 0') + '៖',
        M(r'\vec{n} = (3,\, -4)'),
        [M(r'\vec{n} = (4,\, 3)'), M(r'\vec{n} = (-3,\, -4)'), M(r'\vec{n} = (3,\, 4)')],
        'បន្ទាត់ ax + by + c = 0 មានវ៉ិចទ័រណរម៉ាល់ n = (a, b) = (3, -4)។'
    ))

    C.append(with_img(mcq(
        'easy', 'sec4',
        'ពិនិត្យរូបខាងក្រោម។ កម្លាំងពីរ ' + M(r'\vec{F}_1') + ' និង ' + M(r'\vec{F}_2') + ' មានចំណុចចាប់រួមគ្នា។ តើកម្លាំងផ្គួប ' + M(r'\vec{F}') + ' ស្មើនឹងអ្វី?',
        M(r'\vec{F} = \vec{F}_1 + \vec{F}_2'),
        [M(r'\vec{F} = \vec{F}_1 - \vec{F}_2'), M(r'\vec{F} = \vec{F}_1 \cdot \vec{F}_2'), M(r'F = F_1 \times F_2')],
        'កម្លាំងផ្គួបនៃកម្លាំងពីរមានចំណុចចាប់រួមគ្នាគឺផលបូកវ៉ិចទ័រ F = F_1 + F_2 តាមវិធានប្រលេឡូក្រាម។'
    ), FIG_RESULTANT_FORCE_L22))

    C.append(mcq(
        'easy', 'sec4',
        'តើរូបមន្តគណនាកម្មន្ត ' + M(r'W') + ' នៃកម្លាំងថេរ ' + M(r'\vec{F}') + ' លើបំលាស់ទី ' + M(r'\vec{d}') + ' គឺជាអ្វី?',
        M(r'W = \vec{F} \cdot \vec{d} = |\vec{F}||\vec{d}|\cos\theta'),
        [M(r'W = |\vec{F}| + |\vec{d}|'), M(r'W = |\vec{F}||\vec{d}|\sin\theta'), M(r'W = \dfrac{|\vec{F}|}{|\vec{d}|}')],
        'កម្មន្តនៃកម្លាំងគឺផលគុណស្កាលែរវាងកម្លាំងនិងបំលាស់ទី W = F . d = |F||d|cos theta។'
    ))

    C.append(mcq(
        'easy', 'sec4',
        'អង្គធាតុមួយស្ថិតក្នុងសភាពលំនឹងក្រោមអំពើនៃកម្លាំងបី ' + M(r'\vec{F}_1,\, \vec{F}_2,\, \vec{F}_3') + '។ តើទំនាក់ទំនងណាត្រឹមត្រូវ?',
        M(r'\vec{F}_1 + \vec{F}_2 + \vec{F}_3 = \vec{0}'),
        [M(r'F_1 + F_2 + F_3 = 0'), M(r'\vec{F}_1 = \vec{F}_2 = \vec{F}_3'), M(r'\vec{F}_1 \cdot \vec{F}_2 = \vec{F}_3')],
        'លក្ខខណ្ឌលំនឹងនៃអង្គធាតុគឺផលបូកវ៉ិចទ័រកម្លាំងស្មើវ៉ិចទ័រសូន្យ sum F = 0។'
    ))

    C.append(mcq(
        'easy', 'sec4',
        'កម្លាំងថេរ ' + M(r'F = 30\text{ N}') + ' រុញរទេះឱ្យបំលាស់ទីបាន ' + M(r'd = 5\text{ m}') + ' ស្របទិសដៅនៃកម្លាំង (' + M(r'\theta = 0^\circ') + ')។ គណនាកម្មន្ត W៖',
        M(r'150\text{ J}'),
        [M(r'6\text{ J}'), M(r'0\text{ J}'), M(r'25\text{ J}')],
        'W = F * d * cos 0° = 30 * 5 * 1 = 150 J (Joules)។'
    ))

    # =========================================================================
    # MCQ - MEDIUM (target: 14, provide: 17)
    # =========================================================================

    C.append(mcq(
        'medium', 'sec1',
        'គេមាន ' + M(r'A(2,\, 5)') + ' និង ' + M(r'B(8,\, 11)') + '។ រកកូអរដោនេនៃចំណុចកណ្តាល M នៃអង្កត់ AB៖',
        M(r'M(5,\, 8)'),
        [M(r'M(6,\, 6)'), M(r'M(10,\, 16)'), M(r'M(4,\, 3)')],
        'x_M = (2 + 8)/2 = 5 និង y_M = (5 + 11)/2 = 8 នាំឱ្យ M(5, 8)។'
    ))

    C.append(mcq(
        'medium', 'sec1',
        'ចំណុច C ចែកអង្កត់ AB ខាងក្នុងតាមផលធៀប 2:1។ រកកន្សោម ' + M(r'\vec{c}') + ' ជាអនុគមន៍នៃ ' + M(r'\vec{a}') + ' និង ' + M(r'\vec{b}') + '៖',
        M(r'\vec{c} = \dfrac{\vec{a} + 2\vec{b}}{3}'),
        [M(r'\vec{c} = \dfrac{2\vec{a} + \vec{b}}{3}'), M(r'\vec{c} = \dfrac{\vec{a} + \vec{b}}{3}'), M(r'\vec{c} = 2\vec{b} - \vec{a}')],
        'c = (2b + 1a) / (2 + 1) = (a + 2b) / 3។'
    ))

    C.append(mcq(
        'medium', 'sec1',
        'គេមានចំណុច ' + M(r'A(1,\, 2)') + ' និង ' + M(r'B(7,\, 5)') + '។ ចំណុច C ចែក AB ខាងក្នុងតាមផលធៀប 2:1 (AC : CB = 2 : 1)។ រកកូអរដោនេនៃ C៖',
        M(r'C(5,\, 4)'),
        [M(r'C(4,\, 3.5)'), M(r'C(3,\, 3)'), M(r'C(6,\, 4.5)')],
        'x_C = (1 + 2(7))/3 = 15/3 = 5 និង y_C = (2 + 2(5))/3 = 12/3 = 4 នាំឱ្យ C(5, 4)។'
    ))

    C.append(mcq(
        'medium', 'sec2',
        'ត្រីកោណ ABC មានកំពូល ' + M(r'A(1,\, 2),\, B(3,\, 8),\, C(5,\, 2)') + '។ រកកូអរដោនេនៃទីប្រជុំទម្ងន់ G នៃត្រីកោណ ABC៖',
        M(r'G(3,\, 4)'),
        [M(r'G(4,\, 4)'), M(r'G(3,\, 6)'), M(r'G(9,\, 12)')],
        'x_G = (1 + 3 + 5)/3 = 9/3 = 3 និង y_G = (2 + 8 + 2)/3 = 12/3 = 4 នាំឱ្យ G(3, 4)។'
    ))

    C.append(mcq(
        'medium', 'sec3',
        'បន្ទាត់ L កាត់តាមចំណុច ' + M(r'A(2,\, -1)') + ' ហើយមានវ៉ិចទ័រប្រាប់ទិស ' + M(r'\vec{u} = (3,\, 5)') + '។ សមីការប៉ារ៉ាម៉ែត្រនៃបន្ទាត់ L គឺ៖',
        M(r'\begin{cases} x = 2 + 3t \\ y = -1 + 5t \end{cases}'),
        [M(r'\begin{cases} x = 3 + 2t \\ y = 5 - t \end{cases}'), M(r'\begin{cases} x = 2 - 3t \\ y = -1 - 5t \end{cases}'), M(r'\begin{cases} x = 2 + 5t \\ y = -1 + 3t \end{cases}')],
        'សមីការប៉ារ៉ាម៉ែត្រ: x = x_0 + at = 2 + 3t និង y = y_0 + bt = -1 + 5t។'
    ))

    C.append(mcq(
        'medium', 'sec3',
        'បន្ទាត់មួយកាត់តាមចំណុច ' + M(r'A(1,\, 3)') + ' និងកែងនឹងវ៉ិចទ័រណរម៉ាល់ ' + M(r'\vec{n} = (2,\, -1)') + '។ សមីការទូទៅនៃបន្ទាត់នោះគឺ៖',
        M(r'2x - y + 1 = 0'),
        [M(r'2x - y - 1 = 0'), M(r'2x + y - 5 = 0'), M(r'x + 2y - 7 = 0')],
        '2(x - 1) - 1(y - 3) = 0 <=> 2x - 2 - y + 3 = 0 <=> 2x - y + 1 = 0។'
    ))

    C.append(mcq(
        'medium', 'sec3',
        'រង្វង់មួយមានផ្ចិត ' + M(r'C(3,\, -2)') + ' និងកាំ ' + M(r'R = 4') + '។ សមីការស្តង់ដានៃរង្វង់នេះគឺ៖',
        M(r'(x - 3)^2 + (y + 2)^2 = 16'),
        [M(r'(x + 3)^2 + (y - 2)^2 = 16'), M(r'(x - 3)^2 + (y + 2)^2 = 4'), M(r'(x - 3)^2 + (y - 2)^2 = 16')],
        'តាមរូបមន្ត (x - a)^2 + (y - b)^2 = R^2: (x - 3)^2 + (y + 2)^2 = 16។'
    ))

    C.append(mcq(
        'medium', 'sec4',
        'កម្លាំងពីរស្មើគ្នា ' + M(r'F_1 = F_2 = 10\text{ N}') + ' បង្កើតបានមុំ ' + M(r'60^\circ') + ' រវាងគ្នា។ គណនាម៉ូឌុលនៃកម្លាំងផ្គួប ' + M(r'F') + '៖',
        M(r'10\sqrt{3}\text{ N}\approx 17.32\text{ N}'),
        [M(r'20\text{ N}'), M(r'10\text{ N}'), M(r'15\text{ N}')],
        'F = sqrt(10^2 + 10^2 + 2(10)(10)cos 60°) = sqrt(100 + 100 + 100) = sqrt(300) = 10*sqrt(3) N។'
    ))

    C.append(mcq(
        'medium', 'sec4',
        'កម្លាំង ' + M(r'\vec{F} = (8,\, 6)') + ' N បានធ្វើឱ្យអង្គធាតុមួយបំលាស់ទីបាន ' + M(r'\vec{d} = (5,\, 2)') + ' m។ គណនាកម្មន្ត W ដែលកម្លាំងបានបំពេញ៖',
        M(r'52\text{ J}'),
        [M(r'40\text{ J}'), M(r'26\text{ J}'), M(r'64\text{ J}')],
        'W = F . d = (8)(5) + (6)(2) = 40 + 12 = 52 J។'
    ))

    C.append(mcq(
        'medium', 'sec4',
        'កម្លាំង ' + M(r'F = 40\text{ N}') + ' ទាញប្រអប់មួយបានចម្ងាយ ' + M(r'd = 10\text{ m}') + ' ដោយខ្សែពួរបង្កើតមុំ ' + M(r'60^\circ') + ' ធៀបនឹងប្លង់ដេក។ គណនាកម្មន្ត W៖',
        M(r'200\text{ J}'),
        [M(r'400\text{ J}'), M(r'200\sqrt{3}\text{ J}'), M(r'100\text{ J}')],
        'W = F * d * cos 60° = 40 * 10 * (1/2) = 200 J។'
    ))

    C.append(mcq(
        'medium', 'sec1',
        'ចំណុច D ចែកអង្កត់ AB ខាងក្រៅតាមផលធៀប 3:1។ រកកន្សោម ' + M(r'\vec{d}') + ' ជាអនុគមន៍នៃ ' + M(r'\vec{a}') + ' និង ' + M(r'\vec{b}') + '៖',
        M(r'\vec{d} = \dfrac{3\vec{b} - \vec{a}}{2}'),
        [M(r'\vec{d} = \dfrac{3\vec{b} + \vec{a}}{4}'), M(r'\vec{d} = \dfrac{\vec{b} - 3\vec{a}}{2}'), M(r'\vec{d} = 3\vec{b} - \vec{a}')],
        'd = (3b - 1a) / (3 - 1) = (3b - a) / 2។'
    ))

    C.append(mcq(
        'medium', 'sec2',
        'គេមានត្រីកោណ ABC ដែលមានកំពូល ' + M(r'A(2,\, 1),\, B(4,\, 7)') + ' និងទីប្រជុំទម្ងន់ ' + M(r'G(3,\, 5)') + '។ រកកូអរដោនេនៃកំពូល C៖',
        M(r'C(3,\, 7)'),
        [M(r'C(6,\, 8)'), M(r'C(3,\, 5)'), M(r'C(1,\, 3)')],
        'x_C = 3(3) - (2 + 4) = 9 - 6 = 3; y_C = 3(5) - (1 + 7) = 15 - 8 = 7 នាំឱ្យ C(3, 7)។'
    ))

    C.append(mcq(
        'medium', 'sec3',
        'សមីការប៉ារ៉ាម៉ែត្រនៃបន្ទាត់មួយគឺ ' + M(r'\begin{cases} x = 3 - 2t \\ y = 1 + 4t \end{cases}') + '។ រកវ៉ិចទ័រប្រាប់ទិស ' + M(r'\vec{u}') + ' នៃបន្ទាត់នោះ៖',
        M(r'\vec{u} = (-2,\, 4)'),
        [M(r'\vec{u} = (3,\, 1)'), M(r'\vec{u} = (2,\, 4)'), M(r'\vec{u} = (4,\, -2)')],
        'មេគុណមុខ t គឺ a = -2 និង b = 4 នាំឱ្យវ៉ិចទ័រប្រាប់ទិស u = (-2, 4) (ឬកូលីនេអ៊ែរនឹង (-1, 2))។'
    ))

    C.append(mcq(
        'medium', 'sec4',
        'កម្លាំងបី ' + M(r'\vec{F}_1 = (3,\, 4),\, \vec{F}_2 = (-1,\, 2),\, \vec{F}_3') + ' ធ្វើឱ្យអង្គធាតុមួយមានលំនឹង (' + M(r'\sum\vec{F} = \vec{0}') + ')។ រកកូអរដោនេនៃ ' + M(r'\vec{F}_3') + '៖',
        M(r'\vec{F}_3 = (-2,\, -6)'),
        [M(r'\vec{F}_3 = (2,\, 6)'), M(r'\vec{F}_3 = (-2,\, 6)'), M(r'\vec{F}_3 = (4,\, 2)')],
        'F_3 = -(F_1 + F_2) = -((3 - 1, 4 + 2)) = -(2, 6) = (-2, -6) N។'
    ))

    C.append(mcq(
        'medium', 'sec1',
        'បើ ' + M(r'M(4,\, 3)') + ' ជាចំណុចកណ្តាលនៃអង្កត់ AB ហើយ ' + M(r'A(1,\, 1)') + '។ រកកូអរដោនេនៃចំណុច B៖',
        M(r'B(7,\, 5)'),
        [M(r'B(5,\, 2)'), M(r'B(9,\, 7)'), M(r'B(3,\, 2)')],
        'x_B = 2(4) - 1 = 7; y_B = 2(3) - 1 = 5 នាំឱ្យ B(7, 5)។'
    ))

    C.append(mcq(
        'medium', 'sec3',
        'បន្ទាត់មួយកាត់តាមចំណុចពីរ ' + M(r'A(1,\, 2)') + ' និង ' + M(r'B(4,\, 5)') + '។ វ៉ិចទ័រប្រាប់ទិស ' + M(r'\vec{u}') + ' នៃបន្ទាត់នោះគឺ៖',
        M(r'\vec{u} = (3,\, 3)\text{ ឬ }(1,\, 1)'),
        [M(r'\vec{u} = (5,\, 7)'), M(r'\vec{u} = (3,\, -3)'), M(r'\vec{u} = (-3,\, 3)')],
        'u = AB = (4 - 1, 5 - 2) = (3, 3) ស្របនឹង (1, 1)។'
    ))

    C.append(mcq(
        'medium', 'sec4',
        'កម្លាំង ' + M(r'F = 100\text{ N}') + ' បញ្ចេញលើអង្គធាតុមួយឱ្យរំកិលបាន ' + M(r'd = 8\text{ m}') + '។ កម្មន្តដែលទទួលបានគឺ ' + M(r'W = 400\text{ J}') + '។ គណនាមុំ ' + M(r'\theta') + ' រវាងកម្លាំងនិងបំលាស់ទី៖',
        M(r'60^\circ'),
        [M(r'30^\circ'), M(r'45^\circ'), M(r'90^\circ')],
        'cos theta = W / (F * d) = 400 / (100 * 8) = 400 / 800 = 0.5 នាំឱ្យ theta = 60°។'
    ))

    # =========================================================================
    # MCQ - HARD (target: 7, provide: 10)
    # =========================================================================

    C.append(mcq(
        'hard', 'sec1',
        'ក្នុងត្រីកោណ ABC ចំណុច D ចែក BC តាមផលធៀប ' + M(r'BD : DC = 1 : 2') + '។ កន្សោម ' + M(r'\vec{AD}') + ' ជាអនុគមន៍នៃ ' + M(r'\vec{AB}') + ' និង ' + M(r'\vec{AC}') + ' គឺ៖',
        M(r'\vec{AD} = \dfrac{2}{3}\vec{AB} + \dfrac{1}{3}\vec{AC}'),
        [M(r'\vec{AD} = \dfrac{1}{3}\vec{AB} + \dfrac{2}{3}\vec{AC}'), M(r'\vec{AD} = \dfrac{1}{2}(\vec{AB} + \vec{AC})'), M(r'\vec{AD} = 2\vec{AB} - \vec{AC}')],
        'D ចែក BC តាមផលធៀប 1:2 នាំឱ្យ AD = (2*AB + 1*AC) / (1 + 2) = (2/3)AB + (1/3)AC។'
    ))

    C.append(mcq(
        'hard', 'sec2',
        'បើ G ជាទីប្រជុំទម្ងន់ត្រីកោណ ABC និង O ជាចំណុចណាមួយក្នុងប្លង់ បង្ហាញថា ' + M(r'\vec{OA} + \vec{OB} + \vec{OC} = 3\vec{OG}') + '។ បើ ' + M(r'\vec{OA} + \vec{OB} + \vec{OC} = \vec{0}') + ' តើ O ជាចំណុចណា?',
        'O ជាទីប្រជុំទម្ងន់ G នៃត្រីកោណ ABC',
        ['O ជាផ្ចិតរង្វង់ចារឹកក្រៅត្រីកោណ', 'O ជាអរតូសង់នៃត្រីកោណ', 'O ជាចំណុចកណ្តាលនៃ BC'],
        'OA + OB + OC = 3OG។ បើ OA + OB + OC = 0 នាំឱ្យ 3OG = 0 <=> OG = 0 <=> O ត្រួតស៊ីគ្នានឹង G។'
    ))

    C.append(mcq(
        'hard', 'sec3',
        'បន្ទាត់មួយមានសមីការវ៉ិចទ័រ ' + M(r'\vec{r} = (1,\, 2) + t(3,\, -1)') + '។ សរសេរសមីការទូទៅនៃបន្ទាត់នោះតាមទម្រង់ ' + M(r'ax + by + c = 0') + '៖',
        M(r'x + 3y - 7 = 0'),
        [M(r'3x - y - 1 = 0'), M(r'x - 3y + 5 = 0'), M(r'3x + y - 5 = 0')],
        'x = 1 + 3t => t = (x - 1)/3; y = 2 - t => t = 2 - y។ ស្មើគ្នា: (x - 1)/3 = 2 - y <=> x - 1 = 6 - 3y <=> x + 3y - 7 = 0។'
    ))

    C.append(mcq(
        'hard', 'sec3',
        'រកសមីការបន្ទាត់ប៉ះទៅនឹងរង្វង់ ' + M(r'x^2 + y^2 = 25') + ' ត្រង់ចំណុច ' + M(r'P_0(3,\, 4)') + ' ដោយប្រើផលគុណស្កាលែនៃវ៉ិចទ័រ៖',
        M(r'3x + 4y - 25 = 0'),
        [M(r'4x - 3y = 0'), M(r'3x + 4y + 25 = 0'), M(r'3x - 4y + 7 = 0')],
        'វ៉ិចទ័រកាំ OP_0 = (3, 4) ជាវ៉ិចទ័រណរម៉ាល់នៃបន្ទាត់ប៉ះត្រង់ P_0 នាំឱ្យ 3(x - 3) + 4(y - 4) = 0 <=> 3x + 4y - 25 = 0។'
    ))

    C.append(mcq(
        'hard', 'sec4',
        'កម្លាំងពីរមានម៉ូឌុល ' + M(r'F_1 = 6\text{ N}') + ' និង ' + M(r'F_2 = 10\text{ N}') + '។ តើកម្លាំងផ្គួប ' + M(r'F') + ' អាចមានតម្លៃក្នុងចន្លោះណា?',
        M(r'[4\text{ N},\, 16\text{ N}]'),
        [M(r'[6\text{ N},\, 10\text{ N}]'), M(r'[0\text{ N},\, 16\text{ N}]'), M(r'[8\text{ N},\, 12\text{ N}]')],
        'F_min = |F_1 - F_2| = |6 - 10| = 4 N (ទិសដៅផ្ទុយ) និង F_max = F_1 + F_2 = 16 N (ទិសដៅដូចគ្នា) នាំឱ្យ F in [4 N, 16 N]។'
    ))

    C.append(mcq(
        'hard', 'sec4',
        'កម្លាំងបី ' + M(r'\vec{F}_1,\, \vec{F}_2,\, \vec{F}_3') + ' មានទំហំស្មើគ្នា ' + M(r'10\text{ N}') + ' មានចំណុចចាប់រួម O និងមានទិសដៅបង្កើតបានមុំ ' + M(r'120^\circ') + ' រវាងពីរបន្តបន្ទាប់។ តើកម្លាំងផ្គួបសរុបស្មើនឹងប៉ុន្មាន?',
        M(r'0\text{ N}'),
        [M(r'10\text{ N}'), M(r'30\text{ N}'), M(r'10\sqrt{3}\text{ N}')],
        'កម្លាំងបីស្មើគ្នាបែងចែកមុំស្មើៗគ្នា 120° ជុំវិញចំណុចមួយ មានផលបូកវ៉ិចទ័រស្មើ 0 N (លំនឹងស៊ីមេទ្រី)។'
    ))

    C.append(mcq(
        'hard', 'sec3',
        'គេមានចំណុច ' + M(r'A(1,\, 1)') + ' និង ' + M(r'B(5,\, 3)') + '។ សមីការមេដ្យាទ័រនៃអង្កត់ AB (បន្ទាត់កាត់តាមចំណុចកណ្តាលនិងកែង AB) គឺ៖',
        M(r'2x + y - 8 = 0'),
        [M(r'2x - y - 4 = 0'), M(r'x + 2y - 7 = 0'), M(r'4x + 2y - 15 = 0')],
        'AB = (4, 2) ស្របនឹង n = (2, 1) ជាវ៉ិចទ័រណរម៉ាល់។ ចំណុចកណ្តាល M = (3, 2)។ សមីការ: 2(x - 3) + 1(y - 2) = 0 <=> 2x + y - 8 = 0។'
    ))

    C.append(mcq(
        'hard', 'sec2',
        'ត្រីកោណ ABC មានទីប្រជុំទម្ងន់ G។ ចំណុច M ជាចំណុចកណ្តាលនៃ AG។ បង្ហាញថា ' + M(r'4\vec{MA} + \vec{MB} + \vec{MC} = \vec{0}') + ' ឬទំនាក់ទំនង ' + M(r'\vec{AM}') + ' ស្មើនឹង៖',
        M(r'\vec{AM} = \dfrac{1}{6}(\vec{AB} + \vec{AC})'),
        [M(r'\vec{AM} = \dfrac{1}{3}(\vec{AB} + \vec{AC})'), M(r'\vec{AM} = \dfrac{1}{4}(\vec{AB} + \vec{AC})'), M(r'\vec{AM} = \vec{AB} + \vec{AC}')],
        'AG = (2/3)AL = (2/3)(1/2)(AB + AC) = (1/3)(AB + AC)។ M ជាចំណុចកណ្តាល AG នាំឱ្យ AM = (1/2)AG = (1/6)(AB + AC)។'
    ))

    C.append(mcq(
        'hard', 'sec4',
        'កម្លាំង ' + M(r'\vec{F} = 2\vec{i} + 5\vec{j}') + ' N ធ្វើឱ្យអង្គធាតុផ្លាស់ទីពី ' + M(r'A(1,\, 2)') + ' ទៅ ' + M(r'B(4,\, 6)') + ' (គិតជាម៉ែត្រ)។ គណនាកម្មន្ត W៖',
        M(r'26\text{ J}'),
        [M(r'30\text{ J}'), M(r'20\text{ J}'), M(r'52\text{ J}')],
        'd = AB = (4 - 1, 6 - 2) = (3, 4) m។ W = F . d = (2)(3) + (5)(4) = 6 + 20 = 26 J។'
    ))

    C.append(mcq(
        'hard', 'sec1',
        'គេមានចំណុច ' + M(r'A(\vec{a}),\, B(\vec{b}),\, C(\vec{c})') + '។ លក្ខខណ្ឌចាំបាច់និងគ្រប់គ្រាន់ដើម្បីឱ្យ A, B, C រត់ត្រង់ជួរគ្នាគឺមានចំនួនពិត ' + M(r'\alpha,\, \beta,\, \gamma') + ' មិនសូន្យព្រមគ្នាដែល ៖',
        M(r'\alpha\vec{a} + \beta\vec{b} + \gamma\vec{c} = \vec{0}\text{ និង }\alpha + \beta + \gamma = 0'),
        [M(r'\vec{a} + \vec{b} + \vec{c} = \vec{0}'), M(r'\alpha\vec{a} + \beta\vec{b} + \gamma\vec{c} = \vec{0}\text{ និង }\alpha + \beta + \gamma = 1'), M(r'\vec{a} \cdot \vec{b} \cdot \vec{c} = 0')],
        'ទ្រឹស្តីបទបារីសង់ត្រង់ជួរ: alpha*a + beta*b + gamma*c = 0 ជាមួយ alpha + beta + gamma = 0។'
    ))

    # =========================================================================
    # MCQ - PISA (target: 5, provide: 7)
    # =========================================================================

    C.append(mcq(
        'pisa', 'pisa',
        'PISA អាកាសចរណ៍: យន្តហោះដឹកអ្នកដំណើរមួយត្រូវហោះហើរឆ្ពោះទៅទិសខាងកើតត្រង់ពីភ្នំពេញទៅកាន់ទីក្រុងហូជីមិញ។ ប្រសិនបើមានខ្យល់ព្យុះបក់ខ្លាំងពីទិសខាងត្បូងទៅជើង តើអ្នកបើកបរត្រូវតម្រង់ក្បាលយន្តហោះឆ្ពោះទៅទិសណាដើម្បីកុំឱ្យយន្តហោះរសាត់ខុសផ្លូវ?',
        'តម្រង់ក្បាលយន្តហោះបញ្ឆិតទៅទិសអាគ្នេយ៍ (East-Southeast)',
        ['តម្រង់ក្បាលយន្តហោះទៅទិសឦសាន', 'តម្រង់ក្បាលយន្តហោះទៅទិសខាងកើតត្រង់', 'តម្រង់ក្បាលយន្តហោះទៅទិសខាងជើង'],
        'ដើម្បីបន្សាបសមាសភាគល្បឿនខ្យល់ដែលរុញទៅជើង យន្តហោះត្រូវមានសមាសភាគល្បឿនចង្អុលទៅត្បូង ដូច្នេះត្រូវតម្រង់ទៅទិសអាគ្នេយ៍។'
    ))

    C.append(mcq(
        'pisa', 'pisa',
        'PISA ស្ទូចទំនិញកំពង់ផែ: ស្ទូចមួយលើកកុងតឺន័រទម្ងន់ 20000 N ឡើងលើដោយល្បឿនថេរតាមទិសឈរបានកម្ពស់ 15 m។ គណនាកម្មន្តដែលស្ទូចបានបំពេញ៖',
        M(r'300000\text{ J} = 300\text{ kJ}'),
        [M(r'1333.3\text{ J}'), M(r'0\text{ J}'), M(r'20015\text{ J}')],
        'W = F * d = 20000 * 15 = 300000 J = 300 kJ (theta = 0° ព្រោះកម្លាំងលើកស្របទិសដៅបំលាស់ទី)។'
    ))

    C.append(mcq(
        'pisa', 'pisa',
        'PISA អាជីវកម្មអូសទូក: គេប្រើសេះពីរដើម្បីអូសទូកមួយតាមព្រែកជីក។ សេះទាំងពីរបញ្ចេញកម្លាំងស្មើគ្នា ' + M(r'F_1 = F_2 = 800\text{ N}') + ' នៅសងខាងច្រាំងព្រែក ដោយខ្សែពួរទាំងពីរបង្កើតបានមុំ ' + M(r'60^\circ') + ' រវាងគ្នា។ គណនាកម្លាំងផ្គួបដែលទាញទូកទៅមុខតាមបណ្តោយព្រែក៖',
        M(r'800\sqrt{3}\text{ N}\approx 1385.6\text{ N}'),
        [M(r'1600\text{ N}'), M(r'800\text{ N}'), M(r'1200\text{ N}')],
        'F_res = 2 * F * cos(30°) = 2 * 800 * (sqrt(3)/2) = 800*sqrt(3) ≈ 1385.64 N។'
    ))

    C.append(mcq(
        'pisa', 'pisa',
        'PISA កីឡាជិះទូកក្តោង: ទូកក្តោងមួយត្រូវបានកម្លាំងខ្យល់ ' + M(r'\vec{F} = (120,\, 50)') + ' N រុញច្រានឱ្យបំលាស់ទីបាន ' + M(r'\vec{d} = (200,\, 0)') + ' m តាមបណ្តោយទិសដេក។ គណនាកម្មន្តដែលខ្យល់បានបង្កើតឡើង៖',
        M(r'24000\text{ J} = 24\text{ kJ}'),
        [M(r'10000\text{ J}'), M(r'34000\text{ J}'), M(r'26000\text{ J}')],
        'W = F . d = (120)(200) + (50)(0) = 24000 J = 24 kJ។'
    ))

    C.append(mcq(
        'pisa', 'pisa',
        'PISA រចនាសម្ព័ន្ធស្ពាន: ខ្សែខ្សែកាបព្យួរស្ពានមួយត្រូវបានរចនាឱ្យទប់កម្លាំងផ្គួបនៃទម្ងន់ស្ពាន។ ប្រសិនបើកម្លាំងទម្ងន់ស្ពានទាញចុះក្រោម 50000 N ហើយខ្សែខ្សែកាបពីរសងខាងបញ្ចេញកម្លាំងតំណឹងស្មើគ្នា T មុំ 45 ដឺក្រេធៀបនឹងទិសឈរ តើ T ត្រូវស្មើនឹងប៉ុន្មានដើម្បីឱ្យស្ពានមានលំនឹង?',
        M(r'25000\sqrt{2}\text{ N}\approx 35355\text{ N}'),
        [M(r'25000\text{ N}'), M(r'50000\text{ N}'), M(r'35000\text{ N}')],
        'លំនឹងទិសឈរ: 2T cos 45° = 50000 => 2T(sqrt(2)/2) = 50000 => T*sqrt(2) = 50000 => T = 25000*sqrt(2) ≈ 35355.3 N។'
    ))

    C.append(mcq(
        'pisa', 'pisa',
        'PISA ចរាចរណ៍លើជម្រាល: ឡានមួយទម្ងន់ 15000 N ចតនៅលើផ្លូវជម្រាលភ្នំដែលមានមុំទេរ 30 ដឺក្រេធៀបនឹងប្លង់ដេក។ គណនាសមាសភាគកម្លាំងទម្ងន់ដែលទាញឡានឱ្យរអិលចុះតាមជម្រាល (' + M(r'F_{\parallel} = P \sin 30^\circ') + ')៖',
        M(r'7500\text{ N}'),
        [M(r'15000\text{ N}'), M(r'12990\text{ N}'), M(r'5000\text{ N}')],
        'F_parallel = P * sin 30° = 15000 * 0.5 = 7500 N។'
    ))

    C.append(mcq(
        'pisa', 'pisa',
        'PISA ស្ថានីយអវកាស: យានអវកាសមួយបញ្ឆេះម៉ាស៊ីនជំរុញដោយកម្លាំង ' + M(r'\vec{F} = (500,\, -200)') + ' N ក្នុងលំហគ្មានទំនាញផែនដី ធ្វើឱ្យយានបំលាស់ទីបាន ' + M(r'\vec{d} = (30,\, 40)') + ' m។ គណនាកម្មន្តសរុបដែលម៉ាស៊ីនបានបំពេញ៖',
        M(r'7000\text{ J} = 7\text{ kJ}'),
        [M(r'23000\text{ J}'), M(r'15000\text{ J}'), M(r'-7000\text{ J}')],
        'W = F . d = (500)(30) + (-200)(40) = 15000 - 8000 = 7000 J = 7 kJ។'
    ))

    # =========================================================================
    # WRITING - EASY (target: 1, provide: 2)
    # =========================================================================

    C.append(wr(
        'easy', 'sec1',
        'ក្នុងប្លង់កូអរដោនេ គេមានចំណុច ' + M(r'A(2,\, 3)') + ' និង ' + M(r'B(6,\, 7)') + '។\n'
        'ក. សរសេរវ៉ិចទ័រទីតាំង ' + M(r'\vec{a}') + ' និង ' + M(r'\vec{b}') + ' នៃចំណុច A និង B។\n'
        'ខ. គណនាកូអរដោនេនៃចំណុចកណ្តាល M នៃអង្កត់ AB ដោយប្រើរូបមន្តវ៉ិចទ័រទីតាំង។',
        [
            ('សរសេរវ៉ិចទ័រទីតាំង: \\vec{a} = \\vec{OA} = (2, 3) និង \\vec{b} = \\vec{OB} = (6, 7)', 1.5),
            ('សរសេររូបមន្តចំណុចកណ្តាល: \\vec{m} = \\dfrac{\\vec{a} + \\vec{b}}{2}', 1.5),
            ('ជំនួសតម្លៃគណនា: \\vec{m} = \\dfrac{(2 + 6, 3 + 7)}{2} = \\dfrac{(8, 10)}{2} = (4, 5)', 1),
            ('សន្និដ្ឋានកូអរដោនេ: M(4, 5)', 1)
        ]
    ))

    C.append(wr(
        'easy', 'sec3',
        'គេមានចំណុច ' + M(r'A(1,\, 4)') + ' និងវ៉ិចទ័រប្រាប់ទិស ' + M(r'\vec{u} = (2,\, -3)') + '។\n'
        'ក. សរសេរសមីការវ៉ិចទ័រនៃបន្ទាត់ L កាត់តាម A ស្របនឹង ' + M(r'\vec{u}') + '។\n'
        'ខ. សរសេរសមីការប៉ារ៉ាម៉ែត្រនៃបន្ទាត់ L នេះ។',
        [
            ('សរសេររូបមន្តសមីការវ៉ិចទ័រ: \\vec{r} = \\vec{a} + t\\vec{u}', 1.5),
            ('ជំនួសតម្លៃ: \\vec{r} = (1, 4) + t(2, -3) (t \\in \\mathbb{R})', 1.5),
            ('ទាញសមីការប៉ារ៉ាម៉ែត្រសម្រាប់ x: x = 1 + 2t', 1),
            ('ទាញសមីការប៉ារ៉ាម៉ែត្រសម្រាប់ y: y = 4 - 3t (t \\in \\mathbb{R})', 1)
        ]
    ))

    # =========================================================================
    # WRITING - MEDIUM (target: 4, provide: 5)
    # =========================================================================

    C.append(wr(
        'medium', 'sec1',
        'គេមានចំណុច ' + M(r'A(1,\, 2)') + ' និង ' + M(r'B(7,\, 8)') + '។ ចំណុច C ចែកអង្កត់ AB ខាងក្នុងតាមផលធៀប ' + M(r'2 : 1') + ' (គឺ ' + M(r'AC : CB = 2 : 1') + ')។\n'
        'ក. សរសេររូបមន្តវ៉ិចទ័រទីតាំង ' + M(r'\vec{c}') + ' ជាអនុគមន៍នៃ ' + M(r'\vec{a}') + ' និង ' + M(r'\vec{b}') + '។\n'
        'ខ. គណនាកូអរដោនេនៃចំណុច C។',
        [
            ('សរសេររូបមន្តចំណុចចែកក្នុង: \\vec{c} = \\dfrac{m\\vec{b} + n\\vec{a}}{m + n}', 1.5),
            ('ជំនួស m = 2, n = 1: \\vec{c} = \\dfrac{2\\vec{b} + \\vec{a}}{3}', 1),
            ('គណនា x_C: x_C = (2(7) + 1)/3 = (14 + 1)/3 = 5', 1.5),
            ('គណនា y_C: y_C = (2(8) + 2)/3 = (16 + 2)/3 = 6 នាំឱ្យ C(5, 6)', 1)
        ]
    ))

    C.append(wr(
        'medium', 'sec2',
        'គេមានត្រីកោណ ABC ដែលមានកំពូល ' + M(r'A(2,\, 4),\, B(6,\, 2),\, C(4,\, 9)') + ' ក្នុងប្លង់កូអរដោនេ។\n'
        'ក. រកកូអរដោនេនៃទីប្រជុំទម្ងន់ G នៃត្រីកោណ ABC។\n'
        'ខ. គណនាផលបូកវ៉ិចទ័រ ' + M(r'\vec{GA} + \vec{GB} + \vec{GC}') + ' ដើម្បីផ្ទៀងផ្ទាត់លក្ខណៈនៃទីប្រជុំទម្ងន់។',
        [
            ('សរសេររូបមន្តទីប្រជុំទម្ងន់: \\vec{g} = (\\vec{a} + \\vec{b} + \\vec{c})/3', 1),
            ('គណនាកូអរដោនេ G: x_G = (2 + 6 + 4)/3 = 4, y_G = (4 + 2 + 9)/3 = 5 នាំឱ្យ G(4, 5)', 1.5),
            ('គណនាកូអរដោនេ: \\vec{GA} = (-2, -1), \\vec{GB} = (2, -3), \\vec{GC} = (0, 4)', 1.5),
            ('បូកផ្ទៀងផ្ទាត់: (-2 + 2 + 0, -1 - 3 + 4) = (0, 0) = \\vec{0} ត្រឹមត្រូវ', 1)
        ]
    ))

    C.append(wr(
        'medium', 'sec3',
        'បន្ទាត់ L មួយកាត់តាមចំណុច ' + M(r'A(3,\, -2)') + ' ហើយកែងនឹងវ៉ិចទ័រណរម៉ាល់ ' + M(r'\vec{n} = (4,\, 5)') + '។\n'
        'ក. សរសេរសមីការវ៉ិចទ័រនៃបន្ទាត់ L តាមរូបមន្ត ' + M(r'\vec{n} \cdot (\vec{r} - \vec{a}) = 0') + '។\n'
        'ខ. បំប្លែងទៅជាសមីការទូទៅ ' + M(r'ax + by + c = 0') + '។',
        [
            ('សរសេរកន្សោមវ៉ិចទ័រ: \\vec{r} - \\vec{a} = (x - 3, y - (-2)) = (x - 3, y + 2)', 1.5),
            ('សរសេរផលគុណស្កាលែ: (4, 5) \\cdot (x - 3, y + 2) = 0', 1.5),
            ('ពន្លាតសមីការ: 4(x - 3) + 5(y + 2) = 0 <=> 4x - 12 + 5y + 10 = 0', 1),
            ('បង្រួមសមីការទូទៅ: 4x + 5y - 2 = 0', 1)
        ]
    ))

    C.append(wr(
        'medium', 'sec4',
        'កម្លាំងពីរ ' + M(r'\vec{F}_1') + ' និង ' + M(r'\vec{F}_2') + ' មានទំហំ ' + M(r'F_1 = 30\text{ N}') + ' និង ' + M(r'F_2 = 50\text{ N}') + ' មានចំណុចចាប់រួមគ្នា និងបង្កើតបានមុំ ' + M(r'\theta = 60^\circ') + '។\n'
        'ក. សរសេររូបមន្តគណនាម៉ូឌុលនៃកម្លាំងផ្គួប F។\n'
        'ខ. គណនាម៉ូឌុលកម្លាំងផ្គួប F (យក ' + M(r'\sqrt{4900} = 70') + ')។',
        [
            ('សរសេររូបមន្ត: F = \\sqrt{F_1^2 + F_2^2 + 2F_1 F_2 \\cos\\theta}', 1.5),
            ('ជំនួសតម្លៃ: F^2 = 30^2 + 50^2 + 2(30)(50)\\cos 60°', 1.5),
            ('គណនាតម្លៃលេខ: F^2 = 900 + 2500 + 3000(0.5) = 3400 + 1500 = 4900', 1),
            ('ទាញរកម៉ូឌុល: F = \\sqrt{4900} = 70 N', 1)
        ]
    ))

    C.append(wr(
        'medium', 'sec4',
        'កម្លាំងថេរ ' + M(r'\vec{F} = (15,\, 20)') + ' N ធ្វើឱ្យរទេះមួយផ្លាស់ទីបានវ៉ិចទ័របំលាស់ទី ' + M(r'\vec{d} = (6,\, 2)') + ' m។\n'
        'ក. គណនាកម្មន្ត W ដែលកម្លាំងបានបំពេញ។\n'
        'ខ. គណនាប្រវែងនៃកម្លាំង ' + M(r'|\vec{F}|') + ' និងប្រវែងបំលាស់ទី ' + M(r'|\vec{d}|') + '។',
        [
            ('សរសេររូបមន្តកម្មន្ត: W = \\vec{F} \\cdot \\vec{d} = F_x d_x + F_y d_y', 1.5),
            ('គណនាកម្មន្ត: W = (15)(6) + (20)(2) = 90 + 40 = 130 J', 1.5),
            ('គណនា |\\vec{F}| = \\sqrt{15^2 + 20^2} = \\sqrt{225 + 400} = \\sqrt{625} = 25 N', 1),
            ('គណនា |\\vec{d}| = \\sqrt{6^2 + 2^2} = \\sqrt{36 + 4} = \\sqrt{40} = 2\\sqrt{10} m', 1)
        ]
    ))

    # =========================================================================
    # WRITING - HARD (target: 4, provide: 5)
    # =========================================================================

    C.append(wr(
        'hard', 'sec1',
        'គេមានចំណុច ' + M(r'A(1,\, 2)') + ' និង ' + M(r'B(4,\, 5)') + '។ ចំណុច D ចែកអង្កត់ AB ខាងក្រៅតាមផលធៀប ' + M(r'2 : 1') + ' (គឺ ' + M(r'DA : DB = 2 : 1') + ')។\n'
        'ក. សរសេររូបមន្តវ៉ិចទ័រទីតាំង ' + M(r'\vec{d}') + ' នៃចំណុចចែកក្រៅ។\n'
        'ខ. គណនាកូអរដោនេនៃចំណុច D ព្រមទាំងផ្ទៀងផ្ទាត់ថា B ជាចំណុចកណ្តាលនៃ AD។',
        [
            ('សរសេររូបមន្តចំណុចចែកក្រៅ: \\vec{d} = \\dfrac{m\\vec{b} - n\\vec{a}}{m - n}', 1.5),
            ('ជំនួស m = 2, n = 1: \\vec{d} = \\dfrac{2\\vec{b} - \\vec{a}}{2 - 1} = 2\\vec{b} - \\vec{a}', 1.5),
            ('គណនាកូអរដោនេ D: x_D = 2(4) - 1 = 7, y_D = 2(5) - 2 = 8 នាំឱ្យ D(7, 8)', 1),
            ('ផ្ទៀងផ្ទាត់ចំណុចកណ្តាល AD: ((1 + 7)/2, (2 + 8)/2) = (4, 5) = B (ពិត)', 1)
        ]
    ))

    C.append(wr(
        'hard', 'sec3',
        'គេមានរង្វង់ C កំណត់ដោយសមីការវ៉ិចទ័រ ' + M(r'|\vec{r} - \vec{c}| = 5') + ' ដែល ' + M(r'\vec{c} = (2,\, 3)') + '។\n'
        'ក. បង្ហាញថាសមីការពិជគណិតនៃរង្វង់គឺ ' + M(r'(x - 2)^2 + (y - 3)^2 = 25') + '។\n'
        'ខ. ពិនិត្យថាតើចំណុច ' + M(r'P(5,\, 7)') + ' ស្ថិតនៅលើរង្វង់ C ដែរឬទេ? បើស្ថិតនៅ ចូរសរសេរសមីការបន្ទាត់ប៉ះរង្វង់ត្រង់ P។',
        [
            ('លើកជាការេ: |\\vec{r} - \\vec{c}|^2 = 25 <=> (x - 2)^2 + (y - 3)^2 = 25 (ពិត)', 1.5),
            ('ផ្ទៀងផ្ទាត់ចំណុច P(5, 7): (5 - 2)^2 + (7 - 3)^2 = 3^2 + 4^2 = 25 នាំឱ្យ P ស្ថិតនៅលើរង្វង់', 1),
            ('វ៉ិចទ័រណរម៉ាល់នៃបន្ទាត់ប៉ះ: \\vec{n} = \\vec{CP} = (5 - 2, 7 - 3) = (3, 4)', 1),
            ('សមីការបន្ទាត់ប៉ះ: 3(x - 5) + 4(y - 7) = 0 <=> 3x + 4y - 43 = 0', 1.5)
        ]
    ))

    C.append(wr(
        'hard', 'sec4',
        'អង្គធាតុមួយទម្ងន់ ' + M(r'P = 100\text{ N}') + ' ត្រូវបានព្យួរដោយខ្សែពីរ AC និង BC ភ្ជាប់ទៅពិដានផ្ដេកត្រង់ A និង B។ ខ្សែ AC បង្កើតមុំ ' + M(r'30^\circ') + ' និងខ្សែ BC បង្កើតមុំ ' + M(r'60^\circ') + ' ធៀបនឹងពិដានផ្ដេក (មុំត្រង់ C គឺ 90 ដឺក្រេ)។\n'
        'ក. សរសេរលក្ខខណ្ឌលំនឹងកម្លាំងត្រង់ចំណុច C តាមទិសដេក និងទិសឈរ។\n'
        'ខ. គណនាកម្លាំងតំណឹង ' + M(r'T_1') + ' ក្នុងខ្សែ AC និង ' + M(r'T_2') + ' ក្នុងខ្សែ BC។',
        [
            ('លំនឹងទិសដេក: T_1 \\cos 30° = T_2 \\cos 60° <=> T_1(\\sqrt{3}/2) = T_2(1/2) <=> T_2 = T_1\\sqrt{3}', 1.5),
            ('លំនឹងទិសឈរ: T_1 \\sin 30° + T_2 \\sin 60° = P = 100', 1.5),
            ('ជំនួស T_2: T_1(1/2) + (T_1\\sqrt{3})(\\sqrt{3}/2) = 100 <=> 2T_1 = 100 នាំឱ្យ T_1 = 50 N', 1),
            ('ទាញរក T_2: T_2 = 50\\sqrt{3} ≈ 86.6 N', 1)
        ]
    ))

    C.append(wr(
        'hard', 'sec2',
        'ក្នុងត្រីកោណ ABC គេយក O ជាគល់នៃប្លង់ និង ' + M(r'A(\vec{a}),\, B(\vec{b}),\, C(\vec{c})') + '។ ចំណុច A\' ជាចំណុចកណ្តាលនៃ BC។\n'
        'ក. សរសេរវ៉ិចទ័រទីតាំង ' + M(r'\vec{a}\'') + ' នៃ A\' ជាអនុគមន៍នៃ ' + M(r'\vec{b}') + ' និង ' + M(r'\vec{c}') + '។\n'
        'ខ. ចំណុច G ចែកមេដ្យាន AA\' ខាងក្នុងតាមផលធៀប ' + M(r'AG : GA\' = 2 : 1') + '។ រកវ៉ិចទ័រទីតាំង ' + M(r'\vec{g}') + ' និងទាញសន្និដ្ឋាន។',
        [
            ('សរសេរវ៉ិចទ័រទីតាំងចំណុចកណ្តាល A\': \\vec{a}\' = (\\vec{b} + \\vec{c})/2', 1.5),
            ('រូបមន្តចំណុចចែកក្នុងផលធៀប 2:1: \\vec{g} = \\dfrac{2\\vec{a}\' + 1\\vec{a}}{2 + 1}', 1.5),
            ('ជំនួស \\vec{a}\': \\vec{g} = \\dfrac{2((\\vec{b} + \\vec{c})/2) + \\vec{a}}{3} = \\dfrac{\\vec{a} + \\vec{b} + \\vec{c}}{3}', 1),
            ('សន្និដ្ឋាន: G គឺជាទីប្រជុំទម្ងន់នៃត្រីកោណ ABC ដែលចែកមេដ្យានតាមផលធៀប 2:1', 1)
        ]
    ))

    C.append(wr(
        'hard', 'sec3',
        'គេមានបន្ទាត់ពីរ ' + M(r'L_1: \vec{r} = (1,\, 2) + t(2,\, 3)') + ' និង ' + M(r'L_2: \vec{r} = (4,\, 1) + s(-3,\, 2)') + '។\n'
        'ក. រកវ៉ិចទ័រប្រាប់ទិស ' + M(r'\vec{u}_1') + ' និង ' + M(r'\vec{u}_2') + ' នៃបន្ទាត់ទាំងពីរ។\n'
        'ខ. គណនាផលគុណស្កាលែ ' + M(r'\vec{u}_1 \cdot \vec{u}_2') + ' និងទាញសន្និដ្ឋានអំពីទីតាំងធរណីមាត្ររវាងបន្ទាត់ ' + M(r'L_1') + ' និង ' + M(r'L_2') + '។',
        [
            ('កំណត់វ៉ិចទ័រប្រាប់ទិស: \\vec{u}_1 = (2, 3) និង \\vec{u}_2 = (-3, 2)', 1.5),
            ('គណនាផលគុណស្កាលែ: \\vec{u}_1 \\cdot \\vec{u}_2 = (2)(-3) + (3)(2) = -6 + 6 = 0', 1.5),
            ('ទាញរកទំនាក់ទំនងវ៉ិចទ័រ: \\vec{u}_1 \\perp \\vec{u}_2', 1),
            ('សន្និដ្ឋានធរណីមាត្រ: បន្ទាត់ L_1 កែងនឹងបន្ទាត់ L_2 (L_1 \\perp L_2)', 1)
        ]
    ))

    # =========================================================================
    # WRITING - PISA (target: 5, provide: 6)
    # =========================================================================

    C.append(wr(
        'pisa', 'pisa',
        'PISA នាវាចរណ៍ឆ្លងទន្លេ: ទូកចម្លងមួយបើកបរឆ្លងទន្លេទទឹង ' + M(r'200\text{ m}') + ' ដោយល្បឿន ' + M(r'v_b = 5\text{ m/s}') + ' តម្រង់កាត់កែងនឹងច្រាំងទន្លេ។ ចរន្តទឹកហូរតាមបណ្តោយច្រាំងដោយល្បឿន ' + M(r'v_r = 3.75\text{ m/s}') + '។\n'
        'ក. គណនារយៈពេលដែលទូកចំណាយដើម្បីទៅដល់ត្រើយម្ខាងទៀត។\n'
        'ខ. គណនាចម្ងាយដែលទូករសាត់តាមបណ្តោយចរន្តទឹកទន្លេ។\n'
        'គ. គណនាល្បឿនផ្គួបពិតប្រាកដនៃទូកធៀបនឹងច្រាំង និងចម្ងាយសរុបដែលទូកបានធ្វើដំណើរកាត់ទឹក។',
        [
            ('គណនារយៈពេលឆ្លងទន្លេ: t = 200 / 5 = 40 វិនាទី', 1.5),
            ('គណនាចម្ងាយរសាត់: d_drift = v_r * t = 3.75 * 40 = 150 m', 1.5),
            ('គណនាល្បឿនផ្គួប: v = \\sqrt{5^2 + 3.75^2} = \\sqrt{25 + 14.0625} = \\sqrt{39.0625} = 6.25 m/s', 1),
            ('គណនាចម្ងាយសរុប: d_total = v * t = 6.25 * 40 = 250 m (ឬ \\sqrt{200^2 + 150^2} = 250 m)', 1)
        ]
    ))

    C.append(wr(
        'pisa', 'pisa',
        'PISA ការអូសរទេះទំនិញលើជម្រាល: កម្មករម្នាក់ទាញរទេះផ្ទុកទំនិញឡើងលើផ្លូវជម្រាលភ្នំដែលមានមុំទេរ ' + M(r'30^\circ') + '។ ទម្ងន់សរុបនៃរទេះគឺ ' + M(r'P = 1200\text{ N}') + '។\n'
        'ក. គណនាសមាសភាគកម្លាំងទម្ងន់ទាញចុះស្របតាមជម្រាល ' + M(r'P_{\parallel} = P \sin 30^\circ') + '។\n'
        'ខ. គណនាសមាសភាគកម្លាំងទម្ងន់សង្កត់កែងលើផ្ទៃជម្រាល ' + M(r'P_{\perp} = P \cos 30^\circ') + ' (យក ' + M(r'\cos 30^\circ \approx 0.866') + ')។\n'
        'គ. បើមិនគិតកម្លាំងកកិត តើកម្មករត្រូវបញ្ចេញកម្លាំងទាញ ' + M(r'F') + ' ស្របនឹងជម្រាលយ៉ាងហោចណាស់ប៉ុន្មានដើម្បីអូសរទេះឡើងលើដោយល្បឿនថេរ?',
        [
            ('គណនា P_parallel = 1200 * \\sin 30° = 1200 * 0.5 = 600 N', 1.5),
            ('គណនា P_perp = 1200 * \\cos 30° = 1200 * 0.866 = 1039.2 N', 1.5),
            ('ពន្យល់លក្ខខណ្ឌល្បឿនថេរ: ផលបូកកម្លាំងតាមទិសជម្រាលស្មើ 0: F - P_parallel = 0', 1),
            ('ទាញរកកម្លាំងទាញ: F = P_parallel = 600 N', 1)
        ]
    ))

    C.append(wr(
        'pisa', 'pisa',
        'PISA សន្សំសំចៃថាមពល និងកម្មន្ត: ក្នុងការដឹកជញ្ជូនសម្ភារសំណង់ កម្មករម្នាក់ត្រូវរុញរទេះដោយកម្លាំង ' + M(r'F = 150\text{ N}') + ' បានចម្ងាយ ' + M(r'd = 40\text{ m}') + '។\n'
        'ក. គណនាកម្មន្ត W ប្រសិនបើគាត់រុញរទេះស្របតាមទិសដេក (' + M(r'\theta = 0^\circ') + ')។\n'
        'ខ. គណនាកម្មន្ត W ប្រសិនបើគាត់ទាញខ្សែពួរដែលបង្កើតបានមុំ ' + M(r'\theta = 45^\circ') + ' ធៀបនឹងដីផ្ដេក (យក ' + M(r'\cos 45^\circ \approx 0.707') + ')។\n'
        'គ. តើវិធីណាដែលផ្តល់កម្មន្តទៅលើការរំកិលរទេះបានច្រើនជាង និងច្រើនជាងប៉ុន្មានហ្ស៊ូល?',
        [
            ('គណនា W_1 (មុំ 0°): W_1 = 150 * 40 * 1 = 6000 J = 6 kJ', 1.5),
            ('គណនា W_2 (មុំ 45°): W_2 = 150 * 40 * 0.707 = 4242 J ≈ 4.24 kJ', 1.5),
            ('ប្រៀបធៀប: វិធីទី 1 (មុំ 0°) ផ្តល់កម្មន្តច្រើនជាងវិធីទី 2', 1),
            ('គណនាផលសង: 6000 - 4242 = 1758 J (ច្រើនជាង 1758 J)', 1)
        ]
    ))

    C.append(wr(
        'pisa', 'pisa',
        'PISA ប្រព័ន្ធរ៉ូបូតឃ្លាំងទំនិញ: រ៉ូបូតស្វ័យប្រវត្តមួយក្នុងឃ្លាំងទំនិញផ្លាស់ទីតាមប្លង់កូអរដោនេដេក។ វាចាប់ផ្តើមពីទីតាំង ' + M(r'A(2,\, 3)') + ' ទៅយកទំនិញត្រង់ ' + M(r'B(8,\, 11)') + ' រួចដឹកបន្តទៅដាក់នៅបញ្ជរ ' + M(r'C(14,\, 3)') + ' (គិតជាម៉ែត្រ)។\n'
        'ក. គណនាវ៉ិចទ័របំលាស់ទី ' + M(r'\vec{AB}') + ' និង ' + M(r'\vec{BC}') + '។\n'
        'ខ. គណនាចម្ងាយផ្លូវសរុប ' + M(r'AB + BC') + ' ដែលរ៉ូបូតបានធ្វើដំណើរ។\n'
        'គ. គណនាប្រវែងនៃវ៉ិចទ័របំលាស់ទីសរុប ' + M(r'|\vec{AC}|') + ' ពីចំណុចចាប់ផ្តើម A ដល់ចំណុចបញ្ចប់ C។',
        [
            ('គណនា \\vec{AB} = (8 - 2, 11 - 3) = (6, 8) និង \\vec{BC} = (14 - 8, 3 - 11) = (6, -8)', 1.5),
            ('គណនាប្រវែង: AB = \\sqrt{6^2 + 8^2} = 10 m និង BC = \\sqrt{6^2 + (-8)^2} = 10 m នាំឱ្យចម្ងាយសរុប = 20 m', 1.5),
            ('គណនា \\vec{AC} = \\vec{AB} + \\vec{BC} = (6 + 6, 8 - 8) = (12, 0)', 1),
            ('គណនាប្រវែងបំលាស់ទីសរុប: |\\vec{AC}| = 12 m', 1)
        ]
    ))

    C.append(wr(
        'pisa', 'pisa',
        'PISA លំនឹងស្ទូចសំណង់: ស្ទូចសំណង់មួយកំពុងទប់ទម្ងន់ធ្នឹមដែក ' + M(r'P = 8000\text{ N}') + ' ឱ្យនៅនឹងថ្កល់ក្នុងអាកាស។ កម្លាំងទាញរបស់ខ្សែស្ទូចពីរគឺ ' + M(r'\vec{T}_1') + ' និង ' + M(r'\vec{T}_2') + ' បង្កើតបានមុំ ' + M(r'45^\circ') + ' សងខាងធៀបនឹងបន្ទាត់ឈរ (មុំរវាងខ្សែទាំងពីរគឺ ' + M(r'90^\circ') + ')។\n'
        'ក. សរសេរលក្ខខណ្ឌលំនឹងកម្លាំងនៃធ្នឹមដែក។\n'
        'ខ. គណនាកម្លាំងតំណឹង ' + M(r'T_1 = T_2 = T') + ' ក្នុងខ្សែស្ទូចនីមួយៗ (យក ' + M(r'\cos 45^\circ = \dfrac{\sqrt{2}}{2}') + ')។\n'
        'គ. បើខ្សែនីមួយៗទ្រាំទ្រកម្លាំងអតិបរមា 5000 N តើការលើកនេះមានសុវត្ថិភាពឬទេ?',
        [
            ('លក្ខខណ្ឌលំនឹង: \\vec{T}_1 + \\vec{T}_2 + \\vec{P} = \\vec{0} នាំឱ្យផលបូកទិសឈរ 2T \\cos 45° = P = 8000', 1.5),
            ('ដោះស្រាយសមីការ: 2T(\\sqrt{2}/2) = 8000 <=> T\\sqrt{2} = 8000 នាំឱ្យ T = 4000\\sqrt{2} ≈ 5656.85 N', 1.5),
            ('ប្រៀបធៀបកម្លាំងទ្រាំទ្រ: T ≈ 5656.85 N > 5000 N', 1),
            ('សន្និដ្ឋានសុវត្ថិភាព: មិនមានសុវត្ថិភាពឡើយ ព្រោះកម្លាំងតំណឹងជាក់ស្តែងលើសពីកម្រិតកំណត់អតិបរមា (ខ្សែអាចនឹងដាច់)', 1)
        ]
    ))

    C.append(wr(
        'pisa', 'pisa',
        'PISA ការហោះហើរដ្រូន (Drone Navigation): ដ្រូនមួយហោះហើរក្នុងប្លង់កូអរដោនេផ្ដេកពីទីតាំង ' + M(r'P_0(0,\, 0)') + '។ ដំណាក់កាលទី 1 វាហោះតាមវ៉ិចទ័រ ' + M(r'\vec{d}_1 = (30,\, 40)') + ' ម៉ែត្រ។ ដំណាក់កាលទី 2 វាហោះតាមវ៉ិចទ័រ ' + M(r'\vec{d}_2 = (50,\, -10)') + ' ម៉ែត្រ។ ដំណាក់កាលទី 3 វាហោះតាម ' + M(r'\vec{d}_3 = (-20,\, 30)') + ' ម៉ែត្រ។\n'
        'ក. គណនាវ៉ិចទ័របំលាស់ទីសរុប ' + M(r'\vec{d} = \vec{d}_1 + \vec{d}_2 + \vec{d}_3') + '។\n'
        'ខ. រកកូអរដោនេនៃទីតាំងចុងក្រោយរបស់ដ្រូន។\n'
        'គ. គណនាចម្ងាយត្រង់ពីចំណុចចេញដំណើរដើម ' + M(r'P_0') + ' ទៅកាន់ទីតាំងចុងក្រោយ។',
        [
            ('បូកសមាសភាគ x: 30 + 50 + (-20) = 60 m', 1.5),
            ('បូកសមាសភាគ y: 40 + (-10) + 30 = 60 m នាំឱ្យ \\vec{d} = (60, 60) m', 1.5),
            ('ទីតាំងចុងក្រោយ: P(60, 60)', 1),
            ('គណនាចម្ងាយត្រង់: |\\vec{d}| = \\sqrt{60^2 + 60^2} = 60\\sqrt{2} ≈ 84.85 m', 1)
        ]
    ))

    return C
