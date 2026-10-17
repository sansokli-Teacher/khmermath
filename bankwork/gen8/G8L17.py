"""Bank candidates for Grade 8, Lesson 17: បន្ទាត់និងអង្កត់ពិសេសជួបគ្នានៅក្នុងត្រីកោណ (Concurrent Lines in Triangles)
Covers MoEYS Grade 8 curriculum:
  1. មេដ្យាន និងទីប្រជុំទម្ងន់ G (Medians, Centroid G: AG = 2/3 AA', GA' = 1/3 AA', AG = 2 GA')
  2. មេដ្យាទ័រ និងផ្ចិតរង្វង់ចារឹកក្រៅ O (Perpendicular bisectors, Circumcenter O: OA = OB = OC = R)
  3. កម្ពស់ និងអរតូសង់ H (Altitudes, Orthocenter H)
  4. កន្លះបន្ទាត់ពុះមុំ និងផ្ចិតរង្វង់ចារឹកក្នុង I (Angle bisectors, Incenter I: equidistant from sides, S = p * r)
  5. ត្រីកោណពិសេស (Equilateral triangle: G, O, H, I coincide; Isosceles triangle: 4 points on axis)
  6. ការអនុវត្តជាក់ស្តែង & PISA (Triangular park lighting, mobile tower coverage, gravity balancing point, emergency hub)

Images: Clean vector illustrations, isolated, no background, flat educational textbook style.
Geometry labels use font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic'.
"""
from lib import *

LESSON = "បន្ទាត់និងអង្កត់ពិសេសជួបគ្នានៅក្នុងត្រីកោណ"

# --- SVG Illustrations ---

# 1. FIG_MEDIANS_CENTROID: Triangle ABC with medians AA', BB', CC' concurrent at G
FIG_MEDIANS_CENTROID = (
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 280 200' width='280' height='200'>\n"
    "  <!-- Triangle ABC: A(140, 25), B(35, 175), C(245, 175) -->\n"
    "  <polygon points='140,25 35,175 245,175' fill='#f8fafc' stroke='#334155' stroke-width='2'/>\n"
    "  <!-- Midpoints: A'(140, 175), B'(192.5, 100), C'(87.5, 100) -->\n"
    "  <!-- Medians AA', BB', CC' meeting at G(140, 125) -->\n"
    "  <line x1='140' y1='25' x2='140' y2='175' stroke='#0284c7' stroke-width='1.5' stroke-dasharray='4,3'/>\n"
    "  <line x1='35' y1='175' x2='192.5' y2='100' stroke='#0284c7' stroke-width='1.5' stroke-dasharray='4,3'/>\n"
    "  <line x1='245' y1='175' x2='87.5' y2='100' stroke='#0284c7' stroke-width='1.5' stroke-dasharray='4,3'/>\n"
    "  <!-- Centroid G -->\n"
    "  <circle cx='140' cy='125' r='3.5' fill='#dc2626'/>\n"
    "  <!-- Midpoint tick marks -->\n"
    "  <line x1='85' y1='171' x2='85' y2='179' stroke='#16a34a' stroke-width='1.5'/>\n"
    "  <line x1='195' y1='171' x2='195' y2='179' stroke='#16a34a' stroke-width='1.5'/>\n"
    "  <!-- Labels (Mathcad italic) -->\n"
    "  <text x='140' y='18' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>A</text>\n"
    "  <text x='25' y='185' text-anchor='end' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>B</text>\n"
    "  <text x='255' y='185' text-anchor='start' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>C</text>\n"
    "  <text x='140' y='190' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='12' fill='#0284c7'>A'</text>\n"
    "  <text x='202' y='100' text-anchor='start' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='12' fill='#0284c7'>B'</text>\n"
    "  <text x='78' y='100' text-anchor='end' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='12' fill='#0284c7'>C'</text>\n"
    "  <text x='152' y='125' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='13' fill='#dc2626'>G</text>\n"
    "</svg>"
)

# 2. FIG_PERP_BISECTORS_CIRCUMCENTER: Triangle ABC with perpendicular bisectors and circumcircle
FIG_PERP_BISECTORS_CIRCUMCENTER = (
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 280 210' width='280' height='210'>\n"
    "  <!-- Circumcircle centered at O(140, 110) with R = 85 -->\n"
    "  <circle cx='140' cy='110' r='85' fill='none' stroke='#94a3b8' stroke-width='1.5' stroke-dasharray='4,3'/>\n"
    "  <!-- Triangle ABC: A(140, 25), B(60, 150), C(220, 150) -->\n"
    "  <polygon points='140,25 60,150 220,150' fill='#eff6ff' stroke='#0284c7' stroke-width='2'/>\n"
    "  <!-- Perpendicular bisectors meeting at O(140, 110) -->\n"
    "  <line x1='140' y1='40' x2='140' y2='170' stroke='#16a34a' stroke-width='1.5'/>\n"
    "  <line x1='60' y1='60' x2='180' y2='140' stroke='#16a34a' stroke-width='1.5'/>\n"
    "  <line x1='220' y1='60' x2='100' y2='140' stroke='#16a34a' stroke-width='1.5'/>\n"
    "  <!-- Circumcenter O -->\n"
    "  <circle cx='140' cy='110' r='3.5' fill='#dc2626'/>\n"
    "  <!-- Labels (Mathcad italic) -->\n"
    "  <text x='140' y='18' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>A</text>\n"
    "  <text x='50' y='160' text-anchor='end' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>B</text>\n"
    "  <text x='230' y='160' text-anchor='start' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>C</text>\n"
    "  <text x='152' y='110' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='13' fill='#dc2626'>O</text>\n"
    "</svg>"
)

# 3. FIG_ALTITUDES_ORTHOCENTER: Triangle ABC with altitudes AD, BE, CF concurrent at H
FIG_ALTITUDES_ORTHOCENTER = (
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 280 200' width='280' height='200'>\n"
    "  <!-- Triangle ABC: A(120, 25), B(35, 175), C(245, 175) -->\n"
    "  <polygon points='120,25 35,175 245,175' fill='#f8fafc' stroke='#334155' stroke-width='2'/>\n"
    "  <!-- Altitudes AD, BE, CF meeting at H(120, 130) -->\n"
    "  <line x1='120' y1='25' x2='120' y2='175' stroke='#dc2626' stroke-width='1.5'/>\n"
    "  <line x1='35' y1='175' x2='175' y2='91' stroke='#dc2626' stroke-width='1.5'/>\n"
    "  <line x1='245' y1='175' x2='83' y2='90' stroke='#dc2626' stroke-width='1.5'/>\n"
    "  <!-- Orthocenter H -->\n"
    "  <circle cx='120' cy='130' r='3.5' fill='#dc2626'/>\n"
    "  <!-- Right angle marker at D(120, 175) -->\n"
    "  <path d='M 120,165 L 130,165 L 130,175' fill='none' stroke='#dc2626' stroke-width='1.2'/>\n"
    "  <!-- Labels (Mathcad italic) -->\n"
    "  <text x='120' y='18' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>A</text>\n"
    "  <text x='25' y='185' text-anchor='end' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>B</text>\n"
    "  <text x='255' y='185' text-anchor='start' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>C</text>\n"
    "  <text x='120' y='190' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='12' fill='#dc2626'>D</text>\n"
    "  <text x='132' y='132' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='13' fill='#dc2626'>H</text>\n"
    "</svg>"
)

