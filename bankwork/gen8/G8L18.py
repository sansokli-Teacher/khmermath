"""Bank candidates for Grade 8, Lesson 18: រូបធរណីមាត្រមានវិមាត្របី (Three-Dimensional Geometric Figures)
Covers MoEYS Grade 8 curriculum:
  1. ព្រីស (Prisms: lateral area S_L = p * h, total area S_T = S_L + 2 S_B, volume V = S_B * h)
  2. ពីរ៉ាមីត (Pyramids: lateral area S_L = 1/2 p * a, total area S_T = S_L + S_B, volume V = 1/3 S_B * h)
  3. កោន (Cones: generator l = sqrt(r^2 + h^2), S_L = pi * r * l, S_T = pi * r(l + r), V = 1/3 pi * r^2 * h)
  4. ស៊ីឡាំង និងគូប (Cylinders & Cubes: S_L = 2 pi r h, V = pi r^2 h; V = a^3)
  5. ការអនុវត្តជាក់ស្តែង & PISA (Water tanks, party hats, tents, silos, gift boxes, ice cream cones)

Images: Clean vector illustrations, isolated, no background, flat educational textbook style.
Geometry labels use font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic'.
"""
from lib import *

LESSON = "រូបធរណីមាត្រមានវិមាត្របី"

# --- SVG Illustrations ---

# 1. FIG_PRISM_TRIANGULAR: Right triangular prism with height h and base edges
FIG_PRISM_TRIANGULAR = (
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 260 200' width='260' height='200'>\n"
    "  <!-- Bottom base ABC -->\n"
    "  <polygon points='50,160 170,180 120,135' fill='#eff6ff' stroke='#0284c7' stroke-width='1.5'/>\n"
    "  <!-- Top base DEF -->\n"
    "  <polygon points='50,60 170,80 120,35' fill='#e0f2fe' stroke='#0284c7' stroke-width='1.8'/>\n"
    "  <!-- Vertical edges -->\n"
    "  <line x1='50' y1='60' x2='50' y2='160' stroke='#0284c7' stroke-width='1.8'/>\n"
    "  <line x1='170' y1='80' x2='170' y2='180' stroke='#0284c7' stroke-width='1.8'/>\n"
    "  <!-- Back vertical edge (dashed) -->\n"
    "  <line x1='120' y1='35' x2='120' y2='135' stroke='#94a3b8' stroke-width='1.5' stroke-dasharray='4,3'/>\n"
    "  <!-- Back bottom edges (dashed) -->\n"
    "  <line x1='50' y1='160' x2='120' y2='135' stroke='#94a3b8' stroke-width='1.5' stroke-dasharray='4,3'/>\n"
    "  <line x1='170' y1='180' x2='120' y2='135' stroke='#94a3b8' stroke-width='1.5' stroke-dasharray='4,3'/>\n"
    "  <!-- Height indicator h -->\n"
    "  <line x1='38' y1='60' x2='38' y2='160' stroke='#dc2626' stroke-width='1.2' stroke-dasharray='3,2'/>\n"
    "  <text x='28' y='115' text-anchor='end' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#dc2626'>h</text>\n"
    "  <!-- Labels -->\n"
    "  <text x='42' y='52' text-anchor='end' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='13' fill='#0f172a'>D</text>\n"
    "  <text x='180' y='80' text-anchor='start' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='13' fill='#0f172a'>E</text>\n"
    "  <text x='120' y='26' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='13' fill='#0f172a'>F</text>\n"
    "  <text x='42' y='172' text-anchor='end' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='13' fill='#0f172a'>A</text>\n"
    "  <text x='180' y='190' text-anchor='start' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='13' fill='#0f172a'>B</text>\n"
    "</svg>"
)

# 2. FIG_PYRAMID_SQUARE: Regular square pyramid S.ABCD with altitude SO and apothem SM
FIG_PYRAMID_SQUARE = (
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 260 210' width='260' height='210'>\n"
    "  <!-- Base ABCD in perspective: A(40, 160), B(160, 180), C(220, 140), D(100, 120) -->\n"
    "  <polygon points='40,160 160,180 220,140' fill='#f8fafc' stroke='#334155' stroke-width='1.8'/>\n"
    "  <line x1='40' y1='160' x2='100' y2='120' stroke='#94a3b8' stroke-width='1.5' stroke-dasharray='4,3'/>\n"
    "  <line x1='220' y1='140' x2='100' y2='120' stroke='#94a3b8' stroke-width='1.5' stroke-dasharray='4,3'/>\n"
    "  <!-- Base center O(130, 150) -->\n"
    "  <circle cx='130' cy='150' r='2.5' fill='#dc2626'/>\n"
    "  <!-- Apex S(130, 30) -->\n"
    "  <line x1='130' y1='30' x2='40' y2='160' stroke='#334155' stroke-width='1.8'/>\n"
    "  <line x1='130' y1='30' x2='160' y2='180' stroke='#334155' stroke-width='1.8'/>\n"
    "  <line x1='130' y1='30' x2='220' y2='140' stroke='#334155' stroke-width='1.8'/>\n"
    "  <line x1='130' y1='30' x2='100' y2='120' stroke='#94a3b8' stroke-width='1.5' stroke-dasharray='4,3'/>\n"
    "  <!-- Altitude SO (dashed) -->\n"
    "  <line x1='130' y1='30' x2='130' y2='150' stroke='#dc2626' stroke-width='1.5' stroke-dasharray='3,2'/>\n"
    "  <!-- Apothem SM to BC midpoint M(190, 160) -->\n"
    "  <line x1='130' y1='30' x2='190' y2='160' stroke='#16a34a' stroke-width='1.8'/>\n"
    "  <!-- Labels (Mathcad italic) -->\n"
    "  <text x='130' y='22' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>S</text>\n"
    "  <text x='30' y='168' text-anchor='end' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='13' fill='#0f172a'>A</text>\n"
    "  <text x='162' y='196' text-anchor='start' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='13' fill='#0f172a'>B</text>\n"
    "  <text x='228' y='145' text-anchor='start' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='13' fill='#0f172a'>C</text>\n"
    "  <text x='92' y='115' text-anchor='end' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='13' fill='#0f172a'>D</text>\n"
    "  <text x='122' y='100' text-anchor='end' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='13' fill='#dc2626'>h</text>\n"
    "  <text x='168' y='95' text-anchor='start' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='13' fill='#16a34a'>a</text>\n"
    "</svg>"
)

