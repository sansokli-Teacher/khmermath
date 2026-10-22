# One-off: the teaching-method additions to tools/lesson9_1 (lesson map, guess-first, true/false checks, proof that sqrt2 is irrational, exit ticket).
here = __file__.rsplit('/', 1)[0]
pb, pv = here + '/build.py', here + '/vis9.py'
s = open(pb, encoding='utf-8').read()
v = open(pv, encoding='utf-8').read()


def sub(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (old[:90], s.count(old))
    s = s.replace(old, new)


# ------------------------------------------------------------------ picture: the map of the lesson
v += r'''

# ---------------------------------------------------------------- the map of the lesson: six steps, each builds on the one before
def lesson_map():
    boxes = [('1', '√a', 'ឫសការេ និងចំនួនអសនិទាន', '#1c7ed6'), ('2', '∛a', 'ឫសគូប', '#2b8a87'), ('3', '√a · √b = √ab', 'គុណ និងចែករ៉ាឌីកាល់', '#2f9e44'),
             ('4', '3√2 = √18', 'បញ្ចេញ និងបញ្ចូល', '#f08c00'), ('5', '3√2 + 4√2', 'បូក និងដក', '#e8590c'), ('6', '1/√2 = √2/2', 'បំបាត់រ៉ាឌីកាល់ពីភាគបែង', '#ae3ec9')]
    b = ''
    pos = [(60, 70), (370, 70), (680, 70), (680, 270), (370, 270), (60, 270)]       # a snake: left to right, then back
    for k, ((no, expr, name, col), (x, y)) in enumerate(zip(boxes, pos)):
        g = rect(x, y, 260, 150, '#fff', 20, col, 5) + circ(x + 34, y + 34, 22, col) + M(x + 34, y + 44, no, 30, '#fff')
        g += M(x + 130, y + 88, expr, 38, col) + T(x + 130, y + 132, name, 22, NAVY)
        b += rvg(k, g) if k else g
    for k, (a, c) in enumerate(((0, 1), (1, 2), (2, 3), (3, 4), (4, 5))):
        (x1, y1), (x2, y2) = pos[a], pos[c]
        if y1 == y2:
            xa, xb = (x1 + 262, x2 - 2) if x2 > x1 else (x1 - 2, x2 + 262)
            b += rvg(k + 1, arrow(xa, y1 + 75, xb, y2 + 75, GREY, 6))
        else:
            b += rvg(k + 1, arrow(x1 + 130, y1 + 152, x2 + 130, y2 - 2, GREY, 6))
    return svg(1000, 470, b, '56vh')
'''

# ------------------------------------------------------------------ build.py: helpers, then the slides
sub("S = []\n", r'''def tf_rows(rows, size='1.05em'):
    """statement | answer: the answer appears on its own step (students decide first). rows = [(statement html, True/False, why html)]"""
    cells = []
    for i, (st, ok, why) in enumerate(rows, 1):
        ans = ('<span style="color:#2f9e44;font-weight:800">✓ ពិត</span>' if ok else '<span style="color:#e03131;font-weight:800">✗ មិនពិត</span>') + (' ' + why if why else '')
        cells.append(f'<div style="display:grid;grid-template-columns:1.1fr 1fr;gap:1em;align-items:center;margin:.25em 0"><div><b>{i}.</b> {st}</div>{rvd(i, ans)}</div>')
    return ''.join(cells)


S = []
''')

# lesson map right after the cover
sub("S.append(slide('រំលឹក', 'រំលឹកចំណេះដឹង',", "S.append(ex('ផែនទីមេរៀន', 'ថ្ងៃនេះយើងនឹងដើរតាមជំហានទាំងប្រាំមួយនេះ', fig(lesson_map())))\n\nS.append(slide('រំលឹក', 'រំលឹកចំណេះដឹង',")

# guess first, before the garden
sub("S.append(ex(K[1], 'សួនច្បាររាងការេ',", r'''S.append(ex(K[1], 'ទាយសិន',
    p('សួនច្បាររាងការេមួយ មានក្រឡាផ្ទៃ ' + m(r'3\text{ m}^2') + '។ តើប្រវែងជ្រុងប្រហែលប៉ុន្មាន? ' + hl('សរសេរចម្លើយទាយរបស់ប្អូនៗលើក្តារតូច') + '។')
    + rvd(1, p('ជ្រើសមួយ៖ ' + m('1.5') + '   ' + m('1.7') + '   ' + m('2')))
    + rvd(2, p('ពិនិត្យដោយលើកជាការេ៖ ' + m('1.5^2=2.25') + '  ' + m('1.7^2=2.89') + '  ' + m('2^2=4')))
    + rvd(3, p('មួយណាជិត ' + m('3') + ' ជាងគេ? តើមានចំនួនទសភាគណាដែលការេស្មើ ' + m('3') + ' បេះបិទទេ? ' + hl('តោះស្វែងរក!')))))
assert abs(1.5 ** 2 - 2.25) < 1e-12 and abs(1.7 ** 2 - 2.89) < 1e-12 and 2 ** 2 == 4
S.append(ex(K[1], 'សួនច្បាររាងការេ',''')

# the proof that sqrt 2 is irrational, an extension for strong students, after the sets of numbers
sub("S.append(key(K[1], 'វិធីសម្រេចចិត្ត ១–៣', ol([", r'''S.append(ex('បន្ថែម សម្រាប់សិស្សពូកែ', 'ហេតុអ្វី ' + '√2' + ' ជាចំនួនអសនិទាន?',
    p('យើងសន្មតថា ' + m(r'\sqrt{2}') + ' ជាចំនួនសនិទាន ហើយឃើញថាវាប្រែជាផ្ទុយនឹងខ្លួនវា។')
    + rvd(1, p(hl('១.') + ' សន្មតថា ' + m(r'\sqrt{2}=\dfrac{p}{q}') + ' ដែល ' + m('p,q') + ' ជាចំនួនគត់ ហើយប្រភាគនេះសម្រួលអស់ហើយ (គ្មានកត្តារួម)។'))
    + rvd(2, p(hl('២.') + ' លើកជាការេ៖ ' + m(r'2=\dfrac{p^2}{q^2}') + ' នាំឱ្យ ' + m('p^2=2q^2') + '។ ដូចនេះ ' + m('p^2') + ' ជាចំនួនគូ។'))
    + rvd(3, p(hl('៣.') + ' ការេនៃចំនួនសេសជាចំនួនសេស ដូចនេះ ' + m('p') + ' ជាចំនួនគូ។ តាង ' + m('p=2k') + '។'))
    + rvd(4, p(hl('៤.') + ' ជំនួស៖ ' + m('(2k)^2=2q^2') + ' នាំឱ្យ ' + m('q^2=2k^2') + '។ ដូចនេះ ' + m('q') + ' ក៏ជាចំនួនគូដែរ។'))
    + rvd(5, p(hl('៥.') + ' ' + m('p') + ' និង ' + m('q') + ' ទាំងពីរគូ មានកត្តារួម ' + m('2') + ' ផ្ទុយនឹងការសន្មត។ ដូចនេះ ' + hl('√2 មិនមែនជាចំនួនសនិទានទេ') + '។'))))
S.append(key(K[1], 'វិធីសម្រេចចិត្ត ១–៣', ol([''')

# true / false check at the end of part 1 (before part 2)
sub("S.append(part(2, 'ឫសគូប'))", r'''import math as _m
assert _m.sqrt(9) == 3 and _m.sqrt(16) == 4 and _m.isqrt(5) ** 2 != 5 and abs(1 / 3 - 0.3333333333) < 1e-9
S.append(ex(K[1], 'ពិនិត្យយល់ ៖ ពិត ឬ មិនពិត?', p('ជ្រើសរើសជាមុន (ដោយដៃ ឬក្តារតូច) រួចទើបមើលចម្លើយ។') + tf_rows([
    (m(r'\sqrt{9}=\pm 3'), False, m(r'\sqrt{9}=3')),
    (m('x^2=9') + ' នោះ ' + m(r'x=3') + ' ឬ ' + m('x=-3'), True, ''),
    (m(r'\sqrt{-4}') + ' មានក្នុងចំនួនពិត', False, 'គ្មានចំនួនពិតណាដែលការេអវិជ្ជមាន'),
    (m(r'\sqrt{5}') + ' ជាចំនួនអសនិទាន', True, m('5') + ' មិនមែនជាការេប្រាកដ'),
    (m(r'0.333\ldots') + ' ជាចំនួនសនិទាន', True, m(r'=\dfrac{1}{3}')),
    (m(r'\sqrt{16}') + ' ជាចំនួនអសនិទាន', False, m(r'\sqrt{16}=4')),
])))
S.append(part(2, 'ឫសគូប'))''')

# true / false check on the rules, at the end of part 3.6 (before the exercises)
sub("# ---------------------------------------------------------------- 9. exercises", r'''assert abs(_m.sqrt(2) * _m.sqrt(8) - 4) < 1e-9 and abs(_m.sqrt(9 + 16) - (_m.sqrt(9) + _m.sqrt(16))) > 1
assert abs(3 * _m.sqrt(2) + 4 * _m.sqrt(3) - 7 * _m.sqrt(5)) > 0.1 and abs(_m.sqrt(12) - 2 * _m.sqrt(3)) < 1e-9 and abs(5 / _m.sqrt(5) - _m.sqrt(5)) < 1e-9
S.append(ex('ពិនិត្យយល់', 'ពិត ឬ មិនពិត? (ច្បាប់រ៉ាឌីកាល់)', p('សាកល្បងបំបែកច្បាប់ ដោយគណនាតម្លៃប្រហែលដើម្បីពិនិត្យ។') + tf_rows([
    (m(r'\sqrt{2}\times\sqrt{8}=4'), True, m(r'=\sqrt{16}')),
    (m(r'\sqrt{9+16}=\sqrt{9}+\sqrt{16}'), False, m(r'5\neq 7')),
    (m(r'3\sqrt{2}+4\sqrt{2}=7\sqrt{2}'), True, 'រ៉ាឌីកង់ដូចគ្នា'),
    (m(r'3\sqrt{2}+4\sqrt{3}=7\sqrt{5}'), False, 'រ៉ាឌីកង់ខុសគ្នា បូកមិនបាន'),
    (m(r'\sqrt{12}=2\sqrt{3}'), True, m(r'=\sqrt{4\times 3}')),
    (m(r'\sqrt{x^2}=x') + ' ចំពោះគ្រប់ ' + m('x'), False, m(r'\sqrt{x^2}=|x|')),
])))

# ---------------------------------------------------------------- 9. exercises''')

# exit ticket, before the summary
sub("S.append(key('សង្ខេប', 'សេចក្តីសង្ខេប ១', ul([", r'''assert _m.isqrt(49) == 7 and round(-27 ** (1 / 3) if False else -3) == -3 and 48 == 16 * 3 and abs(2 * _m.sqrt(5) + _m.sqrt(45) - 5 * _m.sqrt(5)) < 1e-9 and abs(6 / _m.sqrt(3) - 2 * _m.sqrt(3)) < 1e-9
S.append(ex('សំបុត្រចេញ', 'ពិនិត្យយល់ចុងក្រោយ (Exit ticket)', p('សរសេរចម្លើយលើក្រដាសតូច ហើយប្រគល់ជូនគ្រូមុនចេញ។') + ''.join(
    f'<div style="display:grid;grid-template-columns:1.2fr 1fr;gap:1em;align-items:center;margin:.3em 0"><div><b>{i}.</b> {q}</div>{rvd(i, a)}</div>' for i, (q, a) in enumerate([
        ('គណនា ' + m(r'\sqrt{49}') + ' និង ' + m(r'\sqrt[3]{-27}'), m(r'7') + ' និង ' + m('-3')),
        ('បញ្ចេញ ' + m(r'\sqrt{48}'), m(r'\sqrt{16\times 3}=4\sqrt{3}')),
        ('សម្រួល ' + m(r'2\sqrt{5}+\sqrt{45}'), m(r'2\sqrt{5}+3\sqrt{5}=5\sqrt{5}')),
        ('បំបាត់រ៉ាឌីកាល់ពីភាគបែង ' + m(r'\dfrac{6}{\sqrt{3}}'), m(r'\dfrac{6\sqrt{3}}{3}=2\sqrt{3}')),
        (m(r'\sqrt{20}') + ' ជាចំនួនសនិទាន ឬអសនិទាន? ហេតុអ្វី?', 'អសនិទាន ព្រោះ ' + m('20') + ' មិនមែនជាការេប្រាកដ'),
    ], 1))))
S.append(key('សង្ខេប', 'សេចក្តីសង្ខេប ១', ul([''')

open(pb, 'w', encoding='utf-8').write(s)
open(pv, 'w', encoding='utf-8').write(v)
print('patched 2')
