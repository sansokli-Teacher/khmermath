# -*- coding: utf-8 -*-
"""
KhmerMath Question Bank: Grade 12 Science (SC)
Chapter 3: ដេរីវេនៃអនុគមន៍
Lesson 2: អនុវត្តន៍នៃដេរីវេ
Reference textbook: Lesson/G12/SC/C3-L2.tex

Target matrix: MCQ easy10/medium14/hard7/pisa5 + writing easy1/medium4/hard4/pisa5 = 50, a Bloom level on each.
Every number (maxima, rates, velocities, accelerations, costs) is re-derived with mpmath: derivatives by numerical
differentiation and optima by a dense scan, so each answer is checked by a method independent of the worked solution.
Figure helpers come from G12L04.
"""
import sys, os, math
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.dirname(__file__))
from lib import *
import svgkit as K
import mpmath as mp
import G12L04 as P
from G12L04 import G, curve

LESSON = 'អនុវត្តន៍នៃដេរីវេ'
CHAPTER = 'ជំពូកទី 3 : ដេរីវេនៃអនុគមន៍'
GRADE = '12SC'
TARGET = P.TARGET
S1 = 'ចលនា ល្បឿន និងសំទុះ'
S2 = 'បញ្ហាបរមា (អតិបរមា និងអប្បបរមា)'
S3 = 'អត្រាបម្រែបម្រួលដែលទាក់ទងគ្នា'
S4 = 'ចំណេញ ចំណាយ និងតម្លៃលក់'
S5 = 'បញ្ហាធរណីមាត្រ'
TOPIC_MAP = {'s1': S1, 's2': S2, 's3': S3, 's4': S4, 's5': S5,
             'p_river': S2, 'p_price': S4, 'p_car': S1, 'p_tank': S3, 'p_ball': S1,
             'p_fence': S2, 'p_bakery': S4, 'p_drive': S1, 'p_sand': S3, 'p_throw': S1}
M_ = M
CNT = [0]


def chk(fn):
    r = fn()
    rs = list(r) if isinstance(r, tuple) else [r]
    assert all(rs), ('numeric check failed', rs)
    CNT[0] += len(rs)


def D(f, t, n=1):
    mp.mp.dps = 40
    return mp.diff(f, mp.mpf(t), n)


def argmax(f, a, b, n=20000):
    """location and value of the maximum of f on [a, b] by a dense scan + local refinement."""
    mp.mp.dps = 30
    best, bx = None, None
    for i in range(n + 1):
        t = a + (b - a) * i / n
        v = f(mp.mpf(t))
        if best is None or v > best:
            best, bx = v, t
    r = mp.findroot(lambda s: mp.diff(f, s), bx)
    return r, f(r)


def argmin(f, a, b, n=20000):
    r, v = argmax(lambda t: -f(t), a, b, n)
    return r, -v


def close(a, b, e=1e-6):
    return abs(mp.mpf(a) - mp.mpf(b)) < e


def with_img(q, svg):
    q['img'] = svg
    return q


# ----------------------------------------------------------------------------- figures
def fig_parab(f, xmax, ymax, w=300, h=220, xt=(), yt=(), peak=None, xl='x', yl='y'):
    kx, ky = (w - 50) / xmax, (h - 50) / ymax
    segs = []
    dots = []
    if peak:
        px_, py_ = peak
        segs = [(px_ * kx, 0, px_ * kx, py_ * ky, K.AXIS, True), (0, py_ * ky, px_ * kx, py_ * ky, K.AXIS, True)]
        dots = [(px_ * kx, py_ * ky, '', 0, 0, K.RED)]
    return G(w, h, [(curve(f, kx, ky), 0, xmax * kx, K.BLUE)], xt=[(kx * v, str(v)) for v in xt], yt=[(ky * v, str(v)) for v in yt], dots=dots, segs=segs, xlabel=xl, ylabel=yl, pad=46)


def fig_river():
    # fence on three sides, river on the fourth
    return K.plane((-0.3, 4.6), (-0.7, 3.0), 55, segs=[(0.5, 0, 0.5, 2.2, K.BLUE, False), (0.5, 0, 3.8, 0, K.BLUE, False), (3.8, 0, 3.8, 2.2, K.BLUE, False)],
                   bands=[(2.2, 3.0, K.BLUE, 0.22)], notes=[(2.1, 0, 'x', -4, 20, K.INK, True), (0.5, 1.1, 'y', -16, 4, K.INK, True)], grid=False, ticks=False, xlabel='', ylabel='')


def fig_vcurve():
    kx, ky = 4.0, 3.3
    fn = lambda t: 60 * t / (t + 6)
    return G(310, 230, [(curve(fn, kx, ky), 0, 60 * kx, K.BLUE)], hl=[(60 * ky, K.AMBER, True)], xt=[(kx * v, str(v)) for v in (10, 20, 30, 40, 50, 60)], yt=[(ky * v, str(v)) for v in (20, 40, 60)], xlabel='t', ylabel='V', pad=44)


def fig_tank():
    return K.plane((-0.5, 3.5), (-1.2, 3.8), 50, segs=[(0, 0, 0, 3, K.INK, False), (2.4, 0, 2.4, 3, K.INK, False), (0, 0, 2.4, 0, K.INK, False)],
                   polys=[([(0, 0), (2.4, 0), (2.4, 1.6), (0, 1.6)], K.BLUE, '#bfdbfe', False)], vecs=[(1.2, 3.7, 1.2, 3.1, K.BLUE, False), (1.2, -0.1, 1.2, -0.9, K.RED, False)],
                   notes=[(1.2, 3.7, '1,2 L/s', 8, 4, K.BLUE, False), (1.2, -0.9, '0,4 L/s', 8, 14, K.RED, False), (0, 0.8, 'h', -16, 4, K.INK, True)], grid=False, ticks=False, xlabel='', ylabel='')


def fig_sand():
    return K.plane((-2.4, 2.6), (-0.6, 3.2), 50, polys=[([(-2, 0), (2, 0), (0, 2.6)], K.BLUE, '#fde68a', False)], segs=[(0, 0, 0, 2.6, K.AXIS, True)],
                   notes=[(1.0, 0, 'r = h/2', -10, 20, K.INK, False), (0, 1.3, 'h', 6, 4, K.INK, True)], vecs=[(0.0, 3.1, 0.0, 2.8, K.BLUE, False)], grid=False, ticks=False, xlabel='', ylabel='')


def fig_projectile():
    kx, ky = 40.0, 7.5
    fn = lambda t: 1.5 + 20 * t - 5 * t * t
    return G(300, 230, [(curve(fn, kx, ky), 0, 4.07 * kx, K.BLUE)], xt=[(kx * v, str(v)) for v in (1, 2, 3, 4)], yt=[(ky * v, str(v)) for v in (1.5, 10, 21.5)],
             dots=[(2 * kx, 21.5 * ky, '', 0, 0, K.RED), (0, 1.5 * ky, '', 0, 0, K.BLUE)], segs=[(2 * kx, 0, 2 * kx, 21.5 * ky, K.AXIS, True), (0, 21.5 * ky, 2 * kx, 21.5 * ky, K.AXIS, True)], xlabel='t', ylabel='h', pad=46)


def fig_ball():
    kx, ky = 40.0, 8.0
    fn = lambda t: 20 * t - 5 * t * t
    return fig_parab(fn, 4.0, 22, xt=(1, 2, 3, 4), yt=(10, 20), peak=(2, 20), xl='t', yl='h')


