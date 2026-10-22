"""Grade 9 Lesson 1 «ចំនួនអសនិទាន» -> public/js/slides/g9/lesson1.js
python3 tools/lesson9_1/build.py
Wording and numbers follow Lesson/G9/.../L01_irrational_numbers.tex. Every number in a picture or a check is computed here."""
import math, json, os, sys
from fractions import Fraction
HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, '..', 'lesson1'))
sys.path.insert(0, os.path.join(HERE, '..', 'lesson2'))
sys.path.insert(0, os.path.join(HERE, '..', 'lesson12'))
from lib import stepify, slide, part, key, ex, prac, sol, m, dm, p, ul, ol, hl, fig, rvd, chain, cols
from tidy_sol import rebuild, split_solution
from animate import animate_deck
from vis9 import *

OUT = os.path.join(HERE, '..', '..', 'public', 'js', 'slides', 'g9', 'lesson1.js')
K = ['', '១. ឫសការេ', '២. ឫសគូប', '៣.១ គុណ', '៣.២ ចែក', '៣.៣ បញ្ចេញ', '៣.៤ បញ្ចូល', '៣.៥ បូក និងដក', '៣.៦ ភាគបែង', 'លំហាត់', 'PISA']


def factor(n):
    n, f, p = abs(int(n)), {}, 2
    while p * p <= n:
        while n % p == 0:
            f[p] = f.get(p, 0) + 1
            n //= p
        p += 1 if p == 2 else 2
    if n > 1:
        f[n] = 1
    return f


def perfect_power(n, k):
    """True when n is an integer k-th power. A positive integer's k-th root is irrational exactly when some exponent is not a multiple of k
    (if the root were p/q in lowest terms, every exponent in n q^k = p^k would be a multiple of k, hence every exponent in n would be too)."""
    if n < 0:
        return k % 2 == 1 and perfect_power(-n, k)
    if n == 0:
        return True
    return all(e % k == 0 for e in factor(n).values())


assert perfect_power(4, 2) and perfect_power(8, 3) and perfect_power(64, 3)
assert not perfect_power(2, 2) and not perfect_power(3, 2) and not perfect_power(17, 3) and not perfect_power(50, 2)
assert [n * n for n in range(0, 21)] == [0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225, 256, 289, 324, 361, 400]
assert [n ** 3 for n in range(1, 11)] == [1, 8, 27, 64, 125, 216, 343, 512, 729, 1000]


def sq_table(a, b):
    nums = list(range(a, b + 1))
    mid = (len(nums) + 1) // 2
    left, right = nums[:mid], nums[mid:]
    rows = ''
    for i in range(mid):
        n = left[i]
        cell = f'<td>{n}</td><td>{n * n}</td>'
        if i < len(right):
            m_ = right[i]
            cell += f'<td>{m_}</td><td>{m_ * m_}</td>'
        else:
            cell += '<td></td><td></td>'
        rows += f'<tr>{cell}</tr>'
    return big('<table class="tbl"><tr><th>n</th><th>n²</th><th>n</th><th>n²</th></tr>' + rows + '</table>')


def cu_table():
    rows = ''
    for n in range(1, 6):
        m_ = n + 5
        rows += f'<tr><td>{n}</td><td>{n ** 3}</td><td>{m_}</td><td>{m_ ** 3}</td></tr>'
    return big('<table class="tbl"><tr><th>n</th><th>n³</th><th>n</th><th>n³</th></tr>' + rows + '</table>')


def labs(title, pairs, kick):
    """One solution slide per exercise; rebuild/split_solution lays long ones out again."""
    lis = ''.join(f'<li class="lab"><span class="lb">{lb}</span><div>{body}</div></li>' for lb, body in pairs)
    return sol(kick, title, f'<ul class="ts-bullets">{lis}</ul>')


def grid(cells, cols=3):
    return (f'<div style="display:grid;grid-template-columns:repeat({cols},1fr);gap:.45em 1.6em;align-items:center">'
            + ''.join(f'<div>{c}</div>' for c in cells) + '</div>')


def lab_cell(lb, body):
    return f'<span style="color:#e03131;font-weight:700;margin-right:.5em">{lb}</span>{body}'


def prac_grid(kick, title, items, cols=3, labels='កខគឃងចឆជឈញដឋឌឍណ'):
    return prac(kick, title, grid([lab_cell(labels[i] + '.', t) for i, t in enumerate(items)], cols))


def sol_grid(kick, title, pairs, cols=3):
    return sol(kick, title, grid([lab_cell(lb, b) for lb, b in pairs], cols))


def big(table_html, px=24):
    """the table cells carry their own small size: set it on every cell"""
    st = f'font-size:{px}px;padding:2px 14px;line-height:1.25'
    return table_html.replace('<td>', f'<td style="{st}">').replace('<th>', f'<th style="{st}">')


def near(a, b, tol=1e-9):
    return abs(a - b) < tol * max(1, abs(b))

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


def tf_rows(rows, size='1.05em'):
    """statement | answer: the answer appears on its own step (students decide first). rows = [(statement html, True/False, why html)]"""
    cells = []
    for i, (st, ok, why) in enumerate(rows, 1):
        ans = ('<span style="color:#2f9e44;font-weight:800">✓ ពិត</span>' if ok else '<span style="color:#e03131;font-weight:800">✗ មិនពិត</span>') + (' ' + why if why else '')
        cells.append(f'<div style="display:grid;grid-template-columns:1.1fr 1fr;gap:1em;align-items:center;margin:.25em 0"><div><b>{i}.</b> {st}</div>{rvd(i, ans)}</div>')
    return ''.join(cells)


S = []

# ---------------------------------------------------------------- cover and warmup (the book's objectives and reminder, before part 1)
S.append({'k': 'title', 'c': 'cover', 'html':
    '<p class="ts-kicker">ថ្នាក់ទី ៩ · មេរៀនទី ១</p><h1>ចំនួនអសនិទាន</h1>'
    + '<div class="ts-obj"><h3>គោលបំណង</h3><ol class="ts-bullets">'
    + '<li>រកឫសការេនៃមួយចំនួនបានត្រឹមត្រូវ។</li>'
    + '<li>រកឫសគូបនៃមួយចំនួនបានត្រឹមត្រូវ។</li>'
    + '<li>បែងចែកចំនួនសនិទាន និងចំនួនអសនិទានបានដោយមានហេតុផល។</li>'
    + '<li>ធ្វើប្រមាណវិធីលើចំនួនអសនិទានបានយ៉ាងស្ទាត់ជំនាញ។</li></ol></div>'})

def _map_box(no, tex, name, col):
    return (f'<div style="border:4px solid {col};border-radius:18px;background:#fff;padding:.5em .6em .6em;text-align:center;position:relative;min-height:9.5em">'
            f'<span style="position:absolute;left:-.5em;top:-.6em;background:{col};color:#fff;border-radius:50%;width:1.7em;height:1.7em;line-height:1.7em;font-weight:800">{no}</span>'
            f'<div style="color:{col};font-size:1.35em;margin:.5em 0 .3em;min-height:2.6em;display:flex;align-items:center;justify-content:center">{m(tex)}</div>'
            f'<div style="font-weight:700;color:#264b66;font-size:.95em">{name}</div></div>')


_MAP = [('១', r'\sqrt{a}', 'ឫសការេ និងចំនួនអសនិទាន', '#1c7ed6'), ('២', r'\sqrt[3]{a}', 'ឫសគូប', '#2b8a87'),
        ('៣', r'\sqrt{a}\cdot\sqrt{b}=\sqrt{ab}', 'គុណ និងចែករ៉ាឌីកាល់', '#2f9e44'), ('៤', r'3\sqrt{2}=\sqrt{18}', 'បញ្ចេញ និងបញ្ចូល', '#f08c00'),
        ('៥', r'3\sqrt{2}+4\sqrt{2}=7\sqrt{2}', 'បូក និងដក', '#e8590c'), ('៦', r'\dfrac{1}{\sqrt{2}}=\dfrac{\sqrt{2}}{2}', 'បំបាត់រ៉ាឌីកាល់ពីភាគបែង', '#ae3ec9')]
assert 3 * math.sqrt(2) - math.sqrt(18) < 1e-12 and abs(1 / math.sqrt(2) - math.sqrt(2) / 2) < 1e-12 and abs(3 * math.sqrt(2) + 4 * math.sqrt(2) - 7 * math.sqrt(2)) < 1e-12


def _map_row(items, arrow):
    out = ''
    for k, it in enumerate(items):
        out += _map_box(*it) + (f'<div style="align-self:center;font-size:1.8em;color:#868e96">{arrow}</div>' if k < 2 else '')
    return f'<div style="display:grid;grid-template-columns:1fr auto 1fr auto 1fr;gap:.4em;margin:.5em 0">{out}</div>'


S.append(ex('ផែនទីមេរៀន', 'ថ្ងៃនេះយើងនឹងដើរតាមជំហានទាំងប្រាំមួយនេះ',
    _map_row(_MAP[:3], '→') + '<div style="text-align:right;padding-right:3.5em;font-size:1.6em;color:#868e96">↓</div>' + _map_row([_MAP[5], _MAP[4], _MAP[3]], '←')))

S.append(slide('រំលឹក', 'រំលឹកចំណេះដឹង',
    p('តើ ' + m('x') + ' ស្មើប៉ុន្មាន បើ ' + m('x + 5 = 3') + '? យើងទាញបាន ' + m('x = 3 - 5 = -2') + '។')
    + p('ចុះបើ ' + m('2x = 5') + ' វិញ? យើងបាន ' + m(r'x = \dfrac{5}{2} = 2.5') + '។')
    + p('ចំនួនដូចជា ' + m('-2') + ' , ' + m(r'\dfrac{5}{2}') + ' ឬ ' + m('2.5') + ' ទាំងអស់នេះ យើងហៅវាថា ' + hl('ចំនួនសនិទាន') + ' ' + m(r'(\mathbb{Q})') + '។')))
assert 3 - 5 == -2 and Fraction(5, 2) == Fraction('2.5')

S.append(key('រំលឹក', 'ចំនួនការេប្រាកដ និងចំនួនសនិទាន',
    p('ចំនួនការេប្រាកដ គឺជាចំនួនដែលអាចសរសេរជាស្វ័យគុណទី២ នៃចំនួនគត់។')
    + p(m('16 = 4^2') + ', ' + m('25 = 5^2') + ', ' + m('36 = 6^2'))
    + p('ចំនួនសនិទាន គឺជាចំនួនដែលអាចសរសេរជាប្រភាគ ' + m(r'\dfrac{p}{q}') + ' បាន ដែល ' + m('q \\neq 0') + '។')
    + p(m(r'3 = \dfrac{3}{1}') + ' , ' + m(r'0.5 = \dfrac{1}{2}') + ' , ' + m(r'0.333... = \dfrac{1}{3}'))))

assert 3 ** 2 == 9 and (-4) ** 2 == 16 and 2 ** 3 == 8 and (-2) ** 3 == -8 and abs(-8) == 8
S.append(prac('សាកល្បង', 'សាកល្បង',
    ul([m('3^2 = ?'), m('(-4)^2 = ?'), m('2^3 = ?'), m('(-2)^3 = ?'), m('|-8| = ?')])))
S.append(labs('ចម្លើយ សាកល្បង', [
    ('ក.', dm('3^2 = 9')),
    ('ខ.', dm('(-4)^2 = 16')),
    ('គ.', dm('2^3 = 8')),
    ('ឃ.', dm('(-2)^3 = -8')),
    ('ង.', dm('|-8| = 8')),
], 'ចម្លើយ'))

