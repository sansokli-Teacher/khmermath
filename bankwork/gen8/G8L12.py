"""Bank candidates for Grade 8, Lesson 12: ការប្រៀបធៀបត្រីកោណ (Comparison of Triangles)
Covers MoEYS Grade 8 curriculum:
  1. និយមន័យនៃត្រីកោណប៉ុនគ្នា (Definition of congruent triangles, 6 pairs of corresponding parts)
  2. ករណីប៉ុនគ្នានៃត្រីកោណ (Congruence criteria: SAS, ASA, SSS)
  3. ករណីប៉ុនគ្នានៃត្រីកោណកែង (Right triangle congruence: HA, HL)
  4. មេដ្យាទ័រនៃអង្កត់ និងត្រីកោណសមបាត (Perpendicular bisector & isosceles triangle properties)
  5. វិសមភាពក្នុងត្រីកោណ (Side-angle inequality & triangle inequality theorem)
  6. ការប្រៀបធៀបអង្កត់ (Perpendicular vs oblique segments, projections)
  7. ការអនុវត្ត និង PISA (Real-world river survey, roof truss, garden fence, structural rigidity)

Images: Clean vector illustrations, isolated, no background, flat educational textbook style.
Geometry labels use font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic'.
"""
from lib import *

LESSON = "ការប្រៀបធៀបត្រីកោណ"

# --- SVG Illustrations ---

# 1. FIG_TRI_SAS: Two congruent triangles ABC and DEF showing SAS
FIG_TRI_SAS = (
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 320 160' width='320' height='160'>\n"
    "  <!-- Triangle ABC -->\n"
    "  <polygon points='30,130 130,130 65,40' fill='#f0fdf4' stroke='#16a34a' stroke-width='1.8'/>\n"
    "  <!-- Angle A arc -->\n"
    "  <path d='M 57,51 A 18 18 0 0 0 76,53' fill='none' stroke='#dc2626' stroke-width='1.5'/>\n"
    "  <text x='66' y='68' text-anchor='middle' font-family='Times New Roman, serif' font-size='10' fill='#dc2626'>60°</text>\n"
    "  <!-- Tick marks on AB (single) -->\n"
    "  <line x1='44' y1='82' x2='52' y2='88' stroke='#16a34a' stroke-width='1.6'/>\n"
    "  <!-- Tick marks on AC (double) -->\n"
    "  <line x1='94' y1='80' x2='102' y2='86' stroke='#16a34a' stroke-width='1.6'/>\n"
    "  <line x1='97' y1='84' x2='105' y2='90' stroke='#16a34a' stroke-width='1.6'/>\n"
    "  <!-- Vertex labels ABC (Mathcad italic) -->\n"
    "  <text x='65' y='30' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>A</text>\n"
    "  <text x='20' y='142' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>B</text>\n"
    "  <text x='140' y='142' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>C</text>\n"
    "  <!-- Side lengths -->\n"
    "  <text x='35' y='80' font-family='Times New Roman, serif' font-size='11' fill='#475569'>5 cm</text>\n"
    "  <text x='106' y='80' font-family='Times New Roman, serif' font-size='11' fill='#475569'>7 cm</text>\n"
    "  <!-- Triangle DEF -->\n"
    "  <polygon points='190,130 290,130 225,40' fill='#eff6ff' stroke='#0284c7' stroke-width='1.8'/>\n"
    "  <!-- Angle D arc -->\n"
    "  <path d='M 217,51 A 18 18 0 0 0 236,53' fill='none' stroke='#dc2626' stroke-width='1.5'/>\n"
    "  <text x='226' y='68' text-anchor='middle' font-family='Times New Roman, serif' font-size='10' fill='#dc2626'>60°</text>\n"
    "  <!-- Tick marks on DE (single) -->\n"
    "  <line x1='204' y1='82' x2='212' y2='88' stroke='#0284c7' stroke-width='1.6'/>\n"
    "  <!-- Tick marks on DF (double) -->\n"
    "  <line x1='254' y1='80' x2='262' y2='86' stroke='#0284c7' stroke-width='1.6'/>\n"
    "  <line x1='257' y1='84' x2='265' y2='90' stroke='#0284c7' stroke-width='1.6'/>\n"
    "  <!-- Vertex labels DEF (Mathcad italic) -->\n"
    "  <text x='225' y='30' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>D</text>\n"
    "  <text x='180' y='142' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>E</text>\n"
    "  <text x='300' y='142' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>F</text>\n"
    "  <!-- Side lengths -->\n"
    "  <text x='195' y='80' font-family='Times New Roman, serif' font-size='11' fill='#475569'>5 cm</text>\n"
    "  <text x='266' y='80' font-family='Times New Roman, serif' font-size='11' fill='#475569'>7 cm</text>\n"
    "</svg>"
)

# 2. FIG_RIGHT_TRI: Two right triangles ABC and DEF showing Hypotenuse-Leg (អ.ជ)
FIG_RIGHT_TRI = (
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 300 150' width='300' height='150'>\n"
    "  <!-- Triangle ABC (right at A) -->\n"
    "  <polygon points='40,120 40,30 120,120' fill='#f8fafc' stroke='#0f172a' stroke-width='1.8'/>\n"
    "  <!-- Right angle square at A -->\n"
    "  <polyline points='40,106 54,106 54,120' fill='none' stroke='#0f172a' stroke-width='1.4'/>\n"
    "  <!-- Tick on leg AB -->\n"
    "  <line x1='35' y1='75' x2='45' y2='75' stroke='#0284c7' stroke-width='1.6'/>\n"
    "  <!-- Tick on hypotenuse BC (double) -->\n"
    "  <line x1='76' y1='72' x2='84' y2='78' stroke='#dc2626' stroke-width='1.6'/>\n"
    "  <line x1='79' y1='69' x2='87' y2='75' stroke='#dc2626' stroke-width='1.6'/>\n"
    "  <!-- Labels (Mathcad italic) -->\n"
    "  <text x='28' y='132' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>A</text>\n"
    "  <text x='38' y='22' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>B</text>\n"
    "  <text x='130' y='126' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>C</text>\n"
    "  <!-- Triangle DEF (right at D) -->\n"
    "  <polygon points='190,120 190,30 270,120' fill='#f8fafc' stroke='#0f172a' stroke-width='1.8'/>\n"
    "  <!-- Right angle square at D -->\n"
    "  <polyline points='190,106 204,106 204,120' fill='none' stroke='#0f172a' stroke-width='1.4'/>\n"
    "  <!-- Tick on leg DE -->\n"
    "  <line x1='185' y1='75' x2='195' y2='75' stroke='#0284c7' stroke-width='1.6'/>\n"
    "  <!-- Tick on hypotenuse EF (double) -->\n"
    "  <line x1='226' y1='72' x2='234' y2='78' stroke='#dc2626' stroke-width='1.6'/>\n"
    "  <line x1='229' y1='69' x2='237' y2='75' stroke='#dc2626' stroke-width='1.6'/>\n"
    "  <!-- Labels (Mathcad italic) -->\n"
    "  <text x='178' y='132' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>D</text>\n"
    "  <text x='188' y='22' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>E</text>\n"
    "  <text x='280' y='126' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>F</text>\n"
    "</svg>"
)