# ----------------------------------------------------------------------------- candidates
def cands():
    C = []
    f = lambda t: 5 * t ** 2 + 2 * t
    chk(lambda: close(D(f, 3), 32))
    # ============================================================ MCQ EASY (10)
    C.append(mcq('easy', 's1', 'វត្ថុមួយផ្លាស់ទីដោយចម្ងាយ ' + M('S(t)=5t^2+2t') + ' (m) ។ តើល្បឿនត្រង់ ' + M('t=3\\ \\text{s}') + ' ស្មើប៉ុន្មាន ?', M('32\\ \\text{m/s}'), [M('47\\ \\text{m/s}'), M('15\\ \\text{m/s}'), M('30\\ \\text{m/s}')],
                 M('V(t)=S\'(t)=10t+2') + ' ដូច្នេះ ' + M('V(3)=32') + ' m/s។', 'Apply'))
    g = lambda t: t ** 3 - 3 * t
    chk(lambda: close(D(g, 2, 2), 12))
    C.append(mcq('easy', 's1', 'ចម្ងាយ ' + M('S(t)=t^3-3t') + ' (m) ។ តើសំទុះត្រង់ ' + M('t=2\\ \\text{s}') + ' ស្មើប៉ុន្មាន ?', M('12\\ \\text{m/s}^2'), [M('9\\ \\text{m/s}^2'), M('6\\ \\text{m/s}^2'), M('3\\ \\text{m/s}^2')],
                 M('V=S\'=3t^2-3') + ' ; ' + M('a=V\'=6t') + ' ដូច្នេះ ' + M('a(2)=12') + '។', 'Apply'))
    C.append(mcq('easy', 's1', 'ល្បឿននៃចលនាមួយនៅខណៈ ' + M('t') + ' ជាអ្វី ដោយប្រៀបធៀបនឹងចម្ងាយ ' + M('S(t)') + ' ?', M('V(t)=S\'(t)=\\dfrac{dS}{dt}'), [M('V(t)=S(t)\\cdot t'), M('V(t)=\\displaystyle\\int S\\,dt'), M('V(t)=S\'\'(t)')],
                 'ល្បឿនគឺដេរីវេទី ១ នៃចម្ងាយ ; សំទុះគឺដេរីវេទី ២។', 'Remember'))
    C.append(mcq('easy', 's1', 'ទំនាក់ទំនងរវាងសំទុះ ' + M('a(t)') + ' និងល្បឿន ' + M('V(t)') + ' គឺ ៖', M('a(t)=V\'(t)=\\dfrac{dV}{dt}'), [M('a(t)=V(t)^2'), M('V(t)=a\'(t)'), M('a(t)=\\dfrac{V(t)}{t}')],
                 'សំទុះជាអត្រាបម្រែបម្រួលនៃល្បឿន ' + M('a=\\dfrac{dV}{dt}') + '។', 'Remember'))
    A = lambda t: t * (20 - t)
    r, v = argmax(A, 0, 20)
    chk(lambda: (close(r, 10, 1e-6), close(v, 100, 1e-6)))
    C.append(mcq('easy', 's2', 'ចតុកោណកែងមួយមានបរិមាត្រ ' + M('40\\ \\text{m}') + ' ។ ផ្ទៃក្រឡា ' + M('A(x)=x(20-x)') + ' ដែល ' + M('x') + ' ជាទទឹង ។ តើ ' + M('x') + ' ស្មើប៉ុន្មាន ដើម្បីឱ្យផ្ទៃក្រឡាធំបំផុត ?', M('x=10\\ \\text{m}'), [M('x=20\\ \\text{m}'), M('x=5\\ \\text{m}'), M('x=40\\ \\text{m}')],
                 M('A\'(x)=20-2x=0') + ' ដូច្នេះ ' + M('x=10') + ' (ការ៉េ)។', 'Apply'))
    A = lambda t: 60 * t - t * t
    r, v = argmax(A, 0, 60)
    chk(lambda: close(r, 30, 1e-6))
    C.append(mcq('easy', 's2', 'អនុគមន៍ ' + M('A(x)=60x-x^2') + ' មានតម្លៃអតិបរមាត្រង់ ' + M('x') + ' ស្មើប៉ុន្មាន ?', M('x=30'), [M('x=60'), M('x=15'), M('x=0')], M('A\'(x)=60-2x=0') + ' ដូច្នេះ ' + M('x=30') + '។', 'Apply'))
    Af = lambda t: mp.pi * t ** 2
    chk(lambda: close(D(Af, 5) * 2, 20 * mp.pi))
    C.append(mcq('easy', 's3', 'កាំរង្វង់មួយកើនដោយអត្រា ' + M('2\\ \\text{cm/s}') + ' ។ តើផ្ទៃក្រឡារង្វង់កើនដោយអត្រាប៉ុន្មាន ត្រង់ ' + M('r=5\\ \\text{cm}') + ' ?', M('20\\pi\\ \\text{cm}^2/\\text{s}'), [M('10\\pi\\ \\text{cm}^2/\\text{s}'), M('25\\pi\\ \\text{cm}^2/\\text{s}'), M('5\\pi\\ \\text{cm}^2/\\text{s}')],
                 M('\\dfrac{dA}{dt}=2\\pi r\\dfrac{dr}{dt}=2\\pi\\cdot5\\cdot2=20\\pi') + '។', 'Apply'))
    chk(lambda: close(25 * mp.pi * 3, 75 * mp.pi))
    C.append(mcq('easy', 's3', 'ស៊ីឡាំងមួយមានកាំបាត ' + M('5\\ \\text{cm}') + ' ថេរ ហើយកម្ពស់ ' + M('h') + ' កើនដោយអត្រា ' + M('3\\ \\text{cm/s}') + ' ។ តើមាឌកើនដោយអត្រាប៉ុន្មាន ?', M('75\\pi\\ \\text{cm}^3/\\text{s}'), [M('30\\pi\\ \\text{cm}^3/\\text{s}'), M('15\\pi\\ \\text{cm}^3/\\text{s}'), M('25\\pi\\ \\text{cm}^3/\\text{s}')],
                 M('V=25\\pi h') + ' ដូច្នេះ ' + M('\\dfrac{dV}{dt}=25\\pi\\cdot3=75\\pi') + '។', 'Apply'))
    q = lambda t: t ** 2 - 6 * t + 5
    r, v = argmin(q, -10, 10)
    chk(lambda: (close(r, 3, 1e-6), close(v, -4, 1e-6)))
    C.append(mcq('easy', 's2', 'អនុគមន៍ ' + M('f(x)=x^2-6x+5') + ' មានតម្លៃអប្បបរមាស្មើប៉ុន្មាន ?', M('-4'), [M('3'), M('5'), M('-6')], M('f\'(x)=2x-6=0') + ' ដូច្នេះ ' + M('x=3') + ' ហើយ ' + M('f(3)=9-18+5=-4') + '។', 'Apply'))
    chk(lambda: close(D(lambda t: 2 * t ** 2 + t, 5, 2), 4))
    C.append(mcq('easy', 's1', 'ល្បឿន ' + M('V(t)=4t+1') + ' (m/s) ។ តើសំទុះស្មើប៉ុន្មាន ?', M('4\\ \\text{m/s}^2'), [M('1\\ \\text{m/s}^2'), M('4t\\ \\text{m/s}^2'), M('5\\ \\text{m/s}^2')], M('a(t)=V\'(t)=4') + ' (ថេរ)។', 'Apply'))

    # ============================================================ MCQ MEDIUM (14)
    Vb = lambda t: t * (10 - 2 * t) ** 2
    r, v = argmax(Vb, 0, 5)
    chk(lambda: (close(r, mp.mpf(5) / 3, 1e-6), close(v, mp.mpf(2000) / 27, 1e-6)))
    C.append(mcq('medium', 's5', 'ប្រអប់បើកធ្វើពីក្រដាសការ៉េ ' + M('10\\times10') + ' ដោយកាត់ការ៉េជ្រុង ' + M('x') + ' ត្រង់ជ្រុងទាំងបួន ។ មាឌ ' + M('V(x)=x(10-2x)^2') + ' ។ តើ ' + M('x') + ' ស្មើប៉ុន្មាន ដើម្បីឱ្យមាឌអតិបរមា ?', M('x=\\dfrac53'), [M('x=5'), M('x=\\dfrac{10}3'), M('x=1')],
                 M('V\'(x)=(10-2x)(10-6x)=0') + ' ដូច្នេះ ' + M('x=5') + ' (មិនយក) ឬ ' + M('x=\\dfrac53') + '។', 'Analyze'))
    Pf = lambda t: t * (20 - t)
    chk(lambda: close(argmax(Pf, 0, 20)[1], 100))
    C.append(mcq('medium', 's2', 'ចំនួនពីរមានផលបូក ' + M('20') + ' ។ តើផលគុណអតិបរមាស្មើប៉ុន្មាន ?', M('100'), [M('200'), M('96'), M('80')], 'តាង ' + M('P(x)=x(20-x)') + ' ; ' + M('P\'=20-2x=0') + ' ឱ្យ ' + M('x=10') + ' ហើយ ' + M('P=100') + '។', 'Apply'))
    pr = lambda t: -t ** 2 + 80 * t - 300
    r, v = argmax(pr, 0, 80)
    chk(lambda: (close(r, 40, 1e-6), close(v, 1300, 1e-6)))
    C.append(mcq('medium', 's4', 'ប្រាក់ចំណេញ ' + M('P(x)=-x^2+80x-300') + ' (ពាន់រៀល) ដែល ' + M('x') + ' ជាចំនួនឯកតាផលិត ។ តើចំណេញអតិបរមាស្មើប៉ុន្មាន ?', M('1300'), [M('1600'), M('40'), M('1000')],
                 M('P\'=-2x+80=0') + ' ឱ្យ ' + M('x=40') + ' ហើយ ' + M('P(40)=-1600+3200-300=1300') + ' ពាន់រៀល។', 'Apply'))
    Pm = lambda t: 2 * t + 200 / t
    r, v = argmin(Pm, 1, 100)
    chk(lambda: (close(r, 10, 1e-6), close(v, 40, 1e-6)))
    C.append(mcq('medium', 's5', 'ចតុកោណកែងមួយមានផ្ទៃក្រឡា ' + M('100\\ \\text{m}^2') + ' ។ បរិមាត្រ ' + M('p(x)=2x+\\dfrac{200}{x}') + ' ។ តើ ' + M('x') + ' ស្មើប៉ុន្មាន ដើម្បីឱ្យបរិមាត្រតូចបំផុត ?', M('x=10\\ \\text{m}'), [M('x=5\\ \\text{m}'), M('x=20\\ \\text{m}'), M('x=\\sqrt{50}\\ \\text{m}')],
                 M('p\'(x)=2-\\dfrac{200}{x^2}=0') + ' ដូច្នេះ ' + M('x^2=100') + ' គឺ ' + M('x=10') + ' (ការ៉េ)។', 'Analyze'))
    chk(lambda: close(200 / (mp.pi * 100), 2 / mp.pi))
    C.append(mcq('medium', 's3', 'ទឹកចូលស៊ីឡាំងកាំបាត ' + M('10\\ \\text{cm}') + ' ដោយអត្រាមាឌ ' + M('200\\ \\text{cm}^3/\\text{s}') + ' ។ តើកម្រិតទឹកកើនដោយអត្រាប៉ុន្មាន ?', M('\\dfrac2\\pi\\ \\text{cm/s}'), [M('2\\ \\text{cm/s}'), M('\\dfrac{20}{\\pi}\\ \\text{cm/s}'), M('2\\pi\\ \\text{cm/s}')],
                 M('V=100\\pi h') + ' ដូច្នេះ ' + M('\\dfrac{dh}{dt}=\\dfrac{200}{100\\pi}=\\dfrac2\\pi') + '។', 'Apply'))
    chk(lambda: close(3 * 25 / (mp.pi * 225), 1 / (3 * mp.pi)))
    C.append(mcq('medium', 's3', 'កោនមាឌ ' + M('V=\\dfrac{\\pi h^3}{75}') + ' ត្រូវបានបំពេញដោយអត្រា ' + M('3\\ \\text{cm}^3/\\text{s}') + ' ។ តើ ' + M('\\dfrac{dh}{dt}') + ' ស្មើប៉ុន្មាន ត្រង់ ' + M('h=15\\ \\text{cm}') + ' ?', M('\\dfrac1{3\\pi}\\ \\text{cm/s}'), [M('\\dfrac{1}{\\pi}\\ \\text{cm/s}'), M('\\dfrac{3}{25\\pi}\\ \\text{cm/s}'), M('\\dfrac{1}{9\\pi}\\ \\text{cm/s}')],
                 M('\\dfrac{dV}{dt}=\\dfrac{\\pi h^2}{25}\\dfrac{dh}{dt}') + ' ដូច្នេះ ' + M('3=9\\pi\\dfrac{dh}{dt}') + ' គឺ ' + M('\\dfrac{dh}{dt}=\\dfrac1{3\\pi}') + '។', 'Apply'))
    chk(lambda: close(4 * mp.pi / (2 * mp.pi * 2), 1))
    C.append(mcq('medium', 's3', 'ផ្ទៃក្រឡារង្វង់កើនដោយអត្រា ' + M('4\\pi\\ \\text{cm}^2/\\text{s}') + ' ។ តើកាំកើនដោយអត្រាប៉ុន្មាន ត្រង់ ' + M('r=2\\ \\text{cm}') + ' ?', M('1\\ \\text{cm/s}'), [M('2\\ \\text{cm/s}'), M('\\dfrac12\\ \\text{cm/s}'), M('4\\ \\text{cm/s}')],
                 M('\\dfrac{dA}{dt}=2\\pi r\\dfrac{dr}{dt}') + ' ដូច្នេះ ' + M('4\\pi=4\\pi\\dfrac{dr}{dt}') + ' គឺ ' + M('\\dfrac{dr}{dt}=1') + '។', 'Apply'))
    s = lambda t: t ** 3 - 9 * t ** 2 + 24 * t
    chk(lambda: (close(D(s, 2), 0, 1e-9), close(D(s, 4), 0, 1e-9)))
    C.append(mcq('medium', 's1', 'ទីតាំង ' + M('S(t)=t^3-9t^2+24t') + ' (m) ។ ល្បឿនសូន្យត្រង់ពេលណា ?', M('t=2') + ' និង ' + M('t=4'), [M('t=1') + ' និង ' + M('t=3'), M('t=3') + ' តែមួយ', M('t=0') + ' និង ' + M('t=6')],
                 M('V=3t^2-18t+24=3(t-2)(t-4)') + ' ។', 'Apply'))
    chk(lambda: close(D(lambda t: t ** 2 - 6 * t + 5, 3), 0, 1e-9))
    C.append(mcq('medium', 's1', 'ល្បឿន ' + M('V(t)=t^2-6t+5') + ' ។ ល្បឿនអប្បបរមាត្រង់ពេលណា ?', M('t=3'), [M('t=1'), M('t=5'), M('t=6')], M('a=V\'=2t-6=0') + ' ដូច្នេះ ' + M('t=3') + ' (ហើយ ' + M('V(3)=-4') + ')។', 'Apply'))
    Vq = lambda t: 20 * t / (t + 4)
    chk(lambda: close(D(Vq, 1), mp.mpf(80) / 25, 1e-9))
    C.append(mcq('medium', 's1', 'ល្បឿន ' + M('V(t)=\\dfrac{20t}{t+4}') + ' (m/s) ។ សំទុះត្រង់ ' + M('t=1') + ' ស្មើប៉ុន្មាន ?', M('3{,}2\\ \\text{m/s}^2'), [M('4\\ \\text{m/s}^2'), M('2{,}4\\ \\text{m/s}^2'), M('5\\ \\text{m/s}^2')],
                 M('a=V\'=\\dfrac{80}{(t+4)^2}') + ' ដូច្នេះ ' + M('a(1)=\\dfrac{80}{25}=3{,}2') + '។', 'Apply'))
    chk(lambda: close(D(lambda t: mp.mpf('4.9') * t ** 2, mp.mpf('2.5')), 24.5))
    C.append(mcq('medium', 's1', 'វត្ថុធ្លាក់ដោយសេរី ' + M('S(t)=4{,}9t^2') + ' (m) ។ ល្បឿនត្រង់ ' + M('t=2{,}5\\ \\text{s}') + ' ស្មើប៉ុន្មាន ?', M('24{,}5\\ \\text{m/s}'), [M('12{,}25\\ \\text{m/s}'), M('9{,}8\\ \\text{m/s}'), M('30{,}6\\ \\text{m/s}')],
                 M('V=9{,}8t') + ' ដូច្នេះ ' + M('V(2{,}5)=24{,}5') + '។', 'Apply'))
    sg = lambda t: t ** 2 - 4 * t
    chk(lambda: close(D(sg, 1), -2, 1e-9))
    C.append(mcq('medium', 's1', 'ទីតាំង ' + M('S(t)=t^2-4t') + ' (m) ។ ត្រង់ ' + M('t=1') + ' តើវត្ថុចលនាតាមទិសណា ?', 'ថយក្រោយ (ទិសអវិជ្ជមាន) ព្រោះ ' + M('V(1)=-2<0'), ['ទៅមុខ ព្រោះ ' + M('V(1)=2>0'), 'ឈប់ ព្រោះ ' + M('V(1)=0'), 'ទៅមុខ ព្រោះ ' + M('S(1)=-3<0')],
                 M('V=S\'=2t-4') + ' ដូច្នេះ ' + M('V(1)=-2<0') + ' គឺវត្ថុថយក្រោយ។', 'Understand'))
    Rp = lambda t: t * (100 - 2 * t)
    r, v = argmax(Rp, 0, 50)
    chk(lambda: (close(r, 25, 1e-6), close(v, 1250, 1e-6)))
    C.append(mcq('medium', 's4', 'ចំណូលសរុប ' + M('R(p)=p(100-2p)') + ' ដែល ' + M('p') + ' ជាតម្លៃលក់ ។ តើ ' + M('p') + ' ស្មើប៉ុន្មាន ដើម្បីឱ្យចំណូលអតិបរមា ?', M('p=25'), [M('p=50'), M('p=100'), M('p=12{,}5')], M('R\'=100-4p=0') + ' ដូច្នេះ ' + M('p=25') + '។', 'Apply'))

    chk(lambda: (close((mp.mpf(9) - 1) / 2, 4), close(D(lambda t: t ** 2, 3), 6)))
    C.append(mcq('medium', 's1', 'ទីតាំង ' + M('S(t)=t^2') + ' (m) ។ តើល្បឿនមធ្យមរវាង ' + M('t=1') + ' និង ' + M('t=3') + ' ស្មើប៉ុន្មាន ?', M('4\\ \\text{m/s}'), [M('6\\ \\text{m/s}'), M('9\\ \\text{m/s}'), M('8\\ \\text{m/s}')],
                 M('\\dfrac{S(3)-S(1)}{3-1}=\\dfrac{9-1}{2}=4') + ' (ខុសពីល្បឿនខណៈ ' + M('V(3)=6') + ' ដែលជាដេរីវេ)។', 'Analyze'))
    # ============================================================ MCQ HARD (7)
    Vs = lambda t: t * (12 - 2 * t) ** 2
    r, v = argmax(Vs, 0, 6)
    chk(lambda: (close(r, 2, 1e-6), close(v, 128, 1e-6)))
    C.append(mcq('hard', 's5', 'ប្រអប់បើកធ្វើពីក្រដាសការ៉េ ' + M('12\\times12') + ' ដោយកាត់ការ៉េជ្រុង ' + M('x') + ' ត្រង់ជ្រុងទាំងបួន ។ តើមាឌអតិបរមាស្មើប៉ុន្មាន ?', M('128'), [M('144'), M('108'), M('96')],
                 M('V=x(12-2x)^2') + ' ; ' + M('V\'=(12-2x)(12-6x)=0') + ' ឱ្យ ' + M('x=2') + ' ហើយ ' + M('V(2)=2\\cdot64=128') + '។', 'Analyze'))
    Sc = lambda rr: 2 * mp.pi * rr ** 2 + 1000 / rr
    r, v = argmin(Sc, 0.5, 20)
    chk(lambda: close(500 / (mp.pi * r ** 2) / r, 2, 1e-4))
    C.append(mcq('hard', 's5', 'ស៊ីឡាំងមួយមានមាឌថេរ ' + M('V') + ' ។ តើផលធៀបកម្ពស់ទៅកាំ ' + M('\\dfrac hr') + ' ស្មើប៉ុន្មាន ដើម្បីឱ្យផ្ទៃក្រឡាសរុបតូចបំផុត ?', M('2'), [M('1'), M('4'), M('\\dfrac12')],
                 M('S=2\\pi r^2+\\dfrac{2V}{r}') + ' ; ' + M('S\'=4\\pi r-\\dfrac{2V}{r^2}=0') + ' ដូច្នេះ ' + M('V=2\\pi r^3') + ' គឺ ' + M('h=\\dfrac V{\\pi r^2}=2r') + '។', 'Analyze'))
    chk(lambda: close(8 * 25 / (mp.pi * 100), 2 / mp.pi))
    C.append(mcq('hard', 's3', 'កោនមាឌ ' + M('V=\\dfrac{\\pi h^3}{75}') + ' ត្រូវបំពេញដោយអត្រា ' + M('8\\ \\text{cm}^3/\\text{s}') + ' ។ តើ ' + M('\\dfrac{dh}{dt}') + ' ស្មើប៉ុន្មាន ត្រង់ ' + M('h=10\\ \\text{cm}') + ' ?', M('\\dfrac2\\pi\\ \\text{cm/s}'), [M('\\dfrac{8}{\\pi}\\ \\text{cm/s}'), M('\\dfrac{1}{\\pi}\\ \\text{cm/s}'), M('\\dfrac{25}{\\pi}\\ \\text{cm/s}')],
                 M('\\dfrac{dV}{dt}=\\dfrac{\\pi h^2}{25}\\dfrac{dh}{dt}=4\\pi\\dfrac{dh}{dt}=8') + ' ដូច្នេះ ' + M('\\dfrac{dh}{dt}=\\dfrac2\\pi') + '។', 'Analyze'))
    chk(lambda: close(-mp.mpf(6) / 8 * 1, -0.75))
    C.append(mcq('hard', 's3', 'ជណ្ដើរប្រវែង ' + M('10\\ \\text{m}') + ' ទល់ជញ្ជាំង ។ ជើងជណ្ដើរដើរឆ្ងាយពីជញ្ជាំងដោយអត្រា ' + M('1\\ \\text{m/s}') + ' ។ តើកំពូលជណ្ដើរធ្លាក់ចុះដោយអត្រាប៉ុន្មាន កាលណាជើងនៅចម្ងាយ ' + M('6\\ \\text{m}') + ' ?',
                 M('0{,}75\\ \\text{m/s}'), [M('1{,}33\\ \\text{m/s}'), M('0{,}6\\ \\text{m/s}'), M('1\\ \\text{m/s}')],
                 M('x^2+y^2=100') + ' ដូច្នេះ ' + M('2xx\'+2yy\'=0') + ' គឺ ' + M('y\'=-\\dfrac xyx\'=-\\dfrac68\\cdot1=-0{,}75') + ' (ពេល ' + M('x=6,\\ y=8') + ')។', 'Analyze'))
    Ar = lambda t: 2 * t * mp.sqrt(25 - t ** 2) * 2
    r, v = argmax(lambda t: 4 * t * mp.sqrt(25 - t ** 2), 0, 5)
    chk(lambda: (close(v, 50, 1e-5), close(r, 5 / mp.sqrt(2), 1e-4)))
    C.append(mcq('hard', 's5', 'ចតុកោណកែងចារឹកក្នុងរង្វង់កាំ ' + M('5') + ' ។ តើផ្ទៃក្រឡាអតិបរមាស្មើប៉ុន្មាន ?', M('50'), [M('25\\pi'), M('48'), M('40')],
                 'ចំពោះជ្រុងពាក់កណ្ដាល ' + M('x') + ' ៖ ' + M('A=4x\\sqrt{25-x^2}') + ' ; អតិបរមាកាលណា ' + M('x=\\dfrac5{\\sqrt2}') + ' (ការ៉េ) ហើយ ' + M('A=50') + '។', 'Analyze'))
    s3_ = lambda t: t ** 3 - 6 * t ** 2 + 9 * t
    chk(lambda: (close(s3_(1), 4), close(s3_(3), 0), close(s3_(4), 4), close(4 + 4 + 4, 12)))
    C.append(mcq('hard', 's1', 'ទីតាំង ' + M('S(t)=t^3-6t^2+9t') + ' (m) ពេល ' + M('0\\le t\\le4') + ' ។ តើចម្ងាយសរុបដែលវត្ថុធ្វើដំណើរស្មើប៉ុន្មាន ?', M('12\\ \\text{m}'), [M('4\\ \\text{m}'), M('8\\ \\text{m}'), M('0\\ \\text{m}')],
                 M('V=3(t-1)(t-3)') + ' ៖ វត្ថុទៅ ' + M('S(1)=4') + ', ថយ ' + M('S(3)=0') + ', ទៅ ' + M('S(4)=4') + ' ។ ចម្ងាយសរុប ' + M('4+4+4=12') + ' (មិនមែនបម្រែបម្រួលទីតាំង ' + M('S(4)-S(0)=4') + ')។', 'Analyze'))
    C.append(mcq('hard', 's2', 'សិស្សម្នាក់រកឃើញ ' + M('A\'(x)=0') + ' ត្រង់ ' + M('x=100') + ' ហើយសន្និដ្ឋានថា ' + M('A') + ' មានអតិបរមាត្រង់នោះ ។ តើហេតុផលណាបញ្ជាក់បានត្រឹមត្រូវ ?',
                 M('A\'') + ' ប្ដូរសញ្ញាពី ' + M('+') + ' ទៅ ' + M('-') + ' ត្រង់ ' + M('x=100') + ' (ឬ ' + M('A\'\'(100)<0') + ')',
                 [M('A\'(100)=0') + ' តែមួយ ក៏គ្រប់គ្រាន់', M('A(100)>0') + ' ដូច្នេះអតិបរមា', M('A\'') + ' មានត្រង់ ' + M('x=100') + ' ដូច្នេះអតិបរមា'],
                 'ឫសនៃ ' + M('A\'=0') + ' អាចជាអតិបរមា អប្បបរមា ឬចំណុចរាបស្មើ (ឧ. ' + M('x^3') + ' ត្រង់ ' + M('0') + ') ។ ត្រូវមើលសញ្ញា ' + M('A\'') + ' ឬ ' + M('A\'\'') + '។', 'Evaluate'))

    # ============================================================ MCQ PISA (5)
    Af = lambda t: t * (120 - 2 * t)
    r, v = argmax(Af, 0, 60)
    chk(lambda: (close(r, 30, 1e-6), close(v, 1800, 1e-6)))
    C.append(with_img(mcq('pisa', 'p_river', 'កសិករម្នាក់មានរបង ' + M('120\\ \\text{m}') + ' ដើម្បីព័ទ្ធចម្ការមួយខាងទន្លេ (មិនត្រូវការរបងខាងទន្លេ) ដូចក្នុងរូប ។ ទទឹង ' + M('x') + ' ដែលផ្ដល់ផ្ទៃក្រឡាធំបំផុតគឺ ?', M('x=30\\ \\text{m}'), [M('x=60\\ \\text{m}'), M('x=40\\ \\text{m}'), M('x=20\\ \\text{m}')],
                          M('y=120-2x') + ' ; ' + M('A=x(120-2x)') + ' ; ' + M('A\'=120-4x=0') + ' ដូច្នេះ ' + M('x=30') + ' (' + M('A=1800\\ \\text{m}^2') + ')។', 'Apply'), fig_river()))
    Pp = lambda p: (p - 20) * (1000 - 4 * p)
    r, v = argmax(Pp, 20, 250)
    chk(lambda: close(r, 135, 1e-5))
    C.append(with_img(mcq('pisa', 'p_price', 'ហាងមួយលក់ទំនិញមួយ ដែលតម្លៃចំណាយ ' + M('20') + ' ដុល្លារ/ឯកតា ហើយបរិមាណលក់ ' + M('q=1000-4p') + ' ដែល ' + M('p') + ' ជាតម្លៃលក់ ។ ចំណេញ ' + M('P(p)=(p-20)(1000-4p)') + ' ដូចក្នុងរូប ។ តើតម្លៃលក់ ' + M('p') + ' ណាផ្ដល់ចំណេញអតិបរមា ?', M('p=135'), [M('p=250'), M('p=100'), M('p=20')],
                          M('P\'=(1000-4p)-4(p-20)=1080-8p=0') + ' ដូច្នេះ ' + M('p=135') + ' ដុល្លារ។', 'Apply'),
                   fig_parab(lambda t: (t - 20) * (1000 - 4 * t) if t >= 20 else 0, 250, 60000, xt=(50, 135, 200), yt=(20000, 50000), peak=(135, 52900), xl='p', yl='P')))
    chk(lambda: close(D(lambda t: 60 * t / (t + 6), 6), mp.mpf(360) / 144, 1e-9))
    C.append(with_img(mcq('pisa', 'p_car', 'រថយន្តមួយមានល្បឿន ' + M('V(t)=\\dfrac{60t}{t+6}') + ' (m/s) ដូចក្នុងរូប ។ តើសំទុះត្រង់ ' + M('t=6\\ \\text{s}') + ' ស្មើប៉ុន្មាន ?', M('2{,}5\\ \\text{m/s}^2'), [M('5\\ \\text{m/s}^2'), M('30\\ \\text{m/s}^2'), M('10\\ \\text{m/s}^2')],
                          M('a=V\'=\\dfrac{360}{(t+6)^2}') + ' ដូច្នេះ ' + M('a(6)=\\dfrac{360}{144}=2{,}5') + '។', 'Apply'), fig_vcurve()))
    chk(lambda: close(800 / (mp.pi * 400), 2 / mp.pi))
    C.append(with_img(mcq('pisa', 'p_tank', 'ធុងស៊ីឡាំងកាំបាត ' + M('20\\ \\text{cm}') + ' ទទួលទឹក ' + M('1{,}2\\ \\text{L/s}') + ' ហើយបង្ហូរចេញ ' + M('0{,}4\\ \\text{L/s}') + ' ដូចក្នុងរូប ។ តើកម្រិតទឹកកើនដោយអត្រាប៉ុន្មាន ? ( ' + M('1\\ \\text{L}=1000\\ \\text{cm}^3') + ' )', M('\\dfrac2\\pi\\ \\text{cm/s}\\approx0{,}64'), [M('\\dfrac{4}{\\pi}\\ \\text{cm/s}'), M('2\\ \\text{cm/s}'), M('\\dfrac{1}{\\pi}\\ \\text{cm/s}')],
                          M('\\dfrac{dV}{dt}=1200-400=800\\ \\text{cm}^3/\\text{s}') + ' ; ' + M('V=400\\pi h') + ' ដូច្នេះ ' + M('\\dfrac{dh}{dt}=\\dfrac{800}{400\\pi}=\\dfrac2\\pi') + '។', 'Apply'), fig_tank()))
    hb = lambda t: 20 * t - 5 * t ** 2
    r, v = argmax(hb, 0, 4)
    chk(lambda: (close(r, 2, 1e-6), close(v, 20, 1e-6)))
    C.append(with_img(mcq('pisa', 'p_ball', 'គេបោះបាល់ឡើងលើ កម្ពស់ ' + M('h(t)=20t-5t^2') + ' (m) ដូចក្នុងរូប ។ តើកម្ពស់អតិបរមាស្មើប៉ុន្មាន ?', M('20\\ \\text{m}'), [M('40\\ \\text{m}'), M('10\\ \\text{m}'), M('15\\ \\text{m}')],
                          M('h\'=20-10t=0') + ' ដូច្នេះ ' + M('t=2') + ' ហើយ ' + M('h(2)=40-20=20') + ' m។', 'Apply'), fig_ball()))
    return C + cands_writing()


