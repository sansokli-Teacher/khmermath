"""Bank candidates for Grade 8, Lesson 15: ផ្ទៃក្រឡាពហុកោណ (Area of Polygons)
Covers MoEYS Grade 8 curriculum:
  1. ផ្ទៃក្រឡាប្រលេឡូក្រាម (Area of parallelogram: S = b * h)
  2. ផ្ទៃក្រឡាចតុកោណព្នាយ (Area of trapezoid: S = (a + b) * h / 2)
  3. ផ្ទៃក្រឡាចតុកោណស្មើ និងចតុកោណខ្លែង (Area of rhombus & kite: S = d1 * d2 / 2)
  4. ផ្ទៃក្រឡាពហុកោណផ្សំ និងផ្នែកប្រផេះ (Composite figures, shaded regions, L-shapes, octagons)
  5. ការអនុវត្តក្នុងជីវភាពរស់នៅ & PISA (Rubber plantation, rose garden, building glass facade, roofing, field division)

Images: Clean vector illustrations, isolated, no background, flat educational textbook style.
Geometry labels use font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic'.
"""
from lib import *

LESSON = "ផ្ទៃក្រឡាពហុកោណ"

# --- SVG Illustrations ---

# 1. FIG_AREA_PARALLELOGRAM: Parallelogram ABCD with base b and height h
FIG_AREA_PARALLELOGRAM = (
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 280 160' width='280' height='160'>\n"
    "  <!-- Parallelogram ABCD -->\n"
    "  <polygon points='70,30 240,30 190,130 20,130' fill='#f0fdf4' stroke='#16a34a' stroke-width='2'/>\n"
    "  <!-- Altitude AH perpendicular to extended or inside base DC -->\n"
    "  <line x1='70' y1='30' x2='70' y2='130' stroke='#dc2626' stroke-width='1.5' stroke-dasharray='4,3'/>\n"
    "  <path d='M 70,118 L 82,118 L 82,130' fill='none' stroke='#dc2626' stroke-width='1.2'/>\n"
    "  <!-- Vertices (Mathcad italic) -->\n"
    "  <text x='65' y='22' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>A</text>\n"
    "  <text x='248' y='26' text-anchor='start' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>B</text>\n"
    "  <text x='198' y='144' text-anchor='start' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>C</text>\n"
    "  <text x='12' y='144' text-anchor='end' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>D</text>\n"
    "  <text x='70' y='144' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='13' fill='#dc2626'>H</text>\n"
    "  <!-- Height label h and base label b -->\n"
    "  <text x='62' y='85' text-anchor='end' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#dc2626'>h</text>\n"
    "  <line x1='20' y1='148' x2='190' y2='148' stroke='#0284c7' stroke-width='1' stroke-dasharray='3,2'/>\n"
    "  <text x='105' y='158' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0284c7'>b</text>\n"
    "</svg>"
)

# 2. FIG_AREA_TRAPEZOID: Trapezoid ABCD with top base a, bottom base b, and height h
FIG_AREA_TRAPEZOID = (
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 280 160' width='280' height='160'>\n"
    "  <!-- Trapezoid ABCD -->\n"
    "  <polygon points='75,30 185,30 235,130 25,130' fill='#eff6ff' stroke='#0284c7' stroke-width='2'/>\n"
    "  <!-- Parallel arrows on AB and CD -->\n"
    "  <polygon points='126,27 134,30 126,33' fill='#0284c7'/>\n"
    "  <polygon points='126,127 134,130 126,133' fill='#0284c7'/>\n"
    "  <!-- Altitude AH perpendicular to CD -->\n"
    "  <line x1='75' y1='30' x2='75' y2='130' stroke='#dc2626' stroke-width='1.5' stroke-dasharray='4,3'/>\n"
    "  <path d='M 75,118 L 87,118 L 87,130' fill='none' stroke='#dc2626' stroke-width='1.2'/>\n"
    "  <!-- Vertices (Mathcad italic) -->\n"
    "  <text x='70' y='22' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>A</text>\n"
    "  <text x='192' y='24' text-anchor='start' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>B</text>\n"
    "  <text x='244' y='142' text-anchor='start' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>C</text>\n"
    "  <text x='16' y='142' text-anchor='end' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>D</text>\n"
    "  <text x='75' y='144' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='13' fill='#dc2626'>H</text>\n"
    "  <!-- Base labels a, b and height h -->\n"
    "  <text x='130' y='22' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='13' fill='#0f172a'>a</text>\n"
    "  <text x='130' y='146' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='13' fill='#0f172a'>b</text>\n"
    "  <text x='66' y='85' text-anchor='end' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#dc2626'>h</text>\n"
    "</svg>"
)

