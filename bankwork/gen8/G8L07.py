from lib import *
import sympy as sp
from sympy import symbols, Rational as Q_
from sympy.parsing.sympy_parser import parse_expr
import re as _re

LESSON = 'សមីការដឺក្រេទី ១ មានមួយអញ្ញាត'
x, y, z, a, b, c, t, m, n, d, k = symbols('x y z a b c t m n d k')
_LD = {s_.name: s_ for s_ in (x, y, z, a, b, c, t, m, n, d, k)}

def L(e): return sp.latex(e).replace(r"\frac", r"\dfrac")

def _plain_tex(sx):
    out = _re.sub(r'\*\*(\d+)', r'^{\1}', sx)
    out = _re.sub(r'(?<=[0-9])\*(?=[0-9])', ' \\times ', out)
    return out.replace('*', '').replace('+-', '-')

def _scan(s_, fn_plain, fn_frac):
    out, i, buf = '', 0, ''
    while i < len(s_):
        ch = s_[i]
        if ch == '[':
            dep, j = 1, i + 1
            while dep:
                dep += (s_[j] == '[') - (s_[j] == ']'); j += 1
            inner = s_[i + 1:j - 1]
            dep, cut = 0, None
            for q_, c_ in enumerate(inner):
                if c_ == '[': dep += 1
                elif c_ == ']': dep -= 1
                elif c_ == '|' and dep == 0: cut = q_; break
            out += fn_plain(buf) + fn_frac(inner[:cut], inner[cut + 1:]); buf = ''; i = j
        else: buf += ch; i += 1
    return out + fn_plain(buf)

def tex(s_): return _scan(s_, _plain_tex, lambda p_, q_: r'\dfrac{%s}{%s}' % (tex(p_), tex(q_)))
def py(s_): return _scan(s_, lambda z_: z_, lambda p_, q_: '((%s)/(%s))' % (py(p_), py(q_)))
def PE(s_): return parse_expr(py(s_), local_dict=_LD)
def EQ(lhs, rhs): return M(tex(lhs) + ' = ' + tex(rhs))

def roots(lhs, rhs, var=x):
    e = sp.simplify(PE(lhs) - PE(rhs))
    if e == 0: return 'all'
    if not e.has(var): return 'none'
    sol = [r_ for r_ in sp.solve(sp.Eq(PE(lhs), PE(rhs)), var) if r_.is_real]
    if not sol: return 'none'
    return sorted(sol, key=lambda r_: float(r_))

def RT(rs, var='x'):
    if rs == 'all': return 'គ្រប់តម្លៃនៃ ' + M(var) + ' (ឫសច្រើនរាប់មិនអស់)'
    if rs == 'none': return 'គ្មានឫស'
    return ' ឬ '.join(M(f'{var} = {L(r_)}') for r_ in rs)

def with_img(q_, s_): q_['img'] = s_; return q_

C = []

def uniq(correct, cands, k_=3):
    out = [correct]
    for c_ in cands:
        if c_ not in out: out.append(c_)
        if len(out) == k_ + 1: break
    assert len(out) == k_ + 1, ('wrongs', correct)
    return out[1:]

def solve_mcq(level, sec, lhs, rhs, prefix='ដោះស្រាយសមីការ ', var=x):
    rs = roots(lhs, rhs, var)
    nm = var.name
    correct = RT(rs, nm)
    c_ = []
    if isinstance(rs, list):
        r0 = rs[0]
        c_ = [RT([-r for r in rs][::-1], nm), RT([r + 1 for r in rs], nm), RT([r * 2 for r in rs], nm), RT([1 / r if r != 0 else r + 2 for r in rs], nm), RT([r - 2 for r in rs], nm), RT([-r - 1 for r in rs], nm)]
        if len(rs) > 1: c_.insert(0, RT([rs[0]], nm)); c_.insert(1, RT([rs[-1] * -1, rs[0]], nm))
        c_ += ['គ្មានឫស', 'គ្រប់តម្លៃនៃ ' + M(nm) + ' (ឫសច្រើនរាប់មិនអស់)']
    elif rs == 'all':
        c_ = [RT([0], nm), 'គ្មានឫស', RT([1], nm), RT([-1], nm)]
    else:
        c_ = [RT([0], nm), 'គ្រប់តម្លៃនៃ ' + M(nm) + ' (ឫសច្រើនរាប់មិនអស់)', RT([1], nm), RT([-1], nm)]
    sol = ('ដោះស្រាយ ៖ ' + (' ; '.join(M(f'{nm} = {L(r_)}') for r_ in rs) if isinstance(rs, list) else ('សមីការពិតគ្រប់តម្លៃ' if rs == 'all' else 'សមភាពមិនពិត គ្មានឫស'))) + '។'
    C.append(mcq(level, sec, prefix + EQ(lhs, rhs) + ' ៖', correct, uniq(correct, c_), sol))

# ---------- figures (Transparent background, Mathcad Italic variables, Upright serif dimensions) ----------
FIG_PERI = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 300 130' width='300' height='130'>
  <rect x='25' y='20' width='210' height='70' fill='#e0f2fe' stroke='#0369a1' stroke-width='2' rx='2'/>
  <text x='130' y='60' text-anchor='middle' font-family='Khmer OS Battambang,Noto Sans Khmer,serif' font-size='13' fill='#0f172a'>បរិមាត្រ <tspan font-family='Mathcad UniMath Italic,Times New Roman,serif' font-style='italic'>P</tspan> = <tspan font-family='Times New Roman,serif' font-style='normal'>148 cm</tspan></text>
  <line x1='25' y1='105' x2='235' y2='105' stroke='#475569' stroke-width='1.2'/>
  <polyline points='30,102 25,105 30,108' fill='none' stroke='#475569' stroke-width='1.2'/>
  <polyline points='230,102 235,105 230,108' fill='none' stroke='#475569' stroke-width='1.2'/>
  <text x='130' y='122' text-anchor='middle' font-family='Mathcad UniMath Italic,Times New Roman,serif' font-style='italic' font-size='14' fill='#0f172a'>a = <tspan font-style='normal'>3</tspan>b + <tspan font-style='normal'>17</tspan></text>
  <line x1='250' y1='20' x2='250' y2='90' stroke='#475569' stroke-width='1.2'/>
  <polyline points='247,25 250,20 253,25' fill='none' stroke='#475569' stroke-width='1.2'/>
  <polyline points='247,85 250,90 253,85' fill='none' stroke='#475569' stroke-width='1.2'/>
  <text x='265' y='60' text-anchor='middle' font-family='Mathcad UniMath Italic,Times New Roman,serif' font-style='italic' font-size='15' fill='#0f172a'>b</text>
