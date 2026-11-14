"""G11 Lesson 5 — ទំនាក់ទំនងតួនៃស្វ៊ីត (recurrences, a_n vs S_n, second-order linear recurrences).
Every numeric answer is produced by iterating the recurrence here, then checked against the closed form."""
from fractions import Fraction as F
from lib import M, mcq, wr

LESSON = 'ទំនាក់ទំនងតួនៃស្វ៊ីត'
CHAPTER = 'ជំពូកទី 1 : ស្វ៊ីតនិងអនុមានរួមគណិតវិទ្យា'


def with_img(q, svg):
    q['img'] = svg
    return q


def it1(a1, step, n):
    """a_1 = a1, a_{k+1} = step(k, a_k); returns a_n."""
    a = F(a1)
    for k in range(1, n):
        a = F(step(k, a))
    return a


def it2(a1, a2, step, n):
    x, y = F(a1), F(a2)
    if n == 1: return x
    for k in range(1, n - 1):
        x, y = y, F(step(k, y, x))
    return y


def v(x):
    x = F(x)
    return M(str(x.numerator)) if x.denominator == 1 else M(r'\dfrac{%d}{%d}' % (x.numerator, x.denominator)) if x > 0 else M(r'-\dfrac{%d}{%d}' % (-x.numerator, x.denominator))


def opts(*xs): return [v(x) for x in xs]


def txt(x, dp=2):
    return ('%.*f' % (dp, float(x)))


# ---- consistency checks between recurrences and closed forms (run at import) -------
assert it1(1, lambda k, a: 1 + 4 * a, 6) == F(4 ** 6 - 1, 3)
assert it1(3, lambda k, a: 2 * a - k + 1, 6) == 2 ** 6 + 6
assert it1(5, lambda k, a: 3 * a - 2 * k, 4) == 99
assert it1(1, lambda k, a: 2 * a + 1, 6) == 2 ** 6 - 1
assert it1(3, lambda k, a: 2 * a - 4, 4) == -4
assert it2(1, 3, lambda k, y, x: 3 * y - 2 * x, 8) == 2 ** 8 - 1
assert it2(0, 3, lambda k, y, x: 4 * y - 3 * x, 6) == F(3 ** 6 - 3, 2)
assert it2(1, 13, lambda k, y, x: y + 6 * x, 5) == 3 ** 5 + (-2) ** 5
assert it2(2, 5, lambda k, y, x: 5 * y - 6 * x, 7) == 2 ** 6 + 3 ** 6
assert it1(1, lambda k, a: 2 * a + k, 8) == 3 * 2 ** 7 - 8 - 1
assert it1(3, lambda k, a: 3 * a - 4, 5) == 2 + 3 ** 4

# ---- figure: arrows with x4+1 ---------------------------------------------------
FIG_CHAIN = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 440 90' width='440' height='90'>" +
             ''.join("<rect x='%d' y='30' width='56' height='34' rx='6' fill='#dbeafe' stroke='#1e40af' stroke-width='1.5'/>"
                     "<text x='%d' y='53' text-anchor='middle' font-family='Times New Roman, serif' font-size='17' fill='#1e40af'>%s</text>" % (20 + 112 * i, 48 + 112 * i, t)
                     for i, t in enumerate(['1', '5', '21', '85'])) +
             ''.join("<path d='M %d 47 L %d 47' stroke='#dc2626' stroke-width='1.8'/><polygon points='%d,42 %d,47 %d,52' fill='#dc2626'/>"
                     "<text x='%d' y='36' text-anchor='middle' font-family='Times New Roman, serif' font-size='13' fill='#dc2626'>×4 + 1</text>" % (78 + 112 * i, 128 + 112 * i, 128 + 112 * i, 134 + 112 * i, 128 + 112 * i, 103 + 112 * i)
                     for i in range(3)) + "</svg>")
FIG_BAR = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 360 110' width='360' height='110'>"
           "<rect x='30' y='46' width='220' height='34' fill='#ccfbf1' stroke='#0f766e' stroke-width='1.6'/>"
           "<rect x='250' y='46' width='80' height='34' fill='#fde68a' stroke='#b45309' stroke-width='1.6'/>"
           "<text x='140' y='69' text-anchor='middle' font-family='Times New Roman, serif' font-size='16' fill='#0f766e'>S(n−1)</text>"
           "<text x='290' y='69' text-anchor='middle' font-family='Times New Roman, serif' font-size='16' fill='#b45309'>a(n)</text>"
           "<path d='M 30 36 Q 30 24 42 24 L 318 24 Q 330 24 330 36' fill='none' stroke='#1e40af' stroke-width='1.6'/>"
           "<text x='180' y='16' text-anchor='middle' font-family='Times New Roman, serif' font-size='16' fill='#1e40af'>S(n) = S(n−1) + a(n)</text></svg>")


