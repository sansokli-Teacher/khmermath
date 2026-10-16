from lib import *
import sympy as sp
from sympy import symbols, expand, factor, Rational as Q_, sqrt, div
LESSON = 'កន្សោមពីជគណិត'
x, y, z, a, b, c, t, m, n = symbols('x y z a b c t m n')

def L(e): return sp.latex(e).replace('\\frac', '\\dfrac')
def ML(e): return M(L(e))
def uniqE(ans, cands, k=3):
    out, seen = [], [sp.expand(ans)]
    for c in cands:
        ce = sp.expand(c)
        if all(sp.simplify(ce - s) != 0 for s in seen):
            out.append(c); seen.append(ce)
    assert len(out) >= k, ('not enough distinct wrongs', ans, cands)
    return [ML(c) for c in out[:k]]
from sympy.parsing.sympy_parser import parse_expr
import re as _re
_LD = {'x': x, 'y': y, 'z': z, 'a': a, 'b': b, 'c': c, 't': t, 'm': m, 'n': n, 'Rational': Q_}
def E(sx): return parse_expr(sx, local_dict=_LD)            # evaluated (for answers)
def _strip(sx):
    sx = sx.strip()
    while sx.startswith('(') and sx.endswith(')'):
        d = 0; ok = True
        for i, ch in enumerate(sx):
            d += (ch == '(') - (ch == ')')
            if d == 0 and i < len(sx) - 1: ok = False; break
        if not ok: break
        sx = sx[1:-1].strip()
    return sx
def conv(sx):
    """python-syntax expression -> TeX written exactly as typed (no reordering / evaluation)"""
    sx = sx.strip()
    sx = _re.sub(r'Rational\((-?\d+),\s*(\d+)\)', lambda m_: '\\dfrac{%s}{%s}' % (m_.group(1), m_.group(2)), sx)
    # top-level division
    d = 0
    for i, ch in enumerate(sx):
        if ch in '({': d += 1
        elif ch in ')}': d -= 1
        elif ch == '/' and d == 0:
            return '\\dfrac{%s}{%s}' % (conv(_strip(sx[:i])), conv(_strip(sx[i + 1:])))
    out = _re.sub(r'\*\*(\d+)', r'^{\1}', sx)
    out = _re.sub(r'\*\*\(([^)]+)\)', r'^{\1}', out)
    out = _re.sub(r'(?<=[0-9])\*(?=[0-9])', ' \\\\times ', out)
    out = out.replace('*', '')
    out = out.replace('+-', '-')
    return out
def T(sx): return conv(sx)
def mq(level, sec, stem, ans, wrongs, sol='', raw=False):
    return mcq(level, sec, stem, ML(ans), uniqE(ans, wrongs), sol)
def with_img(q, s): q['img'] = s; return q

# ---------------- figures ----------------
def _t(x0, y0, s, a='middle', kh=False, sz=13):
    if kh: st = f"font-family='Khmer OS Battambang,Noto Sans Khmer,serif' font-style='normal' font-size='{sz}'"
    else: st = f"font-family='Times New Roman,serif' font-style='italic' font-size='{sz}'"
    return f"<text x='{x0}' y='{y0}' text-anchor='{a}' {st} fill='#111'>{s}</text>"
def svg(w, h, body): return f"<svg xmlns='http://www.w3.org/2000/svg' width='{w}' height='{h}' viewBox='0 0 {w} {h}'><rect width='{w}' height='{h}' fill='white'/>{body}</svg>"
ST = "fill='#eef3ff' stroke='#1d2540' stroke-width='1.6'"
def fig_cube(lab):
    return svg(190, 150, f"<polygon points='20,135 110,135 110,45 20,45' {ST}/><polygon points='20,45 110,45 160,15 70,15' fill='#dfe8ff' stroke='#1d2540' stroke-width='1.6'/><polygon points='110,135 160,105 160,15 110,45' fill='#cfdcff' stroke='#1d2540' stroke-width='1.6'/>" + _t(65, 148, lab) + _t(167, 85, lab, 'start'))
def fig_rect(wl, hl, wpx=150, hpx=80, inner=''):
    return svg(wpx + 70, hpx + 50, f"<rect x='14' y='10' width='{wpx}' height='{hpx}' {ST}/>" + _t(14 + wpx / 2, hpx + 32, wl) + _t(wpx + 22, 10 + hpx / 2 + 4, hl, 'start') + (_t(14 + wpx / 2, 10 + hpx / 2 + 4, inner, kh=False) if inner else ''))
def fig_grid(cols, rows):
    """area model: cols=[(label,px)], rows=[(label,px)], cells labelled with product (strings)"""
    W = sum(p for _, p in cols); H = sum(p for _, p in rows); x0, y0 = 40, 28
    body = ''; yy = y0
    for rl, rp, in rows:
        xx = x0
        for cl, cp in cols:
            body += f"<rect x='{xx}' y='{yy}' width='{cp}' height='{rp}' {ST}/>"
            xx += cp
        body += _t(x0 - 8, yy + rp / 2 + 4, rl, 'end')
        yy += rp
    xx = x0
    for cl, cp in cols:
        body += _t(xx + cp / 2, y0 - 8, cl); xx += cp
    return svg(W + x0 + 20, H + y0 + 12, body), (x0, y0)
def grid_with_cells(cols, rows, cells):
    W = sum(p for _, p in cols); H = sum(p for _, p in rows); x0, y0 = 40, 28
    body = ''; yy = y0
    for ri, (rl, rp) in enumerate(rows):
        xx = x0
        for ci, (cl, cp) in enumerate(cols):
            body += f"<rect x='{xx}' y='{yy}' width='{cp}' height='{rp}' {ST}/>"
            if cells and cells[ri][ci]: body += _t(xx + cp / 2, yy + rp / 2 + 4, cells[ri][ci])
            xx += cp
        body += _t(x0 - 8, yy + rp / 2 + 4, rl, 'end'); yy += rp
    xx = x0
    for cl, cp in cols: body += _t(xx + cp / 2, y0 - 8, cl); xx += cp
    return svg(W + x0 + 20, H + y0 + 12, body)
