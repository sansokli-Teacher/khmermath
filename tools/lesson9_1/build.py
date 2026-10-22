"""Grade 9 Lesson 1 «ចំនួនអសនិទាន» -> public/js/slides/g9/lesson1.js      python3 tools/lesson9_1/build.py
This deck FOLLOWS THE MoEYS TEXTBOOK lesson 1 (12 pages): the same sections, examples, general rules and practice items, in the book's wording.
Teaching-flow additions (marked in docs/LESSON_G9_1_REPORT.md): lesson map, the garden question, ដើមការេ / ដើមគូប, a summary and an exit ticket.
The long deck (30 exercises with solutions, PISA tasks, extras) is archived as build_full.py -> lesson1_full.js (not loaded by the app).
Every answer is checked numerically below; pictures come from vis_book.py (typeset maths, no self-drawing lines)."""
import math, json, os, sys
from fractions import Fraction
HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, '..', 'lesson1'))
from lib import stepify, slide, part, key, ex, prac, m, dm, p, ul, ol, hl, fig, rvd, cols
from vis_book import *

OUT = os.path.join(HERE, '..', '..', 'public', 'js', 'slides', 'g9', 'lesson1.js')
K = ['', '១. ឫសការេ', '២. ឫសគូប', '៣.១ គុណ', '៣.២ ចែក', '៣.៣ បញ្ចេញ', '៣.៤ បញ្ចូល', '៣.៥ បូក និងដក', '៣.៦ ភាគបែង']
V = math.sqrt
C = lambda x: math.copysign(abs(x) ** (1 / 3), x)
LB = 'កខគឃងចឆជឈ'


def near(a, b, tol=1e-9):
    return abs(a - b) < tol * max(1, abs(b))


def lab_cell(lb, body):
    return f'<span style="color:#e03131;font-weight:700;margin-right:.45em">{lb}</span>{body}'


def ans(tex):
    return f'<span style="color:#2f9e44">{m(tex)}</span>'


def qa(kick, title, rows, cols_=2, intro='', labels=LB, k='prac'):
    """practice: the problem is always on screen, its answer appears on the next press of →. rows = [(problem tex, answer tex)]"""
    cells = ''
    for i, (q, a) in enumerate(rows, 1):
        cells += f'<div><div>{lab_cell(labels[i - 1] + ".", m(q))}</div>{rvd(i, ans(a))}</div>'
    body = (p(intro) if intro else '') + f'<div style="display:grid;grid-template-columns:repeat({cols_},1fr);gap:.4em 2.2em;margin-top:.3em">{cells}</div>'
    return slide(kick, title, body, k=k)


def worked(kick, title, rows, intro=''):
    """worked answers, one line per press of →.  rows = [(label, tex)]"""
    items = [lab_cell(lb + '.', m(t)) for lb, t in rows]
    return slide(kick, title, (p(intro) if intro else '') + ul(items), k='sol')


S = []

# ---------------------------------------------------------------- cover: the book's objectives
S.append({'k': 'title', 'c': 'cover', 'html':
    '<p class="ts-kicker">ថ្នាក់ទី ៩ · មេរៀនទី ១</p><h1>ចំនួនអសនិទាន</h1>'
    + '<div class="ts-obj"><h3>វត្ថុបំណង</h3><ol class="ts-bullets">'
    + '<li>រកឫសការេនៃមួយចំនួន។</li><li>រកឫសគូបនៃមួយចំនួន។</li><li>ធ្វើប្រមាណវិធីលើចំនួនអសនិទាន។</li></ol></div>'})


def _map_box(no, tex, name, col):
    return (f'<div style="border:4px solid {col};border-radius:18px;background:#fff;padding:.5em .6em .6em;text-align:center;position:relative;min-height:9.5em">'
            f'<span style="position:absolute;left:-.5em;top:-.6em;background:{col};color:#fff;border-radius:50%;width:1.7em;height:1.7em;line-height:1.7em;font-weight:800">{no}</span>'
            f'<div style="color:{col};font-size:1.35em;margin:.5em 0 .3em;min-height:2.6em;display:flex;align-items:center;justify-content:center">{m(tex)}</div>'
            f'<div style="font-weight:700;color:#264b66;font-size:.95em">{name}</div></div>')


_MAP = [('១', r'\sqrt{a}', 'ឫសការេ និងចំនួនអសនិទាន', '#1c7ed6'), ('២', r'\sqrt[3]{a}', 'ឫសគូប', '#2b8a87'),
        ('៣', r'\sqrt{a}\cdot\sqrt{b}=\sqrt{ab}', 'គុណ និងចែករ៉ាឌីកាល់', '#2f9e44'), ('៤', r'3\sqrt{2}=\sqrt{18}', 'បញ្ចេញ និងបញ្ចូល', '#f08c00'),
        ('៥', r'3\sqrt{2}+4\sqrt{2}=7\sqrt{2}', 'បូក និងដក', '#e8590c'), ('៦', r'\dfrac{1}{\sqrt{2}}=\dfrac{\sqrt{2}}{2}', 'បំបាត់រ៉ាឌីកាល់ពីភាគបែង', '#ae3ec9')]
assert near(3 * V(2), V(18)) and near(1 / V(2), V(2) / 2) and near(3 * V(2) + 4 * V(2), 7 * V(2))


def _map_row(items, arrow):
    out = ''
    for k, it in enumerate(items):
        out += _map_box(*it) + (f'<div style="align-self:center;font-size:1.8em;color:#868e96">{arrow}</div>' if k < 2 else '')
    return f'<div style="display:grid;grid-template-columns:1fr auto 1fr auto 1fr;gap:.4em;margin:.5em 0">{out}</div>'


S.append(ex('ផែនទីមេរៀន', 'ថ្ងៃនេះយើងនឹងដើរតាមជំហានទាំងប្រាំមួយនេះ',
    _map_row(_MAP[:3], '→') + '<div style="text-align:right;padding-right:3.5em;font-size:1.6em;color:#868e96">↓</div>' + _map_row([_MAP[5], _MAP[4], _MAP[3]], '←')))

# ================================================================ 1. ឫសការេ  (book p.1-3)
S.append(part(1, 'ឫសការេ និងចំនួនអសនិទាន'))
assert 3 - 5 == -2 and Fraction(5, 2) == Fraction('2.5')
S.append(slide('រំលឹក', 'រំលឹក', p('១. រក ' + m('x') + ' ដែល ' + m('x+5=3') + ' ។') + dm('x=3-5=-2')
    + p('២. រក ' + m('x') + ' ដែល ' + m('2x=5') + ' ។') + dm(r'x=\dfrac{5}{2}=2.5')
    + p('ចំនួន ' + m('-2') + ' , ' + m(r'\dfrac{5}{2}') + ' , ' + m('2.5') + ' ហៅថា' + hl('ចំនួនសនិទាន') + ' ។ មានករណីខ្លះចំនួនសនិទានពុំអាចបំពេញលក្ខខណ្ឌនៃសមីការបាន ។'), k='ex'))

assert 3 ** 2 == 9 and (-3) ** 2 == 9
S.append(ex(K[1], 'ឧទាហរណ៍ទី ១ ៖ រក ' + m('x') + ' ដែល ' + m('x^2=9'),
    p('ដោយ ' + m('3^2=9') + ' , ' + m('(-3)^2=9'))
    + p('ដូចនេះ ' + m('x=3') + ' , ' + m('x=-3') + ' ។')
    + p('ចំនួន ' + m('3') + ' និង ' + m('-3') + ' ជា' + hl('ឫសការេ') + 'នៃ ' + m('9') + ' ។')
    + p('ហេតុនេះការរកឫសការេនៃ ' + m('9') + ' គឺរក ' + m('x') + ' ដែល ' + m('x^2=9') + ' ។')))

