# -*- coding: utf-8 -*-
"""
KhmerMath Question Bank: Grade 12 Science (SC)
Chapter 1: ចំនួនកុំផ្លិច
Lesson 3: ស្វ័យគុណទី n និងឫសទី n នៃចំនួនកុំផ្លិច
Reference textbook: Lesson/G12/SC/C1-L3.tex

Target matrix: MCQ easy10/medium14/hard7/pisa5 + writing easy1/medium4/hard4/pisa5 = 50, a Bloom level on each.
Every number comes from sympy; verify() re-derives the claims a second time with plain numerics.
"""
import sys, os, math, cmath
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib import *
import svgkit as K
from sympy import (I, Rational, sqrt, simplify, expand, expand_complex, re as sre, im as sim, nsimplify, latex, pi, cos, sin, Abs, arg, Add)

LESSON = 'ស្វ័យគុណទី n និងឫសទី n នៃចំនួនកុំផ្លិច'
CHAPTER = 'ជំពូកទី 1 : ចំនួនកុំផ្លិច'
GRADE = '12SC'
TARGET = {('mcq', 'easy'): 10, ('mcq', 'medium'): 14, ('mcq', 'hard'): 7, ('mcq', 'pisa'): 5,
          ('writing', 'easy'): 1, ('writing', 'medium'): 4, ('writing', 'hard'): 4, ('writing', 'pisa'): 5}
S1, S2, S3, S4 = 'ស្វ័យគុណទី n នៃចំនួនកុំផ្លិច', 'អនុវត្តន៍ក្នុងត្រីកោណមាត្រ', 'ឫសទី n នៃចំនួនកុំផ្លិច', 'ដោះស្រាយសមីការដោយប្រើឫសទី n'
TOPIC_MAP = {'s1_pow': S1, 's2_trig': S2, 's3_root': S3, 's4_eq': S4,
             'pisa_wheel': S3, 'pisa_relay': S3, 'pisa_robot': S1, 'pisa_lamps': S3, 'pisa_filter': S1,
             'pisa_antenna': S1, 'pisa_spiral': S1, 'pisa_square': S4}


# ----------------------------------------------------------------------------- helpers
def _L(x):
    return latex(x).replace('\\frac', '\\dfrac')


def val(z):
    return nsimplify(simplify(expand_complex(expand(z))))


def fz(z):
    """a+bi in LaTeX, brackets around a multi-term part."""
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


def cz(a, b=0):
    return a + b * I


def A(p):
    p = Rational(p)
    if p == 0:
        return '0'
    n, d = p.p, p.q
    sg = '-' if n < 0 else ''
    n = abs(n)
    top = '\\pi' if n == 1 else '%d\\pi' % n
    return sg + (top if d == 1 else '\\dfrac{%s}{%d}' % (top, d))


def ARGM(p):
    return M(A(p))


def _arg_in(p):
    t = A(p)
    return '\\left(%s\\right)' % t if t.startswith('-') else ' ' + t


def TF(r, p):
    r = nsimplify(r)
    rs = '' if r == 1 else _L(r) + ' '
    return M('%s\\left(\\cos%s + i\\sin%s\\right)' % (rs, _arg_in(p), _arg_in(p)))


def cis(r, p):
    return val(r * (cos(p * pi) + I * sin(p * pi)))


def pw(z, n):
    return val(z ** n)


def roots_of(z, n):
    r, a = Abs(z), arg(z)
    return [val(r ** Rational(1, n) * (cos((a + 2 * pi * k) / n) + I * sin((a + 2 * pi * k) / n))) for k in range(n)]


def rset(ws):
    return M(',\\ '.join(fz(w) for w in ws))


def skey(ws):
    return frozenset(fz(w) for w in ws)


def pick_sets(right_ws, cand_lists, n=3):
    seen = {skey(right_ws)}
    out = []
    for ws in cand_lists:
        k = skey(ws)
        if k in seen:
            continue
        if any('\\sqrt{\\sqrt' in c or '\\sqrt{2 -' in c or '\\sqrt{-' in c for c in k):
            continue
        seen.add(k)
        out.append(rset(ws))
    assert len(out) >= n, (len(out), [fz(w) for w in right_ws])
    return out[:n]


def with_img(q, svg):
    q['img'] = svg
    return q


# ----------------------------------------------------------------------------- figures
def fig_roots(n, R, unit, phase_deg=0.0, names='M', ticks=1, poly=True, label_every=1, grid=True, extent=None):
    """regular n-gon: the n-th roots of a number, on a circle of radius R (angles phase + 360k/n)."""
    ex = extent if extent else R * 1.35
    pts, ang = [], []
    for k in range(n):
        a = math.radians(phase_deg + 360.0 * k / n)
        x, y = R * math.cos(a), R * math.sin(a)
        lab = ('%s_%d' % (names, k)) if (k % label_every == 0) else ''
        ca, sa = math.cos(a), math.sin(a)
        if abs(sa) < 0.05 and ca > 0:            # on the positive x-axis: above the point, away from the axis label
            dx, dy = 5, -12
        elif abs(ca) < 0.05:                       # on the y-axis: beside the point, away from the axis label
            dx, dy = 15, (-4 if sa > 0 else 12)
        else:                                      # elsewhere: radially outwards
            dx, dy = 15 * ca + (2 if ca > 0 else -10), -15 * sa + (-2 if sa > 0 else 10)
        pts.append((x, y, lab, dx, dy, K.RED if k == 0 else K.BLUE))
        ang.append((x, y))
    polys = [(ang, K.BLUE, None, False)] if poly else []
    spokes = [(0, 0, x, y, K.AXIS, True) for x, y in ang] if poly else []
    return K.plane((-ex, ex), (-ex, ex), unit=unit, circles=[(0, 0, R, K.GREEN, True)], polys=polys, segs=spokes, pts=pts, grid=grid, tick_every=ticks)