</svg>"""

FIG_EXT = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 340 170' width='340' height='170'>
  <rect x='50' y='25' width='180' height='70' fill='#e0f2fe' stroke='#0284c7' stroke-width='2'/>
  <text x='140' y='62' text-anchor='middle' font-family='Khmer OS Battambang,Noto Sans Khmer,serif' font-size='12' fill='#0369a1'>ផ្ទៃចាស់ <tspan font-family='Times New Roman,serif' font-style='normal' font-weight='bold'>18 cm²</tspan></text>
  <rect x='230' y='25' width='75' height='70' fill='#fef3c7' stroke='#d97706' stroke-width='1.8' stroke-dasharray='5 3'/>
  <rect x='50' y='95' width='180' height='35' fill='#fee2e2' stroke='#dc2626' stroke-width='1.8' stroke-dasharray='5 3'/>
  <rect x='230' y='95' width='75' height='35' fill='#f3f4f6' stroke='#9ca3af' stroke-width='1.8' stroke-dasharray='5 3'/>
  <line x1='50' y1='15' x2='230' y2='15' stroke='#475569' stroke-width='1.2'/>
  <polyline points='55,12 50,15 55,18' fill='none' stroke='#475569' stroke-width='1.2'/>
  <polyline points='225,12 230,15 225,18' fill='none' stroke='#475569' stroke-width='1.2'/>
  <text x='140' y='11' text-anchor='middle' font-family='Times New Roman,serif' font-size='13' font-weight='bold' fill='#0f172a'>9 cm</text>
  <line x1='230' y1='15' x2='305' y2='15' stroke='#d97706' stroke-width='1.2'/>
  <polyline points='235,12 230,15 235,18' fill='none' stroke='#d97706' stroke-width='1.2'/>
  <polyline points='300,12 305,15 300,18' fill='none' stroke='#d97706' stroke-width='1.2'/>
  <text x='267' y='11' text-anchor='middle' font-family='Mathcad UniMath Italic,Times New Roman,serif' font-style='italic' font-size='13' fill='#b45309'>x <tspan font-style='normal' font-family='Times New Roman,serif'>cm</tspan></text>
  <line x1='38' y1='25' x2='38' y2='95' stroke='#475569' stroke-width='1.2'/>
  <polyline points='35,30 38,25 41,30' fill='none' stroke='#475569' stroke-width='1.2'/>
  <polyline points='35,90 38,95 41,90' fill='none' stroke='#475569' stroke-width='1.2'/>
  <text x='28' y='64' text-anchor='end' font-family='Times New Roman,serif' font-size='13' font-weight='bold' fill='#0f172a'>2 cm</text>
  <line x1='38' y1='95' x2='38' y2='130' stroke='#dc2626' stroke-width='1.2'/>
  <polyline points='35,100 38,95 41,100' fill='none' stroke='#dc2626' stroke-width='1.2'/>
  <polyline points='35,125 38,130 41,125' fill='none' stroke='#dc2626' stroke-width='1.2'/>
  <text x='28' y='117' text-anchor='end' font-family='Times New Roman,serif' font-size='13' font-weight='bold' fill='#b91c1c'>1 cm</text>
  <text x='177' y='155' text-anchor='middle' font-family='Khmer OS Battambang,Noto Sans Khmer,serif' font-size='12' fill='#475569'>ផ្ទៃថ្មី = ២ × ផ្ទៃចាស់ = <tspan font-family='Times New Roman,serif' font-style='normal' font-weight='bold'>36 cm²</tspan></text>
</svg>"""

FIG_ROUTE = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 380 130' width='380' height='130'>
  <line x1='40' y1='65' x2='340' y2='65' stroke='#1e293b' stroke-width='2'/>
  <circle cx='40' cy='65' r='5' fill='#2563eb'/>
  <circle cx='180' cy='65' r='5' fill='#dc2626'/>
  <circle cx='340' cy='65' r='5' fill='#16a34a'/>
  <text x='40' y='90' text-anchor='middle' font-family='Khmer OS Battambang,Noto Sans Khmer,serif' font-size='13' fill='#1e293b'>ផ្ទះ</text>
  <text x='180' y='90' text-anchor='middle' font-family='Khmer OS Battambang,Noto Sans Khmer,serif' font-size='13' fill='#dc2626'>បង្គោល ១០ km (ជួបគ្នា)</text>
  <text x='340' y='90' text-anchor='middle' font-family='Khmer OS Battambang,Noto Sans Khmer,serif' font-size='13' fill='#1e293b'>សាលា</text>
  <path d='M 40,50 Q 110,32 180,50' fill='none' stroke='#2563eb' stroke-width='1.5'/>
  <text x='110' y='30' text-anchor='middle' font-family='Times New Roman,serif' font-size='13' font-weight='bold' fill='#1d4ed8'>10 km</text>
  <path d='M 180,50 Q 260,32 340,50' fill='none' stroke='#64748b' stroke-width='1.4' stroke-dasharray='4 3'/>
  <text x='260' y='30' text-anchor='middle' font-family='Mathcad UniMath Italic,Times New Roman,serif' font-style='italic' font-size='13' fill='#475569'>x - <tspan font-style='normal'>10</tspan></text>
  <line x1='40' y1='112' x2='340' y2='112' stroke='#475569' stroke-width='1.2'/>
  <polyline points='45,109 40,112 45,115' fill='none' stroke='#475569' stroke-width='1.2'/>
  <polyline points='335,109 340,112 335,115' fill='none' stroke='#475569' stroke-width='1.2'/>
  <text x='190' y='125' text-anchor='middle' font-family='Khmer OS Battambang,Noto Sans Khmer,serif' font-size='12' fill='#475569'>ចម្ងាយសរុប <tspan font-family='Mathcad UniMath Italic,Times New Roman,serif' font-style='italic'>x</tspan></text>
