# -*- coding: utf-8 -*-
"""
KhmerMath Question Bank: Grade 12 Science (SC)
Chapter 5: វ៉ិចទ័រក្នុងលំហ
Lesson 1: វ៉ិចទ័រក្នុងលំហ
Reference textbook: Lesson/G12/SC/C5-L1.tex
Matrix: MCQ easy10/medium14/hard7/pisa5 + writing easy1/medium4/hard4/pisa5 = 50, Bloom on each.
Vector operations, dot products, distances, angles, and direction cosines are checked numerically.
"""
import sys, os, math
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.dirname(__file__))
from lib import *
import svgkit as K
import mpmath as mp
import G12L04 as P
from G12L04 import G
from G12L07 import close

LESSON = 'វ៉ិចទ័រក្នុងលំហ'
CHAPTER = 'ជំពូកទី 5 : វ៉ិចទ័រក្នុងលំហ'
GRADE = '12SC'
TARGET = P.TARGET

S1 = 'សញ្ញាណវ៉ិចទ័រ វ៉ិចទ័រស្មើគ្នា និងវ៉ិចទ័រផ្ទុយគ្នា'
S2 = 'ប្រមាណវិធីលើវ៉ិចទ័រក្នុងលំហ'
S3 = 'កូអរដោនេក្នុងលំហ'
S4 = 'ផលគុណស្កាលែនៃវ៉ិចទ័រក្នុងលំហ'
S5 = 'ចម្ងាយនិងទិសដៅកូស៊ីនុស'
TOPIC_MAP = {'s1': S1, 's2': S2, 's3': S3, 's4': S4, 's5': S5,
             'p_force': S4, 'p_drone': S5, 'p_roof': S4, 'p_cube': S4, 'p_nav': S5}
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


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def norm2(u):
    return sum(a * a for a in u)


def norm(u):
    return mp.sqrt(norm2(u))


def _svg(w, h, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" style="max-width:100%;height:auto;font-family:serif">{body}</svg>'


def _line(x1, y1, x2, y2, stroke='#2563eb', sw=1.8, dash=''):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"{d}/>'


def _dot(x, y, r=3.5, fill='#dc2626'):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"/>'


def _text(x, y, txt, size=12, fill='#0f172a', anchor='middle', bold=False):
    w = ' font-weight="bold"' if bold else ''
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}"{w}>{txt}</text>'


def fig_cube(labels=True):
    s = []
    # Bottom EFGH: E(60,165), F(180,165), G(230,130), H(110,130)
    # Top ABCD:    A(60,75),  B(180,75),  C(230,40),  D(110,40)
    E, F, Gp, H = (60, 165), (180, 165), (230, 130), (110, 130)
    A, B, C, D = (60, 75), (180, 75), (230, 40), (110, 40)
    for p, q in ((E, H), (H, Gp), (H, D)):
        s.append(_line(p[0], p[1], q[0], q[1], '#94a3b8', 1.3, '4,4'))
    for p, q in ((E, F), (F, Gp), (A, B), (B, C), (C, D), (D, A), (E, A), (F, B), (Gp, C)):
        s.append(_line(p[0], p[1], q[0], q[1], '#2563eb', 1.8))
    if labels:
        for name, (x, y), dx, dy in (('A', A, -12, 4), ('B', B, 8, 12), ('C', C, 8, -2), ('D', D, -10, -6),
                                     ('E', E, -12, 6), ('F', F, 4, 14), ('G', Gp, 8, 4), ('H', H, -12, -4)):
            s.append(_text(x + dx, y + dy, name, 12, '#0f172a', 'middle', True))
    return _svg(290, 215, ''.join(s))


def fig_axes_p():
    s = []
    O = (110, 145)
    s.append(_line(O[0], O[1], 45, 190, '#64748b', 1.5))
    s.append(_line(O[0], O[1], 245, 145, '#64748b', 1.5))
    s.append(_line(O[0], O[1], 110, 25, '#64748b', 1.5))
    s.append(_text(35, 198, 'x', 12, '#334155'))
    s.append(_text(255, 149, 'y', 12, '#334155'))
    s.append(_text(110, 18, 'z', 12, '#334155'))
    s.append(_text(98, 142, 'O', 12, '#0f172a', 'middle', True))
    # Box to P(x,y,z)
    P1 = (75, 169)
    P2 = (195, 145)
    P3 = (110, 55)
    Pp = (160, 169)
    Pt = (160, 79)
    for p, q in ((P1, Pp), (P2, Pp), (Pp, Pt), (P3, Pt)):
        s.append(_line(p[0], p[1], q[0], q[1], '#94a3b8', 1.2, '4,3'))
    s.append(_line(O[0], O[1], Pt[0], Pt[1], '#dc2626', 2.2))
    s.append(_dot(Pt[0], Pt[1], 3.5, '#dc2626'))
    s.append(_text(Pt[0] + 10, Pt[1] - 4, 'P(x,y,z)', 12, '#dc2626', 'start', True))
    s.append(_text(Pp[0] + 6, Pp[1] + 12, 'H(x,y,0)', 11, '#475569', 'start'))
    return _svg(290, 215, ''.join(s))


def fig_pyramid():
    s = []
    A, B, C, D, S = (50, 165), (175, 165), (225, 130), (100, 130), (138, 32)
    for p, q in ((A, D), (D, C), (S, D), (A, C)):
        s.append(_line(p[0], p[1], q[0], q[1], '#94a3b8', 1.3, '4,4'))
    for p, q in ((A, B), (B, C), (S, A), (S, B), (S, C)):
        s.append(_line(p[0], p[1], q[0], q[1], '#2563eb', 1.8))
    for name, (x, y), dx, dy in (('S', S, 0, -8), ('A', A, -10, 12), ('B', B, 8, 12), ('C', C, 10, 2), ('D', D, -10, -4)):
        s.append(_text(x + dx, y + dy, name, 12, '#0f172a', 'middle', True))
    return _svg(280, 210, ''.join(s))