def cands():
    C = []
    s3, s2 = sqrt(3), sqrt(2)

    # =============================================================================== MCQ EASY (10)
    C.append(mcq('easy', 's1_pow', 'រូបមន្តដឺម័រ (de Moivre) កំណត់ថា ' + M('(\\cos\\varphi+i\\sin\\varphi)^n') + ' ស្មើ ៖',
                 M('\\cos n\\varphi+i\\sin n\\varphi'), [M('\\cos^n\\varphi+i\\sin^n\\varphi'), M('n\\cos\\varphi+in\\sin\\varphi'), M('\\cos\\varphi^n+i\\sin\\varphi^n')],
                 'ស្វ័យគុណទី ' + M('n') + ' ធ្វើឱ្យអាគុយម៉ង់គុណនឹង ' + M('n') + ' ហើយម៉ូឌុល ' + M('1') + ' នៅដដែល៖ ' + M('(\\cos\\varphi+i\\sin\\varphi)^n=\\cos n\\varphi+i\\sin n\\varphi') + '។', bloom='Remember'))

    C.append(mcq('easy', 's1_pow', 'បើ ' + M('z=r(\\cos\\varphi+i\\sin\\varphi)') + ' នោះ ' + M('|z^n|') + ' និង ' + M('\\arg z^n') + ' គឺ ៖',
                 M('r^n') + ' និង ' + M('n\\varphi'), [M('nr') + ' និង ' + M('n\\varphi'), M('r^n') + ' និង ' + M('\\varphi^n'), M('nr') + ' និង ' + M('\\varphi^n')],
                 M('z^n=r^n(\\cos n\\varphi+i\\sin n\\varphi)') + ' ដូច្នេះ ' + M('|z^n|=r^n') + ' និង ' + M('\\arg z^n=n\\varphi') + '។', bloom='Remember'))

    z = cis(1, Rational(1, 6))
    C.append(mcq('easy', 's1_pow', 'បើ ' + M('z=\\cos\\dfrac\\pi6+i\\sin\\dfrac\\pi6') + ' នោះ ' + M('z^{12}') + ' ស្មើ ៖', Z(pw(z, 12)), [Z(-1), Z(I), M('0')],
                 M('z^{12}=\\cos\\left(12\\cdot\\dfrac\\pi6\\right)+i\\sin\\left(12\\cdot\\dfrac\\pi6\\right)=\\cos2\\pi+i\\sin2\\pi=1') + '។', bloom='Apply'))

    C.append(mcq('easy', 's1_pow', 'គណនា ' + M('(1+i)^8') + ' ៖', Z(pw(1 + I, 8)), [Z(-16), Z(16 * I), Z(8)],
                 M('(1+i)^2=2i') + ' ដូច្នេះ ' + M('(1+i)^8=(2i)^4=16i^4=16') + ' (ឬ ' + M('(\\sqrt2)^8(\\cos2\\pi+i\\sin2\\pi)=16') + ')។', bloom='Apply'))

    C.append(mcq('easy', 's3_root', 'ចំនួនកុំផ្លិចមិនសូន្យ ' + M('z') + ' មានឫសទី ' + M('n') + ' ចំនួនប៉ុន្មាន ?', M('n'), [M('n-1'), M('n+1'), M('2')],
                 'រូបមន្ត ' + M('w_k') + ' ជាមួយ ' + M('k=0,1,\\dots,n-1') + ' ឱ្យឫសផ្សេងគ្នា ' + M('n') + ' ។ ពេល ' + M('k=n') + ' ឫសនឹងចាប់ផ្ដើមដដែលវិញ។', bloom='Remember'))

    C.append(mcq('easy', 's3_root', 'បើ ' + M('z=r(\\cos\\varphi+i\\sin\\varphi)') + ' នោះឫសទី ' + M('n') + ' នៃ ' + M('z') + ' មានម៉ូឌុលស្មើ ៖',
                 M('\\sqrt[n]{r}'), [M('r^n'), M('\\dfrac rn'), M('nr')],
                 'ពី ' + M('s^n=r') + ' និង ' + M('s>0') + ' គេបាន ' + M('s=\\sqrt[n]{r}') + '។', bloom='Remember'))

    C.append(with_img(mcq('easy', 's3_root', 'ក្នុងរូប ចំណុច ' + M('M_0,\\ M_1,\\dots,\\ M_5') + ' ជារូបភាពនៃឫសទី ' + M('6') + ' នៃ ' + M('1') + ' លើរង្វង់ត្រីកោណមាត្រ។ មុំរវាង ' + M('\\overrightarrow{OM_k}') + ' និង ' + M('\\overrightarrow{OM_{k+1}}') + ' (ជាប់គ្នា) ស្មើ ៖',
                          ARGM(Rational(1, 3)), [ARGM(Rational(2, 3)), ARGM(Rational(1, 6)), ARGM(Rational(1, 2))],
                          'ឫសទី ' + M('6') + ' មានអាគុយម៉ង់ ' + M('\\dfrac{2k\\pi}{6}=\\dfrac{k\\pi}{3}') + ' ដូច្នេះមុំរវាងឫសជាប់គ្នាស្មើ ' + M('\\dfrac{2\\pi}{6}=\\dfrac\\pi3') + ' ហើយឫសជាកំពូលនៃឆកោននិយ័ត។', bloom='Understand'),
                      fig_roots(6, 1, 78, 0, 'M', ticks=1, extent=1.5)))

    C.append(mcq('easy', 's2_trig', 'ពីរូបមន្តដឺម័រ ករណី ' + M('n=2') + ' គេទាញបាន ' + M('\\cos2\\varphi') + ' ស្មើ ៖',
                 M('\\cos^2\\varphi-\\sin^2\\varphi'), [M('\\cos^2\\varphi+\\sin^2\\varphi'), M('2\\sin\\varphi\\cos\\varphi'), M('2\\cos\\varphi')],
                 M('(\\cos\\varphi+i\\sin\\varphi)^2=(\\cos^2\\varphi-\\sin^2\\varphi)+2i\\sin\\varphi\\cos\\varphi') + ' ផ្ទឹមផ្នែកពិតនឹង ' + M('\\cos2\\varphi') + '។', bloom='Remember'))

    C.append(mcq('easy', 's1_pow', 'គណនា ' + M('(-1+i)^4') + ' ៖', Z(pw(-1 + I, 4)), [Z(4), Z(-4 * I), Z(16)],
                 M('(-1+i)^2=1-2i+i^2=-2i') + ' ដូច្នេះ ' + M('(-1+i)^4=(-2i)^2=4i^2=-4') + '។', bloom='Apply'))

    C.append(mcq('easy', 's3_root', 'ចំនួនមួយណាខាងក្រោមជាឫសគូបនៃ ' + M('8') + ' ?', Z(cz(-1, s3)), [Z(cz(1, s3)), Z(2 * I), Z(cz(1, 1))],
                 M('-1+i\\sqrt3=2\\left(\\cos\\tfrac{2\\pi}{3}+i\\sin\\tfrac{2\\pi}{3}\\right)') + ' ដូច្នេះ ' + M('(-1+i\\sqrt3)^3=8(\\cos2\\pi+i\\sin2\\pi)=8') + '។ ' + M('(1+i\\sqrt3)^3=-8') + ' និង ' + M('(2i)^3=-8i') + ' មិនមែន។', bloom='Apply'))

    # =============================================================================== MCQ MEDIUM (14)
    C.append(mcq('medium', 's1_pow', 'គណនា ' + M('(\\sqrt3+i)^6') + ' ៖', Z(pw(s3 + I, 6)), [Z(64), Z(64 * I), Z(-64 * I)],
                 M('\\sqrt3+i=2\\left(\\cos\\tfrac\\pi6+i\\sin\\tfrac\\pi6\\right)') + ' ដូច្នេះ ' + M('(\\sqrt3+i)^6=2^6(\\cos\\pi+i\\sin\\pi)=-64') + '។', bloom='Apply'))

    C.append(mcq('medium', 's1_pow', 'គណនា ' + M('(1-i)^{10}') + ' ៖', Z(pw(1 - I, 10)), [Z(32 * I), Z(-32), Z(32)],
                 M('1-i=\\sqrt2\\left[\\cos\\left(-\\tfrac\\pi4\\right)+i\\sin\\left(-\\tfrac\\pi4\\right)\\right]') + ' ដូច្នេះ ' + M('(1-i)^{10}=2^5\\left[\\cos\\left(-\\tfrac{5\\pi}2\\right)+i\\sin\\left(-\\tfrac{5\\pi}2\\right)\\right]=32(-i)=-32i') + '។', bloom='Apply'))

    zz = -s3 + I
    C.append(mcq('medium', 's1_pow', 'សរសេរ ' + M('(-\\sqrt3+i)^{13}') + ' ជាទម្រង់ ' + M('a+bi') + ' ៖', Z(pw(zz, 13)),
                 [Z(-pw(zz, 13)), Z(pw(zz, 13).conjugate()), Z(13 * zz)],
                 M('-\\sqrt3+i=2\\left(\\cos\\tfrac{5\\pi}6+i\\sin\\tfrac{5\\pi}6\\right)') + ' ដូច្នេះ ' + M('(-\\sqrt3+i)^{13}=2^{13}\\left(\\cos\\tfrac{65\\pi}6+i\\sin\\tfrac{65\\pi}6\\right)=2^{13}\\left(\\cos\\tfrac{5\\pi}6+i\\sin\\tfrac{5\\pi}6\\right)=-2^{12}\\sqrt3+2^{12}i') + '។', bloom='Apply'))

    C.append(mcq('medium', 's1_pow', 'គណនា ' + M('\\left(\\dfrac{1+i}{1-i}\\right)^{2n}') + ' ដែល ' + M('n') + ' ជាចំនួនគត់វិជ្ជមាន ៖', M('(-1)^n'), [M('1'), M('-1'), M('i^n')],
                 M('\\dfrac{1+i}{1-i}=i') + ' ដូច្នេះ ' + M('i^{2n}=(i^2)^n=(-1)^n') + ' (ស្មើ ' + M('1') + ' បើ ' + M('n') + ' គូ ហើយ ' + M('-1') + ' បើ ' + M('n') + ' សេស)។', bloom='Apply'))

    C.append(mcq('medium', 's2_trig', 'រូបមន្តមួយណាត្រឹមត្រូវសម្រាប់ ' + M('\\cos3\\varphi') + ' ?', M('4\\cos^3\\varphi-3\\cos\\varphi'),
                 [M('3\\cos\\varphi-4\\cos^3\\varphi'), M('\\cos^3\\varphi+3\\cos\\varphi\\sin^2\\varphi'), M('3\\cos^2\\varphi\\sin\\varphi-\\sin^3\\varphi')],
                 'ផ្នែកពិតនៃ ' + M('(\\cos\\varphi+i\\sin\\varphi)^3') + ' គឺ ' + M('\\cos^3\\varphi-3\\cos\\varphi\\sin^2\\varphi=4\\cos^3\\varphi-3\\cos\\varphi') + ' (ប្រើ ' + M('\\sin^2\\varphi=1-\\cos^2\\varphi') + ')។', bloom='Understand'))

    C.append(mcq('medium', 's2_trig', 'រូបមន្តមួយណាត្រឹមត្រូវសម្រាប់ ' + M('\\sin3\\varphi') + ' ?', M('3\\sin\\varphi-4\\sin^3\\varphi'),
                 [M('4\\sin^3\\varphi-3\\sin\\varphi'), M('3\\sin\\varphi+4\\sin^3\\varphi'), M('\\sin^3\\varphi-3\\cos^2\\varphi\\sin\\varphi')],
                 'ផ្នែកនិមិត្តនៃ ' + M('(\\cos\\varphi+i\\sin\\varphi)^3') + ' គឺ ' + M('3\\cos^2\\varphi\\sin\\varphi-\\sin^3\\varphi=3\\sin\\varphi-4\\sin^3\\varphi') + '។', bloom='Understand'))

    C.append(mcq('medium', 's3_root', 'ឫសការ៉េនៃ ' + M('z=9\\left(\\cos\\dfrac\\pi4+i\\sin\\dfrac\\pi4\\right)') + ' គឺ ៖',
                 M('\\pm3\\left(\\cos\\dfrac\\pi8+i\\sin\\dfrac\\pi8\\right)'),
                 [M('\\pm3\\left(\\cos\\dfrac\\pi4+i\\sin\\dfrac\\pi4\\right)'), M('\\pm\\sqrt3\\left(\\cos\\dfrac\\pi8+i\\sin\\dfrac\\pi8\\right)'), M('\\pm9\\left(\\cos\\dfrac\\pi8+i\\sin\\dfrac\\pi8\\right)')],
                 'ម៉ូឌុលឫសការ៉េ ' + M('\\sqrt9=3') + ' អាគុយម៉ង់ ' + M('\\dfrac{\\pi/4+2k\\pi}{2}') + ' គឺ ' + M('\\dfrac\\pi8') + ' ឬ ' + M('\\dfrac{9\\pi}{8}') + ' ពោលគឺឫសពីរជាចំនួនផ្ទុយគ្នា ' + M('\\pm3(\\cos\\tfrac\\pi8+i\\sin\\tfrac\\pi8)') + '។', bloom='Apply'))

    ws = roots_of(16, 4)
    C.append(mcq('medium', 's3_root', 'ឫសទី ' + M('4') + ' នៃ ' + M('16') + ' ក្នុងទម្រង់ ' + M('a+bi') + ' គឺ ៖', rset(ws),
                 pick_sets(ws, [roots_of(-16, 4), [w * 2 for w in ws], [w / 2 for w in ws], [-w for w in ws], roots_of(16 * I, 4)]),
                 M('16=16(\\cos0+i\\sin0)') + ' ដូច្នេះ ' + M('w_k=2\\left(\\cos\\tfrac{k\\pi}{2}+i\\sin\\tfrac{k\\pi}{2}\\right)') + ' ដែល ' + M('k=0,1,2,3') + ' គឺ ' + M('2,\\ 2i,\\ -2,\\ -2i') + '។', bloom='Apply'))

    C.append(with_img(mcq('medium', 's3_root', 'ក្នុងរូប ចំណុច ' + M('M_0,\\dots,M_4') + ' ជារូបភាពនៃឫសទី ' + M('5') + ' នៃចំនួនកុំផ្លិចមួយ ដែលស្ថិតលើរង្វង់ដូចគ្នា។ មុំ ' + M('\\widehat{M_0OM_1}') + ' ស្មើ ៖',
                          ARGM(Rational(2, 5)), [ARGM(Rational(1, 5)), ARGM(Rational(1, 3)), ARGM(Rational(4, 5))],
                          'ឫសទី ' + M('5') + ' មានអាគុយម៉ង់ដាច់ពីគ្នា ' + M('\\dfrac{2\\pi}{5}') + ' (' + M('=72^\\circ') + ') ដូច្នេះកំពូលបង្កើតបានជាបញ្ចកោណនិយ័ត។', bloom='Analyze'),
                      fig_roots(5, 2, 40, 18, 'M', ticks=1, extent=2.7)))

    zq = -8 - 8 * s3 * I
    C.append(mcq('medium', 's3_root', 'ឫសទី ' + M('4') + ' នៃ ' + M('z=-8-8\\sqrt3\\,i') + ' មានអាគុយម៉ង់ ' + M('\\dfrac{4\\pi/3+2k\\pi}{4}') + '។ អាគុយម៉ង់នៃឫស ' + M('w_1') + ' (' + M('k=1') + ') ស្មើ ៖',
                 ARGM(Rational(5, 6)), [ARGM(Rational(1, 3)), ARGM(Rational(11, 6)), ARGM(Rational(2, 3))],
                 M('\\dfrac{\\tfrac{4\\pi}{3}+2\\pi}{4}=\\dfrac{\\tfrac{10\\pi}{3}}{4}=\\dfrac{5\\pi}{6}') + ' (ចំណែក ' + M('k=0') + ' ឱ្យ ' + M('\\tfrac\\pi3') + ' ហើយ ' + M('k=3') + ' ឱ្យ ' + M('\\tfrac{11\\pi}{6}') + ')។', bloom='Apply'))

    C.append(mcq('medium', 's4_eq', 'ចំនួនមួយណាខាងក្រោមជាឫសនៃសមីការ ' + M('z^6+64=0') + ' ?', M('2i'), [M('2'), M('\\sqrt3'), M('1+i')],
                 M('(2i)^6=2^6i^6=64\\cdot(-1)=-64') + ' ដូច្នេះ ' + M('(2i)^6+64=0') + '។ ' + M('2^6=64') + ' និង ' + M('(\\sqrt3)^6=27') + ' ហើយ ' + M('(1+i)^6=(2i)^3=-8i') + ' មិនស្មើ ' + M('-64') + '។', bloom='Analyze'))

    C.append(mcq('medium', 's4_eq', 'ដោះស្រាយសមីការ ' + M('(z-2)^3=1') + ' ៖',
                 M('3,\\ \\dfrac32+\\dfrac{\\sqrt3}{2}i,\\ \\dfrac32-\\dfrac{\\sqrt3}{2}i'),
                 [M('1,\\ -\\dfrac12+\\dfrac{\\sqrt3}{2}i,\\ -\\dfrac12-\\dfrac{\\sqrt3}{2}i'), M('-1,\\ \\dfrac12+\\dfrac{\\sqrt3}{2}i,\\ \\dfrac12-\\dfrac{\\sqrt3}{2}i'), M('2,\\ 2+\\dfrac{\\sqrt3}{2}i,\\ 2-\\dfrac{\\sqrt3}{2}i')],
                 M('z-2') + ' ជាឫសគូបនៃ ' + M('1') + ' គឺ ' + M('1,\\ -\\tfrac12\\pm\\tfrac{\\sqrt3}2i') + ' ហើយ ' + M('z=w+2') + ' បាន ' + M('3,\\ \\tfrac32\\pm\\tfrac{\\sqrt3}{2}i') + '។', bloom='Apply'))

    C.append(mcq('medium', 's4_eq', 'ផលបូកនៃឫសគូបទាំងបីនៃ ' + M('1') + ' ស្មើ ៖', M('0'), [M('1'), M('3'), M('-1')],
                 'ឫសគឺ ' + M('1') + ' និង ' + M('-\\tfrac12\\pm\\tfrac{\\sqrt3}{2}i') + ' ដូច្នេះផលបូក ' + M('1+\\left(-\\tfrac12+\\tfrac{\\sqrt3}2i\\right)+\\left(-\\tfrac12-\\tfrac{\\sqrt3}2i\\right)=0') + '។ (ក្នុងសមីការ ' + M('z^3-1=0') + ' មេគុណ ' + M('z^2') + ' ស្មើសូន្យ។)', bloom='Analyze'))

    C.append(mcq('medium', 's4_eq', 'ផលគុណនៃឫសគូបទាំងបីនៃ ' + M('1') + ' ស្មើ ៖', M('1'), [M('0'), M('3'), M('-1')],
                 M('1\\cdot\\left(-\\tfrac12+\\tfrac{\\sqrt3}2i\\right)\\left(-\\tfrac12-\\tfrac{\\sqrt3}2i\\right)=\\tfrac14+\\tfrac34=1') + '។', bloom='Analyze'))

    # =============================================================================== MCQ HARD (7)
    u = pw(1 + I * s3, 5) + pw(1 - I * s3, 5)
    C.append(mcq('hard', 's1_pow', 'គណនា ' + M('u=(1+i\\sqrt3)^5+(1-i\\sqrt3)^5') + ' ៖', Z(u), [Z(16), Z(64), Z(32 * I)],
                 M('1+i\\sqrt3=2\\left(\\cos\\tfrac\\pi3+i\\sin\\tfrac\\pi3\\right)') + ' ដូច្នេះ ' + M('(1+i\\sqrt3)^5=32\\left(\\cos\\tfrac{5\\pi}3+i\\sin\\tfrac{5\\pi}3\\right)=16-16\\sqrt3\\,i') + ' ហើយ ' + M('(1-i\\sqrt3)^5') + ' ជាចំនួនឆ្លាស់ ' + M('16+16\\sqrt3\\,i') + ' ដូច្នេះ ' + M('u=32') + '។', bloom='Analyze'))

    C.append(mcq('hard', 's1_pow', 'សិស្សម្នាក់សរសេរថា ' + M('(\\cos\\varphi+i\\sin\\varphi)^n=\\cos^n\\varphi+i\\sin^n\\varphi') + '។ ឃ្លាមួយណាវាយតម្លៃបានត្រឹមត្រូវ ?',
                 'ខុស ឧ. ' + M('\\varphi=\\tfrac\\pi4,\\ n=2') + ' ៖ ខាងឆ្វេងស្មើ ' + M('i') + ' តែខាងស្ដាំស្មើ ' + M('\\tfrac12+\\tfrac12i'),
                 ['ត្រឹមត្រូវ ព្រោះស្វ័យគុណអនុវត្តលើ ' + M('\\cos') + ' និង ' + M('\\sin') + ' ដោយឡែកពីគ្នា', 'ខុស ព្រោះត្រូវជា ' + M('n\\cos\\varphi+in\\sin\\varphi') + ' ពោលគឺគុណនឹង ' + M('n'), 'ត្រឹមត្រូវតែពេល ' + M('n') + ' ជាចំនួនគូប៉ុណ្ណោះ'],
                 'រូបមន្តត្រឹមត្រូវគឺ ' + M('\\cos n\\varphi+i\\sin n\\varphi') + ' (គុណអាគុយម៉ង់នឹង ' + M('n') + ')។ ជាមួយ ' + M('\\varphi=\\tfrac\\pi4,\\ n=2') + ' ៖ ' + M('(\\cos\\tfrac\\pi4+i\\sin\\tfrac\\pi4)^2=\\cos\\tfrac\\pi2+i\\sin\\tfrac\\pi2=i') + ' តែ ' + M('\\cos^2\\tfrac\\pi4+i\\sin^2\\tfrac\\pi4=\\tfrac12+\\tfrac12i') + ' ខុសគ្នា។', bloom='Evaluate'))

    C.append(mcq('hard', 's1_pow', 'គេដឹងថា ' + M('\\dfrac{1+\\sin\\varphi+i\\cos\\varphi}{1+\\sin\\varphi-i\\cos\\varphi}=\\cos\\left(\\dfrac\\pi2-\\varphi\\right)+i\\sin\\left(\\dfrac\\pi2-\\varphi\\right)') + '។ ស្វ័យគុណទី ' + M('n') + ' នៃប្រភាគនេះស្មើ ៖',
                 M('\\cos\\left[n\\left(\\dfrac\\pi2-\\varphi\\right)\\right]+i\\sin\\left[n\\left(\\dfrac\\pi2-\\varphi\\right)\\right]'),
                 [M('\\cos n\\varphi+i\\sin n\\varphi'), M('\\cos\\left[n\\left(\\dfrac\\pi2+\\varphi\\right)\\right]+i\\sin\\left[n\\left(\\dfrac\\pi2+\\varphi\\right)\\right]'), M('\\cos\\left[\\dfrac{1}{n}\\left(\\dfrac\\pi2-\\varphi\\right)\\right]+i\\sin\\left[\\dfrac{1}{n}\\left(\\dfrac\\pi2-\\varphi\\right)\\right]')],
                 'ប្រភាគមានម៉ូឌុល ' + M('1') + ' និងអាគុយម៉ង់ ' + M('\\tfrac\\pi2-\\varphi') + ' ដូច្នេះតាមរូបមន្តដឺម័រ អាគុយម៉ង់ត្រូវគុណនឹង ' + M('n') + ' ៖ ' + M('\\cos[n(\\tfrac\\pi2-\\varphi)]+i\\sin[n(\\tfrac\\pi2-\\varphi)]') + '។', bloom='Analyze'))

    C.append(mcq('hard', 's4_eq', 'ចំនួន ' + M('z_0=\\sqrt2(1+i)') + ' ជាឫសមួយនៃសមីការមួយណាខាងក្រោម ?', M('z^4+16=0'), [M('z^4-16=0'), M('z^4+4=0'), M('z^2-4=0')],
                 M('z_0=2\\left(\\cos\\tfrac\\pi4+i\\sin\\tfrac\\pi4\\right)') + ' ដូច្នេះ ' + M('z_0^4=16(\\cos\\pi+i\\sin\\pi)=-16') + ' ពោលគឺ ' + M('z_0^4+16=0') + '។ (សមីការ ' + M('z^4-16=0') + ' មានឫស ' + M('\\pm2,\\pm2i') + ' ហើយ ' + M('z_0^2=4i\\ne4') + ')។', bloom='Create'))

    zw = -8 - 8 * s3 * I
    C.append(with_img(mcq('hard', 's3_root', 'ក្នុងរូប ចំណុច ' + M('M_0,\\ M_1,\\ M_2,\\ M_3') + ' ជារូបភាពនៃឫសទី ' + M('4') + ' នៃចំនួនកុំផ្លិច ' + M('z') + '។ ចំណុច ' + M('M_0') + ' មានម៉ូឌុល ' + M('2') + ' និងអាគុយម៉ង់ ' + M('\\dfrac\\pi3') + '។ ចំនួន ' + M('z') + ' ស្មើ ៖',
                          Z(zw), [Z(cz(-8, 8 * s3)), Z(cz(8, -8 * s3)), Z(16)],
                          'ឫសមួយ ' + M('w_0=2\\left(\\cos\\tfrac\\pi3+i\\sin\\tfrac\\pi3\\right)') + ' ដូច្នេះ ' + M('z=w_0^4=16\\left(\\cos\\tfrac{4\\pi}3+i\\sin\\tfrac{4\\pi}3\\right)=16\\left(-\\tfrac12-\\tfrac{\\sqrt3}{2}i\\right)=-8-8\\sqrt3\\,i') + ' (ឫសទាំងបួនស្មើគ្នា ' + M('\\tfrac\\pi2') + ' រវាងគ្នា)។', bloom='Analyze'),
                      fig_roots(4, 2, 40, 60, 'M', ticks=1, extent=2.7)))

    z = cis(1, Rational(1, 6))
    C.append(mcq('hard', 's2_trig', 'បើ ' + M('z=\\cos\\dfrac\\pi6+i\\sin\\dfrac\\pi6') + ' នោះ ' + M('S=1+z+z^2+z^3+\\dots+z^{11}') + ' ស្មើ ៖', M('0'), [M('1'), M('12'), M('-1')],
                 M('z^{12}=\\cos2\\pi+i\\sin2\\pi=1') + ' ហើយ ' + M('z\\ne1') + ' ដូច្នេះ ' + M('S=\\dfrac{z^{12}-1}{z-1}=0') + ' (ផលបូកស្វ៊ីតធរណីមាត្រ)។', bloom='Analyze'))

    C.append(mcq('hard', 's4_eq', 'សមីការ ' + M('z^6+2z^3+1=0') + ' មានឫសខុសៗគ្នាប៉ុន្មានក្នុង ' + M('\\mathbb{C}') + ' ?', '3', ['6', '2', '1'],
                 M('z^6+2z^3+1=(z^3+1)^2') + ' ដូច្នេះសមីការសមមូល ' + M('z^3=-1') + ' ដែលមានឫសខុសគ្នា ' + M('3') + ' គឺ ' + M('\\tfrac12\\pm\\tfrac{\\sqrt3}2i') + ' និង ' + M('-1') + ' (ឫសនីមួយៗជាឫសទ្វេ មិនមែនមាន ' + M('6') + ' ឫសខុសគ្នាទេ)។', bloom='Evaluate'))

    # =============================================================================== MCQ PISA (5)
    C.append(with_img(mcq('pisa', 'pisa_wheel', 'កង់ទេសចរណ៍កាំ ' + M('10\\ \\text{m}') + ' មាន ១២ កាប៊ីនស្ថិតស្មើគ្នាលើរង្វង់ ដូចក្នុងរូប (ជុំវិញផ្ចិត ' + M('O') + ' ជាគល់នៃប្លង់កុំផ្លិច)។ កាប៊ីនលេខ ' + M('0') + ' នៅត្រង់ ' + M('10') + ' ។ កាប៊ីនលេខ ' + M('k') + ' ស្ថិតត្រង់ ' + M('10\\left(\\cos\\tfrac{k\\pi}6+i\\sin\\tfrac{k\\pi}6\\right)') + '។ កាប៊ីនលេខ ' + M('3') + ' ស្ថិតត្រង់ចំនួនកុំផ្លិច ៖',
                          M('10i'), [M('10'), M('-10i'), M('5\\sqrt3+5i')],
                          'ជាមួយ ' + M('k=3') + ' ៖ ' + M('10\\left(\\cos\\tfrac\\pi2+i\\sin\\tfrac\\pi2\\right)=10i') + ' (ចុងកំពូលនៃកង់)។', bloom='Apply'),
                      fig_roots(12, 10, 17, 0, 'C', ticks=100, poly=False, label_every=3, grid=False, extent=12.5)))

    C.append(with_img(mcq('pisa', 'pisa_relay', 'ស្ថានីយ៍ផ្ទេរសញ្ញាបីដាក់ស្មើគ្នាលើរង្វង់កាំ ' + M('6\\ \\text{km}') + ' ជុំវិញប៉មមួយ ដូចក្នុងរូប។ ស្ថានីយ៍ទី ១ នៅត្រង់ ' + M('6') + ' (ជាឫសគូបនៃ ' + M('216') + ')។ ចម្ងាយរវាងស្ថានីយ៍ណាមួយពីរគឺ ៖',
                          M('6\\sqrt3\\ \\text{km}'), [M('6\\ \\text{km}'), M('12\\ \\text{km}'), M('3\\sqrt3\\ \\text{km}')],
                          'ឫសគូបនៃ ' + M('216') + ' គឺ ' + M('6,\\ -3+3\\sqrt3\\,i,\\ -3-3\\sqrt3\\,i') + '។ ' + M('|(-3+3\\sqrt3\\,i)-6|=|-9+3\\sqrt3\\,i|=\\sqrt{81+27}=\\sqrt{108}=6\\sqrt3') + ' ដូចគ្នាចំពោះគ្រប់គូ (ត្រីកោណសមមាត្រ)។', bloom='Analyze'),
                      fig_roots(3, 6, 28, 0, 'S', ticks=2, extent=7.8)))

    C.append(mcq('pisa', 'pisa_robot', 'មនុស្សយន្តបង្វិលទិសខ្លួនច្រាសទ្រនិចនាឡិកា ' + M('15^\\circ') + ' (' + M('=\\dfrac\\pi{12}') + ') រាល់ពេលទទួលបញ្ជា។ ទិសបច្ចុប្បន្នតាងដោយ ' + M('z_0=1') + ' ហើយក្រោយបញ្ជា ' + M('n') + ' ដងទិសគឺ ' + M('\\left(\\cos\\tfrac\\pi{12}+i\\sin\\tfrac\\pi{12}\\right)^n') + '។ ក្រោយបញ្ជាប៉ុន្មានដង ទើបមនុស្សយន្តត្រលប់មកទិសដើមជាលើកដំបូង ?',
                 '24 ដង', ['12 ដង', '6 ដង', '48 ដង'],
                 'ត្រូវការ ' + M('\\left(\\cos\\tfrac\\pi{12}+i\\sin\\tfrac\\pi{12}\\right)^n=\\cos\\tfrac{n\\pi}{12}+i\\sin\\tfrac{n\\pi}{12}=1') + ' គឺ ' + M('\\tfrac{n\\pi}{12}=2\\pi') + ' ដូច្នេះ ' + M('n=24') + ' (ក្រោយ 12 ដងត្រូវបានទិសផ្ទុយ ' + M('-1') + ')។', bloom='Analyze'))

    C.append(with_img(mcq('pisa', 'pisa_lamps', 'បង្គោលភ្លើងប្រាំស្ថិតស្មើគ្នាជុំវិញសួនរង្វង់កាំ ' + M('2\\ \\text{m}') + ' ជាឫសទី ' + M('5') + ' នៃ ' + M('32') + ' ដូចក្នុងរូប ដែលបង្គោល ' + M('L_0') + ' នៅត្រង់ ' + M('2') + '។ បង្គោល ' + M('L_k') + ' មានអាគុយម៉ង់ ' + M('\\tfrac{2k\\pi}{5}') + '។ អាគុយម៉ង់នៃបង្គោល ' + M('L_2') + ' ស្មើ ៖',
                          ARGM(Rational(4, 5)), [ARGM(Rational(2, 5)), ARGM(Rational(6, 5)), ARGM(Rational(8, 5))],
                          M('32=32(\\cos0+i\\sin0)') + ' ដូច្នេះ ' + M('w_k=2\\left(\\cos\\tfrac{2k\\pi}5+i\\sin\\tfrac{2k\\pi}5\\right)') + '។ ជាមួយ ' + M('k=2') + ' ៖ អាគុយម៉ង់ ' + M('\\tfrac{4\\pi}{5}') + '។', bloom='Apply'),
                      fig_roots(5, 2, 40, 0, 'L', ticks=1, extent=2.7)))

    G6 = pw(cis(s2, Rational(1, 12)), 6)
    C.append(mcq('pisa', 'pisa_filter', 'ការឆ្លើយតបនៃដំណាក់កាលតម្រងមួយតាងដោយ ' + M('G=\\sqrt2\\left(\\cos\\dfrac\\pi{12}+i\\sin\\dfrac\\pi{12}\\right)') + '។ ដំណាក់កាលដូចគ្នាប្រាំមួយតភ្ជាប់គ្នា ការឆ្លើយតបសរុបគឺ ' + M('G^6') + ' ស្មើ ៖',
                 Z(G6), [Z(8), Z(-8), Z(64 * I)],
                 M('G^6=(\\sqrt2)^6\\left(\\cos\\tfrac{6\\pi}{12}+i\\sin\\tfrac{6\\pi}{12}\\right)=8\\left(\\cos\\tfrac\\pi2+i\\sin\\tfrac\\pi2\\right)=8i') + ' (អំព្លីទុត ' + M('8') + ' ផាស ' + M('90^\\circ') + ')។', bloom='Apply'))

    # =============================================================================== WRITING EASY (1)
    C.append(wr('easy', 's1_pow', 'គណនា ' + M('(1+i)^{12}') + ' ដោយប្រើទម្រង់ត្រីកោណមាត្រ។',
                [('ម៉ូឌុល និងអាគុយម៉ង់ ៖ ' + M('1+i=\\sqrt2\\left(\\cos\\tfrac\\pi4+i\\sin\\tfrac\\pi4\\right)'), 2),
                 ('រូបមន្តដឺម័រ ៖ ' + M('(1+i)^{12}=(\\sqrt2)^{12}\\left(\\cos\\tfrac{12\\pi}{4}+i\\sin\\tfrac{12\\pi}{4}\\right)=64(\\cos3\\pi+i\\sin3\\pi)'), 2),
                 ('ដូច្នេះ ' + M('(1+i)^{12}=64\\times(-1)=-64'), 1)], bloom='Apply'))

    # =============================================================================== WRITING MEDIUM (4)
    C.append(wr('medium', 's1_pow', 'សរសេរ ' + M('(-\\sqrt3+i)^{13}') + ' ជាទម្រង់ពីជគណិត ' + M('a+bi') + '។',
                [('ម៉ូឌុល ៖ ' + M('r=\\sqrt{(-\\sqrt3)^2+1^2}=2'), 1),
                 ('អាគុយម៉ង់ ៖ ' + M('\\cos\\varphi=-\\dfrac{\\sqrt3}2') + ' និង ' + M('\\sin\\varphi=\\dfrac12') + ' ដូច្នេះ ' + M('\\varphi=\\dfrac{5\\pi}6') + ' គឺ ' + M('-\\sqrt3+i=2\\left(\\cos\\tfrac{5\\pi}6+i\\sin\\tfrac{5\\pi}6\\right)'), 1),
                 ('រូបមន្តដឺម័រ ៖ ' + M('(-\\sqrt3+i)^{13}=2^{13}\\left(\\cos\\tfrac{65\\pi}6+i\\sin\\tfrac{65\\pi}6\\right)'), 1),
                 ('កាត់ ' + M('2\\pi') + ' ចេញ ៖ ' + M('\\tfrac{65\\pi}{6}=10\\pi+\\tfrac{5\\pi}6') + ' ដូច្នេះ ' + M('=2^{13}\\left(\\cos\\tfrac{5\\pi}6+i\\sin\\tfrac{5\\pi}6\\right)'), 1),
                 ('ទម្រង់ពីជគណិត ៖ ' + M('=2^{13}\\left(-\\tfrac{\\sqrt3}2+\\tfrac12i\\right)=-2^{12}\\sqrt3+2^{12}i'), 1)], bloom='Apply'))

    C.append(wr('medium', 's1_pow', 'គណនា ' + M('z=\\left(\\dfrac{1+i}{1-i}\\right)^{2n}') + ' ដែល ' + M('n') + ' ជាចំនួនគត់វិជ្ជមាន ហើយបញ្ជាក់តម្លៃនៃ ' + M('z') + ' ក្នុងករណី ' + M('n') + ' គូ និង ' + M('n') + ' សេស។',
                [('សម្រួលប្រភាគ ៖ ' + M('\\dfrac{1+i}{1-i}=\\dfrac{(1+i)(1+i)}{(1-i)(1+i)}=\\dfrac{2i}{2}=i'), 1),
                 ('ទម្រង់ត្រីកោណមាត្រ ៖ ' + M('i=\\cos\\tfrac\\pi2+i\\sin\\tfrac\\pi2') + ' (ម៉ូឌុល ' + M('1') + ')', 1),
                 ('រូបមន្តដឺម័រ ៖ ' + M('z=i^{2n}=\\cos(n\\pi)+i\\sin(n\\pi)'), 1),
                 ('ដូច្នេះ ' + M('z=(\\cos\\pi+i\\sin\\pi)^n=(-1)^n'), 1),
                 ('សន្និដ្ឋាន ៖ ' + M('z=1') + ' បើ ' + M('n') + ' គូ ហើយ ' + M('z=-1') + ' បើ ' + M('n') + ' សេស។ (ផ្ទៀងផ្ទាត់ ៖ ' + M('i^{2n}=(i^2)^n=(-1)^n') + ')។', 1)], bloom='Apply'))

    wl = roots_of(-1 + I, 5)
    C.append(with_img(wr('medium', 's3_root', 'គណនាឫសទី ' + M('5') + ' នៃចំនួនកុំផ្លិច ' + M('z=-1+i') + ' រួចតាងចំណុចរូបភាពនៃឫសទាំងនោះលើរង្វង់ ដូចក្នុងរូប។',
                         [('ម៉ូឌុល និងអាគុយម៉ង់ ៖ ' + M('r=\\sqrt2') + ' និង ' + M('\\varphi=\\tfrac{3\\pi}4') + ' គឺ ' + M('z=\\sqrt2\\left(\\cos\\tfrac{3\\pi}4+i\\sin\\tfrac{3\\pi}4\\right)'), 1),
                          ('រូបមន្តឫស ៖ ' + M('w_k=2^{\\frac1{10}}\\left[\\cos\\tfrac{\\frac{3\\pi}4+2k\\pi}{5}+i\\sin\\tfrac{\\frac{3\\pi}4+2k\\pi}{5}\\right]') + ' ដែល ' + M('k=0,1,2,3,4'), 1),
                          ('សម្រួលអាគុយម៉ង់ ៖ ' + M('\\tfrac{3\\pi+8k\\pi}{20}') + ' ដូច្នេះ ' + M('w_k=2^{\\frac1{10}}\\left[\\cos\\tfrac{3\\pi+8k\\pi}{20}+i\\sin\\tfrac{3\\pi+8k\\pi}{20}\\right]'), 1),
                          ('តម្លៃអាគុយម៉ង់ ៖ ' + M('\\tfrac{3\\pi}{20},\\ \\tfrac{11\\pi}{20},\\ \\tfrac{19\\pi}{20},\\ \\tfrac{27\\pi}{20},\\ \\tfrac{35\\pi}{20}') + ' សម្រាប់ ' + M('k=0,\\dots,4'), 1),
                          ('រូបភាព ៖ ឫសទាំង ៥ ស្ថិតលើរង្វង់កាំ ' + M('2^{1/10}\\approx1{,}07') + ' ហើយជាកំពូលនៃបញ្ចកោណនិយ័ត (អាគុយម៉ង់ដាច់ពីគ្នា ' + M('\\tfrac{2\\pi}5') + ')។', 1)], bloom='Apply'),
                     fig_roots(5, 2 ** 0.1, 90, 27, 'w', ticks=1, extent=1.6)))

    C.append(wr('medium', 's4_eq', 'ដោះស្រាយសមីការ ' + M('z^6+64=0') + ' ក្នុង ' + M('\\mathbb{C}') + '។',
                [('សមីការសមមូល ' + M('z^6=-64') + ' គឺ ' + M('z') + ' ជាឫសទី ' + M('6') + ' នៃ ' + M('-64'), 1),
                 ('ទម្រង់ត្រីកោណមាត្រ ៖ ' + M('-64=64(\\cos\\pi+i\\sin\\pi)'), 1),
                 ('រូបមន្តឫស ៖ ' + M('w_k=2\\left(\\cos\\tfrac{\\pi+2k\\pi}6+i\\sin\\tfrac{\\pi+2k\\pi}6\\right)') + ' ដែល ' + M('k=0,\\dots,5'), 1),
                 ('គណនា ៖ ' + M('w_0=\\sqrt3+i') + ', ' + M('w_1=2i') + ', ' + M('w_2=-\\sqrt3+i'), 1),
                 (M('w_3=-\\sqrt3-i') + ', ' + M('w_4=-2i') + ', ' + M('w_5=\\sqrt3-i') + ' (កំពូលនៃឆកោននិយ័តកាំ ' + M('2') + ')។', 1)], bloom='Apply'))

    # =============================================================================== WRITING HARD (4)
    C.append(wr('hard', 's1_pow', 'ស្រាយបញ្ជាក់សមភាព ' + M('\\left(\\dfrac{1+\\sin\\varphi+i\\cos\\varphi}{1+\\sin\\varphi-i\\cos\\varphi}\\right)^n=\\cos\\left[n\\left(\\dfrac\\pi2-\\varphi\\right)\\right]+i\\sin\\left[n\\left(\\dfrac\\pi2-\\varphi\\right)\\right]') + '។',
                [('គុណភាគយក និងភាគបែងនឹង ' + M('1+\\sin\\varphi+i\\cos\\varphi') + ' ៖ ' + M('\\dfrac{(1+\\sin\\varphi+i\\cos\\varphi)^2}{(1+\\sin\\varphi)^2-(i\\cos\\varphi)^2}'), 1),
                 ('ភាគបែង ៖ ' + M('(1+\\sin\\varphi)^2+\\cos^2\\varphi=2(1+\\sin\\varphi)'), 1),
                 ('ភាគយក ៖ ' + M('1+\\sin^2\\varphi-\\cos^2\\varphi+2\\sin\\varphi+2i\\cos\\varphi(1+\\sin\\varphi)=2\\sin\\varphi(1+\\sin\\varphi)+2i\\cos\\varphi(1+\\sin\\varphi)'), 1),
                 ('ចែក ៖ ប្រភាគ ' + M('=\\sin\\varphi+i\\cos\\varphi=\\cos\\left(\\tfrac\\pi2-\\varphi\\right)+i\\sin\\left(\\tfrac\\pi2-\\varphi\\right)'), 1),
                 ('រូបមន្តដឺម័រ ៖ ស្វ័យគុណទី ' + M('n') + ' ឱ្យ ' + M('\\cos\\left[n\\left(\\tfrac\\pi2-\\varphi\\right)\\right]+i\\sin\\left[n\\left(\\tfrac\\pi2-\\varphi\\right)\\right]') + ' ជាសមភាពដែលត្រូវស្រាយ។', 1)], bloom='Evaluate'))

    C.append(wr('hard', 's2_trig', 'ក. ដោយប្រើរូបមន្តដឺម័រ ' + M('n=3') + ' បង្ហាញថា ' + M('\\cos3\\varphi=4\\cos^3\\varphi-3\\cos\\varphi') + '។ ខ. ទាញថា ' + M('x=\\cos\\dfrac\\pi9') + ' ជាឫសនៃសមីការ ' + M('8x^3-6x-1=0') + '។',
                [('ពន្លាត ៖ ' + M('(\\cos\\varphi+i\\sin\\varphi)^3=\\cos^3\\varphi+3i\\cos^2\\varphi\\sin\\varphi-3\\cos\\varphi\\sin^2\\varphi-i\\sin^3\\varphi'), 1),
                 ('ផ្នែកពិត ៖ ' + M('\\cos^3\\varphi-3\\cos\\varphi\\sin^2\\varphi'), 1),
                 ('ប្រើ ' + M('\\sin^2\\varphi=1-\\cos^2\\varphi') + ' និងរូបមន្តដឺម័រ ' + M('(\\cdots)^3=\\cos3\\varphi+i\\sin3\\varphi') + ' បាន ' + M('\\cos3\\varphi=4\\cos^3\\varphi-3\\cos\\varphi'), 1),
                 ('ជំនួស ' + M('\\varphi=\\tfrac\\pi9') + ' ៖ ' + M('\\cos\\tfrac\\pi3=4x^3-3x') + ' ដែល ' + M('x=\\cos\\tfrac\\pi9'), 1),
                 ('ដោយ ' + M('\\cos\\tfrac\\pi3=\\tfrac12') + ' នោះ ' + M('4x^3-3x=\\tfrac12') + ' គឺ ' + M('8x^3-6x-1=0') + ' ដូច្នេះ ' + M('x=\\cos\\tfrac\\pi9') + ' ជាឫសនៃសមីការនេះ។', 1)], bloom='Create'))

    wh = roots_of(1, 6)
    C.append(with_img(wr('hard', 's3_root', 'គណនាឫសទី ' + M('6') + ' នៃ ' + M('1') + ' រួចបង្ហាញថាកំពូលរូបភាពរបស់វាបង្កើតបានជាឆកោននិយ័តដែលមានជ្រុងប្រវែង ' + M('1') + ' (ដូចក្នុងរូប) ហើយផលបូកនៃឫសទាំងអស់ស្មើសូន្យ។',
                         [('រូបមន្ត ៖ ' + M('w_k=\\cos\\tfrac{k\\pi}3+i\\sin\\tfrac{k\\pi}3') + ' ដែល ' + M('k=0,\\dots,5'), 1),
                          ('ឫស ៖ ' + M('1,\\ \\tfrac12+\\tfrac{\\sqrt3}2i,\\ -\\tfrac12+\\tfrac{\\sqrt3}2i,\\ -1,\\ -\\tfrac12-\\tfrac{\\sqrt3}2i,\\ \\tfrac12-\\tfrac{\\sqrt3}2i'), 1),
                          ('ជ្រុង ៖ ' + M('w_1-w_0=-\\tfrac12+\\tfrac{\\sqrt3}2i') + ' ហើយ ' + M('|w_1-w_0|=\\sqrt{\\tfrac14+\\tfrac34}=1'), 1),
                          ('ជ្រុងផ្សេងទៀត ៖ ' + M('w_{k+1}-w_k=(\\cos\\tfrac\\pi3+i\\sin\\tfrac\\pi3)^k(w_1-w_0)') + ' មានម៉ូឌុល ' + M('1') + ' ដូចគ្នា ដូច្នេះជ្រុងទាំងប្រាំមួយស្មើ ' + M('1') + ' ហើយមុំស្មើគ្នា គឺឆកោននិយ័ត', 1),
                          ('ផលបូក ៖ ' + M('w_0+w_3=0,\\ w_1+w_4=0,\\ w_2+w_5=0') + ' (ឫសចំណុចឆ្លុះតាមគល់) ដូច្នេះ ' + M('\\sum w_k=0') + '។', 1)], bloom='Create'),
                     fig_roots(6, 1, 78, 0, 'w', ticks=1, extent=1.5)))

    C.append(wr('hard', 's2_trig', 'គេឱ្យ ' + M('z=\\cos\\dfrac\\pi6+i\\sin\\dfrac\\pi6') + '។ ក. កំណត់អាគុយម៉ង់ និងម៉ូឌុលនៃ ' + M('z^k') + ' ចំពោះ ' + M('k=1,2,\\dots,7') + ' ។ ខ. កំណត់តម្លៃនៃ ' + M('S=1+z+z^2+\\dots+z^{11}') + '។ គ. ពន្យល់ដោយធរណីមាត្រថាហេតុអ្វី ' + M('S=0') + '។',
                [('ម៉ូឌុល និងអាគុយម៉ង់ ៖ ' + M('z^k=\\cos\\tfrac{k\\pi}6+i\\sin\\tfrac{k\\pi}6') + ' ដូច្នេះ ' + M('|z^k|=1') + ' និង ' + M('\\arg z^k=\\tfrac{k\\pi}6') + ' (ពិនិត្យ ' + M('z^7') + ' ៖ ' + M('\\tfrac{7\\pi}{6}') + ')', 1),
                 ('ផលបូកស្វ៊ីតធរណីមាត្រ ៖ ' + M('S=\\dfrac{z^{12}-1}{z-1}') + ' ដោយ ' + M('z\\ne1'), 1),
                 ('គណនា ' + M('z^{12}=\\cos2\\pi+i\\sin2\\pi=1') + ' ដូច្នេះ ' + M('S=\\dfrac{1-1}{z-1}=0'), 1),
                 ('ធរណីមាត្រ ៖ ចំណុចរូបភាពនៃ ' + M('1,z,\\dots,z^{11}') + ' ជាកំពូលនៃពហុកោណនិយ័ត ១២ ជ្រុងលើរង្វង់ត្រីកោណមាត្រ', 1),
                 ('ចំណុចនីមួយៗមានចំណុចផ្ទុយតាមគល់ ' + M('z^{k+6}=-z^k') + ' ដូច្នេះវ៉ិចទ័រលុបគ្នាជាគូ ហើយផលបូក ' + M('S=0') + '។', 1)], bloom='Analyze'))

    # =============================================================================== WRITING PISA (5)
    C.append(with_img(wr('pisa', 'pisa_wheel', 'កង់ទេសចរណ៍កាំ ' + M('10\\ \\text{m}') + ' មាន ១២ កាប៊ីនស្ថិតស្មើគ្នា ដែលកាប៊ីនលេខ ' + M('k') + ' ស្ថិតត្រង់ ' + M('w_k=10\\left(\\cos\\tfrac{k\\pi}6+i\\sin\\tfrac{k\\pi}6\\right)') + ' ដូចក្នុងរូប។ ក. រកទីតាំងកាប៊ីនលេខ ' + M('4') + '។ ខ. គណនាចម្ងាយរវាងកាប៊ីនជាប់គ្នា ' + M('w_0') + ' និង ' + M('w_1') + '។',
                         [('កាប៊ីនលេខ ' + M('4') + ' ៖ ' + M('w_4=10\\left(\\cos\\tfrac{2\\pi}3+i\\sin\\tfrac{2\\pi}3\\right)=-5+5\\sqrt3\\,i'), 1),
                          ('ចម្ងាយ ៖ ' + M('w_1-w_0=10\\left(\\tfrac{\\sqrt3}2+\\tfrac12i\\right)-10=\\left(5\\sqrt3-10\\right)+5i'), 1),
                          ('ម៉ូឌុល ៖ ' + M('|w_1-w_0|^2=(5\\sqrt3-10)^2+25=75-100\\sqrt3+100+25=200-100\\sqrt3'), 1),
                          ('ដូច្នេះ ' + M('|w_1-w_0|=10\\sqrt{2-\\sqrt3}') + ' ហើយ ' + M('\\sqrt{2-\\sqrt3}=\\tfrac{\\sqrt6-\\sqrt2}2') + ' គឺ ' + M('=5(\\sqrt6-\\sqrt2)'), 1),
                          ('តម្លៃប្រហែល ៖ ' + M('5(2{,}449-1{,}414)\\approx5{,}18\\ \\text{m}') + ' (ត្រូវនឹងជ្រុងពហុកោណនិយ័ត ១២ ជ្រុងកាំ ' + M('10') + ')។', 1)], bloom='Analyze'),
                     fig_roots(12, 10, 17, 0, 'w', ticks=100, poly=False, label_every=1, grid=False, extent=12.5)))

    C.append(with_img(wr('pisa', 'pisa_square', 'ស្ថានីយ៍ទូរគមនាគមន៍បួនត្រូវដាក់ស្មើគ្នាលើរង្វង់កាំ ' + M('6\\ \\text{km}') + ' ជុំវិញប៉មមួយ ដោយស្ថានីយ៍ទី ១ នៅត្រង់ ' + M('6') + ' (ឫសទី ' + M('4') + ' នៃ ' + M('1296') + ') ដូចក្នុងរូប។ ក. រកទីតាំងស្ថានីយ៍ទាំងបួន។ ខ. គណនាចម្ងាយរវាងស្ថានីយ៍ជាប់គ្នា និងរវាងស្ថានីយ៍ឆ្លងកាត់ប៉ម។',
                         [('រូបមន្តឫស ៖ ' + M('1296=1296(\\cos0+i\\sin0)') + ' ដូច្នេះ ' + M('w_k=6\\left(\\cos\\tfrac{k\\pi}2+i\\sin\\tfrac{k\\pi}2\\right)'), 1),
                          ('ទីតាំង ៖ ' + M('w_0=6,\\ w_1=6i,\\ w_2=-6,\\ w_3=-6i'), 1),
                          ('ស្ថានីយ៍ជាប់គ្នា ៖ ' + M('|w_1-w_0|=|-6+6i|=6\\sqrt2\\approx8{,}49\\ \\text{km}'), 1),
                          ('ស្ថានីយ៍ឆ្លងកាត់ប៉ម ៖ ' + M('|w_2-w_0|=|-12|=12\\ \\text{km}') + ' (អង្កត់ផ្ចិត)', 1),
                          ('ផ្ទៀងផ្ទាត់ ៖ ' + M('(6\\sqrt2)^2+(6\\sqrt2)^2=144=12^2') + ' ស្របតាមទ្រឹស្តីបទពីតាគ័រ ដូច្នេះស្ថានីយ៍បង្កើតបានជាការ៉េ។', 1)], bloom='Apply'),
                     fig_roots(4, 6, 24, 0, 'S', ticks=2, extent=7.8)))

    G = cis(s2, Rational(1, 12))
    C.append(wr('pisa', 'pisa_filter', 'ដំណាក់កាលតម្រងមួយមានការឆ្លើយតប ' + M('G=\\sqrt2\\left(\\cos\\dfrac\\pi{12}+i\\sin\\dfrac\\pi{12}\\right)') + ' ។ ដំណាក់កាលដូចគ្នា ៦ តភ្ជាប់គ្នា។ ក. គណនាការឆ្លើយតបសរុប ' + M('G^6') + ' ជាទម្រង់ត្រីកោណមាត្រ។ ខ. សរសេរជាទម្រង់ ' + M('a+bi') + ' ហើយបញ្ជាក់អំព្លីទុត និងផាស។ គ. ផ្ទៀងផ្ទាត់ជាមួយ ' + M('G^2') + ' រួចលើកស្វ័យគុណទី ' + M('3') + '។',
                [('រូបមន្តដឺម័រ ៖ ' + M('G^6=(\\sqrt2)^6\\left(\\cos\\tfrac{6\\pi}{12}+i\\sin\\tfrac{6\\pi}{12}\\right)'), 1),
                 ('គណនា ៖ ' + M('(\\sqrt2)^6=8') + ' ហើយ ' + M('\\tfrac{6\\pi}{12}=\\tfrac\\pi2') + ' ដូច្នេះ ' + M('G^6=8\\left(\\cos\\tfrac\\pi2+i\\sin\\tfrac\\pi2\\right)'), 1),
                 ('ទម្រង់ពីជគណិត ៖ ' + M('G^6=8i'), 1),
                 ('អំព្លីទុត ' + M('|G^6|=8') + ' ហើយផាស ' + M('\\tfrac\\pi2=90^\\circ'), 1),
                 ('ផ្ទៀងផ្ទាត់ ៖ ' + M('G^2=2\\left(\\cos\\tfrac\\pi6+i\\sin\\tfrac\\pi6\\right)=\\sqrt3+i') + ' ហើយ ' + M('(G^2)^3=(\\sqrt3+i)^3=8i') + ' (ព្រោះ ' + M('2^3\\left(\\cos\\tfrac\\pi2+i\\sin\\tfrac\\pi2\\right)') + ') ស្របគ្នា។', 1)], bloom='Analyze'))

    C.append(wr('pisa', 'pisa_antenna', 'ចុងអង់តែនប្រវែង ' + M('2\\ \\text{m}') + ' ចាប់ផ្ដើមតាមអ័ក្សពិត ' + M('z_0=2') + ' ហើយវិលច្រាសទ្រនិចនាឡិការៀងរាល់ម៉ោងបានម៉ុំ ' + M('\\dfrac\\pi6') + ' ជុំវិញគល់ ' + M('O') + '។ ក្រោយ ' + M('n') + ' ម៉ោង ទីតាំងគឺ ' + M('z_n=2\\left(\\cos\\tfrac\\pi6+i\\sin\\tfrac\\pi6\\right)^n') + '។ ក. រក ' + M('z_3') + ' និង ' + M('z_4') + '។ ខ. ក្រោយប៉ុន្មានម៉ោងទើបចុងអង់តែនត្រលប់ទីតាំងដើមជាលើកដំបូង ? គ. តើក្នុង ' + M('12') + ' ម៉ោង ចុងអង់តែនឆ្លងកាត់ឫសទី ' + M('12') + ' នៃអ្វី ?',
                [('រូបមន្តដឺម័រ ៖ ' + M('z_n=2\\left(\\cos\\tfrac{n\\pi}6+i\\sin\\tfrac{n\\pi}6\\right)'), 1),
                 (M('z_3=2\\left(\\cos\\tfrac\\pi2+i\\sin\\tfrac\\pi2\\right)=2i') + ' និង ' + M('z_4=2\\left(\\cos\\tfrac{2\\pi}3+i\\sin\\tfrac{2\\pi}3\\right)=-1+\\sqrt3\\,i'), 1),
                 ('ត្រលប់ដើម ៖ ' + M('z_n=2') + ' ពេល ' + M('\\tfrac{n\\pi}6=2\\pi') + ' ដូច្នេះ ' + M('n=12') + ' ម៉ោង', 1),
                 ('គ្រប់ ' + M('n') + ' ៖ ' + M('z_n^{12}=2^{12}(\\cos2n\\pi+i\\sin2n\\pi)=2^{12}=4096'), 1),
                 ('សន្និដ្ឋាន ៖ ទីតាំងទាំង ១២ ជាឫសទី ' + M('12') + ' នៃ ' + M('4096') + ' ហើយស្ថិតលើរង្វង់កាំ ' + M('2') + ' ជាកំពូលនៃពហុកោណនិយ័ត ១២ ជ្រុង។', 1)], bloom='Analyze'))

    C.append(wr('pisa', 'pisa_spiral', 'ជណ្ដើរវង់មួយមានជំហាន ដែលជំហាននីមួយៗបង្វិលទិសច្រាសទ្រនិចនាឡិកាម៉ុំ ' + M('\\dfrac\\pi4') + ' ហើយពង្រីកចម្ងាយពីគល់ ' + M('O') + ' ឱ្យធំជា ' + M('\\sqrt2') + ' ដង។ ចំណុចជំហានទី ' + M('n') + ' តាងដោយ ' + M('z_n=(1+i)^n') + ' (ជំហានទី ០ ជា ' + M('z_0=1') + ')។ ក. បង្ហាញថា ' + M('1+i') + ' បង្វិល ' + M('\\tfrac\\pi4') + ' និងពង្រីក ' + M('\\sqrt2') + '។ ខ. រក ' + M('z_4') + ' និង ' + M('z_8') + '។ គ. រកជំហានតូចបំផុតដែលចម្ងាយពី ' + M('O') + ' លើស ' + M('100') + '។',
                [('ទម្រង់ត្រីកោណមាត្រ ៖ ' + M('1+i=\\sqrt2\\left(\\cos\\tfrac\\pi4+i\\sin\\tfrac\\pi4\\right)') + ' ដូច្នេះគុណនឹង ' + M('1+i') + ' បង្វិល ' + M('\\tfrac\\pi4') + ' ហើយពង្រីក ' + M('\\sqrt2') + ' ដង', 1),
                 ('រូបមន្តដឺម័រ ៖ ' + M('z_n=(\\sqrt2)^n\\left(\\cos\\tfrac{n\\pi}4+i\\sin\\tfrac{n\\pi}4\\right)'), 1),
                 (M('z_4=4(\\cos\\pi+i\\sin\\pi)=-4') + ' ហើយ ' + M('z_8=16(\\cos2\\pi+i\\sin2\\pi)=16'), 1),
                 ('ចម្ងាយ ' + M('|z_n|=2^{n/2}') + ' ត្រូវការ ' + M('2^{n/2}>100') + ' គឺ ' + M('n>2\\log_2100\\approx13{,}29'), 1),
                 ('ផ្ទៀងផ្ទាត់ ៖ ' + M('n=13') + ' ឱ្យ ' + M('2^{6{,}5}\\approx90{,}5<100') + ' ហើយ ' + M('n=14') + ' ឱ្យ ' + M('2^7=128>100') + ' ដូច្នេះជំហានតូចបំផុតគឺ ' + M('n=14') + '។', 1)], bloom='Create'))

    return C


