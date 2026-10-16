from lib import *
from fractions import Fraction as F
LESSON = 'ចំនួនសនិទាន'

# ---------- helpers: every number is computed with Fraction ----------
def fr(f):                      # \dfrac form, no \( \)
    f = F(f); return frac(f)
def mx(f):                      # mixed number, e.g. -3\dfrac{1}{2}
    f = F(f)
    if f.denominator == 1: return str(f.numerator)
    w, r = divmod(abs(f.numerator), f.denominator)
    s = '-' if f < 0 else ''
    if w == 0: return s + f'\\dfrac{{{r}}}{{{f.denominator}}}'
    return s + f'{w}\\dfrac{{{r}}}{{{f.denominator}}}'
def Mf(f): return M(fr(f))
def Mm(f): return M(mx(f))
def terminating(f):
    d = F(f).denominator
    for p in (2, 5):
        while d % p == 0: d //= p
    return d == 1
def dec(f):                     # exact terminating decimal as text
    f = F(f); assert terminating(f)
    n, d = f.numerator, f.denominator
    k = 0
    while d != 1 and (10 ** k) % d: k += 1
    v = n * (10 ** k) // d
    s = str(abs(v)).rjust(k + 1, '0')
    s = (s[:-k] + '.' + s[-k:]) if k else s
    return ('-' if f < 0 else '') + s
def rep(whole, nonrep, period):  # 0.1\overline{6}
    return f'{whole}.{nonrep}\\overline{{{period}}}'
def rep_to_frac(whole, nonrep, period):
    # whole.nonrep(period) as a fraction
    a, b = len(nonrep), len(period)
    nr = int(nonrep) if nonrep else 0
    pr = int(period)
    num_all = int((nonrep or '') + period) - nr
    return F(whole) + F(num_all, (10 ** b - 1) * 10 ** a)
def uniq(ans, cand, fmt, k=3, fill=None):
    """k distinct wrong answers (different in VALUE from ans); fill with small shifts."""
    out = []
    for c in cand:
        c = F(c)
        if c != F(ans) and c not in out: out.append(c)
    d = 1
    while len(out) < k:
        base = (fill or (lambda i: F(ans) + F(i, 7)))(d); d += 1
        if base != F(ans) and base not in out: out.append(base)
    return [fmt(c) for c in out[:k]]
def Wf(ans, cand, k=3): return uniq(ans, cand, Mf, k)
def Wm(ans, cand, k=3): return uniq(ans, cand, Mm, k)

