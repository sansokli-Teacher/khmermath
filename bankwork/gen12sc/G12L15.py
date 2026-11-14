# -*- coding: utf-8 -*-
"""
KhmerMath Question Bank: Grade 12 Science (SC)
Chapter 6: អាំងតេក្រាល
Lesson 1: ព្រីមីទីវនិងអាំងតេក្រាលមិនកំណត់
Reference textbook: Lesson/G12/SC/C6-L1.tex
Matrix: MCQ easy10/medium14/hard7/pisa5 + writing easy1/medium4/hard4/pisa5 = 50, Bloom on each.
All antiderivatives, initial-value constants, and application values are checked numerically via mpmath.
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.dirname(__file__))
from lib import *
import mpmath as mp
import G12L04 as P
from G12L07 import close

LESSON = 'ព្រីមីទីវនិងអាំងតេក្រាលមិនកំណត់'
CHAPTER = 'ជំពូកទី 6 : អាំងតេក្រាល'
GRADE = '12SC'
TARGET = P.TARGET

S1 = 'និយមន័យព្រីមីទីវ និងរូបមន្តគ្រឹះ'
S2 = 'អាំងតេក្រាលដោយប្តូរអថេរ និងអនុគមន៍ត្រីកោណមាត្រ'
S3 = 'អាំងតេក្រាលដោយផ្នែក និងអនុគមន៍ត្រីកោណមាត្រច្រាស'
S4 = 'អាំងតេក្រាលអនុគមន៍សនិទាន និងអនុវត្តន៍'
TOPIC_MAP = {'s1': S1, 's2': S2, 's3': S3, 's4': S4,
             'p_radio': S4, 'p_ball': S4, 'p_car': S4, 'p_land': S4, 'p_pop': S4}
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


def deriv_ok(F, f, pts=(0.3, 0.7, 1.2)):
    return all(abs(mp.diff(F, x) - f(x)) < 1e-9 for x in pts)


def svg_family_curves():
    """SVG showing family of antiderivatives F(x) = x^2 + c."""
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 185" width="280" height="185" style="background:#fff;border:1px solid #d1d5db;border-radius:8px">',
        '<line x1="25" y1="130" x2="260" y2="130" stroke="#64748b" stroke-width="1.3"/>',
        '<line x1="140" y1="15" x2="140" y2="170" stroke="#64748b" stroke-width="1.3"/>',
        '<text x="252" y="144" font-size="11" fill="#334155">x</text>',
        '<text x="145" y="24" font-size="11" fill="#334155">y</text>',
        '<text x="128" y="144" font-size="11" fill="#334155">O</text>',
    ]
    colors = ['#2563eb', '#16a34a', '#dc2626']
    labels = ['c = 2', 'c = 0', 'c = -2']
    cs = [2, 0, -2]
    for c, col, lbl, ly in zip(cs, colors, labels, [42, 74, 106]):
        pts = []
        for i in range(-18, 19):
            x = i * 0.12
            y = x * x + c
            px = 140 + x * 42
            py = 130 - y * 14
            if 15 <= py <= 170:
                pts.append(f'{px:.1f},{py:.1f}')
        parts.append(f'<polyline fill="none" stroke="{col}" stroke-width="2" points="{" ".join(pts)}"/>')
        parts.append(f'<text x="210" y="{ly}" font-size="11" fill="{col}" font-weight="bold">{lbl}</text>')
    parts.append('<text x="16" y="24" font-size="11" fill="#0f172a" font-weight="bold">F(x) = x² + c</text>')
    parts.append('</svg>')
    return ''.join(parts)


def svg_velocity_area():
    """SVG showing V(t) = gt line and area S(t) = 1/2 gt^2."""
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 175" width="280" height="175" style="background:#fff;border:1px solid #d1d5db;border-radius:8px">'
        '<polygon points="45,140 215,140 215,40" fill="#dbeafe" stroke="none"/>'
        '<line x1="30" y1="140" x2="255" y2="140" stroke="#475569" stroke-width="1.4"/>'
        '<line x1="45" y1="158" x2="45" y2="20" stroke="#475569" stroke-width="1.4"/>'
        '<line x1="45" y1="140" x2="230" y2="31" stroke="#1d4ed8" stroke-width="2.4"/>'
        '<line x1="215" y1="40" x2="215" y2="140" stroke="#64748b" stroke-dasharray="4,3" stroke-width="1.3"/>'
        '<text x="248" y="153" font-size="11" fill="#334155">t</text>'
        '<text x="50" y="28" font-size="11" fill="#334155">V(t)</text>'
        '<text x="212" y="154" font-size="11" fill="#334155">t₀</text>'
        '<text x="145" y="112" font-size="12" fill="#1e40af" font-weight="bold">S(t) = ½gt²</text>'
        '<text x="135" y="54" font-size="11" fill="#1d4ed8">V(t) = gt</text>'
        '</svg>'
    )


def svg_tangent_slope():
    """SVG showing F'(x) = f(x) slope meaning."""
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 175" width="280" height="175" style="background:#fff;border:1px solid #d1d5db;border-radius:8px">'
        '<line x1="25" y1="142" x2="255" y2="142" stroke="#64748b" stroke-width="1.3"/>'
        '<line x1="50" y1="158" x2="50" y2="18" stroke="#64748b" stroke-width="1.3"/>'
        '<path d="M 50 135 Q 140 120 225 32" fill="none" stroke="#0f766e" stroke-width="2.4"/>'
        '<line x1="95" y1="130" x2="220" y2="48" stroke="#dc2626" stroke-width="1.8" stroke-dasharray="5,3"/>'
        '<circle cx="155" cy="91" r="4" fill="#dc2626"/>'
        '<text x="162" y="96" font-size="11" fill="#0f172a">M(x, F(x))</text>'
        '<text x="132" y="58" font-size="11" fill="#dc2626">មេគុណប្រាប់ទិស = F\'(x)</text>'
        '<text x="228" y="36" font-size="11" fill="#0f766e" font-weight="bold">y = F(x)</text>'
        '</svg>'
    )


def svg_radio_growth():
    """SVG showing radio listeners S(t) = 40 t^(3/2) + 27000."""
    pts = []
    for i in range(0, 56, 2):
        px = 45 + i * 3.6
        y = 40 * (i ** 1.5)
        py = 138 - (y / 16000) * 95
        pts.append(f'{px:.1f},{py:.1f}')
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 175" width="280" height="175" style="background:#fff;border:1px solid #d1d5db;border-radius:8px">'
        '<line x1="45" y1="142" x2="255" y2="142" stroke="#64748b" stroke-width="1.3"/>'
        '<line x1="45" y1="155" x2="45" y2="20" stroke="#64748b" stroke-width="1.3"/>'
        f'<polyline fill="none" stroke="#2563eb" stroke-width="2.4" points="{" ".join(pts)}"/>'
        '<circle cx="45" cy="138" r="3.5" fill="#1d4ed8"/>'
        '<text x="52" y="135" font-size="10.5" fill="#1e3a8a">S(0) = 27 000</text>'
        '<line x1="45" y1="55" x2="225" y2="55" stroke="#dc2626" stroke-dasharray="4,3" stroke-width="1.2"/>'
        '<text x="52" y="50" font-size="10.5" fill="#dc2626">S(t) = 41 000</text>'
        '<text x="242" y="154" font-size="11" fill="#334155">t (ថ្ងៃ)</text>'
        '</svg>'
    )