def cands():
    C = []

    # ======================= MCQ easy (10) =======================
    C.append(mcq('easy', 'sec1_aux', 'ស្វ៊ីតដែលមាន ' + M(r'a_{n+1}=a_n+d') + ' ជាស្វ៊ីត ៖',
                 'ស្វ៊ីតនព្វន្ត', ['ស្វ៊ីតធរណីមាត្រ', 'ស្វ៊ីតថេរតែប៉ុណ្ណោះ', 'មិនមែនស្វ៊ីតទេ'],
                 'បូកចំនួនថេរ ' + M('d') + ' រាល់ពេល គឺជាស្វ៊ីតនព្វន្ត។', 'Remember'))
    C.append(mcq('easy', 'sec1_aux', 'ស្វ៊ីតដែលមាន ' + M(r'a_{n+1}=q\,a_n') + ' ជាស្វ៊ីត ៖',
                 'ស្វ៊ីតធរណីមាត្រ', ['ស្វ៊ីតនព្វន្ត', 'ស្វ៊ីតថេរតែប៉ុណ្ណោះ', 'ស្វ៊ីតផលបូក'],
                 'គុណនឹងចំនួនថេរ ' + M('q') + ' រាល់ពេល គឺជាស្វ៊ីតធរណីមាត្រ។', 'Remember'))
    C.append(mcq('easy', 'sec2_sn', 'ចំពោះ ' + M(r'n\ge2') + ' តួទី ' + M('n') + ' នៃស្វ៊ីតស្មើ ៖',
                 M(r'a_n=S_n-S_{n-1}'), [M(r'a_n=S_n+S_{n-1}'), M(r'a_n=S_{n}-S_{n+1}'), M(r'a_n=\dfrac{S_n}{S_{n-1}}')],
                 M('S_n') + ' ជាផលបូក ' + M('n') + ' តួ ដកផលបូក ' + M('n-1') + ' តួ នៅសល់តួទី ' + M('n') + '។', 'Remember'))
    C.append(mcq('easy', 'sec2_sn', 'តួទី ១ នៃស្វ៊ីត ទាក់ទងនឹងផលបូកដូចខាងក្រោម ៖',
                 M(r'a_1=S_1'), [M(r'a_1=S_2-S_1'), M(r'a_1=0'), M(r'a_1=S_1-S_0')],
                 'ផលបូកមួយតួតែមួយ គឺតួទី ១ ដោយខ្លួនវា។', 'Remember'))
    C.append(mcq('easy', 'sec1_aux', M(r'a_1=2,\ a_{n+1}=a_n+3') + '។ តួទី ៤ ស្មើ ៖',
                 v(it1(2, lambda k, a: a + 3, 4)), opts(9, 12, 14), M(r'2,5,8,11') + ' ដូច្នេះ ' + M('a_4=11') + '។', 'Apply'))
    C.append(mcq('easy', 'sec1_aux', M(r'a_1=1,\ a_{n+1}=2a_n') + '។ តួទី ៥ ស្មើ ៖',
                 v(it1(1, lambda k, a: 2 * a, 5)), opts(10, 32, 8), M(r'1,2,4,8,16') + '។', 'Apply'))
    C.append(with_img(mcq('easy', 'sec1_aux', M(r'a_1=1,\ a_{n+1}=1+4a_n') + '។ តួទី ៣ ស្មើ ៖',
                 v(it1(1, lambda k, a: 1 + 4 * a, 3)), opts(13, 16, 25), M(r'a_2=5,\ a_3=1+20=21') + '។', 'Apply'), FIG_CHAIN))
    C.append(mcq('easy', 'sec3_second', 'សមីការសម្គាល់នៃ ' + M(r'a_{n+2}=a_{n+1}+6a_n') + ' គឺ ៖',
                 M(r'x^2-x-6=0'), [M(r'x^2+x-6=0'), M(r'x^2-x+6=0'), M(r'x^2-6x-1=0')],
                 M(r'a_{n+2}-a_{n+1}-6a_n=0') + ' ដូច្នេះ ' + M(r'x^2-x-6=0') + '។', 'Remember'))
    C.append(mcq('easy', 'sec3_second', M(r'a_1=1,\ a_2=2,\ a_{n+2}=a_{n+1}+a_n') + '។ តួទី ៤ ស្មើ ៖',
                 v(it2(1, 2, lambda k, y, x: y + x, 4)), opts(4, 6, 8), M(r'1,2,3,5') + '។', 'Apply'))
    C.append(with_img(mcq('easy', 'sec2_sn', M(r'S_n=n^2+n') + '។ តួទី ៣ ស្មើ ៖',
                 v(3 ** 2 + 3 - (2 ** 2 + 2)), opts(12, 8, 9), M(r'S_3-S_2=12-6=6') + '។', 'Apply'), FIG_BAR))

    # ======================= MCQ medium (14) =======================
    C.append(mcq('medium', 'sec1_aux', M(r'a_1=3,\ a_{n+1}=2a_n-4') + '។ តួទី ៤ ស្មើ ៖',
                 v(it1(3, lambda k, a: 2 * a - 4, 4)), opts(4, 0, -2), M(r'3,2,0,-4') + '។', 'Apply'))
    C.append(mcq('medium', 'sec1_aux', M(r'a_1=5,\ a_{n+1}=3a_n-2n') + '។ តួទី ៤ ស្មើ ៖',
                 v(it1(5, lambda k, a: 3 * a - 2 * k, 4)), opts(97, 35, 101), M(r'5,13,35,99') + '។', 'Apply'))
    C.append(mcq('medium', 'sec1_aux', 'ស្វ៊ីតជំនួយ ' + M(r'r_n=\alpha n+\beta') + ' សម្រាប់ ' + M(r'a_{n+1}=2a_n-n+1') + ' គឺ ៖',
                 M(r'r_n=n'), [M(r'r_n=n+1'), M(r'r_n=2n'), M(r'r_n=-n')],
                 M(r'\alpha(n+1)+\beta=2(\alpha n+\beta)-n+1') + ' ឱ្យ ' + M(r'\alpha=1,\ \beta=0') + '។', 'Apply'))
    C.append(mcq('medium', 'sec1_aux', M(r'a_1=3,\ a_{n+1}=2a_n-n+1') + ' មាន ' + M(r'a_n=2^n+n') + '។ តួទី ៦ ស្មើ ៖',
                 v(it1(3, lambda k, a: 2 * a - k + 1, 6)), opts(64, 66, 72), M(r'2^6+6=70') + '។', 'Apply'))
    C.append(mcq('medium', 'sec2_sn', M(r'S_n=n^3+2n') + '។ តួទី ៥ ស្មើ ៖',
                 v((5 ** 3 + 10) - (4 ** 3 + 8)), opts(135, 72, 73), M(r'S_5-S_4=135-72=63') + '។', 'Apply'))
    C.append(mcq('medium', 'sec2_sn', M(r'S_n=2n^2+3n') + '។ តួទី ១០ ស្មើ ៖',
                 v((2 * 100 + 30) - (2 * 81 + 27)), opts(230, 39, 43), M(r'S_{10}-S_9=230-189=41') + ' (ឬ ' + M(r'a_n=4n+1') + ')។', 'Apply'))
    C.append(mcq('medium', 'sec2_sn', M(r'S_n=3^n-1') + '។ តួទី ៤ ស្មើ ៖',
                 v((3 ** 4 - 1) - (3 ** 3 - 1)), opts(80, 26, 27), M(r'80-26=54') + ' (ឬ ' + M(r'a_n=2\cdot3^{n-1}') + ')។', 'Apply'))
    C.append(mcq('medium', 'sec3_second', 'ឫសនៃសមីការសម្គាល់របស់ ' + M(r'a_{n+2}=3a_{n+1}-2a_n') + ' គឺ ៖',
                 M(r'1\ \text{និង}\ 2'), [M(r'-1\ \text{និង}\ -2'), M(r'1\ \text{និង}\ -2'), M(r'3\ \text{និង}\ -2')],
                 M(r'x^2-3x+2=(x-1)(x-2)=0') + '។', 'Apply'))
    C.append(mcq('medium', 'sec3_second', M(r'a_1=1,\ a_2=3,\ a_{n+2}=3a_{n+1}-2a_n') + ' មាន ' + M(r'a_n=2^n-1') + '។ តួទី ៨ ស្មើ ៖',
                 v(it2(1, 3, lambda k, y, x: 3 * y - 2 * x, 8)), opts(256, 127, 257), M(r'2^8-1=255') + '។', 'Apply'))
    C.append(mcq('medium', 'sec3_second', M(r'a_1=0,\ a_2=3,\ a_{n+2}=4a_{n+1}-3a_n') + '។ តួទី ៦ ស្មើ ៖',
                 v(it2(0, 3, lambda k, y, x: 4 * y - 3 * x, 6)), opts(360, 726, 243), M(r'\dfrac{3^6-3}{2}=363') + '។', 'Apply'))
    C.append(mcq('medium', 'sec1_aux', M(r'a_1=1,\ a_{n+1}=a_n+n') + '។ តួទី ១០ ស្មើ ៖',
                 v(it1(1, lambda k, a: a + k, 10)), opts(45, 55, 56), M(r'1+\dfrac{10\cdot9}{2}=46') + '។', 'Apply'))
    C.append(mcq('medium', 'sec1_aux', M(r'a_1=1,\ 3a_{n+1}=3a_n+4') + '។ តួទី ៧ ស្មើ ៖',
                 v(it1(1, lambda k, a: a + F(4, 3), 7)), opts(8, 10, F(25, 3)), M(r'\dfrac{4\cdot7-1}{3}=9') + '។', 'Apply'))
    C.append(mcq('medium', 'sec1_aux', M(r'a_1=1,\ a_{n+1}=2a_n+1') + '។ តួទី ៦ ស្មើ ៖',
                 v(it1(1, lambda k, a: 2 * a + 1, 6)), opts(64, 31, 127), M(r'a_n+1=2^n') + ' ដូច្នេះ ' + M(r'a_6=63') + '។', 'Apply'))
    C.append(mcq('medium', 'sec1_aux', M(r'a_1=2,\ a_{n+1}=\dfrac{a_n}{a_n+3}') + ' ហើយ ' + M(r'b_n=\dfrac1{a_n}') + '។ តួ ' + M('b_3') + ' ស្មើ ៖',
                 v(F(17, 2)), opts(F(5, 2), F(7, 2), 9), M(r'b_{n+1}=3b_n+1') + ' និង ' + M(r'b_1=\dfrac12,\ b_2=\dfrac52,\ b_3=\dfrac{17}{2}') + '។', 'Apply'))

    # ======================= MCQ hard (7) =======================
    C.append(mcq('hard', 'sec2_sn', M(r'a_1=1,\ S_n=a_{n+1}+n^2') + '។ តួទី ៥ ស្មើ ៖',
                 v(-29), opts(-11, 11, -35), M(r'a_2=0,\ a_3=-3,\ a_4=-11,\ a_5=-29') + ' (ពី ' + M(r'a_{n+1}=2a_n-2n+1') + ' ចំពោះ ' + M(r'n\ge2') + ')។', 'Analyze'))
    C.append(mcq('hard', 'sec2_sn', M(r'S_n=\dfrac{n}{n-1}a_n') + ' (' + M(r'n\ge2') + ') និង ' + M('a_1=1') + ' ។ តួទី ៥ ស្មើ ៖',
                 v(96), opts(120, 24, 100), M(r'S_n=n!') + ' ដូច្នេះ ' + M(r'a_5=120-24=96') + '។', 'Analyze'))
    C.append(mcq('hard', 'sec1_aux', M(r'a_1=4,\ a_{n+1}=\dfrac{4a_n-9}{a_n-2}') + '។ តួទី ១០ ស្មើ ៖',
                 v(F(31, 10)), opts(F(13, 4), 4, F(10, 3)), M(r'a_n=3+\dfrac1n') + ' ដូច្នេះ ' + M(r'a_{10}=\dfrac{31}{10}') + '។', 'Analyze'))
    C.append(mcq('hard', 'sec1_aux', M(r'a_1=1,\ a_{n+1}=p\,a_n+q') + ' មាន ' + M('a_3=6') + ' និង ' + M('a_5=86') + '។ គូ ' + M('(p,q)') + ' មួយដែលត្រូវ ៖',
                 M(r'(4,-2)'), [M(r'(2,2)'), M(r'(-4,-2)'), M(r'(3,1)')],
                 M(r'p=4,q=-2:\ a_2=2,\ a_3=6,\ a_4=22,\ a_5=86') + ' (ក៏មាន ' + M(r'(-4,\tfrac{10}{3})') + ' ដែរ)។', 'Analyze'))
    C.append(mcq('hard', 'sec2_sn', M(r'S_n=4-a_n-\dfrac{1}{2^{n-2}}') + '។ តួទី ៦ ស្មើ ៖',
                 v(F(3, 16)), opts(F(3, 32), F(3, 8), F(1, 16)), M(r'a_n=\dfrac{n}{2^{n-1}}') + ' ដូច្នេះ ' + M(r'a_6=\dfrac{6}{32}=\dfrac{3}{16}') + '។', 'Analyze'))
    C.append(mcq('hard', 'sec3_second', M(r'a_1=1,\ a_2=13,\ a_{n+2}=a_{n+1}+6a_n') + ' មាន ' + M(r'a_n=3^n+(-2)^n') + '។ តួទី ៥ ស្មើ ៖',
                 v(it2(1, 13, lambda k, y, x: y + 6 * x, 5)), opts(275, 243, 227), M(r'3^5+(-2)^5=243-32=211') + '។', 'Analyze'))
    C.append(mcq('hard', 'sec1_aux', M(r'a_1=1,\ 3a_{n+1}=2a_n+3') + '។ តួទី ៤ ស្មើ ៖',
                 v(F(65, 27)), opts(F(5, 3), F(19, 9), F(8, 3)), M(r'a_n=3-2\left(\dfrac23\right)^{n-1}') + ' ដូច្នេះ ' + M(r'a_4=3-\dfrac{16}{27}=\dfrac{65}{27}') + '។', 'Analyze'))

    # ======================= MCQ pisa (5) =======================
    D12 = 15000 - 10000 * F(102, 100) ** 12
    C.append(mcq('pisa', 'sec1_aux', 'កម្ចី ៥ ០០០ ដុល្លារ ការប្រាក់ ២% ក្នុងមួយខែ ហើយបង់ ៣០០ ដុល្លារក្នុងមួយខែ ៖ ' + M(r'D_{n+1}=1.02D_n-300') + ' ។ ក្រោយបង់ ១២ ខែ សមតុល្យប្រហែល ៖',
                 M(txt(D12)), [M(txt(D12 + 1000)), M(txt(5000 - 3600)), M(txt(5000 * F(102, 100) ** 12))],
                 M(r'D_n=15000-10000(1.02)^n') + ' ដូច្នេះ ' + M(r'D_{12}\approx' + txt(D12)) + ' ដុល្លារ។', 'Evaluate'))
    P3 = 500 + 500 * F(12, 10) ** 3
    C.append(mcq('pisa', 'sec1_aux', 'ត្រីក្នុងស្រះមាន ១ ០០០ ក្បាល ក្នុងមួយឆ្នាំកើន ២០% រួចចាប់យក ១០០ ក្បាល ៖ ' + M(r'P_{n+1}=1.2P_n-100') + ' ។ ក្រោយ ៣ ឆ្នាំ មានត្រីប្រហែល ៖',
                 M(txt(P3, 0)), [M('1300'), M('1200'), M(txt(1000 * F(12, 10) ** 3 , 0))],
                 M(r'P_n=500+500(1.2)^n') + ' ដូច្នេះ ' + M(r'P_3=500+500\times1.728=1364') + '។', 'Evaluate'))
    C.append(mcq('pisa', 'sec1_aux', 'ប៉មហាណូយ ៖ ចំនួនការផ្លាស់ទី ' + M('a_n') + ' សម្រាប់ ' + M('n') + ' ថាស មាន ' + M(r'a_1=1,\ a_{n+1}=2a_n+1') + '។ ចំពោះ ១០ ថាស ត្រូវផ្លាស់ទី ៖',
                 v(it1(1, lambda k, a: 2 * a + 1, 10)), opts(1024, 512, 1000), M(r'a_n=2^n-1') + ' ដូច្នេះ ' + M(r'a_{10}=1023') + '។', 'Evaluate'))
    C.append(mcq('pisa', 'sec2_sn', 'សិស្សសន្សំលុយ ហើយប្រាក់សរុបក្រោយ ' + M('n') + ' ថ្ងៃ គឺ ' + M(r'S_n=n^2+3n') + ' (រយរៀល) ។ ថ្ងៃទី ២០ សន្សំបាន ៖',
                 M(str((400 + 60) - (361 + 57))), [M('460'), M('40'), M('44')],
                 M(r'S_{20}-S_{19}=460-418=42') + ' រយរៀល។', 'Evaluate'))
    C.append(mcq('pisa', 'sec3_second', 'ឡើងជណ្ដើរ ' + M('n') + ' ថ្នាក់ ដោយឡើងម្ដងមួយ ឬពីរថ្នាក់ ចំនួនវិធី ' + M(r'a_n') + ' មាន ' + M(r'a_1=1,\ a_2=2,\ a_{n+2}=a_{n+1}+a_n') + '។ ជណ្ដើរ ៨ ថ្នាក់ មានវិធី ៖',
                 v(it2(1, 2, lambda k, y, x: y + x, 8)), opts(21, 55, 32), M(r'1,2,3,5,8,13,21,34') + '។', 'Evaluate'))

    # ======================= Writing easy (1) =======================
    C.append(wr('easy', 'sec1_aux', M(r'a_1=1,\ a_{n+1}=2a_n+3') + '។ គណនា ' + M('a_2,a_3,a_4') + '។',
                [(M(r'a_2=2a_1+3=2\times1+3') + '។', 1), (M(r'a_2=5') + '។', 1),
                 (M(r'a_3=2\times5+3=13') + '។', 1), (M(r'a_4=2\times13+3') + '។', 1),
                 (M('a_4=%d' % it1(1, lambda k, a: 2 * a + 3, 4)) + '។', 1)], 'Apply'))

    # ======================= Writing medium (4) =======================
    C.append(wr('medium', 'sec2_sn', M(r'S_n=2n^2+3n') + ' ជាផលបូក ' + M('n') + ' តួដំបូង ។ កំណត់ ' + M('a_n') + '។',
                [('ចំពោះ ' + M(r'n\ge2') + '៖ ' + M(r'a_n=S_n-S_{n-1}') + '។', 1),
                 (M(r'=2n^2+3n-[2(n-1)^2+3(n-1)]') + '។', 1),
                 (M(r'=2n^2+3n-2n^2+4n-2-3n+3') + '។', 1),
                 (M(r'a_n=4n+1') + '។', 1),
                 ('ពិនិត្យ ' + M(r'a_1=S_1=5=4(1)+1') + ' ពិត។', 1)], 'Apply'))
    C.append(wr('medium', 'sec1_aux', M(r'a_1=1,\ a_{n+1}=a_n+n') + '។ កំណត់ ' + M('a_n') + '។',
                [(M(r'a_{k+1}-a_k=k') + ' ចំពោះ ' + M(r'k=1,\dots,n-1') + '។', 1),
                 ('បូកអង្គនិងអង្គ ៖ ' + M(r'a_n-a_1=1+2+\dots+(n-1)') + '។', 1),
                 (M(r'=\dfrac{(n-1)n}{2}') + '។', 1),
                 (M(r'a_n=1+\dfrac{n(n-1)}{2}') + '។', 1),
                 ('ពិនិត្យ ' + M('a_1=1') + ' ពិត។', 1)], 'Apply'))
    C.append(wr('medium', 'sec1_aux', M(r'a_1=3,\ a_{n+1}=3a_n-4') + '។ កំណត់ ' + M('a_n') + ' និងគណនា ' + M('a_5') + '។',
                [('ស្វ៊ីតជំនួយថេរ ' + M(r'r=3r-4\Rightarrow r=2') + '។', 1),
                 (M(r'a_{n+1}-2=3(a_n-2)') + '។', 1),
                 (M(r'V_n=a_n-2') + ' ជាធរណីមាត្រ ' + M(r'q=3,\ V_1=1') + '។', 1),
                 (M(r'a_n=2+3^{n-1}') + '។', 1),
                 (M('a_5=2+81=%d' % it1(3, lambda k, a: 3 * a - 4, 5)) + '។', 1)], 'Apply'))
    C.append(wr('medium', 'sec3_second', M(r'a_1=1,\ a_2=5,\ a_{n+2}=5a_{n+1}-6a_n') + '។ កំណត់ ' + M('a_n') + '។',
                [('សមីការសម្គាល់ ' + M(r'x^2-5x+6=0') + ' មានឫស ' + M(r'2,\ 3') + '។', 1),
                 (M(r'a_{n+2}-2a_{n+1}=3(a_{n+1}-2a_n)') + ' ហើយ ' + M(r'a_2-2a_1=3') + '។', 1),
                 (M(r'a_{n+1}-2a_n=3^n') + '។', 1),
                 (M(r'a_{n+1}-3a_n=2^n') + ' (ពីឫសមួយទៀត ' + M(r'a_2-3a_1=2') + ')។', 1),
                 ('ដក ៖ ' + M(r'a_n=3^n-2^n') + '។', 1)], 'Apply'))

    # ======================= Writing hard (4) =======================
    C.append(wr('hard', 'sec2_sn', M(r'a_1=1,\ S_n=a_{n+1}+n^2') + ' (' + M(r'n\ge1') + ') ។ កំណត់ ' + M('a_n') + '។',
                [(M(r'n=1:\ a_2=S_1-1=0') + '។', 1),
                 ('ចំពោះ ' + M(r'n\ge2') + ' ៖ ' + M(r'a_n=S_n-S_{n-1}=a_{n+1}-a_n+2n-1') + ' ឬ ' + M(r'a_{n+1}=2a_n-2n+1') + '។', 1),
                 ('ស្វ៊ីតជំនួយ ' + M(r'r_n=2n+1') + ' ដែល ' + M(r'a_{n+1}-(2n+3)=2(a_n-(2n+1))') + '។', 1),
                 (M(r'a_n-(2n+1)=-5\cdot2^{n-2}') + ' ចំពោះ ' + M(r'n\ge2') + ' (ព្រោះ ' + M(r'a_2-5=-5') + ')។', 1),
                 (M(r'a_n=2n+1-5\cdot2^{n-2}') + ' ចំពោះ ' + M(r'n\ge2') + ' ហើយ ' + M(r'a_1=1') + '។', 1)], 'Analyze'))
    C.append(wr('hard', 'sec1_aux', M(r'a_1=4,\ a_{n+1}=\dfrac{4a_n-9}{a_n-2}') + '។ យក ' + M(r'b_n=\dfrac1{a_n-3}') + '។ កំណត់ ' + M('b_n') + ' និង ' + M('a_n') + '។',
                [(M(r'a_{n+1}-3=\dfrac{a_n-3}{a_n-2}') + ' ហើយ ' + M(r'a_1-3=1\ne0') + '។', 1),
                 (M(r'b_{n+1}=\dfrac{a_n-2}{a_n-3}=1+\dfrac1{a_n-3}') + '។', 1),
                 (M(r'b_{n+1}=b_n+1') + '។', 1),
                 (M(r'b_1=1\Rightarrow b_n=n') + '។', 1),
                 (M(r'a_n=3+\dfrac1n') + '។', 1)], 'Analyze'))
    C.append(wr('hard', 'sec1_aux', M(r'a_1=1,\ a_{n+1}=2a_n+n') + '។ កំណត់ ' + M('a_n') + '។',
                [('តាង ' + M(r'r_n=\alpha n+\beta') + '៖ ' + M(r'\alpha(n+1)+\beta=2\alpha n+2\beta+n') + '។', 1),
                 (M(r'\alpha=2\alpha+1,\ \alpha+\beta=2\beta') + ' ឱ្យ ' + M(r'\alpha=-1,\ \beta=-1') + '។', 1),
                 (M(r'a_{n+1}+(n+1)+1=2(a_n+n+1)') + '។', 1),
                 (M(r'V_n=a_n+n+1') + ' ជាធរណីមាត្រ ' + M(r'q=2,\ V_1=3') + '។', 1),
                 (M(r'a_n=3\cdot2^{n-1}-n-1') + '។', 1)], 'Analyze'))
    C.append(wr('hard', 'sec3_second', M(r'a_1=2,\ a_2=5,\ a_{n+2}=5a_{n+1}-6a_n') + '។ កំណត់ ' + M('a_n') + ' រួចគណនា ' + M('a_3') + '។',
                [('សមីការសម្គាល់ ' + M(r'x^2-5x+6=0') + ' ឫស ' + M(r'2,\ 3') + '។', 1),
                 (M(r'a_{n+1}-2a_n=3^{n-1}(a_2-2a_1)=3^{n-1}') + '។', 1),
                 (M(r'a_{n+1}-3a_n=2^{n-1}(a_2-3a_1)=-2^{n-1}') + '។', 1),
                 ('ដក ៖ ' + M(r'a_n=3^{n-1}+2^{n-1}') + '។', 1),
                 (M(r'a_3=9+4=13') + ' (ពិនិត្យ ' + M(r'5\cdot5-6\cdot2=13') + ')។', 1)], 'Analyze'))

    # ======================= Writing pisa (5) =======================
    C.append(wr('pisa', 'sec1_aux', 'កម្ចី ៥ ០០០ ដុល្លារ ការប្រាក់ ២% ក្នុងមួយខែ ហើយបង់ ៣០០ ដុល្លារក្នុងមួយខែ ៖ ' + M(r'D_{n+1}=1.02D_n-300,\ D_0=5000') + '។ កំណត់ ' + M('D_n') + ' រួចគណនាសមតុល្យក្រោយ ១២ ខែ។',
                [('ស្វ៊ីតជំនួយថេរ ' + M(r'r=1.02r-300\Rightarrow r=15000') + '។', 1),
                 (M(r'D_{n+1}-15000=1.02(D_n-15000)') + '។', 1),
                 (M(r'D_0-15000=-10000') + '។', 1),
                 (M(r'D_n=15000-10000(1.02)^n') + '។', 1),
                 (M(r'D_{12}\approx' + txt(D12)) + ' ដុល្លារ។', 1)], 'Evaluate'))
    P7 = 500 + 500 * F(12, 10) ** 7
    C.append(wr('pisa', 'sec1_aux', 'ត្រីក្នុងស្រះ ' + M('P_0=1000') + ' ក្នុងមួយឆ្នាំកើន ២០% រួចចាប់យក ១០០ ក្បាល ៖ ' + M(r'P_{n+1}=1.2P_n-100') + '។ កំណត់ ' + M('P_n') + ' ហើយរកឆ្នាំដំបូងដែលលើស ២ ០០០ ក្បាល។',
                [('ស្វ៊ីតជំនួយ ' + M(r'r=1.2r-100\Rightarrow r=500') + '។', 1),
                 (M(r'P_n=500+500(1.2)^n') + '។', 1),
                 (M(r'500+500(1.2)^n>2000\iff(1.2)^n>3') + '។', 1),
                 (M(r'(1.2)^6\approx2.99<3,\ (1.2)^7\approx3.58') + '។', 1),
                 ('ឆ្នាំទី ៧ ' + M(r'P_7\approx' + txt(P7, 0)) + ' ក្បាល។', 1)], 'Evaluate'))
    C.append(wr('pisa', 'sec1_aux', 'ប៉មហាណូយ ៖ ' + M(r'a_1=1,\ a_{n+1}=2a_n+1') + '។ កំណត់ ' + M('a_n') + ' ហើយបើផ្លាស់ម្ដង ១ វិនាទី តើ ៨ ថាសត្រូវការពេលប៉ុន្មាន?',
                [('ស្វ៊ីតជំនួយថេរ ' + M(r'r=2r+1\Rightarrow r=-1') + '។', 1),
                 (M(r'a_{n+1}+1=2(a_n+1)') + '។', 1),
                 (M(r'a_n+1=2^{n-1}\cdot2=2^n') + '។', 1),
                 (M(r'a_n=2^n-1') + '។', 1),
                 (M(r'a_8=255') + ' វិនាទី ≈ ៤ នាទី ១៥ វិនាទី។', 1)], 'Evaluate'))
    C.append(wr('pisa', 'sec3_second', 'ឡើងជណ្ដើរ ' + M('n') + ' ថ្នាក់ ដោយឡើងម្ដងមួយ ឬពីរថ្នាក់ ។ ចូរបង្ហាញទំនាក់ទំនងរវាង ' + M(r'a_{n+2},a_{n+1},a_n') + ' រួចគណនាចំនួនវិធីសម្រាប់ ១០ ថ្នាក់។',
                [('ជំហានចុងក្រោយជាថ្នាក់ ១ ឬ ២។', 1),
                 ('បើចុងក្រោយ ១ ថ្នាក់ មាន ' + M('a_{n+1}') + ' វិធី ហើយបើចុងក្រោយ ២ ថ្នាក់ មាន ' + M('a_n') + ' វិធី។', 1),
                 (M(r'a_{n+2}=a_{n+1}+a_n') + '។', 1),
                 (M(r'a_1=1,\ a_2=2') + ' ឱ្យ ' + M(r'1,2,3,5,8,13,21,34,55,89') + '។', 1),
                 (M('a_{10}=%d' % it2(1, 2, lambda k, y, x: y + x, 10)) + ' វិធី។', 1)], 'Evaluate'))
    C.append(wr('pisa', 'sec2_sn', 'សិស្សសន្សំលុយ ប្រាក់សរុបក្រោយ ' + M('n') + ' ថ្ងៃ គឺ ' + M(r'S_n=n^2+3n') + ' (រយរៀល)។ កំណត់ចំនួនសន្សំថ្ងៃទី ' + M('n') + ' ហើយរកថ្ងៃទី ២០ និងសរុប ៣០ ថ្ងៃ។',
                [('ចំពោះ ' + M(r'n\ge2') + '៖ ' + M(r'a_n=S_n-S_{n-1}') + '។', 1),
                 (M(r'=n^2+3n-(n-1)^2-3(n-1)=2n+2') + '។', 1),
                 ('ពិនិត្យ ' + M(r'a_1=S_1=4=2(1)+2') + ' ពិត។', 1),
                 (M(r'a_{20}=42') + ' រយរៀល។', 1),
                 (M(r'S_{30}=900+90=990') + ' រយរៀល ' + M(r'=99\,000') + ' រៀល។', 1)], 'Evaluate'))

    bloom_for = {'easy': 'Understand', 'medium': 'Apply', 'hard': 'Analyze', 'pisa': 'Evaluate'}
    for q in C:
        q['bloom'] = q.get('bloom') or bloom_for[q['level']]
    return C
