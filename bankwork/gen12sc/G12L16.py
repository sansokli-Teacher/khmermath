# -*- coding: utf-8 -*-
"""
KhmerMath Question Bank: Grade 12 Science (SC)
Chapter 6: អាំងតេក្រាល
Lesson 2: អាំងតេក្រាលកំណត់
Reference textbook: Lesson/G12/SC/C6-L2.tex
Matrix: MCQ easy10/medium14/hard7/pisa5 + writing easy1/medium4/hard4/pisa5 = 50, Bloom on each.
All definite integrals and applications are checked numerically via mpmath.
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.dirname(__file__))
from lib import *
import mpmath as mp
import G12L04 as P

LESSON = 'អាំងតេក្រាលកំណត់'
CHAPTER = 'ជំពូកទី 6 : អាំងតេក្រាល'
GRADE = '12SC'
TARGET = P.TARGET

S1 = 'និយមន័យ និងលក្ខណៈនៃអាំងតេក្រាលកំណត់'
S2 = 'អាំងតេក្រាលកំណត់ដោយប្តូរអថេរ'
S3 = 'អាំងតេក្រាលកំណត់ដោយផ្នែក'
S4 = 'ការអនុវត្តអាំងតេក្រាលកំណត់'
TOPIC_MAP = {'s1': S1, 's2': S2, 's3': S3, 's4': S4,
             'p_pop': S4, 'p_vel': S4, 'p_car': S4, 'p_rev': S4}
CNT = [0]
mp.mp.dps = 30


def chk(fn):
    r = fn()
    rs = list(r) if isinstance(r, tuple) else [r]
    assert all(rs), ('numeric check failed', rs)
    CNT[0] += len(rs)


def with_img(q, svg):
    q['img'] = svg
    return q


def writing(level, sec, stem, ans, sol, bloom=None):
    return wr(level, sec, stem, [(sol, 3), (f'ចម្លើយ៖ {ans}', 2)], bloom=bloom)


def int_ok(f, a, b, val):
    return abs(mp.quad(f, [a, b]) - val) < 1e-8


def svg_area_x2():
    """SVG showing area under y = x^2 from 1 to 3."""
    pts = []
    for i in range(0, 34):
        x = i * 0.1
        y = x * x
        px = 45 + x * 52
        py = 148 - y * 13
        pts.append(f'{px:.1f},{py:.1f}')
    poly = ['97.0,148.0'] + [f'{45 + x*52:.1f},{148 - x*x*13:.1f}' for x in [1 + i*0.1 for i in range(21)]] + ['201.0,148.0']
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 175" width="280" height="175" style="background:#fff;border:1px solid #d1d5db;border-radius:8px">'
        f'<polygon points="{" ".join(poly)}" fill="#dbeafe" stroke="none"/>'
        '<line x1="25" y1="148" x2="255" y2="148" stroke="#64748b" stroke-width="1.3"/>'
        '<line x1="45" y1="162" x2="45" y2="18" stroke="#64748b" stroke-width="1.3"/>'
        f'<polyline fill="none" stroke="#1d4ed8" stroke-width="2.3" points="{" ".join(pts)}"/>'
        '<line x1="97" y1="148" x2="97" y2="135" stroke="#1e40af" stroke-dasharray="4,3"/>'
        '<line x1="201" y1="148" x2="201" y2="31" stroke="#1e40af" stroke-dasharray="4,3"/>'
        '<text x="94" y="162" font-size="11" fill="#334155">1</text>'
        '<text x="198" y="162" font-size="11" fill="#334155">3</text>'
        '<text x="135" y="125" font-size="11.5" fill="#1e40af" font-weight="bold">∫₁³ x² dx</text>'
        '</svg>'
    )


def svg_additivity():
    """SVG showing interval additivity [0, 2] + [2, 4] = [0, 4]."""
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 135" width="280" height="135" style="background:#fff;border:1px solid #d1d5db;border-radius:8px">'
        '<rect x="35" y="38" width="95" height="34" fill="#dbeafe" stroke="#2563eb" stroke-width="1.5"/>'
        '<rect x="130" y="38" width="115" height="34" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/>'
        '<text x="82" y="59" text-anchor="middle" font-size="11.5" fill="#1e40af" font-weight="bold">∫ₐᵇ f(x)dx</text>'
        '<text x="187" y="59" text-anchor="middle" font-size="11.5" fill="#166534" font-weight="bold">∫_b^c f(x)dx</text>'
        '<line x1="35" y1="90" x2="245" y2="90" stroke="#475569" stroke-width="1.6"/>'
        '<circle cx="35" cy="90" r="3.5" fill="#0f172a"/><text x="32" y="108" font-size="11">a</text>'
        '<circle cx="130" cy="90" r="3.5" fill="#0f172a"/><text x="127" y="108" font-size="11">b</text>'
        '<circle cx="245" cy="90" r="3.5" fill="#0f172a"/><text x="242" y="108" font-size="11">c</text>'
        '<text x="140" y="23" text-anchor="middle" font-size="11.5" fill="#0f172a" font-weight="bold">∫ₐᶜ f(x)dx = ∫ₐᵇ f(x)dx + ∫_b^c f(x)dx</text>'
        '</svg>'
    )


def svg_car_profit():
    """SVG showing marginal profit P(x) = 30 - 0.28x from x=10 to 30."""
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 175" width="280" height="175" style="background:#fff;border:1px solid #d1d5db;border-radius:8px">'
        '<polygon points="90,140 90,56 190,74 190,140" fill="#fef3c7" stroke="none"/>'
        '<line x1="25" y1="140" x2="255" y2="140" stroke="#64748b" stroke-width="1.3"/>'
        '<line x1="40" y1="158" x2="40" y2="18" stroke="#64748b" stroke-width="1.3"/>'
        '<line x1="40" y1="47" x2="245" y2="84" stroke="#d97706" stroke-width="2.3"/>'
        '<line x1="90" y1="56" x2="90" y2="140" stroke="#92400e" stroke-dasharray="4,3"/>'
        '<line x1="190" y1="74" x2="190" y2="140" stroke="#92400e" stroke-dasharray="4,3"/>'
        '<text x="84" y="155" font-size="11" fill="#334155">10</text>'
        '<text x="184" y="155" font-size="11" fill="#334155">30</text>'
        '<text x="115" y="112" font-size="11.5" fill="#92400e" font-weight="bold">∫₁₀³⁰ P(x)dx</text>'
        '<text x="125" y="45" font-size="11" fill="#b45309">P(x) = 30 - 0.28x</text>'
        '</svg>'
    )


def svg_velocity_graph():
    """SVG showing V(t) = 5 + 3t^2 from t=3 to t=5."""
    pts = []
    for i in range(0, 56, 2):
        t = i * 0.1
        v = 5 + 3 * t * t
        px = 40 + t * 38
        py = 148 - v * 1.45
        if py >= 18:
            pts.append(f'{px:.1f},{py:.1f}')
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 175" width="280" height="175" style="background:#fff;border:1px solid #d1d5db;border-radius:8px">'
        '<line x1="25" y1="148" x2="255" y2="148" stroke="#64748b" stroke-width="1.3"/>'
        '<line x1="40" y1="160" x2="40" y2="18" stroke="#64748b" stroke-width="1.3"/>'
        f'<polyline fill="none" stroke="#0f766e" stroke-width="2.4" points="{" ".join(pts)}"/>'
        '<line x1="154" y1="148" x2="154" y2="101.6" stroke="#0f766e" stroke-dasharray="4,3"/>'
        '<line x1="230" y1="148" x2="230" y2="32" stroke="#0f766e" stroke-dasharray="4,3"/>'
        '<text x="150" y="162" font-size="11" fill="#334155">3</text>'
        '<text x="226" y="162" font-size="11" fill="#334155">5</text>'
        '<text x="110" y="42" font-size="11.5" fill="#0f766e" font-weight="bold">V(t) = 5 + 3t²</text>'
        '</svg>'
    )


def cands():
    qs = []
    # =========================================================================
    # MCQ EASY (10)
    # =========================================================================
    qs.append(mcq('easy', 's1',
        r'បើ $F(x)$ ជាព្រីមីទីវនៃ $f(x)$ លើ $[a, b]$ តើ $\int_{a}^{b} f(x)\,dx$ ស្មើនឹងអ្វី?',
        r'$F(b) - F(a)$',
        [r'$F(a) - F(b)$', r'$F(b) + F(a)$', r'$F\'(b) - F\'(a)$'],
        r'តាមនិយមន័យ $\int_{a}^{b} f(x)\,dx = [F(x)]_{a}^{b} = F(b) - F(a)$ ។',
        bloom='Remember'))

    chk(lambda: int_ok(lambda x: x**2, 1, 3, mp.mpf(26)/3))
    qs.append(with_img(mcq('easy', 's1',
        r'គណនាអាំងតេក្រាលកំណត់ $\int_{1}^{3} x^{2}\,dx$ ៖',
        r'$\frac{26}{3}$',
        [r'$\frac{27}{3}$', r'$\frac{25}{3}$', r'$8$'],
        r'$\left[\frac{1}{3}x^{3}\right]_{1}^{3} = 9 - \frac{1}{3} = \frac{26}{3}$ ។',
        bloom='Apply'), svg_area_x2()))

    chk(lambda: int_ok(lambda x: 4*x**3, -2, 1, -15))
    qs.append(mcq('easy', 's1',
        r'គណនាអាំងតេក្រាលកំណត់ $\int_{-2}^{1} 4x^{3}\,dx$ ៖',
        r'$-15$',
        [r'$15$', r'$-17$', r'$17$'],
        r'$[x^{4}]_{-2}^{1} = 1^{4} - (-2)^{4} = 1 - 16 = -15$ ។',
        bloom='Apply'))

    chk(lambda: int_ok(lambda x: mp.exp(x), 10, 10, 0))
    qs.append(mcq('easy', 's1',
        r'គណនាអាំងតេក្រាលកំណត់ $\int_{10}^{10} e^{x}\,dx$ ៖',
        r'$0$',
        [r'$e^{10}$', r'$2e^{10}$', r'$1$'],
        r'តាមលក្ខណៈ $\int_{a}^{a} f(x)\,dx = 0$ ។',
        bloom='Understand'))

    qs.append(mcq('easy', 's1',
        r'ចំពោះអនុគមន៍ជាប់ $f$ លើ $[a, b]$ តើ $\int_{a}^{b} f(x)\,dx + \int_{b}^{a} f(x)\,dx$ ស្មើនឹងអ្វី?',
        r'$0$',
        [r'$2\int_{a}^{b} f(x)\,dx$', r'$1$', r'$F(b) + F(a)$'],
        r'ព្រោះ $\int_{b}^{a} f(x)\,dx = -\int_{a}^{b} f(x)\,dx$ នោះផលបូកស្មើ $0$ ។',
        bloom='Understand'))

    chk(lambda: int_ok(lambda x: 3*x**2 + 1, 1, 4, 66))
    qs.append(mcq('easy', 's1',
        r'គណនាអាំងតេក្រាលកំណត់ $\int_{1}^{4} (3x^{2} + 1)\,dx$ ៖',
        r'$66$',
        [r'$63$', r'$67$', r'$64$'],
        r'$[x^{3} + x]_{1}^{4} = (64 + 4) - (1 + 1) = 66$ ។',
        bloom='Apply'))

    chk(lambda: int_ok(lambda x: 2/mp.sqrt(x), 4, 9, 4))
    qs.append(mcq('easy', 's1',
        r'គណនាអាំងតេក្រាលកំណត់ $\int_{4}^{9} \frac{2}{\sqrt{x}}\,dx$ ៖',
        r'$4$',
        [r'$2$', r'$6$', r'$8$'],
        r'$[4\sqrt{x}]_{4}^{9} = 4(3) - 4(2) = 4$ ។',
        bloom='Apply'))

    chk(lambda: int_ok(lambda x: 3*mp.sin(x), 0, mp.pi/3, mp.mpf(3)/2))
    qs.append(mcq('easy', 's1',
        r'គណនាអាំងតេក្រាលកំណត់ $\int_{0}^{\frac{\pi}{3}} 3\sin x\,dx$ ៖',
        r'$\frac{3}{2}$',
        [r'$\frac{3\sqrt{3}}{2}$', r'$-\frac{3}{2}$', r'$3$'],
        r'$[-3\cos x]_{0}^{\frac{\pi}{3}} = -3\left(\frac{1}{2}\right) + 3(1) = \frac{3}{2}$ ។',
        bloom='Apply'))

    chk(lambda: int_ok(lambda x: 4*x - 5, 2, 4, 14) and int_ok(lambda x: 5 - 6*x, 2, 4, -26))
    qs.append(mcq('easy', 's1',
        r'គណនា $\int_{2}^{4} (4x - 5)\,dx + \int_{2}^{4} (5 - 6x)\,dx$ ៖',
        r'$-12$',
        [r'$12$', r'$-16$', r'$0$'],
        r'$\int_{2}^{4} [(4x-5)+(5-6x)]dx = \int_{2}^{4} (-2x)\,dx = [-x^{2}]_{2}^{4} = -16 + 4 = -12$ ។',
        bloom='Apply'))

    chk(lambda: int_ok(lambda x: (3*x**2 - 2*x)**2, 0, 1, mp.mpf(2)/15))
    qs.append(mcq('easy', 's1',
        r'គណនាអាំងតេក្រាលកំណត់ $\int_{0}^{1} (3x^{2} - 2x)^{2}\,dx$ ៖',
        r'$\frac{2}{15}$',
        [r'$\frac{1}{15}$', r'$\frac{4}{15}$', r'$\frac{1}{3}$'],
        r'$(3x^{2}-2x)^{2} = 9x^{4} - 12x^{3} + 4x^{2}$ ។ អាំងតេក្រាលលើ $[0,1]$ គឺ $\frac{9}{5} - 3 + \frac{4}{3} = \frac{2}{15}$ ។',
        bloom='Apply'))

    # =========================================================================
    # MCQ MEDIUM (14)
    # =========================================================================
    chk(lambda: int_ok(lambda x: 2*x**2 - 4*x + 5, 1, 4, 27))
    qs.append(mcq('medium', 's1',
        r'គណនាអាំងតេក្រាលកំណត់ $\int_{1}^{4} (2x^{2} - 4x + 5)\,dx$ ៖',
        r'$27$',
        [r'$25$', r'$29$', r'$24$'],
        r'$\left[\frac{2}{3}x^{3} - 2x^{2} + 5x\right]_{1}^{4} = \left(\frac{128}{3}-32+20\right) - \left(\frac{2}{3}-2+5\right) = 27$ ។',
        bloom='Apply'))

    chk(lambda: int_ok(lambda x: x**2 + 1/x - mp.exp(x), 1, 3, mp.mpf(26)/3 + mp.log(3) - mp.exp(3) + mp.e))
    qs.append(mcq('medium', 's1',
        r'គណនាអាំងតេក្រាលកំណត់ $\int_{1}^{3} \left(x^{2} + \frac{1}{x} - e^{x}\right)dx$ ៖',
        r'$\frac{26}{3} + \ln 3 - e^{3} + e$',
        [r'$\frac{26}{3} + \ln 3 - e^{3} - e$', r'$\frac{28}{3} + \ln 3 - e^{3} + e$', r'$\frac{26}{3} - \ln 3 - e^{3} + e$'],
        r'$\left[\frac{x^{3}}{3} + \ln x - e^{x}\right]_{1}^{3} = \left(9 + \ln 3 - e^{3}\right) - \left(\frac{1}{3} + 0 - e\right) = \frac{26}{3} + \ln 3 - e^{3} + e$ ។',
        bloom='Apply'))

    chk(lambda: int_ok(lambda x: -3*x**5 - 3*x**2 + 2*x + 5, 1, 0, mp.mpf(-9)/2))
    qs.append(mcq('medium', 's1',
        r'គណនាអាំងតេក្រាលកំណត់ $\int_{1}^{0} (-3x^{5} - 3x^{2} + 2x + 5)\,dx$ ៖',
        r'$-\frac{9}{2}$',
        [r'$\frac{9}{2}$', r'$-\frac{11}{2}$', r'$-\frac{7}{2}$'],
        r'$\left[-\frac{1}{2}x^{6} - x^{3} + x^{2} + 5x\right]_{1}^{0} = 0 - \left(-\frac{1}{2}-1+1+5\right) = -\frac{9}{2}$ ។',
        bloom='Apply'))

    qs.append(with_img(mcq('medium', 's1',
        r'គេឱ្យ $\int_{1}^{2} f(x)\,dx = -4$ និង $\int_{1}^{5} f(x)\,dx = 6$ ។ គណនា $\int_{2}^{5} f(x)\,dx$ ៖',
        r'$10$',
        [r'$2$', r'$-10$', r'$-2$'],
        r'$\int_{2}^{5} f(x)\,dx = \int_{1}^{5} f(x)\,dx - \int_{1}^{2} f(x)\,dx = 6 - (-4) = 10$ ។',
        bloom='Apply'), svg_additivity()))

    chk(lambda: int_ok(lambda x: 3/x**2 + x/2, 2, 4, mp.mpf(15)/4))
    qs.append(mcq('medium', 's1',
        r'គណនាអាំងតេក្រាលកំណត់ $\int_{2}^{4} \left(\frac{3}{x^{2}} + \frac{1}{2}x\right)dx$ ៖',
        r'$\frac{15}{4}$',
        [r'$\frac{13}{4}$', r'$\frac{17}{4}$', r'$\frac{9}{4}$'],
        r'$\left[-\frac{3}{x} + \frac{1}{4}x^{2}\right]_{2}^{4} = \left(-\frac{3}{4} + 4\right) - \left(-\frac{3}{2} + 1\right) = \frac{15}{4}$ ។',
        bloom='Apply'))

    chk(lambda: int_ok(lambda x: x*(x**2+1)**3, 0, 2, 78))
    qs.append(mcq('medium', 's2',
        r'ដោយប្រើអថេរជំនួស គណនា $\int_{0}^{2} x(x^{2} + 1)^{3}\,dx$ ៖',
        r'$78$',
        [r'$156$', r'$39$', r'$77$'],
        r'តាង $u = x^{2} + 1$ ($x=0 \Rightarrow u=1, x=2 \Rightarrow u=5$) បាន $\frac{1}{2}\int_{1}^{5} u^{3}du = \frac{625-1}{8} = 78$ ។',
        bloom='Apply'))

    chk(lambda: int_ok(lambda x: 3*x**2/(x**3+1)**2, 1, 2, mp.mpf(7)/18))
    qs.append(mcq('medium', 's2',
        r'គណនាអាំងតេក្រាលកំណត់ $\int_{1}^{2} \frac{3x^{2}}{(x^{3} + 1)^{2}}\,dx$ ៖',
        r'$\frac{7}{18}$',
        [r'$\frac{11}{18}$', r'$\frac{7}{9}$', r'$-\frac{7}{18}$'],
        r'តាង $u = x^{3} + 1$ បាន $\int_{2}^{9} \frac{1}{u^{2}}du = \left[-\frac{1}{u}\right]_{2}^{9} = \frac{1}{2} - \frac{1}{9} = \frac{7}{18}$ ។',
        bloom='Apply'))

    chk(lambda: int_ok(lambda x: mp.exp(mp.sqrt(x))/mp.sqrt(x), 1, 4, 2*(mp.exp(2) - mp.e)))
    qs.append(mcq('medium', 's2',
        r'គណនាអាំងតេក្រាលកំណត់ $\int_{1}^{4} \frac{e^{\sqrt{x}}}{\sqrt{x}}\,dx$ ៖',
        r'$2(e^{2} - e)$',
        [r'$e^{2} - e$', r'$2(e^{4} - e)$', r'$\frac{1}{2}(e^{2} - e)$'],
        r'តាង $u = \sqrt{x} \implies du = \frac{dx}{2\sqrt{x}}$ បាន $2\int_{1}^{2} e^{u}du = 2(e^{2} - e)$ ។',
        bloom='Apply'))

    chk(lambda: int_ok(lambda x: x*mp.cos(x), 0, mp.pi/2, mp.pi/2 - 1))
    qs.append(mcq('medium', 's3',
        r'ដោយប្រើអាំងតេក្រាលដោយផ្នែក គណនា $\int_{0}^{\frac{\pi}{2}} x\cos x\,dx$ ៖',
        r'$\frac{\pi}{2} - 1$',
        [r'$\frac{\pi}{2} + 1$', r'$1 - \frac{\pi}{2}$', r'$\frac{\pi}{2}$'],
        r'$[x\sin x]_{0}^{\frac{\pi}{2}} - \int_{0}^{\frac{\pi}{2}} \sin x\,dx = \frac{\pi}{2} + [\cos x]_{0}^{\frac{\pi}{2}} = \frac{\pi}{2} - 1$ ។',
        bloom='Apply'))

    chk(lambda: int_ok(lambda x: x*mp.exp(x), 0, 1, 1))
    qs.append(mcq('medium', 's3',
        r'គណនាអាំងតេក្រាលកំណត់ $\int_{0}^{1} xe^{x}\,dx$ ៖',
        r'$1$',
        [r'$e - 1$', r'$e$', r'$2$'],
        r'$[xe^{x}]_{0}^{1} - \int_{0}^{1} e^{x}dx = e - (e - 1) = 1$ ។',
        bloom='Apply'))

    chk(lambda: int_ok(lambda x: x*mp.log(x), 1, mp.e, (mp.e**2 + 1)/4))
    qs.append(mcq('medium', 's3',
        r'គណនាអាំងតេក្រាលកំណត់ $\int_{1}^{e} x\ln x\,dx$ ៖',
        r'$\frac{e^{2} + 1}{4}$',
        [r'$\frac{e^{2} - 1}{4}$', r'$\frac{e^{2} + 1}{2}$', r'$\frac{e^{2}}{4}$'],
        r'តាង $u = \ln x, dv = x\,dx$ បាន $\left[\frac{x^{2}}{2}\ln x\right]_{1}^{e} - \int_{1}^{e} \frac{x}{2}dx = \frac{e^{2}}{2} - \frac{e^{2}-1}{4} = \frac{e^{2}+1}{4}$ ។',
        bloom='Apply'))

    chk(lambda: int_ok(lambda x: 2*x**2/(1+2*x**3), 0, 1, mp.log(3)/3))
    qs.append(mcq('medium', 's2',
        r'គណនាអាំងតេក្រាលកំណត់ $\int_{0}^{1} \frac{2x^{2}}{1 + 2x^{3}}\,dx$ ៖',
        r'$\frac{1}{3}\ln 3$',
        [r'$\ln 3$', r'$\frac{2}{3}\ln 3$', r'$\frac{1}{6}\ln 3$'],
        r'តាង $u = 1 + 2x^{3} \implies du = 6x^{2}dx$ បាន $\frac{1}{3}\int_{1}^{3} \frac{du}{u} = \frac{1}{3}\ln 3$ ។',
        bloom='Apply'))

    chk(lambda: int_ok(lambda x: mp.log(x)**2/x, 1, mp.e, mp.mpf(1)/3))
    qs.append(mcq('medium', 's2',
        r'គណនាអាំងតេក្រាលកំណត់ $\int_{1}^{e} \frac{(\ln x)^{2}}{x}\,dx$ ៖',
        r'$\frac{1}{3}$',
        [r'$1$', r'$\frac{1}{2}$', r'$\frac{e}{3}$'],
        r'តាង $u = \ln x \implies du = \frac{dx}{x}$ បាន $\int_{0}^{1} u^{2}du = \frac{1}{3}$ ។',
        bloom='Apply'))

    chk(lambda: int_ok(lambda x: mp.tan(x), 0, mp.pi/3, mp.log(2)))
    qs.append(mcq('medium', 's2',
        r'គណនាអាំងតេក្រាលកំណត់ $\int_{0}^{\frac{\pi}{3}} \tan x\,dx$ ៖',
        r'$\ln 2$',
        [r'$\ln 3$', r'$\frac{1}{2}\ln 2$', r'$-\ln 2$'],
        r'$\int_{0}^{\frac{\pi}{3}} \frac{\sin x}{\cos x}dx = [-\ln|\cos x|]_{0}^{\frac{\pi}{3}} = -\ln\frac{1}{2} + \ln 1 = \ln 2$ ។',
        bloom='Apply'))

    # =========================================================================
    # MCQ HARD (7)
    # =========================================================================
    chk(lambda: int_ok(lambda x: (x+1)/(x**2+2*x+2)**3, 0, 4, mp.mpf(21)/338))
    qs.append(mcq('hard', 's2',
        r'គណនាអាំងតេក្រាលកំណត់ $\int_{0}^{4} \frac{x + 1}{(x^{2} + 2x + 2)^{3}}\,dx$ ៖',
        r'$\frac{21}{338}$',
        [r'$\frac{21}{676}$', r'$\frac{11}{338}$', r'$\frac{21}{169}$'],
        r'តាង $u = x^{2}+2x+2$ ($u(0)=2, u(4)=26$) បាន $\frac{1}{2}\int_{2}^{26} u^{-3}du = \frac{1}{4}\left(\frac{1}{4} - \frac{1}{676}\right) = \frac{21}{338}$ ។',
        bloom='Analyze'))

    chk(lambda: int_ok(lambda x: x*mp.exp(2*x), 0, 2, (3*mp.exp(4) + 1)/4))
    qs.append(mcq('hard', 's3',
        r'គណនាអាំងតេក្រាលកំណត់ $\int_{0}^{2} xe^{2x}\,dx$ ៖',
        r'$\frac{3e^{4} + 1}{4}$',
        [r'$\frac{3e^{4} - 1}{4}$', r'$\frac{4e^{4} + 1}{4}$', r'$\frac{3e^{4} + 1}{2}$'],
        r'$\left[\frac{1}{2}xe^{2x} - \frac{1}{4}e^{2x}\right]_{0}^{2} = \left(e^{4} - \frac{1}{4}e^{4}\right) - \left(0 - \frac{1}{4}\right) = \frac{3e^{4}+1}{4}$ ។',
        bloom='Analyze'))

    chk(lambda: int_ok(lambda x: x*mp.sin(x), 0, mp.pi/3, -mp.pi/6 + mp.sqrt(3)/2))
    qs.append(mcq('hard', 's3',
        r'គណនាអាំងតេក្រាលកំណត់ $\int_{0}^{\frac{\pi}{3}} x\sin x\,dx$ ៖',
        r'$-\frac{\pi}{6} + \frac{\sqrt{3}}{2}$',
        [r'$\frac{\pi}{6} + \frac{\sqrt{3}}{2}$', r'$-\frac{\pi}{3} + \frac{\sqrt{3}}{2}$', r'$-\frac{\pi}{6} + \frac{1}{2}$'],
        r'$[-x\cos x + \sin x]_{0}^{\frac{\pi}{3}} = -\frac{\pi}{3}\left(\frac{1}{2}\right) + \frac{\sqrt{3}}{2} = -\frac{\pi}{6} + \frac{\sqrt{3}}{2}$ ។',
        bloom='Analyze'))

    chk(lambda: int_ok(lambda x: 5*x*(x**2-7)**3, 1, 3, -800))
    qs.append(mcq('hard', 's2',
        r'គណនាអាំងតេក្រាលកំណត់ $\int_{1}^{3} 5x(x^{2} - 7)^{3}\,dx$ ៖',
        r'$-800$',
        [r'$800$', r'$-1600$', r'$-400$'],
        r'តាង $u = x^{2} - 7$ ($x=1 \Rightarrow u=-6, x=3 \Rightarrow u=2$) បាន $\frac{5}{2}\int_{-6}^{2} u^{3}du = \frac{5}{8}(16 - 1296) = -800$ ។',
        bloom='Analyze'))

    chk(lambda: int_ok(lambda x: mp.exp(x)/(4*mp.exp(x)-2), 0, mp.log(2), mp.log(3)/4))
    qs.append(mcq('hard', 's2',
        r'គណនាអាំងតេក្រាលកំណត់ $\int_{0}^{\ln 2} \frac{e^{x}}{4e^{x} - 2}\,dx$ ៖',
        r'$\frac{1}{4}\ln 3$',
        [r'$\frac{1}{4}\ln 2$', r'$\ln 3$', r'$\frac{1}{2}\ln 3$'],
        r'តាង $u = 4e^{x} - 2$ ($x=0 \Rightarrow u=2, x=\ln 2 \Rightarrow u=6$) បាន $\frac{1}{4}\int_{2}^{6} \frac{du}{u} = \frac{1}{4}\ln\frac{6}{2} = \frac{1}{4}\ln 3$ ។',
        bloom='Analyze'))

    chk(lambda: int_ok(lambda x: (1+mp.log(x))**2/(2*x), 1, mp.e, mp.mpf(7)/6))
    qs.append(mcq('hard', 's2',
        r'គណនាអាំងតេក្រាលកំណត់ $\int_{1}^{e} \frac{(1 + \ln x)^{2}}{2x}\,dx$ ៖',
        r'$\frac{7}{6}$',
        [r'$\frac{8}{6}$', r'$\frac{7}{3}$', r'$\frac{5}{6}$'],
        r'តាង $u = 1 + \ln x$ ($x=1 \Rightarrow u=1, x=e \Rightarrow u=2$) បាន $\frac{1}{2}\int_{1}^{2} u^{2}du = \frac{8 - 1}{6} = \frac{7}{6}$ ។',
        bloom='Analyze'))

    chk(lambda: int_ok(lambda x: 1/(x*mp.log(x)), mp.e, mp.e**2, mp.log(2)))
    qs.append(mcq('hard', 's2',
        r'គណនាអាំងតេក្រាលកំណត់ $\int_{e}^{e^{2}} \frac{1}{x\ln x}\,dx$ ៖',
        r'$\ln 2$',
        [r'$1$', r'$2$', r'$e$'],
        r'តាង $u = \ln x$ ($x=e \Rightarrow u=1, x=e^{2} \Rightarrow u=2$) បាន $\int_{1}^{2} \frac{du}{u} = \ln 2$ ។',
        bloom='Analyze'))

    # =========================================================================
    # MCQ PISA (5)
    # =========================================================================
    chk(lambda: int_ok(lambda x: 5 + 3*x, 0, 8, 136))
    qs.append(mcq('pisa', 'p_pop',
        r'ប្រជាជនក្នុងសហគមន៍មួយកើនឡើងតាមអត្រា $t(x) = 5 + 3x$ នាក់/ឆ្នាំ ($x$ ជាចំនួនឆ្នាំ) ។ រកកំណើនប្រជាជនសរុបក្នុងរយៈពេល $8$ ឆ្នាំខាងមុខ ៖',
        r'$136$ នាក់',
        [r'$120$ នាក់', r'$96$ នាក់', r'$144$ នាក់'],
        r'$\int_{0}^{8} (5 + 3x)\,dx = \left[5x + \frac{3}{2}x^{2}\right]_{0}^{8} = 40 + 96 = 136$ នាក់ ។',
        bloom='Apply'))

    chk(lambda: int_ok(lambda t: 5 + 3*t**2, 3, 5, 108))
    qs.append(with_img(mcq('pisa', 'p_vel',
        r'វត្ថុមួយផ្លាស់ទីតាមទិសដេកដោយល្បឿន $V(t) = 5 + 3t^{2}\text{ (m/mn)}$ ។ រកកំណើនចម្ងាយចរពីខណៈ $t = 3\text{ mn}$ ដល់ $t = 5\text{ mn}$ ៖',
        r'$108\text{ m}$',
        [r'$150\text{ m}$', r'$42\text{ m}$', r'$118\text{ m}$'],
        r'$\int_{3}^{5} (5 + 3t^{2})\,dt = [5t + t^{3}]_{3}^{5} = 150 - 42 = 108\text{ m}$ ។',
        bloom='Apply'), svg_velocity_graph()))

    chk(lambda: int_ok(lambda x: 30 - 0.28*x, 10, 30, 488))
    qs.append(with_img(mcq('pisa', 'p_car',
        r'អត្រាប្រាក់ចំណេញបន្ថែមនៃការលក់រថយន្តកំណត់ដោយ $P(x) = 30 - 0.28x$ (សែនរៀល) ។ រកបម្រែបម្រួលប្រាក់ចំណេញពីការលក់ $10$ ទៅ $30$ គ្រឿង ៖',
        r'$488$ សែនរៀល ($48\,800\,000$ រៀល)',
        [r'$480$ សែនរៀល', r'$512$ សែនរៀល', r'$460$ សែនរៀល'],
        r'$\int_{10}^{30} (30 - 0.28x)\,dx = [30x - 0.14x^{2}]_{10}^{30} = 774 - 286 = 488$ សែនរៀល ។',
        bloom='Apply'), svg_car_profit()))

    chk(lambda: int_ok(lambda t: 180 + 0.2*t, 30, 40, 1870))
    qs.append(mcq('pisa', 'p_rev',
        r'សហគ្រាសមួយមានអត្រាចំណូលបន្ថែម $R\'(t) = 180 + 0.2t$ (ពាន់រៀល/គ្រឿង) ។ រកបម្រែបម្រួលប្រាក់ចំណូលពេលលក់កើនពី $30$ ទៅ $40$ គ្រឿង ៖',
        r'$1\,870$ ពាន់រៀល ($1\,870\,000$ រៀល)',
        [r'$1\,800$ ពាន់រៀល', r'$1\,940$ ពាន់រៀល', r'$1\,750$ ពាន់រៀល'],
        r'$\int_{30}^{40} (180 + 0.2t)\,dt = [180t + 0.1t^{2}]_{30}^{40} = 7360 - 5490 = 1870$ ពាន់រៀល ។',
        bloom='Apply'))

    chk(lambda: int_ok(lambda t: 180 + 0.2*t, 0, 50, 9250))
    qs.append(mcq('pisa', 'p_rev',
        r'ដោយប្រើអនុគមន៍ចំណូលបន្ថែម $R\'(t) = 180 + 0.2t$ (ពាន់រៀល/គ្រឿង) គណនាចំណូលសរុបបន្ថែមពេលលក់ពី $0$ ដល់ $50$ គ្រឿង ៖',
        r'$9\,250$ ពាន់រៀល',
        [r'$9\,000$ ពាន់រៀល', r'$9\,500$ ពាន់រៀល', r'$8\,750$ ពាន់រៀល'],
        r'$\int_{0}^{50} (180 + 0.2t)\,dt = [180t + 0.1t^{2}]_{0}^{50} = 9000 + 250 = 9250$ ពាន់រៀល ។',
        bloom='Analyze'))

    # =========================================================================
    # WRITING EASY (1)
    # =========================================================================
    chk(lambda: int_ok(lambda x: 3*x**2 + 1, 1, 4, 66))
    qs.append(writing('easy', 's1',
        r'គណនាអាំងតេក្រាលកំណត់ $\int_{1}^{4} (3x^{2} + 1)\,dx$ ។',
        r'66',
        r'$[x^{3} + x]_{1}^{4} = (64 + 4) - (1 + 1) = 68 - 2 = 66$ ។',
        bloom='Apply'))

    # =========================================================================
    # WRITING MEDIUM (4)
    # =========================================================================
    chk(lambda: 4*6 - 2*8 == 8)
    qs.append(with_img(writing('medium', 's1',
        r'គេឱ្យ $\int_{1}^{5} f(x)\,dx = 6$ និង $\int_{1}^{5} g(x)\,dx = 8$ ។ គណនា $\int_{1}^{5} [4f(x) - 2g(x)]\,dx$ ។',
        r'8',
        r'$4\int_{1}^{5} f(x)\,dx - 2\int_{1}^{5} g(x)\,dx = 4(6) - 2(8) = 24 - 16 = 8$ ។',
        bloom='Apply'), svg_additivity()))

    chk(lambda: int_ok(lambda x: 1/mp.sqrt(2*x-1), 1, 5, 2))
    qs.append(writing('medium', 's2',
        r'រកតម្លៃនៃ $k > 1$ បើ $\int_{1}^{k} \frac{1}{\sqrt{2x - 1}}\,dx = 2$ ។',
        r'5',
        r'$\left[\sqrt{2x - 1}\right]_{1}^{k} = \sqrt{2k - 1} - 1 = 2 \implies \sqrt{2k - 1} = 3 \implies k = 5$ ។',
        bloom='Apply'))

    chk(lambda: int_ok(lambda x: (3-mp.sqrt(x))/mp.sqrt(x), 1, 4, 3))
    qs.append(writing('medium', 's1',
        r'គណនាអាំងតេក្រាលកំណត់ $\int_{1}^{4} \frac{3 - \sqrt{x}}{\sqrt{x}}\,dx$ ។',
        r'3',
        r'$\int_{1}^{4} \left(\frac{3}{\sqrt{x}} - 1\right)dx = [6\sqrt{x} - x]_{1}^{4} = (12 - 4) - (6 - 1) = 3$ ។',
        bloom='Apply'))

    chk(lambda: int_ok(lambda x: 3*x**2*mp.sqrt(x**3+1), 0, 2, mp.mpf(52)/3))
    qs.append(writing('medium', 's2',
        r'គណនាអាំងតេក្រាលកំណត់ $\int_{0}^{2} 3x^{2}\sqrt{x^{3} + 1}\,dx$ ជាប្រភាគសម្រួល $p/q$ ។',
        r'52/3',
        r'តាង $u = x^{3} + 1$ បាន $\int_{1}^{9} \sqrt{u}\,du = \left[\frac{2}{3}u^{\frac{3}{2}}\right]_{1}^{9} = \frac{2}{3}(27 - 1) = \frac{52}{3}$ ។',
        bloom='Apply'))

    # =========================================================================
    # WRITING HARD (4)
    # =========================================================================
    chk(lambda: int_ok(lambda x: 1/mp.sqrt(3*x+1), 5, 1, mp.mpf(-4)/3))
    qs.append(writing('hard', 's2',
        r'គណនាអាំងតេក្រាលកំណត់ $\int_{5}^{1} \frac{1}{\sqrt{3x + 1}}\,dx$ ជាប្រភាគសម្រួល $p/q$ ។',
        r'-4/3',
        r'$\left[\frac{2}{3}\sqrt{3x + 1}\right]_{5}^{1} = \frac{2}{3}(2 - 4) = -\frac{4}{3}$ ។',
        bloom='Analyze'))

    chk(lambda: int_ok(lambda x: 5*x*(x**2-7)**3, 1, 3, -800))
    qs.append(writing('hard', 's2',
        r'គណនាអាំងតេក្រាលកំណត់ $\int_{1}^{3} 5x(x^{2} - 7)^{3}\,dx$ ។',
        r'-800',
        r'តាង $u = x^{2} - 7$ បាន $\frac{5}{2}\int_{-6}^{2} u^{3}du = \frac{5}{8}(2^{4} - (-6)^{4}) = \frac{5}{8}(16 - 1296) = -800$ ។',
        bloom='Analyze'))

    chk(lambda: int_ok(lambda x: (x+1)/(x**2+2*x+2)**3, 0, 4, mp.mpf(21)/338))
    qs.append(writing('hard', 's2',
        r'គណនាអាំងតេក្រាលកំណត់ $\int_{0}^{4} \frac{x + 1}{(x^{2} + 2x + 2)^{3}}\,dx$ ជាប្រភាគសម្រួល $p/q$ ។',
        r'21/338',
        r'តាង $u = x^{2}+2x+2$ បាន $\frac{1}{2}\int_{2}^{26} u^{-3}du = \frac{1}{4}\left(\frac{1}{4} - \frac{1}{676}\right) = \frac{21}{338}$ ។',
        bloom='Analyze'))

    chk(lambda: int_ok(lambda x: (1+mp.log(x))**2/(2*x), 1, mp.e, mp.mpf(7)/6))
    qs.append(writing('hard', 's2',
        r'គណនាអាំងតេក្រាលកំណត់ $\int_{1}^{e} \frac{(1 + \ln x)^{2}}{2x}\,dx$ ជាប្រភាគសម្រួល $p/q$ ។',
        r'7/6',
        r'តាង $u = 1 + \ln x$ បាន $\frac{1}{2}\int_{1}^{2} u^{2}du = \frac{1}{6}(8 - 1) = \frac{7}{6}$ ។',
        bloom='Analyze'))

    # =========================================================================
    # WRITING PISA (5)
    # =========================================================================
    chk(lambda: int_ok(lambda x: 5 + 3*x, 0, 8, 136))
    qs.append(writing('pisa', 'p_pop',
        r'ប្រជាជនក្នុងសហគមន៍មួយកើនឡើងតាមអត្រា $t(x) = 5 + 3x$ នាក់/ឆ្នាំ ។ គណនាកំណើនប្រជាជនក្នុងរយៈពេល $8$ ឆ្នាំខាងមុខ ។',
        r'136',
        r'$\int_{0}^{8} (5 + 3x)\,dx = \left[5x + \frac{3}{2}x^{2}\right]_{0}^{8} = 40 + 96 = 136$ នាក់ ។',
        bloom='Apply'))

    chk(lambda: int_ok(lambda t: 5 + 3*t**2, 3, 5, 108))
    qs.append(with_img(writing('pisa', 'p_vel',
        r'វត្ថុមួយផ្លាស់ទីដោយល្បឿន $V(t) = 5 + 3t^{2}\text{ (m/mn)}$ ។ គណនាចម្ងាយចរពីខណៈ $t = 3\text{ mn}$ ដល់ $t = 5\text{ mn}$ (គិតជាម៉ែត្រ) ។',
        r'108',
        r'$\int_{3}^{5} (5 + 3t^{2})\,dt = [5t + t^{3}]_{3}^{5} = 150 - 42 = 108\text{ m}$ ។',
        bloom='Apply'), svg_velocity_graph()))

    chk(lambda: int_ok(lambda x: 30 - 0.28*x, 10, 30, 488))
    qs.append(with_img(writing('pisa', 'p_car',
        r'ក្រុមហ៊ុនលក់រថយន្តមានអត្រាប្រាក់ចំណេញបន្ថែម $P(x) = 30 - 0.28x$ (សែនរៀល) ។ គណនាបម្រែបម្រួលប្រាក់ចំណេញពីការលក់ $10$ ទៅ $30$ គ្រឿង (គិតជាសែនរៀល) ។',
        r'488',
        r'$\int_{10}^{30} (30 - 0.28x)\,dx = [30x - 0.14x^{2}]_{10}^{30} = 774 - 286 = 488$ សែនរៀល ។',
        bloom='Apply'), svg_car_profit()))

    chk(lambda: int_ok(lambda t: 180 + 0.2*t, 30, 40, 1870))
    qs.append(writing('pisa', 'p_rev',
        r'សហគ្រាសមួយមានអត្រាចំណូលបន្ថែម $R\'(t) = 180 + 0.2t$ (ពាន់រៀល/គ្រឿង) ។ គណនាបម្រែបម្រួលប្រាក់ចំណូលពី $30$ ទៅ $40$ គ្រឿង (គិតជាពាន់រៀល) ។',
        r'1870',
        r'$\int_{30}^{40} (180 + 0.2t)\,dt = [180t + 0.1t^{2}]_{30}^{40} = 7360 - 5490 = 1870$ ពាន់រៀល ។',
        bloom='Apply'))

    chk(lambda: int_ok(lambda x: 30 - 0.28*x, 20, 40, 432))
    qs.append(writing('pisa', 'p_car',
        r'ដោយប្រើ $P(x) = 30 - 0.28x$ (សែនរៀល) គណនាបម្រែបម្រួលប្រាក់ចំណេញពីការលក់ $20$ ទៅ $40$ គ្រឿង (គិតជាសែនរៀល) ។',
        r'432',
        r'$\int_{20}^{40} (30 - 0.28x)\,dx = [30x - 0.14x^{2}]_{20}^{40} = (1200 - 224) - (600 - 56) = 432$ សែនរៀល ។',
        bloom='Analyze'))

    return qs


if __name__ == '__main__':
    print(f'G12L16: {len(cands())} candidates, {CNT[0]} numeric checks passed')