def cands():
    C = []
    # ===================== 1. សញ្ញាណចំនួនសនិទាន =====================
    C.append(mcq('easy', 'concept', 'ចំនួនសនិទានមានទម្រង់ ' + M('\\dfrac{a}{b}') + ' ដែល ' + M('a') + ' និង ' + M('b') + ' ជាចំនួនគត់រ៉ឺឡាទីប។ លក្ខខណ្ឌដែលត្រូវតែមានចំពោះ ' + M('b') + ' គឺ៖', M('b \\neq 0'), [M('b > 0'), M('b = 1'), M('b \\neq 1')], 'ភាគបែងមិនអាចស្មើសូន្យបានទេ។'))
    C.append(mcq('easy', 'concept', 'ចំនួនណាមួយខាងក្រោមមិនមែនជាចំនួនសនិទាន ព្រោះភាគបែងស្មើ ' + M(0) + '?', M('\\dfrac{5}{0}'), [M('\\dfrac{0}{5}'), M('\\dfrac{-5}{1}'), M('\\dfrac{5}{-1}')], M('\\dfrac{5}{0}') + ' គ្មានន័យ។'))
    C.append(mcq('easy', 'concept', 'ក្នុងចំនួនខាងក្រោម ចំនួនណាមិនមែនជាចំនួនសនិទាន?', M('\\dfrac{3}{0}'), [M('-3'), M('0.5'), M('2\\dfrac{1}{4}')], 'ចំនួនសនិទានអាចជាចំនួនគត់ ទសភាគ ឬចំនួនចម្រុះ ប៉ុន្តែភាគបែងមិនអាចជា ' + M(0) + '។'))
    C.append(mcq('easy', 'concept', M('\\dfrac{5}{1}') + ' ស្មើនឹង៖', M(5), [M('\\dfrac{1}{5}'), M('-5'), M('0.5')], 'ភាគបែងស្មើ ' + M(1) + ' ចំនួនសនិទានស្មើនឹងចំនួនគត់ភាគយក។'))
    C.append(mcq('easy', 'concept', 'សរសេរ ' + M('\\dfrac{2}{10}') + ' ជាចំនួនទសភាគ៖', M('0.2'), [M('2.10'), M('0.02'), M('20')], M('\\dfrac{2}{10} = 0.2') + '។'))
    C.append(mcq('easy', 'concept', 'សរសេរ ' + M('\\dfrac{-3}{100}') + ' ជាចំនួនទសភាគ៖', M('-0.03'), [M('-0.3'), M('0.03'), M('-3.100')], M('\\dfrac{-3}{100} = -0.03') + '។'))
    C.append(mcq('easy', 'concept', 'សរសេរ ' + M('\\dfrac{7}{3}') + ' ជាចំនួនចម្រុះ៖', Mm(F(7, 3)), [Mm(F(3, 7)), M('3\\dfrac{1}{3}'), M('1\\dfrac{2}{3}')], M('7 \\div 3 = 2') + ' សល់ ' + M(1) + '។'))
    C.append(mcq('easy', 'concept', 'សរសេរ ' + M('\\dfrac{-13}{4}') + ' ជាចំនួនចម្រុះ៖', Mm(F(-13, 4)), [M('-4\\dfrac{1}{4}'), M('-3\\dfrac{3}{4}'), M('3\\dfrac{1}{4}')], M('13 \\div 4 = 3') + ' សល់ ' + M(1) + '។'))
    C.append(mcq('easy', 'concept', M('\\dfrac{1}{3}') + ' ជាចំនួនទសភាគខួប ដែលសរសេរបាន៖', M('0.\\overline{3}'), [M('0.3'), M('0.33'), M('0.\\overline{03}')], M('1 \\div 3 = 0.333\\ldots') + '។'))
    C.append(mcq('easy', 'concept', 'ក្នុងចំនួនខាងក្រោម ចំនួនណាស្មើនឹង ' + M('\\dfrac{1}{2}') + '?', M('\\dfrac{5}{10}'), [M('\\dfrac{2}{1}'), M('\\dfrac{1}{5}'), M('\\dfrac{2}{4} + 1')], M('\\dfrac{5}{10} = \\dfrac{1}{2}') + '។'))
    C.append(mcq('easy', 'concept', 'បើ ' + M('\\dfrac{a}{b} = \\dfrac{c}{d}') + ' នោះផលគុណខ្វែងគឺ៖', M('ad = bc'), [M('ab = cd'), M('ac = bd'), M('a + d = b + c')], 'ផលគុណខ្វែងស្មើគ្នា។'))
    C.append(mcq('easy', 'concept', 'ចំនួនសនិទាន ' + M('0.5') + ' ស្មើនឹងប្រភាគ៖', Mf(F(1, 2)), [Mf(F(1, 5)), Mf(F(5, 1)), Mf(F(5, 100))], M('0.5 = \\dfrac{5}{10} = \\dfrac{1}{2}') + '។'))
    C.append(mcq('easy', 'concept', M('6 \\div 3 = 2') + ' ប៉ុន្តែ ' + M('3 \\div 6') + ' ស្មើនឹង៖', Mf(F(1, 2)), [M('2'), M('-2'), M('\\dfrac{6}{3}')], M('3 \\div 6 = \\dfrac{3}{6} = \\dfrac{1}{2}') + ' ជាចំនួនសនិទាន។'))
    # equal fractions: solve for x
    for n, mixed, x in ((45, F(15, 2), 6), (28, F(7, 2), 8), (36, F(9, 2), 8), (30, F(5, 3), 18)):
        ans = F(n) / mixed
        C.append(mcq('medium', 'equal', 'កំណត់ ' + M('x') + ' ដើម្បីឱ្យ ' + M(f'\\dfrac{{{n}}}{{x}}') + ' ស្មើនឹង ' + Mm(mixed) + '៖', M(int(ans)), [M(int(ans) + 2), M(int(ans) - 2), M(int(ans) * 2)],
                      M(f'\\dfrac{{{n}}}{{x}} = {mx(mixed)} = {fr(mixed)}') + ' នាំឱ្យ ' + M(f'x = {n} \\times {mixed.denominator} \\div {mixed.numerator} = {int(ans)}') + '។'))
    for a, b, c in ((3, 4, 21), (5, 6, 35), (2, 9, 14)):
        ans = F(c * b, a)           # a/b = c/x  -> x = cb/a
        C.append(mcq('medium', 'equal', 'បើ ' + M(f'\\dfrac{{{a}}}{{{b}}} = \\dfrac{{{c}}}{{x}}') + ' នោះ ' + M('x') + ' ស្មើ៖', M(mx(ans)), uniq(ans, [F(c * a, b), ans + 1, ans - 1], lambda v: M(mx(v))),
                      M(f'{a}x = {b} \\times {c}') + ' នាំឱ្យ ' + M(f'x = {mx(ans)}') + '។'))
    C.append(mcq('medium', 'equal', 'កំណត់ ' + M('x, y') + ' ដើម្បីឱ្យ ' + M('\\dfrac{-2}{x}, \\dfrac{y}{5}, -0.2') + ' មានតម្លៃស្មើគ្នា។', M('x = 10,\\ y = -1'), [M('x = -10,\\ y = 1'), M('x = 10,\\ y = 1'), M('x = 5,\\ y = -2')], M('-0.2 = \\dfrac{-1}{5}') + ' ដូចនេះ ' + M('\\dfrac{y}{5} = \\dfrac{-1}{5}') + ' ហើយ ' + M('\\dfrac{-2}{x} = \\dfrac{-2}{10}') + '។'))
    C.append(mcq('medium', 'equal', 'ក្នុងចំនួនខាងក្រោម ក្រុមណាស្មើគ្នាទាំងអស់?', M('-3\\dfrac{1}{2},\\ \\dfrac{-14}{4},\\ -3.5'), [M('-3\\dfrac{1}{2},\\ \\dfrac{14}{4},\\ 3.5'), M('\\dfrac{21}{6},\\ \\dfrac{-14}{4},\\ -3.5'), M('-3\\dfrac{1}{2},\\ \\dfrac{-14}{4},\\ -2.5')], M('-3\\dfrac{1}{2} = \\dfrac{-7}{2} = \\dfrac{-14}{4} = -3.5') + '។'))
    # ===================== 2. ប្រៀបធៀប និងរៀបលំដាប់ =====================
    C.append(mcq('easy', 'compare', 'ចំនួនណាតូចជាង៖ ' + M('-5') + ' ឬ ' + M('-1') + '?', M('-5'), [M('-1'), M('0'), M('1')], 'នៅលើបន្ទាត់ចំនួន ' + M('-5') + ' នៅខាងឆ្វេងនៃ ' + M('-1') + '។'))
    C.append(mcq('easy', 'compare', 'ប្រៀបធៀប ' + M('\\dfrac{1}{4}') + ' និង ' + M('\\dfrac{3}{4}') + '។ ចម្លើយត្រូវគឺ៖', M('\\dfrac{1}{4} < \\dfrac{3}{4}'), [M('\\dfrac{1}{4} > \\dfrac{3}{4}'), M('\\dfrac{1}{4} = \\dfrac{3}{4}'), M('\\dfrac{1}{4} = -\\dfrac{3}{4}')], 'ភាគបែងស្មើគ្នា ' + M('1 < 3') + '។'))
    C.append(mcq('easy', 'compare', 'ប្រៀបធៀប ' + M('-21') + ' និង ' + M('-3') + '៖', M('-21 < -3'), [M('-21 > -3'), M('-21 = -3'), M('21 < -3')], 'ចំនួនអវិជ្ជមានដែលមានតម្លៃដាច់ខាតធំជាង គឺតូចជាង។'))
    for (p, q) in ((F(6, 11), F(7, 12)), (F(5, 9), F(4, 7)), (F(8, 13), F(5, 8)), (F(-5, 7), F(-3, 4))):
        big = max(p, q); small = min(p, q)
        cp = f'{p.numerator}\\times{q.denominator} = {p.numerator * q.denominator}'
        cq = f'{q.numerator}\\times{p.denominator} = {q.numerator * p.denominator}'
        C.append(mcq('medium', 'compare', 'ក្នុងចំនួន ' + Mf(p) + ' និង ' + Mf(q) + ' ចំនួនណាធំជាង?', Mf(big), [Mf(small), M('\\text{ស្មើគ្នា}'), M('\\text{ប្រៀបធៀបមិនបាន}')],
                      'ផលគុណខ្វែង ' + M(cp) + ' ; ' + M(cq) + '។'))
    for p, q in ((F(1, 2), F(2, 3)), (F(3, 4), F(5, 6)), (F(3, 5), F(7, 10))):
        pass
    C.append(mcq('medium', 'compare', 'រៀបចំនួន ' + Mf(F(3, 4)) + ', ' + Mf(F(5, 6)) + ', ' + Mf(F(8, 9)) + ' តាមលំដាប់កើន (ពីតូចទៅធំ)៖', M('\\dfrac{3}{4} < \\dfrac{5}{6} < \\dfrac{8}{9}'), [M('\\dfrac{8}{9} < \\dfrac{5}{6} < \\dfrac{3}{4}'), M('\\dfrac{5}{6} < \\dfrac{3}{4} < \\dfrac{8}{9}'), M('\\dfrac{3}{4} < \\dfrac{8}{9} < \\dfrac{5}{6}')],
                  M('\\dfrac{27}{36} < \\dfrac{30}{36} < \\dfrac{32}{36}') + ' (ភាគបែងរួម ' + M(36) + ')។'))
    C.append(mcq('medium', 'compare', 'រៀបចំនួន ' + Mf(F(2, 5)) + ', ' + Mf(F(3, 8)) + ', ' + Mf(F(1, 3)) + ' តាមលំដាប់ចុះ (ពីធំទៅតូច)៖', M('\\dfrac{2}{5} > \\dfrac{3}{8} > \\dfrac{1}{3}'), [M('\\dfrac{1}{3} > \\dfrac{3}{8} > \\dfrac{2}{5}'), M('\\dfrac{3}{8} > \\dfrac{2}{5} > \\dfrac{1}{3}'), M('\\dfrac{2}{5} > \\dfrac{1}{3} > \\dfrac{3}{8}')],
                  M('\\dfrac{48}{120} > \\dfrac{45}{120} > \\dfrac{40}{120}') + ' (ភាគបែងរួម ' + M(120) + ')។'))
    C.append(mcq('medium', 'compare', 'ក្នុងចំនួន ' + Mf(F(2, 5)) + ', ' + Mf(F(1, 2)) + ', ' + Mf(F(4, 9)) + ' ចំនួនណាធំជាងគេ?', Mf(F(1, 2)), [Mf(F(2, 5)), Mf(F(4, 9)), M('\\text{ស្មើគ្នាទាំងអស់}')], M('\\dfrac{36}{90}, \\dfrac{45}{90}, \\dfrac{40}{90}') + ' (ភាគបែងរួម ' + M(90) + ')។'))
    C.append(mcq('medium', 'compare', 'ក្នុងចំនួន ' + Mf(F(5, 6)) + ', ' + Mf(F(3, 5)) + ', ' + Mf(F(2, 9)) + ' ចំនួនណាតូចជាងគេ?', Mf(F(2, 9)), [Mf(F(5, 6)), Mf(F(3, 5)), M('\\text{ស្មើគ្នាទាំងអស់}')], M('\\dfrac{75}{90}, \\dfrac{54}{90}, \\dfrac{20}{90}') + '។'))
    C.append(mcq('medium', 'compare', 'ប្រៀបធៀប ' + M('0.54') + ' និង ' + M('0.5398') + '៖', M('0.54 > 0.5398'), [M('0.54 < 0.5398'), M('0.54 = 0.5398'), M('0.54 \\leq 0.5398')], M('0.5400 > 0.5398') + '។'))
    C.append(mcq('hard', 'compare', 'ប្រៀបធៀប ' + M('-1\\dfrac{10}{12}') + ' និង ' + M('-1\\dfrac{9}{13}') + '៖', M('-1\\dfrac{10}{12} < -1\\dfrac{9}{13}'), [M('-1\\dfrac{10}{12} > -1\\dfrac{9}{13}'), M('-1\\dfrac{10}{12} = -1\\dfrac{9}{13}'), M('1\\dfrac{10}{12} < -1\\dfrac{9}{13}')],
                  M('1\\dfrac{10}{12} = \\dfrac{11}{6} \\approx 1.83 > \\dfrac{22}{13} \\approx 1.69') + ' ដូច្នេះចំនួនអវិជ្ជមានមានតម្លៃតូចជាង។'))
    C.append(mcq('hard', 'compare', 'រៀបចំនួន ' + M('\\dfrac{1}{8}, -\\dfrac{9}{7}, -1, 0.28, 1\\dfrac{2}{5}') + ' ពីតូចទៅធំ៖', M('-\\dfrac{9}{7} < -1 < \\dfrac{1}{8} < 0.28 < 1\\dfrac{2}{5}'), [M('-1 < -\\dfrac{9}{7} < \\dfrac{1}{8} < 0.28 < 1\\dfrac{2}{5}'), M('-\\dfrac{9}{7} < -1 < 0.28 < \\dfrac{1}{8} < 1\\dfrac{2}{5}'), M('-\\dfrac{9}{7} < \\dfrac{1}{8} < -1 < 0.28 < 1\\dfrac{2}{5}')],
                  M('-1.29 < -1 < 0.125 < 0.28 < 1.4') + '។'))
    C.append(mcq('hard', 'compare', 'រៀបចំនួន ' + M('\\dfrac{4}{3}, 0.3, -0.25, \\dfrac{5}{4}') + ' ពីតូចទៅធំ៖', M('-0.25 < 0.3 < \\dfrac{5}{4} < \\dfrac{4}{3}'), [M('-0.25 < 0.3 < \\dfrac{4}{3} < \\dfrac{5}{4}'), M('0.3 < -0.25 < \\dfrac{5}{4} < \\dfrac{4}{3}'), M('\\dfrac{4}{3} < \\dfrac{5}{4} < 0.3 < -0.25')],
                  'ភាគបែងរួម ' + M(120) + ' ៖ ' + M('\\dfrac{160}{120}, \\dfrac{36}{120}, -\\dfrac{30}{120}, \\dfrac{150}{120}') + '។'))
    C.append(mcq('hard', 'compare', 'ចំនួនសនិទានមួយណាស្ថិតនៅចន្លោះ ' + Mf(F(1, 3)) + ' និង ' + Mf(F(1, 2)) + '?', Mf(F(2, 5)), [Mf(F(3, 5)), Mf(F(1, 4)), Mf(F(5, 9) + F(1, 10))], M('\\dfrac{1}{3} \\approx 0.333 < \\dfrac{2}{5} = 0.4 < \\dfrac{1}{2} = 0.5') + '។'))
    # ===================== 3. សរសេរទម្រង់ផ្សេងៗ =====================
    for x, ans in ((F(2845, 100), F(569, 20)), (F(1378, 1000), F(689, 500)), (F(138, 100), F(69, 50)), (F(125, 1000), F(1, 8))):
        d = dec(x)
        C.append(mcq('easy' if x == F(1, 8) else 'medium', 'convert', 'សរសេរ ' + M(d) + ' ជាប្រភាគសម្រួលរួច៖', Mf(ans), uniq(ans, [x, ans * 2, ans + F(1, 10), F(ans.denominator, ans.numerator)], Mf),
                      M(f'{d} = \\dfrac{{{x.numerator * (10 ** len(d.split(".")[1])) // x.denominator if False else int(d.replace(".", ""))}}}{{{10 ** len(d.split(".")[1])}}} = {fr(ans)}') + '។'))
    for f in (F(3, 16), F(7, 40), F(17, 625), F(3, 8)):
        d = dec(f)
        C.append(mcq('medium', 'convert', 'សរសេរ ' + Mf(f) + ' ជាចំនួនទសភាគ៖', M(d), [M(dec(f * 2)), M(dec(f / 2)), M(dec(f * 10))], M(f'\\dfrac{{{f.numerator}}}{{{f.denominator}}} = {d}') + '។'))
    for (w, nr, pr) in ((0, '', '4'), (0, '', '27'), (0, '', '15'), (1, '', '3')):
        v = rep_to_frac(w, nr, pr); txt = rep(w, nr, pr)
        C.append(mcq('medium', 'repeat', 'សរសេរ ' + M(txt) + ' ជាប្រភាគសម្រួលរួច៖', Mf(v), uniq(v, [F(int(pr), 10 ** len(pr)), F(int(pr), 100), v + 1, F(int(pr), 10 ** len(pr) - 1) * 2], Mf),
                      'ប្រើ ' + M(f'{int(pr)} \\div {"9" * len(pr)}') + (' បូកផ្នែកគត់ ' + M(w) if w else '') + '។'))
    C.append(mcq('hard', 'repeat', 'សរសេរ ' + M('0.1\\overline{6}') + ' ជាប្រភាគសម្រួលរួច៖', Mf(F(1, 6)), [Mf(F(16, 99)), Mf(F(16, 100)), Mf(F(1, 60))], M('x = 0.1666\\ldots') + ' ; ' + M('100x - 10x = 16 - 1 = 15') + ' នាំឱ្យ ' + M('x = \\dfrac{15}{90} = \\dfrac{1}{6}') + '។'))
    C.append(mcq('hard', 'repeat', 'សរសេរ ' + M('0.\\overline{3} + 0.\\overline{6}') + ' ជាចំនួនសនិទាន៖', M(1), [Mf(F(9, 10)), Mf(F(1, 3)), Mf(F(99, 100))], M('\\dfrac{1}{3} + \\dfrac{2}{3} = 1') + '។'))
    C.append(mcq('hard', 'repeat', 'ក្នុងប្រភាគខាងក្រោម ប្រភាគមួយណាសរសេរជាចំនួនទសភាគដាច់ (មិនខួប) បាន?', Mf(F(7, 40)), [Mf(F(1, 3)), Mf(F(5, 6)), Mf(F(4, 7))], M('40 = 2^3 \\times 5') + ' មានតែកត្តាបឋម ' + M(2) + ' និង ' + M(5) + '។'))
    C.append(mcq('easy', 'repeat', 'ចំនួនណាជាចំនួនទសភាគខួប?', M('1.\\overline{3}'), [M('1.3'), M('1.30'), M('0.25')], 'ខ្ទង់ ' + M(3) + ' ដដែលៗជានិច្ច។'))
    # ===================== 4. ប្រមាណវិធីបូក ដក =====================
    C.append(mcq('easy', 'add', 'គណនា ' + M('\\dfrac{3}{8} + \\dfrac{1}{8}') + '៖', Mf(F(1, 2)), [Mf(F(3, 16)), Mf(F(1, 4)), Mf(F(3, 4))], M('\\dfrac{3+1}{8} = \\dfrac{4}{8} = \\dfrac{1}{2}') + '។'))
    C.append(mcq('easy', 'add', 'ចំនួនផ្ទុយនៃ ' + M('-\\dfrac{3}{5}') + ' គឺ៖', Mf(F(3, 5)), [Mf(F(-3, 5)), Mf(F(5, 3)), Mf(F(-5, 3))], 'ចំនួនផ្ទុយមានផលបូកស្មើ ' + M(0) + '។'))
    C.append(mcq('easy', 'add', 'គណនា ' + M('\\dfrac{9}{10} - \\dfrac{7}{10}') + '៖', Mf(F(1, 5)), [Mf(F(16, 10)), Mf(F(2, 20)), Mf(F(1, 2))], M('\\dfrac{2}{10} = \\dfrac{1}{5}') + '។'))
    for a, b in ((F(5, 4), F(7, 8)), (F(3, 5), F(7, 10)), (F(-5, 6), F(-7, 3)), (F(-5, 24), F(7, 30))):
        pass
    C.append(mcq('medium', 'add', 'គណនា ' + M('\\dfrac{5}{4} - \\dfrac{7}{8}') + '៖', Mf(F(3, 8)), [Mf(F(-3, 8)), Mf(F(2, 4)), Mf(F(12, 12))], M('\\dfrac{10-7}{8} = \\dfrac{3}{8}') + '។'))
    C.append(mcq('medium', 'add', 'គណនា ' + M('\\dfrac{3}{5} - \\dfrac{7}{10}') + '៖', Mf(F(-1, 10)), [Mf(F(1, 10)), Mf(F(-4, 5)), Mf(F(13, 10))], M('\\dfrac{6-7}{10} = -\\dfrac{1}{10}') + '។'))
    C.append(mcq('medium', 'add', 'គណនា ' + M('-\\dfrac{5}{6} - \\left(-\\dfrac{7}{3}\\right)') + '៖', Mf(F(3, 2)), [Mf(F(-19, 6)), Mf(F(19, 6)), Mf(F(2, 3))], M('\\dfrac{-5+14}{6} = \\dfrac{9}{6} = \\dfrac{3}{2}') + '។'))
    C.append(mcq('medium', 'add', 'គណនា ' + M('\\left(\\dfrac{5}{6} + \\dfrac{7}{3}\\right) + \\dfrac{5}{3}') + '៖', Mf(F(29, 6)), [Mf(F(17, 6)), Mf(F(5, 4)), Mf(F(29, 12))], 'ប្រើលក្ខណៈផ្តុំ ៖ ' + M('\\dfrac{5}{6} + 4 = \\dfrac{29}{6}') + '។'))
    C.append(mcq('hard', 'add', 'គណនា ' + M('-\\dfrac{5}{24} - \\dfrac{7}{30}') + '៖', Mf(F(-53, 120)), [Mf(F(-12, 54)), Mf(F(3, 120)), Mf(F(-53, 54))], M('\\text{LCM}(24, 30) = 120') + ' ៖ ' + M('\\dfrac{-25-28}{120} = -\\dfrac{53}{120}') + '។'))
    C.append(mcq('hard', 'add', 'គណនា ' + M('\\dfrac{1}{15} - \\dfrac{27}{50}') + '៖', Mf(F(-71, 150)), [Mf(F(71, 150)), Mf(F(-26, 35)), Mf(F(-27, 750))], M('\\text{LCM}(15, 50) = 150') + ' ៖ ' + M('\\dfrac{10-81}{150} = -\\dfrac{71}{150}') + '។'))
    C.append(mcq('medium', 'add', 'គណនា ' + M('2\\dfrac{5}{8} + \\left(-1\\dfrac{1}{8}\\right) + 3\\dfrac{7}{8}') + '៖', Mm(F(43, 8)), [Mm(F(11, 8)), Mm(F(31, 8)), Mm(F(57, 8))], M('\\dfrac{21}{8} - \\dfrac{9}{8} + \\dfrac{31}{8} = \\dfrac{43}{8}') + '។'))
    C.append(mcq('hard', 'add', 'គណនា ' + M('-\\dfrac{1}{8} + 2\\dfrac{5}{9}') + '៖', Mm(F(175, 72)), [Mm(F(-175, 72)), Mm(F(193, 72)), Mm(F(23, 72))], M('-\\dfrac{9}{72} + \\dfrac{184}{72} = \\dfrac{175}{72}') + '។'))
    C.append(mcq('hard', 'add', 'គណនា ' + M('-3\\dfrac{1}{8} - \\left(-2\\dfrac{5}{9}\\right)') + '៖', Mf(F(-41, 72)), [Mf(F(41, 72)), Mf(F(-409, 72)), Mf(F(-1, 72))], M('-\\dfrac{25}{8} + \\dfrac{23}{9} = \\dfrac{-225+184}{72}') + '។'))
    C.append(mcq('medium', 'property', M('\\dfrac{a}{b} + \\dfrac{c}{d} = \\dfrac{c}{d} + \\dfrac{a}{b}') + ' ជាលក្ខណៈ៖', 'ត្រឡប់', ['ផ្តុំ', 'បំបែក', 'ចំនួនផ្ទុយ'], 'ដូរលំដាប់ត្ណាប់ ផលបូកមិនប្រែ។'.replace('ត្ណាប់', 'ត្ថាប់') if False else 'ដូរលំដាប់ពាក្យ ផលបូកមិនប្រែ។'))
    C.append(mcq('medium', 'property', M('\\left(\\dfrac{a}{b} + \\dfrac{c}{d}\\right) + \\dfrac{e}{f} = \\dfrac{a}{b} + \\left(\\dfrac{c}{d} + \\dfrac{e}{f}\\right)') + ' ជាលក្ខណៈ៖', 'ផ្តុំ', ['ត្រឡប់', 'បំបែក', 'ចំនួនច្រាស'], 'ប្តូរការដាក់ដង្កៀប ផលបូកមិនប្រែ។'))
    C.append(mcq('medium', 'property', M('\\dfrac{a}{b}\\left(\\dfrac{c}{d} + \\dfrac{e}{f}\\right) = \\dfrac{a}{b}\\cdot\\dfrac{c}{d} + \\dfrac{a}{b}\\cdot\\dfrac{e}{f}') + ' ជាលក្ខណៈ៖', 'បំបែកនៃវិធីគុណចំពោះវិធីបូក', ['ត្រឡប់នៃវិធីគុណ', 'ផ្តុំនៃវិធីបូក', 'ចំនួនផ្ទុយ'], 'ជាលក្ខណៈបំបែក។'))
    # ===================== 5. គុណ ចែក =====================
    C.append(mcq('easy', 'mul', 'ចំនួនច្រាសនៃ ' + Mf(F(3, 7)) + ' គឺ៖', Mf(F(7, 3)), [Mf(F(-3, 7)), Mf(F(3, 7)), Mf(F(-7, 3))], M('\\dfrac{3}{7} \\cdot \\dfrac{7}{3} = 1') + '។'))
    C.append(mcq('easy', 'mul', 'ផលគុណនៃចំនួនសនិទានអវិជ្ជមានពីរ ជាចំនួន៖', 'វិជ្ជមាន', ['អវិជ្ជមាន', 'សូន្យ', 'មិនអាចដឹងបាន'], 'សញ្ញាដូចគ្នា ផលគុណវិជ្ជមាន។'))
    C.append(mcq('medium', 'mul', 'គណនា ' + M('\\left(-\\dfrac{2}{3}\\right)\\left(-\\dfrac{7}{15}\\right)') + '៖', Mf(F(14, 45)), [Mf(F(-14, 45)), Mf(F(5, 18)), Mf(F(-9, 18))], M('\\dfrac{(-2)(-7)}{3 \\times 15} = \\dfrac{14}{45}') + '។'))
    C.append(mcq('medium', 'mul', 'គណនា ' + M('\\dfrac{3}{8} \\times 3.8') + '៖', Mf(F(57, 40)), [Mf(F(57, 20)), Mf(F(57, 400)), Mf(F(3, 30))], M('\\dfrac{3}{8} \\times \\dfrac{38}{10} = \\dfrac{114}{80} = \\dfrac{57}{40}') + '។'))
    C.append(mcq('medium', 'mul', 'គណនា ' + M('\\dfrac{7}{5}\\cdot\\dfrac{9}{4} + \\dfrac{7}{5}\\cdot\\dfrac{11}{4}') + '៖', M(7), [M(5), Mf(F(63, 20)), Mf(F(140, 20) + 1)], M('\\dfrac{7}{5}\\left(\\dfrac{9+11}{4}\\right) = \\dfrac{7}{5} \\times 5 = 7') + '។'))
    C.append(mcq('hard', 'mul', 'គណនា ' + M('0.75 \\times \\dfrac{13}{125}') + '៖', Mf(F(39, 500)), [Mf(F(39, 50)), Mf(F(13, 500)), Mf(F(13, 166))], M('\\dfrac{3}{4} \\times \\dfrac{13}{125} = \\dfrac{39}{500}') + '។'))
    C.append(mcq('hard', 'mul', 'គណនា ' + M('5\\dfrac{3}{4} \\times \\dfrac{12}{125}') + '៖', Mf(F(69, 125)), [Mf(F(60, 125)), Mf(F(69, 500)), Mf(F(23, 125))], M('\\dfrac{23}{4} \\times \\dfrac{12}{125} = \\dfrac{69}{125}') + '។'))
    C.append(mcq('hard', 'mul', 'គណនា ' + M('\\left(-\\dfrac{1}{3}\\right)\\left(\\dfrac{3}{5}\\right)(0.5)(0.2)') + '៖', Mf(F(-1, 50)), [Mf(F(1, 50)), Mf(F(-1, 5)), Mf(F(-3, 50))], M('-\\dfrac{1}{5} \\times 0.1 = -\\dfrac{1}{50}') + '។'))
    C.append(mcq('medium', 'div', 'គណនា ' + M('\\dfrac{4}{5} \\div \\dfrac{1}{10}') + '៖', M(8), [Mf(F(2, 25)), M(40), Mf(F(1, 8))], M('\\dfrac{4}{5} \\times 10 = 8') + '។'))
    C.append(mcq('medium', 'div', 'គណនា ' + M('-\\dfrac{3}{5} \\div 2\\dfrac{3}{10}') + '៖', Mf(F(-6, 23)), [Mf(F(6, 23)), Mf(F(-23, 6)), Mf(F(-3, 23))], M('-\\dfrac{3}{5} \\times \\dfrac{10}{23} = -\\dfrac{6}{23}') + '។'))
    C.append(mcq('medium', 'div', 'គណនា ' + M('\\dfrac{24}{-25} \\div \\dfrac{6}{15}') + '៖', Mf(F(-12, 5)), [Mf(F(12, 5)), Mf(F(-5, 12)), Mf(F(-24, 5))], M('\\dfrac{24}{-25} \\times \\dfrac{15}{6} = -\\dfrac{12}{5}') + '។'))
    C.append(mcq('hard', 'div', 'គណនា ' + M('\\dfrac{28}{27} \\div \\dfrac{-4}{51}') + '៖', Mf(F(-119, 9)), [Mf(F(119, 9)), Mf(F(-112, 51)), Mf(F(-17, 9))], M('\\dfrac{28}{27} \\times \\dfrac{51}{-4} = -\\dfrac{7 \\times 17}{9} = -\\dfrac{119}{9}') + '។'))
    C.append(mcq('hard', 'div', 'គណនា ' + M('\\dfrac{40}{-27} \\div \\dfrac{-10}{9}') + '៖', Mm(F(4, 3)), [Mm(F(-4, 3)), Mm(F(400, 243)), Mm(F(3, 4))], M('\\dfrac{40}{27} \\times \\dfrac{9}{10} = \\dfrac{4}{3}') + '។'))
    C.append(mcq('medium', 'div', 'គណនា ' + M('154.63 \\div 4.7') + '៖', M('32.9'), [M('3.29'), M('329'), M('33.9')], M('1546.3 \\div 47 = 32.9') + '។'))
    # ===================== 6. កន្សោមចម្រុះ =====================
    C.append(mcq('medium', 'mixed', 'គណនា ' + M('\\left(\\dfrac{1}{2} - \\dfrac{1}{3}\\right) \\div \\dfrac{5}{8}') + '៖', Mf(F(4, 15)), [Mf(F(5, 48)), Mf(F(15, 4)), Mf(F(1, 6))], M('\\dfrac{1}{6} \\times \\dfrac{8}{5} = \\dfrac{8}{30} = \\dfrac{4}{15}') + '។'))
    C.append(mcq('hard', 'mixed', 'គណនា ' + M('\\left(\\dfrac{1}{2} + \\dfrac{1}{3}\\right) \\div \\left(\\dfrac{5}{8} - \\dfrac{1}{4}\\right)') + '៖', Mm(F(20, 9)), [Mm(F(9, 20)), Mm(F(5, 18)), Mm(F(40, 9))], M('\\dfrac{5}{6} \\div \\dfrac{3}{8} = \\dfrac{5}{6} \\times \\dfrac{8}{3} = \\dfrac{20}{9}') + '។'))
    C.append(mcq('hard', 'mixed', 'គណនា ' + M('\\dfrac{3\\frac{2}{5} - \\frac{25}{8}}{\\frac{7}{12} + 5\\frac{4}{9}}') + '៖', Mf(F(99, 2170)), [Mf(F(11, 40)), Mf(F(217, 36)), Mf(F(2170, 99))], 'ភាគយក ' + M('\\dfrac{11}{40}') + ' ភាគបែង ' + M('\\dfrac{217}{36}') + ' ៖ ' + M('\\dfrac{11}{40} \\times \\dfrac{36}{217} = \\dfrac{99}{2170}') + '។'))
    C.append(mcq('hard', 'mixed', 'គណនា ' + M('-\\dfrac{4}{5}\\cdot\\left(\\dfrac{11}{17}\\cdot\\dfrac{10}{16}\\right)') + '៖', Mf(F(-11, 34)), [Mf(F(11, 34)), Mf(F(-44, 85)), Mf(F(-11, 17))], M('-\\dfrac{4}{5}\\cdot\\dfrac{5}{8} = -\\dfrac{1}{2}') + ' ; ' + M('-\\dfrac{1}{2} \\times \\dfrac{11}{17} = -\\dfrac{11}{34}') + '។'))
    C.append(mcq('hard', 'mixed', 'គណនា ' + M('\\left(-\\dfrac{11}{21}\\right)\\cdot\\dfrac{3}{7} + \\left(\\dfrac{-3}{7}\\right)\\cdot\\left(-\\dfrac{11}{21}\\right)') + '៖', M(0), [Mf(F(-22, 49)), Mf(F(22, 49)), Mf(F(-11, 49))], M('-\\dfrac{33}{147} + \\dfrac{33}{147} = 0') + '។'))
    C.append(mcq('hard', 'mixed', 'គណនា ' + M('\\dfrac{13}{4} + \\dfrac{13}{9}') + '៖', Mf(F(169, 36)), [Mf(F(26, 13)), Mf(F(13, 36)), Mf(F(26, 36))], M('\\dfrac{13 \\times 9 + 13 \\times 4}{36} = \\dfrac{13 \\times 13}{36} = \\dfrac{169}{36}') + '។'))
    # ===================== 7. PISA: ស្ថានភាពជីវិត =====================
    C.append(mcq('pisa', 'pisa', 'ក្នុងសិក្ខាសាលាមួយ តន្ត្រីករមាន ' + Mf(F(1, 4)) + ' សិល្បករ ' + Mf(F(2, 5)) + ' អ្នករបាំ ' + Mf(F(1, 10)) + ' និងអ្នកដែលនៅសល់ជាអ្នកនិពន្ធ។ អ្នកនិពន្ធតាងដោយប្រភាគ៖', Mf(F(1, 4)), [Mf(F(3, 4)), Mf(F(1, 5)), Mf(F(3, 10))], M('\\dfrac{1}{4} + \\dfrac{2}{5} + \\dfrac{1}{10} = \\dfrac{3}{4}') + ' ; ' + M('1 - \\dfrac{3}{4} = \\dfrac{1}{4}') + '។'))
    spend = [F(1, 2), F(1, 20), F(1, 10), F(1, 25)]
    C.append(mcq('pisa', 'pisa', 'ប្រាក់ខែមួយខែចំណាយ ' + Mf(F(1, 2)) + ' លើម្ហូប ' + Mf(F(1, 20)) + ' លើសៀវភៅ ' + Mf(F(1, 10)) + ' លើធ្វើដំណើរ និង ' + Mf(F(1, 25)) + ' លើអនឡាញ។ ប្រាក់សន្សំតាងដោយប្រភាគ៖', Mf(1 - sum(spend)), [Mf(sum(spend)), Mf(F(1, 4)), Mf(F(1, 5))], M('\\dfrac{50+5+10+4}{100} = \\dfrac{69}{100}') + ' ; ' + M('1 - \\dfrac{69}{100} = \\dfrac{31}{100}') + '។'))
    C.append(mcq('pisa', 'pisa', 'ចតុកោណកែងមួយមានបរិមាត្រ ' + M('16.38\\ \\text{cm}') + ' ហើយជ្រុងមួយ ' + M('3.26\\ \\text{cm}') + '។ ជ្រុងមួយទៀតមានប្រវែង៖', M('4.93\\ \\text{cm}'), [M('8.19\\ \\text{cm}'), M('5.12\\ \\text{cm}'), M('13.12\\ \\text{cm}')], 'កន្លះបរិមាត្រ ' + M('8.19') + ' ; ' + M('8.19 - 3.26 = 4.93') + '។'))
    C.append(mcq('pisa', 'pisa', 'ចតុកោណកែងមួយមានជ្រុង ' + M('3.26\\ \\text{cm}') + ' និង ' + M('4.93\\ \\text{cm}') + '។ ផ្ទៃក្រឡា ' + M('\\mathcal{A}') + ' ស្មើ៖', M('16.0718\\ \\text{cm}^2'), [M('8.19\\ \\text{cm}^2'), M('16.38\\ \\text{cm}^2'), M('160.718\\ \\text{cm}^2')], M('\\mathcal{A} = 3.26 \\times 4.93 = 16.0718') + '។'))
    C.append(mcq('pisa', 'pisa', 'រូបមន្តធ្វើនំមួយបាច់ប្រើម្សៅ ' + Mm(F(9, 4)) + ' កែវ។ ធ្វើបាន ' + Mm(F(7, 2)) + ' បាច់ ត្រូវប្រើម្សៅប៉ុន្មានកែវ?', Mm(F(63, 8)), [Mm(F(9, 14)), Mm(F(23, 4)), Mm(F(63, 4))], M('\\dfrac{9}{4} \\times \\dfrac{7}{2} = \\dfrac{63}{8} = 7\\dfrac{7}{8}') + '។'))
    C.append(mcq('pisa', 'pisa', 'ទឹកក្នុងធុងមាន ' + M('1') + ' ពេញ។ ព្រឹកប្រើ ' + Mf(F(2, 5)) + ' ហើយរសៀលប្រើ ' + Mf(F(1, 4)) + ' នៃធុង។ ទឹកនៅសល់ជាប្រភាគ៖', Mf(F(7, 20)), [Mf(F(13, 20)), Mf(F(1, 3)), Mf(F(9, 20))], M('1 - \\dfrac{2}{5} - \\dfrac{1}{4} = \\dfrac{20-8-5}{20} = \\dfrac{7}{20}') + '។'))
    C.append(mcq('pisa', 'pisa', 'បុរសម្នាក់ដើរ ' + Mf(F(3, 4)) + ' គីឡូម៉ែត្រ ក្នុងមួយថ្ងៃ រយៈពេល ' + M(5) + ' ថ្ងៃ។ គាត់ដើរសរុប៖', M('3\\dfrac{3}{4}\\ \\text{km}'), [M('\\dfrac{3}{20}\\ \\text{km}'), M('4\\dfrac{3}{4}\\ \\text{km}'), M('1\\dfrac{2}{3}\\ \\text{km}')], M('5 \\times \\dfrac{3}{4} = \\dfrac{15}{4} = 3\\dfrac{3}{4}') + '។'))
    C.append(mcq('pisa', 'pisa', 'ក្រុងមួយមានសីតុណ្ហភាព ' + M('-3\\dfrac{1}{2}') + ' °C ព្រឹកនេះ។ ពេលថ្ងៃកើនឡើង ' + M('2\\dfrac{3}{4}') + ' °C។ សីតុណ្ហភាពពេលថ្ងៃគឺ៖', M('-\\dfrac{3}{4}') + ' °C', [M('\\dfrac{3}{4}') + ' °C', M('-6\\dfrac{1}{4}') + ' °C', M('6\\dfrac{1}{4}') + ' °C'], M('-\\dfrac{7}{2} + \\dfrac{11}{4} = \\dfrac{-14+11}{4} = -\\dfrac{3}{4}') + '។'))
    C.append(mcq('pisa', 'pisa', 'រង្វាន់ ' + R_(3000000) + ' ចែកឱ្យអ្នកឈ្នះទី ១ បាន ' + Mf(F(1, 3)) + ' ទី ២ បាន ' + Mf(F(2, 5)) + ' ហើយនៅសល់ជារង្វាន់ទី ៣។ រង្វាន់ទី ៣ មានប៉ុន្មានរៀល?', R_(800000), [R_(1000000), R_(1200000), R_(2200000)], M('1 - \\dfrac{1}{3} - \\dfrac{2}{5} = \\dfrac{4}{15}') + ' ; ' + M('3\\,000\\,000 \\times \\dfrac{4}{15} = 800\\,000') + '។'))
    # ===================== WRITING =====================
    C.append(wr('easy', 'convert', 'ក. សរសេរ ' + M('28.45') + ' ជាប្រភាគសម្រួលរួច។ ខ. ប្រៀបធៀប ' + M('0.54') + ' និង ' + M('0.5398') + '។', [
        ('ក. ' + M('28.45 = \\dfrac{2845}{100} = \\dfrac{569}{20} = 28\\dfrac{9}{20}'), 3), ('ខ. ' + M('0.5400 > 0.5398') + ' ដូចនេះ ' + M('0.54 > 0.5398'), 2)]))
    C.append(wr('medium', 'compare', 'ក្នុងចំនួន ' + M('\\dfrac{2}{5}, \\dfrac{1}{2}, \\dfrac{4}{9}') + ' រកចំនួនធំជាងគេ ហើយរៀបពីតូចទៅធំ។', [
        ('ភាគបែងរួមតូចបំផុតនៃ ' + M('5, 2, 9') + ' គឺ ' + M(90), 1), (M('\\dfrac{2}{5} = \\dfrac{36}{90},\\ \\dfrac{1}{2} = \\dfrac{45}{90},\\ \\dfrac{4}{9} = \\dfrac{40}{90}'), 2), ('ធំជាងគេ ' + M('\\dfrac{1}{2}') + ' ; លំដាប់ ' + M('\\dfrac{2}{5} < \\dfrac{4}{9} < \\dfrac{1}{2}'), 2)]))
    C.append(wr('medium', 'equal', 'ក. កំណត់ ' + M('x') + ' ដើម្បីឱ្យ ' + M('\\dfrac{45}{x} = 7\\dfrac{1}{2}') + '។ ខ. កំណត់ ' + M('x, y') + ' ដើម្បីឱ្យ ' + M('\\dfrac{-2}{x} = \\dfrac{y}{5} = -0.2') + '។', [
        ('ក. ' + M('7\\dfrac{1}{2} = \\dfrac{15}{2}') + ' ; ' + M('15x = 45 \\times 2'), 1), (M('x = 6'), 1), ('ខ. ' + M('-0.2 = -\\dfrac{1}{5}'), 1), (M('\\dfrac{-2}{x} = -\\dfrac{2}{10} \\Rightarrow x = 10'), 1), (M('\\dfrac{y}{5} = -\\dfrac{1}{5} \\Rightarrow y = -1'), 1)]))
    C.append(wr('medium', 'repeat', 'ក. សរសេរ ' + M('\\dfrac{3}{16}') + ' និង ' + M('\\dfrac{7}{40}') + ' ជាចំនួនទសភាគ។ ខ. សរសេរ ' + M('0.\\overline{4}') + ' និង ' + M('0.\\overline{27}') + ' ជាប្រភាគ។', [
        ('ក. ' + M('\\dfrac{3}{16} = \\dfrac{3 \\times 625}{10\\,000} = 0.1875'), 1), (M('\\dfrac{7}{40} = \\dfrac{7 \\times 25}{1\\,000} = 0.175'), 1), ('ខ. ' + M('0.\\overline{4} = \\dfrac{4}{9}'), 1), (M('0.\\overline{27} = \\dfrac{27}{99} = \\dfrac{3}{11}'), 2)]))
    C.append(wr('medium', 'add', 'គណនា ក. ' + M('-\\dfrac{5}{24} - \\dfrac{7}{30}') + ' ខ. ' + M('\\dfrac{1}{15} - \\dfrac{27}{50}') + ' គ. ' + M('-\\dfrac{5}{6} - \\left(-\\dfrac{7}{3}\\right)') + '។', [
        ('ក. ' + M('\\text{LCM}(24,30) = 120') + ' ; ' + M('\\dfrac{-25-28}{120} = -\\dfrac{53}{120}'), 2), ('ខ. ' + M('\\text{LCM}(15,50) = 150') + ' ; ' + M('\\dfrac{10-81}{150} = -\\dfrac{71}{150}'), 2), ('គ. ' + M('\\dfrac{-5+14}{6} = \\dfrac{9}{6} = \\dfrac{3}{2}'), 1)]))
    C.append(wr('medium', 'mul', 'គណនា ក. ' + M('\\dfrac{3}{8} \\times 3.8') + ' ខ. ' + M('\\left(-\\dfrac{2}{3}\\right)\\left(-\\dfrac{7}{15}\\right)') + ' គ. ' + M('-\\dfrac{3}{5} \\div 2\\dfrac{3}{10}') + '។', [
        ('ក. ' + M('\\dfrac{3}{8} \\times \\dfrac{38}{10} = \\dfrac{114}{80} = \\dfrac{57}{40}'), 2), ('ខ. ' + M('\\dfrac{(-2)(-7)}{3 \\times 15} = \\dfrac{14}{45}'), 1), ('គ. ' + M('-\\dfrac{3}{5} \\times \\dfrac{10}{23} = -\\dfrac{6}{23}'), 2)]))
    C.append(wr('hard', 'proof', 'បង្ហាញថា ' + M('\\dfrac{13}{4} + \\dfrac{13}{9} = \\dfrac{13}{4} \\times \\dfrac{13}{9}') + '។', [
        ('អង្គខាងឆ្វេង ' + M('\\dfrac{13 \\times 9 + 13 \\times 4}{4 \\times 9} = \\dfrac{13(9+4)}{36}'), 2), (M('= \\dfrac{13 \\times 13}{36} = \\dfrac{169}{36}'), 1), ('អង្គខាងស្តាំ ' + M('\\dfrac{13 \\times 13}{4 \\times 9} = \\dfrac{169}{36}'), 1), ('អង្គទាំងពីរស្មើគ្នា ដូចនេះសមភាពពិត។', 1)]))
    C.append(wr('hard', 'proof', 'បើ ' + M('\\dfrac{a}{b} < \\dfrac{c}{d}') + ' ចូរបង្ហាញថា ' + M('\\dfrac{a}{b} + \\dfrac{e}{f} < \\dfrac{c}{d} + \\dfrac{e}{f}') + '។', [
        ('គណនាផលដក ' + M('\\left(\\dfrac{c}{d} + \\dfrac{e}{f}\\right) - \\left(\\dfrac{a}{b} + \\dfrac{e}{f}\\right)'), 1), (M('= \\dfrac{c}{d} - \\dfrac{a}{b}'), 2), ('ដោយ ' + M('\\dfrac{a}{b} < \\dfrac{c}{d}') + ' នោះ ' + M('\\dfrac{c}{d} - \\dfrac{a}{b} > 0'), 1), ('ដូចនេះ ' + M('\\dfrac{a}{b} + \\dfrac{e}{f} < \\dfrac{c}{d} + \\dfrac{e}{f}'), 1)]))
    C.append(wr('hard', 'mixed', 'គណនា ក. ' + M('\\left(\\dfrac{1}{2} + \\dfrac{1}{3}\\right) \\div \\left(\\dfrac{5}{8} - \\dfrac{1}{4}\\right)') + ' ខ. ' + M('\\dfrac{3\\frac{2}{5} - \\frac{25}{8}}{\\frac{7}{12} + 5\\frac{4}{9}}') + '។', [
        ('ក. ' + M('\\dfrac{5}{6} \\div \\dfrac{3}{8} = \\dfrac{5}{6} \\times \\dfrac{8}{3} = \\dfrac{20}{9} = 2\\dfrac{2}{9}'), 2), ('ខ. ភាគយក ' + M('\\dfrac{17}{5} - \\dfrac{25}{8} = \\dfrac{11}{40}'), 1), ('ភាគបែង ' + M('\\dfrac{7}{12} + \\dfrac{49}{9} = \\dfrac{217}{36}'), 1), (M('\\dfrac{11}{40} \\times \\dfrac{36}{217} = \\dfrac{99}{2170}'), 1)]))
    C.append(wr('hard', 'mixed', 'គណនា ក. ' + M('-\\dfrac{11}{8}\\cdot\\dfrac{21}{22} + \\dfrac{17}{16}\\cdot\\dfrac{21}{22}') + ' ខ. ' + M('-\\dfrac{11}{8} + \\dfrac{21}{4} - \\dfrac{17}{16}') + '។', [
        ('ក. ដាក់កត្តារួម ' + M('\\dfrac{21}{22}\\left(-\\dfrac{22}{16} + \\dfrac{17}{16}\\right)'), 1), (M('= \\dfrac{21}{22}\\left(-\\dfrac{5}{16}\\right) = -\\dfrac{105}{352}'), 2), ('ខ. ' + M('\\dfrac{-22 + 84 - 17}{16} = \\dfrac{45}{16} = 2\\dfrac{13}{16}'), 2)]))
    C.append(wr('hard', 'compare', 'រៀបចំនួន ' + M('\\dfrac{1}{8}, -\\dfrac{9}{7}, -1, 0.28, 1\\dfrac{2}{5}') + ' តាមលំដាប់ពីតូចទៅធំ ហើយពន្យល់។', [
        ('បំប្លែងជាទសភាគ ' + M('\\dfrac{1}{8} = 0.125') + ' ; ' + M('-\\dfrac{9}{7} \\approx -1.29') + ' ; ' + M('1\\dfrac{2}{5} = 1.4'), 2), ('ចំនួនអវិជ្ជមានតូចជាងចំនួនវិជ្ជមាន ; ' + M('-1.29 < -1'), 1), (M('-\\dfrac{9}{7} < -1 < \\dfrac{1}{8} < 0.28 < 1\\dfrac{2}{5}'), 2)]))
    C.append(wr('pisa', 'pisa', 'ប្រាក់ចំណូលមួយខែចំណាយ ' + M('\\dfrac{1}{2}') + ' លើម្ហូប ' + M('\\dfrac{1}{20}') + ' លើសៀវភៅ ' + M('\\dfrac{1}{10}') + ' លើធ្វើដំណើរ និង ' + M('\\dfrac{1}{25}') + ' លើអនឡាញ។ ក. រកប្រភាគចំណាយសរុប។ ខ. រកប្រភាគប្រាក់សន្សំ។ គ. បើចំណូល ' + R_(2000000) + ' សន្សំបានប៉ុន្មាន?', [
        ('ក. ' + M('\\dfrac{50 + 5 + 10 + 4}{100} = \\dfrac{69}{100}') + ' (ភាគបែងរួម ' + M(100) + ')', 2), ('ខ. ' + M('1 - \\dfrac{69}{100} = \\dfrac{31}{100}'), 1), ('គ. ' + M('2\\,000\\,000 \\times \\dfrac{31}{100} = 620\\,000') + ' ៛', 2)]))
    C.append(wr('pisa', 'pisa', 'ក្នុងសិក្ខាសាលាមួយ តន្ត្រីករមាន ' + M('\\dfrac{1}{4}') + ' សិល្បករ ' + M('\\dfrac{2}{5}') + ' អ្នករបាំ ' + M('\\dfrac{1}{10}') + ' ហើយនៅសល់ជាអ្នកនិពន្ធ។ ក. រកប្រភាគអ្នកនិពន្ធ។ ខ. បើមានអ្នកចូលរួមសរុប ' + M(200) + ' នាក់ មានអ្នកនិពន្ធប៉ុន្មាននាក់?', [
        ('ក. ' + M('\\dfrac{1}{4} + \\dfrac{2}{5} + \\dfrac{1}{10} = \\dfrac{5 + 8 + 2}{20} = \\dfrac{3}{4}'), 2), (M('1 - \\dfrac{3}{4} = \\dfrac{1}{4}'), 1), ('ខ. ' + M('200 \\times \\dfrac{1}{4} = 50') + ' នាក់', 2)]))
    C.append(wr('pisa', 'pisa', 'ចតុកោណកែងមួយមានបរិមាត្រ ' + M('16.38\\ \\text{cm}') + '។ ក. រកកន្លះបរិមាត្រ។ ខ. បើជ្រុងមួយ ' + M('3.26\\ \\text{cm}') + ' រកជ្រុងមួយទៀត។ គ. គណនាផ្ទៃក្រឡា ' + M('\\mathcal{A}') + '។', [
        ('ក. ' + M('16.38 \\div 2 = 8.19\\ \\text{cm}'), 1), ('ខ. ' + M('x + 3.26 = 8.19 \\Rightarrow x = 4.93\\ \\text{cm}'), 2), ('គ. ' + M('\\mathcal{A} = 3.26 \\times 4.93 = 16.0718\\ \\text{cm}^2'), 2)]))
    C.append(wr('pisa', 'pisa', 'រូបមន្តធ្វើនំមួយបាច់ប្រើម្សៅ ' + M('2\\dfrac{1}{4}') + ' កែវ និងស្ករ ' + M('\\dfrac{3}{4}') + ' កែវ។ ក. ធ្វើ ' + M('3\\dfrac{1}{2}') + ' បាច់ ត្រូវប្រើម្សៅប៉ុន្មានកែវ? ខ. ត្រូវប្រើស្ករប៉ុន្មានកែវ? គ. ម្សៅច្រើនជាងស្ករប៉ុន្មានដង (ក្នុងមួយបាច់)?', [
        ('ក. ' + M('\\dfrac{9}{4} \\times \\dfrac{7}{2} = \\dfrac{63}{8} = 7\\dfrac{7}{8}') + ' កែវ', 2), ('ខ. ' + M('\\dfrac{3}{4} \\times \\dfrac{7}{2} = \\dfrac{21}{8} = 2\\dfrac{5}{8}') + ' កែវ', 2), ('គ. ' + M('\\dfrac{9}{4} \\div \\dfrac{3}{4} = 3') + ' ដង', 1)]))
    C.append(wr('pisa', 'pisa', 'រង្វាន់ ' + M('3\\,000\\,000') + ' ៛ ចែកឱ្យអ្នកឈ្នះទី ១ បាន ' + M('\\dfrac{1}{3}') + ' ទី ២ បាន ' + M('\\dfrac{2}{5}') + ' ហើយនៅសល់ជារង្វាន់ទី ៣។ ក. រកប្រភាគរង្វាន់ទី ៣។ ខ. រករង្វាន់នីមួយៗជារៀល។', [
        ('ក. ' + M('1 - \\dfrac{1}{3} - \\dfrac{2}{5} = \\dfrac{15 - 5 - 6}{15} = \\dfrac{4}{15}'), 2), ('ខ. ទី ១ ' + M('3\\,000\\,000 \\times \\dfrac{1}{3} = 1\\,000\\,000') + ' ; ទី ២ ' + M('3\\,000\\,000 \\times \\dfrac{2}{5} = 1\\,200\\,000'), 2), ('ទី ៣ ' + M('3\\,000\\,000 \\times \\dfrac{4}{15} = 800\\,000') + ' ៛', 1)]))
    return C

def R_(n): return M(num(n)) + ' ៛'