assert (Fraction(5, 2)) ** 2 == Fraction(25, 4) == (Fraction(-5, 2)) ** 2
S.append(ex(K[1], 'ឧទាហរណ៍ទី ២ ៖ រក ' + m('x') + ' ដែល ' + m(r'x^2=\dfrac{25}{4}'),
    p('ដោយ ' + m(r'\left(\dfrac{5}{2}\right)^2=\dfrac{25}{4}') + ' , ' + m(r'\left(-\dfrac{5}{2}\right)^2=\dfrac{25}{4}'))
    + p('ដូចនេះ ' + m(r'x=\dfrac{5}{2}') + ' , ' + m(r'x=-\dfrac{5}{2}') + ' ។')
    + p('ចំនួន ' + m(r'\dfrac{5}{2}') + ' , ' + m(r'-\dfrac{5}{2}') + ' ជាឫសការេនៃ ' + m(r'\dfrac{25}{4}') + ' ។')
    + p('គេអាចថា ' + m(r'\dfrac{25}{4}') + ' មានឫសការេពីរផ្ទុយគ្នាគឺ ' + m(r'\dfrac{5}{2}') + ' និង ' + m(r'-\dfrac{5}{2}') + ' ។')))

S.append(ex(K[1], 'សួនច្បាររាងការេ',
    p('សួនច្បាររាងការេមួយមានក្រឡាផ្ទៃ ' + m(r'3\text{ m}^2') + ' ។ បើតាងប្រវែងជ្រុងដោយ ' + m('x') + ' នោះ ' + m('x^2=3') + ' ។ ' + hl('តើ ' + m('x') + ' ជាចំនួនអ្វី?'))
    + fig(garden())))

trial = [(Fraction(1), '1', r'1^2=1<3'), (Fraction(3, 2), r'\dfrac{3}{2}=1.5', r'\left(\dfrac{3}{2}\right)^2=\dfrac{9}{4}=2.25<3'),
         (Fraction(5, 3), r'\dfrac{5}{3}\approx 1.67', r'\left(\dfrac{5}{3}\right)^2=\dfrac{25}{9}\approx 2.78<3'), (Fraction(2), '2', r'2^2=4>3')]
assert [t[0] ** 2 < 3 for t in trial] == [True, True, True, False] and Fraction(9, 4) == Fraction('2.25') and 2.77 < 25 / 9 < 2.78
tr = ''.join(f'<div style="display:grid;grid-template-columns:.8fr 1.4fr;gap:1em;align-items:center;margin:.2em 0">{rvd(i, "<div>បើឱ្យ " + m("x=" + x) + "</div>")}{rvd(i, "<div>" + m(r) + "</div>")}</div>' for i, (_, x, r) in enumerate(trial, 1))
S.append(ex(K[1], 'ឧទាហរណ៍ទី ៣ ៖ រក ' + m('x') + ' ដែល ' + m('x^2=3'),
    tr + rvd(5, p(hl('យើងឃើញថាគ្មានចំនួនសនិទានណាដែលការេវាស្មើនឹង ' + m('3') + ' ទេ ។')))))
S.append(ex(K[1], 'ឧទាហរណ៍ទី ៣ (ត) ៖ ' + m(r'\sqrt{3}'),
    fig(squeeze_sqrt3()) + p('ក្នុងករណីនេះគេសន្មតតាង ' + m(r'\sqrt{3}') + ' ជាចំនួនមួយដែល ' + m(r'(\sqrt{3})^2=3') + ' ។')))
assert near(V(3) ** 2, 3) and 1.7320 < V(3) < 1.7321
S.append(key(K[1], 'ឫសការេនៃ ' + '3',
    p('មានន័យថាបើ ' + m('x^2=3') + ' ឫសការេនៃ ' + m('3') + ' គឺ ' + m(r'\sqrt{3}') + ' និង ' + m(r'-\sqrt{3}') + ' ។')
    + p(m(r'\sqrt{3}') + ' ជាឫសការេ' + hl('វិជ្ជមាន') + ' ហើយ ' + m(r'-\sqrt{3}') + ' ជាឫសការេ' + hl('អវិជ្ជមាន') + ' ។')
    + p('ចំនួន ' + m(r'\sqrt{3}') + ' ហៅថា' + hl('ចំនួនអសនិទាន') + ' ដែល ' + m(r'\sqrt{3}\approx 1.7320') + ' ។')))
S.append(ex(K[1], 'សញ្ញារ៉ាឌីកាល់',
    p('ចំពោះចំនួន ' + m(r'\sqrt{3}') + ' សញ្ញា ' + m(r'\sqrt{\ }') + ' ហៅថា' + hl('រ៉ាឌីកាល់') + 'មានសន្ទស្សន៍ស្មើនឹង ' + m('2') + ' ។')
    + fig(radical_parts())
    + p('តាមពិតត្រូវសរសេរ ' + m(r'\sqrt[2]{3}') + ' ដើម្បីសម្គាល់សន្ទស្សន៍នៃរ៉ាឌីកាល់ ហើយ ' + m('3') + ' ហៅថា' + hl('រ៉ាឌីកង់') + ' ។')))
S.append(ex(K[1], 'ឧទាហរណ៍ទី ៤ ៖ រក ' + m('x') + ' បើ ' + m('x^2=-3'),
    p('គេដឹងថាគ្មានតម្លៃ ' + m('x') + ' ណាដែលនាំឱ្យ ' + m('x^2') + ' ជាចំនួនអវិជ្ជមានទេ ។')
    + p('ដូចនេះចំនួនអវិជ្ជមាន' + hl('គ្មានឫសការេ') + 'ទេ ។')))
S.append(ex(K[1], 'ដើមការេ',
    cols(fig(plant('sq')),
         '<div style="font-size:1.12em">' + p('«ឫស» គឺជាឫសដើមឈើ និងជាឫសនៃចំនួនផងដែរ ។ ចំនួនលើផ្កា មានឫសនៅក្រោមដី ។')
         + rvd(1, p('<span style="color:#1c7ed6;font-weight:700">' + m('9') + '</span> មានឫសការេ' + hl('ពីរ') + ' ៖ <span style="color:#1c7ed6;font-weight:700">' + m('3') + ' និង ' + m('-3') + '</span> ព្រោះ ' + m('3^2=9') + ' និង ' + m('(-3)^2=9') + ' ។'))
         + rvd(2, p('<span style="color:#e8590c;font-weight:700">' + m('5') + '</span> មានឫសការេ' + hl('ពីរ') + ' ៖ <span style="color:#e8590c;font-weight:700">' + m(r'\sqrt{5}') + ' និង ' + m(r'-\sqrt{5}') + '</span> ។'))
         + rvd(3, p('<span style="color:#6c757d;font-weight:700">' + m('-4') + '</span> → ' + hl('គ្មាន') + ' ។ គ្មានចំនួនពិតណាដែលលើកជាការេបាន ' + m('-4') + ' ។'))
         + '</div>')))
S.append(key(K[1], 'ជាទូទៅ', p('បើ ' + m('a>0') + ' , ' + m('x^2=a') + ' គេបាន ' + m(r'x=\sqrt{a}') + ' និង ' + m(r'x=-\sqrt{a}') + ' ។')))
rows = [('x^2=16', r'x=\sqrt{16}=4,\ \ x=-\sqrt{16}=-4'), ('x^2=7', r'x=\sqrt{7},\ \ x=-\sqrt{7}'), (r'x^2=\dfrac{25}{4}', r'x=\dfrac{5}{2},\ \ x=-\dfrac{5}{2}'),
        ('x^2=-81', r'\text{គ្មានឫសការេ}'), ('x^2=1', r'x=1,\ \ x=-1'), ('x^2=0', r'x=0')]
