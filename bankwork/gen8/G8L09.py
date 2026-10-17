from lib import *
import sympy as sp
from sympy import symbols, Rational as Q_
from sympy.parsing.sympy_parser import parse_expr
import re as _re

LESSON = 'ប្លង់កូអរដោនេនិងក្រាប'
x, y, z, a, b, c, t, m, n, d, k = symbols('x y z a b c t m n d k')
_LD = {s_.name: s_ for s_ in (x, y, z, a, b, c, t, m, n, d, k)}

def L(e): return sp.latex(e).replace(r'\\frac', r'\\dfrac')

C = []

def uniq(correct, cands, k_=3):
    out = [correct]
    for c_ in cands:
        if c_ not in out: out.append(c_)
        if len(out) == k_ + 1: break
    assert len(out) == k_ + 1, ('wrongs', correct)
    return out[1:]

def with_img(q_, s_): q_['img'] = s_; return q_

# ---------- figures (Transparent background, Mathcad Italic variables, Upright serif dimensions) ----------
FIG_POINT_P = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 320 220' width='320' height='220'>
  <line x1='30' y1='170' x2='290' y2='170' stroke='#1e293b' stroke-width='1.8'/>
  <polyline points='282,166 290,170 282,174' fill='none' stroke='#1e293b' stroke-width='1.8'/>
  <text x='295' y='174' font-family='Mathcad UniMath Italic,Times New Roman,serif' font-style='italic' font-size='14' fill='#0f172a'>x</text>
  <line x1='70' y1='195' x2='70' y2='20' stroke='#1e293b' stroke-width='1.8'/>
  <polyline points='66,28 70,20 74,28' fill='none' stroke='#1e293b' stroke-width='1.8'/>
  <text x='70' y='14' text-anchor='middle' font-family='Mathcad UniMath Italic,Times New Roman,serif' font-style='italic' font-size='14' fill='#0f172a'>y</text>
  <text x='58' y='184' font-family='Times New Roman,serif' font-size='13'>O</text>
  <text x='190' y='186' text-anchor='middle' font-family='Times New Roman,serif' font-size='12'>4</text>
  <text x='55' y='84' text-anchor='middle' font-family='Times New Roman,serif' font-size='12'>3</text>
  <line x1='190' y1='170' x2='190' y2='80' stroke='#ef4444' stroke-width='1.4' stroke-dasharray='4 3'/>
  <line x1='70' y1='80' x2='190' y2='80' stroke='#ef4444' stroke-width='1.4' stroke-dasharray='4 3'/>
  <circle cx='190' cy='80' r='4.5' fill='#ef4444'/>
  <text x='202' y='74' font-family='Mathcad UniMath Italic,Times New Roman,serif' font-style='italic' font-size='14' font-weight='bold' fill='#b91c1c'>P(<tspan font-style='normal'>4</tspan>, <tspan font-style='normal'>3</tspan>)</text>
</svg>"""

FIG_LINE = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 320 220' width='320' height='220'>
  <line x1='30' y1='150' x2='290' y2='150' stroke='#1e293b' stroke-width='1.6'/>
  <polyline points='282,146 290,150 282,154' fill='none' stroke='#1e293b' stroke-width='1.6'/>
  <text x='295' y='154' font-family='Mathcad UniMath Italic,Times New Roman,serif' font-style='italic' font-size='14' fill='#0f172a'>x</text>
  <line x1='140' y1='200' x2='140' y2='20' stroke='#1e293b' stroke-width='1.6'/>
  <polyline points='136,28 140,20 144,28' fill='none' stroke='#1e293b' stroke-width='1.6'/>
  <text x='140' y='14' text-anchor='middle' font-family='Mathcad UniMath Italic,Times New Roman,serif' font-style='italic' font-size='14' fill='#0f172a'>y</text>
  <text x='128' y='164' font-family='Times New Roman,serif' font-size='12'>O</text>
  <line x1='80' y1='210' x2='230' y2='40' stroke='#0284c7' stroke-width='2.2'/>
  <circle cx='140' cy='130' r='4' fill='#0369a1'/>
  <text x='125' y='132' text-anchor='end' font-family='Times New Roman,serif' font-size='11'>(0, 1)</text>
  <circle cx='180' cy='90' r='4' fill='#0369a1'/>
  <text x='192' y='92' font-family='Times New Roman,serif' font-size='11'>(1, 3)</text>
  <text x='235' y='36' font-family='Mathcad UniMath Italic,Times New Roman,serif' font-style='italic' font-size='13' fill='#0369a1'>y = <tspan font-style='normal'>2</tspan>x + <tspan font-style='normal'>1</tspan></text>
</svg>"""

FIG_PARALLEL = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 320 200' width='320' height='200'>
  <line x1='30' y1='140' x2='290' y2='140' stroke='#1e293b' stroke-width='1.6'/>
  <text x='295' y='144' font-family='Mathcad UniMath Italic,Times New Roman,serif' font-style='italic' font-size='14'>x</text>
  <line x1='140' y1='180' x2='140' y2='20' stroke='#1e293b' stroke-width='1.6'/>
  <text x='140' y='14' text-anchor='middle' font-family='Mathcad UniMath Italic,Times New Roman,serif' font-style='italic' font-size='14'>y</text>
  <line x1='80' y1='200' x2='210' y2='40' stroke='#2563eb' stroke-width='2'/>
  <text x='215' y='46' font-family='Mathcad UniMath Italic,Times New Roman,serif' font-style='italic' font-size='12' fill='#1d4ed8'>y = <tspan font-style='normal'>2</tspan>x</text>
  <line x1='50' y1='180' x2='180' y2='20' stroke='#16a34a' stroke-width='2'/>
  <text x='130' y='24' font-family='Mathcad UniMath Italic,Times New Roman,serif' font-style='italic' font-size='12' fill='#15803d'>y = <tspan font-style='normal'>2</tspan>x + <tspan font-style='normal'>2</tspan></text>
  <text x='160' y='185' text-anchor='middle' font-family='Khmer OS Battambang,Noto Sans Khmer,serif' font-size='12' fill='#475569'>បន្ទាត់ទាំងពីរស្របគ្នា (មេគុណប្រាប់ទិស <tspan font-family='Mathcad UniMath Italic,Times New Roman,serif' font-style='italic'>a = 2</tspan>)</text>
