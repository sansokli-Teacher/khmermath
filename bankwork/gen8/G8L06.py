from lib import *
import sympy as sp
from sympy import symbols, Rational as Q_
from sympy.parsing.sympy_parser import parse_expr
import re as _re
LESSON = 'កន្សោមសនិទាន'
x, y, z, a, b, c, t, m, n, p, q, u, v, r = symbols('x y z a b c t m n p q u v r')
_LD = {s_.name: s_ for s_ in (x, y, z, a, b, c, t, m, n, p, q, u, v, r)}
_LD['Rational'] = Q_; _LD['pi'] = sp.pi

def L(e): return sp.latex(e).replace('\\frac', '\\dfrac')
def ML(e): return M(L(e))
def E(s_): return parse_expr(s_, local_dict=_LD)
def conv(sx):
    sx = sx.strip()
    sx = _re.sub(r'Rational\((-?\d+),\s*(\d+)\)', lambda m_: '\\dfrac{%s}{%s}' % (m_.group(1), m_.group(2)), sx)
    out = _re.sub(r'\*\*(\d+)', r'^{\1}', sx)
    out = _re.sub(r'(?<=[0-9])\*(?=[0-9])', ' \\\\times ', out)
    out = out.replace('*', '').replace('+-', '-').replace('pi', '\\pi ')
    return out
def FR(nm, dn): return '\\dfrac{%s}{%s}' % (conv(nm), conv(dn))
def with_img(q_, s_): q_['img'] = s_; return q_

# ---------- evaluating a chain of fractions ----------
def chain(terms, ops):
    ex = E('(%s)/(%s)' % terms[0])
    for (nm, dn), op in zip(terms[1:], ops):
        f = E('(%s)/(%s)' % (nm, dn))
        ex = {'*': ex * f, '/': ex / f, '+': ex + f, '-': ex - f}[op]
    return sp.factor(sp.cancel(sp.together(ex)))
OPTEX = {'*': ' \\times ', '/': ' \\div ', '+': ' + ', '-': ' - '}
def tex_chain(terms, ops):
    s_ = FR(*terms[0])
    for (nm, dn), op in zip(terms[1:], ops): s_ += OPTEX[op] + FR(nm, dn)
    return s_
def wrongs_for(ans):
    vs = sorted(ans.free_symbols, key=lambda s_: s_.name) if hasattr(ans, 'free_symbols') else []
    c = [-ans, 1 / ans if ans != 0 else ans + 3]
    if vs:
        v0 = vs[0]
        c.append(sp.factor(sp.cancel(ans.subs(v0, -v0))))
        c.append(sp.factor(sp.cancel(ans + 1)))
        c.append(sp.factor(sp.cancel(ans * (v0 + 1) / (v0 - 1))))
        c.append(sp.factor(sp.cancel(ans * 2)))
    c += [ans + 2, ans * 2, ans - 1]
    return c
def distinct(ans, cands, k=3):
    out, seen = [], [sp.simplify(ans)]
    for c in cands:
        ok = all(sp.simplify(c - s_) != 0 for s_ in seen)
        if ok: out.append(c); seen.append(sp.simplify(c))
        if len(out) == k: break
    assert len(out) == k, ('wrongs', ans)
    return [ML(o) for o in out]

C = []
def rq(level, sec, terms, ops, prefix, wrong=None, sol=''):
    ans = chain(terms, ops)
    ws = [E(w) if isinstance(w, str) else w for w in wrong] if wrong else wrongs_for(ans)
    C.append(mcq(level, sec, prefix + M(tex_chain(terms, ops)) + ' ៖', ML(ans), distinct(ans, ws + wrongs_for(ans)), sol or ('ដាក់ជាផលគុណកត្តា រួចសម្រួល ៖ ' + M(L(ans)) + '។')))

# ---------- figures ----------
def _t(x0, y0, s_, a_='middle', kh=False, sz=13):
    if kh: st = f"font-family='Khmer OS Battambang,Noto Sans Khmer,serif' font-style='normal' font-size='{sz}'"
    else: st = f"font-family='Times New Roman,serif' font-style='italic' font-size='{sz}'"
    return f"<text x='{x0}' y='{y0}' text-anchor='{a_}' {st} fill='#111'>{s_}</text>"