assert 4 ** 2 == 16 and (-4) ** 2 == 16 and 5 ** 2 == 25 and Fraction(5, 2) ** 2 == Fraction(25, 4)
S.append(qa(K[1], 'លំហាត់គួរ ៖ រកឫសការេនៃសមីការខាងក្រោម', rows, 2))
assert near(0.2 ** 2, 0.04) and near(0.1 ** 2, 0.01) and Fraction(5, 6) ** 2 == Fraction(25, 36)
S.append(qa(K[1], 'ប្រតិបត្តិ ៖ រកឫសការេនៃចំនួន', [('0.04', r'\pm 0.2'), ('0.01', r'\pm 0.1'), ('5', r'\pm\sqrt{5}'), ('-1', r'\text{គ្មាន}'), (r'\dfrac{25}{36}', r'\pm\dfrac{5}{6}'), ('0.1', r'\pm\sqrt{0.1}')], 3))

# ================================================================ 2. ឫសគូប  (book p.3-4)
S.append(part(2, 'ឫសគូប'))
assert 4 ** 3 == 64 and (-4) ** 3 == -64 and 3 ** 3 == 27 and (-3) ** 3 == -27
S.append(ex(K[2], 'ឧទាហរណ៍ទី ១ ៖ រក ' + m('x') + ' ដែល ' + m('x^3=64'),
    p(m('4^3=64') + ' , ' + m('(-4)^3=-64') + ' ។ ដូចនេះ ' + m('x=4') + ' ជា' + hl('ឫសគូប') + 'នៃ ' + m('64') + ' ។')
    + p('គេថា ' + m('64') + ' មានឫសគូប' + hl('តែមួយគត់') + 'គឺ ' + m('x=4') + ' ។')
    + p('រកឫសគូបនៃ ' + m('64') + ' គឺរក ' + m('x') + ' ដែល ' + m('x^3=64') + ' ។')))
S.append(ex(K[2], 'ឧទាហរណ៍ទី ២ ៖ រក ' + m('x') + ' ដែល ' + m('x^3=-27'),
    p(m('3^3=27') + ' , ' + m('(-3)^3=-27') + ' ។ ដូចនេះ ' + m('x=-3') + ' ជាឫសគូបនៃ ' + m('-27') + ' ។')
    + p(m('-27') + ' មានឫសគូបតែមួយគត់គឺ ' + m('x=-3') + ' ។')
    + p('គេសង្កេតឃើញថាគ្រប់ចំនួនវិជ្ជមាន ឬអវិជ្ជមាន មានឫសគូបតែមួយគត់ ។ ឫសគូបនៃចំនួនវិជ្ជមានជាចំនួនវិជ្ជមាន ហើយឫសគូបនៃចំនួនអវិជ្ជមានជាចំនួនអវិជ្ជមាន ។')))
S.append(ex(K[2], 'ដើមគូប',
    cols(fig(plant('cu')),
         '<div style="font-size:1.12em">' + p('ដើមគូបមានឫសគូប ។ ចំនួនលើផ្កាលើកជាគូប ពីឫសនៅក្រោមដី ។ ចំនួននីមួយៗមាន' + hl('ឫសគូបតែមួយ') + ' ។')
         + rvd(1, p('<span style="color:#1c7ed6;font-weight:700">' + m('8') + '</span> → <span style="color:#1c7ed6;font-weight:700">' + m(r'\sqrt[3]{8}=2') + '</span> ព្រោះ ' + m('2^3=8') + ' ។'))
         + rvd(2, p('<span style="color:#e8590c;font-weight:700">' + m('17') + '</span> → <span style="color:#e8590c;font-weight:700">' + m(r'\sqrt[3]{17}') + '</span> ។ ជាចំនួន' + hl('អសនិទាន') + ' ។'))
         + rvd(3, p('<span style="color:#ae3ec9;font-weight:700">' + m('-27') + '</span> → <span style="color:#ae3ec9;font-weight:700">' + m(r'\sqrt[3]{-27}=-3') + '</span> ព្រោះ ' + m('(-3)^3=-27') + ' ។'))
         + '</div>')))
assert Fraction('2.5') ** 3 == Fraction('15.625') and Fraction('2.6') ** 3 == Fraction('17.576') and 2 ** 3 == 8
S.append(ex(K[2], 'ឧទាហរណ៍ទី ៣ ៖ រក ' + m('x') + ' ដែល ' + m('x^3=17'),
    p(m('2^3=8') + ' , ' + m('(2.5)^3=15.625') + ' , ' + m('(2.6)^3=17.576') + ' ។') + fig(squeeze_cbrt17())
    + p('យើងឃើញថាគ្មានចំនួនសនិទានណាដែលឫសគូបវាស្មើនឹង ' + m('17') + ' ទេ ។')))
S.append(key(K[2], 'ឫសគូបនៃ ' + '17',
    p('ក្នុងករណីនេះ គេសន្មតតាង ' + m(r'\sqrt[3]{17}') + ' ជាឫសគូបនៃ ' + m('17') + ' ។ ' + m(r'\sqrt[3]{17}') + ' ជាចំនួន' + hl('អសនិទាន') + ' ។')
    + p('ចំពោះ ' + m(r'\sqrt[3]{17}') + ' សញ្ញា ' + m(r'\sqrt[3]{\ }') + ' ជារ៉ាឌីកាល់ដែលមានសន្ទស្សន៍ស្មើនឹង ' + m('3') + ' ហើយ ' + m('17') + ' ជារ៉ាឌីកង់ ។')))
assert near(C(17) ** 3, 17) and 2.5 < C(17) < 2.6
S.append(ex(K[2], 'ឧទាហរណ៍ទី ៤ ៖ រក ' + m('x') + ' ដែល ' + m('x^3=-17'),
    p('ឫសគូបនៃចំនួនអវិជ្ជមានជាចំនួនអវិជ្ជមាន ។')
    + p('ហេតុនេះឫសគូបនៃ ' + m('-17') + ' គឺ ' + m(r'-\sqrt[3]{17}') + ' ។')))
S.append(key(K[2], 'ជាទូទៅ', p('បើ ' + m('x^3=a') + ' គេបាន ' + m(r'x=\sqrt[3]{a}') + ' ។ ' + m('a') + ' អាចវិជ្ជមាន ឬអវិជ្ជមាន ។')))
rows = [('x^3=-64', r'x=\sqrt[3]{-64}=-4'), ('x^3=-1', r'x=-1'), ('x^3=1', r'x=1'), ('x^3=-8', r'x=-2'), ('x^3=4', r'x=\sqrt[3]{4}'), ('x^3=0', r'x=0'),
        (r'x^3=\dfrac{1}{8}', r'x=\dfrac{1}{2}'), (r'x^3=\dfrac{27}{125}', r'x=\dfrac{3}{5}'), (r'x^3=-\dfrac{1}{1000}', r'x=-\dfrac{1}{10}')]
assert (-4) ** 3 == -64 and (-2) ** 3 == -8 and Fraction(1, 2) ** 3 == Fraction(1, 8) and Fraction(3, 5) ** 3 == Fraction(27, 125) and Fraction(-1, 10) ** 3 == Fraction(-1, 1000)
S.append(qa(K[2], 'លំហាត់គួរ ៖ រកឫសគូបនៃចំនួនខាងក្រោម', rows, 3))
assert near(0.2 ** 3, 0.008) and near((-0.1) ** 3, -0.001)
S.append(qa(K[2], 'ប្រតិបត្តិ ៖ រកឫសគូបនៃចំនួន', [('0.008', r'0.2'), ('-0.001', r'-0.1'), ('0.08', r'\sqrt[3]{0.08}'), ('-0.4', r'-\sqrt[3]{0.4}')], 2))

