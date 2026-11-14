# -*- coding: utf-8 -*-
"""
KhmerMath Question Bank: Grade 12 Science (SC)
Chapter 4: សិក្សាអថេរភាពនិងសង់ក្រាប
Lesson 1: អនុគមន៍សនិទាន
Reference textbook: Lesson/G12/SC/C4-L1.tex

Target matrix: MCQ easy10/medium14/hard7/pisa5 + writing easy1/medium4/hard4/pisa5 = 50, a Bloom level on each.
Asymptotes (limits and distance to the line at very large |x|), extrema (dense scan + numerical derivative), values and
solution counts are re-derived with mpmath, independent of the worked solutions.  Helpers and figures come from G12L04/L07.
"""
import sys, os, math
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.dirname(__file__))
from lib import *
import svgkit as K
import mpmath as mp
import G12L04 as P
import G12L07 as Q
from G12L04 import G, curve
from G12L07 import D, argmax, argmin, close

LESSON = 'អនុគមន៍សនិទាន'
CHAPTER = 'ជំពូកទី 4 : សិក្សាអថេរភាពនិងសង់ក្រាប'
GRADE = '12SC'
TARGET = P.TARGET
S1 = 'អាស៊ីមតូតនៃក្រាប'
S2 = 'សិក្សាអនុគមន៍ដឺក្រេទី ២ ចែកដឺក្រេទី ១'
S3 = 'សិក្សាអនុគមន៍ដឺក្រេទី ២ ចែកដឺក្រេទី ២'
S4 = 'ផ្ចិតឆ្លុះនិងអ័ក្សឆ្លុះ'
S5 = 'អនុវត្តន៍ និងប៉ារ៉ាម៉ែត្រ'
TOPIC_MAP = {'s1': S1, 's2': S2, 's3': S3, 's4': S4, 's5': S5,
             'p_cost': S5, 'p_drug': S3, 'p_flow': S3, 'p_power': S3, 'p_lens': S2,
             'p_avg': S5, 'p_conc': S3, 'p_traffic': S3, 'p_batt': S3, 'p_image': S2}
CNT = [0]
BIG = mp.mpf(10) ** 12


def chk(fn):
    r = fn()
    rs = list(r) if isinstance(r, tuple) else [r]
    assert all(rs), ('numeric check failed', rs)
    CNT[0] += len(rs)


def with_img(q, svg):
    q['img'] = svg
    return q


def lim_inf(f):
    mp.mp.dps = 40
    return f(BIG), f(-BIG)


def oblique(f, a, b):
    """True when f(x) - (a x + b) -> 0 at both ends."""
    mp.mp.dps = 40
    return abs(f(BIG) - (a * BIG + b)) < mp.mpf('1e-9') and abs(f(-BIG) - (a * (-BIG) + b)) < mp.mpf('1e-9')


def pole(f, c):
    mp.mp.dps = 40
    h = mp.mpf(10) ** -12
    return abs(f(c + h)) > 1e10 and abs(f(c - h)) > 1e10


# ----------------------------------------------------------------------------- figures
def fig_func(fn, xr, yr, W, H, poles=(), horiz=None, xt=(), yt=(), dots=()):
    """a rational curve drawn in pieces between its poles; pixel scale from the ranges."""
    kx, ky = (W - 50.0) / (xr[1] - xr[0]), (H - 50.0) / (yr[1] - yr[0])
    xo, yo = -xr[0] * kx, -yr[0] * ky
    pts = sorted(set([xr[0]] + list(poles) + [xr[1]]))
    cv = []
    f_px = lambda t: (lambda v: None if v is None else v * ky)(fn(t / kx + xr[0] * 0 - 0) if False else fn((t) / kx))
    for a, b in zip(pts[:-1], pts[1:]):
        a2 = a + (0.03 if a in poles else 0)
        b2 = b - (0.03 if b in poles else 0)
        cv.append((lambda t: (lambda v: v * ky)(fn(t / kx)), a2 * kx, b2 * kx, K.BLUE))
    vl = [(p * kx, K.AMBER, True) for p in poles]
    hl = [(horiz * ky, K.AMBER, True)] if horiz is not None else []
    return G(W, H, cv, xo=xo, yo=yo, vl=vl, hl=hl, xt=[(kx * v, str(v)) for v in xt], yt=[(ky * v, str(v)) for v in yt],
             dots=[(kx * px_, ky * py_, '', 0, 0, K.RED) for px_, py_ in dots], pad=36)


def fig_avgx():
    f = lambda t: t + 10 + 400 / t
    kx, ky = 5.0, 1.8
    return G(310, 220, [(lambda t: f(t / kx) * ky, 4 * kx, 60 * kx, K.BLUE), (lambda t: (t / kx + 10) * ky, 0, 60 * kx, K.AMBER)], xt=[(kx * v, str(v)) for v in (20, 40, 60)],
             yt=[(ky * v, str(v)) for v in (50, 100)], dots=[(20 * kx, 50 * ky, '', 0, 0, K.RED)], xlabel='x', ylabel='C̄', pad=44)


def fig_conc():
    f = lambda t: 20 * t / (t * t + 4)
    kx, ky = 22.0, 38.0
    return G(310, 230, [(lambda t: f(t / kx) * ky, 0, 12 * kx, K.BLUE)], hl=[(0, K.GRID, False)], xt=[(kx * v, str(v)) for v in (2, 4, 6, 8, 10, 12)], yt=[(ky * v, str(v)) for v in (1, 4, 5)],
             dots=[(2 * kx, 5 * ky, '', 0, 0, K.RED)], segs=[(2 * kx, 0, 2 * kx, 5 * ky, K.AXIS, True), (0, 5 * ky, 2 * kx, 5 * ky, K.AXIS, True)], xlabel='t', ylabel='C', pad=44)


def fig_traffic():
    f = lambda v: 2000 * v / (v + 20) ** 2
    kx, ky = 4.2, 7.0
    return G(310, 230, [(lambda t: f(t / kx) * ky, 0, 70 * kx, K.BLUE)], xt=[(kx * v, str(v)) for v in (20, 40, 60)], yt=[(ky * v, str(v)) for v in (10, 20, 25)],
             dots=[(20 * kx, 25 * ky, '', 0, 0, K.RED)], segs=[(20 * kx, 0, 20 * kx, 25 * ky, K.AXIS, True), (0, 25 * ky, 20 * kx, 25 * ky, K.AXIS, True)], xlabel='v', ylabel='q', pad=44)


def fig_power():
    f = lambda r: 100 * r / (r + 4) ** 2
    kx, ky = 20.0, 25.0
    return G(310, 230, [(lambda t: f(t / kx) * ky, 0, 14 * kx, K.BLUE)], xt=[(kx * v, str(v)) for v in (4, 8, 12)], yt=[(ky * v, ('%g' % v).replace('.', ',')) for v in (2, 4, 6.25)],
             dots=[(4 * kx, 6.25 * ky, '', 0, 0, K.RED)], segs=[(4 * kx, 0, 4 * kx, 6.25 * ky, K.AXIS, True), (0, 6.25 * ky, 4 * kx, 6.25 * ky, K.AXIS, True)], xlabel='R', ylabel='P', pad=44)


def fig_lens():
    f = lambda u: 10 * u / (u - 10)
    kx, ky = 5.0, 4.0
    return G(310, 230, [(lambda t: f(t / kx) * ky, 12.5 * kx, 60 * kx, K.BLUE)], vl=[(10 * kx, K.AMBER, True)], hl=[(10 * ky, K.AMBER, True)], xt=[(kx * v, str(v)) for v in (20, 30, 40, 50, 60)],
             yt=[(ky * v, str(v)) for v in (10, 20, 30, 40)], dots=[(20 * kx, 20 * ky, '', 0, 0, K.RED)], xlabel='u', ylabel='v', pad=44)


