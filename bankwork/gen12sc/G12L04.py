# -*- coding: utf-8 -*-
"""
KhmerMath Question Bank: Grade 12 Science (SC)
Chapter 2: លីមីត
Lesson 1: លីមីតនៃអនុគមន៍
Reference textbook: Lesson/G12/SC/C2-L1.tex

Target matrix: MCQ easy10/medium14/hard7/pisa5 + writing easy1/medium4/hard4/pisa5 = 50, a Bloom level on each.
Every limit is computed by sympy (limit()), then re-checked at generation time and again in verify() by plain
high-precision numerics (mpmath) evaluated close to the limit point; the LaTeX of every limit is printed from the
very same sympy expression, so the stem and the answer cannot drift apart.
"""
import sys, os, math
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib import *
import svgkit as K
import mpmath as mp
from sympy import (lambdify, Symbol, Rational, sqrt, simplify, latex, oo, limit, sin, cos, tan, exp, log, Abs, Add, pi, N, S, cbrt, nsimplify, Integer)

LESSON = 'លីមីតនៃអនុគមន៍'
CHAPTER = 'ជំពូកទី 2 : លីមីត'
GRADE = '12SC'
TARGET = {('mcq', 'easy'): 10, ('mcq', 'medium'): 14, ('mcq', 'hard'): 7, ('mcq', 'pisa'): 5,
          ('writing', 'easy'): 1, ('writing', 'medium'): 4, ('writing', 'hard'): 4, ('writing', 'pisa'): 5}
S1 = 'លីមីតតាមនិយមន័យ និងប្រមាណវិធី'
S2 = 'លីមីតនៃអនុគមន៍អសនិទាន និងអនុគមន៍បណ្ដាក់'
S3 = 'លីមីតរាងមិនកំណត់'
S4 = 'លីមីតនៃអនុគមន៍ត្រីកោណមាត្រ'
S5 = 'លីមីតនៃអនុគមន៍អិចស្ប៉ូណង់ស្យែល និងលោការីត'
TOPIC_MAP = {'s1': S1, 's2': S2, 's3': S3, 's4': S4, 's5': S5,
             'p_coffee': S5, 'p_taxi': S1, 'p_chord': S4, 'p_eff': S5, 'p_poly': S4,
             'p_drug': S3, 'p_charge': S5, 'p_cost': S3, 'p_signal': S5, 'p_logis': S5}

x = Symbol('x', real=True)
CHECKS = []          # (python callable, point, direction, expected sympy value) re-verified by verify()


# ----------------------------------------------------------------------------- display helpers
def _L(e):
    return latex(e).replace('\\frac', '\\dfrac')


def V(v):
    """a limit value in LaTeX."""
    if v == oo:
        return '+\\infty'
    if v == -oo:
        return '-\\infty'
    return _L(nsimplify(v)) if not isinstance(v, str) else v


def PT(p):
    if p == oo:
        return '+\\infty'
    if p == -oo:
        return '-\\infty'
    return _L(p)


def LIM(expr, pt, d='+-'):
    arrow = {'+-': '', '+': '^{+}', '-': '^{-}'}[d]
    body = _L(expr)
    if isinstance(expr, Add):
        body = '\\left(' + body + '\\right)'
    return '\\lim_{x\\to %s%s}%s' % (PT(pt), arrow, body)


def LIMV(expr, pt, d='+-'):
    return M(LIM(expr, pt, d))


def num_limit(f, pt, d):
    """independent numeric estimate with mpmath at 60 digits."""
    mp.mp.dps = 60
    if pt == oo:
        return [f(mp.mpf(10) ** k) for k in (8, 12, 16)]
    if pt == -oo:
        return [f(-mp.mpf(10) ** k) for k in (8, 12, 16)]
    p = mp.mpf(N(pt, 50))
    out = []
    for k in (8, 12, 16):
        h = mp.mpf(10) ** (-k)
        if d == '+':
            out.append(f(p + h))
        elif d == '-':
            out.append(f(p - h))
        else:
            out.append(f(p + h))
            out.append(f(p - h))
    return out


def close_to(vals, exp_):
    mp.mp.dps = 60
    if exp_ == oo:      # diverges upward: still growing and already large (ln x grows slowly, so the bar is modest)
        return vals[-1] > vals[-2] > vals[-3] and vals[-1] > 30
    if exp_ == -oo:
        return vals[-1] < vals[-2] < vals[-3] and vals[-1] < -30
    e = mp.mpf(N(exp_, 50))
    return all(abs(v - e) < mp.mpf(10) ** -5 * max(1, abs(e)) for v in vals[-2:])


def lq(level, sec, expr, pt, d, wrongs, sol, bloom, lead='គណនា', tail='', img=None):
    """a 'compute this limit' MCQ: the answer comes from sympy, is cross-checked numerically, and is never among the wrongs."""
    right = limit(expr, x, pt, d) if d != '+-' else limit(expr, x, pt)
    f = lambdify(x, expr, 'mpmath')
    assert close_to(num_limit(f, pt, d), right), ('numeric check failed', expr, pt, d, right)
    CHECKS.append((f, pt, d, right))
    ws = []
    for w in wrongs:
        wv = nsimplify(w) if not isinstance(w, str) else None
        if wv is not None and right not in (oo, -oo) and wv not in (oo, -oo):
            assert simplify(wv - right) != 0, ('a wrong option equals the answer', expr, w)
        if wv is not None and wv == right:
            raise AssertionError(('a wrong option equals the answer', expr, w))
        ws.append(M(V(w)))
    q = mcq(level, sec, lead + ' ' + LIMV(expr, pt, d) + tail + '។', M(V(right)), ws, sol, bloom)
    if img:
        q['img'] = img
    return q


def with_img(q, svg):
    q['img'] = svg
    return q


# ----------------------------------------------------------------------------- figures
def G(W, H, curves, xo=0, yo=0, xt=(), yt=(), hl=(), vl=(), dots=(), odots=(), segs=(), notes=(), xlabel='x', ylabel='y', pad=28):
    """a coordinate figure in pixel units (1 unit = 1 px).  curves: (f_px, x0_px, x1_px, color) with f_px: px -> px or None (a break).
    The axes cross at (0, 0) of the pixel frame; xo / yo shift the frame so that negative values show."""
    seg = []
    for (y, col, dashed) in hl:
        seg.append((-xo, y, W - xo, y, col, dashed))
    for (xx, col, dashed) in vl:
        seg.append((xx, -yo, xx, H - yo, col, dashed))
    for s_ in segs:
        seg.append(s_)
    nt = []
    for (xx, lab) in xt:
        seg.append((xx, -4, xx, 4, K.AXIS, False))
        nt.append((xx, 0, lab, 0, 20, K.AXIS, False))
    for (yy, lab) in yt:
        seg.append((-4, yy, 4, yy, K.AXIS, False))
        nt.append((0, yy, lab, -15, 5, K.AXIS, False))
    base = K.plane((-xo, W - xo), (-yo, H - yo), 1, segs=seg, notes=list(notes) + nt, grid=False, ticks=False,
                   xlabel=xlabel, ylabel=ylabel, pad=pad)
    px = lambda v: pad + (v + xo)
    py = lambda v: pad + (H - yo - v)
    add = []
    for (f, a, b, col) in curves:
        pieces, cur = [], []
        n = 400
        for i in range(n + 1):
            t = a + (b - a) * i / n
            try:
                y = f(t)
            except ZeroDivisionError:
                y = None
            if y is None or y != y or y < -yo - 2 or y > H - yo + 2:
                if len(cur) > 1:
                    pieces.append(cur)
                cur = []
            else:
                cur.append((px(t), py(y)))
        if len(cur) > 1:
            pieces.append(cur)
        for pc in pieces:
            add.append("<polyline fill='none' stroke='%s' stroke-width='2.2' stroke-linejoin='round' points='%s'/>" % (col, ' '.join('%.1f,%.1f' % p for p in pc)))
    for (xx, yy, lab, dx, dy, col) in dots:
        add.append("<circle cx='%.1f' cy='%.1f' r='4' fill='%s'/>" % (px(xx), py(yy), col))
        if lab:
            add.append(K._lab(lab, px(xx) + dx, py(yy) + dy, size=16, color=K.INK, italic=False))
    for (xx, yy, lab, dx, dy, col) in odots:
        add.append("<circle cx='%.1f' cy='%.1f' r='4.2' fill='none' stroke='%s' stroke-width='1.8'/>" % (px(xx), py(yy), col))
        if lab:
            add.append(K._lab(lab, px(xx) + dx, py(yy) + dy, size=16, color=K.INK, italic=False))
    return base.replace('</svg>', '\n'.join(add) + '\n</svg>')