# ================================================================ 3. ប្រមាណវិធីលើរ៉ាឌីកាល់ (book p.5-12)
# ---- 3.1 multiply
S.append(part(3, 'វិធីគុណរ៉ាឌីកាល់', '<p class="ts-sub">៣. ប្រមាណវិធីលើរ៉ាឌីកាល់</p>'))
assert near(V(4) * V(9), V(36)) and near(C(8) * C(27), C(216)) and 6 ** 3 == 216
S.append(ex(K[3], 'ឧទាហរណ៍ទី ១ ៖ ' + m(r'\sqrt{4}\times\sqrt{9}'), p('គេអាចប្រៀបធៀប ' + m(r'\sqrt{4}\times\sqrt{9}') + ' និង ' + m(r'\sqrt{4\times 9}') + ' ដូចខាងក្រោម ។') + fig(area_product())))
S.append(ex(K[3], 'ឧទាហរណ៍ទី ២ ៖ ' + m(r'\sqrt[3]{8}\times\sqrt[3]{27}'),
    p('គេអាចប្រៀបធៀប ' + m(r'\sqrt[3]{8}\times\sqrt[3]{27}') + ' និង ' + m(r'\sqrt[3]{8\times 27}') + ' ដូចខាងក្រោម ។')
    + dm(r'\sqrt[3]{8}\times\sqrt[3]{27}=2\times 3=6')
    + dm(r'\sqrt[3]{8\times 27}=\sqrt[3]{216}=\sqrt[3]{6^3}=6')
    + p('ដូចនេះ ' + m(r'\sqrt[3]{8}\times\sqrt[3]{27}=\sqrt[3]{8\times 27}') + ' ។')))
S.append(key(K[3], 'ជាទូទៅ',
    p('ផលគុណនៃរ៉ាឌីកាល់ដែលមានសន្ទស្សន៍ដូចគ្នា ស្មើនឹងរ៉ាឌីកាល់នៃផលគុណ ។')
    + dm(r'\sqrt{a}\times\sqrt{b}=\sqrt{ab}\qquad a\ge 0\ ,\ b\ge 0')
    + dm(r'\sqrt[3]{a}\times\sqrt[3]{b}=\sqrt[3]{ab}\qquad a,\ b\ \text{អាចវិជ្ជមាន ឬអវិជ្ជមាន}')))
rows = [(r'\sqrt{2}\times\sqrt{8}', r'=\sqrt{16}=4'), (r'\sqrt{3}\times\sqrt{27}', r'=\sqrt{81}=9'), (r'\sqrt[3]{2}\times\sqrt[3]{4}', r'=\sqrt[3]{8}=2'),
        (r'\sqrt[3]{2}\times\sqrt[3]{\dfrac{1}{16}}', r'=\sqrt[3]{\dfrac{1}{8}}=\dfrac{1}{2}'), (r'\sqrt{2}\times\sqrt{32}', r'=\sqrt{64}=8'), (r'\sqrt{50}\times\sqrt{2}', r'=\sqrt{100}=10')]
assert near(V(2) * V(8), 4) and near(V(3) * V(27), 9) and near(C(2) * C(4), 2) and near(C(2) * C(1 / 16), 0.5) and near(V(2) * V(32), 8) and near(V(50) * V(2), 10)
S.append(qa(K[3], 'លំហាត់គួរ ៖ គណនាផលគុណនៃរ៉ាឌីកាល់ខាងក្រោម', rows, 2))
assert near(V(10) * V(0.1), 1) and near(C(10) * C(0.1), 1)
S.append(qa(K[3], 'ប្រតិបត្តិ ៖ គណនា', [(r'\sqrt{10}\times\sqrt{0.1}', r'=\sqrt{1}=1'), (r'\sqrt[3]{10}\times\sqrt[3]{0.1}', r'=\sqrt[3]{1}=1')], 1))

# ---- 3.2 divide
S.append(part(4, 'វិធីចែករ៉ាឌីកាល់'))
assert near(V(36) / V(4), 3) and near(V(36 / 4), 3) and near(C(27) / C(8), 1.5) and near(C(27 / 8), 1.5)
S.append(ex(K[4], 'ឧទាហរណ៍ទី ១ ៖ ' + m(r'\dfrac{\sqrt{36}}{\sqrt{4}}'),
    p('គេអាចប្រៀបធៀប ' + m(r'\dfrac{\sqrt{36}}{\sqrt{4}}') + ' និង ' + m(r'\sqrt{\dfrac{36}{4}}') + ' ដូចខាងក្រោម ។')
    + dm(r'\dfrac{\sqrt{36}}{\sqrt{4}}=\dfrac{\sqrt{6^2}}{\sqrt{2^2}}=\dfrac{6}{2}=3')
    + dm(r'\sqrt{\dfrac{36}{4}}=\sqrt{9}=3')
    + p('ហេតុនេះ ' + m(r'\dfrac{\sqrt{36}}{\sqrt{4}}=\sqrt{\dfrac{36}{4}}') + ' ។')))
S.append(ex(K[4], 'ឧទាហរណ៍ទី ២ ៖ ' + m(r'\dfrac{\sqrt[3]{27}}{\sqrt[3]{8}}'),
    p('គេអាចប្រៀបធៀប ' + m(r'\dfrac{\sqrt[3]{27}}{\sqrt[3]{8}}') + ' និង ' + m(r'\sqrt[3]{\dfrac{27}{8}}') + ' ដូចខាងក្រោម ។')
    + dm(r'\dfrac{\sqrt[3]{27}}{\sqrt[3]{8}}=\dfrac{\sqrt[3]{3^3}}{\sqrt[3]{2^3}}=\dfrac{3}{2}')
    + dm(r'\sqrt[3]{\dfrac{27}{8}}=\sqrt[3]{\left(\dfrac{3}{2}\right)^3}=\dfrac{3}{2}')
    + p('ហេតុនេះ ' + m(r'\dfrac{\sqrt[3]{27}}{\sqrt[3]{8}}=\sqrt[3]{\dfrac{27}{8}}') + ' ។')))
S.append(key(K[4], 'ជាទូទៅ',
    p('ផលចែកនៃរ៉ាឌីកាល់ដែលមានសន្ទស្សន៍ដូចគ្នា ស្មើនឹងរ៉ាឌីកាល់នៃផលចែក ។')
    + dm(r'\dfrac{\sqrt{a}}{\sqrt{b}}=\sqrt{\dfrac{a}{b}}\qquad a\ge 0\ ,\ b>0')
    + dm(r'\dfrac{\sqrt[3]{a}}{\sqrt[3]{b}}=\sqrt[3]{\dfrac{a}{b}}\qquad b\ne 0')))
rows = [(r'\dfrac{\sqrt{8}}{\sqrt{2}}', r'=\sqrt{4}=2'), (r'\dfrac{\sqrt[3]{48}}{\sqrt[3]{6}}', r'=\sqrt[3]{8}=2'), (r'\dfrac{\sqrt{3}}{\sqrt{27}}', r'=\sqrt{\dfrac{1}{9}}=\dfrac{1}{3}'),
        (r'\dfrac{\sqrt{288}}{\sqrt{2}}', r'=\sqrt{144}=12'), (r'\dfrac{\sqrt[3]{16}}{\sqrt[3]{2}}', r'=\sqrt[3]{8}=2'), (r'\dfrac{\sqrt[3]{\frac{1}{2}}}{\sqrt[3]{4}}', r'=\sqrt[3]{\dfrac{1}{8}}=\dfrac{1}{2}'),
        (r'\dfrac{\sqrt{10}}{\sqrt{0.1}}', r'=\sqrt{100}=10'), (r'\dfrac{\sqrt[3]{25}}{\sqrt[3]{0.2}}', r'=\sqrt[3]{125}=5')]