def fig_drone():
    s = []
    O = (60, 165)
    s.append(_line(O[0], O[1], 260, 165, '#64748b', 1.4))
    s.append(_line(O[0], O[1], 60, 30, '#64748b', 1.4))
    s.append(_line(O[0], O[1], 210, 65, '#2563eb', 2.2))
    s.append(_line(210, 65, 210, 165, '#94a3b8', 1.3, '4,3'))
    s.append(_dot(O[0], O[1], 3.5, '#0f172a'))
    s.append(_dot(210, 65, 4, '#dc2626'))
    s.append(_text(52, 178, 'O(0,0,0)', 11, '#0f172a'))
    s.append(_text(215, 58, 'P(6,8,24)', 11, '#dc2626', 'start', True))
    s.append(_text(215, 178, 'H(6,8,0)', 11, '#475569'))
    return _svg(300, 210, ''.join(s))


def cands():
    C = []
    # ============================================================ MCQ EASY (10)
    C.append(mcq('easy', 's1', 'ចំពោះវ៉ិចទ័រ ' + M('\\vec{AB}') + ' ៖', M('A') + ' ជាគល់ និង ' + M('B') + ' ជាចុង',
                 [M('B') + ' ជាគល់ និង ' + M('A') + ' ជាចុង', M('A') + ' និង ' + M('B') + ' ជាគល់', 'គ្មានចំណុចគល់'],
                 'អង្កត់មានទិសដៅ ' + M('AB') + ' មាន ' + M('A') + ' ជាគល់ និង ' + M('B') + ' ជាចុង។', 'Remember'))
    C.append(with_img(mcq('easy', 's1', 'ក្នុងគូប ' + M('ABCD\\text{-}EFGH') + ' ដូចរូប តើវ៉ិចទ័រណាស្មើនឹង ' + M('\\vec{AB}') + ' ?',
                          M('\\vec{DC}'), [M('\\vec{CD}'), M('\\vec{AD}'), M('\\vec{BA}')],
                          'ក្នុងគូប ' + M('\\vec{AB}') + ' និង ' + M('\\vec{DC}') + ' ស្របគ្នា មានទិសដៅដូចគ្នា និងប្រវែងស្មើគ្នា។', 'Understand'), fig_cube()))
    C.append(mcq('easy', 's1', 'ចំពោះពីរចំណុច ' + M('A') + ' និង ' + M('B') + ' ក្នុងលំហ ' + M('\\vec{AB}') + ' ស្មើនឹង ៖',
                 M('-\\vec{BA}'), [M('\\vec{BA}'), M('\\vec{0}'), M('2\\vec{BA}')],
                 M('\\vec{AB}') + ' និង ' + M('\\vec{BA}') + ' ជាវ៉ិចទ័រផ្ទុយគ្នា ដូច្នេះ ' + M('\\vec{AB}=-\\vec{BA}') + '។', 'Remember'))
    C.append(mcq('easy', 's2', 'តាមវិធានត្រីកោណ ' + M('\\vec{AB}+\\vec{BF}') + ' ស្មើនឹង ៖',
                 M('\\vec{AF}'), [M('\\vec{FA}'), M('\\vec{AB}'), M('\\vec{BF}')],
                 'ផលបូកវ៉ិចទ័រតគ្នា ' + M('\\vec{AB}+\\vec{BF}=\\vec{AF}') + '។', 'Remember'))
    C.append(mcq('easy', 's3', 'ក្នុងតម្រុយអរតូណរម៉ាល់ ' + M('(O,\\vec{i},\\vec{j},\\vec{k})') + ' កូអរដោនេនៃវ៉ិចទ័រឯកតា ' + M('\\vec{j}') + ' គឺ ៖',
                 M('(0,1,0)'), [M('(1,0,0)'), M('(0,0,1)'), M('(1,1,0)')],
                 M('\\vec{i}=(1,0,0),\\ \\vec{j}=(0,1,0),\\ \\vec{k}=(0,0,1)') + '។', 'Remember'))
    chk(lambda: (5 - 2 == 3, -1 - 3 == -4, 4 - (-2) == 6))
    C.append(mcq('easy', 's3', 'គេឱ្យ ' + M('A(2,3,-2)') + ' និង ' + M('B(5,-1,4)') + ' ។ កូអរដោនេនៃ ' + M('\\vec{AB}') + ' គឺ ៖',
                 M('(3,-4,6)'), [M('(7,2,2)'), M('(-3,4,-6)'), M('(3,2,6)')],
                 M('\\vec{AB}=(5-2,\\,-1-3,\\,4-(-2))=(3,-4,6)') + '។', 'Apply'))
    chk(lambda: ((2 + 4) / 2 == 3, (-1 + 5) / 2 == 2, (6 + 0) / 2 == 3))
    C.append(mcq('easy', 's3', 'ចំណុចកណ្តាលនៃអង្កត់ ' + M('AB') + ' ដែល ' + M('A(2,-1,6)') + ' និង ' + M('B(4,5,0)') + ' មានកូអរដោនេ ៖',
                 M('(3,2,3)'), [M('(2,6,-6)'), M('(6,4,6)'), M('(1,3,-3)')],
                 M('M=\\left(\\frac{2+4}{2},\\frac{-1+5}{2},\\frac{6+0}{2}\\right)=(3,2,3)') + '។', 'Apply'))
    chk(lambda: dot((2, -3, 1), (4, 1, -5)) == 0)
    C.append(mcq('easy', 's4', 'ផលគុណស្កាលែនៃ ' + M('\\vec{u}=(2,-3,1)') + ' និង ' + M('\\vec{v}=(4,1,-5)') + ' ស្មើប៉ុន្មាន ?',
                 M('0'), [M('10'), M('-6'), M('6')],
                 M('\\vec{u}\\cdot\\vec{v}=2(4)+(-3)(1)+1(-5)=8-3-5=0') + '។', 'Apply'))
    chk(lambda: close(norm((2, -3, 6)), 7))
    C.append(mcq('easy', 's5', 'ណមនៃវ៉ិចទ័រ ' + M('\\vec{u}=(2,-3,6)') + ' ស្មើប៉ុន្មាន ?',
                 M('7'), [M('5'), M('\\sqrt{11}'), M('49')],
                 M('|\\vec{u}|=\\sqrt{2^2+(-3)^2+6^2}=\\sqrt{4+9+36}=\\sqrt{49}=7') + '។', 'Apply'))
    chk(lambda: close(norm((2 - 1, 4 - 2, 5 - 3)), 2 * mp.sqrt(3) if False else mp.sqrt(1 + 4 + 4)))
    C.append(mcq('easy', 's5', 'ចម្ងាយរវាង ' + M('P(1,2,3)') + ' និង ' + M('Q(2,4,5)') + ' ស្មើប៉ុន្មាន ?',
                 M('3'), [M('\\sqrt{5}'), M('9'), M('2\\sqrt{3}')],
                 M('PQ=\\sqrt{(2-1)^2+(4-2)^2+(5-3)^2}=\\sqrt{1+4+4}=3') + '។', 'Apply'))

    # ============================================================ MCQ MEDIUM (14)
    chk(lambda: (2 * 1 - 3 * 0 == 2, 2 * (-1) - 3 * (-1) == 1, 2 * 5 - 3 * 6 == -8))
    C.append(mcq('medium', 's3', 'គេឱ្យ ' + M('\\vec{a}=(1,-1,5)') + ' និង ' + M('\\vec{b}=(0,-1,6)') + ' ។ កូអរដោនេនៃ ' + M('2\\vec{a}-3\\vec{b}') + ' គឺ ៖',
                 M('(2,1,-8)'), [M('(2,-5,-8)'), M('(2,1,28)'), M('(1,0,-1)')],
                 M('2\\vec{a}-3\\vec{b}=(2,-2,10)-(0,-3,18)=(2,1,-8)') + '។', 'Apply'))
    C.append(mcq('medium', 's2', 'រក ' + M('\\vec{x}') + ' ដែលផ្ទៀងផ្ទាត់ ' + M('3(\\vec{a}+\\vec{x})=2(\\vec{x}-3\\vec{b})') + ' ៖',
                 M('\\vec{x}=-3\\vec{a}-6\\vec{b}'), [M('\\vec{x}=3\\vec{a}-6\\vec{b}'), M('\\vec{x}=-3\\vec{a}+6\\vec{b}'), M('\\vec{x}=-\\frac35\\vec{a}-\\frac65\\vec{b}')],
                 M('3\\vec{a}+3\\vec{x}=2\\vec{x}-6\\vec{b}\\implies\\vec{x}=-3\\vec{a}-6\\vec{b}') + '។', 'Apply'))
    C.append(mcq('medium', 's2', 'ក្នុងត្រីកោណ ' + M('PQR') + ' មាន ' + M('M,N') + ' ជាចំណុចកណ្តាលនៃ ' + M('PQ') + ' និង ' + M('PR') + ' ។ ទំនាក់ទំនងត្រឹមត្រូវគឺ ៖',
                 M('\\vec{MN}=\\frac12\\vec{QR}'), [M('\\vec{MN}=2\\vec{QR}'), M('\\vec{MN}=-\\frac12\\vec{QR}'), M('\\vec{MN}=\\vec{QR}')],
                 'តាមលក្ខណៈបន្ទាត់កណ្តាលត្រីកោណ ' + M('MN\\parallel QR') + ' និង ' + M('MN=\\frac12 QR') + ' ទិសដៅដូចគ្នា ដូច្នេះ ' + M('\\vec{MN}=\\frac12\\vec{QR}') + '។', 'Understand'))
    C.append(mcq('medium', 's2', 'វ៉ិចទ័រឯកតាដែលមានទិសដៅដូច ' + M('\\vec{u}=(3,0,-4)') + ' គឺ ៖',
                 M('\\left(\\frac35,0,-\\frac45\\right)'), [M('\\left(\\frac37,0,-\\frac47\\right)'), M('(3,0,-4)'), M('\\left(-\\frac35,0,\\frac45\\right)')],
                 M('|\\vec{u}|=\\sqrt{9+0+16}=5') + ' ដូច្នេះ ' + M('\\frac{\\vec{u}}{|\\vec{u}|}=\\left(\\frac35,0,-\\frac45\\right)') + '។', 'Apply'))
    chk(lambda: (-4 * 2 + 0 * 0 + 2 * (-1) == -10))
    C.append(mcq('medium', 's4', 'មុំរវាង ' + M('\\vec{u}=(-4,0,2)') + ' និង ' + M('\\vec{v}=(2,0,-1)') + ' ស្មើប៉ុន្មាន ?',
                 M('\\pi'), [M('0'), M('\\frac{\\pi}{2}'), M('\\frac{\\pi}{3}')],
                 M('\\cos\\theta=\\frac{-8+0-2}{\\sqrt{20}\\sqrt{5}}=-1\\implies\\theta=\\pi') + '។', 'Apply'))
    chk(lambda: (2 * 1 + 4 * (-1) + 5 * (-2) != 0 and 1 * 1 + (-1) * (-1) + (-2) * (-2) == 6))
    C.append(mcq('medium', 's4', 'ត្រីកោណសម័ង្ស ' + M('ABC') + ' មានជ្រុង ' + M('a') + ' ។ គណនា ' + M('\\vec{AB}\\cdot\\vec{BC}') + ' ៖',
                 M('-\\frac12a^2'), [M('\\frac12a^2'), M('a^2'), M('-a^2')],
                 'មុំរវាង ' + M('\\vec{AB}') + ' និង ' + M('\\vec{BC}') + ' គឺ ' + M('180^\\circ-60^\\circ=120^\\circ') + ' ដូច្នេះ ' + M('a\\cdot a\\cos120^\\circ=-\\frac12a^2') + '។', 'Analyze'))
    chk(lambda: (1 * (1 + 2) + (-1) * (2 * 2 - 1) + 2 * (2 - 2) == 0))
    C.append(mcq('medium', 's4', 'គេឱ្យ ' + M('\\vec{u}=(1,-1,2)') + ' និង ' + M('\\vec{v}=(-1,-2,1)') + ' ។ រក ' + M('l') + ' ដើម្បីឱ្យ ' + M('(\\vec{u}-l\\vec{v})\\perp\\vec{u}') + ' ៖',
                 M('l=2'), [M('l=-2'), M('l=1'), M('l=3')],
                 M('(\\vec{u}-l\\vec{v})\\cdot\\vec{u}=|\\vec{u}|^2-l(\\vec{v}\\cdot\\vec{u})=6-3l=0\\implies l=2') + '។', 'Apply'))
    chk(lambda: (dot((2 - 0, 1 - 1, 3 - 0), (0 - 0, 2 - 1, 1 - 0)) if False else dot((0 - 2, 2 - 1, 1 - 0), (0 - 2, -1 - 1, 4 - 0)) == 6))
    C.append(mcq('medium', 's4', 'គេឱ្យ ' + M('A(2,1,0),\\ B(0,2,1),\\ C(0,-1,4)') + ' ។ មុំ ' + M('(\\vec{AB},\\vec{AC})') + ' ស្មើប៉ុន្មាន ?',
                 M('60^\\circ'), [M('30^\\circ'), M('45^\\circ'), M('90^\\circ')],
                 M('\\vec{AB}=(-2,1,1),\\ \\vec{AC}=(-2,-2,4)') + ' ; ' + M('\\cos\\theta=\\frac{4-2+4}{\\sqrt{6}\\sqrt{24}}=\\frac{6}{12}=\\frac12\\implies\\theta=60^\\circ') + '។', 'Apply'))
    chk(lambda: (norm((-2, 6, 9)) == 11))
    C.append(mcq('medium', 's5', 'ទិសដៅកូស៊ីនុសនៃ ' + M('\\vec{OP}') + ' ដែល ' + M('P(-2,6,9)') + ' គឺ ៖',
                 M('\\left(-\\frac{2}{11},\\frac{6}{11},\\frac{9}{11}\\right)'),
                 [M('\\left(\\frac{2}{11},-\\frac{6}{11},\\frac{9}{11}\\right)'), M('\\left(-\\frac{2}{13},\\frac{6}{13},\\frac{9}{13}\\right)'), M('(-2,6,9)')],
                 M('|\\vec{OP}|=\\sqrt{4+36+81}=11') + ' ដូច្នេះ ' + M('\\cos\\alpha=-\\frac{2}{11},\\ \\cos\\beta=\\frac{6}{11},\\ \\cos\\gamma=\\frac{9}{11}') + '។', 'Apply'))
    chk(lambda: close(0.6**2 + 0.8**2 + 0**2, 1))
    C.append(mcq('medium', 's5', 'បើវ៉ិចទ័រមួយមានទិសដៅកូស៊ីនុស ' + M('\\cos\\alpha=\\frac35') + ' និង ' + M('\\cos\\beta=\\frac45') + ' នោះ ' + M('\\cos\\gamma') + ' ស្មើប៉ុន្មាន ?',
                 M('0'), [M('\\frac15'), M('\\pm\\frac15'), M('1')],
                 M('\\cos^2\\alpha+\\cos^2\\beta+\\cos^2\\gamma=1\\implies\\frac{9}{25}+\\frac{16}{25}+\\cos^2\\gamma=1\\implies\\cos\\gamma=0') + '។', 'Apply'))
    chk(lambda: close(2 * (mp.mpf(-1) / 7 - 1) - 2 + 5 * (mp.mpf(-1) / 7 + 1), 0))
    C.append(mcq('medium', 's4', 'គេឱ្យ ' + M('\\vec{u}=(2,-1,5)') + ' និង ' + M('\\vec{w}=(z-1,2,z+1)') + ' ។ រក ' + M('z') + ' ដើម្បីឱ្យ ' + M('\\vec{u}\\perp\\vec{w}') + ' ៖',
                 M('z=-\\frac17'), [M('z=\\frac17'), M('z=1'), M('z=-\\frac37')],
                 M('2(z-1)-1(2)+5(z+1)=7z+1=0\\implies z=-\\frac17') + '។', 'Apply'))
    chk(lambda: (norm((0 - 0, 1 - 3, -2 - 0)) == norm((2 - 0, 3 - 1, -2 - (-2))) == norm((2 - 0, 3 - 3, -2 - 0))))
    C.append(mcq('medium', 's5', 'គេឱ្យ ' + M('A(0,3,0),\\ B(0,1,-2),\\ C(2,3,-2)') + ' ។ តើ ' + M('\\triangle ABC') + ' ជាត្រីកោណប្រភេទណា ?',
                 'ត្រីកោណសម័ង្ស', ['ត្រីកោណកែង', 'ត្រីកោណសមបាតមិនសម័ង្ស', 'ត្រីកោណសាមញ្ញ'],
                 M('AB=BC=AC=\\sqrt{8}=2\\sqrt{2}') + ' ដូច្នេះជាត្រីកោណសម័ង្ស។', 'Analyze'))
    chk(lambda: close(dot((1 + mp.sqrt(2), mp.sqrt(3), 0), (1 - mp.sqrt(2), 0, -1)), -1))
    C.append(mcq('medium', 's4', 'គណនា ' + M('\\vec{u}\\cdot\\vec{v}') + ' ដែល ' + M('\\vec{u}=(1+\\sqrt2)\\vec{i}+\\sqrt3\\vec{j}') + ' និង ' + M('\\vec{v}=(1-\\sqrt2)\\vec{i}-\\vec{k}') + ' ៖',
                 M('-1'), [M('1'), M('3'), M('1-\\sqrt2')],
                 M('\\vec{u}\\cdot\\vec{v}=(1+\\sqrt2)(1-\\sqrt2)+\\sqrt3(0)+0(-1)=1-2=-1') + '។', 'Apply'))
    C.append(with_img(mcq('medium', 's3', 'ក្នុងរូបតម្រុយ ' + M('Oxyz') + ' ចំណោលកែងនៃចំណុច ' + M('P(x,y,z)') + ' លើប្លង់ ' + M('xOy') + ' គឺ ' + M('H') + ' ។ ចម្ងាយ ' + M('OH') + ' ស្មើនឹង ៖',
                          M('\\sqrt{x^2+y^2}'), [M('\\sqrt{x^2+y^2+z^2}'), M('|z|'), M('x+y')],
                          M('H=(x,y,0)') + ' ដូច្នេះ ' + M('OH=\\sqrt{x^2+y^2}') + '។', 'Understand'), fig_axes_p()))

    # ============================================================ MCQ HARD (7)
    chk(lambda: (2 * (-12) + 4 * (-3) + 36 == 0 and close(2 * (-12) + 16 + 6 * (mp.mpf(4) / 3), 0) and close(4 + 4 * (-3) + 6 * (mp.mpf(4) / 3), 0)))
    C.append(mcq('hard', 's4', 'បីវ៉ិចទ័រ ' + M('\\vec{u}=(x,4,6),\\ \\vec{v}=(2,y,6),\\ \\vec{w}=(2,4,z)') + ' កែងគ្នាពីរៗ ។ រក ' + M('(x,y,z)') + ' ៖',
                 M('(-12,\\,-3,\\,\\frac43)'), [M('(12,-3,\\frac43)'), M('(-12,3,-\\frac43)'), M('(-6,-3,\\frac23)')],
                 'ពី ' + M('\\vec{u}\\cdot\\vec{v}=0,\\ \\vec{u}\\cdot\\vec{w}=0,\\ \\vec{v}\\cdot\\vec{w}=0') + ' បាន ' + M('2x+4y=-36,\\ 2x+6z=-16,\\ 4y+6z=-4') + ' ដោះស្រាយបាន ' + M('x=-12,y=-3,z=\\frac43') + '។', 'Analyze'))
    chk(lambda: (dot((1, 2, -3), (7, 4, 5)) == 0 and dot((2, -1, -2), (7, 4, 5)) == 0 and dot((1, -3, 1), (7, 4, 5)) == 0))
    C.append(mcq('hard', 's4', 'បើ ' + M('\\vec{x}=(x_1,x_2,x_3)\\ne\\vec{0}') + ' កែងនឹង ' + M('\\vec{u}=(1,2,-3)') + ' និង ' + M('\\vec{v}=(2,-1,-2)') + ' នោះផលធៀប ' + M('x_1:x_2:x_3') + ' គឺ ៖',
                 M('7:4:5'), [M('7:-4:5'), M('5:4:7'), M('1:2:3')],
                 'ដោះស្រាយ ' + M('x_1+2x_2-3x_3=0') + ' និង ' + M('2x_1-x_2-2x_3=0') + ' បាន ' + M('x_1=\\frac75 x_3,\\ x_2=\\frac45 x_3') + ' ដូច្នេះ ' + M('7:4:5') + '។', 'Analyze'))
    C.append(with_img(mcq('hard', 's4', 'ពីរ៉ាមីតការេ ' + M('SABCD') + ' មានទ្រនុងទាំងអស់ប្រវែង ' + M('a') + ' ។ គណនា ' + M('\\vec{SA}\\cdot\\vec{AC}') + ' ៖',
                          M('-a^2'), [M('a^2'), M('0'), M('-\\frac12a^2')],
                          M('AC=a\\sqrt2') + ' និង ' + M('SA^2+SC^2=2a^2=AC^2\\implies\\vec{SA}\\cdot\\vec{SC}=0') + ' ; ដូច្នេះ ' + M('\\vec{SA}\\cdot\\vec{AC}=\\vec{SA}\\cdot(\\vec{SC}-\\vec{SA})=-a^2') + '។', 'Analyze'), fig_pyramid()))
    C.append(with_img(mcq('hard', 's4', 'ក្នុងគូប ' + M('ABCD\\text{-}EFGH') + ' ជ្រុង ' + M('a') + ' គណនា ' + M('\\vec{DE}\\cdot\\vec{FC}') + ' ៖',
                          M('-2a^2'), [M('2a^2'), M('0'), M('-a^2')],
                          M('\\vec{DE}=\\vec{CF}=-\\vec{FC}') + ' ដែល ' + M('FC=a\\sqrt2') + ' ដូច្នេះ ' + M('\\vec{DE}\\cdot\\vec{FC}=-|\\vec{FC}|^2=-2a^2') + '។', 'Analyze'), fig_cube()))
    chk(lambda: (dot((2, -2, 1), (2, 3, -4)) == -6 and norm2((2, -2, 1)) == 9))
    C.append(mcq('hard', 's4', 'គេឱ្យ ' + M('\\vec{u}=(2,-2,1)') + ' និង ' + M('\\vec{v}=(2,3,-4)') + ' ។ បើ ' + M('\\vec{w}=\\vec{v}-k\\vec{u}') + ' កែងនឹង ' + M('\\vec{u}') + ' នោះ ' + M('\\vec{w}') + ' គឺ ៖',
                 M('\\left(\\frac{10}{3},\\frac53,-\\frac{10}{3}\\right)'),
                 [M('\\left(\\frac23,\\frac{13}{3},-\\frac{14}{3}\\right)'), M('\\left(\\frac{10}{3},-\\frac53,-\\frac{10}{3}\\right)'), M('(4,1,-3)')],
                 M('k=\\frac{\\vec{u}\\cdot\\vec{v}}{|\\vec{u}|^2}=\\frac{-6}{9}=-\\frac23') + ' ដូច្នេះ ' + M('\\vec{w}=\\vec{v}+\\frac23\\vec{u}=\\left(\\frac{10}{3},\\frac53,-\\frac{10}{3}\\right)') + '។', 'Apply'))
    C.append(mcq('hard', 's2', 'ប្រលេពីប៉ែត ' + M('OADB\\text{-}CEFG') + ' តាង ' + M('\\vec{OA}=\\vec{a},\\vec{OB}=\\vec{b},\\vec{OC}=\\vec{c}') + ' ហើយ ' + M('P') + ' ជាចំណុចប្រសព្វអង្កត់ទ្រូងបាត ' + M('CEFG') + ' ។ វ៉ិចទ័រ ' + M('\\vec{PD}') + ' គឺ ៖',
                 M('\\frac12\\vec{a}+\\frac12\\vec{b}-\\vec{c}'),
                 [M('\\frac12\\vec{a}+\\frac12\\vec{b}+\\vec{c}'), M('\\vec{a}+\\vec{b}-\\vec{c}'), M('-\\frac12\\vec{a}-\\frac12\\vec{b}+\\vec{c}')],
                 M('\\vec{OP}=\\vec{c}+\\frac12(\\vec{a}+\\vec{b})') + ' និង ' + M('\\vec{OD}=\\vec{a}+\\vec{b}') + ' ដូច្នេះ ' + M('\\vec{PD}=\\vec{OD}-\\vec{OP}=\\frac12\\vec{a}+\\frac12\\vec{b}-\\vec{c}') + '។', 'Analyze'))
    chk(lambda: (dot((1, 1, 0), (1, 0, 1)) == 1))
    C.append(mcq('hard', 's3', 'បើ ' + M('\\vec{p}=(5,6,7)=l(1,1,0)+m(1,0,1)+n(0,1,1)') + ' នោះ ' + M('(l,m,n)') + ' ស្មើនឹង ៖',
                 M('(2,3,4)'), [M('(3,2,4)'), M('(2,4,3)'), M('(1,4,5)')],
                 M('l+m=5,\\ l+n=6,\\ m+n=7\\implies l+m+n=9\\implies l=2,m=3,n=4') + '។', 'Apply'))

    # ============================================================ MCQ PISA (5)
    chk(lambda: close(norm((6, 8, 24)), 26))
    C.append(with_img(mcq('pisa', 'p_drone', 'ដ្រូនមួយហោះពីទីតាំង ' + M('O(0,0,0)') + ' ទៅកាន់ ' + M('P(6,8,24)') + ' (ឯកតាគិតជាម៉ែត្រ) ។ ចម្ងាយហោះត្រង់ ' + M('OP') + ' ស្មើប៉ុន្មានម៉ែត្រ ?',
                          M('26\\text{ m}'), [M('38\\text{ m}'), M('24\\text{ m}'), M('10\\text{ m}')],
                          M('OP=\\sqrt{6^2+8^2+24^2}=\\sqrt{36+64+576}=\\sqrt{676}=26\\text{ m}') + '។', 'Apply'), fig_drone()))
    chk(lambda: close(mp.mpf(24) / 26, mp.mpf(12) / 13))
    C.append(mcq('pisa', 'p_drone', 'ដ្រូនហោះតាមវ៉ិចទ័រ ' + M('\\vec{OP}=(6,8,24)') + ' ។ ទិសដៅកូស៊ីនុសធៀបនឹងអ័ក្សឈរ ' + M('Oz') + ' (' + M('\\cos\\gamma') + ') ស្មើប៉ុន្មាន ?',
                 M('\\frac{12}{13}'), [M('\\frac{3}{13}'), M('\\frac{4}{13}'), M('\\frac{5}{13}')],
                 M('|\\vec{OP}|=26') + ' ដូច្នេះ ' + M('\\cos\\gamma=\\frac{24}{26}=\\frac{12}{13}') + '។', 'Apply'))
    chk(lambda: (dot((30, 40, 120), (2, 1, 1)) == 60 + 40 + 120 == 220))
    C.append(mcq('pisa', 'p_force', 'កម្លាំង ' + M('\\vec{F}=(30,40,120)\\text{ N}') + ' បន្លាស់ទីវត្ថុមួយតាមវ៉ិចទ័រ ' + M('\\vec{d}=(2,1,1)\\text{ m}') + ' ។ កម្មន្ត ' + M('W=\\vec{F}\\cdot\\vec{d}') + ' ស្មើប៉ុន្មានហ្ស៊ូល ?',
                 M('220\\text{ J}'), [M('190\\text{ J}'), M('130\\text{ J}'), M('260\\text{ J}')],
                 M('W=30(2)+40(1)+120(1)=60+40+120=220\\text{ J}') + '។', 'Apply'))
    chk(lambda: (dot((1, 2, -2), (-2, 1, 0)) == 0))
    C.append(mcq('pisa', 'p_roof', 'សសរទ្រទ្រង់ពីរមានទិសដៅ ' + M('\\vec{u}=(1,2,-2)') + ' និង ' + M('\\vec{v}=(-2,1,k)') + ' ។ តើ ' + M('k') + ' ត្រូវស្មើប៉ុន្មាន ដើម្បីឱ្យសសរទាំងពីរកែងគ្នា ?',
                 M('k=0'), [M('k=2'), M('k=-2'), M('k=1')],
                 M('\\vec{u}\\cdot\\vec{v}=1(-2)+2(1)-2k=-2k=0\\implies k=0') + '។', 'Evaluate'))
    chk(lambda: close(norm((4 - 1, -2 - 2, 12 - 0)), 13))
    C.append(mcq('pisa', 'p_nav', 'ឧបករណ៍រ៉ាដាចាប់បានយន្តហោះត្រង់ ' + M('A(1,2,0)') + ' និងក្រោយ ១ នាទីត្រង់ ' + M('B(4,-2,12)') + ' (គិតជាគីឡូម៉ែត្រ) ។ ចម្ងាយផ្លាស់ទី ' + M('AB') + ' គឺ ៖',
                 M('13\\text{ km}'), [M('15\\text{ km}'), M('11\\text{ km}'), M('17\\text{ km}')],
                 M('\\vec{AB}=(3,-4,12)\\implies AB=\\sqrt{9+16+144}=\\sqrt{169}=13\\text{ km}') + '។', 'Apply'))

    C.extend(cands_writing())
    return C