# 4. FIG_ANGLE_BISECTORS_INCENTER: Triangle ABC with angle bisectors and incircle
FIG_ANGLE_BISECTORS_INCENTER = (
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 280 200' width='280' height='200'>\n"
    "  <!-- Triangle ABC: A(140, 25), B(35, 175), C(245, 175) -->\n"
    "  <polygon points='140,25 35,175 245,175' fill='#fdf4ff' stroke='#334155' stroke-width='2'/>\n"
    "  <!-- Incircle centered at I(140, 130) with r = 45 -->\n"
    "  <circle cx='140' cy='130' r='45' fill='#fdf2f8' stroke='#ec4899' stroke-width='1.8'/>\n"
    "  <!-- Angle bisectors meeting at I(140, 130) -->\n"
    "  <line x1='140' y1='25' x2='140' y2='175' stroke='#a855f7' stroke-width='1.5' stroke-dasharray='4,3'/>\n"
    "  <line x1='35' y1='175' x2='187' y2='92' stroke='#a855f7' stroke-width='1.5' stroke-dasharray='4,3'/>\n"
    "  <line x1='245' y1='175' x2='93' y2='92' stroke='#a855f7' stroke-width='1.5' stroke-dasharray='4,3'/>\n"
    "  <!-- Incenter I -->\n"
    "  <circle cx='140' cy='130' r='3.5' fill='#dc2626'/>\n"
    "  <!-- Inradius segment (I to base) -->\n"
    "  <line x1='140' y1='130' x2='140' y2='175' stroke='#ec4899' stroke-width='1.5'/>\n"
    "  <text x='146' y='155' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='12' fill='#ec4899'>r</text>\n"
    "  <!-- Labels (Mathcad italic) -->\n"
    "  <text x='140' y='18' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>A</text>\n"
    "  <text x='25' y='185' text-anchor='end' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>B</text>\n"
    "  <text x='255' y='185' text-anchor='start' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>C</text>\n"
    "  <text x='152' y='128' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='13' fill='#dc2626'>I</text>\n"
    "</svg>"
)


