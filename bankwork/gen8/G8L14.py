"""Bank candidates for Grade 8, Lesson 14: ទ្រឹស្តីបទពីតាក័រ (Pythagorean Theorem)
Covers MoEYS Grade 8 curriculum:
  1. ទ្រឹស្តីបទពីតាក័រ (Pythagorean Theorem: c^2 = a^2 + b^2)
  2. សម្រាយបញ្ជាក់ទ្រឹស្តីបទពីតាក័រ (Geometric proof using (a+b)^2 square)
  3. ទ្រឹស្តីបទច្រាសពីតាក័រ (Converse of Pythagorean Theorem, obtuse/acute classification)
  4. អង្កត់ទ្រូងចតុកោណកែង ការេ គូប និងប្រលេឡេពីប៉ែតកែង (Diagonals of rectangle, square, cube, cuboid)
  5. ទំនាក់ទំនងក្នុងត្រីកោណកែង (Right triangle altitude, projections)
  6. ចម្ងាយរវាងពីរចំណុចក្នុងប្លង់កូអរដោនេ (Distance formula between two points)
  7. ការអនុវត្តក្នុងជីវភាពរស់នៅ & PISA (Ladders, clearance, cables, screen diagonal, distance savings)

Images: Clean vector illustrations, isolated, no background, flat educational textbook style.
Geometry labels use font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic'.
"""
from lib import *

LESSON = "ទ្រឹស្តីបទពីតាក័រ"

# --- SVG Illustrations ---

# 1. FIG_PYTH_TRI: Right triangle ABC right-angled at A with legs b, c and hypotenuse a
FIG_PYTH_TRI = (
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 280 180' width='280' height='180'>\n"
    "  <!-- Right triangle ABC at A -->\n"
    "  <polygon points='50,140 230,140 50,40' fill='#eff6ff' stroke='#0284c7' stroke-width='2'/>\n"
    "  <!-- Right angle marker at A(50, 140) -->\n"
    "  <path d='M 50,124 L 66,124 L 66,140' fill='none' stroke='#0284c7' stroke-width='1.5'/>\n"
    "  <!-- Vertices (Mathcad italic) -->\n"
    "  <text x='35' y='152' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='15' fill='#0f172a'>A</text>\n"
    "  <text x='245' y='152' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='15' fill='#0f172a'>B</text>\n"
    "  <text x='40' y='32' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='15' fill='#0f172a'>C</text>\n"
    "  <!-- Side labels -->\n"
    "  <text x='32' y='92' text-anchor='end' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#dc2626'>b</text>\n"
    "  <text x='140' y='158' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#dc2626'>c</text>\n"
    "  <text x='150' y='82' text-anchor='start' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#16a34a'>a</text>\n"
    "</svg>"
)

# 2. FIG_PYTH_PROOF: Square (a+b) with 4 congruent right triangles and central square c^2
FIG_PYTH_PROOF = (
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 240 240' width='240' height='240'>\n"
    "  <!-- Outer square (a+b) -->\n"
    "  <rect x='30' y='30' width='180' height='180' fill='#f8fafc' stroke='#334155' stroke-width='1.8'/>\n"
    "  <!-- Inner tilted square c^2 -->\n"
    "  <polygon points='80,30 210,80 160,210 30,160' fill='#ecfdf5' stroke='#16a34a' stroke-width='2'/>\n"
    "  <!-- 4 Corner right triangles tinted light blue -->\n"
    "  <polygon points='30,30 80,30 30,160' fill='#e0f2fe' opacity='0.75'/>\n"
    "  <polygon points='80,30 210,30 210,80' fill='#e0f2fe' opacity='0.75'/>\n"
    "  <polygon points='210,80 210,210 160,210' fill='#e0f2fe' opacity='0.75'/>\n"
    "  <polygon points='160,210 30,210 30,160' fill='#e0f2fe' opacity='0.75'/>\n"
    "  <!-- Dimension labels (Mathcad italic) -->\n"
    "  <text x='55' y='22' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='13' fill='#0f172a'>a</text>\n"
    "  <text x='145' y='22' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='13' fill='#0f172a'>b</text>\n"
    "  <text x='222' y='55' text-anchor='start' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='13' fill='#0f172a'>a</text>\n"
    "  <text x='222' y='145' text-anchor='start' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='13' fill='#0f172a'>b</text>\n"
    "  <!-- Hypotenuse label and area -->\n"
    "  <text x='120' y='126' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='15' fill='#16a34a'>c²</text>\n"
    "  <text x='62' y='90' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='13' fill='#16a34a'>c</text>\n"
    "</svg>"
)

# 3. FIG_LADDER_WALL: Ladder leaning on vertical wall
FIG_LADDER_WALL = (
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 260 200' width='260' height='200'>\n"
    "  <!-- Ground line -->\n"
    "  <line x1='30' y1='170' x2='230' y2='170' stroke='#64748b' stroke-width='2'/>\n"
    "  <!-- Wall vertical line -->\n"
    "  <line x1='60' y1='30' x2='60' y2='170' stroke='#334155' stroke-width='4'/>\n"
    "  <!-- Right angle marker -->\n"
    "  <path d='M 60,154 L 76,154 L 76,170' fill='none' stroke='#334155' stroke-width='1.5'/>\n"
    "  <!-- Ladder leaning from (180, 170) to (60, 50) -->\n"
    "  <line x1='60' y1='50' x2='180' y2='170' stroke='#b45309' stroke-width='4' stroke-linecap='round'/>\n"
    "  <!-- Rungs of ladder -->\n"
    "  <line x1='75' y1='65' x2='85' y2='75' stroke='#b45309' stroke-width='2.5'/>\n"
    "  <line x1='95' y1='85' x2='105' y2='95' stroke='#b45309' stroke-width='2.5'/>\n"
    "  <line x1='115' y1='105' x2='125' y2='115' stroke='#b45309' stroke-width='2.5'/>\n"
    "  <line x1='135' y1='125' x2='145' y2='135' stroke='#b45309' stroke-width='2.5'/>\n"
    "  <line x1='155' y1='145' x2='165' y2='155' stroke='#b45309' stroke-width='2.5'/>\n"
    "  <!-- Ladder length 10 m -->\n"
    "  <text x='130' y='100' font-family='Times New Roman, serif' font-size='13' fill='#b45309'>10 m</text>\n"
    "  <!-- Ground distance d = 6 m -->\n"
    "  <line x1='60' y1='182' x2='180' y2='182' stroke='#0284c7' stroke-width='1' stroke-dasharray='3,2'/>\n"
    "  <text x='120' y='196' text-anchor='middle' font-family='Times New Roman, serif' font-size='13' fill='#0284c7'>6 m</text>\n"
    "  <!-- Wall height h -->\n"
    "  <line x1='48' y1='50' x2='48' y2='170' stroke='#dc2626' stroke-width='1' stroke-dasharray='3,2'/>\n"
    "  <text x='38' y='115' text-anchor='end' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#dc2626'>h</text>\n"
    "</svg>"
)