# 3. FIG_CONE_ELEMENTS: Right circular cone with vertex S, radius r, height h, generator l
FIG_CONE_ELEMENTS = (
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 240 210' width='240' height='210'>\n"
    "  <!-- Base ellipse: cx=120, cy=165, rx=70, ry=22 -->\n"
    "  <path d='M 50,165 A 70 22 0 0 0 190,165' fill='none' stroke='#0284c7' stroke-width='2'/>\n"
    "  <path d='M 50,165 A 70 22 0 0 1 190,165' fill='none' stroke='#94a3b8' stroke-width='1.5' stroke-dasharray='4,3'/>\n"
    "  <!-- Apex S(120, 30) -->\n"
    "  <line x1='120' y1='30' x2='50' y2='165' stroke='#0284c7' stroke-width='2'/>\n"
    "  <line x1='120' y1='30' x2='190' y2='165' stroke='#0284c7' stroke-width='2'/>\n"
    "  <!-- Altitude SO (dashed) -->\n"
    "  <line x1='120' y1='30' x2='120' y2='165' stroke='#dc2626' stroke-width='1.5' stroke-dasharray='3,2'/>\n"
    "  <!-- Radius OA (dashed) -->\n"
    "  <line x1='120' y1='165' x2='190' y2='165' stroke='#16a34a' stroke-width='1.5' stroke-dasharray='3,2'/>\n"
    "  <!-- Center O -->\n"
    "  <circle cx='120' cy='165' r='3' fill='#dc2626'/>\n"
    "  <!-- Right angle marker at O -->\n"
    "  <path d='M 120,155 L 130,155 L 130,165' fill='none' stroke='#dc2626' stroke-width='1.2'/>\n"
    "  <!-- Labels (Mathcad italic) -->\n"
    "  <text x='120' y='22' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>S</text>\n"
    "  <text x='112' y='178' text-anchor='end' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='13' fill='#dc2626'>O</text>\n"
    "  <text x='198' y='172' text-anchor='start' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='13' fill='#0f172a'>A</text>\n"
    "  <text x='112' y='100' text-anchor='end' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='13' fill='#dc2626'>h</text>\n"
    "  <text x='155' y='160' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='13' fill='#16a34a'>r</text>\n"
    "  <text x='165' y='95' text-anchor='start' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='13' fill='#0284c7'>l</text>\n"
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
    M_add('easy', 'prism_lat_area_formula',
          'តើរូបមន្តសម្រាប់គណនាផ្ទៃក្រឡាខាងនៃព្រីសត្រង់ដែលមានបរិមាត្របាត ' + M('p') + ' និងកម្ពស់ ' + M('h') + ' ណាត្រឹមត្រូវ?',
          M('S_L = p \\times h'),
          [M('S_L = \\dfrac{p \\times h}{2}'), M('S_L = p + h'), M('S_L = S_B \\times h')],
          'ផ្ទៃក្រឡាខាងនៃព្រីសត្រង់ស្មើបរិមាត្របាតគុណនឹងកម្ពស់ ៖ ' + M('S_L = p \\times h'),
          FIG_PRISM_TRIANGULAR)

    M_add('easy', 'prism_volume_formula',
          'តើរូបមន្តសម្រាប់គណនាមាឌនៃព្រីសដែលមានផ្ទៃបាត ' + M('S_B') + ' និងកម្ពស់ ' + M('h') + ' ណាត្រឹមត្រូវ?',
          M('V = S_B \\times h'),
          [M('V = \\dfrac{1}{3} S_B \\times h'), M('V = \\dfrac{1}{2} S_B \\times h'), M('V = S_B + h')],
          'មាឌព្រីសស្មើផ្ទៃបាតគុណនឹងកម្ពស់ ៖ ' + M('V = S_B \\times h'))

    M_add('easy', 'pyramid_volume_formula',
          'តើរូបមន្តសម្រាប់គណនាមាឌនៃពីរ៉ាមីតដែលមានផ្ទៃបាត ' + M('S_B') + ' និងកម្ពស់ ' + M('h') + ' ណាត្រឹមត្រូវ?',
          M('V = \\dfrac{1}{3} S_B \\times h'),
          [M('V = S_B \\times h'), M('V = \\dfrac{1}{2} S_B \\times h'), M('V = 3 S_B \\times h')],
          'មាឌពីរ៉ាមីតស្មើមួយភាគបីនៃផ្ទៃបាតគុណនឹងកម្ពស់ ៖ ' + M('V = \\dfrac{1}{3} S_B \\times h'),
          FIG_PYRAMID_SQUARE)

    M_add('easy', 'pyramid_lat_area_formula',
          'តើរូបមន្តសម្រាប់គណនាផ្ទៃក្រឡាខាងនៃពីរ៉ាមីតទៀងទាត់ដែលមានបរិមាត្របាត ' + M('p') + ' និងអាប៉ូតែម ' + M('a') + ' ណាត្រឹមត្រូវ?',
          M('S_L = \\dfrac{1}{2} p \\times a'),
          [M('S_L = p \\times a'), M('S_L = \\dfrac{1}{3} p \\times a'), M('S_L = 2 p \\times a')],
          'ផ្ទៃក្រឡាខាងនៃពីរ៉ាមីតទៀងទាត់ស្មើកន្លះបរិមាត្របាតគុណនឹងអាប៉ូតែម ៖ ' + M('S_L = \\dfrac{1}{2} p \\times a'))

    M_add('easy', 'cone_lat_area_formula',
          'តើរូបមន្តគណនាផ្ទៃក្រឡាខាងនៃកោនដែលមានកាំបាត ' + M('r') + ' និងប្រវែងជននី ' + M('l') + ' ណាត្រឹមត្រូវ?',
          M('S_L = \pi r l'),
          [M('S_L = 2\pi r l'), M('S_L = \pi r^2 l'), M('S_L = \\dfrac{1}{3} \pi r l')],
          'ផ្ទៃក្រឡាខាងនៃកោន ៖ ' + M('S_L = \pi r l'),
          FIG_CONE_ELEMENTS)

    M_add('easy', 'cone_volume_formula',
          'តើរូបមន្តគណនាមាឌកោនដែលមានកាំបាត ' + M('r') + ' និងកម្ពស់ ' + M('h') + ' ណាត្រឹមត្រូវ?',
          M('V = \\dfrac{1}{3} \pi r^2 h'),
          [M('V = \pi r^2 h'), M('V = \\dfrac{1}{2} \pi r^2 h'), M('V = \\dfrac{4}{3} \pi r^3')],
          'មាឌកោនស្មើមួយភាគបីនៃមាឌស៊ីឡាំងដែលមានបាតនិងកម្ពស់ដូចគ្នា ៖ ' + M('V = \\dfrac{1}{3} \pi r^2 h'))

    M_add('easy', 'cube_volume_calc',
          'គូបមួយមានរង្វាស់គែម ' + M('a = 5\\ \\text{cm}') + '។ គណនាមាឌនៃគូបនោះ។',
          M('125\\ \\text{cm}^3'),
          [M('25\\ \\text{cm}^3'), M('150\\ \\text{cm}^3'), M('75\\ \\text{cm}^3')],
          M('V = a^3 = 5^3 = 125\\ \\text{cm}^3'))

    M_add('easy', 'cuboid_volume_calc',
          'ប្រលេឡេពីប៉ែតកែងមួយមានបណ្តោយ ' + M('8\\ \\text{cm}') + ', ទទឹង ' + M('5\\ \\text{cm}') + ' និងកម្ពស់ ' + M('4\\ \\text{cm}') + '។ គណនាមាឌរបស់វា។',
          M('160\\ \\text{cm}^3'),
          [M('80\\ \\text{cm}^3'), M('40\\ \\text{cm}^3'), M('17\\ \\text{cm}^3')],
          M('V = 8 \\times 5 \\times 4 = 160\\ \\text{cm}^3'))

    M_add('easy', 'cylinder_volume_formula',
          'តើរូបមន្តគណនាមាឌស៊ីឡាំងដែលមានកាំបាត ' + M('r') + ' និងកម្ពស់ ' + M('h') + ' ណាត្រឹមត្រូវ?',
          M('V = \pi r^2 h'),
          [M('V = 2\pi r h'), M('V = \\dfrac{1}{3} \pi r^2 h'), M('V = \pi r h^2')],
          'មាឌស៊ីឡាំង ៖ ' + M('V = \pi r^2 h'))

    M_add('easy', 'cone_slant_height_rel',
          'តើទំនាក់ទំនងរវាងកម្ពស់ ' + M('h') + ', កាំបាត ' + M('r') + ' និងជននី ' + M('l') + ' នៃកោនណាត្រឹមត្រូវ?',
          M('l^2 = r^2 + h^2'),
          [M('l = r + h'), M('h^2 = l^2 + r^2'), M('l^2 = h^2 - r^2')],
          'តាមពីតាក័រក្នុងត្រីកោណកែង ៖ ' + M('l = \sqrt{r^2 + h^2}'))

    # ==========================================
    # 2. MCQ MEDIUM (14 target)
    # ==========================================
    M_add('medium', 'calc_tri_prism_volume',
          'ព្រីសត្រង់មួយមានបាតជាត្រីកោណកែងដែលមានជ្រុងមុំកែង ' + M('6\\ \\text{cm}') + ' និង ' + M('8\\ \\text{cm}') + '។ បើកម្ពស់ព្រីសគឺ ' + M('10\\ \\text{cm}') + ' គណនាមាឌព្រីស។',
          M('240\\ \\text{cm}^3'),
          [M('480\\ \\text{cm}^3'), M('120\\ \\text{cm}^3'), M('140\\ \\text{cm}^3')],
          'ផ្ទៃបាត ៖ ' + M('S_B = \\dfrac{6 \\times 8}{2} = 24\\ \\text{cm}^2 \\Rightarrow V = 24 \\times 10 = 240\\ \\text{cm}^3'))

    M_add('medium', 'calc_tri_prism_lat_area',
          'ព្រីសត្រង់មួយមានបាតជាត្រីកោណសម័ង្សជ្រុង ' + M('5\\ \\text{cm}') + ' និងកម្ពស់ព្រីស ' + M('12\\ \\text{cm}') + '។ គណនាផ្ទៃក្រឡាខាងនៃព្រីស។',
          M('180\\ \\text{cm}^2'),
          [M('60\\ \\text{cm}^2'), M('90\\ \\text{cm}^2'), M('150\\ \\text{cm}^2')],
          'បរិមាត្របាត ៖ ' + M('p = 3 \\times 5 = 15\\ \\text{cm} \\Rightarrow S_L = 15 \\times 12 = 180\\ \\text{cm}^2'))

    M_add('medium', 'calc_sq_pyramid_volume',
          'ពីរ៉ាមីតទៀងទាត់មួយមានបាតជាការេជ្រុង ' + M('6\\ \\text{cm}') + ' និងកម្ពស់ ' + M('10\\ \\text{cm}') + '។ គណនាមាឌនៃពីរ៉ាមីតនោះ។',
          M('120\\ \\text{cm}^3'),
          [M('360\\ \\text{cm}^3'), M('60\\ \\text{cm}^3'), M('180\\ \\text{cm}^3')],
          'ផ្ទៃបាត ៖ ' + M('S_B = 6^2 = 36\\ \\text{cm}^2 \\Rightarrow V = \\dfrac{1}{3} \\times 36 \\times 10 = 120\\ \\text{cm}^3'))

    M_add('medium', 'calc_sq_pyramid_lat_area',
          'ពីរ៉ាមីតទៀងទាត់មួយមានបាតជាការេជ្រុង ' + M('8\\ \\text{cm}') + ' និងអាប៉ូតែម ' + M('a = 5\\ \\text{cm}') + '។ គណនាផ្ទៃក្រឡាខាងរបស់វា។',
          M('80\\ \\text{cm}^2'),
          [M('160\\ \\text{cm}^2'), M('40\\ \\text{cm}^2'), M('144\\ \\text{cm}^2')],
          'បរិមាត្របាត ៖ ' + M('p = 4 \\times 8 = 32\\ \\text{cm} \\Rightarrow S_L = \\dfrac{1}{2} \\times 32 \\times 5 = 80\\ \\text{cm}^2'))

    M_add('medium', 'calc_cone_lat_area_calc',
          'កោនមួយមានកាំបាត ' + M('r = 3\\ \\text{cm}') + ' និងជននី ' + M('l = 5\\ \\text{cm}') + '។ គណនាផ្ទៃក្រឡាខាងជាអនុគមន៍នៃ ' + M('\pi') + '។',
          M('15\pi\\ \\text{cm}^2'),
          [M('30\pi\\ \\text{cm}^2'), M('24\pi\\ \\text{cm}^2'), M('9\pi\\ \\text{cm}^2')],
          M('S_L = \pi r l = \pi \\times 3 \\times 5 = 15\pi\\ \\text{cm}^2'))

    M_add('medium', 'calc_cone_total_area',
          'កោនមួយមានកាំបាត ' + M('r = 4\\ \\text{cm}') + ' និងជននី ' + M('l = 6\\ \\text{cm}') + '។ គណនាផ្ទៃក្រឡាទាំងអស់នៃកោនជាអនុគមន៍នៃ ' + M('\pi') + '។',
          M('40\pi\\ \\text{cm}^2'),
          [M('24\pi\\ \\text{cm}^2'), M('16\pi\\ \\text{cm}^2'), M('48\pi\\ \\text{cm}^2')],
          M('S_T = \pi r l + \pi r^2 = \pi(4)(6) + \pi(4^2) = 24\pi + 16\pi = 40\pi\\ \\text{cm}^2'))

    M_add('medium', 'calc_cone_volume_nums',
          'កោនមួយមានកាំបាត ' + M('r = 6\\ \\text{cm}') + ' និងកម្ពស់ ' + M('h = 10\\ \\text{cm}') + '។ គណនាមាឌកោនជាអនុគមន៍នៃ ' + M('\pi') + '។',
          M('120\pi\\ \\text{cm}^3'),
          [M('360\pi\\ \\text{cm}^3'), M('60\pi\\ \\text{cm}^3'), M('180\pi\\ \\text{cm}^3')],
          M('V = \\dfrac{1}{3} \pi r^2 h = \\dfrac{1}{3} \pi (36)(10) = 120\pi\\ \\text{cm}^3'))

    M_add('medium', 'calc_cone_generator_pyth',
          'កោនមួយមានកាំបាត ' + M('r = 6\\ \\text{cm}') + ' និងកម្ពស់ ' + M('h = 8\\ \\text{cm}') + '។ គណនាប្រវែងជននី ' + M('l') + ' នៃកោន។',
          M('10\\ \\text{cm}'),
          [M('14\\ \\text{cm}'), M('12\\ \\text{cm}'), M('\sqrt{28}\\ \\text{cm}')],
          M('l = \sqrt{r^2 + h^2} = \sqrt{6^2 + 8^2} = \sqrt{36 + 64} = 10\\ \\text{cm}'))

    M_add('medium', 'calc_cylinder_volume_nums',
          'ស៊ីឡាំងមួយមានកាំបាត ' + M('r = 5\\ \\text{cm}') + ' និងកម្ពស់ ' + M('h = 12\\ \\text{cm}') + '។ គណនាមាឌស៊ីឡាំងជាអនុគមន៍នៃ ' + M('\pi') + '។',
          M('300\pi\\ \\text{cm}^3'),
          [M('60\pi\\ \\text{cm}^3'), M('150\pi\\ \\text{cm}^3'), M('600\pi\\ \\text{cm}^3')],
          M('V = \pi r^2 h = \pi (5^2)(12) = 300\pi\\ \\text{cm}^3'))

    M_add('medium', 'calc_cylinder_lat_area',
          'ស៊ីឡាំងមួយមានកាំបាត ' + M('r = 7\\ \\text{cm}') + ' និងកម្ពស់ ' + M('h = 10\\ \\text{cm}') + '។ គណនាផ្ទៃក្រឡាខាង (យក ' + M('\pi \approx \\dfrac{22}{7}') + ')។',
          M('440\\ \\text{cm}^2'),
          [M('220\\ \\text{cm}^2'), M('880\\ \\text{cm}^2'), M('154\\ \\text{cm}^2')],
          M('S_L = 2\pi r h = 2 \\times \\dfrac{22}{7} \\times 7 \\times 10 = 440\\ \\text{cm}^2'))

    M_add('medium', 'calc_cube_total_area',
          'គូបមួយមានមាឌ ' + M('64\\ \\text{cm}^3') + '។ គណនាផ្ទៃក្រឡាសរុបនៃគូបនោះ។',
          M('96\\ \\text{cm}^2'),
          [M('16\\ \\text{cm}^2'), M('64\\ \\text{cm}^2'), M('24\\ \\text{cm}^2')],
          'គែម ៖ ' + M('a = \sqrt[3]{64} = 4\\ \\text{cm} \\Rightarrow S = 6a^2 = 6 \\times 16 = 96\\ \\text{cm}^2'))

    M_add('medium', 'water_liters_conversion',
          'អាងស្តុកទឹកមួយរាងប្រលេឡេពីប៉ែតកែងមានវិមាត្រ ' + M('2\\ \\text{m} \\times 1.5\\ \\text{m} \\times 1\\ \\text{m}') + '។ តើអាងនេះអាចផ្ទុកទឹកបានប៉ុន្មានលីត្រ?',
          M('3\\,000\\ \\text{L}'),
          [M('300\\ \\text{L}'), M('30\\,000\\ \\text{L}'), M('30\\ \\text{L}')],
          M('V = 2 \\times 1.5 \\times 1 = 3\\ \\text{m}^3') + '។ ដោយ ' + M('1\\ \\text{m}^3 = 1000\\ \\text{L} \\Rightarrow 3000\\ \\text{L}'))

    M_add('medium', 'pyramid_total_area_calc',
          'ពីរ៉ាមីតទៀងទាត់មួយមានបាតជាការេជ្រុង ' + M('10\\ \\text{cm}') + ' និងផ្ទៃក្រឡាខាង ' + M('260\\ \\text{cm}^2') + '។ គណនាផ្ទៃក្រឡាទាំងអស់នៃពីរ៉ាមីត។',
          M('360\\ \\text{cm}^2'),
          [M('270\\ \\text{cm}^2'), M('460\\ \\text{cm}^2'), M('310\\ \\text{cm}^2')],
          'ផ្ទៃបាត ៖ ' + M('S_B = 10^2 = 100\\ \\text{cm}^2 \\Rightarrow S_T = S_L + S_B = 260 + 100 = 360\\ \\text{cm}^2'))

    M_add('medium', 'cone_vs_cylinder_ratio',
          'ស៊ីឡាំងមួយ និងកោនមួយមានកាំបាត ' + M('r') + ' ដូចគ្នា និងកម្ពស់ ' + M('h') + ' ដូចគ្នា។ តើផលធៀបមាឌកោនធៀបនឹងមាឌស៊ីឡាំងស្មើនឹងប៉ុន្មាន?',
          M('\\dfrac{1}{3}'),
          [M('\\dfrac{1}{2}'), M('\\dfrac{2}{3}'), M('3')],
          M('\\dfrac{V_{\\text{កោន}}}{V_{\\text{ស៊ីឡាំង}}} = \\dfrac{\\frac{1}{3}\pi r^2 h}{\pi r^2 h} = \\dfrac{1}{3}'))

    # ==========================================
    # 3. MCQ HARD (7 target)
    # ==========================================
    M_add('hard', 'pyramid_apothem_from_height',
          'ពីរ៉ាមីតទៀងទាត់មួយមានបាតជាការេជ្រុង ' + M('12\\ \\text{cm}') + ' និងកម្ពស់ ' + M('8\\ \\text{cm}') + '។ គណនាប្រវែងអាប៉ូតែម ' + M('a') + ' នៃពីរ៉ាមីតនោះ។',
          M('10\\ \\text{cm}'),
          [M('14\\ \\text{cm}'), M('12\\ \\text{cm}'), M('6\\ \\text{cm}')],
          'ចម្ងាយពីផ្ចិតបាតទៅជ្រុងគឺ ' + M('r = \\dfrac{12}{2} = 6\\ \\text{cm} \\Rightarrow a = \sqrt{8^2 + 6^2} = 10\\ \\text{cm}'))

    M_add('hard', 'sq_pyramid_total_surface_complete',
          'ពីរ៉ាមីតទៀងទាត់មានបាតជាការេជ្រុង ' + M('16\\ \\text{cm}') + ' និងកម្ពស់ ' + M('6\\ \\text{cm}') + '។ គណនាផ្ទៃក្រឡាទាំងអស់នៃពីរ៉ាមីត។',
          M('576\\ \\text{cm}^2'),
          [M('256\\ \\text{cm}^2'), M('320\\ \\text{cm}^2'), M('512\\ \\text{cm}^2')],
          M('a = \sqrt{6^2 + 8^2} = 10\\ \\text{cm} \\Rightarrow S_L = \\dfrac{1}{2}(64)(10) = 320\\ \\text{cm}^2') + '; ' + M('S_B = 256 \\Rightarrow S_T = 576\\ \\text{cm}^2'))

    M_add('hard', 'cone_volume_from_total_area',
          'កោនមួយមានកាំបាត ' + M('r = 5\\ \\text{cm}') + ' និងជននី ' + M('l = 13\\ \\text{cm}') + '។ គណនាមាឌកោនជាអនុគមន៍នៃ ' + M('\pi') + '។',
          M('100\pi\\ \\text{cm}^3'),
          [M('300\pi\\ \\text{cm}^3'), M('150\pi\\ \\text{cm}^3'), M('325\pi\\ \\text{cm}^3')],
          M('h = \sqrt{13^2 - 5^2} = 12\\ \\text{cm} \\Rightarrow V = \\dfrac{1}{3} \pi (25)(12) = 100\pi\\ \\text{cm}^3'))

    M_add('hard', 'prism_hexagonal_volume',
          'ព្រីសទៀងទាត់មួយមានកម្ពស់ ' + M('10\\ \\text{cm}') + ' និងបាតជាឆកោណទៀងទាត់ជ្រុង ' + M('4\\ \\text{cm}') + '។ គណនាមាឌនៃព្រីសជាទម្រង់រ៉ាឌីកាល់សម្រួល។',
          M('240\sqrt{3}\\ \\text{cm}^3'),
          [M('120\sqrt{3}\\ \\text{cm}^3'), M('480\sqrt{3}\\ \\text{cm}^3'), M('240\\ \\text{cm}^3')],
          'ផ្ទៃបាត ៖ ' + M('S_B = 6 \\times \\left(\\dfrac{\sqrt{3}}{4} \\times 16\\right) = 24\sqrt{3}\\ \\text{cm}^2 \\Rightarrow V = 24\sqrt{3} \\times 10 = 240\sqrt{3}\\ \\text{cm}^3'))

    M_add('hard', 'composite_solid_pencil',
          'វត្ថុរឹងមួយផ្សំឡើងដោយស៊ីឡាំងកម្ពស់ ' + M('12\\ \\text{cm}') + ' និងកោននៅពីលើកម្ពស់ ' + M('3\\ \\text{cm}') + ' ដោយមានកាំបាតរួម ' + M('r = 4\\ \\text{cm}') + '។ គណនាមាឌសរុបជាអនុគមន៍នៃ ' + M('\pi') + '។',
          M('208\pi\\ \\text{cm}^3'),
          [M('240\pi\\ \\text{cm}^3'), M('192\pi\\ \\text{cm}^3'), M('224\pi\\ \\text{cm}^3')],
          M('V_1 = \pi (16)(12) = 192\pi') + '; ' + M('V_2 = \\dfrac{1}{3} \pi (16)(3) = 16\pi \\Rightarrow V = 192\pi + 16\pi = 208\pi\\ \\text{cm}^3'))

    M_add('hard', 'hollow_cylinder_pipe',
          'បំពង់ដែកស៊ីឡាំងប្រហោងមួយមានកម្ពស់ ' + M('50\\ \\text{cm}') + ', កាំក្រៅ ' + M('R = 6\\ \\text{cm}') + ' និងកាំក្នុង ' + M('r = 4\\ \\text{cm}') + '។ គណនាមាឌដែកពិតប្រាកដជាអនុគមន៍នៃ ' + M('\pi') + '។',
          M('1\\,000\pi\\ \\text{cm}^3'),
          [M('2\\,000\pi\\ \\text{cm}^3'), M('500\pi\\ \\text{cm}^3'), M('800\pi\\ \\text{cm}^3')],
          M('V = \pi(R^2 - r^2)h = \pi(36 - 16)(50) = 1000\pi\\ \\text{cm}^3'))

    M_add('hard', 'sphere_in_cylinder',
          'ស៊ីឡាំងមួយមានកម្ពស់ ' + M('h = 10\\ \\text{cm}') + ' និងកាំបាត ' + M('r = 5\\ \\text{cm}') + '។ គេទម្លាក់ដុំដែកមួយចូលធ្វើឱ្យទឹកហៀរចេញ ' + M('25\%') + ' នៃចំណុះស៊ីឡាំង។ តើដុំដែកនោះមានមាឌប៉ុន្មានជាអនុគមន៍នៃ ' + M('\pi') + '?',
          M('62.5\pi\\ \\text{cm}^3'),
          [M('250\pi\\ \\text{cm}^3'), M('125\pi\\ \\text{cm}^3'), M('50\pi\\ \\text{cm}^3')],
          M('V = \pi (25)(10) = 250\pi \\Rightarrow V_{\\text{ដែក}} = 250\pi \\times 0.25 = 62.5\pi\\ \\text{cm}^3'))

    # ==========================================
    # 4. MCQ PISA (5 target)
    # ==========================================
    M_add('pisa', 'party_hat_paper',
          'មួកខួបកំណើតមួយរាងកោនមានកាំបាត ' + M('7\\ \\text{cm}') + ' និងជននី ' + M('25\\ \\text{cm}') + '។ គណនាផ្ទៃក្រដាសរឹងដែលត្រូវប្រើធ្វើមួកមួយនេះ (មិនគិតបាត, យក ' + M('\pi \approx \\dfrac{22}{7}') + ')។',
          M('550\\ \\text{cm}^2'),
          [M('704\\ \\text{cm}^2'), M('350\\ \\text{cm}^2'), M('1\\,100\\ \\text{cm}^2')],
          M('S_L = \pi r l = \\dfrac{22}{7} \\times 7 \\times 25 = 550\\ \\text{cm}^2'))

    M_add('pisa', 'tent_camping_cone',
          'តង់បោះជំរំមួយរាងកោនមានកម្ពស់ ' + M('2.4\\ \\text{m}') + ' និងកាំបាត ' + M('0.7\\ \\text{m}') + '។ គណនាផ្ទៃក្រណាត់តង់ដែលត្រូវប្រើធ្វើដំបូលជុំវិញ (យក ' + M('\pi \approx \\dfrac{22}{7}') + ')។',
          M('5.5\\ \\text{m}^2'),
          [M('7.04\\ \\text{m}^2'), M('11\\ \\text{m}^2'), M('4.8\\ \\text{m}^2')],
          M('l = \sqrt{2.4^2 + 0.7^2} = 2.5\\ \\text{m} \\Rightarrow S_L = \\dfrac{22}{7} \\times 0.7 \\times 2.5 = 5.5\\ \\text{m}^2'))

    M_add('pisa', 'grain_silo_capacity',
          'ស៊ីឡូស្តុកស្រូវមួយផ្នែកខាងក្រោមជារាងស៊ីឡាំងកម្ពស់ ' + M('10\\ \\text{m}') + ' និងកាំ ' + M('3\\ \\text{m}') + '។ គណនាមាឌស្តុកនៃផ្នែកស៊ីឡាំងនោះ (យក ' + M('\pi \approx 3.14') + ')។',
          M('282.6\\ \\text{m}^3'),
          [M('94.2\\ \\text{m}^3'), M('188.4\\ \\text{m}^3'), M('565.2\\ \\text{m}^3')],
          M('V = 3.14 \\times 3^2 \\times 10 = 3.14 \\times 90 = 282.6\\ \\text{m}^3'))

    M_add('pisa', 'ice_cream_cone_capacity',
          'នំកោនការ៉េមមួយមានកាំមាត់ ' + M('3\\ \\text{cm}') + ' និងជម្រៅកម្ពស់ ' + M('14\\ \\text{cm}') + '។ គណនាមាឌការ៉េមរលាយដែលអាចបំពេញក្នុងនំនោះបាន (យក ' + M('\pi \approx \\dfrac{22}{7}') + ')។',
          M('132\\ \\text{cm}^3'),
          [M('396\\ \\text{cm}^3'), M('66\\ \\text{cm}^3'), M('264\\ \\text{cm}^3')],
          M('V = \\dfrac{1}{3} \\times \\dfrac{22}{7} \\times 3^2 \\times 14 = \\dfrac{1}{3} \\times 22 \\times 9 \\times 2 = 132\\ \\text{cm}^3'))

    M_add('pisa', 'gift_box_wrapping',
          'ប្រអប់កាដូរាងគូបមួយមានរង្វាស់គែម ' + M('20\\ \\text{cm}') + '។ បើគេចង់ខ្ចប់ប្រអប់នេះដោយប្រើក្រដាសកាដូបូកបន្ថែម ' + M('10\%') + ' សម្រាប់ផ្នត់គែម តើត្រូវប្រើក្រដាសផ្ទៃប៉ុន្មាន?',
          M('2\\,640\\ \\text{cm}^2'),
          [M('2\\,400\\ \\text{cm}^2'), M('4\\,800\\ \\text{cm}^2'), M('2\\,880\\ \\text{cm}^2')],
          M('S = 6 \\times 20^2 = 2400\\ \\text{cm}^2 \\Rightarrow S_{\\text{ក្រដាស}} = 2400 \\times 1.10 = 2640\\ \\text{cm}^2'))

    # ==========================================
    # 5. WRITING EASY (1 target, 5 pts total)
    # ==========================================
    W('easy', 'wr_tri_prism_basic',
      'ព្រីសត្រង់មួយមានកម្ពស់ ' + M('h = 10\\ \\text{cm}') + ' និងបាតជាត្រីកោណកែងដែលមានជ្រុងមុំកែង ' + M('a = 3\\ \\text{cm}') + ' និង ' + M('b = 4\\ \\text{cm}') + '។\n'
      'ក. គណនាផ្ទៃក្រឡាបាត ' + M('S_B') + ' នៃព្រីស។\n'
      'ខ. សរសេររូបមន្ត និងគណនាមាឌ ' + M('V') + ' នៃព្រីស។', [
          ('ក. ផ្ទៃបាត ៖ ' + M('S_B = \\dfrac{a \\times b}{2} = \\dfrac{3 \\times 4}{2} = 6\\ \\text{cm}^2'), 2),
          ('ខ. រូបមន្តមាឌព្រីស ៖ ' + M('V = S_B \\times h'), 1),
          ('ជំនួសតម្លៃ ៖ ' + M('V = 6 \\times 10 = 60\\ \\text{cm}^3'), 2)], FIG_PRISM_TRIANGULAR)

    # ==========================================
    # 6. WRITING MEDIUM (4 target, 5 pts total each)
    # ==========================================
    W('medium', 'wr_cone_complete_calc',
      'កោនមួយមានកាំបាត ' + M('r = 6\\ \\text{cm}') + ' និងកម្ពស់ ' + M('h = 8\\ \\text{cm}') + '។\n'
      'ក. គណនាប្រវែងជននី ' + M('l') + ' នៃកោន។\n'
      'ខ. គណនាផ្ទៃក្រឡាខាង ' + M('S_L') + ' ជាអនុគមន៍នៃ ' + M('\pi') + '។\n'
      'គ. គណនាមាឌ ' + M('V') + ' នៃកោនជាអនុគមន៍នៃ ' + M('\pi') + '។', [
          ('ក. តាមពីតាក័រ ៖ ' + M('l = \sqrt{r^2 + h^2} = \sqrt{6^2 + 8^2} = \sqrt{100} = 10\\ \\text{cm}'), 2),
          ('ខ. ផ្ទៃក្រឡាខាង ៖ ' + M('S_L = \pi r l = \pi \\times 6 \\times 10 = 60\pi\\ \\text{cm}^2'), 1),
          ('គ. មាឌកោន ៖ ' + M('V = \\dfrac{1}{3} \pi r^2 h = \\dfrac{1}{3} \pi (36)(8) = 96\pi\\ \\text{cm}^3'), 2)], FIG_CONE_ELEMENTS)

    W('medium', 'wr_sq_pyramid_calc',
      'ពីរ៉ាមីតទៀងទាត់មួយមានបាតជាការេជ្រុង ' + M('10\\ \\text{cm}') + ' និងអាប៉ូតែម ' + M('a = 13\\ \\text{cm}') + '។\n'
      'ក. គណនាបរិមាត្របាត ' + M('p') + ' និងផ្ទៃក្រឡាបាត ' + M('S_B') + '។\n'
      'ខ. គណនាផ្ទៃក្រឡាខាង ' + M('S_L') + ' នៃពីរ៉ាមីត។\n'
      'គ. គណនាផ្ទៃក្រឡាទាំងអស់ ' + M('S_T') + ' នៃពីរ៉ាមីត។', [
          ('ក. បរិមាត្របាត ៖ ' + M('p = 4 \\times 10 = 40\\ \\text{cm}') + '; ផ្ទៃបាត ៖ ' + M('S_B = 10^2 = 100\\ \\text{cm}^2'), 2),
          ('ខ. ផ្ទៃក្រឡាខាង ៖ ' + M('S_L = \\dfrac{1}{2} p \\times a = \\dfrac{1}{2} \\times 40 \\times 13 = 260\\ \\text{cm}^2'), 2),
          ('គ. ផ្ទៃក្រឡាទាំងអស់ ៖ ' + M('S_T = S_L + S_B = 260 + 100 = 360\\ \\text{cm}^2'), 1)], FIG_PYRAMID_SQUARE)

    W('medium', 'wr_cylinder_complete',
      'ស៊ីឡាំងមួយមានកាំបាត ' + M('r = 7\\ \\text{cm}') + ' និងកម្ពស់ ' + M('h = 15\\ \\text{cm}') + '។\n'
      'ក. គណនាផ្ទៃក្រឡាខាង ' + M('S_L') + ' នៃស៊ីឡាំង (យក ' + M('\pi \approx \\dfrac{22}{7}') + ')។\n'
      'ខ. គណនាផ្ទៃក្រឡាទាំងអស់ ' + M('S_T') + ' នៃស៊ីឡាំង។\n'
      'គ. គណនាមាឌ ' + M('V') + ' នៃស៊ីឡាំង។', [
          ('ក. ' + M('S_L = 2\pi r h = 2 \\times \\dfrac{22}{7} \\times 7 \\times 15 = 660\\ \\text{cm}^2'), 2),
          ('ខ. ផ្ទៃបាតពីរ ៖ ' + M('2S_B = 2 \\times \\dfrac{22}{7} \\times 49 = 308\\ \\text{cm}^2 \\Rightarrow S_T = 660 + 308 = 968\\ \\text{cm}^2'), 1),
          ('គ. មាឌ ៖ ' + M('V = \pi r^2 h = \\dfrac{22}{7} \\times 49 \\times 15 = 154 \\times 15 = 2310\\ \\text{cm}^3'), 2)])

    W('medium', 'wr_tri_prism_total_area',
      'ព្រីសត្រង់មួយមានកម្ពស់ ' + M('12\\ \\text{cm}') + ' និងបាតជាត្រីកោណសម័ង្សជ្រុង ' + M('6\\ \\text{cm}') + '។\n'
      'ក. គណនាផ្ទៃក្រឡាខាង ' + M('S_L') + ' នៃព្រីស។\n'
      'ខ. គណនាផ្ទៃក្រឡាបាត ' + M('S_B') + ' មួយជាទម្រង់រ៉ាឌីកាល់សម្រួល។\n'
      'គ. គណនាផ្ទៃក្រឡាទាំងអស់ ' + M('S_T') + ' នៃព្រីស។', [
          ('ក. បរិមាត្របាត ៖ ' + M('p = 3 \\times 6 = 18\\ \\text{cm} \\Rightarrow S_L = 18 \\times 12 = 216\\ \\text{cm}^2'), 2),
          ('ខ. ផ្ទៃបាត ៖ ' + M('S_B = \\dfrac{\sqrt{3}}{4} \\times 6^2 = 9\sqrt{3}\\ \\text{cm}^2'), 1),
          ('គ. ផ្ទៃទាំងអស់ ៖ ' + M('S_T = S_L + 2S_B = 216 + 18\sqrt{3}\\ \\text{cm}^2'), 2)])

    # ==========================================
    # 7. WRITING HARD (4 target, 5 pts total each)
    # ==========================================
    W('hard', 'wr_pyramid_height_from_apothem',
      'ពីរ៉ាមីតទៀងទាត់មួយមានបាតជាការេជ្រុង ' + M('16\\ \\text{cm}') + ' និងអាប៉ូតែម ' + M('a = 17\\ \\text{cm}') + '។\n'
      'ក. គណនាចម្ងាយពីផ្ចិតបាតទៅជ្រុងបាត ' + M('r') + '។\n'
      'ខ. គណនាកម្ពស់ ' + M('h') + ' នៃពីរ៉ាមីត។\n'
      'គ. គណនាមាឌ ' + M('V') + ' នៃពីរ៉ាមីត។', [
          ('ក. ' + M('r = \\dfrac{16}{2} = 8\\ \\text{cm}'), 1),
          ('ខ. ក្នុងត្រីកោណកែង ៖ ' + M('h = \sqrt{a^2 - r^2} = \sqrt{17^2 - 8^2} = \sqrt{289 - 64} = \sqrt{225} = 15\\ \\text{cm}'), 2),
          ('គ. ផ្ទៃបាត ' + M('S_B = 16^2 = 256\\ \\text{cm}^2 \\Rightarrow V = \\dfrac{1}{3} \\times 256 \\times 15 = 1280\\ \\text{cm}^3'), 2)])

    W('hard', 'wr_cone_sector_unfolding',
      'ក្រដាសមួយផ្ទាំងជារាងចម្រៀករង្វង់មានកាំ ' + M('R = 10\\ \\text{cm}') + ' និងមុំផ្ចិត ' + M('216^\circ') + ' ត្រូវបានរុំបង្កើតជាកោនមួយ។\n'
      'ក. គណនាប្រវែងធ្នូនៃចម្រៀករង្វង់ (យក ' + M('\pi') + ')។\n'
      'ខ. បង្ហាញថាប្រវែងធ្នូនេះស្មើនឹងបរិមាត្របាតកោន រួចទាញរកកាំបាត ' + M('r') + '។\n'
      'គ. គណនាកម្ពស់ ' + M('h') + ' និងមាឌ ' + M('V') + ' នៃកោននោះ។', [
          ('ក. ប្រវែងធ្នូ ៖ ' + M('L = \\dfrac{2\pi (10) \\times 216}{360} = 12\pi\\ \\text{cm}'), 1),
          ('ខ. បរិមាត្របាតកោន ' + M('2\pi r = 12\pi \\Rightarrow r = 6\\ \\text{cm}') + ' (ជននីកោនគឺ ' + M('l = R = 10\\ \\text{cm}') + ')', 2),
          ('គ. កម្ពស់ ' + M('h = \sqrt{10^2 - 6^2} = 8\\ \\text{cm} \\Rightarrow V = \\dfrac{1}{3}\pi (36)(8) = 96\pi\\ \\text{cm}^3'), 2)])

    W('hard', 'wr_trapezoidal_prism_trough',
      'ស្នូកទឹកមួយរាងព្រីសត្រង់មានបាតជាចតុកោណព្នាយសមបាត ៖ បាតតូច ' + M('0.6\\ \\text{m}') + ', បាតធំ ' + M('1.2\\ \\text{m}') + ', ជម្រៅ ' + M('0.8\\ \\text{m}') + ' និងប្រវែងស្នូក ' + M('3\\ \\text{m}') + '។\n'
      'ក. គណនាផ្ទៃក្រឡាបាតចតុកោណព្នាយ។\n'
      'ខ. គណនាមាឌទឹកអតិបរិមាដែលស្នូកអាចផ្ទុកបានគិតជាម៉ែត្រគូប។\n'
      'គ. បំលែងមាឌទឹកនោះទៅជាលីត្រ (' + M('\\text{L}') + ')។', [
          ('ក. ផ្ទៃបាតព្នាយ ៖ ' + M('S_B = \\dfrac{(0.6 + 1.2) \\times 0.8}{2} = \\dfrac{1.8 \\times 0.8}{2} = 0.72\\ \\text{m}^2'), 2),
          ('ខ. មាឌស្នូក ៖ ' + M('V = S_B \\times h = 0.72 \\times 3 = 2.16\\ \\text{m}^3'), 1),
          ('គ. ដោយ ' + M('1\\ \\text{m}^3 = 1000\\ \\text{L} \\Rightarrow 2.16 \\times 1000 = 2160\\ \\text{L}'), 2)])

    W('hard', 'wr_metal_melting_sphere_cylinder',
      'គេយកដុំដែកទម្រង់គូបជ្រុង ' + M('a = 6\\ \\text{cm}') + ' ទៅរំលាយរួចចាក់ពុម្ពធ្វើជាកោនមួយដែលមានកាំបាត ' + M('r = 6\\ \\text{cm}') + '។\n'
      'ក. គណនាមាឌនៃដុំដែកគូបដើម។\n'
      'ខ. គណនាកម្ពស់ ' + M('h') + ' នៃកោនថ្មី (ដឹងថាមាឌមិនបាត់បង់, យក ' + M('\pi \approx 3.14') + ')។\n'
      'គ. ប្រៀបធៀបកម្ពស់កោនធៀបនឹងជ្រុងគូប។', [
          ('ក. មាឌគូប ៖ ' + M('V = 6^3 = 216\\ \\text{cm}^3'), 1),
          ('ខ. មាឌកោន ៖ ' + M('V = \\dfrac{1}{3} \pi r^2 h \\Rightarrow 216 = \\dfrac{1}{3} \\times 3.14 \\times 36 \\times h = 37.68 h'), 2),
          ('ទាញបាន ' + M('h = \\dfrac{216}{37.68} \approx 5.73\\ \\text{cm}'), 1),
          ('គ. កម្ពស់កោន ' + M('h \approx 5.73\\ \\text{cm} < 6\\ \\text{cm}') + ' (ទាបជាងជ្រុងគូបបន្តិច)', 1)])

    # ==========================================
    # 8. WRITING PISA (5 target, 5 pts total each)
    # ==========================================
    W('pisa', 'wr_pisa_water_tank_concrete',
      'អាងស្តុកទឹកបេតុងរាងប្រលេឡេពីប៉ែតកែងមួយមានវិមាត្រខាងក្នុង ៖ បណ្តោយ ' + M('4\\ \\text{m}') + ', ទទឹង ' + M('2.5\\ \\text{m}') + ' និងកម្ពស់ ' + M('2\\ \\text{m}') + '។\n'
      'ក. គណនាចំណុះទឹកអតិបរិមានៃអាងគិតជាលីត្រ។\n'
      'ខ. បើគេចង់បូកស៊ីម៉ង់តិ៍ផ្ទៃជញ្ជាំងខាងក្នុងទាំង ៤ និងបាតក្រោម គណនាផ្ទៃក្រឡាដែលត្រូវបូក។\n'
      'គ. បើថ្លៃបូកស៊ីម៉ង់តិ៍គឺ ' + M('6\$/\\text{m}^2') + ' គណនាថ្លៃចំណាយសរុប។', [
          ('ក. មាឌអាង ៖ ' + M('V = 4 \\times 2.5 \\times 2 = 20\\ \\text{m}^3 = 20\\,000\\ \\text{L}'), 2),
          ('ខ. ផ្ទៃបាត ៖ ' + M('4 \\times 2.5 = 10\\ \\text{m}^2') + '; ផ្ទៃជញ្ជាំង ៤ ៖ ' + M('2(4 + 2.5) \\times 2 = 26\\ \\text{m}^2 \\Rightarrow S = 10 + 26 = 36\\ \\text{m}^2'), 2),
          ('គ. ថ្លៃចំណាយ ៖ ' + M('36 \\times 6 = 216\$'), 1)])

    W('pisa', 'wr_pisa_circus_tent',
      'រោងសៀកមួយមានដំបូលរាងកោនដែលមានកាំបាត ' + M('14\\ \\text{m}') + ' និងកម្ពស់ ' + M('4.8\\ \\text{m}') + '។\n'
      'ក. គណនាប្រវែងជននី ' + M('l') + ' នៃដំបូលកោន។\n'
      'ខ. គណនាផ្ទៃក្រណាត់តង់ដែលត្រូវប្រើសម្រាប់ដំបូល (យក ' + M('\pi \approx \\dfrac{22}{7}') + ')។\n'
      'គ. បើក្រណាត់តង់ ១ ម៉ែត្រការេមានតម្លៃ ' + M('12\$') + ' គណនាថ្លៃទិញក្រណាត់តង់ដំបូល។', [
          ('ក. ជននី ៖ ' + M('l = \sqrt{14^2 + 4.8^2} = \sqrt{196 + 23.04} = \sqrt{219.04} = 14.8\\ \\text{m}'), 2),
          ('ខ. ផ្ទៃដំបូលកោន ៖ ' + M('S_L = \pi r l = \\dfrac{22}{7} \\times 14 \\times 14.8 = 44 \\times 14.8 = 651.2\\ \\text{m}^2'), 2),
          ('គ. ថ្លៃក្រណាត់តង់ ៖ ' + M('651.2 \\times 12 = 7814.40\$'), 1)])

    W('pisa', 'wr_pisa_grain_silo_storage',
      'ស៊ីឡូស្តុកគ្រាប់ធញ្ញជាតិមួយរាងស៊ីឡាំងមានកាំបាត ' + M('4\\ \\text{m}') + ' និងកម្ពស់ ' + M('15\\ \\text{m}') + '។\n'
      'ក. គណនាមាឌស៊ីឡូស្តុកនោះ (យក ' + M('\pi \approx 3.14') + ')។\n'
      'ខ. បើស្រូវ ១ ម៉ែត្រគូប មានទម្ងន់ ' + M('0.75\\ \\text{តោន}') + ' គណនាទម្ងន់ស្រូវអតិបរិមាដែលអាចស្តុកបាន។\n'
      'គ. បើឡានដឹកស្រូវមួយជើងអាចដឹកបាន ' + M('15\\ \\text{តោន}') + ' តើត្រូវដឹកប៉ុន្មានជើងដើម្បីបំពេញស៊ីឡូនោះ?', [
          ('ក. មាឌស៊ីឡូ ៖ ' + M('V = 3.14 \\times 4^2 \\times 15 = 3.14 \\times 16 \\times 15 = 753.6\\ \\text{m}^3'), 2),
          ('ខ. ទម្ងន់ស្រូវសរុប ៖ ' + M('753.6 \\times 0.75 = 565.2\\ \\text{តោន}'), 2),
          ('គ. ចំនួនជើងឡាន ៖ ' + M('\\dfrac{565.2}{15} = 37.68 \\Rightarrow 38\\ \\text{ជើង}'), 1)])

    W('pisa', 'wr_pisa_cardboard_box_packaging',
      'រោងចក្រផលិតប្រអប់ក្រដាសមួយចង់ផលិតប្រអប់រាងប្រលេឡេពីប៉ែតកែងមានវិមាត្រ ' + M('30\\ \\text{cm} \\times 20\\ \\text{cm} \\times 15\\ \\text{cm}') + ' ចំនួន ១០០០ ប្រអប់។\n'
      'ក. គណនាផ្ទៃក្រឡាទាំងអស់នៃប្រអប់មួយ។\n'
      'ខ. ដោយគិតបន្ថែម ' + M('15\%') + ' សម្រាប់កាត់គែមនិងបិទកាវ គណនាផ្ទៃក្រដាសរឹងសរុបសម្រាប់ ១ ប្រអប់។\n'
      'គ. គណនាផ្ទៃក្រដាសរឹងសរុបគិតជាម៉ែត្រការេ (' + M('\\text{m}^2') + ') សម្រាប់ផលិត ១០០០ ប្រអប់។', [
          ('ក. ផ្ទៃប្រអប់មួយ ៖ ' + M('S_T = 2(30 \\times 20 + 30 \\times 15 + 20 \\times 15) = 2(600 + 450 + 300) = 2700\\ \\text{cm}^2'), 2),
          ('ខ. ផ្ទៃរួមបន្ថែម ' + M('15\%') + ' ៖ ' + M('2700 \\times 1.15 = 3105\\ \\text{cm}^2'), 1),
          ('គ. សម្រាប់ ១០០០ ប្រអប់ ៖ ' + M('3105 \\times 1000 = 3\\,105\\,000\\ \\text{cm}^2 = 310.5\\ \\text{m}^2'), 2)])

    W('pisa', 'wr_pisa_pool_water_rate',
      'អាងហែលទឹកមួយមានបណ្តោយ ' + M('25\\ \\text{m}') + ', ទទឹង ' + M('10\\ \\text{m}') + ' និងជម្រៅទឹកជាមធ្យម ' + M('1.8\\ \\text{m}') + '។\n'
      'ក. គណនាមាឌទឹកក្នុងអាងគិតជាម៉ែត្រគូប។\n'
      'ខ. គេប្រើម៉ាស៊ីនបូមទឹកដែលមានអានុភាពបូម ' + M('50\\ \\text{m}^3/\\text{h}') + '។ តើត្រូវចំណាយពេលប៉ុន្មានម៉ោងដើម្បីបូមទឹកបំពេញអាង?\n'
      'គ. បើតម្លៃទឹកស្អាតគឺ ' + M('1500\\ \\text{រៀល/m}^3') + ' គណនាថ្លៃទឹកសរុបសម្រាប់បំពេញអាង។', [
          ('ក. មាឌទឹក ៖ ' + M('V = 25 \\times 10 \\times 1.8 = 450\\ \\text{m}^3'), 2),
          ('ខ. រយៈពេលបូម ៖ ' + M('T = \\dfrac{450}{50} = 9\\ \\text{ម៉ោង}'), 2),
          ('គ. ថ្លៃទឹកសរុប ៖ ' + M('450 \\times 1500 = 675\\,000\\ \\text{រៀល}'), 1)])

    return C
