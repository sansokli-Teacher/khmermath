"""G11 Lesson 8 — អនុគមន៍លោការីត (logarithmic functions, change of base, equations, inequalities, applications).
All numeric answers are computed with math/Fraction and the solved equations are re-checked at import."""
from fractions import Fraction as F
from math import log, log10, exp, sqrt
from lib import M, mcq, wr

LESSON = 'អនុគមន៍លោការីត'
CHAPTER = 'ជំពូកទី 2 : អនុគមន៍អិចស្ប៉ូណង់ស្យែលនិងអនុគមន៍លោការីត'


def with_img(q, svg):
    q['img'] = svg
    return q


def lg(b, x): return log(x) / log(b)


def opts(*xs): return [M(str(x)) for x in xs]


def fr(x):
    x = F(x)
    if x.denominator == 1: return M(str(x.numerator))
    return M(('-' if x < 0 else '') + r'\dfrac{%d}{%d}' % (abs(x.numerator), x.denominator))


def d(x, dp=2): return '%.*f' % (dp, x)


# ---- import-time checks ------------------------------------------------------------------------
assert abs(lg(9, 27) - 1.5) < 1e-12 and abs(lg(27, 1 / 3) + 1 / 3) < 1e-12 and abs(lg(0.5, 8) + 3) < 1e-12
assert 4 ** 2.5 == 32 and 9 ** 1.5 == 27 and abs(0.1 ** -3 - 1000) < 1e-9
assert all(abs(6 * (lg(x, 8) + lg(8, x)) - 13) < 1e-9 for x in (4, 16 * sqrt(2)))
assert all(abs(lg(9, x) + lg(x, 9) - 2.5) < 1e-9 for x in (3, 81))
assert abs(log10(1) + log10(10) - 1) < 1e-12
assert all(abs(log10(x + 10) + 0.5 * log10(x * x) - (2 - log10(4))) < 1e-9 for x in (-5, 5 * sqrt(2) - 5))
assert abs(8 ** lg(2, 3) - 2 ** (lg(2, 3) + 2) - 15) < 1e-9
T_BANK = lg(1.05, 3705000 / 2925000) / 2
T_SUGAR = log(0.5) / log(0.89)
T_DBL = log(2) / log(1.06)
T_POP = log(1.26 / 1.01) / 0.006
V18 = 10000 * exp(-(log(2) / 12) * 18)
assert 2.4 < T_BANK < 2.45 and 5.9 < T_SUGAR < 6 and 11.8 < T_DBL < 12 and 36.8 < T_POP < 37 and abs(V18 - 3535.53) < 0.01
assert 2000 + int(T_POP) + 1 == 2037

# ---- figures ------------------------------------------------------------------------------------
def _poly(f, x0, x1, n=120, sx=36, sy=34, ox=40, oy=100):
    pts = []
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        try:
            y = f(x)
        except Exception:
            continue
        px, py = ox + sx * x, oy - sy * y
        if -5 < py < 195:
            pts.append('%.1f,%.1f' % (px, py))
    return ' '.join(pts)


FIG_INV = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 260 200' width='260' height='200'>"
           "<line x1='5' y1='160' x2='255' y2='160' stroke='#94a3b8'/><line x1='40' y1='5' x2='40' y2='195' stroke='#94a3b8'/>"
           "<line x1='40' y1='160' x2='225' y2='-25' stroke='#94a3b8' stroke-dasharray='4,3'/>"
           "<polyline fill='none' stroke='#1e40af' stroke-width='2' points='" + _poly(lambda x: 4 ** x, -1.2, 1.4, 120, 45, 30, 40, 160) + "'/>"
           "<polyline fill='none' stroke='#dc2626' stroke-width='2' points='" + _poly(lambda x: log(x) / log(4), 0.06, 4.4, 160, 45, 45, 40, 160) + "'/>"
           "<text x='55' y='35' font-family='Times New Roman, serif' font-size='13' fill='#1e40af'>4^x</text>"
           "<text x='200' y='118' font-family='Times New Roman, serif' font-size='13' fill='#dc2626'>log_4 x</text>"
           "<text x='170' y='45' font-family='Times New Roman, serif' font-size='12' fill='#64748b'>y = x</text></svg>")