# ---------------------------------------------------------------- 1. square roots and irrationals
S.append(part(1, 'ឫសការេ និងចំនួនអសនិទាន'))
S.append(ex(K[1], 'ទាយសិន',
    p('សួនច្បាររាងការេមួយ មានក្រឡាផ្ទៃ ' + m(r'3\text{ m}^2') + '។ តើប្រវែងជ្រុងប្រហែលប៉ុន្មាន? ' + hl('សរសេរចម្លើយទាយរបស់ប្អូនៗលើក្តារតូច') + '។')
    + rvd(1, p('ជ្រើសមួយ៖ ' + m('1.5') + '   ' + m('1.7') + '   ' + m('2')))
    + rvd(2, p('ពិនិត្យដោយលើកជាការេ៖ ' + m('1.5^2=2.25') + '  ' + m('1.7^2=2.89') + '  ' + m('2^2=4')))
    + rvd(3, p('មួយណាជិត ' + m('3') + ' ជាងគេ? តើមានចំនួនទសភាគណាដែលការេស្មើ ' + m('3') + ' បេះបិទទេ? ' + hl('តោះស្វែងរក!')))))
assert abs(1.5 ** 2 - 2.25) < 1e-12 and abs(1.7 ** 2 - 2.89) < 1e-12 and 2 ** 2 == 4
S.append(ex(K[1], 'សួនច្បាររាងការេ',
    p('ឧបមាថាប្អូនៗមានសួនច្បាររាងការេមួយ ដែលមានក្រឡាផ្ទៃស្មើ ' + m(r'3\text{ m}^2') + '។ បើតាងប្រវែងជ្រុងដោយ ' + m('x') + ' នោះ ' + m('x^2 = 3') + '។')
    + fig(garden_square())))
S.append(key(K[1], 'ចំនួនអសនិទាន',
    p('ចំនួនជាច្រើនយើងអាចសរសេរជាប្រភាគបាន ដូចជា ' + m(r'\dfrac{1}{2}') + ', ' + m(r'\dfrac{3}{4}') + ' ឬ ' + m(r'2=\dfrac{2}{1}') + '។')
    + p('ចំនួនដែលមិនអាចសរសេរជាប្រភាគបាន ដូចជា ' + m(r'\sqrt{2}') + ' ឬ ' + m(r'\sqrt{3}') + ' ហៅថា ' + hl('ចំនួនអសនិទាន') + '។')))
S.append(slide(K[1], 'សំណុំចំនួន', fig(number_sets()) + p(m(r'\mathbb{N} \subset \mathbb{Z} \subset \mathbb{Q} \subset \mathbb{R}') + '។ ' + m(r'\sqrt{2}') + ' និង ' + m(r'\pi') + ' នៅក្នុង ' + m(r'\mathbb{R}') + ' តែនៅក្រៅ ' + m(r'\mathbb{Q}') + '។')))
S.append(ex('បន្ថែម សម្រាប់សិស្សពូកែ', 'ហេតុអ្វី ' + '√2' + ' ជាចំនួនអសនិទាន?',
    p('យើងសន្មតថា ' + m(r'\sqrt{2}') + ' ជាចំនួនសនិទាន ហើយឃើញថាវាប្រែជាផ្ទុយនឹងខ្លួនវា។')
    + rvd(1, p(hl('១.') + ' សន្មតថា ' + m(r'\sqrt{2}=\dfrac{p}{q}') + ' ដែល ' + m('p,q') + ' ជាចំនួនគត់ ហើយប្រភាគនេះសម្រួលអស់ហើយ (គ្មានកត្តារួម)។'))
    + rvd(2, p(hl('២.') + ' លើកជាការេ៖ ' + m(r'2=\dfrac{p^2}{q^2}') + ' នាំឱ្យ ' + m('p^2=2q^2') + '។ ដូចនេះ ' + m('p^2') + ' ជាចំនួនគូ។'))
    + rvd(3, p(hl('៣.') + ' ការេនៃចំនួនសេសជាចំនួនសេស ដូចនេះ ' + m('p') + ' ជាចំនួនគូ។ តាង ' + m('p=2k') + '។'))
    + rvd(4, p(hl('៤.') + ' ជំនួស៖ ' + m('(2k)^2=2q^2') + ' នាំឱ្យ ' + m('q^2=2k^2') + '។ ដូចនេះ ' + m('q') + ' ក៏ជាចំនួនគូដែរ។'))
    + rvd(5, p(hl('៥.') + ' ' + m('p') + ' និង ' + m('q') + ' ទាំងពីរគូ មានកត្តារួម ' + m('2') + ' ផ្ទុយនឹងការសន្មត។ ដូចនេះ ' + hl('√2 មិនមែនជាចំនួនសនិទានទេ') + '។'))))
S.append(key(K[1], 'វិធីសម្រេចចិត្ត ១–៣', ol([
    'បើសរសេរជា ' + m(r'\dfrac{p}{q}') + ' បាន ដែល ' + m('q\\neq 0') + ' នោះវាជា ' + hl('ចំនួនសនិទាន') + '។',
    'បើជា ' + m(r'\sqrt{n}') + ' ហើយ ' + m('n') + ' ជាការេប្រាកដ នោះវាជា ' + hl('ចំនួនសនិទាន') + '។ ឧទាហរណ៍ ' + m(r'\sqrt{49}=7') + '។',
    'បើជា ' + m(r'\sqrt{n}') + ' ហើយ ' + m('n') + ' មិនមែនជាការេប្រាកដ នោះវាជា ' + hl('ចំនួនអសនិទាន') + '។ ឧទាហរណ៍ ' + m(r'\sqrt{50}=5\sqrt{2}') + '។',
])))
S.append(key(K[1], 'វិធីសម្រេចចិត្ត ៤–៥', ol([
    'បើជា ' + m(r'\sqrt[3]{n}') + ' ហើយ ' + m('n') + ' ជាគូបប្រាកដ នោះវាជា ' + hl('ចំនួនសនិទាន') + '។ ឧទាហរណ៍ ' + m(r'\sqrt[3]{-8}=-2') + '។',
    'បើជា ' + m(r'\sqrt[3]{n}') + ' ហើយ ' + m('n') + ' មិនមែនជាគូបប្រាកដ នោះវាជា ' + hl('ចំនួនអសនិទាន') + '។ ឧទាហរណ៍ ' + m(r'\sqrt[3]{4}') + '។',
])))
assert 7 ** 2 == 49 and 50 == 25 * 2 and (-2) ** 3 == -8 and not perfect_power(4, 3)

S.append(key(K[1], 'ចំនួនការេប្រាកដ ពី 0 ដល់ 10', p('ទន្ទេញចាំចំនួនការេពី ' + m('0') + ' ដល់ ' + m('20') + '។') + sq_table(0, 10)))
S.append(key(K[1], 'ចំនួនការេប្រាកដ ពី 11 ដល់ 20', sq_table(11, 20)))

assert 3 ** 2 == 9 and (-3) ** 2 == 9
S.append(ex(K[1], 'ឧទាហរណ៍ទី១',
    p('រក ' + m('x') + ' ដែល ' + m('x^2 = 9') + '។')
    + rvd(1, p('ចំនួនវិជ្ជមាន៖ ' + m('3 \\times 3 = 3^2 = 9') + '។ ដូចនេះ ' + m('x=3') + '។'))
    + rvd(2, p('ចំនួនអវិជ្ជមាន៖ ' + m('(-3)\\times(-3)=9') + '។ ដូចនេះ ' + m('x=-3') + '។'))
    + rvd(3, dm('x = 3 \\text{ ឬ } x = -3'))))
S.append(key(K[1], 'គន្លឹះគ្រូ',
    p('ចំនួនវិជ្ជមានតែងតែមានឫសការេពីរ គឺមួយវិជ្ជមាន និងមួយអវិជ្ជមាន។')
    + p('បើគេសួររកឫសការេនៃ 16 ចម្លើយគឺ 4 និង −4។ តែ ' + m(r'\sqrt{16}') + ' សំដៅតែលើតម្លៃវិជ្ជមាន ' + m('4') + '។')))

assert 5 ** 2 == 25 and (-5) ** 2 == 25
S.append(prac(K[1], 'សាកល្បងខ្លួនឯង', p('ចូររកតម្លៃ ' + m('x') + ' ដែល ' + m('x^2 = 25') + '។')))
S.append(labs('ដំណោះស្រាយ x² = 25', [(' ', dm(r'x=\pm\sqrt{25}=\pm 5') + p('ពិនិត្យ៖ ' + m('5^2=25') + ' និង ' + m('(-5)^2=25') + '។'))], 'ចម្លើយ'))

assert Fraction(5, 2) ** 2 == Fraction(25, 4)
S.append(ex(K[1], 'ឧទាហរណ៍ទី២',
    p('រក ' + m('x') + ' ដែល ' + m(r'x^2 = \dfrac{25}{4}') + '។')
    + rvd(1, dm(r'\left(\dfrac{5}{2}\right)^2 = \dfrac{25}{4}'))
    + rvd(2, dm(r'\left(-\dfrac{5}{2}\right)^2 = \dfrac{25}{4}'))
    + rvd(3, dm(r'x = \dfrac{5}{2} \text{ ឬ } x = -\dfrac{5}{2}'))))
assert Fraction(4, 3) ** 2 == Fraction(16, 9)
S.append(prac(K[1], 'សាកល្បងខ្លួនឯង', p('ចូររកតម្លៃ ' + m('x') + ' ដែល ' + m(r'x^2 = \dfrac{16}{9}') + '។')))
S.append(labs('ដំណោះស្រាយ x² = 16/9', [(' ', dm(r'x=\pm\dfrac{4}{3}'))], 'ចម្លើយ'))

S.append(ex(K[1], 'ឧទាហរណ៍ទី៣  ចន្លោះគត់',
    p('រក ' + m('x') + ' ដែល ' + m('x^2 = 3') + '។ លេខ 3 មិនមែនជាការេប្រាកដទេ។')
    + rvd(1, p(m('1^2 = 1 < 3') + ' និង ' + m('2^2 = 4 > 3') + '។ ដូចនេះ ' + m('x') + ' នៅចន្លោះ 1 និង 2។'))
    + fig(squeeze_sqrt3())))
S.append(ex(K[1], 'ឧទាហរណ៍ទី៣  ទសភាគ',
    p(m('1.5^2 = 2.25 < 3') + ' , ' + m('1.7^2 = 2.89 < 3') + ' , ' + m('1.8^2 = 3.24 > 3') + '។')
    + p('គ្មានចំនួនសនិទានណាមួយ (ទសភាគបញ្ចប់) ដែលមានការេស្មើនឹង 3 បេះបិទនោះទេ។')
    + dm(r'x = \sqrt{3} \text{ ឬ } x = -\sqrt{3}')))
assert Fraction('1.5') ** 2 == Fraction('2.25') < 3
assert Fraction('1.7') ** 2 == Fraction('2.89') < 3
assert Fraction('1.8') ** 2 == Fraction('3.24') > 3
S.append(ex(K[1], 'ដើមការេ',
    cols(fig(plant('sq')),
         p('«ឫស» គឺជាឫសដើមឈើ និងជាឫសនៃចំនួនផងដែរ។ ចំនួននៅលើផ្កា ឫសរបស់វាលាក់នៅក្រោមដី។')
         + rvd(1, p(m('9') + ' → ' + m(r'\sqrt{9}=3') + ' ព្រោះ ' + m('3^2=9') + '។ ឫសជាចំនួនគត់ (សនិទាន)។'))
         + rvd(2, p(m('5') + ' → ' + m(r'\sqrt{5}') + '។ ' + m('5') + ' មិនមែនជាការេប្រាកដ ដូចនេះឫសជាចំនួន' + hl('អសនិទាន') + '។'))
         + rvd(3, p(m('-4') + ' → ' + hl('គ្មាន') + '។ គ្មានចំនួនពិតណាដែលលើកជាការេបាន ' + m('-4') + '។')))))
S.append(key(K[1], 'រ៉ាឌីកាល់',
    p(m(r'\sqrt{3}') + ' អានថា ឫសទីពីរនៃ 3។ ' + m(r'(\sqrt{3})^2 = 3') + '។')
    + p('សញ្ញា ' + m(r'\sqrt{\;}') + ' ហៅថា ' + hl('រ៉ាឌីកាល់') + '។ សន្ទស្សន៍លាក់ទុកស្មើនឹង 2 ហើយលេខ 3 ហៅថា ' + hl('រ៉ាឌីកង់') + '។')
    + p(hl('កុំច្រឡំ') + ' ' + m(r'\sqrt{3} = 1.73') + '។ ' + m(r'\sqrt{3}') + ' ជាតម្លៃពិតប្រាកដ រីឯ 1.73 ជាតម្លៃប្រហែល។ ប្រើ ' + m(r'\approx') + '។')))