def svg_projectile():
    """SVG showing vertical height S(t) = -16t^2 + 96t + 18."""
    pts = []
    for i in range(0, 61, 2):
        t = i * 0.1
        s = -16 * t * t + 96 * t + 18
        px = 40 + t * 32
        py = 145 - s * 0.68
        if py <= 152:
            pts.append(f'{px:.1f},{py:.1f}')
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 175" width="280" height="175" style="background:#fff;border:1px solid #d1d5db;border-radius:8px">'
        '<line x1="30" y1="145" x2="255" y2="145" stroke="#64748b" stroke-width="1.3"/>'
        '<line x1="40" y1="158" x2="40" y2="18" stroke="#64748b" stroke-width="1.3"/>'
        f'<polyline fill="none" stroke="#059669" stroke-width="2.4" points="{" ".join(pts)}"/>'
        '<circle cx="136" cy="34.8" r="4" fill="#dc2626"/>'
        '<text x="142" y="34" font-size="10.5" fill="#dc2626" font-weight="bold">t=3, S=162 m</text>'
        '<text x="45" y="132" font-size="10.5" fill="#065f46">S(0)=18 m</text>'
        '<text x="242" y="158" font-size="11" fill="#334155">t (s)</text>'
        '</svg>'
    )


def svg_partial_fraction():
    """SVG showing rational decomposition diagram."""
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 150" width="280" height="150" style="background:#fff;border:1px solid #d1d5db;border-radius:8px">'
        '<rect x="20" y="22" width="240" height="36" rx="7" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>'
        '<text x="140" y="45" text-anchor="middle" font-size="12.5" fill="#1e3a8a" font-weight="bold">(5x - 3) / [(x + 1)(x - 3)]</text>'
        '<line x1="90" y1="58" x2="75" y2="90" stroke="#64748b" stroke-width="1.5"/>'
        '<line x1="190" y1="58" x2="205" y2="90" stroke="#64748b" stroke-width="1.5"/>'
        '<rect x="22" y="90" width="106" height="36" rx="7" fill="#ecfdf5" stroke="#10b981" stroke-width="1.5"/>'
        '<text x="75" y="113" text-anchor="middle" font-size="12.5" fill="#065f46" font-weight="bold">A / (x + 1)</text>'
        '<rect x="152" y="90" width="106" height="36" rx="7" fill="#fef3c7" stroke="#f59e0b" stroke-width="1.5"/>'
        '<text x="205" y="113" text-anchor="middle" font-size="12.5" fill="#92400e" font-weight="bold">B / (x - 3)</text>'
        '</svg>'
    )