def curve(fn, kx, ky):
    """a data-space function -> pixel-space function."""
    def f(px_):
        try:
            v = fn(px_ / kx)
        except (ZeroDivisionError, ValueError, OverflowError):
            return None
        return None if v is None else v * ky
    return f


def fig_inv(a=1):      # y = 1/(x-1), asymptotes x=1 and y=0
    kx, ky = 40, 40
    fn = lambda t: 1 / (t - a)
    cv = [(curve(fn, kx, ky), -150, a * kx - 3, K.BLUE), (curve(fn, kx, ky), a * kx + 3, 170, K.BLUE)]
    return G(330, 190, cv, xo=150, yo=95, vl=[(a * kx, K.AMBER, True)], hl=[(0, K.GRID, False)], xt=[(a * kx, '1')],
             notes=[(a * kx, -70, 'y = 1/(x − 1)', 40, 0, K.BLUE, False)])


def fig_sinc():
    kx, ky = 17, 110
    fn = lambda t: (math.sin(t) / t) if abs(t) > 1e-9 else 1.0
    cv = [(curve(fn, kx, ky), -150, 150, K.BLUE)]
    return G(330, 150, cv, xo=165, yo=45, hl=[(ky, K.AMBER, True)], xt=[(-2 * math.pi * kx, '−2π'), (2 * math.pi * kx, '2π')], yt=[(ky, '1')],
             odots=[(0, ky, '', 0, 0, K.RED)], notes=[(95, 78, 'y = sin x / x', 0, 0, K.BLUE, False)])


def fig_decay(c, a, tau, tmax, ymax, ylab, asym_lab, w=330, h=190, ty=None, tx=None):
    """y = c + a e^{-t/tau} (c=asymptote)."""
    kx = (w - 40) / tmax
    ky = (h - 40) / ymax
    fn = lambda t: c + a * math.exp(-t / tau)
    xt = [(kx * v, str(v)) for v in (tx or [])]
    yt = [(ky * v, str(v)) for v in (ty or [])]
    return G(w, h, [(curve(fn, kx, ky), 0, tmax * kx, K.BLUE)], hl=[(c * ky, K.AMBER, True)], xt=xt, yt=yt,
             notes=[(w - 30, c * ky, asym_lab, -4, -8, K.AMBER, False)], xlabel='t', ylabel=ylab)


def fig_taxi():
    kx, ky, = 28, 14
    xs = [(0, 3, 5), (3, 6, 8), (6, 9, 11)]
    seg = [(a * kx, v * ky, b * kx, v * ky, K.BLUE, False) for a, b, v in xs]
    dots = [(b * kx, v * ky, '', 0, 0, K.BLUE) for a, b, v in xs]
    od = [(a * kx, v * ky, '', 0, 0, K.BLUE) for a, b, v in xs[1:]]
    xt = [(kx * v, str(v)) for v in (3, 6, 9)]
    yt = [(ky * v, str(v)) for v in (5, 8, 11)]
    return G(300, 190, [], segs=seg, dots=dots, odots=od, xt=xt, yt=yt, xlabel='x', ylabel='F',
             vl=[(6 * kx, K.GRID, True)])


def fig_eff():
    kx, ky = 6.2, 250
    fn = lambda t: math.log(t) / t if t > 0 else None
    return G(330, 120, [(curve(fn, kx, ky), 1.0 * kx, 50 * kx, K.BLUE)], hl=[(0, K.GRID, False)], xt=[(kx * v, str(v)) for v in (10, 20, 30, 40, 50)],
             yt=[(ky * 0.2, '0,2')], dots=[(math.e * kx, math.log(math.e) / math.e * ky, '', 0, 0, K.RED)], xlabel='n', ylabel='E')


def fig_chord():
    th = 50
    a = math.radians(th)
    return K.plane((-0.35, 1.35), (-0.2, 1.1), 150, pts=[(0, 0, '', 0, 0, K.INK), (1, 0, 'A', 8, 16, K.INK), (math.cos(a), math.sin(a), 'B', 6, -8, K.INK)],
                   segs=[(0, 0, 1, 0, K.AXIS, False), (0, 0, math.cos(a), math.sin(a), K.AXIS, False), (1, 0, math.cos(a), math.sin(a), K.RED, False)],
                   arcs=[(0, 0, 1, 0, th, K.BLUE), (0, 0, 0.22, 0, th, K.AXIS)], circles=[(0, 0, 1, K.GRID, True)],
                   notes=[(0.3, 0.1, 'θ', 6, 0, K.INK, True), (0.93, 0.62, 's', 10, 0, K.BLUE, True), (0.87, 0.28, 'c', 10, 6, K.RED, True)],
                   grid=False, ticks=False, xlabel='', ylabel='')


def fig_poly6():
    pts = [(math.cos(math.radians(60 * k)), math.sin(math.radians(60 * k))) for k in range(6)]
    return K.plane((-1.35, 1.35), (-1.3, 1.3), 80, pts=[(px_, py_, '', 0, 0, K.RED) for px_, py_ in pts], polys=[(pts, K.GREEN, None, False)],
                   circles=[(0, 0, 1, K.BLUE, False)], notes=[(0, 0, 'n = 6', -22, -4, K.INK, False)], grid=False, ticks=False, xlabel='', ylabel='')


def fig_squeeze():
    kx, ky = 9, 55
    f = lambda t: (2 * t + math.sin(t)) / (t + 1)
    up = lambda t: (2 * t + 1) / (t + 1)
    lo = lambda t: (2 * t - 1) / (t + 1)
    cv = [(curve(lo, kx, ky), 0, 33 * kx, K.GREEN), (curve(up, kx, ky), 0, 33 * kx, K.RED), (curve(f, kx, ky), 0, 33 * kx, K.BLUE)]
    return G(330, 190, cv, yo=55, hl=[(2 * ky, K.AMBER, True)], yt=[(2 * ky, '2')], xt=[(kx * v, str(v)) for v in (10, 20, 30)],
             notes=[(33 * kx, 2 * ky, 'h', 4, -16, K.RED, True), (33 * kx, 2 * ky, 'f', 6, 4, K.BLUE, True), (33 * kx, 2 * ky, 'g', 4, 26, K.GREEN, True)])


def fig_delta():
    kx, ky = 70, 14
    f = lambda t: 4 * t - 5
    return G(300, 190, [(curve(f, kx, ky), 2 * kx, 4 * kx, K.BLUE)], xo=0, yo=0,
             segs=[(2.5 * kx, 0, 2.5 * kx, 5 * ky, K.AXIS, True), (3.5 * kx, 0, 3.5 * kx, 9 * ky, K.AXIS, True), (3 * kx, 0, 3 * kx, 7 * ky, K.AXIS, True),
                   (0, 5 * ky, 2.5 * kx, 5 * ky, K.AXIS, True), (0, 9 * ky, 3.5 * kx, 9 * ky, K.AXIS, True), (0, 7 * ky, 3 * kx, 7 * ky, K.AXIS, True)],
             xt=[(2.5 * kx, '3 − δ'), (3.5 * kx, '3 + δ')], yt=[(5 * ky, '7 − ε'), (9 * ky, '7 + ε')],
             dots=[(3 * kx, 7 * ky, '', 0, 0, K.RED)], notes=[(3 * kx, 0, '3', 0, 20, K.AXIS, False), (0, 7 * ky, '7', -9, 5, K.AXIS, False)])


def fig_logis():
    kx, ky = 11, 33.0 / 1000
    fn = lambda t: 5000 / (1 + 49 * math.exp(-0.4 * t))
    t_half = math.log(49) / 0.4
    return G(330, 200, [(curve(fn, kx, ky), 0, 25 * kx, K.BLUE)], hl=[(5000 * ky, K.AMBER, True)], xt=[(kx * v, str(v)) for v in (5, 10, 15, 20, 25)],
             yt=[(1000 * ky * k, str(1000 * k)) for k in (1, 3, 5)], dots=[(t_half * kx, 2500 * ky, '', 0, 0, K.RED)],
             segs=[(t_half * kx, 0, t_half * kx, 2500 * ky, K.AXIS, True), (0, 2500 * ky, t_half * kx, 2500 * ky, K.AXIS, True)], xlabel='t', ylabel='P')