# 4. FIG_CUBOID_DIAG: Rectangular cuboid with space diagonal d
FIG_CUBOID_DIAG = (
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 260 200' width='260' height='200'>\n"
    "  <!-- Front face: (50, 90) to (170, 180) -->\n"
    "  <polygon points='50,90 170,90 170,180 50,180' fill='#f8fafc' stroke='#334155' stroke-width='1.8'/>\n"
    "  <!-- Back face top and right visible edges -->\n"
    "  <line x1='90' y1='40' x2='210' y2='40' stroke='#334155' stroke-width='1.8'/>\n"
    "  <line x1='210' y1='40' x2='210' y2='130' stroke='#334155' stroke-width='1.8'/>\n"
    "  <!-- Hidden back edges (dashed) -->\n"
    "  <line x1='90' y1='40' x2='90' y2='130' stroke='#94a3b8' stroke-width='1.5' stroke-dasharray='4,3'/>\n"
    "  <line x1='90' y1='130' x2='210' y2='130' stroke='#94a3b8' stroke-width='1.5' stroke-dasharray='4,3'/>\n"
    "  <line x1='50' y1='180' x2='90' y2='130' stroke='#94a3b8' stroke-width='1.5' stroke-dasharray='4,3'/>\n"
    "  <!-- Oblique connecting edges -->\n"
    "  <line x1='50' y1='90' x2='90' y2='40' stroke='#334155' stroke-width='1.8'/>\n"
    "  <line x1='170' y1='90' x2='210' y2='40' stroke='#334155' stroke-width='1.8'/>\n"
    "  <line x1='170' y1='180' x2='210' y2='130' stroke='#334155' stroke-width='1.8'/>\n"
    "  <!-- Bottom face diagonal (dashed) -->\n"
    "  <line x1='50' y1='180' x2='210' y2='130' stroke='#0284c7' stroke-width='1.5' stroke-dasharray='3,2'/>\n"
    "  <!-- Space diagonal d -->\n"
    "  <line x1='50' y1='180' x2='210' y2='40' stroke='#dc2626' stroke-width='2'/>\n"
    "  <!-- Labels (Mathcad italic) -->\n"
    "  <text x='110' y='196' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='13' fill='#334155'>x</text>\n"
    "  <text x='200' y='165' text-anchor='start' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='13' fill='#334155'>y</text>\n"
    "  <text x='38' y='140' text-anchor='end' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='13' fill='#334155'>z</text>\n"
    "  <text x='130' y='105' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#dc2626'>d</text>\n"
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
    M_add('easy', 'pyth_def',
          'ក្នុងត្រីកោណកែងមួយដែលមានប្រវែងជ្រុងមុំកែង ' + M('a') + ' និង ' + M('b') + ' ហើយអ៊ីប៉ូតេនុស ' + M('c') + ' តើរូបមន្តទ្រឹស្តីបទពីតាក័រណាត្រឹមត្រូវ?',
          M('c^2 = a^2 + b^2'),
          [M('c = a + b'), M('c^2 = a^2 - b^2'), M('a^2 = b^2 + c^2')],
          'ទ្រឹស្តីបទពីតាក័រចែងថា ក្នុងត្រីកោណកែង ការេនៃអ៊ីប៉ូតេនុសស្មើផលបូកការេនៃជ្រុងមុំកែងទាំងពីរ ៖ ' + M('c^2 = a^2 + b^2'),
          FIG_PYTH_TRI)

    M_add('easy', 'calc_hyp_345',
          'ត្រីកោណកែងមួយមានរង្វាស់ជ្រុងមុំកែង ' + M('a = 3\\ \\text{cm}') + ' និង ' + M('b = 4\\ \\text{cm}') + '។ គណនាប្រវែងអ៊ីប៉ូតេនុស ' + M('c') + '។',
          M('5\\ \\text{cm}'),
          [M('6\\ \\text{cm}'), M('7\\ \\text{cm}'), M('25\\ \\text{cm}')],
          'តាមពីតាក័រ ៖ ' + M('c = \sqrt{3^2 + 4^2} = \sqrt{9 + 16} = \sqrt{25} = 5\\ \\text{cm}'))

    M_add('easy', 'calc_hyp_6810',
          'ត្រីកោណកែងមួយមានជ្រុងមុំកែង ' + M('6\\ \\text{cm}') + ' និង ' + M('8\\ \\text{cm}') + '។ រកប្រវែងអ៊ីប៉ូតេនុស។',
          M('10\\ \\text{cm}'),
          [M('12\\ \\text{cm}'), M('14\\ \\text{cm}'), M('100\\ \\text{cm}')],
          M('c = \sqrt{6^2 + 8^2} = \sqrt{36 + 64} = \sqrt{100} = 10\\ \\text{cm}'))

    M_add('easy', 'calc_hyp_5_12',
          'ត្រីកោណកែងមួយមានជ្រុងមុំកែង ' + M('5\\ \\text{dm}') + ' និង ' + M('12\\ \\text{dm}') + '។ គណនាអ៊ីប៉ូតេនុស។',
          M('13\\ \\text{dm}'),
          [M('15\\ \\text{dm}'), M('17\\ \\text{dm}'), M('169\\ \\text{dm}')],
          M('c = \sqrt{5^2 + 12^2} = \sqrt{25 + 144} = \sqrt{169} = 13\\ \\text{dm}'))

    M_add('easy', 'calc_leg_10_6',
          'ត្រីកោណកែងមួយមានអ៊ីប៉ូតេនុស ' + M('c = 10\\ \\text{cm}') + ' និងជ្រុងមុំកែងមួយ ' + M('a = 6\\ \\text{cm}') + '។ គណនាជ្រុងមុំកែងមួយទៀត ' + M('b') + '។',
          M('8\\ \\text{cm}'),
          [M('4\\ \\text{cm}'), M('12\\ \\text{cm}'), M('16\\ \\text{cm}')],
          M('b = \sqrt{c^2 - a^2} = \sqrt{10^2 - 6^2} = \sqrt{100 - 36} = \sqrt{64} = 8\\ \\text{cm}'))

    M_add('easy', 'calc_leg_15_9',
          'ត្រីកោណកែង ' + M('ABC') + ' កែងត្រង់ ' + M('A') + ' មាន ' + M('BC = 15\\ \\text{cm}') + ' និង ' + M('AB = 9\\ \\text{cm}') + '។ គណនា ' + M('AC') + '។',
          M('12\\ \\text{cm}'),
          [M('6\\ \\text{cm}'), M('10\\ \\text{cm}'), M('16\\ \\text{cm}')],
          M('AC = \sqrt{BC^2 - AB^2} = \sqrt{225 - 81} = \sqrt{144} = 12\\ \\text{cm}'))

    M_add('easy', 'square_diag_formula',
          'ការេមួយមានរង្វាស់ជ្រុង ' + M('a') + '។ តើប្រវែងអង្កត់ទ្រូង ' + M('d') + ' នៃការេស្មើនឹងប៉ុន្មាន?',
          M('d = a\sqrt{2}'),
          [M('d = 2a'), M('d = a\sqrt{3}'), M('d = \\dfrac{a}{\sqrt{2}}')],
          M('d^2 = a^2 + a^2 = 2a^2 \\Rightarrow d = \sqrt{2a^2} = a\sqrt{2}'))

    M_add('easy', 'rec_diag_calc',
          'ចតុកោណកែងមួយមានបណ្តោយ ' + M('8\\ \\text{cm}') + ' និងទទឹង ' + M('6\\ \\text{cm}') + '។ គណនាប្រវែងអង្កត់ទ្រូង។',
          M('10\\ \\text{cm}'),
          [M('14\\ \\text{cm}'), M('12\\ \\text{cm}'), M('48\\ \\text{cm}')],
          M('d = \sqrt{8^2 + 6^2} = \sqrt{64 + 36} = \sqrt{100} = 10\\ \\text{cm}'))

    M_add('easy', 'converse_ident',
          'ក្នុងចំណោមប្រវែងជ្រុងទាំង 3 ខាងក្រោម តើមួយណាជាជ្រុងនៃត្រីកោណកែង?',
          M('3,\\ 4,\\ 5'),
          [M('2,\\ 3,\\ 4'), M('4,\\ 5,\\ 6'), M('5,\\ 6,\\ 7')],
          M('3^2 + 4^2 = 9 + 16 = 25 = 5^2') + ' ដូចនេះ ' + M('(3, 4, 5)') + ' ជាជ្រុងនៃត្រីកោណកែង')

    M_add('easy', 'proof_square_side',
          'ក្នុងការស្រាយបញ្ជាក់ទ្រឹស្តីបទពីតាក័រដោយផ្គុំត្រីកោណកែង 4 ដែលមានជ្រុងមុំកែង ' + M('a') + ' និង ' + M('b') + ' ជុំវិញការេកណ្តាល ' + M('c^2') + ' តើការេធំខាងក្រៅមានរង្វាស់ជ្រុងស្មើនឹងប៉ុន្មាន?',
          M('a + b'),
          [M('ab'), M('c'), M('\sqrt{a^2 + b^2}')],
          'ការេធំខាងក្រៅផ្គុំដោយជ្រុង ' + M('a') + ' និង ' + M('b') + ' ដូច្នេះជ្រុងរបស់វាគឺ ' + M('a + b'),
          FIG_PYTH_PROOF)

    # ==========================================
    # 2. MCQ MEDIUM (14 target)
    # ==========================================
    M_add('medium', 'calc_hyp_8_15',
          'ត្រីកោណកែងមួយមានជ្រុងមុំកែង ' + M('8\\ \\text{cm}') + ' និង ' + M('15\\ \\text{cm}') + '។ គណនាអ៊ីប៉ូតេនុស។',
          M('17\\ \\text{cm}'),
          [M('16\\ \\text{cm}'), M('19\\ \\text{cm}'), M('23\\ \\text{cm}')],
          M('c = \sqrt{8^2 + 15^2} = \sqrt{64 + 225} = \sqrt{289} = 17\\ \\text{cm}'))

    M_add('medium', 'calc_leg_25_7',
          'ត្រីកោណកែងមួយមានអ៊ីប៉ូតេនុស ' + M('25\\ \\text{m}') + ' និងជ្រុងមុំកែងមួយ ' + M('7\\ \\text{m}') + '។ គណនាជ្រុងមុំកែងមួយទៀត។',
          M('24\\ \\text{m}'),
          [M('22\\ \\text{m}'), M('20\\ \\text{m}'), M('18\\ \\text{m}')],
          M('b = \sqrt{25^2 - 7^2} = \sqrt{625 - 49} = \sqrt{576} = 24\\ \\text{m}'))

    M_add('medium', 'calc_leg_26_10',
          'ត្រីកោណកែង ' + M('ABC') + ' កែងត្រង់ ' + M('B') + ' មាន ' + M('AC = 26\\ \\text{cm}') + ' និង ' + M('BC = 10\\ \\text{cm}') + '។ គណនា ' + M('AB') + '។',
          M('24\\ \\text{cm}'),
          [M('22\\ \\text{cm}'), M('20\\ \\text{cm}'), M('16\\ \\text{cm}')],
          M('AB = \sqrt{26^2 - 10^2} = \sqrt{676 - 100} = \sqrt{576} = 24\\ \\text{cm}'))

    M_add('medium', 'calc_iso_right_hyp',
          'ត្រីកោណកែងសមបាតមួយមានជ្រុងមុំកែងស្មើគ្នា ' + M('a = b = 5\\ \\text{cm}') + '។ គណនាប្រវែងអ៊ីប៉ូតេនុស។',
          M('5\sqrt{2}\\ \\text{cm}'),
          [M('10\\ \\text{cm}'), M('5\sqrt{3}\\ \\text{cm}'), M('25\\ \\text{cm}')],
          M('c = \sqrt{5^2 + 5^2} = \sqrt{50} = 5\sqrt{2}\\ \\text{cm}'))

    M_add('medium', 'calc_iso_right_leg',
          'ត្រីកោណកែងសមបាតមួយមានអ៊ីប៉ូតេនុសប្រវែង ' + M('8\sqrt{2}\\ \\text{cm}') + '។ គណនារង្វាស់ជ្រុងមុំកែងនីមួយៗ។',
          M('8\\ \\text{cm}'),
          [M('4\\ \\text{cm}'), M('4\sqrt{2}\\ \\text{cm}'), M('16\\ \\text{cm}')],
          M('c = a\sqrt{2} = 8\sqrt{2} \\Rightarrow a = 8\\ \\text{cm}'))

    M_add('medium', 'diag_square_side',
          'ការេមួយមានប្រវែងអង្កត់ទ្រូង ' + M('12\\ \\text{cm}') + '។ គណនាប្រវែងជ្រុងនៃការេនោះ។',
          M('6\sqrt{2}\\ \\text{cm}'),
          [M('6\\ \\text{cm}'), M('12\sqrt{2}\\ \\text{cm}'), M('3\sqrt{2}\\ \\text{cm}')],
          M('a = \\dfrac{d}{\sqrt{2}} = \\dfrac{12}{\sqrt{2}} = \\dfrac{12\sqrt{2}}{2} = 6\sqrt{2}\\ \\text{cm}'))

    M_add('medium', 'rhombus_side_from_diag',
          'ចតុកោណស្មើមួយមានអង្កត់ទ្រូងទាំងពីរប្រវែង ' + M('16\\ \\text{cm}') + ' និង ' + M('12\\ \\text{cm}') + '។ គណនាប្រវែងជ្រុងនៃចតុកោណស្មើ។',
          M('10\\ \\text{cm}'),
          [M('14\\ \\text{cm}'), M('8\\ \\text{cm}'), M('20\\ \\text{cm}')],
          'អង្កត់ទ្រូងចតុកោណស្មើកាត់គ្នាកែងត្រង់ចំណុចកណ្តាល ៖ ' + M('a = \sqrt{8^2 + 6^2} = \sqrt{64 + 36} = 10\\ \\text{cm}'))

    M_add('medium', 'ladder_calc',
          'ជណ្តើរមួយប្រវែង ' + M('10\\ \\text{m}') + ' ផ្អែកលើជញ្ជាំងអគារដោយគល់ជណ្តើរនៅចម្ងាយ ' + M('6\\ \\text{m}') + ' ពីជញ្ជាំង។ តើចុងជណ្តើរប៉ះជញ្ជាំងកម្ពស់ប៉ុន្មានពីដី?',
          M('8\\ \\text{m}'),
          [M('7\\ \\text{m}'), M('9\\ \\text{m}'), M('4\\ \\text{m}')],
          M('h = \sqrt{10^2 - 6^2} = \sqrt{100 - 36} = \sqrt{64} = 8\\ \\text{m}'),
          FIG_LADDER_WALL)

    M_add('medium', 'converse_triple_13',
          'តើត្រីកោណដែលមានរង្វាស់ជ្រុង ' + M('5\\ \\text{cm},\\ 12\\ \\text{cm},\\ 13\\ \\text{cm}') + ' ជាប្រភេទត្រីកោណអ្វី?',
          'ត្រីកោណកែង',
          ['ត្រីកោណស្រួច', 'ត្រីកោណទាល', 'ត្រីកោណសមបាតមិនកែង'],
          M('5^2 + 12^2 = 25 + 144 = 169 = 13^2') + ' តាមទ្រឹស្តីបទច្រាសពីតាក័រ វាជាត្រីកោណកែង')

    M_add('medium', 'converse_obtuse',
          'ត្រីកោណមួយមានរង្វាស់ជ្រុង ' + M('4\\ \\text{cm},\\ 6\\ \\text{cm},\\ 8\\ \\text{cm}') + '។ តើត្រីកោណនេះជាប្រភេទអ្វី?',
          'ត្រីកោណទាល',
          ['ត្រីកោណកែង', 'ត្រីកោណស្រួច', 'ត្រីកោណសម័ង្ស'],
          M('4^2 + 6^2 = 16 + 36 = 52 < 8^2 = 64') + ' ដោយ ' + M('c^2 > a^2 + b^2') + ' នោះវាជាត្រីកោណទាល')

    M_add('medium', 'converse_acute',
          'ត្រីកោណមួយមានរង្វាស់ជ្រុង ' + M('5\\ \\text{cm},\\ 6\\ \\text{cm},\\ 7\\ \\text{cm}') + '។ តើត្រីកោណនេះជាប្រភេទអ្វី?',
          'ត្រីកោណស្រួច',
          ['ត្រីកោណកែង', 'ត្រីកោណទាល', 'ត្រីកោណកែងសមបាត'],
          M('5^2 + 6^2 = 25 + 36 = 61 > 7^2 = 49') + ' ដោយ ' + M('c^2 < a^2 + b^2') + ' នោះវាជាត្រីកោណស្រួច')

    M_add('medium', 'theodorus_spiral',
          'ក្នុងគំនូសគូសបន្តបន្ទាប់ (កង្ហារពីតាក័រ) ៖ ត្រីកោណកែងទី១ មានជ្រុង ' + M('1') + ' និង ' + M('1') + ' នាំឱ្យអ៊ីប៉ូតេនុស ' + M('\sqrt{2}') + '។ ត្រីកោណកែងទី២ មានជ្រុង ' + M('\sqrt{2}') + ' និង ' + M('1') + '។ គណនាអ៊ីប៉ូតេនុសនៃត្រីកោណទី២។',
          M('\sqrt{3}'),
          [M('\sqrt{5}'), M('2'), M('\sqrt{2}')],
          M('x = \sqrt{(\sqrt{2})^2 + 1^2} = \sqrt{2 + 1} = \sqrt{3}'))

    M_add('medium', 'dist_two_points',
          'ក្នុងប្លង់កូអរដោនេ រកចម្ងាយរវាងចំណុច ' + M('A(1, 2)') + ' និង ' + M('B(4, 6)') + '។',
          M('5'),
          [M('7'), M('\sqrt{7}'), M('25')],
          M('AB = \sqrt{(4-1)^2 + (6-2)^2} = \sqrt{3^2 + 4^2} = \sqrt{9 + 16} = 5'))

    M_add('medium', 'cube_diagonal_formula',
          'គូបមួយមានរង្វាស់គែម ' + M('a') + '។ តើប្រវែងអង្កត់ទ្រូងនៃគូបស្មើនឹងប៉ុន្មាន?',
          M('a\sqrt{3}'),
          [M('a\sqrt{2}'), M('3a'), M('\sqrt{3a}')],
          'អង្កត់ទ្រូងបាតគឺ ' + M('d_1 = a\sqrt{2}') + ' នាំឱ្យអង្កត់ទ្រូងគូប ' + M('d = \sqrt{d_1^2 + a^2} = \sqrt{2a^2 + a^2} = a\sqrt{3}'))

    # ==========================================
    # 3. MCQ HARD (7 target)
    # ==========================================
    M_add('hard', 'cuboid_diag_calc',
          'ប្រលេឡេពីប៉ែតកែងមួយមានវិមាត្របណ្តោយ ' + M('12\\ \\text{cm}') + ', ទទឹង ' + M('4\\ \\text{cm}') + ' និងកម្ពស់ ' + M('3\\ \\text{cm}') + '។ គណនាប្រវែងអង្កត់ទ្រូងនៃប្រលេឡេពីប៉ែតនោះ។',
          M('13\\ \\text{cm}'),
          [M('15\\ \\text{cm}'), M('19\\ \\text{cm}'), M('\sqrt{160}\\ \\text{cm}')],
          M('d = \sqrt{12^2 + 4^2 + 3^2} = \sqrt{144 + 16 + 9} = \sqrt{169} = 13\\ \\text{cm}'),
          FIG_CUBOID_DIAG)

    M_add('hard', 'cube_edge_from_diag',
          'គូបមួយមានប្រវែងអង្កត់ទ្រូង ' + M('d = 6\sqrt{3}\\ \\text{cm}') + '។ គណនាផ្ទៃក្រឡាសរុបនៃគូបនោះ។',
          M('216\\ \\text{cm}^2'),
          [M('36\\ \\text{cm}^2'), M('108\\ \\text{cm}^2'), M('144\\ \\text{cm}^2')],
          M('d = a\sqrt{3} = 6\sqrt{3} \\Rightarrow a = 6\\ \\text{cm}') + ' ផ្ទៃសរុប ៖ ' + M('S = 6a^2 = 6 \\times 36 = 216\\ \\text{cm}^2'))

    M_add('hard', 'right_tri_altitude',
          'ត្រីកោណ ' + M('ABC') + ' កែងត្រង់ ' + M('A') + ' មាន ' + M('AB = 12\\ \\text{cm}') + ' និង ' + M('AC = 16\\ \\text{cm}') + '។ គណនាកម្ពស់ ' + M('AH') + ' គូសលើអ៊ីប៉ូតេនុស ' + M('BC') + '។',
          M('9.6\\ \\text{cm}'),
          [M('10\\ \\text{cm}'), M('8.4\\ \\text{cm}'), M('11.2\\ \\text{cm}')],
          M('BC = \sqrt{12^2 + 16^2} = 20\\ \\text{cm}') + '។ តាមផ្ទៃក្រឡា ៖ ' + M('AH = \\dfrac{AB \\times AC}{BC} = \\dfrac{12 \\times 16}{20} = 9.6\\ \\text{cm}'))

    M_add('hard', 'right_tri_projection',
          'ត្រីកោណ ' + M('ABC') + ' កែងត្រង់ ' + M('A') + ' មាន ' + M('AB = 12\\ \\text{cm}') + ', ' + M('AC = 16\\ \\text{cm}') + ' និងកម្ពស់ ' + M('AH') + ' (' + M('H \in BC') + ')។ គណនាប្រវែងចំណោល ' + M('BH') + '។',
          M('7.2\\ \\text{cm}'),
          [M('8\\ \\text{cm}'), M('12.8\\ \\text{cm}'), M('6.4\\ \\text{cm}')],
          M('BC = 20\\ \\text{cm}') + '។ តាមទំនាក់ទំនងក្នុងត្រីកោណកែង ៖ ' + M('AB^2 = BH \\times BC \\Rightarrow BH = \\dfrac{144}{20} = 7.2\\ \\text{cm}'))

    M_add('hard', 'equilateral_altitude',
          'ត្រីកោណសម័ង្សមួយមានរង្វាស់ជ្រុង ' + M('8\\ \\text{cm}') + '។ គណនាកម្ពស់នៃត្រីកោណសម័ង្សនោះ។',
          M('4\sqrt{3}\\ \\text{cm}'),
          [M('4\\ \\text{cm}'), M('6\\ \\text{cm}'), M('8\sqrt{3}\\ \\text{cm}')],
          'កម្ពស់បំបែកជាត្រីកោណកែងមានជ្រុងមុំកែង ' + M('4\\ \\text{cm}') + ' និងអ៊ីប៉ូតេនុស ' + M('8\\ \\text{cm}') + ' ៖ ' + M('h = \sqrt{8^2 - 4^2} = \sqrt{64 - 16} = \sqrt{48} = 4\sqrt{3}\\ \\text{cm}'))

    M_add('hard', 'isosceles_altitude',
          'ត្រីកោណសមបាត ' + M('ABC') + ' មាន ' + M('AB = AC = 13\\ \\text{cm}') + ' និងបាត ' + M('BC = 10\\ \\text{cm}') + '។ គណនាផ្ទៃក្រឡានៃត្រីកោណ ' + M('ABC') + '។',
          M('60\\ \\text{cm}^2'),
          [M('65\\ \\text{cm}^2'), M('120\\ \\text{cm}^2'), M('130\\ \\text{cm}^2')],
          'កម្ពស់ ' + M('AH') + ' ធ្លាក់ចំកណ្តាលបាត ៖ ' + M('BH = 5\\ \\text{cm}') + ' នាំឱ្យ ' + M('AH = \sqrt{13^2 - 5^2} = 12\\ \\text{cm}') + '។ ផ្ទៃ ៖ ' + M('S = \\dfrac{10 \\times 12}{2} = 60\\ \\text{cm}^2'))

    M_add('hard', 'trapezoid_altitude_pyth',
          'ចតុកោណព្នាយសមបាត ' + M('ABCD') + ' មានបាតតូច ' + M('AB = 6\\ \\text{cm}') + ', បាតធំ ' + M('CD = 16\\ \\text{cm}') + ' និងជ្រុងទ្រេត ' + M('AD = BC = 13\\ \\text{cm}') + '។ គណនាកម្ពស់ ' + M('h') + ' នៃចតុកោណព្នាយ។',
          M('12\\ \\text{cm}'),
          [M('10\\ \\text{cm}'), M('11\\ \\text{cm}'), M('15\\ \\text{cm}')],
          'ចំណោលកែងលើបាតធំ ៖ ' + M('x = \\dfrac{16 - 6}{2} = 5\\ \\text{cm}') + ' នាំឱ្យកម្ពស់ ' + M('h = \sqrt{13^2 - 5^2} = \sqrt{169 - 25} = 12\\ \\text{cm}'))

    # ==========================================
    # 4. MCQ PISA (5 target)
    # ==========================================
    M_add('pisa', 'wardrobe_clearance',
          'ទូខោអាវមួយមានកម្ពស់ ' + M('2.4\\ \\text{m}') + ' និងជម្រៅ ' + M('0.7\\ \\text{m}') + '។ គេត្រូវផ្តេកទូលើកម្រាលដើម្បីដំឡើង រួចលើកបញ្ឈរឡើងវិញ។ បើពិដានបន្ទប់មានកម្ពស់ ' + M('2.45\\ \\text{m}') + ' តើទូនោះអាចលើកបញ្ឈរឡើងវិញបានឬទេ?',
          'មិនបានទេ ព្រោះអង្កត់ទ្រូងទូគឺ ' + M('2.5\\ \\text{m} > 2.45\\ \\text{m}'),
          ['បាន ព្រោះកម្ពស់ទូ ' + M('2.4\\ \\text{m} < 2.45\\ \\text{m}'),
           'មិនបានទេ ព្រោះផលបូកវិមាត្រ ' + M('3.1\\ \\text{m} > 2.45\\ \\text{m}'),
           'បាន ព្រោះជម្រៅទូត្រឹមតែ ' + M('0.7\\ \\text{m}')],
          'ពេលលើកបញ្ឈរ ចម្ងាយខ្ពស់បំផុតគឺអង្កត់ទ្រូងទូ ៖ ' + M('d = \sqrt{2.4^2 + 0.7^2} = \sqrt{5.76 + 0.49} = \sqrt{6.25} = 2.5\\ \\text{m} > 2.45\\ \\text{m}'))

    M_add('pisa', 'pathway_shortcut',
          'សួនច្បាររាងចតុកោណកែងមានបណ្តោយ ' + M('80\\ \\text{m}') + ' និងទទឹង ' + M('60\\ \\text{m}') + '។ សិស្សម្នាក់ដើរកាត់តាមផ្លូវអង្កត់ទ្រូងជំនួសឱ្យការដើរតាមគែមទាំងពីរ។ តើគាត់កាត់បន្ថយចម្ងាយដើរបានប៉ុន្មានម៉ែត្រ?',
          M('40\\ \\text{m}'),
          [M('20\\ \\text{m}'), M('50\\ \\text{m}'), M('100\\ \\text{m}')],
          'ដើរតាមគែម ៖ ' + M('80 + 60 = 140\\ \\text{m}') + '។ ដើរតាមអង្កត់ទ្រូង ៖ ' + M('d = \sqrt{80^2 + 60^2} = 100\\ \\text{m}') + '។ ចម្ងាយបន្ថយបាន ៖ ' + M('140 - 100 = 40\\ \\text{m}'))

    M_add('pisa', 'tower_guy_wire',
          'បង្គោលអង់តែនទូរគមនាគមន៍មួយមានកម្ពស់ ' + M('24\\ \\text{m}') + '។ គេចងខ្សែលួសទប់ពីកំពូលបង្គោលទៅដីនៅចម្ងាយ ' + M('7\\ \\text{m}') + ' ពីគល់បង្គោល។ រកប្រវែងខ្សែលួសនោះ។',
          M('25\\ \\text{m}'),
          [M('31\\ \\text{m}'), M('26\\ \\text{m}'), M('28\\ \\text{m}')],
          M('L = \sqrt{24^2 + 7^2} = \sqrt{576 + 49} = \sqrt{625} = 25\\ \\text{m}'))

    M_add('pisa', 'tv_diagonal',
          'កញ្ចក់ទូរទស្សន៍មួយមានទទឹង ' + M('80\\ \\text{cm}') + ' និងបណ្តោយ ' + M('60\\ \\text{cm}') + '។ គណនាប្រវែងអង្កត់ទ្រូងនៃកញ្ចក់ទូរទស្សន៍នោះគិតជាសង់ទីម៉ែត្រ។',
          M('100\\ \\text{cm}'),
          [M('140\\ \\text{cm}'), M('120\\ \\text{cm}'), M('90\\ \\text{cm}')],
          M('d = \sqrt{80^2 + 60^2} = \sqrt{6400 + 3600} = \sqrt{10000} = 100\\ \\text{cm}'))

    M_add('pisa', 'airplane_flight',
          'យន្តហោះពីរហោះចេញពីចំណុច ' + M('O') + ' ដំណាលគ្នាតាមទិសពីរដែលកែងគ្នា។ យន្តហោះទី១ ហោះបានចម្ងាយ ' + M('300\\ \\text{km}') + ' និងយន្តហោះទី២ ហោះបាន ' + M('400\\ \\text{km}') + '។ តើយន្តហោះទាំងពីរនៅឃ្លាតពីគ្នាចម្ងាយប៉ុន្មាន?',
          M('500\\ \\text{km}'),
          [M('700\\ \\text{km}'), M('600\\ \\text{km}'), M('450\\ \\text{km}')],
          M('d = \sqrt{300^2 + 400^2} = \sqrt{90000 + 160000} = \sqrt{250000} = 500\\ \\text{km}'))

    # ==========================================
    # 5. WRITING EASY (1 target, 5 pts total)
    # ==========================================
    W('easy', 'wr_pyth_basic',
      'ត្រីកោណ ' + M('ABC') + ' កែងត្រង់ ' + M('A') + ' មានជ្រុងមុំកែង ' + M('AB = 9\\ \\text{cm}') + ' និង ' + M('AC = 12\\ \\text{cm}') + '។\n'
      'ក. សរសេររូបមន្តទ្រឹស្តីបទពីតាក័រសម្រាប់ត្រីកោណនេះ។\n'
      'ខ. គណនាប្រវែងអ៊ីប៉ូតេនុស ' + M('BC') + '។', [
          ('ក. រូបមន្តទ្រឹស្តីបទពីតាក័រ ៖ ' + M('BC^2 = AB^2 + AC^2'), 2),
          ('ខ. ជំនួសតម្លៃ ៖ ' + M('BC^2 = 9^2 + 12^2 = 81 + 144 = 225'), 2),
          ('ទាញបាន ' + M('BC = \sqrt{225} = 15\\ \\text{cm}'), 1)], FIG_PYTH_TRI)

    # ==========================================
    # 6. WRITING MEDIUM (4 target, 5 pts total each)
    # ==========================================
    W('medium', 'wr_converse_proof',
      'គេឱ្យត្រីកោណ ' + M('MNP') + ' ដែលមានរង្វាស់ជ្រុង ' + M('MN = 7\\ \\text{cm}') + ', ' + M('NP = 24\\ \\text{cm}') + ' និង ' + M('MP = 25\\ \\text{cm}') + '។\n'
      'ក. គណនា ' + M('MN^2 + NP^2') + ' និង ' + M('MP^2') + '។\n'
      'ខ. ប្រៀបធៀបតម្លៃទាំងពីរ រួចសន្និដ្ឋានពីប្រភេទត្រីកោណ ' + M('MNP') + ' និងបញ្ជាក់ថាតើវាកែងត្រង់កំពូលណា។', [
          ('ក. គណនា ៖ ' + M('MN^2 + NP^2 = 7^2 + 24^2 = 49 + 576 = 625'), 2),
          ('គណនា ៖ ' + M('MP^2 = 25^2 = 625'), 1),
          ('ខ. ដោយ ' + M('MP^2 = MN^2 + NP^2 = 625') + ' តាមទ្រឹស្តីបទច្រាសពីតាក័រ ត្រីកោណ ' + M('MNP') + ' ជាត្រីកោណកែងត្រង់កំពូល ' + M('N'), 2)])

    W('medium', 'wr_square_diag',
      'ការេ ' + M('ABCD') + ' មួយមានរង្វាស់ជ្រុង ' + M('AB = 8\\ \\text{cm}') + '។\n'
      'ក. គណនាប្រវែងអង្កត់ទ្រូង ' + M('AC') + ' ជាទម្រង់រ៉ាឌីកាល់ ' + M('a\sqrt{2}') + '។\n'
      'ខ. គណនាផ្ទៃក្រឡានៃការេតាមពីររបៀប ៖ តាមជ្រុង និងតាមអង្កត់ទ្រូង (' + M('S = \\dfrac{d^2}{2}') + ') រួចផ្ទៀងផ្ទាត់ថាលទ្ធផលដូចគ្នា។', [
          ('ក. ត្រីកោណ ' + M('ABC') + ' កែងត្រង់ ' + M('B') + ' ៖ ' + M('AC = \sqrt{8^2 + 8^2} = \sqrt{64 \\times 2} = 8\sqrt{2}\\ \\text{cm}'), 2),
          ('ខ. របៀបទី១ តាមជ្រុង ៖ ' + M('S = 8^2 = 64\\ \\text{cm}^2'), 1),
          ('របៀបទី២ តាមអង្កត់ទ្រូង ៖ ' + M('S = \\dfrac{(8\sqrt{2})^2}{2} = \\dfrac{64 \\times 2}{2} = 64\\ \\text{cm}^2') + ' (លទ្ធផលដូចគ្នា)', 2)])

    W('medium', 'wr_ladder_problem',
      'ជណ្តើរមួយមានប្រវែង ' + M('8\\ \\text{m}') + ' ផ្អែកលើជញ្ជាំងអគារដោយគល់ជណ្តើរនៅចម្ងាយ ' + M('2\\ \\text{m}') + ' ពីជញ្ជាំង។\n'
      'ក. សង់រូបគំរូនៃត្រីកោណកែងតំណាងឱ្យស្ថានភាពនេះ។\n'
      'ខ. គណនាកម្ពស់ ' + M('h') + ' ដែលចុងជណ្តើរប៉ះជញ្ជាំងជាទម្រង់រ៉ាឌីកាល់សម្រួល និងជាតម្លៃប្រហែល (យក ' + M('\sqrt{15} \approx 3.87') + ')។', [
          ('ក. ជញ្ជាំងកែងនឹងដី បង្កើតបានត្រីកោណកែងមានអ៊ីប៉ូតេនុស ' + M('L = 8\\ \\text{m}') + ' និងបាត ' + M('d = 2\\ \\text{m}'), 1),
          ('ខ. តាមទ្រឹស្តីបទពីតាក័រ ៖ ' + M('h^2 = 8^2 - 2^2 = 64 - 4 = 60'), 2),
          ('ទាញបាន ' + M('h = \sqrt{60} = 2\sqrt{15}\\ \\text{m} \approx 2 \\times 3.87 = 7.74\\ \\text{m}'), 2)], FIG_LADDER_WALL)

    W('medium', 'wr_rhombus_props',
      'ចតុកោណស្មើ ' + M('ABCD') + ' មានអង្កត់ទ្រូងកាត់គ្នាកែងត្រង់ ' + M('O') + ' ដោយ ' + M('AC = 24\\ \\text{cm}') + ' និង ' + M('BD = 10\\ \\text{cm}') + '។\n'
      'ក. គណនាប្រវែង ' + M('OA') + ' និង ' + M('OB') + '។\n'
      'ខ. គណនាប្រវែងជ្រុង ' + M('AB') + ' និងបរិមាត្រនៃចតុកោណស្មើ។', [
          ('ក. អង្កត់ទ្រូងកាត់គ្នាកែងត្រង់ចំណុចកណ្តាល ៖ ' + M('OA = \\dfrac{24}{2} = 12\\ \\text{cm}') + ' និង ' + M('OB = \\dfrac{10}{2} = 5\\ \\text{cm}'), 2),
          ('ខ. ក្នុងត្រីកោណកែង ' + M('OAB') + ' ៖ ' + M('AB = \sqrt{12^2 + 5^2} = \sqrt{144 + 25} = \sqrt{169} = 13\\ \\text{cm}'), 2),
          ('បរិមាត្រនៃចតុកោណស្មើ ៖ ' + M('P = 4 \\times 13 = 52\\ \\text{cm}'), 1)])

    # ==========================================
    # 7. WRITING HARD (4 target, 5 pts total each)
    # ==========================================
    W('hard', 'wr_pyth_proof_full',
      'ពិនិត្យការេធំដែលមានជ្រុង ' + M('(a+b)') + ' ក្នុងរូបខាងស្តាំ ដែលផ្គុំឡើងដោយត្រីកោណកែងចំនួន 4 (ជ្រុងមុំកែង ' + M('a, b') + ') និងការេខាងក្នុងដែលមានជ្រុង ' + M('c') + '។\n'
      'ក. សរសេរកន្សោមផ្ទៃក្រឡាការេធំជាអនុគមន៍នៃ ' + M('a') + ' និង ' + M('b') + '។\n'
      'ខ. សរសេរផលបូកផ្ទៃក្រឡានៃត្រីកោណកែងទាំង 4 និងការេកណ្តាល។\n'
      'គ. ទាញស្រាយបញ្ជាក់ទ្រឹស្តីបទពីតាក័រ ' + M('c^2 = a^2 + b^2') + '។', [
          ('ក. ផ្ទៃក្រឡាការេធំ ៖ ' + M('S_{\\text{ធំ}} = (a+b)^2 = a^2 + 2ab + b^2'), 2),
          ('ខ. ផ្ទៃត្រីកោណកែងទាំងបួន ៖ ' + M('4 \\times \\dfrac{1}{2}ab = 2ab') + '; ផ្ទៃការេកណ្តាល ៖ ' + M('c^2'), 1),
          ('គ. ដោយ ' + M('S_{\\text{ធំ}} = c^2 + 2ab \\Rightarrow a^2 + 2ab + b^2 = c^2 + 2ab \\Rightarrow c^2 = a^2 + b^2'), 2)], FIG_PYTH_PROOF)

    W('hard', 'wr_alt_hypotenuse',
      'ត្រីកោណ ' + M('ABC') + ' កែងត្រង់ ' + M('A') + ' មាន ' + M('BC = 20\\ \\text{cm}') + ' និង ' + M('AC = 16\\ \\text{cm}') + '។ ' + M('AH') + ' ជាកម្ពស់គូសលើ ' + M('BC') + '។\n'
      'ក. គណនារង្វាស់ជ្រុង ' + M('AB') + '។\n'
      'ខ. គណនាកម្ពស់ ' + M('AH') + '។\n'
      'គ. គណនាប្រវែងកំណាត់ ' + M('BH') + ' និង ' + M('HC') + '។', [
          ('ក. ' + M('AB = \sqrt{BC^2 - AC^2} = \sqrt{20^2 - 16^2} = \sqrt{400 - 256} = \sqrt{144} = 12\\ \\text{cm}'), 1),
          ('ខ. តាមផ្ទៃក្រឡា ' + M('S = \\dfrac{AB \\times AC}{2} = \\dfrac{BC \\times AH}{2} \\Rightarrow AH = \\dfrac{12 \\times 16}{20} = 9.6\\ \\text{cm}'), 2),
          ('គ. ' + M('BH = \sqrt{12^2 - 9.6^2} = 7.2\\ \\text{cm}') + ' និង ' + M('HC = 20 - 7.2 = 12.8\\ \\text{cm}'), 2)])

    W('hard', 'wr_cube_space_diag',
      'គេឱ្យគូបមួយដែលមានរង្វាស់គែម ' + M('a = 4\\ \\text{cm}') + '។\n'
      'ក. គណនាប្រវែងអង្កត់ទ្រូងបាត ' + M('d_1') + '។\n'
      'ខ. បង្ហាញថាអង្កត់ទ្រូងគូប ' + M('d') + ' ផ្ទៀងផ្ទាត់ ' + M('d = a\sqrt{3}') + ' រួចគណនាតម្លៃពិតប្រាកដរបស់វា។', [
          ('ក. អង្កត់ទ្រូងបាត ៖ ' + M('d_1 = \sqrt{a^2 + a^2} = \sqrt{4^2 + 4^2} = 4\sqrt{2}\\ \\text{cm}'), 2),
          ('ខ. ត្រីកោណកែងបង្កើតដោយ ' + M('d_1') + ', កម្ពស់ ' + M('a') + ' និងអង្កត់ទ្រូង ' + M('d') + ' ៖ ' + M('d = \sqrt{d_1^2 + a^2} = \sqrt{(a\sqrt{2})^2 + a^2} = \sqrt{3a^2} = a\sqrt{3}'), 2),
          ('ជំនួស ' + M('a = 4\\ \\text{cm} \\Rightarrow d = 4\sqrt{3}\\ \\text{cm}'), 1)])

    W('hard', 'wr_coord_distance',
      'ក្នុងតម្រុយអ័ក្សអរតូណរម៉េ គេឱ្យចំណុច ' + M('A(-2, 9)') + ' និង ' + M('B(10, 4)') + '។\n'
      'ក. រកប្រវែងចំណោលដេក ' + M('|x_B - x_A|') + ' និងចំណោលឈរ ' + M('|y_B - y_A|') + '។\n'
      'ខ. គណនាចម្ងាយ ' + M('AB') + '។\n'
      'គ. បើចំណុច ' + M('C(10, 9)') + ' បង្កើតបានត្រីកោណ ' + M('ABC') + ' បញ្ជាក់ថាតើត្រីកោណ ' + M('ABC') + ' ជាប្រភេទត្រីកោណអ្វី?', [
          ('ក. ចំណោលដេក ៖ ' + M('|10 - (-2)| = 12') + '; ចំណោលឈរ ៖ ' + M('|4 - 9| = 5'), 2),
          ('ខ. តាមរូបមន្តចម្ងាយ (ពីតាក័រ) ៖ ' + M('AB = \sqrt{12^2 + 5^2} = \sqrt{144 + 25} = \sqrt{169} = 13'), 2),
          ('គ. ចំណុច ' + M('C(10, 9)') + ' មាន ' + M('AC = 12, BC = 5') + ' នាំឱ្យ ' + M('AC^2 + BC^2 = 12^2 + 5^2 = 169 = AB^2') + ' ដូចនេះ ' + M('\Delta ABC') + ' កែងត្រង់ ' + M('C'), 1)])

    # ==========================================
    # 8. WRITING PISA (5 target, 5 pts total each)
    # ==========================================
    W('pisa', 'wr_airplane_flight',
      'យន្តហោះពីរហោះចេញពីព្រលានយន្តហោះ ' + M('O') + ' ដំណាលគ្នានៅម៉ោង ' + M('8:00') + ' ព្រឹក ដោយយន្តហោះ ' + M('A') + ' ហោះទៅទិសខាងជើងដោយល្បឿន ' + M('600\\ \\text{km/h}') + ' និងយន្តហោះ ' + M('B') + ' ហោះទៅទិសខាងកើតដោយល្បឿន ' + M('800\\ \\text{km/h}') + '។\n'
      'ក. គណនាចម្ងាយចរនៃយន្តហោះនីមួយៗនៅម៉ោង ' + M('9:30') + ' ព្រឹក (រយៈពេល ' + M('1.5\\ \\text{ម៉ោង}') + ')។\n'
      'ខ. គណនាចម្ងាយរវាងយន្តហោះទាំងពីរនៅម៉ោង ' + M('9:30') + ' ព្រឹក។\n'
      'គ. ពន្យល់ហេតុអ្វីបានជាយើងអាចប្រើទ្រឹស្តីបទពីតាក័រក្នុងករណីនេះ។', [
          ('ក. ចម្ងាយយន្តហោះ ' + M('A') + ' ៖ ' + M('d_A = 600 \\times 1.5 = 900\\ \\text{km}') + '; ចម្ងាយយន្តហោះ ' + M('B') + ' ៖ ' + M('d_B = 800 \\times 1.5 = 1200\\ \\text{km}'), 2),
          ('ខ. ចម្ងាយរវាងយន្តហោះទាំងពីរ ៖ ' + M('AB = \sqrt{900^2 + 1200^2} = \sqrt{810\\,000 + 1\\,440\\,000} = \sqrt{2\\,250\\,000} = 1500\\ \\text{km}'), 2),
          ('គ. ទិសខាងជើងនិងទិសខាងកើតកែងគ្នាបង្កើតបានមុំ ' + M('90^\circ') + ' នាំឱ្យគន្លងហោះហើរ និងចម្ងាយរវាងយន្តហោះទាំងពីរបង្កើតបានជាត្រីកោណកែង', 1)])

    W('pisa', 'wr_equilateral_theorem',
      'គេសង់ត្រីកោណសម័ង្សបីគឺ ' + M('\Delta BCR, \Delta ACQ') + ' និង ' + M('\Delta ABP') + ' លើជ្រុង ' + M('a, b, c') + ' នៃត្រីកោណកែង ' + M('ABC') + ' (កែងត្រង់ ' + M('C') + ') រៀងគ្នា។\n'
      'ក. សរសេររូបមន្តផ្ទៃក្រឡានៃត្រីកោណសម័ង្សដែលមានជ្រុង ' + M('s') + '។\n'
      'ខ. គណនាផ្ទៃក្រឡា ' + M('S_{BCR}, S_{ACQ}') + ' និង ' + M('S_{ABP}') + '។\n'
      'គ. បង្ហាញថា ' + M('S_{ABP} = S_{BCR} + S_{ACQ}') + '។', [
          ('ក. រូបមន្តផ្ទៃត្រីកោណសម័ង្សជ្រុង ' + M('s') + ' គឺ ៖ ' + M('S = \\dfrac{\sqrt{3}}{4}s^2'), 1),
          ('ខ. ផ្ទៃទាំងបី ៖ ' + M('S_{BCR} = \\dfrac{\sqrt{3}}{4}a^2') + ', ' + M('S_{ACQ} = \\dfrac{\sqrt{3}}{4}b^2') + ', ' + M('S_{ABP} = \\dfrac{\sqrt{3}}{4}c^2'), 2),
          ('គ. ផលបូក ៖ ' + M('S_{BCR} + S_{ACQ} = \\dfrac{\sqrt{3}}{4}(a^2 + b^2)') + '។ ដោយ ' + M('a^2 + b^2 = c^2') + ' (ពីតាក័រ) នោះ ' + M('S_{BCR} + S_{ACQ} = \\dfrac{\sqrt{3}}{4}c^2 = S_{ABP}'), 2)])

    W('pisa', 'wr_guy_wire_safety',
      'វិស្វករម្នាក់ត្រូវដំឡើងខ្សែលួសទប់បង្គោលអង់តែនកម្ពស់ ' + M('36\\ \\text{m}') + '។ តាមបទដ្ឋានសុវត្ថិភាព មុំរវាងខ្សែលួសនិងដីត្រូវស្ថិតនៅចន្លោះពី ' + M('45^\circ') + ' ទៅ ' + M('60^\circ') + '។ គាត់សម្រេចចងគល់ខ្សែលួសនៅចម្ងាយ ' + M('27\\ \\text{m}') + ' ពីគល់បង្គោល។\n'
      'ក. គណនាប្រវែងខ្សែលួសដែលត្រូវការសម្រាប់ខ្សែមួយខ្សែ។\n'
      'ខ. បើបង្គោលនោះត្រូវការខ្សែលួសទប់ចំនួន 4 ទិសស្មើគ្នា តើត្រូវប្រើខ្សែលួសសរុបប្រវែងប៉ុន្មាន?\n'
      'គ. បើខ្សែលួស ១ ម៉ែត្រមានតម្លៃ ' + M('3.5\$') + ' គណនាថ្លៃទិញខ្សែលួសទាំងអស់។', [
          ('ក. ប្រវែងខ្សែមួយ ៖ ' + M('L = \sqrt{36^2 + 27^2} = \sqrt{1296 + 729} = \sqrt{2025} = 45\\ \\text{m}'), 2),
          ('ខ. ប្រវែងខ្សែសរុបសម្រាប់ 4 ទិស ៖ ' + M('45 \\times 4 = 180\\ \\text{m}'), 2),
          ('គ. ថ្លៃខ្សែលួសសរុប ៖ ' + M('180 \\times 3.5 = 630\$'), 1)])

    W('pisa', 'wr_door_passage',
      'ទ្វារបន្ទប់មួយមានរាងចតុកោណកែងទទឹង ' + M('1\\ \\text{m}') + ' និងកម្ពស់ ' + M('2\\ \\text{m}') + '។ ជាងម្នាក់ចង់សែងបន្ទះក្តារបន្ទះមូលមួយផ្ទាំងដែលមានអង្កត់ផ្ចិត ' + M('2.2\\ \\text{m}') + ' ចូលក្នុងបន្ទប់។\n'
      'ក. គណនាប្រវែងអង្កត់ទ្រូងនៃទ្វារបន្ទប់ (យក ' + M('\sqrt{5} \approx 2.236\\ \\text{m}') + ')។\n'
      'ខ. តើជាងនោះអាចសែងបន្ទះក្តារមូលនោះកាត់តាមទ្វារដោយផ្អៀងតាមអង្កត់ទ្រូងបានឬទេ? ពន្យល់។', [
          ('ក. ប្រវែងអង្កត់ទ្រូងទ្វារ ៖ ' + M('d = \sqrt{1^2 + 2^2} = \sqrt{1 + 4} = \sqrt{5}\\ \\text{m} \approx 2.236\\ \\text{m}'), 3),
          ('ខ. បាន ព្រោះបន្ទះក្តារមូលមានអង្កត់ផ្ចិត ' + M('2.2\\ \\text{m} < 2.236\\ \\text{m}') + ' (អង្កត់ទ្រូងទ្វារ) ដូច្នេះបើផ្អៀងបន្ទះក្តារតាមអង្កត់ទ្រូងទ្វារ គឺអាចឆ្លងកាត់បាន', 2)])

    W('pisa', 'wr_city_distance',
      'នៅលើប្លង់ផែនទីមួយ ទីក្រុង ' + M('A') + ' ស្ថិតនៅចម្ងាយ ' + M('20\\ \\text{km}') + ' ខាងលិច និង ' + M('9\\ \\text{km}') + ' ខាងជើងពីចំណុចកណ្តាល ' + M('O') + '។ ទីក្រុង ' + M('B') + ' ស្ថិតនៅ ' + M('15\\ \\text{km}') + ' ខាងកើត និង ' + M('21\\ \\text{km}') + ' ខាងត្បូងពី ' + M('O') + '។\n'
      'ក. គណនាចម្ងាយពី ' + M('O') + ' ទៅទីក្រុង ' + M('A') + ' (' + M('OA') + ')។\n'
      'ខ. គណនាចម្ងាយពី ' + M('O') + ' ទៅទីក្រុង ' + M('B') + ' (' + M('OB') + ')។\n'
      'គ. គណនាចម្ងាយត្រង់រវាងទីក្រុង ' + M('A') + ' និងទីក្រុង ' + M('B') + ' (' + M('AB') + ')។', [
          ('ក. ' + M('OA = \sqrt{(-20)^2 + 9^2} = \sqrt{400 + 81} = \sqrt{481}\\ \\text{km} \approx 21.93\\ \\text{km}'), 1),
          ('ខ. ' + M('OB = \sqrt{15^2 + (-21)^2} = \sqrt{225 + 441} = \sqrt{666} = 3\sqrt{74}\\ \\text{km} \approx 25.81\\ \\text{km}'), 2),
          ('គ. ' + M('AB = \sqrt{(15 - (-20))^2 + (-21 - 9)^2} = \sqrt{35^2 + (-30)^2} = \sqrt{1225 + 900} = \sqrt{2125} = 5\sqrt{85}\\ \\text{km} \approx 46.10\\ \\text{km}'), 2)])

    return C