S.append(ex(K[1], 'ស្ថាបនា √2', fig(sqrt2_compass()) + p('ត្រីកោណកែងមានជ្រុងកែង 1 និង 1។ អ៊ីប៉ូតេនុស ' + m(r'\sqrt{2}') + ' ត្រូវបានគូសទៅលើបន្ទាត់ចំនួនដោយរង្វាស់ដែកឈាន។')))
S.append(ex(K[1], 'ការេផ្ទៃ 2', fig(square_area2()) + p('ការេដែលមានផ្ទៃ 2 មានជ្រុង ' + m(r'\sqrt{2}') + '។')))
S.append(ex(K[1], 'គូសឫសជាបន្ត', fig(root_spiral()) + p(m(r'\sqrt{2},\sqrt{3},\sqrt{5}') + ' ជាប្រវែងពិតប្រាកដនៃអ៊ីប៉ូតេនុស។')))

S.append(ex(K[1], 'ឧទាហរណ៍ទី៤',
    p('រក ' + m('x') + ' ដែល ' + m('x^2 = -3') + '។')
    + rvd(1, p('វិជ្ជមានគុណវិជ្ជមានបានវិជ្ជមាន ហើយអវិជ្ជមានគុណអវិជ្ជមានក៏បានវិជ្ជមាន។'))
    + rvd(2, p(hl('គ្មានចម្លើយក្នុងចំនួនពិតទេ') + '។ ក្នុងចំនួនពិត ចំនួនអវិជ្ជមានគ្មានឫសការេទេ។'))))
S.append(key(K[1], 'រកឫសការេ',
    ul([
        'បើ ' + m('a > 0') + ' និង ' + m('x^2 = a') + ' គេបាន ' + m(r'x = \sqrt{a}') + ' និង ' + m(r'x = -\sqrt{a}') + '។',
        'បើ ' + m('a = 0') + ' នោះ ' + m('x = 0') + ' តែមួយគត់។',
        'បើ ' + m('a < 0') + ' នោះគ្មានចម្លើយក្នុងចំនួនពិតទេ។',
    ])))

assert 4 ** 2 == 16 and (-4) ** 2 == 16 and not perfect_power(7, 2) and Fraction(5, 2) ** 2 == Fraction(25, 4) and 0 ** 2 == 0
S.append(ex(K[1], 'ឧទាហរណ៍ទី៥  ក–គ',
    rvd(1, p('ក. ' + m('x^2 = 16') + ' ឲ្យ ' + m('x = 4') + ' ឬ ' + m('x = -4') + '។'))
    + rvd(2, p('ខ. ' + m('x^2 = 7') + ' ឲ្យ ' + m(r'x = \sqrt{7}') + ' ឬ ' + m(r'x = -\sqrt{7}') + '។'))
    + rvd(3, p('គ. ' + m(r'x^2 = \dfrac{25}{4}') + ' ឲ្យ ' + m(r'x = \dfrac{5}{2}') + ' ឬ ' + m(r'x = -\dfrac{5}{2}') + '។'))))
S.append(ex(K[1], 'ឧទាហរណ៍ទី៥  ឃ–ច',
    rvd(1, p('ឃ. ' + m('x^2 = -81') + ' គ្មានចម្លើយក្នុងចំនួនពិត។'))
    + rvd(2, p('ង. ' + m('x^2 = 1') + ' ឲ្យ ' + m('x = 1') + ' ឬ ' + m('x = -1') + '។'))
    + rvd(3, p('ច. ' + m('x^2 = 0') + ' ឲ្យ ' + m('x = 0') + ' តែមួយគត់។'))))

assert Fraction('0.2') ** 2 == Fraction('0.04') and Fraction('0.1') ** 2 == Fraction('0.01')
assert Fraction(5, 6) ** 2 == Fraction(25, 36)
assert not perfect_power(5, 2) and not perfect_power(10, 2)
S.append(prac(K[1], 'រកឫសការេ', ul([
    m('0.04'), m('0.01'), m('5'), m('-1'), m(r'\dfrac{25}{36}'), m('0.1'),
])))
S.append(labs('ដំណោះស្រាយ ឫសការេ', [
    ('ក.', dm(r'\sqrt{0.04}=0.2')),
    ('ខ.', dm(r'\sqrt{0.01}=0.1')),
    ('គ.', p(m(r'\sqrt{5}') + ' ជាចំនួនអសនិទាន ព្រោះ 5 មិនមែនជាការេប្រាកដ។')),
    ('ឃ.', p(m(r'\sqrt{-1}') + ' មិនមានក្នុងចំនួនពិត។')),
    ('ង.', dm(r'\sqrt{\dfrac{25}{36}}=\dfrac{5}{6}')),
    ('ច.', p(m(r'\sqrt{0.1}=\dfrac{\sqrt{10}}{10}') + ' ជាចំនួនអសនិទាន។')),
], 'ចម្លើយ'))

S.append(key(K[1], 'កុំច្រឡំ',
    p(hl('កំហុសទី ១') + ' ' + m(r'\sqrt{9} = 3') + ' មិនមែន ' + m(r'\pm 3') + ' ទេ។ សញ្ញាឫសតំណាងឱ្យឫសវិជ្ជមាន។')
    + p('បើ ' + m('x^2 = 9') + ' ទើបមាន ' + m('x = 3') + ' ឬ ' + m('x = -3') + '។')
    + p(hl('កំហុសទី ២') + ' ' + m(r'\sqrt{-4}') + ' គ្មានតម្លៃក្នុងចំនួនពិត។')))
assert 5 ** 2 * 2 == 50 and 7 ** 2 == 49
S.append(ex(K[1], 'សួនផ្ទៃ 50 m²',
    p('ក្រឡាផ្ទៃ ' + m(r'50\text{ m}^2') + ' ឲ្យ ' + m('x^2 = 50') + ' និង ' + m(r'x = \sqrt{50}') + ' ព្រោះប្រវែងវិជ្ជមាន។')
    + dm(r'\sqrt{50}=\sqrt{25\times 2}=5\sqrt{2}')
    + p(m(r'\sqrt{49}=7') + ' ដូច្នេះ ' + m(r'\sqrt{50}') + ' មានប្រវែងប្រហែល 7 ម៉ែត្រជាង។')))

S.append(prac(K[1], 'ចំណាត់ថ្នាក់', ul([m(r'\sqrt{4}'), m(r'\sqrt{5}'), m(r'\sqrt{9}')])))
S.append(labs('ដំណោះស្រាយ ចំណាត់ថ្នាក់', [
    ('ក.', p(m(r'\sqrt{4}=2') + ' ជាចំនួនសនិទាន។')),
    ('ខ.', p(m(r'\sqrt{5}') + ' ជាចំនួនអសនិទាន ព្រោះ 5 មិនមែនជាការេប្រាកដ។')),
    ('គ.', p(m(r'\sqrt{9}=3') + ' ជាចំនួនសនិទាន។')),
], 'ចម្លើយ'))

# ---------------------------------------------------------------- 2. cube roots
import math as _m
assert _m.sqrt(9) == 3 and _m.sqrt(16) == 4 and _m.isqrt(5) ** 2 != 5 and abs(1 / 3 - 0.3333333333) < 1e-9
S.append(ex(K[1], 'ពិនិត្យយល់ ៖ ពិត ឬ មិនពិត?', p('ជ្រើសរើសជាមុន (ដោយដៃ ឬក្តារតូច) រួចទើបមើលចម្លើយ។') + tf_rows([
    (m(r'\sqrt{9}=\pm 3'), False, m(r'\sqrt{9}=3')),
    (m('x^2=9') + ' នោះ ' + m(r'x=3') + ' ឬ ' + m('x=-3'), True, ''),
    (m(r'\sqrt{-4}') + ' មានក្នុងចំនួនពិត', False, 'គ្មានចំនួនពិតណាដែលការេអវិជ្ជមាន'),
    (m(r'\sqrt{5}') + ' ជាចំនួនអសនិទាន', True, m('5') + ' មិនមែនជាការេប្រាកដ'),
    (m(r'0.333\ldots') + ' ជាចំនួនសនិទាន', True, m(r'=\dfrac{1}{3}')),
    (m(r'\sqrt{16}') + ' ជាចំនួនអសនិទាន', False, m(r'\sqrt{16}=4')),
])))
S.append(part(2, 'ឫសគូប'))
S.append(ex(K[2], 'ប្រអប់មាឌ 64', fig(cube64()) + p('បើ ' + m('x^3 = 64') + ' នោះ ' + m(r'x = \sqrt[3]{64} = 4') + '។ ចំនួនអវិជ្ជមានក៏មានឫសគូបបានដែរ។')))
S.append(ex(K[2], 'ដើមគូប',
    cols(fig(plant('cu')),
         p('ដើមគូបមានឫសគូប។ ចំនួនលើផ្កាលើកជាគូប ពីឫសនៅក្រោមដី។')
         + rvd(1, p(m('8') + ' → ' + m(r'\sqrt[3]{8}=2') + ' ព្រោះ ' + m('2^3=8') + '។'))
         + rvd(2, p(m('17') + ' → ' + m(r'\sqrt[3]{17}') + '។ ' + m('17') + ' មិនមែនជាគូបប្រាកដ ដូចនេះជាចំនួន' + hl('អសនិទាន') + '។'))
         + rvd(3, p(m('-27') + ' → ' + m(r'\sqrt[3]{-27}=-3') + ' ព្រោះ ' + m('(-3)^3=-27') + '។ ' + hl('ដើមគូបមានឫសទោះចំនួនអវិជ្ជមាន') + '។')))))
S.append(key(K[2], 'ចំនួនគូបប្រាកដ ពី 1 ដល់ 10', cu_table()))
assert 4 ** 3 == 64 and (-4) ** 3 == -64 and (-3) ** 3 == -27
S.append(ex(K[2], 'ឧទាហរណ៍ទី៦',
    rvd(1, p('ក. ' + m('4\\times 4\\times 4 = 64') + ' តែ ' + m('(-4)^3 = -64') + '។ ដូចនេះ ' + m(r'x=\sqrt[3]{64}=4') + '។'))
    + rvd(2, p('ខ. ' + m('(-3)^3 = -27') + '។ ដូចនេះ ' + m(r'x=\sqrt[3]{-27}=-3') + '។'))))
assert 5 ** 3 == 125 and (-2) ** 3 == -8
S.append(prac(K[2], 'សាកល្បងខ្លួនឯង', p('ចូររកឫសគូបនៃ ' + m('125') + ' និង ' + m('-8') + '។')))
S.append(labs('ដំណោះស្រាយ ឫសគូប 125 និង −8', [
    ('ក.', dm(r'\sqrt[3]{125}=5')),
    ('ខ.', dm(r'\sqrt[3]{-8}=-2')),
], 'ចម្លើយ'))
S.append(ex(K[2], 'ឧទាហរណ៍ទី៧',
    p(m('17') + ' មិនមែនជាគូបប្រាកដទេ។') + fig(squeeze_cbrt17())
    + rvd(1, dm(r'x=\sqrt[3]{17}'))
    + rvd(2, dm(r'x=\sqrt[3]{-17}=-\sqrt[3]{17}'))))
S.append(key(K[2], 'រកឫសគូប', p('បើ ' + m('x^3 = a') + ' គេបាន ' + m(r'x = \sqrt[3]{a}') + ' ដែល ' + m('a') + ' អាចវិជ្ជមាន ឬអវិជ្ជមាន។')))

cube_ex = [
    ('ក.', -64, -4), ('ខ.', -1, -1), ('គ.', 1, 1), ('ឃ.', -8, -2),
    ('ច.', 0, 0), ('ឆ.', Fraction(1, 8), Fraction(1, 2)),
    ('ជ.', Fraction(27, 125), Fraction(3, 5)), ('ឈ.', Fraction(-1, 1000), Fraction(-1, 10)),
]
for lb, a, r in cube_ex:
    assert r ** 3 == a