def svg(w, h, body): return f"<svg xmlns='http://www.w3.org/2000/svg' width='{w}' height='{h}' viewBox='0 0 {w} {h}'><rect width='{w}' height='{h}' fill='white'/>{body}</svg>"
ST = "fill='#eef3ff' stroke='#1d2540' stroke-width='1.6'"
FIG_CIRCSQ = svg(180, 170, f"<rect x='20' y='10' width='130' height='130' {ST}/><circle cx='85' cy='75' r='65' fill='#fff6e0' stroke='#1d2540' stroke-width='1.6'/><line x1='85' y1='75' x2='150' y2='75' stroke='#1d2540' stroke-width='1.2' stroke-dasharray='4 3'/>" + _t(118, 69, 'r') + _t(85, 160, 'x') + _t(158, 80, 'x', 'start'))
FIG_RECT = svg(220, 120, f"<rect x='20' y='10' width='150' height='80' {ST}/>" + _t(95, 110, 'x') + _t(178, 54, 'y', 'start'))
FIG_CIRC_R_SQ = svg(250, 170, f"<circle cx='65' cy='80' r='55' fill='#fff6e0' stroke='#1d2540' stroke-width='1.6'/><line x1='65' y1='80' x2='120' y2='80' stroke='#1d2540' stroke-width='1.2'/>" + _t(93, 74, 'r') + f"<rect x='150' y='30' width='90' height='90' {ST}/>" + _t(195, 138, 'x') + _t(65, 155, 'rង្វង់', kh=True, sz=11).replace('rង្វង់', 'កាំ r'))
FIG_TRIP = svg(330, 110, "<line x1='30' y1='60' x2='300' y2='60' stroke='#1d2540' stroke-width='1.4'/><circle cx='30' cy='60' r='5' fill='#1d2540'/><circle cx='300' cy='60' r='5' fill='#1d2540'/><line x1='36' y1='44' x2='290' y2='44' stroke='#c0392b' stroke-width='1.8'/><polygon points='290,40 300,44 290,48' fill='#c0392b'/><line x1='294' y1='76' x2='40' y2='76' stroke='#2563eb' stroke-width='1.8'/><polygon points='40,72 30,76 40,80' fill='#2563eb'/>" + _t(165, 36, 'ទៅ x km/h', kh=True, sz=12).replace('ទៅ x km/h', 'ទៅ 12 km ល្បឿន x km/h') + _t(165, 98, 'ត្រឡប់ 12 km ល្បឿន (x+2) km/h', kh=True, sz=12))

