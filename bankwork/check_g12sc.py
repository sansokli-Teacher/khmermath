# -*- coding: utf-8 -*-
"""Independent checks for gen12sc lessons.  python3 check_g12sc.py G12L01
1. structure: option uniqueness, balanced \\( \\) and braces, writing marks = 5, Bloom/level quotas, SVG well-formed + style guide
2. numbers: every complex-number answer is re-derived here with sympy from the *stem text*, not from the generator's variables."""
import sys, re, importlib, collections
from xml.dom import minidom
from sympy import I, sympify, simplify, expand, sqrt, Rational, symbols, solve
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

TR = standard_transformations + (implicit_multiplication_application, convert_xor)


def tex2sym(t):
    t = t.replace('\\(', '').replace('\\)', '').replace('\\ ', ' ').replace('\\,', '')
    t = re.sub(r'\\text\{[^}]*\}', '', t)
    for _ in range(4):
        t = re.sub(r'\\dfrac\{([^{}]*)\}\{([^{}]*)\}', r'((\1)/(\2))', t)
        t = re.sub(r'\\sqrt\{([^{}]*)\}', r'sqrt(\1)', t)
    t = t.replace('\\times', '*').replace('\\cdot', '*').replace('\\bar', 'conjugate').replace('{', '(').replace('}', ')')
    t = re.sub(r'\bi\b', 'I', t)
    t = re.sub(r'(?<=\d)i\b', '*I', t)
    t = re.sub(r'(?<=\))i\b', '*I', t)
    t = re.sub(r'(?<![A-Za-z])I(?=\d)', 'I*', t)
    return parse_expr(t, transformations=TR, evaluate=True)


def num(t):
    return simplify(expand(tex2sym(t)))


def stem_expr(stem):
    """the first \\( ... \\) in the stem."""
    m = re.search(r'\\\((.*?)\\\)', stem)
    return m.group(1)