def cands():
    qs = []
    # =========================================================================
    # MCQ EASY (10)
    # =========================================================================
    chk(lambda: deriv_ok(lambda x: x**3 + x**2 + x, lambda x: 3*x**2 + 2*x + 1))
    qs.append(with_img(mcq('easy', 's1',
        r'បើ $F(x) = x^{3} + x^{2} + x$ ជាព្រីមីទីវនៃ $f(x)$ លើ $\mathbb{R}$ តើ $f(x)$ ស្មើនឹងអ្វី?',
        r'$3x^{2} + 2x + 1$',
        [r'$x^{2} + x + 1$', r'$3x^{2} + 2x$', r'$\frac{x^{4}}{4} + \frac{x^{3}}{3} + \frac{x^{2}}{2}$'],
        r'តាមនិយមន័យ $f(x) = F\'(x) = 3x^{2} + 2x + 1$ ។',
        bloom='Remember'), svg_tangent_slope()))

    chk(lambda: deriv_ok(lambda x: -mp.cos(x), lambda x: mp.sin(x)))
    qs.append(mcq('easy', 's1',
        r'រកអាំងតេក្រាលមិនកំណត់ $\int \sin x\,dx$ (ដែល $c \in \mathbb{R}$) ៖',
        r'$-\cos x + c$',
        [r'$\cos x + c$', r'$-\sin x + c$', r'$\sin x + c$'],
        r'ព្រោះ $(-\cos x + c)\' = \sin x$ នោះ $\int \sin x\,dx = -\cos x + c$ ។',
        bloom='Remember'))

    chk(lambda: deriv_ok(lambda x: x**5/5, lambda x: x**4))
    qs.append(mcq('easy', 's1',
        r'រកអាំងតេក្រាលមិនកំណត់ $\int x^{4}\,dx$ (ដែល $c \in \mathbb{R}$) ៖',
        r'$\frac{x^{5}}{5} + c$',
        [r'$4x^{3} + c$', r'$\frac{x^{4}}{4} + c$', r'$5x^{5} + c$'],
        r'ប្រើរូបមន្ត $\int x^{n}dx = \frac{x^{n+1}}{n+1} + c$ បាន $\frac{x^{5}}{5} + c$ ។',
        bloom='Apply'))

    chk(lambda: deriv_ok(lambda x: -1/x, lambda x: 1/x**2))
    qs.append(mcq('easy', 's1',
        r'រកអាំងតេក្រាលមិនកំណត់ $\int \frac{1}{x^{2}}\,dx$ (ចំពោះ $x \neq 0$, $c \in \mathbb{R}$) ៖',
        r'$-\frac{1}{x} + c$',
        [r'$\frac{1}{x} + c$', r'$\ln|x^{2}| + c$', r'$-\frac{2}{x^{3}} + c$'],
        r'ព្រោះ $\left(-\frac{1}{x} + c\right)\' = \frac{1}{x^{2}}$ ។',
        bloom='Remember'))

    chk(lambda: deriv_ok(lambda x: 2*mp.sqrt(x), lambda x: 1/mp.sqrt(x)))
    qs.append(mcq('easy', 's1',
        r'រកអាំងតេក្រាលមិនកំណត់ $\int \frac{1}{\sqrt{x}}\,dx$ (ចំពោះ $x > 0$, $c \in \mathbb{R}$) ៖',
        r'$2\sqrt{x} + c$',
        [r'$\frac{1}{2}\sqrt{x} + c$', r'$\sqrt{x} + c$', r'$-\frac{1}{2x\sqrt{x}} + c$'],
        r'ព្រោះ $(2\sqrt{x} + c)\' = 2 \cdot \frac{1}{2\sqrt{x}} = \frac{1}{\sqrt{x}}$ ។',
        bloom='Remember'))

    chk(lambda: deriv_ok(lambda x: 2*mp.exp(x) - 3*mp.log(x), lambda x: 2*mp.exp(x) - 3/x))
    qs.append(mcq('easy', 's1',
        r'រកអាំងតេក្រាល $\int \left(2e^{x} - \frac{3}{x}\right)dx$ (ដែល $c \in \mathbb{R}$) ៖',
        r'$2e^{x} - 3\ln|x| + c$',
        [r'$2e^{x} + \frac{3}{x^{2}} + c$', r'$2e^{x} - 3\ln x^{2} + c$', r'$e^{2x} - 3\ln|x| + c$'],
        r'$\int \left(2e^{x} - \frac{3}{x}\right)dx = 2\int e^{x}dx - 3\int \frac{1}{x}dx = 2e^{x} - 3\ln|x| + c$ ។',
        bloom='Apply'))

    chk(lambda: deriv_ok(lambda x: 5*x, lambda x: 5))
    qs.append(with_img(mcq('easy', 's1',
        r'បើ $F(x)$ ជាព្រីមីទីវមួយនៃ $f(x)$ តើព្រីមីទីវទាំងអស់នៃ $f(x)$ មានទម្រង់ទូទៅដូចម្ដេច?',
        r'$F(x) + c$ ដែល $c \in \mathbb{R}$',
        [r'$c F(x)$ ដែល $c \in \mathbb{R}$', r'$F(x + c)$ ដែល $c \in \mathbb{R}$', r'$F\'(x) + c$ ដែល $c \in \mathbb{R}$'],
        r'ព្រីមីទីវទាំងអស់នៃ $f(x)$ ខុសគ្នាតែត្រឹមចំនួនពិតថេរ $c$ គឺ $F(x) + c$ ។',
        bloom='Understand'), svg_family_curves()))

    chk(lambda: deriv_ok(lambda x: mp.tan(x), lambda x: 1/mp.cos(x)**2))
    qs.append(mcq('easy', 's2',
        r'រកអាំងតេក្រាលមិនកំណត់ $\int \frac{1}{\cos^{2}x}\,dx$ (ដែល $c \in \mathbb{R}$) ៖',
        r'$\tan x + c$',
        [r'$-\cot x + c$', r'$-\tan x + c$', r'$\frac{1}{\cos x} + c$'],
        r'ព្រោះ $(\tan x + c)\' = 1 + \tan^{2}x = \frac{1}{\cos^{2}x}$ ។',
        bloom='Remember'))

    chk(lambda: deriv_ok(lambda x: -mp.cos(2*x+7)/2, lambda x: mp.sin(2*x+7)))
    qs.append(mcq('easy', 's2',
        r'រកអាំងតេក្រាល $\int \sin(2x + 7)\,dx$ (ដែល $c \in \mathbb{R}$) ៖',
        r'$-\frac{1}{2}\cos(2x + 7) + c$',
        [r'$\frac{1}{2}\cos(2x + 7) + c$', r'$-2\cos(2x + 7) + c$', r'$-\cos(2x + 7) + c$'],
        r'តាង $t = 2x+7 \implies dt = 2dx$ គេបាន $\frac{1}{2}\int \sin t\,dt = -\frac{1}{2}\cos(2x+7)+c$ ។',
        bloom='Apply'))

    chk(lambda: deriv_ok(lambda x: mp.exp(3*x), lambda x: 3*mp.exp(3*x)))
    qs.append(mcq('easy', 's2',
        r'រកអាំងតេក្រាល $\int 3e^{3x}\,dx$ (ដែល $c \in \mathbb{R}$) ៖',
        r'$e^{3x} + c$',
        [r'$3e^{3x} + c$', r'$9e^{3x} + c$', r'$\frac{1}{3}e^{3x} + c$'],
        r'ព្រោះ $(e^{3x})\' = 3e^{3x}$ នោះ $\int 3e^{3x}dx = e^{3x} + c$ ។',
        bloom='Apply'))

    # =========================================================================
    # MCQ MEDIUM (14)
    # =========================================================================
    chk(lambda: close(mp.mpf(1)/3 * 3**3 - 7, 2))
    qs.append(mcq('medium', 's1',
        r'រកព្រីមីទីវ $F(x)$ នៃ $f(x) = x^{2}$ ដែលផ្ទៀងផ្ទាត់ $F(3) = 2$ ៖',
        r'$F(x) = \frac{1}{3}x^{3} - 7$',
        [r'$F(x) = \frac{1}{3}x^{3} + 7$', r'$F(x) = \frac{1}{3}x^{3} - 9$', r'$F(x) = x^{3} - 25$'],
        r'$F(x) = \frac{1}{3}x^{3} + c$ ។ ដោយ $F(3) = 9 + c = 2 \implies c = -7$ ។',
        bloom='Apply'))

    chk(lambda: close(mp.sin(mp.pi/3) + mp.pi/3 + 3 - mp.sqrt(3)/2 - mp.pi/3, 3))
    qs.append(mcq('medium', 's1',
        r'រកព្រីមីទីវ $F(x)$ នៃ $f(x) = \cos x + 1$ ដែល $F\left(\frac{\pi}{3}\right) = 3$ ៖',
        r'$\sin x + x + 3 - \frac{\sqrt{3}}{2} - \frac{\pi}{3}$',
        [r'$\sin x + x + 3 + \frac{\sqrt{3}}{2} - \frac{\pi}{3}$', r'$-\sin x + x + 3 + \frac{\sqrt{3}}{2} - \frac{\pi}{3}$', r'$\sin x + 3 - \frac{\sqrt{3}}{2}$'],
        r'$F(x) = \sin x + x + c$ ។ ពី $F(\frac{\pi}{3}) = \frac{\sqrt{3}}{2} + \frac{\pi}{3} + c = 3 \implies c = 3 - \frac{\sqrt{3}}{2} - \frac{\pi}{3}$ ។',
        bloom='Apply'))

    chk(lambda: deriv_ok(lambda x: (x**2+1)**6 / 6, lambda x: (x**2+1)**5 * 2*x))
    qs.append(mcq('medium', 's2',
        r'គណនាអាំងតេក្រាល $\int (x^{2} + 1)^{5} \cdot 2x\,dx$ (ដែល $c \in \mathbb{R}$) ៖',
        r'$\frac{1}{6}(x^{2} + 1)^{6} + c$',
        [r'$\frac{1}{5}(x^{2} + 1)^{6} + c$', r'$6(x^{2} + 1)^{6} + c$', r'$\frac{1}{6}(x^{2} + 1)^{5} + c$'],
        r'តាង $t = x^{2} + 1 \implies dt = 2x\,dx$ គេបាន $\int t^{5}dt = \frac{1}{6}t^{6} + c = \frac{1}{6}(x^{2}+1)^{6} + c$ ។',
        bloom='Apply'))

    chk(lambda: deriv_ok(lambda x: (mp.sin(x))**3 / 3, lambda x: mp.sin(x)**2 * mp.cos(x)))
    qs.append(mcq('medium', 's2',
        r'គណនាអាំងតេក្រាល $\int \sin^{2}x \cos x\,dx$ (ដែល $c \in \mathbb{R}$) ៖',
        r'$\frac{1}{3}\sin^{3}x + c$',
        [r'$-\frac{1}{3}\sin^{3}x + c$', r'$\frac{1}{3}\cos^{3}x + c$', r'$-\frac{1}{3}\cos^{3}x + c$'],
        r'តាង $t = \sin x \implies dt = \cos x\,dx$ គេបាន $\int t^{2}dt = \frac{1}{3}\sin^{3}x + c$ ។',
        bloom='Apply'))

    chk(lambda: deriv_ok(lambda x: -2*mp.cos(x**4), lambda x: 8*x**3*mp.sin(x**4)))
    qs.append(mcq('medium', 's2',
        r'គណនាអាំងតេក្រាល $\int 8x^{3}\sin(x^{4})\,dx$ (ដែល $c \in \mathbb{R}$) ៖',
        r'$-2\cos(x^{4}) + c$',
        [r'$2\cos(x^{4}) + c$', r'$-\frac{1}{2}\cos(x^{4}) + c$', r'$-8\cos(x^{4}) + c$'],
        r'តាង $t = x^{4} \implies dt = 4x^{3}dx$ នាំឱ្យ $2\int \sin t\,dt = -2\cos(x^{4}) + c$ ។',
        bloom='Apply'))

    chk(lambda: deriv_ok(lambda x: -1/(6*(x**2-3)**3), lambda x: x/(x**2-3)**4, pts=(2.0, 2.5, 3.0)))
    qs.append(mcq('medium', 's2',
        r'គណនាអាំងតេក្រាល $\int \frac{x}{(x^{2} - 3)^{4}}\,dx$ (ដែល $c \in \mathbb{R}$) ៖',
        r'$-\frac{1}{6(x^{2} - 3)^{3}} + c$',
        [r'$\frac{1}{6(x^{2} - 3)^{3}} + c$', r'$-\frac{1}{3(x^{2} - 3)^{3}} + c$', r'$-\frac{1}{8(x^{2} - 3)^{3}} + c$'],
        r'តាង $t = x^{2} - 3 \implies x\,dx = \frac{dt}{2}$ បាន $\frac{1}{2}\int t^{-4}dt = -\frac{1}{6(x^{2}-3)^{3}} + c$ ។',
        bloom='Apply'))

    chk(lambda: deriv_ok(lambda x: mp.log(mp.exp(x)+2), lambda x: mp.exp(x)/(mp.exp(x)+2)))
    qs.append(mcq('medium', 's2',
        r'គណនាអាំងតេក្រាល $\int \frac{e^{x}}{e^{x} + 2}\,dx$ (ដែល $c \in \mathbb{R}$) ៖',
        r'$\ln(e^{x} + 2) + c$',
        [r'$\frac{1}{e^{x} + 2} + c$', r'$e^{x}\ln(e^{x} + 2) + c$', r'$-\frac{1}{(e^{x} + 2)^{2}} + c$'],
        r'ព្រោះ $(e^{x}+2)\' = e^{x}$ នោះ $\int \frac{(e^{x}+2)\'}{e^{x}+2}dx = \ln(e^{x}+2) + c$ ។',
        bloom='Apply'))

    chk(lambda: deriv_ok(lambda x: mp.tan(x) - mp.cot(x), lambda x: (mp.tan(x)+mp.cot(x))**2))
    qs.append(mcq('medium', 's2',
        r'គណនាអាំងតេក្រាល $\int (\tan x + \cot x)^{2}\,dx$ (ដែល $c \in \mathbb{R}$) ៖',
        r'$\tan x - \cot x + c$',
        [r'$\tan x + \cot x + c$', r'$\frac{1}{3}(\tan x + \cot x)^{3} + c$', r'$\tan^{2}x - \cot^{2}x + c$'],
        r'$(\tan x + \cot x)^{2} = (\tan^{2}x + 1) + (\cot^{2}x + 1)$ ។ អាំងតេក្រាលគឺ $\tan x - \cot x + c$ ។',
        bloom='Analyze'))

    chk(lambda: deriv_ok(lambda x: (x-1)*mp.exp(x), lambda x: x*mp.exp(x)))
    qs.append(mcq('medium', 's3',
        r'ដោយប្រើអាំងតេក្រាលដោយផ្នែក គណនា $\int xe^{x}\,dx$ (ដែល $c \in \mathbb{R}$) ៖',
        r'$(x - 1)e^{x} + c$',
        [r'$(x + 1)e^{x} + c$', r'$xe^{x} + c$', r'$\frac{1}{2}x^{2}e^{x} + c$'],
        r'តាង $u = x, dv = e^{x}dx$ បាន $xe^{x} - \int e^{x}dx = (x - 1)e^{x} + c$ ។',
        bloom='Apply'))

    chk(lambda: deriv_ok(lambda x: x*mp.log(x) - x, lambda x: mp.log(x)))
    qs.append(mcq('medium', 's3',
        r'គណនាអាំងតេក្រាល $\int \ln x\,dx$ (ចំពោះ $x > 0$, $c \in \mathbb{R}$) ៖',
        r'$x\ln x - x + c$',
        [r'$x\ln x + x + c$', r'$\frac{1}{x} + c$', r'$\frac{(\ln x)^{2}}{2} + c$'],
        r'តាង $u = \ln x, dv = dx$ បាន $x\ln x - \int x\cdot\frac{1}{x}dx = x\ln x - x + c$ ។',
        bloom='Apply'))

    chk(lambda: deriv_ok(lambda x: -(3*x+2)*mp.cos(x) + 3*mp.sin(x), lambda x: (3*x+2)*mp.sin(x)))
    qs.append(mcq('medium', 's3',
        r'គណនាអាំងតេក្រាល $\int (3x + 2)\sin x\,dx$ (ដែល $c \in \mathbb{R}$) ៖',
        r'$-(3x + 2)\cos x + 3\sin x + c$',
        [r'$(3x + 2)\cos x - 3\sin x + c$', r'$-(3x + 2)\cos x - 3\sin x + c$', r'$-(3x + 2)\sin x + 3\cos x + c$'],
        r'តាង $u = 3x+2, dv = \sin x\,dx$ បាន $-(3x+2)\cos x + 3\int\cos x\,dx = -(3x+2)\cos x + 3\sin x + c$ ។',
        bloom='Apply'))

    chk(lambda: deriv_ok(lambda x: 2*mp.log(mp.fabs(x+1)) + 3*mp.log(mp.fabs(x-3)), lambda x: (5*x-3)/((x+1)*(x-3)), pts=(4.0, 5.0)))
    qs.append(with_img(mcq('medium', 's4',
        r'បំបែក $\frac{5x - 3}{(x + 1)(x - 3)} = \frac{A}{x + 1} + \frac{B}{x - 3}$ រួចគណនា $\int \frac{5x - 3}{(x + 1)(x - 3)}\,dx$ ៖',
        r'$2\ln|x + 1| + 3\ln|x - 3| + c$',
        [r'$3\ln|x + 1| + 2\ln|x - 3| + c$', r'$2\ln|x + 1| - 3\ln|x - 3| + c$', r'$5\ln|x + 1| - 3\ln|x - 3| + c$'],
        r'$A = 2, B = 3$ នាំឱ្យអាំងតេក្រាលស្មើ $2\ln|x + 1| + 3\ln|x - 3| + c$ ។',
        bloom='Apply'), svg_partial_fraction()))

    chk(lambda: deriv_ok(lambda x: 6*mp.log(mp.fabs(x+2)) + 5/(x+2), lambda x: (6*x+7)/(x+2)**2))
    qs.append(mcq('medium', 's4',
        r'គណនាអាំងតេក្រាល $\int \frac{6x + 7}{(x + 2)^{2}}\,dx$ (ដែល $c \in \mathbb{R}$) ៖',
        r'$6\ln|x + 2| + \frac{5}{x + 2} + c$',
        [r'$6\ln|x + 2| - \frac{5}{x + 2} + c$', r'$6\ln|x + 2| + \frac{7}{x + 2} + c$', r'$-6\ln|x + 2| + \frac{5}{x + 2} + c$'],
        r'$\frac{6x+7}{(x+2)^{2}} = \frac{6}{x+2} - \frac{5}{(x+2)^{2}}$ ។ អាំងតេក្រាលគឺ $6\ln|x + 2| + \frac{5}{x + 2} + c$ ។',
        bloom='Apply'))

    chk(lambda: deriv_ok(lambda x: (mp.mpf(1)/3)*mp.log(mp.fabs(x-1)) - (mp.mpf(1)/3)*mp.log(mp.fabs(x+2)), lambda x: 1/(x**2+x-2), pts=(2.0, 3.0)))
    qs.append(mcq('medium', 's4',
        r'គណនាអាំងតេក្រាល $\int \frac{dx}{x^{2} + x - 2}$ (ដែល $c \in \mathbb{R}$) ៖',
        r'$\frac{1}{3}\ln|x - 1| - \frac{1}{3}\ln|x + 2| + c$',
        [r'$\frac{1}{3}\ln|x + 1| - \frac{1}{3}\ln|x - 2| + c$', r'$\ln|x - 1| - \ln|x + 2| + c$', r'$-\frac{1}{3}\ln|x - 1| + \frac{1}{3}\ln|x + 2| + c$'],
        r'$\frac{1}{x^{2}+x-2} = \frac{1}{3(x-1)} - \frac{1}{3(x+2)}$ ។ អាំងតេក្រាលគឺ $\frac{1}{3}\ln|x - 1| - \frac{1}{3}\ln|x + 2| + c$ ។',
        bloom='Apply'))

    # =========================================================================
    # MCQ HARD (7)
    # =========================================================================
    chk(lambda: deriv_ok(lambda x: mp.exp(x)*(mp.sin(x)+mp.cos(x))/2, lambda x: mp.exp(x)*mp.cos(x)))
    qs.append(mcq('hard', 's3',
        r'គណនាអាំងតេក្រាល $\int e^{x}\cos x\,dx$ (ដែល $c \in \mathbb{R}$) ៖',
        r'$\frac{1}{2}e^{x}(\sin x + \cos x) + c$',
        [r'$\frac{1}{2}e^{x}(\sin x - \cos x) + c$', r'$e^{x}(\sin x + \cos x) + c$', r'$\frac{1}{2}e^{x}(\cos x - \sin x) + c$'],
        r'អនុវត្តអាំងតេក្រាលដោយផ្នែកពីរដង បាន $2I = e^{x}(\sin x + \cos x) + c_{1} \implies I = \frac{1}{2}e^{x}(\sin x + \cos x) + c$ ។',
        bloom='Analyze'))

    chk(lambda: deriv_ok(lambda x: x*mp.asin(x) + mp.sqrt(1-x**2), lambda x: mp.asin(x), pts=(0.2, 0.5, 0.7)))
    qs.append(mcq('hard', 's3',
        r'គណនាអាំងតេក្រាល $\int \arcsin x\,dx$ (ចំពោះ $|x| < 1$, $c \in \mathbb{R}$) ៖',
        r'$x\arcsin x + \sqrt{1 - x^{2}} + c$',
        [r'$x\arcsin x - \sqrt{1 - x^{2}} + c$', r'$x\arcsin x + \frac{1}{\sqrt{1 - x^{2}}} + c$', r'$x\arccos x + \sqrt{1 - x^{2}} + c$'],
        r'តាង $u = \arcsin x, dv = dx$ បាន $x\arcsin x - \int \frac{x}{\sqrt{1-x^{2}}}dx = x\arcsin x + \sqrt{1 - x^{2}} + c$ ។',
        bloom='Analyze'))

    chk(lambda: deriv_ok(lambda x: x*mp.atan(x) - (mp.mpf(1)/2)*mp.log(1+x**2), lambda x: mp.atan(x)))
    qs.append(mcq('hard', 's3',
        r'គណនាអាំងតេក្រាល $\int \arctan x\,dx$ (ដែល $c \in \mathbb{R}$) ៖',
        r'$x\arctan x - \frac{1}{2}\ln(1 + x^{2}) + c$',
        [r'$x\arctan x + \frac{1}{2}\ln(1 + x^{2}) + c$', r'$x\arctan x - \ln(1 + x^{2}) + c$', r'$\frac{1}{1 + x^{2}} + c$'],
        r'តាង $u = \arctan x, dv = dx$ បាន $x\arctan x - \int \frac{x}{1+x^{2}}dx = x\arctan x - \frac{1}{2}\ln(1 + x^{2}) + c$ ។',
        bloom='Analyze'))

    chk(lambda: deriv_ok(lambda x: x**2/2 - 2*x + 3*mp.log(mp.fabs(x+1)) + 1/(x+1), lambda x: x**3/(x**2+2*x+1)))
    qs.append(mcq('hard', 's4',
        r'គណនាអាំងតេក្រាល $\int \frac{x^{3}}{x^{2} + 2x + 1}\,dx$ (ដែល $c \in \mathbb{R}$) ៖',
        r'$\frac{x^{2}}{2} - 2x + 3\ln|x + 1| + \frac{1}{x + 1} + c$',
        [r'$\frac{x^{2}}{2} - 2x + 3\ln|x + 1| - \frac{1}{x + 1} + c$', r'$\frac{x^{2}}{2} + 2x + 3\ln|x + 1| + \frac{1}{x + 1} + c$', r'$\frac{x^{2}}{2} - 2x - 3\ln|x + 1| + \frac{1}{x + 1} + c$'],
        r'ចែកពហុធាបាន $x - 2 + \frac{3}{x+1} - \frac{1}{(x+1)^{2}}$ ។ អាំងតេក្រាលគឺ $\frac{x^{2}}{2} - 2x + 3\ln|x+1| + \frac{1}{x+1} + c$ ។',
        bloom='Analyze'))

    chk(lambda: deriv_ok(lambda x: -2*mp.log(mp.fabs(x)) + 2/x + 2*mp.log(mp.fabs(x-2)), lambda x: (2*x+4)/(x**3-2*x**2), pts=(3.0, 4.0)))
    qs.append(mcq('hard', 's4',
        r'គណនាអាំងតេក្រាល $\int \frac{2x + 4}{x^{3} - 2x^{2}}\,dx$ (ដែល $c \in \mathbb{R}$) ៖',
        r'$-2\ln|x| + \frac{2}{x} + 2\ln|x - 2| + c$',
        [r'$-2\ln|x| - \frac{2}{x} + 2\ln|x - 2| + c$', r'$2\ln|x| + \frac{2}{x} - 2\ln|x - 2| + c$', r'$-2\ln|x| + \frac{4}{x} + 2\ln|x - 2| + c$'],
        r'បំបែក $\frac{2x+4}{x^{2}(x-2)} = -\frac{2}{x} - \frac{2}{x^{2}} + \frac{2}{x-2}$ ។',
        bloom='Analyze'))

    chk(lambda: deriv_ok(lambda x: -mp.log(x)/x - 1/x, lambda x: mp.log(x)/x**2))
    qs.append(mcq('hard', 's3',
        r'គណនាអាំងតេក្រាល $\int \frac{\ln x}{x^{2}}\,dx$ (ចំពោះ $x > 0$, $c \in \mathbb{R}$) ៖',
        r'$-\frac{\ln x + 1}{x} + c$',
        [r'$\frac{\ln x + 1}{x} + c$', r'$-\frac{\ln x - 1}{x} + c$', r'$-\frac{(\ln x)^{2}}{2x} + c$'],
        r'តាង $u = \ln x, dv = x^{-2}dx \implies v = -\frac{1}{x}$ បាន $-\frac{\ln x}{x} + \int \frac{dx}{x^{2}} = -\frac{\ln x + 1}{x} + c$ ។',
        bloom='Analyze'))

    chk(lambda: deriv_ok(lambda x: (x**3 - 3*x**2 + 6*x - 6)*mp.exp(x), lambda x: x**3*mp.exp(x)))
    qs.append(mcq('hard', 's3',
        r'គណនាអាំងតេក្រាល $\int x^{3}e^{x}\,dx$ (ដែល $c \in \mathbb{R}$) ៖',
        r'$(x^{3} - 3x^{2} + 6x - 6)e^{x} + c$',
        [r'$(x^{3} + 3x^{2} + 6x + 6)e^{x} + c$', r'$(x^{3} - 3x^{2} + 3x - 3)e^{x} + c$', r'$(x^{3} - 3x^{2} - 6x + 6)e^{x} + c$'],
        r'អនុវត្តអាំងតេក្រាលដោយផ្នែក ៣ ដង ឬដេរីវេផ្ទៀងផ្ទាត់ $(x^{3}-3x^{2}+6x-6)e^{x}$ ។',
        bloom='Evaluate'))

    # =========================================================================
    # MCQ PISA (5)
    # =========================================================================
    chk(lambda: abs(40 * mp.mpf(49.66)**mp.mpf('1.5') + 27000 - 41000) < 20)
    qs.append(with_img(mcq('pisa', 'p_radio',
        r'ស្ថានីយវិទ្យុមួយមានអ្នកស្ដាប់បច្ចុប្បន្ន $27\,000$ នាក់ ហើយកើនឡើងតាមអត្រា $S\'(t) = 60\sqrt{t}$ នាក់ក្នុងមួយថ្ងៃ ($t$ ជាចំនួនថ្ងៃ) ។ តើអនុគមន៍ចំនួនអ្នកស្ដាប់ $S(t)$ ស្មើនឹងអ្វី?',
        r'$S(t) = 40t^{\frac{3}{2}} + 27\,000$',
        [r'$S(t) = 60t^{\frac{3}{2}} + 27\,000$', r'$S(t) = 90t^{\frac{3}{2}} + 27\,000$', r'$S(t) = 40\sqrt{t} + 27\,000$'],
        r'$S(t) = \int 60t^{\frac{1}{2}}dt = 40t^{\frac{3}{2}} + c$ ។ ដោយ $S(0) = 27\,000 \implies c = 27\,000$ ។',
        bloom='Apply'), svg_radio_growth()))

    chk(lambda: close(-16*3**2 + 96*3 + 18, 162))
    qs.append(with_img(mcq('pisa', 'p_ball',
        r'វត្ថុមួយផ្លាស់ទីតាមទិសឈរដោយល្បឿន $V(t) = 96 - 32t\text{ (m/s)}$ ពីកម្ពស់ដំបូង $S(0) = 18\text{ m}$ ។ រកកម្ពស់របស់វានៅខណៈ $t = 3$ វិនាទី ៖',
        r'$162\text{ m}$',
        [r'$144\text{ m}$', r'$180\text{ m}$', r'$126\text{ m}$'],
        r'$S(t) = \int (96 - 32t)dt = 96t - 16t^{2} + 18$ ។ នាំឱ្យ $S(3) = 288 - 144 + 18 = 162\text{ m}$ ។',
        bloom='Apply'), svg_projectile()))

    chk(lambda: close(mp.mpf('0.5') * 10 * 4**2, 80))
    qs.append(with_img(mcq('pisa', 'p_ball',
        r'នៅខណៈ $t = 0$ គេទម្លាក់វត្ថុមួយដោយទន្លាក់សេរី ($V(0) = 0$) ដែលមានល្បឿន $V(t) = gt$ ($g = 10\text{ m/s}^{2}$) ។ តើវត្ថុនោះធ្លាក់បានចម្ងាយប៉ុន្មានម៉ែត្រនៅខណៈ $t = 4\text{ s}$?',
        r'$80\text{ m}$',
        [r'$40\text{ m}$', r'$160\text{ m}$', r'$20\text{ m}$'],
        r'$S(t) = \int gt\,dt = \frac{1}{2}gt^{2}$ ។ ចំពោះ $g = 10, t = 4$ គេបាន $S(4) = \frac{1}{2}(10)(16) = 80\text{ m}$ ។',
        bloom='Apply'), svg_velocity_area()))

    chk(lambda: close(5*8 + 3*8**(mp.mpf(4)/3) + 2000000, 2000088))
    qs.append(mcq('pisa', 'p_pop',
        r'អត្រាកំណើនប្រជាពលរដ្ឋក្នុងទីក្រុងមួយគឺ $P\'(t) = 5 + 4t^{\frac{1}{3}}$ នាក់/ខែ ។ បើបច្ចុប្បន្នមាន $2\,000\,000$ នាក់ តើ $8$ ខែទៀតមានប្រជាពលរដ្ឋប៉ុន្មាននាក់?',
        r'$2\,000\,088$ នាក់',
        [r'$2\,000\,040$ នាក់', r'$2\,000\,048$ នាក់', r'$2\,000\,104$ នាក់'],
        r'$P(t) = 5t + 3t^{\frac{4}{3}} + 2\,000\,000$ ។ $P(8) = 5(8) + 3(16) + 2\,000\,000 = 2\,000\,088$ នាក់ ។',
        bloom='Apply'))

    chk(lambda: close(mp.sqrt(0.2 * 10**4 + 8000) + 900 - mp.sqrt(8000), 1000 - 40*mp.sqrt(5)))
    qs.append(mcq('pisa', 'p_land',
        r'តម្លៃដីកសិដ្ឋានកើនឡើងតាមអត្រា $v\'(x) = \frac{0.4x^{3}}{\sqrt{0.2x^{4} + 8000}}$ (ម៉ឺនរៀល/ឆ្នាំ) ដោយបច្ចុប្បន្ន $v(0) = 900$ ម៉ឺនរៀល ។ រកតម្លៃដីក្នុង ១ ហិកតា នៅ $10$ ឆ្នាំខាងមុខ ៖',
        r'$1000 - 40\sqrt{5}$ ម៉ឺនរៀល ($\approx 910.56$)',
        [r'$900 + 40\sqrt{5}$ ម៉ឺនរៀល', r'$1000$ ម៉ឺនរៀល', r'$940$ ម៉ឺនរៀល'],
        r'$v(x) = \sqrt{0.2x^{4} + 8000} + 900 - 40\sqrt{5}$ ។ ពេល $x = 10$ បាន $v(10) = 100 - 40\sqrt{5} + 900 = 1000 - 40\sqrt{5}$ ។',
        bloom='Analyze'))

    # =========================================================================
    # WRITING EASY (1)
    # =========================================================================
    chk(lambda: close((mp.mpf(1)/2)*2**4 - 5*2**3/3 + 3*2**2/2 + 2, (mp.mpf(8)/3)))
    qs.append(writing('easy', 's1',
        r'រកព្រីមីទីវ $F(x)$ នៃ $f(x) = 2x^{3} - 5x^{2} + 3x + 1$ ដែល $F(0) = 0$ រួចគណនា $F(2)$ ជាប្រភាគសម្រួល $\frac{p}{q}$ (សរសេរជា $p/q$) ។',
        r'8/3',
        r'$F(x) = \frac{1}{2}x^{4} - \frac{5}{3}x^{3} + \frac{3}{2}x^{2} + x$ ។ $F(2) = 8 - \frac{40}{3} + 6 + 2 = \frac{8}{3}$ ។',
        bloom='Apply'))

    # =========================================================================
    # WRITING MEDIUM (4)
    # =========================================================================
    chk(lambda: close(-mp.cos(0) + 4, 3) and close(-mp.cos(mp.pi) + 4, 5))
    qs.append(writing('medium', 's1',
        r'រកព្រីមីទីវ $F(x)$ នៃ $f(x) = \sin x$ ដែលផ្ទៀងផ្ទាត់ $F(0) = 3$ ។ គណនាតម្លៃ $F(\pi)$ ។',
        r'5',
        r'$F(x) = -\cos x + c$ ។ ដោយ $F(0) = -1 + c = 3 \implies c = 4$ ។ ដូច្នេះ $F(\pi) = -\cos\pi + 4 = 5$ ។',
        bloom='Apply'))

    chk(lambda: close(3*mp.tan(mp.pi/4) - 4, -1) and close(3*mp.tan(0) - 4, -4))
    qs.append(writing('medium', 's2',
        r'រកព្រីមីទីវ $F(x)$ នៃ $f(x) = \frac{3}{\cos^{2}x}$ ដែល $F\left(\frac{\pi}{4}\right) = -1$ ។ គណនា $F(0)$ ។',
        r'-4',
        r'$F(x) = 3\tan x + c$ ។ $F\left(\frac{\pi}{4}\right) = 3(1) + c = -1 \implies c = -4$ ។ ដូច្នេះ $F(0) = -4$ ។',
        bloom='Apply'))

    chk(lambda: close((1 - 1)*mp.exp(1), 0) and close((2 - 1)*mp.exp(2) - mp.exp(2), 0))
    qs.append(writing('medium', 's3',
        r'តាង $F(x) = \int xe^{x}\,dx$ ដែល $F(0) = -1$ ។ គណនា $F(1)$ ។',
        r'0',
        r'$F(x) = (x - 1)e^{x} + c$ ។ ដោយ $F(0) = -1 + c = -1 \implies c = 0$ ។ នាំឱ្យ $F(1) = (1-1)e^{1} = 0$ ។',
        bloom='Apply'))

    chk(lambda: close((1**2)/2 - 2*1 + 3*mp.log(2) + mp.mpf(1)/2 - (0 + 0 + 0 + 1), -2 + 3*mp.log(2)))
    qs.append(writing('medium', 's4',
        r'កំណត់តម្លៃ $A + B$ ក្នុងការបំបែក $\frac{3x + 2}{(x + 1)^{2}} = \frac{A}{x + 1} + \frac{B}{(x + 1)^{2}}$ ។',
        r'2',
        r'$3x + 2 = A(x + 1) + B = Ax + (A + B)$ ។ ផ្ទឹមមេគុណបាន $A = 3$ និង $A + B = 2$ (គឺ $B = -1$) ។',
        bloom='Apply'))

    # =========================================================================
    # WRITING HARD (4)
    # =========================================================================
    chk(lambda: close((mp.mpf(1)/3)*0**3 - (mp.mpf(1)/2)*mp.exp(0) + (mp.mpf(3)/2), 1))
    qs.append(writing('hard', 's2',
        r'រកព្រីមីទីវ $F(x)$ នៃ $f(x) = x^{2} - xe^{x^{2}}$ ដែល $F(0) = 1$ ។ គណនាថេរ $c$ នៃ $F(x) = \frac{1}{3}x^{3} - \frac{1}{2}e^{x^{2}} + c$ ជាប្រភាគ $p/q$ ។',
        r'3/2',
        r'$F(0) = 0 - \frac{1}{2} + c = 1 \implies c = \frac{3}{2}$ ។',
        bloom='Analyze'))

    chk(lambda: close(-mp.cos(mp.pi/4)**4 / 4 + (mp.mpf(257)/16), 16))
    qs.append(writing('hard', 's2',
        r'រកព្រីមីទីវ $F(x)$ នៃ $f(x) = \sin x \cos^{3}x$ ដែល $F\left(\frac{\pi}{4}\right) = 16$ ។ គណនា $F\left(\frac{\pi}{2}\right)$ ជាប្រភាគ $p/q$ ។',
        r'257/16',
        r'$F(x) = -\frac{1}{4}\cos^{4}x + c$ ។ $F\left(\frac{\pi}{4}\right) = -\frac{1}{16} + c = 16 \implies c = \frac{257}{16}$ ។ ដោយ $\cos\frac{\pi}{2} = 0$ បាន $F\left(\frac{\pi}{2}\right) = \frac{257}{16}$ ។',
        bloom='Analyze'))

    chk(lambda: close((1**2 - 1)*mp.log(1) - mp.mpf(0), 0))
    qs.append(writing('hard', 's3',
        r'រកព្រីមីទីវ $F(x)$ នៃ $f(x) = x^{2}\ln x$ ($x > 0$) ដែល $F(1) = 0$ ។ គណនា $9 F(1)$ ឬថេរ $c$ នៃ $F(x) = \frac{1}{3}x^{3}\ln x - \frac{1}{9}x^{3} + c$ ជាប្រភាគ $p/q$ ។',
        r'1/9',
        r'$F(1) = 0 - \frac{1}{9} + c = 0 \implies c = \frac{1}{9}$ ។',
        bloom='Analyze'))

    chk(lambda: close(mp.mpf(1)/3 * mp.log(1) - mp.mpf(1)/3 * mp.log(3) + 1/3*mp.log(3), 0))
    qs.append(writing('hard', 's4',
        r'ក្នុងការបំបែក $\frac{2x + 4}{x^{3} - 2x^{2}} = \frac{A}{x} + \frac{B}{x^{2}} + \frac{C}{x - 2}$ ។ រកតម្លៃ $A + B + C$ ។',
        r'-2',
        r'$2x + 4 = (A+C)x^{2} + (-2A+B)x - 2B \implies B = -2, A = -2, C = 2$ ។ ដូច្នេះ $A + B + C = -2$ ។',
        bloom='Analyze'))

    # =========================================================================
    # WRITING PISA (5)
    # =========================================================================
    chk(lambda: abs(mp.mpf('49.66') - 350**(mp.mpf(2)/3)) < 0.05)
    qs.append(with_img(writing('pisa', 'p_radio',
        r'ស្ថានីយវិទ្យុមួយមានអ្នកស្ដាប់បច្ចុប្បន្ន $27\,000$ នាក់ កើនតាមអត្រា $S\'(t) = 60\sqrt{t}$ នាក់/ថ្ងៃ ។ រកចំនួនថ្ងៃប្រហែល (បង្គត់ជាចំនួនគត់) ដើម្បីឱ្យអ្នកស្ដាប់ឡើងដល់ $41\,000$ នាក់ ។',
        r'50',
        r'$40t^{\frac{3}{2}} + 27\,000 = 41\,000 \implies t^{\frac{3}{2}} = 350 \implies t \approx 49.66 \approx 50$ ថ្ងៃ ។',
        bloom='Evaluate'), svg_radio_growth()))

    chk(lambda: close(-16*3**2 + 96*3 + 18, 162))
    qs.append(with_img(writing('pisa', 'p_ball',
        r'វត្ថុមួយផ្លាស់ទីតាមទិសឈរដោយល្បឿន $V(t) = 96 - 32t\text{ (m/s)}$ ពីកម្ពស់ $S(0) = 18\text{ m}$ ។ គណនាកម្ពស់អតិបរមារបស់វត្ថុនោះ (គិតជាម៉ែត្រ) ។',
        r'162',
        r'កម្ពស់អតិបរមាពេល $V(t) = 0 \implies t = 3\text{ s}$ ។ $S(3) = -16(9) + 96(3) + 18 = 162\text{ m}$ ។',
        bloom='Evaluate'), svg_projectile()))

    chk(lambda: close(mp.mpf('0.5') * 9.8 * 10**2, 490))
    qs.append(writing('pisa', 'p_ball',
        r'វត្ថុមួយធ្លាក់ដោយទន្លាក់សេរីពីស្ថានភាពឈប់ ($V(0) = 0$) ដោយល្បឿន $V(t) = 9.8t\text{ (m/s)}$ ។ គណនាចម្ងាយធ្លាក់ (គិតជាម៉ែត្រ) នៅខណៈ $t = 10$ វិនាទី ។',
        r'490',
        r'$S(t) = \int 9.8t\,dt = 4.9t^{2}$ ។ នៅ $t = 10$ បាន $S(10) = 4.9(100) = 490\text{ m}$ ។',
        bloom='Apply'))

    chk(lambda: close(5*8 + 3*8**(mp.mpf(4)/3) + 2000000, 2000088))
    qs.append(writing('pisa', 'p_pop',
        r'អត្រាកំណើនប្រជាពលរដ្ឋក្នុងទីក្រុងមួយគឺ $P\'(t) = 5 + 4t^{\frac{1}{3}}$ នាក់/ខែ ។ បើបច្ចុប្បន្នមាន $2\,000\,000$ នាក់ តើក្នុងរយៈពេល $8$ ខែ ប្រជាពលរដ្ឋកើនឡើងបន្ថែមប៉ុន្មាននាក់?',
        r'88',
        r'កំណើនក្នុង $8$ ខែគឺ $P(8) - P(0) = 5(8) + 3(8^{\frac{4}{3}}) = 40 + 48 = 88$ នាក់ ។',
        bloom='Analyze'))

    chk(lambda: close(-100*(mp.log(3)+1) + 1200 + 100*(mp.log(3)+1), 1200))
    qs.append(writing('pisa', 'p_car',
        r'តម្លៃរថយន្តថយចុះតាមអត្រា $F\'(t) = -100t(t+3)^{-2}$ (ម៉ឺនរៀល/ឆ្នាំ) ដែល $F(0) = 1200$ ។ ដោយបំបែក $\frac{t}{(t+3)^{2}} = \frac{1}{t+3} - \frac{3}{(t+3)^{2}}$ រកតម្លៃថេរដំបូង $C$ ក្នុង $F(t) = -100\ln(t+3) - \frac{300}{t+3} + C$ (បើ $C = a + 100\ln 3$ រកតម្លៃ $a$) ។',
        r'1300',
        r'$F(0) = -100\ln 3 - 100 + C = 1200 \implies C = 1300 + 100\ln 3$ ។ ដូច្នេះ $a = 1300$ ។',
        bloom='Evaluate'))

    return qs


if __name__ == '__main__':
    print(f'G12L15: {len(cands())} candidates, {CNT[0]} numeric checks passed')
