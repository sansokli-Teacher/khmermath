"""G11 Lesson 9 — អនុគមន៍ត្រីកោណមាត្រ.  Parts (sec tag prefix): sec1 រង្វាស់មុំ, sec2 អនុគមន៍ត្រីកោណមាត្រ,
sec3 លក្ខណៈនៃអនុគមន៍ត្រីកោណមាត្រ, sec4 ការសិក្សាអនុគមន៍ត្រីកោណមាត្រ (see gen11sc/parts.py).
Numeric answers are computed with math and re-checked at import."""
from math import pi, sin, cos, tan, radians, sqrt, isclose
from lib import M, mcq, wr

LESSON = 'អនុគមន៍ត្រីកោណមាត្រ'
CHAPTER = 'ជំពូកទី 3 : អនុគមន៍ត្រីកោណមាត្រ'


def with_img(q, svg):
    q['img'] = svg
    return q


cot = lambda t: cos(t) / sin(t)


def opts(*xs): return [M(str(x)) for x in xs]


# ---- import-time checks of every closed form used below ---------------------------------------------------------
def near(a, b, t=1e-9): return abs(a - b) < t


assert near(sin(pi / 6), 1 / 2) and near(cos(pi / 3), 1 / 2) and near(tan(pi / 4), 1)
assert near(cos(2 * pi / 3), -1 / 2) and near(sin(5 * pi / 4), -sqrt(2) / 2) and near(tan(5 * pi / 6), -sqrt(3) / 3)
assert near(2 * sin(pi / 3) + 4 * cos(pi / 6) - 3 * tan(pi / 3) + 4 * cot(pi / 4), 4)
assert near((5 - 4 * tan(pi / 4) ** 2 + cot(pi / 3) ** 2) / (2 * cos(pi / 3) ** 2 - 2 * sin(pi / 2) ** 3 + 4 * tan(pi / 4)), 8 / 15)
assert near(2 * sin(pi / 4) ** 2 - 3 * tan(pi / 6) ** 2 + 2 * cos(pi / 2) ** 2 + 3 * cot(pi / 4) ** 2, 3)
assert near(sin(radians(150)), 1 / 2) and near(cos(pi + pi / 6), -sqrt(3) / 2) and near(sin(-pi / 3), -sqrt(3) / 2)
assert near(cos(-17 * pi / 3), 1 / 2) and near(sin(radians(870)), 1 / 2) and near(cot(25 * pi / 4), 1)
assert near((5 * (4 / 15) + 7) / (6 - 3 * (4 / 15)), 125 / 78)
assert near((4 / 3 + 3 / 4) / (4 / 3 - 3 / 4), 25 / 7)
assert near(((cot(radians(44)) + tan(radians(226))) * cos(radians(406))) / cos(radians(316)) - cot(radians(72)) * cot(radians(18)), 1)
assert near(12 + 10 * sin(7 * pi / 6), 7) and near(12 + 10 * sin(13 * pi / 2), 22)
assert near(8 * (5 * pi / 6), 20 * pi / 3) and near(12 * (2 * pi / 3), 8 * pi) and near(5 * 2 * pi * 0.35, 3.5 * pi)
assert near(2 * pi / 100 / pi, 0.02) and near(pi / (pi / 6), 6)
s_c = (0.25 - 1) / 2
assert near(s_c, -3 / 8) and near(-0.5 * (1 - s_c), -11 / 16)

# ---- figures -------------------------------------------------------------------------------------------------------
FIG_UNIT = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 260 220' width='260' height='220'>"
            "<line x1='20' y1='110' x2='245' y2='110' stroke='#94a3b8'/><line x1='110' y1='15' x2='110' y2='205' stroke='#94a3b8'/>"
            "<circle cx='110' cy='110' r='85' fill='none' stroke='#475569' stroke-width='1.8'/>"
            "<line x1='110' y1='110' x2='%.1f' y2='%.1f' stroke='#1d4ed8' stroke-width='2'/>" % (110 + 85 * cos(radians(40)), 110 - 85 * sin(radians(40))) +
            "<line x1='%.1f' y1='110' x2='%.1f' y2='%.1f' stroke='#94a3b8' stroke-dasharray='4,3'/>" % (110 + 85 * cos(radians(40)), 110 + 85 * cos(radians(40)), 110 - 85 * sin(radians(40))) +
            "<line x1='110' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#94a3b8' stroke-dasharray='4,3'/>" % (110 - 85 * sin(radians(40)), 110 + 85 * cos(radians(40)), 110 - 85 * sin(radians(40))) +
            "<line x1='110' y1='110' x2='%.1f' y2='110' stroke='#dc2626' stroke-width='3'/>" % (110 + 85 * cos(radians(40))) +
            "<line x1='110' y1='110' x2='110' y2='%.1f' stroke='#0d9488' stroke-width='3'/>" % (110 - 85 * sin(radians(40))) +
            "<circle cx='%.1f' cy='%.1f' r='3.5' fill='#1d4ed8'/>" % (110 + 85 * cos(radians(40)), 110 - 85 * sin(radians(40))) +
            "<text x='%.1f' y='%.1f' font-family='Times New Roman, serif' font-size='14' fill='#1d4ed8'>P</text>" % (110 + 85 * cos(radians(40)) + 6, 110 - 85 * sin(radians(40)) - 4) +
            "<text x='128' y='126' font-family='Times New Roman, serif' font-size='13' fill='#dc2626'>cos θ</text>"
            "<text x='60' y='80' font-family='Times New Roman, serif' font-size='13' fill='#0d9488'>sin θ</text>"
            "<text x='132' y='105' font-family='Times New Roman, serif' font-size='13' fill='#1d4ed8'>θ</text></svg>")