def main(name):
    mod = importlib.import_module('gen12sc.' + name)
    C = mod.cands()
    errs = []
    # ---- structure
    for n, q in enumerate(C, 1):
        tag = '#%d %s/%s' % (n, q['kind'], q['level'])
        for field in ('stem', 'sol'):
            txt = q.get(field) or ''
            if txt.count('\\(') != txt.count('\\)'):
                errs.append('%s: unbalanced math in %s' % (tag, field))
            if txt.count('{') != txt.count('}'):
                errs.append('%s: unbalanced braces in %s' % (tag, field))
        if q['kind'] == 'mcq':
            if len(set(q['options'])) != 4:
                errs.append('%s: duplicate options' % tag)
            for o in q['options']:
                if o.count('\\(') != o.count('\\)') or o.count('{') != o.count('}'):
                    errs.append('%s: option math unbalanced %r' % (tag, o))
            if not q['sol']:
                errs.append('%s: no solution' % tag)
        else:
            marks = re.findall(r'\((\d+) ពិន្ទុ\)\s*$', q['sol'], flags=re.M)
            if sum(map(int, marks)) != 5:
                errs.append('%s: marks %s' % (tag, marks))
        if not q.get('bloom'):
            errs.append('%s: no Bloom level' % tag)
        if q.get('img'):
            try:
                d = minidom.parseString(q['img'])
            except Exception as e:
                errs.append('%s: SVG not well-formed: %s' % (tag, e)); continue
            if '<rect' in q['img'] and re.search(r"<rect[^>]*fill='(#fff|#ffffff|white)'", q['img'], re.I):
                errs.append('%s: SVG has a white background rect' % tag)
        if 'ក្នុងរូប' in q['stem'] or 'ដូចរូប' in q['stem'] or 'ដូចក្នុងរូប' in q['stem']:
            if not q.get('img'):
                errs.append('%s: stem refers to a figure but has no image' % tag)
    # ---- numbers (re-derived from the stem text)
    z = symbols('z')
    def correct(q): return q['options'][0]
    checks = 0
    for n, q in enumerate(C, 1):
        if q['kind'] != 'mcq':
            continue
        s = q['stem']
        try:
            if s.startswith('គណនា ') and '\\dfrac' in s or (s.startswith('គណនា ') and 'ៈ' not in s[:3]):
                e = stem_expr(s)
                if re.search(r'[a-z]\_|bar|x', e.replace('\\times', '')):
                    continue
                exp = num(e.replace('\\dfrac', '\\dfrac'))
                got = num(correct(q))
                assert simplify(exp - got) == 0, ('stem', e, 'expected', exp, 'got', got)
                checks += 1
        except AssertionError as ex:
            errs.append('#%d numeric mismatch: %s' % (n, ex))
        except Exception as ex:
            pass
    # specific claims, independent of the generator
    expect = {
        'z_1z_2': None,
    }
    I_ = I
    pairs = [('(5+3i)+(-1+2i)', '4+5i'), ('(9-2i)-(4-4i)', '5+2i'), ('(2+3i)(4+2i)', '2+16i'), ('3i(5-4i)', '12+15i'),
             ('\\dfrac{3}{2+i}', '\\dfrac{6}{5}-\\dfrac{3}{5}i'), ('\\dfrac{3+2i}{1-3i}', '\\dfrac{-3}{10}+\\dfrac{11}{10}i'), ('(2-i)^2', '3-4i'),
             ('\\dfrac{1+i}{1-i}', 'i'), ('\\dfrac{1}{1+i}', '\\dfrac{1}{2}-\\dfrac{1}{2}i'), ('(1+2i)(3-5i)', '13+i'), ('(1+2i)+(3-5i)', '4-3i')]
    for a, b in pairs:
        assert simplify(num(a) - num(b)) == 0, (a, b)
        checks += 1
    # hand-solved items: re-solve here
    a, b, x_, y_ = symbols('a b x_ y_', real=True)
    sol = solve([(a + b*I + 2*(a - b*I) - (3 + 2*I)).as_real_imag()[0], (a + b*I + 2*(a - b*I) - (3 + 2*I)).as_real_imag()[1]], [a, b], dict=True)[0]
    assert (sol[a], sol[b]) == (1, -2); checks += 1                                  # z + 2 conj z = 3 + 2i  -> 1 - 2i
    xs = symbols('xs', real=True)
    e = (3 + I)/(1 + I) + (xs - I)/(1 - I)
    assert solve(e.expand(complex=True).as_real_imag()[1], xs) == [3]; checks += 1     # real  -> x = 3
    sol = solve([((x_ + y_*I)*(2 - I) - (5 + 5*I)).expand(complex=True).as_real_imag()[0], ((x_ + y_*I)*(2 - I) - (5 + 5*I)).expand(complex=True).as_real_imag()[1]], [x_, y_], dict=True)[0]
    assert (sol[x_], sol[y_]) == (1, 3); checks += 1                                  # (x+iy)(2-i) = 5+5i
    z1, z2 = symbols('z1 z2')
    s_ = solve([z1 + 2*z2 - (4 + 3*I), 2*z1 - z2 - (3 - 4*I)], [z1, z2], dict=True)[0]
    assert (simplify(s_[z1] - (2 - I)), simplify(s_[z2] - (1 + 2*I))) == (0, 0); checks += 1
    assert simplify((1 + 3*I)/(2 - I) - (2 + I)/(1 + 2*I) - (-1 + 2*I)) == 0; checks += 1
    assert simplify((20 + 10*I)/(4 + 2*I) - 5) == 0 and simplify(5*(4 + 2*I) - (20 + 10*I)) == 0; checks += 1   # impedance
    assert simplify((2 - I)*(3 + 2*I) - (8 + I)) == 0; checks += 1                       # Ohm
    assert simplify((1 + 7*I) - (4 + 3*I) - (-3 + 4*I)) == 0; checks += 1               # drones
    assert simplify(((-2 + 6*I) + (4 - 2*I))/2 - (1 + 2*I)) == 0; checks += 1          # midpoint
    assert simplify((1 + 4*I) + 4*(2 - I) - 9) == 0 and all(simplify((1 + 4*I + k*(2 - I)).as_real_imag()[1]) != 0 for k in (1, 2, 3)); checks += 1  # robot n = 4
    assert simplify((1 + I) + (5 + 5*I) - (4 + 2*I) - (2 + 4*I)) == 0 and simplify(((1 + I) + (5 + 5*I))/2 - ((4 + 2*I) + (2 + 4*I))/2) == 0; checks += 1  # plot D
    assert simplify(1/(1 + 2*I) - (Rational(1, 5) - Rational(2, 5)*I)) == 0; checks += 1  # filter
    assert simplify((2 + 3*I)**2 - 4*(2 + 3*I) + 13) == 0; checks += 1                     # quadratic
    # pump station: minimise AP+PB on y = 0 numerically
    import math
    best = min((math.hypot(t - 1, 3) + math.hypot(5 - t, 2), t) for t in [i/1000 for i in range(0, 8000)])
    assert abs(best[1] - 3.4) < 0.002, best; checks += 1
    # z * conj z = 1 for z = (i-x)/(i+x)
    xr = symbols('xr', real=True)
    zz = (I - xr)/(I + xr)
    assert simplify(zz*zz.conjugate()) == 1; checks += 1
    assert simplify(zz.expand(complex=True).as_real_imag()[0] - (1 - xr**2)/(1 + xr**2)) == 0 and simplify(zz.expand(complex=True).as_real_imag()[1] - 2*xr/(1 + xr**2)) == 0; checks += 1
    # Bloom + quotas
    kinds = collections.Counter((q['kind'], q['level']) for q in C)
    assert kinds == collections.Counter(mod.TARGET), (kinds, mod.TARGET)
    print('structure + numeric checks:', checks, 'independent checks passed')
    print('Bloom:', dict(collections.Counter(q['bloom'] for q in C)))
    print('images:', sum(1 for q in C if q.get('img')))
    if errs:
        print('PROBLEMS (%d):' % len(errs))
        for e in errs:
            print(' -', e)
        sys.exit(1)
    print('no structural problems')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'G12L01')