</svg>"""

FIG_SHADOW = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 340 160' width='340' height='160'>
  <line x1='40' y1='130' x2='320' y2='130' stroke='#1e293b' stroke-width='1.6'/>
  <polyline points='312,126 320,130 312,134' fill='none' stroke='#1e293b' stroke-width='1.6'/>
  <text x='325' y='134' font-family='Times New Roman,serif' font-size='12'>t (h)</text>
  <line x1='50' y1='140' x2='50' y2='20' stroke='#1e293b' stroke-width='1.6'/>
  <polyline points='46,28 50,20 54,28' fill='none' stroke='#1e293b' stroke-width='1.6'/>
  <text x='50' y='14' text-anchor='middle' font-family='Khmer OS Battambang,Noto Sans Khmer,serif' font-size='11'>ស្រមោល (cm)</text>
  <text x='80' y='145' text-anchor='middle' font-family='Times New Roman,serif' font-size='11'>7h</text>
  <text x='180' y='145' text-anchor='middle' font-family='Times New Roman,serif' font-size='11' font-weight='bold'>12h</text>
  <text x='280' y='145' text-anchor='middle' font-family='Times New Roman,serif' font-size='11'>17h</text>
  <path d='M 80,40 Q 180,120 280,40' fill='none' stroke='#d97706' stroke-width='2.4'/>
  <circle cx='180' cy='100' r='4' fill='#b45309'/>
  <text x='180' y='92' text-anchor='middle' font-family='Khmer OS Battambang,Noto Sans Khmer,serif' font-size='11' fill='#92400e'>ខ្លីបំផុតនៅម៉ោង ១២ ថ្ងៃត្រង់</text>
</svg>"""