def _sine_pts():
    return ' '.join('%.1f,%.1f' % (30 + 55 * x, 80 - 55 * sin(pi * x)) for x in [i / 40 for i in range(-20, 61)] if True)


FIG_SIN = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 170' width='400' height='170'>"
           "<line x1='5' y1='80' x2='395' y2='80' stroke='#94a3b8'/><line x1='140' y1='10' x2='140' y2='150' stroke='#94a3b8'/>"
           "<polyline fill='none' stroke='#1d4ed8' stroke-width='2' points='" + ' '.join('%.1f,%.1f' % (140 + 55 * x, 80 - 55 * sin(pi * x)) for x in [i / 40 for i in range(-48, 88)]) + "'/>"
           "<text x='190' y='98' font-family='Times New Roman, serif' font-size='12' fill='#334155'>π</text>"
           "<text x='243' y='98' font-family='Times New Roman, serif' font-size='12' fill='#334155'>2π</text>"
           "<text x='146' y='20' font-family='Times New Roman, serif' font-size='12' fill='#334155'>1</text></svg>")


def cands():
    C = []

    # ============================ PART 1: រង្វាស់មុំ ============================
    C.append(mcq('easy', 'sec1_a', M('180^\\circ') + ' ស្មើនឹងប៉ុន្មានរ៉ាដ្យង់ ?', M('\\pi'), [M('\\dfrac\\pi2'), M('2\\pi'), M('\\dfrac{\\pi}{180}')],
                 M('360^\\circ=2\\pi') + ' ដូច្នេះ ' + M('180^\\circ=\\pi') + '។', 'Remember'))
    C.append(mcq('easy', 'sec1_a', M('\\dfrac\\pi2') + ' រ៉ាដ្យង់ ស្មើនឹងប៉ុន្មានដឺក្រេ ?', M('90^\\circ'), [M('45^\\circ'), M('180^\\circ'), M('60^\\circ')],
                 M('\\dfrac\\pi2\\times\\dfrac{180^\\circ}{\\pi}=90^\\circ') + '។', 'Apply'))
    C.append(mcq('easy', 'sec1_a', M('1') + ' រ៉ាដ្យង់ មានរង្វាស់ប្រហែល ៖', M('57^\\circ'), [M('1^\\circ'), M('90^\\circ'), M('180^\\circ')], M('1\\text{ rd}=\\dfrac{180^\\circ}{\\pi}\\approx57^\\circ') + '។', 'Remember'))
    C.append(mcq('medium', 'sec1_b', 'ប្តូរ ' + M('-135^\\circ') + ' ជារ៉ាដ្យង់ ៖', M('-\\dfrac{3\\pi}{4}'), [M('\\dfrac{3\\pi}{4}'), M('-\\dfrac{3\\pi}{2}'), M('-\\dfrac{4\\pi}{3}')],
                 M('-135\\times\\dfrac\\pi{180}=-\\dfrac{3\\pi}4') + '។', 'Apply'))
    C.append(mcq('medium', 'sec1_b', 'ប្តូរ ' + M('\\dfrac{7\\pi}{6}') + ' ជាដឺក្រេ ៖', M('210^\\circ'), [M('150^\\circ'), M('240^\\circ'), M('105^\\circ')], M('\\dfrac{7\\pi}6\\times\\dfrac{180^\\circ}\\pi=210^\\circ') + '។', 'Apply'))
    C.append(mcq('hard', 'sec1_b', 'រង្វង់កាំ ' + M('8\\text{ cm}') + ' មានមុំផ្ចិត ' + M('150^\\circ') + '។ ប្រវែងធ្នូ (cm) គឺ ៖', M('\\dfrac{20\\pi}{3}\\approx20.94'), [M('\\dfrac{40\\pi}{3}\\approx41.89'), M('\\dfrac{5\\pi}{6}\\approx2.62'), M('150\\pi')],
                 M('150^\\circ=\\dfrac{5\\pi}6') + ' ហើយ ' + M('s=\\alpha r=\\dfrac{5\\pi}6\\times8=\\dfrac{20\\pi}3') + '។', 'Analyze'))
    C.append(mcq('pisa', 'sec1_c', 'ម្ជុលនាទីនាឡិកាមួយប្រវែង ' + M('12\\text{ cm}') + ' ដើរបាន ២០ នាទី ។ ចុងម្ជុលធ្វើដំណើរបានប្រវែងធ្នូ (cm) ៖', M('8\\pi\\approx25.13'), [M('4\\pi'), M('12\\pi'), M('\\dfrac{2\\pi}{3}')],
                 '២០ នាទី ' + M('=\\dfrac13') + ' ជុំ ' + M('=\\dfrac{2\\pi}3') + ' ហើយ ' + M('s=12\\times\\dfrac{2\\pi}3=8\\pi') + '។', 'Evaluate'))
    C.append(mcq('pisa', 'sec1_c', 'កង់ជិះកង់មានកាំ ' + M('35\\text{ cm}') + ' វិលបាន ៥ ជុំ ។ ចម្ងាយដែលកង់រំកិលបាន (m) គឺ ៖', M('3.5\\pi\\approx11.0'), [M('1.75\\pi\\approx5.5'), M('7\\pi\\approx22.0'), M('0.35\\pi\\approx1.1')],
                 M('5\\times2\\pi\\times0.35=3.5\\pi') + ' ម៉ែត្រ។', 'Evaluate'))
    C.append(wr('easy', 'sec1_a', 'ប្តូរ ' + M('225^\\circ') + ' ជារ៉ាដ្យង់ និង ' + M('-\\dfrac{7\\pi}{6}') + ' ជាដឺក្រេ ។',
                [('ប្រើ ' + M('1^\\circ=\\dfrac\\pi{180}') + '។', 1), (M('225\\times\\dfrac\\pi{180}=\\dfrac{5\\pi}4') + '។', 1), ('ប្រើ ' + M('1\\text{ rd}=\\dfrac{180^\\circ}\\pi') + '។', 1),
                 (M('-\\dfrac{7\\pi}6\\times\\dfrac{180^\\circ}\\pi') + '។', 1), (M('=-210^\\circ') + '។', 1)], 'Apply'))
    C.append(wr('medium', 'sec1_b', 'រង្វង់កាំ ' + M('6\\text{ cm}') + ' មានមុំផ្ចិត ' + M('120^\\circ') + '។ គណនាប្រវែងធ្នូ ។',
                [('ប្តូរ ' + M('120^\\circ=120\\times\\dfrac\\pi{180}') + '។', 1), (M('=\\dfrac{2\\pi}3') + ' rd។', 1), ('ប្រើ ' + M('s=\\alpha r') + '។', 1),
                 (M('s=\\dfrac{2\\pi}3\\times6=4\\pi') + '។', 1), (M('s\\approx12.57\\text{ cm}') + '។', 1)], 'Apply'))
    C.append(wr('pisa', 'sec1_c', 'កង់ទាញកាំ ' + M('20\\text{ m}') + ' វិលបាន ' + M('\\dfrac38') + ' ជុំ ។ រកមុំវិល (rd) និងប្រវែងធ្នូដែលអ្នកជិះធ្វើដំណើរ ។',
                [('មួយជុំ ' + M('=2\\pi') + ' rd។', 1), ('មុំ ' + M('\\alpha=\\dfrac38\\times2\\pi') + '។', 1), (M('\\alpha=\\dfrac{3\\pi}4\\approx2.36\\text{ rd}') + '។', 1),
                 ('ប្រវែងធ្នូ ' + M('s=\\alpha r=\\dfrac{3\\pi}4\\times20') + '។', 1), (M('s=15\\pi\\approx47.12\\text{ m}') + '។', 1)], 'Evaluate'))

    # ============================ PART 2: អនុគមន៍ត្រីកោណមាត្រ ============================
    C.append(with_img(mcq('easy', 'sec2_a', 'ក្នុងរង្វង់ឯកតា ចំណុច ' + M('P') + ' ត្រូវនឹងមុំ ' + M('\\theta') + '។ កូអរដោនេនៃ ' + M('P') + ' គឺ ៖', M('(\\cos\\theta,\\ \\sin\\theta)'),
                       [M('(\\sin\\theta,\\ \\cos\\theta)'), M('(\\tan\\theta,\\ \\cot\\theta)'), M('(\\theta,\\ \\sin\\theta)')], 'ចំណោលកែងលើអ័ក្សដេក ' + M('=\\cos\\theta') + ' លើអ័ក្សឈរ ' + M('=\\sin\\theta') + '។', 'Remember'), FIG_UNIT))
    C.append(mcq('easy', 'sec2_a', M('\\sin\\dfrac\\pi6') + ' ស្មើនឹង ៖', M('\\dfrac12'), [M('\\dfrac{\\sqrt3}2'), M('\\dfrac{\\sqrt2}2'), M('1')], 'តារាងតម្លៃមុំពិសេស។', 'Remember'))
    C.append(mcq('easy', 'sec2_a', M('\\tan\\dfrac\\pi4') + ' ស្មើនឹង ៖', M('1'), [M('0'), M('\\sqrt3'), M('\\dfrac{\\sqrt3}3')], M('\\tan\\dfrac\\pi4=\\dfrac{\\sin}{\\cos}=\\dfrac{\\sqrt2/2}{\\sqrt2/2}=1') + '។', 'Remember'))
    C.append(mcq('medium', 'sec2_b', M('\\cos\\dfrac{2\\pi}{3}') + ' ស្មើនឹង ៖', M('-\\dfrac12'), [M('\\dfrac12'), M('-\\dfrac{\\sqrt3}2'), M('\\dfrac{\\sqrt3}2')], 'មុំនៅកាដ្រង់ II កូស៊ីនុសអវិជ្ជមាន ហើយ ' + M('\\cos\\dfrac{2\\pi}3=-\\dfrac12') + '។', 'Apply'))
    C.append(mcq('medium', 'sec2_b', M('\\sin\\dfrac{5\\pi}{4}') + ' ស្មើនឹង ៖', M('-\\dfrac{\\sqrt2}2'), [M('\\dfrac{\\sqrt2}2'), M('-\\dfrac12'), M('-1')], 'កាដ្រង់ III ស៊ីនុសអវិជ្ជមាន។', 'Apply'))
    C.append(mcq('medium', 'sec2_b', M('\\tan\\dfrac{5\\pi}{6}') + ' ស្មើនឹង ៖', M('-\\dfrac{\\sqrt3}3'), [M('\\dfrac{\\sqrt3}3'), M('-\\sqrt3'), M('\\sqrt3')], 'កាដ្រង់ II តង់សង់អវិជ្ជមាន ' + M('\\tan\\dfrac{5\\pi}6=-\\dfrac{\\sqrt3}3') + '។', 'Apply'))
    C.append(mcq('hard', 'sec2_a', M('2\\sin\\dfrac\\pi3+4\\cos\\dfrac\\pi6-3\\tan\\dfrac\\pi3+4\\cot\\dfrac\\pi4') + ' ស្មើនឹង ៖', M('4'), opts(2, 0, '4+\\sqrt3'),
                 M('\\sqrt3+2\\sqrt3-3\\sqrt3+4=4') + '។', 'Analyze'))
    C.append(mcq('hard', 'sec2_a', M('\\dfrac{5-4\\tan^245^\\circ+\\cot^260^\\circ}{2\\cos^260^\\circ-2\\sin^390^\\circ+4\\tan45^\\circ}') + ' ស្មើនឹង ៖', M('\\dfrac8{15}'), [M('\\dfrac{15}8'), M('\\dfrac4{5}'), M('\\dfrac{2}{3}')],
                 M('\\dfrac{1+\\frac13}{\\frac12-2+4}=\\dfrac{4/3}{5/2}=\\dfrac8{15}') + '។', 'Analyze'))
    C.append(mcq('pisa', 'sec2_b', 'ជណ្ដើរវែង ' + M('5\\text{ m}') + ' ផ្អៀងនឹងជញ្ជាំងបង្កើតមុំ ' + M('60^\\circ') + ' នឹងដី ។ កម្ពស់ដែលជណ្ដើរឡើងដល់ (m) គឺ ៖', M('\\dfrac{5\\sqrt3}2\\approx4.33'), [M('\\dfrac52=2.5'), M('5\\sqrt3\\approx8.66'), M('\\dfrac{5\\sqrt2}{2}\\approx3.54')],
                 M('h=5\\sin60^\\circ=\\dfrac{5\\sqrt3}2') + '។', 'Evaluate'))
    C.append(wr('medium', 'sec2_b', 'គណនា ' + M('A=2\\sin^2\\dfrac\\pi4-3\\tan^2\\dfrac\\pi6+2\\cos^2\\dfrac\\pi2+3\\cot^2\\dfrac\\pi4') + '។',
                [(M('\\sin\\dfrac\\pi4=\\dfrac{\\sqrt2}2\\Rightarrow2\\sin^2\\dfrac\\pi4=1') + '។', 1), (M('\\tan\\dfrac\\pi6=\\dfrac{\\sqrt3}3\\Rightarrow3\\tan^2\\dfrac\\pi6=1') + '។', 1),
                 (M('\\cos\\dfrac\\pi2=0\\Rightarrow2\\cos^2\\dfrac\\pi2=0') + '។', 1), (M('\\cot\\dfrac\\pi4=1\\Rightarrow3\\cot^2\\dfrac\\pi4=3') + '។', 1), (M('A=1-1+0+3=3') + '។', 1)], 'Apply'))
    C.append(wr('hard', 'sec2_a', 'គណនា ' + M('\\dfrac{5-4\\tan^245^\\circ+\\cot^260^\\circ}{2\\cos^260^\\circ-2\\sin^390^\\circ+4\\tan45^\\circ}') + '។',
                [(M('\\tan45^\\circ=1,\\ \\cot60^\\circ=\\dfrac{\\sqrt3}3,\\ \\cos60^\\circ=\\dfrac12,\\ \\sin90^\\circ=1') + '។', 1),
                 ('ភាគយក ' + M('5-4+\\dfrac13=\\dfrac43') + '។', 1), ('ភាគបែង ' + M('2\\cdot\\dfrac14-2+4=\\dfrac52') + '។', 1), (M('\\dfrac{4/3}{5/2}=\\dfrac43\\times\\dfrac25') + '។', 1), (M('=\\dfrac8{15}') + '។', 1)], 'Analyze'))
    C.append(wr('pisa', 'sec2_b', 'ជណ្ដើរវែង ' + M('5\\text{ m}') + ' ផ្អៀងនឹងជញ្ជាំងបង្កើតមុំ ' + M('60^\\circ') + ' នឹងដី ។ រកកម្ពស់ដែលជណ្ដើរឡើងដល់ និងចម្ងាយពីជើងជណ្ដើរទៅជញ្ជាំង ។',
                [('ត្រីកោណកែង ៖ អ៊ីប៉ូតេនុស ' + M('=5') + ' មុំ ' + M('60^\\circ') + ' នឹងដី។', 1), ('កម្ពស់ ' + M('h=5\\sin60^\\circ') + '។', 1), (M('h=\\dfrac{5\\sqrt3}2\\approx4.33\\text{ m}') + '។', 1),
                 ('ចម្ងាយ ' + M('d=5\\cos60^\\circ') + '។', 1), (M('d=2.5\\text{ m}') + '។', 1)], 'Evaluate'))

    # ============================ PART 3: លក្ខណៈនៃអនុគមន៍ត្រីកោណមាត្រ ============================
    C.append(mcq('easy', 'sec3_a', 'ទំនាក់ទំនងគោលនៃអនុគមន៍ត្រីកោណមាត្រ គឺ ៖', M('\\sin^2\\theta+\\cos^2\\theta=1'), [M('\\sin\\theta+\\cos\\theta=1'), M('\\sin^2\\theta-\\cos^2\\theta=1'), M('\\sin\\theta\\cos\\theta=1')],
                 'តាមទ្រឹស្តីបទពីតាគ័រក្នុងរង្វង់ឯកតា។', 'Remember'))
    C.append(mcq('easy', 'sec3_c', M('\\cos(-\\theta)') + ' ស្មើនឹង ៖', M('\\cos\\theta'), [M('-\\cos\\theta'), M('\\sin\\theta'), M('-\\sin\\theta')], 'មុំផ្ទុយគ្នាមានកូស៊ីនុសដូចគ្នា។', 'Remember'))
    C.append(mcq('medium', 'sec3_c', M('\\sin150^\\circ') + ' ស្មើនឹង ៖', M('\\dfrac12'), [M('-\\dfrac12'), M('\\dfrac{\\sqrt3}2'), M('-\\dfrac{\\sqrt3}2')], M('\\sin(180^\\circ-30^\\circ)=\\sin30^\\circ') + '។', 'Apply'))
    C.append(mcq('medium', 'sec3_c', M('\\cos\\left(\\pi+\\dfrac\\pi6\\right)') + ' ស្មើនឹង ៖', M('-\\dfrac{\\sqrt3}2'), [M('\\dfrac{\\sqrt3}2'), M('-\\dfrac12'), M('\\dfrac12')], M('\\cos(\\pi+\\theta)=-\\cos\\theta') + '។', 'Apply'))
    C.append(mcq('medium', 'sec3_b', M('\\cos\\left(-\\dfrac{17\\pi}3\\right)') + ' ស្មើនឹង ៖', M('\\dfrac12'), [M('-\\dfrac12'), M('\\dfrac{\\sqrt3}2'), M('-\\dfrac{\\sqrt3}2')], M('-\\dfrac{17\\pi}3=\\dfrac\\pi3-6\\pi') + ' ដូច្នេះ ' + M('\\cos\\dfrac\\pi3=\\dfrac12') + '។', 'Apply'))
    C.append(mcq('medium', 'sec3_a', M('\\sin\\theta=\\dfrac35') + ' ហើយ ' + M('\\theta') + ' នៅកាដ្រង់ II ។ ' + M('\\cos\\theta') + ' ស្មើ ៖', M('-\\dfrac45'), [M('\\dfrac45'), M('-\\dfrac35'), M('\\dfrac34')],
                 M('\\cos\\theta=-\\sqrt{1-\\tfrac9{25}}=-\\dfrac45') + '។', 'Apply'))
    C.append(mcq('medium', 'sec3_c', M('\\tan\\dfrac{7\\pi}6') + ' ស្មើនឹង ៖', M('\\dfrac{\\sqrt3}3'), [M('-\\dfrac{\\sqrt3}3'), M('\\sqrt3'), M('-\\sqrt3')], M('\\tan(\\pi+\\theta)=\\tan\\theta') + ' ដូច្នេះ ' + M('\\tan\\dfrac\\pi6') + '។', 'Apply'))
    C.append(mcq('hard', 'sec3_a', M('\\tan\\alpha=\\dfrac4{15}') + '។ ' + M('\\dfrac{5\\sin\\alpha+7\\cos\\alpha}{6\\cos\\alpha-3\\sin\\alpha}') + ' ស្មើ ៖', M('\\dfrac{125}{78}'), [M('\\dfrac{78}{125}'), M('\\dfrac{25}{13}'), M('\\dfrac{5}{3}')],
                 'ចែកនឹង ' + M('\\cos\\alpha') + ' ៖ ' + M('\\dfrac{5\\tan\\alpha+7}{6-3\\tan\\alpha}=\\dfrac{25/3}{26/5}=\\dfrac{125}{78}') + '។', 'Analyze'))
    C.append(mcq('hard', 'sec3_a', M('\\sin\\alpha=\\dfrac35') + ' និង ' + M('0<\\alpha<\\dfrac\\pi2') + '។ ' + M('\\dfrac{\\cot\\alpha+\\tan\\alpha}{\\cot\\alpha-\\tan\\alpha}') + ' ស្មើ ៖', M('\\dfrac{25}7'), [M('\\dfrac7{25}'), M('\\dfrac{25}{12}'), M('\\dfrac{5}{4}')],
                 M('\\cos\\alpha=\\dfrac45,\\ \\cot\\alpha=\\dfrac43,\\ \\tan\\alpha=\\dfrac34') + ' ដូច្នេះ ' + M('\\dfrac{25/12}{7/12}=\\dfrac{25}7') + '។', 'Analyze'))
    C.append(mcq('hard', 'sec3_c', M('\\dfrac{(\\cot44^\\circ+\\tan226^\\circ)\\cos406^\\circ}{\\cos316^\\circ}-\\cot72^\\circ\\cot18^\\circ') + ' ស្មើ ៖', M('1'), [M('2\\tan44^\\circ-1'), M('0'), M('2')],
                 M('\\tan226^\\circ=\\cot44^\\circ,\\ \\cos406^\\circ=\\sin44^\\circ,\\ \\cos316^\\circ=\\cos44^\\circ') + ' ឱ្យ ' + M('2') + ' ហើយ ' + M('\\cot72^\\circ\\cot18^\\circ=1') + ' ដូច្នេះ ' + M('2-1=1') + '។', 'Analyze'))
    C.append(mcq('pisa', 'sec3_b', 'កម្ពស់កៅអីកង់ទាញ (m) គឺ ' + M('h(\\theta)=12+10\\sin\\theta') + '។ ពេល ' + M('\\theta=\\dfrac{7\\pi}6') + ' កម្ពស់ស្មើ ៖', M('7'), opts(17, 12, '12+5\\sqrt3'),
                 M('\\sin\\dfrac{7\\pi}6=-\\dfrac12') + ' ឱ្យ ' + M('h=12-5=7') + '។', 'Evaluate'))
    C.append(wr('medium', 'sec3_c', 'គណនា ' + M('A=\\cos(-\\theta)+\\sin\\left(\\dfrac\\pi2-\\theta\\right)+\\cos(\\pi-\\theta)+\\sin\\left(\\dfrac{3\\pi}2+\\theta\\right)') + '។',
                [(M('\\cos(-\\theta)=\\cos\\theta') + '។', 1), (M('\\sin\\left(\\dfrac\\pi2-\\theta\\right)=\\cos\\theta') + '។', 1), (M('\\cos(\\pi-\\theta)=-\\cos\\theta') + '។', 1),
                 (M('\\sin\\left(\\dfrac{3\\pi}2+\\theta\\right)=-\\cos\\theta') + '។', 1), (M('A=\\cos\\theta+\\cos\\theta-\\cos\\theta-\\cos\\theta=0') + '។', 1)], 'Apply'))
    C.append(wr('hard', 'sec3_a', M('\\sin\\theta+\\cos\\theta=-\\dfrac12') + ' និង ' + M('\\pi<\\theta<2\\pi') + '។ គណនា ក. ' + M('\\sin\\theta\\cos\\theta') + ' ខ. ' + M('\\tan\\theta+\\dfrac1{\\tan\\theta}') + ' គ. ' + M('\\sin^3\\theta+\\cos^3\\theta') + '។',
                [('ឡើងការេ ៖ ' + M('1+2\\sin\\theta\\cos\\theta=\\dfrac14') + '។', 1), (M('\\sin\\theta\\cos\\theta=-\\dfrac38') + '។', 1),
                 (M('\\tan\\theta+\\dfrac1{\\tan\\theta}=\\dfrac{1}{\\sin\\theta\\cos\\theta}=-\\dfrac83') + '។', 1), (M('\\sin^3+\\cos^3=(\\sin+\\cos)(1-\\sin\\cos)') + '។', 1),
                 (M('=-\\dfrac12\\cdot\\dfrac{11}8=-\\dfrac{11}{16}') + '។', 1)], 'Analyze'))
    C.append(wr('pisa', 'sec3_b', 'កម្ពស់កៅអីកង់ទាញ (m) គឺ ' + M('h(\\theta)=12+10\\sin\\theta') + '។ គណនា ' + M('h') + ' ពេល ' + M('\\theta=\\dfrac{7\\pi}6') + ' និង ' + M('\\theta=\\dfrac{13\\pi}2') + '។',
                [(M('\\sin\\dfrac{7\\pi}6=\\sin\\left(\\pi+\\dfrac\\pi6\\right)=-\\sin\\dfrac\\pi6=-\\dfrac12') + '។', 1), (M('h=12-5=7\\text{ m}') + '។', 1),
                 (M('\\dfrac{13\\pi}2=\\dfrac\\pi2+6\\pi') + '។', 1), (M('\\sin\\dfrac{13\\pi}2=\\sin\\dfrac\\pi2=1') + '។', 1), (M('h=12+10=22\\text{ m}') + ' (កម្ពស់អតិបរមា)។', 1)], 'Evaluate'))

    # ============================ PART 4: ការសិក្សាអនុគមន៍ត្រីកោណមាត្រ ============================
    C.append(mcq('easy', 'sec4_a', 'ដែនកំណត់នៃ ' + M('y=\\tan x') + ' គឺ ៖', M('x\\ne\\dfrac\\pi2+k\\pi'), [M('x\\ne k\\pi'), M('x\\in\\mathbb{R}'), M('x\\ne2k\\pi')], M('\\tan x=\\dfrac{\\sin x}{\\cos x}') + ' កំណត់កាលណា ' + M('\\cos x\\ne0') + '។', 'Remember'))
    C.append(with_img(mcq('easy', 'sec4_d', 'អនុគមន៍ ' + M('y=\\sin x') + ' មានខួបស្មើ ៖', M('2\\pi'), [M('\\pi'), M('\\dfrac\\pi2'), M('4\\pi')], M('\\sin(x+2\\pi)=\\sin x') + ' ហើយ ' + M('2\\pi') + ' តូចបំផុត។', 'Remember'), FIG_SIN))
    C.append(mcq('medium', 'sec4_b', 'ខួបនៃ ' + M('y=\\sin\\dfrac12x') + ' គឺ ៖', M('4\\pi'), [M('\\pi'), M('2\\pi'), M('\\dfrac\\pi2')], M('p=\\dfrac{2\\pi}{|a|}=\\dfrac{2\\pi}{1/2}=4\\pi') + '។', 'Apply'))
    C.append(mcq('medium', 'sec4_b', 'ខួបនៃ ' + M('y=\\cos(-3x)') + ' គឺ ៖', M('\\dfrac{2\\pi}3'), [M('2\\pi'), M('6\\pi'), M('\\dfrac\\pi3')], M('p=\\dfrac{2\\pi}{|-3|}=\\dfrac{2\\pi}3') + '។', 'Apply'))
    C.append(mcq('medium', 'sec4_b', 'ខួបនៃ ' + M('y=\\cot5x') + ' គឺ ៖', M('\\dfrac\\pi5'), [M('\\dfrac{2\\pi}5'), M('5\\pi'), M('\\pi')], M('p=\\dfrac\\pi{|a|}=\\dfrac\\pi5') + '។', 'Apply'))
    C.append(mcq('medium', 'sec4_c', 'អនុគមន៍ ' + M('y=x-\\sin x') + ' ជា ៖', 'អនុគមន៍សេស', ['អនុគមន៍គូ', 'អនុគមន៍ទាំងគូទាំងសេស', 'មិនគូមិនសេស'],
                 M('f(-x)=-x-\\sin(-x)=-(x-\\sin x)=-f(x)') + '។', 'Analyze'))
    C.append(mcq('hard', 'sec4_b', 'ខួបនៃអនុគមន៍ ' + M('y=\\sin2x+\\cos x') + ' គឺ ៖', M('2\\pi'), [M('\\pi'), M('\\dfrac\\pi2'), M('4\\pi')],
                 M('\\sin2x') + ' មានខួប ' + M('\\pi') + ' ហើយ ' + M('\\cos x') + ' មានខួប ' + M('2\\pi') + ' ដូច្នេះខួបរួមតូចបំផុត ' + M('2\\pi') + '។', 'Analyze'))
    C.append(mcq('pisa', 'sec4_d', 'ទីតាំងរបស់ប៉ោលមួយ ' + M('x(t)=10\\cos\\dfrac{2\\pi t}{3}') + ' (cm, ' + M('t') + ' គិតជាវិនាទី) ។ រយៈពេលនៃរំយោលមួយជុំ (វិនាទី) គឺ ៖', M('3'), opts(1.5, 6, 2),
                 M('p=\\dfrac{2\\pi}{2\\pi/3}=3') + ' វិនាទី។', 'Evaluate'))
    C.append(wr('medium', 'sec4_d', 'សិក្សា និងសង់តារាងតម្លៃនៃអនុគមន៍ ' + M('y=2\\sin x') + ' លើ ' + M('[0,2\\pi]') + '។',
                [('ដែនកំណត់ ' + M('\\mathbb{R}') + ' ខួប ' + M('2\\pi') + '។', 1), ('ជាអនុគមន៍សេស ព្រោះ ' + M('2\\sin(-x)=-2\\sin x') + '។', 1),
                 ('តារាង ' + M('x=0,\\dfrac\\pi2,\\pi,\\dfrac{3\\pi}2,2\\pi') + '។', 1), (M('y=0,2,0,-2,0') + '។', 1), ('អតិបរមា ' + M('2') + ' ត្រង់ ' + M('x=\\dfrac\\pi2') + ' អប្បបរមា ' + M('-2') + ' ត្រង់ ' + M('x=\\dfrac{3\\pi}2') + '។', 1)], 'Apply'))
    C.append(wr('hard', 'sec4_b', 'រកខួប និងភាពគូ/សេសនៃ ' + M('y=\\sin5x+\\sin3x+5\\sin x\\cos2x') + '។',
                [('ខួបនៃ ' + M('\\sin5x') + ' គឺ ' + M('\\dfrac{2\\pi}5') + ' ' + M('\\sin3x') + ' គឺ ' + M('\\dfrac{2\\pi}3') + ' ' + M('\\sin x\\cos2x') + ' គឺ ' + M('2\\pi') + '។', 1),
                 ('ខួបរួមតូចបំផុត ' + M('2\\pi') + ' (ពហុគុណរួមនៃ ' + M('\\tfrac{2\\pi}5,\\tfrac{2\\pi}3,2\\pi') + ')។', 1), ('ដែនកំណត់ ' + M('\\mathbb{R}') + ' ' + M('-x\\in D') + '។', 1),
                 (M('f(-x)=-\\sin5x-\\sin3x-5\\sin x\\cos2x') + '។', 1), (M('f(-x)=-f(x)') + ' ដូច្នេះជាអនុគមន៍សេស។', 1)], 'Analyze'))
    C.append(wr('hard', 'sec4_d', 'សិក្សា និងសង់តារាងនៃ ' + M('y=\\tan\\left(\\dfrac\\pi6-x\\right)') + '។',
                [('តាង ' + M('X=x-\\dfrac\\pi6') + ' នោះ ' + M('y=\\tan(-X)=-\\tan X') + '។', 1), ('ខួប ' + M('\\pi') + ' អាស៊ីមតូតឈរ ' + M('X=\\pm\\dfrac\\pi2') + '។', 1),
                 ('តារាង ' + M('X=-\\dfrac\\pi2,-\\dfrac\\pi4,0,\\dfrac\\pi4,\\dfrac\\pi2') + ' ឱ្យ ' + M('x=-\\dfrac\\pi3,-\\dfrac\\pi{12},\\dfrac\\pi6,\\dfrac{5\\pi}{12},\\dfrac{2\\pi}3') + '។', 1),
                 (M('y=+\\infty,1,0,-1,-\\infty') + '។', 1), ('ជាអនុគមន៍ចុះលើ ' + M('\\left(-\\dfrac\\pi3,\\dfrac{2\\pi}3\\right)') + ' ព្រោះ ' + M('-\\tan X') + ' ចុះ។', 1)], 'Analyze'))
    C.append(wr('pisa', 'sec4_d', 'កម្ពស់ទឹកសមុទ្រ (m) គឺ ' + M('H(t)=3+2\\cos\\dfrac{\\pi t}{6}') + ' ដែល ' + M('t') + ' ជាម៉ោង ។ រកខួប កម្ពស់អតិបរមា និងអប្បបរមា ។',
                [('ខួប ' + M('p=\\dfrac{2\\pi}{\\pi/6}=12') + ' ម៉ោង។', 1), ('ដោយ ' + M('-1\\le\\cos\\le1') + ' ។', 1), ('អតិបរមា ' + M('H=3+2=5\\text{ m}') + ' ពេល ' + M('t=0,12,\\dots') + '។', 1),
                 ('អប្បបរមា ' + M('H=3-2=1\\text{ m}') + ' ពេល ' + M('t=6,18,\\dots') + '។', 1), ('ជំនោរខ្ពស់រៀងរាល់ ១២ ម៉ោង។', 1)], 'Evaluate'))
    C.append(wr('pisa', 'sec4_d', 'តង់ស្យុងអគ្គិសនី (V) ក្នុងបណ្ដាញ ' + M('V(t)=311\\sin(100\\pi t)') + ' ដែល ' + M('t') + ' ជាវិនាទី ។ រកខួប ហើយទាញរកប្រេកង់ ។',
                [('ខួប ' + M('p=\\dfrac{2\\pi}{100\\pi}') + '។', 1), (M('p=0.02\\text{ s}') + '។', 1), ('ប្រេកង់ ' + M('f=\\dfrac1p') + '។', 1), (M('f=50\\text{ Hz}') + '។', 1), ('តង់ស្យុងអតិបរមា ' + M('311\\text{ V}') + '។', 1)], 'Evaluate'))

    bloom_for = {'easy': 'Understand', 'medium': 'Apply', 'hard': 'Analyze', 'pisa': 'Evaluate'}
    for q in C:
        q['bloom'] = q.get('bloom') or bloom_for[q['level']]
    return C