# 3. FIG_PERP_BISECTOR: Perpendicular bisector of segment BC
FIG_PERP_BISECTOR = (
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 240 160' width='240' height='160'>\n"
    "  <!-- Segment BC -->\n"
    "  <line x1='30' y1='120' x2='210' y2='120' stroke='#0f172a' stroke-width='2'/>\n"
    "  <!-- Perpendicular line Delta -->\n"
    "  <line x1='120' y1='15' x2='120' y2='145' stroke='#0284c7' stroke-width='1.6' stroke-dasharray='4,3'/>\n"
    "  <!-- Right angle at I -->\n"
    "  <polyline points='120,108 132,108 132,120' fill='none' stroke='#0f172a' stroke-width='1.3'/>\n"
    "  <!-- Point M on Delta -->\n"
    "  <circle cx='120' cy='35' r='3.5' fill='#dc2626'/>\n"
    "  <!-- Lines MB and MC -->\n"
    "  <line x1='120' y1='35' x2='30' y2='120' stroke='#16a34a' stroke-width='1.6'/>\n"
    "  <line x1='120' y1='35' x2='210' y2='120' stroke='#16a34a' stroke-width='1.6'/>\n"
    "  <!-- Ticks on BI and IC (single) -->\n"
    "  <line x1='75' y1='115' x2='75' y2='125' stroke='#0f172a' stroke-width='1.5'/>\n"
    "  <line x1='165' y1='115' x2='165' y2='125' stroke='#0f172a' stroke-width='1.5'/>\n"
    "  <!-- Ticks on MB and MC (double) -->\n"
    "  <line x1='72' y1='74' x2='78' y2='80' stroke='#16a34a' stroke-width='1.5'/>\n"
    "  <line x1='75' y1='71' x2='81' y2='77' stroke='#16a34a' stroke-width='1.5'/>\n"
    "  <line x1='162' y1='80' x2='168' y2='74' stroke='#16a34a' stroke-width='1.5'/>\n"
    "  <line x1='159' y1='77' x2='165' y2='71' stroke='#16a34a' stroke-width='1.5'/>\n"
    "  <!-- Labels (Mathcad italic) -->\n"
    "  <text x='120' y='26' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>M</text>\n"
    "  <text x='20' y='125' text-anchor='end' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>B</text>\n"
    "  <text x='218' y='125' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>C</text>\n"
    "  <text x='112' y='135' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='13' fill='#0f172a'>I</text>\n"
    "  <text x='128' y='145' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='13' fill='#0284c7'>Δ</text>\n"
    "</svg>"
)

# 4. FIG_PERP_OBLIQUE: Perpendicular AH vs Oblique segments AB, AC
FIG_PERP_OBLIQUE = (
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 260 160' width='260' height='160'>\n"
    "  <!-- Baseline Delta -->\n"
    "  <line x1='20' y1='130' x2='240' y2='130' stroke='#0f172a' stroke-width='1.8'/>\n"
    "  <text x='245' y='134' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='13' fill='#0284c7'>Δ</text>\n"
    "  <!-- Point A -->\n"
    "  <circle cx='60' cy='30' r='3.5' fill='#0f172a'/>\n"
    "  <!-- Perpendicular AH -->\n"
    "  <line x1='60' y1='30' x2='60' y2='130' stroke='#dc2626' stroke-width='2'/>\n"
    "  <!-- Right angle at H -->\n"
    "  <polyline points='60,118 72,118 72,130' fill='none' stroke='#0f172a' stroke-width='1.3'/>\n"
    "  <!-- Oblique AB -->\n"
    "  <line x1='60' y1='30' x2='130' y2='130' stroke='#0284c7' stroke-width='1.8'/>\n"
    "  <!-- Oblique AC -->\n"
    "  <line x1='60' y1='30' x2='210' y2='130' stroke='#16a34a' stroke-width='1.8'/>\n"
    "  <!-- Points H, B, C -->\n"
    "  <circle cx='60' cy='130' r='3' fill='#0f172a'/>\n"
    "  <circle cx='130' cy='130' r='3' fill='#0f172a'/>\n"
    "  <circle cx='210' cy='130' r='3' fill='#0f172a'/>\n"
    "  <!-- Labels (Mathcad italic) -->\n"
    "  <text x='60' y='22' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>A</text>\n"
    "  <text x='55' y='146' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>H</text>\n"
    "  <text x='130' y='146' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>B</text>\n"
    "  <text x='210' y='146' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>C</text>\n"
    "</svg>"
)