# 3. FIG_AREA_RHOMBUS: Rhombus ABCD with diagonals d1, d2
FIG_AREA_RHOMBUS = (
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 240 180' width='240' height='180'>\n"
    "  <!-- Rhombus ABCD -->\n"
    "  <polygon points='120,20 210,90 120,160 30,90' fill='#fdf4ff' stroke='#a855f7' stroke-width='2'/>\n"
    "  <!-- Diagonals AC and BD -->\n"
    "  <line x1='120' y1='20' x2='120' y2='160' stroke='#0284c7' stroke-width='1.5' stroke-dasharray='4,3'/>\n"
    "  <line x1='30' y1='90' x2='210' y2='90' stroke='#0284c7' stroke-width='1.5' stroke-dasharray='4,3'/>\n"
    "  <!-- Right angle marker at O(120, 90) -->\n"
    "  <path d='M 120,80 L 130,80 L 130,90' fill='none' stroke='#0284c7' stroke-width='1.2'/>\n"
    "  <!-- Center intersection O -->\n"
    "  <circle cx='120' cy='90' r='3' fill='#dc2626'/>\n"
    "  <!-- Vertices (Mathcad italic) -->\n"
    "  <text x='120' y='14' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>A</text>\n"
    "  <text x='222' y='94' text-anchor='start' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>B</text>\n"
    "  <text x='120' y='175' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>C</text>\n"
    "  <text x='18' y='94' text-anchor='end' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>D</text>\n"
    "  <text x='132' y='104' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='12' fill='#dc2626'>O</text>\n"
    "  <!-- Diagonal labels -->\n"
    "  <text x='112' y='55' text-anchor='end' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='13' fill='#0284c7'>d₁</text>\n"
    "  <text x='170' y='82' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='13' fill='#0284c7'>d₂</text>\n"
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
    M_add('easy', 'para_area_formula',
          'តើរូបមន្តសម្រាប់គណនាផ្ទៃក្រឡាប្រលេឡូក្រាមដែលមានបាត ' + M('b') + ' និងកម្ពស់ ' + M('h') + ' ណាត្រឹមត្រូវ?',
          M('S = b \\times h'),
          [M('S = \\dfrac{b \\times h}{2}'), M('S = 2(b + h)'), M('S = b^2 \\times h')],
          'ផ្ទៃក្រឡាប្រលេឡូក្រាមស្មើផលគុណរវាងបាតនិងកម្ពស់ត្រូវគ្នា ៖ ' + M('S = b \\times h'),
          FIG_AREA_PARALLELOGRAM)

    M_add('easy', 'trap_area_formula',
          'តើរូបមន្តសម្រាប់គណនាផ្ទៃក្រឡាចតុកោណព្នាយដែលមានបាតទាំងពីរ ' + M('a, b') + ' និងកម្ពស់ ' + M('h') + ' ណាត្រឹមត្រូវ?',
          M('S = \\dfrac{(a + b) \\times h}{2}'),
          [M('S = (a + b) \\times h'), M('S = \\dfrac{a \\times b \\times h}{2}'), M('S = \\dfrac{a + b}{h}')],
          'ផ្ទៃក្រឡាចតុកោណព្នាយស្មើកន្លះផលបូកបាតទាំងពីរគុណនឹងកម្ពស់ ៖ ' + M('S = \\dfrac{(a+b)h}{2}'),
          FIG_AREA_TRAPEZOID)

    M_add('easy', 'rhombus_area_formula',
          'តើរូបមន្តសម្រាប់គណនាផ្ទៃក្រឡាចតុកោណស្មើដែលមានអង្កត់ទ្រូង ' + M('d_1') + ' និង ' + M('d_2') + ' ណាត្រឹមត្រូវ?',
          M('S = \\dfrac{d_1 \\times d_2}{2}'),
          [M('S = d_1 \\times d_2'), M('S = 2(d_1 + d_2)'), M('S = \\dfrac{d_1 + d_2}{2}')],
          'ផ្ទៃក្រឡាចតុកោណស្មើស្មើកន្លះផលគុណនៃអង្កត់ទ្រូងទាំងពីរ ៖ ' + M('S = \\dfrac{d_1 \\times d_2}{2}'),
          FIG_AREA_RHOMBUS)

    M_add('easy', 'calc_para_basic',
          'ប្រលេឡូក្រាមមួយមានបាត ' + M('8\\ \\text{cm}') + ' និងកម្ពស់ត្រូវគ្នា ' + M('5\\ \\text{cm}') + '។ គណនាផ្ទៃក្រឡារបស់វា។',
          M('40\\ \\text{cm}^2'),
          [M('20\\ \\text{cm}^2'), M('26\\ \\text{cm}^2'), M('80\\ \\text{cm}^2')],
          M('S = b \\times h = 8 \\times 5 = 40\\ \\text{cm}^2'))

    M_add('easy', 'calc_trap_basic',
          'ចតុកោណព្នាយមួយមានបាតតូច ' + M('6\\ \\text{cm}') + ', បាតធំ ' + M('10\\ \\text{cm}') + ' និងកម្ពស់ ' + M('4\\ \\text{cm}') + '។ គណនាផ្ទៃក្រឡា។',
          M('32\\ \\text{cm}^2'),
          [M('64\\ \\text{cm}^2'), M('24\\ \\text{cm}^2'), M('40\\ \\text{cm}^2')],
          M('S = \\dfrac{(6 + 10) \\times 4}{2} = \\dfrac{16 \\times 4}{2} = 32\\ \\text{cm}^2'))

    M_add('easy', 'calc_rhombus_basic',
          'ចតុកោណស្មើមួយមានអង្កត់ទ្រូងទាំងពីរប្រវែង ' + M('10\\ \\text{cm}') + ' និង ' + M('8\\ \\text{cm}') + '។ គណនាផ្ទៃក្រឡា។',
          M('40\\ \\text{cm}^2'),
          [M('80\\ \\text{cm}^2'), M('36\\ \\text{cm}^2'), M('20\\ \\text{cm}^2')],
          M('S = \\dfrac{10 \\times 8}{2} = 40\\ \\text{cm}^2'))

    M_add('easy', 'calc_kite_basic',
          'ចតុកោណខ្លែងមួយមានអង្កត់ទ្រូងកាត់គ្នាកែងប្រវែង ' + M('14\\ \\text{cm}') + ' និង ' + M('6\\ \\text{cm}') + '។ គណនាផ្ទៃក្រឡារបស់វា។',
          M('42\\ \\text{cm}^2'),
          [M('84\\ \\text{cm}^2'), M('20\\ \\text{cm}^2'), M('40\\ \\text{cm}^2')],
          M('S = \\dfrac{14 \\times 6}{2} = 42\\ \\text{cm}^2'))

    M_add('easy', 'calc_square_side11',
          'ការេមួយមានរង្វាស់ជ្រុង ' + M('11\\ \\text{cm}') + '។ គណនាផ្ទៃក្រឡានៃការេនោះ។',
          M('121\\ \\text{cm}^2'),
          [M('44\\ \\text{cm}^2'), M('22\\ \\text{cm}^2'), M('110\\ \\text{cm}^2')],
          M('S = a^2 = 11^2 = 121\\ \\text{cm}^2'))

    M_add('easy', 'calc_rec_area_easy',
          'ចតុកោណកែងមួយមានបណ្តោយ ' + M('15\\ \\text{m}') + ' និងទទឹង ' + M('8\\ \\text{m}') + '។ គណនាផ្ទៃក្រឡារបស់វា។',
          M('120\\ \\text{m}^2'),
          [M('46\\ \\text{m}^2'), M('60\\ \\text{m}^2'), M('240\\ \\text{m}^2')],
          M('S = 15 \\times 8 = 120\\ \\text{m}^2'))

    M_add('easy', 'trap_median_calc',
          'ចតុកោណព្នាយមួយមានបន្ទាត់មធ្យម ' + M('m = 12\\ \\text{cm}') + ' និងកម្ពស់ ' + M('h = 5\\ \\text{cm}') + '។ គណនាផ្ទៃក្រឡារបស់វា។',
          M('60\\ \\text{cm}^2'),
          [M('30\\ \\text{cm}^2'), M('17\\ \\text{cm}^2'), M('120\\ \\text{cm}^2')],
          M('S = m \\times h = 12 \\times 5 = 60\\ \\text{cm}^2'))

    # ==========================================
    # 2. MCQ MEDIUM (14 target)
    # ==========================================
    M_add('medium', 'para_find_height',
          'ប្រលេឡូក្រាមមួយមានផ្ទៃក្រឡា ' + M('72\\ \\text{cm}^2') + ' និងបាតប្រវែង ' + M('9\\ \\text{cm}') + '។ គណនាកម្ពស់ត្រូវគ្នានឹងបាតនេះ។',
          M('8\\ \\text{cm}'),
          [M('6\\ \\text{cm}'), M('9\\ \\text{cm}'), M('12\\ \\text{cm}')],
          M('h = \\dfrac{S}{b} = \\dfrac{72}{9} = 8\\ \\text{cm}'))

    M_add('medium', 'trap_find_height',
          'ចតុកោណព្នាយមួយមានផ្ទៃក្រឡា ' + M('90\\ \\text{cm}^2') + ' និងបាតទាំងពីរមានរង្វាស់ ' + M('8\\ \\text{cm}') + ' និង ' + M('12\\ \\text{cm}') + '។ គណនាកម្ពស់។',
          M('9\\ \\text{cm}'),
          [M('4.5\\ \\text{cm}'), M('18\\ \\text{cm}'), M('10\\ \\text{cm}')],
          M('h = \\dfrac{2S}{a + b} = \\dfrac{2 \\times 90}{8 + 12} = \\dfrac{180}{20} = 9\\ \\text{cm}'))

    M_add('medium', 'trap_find_base',
          'ចតុកោណព្នាយមួយមានផ្ទៃក្រឡា ' + M('84\\ \\text{cm}^2') + ', កម្ពស់ ' + M('7\\ \\text{cm}') + ' និងបាតមួយមានរង្វាស់ ' + M('10\\ \\text{cm}') + '។ គណនារង្វាស់បាតមួយទៀត។',
          M('14\\ \\text{cm}'),
          [M('12\\ \\text{cm}'), M('16\\ \\text{cm}'), M('8\\ \\text{cm}')],
          M('a + b = \\dfrac{2S}{h} = \\dfrac{168}{7} = 24 \\Rightarrow b = 24 - 10 = 14\\ \\text{cm}'))

    M_add('medium', 'rhombus_find_diag',
          'ចតុកោណស្មើមួយមានផ្ទៃក្រឡា ' + M('60\\ \\text{cm}^2') + ' និងអង្កត់ទ្រូងមួយមានប្រវែង ' + M('12\\ \\text{cm}') + '។ គណនាប្រវែងអង្កត់ទ្រូងមួយទៀត។',
          M('10\\ \\text{cm}'),
          [M('5\\ \\text{cm}'), M('8\\ \\text{cm}'), M('15\\ \\text{cm}')],
          M('d_2 = \\dfrac{2S}{d_1} = \\dfrac{2 \\times 60}{12} = 10\\ \\text{cm}'))

    M_add('medium', 'para_two_altitudes',
          'ប្រលេឡូក្រាម ' + M('ABCD') + ' មានជ្រុង ' + M('AB = 15\\ \\text{cm}') + ' និង ' + M('BC = 10\\ \\text{cm}') + '។ កម្ពស់ត្រូវនឹងបាត ' + M('AB') + ' គឺ ' + M('6\\ \\text{cm}') + '។ គណនាកម្ពស់ត្រូវនឹងបាត ' + M('BC') + '។',
          M('9\\ \\text{cm}'),
          [M('4\\ \\text{cm}'), M('8\\ \\text{cm}'), M('12\\ \\text{cm}')],
          M('S = 15 \\times 6 = 90\\ \\text{cm}^2 \\Rightarrow h_2 = \\dfrac{90}{10} = 9\\ \\text{cm}'))

    M_add('medium', 'iso_trap_pyth_area',
          'ចតុកោណព្នាយសមបាតមួយមានបាតតូច ' + M('10\\ \\text{cm}') + ', បាតធំ ' + M('22\\ \\text{cm}') + ' និងជ្រុងទ្រេត ' + M('10\\ \\text{cm}') + '។ គណនាផ្ទៃក្រឡា។',
          M('128\\ \\text{cm}^2'),
          [M('160\\ \\text{cm}^2'), M('96\\ \\text{cm}^2'), M('256\\ \\text{cm}^2')],
          M('x = \\dfrac{22 - 10}{2} = 6\\ \\text{cm} \\Rightarrow h = \sqrt{10^2 - 6^2} = 8\\ \\text{cm}') + '។ ផ្ទៃ ៖ ' + M('S = \\dfrac{(10+22) \\times 8}{2} = 128\\ \\text{cm}^2'))

    M_add('medium', 'right_trap_area_calc',
          'ចតុកោណព្នាយកែងមួយមានបាតទាំងពីរប្រវែង ' + M('7.5\\ \\text{cm}') + ' និង ' + M('12\\ \\text{cm}') + ' ហើយកម្ពស់ប្រវែង ' + M('3\\ \\text{cm}') + '។ គណនាផ្ទៃក្រឡា។',
          M('29.25\\ \\text{cm}^2'),
          [M('58.5\\ \\text{cm}^2'), M('24.5\\ \\text{cm}^2'), M('32.5\\ \\text{cm}^2')],
          M('S = \\dfrac{(7.5 + 12) \\times 3}{2} = \\dfrac{19.5 \\times 3}{2} = 29.25\\ \\text{cm}^2'))

    M_add('medium', 'rhombus_side_diag_area',
          'ចតុកោណស្មើមួយមានជ្រុងប្រវែង ' + M('13\\ \\text{cm}') + ' និងអង្កត់ទ្រូងមួយប្រវែង ' + M('24\\ \\text{cm}') + '។ គណនាផ្ទៃក្រឡានៃចតុកោណស្មើ។',
          M('120\\ \\text{cm}^2'),
          [M('240\\ \\text{cm}^2'), M('60\\ \\text{cm}^2'), M('312\\ \\text{cm}^2')],
          'កន្លះអង្កត់ទ្រូងទីពីរ ៖ ' + M('\sqrt{13^2 - 12^2} = 5\\ \\text{cm} \\Rightarrow d_2 = 10\\ \\text{cm}') + '។ ផ្ទៃ ៖ ' + M('S = \\dfrac{24 \\times 10}{2} = 120\\ \\text{cm}^2'))

    M_add('medium', 'ha_conversion_rubber',
          'ចម្ការកៅស៊ូមួយរាងចតុកោណកែងមានបណ្តោយ ' + M('5\\ \\text{km}') + ' និងទទឹង ' + M('2.3\\ \\text{km}') + '។ គណនាផ្ទៃក្រឡាចម្ការគិតជាហិកតា (' + M('\\text{ha}') + ')។',
          M('1150\\ \\text{ha}'),
          [M('115\\ \\text{ha}'), M('11.5\\ \\text{ha}'), M('11\\,500\\ \\text{ha}')],
          M('S = 5 \\times 2.3 = 11.5\\ \\text{km}^2') + '។ ដោយ ' + M('1\\ \\text{km}^2 = 100\\ \\text{ha} \\Rightarrow S = 11.5 \\times 100 = 1150\\ \\text{ha}'))

    M_add('medium', 'rose_garden_calc',
          'សួនផ្កាកុលាបរាងត្រីកោណមានបាត ' + M('5\\ \\text{m}') + ' និងកម្ពស់ ' + M('3\\ \\text{m}') + '។ បើដាំផ្កាកុលាប ១ ដើមត្រូវការផ្ទៃ ' + M('0.5\\ \\text{m}^2') + ' តើគេអាចដាំផ្កាបានប៉ុន្មានដើម?',
          M('15\\ \\text{ដើម}'),
          [M('30\\ \\text{ដើម}'), M('10\\ \\text{ដើម}'), M('7.5\\ \\text{ដើម}')],
          M('S = \\dfrac{5 \\times 3}{2} = 7.5\\ \\text{m}^2 \\Rightarrow N = \\dfrac{7.5}{0.5} = 15\\ \\text{ដើម}'))

    M_add('medium', 'shaded_trap_cutout',
          'ចតុកោណព្នាយមានបាត ' + M('12\\ \\text{cm}') + ' និង ' + M('16\\ \\text{cm}') + ' កម្ពស់ ' + M('10\\ \\text{cm}') + '។ គេកាត់ប្រហោងត្រីកោណបាត ' + M('8\\ \\text{cm}') + ' និងកម្ពស់ ' + M('10\\ \\text{cm}') + ' ចេញ។ រកផ្ទៃក្រឡាផ្នែកនៅសល់។',
          M('100\\ \\text{cm}^2'),
          [M('140\\ \\text{cm}^2'), M('40\\ \\text{cm}^2'), M('80\\ \\text{cm}^2')],
          M('S_{\\text{ព្នាយ}} = \\dfrac{(12+16) \\times 10}{2} = 140') + '; ' + M('S_{\Delta} = \\dfrac{8 \\times 10}{2} = 40 \\Rightarrow S = 140 - 40 = 100\\ \\text{cm}^2'))

    M_add('medium', 'l_shape_area_calc',
          'ដីមួយកន្លែងរាងអក្សរ L បំបែកជាចតុកោណកែងពីរ ៖ មួយមានទំហំ ' + M('9\\ \\text{m} \\times 15\\ \\text{m}') + ' និងមួយទៀត ' + M('12\\ \\text{m} \\times 9\\ \\text{m}') + '។ គណនាផ្ទៃក្រឡាសរុប។',
          M('243\\ \\text{m}^2'),
          [M('216\\ \\text{m}^2'), M('189\\ \\text{m}^2'), M('300\\ \\text{m}^2')],
          M('S = (9 \\times 15) + (12 \\times 9) = 135 + 108 = 243\\ \\text{m}^2'))

    M_add('medium', 'octagon_from_square',
          'ក្រដាសរាងការេមួយមានជ្រុង ' + M('9\\ \\text{cm}') + '។ គេកាត់ជ្រុងទាំងបួនចេញជាត្រីកោណកែងសមបាតមានជ្រុងមុំកែង ' + M('3\\ \\text{cm}') + '។ គណនាផ្ទៃក្រឡាអដ្ឋកោណដែលនៅសល់។',
          M('63\\ \\text{cm}^2'),
          [M('72\\ \\text{cm}^2'), M('54\\ \\text{cm}^2'), M('69\\ \\text{cm}^2')],
          M('S_{\\text{ការេ}} = 9^2 = 81') + '; ផ្ទៃកាត់ ៖ ' + M('4 \\times \\dfrac{3 \\times 3}{2} = 18 \\Rightarrow S = 81 - 18 = 63\\ \\text{cm}^2'))

    M_add('medium', 'house_shape_area',
          'ផ្ទៃជញ្ជាំងមុខផ្ទះផ្សំដោយចតុកោណកែង ' + M('10\\ \\text{m} \\times 6\\ \\text{m}') + ' និងត្រីកោណដំបូលខាងលើមានបាត ' + M('10\\ \\text{m}') + ' និងកម្ពស់ ' + M('4\\ \\text{m}') + '។ គណនាផ្ទៃក្រឡាសរុប។',
          M('80\\ \\text{m}^2'),
          [M('100\\ \\text{m}^2'), M('70\\ \\text{m}^2'), M('85\\ \\text{m}^2')],
          M('S = (10 \\times 6) + \\dfrac{10 \\times 4}{2} = 60 + 20 = 80\\ \\text{m}^2'))

    # ==========================================
    # 3. MCQ HARD (7 target)
    # ==========================================
    M_add('hard', 'shaded_quad_corners',
          'ចតុកោណកែង ' + M('ABCD') + ' មានវិមាត្រ ' + M('25\\ \\text{cm} \\times 17\\ \\text{cm}') + ' (ផ្ទៃ ' + M('425\\ \\text{cm}^2') + ')។ គេគូសចតុកោណ ' + M('PQRS') + ' នៅខាងក្នុងដោយបន្សល់ទុកត្រីកោណកែង 4 នៅជ្រុងដែលមានផ្ទៃរៀងគ្នា ' + M('88\\ \\text{cm}^2,\\ 22.5\\ \\text{cm}^2,\\ 140\\ \\text{cm}^2,\\ 4.5\\ \\text{cm}^2') + '។ គណនាផ្ទៃក្រឡាចតុកោណ ' + M('PQRS') + '។',
          M('170\\ \\text{cm}^2'),
          [M('180\\ \\text{cm}^2'), M('160\\ \\text{cm}^2'), M('255\\ \\text{cm}^2')],
          'ផលបូកផ្ទៃត្រីកោណទាំងបួន ៖ ' + M('88 + 22.5 + 140 + 4.5 = 255\\ \\text{cm}^2') + '។ ផ្ទៃក្រឡា ' + M('PQRS = 425 - 255 = 170\\ \\text{cm}^2'))

    M_add('hard', 'rhombus_perimeter_area',
          'ចតុកោណស្មើមួយមានបរិមាត្រ ' + M('52\\ \\text{cm}') + ' និងផលធៀបអង្កត់ទ្រូងទាំងពីរគឺ ' + M('\\dfrac{d_1}{d_2} = \\dfrac{12}{5}') + '។ គណនាផ្ទៃក្រឡារបស់វា។',
          M('120\\ \\text{cm}^2'),
          [M('240\\ \\text{cm}^2'), M('60\\ \\text{cm}^2'), M('130\\ \\text{cm}^2')],
          'ជ្រុង ' + M('a = 13\\ \\text{cm}') + '។ តាង ' + M('d_1 = 24x, d_2 = 10x \\Rightarrow (12x)^2 + (5x)^2 = 13^2 \\Rightarrow 13x = 13 \\Rightarrow x = 1') + ' នាំឱ្យ ' + M('S = \\dfrac{24 \\times 10}{2} = 120\\ \\text{cm}^2'))

    M_add('hard', 'trapezoid_area_ratio',
          'ចតុកោណព្នាយ ' + M('ABCD') + ' (' + M('AB \parallel CD') + ') មានបាត ' + M('AB = 4\\ \\text{cm}') + ' និង ' + M('CD = 8\\ \\text{cm}') + '។ អង្កត់ទ្រូងកាត់គ្នាត្រង់ ' + M('O') + '។ តើផលធៀបផ្ទៃក្រឡា ' + M('\\dfrac{S_{\Delta OAB}}{S_{\Delta OCD}}') + ' ស្មើនឹងប៉ុន្មាន?',
          M('\\dfrac{1}{4}'),
          [M('\\dfrac{1}{2}'), M('\\dfrac{1}{8}'), M('\\dfrac{1}{16}')],
          'ត្រីកោណ ' + M('\Delta OAB \sim \Delta OCD') + ' តាមផលធៀបដូច ' + M('k = \\dfrac{AB}{CD} = \\dfrac{4}{8} = \\dfrac{1}{2}') + ' នាំឱ្យផលធៀបផ្ទៃ ' + M('k^2 = \\dfrac{1}{4}'))

    M_add('hard', 'para_area_angle30',
          'ប្រលេឡូក្រាមមួយមានរង្វាស់ជ្រុងជាប់គ្នា ' + M('8\\ \\text{cm}') + ' និង ' + M('10\\ \\text{cm}') + ' ហើយមុំស្រួចមួយមានរង្វាស់ ' + M('30^\circ') + '។ គណនាផ្ទៃក្រឡានៃប្រលេឡូក្រាមនោះ។',
          M('40\\ \\text{cm}^2'),
          [M('80\\ \\text{cm}^2'), M('20\\ \\text{cm}^2'), M('40\sqrt{3}\\ \\text{cm}^2')],
          M('h = 8 \\times \sin 30^\circ = 8 \\times 0.5 = 4\\ \\text{cm} \\Rightarrow S = 10 \\times 4 = 40\\ \\text{cm}^2'))

    M_add('hard', 'equilateral_area_calc',
          'ត្រីកោណសម័ង្សមួយមានរង្វាស់ជ្រុង ' + M('6\\ \\text{cm}') + '។ គណនាផ្ទៃក្រឡារបស់វា។',
          M('9\sqrt{3}\\ \\text{cm}^2'),
          [M('18\sqrt{3}\\ \\text{cm}^2'), M('12\\ \\text{cm}^2'), M('36\sqrt{3}\\ \\text{cm}^2')],
          M('S = \\dfrac{\sqrt{3}}{4} \\times 6^2 = \\dfrac{36\sqrt{3}}{4} = 9\sqrt{3}\\ \\text{cm}^2'))

    M_add('hard', 'regular_hexagon_area',
          'ឆកោណទៀងទាត់មួយមានរង្វាស់ជ្រុង ' + M('4\\ \\text{cm}') + '។ គណនាផ្ទៃក្រឡានៃឆកោណទៀងទាត់នោះ។',
          M('24\sqrt{3}\\ \\text{cm}^2'),
          [M('16\sqrt{3}\\ \\text{cm}^2'), M('48\sqrt{3}\\ \\text{cm}^2'), M('36\\ \\text{cm}^2')],
          'ឆកោណទៀងទាត់ផ្គុំដោយត្រីកោណសម័ង្សចំនួន 6 ៖ ' + M('S = 6 \\times \\left(\\dfrac{\sqrt{3}}{4} \\times 4^2\\right) = 6 \\times 4\sqrt{3} = 24\sqrt{3}\\ \\text{cm}^2'))

    M_add('hard', 'complex_shaded_cutout',
          'បន្ទះដែកមួយរាងចតុកោណកែងទំហំ ' + M('24\\ \\text{cm} \\times 42\\ \\text{cm}') + ' (ផ្ទៃ ' + M('1008\\ \\text{cm}^2') + ')។ គេកាត់ចេញនូវការេជ្រុង ' + M('8\\ \\text{cm}') + ' មួយ និងត្រីកោណកែងជ្រុង ' + M('14\\ \\text{cm} \\times 26\\ \\text{cm}') + ' មួយ។ គណនាផ្ទៃដែកដែលនៅសល់។',
          M('762\\ \\text{cm}^2'),
          [M('826\\ \\text{cm}^2'), M('740\\ \\text{cm}^2'), M('698\\ \\text{cm}^2')],
          M('S = 1008 - 8^2 - \\dfrac{14 \\times 26}{2} = 1008 - 64 - 182 = 762\\ \\text{cm}^2'))

    # ==========================================
    # 4. MCQ PISA (5 target)
    # ==========================================
    M_add('pisa', 'building_glass_facade',
          'ជ្រុងម្ខាងនៃអគាររាងចតុកោណព្នាយមានបាតដី ' + M('400\\ \\text{m}') + ', ដំបូល ' + M('150\\ \\text{m}') + ' និងកម្ពស់ ' + M('500\\ \\text{m}') + '។ បើគេបិទកញ្ចក់ដែលមួយផ្ទាំងមានផ្ទៃ ' + M('1\\ \\text{m}^2') + ' តើត្រូវប្រើកញ្ចក់ប៉ុន្មានផ្ទាំង?',
          M('137\\,500\\ \\text{ផ្ទាំង}'),
          [M('275\\,000\\ \\text{ផ្ទាំង}'), M('135\\,000\\ \\text{ផ្ទាំង}'), M('140\\,000\\ \\text{ផ្ទាំង}')],
          M('S = \\dfrac{(400 + 150) \\times 500}{2} = 550 \\times 250 = 137\\,500\\ \\text{m}^2 \\Rightarrow N = 137\\,500\\ \\text{ផ្ទាំង}'))

    M_add('pisa', 'paving_cost_trap',
          'ផ្លូវចូលផ្ទះរាងចតុកោណព្នាយមានបាតទាំងពីរ ' + M('12\\ \\text{m}') + ' និង ' + M('8\\ \\text{m}') + ' ហើយកម្ពស់ ' + M('15\\ \\text{m}') + '។ បើថ្លៃចាក់បេតុងក្រាលផ្លូវគឺ ' + M('18\$/\\text{m}^2') + ' គណនាថ្លៃចំណាយសរុប។',
          M('2\\,700\$'),
          [M('5\\,400\$'), M('2\\,400\$'), M('3\\,240\$')],
          M('S = \\dfrac{(12 + 8) \\times 15}{2} = 150\\ \\text{m}^2 \\Rightarrow \\text{ថ្លៃ} = 150 \\times 18 = 2\\,700\$'))

    M_add('pisa', 'field_harvest_yield',
          'ស្រែរាងប្រលេឡូក្រាមមួយមានបាត ' + M('120\\ \\text{m}') + ' និងកម្ពស់ ' + M('75\\ \\text{m}') + '។ បើទិន្នផលស្រូវជាមធ្យមទទួលបាន ' + M('5.5\\ \\text{តោន/ហិកតា}') + ' គណនាបរិមាណស្រូវប្រមូលផលបានពីស្រែនេះ។',
          M('4.95\\ \\text{តោន}'),
          [M('9.9\\ \\text{តោន}'), M('49.5\\ \\text{តោន}'), M('5.5\\ \\text{តោន}')],
          M('S = 120 \\times 75 = 9\\,000\\ \\text{m}^2 = 0.9\\ \\text{ha} \\Rightarrow \\text{ផល} = 0.9 \\times 5.5 = 4.95\\ \\text{តោន}'))

    M_add('pisa', 'kite_paper_wastage',
          'ខ្លែងមួយរាងចតុកោណខ្លែងមានអង្កត់ទ្រូង ' + M('50\\ \\text{cm}') + ' និង ' + M('30\\ \\text{cm}') + '។ ដោយសារការកាត់គែមបិទភ្ជាប់ គេត្រូវប្រើក្រដាសលើសផ្ទៃខ្លែង ' + M('20\%') + '។ គណនាផ្ទៃក្រដាសដែលត្រូវប្រើ។',
          M('900\\ \\text{cm}^2'),
          [M('750\\ \\text{cm}^2'), M('850\\ \\text{cm}^2'), M('1\\,000\\ \\text{cm}^2')],
          M('S = \\dfrac{50 \\times 30}{2} = 750\\ \\text{cm}^2 \\Rightarrow S_{\\text{ក្រដាស}} = 750 \\times 1.20 = 900\\ \\text{cm}^2'))

    M_add('pisa', 'solar_panel_roof',
          'ដំបូលរោងចក្ររាងចតុកោណព្នាយមានបាត ' + M('10\\ \\text{m}') + ' និង ' + M('6\\ \\text{m}') + ' កម្ពស់ ' + M('4\\ \\text{m}') + '។ គេចង់ដំឡើងផ្ទាំងសូឡាទំហំ ' + M('1.6\\ \\text{m}^2') + ' លើផ្ទៃដំបូល ' + M('80\%') + '។ តើដំឡើងបានប៉ុន្មានផ្ទាំង?',
          M('16\\ \\text{ផ្ទាំង}'),
          [M('20\\ \\text{ផ្ទាំង}'), M('12\\ \\text{ផ្ទាំង}'), M('25\\ \\text{ផ្ទាំង}')],
          M('S = \\dfrac{(10 + 6) \\times 4}{2} = 32\\ \\text{m}^2') + '; ផ្ទៃសូឡា ៖ ' + M('32 \\times 0.8 = 25.6\\ \\text{m}^2 \\Rightarrow N = \\dfrac{25.6}{1.6} = 16\\ \\text{ផ្ទាំង}'))

    # ==========================================
    # 5. WRITING EASY (1 target, 5 pts total)
    # ==========================================
    W('easy', 'wr_para_proof_area',
      'ប្រលេឡូក្រាម ' + M('ABCD') + ' មួយមានបាត ' + M('b = 14\\ \\text{cm}') + ' និងកម្ពស់ត្រូវគ្នា ' + M('h = 8\\ \\text{cm}') + '។\n'
      'ក. សរសេររូបមន្តគណនាផ្ទៃក្រឡាប្រលេឡូក្រាម។\n'
      'ខ. គណនាផ្ទៃក្រឡានៃប្រលេឡូក្រាមនោះ។\n'
      'គ. បញ្ជាក់ខ្នាតនៃផ្ទៃក្រឡាឱ្យបានត្រឹមត្រូវ។', [
          ('ក. រូបមន្តផ្ទៃក្រឡាប្រលេឡូក្រាម ៖ ' + M('S = b \\times h'), 2),
          ('ខ. ជំនួសតម្លៃ ៖ ' + M('S = 14 \\times 8 = 112'), 2),
          ('គ. ខ្នាតផ្ទៃក្រឡាគឺ សង់ទីម៉ែត្រការេ (' + M('\\text{cm}^2') + ') ដូចនេះ ' + M('S = 112\\ \\text{cm}^2'), 1)], FIG_AREA_PARALLELOGRAM)

    # ==========================================
    # 6. WRITING MEDIUM (4 target, 5 pts total each)
    # ==========================================
    W('medium', 'wr_trap_two_triangles',
      'បង្ហាញរូបមន្តផ្ទៃក្រឡាចតុកោណព្នាយ ' + M('ABCD') + ' (' + M('AB \parallel CD') + ') ដែលមានបាត ' + M('AB = a') + ', ' + M('CD = b') + ' និងកម្ពស់ ' + M('h') + '។\n'
      'ក. គូសអង្កត់ទ្រូង ' + M('AC') + ' បំបែកចតុកោណព្នាយជាត្រីកោណពីរណាខ្លះ?\n'
      'ខ. គណនាផ្ទៃក្រឡានៃត្រីកោណទាំងពីរនោះជាអនុគមន៍នៃ ' + M('a, b, h') + '។\n'
      'គ. ទាញរកផ្ទៃក្រឡាចតុកោណព្នាយ ' + M('S = \\dfrac{(a + b)h}{2}') + '។', [
          ('ក. អង្កត់ទ្រូង ' + M('AC') + ' បំបែកចតុកោណព្នាយជាត្រីកោណពីរគឺ ' + M('\Delta ABC') + ' និង ' + M('\Delta ADC'), 1),
          ('ខ. ផ្ទៃ ' + M('S_{\Delta ADC} = \\dfrac{b \\times h}{2}') + ' និងផ្ទៃ ' + M('S_{\Delta ABC} = \\dfrac{a \\times h}{2}'), 2),
          ('គ. ផ្ទៃសរុប ' + M('S = S_{\Delta ADC} + S_{\Delta ABC} = \\dfrac{bh}{2} + \\dfrac{ah}{2} = \\dfrac{(a + b)h}{2}'), 2)], FIG_AREA_TRAPEZOID)

    W('medium', 'wr_rhombus_diag_calc',
      'ចតុកោណស្មើ ' + M('ABCD') + ' មានអង្កត់ទ្រូងកាត់គ្នាកែងត្រង់ ' + M('O') + ' ដោយ ' + M('AC = 18\\ \\text{cm}') + ' និង ' + M('BD = 12\\ \\text{cm}') + '។\n'
      'ក. សរសេររូបមន្ត និងគណនាផ្ទៃក្រឡានៃចតុកោណស្មើ។\n'
      'ខ. គណនាប្រវែងកន្លះអង្កត់ទ្រូង ' + M('OA') + ' និង ' + M('OB') + '។\n'
      'គ. គណនាប្រវែងជ្រុង ' + M('AB') + ' និងបរិមាត្រ ' + M('P') + ' ជាទម្រង់រ៉ាឌីកាល់សម្រួល។', [
          ('ក. រូបមន្ត ៖ ' + M('S = \\dfrac{d_1 \\times d_2}{2} = \\dfrac{18 \\times 12}{2} = 108\\ \\text{cm}^2'), 2),
          ('ខ. កន្លះអង្កត់ទ្រូង ៖ ' + M('OA = \\dfrac{18}{2} = 9\\ \\text{cm}') + ' និង ' + M('OB = \\dfrac{12}{2} = 6\\ \\text{cm}'), 1),
          ('គ. ជ្រុង ' + M('AB = \sqrt{9^2 + 6^2} = \sqrt{81 + 36} = \sqrt{117} = 3\sqrt{13}\\ \\text{cm}') + ' នាំឱ្យបរិមាត្រ ' + M('P = 4 \\times 3\sqrt{13} = 12\sqrt{13}\\ \\text{cm}'), 2)], FIG_AREA_RHOMBUS)

    W('medium', 'wr_para_two_alt',
      'ប្រលេឡូក្រាម ' + M('ABCD') + ' មានជ្រុង ' + M('AB = 20\\ \\text{cm}') + ' និង ' + M('AD = 12\\ \\text{cm}') + '។ កម្ពស់ត្រូវនឹងបាត ' + M('AB') + ' គឺ ' + M('h_1 = 9\\ \\text{cm}') + '។\n'
      'ក. គណនាផ្ទៃក្រឡានៃប្រលេឡូក្រាម ' + M('ABCD') + '។\n'
      'ខ. សរសេរសមីការទំនាក់ទំនងផ្ទៃក្រឡាធៀបនឹងបាត ' + M('AD') + ' និងកម្ពស់ ' + M('h_2') + '។\n'
      'គ. គណនាកម្ពស់ ' + M('h_2') + ' ត្រូវនឹងបាត ' + M('AD') + '។', [
          ('ក. ផ្ទៃក្រឡា ៖ ' + M('S = AB \\times h_1 = 20 \\times 9 = 180\\ \\text{cm}^2'), 2),
          ('ខ. សមីការ ៖ ' + M('S = AD \\times h_2 \\Rightarrow 180 = 12 \\times h_2'), 1),
          ('គ. ទាញបាន ' + M('h_2 = \\dfrac{180}{12} = 15\\ \\text{cm}'), 2)])

    W('medium', 'wr_right_trap_calc',
      'ចតុកោណព្នាយកែង ' + M('ABCD') + ' (' + M('\angle A = \angle D = 90^\circ') + ') មានបាតតូច ' + M('AB = 8\\ \\text{cm}') + ', បាតធំ ' + M('CD = 14\\ \\text{cm}') + ' និងជ្រុងទ្រេត ' + M('BC = 10\\ \\text{cm}') + '។\n'
      'ក. គូសកម្ពស់ ' + M('BH \perp CD') + ' រួចគណនាប្រវែងកំណាត់ ' + M('HC') + '។\n'
      'ខ. គណនាកម្ពស់ ' + M('h = BH') + '។\n'
      'គ. គណនាផ្ទៃក្រឡានៃចតុកោណព្នាយកែង ' + M('ABCD') + '។', [
          ('ក. ដោយ ' + M('ABHD') + ' ជាចតុកោណកែង នោះ ' + M('DH = AB = 8\\ \\text{cm} \\Rightarrow HC = CD - DH = 14 - 8 = 6\\ \\text{cm}'), 1),
          ('ខ. ក្នុងត្រីកោណកែង ' + M('BHC') + ' ៖ ' + M('BH = \sqrt{BC^2 - HC^2} = \sqrt{10^2 - 6^2} = 8\\ \\text{cm}'), 2),
          ('គ. ផ្ទៃក្រឡា ៖ ' + M('S = \\dfrac{(AB + CD) \\times BH}{2} = \\dfrac{(8 + 14) \\times 8}{2} = 88\\ \\text{cm}^2'), 2)])

    # ==========================================
    # 7. WRITING HARD (4 target, 5 pts total each)
    # ==========================================
    W('hard', 'wr_iso_trap_complete',
      'ចតុកោណព្នាយសមបាត ' + M('ABCD') + ' មានបាតតូច ' + M('AB = 14\\ \\text{cm}') + ', បាតធំ ' + M('CD = 30\\ \\text{cm}') + ' និងជ្រុងទ្រេត ' + M('AD = BC = 17\\ \\text{cm}') + '។\n'
      'ក. គណនាប្រវែងចំណោលកែង ' + M('x') + ' នៃជ្រុងទ្រេតលើបាតធំ។\n'
      'ខ. គណនាកម្ពស់ ' + M('h') + ' នៃចតុកោណព្នាយ។\n'
      'គ. គណនាផ្ទៃក្រឡា និងបរិមាត្រនៃចតុកោណព្នាយ។', [
          ('ក. ចំណោលកែង ៖ ' + M('x = \\dfrac{CD - AB}{2} = \\dfrac{30 - 14}{2} = 8\\ \\text{cm}'), 1),
          ('ខ. តាមពីតាក័រ ៖ ' + M('h = \sqrt{17^2 - 8^2} = \sqrt{289 - 64} = \sqrt{225} = 15\\ \\text{cm}'), 2),
          ('គ. ផ្ទៃ ៖ ' + M('S = \\dfrac{(14 + 30) \\times 15}{2} = 330\\ \\text{cm}^2') + '; បរិមាត្រ ៖ ' + M('P = 14 + 30 + 2(17) = 78\\ \\text{cm}'), 2)])

    W('hard', 'wr_shaded_subtraction',
      'ចតុកោណកែងធំ ' + M('ABCD') + ' មួយមានវិមាត្រ ' + M('25\\ \\text{cm} \\times 17\\ \\text{cm}') + '។ ចំណុច ' + M('P, Q, R, S') + ' ស្ថិតនៅលើជ្រុងទាំងបួន បង្កើតបានចតុកោណ ' + M('PQRS') + ' និងត្រីកោណកែង 4 នៅជ្រុងទាំងបួនដែលមានផ្ទៃរៀងគ្នា ' + M('S_1 = 88\\ \\text{cm}^2') + ', ' + M('S_2 = 22.5\\ \\text{cm}^2') + ', ' + M('S_3 = 140\\ \\text{cm}^2') + ' និង ' + M('S_4 = 4.5\\ \\text{cm}^2') + '។\n'
      'ក. គណនាផ្ទៃក្រឡាសរុបនៃចតុកោណកែង ' + M('ABCD') + '។\n'
      'ខ. គណនាផលបូកផ្ទៃក្រឡានៃត្រីកោណកែងទាំងបួន។\n'
      'គ. ទាញរកផ្ទៃក្រឡានៃចតុកោណ ' + M('PQRS') + '។', [
          ('ក. ផ្ទៃក្រឡាចតុកោណកែង ៖ ' + M('S_{\\text{ធំ}} = 25 \\times 17 = 425\\ \\text{cm}^2'), 1),
          ('ខ. ផលបូកផ្ទៃត្រីកោណទាំងបួន ៖ ' + M('S_{\\text{បួន}} = 88 + 22.5 + 140 + 4.5 = 255\\ \\text{cm}^2'), 2),
          ('គ. ផ្ទៃក្រឡាចតុកោណ ' + M('PQRS = S_{\\text{ធំ}} - S_{\\text{បួន}} = 425 - 255 = 170\\ \\text{cm}^2'), 2)])

    W('hard', 'wr_kite_area_proof',
      'ចតុកោណខ្លែង ' + M('ABCD') + ' មានអង្កត់ទ្រូងពីរកាត់គ្នាកែងត្រង់ ' + M('O') + ' (' + M('AC \perp BD') + ')។\n'
      'ក. បង្ហាញថាអង្កត់ទ្រូង ' + M('AC') + ' ចែកចតុកោណខ្លែងជាត្រីកោណពីរ ' + M('\Delta ABC') + ' និង ' + M('\Delta ADC') + ' ដែលមានបាតរួម ' + M('AC') + '។\n'
      'ខ. សរសេរកន្សោមផ្ទៃក្រឡានៃត្រីកោណទាំងពីរជាអនុគមន៍នៃ ' + M('AC, OB') + ' និង ' + M('OD') + '។\n'
      'គ. បង្ហាញថាផ្ទៃក្រឡាចតុកោណខ្លែងគឺ ' + M('S = \\dfrac{AC \\times BD}{2}') + '។', [
          ('ក. អង្កត់ទ្រូង ' + M('AC') + ' ចែកចតុកោណជា ' + M('\Delta ABC') + ' និង ' + M('\Delta ADC') + ' ដែលមានបាតរួម ' + M('AC') + ' និងកម្ពស់រៀងគ្នា ' + M('OB, OD') + ' (ព្រោះ ' + M('BD \perp AC') + ')', 2),
          ('ខ. ' + M('S_{ABC} = \\dfrac{1}{2} AC \\times OB') + ' និង ' + M('S_{ADC} = \\dfrac{1}{2} AC \\times OD'), 1),
          ('គ. ' + M('S = S_{ABC} + S_{ADC} = \\dfrac{1}{2} AC (OB + OD) = \\dfrac{1}{2} AC \\times BD = \\dfrac{AC \\times BD}{2}'), 2)])

    W('hard', 'wr_composite_polygon_l',
      'ដីឡូត៍មួយមានរាងអក្សរ L ដែលមានវិមាត្រខាងក្រៅ ៖ បណ្តោយសរុប ' + M('21\\ \\text{m}') + ', ទទឹងសរុប ' + M('15\\ \\text{m}') + '។ គេអាចបំបែកដីនេះជាចតុកោណកែងពីរ ៖ ចតុកោណកែងទី១ ទំហំ ' + M('9\\ \\text{m} \\times 15\\ \\text{m}') + ' និងចតុកោណកែងទី២ ទំហំ ' + M('12\\ \\text{m} \\times 9\\ \\text{m}') + '។\n'
      'ក. គណនាផ្ទៃក្រឡានៃចតុកោណកែងនីមួយៗ។\n'
      'ខ. គណនាផ្ទៃក្រឡាសរុបនៃដីឡូត៍នោះ។\n'
      'គ. គណនាបរិមាត្រជុំវិញនៃដីឡូត៍ (ដឹងថាជ្រុងទាំង 6 មានប្រវែង ' + M('21\\ \\text{m}, 15\\ \\text{m}, 9\\ \\text{m}, 6\\ \\text{m}, 12\\ \\text{m}, 9\\ \\text{m}') + ')។', [
          ('ក. ផ្ទៃទី១ ៖ ' + M('S_1 = 9 \\times 15 = 135\\ \\text{m}^2') + '; ផ្ទៃទី២ ៖ ' + M('S_2 = 12 \\times 9 = 108\\ \\text{m}^2'), 2),
          ('ខ. ផ្ទៃសរុប ៖ ' + M('S = S_1 + S_2 = 135 + 108 = 243\\ \\text{m}^2'), 1),
          ('គ. បរិមាត្រ ៖ ' + M('P = 21 + 15 + 9 + 6 + 12 + 9 = 72\\ \\text{m}'), 2)])

    # ==========================================
    # 8. WRITING PISA (5 target, 5 pts total each)
    # ==========================================
    W('pisa', 'wr_pisa_rubber_ha',
      'ចម្ការកៅស៊ូមួយកន្លែងរាងចតុកោណកែងមានបណ្តោយប្រវែង ' + M('5\\ \\text{km}') + ' និងទទឹងប្រវែង ' + M('2.3\\ \\text{km}') + '។\n'
      'ក. គណនាផ្ទៃក្រឡាចម្ការគិតជាគីឡូម៉ែត្រការេ (' + M('\\text{km}^2') + ')។\n'
      'ខ. បំលែងផ្ទៃក្រឡានោះទៅជាហិកតា (' + M('\\text{ha}') + ') ដោយដឹងថា ' + M('1\\ \\text{km}^2 = 100\\ \\text{ha}') + '។\n'
      'គ. បើចម្ការនេះអាចទាញយកជ័រកៅស៊ូជាមធ្យម ' + M('1.8\\ \\text{តោន/ហិកតា}') + ' ក្នុងមួយឆ្នាំ គណនាទិន្នផលជ័រប្រចាំឆ្នាំសរុប។', [
          ('ក. ផ្ទៃក្រឡាជាគីឡូម៉ែត្រការេ ៖ ' + M('S = 5\\ \\text{km} \\times 2.3\\ \\text{km} = 11.5\\ \\text{km}^2'), 2),
          ('ខ. បំលែងជាហិកតា ៖ ' + M('S = 11.5 \\times 100 = 1150\\ \\text{ha}'), 2),
          ('គ. ទិន្នផលប្រចាំឆ្នាំសរុប ៖ ' + M('1150 \\times 1.8 = 2070\\ \\text{តោន}'), 1)])

    W('pisa', 'wr_pisa_rose_garden',
      'សួនច្បារផ្កាកុលាបមួយរាងត្រីកោណមានបាត ' + M('5\\ \\text{m}') + ' និងកម្ពស់ ' + M('3\\ \\text{m}') + '។\n'
      'ក. គណនាផ្ទៃក្រឡាសួនច្បាររាងត្រីកោណនេះ។\n'
      'ខ. បើគេដាំផ្កាកុលាប ១ ដើម ត្រូវការផ្ទៃដី ' + M('0.5\\ \\text{m}^2') + ' តើគេអាចដាំផ្កាកុលាបបានប៉ុន្មានដើមក្នុងសួននេះ?\n'
      'គ. បើកូនផ្កាកុលាបមួយដើមថ្លៃ ' + M('2.50\$') + ' គណនាថ្លៃទិញកូនផ្កាទាំងអស់សម្រាប់ដាំក្នុងសួន។', [
          ('ក. ផ្ទៃក្រឡាសួនច្បារ ៖ ' + M('S = \\dfrac{1}{2} \\times 5 \\times 3 = 7.5\\ \\text{m}^2'), 2),
          ('ខ. ចំនួនដើមផ្កាកុលាបដែលអាចដាំបាន ៖ ' + M('N = \\dfrac{7.5\\ \\text{m}^2}{0.5\\ \\text{m}^2} = 15\\ \\text{ដើម}'), 2),
          ('គ. ថ្លៃទិញកូនផ្កាសរុប ៖ ' + M('15 \\times 2.50 = 37.50\$'), 1)])

    W('pisa', 'wr_pisa_building_glass',
      'ជ្រុងម្ខាងនៃអគាររាងចតុកោណព្នាយមួយមានបាតក្រោមប្រវែង ' + M('400\\ \\text{m}') + ', បាតលើ (ដំបូល) ប្រវែង ' + M('150\\ \\text{m}') + ' និងកម្ពស់ប្រវែង ' + M('500\\ \\text{m}') + '។\n'
      'ក. គណនាផ្ទៃក្រឡាជញ្ជាំងជ្រុងអគារនោះ។\n'
      'ខ. បើគេបិទកញ្ចក់ការពារកម្តៅថ្ងៃដែលមួយផ្ទាំងមានផ្ទៃ ' + M('1\\ \\text{m}^2') + ' តើត្រូវប្រើកញ្ចក់អស់ប៉ុន្មានផ្ទាំង?\n'
      'គ. បើតម្លៃកញ្ចក់រួមទាំងថ្លៃដំឡើងគឺ ' + M('45\$/\\text{m}^2') + ' គណនាថវិកាសរុបដែលត្រូវចំណាយ។', [
          ('ក. ផ្ទៃក្រឡាជញ្ជាំងអគារ ៖ ' + M('S = \\dfrac{(400 + 150) \\times 500}{2} = \\dfrac{550 \\times 500}{2} = 137\\,500\\ \\text{m}^2'), 2),
          ('ខ. ចំនួនផ្ទាំងកញ្ចក់ដែលត្រូវប្រើ ៖ ' + M('N = \\dfrac{137\\,500\\ \\text{m}^2}{1\\ \\text{m}^2} = 137\\,500\\ \\text{ផ្ទាំង}'), 1),
          ('គ. ថវិកាសរុប ៖ ' + M('137\\,500 \\times 45 = 6\\,187\\,500\$'), 2)])

    W('pisa', 'wr_pisa_roof_tiles',
      'ដំបូលរោងចក្រមួយផ្នែកមានរាងចតុកោណព្នាយសមបាតមានបាតក្រោម ' + M('16\\ \\text{m}') + ', បាតលើ ' + M('10\\ \\text{m}') + ' និងកម្ពស់ជម្រាល ' + M('6\\ \\text{m}') + '។\n'
      'ក. គណនាផ្ទៃក្រឡានៃផ្នែកដំបូលនោះមួយផ្ទាំង។\n'
      'ខ. បើដំបូលនោះមាន ២ ផ្ទាំងដូចគ្នា គណនាផ្ទៃក្រឡាដំបូលសរុប។\n'
      'គ. បើ ១ ម៉ែត្រការេត្រូវប្រើក្បឿង ១២ សន្លឹក ហើយគេត្រូវទិញបន្ថែម ' + M('5\%') + ' សម្រាប់កាត់គែមនិងបាក់បែក តើត្រូវទិញក្បឿងសរុបប៉ុន្មានសន្លឹក?', [
          ('ក. ផ្ទៃមួយផ្ទាំង ៖ ' + M('S_1 = \\dfrac{(16 + 10) \\times 6}{2} = \\dfrac{26 \\times 6}{2} = 78\\ \\text{m}^2'), 2),
          ('ខ. ផ្ទៃសរុប ២ ផ្ទាំង ៖ ' + M('S = 78 \\times 2 = 156\\ \\text{m}^2'), 1),
          ('គ. ចំនួនក្បឿងត្រូវការ ៖ ' + M('156 \\times 12 = 1872\\ \\text{សន្លឹក}') + '។ ទិញបន្ថែម ' + M('5\%') + ' ៖ ' + M('1872 \\times 1.05 = 1965.6 \approx 1966\\ \\text{សន្លឹក}'), 2)])

    W('pisa', 'wr_pisa_field_division',
      'ដីស្រែរាងចតុកោណព្នាយ ' + M('ABCD') + ' (' + M('AB \parallel CD') + ') មានបាត ' + M('AB = 40\\ \\text{m}') + ', ' + M('CD = 80\\ \\text{m}') + ' និងកម្ពស់ ' + M('30\\ \\text{m}') + '។\n'
      'ក. គណនាផ្ទៃក្រឡាដីស្រែសរុប។\n'
      'ខ. ម្ចាស់ដីចែកដីជាពីរចំណែកដោយគូសបន្ទាត់ស្រប ' + M('BE \parallel AD') + ' (' + M('E \in CD') + ') បង្កើតបានប្រលេឡូក្រាម ' + M('ABED') + ' និងត្រីកោណ ' + M('BCE') + '។ គណនាផ្ទៃក្រឡាចំណែកនីមួយៗ។\n'
      'គ. ផ្ទៀងផ្ទាត់ផលបូកផ្ទៃក្រឡាទាំងពីរធៀបនឹងផ្ទៃសរុប។', [
          ('ក. ផ្ទៃស្រែសរុប ៖ ' + M('S = \\dfrac{(40 + 80) \\times 30}{2} = \\dfrac{120 \\times 30}{2} = 1800\\ \\text{m}^2'), 2),
          ('ខ. ' + M('ED = AB = 40\\ \\text{m} \\Rightarrow EC = 80 - 40 = 40\\ \\text{m}') + '។ ផ្ទៃប្រលេឡូក្រាម ' + M('S_1 = 40 \\times 30 = 1200\\ \\text{m}^2') + '; ផ្ទៃត្រីកោណ ' + M('S_2 = \\dfrac{40 \\times 30}{2} = 600\\ \\text{m}^2'), 2),
          ('គ. ផ្ទៀងផ្ទាត់ ៖ ' + M('S_1 + S_2 = 1200 + 600 = 1800\\ \\text{m}^2 = S') + ' (ត្រឹមត្រូវ)', 1)])

    return C