</svg>"""

def cands():
    global C
    C = []
    # ================= notion =================
    C.append(mcq('easy', 'notion', 'សមីការដឺក្រេទី ១ មានមួយអញ្ញាតមានរាងទូទៅ (ក្រោយសម្រួល)៖', M('ax + b = 0\\ (a \\neq 0)'), [M('ax^2 + b = 0'), M('ax + by = 0'), M('\\dfrac{a}{x} + b = 0')], 'មានអញ្ញាតតែមួយ ហើយនិទស្សន្តស្មើ ' + M(1) + '។'))
    C.append(mcq('easy', 'notion', 'តម្លៃនៃអញ្ញាតដែលធ្វើឱ្យអង្គទាំងពីរនៃសមីការស្មើគ្នា ហៅថា៖', 'ឫសនៃសមីការ', ['មេគុណ', 'និទស្សន្ត', 'ដឺក្រេ'], 'ជាឫសនៃសមីការ។'))
    C.append(mcq('easy', 'notion', 'ក្នុងចំណោមតម្លៃ ' + M('m = 12,\\ 3,\\ 6') + ' តម្លៃណាជាឫសនៃ ' + M('2m + 6 = 12') + '?', M('m = 3'), [M('m = 12'), M('m = 6'), M('\\text{គ្មានតម្លៃណាមួយ}')], M('2(3) + 6 = 12') + ' ពិត។'))
    C.append(mcq('easy', 'notion', 'បីដងនៃចំនួនមួយថែម ' + M(21) + ' ស្មើ ' + M(85) + '។ សមីការគឺ៖', M('3x + 21 = 85'), [M('3(x + 21) = 85'), M('3x - 21 = 85'), M('x + 63 = 85')], 'តាង ' + M('x') + ' ជាចំនួននោះ។'))
    C.append(mcq('easy', 'notion', 'ពីរដងនៃចំនួនមួយដក ' + M(15) + ' ស្មើ ' + M(75) + '។ ចំនួននោះគឺ៖', M(45), [M(30), M(90), M(60)], M('2t - 15 = 75') + ' នាំឱ្យ ' + M('t = 45') + '។'))
    C.append(mcq('easy', 'notion', 'សមីការ ' + M('(x+3)(x+5) = x^2 + 6x + 3') + ' សមមូលនឹងសមីការដឺក្រេទី ១៖', M('2x + 12 = 0'), [M('2x + 18 = 0'), M('x^2 + 12 = 0'), M('14x = 0')], M('x^2 + 8x + 15 - x^2 - 6x - 3 = 2x + 12') + '។'))

    # ================= easy equations =================
    solve_mcq('easy', 'basic', '2*x+3', '12'); solve_mcq('easy', 'basic', '2*x-3', '11'); solve_mcq('easy', 'basic', '6*x+15', '45')
    solve_mcq('easy', 'basic', '8*y', '25+3*y', var=y); solve_mcq('easy', 'basic', '5*m-2', '7-4*m', var=m); solve_mcq('easy', 'basic', 'a+40', '6*a', var=a)
    solve_mcq('easy', 'basic', '3*x-2', '-17'); solve_mcq('easy', 'basic', '3*x+5', '2*x-3'); solve_mcq('easy', 'basic', '2*n+5', '25', var=n)
    C.append(mcq('easy', 'zero', 'ដោះស្រាយ ' + M('x(x-3) = 0') + '៖', M('x = 0') + ' ឬ ' + M('x = 3'), [M('x = 3') + ' តែប៉ុណ្ណោះ', M('x = 0') + ' តែប៉ុណ្ណោះ', M('x = -3') + ' ឬ ' + M('x = 0')], 'ផលគុណស្មើសូន្យ លុះត្រាតែកត្តាណាមួយស្មើសូន្យ។'))
    C.append(mcq('easy', 'zero', 'ដោះស្រាយ ' + M('x^2 - 9 = 0') + '៖', M('x = 3') + ' ឬ ' + M('x = -3'), [M('x = 3') + ' តែប៉ុណ្ណោះ', M('x = 9') + ' ឬ ' + M('x = -9'), M('x = 0')], M('(x-3)(x+3) = 0') + '។'))

    # ================= medium =================
    solve_mcq('medium', 'basic', '3*(x-3)', '12'); solve_mcq('medium', 'basic', '3*(x+4)', '5*x'); solve_mcq('medium', 'basic', '4*(a+6)', '24*a', var=a)
    solve_mcq('medium', 'basic', '9*(n-8)', '-18*n', var=n); solve_mcq('medium', 'basic', '4*(x-2)', '3*(x+1)'); solve_mcq('medium', 'basic', '8-2*(x+1)', '-3*x+1')
    solve_mcq('medium', 'frac', '[3|5]*x-4', '14'); solve_mcq('medium', 'frac', '[3*m|4]', '15', var=m); solve_mcq('medium', 'frac', '2*x+[1|2]', '[2|3]')
    solve_mcq('medium', 'frac', '[x|4]', '9-[3*x|4]'); solve_mcq('medium', 'frac', '[2*x|5]+[x|4]', '[26|5]'); solve_mcq('medium', 'frac', '[3|5]*x+3', '[1|5]*x-7')
    solve_mcq('medium', 'special', '-3*(2*n-5)', '[1|2]*(-12*n+30)', var=n)
    solve_mcq('medium', 'special', '-3*y+5*(6-y)', '4*(1-2*y)', var=y)
    solve_mcq('medium', 'special', '3*(x+1)-5', '3*x-2')
    solve_mcq('medium', 'zero', '(x-3)*(2*x-8)', '0'); solve_mcq('medium', 'zero', '(a+12)*(a-4)', '2*a*(a-4)', var=a); solve_mcq('medium', 'zero', '(a+3)**2-25', '0', var=a)
    solve_mcq('medium', 'zero', 'x**2+64', '16*x'); solve_mcq('medium', 'zero', '(x-12)*(x-7)', '0'); solve_mcq('medium', 'zero', '(2*x-1)**2', '(x+3)**2')

    # ================= hard =================
    solve_mcq('hard', 'frac', '[3*x|4]-[x-5|3]', '[x|2]'); solve_mcq('hard', 'frac', '[y-12|5]+[3*y|4]', '[y+6|2]', var=y); solve_mcq('hard', 'frac', '[5|6]*x+1', '[1|4]-[1|2]*x')
    solve_mcq('hard', 'zero', '2*(x-3)', 'x*(3-x)'); solve_mcq('hard', 'zero', '4*x**2*(x+1)', '9*(x+1)'); solve_mcq('hard', 'zero', '(x-7)**2', '(5*x-6)**2')
    solve_mcq('hard', 'zero', '8*(x+1)**3', '27*(2*x-1)**3'); solve_mcq('hard', 'zero', '4*a**3-12*a**2+8*a', '0', var=a); solve_mcq('hard', 'zero', '(2*x-3)**2', '(2*x-3)*(x+1)'); solve_mcq('hard', 'zero', '(x-3)*(5*x+3)', '7*(5*x+3)')
    C.append(mcq('hard', 'error', 'វិបុលដោះស្រាយ ' + M('6m - 15 = 10m - 25') + ' ដោយសរសេរ ' + M('3(2m-5) = 5(2m-5)') + ' រួចចែកអង្គទាំងពីរនឹង ' + M('2m-5') + ' បាន ' + M('3 = 5') + ' (គ្មានឫស)។ កំហុសរបស់វិបុលគឺ៖', 'ចែកនឹង ' + M('2m-5') + ' ដែលអាចស្មើសូន្យ (ពេល ' + M('m = 2.5') + ')', ['ដកអង្គទាំងពីរខុស', 'ដាក់កត្តារួមខុស', 'គណនា ' + M('6m - 10m') + ' ខុស'], 'សមីការពិតមានឫស ' + M('m = \\dfrac{5}{2}') + '។'))

    # ================= word problems (medium / hard) =================
    C.append(mcq('medium', 'word', 'ចម្ការកៅស៊ូរាងចតុកោណកែងមានកន្លះបរិមាត្រ ' + M('3\\,528\\ \\text{m}') + ' បណ្តោយស្មើទទឹង ' + M(6) + ' ដងថែម ' + M('14\\ \\text{m}') + '។ ទទឹងគឺ៖', M('502\\ \\text{m}'), [M('504\\ \\text{m}'), M('3\\,514\\ \\text{m}'), M('588\\ \\text{m}')], M('7x + 14 = 3\\,528') + ' នាំឱ្យ ' + M('x = 502') + '។'))
    C.append(mcq('medium', 'word', 'ផលបូកបីចំនួនគត់តគ្នាស្មើ ' + M(300) + '។ ចំនួនតូចជាងគេគឺ៖', M(99), [M(100), M(98), M(101)], M('a + (a+1) + (a+2) = 300') + ' នាំឱ្យ ' + M('a = 99') + '។'))
    C.append(mcq('medium', 'word', 'ផលបូកបីចំនួនគត់គូតគ្នាស្មើ ' + M(-12) + '។ ចំនួនធំជាងគេគឺ៖', M(-2), [M(-6), M(-4), M(0)], M('x + (x+2) + (x+4) = -12') + ' នាំឱ្យ ' + M('x = -6') + ' ; ' + M('-6, -4, -2') + '។'))
    C.append(mcq('medium', 'word', 'ផលបូកប្រាំចំនួនគត់តគ្នាស្មើ ' + M(520) + '។ ចំនួនធំជាងគេគឺ៖', M(106), [M(102), M(104), M(108)], M('5n + 10 = 520') + ' នាំឱ្យ ' + M('n = 102') + ' ; ធំជាងគេ ' + M(106) + '។'))
    C.append(mcq('medium', 'word', 'កសិករនិងគោសរុប ' + M(36) + ' ជើងសរុប ' + M(100) + '។ ចំនួនកសិករគឺ៖', M(22), [M(14), M(18), M(25)], M('2m + 4(36 - m) = 100') + ' នាំឱ្យ ' + M('m = 22') + '។'))
    C.append(mcq('medium', 'word', 'សូផាតអាយុ ' + M(51) + ' ឆ្នាំ រស្មីអាយុ ' + M(21) + ' ឆ្នាំ។ ប៉ុន្មានឆ្នាំទៀតអាយុសូផាតស្មើពីរដងរស្មី?', M(9) + ' ឆ្នាំ', [M(30) + ' ឆ្នាំ', M(12) + ' ឆ្នាំ', M(7) + ' ឆ្នាំ'], M('51 + t = 2(21 + t)') + ' នាំឱ្យ ' + M('t = 9') + '។'))
    C.append(mcq('hard', 'word', 'ស៊ីណាអាយុ ' + M('x') + ' ម្តាយអាយុ ' + M('3x') + '។ ពេលស៊ីណាអាយុស្មើអាយុម្តាយសព្វថ្ងៃ ផលបូកអាយុអ្នកទាំងពីរ ' + M(112) + '។ អាយុស៊ីណាសព្វថ្ងៃគឺ៖', M(14) + ' ឆ្នាំ', [M(21) + ' ឆ្នាំ', M(28) + ' ឆ្នាំ', M(42) + ' ឆ្នាំ'], M('3x + 5x = 112') + ' នាំឱ្យ ' + M('x = 14') + '។'))

    # ================= PISA / APPLICATION MCQs =================
    # 1. Bicycle problem (with FIG_ROUTE)
    C.append(with_img(mcq('pisa', 'pisa', 'ធីតាជិះកង់ ' + M('15\\ \\text{km/h}') + ' លក្ខិណាដើរ ' + M('4\\ \\text{km/h}') + ' ចេញពីផ្ទះម៉ោងជាមួយគ្នាទៅសាលា។ ធីតាដល់សាលារួចត្រឡប់មកវិញ ជួបលក្ខិណាត្រង់បង្គោល ' + M('10\\ \\text{km}') + ' (គិតពីផ្ទះ)។ ចម្ងាយពីផ្ទះទៅសាលាគឺ៖', M('23.75\\ \\text{km}'), [M('20\\ \\text{km}'), M('26\\ \\text{km}'), M('30\\ \\text{km}')], 'រយៈពេលលក្ខិណា ' + M('10/4') + ' ស្មើពេលធីតា ' + M('(2x-10)/15') + ' នាំឱ្យ ' + M('8x - 40 = 150 \\Rightarrow x = 23.75\\ \\text{km}') + '។'), FIG_ROUTE))
    # 2. Women exercise group
    C.append(mcq('pisa', 'pisa', 'ក្រុមស្ត្រីហាត់ប្រាណ ៖ «ចំនួនពួកយើង បូកចំនួនពួកយើង បូកពាក់កណ្តាលពួកយើង បូក ' + M('\\dfrac{1}{4}') + ' នៃពួកយើង និងស៊ីថាម្នាក់ទៀត ស្មើ ' + M(100) + ' នាក់»។ ចំនួនស្ត្រីក្នុងក្រុមគឺ៖', M(36) + ' នាក់', [M(40) + ' នាក់', M(33) + ' នាក់', M(45) + ' នាក់'], M('x + x + \\dfrac{x}{2} + \\dfrac{x}{4} + 1 = 100 \\Rightarrow \\dfrac{11x}{4} = 99 \\Rightarrow x = 36') + ' នាក់។'))
    # 3. Mountain hiker
    C.append(mcq('pisa', 'pisa', 'អ្នកថ្មើរជើងម្នាក់ឡើងភ្នំក្នុងល្បឿនមធ្យម ' + M('300\\ \\text{m/h}') + ' និងចុះមកវិញក្នុងល្បឿន ' + M('450\\ \\text{m/h}') + '។ ចេញដំណើរម៉ោង ' + M('7\\text{h}\\ 00') + ' ដល់កន្លែងដើមវិញម៉ោង ' + M('18\\text{h}\\ 45') + ' ដោយសម្រាកលើកំពូលភ្នំ ' + M('4\\text{h}\\ 15') + '។ ចម្ងាយផ្លូវពីជើងភ្នំដល់កំពូលភ្នំគឺ៖', M('1\\,350\\ \\text{m}'), [M('1\\,800\\ \\text{m}'), M('2\\,250\\ \\text{m}'), M('900\\ \\text{m}')], 'ពេលធ្វើដំណើរសរុប ' + M('11.75 - 4.25 = 7.5\\ \\text{h}') + '។ ' + M('\\dfrac{d}{300} + \\dfrac{d}{450} = 7.5 \\Rightarrow \\dfrac{5d}{900} = 7.5 \\Rightarrow d = 1\\,350\\ \\text{m}') + '។'))
    # 4. Extended rectangle (with FIG_EXT)
    C.append(with_img(mcq('pisa', 'pisa', 'ចតុកោណកែងមួយមានទទឹង ' + M('2\\ \\text{cm}') + ' និងបណ្តោយ ' + M('9\\ \\text{cm}') + '។ បើគេបង្កើនទទឹង ' + M('1\\ \\text{cm}') + ' និងបណ្តោយ ' + M('x\\ \\text{cm}') + ' ផ្ទៃក្រឡាថ្មីស្មើពីរដងនៃផ្ទៃក្រឡាចាស់។ តម្លៃនៃ ' + M('x') + ' គឺ៖', M('3\\ \\text{cm}'), [M('4.5\\ \\text{cm}'), M('6\\ \\text{cm}'), M('9\\ \\text{cm}')], 'ផ្ទៃចាស់ ' + M('18\\ \\text{cm}^2') + '។ ផ្ទៃថ្មី ' + M('3(9 + x) = 36 \\Rightarrow 9 + x = 12 \\Rightarrow x = 3\\ \\text{cm}') + '។'), FIG_EXT))
    # 5. Perimeter rectangle (with FIG_PERI)
    C.append(with_img(mcq('pisa', 'pisa', 'ចតុកោណកែងមានបរិមាត្រ ' + M('148\\ \\text{cm}') + ' ហើយបណ្តោយវែងជាងបីដងទទឹងចំនួន ' + M('17\\ \\text{cm}') + '។ ទទឹងនៃចតុកោណកែងនេះគឺ៖', M('14.25\\ \\text{cm}'), [M('14\\ \\text{cm}'), M('59.75\\ \\text{cm}'), M('18.5\\ \\text{cm}')], 'សមីការ ' + M('2(b + 3b + 17) = 148 \\Rightarrow 8b = 114 \\Rightarrow b = 14.25\\ \\text{cm}') + '។'), FIG_PERI))
    # 6. Classroom test fraction
    C.append(mcq('pisa', 'pisa', 'នៅក្នុងថ្នាក់មួយ សិស្ស ' + M('\\dfrac{1}{3}') + ' ធ្វើត្រូវទាំងអស់ ' + M('\\dfrac{2}{5}') + ' ធ្វើត្រូវពាក់កណ្តាល ហើយសិស្ស ' + M(8) + ' នាក់ធ្វើមិនត្រូវ។ ថ្នាក់មានសិស្សសរុប៖', M(30) + ' នាក់', [M(24) + ' នាក់', M(36) + ' នាក់', M(40) + ' នាក់'], M('N - \\dfrac{N}{3} - \\dfrac{2N}{5} = 8 \\Rightarrow \\dfrac{4N}{15} = 8 \\Rightarrow N = 30') + ' នាក់។'))
    # 7. Land rented perimeter
    C.append(mcq('pisa', 'pisa', 'ដីចម្ការរាងចតុកោណកែងមានទទឹង ' + M('x') + ' បណ្តោយ ' + M('x + 6') + ' ហើយបរិមាត្រ ' + M('44\\ \\text{m}') + '។ តម្លៃនៃ ' + M('x') + ' ស្មើ៖', M('8\\ \\text{m}'), [M('11\\ \\text{m}'), M('16\\ \\text{m}'), M('10\\ \\text{m}')], M('2(x + x + 6) = 44 \\Rightarrow 4x = 32 \\Rightarrow x = 8\\ \\text{m}') + '។'))

    # ================= WRITING =================
    def W(level, sec, stem, steps, img=None):
        q_ = wr(level, sec, stem, steps)
        if img: q_['img'] = img
        C.append(q_)

    # Writing Easy
    W('easy', 'basic', 'ដោះស្រាយសមីការ ក. ' + EQ('6*x+15', '45') + ' ខ. ' + EQ('3*x+5', '2*x-3') + ' រួចផ្ទៀងផ្ទាត់។', [
        ('ក. ' + M('6x = 45 - 15 = 30') + ' ; ' + M('x = 5'), 1),
        ('ផ្ទៀងផ្ទាត់ ' + M('6(5) + 15 = 45'), 1),
        ('ខ. ' + M('3x - 2x = -3 - 5') + ' ; ' + M('x = -8'), 2),
        ('ផ្ទៀងផ្ទាត់ ' + M('3(-8) + 5 = -19 = 2(-8) - 3'), 1)])
    W('easy', 'basic', 'ដោះស្រាយសមីការ ក. ' + EQ('2*x-3', '11') + ' ខ. ' + EQ('a+40', '6*a') + ' រួចផ្ទៀងផ្ទាត់។', [
        ('ក. ' + M('2x = 11 + 3 = 14 \\Rightarrow x = 7'), 1),
        ('ផ្ទៀងផ្ទាត់ ៖ ' + M('2(7) - 3 = 11') + ' (ពិត)', 1),
        ('ខ. ' + M('6a - a = 40 \\Rightarrow 5a = 40 \\Rightarrow a = 8'), 2),
        ('ផ្ទៀងផ្ទាត់ ៖ ' + M('8 + 40 = 6(8) = 48') + ' (ពិត)', 1)])

    # Writing Medium
    W('medium', 'frac', 'ដោះស្រាយសមីការ ក. ' + EQ('[2*x|5]+[x|4]', '[26|5]') + ' ខ. ' + EQ('[3|5]*x+3', '[1|5]*x-7') + '។', [
        ('ក. គុណអង្គទាំងពីរនឹង ' + M(20) + ' ៖ ' + M('8x + 5x = 104'), 1),
        (M('13x = 104 \\Rightarrow x = 8'), 1),
        ('ខ. ' + M('\\dfrac{3}{5}x - \\dfrac{1}{5}x = -7 - 3'), 1),
        (M('\\dfrac{2}{5}x = -10'), 1),
        (M('x = -10 \\times \\dfrac{5}{2} = -25'), 1)])
    W('medium', 'basic', 'ដោះស្រាយសមីការ ក. ' + EQ('8-2*(x+1)', '-3*x+1') + ' ខ. ' + EQ('4*(a+6)', '24*a') + '។', [
        ('ក. ' + M('8 - 2x - 2 = -3x + 1'), 1),
        (M('-2x + 6 = -3x + 1 \\Rightarrow x = -5'), 2),
        ('ខ. ' + M('4a + 24 = 24a \\Rightarrow 20a = 24'), 1),
        (M('a = \\dfrac{6}{5} = 1.2'), 1)])
    W('medium', 'special', 'ដោះស្រាយ ក. ' + EQ('-3*(2*n-5)', '[1|2]*(-12*n+30)') + ' ខ. ' + EQ('-3*y+5*(6-y)', '4*(1-2*y)') + ' ហើយប្រាប់ចំនួនឫស។', [
        ('ក. អង្គទី ១ ' + M('-6n + 15') + ' ; អង្គទី ២ ' + M('-6n + 15'), 1),
        ('សមីការពិតគ្រប់តម្លៃ ' + M('n') + ' (ឫសច្រើនរាប់មិនអស់)', 1),
        ('ខ. អង្គទី ១ ' + M('-3y + 30 - 5y = -8y + 30'), 1),
        ('អង្គទី ២ ' + M('4 - 8y') + ' នាំឱ្យ ' + M('30 = 4') + ' មិនពិត', 1),
        ('ដូចនេះ សមីការគ្មានឫស', 1)])
    W('medium', 'zero', 'ដោះស្រាយ ក. ' + EQ('(a+12)*(a-4)', '2*a*(a-4)') + ' ខ. ' + EQ('(2*x-1)**2', '(x+3)**2') + '។', [
        ('ក. ' + M('(a-4)[(a+12) - 2a] = 0 \\Rightarrow (a-4)(12-a) = 0'), 1),
        (M('a = 4') + ' ឬ ' + M('a = 12'), 1),
        ('ខ. ' + M('(2x-1)^2 - (x+3)^2 = 0 \\Rightarrow [(2x-1)+(x+3)][(2x-1)-(x+3)] = 0'), 1),
        (M('(3x+2)(x-4) = 0'), 1),
        (M('x = -\\dfrac{2}{3}') + ' ឬ ' + M('x = 4'), 1)])

    # Writing Hard
    W('hard', 'zero', 'ដោះស្រាយ ក. ' + EQ('4*x**2*(x+1)', '9*(x+1)') + ' ខ. ' + EQ('(x-7)**2', '(5*x-6)**2') + '។', [
        ('ក. ' + M('(x+1)(4x^2 - 9) = 0 \\Rightarrow (x+1)(2x-3)(2x+3) = 0'), 1),
        (M('x = -1,\\ x = \\dfrac{3}{2},\\ x = -\\dfrac{3}{2}'), 1),
        ('ខ. ' + M('[(x-7)+(5x-6)][(x-7)-(5x-6)] = 0'), 1),
        (M('(6x-13)(-4x-1) = 0'), 1),
        (M('x = \\dfrac{13}{6}') + ' ឬ ' + M('x = -\\dfrac{1}{4}'), 1)])
    W('hard', 'error', 'វិបុលដោះស្រាយ ' + M('6m - 15 = 10m - 25') + ' ដោយដាក់កត្តា ' + M('3(2m-5) = 5(2m-5)') + ' រួចចែកនឹង ' + M('2m-5') + ' បាន ' + M('3 = 5') + '។ ក. រកកំហុស។ ខ. ដោះស្រាយឱ្យត្រឹមត្រូវ។', [
        ('ក. កំហុស ៖ ចែកអង្គទាំងពីរនឹង ' + M('2m-5') + ' ដែលអាចស្មើសូន្យ (បាត់បង់ឫស)', 1),
        ('ខ. ' + M('3(2m-5) - 5(2m-5) = 0'), 1),
        (M('-2(2m-5) = 0'), 1),
        (M('2m - 5 = 0'), 1),
        (M('m = \\dfrac{5}{2} = 2.5'), 1)])
    W('hard', 'word', 'ក. រកបីចំនួនគត់គូតគ្នាដែលផលបូក ' + M(-12) + '។ ខ. រកប្រាំចំនួនគត់តគ្នាដែលផលបូក ' + M(520) + '។', [
        ('ក. តាង ' + M('x, x+2, x+4') + ' ; ' + M('3x + 6 = -12'), 1),
        (M('x = -6') + ' ; ចំនួនគឺ ' + M('-6, -4, -2'), 1),
        ('ខ. តាង ' + M('n, n+1, \\ldots, n+4') + ' ; ' + M('5n + 10 = 520'), 1),
        (M('n = 102'), 1),
        (M('102, 103, 104, 105, 106') + ' (ផលបូក ' + M(520) + ')', 1)])
    W('hard', 'word', 'សូផាតអាយុ ' + M(51) + ' ឆ្នាំ រស្មីអាយុ ' + M(21) + ' ឆ្នាំ។ ក. សរសេរសមីការរកចំនួនឆ្នាំ ' + M('t') + ' ដែលសូផាតមានអាយុស្មើពីរដងរស្មី។ ខ. ដោះស្រាយ និងផ្ទៀងផ្ទាត់។', [
        ('ក. ' + M('51 + t = 2(21 + t)'), 1),
        ('ខ. ' + M('51 + t = 42 + 2t'), 1),
        (M('t = 9'), 1),
        ('ផ្ទៀងផ្ទាត់ ៖ សូផាត ' + M('60') + ' រស្មី ' + M('30'), 1),
        (M('60 = 2 \\times 30') + ' ពិត', 1)])

    # Writing PISA
    W('pisa', 'pisa', 'ចតុកោណកែងមានបរិមាត្រ ' + M('148\\ \\text{cm}') + ' ហើយបណ្តោយស្មើបីដងទទឹងថែម ' + M('17\\ \\text{cm}') + '។ ក. សរសេរសមីការ។ ខ. រកទទឹង និងបណ្តោយ។ គ. គណនាផ្ទៃក្រឡា។', [
        ('ក. តាង ' + M('b') + ' ជាទទឹង បណ្តោយ ' + M('3b + 17') + ' ; ' + M('2(3b + 17 + b) = 148'), 1),
        ('ខ. ' + M('8b + 34 = 148 \\Rightarrow 8b = 114 \\Rightarrow b = 14.25\\ \\text{cm}'), 1),
        ('បណ្តោយ ' + M('3(14.25) + 17 = 59.75\\ \\text{cm}'), 1),
        ('គ. ' + M('\\mathcal{A} = 14.25 \\times 59.75'), 1),
        (M('= 851.4375\\ \\text{cm}^2'), 1)], FIG_PERI)
    W('pisa', 'pisa', 'ចតុកោណកែងទទឹង ' + M('2\\ \\text{cm}') + ' បណ្តោយ ' + M('9\\ \\text{cm}') + '។ បង្កើនទទឹង ' + M('1\\ \\text{cm}') + ' និងបណ្តោយ ' + M('x\\ \\text{cm}') + ' ផ្ទៃក្រឡាថ្មីស្មើពីរដងនៃផ្ទៃក្រឡាចាស់។ ក. រកផ្ទៃក្រឡាចាស់។ ខ. សរសេរសមីការ។ គ. រក ' + M('x') + '។', [
        ('ក. ផ្ទៃចាស់ ' + M('\\mathcal{A}_1 = 9 \\times 2 = 18\\ \\text{cm}^2'), 1),
        ('ខ. វិមាត្រថ្មី ' + M('3') + ' និង ' + M('9 + x') + ' ; ' + M('3(9 + x) = 2 \\times 18 = 36'), 2),
        ('គ. ' + M('27 + 3x = 36 \\Rightarrow 3x = 9'), 1),
        (M('x = 3\\ \\text{cm}'), 1)], FIG_EXT)
    W('pisa', 'pisa', 'ធីតាជិះកង់ ' + M('15\\ \\text{km/h}') + ' លក្ខិណាដើរ ' + M('4\\ \\text{km/h}') + ' ចេញពីផ្ទះម៉ោងជាមួយគ្នាទៅសាលា។ ធីតាដល់សាលារួចត្រឡប់មកវិញ ជួបលក្ខិណាត្រង់បង្គោល ' + M('10\\ \\text{km}') + ' (គិតពីផ្ទះ)។ រកចម្ងាយពីផ្ទះទៅសាលា។', [
        ('តាង ' + M('x') + ' ជាចម្ងាយពីផ្ទះទៅសាលា ' + M('(x > 10)'), 1),
        ('ពេលលក្ខិណាដើរ ' + M('t_1 = \\dfrac{10}{4}\\ \\text{h}'), 1),
        ('ធីតាចរបាន ' + M('x + (x - 10) = 2x - 10') + ' ; ពេលធីតា ' + M('t_2 = \\dfrac{2x - 10}{15}\\ \\text{h}'), 1),
        ('សមីការ ៖ ' + M('\\dfrac{10}{4} = \\dfrac{2x - 10}{15} \\Rightarrow 150 = 8x - 40'), 1),
        (M('8x = 190 \\Rightarrow x = 23.75\\ \\text{km}'), 1)], FIG_ROUTE)
    W('pisa', 'pisa', 'ក្រុមស្ត្រីហាត់ប្រាណមួយ ៖ «ចំនួនពួកយើង បូកចំនួនពួកយើង បូកពាក់កណ្តាល បូក ' + M('\\dfrac{1}{4}') + ' នៃពួកយើង រួមទាំងស៊ីថាម្នាក់ទៀត ស្មើ ' + M(100) + ' នាក់»។ រកចំនួនស្ត្រីក្នុងក្រុម។', [
        ('តាង ' + M('x') + ' ជាចំនួនស្ត្រីក្នុងក្រុម', 1),
        (M('x + x + \\dfrac{x}{2} + \\dfrac{x}{4} + 1 = 100'), 1),
        (M('\\dfrac{11x}{4} = 99 \\Rightarrow 11x = 396'), 1),
        (M('x = 36') + ' នាក់', 1),
        ('ផ្ទៀងផ្ទាត់ ៖ ' + M('36 + 36 + 18 + 9 + 1 = 100') + ' (ពិត)', 1)])
    W('pisa', 'pisa', 'អ្នកថ្មើរជើងឡើងភ្នំ ' + M('300\\ \\text{m/h}') + ' ចុះ ' + M('450\\ \\text{m/h}') + ' ចេញម៉ោង ' + M('7\\text{h}\\ 00') + ' ត្រឡប់ដល់វិញ ' + M('18\\text{h}\\ 45') + ' សម្រាក ' + M('4\\text{h}\\ 15') + '។ រកចម្ងាយផ្លូវពីជើងភ្នំដល់កំពូល។', [
        ('ពេលសរុប ' + M('18.75 - 7 = 11.75\\ \\text{h}') + ' ; ដកសម្រាក ' + M('4.25\\ \\text{h}') + ' នៅ ' + M('7.5\\ \\text{h}'), 1),
        ('តាង ' + M('d') + ' ជាចម្ងាយ (m) ៖ ' + M('\\dfrac{d}{300} + \\dfrac{d}{450} = 7.5'), 1),
        (M('\\dfrac{5d}{900} = 7.5 \\Rightarrow \\dfrac{d}{180} = 7.5'), 1),
        (M('d = 1\\,350\\ \\text{m} = 1.35\\ \\text{km}'), 1),
        ('ផ្ទៀងផ្ទាត់ ៖ ' + M('4.5 + 3 + 4.25 = 11.75') + ' (ពិត)', 1)])
    W('pisa', 'pisa', 'ចម្ការកៅស៊ូរាងចតុកោណកែងមានកន្លះបរិមាត្រ ' + M('3\\,528\\ \\text{m}') + '។ បណ្តោយស្មើ ' + M(6) + ' ដងនៃទទឹងថែម ' + M('14\\ \\text{m}') + '។ ក. សរសេរសមីការរកទទឹង។ ខ. រកទទឹង និងបណ្តោយ។ គ. គណនាផ្ទៃក្រឡាគិតជាហិកតា (ha)។', [
        ('ក. តាង ' + M('x') + ' ជាទទឹង (m) ; បណ្តោយ ' + M('6x + 14') + ' ; ' + M('x + (6x + 14) = 3\\,528'), 1),
        ('ខ. ' + M('7x + 14 = 3\\,528 \\Rightarrow 7x = 3\\,514 \\Rightarrow x = 502\\ \\text{m}'), 1),
        ('បណ្តោយ ' + M('6(502) + 14 = 3\\,026\\ \\text{m}'), 1),
        ('គ. ' + M('\\mathcal{A} = 502 \\times 3\\,026 = 1\\,519\\,052\\ \\text{m}^2'), 1),
        (M('\\mathcal{A} = 151.9052\\ \\text{ha} \approx 151.9\\ \\text{ha}'), 1)])

    return C