assert near(V(8) / V(2), 2) and near(C(48) / C(6), 2) and near(V(3) / V(27), 1 / 3) and near(V(288) / V(2), 12) and near(C(16) / C(2), 2)
assert near(C(0.5) / C(4), 0.5) and near(V(10) / V(0.1), 10) and near(C(25) / C(0.2), 5)
S.append(qa(K[4], 'លំហាត់គួរ ៖ គណនាផលចែកនៃរ៉ាឌីកាល់ខាងក្រោម', rows, 2))
assert near(V(7) / V(28), .5) and near(C(5) / C(0.2), C(25)) and near(V(10) / V(1000), .1) and near(C(100) / C(0.1), 10)
S.append(qa(K[4], 'ប្រតិបត្តិ ៖ គណនាផលចែក', [(r'\dfrac{\sqrt{7}}{\sqrt{28}}', r'=\sqrt{\dfrac{1}{4}}=\dfrac{1}{2}'), (r'\dfrac{\sqrt[3]{5}}{\sqrt[3]{0.2}}', r'=\sqrt[3]{25}'),
    (r'\dfrac{\sqrt{10}}{\sqrt{1000}}', r'=\sqrt{\dfrac{1}{100}}=\dfrac{1}{10}'), (r'\dfrac{\sqrt[3]{100}}{\sqrt[3]{0.1}}', r'=\sqrt[3]{1000}=10')], 2))

# ---- 3.3 take a number out
S.append(part(5, 'ការបញ្ចេញមួយចំនួនពីរ៉ាឌីកាល់'))
S.append(ex(K[5], 'ឧទាហរណ៍ទី ១ ៖ រក ' + m('x') + ' បើ ' + m('x^2=9'),
    p('តាមរូបមន្ត ' + m(r'x=\sqrt{a}') + ' , ' + m(r'x=-\sqrt{a}') + ' ។ ' + m('9') + ' មានឫសការេពីរគឺ ' + m(r'x=\sqrt{9}') + ' និង ' + m(r'x=-\sqrt{9}') + ' ។')
    + p('ម៉្យាងទៀត ' + m('3^2=9') + ' , ' + m('(-3)^2=9') + ' ដូចនេះ ' + m('3') + ' , ' + m('-3') + ' ក៏ជាឫសការេនៃ ' + m('9') + ' ។')
    + p('យើងទាញបាន ' + m(r'\sqrt{9}=3') + ' , ' + m(r'-\sqrt{9}=-3') + ' ។')
    + p('គេសម្គាល់ឃើញថា ' + m(r'\sqrt{9}=\sqrt{3^2}=3') + ' មានន័យថាគេបាន' + hl('បញ្ចេញ ' + m('9') + ' ពីរ៉ាឌីកាល់') + ' ។')))
S.append(ex(K[5], 'ឧទាហរណ៍ទី ២ ៖ រក ' + m('x') + ' បើ ' + m('x^3=8'),
    p('តាម ' + m('x^3=a') + ' , ' + m(r'x=\sqrt[3]{a}') + ' ។ ម៉្យាងទៀត ' + m('2^3=8') + ' ។')
    + p('យើងទាញបាន ' + m(r'\sqrt[3]{8}=2') + ' ។')
    + p('គេសម្គាល់ឃើញថា ' + m(r'\sqrt[3]{8}=\sqrt[3]{2^3}=2') + ' មានន័យថាគេបាន' + hl('បញ្ចេញ ' + m('8') + ' ពីរ៉ាឌីកាល់') + ' ។')))
S.append(key(K[5], 'ជាទូទៅ',
    p('ដើម្បីបញ្ចេញមួយចំនួនពីរ៉ាឌីកាល់ គេត្រូវប្លែងរ៉ាឌីកង់ជាស្វ័យគុណដែលមាននិទស្សន្តស្មើនឹងសន្ទស្សន៍នៃរ៉ាឌីកាល់ ។')))
S.append(ex(K[5], 'ករណីរ៉ាឌីកង់ជាចំនួនអថេរ',
    p('ដោយ ' + m(r'\sqrt{5^2}=5') + ' , ' + m(r'\sqrt{(-5)^2}=5') + ' ដូចនេះ ' + m(r'\sqrt{x^2}=|x|') + ' ជាចំនួនវិជ្ជមាន ។')
    + p('បើ ' + m(r'x\ge 0') + ' នោះ ' + m(r'\sqrt{x^2}=x') + ' ; បើ ' + m(r'x\le 0') + ' , ' + m(r'\sqrt{x^2}=-x') + ' ។')
    + p('ដោយ ' + m(r'\sqrt[3]{5^3}=5') + ' , ' + m(r'\sqrt[3]{(-5)^3}=-5') + ' ដូចនេះ ' + m(r'\sqrt[3]{x^3}=x') + ' ។')))
assert near(V(121), 11) and near(V(4 / 9), 2 / 3) and near(C(125), 5) and near(V(16 * 81), 36) and near(C(-27), -3) and near(C(2 / 2000), 1 / 10)
rows = [(r'\sqrt{121}', r'=\sqrt{11^2}=11'), (r'\sqrt{\dfrac{4}{9}}', r'=\sqrt{\left(\dfrac{2}{3}\right)^2}=\dfrac{2}{3}'), (r'\sqrt[3]{125}', r'=\sqrt[3]{5^3}=5'),
        (r'\sqrt{16\times 81}', r'=\sqrt{(4\times 9)^2}=36'), (r'\sqrt[3]{-27}', r'=-\sqrt[3]{27}=-\sqrt[3]{3^3}=-3'), (r'\sqrt[3]{\dfrac{2}{2000}}', r'=\sqrt[3]{\dfrac{1}{1000}}=\dfrac{1}{10}')]
S.append(qa(K[5], 'លំហាត់គួរទី ១ ៖ បញ្ចេញមួយចំនួនពីរ៉ាឌីកាល់', rows, 2))
assert near(V(32), 4 * V(2)) and near(C(16), 2 * C(2))
S.append(ex(K[5], 'លំហាត់គួរទី ២ ៖ បញ្ចេញចំនួនពីរ៉ាឌីកាល់ ' + m(r'\sqrt{32}') + ' និង ' + m(r'\sqrt[3]{16}'),
    p('តាមលក្ខណៈនៃវិធីគុណ ៖')
    + dm(r'\sqrt{32}=\sqrt{16\times 2}=\sqrt{16}\times\sqrt{2}=\sqrt{4^2}\times\sqrt{2}=4\sqrt{2}')
    + dm(r'\sqrt[3]{16}=\sqrt[3]{8\times 2}=\sqrt[3]{8}\times\sqrt[3]{2}=\sqrt[3]{2^3}\times\sqrt[3]{2}=2\sqrt[3]{2}')))
S.append(ex(K[5], 'រូបភាព ៖ ' + m(r'\sqrt{18}=3\sqrt{2}'), fig(simplify18())))
assert near(V(2 / 8), .5) and near(C(81 / 3), 3) and near(V(12), 2 * V(3)) and near(C(81), 3 * C(3)) and near(V(50), 5 * V(2)) and near(V(2 / 25), V(2) / 5)
S.append(qa(K[5], 'ប្រតិបត្តិ ៖ បញ្ចេញមួយចំនួនពីរ៉ាឌីកាល់', [(r'\sqrt{\dfrac{2}{8}}', r'=\dfrac{1}{2}'), (r'\sqrt[3]{\dfrac{81}{3}}', r'=\sqrt[3]{27}=3'), (r'\sqrt{12}', r'=2\sqrt{3}'),
    (r'\sqrt[3]{81}', r'=3\sqrt[3]{3}'), (r'\sqrt{50}', r'=5\sqrt{2}'), (r'\sqrt{\dfrac{2}{25}}', r'=\dfrac{\sqrt{2}}{5}')], 3))

