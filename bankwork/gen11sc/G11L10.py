"""G11 Lesson 10 — រូបមន្តត្រីកោណមាត្រ.  Parts (sec prefix): sec1 រូបមន្តផលបូកនិងផលដក, sec2 រូបមន្តមុំឌុប និងកន្លះមុំ,
sec3 រូបមន្តបម្លែង (see gen11sc/parts.py).  Every closed form below is asserted numerically at import."""
from math import pi, sin, cos, tan, radians, sqrt, atan, degrees
from lib import M, mcq, wr

LESSON = 'រូបមន្តត្រីកោណមាត្រ'
CHAPTER = 'ជំពូកទី 3 : អនុគមន៍ត្រីកោណមាត្រ'


def with_img(q, svg):
    q['img'] = svg
    return q


def opts(*xs): return [M(str(x)) for x in xs]


def near(a, b, t=1e-9): return abs(a - b) < t


cot = lambda t: cos(t) / sin(t)
# ---- import-time checks ------------------------------------------------------------------------------------------
assert near(cos(radians(75)), (sqrt(6) - sqrt(2)) / 4) and near(sin(radians(15)), (sqrt(6) - sqrt(2)) / 4)
assert near(cos(radians(105)), (sqrt(2) - sqrt(6)) / 4) and near(tan(radians(75)), 2 + sqrt(3)) and near(tan(radians(15)), 2 - sqrt(3))
assert near(3 / 5 * 5 / 13 + 4 / 5 * 12 / 13, 63 / 65)
assert near((sin(radians(9)) * cos(radians(39)) - cos(radians(9)) * sin(radians(39))) / (cos(3 * pi / 7) * cos(5 * pi / 28) + sin(3 * pi / 7) * sin(5 * pi / 28)), -sqrt(2) / 2)
assert near((2 + 3) / (1 + 2 * (-3)), -1) and near(tan(pi / 4 + 0.4) * tan(pi / 4 - 0.4), 1)
assert near((1 / 3 + 1 / 2) / (1 - 1 / 6), 1)
assert near(2 * (3 / 5) * (-4 / 5), -24 / 25) and near(1 - 2 * (3 / 5) ** 2, 7 / 25)
assert near(sin(radians(22.5)), sqrt(2 - sqrt(2)) / 2) and near(tan(3 * pi / 8), sqrt(2) + 1) and near(sin(3 * (pi / 6)), 1)
assert near(sqrt((1 - (-3 / 5)) / 2), 2 * sqrt(5) / 5)
assert near(2 * (1 / 3) ** 2 - 1, -7 / 9) and near(2 * (7 / 9) ** 2 - 1, 17 / 81)
t_ = 1 / 2
assert near(2 * t_ / (1 + t_ ** 2), 4 / 5) and near((1 - t_ ** 2) / (1 + t_ ** 2), 3 / 5) and near(2 * t_ / (1 - t_ ** 2), 4 / 3)
assert near(400 * sin(radians(30)) / 10, 20) and near(40 * sin(radians(150)), 20) and near(40 * sin(pi / 2), 40)
assert near(cos(radians(75)) * cos(radians(45)), (sqrt(3) - 1) / 4) and near(sin(radians(105)) + sin(radians(15)), sqrt(6) / 2)
assert near(sin(5 * pi / 12) * sin(pi / 4), (sqrt(3) + 1) / 4) and near(cos(radians(75)) - cos(radians(15)), -sqrt(2) / 2)
assert near(sin(radians(75)) * cos(radians(15)), (2 + sqrt(3)) / 4)
assert near(2 * (1 / sin(pi / 3) + cot(pi / 3)), 2 * sqrt(3)) and near(cot(pi / 12) - tan(pi / 12), 2 * sqrt(3))
assert near(3 * sin(pi / 3), 3 * sqrt(3) / 2) and near(4 * cos(pi / 6) ** 3, 3 * sqrt(3) / 2)
assert near(sin(3 * pi / 3) * 3, 0)                       # equilateral: sin3A = sin180 = 0 (consistent with A = 60 deg)
assert near(3 * sin(0.7) + 4 * cos(0.7), 5 * sin(0.7 + atan(4 / 3)))
assert near(0.5 * 311 * 10 * cos(radians(60)), 777.5)
tb = (7 / 4 - 3 / 4) / (1 + 21 / 16)
assert near(tb, 16 / 37) and near(degrees(atan(7 / 4) - atan(3 / 4)), degrees(atan(16 / 37)))