assert not perfect_power(4, 3)
S.append(ex(K[2], 'ឫសគូប ក–ឃ', ul([
    m('x^3=-64') + ' ឲ្យ ' + m(r'x=-4'),
    m('x^3=-1') + ' ឲ្យ ' + m(r'x=-1'),
    m('x^3=1') + ' ឲ្យ ' + m(r'x=1'),
    m('x^3=-8') + ' ឲ្យ ' + m(r'x=-2'),
])))
S.append(ex(K[2], 'ឫសគូប ង–ឈ', ul([
    m('x^3=4') + ' ឲ្យ ' + m(r'x=\sqrt[3]{4}') + ' (អសនិទាន)',
    m('x^3=0') + ' ឲ្យ ' + m('x=0'),
    m(r'x^3=\dfrac{1}{8}') + ' ឲ្យ ' + m(r'x=\dfrac{1}{2}'),
    m(r'x^3=\dfrac{27}{125}') + ' ឲ្យ ' + m(r'x=\dfrac{3}{5}'),
    m(r'x^3=-\dfrac{1}{1000}') + ' ឲ្យ ' + m(r'x=-\dfrac{1}{10}'),
])))
assert Fraction(8, 1000) == Fraction('0.008') and Fraction(2, 10) ** 3 == Fraction(8, 1000)
assert -Fraction(1, 10) ** 3 == Fraction('-0.001')
S.append(prac(K[2], 'ឫសគូបទសភាគ', ul([m('0.008'), m('-0.001'), m('0.08'), m('-0.4')])))
S.append(labs('ដំណោះស្រាយ ឫសគូបទសភាគ', [
    ('ក.', dm(r'\sqrt[3]{0.008}=0.2')),
    ('ខ.', dm(r'\sqrt[3]{-0.001}=-0.1')),
    ('គ.', p(m(r'\sqrt[3]{0.08}=\dfrac{\sqrt[3]{10}}{5}') + ' ជាចំនួនអសនិទាន។')),
    ('ឃ.', p(m(r'\sqrt[3]{-0.4}') + ' ជាចំនួនអសនិទាន។')),
], 'ចម្លើយ'))
assert (-2) ** 3 == -8 and 3 ** 3 == 27
S.append(prac(K[2], 'ប្រៀបធៀបឫស', ul([
    m(r'\sqrt[3]{-8}=?'), m(r'\sqrt[3]{27}=?'), m(r'\sqrt{-4}') + ' មានឬគ្មាន?',
])))
S.append(labs('ដំណោះស្រាយ ប្រៀបធៀបឫស', [
    ('ក.', dm('-2')), ('ខ.', dm('3')), ('គ.', p('គ្មាន')),
], 'ចម្លើយ'))

# ---------------------------------------------------------------- 3.1 multiplication
S.append(part(3, 'វិធីគុណរ៉ាឌីកាល់', '<p class="ts-sub">៣. ប្រមាណវិធីលើរ៉ាឌីកាល់</p>'))
S.append(key(K[3], 'ផ្លូវធ្វើលំហាត់', ol([
    'មើលសន្ទស្សន៍សិន។ ឫសការេត្រូវរកគូកត្តា ឫសគូបត្រូវរកកត្តាបីដូចគ្នា។',
    'បំបែករ៉ាឌីកង់ជាផលគុណដែលមានការេប្រាកដ ឬគូបប្រាកដ។',
    'សម្រួលរ៉ាឌីកាល់មុនបូកដក។ បូកដកបានតែពេលរ៉ាឌីកង់ និងសន្ទស្សន៍ដូចគ្នា។',
    'ផលគុណ ឬផលចែក អាចដាក់ចូលក្នុងរ៉ាឌីកាល់តែមួយបាន បើសន្ទស្សន៍ដូចគ្នា។',
    'បើមានរ៉ាឌីកាល់នៅភាគបែង ត្រូវបំបាត់វាជាចុងក្រោយ។',
])))
assert math.isqrt(4) * math.isqrt(9) == 6 and math.isqrt(36) == 6
S.append(ex(K[3], 'ឧទាហរណ៍ទី៨', fig(area_product())
    + rvd(1, dm(r'\sqrt{4}\times\sqrt{9}=2\times 3=6'))
    + rvd(2, dm(r'\sqrt{4\times 9}=\sqrt{36}=6'))))
assert 2 * 3 == 6 and 6 ** 3 == 216
S.append(ex(K[3], 'ឧទាហរណ៍ទី៩',
    rvd(1, dm(r'\sqrt[3]{8}\times\sqrt[3]{27}=2\times 3=6'))
    + rvd(2, dm(r'\sqrt[3]{8\times 27}=\sqrt[3]{216}=6'))))
S.append(key(K[3], 'ផលគុណរ៉ាឌីកាល់',
    dm(r'\sqrt{a}\times\sqrt{b}=\sqrt{ab}\quad (a\ge 0,\; b\ge 0)')
    + dm(r'\sqrt[3]{a}\times\sqrt[3]{b}=\sqrt[3]{ab}')
    + p(m(r'm\sqrt{a}\times n\sqrt{b}=(m\times n)\sqrt{a\times b}'))))
S.append(key(K[3], 'កំហុសធំ',
    p('កុំច្រឡំថា ' + m(r'\sqrt{a}+\sqrt{b}=\sqrt{a+b}') + '។')
    + p(m(r'\sqrt{9+16}=\sqrt{25}=5') + ' មិនមែន ' + m(r'\sqrt{9}+\sqrt{16}=7') + ' ទេ។')))
assert 9 + 16 == 25 and 3 + 4 == 7 and 5 != 7
prod = [(r'\sqrt{2}\times\sqrt{8}', 4), (r'\sqrt{3}\times\sqrt{27}', 9), (r'\sqrt{2}\times\sqrt{32}', 8), (r'\sqrt{50}\times\sqrt{2}', 10)]
assert 2 * 8 == 16 and 3 * 27 == 81 and 2 * 32 == 64 and 50 * 2 == 100
assert 2 * 4 == 8 and Fraction(2, 16) == Fraction(1, 8) and Fraction(1, 2) ** 3 == Fraction(1, 8)
S.append(ex(K[3], 'ឧទាហរណ៍ទី១០  ក–គ',
    rvd(1, dm(r'\sqrt{2}\times\sqrt{8}=\sqrt{16}=4'))
    + rvd(2, dm(r'\sqrt{3}\times\sqrt{27}=\sqrt{81}=9'))
    + rvd(3, dm(r'\sqrt[3]{2}\times\sqrt[3]{4}=\sqrt[3]{8}=2'))))
S.append(ex(K[3], 'ឧទាហរណ៍ទី១០  ឃ–ច',
    rvd(1, dm(r'\sqrt[3]{2}\times\sqrt[3]{\dfrac{1}{16}}=\sqrt[3]{\dfrac{1}{8}}=\dfrac{1}{2}'))
    + rvd(2, dm(r'\sqrt{2}\times\sqrt{32}=\sqrt{64}=8'))
    + rvd(3, dm(r'\sqrt{50}\times\sqrt{2}=\sqrt{100}=10'))))
assert Fraction(10) * Fraction('0.1') == 1
S.append(prac(K[3], 'គណនា', ul([m(r'\sqrt{10}\times\sqrt{0.1}'), m(r'\sqrt[3]{10}\times\sqrt[3]{0.1}')])))
S.append(labs('ដំណោះស្រាយ គុណ 10 និង 0.1', [
    ('ក.', dm(r'\sqrt{10\times 0.1}=\sqrt{1}=1')),
    ('ខ.', dm(r'\sqrt[3]{10\times 0.1}=\sqrt[3]{1}=1')),
], 'ចម្លើយ'))

# ---------------------------------------------------------------- 3.2 division
S.append(part(4, 'វិធីចែករ៉ាឌីកាល់'))
assert math.isqrt(36) / math.isqrt(4) == 3 and 36 / 4 == 9
S.append(ex(K[4], 'ឧទាហរណ៍ទី១១',
    rvd(1, dm(r'\dfrac{\sqrt{36}}{\sqrt{4}}=\dfrac{6}{2}=3'))
    + rvd(2, dm(r'\sqrt{\dfrac{36}{4}}=\sqrt{9}=3'))))
assert 27 / 8 == 3.375 and Fraction(3, 2) ** 3 == Fraction(27, 8)
S.append(ex(K[4], 'ឧទាហរណ៍ទី១២',
    rvd(1, dm(r'\dfrac{\sqrt[3]{27}}{\sqrt[3]{8}}=\dfrac{3}{2}'))
    + rvd(2, dm(r'\sqrt[3]{\dfrac{27}{8}}=\dfrac{3}{2}'))))
S.append(key(K[4], 'ផលចែករ៉ាឌីកាល់',
    dm(r'\dfrac{\sqrt{a}}{\sqrt{b}}=\sqrt{\dfrac{a}{b}}\quad (a\ge 0,\; b>0)')
    + dm(r'\dfrac{\sqrt[3]{a}}{\sqrt[3]{b}}=\sqrt[3]{\dfrac{a}{b}}\quad (b\neq 0)')))
assert 8 / 2 == 4 and 48 / 6 == 8 and Fraction(3, 27) == Fraction(1, 9)
assert 288 / 2 == 144 and 16 / 2 == 8 and Fraction(1, 2) / 4 == Fraction(1, 8)
assert Fraction(10) / Fraction('0.1') == 100 and Fraction(25) / Fraction('0.2') == 125
S.append(ex(K[4], 'ឧទាហរណ៍ទី១៣  ក–ឃ',
    rvd(1, dm(r'\dfrac{\sqrt{8}}{\sqrt{2}}=\sqrt{4}=2'))
    + rvd(2, dm(r'\dfrac{\sqrt[3]{48}}{\sqrt[3]{6}}=\sqrt[3]{8}=2'))
    + rvd(3, dm(r'\dfrac{\sqrt{3}}{\sqrt{27}}=\sqrt{\dfrac{1}{9}}=\dfrac{1}{3}'))
    + rvd(4, dm(r'\dfrac{\sqrt{288}}{\sqrt{2}}=\sqrt{144}=12'))))
S.append(ex(K[4], 'ឧទាហរណ៍ទី១៣  ង–ជ',
    rvd(1, dm(r'\dfrac{\sqrt[3]{16}}{\sqrt[3]{2}}=\sqrt[3]{8}=2'))
    + rvd(2, dm(r'\dfrac{\sqrt[3]{\frac{1}{2}}}{\sqrt[3]{4}}=\sqrt[3]{\dfrac{1}{8}}=\dfrac{1}{2}'))
    + rvd(3, dm(r'\dfrac{\sqrt{10}}{\sqrt{0.1}}=\sqrt{100}=10'))
    + rvd(4, dm(r'\dfrac{\sqrt[3]{25}}{\sqrt[3]{0.2}}=\sqrt[3]{125}=5'))))

S.append(prac_grid(K[4], 'គណនាផលចែក', [m(r'\dfrac{\sqrt{7}}{\sqrt{28}}'), m(r'\dfrac{\sqrt[3]{5}}{\sqrt[3]{0.2}}'), m(r'\dfrac{\sqrt{10}}{\sqrt{1000}}'), m(r'\dfrac{\sqrt[3]{100}}{\sqrt[3]{0.1}}')], 2))
S.append(sol_grid('ចម្លើយ', 'ដំណោះស្រាយ ផលចែក', [
    ('ក.', m(r'\sqrt{\dfrac{7}{28}}=\sqrt{\dfrac{1}{4}}=\dfrac{1}{2}')),
    ('ខ.', m(r'\sqrt[3]{\dfrac{5}{0.2}}=\sqrt[3]{25}')),
    ('គ.', m(r'\sqrt{\dfrac{10}{1000}}=\sqrt{\dfrac{1}{100}}=\dfrac{1}{10}')),
    ('ឃ.', m(r'\sqrt[3]{\dfrac{100}{0.1}}=\sqrt[3]{1000}=10')),
], 1))

