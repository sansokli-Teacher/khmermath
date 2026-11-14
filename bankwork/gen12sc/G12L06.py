# -*- coding: utf-8 -*-
"""
KhmerMath Question Bank: Grade 12 Science (SC)
Chapter 3: ដេរីវេនៃអនុគមន៍
Lesson 1: ដេរីវេនៃអនុគមន៍
Reference textbook: Lesson/G12/SC/C3-L1.tex

Target matrix: MCQ easy10/medium14/hard7/pisa5 + writing easy1/medium4/hard4/pisa5 = 50, a Bloom level on each.
Every derivative answer is a hand-written closed form that is checked, at generation time, against mpmath's numerical
derivative of the original function at several points (and each wrong option is checked to differ from it);
implicit-differentiation, root and rate claims are re-derived with plain numerics.  Figures and helpers come from G12L04.
"""
import sys, os, math
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.dirname(__file__))
from lib import *
import svgkit as K
import mpmath as mp
import G12L04 as P
from G12L04 import G, curve, x
from sympy import (Symbol, Rational, sqrt, simplify, latex, sin, cos, tan, exp, log, asin, acos, atan, acot, N, pi, cbrt, lambdify, diff, S, Function)

LESSON = 'ដេរីវេនៃអនុគមន៍'
CHAPTER = 'ជំពូកទី 3 : ដេរីវេនៃអនុគមន៍'
GRADE = '12SC'
TARGET = P.TARGET
S1 = 'និយមន័យនិងដេរីវេនៃអនុគមន៍បណ្ដាក់'
S2 = 'ដេរីវេនៃអនុគមន៍ត្រីកោណមាត្រ'
S3 = 'ដេរីវេនៃអនុគមន៍ច្រាសត្រីកោណមាត្រ'
S4 = 'ដេរីវេទី 2 និងដេរីវេអាប់លីស៊ីត'
S5 = 'ដេរីវេលំដាប់ខ្ពស់'
TOPIC_MAP = {'s1': S1, 's2': S2, 's3': S3, 's4': S4, 's5': S5,
             'p_area': S1, 'p_speed': S1, 'p_cost': S1, 'p_pend': S2, 'p_angle': S3,
             'p_fence': S4, 'p_motion': S5, 'p_chain': S1, 'p_drone': S3, 'p_osc': S5}
_L = P._L
CNT = [0]
PTS = (mp.mpf('0.37'), mp.mpf('0.61'), mp.mpf('0.83'))


def chk(fn):
    r = fn()
    rs = list(r) if isinstance(r, tuple) else [r]
    assert all(rs), ('numeric check failed', rs)
    CNT[0] += len(rs)


def lam(e):
    return lambdify(x, e, 'mpmath')


def dnum(f_expr, t, n=1):
    mp.mp.dps = 40
    return mp.diff(lam(f_expr), t, n)


def with_img(q, svg):
    q['img'] = svg
    return q


def dq(level, sec, f, ans, wrongs, sol, bloom, lead='គណនាដេរីវេនៃ', name="y", pts=PTS, n=1, img=None, tail=''):
    """derivative MCQ: `ans` (a closed form) must equal the numeric derivative of f at every test point, each wrong must not."""
    mp.mp.dps = 40
    fa = lam(ans)
    for t in pts:
        assert abs(dnum(f, t, n) - fa(t)) < mp.mpf('1e-12') * max(1, abs(fa(t))), ('wrong closed form', f, ans, t)
    CNT[0] += len(pts)
    ws = []
    for w in wrongs:
        fw = lam(w)
        assert any(abs(fw(t) - fa(t)) > mp.mpf('1e-6') for t in pts), ('a wrong option equals the answer', f, w)
        ws.append(M(_L(w)))
    label = (name + '(x)=') if name in ('f', 'g') else (name + '=')
    q = mcq(level, sec, lead + ' ' + M(label + _L(f)) + tail + '។', M(_L(ans)), ws, sol, bloom)
    if img:
        q['img'] = img
    return q


# ----------------------------------------------------------------------------- figures
def fig_parab():
    kx, ky = 1.35, 0.0215
    fn = lambda t: 200 * t - t * t
    return G(300, 230, [(curve(fn, kx, ky), 0, 200 * kx, K.BLUE)], xt=[(kx * v, str(v)) for v in (50, 100, 150, 200)], yt=[(ky * v, str(v)) for v in (5000, 10000)],
             dots=[(100 * kx, 10000 * ky, '', 0, 0, K.RED)], segs=[(100 * kx, 0, 100 * kx, 10000 * ky, K.AXIS, True), (0, 10000 * ky, 100 * kx, 10000 * ky, K.AXIS, True)], xlabel='x', ylabel='A', pad=46)


def fig_motion():
    kx, ky = 60.0, 14.0
    fn = lambda t: t ** 3 - 6 * t ** 2 + 9 * t
    return G(300, 190, [(curve(fn, kx, ky), 0, 4.0 * kx, K.BLUE)], xt=[(kx * v, str(v)) for v in (1, 2, 3, 4)], yt=[(ky * v, str(v)) for v in (4, 8, 12)],
             dots=[(1 * kx, 4 * ky, '', 0, 0, K.RED), (3 * kx, 0, '', 0, 0, K.RED)], xlabel='t', ylabel='s')


def fig_cost_tangent():
    kx, ky = 13.0, 2.4
    fn = lambda t: 0.5 * t * t + 3 * t
    tg = lambda t: 56 + 11 * (t - 8)
    return G(300, 220, [(curve(fn, kx, ky), 0, 14 * kx, K.BLUE), (curve(tg, kx, ky), 2.5 * kx, 13 * kx, K.GREEN)], xt=[(kx * v, str(v)) for v in (4, 8, 12)],
             yt=[(ky * v, str(v)) for v in (20, 56)], dots=[(8 * kx, 56 * ky, '', 0, 0, K.RED)],
             segs=[(8 * kx, 0, 8 * kx, 56 * ky, K.AXIS, True), (0, 56 * ky, 8 * kx, 56 * ky, K.AXIS, True)], xlabel='x', ylabel='C')


def fig_pendulum():
    kx, ky = 30.0, 150.0
    fn = lambda t: 0.3 * math.cos(2 * t)
    om = lambda t: -0.6 * math.sin(2 * t)
    return G(320, 190, [(curve(fn, kx, ky), 0, 10 * kx, K.BLUE), (curve(om, kx, ky), 0, 10 * kx, K.RED)], yo=95, xt=[(kx * v, str(v)) for v in (2, 4, 6, 8, 10)],
             yt=[(ky * 0.3, '0,3'), (-ky * 0.3, '−0,3')], xlabel='t', ylabel='', notes=[(10 * kx, 0.3 * ky, 'θ', 5, 0, K.BLUE, True), (10 * kx, 0.6 * ky * 0.0 - 5, 'ω', 5, 14, K.RED, True)])


def fig_angle():
    kx, ky = 0.9, 105.0
    fn = lambda t: math.atan(30.0 / t) if t > 0 else math.pi / 2
    return G(300, 200, [(curve(lambda t: math.atan(30.0 / t) if t > 0 else None, kx, ky), 3, 300, K.BLUE)], xt=[(kx * v, str(v)) for v in (50, 100, 150, 200, 250)], yt=[(ky * 0.5, '0,5'), (ky * 1.0, '1')],
             dots=[(40 * kx, math.atan(30 / 40) * ky, '', 0, 0, K.RED)], xlabel='x', ylabel='θ')


def fig_chain():
    return fig_cost_tangent()