# 5. FIG_RIVER_SURVEY: River width survey via congruent triangles
FIG_RIVER_SURVEY = (
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 280 180' width='280' height='180'>\n"
    "  <!-- River bank lines (wavy / dashed) -->\n"
    "  <path d='M 10 70 Q 140 60 270 70' fill='none' stroke='#38bdf8' stroke-width='2' stroke-dasharray='6,4'/>\n"
    "  <path d='M 10 110 Q 140 100 270 110' fill='none' stroke='#38bdf8' stroke-width='2' stroke-dasharray='6,4'/>\n"
    "  <text x='20' y='94' font-family='Khmer OS Battambang, Noto Sans Khmer, serif' font-size='10' fill='#0284c7'>ទន្លេ</text>\n"
    "  <!-- Triangle OAB on upper bank -->\n"
    "  <line x1='70' y1='25' x2='70' y2='125' stroke='#0f172a' stroke-width='1.8'/>\n"
    "  <line x1='70' y1='125' x2='190' y2='125' stroke='#0f172a' stroke-width='1.8'/>\n"
    "  <line x1='190' y1='125' x2='190' y2='165' stroke='#0f172a' stroke-width='1.8'/>\n"
    "  <line x1='70' y1='25' x2='190' y2='165' stroke='#dc2626' stroke-width='1.6' stroke-dasharray='4,3'/>\n"
    "  <!-- Midpoint O -->\n"
    "  <circle cx='130' cy='125' r='3.5' fill='#0284c7'/>\n"
    "  <!-- Points -->\n"
    "  <circle cx='70' cy='25' r='3.5' fill='#0f172a'/>\n"
    "  <circle cx='70' cy='125' r='3.5' fill='#0f172a'/>\n"
    "  <circle cx='190' cy='125' r='3.5' fill='#0f172a'/>\n"
    "  <circle cx='190' cy='165' r='3.5' fill='#0f172a'/>\n"
    "  <!-- Right angle symbols at A and C -->\n"
    "  <polyline points='70,113 82,113 82,125' fill='none' stroke='#0f172a' stroke-width='1.2'/>\n"
    "  <polyline points='190,137 178,137 178,125' fill='none' stroke='#0f172a' stroke-width='1.2'/>\n"
    "  <!-- Labels (Mathcad italic) -->\n"
    "  <text x='70' y='18' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>B</text>\n"
    "  <text x='58' y='132' text-anchor='end' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>A</text>\n"
    "  <text x='130' y='142' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0284c7'>O</text>\n"
    "  <text x='202' y='128' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>C</text>\n"
    "  <text x='202' y='172' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>D</text>\n"
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
    C.append(mcq('easy', 'definition', 'បើ ' + M('\\Delta ABC \\cong \\Delta DEF') + ' នោះធាតុត្រូវគ្នារវាងត្រីកោណទាំងពីរមានចំនួនប៉ុន្មានគូ?', M('6\\ \\text{គូ}'), [M('3\\ \\text{គូ}'), M('4\\ \\text{គូ}'), M('5\\ \\text{គូ}')], 'ត្រីកោណពីរប៉ុនគ្នាមានធាតុត្រូវគ្នា ៦ គូ គឺជ្រុងត្រូវគ្នា ៣ គូ និងមុំត្រូវគ្នា ៣ គូ។'))
    C.append(mcq('easy', 'definition', 'បើ ' + M('\\Delta ABC \\cong \\Delta MNP') + ' នោះជ្រុងត្រូវគ្នានឹងជ្រុង ' + M('AB') + ' គឺ ៖', M('MN'), [M('NP'), M('MP'), M('BC')], 'តាមលំដាប់កំពូលត្រូវគ្នា ជ្រុង ' + M('AB') + ' ត្រូវគ្នានឹងជ្រុង ' + M('MN') + '។'))
    C.append(mcq('easy', 'definition', 'បើ ' + M('\\Delta ABC \\cong \\Delta XYZ') + ' នោះមុំត្រូវគ្នានឹងមុំ ' + M('\\angle C') + ' គឺ ៖', M('\\angle Z'), [M('\\angle X'), M('\\angle Y'), M('\\angle B')], 'តាមលំដាប់កំពូលត្រូវគ្នា មុំ ' + M('\\angle C') + ' ត្រូវគ្នានឹងមុំ ' + M('\\angle Z') + '។'))
    C.append(mcq('easy', 'cases', 'ករណីប៉ុនគ្នានៃត្រីកោណ "ជ.ម.ជ" សំដៅលើលក្ខខណ្ឌណា?', M('\\text{ជ្រុងពីរនិងមុំផ្គុំដោយជ្រុងទាំងពីរប៉ុនរៀងគ្នា}'), [M('\\text{ជ្រុងពីរនិងមុំមួយណាក៏បាន}'), M('\\text{មុំពីរនិងជ្រុងមួយ}'), M('\\text{ជ្រុងទាំងបីប៉ុនគ្នា}')], 'ជ.ម.ជ (Side-Angle-Side) គឺមុំមួយប៉ុនគ្នាអមដោយជ្រុងពីរប៉ុនរៀងគ្នា។'))
    C.append(mcq('easy', 'cases', 'ករណីប៉ុនគ្នានៃត្រីកោណ "ម.ជ.ម" សំដៅលើលក្ខខណ្ឌណា?', M('\\text{ជ្រុងមួយនិងមុំជាប់ជ្រុងនោះពីរប៉ុនរៀងគ្នា}'), [M('\\text{មុំបីប៉ុនគ្នា}'), M('\\text{ជ្រុងពីរនិងមុំមួយ}'), M('\\text{ជ្រុងទាំងបីប៉ុនគ្នា}')], 'ម.ជ.ម (Angle-Side-Angle) គឺជ្រុងមួយប៉ុនគ្នាជាប់នឹងមុំពីរប៉ុនរៀងគ្នា។'))
    C.append(mcq('easy', 'cases', 'ករណីប៉ុនគ្នានៃត្រីកោណ "ជ.ជ.ជ" សំដៅលើលក្ខខណ្ឌណា?', M('\\text{ជ្រុងទាំងបីនៃត្រីកោណប៉ុនរៀងគ្នា}'), [M('\\text{មុំទាំងបីប៉ុនរៀងគ្នា}'), M('\\text{ជ្រុងពីរស្មើគ្នា}'), M('\\text{មុំពីរស្មើគ្នា}')], 'ជ.ជ.ជ (Side-Side-Side) គឺជ្រុងទាំងបីប៉ុនរៀងគ្នា។'))
    C.append(mcq('easy', 'right_tri', 'ត្រីកោណកែងពីរប៉ុនគ្នាតាមករណី "អ.ម" កាលណាវាមាន ៖', M('\\text{អ៊ីប៉ូតេនុសប៉ុនគ្នានិងមុំស្រួចមួយប៉ុនគ្នា}'), [M('\\text{ជ្រុងមុំកែងពីរប៉ុនគ្នា}'), M('\\text{មុំកែងពីរស្មើគ្នា}'), M('\\text{អ៊ីប៉ូតេនុសស្មើជ្រុងមុំកែង}')], 'អ.ម គឺអ៊ីប៉ូតេនុសប៉ុនគ្នានិងមុំស្រួចមួយប៉ុនគ្នា។'))
    C.append(mcq('easy', 'tri_ineq', 'ក្នុងត្រីកោណមួយ ប្រវែងជ្រុងមួយតែងតែ ៖', M('\\text{តូចជាងផលបូកជ្រុងពីរទៀត}'), [M('\\text{ធំជាងផលបូកជ្រុងពីរទៀត}'), M('\\text{ស្មើផលបូកជ្រុងពីរទៀត}'), M('\\text{ស្មើផលគុណជ្រុងពីរទៀត}')], 'ទ្រឹស្តីបទវិសមភាពត្រីកោណ ៖ ផលបូកប្រវែងជ្រុងពីរតែងតែធំជាងជ្រុងទីបី នាំឱ្យជ្រុងមួយតូចជាងផលបូកជ្រុងពីរទៀត។'))
    C.append(mcq('easy', 'perp_oblique', 'ពីចំណុចមួយនៅក្រៅបន្ទាត់ អង្កត់ដែលខ្លីជាងគេបង្អស់ទៅកាន់បន្ទាត់នោះគឺ ៖', M('\\text{អង្កត់កែង}'), [M('\\text{អង្កត់ទ្រេត}'), M('\\text{អង្កត់ស្រប}'), M('\\text{អង្កត់ពុះ}')], 'អង្កត់កែងមានប្រវែងខ្លីជាងអង្កត់ទ្រេតជានិច្ច។'))
    C.append(with_img(mcq('easy', 'bisector', 'គ្រប់ចំណុចដែលឋិតនៅលើមេដ្យាទ័រនៃអង្កត់ ' + M('BC') + ' តែងតែមានចម្ងាយ ៖', M('\\text{ស្មើគ្នាពីចុង } B \\text{ និងចុង } C'), [M('\\text{ស្មើចម្ងាយពីបន្ទាត់កែង}'), M('\\text{ធំជាងចម្ងាយពី } B'), M('\\text{តូចជាងចម្ងាយពី } C')], 'លក្ខណៈមេដ្យាទ័រ ៖ គ្រប់ចំណុចនៅលើមេដ្យាទ័រនៃអង្កត់មួយឋិតនៅស្មើចម្ងាយពីចុងទាំងសងខាងនៃអង្កត់នោះ (' + M('MB = MC') + ')។'), FIG_PERP_BISECTOR))
    C.append(mcq('easy', 'isosceles', 'ក្នុងត្រីកោណសមបាត លក្ខណៈនៃមុំបាតទាំងពីរគឺ ៖', M('\\text{ជាមុំប៉ុនគ្នា}'), [M('\\text{ជាមុំកែង}'), M('\\text{មានផលបូកស្មើ } 90^\\circ'), M('\\text{ជាមុំទាល}')], 'ក្នុងត្រីកោណសមបាត មុំបាតទាំងពីរជាមុំប៉ុនគ្នា។'))
    C.append(mcq('easy', 'angles', 'ផលបូករង្វាស់មុំក្នុងទាំងបីនៃត្រីកោណមួយស្មើនឹង ៖', M('180^\\circ'), [M('90^\\circ'), M('360^\\circ'), M('270^\\circ')], 'ផលបូកមុំក្នុងនៃត្រីកោណមួយស្មើនឹង ' + M('180^\\circ') + ' ជានិច្ច។'))

    # ==========================================
    # 2. MCQ MEDIUM (14 target)
    # ==========================================
    C.append(with_img(mcq('medium', 'sas', 'ត្រីកោណ ' + M('ABC') + ' និង ' + M('DEF') + ' មាន ' + M('AB = DE = 5\\ \\text{cm}') + ', ' + M('AC = DF = 7\\ \\text{cm}') + ' និង ' + M('\\angle A = \\angle D = 60^\\circ') + '។ ត្រីកោណទាំងពីរប៉ុនគ្នាតាមករណី ៖', M('\\text{ជ.ម.ជ}'), [M('\\text{ម.ជ.ម}'), M('\\text{ជ.ជ.ជ}'), M('\\text{អ.ម}')], 'មានជ្រុងពីរ និងមុំផ្គុំដោយជ្រុងទាំងពីរប៉ុនគ្នា នាំឱ្យប៉ុនគ្នាតាម ជ.ម.ជ (SAS)។'), FIG_TRI_SAS))
    C.append(mcq('medium', 'asa', 'ត្រីកោណ ' + M('PQR') + ' និង ' + M('STU') + ' មាន ' + M('\\angle P = \\angle S = 45^\\circ') + ', ' + M('\\angle Q = \\angle T = 65^\\circ') + ' និង ' + M('PQ = ST = 8\\ \\text{cm}') + '។ ត្រីកោណទាំងពីរប៉ុនគ្នាតាម ៖', M('\\text{ម.ជ.ម}'), [M('\\text{ជ.ម.ជ}'), M('\\text{ជ.ជ.ជ}'), M('\\text{អ.ជ}')], 'មានជ្រុងមួយជាប់នឹងមុំពីរប៉ុនរៀងគ្នា នាំឱ្យប៉ុនគ្នាតាម ម.ជ.ម (ASA)។'))
    C.append(mcq('medium', 'sss', 'ត្រីកោណពីរមានរង្វាស់ជ្រុងរៀងគ្នា ' + M('4\\ \\text{cm},\\ 6\\ \\text{cm},\\ 8\\ \\text{cm}') + ' និង ' + M('4\\ \\text{cm},\\ 6\\ \\text{cm},\\ 8\\ \\text{cm}') + '។ ត្រីកោណទាំងពីរប៉ុនគ្នាតាម ៖', M('\\text{ជ.ជ.ជ}'), [M('\\text{ជ.ម.ជ}'), M('\\text{ម.ជ.ម}'), M('\\text{អ.ម}')], 'ជ្រុងទាំងបីប៉ុនរៀងគ្នា នាំឱ្យប៉ុនគ្នាតាម ជ.ជ.ជ (SSS)។'))
    C.append(mcq('medium', 'algebra', 'បើ ' + M('\\Delta ABC \\cong \\Delta DEF') + ' ដោយ ' + M('BC = 2x + 30') + ' និង ' + M('EF = 5x - 90') + ' នោះប្រវែង ' + M('BC') + ' ស្មើ ៖', M('110\\ \\text{cm}'), [M('40\\ \\text{cm}'), M('80\\ \\text{cm}'), M('120\\ \\text{cm}')], M('2x + 30 = 5x - 90 \\Rightarrow 3x = 120 \\Rightarrow x = 40') + ' នាំឱ្យ ' + M('BC = 2(40) + 30 = 110\\ \\text{cm}') + '។'))
    C.append(mcq('medium', 'algebra', 'បើ ' + M('\\Delta ABC \\cong \\Delta MNP') + ' ដោយ ' + M('\\angle A = 3x + 15^\\circ') + ' និង ' + M('\\angle M = 75^\\circ') + ' នោះតម្លៃនៃ ' + M('x') + ' ស្មើ ៖', M('20^\\circ'), [M('25^\\circ'), M('30^\\circ'), M('15^\\circ')], M('3x + 15^\\circ = 75^\\circ \\Rightarrow 3x = 60^\\circ \\Rightarrow x = 20^\\circ') + '។'))
    C.append(with_img(mcq('medium', 'right_tri', 'ត្រីកោណកែងពីរ ' + M('ABC') + ' និង ' + M('DEF') + ' កែងត្រង់ ' + M('A') + ' និង ' + M('D') + ' មាន ' + M('AB = DE') + ' និងអ៊ីប៉ូតេនុស ' + M('BC = EF') + '។ ត្រីកោណទាំងពីរប៉ុនគ្នាតាម ៖', M('\\text{អ.ជ}'), [M('\\text{អ.ម}'), M('\\text{ជ.ម.ជ}'), M('\\text{ម.ជ.ម}')], 'មានអ៊ីប៉ូតេនុសប៉ុនគ្នា និងជ្រុងមុំកែងមួយប៉ុនគ្នា នាំឱ្យប៉ុនគ្នាតាម អ.ជ (Hypotenuse-Leg)។'), FIG_RIGHT_TRI))
    C.append(mcq('medium', 'side_angle_ineq', 'ក្នុង ' + M('\\Delta ABC') + ' មាន ' + M('\\angle A = 80^\\circ') + ', ' + M('\\angle B = 60^\\circ') + ' និង ' + M('\\angle C = 40^\\circ') + '។ ជ្រុងដែលវែងជាងគេគឺ ៖', M('BC'), [M('AB'), M('AC'), M('\\text{ជ្រុងទាំងបីស្មើគ្នា}')], 'ជ្រុងឈមនឹងមុំធំជាងគេ (' + M('\\angle A = 80^\\circ') + ') គឺជាជ្រុងវែងជាងគេ គឺជ្រុង ' + M('BC') + '។'))
    C.append(mcq('medium', 'side_angle_ineq', 'ក្នុង ' + M('\\Delta MNP') + ' មាន ' + M('MN = 7\\ \\text{cm}') + ', ' + M('NP = 9\\ \\text{cm}') + ' និង ' + M('MP = 5\\ \\text{cm}') + '។ មុំដែលតូចជាងគេគឺ ៖', M('\\angle N'), [M('\\angle M'), M('\\angle P'), M('\\angle M = \\angle P')], 'មុំឈមនឹងជ្រុងខ្លីជាងគេ (' + M('MP = 5\\ \\text{cm}') + ') គឺជាមុំតូចជាងគេ គឺមុំ ' + M('\\angle N') + '។'))
    C.append(mcq('medium', 'tri_ineq', 'ក្នុងចំណោមប្រវែងជ្រុងខាងក្រោម តើមួយណាអាចបង្កើតបានជាត្រីកោណ?', M('11,\\ 12,\\ 17'), [M('1,\\ 2,\\ 3'), M('4.1,\\ 4.7,\\ 9'), M('2,\\ 3,\\ 6')], M('11 + 12 = 23 > 17') + ' (ផលបូកពីរជ្រុងតូចធំជាងជ្រុងវែងបំផុត) នាំឱ្យសង់ត្រីកោណបាន។'))
    C.append(mcq('medium', 'tri_ineq', 'ក្នុងចំណោមប្រវែងជ្រុងខាងក្រោម តើមួយណាមិនអាចបង្កើតជាត្រីកោណបាន?', M('1,\\ 2,\\ 3'), [M('3,\\ 4,\\ 5'), M('5,\\ 6,\\ 7'), M('7,\\ 8,\\ 9')], M('1 + 2 = 3') + ' (ផលបូកស្មើនឹងជ្រុងទីបី ចំណុចរត់ត្រង់ជួរគ្នា) មិនអាចបង្កើតជាត្រីកោណបានឡើយ។'))
    C.append(with_img(mcq('medium', 'perp_oblique', 'បើ ' + M('AH \\perp \\Delta') + ' ត្រង់ ' + M('H') + ' ហើយចំណុច ' + M('B, C') + ' នៅលើ ' + M('\\Delta') + ' ដោយ ' + M('HB = 4\\ \\text{cm}') + ' និង ' + M('HC = 6\\ \\text{cm}') + ' នោះ ៖', M('AB < AC'), [M('AB > AC'), M('AB = AC'), M('AC < AH')], 'អង្កត់ទ្រេតណាមានគម្លាត (ចំណោលកែង) ធំជាង គឺវែងជាង នាំឱ្យ ' + M('AB < AC') + '។'), FIG_PERP_OBLIQUE))
    C.append(mcq('medium', 'perp_oblique', 'បើ ' + M('AH \\perp \\Delta') + ' ត្រង់ ' + M('H') + ' ហើយអង្កត់ទ្រេតពីរ ' + M('AB = AC') + ' នោះគម្លាត ' + M('HB') + ' និង ' + M('HC') + ' ៖', M('HB = HC'), [M('HB > HC'), M('HB < HC'), M('HB + HC = AH')], 'អង្កត់ទ្រេតពីរប៉ុនគ្នា នាំឱ្យមានគម្លាតស្មើគ្នា ៖ ' + M('HB = HC') + '។'))
    C.append(mcq('medium', 'isosceles', 'ត្រីកោណសមបាត ' + M('ABC') + ' មានកំពូល ' + M('A') + ' និងមុំកំពូល ' + M('\\angle A = 50^\\circ') + '។ រង្វាស់មុំបាត ' + M('\\angle B') + ' ស្មើ ៖', M('65^\\circ'), [M('50^\\circ'), M('60^\\circ'), M('70^\\circ')], M('\\angle B = \\dfrac{180^\\circ - 50^\\circ}{2} = \\dfrac{130^\\circ}{2} = 65^\\circ') + '។'))
    C.append(mcq('medium', 'equilateral', 'ត្រីកោណសម័ង្សជាត្រីកោណដែលមានជ្រុងទាំងបីប៉ុនគ្នា។ រង្វាស់មុំនីមួយៗនៃត្រីកោណសម័ង្សស្មើ ៖', M('60^\\circ'), [M('45^\\circ'), M('90^\\circ'), M('180^\\circ')], M('\\dfrac{180^\\circ}{3} = 60^\\circ') + '។'))

    # ==========================================
    # 3. MCQ HARD (7 target)
    # ==========================================
    C.append(mcq('hard', 'angle_calc', 'ក្នុង ' + M('\\Delta ABC') + ' មាន ' + M('\\angle A = 6x + 4^\\circ') + ', ' + M('\\angle B = 7x + 12^\\circ') + ' និង ' + M('\\angle C = 6x - 7^\\circ') + '។ លំដាប់ជ្រុងពីធំទៅតូចគឺ ៖', M('AC > BC > AB'), [M('AB > BC > AC'), M('BC > AC > AB'), M('AC > AB > BC')], M('19x + 9 = 180 \\Rightarrow x = 9^\\circ') + ' នាំឱ្យ ' + M('\\angle B = 75^\\circ > \\angle A = 58^\\circ > \\angle C = 47^\\circ') + ' ដូចនេះ ' + M('AC > BC > AB') + '។'))
    C.append(mcq('hard', 'tri_ineq_range', 'ត្រីកោណមួយមានប្រវែងជ្រុងពីរគឺ ' + M('5\\ \\text{cm}') + ' និង ' + M('9\\ \\text{cm}') + '។ ប្រវែងជ្រុងទីបី ' + M('x') + ' ត្រូវផ្ទៀងផ្ទាត់ ៖', M('4 < x < 14'), [M('x > 4'), M('x < 14'), M('5 < x < 9')], 'តាមវិសមភាពត្រីកោណ ' + M('9 - 5 < x < 9 + 5 \\Rightarrow 4 < x < 14') + '។'))
    C.append(mcq('hard', 'bisector_inter', 'ចំណុចប្រសព្វនៃកន្លះបន្ទាត់ពុះមុំក្នុងទាំងបីនៃត្រីកោណមួយ ឋិតនៅស្មើចម្ងាយពី ៖', M('\\text{ជ្រុងទាំងបីនៃត្រីកោណ}'), [M('\\text{កំពូលទាំងបីនៃត្រីកោណ}'), M('\\text{មេដ្យានទាំងបី}'), M('\\text{កម្ពស់ទាំងបី}')], 'កន្លះបន្ទាត់ពុះមុំទាំងបីប្រសព្វគ្នាត្រង់ផ្ចិតរង្វង់ចារឹកក្នុងត្រីកោណ ដែលមានចម្ងាយស្មើគ្នាពីជ្រុងទាំងបី។'))
    C.append(mcq('hard', 'perp_bisector_inter', 'ចំណុចប្រសព្វនៃមេដ្យាទ័រជ្រុងទាំងបីនៃត្រីកោណមួយ ឋិតនៅស្មើចម្ងាយពី ៖', M('\\text{កំពូលទាំងបីនៃត្រីកោណ}'), [M('\\text{ជ្រុងទាំងបីនៃត្រីកោណ}'), M('\\text{កម្ពស់ទាំងបី}'), M('\\text{បន្ទាត់ពុះមុំ}')], 'មេដ្យាទ័រជ្រុងទាំងបីប្រសព្វគ្នាត្រង់ផ្ចិតរង្វង់ចារឹកក្រៅត្រីកោណ ដែលស្មើចម្ងាយពីកំពូលទាំងបី (' + M('OA = OB = OC') + ')។'))
    C.append(mcq('hard', 'congruence_proof', 'អង្កត់ ' + M('AB') + ' និង ' + M('CD') + ' កាត់គ្នាត្រង់ចំណុចកណ្តាល ' + M('E') + ' នៃអង្កត់នីមួយៗ។ ត្រីកោណ ' + M('EAD') + ' និង ' + M('EBC') + ' ប៉ុនគ្នាតាម ៖', M('\\text{ជ.ម.ជ}'), [M('\\text{ម.ជ.ម}'), M('\\text{ជ.ជ.ជ}'), M('\\text{អ.ម}')], M('EA = EB, ED = EC') + ' និង ' + M('\\angle AED = \\angle BEC') + ' (មុំទល់កំពូល) នាំឱ្យប៉ុនគ្នាតាម ជ.ម.ជ។'))
    C.append(mcq('hard', 'right_pythagoras', 'ត្រីកោណកែងពីរ ' + M('ABC') + ' និង ' + M('DEF') + ' (កែងត្រង់ ' + M('A') + ' និង ' + M('D') + ') មានអ៊ីប៉ូតេនុស ' + M('BC = EF = 10\\ \\text{cm}') + ' និងជ្រុងមុំកែង ' + M('AB = DE = 6\\ \\text{cm}') + '។ ប្រវែងជ្រុង ' + M('AC') + ' ស្មើ ៖', M('8\\ \\text{cm}'), [M('4\\ \\text{cm}'), M('16\\ \\text{cm}'), M('6\\ \\text{cm}')], M('AC = \\sqrt{10^2 - 6^2} = \\sqrt{64} = 8\\ \\text{cm}') + '។'))
    C.append(mcq('hard', 'kite_diagonal', 'ក្នុងចតុកោណរាងខ្លែង ' + M('ABCD') + ' មាន ' + M('AB = BC') + ' និង ' + M('AD = CD') + '។ អង្កត់ទ្រូង ' + M('BD') + ' មានលក្ខណៈ ៖', M('\\text{ជាបន្ទាត់ពុះមុំ } \\angle B \\text{ និង } \\angle D \\text{ ហើយកែងនឹង } AC'), [M('\\text{ស្របនឹង } AC'), M('\\text{ស្មើនឹង } AC'), M('\\text{មិនកែងនឹង } AC')], M('\\Delta ABD \\cong \\Delta CBD') + ' (ជ.ជ.ជ) នាំឱ្យ ' + M('BD') + ' ជាបន្ទាត់ពុះមុំ និងជាមេដ្យាទ័រនៃ ' + M('AC') + '។'))

    # ==========================================
    # 4. MCQ PISA (5 target)
    # ==========================================
    C.append(with_img(mcq('pisa', 'pisa', 'វិស្វករម្នាក់វាស់ទទឹងទន្លេ ' + M('AB') + ' ដោយបង្កើតត្រីកោណ ' + M('\\Delta OAB \\cong \\Delta OCD') + ' (ដូចរូប)។ បើគាត់វាស់បាន ' + M('CD = 45\\ \\text{m}') + ' នោះទទឹងទន្លេ ' + M('AB') + ' ស្មើ ៖', M('45\\ \\text{m}'), [M('90\\ \\text{m}'), M('22.5\\ \\text{m}'), M('50\\ \\text{m}')], 'ដោយ ' + M('\\Delta OAB \\cong \\Delta OCD') + ' នាំឱ្យជ្រុងត្រូវគ្នា ' + M('AB = CD = 45\\ \\text{m}') + '។'), FIG_RIVER_SURVEY))
    C.append(mcq('pisa', 'pisa', 'ជាងឈើមានកំណាត់ឈើ ៤ ប្រវែង ' + M('2\\ \\text{m},\\ 4.5\\ \\text{m},\\ 5.8\\ \\text{m}') + ' និង ' + M('10.2\\ \\text{m}') + '។ ចំនួនត្រីកោណផ្សេងគ្នាដែលអាចផ្គុំបានគឺ ៖', M('2\\ \\text{ត្រីកោណ}'), [M('1\\ \\text{ត្រីកោណ}'), M('3\\ \\text{ត្រីកោណ}'), M('4\\ \\text{ត្រីកោណ}')], 'បន្សំផ្ទៀងផ្ទាត់វិសមភាពត្រីកោណមានតែ ២ គឺ ' + M('\\{2, 4.5, 5.8\\}') + ' និង ' + M('\\{4.5, 5.8, 10.2\\}') + '។'))
    C.append(mcq('pisa', 'pisa', 'គ្រោងដំបូលផ្ទះរាងត្រីកោណសមបាត ' + M('ABC') + ' មានមុំកំពូល ' + M('\\angle A = 120^\\circ') + '។ មុំបាតជម្រាលដំបូលនីមួយៗស្មើ ៖', M('30^\\circ'), [M('60^\\circ'), M('45^\\circ'), M('25^\\circ')], M('\\dfrac{180^\\circ - 120^\\circ}{2} = 30^\\circ') + '។'))
    C.append(mcq('pisa', 'pisa', 'ក្នុងវិស្វកម្មស្ពានដែក គេតែងប្រើរចនាសម្ព័ន្ធត្រីកោណ (Truss) ពីព្រោះ ៖', M('\\text{ត្រីកោណមានរាងរឹងមាំមិនប្រែប្រួលតាមលក្ខណៈ ជ.ជ.ជ}'), [M('\\text{ត្រីកោណសន្សំសំចៃដែកជាងគេ}'), M('\\text{ត្រីកោណមានទម្ងន់ធ្ងន់ជាងគេ}'), M('\\text{ត្រីកោណងាយស្រួលបត់បែន}')], 'តាមលក្ខណៈ ជ.ជ.ជ កាលណាជ្រុងទាំងបីថេរ រូបរាងត្រីកោណមិនអាចប្រែប្រួលរាងឡើយ (Triangle Rigidity)។'))
    C.append(mcq('pisa', 'pisa', 'សិស្សានុសិស្សបោះជំរំនៅចំណុច ' + M('A') + ' និង ' + M('B') + ' នៅសងខាងអូរមួយ។ ពួកគេវាស់ចម្ងាយតាមត្រីកោណប៉ុនគ្នាបាន ' + M('A\'B\' = 28.5\\ \\text{m}') + '។ ចម្ងាយ ' + M('AB') + ' ពិតប្រាកដគឺ ៖', M('28.5\\ \\text{m}'), [M('57\\ \\text{m}'), M('14.25\\ \\text{m}'), M('30\\ \\text{m}')], 'ជ្រុងត្រូវគ្នានៃត្រីកោណប៉ុនគ្នាមានប្រវែងស្មើគ្នា ៖ ' + M('AB = A\'B\' = 28.5\\ \\text{m}') + '។'))

    # ==========================================
    # 5. WRITING EASY (1 target, 5 pts total)
    # ==========================================
    W('easy', 'algebra_congruent', 'គេឱ្យ ' + M('\\Delta ABC \\cong \\Delta DEF') + ' ដែលជ្រុង ' + M('BC = 2x + 30\\ \\text{cm}') + ' និង ' + M('EF = 5x - 90\\ \\text{cm}') + '។ ក. ពន្យល់ហេតុអ្វី ' + M('BC = EF') + '។ ខ. កំណត់តម្លៃនៃ ' + M('x') + '។ គ. គណនាប្រវែងជ្រុង ' + M('BC') + '។', [
        ('ក. ដោយ ' + M('\\Delta ABC \\cong \\Delta DEF') + ' នោះជ្រុងត្រូវគ្នាប៉ុនរៀងគ្នា នាំឱ្យ ' + M('BC = EF'), 1),
        ('ខ. សមីការ ៖ ' + M('2x + 30 = 5x - 90 \\Rightarrow 5x - 2x = 30 + 90'), 1),
        (M('3x = 120 \\Rightarrow x = 40'), 1),
        ('គ. គណនាប្រវែង ' + M('BC = 2(40) + 30 = 80 + 30 = 110\\ \\text{cm}'), 1),
        ('ដូចនេះ ' + M('BC = 110\\ \\text{cm}') + ' (និង ' + M('EF = 110\\ \\text{cm}') + ')', 1)])

    # ==========================================
    # 6. WRITING MEDIUM (4 target, 5 pts total each)
    # ==========================================
    W('medium', 'midpoint_segments', 'អង្កត់ ' + M('AB') + ' និង ' + M('CD') + ' ប្រសព្វគ្នាត្រង់ចំណុចកណ្តាល ' + M('E') + ' នៃអង្កត់នីមួយៗ (' + M('EA = EB') + ' និង ' + M('EC = ED') + ')។ ក. ប្រៀបធៀបត្រីកោណ ' + M('EAD') + ' និង ' + M('EBC') + '។ ខ. ទាញបញ្ជាក់ថា ' + M('AD = BC') + '។ គ. បង្ហាញថាអង្កត់ ' + M('AD \\parallel BC') + '។', [
        ('ក. ក្នុង ' + M('\\Delta EAD') + ' និង ' + M('\\Delta EBC') + ' មាន ' + M('EA = EB') + ' និង ' + M('ED = EC'), 1),
        (M('\\angle AED = \\angle BEC') + ' (មុំទល់កំពូល) នាំឱ្យ ' + M('\\Delta EAD \\cong \\Delta EBC') + ' (តាម ជ.ម.ជ)', 1),
        ('ខ. វិបាក ៖ ជ្រុងត្រូវគ្នាប៉ុនគ្នា នាំឱ្យ ' + M('AD = BC'), 1),
        ('គ. វិបាក ៖ មុំត្រូវគ្នា ' + M('\\angle EAD = \\angle EBC'), 1),
        ('ដោយមុំទាំងពីរជាមុំឆ្លាស់ក្នុង នាំឱ្យ ' + M('AD \\parallel BC'), 1)])

    W('medium', 'tri_ineq_check', 'គេឱ្យរង្វាស់ជ្រុងបីករណី ៖ ក. ' + M('11,\\ 12,\\ 17') + ' \t ខ. ' + M('1,\\ 2,\\ 3') + ' \t គ. ' + M('4.1,\\ 4.7,\\ 9') + '។ ចំពោះករណីនីមួយៗ តើគេអាចគូសបានត្រីកោណមួយឬទេ? ព្រោះអ្វី?', [
        ('ក. ' + M('11 + 12 = 23 > 17') + ' (ផលបូកពីរជ្រុងធំជាងជ្រុងទីបី) នាំឱ្យអាចគូសបានត្រីកោណ', 2),
        ('ខ. ' + M('1 + 2 = 3') + ' (ផលបូកស្មើជ្រុងទីបី ចំណុចរត់ត្រង់ជួរ) នាំឱ្យមិនអាចគូសបានត្រីកោណទេ', 1),
        ('គ. ' + M('4.1 + 4.7 = 8.8 < 9') + ' (ផលបូកតូចជាងជ្រុងទីបី) នាំឱ្យមិនអាចគូសបានត្រីកោណទេ', 2)])

    W('medium', 'isosceles_heights', M('\\Delta ABC') + ' ជាត្រីកោណសមបាតកំពូល ' + M('A') + ' (' + M('AB = AC') + ')។ កម្ពស់គូសចេញពី ' + M('B') + ' និង ' + M('C') + ' កាត់ជ្រុង ' + M('AC') + ' និង ' + M('AB') + ' ត្រង់ ' + M('D') + ' និង ' + M('E') + ' រៀងគ្នា។ ក. បង្ហាញថា ' + M('\\Delta BDC') + ' និង ' + M('\\Delta CEB') + ' ជាត្រីកោណកែង។ ខ. បង្ហាញថា ' + M('\\Delta BDC \\cong \\Delta CEB') + '។ គ. ទាញវិបាកថា ' + M('BD = CE') + '។', [
        ('ក. ' + M('BD \\perp AC \\Rightarrow \\angle BDC = 90^\\circ') + ' និង ' + M('CE \\perp AB \\Rightarrow \\angle CEB = 90^\\circ'), 1),
        ('ខ. ក្នុងត្រីកោណកែងទាំងពីរមាន អ៊ីប៉ូតេនុស ' + M('BC') + ' ជាជ្រុងរួម', 1),
        ('មុំស្រួច ' + M('\\angle DCB = \\angle EBC') + ' (មុំបាតនៃត្រីកោណសមបាត ' + M('ABC') + ')', 1),
        ('ដូចនេះ ' + M('\\Delta BDC \\cong \\Delta CEB') + ' (តាមលក្ខខណ្ឌ អ.ម)', 1),
        ('គ. វិបាក ៖ ជ្រុងត្រូវគ្នាប៉ុនគ្នា នាំឱ្យ ' + M('BD = CE') + ' (កម្ពស់ទាំងពីរប៉ុនគ្នា)', 1)])

    W('medium', 'perp_oblique_proof', 'គេឱ្យចំណុច ' + M('A') + ' មិននៅលើបន្ទាត់ ' + M('\\Delta') + '។ ' + M('AH \\perp \\Delta') + ' ត្រង់ ' + M('H') + '។ ចំណុច ' + M('B') + ' និង ' + M('C') + ' នៅលើ ' + M('\\Delta') + ' ដោយ ' + M('HB = HC') + '។ ក. ប្រៀបធៀបត្រីកោណកែង ' + M('AHB') + ' និង ' + M('AHC') + '។ ខ. ទាញបញ្ជាក់ថា ' + M('AB = AC') + '។ គ. បញ្ជាក់ប្រភេទនៃ ' + M('\\Delta ABC') + '។', [
        ('ក. ក្នុងត្រីកោណកែង ' + M('AHB') + ' និង ' + M('AHC') + ' មាន ' + M('AH') + ' ជាជ្រុងរួម', 1),
        (M('HB = HC') + ' (សម្មតិកម្ម) នាំឱ្យ ' + M('\\Delta AHB \\cong \\Delta AHC') + ' (តាម ជ.ម.ជ)', 1),
        ('ខ. វិបាក ៖ អ៊ីប៉ូតេនុសត្រូវគ្នាប៉ុនគ្នា នាំឱ្យ ' + M('AB = AC'), 2),
        ('គ. ដោយ ' + M('AB = AC') + ' នោះ ' + M('\\Delta ABC') + ' ជាត្រីកោណសមបាតកំពូល ' + M('A'), 1)], FIG_PERP_BISECTOR)

    # ==========================================
    # 7. WRITING HARD (4 target, 5 pts total each)
    # ==========================================
    W('hard', 'angle_expressions', 'ក្នុង ' + M('\\Delta ABC') + ' មាន ' + M('\\angle A = 6x + 4^\\circ') + ', ' + M('\\angle B = 7x + 12^\\circ') + ' និង ' + M('\\angle C = 6x - 7^\\circ') + '។ ក. រកតម្លៃនៃ ' + M('x') + '។ ខ. គណនារង្វាស់មុំ ' + M('\\angle A, \\angle B, \\angle C') + '។ គ. រៀបប្រវែងជ្រុងតាមលំដាប់ពីធំទៅតូច។', [
        ('ក. ផលបូកមុំក្នុង ៖ ' + M('(6x+4) + (7x+12) + (6x-7) = 180^\\circ \\Rightarrow 19x + 9 = 180'), 1),
        (M('19x = 171 \\Rightarrow x = 9^\\circ'), 1),
        ('ខ. ' + M('\\angle A = 58^\\circ') + ', ' + M('\\angle B = 75^\\circ') + ', ' + M('\\angle C = 47^\\circ'), 1),
        ('គ. ដោយ ' + M('\\angle B > \\angle A > \\angle C') + ' នោះជ្រុងឈមធំជាង', 1),
        ('ដូចនេះ លំដាប់ជ្រុងពីធំទៅតូចគឺ ' + M('AC > BC > AB'), 1)])

    W('hard', 'bisector_equidistant', 'កន្លះបន្ទាត់ពុះនៃ ' + M('\\angle B') + ' និង ' + M('\\angle C') + ' ក្នុង ' + M('\\Delta ABC') + ' ប្រសព្វគ្នាត្រង់ ' + M('I') + '។ គូស ' + M('ID \\perp AB, IE \\perp BC, IF \\perp AC') + '។ ក. បង្ហាញថា ' + M('\\Delta BDI \\cong \\Delta BEI') + ' រួចទាញថា ' + M('ID = IE') + '។ ខ. បង្ហាញថា ' + M('IE = IF') + '។ គ. ទាញបញ្ជាក់ថា ' + M('AI') + ' ជាកន្លះបន្ទាត់ពុះនៃ ' + M('\\angle BAC') + '។', [
        ('ក. ' + M('\\Delta BDI \\cong \\Delta BEI') + ' (អ.ម ៖ អ៊ីប៉ូតេនុស ' + M('BI') + ' រួម, ' + M('\\angle IBD = \\angle IBE') + ') នាំឱ្យ ' + M('ID = IE'), 2),
        ('ខ. ដូចគ្នា ' + M('\\Delta CEI \\cong \\Delta CFI') + ' (អ.ម) នាំឱ្យ ' + M('IE = IF') + ' ដូចនេះ ' + M('ID = IE = IF'), 1),
        ('គ. ក្នុងត្រីកោណកែង ' + M('IDA') + ' និង ' + M('IFA') + ' មាន អ៊ីប៉ូតេនុស ' + M('AI') + ' រួម និង ' + M('ID = IF'), 1),
        ('នាំឱ្យ ' + M('\\Delta IDA \\cong \\Delta IFA') + ' (អ.ជ) ទាញបាន ' + M('\\angle IAD = \\angle IAF') + ' ដូចនេះ ' + M('AI') + ' ជាកន្លះបន្ទាត់ពុះ', 1)])

    W('hard', 'kite_congruence', 'ចតុកោណ ' + M('ABCD') + ' មាន ' + M('AB = BC') + ' និង ' + M('AD = CD') + ' (រាងខ្លែង)។ ' + M('E') + ' ជាចំណុចនៅលើអង្កត់ទ្រូង ' + M('BD') + '។ ក. បង្ហាញថា ' + M('\\Delta ABD \\cong \\Delta CBD') + '។ ខ. ទាញបញ្ជាក់ថា ' + M('\\angle ADE = \\angle CDE') + '។ គ. បង្ហាញថា ' + M('\\Delta AED \\cong \\Delta CED') + '។', [
        ('ក. ក្នុង ' + M('\\Delta ABD') + ' និង ' + M('\\Delta CBD') + ' មាន ' + M('AB = BC, AD = CD') + ' និង ' + M('BD') + ' ជាជ្រុងរួម', 1),
        ('ដូចនេះ ' + M('\\Delta ABD \\cong \\Delta CBD') + ' (តាមលក្ខខណ្ឌ ជ.ជ.ជ)', 1),
        ('ខ. វិបាក ៖ មុំត្រូវគ្នាប៉ុនគ្នា នាំឱ្យ ' + M('\\angle ADB = \\angle CDB') + ' ឬ ' + M('\\angle ADE = \\angle CDE'), 1),
        ('គ. ក្នុង ' + M('\\Delta AED') + ' និង ' + M('\\Delta CED') + ' មាន ' + M('AD = CD') + ', ' + M('\\angle ADE = \\angle CDE') + ' និង ' + M('ED') + ' ជាជ្រុងរួម', 1),
        ('ដូចនេះ ' + M('\\Delta AED \\cong \\Delta CED') + ' (តាមលក្ខខណ្ឌ ជ.ម.ជ)', 1)])

    W('hard', 'sum_heights_less_perimeter', 'គេឱ្យ ' + M('AD, BE, CF') + ' ជាកម្ពស់ទាំងបីនៃត្រីកោណ ' + M('ABC') + '។ ក. ប្រៀបធៀបកម្ពស់ ' + M('AD') + ' ជាមួយជ្រុង ' + M('AB') + '។ ខ. ប្រៀបធៀបកម្ពស់ ' + M('BE') + ' ជាមួយ ' + M('BC') + ' និង ' + M('CF') + ' ជាមួយ ' + M('AC') + '។ គ. បង្ហាញថា ' + M('AB + BC + AC > AD + BE + CF') + '។', [
        ('ក. ក្នុងត្រីកោណកែង ' + M('ADB') + ' អង្កត់កែងខ្លីជាងអ៊ីប៉ូតេនុស នាំឱ្យ ' + M('AD < AB'), 1.5),
        ('ខ. ដូចគ្នា ក្នុងត្រីកោណកែង ' + M('BEC') + ' បាន ' + M('BE < BC') + ' និងក្នុង ' + M('CFA') + ' បាន ' + M('CF < AC'), 1.5),
        ('គ. បូកវិសមភាពទាំងបីអង្គនិងអង្គ ៖ ' + M('AD + BE + CF < AB + BC + AC'), 1),
        ('ឬ ' + M('AB + BC + AC > AD + BE + CF') + ' (បរិមាត្រធំជាងផលបូកកម្ពស់ទាំងបី)', 1)])

    # ==========================================
    # 8. WRITING PISA (5 target, 5 pts total each)
    # ==========================================
    W('pisa', 'river_width', 'ដើម្បីវាស់ទទឹងស្ទឹងពីចំណុច ' + M('A') + ' ទៅ ' + M('B') + ' (' + M('AB \\perp AC') + ') វិស្វករដៅ ' + M('O') + ' ជាចំណុចកណ្តាលនៃ ' + M('AC') + ' (' + M('OA = OC') + ') រួចដើរកែងនឹង ' + M('AC') + ' ដល់ ' + M('D') + ' ត្រង់ជួរនឹង ' + M('B, O') + ' (ដូចរូប)។ ក. បង្ហាញថា ' + M('\\Delta OAB \\cong \\Delta OCD') + '។ ខ. បញ្ជាក់ករណីប៉ុនគ្នា។ គ. បើវាស់បាន ' + M('CD = 38\\ \\text{m}') + ' រកទទឹងស្ទឹង ' + M('AB') + '។', [
        ('ក. ក្នុង ' + M('\\Delta OAB') + ' និង ' + M('\\Delta OCD') + ' មាន ' + M('\\angle OAB = \\angle OCD = 90^\\circ') + ' និង ' + M('OA = OC'), 1),
        (M('\\angle AOB = \\angle COD') + ' (មុំទល់កំពូល)', 1),
        ('ដូចនេះ ' + M('\\Delta OAB \\cong \\Delta OCD'), 1),
        ('ខ. ត្រីកោណទាំងពីរប៉ុនគ្នាតាមករណី ម.ជ.ម (Angle-Side-Angle)', 1),
        ('គ. វិបាក ៖ ' + M('AB = CD = 38\\ \\text{m}') + ' ដូចនេះទទឹងស្ទឹងគឺ ' + M('38\\ \\text{m}'), 1)], FIG_RIVER_SURVEY)

    W('pisa', 'garden_fence', 'សុខាមានកំណាត់ឈើ ៤ ប្រវែង ' + M('2\\ \\text{m},\\ 4.5\\ \\text{m},\\ 5.8\\ \\text{m},\\ 10.2\\ \\text{m}') + ' សម្រាប់ធ្វើស៊ុមត្រីកោណព័ទ្ធសួនផ្កា។ ក. សរសេរបន្សំទាំង ៤ ដែលអាចរើសឈើ ៣ កំណាត់។ ខ. ពិនិត្យវិសមភាពត្រីកោណលើបន្សំនីមួយៗ។ គ. សន្និដ្ឋានចំនួនត្រីកោណដែលអាចបង្កើតបាន។', [
        ('ក. បន្សំទាំង ៤ ៖ ' + M('\\{2, 4.5, 5.8\\},\\ \\{2, 4.5, 10.2\\},\\ \\{2, 5.8, 10.2\\},\\ \\{4.5, 5.8, 10.2\\}'), 1),
        ('ខ. ' + M('\\{2, 4.5, 5.8\\} \\colon 2 + 4.5 = 6.5 > 5.8') + ' (បានត្រីកោណ)', 1),
        (M('\\{2, 4.5, 10.2\\} \\colon 2 + 4.5 = 6.5 < 10.2') + ' (មិនបាន), ' + M('\\{2, 5.8, 10.2\\} \\colon 2 + 5.8 = 7.8 < 10.2') + ' (មិនបាន)', 1),
        (M('\\{4.5, 5.8, 10.2\\} \\colon 4.5 + 5.8 = 10.3 > 10.2') + ' (បានត្រីកោណ)', 1),
        ('គ. សន្និដ្ឋាន ៖ សុខាអាចបង្កើតត្រីកោណខុសៗគ្នាបានតែ 2 ប៉ុណ្ណោះ', 1)])

    W('pisa', 'roof_truss', 'គ្រោងដំបូលផ្ទះរាងត្រីកោណសមបាត ' + M('ABC') + ' កំពូល ' + M('A') + ' មានកម្ពស់ ' + M('AH \\perp BC') + '។ ក. បង្ហាញថា ' + M('\\Delta AHB \\cong \\Delta AHC') + ' (តាម អ.ជ)។ ខ. ទាញបញ្ជាក់ថា ' + M('H') + ' ជាចំណុចកណ្តាលនៃ ' + M('BC') + '។ គ. បើធ្នឹមបាត ' + M('BC = 8\\ \\text{m}') + ' និងកម្ពស់ ' + M('AH = 3\\ \\text{m}') + ' គណនាប្រវែងជើងធ្នឹម ' + M('AB') + '។', [
        ('ក. ក្នុងត្រីកោណកែងទាំងពីរមាន ' + M('AH') + ' ជាជ្រុងរួម និងអ៊ីប៉ូតេនុស ' + M('AB = AC') + ' (សមបាត)', 1),
        ('ដូចនេះ ' + M('\\Delta AHB \\cong \\Delta AHC') + ' (តាមលក្ខខណ្ឌ អ.ជ)', 1),
        ('ខ. វិបាក ៖ ' + M('HB = HC = \\dfrac{BC}{2} = \\dfrac{8}{2} = 4\\ \\text{m}') + ' នាំឱ្យ ' + M('H') + ' ជាចំណុចកណ្តាលនៃ ' + M('BC'), 1),
        ('គ. តាមទ្រឹស្តីបទពីតាករក្នុង ' + M('\\Delta AHB') + ' ៖ ' + M('AB^2 = AH^2 + HB^2 = 3^2 + 4^2 = 9 + 16 = 25'), 1),
        (M('AB = \\sqrt{25} = 5\\ \\text{m}') + ' ដូចនេះប្រវែងជើងធ្នឹមគឺ ' + M('AB = AC = 5\\ \\text{m}'), 1)])

    W('pisa', 'tri_rigidity', 'ក្នុងវិស្វកម្មសំណង់ គេតែងរៀបរចនាសម្ព័ន្ធដែកជាទម្រង់ត្រីកោណ (Truss Structure)។ ក. ពន្យល់ហេតុផលធរណីមាត្រតាមករណី ជ.ជ.ជ។ ខ. ប្រៀបធៀបរវាងស៊ុមចតុកោណ និងស៊ុមត្រីកោណ ពេលរងកម្លាំងរុញ។ គ. បញ្ជាក់វិធីធ្វើឱ្យស៊ុមចតុកោណរឹងមាំដូចត្រីកោណ។', [
        ('ក. តាមករណី ជ.ជ.ជ កាលណាប្រវែងជ្រុងទាំងបីថេរ រូបរាងនិងមុំនៃត្រីកោណមិនអាចប្រែប្រួលរាងបានឡើយ', 2),
        ('ខ. ស៊ុមចតុកោណអាចបត់ទ្រេតទៅជាប្រលេឡូក្រាមពេលរងកម្លាំងពីចំហៀង ឯត្រីកោណរក្សារូបរាងដដែល', 1),
        ('គ. វិធីដោះស្រាយ ៖ គេដាក់អង្កត់ទ្រូងមួយខ្វែងកណ្តាលចតុកោណ (Cross-bracing)', 1),
        ('ដើម្បីបំបែកចតុកោណទៅជាត្រីកោណពីរដែលរឹងមាំទប់ទល់នឹងកម្លាំងរុញច្រាន', 1)])

    W('pisa', 'accessible_survey', 'សិស្សានុសិស្សចង់វាស់ចម្ងាយរវាងដើមឈើពីរដើម ' + M('A') + ' និង ' + M('B') + ' នៅត្រើយម្ខាងស្រះ។ ពួកគេដៅ ' + M('O') + ' រួចបន្លាយ ' + M('AO') + ' ឱ្យបាន ' + M('OA\' = OA') + ' និងបន្លាយ ' + M('BO') + ' ឱ្យបាន ' + M('OB\' = OB') + '។ ក. បង្ហាញថា ' + M('\\Delta OAB \\cong \\Delta OA\'B\'') + '។ ខ. ទាញបញ្ជាក់ថា ' + M('AB = A\'B\'') + '។ គ. បើវាស់បាន ' + M('A\'B\' = 24.5\\ \\text{m}') + ' រកចម្ងាយ ' + M('AB') + '។', [
        ('ក. ក្នុង ' + M('\\Delta OAB') + ' និង ' + M('\\Delta OA\'B\'') + ' មាន ' + M('OA = OA\'') + ' និង ' + M('OB = OB\''), 1),
        (M('\\angle AOB = \\angle A\'OB\'') + ' (មុំទល់កំពូល) នាំឱ្យ ' + M('\\Delta OAB \\cong \\Delta OA\'B\'') + ' (តាម ជ.ម.ជ)', 1),
        ('ខ. វិបាក ៖ ជ្រុងត្រូវគ្នាប៉ុនរៀងគ្នា នាំឱ្យ ' + M('AB = A\'B\''), 1),
        ('គ. ដោយវាស់បាន ' + M('A\'B\' = 24.5\\ \\text{m}') + ' នៅលើទីវាលស្ងួត', 1),
        ('ដូចនេះ ចម្ងាយរវាងដើមឈើទាំងពីរគឺ ' + M('AB = 24.5\\ \\text{m}'), 1)])

    return C