FIG_SQ_AB = grid_with_cells([('a', 90), ('b', 50)], [('a', 90), ('b', 50)], [['a²', 'ab'], ['ab', 'b²']])
FIG_PHOTO = grid_with_cells([('3x', 110), ('2', 40)], [('x', 60), ('1', 25)], [['3x²', '2x'], ['3x', '2']])
FIG_X3X1 = grid_with_cells([('3x', 110), ('1', 40)], [('x', 70)], [['3x²', 'x']])
FIG_GARDEN = fig_rect('5x', '2x', 160, 64)
FIG_POND = fig_rect('4y', 'ប' if False else '?', 150, 64, inner='𝒜 = 16xy²').replace('𝒜 = 16xy²', 'A = 16xy²')

def FIG_TRI():
    return svg(190, 130, f"<polygon points='20,110 170,110 120,20' {ST}/>" + _t(95, 126, '2x') + _t(160, 62, '3y', 'start') + _t(60, 58, '8', 'end') + _t(18, 118, 'A', 'end') + _t(176, 118, 'B', 'start') + _t(120, 14, 'C'))

def cands():
    C = []
    # ================= 1. ឯកធា =================
    C.append(mcq('easy', 'monomial', 'ក្នុងកន្សោមខាងក្រោម កន្សោមមួយណាជាឯកធា?', M('3x^2y'), [M('x + y'), M('3x^2 + 2'), M('\\dfrac{3}{x}')], 'ឯកធាមានតែប្រមាណវិធីគុណ និងស្វ័យគុណដែលនិទស្សន្តជាចំនួនគត់វិជ្ជមានឬសូន្យ។'))
    C.append(mcq('easy', 'monomial', 'កន្សោមមួយណាមិនមែនជាឯកធា?', M('25 - \\dfrac{3}{4}a^4bc^2'), [M('\\dfrac{1}{5}x^2y'), M('zx^2a^3b^4'), M('8')], 'កន្សោមនេះមានវិធីដក ហើយចំនួនថេរ ' + M(8) + ' ជាឯកធា (' + M('8 = 8x^0') + ')។'))
    C.append(mcq('easy', 'monomial', 'ឯកធា ' + M('7x^2y') + ' មានមេគុណស្មើ៖', M(7), [M(2), M(3), M('x^2y')], 'មេគុណជាចំនួនដែលគុណនឹងផ្នែកអថេរ។'))
    C.append(mcq('easy', 'monomial', 'ឯកធា ' + M('-\\dfrac{3}{4}ab^2x') + ' មានអថេរគឺ៖', M('a, b, x'), [M('\\dfrac{3}{4}'), M('a, b'), M('2')], 'មេគុណគឺ ' + M('-\\dfrac{3}{4}') + ' អថេរគឺ ' + M('a, b, x') + '។'))
    C.append(mcq('easy', 'monomial', 'ដឺក្រេនៃឯកធា ' + M('ax^2y') + ' គឺ៖', M(4), [M(3), M(2), M(1)], M('1 + 2 + 1 = 4') + ' (ផលបូកនិទស្សន្តនៃអថេរទាំងអស់)។'))
    C.append(mcq('easy', 'monomial', 'ដឺក្រេនៃចំនួនថេរ ' + M(14) + ' ជាឯកធាគឺ៖', M(0), [M(1), M(14), M(2)], M('14 = 14x^0') + ' ដូចនេះដឺក្រេ ' + M(0) + '។'))
    for (ex, dg) in ((x ** 3 * y * z ** 2 * 8, 6), (21 * a * b ** 4 * c, 6), (3 * x ** 2 * y ** 3 * z ** 4, 9), (Q_(1, 2) * x * y * z, 3)):
        C.append(mcq('medium', 'monomial', 'ដឺក្រេនៃឯកធា ' + ML(ex) + ' គឺ៖', M(dg), [M(dg - 1), M(dg + 1), M(dg + 3)] if dg != 3 else [M(2), M(4), M(1)], 'ផលបូកនិទស្សន្តនៃអថេរទាំងអស់ ' + M(dg) + '។'))
    C.append(mcq('easy', 'monomial', 'ក្នុងបណ្តាឯកធាខាងក្រោម គូណាជាឯកធាដូចគ្នា?', M('5x^2yz^3,\\ \\dfrac{1}{2}x^2yz^3'), [M('5x^2yz^3,\\ \\dfrac{7}{2}x^2cy^3'), M('\\dfrac{1}{2}xy,\\ -2x^2y'), M('ay,\\ 3ax')], 'ឯកធាដូចគ្នាមានផ្នែកអថេរដូចគ្នា។'))
    C.append(mcq('easy', 'monomial', 'ឯកធាដូចគ្នានឹង ' + M('\\dfrac{1}{2}xy') + ' គឺ៖', M('xy'), [M('x^2y'), M('ay'), M('2xy^2')], 'មានផ្នែកអថេរ ' + M('xy') + ' ដូចគ្នា។'))

    def mqs(level, sec, prefix, expr, wrong_strs, sol='', op='expand', suffix=' ៖'):
        e = E(expr)
        if op == 'expand': ans = sp.expand(e)
        elif op == 'simp': ans = sp.simplify(e)
        elif op == 'cancel': ans = sp.cancel(e)
        else: ans = sp.factor(sp.expand(e))
        ws = [E(w) for w in wrong_strs]
        C.append(mcq(level, sec, prefix + M(T(expr)) + suffix, ML(ans), uniqE(ans, ws), sol or (M(T(expr) + ' = ' + L(ans)) + '។')))
    # ---------- monomial add / subtract ----------
    mqs('easy', 'monoadd', 'គណនា ', '2*x*y+5*x*y', ['10*x*y', '7*x**2*y**2', '3*x*y', '7*x*y**2'])
    mqs('easy', 'monoadd', 'គណនា ', '5*x**2*y-3*x**2*y', ['8*x**2*y', '2*x**4*y**2', '2*x*y', '15*x**2*y'])
    mqs('medium', 'monoadd', 'គណនា ', '3*a*b**2+7*a*b**2+a*b**2', ['10*a*b**2', '11*a**3*b**6', '21*a*b**2', '11*a*b'])
    mqs('medium', 'monoadd', 'គណនា ', '8*x**2*y**3*z-3*x**2*y**3*z-7*x**2*y**3*z', ['2*x**2*y**3*z', '-18*x**2*y**3*z', '-2*x**6*y**9*z**3', '-4*x**2*y**3*z'])
    mqs('medium', 'monoadd', 'គណនា ', 'Rational(3,2)*x**4*y**4*t+2*x**4*y**4*t-x**4*y**4*t', ['Rational(7,2)*x**4*y**4*t', '2*x**4*y**4*t', 'Rational(5,2)*x**12*y**12*t**3', 'Rational(3,2)*x**4*y**4*t'])
    # ---------- monomial multiply / divide ----------
    mqs('easy', 'monomul', 'គណនាផលគុណ ', '(5*x)*(2*x)', ['10*x', '7*x**2', '10*x**2*x', '25*x**2'], op='simp')
    mqs('medium', 'monomul', 'គណនាផលគុណ ', '(5*x*y**3)*(x**2*y)', ['5*x**2*y**3', '5*x**3*y**3', '6*x**3*y**4', '5*x**2*y**4'], op='simp')
    mqs('medium', 'monomul', 'គណនាផលគុណ ', 'Rational(1,2)*a*b**3*(3*a**2*b**2)', ['Rational(3,2)*a**2*b**5', 'Rational(3,2)*a**3*b**6', '2*a**3*b**5', 'Rational(1,2)*a**3*b**5'], op='simp')
    mqs('medium', 'monomul', 'គណនាផលគុណ ', '(-4*y**3*c**2*b**3)*(8*y*c**2*b)', ['-32*y**3*c**4*b**3', '32*y**4*c**4*b**4', '-4*y**4*c**4*b**4', '-32*y**4*c**4*b**3'], op='simp')
    mqs('hard', 'monomul', 'គណនាផលគុណ ', '(a*b**2*c**3)*(-4*a*c**2*b)*(a*c*b)', ['4*a**3*b**4*c**6', '-4*a**3*b**3*c**6', '-4*a**3*b**4*c**5', '-4*a*b**4*c**6'], op='simp')
    mqs('hard', 'monomul', 'គណនាផលគុណ ', 'Rational(1,2)*a*c**2*b**3*(-Rational(1,2)*a*c**2*b**3)*(a*c**2*b**3)', ['Rational(1,4)*a**3*b**9*c**6', '-Rational(1,2)*a**3*b**9*c**6', '-Rational(1,4)*a**3*b**9*c**4', '-Rational(1,4)*a*b**3*c**2'], op='simp')
    mqs('medium', 'monodiv', 'គណនាផលចែក ', '(8*x**4*y**5)/(16*x**2*y**3)', ['2*x**2*y**2', 'Rational(1,2)*x**6*y**8', 'Rational(1,2)*x**2*y**3', '2*x**6*y**8'], op='simp')
    mqs('medium', 'monodiv', 'គណនាផលចែក ', '(18*x*y*z**3)/(9*y*z**2)', ['2*x*y*z', '9*x*z', '2*x*z**3', '2*x*y*z**5'], op='simp')
    mqs('easy', 'monodiv', 'គណនាផលចែក ', '(5*x*y**3)/(x*y)', ['5*x**2*y**4', '5*y**3', '5*x*y**2', '4*y**2'], op='simp')
    mqs('hard', 'monodiv', 'គណនាផលចែក ', '(81*z**12*b**3)/(3*z**12*b)', ['27*z**24*b**4', '27*z**12*b**2', '27*b', '78*b**2'], op='simp')
    C.append(mcq('hard', 'monodiv', 'គណនា ' + M('x^{3n} \\div x^{2n}') + '៖', M('x^n'), [M('x^{5n}'), M('x^{6n^2}'), M('x^{n^2}')], M('x^{3n-2n} = x^n') + '។'))
    # ---------- polynomial notion ----------
    C.append(mcq('easy', 'poly', 'ពហុធាដែលមានពីរតួហៅថា៖', 'ទ្វេធា', ['ឯកធា', 'ត្រីធា', 'ពហុធាដឺក្រេទី ២'], M('3x + 1') + ' ជាទ្វេធា។'))
    C.append(mcq('easy', 'poly', 'ពហុធាដែលមានបីតួហៅថា៖', 'ត្រីធា', ['ទ្វេធា', 'ឯកធា', 'ពហុធាដឺក្រេទី ៣'], M('5x^2 - 2x + 7') + ' ជាត្រីធា។'))
    C.append(mcq('easy', 'poly', 'កន្សោមមួយណាមិនមែនជាពហុធា?', M('x + \\dfrac{3}{b^2}'), [M('3x - 8'), M('2k^3 - 4 + k^2 - k'), M('5x^2 - 2x + 1')], M('\\dfrac{3}{b^2}') + ' មិនមែនជាឯកធា។'))
    for (ex, dg) in (('x**2+x-3', 2), ('-Rational(3,4)*x+3', 1), ('a**2+2*a*b+c**2*d', 3), ('y**3+4*y**4*x+7+y', 5), ('2*k**3-4+k**2-k', 3)):
        C.append(mcq('easy' if dg < 3 else 'medium', 'poly', 'ដឺក្រេនៃពហុធា ' + M(T(ex)) + ' គឺ៖', M(dg), [M(dg + 1), M(dg - 1), M(dg + 2)], 'ដឺក្រេនៃពហុធាគឺដឺក្រេរបស់តួដែលមានដឺក្រេខ្ពស់ជាងគេ។'))
    C.append(mcq('medium', 'poly', 'រៀបពហុធា ' + M('11 + 5x^2 - 3x') + ' តាមលំដាប់ចុះ៖', M('5x^2 - 3x + 11'), [M('11 - 3x + 5x^2'), M('5x^2 + 3x + 11'), M('-3x + 5x^2 + 11')], 'រៀបពីដឺក្រេខ្ពស់ទៅទាប។'))
    C.append(mcq('medium', 'poly', 'សរសេរ ' + M(7368) + ' ជាពហុធានៃ ' + M(10) + ' តាមលំដាប់ចុះ៖', M('7 \\times 10^3 + 3 \\times 10^2 + 6 \\times 10 + 8'), [M('7 \\times 10^2 + 3 \\times 10 + 6 + 8'), M('8 \\times 10^3 + 6 \\times 10^2 + 3 \\times 10 + 7'), M('7 + 3 + 6 + 8')], M('7000 + 300 + 60 + 8') + '។'))
    # ---------- polynomial add / sub ----------
    mqs('medium', 'polyadd', 'គណនា ', '(2*x**2+3*x+1)+(-x**2+2*x+4)', ['x**2+x-3', '3*x**2+5*x+5', 'x**2+5*x-3', 'x**2+5*x+4'])
    mqs('medium', 'polyadd', 'គណនា ', '(2*x**2+3*x+1)-(-x**2+2*x+4)', ['x**2+5*x+5', '3*x**2+5*x+5', '3*x**2+x+5', '3*x**2-x-3'])
    mqs('medium', 'polyadd', 'គណនា ', '(12*a**2+2*a*b+54)-(9*a**2-4*a*b-25)', ['3*a**2-2*a*b+29', '21*a**2-2*a*b+29', '3*a**2+6*a*b+29', '3*a**2+6*a*b-79'])
    mqs('medium', 'polyadd', 'គណនា ', '(5*x**3-2*x**2+7*x+4)+(2*x**3+4*x**2-6)', ['7*x**3+6*x**2+7*x-2', '3*x**3-6*x**2+7*x+10', '7*x**3+2*x**2+7*x+10', '10*x**6+7*x+4'])
    mqs('hard', 'polyadd', 'គណនា ', '(5*x**3-2*x**2+7*x+4)-(2*x**3+4*x**2-6)', ['3*x**3+2*x**2+7*x-2', '3*x**3-6*x**2+7*x-2', '7*x**3+2*x**2+7*x-2', '3*x**3-6*x**2+7*x+4'])
    mqs('hard', 'polyadd', 'គណនា ', '(5*a**3*b**2-3*a*b)+(2*a**3*b**2-a*b)', ['7*a**3*b**2-2*a*b', '7*a**6*b**4-4*a**2*b**2', '3*a**3*b**2-2*a*b', '7*a**3*b**2+4*a*b'])
    mqs('hard', 'polyadd', 'គណនា ', '(5*t**3+t-3*b)+(4*t**3-2*t**2+4)+(3*t**3+4*t**2-5)', ['12*t**3+2*t**2+t-3*b-1', '12*t**3-2*t**2+t-3*b-1', '12*t**3+2*t**2+t+3*b-1', '12*t**3+2*t**2+t-3*b+1'])
    # ---------- multiplication ----------
    mqs('easy', 'polymul', 'គណនា ', 'x*(3*x+1)', ['3*x+x', '3*x**2+1', '3*x+1', '4*x**2'])
    mqs('medium', 'polymul', 'គណនា ', '(3*x+2)*(x+1)', ['3*x**2+2', '3*x**2+2*x+2', '3*x**2+5*x+3', '4*x**2+5*x+2'])
    mqs('medium', 'polymul', 'គណនា ', '2*x**2*(2*x**2+3*x-1)', ['4*x**4+3*x-1', '4*x**4+6*x**3-1', '4*x**2+6*x**2-2*x', '4*x**4+6*x**3+2*x**2'])
    mqs('medium', 'polymul', 'គណនា ', '3*x**2*(4*x**3+x*y-5*y**2)', ['12*x**5+3*x**3*y-15*x**2*y**2*2', '12*x**5+3*x*y-5*y**2', '12*x**6+3*x**4*y-15*x**4*y**2', '12*x**5+3*x**3*y+15*x**2*y**2'])
    mqs('medium', 'polymul', 'គណនា ', '(a**2+2*a*b)*(a-b)', ['a**3-2*a*b**2', 'a**3+3*a**2*b-2*a*b**2', 'a**3-a**2*b-2*a*b**2', 'a**3+a**2*b+2*a*b**2'])
    mqs('hard', 'polymul', 'គណនា ', '(9*a**2-25)*(a**5+a*b)', ['9*a**7+9*a**3*b-25*a**5+25*a*b', '9*a**7-25*a**5', '9*a**7+9*a**3*b-25*a**5-25*b', '9*a**7+9*a**2*b-25*a**5-25*a*b'])
    mqs('hard', 'polymul', 'គណនា ', '(x**2-3*x+1)*(2*x-3)', ['2*x**3-3*x**2+2*x-3', '2*x**3-9*x**2+11*x+3', '2*x**3-3*x**2-9*x-3', '2*x**3-6*x**2+2*x-3'])
    mqs('medium', 'polymul', 'គណនា ', '(x**2+2*y)*(x+1)', ['x**3+2*x*y+1', 'x**3+x**2+2*y', 'x**3+x+2*x*y+2*y', 'x**3+x**2+2*y**2+2*y'])
    # ---------- identities ----------
    for (e, wr_) in (('(x+3)**2', ['x**2+9', 'x**2+3*x+9', 'x**2+6*x+6', 'x**2-6*x+9']), ('(2*m+3*n)**2', ['4*m**2+9*n**2', '4*m**2+6*m*n+9*n**2', '2*m**2+12*m*n+3*n**2', '4*m**2-12*m*n+9*n**2']), ('(5*x+2*y)**2', ['25*x**2+4*y**2', '25*x**2+10*x*y+4*y**2', '5*x**2+20*x*y+2*y**2', '25*x**2-20*x*y+4*y**2']), ('(6*x**2+4)**2', ['36*x**4+16', '36*x**4+24*x**2+16', '36*x**2+48*x+16', '12*x**4+48*x**2+16'])):
        mqs('medium', 'identity', 'ពង្រាត ', e, wr_)
    for (e, wr_) in (('(x-1)**2', ['x**2-1', 'x**2+2*x+1', 'x**2-x+1', 'x**2-2*x-1']), ('(x-2*y)**2', ['x**2-4*y**2', 'x**2-2*x*y+4*y**2', 'x**2+4*x*y+4*y**2', 'x**2-4*x*y-4*y**2']), ('(5*b-y)**2', ['25*b**2-y**2', '25*b**2+10*b*y+y**2', '5*b**2-10*b*y+y**2', '25*b**2-5*b*y+y**2'])):
        mqs('medium', 'identity', 'ពង្រាត ', e, wr_)
    mqs('easy', 'identity', 'ពង្រាត ', '(a+5)**2', ['a**2+25', 'a**2+5*a+25', 'a**2+10*a+10', 'a**2-10*a+25'])
    mqs('easy', 'identity', 'ពង្រាត ', '(x-2)*(x+2)', ['x**2+4', 'x**2-4*x-4', 'x**2-2', 'x**2+4*x+4'])
    mqs('medium', 'identity', 'ពង្រាត ', '(x+1)**3', ['x**3+1', 'x**3+3*x+1', 'x**3+x**2+x+1', 'x**3+3*x**2+3*x+3'])
    mqs('hard', 'identity', 'ពង្រាត ', '(x+2*y)**3', ['x**3+8*y**3', 'x**3+6*x**2*y+6*x*y**2+8*y**3', 'x**3+6*x**2*y+12*x*y**2+2*y**3', 'x**3+2*x**2*y+4*x*y**2+8*y**3'])
    mqs('hard', 'identity', 'ពង្រាត ', '(3*x-2*y)**3', ['27*x**3-8*y**3', '27*x**3-18*x**2*y+12*x*y**2-8*y**3', '9*x**3-54*x**2*y+36*x*y**2-8*y**3', '27*x**3+54*x**2*y+36*x*y**2+8*y**3'])
    mqs('medium', 'identity', 'ពង្រាត ', '(x-3)*(x**2+3*x+9)', ['x**3+27', 'x**3-9', 'x**3-3*x**2+9*x-27', 'x**3+3*x**2-27'])
    mqs('hard', 'identity', 'ពង្រាត ', '(2*x+1)*(4*x**2-2*x+1)', ['8*x**3-1', '4*x**3+1', '8*x**3+4*x**2+1', '2*x**3+1'])
    mqs('hard', 'identity', 'ពង្រាត ', '(x-1)**3-(x+2)**3', ['-9*x**2-9*x-9', '-9*x**2-9*x-7', '-6*x**2+9', '-3*x**2-9*x-9'])
    for (txt, ans_) in (('101^2', 10201), ('99^2', 9801)):
        base = int(txt.split('^')[0])
        C.append(mcq('medium', 'identity', 'គណនា ' + M(txt) + ' ដោយប្រើសមភាព' + '៖', M(num(ans_)), [M(num(base * base - 2 * base)), M(num(base * base + 2 * base)), M(num(base * 2))], M(f'({"100+1" if base == 101 else "100-1"})^2 = ' + num(ans_)) + '។'))
    C.append(mcq('medium', 'identity', 'គណនា ' + M('39 \\times 41') + ' ដោយប្រើ ' + M('(a-b)(a+b)') + '៖', M(1599), [M(1600), M(1601), M(1519)], M('(40-1)(40+1) = 40^2 - 1 = 1\\,599') + '។'))
    C.append(mcq('hard', 'identity', 'គណនា ' + M('54^2 - 46^2') + '៖', M(800), [M(8), M(2916), M(100)], M('(54-46)(54+46) = 8 \\times 100') + '។'))
    # ---------- division of polynomials ----------
    mqs('medium', 'polydiv', 'គណនា ', '(15*x**4-30*x**6)/(5*x**2)', ['3*x**2-6*x**4*2', '3*x**2-30*x**6', '3*x**2+6*x**4', '15*x**2-6*x**4'], op='cancel')
    mqs('medium', 'polydiv', 'គណនា ', '(a**2*b**3+2*a*b)/(a*b)', ['a*b**2+2*a*b', 'a*b**2+2*b', 'a**2*b**2+2', 'a*b+2'], op='cancel')
    mqs('hard', 'polydiv', 'គណនា ', '(6*x**2+5*x-4)/(2*x-1)', ['3*x+1', '3*x-4', '3*x+2', '3*x-1'], op='cancel')
    mqs('hard', 'polydiv', 'គណនា ', '(a**2+6*a-55)/(a-5)', ['a-11', 'a+10', 'a+5', 'a+1'], op='cancel')
    C.append(mcq('hard', 'polydiv', 'ផលចែក ' + M('(x^2 - 2x + 4) \\div (x - 1)') + ' ស្មើ៖', M('x - 1 + \\dfrac{3}{x - 1}'), [M('x - 1 + \\dfrac{-3}{x - 1}'), M('x - 1'), M('x + 1 + \\dfrac{3}{x - 1}')], 'ផលចែក ' + M('x - 1') + ' សំណល់ ' + M(3) + '។'))
    C.append(mcq('hard', 'polydiv', 'ក្នុងវិធីចែក ' + M('(8y^3 + 4y^2 - 7) \\div (2y + 3)') + ' សំណល់ស្មើ៖', M(-25), [M(25), M(-7), M(0)], 'ផលចែក ' + M('4y^2 - 4y + 6') + ' សំណល់ ' + M(-25) + '។'))
    # ---------- factoring ----------
    mqs('easy', 'factor', 'ដាក់ជាផលគុណកត្តា ', '3*x+3*y+3*z', ['3*(x+y)+z', '3*x*(y+z)', 'x*(3+y+z)', '(3+x)*(y+z)'], op='factor')
    mqs('medium', 'factor', 'ដាក់ជាផលគុណកត្តា ', '4*a**2+12*a+9', ['(2*a+3)*(2*a-3)', '(4*a+3)**2', '(2*a-3)**2', '(2*a+9)**2'], op='factor')
    mqs('easy', 'factor', 'ដាក់ជាផលគុណកត្តា ', 'x**2-8*x+16', ['(x+4)**2', '(x-4)*(x+4)', '(x-8)**2', '(x-2)*(x-8)'], op='factor')
    mqs('easy', 'factor', 'ដាក់ជាផលគុណកត្តា ', 'x**2-4*y**2', ['(x-4*y)**2', '(x-2*y)**2', '(x+2*y)**2', '(x-4*y)*(x+4*y)'], op='factor')
    mqs('medium', 'factor', 'ដាក់ជាផលគុណកត្តា ', '9*x**2-4', ['(9*x-2)*(x+2)', '(3*x-2)**2', '(3*x+4)*(3*x-4)', '(9*x-4)*(9*x+4)'], op='factor')
    mqs('medium', 'factor', 'ដាក់ជាផលគុណកត្តា ', '5*x**3-80*x', ['5*x*(x-4)**2', '5*x*(x**2-16)*x', '5*(x**3-16*x)', '5*x*(x-16)*(x+1)'], op='factor')
    mqs('medium', 'factor', 'ដាក់ជាផលគុណកត្តា ', '3*x**2+14*x+8', ['(3*x+4)*(x+2)', '(3*x+2)*(x+4)*3', '(3*x-2)*(x-4)', '(3*x+8)*(x+1)'], op='factor')
    mqs('medium', 'factor', 'ដាក់ជាផលគុណកត្តា ', '6*x**2+5*x+1', ['(6*x+1)*(x+1)', '(2*x+1)*(3*x-1)', '(3*x+2)*(2*x+1)*2', '(6*x-1)*(x-1)'], op='factor')
    mqs('hard', 'factor', 'ដាក់ជាផលគុណកត្តា ', 'x**3-2*x**2-4*x+8', ['(x-2)*(x**2+4)', '(x+2)**2*(x-2)', '(x-2)*(x+2)', '(x-2)**3'], op='factor')
    mqs('hard', 'factor', 'ដាក់ជាផលគុណកត្តា ', '8*a*x-b*x+8*a*y-b*y', ['(8*a-b)*(x-y)', '(8*a+b)*(x+y)', '8*a*(x+y)+b*(x+y)', '(8*a-b)*x*y'], op='factor')
    mqs('hard', 'factor', 'ដាក់ជាផលគុណកត្តា ', '8*x**3+y**3', ['(2*x+y)**3', '(2*x+y)*(4*x**2+2*x*y+y**2)', '(2*x-y)*(4*x**2+2*x*y+y**2)', '(8*x+y)*(x**2-x*y+y**2)'], op='factor')
    mqs('hard', 'factor', 'ដាក់ជាផលគុណកត្តា ', '27*y**3-64', ['(3*y-4)**3', '(3*y+4)*(9*y**2-12*y+16)', '(3*y-4)*(9*y**2-12*y+16)', '(27*y-64)*(y**2+y+1)'], op='factor')
    mqs('hard', 'factor', 'ដាក់ជាផលគុណកត្តា ', '9*a**2-(a+2)**2', ['(2*a-2)*(4*a-2)', '(8*a-2)*(a-2)', '(3*a-a+2)*(3*a+a+2)*2', '8*(a-1)*(a+1)'], op='factor')
    mqs('hard', 'factor', 'ដាក់ជាផលគុណកត្តា ', '(a-3*b)**2-9*(a-3*b)', ['(a-3*b)*(a-3*b+9)', '(a-3*b-9)**2', '(a-3*b)**2*(1-9)', '(a-3*b-3)*(a-3*b+3)'], op='factor')
    # ---------- PISA / figures ----------
    C.append(with_img(mcq('pisa', 'figure', 'គូបមួយមានទ្រនុងប្រវែង ' + M('2a') + '។ ផ្ទៃក្រឡានៃមុខមួយគឺ៖', M('4a^2'), [M('2a^2'), M('4a'), M('8a^2')], M('(2a)^2 = 4a^2') + '។'), fig_cube('2a')))
    C.append(with_img(mcq('pisa', 'figure', 'គូបមួយមានទ្រនុងប្រវែង ' + M('2a') + '។ មាឌនៃគូបគឺ៖', M('8a^3'), [M('6a^3'), M('4a^3'), M('8a')], M('(2a)^3 = 8a^3') + '។'), fig_cube('2a')))
    C.append(with_img(mcq('pisa', 'figure', 'សួនច្បារចតុកោណកែងមានបណ្តោយ ' + M('5x') + ' និងទទឹង ' + M('2x') + '។ ផ្ទៃក្រឡា ' + M('\\mathcal{A}') + ' គឺ៖', M('10x^2'), [M('10x'), M('7x^2'), M('7x')], M('(5x)(2x) = 10x^2') + '។'), FIG_GARDEN))
    C.append(with_img(mcq('pisa', 'figure', 'រូបថតមួយមានរាងចតុកោណកែងវិមាត្រ ' + M('3x+2') + ' និង ' + M('x+1') + ' (ម៉ែត្រ)។ ផ្ទៃក្រឡាគឺ៖', M('3x^2 + 5x + 2'), [M('3x^2 + 2'), M('4x + 3'), M('3x^2 + 5x + 3')], M('(3x+2)(x+1) = 3x^2 + 3x + 2x + 2') + '។'), fig_rect('3x + 2', 'x + 1', 160, 70)))
    C.append(with_img(mcq('pisa', 'figure', 'ផ្លូវជុំវិញផ្ទះមានវិមាត្រ ' + M('18a') + ' និង ' + M('12a') + '។ ផ្ទៃក្រឡាផ្លូវគឺ៖', M('216a^2'), [M('30a'), M('216a'), M('30a^2')], M('(18a)(12a) = 216a^2') + '។'), fig_rect('18a', '12a', 160, 108)))
    C.append(with_img(mcq('pisa', 'figure', 'ស្រះទឹករាងចតុកោណកែងមានផ្ទៃក្រឡា ' + M('16xy^2') + ' និងទទឹង ' + M('4y') + '។ បណ្តោយគឺ៖', M('4xy'), [M('12xy'), M('4xy^2'), M('64xy^3')], M('\\dfrac{16xy^2}{4y} = 4xy') + '។'), fig_rect('4y', '?', 150, 64, inner='A = 16xy²')))
    C.append(with_img(mcq('pisa', 'figure', 'ត្រីកោណ ' + M('ABC') + ' មានជ្រុង ' + M('AB = 2x') + ', ' + M('BC = 3y') + ', ' + M('CA = 8') + '។ បរិមាត្រគឺ៖', M('2x + 3y + 8'), [M('5xy + 8'), M('6xy'), M('13xy')], 'បរិមាត្រជាផលបូកជ្រុងទាំងបី។'), FIG_TRI()))
    C.append(with_img(mcq('pisa', 'figure', 'ការេមួយមានជ្រុង ' + M('a + b') + ' ចែកជាបួនផ្នែកដូចរូប។ ផ្ទៃក្រឡាសរុប ' + M('(a+b)^2') + ' ស្មើ៖', M('a^2 + 2ab + b^2'), [M('a^2 + b^2'), M('a^2 + ab + b^2'), M('2a + 2b')], 'ផ្ទៃទាំងបួន ' + M('a^2, ab, ab, b^2') + '។'), FIG_SQ_AB))
    # ================= WRITING =================
    def W(level, sec, stem, steps, img=None):
        q = wr(level, sec, stem, steps)
        if img: q['img'] = img
        C.append(q)
    W('easy', 'monomial', 'ក. ប្រាប់មេគុណ អថេរ និងដឺក្រេនៃ ' + M('-\\dfrac{3}{4}ab^2x') + ' និង ' + M('8x^3yz^2') + '។ ខ. ក្នុង ' + M('\\dfrac{1}{2}xy,\\ -2x^2y,\\ ay,\\ 3ax,\\ 2xy^2,\\ xy') + ' រកឯកធាដូចគ្នា។', [
        ('ក. ' + M('-\\dfrac{3}{4}ab^2x') + ' ៖ មេគុណ ' + M('-\\dfrac{3}{4}') + ' អថេរ ' + M('a, b, x') + ' ដឺក្រេ ' + M('1+2+1 = 4'), 2), (M('8x^3yz^2') + ' ៖ មេគុណ ' + M(8) + ' អថេរ ' + M('x,y,z') + ' ដឺក្រេ ' + M('3+1+2 = 6'), 2), ('ខ. ឯកធាដូចគ្នាគឺ ' + M('\\dfrac{1}{2}xy') + ' និង ' + M('xy'), 1)])
    for (lvl, sec, stem_s, steps_f) in [
        ('medium', 'polyadd', ('គណនា ក. ', '(2*x**2+3*x+1)+(-x**2+2*x+4)', ' ខ. ', '(2*x**2+3*x+1)-(-x**2+2*x+4)'), None),
        ('medium', 'polyadd', ('គណនា ក. ', '(12*a**2+2*a*b+54)+(9*a**2-4*a*b-25)', ' ខ. ', '(12*a**2+2*a*b+54)-(9*a**2-4*a*b-25)'), None),
    ]:
        e1, e2 = E(stem_s[1]), E(stem_s[3])
        W(lvl, sec, stem_s[0] + M(T(stem_s[1])) + stem_s[2] + M(T(stem_s[3])) + '។', [
            ('ក. ផ្ដុំឯកធាដូចគ្នា ' + M(T(stem_s[1])), 1), (M('= ' + L(sp.expand(e1))), 2), ('ខ. ផ្ដុំឯកធាដូចគ្នា (សញ្ញាដកប្តូរសញ្ញាតួក្នុងដង្កៀប)', 1), (M('= ' + L(sp.expand(e2))), 1)])
    W('medium', 'polymul', 'គណនាផលគុណ ក. ' + M('2x^2(2x^2 + 3x - 1)') + ' ខ. ' + M('(a^2 + 2ab)(a - b)') + '។', [
        ('ក. ' + M('2x^2 \\cdot 2x^2 + 2x^2 \\cdot 3x - 2x^2 \\cdot 1'), 1), (M('= 4x^4 + 6x^3 - 2x^2'), 1), ('ខ. ' + M('a^2 \\cdot a - a^2 \\cdot b + 2ab \\cdot a - 2ab \\cdot b'), 2), (M('= a^3 + a^2b - 2ab^2'), 1)])
    W('medium', 'identity', 'ពង្រាត ក. ' + M('(5x + 2y)^2') + ' ខ. ' + M('(x - 4y)^2') + ' គ. ' + M('(x - 2)(x + 2)') + '។', [
        ('ក. ' + M('(5x)^2 + 2(5x)(2y) + (2y)^2 = 25x^2 + 20xy + 4y^2'), 2), ('ខ. ' + M('x^2 - 2(x)(4y) + (4y)^2 = x^2 - 8xy + 16y^2'), 2), ('គ. ' + M('x^2 - 2^2 = x^2 - 4'), 1)])
    W('medium', 'identity', 'គណនាដោយប្រើសមភាពសំខាន់ៗ ក. ' + M('101^2') + ' ខ. ' + M('99^2') + ' គ. ' + M('39 \\times 41') + '។', [
        ('ក. ' + M('(100+1)^2 = 100^2 + 2(100)(1) + 1 = 10\\,201'), 2), ('ខ. ' + M('(100-1)^2 = 10\\,000 - 200 + 1 = 9\\,801'), 2), ('គ. ' + M('(40-1)(40+1) = 40^2 - 1 = 1\\,599'), 1)])
    W('hard', 'polydiv', 'ធ្វើវិធីចែក ' + M('(6x^2 + 5x - 4) \\div (2x - 1)') + ' និង ' + M('(x^2 - 2x + 4) \\div (x - 1)') + '។', [
        ('ក. ' + M('6x^2 \\div 2x = 3x') + ' ; ' + M('3x(2x-1) = 6x^2 - 3x'), 1), ('សំណល់ទី ១ ' + M('8x - 4') + ' ; ' + M('8x - 4 = 4(2x-1)') + ' នាំឱ្យ ផលចែក ' + M('3x + 4') + ' សំណល់ ' + M(0), 2), ('ខ. ' + M('x^2 \\div x = x') + ' សំណល់ ' + M('-x + 4') + ' ; ' + M('-1 \\cdot (x-1)') + ' សំណល់ ' + M(3), 1), (M('\\dfrac{x^2 - 2x + 4}{x - 1} = x - 1 + \\dfrac{3}{x - 1}'), 1)])
    W('hard', 'factor', 'ដាក់ជាផលគុណកត្តា ក. ' + M('x^3 - 2x^2 - 4x + 8') + ' ខ. ' + M('4x^2 + y^2 - b^2 - 4xy') + '។', [
        ('ក. ' + M('(x^3 - 2x^2) - (4x - 8) = x^2(x - 2) - 4(x - 2)'), 1), (M('= (x-2)(x^2 - 4) = (x-2)^2(x+2)'), 2), ('ខ. ' + M('(4x^2 - 4xy + y^2) - b^2 = (2x - y)^2 - b^2'), 1), (M('= (2x - y - b)(2x - y + b)'), 1)])
    W('hard', 'factor', 'ដាក់ជាផលគុណកត្តា ក. ' + M('8x^3 + y^3') + ' ខ. ' + M('27y^3 - 64') + ' គ. ' + M('3x^2 + 14x + 8') + '។', [
        ('ក. ' + M('(2x)^3 + y^3 = (2x + y)(4x^2 - 2xy + y^2)'), 1), ('ខ. ' + M('(3y)^3 - 4^3 = (3y - 4)(9y^2 + 12y + 16)'), 1), ('គ. ' + M('3x^2 + 12x + 2x + 8'), 1), (M('= 3x(x + 4) + 2(x + 4)'), 1), (M('= (x + 4)(3x + 2)'), 1)])
    W('hard', 'identity', 'បង្ហាញថា ក. ' + M('(1+x)(1-x)(1+x^2) = 1 - x^4') + ' ខ. ' + M('5b^2 - 3(b+1)(b-1) = 2b^2 + 3') + '។', [
        ('ក. ' + M('(1+x)(1-x) = 1 - x^2'), 1), (M('(1 - x^2)(1 + x^2) = 1 - x^4') + ' ដូចអង្គខាងស្ដាំ', 2), ('ខ. ' + M('3(b+1)(b-1) = 3(b^2 - 1) = 3b^2 - 3'), 1), (M('5b^2 - (3b^2 - 3) = 2b^2 + 3') + ' ដូចអង្គខាងស្ដាំ', 1)])
    W('pisa', 'figure', 'គូបមួយមានទ្រនុងប្រវែង ' + M('2a') + '។ ក. គណនាផ្ទៃក្រឡានៃមុខមួយ។ ខ. គណនាផ្ទៃក្រឡាសរុបនៃគូប។ គ. គណនាមាឌនៃគូប។', [
        ('ក. ' + M('(2a)^2 = 4a^2'), 1), ('ខ. គូបមាន ' + M(6) + ' មុខ ' + M('6 \\times 4a^2 = 24a^2'), 2), ('គ. ' + M('V = (2a)^3 = 8a^3'), 2)], fig_cube('2a'))
    W('pisa', 'figure', 'រូបថតមួយរាងចតុកោណកែងមានវិមាត្រ ' + M('3x + 2') + ' និង ' + M('x + 1') + ' ម៉ែត្រ។ ក. គណនាផ្ទៃក្រឡារូបថត។ ខ. គណនាបរិមាត្ររូបថត។ គ. គណនាផ្ទៃក្រឡា ពេល ' + M('x = 2') + '។', [
        ('ក. ' + M('(3x+2)(x+1) = 3x^2 + 3x + 2x + 2 = 3x^2 + 5x + 2'), 2), ('ខ. ' + M('P = 2[(3x+2) + (x+1)] = 2(4x + 3) = 8x + 6'), 2), ('គ. ' + M('3(2)^2 + 5(2) + 2 = 12 + 10 + 2 = 24\\ \\text{m}^2'), 1)], FIG_PHOTO)
    W('pisa', 'figure', 'ស្រះទឹករាងចតុកោណកែងមានផ្ទៃក្រឡា ' + M('16xy^2') + ' ទទឹង ' + M('4y') + '។ ក. គណនាបណ្តោយ។ ខ. គណនាបរិមាត្រ។ គ. គណនាបណ្តោយ និងទទឹង ពេល ' + M('x = 3, y = 2') + '។', [
        ('ក. ' + M('\\dfrac{16xy^2}{4y} = 4xy'), 2), ('ខ. ' + M('P = 2(4xy + 4y) = 8xy + 8y'), 1), ('គ. បណ្តោយ ' + M('4(3)(2) = 24') + ' ; ទទឹង ' + M('4(2) = 8'), 2)], fig_rect('4y', '?', 150, 64, inner='A = 16xy²'))
    W('pisa', 'figure', 'ផ្លូវដើរជុំវិញផ្ទះមានវិមាត្រ ' + M('18a') + ' និង ' + M('12a') + '។ ក. គណនាផ្ទៃក្រឡាផ្លូវ។ ខ. គណនាបរិមាត្រផ្លូវ។ គ. បើ ' + M('a = 2\\ \\text{m}') + ' គណនាផ្ទៃក្រឡា។', [
        ('ក. ' + M('(18a)(12a) = 216a^2'), 2), ('ខ. ' + M('P = 2(18a + 12a) = 60a'), 1), ('គ. ' + M('216(2)^2 = 864\\ \\text{m}^2'), 2)], fig_rect('18a', '12a', 160, 108))
    W('pisa', 'figure', 'ត្រីកោណ ' + M('ABC') + ' មានជ្រុង ' + M('AB = 2x') + ', ' + M('BC = 3y') + ', ' + M('CA = 8') + '។ ក. សរសេរបរិមាត្រជាពហុធា។ ខ. ប្រាប់ដឺក្រេនិងចំនួនតួ។ គ. គណនាបរិមាត្រ ពេល ' + M('x = 4, y = 2') + '។', [
        ('ក. ' + M('P = 2x + 3y + 8'), 1), ('ខ. ពហុធាមាន ' + M(3) + ' តួ (ត្រីធា) ដឺក្រេ ' + M(1), 2), ('គ. ' + M('2(4) + 3(2) + 8 = 8 + 6 + 8 = 22'), 2)], FIG_TRI())
    return C