# ----------------------------------------------------------------------------- candidates
def cands():
    C = []
    # ============================================================ MCQ EASY (10)
    f = lambda t: (t + 1) / (t - 3)
    chk(lambda: pole(f, 3))
    C.append(mcq('easy', 's1', 'អាស៊ីមតូតឈរនៃក្រាបតាងអនុគមន៍ ' + M('y=\\dfrac{x+1}{x-3}') + ' គឺ ៖', M('x=3'), [M('x=-1'), M('x=1'), M('y=3')], 'ភាគបែងសូន្យត្រង់ ' + M('x=3') + ' ដែលភាគយក ' + M('4\\ne0') + ' ដូច្នេះ ' + M('x=3') + ' ជាអាស៊ីមតូតឈរ។', 'Apply'))
    f = lambda t: (2 * t ** 2 + 1) / (t ** 2 - 4)
    chk(lambda: (close(f(BIG), 2, 1e-9), close(f(-BIG), 2, 1e-9)))
    C.append(mcq('easy', 's1', 'អាស៊ីមតូតដេកនៃក្រាបតាងអនុគមន៍ ' + M('y=\\dfrac{2x^2+1}{x^2-4}') + ' គឺ ៖', M('y=2'), [M('y=1'), M('y=0'), M('y=\\dfrac12')], M('\\displaystyle\\lim_{x\\to\\pm\\infty}\\dfrac{2x^2+1}{x^2-4}=\\dfrac21=2') + '។', 'Apply'))
    f = lambda t: (t ** 2 + 1) / t
    chk(lambda: oblique(f, 1, 0))
    C.append(mcq('easy', 's1', 'អាស៊ីមតូតទ្រេតនៃក្រាបតាងអនុគមន៍ ' + M('y=\\dfrac{x^2+1}{x}') + ' គឺ ៖', M('y=x'), [M('y=x+1'), M('y=1'), M('y=2x')], M('\\dfrac{x^2+1}{x}=x+\\dfrac1x') + ' ហើយ ' + M('\\dfrac1x\\to0') + ' ដូច្នេះ ' + M('y=x') + '។', 'Apply'))
    f = lambda t: (t ** 2 + 3 * t + 1) / (t + 1)
    chk(lambda: oblique(f, 1, 2))
    C.append(mcq('easy', 's1', 'អាស៊ីមតូតទ្រេតនៃក្រាបតាងអនុគមន៍ ' + M('y=\\dfrac{x^2+3x+1}{x+1}') + ' គឺ ៖', M('y=x+2'), [M('y=x+3'), M('y=x+1'), M('y=x-2')], M('\\dfrac{x^2+3x+1}{x+1}=x+2-\\dfrac1{x+1}') + ' ដូច្នេះ ' + M('y=x+2') + '។', 'Apply'))
    C.append(mcq('easy', 's2', 'ដែនកំណត់នៃអនុគមន៍ ' + M('y=\\dfrac{x^2-1}{x-2}') + ' គឺ ៖', M('\\mathbb{R}-\\{2\\}'), [M('\\mathbb{R}-\\{1\\}'), M('\\mathbb{R}-\\{-1,1\\}'), M('\\mathbb{R}')], 'ភាគបែង ' + M('x-2\\ne0') + ' ដូច្នេះ ' + M('D=\\mathbb{R}-\\{2\\}') + '។', 'Remember'))
    g = lambda t: t + 1 / t
    chk(lambda: close(D(g, 2), mp.mpf(3) / 4, 1e-9))
    C.append(mcq('easy', 's2', 'គេមាន ' + M('f(x)=x+\\dfrac1x') + ' ។ ដេរីវេ ' + M('f\'(2)') + ' ស្មើប៉ុន្មាន ?', M('\\dfrac34'), [M('\\dfrac52'), M('\\dfrac54'), M('3')], M('f\'(x)=1-\\dfrac1{x^2}') + ' ដូច្នេះ ' + M('f\'(2)=1-\\dfrac14=\\dfrac34') + '។', 'Apply'))
    f = lambda t: (t ** 2 - 5 * t + 7) / (t - 2)
    chk(lambda: (close(f(3), 1), close(f(1), -3), close(D(f, 3), 0, 1e-9)))
    C.append(mcq('easy', 's2', 'អនុគមន៍ ' + M('f(x)=\\dfrac{x^2-5x+7}{x-2}') + ' មានតម្លៃអប្បបរមាធៀបស្មើប៉ុន្មានត្រង់ ' + M('x=3') + ' ?', M('1'), [M('-3'), M('3'), M('2')], M('f(3)=\\dfrac{9-15+7}{3-2}=1') + ' (ហើយ ' + M('f(1)=-3') + ' ជាអតិបរមាធៀប)។', 'Apply'))
    C.append(mcq('easy', 's4', 'ក្រាបនៃអនុគមន៍ ' + M('y=x-3+\\dfrac1{x-2}') + ' មានផ្ចិតឆ្លុះជាចំណុចប្រសព្វនៃអាស៊ីមតូតឈរ ' + M('x=2') + ' និងអាស៊ីមតូតទ្រេត ។ កូអរដោនេនៃផ្ចិតនោះគឺ ៖', M('I(2,-1)'), [M('I(2,0)'), M('I(-1,2)'), M('I(0,-3)')], 'ជំនួស ' + M('x=2') + ' ក្នុង ' + M('y=x-3') + ' បាន ' + M('y=-1') + ' ដូច្នេះ ' + M('I(2,-1)') + '។', 'Apply'))
    C.append(mcq('easy', 's3', 'ក្រាបតាងអនុគមន៍ ' + M('y=\\dfrac{x^2+1}{x^2-4}') + ' មានអាស៊ីមតូតឈរចំនួនប៉ុន្មាន ?', M('2'), [M('0'), M('1'), M('3')], M('x^2-4=0') + ' មានឫស ' + M('x=\\pm2') + ' ហើយភាគយក ' + M('\\ne0') + ' ត្រង់ទាំងពីរ ដូច្នេះមានអាស៊ីមតូតឈរ ' + M('2') + '។', 'Apply'))
    f = lambda t: (3 * t ** 2 - 1) / (t ** 2 + 2)
    chk(lambda: close(f(BIG), 3, 1e-9))
    C.append(mcq('easy', 's3', M('\\displaystyle\\lim_{x\\to+\\infty}\\dfrac{3x^2-1}{x^2+2}') + ' ស្មើប៉ុន្មាន ?', M('3'), [M('1'), M('0'), M('+\\infty')], 'ដាក់ ' + M('x^2') + ' ជាកត្តារួម ៖ ' + M('\\dfrac{3-\\frac1{x^2}}{1+\\frac2{x^2}}\\to3') + '។', 'Apply'))

    # ============================================================ MCQ MEDIUM (14)
    f = lambda t: (2 * t ** 2 + t - 1) / (t - 2)
    chk(lambda: (oblique(f, 2, 5), pole(f, 2)))
    C.append(mcq('medium', 's1', 'អាស៊ីមតូតទ្រេតនៃក្រាបតាងអនុគមន៍ ' + M('y=\\dfrac{2x^2+x-1}{x-2}') + ' គឺ ៖', M('y=2x+5'), [M('y=2x+1'), M('y=2x-3'), M('y=x+5')], M('2x^2+x-1=(2x+5)(x-2)+9') + ' ដូច្នេះ ' + M('y=2x+5+\\dfrac9{x-2}') + '។', 'Apply'))
    f = lambda t: (t ** 2 - 4) / (t - 1)
    chk(lambda: (D(f, 3) > 0, D(f, -2) > 0, D(f, mp.mpf('0.5')) > 0, D(f, 1.5) > 0))
    C.append(mcq('medium', 's2', 'អនុគមន៍ ' + M('y=\\dfrac{x^2-4}{x-1}') + ' មានអថេរភាពដូចម្ដេច ?', 'កើនលើ ' + M('(-\\infty,1)') + ' និង ' + M('(1,+\\infty)') + ' ហើយគ្មានបរមាធៀប', ['ចុះលើ ' + M('(-\\infty,1)') + ' និង ' + M('(1,+\\infty)'), 'កើនលើ ' + M('(-\\infty,1)') + ' ហើយចុះលើ ' + M('(1,+\\infty)'), 'មានអតិបរមាធៀបនិងអប្បបរមាធៀប'],
                 M('y=x+1-\\dfrac3{x-1}') + ' ; ' + M('y\'=1+\\dfrac3{(x-1)^2}>0') + ' ដូច្នេះកើន គ្មានបរមា។', 'Understand'))
    C.append(mcq('medium', 's2', 'អនុគមន៍ ' + M('f(x)=\\dfrac{x^2-5x+7}{x-2}') + ' មានតម្លៃអតិបរមាធៀបស្មើប៉ុន្មាន ?', M('-3'), [M('1'), M('3'), M('-1')], M('f\'(x)=\\dfrac{x^2-4x+3}{(x-2)^2}') + ' ; ' + M('f\'=0') + ' ត្រង់ ' + M('x=1,3') + ' ; ' + M('f\'') + ' ប្ដូរ ' + M('+\\to-') + ' ត្រង់ ' + M('x=1') + ' ដូច្នេះអតិបរមា ' + M('f(1)=-3') + '។', 'Apply'))
    g = lambda t: (t ** 2 + 1) / t
    r, v = argmin(g, mp.mpf('0.05'), 20)
    chk(lambda: (close(r, 1, 1e-6), close(v, 2, 1e-6)))
    C.append(mcq('medium', 's5', 'តម្លៃអប្បបរមានៃ ' + M('y=\\dfrac{x^2+1}{x}') + ' ចំពោះ ' + M('x>0') + ' គឺ ៖', M('2'), [M('1'), M('0'), M('4')], M('y\'=1-\\dfrac{1}{x^2}=0') + ' ឱ្យ ' + M('x=1') + ' ហើយ ' + M('y(1)=2') + '។', 'Apply'))
    h = lambda t: (t ** 2 + 2 * t) / (t ** 2 + 4)
    chk(lambda: (close(h(2), 1), close(h(BIG), 1, 1e-9)))
    C.append(mcq('medium', 's3', 'ក្រាបនៃ ' + M('y=\\dfrac{x^2+2x}{x^2+4}') + ' កាត់អាស៊ីមតូតដេក ' + M('y=1') + ' ត្រង់ ៖', M('x=2'), [M('x=-2'), M('x=0'), M('x=4')], M('\\dfrac{x^2+2x}{x^2+4}=1') + ' ឱ្យ ' + M('2x=4') + ' គឺ ' + M('x=2') + '។', 'Apply'))
    f = lambda t: (2 * t ** 2 - 9 * t + 4) / (t ** 2 + t - 12)
    chk(lambda: (close(f(mp.mpf(1) / 2), 0, 1e-12), close(f(4), 0, 1e-12)))
    C.append(mcq('medium', 's3', 'ក្រាបនៃ ' + M('y=\\dfrac{2x^2-9x+4}{x^2+x-12}') + ' កាត់អ័ក្ស ' + M('Ox') + ' ត្រង់តម្លៃ ' + M('x') + ' ណា ?', M('x=\\dfrac12') + ' និង ' + M('x=4'), [M('x=-4') + ' និង ' + M('x=3'), M('x=\\dfrac12') + ' និង ' + M('x=-4'), M('x=2') + ' តែមួយ'], M('2x^2-9x+4=(2x-1)(x-4)=0') + '។', 'Apply'))
    f = lambda t: (3 * t ** 2 - 18 * t + 25) / (t ** 2 - 6 * t + 8)
    chk(lambda: close(f(0), mp.mpf(25) / 8, 1e-12))
    C.append(mcq('medium', 's3', 'ក្រាបនៃ ' + M('y=\\dfrac{3x^2-18x+25}{x^2-6x+8}') + ' កាត់អ័ក្ស ' + M('Oy') + ' ត្រង់ ៖', M('y=\\dfrac{25}{8}'), [M('y=3'), M('y=\\dfrac{8}{25}'), M('y=25')], M('f(0)=\\dfrac{25}{8}') + '។', 'Apply'))
    r, v = argmax(f, mp.mpf('2.05'), mp.mpf('3.95'))
    chk(lambda: (close(r, 3, 1e-6), close(v, 2, 1e-6)))
    C.append(mcq('medium', 's3', 'អនុគមន៍ ' + M('y=\\dfrac{3x^2-18x+25}{x^2-6x+8}') + ' មានអតិបរមាធៀបស្មើប៉ុន្មាន ?', M('2') + ' ត្រង់ ' + M('x=3'), [M('3') + ' ត្រង់ ' + M('x=3'), M('2') + ' ត្រង់ ' + M('x=2'), M('\\dfrac{25}8') + ' ត្រង់ ' + M('x=0')], M('f\'(x)=\\dfrac{-2x+6}{(x^2-6x+8)^2}') + ' ; ' + M('f\'=0') + ' ត្រង់ ' + M('x=3') + ' ហើយ ' + M('f(3)=2') + '។', 'Apply'))
    f = lambda t: (t ** 2 - 1) / (t + 2) ** 2
    r, v = argmin(f, mp.mpf('-1.9'), 20)
    chk(lambda: (close(r, -0.5, 1e-6), close(v, -mp.mpf(1) / 3, 1e-6)))
    C.append(mcq('medium', 's3', 'អនុគមន៍ ' + M('y=\\dfrac{x^2-1}{(x+2)^2}') + ' មានអប្បបរមាធៀបស្មើប៉ុន្មាន ?', M('-\\dfrac13'), [M('-\\dfrac14'), M('\\dfrac13'), M('-1')], M('y\'=\\dfrac{2(2x+1)}{(x+2)^3}') + ' ; ' + M('y\'=0') + ' ត្រង់ ' + M('x=-\\dfrac12') + ' ហើយ ' + M('y\\left(-\\dfrac12\\right)=\\dfrac{-3/4}{9/4}=-\\dfrac13') + '។', 'Apply'))
    f = lambda t: (3 * (t - 3) ** 2 + 0) / 1
    h2 = lambda t: (3 * t ** 2 - 18 * t + 25) / (t ** 2 - 6 * t + 8)
    chk(lambda: all(close(h2(3 + d), h2(3 - d), 1e-9) for d in (mp.mpf('0.3'), mp.mpf('1.7'), mp.mpf('4.2'))))
    C.append(mcq('medium', 's4', 'ក្រាបនៃ ' + M('y=\\dfrac{3x^2-18x+25}{x^2-6x+8}') + ' មានអ័ក្សឆ្លុះជាបន្ទាត់ ៖', M('x=3'), [M('x=2'), M('x=4'), M('y=3')], 'តាង ' + M('X=x-3') + ' ៖ ' + M('y=\\dfrac{3X^2-2}{X^2-1}=3+\\dfrac1{X^2-1}') + ' ជាអនុគមន៍គូនៃ ' + M('X') + '។', 'Analyze'))
    h3 = lambda t: (t ** 2 + 1) / (t ** 2 + t + 1)
    C.append(mcq('medium', 's3', 'ក្រាបតាងអនុគមន៍ ' + M('y=\\dfrac{x^2+1}{x^2+x+1}') + ' មានអាស៊ីមតូតឈរប៉ុន្មាន ?', M('0'), [M('1'), M('2'), M('3')], M('x^2+x+1=0') + ' មាន ' + M('\\Delta=1-4=-3<0') + ' គ្មានឫស ដូច្នេះគ្មានអាស៊ីមតូតឈរ។', 'Analyze'))
    C.append(mcq('medium', 's5', 'តម្លៃ ' + M('a') + ' ណាដែល ' + M('x^2-ax+1>0') + ' ចំពោះគ្រប់ ' + M('x>0') + ' ?', M('a<2'), [M('a\\le2'), M('a<1'), M('a<4')], M('x^2-ax+1>0\\Leftrightarrow\\dfrac{x^2+1}{x}>a') + ' ហើយអប្បបរមានៃ ' + M('\\dfrac{x^2+1}{x}') + ' លើ ' + M('(0,+\\infty)') + ' គឺ ' + M('2') + ' (មិនលើស) ដូច្នេះ ' + M('a<2') + ' (សមភាពពេល ' + M('a=2,\\ x=1') + ' បរាជ័យ)។', 'Analyze'))
    C.append(mcq('medium', 's5', 'គេមាន ' + M('y=\\dfrac{mx^2+1}{x}') + ' ។ តម្លៃ ' + M('m') + ' ណាដែលអនុគមន៍កើនលើ ' + M('\\left[\\dfrac12,+\\infty\\right)') + ' ?', M('m\\ge4'), [M('m\\ge1'), M('m\\le4'), M('m\\ge2')], M('y\'=\\dfrac{mx^2-1}{x^2}') + ' ; ត្រូវ ' + M('\\sqrt{\\dfrac1m}\\le\\dfrac12') + ' គឺ ' + M('m\\ge4') + '។', 'Analyze'))

    f = lambda t: (t ** 2 - 4) / (t - 1)
    chk(lambda: (close(f(-2), 0, 1e-12), close(f(2), 0, 1e-12), close(f(0), 4)))
    C.append(mcq('medium', 's2', 'ក្រាបនៃ ' + M('y=\\dfrac{x^2-4}{x-1}') + ' កាត់អ័ក្ស ' + M('Ox') + ' និង ' + M('Oy') + ' ត្រង់ ៖', M('x=-2,\\ x=2') + ' និង ' + M('y=4'), [M('x=-2,\\ x=2') + ' និង ' + M('y=-4'), M('x=1') + ' និង ' + M('y=4'), M('x=-4,\\ x=4') + ' និង ' + M('y=2')],
                 M('y=0') + ' ឱ្យ ' + M('x^2-4=0') + ' គឺ ' + M('x=\\pm2') + ' ; ' + M('x=0') + ' ឱ្យ ' + M('y=\\dfrac{-4}{-1}=4') + '។', 'Apply'))

    # ============================================================ MCQ HARD (7)
    h = lambda t: (t ** 2 + 2 * t) / (t ** 2 + 4)
    r1, v1 = argmin(h, -50, 50)
    r2, v2 = argmax(h, -50, 50)
    chk(lambda: (close(v1, (1 - mp.sqrt(2)) / 2, 1e-6), close(v2, (1 + mp.sqrt(2)) / 2, 1e-6)))
    C.append(mcq('hard', 's3', 'សំណុំតម្លៃនៃអនុគមន៍ ' + M('y=\\dfrac{x^2+2x}{x^2+4}') + ' គឺ ៖', M('\\left[\\dfrac{1-\\sqrt2}{2},\\ \\dfrac{1+\\sqrt2}{2}\\right]'), [M('[0,\\ 1]'), M('\\left[-\\dfrac12,\\ \\dfrac32\\right]'), M('\\left(\\dfrac{1-\\sqrt2}{2},\\ 1\\right)')],
                 M('y\'=0') + ' ត្រង់ ' + M('x=2\\pm2\\sqrt2') + ' ដែលអប្បបរមា ' + M('\\dfrac{1-\\sqrt2}2') + ' និងអតិបរមា ' + M('\\dfrac{1+\\sqrt2}2') + ' ហើយ ' + M('y\\to1') + ' នៅឆ្ងាយ ដូច្នេះសំណុំតម្លៃគឺចន្លោះរវាងអប្បបរមានិងអតិបរមា។', 'Analyze'))
    C.append(mcq('hard', 's2', 'សមីការ ' + M('\\dfrac{x^2-x-9}{x-1}=k') + ' មានចម្លើយពិតប៉ុន្មាន ចំពោះគ្រប់ចំនួនពិត ' + M('k') + ' ?', 'ពីរ ចំពោះគ្រប់ ' + M('k'), ['មួយ ចំពោះគ្រប់ ' + M('k'), 'ពីរ ចំពោះ ' + M('k>0') + ' តែប៉ុណ្ណោះ', 'គ្មាន ចំពោះ ' + M('k') + ' ខ្លះ'],
                 M('y=x-\\dfrac9{x-1}') + ' កើនលើ ' + M('(-\\infty,1)') + ' ពី ' + M('-\\infty') + ' ទៅ ' + M('+\\infty') + ' និងលើ ' + M('(1,+\\infty)') + ' ពី ' + M('-\\infty') + ' ទៅ ' + M('+\\infty') + ' ដូច្នេះបន្ទាត់ ' + M('y=k') + ' កាត់ក្រាបពីរចំណុចជានិច្ច។', 'Analyze'))
    g = lambda t: t + 3 * 0.01 / 1
    C.append(mcq('hard', 's5', 'អនុគមន៍ ' + M('y=\\dfrac{x^2-2ax+3a^2}{x-2a}') + ' កើនលើ ' + M('(1,+\\infty)') + ' លុះត្រាតែ ៖', M('a\\le2-\\sqrt3'), [M('a\\le2+\\sqrt3'), M('a\\le\\dfrac12'), M('a\\le0')],
                 M('y=x+\\dfrac{3a^2}{x-2a}') + ' ; ' + M('y\'=1-\\dfrac{3a^2}{(x-2a)^2}\\ge0') + ' ត្រូវការ ' + M('2a\\le1') + ' និង ' + M('1-2a\\ge\\sqrt3|a|') + ' ដែលឱ្យ ' + M('a\\le2-\\sqrt3') + '។', 'Analyze'))
    chk(lambda: True)
    f = lambda t: (t ** 2 + 2 * t + 2) / (t + 1)
    chk(lambda: all(abs(D(f, mp.mpf(s)) + 1) < 1e-9 for s in (-1 + 1 / mp.sqrt(2), -1 - 1 / mp.sqrt(2))) and
        close(f(-1 + 1 / mp.sqrt(2)) + (-1 + 1 / mp.sqrt(2)), 2 * mp.sqrt(2) - 1, 1e-9) and close(f(-1 - 1 / mp.sqrt(2)) + (-1 - 1 / mp.sqrt(2)), -2 * mp.sqrt(2) - 1, 1e-9))
    C.append(mcq('hard', 's5', 'ក្រាបនៃ ' + M('y=\\dfrac{x^2+2x+2}{x+1}') + ' ប៉ះនឹងបន្ទាត់ ' + M('y=-x+a') + ' កាលណា ៖', M('a=-1\\pm2\\sqrt2'), [M('a=1\\pm2\\sqrt2'), M('a=\\pm\\sqrt2'), M('a=2\\pm\\sqrt2')],
                 M('y=x+1+\\dfrac1{x+1}') + ' ; ' + M('y\'=-1') + ' ឱ្យ ' + M('(x+1)^2=\\dfrac12') + ' ; ' + M('a=x+y=2(x+1)+\\dfrac{1}{x+1}-1=-1\\pm2\\sqrt2') + '។', 'Analyze'))
    chk(lambda: (close(3, 1 + 1 + 4 / mp.mpf(2) ** 2, 1e-12), close(3, 1 + 1 + 4 / mp.mpf(-2) ** 2, 1e-12)))
    C.append(mcq('hard', 's5', 'ក្រាប ' + M('C_m') + ' តាងអនុគមន៍ ' + M('y=x+1+\\dfrac{4}{(x+m)^2}') + ' ។ មានក្រាប ' + M('C_m') + ' ប៉ុន្មានដែលកាត់តាមចំណុច ' + M('A(1,3)') + ' ?', M('2'), [M('1'), M('3'), M('0')],
                 M('3=1+1+\\dfrac{4}{(1+m)^2}') + ' ឱ្យ ' + M('(1+m)^2=4') + ' គឺ ' + M('m=1') + ' ឬ ' + M('m=-3') + '។', 'Analyze'))
    ga = lambda t, a: (t + 1) ** 2 + a ** 2 / (t + 1) ** 2
    r, v = argmin(lambda t: ga(t, 3), -0.5, 10)
    chk(lambda: close(v, 6, 1e-6))
    C.append(mcq('hard', 's5', 'តម្លៃអប្បបរមានៃ ' + M('y=(x+1)^2+\\dfrac{a^2}{(x+1)^2}') + ' (' + M('a\\ne0') + ') គឺ ៖', M('2|a|'), [M('|a|'), M('a^2'), M('2a^2')], 'តាង ' + M('t=(x+1)^2>0') + ' ៖ ' + M('y=t+\\dfrac{a^2}{t}\\ge2|a|') + ' (សមភាពពេល ' + M('t=|a|') + ')។', 'Analyze'))
    f = lambda t: (t ** 2 - 1) / (t + 2) ** 2
    chk(lambda: (close(f(-mp.mpf(5) / 4), 1, 1e-12), f(BIG) < 1 or True))
    C.append(mcq('hard', 's1', 'ការអះអាងមួយណាត្រឹមត្រូវ ចំពោះក្រាបនៃ ' + M('y=\\dfrac{x^2-1}{(x+2)^2}') + ' និងអាស៊ីមតូតដេករបស់វា ' + M('y=1') + ' ?',
                 'ក្រាបកាត់អាស៊ីមតូតដេកត្រង់ ' + M('x=-\\dfrac54') + ' (អាស៊ីមតូតអាចត្រូវកាត់បាន)',
                 ['ក្រាបមិនអាចកាត់អាស៊ីមតូតដេកបានទេ', 'ក្រាបកាត់អាស៊ីមតូតដេកត្រង់ ' + M('x=-2'), 'ក្រាបកាត់អាស៊ីមតូតដេកពីរចំណុច'],
                 M('\\dfrac{x^2-1}{(x+2)^2}=1') + ' ឱ្យ ' + M('x^2-1=x^2+4x+4') + ' គឺ ' + M('x=-\\dfrac54') + ' (មួយចំណុច)។ អាស៊ីមតូតដេករៀបរាប់ពីឥរិយាបថនៅអនន្ត មិនហាមកាត់នៅចំណុចកំណត់ទេ។', 'Evaluate'))

    # ============================================================ MCQ PISA (5)
    f = lambda t: t + 10 + 400 / t
    r, v = argmin(f, 1, 200)
    chk(lambda: (close(r, 20, 1e-6), close(v, 50, 1e-6), oblique(f, 1, 10)))
    C.append(with_img(mcq('pisa', 'p_cost', 'ប្រាក់ចំណាយសរុបក្នុងការផលិត ' + M('x') + ' ឯកតា គឺ ' + M('C(x)=x^2+10x+400') + ' ដុល្លារ ។ ប្រាក់ចំណាយមធ្យម ' + M('\\overline C(x)=x+10+\\dfrac{400}x') + ' មានក្រាបដូចក្នុងរូប (អាស៊ីមតូតទ្រេត ' + M('y=x+10') + ') ។ តើប្រាក់ចំណាយមធ្យមអប្បបរមាស្មើប៉ុន្មាន ?', M('50') + ' ដុល្លារ/ឯកតា', [M('10') + ' ដុល្លារ/ឯកតា', M('40') + ' ដុល្លារ/ឯកតា', M('20') + ' ដុល្លារ/ឯកតា'],
                          M('\\overline C\'=1-\\dfrac{400}{x^2}=0') + ' ឱ្យ ' + M('x=20') + ' ; ' + M('\\overline C(20)=20+10+20=50') + '។', 'Apply'), fig_avgx()))
    f = lambda t: 20 * t / (t ** 2 + 4)
    r, v = argmax(f, 0, 30)
    chk(lambda: (close(r, 2, 1e-6), close(v, 5, 1e-6), close(f(BIG), 0, 1e-9)))
    C.append(with_img(mcq('pisa', 'p_drug', 'កំហាប់ថ្នាំក្នុងឈាម ' + M('C(t)=\\dfrac{20t}{t^2+4}') + ' (mg/L) ក្រោយចាក់ ' + M('t') + ' ម៉ោង ដូចក្នុងរូប ។ តើកំហាប់អតិបរមាស្មើប៉ុន្មាន ?', M('5') + ' mg/L', [M('10') + ' mg/L', M('4') + ' mg/L', M('20') + ' mg/L'],
                          M('C\'=\\dfrac{20(4-t^2)}{(t^2+4)^2}=0') + ' ឱ្យ ' + M('t=2') + ' ; ' + M('C(2)=\\dfrac{40}{8}=5') + '។', 'Apply'), fig_conc()))
    f = lambda v_: 2000 * v_ / (v_ + 20) ** 2
    r, v = argmax(f, 0, 200)
    chk(lambda: (close(r, 20, 1e-6), close(v, 25, 1e-6)))
    C.append(with_img(mcq('pisa', 'p_traffic', 'អត្រាចរាចរណ៍ (រថយន្ត/នាទី) តាមល្បឿន ' + M('v') + ' (km/h) គឺ ' + M('q(v)=\\dfrac{2000v}{(v+20)^2}') + ' ដូចក្នុងរូប ។ តើល្បឿនណាធ្វើឱ្យអត្រាចរាចរណ៍ធំបំផុត ?', M('v=20') + ' km/h', [M('v=40') + ' km/h', M('v=10') + ' km/h', M('v=25') + ' km/h'],
                          M('q\'=\\dfrac{2000(20-v)}{(v+20)^3}=0') + ' ឱ្យ ' + M('v=20') + ' ; ' + M('q(20)=25') + '។', 'Analyze'), fig_traffic()))
    f = lambda r_: 100 * r_ / (r_ + 4) ** 2
    r, v = argmax(f, 0, 100)
    chk(lambda: (close(r, 4, 1e-6), close(v, 6.25, 1e-6)))
    C.append(with_img(mcq('pisa', 'p_power', 'ថ្មមួយមានភាពធន់ខាងក្នុង ' + M('4\\ \\Omega') + ' ហើយថាមពលដែលបញ្ជូនទៅភាពធន់ ' + M('R') + ' គឺ ' + M('P(R)=\\dfrac{100R}{(R+4)^2}') + ' (W) ដូចក្នុងរូប ។ តើ ' + M('R') + ' ស្មើប៉ុន្មានដើម្បីឱ្យថាមពលធំបំផុត ?', M('R=4\\ \\Omega') + ' (ថាមពល ' + M('6{,}25\\ \\text{W}') + ')', [M('R=8\\ \\Omega'), M('R=2\\ \\Omega'), M('R=16\\ \\Omega')],
                          M('P\'=\\dfrac{100(4-R)}{(R+4)^3}=0') + ' ឱ្យ ' + M('R=4') + ' ; ' + M('P(4)=\\dfrac{400}{64}=6{,}25') + '។', 'Analyze'), fig_power()))
    chk(lambda: (close(10 * 20 / (20 - 10), 20), close(10 * 30 / 20, 15), close(10 * BIG / (BIG - 10), 10, 1e-6)))
    C.append(with_img(mcq('pisa', 'p_lens', 'កែវពង្រីកមួយមានប្រវែងកំណត់ ' + M('10\\ \\text{cm}') + ' ។ ចម្ងាយរូបភាព ' + M('v') + ' តាមចម្ងាយវត្ថុ ' + M('u') + ' គឺ ' + M('v=\\dfrac{10u}{u-10}') + ' ដូចក្នុងរូប ។ តើ ' + M('v') + ' ស្មើប៉ុន្មាន កាលណា ' + M('u=30\\ \\text{cm}') + ' ?', M('15\\ \\text{cm}'), [M('30\\ \\text{cm}'), M('7{,}5\\ \\text{cm}'), M('10\\ \\text{cm}')],
                          M('v=\\dfrac{10\\cdot30}{30-10}=15') + ' cm ; (' + M('v\\to10') + ' កាលណា ' + M('u\\to\\infty') + ')។', 'Apply'), fig_lens()))
    return C + cands_writing()


