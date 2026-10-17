"""Bank candidates for Grade 8, Lesson 13: ចតុកោណ (Quadrilaterals)
Covers MoEYS Grade 8 curriculum:
  1. និយមន័យចតុកោណ និងផលបូកមុំក្នុង (Sum of interior angles = 360°)
  2. ចតុកោណព្នាយ (Trapezoid, isosceles & right trapezoids)
  3. ប្រលេឡូក្រាម (Parallelogram properties: sides, opposite angles, consecutive angles, diagonals)
  4. ចតុកោណកែង (Rectangle: 4 right angles, equal diagonals)
  5. ចតុកោណស្មើ (Rhombus: 4 equal sides, perpendicular diagonals, angle bisectors)
  6. ការេ (Square: rectangle + rhombus properties)
  7. ចតុកោណខ្លែង (Kite properties)
  8. PISA & Real-world applications (Gate bracing, parking stalls, tiling, kite design)

Images: Clean vector illustrations, isolated, no background, flat educational textbook style.
Geometry labels use font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic'.
"""
from lib import *

LESSON = "ចតុកោណ"

# --- SVG Illustrations ---

# 1. FIG_PARALLELOGRAM: Parallelogram ABCD with diagonals intersecting at O
FIG_PARALLELOGRAM = (
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 280 160' width='280' height='160'>\n"
    "  <!-- Parallelogram ABCD -->\n"
    "  <polygon points='70,30 240,30 190,130 20,130' fill='#f0fdf4' stroke='#16a34a' stroke-width='2'/>\n"
    "  <!-- Diagonals AC and BD -->\n"
    "  <line x1='70' y1='30' x2='190' y2='130' stroke='#0284c7' stroke-width='1.5' stroke-dasharray='4,3'/>\n"
    "  <line x1='240' y1='30' x2='20' y2='130' stroke='#0284c7' stroke-width='1.5' stroke-dasharray='4,3'/>\n"
    "  <!-- Center intersection O -->\n"
    "  <circle cx='130' cy='80' r='3.5' fill='#dc2626'/>\n"
    "  <!-- Vertex labels (Mathcad italic) -->\n"
    "  <text x='65' y='22' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>A</text>\n"
    "  <text x='248' y='26' text-anchor='start' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>B</text>\n"
    "  <text x='198' y='142' text-anchor='start' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>C</text>\n"
    "  <text x='12' y='142' text-anchor='end' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>D</text>\n"
    "  <text x='138' y='76' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='13' fill='#dc2626'>O</text>\n"
    "  <!-- Equal ticks on AO and OC (single) -->\n"
    "  <line x1='97' y1='52' x2='103' y2='58' stroke='#0284c7' stroke-width='1.4'/>\n"
    "  <line x1='157' y1='102' x2='163' y2='108' stroke='#0284c7' stroke-width='1.4'/>\n"
    "  <!-- Equal ticks on BO and OD (double) -->\n"
    "  <line x1='182' y1='52' x2='188' y2='58' stroke='#0284c7' stroke-width='1.4'/>\n"
    "  <line x1='185' y1='55' x2='191' y2='61' stroke='#0284c7' stroke-width='1.4'/>\n"
    "  <line x1='72' y1='102' x2='78' y2='108' stroke='#0284c7' stroke-width='1.4'/>\n"
    "  <line x1='75' y1='105' x2='81' y2='111' stroke='#0284c7' stroke-width='1.4'/>\n"
    "</svg>"
)

# 2. FIG_TRAPEZOID: Isosceles trapezoid ABCD (AB // CD, AD = BC)
FIG_TRAPEZOID = (
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 260 150' width='260' height='150'>\n"
    "  <!-- Trapezoid ABCD -->\n"
    "  <polygon points='65,30 195,30 235,120 25,120' fill='#eff6ff' stroke='#0284c7' stroke-width='2'/>\n"
    "  <!-- Parallel arrows on AB and CD -->\n"
    "  <polygon points='128,27 136,30 128,33' fill='#0284c7'/>\n"
    "  <polygon points='128,117 136,120 128,123' fill='#0284c7'/>\n"
    "  <!-- Tick marks on legs AD and BC -->\n"
    "  <line x1='42' y1='73' x2='48' y2='77' stroke='#dc2626' stroke-width='1.6'/>\n"
    "  <line x1='212' y1='73' x2='218' y2='77' stroke='#dc2626' stroke-width='1.6'/>\n"
    "  <!-- Base angle arcs -->\n"
    "  <path d='M 45,120 A 20 20 0 0 0 35,100' fill='none' stroke='#16a34a' stroke-width='1.5'/>\n"
    "  <path d='M 215,120 A 20 20 0 0 1 225,100' fill='none' stroke='#16a34a' stroke-width='1.5'/>\n"
    "  <!-- Labels (Mathcad italic) -->\n"
    "  <text x='60' y='22' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>A</text>\n"
    "  <text x='200' y='22' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>B</text>\n"
    "  <text x='245' y='128' text-anchor='start' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>C</text>\n"
    "  <text x='15' y='128' text-anchor='end' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>D</text>\n"
    "</svg>"
)

# 3. FIG_RHOMBUS: Rhombus ABCD with perpendicular diagonals
FIG_RHOMBUS = (
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 240 180' width='240' height='180'>\n"
    "  <!-- Rhombus ABCD -->\n"
    "  <polygon points='120,20 210,90 120,160 30,90' fill='#fefce8' stroke='#ca8a04' stroke-width='2'/>\n"
    "  <!-- Diagonals AC and BD -->\n"
    "  <line x1='120' y1='20' x2='120' y2='160' stroke='#0f172a' stroke-width='1.5'/>\n"
    "  <line x1='30' y1='90' x2='210' y2='90' stroke='#0f172a' stroke-width='1.5'/>\n"
    "  <!-- Right angle at center O -->\n"
    "  <polyline points='120,78 132,78 132,90' fill='none' stroke='#0f172a' stroke-width='1.2'/>\n"
    "  <!-- 4 ticks on sides -->\n"
    "  <line x1='72' y1='52' x2='78' y2='58' stroke='#ca8a04' stroke-width='1.6'/>\n"
    "  <line x1='162' y1='52' x2='168' y2='58' stroke='#ca8a04' stroke-width='1.6'/>\n"
    "  <line x1='162' y1='122' x2='168' y2='128' stroke='#ca8a04' stroke-width='1.6'/>\n"
    "  <line x1='72' y1='122' x2='78' y2='128' stroke='#ca8a04' stroke-width='1.6'/>\n"
    "  <!-- Labels (Mathcad italic) -->\n"
    "  <text x='120' y='14' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>A</text>\n"
    "  <text x='222' y='94' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>B</text>\n"
    "  <text x='120' y='175' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>C</text>\n"
    "  <text x='18' y='94' text-anchor='end' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>D</text>\n"
    "  <text x='134' y='86' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='12' fill='#0f172a'>O</text>\n"
    "</svg>"
)

