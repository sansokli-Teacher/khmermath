# One-off repair of tools/lesson9_1/build.py (kept for the record): compact grids, the missing examples and practice, full Example 21, corrected practice answers.
import re
p = __file__.replace('_patch1.py', 'build.py')
s = open(p, encoding='utf-8').read()


def sub(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (old[:90], s.count(old))
    s = s.replace(old, new)


def al(*lines):
    """an aligned display equation from several lines (the first holds the left-hand side)"""
    return r"dm(r'\begin{aligned}" + r'\\'.join(lines) + r"\end{aligned}')"


# ------------------------------------------------------------------ helpers and numeric checks (these stay in build.py)
CHECKS = r'''
# numeric checks of the added examples and practice answers (floats, with sample values for the letters)
_v = math.sqrt
_c = lambda x: x ** (1 / 3)
assert near(3 * _v(11) + 5 * _v(44) - 3 * _v(99), 4 * _v(11)) and near(3 * _v(18) - _v(12) + _v(75) + _v(2), 10 * _v(2) + 3 * _v(3))
assert near(3 * _c(24) + 6 * _c(81), 24 * _c(3)) and near(_v(20) + _v(80) - _v(45), 3 * _v(5)) and near(14 * _v(3) + 6 * _v(2) - 11 * _v(3), 3 * _v(3) + 6 * _v(2))
assert near(5 * _v(50) - 8 * _v(32), -7 * _v(2))
for _x in (1.7, 2.9):
    assert near(6 * _c(8 * _x ** 2) - 2 * _c(27 * _x ** 2), 6 * _c(_x ** 2))
    assert near(_v(128 * _x) - _v(2 * _x), 7 * _v(2 * _x)) and near(5 * _v(18 * _x) + 2 * _v(8 * _x), 19 * _v(2 * _x))
    assert near(_v(8 * _x + 8) + _v(2 * _x + 2), 3 * _v(2 * _x + 2)) and near(_v(200 * _x ** 2) - _v(98 * _x ** 2), 3 * _x * _v(2))
    assert near(_v(8 * _x ** 2) + _v(2 * _x ** 2), 3 * _x * _v(2)) and near(2 * _v(45 * _x ** 3) - _v(20 * _x ** 3), 4 * _x * _v(5 * _x))
    assert near(_v(48 * _x) - _v(27 * _x), _v(3 * _x)) and near(_v(5 * _x) + 3 * _v(45 * _x ** 3), (1 + 9 * _x) * _v(5 * _x))
    assert near(_v(12 * _x + 12) + _v(27 * _x + 27), 5 * _v(3 * (_x + 1))) and near(_v(72 * _x) - 3 * _v(98 * _x), -15 * _v(2 * _x))
assert near(_v(7) / _v(28), 1 / 2) and near(_c(5) / _c(0.2), _c(25)) and near(_v(10) / _v(1000), 1 / 10) and near(_c(100) / _c(0.1), 10)
# the book's printed answers for these three practice items disagree with the numbers (see docs/LESSON_G9_1_REPORT.md): these are the checked values
assert near((3 * _v(2) + 2 * _v(3)) / (_v(12) - _v(18)), -5 - 2 * _v(6))
assert near(_c(3) / (_c(4) + _c(2)), (2 * _c(6) - 2 * _c(3) + _c(12)) / 6)
assert near(1 / (_v(5) + _v(2)), (_v(5) - _v(2)) / 3) and near(3 / (_c(5) - _c(4)), 3 * _c(25) + 3 * _c(20) + 6 * _c(2))
assert 3 ** 2 == 9 and 2 ** 3 == 8
'''
sub("S = []\n", r'''def grid(cells, cols=3):
    return (f'<div style="display:grid;grid-template-columns:repeat({cols},1fr);gap:.45em 1.6em;align-items:center">'
            + ''.join(f'<div>{c}</div>' for c in cells) + '</div>')


def lab_cell(lb, body):
    return f'<span style="color:#e03131;font-weight:700;margin-right:.5em">{lb}</span>{body}'


def prac_grid(kick, title, items, cols=3, labels='កខគឃងចឆជឈញដឋឌឍណ'):
    return prac(kick, title, grid([lab_cell(labels[i] + '.', t) for i, t in enumerate(items)], cols))


def sol_grid(kick, title, pairs, cols=3):
    return sol(kick, title, grid([lab_cell(lb, b) for lb, b in pairs], cols))


def near(a, b, tol=1e-9):
    return abs(a - b) < tol * max(1, abs(b))
''' + CHECKS + "\n\nS = []\n")
sub('''    return '<table class="tbl"><tr><th>n</th><th>n²</th><th>n</th><th>n²</th></tr>' + rows + '</table>\'''', '''    return '<table class="tbl" style="font-size:28px"><tr><th>n</th><th>n²</th><th>n</th><th>n²</th></tr>' + rows + '</table>\'''')
sub('''    return '<table class="tbl"><tr><th>n</th><th>n³</th><th>n</th><th>n³</th></tr>' + rows + '</table>\'''', '''    return '<table class="tbl" style="font-size:28px"><tr><th>n</th><th>n³</th><th>n</th><th>n³</th></tr>' + rows + '</table>\'''')

# ------------------------------------------------------------------ 3.2 division: the book's four practice items were missing
sub("# ---------------------------------------------------------------- 3.3 simplifying out of the radical\n", r'''S.append(prac_grid(K[4], 'គណនាផលចែក', [m(r'\dfrac{\sqrt{7}}{\sqrt{28}}'), m(r'\dfrac{\sqrt[3]{5}}{\sqrt[3]{0.2}}'), m(r'\dfrac{\sqrt{10}}{\sqrt{1000}}'), m(r'\dfrac{\sqrt[3]{100}}{\sqrt[3]{0.1}}')], 2))
S.append(sol_grid('ចម្លើយ', 'ដំណោះស្រាយ ផលចែក', [
    ('ក.', m(r'\sqrt{\dfrac{7}{28}}=\sqrt{\dfrac{1}{4}}=\dfrac{1}{2}')),
    ('ខ.', m(r'\sqrt[3]{\dfrac{5}{0.2}}=\sqrt[3]{25}')),
    ('គ.', m(r'\sqrt{\dfrac{10}{1000}}=\sqrt{\dfrac{1}{100}}=\dfrac{1}{10}')),
    ('ឃ.', m(r'\sqrt[3]{\dfrac{100}{0.1}}=\sqrt[3]{1000}=10')),
], 1))

# ---------------------------------------------------------------- 3.3 simplifying out of the radical
''')

# ------------------------------------------------------------------ 3.3: example 15 (equations and taking a number out of the radical)
sub("S.append(key(K[5], 'បញ្ចេញអថេរ',", r'''S.append(ex(K[5], 'ឧទាហរណ៍ទី១៥',
    p('ក. រក ' + m('x') + ' បើ ' + m('x^2=9') + '    ខ. រក ' + m('x') + ' បើ ' + m('x^3=8'))
    + rvd(1, p('ក. ' + m(r'x=\sqrt{9}') + ' ឬ ' + m(r'x=-\sqrt{9}') + '។ ដោយ ' + m('3^2=9') + ' នោះ ' + m(r'\sqrt{9}=\sqrt{3^2}=3') + ' និង ' + m(r'-\sqrt{9}=-3') + '។'))
    + rvd(2, dm(r'\sqrt{3^2}=3\quad(\text{បញ្ចេញ }9\text{ ពីរ៉ាឌីកាល់})'))
    + rvd(3, p('ខ. ' + m(r'x=\sqrt[3]{8}') + '។ ដោយ ' + m('2^3=8') + ' នោះ ' + m(r'\sqrt[3]{8}=\sqrt[3]{2^3}=2') + '។'))
    + rvd(4, dm(r'\sqrt[3]{2^3}=2\quad(\text{បញ្ចេញ }8\text{ ពីរ៉ាឌីកាល់})'))))
S.append(key(K[5], 'បញ្ចេញអថេរ',''')

# ------------------------------------------------------------------ 3.5: full Example 21, Example 22 and the practice
old_start = s.index("S.append(ex(K[7], 'ឧទាហរណ៍ទី២១  A–C',")
old_end = s.index("# ---------------------------------------------------------------- 3.6 rationalise")
new_block = (
    "S.append(ex(K[7], 'ឧទាហរណ៍ទី២១  A , B',\n"
    "    rvd(1, " + al(r"A&=3\sqrt{11}+5\sqrt{4\times 11}-3\sqrt{9\times 11}", r"&=3\sqrt{11}+10\sqrt{11}-9\sqrt{11}=4\sqrt{11}") + ")\n"
    "    + rvd(2, " + al(r"B&=3\sqrt{18}-\sqrt{12}+\sqrt{75}+\sqrt{2}", r"&=3\sqrt{9\times 2}-\sqrt{4\times 3}+\sqrt{25\times 3}+\sqrt{2}", r"&=9\sqrt{2}-2\sqrt{3}+5\sqrt{3}+\sqrt{2}=10\sqrt{2}+3\sqrt{3}") + ")))\n"
    "S.append(ex(K[7], 'ឧទាហរណ៍ទី២១  C , D',\n"
    "    rvd(1, " + al(r"C&=3\sqrt[3]{24}+6\sqrt[3]{81}", r"&=3\sqrt[3]{8\times 3}+6\sqrt[3]{27\times 3}", r"&=6\sqrt[3]{3}+18\sqrt[3]{3}=24\sqrt[3]{3}") + ")\n"
    "    + rvd(2, " + al(r"D&=6\sqrt[3]{8x^2}-2\sqrt[3]{27x^2}", r"&=12\sqrt[3]{x^2}-6\sqrt[3]{x^2}=6\sqrt[3]{x^2}") + ")))\n"
    "S.append(ex(K[7], 'ឧទាហរណ៍ទី២១  E , F',\n"
    "    rvd(1, " + al(r"E&=\sqrt{20}+\sqrt{80}-\sqrt{45}", r"&=\sqrt{4\times 5}+\sqrt{16\times 5}-\sqrt{9\times 5}", r"&=2\sqrt{5}+4\sqrt{5}-3\sqrt{5}=3\sqrt{5}") + ")\n"
    "    + rvd(2, " + al(r"F&=14\sqrt{3}+6\sqrt{2}-11\sqrt{3}", r"&=(14-11)\sqrt{3}+6\sqrt{2}=3\sqrt{3}+6\sqrt{2}") + ")\n"
    "    + rvd(3, p('បើមានរ៉ាឌីកង់ណាដែលខុសគេ យើងគ្រាន់តែទុកវានៅដដែល (ដូចករណី B និង F)។'))))\n"
    "S.append(ex(K[7], 'ឧទាហរណ៍ទី២២  A , B',\n"
    "    p('សម្រួលកន្សោមដែលមានអថេរ (ដោយសន្មតថាអថេរទាំងអស់វិជ្ជមាន)')\n"
    "    + rvd(1, " + al(r"A&=\sqrt{128y}-\sqrt{2y}=\sqrt{64\times 2y}-\sqrt{2y}", r"&=8\sqrt{2y}-\sqrt{2y}=7\sqrt{2y}") + ")\n"
    "    + rvd(2, " + al(r"B&=5\sqrt{18x}+2\sqrt{8x}=5\sqrt{9\times 2x}+2\sqrt{4\times 2x}", r"&=15\sqrt{2x}+4\sqrt{2x}=19\sqrt{2x}") + ")))\n"
    "S.append(ex(K[7], 'ឧទាហរណ៍ទី២២  C , D',\n"
    "    rvd(1, " + al(r"C&=\sqrt{8n+8}+\sqrt{2n+2}=\sqrt{4(2n+2)}+\sqrt{2n+2}", r"&=2\sqrt{2n+2}+\sqrt{2n+2}=3\sqrt{2n+2}") + ")\n"
    "    + rvd(2, " + al(r"D&=\sqrt{200k^2}-\sqrt{98k^2}=\sqrt{100\times 2k^2}-\sqrt{49\times 2k^2}", r"&=10k\sqrt{2}-7k\sqrt{2}=3k\sqrt{2}") + ")))\n"
    "S.append(ex(K[7], 'ឧទាហរណ៍ទី២២  E , F',\n"
    "    rvd(1, " + al(r"E&=\sqrt{8x^2}+\sqrt{2x^2}=\sqrt{4\times 2x^2}+\sqrt{2x^2}", r"&=2x\sqrt{2}+x\sqrt{2}=3x\sqrt{2}") + ")\n"
    "    + rvd(2, " + al(r"F&=2\sqrt{45x^3}-\sqrt{20x^3}=2\sqrt{9\times 5x^3}-\sqrt{4\times 5x^3}", r"&=6x\sqrt{5x}-2x\sqrt{5x}=4x\sqrt{5x}") + ")\n"
    "    + rvd(3, p('ទោះមានអក្សរក៏ដោយ លក្ខណៈនៃការបូកដកនៅតែរក្សាដដែល។'))))\n"
    r'''S.append(prac_grid(K[7], 'សម្រួល', [m(r'5\sqrt{50}-8\sqrt{32}'), m(r'\sqrt{48x}-\sqrt{27x}'), m(r'\sqrt{5P}+3\sqrt{45P^3}\;(P>0)'),
                                         m(r'\sqrt{12x+12}+\sqrt{27x+27}'), m(r'\sqrt{72a}-3\sqrt{98a}')], 2))
S.append(sol_grid('ចម្លើយ', 'ដំណោះស្រាយ សម្រួល', [
    ('ក.', m(r'5(5\sqrt{2})-8(4\sqrt{2})=-7\sqrt{2}')),
    ('ខ.', m(r'4\sqrt{3x}-3\sqrt{3x}=\sqrt{3x}')),
    ('គ.', m(r'\sqrt{5P}+9P\sqrt{5P}=(1+9P)\sqrt{5P}')),
    ('ឃ.', m(r'2\sqrt{3(x+1)}+3\sqrt{3(x+1)}=5\sqrt{3(x+1)}')),
    ('ង.', m(r'6\sqrt{2a}-21\sqrt{2a}=-15\sqrt{2a}')),
], 1))

''')
s = s[:old_start] + new_block + s[old_end:]

# ------------------------------------------------------------------ 3.6: the practice has four items (the book's printed answers for b and d are wrong; see the checks above)
old_start = s.index("S.append(prac(K[8], 'សម្រួល', ul([")
old_end = s.index("# ---------------------------------------------------------------- 9. exercises")
s = s[:old_start] + r'''S.append(prac_grid(K[8], 'សម្រួល', [m(r'\dfrac{1}{\sqrt{5}+\sqrt{2}}'), m(r'\dfrac{3\sqrt{2}+2\sqrt{3}}{\sqrt{12}-\sqrt{18}}'),
                                     m(r'\dfrac{3}{\sqrt[3]{5}-\sqrt[3]{4}}'), m(r'\dfrac{\sqrt[3]{3}}{\sqrt[3]{4}+\sqrt[3]{2}}')], 2))
S.append(sol_grid('ចម្លើយ', 'ដំណោះស្រាយ សម្រួលភាគបែង', [
    ('ក.', m(r'\dfrac{\sqrt{5}-\sqrt{2}}{3}')),
    ('ខ.', m(r'-5-2\sqrt{6}')),
    ('គ.', m(r'3\sqrt[3]{25}+3\sqrt[3]{20}+6\sqrt[3]{2}')),
    ('ឃ.', m(r'\dfrac{2\sqrt[3]{6}-2\sqrt[3]{3}+\sqrt[3]{12}}{6}')),
], 2))

''' + s[old_end:]

# ------------------------------------------------------------------ exercises 1-3: compact grids instead of long lists
sub("S.append(prac('លំហាត់ទី១', 'ចូរគណនា', ul([m(t) for t, _, _ in ex1] + [m(r'\\sqrt[3]{100}')])))",
    "S.append(prac_grid('លំហាត់ទី១', 'ចូរគណនា', [m(t) for t, _, _ in ex1] + [m(r'\\sqrt[3]{100}')], 5))")
sub("""S.append(labs('ដំណោះស្រាយ លំហាត់ទី១', [(LB[i] + '.', dm(tex + '=' + ans)) for i, (tex, ans, _) in enumerate(ex1)]
         + [('ណ.', p(m(r'\\sqrt[3]{100}') + ' ជាចំនួនអសនិទាន ព្រោះ ' + m('4^3=64<100<125=5^3') + '។'))], 'ចម្លើយ'))""",
    """S.append(sol_grid('ចម្លើយ', 'ដំណោះស្រាយ លំហាត់ទី១', [(LB[i] + '.', m(tex + '=' + ans)) for i, (tex, ans, _) in enumerate(ex1)]
         + [('ណ.', m(r'\\sqrt[3]{100}') + ' ជាចំនួនអសនិទាន ព្រោះ ' + m('4^3=64<100<125=5^3') + '។')], 5))""")
sub("S.append(prac('លំហាត់ទី២', 'ចូរគណនា', ul([m(t) for t, _, _ in ex2])))", "S.append(prac_grid('លំហាត់ទី២', 'ចូរគណនា', [m(t) for t, _, _ in ex2], 4))")
sub("S.append(labs('ដំណោះស្រាយ លំហាត់ទី២', [(LB[i] + '.', dm(tex + '=' + ans)) for i, (tex, ans, _) in enumerate(ex2)], 'ចម្លើយ'))",
    "S.append(sol_grid('ចម្លើយ', 'ដំណោះស្រាយ លំហាត់ទី២', [(LB[i] + '.', m(tex + '=' + ans)) for i, (tex, ans, _) in enumerate(ex2)], 4))")
old_start = s.index("S.append(prac('លំហាត់ទី៣', 'ចូរសម្រួលរ៉ាឌីកាល់', ul([")
old_end = s.index("# ---------------------------------------------------------------- 10. PISA")
s = s[:old_start] + r'''S.append(prac_grid('លំហាត់ទី៣', 'ចូរសម្រួលរ៉ាឌីកាល់', [
    m(r'\sqrt{16^3}'), m(r'-\sqrt[3]{36^2}'), m(r'\sqrt{64^3}'), m(r'(\sqrt[3]{-8})^3'),
    m(r'\sqrt[3]{-27^3}'), m(r'\sqrt[3]{1^5}'), m(r'\sqrt[3]{8^2}'), m(r'\sqrt[3]{64^2}'), m(r'\sqrt[3]{(-27)^2}'),
], 3))
S.append(sol_grid('ចម្លើយ', 'ដំណោះស្រាយ លំហាត់ទី៣', [
    ('ក.', m(r'\sqrt{16^3}=64')), ('ខ.', m(r'-\sqrt[3]{36^2}=-6\sqrt[3]{6}')), ('គ.', m(r'\sqrt{64^3}=512')),
    ('ឃ.', m(r'(\sqrt[3]{-8})^3=-8')), ('ង.', m(r'\sqrt[3]{-27^3}=-27')), ('ច.', m(r'\sqrt[3]{1^5}=1')),
    ('ឆ.', m(r'\sqrt[3]{8^2}=4')), ('ជ.', m(r'\sqrt[3]{64^2}=16')), ('ឈ.', m(r'\sqrt[3]{(-27)^2}=9')),
], 3))

''' + s[old_end:]

open(p, 'w', encoding='utf-8').write(s)
print('patched')