def fig_angle_atan():
    kx, ky = 0.9, 105.0
    fn = lambda t: math.atan(t / 10.0)
    return G(300, 200, [(curve(fn, kx, ky), 0, 300, K.BLUE)], xt=[(kx * v, str(v)) for v in (50, 100, 150, 200, 250)], yt=[(ky * 0.5, '0,5'), (ky * 1.0, '1'), (ky * 1.5, '1,5')],
             dots=[(10 * kx, math.atan(1) * ky, '', 0, 0, K.RED)], xlabel='x', ylabel='θ')


def fig_osc():
    return fig_pendulum()


# ----------------------------------------------------------------------------- candidates
def cands():
    C = []
    X = x
    # ============================================================ MCQ EASY (10)
    f = 3 * X ** 2 - 5 * X + 1
    C.append(dq('easy', 's1', f, 6 * X - 5, [6 * X, 3 * X - 5, 6 * X + 5], 'ដេរីវេពហុធា ៖ ' + M('(3x^2)\'=6x') + ', ' + M('(-5x)\'=-5') + ' ដូច្នេះ ' + M('f\'(x)=6x-5') + ' (ហើយ ' + M('f\'(2)=7') + ')។', 'Apply', name='f'))
    f = (X ** 2 + 1) ** 3
    C.append(dq('easy', 's1', f, 6 * X * (X ** 2 + 1) ** 2, [3 * (X ** 2 + 1) ** 2, 6 * X * (X ** 2 + 1) ** 3, 3 * X * (X ** 2 + 1) ** 2],
                'តាង ' + M('u=x^2+1') + ' ៖ ' + M('y\'=3u^2\\cdot u\'=3(x^2+1)^2\\cdot2x=6x(x^2+1)^2') + '។', 'Apply'))
    f = sin(3 * X)
    C.append(dq('easy', 's2', f, 3 * cos(3 * X), [cos(3 * X), -3 * cos(3 * X), 3 * sin(3 * X)], M('(\\sin u)\'=u\'\\cos u') + ' ជាមួយ ' + M('u=3x') + ' ៖ ' + M('y\'=3\\cos3x') + '។', 'Remember'))
    f = cos(2 * X + 1)
    C.append(dq('easy', 's2', f, -2 * sin(2 * X + 1), [2 * sin(2 * X + 1), -sin(2 * X + 1), -2 * cos(2 * X + 1)], M('(\\cos u)\'=-u\'\\sin u') + ' ជាមួយ ' + M('u=2x+1') + ' ៖ ' + M('y\'=-2\\sin(2x+1)') + '។', 'Remember'))
    f = tan(X)
    C.append(dq('easy', 's2', f, 1 / cos(X) ** 2, [-1 / sin(X) ** 2, 1 / sin(X) ** 2, -1 / cos(X) ** 2], M('(\\tan x)\'=\\dfrac1{\\cos^2x}=1+\\tan^2x') + '។', 'Remember'))
    f = asin(X)
    C.append(dq('easy', 's3', f, 1 / sqrt(1 - X ** 2), [-1 / sqrt(1 - X ** 2), 1 / (1 + X ** 2), 1 / sqrt(1 + X ** 2)], M('\\dfrac{d}{dx}(\\sin^{-1}x)=\\dfrac1{\\sqrt{1-x^2}}') + '។', 'Remember', pts=(mp.mpf('0.2'), mp.mpf('0.5'), mp.mpf('0.7'))))
    f = atan(X)
    C.append(dq('easy', 's3', f, 1 / (1 + X ** 2), [1 / (1 - X ** 2), 1 / sqrt(1 - X ** 2), -1 / (1 + X ** 2)], M('\\dfrac{d}{dx}(\\tan^{-1}x)=\\dfrac1{1+x^2}') + '។', 'Remember'))
    f = sqrt(X ** 2 - 1)
    C.append(dq('easy', 's1', f, X / sqrt(X ** 2 - 1), [1 / (2 * sqrt(X ** 2 - 1)), 2 * X / sqrt(X ** 2 - 1), X / sqrt(X ** 2 + 1)], M('(\\sqrt u)\'=\\dfrac{u\'}{2\\sqrt u}') + ' ជាមួយ ' + M('u=x^2-1') + ' ៖ ' + M('\\dfrac{2x}{2\\sqrt{x^2-1}}=\\dfrac x{\\sqrt{x^2-1}}') + '។',
                'Apply', pts=(mp.mpf('1.3'), mp.mpf('2.1'), mp.mpf('3.7'))))
    f = X ** 4 - 3 * X ** 2
    C.append(dq('easy', 's4', f, 12 * X ** 2 - 6, [4 * X ** 3 - 6 * X, 12 * X ** 2 - 6 * X, 12 * X ** 3], M('y\'=4x^3-6x') + ' ហើយ ' + M('y\'\'=12x^2-6') + '។', 'Apply', lead='គណនាដេរីវេទី ២ នៃ', n=2))
    f = 1 / X
    C.append(dq('easy', 's5', f, -1 / X ** 2, [1 / X ** 2, -1 / X, 1 / X], M('\\left(x^{-1}\\right)\'=-x^{-2}=-\\dfrac1{x^2}') + '។', 'Remember', name='f'))

    # ============================================================ MCQ MEDIUM (14)
    f = (3 * X ** 2 + 5 * X - 2) ** 3
    C.append(dq('medium', 's1', f, 3 * (3 * X ** 2 + 5 * X - 2) ** 2 * (6 * X + 5), [3 * (3 * X ** 2 + 5 * X - 2) ** 2, (3 * X ** 2 + 5 * X - 2) ** 2 * (6 * X + 5), 3 * (3 * X ** 2 + 5 * X - 2) ** 3 * (6 * X + 5)],
                'តាង ' + M('u=3x^2+5x-2') + ' ៖ ' + M('y\'=3u^2\\cdot u\'=3(3x^2+5x-2)^2(6x+5)') + '។', 'Apply'))
    f = X ** 2 * cos(3 * X + 1)
    C.append(dq('medium', 's2', f, 2 * X * cos(3 * X + 1) - 3 * X ** 2 * sin(3 * X + 1), [2 * X * cos(3 * X + 1) + 3 * X ** 2 * sin(3 * X + 1), 2 * X * cos(3 * X + 1) - X ** 2 * sin(3 * X + 1), -6 * X * sin(3 * X + 1)],
                'ដេរីវេផលគុណ ' + M('(uv)\'=u\'v+uv\'') + ' ៖ ' + M('2x\\cos(3x+1)+x^2\\cdot(-3\\sin(3x+1))') + '។', 'Apply', name='f'))
    f = X ** 3 * tan(X)
    C.append(dq('medium', 's2', f, 3 * X ** 2 * tan(X) + X ** 3 / cos(X) ** 2, [3 * X ** 2 / cos(X) ** 2, 3 * X ** 2 * tan(X) - X ** 3 / cos(X) ** 2, 3 * X ** 2 * tan(X) + X ** 3 * tan(X) ** 2], M('(uv)\'=u\'v+uv\'') + ' ជាមួយ ' + M('u=x^3,\\ v=\\tan x') + '។', 'Apply', name='f'))
    f = 3 * cbrt(X ** 2 - 3 * X + 1)
    C.append(dq('medium', 's1', f, (2 * X - 3) / (X ** 2 - 3 * X + 1) ** Rational(2, 3), [(2 * X - 3) / (X ** 2 - 3 * X + 1) ** Rational(1, 3), (2 * X - 3) / (3 * (X ** 2 - 3 * X + 1) ** Rational(2, 3)), 3 * (2 * X - 3) / (X ** 2 - 3 * X + 1) ** Rational(2, 3)],
                'សរសេរ ' + M('y=3u^{1/3}') + ' ជាមួយ ' + M('u=x^2-3x+1') + ' ៖ ' + M('y\'=3\\cdot\\tfrac13u^{-2/3}u\'=\\dfrac{2x-3}{(x^2-3x+1)^{2/3}}') + '។', 'Apply', pts=(mp.mpf('2.4'), mp.mpf('3.1'), mp.mpf('4.2'))))
    f = (2 * X - sin(X)) ** 3
    C.append(dq('medium', 's2', f, 3 * (2 * X - sin(X)) ** 2 * (2 - cos(X)), [3 * (2 * X - sin(X)) ** 2 * (2 + cos(X)), 3 * (2 * X - sin(X)) ** 2, (2 * X - sin(X)) ** 2 * (2 - cos(X))], M('y\'=3u^2u\'') + ' ជាមួយ ' + M('u=2x-\\sin x') + ' ៖ ' + M('u\'=2-\\cos x') + '។', 'Apply'))
    f = X * asin(X)
    C.append(dq('medium', 's3', f, asin(X) + X / sqrt(1 - X ** 2), [asin(X) - X / sqrt(1 - X ** 2), X / sqrt(1 - X ** 2), asin(X) + 1 / sqrt(1 - X ** 2)], M('(uv)\'=u\'v+uv\'=\\sin^{-1}x+\\dfrac x{\\sqrt{1-x^2}}') + '។', 'Apply', pts=(mp.mpf('0.2'), mp.mpf('0.5'), mp.mpf('0.7'))))
    f = acos(2 * X)
    C.append(dq('medium', 's3', f, -2 / sqrt(1 - 4 * X ** 2), [2 / sqrt(1 - 4 * X ** 2), -1 / sqrt(1 - 4 * X ** 2), -2 / sqrt(1 - 2 * X ** 2)], M('(\\cos^{-1}u)\'=-\\dfrac{u\'}{\\sqrt{1-u^2}}') + ' ជាមួយ ' + M('u=2x') + '។', 'Apply', pts=(mp.mpf('0.1'), mp.mpf('0.2'), mp.mpf('0.4'))))
    f = atan(5 * X)
    C.append(dq('medium', 's3', f, 5 / (1 + 25 * X ** 2), [1 / (1 + 25 * X ** 2), 5 / (1 + 5 * X ** 2), 5 / (1 - 25 * X ** 2)], M('(\\tan^{-1}u)\'=\\dfrac{u\'}{1+u^2}') + ' ជាមួយ ' + M('u=5x') + '។', 'Apply'))
    f = sin(X ** 2) ** 2
    C.append(dq('medium', 's2', f, 2 * X * sin(2 * X ** 2), [2 * sin(X ** 2) * cos(X ** 2), 2 * sin(X ** 2), 4 * X * sin(X ** 2) * cos(2 * X ** 2)], M('y=[\\sin(x^2)]^2') + ' ៖ ' + M('y\'=2\\sin(x^2)\\cos(x^2)\\cdot2x=2x\\sin2x^2') + '។', 'Analyze', name='f'))
    f = tan(2 * X ** 3 - 5 * X)
    C.append(dq('medium', 's2', f, (6 * X ** 2 - 5) / cos(2 * X ** 3 - 5 * X) ** 2, [(6 * X ** 2 - 5) / sin(2 * X ** 3 - 5 * X) ** 2, 1 / cos(2 * X ** 3 - 5 * X) ** 2, (2 * X ** 3 - 5 * X) / cos(2 * X ** 3 - 5 * X) ** 2],
                M('(\\tan u)\'=\\dfrac{u\'}{\\cos^2u}') + ' ជាមួយ ' + M('u=2x^3-5x') + '។', 'Apply', name='f', pts=(mp.mpf('0.2'), mp.mpf('0.4'), mp.mpf('0.6'))))
    f = X ** 2 / (X + 1)
    C.append(dq('medium', 's4', f, 2 / (X + 1) ** 3, [(X ** 2 + 2 * X) / (X + 1) ** 2, 2 / (X + 1) ** 2, 2 * X / (X + 1) ** 3], M('g(x)=x-1+\\dfrac1{x+1}') + ' ដូច្នេះ ' + M('g\'\'(x)=\\dfrac2{(x+1)^3}') + '។', 'Apply', lead='គណនាដេរីវេទី ២ នៃ', name='g', n=2))
    f = sin(X) / X
    C.append(dq('medium', 's1', f, (X * cos(X) - sin(X)) / X ** 2, [cos(X) / X ** 2, (cos(X) - sin(X)) / X ** 2, cos(X) / X - sin(X) / X ** 2 * X], M('\\left(\\dfrac uv\\right)\'=\\dfrac{u\'v-uv\'}{v^2}=\\dfrac{x\\cos x-\\sin x}{x^2}') + '។', 'Apply', name='f'))
    f = sin(2 * X)
    C.append(dq('medium', 's5', f, 16 * sin(2 * X), [8 * sin(2 * X), 16 * cos(2 * X), -16 * sin(2 * X)], M('y\'=2\\cos2x') + ', ' + M('y\'\'=-4\\sin2x') + ', ' + M('y\'\'\'=-8\\cos2x') + ', ' + M('y^{(4)}=16\\sin2x') + '។', 'Analyze', lead='គណនាដេរីវេទី ៤ នៃ', n=4))
    # implicit slope at a point
    chk(lambda: (abs(-mp.sqrt(2) / mp.sqrt(2) - (-1)) < 1e-12,))
    C.append(mcq('medium', 's4', 'គេឱ្យសមីការ ' + M('x^2+y^2=4') + '។ គណនា ' + M('\\dfrac{dy}{dx}') + ' ត្រង់ចំណុច ' + M('(\\sqrt2,\\ \\sqrt2)') + '។', M('-1'), [M('1'), M('0'), M('-\\sqrt2')],
                 M('2x+2yy\'=0') + ' ដូច្នេះ ' + M('y\'=-\\dfrac xy=-\\dfrac{\\sqrt2}{\\sqrt2}=-1') + '។', 'Apply'))

    # ============================================================ MCQ HARD (7)
    # y'' for xy + y^2 - x^2 = 5 at (1, 2)
    chk(lambda: (abs(50 / mp.mpf(1 + 4) ** 3 - mp.mpf(2) / 5) < 1e-12, abs((2 * 1 - 2) / mp.mpf(1 + 4)) < 1e-12))
    yy = lambda xx: mp.findroot(lambda yv: xx * yv + yv ** 2 - xx ** 2 - 5, 2)
    chk(lambda: (abs(mp.diff(yy, mp.mpf(1)) - 0) < 1e-8, abs(mp.diff(yy, mp.mpf(1), 2) - mp.mpf('0.4')) < 1e-6))
    C.append(mcq('hard', 's4', 'គេឱ្យសមីការ ' + M('xy+y^2-x^2=5') + ' ដែលមានចំណុច ' + M('(1,\\ 2)') + '។ តម្លៃ ' + M('y\'\'') + ' ត្រង់ចំណុចនេះ ស្មើនឹងប៉ុន្មាន ?',
                 M('\\dfrac25'), [M('0'), M('\\dfrac{2}{5}\\cdot5'), M('-\\dfrac25')],
                 M('y\'=\\dfrac{2x-y}{x+2y}=0') + ' ត្រង់ ' + M('(1,2)') + ' ហើយ ' + M('y\'\'=\\dfrac{50}{(x+2y)^3}=\\dfrac{50}{125}=\\dfrac25') + '។', 'Analyze'))
    f = asin(X ** 2)
    C.append(dq('hard', 's3', f, 2 * X / sqrt(1 - X ** 4), [2 * X / sqrt(1 - X ** 2), 1 / sqrt(1 - X ** 4), 2 * X / sqrt(1 - X ** 4) ** 2], M('(\\sin^{-1}u)\'=\\dfrac{u\'}{\\sqrt{1-u^2}}') + ' ជាមួយ ' + M('u=x^2') + ' ៖ ' + M('\\dfrac{2x}{\\sqrt{1-x^4}}') + '។', 'Analyze', pts=(mp.mpf('0.3'), mp.mpf('0.6'), mp.mpf('0.8'))))
    f = X ** -2
    C.append(dq('hard', 's5', f, -720 / X ** 7, [720 / X ** 7, -120 / X ** 6, -720 / X ** 8], M('f^{(n)}(x)=(-1)^n(n+1)!\\,x^{-(n+2)}') + ' ដូច្នេះ ' + M('f^{(5)}(x)=-\\dfrac{720}{x^7}') + '។', 'Analyze', lead='គណនាដេរីវេទី ៥ នៃ', name='f', n=5))
    f = sin(2 * X + 1) ** 3
    C.append(dq('hard', 's2', f, 6 * sin(2 * X + 1) ** 2 * cos(2 * X + 1), [3 * sin(2 * X + 1) ** 2 * cos(2 * X + 1), 6 * sin(2 * X + 1) ** 2, 6 * cos(2 * X + 1) ** 2 * sin(2 * X + 1)], 'ស្រទាប់បី ៖ ' + M('(w^3)\'=3w^2w\'') + ' ដែល ' + M('w=\\sin(2x+1)') + ' ហើយ ' + M('w\'=2\\cos(2x+1)') + '។', 'Analyze'))
    chk(lambda: (abs(mp.diff(lambda t: mp.atan(t) + mp.acot(t), mp.mpf('0.7'))) < 1e-12, abs(mp.atan(mp.mpf('0.7')) + mp.acot(mp.mpf('0.7')) - mp.pi / 2) < 1e-12))
    C.append(mcq('hard', 's3', 'ការអះអាងមួយណាត្រឹមត្រូវ ?',
                 M('\\dfrac{d}{dx}\\left(\\tan^{-1}x+\\cot^{-1}x\\right)=0') + ' ដូច្នេះ ' + M('\\tan^{-1}x+\\cot^{-1}x') + ' ជាចំនួនថេរ',
                 [M('\\dfrac{d}{dx}\\left(\\tan^{-1}x+\\cot^{-1}x\\right)=\\dfrac{2}{1+x^2}'), M('\\dfrac{d}{dx}\\left(\\sin^{-1}x\\right)=\\dfrac{1}{1+x^2}'), M('\\dfrac{d}{dx}\\left(\\cos^{-1}x\\right)=\\dfrac{1}{\\sqrt{1-x^2}}')],
                 M('\\dfrac1{1+x^2}-\\dfrac1{1+x^2}=0') + ' ។ (ការពិត ' + M('\\tan^{-1}x+\\cot^{-1}x=\\dfrac\\pi2') + ' ។) ឯខ្សែផ្សេងទៀតត្រូវជា ' + M('\\dfrac{1}{\\sqrt{1-x^2}}') + ' (ស៊ីនុស) និង ' + M('-\\dfrac{1}{\\sqrt{1-x^2}}') + ' (កូស៊ីនុស)។', 'Evaluate'))
    f = X ** 2 * sin(X ** 3)
    C.append(dq('hard', 's2', f, 2 * X * sin(X ** 3) + 3 * X ** 4 * cos(X ** 3), [2 * X * sin(X ** 3) + 3 * X ** 2 * cos(X ** 3), 2 * X * cos(X ** 3), 2 * X * sin(X ** 3) - 3 * X ** 4 * cos(X ** 3)], M('(uv)\'=u\'v+uv\'') + ' ជាមួយ ' + M('u=x^2') + ' និង ' + M('v=\\sin x^3') + ' ដែល ' + M('v\'=3x^2\\cos x^3') + '។', 'Analyze', name='f'))

    f = asin(X)
    C.append(dq('hard', 's4', f, X / (1 - X ** 2) ** Rational(3, 2), [X / sqrt(1 - X ** 2), 1 / (1 - X ** 2) ** Rational(3, 2), -X / (1 - X ** 2) ** Rational(3, 2)],
                M('y\'=(1-x^2)^{-1/2}') + ' ដូច្នេះ ' + M('y\'\'=-\\tfrac12(1-x^2)^{-3/2}\\cdot(-2x)=\\dfrac{x}{(1-x^2)^{3/2}}') + '។', 'Analyze', lead='គណនាដេរីវេទី ២ នៃ', n=2, pts=(mp.mpf('0.2'), mp.mpf('0.5'), mp.mpf('0.7'))))

    # ============================================================ MCQ PISA (5)
    chk(lambda: (abs(200 - 2 * 100) < 1e-12, abs(100 * (200 - 100) - 10000) < 1e-9))
    C.append(with_img(mcq('pisa', 'p_area', 'កសិករម្នាក់ចង់ធ្វើរបងព័ទ្ធចម្ការរាងចតុកោណកែងដែលមានបរិមាត្រ ' + M('400\\ \\text{m}') + ' ។ ផ្ទៃក្រឡាជាអនុគមន៍នៃទទឹង ' + M('x') + ' គឺ ' + M('A(x)=200x-x^2') + ' ដូចក្នុងរូប ។ តើ ' + M('x') + ' ស្មើប៉ុន្មាន ដើម្បីឱ្យផ្ទៃក្រឡាធំបំផុត ?',
                          M('x=100\\ \\text{m}'), [M('x=200\\ \\text{m}'), M('x=50\\ \\text{m}'), M('x=400\\ \\text{m}')],
                          M('A\'(x)=200-2x=0') + ' ដូច្នេះ ' + M('x=100') + ' (ហើយ ' + M('A\'\'=-2<0') + ' ជាអតិបរមា ; ទទឹងស្មើបណ្ដោយ គឺការ៉េ ' + M('100\\times100') + ')។', 'Apply'), fig_parab()))
    s_ = lambda t: t ** 3 - 6 * t ** 2 + 9 * t
    chk(lambda: (abs(mp.diff(s_, mp.mpf(2)) - (-3)) < 1e-9, abs(3 * 4 - 12 * 2 + 9 - (-3)) < 1e-12))
    C.append(with_img(mcq('pisa', 'p_speed', 'រថយន្តលេងមួយដើរតាមបន្ទាត់ត្រង់ ដោយទីតាំង ' + M('s(t)=t^3-6t^2+9t') + ' (m) ត្រង់ពេល ' + M('t') + ' វិនាទី ដូចក្នុងរូប ។ តើល្បឿន ' + M('v(2)') + ' (m/s) ស្មើប៉ុន្មាន ?',
                          M('-3'), [M('2'), M('3'), M('-12')],
                          M('v(t)=s\'(t)=3t^2-12t+9') + ' ដូច្នេះ ' + M('v(2)=12-24+9=-3') + ' m/s (ចលនាថយក្រោយ)។', 'Apply'), fig_motion()))
    chk(lambda: (abs((8 + 3) * 4 - 44) < 1e-12, abs(mp.diff(lambda t: mp.mpf('0.5') * (4 * t) ** 2 + 3 * (4 * t), mp.mpf(2)) - 44) < 1e-8))
    C.append(with_img(mcq('pisa', 'p_cost', 'ចំណាយផលិត ' + M('C(x)=0{,}5x^2+3x') + ' (លានរៀល) ដែល ' + M('x') + ' ជាបរិមាណផលិត (រូបបង្ហាញខ្សែកោង និងបន្ទាត់ប៉ះត្រង់ ' + M('x=8') + ') ហើយ ' + M('x=4t') + ' ត្រង់ពេល ' + M('t') + ' ម៉ោង ។ គណនា ' + M('\\dfrac{dC}{dt}') + ' ត្រង់ ' + M('t=2') + ' (លានរៀល/ម៉ោង) ។',
                          M('44'), [M('11'), M('88'), M('56')],
                          M('\\dfrac{dC}{dt}=\\dfrac{dC}{dx}\\cdot\\dfrac{dx}{dt}=(x+3)\\cdot4') + ' ; ត្រង់ ' + M('t=2') + ' មាន ' + M('x=8') + ' ដូច្នេះ ' + M('(8+3)\\times4=44') + '។', 'Apply'), fig_cost_tangent()))
    om = lambda t: -0.6 * mp.sin(2 * t)
    chk(lambda: (abs(mp.diff(lambda t: 0.3 * mp.cos(2 * t), mp.pi / 4) - (-0.6)) < 1e-12, abs(om(mp.pi / 4) - (-0.6)) < 1e-12))
    C.append(with_img(mcq('pisa', 'p_pend', 'មុំរបស់ប៉ោលមួយ (rad) ត្រូវបានតាមដោយ ' + M('\\theta(t)=0{,}3\\cos2t') + ' (រូបបង្ហាញ ' + M('\\theta') + ' និងល្បឿនមុំ ' + M('\\omega=\\theta\'') + ') ។ គណនាល្បឿនមុំ ' + M('\\omega') + ' (rad/s) ត្រង់ ' + M('t=\\dfrac\\pi4') + ' ។',
                          M('-0{,}6'), [M('0{,}6'), M('0'), M('-0{,}3')],
                          M('\\omega=\\theta\'=-0{,}6\\sin2t') + ' ដូច្នេះ ' + M('\\omega\\left(\\dfrac\\pi4\\right)=-0{,}6\\sin\\dfrac\\pi2=-0{,}6') + ' rad/s។', 'Apply'), fig_pendulum()))
    chk(lambda: (abs(mp.diff(lambda t: mp.atan(t / 10), mp.mpf(10)) - mp.mpf('0.05')) < 1e-12, abs(10 / (100 + 100.0) - 0.05) < 1e-12))
    C.append(with_img(mcq('pisa', 'p_angle', 'កាមេរ៉ាមើលវត្ថុដែលនៅឆ្ងាយ ' + M('x') + ' ម៉ែត្រ ដោយមុំ ' + M('\\theta(x)=\\tan^{-1}\\dfrac x{10}') + ' (rad) ដូចក្នុងរូប ។ គណនាអត្រាបម្រែបម្រួល ' + M('\\theta\'(x)') + ' ត្រង់ ' + M('x=10') + ' (rad/m) ។',
                          M('0{,}05'), [M('0{,}5'), M('0{,}1'), M('0{,}01')],
                          M('\\theta\'(x)=\\dfrac{\\frac1{10}}{1+\\frac{x^2}{100}}=\\dfrac{10}{100+x^2}') + ' ដូច្នេះ ' + M('\\theta\'(10)=\\dfrac{10}{200}=0{,}05') + '។', 'Analyze'), fig_angle_atan()))
    return C + cands_writing()