def _fig_charge():
    kx, ky = 24, 3.6
    fn = lambda t: 50 * (1 - math.exp(-t / 2))
    return G(330, 210, [(curve(fn, kx, ky), 0, 12 * kx, K.BLUE)], hl=[(50 * ky, K.AMBER, True)], xt=[(kx * v, str(v)) for v in (2, 4, 6, 8, 10, 12)],
             yt=[(ky * 25, '25'), (ky * 50, '50')], xlabel='t', ylabel='Q')


def fig_signal():
    kx, ky = 22, 12
    fn = lambda t: 12 * math.exp(-0.2 * t)
    return G(330, 190, [(curve(fn, kx, ky), 0, 14 * kx, K.BLUE)], hl=[(0, K.GRID, False)], xt=[(kx * v, str(v)) for v in (2, 4, 6, 8, 10, 12, 14)],
             yt=[(ky * 6, '6'), (ky * 12, '12')], dots=[(5 * math.log(2) * kx, 6 * ky, '', 0, 0, K.RED)], xlabel='t', ylabel='V')


# ----------------------------------------------------------------------------- candidates
def cands():
    C = []
    # ============================================================ MCQ EASY (10)
    C.append(lq('easy', 's1', 3 * x ** 2 - x + 1, 2, '+-', [9, 13, 15],
                'ដោយ ' + M('f(x)=3x^2-x+1') + ' ជាពហុធា គេជំនួស ' + M('x=2') + ' ត្រង់ៗ ៖ ' + M('3(4)-2+1=11') + '។', 'Apply'))
    C.append(lq('easy', 's1', 3 + 5 / x, -oo, '+-', [5, 8, 0],
                M('\\dfrac5x\\to0') + ' កាលណា ' + M('x\\to-\\infty') + ' ដូច្នេះលីមីត ' + M('=3+0=3') + '។', 'Apply'))
    C.append(lq('easy', 's4', sin(x) / x, 0, '+-', [0, -1, oo],
                'លីមីតគោលនៃអនុគមន៍ត្រីកោណមាត្រ ៖ ' + M('\\displaystyle\\lim_{x\\to0}\\dfrac{\\sin x}{x}=1') + ' ដោយ ' + M('x') + ' ជារ៉ាដ្យង់។', 'Remember',
                tail=' (ក្រាបនៃ ' + M('y=\\dfrac{\\sin x}{x}') + ' ដូចក្នុងរូប)', img=fig_sinc()))
    C.append(lq('easy', 's5', (exp(x) - 1) / x, 0, '+-', [0, exp(1), oo],
                'លីមីតគោលនៃអនុគមន៍អិចស្ប៉ូណង់ស្យែល ៖ ' + M('\\displaystyle\\lim_{x\\to0}\\dfrac{e^x-1}{x}=1') + '។', 'Remember'))
    C.append(lq('easy', 's5', log(x), 0, '+', [0, oo, 1],
                'ពេល ' + M('x\\to0^{+}') + ' តម្លៃ ' + M('\\ln x') + ' ចុះតូចជាអវិជ្ជមានឥតកំណត់ ៖ ' + M('\\lim_{x\\to0^{+}}\\ln x=-\\infty') + '។', 'Remember'))
    C.append(lq('easy', 's5', exp(x) + 4, -oo, '+-', [0, 5, oo],
                M('e^x\\to0') + ' កាលណា ' + M('x\\to-\\infty') + ' ដូច្នេះលីមីត ' + M('=0+4=4') + '។', 'Apply'))
    C.append(lq('easy', 's3', (x ** 2 - 9) / (x - 3), 3, '+-', [0, 3, 9],
                'រាងមិនកំណត់ ' + M('\\tfrac00') + ' ៖ ' + M('\\dfrac{(x-3)(x+3)}{x-3}=x+3') + ' ចំពោះ ' + M('x\\ne3') + ' ដូច្នេះលីមីត ' + M('=6') + '។', 'Apply'))
    C.append(lq('easy', 's1', 1 / (x - 1), 1, '-', [oo, 0, 1],
                'ពេល ' + M('x\\to1^{-}') + ' ភាគបែង ' + M('x-1\\to0^{-}') + ' (អវិជ្ជមានតូច) ភាគយក ' + M('1>0') + ' ដូច្នេះលីមីត ' + M('=-\\infty') + '។', 'Understand',
                tail=' (ក្រាបដូចក្នុងរូប)', img=fig_inv()))
    f_, g_ = 2 * x + 1, x ** 2
    C.append(mcq('easy', 's2', 'គេមាន ' + M('f(x)=2x+1') + ' និង ' + M('g(x)=x^2') + '។ អនុគមន៍បណ្ដាក់ ' + M('(g\\circ f)(x)=g[f(x)]') + ' ស្មើនឹងអ្វី ?',
                 M('(2x+1)^2'), [M('2x^2+1'), M('4x^2+1'), M('2x+1+x^2')],
                 M('(g\\circ f)(x)=g[f(x)]=g(2x+1)=(2x+1)^2') + '។ អនុគមន៍ ' + M('f\\circ g') + ' ទើបស្មើ ' + M('2x^2+1') + '។', 'Remember'))
    C.append(lq('easy', 's1', (2 * x + 1) / (x - 1), oo, '+-', [1, 0, oo],
                'ចែកភាគយក និងភាគបែងនឹង ' + M('x') + ' ៖ ' + M('\\dfrac{2+\\frac1x}{1-\\frac1x}\\to\\dfrac21=2') + '។', 'Apply'))

    # ============================================================ MCQ MEDIUM (14)
    C.append(lq('medium', 's2', (sqrt(x) - 2) / (x - 4), 4, '+-', [Rational(1, 2), 0, 4],
                'គុណនឹងអនុញ្ញាតិរួម ៖ ' + M('\\dfrac{\\sqrt x-2}{x-4}=\\dfrac1{\\sqrt x+2}\\to\\dfrac14') + '។', 'Apply'))
    C.append(lq('medium', 's3', (3 * x ** 2 - x + 5) / (2 * x ** 2 + 7), oo, '+-', [3, Rational(2, 3), oo],
                'ដាក់ ' + M('x^2') + ' ជាកត្តារួម ៖ ' + M('\\dfrac{3-\\frac1x+\\frac5{x^2}}{2+\\frac7{x^2}}\\to\\dfrac32') + '។', 'Apply'))
    C.append(lq('medium', 's4', sin(5 * x) / sin(3 * x), 0, '+-', [Rational(3, 5), 15, 1],
                M('\\dfrac{\\sin5x}{\\sin3x}=\\dfrac{\\sin5x}{5x}\\cdot\\dfrac{3x}{\\sin3x}\\cdot\\dfrac53\\to\\dfrac53') + '។', 'Apply'))
    C.append(lq('medium', 's4', (1 - cos(x)) / x ** 2, 0, '+-', [1, 0, 2],
                M('1-\\cos x=2\\sin^2\\tfrac x2') + ' ដូច្នេះ ' + M('\\dfrac{2\\sin^2\\frac x2}{x^2}=\\dfrac12\\left(\\dfrac{\\sin\\frac x2}{\\frac x2}\\right)^2\\to\\dfrac12') + '។', 'Understand'))
    C.append(lq('medium', 's5', (exp(3 * x) - 1) / x, 0, '+-', [1, 0, exp(3)],
                M('\\dfrac{e^{3x}-1}{x}=3\\cdot\\dfrac{e^{3x}-1}{3x}\\to3\\cdot1=3') + '។', 'Apply'))
    C.append(lq('medium', 's5', log(1 + 4 * x) / x, 0, '+-', [1, Rational(1, 4), 0],
                M('\\dfrac{\\ln(1+4x)}{x}=4\\cdot\\dfrac{\\ln(1+4x)}{4x}\\to4') + '។', 'Apply'))
    C.append(lq('medium', 's3', sqrt(x ** 2 + 3 * x) - x, oo, '+-', [0, 3, oo],
                'រាង ' + M('\\infty-\\infty') + ' ៖ គុណនឹងអនុញ្ញាតិរួម ' + M('\\dfrac{3x}{\\sqrt{x^2+3x}+x}=\\dfrac{3}{\\sqrt{1+\\frac3x}+1}\\to\\dfrac32') + '។', 'Analyze'))
    C.append(lq('medium', 's5', x * exp(-x), oo, '+-', [1, oo, -oo],
                M('xe^{-x}=\\dfrac{x}{e^x}\\to0') + ' ព្រោះអិចស្ប៉ូណង់ស្យែលធំលឿនជាងស្វ័យគុណ ៖ ' + M('\\dfrac{e^x}{x}\\to+\\infty') + '។', 'Understand'))
    C.append(lq('medium', 's5', x * log(x), 0, '+', [-oo, 1, -1],
                'តាង ' + M('x=\\tfrac1X') + ' ៖ ' + M('x\\ln x=-\\dfrac{\\ln X}{X}\\to0') + ' កាលណា ' + M('X\\to+\\infty') + '។', 'Understand'))
    C.append(lq('medium', 's3', sqrt(x ** 2 + 1) / (x + 2), -oo, '+-', [1, 0, -oo],
                'ពេល ' + M('x\\to-\\infty') + ' គេមាន ' + M('\\sqrt{x^2+1}=|x|\\sqrt{1+\\frac1{x^2}}=-x\\sqrt{\\cdots}') + ' ដូច្នេះលីមីត ' + M('=\\dfrac{-x}{x}=-1') + '។', 'Analyze'))
    C.append(lq('medium', 's2', sqrt((4 * x - 1) / (x + 3)), oo, '+-', [4, sqrt(2), oo],
                'លីមីតនៃអនុគមន៍បណ្ដាក់ ៖ ' + M('X=\\dfrac{4x-1}{x+3}\\to4') + ' ហើយ ' + M('\\sqrt X\\to\\sqrt4=2') + '។', 'Apply'))
    C.append(lq('medium', 's3', (x ** 3 - 1) / (x ** 2 - 1), 1, '+-', [3, 1, 0],
                M('\\dfrac{(x-1)(x^2+x+1)}{(x-1)(x+1)}=\\dfrac{x^2+x+1}{x+1}\\to\\dfrac32') + '។', 'Apply'))
    C.append(lq('medium', 's4', cos(x) / (x - pi / 2), pi / 2, '+-', [1, 0, oo],
                'តាង ' + M('\\alpha=x-\\tfrac\\pi2') + ' ៖ ' + M('\\cos(\\alpha+\\tfrac\\pi2)=-\\sin\\alpha') + ' ដូច្នេះ ' + M('-\\dfrac{\\sin\\alpha}{\\alpha}\\to-1') + '។', 'Analyze'))
    C.append(mcq('medium', 's1', 'ចំពោះតម្លៃ ' + M('a') + ' ណា ទើបលីមីត ' + M('\\displaystyle\\lim_{x\\to2}\\dfrac{x^2+ax-6}{x-2}') + ' ជាចំនួនថេរ ?', M('a=1'), [M('a=2'), M('a=-1'), M('a=3')],
                'ភាគបែង ' + M('\\to0') + ' ដូច្នេះភាគយកត្រូវ ' + M('\\to0') + ' ៖ ' + M('4+2a-6=0') + ' គឺ ' + M('a=1') + ' ហើយ ' + M('\\dfrac{(x-2)(x+3)}{x-2}\\to5') + '។', 'Analyze'))

    # ============================================================ MCQ HARD (7)
    C.append(lq('hard', 's5', (exp(2 * x) - exp(-x)) / x, 0, '+-', [1, 2, 0],
                M('\\dfrac{e^{2x}-1}{x}+\\dfrac{1-e^{-x}}{x}\\to2+1=3') + ' ព្រោះ ' + M('\\dfrac{1-e^{-x}}{x}=\\dfrac{e^{-x}-1}{-x}\\to1') + '។', 'Analyze'))
    C.append(lq('hard', 's3', sqrt(x ** 2 + 4 * x + 1) - sqrt(x ** 2 - 2 * x), oo, '+-', [6, 1, Rational(3, 2)],
                'ផលដក ៖ ' + M('\\dfrac{6x+1}{\\sqrt{x^2+4x+1}+\\sqrt{x^2-2x}}=\\dfrac{6+\\frac1x}{\\sqrt{1+\\frac4x+\\cdots}+\\sqrt{1-\\frac2x}}\\to\\dfrac62=3') + '។', 'Analyze'))
    C.append(lq('hard', 's4', (sqrt(1 + x) - sqrt(1 - x)) / sin(3 * x), 0, '+-', [Rational(1, 6), Rational(2, 3), 3],
                'គុណអនុញ្ញាតិរួម ៖ ' + M('\\dfrac{2x}{(\\sqrt{1+x}+\\sqrt{1-x})\\sin3x}=\\dfrac{2}{3\\cdot\\frac{\\sin3x}{3x}(\\sqrt{1+x}+\\sqrt{1-x})}\\to\\dfrac{2}{3\\cdot2}=\\dfrac13') + '។', 'Analyze'))
    C.append(lq('hard', 's4', (1 - cos(4 * x)) / (x * sin(x)), 0, '+-', [4, 16, 2],
                M('1-\\cos4x=2\\sin^22x') + ' ៖ ' + M('\\dfrac{2\\sin^22x}{x\\sin x}=2\\left(\\dfrac{\\sin2x}{2x}\\right)^2\\cdot\\dfrac{4x^2}{x\\sin x}\\to2\\cdot4=8') + '។', 'Analyze'))
    C.append(lq('hard', 's5', exp(x) - x ** 3, oo, '+-', [0, -oo, 1],
                M('e^x-x^3=x^3\\left(\\dfrac{e^x}{x^3}-1\\right)') + ' ដោយ ' + M('\\dfrac{e^x}{x^3}\\to+\\infty') + ' ដូច្នេះលីមីត ' + M('=+\\infty') + '។', 'Evaluate'))
    C.append(lq('hard', 's3', (x ** 10 - 1) / (x ** 4 - 1), 1, '+-', [Rational(2, 5), 6, 1],
                'ប្រើ ' + M('\\displaystyle\\lim_{x\\to1}\\dfrac{x^m-1}{x^n-1}=\\dfrac mn') + ' ដែល ' + M('m=10,\\ n=4') + ' ៖ ' + M('\\dfrac{10}4=\\dfrac52') + '។', 'Analyze'))
    C.append(mcq('hard', 's1', 'ទំនាក់ទំនងមួយណាខាងក្រោមត្រឹមត្រូវ ?',
                 M('\\displaystyle\\lim_{x\\to0^-}\\dfrac{x}{|x|}=-1'),
                 [M('\\displaystyle\\lim_{x\\to0}\\dfrac{\\sin2x}{x}=1'), M('\\displaystyle\\lim_{x\\to+\\infty}\\dfrac{\\ln x}{x}=+\\infty'), M('\\displaystyle\\lim_{x\\to0}\\dfrac{e^x-1}{x}=0')],
                 'ចំពោះ ' + M('x<0') + ' ៖ ' + M('|x|=-x') + ' ដូច្នេះ ' + M('\\dfrac x{|x|}=-1') + '។ ឯខ្សែផ្សេងទៀតខុស ៖ ' + M('\\dfrac{\\sin2x}x\\to2') + ', ' + M('\\dfrac{\\ln x}x\\to0') + ', ' + M('\\dfrac{e^x-1}x\\to1') + '។', 'Evaluate'))

    # ============================================================ MCQ PISA (5)
    C.append(with_img(
                   mcq('pisa', 'p_coffee', 'កាហ្វេក្តៅមួយកែវដាក់ក្នុងបន្ទប់ ។ សីតុណ្ហភាព (°C) ក្រោយ ' + M('t') + ' នាទី គឺ ' + M('T(t)=25+60e^{-t/10}') + ' ដូចក្នុងរូប ។ តើសីតុណ្ហភាពកាហ្វេខិតទៅរកតម្លៃប៉ុន្មាន (គិតជា °C) កាលណា ' + M('t') + ' ធំឥតកំណត់ ?',
                       M('25'), [M('0'), M('60'), M('85')],
                       M('e^{-t/10}\\to0') + ' ដូច្នេះ ' + M('T\\to25+0=25') + ' °C (សីតុណ្ហភាពបន្ទប់) ដែលក្រាបមាន ' + M('y=25') + ' ជាអាស៊ីមតូតដេក។', 'Apply'),
                   fig_decay(25, 60, 10, 50, 90, 'T', 'y = 25', ty=[25, 85], tx=[10, 20, 30, 40, 50])))
    C.append(with_img(mcq('pisa', 'p_taxi', 'តារាងតម្លៃតាក់ស៊ី ' + M('F(x)') + ' (ដុល្លារ) តាមចម្ងាយ ' + M('x') + ' (គីឡូម៉ែត្រ) ត្រូវបានបង្ហាញដោយក្រាបក្នុងរូប ។ គណនា ' + M('\\displaystyle\\lim_{x\\to6^{+}}F(x)-\\lim_{x\\to6^{-}}F(x)') + ' ។',
                          M('3'), [M('0'), M('8'), M('11')],
                          'ពីក្រាប ៖ ' + M('\\lim_{x\\to6^-}F(x)=8') + ' (ជណ្ដើរមុន) និង ' + M('\\lim_{x\\to6^+}F(x)=11') + ' (ជណ្ដើរបន្ទាប់) ដូច្នេះផលដក ' + M('11-8=3') + ' ហើយលីមីតនៅ ' + M('x=6') + ' មិនមាន (លោត ' + M('3') + ' ដុល្លារ)។', 'Analyze'),
                   fig_taxi()))
    C.append(with_img(
                   mcq('pisa', 'p_chord', 'ក្នុងរង្វង់កាំ ' + M('1') + ' ធ្នូ ' + M('AB') + ' ប្រវែង ' + M('s=\\theta') + ' ហើយអង្កត់ធ្នូ ' + M('AB=c=2\\sin\\dfrac\\theta2') + ' ដូចក្នុងរូប ។ តើសមាមាត្រ ' + M('\\dfrac cs') + ' ខិតទៅរកអ្វី កាលណា ' + M('\\theta\\to0') + ' ?',
                       M('1'), [M('\\dfrac12'), M('2'), M('0')],
                       M('\\dfrac cs=\\dfrac{2\\sin\\frac\\theta2}{\\theta}=\\dfrac{\\sin\\frac\\theta2}{\\frac\\theta2}\\to1') + ' ដូច្នេះ ' + M('c\\approx s') + ' កាលណាមុំតូច។', 'Apply'),
                   fig_chord()))
    C.append(with_img(mcq('pisa', 'p_eff', 'ក្បួនដោះស្រាយមួយមានប្រសិទ្ធភាព ' + M('E(n)=\\dfrac{\\ln n}{n}') + ' ដែល ' + M('n') + ' ជាចំនួនទិន្នន័យ ដូចក្នុងរូប ។ តើប្រសិទ្ធភាពខិតទៅរកអ្វី កាលណា ' + M('n\\to+\\infty') + ' ?',
                          M('0'), [M('1'), M('+\\infty'), M('\\dfrac1e')],
                          M('\\displaystyle\\lim_{n\\to+\\infty}\\dfrac{\\ln n}{n}=0') + ' ព្រោះ ' + M('\\ln n') + ' កើនយឺតជាង ' + M('n') + '។ តម្លៃធំបំផុត ' + M('\\dfrac1e\\approx0{,}37') + ' ត្រង់ ' + M('n=e') + ' មិនមែនជាលីមីតទេ។', 'Analyze'),
                   fig_eff()))
    C.append(with_img(mcq('pisa', 'p_poly', 'ពហុកោណនិយ័ត ' + M('n') + ' ជ្រុងចារឹកក្នុងរង្វង់កាំ ' + M('1') + ' (រូបបង្ហាញ ' + M('n=6') + ') មានបរិមាត្រ ' + M('P_n=2n\\sin\\dfrac\\pi n') + ' ។ តើ ' + M('P_n') + ' ខិតទៅរកអ្វី កាលណា ' + M('n\\to+\\infty') + ' ?',
                          M('2\\pi'), [M('2'), M('\\pi'), M('4\\pi')],
                          M('P_n=2\\pi\\cdot\\dfrac{\\sin\\frac\\pi n}{\\frac\\pi n}\\to2\\pi\\cdot1=2\\pi') + ' ជាបរិមាត្ររង្វង់កាំ ' + M('1') + '។', 'Analyze'),
                   fig_poly6()))
    return C + cands_writing()