# ---- 3.4 put a number in
S.append(part(6, 'ការបញ្ចូលមួយចំនួនក្នុងរ៉ាឌីកាល់'))
assert near(4 * V(2), V(32)) and near(3 * C(2), C(54))
S.append(ex(K[6], 'ការបញ្ចូលមួយចំនួនទៅក្នុងរ៉ាឌីកាល់',
    p('ជាវិធីប្រាសនៃការបញ្ចេញមួយចំនួនពីរ៉ាឌីកាល់ ។')
    + p(hl('ឧទាហរណ៍ទី ១') + ' ៖ គេមាន ' + m(r'4\sqrt{2}') + ' បញ្ចូល ' + m('4') + ' ទៅក្នុងរ៉ាឌីកាល់ ។')
    + dm(r'4\sqrt{2}=\sqrt{4^2}\times\sqrt{2}=\sqrt{4^2\times 2}=\sqrt{16\times 2}=\sqrt{32}')
    + p(hl('ឧទាហរណ៍ទី ២') + ' ៖ គេមាន ' + m(r'3\sqrt[3]{2}') + ' បញ្ចូល ' + m('3') + ' ទៅក្នុងរ៉ាឌីកាល់ ។')
    + dm(r'3\sqrt[3]{2}=\sqrt[3]{3^3}\times\sqrt[3]{2}=\sqrt[3]{27\times 2}=\sqrt[3]{54}')))
S.append(key(K[6], 'ជាទូទៅ', p('ដើម្បីបញ្ចូលមួយចំនួនទៅក្នុងរ៉ាឌីកាល់ គេត្រូវលើកចំនួននោះជាស្វ័យគុណដោយឱ្យនិទស្សន្តនៃស្វ័យគុណស្មើនឹងសន្ទស្សន៍នៃរ៉ាឌីកាល់ ។')))
rows = [(r'\dfrac{2}{3}\sqrt{\dfrac{12}{5}}', r'=\sqrt{\dfrac{4}{9}}\times\sqrt{\dfrac{12}{5}}=\sqrt{\dfrac{16}{15}}'), (r'5\sqrt{\dfrac{3}{50}}', r'=\sqrt{25}\times\sqrt{\dfrac{3}{50}}=\sqrt{\dfrac{3}{2}}'),
        (r'-7\sqrt{5}', r'=-\sqrt{49}\times\sqrt{5}=-\sqrt{245}'), (r'-5\sqrt[3]{\dfrac{4}{25}}', r'=-\sqrt[3]{125}\times\sqrt[3]{\dfrac{4}{25}}=-\sqrt[3]{20}'),
        (r'2\sqrt[3]{\dfrac{5}{12}}', r'=\sqrt[3]{8}\times\sqrt[3]{\dfrac{5}{12}}=\sqrt[3]{\dfrac{10}{3}}'), (r'\dfrac{1}{2}\sqrt[3]{4}', r'=\sqrt[3]{\dfrac{1}{8}}\times\sqrt[3]{4}=\sqrt[3]{\dfrac{1}{2}}')]
assert near(2 / 3 * V(12 / 5), V(16 / 15)) and near(5 * V(3 / 50), V(3 / 2)) and near(-7 * V(5), -V(245)) and near(-5 * C(4 / 25), -C(20)) and near(2 * C(5 / 12), C(10 / 3)) and near(C(4) / 2, C(1 / 2))
S.append(worked(K[6], 'លំហាត់គួរ ៖ បញ្ចូលមួយចំនួនក្នុងរ៉ាឌីកាល់', [(LB[i], q + a) for i, (q, a) in enumerate(rows)]))
assert near(V(3) / 3, V(1 / 3)) and near(5 * C(2 / 25), C(10)) and near(2 / 11 * V(121 / 7), V(4 / 7))
S.append(qa(K[6], 'ប្រតិបត្តិ ៖ បញ្ចូលមួយចំនួនក្នុងរ៉ាឌីកាល់', [(r'\dfrac{1}{3}\sqrt{3}', r'=\sqrt{\dfrac{1}{3}}'), (r'5\sqrt[3]{\dfrac{2}{25}}', r'=\sqrt[3]{10}'), (r'\dfrac{2}{11}\sqrt{\dfrac{121}{7}}', r'=\sqrt{\dfrac{4}{7}}')], 1))

# ---- 3.5 add and subtract
S.append(part(7, 'វិធីបូកនិងវិធីដករ៉ាឌីកាល់'))
assert near(2 * V(3) + 6 * V(3), 8 * V(3)) and near(7 * V(6) - 5 * V(6), 2 * V(6)) and near(C(7) + 4 * C(7), 5 * C(7)) and near(12 * C(5) - 7 * C(5), 5 * C(5))
S.append(ex(K[7], 'ឧទាហរណ៍ទី ១',
    p('ដូចគ្នានឹងវិធីបូកនិងវិធីដកលើឯកធាតុ ' + m('3x+4x=(3+4)x=7x') + ' ។')
    + dm(r'2\sqrt{3}+6\sqrt{3}=(2+6)\sqrt{3}=8\sqrt{3}')
    + dm(r'7\sqrt{6}-5\sqrt{6}=(7-5)\sqrt{6}=2\sqrt{6}')
    + dm(r'\sqrt[3]{7}+4\sqrt[3]{7}=(1+4)\sqrt[3]{7}=5\sqrt[3]{7}')
    + dm(r'12\sqrt[3]{5}-7\sqrt[3]{5}=(12-7)\sqrt[3]{5}=5\sqrt[3]{5}')))
S.append(ex(K[7], 'រូបភាព ៖ រ៉ាឌីកង់ដូចគ្នាទើបបូកបាន', fig(like_radicals())))
S.append(ex(K[7], 'សម្គាល់',
    p(hl('សម្គាល់') + ' ៖ ' + m(r'\sqrt{3}+\sqrt{7}') + ' មានរ៉ាឌីកង់ខុសគ្នា ខុសគ្នាមិនអាចបូកបានទេ ។')
    + p('ក្នុងករណីរ៉ាឌីកាល់មានរ៉ាឌីកង់ខុសគ្នា គេត្រូវបំប្លែងឱ្យមានរ៉ាឌីកង់ដូចគ្នាសិន ។')))
assert near(3 * V(2) + V(8), 5 * V(2)) and near(5 * V(12) - V(27), 7 * V(3)) and near(3 * C(16) + 5 * C(2), 11 * C(2))
S.append(ex(K[7], 'ឧទាហរណ៍ទី ២',
    dm(r'3\sqrt{2}+\sqrt{8}=3\sqrt{2}+2\sqrt{2}=(3+2)\sqrt{2}=5\sqrt{2}')
    + dm(r'5\sqrt{12}-\sqrt{27}=5\sqrt{4\times 3}-\sqrt{9\times 3}=10\sqrt{3}-3\sqrt{3}=(10-3)\sqrt{3}=7\sqrt{3}')
    + dm(r'3\sqrt[3]{16}+5\sqrt[3]{2}=3\sqrt[3]{8\times 2}+5\sqrt[3]{2}=6\sqrt[3]{2}+5\sqrt[3]{2}=(6+5)\sqrt[3]{2}=11\sqrt[3]{2}')))
S.append(key(K[7], 'ជាទូទៅ',
    p('ដើម្បីគណនាផលបូកនិងផលដករ៉ាឌីកាល់ដែលមានសន្ទស្សន៍ដូចគ្នា គេត្រូវបំប្លែងរ៉ាឌីកង់ឱ្យដូចគ្នា ។')
    + p('ដើម្បីគណនាផលបូកនិងផលដករ៉ាឌីកាល់ដែលមានរ៉ាឌីកង់ដូចគ្នានិងមានសន្ទស្សន៍ដូចគ្នា គេបូក-ដកមេគុណនឹងមេគុណ ហើយរ៉ាឌីកាល់ទុកដដែល ។')))
assert near(3 * V(11) + 5 * V(44) - 3 * V(99), 4 * V(11)) and near(3 * V(18) - V(12) + V(75) + V(2), 10 * V(2) + 3 * V(3)) and near(3 * C(24) + 6 * C(81), 24 * C(3))
assert near(V(20) + V(80) - V(45), 3 * V(5)) and near(14 * V(3) + 6 * V(2) - 11 * V(3), 3 * V(3) + 6 * V(2))
for _x in (1.7, 2.9):
    assert near(6 * C(8 * _x ** 2) - 2 * C(27 * _x ** 2), 6 * C(_x ** 2))