def cands_writing():
    C = []
    X = x
    # ============================================================ WRITING EASY (1)
    chk(lambda: abs(mp.diff(lambda t: (2 * t - 3) ** 4, mp.mpf('0.7')) - 8 * (2 * mp.mpf('0.7') - 3) ** 3) < 1e-9)
    C.append(wr('easy', 's1', 'គណនាដេរីវេនៃអនុគមន៍ ' + M('y=(2x-3)^4') + ' ដោយប្រើរូបមន្តដេរីវេនៃអនុគមន៍បណ្ដាក់ ។',
                [('តាង ' + M('u=2x-3') + ' ដូច្នេះ ' + M('y=u^4'), 1),
                 ('គណនា ' + M('\\dfrac{du}{dx}=2'), 1),
                 ('គណនា ' + M('\\dfrac{dy}{du}=4u^3'), 1),
                 ('ប្រើ ' + M('\\dfrac{dy}{dx}=\\dfrac{dy}{du}\\times\\dfrac{du}{dx}=4u^3\\times2=8u^3'), 1),
                 ('ជំនួស ' + M('u=2x-3') + ' ៖ ' + M('\\dfrac{dy}{dx}=8(2x-3)^3') + '។', 1)], bloom='Apply'))

    # ============================================================ WRITING MEDIUM (4)
    chk(lambda: abs(mp.diff(lambda t: t ** 2 * mp.cos(3 * t + 1), mp.mpf('0.6')) - (2 * mp.mpf('0.6') * mp.cos(3 * mp.mpf('0.6') + 1) - 3 * mp.mpf('0.6') ** 2 * mp.sin(3 * mp.mpf('0.6') + 1))) < 1e-9)
    C.append(wr('medium', 's2', 'គណនាដេរីវេនៃអនុគមន៍ ' + M('f(x)=x^2\\cos(3x+1)') + ' ហើយគណនា ' + M('f\'(0)') + '។',
                [('ប្រើដេរីវេនៃផលគុណ ' + M('(uv)\'=u\'v+uv\'') + ' ដែល ' + M('u=x^2,\\ v=\\cos(3x+1)'), 1),
                 (M('u\'=2x'), 1),
                 ('ប្រើអនុគមន៍បណ្ដាក់ ៖ ' + M('v\'=-3\\sin(3x+1)'), 1),
                 ('បូកបញ្ចូលគ្នា ៖ ' + M('f\'(x)=2x\\cos(3x+1)-3x^2\\sin(3x+1)'), 1),
                 ('ជំនួស ' + M('x=0') + ' ៖ ' + M('f\'(0)=0-0=0') + '។', 1)], bloom='Apply'))
    chk(lambda: abs(mp.diff(lambda t: t * mp.asin(2 * t), mp.mpf('0.2')) - (mp.asin(2 * mp.mpf('0.2')) + 2 * mp.mpf('0.2') / mp.sqrt(1 - 4 * mp.mpf('0.2') ** 2))) < 1e-9)
    C.append(wr('medium', 's3', 'គណនាដេរីវេនៃអនុគមន៍ ' + M('y=x\\sin^{-1}2x') + ' ដែល ' + M('|x|<\\dfrac12') + '។',
                [('ប្រើ ' + M('(uv)\'=u\'v+uv\'') + ' ដែល ' + M('u=x') + ' និង ' + M('v=\\sin^{-1}2x'), 1),
                 (M('u\'=1'), 1),
                 ('ប្រើ ' + M('(\\sin^{-1}w)\'=\\dfrac{w\'}{\\sqrt{1-w^2}}') + ' ជាមួយ ' + M('w=2x') + ' ៖ ' + M('v\'=\\dfrac{2}{\\sqrt{1-4x^2}}'), 1),
                 ('បូក ៖ ' + M('y\'=\\sin^{-1}2x+x\\cdot\\dfrac2{\\sqrt{1-4x^2}}'), 1),
                 ('ដូច្នេះ ' + M('y\'=\\sin^{-1}2x+\\dfrac{2x}{\\sqrt{1-4x^2}}') + '។', 1)], bloom='Apply'))
    chk(lambda: (abs(-mp.mpf(3) / 4 - (-0.75)) < 1e-12, abs(-25 / mp.mpf(4) ** 3 - (-25 / 64)) < 1e-12))
    yc = lambda xx: mp.sqrt(25 - xx ** 2)
    chk(lambda: (abs(mp.diff(yc, mp.mpf(3)) - (-0.75)) < 1e-9, abs(mp.diff(yc, mp.mpf(3), 2) - (-25 / mp.mpf(64))) < 1e-8))
    C.append(wr('medium', 's4', 'គេឱ្យរង្វង់ ' + M('x^2+y^2=25') + ' ។ ក. រក ' + M('y\'') + ' ជាអនុគមន៍នៃ ' + M('x') + ' និង ' + M('y') + ' ។ ខ. រក ' + M('y\'\'') + ' ។ គ. គណនាមេគុណប្រាប់ទិសនៃបន្ទាត់ប៉ះត្រង់ ' + M('(3,4)') + ' និងតម្លៃ ' + M('y\'\'') + ' ត្រង់ចំណុចនេះ។',
                [('ក. ដេរីវេអង្គទាំងពីរ ៖ ' + M('2x+2yy\'=0') + ' ដូច្នេះ ' + M('y\'=-\\dfrac xy') + ' ($y\\ne0$)', 1),
                 ('ខ. ដេរីវេ ' + M('x+yy\'=0') + ' ម្ដងទៀត ៖ ' + M('1+y\'^2+yy\'\'=0'), 1),
                 ('ដូច្នេះ ' + M('y\'\'=-\\dfrac{1+y\'^2}{y}=-\\dfrac{1+\\frac{x^2}{y^2}}{y}=-\\dfrac{x^2+y^2}{y^3}=-\\dfrac{25}{y^3}'), 1),
                 ('គ. ត្រង់ ' + M('(3,4)') + ' ៖ ' + M('y\'=-\\dfrac34'), 1),
                 (M('y\'\'=-\\dfrac{25}{4^3}=-\\dfrac{25}{64}<0') + ' (រង្វង់ផ្នែកខាងលើកោងចុះ)។', 1)], bloom='Analyze'))
    C.append(wr('medium', 's2', 'ដោយប្រើវិធីដេរីវេនៃផលចែក បង្ហាញថា ក. ' + M('(\\tan x)\'=\\dfrac1{\\cos^2x}') + ' ខ. ' + M('(\\cot x)\'=-\\dfrac1{\\sin^2x}') + '។',
                [('ក. សរសេរ ' + M('\\tan x=\\dfrac{\\sin x}{\\cos x}') + ' ហើយប្រើ ' + M('\\left(\\dfrac uv\\right)\'=\\dfrac{u\'v-uv\'}{v^2}'), 1),
                 ('គណនា ' + M('(\\tan x)\'=\\dfrac{\\cos x\\cos x-(-\\sin x)\\sin x}{\\cos^2x}=\\dfrac{\\cos^2x+\\sin^2x}{\\cos^2x}'), 1),
                 ('ដូច្នេះ ' + M('(\\tan x)\'=\\dfrac1{\\cos^2x}=1+\\tan^2x'), 1),
                 ('ខ. ' + M('\\cot x=\\dfrac{\\cos x}{\\sin x}') + ' ៖ ' + M('(\\cot x)\'=\\dfrac{-\\sin x\\sin x-\\cos x\\cos x}{\\sin^2x}'), 1),
                 ('សម្រួល ' + M('=\\dfrac{-(\\sin^2x+\\cos^2x)}{\\sin^2x}=-\\dfrac1{\\sin^2x}=-(1+\\cot^2x)') + '។', 1)], bloom='Understand'))
    chk(lambda: (abs(mp.diff(mp.tan, mp.mpf('0.4')) - 1 / mp.cos(mp.mpf('0.4')) ** 2) < 1e-9, abs(mp.diff(mp.cot, mp.mpf('0.4')) + 1 / mp.sin(mp.mpf('0.4')) ** 2) < 1e-9))

    # ============================================================ WRITING HARD (4)
    chk(lambda: all(abs(mp.diff(mp.cos, mp.mpf('0.3'), n) - mp.cos(mp.mpf('0.3') + n * mp.pi / 2)) < 1e-9 for n in range(1, 8)))
    C.append(wr('hard', 's5', 'ស្រាយបញ្ជាក់ដោយអនុមានរួមគណិតវិទ្យាថា ដេរីវេទី ' + M('n') + ' នៃ ' + M('y=\\cos x') + ' គឺ ' + M('y^{(n)}=\\cos\\left(x+\\dfrac{n\\pi}2\\right)') + ' ចំពោះគ្រប់ ' + M('n\\in\\mathbb{N}^*') + '។',
                [('មូលដ្ឋាន ' + M('n=1') + ' ៖ ' + M('y\'=-\\sin x=\\cos\\left(x+\\dfrac\\pi2\\right)') + ' ពិត', 1),
                 ('ឧបមា ' + M('P(k)') + ' ៖ ' + M('y^{(k)}=\\cos\\left(x+\\dfrac{k\\pi}2\\right)') + ' ពិតចំពោះ ' + M('k\\ge1'), 1),
                 ('ដេរីវេ ៖ ' + M('y^{(k+1)}=\\left[\\cos\\left(x+\\tfrac{k\\pi}2\\right)\\right]\'=-\\sin\\left(x+\\tfrac{k\\pi}2\\right)'), 1),
                 ('ប្រើ ' + M('-\\sin\\alpha=\\cos\\left(\\alpha+\\tfrac\\pi2\\right)') + ' ៖ ' + M('y^{(k+1)}=\\cos\\left(x+\\tfrac{k\\pi}2+\\tfrac\\pi2\\right)=\\cos\\left[x+\\tfrac{(k+1)\\pi}2\\right]'), 1),
                 ('ដូច្នេះ ' + M('P(k+1)') + ' ពិត ; តាមអនុមានរួម ' + M('P(n)') + ' ពិតគ្រប់ ' + M('n\\in\\mathbb{N}^*') + '។', 1)], bloom='Create'))
    fx = lambda t: 1 / (t * (t + 1))
    chk(lambda: all(abs(mp.diff(fx, mp.mpf('0.9'), n) - (-1) ** n * mp.factorial(n) * (1 / mp.mpf('0.9') ** (n + 1) - 1 / mp.mpf('1.9') ** (n + 1))) < 1e-6 * mp.factorial(n) * 10 ** n for n in range(1, 6)))
    C.append(wr('hard', 's5', 'គេឱ្យ ' + M('f(x)=\\dfrac{1}{x(x+1)}') + '។ ក. សរសេរ ' + M('f(x)=\\dfrac ax+\\dfrac b{x+1}') + ' ដោយរក ' + M('a,b') + '។ ខ. រកដេរីវេទី ' + M('n') + ' ' + M('f^{(n)}(x)') + ' ។ គ. គណនា ' + M('f^{(5)}(1)') + '។',
                [('ក. ' + M('1=a(x+1)+bx') + ' ៖ ដាក់ ' + M('x=0') + ' បាន ' + M('a=1') + ' ; ដាក់ ' + M('x=-1') + ' បាន ' + M('b=-1'), 1),
                 ('ដូច្នេះ ' + M('f(x)=\\dfrac1x-\\dfrac1{x+1}'), 1),
                 ('ខ. ប្រើ ' + M('\\left(\\dfrac1{x+c}\\right)^{(n)}=\\dfrac{(-1)^nn!}{(x+c)^{n+1}}') + ' ៖ ' + M('f^{(n)}(x)=(-1)^nn!\\left[\\dfrac1{x^{n+1}}-\\dfrac1{(x+1)^{n+1}}\\right]'), 1),
                 ('គ. ជំនួស ' + M('n=5,\\ x=1') + ' ៖ ' + M('f^{(5)}(1)=(-1)^5\\,5!\\left[1-\\dfrac1{2^6}\\right]'), 1),
                 ('ដូច្នេះ ' + M('f^{(5)}(1)=-120\\cdot\\dfrac{63}{64}=-\\dfrac{945}{8}=-118{,}125') + '។', 1)], bloom='Analyze'))
    chk(lambda: abs(-120 * mp.mpf(63) / 64 - (-118.125)) < 1e-12 and abs(mp.diff(fx, mp.mpf(1), 5) - (-118.125)) < 1e-4)
    chk(lambda: (abs(mp.diff(mp.asin, mp.mpf('0.5')) - 1 / mp.sqrt(1 - mp.mpf('0.5') ** 2)) < 1e-12, mp.diff(mp.asin, mp.mpf('0.999999')) > 700))
    C.append(wr('hard', 's3', 'ក. ប្រើអនុគមន៍ច្រាស ' + M('x=\\sin y') + ' ដោយ ' + M('-\\dfrac\\pi2\\le y\\le\\dfrac\\pi2') + ' បង្ហាញថា ' + M('(\\sin^{-1}x)\'=\\dfrac1{\\sqrt{1-x^2}}') + '។ ខ. វាយតម្លៃសេចក្ដីអះអាង "' + M('\\sin^{-1}x') + ' មានដេរីវេគ្រប់ ' + M('x\\in[-1,1]') + '" ។',
                [('ក. ពី ' + M('x=\\sin y') + ' ដេរីវេទាក់ទង ' + M('x') + ' ៖ ' + M('1=\\cos y\\cdot y\''), 1),
                 ('ដូច្នេះ ' + M('y\'=\\dfrac1{\\cos y}') + ' ដែល ' + M('\\cos y\\ne0'), 1),
                 ('ដោយ ' + M('-\\dfrac\\pi2\\le y\\le\\dfrac\\pi2') + ' នោះ ' + M('\\cos y\\ge0') + ' ដូច្នេះ ' + M('\\cos y=\\sqrt{1-\\sin^2y}=\\sqrt{1-x^2}') + ' ហើយ ' + M('y\'=\\dfrac1{\\sqrt{1-x^2}}'), 1),
                 ('ខ. ត្រង់ ' + M('x=\\pm1') + ' មាន ' + M('y=\\pm\\dfrac\\pi2') + ' ដូច្នេះ ' + M('\\cos y=0') + ' ភាគបែងស្មើសូន្យ', 1),
                 ('ដូច្នេះដេរីវេមាន (កំណត់) តែចំពោះ ' + M('-1<x<1') + ' (តង់សង់បញ្ឈរត្រង់ចុង) ; សេចក្ដីអះអាងមិនត្រឹមត្រូវ។', 1)], bloom='Evaluate'))
    C.append(wr('hard', 's3', 'ក. គណនា ' + M('\\dfrac{d}{dx}\\left(\\sin^{-1}x+\\cos^{-1}x\\right)') + ' ចំពោះ ' + M('-1<x<1') + ' ។ ខ. ទាញថា ' + M('\\sin^{-1}x+\\cos^{-1}x') + ' ជាចំនួនថេរ ហើយរកតម្លៃចំនួនថេរនេះ ។ គ. ប្រើលទ្ធផលដើម្បីបង្ហាញថា ' + M('\\dfrac{d}{dx}\\cos^{-1}x=-\\dfrac{d}{dx}\\sin^{-1}x') + '។',
                [('ក. ' + M('(\\sin^{-1}x)\'=\\dfrac1{\\sqrt{1-x^2}}') + ' និង ' + M('(\\cos^{-1}x)\'=-\\dfrac1{\\sqrt{1-x^2}}'), 1),
                 ('ផលបូក ៖ ' + M('\\dfrac1{\\sqrt{1-x^2}}-\\dfrac1{\\sqrt{1-x^2}}=0'), 1),
                 ('ខ. ដេរីវេស្មើសូន្យលើចន្លោះ ' + M('(-1,1)') + ' ដូច្នេះអនុគមន៍ ' + M('h(x)=\\sin^{-1}x+\\cos^{-1}x') + ' ជាចំនួនថេរ ' + M('c'), 1),
                 ('រក ' + M('c') + ' ដោយ ' + M('x=0') + ' ៖ ' + M('c=\\sin^{-1}0+\\cos^{-1}0=0+\\dfrac\\pi2=\\dfrac\\pi2'), 1),
                 ('គ. ដូច្នេះ ' + M('\\cos^{-1}x=\\dfrac\\pi2-\\sin^{-1}x') + ' ហើយដេរីវេ ៖ ' + M('(\\cos^{-1}x)\'=-(\\sin^{-1}x)\'') + '។', 1)], bloom='Create'))
    chk(lambda: (abs(mp.asin(mp.mpf('0.37')) + mp.acos(mp.mpf('0.37')) - mp.pi / 2) < 1e-12, abs(mp.diff(lambda t: mp.asin(t) + mp.acos(t), mp.mpf('0.37'))) < 1e-12))

    # ============================================================ WRITING PISA (5)
    chk(lambda: (abs(200 - 2 * 100) < 1e-12, abs(100 * 100 - 10000) < 1e-12, abs(mp.diff(lambda t: t * (200 - t), mp.mpf(100), 2) - (-2)) < 1e-6))
    C.append(with_img(wr('pisa', 'p_fence', 'កសិករម្នាក់មានរបង ' + M('400\\ \\text{m}') + ' ដើម្បីព័ទ្ធចម្ការរាងចតុកោណកែង ទទឹង ' + M('x') + ' បណ្ដោយ ' + M('y') + ' ដូចក្នុងរូប ។ ក. បង្ហាញថា ' + M('A(x)=200x-x^2') + '។ ខ. រកដេរីវេ ' + M('A\'(x)') + ' ហើយរកតម្លៃ ' + M('x') + ' ដែល ' + M('A\'(x)=0') + '។ គ. ប្រើដេរីវេទី ២ បញ្ជាក់ថាជាអតិបរមា ហើយរកផ្ទៃក្រឡាអតិបរមា ។',
                          [('ក. បរិមាត្រ ' + M('2x+2y=400') + ' ដូច្នេះ ' + M('y=200-x') + ' ហើយ ' + M('A=xy=x(200-x)=200x-x^2'), 1),
                           ('ខ. ' + M('A\'(x)=200-2x'), 1),
                           ('ដោះស្រាយ ' + M('200-2x=0') + ' បាន ' + M('x=100') + ' (ដូច្នេះ ' + M('y=100') + ')', 1),
                           ('គ. ' + M('A\'\'(x)=-2<0') + ' ដូច្នេះ ' + M('x=100') + ' ផ្ដល់អតិបរមា', 1),
                           ('ផ្ទៃក្រឡាអតិបរមា ' + M('A(100)=100\\times100=10\\,000\\ \\text{m}^2') + ' (ការ៉េ)។', 1)], bloom='Apply'),
                   fig_parab()))
    st = lambda t: t ** 3 - 6 * t ** 2 + 9 * t
    chk(lambda: (abs(mp.diff(st, mp.mpf(1))) < 1e-9, abs(mp.diff(st, mp.mpf(3))) < 1e-9, abs(mp.diff(st, mp.mpf(2), 2)) < 1e-6, abs(st(1) - 4) < 1e-12, abs(st(3)) < 1e-12))
    C.append(with_img(wr('pisa', 'p_motion', 'ទីតាំងនៃចំណុចមួយតាមបន្ទាត់ត្រង់ ' + M('s(t)=t^3-6t^2+9t') + ' (m) ត្រង់ពេល ' + M('t') + ' វិនាទី ដូចក្នុងរូប ។ ក. រកល្បឿន ' + M('v(t)=s\'(t)') + ' និងសំទុះ ' + M('a(t)=s\'\'(t)') + '។ ខ. ចំណុចឈប់ត្រង់ពេលណា ? គ. រកទីតាំងនៅពេលឈប់ និងសំទុះត្រង់ ' + M('t=2') + '។',
                          [('ក. ' + M('v(t)=3t^2-12t+9') + ' (m/s)', 1),
                           (M('a(t)=v\'(t)=6t-12') + ' (m/s²)', 1),
                           ('ខ. ' + M('v=0') + ' ៖ ' + M('3(t^2-4t+3)=3(t-1)(t-3)=0') + ' ដូច្នេះ ' + M('t=1') + ' ឬ ' + M('t=3') + ' វិនាទី', 1),
                           ('គ. ' + M('s(1)=1-6+9=4') + ' m ហើយ ' + M('s(3)=27-54+27=0') + ' m', 1),
                           (M('a(2)=6(2)-12=0') + ' m/s² (ត្រង់ពេលនេះល្បឿនអប្បបរមា ' + M('v(2)=-3') + ' m/s)។', 1)], bloom='Apply'),
                   fig_motion()))
    C.append(with_img(wr('pisa', 'p_chain', 'ចំណាយផលិត ' + M('C(x)=0{,}5x^2+3x') + ' (លានរៀល) ដែល ' + M('x') + ' ជាចំនួនឯកតា ហើយការផលិតកើនតាមពេល ' + M('x(t)=4t') + ' ឯកតា (t ម៉ោង) ដូចក្នុងរូប ។ ក. រក ' + M('\\dfrac{dC}{dx}') + ' និង ' + M('\\dfrac{dx}{dt}') + '។ ខ. គណនា ' + M('\\dfrac{dC}{dt}') + ' ត្រង់ ' + M('t=2') + '។ គ. ផ្ទៀងផ្ទាត់ដោយសរសេរ ' + M('C') + ' ជាអនុគមន៍នៃ ' + M('t') + ' ដោយផ្ទាល់ ។',
                          [('ក. ' + M('\\dfrac{dC}{dx}=x+3') + ' ហើយ ' + M('\\dfrac{dx}{dt}=4'), 1),
                           ('ខ. ' + M('\\dfrac{dC}{dt}=\\dfrac{dC}{dx}\\cdot\\dfrac{dx}{dt}=(x+3)\\cdot4'), 1),
                           ('ត្រង់ ' + M('t=2') + ' មាន ' + M('x=4\\times2=8'), 1),
                           ('ដូច្នេះ ' + M('\\dfrac{dC}{dt}=(8+3)\\times4=44') + ' លានរៀល/ម៉ោង', 1),
                           ('គ. ' + M('C(t)=0{,}5(4t)^2+3(4t)=8t^2+12t') + ' ដូច្នេះ ' + M('C\'(t)=16t+12') + ' ហើយ ' + M('C\'(2)=44') + ' ត្រូវគ្នា។', 1)], bloom='Analyze'),
                   fig_cost_tangent()))
    chk(lambda: (abs(mp.diff(lambda t: mp.atan(30 / t), mp.mpf(40)) - (-0.012)) < 1e-9, abs(-30 / mp.mpf(40 ** 2 + 900) - (-0.012)) < 1e-12))
    C.append(with_img(wr('pisa', 'p_drone', 'ដ្រូនមួយហោះនៅកម្ពស់ ' + M('30\\ \\text{m}') + ' ដោយអ្នកសង្កេតនៅចម្ងាយផ្ដេក ' + M('x') + ' ម៉ែត្រ ។ មុំសំលឹកឡើង ' + M('\\theta(x)=\\tan^{-1}\\dfrac{30}x') + ' (rad) ដូចក្នុងរូប ។ ក. គណនា ' + M('\\theta\'(x)') + '។ ខ. គណនា ' + M('\\theta\'(40)') + ' ហើយបកស្រាយសញ្ញា ។ គ. ប្រៀបធៀបអត្រាត្រង់ ' + M('x=40') + ' និង ' + M('x=10') + '។',
                          [('ក. ប្រើ ' + M('(\\tan^{-1}u)\'=\\dfrac{u\'}{1+u^2}') + ' ជាមួយ ' + M('u=\\dfrac{30}x') + ' ដែល ' + M('u\'=-\\dfrac{30}{x^2}'), 1),
                           ('ដូច្នេះ ' + M('\\theta\'(x)=\\dfrac{-30/x^2}{1+900/x^2}=-\\dfrac{30}{x^2+900}'), 1),
                           ('ខ. ' + M('\\theta\'(40)=-\\dfrac{30}{1600+900}=-\\dfrac{30}{2500}=-0{,}012') + ' rad/m', 1),
                           ('សញ្ញាអវិជ្ជមាន ៖ ដ្រូនកាន់តែឆ្ងាយ មុំសំលឹកកាន់តែតូច', 1),
                           ('គ. ' + M('\\theta\'(10)=-\\dfrac{30}{1000}=-0{,}03') + ' rad/m ធំជាង ' + M('0{,}012') + ' ក្នុងតម្លៃដាច់ខាត ៖ ក្បែរគល់មុំប្ដូរលឿនជាង។', 1)], bloom='Analyze'),
                   fig_angle()))
    chk(lambda: abs(mp.diff(lambda t: 0.3 * mp.cos(2 * t), mp.pi / 6, 2) - (-1.2 * mp.cos(mp.pi / 3))) < 1e-9)
    chk(lambda: all(abs(mp.diff(lambda t: 0.3 * mp.cos(2 * t), mp.mpf(v), 2) + 4 * 0.3 * mp.cos(2 * mp.mpf(v))) < 1e-9 for v in ('0.2', '0.9', '1.7')))
    C.append(with_img(wr('pisa', 'p_osc', 'មុំរបស់ប៉ោលមួយ ' + M('\\theta(t)=0{,}3\\cos2t') + ' (rad) ដូចក្នុងរូប ។ ក. រកល្បឿនមុំ ' + M('\\omega=\\theta\'') + ' និងសំទុះមុំ ' + M('\\alpha=\\theta\'\'') + '។ ខ. បង្ហាញថា ' + M('\\theta\'\'+4\\theta=0') + '។ គ. វាយតម្លៃថា "សំទុះមុំធំបំផុតកើតឡើងនៅពេលល្បឿនមុំស្មើសូន្យ" ។',
                          [('ក. ' + M('\\omega=\\theta\'=-0{,}6\\sin2t') + ' (ប្រើអនុគមន៍បណ្ដាក់)', 1),
                           (M('\\alpha=\\theta\'\'=-1{,}2\\cos2t'), 1),
                           ('ខ. ' + M('\\theta\'\'+4\\theta=-1{,}2\\cos2t+4(0{,}3\\cos2t)=-1{,}2\\cos2t+1{,}2\\cos2t=0'), 1),
                           ('គ. ' + M('|\\alpha|=1{,}2|\\cos2t|') + ' ធំបំផុត ' + M('=1{,}2') + ' កាលណា ' + M('|\\cos2t|=1'), 1),
                           ('ពេលនោះ ' + M('\\sin2t=0') + ' គឺ ' + M('\\omega=0') + ' ដូច្នេះសេចក្ដីអះអាងត្រឹមត្រូវ (ចុងរំញ័រ ល្បឿនស្មើសូន្យ សំទុះធំបំផុត)។', 1)], bloom='Evaluate'),
                   fig_pendulum()))
    return C


def verify():
    """independent numeric re-derivation: every dq() closed form and wrong option, plus the chk() claims, run again from scratch."""
    mp.mp.dps = 40
    CNT[0] = 0
    C = cands()
    return CNT[0]