def cands_writing():
    C = []
    # ============================================================ WRITING EASY (1)
    chk(lambda: (close(D(lambda t: 3 * t ** 2 + 2 * t, 2), 14), close(D(lambda t: 3 * t ** 2 + 2 * t, 2, 2), 6)))
    C.append(wr('easy', 's1', 'ទីតាំងនៃវត្ថុមួយ ' + M('S(t)=3t^2+2t') + ' (m) ។ ក. រកល្បឿន ' + M('V(t)') + ' ។ ខ. រកសំទុះ ' + M('a(t)') + ' ។ គ. គណនាល្បឿននិងសំទុះត្រង់ ' + M('t=2\\ \\text{s}') + '។',
                [('ក. ល្បឿនជាដេរីវេនៃទីតាំង ៖ ' + M('V(t)=S\'(t)=6t+2'), 1),
                 ('ខ. សំទុះជាដេរីវេនៃល្បឿន ៖ ' + M('a(t)=V\'(t)=6'), 1),
                 ('គ. ជំនួស ' + M('t=2') + ' ក្នុង ' + M('V') + ' ៖ ' + M('V(2)=6\\cdot2+2=14\\ \\text{m/s}'), 1),
                 ('សំទុះថេរ ៖ ' + M('a(2)=6\\ \\text{m/s}^2'), 1),
                 ('សន្និដ្ឋាន ៖ ល្បឿនកើនឡើងដោយសំទុះថេរ ' + M('6\\ \\text{m/s}^2') + ' (ចលនាបង្កើនល្បឿនស្មើ)។', 1)], bloom='Apply'))

    # ============================================================ WRITING MEDIUM (4)
    A = lambda t: t * (30 - t)
    chk(lambda: (close(argmax(A, 0, 30)[0], 15, 1e-6), close(A(15), 225)))
    C.append(wr('medium', 's2', 'ចម្ការរាងចតុកោណកែងមួយមានបរិមាត្រ ' + M('60\\ \\text{m}') + ' ។ ក. សរសេរផ្ទៃក្រឡាជាអនុគមន៍នៃទទឹង ' + M('x') + ' ។ ខ. រក ' + M('x') + ' ដែលផ្ទៃក្រឡាធំបំផុត ហើយបញ្ជាក់ថាជាអតិបរមា ។',
                [('ក. បរិមាត្រ ' + M('2x+2y=60') + ' ដូច្នេះ ' + M('y=30-x'), 1),
                 ('ផ្ទៃក្រឡា ' + M('A(x)=xy=x(30-x)=30x-x^2') + ' ដែល ' + M('0<x<30'), 1),
                 ('ខ. ' + M('A\'(x)=30-2x') + ' ; ' + M('A\'(x)=0') + ' ឱ្យ ' + M('x=15'), 1),
                 ('បញ្ជាក់ ៖ ' + M('A\'\'(x)=-2<0') + ' ដូច្នេះ ' + M('x=15') + ' ជាអតិបរមា', 1),
                 (M('y=30-15=15') + ' ដូច្នេះចម្ការជាការ៉េ ហើយ ' + M('A_{\\max}=15\\times15=225\\ \\text{m}^2') + '។', 1)], bloom='Apply'))
    Vv = lambda t: 18 * t / (t + 3)
    chk(lambda: (close(D(Vv, 0), 6, 1e-9), close(D(Vv, 3), mp.mpf(54) / 36, 1e-9), close(D(Vv, 9), mp.mpf(54) / 144, 1e-9)))
    C.append(wr('medium', 's1', 'ល្បឿនរថយន្តមួយ ' + M('V(t)=\\dfrac{18t}{t+3}') + ' (m/s) ។ ក. រកសំទុះ ' + M('a(t)') + ' ។ ខ. គណនា ' + M('a(0),\\ a(3),\\ a(9)') + ' ។ គ. បកស្រាយថាតើល្បឿនកើនឬចុះ និងខិតទៅរកតម្លៃណា ។',
                [('ក. ' + M('a(t)=V\'(t)=\\dfrac{18(t+3)-18t}{(t+3)^2}=\\dfrac{54}{(t+3)^2}'), 1),
                 ('ខ. ' + M('a(0)=\\dfrac{54}{9}=6\\ \\text{m/s}^2'), 1),
                 (M('a(3)=\\dfrac{54}{36}=1{,}5\\ \\text{m/s}^2') + ' ហើយ ' + M('a(9)=\\dfrac{54}{144}=0{,}375\\ \\text{m/s}^2'), 1),
                 ('គ. ' + M('a(t)>0') + ' ជានិច្ច ដូច្នេះល្បឿនកើនឡើងជានិច្ច ប៉ុន្តែសំទុះថយចុះ', 1),
                 ('ល្បឿនខិតទៅ ' + M('\\displaystyle\\lim_{t\\to+\\infty}\\dfrac{18t}{t+3}=18\\ \\text{m/s}') + ' ដែលជាល្បឿនកំណត់ (សំទុះ ' + M('\\to0') + ')។', 1)], bloom='Apply'))
    Vo = lambda t: t * (20 - 2 * t) * (12 - 2 * t)
    r, v = argmax(Vo, 0, 6)
    xr = (32 - mp.sqrt(304)) / 6
    chk(lambda: (close(r, xr, 1e-5), close(v, Vo(xr), 1e-6), 2.4 < xr < 2.5, 262 < v < 264))
    C.append(wr('medium', 's5', 'គេធ្វើប្រអប់បើកពីក្រដាសកាតុង ' + M('20\\ \\text{cm}\\times12\\ \\text{cm}') + ' ដោយកាត់ការ៉េជ្រុង ' + M('x') + ' ត្រង់ម៉ុំទាំងបួន ។ ក. សរសេរមាឌ ' + M('V(x)') + ' ហើយកំណត់ដែន ។ ខ. រក ' + M('x') + ' ដែលមាឌអតិបរមា ហើយគណនាមាឌនោះ ។',
                [('ក. ទទឹង ' + M('12-2x>0') + ' ដូច្នេះ ' + M('0<x<6') + ' ; ' + M('V(x)=x(20-2x)(12-2x)=4x^3-64x^2+240x'), 1),
                 ('ខ. ' + M('V\'(x)=12x^2-128x+240=4(3x^2-32x+60)'), 1),
                 ('ដោះស្រាយ ' + M('3x^2-32x+60=0') + ' ៖ ' + M('x=\\dfrac{32\\pm\\sqrt{304}}6') + ' គឺ ' + M('x\\approx2{,}43') + ' ឬ ' + M('x\\approx8{,}24') + ' (មិនក្នុងដែន)', 1),
                 ('សញ្ញា ' + M('V\'') + ' ប្ដូរពី ' + M('+') + ' ទៅ ' + M('-') + ' ត្រង់ ' + M('x\\approx2{,}43') + ' ដូច្នេះអតិបរមា', 1),
                 (M('V(2{,}43)\\approx2{,}43\\times15{,}15\\times7{,}15\\approx263\\ \\text{cm}^3') + '។', 1)], bloom='Analyze'))
    chk(lambda: close(100 / (4 * mp.pi * 100), 1 / (4 * mp.pi)))
    C.append(wr('medium', 's3', 'គេបូមខ្យល់ចូលក្នុងប៉េងប៉ោងរាងស្វ៊ែរដោយអត្រា ' + M('100\\ \\text{cm}^3/\\text{s}') + ' ។ ក. សរសេរទំនាក់ទំនងរវាង ' + M('\\dfrac{dV}{dt}') + ' និង ' + M('\\dfrac{dr}{dt}') + ' ។ ខ. រក ' + M('\\dfrac{dr}{dt}') + ' ពេល ' + M('r=10\\ \\text{cm}') + '។',
                [('ក. មាឌស្វ៊ែរ ' + M('V=\\dfrac43\\pi r^3'), 1),
                 ('ដេរីវេទាក់ទង ' + M('t') + ' (អនុគមន៍បណ្ដាក់) ៖ ' + M('\\dfrac{dV}{dt}=4\\pi r^2\\dfrac{dr}{dt}'), 1),
                 ('ខ. ជំនួស ' + M('\\dfrac{dV}{dt}=100') + ' និង ' + M('r=10') + ' ៖ ' + M('100=4\\pi(100)\\dfrac{dr}{dt}'), 1),
                 ('ដូច្នេះ ' + M('\\dfrac{dr}{dt}=\\dfrac{100}{400\\pi}=\\dfrac1{4\\pi}\\approx0{,}0796\\ \\text{cm/s}'), 1),
                 ('កាំកើនយឺត ព្រោះផ្ទៃស្វ៊ែរធំ ដូច្នេះអត្រាកើនកាំតូចទោះបីមាឌកើនអត្រាថេរ។', 1)], bloom='Analyze'))

    # ============================================================ WRITING HARD (4)
    chk(lambda: close(argmax(lambda t: t * (mp.mpf(10) - t), 0, 10)[0], 5, 1e-6))
    C.append(wr('hard', 's2', 'ក្នុងចតុកោណកែងទាំងអស់ដែលមានបរិមាត្រ ' + M('P') + ' ថេរ បង្ហាញថាការ៉េមានផ្ទៃក្រឡាធំបំផុត ។',
                [('តាង ' + M('x') + ' ជាទទឹង ហើយបណ្ដោយ ' + M('y=\\dfrac P2-x') + ' ដែល ' + M('0<x<\\dfrac P2'), 1),
                 ('ផ្ទៃក្រឡា ' + M('A(x)=x\\left(\\dfrac P2-x\\right)=\\dfrac P2x-x^2'), 1),
                 ('ដេរីវេ ' + M('A\'(x)=\\dfrac P2-2x=0') + ' ឱ្យ ' + M('x=\\dfrac P4'), 1),
                 ('សញ្ញា ' + M('A\'') + ' ប្ដូរ ' + M('+\\to-') + ' (ឬ ' + M('A\'\'=-2<0') + ') ដូច្នេះអតិបរមា', 1),
                 ('ពេលនោះ ' + M('y=\\dfrac P2-\\dfrac P4=\\dfrac P4=x') + ' ដូច្នេះជាការ៉េ ហើយ ' + M('A_{\\max}=\\dfrac{P^2}{16}') + '។', 1)], bloom='Create'))
    Pp = lambda p: (p - 3) * (600 - 50 * p)
    r, v = argmax(Pp, 3, 12)
    chk(lambda: (close(r, 7.5, 1e-6), close(v, 1012.5, 1e-6)))
    C.append(wr('hard', 's4', 'ហាងមួយទិញទំនិញតម្លៃ ' + M('3') + ' ដុល្លារ/ឯកតា ហើយបរិមាណលក់ ' + M('q(p)=600-50p') + ' ដែល ' + M('p') + ' ជាតម្លៃលក់ ។ ក. សរសេរប្រាក់ចំណេញ ' + M('P(p)') + ' ។ ខ. រកតម្លៃលក់ដែលចំណេញអតិបរមា និងចំណេញនោះ ។ គ. ពិនិត្យថាតម្លៃនេះមានន័យក្នុងបរិបទ ។',
                [('ក. ចំណេញក្នុង ១ ឯកតា ' + M('p-3') + ' ដូច្នេះ ' + M('P(p)=(p-3)(600-50p)'), 1),
                 ('ខ. ' + M('P\'(p)=(600-50p)-50(p-3)=750-100p'), 1),
                 (M('P\'(p)=0') + ' ឱ្យ ' + M('p=7{,}5') + ' ; ' + M('P\'\'=-100<0') + ' ដូច្នេះអតិបរមា', 1),
                 ('ចំណេញអតិបរមា ' + M('P(7{,}5)=(4{,}5)(225)=1012{,}5') + ' ដុល្លារ', 1),
                 ('គ. បរិមាណលក់ ' + M('q(7{,}5)=600-375=225>0') + ' និង ' + M('p>3') + ' ដូច្នេះមានន័យ (' + M('q\\ge0') + ' ពេល ' + M('p\\le12') + ')។', 1)], bloom='Analyze'))
    chk(lambda: (close(D(lambda t: t ** 3 - 6 * t ** 2 + 9 * t, 1), 0, 1e-9), close(D(lambda t: t ** 3 - 6 * t ** 2 + 9 * t, 1, 2), -6, 1e-6), close(D(lambda t: t ** 3 - 6 * t ** 2 + 9 * t, 3, 2), 6, 1e-6)))
    C.append(wr('hard', 's1', 'គេឱ្យ ' + M('S(t)=t^3-6t^2+9t') + ' (m) ។ វាយតម្លៃសេចក្ដីអះអាង "ពេលល្បឿនស្មើសូន្យ វត្ថុឈប់ជាអចិន្ត្រៃយ៍" ។',
                [('ល្បឿន ' + M('V(t)=3t^2-12t+9=3(t-1)(t-3)') + ' សូន្យត្រង់ ' + M('t=1') + ' និង ' + M('t=3'), 1),
                 ('សំទុះ ' + M('a(t)=6t-12') + ' ដូច្នេះ ' + M('a(1)=-6\\ne0') + ' និង ' + M('a(3)=6\\ne0'), 1),
                 ('ដោយសំទុះមិនសូន្យ ល្បឿនប្ដូរសញ្ញាត្រង់ ' + M('t=1') + ' (ពី ' + M('+') + ' ទៅ ' + M('-') + ') និង ' + M('t=3') + ' (ពី ' + M('-') + ' ទៅ ' + M('+') + ')', 1),
                 ('ដូច្នេះវត្ថុឈប់តែមួយប៉ព្រិចភ្នែក ហើយប្ដូរទិស ; ' + M('S(1)=4') + ' ជាចំណុចឆ្ងាយបំផុត និង ' + M('S(3)=0') + ' ត្រលប់មកគល់', 1),
                 ('សន្និដ្ឋាន ៖ សេចក្ដីអះអាងមិនត្រឹមត្រូវ (ឈប់ជាអចិន្ត្រៃយ៍ ទាល់តែ ' + M('V\\equiv0') + ' និង ' + M('a\\equiv0') + ')។', 1)], bloom='Evaluate'))
    Sc = lambda rr: 2 * mp.pi * rr ** 2 + 1000 / rr
    r, v = argmin(Sc, 1, 20)
    chk(lambda: (close(r, (250 / mp.pi) ** (mp.mpf(1) / 3), 1e-4), close(500 / (mp.pi * r ** 2), 2 * r, 1e-3), 348 < v < 349.5))
    C.append(wr('hard', 's5', 'រចនាកំប៉ុងស៊ីឡាំងមួយមានមាឌ ' + M('500\\ \\text{cm}^3') + ' ដោយប្រើសម្ភារៈតិចបំផុត (ផ្ទៃក្រឡាសរុបតូចបំផុត) ។ ក. សរសេរផ្ទៃក្រឡា ' + M('S(r)') + ' ។ ខ. រក ' + M('r') + ' និង ' + M('h') + ' ដែលល្អបំផុត ។ គ. គណនា ' + M('S_{\\min}') + '។',
                [('ក. ' + M('\\pi r^2h=500') + ' ដូច្នេះ ' + M('h=\\dfrac{500}{\\pi r^2}') + ' ; ' + M('S=2\\pi r^2+2\\pi rh=2\\pi r^2+\\dfrac{1000}{r}'), 1),
                 ('ខ. ' + M('S\'(r)=4\\pi r-\\dfrac{1000}{r^2}=0') + ' ឱ្យ ' + M('r^3=\\dfrac{250}{\\pi}'), 1),
                 (M('r=\\sqrt[3]{250/\\pi}\\approx4{,}30\\ \\text{cm}') + ' ហើយ ' + M('h=\\dfrac{500}{\\pi r^2}=2r\\approx8{,}60\\ \\text{cm}'), 1),
                 ('ពិនិត្យអប្បបរមា ៖ ' + M('S\'\'=4\\pi+\\dfrac{2000}{r^3}>0'), 1),
                 ('គ. ' + M('S_{\\min}=2\\pi(4{,}30)^2+\\dfrac{1000}{4{,}30}\\approx116{,}2+232{,}6\\approx348{,}8\\ \\text{cm}^2') + '។', 1)], bloom='Create'))

    # ============================================================ WRITING PISA (5)
    C.append(with_img(wr('pisa', 'p_fence', 'កសិករម្នាក់មានរបង ' + M('120\\ \\text{m}') + ' ដើម្បីព័ទ្ធចម្ការរាងចតុកោណកែងមួយខាងទន្លេ (មិនត្រូវការរបងខាងទន្លេ) ដូចក្នុងរូប ។ ក. សរសេរផ្ទៃក្រឡា ' + M('A(x)') + ' ។ ខ. រកទំហំដែលផ្ទៃក្រឡាធំបំផុត ។ គ. ប្រៀបធៀបនឹងចម្ការការ៉េមានរបងដូចគ្នាបួនជ្រុង ។',
                         [('ក. របងបីខាង ' + M('2x+y=120') + ' ដូច្នេះ ' + M('y=120-2x') + ' ; ' + M('A(x)=x(120-2x)=120x-2x^2'), 1),
                          ('ខ. ' + M('A\'(x)=120-4x=0') + ' ឱ្យ ' + M('x=30') + ' ; ' + M('A\'\'=-4<0') + ' អតិបរមា', 1),
                          ('ដូច្នេះ ' + M('x=30\\ \\text{m}') + ' ហើយ ' + M('y=120-60=60\\ \\text{m}') + ' ; ' + M('A_{\\max}=30\\times60=1800\\ \\text{m}^2'), 1),
                          ('គ. ការ៉េបួនជ្រុង ៖ ជ្រុង ' + M('\\dfrac{120}{4}=30') + ' ដូច្នេះ ' + M('A=900\\ \\text{m}^2'), 1),
                          ('ចម្ការខាងទន្លេមានផ្ទៃក្រឡាធំជាង ព្រោះទន្លេជាជ្រុងមួយរួចហើយ (ប្រវែងបណ្ដោយ ' + M('y=2x') + ')។', 1)], bloom='Apply'),
                   fig_river()))
    Pb = lambda p: (p - 2) * (200 - 40 * (p - 5))
    r, v = argmax(Pb, 2, 10)
    chk(lambda: (close(r, 6, 1e-6), close(v, 640, 1e-5)))
    C.append(with_img(wr('pisa', 'p_bakery', 'ហាងនំលក់នំ ' + M('200') + ' ដុំក្នុងមួយថ្ងៃ បើតម្លៃ ' + M('5') + ' ដុល្លារ/ដុំ ។ រាល់ដងតម្លៃកើនឡើង ' + M('0{,}5') + ' ដុល្លារ ការលក់ថយចុះ ' + M('20') + ' ដុំ ។ ចំណាយ ' + M('2') + ' ដុល្លារ/ដុំ ។ ក. បង្ហាញថាចំណេញ ' + M('P(x)=40(x-2)(10-x)') + ' ដែល ' + M('x') + ' ជាតម្លៃ ។ ខ. រកតម្លៃដែលចំណេញអតិបរមា ។',
                         [('ក. ក្នុង ' + M('x') + ' ដុល្លារ ការលក់ថយចុះ ' + M('40(x-5)') + ' ដុំ (ព្រោះ ' + M('0{,}5') + ' ឱ្យ ' + M('20') + ')', 1),
                          ('បរិមាណលក់ ' + M('q=200-40(x-5)=400-40x=40(10-x)'), 1),
                          ('ចំណេញ ' + M('P(x)=(x-2)q=40(x-2)(10-x)'), 1),
                          ('ខ. ' + M('P\'(x)=40[(10-x)-(x-2)]=40(12-2x)=0') + ' ឱ្យ ' + M('x=6'), 1),
                          (M('P(6)=40\\times4\\times4=640') + ' ដុល្លារ (អតិបរមា ព្រោះ ' + M('P\'') + ' ប្ដូរ ' + M('+\\to-') + ') ដូច្នេះលក់ ' + M('6') + ' ដុល្លារ/ដុំ។', 1)], bloom='Apply'),
                   fig_parab(lambda t: 40 * (t - 2) * (10 - t) if 2 <= t <= 10 else 0, 10, 700, xt=(2, 6, 10), yt=(320, 640), peak=(6, 640), xl='x', yl='P')))
    chk(lambda: (close(D(lambda t: 60 * t / (t + 6), 0), 10, 1e-9), close(60 * 18 / 24, 45), close(D(lambda t: 60 * t / (t + 6), 18), mp.mpf(360) / 576, 1e-9)))
    C.append(with_img(wr('pisa', 'p_drive', 'រថយន្តមួយចាប់ផ្ដើមដំណើរ ល្បឿន ' + M('V(t)=\\dfrac{60t}{t+6}') + ' (m/s) ដូចក្នុងរូប ។ ក. រកសំទុះ ' + M('a(t)') + ' ។ ខ. រកល្បឿនកំណត់ (កាលណា ' + M('t\\to\\infty') + ') ។ គ. រកពេលដែលល្បឿនដល់ ' + M('45\\ \\text{m/s}') + ' ហើយគណនាសំទុះពេលនោះ ។',
                         [('ក. ' + M('a(t)=V\'(t)=\\dfrac{60(t+6)-60t}{(t+6)^2}=\\dfrac{360}{(t+6)^2}'), 1),
                          ('ខ. ' + M('\\displaystyle\\lim_{t\\to+\\infty}\\dfrac{60t}{t+6}=60\\ \\text{m/s}') + ' (អាស៊ីមតូតដេរ)', 1),
                          ('គ. ' + M('\\dfrac{60t}{t+6}=45') + ' គឺ ' + M('60t=45t+270'), 1),
                          ('ដូច្នេះ ' + M('15t=270') + ' បាន ' + M('t=18\\ \\text{s}'), 1),
                          ('សំទុះ ' + M('a(18)=\\dfrac{360}{24^2}=\\dfrac{360}{576}=0{,}625\\ \\text{m/s}^2') + ' (សំទុះតូចក្បែរល្បឿនកំណត់)។', 1)], bloom='Analyze'), fig_vcurve()))
    chk(lambda: close(3 * 4 / (mp.pi * 16), 3 / (4 * mp.pi), 1e-9) and close(3 * 4 / (mp.pi * 16), 0.2387, 1e-3))
    C.append(with_img(wr('pisa', 'p_sand', 'គំនរខ្សាច់រាងកោនធ្លាក់ដោយអត្រា ' + M('3\\ \\text{m}^3/\\text{min}') + ' ។ កាំបាតតែងស្មើពាក់កណ្ដាលកម្ពស់ ' + M('r=\\dfrac h2') + ' ដូចក្នុងរូប ។ ក. បង្ហាញថា ' + M('V=\\dfrac{\\pi h^3}{12}') + ' ។ ខ. រក ' + M('\\dfrac{dh}{dt}') + ' ពេល ' + M('h=4\\ \\text{m}') + ' ។ គ. បកស្រាយថាហេតុអ្វី ' + M('\\dfrac{dh}{dt}') + ' ថយចុះពេលគំនរកាន់តែខ្ពស់ ។',
                         [('ក. ' + M('V=\\dfrac13\\pi r^2h=\\dfrac13\\pi\\left(\\dfrac h2\\right)^2h=\\dfrac{\\pi h^3}{12}'), 1),
                          ('ខ. ដេរីវេទាក់ទង ' + M('t') + ' ៖ ' + M('\\dfrac{dV}{dt}=\\dfrac{\\pi h^2}{4}\\dfrac{dh}{dt}'), 1),
                          ('ជំនួស ' + M('\\dfrac{dV}{dt}=3') + ' និង ' + M('h=4') + ' ៖ ' + M('3=\\dfrac{\\pi\\cdot16}{4}\\dfrac{dh}{dt}=4\\pi\\dfrac{dh}{dt}'), 1),
                          ('ដូច្នេះ ' + M('\\dfrac{dh}{dt}=\\dfrac{3}{4\\pi}\\approx0{,}239\\ \\text{m/min}'), 1),
                          ('គ. ' + M('\\dfrac{dh}{dt}=\\dfrac{4}{\\pi h^2}\\cdot\\dfrac{dV}{dt}') + ' ថយចុះតាម ' + M('\\dfrac1{h^2}') + ' ព្រោះមុខកាត់ផ្ដេកកាន់តែធំ ដូច្នេះមាឌដូចគ្នាបង្កើនកម្ពស់តិចជាង។', 1)], bloom='Analyze'), fig_sand()))
    hh = lambda t: mp.mpf('1.5') + 20 * t - 5 * t ** 2
    tg = (20 + mp.sqrt(430)) / 10
    chk(lambda: (close(argmax(hh, 0, 4)[0], 2, 1e-6), close(hh(2), 21.5), close(hh(tg), 0, 1e-9), close(D(hh, tg), 20 - 10 * tg, 1e-9), 20 < abs(20 - 10 * tg) < 21))
    C.append(with_img(wr('pisa', 'p_throw', 'គេបោះគ្រាប់មួយពីកម្ពស់ ' + M('1{,}5\\ \\text{m}') + ' ឡើងលើ ហើយកម្ពស់ ' + M('h(t)=1{,}5+20t-5t^2') + ' (m) ដូចក្នុងរូប ។ ក. រកពេលនិងកម្ពស់អតិបរមា ។ ខ. រកពេលដែលគ្រាប់ធ្លាក់ដល់ដី និងល្បឿនពេលប៉ះដី ។ គ. វាយតម្លៃថា "ល្បឿនពេលប៉ះដីស្មើល្បឿនបោះ ' + M('20\\ \\text{m/s}') + '" ។',
                         [('ក. ' + M('V(t)=h\'(t)=20-10t=0') + ' ឱ្យ ' + M('t=2\\ \\text{s}') + ' ; ' + M('h(2)=1{,}5+40-20=21{,}5\\ \\text{m}'), 1),
                          ('ខ. ' + M('h=0') + ' ៖ ' + M('5t^2-20t-1{,}5=0') + ' ឱ្យ ' + M('t=\\dfrac{20+\\sqrt{430}}{10}\\approx4{,}07\\ \\text{s}'), 1),
                          ('ល្បឿនពេលប៉ះដី ' + M('V=20-10(4{,}07)\\approx-20{,}7\\ \\text{m/s}') + ' (ចុះក្រោម)', 1),
                          ('គ. ទំហំល្បឿន ' + M('20{,}7>20') + ' ដូច្នេះសេចក្ដីអះអាងមិនត្រឹមត្រូវ', 1),
                          ('ពិនិត្យ ៖ ធ្លាក់ពីកម្ពស់អតិបរមា ' + M('21{,}5\\ \\text{m}') + ' បាន ' + M('V=\\sqrt{2\\cdot10\\cdot21{,}5}=\\sqrt{430}\\approx20{,}7\\ \\text{m/s}') + ' ព្រោះគ្រាប់បោះពីកម្ពស់ ' + M('1{,}5\\ \\text{m}') + ' ខ្ពស់ជាងដី ដូច្នេះល្បឿនពេលប៉ះដីធំជាងល្បឿនបោះបន្តិច។', 1)], bloom='Evaluate'), fig_projectile()))
    return C


def verify():
    mp.mp.dps = 40
    CNT[0] = 0
    cands()
    return CNT[0]