S.append(worked(K[7], 'លំហាត់គួរទី ១ ៖ គណនា', [
    ('ក', r'A=3\sqrt{11}+5\sqrt{44}-3\sqrt{99}=3\sqrt{11}+10\sqrt{11}-9\sqrt{11}=4\sqrt{11}'),
    ('ខ', r'B=3\sqrt{18}-\sqrt{12}+\sqrt{75}+\sqrt{2}=9\sqrt{2}-2\sqrt{3}+5\sqrt{3}+\sqrt{2}=10\sqrt{2}+3\sqrt{3}'),
    ('គ', r'C=3\sqrt[3]{24}+6\sqrt[3]{81}=6\sqrt[3]{3}+18\sqrt[3]{3}=24\sqrt[3]{3}'),
    ('ឃ', r'D=6\sqrt[3]{8x^2}-2\sqrt[3]{27x^2}=12\sqrt[3]{x^2}-6\sqrt[3]{x^2}=6\sqrt[3]{x^2}'),
    ('ង', r'E=\sqrt{20}+\sqrt{80}-\sqrt{45}=2\sqrt{5}+4\sqrt{5}-3\sqrt{5}=3\sqrt{5}'),
    ('ច', r'F=14\sqrt{3}+6\sqrt{2}-11\sqrt{3}=3\sqrt{3}+6\sqrt{2}')]))
for _x in (1.7, 2.9):
    assert near(V(128 * _x) - V(2 * _x), 7 * V(2 * _x)) and near(5 * V(18 * _x) + 2 * V(8 * _x), 19 * V(2 * _x)) and near(V(8 * _x + 8) + V(2 * _x + 2), 3 * V(2 * _x + 2))
    assert near(V(200 * _x ** 2) - V(98 * _x ** 2), 3 * _x * V(2)) and near(V(8 * _x ** 2) + V(2 * _x ** 2), 3 * _x * V(2)) and near(2 * V(45 * _x ** 3) - V(20 * _x ** 3), 4 * _x * V(5 * _x))
S.append(worked(K[7], 'លំហាត់គួរទី ២ ៖ សម្រួល', [
    ('ក', r'A=\sqrt{128y}-\sqrt{2y}=8\sqrt{2y}-\sqrt{2y}=7\sqrt{2y}\quad(y>0)'),
    ('ខ', r'B=5\sqrt{18x}+2\sqrt{8x}=15\sqrt{2x}+4\sqrt{2x}=19\sqrt{2x}\quad(x>0)'),
    ('គ', r'C=\sqrt{8n+8}+\sqrt{2n+2}=2\sqrt{2n+2}+\sqrt{2n+2}=3\sqrt{2n+2}\quad(n>0)'),
    ('ឃ', r'D=\sqrt{200k^2}-\sqrt{98k^2}=10k\sqrt{2}-7k\sqrt{2}=3k\sqrt{2}\quad(k>0)'),
    ('ង', r'E=\sqrt{8x^2}+\sqrt{2x^2}=2x\sqrt{2}+x\sqrt{2}=3x\sqrt{2}\quad(x>0)'),
    ('ច', r'F=2\sqrt{45x^3}-\sqrt{20x^3}=6x\sqrt{5x}-2x\sqrt{5x}=4x\sqrt{5x}\quad(x>0)')]))
assert near(5 * V(50) - 8 * V(32), -7 * V(2))
for _x in (1.7, 2.9):
    assert near(V(48 * _x) - V(27 * _x), V(3 * _x)) and near(V(5 * _x) + 3 * V(45 * _x ** 3), (1 + 9 * _x) * V(5 * _x)) and near(V(12 * _x + 12) + V(27 * _x + 27), 5 * V(3 * _x + 3)) and near(V(72 * _x) - 3 * V(98 * _x), -15 * V(2 * _x))
S.append(qa(K[7], 'ប្រតិបត្តិ ៖ សម្រួល', [
    (r'5\sqrt{50}-8\sqrt{32}', r'=-7\sqrt{2}'), (r'\sqrt{48x}-\sqrt{27x}', r'=\sqrt{3x}'), (r'\sqrt{5P}+3\sqrt{45P^3}\ (P>0)', r'=(1+9P)\sqrt{5P}'),
    (r'\sqrt{12x+12}+\sqrt{27x+27}', r'=5\sqrt{3x+3}'), (r'\sqrt{72a}-3\sqrt{98a}', r'=-15\sqrt{2a}')], 1))

# ---- 3.6 rationalise
S.append(part(8, 'វិធីបំបាត់រ៉ាឌីកាល់ពីភាគបែង'))
assert near(3 / V(2), 3 * V(2) / 2) and near(3 / V(2), 2.1213203435596424) and near(C(3) / C(4), C(6) / 2)
S.append(ex(K[8], 'ឧទាហរណ៍ទី ១',
    p('ជាទូទៅគេមិនទុកឱ្យចំនួនដែលមានរ៉ាឌីកាល់នៅភាគបែងទេ ។ ' + m(r'\dfrac{3}{\sqrt{2}}') + ' ជាចំនួនដែលមានរ៉ាឌីកាល់នៅភាគបែង ជាហេតុធ្វើឱ្យពិបាកស្គាល់មេគុណរបស់វា ។')
    + dm(r'\dfrac{3}{\sqrt{2}}=\dfrac{3\times\sqrt{2}}{\sqrt{2}\sqrt{2}}=\dfrac{3\sqrt{2}}{2}=\dfrac{3}{2}\sqrt{2}')
    + p('ដូចគ្នានេះដែរ ចំពោះចំនួន ' + m(r'\dfrac{\sqrt[3]{3}}{\sqrt[3]{4}}') + ' ៖')
    + dm(r'\dfrac{\sqrt[3]{3}\sqrt[3]{2}}{\sqrt[3]{4}\sqrt[3]{2}}=\dfrac{\sqrt[3]{6}}{\sqrt[3]{8}}=\dfrac{\sqrt[3]{6}}{2}=\dfrac{1}{2}\sqrt[3]{6}')))
assert near(2 / (V(7) - 2), 2 * (V(7) + 2) / 3) and near(V(2) / (V(5) + V(2)), (V(10) - 2) / 3)
S.append(ex(K[8], 'ឧទាហរណ៍ទី ២ ៖ ' + m(r'\dfrac{2}{\sqrt{7}-2}'),
    p('ក្នុងករណីដែលភាគបែងមានរ៉ាឌីកាល់ពីរតួ គេត្រូវគុណនឹងកន្សោមឆ្លាស់ ។')
    + p('កន្សោមឆ្លាស់នៃ ' + m(r'\sqrt{7}-2') + ' គឺ ' + m(r'\sqrt{7}+2') + ' ដោយប្រើ ' + m('a^2-b^2=(a-b)(a+b)') + ' ។')
    + dm(r'\dfrac{2}{\sqrt{7}-2}=\dfrac{2(\sqrt{7}+2)}{(\sqrt{7}-2)(\sqrt{7}+2)}=\dfrac{2(\sqrt{7}+2)}{7-4}=\dfrac{2(\sqrt{7}+2)}{3}')))
S.append(ex(K[8], 'ឧទាហរណ៍ទី ៣ ៖ ' + m(r'\dfrac{\sqrt{2}}{\sqrt{5}+\sqrt{2}}'),
    dm(r'\dfrac{\sqrt{2}}{\sqrt{5}+\sqrt{2}}=\dfrac{\sqrt{2}(\sqrt{5}-\sqrt{2})}{(\sqrt{5}+\sqrt{2})(\sqrt{5}-\sqrt{2})}=\dfrac{\sqrt{10}-2}{5-2}=\dfrac{\sqrt{10}-2}{3}')))