def cands():
    C = []
    # ================================ PART 1: រូបមន្តផលបូកនិងផលដក ================================
    C.append(mcq('easy', 'sec1_a', M('\\cos(\\alpha-\\beta)') + ' ស្មើនឹង ៖', M('\\cos\\alpha\\cos\\beta+\\sin\\alpha\\sin\\beta'),
                 [M('\\cos\\alpha\\cos\\beta-\\sin\\alpha\\sin\\beta'), M('\\cos\\alpha-\\cos\\beta'), M('\\sin\\alpha\\cos\\beta+\\cos\\alpha\\sin\\beta')],
                 'ពីផលគុណស្កាលែនៃ ' + M('\\vec{OM}=(\\cos\\alpha,\\sin\\alpha)') + ' និង ' + M('\\vec{ON}=(\\cos\\beta,\\sin\\beta)') + '។', 'Remember'))
    C.append(mcq('easy', 'sec1_a', M('\\sin(\\alpha+\\beta)') + ' ស្មើនឹង ៖', M('\\sin\\alpha\\cos\\beta+\\cos\\alpha\\sin\\beta'),
                 [M('\\sin\\alpha\\cos\\beta-\\cos\\alpha\\sin\\beta'), M('\\sin\\alpha+\\sin\\beta'), M('\\cos\\alpha\\cos\\beta-\\sin\\alpha\\sin\\beta')], 'រូបមន្តផលបូកនៃស៊ីនុស។', 'Remember'))
    C.append(mcq('easy', 'sec1_a', M('\\tan(\\alpha+\\beta)') + ' ស្មើនឹង ៖', M('\\dfrac{\\tan\\alpha+\\tan\\beta}{1-\\tan\\alpha\\tan\\beta}'),
                 [M('\\dfrac{\\tan\\alpha-\\tan\\beta}{1+\\tan\\alpha\\tan\\beta}'), M('\\tan\\alpha+\\tan\\beta'), M('\\dfrac{\\tan\\alpha+\\tan\\beta}{1+\\tan\\alpha\\tan\\beta}')], 'ចែក ' + M('\\dfrac{\\sin(\\alpha+\\beta)}{\\cos(\\alpha+\\beta)}') + ' នឹង ' + M('\\cos\\alpha\\cos\\beta') + '។', 'Remember'))
    C.append(mcq('medium', 'sec1_b', M('\\cos75^\\circ') + ' ស្មើនឹង ៖', M('\\dfrac{\\sqrt6-\\sqrt2}4'), [M('\\dfrac{\\sqrt6+\\sqrt2}4'), M('\\dfrac{\\sqrt3-1}2'), M('\\dfrac{\\sqrt2-\\sqrt6}4')],
                 M('\\cos(45^\\circ+30^\\circ)=\\dfrac{\\sqrt2}2\\cdot\\dfrac{\\sqrt3}2-\\dfrac{\\sqrt2}2\\cdot\\dfrac12') + '។', 'Apply'))
    C.append(mcq('medium', 'sec1_b', M('\\sin15^\\circ') + ' ស្មើនឹង ៖', M('\\dfrac{\\sqrt6-\\sqrt2}4'), [M('\\dfrac{\\sqrt6+\\sqrt2}4'), M('\\dfrac{\\sqrt3}2-\\dfrac12'), M('\\dfrac{\\sqrt2-\\sqrt6}4')],
                 M('\\sin(45^\\circ-30^\\circ)=\\sin45^\\circ\\cos30^\\circ-\\cos45^\\circ\\sin30^\\circ') + '។', 'Apply'))
    C.append(mcq('medium', 'sec1_b', M('\\cos105^\\circ') + ' ស្មើនឹង ៖', M('\\dfrac{\\sqrt2-\\sqrt6}4'), [M('\\dfrac{\\sqrt6-\\sqrt2}4'), M('\\dfrac{\\sqrt6+\\sqrt2}4'), M('-\\dfrac{\\sqrt6+\\sqrt2}4')],
                 M('\\cos(60^\\circ+45^\\circ)=\\dfrac12\\cdot\\dfrac{\\sqrt2}2-\\dfrac{\\sqrt3}2\\cdot\\dfrac{\\sqrt2}2') + ' អវិជ្ជមាន ព្រោះ ' + M('105^\\circ') + ' នៅកាដ្រង់ II។', 'Apply'))
    C.append(mcq('medium', 'sec1_b', M('\\tan75^\\circ') + ' ស្មើនឹង ៖', M('2+\\sqrt3'), [M('2-\\sqrt3'), M('\\sqrt3+1'), M('\\dfrac{\\sqrt3}3')], M('\\tan(45^\\circ+30^\\circ)=\\dfrac{1+\\frac{\\sqrt3}3}{1-\\frac{\\sqrt3}3}=2+\\sqrt3') + '។', 'Apply'))
    C.append(mcq('medium', 'sec1_b', M('\\sin\\alpha=\\dfrac35') + ' និង ' + M('\\cos\\beta=\\dfrac5{13}') + ' (មុំស្រួចទាំងពីរ) ។ ' + M('\\sin(\\alpha+\\beta)') + ' ស្មើ ៖', M('\\dfrac{63}{65}'), [M('\\dfrac{33}{65}'), M('\\dfrac{15}{65}'), M('\\dfrac{56}{65}')],
                 M('\\cos\\alpha=\\dfrac45,\\ \\sin\\beta=\\dfrac{12}{13}') + ' ៖ ' + M('\\dfrac35\\cdot\\dfrac5{13}+\\dfrac45\\cdot\\dfrac{12}{13}=\\dfrac{63}{65}') + '។', 'Apply'))
    C.append(mcq('hard', 'sec1_b', M('\\dfrac{\\sin9^\\circ\\cos39^\\circ-\\cos9^\\circ\\sin39^\\circ}{\\cos\\frac{3\\pi}7\\cos\\frac{5\\pi}{28}+\\sin\\frac{3\\pi}7\\sin\\frac{5\\pi}{28}}') + ' ស្មើ ៖', M('-\\dfrac{\\sqrt2}2'), [M('\\dfrac{\\sqrt2}2'), M('-\\dfrac12'), M('-\\sqrt2')],
                 M('\\dfrac{\\sin(-30^\\circ)}{\\cos\\frac\\pi4}=\\dfrac{-1/2}{\\sqrt2/2}') + '។', 'Analyze'))
    C.append(mcq('hard', 'sec1_b', M('\\tan\\alpha=2') + ' និង ' + M('\\tan\\beta=-3') + '។ ' + M('\\tan(\\alpha-\\beta)') + ' ស្មើ ៖', M('-1'), opts(1, -5, '\\tfrac{-1}{7}'), M('\\dfrac{2-(-3)}{1+2(-3)}=\\dfrac{5}{-5}=-1') + '។', 'Analyze'))
    C.append(mcq('pisa', 'sec1_c', 'ផ្លូវពីរកាត់បន្តគ្នា មានជម្រាល ' + M('\\tan\\alpha=\\dfrac13') + ' និង ' + M('\\tan\\beta=\\dfrac12') + '។ ជម្រាលសរុបបង្កើតមុំ ' + M('\\alpha+\\beta') + ' ស្មើ ៖', M('45^\\circ'), [M('30^\\circ'), M('60^\\circ'), M('\\approx50^\\circ')],
                 M('\\tan(\\alpha+\\beta)=\\dfrac{\\frac13+\\frac12}{1-\\frac16}=1') + ' ដូច្នេះ ' + M('45^\\circ') + '។', 'Evaluate'))
    C.append(wr('easy', 'sec1_b', 'គណនា ' + M('\\sin75^\\circ') + ' ដោយប្រើ ' + M('75^\\circ=45^\\circ+30^\\circ') + '។',
                [('ប្រើ ' + M('\\sin(\\alpha+\\beta)=\\sin\\alpha\\cos\\beta+\\cos\\alpha\\sin\\beta') + '។', 1), (M('\\sin45^\\circ\\cos30^\\circ=\\dfrac{\\sqrt2}2\\cdot\\dfrac{\\sqrt3}2') + '។', 1),
                 (M('\\cos45^\\circ\\sin30^\\circ=\\dfrac{\\sqrt2}2\\cdot\\dfrac12') + '។', 1), (M('\\sin75^\\circ=\\dfrac{\\sqrt6}4+\\dfrac{\\sqrt2}4') + '។', 1), (M('=\\dfrac{\\sqrt6+\\sqrt2}4\\approx0.966') + '។', 1)], 'Apply'))
    C.append(wr('medium', 'sec1_b', 'គណនា ' + M('\\cos15^\\circ') + ' ដោយប្រើ ' + M('15^\\circ=60^\\circ-45^\\circ') + '។',
                [('ប្រើ ' + M('\\cos(\\alpha-\\beta)=\\cos\\alpha\\cos\\beta+\\sin\\alpha\\sin\\beta') + '។', 1), (M('\\cos60^\\circ\\cos45^\\circ=\\dfrac12\\cdot\\dfrac{\\sqrt2}2') + '។', 1),
                 (M('\\sin60^\\circ\\sin45^\\circ=\\dfrac{\\sqrt3}2\\cdot\\dfrac{\\sqrt2}2') + '។', 1), (M('\\cos15^\\circ=\\dfrac{\\sqrt2}4+\\dfrac{\\sqrt6}4') + '។', 1), (M('=\\dfrac{\\sqrt2+\\sqrt6}4') + '។', 1)], 'Apply'))
    C.append(wr('hard', 'sec1_b', 'បង្ហាញថា ' + M('\\sin\\alpha+\\cos\\alpha=\\sqrt2\\sin\\left(\\alpha+\\dfrac\\pi4\\right)') + ' រួចទាញរកតម្លៃអតិបរមានៃ ' + M('\\sin\\alpha+\\cos\\alpha') + '។',
                [('សរសេរ ' + M('\\sin\\alpha+\\cos\\alpha=\\sqrt2\\left(\\dfrac{\\sqrt2}2\\sin\\alpha+\\dfrac{\\sqrt2}2\\cos\\alpha\\right)') + '។', 1),
                 (M('\\dfrac{\\sqrt2}2=\\cos\\dfrac\\pi4=\\sin\\dfrac\\pi4') + '។', 1), (M('=\\sqrt2\\left(\\sin\\alpha\\cos\\dfrac\\pi4+\\cos\\alpha\\sin\\dfrac\\pi4\\right)') + '។', 1),
                 (M('=\\sqrt2\\sin\\left(\\alpha+\\dfrac\\pi4\\right)') + '។', 1), ('ដោយ ' + M('-1\\le\\sin\\le1') + ' អតិបរមា ' + M('=\\sqrt2') + ' ពេល ' + M('\\alpha=\\dfrac\\pi4') + '។', 1)], 'Analyze'))
    C.append(wr('pisa', 'sec1_c', 'ជម្រាលពីរ ' + M('\\tan\\alpha=\\dfrac13') + ' និង ' + M('\\tan\\beta=\\dfrac12') + ' ត្រូវបន្តគ្នា ។ រកមុំសរុប ' + M('\\alpha+\\beta') + '។',
                [('ប្រើ ' + M('\\tan(\\alpha+\\beta)=\\dfrac{\\tan\\alpha+\\tan\\beta}{1-\\tan\\alpha\\tan\\beta}') + '។', 1), (M('\\tan\\alpha+\\tan\\beta=\\dfrac13+\\dfrac12=\\dfrac56') + '។', 1),
                 (M('1-\\tan\\alpha\\tan\\beta=1-\\dfrac16=\\dfrac56') + '។', 1), (M('\\tan(\\alpha+\\beta)=1') + '។', 1), ('ដោយមុំស្រួច ' + M('\\alpha+\\beta=45^\\circ') + '។', 1)], 'Evaluate'))
    C.append(wr('pisa', 'sec1_c', 'ទស្សនិកជនឈរចម្ងាយ ' + M('20\\text{ m}') + ' ពីអគារ មើលឃើញកំពូលសសរកម្ពស់ ' + M('15\\text{ m}') + ' និងកំពូលអគារកម្ពស់ ' + M('35\\text{ m}') + ' (គិតពីកម្រិតភ្នែក) ។ រកមុំមើលរវាងកំពូលទាំងពីរ ។',
                [(M('\\tan\\alpha=\\dfrac{15}{20}=\\dfrac34') + ' និង ' + M('\\tan\\beta=\\dfrac{35}{20}=\\dfrac74') + '។', 1), ('មុំរវាង ' + M('\\theta=\\beta-\\alpha') + '។', 1),
                 (M('\\tan\\theta=\\dfrac{\\tan\\beta-\\tan\\alpha}{1+\\tan\\alpha\\tan\\beta}') + '។', 1), (M('=\\dfrac{7/4-3/4}{1+21/16}=\\dfrac{16}{37}') + '។', 1), (M('\\theta\\approx%.1f^\\circ' % degrees(atan(16 / 37))) + '។', 1)], 'Evaluate'))

    # ================================ PART 2: រូបមន្តមុំឌុប និងរូបមន្តកន្លះមុំ ================================
    C.append(mcq('easy', 'sec2_a', M('\\sin2\\alpha') + ' ស្មើនឹង ៖', M('2\\sin\\alpha\\cos\\alpha'), [M('2\\sin\\alpha'), M('\\sin^2\\alpha-\\cos^2\\alpha'), M('\\sin\\alpha+\\cos\\alpha')], 'ដាក់ ' + M('\\beta=\\alpha') + ' ក្នុង ' + M('\\sin(\\alpha+\\beta)') + '។', 'Remember'))
    C.append(mcq('easy', 'sec2_a', 'កន្សោមណាមួយខាងក្រោម មិនស្មើ ' + M('\\cos2\\alpha') + ' ?', M('2\\cos\\alpha-1'), [M('\\cos^2\\alpha-\\sin^2\\alpha'), M('1-2\\sin^2\\alpha'), M('2\\cos^2\\alpha-1')],
                 M('\\cos2\\alpha=\\cos^2\\alpha-\\sin^2\\alpha=1-2\\sin^2\\alpha=2\\cos^2\\alpha-1') + '។', 'Understand'))
    C.append(mcq('easy', 'sec2_a', M('\\tan2\\alpha') + ' ស្មើនឹង ៖', M('\\dfrac{2\\tan\\alpha}{1-\\tan^2\\alpha}'), [M('\\dfrac{2\\tan\\alpha}{1+\\tan^2\\alpha}'), M('2\\tan\\alpha'), M('\\dfrac{\\tan\\alpha}{1-\\tan^2\\alpha}')], 'ដាក់ ' + M('\\beta=\\alpha') + ' ក្នុង ' + M('\\tan(\\alpha+\\beta)') + '។', 'Remember'))
    C.append(mcq('easy', 'sec2_b', M('\\tan\\dfrac\\alpha2') + ' ស្មើនឹង ៖', M('\\dfrac{\\sin\\alpha}{1+\\cos\\alpha}'), [M('\\dfrac{\\sin\\alpha}{1-\\cos\\alpha}'), M('\\dfrac{1+\\cos\\alpha}{\\sin\\alpha}'), M('\\dfrac{\\sin\\alpha}{2}')], M('\\tan x=\\dfrac{\\sin2x}{1+\\cos2x}') + ' ជាមួយ ' + M('x=\\tfrac\\alpha2') + '។', 'Remember'))
    C.append(mcq('medium', 'sec2_a', M('\\sin\\alpha=\\dfrac35') + ' ហើយ ' + M('\\alpha') + ' ជាមុំទី II ។ ' + M('\\sin2\\alpha') + ' ស្មើ ៖', M('-\\dfrac{24}{25}'), [M('\\dfrac{24}{25}'), M('-\\dfrac{7}{25}'), M('\\dfrac{6}{5}')],
                 M('\\cos\\alpha=-\\dfrac45') + ' ដូច្នេះ ' + M('2\\cdot\\dfrac35\\cdot\\left(-\\dfrac45\\right)=-\\dfrac{24}{25}') + '។', 'Apply'))
    C.append(mcq('medium', 'sec2_a', M('\\sin\\alpha=\\dfrac35') + '។ ' + M('\\cos2\\alpha') + ' ស្មើ ៖', M('\\dfrac7{25}'), [M('-\\dfrac7{25}'), M('\\dfrac{16}{25}'), M('\\dfrac{9}{25}')], M('1-2\\sin^2\\alpha=1-\\dfrac{18}{25}=\\dfrac7{25}') + '។', 'Apply'))
    C.append(mcq('medium', 'sec2_b', M('\\sin22^\\circ30\'') + ' ស្មើនឹង ៖', M('\\dfrac{\\sqrt{2-\\sqrt2}}2'), [M('\\dfrac{\\sqrt{2+\\sqrt2}}2'), M('\\dfrac{\\sqrt2}4'), M('\\dfrac{1}{4}')], M('\\sqrt{\\dfrac{1-\\cos45^\\circ}{2}}=\\sqrt{\\dfrac{1-\\frac{\\sqrt2}2}2}') + '។', 'Apply'))
    C.append(mcq('medium', 'sec2_b', M('\\tan\\dfrac{3\\pi}8') + ' ស្មើនឹង ៖', M('\\sqrt2+1'), [M('\\sqrt2-1'), M('\\dfrac{\\sqrt2}2'), M('2')], M('\\dfrac{\\sin\\frac{3\\pi}4}{1+\\cos\\frac{3\\pi}4}=\\dfrac{\\sqrt2/2}{1-\\sqrt2/2}=\\sqrt2+1') + '។', 'Apply'))
    C.append(mcq('medium', 'sec2_b', M('\\cos\\alpha=-\\dfrac35') + ' ហើយ ' + M('\\dfrac\\pi2<\\alpha<\\pi') + '។ ' + M('\\cos\\dfrac\\alpha2') + ' ស្មើ ៖', M('\\dfrac{\\sqrt5}5'), [M('-\\dfrac{\\sqrt5}5'), M('\\dfrac{2\\sqrt5}5'), M('\\dfrac{1}{5}')],
                 M('\\dfrac\\pi4<\\dfrac\\alpha2<\\dfrac\\pi2') + ' វិជ្ជមាន ៖ ' + M('\\sqrt{\\dfrac{1-\\frac35}{2}}=\\dfrac{\\sqrt5}5') + '។', 'Apply'))
    C.append(mcq('hard', 'sec2_a', M('\\cos\\alpha=\\dfrac13') + '។ ' + M('\\cos4\\alpha') + ' ស្មើ ៖', M('\\dfrac{17}{81}'), [M('-\\dfrac{7}{9}'), M('\\dfrac{49}{81}'), M('-\\dfrac{17}{81}')],
                 M('\\cos2\\alpha=2\\cdot\\dfrac19-1=-\\dfrac79') + ' ហើយ ' + M('\\cos4\\alpha=2\\cdot\\dfrac{49}{81}-1=\\dfrac{17}{81}') + '។', 'Analyze'))
    C.append(mcq('hard', 'sec2_b', M('\\tan\\dfrac\\alpha2=\\dfrac12') + '។ ' + M('\\tan\\alpha') + ' ស្មើ ៖', M('\\dfrac43'), [M('1'), M('\\dfrac34'), M('\\dfrac23')], M('\\dfrac{2t}{1-t^2}=\\dfrac{1}{3/4}=\\dfrac43') + '។', 'Analyze'))
    C.append(mcq('hard', 'sec2_b', M('\\cos\\alpha=-\\dfrac7{25}') + ' និង ' + M('180^\\circ<\\alpha<270^\\circ') + '។ ' + M('\\tan\\dfrac\\alpha2') + ' ស្មើ ៖', M('-\\dfrac43'), [M('\\dfrac43'), M('\\dfrac34'), M('-\\dfrac34')],
                 M('90^\\circ<\\dfrac\\alpha2<135^\\circ') + ' ដូច្នេះអវិជ្ជមាន ៖ ' + M('\\dfrac{\\sin\\alpha}{1+\\cos\\alpha}=\\dfrac{-24/25}{18/25}=-\\dfrac43') + '។', 'Analyze'))
    C.append(mcq('pisa', 'sec2_a', 'ចម្ងាយបាញ់ឆ្ងាយ ' + M('R=\\dfrac{v^2\\sin2\\theta}{g}') + '។ ចំពោះ ' + M('v=20\\text{ m/s}') + ', ' + M('\\theta=15^\\circ') + ', ' + M('g=10\\text{ m/s}^2') + ' ចម្ងាយ (m) គឺ ៖', M('20'), opts(10, 40, 34.6),
                 M('R=\\dfrac{400\\sin30^\\circ}{10}=20') + '។', 'Evaluate'))
    C.append(mcq('pisa', 'sec2_a', 'ចម្ងាយបាញ់ ' + M('R(\\theta)=40\\sin2\\theta') + ' (m)។ មុំ ' + M('\\theta') + ' ដែលឱ្យ ' + M('R') + ' អតិបរមា គឺ ៖', M('45^\\circ'), [M('30^\\circ'), M('60^\\circ'), M('90^\\circ')],
                 M('\\sin2\\theta=1\\Rightarrow2\\theta=90^\\circ') + ' ហើយ ' + M('R_{\\max}=40') + ' m។', 'Evaluate'))
    C.append(wr('medium', 'sec2_a', M('\\cos\\alpha=-\\dfrac45') + ' និង ' + M('\\dfrac\\pi2<\\alpha<\\pi') + '។ រក ' + M('\\sin2\\alpha,\\ \\cos2\\alpha,\\ \\tan2\\alpha') + '។',
                [(M('\\sin\\alpha>0\\Rightarrow\\sin\\alpha=\\sqrt{1-\\tfrac{16}{25}}=\\dfrac35') + '។', 1), (M('\\sin2\\alpha=2\\cdot\\dfrac35\\cdot\\left(-\\dfrac45\\right)=-\\dfrac{24}{25}') + '។', 1),
                 (M('\\cos2\\alpha=2\\cos^2\\alpha-1=\\dfrac{32}{25}-1=\\dfrac7{25}') + '។', 1), (M('\\tan\\alpha=-\\dfrac34') + '។', 1), (M('\\tan2\\alpha=\\dfrac{\\sin2\\alpha}{\\cos2\\alpha}=-\\dfrac{24}7') + '។', 1)], 'Apply'))
    C.append(wr('medium', 'sec2_b', M('\\cos\\alpha=-\\dfrac35') + ' និង ' + M('\\dfrac\\pi2<\\alpha<\\pi') + '។ គណនា ' + M('\\sin\\dfrac\\alpha2') + ' និង ' + M('\\cos\\dfrac\\alpha2') + '។',
                [(M('\\dfrac\\pi2<\\alpha<\\pi\\Rightarrow\\dfrac\\pi4<\\dfrac\\alpha2<\\dfrac\\pi2') + ' ដូច្នេះ ' + M('\\sin\\dfrac\\alpha2,\\ \\cos\\dfrac\\alpha2>0') + '។', 1),
                 (M('\\sin^2\\dfrac\\alpha2=\\dfrac{1-\\cos\\alpha}2=\\dfrac{1+\\frac35}{2}=\\dfrac45') + '។', 1), (M('\\sin\\dfrac\\alpha2=\\dfrac{2\\sqrt5}5') + '។', 1),
                 (M('\\cos^2\\dfrac\\alpha2=\\dfrac{1+\\cos\\alpha}2=\\dfrac15') + '។', 1), (M('\\cos\\dfrac\\alpha2=\\dfrac{\\sqrt5}5') + '។', 1)], 'Apply'))
    C.append(wr('hard', 'sec2_a', 'បង្ហាញថា ' + M('\\sin3\\alpha=3\\sin\\alpha-4\\sin^3\\alpha') + '។',
                [(M('\\sin3\\alpha=\\sin(2\\alpha+\\alpha)=\\sin2\\alpha\\cos\\alpha+\\cos2\\alpha\\sin\\alpha') + '។', 1),
                 ('ជំនួស ' + M('\\sin2\\alpha=2\\sin\\alpha\\cos\\alpha') + ' និង ' + M('\\cos2\\alpha=1-2\\sin^2\\alpha') + '។', 1),
                 (M('=2\\sin\\alpha\\cos^2\\alpha+\\sin\\alpha-2\\sin^3\\alpha') + '។', 1), (M('\\cos^2\\alpha=1-\\sin^2\\alpha') + ' ឱ្យ ' + M('2\\sin\\alpha-2\\sin^3\\alpha+\\sin\\alpha-2\\sin^3\\alpha') + '។', 1),
                 (M('=3\\sin\\alpha-4\\sin^3\\alpha') + '។', 1)], 'Analyze'))
    C.append(wr('pisa', 'sec2_a', 'ចម្ងាយបាញ់ ' + M('R(\\theta)=40\\sin2\\theta') + ' (m)។ គណនា ' + M('R') + ' ពេល ' + M('\\theta=15^\\circ,\\ 45^\\circ,\\ 75^\\circ') + ' ហើយពន្យល់ថាមុំណាល្អបំផុត ។',
                [(M('\\theta=15^\\circ:\\ R=40\\sin30^\\circ=20') + ' m។', 1), (M('\\theta=45^\\circ:\\ R=40\\sin90^\\circ=40') + ' m។', 1), (M('\\theta=75^\\circ:\\ R=40\\sin150^\\circ=20') + ' m។', 1),
                 ('មុំបំពេញគ្នា ' + M('15^\\circ+75^\\circ=90^\\circ') + ' ឱ្យចម្ងាយស្មើគ្នា។', 1), ('មុំល្អបំផុត ' + M('45^\\circ') + ' ព្រោះ ' + M('\\sin2\\theta=1') + '។', 1)], 'Evaluate'))

    # ================================ PART 3: រូបមន្តបម្លែង ================================
    C.append(mcq('easy', 'sec3_a', M('\\cos\\alpha\\cos\\beta') + ' ស្មើនឹង ៖', M('\\dfrac12[\\cos(\\alpha+\\beta)+\\cos(\\alpha-\\beta)]'), [M('\\dfrac12[\\cos(\\alpha+\\beta)-\\cos(\\alpha-\\beta)]'), M('\\cos(\\alpha+\\beta)+\\cos(\\alpha-\\beta)'), M('\\dfrac12[\\sin(\\alpha+\\beta)+\\sin(\\alpha-\\beta)]')],
                 'បូករូបមន្ត ' + M('\\cos(\\alpha+\\beta)') + ' និង ' + M('\\cos(\\alpha-\\beta)') + '។', 'Remember'))
    C.append(mcq('easy', 'sec3_a', M('\\sin\\alpha\\sin\\beta') + ' ស្មើនឹង ៖', M('\\dfrac12[\\cos(\\alpha-\\beta)-\\cos(\\alpha+\\beta)]'), [M('\\dfrac12[\\cos(\\alpha+\\beta)-\\cos(\\alpha-\\beta)]'), M('\\dfrac12[\\cos(\\alpha-\\beta)+\\cos(\\alpha+\\beta)]'), M('\\dfrac12[\\sin(\\alpha+\\beta)-\\sin(\\alpha-\\beta)]')],
                 'ដក ' + M('\\cos(\\alpha-\\beta)-\\cos(\\alpha+\\beta)=2\\sin\\alpha\\sin\\beta') + '។', 'Remember'))
    C.append(mcq('easy', 'sec3_b', M('\\sin p+\\sin q') + ' ស្មើនឹង ៖', M('2\\sin\\dfrac{p+q}2\\cos\\dfrac{p-q}2'), [M('2\\sin\\dfrac{p-q}2\\cos\\dfrac{p+q}2'), M('2\\cos\\dfrac{p+q}2\\cos\\dfrac{p-q}2'), M('\\sin(p+q)')], 'តាង ' + M('p=\\alpha+\\beta,\\ q=\\alpha-\\beta') + '។', 'Remember'))
    C.append(mcq('medium', 'sec3_a', M('\\cos75^\\circ\\cos45^\\circ') + ' ស្មើនឹង ៖', M('\\dfrac{\\sqrt3-1}4'), [M('\\dfrac{\\sqrt3+1}4'), M('\\dfrac{1-\\sqrt3}4'), M('\\dfrac{\\sqrt2}4')], M('\\dfrac12(\\cos120^\\circ+\\cos30^\\circ)=\\dfrac12\\left(-\\dfrac12+\\dfrac{\\sqrt3}2\\right)') + '។', 'Apply'))
    C.append(mcq('medium', 'sec3_a', M('\\sin\\dfrac{5\\pi}{12}\\sin\\dfrac\\pi4') + ' ស្មើនឹង ៖', M('\\dfrac{\\sqrt3+1}4'), [M('\\dfrac{\\sqrt3-1}4'), M('\\dfrac{1}{4}'), M('\\dfrac{\\sqrt3}4')], M('\\dfrac12\\left[\\cos\\dfrac\\pi6-\\cos\\dfrac{2\\pi}3\\right]=\\dfrac12\\left[\\dfrac{\\sqrt3}2+\\dfrac12\\right]') + '។', 'Apply'))
    C.append(mcq('medium', 'sec3_b', M('\\sin105^\\circ+\\sin15^\\circ') + ' ស្មើនឹង ៖', M('\\dfrac{\\sqrt6}2'), [M('\\dfrac{\\sqrt2}2'), M('\\dfrac{\\sqrt3}2'), M('\\dfrac{\\sqrt6}4')], M('2\\sin60^\\circ\\cos45^\\circ=2\\cdot\\dfrac{\\sqrt3}2\\cdot\\dfrac{\\sqrt2}2') + '។', 'Apply'))
    C.append(mcq('medium', 'sec3_b', M('\\cos75^\\circ-\\cos15^\\circ') + ' ស្មើនឹង ៖', M('-\\dfrac{\\sqrt2}2'), [M('\\dfrac{\\sqrt2}2'), M('-\\dfrac12'), M('-\\dfrac{\\sqrt6}2')], M('-2\\sin45^\\circ\\sin30^\\circ=-2\\cdot\\dfrac{\\sqrt2}2\\cdot\\dfrac12') + '។', 'Apply'))
    C.append(mcq('hard', 'sec3_b', M('\\alpha=\\dfrac\\pi6') + '។ តម្លៃនៃ ' + M('2\\left(\\dfrac1{\\sin2\\alpha}+\\cot2\\alpha\\right)') + ' (ស្មើ ' + M('\\cot\\dfrac\\alpha2-\\tan\\dfrac\\alpha2') + ') គឺ ៖', M('2\\sqrt3'), [M('\\sqrt3'), M('4'), M('2')],
                 M('\\cot\\dfrac\\pi{12}-\\tan\\dfrac\\pi{12}=(2+\\sqrt3)-(2-\\sqrt3)=2\\sqrt3') + '។', 'Analyze'))
    C.append(mcq('hard', 'sec3_b', M('A,B,C') + ' ជាមុំក្នុងត្រីកោណសម័ង្ស ។ ' + M('\\sin A+\\sin B+\\sin C=4\\cos\\dfrac A2\\cos\\dfrac B2\\cos\\dfrac C2') + ' មានតម្លៃ ៖', M('\\dfrac{3\\sqrt3}2'), [M('\\dfrac{3}{2}'), M('3'), M('\\dfrac{\\sqrt3}2')],
                 M('3\\sin60^\\circ=\\dfrac{3\\sqrt3}2') + ' ហើយ ' + M('4\\cos^330^\\circ=4\\cdot\\dfrac{3\\sqrt3}8') + ' ដូចគ្នា។', 'Analyze'))
    C.append(mcq('pisa', 'sec3_a', 'ស្ទ្រីមសំឡេងពីរមានប្រេកង់ ' + M('440\\text{ Hz}') + ' និង ' + M('444\\text{ Hz}') + '។ ' + M('\\sin2\\pi(440t)+\\sin2\\pi(444t)=2\\sin2\\pi(442t)\\cos2\\pi(2t)') + '។ ប្រេកង់ញ័រ (beat) គឺ ៖', M('4\\text{ Hz}'), [M('2\\text{ Hz}'), M('442\\text{ Hz}'), M('884\\text{ Hz}')],
                 'ស្រោបទំហំ ' + M('|\\cos2\\pi(2t)|') + ' មានប្រេកង់ ' + M('2\\times2=4') + ' Hz ពោលគឺ ' + M('|444-440|') + '។', 'Evaluate'))
    C.append(mcq('pisa', 'sec3_a', 'តង់ស្យុង ' + M('v=311\\sin\\omega t') + ' ចរន្ត ' + M('i=10\\sin(\\omega t-60^\\circ)') + '។ ' + M('vi=\\dfrac{311\\cdot10}2\\left[\\cos60^\\circ-\\cos(2\\omega t-60^\\circ)\\right]') + '។ ថាមពលមធ្យម (W) គឺ ៖', M('777.5'), opts(1555, 3110, 388.75),
                 'ផ្នែក ' + M('\\cos(2\\omega t-60^\\circ)') + ' មធ្យមស្មើ ០ ដូច្នេះ ' + M('\\dfrac{311\\cdot10}2\\cos60^\\circ=777.5') + '។', 'Evaluate'))
    C.append(wr('medium', 'sec3_b', 'គណនា ' + M('\\sin105^\\circ+\\sin15^\\circ') + ' ដោយបម្លែងជាផលគុណ ។',
                [('ប្រើ ' + M('\\sin p+\\sin q=2\\sin\\dfrac{p+q}2\\cos\\dfrac{p-q}2') + '។', 1), (M('\\dfrac{105^\\circ+15^\\circ}2=60^\\circ') + '។', 1), (M('\\dfrac{105^\\circ-15^\\circ}2=45^\\circ') + '។', 1),
                 (M('=2\\sin60^\\circ\\cos45^\\circ=2\\cdot\\dfrac{\\sqrt3}2\\cdot\\dfrac{\\sqrt2}2') + '។', 1), (M('=\\dfrac{\\sqrt6}2') + '។', 1)], 'Apply'))
    C.append(wr('hard', 'sec3_b', 'ក្នុងត្រីកោណ ' + M('ABC') + ' បង្ហាញថា ' + M('\\sin A+\\sin B+\\sin C=4\\cos\\dfrac A2\\cos\\dfrac B2\\cos\\dfrac C2') + '។',
                [(M('\\sin A+\\sin B=2\\sin\\dfrac{A+B}2\\cos\\dfrac{A-B}2') + '។', 1), ('ដោយ ' + M('A+B+C=\\pi') + ' ៖ ' + M('\\sin\\dfrac{A+B}2=\\cos\\dfrac C2') + '។', 1),
                 (M('\\sin C=2\\sin\\dfrac C2\\cos\\dfrac C2=2\\cos\\dfrac{A+B}2\\cos\\dfrac C2') + '។', 1), ('បូក ៖ ' + M('2\\cos\\dfrac C2\\left[\\cos\\dfrac{A-B}2+\\cos\\dfrac{A+B}2\\right]') + '។', 1),
                 (M('\\cos\\dfrac{A-B}2+\\cos\\dfrac{A+B}2=2\\cos\\dfrac A2\\cos\\dfrac B2') + ' ដូច្នេះបានលទ្ធផល។', 1)], 'Analyze'))
    C.append(wr('hard', 'sec3_b', 'ក្នុងត្រីកោណ ' + M('ABC') + ' ដែល ' + M('\\sin3A+\\sin3B+\\sin3C=0') + ' ។ បង្ហាញថាត្រីកោណមានមុំមួយស្មើ ' + M('60^\\circ') + '។',
                [('ដោយ ' + M('3A+3B+3C=3\\pi') + ' ៖ ' + M('\\sin3C=\\sin(3\\pi-3A-3B)=\\sin(3A+3B)') + '។', 1),
                 (M('\\sin3A+\\sin3B+\\sin(3A+3B)=4\\sin\\dfrac{3A+3B}2\\cos\\dfrac{3A}2\\cos\\dfrac{3B}2') + '។', 1),
                 (M('\\sin\\dfrac{3A+3B}2=\\sin\\left(\\dfrac{3\\pi}2-\\dfrac{3C}2\\right)=-\\cos\\dfrac{3C}2') + '។', 1),
                 ('ផលបូក ' + M('=-4\\cos\\dfrac{3A}2\\cos\\dfrac{3B}2\\cos\\dfrac{3C}2=0') + '។', 1), (M('\\cos\\dfrac{3X}2=0\\Rightarrow X=60^\\circ') + ' (ក្នុង ' + M('(0^\\circ,180^\\circ)') + ')។', 1)], 'Analyze'))
    C.append(wr('pisa', 'sec3_a', 'សំឡេងពីរ ' + M('\\sin2\\pi(440t)') + ' និង ' + M('\\sin2\\pi(444t)') + ' បូកគ្នា ។ បម្លែងជាផលគុណ ហើយរកប្រេកង់ញ័រ (beat) ។',
                [('ប្រើ ' + M('\\sin p+\\sin q=2\\sin\\dfrac{p+q}2\\cos\\dfrac{p-q}2') + '។', 1), (M('\\dfrac{p+q}2=2\\pi(442t)') + '។', 1), (M('\\dfrac{p-q}2=-2\\pi(2t)') + ' ហើយ ' + M('\\cos') + ' គូ។', 1),
                 (M('=2\\sin2\\pi(442t)\\cos2\\pi(2t)') + '។', 1), ('ស្រោបទំហំ ' + M('|\\cos2\\pi(2t)|') + ' ប្រេកង់ ' + M('4\\text{ Hz}=|444-440|') + '។', 1)], 'Evaluate'))
    C.append(wr('pisa', 'sec3_a', 'តង់ស្យុង ' + M('v=311\\sin\\omega t') + ' ចរន្ត ' + M('i=10\\sin(\\omega t-60^\\circ)') + '។ ប្រើរូបមន្តបម្លែង រកថាមពលមធ្យម ' + M('\\overline{vi}') + '។',
                [(M('vi=3110\\sin\\omega t\\sin(\\omega t-60^\\circ)') + '។', 1), (M('\\sin a\\sin b=\\dfrac12[\\cos(a-b)-\\cos(a+b)]') + '។', 1),
                 (M('vi=1555[\\cos60^\\circ-\\cos(2\\omega t-60^\\circ)]') + '។', 1), ('មធ្យមនៃ ' + M('\\cos(2\\omega t-60^\\circ)') + ' ស្មើ ០។', 1), (M('\\overline{vi}=1555\\cos60^\\circ=777.5\\text{ W}') + '។', 1)], 'Evaluate'))

    bloom_for = {'easy': 'Understand', 'medium': 'Apply', 'hard': 'Analyze', 'pisa': 'Evaluate'}
    for q in C:
        q['bloom'] = q.get('bloom') or bloom_for[q['level']]
    return C