def cands_writing():
    C = []
    # ============================================================ WRITING EASY (1)
    chk(lambda: (3 * (-2) - 4 * 0 == -6 if False else (3 * 2 - 4 * (-3) == 18 and 3 * (-3) - 4 * 2 == -17 and 3 * 0 - 4 * 5 == -20)))
    C.append(wr('easy', 's3', 'គេឱ្យ ' + M('\\vec{a}=(2,-3,0)') + ' និង ' + M('\\vec{b}=(-3,2,5)') + ' ។ គណនាកូអរដោនេនៃ ' + M('\\vec{u}=3\\vec{a}-4\\vec{b}') + ' ។',
                [(M('3\\vec{a}=(6,-9,0)'), 1),
                 (M('4\\vec{b}=(-12,8,20)'), 2),
                 (M('\\vec{u}=(6-(-12),\\,-9-8,\\,0-20)=(18,-17,-20)'), 2)], bloom='Apply'))

    # ============================================================ WRITING MEDIUM (4)
    chk(lambda: (dot((1, -3, 1), (-3, -2, -3)) == 0))
    C.append(wr('medium', 's4', 'ក្នុងតម្រុយអរតូណរម៉ាល់ ' + M('(O,\\vec{i},\\vec{j},\\vec{k})') + ' គេឱ្យ ' + M('A(1,4,2),\\ B(2,1,3),\\ C(-2,2,-1)') + ' ។ បង្ហាញថា ' + M('\\vec{AC}\\perp\\vec{AB}') + ' ។',
                [(M('\\vec{AB}=(2-1,1-4,3-2)=(1,-3,1)'), 1),
                 (M('\\vec{AC}=(-2-1,2-4,-1-2)=(-3,-2,-3)'), 2),
                 (M('\\vec{AB}\\cdot\\vec{AC}=1(-3)+(-3)(-2)+1(-3)=-3+6-3=0\\implies\\vec{AC}\\perp\\vec{AB}'), 2)], bloom='Apply'))
    chk(lambda: close(norm((3, -4, 5)), 5 * mp.sqrt(2)))
    C.append(wr('medium', 's5', 'រកទិសដៅកូស៊ីនុសនៃវ៉ិចទ័រ ' + M('\\vec{u}=(3,-4,5)') + ' និងផ្ទៀងផ្ទាត់ ' + M('\\cos^2\\alpha+\\cos^2\\beta+\\cos^2\\gamma=1') + ' ។',
                [(M('|\\vec{u}|=\\sqrt{3^2+(-4)^2+5^2}=\\sqrt{50}=5\\sqrt2'), 1),
                 (M('\\cos\\alpha=\\frac{3\\sqrt2}{10},\\ \\cos\\beta=-\\frac{2\\sqrt2}{5},\\ \\cos\\gamma=\\frac{\\sqrt2}{2}'), 2),
                 (M('\\cos^2\\alpha+\\cos^2\\beta+\\cos^2\\gamma=\\frac{18}{100}+\\frac{32}{100}+\\frac{50}{100}=1'), 2)], bloom='Apply'))
    chk(lambda: (close(norm((0, 4, -4)), 4 * mp.sqrt(2)) and dot((0, 4, -4), (-4, 4, 0)) == 16))
    C.append(wr('medium', 's5', 'គេឱ្យ ' + M('M(3,1,5),\\ N(3,5,1),\\ P(-1,5,5)') + ' ។ ក. គណនា ' + M('MN,\\ MP') + ' និង ' + M('\\cos\\theta') + ' រវាង ' + M('\\vec{MN},\\vec{MP}') + ' ។ ខ. បញ្ជាក់ប្រភេទត្រីកោណ ' + M('MNP') + ' ។',
                [('ក. ' + M('\\vec{MN}=(0,4,-4)\\implies MN=4\\sqrt2') + ' ; ' + M('\\vec{MP}=(-4,4,0)\\implies MP=4\\sqrt2'), 2),
                 (M('\\vec{MN}\\cdot\\vec{MP}=16\\implies\\cos\\theta=\\frac{16}{32}=\\frac12\\implies\\theta=60^\\circ'), 2),
                 ('ខ. ដោយ ' + M('MN=MP') + ' និង ' + M('\\theta=60^\\circ') + ' នោះ ' + M('\\triangle MNP') + ' ជាត្រីកោណសម័ង្ស', 1)], bloom='Analyze'))
    C.append(wr('medium', 's2', 'ប្រលេពីប៉ែតកែង ' + M('ABCD\\text{-}EFGH') + ' តាង ' + M('\\vec{AB}=\\vec{a},\\vec{AD}=\\vec{b},\\vec{AE}=\\vec{c}') + ' ។ សរសេរ ' + M('\\vec{AG}') + ' និង ' + M('\\vec{FD}') + ' ជាអនុគមន៍នៃ ' + M('\\vec{a},\\vec{b},\\vec{c}') + ' ។',
                [(M('\\vec{AG}=\\vec{AB}+\\vec{BC}+\\vec{CG}=\\vec{a}+\\vec{b}+\\vec{c}'), 2),
                 (M('\\vec{FD}=\\vec{FE}+\\vec{EH}+\\vec{HD}=-\\vec{a}+\\vec{b}-\\vec{c}'), 3)], bloom='Understand'))

    # ============================================================ WRITING HARD (4)
    chk(lambda: (dot((2, -1, 4), (-4, 5, 3)) == -1))
    C.append(wr('hard', 's4', 'គេឱ្យ ' + M('\\vec{u}=(2,-1,4)') + ' និង ' + M('\\vec{v}=(-4,5,3)') + ' ។ កំណត់តម្លៃ ' + M('k') + ' ដែល ' + M('(\\vec{u}-k\\vec{v})\\perp\\vec{u}') + ' ។',
                [(M('(\\vec{u}-k\\vec{v})\\cdot\\vec{u}=|\\vec{u}|^2-k(\\vec{u}\\cdot\\vec{v})=0'), 2),
                 (M('|\\vec{u}|^2=4+1+16=21') + ' និង ' + M('\\vec{u}\\cdot\\vec{v}=-8-5+12=-1'), 2),
                 (M('21-k(-1)=0\\implies k=-21'), 1)], bloom='Apply'))
    C.append(with_img(wr('hard', 's4', 'ពីរ៉ាមីតការេ ' + M('SABCD') + ' មានទ្រនុងទាំងអស់ស្មើ ' + M('a') + ' ។ គណនា ក. ' + M('\\vec{SA}\\cdot\\vec{SB}') + ' ខ. ' + M('\\vec{SA}\\cdot\\vec{SC}') + ' គ. ' + M('\\vec{SA}\\cdot\\vec{AC}') + ' ។',
                         [('ក. ' + M('\\triangle SAB') + ' សម័ង្សជ្រុង ' + M('a\\implies\\vec{SA}\\cdot\\vec{SB}=a^2\\cos60^\\circ=\\frac12a^2'), 1),
                          ('ខ. ' + M('AC=a\\sqrt2') + ' និង ' + M('SA^2+SC^2=2a^2=AC^2\\implies\\vec{SA}\\cdot\\vec{SC}=0'), 2),
                          ('គ. ' + M('\\vec{SA}\\cdot\\vec{AC}=\\vec{SA}\\cdot(\\vec{SC}-\\vec{SA})=0-a^2=-a^2'), 2)], bloom='Analyze'), fig_pyramid()))
    C.append(wr('hard', 's4', 'រង្វង់ ' + M('C') + ' អង្កត់ផ្ចិត ' + M('AB') + ' ក្នុងប្លង់ ' + M('\\alpha') + ' ; បន្ទាត់ ' + M('L\\perp\\alpha') + ' ត្រង់ ' + M('A') + ' និង ' + M('P\\in L') + ' ។ បង្ហាញថា ' + M('\\forall M\\in C,\\ \\vec{PM}\\cdot\\vec{MB}=0') + ' ។',
                [(M('\\vec{PM}\\cdot\\vec{MB}=(\\vec{PA}+\\vec{AM})\\cdot\\vec{MB}=\\vec{PA}\\cdot\\vec{MB}+\\vec{AM}\\cdot\\vec{MB}'), 2),
                 ('ដោយ ' + M('L\\perp\\alpha\\implies PA\\perp MB\\implies\\vec{PA}\\cdot\\vec{MB}=0'), 1),
                 ('ដោយ ' + M('M') + ' លើរង្វង់អង្កត់ផ្ចិត ' + M('AB\\implies AM\\perp MB\\implies\\vec{AM}\\cdot\\vec{MB}=0') + ' ដូច្នេះ ' + M('\\vec{PM}\\cdot\\vec{MB}=0'), 2)], bloom='Evaluate'))
    C.append(wr('hard', 's3', 'បង្ហាញថា ' + M('\\vec{u}=(x,y,z)') + ' និង ' + M('\\vec{v}=(x\',y\',z\')') + ' កូលីនេអ៊ែរ លុះត្រាតែ ' + M('\\frac{x}{x\'}=\\frac{y}{y\'}=\\frac{z}{z\'}') + ' (ករណី ' + M('x\',y\',z\'\\ne0') + ') ។',
                [(M('\\vec{u}\\parallel\\vec{v}\\iff\\exists t\\in\\mathbb{R}:\\vec{u}=t\\vec{v}'), 2),
                 ('សមមូល ' + M('x=tx\',\\ y=ty\',\\ z=tz\'\\iff\\frac{x}{x\'}=\\frac{y}{y\'}=\\frac{z}{z\'}=t'), 3)], bloom='Understand'))

    # ============================================================ WRITING PISA (5)
    chk(lambda: (close(norm((6, 8, 24)), 26) and close(mp.mpf(24) / 26, mp.mpf(12) / 13)))
    C.append(with_img(wr('pisa', 'p_drone', 'ដ្រូនដឹកទំនិញហោះត្រង់ពី ' + M('O(0,0,0)') + ' ទៅ ' + M('P(6,8,24)') + ' (ម៉ែត្រ) ។ ក. គណនាចម្ងាយ ' + M('OP') + ' ។ ខ. គណនាកូស៊ីនុសមុំឡើងធៀបនឹងអ័ក្សឈរ ' + M('Oz') + ' ។ គ. បើល្បឿន ' + M('13\\text{ m/s}') + ' រកពេលហោះ។',
                         [('ក. ' + M('OP=\\sqrt{6^2+8^2+24^2}=\\sqrt{676}=26\\text{ m}'), 2),
                          ('ខ. ' + M('\\cos\\gamma=\\frac{24}{26}=\\frac{12}{13}'), 2),
                          ('គ. ' + M('t=\\frac{26}{13}=2\\text{ s}'), 1)], bloom='Apply'), fig_drone()))
    chk(lambda: (dot((30, 40, 120), (2, 1, 1)) == 220 and norm((30, 40, 120)) == 130))
    C.append(wr('pisa', 'p_force', 'កម្លាំង ' + M('\\vec{F}=(30,40,120)\\text{ N}') + ' ធ្វើឱ្យវត្ថុផ្លាស់ទីតាម ' + M('\\vec{d}=(2,1,1)\\text{ m}') + ' ។ ក. រកទំហំកម្លាំង ' + M('|\\vec{F}|') + ' ។ ខ. គណនាកម្មន្ត ' + M('W=\\vec{F}\\cdot\\vec{d}') + ' ។',
                [('ក. ' + M('|\\vec{F}|=\\sqrt{30^2+40^2+120^2}=\\sqrt{16900}=130\\text{ N}'), 2),
                 ('ខ. ' + M('W=30(2)+40(1)+120(1)=220\\text{ J}'), 3)], bloom='Apply'))
    chk(lambda: (dot((3, 4, 0), (0, 4, 3)) == 16 and norm((3, 4, 0)) == 5 and norm((0, 4, 3)) == 5))
    C.append(wr('pisa', 'p_roof', 'ដំបូលផ្ទះមានធ្នឹមពីរតាមទិស ' + M('\\vec{u}=(3,4,0)') + ' និង ' + M('\\vec{v}=(0,4,3)') + ' ។ ក. គណនា ' + M('\\cos\\theta') + ' នៃមុំរវាងធ្នឹមទាំងពីរ ។ ខ. តើធ្នឹមទាំងពីរកែងគ្នាឬទេ ?',
                [('ក. ' + M('|\\vec{u}|=5,\\ |\\vec{v}|=5,\\ \\vec{u}\\cdot\\vec{v}=16\\implies\\cos\\theta=\\frac{16}{25}=0{,}64'), 3),
                 ('ខ. ដោយ ' + M('\\vec{u}\\cdot\\vec{v}=16\\ne0') + ' ធ្នឹមទាំងពីរមិនកែងគ្នាទេ', 2)], bloom='Analyze'))
    chk(lambda: (norm((4 - 1, -2 - 2, 12 - 0)) == 13))
    C.append(wr('pisa', 'p_nav', 'រ៉ាដាចាប់យន្តហោះត្រង់ ' + M('A(1,2,0)') + ' ហើយក្រោយ ' + M('50\\text{ s}') + ' ត្រង់ ' + M('B(4,-2,12)') + ' (គិតជា ' + M('\\text{km}') + ') ។ គណនាវ៉ិចទ័រ ' + M('\\vec{AB}') + ' និងល្បឿនមធ្យមគិតជា ' + M('\\text{m/s}') + ' ។',
                [(M('\\vec{AB}=(3,-4,12)\\text{ km}'), 1),
                 (M('AB=\\sqrt{9+16+144}=13\\text{ km}=13000\\text{ m}'), 2),
                 (M('v=\\frac{13000}{50}=260\\text{ m/s}'), 2)], bloom='Apply'))
    chk(lambda: (dot((2, -2, 1), (1, 2, 2)) == 0))
    C.append(with_img(wr('pisa', 'p_cube', 'ប្រព័ន្ធកាមេរ៉ាដាក់តាមខ្សែ ' + M('\\vec{u}=(2,-2,1)') + ' និងបង្គោលភ្លើងតាម ' + M('\\vec{v}=(1,2,2)') + ' ។ បង្ហាញថាទិសទាំងពីរកែងគ្នា និងរកប្រវែងវ៉ិចទ័រទាំងពីរ។',
                         [(M('\\vec{u}\\cdot\\vec{v}=2(1)+(-2)(2)+1(2)=2-4+2=0\\implies\\vec{u}\\perp\\vec{v}'), 3),
                          (M('|\\vec{u}|=\\sqrt{4+4+1}=3,\\ |\\vec{v}|=\\sqrt{1+4+4}=3'), 2)], bloom='Evaluate'), fig_cube()))
    return C


def verify():
    mp.mp.dps = 30
    CNT[0] = 0
    cands()
    return CNT[0]