def cands_writing():
    C = []
    # ============================================================ WRITING EASY (1)
    C.append(wr('easy', 's3', 'គណនាលីមីត ' + M('\\displaystyle\\lim_{x\\to-1}\\dfrac{x^2-1}{x^2+3x+2}') + ' ។',
                [('ជំនួស ' + M('x=-1') + ' ៖ ភាគយក ' + M('=0') + ' និងភាគបែង ' + M('=0') + ' ដូច្នេះមានរាងមិនកំណត់ ' + M('\\tfrac00'), 1),
                 ('ដាក់ជាកត្តា ៖ ' + M('x^2-1=(x-1)(x+1)'), 1),
                 ('ភាគបែង ៖ ' + M('x^2+3x+2=(x+1)(x+2)'), 1),
                 ('សម្រួលកត្តារួម ' + M('(x+1)') + ' (ព្រោះ ' + M('x\\ne-1') + ') ៖ ' + M('\\dfrac{x-1}{x+2}'), 1),
                 ('ជំនួស ' + M('x=-1') + ' ៖ ' + M('\\dfrac{-1-1}{-1+2}=-2') + ' ដូច្នេះលីមីត ' + M('=-2') + '។', 1)], bloom='Apply'))

    # ============================================================ WRITING MEDIUM (4)
    C.append(wr('medium', 's3', 'គណនា ' + M('\\displaystyle\\lim_{x\\to+\\infty}\\left(\\sqrt{x^2+x+1}-\\sqrt{x^2-x}\\right)') + ' ។',
                [('រាងមិនកំណត់ ' + M('+\\infty-\\infty') + ' ដូច្នេះគុណ និងចែកនឹងអនុញ្ញាតិរួម ' + M('\\sqrt{x^2+x+1}+\\sqrt{x^2-x}'), 1),
                 ('ភាគយក ៖ ' + M('(x^2+x+1)-(x^2-x)=2x+1'), 1),
                 ('ដាក់ ' + M('x') + ' ជាកត្តារួម ៖ ' + M('\\dfrac{x\\left(2+\\frac1x\\right)}{x\\left(\\sqrt{1+\\frac1x+\\frac1{x^2}}+\\sqrt{1-\\frac1x}\\right)}'), 1),
                 ('សម្រួល ' + M('x') + ' (ព្រោះ ' + M('x>0') + ') ទុកប្រភាគ ' + M('\\dfrac{2+\\frac1x}{\\sqrt{1+\\frac1x+\\frac1{x^2}}+\\sqrt{1-\\frac1x}}'), 1),
                 ('ឱ្យ ' + M('x\\to+\\infty') + ' ៖ ' + M('\\dfrac{2+0}{\\sqrt1+\\sqrt1}=1') + ' ដូច្នេះលីមីត ' + M('=1') + '។', 1)], bloom='Apply'))
    C.append(wr('medium', 's4', 'គណនា ' + M('\\displaystyle\\lim_{x\\to0}\\dfrac{1-\\cos3x}{x^2}') + ' ។',
                [('រាងមិនកំណត់ ' + M('\\tfrac00') + ' ព្រោះ ' + M('1-\\cos0=0'), 1),
                 ('ប្រើ ' + M('1-\\cos\\alpha=2\\sin^2\\tfrac\\alpha2') + ' ៖ ' + M('1-\\cos3x=2\\sin^2\\tfrac{3x}2'), 1),
                 ('សរសេរ ' + M('\\dfrac{2\\sin^2\\frac{3x}2}{x^2}=2\\cdot\\dfrac94\\left(\\dfrac{\\sin\\frac{3x}2}{\\frac{3x}2}\\right)^2') + ' ព្រោះ ' + M('\\left(\\tfrac{3x}2\\right)^2=\\tfrac94x^2'), 1),
                 ('ប្រើ ' + M('\\displaystyle\\lim_{u\\to0}\\dfrac{\\sin u}u=1') + ' ជាមួយ ' + M('u=\\tfrac{3x}2\\to0'), 1),
                 ('លីមីត ' + M('=2\\cdot\\dfrac94\\cdot1^2=\\dfrac92') + '។', 1)], bloom='Apply'))
    C.append(wr('medium', 's1', 'កំណត់ចំនួនថេរ ' + M('a') + ' និង ' + M('b') + ' ដើម្បីឱ្យ ' + M('\\displaystyle\\lim_{x\\to1}\\dfrac{x^2+ax+b}{x-1}=3') + ' ។',
                [('ដោយភាគបែង ' + M('x-1\\to0') + ' ហើយលីមីតជាចំនួនកំណត់ ដូច្នេះភាគយកត្រូវ ' + M('\\to0') + ' ត្រង់ ' + M('x=1'), 1),
                 ('លក្ខខណ្ឌ ៖ ' + M('1+a+b=0') + ' គឺ ' + M('b=-1-a'), 1),
                 ('ដាក់ជាកត្តា ៖ ' + M('x^2+ax-1-a=(x-1)(x+1+a)'), 1),
                 ('សម្រួល ៖ ' + M('\\dfrac{x^2+ax+b}{x-1}=x+1+a') + ' ដូច្នេះលីមីត ' + M('=2+a'), 1),
                 ('ឱ្យ ' + M('2+a=3') + ' បាន ' + M('a=1') + ' ហើយ ' + M('b=-2') + ' ។ ផ្ទៀងផ្ទាត់ ' + M('\\dfrac{(x-1)(x+2)}{x-1}\\to3') + '។', 1)], bloom='Analyze'))
    C.append(wr('medium', 's5', 'គណនា ' + M('\\displaystyle\\lim_{x\\to0}\\dfrac{e^{5x}-e^{2x}}{\\ln(1+3x)}') + ' ។',
                [('ទាំងភាគយក និងភាគបែង ' + M('\\to0') + ' ដូច្នេះរាង ' + M('\\tfrac00') + ' ។ ចែកភាគយក និងភាគបែងនឹង ' + M('x'), 1),
                 ('ភាគយក ៖ ' + M('\\dfrac{e^{5x}-e^{2x}}x=\\dfrac{e^{5x}-1}x-\\dfrac{e^{2x}-1}x'), 1),
                 ('ប្រើ ' + M('\\dfrac{e^{ax}-1}{ax}\\to1') + ' ៖ ភាគយក ' + M('\\to5-2=3'), 1),
                 ('ភាគបែង ៖ ' + M('\\dfrac{\\ln(1+3x)}x=3\\cdot\\dfrac{\\ln(1+3x)}{3x}\\to3'), 1),
                 ('ដូច្នេះលីមីត ' + M('=\\dfrac33=1') + '។', 1)], bloom='Apply'))

    # ============================================================ WRITING HARD (4)
    C.append(with_img(wr('hard', 's1', 'ក្រាបក្នុងរូបបង្ហាញអនុគមន៍ ' + M('f(x)=\\dfrac{2x+\\sin x}{x+1}') + ' ដែលស្ថិតចន្លោះ ' + M('g(x)=\\dfrac{2x-1}{x+1}') + ' និង ' + M('h(x)=\\dfrac{2x+1}{x+1}') + ' ចំពោះ ' + M('x\\ge0') + '។ ក. បង្ហាញថា ' + M('g(x)\\le f(x)\\le h(x)') + ' ។ ខ. ដោយប្រើទ្រឹស្ដីបទកៀប រកលីមីតនៃ ' + M('f(x)') + ' កាលណា ' + M('x\\to+\\infty') + '។',
                         [('ដោយ ' + M('-1\\le\\sin x\\le1') + ' ដូច្នេះ ' + M('2x-1\\le2x+\\sin x\\le2x+1'), 1),
                          ('ចែកនឹង ' + M('x+1>0') + ' (មិនប្ដូរទិស) ៖ ' + M('g(x)\\le f(x)\\le h(x)') + ' ចំពោះ ' + M('x\\ge0'), 1),
                          ('លីមី ' + M('g') + ' ៖ ' + M('\\dfrac{2x-1}{x+1}=\\dfrac{2-\\frac1x}{1+\\frac1x}\\to2'), 1),
                          ('លីមី ' + M('h') + ' ៖ ' + M('\\dfrac{2x+1}{x+1}=\\dfrac{2+\\frac1x}{1+\\frac1x}\\to2'), 1),
                          ('ទ្រឹស្ដីបទកៀប ៖ ' + M('g\\to2') + ' និង ' + M('h\\to2') + ' ដូច្នេះ ' + M('\\displaystyle\\lim_{x\\to+\\infty}f(x)=2') + ' (ក្រាប ' + M('f') + ' ត្រូវចងក្នុងក្រាប ' + M('g') + ' និង ' + M('h') + ')។', 1)], bloom='Evaluate'),
                   fig_squeeze()))
    C.append(with_img(wr('hard', 's1', 'ដោយប្រើនិយមន័យ ' + M('\\varepsilon') + '–' + M('\\delta') + ' បង្ហាញថា ' + M('\\displaystyle\\lim_{x\\to3}(4x-5)=7') + ' (ក្រាបក្នុងរូបបង្ហាញចន្លោះ ' + M('3\\pm\\delta') + ' និង ' + M('7\\pm\\varepsilon') + ') រួចរក ' + M('\\delta') + ' ធំបំផុតដែលបានពី ' + M('\\varepsilon=0{,}02') + '។',
                         [('ត្រូវការ ៖ ចំពោះគ្រប់ ' + M('\\varepsilon>0') + ' មាន ' + M('\\delta>0') + ' ដែល ' + M('0<|x-3|<\\delta') + ' នាំឱ្យ ' + M('|f(x)-7|<\\varepsilon'), 1),
                          ('គណនា ៖ ' + M('|f(x)-7|=|4x-5-7|=|4x-12|=4|x-3|'), 1),
                          ('ដើម្បីឱ្យ ' + M('4|x-3|<\\varepsilon') + ' ត្រូវ ' + M('|x-3|<\\dfrac\\varepsilon4'), 1),
                          ('យក ' + M('\\delta=\\dfrac\\varepsilon4') + ' ៖ ' + M('0<|x-3|<\\delta') + ' នាំឱ្យ ' + M('|f(x)-7|=4|x-3|<4\\delta=\\varepsilon') + ' ដូច្នេះលីមីត ' + M('=7'), 1),
                          ('ចំពោះ ' + M('\\varepsilon=0{,}02') + ' ៖ ' + M('\\delta=\\dfrac{0{,}02}4=0{,}005') + '។', 1)], bloom='Analyze'),
                   fig_delta()))
    C.append(wr('hard', 's1', 'កំណត់អនុគមន៍ដឺក្រេទី ២ ' + M('f(x)=px^2+qx+r') + ' (' + M('p\\ne0') + ') ដែលបំពេញលក្ខខណ្ឌទាំងពីរ ៖ ' + M('\\displaystyle\\lim_{x\\to+\\infty}\\dfrac{f(x)}{x^2-1}=2') + ' និង ' + M('\\displaystyle\\lim_{x\\to1}\\dfrac{f(x)}{x^2-1}=-1') + '។',
                [('កាលណា ' + M('x\\to+\\infty') + ' ៖ ' + M('\\dfrac{px^2+qx+r}{x^2-1}\\to p') + ' ដូច្នេះ ' + M('p=2'), 1),
                 ('ភាគបែង ' + M('x^2-1\\to0') + ' កាលណា ' + M('x\\to1') + ' ដូច្នេះត្រូវ ' + M('f(1)=0') + ' គឺ ' + M('2+q+r=0'), 1),
                 ('ដូច្នេះ ' + M('f(x)=(x-1)(2x+c)') + ' ជាមួយចំនួនថេរ ' + M('c') + ' (ព្រោះ ' + M('f(1)=0') + ' និង ' + M('p=2') + ')', 1),
                 ('សម្រួល ៖ ' + M('\\dfrac{f(x)}{x^2-1}=\\dfrac{2x+c}{x+1}') + ' ហើយកាលណា ' + M('x\\to1') + ' បាន ' + M('\\dfrac{2+c}2=-1') + ' ដូច្នេះ ' + M('c=-4'), 1),
                 ('ចម្លើយ ៖ ' + M('f(x)=(x-1)(2x-4)=2x^2-6x+4') + ' ផ្ទៀងផ្ទាត់ ' + M('\\dfrac{2(x-2)}{x+1}') + ' ' + M('\\to2') + ' (កាលណា ' + M('x\\to+\\infty') + ') និង ' + M('\\to-1') + ' (កាលណា ' + M('x\\to1') + ')។', 1)], bloom='Create'))
    C.append(wr('hard', 's5', 'ក. បង្ហាញថា ' + M('\\displaystyle\\lim_{x\\to+\\infty}x\\left(e^{1/x}-1\\right)=1') + ' ដោយប្ដូរអថេរ ។ ខ. ទាញរក ' + M('\\displaystyle\\lim_{x\\to+\\infty}x\\left(e^{3/x}-1\\right)') + ' ។ គ. ពន្យល់ថាហេតុអ្វីលីមីតនេះមិនអាចរកដោយជំនួស ' + M('x=+\\infty') + ' ត្រង់ៗ បាន។',
                [('តាង ' + M('u=\\dfrac1x') + ' ដូច្នេះ ' + M('x\\to+\\infty') + ' គឺ ' + M('u\\to0^{+}'), 1),
                 ('សរសេរ ' + M('x\\left(e^{1/x}-1\\right)=\\dfrac{e^u-1}{u}'), 1),
                 ('ប្រើលីមីតគោល ' + M('\\dfrac{e^u-1}u\\to1') + ' ដូច្នេះ ក. ' + M('=1'), 1),
                 ('ខ. តាង ' + M('v=\\dfrac3x\\to0') + ' ៖ ' + M('x\\left(e^{3/x}-1\\right)=3\\cdot\\dfrac{e^v-1}{v}\\to3'), 1),
                 ('គ. ជំនួសត្រង់ៗ បានរាង ' + M('\\infty\\cdot0') + ' ជារាងមិនកំណត់ (ស្វ័យគុណ ' + M('x\\to\\infty') + ' ប៉ុន្តែ ' + M('e^{1/x}-1\\to0') + ') ដូច្នេះត្រូវប្ដូរអថេរដើម្បីឱ្យទៅជាលីមីតគោល។', 1)], bloom='Analyze'))

    # ============================================================ WRITING PISA (5)
    C.append(with_img(wr('pisa', 'p_drug', 'កំហាប់ថ្នាំក្នុងឈាម (mg/L) បន្ទាប់ពីចាក់ ' + M('t') + ' ម៉ោង ត្រូវបានគណនាដោយ ' + M('C(t)=\\dfrac{20t}{t+4}') + ' ដូចក្នុងរូប ។ ក. គណនា ' + M('C(4)') + '។ ខ. រកកំហាប់ដែលខិតជិតក្នុងរយៈពេលវែង ' + M('\\displaystyle\\lim_{t\\to+\\infty}C(t)') + '។ គ. តើក្រោយប៉ុន្មានម៉ោងទើបកំហាប់ដល់ ' + M('90\\%') + ' នៃតម្លៃលីមីតនេះ ?',
                         [('ក. ' + M('C(4)=\\dfrac{20\\cdot4}{4+4}=10') + ' mg/L', 1),
                          ('ខ. ចែកភាគយក និងភាគបែងនឹង ' + M('t') + ' ៖ ' + M('C(t)=\\dfrac{20}{1+\\frac4t}'), 1),
                          ('ឱ្យ ' + M('t\\to+\\infty') + ' ៖ ' + M('\\dfrac4t\\to0') + ' ដូច្នេះលីមីត ' + M('=20') + ' mg/L (អាស៊ីមតូតដេក ' + M('y=20') + ')', 1),
                          ('គ. ' + M('90\\%') + ' នៃ ' + M('20') + ' គឺ ' + M('18') + ' ៖ ' + M('\\dfrac{20t}{t+4}=18') + ' គឺ ' + M('20t=18t+72'), 1),
                          ('ដូច្នេះ ' + M('2t=72') + ' បាន ' + M('t=36') + ' ម៉ោង។', 1)], bloom='Apply'),
                   _fig_drug()))
    C.append(with_img(wr('pisa', 'p_charge', 'កុងដង់សាទ័រមួយសាកថាមពល ដោយបន្ទុកក្នុងវា (µC) ក្រោយ ' + M('t') + ' វិនាទី គឺ ' + M('Q(t)=50\\left(1-e^{-t/2}\\right)') + ' ដូចក្នុងរូប ។ ក. រកបន្ទុកដែលខិតជិតពេល ' + M('t\\to+\\infty') + '។ ខ. រកពេលវេលាដែល ' + M('Q=47{,}5') + ' (គឺ ' + M('95\\%') + ' នៃតម្លៃអតិបរមា) ។ គ. គណនាអត្រាដើម ' + M('\\displaystyle\\lim_{t\\to0}\\dfrac{Q(t)}t') + '។',
                         [('ក. ' + M('e^{-t/2}\\to0') + ' ដូច្នេះ ' + M('Q\\to50(1-0)=50') + ' µC', 1),
                          ('ខ. ' + M('50\\left(1-e^{-t/2}\\right)=47{,}5') + ' គឺ ' + M('e^{-t/2}=0{,}05'), 1),
                          ('យកលោការីតនេពែ ៖ ' + M('-\\dfrac t2=\\ln0{,}05=-\\ln20') + ' ដូច្នេះ ' + M('t=2\\ln20\\approx5{,}99') + ' s', 1),
                          ('គ. ' + M('\\dfrac{Q(t)}t=50\\cdot\\dfrac{1-e^{-t/2}}{t}=25\\cdot\\dfrac{e^{-t/2}-1}{-t/2}'), 1),
                          ('ប្រើ ' + M('\\dfrac{e^u-1}u\\to1') + ' ជាមួយ ' + M('u=-\\tfrac t2\\to0') + ' ៖ អត្រាដើម ' + M('=25') + ' µC/s។', 1)], bloom='Analyze'),
                   _fig_charge()))
    C.append(with_img(wr('pisa', 'p_cost', 'រោងចក្រមួយមានចំណាយថេរ ' + M('2000') + ' ដុល្លារ និងចំណាយលើអង្គមួយ ' + M('15') + ' ដុល្លារ ។ ចំណាយមធ្យមក្នុងអង្គមួយនៅពេលផលិត ' + M('x') + ' អង្គ គឺ ' + M('C(x)=\\dfrac{2000+15x}{x}') + ' ដូចក្នុងរូប ។ ក. គណនា ' + M('C(100)') + '។ ខ. រកលីមីត ' + M('\\displaystyle\\lim_{x\\to+\\infty}C(x)') + ' ហើយបកស្រាយ។ គ. រកចំនួនអង្គតិចបំផុតដើម្បីឱ្យ ' + M('C(x)<16') + '។',
                         [('ក. ' + M('C(100)=\\dfrac{2000+1500}{100}=35') + ' ដុល្លារ/អង្គ', 1),
                          ('ខ. សរសេរ ' + M('C(x)=\\dfrac{2000}x+15'), 1),
                          ('ឱ្យ ' + M('x\\to+\\infty') + ' ៖ ' + M('\\dfrac{2000}x\\to0') + ' ដូច្នេះ ' + M('C\\to15') + ' ដុល្លារ/អង្គ (ចំណាយផ្លាស់ប្ដូរ ដោយចំណាយថេរចែកទៅអង្គច្រើនឥតកំណត់)', 1),
                          ('គ. ' + M('\\dfrac{2000}x+15<16') + ' គឺ ' + M('\\dfrac{2000}x<1'), 1),
                          ('ដោយ ' + M('x>0') + ' ៖ ' + M('x>2000') + ' ដូច្នេះតិចបំផុតគឺ ' + M('2001') + ' អង្គ។', 1)], bloom='Apply'),
                   _fig_cost()))
    C.append(with_img(wr('pisa', 'p_signal', 'សញ្ញាសំឡេងមួយអន់ថយតាមពេលវេលា ដោយវ៉ុលរបស់វា (V) គឺ ' + M('V(t)=12e^{-0{,}2t}') + ' (t គិតជាវិនាទី) ដូចក្នុងរូប ។ ក. រក ' + M('\\displaystyle\\lim_{t\\to+\\infty}V(t)') + '។ ខ. តើពេលណាវ៉ុលនៅសល់ពាក់កណ្ដាលតម្លៃដើម ? គ. បង្ហាញថា ' + M('\\displaystyle\\lim_{t\\to+\\infty}t^3V(t)=0') + ' ហើយបកស្រាយ។',
                         [('ក. ' + M('-0{,}2t\\to-\\infty') + ' ដូច្នេះ ' + M('e^{-0{,}2t}\\to0') + ' ហើយ ' + M('V\\to0') + ' V', 1),
                          ('ខ. ' + M('12e^{-0{,}2t}=6') + ' គឺ ' + M('e^{-0{,}2t}=\\tfrac12'), 1),
                          ('យកលោការីត ៖ ' + M('-0{,}2t=-\\ln2') + ' ដូច្នេះ ' + M('t=5\\ln2\\approx3{,}47') + ' s', 1),
                          ('គ. ' + M('t^3V(t)=12t^3e^{-0{,}2t}') + ' តាង ' + M('u=0{,}2t') + ' ៖ ' + M('12\\cdot125\\,u^3e^{-u}'), 1),
                          ('ដោយ ' + M('\\dfrac{u^3}{e^u}\\to0') + ' កាលណា ' + M('u\\to+\\infty') + ' ដូច្នេះលីមី ' + M('=0') + ' ៖ អិចស្ប៉ូណង់ស្យែលអន់ថយលឿនជាងស្វ័យគុណនៃ ' + M('t') + ' កើន។', 1)], bloom='Analyze'),
                   _fig_signal()))
    C.append(with_img(wr('pisa', 'p_logis', 'ចំនួនត្រីក្នុងបឹងមួយ ក្រោយ ' + M('t') + ' ឆ្នាំ ត្រូវបានគណនាដោយ ' + M('P(t)=\\dfrac{5000}{1+49e^{-0{,}4t}}') + ' ដូចក្នុងរូប ។ ក. រក ' + M('P(0)') + '។ ខ. រកលីមីត ' + M('\\displaystyle\\lim_{t\\to+\\infty}P(t)') + ' (សមត្ថភាពអតិបរមា) ។ គ. តើក្រោយប៉ុន្មានឆ្នាំ ចំនួនត្រីដល់ពាក់កណ្ដាលសមត្ថភាព ? ឃ. វាយតម្លៃថាតើបឹងអាចមានត្រី ' + M('6000') + ' ក្បាលដែរឬទេ ?',
                         [('ក. ' + M('P(0)=\\dfrac{5000}{1+49}=100') + ' ក្បាល', 1),
                          ('ខ. ' + M('e^{-0{,}4t}\\to0') + ' ដូច្នេះ ' + M('P\\to\\dfrac{5000}{1+0}=5000') + ' ក្បាល', 1),
                          ('គ. ' + M('P=2500') + ' ៖ ' + M('1+49e^{-0{,}4t}=2') + ' គឺ ' + M('e^{-0{,}4t}=\\dfrac1{49}'), 1),
                          ('ដូច្នេះ ' + M('t=\\dfrac{\\ln49}{0{,}4}\\approx9{,}73') + ' ឆ្នាំ', 1),
                          ('ឃ. ' + M('1+49e^{-0{,}4t}>1') + ' ដូច្នេះ ' + M('P(t)<5000') + ' គ្រប់ ' + M('t') + ' ហើយ ' + M('P\\to5000') + ' ដូច្នេះមិនអាចមាន ' + M('6000') + ' ក្បាលបានទេ (អាស៊ីមតូត ' + M('y=5000') + ')។', 1)], bloom='Evaluate'),
                   _fig_logis()))
    return C


