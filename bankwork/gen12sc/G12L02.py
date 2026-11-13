# -*- coding: utf-8 -*-
"""
KhmerMath Question Bank: Grade 12 Science (SC)
Chapter 1: ចំនួនកុំផ្លិច
Lesson 2: ចំនួនកុំផ្លិចទម្រង់ត្រីកោណមាត្រ
Reference textbook: Lesson/G12/SC/C1-L2.tex

Target matrix: MCQ easy10/medium14/hard7/pisa5 + writing easy1/medium4/hard4/pisa5 = 50, a Bloom level on each.
Every number comes from sympy; verify() re-derives the claims a second time, independently of the code that wrote them.
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib import *
import svgkit as K
from sympy import (I, Rational, sqrt, simplify, expand, expand_complex, re as sre, im as sim, nsimplify, latex, pi, cos, sin, Abs, arg,
                   symbols, solve, N as numeval)

LESSON = 'ចំនួនកុំផ្លិចទម្រង់ត្រីកោណមាត្រ'
CHAPTER = 'ជំពូកទី 1 : ចំនួនកុំផ្លិច'
GRADE = '12SC'
TARGET = {('mcq', 'easy'): 10, ('mcq', 'medium'): 14, ('mcq', 'hard'): 7, ('mcq', 'pisa'): 5,
          ('writing', 'easy'): 1, ('writing', 'medium'): 4, ('writing', 'hard'): 4, ('writing', 'pisa'): 5}
S1, S2, S3, S4, S5 = 'ម៉ូឌុលនៃចំនួនកុំផ្លិច', 'អាគុយម៉ង់នៃចំនួនកុំផ្លិច', 'ទម្រង់ត្រីកោណមាត្រ', 'ផលគុណនិងផលចែកតាមទម្រង់ត្រីកោណមាត្រ', 'បំប្លែងវិល'
TOPIC_MAP = {'s1_mod': S1, 's2_arg': S2, 's3_trig': S3, 's4_muldiv': S4, 's5_rot': S5,
             'pisa_ship': S1, 'pisa_phasor': S3, 'pisa_arm': S5, 'pisa_gear': S5, 'pisa_wind': S5,
             'pisa_series': S1, 'pisa_turbine': S5, 'pisa_arm2': S3, 'pisa_drone': S5, 'pisa_signal': S4}


# ----------------------------------------------------------------------------- helpers
def _L(x):
    return latex(x).replace('\\frac', '\\dfrac')


def val(z):
    return nsimplify(simplify(expand_complex(expand(z))))


def fz(z):
    """complex number -> LaTeX a+bi, with brackets around a part that has several terms: (1-2\\sqrt3)+(2+\\sqrt3)i"""
    from sympy import Add
    z = val(z)
    a, b = simplify(sre(z)), simplify(sim(z))
    if b == 0:
        return _L(a)
    neg = (not isinstance(b, Add)) and b.could_extract_minus_sign()
    bb = -b if neg else b
    bs = '' if bb == 1 else (('(' + _L(bb) + ')') if isinstance(bb, Add) else _L(bb))
    if a == 0:
        return ('-' if neg else '') + bs + 'i'
    as_ = ('(' + _L(a) + ')') if isinstance(a, Add) else _L(a)
    return as_ + (' - ' if neg else ' + ') + bs + 'i'


def Z(z):
    return M(fz(z))


def A(p):
    """angle p*pi -> LaTeX"""
    p = Rational(p)
    if p == 0:
        return '0'
    n, d = p.p, p.q
    sg = '-' if n < 0 else ''
    n = abs(n)
    top = '\\pi' if n == 1 else '%d\\pi' % n
    return sg + (top if d == 1 else '\\dfrac{%s}{%d}' % (top, d))


def _arg_in(p):
    t = A(p)
    return '\\left(%s\\right)' % t if t.startswith('-') else ' ' + t


def TF(r, p):
    """r(cos p*pi + i sin p*pi) with brackets around negative angles."""
    r = nsimplify(r)
    rs = '' if r == 1 else _L(r) + ' '
    return M('%s\\left(\\cos%s + i\\sin%s\\right)' % (rs, _arg_in(p), _arg_in(p)))


def cis(r, p):
    return val(r * (cos(p * pi) + I * sin(p * pi)))


def ARGM(p):
    return M(A(p))


def principal(z):
    return nsimplify(simplify(arg(val(z)) / pi))


def cz(a, b=0):
    return a + b * I


def with_img(q, svg):
    q['img'] = svg
    return q


# ----------------------------------------------------------------------------- figures (IMAGE_STYLE_GUIDE.md)
def fig_triangle():
    return K.plane((-1, 6), (-1, 5), unit=40, segs=[(0, 0, 4, 3, K.BLUE, False), (4, 0, 4, 3, K.AXIS, True)],
                   pts=[(4, 3, 'M', 9, -8, K.RED), (4, 0, 'N', 9, -9, K.AXIS)])


def fig_angle60():
    s3 = float(sqrt(3))
    return K.plane((-1, 3), (-1, 3), unit=64, segs=[(0, 0, 1, s3, K.BLUE, False)] + K.dashed_to_axes(1, s3),
                   arcs=[(0, 0, 0.45, 0, 60, K.RED)], pts=[(1, s3, 'M', 9, -8, K.RED)], notes=[(0.55, 0.12, 'φ', 4, 4, K.RED, True)])


def fig_two_angles():
    import math
    p1 = (3 * math.cos(math.pi / 4), 3 * math.sin(math.pi / 4))
    p2 = (4 * math.cos(math.pi / 6), 4 * math.sin(math.pi / 6))
    return K.plane((-1, 5), (-1, 4), unit=46, vecs=[(0, 0, p1[0], p1[1], K.BLUE, False), (0, 0, p2[0], p2[1], K.RED, False)],
                   arcs=[(0, 0, 0.9, 0, 45, K.BLUE), (0, 0, 1.5, 0, 30, K.RED)],
                   pts=[(p1[0], p1[1], 'z_1', -6, -12, K.BLUE), (p2[0], p2[1], 'z_2', 10, 6, K.RED)],
                   notes=[(0.55, 0.62, 'π/4', -4, -2, K.BLUE, False), (1.55, 0.35, 'π/6', 12, 14, K.RED, False)])


def fig_tangent():
    return K.plane((-4, 5), (-1, 9), unit=32, circles=[(0, 5, 3, K.GREEN, False)],
                   segs=[(0, 0, 2.4, 3.2, K.BLUE, False), (0, 5, 2.4, 3.2, K.AXIS, True)],
                   pts=[(2.4, 3.2, 'P', 10, 14, K.RED), (0, 5, 'Q', 11, 5, K.INK)])


def fig_ship():
    return K.plane((-1, 6), (-1, 6), unit=40, segs=[(0, 0, 3, 4, K.BLUE, False), (3, 0, 3, 4, K.AXIS, True), (0, 0, 3, 0, K.AXIS, True)],
                   pts=[(3, 4, 'S', 9, -8, K.RED), (0, 0, 'P', -14, -2, K.INK)])


def fig_arm():
    import math
    return K.plane((-5, 5), (-1, 5), unit=40, segs=[(0, 0, 4, 0, K.AXIS, True)],
                   vecs=[(0, 0, 4 * math.cos(2 * math.pi / 3), 4 * math.sin(2 * math.pi / 3), K.BLUE, False)],
                   arcs=[(0, 0, 1.2, 0, 120, K.RED)], pts=[(4 * math.cos(2 * math.pi / 3), 4 * math.sin(2 * math.pi / 3), 'E', -14, -8, K.RED)],
                   notes=[(0.5, 0.9, '2π/3', 6, 4, K.RED, False)])


def fig_windmill():
    import math
    return K.plane((-6, 6), (-6, 6), unit=26, circles=[(0, 0, 5, K.GREEN, True)],
                   vecs=[(0, 0, 5, 0, K.BLUE, False), (0, 0, 5 * math.cos(math.pi / 6), 5 * math.sin(math.pi / 6), K.RED, False)],
                   arcs=[(0, 0, 1.6, 0, 30, K.RED)],
                   pts=[(5, 0, 'T_0', 3, -10, K.BLUE), (5 * math.cos(math.pi / 6), 5 * math.sin(math.pi / 6), 'T_1', 8, -6, K.RED)])


def fig_ineq():
    return K.plane((-3, 3), (-1, 4), unit=46,
                   vecs=[(0, 0, -1, 2, K.BLUE, False), (0, 0, 0, 3, K.RED, False)],
                   segs=[(-1, 2, 0, 3, K.BLUE, False), (0, 0, 1, 1, K.AXIS, True), (1, 1, 0, 3, K.AXIS, True)],
                   pts=[(-1, 2, 'N_1', -26, -4, K.BLUE), (0, 3, 'N', 10, -2, K.RED), (1, 1, 'N_2', 10, 14, K.AXIS)])


def fig_square():
    return K.plane((-4, 4), (-4, 4), unit=36, polys=[([(3, 1), (-1, 3), (-3, -1), (1, -3)], K.BLUE, None, False)],
                   pts=[(3, 1, 'A', 9, -6, K.RED), (-1, 3, 'B', -6, -10, K.BLUE), (-3, -1, 'C', -18, 16, K.BLUE), (1, -3, 'D', 8, 16, K.BLUE)])


def fig_turbine():
    import math
    w = [(8, 0), (8 * math.cos(2 * math.pi / 3), 8 * math.sin(2 * math.pi / 3)), (8 * math.cos(4 * math.pi / 3), 8 * math.sin(4 * math.pi / 3))]
    return K.plane((-10, 10), (-10, 10), unit=17, grid=False, tick_every=4, circles=[(0, 0, 8, K.GREEN, True)],
                   segs=[(0, 0, w[0][0], w[0][1], K.BLUE, False), (0, 0, w[1][0], w[1][1], K.BLUE, False), (0, 0, w[2][0], w[2][1], K.BLUE, False)],
                   polys=[(w, K.RED, None, True)],
                   pts=[(w[0][0], w[0][1], 'w_0', 4, -10, K.RED), (w[1][0], w[1][1], 'w_1', -26, -6, K.RED), (w[2][0], w[2][1], 'w_2', -26, 14, K.RED)])


def fig_arm2():
    import math
    P = (3 * math.cos(math.pi / 6), 3 * math.sin(math.pi / 6))
    return K.plane((-1, 5), (-1, 5), unit=52, vecs=[(0, 0, P[0], P[1], K.BLUE, False), (P[0], P[1], P[0], P[1] + 2, K.RED, False)],
                   pts=[(P[0], P[1], 'P', 10, 14, K.BLUE), (P[0], P[1] + 2, 'E', 10, -2, K.RED)],
                   arcs=[(0, 0, 0.9, 0, 30, K.BLUE)], notes=[(1.0, 0.18, 'π/6', 4, 2, K.BLUE, False)])


def cands():
    C = []
    s3 = sqrt(3)

    # =============================================================================== MCQ EASY (10)
    C.append(mcq('easy', 's1_mod', 'ម៉ូឌុលនៃចំនួនកុំផ្លិច ' + M('z=a+bi') + ' (' + M('a,\\ b') + ' ជាចំនួនពិត) ត្រូវបានគណនាដោយរូបមន្តមួយណា ?',
                 M('|z|=\\sqrt{a^2+b^2}'), [M('|z|=a^2+b^2'), M('|z|=a+b'), M('|z|=\\sqrt{a^2-b^2}')],
                 'ម៉ូឌុលនៃ ' + M('z') + ' ជាប្រវែង ' + M('OM') + ' ដែល ' + M('M(a,\\ b)') + ' ជារូបភាពនៃ ' + M('z') + '។ តាមទ្រឹស្តីបទពីតាគ័រ ' + M('OM=\\sqrt{a^2+b^2}') + '។', bloom='Remember'))

    z = cz(-8, 6)
    C.append(mcq('easy', 's1_mod', 'គណនាម៉ូឌុល ' + M('|-8+6i|') + ' ៖', M('10'), [M('2'), M('14'), M('\\sqrt{14}')],
                 M('|-8+6i|=\\sqrt{(-8)^2+6^2}=\\sqrt{64+36}=\\sqrt{100}=10') + '។', bloom='Apply'))

    C.append(with_img(mcq('easy', 's1_mod', 'ក្នុងរូប ចំណុច ' + M('M') + ' ជារូបភាពនៃចំនួនកុំផ្លិច ' + M('z') + ' ហើយ ' + M('N') + ' ជាចំណោលកែងនៃ ' + M('M') + ' លើអ័ក្សពិត។ ម៉ូឌុល ' + M('|z|') + ' ស្មើ ៖',
                          M('5'), [M('7'), M('25'), M('\\sqrt{7}')],
                          'អានពីរូប ' + M('M(4,\\ 3)') + ' ដូច្នេះ ' + M('z=4+3i') + ' ហើយ ' + M('|z|=OM=\\sqrt{4^2+3^2}=\\sqrt{25}=5') + '។', bloom='Understand'),
                      fig_triangle()))

    C.append(mcq('easy', 's1_mod', 'ចំពោះគ្រប់ចំនួនកុំផ្លិច ' + M('z') + ' ឃ្លាមួយណាខាងក្រោម «ខុស» ?',
                 M('|z|=z\\cdot\\bar z'), [M('|z|=|\\bar z|'), M('|z|=|-z|'), M('|z|^2=z\\cdot\\bar z')],
                 M('z\\cdot\\bar z=a^2+b^2=|z|^2') + ' មិនមែន ' + M('|z|') + ' ទេ (ឧ. ' + M('z=3+4i') + ' ៖ ' + M('z\\bar z=25') + ' តែ ' + M('|z|=5') + ')។ ឃ្លាបីផ្សេងទៀតពិត។', bloom='Understand'))

    C.append(mcq('easy', 's2_arg', 'ចំនួនកុំផ្លិចមួយណាខាងក្រោម «គ្មាន» អាគុយម៉ង់ ?', M('0'), [M('1'), M('i'), M('-1')],
                 'អាគុយម៉ង់ជាម៉ុំ ' + M('(\\overrightarrow{Ox},\\overrightarrow{OM})') + ' ដែលត្រូវការវ៉ិចទ័រ ' + M('\\overrightarrow{OM}') + ' មិនសូន្យ។ ' + M('z=0') + ' មានរូបភាពជាគល់ ' + M('O') + ' ដូច្នេះគ្មានអាគុយម៉ង់។', bloom='Remember'))

    C.append(with_img(mcq('easy', 's2_arg', 'ក្នុងរូប ' + M('M') + ' ជារូបភាពនៃ ' + M('z=1+i\\sqrt3') + '។ អាគុយម៉ង់ ' + M('\\varphi') + ' នៃ ' + M('z') + ' (ក្នុង ' + M('-\\pi<\\varphi\\le\\pi') + ') ស្មើ ៖',
                          ARGM(Rational(1, 3)), [ARGM(Rational(1, 6)), ARGM(Rational(1, 4)), ARGM(Rational(2, 3))],
                          M('r=|z|=2') + '។ ' + M('\\cos\\varphi=\\dfrac12') + ' និង ' + M('\\sin\\varphi=\\dfrac{\\sqrt3}{2}') + ' ដូច្នេះ ' + M('\\varphi=\\dfrac{\\pi}{3}') + ' (កាដ្រង់ទី ១)។', bloom='Apply'),
                      fig_angle60()))

    z = cz(-1, 1) * 0 + (-1 + s3 * I)
    C.append(mcq('easy', 's2_arg', 'អាគុយម៉ង់ (ក្នុង ' + M('-\\pi<\\varphi\\le\\pi') + ') នៃ ' + M('z=-1+i\\sqrt3') + ' គឺ ៖',
                 ARGM(principal(z)), [ARGM(Rational(1, 3)), ARGM(Rational(-2, 3)), ARGM(Rational(5, 6))],
                 M('r=2') + '។ ' + M('\\cos\\varphi=-\\dfrac12<0') + ' និង ' + M('\\sin\\varphi=\\dfrac{\\sqrt3}{2}>0') + ' ដូច្នេះ ' + M('\\varphi') + ' នៅកាដ្រង់ទី ២ គឺ ' + M('\\dfrac{2\\pi}{3}') + '។', bloom='Understand'))

    C.append(mcq('easy', 's2_arg', 'អាគុយម៉ង់ (ក្នុង ' + M('-\\pi<\\varphi\\le\\pi') + ') នៃ ' + M('z=-i') + ' គឺ ៖',
                 ARGM(Rational(-1, 2)), [ARGM(Rational(1, 2)), ARGM(1), ARGM(0)],
                 M('-i=0+(-1)i') + ' ដូច្នេះ ' + M('r=1,\\ \\cos\\varphi=0,\\ \\sin\\varphi=-1') + ' នាំឱ្យ ' + M('\\varphi=-\\dfrac{\\pi}{2}') + '។', bloom='Apply'))

    C.append(mcq('easy', 's3_trig', 'ទម្រង់ត្រីកោណមាត្រនៃចំនួនកុំផ្លិច ' + M('z\\ne0') + ' គឺ ៖',
                 M('z=r(\\cos\\varphi+i\\sin\\varphi)') + ' ដែល ' + M('r=|z|') + ' និង ' + M('\\varphi=\\arg z'),
                 [M('z=r(\\cos\\varphi-i\\sin\\varphi)') + ' ដែល ' + M('r=|z|') + ' និង ' + M('\\varphi=\\arg z'), M('z=r(\\sin\\varphi+i\\cos\\varphi)') + ' ដែល ' + M('r=|z|') + ' និង ' + M('\\varphi=\\arg z'), M('z=|z|\\cos\\varphi+\\sin\\varphi') + ' ដែល ' + M('\\varphi=\\arg z')],
                 'ដោយ ' + M('a=r\\cos\\varphi') + ' និង ' + M('b=r\\sin\\varphi') + ' គេបាន ' + M('z=a+bi=r(\\cos\\varphi+i\\sin\\varphi)') + '។', bloom='Remember'))

    z = cis(2, Rational(1, 3))
    C.append(mcq('easy', 's3_trig', 'សរសេរ ' + TF(2, Rational(1, 3)) + ' ជាទម្រង់ ' + M('a+bi') + ' ៖', Z(z),
                 [Z(cz(s3, 1)), Z(cz(2, 2 * s3)), Z(cz(1, -s3))],
                 M('2\\left(\\dfrac12+\\dfrac{\\sqrt3}{2}i\\right)=1+\\sqrt3\\,i') + '។', bloom='Apply'))

    # =============================================================================== MCQ MEDIUM (14)
    z = cz(-4, 4)
    C.append(mcq('medium', 's3_trig', 'ទម្រង់ត្រីកោណមាត្រ (ក្នុង ' + M('-\\pi<\\varphi\\le\\pi') + ') នៃ ' + M('z=-4+4i') + ' គឺ ៖',
                 TF(4 * sqrt(2), Rational(3, 4)), [TF(4 * sqrt(2), Rational(-3, 4)), TF(4 * sqrt(2), Rational(1, 4)), TF(8, Rational(3, 4))],
                 M('r=\\sqrt{16+16}=4\\sqrt2') + '។ ' + M('\\cos\\varphi=-\\dfrac{\\sqrt2}{2}') + ' និង ' + M('\\sin\\varphi=\\dfrac{\\sqrt2}{2}') + ' ដូច្នេះ ' + M('\\varphi=\\dfrac{3\\pi}{4}') + '។', bloom='Apply'))

    C.append(mcq('medium', 's3_trig', 'ទម្រង់ត្រីកោណមាត្រ (ក្នុង ' + M('-\\pi<\\varphi\\le\\pi') + ') នៃ ' + M('z=2\\sqrt3-2i') + ' គឺ ៖',
                 TF(4, Rational(-1, 6)), [TF(4, Rational(1, 6)), TF(4, Rational(5, 6)), TF(8, Rational(-1, 6))],
                 M('r=\\sqrt{12+4}=4') + '។ ' + M('\\cos\\varphi=\\dfrac{\\sqrt3}{2}>0') + ' និង ' + M('\\sin\\varphi=-\\dfrac12<0') + ' ដូច្នេះ ' + M('\\varphi=-\\dfrac{\\pi}{6}') + ' (កាដ្រង់ទី ៤)។', bloom='Apply'))

    C.append(mcq('medium', 's4_muldiv', 'គេឱ្យ ' + M('z_1=') + ' ' + TF(2, Rational(1, 4)) + ' និង ' + M('z_2=') + ' ' + TF(3, Rational(1, 6)) + '។ ផលគុណ ' + M('z_1z_2') + ' ស្មើ ៖',
                 TF(6, Rational(5, 12)), [TF(5, Rational(5, 12)), TF(6, Rational(1, 24)), TF(6, Rational(1, 12))],
                 'គុណម៉ូឌុល បូកអាគុយម៉ង់ ៖ ' + M('2\\times3=6') + ' និង ' + M('\\dfrac\\pi4+\\dfrac\\pi6=\\dfrac{5\\pi}{12}') + '។', bloom='Apply'))

    C.append(mcq('medium', 's4_muldiv', 'គេឱ្យ ' + M('z_1=') + ' ' + TF(6, Rational(5, 12)) + ' និង ' + M('z_2=') + ' ' + TF(2, Rational(1, 12)) + '។ ផលចែក ' + M('\\dfrac{z_1}{z_2}') + ' ស្មើ ៖',
                 TF(3, Rational(1, 3)), [TF(3, Rational(1, 2)), TF(12, Rational(1, 3)), TF(3, Rational(1, 36))],
                 'ចែកម៉ូឌុល ដកអាគុយម៉ង់ ៖ ' + M('\\dfrac62=3') + ' និង ' + M('\\dfrac{5\\pi}{12}-\\dfrac{\\pi}{12}=\\dfrac{\\pi}{3}') + '។', bloom='Apply'))

    C.append(mcq('medium', 's3_trig', 'ចំនួនមួយណាខាងក្រោមមាន «ទម្រង់ត្រីកោណមាត្រ» ត្រឹមត្រូវ ' + M('r(\\cos\\varphi+i\\sin\\varphi)') + ' ដែល ' + M('r>0') + ' ?',
                 M('6\\left(\\cos\\dfrac{\\pi}{5}+i\\sin\\dfrac{\\pi}{5}\\right)'),
                 [M('-5\\left(\\cos\\dfrac{\\pi}{8}+i\\sin\\dfrac{\\pi}{8}\\right)'), M('\\sqrt2\\left(\\cos\\dfrac{3\\pi}{4}+i\\sin\\dfrac{5\\pi}{6}\\right)'),
                  M('-\\sqrt3\\left(\\sin\\dfrac{2\\pi}{3}+i\\cos\\dfrac{2\\pi}{3}\\right)')],
                 'ទម្រង់ត្រីកោណមាត្រត្រូវមានម៉ូឌុល ' + M('r>0') + ' ហើយ ' + M('\\cos') + ' និង ' + M('\\sin') + ' ត្រូវមានអាគុយម៉ង់ដូចគ្នា។ ជម្រើសទី ១ ពិត៖ ម៉ូឌុល ' + M('6>0') + ' អាគុយម៉ង់ ' + M('\\dfrac\\pi5') + ' ដូចគ្នា។ ជម្រើសផ្សេងមាន ' + M('r<0') + ' ឬអាគុយម៉ង់ខុសគ្នា ឬ ' + M('\\sin') + ' និង ' + M('\\cos') + ' ប្ដូរកន្លែង។', bloom='Analyze'))

    z = cz(1, 1)
    zp = val(I * z)
    C.append(mcq('medium', 's5_rot', 'រូបភាពនៃ ' + M('z=1+i') + ' តាមបំប្លែងវិលផ្ចិត ' + M('O') + ' ម៉ុំ ' + M('\\dfrac{\\pi}{2}') + ' គឺចំនួនកុំផ្លិច ៖',
                 Z(zp), [Z(-I * z), Z(-z), Z(cz(1, 1) * 2)],
                 M('z\'=(\\cos\\tfrac\\pi2+i\\sin\\tfrac\\pi2)z=i(1+i)=i+i^2=-1+i') + '។ (ការគុណនឹង ' + M('i') + ' បង្វិលចំណុច ' + M('90^\\circ') + ' ច្រាសទ្រនិចនាឡិកា។)', bloom='Apply'))

    C.append(mcq('medium', 's5_rot', 'ចំណុច ' + M('M(z)') + ' មានរូបភាព ' + M('M\'(z\')') + ' តាមបំប្លែងវិលផ្ចិត ' + M('O') + ' ដែល ' + M('z\'=-iz') + '។ ម៉ុំ ' + M('\\theta') + ' នៃការវិលគឺ ៖',
                 ARGM(Rational(-1, 2)), [ARGM(Rational(1, 2)), ARGM(1), ARGM(Rational(1, 4))],
                 M('-i=\\cos\\left(-\\dfrac\\pi2\\right)+i\\sin\\left(-\\dfrac\\pi2\\right)') + ' ដូច្នេះ ' + M('z\'=(\\cos\\theta+i\\sin\\theta)z') + ' ជាមួយ ' + M('\\theta=-\\dfrac{\\pi}{2}') + ' (វិលតាមទ្រនិចនាឡិកា ' + M('90^\\circ') + ')។', bloom='Understand'))

    C.append(with_img(mcq('medium', 's4_muldiv', 'ក្នុងរូប ' + M('\\arg z_1=\\dfrac\\pi4') + ' និង ' + M('\\arg z_2=\\dfrac\\pi6') + '។ អាគុយម៉ង់នៃផលគុណ ' + M('z_1z_2') + ' គឺ ៖',
                          ARGM(Rational(5, 12)), [ARGM(Rational(1, 12)), ARGM(Rational(1, 24)), ARGM(Rational(5, 6))],
                          M('\\arg(z_1z_2)=\\arg z_1+\\arg z_2=\\dfrac\\pi4+\\dfrac\\pi6=\\dfrac{5\\pi}{12}') + ' (មិនមែនផលដក ឬផលគុណនៃអាគុយម៉ង់ទេ)។', bloom='Analyze'),
                      fig_two_angles()))

    z1, z2 = cz(1, -1), cz(2, 1)
    C.append(mcq('medium', 's1_mod', 'គេឱ្យ ' + M('z_1=1-i') + ' និង ' + M('z_2=2+i') + '។ ម៉ូឌុល ' + M('|z_1z_2|') + ' ស្មើ ៖',
                 M('\\sqrt{10}'), [M('\\sqrt2+\\sqrt5'), M('10'), M('\\sqrt3')],
                 M('|z_1z_2|=|z_1|\\cdot|z_2|=\\sqrt2\\cdot\\sqrt5=\\sqrt{10}') + ' (ផ្ទៀងផ្ទាត់ ៖ ' + M('z_1z_2=3-i') + ' ' + M('|3-i|=\\sqrt{10}') + ')។', bloom='Apply'))

    C.append(mcq('medium', 's1_mod', 'វិសមភាពត្រីកោណ ' + M('|z_1+z_2|\\le|z_1|+|z_2|') + ' ក្លាយជាសមភាព ' + M('|z_1+z_2|=|z_1|+|z_2|') + ' នៅពេលណា ?',
                 'ពេល ' + M('z_1') + ' និង ' + M('z_2') + ' មានអាគុយម៉ង់ដូចគ្នា',
                 ['ពេល ' + M('z_1') + ' និង ' + M('z_2') + ' មានម៉ូឌុលស្មើគ្នា', 'ពេលអាគុយម៉ង់នៃពួកវាខុសគ្នា ' + M('\\dfrac\\pi2'), 'ពេល ' + M('z_1z_2') + ' ជាចំនួនពិត'],
                 'ក្នុងត្រីកោណ ' + M('ON_1N') + ' ' + M('ON=ON_1+N_1N') + ' លុះត្រាតែ ' + M('O,N_1,N') + ' ត្រង់គ្នា ហើយ ' + M('N_1') + ' នៅចន្លោះ ' + M('O') + ' និង ' + M('N') + ' គឺ ' + M('\\overrightarrow{OM_1}') + ' និង ' + M('\\overrightarrow{OM_2}') + ' ទិសដូចគ្នា។ ឧ. ' + M('z_1=1+i,\\ z_2=2+2i') + ' ៖ ' + M('|z_1+z_2|=3\\sqrt2=\\sqrt2+2\\sqrt2') + '។ ម៉ូឌុលស្មើគ្នាមិនគ្រប់គ្រាន់ទេ (ឧ. ' + M('1') + ' និង ' + M('-1') + ')។', bloom='Evaluate'))

    C.append(mcq('medium', 's1_mod', 'គេឱ្យ ' + M('z_1=3-4i') + ' និង ' + M('z_2=-1-i\\sqrt3') + '។ ទំនាក់ទំនងមួយណាត្រឹមត្រូវ ?',
                 M('|z_1+z_2|<|z_1|+|z_2|=7'), [M('|z_1+z_2|=|z_1|+|z_2|=7'), M('|z_1+z_2|>|z_1|+|z_2|'), M('|z_1+z_2|=|z_1|\\cdot|z_2|=10')],
                 M('|z_1|=5,\\ |z_2|=2') + ' ដូច្នេះ ' + M('|z_1|+|z_2|=7') + '។ ' + M('z_1+z_2=2+(-4-\\sqrt3)i') + ' ' + M('|z_1+z_2|=\\sqrt{23+8\\sqrt3}\\approx6{,}07<7') + ' (វិសមភាពត្រីកោណ ' + M('|z_1+z_2|\\le|z_1|+|z_2|') + ' ហើយស្មើគ្នាតែពេលវ៉ិចទ័រទិសដូចគ្នា)។', bloom='Analyze'))

    C.append(mcq('medium', 's2_arg', 'ចំនួនកុំផ្លិច ' + M('z=\\cos a-i\\sin a') + ' មានអាគុយម៉ង់ ៖',
                 M('-a+2k\\pi,\\ k\\in\\mathbb{Z}'), [M('a+2k\\pi,\\ k\\in\\mathbb{Z}'), M('\\pi-a+2k\\pi,\\ k\\in\\mathbb{Z}'), M('a+\\pi+2k\\pi,\\ k\\in\\mathbb{Z}')],
                 M('r=1') + '។ ' + M('\\cos\\varphi=\\cos a=\\cos(-a)') + ' និង ' + M('\\sin\\varphi=-\\sin a=\\sin(-a)') + ' ដូច្នេះ ' + M('\\varphi=-a') + '។', bloom='Apply'))

    z = (3 + 4 * I) / (5 - 12 * I)
    C.append(mcq('medium', 's1_mod', 'គណនាម៉ូឌុលនៃ ' + M('z=\\dfrac{3+4i}{5-12i}') + ' ៖', M('\\dfrac{5}{13}'), [M('\\dfrac{13}{5}'), M('\\dfrac{7}{17}'), M('\\dfrac{1}{3}')],
                 M('|z|=\\dfrac{|3+4i|}{|5-12i|}=\\dfrac{5}{13}') + ' (មិនចាំបាច់បំប្លែង ' + M('z') + ' ជា ' + M('a+bi') + ' ជាមុនទេ)។', bloom='Apply'))

    C.append(mcq('medium', 's2_arg', 'បើ ' + M('\\arg z=\\dfrac{\\pi}{5}') + ' នោះអាគុយម៉ង់ (ក្នុង ' + M('-\\pi<\\varphi\\le\\pi') + ') នៃ ' + M('\\bar z') + ' និង ' + M('-z') + ' រៀងគ្នាគឺ ៖',
                 M('-\\dfrac\\pi5') + ' និង ' + M('-\\dfrac{4\\pi}{5}'),
                 [M('\\dfrac\\pi5') + ' និង ' + M('\\dfrac{6\\pi}{5}'), M('-\\dfrac\\pi5') + ' និង ' + M('\\dfrac{6\\pi}{5}'), M('\\dfrac{4\\pi}{5}') + ' និង ' + M('-\\dfrac\\pi5')],
                 M('\\bar z') + ' ឆ្លុះ ' + M('z') + ' តាមអ័ក្សពិត ដូច្នេះអាគុយម៉ង់ប្ដូរសញ្ញា ' + M('-\\tfrac\\pi5') + '។ ' + M('-z') + ' ឆ្លុះ ' + M('z') + ' តាមគល់ ដូច្នេះអាគុយម៉ង់បូក ' + M('\\pi') + ' បាន ' + M('\\tfrac\\pi5+\\pi=\\tfrac{6\\pi}{5}') + ' ហើយក្នុង ' + M('(-\\pi,\\pi]') + ' គឺ ' + M('\\tfrac{6\\pi}{5}-2\\pi=-\\tfrac{4\\pi}{5}') + '។', bloom='Understand'))

    C.append(mcq('hard', 's3_trig', 'គេឱ្យ ' + M('z=1+\\cos\\varphi-i\\sin\\varphi') + ' ដែល ' + M('-\\pi<\\varphi<\\pi') + '។ ទម្រង់ត្រីកោណមាត្រនៃ ' + M('z') + ' គឺ ៖',
                 M('2\\cos\\dfrac\\varphi2\\left[\\cos\\left(-\\dfrac\\varphi2\\right)+i\\sin\\left(-\\dfrac\\varphi2\\right)\\right]'),
                 [M('2\\cos\\dfrac\\varphi2\\left[\\cos\\dfrac\\varphi2+i\\sin\\dfrac\\varphi2\\right]'), M('2\\left[\\cos\\left(-\\dfrac\\varphi2\\right)+i\\sin\\left(-\\dfrac\\varphi2\\right)\\right]'),
                  M('2\\sin\\dfrac\\varphi2\\left[\\cos\\left(-\\dfrac\\varphi2\\right)+i\\sin\\left(-\\dfrac\\varphi2\\right)\\right]')],
                 M('1+\\cos\\varphi=2\\cos^2\\tfrac\\varphi2') + ' និង ' + M('\\sin\\varphi=2\\sin\\tfrac\\varphi2\\cos\\tfrac\\varphi2') + ' ដូច្នេះ ' + M('z=2\\cos\\tfrac\\varphi2\\left(\\cos\\tfrac\\varphi2-i\\sin\\tfrac\\varphi2\\right)') + '។ ដោយ ' + M('-\\tfrac\\pi2<\\tfrac\\varphi2<\\tfrac\\pi2') + ' នោះ ' + M('\\cos\\tfrac\\varphi2>0') + ' ដូច្នេះ ' + M('2\\cos\\tfrac\\varphi2') + ' ជាម៉ូឌុល។', bloom='Analyze'))

    C.append(mcq('hard', 's2_arg', 'គេឱ្យ ' + M('z_1=z_2=-1+i') + '។ ដោយ ' + M('\\arg z_1=\\arg z_2=\\dfrac{3\\pi}{4}') + ' ហើយ ' + M('z_1z_2=-2i') + ' តើឃ្លាមួយណាត្រឹមត្រូវ ?',
                 'រូបមន្តពិតម៉ូឌុល ' + M('2\\pi') + ' ព្រោះ ' + M('\\dfrac{3\\pi}{2}') + ' និង ' + M('\\arg(-2i)=-\\dfrac\\pi2') + ' ខុសគ្នា ' + M('2\\pi'),
                 ['រូបមន្តពិតតែពេលផលបូកស្ថិតក្នុង ' + M('(-\\pi,\\pi]') + ' ដូច្នេះ ' + M('\\arg(-2i)=\\dfrac{3\\pi}{2}'),
                  'រូបមន្តអាគុយម៉ង់នៃផលគុណមិនពិតសម្រាប់ ' + M('z_1,\\ z_2') + ' នេះទេ',
                  M('\\arg(-2i)=\\dfrac\\pi2') + ' ព្រោះ ' + M('-2i') + ' នៅលើអ័ក្សនិមិត្តវិជ្ជមាន'],
                 M('\\arg(z_1z_2)=\\arg z_1+\\arg z_2+2k\\pi') + ' ពិតជានិច្ច។ នៅទីនេះ ' + M('\\dfrac{3\\pi}{2}-2\\pi=-\\dfrac\\pi2=\\arg(-2i)') + ' ព្រោះ ' + M('-2i') + ' នៅលើអ័ក្សនិមិត្តអវិជ្ជមាន ហើយអាគុយម៉ង់ក្នុង ' + M('(-\\pi,\\pi]') + ' តែងត្រូវកាត់ ' + M('2\\pi') + ' ចេញដើម្បីឱ្យស្ថិតក្នុងចន្លោះ។', bloom='Evaluate'))

    C.append(with_img(mcq('hard', 's2_arg', 'ចំនួនកុំផ្លិច ' + M('z') + ' បំពេញ ' + M('|z-5i|=3') + ' (រង្វង់ក្នុងរូប)។ ចំនួនកុំផ្លិច ' + M('z') + ' ដែលមានអាគុយម៉ង់វិជ្ជមានតូចបំផុតគឺ ៖',
                          Z(cz(Rational(12, 5), Rational(16, 5))), [Z(cz(Rational(16, 5), Rational(12, 5))), Z(cz(3, 4)), Z(cz(Rational(9, 5), Rational(12, 5)))],
                          'អាគុយម៉ង់តូចបំផុតគឺពេល ' + M('OP') + ' ប៉ះរង្វង់។ ' + M('OP=\\sqrt{5^2-3^2}=4') + '។ ក្នុងត្រីកោណកែងពីរ ទាញ ' + M('QM=\\dfrac95') + ' ' + M('MP=\\dfrac{12}{5}') + ' ' + M('OM=5-\\dfrac95=\\dfrac{16}{5}') + ' ដូច្នេះ ' + M('z=\\dfrac{12}{5}+\\dfrac{16}{5}i') + ' (ផ្ទៀងផ្ទាត់ ' + M('|z|=4') + ')។', bloom='Analyze'),
                      fig_tangent()))

    C.append(mcq('hard', 's2_arg', 'អាគុយម៉ង់នៃចំនួនកុំផ្លិច ' + M('z=1+\\cos\\dfrac{\\pi}{7}+i\\sin\\dfrac{\\pi}{7}') + ' គឺ ៖',
                 ARGM(Rational(1, 14)), [ARGM(Rational(1, 7)), ARGM(Rational(1, 28)), ARGM(Rational(2, 7))],
                 M('1+\\cos\\tfrac\\pi7=2\\cos^2\\tfrac{\\pi}{14}') + ' និង ' + M('\\sin\\tfrac\\pi7=2\\sin\\tfrac\\pi{14}\\cos\\tfrac\\pi{14}') + ' ដូច្នេះ ' + M('z=2\\cos\\tfrac\\pi{14}\\left(\\cos\\tfrac\\pi{14}+i\\sin\\tfrac\\pi{14}\\right)') + ' ដែល ' + M('2\\cos\\tfrac\\pi{14}>0') + ' ដូច្នេះអាគុយម៉ង់គឺ ' + M('\\dfrac{\\pi}{14}') + '។', bloom='Analyze'))

    C.append(mcq('hard', 's4_muldiv', 'ដោយគណនា ' + M('(1+i)(1+i\\sqrt3)') + ' តាមពីរវិធី (ទម្រង់ពីជគណិត និងទម្រង់ត្រីកោណមាត្រ) តម្លៃនៃ ' + M('\\cos\\dfrac{7\\pi}{12}') + ' គឺ ៖',
                 M('\\dfrac{\\sqrt2-\\sqrt6}{4}'), [M('\\dfrac{\\sqrt6-\\sqrt2}{4}'), M('\\dfrac{\\sqrt6+\\sqrt2}{4}'), M('\\dfrac{\\sqrt2+\\sqrt6}{4}')],
                 M('(1+i)(1+i\\sqrt3)=(1-\\sqrt3)+(1+\\sqrt3)i') + ' ហើយទម្រង់ត្រីកោណមាត្រ ' + M('=2\\sqrt2\\left(\\cos\\tfrac{7\\pi}{12}+i\\sin\\tfrac{7\\pi}{12}\\right)') + ' (ម៉ូឌុល ' + M('\\sqrt2\\cdot2') + ' អាគុយម៉ង់ ' + M('\\tfrac\\pi4+\\tfrac\\pi3') + ')។ ផ្ទឹមផ្នែកពិត ' + M('\\cos\\tfrac{7\\pi}{12}=\\dfrac{1-\\sqrt3}{2\\sqrt2}=\\dfrac{\\sqrt2-\\sqrt6}{4}') + ' (អវិជ្ជមាន ព្រោះ ' + M('\\tfrac{7\\pi}{12}>\\tfrac\\pi2') + ')។', bloom='Analyze'))

    z = cz(3, 1)
    w = val(2 * I * z)
    C.append(mcq('hard', 's5_rot', 'ត្រូវការបំប្លែងចំណុច ' + M('M(z=3+i)') + ' ទៅចំណុច ' + M('M\'(w)') + ' ដោយវិលជុំវិញ ' + M('O') + ' ម៉ុំ ' + M('\\dfrac\\pi2') + ' រួចពង្រីកចម្ងាយពី ' + M('O') + ' ឱ្យធំជា ' + M('2') + ' ដង។ ចំនួន ' + M('w') + ' ស្មើ ៖',
                 Z(w), [Z(-2 * I * z), Z(2 * z), Z(cz(-1, 3))],
                 'វិលម៉ុំ ' + M('\\tfrac\\pi2') + ' គុណនឹង ' + M('i') + ' ហើយពង្រីក ' + M('2') + ' ដងគុណនឹង ' + M('2') + ' ដូច្នេះ ' + M('w=2i\\cdot z=2i(3+i)=6i-2=-2+6i') + '។ (' + M('-1+3i') + ' ជាករណីវិលតែមួយមិនទាន់ពង្រីក។)', bloom='Create'))

    C.append(mcq('hard', 's4_muldiv', 'សិស្សម្នាក់សរសេរថា ' + M('\\arg\\dfrac{z_1}{z_2}=\\dfrac{\\arg z_1}{\\arg z_2}') + '។ ឃ្លាមួយណាវាយតម្លៃការសរសេរនេះបានត្រឹមត្រូវ ?',
                 'ខុស ព្រោះអាគុយម៉ង់ផលចែកត្រូវ «ដក» ' + M('\\arg z_1-\\arg z_2+2k\\pi'),
                 ['ត្រឹមត្រូវ ព្រោះផលចែកចែកទាំងម៉ូឌុល និងអាគុយម៉ង់', 'ខុស ព្រោះអាគុយម៉ង់ផលចែកត្រូវ «បូក» ' + M('\\arg z_1+\\arg z_2'), 'ត្រឹមត្រូវ តែពេល ' + M('z_2') + ' ជាចំនួនពិត'],
                 M('\\dfrac{z_1}{z_2}=\\dfrac{r_1}{r_2}[\\cos(\\varphi_1-\\varphi_2)+i\\sin(\\varphi_1-\\varphi_2)]') + ' ដូច្នេះអាគុយម៉ង់ត្រូវ «ដក» មិនមែន «ចែក»។ ឧ. ' + M('z_1=i,\\ z_2=1') + ' ៖ ' + M('\\arg\\dfrac{z_1}{z_2}=\\dfrac\\pi2') + ' តែ ' + M('\\dfrac{\\pi/2}{0}') + ' គ្មានន័យ។', bloom='Evaluate'))

    C.append(with_img(mcq('pisa', 'pisa_ship', 'កំពង់ផែ ' + M('P') + ' ស្ថិតនៅគល់ ' + M('O') + ' នៃប្លង់កុំផ្លិច (១ ឯកតា = ១ km)។ កប៉ាល់ ' + M('S') + ' ស្ថិតនៅត្រង់ចំណុចរូបភាពនៃ ' + M('z=3+4i') + ' ដូចក្នុងរូប។ ចម្ងាយពីកំពង់ផែទៅកប៉ាល់ គឺ ៖',
                          M('5\\ \\text{km}'), [M('7\\ \\text{km}'), M('25\\ \\text{km}'), M('\\sqrt7\\ \\text{km}')],
                          'ចម្ងាយ ' + M('PS=|z|=\\sqrt{3^2+4^2}=\\sqrt{25}=5\\ \\text{km}') + '។', bloom='Apply'),
                      fig_ship()))

    C.append(mcq('pisa', 'pisa_phasor', 'វ៉ុលតាពចរន្តឆ្លាស់មួយ ត្រូវបានតាងដោយចំនួនកុំផ្លិច ' + M('V=10\\left(\\cos\\dfrac\\pi6+i\\sin\\dfrac\\pi6\\right)') + ' (គិតជា V) ដែលម៉ូឌុលជាអំព្លីទុត ហើយអាគុយម៉ង់ជាផាស។ សរសេរ ' + M('V') + ' ជាទម្រង់ ' + M('a+bi') + ' ៖',
                 M(fz(cis(10, Rational(1, 6))) + '\\ \\text{V}'),
                 [M(fz(cz(5, 5 * s3)) + '\\ \\text{V}'), M(fz(cz(10 * s3, 10)) + '\\ \\text{V}'), M(fz(cz(5 * s3, -5)) + '\\ \\text{V}')],
                 M('V=10\\left(\\dfrac{\\sqrt3}{2}+\\dfrac12i\\right)=5\\sqrt3+5i\\ \\text{V}') + ' (ផ្នែកពិត ' + M('10\\cos\\tfrac\\pi6') + ' ហើយផ្នែកនិមិត្ត ' + M('10\\sin\\tfrac\\pi6') + ')។', bloom='Apply'))

    E4 = cis(4, Rational(2, 3))
    C.append(with_img(mcq('pisa', 'pisa_arm', 'ដៃមនុស្សយន្តប្រវែង ' + M('4\\ \\text{m}') + ' មានគល់នៅ ' + M('O') + ' ហើយដំបូងស្ថិតតាមអ័ក្សពិត ' + M('(4,\\ 0)') + '។ វាវិលតាមទិសច្រាសទ្រនិចនាឡិកាម៉ុំ ' + M('\\dfrac{2\\pi}{3}') + ' ដូចក្នុងរូប។ ចុង ' + M('E') + ' នៃដៃស្ថិតត្រង់ចំនួនកុំផ្លិច ៖',
                          Z(E4), [Z(cz(2, 2 * s3)), Z(cz(-2, -2 * s3)), Z(cz(-2 * s3, 2))],
                          M('E=4\\left(\\cos\\dfrac{2\\pi}{3}+i\\sin\\dfrac{2\\pi}{3}\\right)=4\\left(-\\dfrac12+\\dfrac{\\sqrt3}{2}i\\right)=-2+2\\sqrt3\\,i') + '។', bloom='Apply'),
                      fig_arm()))

    C.append(mcq('pisa', 'pisa_gear', 'ចំណុចមួយលើកង់ធ្មេញកាំ ' + M('3\\ \\text{m}') + ' មានទីតាំងដំបូង ' + M('z_0=3\\left(\\cos\\dfrac\\pi4+i\\sin\\dfrac\\pi4\\right)') + '។ កង់វិលតាមទិសច្រាសទ្រនិចនាឡិកាម៉ុំសរុប ' + M('\\dfrac{3\\pi}{4}') + '។ ទីតាំងថ្មីនៃចំណុចនោះគឺ ៖',
                 Z(cz(-3)), [Z(cz(3)), Z(cz(0, 3)), Z(cz(0, -3))],
                 'ទីតាំងថ្មី ' + M('z=\\left(\\cos\\tfrac{3\\pi}4+i\\sin\\tfrac{3\\pi}4\\right)z_0=3\\left[\\cos\\left(\\tfrac\\pi4+\\tfrac{3\\pi}{4}\\right)+i\\sin(\\ldots)\\right]=3(\\cos\\pi+i\\sin\\pi)=-3').replace('\\sin(\\ldots)', '\\sin\\pi') + '។', bloom='Apply'))

    C.append(with_img(mcq('pisa', 'pisa_wind', 'ចុងស្លឹកកង្ហារខ្យល់ចាប់ផ្ដើមនៅ ' + M('T_0=5') + ' (ម៉ែត្រ) ហើយវិលច្រាសទ្រនិចនាឡិការៀងរាល់វិនាទីបានម៉ុំ ' + M('\\dfrac\\pi6') + ' ជុំវិញ ' + M('O') + ' ដូចក្នុងរូប (វិនាទីទី ១)។ ក្រោយប៉ុន្មានវិនាទី ទើបចុងស្លឹកមកដល់ចំណុច ' + M('5i') + ' លើអ័ក្សនិមិត្តជាលើកដំបូង ?',
                          '3 វិនាទី', ['2 វិនាទី', '4 វិនាទី', '6 វិនាទី'],
                          'ក្រោយ ' + M('t') + ' វិនាទី ទីតាំងគឺ ' + M('5\\left(\\cos\\tfrac{t\\pi}{6}+i\\sin\\tfrac{t\\pi}{6}\\right)') + '។ ត្រូវការ ' + M('\\tfrac{t\\pi}{6}=\\tfrac\\pi2') + ' ដូច្នេះ ' + M('t=3') + ' ហើយទីតាំង ' + M('=5i') + '។', bloom='Analyze'),
                      fig_windmill()))

    # =============================================================================== WRITING EASY (1)
    C.append(wr('easy', 's3_trig', 'សរសេរចំនួនកុំផ្លិច ' + M('z=1+i\\sqrt3') + ' ជាទម្រង់ត្រីកោណមាត្រ រួចផ្ទៀងផ្ទាត់ចម្លើយ។',
                [('គណនាម៉ូឌុល ៖ ' + M('r=\\sqrt{1^2+(\\sqrt3)^2}=2'), 1),
                 ('រកអាគុយម៉ង់ ៖ ' + M('\\cos\\varphi=\\dfrac12') + ' និង ' + M('\\sin\\varphi=\\dfrac{\\sqrt3}{2}'), 1),
                 ('ដូច្នេះ ' + M('\\varphi=\\dfrac\\pi3') + ' (កាដ្រង់ទី ១)', 1),
                 ('ទម្រង់ត្រីកោណមាត្រ ៖ ' + M('z=2\\left(\\cos\\dfrac\\pi3+i\\sin\\dfrac\\pi3\\right)'), 1),
                 ('ផ្ទៀងផ្ទាត់ ៖ ' + M('2\\left(\\dfrac12+\\dfrac{\\sqrt3}{2}i\\right)=1+i\\sqrt3') + ' ត្រឹមត្រូវ។', 1)], bloom='Apply'))

    # =============================================================================== WRITING MEDIUM (4)
    C.append(wr('medium', 's4_muldiv', 'គេឱ្យ ' + M('z_1=1+i') + ' និង ' + M('z_2=1+i\\sqrt3') + '។ ក. សរសេរ ' + M('z_1') + ' និង ' + M('z_2') + ' ជាទម្រង់ត្រីកោណមាត្រ រួចគណនា ' + M('z_1z_2') + ' ជាទម្រង់ត្រីកោណមាត្រ។ ខ. គណនា ' + M('z_1z_2') + ' ជាទម្រង់ពីជគណិត រួចទាញរក ' + M('\\cos\\dfrac{7\\pi}{12}') + ' និង ' + M('\\sin\\dfrac{7\\pi}{12}') + '។',
                [('ទម្រង់ត្រីកោណមាត្រ ៖ ' + M('z_1=\\sqrt2\\left(\\cos\\tfrac\\pi4+i\\sin\\tfrac\\pi4\\right)') + ' និង ' + M('z_2=2\\left(\\cos\\tfrac\\pi3+i\\sin\\tfrac\\pi3\\right)'), 1),
                 ('ផលគុណ ៖ ' + M('z_1z_2=2\\sqrt2\\left[\\cos\\left(\\tfrac\\pi4+\\tfrac\\pi3\\right)+i\\sin\\left(\\tfrac\\pi4+\\tfrac\\pi3\\right)\\right]=2\\sqrt2\\left(\\cos\\tfrac{7\\pi}{12}+i\\sin\\tfrac{7\\pi}{12}\\right)'), 1),
                 ('ទម្រង់ពីជគណិត ៖ ' + M('z_1z_2=(1+i)(1+i\\sqrt3)=1+i\\sqrt3+i-\\sqrt3=(1-\\sqrt3)+(1+\\sqrt3)i'), 1),
                 ('ផ្ទឹមផ្នែកពិត ៖ ' + M('2\\sqrt2\\cos\\tfrac{7\\pi}{12}=1-\\sqrt3') + ' ដូច្នេះ ' + M('\\cos\\tfrac{7\\pi}{12}=\\dfrac{1-\\sqrt3}{2\\sqrt2}=\\dfrac{\\sqrt2-\\sqrt6}{4}'), 1),
                 ('ផ្ទឹមផ្នែកនិមិត្ត ៖ ' + M('\\sin\\tfrac{7\\pi}{12}=\\dfrac{1+\\sqrt3}{2\\sqrt2}=\\dfrac{\\sqrt2+\\sqrt6}{4}'), 1)], bloom='Apply'))

    C.append(wr('medium', 's4_muldiv', 'គេឱ្យ ' + M('z_1=-1+i\\sqrt3') + ' និង ' + M('z_2=1+i') + '។ ក. គណនា ' + M('\\dfrac{z_1}{z_2}') + ' ជាទម្រង់ត្រីកោណមាត្រ។ ខ. គណនា ' + M('\\dfrac{z_1}{z_2}') + ' ជាទម្រង់ពីជគណិត រួចទាញរក ' + M('\\cos\\dfrac{5\\pi}{12}') + ' និង ' + M('\\sin\\dfrac{5\\pi}{12}') + '។',
                [('ទម្រង់ត្រីកោណមាត្រ ៖ ' + M('z_1=2\\left(\\cos\\tfrac{2\\pi}3+i\\sin\\tfrac{2\\pi}3\\right)') + ' និង ' + M('z_2=\\sqrt2\\left(\\cos\\tfrac\\pi4+i\\sin\\tfrac\\pi4\\right)'), 1),
                 ('ផលចែក ៖ ' + M('\\dfrac{z_1}{z_2}=\\dfrac{2}{\\sqrt2}\\left[\\cos\\left(\\tfrac{2\\pi}3-\\tfrac\\pi4\\right)+i\\sin(\\cdot)\\right]=\\sqrt2\\left(\\cos\\tfrac{5\\pi}{12}+i\\sin\\tfrac{5\\pi}{12}\\right)').replace('\\sin(\\cdot)', '\\sin\\left(\\tfrac{2\\pi}3-\\tfrac\\pi4\\right)'), 1),
                 ('ទម្រង់ពីជគណិត ៖ ' + M('\\dfrac{-1+i\\sqrt3}{1+i}=\\dfrac{(-1+i\\sqrt3)(1-i)}{2}=\\dfrac{(\\sqrt3-1)+(\\sqrt3+1)i}{2}'), 1),
                 ('ផ្ទឹមផ្នែកពិត ៖ ' + M('\\sqrt2\\cos\\tfrac{5\\pi}{12}=\\dfrac{\\sqrt3-1}{2}') + ' ដូច្នេះ ' + M('\\cos\\tfrac{5\\pi}{12}=\\dfrac{\\sqrt6-\\sqrt2}{4}'), 1),
                 ('ផ្ទឹមផ្នែកនិមិត្ត ៖ ' + M('\\sin\\tfrac{5\\pi}{12}=\\dfrac{\\sqrt3+1}{2\\sqrt2}=\\dfrac{\\sqrt6+\\sqrt2}{4}'), 1)], bloom='Apply'))

    z = cz(4, -2)
    zp = val((cos(-7 * pi / 6) + I * sin(-7 * pi / 6)) * z)
    C.append(wr('medium', 's5_rot', 'ចំណុច ' + M('M(z)') + ' ដែល ' + M('z=4-2i') + ' វិលជុំវិញគល់ ' + M('O') + ' ម៉ុំ ' + M('-\\dfrac{7\\pi}{6}') + ' ទៅចំណុច ' + M('M\'(z\')') + '។ កំណត់ ' + M('z\'') + ' ជាទម្រង់ ' + M('a+bi') + '។',
                [('រូបមន្តបំប្លែងវិល ៖ ' + M('z\'=(\\cos\\alpha+i\\sin\\alpha)z') + ' ដែល ' + M('\\alpha=-\\tfrac{7\\pi}{6}'), 1),
                 ('គណនា ' + M('\\cos\\left(-\\tfrac{7\\pi}{6}\\right)=-\\dfrac{\\sqrt3}{2}') + ' និង ' + M('\\sin\\left(-\\tfrac{7\\pi}{6}\\right)=\\dfrac12'), 1),
                 ('ជំនួស ៖ ' + M('z\'=\\left(-\\dfrac{\\sqrt3}{2}+\\dfrac12i\\right)(4-2i)'), 1),
                 ('ពន្លាត ៖ ' + M('=-2\\sqrt3+\\sqrt3\\,i+2i-i^2'), 1),
                 ('ជំនួស ' + M('i^2=-1') + ' ៖ ' + M('z\'=%s' % fz(zp)), 1)], bloom='Apply'))

    C.append(with_img(wr('medium', 's1_mod', 'គេឱ្យ ' + M('z_1=-1+2i') + ' និង ' + M('z_2=1+i') + ' ដែលមានរូបភាព ' + M('N_1') + ' និង ' + M('N_2') + ' ដូចក្នុងរូប ហើយ ' + M('N') + ' ជារូបភាពនៃ ' + M('z_1+z_2') + '។ ក. គណនា ' + M('|z_1|,\\ |z_2|') + ' និង ' + M('|z_1+z_2|') + '។ ខ. ផ្ទៀងផ្ទាត់ ' + M('|z_1+z_2|\\le|z_1|+|z_2|') + '។ គ. ពន្យល់តាមធរណីមាត្រក្នុងត្រីកោណ ' + M('ON_1N') + '។',
                         [('ម៉ូឌុល ៖ ' + M('|z_1|=\\sqrt{1+4}=\\sqrt5') + ' និង ' + M('|z_2|=\\sqrt{1+1}=\\sqrt2'), 1),
                          ('ផលបូក ៖ ' + M('z_1+z_2=0+3i=3i') + ' ដូច្នេះ ' + M('|z_1+z_2|=3'), 1),
                          ('ប្រៀបធៀប ៖ ' + M('|z_1|+|z_2|=\\sqrt5+\\sqrt2\\approx3{,}65') + ' ហើយ ' + M('3<3{,}65'), 1),
                          ('ដូច្នេះ ' + M('|z_1+z_2|\\le|z_1|+|z_2|') + ' ត្រឹមត្រូវ', 1),
                          ('ធរណីមាត្រ ៖ ' + M('ON=|z_1+z_2|') + ' ' + M('ON_1=|z_1|') + ' ' + M('N_1N=ON_2=|z_2|') + ' ។ ក្នុងត្រីកោណ ' + M('ON_1N') + ' ជ្រុង ' + M('ON') + ' តូចជាងឬស្មើផលបូកជ្រុងពីរផ្សេងទៀត (វិសមភាពត្រីកោណ)', 1)], bloom='Analyze'),
                     fig_ineq()))

    # =============================================================================== WRITING HARD (4)
    C.append(wr('hard', 's3_trig', 'គេឱ្យ ' + M('z=1+\\cos\\varphi-i\\sin\\varphi') + ' ដែល ' + M('-\\pi<\\varphi<\\pi') + '។ ក. សរសេរ ' + M('z') + ' ជាទម្រង់ត្រីកោណមាត្រ។ ខ. បញ្ជាក់ម៉ូឌុល និងអាគុយម៉ង់នៃ ' + M('z') + ' ហើយពន្យល់ហេតុអ្វីតម្លៃ ' + M('2\\cos\\tfrac\\varphi2') + ' ជាម៉ូឌុលត្រឹមត្រូវ។ គ. ផ្ទៀងផ្ទាត់ជាមួយ ' + M('\\varphi=\\dfrac\\pi2') + '។',
                [('រូបមន្តកន្លះមុំ ៖ ' + M('1+\\cos\\varphi=2\\cos^2\\tfrac\\varphi2') + ' និង ' + M('\\sin\\varphi=2\\sin\\tfrac\\varphi2\\cos\\tfrac\\varphi2'), 1),
                 ('ដាក់កត្តាខាងក្រៅ ៖ ' + M('z=2\\cos\\tfrac\\varphi2\\left(\\cos\\tfrac\\varphi2-i\\sin\\tfrac\\varphi2\\right)'), 1),
                 ('ទម្រង់ត្រីកោណមាត្រ ៖ ' + M('z=2\\cos\\tfrac\\varphi2\\left[\\cos\\left(-\\tfrac\\varphi2\\right)+i\\sin\\left(-\\tfrac\\varphi2\\right)\\right]'), 1),
                 ('ដោយ ' + M('-\\pi<\\varphi<\\pi') + ' នោះ ' + M('-\\tfrac\\pi2<\\tfrac\\varphi2<\\tfrac\\pi2') + ' ហើយ ' + M('\\cos\\tfrac\\varphi2>0') + ' ដូច្នេះ ' + M('r=2\\cos\\tfrac\\varphi2>0') + ' ជាម៉ូឌុលត្រឹមត្រូវ ហើយអាគុយម៉ង់គឺ ' + M('-\\tfrac\\varphi2'), 1),
                 ('ផ្ទៀងផ្ទាត់ ៖ ' + M('\\varphi=\\tfrac\\pi2') + ' ឱ្យ ' + M('z=1+0-i=1-i=\\sqrt2\\left[\\cos\\left(-\\tfrac\\pi4\\right)+i\\sin\\left(-\\tfrac\\pi4\\right)\\right]') + ' ស្របនឹងរូបមន្ត ' + M('2\\cos\\tfrac\\pi4=\\sqrt2') + ' និងអាគុយម៉ង់ ' + M('-\\tfrac\\pi4') + '។', 1)], bloom='Evaluate'))

    C.append(with_img(wr('hard', 's2_arg', 'ចំនួនកុំផ្លិច ' + M('z') + ' បំពេញលក្ខខណ្ឌ ' + M('|z-5i|=3') + '។ រកចំនួនកុំផ្លិច ' + M('z') + ' ដែលមានអាគុយម៉ង់វិជ្ជមានតូចបំផុត ដូចក្នុងរូប (ដែល ' + M('Q') + ' ជាផ្ចិតរង្វង់ ' + M('P') + ' ជាចំណុចប៉ះ)។',
                         [('សមីការ ៖ ' + M('|x+(y-5)i|=3') + ' ឱ្យ ' + M('x^2+(y-5)^2=9') + ' ជារង្វង់ផ្ចិត ' + M('Q(0,5)') + ' កាំ ' + M('3'), 1),
                          ('អាគុយម៉ង់តូចបំផុតពេល ' + M('OP') + ' ប៉ះរង្វង់ ដូច្នេះ ' + M('QP\\perp OP') + ' ហើយ ' + M('OP^2=OQ^2-QP^2=25-9=16') + ' គឺ ' + M('OP=4'), 1),
                          ('តាង ' + M('M') + ' ជាចំណោលកែងនៃ ' + M('P') + ' លើអ័ក្សនិមិត្ត។ ក្នុងត្រីកោណ ' + M('MPQ') + ' ' + M('MP^2=9-QM^2') + ' ហើយក្នុង ' + M('MPO') + ' ' + M('MP^2=16-MO^2') + ' ជាមួយ ' + M('MO=5-QM'), 1),
                          ('ដោះស្រាយ ៖ ' + M('9-QM^2=16-(5-QM)^2') + ' ឱ្យ ' + M('10QM=18') + ' ដូច្នេះ ' + M('QM=\\dfrac95') + ' ហើយ ' + M('MP=\\sqrt{9-\\dfrac{81}{25}}=\\dfrac{12}{5}') + ' ព្រមទាំង ' + M('OM=5-\\dfrac95=\\dfrac{16}{5}'), 1),
                          ('ដូច្នេះ ' + M('P\\left(\\dfrac{12}{5},\\ \\dfrac{16}{5}\\right)') + ' គឺ ' + M('z=\\dfrac{12}{5}+\\dfrac{16}{5}i') + ' (ផ្ទៀងផ្ទាត់ ៖ ' + M('|z|=\\sqrt{\\tfrac{144+256}{25}}=4') + ')។', 1)], bloom='Analyze'),
                     fig_tangent()))

    C.append(with_img(wr('hard', 's5_rot', 'ការ៉េ ' + M('ABCD') + ' មានផ្ចិតត្រូវនឹងគល់ ' + M('O') + ' ហើយកំពូល ' + M('A') + ' ជារូបភាពនៃ ' + M('z_A=3+i') + ' ដូចក្នុងរូប។ ដោយប្រើបំប្លែងវិលផ្ចិត ' + M('O') + ' ម៉ុំ ' + M('\\dfrac\\pi2') + ' រកចំនួនកុំផ្លិចនៃកំពូល ' + M('B,\\ C,\\ D') + ' (តាមលំដាប់ច្រាសទ្រនិចនាឡិកា) រួចផ្ទៀងផ្ទាត់ថាវាជាការ៉េ។',
                         [('កំពូលបន្ទាប់គឺរូបភាពនៃកំពូលមុនតាមបំប្លែងវិលម៉ុំ ' + M('\\tfrac\\pi2') + ' ដូច្នេះគុណនឹង ' + M('i') + ' ព្រោះ ' + M('\\cos\\tfrac\\pi2+i\\sin\\tfrac\\pi2=i'), 1),
                          (M('z_B=i\\,z_A=i(3+i)=-1+3i'), 1),
                          (M('z_C=i\\,z_B=-3-i=-z_A') + ' (វិលម៉ុំ ' + M('\\pi') + ' ពី ' + M('A') + ')', 1),
                          (M('z_D=i\\,z_C=1-3i'), 1),
                          ('ផ្ទៀងផ្ទាត់ ៖ ម៉ូឌុលទាំងបួនស្មើ ' + M('\\sqrt{10}') + ' ហើយ ' + M('\\dfrac{z_B}{z_A}=i') + ' (កែងគ្នា) ដូច្នេះ ' + M('OA=OB=OC=OD') + ' និងអង្កត់ទ្រូង ' + M('AC\\perp BD') + ' កាត់គ្នាត្រង់ចំណុចកណ្ដាល ' + M('O') + ' គឺជាការ៉េ។', 1)], bloom='Create'),
                     fig_square()))

    C.append(wr('hard', 's3_trig', 'ពិនិត្យឃ្លា «ចំនួន ' + M('-2\\left(\\cos\\dfrac\\pi3+i\\sin\\dfrac\\pi3\\right)') + ' ជាទម្រង់ត្រីកោណមាត្រ»។ ក. បង្ហាញថាឃ្លានេះខុស។ ខ. សរសេរចំនួននេះជាទម្រង់ត្រីកោណមាត្រត្រឹមត្រូវ។ គ. ផ្ទៀងផ្ទាត់ជាទម្រង់ពីជគណិត។',
                [('ទម្រង់ត្រីកោណមាត្រទាមទារម៉ូឌុល ' + M('r>0') + ' តែនៅទីនេះមេគុណ ' + M('-2<0') + ' ដូច្នេះមិនមែនទម្រង់ត្រីកោណមាត្រទេ', 1),
                 ('ប្រើ ' + M('-1=\\cos\\pi+i\\sin\\pi') + ' ៖ ' + M('-2\\,\\text{cis}\\tfrac\\pi3=2\\,\\text{cis}\\,\\pi\\cdot\\text{cis}\\tfrac\\pi3') + ' ដោយ ' + M('\\text{cis}\\,\\theta=\\cos\\theta+i\\sin\\theta'), 1),
                 ('បូកអាគុយម៉ង់ ៖ ' + M('\\pi+\\tfrac\\pi3=\\tfrac{4\\pi}{3}') + ' ដូច្នេះ ' + M('2\\left(\\cos\\tfrac{4\\pi}{3}+i\\sin\\tfrac{4\\pi}{3}\\right)') + ' (ឬ ' + M('2\\left[\\cos\\left(-\\tfrac{2\\pi}{3}\\right)+i\\sin\\left(-\\tfrac{2\\pi}{3}\\right)\\right]') + ')', 1),
                 ('ពិនិត្យទម្រង់ដើម ៖ ' + M('-2\\left(\\dfrac12+\\dfrac{\\sqrt3}{2}i\\right)=-1-\\sqrt3\\,i'), 1),
                 ('ពិនិត្យទម្រង់ថ្មី ៖ ' + M('2\\left(-\\dfrac12-\\dfrac{\\sqrt3}{2}i\\right)=-1-\\sqrt3\\,i') + ' ដូចគ្នា ដូច្នេះត្រឹមត្រូវ។', 1)], bloom='Evaluate'))

    # =============================================================================== WRITING PISA (5)
    C.append(wr('pisa', 'pisa_series', 'វ៉ុលតាពពីរក្នុងសៀគ្វីចរន្តឆ្លាស់ ត្រូវបានតាងដោយចំនួនកុំផ្លិច (ម៉ូឌុលជាអំព្លីទុត អាគុយម៉ង់ជាផាស) ៖ ' + M('V_1=4(\\cos0+i\\sin0)\\ \\text{V}') + ' និង ' + M('V_2=3\\left(\\cos\\dfrac\\pi2+i\\sin\\dfrac\\pi2\\right)\\ \\text{V}') + '។ ក. សរសេរ ' + M('V_1,\\ V_2') + ' ជាទម្រង់ ' + M('a+bi') + '។ ខ. គណនាវ៉ុលតាពសរុប ' + M('V=V_1+V_2') + ' និងអំព្លីទុតរបស់វា។ គ. រកអាគុយម៉ង់ ' + M('\\varphi') + ' នៃ ' + M('V') + ' (បង្ហាញ ' + M('\\tan\\varphi') + ')។',
                [('ទម្រង់ពីជគណិត ៖ ' + M('V_1=4') + ' និង ' + M('V_2=3i'), 1),
                 ('វ៉ុលតាពសរុប ៖ ' + M('V=V_1+V_2=4+3i\\ \\text{V}'), 1),
                 ('អំព្លីទុត ៖ ' + M('|V|=\\sqrt{4^2+3^2}=5\\ \\text{V}') + ' (មិនមែន ' + M('4+3=7') + ' ទេ)', 1),
                 ('អាគុយម៉ង់ ៖ ' + M('\\cos\\varphi=\\dfrac45') + ' និង ' + M('\\sin\\varphi=\\dfrac35') + ' ដូច្នេះ ' + M('\\tan\\varphi=\\dfrac34') + ' ហើយ ' + M('\\varphi\\approx36{,}9^\\circ') + ' (កាដ្រង់ទី ១)', 1),
                 ('សន្និដ្ឋាន ៖ ' + M('V=5\\left(\\cos\\varphi+i\\sin\\varphi\\right)\\ \\text{V}') + ' ដែលអំព្លីទុតតូចជាងផលបូក ' + M('7') + ' ព្រោះសញ្ញាទាំងពីរមានផាសខុសគ្នា ' + M('90^\\circ') + '។', 1)], bloom='Apply'))

    wt = [cis(8, Rational(2 * k, 3)) for k in range(3)]
    C.append(with_img(wr('pisa', 'pisa_turbine', 'ស្លឹកទាំងបីនៃកង្ហារខ្យល់ប្រវែង ' + M('8\\ \\text{m}') + ' ស្ថិតដាច់ពីគ្នា ' + M('120^\\circ') + ' ចុងស្លឹកទី ១ នៅត្រង់ ' + M('w_0=8') + '។ ក. រក ' + M('w_1') + ' និង ' + M('w_2') + ' (ចុងស្លឹកទី ២ និងទី ៣) ដោយប្រើបំប្លែងវិលម៉ុំ ' + M('\\dfrac{2\\pi}{3}') + '។ ខ. បង្ហាញថាចុងស្លឹកទាំងបីជាកំពូលនៃត្រីកោណសមមាត្រ ហើយរកប្រវែងជ្រុង។',
                         [('បំប្លែងវិលម៉ុំ ' + M('\\tfrac{2\\pi}3') + ' ៖ ' + M('w_1=\\left(\\cos\\tfrac{2\\pi}3+i\\sin\\tfrac{2\\pi}3\\right)\\cdot8=-4+4\\sqrt3\\,i'), 1),
                          (M('w_2=\\left(\\cos\\tfrac{2\\pi}3+i\\sin\\tfrac{2\\pi}3\\right)w_1=8\\left(\\cos\\tfrac{4\\pi}3+i\\sin\\tfrac{4\\pi}3\\right)=-4-4\\sqrt3\\,i'), 1),
                          (M('w_1-w_0=-12+4\\sqrt3\\,i') + ' ដូច្នេះ ' + M('|w_1-w_0|=\\sqrt{144+48}=\\sqrt{192}=8\\sqrt3'), 1),
                          (M('w_2-w_1=-8\\sqrt3\\,i') + ' ដូច្នេះ ' + M('|w_2-w_1|=8\\sqrt3'), 1),
                          (M('w_0-w_2=12+4\\sqrt3\\,i') + ' ដូច្នេះ ' + M('|w_0-w_2|=8\\sqrt3') + ' ។ ជ្រុងទាំងបីស្មើគ្នា គឺត្រីកោណសមមាត្រ ប្រវែងជ្រុង ' + M('8\\sqrt3\\approx13{,}9\\ \\text{m}') + '។', 1)], bloom='Create'),
                     fig_turbine()))

    P2 = cis(3, Rational(1, 6))
    E2 = val(P2 + 2 * I)
    C.append(with_img(wr('pisa', 'pisa_arm2', 'ដៃម៉ាស៊ីនមានពីរកំណាត់ ៖ កំណាត់ទី ១ ប្រវែង ' + M('3\\ \\text{m}') + ' ចេញពីគល់ ' + M('O') + ' ទៅ ' + M('P') + ' តាមទិសមានអាគុយម៉ង់ ' + M('\\dfrac\\pi6') + ' ហើយកំណាត់ទី ២ ប្រវែង ' + M('2\\ \\text{m}') + ' ចេញពី ' + M('P') + ' ទៅ ' + M('E') + ' តាមទិសមានអាគុយម៉ង់ ' + M('\\dfrac\\pi6+\\dfrac\\pi3') + ' ដូចក្នុងរូប។ ក. រកចំនួនកុំផ្លិចនៃ ' + M('P') + ' និង ' + M('E') + '។ ខ. គណនាចម្ងាយ ' + M('OE') + '។',
                         [('ចំណុច ' + M('P') + ' ៖ ' + M('z_P=3\\left(\\cos\\tfrac\\pi6+i\\sin\\tfrac\\pi6\\right)=\\dfrac{3\\sqrt3}{2}+\\dfrac32i'), 1),
                          ('ទិសកំណាត់ទី ២ មានអាគុយម៉ង់ ' + M('\\tfrac\\pi6+\\tfrac\\pi3=\\tfrac\\pi2') + ' ដូច្នេះវ៉ិចទ័រ ' + M('\\overrightarrow{PE}') + ' ត្រូវនឹង ' + M('2\\left(\\cos\\tfrac\\pi2+i\\sin\\tfrac\\pi2\\right)=2i'), 1),
                          ('ចំណុច ' + M('E') + ' ៖ ' + M('z_E=z_P+2i'), 1),
                          ('គណនា ៖ ' + M('z_E=\\dfrac{3\\sqrt3}{2}+\\left(\\dfrac32+2\\right)i=\\dfrac{3\\sqrt3}{2}+\\dfrac72i'), 1),
                          ('ចម្ងាយ ៖ ' + M('OE=|z_E|=\\sqrt{\\dfrac{27}{4}+\\dfrac{49}{4}}=\\sqrt{19}\\approx4{,}36\\ \\text{m}') + '។', 1)], bloom='Apply'),
                     fig_arm2()))

    C.append(wr('pisa', 'pisa_drone', 'ដ្រូនមួយហោះជារង្វង់ជុំវិញប៉មដែលស្ថិតនៅគល់ ' + M('O') + ' ក្នុងរង្វង់កាំ ' + M('50\\ \\text{m}') + '។ វាចាប់ផ្ដើមពី ' + M('z(0)=50') + ' ហើយរៀងរាល់វិនាទីវិលច្រាសទ្រនិចនាឡិកាបានម៉ុំ ' + M('\\dfrac{\\pi}{12}') + '។ ក. សរសេរទីតាំង ' + M('z(t)') + ' រួចរក ' + M('z(8)') + '។ ខ. ក្រោយប៉ុន្មានវិនាទី ទើបដ្រូនឆ្លងកាត់ចំណុច ' + M('50i') + ' ជាលើកដំបូង ? គ. គណនាចម្ងាយរវាងទីតាំងនៅ ' + M('t=0') + ' និង ' + M('t=8') + '។',
                [('ទីតាំងនៅវិនាទី ' + M('t') + ' ៖ ' + M('z(t)=50\\left(\\cos\\tfrac{t\\pi}{12}+i\\sin\\tfrac{t\\pi}{12}\\right)'), 1),
                 (M('t=8') + ' ៖ ម៉ុំ ' + M('\\tfrac{8\\pi}{12}=\\tfrac{2\\pi}3') + ' ដូច្នេះ ' + M('z(8)=50\\left(-\\tfrac12+\\tfrac{\\sqrt3}2i\\right)=-25+25\\sqrt3\\,i'), 1),
                 ('ត្រូវការ ' + M('\\tfrac{t\\pi}{12}=\\tfrac\\pi2') + ' ដូច្នេះ ' + M('t=6') + ' វិនាទី (ដ្រូនឆ្លងកាត់ ' + M('50i') + ')', 1),
                 ('វ៉ិចទ័រពីទីតាំងដើមទៅទីតាំងនៅ ' + M('t=8') + ' ៖ ' + M('z(8)-z(0)=-25+25\\sqrt3\\,i-50=-75+25\\sqrt3\\,i'), 1),
                 ('ចម្ងាយ ៖ ' + M('|z(8)-z(0)|=\\sqrt{5625+1875}=\\sqrt{7500}=50\\sqrt3\\approx86{,}6\\ \\text{m}') + '។', 1)], bloom='Analyze'))

    C.append(wr('pisa', 'pisa_signal', 'សៀគ្វីពីរដំណាក់កាលមានមេគុណបញ្ជូន ' + M('H_1=2\\left(\\cos\\dfrac\\pi4+i\\sin\\dfrac\\pi4\\right)') + ' និង ' + M('H_2=\\dfrac12\\left(\\cos\\dfrac\\pi6+i\\sin\\dfrac\\pi6\\right)') + '។ មេគុណសរុបគឺ ' + M('H=H_1H_2') + '។ ក. គណនា ' + M('H') + ' ជាទម្រង់ត្រីកោណមាត្រ ហើយបញ្ជាក់អំព្លីទុត និងផាស។ ខ. គណនា ' + M('H') + ' ម្ដងទៀតជាទម្រង់ពីជគណិត រួចទាញរក ' + M('\\cos\\dfrac{5\\pi}{12}') + ' និង ' + M('\\sin\\dfrac{5\\pi}{12}') + '។',
                [('ផលគុណ ៖ ' + M('H=2\\times\\tfrac12\\left[\\cos\\left(\\tfrac\\pi4+\\tfrac\\pi6\\right)+i\\sin\\left(\\tfrac\\pi4+\\tfrac\\pi6\\right)\\right]'), 1),
                 ('ដូច្នេះ ' + M('H=\\cos\\tfrac{5\\pi}{12}+i\\sin\\tfrac{5\\pi}{12}') + ' អំព្លីទុត ' + M('|H|=1') + ' និងផាស ' + M('\\tfrac{5\\pi}{12}=75^\\circ'), 1),
                 ('ទម្រង់ពីជគណិត ៖ ' + M('H_1=\\sqrt2+\\sqrt2\\,i') + ' និង ' + M('H_2=\\dfrac{\\sqrt3}{4}+\\dfrac14i'), 1),
                 ('គុណ ៖ ' + M('H=(\\sqrt2+\\sqrt2\\,i)\\left(\\dfrac{\\sqrt3}{4}+\\dfrac14i\\right)=\\dfrac{\\sqrt6-\\sqrt2}{4}+\\dfrac{\\sqrt6+\\sqrt2}{4}i'), 1),
                 ('ផ្ទឹមនឹង ក. ៖ ' + M('\\cos\\tfrac{5\\pi}{12}=\\dfrac{\\sqrt6-\\sqrt2}{4}') + ' និង ' + M('\\sin\\tfrac{5\\pi}{12}=\\dfrac{\\sqrt6+\\sqrt2}{4}') + '។', 1)], bloom='Analyze'))

    return C


def verify():
    """independent re-derivation of the claims above (a second implementation, sympy + numerics)."""
    import math, cmath
    n = 0
    z = lambda a, b: complex(a, b)
    def close(x, y, e=1e-9): return abs(x - y) < e
    # arguments / trig forms
    for (a, b, r, p) in [(1, math.sqrt(3), 2, 1/3), (-1, math.sqrt(3), 2, 2/3), (0, -1, 1, -1/2), (-4, 4, 4*math.sqrt(2), 3/4), (2*math.sqrt(3), -2, 4, -1/6)]:
        w = z(a, b); assert close(abs(w), r) and close(cmath.phase(w), p*math.pi), (a, b); n += 1
    # products / quotients
    assert close(2*cmath.exp(1j*math.pi/4) * 3*cmath.exp(1j*math.pi/6), 6*cmath.exp(1j*5*math.pi/12)); n += 1
    assert close(6*cmath.exp(1j*5*math.pi/12) / (2*cmath.exp(1j*math.pi/12)), 3*cmath.exp(1j*math.pi/3)); n += 1
    assert close(abs(z(1, -1)*z(2, 1)), math.sqrt(10)) and close(abs(z(3, 1)/z(1, -1)), math.sqrt(5)); n += 2
    assert close(abs(z(3, 4)/z(5, -12)), 5/13) and close(abs(z(2, 1)*z(1, -3)), 5*math.sqrt(2)); n += 2
    # triangle inequality example (MCQ) and writing
    z1, z2 = z(3, -4), z(-1, -math.sqrt(3))
    assert abs(z1 + z2) < abs(z1) + abs(z2) and close(abs(z1)+abs(z2), 7) and close(abs(z1+z2), math.sqrt(23 + 8*math.sqrt(3))); n += 2
    assert abs(z(-1, 2) + z(1, 1)) == 3 and abs(z(-1, 2)) + abs(z(1, 1)) > 3; n += 1
    # cos 7pi/12, sin 7pi/12 and 5pi/12
    p = z(1, 1) * z(1, math.sqrt(3))
    assert close(p.real, 2*math.sqrt(2)*math.cos(7*math.pi/12)) and close(math.cos(7*math.pi/12), (math.sqrt(2)-math.sqrt(6))/4) and close(math.sin(7*math.pi/12), (math.sqrt(2)+math.sqrt(6))/4); n += 3
    q = z(-1, math.sqrt(3)) / z(1, 1)
    assert close(q, math.sqrt(2)*cmath.exp(1j*5*math.pi/12)) and close(math.cos(5*math.pi/12), (math.sqrt(6)-math.sqrt(2))/4) and close(math.sin(5*math.pi/12), (math.sqrt(6)+math.sqrt(2))/4); n += 3
    h = (math.sqrt(2) + math.sqrt(2)*1j) * (math.sqrt(3)/4 + 0.25j)
    assert close(h, cmath.exp(1j*5*math.pi/12)) and close(2*cmath.exp(1j*math.pi/4) * 0.5*cmath.exp(1j*math.pi/6), h); n += 2
    # rotations
    assert close(1j*z(1, 1), z(-1, 1)); n += 1
    rot = cmath.exp(-1j*7*math.pi/6) * z(4, -2)
    assert close(rot, z(1 - 2*math.sqrt(3), 2 + math.sqrt(3))); n += 1
    assert close(2j*z(3, 1), z(-2, 6)); n += 1
    assert close(4*cmath.exp(2j*math.pi/3), z(-2, 2*math.sqrt(3))); n += 1
    assert close(3*cmath.exp(1j*(math.pi/4 + 3*math.pi/4)), -3); n += 1
    assert close(5*cmath.exp(3j*math.pi/6), 5j) and all(not close(5*cmath.exp(1j*k*math.pi/6), 5j) for k in (1, 2)); n += 2
    assert close(10*cmath.exp(1j*math.pi/6), z(5*math.sqrt(3), 5)); n += 1
    # cos a - i sin a has argument -a
    for a in (0.3, 1.1, 2.0):
        assert close(cmath.phase(z(math.cos(a), -math.sin(a))), -a); n += 1
    # 1 + cos(phi) - i sin(phi) = 2cos(phi/2) cis(-phi/2) ; 1 + cos(pi/7) + i sin(pi/7) argument pi/14
    for ph in (-2.5, -1.0, 0.7, 2.9):
        assert close(z(1 + math.cos(ph), -math.sin(ph)), 2*math.cos(ph/2)*cmath.exp(-1j*ph/2)); n += 1
    assert close(cmath.phase(z(1 + math.cos(math.pi/7), math.sin(math.pi/7))), math.pi/14); n += 1
    # tangent problem: minimise the argument on the circle |z - 5i| = 3 (numerically) and compare with 12/5 + 16/5 i
    best = min((cmath.phase(5j + 3*cmath.exp(1j*t)) , 5j + 3*cmath.exp(1j*t)) for t in [k*2*math.pi/200000 for k in range(200000)] if cmath.phase(5j + 3*cmath.exp(1j*t)) > 0)
    assert close(best[1], z(12/5, 16/5), 1e-3), best; n += 1
    # square, turbine, arm, drone, series
    A_ = z(3, 1); assert [close(1j**k*A_, v) for k, v in [(1, z(-1, 3)), (2, z(-3, -1)), (3, z(1, -3))]] == [True]*3; n += 3
    w = [8*cmath.exp(2j*math.pi*k/3) for k in range(3)]
    assert all(close(abs(w[(k+1) % 3] - w[k]), 8*math.sqrt(3)) for k in range(3)); n += 3
    P = 3*cmath.exp(1j*math.pi/6); E = P + 2*cmath.exp(1j*(math.pi/6 + math.pi/3))
    assert close(E, z(3*math.sqrt(3)/2, 3.5)) and close(abs(E), math.sqrt(19)); n += 2
    z8 = 50*cmath.exp(1j*8*math.pi/12)
    assert close(z8, z(-25, 25*math.sqrt(3))) and close(abs(z8 - 50), 50*math.sqrt(3)) and close(50*cmath.exp(1j*6*math.pi/12), 50j); n += 3
    V = 4 + 3j
    assert close(abs(V), 5) and close(math.degrees(cmath.phase(V)), 36.8698976, 1e-6); n += 2
    # trig-form validity example: -2 cis(pi/3) == 2 cis(4pi/3)
    assert close(-2*cmath.exp(1j*math.pi/3), 2*cmath.exp(1j*4*math.pi/3)) and close(-2*cmath.exp(1j*math.pi/3), z(-1, -math.sqrt(3))); n += 2
    # arg additivity only mod 2pi: z1 = z2 = -1 + i
    a1 = cmath.phase(z(-1, 1)); assert close(2*a1, 3*math.pi/2) and close(cmath.phase(z(-1, 1)**2), -math.pi/2) and close((2*a1 - cmath.phase(z(-1, 1)**2)) % (2*math.pi), 0); n += 2
    # arg of conj z and of -z for arg z = pi/5 ; equality case of the triangle inequality
    zz = cmath.exp(1j*math.pi/5)
    assert close(cmath.phase(zz.conjugate()), -math.pi/5) and close(cmath.phase(-zz), -4*math.pi/5); n += 2
    assert close(abs(z(1, 1) + z(2, 2)), abs(z(1, 1)) + abs(z(2, 2))) and abs(abs(1 + -1) - 2) > 0; n += 2
    return n