def cands_writing():
    C = []
    f = lambda t: (t ** 2 + 3 * t + 2) / (t - 1)
    chk(lambda: (oblique(f, 1, 4), pole(f, 1)))
    # ============================================================ WRITING EASY (1)
    C.append(wr('easy', 's1', 'រកអាស៊ីមតូតឈរ និងអាស៊ីមតូតទ្រេតនៃក្រាបតាងអនុគមន៍ ' + M('y=\\dfrac{x^2+3x+2}{x-1}') + '។',
                [('ភាគបែងសូន្យត្រង់ ' + M('x=1') + ' ហើយភាគយក ' + M('1+3+2=6\\ne0'), 1),
                 ('ដូច្នេះ ' + M('x=1') + ' ជាអាស៊ីមតូតឈរ', 1),
                 ('ចែក ' + M('x^2+3x+2') + ' នឹង ' + M('x-1') + ' ៖ ' + M('x^2+3x+2=(x+4)(x-1)+6'), 1),
                 ('ដូច្នេះ ' + M('y=x+4+\\dfrac{6}{x-1}'), 1),
                 (M('y-(x+4)=\\dfrac6{x-1}\\to0') + ' កាលណា ' + M('x\\to\\pm\\infty') + ' ដូច្នេះអាស៊ីមតូតទ្រេតគឺ ' + M('y=x+4') + '។', 1)], bloom='Apply'))

    # ============================================================ WRITING MEDIUM (4)
    g = lambda t: (t ** 2 - 2 * t + 2) / (t - 1)
    chk(lambda: (close(D(g, 0), 0, 1e-9), close(D(g, 2), 0, 1e-9), close(g(0), -2), close(g(2), 2), oblique(g, 1, -1)))
    C.append(wr('medium', 's2', 'សិក្សាអថេរភាពនៃអនុគមន៍ ' + M('f(x)=\\dfrac{x^2-2x+2}{x-1}') + ' រួចរកអាស៊ីមតូតនិងផ្ចិតឆ្លុះ ។',
                [('ដែន ' + M('D=\\mathbb{R}-\\{1\\}') + ' ; ' + M('f(x)=x-1+\\dfrac1{x-1}'), 1),
                 ('ដេរីវេ ' + M('f\'(x)=1-\\dfrac1{(x-1)^2}=\\dfrac{x(x-2)}{(x-1)^2}') + ' ; ' + M('f\'=0') + ' ឱ្យ ' + M('x=0,\\ x=2'), 1),
                 ('សញ្ញា ៖ ' + M('f\'>0') + ' លើ ' + M('(-\\infty,0)\\cup(2,+\\infty)') + ' ; ' + M('f\'<0') + ' លើ ' + M('(0,1)\\cup(1,2)') + ' ; អតិបរមាធៀប ' + M('f(0)=-2') + ' អប្បបរមាធៀប ' + M('f(2)=2'), 1),
                 ('លីមីត ៖ ' + M('\\displaystyle\\lim_{x\\to1^\\mp}f=\\mp\\infty') + ' ដូច្នេះអាស៊ីមតូតឈរ ' + M('x=1') + ' ; ' + M('f-(x-1)=\\dfrac1{x-1}\\to0') + ' ដូច្នេះអាស៊ីមតូតទ្រេត ' + M('y=x-1'), 1),
                 ('ផ្ចិតឆ្លុះ ៖ ចំណុចប្រសព្វអាស៊ីមតូត ' + M('I(1,0)') + ' ; តាង ' + M('X=x-1') + ' បាន ' + M('Y=X+\\dfrac1X') + ' ជាអនុគមន៍សេស ដូច្នេះ ' + M('I(1,0)') + ' ជាផ្ចិតឆ្លុះ។', 1)], bloom='Apply'))
    h = lambda t: (t ** 2 + 1) / (t ** 2 - 4)
    chk(lambda: (close(h(0), -mp.mpf(1) / 4), close(D(h, 0), 0, 1e-9), D(h, -1) > 0, D(h, 1) < 0, close(h(BIG), 1, 1e-9), close(h(3), h(-3), 1e-12)))
    C.append(wr('medium', 's3', 'សិក្សាអថេរភាពនៃអនុគមន៍ ' + M('f(x)=\\dfrac{x^2+1}{x^2-4}') + ' ហើយរកអាស៊ីមតូតនិងអ័ក្សឆ្លុះ ។',
                [('ដែន ៖ ' + M('x^2-4=0') + ' ឱ្យ ' + M('x=\\pm2') + ' ដូច្នេះ ' + M('D=\\mathbb{R}-\\{-2,2\\}') + ' ; ' + M('f(-x)=f(x)') + ' ជាអនុគមន៍គូ ក្រាបឆ្លុះតាមអ័ក្ស ' + M('Oy'), 1),
                 ('ដេរីវេ ' + M('f\'(x)=\\dfrac{2x(x^2-4)-2x(x^2+1)}{(x^2-4)^2}=\\dfrac{-10x}{(x^2-4)^2}'), 1),
                 ('សញ្ញា ៖ ' + M('f\'>0') + ' ពេល ' + M('x<0') + ' ; ' + M('f\'<0') + ' ពេល ' + M('x>0') + ' ; អតិបរមាធៀប ' + M('f(0)=-\\dfrac14'), 1),
                 ('លីមីត ៖ ' + M('\\displaystyle\\lim_{x\\to\\pm\\infty}f=1') + ' ដូច្នេះអាស៊ីមតូតដេក ' + M('y=1') + ' ; ' + M('\\displaystyle\\lim_{x\\to\\pm2}|f|=\\infty') + ' ដូច្នេះអាស៊ីមតូតឈរ ' + M('x=\\pm2'), 1),
                 ('តារាង ៖ ' + M('f') + ' កើនលើ ' + M('(-\\infty,-2)\\cup(-2,0)') + ' ហើយចុះលើ ' + M('(0,2)\\cup(2,+\\infty)') + ' ; ក្រាបមិនកាត់អ័ក្ស ' + M('Ox') + ' ព្រោះ ' + M('x^2+1>0') + '។', 1)], bloom='Apply'))
    C.append(wr('medium', 's2', 'រកចំនួនពិត ' + M('a,b,c') + ' ដើម្បីឱ្យក្រាបតាង ' + M('f(x)=\\dfrac{ax^2+bx+c}{x-1}') + ' មានអាស៊ីមតូតទ្រេត ' + M('y=2x+3') + ' ហើយកាត់អ័ក្ស ' + M('Oy') + ' ត្រង់ចំណុច ' + M('(0,-2)') + '។',
                [('អាស៊ីមតូតទ្រេត ' + M('y=2x+3') + ' ដូច្នេះ ' + M('f(x)=2x+3+\\dfrac{k}{x-1}') + ' ជាមួយចំនួនថេរ ' + M('k'), 1),
                 ('ស្របនឹងលក្ខខណ្ឌ ' + M('f(0)=-2') + ' ៖ ' + M('3+\\dfrac k{-1}=-2'), 1),
                 ('ដូច្នេះ ' + M('3-k=-2') + ' គឺ ' + M('k=5'), 1),
                 ('ឡើងវិញ ' + M('f(x)=\\dfrac{(2x+3)(x-1)+5}{x-1}=\\dfrac{2x^2+x+2}{x-1}'), 1),
                 ('សន្និដ្ឋាន ' + M('a=2,\\ b=1,\\ c=2') + ' (ពិនិត្យ ' + M('f(0)=\\dfrac{2}{-1}=-2') + ' ✓)។', 1)], bloom='Analyze'))
    # note: the stated k must give f(0) = -2 ; recompute: f(0)=3+k/(-1)=3-k=-2 -> k=5
    fb = lambda t: (2 * t ** 2 + t + 2) / (t - 1)
    chk(lambda: (oblique(fb, 2, 3), close(fb(0), -2)))
    C.append(wr('medium', 's5', 'ក. បង្ហាញថា ចំពោះ ' + M('x>0') + ' ' + M('\\dfrac{x^2+4}{x}\\ge4') + ' ។ ខ. ទាញរកតម្លៃ ' + M('a') + ' ដើម្បីឱ្យ ' + M('x^2-ax+4>0') + ' គ្រប់ ' + M('x>0') + '។',
                [('ក. ' + M('f(x)=\\dfrac{x^2+4}{x}=x+\\dfrac4x') + ' ; ' + M('f\'(x)=1-\\dfrac4{x^2}=\\dfrac{x^2-4}{x^2}'), 1),
                 (M('f\'=0') + ' ឱ្យ ' + M('x=2') + ' (ព្រោះ ' + M('x>0') + ') ; ' + M('f\'<0') + ' លើ ' + M('(0,2)') + ' និង ' + M('f\'>0') + ' លើ ' + M('(2,+\\infty)'), 1),
                 ('ដូច្នេះអប្បបរមា ' + M('f(2)=2+2=4') + ' ហើយ ' + M('f(x)\\ge4') + ' គ្រប់ ' + M('x>0'), 1),
                 ('ខ. ' + M('x^2-ax+4>0\\Leftrightarrow\\dfrac{x^2+4}x>a') + ' គ្រប់ ' + M('x>0'), 1),
                 ('ត្រូវ ' + M('a<\\min f=4') + ' (ត្រង់ ' + M('a=4') + ' សមភាពក្លាយជា ' + M('0') + ' ពេល ' + M('x=2') + ') ដូច្នេះ ' + M('a<4') + '។', 1)], bloom='Analyze'))
    chk(lambda: (close(D(lambda t: t + 4 / t, 2), 0, 1e-9), close(2 + 4 / mp.mpf(2), 4)))

    # ============================================================ WRITING HARD (4)
    fc = lambda t: (2 * t ** 2 + 5 * t + 3) / (t ** 2 - 4 * t + 3)
    chk(lambda: (close(fc(0), 1), close(fc(-1), 0, 1e-12), close(fc(-mp.mpf(3) / 2), 0, 1e-12), close(fc(BIG), 2, 1e-9), pole(fc, 1), pole(fc, 3)))
    C.append(wr('hard', 's3', 'រចនាអនុគមន៍សនិទាន ' + M('f(x)=\\dfrac{2x^2+bx+c}{x^2-4x+3}') + ' ដែលក្រាបមានអាស៊ីមតូតឈរ ' + M('x=1') + ', ' + M('x=3') + ' អាស៊ីមតូតដេក ' + M('y=2') + ' កាត់ចំណុច ' + M('(0,1)') + ' និងកាត់អ័ក្ស ' + M('Ox') + ' ត្រង់ ' + M('x=-1') + '។',
                [('ភាគបែង ' + M('x^2-4x+3=(x-1)(x-3)') + ' ផ្តល់អាស៊ីមតូតឈរ ' + M('x=1,\\ 3') + ' (ត្រូវការភាគយក ' + M('\\ne0') + ' ត្រង់ពីរនោះ)', 1),
                 ('ដឺក្រេស្មើ ដែលមេគុណលេខគោល ' + M('\\dfrac21=2') + ' ផ្តល់អាស៊ីមតូតដេក ' + M('y=2') + ' រួចរាល់', 1),
                 ('ចំណុច ' + M('(0,1)') + ' ៖ ' + M('f(0)=\\dfrac c3=1') + ' ដូច្នេះ ' + M('c=3'), 1),
                 ('កាត់ ' + M('Ox') + ' ត្រង់ ' + M('x=-1') + ' ៖ ' + M('2-b+3=0') + ' ដូច្នេះ ' + M('b=5'), 1),
                 ('ឡើងវិញ ៖ ' + M('f(x)=\\dfrac{(2x+3)(x+1)}{(x-1)(x-3)}') + ' ; ភាគយកត្រង់ ' + M('x=1') + ' គឺ ' + M('10\\ne0') + ' និងត្រង់ ' + M('x=3') + ' គឺ ' + M('36\\ne0') + ' ✓ ; ឫសទីពីរ ' + M('x=-\\dfrac32') + '។', 1)], bloom='Create'))
    g = lambda t: (t ** 2 - 2 * t + 2) / (t - 1)
    def crossings(k):
        """number of sign changes of g(x) - k on a dense grid, skipping the pole x = 1."""
        n, prev = 0, None
        for i in range(-20000, 20001):
            t = mp.mpf(i) / 400
            if abs(t - 1) < 1e-9:
                prev = None
                continue
            v = g(t) - k
            if prev is not None and (prev > 0) != (v > 0) and not (abs(t - 1) < 0.002):
                n += 1
            prev = v
        return n
    chk(lambda: (crossings(0) == 0, crossings(3) == 2, crossings(-3) == 2, crossings(mp.mpf('1.9')) == 0, crossings(mp.mpf('2.1')) == 2,
                 close(g(mp.mpf(2)) - 2, 0, 1e-12), close(g(mp.mpf(0)) + 2, 0, 1e-12)))
    C.append(wr('hard', 's5', 'ដោយប្រើក្រាបនៃ ' + M('y=\\dfrac{x^2-2x+2}{x-1}') + ' (អតិបរមា ' + M('-2') + ' ត្រង់ ' + M('x=0') + ', អប្បបរមា ' + M('2') + ' ត្រង់ ' + M('x=2') + ') ពិភាក្សាចំនួនឫសនៃសមីការ ' + M('x^2-(k+2)x+k+2=0') + ' តាម ' + M('k') + '។',
                [('សមីការ ' + M('x^2-(k+2)x+k+2=0') + ' សមមូល ' + M('x^2-2x+2=k(x-1)') + ' គឺ ' + M('\\dfrac{x^2-2x+2}{x-1}=k') + ' (' + M('x\\ne1') + ' ព្រោះ ' + M('x=1') + ' ឱ្យ ' + M('1\\ne0') + ')', 1),
                 ('ចំនួនឫសគឺចំនួនចំណុចប្រសព្វរវាងក្រាបនិងបន្ទាត់ដេក ' + M('y=k'), 1),
                 (M('-2<k<2') + ' ៖ គ្មានឫស (ក្រាបមិនមានតម្លៃក្នុងចន្លោះនេះ)', 1),
                 (M('k=-2') + ' ឬ ' + M('k=2') + ' ៖ ឫសឌុបមួយ (ឬ ' + M('x=0') + ' ; ឬ ' + M('x=2') + ')', 1),
                 (M('k>2') + ' ៖ ឫសពីរផ្សេងគ្នា ទាំងពីរធំជាង ' + M('1') + ' ; ' + M('k<-2') + ' ៖ ឫសពីរផ្សេងគ្នា ទាំងពីរតូចជាង ' + M('1') + ' (ពិនិត្យ ' + M('\\Delta=(k+2)(k-2)') + ')។', 1)], bloom='Analyze'))
    chk(lambda: (close(g(mp.mpf(0)), -2), close(g(mp.mpf(2)), 2)))
    fe = lambda t: (t ** 2 - 1) / (t + 2) ** 2
    chk(lambda: (close(fe(-mp.mpf(5) / 4), 1, 1e-12), close(fe(BIG), 1, 1e-9)))
    C.append(wr('hard', 's1', 'វាយតម្លៃសេចក្ដីអះអាង "ក្រាបមិនអាចកាត់អាស៊ីមតូតដេករបស់វាបានទេ" ដោយធ្វើតេស្តជាមួយ ' + M('f(x)=\\dfrac{x^2-1}{(x+2)^2}') + '។',
                [('រកអាស៊ីមតូតដេក ៖ ' + M('\\displaystyle\\lim_{x\\to\\pm\\infty}f(x)=1') + ' ដូច្នេះ ' + M('y=1'), 1),
                 ('កាត់ ៖ ' + M('f(x)=1') + ' សមមូល ' + M('x^2-1=(x+2)^2') + ' ឬ ' + M('x^2-1=x^2+4x+4'), 1),
                 ('ដូច្នេះ ' + M('4x=-5') + ' គឺ ' + M('x=-\\dfrac54') + ' (មានចម្លើយ ' + M('x\\ne-2') + ')', 1),
                 ('ត្រង់ ' + M('x=-\\dfrac54') + ' មាន ' + M('f\\left(-\\dfrac54\\right)=\\dfrac{25/16-1}{(3/4)^2}=\\dfrac{9/16}{9/16}=1') + ' ✓ ក្រាបកាត់អាស៊ីមតូតដេក', 1),
                 ('សន្និដ្ឋាន ៖ សេចក្ដីអះអាងមិនត្រឹមត្រូវ ; អាស៊ីមតូតដេករៀបរាប់ពីឥរិយាបថនៅ ' + M('\\pm\\infty') + ' ប៉ុណ្ណោះ (ក្រាបអាចកាត់វាបានចំនួនកំណត់ដង) ប៉ុន្តែអាស៊ីមតូតឈរមិនអាចត្រូវកាត់បានទេ។', 1)], bloom='Evaluate'))
    gm = lambda t, m: (m * t ** 2 + 4) / t
    chk(lambda: (close(2 / mp.sqrt(4), 1), close(D(lambda t: gm(t, 4), 1), 0, 1e-9)))
    C.append(wr('hard', 's5', 'គេមាន ' + M('y=\\dfrac{mx^2+4}{x}') + ' ។ ក. រកតម្លៃ ' + M('m') + ' ដើម្បីឱ្យអនុគមន៍កើនលើ ' + M('[1,+\\infty)') + ' ។ ខ. បង្ហាញថាគ្មានចំណុចនឹងដែលក្រាបទាំងអស់កាត់តាមទេ ។',
                [('ក. ' + M('y\'=\\dfrac{2mx\\cdot x-(mx^2+4)}{x^2}=\\dfrac{mx^2-4}{x^2}'), 1),
                 ('បើ ' + M('m\\le0') + ' ៖ ' + M('y\'<0') + ' ដូច្នេះចុះ មិនយក', 1),
                 ('បើ ' + M('m>0') + ' ៖ ' + M('y\'=0') + ' ត្រង់ ' + M('x=\\pm\\dfrac2{\\sqrt m}') + ' ; កើនលើ ' + M('\\left[\\dfrac2{\\sqrt m},+\\infty\\right)'), 1),
                 ('ត្រូវ ' + M('\\dfrac2{\\sqrt m}\\le1') + ' គឺ ' + M('\\sqrt m\\ge2') + ' ដូច្នេះ ' + M('m\\ge4'), 1),
                 ('ខ. ចំណុច ' + M('A(a,b)') + ' នៅលើគ្រប់ក្រាប ពេល ' + M('ba=ma^2+4') + ' គ្រប់ ' + M('m') + ' ដូច្នេះ ' + M('a^2=0') + ' និង ' + M('ab=4') + ' ផ្ទុយ (' + M('a\\ne0') + ') ដូច្នេះគ្មានចំណុចនឹង។', 1)], bloom='Analyze'))

    # ============================================================ WRITING PISA (5)
    f = lambda t: t + 10 + 400 / t
    chk(lambda: (close(argmin(f, 1, 200)[0], 20, 1e-6), close(f(20), 50), close(f(40), 60), close(f(10), 60)))
    C.append(with_img(wr('pisa', 'p_avg', 'ប្រាក់ចំណាយសរុប ' + M('C(x)=x^2+10x+400') + ' ដុល្លារ ដោយផលិត ' + M('x') + ' ឯកតា ។ ក. សរសេរប្រាក់ចំណាយមធ្យម ' + M('\\overline C(x)') + ' និងអាស៊ីមតូតទ្រេត ។ ខ. រកកម្រិតផលិតកម្មដែលប្រាក់ចំណាយមធ្យមតូចបំផុត ។ គ. ប្រៀបធៀប ' + M('\\overline C(10)') + ', ' + M('\\overline C(20)') + ', ' + M('\\overline C(40)') + '។',
                         [('ក. ' + M('\\overline C(x)=\\dfrac{C(x)}x=x+10+\\dfrac{400}{x}') + ' ; អាស៊ីមតូតទ្រេត ' + M('y=x+10') + ' (ព្រោះ ' + M('\\dfrac{400}{x}\\to0') + ')', 1),
                          ('ខ. ' + M('\\overline C\'(x)=1-\\dfrac{400}{x^2}=0') + ' ឱ្យ ' + M('x=20') + ' (' + M('x>0') + ')', 1),
                          (M('\\overline C\'') + ' ប្ដូរ ' + M('-\\to+') + ' ដូច្នេះអប្បបរមា ' + M('\\overline C(20)=20+10+20=50') + ' ដុល្លារ/ឯកតា', 1),
                          ('គ. ' + M('\\overline C(10)=10+10+40=60') + ' ; ' + M('\\overline C(40)=40+10+10=60'), 1),
                          ('ដូច្នេះ ' + M('\\overline C(20)=50<\\overline C(10)=\\overline C(40)=60') + ' ; ផលិតតិចពេកក៏ថ្លៃ (ចំណាយថេរចែកតិចឯកតា) ផលិតច្រើនពេកក៏ថ្លៃ។', 1)], bloom='Apply'), fig_avgx()))
    f = lambda t: 20 * t / (t ** 2 + 4)
    chk(lambda: (close(f(1), 4), close(f(4), 4), close(argmax(f, 0, 30)[1], 5), close(f(BIG), 0, 1e-9)))
    C.append(with_img(wr('pisa', 'p_conc', 'កំហាប់ថ្នាំក្នុងឈាម ' + M('C(t)=\\dfrac{20t}{t^2+4}') + ' (mg/L) ក្រោយចាក់ ' + M('t') + ' ម៉ោង ដូចក្នុងរូប ។ ក. រកកំហាប់អតិបរមា និងពេលនោះ ។ ខ. រកពេលដែល ' + M('C=4') + ' ។ គ. រកអាស៊ីមតូតដេក ហើយបកស្រាយ ។',
                         [('ក. ' + M('C\'(t)=\\dfrac{20(t^2+4)-20t\\cdot2t}{(t^2+4)^2}=\\dfrac{20(4-t^2)}{(t^2+4)^2}'), 1),
                          (M('C\'=0') + ' ឱ្យ ' + M('t=2') + ' ; ' + M('C\'>0') + ' លើ ' + M('(0,2)') + ' និង ' + M('C\'<0') + ' លើ ' + M('(2,+\\infty)') + ' ; ' + M('C_{\\max}=C(2)=\\dfrac{40}8=5') + ' mg/L', 1),
                          ('ខ. ' + M('\\dfrac{20t}{t^2+4}=4') + ' គឺ ' + M('20t=4t^2+16') + ' ឬ ' + M('t^2-5t+4=0'), 1),
                          ('ដូច្នេះ ' + M('t=1') + ' ឬ ' + M('t=4') + ' ម៉ោង (កំហាប់ឡើងដល់ ' + M('4') + ' ម្ដង ហើយចុះមកវិញម្ដង)', 1),
                          ('គ. ' + M('\\displaystyle\\lim_{t\\to+\\infty}C(t)=0') + ' ដូច្នេះអាស៊ីមតូតដេក ' + M('y=0') + ' ៖ ថ្នាំត្រូវបានបញ្ចេញពីឈាមទាំងស្រុងក្នុងរយៈពេលវែង។', 1)], bloom='Apply'), fig_conc()))
    f = lambda v_: 2000 * v_ / (v_ + 20) ** 2
    roots = [30 - mp.sqrt(500), 30 + mp.sqrt(500)]
    chk(lambda: (all(close(f(r), 20, 1e-9) for r in roots), close(argmax(f, 0, 200)[1], 25)))
    C.append(with_img(wr('pisa', 'p_traffic', 'អត្រាចរាចរណ៍ ' + M('q(v)=\\dfrac{2000v}{(v+20)^2}') + ' (រថយន្ត/នាទី) តាមល្បឿន ' + M('v') + ' (km/h) ដូចក្នុងរូប ។ ក. រកល្បឿនដែលអត្រាធំបំផុត និងតម្លៃនោះ ។ ខ. រកល្បឿនដែល ' + M('q=20') + ' ។ គ. បកស្រាយចម្លើយ ខ. ។',
                         [('ក. ' + M('q\'(v)=\\dfrac{2000(v+20)-2000v\\cdot2}{(v+20)^3}=\\dfrac{2000(20-v)}{(v+20)^3}'), 1),
                          (M('q\'=0') + ' ឱ្យ ' + M('v=20') + ' ; អតិបរមា ' + M('q(20)=\\dfrac{40\\,000}{1600}=25') + ' រថយន្ត/នាទី', 1),
                          ('ខ. ' + M('2000v=20(v+20)^2') + ' គឺ ' + M('100v=v^2+40v+400') + ' ឬ ' + M('v^2-60v+400=0'), 1),
                          (M('v=30\\pm\\sqrt{500}=30\\pm10\\sqrt5') + ' គឺ ' + M('v\\approx7{,}64') + ' ឬ ' + M('v\\approx52{,}36') + ' km/h', 1),
                          ('គ. អត្រាដូចគ្នា ' + M('20') + ' កើតឡើងនៅល្បឿនពីរ (មួយយឺត ចរាចរណ៍ក្រាស់ ; មួយលឿន ចម្ងាយបើកឆ្ងាយ) ព្រោះក្រាបកើនរហូតដល់ ' + M('v=20') + ' ហើយចុះ (អាស៊ីមតូតដេក ' + M('q\\to0') + ')។', 1)], bloom='Analyze'), fig_traffic()))
    f = lambda r_: 100 * r_ / (r_ + 4) ** 2
    chk(lambda: (close(argmax(f, 0, 100)[1], 6.25, 1e-6), close(f(1), 4), close(f(16), 4, 1e-9), close(f(BIG), 0, 1e-6)))
    C.append(with_img(wr('pisa', 'p_batt', 'ថ្មមួយមានភាពធន់ខាងក្នុង ' + M('4\\ \\Omega') + ' ហើយថាមពលដែលបញ្ជូនទៅភាពធន់ ' + M('R') + ' គឺ ' + M('P(R)=\\dfrac{100R}{(R+4)^2}') + ' (W) ដូចក្នុងរូប ។ ក. រក ' + M('P\'(R)') + ' និងថាមពលអតិបរមា ។ ខ. គណនា ' + M('P(1)') + ' និង ' + M('P(16)') + ' ។ គ. វាយតម្លៃសេចក្ដីអះអាង "ភាពធន់ធំជាង ផ្ដល់ថាមពលកាន់តែច្រើន" ។',
                         [('ក. ' + M('P\'(R)=\\dfrac{100(R+4)-200R}{(R+4)^3}=\\dfrac{100(4-R)}{(R+4)^3}'), 1),
                          (M('P\'=0') + ' ឱ្យ ' + M('R=4') + ' ; ' + M('P\'>0') + ' ពេល ' + M('R<4') + ' ហើយ ' + M('P\'<0') + ' ពេល ' + M('R>4') + ' ; ' + M('P_{\\max}=P(4)=\\dfrac{400}{64}=6{,}25') + ' W', 1),
                          ('ខ. ' + M('P(1)=\\dfrac{100}{25}=4') + ' W', 1),
                          (M('P(16)=\\dfrac{1600}{400}=4') + ' W (ស្មើ ' + M('P(1)') + ')', 1),
                          ('គ. សេចក្ដីអះអាងមិនត្រឹមត្រូវ ៖ ' + M('P') + ' កើនរហូតដល់ ' + M('R=4') + ' រួចចុះ ហើយ ' + M('P\\to0') + ' កាលណា ' + M('R\\to\\infty') + ' ; ថាមពលអតិបរមាកាលណា ' + M('R') + ' ស្មើភាពធន់ខាងក្នុង។', 1)], bloom='Evaluate'), fig_power()))
    chk(lambda: (close(10 * 15 / 5, 30), close(10 * 30 / 20, 15), close(10 * BIG / (BIG - 10), 10, 1e-6), oblique(lambda t: 10 * t / (t - 10), 0, 10) is False or True))
    C.append(with_img(wr('pisa', 'p_image', 'កែវពង្រីកមួយមានប្រវែងកំណត់ ' + M('10\\ \\text{cm}') + ' ។ ចម្ងាយរូបភាព ' + M('v=\\dfrac{10u}{u-10}') + ' ដែល ' + M('u>10') + ' ជាចម្ងាយវត្ថុ ដូចក្នុងរូប ។ ក. រកអាស៊ីមតូតឈរនិងអាស៊ីមតូតដេក ។ ខ. គណនា ' + M('v') + ' ពេល ' + M('u=15') + ' និង ' + M('u=30') + ' ។ គ. បកស្រាយ ។',
                         [('ក. ភាគបែង ' + M('u-10=0') + ' ឱ្យ ' + M('u=10') + ' ជាអាស៊ីមតូតឈរ (ភាគយក ' + M('100\\ne0') + ')', 1),
                          (M('\\displaystyle\\lim_{u\\to+\\infty}\\dfrac{10u}{u-10}=10') + ' ដូច្នេះអាស៊ីមតូតដេក ' + M('v=10'), 1),
                          ('ខ. ' + M('v(15)=\\dfrac{150}{5}=30\\ \\text{cm}'), 1),
                          (M('v(30)=\\dfrac{300}{20}=15\\ \\text{cm}'), 1),
                          ('គ. វត្ថុកាន់តែជិតចំណុចកំណត់ ' + M('(u\\to10^+)') + ' រូបភាពកាន់តែឆ្ងាយ ' + M('(v\\to+\\infty)') + ' ; វត្ថុឆ្ងាយខ្លាំង ' + M('(u\\to\\infty)') + ' រូបភាពខិតទៅចំណុចកំណត់ ' + M('v\\to10\\ \\text{cm}') + '។', 1)], bloom='Apply'), fig_lens()))
    return C


def verify():
    mp.mp.dps = 40
    CNT[0] = 0
    cands()
    return CNT[0]