# ---------------------------------------------------------------- 3.3 simplifying out of the radical
S.append(part(5, 'ការបញ្ចេញមួយចំនួនពីរ៉ាឌីកាល់'))
S.append(ex(K[5], 'ឈ្មោះផ្នែកនៃរ៉ាឌីកាល់', fig(radical_anatomy())))
S.append(ex(K[5], 'ផ្ទៃ 18', fig(simplify_18())
    + p('ដើម្បីចេញពីរ៉ាឌីកាល់ លេខត្រូវមានស្វ័យគុណស្មើនឹងសន្ទស្សន៍។')))
assert 72 == 2 ** 3 * 3 ** 2 and 2 * 3 == 6
S.append(ex(K[5], 'ជំហាន √72',
    rvd(1, dm(r'72 = 2^3 \times 3^2'))
    + rvd(2, dm(r'72 = 2^2 \times 3^2 \times 2'))
    + rvd(3, dm(r'\sqrt{72}=2\times 3\times\sqrt{2}=6\sqrt{2}'))))
assert 18 == 9 * 2 and 72 == 36 * 2 and 200 == 100 * 2
S.append(ex(K[5], 'ឧទាហរណ៍ទី១៤',
    rvd(1, dm(r'\sqrt{18}=\sqrt{9\times 2}=3\sqrt{2}'))
    + rvd(2, dm(r'\sqrt{72}=\sqrt{36\times 2}=6\sqrt{2}'))
    + rvd(3, dm(r'\sqrt{200x^3}=10x\sqrt{2x}\quad (x>0)'))))
S.append(ex(K[5], 'ឧទាហរណ៍ទី១៥',
    p('ក. រក ' + m('x') + ' បើ ' + m('x^2=9') + '    ខ. រក ' + m('x') + ' បើ ' + m('x^3=8'))
    + rvd(1, p('ក. ' + m(r'x=\sqrt{9}') + ' ឬ ' + m(r'x=-\sqrt{9}') + '។ ដោយ ' + m('3^2=9') + ' នោះ ' + m(r'\sqrt{9}=\sqrt{3^2}=3') + ' និង ' + m(r'-\sqrt{9}=-3') + '។'))
    + rvd(2, dm(r'\sqrt{3^2}=3\quad(\text{បញ្ចេញ }9\text{ ពីរ៉ាឌីកាល់})'))
    + rvd(3, p('ខ. ' + m(r'x=\sqrt[3]{8}') + '។ ដោយ ' + m('2^3=8') + ' នោះ ' + m(r'\sqrt[3]{8}=\sqrt[3]{2^3}=2') + '។'))
    + rvd(4, dm(r'\sqrt[3]{2^3}=2\quad(\text{បញ្ចេញ }8\text{ ពីរ៉ាឌីកាល់})'))))
S.append(key(K[5], 'បញ្ចេញអថេរ',
    p(m(r'\sqrt{x^2}=|x|') + '។ បើ ' + m('x\\ge 0') + ' នោះ ' + m(r'\sqrt{x^2}=x') + ' បើ ' + m('x\\le 0') + ' នោះ ' + m(r'\sqrt{x^2}=-x') + '។')
    + p(m(r'\sqrt[3]{x^3}=x') + '។')))
assert 11 ** 2 == 121 and Fraction(2, 3) ** 2 == Fraction(4, 9) and 5 ** 3 == 125
assert (4 * 9) ** 2 == 16 * 81 and (-3) ** 3 == -27 and Fraction(1, 10) ** 3 == Fraction(1, 1000)
S.append(ex(K[5], 'ឧទាហរណ៍ទី១៦',
    ul([
        m(r'\sqrt{121}=11'), m(r'\sqrt{\dfrac{4}{9}}=\dfrac{2}{3}'), m(r'\sqrt[3]{125}=5'),
        m(r'\sqrt{16\times 81}=36'), m(r'\sqrt[3]{-27}=-3'), m(r'\sqrt[3]{\dfrac{2}{2000}}=\dfrac{1}{10}'),
    ])))
assert 32 == 16 * 2 and 16 == 8 * 2
S.append(ex(K[5], 'ឧទាហរណ៍ទី១៧',
    rvd(1, dm(r'\sqrt{32}=\sqrt{16\times 2}=4\sqrt{2}'))
    + rvd(2, dm(r'\sqrt[3]{16}=\sqrt[3]{8\times 2}=2\sqrt[3]{2}'))))
assert Fraction(2, 8) == Fraction(1, 4) and 81 / 3 == 27 and 27 == 9 * 3
assert 12 == 4 * 3 and 81 == 27 * 3 and 50 == 25 * 2
S.append(prac(K[5], 'បញ្ចេញ', ul([
    m(r'\sqrt{\dfrac{2}{8}}'), m(r'\sqrt{\dfrac{81}{3}}'), m(r'\sqrt{12}'),
    m(r'\sqrt[3]{81}'), m(r'\sqrt{50}'), m(r'\sqrt{\dfrac{2}{25}}'),
])))
S.append(labs('ដំណោះស្រាយ បញ្ចេញ', [
    ('ក.', dm(r'\sqrt{\dfrac{2}{8}}=\dfrac{1}{2}')),
    ('ខ.', dm(r'\sqrt{27}=3\sqrt{3}')),
    ('គ.', dm(r'\sqrt{12}=2\sqrt{3}')),
    ('ឃ.', dm(r'\sqrt[3]{81}=3\sqrt[3]{3}')),
    ('ង.', dm(r'\sqrt{50}=5\sqrt{2}')),
    ('ច.', dm(r'\sqrt{\dfrac{2}{25}}=\dfrac{\sqrt{2}}{5}')),
], 'ចម្លើយ'))

# ---------------------------------------------------------------- 3.4 putting a number into the radical
S.append(part(6, 'ការបញ្ចូលមួយចំនួនក្នុងរ៉ាឌីកាល់'))
S.append(key(K[6], 'ងាយយល់', p('ការបញ្ចូលជាវិធីច្រាសនៃការបញ្ចេញ។ មុននឹងបញ្ចូល ត្រូវបំពាក់ស្វ័យគុណឱ្យស្មើនឹងសន្ទស្សន៍។')))
assert 4 ** 2 * 2 == 32 and 3 ** 3 * 2 == 54
S.append(ex(K[6], 'ឧទាហរណ៍ទី១៨',
    rvd(1, dm(r'4\sqrt{2}=\sqrt{4^2\times 2}=\sqrt{32}'))
    + rvd(2, dm(r'3\sqrt[3]{2}=\sqrt[3]{3^3\times 2}=\sqrt[3]{54}'))))
S.append(key(K[6], 'វិធីបញ្ចូល', p('លើកចំនួនដែលនឹងបញ្ចូល ជាស្វ័យគុណដែលនិទស្សន្តស្មើនឹងសន្ទស្សន៍នៃរ៉ាឌីកាល់។')))
assert Fraction(4, 9) * Fraction(12, 5) == Fraction(48, 45) == Fraction(16, 15)
assert 25 * Fraction(3, 50) == Fraction(3, 2)
assert 49 * 5 == 245
assert (-5) ** 3 * Fraction(4, 25) == -20
assert 8 * Fraction(5, 12) == Fraction(10, 3)
assert Fraction(1, 8) * 4 == Fraction(1, 2)
S.append(ex(K[6], 'ឧទាហរណ៍ទី១៩  ក–គ',
    rvd(1, dm(r'\dfrac{2}{3}\sqrt{\dfrac{12}{5}}=\sqrt{\dfrac{16}{15}}'))
    + rvd(2, dm(r'5\sqrt{\dfrac{3}{50}}=\sqrt{\dfrac{3}{2}}'))
    + rvd(3, dm(r'-7\sqrt{5}=-\sqrt{245}'))))
S.append(ex(K[6], 'ឧទាហរណ៍ទី១៩  ឃ–ច',
    rvd(1, dm(r'-5\sqrt[3]{\dfrac{4}{25}}=\sqrt[3]{-20}'))
    + rvd(2, dm(r'2\sqrt[3]{\dfrac{5}{12}}=\sqrt[3]{\dfrac{10}{3}}'))
    + rvd(3, dm(r'\dfrac{1}{2}\sqrt[3]{4}=\sqrt[3]{\dfrac{1}{2}}'))))
assert Fraction(1, 3) ** 2 * 3 == Fraction(1, 3)
assert 125 * Fraction(2, 25) == 10
assert Fraction(4, 121) * Fraction(121, 7) == Fraction(4, 7)
S.append(prac(K[6], 'បញ្ចូល', ul([
    m(r'\sqrt[3]{\dfrac{1}{3}}'), m(r'\dfrac{1}{3}\sqrt{3}'), m(r'5\sqrt[3]{\dfrac{2}{25}}'), m(r'\dfrac{2}{11}\sqrt{\dfrac{121}{7}}'),
])))
S.append(labs('ដំណោះស្រាយ បញ្ចូល', [
    ('ក.', p('មានចំនួនទាំងអស់នៅក្រោមរ៉ាឌីកាល់រួចហើយ។')),
    ('ខ.', dm(r'\dfrac{1}{3}\sqrt{3}=\sqrt{\dfrac{1}{3}}')),
    ('គ.', dm(r'5\sqrt[3]{\dfrac{2}{25}}=\sqrt[3]{10}')),
    ('ឃ.', dm(r'\dfrac{2}{11}\sqrt{\dfrac{121}{7}}=\sqrt{\dfrac{4}{7}}')),
], 'ចម្លើយ'))

# ---------------------------------------------------------------- 3.5 addition and subtraction
S.append(part(7, 'វិធីបូកនិងវិធីដករ៉ាឌីកាល់'))
S.append(key(K[7], 'ងាយយល់',
    p('ដូចការបូកដកឯកធា។ ' + m(r'3x+4x=7x') + ' ដូច ' + m(r'3\sqrt{2}+4\sqrt{2}=7\sqrt{2}') + '។')
    + p('បូកដកបានតែពេលរ៉ាឌីកង់ និងសន្ទស្សន៍ដូចគ្នា។')))
assert (2 + 5) == 7 and (5 - 3 + 1) == 3 and 8 == 4 * 2 and (3 + 2) == 5
assert 12 == 4 * 3 and 27 == 9 * 3 and (2 + 3 - 1) == 4
S.append(ex(K[7], 'ឧទាហរណ៍ទី២០',
    rvd(1, dm(r'2\sqrt{3}+5\sqrt{3}=7\sqrt{3}'))
    + rvd(2, dm(r'5\sqrt{2}-3\sqrt{2}+\sqrt{2}=3\sqrt{2}'))
    + rvd(3, dm(r'3\sqrt{2}+\sqrt{8}=5\sqrt{2}'))
    + rvd(4, dm(r'\sqrt{12}+\sqrt{27}-\sqrt{3}=4\sqrt{3}'))))
S.append(ex(K[7], 'ប្រវែងដូចគ្នា ទើបបូកបាន', fig(like_radicals())))
S.append(key(K[7], 'រ៉ាឌីកង់ខុសគ្នា',
    p(m(r'\sqrt{3}+\sqrt{7}') + ' មិនអាចបូកបានទេ។')
    + p(m(r'3\sqrt{2}+4\sqrt{3}') + ' មិនស្មើ ' + m(r'7\sqrt{5}') + ' ទេ។')))
S.append(key(K[7], 'វិធីបូក និងដក',
    p('បំប្លែងរ៉ាឌីកង់ឱ្យដូចគ្នា បើសន្ទស្សន៍ដូចគ្នា។ បន្ទាប់មកបូក-ដកមេគុណ ហើយរ៉ាឌីកាល់ទុកដដែល។')))
assert 3 + 5 * 2 - 3 * 3 == 4
assert 3 * 3 + 1 == 10 and -2 + 5 == 3
assert 3 * 2 + 6 * 3 == 24
assert 6 * 2 - 2 * 3 == 6
assert 2 + 4 - 3 == 3 and 14 - 11 == 3
S.append(ex(K[7], 'ឧទាហរណ៍ទី២១  A , B',
    rvd(1, dm(r'\begin{aligned}A&=3\sqrt{11}+5\sqrt{4\times 11}-3\sqrt{9\times 11}\\&=3\sqrt{11}+10\sqrt{11}-9\sqrt{11}=4\sqrt{11}\end{aligned}'))
    + rvd(2, dm(r'\begin{aligned}B&=3\sqrt{18}-\sqrt{12}+\sqrt{75}+\sqrt{2}\\&=3\sqrt{9\times 2}-\sqrt{4\times 3}+\sqrt{25\times 3}+\sqrt{2}\\&=9\sqrt{2}-2\sqrt{3}+5\sqrt{3}+\sqrt{2}=10\sqrt{2}+3\sqrt{3}\end{aligned}'))))