assert near((V(3) + V(2)) / (V(3) - V(2)), 5 + 2 * V(6)) and near((1 + V(2)) / (3 - V(3)), (3 + V(3) + 3 * V(2) + V(6)) / 6) and near((1 + V(3)) / (2 + V(5)), -2 + V(5) - 2 * V(3) + V(15))
assert near(8 * V(2) / (V(20) - V(18)), 8 * V(10) + 24) and near(2 / C(7), 2 * C(49) / 7) and near(3 / (C(5) - C(2)), C(25) + C(10) + C(4))
S.append(worked(K[8], 'លំហាត់គួរទី ១ ៖ សម្រួល (ក ដល់ ឃ)', [
    ('ក', r'A=\dfrac{\sqrt{3}+\sqrt{2}}{\sqrt{3}-\sqrt{2}}=\dfrac{(\sqrt{3}+\sqrt{2})^2}{3-2}=5+2\sqrt{6}'),
    ('ខ', r'B=\dfrac{1+\sqrt{2}}{3-\sqrt{3}}=\dfrac{(1+\sqrt{2})(3+\sqrt{3})}{9-3}=\dfrac{3+\sqrt{3}+3\sqrt{2}+\sqrt{6}}{6}'),
    ('គ', r'C=\dfrac{1+\sqrt{3}}{2+\sqrt{5}}=\dfrac{(1+\sqrt{3})(2-\sqrt{5})}{4-5}=-2+\sqrt{5}-2\sqrt{3}+\sqrt{15}'),
    ('ឃ', r'D=\dfrac{8\sqrt{2}}{\sqrt{20}-\sqrt{18}}=\dfrac{8\sqrt{2}(\sqrt{20}+\sqrt{18})}{20-18}=\dfrac{16\sqrt{10}+48}{2}=8\sqrt{10}+24')]))
S.append(worked(K[8], 'លំហាត់គួរទី ១ ៖ សម្រួល (ង និង ច)', [
    ('ង', r'E=\dfrac{2}{\sqrt[3]{7}}=\dfrac{2(\sqrt[3]{7})^2}{\sqrt[3]{7}(\sqrt[3]{7})^2}=\dfrac{2\sqrt[3]{49}}{7}'),
    ('ច', r'F=\dfrac{3}{\sqrt[3]{5}-\sqrt[3]{2}}\ \ \text{ប្រើ}\ (a-b)(a^2+ab+b^2)=a^3-b^3'),
    ('', r'=\dfrac{3(\sqrt[3]{25}+\sqrt[3]{10}+\sqrt[3]{4})}{5-2}=\sqrt[3]{25}+\sqrt[3]{10}+\sqrt[3]{4}')]))
assert near(1 / (V(5) + V(2)), (V(5) - V(2)) / 3) and near((3 * V(2) + 2 * V(3)) / (V(12) - V(18)), -5 - 2 * V(6))
assert near(3 / (C(5) - C(4)), 3 * C(25) + 3 * C(20) + 6 * C(2)) and near(C(3) / (C(4) + C(2)), (2 * C(6) - 2 * C(3) + C(12)) / 6)
S.append(qa(K[8], 'ប្រតិបត្តិ ៖ សម្រួល', [(r'\dfrac{1}{\sqrt{5}+\sqrt{2}}', r'=\dfrac{\sqrt{5}-\sqrt{2}}{3}'), (r'\dfrac{3\sqrt{2}+2\sqrt{3}}{\sqrt{12}-\sqrt{18}}', r'=-5-2\sqrt{6}'),
    (r'\dfrac{3}{\sqrt[3]{5}-\sqrt[3]{4}}', r'=3\sqrt[3]{25}+3\sqrt[3]{20}+6\sqrt[3]{2}'), (r'\dfrac{\sqrt[3]{3}}{\sqrt[3]{4}+\sqrt[3]{2}}', r'=\dfrac{2\sqrt[3]{6}-2\sqrt[3]{3}+\sqrt[3]{12}}{6}')], 1))

# ---------------------------------------------------------------- summary, exit ticket, end
S.append(key('សង្ខេប', 'សេចក្តីសង្ខេប', ul([
    'បើ ' + m('a>0') + ' , ' + m('x^2=a') + ' នោះ ' + m(r'x=\pm\sqrt{a}') + ' ។ បើ ' + m('x^3=a') + ' នោះ ' + m(r'x=\sqrt[3]{a}') + ' ។',
    m(r'\sqrt{a}\times\sqrt{b}=\sqrt{ab}') + ' , ' + m(r'\dfrac{\sqrt{a}}{\sqrt{b}}=\sqrt{\dfrac{a}{b}}') + ' ។',
    'បញ្ចេញ ៖ ' + m(r'\sqrt{12}=2\sqrt{3}') + ' ។ បញ្ចូល ៖ ' + m(r'3\sqrt{2}=\sqrt{18}') + ' ។ បូក-ដកបានលុះត្រាតែរ៉ាឌីកាល់ដូចគ្នា ។',
    'ភាគបែងមានរ៉ាឌីកាល់ ៖ គុណនឹងរ៉ាឌីកាល់ ឬកន្សោមឆ្លាស់ ។'])))
assert near(V(49), 7) and near(C(-27), -3) and near(V(48), 4 * V(3)) and near(2 * V(5) + V(45), 5 * V(5)) and near(6 / V(3), 2 * V(3))
exit_rows = [('គណនា ' + m(r'\sqrt{49}') + ' និង ' + m(r'\sqrt[3]{-27}'), m('7') + ' និង ' + m('-3')),
             ('បញ្ចេញ ' + m(r'\sqrt{48}'), m(r'\sqrt{16\times 3}=4\sqrt{3}')),
             ('សម្រួល ' + m(r'2\sqrt{5}+\sqrt{45}'), m(r'2\sqrt{5}+3\sqrt{5}=5\sqrt{5}')),
             ('បំបាត់រ៉ាឌីកាល់ពីភាគបែង ' + m(r'\dfrac{6}{\sqrt{3}}'), m(r'\dfrac{6\sqrt{3}}{3}=2\sqrt{3}')),
             (m(r'\sqrt{20}') + ' ជាចំនួនសនិទាន ឬអសនិទាន? ហេតុអ្វី?', 'អសនិទាន ព្រោះ ' + m('20') + ' មិនមែនជាការេប្រាកដ')]
S.append(ex('សំបុត្រចេញ', 'ពិនិត្យយល់ចុងក្រោយ', p('សរសេរចម្លើយលើក្រដាសតូច ហើយប្រគល់ជូនគ្រូមុនចេញ ។') + ''.join(
    f'<div style="display:grid;grid-template-columns:1.2fr 1fr;gap:1em;align-items:center;margin:.3em 0"><div><b>{i}.</b> {q}</div>{rvd(i, a)}</div>' for i, (q, a) in enumerate(exit_rows, 1))))
S.append({'k': 'title', 'html': '<p class="ts-kicker">មេរៀនទី ១</p><h1>ចប់មេរៀន</h1><p class="ts-sub">ចំនួនអសនិទាន</p><div class="th-you">សូមអរគុណ</div>'})

# ---------------------------------------------------------------- write (no draw-on animation: pictures fade in smoothly, pieces appear with the reveal steps)
for s in S:
    s.setdefault('k', '')
    s['html'] = s['html'].replace(' ។', '\u00a0។')    # the book spaces before ។: keep it with the word so a line never starts with it
out = [stepify(x) if x.get('k') in ('sol', 'ex', 'key', 'prac') and 'data-step' not in x['html'] else x for x in S]
os.makedirs(os.path.dirname(OUT), exist_ok=True)
js = ('// Deck for Grade 9 Lesson 1 (follows the MoEYS textbook): tools/lesson9_1/build.py — do not edit by hand.\n'
      + 'window.TEACH_SLIDES = window.TEACH_SLIDES || {};\n'
      + "window.TEACH_SLIDES['9-1'] = " + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ';\n')
open(OUT, 'w', encoding='utf8').write(js)
print(len(out), 'slides ->', os.path.abspath(OUT), len(js) // 1024, 'KB')
