# -*- coding: utf-8 -*-
"""
KhmerMath Question Bank: Grade 12 Science (SC)
Chapter 5: វ៉ិចទ័រក្នុងលំហ
Lesson 2: ផលគុណនៃពីរវ៉ិចទ័រក្នុងលំហ
Reference textbook: Lesson/G12/SC/C5-L2.tex
Matrix: MCQ easy10/medium14/hard7/pisa5 + writing easy1/medium4/hard4/pisa5 = 50, Bloom on each.
Cross products, triple scalar products, areas, volumes, and torque are checked numerically.
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.dirname(__file__))
from lib import *
import mpmath as mp
import G12L04 as P
from G12L07 import close

LESSON = 'ផលគុណនៃពីរវ៉ិចទ័រក្នុងលំហ'
CHAPTER = 'ជំពូកទី 5 : វ៉ិចទ័រក្នុងលំហ'
GRADE = '12SC'
TARGET = P.TARGET

S1 = 'និយមន័យនិងលក្ខណៈផលគុណវ៉ិចទ័រ'
S2 = 'បំណកស្រាយធរណីមាត្រ និងផ្ទៃក្រឡា'
S3 = 'អនុវត្តន៍ក្នុងរូបវិទ្យា (ម៉ូម៉ង់នៃកម្លាំង)'
S4 = 'ផលគុណចម្រុះ និងមាឌប្រលេពីប៉ែត'
TOPIC_MAP = {'s1': S1, 's2': S2, 's3': S3, 's4': S4,
             'p_torque': S3, 'p_solar': S2, 'p_roof': S2, 'p_box': S4, 'p_wrench': S3}
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


def cross(u, v):
    return (u[1] * v[2] - u[2] * v[1],
            u[2] * v[0] - u[0] * v[2],
            u[0] * v[1] - u[1] * v[0])


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


def fig_para():
    s = [f'<polygon points="50,155 190,155 240,95 100,95" fill="#dbeafe" stroke="#2563eb" stroke-width="1.6"/>']
    s.append(_line(50, 155, 50, 40, '#0d9488', 2.2))
    s.append(_dot(50, 155, 3, '#0f172a'))
    s.append(_text(120, 172, 'u', 12, '#1d4ed8', 'middle', True))
    s.append(_text(66, 122, 'v', 12, '#dc2626', 'middle', True))
    s.append(_text(56, 36, 'u × v', 12, '#0d9488', 'start', True))
    s.append(_text(86, 146, 'θ', 12, '#334155'))
    return _svg(280, 195, ''.join(s))


def fig_torque():
    s = []
    P, Q = (65, 145), (205, 125)
    s.append(_line(P[0], P[1], Q[0], Q[1], '#2563eb', 2.2))
    s.append(_line(Q[0], Q[1], 240, 65, '#dc2626', 2.2))
    s.append(_line(P[0], P[1], P[0], 35, '#0d9488', 2.2))
    s.append(_dot(P[0], P[1], 3.5, '#0f172a'))
    s.append(_dot(Q[0], Q[1], 3.5, '#0f172a'))
    s.append(_text(55, 158, 'P', 12, '#0f172a', 'middle', True))
    s.append(_text(215, 138, 'Q', 12, '#0f172a', 'middle', True))
    s.append(_text(135, 150, 'PQ', 11, '#2563eb', 'middle', True))
    s.append(_text(246, 62, 'F', 12, '#dc2626', 'start', True))
    s.append(_text(72, 35, 'M = PQ × F', 11, '#0d9488', 'start', True))
    return _svg(290, 185, ''.join(s))


def fig_box():
    s = []
    O, V, W, VW = (50, 160), (175, 160), (105, 115), (230, 115)
    U, UV, UW, UVW = (80, 75), (205, 75), (135, 30), (260, 30)
    for p, q in ((O, W), (W, VW), (W, UW)):
        s.append(_line(p[0], p[1], q[0], q[1], '#94a3b8', 1.3, '4,4'))
    for p, q in ((O, V), (V, VW), (U, UV), (UV, UVW), (UVW, UW), (UW, U), (V, UV), (VW, UVW), (O, U)):
        s.append(_line(p[0], p[1], q[0], q[1], '#2563eb', 1.7))
    s.append(_text(115, 176, 'v', 12, '#1d4ed8', 'middle', True))
    s.append(_text(66, 134, 'w', 12, '#dc2626', 'middle', True))
    s.append(_text(52, 114, 'u', 12, '#0d9488', 'middle', True))
    return _svg(295, 195, ''.join(s))


def cands():
    C = []
    # ============================================================ MCQ EASY (10)
    C.append(mcq('easy', 's1', 'ចំពោះវ៉ិចទ័រឯកតា ' + M('\\vec{i},\\vec{j},\\vec{k}') + ' ផលគុណ ' + M('\\vec{i}\\times\\vec{j}') + ' ស្មើនឹង ៖',
                 M('\\vec{k}'), [M('-\\vec{k}'), M('\\vec{0}'), M('1')],
                 M('\\vec{i}\\times\\vec{j}=\\vec{k}') + ' តាមវដ្តវិជ្ជមាន។', 'Remember'))
    C.append(mcq('easy', 's1', 'ផលគុណ ' + M('\\vec{j}\\times\\vec{i}') + ' ស្មើនឹង ៖',
                 M('-\\vec{k}'), [M('\\vec{k}'), M('\\vec{i}'), M('\\vec{0}')],
                 M('\\vec{j}\\times\\vec{i}=-(\\vec{i}\\times\\vec{j})=-\\vec{k}') + '។', 'Remember'))
    C.append(mcq('easy', 's1', 'ចំពោះវ៉ិចទ័រ ' + M('\\vec{u}') + ' ណាមួយ ' + M('\\vec{u}\\times\\vec{u}') + ' ស្មើនឹង ៖',
                 M('\\vec{0}'), [M('0'), M('|\\vec{u}|^2'), M('2\\vec{u}')],
                 'វ៉ិចទ័រទាំងពីរមានទិសដៅដូចគ្នា (' + M('\\theta=0') + ') ដូច្នេះ ' + M('\\vec{u}\\times\\vec{u}=\\vec{0}') + '។', 'Remember'))
    C.append(mcq('easy', 's1', 'លក្ខណៈប្រឆាំងឆ្លុះនៃផលគុណវ៉ិចទ័រគឺ ៖',
                 M('\\vec{u}\\times\\vec{v}=-(\\vec{v}\\times\\vec{u})'),
                 [M('\\vec{u}\\times\\vec{v}=\\vec{v}\\times\\vec{u}'), M('\\vec{u}\\times\\vec{v}=\\vec{0}'), M('|\\vec{u}\\times\\vec{v}|=-|\\vec{v}\\times\\vec{u}|')],
                 'ប្តូរលំដាប់វ៉ិចទ័រ ផលគុណវ៉ិចទ័រផ្លាស់ប្តូរសញ្ញា។', 'Remember'))
    C.append(with_img(mcq('easy', 's2', 'ដូចក្នុងរូប វ៉ិចទ័រ ' + M('\\vec{u}\\times\\vec{v}') + ' មានទិសយ៉ាងណាធៀបនឹង ' + M('\\vec{u}') + ' និង ' + M('\\vec{v}') + ' ?',
                          'កែងនឹង ' + M('\\vec{u}') + ' ផង និងកែងនឹង ' + M('\\vec{v}') + ' ផង',
                          ['ស្របនឹង ' + M('\\vec{u}'), 'ស្របនឹង ' + M('\\vec{v}'), 'ស្មើនឹង ' + M('\\vec{0}') + ' ជានិច្ច'],
                          M('(\\vec{u}\\times\\vec{v})\\cdot\\vec{u}=0') + ' និង ' + M('(\\vec{u}\\times\\vec{v})\\cdot\\vec{v}=0') + '។', 'Understand'), fig_para()))
    C.append(mcq('easy', 's2', 'ណមនៃផលគុណវ៉ិចទ័រ ' + M('|\\vec{u}\\times\\vec{v}|') + ' កំណត់ដោយ ៖',
                 M('|\\vec{u}||\\vec{v}|\\sin\\theta'), [M('|\\vec{u}||\\vec{v}|\\cos\\theta'), M('|\\vec{u}||\\vec{v}|\\tan\\theta'), M('\\frac12|\\vec{u}||\\vec{v}|\\sin\\theta')],
                 M('|\\vec{u}\\times\\vec{v}|=|\\vec{u}||\\vec{v}|\\sin\\theta') + ' ដែល ' + M('\\theta') + ' ជាមុំរវាង ' + M('\\vec{u}') + ' និង ' + M('\\vec{v}') + '។', 'Remember'))
    C.append(mcq('easy', 's2', 'បើ ' + M('\\vec{u}\\times\\vec{v}=\\vec{0}') + ' នោះ ' + M('\\vec{u}') + ' និង ' + M('\\vec{v}') + ' ៖',
                 'កូលីនេអ៊ែរនឹងគ្នា', ['កែងគ្នា', 'មានប្រវែងស្មើគ្នា', 'មិនអាចប្រៀបធៀបបាន'],
                 M('\\sin\\theta=0\\implies\\theta=0') + ' ឬ ' + M('\\pi') + ' គឺ ' + M('\\vec{u}') + ' និង ' + M('\\vec{v}') + ' កូលីនេអ៊ែរនឹងគ្នា។', 'Understand'))
    chk(lambda: cross((0, 1, 0), (0, 1, 1)) == (1, 0, 0))
    C.append(mcq('easy', 's2', 'ផ្ទៃក្រឡាប្រលេឡូក្រាមសង់លើ ' + M('\\vec{u}=\\vec{j}') + ' និង ' + M('\\vec{v}=\\vec{j}+\\vec{k}') + ' ស្មើនឹង ៖',
                 M('1'), [M('2'), M('\\sqrt2'), M('0')],
                 M('\\vec{u}\\times\\vec{v}=\\vec{j}\\times(\\vec{j}+\\vec{k})=\\vec{i}') + ' ដូច្នេះផ្ទៃក្រឡា ' + M('|\\vec{i}|=1') + '។', 'Apply'))
    chk(lambda: dot((1, 0, 0), cross((0, 1, 0), (0, 0, 1))) == 1)
    C.append(mcq('easy', 's4', 'ផលគុណចម្រុះ ' + M('\\vec{i}\\cdot(\\vec{j}\\times\\vec{k})') + ' ស្មើប៉ុន្មាន ?',
                 M('1'), [M('0'), M('-1'), M('3')],
                 M('\\vec{j}\\times\\vec{k}=\\vec{i}\\implies\\vec{i}\\cdot\\vec{i}=1') + '។', 'Apply'))
    C.append(mcq('easy', 's4', 'បើ ' + M('\\vec{u}\\cdot(\\vec{v}\\times\\vec{w})=0') + ' នោះវ៉ិចទ័រ ' + M('\\vec{u},\\vec{v},\\vec{w}') + ' ៖',
                 'ស្ថិតក្នុងប្លង់តែមួយ', ['កែងគ្នាពីរៗ', 'កូលីនេអ៊ែរទាំងបី', 'មានណមស្មើ ០'],
                 'មាឌប្រលេពីប៉ែតស្មើ ០ មានន័យថាវ៉ិចទ័រទាំងបីស្ថិតក្នុងប្លង់តែមួយ។', 'Understand'))

    # ============================================================ MCQ MEDIUM (14)
    chk(lambda: cross((2, 1, -2), (1, -3, 2)) == (-4, -6, -7))
    C.append(mcq('medium', 's1', 'គណនា ' + M('\\vec{u}\\times\\vec{v}') + ' ដែល ' + M('\\vec{u}=2\\vec{i}+\\vec{j}-2\\vec{k}') + ' និង ' + M('\\vec{v}=\\vec{i}-3\\vec{j}+2\\vec{k}') + ' ៖',
                 M('-4\\vec{i}-6\\vec{j}-7\\vec{k}'),
                 [M('4\\vec{i}+6\\vec{j}+7\\vec{k}'), M('-4\\vec{i}+6\\vec{j}-7\\vec{k}'), M('-8\\vec{i}-6\\vec{j}-5\\vec{k}')],
                 M('\\begin{vmatrix}\\vec{i}&\\vec{j}&\\vec{k}\\\\2&1&-2\\\\1&-3&2\\end{vmatrix}=(2-6)\\vec{i}-(4+2)\\vec{j}+(-6-1)\\vec{k}=-4\\vec{i}-6\\vec{j}-7\\vec{k}') + '។', 'Apply'))
    chk(lambda: cross((1, -2, 1), (3, 1, -2)) == (3, 5, 7))
    C.append(mcq('medium', 's1', 'គេឱ្យ ' + M('\\vec{u}=(1,-2,1)') + ' និង ' + M('\\vec{v}=(3,1,-2)') + ' ។ កូអរដោនេនៃ ' + M('\\vec{u}\\times\\vec{v}') + ' គឺ ៖',
                 M('(3,5,7)'), [M('(-3,-5,-7)'), M('(3,-5,7)'), M('(5,5,7)')],
                 M('(4-1,\\,-(-2-3),\\,1+6)=(3,5,7)') + '។', 'Apply'))
    chk(lambda: cross((2, -3, 1), (1, -2, 1)) == (-1, -1, -1))
    C.append(mcq('medium', 's1', 'គេឱ្យ ' + M('\\vec{u}=(2,-3,1)') + ' និង ' + M('\\vec{v}=(1,-2,1)') + ' ។ គណនា ' + M('\\vec{u}\\times\\vec{v}') + ' ៖',
                 M('(-1,-1,-1)'), [M('(1,1,1)'), M('(-1,1,-1)'), M('(-5,-1,-1)')],
                 M('(-3+2,\\,-(2-1),\\,-4+3)=(-1,-1,-1)') + '។', 'Apply'))
    chk(lambda: cross((12, -3, 0), (-2, 5, 0)) == (0, 0, 54))
    C.append(mcq('medium', 's1', 'គណនា ' + M('(12,-3,0)\\times(-2,5,0)') + ' ៖',
                 M('(0,0,54)'), [M('(0,0,-54)'), M('(0,0,66)'), M('(54,0,0)')],
                 'វ៉ិចទ័រទាំងពីរនៅក្នុងប្លង់ ' + M('xOy') + ' ដូច្នេះ ' + M('(0,0,12(5)-(-3)(-2))=(0,0,54)') + '។', 'Apply'))
    chk(lambda: norm2(cross((3, 2, -1), (1, 2, 3))) == 180)
    C.append(mcq('medium', 's2', 'ផ្ទៃក្រឡាប្រលេឡូក្រាមសង់លើ ' + M('\\vec{u}=(3,2,-1)') + ' និង ' + M('\\vec{v}=(1,2,3)') + ' ស្មើនឹង ៖',
                 M('6\\sqrt5'), [M('3\\sqrt5'), M('\\sqrt{180}').replace('\\sqrt{180}', '180'), M('12\\sqrt5')],
                 M('\\vec{u}\\times\\vec{v}=(8,-10,4)') + ' ដូច្នេះ ' + M('|\\vec{u}\\times\\vec{v}|=\\sqrt{64+100+16}=\\sqrt{180}=6\\sqrt5') + '។', 'Apply'))
    chk(lambda: norm2(cross((2, -1, 0), (-1, 2, 0))) == 9)
    C.append(mcq('medium', 's2', 'ផ្ទៃក្រឡាប្រលេឡូក្រាមសង់លើ ' + M('\\vec{u}=(2,-1,0)') + ' និង ' + M('\\vec{v}=(-1,2,0)') + ' ស្មើនឹង ៖',
                 M('3'), [M('5'), M('\\frac32'), M('9')],
                 M('\\vec{u}\\times\\vec{v}=(0,0,4-1)=(0,0,3)') + ' ដូច្នេះផ្ទៃក្រឡាស្មើ ' + M('3') + '។', 'Apply'))
    chk(lambda: norm2(cross((1, 2, 0), (-2, 1, 0))) == 25)
    C.append(mcq('medium', 's2', 'ផ្ទៃក្រឡាត្រីកោណមានកំពូល ' + M('(1,2,0),\\ (-2,1,0),\\ (0,0,0)') + ' ស្មើនឹង ៖',
                 M('\\frac52'), [M('5'), M('\\frac32'), M('10')],
                 M('\\frac12|(1,2,0)\\times(-2,1,0)|=\\frac12|(0,0,5)|=\\frac52') + '។', 'Apply'))
    chk(lambda: norm2(cross((2 - 1, 0 - 1, 3 - 1), (-1 - 1, 2 - 1, 0 - 1))) == 11)
    C.append(mcq('medium', 's2', 'ផ្ទៃក្រឡាត្រីកោណ ' + M('ABC') + ' ដែល ' + M('A(1,1,1),\\ B(2,0,3),\\ C(-1,2,0)') + ' គឺ ៖',
                 M('\\frac{\\sqrt{11}}{2}'), [M('\\sqrt{11}'), M('\\frac{\\sqrt{14}}{2}'), M('\\frac{11}{2}')],
                 M('\\vec{AB}=(1,-1,2),\\ \\vec{AC}=(-2,1,-1)') + ' ; ' + M('\\vec{AB}\\times\\vec{AC}=(-1,-3,-1)') + ' ដូច្នេះ ' + M('\\mathcal{A}=\\frac12\\sqrt{1+9+1}=\\frac{\\sqrt{11}}{2}') + '។', 'Apply'))
    chk(lambda: norm2(cross((1, -4, 1), (2, 3, 0))) == 134)
    C.append(mcq('medium', 's1', 'វ៉ិចទ័រឯកតាអរតូកូណាល់នឹង ' + M('\\vec{u}=(1,-4,1)') + ' និង ' + M('\\vec{v}=(2,3,0)') + ' មួយគឺ ៖',
                 M('\\frac{-3\\vec{i}+2\\vec{j}+11\\vec{k}}{\\sqrt{134}}'),
                 [M('\\frac{3\\vec{i}+2\\vec{j}+11\\vec{k}}{\\sqrt{134}}'), M('\\frac{-3\\vec{i}+2\\vec{j}+11\\vec{k}}{134}'), M('-3\\vec{i}+2\\vec{j}+11\\vec{k}')],
                 M('\\vec{u}\\times\\vec{v}=(-3,2,11)') + ' មានណម ' + M('\\sqrt{9+4+121}=\\sqrt{134}') + '។', 'Apply'))
    chk(lambda: dot((1, 1, 1), cross((2, 1, 0), (0, 0, 1))) == -1)
    C.append(mcq('medium', 's4', 'គណនាផលគុណចម្រុះ ' + M('\\vec{u}\\cdot(\\vec{v}\\times\\vec{w})') + ' ដែល ' + M('\\vec{u}=(1,1,1),\\ \\vec{v}=(2,1,0),\\ \\vec{w}=(0,0,1)') + ' ៖',
                 M('-1'), [M('1'), M('0'), M('2')],
                 M('\\vec{v}\\times\\vec{w}=(1,-2,0)\\implies\\vec{u}\\cdot(\\vec{v}\\times\\vec{w})=1-2+0=-1') + '។', 'Apply'))
    chk(lambda: dot((2, 0, 1), cross((0, 3, 0), (0, 0, 1))) == 6)
    C.append(mcq('medium', 's4', 'មាឌប្រលេពីប៉ែតសង់លើ ' + M('\\vec{u}=(2,0,1),\\ \\vec{v}=(0,3,0),\\ \\vec{w}=(0,0,1)') + ' ស្មើនឹង ៖',
                 M('6'), [M('3'), M('1'), M('12')],
                 M('V=|\\vec{u}\\cdot(\\vec{v}\\times\\vec{w})|=|\\det|=|2\\times3\\times1|=6') + '។', 'Apply'))
    chk(lambda: abs(dot((1, 1, 0), cross((0, 1, 1), (1, 0, 1)))) == 2)
    C.append(mcq('medium', 's4', 'មាឌប្រលេពីប៉ែតសង់លើ ' + M('\\vec{u}=\\vec{i}+\\vec{j},\\ \\vec{v}=\\vec{j}+\\vec{k},\\ \\vec{w}=\\vec{i}+\\vec{k}') + ' គឺ ៖',
                 M('2'), [M('1'), M('4'), M('6')],
                 M('\\det\\begin{pmatrix}1&1&0\\\\0&1&1\\\\1&0&1\\end{pmatrix}=1(1)-1(-1)=2') + '។', 'Apply'))
    chk(lambda: abs(dot((1, 3, 1), cross((0, 5, 5), (4, 0, 4)))) == 60)
    C.append(mcq('medium', 's4', 'មាឌតេត្រាអែតសង់លើ ' + M('\\vec{u}=(1,3,1),\\ \\vec{v}=(0,5,5),\\ \\vec{w}=(4,0,4)') + ' ស្មើនឹង ៖',
                 M('10'), [M('60'), M('30'), M('20')],
                 'មាឌប្រលេពីប៉ែត ' + M('V=60') + ' ដូច្នេះមាឌតេត្រាអែត ' + M('W=\\frac{60}{6}=10') + '។', 'Apply'))
    C.append(with_img(mcq('medium', 's3', 'ដូចក្នុងរូប បើ ' + M('\\vec{PQ}=\\vec{j}') + ' (' + M('1\\text{ m}') + ') និង ' + M('\\vec{F}=-50\\vec{k}\\text{ N}') + ' នោះម៉ូម៉ង់ ' + M('|\\vec{M}|=|\\vec{PQ}\\times\\vec{F}|') + ' ស្មើនឹង ៖',
                          M('50\\text{ Nm}'), [M('25\\text{ Nm}'), M('0\\text{ Nm}'), M('100\\text{ Nm}')],
                          M('\\vec{j}\\times(-50\\vec{k})=-50\\vec{i}') + ' ដូច្នេះ ' + M('|\\vec{M}|=50\\text{ Nm}') + '។', 'Apply'), fig_torque()))

    # ============================================================ MCQ HARD (7)
    chk(lambda: dot((3, -5, 1), cross((0, 2, -2), (3, 1, 1))) == 36)
    C.append(with_img(mcq('hard', 's4', 'មាឌប្រលេពីប៉ែតមានជ្រុងជាប់ ' + M('\\vec{u}=(3,-5,1),\\ \\vec{v}=(0,2,-2),\\ \\vec{w}=(3,1,1)') + ' គឺ ៖',
                          M('36'), [M('18'), M('6'), M('24')],
                          M('V=|3(2+2)-(-5)(0+6)+1(0-6)|=|12+30-6|=36') + '។', 'Apply'), fig_box()))
    chk(lambda: norm2(cross((1, 2, 3), (5, 4, 1))) == 332)
    C.append(mcq('hard', 's2', 'ប្រលេឡូក្រាមមានកំពូល ' + M('A(1,1,1),\\ B(2,3,4),\\ C(6,5,2),\\ D(7,7,5)') + ' មានផ្ទៃក្រឡា ៖',
                 M('2\\sqrt{83}'), [M('\\sqrt{83}'), M('2\\sqrt{43}'), M('4\\sqrt{83}')],
                 M('\\vec{AB}=(1,2,3),\\ \\vec{AC}=(5,4,1)\\implies\\vec{AB}\\times\\vec{AC}=(-10,14,-6)') + ' ណម ' + M('\\sqrt{332}=2\\sqrt{83}') + '។', 'Analyze'))
    chk(lambda: norm2(cross((2, 0, -5), (-3, -3, 0))) == 486)
    C.append(mcq('hard', 's2', 'ផ្ទៃក្រឡាត្រីកោណមានកំពូល ' + M('(1,3,5),\\ (3,3,0),\\ (-2,0,5)') + ' ស្មើនឹង ៖',
                 M('\\frac{9\\sqrt6}{2}'), [M('9\\sqrt6'), M('\\frac{3\\sqrt{13}}{2}'), M('3\\sqrt6')],
                 M('\\vec{AB}=(2,0,-5),\\ \\vec{AC}=(-3,-3,0)\\implies\\vec{AB}\\times\\vec{AC}=(-15,15,-6)') + ' ; ' + M('\\mathcal{A}=\\frac12\\sqrt{486}=\\frac{9\\sqrt6}{2}') + '។', 'Apply'))
    chk(lambda: abs(dot((3, 0, 0), cross((0, 5, 1), (2, 0, 5)))) == 75)
    C.append(mcq('hard', 's4', 'ប្រលេពីប៉ែតមានគល់ ' + M('(0,0,0)') + ' និងកំពូលជាប់ ' + M('(3,0,0),\\ (0,5,1),\\ (2,0,5)') + ' មានមាឌ ៖',
                 M('75'), [M('25'), M('15'), M('150')],
                 M('V=|\\det\\begin{pmatrix}3&0&0\\\\0&5&1\\\\2&0&5\\end{pmatrix}|=|3(25)|=75') + '។', 'Apply'))
    chk(lambda: abs(dot((1, 1, 0), cross((1, 0, 2), (0, 1, 1)))) == 3)
    C.append(mcq('hard', 's4', 'ប្រលេពីប៉ែតមានជ្រុងជាប់ ' + M('(1,1,0),\\ (1,0,2),\\ (0,1,1)') + ' មានមាឌ ៖',
                 M('3'), [M('1'), M('6'), M('2')],
                 M('V=|1(0-2)-1(1-0)+0|=|-3|=3') + '។', 'Apply'))
    chk(lambda: dot((2, 0, 0), cross((1, 1, 1), (0, 2, 2))) == 0)
    C.append(mcq('hard', 's4', 'គណនា ' + M('\\vec{u}\\cdot(\\vec{v}\\times\\vec{w})') + ' ដែល ' + M('\\vec{u}=(2,0,0),\\ \\vec{v}=(1,1,1),\\ \\vec{w}=(0,2,2)') + ' ៖',
                 M('0'), [M('4'), M('-4'), M('2')],
                 M('\\vec{v}\\times\\vec{w}=(0,-2,2)\\implies\\vec{u}\\cdot(\\vec{v}\\times\\vec{w})=2(0)+0+0=0') + '។', 'Analyze'))
    chk(lambda: (dot((1, 2, -1), (2, 1, 4)) == 0))
    C.append(mcq('hard', 's1', 'បើ ' + M('\\vec{u}=(1,2,-1),\\ \\vec{v}=(2,1,4)') + ' នោះ ' + M('(\\vec{u}\\times\\vec{v})\\cdot(\\vec{u}+\\vec{v})') + ' ស្មើប៉ុន្មាន ?',
                 M('0'), [M('1'), M('-5'), M('10')],
                 M('\\vec{u}\\times\\vec{v}') + ' កែងនឹងទាំង ' + M('\\vec{u}') + ' និង ' + M('\\vec{v}') + ' ដូច្នេះកែងនឹង ' + M('\\vec{u}+\\vec{v}') + ' ដែរ។', 'Evaluate'))

    # ============================================================ MCQ PISA (5)
    chk(lambda: close(50 * mp.sin(mp.pi / 3) if False else 50 * mp.mpf('0.5'), 25))
    C.append(with_img(mcq('pisa', 'p_torque', 'កម្លាំងបញ្ឈរ ' + M('50\\text{ N}') + ' (' + M('\\vec{F}=-50\\vec{k}') + ') ទាញចុងដងថ្លឹង ' + M('\\vec{PQ}=\\frac12\\vec{j}+\\frac{\\sqrt3}{2}\\vec{k}') + ' (ប្រវែង ' + M('1\\text{ m}') + ') ។ ម៉ូម៉ង់ ' + M('|\\vec{M}|') + ' ស្មើ ៖',
                          M('25\\text{ Nm}'), [M('25\\sqrt3\\text{ Nm}'), M('50\\text{ Nm}'), M('12{,}5\\text{ Nm}')],
                          M('\\vec{PQ}\\times\\vec{F}=-25\\vec{i}\\implies|\\vec{M}|=25\\text{ Nm}') + '។', 'Apply'), fig_torque()))
    chk(lambda: norm2(cross((4, 0, 0), (0, 3, 4))) == 400)
    C.append(mcq('pisa', 'p_solar', 'ផ្ទាំងសូឡាមួយតាងដោយប្រលេឡូក្រាមសង់លើ ' + M('\\vec{u}=(4,0,0)\\text{ m}') + ' និង ' + M('\\vec{v}=(0,3,4)\\text{ m}') + ' ។ ផ្ទៃក្រឡាផ្ទាំងសូឡាស្មើ ៖',
                 M('20\\text{ m}^2'), [M('12\\text{ m}^2'), M('16\\text{ m}^2'), M('25\\text{ m}^2')],
                 M('\\vec{u}\\times\\vec{v}=(0,-16,12)\\implies|\\vec{u}\\times\\vec{v}|=\\sqrt{256+144}=20\\text{ m}^2') + '។', 'Apply'))
    chk(lambda: norm2(cross((6, 0, 0), (0, 8, 6))) == 3600)
    C.append(mcq('pisa', 'p_roof', 'ដំបូលត្រីកោណមានវ៉ិចទ័រជ្រុង ' + M('\\vec{AB}=(6,0,0)\\text{ m}') + ' និង ' + M('\\vec{AC}=(0,8,6)\\text{ m}') + ' ។ ផ្ទៃក្រឡាដំបូលត្រីកោណស្មើ ៖',
                 M('30\\text{ m}^2'), [M('60\\text{ m}^2'), M('24\\text{ m}^2'), M('48\\text{ m}^2')],
                 M('\\frac12|(6,0,0)\\times(0,8,6)|=\\frac12|(0,-36,48)|=\\frac12(60)=30\\text{ m}^2') + '។', 'Apply'))
    chk(lambda: abs(dot((4, 0, 0), cross((0, 5, 0), (1, 1, 3)))) == 60)
    C.append(with_img(mcq('pisa', 'p_box', 'ឃ្លាំងរាងប្រលេពីប៉ែតទ្រេតសង់លើ ' + M('\\vec{u}=(4,0,0),\\ \\vec{v}=(0,5,0),\\ \\vec{w}=(1,1,3)') + ' (ម៉ែត្រ) ។ មាឌឃ្លាំងស្មើ ៖',
                          M('60\\text{ m}^3'), [M('20\\text{ m}^3'), M('12\\text{ m}^3'), M('45\\text{ m}^3')],
                          M('V=|4(15)|=60\\text{ m}^3') + '។', 'Apply'), fig_box()))
    chk(lambda: norm2(cross((0, mp.mpf('0.4'), 0), (0, 0, 30))) == 144)
    C.append(mcq('pisa', 'p_wrench', 'ដងកូនសោប្រវែង ' + M('0{,}4\\text{ m}') + ' តាម ' + M('\\vec{j}') + ' ទទួលកម្លាំង ' + M('\\vec{F}=30\\vec{k}\\text{ N}') + ' ។ ទំហំម៉ូម៉ង់បង្វិលគឺ ៖',
                 M('12\\text{ Nm}'), [M('75\\text{ Nm}'), M('30\\text{ Nm}'), M('6\\text{ Nm}')],
                 M('|0{,}4\\vec{j}\\times30\\vec{k}|=|12\\vec{i}|=12\\text{ Nm}') + '។', 'Apply'))

    C.extend(cands_writing())
    return C


def cands_writing():
    C = []
    # ============================================================ WRITING EASY (1)
    chk(lambda: cross((1, 1, 1), (2, 1, -1)) == (-2, 3, -1))
    C.append(wr('easy', 's1', 'គេឱ្យ ' + M('\\vec{u}=\\vec{i}+\\vec{j}+\\vec{k}') + ' និង ' + M('\\vec{v}=2\\vec{i}+\\vec{j}-\\vec{k}') + ' ។ គណនា ' + M('\\vec{u}\\times\\vec{v}') + ' និងផ្ទៀងផ្ទាត់ថាវាកែងនឹង ' + M('\\vec{u}') + ' ។',
                [(M('\\vec{u}\\times\\vec{v}=(-1-1)\\vec{i}-(-1-2)\\vec{j}+(1-2)\\vec{k}=-2\\vec{i}+3\\vec{j}-\\vec{k}'), 3),
                 (M('(\\vec{u}\\times\\vec{v})\\cdot\\vec{u}=-2(1)+3(1)+(-1)(1)=0\\implies(\\vec{u}\\times\\vec{v})\\perp\\vec{u}'), 2)], bloom='Apply'))

    # ============================================================ WRITING MEDIUM (4)
    chk(lambda: norm2(cross((-2, -2, -2), (-3, -1, -4))) == 56)
    C.append(wr('medium', 's2', 'រកផ្ទៃក្រឡាត្រីកោណដែលមានកំពូល ' + M('A(2,3,4),\\ B(0,1,2),\\ C(-1,2,0)') + ' ។',
                [(M('\\vec{AB}=(-2,-2,-2),\\ \\vec{AC}=(-3,-1,-4)'), 1),
                 (M('\\vec{AB}\\times\\vec{AC}=(6,-2,-4)'), 2),
                 (M('\\mathcal{A}=\\frac12\\sqrt{36+4+16}=\\frac12\\sqrt{56}=\\sqrt{14}'), 2)], bloom='Apply'))
    chk(lambda: cross((-8, -6, 4), (10, -12, -2)) == (60, 24, 156))
    C.append(wr('medium', 's1', 'គេឱ្យ ' + M('\\vec{u}=(-8,-6,4)') + ' និង ' + M('\\vec{v}=(10,-12,-2)') + ' ។ រក ' + M('\\vec{u}\\times\\vec{v}') + ' និងវ៉ិចទ័រឯកតាអរតូកូណាល់នឹងទាំងពីរ។',
                [(M('\\vec{u}\\times\\vec{v}=(12+48,\\,-(16-40),\\,96+60)=(60,24,156)'), 2),
                 (M('|\\vec{u}\\times\\vec{v}|=12\\sqrt{5^2+2^2+13^2}=12\\sqrt{198}=36\\sqrt{22}'), 2),
                 ('វ៉ិចទ័រឯកតា ' + M('\\pm\\frac{1}{3\\sqrt{22}}(5,2,13)'), 1)], bloom='Apply'))
    chk(lambda: cross((-3, 4, 1), (0, -2, 6)) == (26, 18, 6))
    C.append(wr('medium', 's2', 'បង្ហាញថា ' + M('A(5,2,0),\\ B(2,6,1),\\ C(2,4,7),\\ D(5,0,6)') + ' ជាកំពូលប្រលេឡូក្រាម រួចរកផ្ទៃក្រឡា។',
                [(M('\\vec{AB}=(-3,4,1)=\\vec{DC}') + ' ដូច្នេះ ' + M('ABCD') + ' ជាប្រលេឡូក្រាម', 2),
                 (M('\\vec{AD}=(0,-2,6)\\implies\\vec{AB}\\times\\vec{AD}=(26,18,6)'), 2),
                 (M('\\mathcal{A}=\\sqrt{26^2+18^2+6^2}=\\sqrt{1036}=2\\sqrt{259}'), 1)], bloom='Analyze'))
    chk(lambda: abs(dot((1, 1, 0), cross((0, 1, 1), (1, 0, 1)))) == 2)
    C.append(wr('medium', 's4', 'រកមាឌប្រលេពីប៉ែតដែលមានជ្រុងជាប់ ' + M('\\vec{u}=(1,1,0),\\ \\vec{v}=(0,1,1),\\ \\vec{w}=(1,0,1)') + ' ។',
                [(M('\\vec{v}\\times\\vec{w}=(1,1,-1)'), 2),
                 (M('V=|\\vec{u}\\cdot(\\vec{v}\\times\\vec{w})|=|1(1)+1(1)+0(-1)|=2'), 3)], bloom='Apply'))

    # ============================================================ WRITING HARD (4)
    chk(lambda: norm2(cross((0, 1, 6), (1, -2, 1))) == 206)
    C.append(wr('hard', 's1', 'គេឱ្យ ' + M('\\vec{u}=\\vec{j}+6\\vec{k}') + ' និង ' + M('\\vec{v}=\\vec{i}-2\\vec{j}+\\vec{k}') + ' ។ គណនា ' + M('\\vec{u}\\times\\vec{v}') + ' និងផ្ទៀងផ្ទាត់ថាវាកែងនឹងទាំង ' + M('\\vec{u}') + ' និង ' + M('\\vec{v}') + ' ។',
                [(M('\\vec{u}\\times\\vec{v}=(1+12)\\vec{i}-(0-6)\\vec{j}+(0-1)\\vec{k}=13\\vec{i}+6\\vec{j}-\\vec{k}'), 3),
                 (M('(13,6,-1)\\cdot(0,1,6)=6-6=0') + ' និង ' + M('(13,6,-1)\\cdot(1,-2,1)=13-12-1=0'), 2)], bloom='Apply'))
    chk(lambda: abs(dot((1, 2, 4), cross((-2, 0, -1), (0, 1, 2)))) == 1)
    C.append(wr('hard', 's4', 'គណនាផលគុណចម្រុះ ' + M('\\vec{u}\\cdot(\\vec{v}\\times\\vec{w})') + ' ដែល ' + M('\\vec{u}=(1,2,4),\\ \\vec{v}=(-2,0,-1),\\ \\vec{w}=(0,1,2)') + ' ។ តើវ៉ិចទ័រទាំងបីស្ថិតក្នុងប្លង់តែមួយឬទេ ?',
                [(M('\\vec{v}\\times\\vec{w}=(1,4,-2)'), 2),
                 (M('\\vec{u}\\cdot(\\vec{v}\\times\\vec{w})=1(1)+2(4)+4(-2)=1\\ne0'), 2),
                 ('ដោយផលគុណចម្រុះខុសពី ០ វ៉ិចទ័រទាំងបីមិនស្ថិតក្នុងប្លង់តែមួយទេ', 1)], bloom='Evaluate'))
    chk(lambda: norm2(cross((3, 2, 3), (-2, 2, 0))) == 172)
    C.append(wr('hard', 's2', 'ផ្ទៀងផ្ទាត់ថា ' + M('A(2,-1,1),\\ B(5,1,4),\\ C(0,1,1),\\ D(3,3,4)') + ' ជាកំពូលប្រលេឡូក្រាម រួចគណនាផ្ទៃក្រឡា។',
                [(M('\\vec{AB}=(3,2,3)=\\vec{CD}') + ' ដូច្នេះ ' + M('ABDC') + ' ជាប្រលេឡូក្រាម', 2),
                 (M('\\vec{AC}=(-2,2,0)\\implies\\vec{AB}\\times\\vec{AC}=(-6,-6,10)'), 2),
                 (M('\\mathcal{A}=\\sqrt{36+36+100}=\\sqrt{172}=2\\sqrt{43}'), 1)], bloom='Analyze'))
    C.append(wr('hard', 's1', 'បង្ហាញថា ' + M('\\vec{u}\\cdot(\\vec{v}\\times\\vec{w})=(\\vec{u}\\times\\vec{v})\\cdot\\vec{w}') + ' ចំពោះគ្រប់វ៉ិចទ័រ ' + M('\\vec{u},\\vec{v},\\vec{w}') + ' ។',
                [(M('\\vec{u}\\cdot(\\vec{v}\\times\\vec{w})=u_1(v_2w_3-v_3w_2)-u_2(v_1w_3-v_3w_1)+u_3(v_1w_2-v_2w_1)'), 2),
                 (M('(\\vec{u}\\times\\vec{v})\\cdot\\vec{w}=(u_2v_3-u_3v_2)w_1-(u_1v_3-u_3v_1)w_2+(u_1v_2-u_2v_1)w_3'), 2),
                 ('ពន្លាតទាំងពីរកន្សោមឃើញមាន ៦ តួដូចគ្នាទាំងស្រុង', 1)], bloom='Understand'))

    # ============================================================ WRITING PISA (5)
    chk(lambda: norm2(cross((0, mp.mpf('0.5'), mp.sqrt(3) / 2), (0, 0, -50))) == 625)
    C.append(with_img(wr('pisa', 'p_torque', 'កម្លាំង ' + M('\\vec{F}=-50\\vec{k}\\text{ N}') + ' អនុវត្តលើចុងដងថ្លឹង ' + M('\\vec{PQ}=\\frac12\\vec{j}+\\frac{\\sqrt3}{2}\\vec{k}\\text{ m}') + ' ។ គណនាវ៉ិចទ័រម៉ូម៉ង់ ' + M('\\vec{M}=\\vec{PQ}\\times\\vec{F}') + ' និងទំហំ ' + M('|\\vec{M}|') + ' ។',
                         [(M('\\vec{M}=\\begin{vmatrix}\\vec{i}&\\vec{j}&\\vec{k}\\\\0&\\frac12&\\frac{\\sqrt3}{2}\\\\0&0&-50\\end{vmatrix}=-25\\vec{i}'), 3),
                          (M('|\\vec{M}|=25\\text{ Nm}'), 2)], bloom='Apply'), fig_torque()))
    chk(lambda: norm2(cross((4, 0, 0), (0, 3, 4))) == 400)
    C.append(wr('pisa', 'p_solar', 'បន្ទះសូឡារាងប្រលេឡូក្រាមកំណត់ដោយ ' + M('\\vec{u}=(4,0,0)\\text{ m}') + ' និង ' + M('\\vec{v}=(0,3,4)\\text{ m}') + ' ។ គណនាវ៉ិចទ័រកែងបន្ទះ និងផ្ទៃក្រឡាបន្ទះ។',
                [(M('\\vec{u}\\times\\vec{v}=(0,-16,12)'), 3),
                 (M('\\mathcal{A}=\\sqrt{0+256+144}=20\\text{ m}^2'), 2)], bloom='Apply'))
    chk(lambda: norm2(cross((6, 0, 0), (0, 8, 6))) == 3600)
    C.append(wr('pisa', 'p_roof', 'ដំបូលត្រីកោណមានជ្រុង ' + M('\\vec{AB}=(6,0,0)\\text{ m}') + ' និង ' + M('\\vec{AC}=(0,8,6)\\text{ m}') + ' ។ គណនាផ្ទៃក្រឡាដំបូល និងតម្លៃក្បឿងបើ ' + M('1\\text{ m}^2') + ' ថ្លៃ ' + M('10\\$') + ' ។',
                [(M('\\vec{AB}\\times\\vec{AC}=(0,-36,48)\\implies\\mathcal{A}=\\frac12\\sqrt{36^2+48^2}=30\\text{ m}^2'), 3),
                 ('តម្លៃក្បឿង ' + M('=30\\times10=300\\$'), 2)], bloom='Apply'))
    chk(lambda: abs(dot((4, 0, 0), cross((0, 5, 0), (1, 1, 3)))) == 60)
    C.append(with_img(wr('pisa', 'p_box', 'រោងដាក់ទំនិញរាងប្រលេពីប៉ែតមានជ្រុង ' + M('\\vec{u}=(4,0,0),\\ \\vec{v}=(0,5,0),\\ \\vec{w}=(1,1,3)') + ' (ម៉ែត្រ) ។ គណនាមាឌរោង និងចំណុះគិតជាលីត្រ។',
                         [(M('V=|\\vec{u}\\cdot(\\vec{v}\\times\\vec{w})|=60\\text{ m}^3'), 3),
                          ('ចំណុះ ' + M('=60\\times1000=60\\,000\\text{ L}'), 2)], bloom='Apply'), fig_box()))
    chk(lambda: norm2(cross((0, mp.mpf('0.4'), 0), (0, 0, 30))) == 144)
    C.append(wr('pisa', 'p_wrench', 'ដងកូនសោ ' + M('\\vec{r}=0{,}4\\vec{j}\\text{ m}') + ' ទទួលកម្លាំង ' + M('\\vec{F}=30\\vec{k}\\text{ N}') + ' ។ ក. គណនាម៉ូម៉ង់ ' + M('\\vec{M}') + ' ។ ខ. បើបង្កើនប្រវែងដងដល់ ' + M('0{,}6\\text{ m}') + ' តើម៉ូម៉ង់កើនប៉ុន្មាន ?',
                [('ក. ' + M('\\vec{M}=0{,}4\\vec{j}\\times30\\vec{k}=12\\vec{i}\\implies|\\vec{M}|=12\\text{ Nm}'), 3),
                 ('ខ. ម៉ូម៉ង់ថ្មី ' + M('0{,}6\\times30=18\\text{ Nm}') + ' កើនឡើង ' + M('6\\text{ Nm}'), 2)], bloom='Analyze'))
    return C


def verify():
    mp.mp.dps = 30
    CNT[0] = 0
    cands()
    return CNT[0]