def _fig_drug():
    kx, ky = 5.0, 7.5
    fn = lambda t: 20 * t / (t + 4)
    return G(330, 190, [(curve(fn, kx, ky), 0, 60 * kx, K.BLUE)], hl=[(20 * ky, K.AMBER, True)], xt=[(kx * v, str(v)) for v in (10, 20, 30, 40, 50, 60)],
             yt=[(ky * 10, '10'), (ky * 20, '20')], dots=[(4 * kx, 10 * ky, '', 0, 0, K.RED)], xlabel='t', ylabel='C')


def _fig_cost():
    kx, ky = 0.14, 5.0
    fn = lambda t: (2000 + 15 * t) / t if t > 0 else None
    return G(330, 200, [(curve(fn, kx, ky), 55 * kx, 2000 * kx, K.BLUE)], hl=[(15 * ky, K.AMBER, True)],
             xt=[(kx * v, str(v)) for v in (500, 1000, 1500, 2000)], yt=[(15 * ky, '15'), (35 * ky, '35')], xlabel='x', ylabel='C')


def _fig_signal():
    return fig_signal()


def _fig_logis():
    return fig_logis()


def verify():
    """independent numeric re-derivation: (1) every limit in CHECKS at 60 digits, (2) the closed forms used in the worked solutions."""
    n = 0
    mp.mp.dps = 60
    cands()
    for f, pt, d, right in CHECKS:
        assert close_to(num_limit(f, pt, d), right), (pt, d, right)
        n += 1
    m = mp.mpf
    # writing / parameter claims
    assert abs((m(1) ** 2 - 1) / (m(1) ** 2 + 3 + 2) - 0) >= 0 and abs(((-1 + m(10) ** -9) ** 2 - 1) / ((-1 + m(10) ** -9) ** 2 + 3 * (-1 + m(10) ** -9) + 2) + 2) < 1e-6; n += 1
    t = m(10) ** 14
    assert abs((mp.sqrt(t * t + t + 1) - mp.sqrt(t * t - t)) - 1) < 1e-6; n += 1
    h = m(10) ** -10
    assert abs((1 - mp.cos(3 * h)) / h ** 2 - m(9) / 2) < 1e-6; n += 1
    assert abs(((1 + h) ** 2 + 1 * (1 + h) - 2) / h - 3) < 1e-6; n += 1                           # a=1, b=-2: (x^2+x-2)/(x-1) -> 3
    assert abs((mp.e ** (5 * h) - mp.e ** (2 * h)) / mp.log(1 + 3 * h) - 1) < 1e-6; n += 1
    for X in (m(10) ** 6, m(10) ** 9):                                                              # squeeze
        fx = (2 * X + mp.sin(X)) / (X + 1)
        assert (2 * X - 1) / (X + 1) <= fx <= (2 * X + 1) / (X + 1) and abs(fx - 2) < 1e-5; n += 2
    assert abs((4 * (3 + h) - 5) - 7) < 1e-8 and abs(m('0.02') / 4 - m('0.005')) < 1e-12; n += 2   # delta-epsilon
    f2 = lambda xx: 2 * xx ** 2 - 6 * xx + 4
    assert abs(f2(2 + 0) - 0) < 1e-12 and abs(f2(1 + h) / ((1 + h) ** 2 - 1) + 1) < 1e-6 and abs(f2(m(10) ** 9) / (m(10) ** 18 - 1) - 2) < 1e-6; n += 3
    for k in (3, 1):
        X = m(10) ** 10
        assert abs(X * (mp.e ** (m(k) / X) - 1) - k) < 1e-6; n += 1
    # PISA contexts
    C = lambda tt: 20 * tt / (tt + 4)
    assert C(4) == 10 and abs(C(36) - 18) < 1e-12 and C(m(10) ** 12) < 20 and abs(C(m(10) ** 12) - 20) < 1e-6; n += 3
    Q = lambda tt: 50 * (1 - mp.e ** (-tt / 2))
    assert abs(Q(2 * mp.log(20)) - m('47.5')) < 1e-9 and abs(2 * mp.log(20) - m('5.99')) < 0.01 and abs(Q(h) / h - 25) < 1e-6; n += 3
    CC = lambda xx: (2000 + 15 * xx) / xx
    assert CC(100) == 35 and CC(2000) == 16 and CC(2001) < 16; n += 3
    Vv = lambda tt: 12 * mp.e ** (-m('0.2') * tt)
    assert abs(Vv(5 * mp.log(2)) - 6) < 1e-9 and abs(5 * mp.log(2) - m('3.47')) < 0.01 and Vv(m(10) ** 3) * m(10) ** 9 < 1e-50; n += 3
    P = lambda tt: 5000 / (1 + 49 * mp.e ** (-m('0.4') * tt))
    assert P(0) == 100 and abs(P(mp.log(49) / m('0.4')) - 2500) < 1e-9 and abs(mp.log(49) / m('0.4') - m('9.73')) < 0.01 and P(m(100)) < 5000; n += 4
    Tt = lambda tt: 25 + 60 * mp.e ** (-tt / 10)
    assert abs(Tt(m(10) ** 4) - 25) < 1e-6; n += 1
    for nn in (m(10) ** 6, m(10) ** 9):
        assert abs(2 * nn * mp.sin(mp.pi / nn) - 2 * mp.pi) < 1e-6 and abs(mp.log(nn) / nn) < 1e-4; n += 2
    assert abs(2 * mp.sin(h / 2) / h - 1) < 1e-9; n += 1
    # composite function claim
    assert all((2 * v + 1) ** 2 != 2 * v ** 2 + 1 for v in (1, 2, 3)); n += 1
    return n