S.append(ex(K[7], 'ឧទាហរណ៍ទី២១  C , D',
    rvd(1, dm(r'\begin{aligned}C&=3\sqrt[3]{24}+6\sqrt[3]{81}\\&=3\sqrt[3]{8\times 3}+6\sqrt[3]{27\times 3}\\&=6\sqrt[3]{3}+18\sqrt[3]{3}=24\sqrt[3]{3}\end{aligned}'))
    + rvd(2, dm(r'\begin{aligned}D&=6\sqrt[3]{8x^2}-2\sqrt[3]{27x^2}\\&=12\sqrt[3]{x^2}-6\sqrt[3]{x^2}=6\sqrt[3]{x^2}\end{aligned}'))))
S.append(ex(K[7], 'ឧទាហរណ៍ទី២១  E , F',
    rvd(1, dm(r'\begin{aligned}E&=\sqrt{20}+\sqrt{80}-\sqrt{45}\\&=\sqrt{4\times 5}+\sqrt{16\times 5}-\sqrt{9\times 5}\\&=2\sqrt{5}+4\sqrt{5}-3\sqrt{5}=3\sqrt{5}\end{aligned}'))
    + rvd(2, dm(r'\begin{aligned}F&=14\sqrt{3}+6\sqrt{2}-11\sqrt{3}\\&=(14-11)\sqrt{3}+6\sqrt{2}=3\sqrt{3}+6\sqrt{2}\end{aligned}'))
    + rvd(3, p('បើមានរ៉ាឌីកង់ណាដែលខុសគេ យើងគ្រាន់តែទុកវានៅដដែល (ដូចករណី B និង F)។'))))
S.append(ex(K[7], 'ឧទាហរណ៍ទី២២  A , B',
    p('សម្រួលកន្សោមដែលមានអថេរ (ដោយសន្មតថាអថេរទាំងអស់វិជ្ជមាន)')
    + rvd(1, dm(r'\begin{aligned}A&=\sqrt{128y}-\sqrt{2y}=\sqrt{64\times 2y}-\sqrt{2y}\\&=8\sqrt{2y}-\sqrt{2y}=7\sqrt{2y}\end{aligned}'))
    + rvd(2, dm(r'\begin{aligned}B&=5\sqrt{18x}+2\sqrt{8x}=5\sqrt{9\times 2x}+2\sqrt{4\times 2x}\\&=15\sqrt{2x}+4\sqrt{2x}=19\sqrt{2x}\end{aligned}'))))
S.append(ex(K[7], 'ឧទាហរណ៍ទី២២  C , D',
    rvd(1, dm(r'\begin{aligned}C&=\sqrt{8n+8}+\sqrt{2n+2}=\sqrt{4(2n+2)}+\sqrt{2n+2}\\&=2\sqrt{2n+2}+\sqrt{2n+2}=3\sqrt{2n+2}\end{aligned}'))
    + rvd(2, dm(r'\begin{aligned}D&=\sqrt{200k^2}-\sqrt{98k^2}=\sqrt{100\times 2k^2}-\sqrt{49\times 2k^2}\\&=10k\sqrt{2}-7k\sqrt{2}=3k\sqrt{2}\end{aligned}'))))
S.append(ex(K[7], 'ឧទាហរណ៍ទី២២  E , F',
    rvd(1, dm(r'\begin{aligned}E&=\sqrt{8x^2}+\sqrt{2x^2}=\sqrt{4\times 2x^2}+\sqrt{2x^2}\\&=2x\sqrt{2}+x\sqrt{2}=3x\sqrt{2}\end{aligned}'))
    + rvd(2, dm(r'\begin{aligned}F&=2\sqrt{45x^3}-\sqrt{20x^3}=2\sqrt{9\times 5x^3}-\sqrt{4\times 5x^3}\\&=6x\sqrt{5x}-2x\sqrt{5x}=4x\sqrt{5x}\end{aligned}'))
    + rvd(3, p('ទោះមានអក្សរក៏ដោយ លក្ខណៈនៃការបូកដកនៅតែរក្សាដដែល។'))))
S.append(prac_grid(K[7], 'សម្រួល', [m(r'5\sqrt{50}-8\sqrt{32}'), m(r'\sqrt{48x}-\sqrt{27x}'), m(r'\sqrt{5P}+3\sqrt{45P^3}\;(P>0)'),
                                         m(r'\sqrt{12x+12}+\sqrt{27x+27}'), m(r'\sqrt{72a}-3\sqrt{98a}')], 2))
S.append(sol_grid('ចម្លើយ', 'ដំណោះស្រាយ សម្រួល', [
    ('ក.', m(r'5(5\sqrt{2})-8(4\sqrt{2})=-7\sqrt{2}')),
    ('ខ.', m(r'4\sqrt{3x}-3\sqrt{3x}=\sqrt{3x}')),
    ('គ.', m(r'\sqrt{5P}+9P\sqrt{5P}=(1+9P)\sqrt{5P}')),
    ('ឃ.', m(r'2\sqrt{3(x+1)}+3\sqrt{3(x+1)}=5\sqrt{3(x+1)}')),
    ('ង.', m(r'6\sqrt{2a}-21\sqrt{2a}=-15\sqrt{2a}')),
], 1))

# ---------------------------------------------------------------- 3.6 rationalise
S.append(part(8, 'វិធីបំបាត់រ៉ាឌីកាល់ពីភាគបែង'))
S.append(key(K[8], 'ហេតុអ្វីត្រូវបំបាត់',
    p('ជាទូទៅគេមិនទុករ៉ាឌីកាល់នៅភាគបែងទេ។ គុណទាំងភាគយកនិងភាគបែងនឹងកន្សោមដែលធ្វើឱ្យភាគបែងលែងមានរ៉ាឌីកាល់។')))
S.append(ex(K[8], 'មួយតួ', fig(rationalise_steps())
    + dm(r'\dfrac{a}{\sqrt{b}}=\dfrac{a\sqrt{b}}{b}\quad (b>0)')
    + dm(r'\dfrac{a}{\sqrt[3]{b}}=\dfrac{a\sqrt[3]{b^2}}{b}')))
assert True
S.append(ex(K[8], 'ឧទាហរណ៍ទី២៣  ក–ខ',
    rvd(1, dm(r'\dfrac{3}{\sqrt{2}}=\dfrac{3\sqrt{2}}{2}'))
    + rvd(2, dm(r'\dfrac{5}{2\sqrt{3}}=\dfrac{5\sqrt{3}}{6}'))))
S.append(ex(K[8], 'ឧទាហរណ៍ទី២៣  គ–ង',
    rvd(1, dm(r'\dfrac{2}{\sqrt[3]{5}}=\dfrac{2\sqrt[3]{25}}{5}'))
    + rvd(2, dm(r'\dfrac{7}{\sqrt[3]{4}}=\dfrac{7\sqrt[3]{2}}{2}'))
    + rvd(3, dm(r'\dfrac{\sqrt[3]{3}}{\sqrt[3]{4}}=\dfrac{\sqrt[3]{6}}{2}'))))
S.append(prac(K[8], 'បំបាត់មួយតួ', ul([m(r'\dfrac{7}{\sqrt{5}}'), m(r'\dfrac{2}{3\sqrt{7}}'), m(r'\dfrac{4}{\sqrt[3]{2}}')])))
S.append(labs('ដំណោះស្រាយ បំបាត់មួយតួ', [
    ('ក.', dm(r'\dfrac{7\sqrt{5}}{5}')),
    ('ខ.', dm(r'\dfrac{2\sqrt{7}}{21}')),
    ('គ.', dm(r'2\sqrt[3]{4}')),
], 'ចម្លើយ'))
S.append(key(K[8], 'ភាគបែងពីរតួ',
    p('ឫសការេ៖ គុណនឹង ' + hl('កន្សោមឆ្លាស់') + ' ដើម្បីប្រើ ' + m('(a-b)(a+b)=a^2-b^2') + '។')
    + p('ឫសគូប៖ គុណនឹង ' + hl('កន្សោមបំពេញ') + ' ដើម្បីប្រើ ' + m('a^3-b^3') + ' ឬ ' + m('a^3+b^3') + '។')))
assert 7 - 4 == 3 and 5 - 2 == 3
assert abs((math.sqrt(3) + math.sqrt(2)) ** 2 - (5 + 2 * math.sqrt(6))) < 1e-9
# exact: (√3+√2)^2 = 3+2+2√6 = 5+2√6
assert 3 + 2 == 5
S.append(ex(K[8], 'ឧទាហរណ៍ទី២៤',
    rvd(1, dm(r'\dfrac{2}{\sqrt{7}-2}=\dfrac{2(\sqrt{7}+2)}{3}'))
    + rvd(2, dm(r'\dfrac{\sqrt{2}}{\sqrt{5}+\sqrt{2}}=\dfrac{\sqrt{10}-2}{3}'))))
S.append(key(K[8], 'កុំលើកការេភាគបែង',
    p(m(r'(\sqrt{a}+\sqrt{b})^2=a+2\sqrt{ab}+b') + ' នៅតែមានរ៉ាឌីកាល់។')
    + p('ត្រូវគុណនឹងកន្សោមឆ្លាស់ ' + m(r'(\sqrt{a}-\sqrt{b})') + '។')))
assert 3 - 2 == 1 and 3 + 2 == 5  # (√3+√2)^2 = 3 + 2√6 + 2 = 5 + 2√6
S.append(ex(K[8], 'ឧទាហរណ៍ទី២៥',
    p(m(r'A=\dfrac{\sqrt{3}+\sqrt{2}}{\sqrt{3}-\sqrt{2}}'))
    + rvd(1, dm(r'A=\dfrac{(\sqrt{3}+\sqrt{2})^2}{3-2}'))
    + rvd(2, dm(r'A=5+2\sqrt{6}'))))
assert 20 - 18 == 2 and 16 / 2 == 8 and 48 / 2 == 24
S.append(ex(K[8], 'ឧទាហរណ៍ទី២៦',
    p(m(r'B=\dfrac{8\sqrt{2}}{\sqrt{20}-\sqrt{18}}'))
    + rvd(1, p('សម្រួលសិន ' + m(r'\sqrt{20}=2\sqrt{5}') + ' , ' + m(r'\sqrt{18}=3\sqrt{2}') + '។'))
    + rvd(2, dm(r'B=8\sqrt{10}+24'))))
assert 2 - 1 == 1 and 5 - 2 == 3
S.append(ex(K[8], 'ឧទាហរណ៍ទី២៧',
    rvd(1, dm(r'\dfrac{1}{\sqrt[3]{2}-1}=\sqrt[3]{4}+\sqrt[3]{2}+1'))
    + rvd(2, dm(r'\dfrac{3}{\sqrt[3]{5}-\sqrt[3]{2}}=\sqrt[3]{25}+\sqrt[3]{10}+\sqrt[3]{4}'))))
S.append(prac_grid(K[8], 'សម្រួល', [m(r'\dfrac{1}{\sqrt{5}+\sqrt{2}}'), m(r'\dfrac{3\sqrt{2}+2\sqrt{3}}{\sqrt{12}-\sqrt{18}}'),
                                     m(r'\dfrac{3}{\sqrt[3]{5}-\sqrt[3]{4}}'), m(r'\dfrac{\sqrt[3]{3}}{\sqrt[3]{4}+\sqrt[3]{2}}')], 2))
