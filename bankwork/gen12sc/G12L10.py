# -*- coding: utf-8 -*-
"""
KhmerMath Question Bank: Grade 12 Science (SC)
Chapter 4: សិក្សាអថេរភាពនិងសង់ក្រាប
Lesson 2: អនុគមន៍អិចស្ប៉ូណង់ស្យែល
Reference textbook: Lesson/G12/SC/C4-L2.tex
Matrix: MCQ easy10/medium14/hard7/pisa5 + writing easy1/medium4/hard4/pisa5 = 50, Bloom on each.
Limits, extrema, zero counts, derivative values and application numbers are re-derived with mpmath (dense scans,
numerical derivatives) independently of the written solutions.
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.dirname(__file__))
from lib import *
import svgkit as K
import mpmath as mp
import G12L04 as P
from G12L04 import G
from G12L07 import D, argmax, argmin, close

LESSON = 'អនុគមន៍អិចស្ប៉ូណង់ស្យែល'
CHAPTER = 'ជំពូកទី 4 : សិក្សាអថេរភាពនិងសង់ក្រាប'
GRADE = '12SC'
TARGET = P.TARGET
S1 = 'ចំនួន e'
S2 = 'អនុគមន៍ e^x និងលក្ខណៈ'
S3 = 'ដេរីវេនៃអនុគមន៍អិចស្ប៉ូណង់ស្យែល'
S4 = 'សិក្សាអថេរភាពនិងសង់ក្រាប'
S5 = 'អនុវត្តន៍ : កំណើននិងការប្រាក់'
TOPIC_MAP = {'s1': S1, 's2': S2, 's3': S3, 's4': S4, 's5': S5,
             'p_bact': S5, 'p_comp': S5, 'p_dep': S5, 'p_drug': S4, 'p_money': S5, 'p_pop': S5}
CNT = [0]
mp.mp.dps = 40
BIG = mp.mpf(10) ** 12
E = mp.e


def chk(fn):
    r = fn()
    rs = list(r) if isinstance(r, tuple) else [r]
    assert all(rs), ('numeric check failed', rs)
    CNT[0] += len(rs)


def with_img(q, svg):
    q['img'] = svg
    return q


def fig_pos(f, xmax, kx, ky, xt, yt, xl, yl, dots=(), W=310, H=230, hl=()):
    return G(W, H, [(lambda t: f(t / kx) * ky, 0, xmax * kx, K.BLUE)], xt=[(kx * v, str(v)) for v in xt], yt=[(ky * v, str(v)) for v in yt],
             dots=[(kx * a, ky * b, '', 0, 0, K.RED) for a, b in dots], hl=[(ky * v, K.AMBER, True) for v in hl], xlabel=xl, ylabel=yl, pad=44)


def fig_bact():
    return fig_pos(lambda t: mp.e ** (1.386 * t), 5, 50.0, 0.2, (1, 2, 3, 4, 5), (200, 600, 1000), 't', 'N', dots=[(5, 1022)])


def fig_dep():
    return fig_pos(lambda t: 100000 * mp.e ** (-0.1 * t), 20, 12.0, 0.0018, (5, 10, 15, 20), (20000, 60000, 100000), 't', 'V', dots=[(5, 60653)])


def fig_drug():
    return fig_pos(lambda t: 10 * t * mp.e ** (-t / 2), 12, 20.0, 18.0, (2, 4, 6, 8, 10, 12), (2, 4, 6, 8), 't', 'C', dots=[(2, 20 / float(E))])


def fig_money():
    return fig_pos(lambda t: 100 * mp.e ** (0.12 * t), 9, 28.0, 0.7, (3, 6, 9), (100, 200, 294), 't', 'A', dots=[(9, 100 * float(E) ** 1.08)])


def cands():
    C = []
    # ============================================================ MCQ EASY (10)
    chk(lambda: close((1 + mp.mpf(1) / 10 ** 9) ** (10 ** 9), E, 1e-8))
    C.append(mcq('easy', 's1', 'ចំនួន ' + M('e=\\displaystyle\\lim_{n\\to+\\infty}\\left(1+\\dfrac1n\\right)^n') + ' មានតម្លៃប្រហែលស្មើ ៖', M('2{,}718'), [M('3{,}142'), M('1{,}618'), M('2{,}000')], 'តារាងតម្លៃ ' + M('\\left(1+\\dfrac1n\\right)^n') + ' ខិតទៅរក ' + M('2{,}71828\\ldots') + '។', 'Remember'))
    chk(lambda: close(E ** (2 + 3), E ** 2 * E ** 3, 1e-12))
    C.append(mcq('easy', 's2', 'ចំពោះគ្រប់ចំនួនពិត ' + M('m,n') + ' ' + M('e^{m+n}') + ' ស្មើ ៖', M('e^m\\cdot e^n'), [M('e^m+e^n'), M('e^{mn}'), M('\\dfrac{e^m}{e^n}')], 'លក្ខណៈ ' + M('e^{m+n}=e^m\\cdot e^n') + '។', 'Remember'))
    f = lambda t: E ** (4 * t - 1) / E ** (t + 3)
    chk(lambda: close(f(mp.mpf('0.7')), E ** (3 * mp.mpf('0.7') - 4), 1e-12))
    C.append(mcq('easy', 's2', 'សម្រួល ' + M('\\dfrac{e^{4x-1}}{e^{x+3}}') + ' ។', M('e^{3x-4}'), [M('e^{3x+2}'), M('e^{5x+2}'), M('e^{4x-4}')], M('e^{(4x-1)-(x+3)}=e^{3x-4}') + '។', 'Apply'))
    chk(lambda: close(D(lambda t: E ** (3 * t), 0.4), 3 * E ** (1.2), 1e-8))
    C.append(mcq('easy', 's3', 'ដេរីវេនៃ ' + M('y=e^{3x}') + ' គឺ ៖', M('3e^{3x}'), [M('e^{3x}'), M('3xe^{3x-1}'), M('\\dfrac{e^{3x}}3')], M('(e^{u})\'=u\'e^{u}') + ' ដែល ' + M('u=3x') + '។', 'Apply'))
    chk(lambda: close(D(lambda t: E ** (t * t), 0.7), 1.4 * E ** 0.49, 1e-8))
    C.append(mcq('easy', 's3', 'ដេរីវេនៃ ' + M('y=e^{x^2}') + ' គឺ ៖', M('2xe^{x^2}'), [M('e^{x^2}'), M('x^2e^{x^2-1}'), M('2e^{x^2}')], M('(e^{x^2})\'=(x^2)\'e^{x^2}=2xe^{x^2}') + '។', 'Apply'))
    chk(lambda: close(D(lambda t: t * E ** t, 0.5), 1.5 * E ** 0.5, 1e-8))
    C.append(mcq('easy', 's3', 'ដេរីវេនៃ ' + M('y=xe^x') + ' គឺ ៖', M('(1+x)e^x'), [M('xe^x'), M('e^x'), M('(1-x)e^x')], M('y\'=1\\cdot e^x+x\\cdot e^x=(1+x)e^x') + '។', 'Apply'))
    chk(lambda: (E ** (2 * BIG) > 1e100, E ** (-BIG) < 1e-100))
    C.append(mcq('easy', 's2', M('\\displaystyle\\lim_{x\\to+\\infty}e^{2x}') + ' ស្មើប៉ុន្មាន ?', M('+\\infty'), [M('0'), M('1'), M('2')], M('2x\\to+\\infty') + ' ដូច្នេះ ' + M('e^{2x}\\to+\\infty') + '។', 'Apply'))
    C.append(mcq('easy', 's2', 'ក្រាបនៃ ' + M('y=e^x') + ' មានអាស៊ីមតូតដេកជាបន្ទាត់ណា ?', M('y=0') + ' (កាលណា ' + M('x\\to-\\infty') + ')', [M('y=1'), M('x=0'), M('y=e')], M('\\displaystyle\\lim_{x\\to-\\infty}e^x=0') + '។', 'Understand'))
    C.append(mcq('easy', 's2', 'ក្រាបនៃ ' + M('y=e^x') + ' កាត់អ័ក្ស ' + M('Oy') + ' ត្រង់ចំណុចណា ?', M('(0,1)'), [M('(0,0)'), M('(0,e)'), M('(1,0)')], M('e^0=1') + '។', 'Remember'))
    chk(lambda: close(D(lambda t: E ** (-t), 0.9), -E ** (-0.9), 1e-8))
    C.append(mcq('easy', 's3', 'ដេរីវេនៃ ' + M('y=e^{-x}') + ' គឺ ៖', M('-e^{-x}'), [M('e^{-x}'), M('-e^{x}'), M('xe^{-x}')], M('u=-x') + ' ដូច្នេះ ' + M('y\'=(-1)e^{-x}') + '។', 'Apply'))

    # ============================================================ MCQ MEDIUM (14)
    f = lambda t: E ** (t * t - 3 * t + 1)
    chk(lambda: close(D(f, 1), -1 / E, 1e-8))
    C.append(mcq('medium', 's3', 'គេមាន ' + M('f(x)=e^{x^2-3x+1}') + ' ។ ' + M('f\'(1)') + ' ស្មើប៉ុន្មាន ?', M('-\\dfrac1e'), [M('\\dfrac1e'), M('-e'), M('0')], M('f\'(x)=(2x-3)e^{x^2-3x+1}') + ' ; ' + M('f\'(1)=(-1)e^{-1}') + '។', 'Apply'))
    f = lambda t: t * t * E ** (-2 * t)
    chk(lambda: close(D(f, 0.6), (1.2 - 0.72) * E ** (-1.2), 1e-8))
    C.append(mcq('medium', 's3', 'ដេរីវេនៃ ' + M('y=x^2e^{-2x}') + ' គឺ ៖', M('(2x-2x^2)e^{-2x}'), [M('(2x+2x^2)e^{-2x}'), M('2xe^{-2x}'), M('(2x-x^2)e^{-2x}')], M('y\'=2xe^{-2x}+x^2(-2)e^{-2x}=(2x-2x^2)e^{-2x}') + '។', 'Apply'))
    f = lambda t: mp.sqrt(t) / E ** t
    chk(lambda: close(D(f, 2), (1 - 4) / (2 * E ** 2 * mp.sqrt(2)), 1e-8))
    C.append(mcq('medium', 's3', 'ដេរីវេនៃ ' + M('y=\\dfrac{\\sqrt x}{e^x}') + ' គឺ ៖', M('\\dfrac{1-2x}{2e^x\\sqrt x}'), [M('\\dfrac{1+2x}{2e^x\\sqrt x}'), M('\\dfrac{1}{2e^x\\sqrt x}'), M('\\dfrac{2x-1}{2e^x\\sqrt x}')], M('y=\\sqrt x\\,e^{-x}') + ' ; ' + M('y\'=\\dfrac{e^{-x}}{2\\sqrt x}-\\sqrt xe^{-x}=\\dfrac{1-2x}{2e^x\\sqrt x}') + '។', 'Apply'))
    chk(lambda: (close(4 - 2 * E ** (-BIG), 4, 1e-9), D(lambda t: 4 - 2 * E ** (-t), 3) > 0))
    C.append(mcq('medium', 's4', 'ក្រាបនៃ ' + M('y=4-2e^{-x}') + ' មានអាស៊ីមតូតដេកជាបន្ទាត់ ៖', M('y=4'), [M('y=2'), M('y=0'), M('y=-2')], M('\\displaystyle\\lim_{x\\to+\\infty}e^{-x}=0') + ' ដូច្នេះ ' + M('y\\to4') + '។', 'Apply'))
    f = lambda t: t - E ** t
    r, v = argmax(f, -5, 5)
    chk(lambda: (close(r, 0, 1e-5), close(v, -1, 1e-8)))
    C.append(mcq('medium', 's4', 'អនុគមន៍ ' + M('f(x)=x-e^x') + ' មានតម្លៃអតិបរមាធៀបស្មើ ៖', M('-1') + ' ត្រង់ ' + M('x=0'), [M('1') + ' ត្រង់ ' + M('x=0'), M('-1') + ' ត្រង់ ' + M('x=1'), M('0') + ' ត្រង់ ' + M('x=0')], M('f\'=1-e^x=0') + ' ឱ្យ ' + M('x=0') + ' ; ' + M('f(0)=-1') + '។', 'Apply'))
    f = lambda t: t * E ** t
    r, v = argmin(f, -5, 5)
    chk(lambda: (close(r, -1, 1e-5), close(v, -1 / E, 1e-8)))
    C.append(mcq('medium', 's4', 'អនុគមន៍ ' + M('y=xe^x') + ' មានតម្លៃអប្បបរមាស្មើ ៖', M('-\\dfrac1e') + ' ត្រង់ ' + M('x=-1'), [M('-\\dfrac1e') + ' ត្រង់ ' + M('x=1'), M('-e') + ' ត្រង់ ' + M('x=-1'), M('0') + ' ត្រង់ ' + M('x=0')], M('y\'=(1+x)e^x=0') + ' ឱ្យ ' + M('x=-1') + ' ; ' + M('y(-1)=-e^{-1}') + '។', 'Apply'))
    d2x = lambda t: mp.diff(lambda s: s * E ** s, t, 2)
    chk(lambda: (close(d2x(-2), 0, 1e-12), d2x(-3) < 0, d2x(-1) > 0))
    C.append(mcq('medium', 's4', 'ចំណុចរបត់នៃក្រាប ' + M('y=xe^x') + ' មានអាប់ស៊ីសស្មើ ៖', M('-2'), [M('-1'), M('0'), M('2')], M('y\'\'=(x+2)e^x') + ' ប្ដូរសញ្ញាត្រង់ ' + M('x=-2') + '។', 'Apply'))
    chk(lambda: close(BIG / E ** BIG, 0, 1e-9))
    C.append(mcq('medium', 's4', M('\\displaystyle\\lim_{x\\to+\\infty}\\dfrac{x}{e^x}') + ' ស្មើប៉ុន្មាន ?', M('0'), [M('1'), M('+\\infty'), M('e')], 'អិចស្ប៉ូណង់ស្យែលធំលឿនជាង ' + M('x') + ' ដូច្នេះលីមីតស្មើ ' + M('0') + '។', 'Understand'))
    chk(lambda: close((1 + 3 / BIG) ** BIG, E ** 3, 1e-8))
    C.append(mcq('medium', 's1', M('\\displaystyle\\lim_{x\\to+\\infty}\\left(1+\\dfrac3x\\right)^x') + ' ស្មើប៉ុន្មាន ?', M('e^3'), [M('3e'), M('e'), M('3')], 'តាង ' + M('x=3m') + ' ៖ ' + M('\\left[\\left(1+\\dfrac1m\\right)^m\\right]^3\\to e^3') + '។', 'Apply'))
    chk(lambda: close(((E ** mp.mpf('1e-12')) - E ** (-mp.mpf('1e-12'))) / mp.mpf('1e-12'), 2, 1e-9))
    C.append(mcq('medium', 's3', M('\\displaystyle\\lim_{x\\to0}\\dfrac{e^x-e^{-x}}{x}') + ' ស្មើប៉ុន្មាន ?', M('2'), [M('0'), M('1'), M('e')], M('\\dfrac{e^x-e^{-x}}x=\\dfrac{e^x-1}x+\\dfrac{1-e^{-x}}x\\to1+1=2') + '។', 'Apply'))
    chk(lambda: close(E ** (2 * 3), E ** (3 + 3), 1e-12))
    C.append(mcq('medium', 's2', 'ចម្លើយនៃសមីការ ' + M('e^{2x}=e^{x+3}') + ' គឺ ៖', M('x=3'), [M('x=1'), M('x=\\dfrac32'), M('x=-3')], M('e^{2x}=e^{x+3}') + ' សមមូល ' + M('2x=x+3') + '។', 'Apply'))
    chk(lambda: all(close(E ** (2 * s) - 3 * E ** s + 2, 0, 1e-12) for s in (mp.mpf(0), mp.log(2))))
    C.append(mcq('medium', 's2', 'សំណុំចម្លើយនៃសមីការ ' + M('e^{2x}-3e^x+2=0') + ' គឺ ៖', M('\\{0,\\ \\ln2\\}'), [M('\\{1,\\ 2\\}'), M('\\{0,\\ 2\\}'), M('\\{1,\\ \\ln2\\}')], 'តាង ' + M('t=e^x>0') + ' ៖ ' + M('t^2-3t+2=0') + ' ឱ្យ ' + M('t=1,2') + ' ដូច្នេះ ' + M('x=0,\\ \\ln2') + '។', 'Apply'))
    f = lambda t: t + E ** t
    chk(lambda: (close(f(-BIG) - (-BIG), 0, 1e-9), D(f, 0.3) > 0))
    C.append(mcq('medium', 's4', 'ក្រាបនៃ ' + M('y=x+e^x') + ' មានអាស៊ីមតូតទ្រេតជាបន្ទាត់ ៖', M('y=x') + ' (កាលណា ' + M('x\\to-\\infty') + ')', [M('y=x+1') + ' (កាលណា ' + M('x\\to-\\infty') + ')', M('y=e^x'), M('y=0')], M('y-x=e^x\\to0') + ' កាលណា ' + M('x\\to-\\infty') + '។', 'Apply'))
    f = lambda t: 3 / (1 + 2 * E ** (-5 * t))
    chk(lambda: (close(f(BIG), 3, 1e-9), close(f(-BIG), 0, 1e-9)))
    C.append(mcq('medium', 's4', 'ក្រាបនៃ ' + M('f(x)=\\dfrac{3}{1+2e^{-5x}}') + ' មានអាស៊ីមតូតដេកជាបន្ទាត់ ៖', M('y=0') + ' និង ' + M('y=3'), [M('y=3') + ' តែមួយ', M('y=0') + ' តែមួយ', M('y=1') + ' និង ' + M('y=3')], M('x\\to-\\infty') + ' ឱ្យ ' + M('f\\to0') + ' ; ' + M('x\\to+\\infty') + ' ឱ្យ ' + M('f\\to3') + '។', 'Analyze'))

    # ============================================================ MCQ HARD (7)
    f = lambda t: t * t * E ** (-t)
    r, v = argmax(f, 0.5, 6)
    chk(lambda: (close(r, 2, 1e-5), close(v, 4 * E ** (-2), 1e-8)))
    C.append(mcq('hard', 's4', 'អនុគមន៍ ' + M('y=x^2e^{-x}') + ' មានតម្លៃអតិបរមាធៀបស្មើ ៖', M('4e^{-2}'), [M('e^{-1}'), M('2e^{-2}'), M('4e^{-1}')], M('y\'=x(2-x)e^{-x}=0') + ' ឱ្យ ' + M('x=0,2') + ' ; ' + M('y(2)=4e^{-2}') + ' ជាអតិបរមា ហើយ ' + M('y(0)=0') + ' ជាអប្បបរមា។', 'Analyze'))
    pts = [2 - mp.sqrt(2), 2 + mp.sqrt(2)]
    d2 = lambda t: mp.diff(f, t, 2)
    chk(lambda: (all(abs(d2(p)) < 1e-12 for p in pts), d2(1) < 0, d2(0.1) > 0, d2(4) > 0))
    C.append(mcq('hard', 's4', 'ក្រាបនៃ ' + M('y=x^2e^{-x}') + ' មានចំណុចរបត់ប៉ុន្មាន ?', M('2') + ' (' + M('x=2\\pm\\sqrt2') + ')', [M('0'), M('1'), M('3')], M('y\'\'=(x^2-4x+2)e^{-x}') + ' ; ' + M('\\Delta=8>0') + ' ឫស ' + M('x=2\\pm\\sqrt2') + ' ហើយ ' + M('y\'\'') + ' ប្ដូរសញ្ញាត្រង់ទាំងពីរ។', 'Analyze'))
    g = lambda t: E ** t - t * t
    xs = [mp.mpf(i) / 100 for i in range(-1000, 1001)]
    chg = sum(1 for a, b in zip(xs[:-1], xs[1:]) if (g(a) > 0) != (g(b) > 0))
    chk(lambda: (chg == 1, close(mp.findroot(g, -0.7), -0.7034674, 1e-6), all(D(g, s) > 0 for s in xs[::20])))
    C.append(mcq('hard', 's4', 'សមីការ ' + M('e^x=x^2') + ' មានចម្លើយពិតប៉ុន្មាន ?', M('1'), [M('0'), M('2'), M('3')], M('g(x)=e^x-x^2') + ' ; ' + M('g\'=e^x-2x>0') + ' (អប្បបរមា ' + M('2-2\\ln2>0') + ') ដូច្នេះ ' + M('g') + ' កើនលើ ' + M('\\mathbb{R}') + ' ពី ' + M('-\\infty') + ' ដល់ ' + M('+\\infty') + ' ដូច្នេះមានឫសតែមួយ ' + M('x\\approx-0{,}703') + '។', 'Analyze'))
    h = lambda t: t * E ** (-t)
    r, v = argmax(h, -3, 8)
    chk(lambda: (close(v, 1 / E, 1e-8), close(h(-BIG), -BIG * E ** BIG, 1e-9) is not None, h(-5) < 0, close(h(BIG), 0, 1e-9)))
    C.append(mcq('hard', 's4', 'សំណុំតម្លៃនៃអនុគមន៍ ' + M('y=xe^{-x}') + ' គឺ ៖', M('\\left(-\\infty,\\ \\dfrac1e\\right]'), [M('\\left(-\\infty,\\ 1\\right]'), M('\\left[0,\\ \\dfrac1e\\right]'), M('\\left[-\\dfrac1e,\\ +\\infty\\right)')], M('y\'=(1-x)e^{-x}') + ' ; អតិបរមា ' + M('y(1)=\\dfrac1e') + ' ; ' + M('y\\to-\\infty') + ' កាលណា ' + M('x\\to-\\infty') + '។', 'Analyze'))
    k = lambda t: E ** t / (t * t)
    r, v = argmin(k, 0.3, 8)
    chk(lambda: (close(r, 2, 1e-4), close(v, E ** 2 / 4, 1e-7)))
    C.append(mcq('hard', 's4', 'តម្លៃអប្បបរមានៃ ' + M('g(x)=\\dfrac{e^x}{x^2}') + ' ចំពោះ ' + M('x>0') + ' គឺ ៖', M('\\dfrac{e^2}4'), [M('e'), M('\\dfrac{e}{4}'), M('\\dfrac{e^2}{2}')], M('g\'=\\dfrac{(x-2)e^x}{x^3}') + ' ; ប្ដូរ ' + M('-\\to+') + ' ត្រង់ ' + M('x=2') + ' ដូច្នេះ ' + M('g(2)=\\dfrac{e^2}4') + '។', 'Analyze'))
    q = lambda t: 1 / (2 - E ** (-t))
    chk(lambda: (close(q(-BIG), 0, 1e-9), close(q(BIG), mp.mpf(1) / 2, 1e-9), abs(q(-mp.log(2) + mp.mpf('1e-9'))) > 1e8, abs(q(-mp.log(2) - mp.mpf('1e-9'))) > 1e8))
    C.append(mcq('hard', 's4', 'អនុគមន៍ ' + M('f(x)=\\dfrac{1}{2-e^{-x}}') + ' មានអាស៊ីមតូតឈរ ៖', M('x=-\\ln2'), [M('x=\\ln2'), M('x=0'), M('មិនមាន')], M('2-e^{-x}=0') + ' ឱ្យ ' + M('e^{-x}=2') + ' គឺ ' + M('x=-\\ln2') + ' ហើយ ' + M('|f|\\to\\infty') + ' នៅទីនោះ។', 'Analyze'))
    ph = lambda t: E ** t - t - 1
    chk(lambda: (all(ph(mp.mpf(s)) >= -1e-15 for s in xs[::5]), ph(mp.mpf(0)) == 0, all(ph(mp.mpf(s)) > 0 for s in xs[::5] if s != 0)))
    C.append(mcq('hard', 's4', 'ការអះអាងមួយណាត្រឹមត្រូវ ?', M('e^x\\ge x+1') + ' ចំពោះគ្រប់ ' + M('x') + ' ហើយសមភាពកើតមានតែពេល ' + M('x=0'), [M('e^x>x+1') + ' ចំពោះគ្រប់ ' + M('x'), M('e^x\\le x+1') + ' ចំពោះគ្រប់ ' + M('x'), M('e^x\\ge x+1') + ' តែចំពោះ ' + M('x\\ge0')],
                 'តាង ' + M('\\varphi=e^x-x-1') + ' ; ' + M('\\varphi\'=e^x-1') + ' ប្ដូរ ' + M('-\\to+') + ' ត្រង់ ' + M('x=0') + ' ដូច្នេះអប្បបរមា ' + M('\\varphi(0)=0') + ' ដូច្នេះ ' + M('\\varphi\\ge0') + ' ហើយ ' + M('=0') + ' តែត្រង់ ' + M('x=0') + '។', 'Evaluate'))

    # ============================================================ MCQ PISA (5)
    chk(lambda: close(E ** (1.386 * 5), 1022.49, 1e-2))
    C.append(with_img(mcq('pisa', 'p_bact', 'បាក់តេរីបង្កើនខ្លួនតាមរូបមន្ត ' + M('N=N_0e^{1{,}386t}') + ' (' + M('t') + ' ជាម៉ោង) ។ ចាប់ផ្ដើមពី ' + M('N_0=1') + ' តើមានបាក់តេរីប្រហែលប៉ុន្មាននៅពេល ' + M('t=5') + ' ម៉ោង ដូចក្នុងរូប ?', M('1022'), [M('7'), M('139'), M('6{,}93')], M('N=e^{1{,}386\\times5}=e^{6{,}93}\\approx1022') + '។', 'Apply'), fig_bact()))
    chk(lambda: close(100 * E ** (0.08 * 2), 117.351, 1e-4))
    C.append(with_img(mcq('pisa', 'p_comp', 'ដាក់ប្រាក់ ' + M('100') + ' ដុល្លារ ការប្រាក់សមាសបន្តបន្ទាប់ ' + M('A=pe^{rt}') + ' អត្រា ' + M('r=12\\%') + ' ក្នុងមួយឆ្នាំ រយៈពេល ' + M('t=9') + ' ឆ្នាំ ដូចក្នុងរូប ។ តើប្រាក់សរុបប្រហែលប៉ុន្មាន ?', M('294{,}47') + ' ដុល្លារ', [M('277{,}31') + ' ដុល្លារ', M('208{,}00') + ' ដុល្លារ', M('120{,}00') + ' ដុល្លារ'], M('A=100e^{0{,}12\\times9}=100e^{1{,}08}\\approx294{,}47') + ' (ការទូទាត់ ' + M('1') + ' ដងក្នុងមួយឆ្នាំ ឱ្យ ' + M('277{,}31') + ')។', 'Apply'), fig_money()))
    chk(lambda: close(100000 * E ** (-0.5), 60653.07, 1e-2))
    C.append(with_img(mcq('pisa', 'p_dep', 'តម្លៃម៉ាស៊ីនមួយ ' + M('V(t)=100\\,000\\,e^{-0{,}1t}') + ' ដុល្លារ (' + M('t') + ' ជាឆ្នាំ) ដូចក្នុងរូប ។ តើតម្លៃបន្ទាប់ពី ' + M('5') + ' ឆ្នាំប្រហែលប៉ុន្មាន ?', M('60\\,653') + ' ដុល្លារ', [M('50\\,000') + ' ដុល្លារ', M('36\\,788') + ' ដុល្លារ', M('90\\,000') + ' ដុល្លារ'], M('V(5)=100000e^{-0{,}5}\\approx60\\,653') + '។', 'Apply'), fig_dep()))
    f = lambda t: 10 * t * E ** (-t / 2)
    r, v = argmax(f, 0, 30)
    chk(lambda: (close(r, 2, 1e-5), close(v, 20 / E, 1e-8), close(f(BIG), 0, 1e-9)))
    C.append(with_img(mcq('pisa', 'p_drug', 'កំហាប់ថ្នាំក្នុងឈាម ' + M('C(t)=10te^{-t/2}') + ' (mg/L) ក្រោយចាក់ ' + M('t') + ' ម៉ោង ដូចក្នុងរូប ។ តើពេលណាកំហាប់ធំបំផុត និងស្មើប៉ុន្មាន ?', M('t=2') + ' ម៉ោង ; ' + M('\\dfrac{20}{e}\\approx7{,}36') + ' mg/L', [M('t=1') + ' ម៉ោង ; ' + M('\\dfrac{10}{\\sqrt e}\\approx6{,}07') + ' mg/L', M('t=4') + ' ម៉ោង ; ' + M('\\dfrac{40}{e^2}\\approx5{,}41') + ' mg/L', M('t=2') + ' ម៉ោង ; ' + M('20') + ' mg/L'],
                          M('C\'=10\\left(1-\\dfrac t2\\right)e^{-t/2}=0') + ' ឱ្យ ' + M('t=2') + ' ; ' + M('C(2)=20e^{-1}\\approx7{,}36') + '។', 'Analyze'), fig_drug()))
    chk(lambda: close(mp.log(3) / 0.07, 15.694, 1e-3))
    C.append(mcq('pisa', 'p_money', 'ប្រាក់ដាក់ក្នុងធនាគារដោយការប្រាក់សមាសបន្តបន្ទាប់ ' + M('7\\%') + ' ក្នុងមួយឆ្នាំ ។ តើប្រហែលប៉ុន្មានឆ្នាំទើបប្រាក់កើនដល់បីដងនៃប្រាក់ដើម ?', M('15{,}7') + ' ឆ្នាំ', [M('14{,}3') + ' ឆ្នាំ', M('42{,}9') + ' ឆ្នាំ', M('10{,}0') + ' ឆ្នាំ'], M('pe^{0{,}07t}=3p') + ' ឱ្យ ' + M('t=\\dfrac{\\ln3}{0{,}07}\\approx15{,}7') + '។', 'Apply'))
    return C + cands_writing()


def cands_writing():
    C = []
    f = lambda t: t * E ** (-t)
    chk(lambda: (close(D(f, 0.5), 0.5 * E ** (-0.5), 1e-8), close(D(f, 2), -E ** (-2), 1e-8)))
    # ============================================================ WRITING EASY (1)
    C.append(wr('easy', 's3', 'គណនាដេរីវេនៃ ' + M('y=xe^{-x}') + ' រួចរកតម្លៃ ' + M('x') + ' ដែល ' + M('y\'=0') + '។',
                [('ប្រើរូបមន្ត ' + M('(uv)\'=u\'v+uv\'') + ' ជាមួយ ' + M('u=x') + ', ' + M('v=e^{-x}'), 1),
                 (M('u\'=1') + ' ; ' + M('v\'=(-x)\'e^{-x}=-e^{-x}'), 1),
                 (M('y\'=e^{-x}+x(-e^{-x})=(1-x)e^{-x}'), 1),
                 (M('y\'=0') + ' សមមូល ' + M('(1-x)e^{-x}=0'), 1),
                 ('ដោយ ' + M('e^{-x}>0') + ' ដូច្នេះ ' + M('1-x=0') + ' គឺ ' + M('x=1') + '។', 1)], bloom='Apply'))

    # ============================================================ WRITING MEDIUM (4)
    g = lambda t: t + E ** (-t)
    chk(lambda: (close(D(g, 0), 0, 1e-8), close(g(0), 1), D(g, -1) < 0 and D(g, 1) > 0, close(g(BIG) - BIG, 0, 1e-9)))
    C.append(wr('medium', 's4', 'សិក្សាអថេរភាពនៃអនុគមន៍ ' + M('f(x)=x+e^{-x}') + ' ហើយរកអាស៊ីមតូតទ្រេត ។',
                [('ដែន ' + M('D=\\mathbb{R}') + ' ; ' + M('f\'(x)=1-e^{-x}'), 1),
                 (M('f\'=0') + ' ឱ្យ ' + M('e^{-x}=1') + ' គឺ ' + M('x=0') + ' ; ' + M('f\'<0') + ' ពេល ' + M('x<0') + ' ; ' + M('f\'>0') + ' ពេល ' + M('x>0'), 1),
                 ('ដូច្នេះ ' + M('f') + ' ចុះលើ ' + M('(-\\infty,0)') + ' កើនលើ ' + M('(0,+\\infty)') + ' ; អប្បបរមា ' + M('f(0)=0+1=1'), 1),
                 ('លីមីត ' + M('\\displaystyle\\lim_{x\\to-\\infty}f=+\\infty') + ' (' + M('e^{-x}\\to+\\infty') + ') ; ' + M('\\displaystyle\\lim_{x\\to+\\infty}f=+\\infty'), 1),
                 (M('f(x)-x=e^{-x}\\to0') + ' កាលណា ' + M('x\\to+\\infty') + ' ដូច្នេះអាស៊ីមតូតទ្រេត ' + M('y=x') + '។', 1)], bloom='Apply'))
    chk(lambda: (close((BIG ** 2 + 1) / E ** BIG, 0, 1e-9), close(-BIG * E ** (-BIG), 0, 1e-9)))
    C.append(wr('medium', 's4', 'គណនាលីមីត ក. ' + M('\\displaystyle\\lim_{x\\to+\\infty}\\dfrac{x^2+1}{e^x}') + ' ខ. ' + M('\\displaystyle\\lim_{x\\to-\\infty}xe^x') + ' ។',
                [('ក. ' + M('\\dfrac{x^2+1}{e^x}=\\dfrac{x^2}{e^x}+\\dfrac1{e^x}'), 1),
                 ('អិចស្ប៉ូណង់ស្យែលធំលើសពហុធា ដូច្នេះ ' + M('\\dfrac{x^2}{e^x}\\to0') + ' ; ' + M('\\dfrac1{e^x}\\to0'), 1),
                 ('ដូច្នេះ ' + M('\\displaystyle\\lim_{x\\to+\\infty}\\dfrac{x^2+1}{e^x}=0'), 1),
                 ('ខ. តាង ' + M('t=-x\\to+\\infty') + ' ៖ ' + M('xe^x=-\\dfrac{t}{e^t}'), 1),
                 (M('\\dfrac t{e^t}\\to0') + ' ដូច្នេះ ' + M('\\displaystyle\\lim_{x\\to-\\infty}xe^x=0') + '។', 1)], bloom='Apply'))
    chk(lambda: (close(E ** (2 * mp.log(2)) - 3 * E ** mp.log(2) + 2, 0, 1e-12), all(E ** (2 * s) - 3 * E ** s + 2 < 0 for s in (mp.mpf('0.3'), mp.mpf('0.6'))), all(E ** (2 * s) - 3 * E ** s + 2 > 0 for s in (mp.mpf('-1'), mp.mpf('1')))))
    C.append(wr('medium', 's2', 'ដោះស្រាយសមីការ ' + M('e^{2x}-3e^x+2=0') + ' និងវិសមីការ ' + M('e^{2x}-3e^x+2<0') + '។',
                [('តាង ' + M('t=e^x') + ' ដែល ' + M('t>0') + ' ; សមីការក្លាយ ' + M('t^2-3t+2=0'), 1),
                 (M('(t-1)(t-2)=0') + ' ឱ្យ ' + M('t=1') + ' ឬ ' + M('t=2') + ' (ទាំងពីរវិជ្ជមាន)', 1),
                 ('ដូច្នេះ ' + M('e^x=1') + ' គឺ ' + M('x=0') + ' ឬ ' + M('e^x=2') + ' គឺ ' + M('x=\\ln2'), 1),
                 ('វិសមីការ ' + M('(t-1)(t-2)<0') + ' ឱ្យ ' + M('1<t<2'), 1),
                 ('ដូច្នេះ ' + M('1<e^x<2') + ' គឺ ' + M('0<x<\\ln2') + ' (ព្រោះ ' + M('e^x') + ' កើន)។', 1)], bloom='Apply'))
    f = lambda t: E ** (2 * t - 1)
    chk(lambda: (close(f(0.5), 1), close(D(f, 0.5), 2, 1e-8)))
    C.append(wr('medium', 's3', 'រកសមីការបន្ទាត់ប៉ះក្រាបនៃ ' + M('f(x)=e^{2x-1}') + ' ត្រង់ចំណុចដែល ' + M('x=\\dfrac12') + '។',
                [('ដេរីវេ ' + M('f\'(x)=2e^{2x-1}'), 1),
                 (M('f\\left(\\dfrac12\\right)=e^0=1'), 1),
                 (M('f\'\\left(\\dfrac12\\right)=2e^0=2'), 1),
                 ('បន្ទាត់ប៉ះ ' + M('y-1=2\\left(x-\\dfrac12\\right)'), 1),
                 ('ដូច្នេះ ' + M('y=2x') + ' (កាត់គល់ ' + M('O') + ')។', 1)], bloom='Apply'))

    # ============================================================ WRITING HARD (4)
    ff = lambda t: t * t * E ** (-t)
    r, v = argmax(ff, 0.5, 6)
    chk(lambda: (close(r, 2, 1e-5), close(v, 4 * E ** -2, 1e-8), close(ff(0), 0), close(ff(-BIG), BIG ** 2 * E ** BIG, 1e-9) is not None, close(ff(BIG), 0, 1e-9)))
    C.append(wr('hard', 's4', 'សិក្សាអថេរភាព និងរកអាស៊ីមតូតនៃអនុគមន៍ ' + M('f(x)=x^2e^{-x}') + '។',
                [('ដែន ' + M('D=\\mathbb{R}') + ' ; ' + M('f\'(x)=2xe^{-x}-x^2e^{-x}=x(2-x)e^{-x}'), 1),
                 (M('f\'=0') + ' ឱ្យ ' + M('x=0') + ' ឬ ' + M('x=2') + ' ; ' + M('f\'<0') + ' លើ ' + M('(-\\infty,0)\\cup(2,+\\infty)') + ' ; ' + M('f\'>0') + ' លើ ' + M('(0,2)'), 1),
                 ('អប្បបរមាធៀប ' + M('f(0)=0') + ' ; អតិបរមាធៀប ' + M('f(2)=4e^{-2}\\approx0{,}54'), 1),
                 ('លីមីត ' + M('\\displaystyle\\lim_{x\\to-\\infty}f=+\\infty') + ' ; ' + M('\\displaystyle\\lim_{x\\to+\\infty}f=0') + ' (អិចស្ប៉ូណង់ស្យែលធំលើសពហុធា)', 1),
                 ('ដូច្នេះអាស៊ីមតូតដេក ' + M('y=0') + ' (កាលណា ' + M('x\\to+\\infty') + ') ; ' + M('f\'\'=(x^2-4x+2)e^{-x}') + ' ឱ្យចំណុចរបត់ ' + M('x=2\\pm\\sqrt2') + '។', 1)], bloom='Analyze'))
    ph = lambda t: E ** t - t - 1
    chk(lambda: (ph(mp.mpf(0)) == 0, all(ph(mp.mpf(s) / 10) > 0 for s in range(-50, 51) if s != 0)))
    C.append(wr('hard', 's4', 'ស្រាយបញ្ជាក់ថា ចំពោះគ្រប់ចំនួនពិត ' + M('x') + ' មាន ' + M('e^x\\ge x+1') + ' ហើយទាញថា ' + M('e^{-x}\\ge1-x') + '។',
                [('តាង ' + M('\\varphi(x)=e^x-x-1') + ' ; ' + M('\\varphi\'(x)=e^x-1'), 1),
                 (M('\\varphi\'<0') + ' ពេល ' + M('x<0') + ' ; ' + M('\\varphi\'>0') + ' ពេល ' + M('x>0') + ' ; ' + M('\\varphi\'(0)=0'), 1),
                 ('ដូច្នេះ ' + M('\\varphi') + ' មានអប្បបរមាត្រង់ ' + M('x=0') + ' ដែល ' + M('\\varphi(0)=1-0-1=0'), 1),
                 ('ដូច្នេះ ' + M('\\varphi(x)\\ge0') + ' គឺ ' + M('e^x\\ge x+1') + ' គ្រប់ ' + M('x'), 1),
                 ('ជំនួស ' + M('x') + ' ដោយ ' + M('-x') + ' ៖ ' + M('e^{-x}\\ge-x+1=1-x') + '។', 1)], bloom='Evaluate'))
    gm = lambda t: E ** t / t

    def nsol(m):
        xs = [mp.mpf(i) / 50 for i in range(-1500, 1501) if i != 0]
        n, prev = 0, None
        for t in xs:
            v = gm(t) - m * 1 if False else E ** t - m * t
            if prev is not None and prev[0] * t > 0 and (prev[1] > 0) != (v > 0):
                n += 1
            prev = (t, v)
        return n
    chk(lambda: (nsol(-1) == 1, nsol(1) == 0, nsol(2) == 0, nsol(3) == 2, nsol(5) == 2, close(gm(1), E)))
    C.append(wr('hard', 's4', 'ពិភាក្សាចំនួនឫសនៃសមីការ ' + M('e^x=mx') + ' តាមតម្លៃ ' + M('m') + ' ដោយសិក្សា ' + M('g(x)=\\dfrac{e^x}{x}') + ' ។',
                [('ដោយ ' + M('x=0') + ' មិនជាឫស (' + M('e^0=1\\ne0') + ') សមីការសមមូល ' + M('g(x)=\\dfrac{e^x}x=m') + ' ចំពោះ ' + M('x\\ne0'), 1),
                 (M('g\'(x)=\\dfrac{(x-1)e^x}{x^2}') + ' ; ចុះលើ ' + M('(-\\infty,0)') + ' និង ' + M('(0,1)') + ' ; កើនលើ ' + M('(1,+\\infty)') + ' ; អប្បបរមា ' + M('g(1)=e') + ' (ចំពោះ ' + M('x>0') + ')', 1),
                 ('លីមីត ៖ ' + M('x\\to-\\infty') + ' ឱ្យ ' + M('g\\to0^-') + ' ; ' + M('x\\to0^-') + ' ឱ្យ ' + M('-\\infty') + ' ; ' + M('x\\to0^+') + ' ឬ ' + M('+\\infty') + ' ឱ្យ ' + M('+\\infty'), 1),
                 ('លើ ' + M('(-\\infty,0)') + ' ' + M('g<0') + ' ចុះពី ' + M('0') + ' ដល់ ' + M('-\\infty') + ' ដូច្នេះ ' + M('m<0') + ' មានឫសមួយ ; លើ ' + M('(0,+\\infty)') + ' ' + M('g\\ge e') + ' ដូច្នេះ ' + M('0\\le m<e') + ' គ្មានឫស', 1),
                 (M('m=e') + ' មួយឫស (' + M('x=1') + ') ; ' + M('m>e') + ' ពីរឫស (មួយក្នុង ' + M('(0,1)') + ' មួយក្នុង ' + M('(1,+\\infty)') + ')។', 1)], bloom='Analyze'))
    fh = lambda t: (1 - t) * E ** (-t)
    chk(lambda: (close(fh(0), 1), close(D(fh, 2), 0, 1e-8), close(fh(2), -E ** -2, 1e-12), D(fh, 1) < 0 and D(fh, 3) > 0))
    C.append(wr('hard', 's3', 'រកចំនួន ' + M('a,b') + ' ដើម្បីឱ្យអនុគមន៍ ' + M('f(x)=(ax+b)e^{-x}') + ' កាត់អ័ក្ស ' + M('Oy') + ' ត្រង់ ' + M('(0,1)') + ' ហើយមានតម្លៃបរមាត្រង់ ' + M('x=2') + '។ រកតម្លៃបរមានោះ ហើយបញ្ជាក់ថាជាអប្បបរមា ។',
                [('ដេរីវេ ' + M('f\'(x)=ae^{-x}-(ax+b)e^{-x}=(a-b-ax)e^{-x}'), 1),
                 ('ត្រង់ ' + M('(0,1)') + ' ៖ ' + M('f(0)=b=1'), 1),
                 (M('f\'(2)=0') + ' ឱ្យ ' + M('a-b-2a=0') + ' គឺ ' + M('-a-b=0') + ' ដូច្នេះ ' + M('a=-b=-1'), 1),
                 ('ឡើងវិញ ' + M('f(x)=(1-x)e^{-x}') + ' ; ' + M('f\'(x)=(x-2)e^{-x}') + ' ប្ដូរ ' + M('-\\to+') + ' ត្រង់ ' + M('x=2'), 1),
                 ('ដូច្នេះអប្បបរមា ' + M('f(2)=(1-2)e^{-2}=-e^{-2}\\approx-0{,}135') + '។', 1)], bloom='Create'))

    # ============================================================ WRITING PISA (5)
    chk(lambda: (close(E ** (1.386 * 0.5), 2, 1e-3), close(E ** (1.386 * 5), 1022.49, 1e-2), close(mp.log(2) / 1.386, 0.5001, 1e-3)))
    C.append(with_img(wr('pisa', 'p_bact', 'បាក់តេរីបង្កើនខ្លួនតាម ' + M('N=e^{1{,}386t}') + ' (ចាប់ពី ' + M('N_0=1') + ', ' + M('t') + ' ម៉ោង) ដូចក្នុងរូប ។ ក. រកចំនួនបាក់តេរីពេល ' + M('t=5') + ' និង ' + M('t=12') + ' ។ ខ. រកពេលដែលចំនួនកើនទ្វេដង ។ គ. ពន្យល់ថាហេតុអ្វីម៉ូដែលនេះមិនអាចត្រឹមត្រូវជាយូរអង្វែង ។',
                         [('ក. ' + M('N(5)=e^{6{,}93}\\approx1022') + ' បាក់តេរី', 1),
                          (M('N(12)=e^{16{,}632}\\approx16\\,718\\,057'), 1),
                          ('ខ. ទ្វេដង ៖ ' + M('e^{1{,}386t}=2') + ' ដូច្នេះ ' + M('t=\\dfrac{\\ln2}{1{,}386}\\approx0{,}50') + ' ម៉ោង (៣០ នាទី)', 1),
                          ('ពិនិត្យ ៖ ១២ ម៉ោង = ២៤ ដងនៃការទ្វេ ' + M('2^{24}\\approx1{,}68\\times10^7') + ' ស្របនឹងចម្លើយ ក.', 1),
                          ('គ. កំណើនអិចស្ប៉ូណង់ស្យែលគ្មានកំណត់មិនអាចបន្តយូរ ព្រោះអាហារ និងទីតាំងមានកំណត់ ; ចំនួនបាក់តេរីនឹងឈប់កើនលឿន។', 1)], bloom='Apply'), fig_bact()))
    chk(lambda: (close(100 * 1.12 ** 9, 277.31, 1e-2), close(100 * 1.03 ** 36, 289.83, 1e-2), close(100 * E ** 1.08, 294.47, 1e-2), 100 * 1.12 ** 9 < 100 * 1.03 ** 36 < 100 * E ** 1.08))
    C.append(with_img(wr('pisa', 'p_comp', 'ដាក់ប្រាក់ ' + M('100') + ' ដុល្លារ ការប្រាក់សមាស ' + M('12\\%') + ' ក្នុងមួយឆ្នាំ រយៈពេល ' + M('9') + ' ឆ្នាំ ។ ក. គណនាប្រាក់សរុបបើទូទាត់ឆ្នាំម្ដង ត្រីមាសម្ដង និងបន្តបន្ទាប់ ។ ខ. តើការទូទាត់ញឹកជាង ផ្ដល់ប្រាក់ច្រើនជាងដោយគ្មានដែនកំណត់ឬទេ ? ពន្យល់ ។',
                         [('ក. ឆ្នាំម្ដង ៖ ' + M('A=100(1+0{,}12)^9\\approx277{,}31'), 1),
                          ('ត្រីមាសម្ដង ៖ ' + M('A=100\\left(1+\\dfrac{0{,}12}4\\right)^{36}=100(1{,}03)^{36}\\approx289{,}83'), 1),
                          ('បន្តបន្ទាប់ ៖ ' + M('A=100e^{0{,}12\\times9}=100e^{1{,}08}\\approx294{,}47'), 1),
                          ('ខ. ' + M('277{,}31<289{,}83<294{,}47') + ' ដូច្នេះទូទាត់ញឹកជាងឱ្យច្រើនជាង', 1),
                          ('ប៉ុន្តែកើនយឺតៗទៅរកលីមីត ' + M('pe^{rt}=294{,}47') + ' (' + M('\\left(1+\\dfrac rn\\right)^{nt}\\to e^{rt}') + ') ដូច្នេះមិនអាចកើនដោយគ្មានដែនកំណត់ទេ។', 1)], bloom='Analyze'), fig_money()))
    chk(lambda: (close(100000 * E ** (-0.1 * 5), 60653.07, 1e-2), close(10 * mp.log(2), 6.9315, 1e-4), close(100000 * E ** (-0.1 * 10 * mp.log(2)), 50000, 1e-9), close(-1, -1)))
    C.append(with_img(wr('pisa', 'p_dep', 'តម្លៃម៉ាស៊ីនមួយ ' + M('V(t)=100\\,000\\,e^{-0{,}1t}') + ' ដុល្លារ (' + M('t') + ' ជាឆ្នាំ) ដូចក្នុងរូប ។ ក. រកតម្លៃដំបូង និងតម្លៃបន្ទាប់ពី ' + M('5') + ' ឆ្នាំ ។ ខ. រកពេលដែលតម្លៃនៅសល់ពាក់កណ្ដាល ។ គ. រក ' + M('V\'(t)') + ' ហើយបកស្រាយ ។',
                         [('ក. ' + M('V(0)=100\\,000') + ' ដុល្លារ ; ' + M('V(5)=100000e^{-0{,}5}\\approx60\\,653') + ' ដុល្លារ', 1),
                          ('ខ. ' + M('100000e^{-0{,}1t}=50000') + ' ឱ្យ ' + M('e^{-0{,}1t}=\\dfrac12'), 1),
                          ('ដូច្នេះ ' + M('-0{,}1t=-\\ln2') + ' គឺ ' + M('t=10\\ln2\\approx6{,}93') + ' ឆ្នាំ', 1),
                          ('គ. ' + M('V\'(t)=-0{,}1V(t)=-10\\,000e^{-0{,}1t}<0') + ' ដូច្នេះតម្លៃចុះជានិច្ច', 1),
                          ('អត្រាចុះ ស្មើ ' + M('10\\%') + ' នៃតម្លៃបច្ចុប្បន្ន (ចុះលឿនពីដំបូង បន្ទាប់មកយឺតទៅៗ) ; ' + M('V\\to0') + ' កាលណា ' + M('t\\to\\infty') + '។', 1)], bloom='Apply'), fig_dep()))
    f = lambda t: 10 * t * E ** (-t / 2)
    chk(lambda: (close(f(2), 20 / E, 1e-9), close(f(4), 40 / E ** 2, 1e-9), close(f(1), 10 / mp.sqrt(E), 1e-9), close(f(BIG), 0, 1e-9), all(D(f, s) < 0 for s in (2.5, 3, 5, 9))))
    C.append(with_img(wr('pisa', 'p_drug', 'កំហាប់ថ្នាំក្នុងឈាម ' + M('C(t)=10te^{-t/2}') + ' (mg/L) ក្រោយចាក់ ' + M('t') + ' ម៉ោង ដូចក្នុងរូប ។ ក. រក ' + M('C\'(t)') + ' និងពេលដែលកំហាប់ធំបំផុត ។ ខ. គណនាកំហាប់អតិបរមា និងប្រៀបធៀប ' + M('C(1)') + ', ' + M('C(4)') + ' ។ គ. រកអាស៊ីមតូតដេក ហើយបកស្រាយ ។',
                         [('ក. ' + M('C\'(t)=10e^{-t/2}+10t\\left(-\\dfrac12\\right)e^{-t/2}=10\\left(1-\\dfrac t2\\right)e^{-t/2}'), 1),
                          (M('C\'=0') + ' ឱ្យ ' + M('t=2') + ' ; ' + M('C\'>0') + ' ពេល ' + M('t<2') + ' ; ' + M('C\'<0') + ' ពេល ' + M('t>2') + ' ដូច្នេះអតិបរមាត្រង់ ' + M('t=2') + ' ម៉ោង', 1),
                          ('ខ. ' + M('C(2)=20e^{-1}\\approx7{,}36') + ' mg/L', 1),
                          (M('C(1)=10e^{-0{,}5}\\approx6{,}07') + ' ; ' + M('C(4)=40e^{-2}\\approx5{,}41') + ' ដូច្នេះ ' + M('C(1)>C(4)') + ' (ឡើងលឿន ចុះយឺត)', 1),
                          ('គ. ' + M('\\displaystyle\\lim_{t\\to+\\infty}10te^{-t/2}=0') + ' ដូច្នេះអាស៊ីមតូតដេក ' + M('y=0') + ' ៖ ថ្នាំបាត់ពីឈាមជាបណ្ដើរៗ។', 1)], bloom='Analyze'), fig_drug()))
    chk(lambda: (close(30000 * mp.mpf(1.35) ** mp.mpf(3.8), 93840, 1), close(mp.log(1.35) / 10, 0.030010, 1e-3), close(mp.log(2) / (mp.log(1.35) / 10), 23.1, 1e-2)))
    C.append(wr('pisa', 'p_pop', 'ទីក្រុងមួយមានប្រជាជន ' + M('30\\,000') + ' នាក់ ឆ្នាំ ' + M('1970') + ' និង ' + M('40\\,500') + ' នាក់ ឆ្នាំ ' + M('1980') + ' ។ ប្រើ ' + M('p(t)=p_0e^{kt}') + ' (' + M('t') + ' គិតពី ' + M('1970') + ') ។ ក. រក ' + M('p_0') + ' និង ' + M('k') + ' ។ ខ. ប៉ាន់ស្មានប្រជាជនឆ្នាំ ' + M('2008') + ' ។ គ. រកពេលវេលាដែលប្រជាជនកើនទ្វេដង ។',
                [('ក. ' + M('p(0)=p_0=30\\,000'), 1),
                 (M('p(10)=30000e^{10k}=40500') + ' ដូច្នេះ ' + M('e^{10k}=1{,}35') + ' គឺ ' + M('k=\\dfrac{\\ln1{,}35}{10}\\approx0{,}0300'), 1),
                 ('ខ. ' + M('t=2008-1970=38') + ' ; ' + M('p(38)=30000\\cdot1{,}35^{3{,}8}\\approx93\\,840') + ' នាក់', 1),
                 ('គ. ទ្វេដង ៖ ' + M('e^{kt}=2') + ' ដូច្នេះ ' + M('t=\\dfrac{\\ln2}{k}=\\dfrac{10\\ln2}{\\ln1{,}35}\\approx23{,}1') + ' ឆ្នាំ', 1),
                 ('សន្និដ្ឋាន ៖ ប្រជាជនកើនប្រហែល ' + M('3\\%') + ' ក្នុងមួយឆ្នាំ ទ្វេដងរៀងរាល់ប្រមាណ ' + M('23') + ' ឆ្នាំ។', 1)], bloom='Evaluate'))
    return C


def verify():
    mp.mp.dps = 40
    CNT[0] = 0
    cands()
    return CNT[0]