def cands():
    global C
    C = []
    # ================= 1. NOTION (Easy MCQ) =================
    C.append(mcq('easy', 'notion', "ក្នុងប្លង់កូអរដោនេ អ័ក្សដេក " + M("x'Ox") + " ហៅថា ៖", 'អ័ក្សអាប់ស៊ីស', ['អ័ក្សអរដោនេ', 'គល់តម្រុយ', 'កាដ្រង់'], "អ័ក្សដេកជាអ័ក្សអាប់ស៊ីស (x) ហើយអ័ក្សឈរជាអ័ក្សអរដោនេ (y)។"))
    C.append(mcq('easy', 'notion', "ក្នុងប្លង់កូអរដោនេ អ័ក្សឈរ " + M("y'Oy") + " ហៅថា ៖", 'អ័ក្សអរដោនេ', ['អ័ក្សអាប់ស៊ីស', 'គល់តម្រុយ', 'កាដ្រង់'], "អ័ក្សឈរជាអ័ក្សអរដោនេ (y)។"))
    C.append(mcq('easy', 'notion', 'ចំណុចប្រសព្វរវាងអ័ក្សទាំងពីរ ' + M('O') + ' ហៅថា ៖', 'គល់កូអរដោនេ មានកូអរដោនេ ' + M('(0, 0)'), ['ចំណុចកំពូល', 'ចំណុចកណ្តាល', 'កាដ្រង់ទី ១'], 'គល់កូអរដោនេ O មានកូអរដោនេ (0, 0)។'))
    C.append(mcq('easy', 'notion', 'ចំណុច ' + M('A(3, 5)') + ' មានអាប់ស៊ីសនិងអរដោនេរៀងគ្នាគឺ ៖', M('x = 3,\\ y = 5'), [M('x = 5,\\ y = 3'), M('x = -3,\\ y = 5'), M('x = 3,\\ y = -5')], 'ក្នុងគូ (x, y) តម្លៃខាងមុខជាអាប់ស៊ីស និងខាងក្រោយជាអរដោនេ។'))
    C.append(mcq('easy', 'notion', 'ចំណុច ' + M('B(-3, 4)') + ' ឋិតនៅក្នុងកាដ្រង់ណា?', 'កាដ្រង់ទី II', ['កាដ្រង់ទី I', 'កាដ្រង់ទី III', 'កាដ្រង់ទី IV'], 'កាដ្រង់ទី II មាន ' + M('x < 0,\\ y > 0') + '។'))
    C.append(mcq('easy', 'notion', 'ចំណុច ' + M('C(-4, -3)') + ' ឋិតនៅក្នុងកាដ្រង់ណា?', 'កាដ្រង់ទី III', ['កាដ្រង់ទី I', 'កាដ្រង់ទី II', 'កាដ្រង់ទី IV'], 'កាដ្រង់ទី III មាន ' + M('x < 0,\\ y < 0') + '។'))
    C.append(mcq('easy', 'notion', 'ចំណុច ' + M('G(2, -3)') + ' ឋិតនៅក្នុងកាដ្រង់ណា?', 'កាដ្រង់ទី IV', ['កាដ្រង់ទី I', 'កាដ្រង់ទី II', 'កាដ្រង់ទី III'], 'កាដ្រង់ទី IV មាន ' + M('x > 0,\\ y < 0') + '។'))
    C.append(mcq('easy', 'notion', 'ចំណុច ' + M('H(3, 0)') + ' ឋិតនៅលើ ៖', "អ័ក្សអាប់ស៊ីស (" + M("x'x") + ")", ["អ័ក្សអរដោនេ (" + M("y'y") + ")", 'កាដ្រង់ទី I', 'កាដ្រង់ទី II'], 'ចំណុចដែលមាន ' + M('y = 0') + ' ឋិតនៅលើអ័ក្សអាប់ស៊ីស។'))
    C.append(mcq('easy', 'notion', 'ចំណុច ' + M('D(0, 6)') + ' ឋិតនៅលើ ៖', "អ័ក្សអរដោនេ (" + M("y'y") + ")", ["អ័ក្សអាប់ស៊ីស (" + M("x'x") + ")", 'កាដ្រង់ទី I', 'កាដ្រង់ទី II'], 'ចំណុចដែលមាន ' + M('x = 0') + ' ឋិតនៅលើអ័ក្សអរដោនេ។'))
    C.append(mcq('easy', 'notion', 'ចំណុចណាខាងក្រោមនេះឋិតនៅលើបន្ទាត់ ' + M('y = 2x') + '?', M('(2, 4)'), [M('(2, 2)'), M('(4, 2)'), M('(1, 3)')], 'ជំនួស ' + M('x = 2') + ' បាន ' + M('y = 2(2) = 4') + '។'))
    C.append(mcq('easy', 'notion', 'ចំណុច ' + M('(0, 0)') + ' ផ្ទៀងផ្ទាត់សមីការបន្ទាត់ណា?', M('y = 3x'), [M('y = 3x + 1'), M('y = 3x - 2'), M('y = x + 5')], 'បន្ទាត់ ' + M('y = ax') + ' តែងតែកាត់តាមគល់តម្រុយ ' + M('O(0, 0)') + '។'))
    C.append(with_img(mcq('easy', 'notion', 'ក្នុងរូបដ្យាក្រាម ចំណុច ' + M('P') + ' មានកូអរដោនេ ៖', M('(4, 3)'), [M('(3, 4)'), M('(4, 0)'), M('(0, 3)')], 'អាប់ស៊ីស ' + M('x = 4') + ' និងអរដោនេ ' + M('y = 3') + ' នាំឱ្យ ' + M('P(4, 3)') + '។'), FIG_POINT_P))

    # ================= 2. LINEAR EQUATIONS & GRAPHS (Medium MCQ) =================
    C.append(mcq('medium', 'line', 'បន្ទាត់ ' + M('y = 2x + 4') + ' កាត់តាមអ័ក្សអរដោនេ ' + M("y'y") + ' ត្រង់ចំណុច ៖', M('(0, 4)'), [M('(4, 0)'), M('(0, -2)'), M('(-2, 0)')], 'នៅលើអ័ក្សអរដោនេ ' + M('x = 0 \\Rightarrow y = 4') + ' គឺ ' + M('(0, 4)') + '។'))
    C.append(mcq('medium', 'line', 'បន្ទាត់ ' + M('y = 2x + 4') + ' កាត់តាមអ័ក្សអាប់ស៊ីស ' + M("x'x") + ' ត្រង់ចំណុច ៖', M('(-2, 0)'), [M('(2, 0)'), M('(0, 4)'), M('(0, -2)')], 'នៅលើអ័ក្សអាប់ស៊ីស ' + M('y = 0 \\Rightarrow 2x + 4 = 0 \\Rightarrow x = -2') + ' គឺ ' + M('(-2, 0)') + '។'))
    C.append(mcq('medium', 'line', 'បើ ' + M('x = 1') + ' តម្លៃ ' + M('y') + ' នៃបន្ទាត់ ' + M('y = 3x + 5') + ' ស្មើ ៖', M('8'), [M('6'), M('15'), M('2')], M('y = 3(1) + 5 = 8') + '។'))
    C.append(mcq('medium', 'line', 'បើ ' + M('x = -1') + ' តម្លៃ ' + M('y') + ' នៃបន្ទាត់ ' + M('y = -2x + 0.5') + ' ស្មើ ៖', M('2.5'), [M('-1.5'), M('0.5'), M('-2.5')], M('y = -2(-1) + 0.5 = 2 + 0.5 = 2.5') + '។'))
    C.append(mcq('medium', 'line', 'សមីការ ' + M('3x + y = 2') + ' សរសេរជាទម្រង់ ' + M('y = ax + b') + ' គឺ ៖', M('y = -3x + 2'), [M('y = 3x + 2'), M('y = 3x - 2'), M('y = -3x - 2')], M('y = -3x + 2') + '។'))
    C.append(mcq('medium', 'line', 'សមីការ ' + M('x - 3 = -3y') + ' សរសេរជាទម្រង់ ' + M('y = ax + b') + ' គឺ ៖', M('y = -\\dfrac{1}{3}x + 1'), [M('y = \\dfrac{1}{3}x + 1'), M('y = -3x + 3'), M('y = 3x - 3')], M('-3y = x - 3 \\Rightarrow y = -\\dfrac{1}{3}x + 1') + '។'))
    C.append(mcq('medium', 'line', 'ក្នុងសមីការបន្ទាត់ ' + M('y = ax + b') + ' មេគុណ ' + M('a') + ' ហៅថា ៖', 'មេគុណប្រាប់ទិស', ['តួថេរ', 'អរដោនេដើម', 'អាប់ស៊ីសដើម'], M('a') + ' ជាមេគុណប្រាប់ទិសនៃបន្ទាត់។'))
    C.append(mcq('medium', 'line', 'បន្ទាត់ ' + M('y = -2x + 1') + ' មានមេគុណប្រាប់ទិសស្មើ ៖', M('-2'), [M('2'), M('1'), M('-1')], 'មេគុណមុខ ' + M('x') + ' គឺ ' + M('a = -2') + '។'))
    C.append(mcq('medium', 'line', 'បន្ទាត់ណាខាងក្រោមនេះស្របនឹងបន្ទាត់ ' + M('y = 2x + 1') + '?', M('y = 2x - 5'), [M('y = -2x + 1'), M('y = 3x + 1'), M('y = -2x - 5')], 'បន្ទាត់ពីរស្របគ្នា លុះត្រាតែមេគុណប្រាប់ទិសស្មើគ្នា (' + M('a_1 = a_2 = 2') + ')។'))
    C.append(mcq('medium', 'line', 'បន្ទាត់ ' + M('y = 4') + ' ក្នុងប្លង់កូអរដោនេជាបន្ទាត់ ៖', 'ស្របនឹងអ័ក្សអាប់ស៊ីស (ដេក)', ['ស្របនឹងអ័ក្សអរដោនេ (ឈរ)', 'កាត់តាមគល់តម្រុយ', 'ទ្រេត 45 ដឺក្រេ'], M('y = 4') + ' មានអរដោនេថេរ ជាបន្ទាត់ដេកស្របអ័ក្សអាប់ស៊ីស។'))
    C.append(mcq('medium', 'line', 'បន្ទាត់ ' + M('x = -3') + ' ក្នុងប្លង់កូអរដោនេជាបន្ទាត់ ៖', 'ស្របនឹងអ័ក្សអរដោនេ (ឈរ)', ['ស្របនឹងអ័ក្សអាប់ស៊ីស (ដេក)', 'កាត់តាមគល់តម្រុយ', 'កាត់តាមកាដ្រង់ទី I'], M('x = -3') + ' មានអាប់ស៊ីសថេរ ជាបន្ទាត់ឈរស្របអ័ក្សអរដោនេ។'))
    C.append(mcq('medium', 'line', 'ចម្ងាយរវាងចំណុច ' + M('A(0, 0)') + ' និង ' + M('B(3, 4)') + ' ស្មើ ៖', M('5'), [M('7'), M('12'), M('25')], M('d = \\sqrt{3^2 + 4^2} = \\sqrt{9 + 16} = \\sqrt{25} = 5') + '។'))
    C.append(mcq('medium', 'line', 'ចម្ងាយរវាងចំណុច ' + M('M(1, 2)') + ' និង ' + M('N(4, 6)') + ' ស្មើ ៖', M('5'), [M('7'), M('4'), M('25')], M('MN = \\sqrt{(4-1)^2 + (6-2)^2} = \\sqrt{3^2 + 4^2} = 5') + '។'))
    C.append(with_img(mcq('medium', 'line', 'ក្នុងរូប បន្ទាត់កាត់តាម ' + M('(0, 1)') + ' និង ' + M('(1, 3)') + ' មានសមីការ ៖', M('y = 2x + 1'), [M('y = x + 1'), M('y = 2x - 1'), M('y = 3x + 1')], 'មេគុណ ' + M('a = \\dfrac{3 - 1}{1 - 0} = 2') + ' និងកាត់ ' + M('y') + ' ត្រង់ ' + M('1 \\Rightarrow y = 2x + 1') + '។'), FIG_LINE))
    C.append(with_img(mcq('medium', 'line', 'បន្ទាត់ ' + M('y = 2x') + ' និង ' + M('y = 2x + 2') + ' មានលក្ខណៈ ៖', 'ស្របគ្នាព្រោះមានមេគុណប្រាប់ទិសស្មើគ្នា', ['កាត់គ្នាត្រង់គល់តម្រុយ', 'កែងគ្នា', 'ត្រួតស៊ីគ្នា'], 'មេគុណប្រាប់ទិសទាំងពីរស្មើ ' + M('2') + ' ដូចនេះបន្ទាត់ទាំងពីរស្របគ្នា។'), FIG_PARALLEL))

    # ================= 3. HARD MCQ =================
    C.append(mcq('hard', 'line', 'សមីការបន្ទាត់កាត់តាមចំណុច ' + M('A(0, 3)') + ' និង ' + M('B(3, 6)') + ' គឺ ៖', M('y = x + 3'), [M('y = 2x + 3'), M('y = x - 3'), M('y = -x + 3')], M('a = \\dfrac{6-3}{3-0} = 1 \\Rightarrow y = x + 3') + '។'))
    C.append(mcq('hard', 'line', 'សមីការបន្ទាត់កាត់តាមចំណុច ' + M('A(0, 4)') + ' និង ' + M('B(2, 2)') + ' គឺ ៖', M('y = -x + 4'), [M('y = x + 4'), M('y = -2x + 4'), M('y = -x - 4')], M('a = \\dfrac{2-4}{2-0} = -1 \\Rightarrow y = -x + 4') + '។'))
    C.append(mcq('hard', 'area', 'ផ្ទៃក្រឡាត្រីកោណកែងដែលបង្កើតឡើងដោយបន្ទាត់ ' + M('y = -2x + 4') + ' ជាមួយអ័ក្សទាំងពីរគឺ ៖', M('4\\ \\text{ឯកតាផ្ទៃ}'), [M('8\\ \\text{ឯកតាផ្ទៃ}'), M('2\\ \\text{ឯកតាផ្ទៃ}'), M('6\\ \\text{ឯកតាផ្ទៃ}')], 'កាត់ ' + M('x') + ' ត្រង់ ' + M('2') + ' និងកាត់ ' + M('y') + ' ត្រង់ ' + M('4 \\Rightarrow S = \\dfrac{1}{2} \\times 2 \\times 4 = 4') + '។'))
    C.append(mcq('hard', 'area', 'ផ្ទៃក្រឡាត្រីកោណដែលមានកំពូល ' + M('O(0, 0), A(6, 0)') + ' និង ' + M('B(0, 5)') + ' ស្មើ ៖', M('15'), [M('30'), M('11'), M('18')], M('S = \\dfrac{1}{2} \\times 6 \\times 5 = 15') + ' ឯកតាផ្ទៃ។'))
    C.append(mcq('hard', 'line', 'តម្លៃនៃ ' + M('m') + ' ដើម្បីឱ្យបន្ទាត់ ' + M('y = mx + 3') + ' ស្របនឹងបន្ទាត់ ' + M('2x - y + 5 = 0') + ' គឺ ៖', M('m = 2'), [M('m = -2'), M('m = \\dfrac{1}{2}'), M('m = 5')], M('2x - y + 5 = 0 \\Rightarrow y = 2x + 5 \\Rightarrow m = 2') + '។'))
    C.append(mcq('hard', 'collinear', 'ក្នុងចំណោមចំណុច ' + M('A(0, 5), B(1, 4), D(3, 0)') + ' ចំណុចទាំងបីនេះ ៖', 'មិនរត់ត្រង់ជួរគ្នាទេ', ['រត់ត្រង់ជួរគ្នា', 'បង្កើតបានត្រីកោណសម័ង្ស', 'ឋិតលើបន្ទាត់តែមួយ'], M('m_{AB} = \\dfrac{4-5}{1-0} = -1') + ' តែ ' + M('m_{BD} = \\dfrac{0-4}{3-1} = -2 \\neq -1') + ' ដូចនេះមិនរត់ត្រង់ជួរទេ។'))
    C.append(mcq('hard', 'line', 'បន្ទាត់ ' + M('y = -3x + 6') + ' និងបន្ទាត់ ' + M('y = 2x + 1') + ' ប្រសព្វគ្នាត្រង់ចំណុច ៖', M('(1, 3)'), [M('(2, 0)'), M('(0, 6)'), M('(1, 5)')], M('-3x + 6 = 2x + 1 \\Rightarrow 5x = 5 \\Rightarrow x = 1 \\Rightarrow y = 3') + ' គឺ ' + M('(1, 3)') + '។'))

    # ================= 4. PISA / APPLICATION MCQs =================
    # 1. Shadow length graph (with FIG_SHADOW)
    C.append(with_img(mcq('pisa', 'pisa', 'ក្រាបបង្ហាញប្រវែងស្រមោលបង្គោលមួយពីម៉ោង 7h ដល់ 17h។ តាមក្រាប ស្រមោលមានប្រវែងខ្លីបំផុតនៅវេលាម៉ោង ៖', 'ម៉ោង 12 ថ្ងៃត្រង់', ['ម៉ោង 7 ព្រឹក', 'ម៉ោង 17 ល្ងាច', 'ម៉ោង 10 ព្រឹក'], 'នៅពេលថ្ងៃត្រង់ ព្រះអាទិត្យនៅត្រង់ក្បាល បង្កើតស្រមោលខ្លីបំផុត។'), FIG_SHADOW))
    # 2. Taxi fare equation
    C.append(mcq('pisa', 'pisa', 'តាក់ស៊ីមួយគិតថ្លៃសេវា ' + M('y = 2\\,000x + 5\\,000') + ' (រៀល) ដែល ' + M('x') + ' ជាចម្ងាយ (km)។ បើអ្នកដំណើរជិះចម្ងាយ ' + M('12\\ \\text{km}') + ' ថ្លៃឈ្នួលត្រូវបង់គឺ ៖', M('29\\,000\\ \\text{រៀល}'), [M('24\\,000\\ \\text{រៀល}'), M('34\\,000\\ \\text{រៀល}'), M('19\\,000\\ \\text{រៀល}')], M('y = 2\\,000(12) + 5\\,000 = 24\\,000 + 5\\,000 = 29\\,000\\ \\text{រៀល}') + '។'))
    # 3. Height vs Age
    C.append(mcq('pisa', 'pisa', 'ក្រាបកម្ពស់តាមអាយុបង្ហាញថា សិស្សម្នាក់មានកម្ពស់ ' + M('130\\ \\text{cm}') + ' នៅអាយុ ១០ ឆ្នាំ និង ' + M('170\\ \\text{cm}') + ' នៅអាយុ ១៨ ឆ្នាំ។ កំណើនកម្ពស់មធ្យមក្នុងមួយឆ្នាំគឺ ៖', M('5\\ \\text{cm/ឆ្នាំ}'), [M('4\\ \\text{cm/ឆ្នាំ}'), M('6\\ \\text{cm/ឆ្នាំ}'), M('8\\ \\text{cm/ឆ្នាំ}')], M('\\dfrac{170 - 130}{18 - 10} = \\dfrac{40}{8} = 5\\ \\text{cm/ឆ្នាំ}') + '។'))
    # 4. Temperature over 24h
    C.append(mcq('pisa', 'pisa', 'ក្រាបសីតុណ្ហភាពប្រចាំថ្ងៃបង្ហាញថា សីតុណ្ហភាពអប្បបរមា ' + M('22^\\circ\\text{C}') + ' នៅម៉ោង 5h ព្រឹក និងអតិបរមា ' + M('34^\\circ\\text{C}') + ' នៅម៉ោង 14h រសៀល។ គម្លាតសីតុណ្ហភាពក្នុងថ្ងៃនោះគឺ ៖', M('12^\\circ\\text{C}'), [M('10^\\circ\\text{C}'), M('14^\\circ\\text{C}'), M('56^\\circ\\text{C}')], M('34^\\circ\\text{C} - 22^\\circ\\text{C} = 12^\\circ\\text{C}') + '។'))
    # 5. Water tank drainage
    C.append(mcq('pisa', 'pisa', 'អាងទឹកមួយមានទឹក 500 L កំពុងបង្ហូរចេញតាមសមីការ ' + M('V = 500 - 25t') + ' ដែល ' + M('t') + ' គិតជា នាទី (mn)។ រយៈពេលដើម្បីបង្ហូរទឹកអស់ពីអាងគឺ ៖', M('20\\ \\text{mn}'), [M('25\\ \\text{mn}'), M('15\\ \\text{mn}'), M('50\\ \\text{mn}')], 'ទឹកអស់ពីអាងពេល ' + M('V = 0 \\Rightarrow 500 - 25t = 0 \\Rightarrow t = 20\\ \\text{mn}') + '។'))

    # ================= 5. WRITING =================
    def W(level, sec, stem, steps, img=None):
        q_ = wr(level, sec, stem, steps)
        if img: q_['img'] = img
        C.append(q_)

    # Writing Easy
    W('easy', 'notion', 'គេឱ្យចំណុច ' + M('A(3, 5), B(-3, 4), C(-4, -3), D(2, -3)') + ' ក្នុងប្លង់កូអរដោនេ។ ចូរបញ្ជាក់កាដ្រង់ដែលចំណុចនីមួយៗស្ថិតនៅ។', [
        (M('A(3, 5)') + ' ៖ អាប់ស៊ីសវិជ្ជមាន អរដោនេវិជ្ជមាន ឋិតក្នុងកាដ្រង់ទី I', 1),
        (M('B(-3, 4)') + ' ៖ អាប់ស៊ីសអវិជ្ជមាន អរដោនេវិជ្ជមាន ឋិតក្នុងកាដ្រង់ទី II', 1),
        (M('C(-4, -3)') + ' ៖ អាប់ស៊ីសអវិជ្ជមាន អរដោនេអវិជ្ជមាន ឋិតក្នុងកាដ្រង់ទី III', 1),
        (M('D(2, -3)') + ' ៖ អាប់ស៊ីសវិជ្ជមាន អរដោនេអវិជ្ជមាន ឋិតក្នុងកាដ្រង់ទី IV', 1),
        ('សន្និដ្ឋាន ៖ ចំណុចទាំង ៤ ឋិតក្នុងកាដ្រង់ខុសៗគ្នាទាំងបួន', 1)])
    W('easy', 'notion', 'ចូរកំណត់កូអរដោនេនៃចំណុចដូចតទៅ ៖ ក. គល់កូអរដោនេ ខ. ចំណុចនៅលើអ័ក្ស ' + M("x'x") + ' មានអាប់ស៊ីស 5 គ. ចំណុចនៅលើអ័ក្ស ' + M("y'y") + ' មានអរដោនេ -4។', [
        ('ក. គល់កូអរដោនេ ' + M('O(0, 0)'), 2),
        ('ខ. ចំណុចលើអ័ក្សអាប់ស៊ីសមានអរដោនេ ' + M('y = 0 \\Rightarrow (5, 0)'), 2),
        ('គ. ចំណុចលើអ័ក្សអរដោនេមានអាប់ស៊ីស ' + M('x = 0 \\Rightarrow (0, -4)'), 1)])

    # Writing Medium
    W('medium', 'line', 'គេឱ្យសមីការបន្ទាត់ ' + M('y = 2x + 4') + '។ ក. រកចំណុចប្រសព្វជាមួយអ័ក្ស ' + M("y'y") + '។ ខ. រកចំណុចប្រសព្វជាមួយអ័ក្ស ' + M("x'x") + '។ គ. សរសេរតារាងតម្លៃលេខពី ' + M('x = -2, 0, 1') + '។', [
        ('ក. ប្រសព្វ ' + M("y'y \\Rightarrow x = 0 \\Rightarrow y = 4 \\Rightarrow (0, 4)"), 1),
        ('ខ. ប្រសព្វ ' + M("x'x \\Rightarrow y = 0 \\Rightarrow 2x + 4 = 0 \\Rightarrow x = -2 \\Rightarrow (-2, 0)"), 2),
        ('គ. តារាង ៖ ' + M('x = -2 \\Rightarrow y = 0') + ' ; ' + M('x = 0 \\Rightarrow y = 4'), 1),
        (M('x = 1 \\Rightarrow y = 6') + ' (កាត់ចំណុច ' + M('(-2, 0), (0, 4), (1, 6)') + ')', 1)])
    W('medium', 'line', 'គេឱ្យសមីការ ' + M('3x + y = 2') + '។ ក. សរសេរសមីការជាទម្រង់ ' + M('y = ax + b') + '។ ខ. បង្ហាញមេគុណប្រាប់ទិស។ គ. រកតម្លៃ ' + M('y') + ' ចំពោះ ' + M('x = 0, 1, 2') + '។', [
        ('ក. ' + M('y = -3x + 2'), 2),
        ('ខ. មេគុណប្រាប់ទិស ' + M('a = -3'), 1),
        ('គ. ចំពោះ ' + M('x = 0 \\Rightarrow y = 2') + ' ; ' + M('x = 1 \\Rightarrow y = -1'), 1),
        (M('x = 2 \\Rightarrow y = -4'), 1)])
    W('medium', 'line', 'គេឱ្យសមីការ ' + M('x - 3 = -3y') + '។ ក. សរសេរ ' + M('y') + ' ជាអនុគមន៍នៃ ' + M('x') + '។ ខ. រកកូអរដោនេ ៣ ចំណុចនៅលើបន្ទាត់នេះ។', [
        ('ក. ' + M('-3y = x - 3 \\Rightarrow 3y = -x + 3'), 2),
        (M('y = -\\dfrac{1}{3}x + 1'), 1),
        ('ខ. យក ' + M('x = -3 \\Rightarrow y = 2 \\Rightarrow (-3, 2)'), 1),
        (M('x = 0 \\Rightarrow (0, 1)') + ' និង ' + M('x = 3 \\Rightarrow (3, 0)'), 1)])
    W('medium', 'line', 'គណនាចម្ងាយរវាងចំណុច ' + M('A(4, 5)') + ' និង ' + M('B(8, 2)') + ' ក្នុងប្លង់កូអរដោនេ។', [
        ('រូបមន្តចម្ងាយ ៖ ' + M('AB = \\sqrt{(x_B - x_A)^2 + (y_B - y_A)^2}'), 1),
        (M('AB = \\sqrt{(8 - 4)^2 + (2 - 5)^2}'), 1),
        (M('= \\sqrt{4^2 + (-3)^2}'), 1),
        (M('= \\sqrt{16 + 9} = \\sqrt{25}'), 1),
        (M('= 5\\ \\text{ឯកតាប្រវែង}'), 1)])

    # Writing Hard
    W('hard', 'line', 'គេឱ្យបន្ទាត់បួន ៖ ' + M('y = 2x, y = 2x+1, y = 2x-3, y = 2x+2') + '។ ក. រកមេគុណប្រាប់ទិសនៃបន្ទាត់នីមួយៗ។ ខ. ទាញសេចក្តីសន្និដ្ឋានអំពីទីតាំងនៃបន្ទាត់ទាំងបួនក្នុងប្លង់។', [
        ('ក. បន្ទាត់នីមួយៗមានមេគុណមុខ ' + M('x') + ' ស្មើគ្នា គឺ ' + M('a = 2'), 2),
        ('ខ. ដោយសារបន្ទាត់ទាំងអស់មានមេគុណប្រាប់ទិសស្មើគ្នា ' + M('(a = 2)'), 1),
        ('បន្ទាត់ទាំងបួនស្របគ្នាទាំងអស់ក្នុងប្លង់កូអរដោនេ', 1),
        (M('(y=2x) \\parallel (y=2x+1) \\parallel (y=2x-3) \\parallel (y=2x+2)'), 1)], FIG_PARALLEL)
    W('hard', 'line', 'រកសមីការបន្ទាត់កាត់តាមចំណុច ' + M('A(0, 3)') + ' និង ' + M('B(3, 6)') + '។', [
        ('សមីការទូទៅ ៖ ' + M('y = ax + b'), 1),
        ('មេគុណប្រាប់ទិស ៖ ' + M('a = \\dfrac{y_B - y_A}{x_B - x_A} = \\dfrac{6 - 3}{3 - 0} = \\dfrac{3}{3} = 1'), 2),
        ('ដោយបន្ទាត់កាត់ ' + M('A(0, 3) \\Rightarrow b = 3'), 1),
        ('ដូចនេះ សមីការបន្ទាត់គឺ ' + M('y = x + 3'), 1)])
    W('hard', 'area', 'គណនាផ្ទៃក្រឡាត្រីកោណកែងដែលបង្កើតដោយបន្ទាត់ ' + M('y = -2x + 4') + ' ជាមួយអ័ក្សកូអរដោនេទាំងពីរ។', [
        ('រកចំណុចប្រសព្វជាមួយអ័ក្សអរដោនេ ៖ ' + M('x = 0 \\Rightarrow y = 4 \\Rightarrow A(0, 4)'), 1),
        ('រកចំណុចប្រសព្វជាមួយអ័ក្សអាប់ស៊ីស ៖ ' + M('y = 0 \\Rightarrow -2x + 4 = 0 \\Rightarrow x = 2 \\Rightarrow B(2, 0)'), 1),
        ('ត្រីកោណ ' + M('OAB') + ' កែងត្រង់គល់ ' + M('O(0, 0)') + ' មានប្រវែង ' + M('OA = 4') + ' និង ' + M('OB = 2'), 1),
        ('ផ្ទៃក្រឡា ៖ ' + M('S = \\dfrac{1}{2} \\times OA \\times OB = \\dfrac{1}{2} \\times 4 \\times 2'), 1),
        (M('= 4\\ \\text{ឯកតាផ្ទៃ}'), 1)])
    W('hard', 'collinear', 'គេឱ្យចំណុច ' + M('A(1, 2), B(2, 4), C(3, 6)') + '។ ក. រកមេគុណប្រាប់ទិស ' + M('m_{AB}') + ' និង ' + M('m_{BC}') + '។ ខ. បញ្ជាក់ថាតើចំណុចទាំងបីរត់ត្រង់ជួរគ្នាឬទេ។', [
        ('ក. ' + M('m_{AB} = \\dfrac{4 - 2}{2 - 1} = \\dfrac{2}{1} = 2'), 2),
        (M('m_{BC} = \\dfrac{6 - 4}{3 - 2} = \\dfrac{2}{1} = 2'), 1),
        ('ខ. ដោយសារ ' + M('m_{AB} = m_{BC} = 2') + ' និងមានចំណុច ' + M('B') + ' រួម', 1),
        ('ដូចនេះ ចំណុចទាំងបី ' + M('A, B, C') + ' រត់ត្រង់ជួរគ្នា (ឋិតលើបន្ទាត់ ' + M('y = 2x') + ')', 1)])

    # Writing PISA
    W('pisa', 'pisa', 'ក្រាបកម្ពស់បង្ហាញថាសិស្សម្នាក់មានកម្ពស់ ' + M('130\\ \\text{cm}') + ' នៅអាយុ ១០ ឆ្នាំ និង ' + M('170\\ \\text{cm}') + ' នៅអាយុ ១៨ ឆ្នាំ។ ក. រកអត្រាកំណើនកម្ពស់មធ្យមក្នុងមួយឆ្នាំ។ ខ. សរសេរសមីការបន្ទាត់កម្ពស់ ' + M('h') + ' តាមអាយុ ' + M('t') + '។ គ. ប៉ាន់ស្មានកម្ពស់នៅអាយុ ១៤ ឆ្នាំ។', [
        ('ក. អត្រាកំណើន ៖ ' + M('a = \\dfrac{170 - 130}{18 - 10} = \\dfrac{40}{8} = 5\\ \\text{cm/ឆ្នាំ}'), 2),
        ('ខ. ' + M('h - 130 = 5(t - 10) \\Rightarrow h = 5t + 80'), 1),
        ('គ. នៅអាយុ ' + M('t = 14') + ' ៖ ' + M('h = 5(14) + 80 = 70 + 80'), 1),
        (M('h = 150\\ \\text{cm}'), 1)])
    W('pisa', 'pisa', 'តាក់ស៊ីមួយគិតថ្លៃសេវា ' + M('y = 2\\,000x + 5\\,000') + ' (រៀល) ដែល ' + M('x') + ' ជាចម្ងាយ (km)។ ក. ប្រាប់អត្ថន័យនៃលេខ 5 000 និងលេខ 2 000។ ខ. គណនាថ្លៃឈ្នួលបើជិះបាន 15 km។ គ. បើអ្នកដំណើរមានប្រាក់ 45 000 រៀល រកចម្ងាយអតិបរមាដែលអាចជិះបាន។', [
        ('ក. ' + M('5\\,000') + ' ជាថ្លៃសេវាចាប់ផ្តើមដំបូង ; ' + M('2\\,000') + ' ជាថ្លៃឈ្នួលក្នុង 1 km', 1),
        ('ខ. ជិះ ' + M('15\\ \\text{km} \\Rightarrow y = 2\\,000(15) + 5\\,000 = 30\\,000 + 5\\,000 = 35\\,000\\ \\text{រៀល}'), 2),
        ('គ. ' + M('2\\,000x + 5\\,000 \\le 45\\,000 \\Rightarrow 2\\,000x \\le 40\\,000'), 1),
        (M('x \\le 20\\ \\text{km}') + ' (ចម្ងាយអតិបរមា ២០ km)', 1)])
    W('pisa', 'pisa', 'អាងទឹកមួយមានទឹក 500 L ត្រូវបានបង្ហូរចេញតាមសមីការ ' + M('V = 500 - 25t') + ' (' + M('t') + ' គិតជា នាទី)។ ក. រកបរិមាណទឹកនៅពេល ' + M('t = 0') + '។ ខ. រកបរិមាណទឹកក្រោយបង្ហូរបាន 10 នាទី។ គ. រករយៈពេលដើម្បីបង្ហូរទឹកអស់ពីអាង។', [
        ('ក. នៅពេល ' + M('t = 0 \\Rightarrow V = 500\\ \\text{L}') + ' (ទឹកពេញអាង)', 1),
        ('ខ. នៅពេល ' + M('t = 10 \\Rightarrow V = 500 - 25(10) = 500 - 250'), 1),
        (M('V = 250\\ \\text{L}'), 1),
        ('គ. ទឹកអស់ពីអាងពេល ' + M('V = 0 \\Rightarrow 500 - 25t = 0'), 1),
        (M('25t = 500 \\Rightarrow t = 20\\ \\text{នាទី}'), 1)])
    W('pisa', 'pisa', 'ដ្យាក្រាមស្រមោលបង្ហាញប្រវែងស្រមោលបង្គោលមួយពីម៉ោង 7h ដល់ 17h។ ក. រកម៉ោងដែលស្រមោលមានប្រវែងវែងជាងគេ។ ខ. រកម៉ោងដែលស្រមោលមានប្រវែងខ្លីជាងគេ។ គ. ពន្យល់មូលហេតុវិទ្យាសាស្ត្រ។', [
        ('ក. ស្រមោលវែងជាងគេនៅម៉ោង 7h ព្រឹក និងម៉ោង 17h ល្ងាច', 1),
        ('ខ. ស្រមោលខ្លីជាងគេនៅម៉ោង 12h ថ្ងៃត្រង់', 2),
        ('គ. មូលហេតុ ៖ នៅពេលព្រឹកនិងល្ងាច ពន្លឺព្រះអាទិត្យចាំងជម្រាលខ្លាំងបង្កើតស្រមោលវែង', 1),
        ('រីឯនៅម៉ោង ១២ ថ្ងៃត្រង់ ព្រះអាទិត្យនៅត្រង់ក្បាល បង្កើតស្រមោលខ្លីបំផុត', 1)], FIG_SHADOW)
    W('pisa', 'pisa', 'ក្រាបសីតុណ្ហភាពមួយបង្ហាញថាសីតុណ្ហភាពអប្បបរមា ' + M('22^\\circ\\text{C}') + ' នៅម៉ោង 5h ព្រឹក និងអតិបរមា ' + M('34^\\circ\\text{C}') + ' នៅម៉ោង 14h រសៀល។ ក. គណនាគម្លាតសីតុណ្ហភាពប្រចាំថ្ងៃ។ ខ. ប៉ាន់ស្មានសីតុណ្ហភាពមធ្យមនៃថ្ងៃនោះ។', [
        ('ក. គម្លាតសីតុណ្ហភាព ៖ ' + M('\\Delta T = T_{\\max} - T_{\\min}'), 1),
        (M('= 34^\\circ\\text{C} - 22^\\circ\\text{C} = 12^\\circ\\text{C}'), 2),
        ('ខ. សីតុណ្ហភាពមធ្យម ៖ ' + M('T_{\\text{avg}} = \\dfrac{T_{\\max} + T_{\\min}}{2}'), 1),
        (M('= \\dfrac{34 + 22}{2} = \\dfrac{56}{2} = 28^\\circ\\text{C}'), 1)])

    return C