S.append(sol_grid('ចម្លើយ', 'ដំណោះស្រាយ សម្រួលភាគបែង', [
    ('ក.', m(r'\dfrac{\sqrt{5}-\sqrt{2}}{3}')),
    ('ខ.', m(r'-5-2\sqrt{6}')),
    ('គ.', m(r'3\sqrt[3]{25}+3\sqrt[3]{20}+6\sqrt[3]{2}')),
    ('ឃ.', m(r'\dfrac{2\sqrt[3]{6}-2\sqrt[3]{3}+\sqrt[3]{12}}{6}')),
], 2))

assert abs(_m.sqrt(2) * _m.sqrt(8) - 4) < 1e-9 and abs(_m.sqrt(9 + 16) - (_m.sqrt(9) + _m.sqrt(16))) > 1
assert abs(3 * _m.sqrt(2) + 4 * _m.sqrt(3) - 7 * _m.sqrt(5)) > 0.1 and abs(_m.sqrt(12) - 2 * _m.sqrt(3)) < 1e-9 and abs(5 / _m.sqrt(5) - _m.sqrt(5)) < 1e-9
S.append(ex('ពិនិត្យយល់', 'ពិត ឬ មិនពិត? (ច្បាប់រ៉ាឌីកាល់)', p('សាកល្បងបំបែកច្បាប់ ដោយគណនាតម្លៃប្រហែលដើម្បីពិនិត្យ។') + tf_rows([
    (m(r'\sqrt{2}\times\sqrt{8}=4'), True, m(r'=\sqrt{16}')),
    (m(r'\sqrt{9+16}=\sqrt{9}+\sqrt{16}'), False, m(r'5\neq 7')),
    (m(r'3\sqrt{2}+4\sqrt{2}=7\sqrt{2}'), True, 'រ៉ាឌីកង់ដូចគ្នា'),
    (m(r'3\sqrt{2}+4\sqrt{3}=7\sqrt{5}'), False, 'រ៉ាឌីកង់ខុសគ្នា បូកមិនបាន'),
    (m(r'\sqrt{12}=2\sqrt{3}'), True, m(r'=\sqrt{4\times 3}')),
    (m(r'\sqrt{x^2}=x') + ' ចំពោះគ្រប់ ' + m('x'), False, m(r'\sqrt{x^2}=|x|')),
])))

# ---------------------------------------------------------------- 9. exercises (difficulty one, every item; answers checked above the slides)
S.append(part(9, 'លំហាត់'))
ex1 = [
    (r'\sqrt{9}', '3', 3 ** 2 == 9),
    (r'\sqrt{16}', '4', 4 ** 2 == 16),
    (r'\sqrt{36}', '6', 6 ** 2 == 36),
    (r'-\sqrt{64}', '-8', 8 ** 2 == 64),
    (r'-\sqrt{100}', '-10', 10 ** 2 == 100),
    (r'\sqrt{121}', '11', 11 ** 2 == 121),
    (r'-\sqrt{144}', '-12', 12 ** 2 == 144),
    (r'\sqrt{625}', '25', 25 ** 2 == 625),
    (r'\sqrt[3]{8}', '2', 2 ** 3 == 8),
    (r'\sqrt[3]{-8}', '-2', (-2) ** 3 == -8),
    (r'-\sqrt[3]{27}', '-3', 3 ** 3 == 27),
    (r'-\sqrt[3]{64}', '-4', 4 ** 3 == 64),
    (r'\sqrt[3]{125}', '5', 5 ** 3 == 125),
    (r'\sqrt[3]{216}', '6', 6 ** 3 == 216),
]
assert all(ok for _, _, ok in ex1)
assert not perfect_power(100, 3) and 4 ** 3 < 100 < 5 ** 3
LB = 'កខគឃងចឆជឈញដឋឌឍណ'
S.append(prac_grid('លំហាត់ទី១', 'ចូរគណនា', [m(t) for t, _, _ in ex1] + [m(r'\sqrt[3]{100}')], 5))
S.append(sol_grid('ចម្លើយ', 'ដំណោះស្រាយ លំហាត់ទី១', [(LB[i] + '.', m(tex + '=' + ans)) for i, (tex, ans, _) in enumerate(ex1)]
         + [('ណ.', m(r'\sqrt[3]{100}') + ' ជាចំនួនអសនិទាន ព្រោះ ' + m('4^3=64<100<125=5^3') + '។')], 5))

ex2 = [
    (r'\sqrt{\dfrac{9}{16}}', r'\dfrac{3}{4}', Fraction(3, 4) ** 2 == Fraction(9, 16)),
    (r'\sqrt{\dfrac{49}{9}}', r'\dfrac{7}{3}', Fraction(7, 3) ** 2 == Fraction(49, 9)),
    (r'-\sqrt{\dfrac{81}{4}}', r'-\dfrac{9}{2}', Fraction(9, 2) ** 2 == Fraction(81, 4)),
    (r'\sqrt{\dfrac{169}{49}}', r'\dfrac{13}{7}', Fraction(13, 7) ** 2 == Fraction(169, 49)),
    (r'\sqrt{\dfrac{196}{25}}', r'\dfrac{14}{5}', Fraction(14, 5) ** 2 == Fraction(196, 25)),
    (r'-\sqrt{\dfrac{400}{225}}', r'-\dfrac{4}{3}', Fraction(20, 15) ** 2 == Fraction(400, 225) and Fraction(20, 15) == Fraction(4, 3)),
    (r'\sqrt[3]{\dfrac{1}{8}}', r'\dfrac{1}{2}', Fraction(1, 2) ** 3 == Fraction(1, 8)),
    (r'\sqrt[3]{\dfrac{8}{27}}', r'\dfrac{2}{3}', Fraction(2, 3) ** 3 == Fraction(8, 27)),
    (r'\sqrt[3]{\dfrac{64}{125}}', r'\dfrac{4}{5}', Fraction(4, 5) ** 3 == Fraction(64, 125)),
    (r'\sqrt[3]{\dfrac{512}{343}}', r'\dfrac{8}{7}', Fraction(8, 7) ** 3 == Fraction(512, 343)),
    (r'\sqrt[3]{-\dfrac{216}{1000}}', r'-\dfrac{3}{5}', Fraction(-3, 5) ** 3 == Fraction(-216, 1000)),
]
assert all(ok for _, _, ok in ex2)
S.append(prac_grid('លំហាត់ទី២', 'ចូរគណនា', [m(t) for t, _, _ in ex2], 4))
S.append(sol_grid('ចម្លើយ', 'ដំណោះស្រាយ លំហាត់ទី២', [(LB[i] + '.', m(tex + '=' + ans)) for i, (tex, ans, _) in enumerate(ex2)], 4))

assert 4 ** 3 == 64 and 6 ** 3 * 6 == 36 ** 2 and 8 ** 3 == 512 and 16 ** 3 == 64 ** 2 and 9 ** 3 == 27 ** 2
S.append(prac_grid('លំហាត់ទី៣', 'ចូរសម្រួលរ៉ាឌីកាល់', [
    m(r'\sqrt{16^3}'), m(r'-\sqrt[3]{36^2}'), m(r'\sqrt{64^3}'), m(r'(\sqrt[3]{-8})^3'),
    m(r'\sqrt[3]{-27^3}'), m(r'\sqrt[3]{1^5}'), m(r'\sqrt[3]{8^2}'), m(r'\sqrt[3]{64^2}'), m(r'\sqrt[3]{(-27)^2}'),
], 3))
S.append(sol_grid('ចម្លើយ', 'ដំណោះស្រាយ លំហាត់ទី៣', [
    ('ក.', m(r'\sqrt{16^3}=64')), ('ខ.', m(r'-\sqrt[3]{36^2}=-6\sqrt[3]{6}')), ('គ.', m(r'\sqrt{64^3}=512')),
    ('ឃ.', m(r'(\sqrt[3]{-8})^3=-8')), ('ង.', m(r'\sqrt[3]{-27^3}=-27')), ('ច.', m(r'\sqrt[3]{1^5}=1')),
    ('ឆ.', m(r'\sqrt[3]{8^2}=4')), ('ជ.', m(r'\sqrt[3]{64^2}=16')), ('ឈ.', m(r'\sqrt[3]{(-27)^2}=9')),
], 3))

# ---------------------------------------------------------------- 10. PISA
S.append(part(10, 'លំហាត់វាយតម្លៃសមត្ថភាព PISA'))
assert 3 ** 2 == 9 and (3 / Fraction('0.5')) ** 2 == 36
S.append(prac('ផ្សារទិញការ៉ូ', 'ផ្ទះបាយ 9 m²',
    p('គ្រួសារមួយចង់ក្រាលការ៉ូជារាងការ៉េក្នុងផ្ទះបាយ ដែលមានផ្ទៃក្រឡា ' + m(r'9\text{ m}^2') + '។')
    + p('សំណួរទី១ តើប្រវែងជ្រុងផ្ទះបាយស្មើប៉ុន្មានម៉ែត្រ?')
    + p('សំណួរទី២ បើការ៉ូមួយសន្លឹកមានជ្រុង ' + m(r'0.5\text{ m}') + ' តើត្រូវការការ៉ូប៉ុន្មានសន្លឹក?')
    + ul(['ក. 18 សន្លឹក', 'ខ. 36 សន្លឹក', 'គ. 12 សន្លឹក', 'ឃ. 81 សន្លឹក'])
    + p('សំណួរទី៣ ពន្យល់ថាតើការប្រើប្រាស់ "ឫសការេ" ជួយអ្នកក្នុងការដោះស្រាយបញ្ហានេះយ៉ាងដូចម្តេច? ចូរលើកហេតុផលបញ្ជាក់។')))
S.append(labs('ដំណោះស្រាយ ផ្សារទិញការ៉ូ', [
    ('១.', dm(r'x=\sqrt{9}=3')),
    ('២.', p('ខ. 36 សន្លឹក ព្រោះជ្រុងមួយមាន ' + m(r'3\div 0.5=6') + ' សន្លឹក ហើយ ' + m('6\\times 6=36') + '។')),
    ('៣.', p('ការប្រើប្រាស់ឫសការេជួយយើងឱ្យទាញរកប្រវែងជ្រុងពីផ្ទៃក្រឡាសរុប ដែលមានប្រយោជន៍ក្នុងការប៉ាន់ស្មានទំហំផ្ទៃបាត ឬរៀបចំផែនការទិញសម្ភារៈក្នុងជីវភាពប្រចាំថ្ងៃ។')),
], 'ចម្លើយ'))

assert not perfect_power(15, 2)
S.append(prac('សួនច្បារ', 'ដី 15 m²',
    p('សាលាមានដីចាក់បំពេញបានត្រឹម ' + m(r'15\text{ m}^2') + '។')
    + p('សំណួរទី១ ប្រវែងជ្រុងជាតម្លៃពិតប្រាកដ?')
    + p('សំណួរទី២ ប្រវែងនោះជាចំនួនសនិទាន ឬអសនិទាន?')
    + ul(['ក. ចំនួនសនិទាន ព្រោះវាអាចសរសេរជាប្រភាគបាន។',
          'ខ. ចំនួនអសនិទាន ព្រោះ 15 មិនមែនជាការេប្រាកដ។',
          'គ. ចំនួនគត់ ព្រោះវាជារង្វាស់ប្រវែង។',
          'ឃ. គ្មានចម្លើយណាត្រឹមត្រូវទេ។'])
    + p('សំណួរទី៣ ហេតុអ្វីបានជាជាងសង់សួនច្បារ ត្រូវប៉ាន់ស្មានប្រវែងនេះជាទសភាគ ដើម្បីវាស់ក្នុងជាក់ស្តែង?')))
S.append(labs('ដំណោះស្រាយ សួនច្បារ', [
    ('១.', dm(r'x=\sqrt{15}')),
    ('២.', p('ខ. ចំនួនអសនិទាន ព្រោះ 15 មិនមែនជាការេប្រាកដ។')),
    ('៣.', p('ក្នុងការវាស់ជាក់ស្តែង គេមិនអាចវាស់ប្រវែង ' + m(r'\sqrt{15}') + ' ដោយតម្លៃពិតប្រាកដលើម៉ែត្រវាស់បានទេ។ ដូចនេះត្រូវប៉ាន់ស្មានជាទសភាគ ' + m(r'\sqrt{15}\approx 3.87\text{ m}') + ' ដើម្បីកំណត់ប្រវែងសង់ឱ្យបានជិតត្រឹមត្រូវ។')),
], 'ចម្លើយ'))