def cands():
    # ================= notion =================
    C.append(mcq('easy', 'notion', 'កន្សោមសនិទានជាកន្សោមមានទម្រង់ ' + M('\\dfrac{A}{B}') + ' ដែល ' + M('A') + ' និង ' + M('B') + ' ជាឯកធា ឬពហុធា ហើយ៖', M('B \\neq 0'), [M('A \\neq 0'), M('B = 1'), M('A = B')], 'ភាគបែងមិនអាចស្មើសូន្យ។'))
    C.append(mcq('easy', 'notion', 'កន្សោមមួយណាមិនមែនជាកន្សោមសនិទាន?', M('\\dfrac{x}{\\sqrt{y}}'), [M('\\dfrac{x}{y}'), M('\\dfrac{a+b}{b}'), M('\\dfrac{1+x}{x^2-1}')], M('\\sqrt{y}') + ' ពុំមែនជាឯកធា ឬពហុធា។'))
    C.append(mcq('easy', 'notion', 'កន្សោមមួយណាជាកន្សោមសនិទាន?', M('\\dfrac{1+x}{x^2-1}'), [M('\\dfrac{x}{\\sqrt{y}}'), M('\\sqrt{x+1}'), M('\\dfrac{2}{\\sqrt{3}\\,\\sqrt{x}}')], 'ភាគយក និងភាគបែងជាពហុធា។'))
    C.append(mcq('medium', 'notion', 'ផលធៀបនៃចំនួនគត់ ' + M('n') + ' និងចំនួនគត់បន្ទាប់គឺ៖', M('\\dfrac{n}{n+1}'), [M('\\dfrac{n+1}{n}'), M('\\dfrac{n}{n-1}'), M('\\dfrac{1}{n+1}')], 'ចំនួនគត់បន្ទាប់គឺ ' + M('n+1') + '។'))
    C.append(mcq('medium', 'notion', 'ផលធៀបរវាងផ្ទៃក្រឡានិងបរិមាត្រនៃចតុកោណកែងវិមាត្រ ' + M('x') + ' និង ' + M('y') + ' គឺ៖', M('\\dfrac{xy}{2(x+y)}'), [M('\\dfrac{2(x+y)}{xy}'), M('\\dfrac{xy}{x+y}'), M('\\dfrac{x+y}{xy}')], M('\\mathcal{A} = xy') + ' ; ' + M('P = 2(x+y)') + '។'))
    C.append(with_img(mcq('pisa', 'figure', 'ចតុកោណកែងមានវិមាត្រ ' + M('x') + ' និង ' + M('y') + ' ដូចរូប។ ផលធៀបរវាងផ្ទៃក្រឡានិងបរិមាត្រគឺ៖', M('\\dfrac{xy}{2(x+y)}'), [M('\\dfrac{2(x+y)}{xy}'), M('\\dfrac{xy}{x+y}'), M('\\dfrac{x+y}{xy}')], M('\\mathcal{A} = xy') + ' ; ' + M('P = 2(x+y)') + '។'), FIG_RECT))
    C.append(mcq('hard', 'notion', 'ផលធៀបរវាងផ្ទៃក្រឡារង្វង់កាំ ' + M('r') + ' និងការេជ្រុង ' + M('x') + ' គឺ៖', M('\\dfrac{\\pi r^2}{x^2}'), [M('\\dfrac{2\\pi r}{4x}'), M('\\dfrac{\\pi r}{x}'), M('\\dfrac{r^2}{\\pi x^2}')], M('\\mathcal{A}_{\\text{រង្វង់}} = \\pi r^2') + ' ; ' + M('\\mathcal{A}_{\\text{ការេ}} = x^2') + '។'))
    C.append(with_img(mcq('pisa', 'figure', 'រង្វង់មួយចារឹកក្នុងការេជ្រុង ' + M('x') + '។ ផលធៀបរវាងផ្ទៃក្រឡារង្វង់និងការេគឺ៖', M('\\dfrac{\\pi}{4}'), [M('\\dfrac{\\pi}{2}'), M('\\pi'), M('\\dfrac{4}{\\pi}')], M('r = \\dfrac{x}{2}') + ' ; ' + M('\\dfrac{\\pi (x/2)^2}{x^2} = \\dfrac{\\pi}{4}') + '។'), FIG_CIRCSQ))
    # ================= numerical value / domain =================
    C.append(mcq('easy', 'value', 'តម្លៃលេខនៃ ' + M('\\dfrac{3x}{x-2}') + ' ចំពោះ ' + M('x = -1') + ' គឺ៖', M(1), [M(-1), M(3), M(0)], M('\\dfrac{3(-1)}{-1-2} = \\dfrac{-3}{-3} = 1') + '។'))
    C.append(mcq('easy', 'value', 'តម្លៃលេខនៃ ' + M('\\dfrac{3x}{x-2}') + ' ចំពោះ ' + M('x = 0') + ' គឺ៖', M(0), [M(1), M(-1), M('\\text{គ្មានន័យ}')], 'ភាគយកស្មើ ' + M(0) + ' ភាគបែង ' + M(-2) + ' ≠ ' + M(0) + '។'))
    C.append(mcq('easy', 'value', 'កន្សោម ' + M('\\dfrac{3x}{x-2}') + ' គ្មានន័យ ពេល៖', M('x = 2'), [M('x = 0'), M('x = -2'), M('x = 3')], 'ភាគបែង ' + M('x-2 = 0') + '។'))
    C.append(mcq('medium', 'value', 'កន្សោម ' + M('\\dfrac{a-5}{2a+6}') + ' គ្មានន័យ ពេល៖', M('a = -3'), [M('a = 5'), M('a = 3'), M('a = -5')], M('2a + 6 = 0') + ' នាំឱ្យ ' + M('a = -3') + '។'))
    C.append(mcq('medium', 'value', 'កន្សោម ' + M('\\dfrac{a-5}{2a+6}') + ' ស្មើសូន្យ ពេល៖', M('a = 5'), [M('a = -3'), M('a = -5'), M('a = 3')], 'ភាគយក ' + M('a - 5 = 0') + ' ហើយភាគបែង ' + M('16 \\neq 0') + '។'))
    C.append(mcq('medium', 'value', 'តម្លៃលេខនៃ ' + M('\\dfrac{4}{x^2+1}') + ' ចំពោះ ' + M('x = -1') + ' គឺ៖', M(2), [M(4), M(0), M(-2)], M('\\dfrac{4}{(-1)^2+1} = \\dfrac{4}{2} = 2') + '។'))
    C.append(mcq('hard', 'value', 'តម្លៃ ' + M('x') + ' ណាធ្វើឱ្យ ' + M('\\dfrac{(x-5)(2x-1)-x+5}{x^2-4}') + ' ស្មើសូន្យ?', M('x = 5') + ' ឬ ' + M('x = 1'), [M('x = 5') + ' ឬ ' + M('x = \\tfrac12'), M('x = \\pm 2'), M('x = 1') + ' ឬ ' + M('x = -5')], 'ភាគយក ' + M('(x-5)(2x-1) - (x-5) = 2(x-5)(x-1)') + '។'))
    C.append(mcq('hard', 'value', 'កន្សោម ' + M('\\dfrac{1}{a^3-a}') + ' គ្មានន័យ ពេល៖', M('a = 0,\\ 1,\\ -1'), [M('a = 0') + ' តែប៉ុណ្ណោះ', M('a = 1,\\ -1'), M('a = 0,\\ 1')], M('a^3 - a = a(a-1)(a+1)') + '។'))
    # ================= simplify =================
    rq('easy', 'simplify', [('12*a**2*b**3', '15*a**5*b')], [], 'សម្រួល ')
    rq('easy', 'simplify', [('14*x**3', '7*x**2*y')], [], 'សម្រួល ')
    rq('medium', 'simplify', [('2*x-6', '5*x-15')], [], 'សម្រួល ')
    rq('medium', 'simplify', [('3*x**2+4*x', '9*x**2-16')], [], 'សម្រួល ')
    rq('medium', 'simplify', [('1-x', 'x**2+x-2')], [], 'សម្រួល ')
    rq('medium', 'simplify', [('a-b', 'b**2-a**2')], [], 'សម្រួល ')
    rq('medium', 'simplify', [('4*x**2+8*x+4', '5*x**2+10*x+5')], [], 'សម្រួល ')
    rq('medium', 'simplify', [('1-25*x**2', '5*x-1')], [], 'សម្រួល ')
    rq('medium', 'simplify', [('a**2+4*a-12', 'a**2+2*a-8')], [], 'សម្រួល ')
    rq('medium', 'simplify', [('2*y**2-17*y+21', 'y**2-6*y-7')], [], 'សម្រួល ')
    rq('hard', 'simplify', [('3*a**3-3*a**2-6*a', '6*a**3-12*a**2-18*a')], [], 'សម្រួល ')
    rq('hard', 'simplify', [('x-y', 'x**2+x*z-x*y-z*y')], [], 'សម្រួល ')
    rq('hard', 'simplify', [('a**2+a*m-a*n-m*n', 'a**2+a*m+a*n+m*n')], [], 'សម្រួល ')
    rq('hard', 'simplify', [('b**2-a**2', '2*a**2+a*b-3*b**2')], [], 'សម្រួល ')
    rq('hard', 'simplify', [('-8*a**2*b**4*x', '(-2*a*b*x)**3')], [], 'សម្រួល ')
    rq('hard', 'simplify', [('(x-3)*(3*x+1)-(2*x-6)*(x+1)', '1-x**2')], [], 'សម្រួល ')
    # ================= multiply / divide =================
    rq('easy', 'muldiv', [('7*b', '10*a'), ('5*a**2', '8*b')], ['*'], 'គណនាផលគុណ ')
    rq('medium', 'muldiv', [('5*x', '4*x-12'), ('2*x**2-6*x', '3')], ['*'], 'គណនាផលគុណ ')
    rq('medium', 'muldiv', [('a**2-2*a+1', 'a**2-1'), ('a**2+a', 'a**2-2*a')], ['*'], 'គណនាផលគុណ ')
    rq('medium', 'muldiv', [('4*x**2', '15*y'), ('3*x', '10*y**2')], ['/'], 'គណនាផលចែក ')
    rq('medium', 'muldiv', [('a**2-9', '3*a'), ('a+3', 'a-3')], ['/'], 'គណនាផលចែក ')
    rq('medium', 'muldiv', [('4*x+8', 'x+3'), ('x+2', '1')], ['/'], 'គណនាផលចែក ')
    rq('hard', 'muldiv', [('9*a**2-6*a+1', '5-a'), ('5*(a-2)-a*(a-2)', 'a**2-4*a+4')], ['*'], 'គណនាផលគុណ ')
    rq('hard', 'muldiv', [('4*x**2+8*x', 'x**2-9'), ('6*x**3+12*x**2', 'x**2-2*x-3')], ['/'], 'គណនាផលចែក ')
    rq('hard', 'muldiv', [('x-y', 'x**2-y**2'), ('x+y', 'x**2+2*x*y+y**2')], ['/'], 'គណនាផលចែក ')
    rq('hard', 'muldiv', [('3*p-5*q', '4*p**2-q**2'), ('5*q-3*p', '8*p**2-4*p*q')], ['/'], 'គណនាផលចែក ')
    rq('hard', 'muldiv', [('b**2-1', 'b**2+3*b+2'), ('b**2-2*b-8', 'b**2-4*b+3')], ['*'], 'គណនាផលគុណ ')
    rq('hard', 'muldiv', [('2*m**2+3*m*n-2*n**2', '2*m**2-3*m*n-2*n**2'), ('2*m-n', '2*m+n')], ['/'], 'គណនាផលចែក ')
    # ================= add / subtract =================
    rq('easy', 'addsub', [('5', 'a'), ('7', 'a')], ['+'], 'គណនា ')
    rq('easy', 'addsub', [('12*a', '7'), ('2*a', '7')], ['+'], 'គណនា ')
    rq('medium', 'addsub', [('3*y-2', 'y-5'), ('8*y+7', 'y-5')], ['+'], 'គណនា ')
    rq('medium', 'addsub', [('a', '2*a+3'), ('a-3', '2*a+3')], ['-'], 'គណនា ')
    rq('medium', 'addsub', [('2', 'x-3'), ('7', '3-x')], ['+'], 'គណនា ')
    rq('medium', 'addsub', [('5*x', 'x-y'), ('5*y', 'y-x')], ['-'], 'គណនា ')
    rq('medium', 'addsub', [('y', '2*x'), ('x', '3*y')], ['+'], 'គណនា ')
    rq('medium', 'addsub', [('4', 'n'), ('2', 'n+1')], ['-'], 'គណនា ')
    rq('hard', 'addsub', [('t+1', 't**2+5*t'), ('8', 't**2-25')], ['+'], 'គណនា ')
    rq('hard', 'addsub', [('2*m', 'm-5'), ('12', 'm**2-25')], ['+'], 'គណនា ')
    rq('hard', 'addsub', [('a**2-1', 'a**2-2*a-15'), ('a+2', 'a+3')], ['-'], 'គណនា ')
    rq('hard', 'addsub', [('x**2+6*x+9', 'x**2+3*x'), ('x**2-x-2', 'x**2-4')], ['+'], 'គណនា ')
    rq('hard', 'addsub', [('3*x-y', '2'), ('2*x-y', '4')], ['+'], 'គណនា ')
    rq('hard', 'addsub', [('4*a', '2*a+6'), ('3', 'a+3')], ['+'], 'គណនា ')
    rq('hard', 'addsub', [('a+1', '2*a-8'), ('a+2', '12-3*a')], ['-'], 'គណនា ')
    rq('hard', 'addsub', [('1', 'x-1'), ('1', '3*x'), ('1', 'x**2*(x-1)')], ['+', '-'], 'គណនា ')
    # ================= PISA =================
    C.append(with_img(mcq('pisa', 'pisa', 'អ្នកដើរចម្ងាយ ' + M('12\\ \\text{km}') + ' ក្នុងល្បឿន ' + M('x\\ \\text{km/h}') + ' ហើយត្រឡប់មកវិញក្នុងល្បឿន ' + M('(x+2)\\ \\text{km/h}') + '។ ពេលសរុប (ម៉ោង) គឺ៖', M('\\dfrac{24(x+1)}{x(x+2)}'), [M('\\dfrac{24}{2x+2}'), M('\\dfrac{24}{x(x+2)}'), M('\\dfrac{12}{x} - \\dfrac{12}{x+2}')], M('\\dfrac{12}{x} + \\dfrac{12}{x+2} = \\dfrac{12(x+2)+12x}{x(x+2)} = \\dfrac{24(x+1)}{x(x+2)}') + '។'), FIG_TRIP))
    C.append(mcq('pisa', 'pisa', 'អ្នកដើរចម្ងាយ ' + M('12\\ \\text{km}') + ' ក្នុងល្បឿន ' + M('4\\ \\text{km/h}') + ' ហើយត្រឡប់មកវិញក្នុងល្បឿន ' + M('6\\ \\text{km/h}') + '។ ពេលធ្វើដំណើរសរុបគឺ៖', M('5') + ' ម៉ោង', [M('3') + ' ម៉ោង', M('6') + ' ម៉ោង', M('4.8') + ' ម៉ោង'], M('\\dfrac{12}{4} + \\dfrac{12}{6} = 3 + 2 = 5') + '។'))
    C.append(mcq('pisa', 'pisa', 'គណនា ' + M('S = \\dfrac{1}{1\\times2} + \\dfrac{1}{2\\times3} + \\dfrac{1}{3\\times4} + \\dfrac{1}{4\\times5}') + ' ដោយប្រើ ' + M('\\dfrac{1}{n(n+1)} = \\dfrac{1}{n} - \\dfrac{1}{n+1}') + '៖', M('\\dfrac{4}{5}'), [M('\\dfrac{1}{5}'), M('\\dfrac{9}{20}'), M('\\dfrac{5}{4}')], M('S = 1 - \\dfrac{1}{5} = \\dfrac{4}{5}') + '។'))
    C.append(mcq('pisa', 'pisa', 'បង្ហាញថា ' + M('\\dfrac{1}{n} - \\dfrac{1}{n+1}') + ' ស្មើ៖', M('\\dfrac{1}{n(n+1)}'), [M('\\dfrac{1}{n+1}'), M('\\dfrac{2}{n(n+1)}'), M('\\dfrac{1}{n^2+1}')], M('\\dfrac{(n+1) - n}{n(n+1)} = \\dfrac{1}{n(n+1)}') + '។'))
    # ================= WRITING =================
    def W(level, sec, stem, steps, img=None):
        q_ = wr(level, sec, stem, steps)
        if img: q_['img'] = img
        C.append(q_)
    W('easy', 'value', 'គេមានកន្សោម ' + M('\\dfrac{3x}{x-2}') + '។ គណនាតម្លៃលេខ ចំពោះ ' + M('x = -1') + ', ' + M('x = 0') + ', ' + M('x = 2') + '។', [
        ('ជំនួសតម្លៃ ' + M('x = -1') + ' ៖ ' + M('\\dfrac{3(-1)}{-1-2} = \\dfrac{-3}{-3} = 1'), 2), (M('x = 0') + ' ៖ ' + M('\\dfrac{0}{-2} = 0'), 1), (M('x = 2') + ' ៖ ភាគបែង ' + M('2 - 2 = 0'), 1), ('ដូចនេះកន្សោមគ្មានន័យ', 1)])
    W('medium', 'value', 'គេមានកន្សោម ' + M('\\dfrac{a-5}{2a+6}') + '។ កំណត់ ' + M('a') + ' ដើម្បីឱ្យកន្សោម ក. គ្មានន័យ ខ. ស្មើសូន្យ។', [
        ('ក. គ្មានន័យ លុះត្រាតែភាគបែងស្មើ ' + M(0), 1), (M('2a + 6 = 0 \\Rightarrow a = -3'), 1), ('ខ. ស្មើសូន្យ លុះត្រាតែភាគយកស្មើ ' + M(0) + ' និងភាគបែងខុសពីសូន្យ', 1), (M('a - 5 = 0 \\Rightarrow a = 5'), 1), ('ត្រួតពិនិត្យ ' + M('2(5) + 6 = 16 \\neq 0'), 1)])
    ex = [('2*x-6', '5*x-15'), ('3*x**2+4*x', '9*x**2-16'), ('a**2+4*a-12', 'a**2+2*a-8')]
    W('medium', 'simplify', 'សម្រួល ក. ' + M(FR(*ex[0])) + ' ខ. ' + M(FR(*ex[1])) + ' គ. ' + M(FR(*ex[2])) + '។', [
        ('ក. ' + M('\\dfrac{2(x-3)}{5(x-3)} = ' + L(chain([ex[0]], []))), 1), ('ខ. ' + M('\\dfrac{x(3x+4)}{(3x-4)(3x+4)}'), 1), (M('= ' + L(chain([ex[1]], []))), 1), ('គ. ' + M('\\dfrac{(a+6)(a-2)}{(a+4)(a-2)}'), 1), (M('= ' + L(chain([ex[2]], []))), 1)])
    W('medium', 'muldiv', 'គណនាផលគុណ ' + M(tex_chain([('7*b', '10*a'), ('5*a**2', '8*b')], ['*'])) + ' និង ' + M(tex_chain([('5*x', '4*x-12'), ('2*x**2-6*x', '3')], ['*'])) + '។', [
        ('ក. ' + M('\\dfrac{7b \\cdot 5a^2}{10a \\cdot 8b} = \\dfrac{35a^2 b}{80ab}'), 1), (M('= ' + L(chain([('7*b', '10*a'), ('5*a**2', '8*b')], ['*']))), 1), ('ខ. ' + M('\\dfrac{5x}{4(x-3)} \\times \\dfrac{2x(x-3)}{3}'), 1), (M('= \\dfrac{10x^2(x-3)}{12(x-3)}'), 1), (M('= ' + L(chain([('5*x', '4*x-12'), ('2*x**2-6*x', '3')], ['*']))), 1)])
    W('medium', 'addsub', 'គណនា ក. ' + M('\\dfrac{y}{2x} + \\dfrac{x}{3y}') + ' ខ. ' + M('\\dfrac{4}{n} - \\dfrac{2}{n+1}') + '។', [
        ('ក. ភាគបែងរួមតូចបំផុត ' + M('6xy'), 1), (M('\\dfrac{3y^2 + 2x^2}{6xy}'), 1), ('ខ. ភាគបែងរួម ' + M('n(n+1)'), 1), (M('\\dfrac{4(n+1) - 2n}{n(n+1)} = \\dfrac{2n+4}{n(n+1)}'), 1), (M('= \\dfrac{2(n+2)}{n(n+1)}'), 1)])
    W('hard', 'simplify', 'សម្រួល ' + M(FR('(x-3)*(3*x+1)-(2*x-6)*(x+1)', '1-x**2')) + '។', [
        ('កត្តា ' + M('2x - 6 = 2(x-3)') + ' ; ' + M('1 - x^2 = -(x-1)(x+1)'), 1), ('ភាគយក ' + M('(x-3)[(3x+1) - 2(x+1)] = (x-3)(x-1)'), 2), (M('\\dfrac{(x-3)(x-1)}{-(x-1)(x+1)}'), 1), (M('= -\\dfrac{x-3}{x+1}'), 1)])
    W('hard', 'muldiv', 'គណនាផលចែក ' + M(tex_chain([('4*x**2+8*x', 'x**2-9'), ('6*x**3+12*x**2', 'x**2-2*x-3')], ['/'])) + '។', [
        ('កត្តា ' + M('4x(x+2)') + ' ; ' + M('(x-3)(x+3)') + ' ; ' + M('6x^2(x+2)') + ' ; ' + M('(x-3)(x+1)'), 2), ('គុណនឹងចម្រាស ' + M('\\dfrac{4x(x+2)}{(x-3)(x+3)} \\times \\dfrac{(x-3)(x+1)}{6x^2(x+2)}'), 1), (M('= ' + L(chain([('4*x**2+8*x', 'x**2-9'), ('6*x**3+12*x**2', 'x**2-2*x-3')], ['/']))), 2)])
    W('hard', 'addsub', 'គណនា ' + M(tex_chain([('t+1', 't**2+5*t'), ('8', 't**2-25')], ['+'])) + '។', [
        ('ភាគបែង ' + M('t(t+5)') + ' និង ' + M('(t-5)(t+5)') + ' ភាគបែងរួម ' + M('t(t+5)(t-5)'), 1), (M('\\dfrac{(t+1)(t-5) + 8t}{t(t+5)(t-5)} = \\dfrac{t^2 + 4t - 5}{t(t+5)(t-5)}'), 2), (M('= \\dfrac{(t+5)(t-1)}{t(t+5)(t-5)} = \\dfrac{t-1}{t(t-5)}'), 2)])
    W('hard', 'pisa', 'ក. បង្ហាញថា ' + M('\\dfrac{1}{n} - \\dfrac{1}{n+1} = \\dfrac{1}{n(n+1)}') + '។ ខ. គណនា ' + M('S = \\dfrac{1}{1\\times2} + \\dfrac{1}{2\\times3} + \\dfrac{1}{3\\times4} + \\dfrac{1}{4\\times5}') + '។', [
        ('ក. ' + M('\\dfrac{(n+1) - n}{n(n+1)}'), 1), (M('= \\dfrac{1}{n(n+1)}'), 1), ('ខ. សរសេរ ' + M('S = (1 - \\tfrac12) + (\\tfrac12 - \\tfrac13) + (\\tfrac13 - \\tfrac14) + (\\tfrac14 - \\tfrac15)'), 1), ('ពាក្យកណ្តាលលុបគ្នា', 1), (M('S = 1 - \\dfrac{1}{5} = \\dfrac{4}{5}'), 1)])
    W('pisa', 'figure', 'រង្វង់មួយចារឹកក្នុងការេជ្រុង ' + M('x') + '។ ក. រកកាំរង្វង់។ ខ. រកផ្ទៃក្រឡារង្វង់ និងការេ។ គ. រកផលធៀបរវាងផ្ទៃក្រឡារង្វង់និងការេ។', [
        ('ក. ' + M('r = \\dfrac{x}{2}'), 1), ('ខ. ' + M('\\mathcal{A}_{\\text{រង្វង់}} = \\pi\\left(\\dfrac{x}{2}\\right)^2 = \\dfrac{\\pi}{4}x^2'), 1), (M('\\mathcal{A}_{\\text{ការេ}} = x^2'), 1), ('គ. ' + M('\\dfrac{\\pi x^2 / 4}{x^2}'), 1), (M('= \\dfrac{\\pi}{4}'), 1)], FIG_CIRCSQ)
    W('pisa', 'figure', 'ចតុកោណកែងមានវិមាត្រ ' + M('x') + ' និង ' + M('y') + '។ ក. សរសេរផ្ទៃក្រឡានិងបរិមាត្រ។ ខ. សរសេរផលធៀបរវាងផ្ទៃក្រឡានិងបរិមាត្រជាកន្សោមសនិទាន។ គ. គណនាផលធៀប ពេល ' + M('x = 6, y = 3') + '។', [
        ('ក. ' + M('\\mathcal{A} = xy') + ' ; ' + M('P = 2(x+y)'), 2), ('ខ. ' + M('\\dfrac{\\mathcal{A}}{P} = \\dfrac{xy}{2(x+y)}'), 1), ('គ. ' + M('\\dfrac{6 \\times 3}{2(6+3)} = \\dfrac{18}{18}'), 1), (M('= 1'), 1)], FIG_RECT)
    W('pisa', 'pisa', 'អ្នកដើរចម្ងាយ ' + M('12\\ \\text{km}') + ' ក្នុងល្បឿន ' + M('x\\ \\text{km/h}') + ' ហើយត្រឡប់ក្នុងល្បឿន ' + M('(x+2)\\ \\text{km/h}') + '។ ក. សរសេរពេលសរុបជាកន្សោមសនិទានសម្រួលរួច។ ខ. គណនាពេលសរុប ពេល ' + M('x = 4') + '។', [
        ('ក. ' + M('t_1 = \\dfrac{12}{x}') + ' ; ' + M('t_2 = \\dfrac{12}{x+2}'), 1), (M('\\dfrac{12(x+2) + 12x}{x(x+2)} = \\dfrac{24x + 24}{x(x+2)}'), 1), (M('= \\dfrac{24(x+1)}{x(x+2)}'), 1), ('ខ. ' + M('\\dfrac{24 \\times 5}{4 \\times 6} = \\dfrac{120}{24}'), 1), (M('= 5') + ' ម៉ោង', 1)], FIG_TRIP)
    W('pisa', 'pisa', 'ផលធៀបនៃចំនួនគត់ ' + M('n') + ' និងចំនួនគត់បន្ទាប់ជាកន្សោមសនិទាន។ ក. សរសេរកន្សោមនោះ។ ខ. កំណត់ ' + M('n') + ' ដែលកន្សោមស្មើ ' + M('\\dfrac{4}{5}') + '។ គ. កំណត់តម្លៃ ' + M('n') + ' ដែលកន្សោមគ្មានន័យ។', [
        ('ក. ' + M('\\dfrac{n}{n+1}'), 1), ('ខ. ' + M('\\dfrac{n}{n+1} = \\dfrac{4}{5} \\Rightarrow 5n = 4(n+1)'), 2), (M('n = 4'), 1), ('គ. ភាគបែង ' + M('n + 1 = 0 \\Rightarrow n = -1'), 1)])
    W('pisa', 'pisa', 'ចតុកោណកែងមួយមានផ្ទៃក្រឡា ' + M('x^2 - 9') + ' និងទទឹង ' + M('x + 3') + '។ ក. រកបណ្តោយជាកន្សោមសនិទានសម្រួលរួច។ ខ. សរសេរផលធៀបបណ្តោយនិងទទឹង។ គ. គណនាផលធៀប ពេល ' + M('x = 7') + '។', [
        ('ក. បណ្តោយ ' + M('\\dfrac{x^2 - 9}{x + 3} = \\dfrac{(x-3)(x+3)}{x+3}'), 1), (M('= x - 3'), 1), ('ខ. ' + M('\\dfrac{\\text{បណ្តោយ}}{\\text{ទទឹង}} = \\dfrac{x-3}{x+3}'), 1), ('គ. ' + M('\\dfrac{7-3}{7+3} = \\dfrac{4}{10}'), 1), (M('= \\dfrac{2}{5}'), 1)])
    return C