# 4. FIG_GATE_BRACE: Rectangle gate with diagonal brace
FIG_GATE_BRACE = (
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 220 180' width='220' height='180'>\n"
    "  <!-- Rectangle Frame -->\n"
    "  <rect x='40' y='20' width='140' height='140' fill='#f8fafc' stroke='#0f172a' stroke-width='2'/>\n"
    "  <!-- Diagonal brace -->\n"
    "  <line x1='40' y1='160' x2='180' y2='20' stroke='#dc2626' stroke-width='2.5'/>\n"
    "  <!-- Dimensions -->\n"
    "  <text x='110' y='174' text-anchor='middle' font-family='Times New Roman, serif' font-size='12' fill='#475569'>1.5 m</text>\n"
    "  <text x='25' y='95' text-anchor='middle' font-family='Times New Roman, serif' font-size='12' fill='#475569'>2 m</text>\n"
    "  <!-- Diagonal label (Mathcad italic) -->\n"
    "  <text x='115' y='82' text-anchor='start' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='13' fill='#dc2626'>d = 2.5 m</text>\n"
    "  <!-- Right angle symbols -->\n"
    "  <polyline points='40,146 54,146 54,160' fill='none' stroke='#0f172a' stroke-width='1.2'/>\n"
    "  <polyline points='166,160 166,146 180,146' fill='none' stroke='#0f172a' stroke-width='1.2'/>\n"
    "</svg>"
)

def with_img(q_, s_): q_['img'] = s_; return q_