def verify():
    """independent re-derivation of the claims above, with plain complex numbers."""
    n = 0
    z = lambda a, b: complex(a, b)
    def close(x, y, e=1e-8): return abs(x - y) < e
    r3, r2 = math.sqrt(3), math.sqrt(2)
    cis_ = lambda r, p: r * cmath.exp(1j * p)
    # powers
    assert close(cmath.exp(1j * math.pi / 6) ** 12, 1) and close((1 + 1j) ** 8, 16) and close((-1 + 1j) ** 4, -4); n += 3
    assert close((-1 + 1j * r3) ** 3, 8) and all(not close(w ** 3, 8) for w in (1 + 1j * r3, 2j, 1 + 1j)); n += 2
    assert close((r3 + 1j) ** 6, -64) and close((1 - 1j) ** 10, -32j); n += 2
    v = (-r3 + 1j) ** 13
    assert close(v, z(-4096 * r3, 4096)); n += 1
    for k in (1, 2, 3, 4):
        assert close(((1 + 1j) / (1 - 1j)) ** (2 * k), (-1) ** k); n += 1
    assert close((1 + 1j * r3) ** 5 + (1 - 1j * r3) ** 5, 32); n += 1
    assert close((1 + 1j) ** 12, -64); n += 1
    # cos 3x, sin 3x identities, numerically
    for x in (0.3, 1.1, 2.4):
        assert close(math.cos(3 * x), 4 * math.cos(x) ** 3 - 3 * math.cos(x)) and close(math.sin(3 * x), 3 * math.sin(x) - 4 * math.sin(x) ** 3); n += 2
    assert close(4 * math.cos(math.pi / 9) ** 3 - 3 * math.cos(math.pi / 9), 0.5) and close(8 * math.cos(math.pi / 9) ** 3 - 6 * math.cos(math.pi / 9) - 1, 0); n += 2
    # (1+sin+i cos)/(1+sin-i cos)
    for ph in (0.3, 1.0, 2.0):
        q = z(1 + math.sin(ph), math.cos(ph)) / z(1 + math.sin(ph), -math.cos(ph))
        assert close(q, cmath.exp(1j * (math.pi / 2 - ph))) and close(q ** 5, cmath.exp(5j * (math.pi / 2 - ph))); n += 2
    # student error counterexample
    assert close(cmath.exp(1j * math.pi / 4) ** 2, 1j) and close(math.cos(math.pi / 4) ** 2 + 1j * math.sin(math.pi / 4) ** 2, 0.5 + 0.5j); n += 2
    # roots
    def roots(w, m): return [abs(w) ** (1 / m) * cmath.exp(1j * (cmath.phase(w) + 2 * math.pi * k) / m) for k in range(m)]
    assert all(close(w ** 4, 16) for w in roots(16, 4)); n += 1
    assert any(close(w, 2j) for w in roots(-64, 6)) and close((2j) ** 6, -64) and all(not close(w ** 6, -64) for w in (2, r3, 1 + 1j)); n += 2
    zq = z(-8, -8 * r3)
    r4 = roots(zq, 4)
    lesson_roots = [cis_(2, (4 * math.pi / 3 + 2 * math.pi * k) / 4) for k in range(4)]      # the lesson's formula with phi = 4pi/3
    assert all(close(w ** 4, zq) for w in lesson_roots); n += 4
    assert [round(cmath.phase(w) / math.pi * 6) % 12 for w in lesson_roots] == [2, 5, 8, 11]; n += 1     # pi/3, 5pi/6, 4pi/3, 11pi/6
    assert all(any(close(w, v) for v in r4) for w in lesson_roots); n += 1
    assert close(sum(roots(1, 3)), 0) and close(roots(1, 3)[0] * roots(1, 3)[1] * roots(1, 3)[2], 1); n += 2
    assert all(close((w - 2) ** 3, 1) for w in (3, z(1.5, r3 / 2), z(1.5, -r3 / 2))); n += 3
    z0 = r2 * (1 + 1j)
    assert close(z0 ** 4, -16) and not close(z0 ** 4, 16) and not close(z0 ** 4, -4) and not close(z0 ** 2, 4); n += 3
    # z^6 + 2 z^3 + 1 : number of distinct roots
    import itertools
    rts = [w for w in roots(-1, 3)]
    assert all(close(w ** 6 + 2 * w ** 3 + 1, 0) for w in rts) and len({(round(w.real, 6), round(w.imag, 6)) for w in rts}) == 3; n += 2
    # geometric sum and 12-gon facts
    zz = cmath.exp(1j * math.pi / 6)
    assert close(sum(zz ** k for k in range(12)), 0) and close(zz ** 12, 1); n += 2
    assert close(abs(cis_(10, math.pi / 6) - 10), 5 * (math.sqrt(6) - r2)) and close(10 * cmath.exp(2j * math.pi / 3 * 1), z(-5, 5 * r3)); n += 2
    assert close(cis_(10, 3 * math.pi / 6), 10j); n += 1
    # three relay stations, four stations, lamps
    w3 = roots(216, 3)
    assert all(close(abs(w3[i] - w3[j]), 6 * r3) for i, j in itertools.combinations(range(3), 2)) and close(w3[1], z(-3, 3 * r3)); n += 2
    w4 = [6 * 1j ** k for k in range(4)]
    assert all(close(w ** 4, 1296) for w in w4) and close(abs(w4[1] - w4[0]), 6 * r2) and close(abs(w4[2] - w4[0]), 12); n += 3
    assert close(cmath.phase(cis_(2, 4 * math.pi / 5)), 4 * math.pi / 5) and close(cis_(2, 4 * math.pi / 5) ** 5, 32); n += 2
    # robot, filter, antenna, spiral, hexagon
    assert close(cmath.exp(1j * math.pi / 12) ** 24, 1) and all(not close(cmath.exp(1j * math.pi / 12) ** m, 1) for m in range(1, 24)); n += 2
    G = cis_(r2, math.pi / 12)
    assert close(G ** 6, 8j) and close((G ** 2) ** 3, 8j) and close(G ** 2, z(r3, 1)); n += 3
    assert close(2 * cmath.exp(1j * math.pi / 6) ** 3, 2j) and close(2 * cmath.exp(1j * math.pi / 6) ** 4, z(-1, r3)) and close(2 * cmath.exp(1j * math.pi / 6) ** 12, 2); n += 3
    assert close((1 + 1j) ** 4, -4) and close((1 + 1j) ** 8, 16) and abs((1 + 1j) ** 13) < 100 < abs((1 + 1j) ** 14); n += 3
    h6 = roots(1, 6)
    assert close(sum(h6), 0) and all(close(abs(h6[(k + 1) % 6] - h6[k]), 1) for k in range(6)); n += 2
    p5 = roots(-1 + 1j, 5)
    assert close(abs(p5[0]), 2 ** 0.1) and [round(cmath.phase(w) / math.pi * 20) % 40 for w in p5] == [3, 11, 19, 27, 35]; n += 2
    assert close(abs(cmath.exp(1j * 1) - 1), 2 * math.sin(0.5)); n += 1
    return n