def cands():
    C = []

    def M_add(level, sec, stem, correct, wrongs, sol='', img=None):
        d = mcq(level, sec, stem, correct, wrongs, sol)
        if img: d['img'] = img
        C.append(d)

    def W(level, sec, stem, steps, img=None):
        d = wr(level, sec, stem, steps)
        if img: d['img'] = img
        C.append(d)

    # ==========================================
    # 1. MCQ EASY (10 target)
    # ==========================================
    M_add('easy', 'centroid_def',
          'ចំណុចប្រសព្វនៃមេដ្យានទាំងបីរបស់ត្រីកោណ ហៅថាអ្វី?',
          'ទីប្រជុំទម្ងន់ (Centroid)',
          ['អរតូសង់', 'ផ្ចិតរង្វង់ចារឹកក្រៅ', 'ផ្ចិតរង្វង់ចារឹកក្នុង'],
          'មេដ្យានទាំងបីនៃត្រីកោណប្រសព្វគ្នាត្រង់ចំណុចតែមួយហៅថា ទីប្រជុំទម្ងន់ កំណត់ដោយ ' + M('G'),
          FIG_MEDIANS_CENTROID)

    M_add('easy', 'circumcenter_def',
          'ចំណុចប្រសព្វនៃមេដ្យាទ័រទាំងបីនៃជ្រុងរបស់ត្រីកោណ ហៅថាអ្វី?',
          'ផ្ចិតរង្វង់ចារឹកក្រៅត្រីកោណ (Circumcenter)',
          ['ទីប្រជុំទម្ងន់', 'អរតូសង់', 'ផ្ចិតរង្វង់ចារឹកក្នុង'],
          'មេដ្យាទ័រទាំងបីនៃជ្រុងត្រីកោណប្រសព្វគ្នាត្រង់ផ្ចិតនៃរង្វង់ចារឹកក្រៅត្រីកោណ កំណត់ដោយ ' + M('O'),
          FIG_PERP_BISECTORS_CIRCUMCENTER)

    M_add('easy', 'orthocenter_def',
          'ចំណុចប្រសព្វនៃកម្ពស់ទាំងបីរបស់ត្រីកោណ ហៅថាអ្វី?',
          'អរតូសង់ (Orthocenter)',
          ['ទីប្រជុំទម្ងន់', 'ផ្ចិតរង្វង់ចារឹកក្រៅ', 'ផ្ចិតរង្វង់ចារឹកក្នុង'],
          'កម្ពស់ទាំងបីនៃត្រីកោណប្រសព្វគ្នាត្រង់ចំណុចតែមួយហៅថា អរតូសង់ កំណត់ដោយ ' + M('H'),
          FIG_ALTITUDES_ORTHOCENTER)

    M_add('easy', 'incenter_def',
          'ចំណុចប្រសព្វនៃកន្លះបន្ទាត់ពុះមុំក្នុងទាំងបីរបស់ត្រីកោណ ហៅថាអ្វី?',
          'ផ្ចិតរង្វង់ចារឹកក្នុងត្រីកោណ (Incenter)',
          ['អរតូសង់', 'ទីប្រជុំទម្ងន់', 'ផ្ចិតរង្វង់ចារឹកក្រៅ'],
          'កន្លះបន្ទាត់ពុះមុំទាំងបីនៃត្រីកោណប្រសព្វគ្នាត្រង់ផ្ចិតរង្វង់ចារឹកក្នុងត្រីកោណ កំណត់ដោយ ' + M('I'),
          FIG_ANGLE_BISECTORS_INCENTER)

    M_add('easy', 'centroid_ratio_vertex',
          'បើ ' + M('G') + ' ជាទីប្រជុំទម្ងន់នៃត្រីកោណ ' + M('ABC') + ' ហើយ ' + M("AA'") + ' ជាមេដ្យានគូសចេញពីកំពូល ' + M('A') + ' តើផលធៀប ' + M("\\dfrac{AG}{AA'}") + ' ស្មើនឹងប៉ុន្មាន?',
          M('\\dfrac{2}{3}'),
          [M('\\dfrac{1}{3}'), M('\\dfrac{1}{2}'), M('\\dfrac{3}{4}')],
          'ទីប្រជុំទម្ងន់ស្ថិតនៅចម្ងាយ ' + M('\\dfrac{2}{3}') + ' នៃមេដ្យានពីកំពូល ៖ ' + M("AG = \dfrac{2}{3}AA'"))

    M_add('easy', 'centroid_ratio_base',
          'បើ ' + M('G') + ' ជាទីប្រជុំទម្ងន់នៃត្រីកោណ ' + M('ABC') + ' និង ' + M("AA'") + ' ជាមេដ្យាន គូសទៅបាត ' + M('BC') + ' តើ ' + M("\dfrac{GA'}{AA'}") + ' ស្មើនឹងប៉ុន្មាន?',
          M('\\dfrac{1}{3}'),
          [M('\\dfrac{2}{3}'), M('\\dfrac{1}{2}'), M('\\dfrac{1}{4}')],
          M("GA' = \\dfrac{1}{3}AA'"))

    M_add('easy', 'circumcenter_equidistant',
          'តើចំណុចប្រសព្វនៃមេដ្យាទ័រទាំងបី (ផ្ចិតរង្វង់ចារឹកក្រៅ ' + M('O') + ') មានចម្ងាយស្មើគ្នាទៅនឹងអ្វី?',
          'កំពូលទាំងបីនៃត្រីកោណ',
          ['ជ្រុងទាំងបីនៃត្រីកោណ', 'ជើងមេដ្យានទាំងបី', 'ជើងកម្ពស់ទាំងបី'],
          'ផ្ចិតរង្វង់ចារឹកក្រៅ ' + M('O') + ' មានចម្ងាយស្មើគ្នាទៅកំពូលទាំងបី ៖ ' + M('OA = OB = OC = R'))

    M_add('easy', 'incenter_equidistant',
          'តើចំណុចប្រសព្វនៃកន្លះបន្ទាត់ពុះមុំទាំងបី (ផ្ចិតរង្វង់ចារឹកក្នុង ' + M('I') + ') មានចម្ងាយស្មើគ្នាទៅនឹងអ្វី?',
          'ជ្រុងទាំងបីនៃត្រីកោណ',
          ['កំពូលទាំងបីនៃត្រីកោណ', 'មេដ្យានទាំងបី', 'កម្ពស់ទាំងបី'],
          'ផ្ចិតរង្វង់ចារឹកក្នុង ' + M('I') + ' មានចម្ងាយស្មើគ្នាទៅជ្រុងទាំងបីនៃត្រីកោណ ៖ ' + M('d(I, AB) = d(I, BC) = d(I, AC) = r'))

    M_add('easy', 'equilateral_coincide',
          'ក្នុងត្រីកោណសម័ង្ស តើចំណុចពិសេសទាំងបួន (ទីប្រជុំទម្ងន់ ' + M('G') + ', ផ្ចិតចារឹកក្រៅ ' + M('O') + ', អរតូសង់ ' + M('H') + ', ផ្ចិតចារឹកក្នុង ' + M('I') + ') មានទំនាក់ទំនងគ្នាយ៉ាងដូចម្តេច?',
          'ត្រួតស៊ីគ្នាជាចំណុចតែមួយ',
          ['នៅដាច់ដោយឡែកពីគ្នា', 'រត់ត្រង់ជួរគ្នាតែមិនត្រួតគ្នា', 'បង្កើតបានជាត្រីកោណសម័ង្សតូចមួយ'],
          'ក្នុងត្រីកោណសម័ង្ស បន្ទាត់ពិសេសទាំងបួនត្រួតស៊ីគ្នា នាំឱ្យចំណុច ' + M('G, O, H, I') + ' ត្រួតស៊ីគ្នាជាចំណុចតែមួយ')

    M_add('easy', 'right_tri_orthocenter',
          'ក្នុងត្រីកោណកែងមួយ តើអរតូសង់ ' + M('H') + ' ស្ថិតនៅត្រង់ទីតាំងណា?',
          'ត្រង់កំពូលនៃមុំកែង',
          ['នៅចំកណ្តាលអ៊ីប៉ូតេនុស', 'នៅខាងក្រៅត្រីកោណ', 'នៅចំផ្ចិតរង្វង់ចារឹកក្នុង'],
          'ក្នុងត្រីកោណកែង ជ្រុងមុំកែងទាំងពីរដើរតួជាកម្ពស់ ដូច្នេះកម្ពស់ទាំងបីកាត់គ្នាត្រង់កំពូលមុំកែង')

    # ==========================================
    # 2. MCQ MEDIUM (14 target)
    # ==========================================
    M_add('medium', 'calc_ag_from_median',
          'ក្នុងត្រីកោណ ' + M('ABC') + ' មេដ្យាន ' + M("AA' = 12\\ \\text{cm}") + '។ បើ ' + M('G') + ' ជាទីប្រជុំទម្ងន់ គណនាប្រវែង ' + M('AG') + '។',
          M('8\ \text{cm}'),
          [M('4\ \text{cm}'), M('6\ \text{cm}'), M('9\ \text{cm}')],
          M("AG = \\dfrac{2}{3}AA' = \dfrac{2}{3} \times 12 = 8\ \text{cm}"))

    M_add('medium', 'calc_ga_prime_from_median',
          'ក្នុងត្រីកោណ ' + M('ABC') + ' មេដ្យាន ' + M("BB' = 15\\ \\text{cm}") + '។ បើ ' + M('G') + ' ជាទីប្រជុំទម្ងន់ គណនា ' + M("GB'") + '។',
          M('5\\ \\text{cm}'),
          [M('10\\ \\text{cm}'), M('7.5\\ \\text{cm}'), M('3\\ \\text{cm}')],
          M("GB' = \\dfrac{1}{3}BB' = \dfrac{1}{3} \times 15 = 5\ \text{cm}"))

    M_add('medium', 'calc_median_from_ga',
          'ក្នុងត្រីកោណមួយ ចម្ងាយពីទីប្រជុំទម្ងន់ ' + M('G') + ' ទៅជើងមេដ្យាន ' + M("A'") + ' គឺ ' + M("GA' = 4\ \text{cm}") + '។ គណនាប្រវែងមេដ្យាន ' + M("AA'") + ' សរុប។',
          M('12\ \text{cm}'),
          [M('8\ \text{cm}'), M('6\ \text{cm}'), M('16\ \text{cm}')],
          M("AA' = 3 \times GA' = 3 \\times 4 = 12\\ \\text{cm}"))

    M_add('medium', 'calc_ag_from_ga_prime',
          'ក្នុងត្រីកោណមួយ គេដឹងថា ' + M("GA' = 3.5\ \text{cm}") + ' (' + M('G') + ' ជាទីប្រជុំទម្ងន់)។ គណនាប្រវែង ' + M('AG') + '។',
          M('7\\ \\text{cm}'),
          [M('3.5\\ \\text{cm}'), M('10.5\\ \\text{cm}'), M('5.25\\ \\text{cm}')],
          M("AG = 2 \times GA' = 2 \\times 3.5 = 7\\ \\text{cm}"))

    M_add('medium', 'right_tri_circumradius',
          'ត្រីកោណកែងមួយមានអ៊ីប៉ូតេនុសប្រវែង ' + M('16\ \text{cm}') + '។ គណនាកាំនៃរង្វង់ចារឹកក្រៅ ' + M('R') + ' នៃត្រីកោណនោះ។',
          M('8\ \text{cm}'),
          [M('16\ \text{cm}'), M('4\ \text{cm}'), M('5.33\ \text{cm}')],
          'ផ្ចិតរង្វង់ចារឹកក្រៅត្រីកោណកែងជាចំណុចកណ្តាលនៃអ៊ីប៉ូតេនុស ៖ ' + M('R = \dfrac{c}{2} = \dfrac{16}{2} = 8\ \text{cm}'))

    M_add('medium', 'right_tri_median_hypotenuse',
          'ក្នុងត្រីកោណ ' + M('ABC') + ' កែងត្រង់ ' + M('A') + ' មាន ' + M('BC = 20\ \text{cm}') + '។ មេដ្យាន ' + M('AM') + ' គូសទៅអ៊ីប៉ូតេនុស ' + M('BC') + ' មានប្រវែងស្មើនឹងប៉ុន្មាន?',
          M('10\ \text{cm}'),
          [M('20\ \text{cm}'), M('5\ \text{cm}'), M('15\ \text{cm}')],
          'មេដ្យានទៅអ៊ីប៉ូតេនុសនៃត្រីកោណកែងស្មើកន្លះអ៊ីប៉ូតេនុស ៖ ' + M('AM = \dfrac{BC}{2} = 10\ \text{cm}'))

    M_add('medium', 'two_equal_medians',
          'បើត្រីកោណ ' + M('ABC') + ' មានមេដ្យានពីរ ' + M("BB' = CC'") + ' ស្មើគ្នា តើត្រីកោណ ' + M('ABC') + ' ជាប្រភេទត្រីកោណអ្វី?',
          'ត្រីកោណសមបាតកំពូល A',
          ['ត្រីកោណសម័ង្ស', 'ត្រីកោណកែង', 'ត្រីកោណមិនសមបាត'],
          'ត្រីកោណដែលមានមេដ្យានពីរស្មើគ្នា គឺជាត្រីកោណសមបាត')

    M_add('medium', 'obtuse_tri_orthocenter',
          'ក្នុងត្រីកោណទាលមួយ (មានមុំមួយធំជាង ' + M('90^\circ') + ') តើអរតូសង់ ' + M('H') + ' ស្ថិតនៅទីណា?',
          'នៅខាងក្រៅត្រីកោណ',
          ['នៅខាងក្នុងត្រីកោណ', 'នៅលើជ្រុងវែងជាងគេ', 'ត្រង់កំពូលនៃមុំទាល'],
          'ក្នុងត្រីកោណទាល កម្ពស់ទាំងបីប្រសព្វគ្នានៅខាងក្រៅត្រីកោណ')

    M_add('medium', 'obtuse_tri_circumcenter',
          'ក្នុងត្រីកោណទាលមួយ តើផ្ចិតរង្វង់ចារឹកក្រៅ ' + M('O') + ' ស្ថិតនៅទីណា?',
          'នៅខាងក្រៅត្រីកោណ',
          ['នៅខាងក្នុងត្រីកោណ', 'នៅលើជ្រុងឈមមុំទាល', 'ត្រង់កំពូលមុំទាល'],
          'ក្នុងត្រីកោណទាល ផ្ចិតរង្វង់ចារឹកក្រៅ ' + M('O') + ' ស្ថិតនៅខាងក្រៅត្រីកោណ')

    M_add('medium', 'incenter_location_always',
          'សម្រាប់ត្រីកោណគ្រប់ប្រភេទ (ស្រួច កែង ឬទាល) តើផ្ចិតរង្វង់ចារឹកក្នុង ' + M('I') + ' ស្ថិតនៅទីណាជានិច្ច?',
          'នៅខាងក្នុងត្រីកោណជានិច្ច',
          ['នៅខាងក្រៅត្រីកោណពេលមុំទាល', 'នៅលើជ្រុងពេលត្រីកោណកែង', 'អាចនៅក្រៅឬក្នុង'],
          'ផ្ចិតរង្វង់ចារឹកក្នុង ' + M('I') + ' ជាប្រសព្វបន្ទាត់ពុះមុំក្នុង ដូច្នេះវាស្ថិតនៅខាងក្នុងត្រីកោណជានិច្ច')

    M_add('medium', 'tri_area_inradius',
          'ត្រីកោណមួយមានបរិមាត្រ ' + M('P = 36\ \text{cm}') + ' និងកាំរង្វង់ចារឹកក្នុង ' + M('r = 3\ \text{cm}') + '។ គណនាផ្ទៃក្រឡានៃត្រីកោណនោះ។',
          M('54\ \text{cm}^2'),
          [M('108\ \text{cm}^2'), M('27\ \text{cm}^2'), M('36\ \text{cm}^2')],
          'កន្លះបរិមាត្រ ៖ ' + M('p = \dfrac{36}{2} = 18\ \text{cm} \Rightarrow S = p \times r = 18 \times 3 = 54\ \text{cm}^2'))

    M_add('medium', 'centroid_splits_three_areas',
          'ត្រីកោណ ' + M('ABC') + ' មានផ្ទៃក្រឡា ' + M('48\ \text{cm}^2') + '។ ' + M('G') + ' ជាទីប្រជុំទម្ងន់នៃត្រីកោណ។ គណនាផ្ទៃក្រឡានៃត្រីកោណ ' + M('GBC') + '។',
          M('16\ \text{cm}^2'),
          [M('24\ \text{cm}^2'), M('12\ \text{cm}^2'), M('8\ \text{cm}^2')],
          'ទីប្រជុំទម្ងន់ចែកត្រីកោណជា ៣ ត្រីកោណតូចៗដែលមានផ្ទៃស្មើគ្នា ៖ ' + M('S_{GBC} = \dfrac{48}{3} = 16\ \text{cm}^2'))

    M_add('medium', 'iso_triangle_axis',
          'ក្នុងត្រីកោណសមបាត ' + M('ABC') + ' (' + M('AB = AC') + ') តើបន្ទាត់ពិសេសណាខ្លះដែលត្រួតស៊ីគ្នាគូសចេញពីកំពូល ' + M('A') + '?',
          'មេដ្យាន កម្ពស់ មេដ្យាទ័រ និងកន្លះបន្ទាត់ពុះមុំ',
          ['តែមេដ្យាននិងកម្ពស់ប៉ុណ្ណោះ', 'តែកម្ពស់និងបន្ទាត់ពុះមុំប៉ុណ្ណោះ', 'គ្មានបន្ទាត់ណាត្រួតស៊ីគ្នាទេ'],
          'ក្នុងត្រីកោណសមបាត បន្ទាត់ពិសេសទាំង ៤ គូសចេញពីកំពូលត្រួតស៊ីគ្នាជាបន្ទាត់តែមួយ')

    M_add('medium', 'equilateral_inradius_circumradius',
          'ក្នុងត្រីកោណសម័ង្សមួយ បើកាំរង្វង់ចារឹកក្រៅគឺ ' + M('R = 10\ \text{cm}') + ' តើកាំរង្វង់ចារឹកក្នុង ' + M('r') + ' ស្មើនឹងប៉ុន្មាន?',
          M('5\ \text{cm}'),
          [M('10\ \text{cm}'), M('2.5\ \text{cm}'), M('3.33\ \text{cm}')],
          'ក្នុងត្រីកោណសម័ង្ស ទីប្រជុំទម្ងន់ជាផ្ចិតចារឹកក្នុងនិងក្រៅ នាំឱ្យ ' + M('r = \dfrac{1}{2}R = 5\ \text{cm}'))

    # ==========================================
    # 3. MCQ HARD (7 target)
    # ==========================================
    M_add('hard', 'equilateral_height_radii',
          'ត្រីកោណសម័ង្សមួយមានរង្វាស់ជ្រុង ' + M('a = 6\sqrt{3}\ \text{cm}') + '។ គណនាកាំរង្វង់ចារឹកក្រៅ ' + M('R') + ' នៃត្រីកោណសម័ង្សនោះ។',
          M('6\ \text{cm}'),
          [M('3\ \text{cm}'), M('9\ \text{cm}'), M('12\ \text{cm}')],
          'កម្ពស់ ៖ ' + M('h = \dfrac{a\sqrt{3}}{2} = \dfrac{6\sqrt{3} \times \sqrt{3}}{2} = 9\ \text{cm}') + ' នាំឱ្យ ' + M('R = \dfrac{2}{3}h = 6\ \text{cm}'))

    M_add('hard', 'right_tri_inradius_formula',
          'ត្រីកោណកែងមួយមានជ្រុងមុំកែង ' + M('a = 6\ \text{cm}, b = 8\ \text{cm}') + ' និងអ៊ីប៉ូតេនុស ' + M('c = 10\ \text{cm}') + '។ គណនាកាំរង្វង់ចារឹកក្នុង ' + M('r') + '។',
          M('2\ \text{cm}'),
          [M('1\ \text{cm}'), M('3\ \text{cm}'), M('4\ \text{cm}')],
          M('r = \dfrac{a + b - c}{2} = \dfrac{6 + 8 - 10}{2} = \dfrac{4}{2} = 2\ \text{cm}'))

    M_add('hard', 'centroid_coordinates',
          'ក្នុងប្លង់កូអរដោនេ ត្រីកោណ ' + M('ABC') + ' មានកំពូល ' + M('A(2, 4), B(5, 1), C(5, 7)') + '។ រកកូអរដោនេនៃទីប្រជុំទម្ងន់ ' + M('G') + '។',
          M('G(4, 4)'),
          [M('G(6, 6)'), M('G(3, 4)'), M('G(4, 3)')],
          M('x_G = \dfrac{2 + 5 + 5}{3} = 4') + ', ' + M('y_G = \dfrac{4 + 1 + 7}{3} = 4 \Rightarrow G(4, 4)'))

    M_add('hard', 'area_six_subtriangles',
          'មេដ្យានទាំងបីនៃត្រីកោណ ' + M('ABC') + ' បែងចែកត្រីកោណធំជា ៦ ត្រីកោណតូចៗ។ បើផ្ទៃត្រីកោណ ' + M('ABC') + ' ស្មើ ' + M('72\ \text{cm}^2') + ' គណនាផ្ទៃនៃត្រីកោណតូចមួយ។',
          M('12\ \text{cm}^2'),
          [M('24\ \text{cm}^2'), M('18\ \text{cm}^2'), M('6\ \text{cm}^2')],
          'មេដ្យានទាំងបីចែកត្រីកោណជា ៦ ត្រីកោណតូចៗមានផ្ទៃស្មើគ្នា ៖ ' + M('\dfrac{72}{6} = 12\ \text{cm}^2'))

    M_add('hard', 'euler_line_order',
          'ក្នុងត្រីកោណមិនសម័ង្សមួយ ចំណុចអរតូសង់ ' + M('H') + ', ទីប្រជុំទម្ងន់ ' + M('G') + ' និងផ្ចិតចារឹកក្រៅ ' + M('O') + ' ស្ថិតនៅលើបន្ទាត់តែមួយ (បន្ទាត់អយល័រ Euler Line)។ តើផលធៀប ' + M('\dfrac{HG}{GO}') + ' ស្មើនឹងប៉ុន្មាន?',
          M('2'),
          [M('1'), M('\dfrac{1}{2}'), M('3')],
          'តាមទ្រឹស្តីបទបន្ទាត់អយល័រ ចម្ងាយ ' + M('HG = 2 GO \Rightarrow \dfrac{HG}{GO} = 2'))

    M_add('hard', 'angle_incenter_formula',
          'ក្នុងត្រីកោណ ' + M('ABC') + ' គេដឹងថាមុំ ' + M('\angle A = 70^\circ') + '។ ' + M('I') + ' ជាផ្ចិតរង្វង់ចារឹកក្នុងត្រីកោណ។ គណនារង្វាស់មុំ ' + M('\angle BIC') + '។',
          M('125^\circ'),
          [M('140^\circ'), M('110^\circ'), M('135^\circ')],
          M('\angle BIC = 90^\circ + \dfrac{\angle A}{2} = 90^\circ + 35^\circ = 125^\circ'))

    M_add('hard', 'orthocenter_angle_formula',
          'ក្នុងត្រីកោណស្រួច ' + M('ABC') + ' មានមុំ ' + M('\angle A = 50^\circ') + '។ ' + M('H') + ' ជាអរតូសង់នៃត្រីកោណ។ គណនារង្វាស់មុំ ' + M('\angle BHC') + '។',
          M('130^\circ'),
          [M('100^\circ'), M('140^\circ'), M('115^\circ')],
          M('\angle BHC = 180^\circ - \angle A = 180^\circ - 50^\circ = 130^\circ'))

    # ==========================================
    # 4. MCQ PISA (5 target)
    # ==========================================
    M_add('pisa', 'triangular_park_lamp',
          'សួនផ្ការាងត្រីកោណមួយមានកំពូលបីជាទីតាំងដើមឈើធំ ' + M('A, B, C') + '។ គេចង់ដាក់បង្គោលភ្លើងបំភ្លឺមួយដើមឱ្យមានចម្ងាយស្មើគ្នាទៅកាន់ដើមឈើទាំងបី។ តើគេត្រូវកំណត់ទីតាំងបង្គោលភ្លើងត្រង់ចំណុចប្រសព្វនៃបន្ទាត់អ្វី?',
          'មេដ្យាទ័រនៃជ្រុងទាំងបី (ផ្ចិតរង្វង់ចារឹកក្រៅ O)',
          ['មេដ្យាននៃជ្រុងទាំងបី', 'កម្ពស់នៃជ្រុងទាំងបី', 'កន្លះបន្ទាត់ពុះមុំ'],
          'ចំណុចដែលមានចម្ងាយស្មើគ្នាទៅកំពូលទាំងបី គឺជាផ្ចិតនៃរង្វង់ចារឹកក្រៅត្រីកោណ (ប្រសព្វមេដ្យាទ័រ)')

    M_add('pisa', 'three_roads_shop',
          'ទីប្រជុំជនមួយមានផ្លូវធំ ៣ ខ្វែងគ្នាបង្កើតបានជារាងត្រីកោណ។ អាជីវករម្នាក់ចង់បើកតូបលក់ទំនិញនៅទីតាំងមួយដែលនៅស្មើចម្ងាយពីផ្លូវទាំងបី។ តើគាត់ត្រូវជ្រើសរើសចំណុចប្រសព្វនៃបន្ទាត់ណា?',
          'កន្លះបន្ទាត់ពុះមុំក្នុងទាំងបី (ផ្ចិតរង្វង់ចារឹកក្នុង I)',
          ['មេដ្យានទាំងបី', 'មេដ្យាទ័រនៃជ្រុងទាំងបី', 'កម្ពស់ទាំងបី'],
          'ចំណុចដែលនៅស្មើចម្ងាយពីជ្រុង (ផ្លូវ) ទាំងបី គឺជាផ្ចិតរង្វង់ចារឹកក្នុង (ប្រសព្វបន្ទាត់ពុះមុំ)')

    M_add('pisa', 'triangular_plate_balance',
          'ជាងដែកម្នាក់ចង់ទប់ផ្លាកសញ្ញាផ្សាយពាណិជ្ជកម្មរាងត្រីកោណមួយផ្ទាំងឱ្យមានលំនឹងផ្ដេកដោយប្រើទ្រនាប់ចុងម្ជុលតែមួយគត់។ តើគាត់ត្រូវដាក់ទ្រនាប់ចំចំណុចណា?',
          'ទីប្រជុំទម្ងន់ G (Centroid)',
          ['អរតូសង់ H', 'ផ្ចិតរង្វង់ចារឹកក្រៅ O', 'ផ្ចិតរង្វង់ចារឹកក្នុង I'],
          'ទីប្រជុំទម្ងន់ គឺជាចំណុចកណ្តាលទំនាញ (Center of Gravity) ដែលអាចទប់វត្ថុរាងត្រីកោណឱ្យមានលំនឹង')

    M_add('pisa', 'cellular_tower_three_villages',
          'ភូមិបី ' + M('A, B, C') + ' បង្កើតបានជាត្រីកោណកែងត្រង់ ' + M('A') + ' ដែល ' + M('AB = 6\ \text{km}') + ' និង ' + M('AC = 8\ \text{km}') + '។ ក្រុមហ៊ុនទូរស័ព្ទចង់ដាក់អង់តែនមួយនៅស្មើចម្ងាយពីភូមិទាំងបី។ តើចម្ងាយពីអង់តែនទៅភូមិនីមួយៗស្មើប៉ុន្មាន?',
          M('5\ \text{km}'),
          [M('10\ \text{km}'), M('7\ \text{km}'), M('4.8\ \text{km}')],
          'អ៊ីប៉ូតេនុស ៖ ' + M('BC = 10\ \text{km}') + '។ អង់តែននៅចំកណ្តាល ' + M('BC') + ' នាំឱ្យ ' + M('R = \dfrac{10}{2} = 5\ \text{km}'))

    M_add('pisa', 'fire_station_tri_city',
          'ក្រុងបីបង្កើតបានជាត្រីកោណសម័ង្សដែលមានជ្រុង ' + M('12\ \text{km}') + '។ គេចង់សាងសង់ស្ថានីយពន្លត់អគ្គិភ័យកណ្តាលមួយដែលស្មើចម្ងាយពីក្រុងទាំងបី។ គណនាចម្ងាយពីស្ថានីយទៅកាន់ក្រុងនីមួយៗ (យក ' + M('\sqrt{3} \approx 1.732') + ')។',
          M('6.93\ \text{km}'),
          [M('10.39\ \text{km}'), M('3.46\ \text{km}'), M('6\ \text{km}')],
          M('h = \dfrac{12\sqrt{3}}{2} = 6\sqrt{3}\ \text{km} \Rightarrow R = \dfrac{2}{3}(6\sqrt{3}) = 4\sqrt{3} \approx 4 \times 1.732 = 6.93\ \text{km}'))

    # ==========================================
    # 5. WRITING EASY (1 target, 5 pts total)
    # ==========================================
    W('easy', 'wr_median_basic_calc',
      'ក្នុងត្រីកោណ ' + M('ABC') + ' មេដ្យាន ' + M("AA' = 18\ \text{cm}") + '។ ' + M('G') + ' ជាទីប្រជុំទម្ងន់នៃត្រីកោណ។\n'
      'ក. សរសេររូបមន្តទំនាក់ទំនងរវាង ' + M('AG') + ' និង ' + M("AA'") + '។\n'
      'ខ. គណនាប្រវែង ' + M('AG') + '។\n'
      'គ. គណនាប្រវែង ' + M("GA'") + '។', [
          ('ក. ទំនាក់ទំនងទីប្រជុំទម្ងន់ ៖ ' + M("AG = \dfrac{2}{3}AA'") + ' និង ' + M("GA' = \dfrac{1}{3}AA'"), 2),
          ('ខ. គណនា ' + M('AG = \dfrac{2}{3} \times 18 = 12\ \text{cm}'), 2),
          ('គ. គណនា ' + M("GA' = 18 - 12 = 6\ \text{cm}"), 1)], FIG_MEDIANS_CENTROID)

    # ==========================================
    # 6. WRITING MEDIUM (4 target, 5 pts total each)
    # ==========================================
    W('medium', 'wr_iso_tri_medians_proof',
      'គេឱ្យត្រីកោណ ' + M('ABC') + ' ដែលមានមេដ្យាន ' + M("BB'") + ' និង ' + M("CC'") + ' មានប្រវែងស្មើគ្នា (' + M("BB' = CC'") + ') កាត់គ្នាត្រង់ ' + M('G') + '។\n'
      'ក. បង្ហាញថា ' + M('GB = GC') + ' និង ' + M("GB' = GC'") + '។\n'
      'ខ. បង្ហាញថាទីប្រជុំទម្ងន់ ' + M('G') + ' ស្ថិតនៅលើមេដ្យាទ័រនៃអង្កត់ ' + M('BC') + '។\n'
      'គ. ទាញបញ្ជាក់ថាត្រីកោណ ' + M('ABC') + ' ជាត្រីកោណសមបាតកំពូល ' + M('A') + '។', [
          ('ក. ' + M("GB = \dfrac{2}{3}BB'") + ' និង ' + M("GC = \\dfrac{2}{3}CC'") + '។ ដោយ ' + M("BB' = CC' \Rightarrow GB = GC") + ' និង ' + M("GB' = GC' = \dfrac{1}{3}BB'"), 2),
          ('ខ. ដោយ ' + M('GB = GC') + ' នាំឱ្យចំណុច ' + M('G') + ' ស្មើចម្ងាយពី ' + M('B') + ' និង ' + M('C') + ' ដូចនេះ ' + M('G') + ' ស្ថិតនៅលើមេដ្យាទ័រនៃ ' + M('BC'), 1),
          ('គ. មេដ្យាន ' + M("AA'") + ' កាត់តាម ' + M('G') + ' និង ' + M("A'") + ' (ចំណុចកណ្តាល ' + M('BC') + ') នាំឱ្យ ' + M("AA'") + ' ជាមេដ្យាទ័រនៃ ' + M('BC') + ' នាំឱ្យ ' + M('AB = AC') + ' (សមបាតកំពូល ' + M('A') + ')', 2)])

    W('medium', 'wr_right_tri_circumcenter_proof',
      'ត្រីកោណ ' + M('ABC') + ' កែងត្រង់ ' + M('A') + ' មាន ' + M('AB = 12\\ \\text{cm}') + ' និង ' + M('AC = 16\\ \\text{cm}') + '។ ' + M('M') + ' ជាចំណុចកណ្តាលនៃអ៊ីប៉ូតេនុស ' + M('BC') + '។\n'
      'ក. គណនាប្រវែងអ៊ីប៉ូតេនុស ' + M('BC') + '។\n'
      'ខ. បង្ហាញថា ' + M('M') + ' ជាផ្ចិតនៃរង្វង់ចារឹកក្រៅត្រីកោណ ' + M('ABC') + '។\n'
      'គ. គណនាប្រវែងមេដ្យាន ' + M('AM') + ' និងកាំរង្វង់ចារឹកក្រៅ ' + M('R') + '។', [
          ('ក. តាមពីតាក័រ ៖ ' + M('BC = \sqrt{12^2 + 16^2} = \sqrt{144 + 256} = \sqrt{400} = 20\\ \\text{cm}'), 2),
          ('ខ. ក្នុងត្រីកោណកែង ចំណុចកណ្តាលនៃអ៊ីប៉ូតេនុសស្មើចម្ងាយពីកំពូលទាំងបី (' + M('MA = MB = MC') + ') ដូច្នេះ ' + M('M') + ' ជាផ្ចិតរង្វង់ចារឹកក្រៅ', 1),
          ('គ. ' + M('AM = \\dfrac{BC}{2} = 10\\ \\text{cm}') + ' និងកាំ ' + M('R = 10\\ \\text{cm}'), 2)])

    W('medium', 'wr_incenter_area_calc',
      'ត្រីកោណ ' + M('ABC') + ' មួយមានរង្វាស់ជ្រុង ' + M('a = 13\\ \\text{cm}, b = 14\\ \\text{cm}, c = 15\\ \\text{cm}') + ' និងមានផ្ទៃក្រឡា ' + M('S = 84\\ \\text{cm}^2') + '។\n'
      'ក. គណនាបរិមាត្រ ' + M('P') + ' និងកន្លះបរិមាត្រ ' + M('p') + ' នៃត្រីកោណនោះ។\n'
      'ខ. សរសេររូបមន្តទំនាក់ទំនងរវាងផ្ទៃក្រឡា កន្លះបរិមាត្រ និងកាំរង្វង់ចារឹកក្នុង ' + M('r') + '។\n'
      'គ. គណនាកាំរង្វង់ចារឹកក្នុង ' + M('r') + ' នៃត្រីកោណ។', [
          ('ក. បរិមាត្រ ៖ ' + M('P = 13 + 14 + 15 = 42\\ \\text{cm}') + '; កន្លះបរិមាត្រ ៖ ' + M('p = \\dfrac{42}{2} = 21\\ \\text{cm}'), 2),
          ('ខ. រូបមន្តទំនាក់ទំនង ៖ ' + M('S = p \\times r'), 1),
          ('គ. ទាញបានកាំ ៖ ' + M('r = \\dfrac{S}{p} = \\dfrac{84}{21} = 4\\ \\text{cm}'), 2)], FIG_ANGLE_BISECTORS_INCENTER)

    W('medium', 'wr_construct_centroid_c',
      'គេឱ្យអង្កត់បាត ' + M('AB = 8\\ \\text{cm}') + ' និងទីប្រជុំទម្ងន់ ' + M('G') + ' ដែលដឹងថាចម្ងាយពី ' + M('G') + ' ទៅចំណុចកណ្តាល ' + M('M') + ' នៃ ' + M('AB') + ' គឺ ' + M('GM = 3\\ \\text{cm}') + '។\n'
      'ក. ពន្យល់ពីទីតាំងនៃកំពូល ' + M('C') + ' ធៀបនឹងកន្លះបន្ទាត់ ' + M('MG') + '។\n'
      'ខ. គណនាប្រវែង ' + M('GC') + ' និងប្រវែងមេដ្យាន ' + M('MC') + ' សរុប។\n'
      'គ. រៀបរាប់ជំហានសង់កំពូល ' + M('C') + ' នៃត្រីកោណ ' + M('ABC') + '។', [
          ('ក. កំពូល ' + M('C') + ' ស្ថិតនៅលើកន្លះបន្ទាត់ ' + M('MG') + ' បន្តពី ' + M('G') + ' ព្រោះ ' + M('MC') + ' ជាមេដ្យានទីបី', 1),
          ('ខ. តាមលក្ខណៈទីប្រជុំទម្ងន់ ៖ ' + M('GC = 2GM = 2 \\times 3 = 6\\ \\text{cm}') + ' នាំឱ្យ ' + M('MC = GM + GC = 3 + 6 = 9\\ \\text{cm}'), 2),
          ('គ. ជំហានសង់ ៖ ១. កំណត់ចំណុចកណ្តាល ' + M('M') + ' នៃ ' + M('AB') + '; ២. គូសកន្លះបន្ទាត់ ' + M('MG') + '; ៣. វាស់ ' + M('GC = 6\\ \\text{cm}') + ' នៅលើកន្លះបន្ទាត់នោះ រួចភ្ជាប់ ' + M('CA, CB'), 2)])

    # ==========================================
    # 7. WRITING HARD (4 target, 5 pts total each)
    # ==========================================
    W('hard', 'wr_equilateral_all_points',
      'ត្រីកោណសម័ង្ស ' + M('ABC') + ' មួយមានរង្វាស់ជ្រុង ' + M('a = 12\\ \\text{cm}') + '។\n'
      'ក. គណនាកម្ពស់ ' + M('h') + ' នៃត្រីកោណសម័ង្សជាទម្រង់រ៉ាឌីកាល់សម្រួល។\n'
      'ខ. ពន្យល់ហេតុអ្វីបានជាចំណុច ' + M('G, O, H, I') + ' ត្រួតស៊ីគ្នា។\n'
      'គ. គណនាកាំរង្វង់ចារឹកក្រៅ ' + M('R') + ' និងកាំរង្វង់ចារឹកក្នុង ' + M('r') + '។', [
          ('ក. ' + M('h = \\dfrac{a\sqrt{3}}{2} = \\dfrac{12\sqrt{3}}{2} = 6\sqrt{3}\\ \\text{cm}'), 1),
          ('ខ. ក្នុងត្រីកោណសម័ង្ស មេដ្យាន កម្ពស់ មេដ្យាទ័រ និងកន្លះបន្ទាត់ពុះមុំត្រួតស៊ីគ្នា នាំឱ្យប្រសព្វទាំងបួន ' + M('G, O, H, I') + ' ត្រួតស៊ីគ្នាជាចំណុចតែមួយ', 2),
          ('គ. ' + M('R = \\dfrac{2}{3}h = \\dfrac{2}{3}(6\sqrt{3}) = 4\sqrt{3}\\ \\text{cm}') + ' និង ' + M('r = \\dfrac{1}{3}h = 2\sqrt{3}\\ \\text{cm}'), 2)])

    W('hard', 'wr_centroid_three_equal_areas',
      'គេឱ្យត្រីកោណ ' + M('ABC') + ' ដែលមាន ' + M('G') + ' ជាទីប្រជុំទម្ងន់ និង ' + M("A'") + ' ជាចំណុចកណ្តាលនៃ ' + M('BC') + '។\n'
      'ក. បង្ហាញថា ' + M("\mathcal{A}_{\Delta ABA'} = \mathcal{A}_{\Delta ACA'} = \\dfrac{1}{2}\mathcal{A}_{\Delta ABC}") + '។\n'
      'ខ. បង្ហាញថា ' + M("\mathcal{A}_{\Delta GBA'} = \mathcal{A}_{\Delta GCA'}") + '។\n'
      'គ. ទាញបង្ហាញថា ' + M('\mathcal{A}_{\Delta GAB} = \mathcal{A}_{\Delta GBC} = \mathcal{A}_{\Delta GCA} = \dfrac{1}{3}\mathcal{A}_{\Delta ABC}') + '។', [
          ('ក. ត្រីកោណ ' + M("ABA'") + ' និង ' + M("ACA'") + ' មានកម្ពស់រួមពី ' + M('A') + ' និងបាតស្មើគ្នា ' + M("BA' = A'C") + ' នាំឱ្យផ្ទៃស្មើគ្នា', 2),
          ('ខ. ត្រីកោណ ' + M("GBA'") + ' និង ' + M("GCA'") + ' មានកម្ពស់រួមពី ' + M('G') + ' និងបាត ' + M("BA' = A'C") + ' នាំឱ្យផ្ទៃស្មើគ្នា', 1),
          ('គ. ដកសមីការ ៖ ' + M("\mathcal{A}_{GAB} = \mathcal{A}_{ABA'} - \mathcal{A}_{GBA'}") + ' ដូចគ្នាចំពោះផ្នែកផ្សេងទៀត នាំឱ្យផ្ទៃទាំងបីស្មើគ្នា និងស្មើ ' + M('\dfrac{1}{3}\mathcal{A}_{ABC}'), 2)])

    W('hard', 'wr_orthocenter_obtuse_proof',
      'គេឱ្យត្រីកោណ ' + M('ABC') + ' ដែលមានមុំ ' + M('\angle A = 120^\circ') + ' (ត្រីកោណទាល)។ កម្ពស់គូសចេញពី ' + M('B') + ' គឺ ' + M('BE \perp AC') + ' (បន្លាយ ' + M('AC') + ') និងកម្ពស់ពី ' + M('C') + ' គឺ ' + M('CF \perp AB') + ' (បន្លាយ ' + M('AB') + ') ប្រសព្វគ្នាត្រង់ ' + M('H') + '។\n'
      'ក. ពន្យល់ហេតុអ្វីបានជាជើងកម្ពស់ ' + M('E') + ' និង ' + M('F') + ' ធ្លាក់នៅក្រៅជ្រុងនៃត្រីកោណ។\n'
      'ខ. គណនាមុំ ' + M('\angle EAF') + '។\n'
      'គ. គណនាមុំ ' + M('\angle BHC') + ' នៃអរតូសង់។', [
          ('ក. មុំ ' + M('\angle A = 120^\circ > 90^\circ') + ' នាំឱ្យកម្ពស់គូសពី ' + M('B') + ' និង ' + M('C') + ' ត្រូវធ្លាក់លើបន្ទាត់បន្លាយនៃជ្រុងឈម (នៅក្រៅត្រីកោណ)', 2),
          ('ខ. មុំ ' + M('\angle EAF') + ' និងមុំ ' + M('\angle BAC') + ' ជាមុំទល់កំពូល នាំឱ្យ ' + M('\angle EAF = 120^\circ'), 1),
          ('គ. ក្នុងចតុកោណ ' + M('AFHE') + ' មានមុំកែងពីរត្រង់ ' + M('E') + ' និង ' + M('F') + ' នាំឱ្យ ' + M('\angle BHC = 180^\circ - 120^\circ = 60^\circ'), 2)])

    W('hard', 'wr_right_triangle_all_radii',
      'ត្រីកោណ ' + M('ABC') + ' កែងត្រង់ ' + M('A') + ' មានជ្រុងមុំកែង ' + M('AB = 5\ \text{cm}') + ' និង ' + M('AC = 12\ \text{cm}') + '។\n'
      'ក. គណនាប្រវែងអ៊ីប៉ូតេនុស ' + M('BC') + ' និងផ្ទៃក្រឡា ' + M('S') + '។\n'
      'ខ. គណនាកាំរង្វង់ចារឹកក្រៅ ' + M('R') + '។\n'
      'គ. គណនាកាំរង្វង់ចារឹកក្នុង ' + M('r') + '។', [
          ('ក. ' + M('BC = \sqrt{5^2 + 12^2} = 13\ \text{cm}') + '; ផ្ទៃក្រឡា ៖ ' + M('S = \dfrac{5 \times 12}{2} = 30\ \text{cm}^2'), 2),
          ('ខ. កាំរង្វង់ចារឹកក្រៅ ៖ ' + M('R = \dfrac{BC}{2} = \dfrac{13}{2} = 6.5\ \text{cm}'), 1),
          ('គ. កន្លះបរិមាត្រ ' + M('p = \dfrac{5 + 12 + 13}{2} = 15\ \text{cm} \Rightarrow r = \dfrac{S}{p} = \dfrac{30}{15} = 2\ \text{cm}'), 2)])

    # ==========================================
    # 8. WRITING PISA (5 target, 5 pts total each)
    # ==========================================
    W('pisa', 'wr_pisa_park_lighting',
      'សួនសាធារណៈមួយមានរាងជាត្រីកោណ ' + M('ABC') + ' ដែលមានជ្រុង ' + M('AB = 30\ \text{m}, BC = 40\ \text{m}, AC = 50\ \text{m}') + '។ គណៈកម្មការសួនចង់ដំឡើងបង្គោលភ្លើងហ្វាបំភ្លឺមួយដើមឱ្យស្មើចម្ងាយពីកំពូលសួនទាំងបី។\n'
      'ក. បង្ហាញថាត្រីកោណ ' + M('ABC') + ' ជាត្រីកោណកែង។\n'
      'ខ. កំណត់ទីតាំងពិតប្រាកដដែលត្រូវដំឡើងបង្គោលភ្លើង។\n'
      'គ. គណនាចម្ងាយពីបង្គោលភ្លើងទៅកាន់កំពូលសួននីមួយៗ។', [
          ('ក. ' + M('30^2 + 40^2 = 900 + 1600 = 2500 = 50^2') + ' តាមទ្រឹស្តីបទច្រាសពីតាក័រ ត្រីកោណ ' + M('ABC') + ' កែងត្រង់ ' + M('B'), 2),
          ('ខ. បង្គោលភ្លើងត្រូវនៅស្មើចម្ងាយពីកំពូលទាំងបី ដូច្នេះវាជាផ្ចិតចារឹកក្រៅ ដែលស្ថិតនៅចំចំណុចកណ្តាលនៃអ៊ីប៉ូតេនុស ' + M('AC'), 2),
          ('គ. ចម្ងាយទៅកំពូលនីមួយៗគឺ ' + M('R = \dfrac{50}{2} = 25\ \text{m}'), 1)])

    W('pisa', 'wr_pisa_hospital_location',
      'មន្ទីរសុខាភិបាលចង់សាងសង់មន្ទីរពេទ្យបង្អែកថ្មីមួយនៅទីតាំងមួយដែលនៅស្មើចម្ងាយពីផ្លូវជាតិទាំងបីដែលព័ទ្ធជុំវិញស្រុក (ផ្លូវទាំងបីខ្វែងគ្នាជារាងត្រីកោណ)។\n'
      'ក. តើទីតាំងមន្ទីរពេទ្យត្រូវជាចំណុចពិសេសណា ក្នុងចំណោមចំណុច ' + M('G, O, H, I') + '? ពន្យល់។\n'
      'ខ. បើផ្ទៃដីត្រីកោណនោះមានទំហំ ' + M('60\ \text{km}^2') + ' និងផលបូកប្រវែងផ្លូវទាំងបីគឺ ' + M('30\ \text{km}') + ' គណនាចម្ងាយកែងពីមន្ទីរពេទ្យទៅកាន់ផ្លូវនីមួយៗ។\n'
      'គ. ហេតុអ្វីបានជាការជ្រើសរើសចំណុចនេះមានសារៈសំខាន់សម្រាប់រថយន្តសង្គ្រោះបន្ទាន់?', [
          ('ក. ត្រូវជាចំណុច ' + M('I') + ' (ផ្ចិតរង្វង់ចារឹកក្នុង) ព្រោះចំណុចនេះនៅស្មើចម្ងាយពីជ្រុង (ផ្លូវ) ទាំងបីនៃត្រីកោណ', 2),
          ('ខ. កន្លះបរិមាត្រ ' + M('p = \dfrac{30}{2} = 15\ \text{km}') + '។ ចម្ងាយកែងទៅផ្លូវនីមួយៗគឺ ' + M('r = \dfrac{S}{p} = \dfrac{60}{15} = 4\ \text{km}'), 2),
          ('គ. ធានាថារថយន្តសង្គ្រោះបន្ទាន់អាចចេញទៅកាន់ផ្លូវជាតិទាំងបីដោយប្រើចម្ងាយជិតបំផុតស្មើៗគ្នា (ត្រឹម ' + M('4\ \text{km}') + ')', 1)])

    W('pisa', 'wr_pisa_signboard_support',
      'វិស្វករម្នាក់រចនាផ្លាកសញ្ញាចរាចរណ៍រាងត្រីកោណសម័ង្សមួយផ្ទាំងមានជ្រុង ' + M('60\ \text{cm}') + '។ គាត់ត្រូវភ្ជាប់បង្គោលទប់នៅចំចំណុចកណ្តាលទំនាញ (ទីប្រជុំទម្ងន់ ' + M('G') + ')។\n'
      'ក. គណនាកម្ពស់ ' + M('h') + ' នៃផ្លាកសញ្ញា (យក ' + M('\sqrt{3} \approx 1.732') + ')។\n'
      'ខ. គណនាចម្ងាយពីចំណុចភ្ជាប់បង្គោល ' + M('G') + ' ទៅកាន់បាតខាងក្រោមនៃផ្លាកសញ្ញា។\n'
      'គ. គណនាចម្ងាយពីចំណុច ' + M('G') + ' ទៅកាន់កំពូលខាងលើនៃផ្លាកសញ្ញា។', [
          ('ក. កម្ពស់ ៖ ' + M('h = \dfrac{60\sqrt{3}}{2} = 30\sqrt{3} \approx 30 \times 1.732 = 51.96\ \text{cm}'), 2),
          ('ខ. ចម្ងាយទៅបាត ៖ ' + M("GA' = \dfrac{1}{3}h = \dfrac{51.96}{3} = 17.32\ \text{cm}"), 1),
          ('គ. ចម្ងាយទៅកំពូល ៖ ' + M('AG = \\dfrac{2}{3}h = 2 \\times 17.32 = 34.64\\ \\text{cm}'), 2)])

    W('pisa', 'wr_pisa_three_substations',
      'អនុស្ថានីយអគ្គិសនីចំនួន ៣ ស្ថិតនៅទីតាំង ' + M('A, B, C') + '។ គេចង់សង់មជ្ឈមណ្ឌលចែកចាយថាមពលមេ ' + M('O') + ' មួយដែលស្មើចម្ងាយពីអនុស្ថានីយទាំងបី។ ដឹងថា ' + M('AB = AC = 10\\ \\text{km}') + ' និង ' + M('BC = 12\\ \\text{km}') + '។\n'
      'ក. គណនាកម្ពស់ ' + M('AH') + ' នៃត្រីកោណសមបាត ' + M('ABC') + '។\n'
      'ខ. គណនាផ្ទៃក្រឡានៃត្រីកោណ ' + M('ABC') + '។\n'
      'គ. គណនាចម្ងាយខ្សែបណ្តាញពីមជ្ឈមណ្ឌល ' + M('O') + ' ទៅកាន់អនុស្ថានីយនីមួយៗ (' + M('R = \\dfrac{abc}{4S}') + ')។', [
          ('ក. ' + M('BH = 6\\ \\text{km} \\Rightarrow AH = \sqrt{10^2 - 6^2} = 8\\ \\text{km}'), 2),
          ('ខ. ផ្ទៃក្រឡា ៖ ' + M('S = \\dfrac{12 \\times 8}{2} = 48\\ \\text{km}^2'), 1),
          ('គ. ចម្ងាយខ្សែបណ្តាញ ៖ ' + M('R = \\dfrac{10 \\times 10 \\times 12}{4 \\times 48} = \\dfrac{1200}{192} = 6.25\\ \\text{km}'), 2)])

    W('pisa', 'wr_pisa_helicopter_landing',
      'មូលដ្ឋានយោធាបី ' + M('A, B, C') + ' បង្កើតបានជាត្រីកោណមួយ។ ឧទ្ធម្ភាគចក្រមួយគ្រឿងចង់ចុះចតនៅចំណុចមួយក្នុងតំបន់ត្រីកោណ ដែលចំណុចនោះបង្កើតបានជា ៣ តំបន់ស្មើផ្ទៃគ្នាសម្រាប់កងកម្លាំងនីមួយៗទទួលខុសត្រូវ។\n'
      'ក. តើចំណុចចុះចតនោះត្រូវជាចំណុចពិសេសណា ក្នុងចំណោម ' + M('G, O, H, I') + '?\n'
      'ខ. ពន្យល់មូលហេតុធរណីមាត្រដែលធ្វើឱ្យផ្ទៃទាំងបីស្មើគ្នា។\n'
      'គ. បើផ្ទៃដីរួមគឺ ' + M('90\\ \\text{km}^2') + ' គណនាផ្ទៃដីនៃតំបន់នីមួយៗ។', [
          ('ក. ចំណុចចុះចតត្រូវជា ទីប្រជុំទម្ងន់ ' + M('G') + ' (Centroid)', 1),
          ('ខ. មេដ្យានទាំងបីចែកត្រីកោណជា ៦ ត្រីកោណតូចៗមានផ្ទៃស្មើគ្នា នាំឱ្យត្រីកោណ ' + M('GAB, GBC, GCA') + ' នីមួយៗផ្សំដោយ ២ ត្រីកោណតូច ដូច្នេះផ្ទៃទាំងបីស្មើគ្នា', 2),
          ('គ. ផ្ទៃដីតំបន់នីមួយៗ ៖ ' + M('\\dfrac{90}{3} = 30\\ \\text{km}^2'), 2)])

    return C