def cands():
    C = []
    def W(level, sec, stem, steps, img=None):
        q_ = wr(level, sec, stem, steps)
        if img: q_['img'] = img
        C.append(q_)

    # ==========================================
    # 1. MCQ EASY (10 target)
    # ==========================================
    C.append(mcq('easy', 'angle_sum', 'ផលបូករង្វាស់មុំក្នុងទាំងបួននៃចតុកោណមួយស្មើនឹង ៖', M('360^\\circ'), [M('180^\\circ'), M('270^\\circ'), M('540^\\circ')], 'ផលបូកមុំក្នុងនៃចតុកោណមួយស្មើនឹង ' + M('360^\\circ') + ' ជានិច្ច។'))
    C.append(mcq('easy', 'trapezoid', 'ចតុកោណព្នាយជាចតុកោណដែលមាន ៖', M('\\text{ជ្រុងឈមមួយគូស្របគ្នា}'), [M('\\text{ជ្រុងឈមពីរគូស្របគ្នា}'), M('\\text{ជ្រុងទាំងបួនប៉ុនគ្នា}'), M('\\text{មុំទាំងបួនកែង}')], 'តាមនិយមន័យ ចតុកោណព្នាយមានជ្រុងឈមតែមួយគូប៉ុណ្ណោះដែលស្របគ្នា (ហៅថាបាត)។'))
    C.append(mcq('easy', 'parallelogram', 'ក្នុងប្រលេឡូក្រាមមួយ លក្ខណៈនៃជ្រុងឈមគឺ ៖', M('\\text{ស្របគ្នានិងប៉ុនគ្នា}'), [M('\\text{កែងគ្នា}'), M('\\text{មិនប៉ុនគ្នា}'), M('\\text{កាត់គ្នា}')], 'ក្នុងប្រលេឡូក្រាម ជ្រុងឈមទាំងពីរគូស្របគ្នានិងមានប្រវែងប៉ុនគ្នា។'))
    C.append(mcq('easy', 'parallelogram', 'ក្នុងប្រលេឡូក្រាមមួយ លក្ខណៈនៃមុំឈមគឺ ៖', M('\\text{ជាមុំប៉ុនគ្នា}'), [M('\\text{ជាមុំកែង}'), M('\\text{មានផលបូកស្មើ } 90^\\circ'), M('\\text{មិនប៉ុនគ្នា}')], 'ក្នុងប្រលេឡូក្រាម មុំឈមទាំងពីរគូជាមុំប៉ុនគ្នា។'))
    C.append(with_img(mcq('easy', 'parallelogram', 'ក្នុងប្រលេឡូក្រាម អង្កត់ទ្រូងទាំងពីរមានលក្ខណៈ ៖', M('\\text{កាត់គ្នាត្រង់ចំណុចកណ្តាលនៃអង្កត់ទ្រូងនីមួយៗ}'), [M('\\text{កែងគ្នាជានិច្ច}'), M('\\text{មានប្រវែងប៉ុនគ្នាជានិច្ច}'), M('\\text{ស្របគ្នា}')], 'អង្កត់ទ្រូងទាំងពីរនៃប្រលេឡូក្រាមកាត់គ្នាត្រង់ចំណុចកណ្តាលនៃអង្កត់នីមួយៗ។'), FIG_PARALLELOGRAM))
    C.append(mcq('easy', 'rectangle', 'ចតុកោណកែងជាប្រលេឡូក្រាមដែលមាន ៖', M('\\text{មុំកែងមួយ (នាំឱ្យមុំទាំង ៤ ជាមុំកែង)}'), [M('\\text{ជ្រុងទាំង ៤ ប៉ុនគ្នា}'), M('\\text{អង្កត់ទ្រូងកែងគ្នា}'), M('\\text{ជ្រុងឈមមិនស្របគ្នា}')], 'ចតុកោណកែងមានមុំទាំងបួនជាមុំកែង ហើយអង្កត់ទ្រូងទាំងពីរប៉ុនគ្នា។'))
    C.append(mcq('easy', 'rhombus', 'ចតុកោណស្មើជាប្រលេឡូក្រាមដែលមាន ៖', M('\\text{ជ្រុងទាំងបួនមានប្រវែងប៉ុនគ្នា}'), [M('\\text{មុំទាំងបួនកែង}'), M('\\text{អង្កត់ទ្រូងប៉ុនគ្នា}'), M('\\text{ជ្រុងឈមមិនប៉ុនគ្នា}')], 'ចតុកោណស្មើ (Rhombus) មានជ្រុងទាំងបួនប៉ុនគ្នា។'))
    C.append(mcq('easy', 'square', 'ការេជាចតុកោណដែលមាន ៖', M('\\text{ជ្រុងទាំង ៤ ប៉ុនគ្នា និងមុំទាំង ៤ ជាមុំកែង}'), [M('\\text{មុំពីរស្រួច មុំពីរទាល}'), M('\\text{អង្កត់ទ្រូងមិនកែងគ្នា}'), M('\\text{ជ្រុងជាប់គ្នាមិនស្មើគ្នា}')], 'ការេជាចតុកោណកែងផង និងជាចតុកោណស្មើផង។'))
    C.append(with_img(mcq('easy', 'trapezoid', 'ចតុកោណព្នាយសមបាតជាចតុកោណព្នាយដែលមាន ៖', M('\\text{ជ្រុងទ្រេតពីរប៉ុនគ្នា និងមុំបាតប៉ុនគ្នា}'), [M('\\text{មុំទាំងបួនកែង}'), M('\\text{ជ្រុងបាតពីរប៉ុនគ្នា}'), M('\\text{អង្កត់ទ្រូងកែងគ្នា}')], 'ចតុកោណព្នាយសមបាតមានជ្រុងទ្រេតពីរប៉ុនគ្នា មុំបាតប៉ុនគ្នា និងអង្កត់ទ្រូងពីរប៉ុនគ្នា។'), FIG_TRAPEZOID))
    C.append(with_img(mcq('easy', 'rhombus', 'ក្នុងចតុកោណស្មើ អង្កត់ទ្រូងទាំងពីរមានលក្ខណៈ ៖', M('\\text{កែងគ្នាត្រង់ចំណុចកណ្តាល}'), [M('\\text{មានប្រវែងប៉ុនគ្នាជានិច្ច}'), M('\\text{មិនកាត់គ្នា}'), M('\\text{ស្របគ្នា}')], 'អង្កត់ទ្រូងទាំងពីរនៃចតុកោណស្មែកែងគ្នាត្រង់ចំណុចកណ្តាល និងជាបន្ទាត់ពុះមុំ។'), FIG_RHOMBUS))
    C.append(mcq('easy', 'kite', 'ចតុកោណខ្លែងជាចតុកោណដែលមាន ៖', M('\\text{ជ្រុងជាប់គ្នាពីរគូប៉ុនគ្នា}'), [M('\\text{ជ្រុងឈមស្របគ្នា}'), M('\\text{ជ្រុងទាំងបួនប៉ុនគ្នា}'), M('\\text{មុំទាំងបួនស្មើគ្នា}')], 'ចតុកោណខ្លែងមានជ្រុងជាប់គ្នាពីរគូប៉ុនគ្នា។'))
    C.append(mcq('easy', 'rectangle', 'ក្នុងចតុកោណកែង អង្កត់ទ្រូងទាំងពីរមានលក្ខណៈ ៖', M('\\text{មានប្រវែងប៉ុនគ្នា}'), [M('\\text{កែងគ្នាជានិច្ច}'), M('\\text{មិនកាត់គ្នា}'), M('\\text{មានប្រវែងខុសគ្នាជានិច្ច}')], 'អង្កត់ទ្រូងទាំងពីរនៃចតុកោណកែងមានប្រវែងប៉ុនគ្នា។'))

    # ==========================================
    # 2. MCQ MEDIUM (14 target)
    # ==========================================
    C.append(mcq('medium', 'angle_calc', 'ក្នុងចតុកោណ ' + M('ABCD') + ' មាន ' + M('\\angle A = 80^\\circ, \\angle B = 110^\\circ, \\angle C = 75^\\circ') + '។ រង្វាស់មុំ ' + M('\\angle D') + ' ស្មើ ៖', M('95^\\circ'), [M('85^\\circ'), M('105^\\circ'), M('90^\\circ')], M('\\angle D = 360^\\circ - (80^\\circ + 110^\\circ + 75^\\circ) = 360^\\circ - 265^\\circ = 95^\\circ') + '។'))
    C.append(mcq('medium', 'parallelogram', 'ក្នុងប្រលេឡូក្រាម ' + M('ABCD') + ' មានមុំ ' + M('\\angle A = 70^\\circ') + '។ រង្វាស់មុំ ' + M('\\angle B') + ' ស្មើ ៖', M('110^\\circ'), [M('70^\\circ'), M('90^\\circ'), M('120^\\circ')], 'មុំតគ្នាក្នុងប្រលេឡូក្រាមជាមុំជាប់បន្ថែម ៖ ' + M('\\angle B = 180^\\circ - 70^\\circ = 110^\\circ') + '។'))
    C.append(mcq('medium', 'parallelogram', 'ក្នុងប្រលេឡូក្រាម ' + M('ABCD') + ' មានមុំឈម ' + M('\\angle A = 2x + 10^\\circ') + ' និង ' + M('\\angle C = 3x - 20^\\circ') + '។ តម្លៃនៃ ' + M('x') + ' គឺ ៖', M('30^\\circ'), [M('20^\\circ'), M('40^\\circ'), M('25^\\circ')], M('2x + 10 = 3x - 20 \\Rightarrow x = 30^\\circ') + ' នាំឱ្យ ' + M('\\angle A = \\angle C = 70^\\circ') + '។'))
    C.append(mcq('medium', 'parallelogram', 'ប្រលេឡូក្រាម ' + M('ABCD') + ' មានអង្កត់ទ្រូងកាត់គ្នាត្រង់ ' + M('O') + '។ បើ ' + M('OA = 3x - 5') + ' និង ' + M('OC = x + 7') + ' នោះ ' + M('x') + ' ស្មើ ៖', M('6'), [M('4'), M('5'), M('8')], M('3x - 5 = x + 7 \\Rightarrow 2x = 12 \\Rightarrow x = 6') + ' នាំឱ្យ ' + M('OA = OC = 13') + '។'))
    C.append(mcq('medium', 'trapezoid', 'ចតុកោណព្នាយសមបាត ' + M('ABCD') + ' (' + M('AB \\parallel CD') + ') មានមុំបាត ' + M('\\angle D = 65^\\circ') + '។ រង្វាស់មុំ ' + M('\\angle A') + ' ស្មើ ៖', M('115^\\circ'), [M('65^\\circ'), M('125^\\circ'), M('90^\\circ')], M('\\angle A = 180^\\circ - 65^\\circ = 115^\\circ') + ' (មុំក្នុងរួមខាងព្រោះ ' + M('AB \\parallel CD') + ')។'))
    C.append(mcq('medium', 'rhombus', 'ចតុកោណស្មើមួយមានបរិមាត្រ ' + M('48\\ \\text{cm}') + '។ ប្រវែងជ្រុងនីមួយៗរបស់វាស្មើ ៖', M('12\\ \\text{cm}'), [M('24\\ \\text{cm}'), M('16\\ \\text{cm}'), M('8\\ \\text{cm}')], M('\\dfrac{48}{4} = 12\\ \\text{cm}') + ' (ជ្រុងទាំងបួនប៉ុនគ្នា)។'))
    C.append(mcq('medium', 'rhombus', 'ចតុកោណស្មើមួយមានជ្រុងប្រវែង ' + M('5\\ \\text{cm}') + ' និងអង្កត់ទ្រូងមួយប្រវែង ' + M('6\\ \\text{cm}') + '។ ប្រវែងអង្កត់ទ្រូងមួយទៀតស្មើ ៖', M('8\\ \\text{cm}'), [M('4\\ \\text{cm}'), M('10\\ \\text{cm}'), M('6\\ \\text{cm}')], 'ពាក់កណ្តាលអង្កត់ទ្រូង ' + M('\\sqrt{5^2 - 3^2} = 4\\ \\text{cm}') + ' នាំឱ្យអង្កត់ទ្រូងទីពីរគឺ ' + M('2 \\times 4 = 8\\ \\text{cm}') + '។'))
    C.append(mcq('medium', 'rectangle', 'ចតុកោណកែងមួយមានបណ្តោយ ' + M('12\\ \\text{cm}') + ' និងទទឹង ' + M('5\\ \\text{cm}') + '។ ប្រវែងអង្កត់ទ្រូងរបស់វាស្មើ ៖', M('13\\ \\text{cm}'), [M('17\\ \\text{cm}'), M('15\\ \\text{cm}'), M('10\\ \\text{cm}')], M('d = \\sqrt{12^2 + 5^2} = \\sqrt{144 + 25} = \\sqrt{169} = 13\\ \\text{cm}') + '។'))
    C.append(mcq('medium', 'square', 'ការេមួយមានប្រវែងអង្កត់ទ្រូង ' + M('6\\sqrt{2}\\ \\text{cm}') + '។ ប្រវែងជ្រុងនៃការេនោះស្មើ ៖', M('6\\ \\text{cm}'), [M('3\\ \\text{cm}'), M('12\\ \\text{cm}'), M('6\\sqrt{2}\\ \\text{cm}')], 'អង្កត់ទ្រូងការេ ' + M('d = a\\sqrt{2} \\Rightarrow a = 6\\ \\text{cm}') + '។'))
    C.append(mcq('medium', 'trapezoid_mid', 'ចតុកោណព្នាយមួយមានបាតតូច ' + M('8\\ \\text{cm}') + ' និងបាតធំ ' + M('14\\ \\text{cm}') + '។ ប្រវែងមូលដ្ឋានមធ្យម (កាត់ចំណុចកណ្តាលជ្រុងទ្រេតទាំងពីរ) ស្មើ ៖', M('11\\ \\text{cm}'), [M('22\\ \\text{cm}'), M('10\\ \\text{cm}'), M('12\\ \\text{cm}')], M('m = \\dfrac{8 + 14}{2} = \\dfrac{22}{2} = 11\\ \\text{cm}') + '។'))
    C.append(mcq('medium', 'consecutive_ratio', 'ក្នុងប្រលេឡូក្រាមមួយ មុំតគ្នាពីរមានផលធៀប ' + M('1 \\colon 3') + '។ រង្វាស់មុំតូចគឺ ៖', M('45^\\circ'), [M('30^\\circ'), M('60^\\circ'), M('40^\\circ')], M('x + 3x = 180^\\circ \\Rightarrow 4x = 180^\\circ \\Rightarrow x = 45^\\circ') + '។'))
    C.append(mcq('medium', 'parallelogram_sides', 'ប្រលេឡូក្រាមមួយមានបរិមាត្រ ' + M('36\\ \\text{cm}') + ' ហើយជ្រុងមួយវែងជាងជ្រុងមួយទៀត ' + M('4\\ \\text{cm}') + '។ ប្រវែងជ្រុងទាំងពីរគឺ ៖', M('7\\ \\text{cm}\\ \\text{និង}\\ 11\\ \\text{cm}'), [M('6\\ \\text{cm}\\ \\text{និង}\\ 10\\ \\text{cm}'), M('8\\ \\text{cm}\\ \\text{និង}\\ 12\\ \\text{cm}'), M('5\\ \\text{cm}\\ \\text{និង}\\ 9\\ \\text{cm}')], M('2(x + x + 4) = 36 \\Rightarrow 4x + 8 = 36 \\Rightarrow 4x = 28 \\Rightarrow x = 7\\ \\text{cm}') + ' នាំឱ្យជ្រុងគឺ 7 និង 11។'))
    C.append(mcq('medium', 'kite_angles', 'ចតុកោណខ្លែង ' + M('ABCD') + ' មាន ' + M('AB = AD') + ' និង ' + M('CB = CD') + '។ បើ ' + M('\\angle B = 100^\\circ') + ' នោះរង្វាស់មុំ ' + M('\\angle D') + ' ស្មើ ៖', M('100^\\circ'), [M('80^\\circ'), M('90^\\circ'), M('120^\\circ')], 'ក្នុងចតុកោណខ្លែង មុំរវាងជ្រុងមិនស្មើគ្នាទាំងពីរគូជាមុំប៉ុនគ្នា ៖ ' + M('\\angle B = \\angle D = 100^\\circ') + '។'))
    C.append(mcq('medium', 'hierarchy', 'ប្រលេឡូក្រាមដែលមានអង្កត់ទ្រូងទាំងពីរប៉ុនគ្នាផង និងកែងគ្នាផង គឺជា ៖', M('\\text{ការេ}'), [M('\\text{ចតុកោណកែង}'), M('\\text{ចតុកោណស្មើ}'), M('\\text{ចតុកោណព្នាយ}')], 'អង្កត់ទ្រូងប៉ុនគ្នា (ចតុកោណកែង) + កែងគ្នា (ចតុកោណស្មើ) $\\implies$ ការេ (Square)។'))

    # ==========================================
    # 3. MCQ HARD (7 target)
    # ==========================================
    C.append(mcq('hard', 'consecutive_algebra', 'ក្នុងប្រលេឡូក្រាម ' + M('ABCD') + ' មាន ' + M('\\angle A = 5x - 20^\\circ') + ' និង ' + M('\\angle B = 3x + 40^\\circ') + '។ រង្វាស់មុំ ' + M('\\angle A') + ' ស្មើ ៖', M('80^\\circ'), [M('100^\\circ'), M('75^\\circ'), M('85^\\circ')], M('(5x - 20) + (3x + 40) = 180 \\Rightarrow 8x = 160 \\Rightarrow x = 20^\\circ') + ' នាំឱ្យ ' + M('\\angle A = 5(20) - 20 = 80^\\circ') + '។'))
    C.append(mcq('hard', 'rhombus_angles', 'ចតុកោណស្មើ ' + M('ABCD') + ' មានអង្កត់ទ្រូង ' + M('AC') + ' ស្មើនឹងជ្រុង ' + M('AB') + '។ រង្វាស់មុំទាល ' + M('\\angle B') + ' ស្មើ ៖', M('120^\\circ'), [M('100^\\circ'), M('110^\\circ'), M('135^\\circ')], M('\\Delta ABC') + ' សម័ង្ស នាំឱ្យ ' + M('\\angle BAC = 60^\\circ') + ' នាំឱ្យ ' + M('\\angle A = 120^\\circ') + ' ឬ ' + M('\\angle B = 180^\\circ - 60^\\circ = 120^\\circ') + '។'))
    C.append(mcq('hard', 'square_inscribed', 'ការេមួយមានផ្ទៃក្រឡា ' + M('100\\ \\text{cm}^2') + '។ ប្រវែងអង្កត់ទ្រូងរបស់វាគឺ ៖', M('10\\sqrt{2}\\ \\text{cm}'), [M('10\\ \\text{cm}'), M('20\\ \\text{cm}'), M('14\\ \\text{cm}')], M('a = 10\\ \\text{cm} \\Rightarrow d = 10\\sqrt{2}\\ \\text{cm}') + '។'))
    C.append(mcq('hard', 'parallelogram_bisector', 'ក្នុងប្រលេឡូក្រាម ' + M('ABCD') + ' កន្លះបន្ទាត់ពុះមុំ ' + M('\\angle A') + ' កាត់ជ្រុង ' + M('BC') + ' ត្រង់ ' + M('E') + '។ ត្រីកោណ ' + M('ABE') + ' ជា ៖', M('\\text{ត្រីកោណសមបាតកំពូល } B'), [M('\\text{ត្រីកោណកែង}'), M('\\text{ត្រីកោណសម័ង្ស}'), M('\\text{ត្រីកោណទូទៅ}')], M('\\angle BAE = \\angle EAD = \\angle BEA') + ' (មុំឆ្លាស់ក្នុង) នាំឱ្យ ' + M('BA = BE') + ' (សមបាត)។'))
    C.append(mcq('hard', 'trapezoid_diagonals', 'ចតុកោណព្នាយកែង ' + M('ABCD') + ' មានមុំកែង ' + M('\\angle A = \\angle D = 90^\\circ') + ' បាត ' + M('AB = 4\\ \\text{cm}') + ', ' + M('CD = 9\\ \\text{cm}') + ' និងកម្ពស់ ' + M('AD = 12\\ \\text{cm}') + '។ ប្រវែងជ្រុងទ្រេត ' + M('BC') + ' ស្មើ ៖', M('13\\ \\text{cm}'), [M('15\\ \\text{cm}'), M('11\\ \\text{cm}'), M('12\\ \\text{cm}')], M('HC = 9 - 4 = 5\\ \\text{cm} \\Rightarrow BC = \\sqrt{12^2 + 5^2} = 13\\ \\text{cm}') + '។'))
    C.append(mcq('hard', 'kite_area', 'ចតុកោណខ្លែងមួយមានអង្កត់ទ្រូងទាំងពីរប្រវែង ' + M('16\\ \\text{cm}') + ' និង ' + M('25\\ \\text{cm}') + '។ ផ្ទៃក្រឡារបស់វាស្មើ ៖', M('200\\ \\text{cm}^2'), [M('400\\ \\text{cm}^2'), M('100\\ \\text{cm}^2'), M('250\\ \\text{cm}^2')], M('S = \\dfrac{16 \\times 25}{2} = 200\\ \\text{cm}^2') + '។'))
    C.append(mcq('hard', 'center_symmetry', 'ផ្ចិតឆ្លុះនៃប្រលេឡូក្រាមមួយគឺជា ៖', M('\\text{ចំណុចប្រសព្វនៃអង្កត់ទ្រូងទាំងពីរ}'), [M('\\text{ចំណុចកណ្តាលនៃជ្រុងមួយ}'), M('\\text{កំពូលណាមួយ}'), M('\\text{គ្មានផ្ចិតឆ្លុះទេ}')], 'ចំណុចប្រសព្វនៃអង្កត់ទ្រូងជាផ្ចិតឆ្លុះនៃប្រលេឡូក្រាម។'))

    # ==========================================
    # 4. MCQ PISA (5 target)
    # ==========================================
    C.append(with_img(mcq('pisa', 'pisa', 'ទ្វាររបងឈើរាងចតុកោណកែងមានទទឹង ' + M('1.5\\ \\text{m}') + ' និងកម្ពស់ ' + M('2\\ \\text{m}') + ' (ដូចរូប)។ ប្រវែងបន្ទះក្តារបន្ទូលខ្វែងអង្កត់ទ្រូង (' + M('d') + ') ដើម្បីទប់ទ្វារកុំឱ្យទ្រេតគឺ ៖', M('2.5\\ \\text{m}'), [M('3.5\\ \\text{m}'), M('2.2\\ \\text{m}'), M('3\\ \\text{m}')], M('d = \\sqrt{1.5^2 + 2^2} = \\sqrt{2.25 + 4} = \\sqrt{6.25} = 2.5\\ \\text{m}') + '។'), FIG_GATE_BRACE))
    C.append(mcq('pisa', 'pisa', 'ដីស្រែរាងចតុកោណព្នាយមានបាតតូច ' + M('30\\ \\text{m}') + ', បាតធំ ' + M('50\\ \\text{m}') + ' និងកម្ពស់ ' + M('20\\ \\text{m}') + '។ ផ្ទៃក្រឡាដីស្រែនោះគឺ ៖', M('800\\ \\text{m}^2'), [M('1\\,600\\ \\text{m}^2'), M('600\\ \\text{m}^2'), M('750\\ \\text{m}^2')], M('S = \\dfrac{(30 + 50) \\times 20}{2} = 800\\ \\text{m}^2') + '។'))
    C.append(mcq('pisa', 'pisa', 'កុមារាម្នាក់ធ្វើខ្លែងរាងចតុកោណខ្លែងដោយប្រើឆ្អឹងខ្នងខ្វែងគ្នាកែងប្រវែង ' + M('40\\ \\text{cm}') + ' និង ' + M('30\\ \\text{cm}') + '។ ផ្ទៃក្រឡាខ្លែងនោះគឺ ៖', M('600\\ \\text{cm}^2'), [M('1\\,200\\ \\text{cm}^2'), M('300\\ \\text{cm}^2'), M('700\\ \\text{cm}^2')], M('S = \\dfrac{40 \\times 30}{2} = 600\\ \\text{cm}^2') + '។'))
    C.append(mcq('pisa', 'pisa', 'ការ៉ូផ្កាថ្មរាងចតុកោណស្មើមានអង្កត់ទ្រូង ' + M('24\\ \\text{cm}') + ' និង ' + M('10\\ \\text{cm}') + '។ ផ្ទៃក្រឡានៃការ៉ូមួយដុំគឺ ៖', M('120\\ \\text{cm}^2'), [M('240\\ \\text{cm}^2'), M('60\\ \\text{cm}^2'), M('150\\ \\text{cm}^2')], M('S = \\dfrac{24 \\times 10}{2} = 120\\ \\text{cm}^2') + '។'))
    C.append(mcq('pisa', 'pisa', 'ប្រឡោះចតរថយន្តរាងប្រលេឡូក្រាមមានបាត ' + M('2.5\\ \\text{m}') + ' និងកម្ពស់កែង ' + M('5\\ \\text{m}') + '។ ផ្ទៃក្រឡានៃប្រឡោះចតរថយន្តមួយគឺ ៖', M('12.5\\ \\text{m}^2'), [M('25\\ \\text{m}^2'), M('15\\ \\text{m}^2'), M('10\\ \\text{m}^2')], M('S = 2.5 \\times 5 = 12.5\\ \\text{m}^2') + '។'))

    # ==========================================
    # 5. WRITING EASY (1 target, 5 pts total)
    # ==========================================
    W('easy', 'angle_sum_quad', 'ក្នុងចតុកោណ ' + M('ABCD') + ' មួយមាន ' + M('\\angle A = 85^\\circ, \\angle B = 115^\\circ, \\angle C = 70^\\circ') + '។ ក. រំលឹកផលបូករង្វាស់មុំក្នុងទាំងបួននៃចតុកោណមួយ។ ខ. សរសេរសមីការគណនាមុំ ' + M('\\angle D') + '។ គ. គណនារង្វាស់មុំ ' + M('\\angle D') + '។', [
        ('ក. ផលបូករង្វាស់មុំក្នុងទាំងបួននៃចតុកោណមួយស្មើនឹង ' + M('360^\\circ'), 1),
        ('ខ. សមីការ ៖ ' + M('\\angle A + \\angle B + \\angle C + \\angle D = 360^\\circ'), 1),
        (M('85^\\circ + 115^\\circ + 70^\\circ + \\angle D = 360^\\circ'), 1),
        ('គ. ' + M('270^\\circ + \\angle D = 360^\\circ \\Rightarrow \\angle D = 360^\\circ - 270^\\circ'), 1),
        ('ដូចនេះ ' + M('\\angle D = 90^\\circ'), 1)])

    # ==========================================
    # 6. WRITING MEDIUM (4 target, 5 pts total each)
    # ==========================================
    W('medium', 'parallelogram_angles', 'ក្នុងប្រលេឡូក្រាម ' + M('ABCD') + ' មួយមានមុំឈម ' + M('\\angle A = 2x + 10^\\circ') + ' និង ' + M('\\angle C = 3x - 20^\\circ') + '។ ក. បញ្ជាក់ទំនាក់ទំនងរវាងមុំឈម ' + M('\\angle A') + ' និង ' + M('\\angle C') + '។ ខ. រកតម្លៃនៃ ' + M('x') + '។ គ. គណនារង្វាស់មុំទាំងបួននៃប្រលេឡូក្រាម។', [
        ('ក. ក្នុងប្រលេឡូក្រាម មុំឈមជាមុំប៉ុនគ្នា នាំឱ្យ ' + M('\\angle A = \\angle C'), 1),
        ('ខ. សមីការ ៖ ' + M('2x + 10 = 3x - 20 \\Rightarrow 3x - 2x = 10 + 20 \\Rightarrow x = 30^\\circ'), 2),
        ('គ. មុំ ' + M('\\angle A = \\angle C = 2(30^\\circ) + 10^\\circ = 70^\\circ'), 1),
        ('មុំតគ្នាជាប់បន្ថែម ៖ ' + M('\\angle B = \\angle D = 180^\\circ - 70^\\circ = 110^\\circ'), 1)])

    W('medium', 'parallelogram_diagonals', 'ប្រលេឡូក្រាម ' + M('ABCD') + ' មានអង្កត់ទ្រូង ' + M('AC') + ' និង ' + M('BD') + ' ប្រសព្វគ្នាត្រង់ ' + M('O') + '។ គេដឹងថា ' + M('OA = 3x - 5\\ \\text{cm}') + ' និង ' + M('OC = x + 7\\ \\text{cm}') + '។ ក. បញ្ជាក់លក្ខណៈប្រសព្វនៃអង្កត់ទ្រូងទាំងពីរ។ ខ. រកតម្លៃនៃ ' + M('x') + '។ គ. គណនាប្រវែងអង្កត់ទ្រូង ' + M('AC') + '។', [
        ('ក. អង្កត់ទ្រូងទាំងពីរកាត់គ្នាត្រង់ចំណុចកណ្តាល ' + M('O') + ' នាំឱ្យ ' + M('OA = OC'), 1),
        ('ខ. សមីការ ៖ ' + M('3x - 5 = x + 7 \\Rightarrow 2x = 12 \\Rightarrow x = 6'), 2),
        ('គ. ប្រវែង ' + M('OA = 3(6) - 5 = 13\\ \\text{cm}'), 1),
        ('អង្កត់ទ្រូង ' + M('AC = 2 \\times OA = 2 \\times 13 = 26\\ \\text{cm}'), 1)], FIG_PARALLELOGRAM)

    W('medium', 'isosceles_trapezoid', 'ចតុកោណព្នាយសមបាត ' + M('ABCD') + ' (' + M('AB \\parallel CD') + ') មានមុំបាត ' + M('\\angle D = 65^\\circ') + '។ ក. គណនារង្វាស់មុំបាត ' + M('\\angle C') + '។ ខ. គណនារង្វាស់មុំ ' + M('\\angle A') + ' និង ' + M('\\angle B') + '។ គ. ពន្យល់ទំនាក់ទំនងរវាងអង្កត់ទ្រូង ' + M('AC') + ' និង ' + M('BD') + '។', [
        ('ក. ចតុកោណព្នាយសមបាតមានមុំបាតស្មើគ្នា នាំឱ្យ ' + M('\\angle C = \\angle D = 65^\\circ'), 1),
        ('ខ. មុំ ' + M('\\angle A') + ' និង ' + M('\\angle D') + ' ជាមុំក្នុងរួមខាង (' + M('AB \\parallel CD') + ') នាំឱ្យ ' + M('\\angle A = 180^\\circ - 65^\\circ = 115^\\circ'), 1),
        ('ដូចគ្នា មុំ ' + M('\\angle B = 180^\\circ - 65^\\circ = 115^\\circ'), 1),
        ('គ. ចតុកោណព្នាយសមបាតមានអង្កត់ទ្រូងពីរប៉ុនគ្នា គឺ ' + M('AC = BD'), 2)], FIG_TRAPEZOID)

    W('medium', 'rhombus_properties', 'ចតុកោណស្មើ ' + M('ABCD') + ' មានជ្រុង ' + M('AB = 5\\ \\text{cm}') + ' និងអង្កត់ទ្រូង ' + M('BD = 6\\ \\text{cm}') + ' កាត់ ' + M('AC') + ' ត្រង់ ' + M('O') + '។ ក. បញ្ជាក់រង្វាស់ជ្រុងទាំងបួន។ ខ. បញ្ជាក់លក្ខណៈកែងគ្នានៃអង្កត់ទ្រូងទាំងពីរ។ គ. គណនាប្រវែងអង្កត់ទ្រូង ' + M('AC') + '។', [
        ('ក. ជ្រុងទាំងបួនប៉ុនគ្នា ៖ ' + M('AB = BC = CD = DA = 5\\ \\text{cm}'), 1),
        ('ខ. អង្កត់ទ្រូងទាំងពីរកែងគ្នាត្រង់ចំណុចកណ្តាល ' + M('O') + ' (' + M('AC \\perp BD') + ')', 1),
        ('គ. ' + M('BO = \\dfrac{BD}{2} = 3\\ \\text{cm}') + '។ ក្នុងត្រីកោណកែង ' + M('AOB') + ' ៖ ' + M('OA = \\sqrt{5^2 - 3^2} = 4\\ \\text{cm}'), 2),
        ('ដូចនេះ អង្កត់ទ្រូង ' + M('AC = 2 \\times 4 = 8\\ \\text{cm}'), 1)], FIG_RHOMBUS)

    # ==========================================
    # 7. WRITING HARD (4 target, 5 pts total each)
    # ==========================================
    W('hard', 'rhombus_proof', M('\\Delta ABC') + ' ជាត្រីកោណសមបាតកំពូល ' + M('A') + ' (' + M('AB = AC') + ')។ ' + M('M') + ' ជាចំណុចកណ្តាលនៃ ' + M('BC') + '។ តាម ' + M('A') + ' គូសបន្ទាត់ស្របនឹង ' + M('BC') + ' ហើយតាម ' + M('C') + ' គូសបន្ទាត់ស្របនឹង ' + M('AM') + ' បន្ទាត់ទាំងពីរជួបគ្នាត្រង់ ' + M('D') + '។ ក. បង្ហាញថាចតុកោណ ' + M('AMCD') + ' ជាចតុកោណកែង។ ខ. បង្ហាញថា ' + M('AD = MC = MB') + '។ គ. បង្ហាញថាចតុកោណ ' + M('ABMD') + ' ជាប្រលេឡូក្រាម។', [
        ('ក. ' + M('AD \\parallel MC') + ' និង ' + M('CD \\parallel AM \\Rightarrow AMCD') + ' ជាប្រលេឡូក្រាម។ ដោយ ' + M('AM \\perp BC \\Rightarrow \\angle AMC = 90^\\circ') + ' នាំឱ្យ ' + M('AMCD') + ' ជាចតុកោណកែង', 2),
        ('ខ. វិបាកចតុកោណកែង ៖ ' + M('AD = MC') + '។ ដោយ ' + M('M') + ' ជាចំណុចកណ្តាល ' + M('BC \\Rightarrow MC = MB') + ' ដូចនេះ ' + M('AD = MC = MB'), 1),
        ('គ. ចតុកោណ ' + M('ABMD') + ' មាន ' + M('AD \\parallel BM') + ' និង ' + M('AD = BM') + ' (ជ្រុងឈមមួយគូស្របគ្នានិងប៉ុនគ្នា)', 1),
        ('ដូចនេះ ' + M('ABMD') + ' ជាប្រលេឡូក្រាម', 1)])

    W('hard', 'rectangle_diagonal_proof', 'ចតុកោណកែង ' + M('ABCD') + ' មានអង្កត់ទ្រូង ' + M('AC') + ' និង ' + M('BD') + ' កាត់គ្នាត្រង់ ' + M('O') + '។ ក. ប្រើត្រីកោណប៉ុនគ្នា ' + M('\\Delta ABC') + ' និង ' + M('\\Delta BAD') + ' បង្ហាញថា ' + M('AC = BD') + '។ ខ. បង្ហាញថា ' + M('O') + ' ជាចំណុចកណ្តាលនៃ ' + M('AC') + ' និង ' + M('BD') + '។ គ. ទាញបញ្ជាក់ថា ' + M('OA = OB = OC = OD') + '។', [
        ('ក. ត្រីកោណកែង ' + M('ABC') + ' និង ' + M('BAD') + ' មាន ' + M('AB') + ' ជាជ្រុងរួម, ' + M('BC = AD') + ' នាំឱ្យ ' + M('\\Delta ABC \\cong \\Delta BAD') + ' (ជ.ម.ជ) នាំឱ្យ ' + M('AC = BD'), 2),
        ('ខ. ចតុកោណកែងជាប្រលេឡូក្រាម នាំឱ្យអង្កត់ទ្រូងកាត់គ្នាត្រង់ចំណុចកណ្តាល ' + M('O'), 1),
        ('គ. ដោយ ' + M('AC = BD') + ' នោះកន្លះអង្កត់ទ្រូងស្មើគ្នា ៖ ' + M('OA = OB = OC = OD = \\dfrac{AC}{2}'), 2)])

    W('hard', 'consecutive_angles_algebra', 'ក្នុងប្រលេឡូក្រាម ' + M('ABCD') + ' មានមុំតគ្នា ' + M('\\angle A = 5x - 20^\\circ') + ' និង ' + M('\\angle B = 3x + 40^\\circ') + '។ ក. សរសេរទំនាក់ទំនងផលបូក ' + M('\\angle A + \\angle B') + '។ ខ. រកតម្លៃនៃ ' + M('x') + '។ គ. គណនារង្វាស់មុំទាំងបួន។', [
        ('ក. មុំតគ្នាក្នុងប្រលេឡូក្រាមជាមុំជាប់បន្ថែម ៖ ' + M('\\angle A + \\angle B = 180^\\circ'), 1),
        ('ខ. ' + M('(5x - 20) + (3x + 40) = 180 \\Rightarrow 8x + 20 = 180 \\Rightarrow 8x = 160 \\Rightarrow x = 20^\\circ'), 2),
        ('គ. ' + M('\\angle A = 5(20^\\circ) - 20^\\circ = 80^\\circ \\Rightarrow \\angle C = 80^\\circ'), 1),
        (M('\\angle B = 3(20^\\circ) + 40^\\circ = 100^\\circ \\Rightarrow \\angle D = 100^\\circ'), 1)])

    W('hard', 'kite_orthogonality', 'ចតុកោណ ' + M('ABCD') + ' មាន ' + M('AB = AD') + ' និង ' + M('CB = CD') + ' (ចតុកោណខ្លែង)។ ក. បង្ហាញថាចំណុច ' + M('A') + ' និង ' + M('C') + ' ឋិតនៅលើមេដ្យាទ័រនៃ ' + M('BD') + '។ ខ. ទាញបញ្ជាក់ថា ' + M('AC \\perp BD') + '។ គ. បង្ហាញថា ' + M('AC') + ' ជាបន្ទាត់ពុះមុំ ' + M('\\angle A') + ' និង ' + M('\\angle C') + '។', [
        ('ក. ' + M('AB = AD \\Rightarrow A') + ' នៅលើមេដ្យាទ័រនៃ ' + M('BD') + '; ' + M('CB = CD \\Rightarrow C') + ' នៅលើមេដ្យាទ័រនៃ ' + M('BD'), 2),
        ('ខ. បន្ទាត់ ' + M('AC') + ' ឆ្លងកាត់ ' + M('A') + ' និង ' + M('C') + ' គឺជាមេដ្យាទ័រនៃ ' + M('BD') + ' នាំឱ្យ ' + M('AC \\perp BD'), 1),
        ('គ. ' + M('\\Delta ABC \\cong \\Delta ADC') + ' (ជ.ជ.ជ) នាំឱ្យ ' + M('\\angle BAC = \\angle DAC') + ' និង ' + M('\\angle BCA = \\angle DCA') + ' ដូចនេះ ' + M('AC') + ' ជាបន្ទាត់ពុះមុំទាំងពីរ', 2)])

    # ==========================================
    # 8. WRITING PISA (5 target, 5 pts total each)
    # ==========================================
    W('pisa', 'gate_brace', 'ទ្វាររបងឈើមួយមានរាងចតុកោណកែងទទឹង ' + M('1.5\\ \\text{m}') + ' និងកម្ពស់ ' + M('2\\ \\text{m}') + '។ ក. ពន្យល់ហេតុអ្វីគេត្រូវវាយបន្ទះក្តារបន្ទូលខ្វែងអង្កត់ទ្រូង (Cross-brace)។ ខ. គណនាប្រវែងបន្ទះក្តារខ្វែងនោះ។ គ. បើគ្មានបន្ទះក្តារខ្វែង តើទ្វារអាចប្រែប្រួលរាងយ៉ាងដូចម្តេច?', [
        ('ក. បន្ទះក្តារខ្វែងបំបែកចតុកោណកែងទៅជាត្រីកោណពីរដែលមានរាងរឹងមាំមិនប្រែប្រួលរាង (Triangle Rigidity)', 2),
        ('ខ. តាមទ្រឹស្តីបទពីតាករ ៖ ' + M('d = \\sqrt{1.5^2 + 2^2} = \\sqrt{2.25 + 4} = \\sqrt{6.25} = 2.5\\ \\text{m}'), 2),
        ('គ. បើគ្មានបន្ទះក្តារខ្វែង ទ្វារអាចបត់ទ្រេតទៅជាប្រលេឡូក្រាម (Sagging) ពិបាកបិទបើក', 1)], FIG_GATE_BRACE)

    W('pisa', 'field_division', 'ដីស្រែរាងចតុកោណព្នាយ ' + M('ABCD') + ' (' + M('AB \\parallel CD') + ') មានបាតតូច ' + M('AB = 30\\ \\text{m}') + ', បាតធំ ' + M('CD = 50\\ \\text{m}') + ' និងកម្ពស់ ' + M('20\\ \\text{m}') + '។ ក. គណនាផ្ទៃក្រឡាដីស្រែសរុប។ ខ. គេចែកដីជាពីរចំណែក ៖ ត្រីកោណកែង ' + M('ADH') + ' (' + M('DH = 10\\ \\text{m}') + ') និងចតុកោណព្នាយកែង ' + M('ABCH') + ' (' + M('HC = 40\\ \\text{m}') + ')។ គណនាផ្ទៃក្រឡាចំណែកនីមួយៗ។ គ. ផ្ទៀងផ្ទាត់ផលបូកផ្ទៃក្រឡាទាំងពីរ។', [
        ('ក. ផ្ទៃសរុប ៖ ' + M('S = \\dfrac{(30 + 50) \\times 20}{2} = 800\\ \\text{m}^2'), 2),
        ('ខ. ផ្ទៃត្រីកោណ ' + M('S_1 = \\dfrac{10 \\times 20}{2} = 100\\ \\text{m}^2') + '; ផ្ទៃចតុកោណព្នាយ ' + M('S_2 = \\dfrac{(30 + 40) \\times 20}{2} = 700\\ \\text{m}^2'), 2),
        ('គ. ផ្ទៀងផ្ទាត់ ៖ ' + M('S_1 + S_2 = 100 + 700 = 800\\ \\text{m}^2 = S') + ' (ត្រឹមត្រូវ)', 1)])

    W('pisa', 'kite_toy', 'កុមារាម្នាក់ធ្វើខ្លែងរាងចតុកោណខ្លែង ' + M('ABCD') + ' ដោយប្រើបន្ទះឫស្សីខ្វែងគ្នាកែង ' + M('AC = 40\\ \\text{cm}') + ' និង ' + M('BD = 30\\ \\text{cm}') + '។ ក. ពន្យល់លក្ខណៈកែងគ្នានៃឆ្អឹងខ្នងទាំងពីរ។ ខ. គណនាផ្ទៃក្រឡានៃខ្លែង។ គ. បើគាត់ចង់បិទក្រដាសបន្ថែមគែម ' + M('10\\%') + ' តើត្រូវត្រៀមក្រដាសផ្ទៃប៉ុន្មាន?', [
        ('ក. ឆ្អឹងខ្នងទាំងពីរកែងគ្នាព្រោះចតុកោណខ្លែងមានអង្កត់ទ្រូងកាត់គ្នាកែង (' + M('AC \\perp BD') + ')', 1),
        ('ខ. ផ្ទៃក្រឡាខ្លែង ៖ ' + M('S = \\dfrac{AC \\times BD}{2} = \\dfrac{40 \\times 30}{2} = 600\\ \\text{cm}^2'), 2),
        ('គ. ផ្ទៃក្រដាសត្រូវត្រៀម ៖ ' + M('600 \\times 1.10 = 660\\ \\text{cm}^2'), 2)])

    W('pisa', 'tiling_rhombus', 'សាលប្រជុំមួយក្រាលការ៉ូរាងចតុកោណស្មើដែលមានអង្កត់ទ្រូង ' + M('24\\ \\text{cm}') + ' និង ' + M('10\\ \\text{cm}') + '។ ក. គណនាផ្ទៃក្រឡានៃការ៉ូមួយដុំ។ ខ. គណនាប្រវែងជ្រុងនៃការ៉ូនីមួយៗ។ គ. បើសាលប្រជុំមានផ្ទៃ ' + M('60\\ \\text{m}^2') + ' (' + M('600\\,000\\ \\text{cm}^2') + ') តើត្រូវការ៉ូប៉ុន្មានដុំ?', [
        ('ក. ផ្ទៃក្រឡាការ៉ូមួយដុំ ៖ ' + M('S_1 = \\dfrac{24 \\times 10}{2} = 120\\ \\text{cm}^2'), 1),
        ('ខ. ជ្រុងការ៉ូ ៖ ' + M('a = \\sqrt{12^2 + 5^2} = \\sqrt{144 + 25} = 13\\ \\text{cm}'), 2),
        ('គ. ចំនួនការ៉ូ ៖ ' + M('N = \\dfrac{600\\,000}{120} = 5\\,000\\ \\text{ដុំ}'), 2)])

    W('pisa', 'parking_parallelogram', 'ចំណតរថយន្តមានប្រឡោះរាងប្រលេឡូក្រាមមានបាត ' + M('b = 2.5\\ \\text{m}') + ', កម្ពស់កែង ' + M('h = 5\\ \\text{m}') + ' និងជ្រុងទ្រេត ' + M('6\\ \\text{m}') + '។ ក. គណនាផ្ទៃក្រឡានៃប្រឡោះមួយ។ ខ. បើមាន ២០ ប្រឡោះ គណនាផ្ទៃក្រឡាសរុប។ គ. ហេតុអ្វីបានជាគេរចនាប្រឡោះចតជារាងប្រលេឡូក្រាមទ្រេត?', [
        ('ក. ផ្ទៃក្រឡាមួយប្រឡោះ ៖ ' + M('S = b \\times h = 2.5 \\times 5 = 12.5\\ \\text{m}^2'), 2),
        ('ខ. ផ្ទៃសរុប ២០ ប្រឡោះ ៖ ' + M('12.5 \\times 20 = 250\\ \\text{m}^2'), 1),
        ('គ. រាងប្រលេឡូក្រាមទ្រេតជួយឱ្យមុំបត់ចូលចតតូចជាង ' + M('90^\\circ') + ' (ស្រួលចត) និងកាត់បន្ថយទទឹងផ្លូវបើកបរ', 2)])

    return C