assert 3.14 < math.pi < 3.15
S.append(prac('កង់រទេះ', 'អង្កត់ផ្ចិត 1 m',
    p('កង់មានអង្កត់ផ្ចិត ' + m(r'1\text{ m}') + '។ បន្ទះដែករុំព័ទ្ធជុំវិញកង់។')
    + p('សំណួរទី១ ប្រវែងបន្ទះដែកជាតម្លៃពិតប្រាកដ?')
    + p('សំណួរទី២ ប្រវែងនោះជាចំនួនសនិទាន ឬអសនិទាន?')
    + ul(['ក. ចំនួនសនិទាន ព្រោះអង្កត់ផ្ចិតជាចំនួនគត់។',
          'ខ. ចំនួនសនិទាន ព្រោះវាមានប្រវែងច្បាស់លាស់។',
          'គ. ចំនួនអសនិទាន ព្រោះវាទាក់ទងនឹងចំនួន ' + m(r'\pi') + '។',
          'ឃ. គ្មានចម្លើយណាត្រឹមត្រូវទេ។'])
    + p('សំណួរទី៣ បើជាងឈើត្រូវកាត់ដែកពីហាង តើគាត់គួរទិញដែកប្រវែងប៉ុន្មាន ដើម្បីឱ្យល្មម និងមានសុវត្ថិភាពក្នុងការរុំកង់នេះ (ប៉ាន់ស្មានត្រឹម ២ ខ្ទង់ទសភាគ)? ពន្យល់ពីហេតុផល។')))
S.append(labs('ដំណោះស្រាយ កង់រទេះ', [
    ('១.', dm(r'\pi \times 1 = \pi')),
    ('២.', p('គ. ចំនួនអសនិទាន ព្រោះវាទាក់ទងនឹង ' + m(r'\pi') + '។')),
    ('៣.', p('ប៉ាន់ស្មានពីរខ្ទង់៖ ' + m(r'\pi \approx 3.14') + '។ ដើម្បីឱ្យល្មម និងមានសល់បន្តិច ទិញ ' + m(r'3.15\text{ m}') + '។')),
], 'ចម្លើយ'))

assert 1 ** 2 + 2 ** 2 == 5 and not perfect_power(5, 2) and Fraction('2.23') ** 2 != 5
S.append(prac('ទ្វារ', 'ទ្វារ 1 m × 2 m',
    p('ទ្វារមានទំហំ ' + m(r'1\text{ m}\times 2\text{ m}') + '។ អង្កត់ទ្រូងត្រូវបានតាងដោយ ' + m('d') + '។')
    + p('សំណួរទី១ ប្រវែងអង្កត់ទ្រូងជាតម្លៃពិតប្រាកដ?')
    + p('សំណួរទី២ អះអាងណាពិត?')
    + ul(['១. អង្កត់ទ្រូងសរសេរជាប្រភាគនៃចំនួនគត់បាន។',
          '២. បើវាស់បាន 2.23 m នោះជាតម្លៃពិតប្រាកដ។',
          '៣. តម្លៃពិតប្រាកដជាចំនួនអសនិទាន។'])
    + p('សំណួរទី៣ ហេតុអ្វីបានជាជាងឈើមិនអាចវាស់ប្រវែងអង្កត់ទ្រូងនេះឱ្យបានច្បាស់លាស់ ១០០% ជាមួយម៉ែត្រវាស់ធម្មតា? ពន្យល់។')))
S.append(labs('ដំណោះស្រាយ ទ្វារ', [
    ('១.', dm(r'd=\sqrt{1^2+2^2}=\sqrt{5}')),
    ('២.', p('១ មិនពិត , ២ មិនពិត , ៣ ពិត។')),
    ('៣.', p('ម៉ែត្រវាស់មានគំនូសត្រឹមមិល្លីម៉ែត្រ ខណៈ ' + m(r'\sqrt{5}') + ' ជាចំនួនទសភាគមិនចេះចប់មិនខួប ដូច្នេះវាមិនអាចចង្អុលបង្ហាញចំចំណុចច្បាស់លាស់ ១០០% លើម៉ែត្របានទេ បានត្រឹមតែតម្លៃប្រហែលប៉ុណ្ណោះ។')),
], 'ចម្លើយ'))

assert 4 ** 2 == 16 and 20 == 4 * 5 and (2 * math.sqrt(5)) ** 2 == 20 or abs((2 * math.sqrt(5)) ** 2 - 20) < 1e-9
per = 8 * Fraction('2.236')
assert 17 < per < 18
S.append(prac('របង', 'ដី 16 m² និង 20 m²',
    p('កសិករ ក មានដី ' + m(r'16\text{ m}^2') + ' កសិករ ខ មានដី ' + m(r'20\text{ m}^2') + '។')
    + p('សំណួរទី១ បំពេញតារាងដោយសរសេរតម្លៃពិតប្រាកដនៃប្រវែងជ្រុង និងបរិមាត្រ។')
    + big('<table class="tbl"><tr><th>ម្ចាស់ដី</th><th>ប្រវែងជ្រុង (m)</th><th>បរិមាត្រ (m)</th></tr><tr><td>កសិករ ក</td><td></td><td></td></tr><tr><td>កសិករ ខ</td><td></td><td></td></tr></table>', 26)
    + p('សំណួរទី២ ប្រវែងជ្រុងដីរបស់កសិករ ខ ជាចំនួនសនិទានដែរឬទេ?  បាទ/ចាស (Yes)  ឬ  ទេ (No)')
    + p('សំណួរទី៣ បើកសិករ ខ ត្រូវទិញលួសធ្វើរបងដែលលក់គិតជាម៉ែត្រគត់ តើគាត់គួរទិញលួសយ៉ាងតិចប៉ុន្មានម៉ែត្រ ទើបអាចព័ទ្ធរបងបានជុំវិញដីរបស់គាត់? ពន្យល់ហេតុផលដោយប្រើការប៉ាន់ស្មាន ' + m(r'\sqrt{5}\approx 2.236') + '។')))
S.append(labs('ដំណោះស្រាយ របង', [
    ('ក.', dm(r'4\text{ m},\quad 16\text{ m}')),
    ('ខ.', dm(r'2\sqrt{5}\text{ m},\quad 8\sqrt{5}\text{ m}')),
    ('២.', p('ទេ។ 20 មិនមែនជាការេប្រាកដ។')),
    ('៣.', p(m(r'\sqrt{5}\approx 2.236') + ' ឲ្យបរិមាត្រប្រហែល ' + m('17.888') + ' m។ លួសគិតជាម៉ែត្រគត់ ត្រូវទិញយ៉ាងតិច 18 m។')),
], 'ចម្លើយ'))

# nested radical, as in the lesson after the PISA section
A, B = 7, 40
C = math.isqrt(A * A - B)
assert C * C == A * A - B == 9
assert (A + C) / 2 == 5 and (A - C) / 2 == 2
S.append(ex('បន្ថែម', 'ឫសជាន់គ្នា',
    p('ចូរសម្រួល ' + m(r'\sqrt{7+\sqrt{40}}') + '។')
    + rvd(1, dm(r'C=\sqrt{7^2-40}=\sqrt{9}=3'))
    + rvd(2, dm(r'\sqrt{7+\sqrt{40}}=\sqrt{5}+\sqrt{2}'))))

assert _m.isqrt(49) == 7 and round(-27 ** (1 / 3) if False else -3) == -3 and 48 == 16 * 3 and abs(2 * _m.sqrt(5) + _m.sqrt(45) - 5 * _m.sqrt(5)) < 1e-9 and abs(6 / _m.sqrt(3) - 2 * _m.sqrt(3)) < 1e-9
S.append(ex('សំបុត្រចេញ', 'ពិនិត្យយល់ចុងក្រោយ (Exit ticket)', p('សរសេរចម្លើយលើក្រដាសតូច ហើយប្រគល់ជូនគ្រូមុនចេញ។') + ''.join(
    f'<div style="display:grid;grid-template-columns:1.2fr 1fr;gap:1em;align-items:center;margin:.3em 0"><div><b>{i}.</b> {q}</div>{rvd(i, a)}</div>' for i, (q, a) in enumerate([
        ('គណនា ' + m(r'\sqrt{49}') + ' និង ' + m(r'\sqrt[3]{-27}'), m(r'7') + ' និង ' + m('-3')),
        ('បញ្ចេញ ' + m(r'\sqrt{48}'), m(r'\sqrt{16\times 3}=4\sqrt{3}')),
        ('សម្រួល ' + m(r'2\sqrt{5}+\sqrt{45}'), m(r'2\sqrt{5}+3\sqrt{5}=5\sqrt{5}')),
        ('បំបាត់រ៉ាឌីកាល់ពីភាគបែង ' + m(r'\dfrac{6}{\sqrt{3}}'), m(r'\dfrac{6\sqrt{3}}{3}=2\sqrt{3}')),
        (m(r'\sqrt{20}') + ' ជាចំនួនសនិទាន ឬអសនិទាន? ហេតុអ្វី?', 'អសនិទាន ព្រោះ ' + m('20') + ' មិនមែនជាការេប្រាកដ'),
    ], 1))))
S.append(key('សង្ខេប', 'សេចក្តីសង្ខេប ១', ul([
    'ចំនួនសនិទានសរសេរជាប្រភាគបាន។ ចំនួនអសនិទានមិនសរសេរជាប្រភាគបាន ដូចជា ' + m(r'\sqrt{2}') + ' និង ' + m(r'\pi') + '។',
    'បើ ' + m('a>0') + ' និង ' + m('x^2=a') + ' នោះ ' + m(r'x=\pm\sqrt{a}') + '។ បើ ' + m('x^3=a') + ' នោះ ' + m(r'x=\sqrt[3]{a}') + '។',
    m(r'\sqrt{a}\times\sqrt{b}=\sqrt{ab}') + ' និង ' + m(r'\dfrac{\sqrt{a}}{\sqrt{b}}=\sqrt{\dfrac{a}{b}}') + '។',
])))
S.append(key('សង្ខេប', 'សេចក្តីសង្ខេប ២', ul([
    m(r'\sqrt{x^2}=|x|') + ' និង ' + m(r'\sqrt[3]{x^3}=x') + '។ បញ្ចូល៖ ' + m(r'x\sqrt{y}=\sqrt{x^2 y}') + ' បើ ' + m('x\\ge 0') + '។',
    'បូកនិងដកបានលុះត្រាតែសន្ទស្សន៍ និងរ៉ាឌីកង់ដូចគ្នា។',
    'បំបាត់រ៉ាឌីកាល់ពីភាគបែង៖ មួយតួគុណនឹងរ៉ាឌីកាល់បំពេញ ពីរតួឫសការេគុណនឹងកន្សោមឆ្លាស់ ពីរតួឫសគូបគុណនឹងកន្សោមបំពេញ។',
])))
S.append({'k': 'title', 'html': '<p class="ts-kicker">មេរៀនទី ១</p><h1>ចប់មេរៀន</h1><p class="ts-sub">ចំនួនអសនិទាន</p><div class="th-you">សូមអរគុណ</div>'})

# ---------------------------------------------------------------- lay out, animate, write
out = []
for s in S:
    if s.get('k') == 'sol' and s['html'].count('<li class="lab">') >= 2:
        out.extend(split_solution(s, limit=220))
    else:
        out.append(s)
for s in out:
    s.setdefault('k', '')
out = rebuild(out)
out = [stepify(x) if x.get('k') in ('sol', 'ex', 'key', 'prac') and 'data-step' not in x['html'] else x for x in out]
out = animate_deck(out)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
js = ('// Hand-designed deck for Grade 9 Lesson 1: tools/lesson9_1/*.py — do not edit by hand.\n'
      + 'window.TEACH_SLIDES = window.TEACH_SLIDES || {};\n'
      + "window.TEACH_SLIDES['9-1'] = " + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ';\n')
open(OUT, 'w', encoding='utf8').write(js)
print(len(out), 'slides ->', os.path.abspath(OUT), len(js) // 1024, 'KB')