FIG_LOGCMP = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 280 200' width='280' height='200'>"
              "<line x1='5' y1='110' x2='275' y2='110' stroke='#94a3b8'/><line x1='25' y1='5' x2='25' y2='195' stroke='#94a3b8'/>"
              "<polyline fill='none' stroke='#dc2626' stroke-width='2' points='" + _poly(lambda x: log(x) / log(2), 0.1, 11, 140, 22, 22, 25, 110) + "'/>"
              "<polyline fill='none' stroke='#1e40af' stroke-width='2' points='" + _poly(lambda x: log(x), 0.1, 11, 140, 22, 22, 25, 110) + "'/>"
              "<polyline fill='none' stroke='#0d9488' stroke-width='2' points='" + _poly(lambda x: log10(x), 0.1, 11, 140, 22, 22, 25, 110) + "'/>"
              "<text x='235' y='30' font-family='Times New Roman, serif' font-size='13' fill='#dc2626'>log_2 x</text>"
              "<text x='235' y='55' font-family='Times New Roman, serif' font-size='13' fill='#1e40af'>ln x</text>"
              "<text x='235' y='82' font-family='Times New Roman, serif' font-size='13' fill='#0d9488'>log x</text></svg>")


def cands():
    C = []

    # ======================= MCQ easy (10) =======================
    C.append(mcq('easy', 'sec1_graph', 'ដែនកំណត់នៃអនុគមន៍ ' + M(r'y=\log_a x') + ' គឺ ៖', M('x>0'), [M('x\\ge0'), M('x<0'), M('x\\in\\mathbb{R}')],
                 'លោការីតមានន័យតែចំពោះចំនួនវិជ្ជមាន។', 'Remember'))
    C.append(mcq('easy', 'sec1_graph', 'ក្រាបនៃ ' + M(r'y=\log_a x') + ' កាត់តាមចំណុចថេរមួយគឺ ៖', M('(1,0)'), [M('(0,1)'), M('(0,0)'), M('(1,1)')],
                 M(r'\log_a1=0') + '។', 'Remember'))
    C.append(mcq('easy', 'sec1_graph', 'បើ ' + M('a>1') + ' នោះ ' + M(r'y=\log_a x') + ' ជា ៖', 'អនុគមន៍កើន', ['អនុគមន៍ចុះ', 'អនុគមន៍ថេរ', 'អនុគមន៍សេស'],
                 'គោលធំជាង ១ ក្រាបកើនពីឆ្វេងទៅស្តាំ។', 'Remember'))
    C.append(mcq('easy', 'sec1_graph', 'បើ ' + M('0<a<1') + ' នោះ ' + M(r'y=\log_a x') + ' ជា ៖', 'អនុគមន៍ចុះ', ['អនុគមន៍កើន', 'អនុគមន៍ថេរ', 'អនុគមន៍គូ'],
                 'គោលនៅចន្លោះ ០ និង ១ ក្រាបចុះ។', 'Remember'))
    C.append(with_img(mcq('easy', 'sec1_graph', 'ក្រាបនៃ ' + M(r'y=\log_a x') + ' និង ' + M('y=a^x') + ' ឆ្លុះគ្នាធៀបនឹង ៖', 'បន្ទាត់ ' + M('y=x'),
                 ['អ័ក្ស ' + M('Ox'), 'អ័ក្ស ' + M('Oy'), 'ដើមតម្រុយ'], 'ពីព្រោះជាអនុគមន៍ច្រាសគ្នា។', 'Understand'), FIG_INV))
    C.append(mcq('easy', 'sec1_def', M(r'\log_2 8') + ' ស្មើនឹង ៖', M(3), opts(2, 4, 16), M('2^3=8') + '។', 'Apply'))
    C.append(mcq('easy', 'sec1_def', M(r'\log_{10} 1000') + ' ស្មើនឹង ៖', M(3), opts(1, 10, 100), M('10^3=1000') + '។', 'Apply'))
    C.append(mcq('easy', 'sec1_def', M(r'\log_a 1') + ' និង ' + M(r'\log_a a') + ' ស្មើគ្នារៀងគ្នា ៖', M('0') + ' និង ' + M('1'),
                [M('1') + ' និង ' + M('0'), M('0') + ' និង ' + M('0'), M('1') + ' និង ' + M('1')], M('a^0=1,\\ a^1=a') + '។', 'Remember'))
    C.append(mcq('easy', 'sec1_def', 'ទំនាក់ទំនង ' + M('2^5=32') + ' សរសេរជាលោការីតបាន ៖', M(r'\log_2 32=5'), [M(r'\log_5 32=2'), M(r'\log_{32}2=5'), M(r'\log_2 5=32')],
                 M('a^x=y\\iff x=\\log_a y') + '។', 'Understand'))
    C.append(with_img(mcq('easy', 'sec5_nat', 'សញ្ញា ' + M(r'\ln x') + ' មានន័យថា ៖', M(r'\log_e x'), [M(r'\log_{10}x'), M(r'\log_2 x'), M(r'\dfrac1x')],
                 M('e\\approx2.718') + ' ជាគោលនៃលោការីតនេពែ។', 'Remember'), FIG_LOGCMP))

    # ======================= MCQ medium (14) =======================
    C.append(mcq('medium', 'sec3_base', M(r'\log_9 27') + ' ស្មើនឹង ៖', fr(F(3, 2)), [fr(F(2, 3)), M('3'), M('2')], M(r'\dfrac{\log_3 27}{\log_3 9}=\dfrac32') + '។', 'Apply'))
    C.append(mcq('medium', 'sec3_base', M(r'\log_{27}\dfrac13') + ' ស្មើនឹង ៖', fr(F(-1, 3)), [fr(F(1, 3)), M('-3'), M('3')], M(r'\log_{3^3}3^{-1}=-\dfrac13') + '។', 'Apply'))
    C.append(mcq('medium', 'sec3_base', M(r'\log_{1/2} 8') + ' ស្មើនឹង ៖', M(-3), [M('3'), M(r'-\dfrac13'), M('-4')], M(r'\left(\tfrac12\right)^{-3}=8') + '។', 'Apply'))
    C.append(mcq('medium', 'sec4_eq', M(r'\log_4 x=\dfrac52') + ' មានចម្លើយ ៖', M('x=32'), opts('x=10', 'x=16', 'x=64'), M('x=4^{5/2}=2^5=32') + '។', 'Apply'))
    C.append(mcq('medium', 'sec4_eq', M(r'\log_9 x=\dfrac32') + ' មានចម្លើយ ៖', M('x=27'), opts('x=18', 'x=81', 'x=13.5'), M('x=9^{3/2}=27') + '។', 'Apply'))
    C.append(mcq('medium', 'sec4_eq', M(r'\log_{1/10}x=-3') + ' មានចម្លើយ ៖', M('x=1000'), opts('x=0.001', 'x=30', 'x=-1000'), M('x=(1/10)^{-3}=1000') + '។', 'Apply'))
    C.append(mcq('medium', 'sec4_eq', M(r'\log_x 9=2') + ' មានចម្លើយ ៖', M('x=3'), opts('x=-3', 'x=4.5', 'x=81'), M('x^2=9') + ' ហើយគោលត្រូវវិជ្ជមាន ដូច្នេះ ' + M('x=3') + '។', 'Apply'))
    C.append(mcq('medium', 'sec4_ineq', M(r'\log_3(3x-5)>\log_3(x+7)') + ' មានចម្លើយ ៖', M('x>6'), opts('x<6', 'x>5/3', 'x>-7'), M('3x-5>x+7\\Rightarrow x>6') + '។', 'Apply'))
    C.append(mcq('medium', 'sec4_ineq', M(r'\log_{1/2}(2x-1)\le2') + ' មានចម្លើយ ៖', M(r'x\ge\dfrac58'), [M(r'x\le\dfrac58'), M(r'x\ge\dfrac12'), M(r'x\ge\dfrac34')],
                 'គោល ' + M('<1') + ' ប្តូរទិស៖ ' + M('2x-1\\ge\\tfrac14\\Rightarrow x\\ge\\tfrac58') + '។', 'Apply'))
    C.append(mcq('medium', 'sec4_ineq', M(r'\log_{1/3}x<0') + ' មានចម្លើយ ៖', M('x>1'), opts('x<1', '0<x<1', 'x<0'), M('\\log_{1/3}x<\\log_{1/3}1\\Rightarrow x>1') + '។', 'Apply'))
    C.append(mcq('medium', 'sec4_ineq', M(r'\log_x27\ge3') + ' មានចម្លើយ ៖', M('1<x\\le3'), [M('x\\le3'), M('x\\ge3'), M('0<x<1')],
                 'ចំពោះ ' + M('x>1') + ' ៖ ' + M('27\\ge x^3\\Rightarrow x\\le3') + ' ចំពោះ ' + M('0<x<1') + ' ' + M('\\log_x27<0') + ' មិនត្រូវ។', 'Analyze'))
    C.append(mcq('medium', 'sec5_nat', M('e^{x-2}=12') + ' មានចម្លើយ ៖', M('x=\\ln12+2'), [M('x=\\ln10+2'), M('x=12e^2'), M('x=\\ln12-2')], M('x-2=\\ln12') + '។', 'Apply'))
    C.append(mcq('medium', 'sec1_graph', 'ដែនកំណត់នៃ ' + M(r'y=\log_3(x-2)') + ' គឺ ៖', M('x>2'), [M('x>0'), M('x>-2'), M('x\\ne2')], M('x-2>0') + '។ ក្រាបរំកិល ' + M('\\log_3x') + ' ទៅស្តាំ ២។', 'Understand'))

    C.append(mcq('medium', 'sec3_base', M(r'\log_7 27') + ' ស្មើប្រហែល ៖', M(d(lg(7, 27), 4)), [M(d(lg(27, 7), 4)), M('3.8571'), M('0.5905')],
                 M(r'\dfrac{\log27}{\log7}\approx1.6937') + '។', 'Apply'))

    # ======================= MCQ hard (7) =======================
    C.append(mcq('hard', 'sec4_eq', 'សមីការ ' + M(r'6(\log_x8+\log_8x)=13') + ' មានឫសពីរ។ ផលគុណឫសស្មើ ៖', M(r'64\sqrt2'), [M('64'), M(r'16\sqrt2'), M('20')],
                 'តាង ' + M('t=\\log_8x') + ' ៖ ' + M('6t^2-13t+6=0') + ' ឱ្យ ' + M('x=4,\\ 16\\sqrt2') + ' ផលគុណ ' + M('64\\sqrt2') + '។', 'Analyze'))
    C.append(mcq('hard', 'sec4_eq', 'សមីការ ' + M(r'\log_9x+\log_x9=\dfrac52') + ' មានឫសពីរ។ ផលគុណឫសស្មើ ៖', M('243'), opts(84, 81, 27), 'ឫស ' + M('3') + ' និង ' + M('81') + ' ផលគុណ ' + M('243') + '។', 'Analyze'))
    C.append(mcq('hard', 'sec4_eq', M(r'\log x+\log(x+9)=1') + ' មានចម្លើយ ៖', M('x=1'), opts('x=-10', 'x=10', 'x=9'), M('x(x+9)=10') + ' ឱ្យ ' + M('x=1') + ' ឬ ' + M('-10') + ' ប៉ុន្តែ ' + M('x>0') + '។', 'Analyze'))
    C.append(mcq('hard', 'sec4_ineq', M(r'\log_2(2x)\le\log_4(x+3)') + ' មានចម្លើយ ៖', M('0<x\\le1'), [M('x\\le1'), M('-\\tfrac34\\le x\\le1'), M('x\\ge1')],
                 M('4x^2\\le x+3\\Rightarrow -\\tfrac34\\le x\\le1') + ' ហើយ ' + M('x>0') + '។', 'Analyze'))
    C.append(mcq('hard', 'sec4_ineq', M(r'\log\dfrac{x^2-x}{x^2-1}<0') + '។ ចំនួនគត់ក្នុង ' + M('[-3,3]') + ' ដែលជាចម្លើយមាន ៖', M(2), opts(1, 3, 4),
                 M('\\dfrac{x^2-x}{x^2-1}=\\dfrac{x}{x+1}') + ' ត្រូវ ' + M('0<\\tfrac x{x+1}<1') + ' គឺ ' + M('x>0,\\ x\\ne1') + ' ដូច្នេះ ' + M('x=2,3') + '។', 'Analyze'))
    C.append(mcq('hard', 'sec4_ineq', M(r'\log_{0.5}x^2<\log_{0.5}3x') + ' មានចំនួនគត់តូចបំផុតជាចម្លើយ ៖', M(4), opts(1, 3, 2),
                 M('x^2>3x') + ' និង ' + M('x>0') + ' ឱ្យ ' + M('x>3') + ' ចំនួនគត់តូចបំផុត ' + M('4') + '។', 'Analyze'))
    C.append(mcq('hard', 'sec2_shift', 'តម្លៃ ' + M('a') + ' ដែលធ្វើឱ្យ ' + M(r'\log_{\frac1{a+1}}(x^2+2)\ge1') + ' ពិតគ្រប់ ' + M('x') + ' គឺ ៖', M(r'a=-\dfrac14'), [M(r'a=\dfrac12'), M('a=-1'), M(r'a=-\dfrac34')],
                 'ត្រូវ ' + M('1<\\tfrac1{a+1}\\le2') + ' ឱ្យ ' + M('-\\tfrac12\\le a<0') + '។', 'Analyze'))

    # ======================= MCQ pisa (5) =======================
    C.append(mcq('pisa', 'sec6_apply', 'ដាក់ ២ ៩២៥ ០០០ ៛ ការប្រាក់ ១០% ក្នុងមួយឆ្នាំ ទូទាត់មួយឆមាសម្តង ។ ប៉ុន្មានឆ្នាំ ទើបកើនដល់ ៣ ៧០៥ ០០០ ៛ ?',
                 M('\\approx%s\\text{ ឆ្នាំ}' % d(T_BANK)), [M('\\approx1.26\\text{ ឆ្នាំ}'), M('\\approx4.84\\text{ ឆ្នាំ}'), M('\\approx5\\text{ ឆ្នាំ}')],
                 M('1.05^{2t}=1.26667\\Rightarrow t=\\dfrac{\\log1.26667}{2\\log1.05}\\approx2.42') + '។', 'Evaluate'))
    C.append(mcq('pisa', 'sec6_apply', 'ស្ករ ១៣០ mg រលាយក្នុងរាងកាយអត្រា ១១% ក្នុងមួយម៉ោង ។ ប៉ុន្មានម៉ោងរលាយអស់ពាក់កណ្តាល ?',
                 M('\\approx%s\\text{ ម៉ោង}' % d(T_SUGAR)), [M('\\approx0.5\\text{ ម៉ោង}'), M('\\approx9\\text{ ម៉ោង}'), M('\\approx11\\text{ ម៉ោង}')],
                 M('0.89^t=0.5\\Rightarrow t=\\dfrac{\\log0.5}{\\log0.89}\\approx5.95') + '។', 'Evaluate'))
    C.append(mcq('pisa', 'sec6_apply', 'ដាក់ប្រាក់ ការប្រាក់ ៦% ក្នុងមួយឆ្នាំ ។ ប៉ុន្មានឆ្នាំ ទើបប្រាក់កើនពីរដង ?',
                 M('\\approx%s\\text{ ឆ្នាំ}' % d(T_DBL)), [M('\\approx6\\text{ ឆ្នាំ}'), M('\\approx16.7\\text{ ឆ្នាំ}'), M('\\approx2\\text{ ឆ្នាំ}')],
                 M('1.06^t=2\\Rightarrow t=\\dfrac{\\ln2}{\\ln1.06}\\approx11.90') + '។', 'Evaluate'))
    C.append(mcq('pisa', 'sec6_apply', 'ឆ្នាំ ២០០០ ចិនមាន ' + M('1.26') + ' ពាន់លាននាក់ ឥណ្ឌា ' + M('1.01') + ' ពាន់លាននាក់ ។ ' + M('C(t)=1.26e^{0.009t}') + ' និង ' + M('I(t)=1.01e^{0.015t}') + '។ ឥណ្ឌាមានច្រើនជាងចិនចាប់ពីឆ្នាំ ៖',
                 M('2037'), opts(2025, 2031, 2050), M('t>\\dfrac{\\ln(1.26/1.01)}{0.006}\\approx36.9') + ' ដូច្នេះ ' + M('2037') + '។', 'Evaluate'))
    C.append(mcq('pisa', 'sec6_apply', 'តម្លៃម៉ូតូ ' + M('V=10000e^{-pt}') + ' ដែល ' + M('t') + ' ជាខែ ហើយក្រោយ ១២ ខែ ' + M('V=5000') + '។ ក្រោយ ១៨ ខែ តម្លៃប្រហែល ៖',
                 M(d(V18) + '\\$'), [M('2500\\$'), M('3750\\$'), M('4000\\$')], M('p=\\dfrac{\\ln2}{12},\\ V(18)=10000\\cdot2^{-3/2}\\approx3535.53') + '។', 'Evaluate'))

    # ======================= Writing easy (1) =======================
    C.append(wr('easy', 'sec3_base', 'គណនា ' + M(r'\log_9 27') + ' ដោយប្រើរូបមន្តប្តូរគោល ។',
                [('រូបមន្ត ' + M(r'\log_ax=\dfrac{\log_bx}{\log_ba}') + '។', 1), ('យកគោល ' + M('b=3') + ' ៖ ' + M(r'\log_927=\dfrac{\log_327}{\log_39}') + '។', 1),
                 (M(r'\log_327=3') + '។', 1), (M(r'\log_39=2') + '។', 1), (M(r'\log_927=\dfrac32') + '។', 1)], 'Apply'))

    # ======================= Writing medium (4) =======================
    C.append(wr('medium', 'sec4_eq', 'ដោះស្រាយសមីការ ' + M(r'\log x+\log(x+9)=1') + ' ។',
                [('លក្ខខណ្ឌ ' + M('x>0') + '។', 1), (M(r'\log[x(x+9)]=1') + '។', 1), (M('x(x+9)=10') + '។', 1), (M('x^2+9x-10=0\\Rightarrow x=1') + ' ឬ ' + M('x=-10') + '។', 1),
                 ('ដោយ ' + M('x>0') + ' ចម្លើយ ' + M('x=1') + '។', 1)], 'Apply'))
    C.append(wr('medium', 'sec4_ineq', 'ដោះស្រាយ និងផ្ទៀងផ្ទាត់ ' + M(r'\log_3(3x-5)>\log_3(x+7)') + ' ។',
                [('គោល ' + M('3>1') + ' រក្សាទិស ៖ ' + M('3x-5>x+7') + '។', 1), (M('2x>12\\Rightarrow x>6') + '។', 1), ('លក្ខខណ្ឌ ' + M('3x-5>0\\Rightarrow x>\\tfrac53') + '។', 1),
                 ('លក្ខខណ្ឌ ' + M('x+7>0\\Rightarrow x>-7') + '។', 1), ('ចម្លើយ ' + M('x\\in(6,+\\infty)') + '។', 1)], 'Apply'))
    C.append(wr('medium', 'sec4_ineq', 'ដោះស្រាយ ' + M(r'\log_{1/2}(2x-1)\le2') + ' ។',
                [('សរសេរ ' + M(r'2=\log_{1/2}\left(\tfrac12\right)^2=\log_{1/2}\tfrac14') + '។', 1), ('គោល ' + M('<1') + ' ប្តូរទិស ៖ ' + M('2x-1\\ge\\tfrac14') + '។', 1),
                 (M('x\\ge\\tfrac58') + '។', 1), ('លក្ខខណ្ឌ ' + M('2x-1>0\\Rightarrow x>\\tfrac12') + '។', 1), ('ចម្លើយ ' + M('\\left[\\tfrac58,+\\infty\\right)') + '។', 1)], 'Apply'))
    C.append(wr('medium', 'sec2_shift', 'សង់តារាងតម្លៃ និងពន្យល់ការសង់ក្រាប ' + M(r'y=\log_3(x-2)') + ' ។',
                [('ដែនកំណត់ ' + M('x-2>0\\Rightarrow x>2') + '។', 1), ('តារាង ' + M('x=\\tfrac73,3,5,11') + ' ឱ្យ ' + M('y=-1,0,1,2') + '។', 1),
                 ('ក្រាបកាត់ ' + M('(3,0)') + ' ជំនួស ' + M('(1,0)') + '។', 1), ('រំកិលក្រាប ' + M(r'y=\log_3x') + ' ទៅស្តាំ ២ ឯកតា។', 1),
                 ('ក្រាបមានអាស៊ីមតូតឈរ ' + M('x=2') + '។', 1)], 'Apply'))

    # ======================= Writing hard (4) =======================
    C.append(wr('hard', 'sec4_eq', 'ដោះស្រាយ ' + M(r'6(\log_x8+\log_8x)=13') + ' ។',
                [('លក្ខខណ្ឌ ' + M('x>0,\\ x\\ne1') + ' ហើយ ' + M(r'\log_x8=\dfrac1{\log_8x}') + '។', 1), ('តាង ' + M('t=\\log_8x') + ' ៖ ' + M(r'6\left(\dfrac1t+t\right)=13') + '។', 1),
                 (M('6t^2-13t+6=0') + '។', 1), (M('(3t-2)(2t-3)=0\\Rightarrow t=\\dfrac23,\\ \\dfrac32') + '។', 1), (M('x=8^{2/3}=4') + ' ឬ ' + M('x=8^{3/2}=16\\sqrt2') + '។', 1)], 'Analyze'))
    C.append(wr('hard', 'sec4_eq', 'ដោះស្រាយ ' + M(r'\log(x+10)+\dfrac12\log x^2=2-\log4') + ' ។',
                [('លក្ខខណ្ឌ ' + M('x+10>0,\\ x\\ne0') + '។', 1), (M(r'\tfrac12\log x^2=\log|x|') + '។', 1), (M(r'\log[(x+10)|x|]=\log25') + ' ឱ្យ ' + M('(x+10)|x|=25') + '។', 1),
                 ('ចំពោះ ' + M('x>0') + ' ៖ ' + M('x^2+10x-25=0\\Rightarrow x=5\\sqrt2-5') + '។', 1), ('ចំពោះ ' + M('x<0') + ' ៖ ' + M('x^2+10x+25=0\\Rightarrow x=-5') + '។', 1)], 'Analyze'))
    C.append(wr('hard', 'sec4_eq', 'ដោះស្រាយ ' + M('8^x-2^{x+2}=15') + ' ដោយតាង ' + M('u=2^x') + ' ។',
                [(M('8^x=u^3') + ' និង ' + M('2^{x+2}=4u') + '។', 1), (M('u^3-4u-15=0') + '។', 1), (M('u=3') + ' ជាឫស ព្រោះ ' + M('27-12-15=0') + '។', 1),
                 (M('(u-3)(u^2+3u+5)=0') + ' ហើយ ' + M('u^2+3u+5>0') + ' (' + M('\\Delta=-11<0') + ')។', 1), (M('2^x=3\\Rightarrow x=\\log_23') + '។', 1)], 'Analyze'))
    C.append(wr('hard', 'sec4_ineq', 'រកតម្លៃ ' + M('m') + ' ដើម្បីឱ្យ ' + M(r'1+\log_5(x^2+1)\ge\log_5(mx^2+4x+m)') + ' ពិតគ្រប់ ' + M('x') + ' ។',
                [('ត្រូវ ' + M('mx^2+4x+m>0') + ' គ្រប់ ' + M('x') + ' ៖ ' + M('m>0') + ' និង ' + M('16-4m^2<0\\Rightarrow m>2') + '។', 1),
                 ('វិសមីការសមមូល ' + M('5(x^2+1)\\ge mx^2+4x+m') + '។', 1), (M('(5-m)x^2-4x+(5-m)\\ge0') + ' គ្រប់ ' + M('x') + '។', 1),
                 (M('5-m>0') + ' និង ' + M('16-4(5-m)^2\\le0\\Rightarrow 5-m\\ge2') + ' គឺ ' + M('m\\le3') + '។', 1), ('សរុប ' + M('2<m\\le3') + '។', 1)], 'Analyze'))

    # ======================= Writing pisa (5) =======================
    C.append(wr('pisa', 'sec6_apply', 'ដាក់ ២ ៩២៥ ០០០ ៛ ការប្រាក់ ១០% ក្នុងមួយឆ្នាំ ទូទាត់មួយឆមាសម្តង ។ រកពេលដែលប្រាក់កើនដល់ ៣ ៧០៥ ០០០ ៛ ។',
                [('រូបមន្ត ' + M('A=P(1+\\tfrac rn)^{nt}') + ' ដែល ' + M('n=2,\\ r=0.10') + '។', 1), (M('3\\,705\\,000=2\\,925\\,000(1.05)^{2t}') + '។', 1),
                 (M('1.05^{2t}=1.26667') + '។', 1), (M('2t\\log1.05=\\log1.26667') + '។', 1), (M('t\\approx%s' % d(T_BANK)) + ' ឆ្នាំ។', 1)], 'Evaluate'))
    C.append(wr('pisa', 'sec6_apply', 'ស្ករ ១៣០ mg រលាយក្នុងរាងកាយអត្រា ១១% ក្នុងមួយម៉ោង ។ រកពេលដែលស្ករនៅសល់ពាក់កណ្តាល ។',
                [('រូបមន្ត ' + M('y=a(1-r)^t') + '។', 1), (M('65=130(0.89)^t') + '។', 1), (M('0.89^t=0.5') + '។', 1), (M('t=\\dfrac{\\log0.5}{\\log0.89}') + '។', 1),
                 (M('t\\approx%s' % d(T_SUGAR, 3)) + ' ម៉ោង ≈ ៦ ម៉ោង។', 1)], 'Evaluate'))
    C.append(wr('pisa', 'sec6_apply', 'ដាក់ ២ ០០០ ០០០ ៛ ការប្រាក់ ៦% ក្នុងមួយឆ្នាំ ។ រកពេលដែលប្រាក់កើនពីរដង និងពន្យល់ថាតើវាអាស្រ័យនឹងប្រាក់ដើមឬទេ ។',
                [(M('2P=P(1.06)^t') + '។', 1), (M('1.06^t=2') + '។', 1), (M('t=\\dfrac{\\ln2}{\\ln1.06}') + '។', 1), (M('t\\approx%s' % d(T_DBL)) + ' ឆ្នាំ។', 1),
                 ('ប្រាក់ដើម ' + M('P') + ' ត្រូវកាត់ចោល ដូច្នេះពេលកើនពីរដងមិនអាស្រ័យនឹងប្រាក់ដើមទេ។', 1)], 'Evaluate'))
    C.append(wr('pisa', 'sec6_apply', M('C(t)=1.26e^{0.009t}') + ' និង ' + M('I(t)=1.01e^{0.015t}') + ' ជាចំនួនប្រជាជនចិន និងឥណ្ឌា (ពាន់លាននាក់) ចាប់ពីឆ្នាំ ២០០០ ។ រកឆ្នាំដែលឥណ្ឌាច្រើនជាងចិន ។',
                [('ត្រូវ ' + M('1.01e^{0.015t}>1.26e^{0.009t}') + '។', 1), (M('e^{0.006t}>\\dfrac{1.26}{1.01}') + '។', 1), (M('0.006t>\\ln\\dfrac{1.26}{1.01}') + '។', 1),
                 (M('t>%s' % d(T_POP, 1)) + '។', 1), ('ដូច្នេះឆ្នាំ ' + M('2037') + ' (' + M('t=37') + ')។', 1)], 'Evaluate'))
    k = log(2) / 8
    C.append(wr('pisa', 'sec6_apply', 'តម្លៃផ្ទះ ' + M('V=V_0e^{kt}') + '។ ក្រោយ ៨ ឆ្នាំ តម្លៃស្មើពីរដងតម្លៃដើម ។ រក ' + M('k') + ' និងពេលដែលតម្លៃស្មើបីដង ។',
                [(M('2V_0=V_0e^{8k}') + ' ឱ្យ ' + M('e^{8k}=2') + '។', 1), (M('k=\\dfrac{\\ln2}{8}\\approx%s' % d(k, 4)) + '។', 1), (M('3=e^{kt}') + '។', 1),
                 (M('t=\\dfrac{\\ln3}{k}=\\dfrac{8\\ln3}{\\ln2}') + '។', 1), (M('t\\approx%s' % d(log(3) / k)) + ' ឆ្នាំ។', 1)], 'Evaluate'))

    bloom_for = {'easy': 'Understand', 'medium': 'Apply', 'hard': 'Analyze', 'pisa': 'Evaluate'}
    for q in C:
        q['bloom'] = q.get('bloom') or bloom_for[q['level']]
    return C
