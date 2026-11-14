"""G11 Lesson 4 — ផលបូកតួនៃស្វ៊ីតផ្សេងៗ (sums of other sequences, sigma notation, difference sequences).
Every numeric answer is computed here (not typed) so the bank cannot disagree with the maths."""
from fractions import Fraction as F
from lib import M, mcq, wr

LESSON = 'ផលបូកតួនៃស្វ៊ីតផ្សេងៗ'
CHAPTER = 'ជំពូកទី 1 : ស្វ៊ីតនិងអនុមានរួមគណិតវិទ្យា'


def with_img(q, svg):
    q['img'] = svg
    return q


def s1(n): return n * (n + 1) // 2
def s2(n): return n * (n + 1) * (2 * n + 1) // 6
def s3(n): return s1(n) ** 2


def frac(f):
    f = F(f)
    return M(str(f.numerator)) if f.denominator == 1 else M(r'\dfrac{%d}{%d}' % (f.numerator, f.denominator))


def ints(*xs): return [M(str(x)) for x in xs]


# ---- figures ------------------------------------------------------------------
def _dots():
    cols = {1: '#0d9488', 2: '#2563eb', 3: '#d97706', 4: '#dc2626'}
    out = []
    for i in range(1, 5):
        for j in range(1, 5):
            out.append("<circle cx='%d' cy='%d' r='9' fill='%s'/>" % (40 + 36 * (i - 1), 150 - 36 * (j - 1), cols[max(i, j)]))
    return ''.join(out)


FIG_ODD_SQUARE = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 300 190' width='300' height='190'>" + _dots() +
                  "<text x='235' y='155' font-family='Times New Roman, serif' font-size='14' fill='#0d9488'>1</text>"
                  "<text x='235' y='119' font-family='Times New Roman, serif' font-size='14' fill='#2563eb'>3</text>"
                  "<text x='235' y='83' font-family='Times New Roman, serif' font-size='14' fill='#d97706'>5</text>"
                  "<text x='235' y='47' font-family='Times New Roman, serif' font-size='14' fill='#dc2626'>7</text>"
                  "<text x='150' y='184' text-anchor='middle' font-family='Times New Roman, serif' font-size='13' fill='#334155'>1 + 3 + 5 + 7 = 4²</text></svg>")


def _table(rows):
    """rows: list of (label, [values], x-offset in cells)."""
    out = ["<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 150' width='400' height='150'>"]
    for r, (lab, vals, off) in enumerate(rows):
        y = 34 + r * 42
        out.append("<text x='20' y='%d' font-family='Times New Roman, serif' font-style='italic' font-size='15' fill='#334155'>%s</text>" % (y, lab))
        for c, v in enumerate(vals):
            x = 70 + (c + off) * 52
            out.append("<text x='%d' y='%d' text-anchor='middle' font-family='Times New Roman, serif' font-size='16' fill='#1e40af'>%s</text>" % (x, y, v))
    out.append('</svg>')
    return ''.join(out)


FIG_DIFF = _table([('a', [1, 3, 7, 13, 21, 31], 0), ('b', [2, 4, 6, 8, 10], 0.5), ('c', [2, 2, 2, 2], 1)])


def cands():
    C = []

    # ======================= MCQ easy (10) =======================
    C.append(mcq('easy', 'sec1_formula', 'ផលបូក ' + M(r'1+2+3+\dots+n') + ' ស្មើនឹង ៖',
                 M(r'\dfrac{n(n+1)}{2}'), [M(r'\dfrac{n(n+1)(2n+1)}{6}'), M(r'n(n+1)'), M(r'\dfrac{n^2}{2}')],
                 'ជាផលបូកតួនៃស្វ៊ីតនព្វន្ត ' + M(r'S_n=\dfrac{n(1+n)}{2}') + '។', 'Remember'))
    C.append(mcq('easy', 'sec1_formula', 'ផលបូក ' + M(r'1^2+2^2+3^2+\dots+n^2') + ' ស្មើនឹង ៖',
                 M(r'\dfrac{n(n+1)(2n+1)}{6}'), [M(r'\dfrac{n(n+1)}{2}'), M(r'\left[\dfrac{n(n+1)}{2}\right]^2'), M(r'\dfrac{n(n+1)(n+2)}{6}')],
                 'រូបមន្តស្តង់ដារនៃផលបូកការេ។', 'Remember'))
    C.append(mcq('easy', 'sec1_formula', 'ផលបូក ' + M(r'1^3+2^3+3^3+\dots+n^3') + ' ស្មើនឹង ៖',
                 M(r'\left[\dfrac{n(n+1)}{2}\right]^2'), [M(r'\dfrac{n(n+1)(2n+1)}{6}'), M(r'\dfrac{n^2(n+1)}{4}'), M(r'\dfrac{n(n+1)}{2}')],
                 'ផលបូកស៊ុបគូបស្មើការេនៃ ' + M(r'1+2+\dots+n') + '។', 'Remember'))
    C.append(with_img(mcq('easy', 'sec2_pattern', 'ពីគំនូរ លំនាំ ' + M(r'1+3+5+7') + ' បង្កើតបានរាងការេ។ ដូច្នេះ ' + M(r'1+3+5+\dots+(2n-1)') + ' ស្មើ ៖',
                 M(r'n^2'), [M(r'n(n+1)'), M(r'2n'), M(r'n^2+1')],
                 M(r'1=1^2,\ 1+3=2^2,\ 1+3+5=3^2') + ' ទើបបាន ' + M(r'n^2') + '។', 'Understand'), FIG_ODD_SQUARE))
    C.append(mcq('easy', 'sec2_pattern', 'ផលបូក ' + M(r'2+4+6+\dots+2n') + ' ស្មើនឹង ៖',
                 M(r'n(n+1)'), [M(r'n^2'), M(r'2n'), M(r'\dfrac{n(n+1)}{2}')],
                 M(r'2+4+\dots+2n=2(1+2+\dots+n)=n(n+1)') + '។', 'Understand'))
    C.append(mcq('easy', 'sec3_sigma', M(r'\sum_{k=1}^{6} 2') + ' ស្មើនឹង ៖',
                 M('12'), ints(2, 8, 21), 'ជាផលបូកចំនួនថេរ ២ ចំនួន ៦ ដង៖ ' + M(r'6\times2=12') + '។', 'Understand'))
    C.append(mcq('easy', 'sec1_formula', M(r'1+2+3+\dots+10') + ' ស្មើនឹង ៖',
                 M(s1(10)), ints(50, 100, 110), M(r'\dfrac{10\times11}{2}=55') + '។', 'Apply'))
    C.append(mcq('easy', 'sec1_formula', M(r'1^2+2^2+3^2+4^2') + ' ស្មើនឹង ៖',
                 M(s2(4)), ints(10, 100, 20), M(r'1+4+9+16=30') + '។', 'Apply'))
    C.append(mcq('easy', 'sec3_prop', M(r'\sum_{k=1}^{n} c') + ' (ជាចំនួនថេរ ' + M('c') + ') ស្មើនឹង ៖',
                 M(r'nc'), [M(r'c'), M(r'c^n'), M(r'c+n')], 'បូក ' + M('c') + ' ចំនួន ' + M('n') + ' ដង។', 'Remember'))
    C.append(mcq('easy', 'sec4_diff1', 'ផលសងតួលំដាប់ទី ១ នៃស្វ៊ីត ' + M(r'(a_n)') + ' កំណត់ដោយ ៖',
                 M(r'b_n=a_{n+1}-a_n'), [M(r'b_n=a_{n+1}+a_n'), M(r'b_n=\dfrac{a_{n+1}}{a_n}'), M(r'b_n=a_n-a_1')],
                 'ជាផលសងនៃតួបន្តបន្ទាប់។', 'Remember'))

    # ======================= MCQ medium (14) =======================
    C.append(mcq('medium', 'sec3_prop', M(r'\sum_{k=1}^{20}(3k+1)') + ' ស្មើនឹង ៖',
                 M(650), ints(630, 660, 1260), M(r'3\times210+20=650') + '។', 'Apply'))
    C.append(mcq('medium', 'sec3_prop', M(r'\sum_{k=1}^{7}2^k') + ' ស្មើនឹង ៖',
                 M(254), ints(127, 128, 255), M(r'2+4+8+16+32+64+128=254') + '។', 'Apply'))
    C.append(mcq('medium', 'sec3_prop', M(r'\sum_{k=4}^{14}(4k-3)') + ' ស្មើនឹង ៖',
                 M(363), ints(396, 330, 407), M(r'4\times99-3\times11=363') + ' (មាន ១១ តួ ហើយ ' + M(r'\sum_{k=4}^{14}k=99') + ')។', 'Apply'))
    C.append(mcq('medium', 'sec3_prop', M(r'\sum_{k=1}^{30}k(k+1)') + ' ស្មើនឹង ៖',
                 M(9920), ints(9455, 465, 14415), M(r'\sum k^2+\sum k=9455+465=9920') + '។', 'Apply'))
    C.append(mcq('medium', 'sec3_prop', M(r'\sum_{k=1}^{15}(4k+3)') + ' ស្មើនឹង ៖',
                 M(525), ints(480, 495, 1050), M(r'4\times120+45=525') + '។', 'Apply'))
    C.append(mcq('medium', 'sec1_formula', M(r'\sum_{k=1}^{11}k^2') + ' ស្មើនឹង ៖',
                 M(s2(11)), ints(66, 726, 1331), M(r'\dfrac{11\times12\times23}{6}=506') + '។', 'Apply'))
    C.append(mcq('medium', 'sec1_formula', M(r'\sum_{k=1}^{15}k^3') + ' ស្មើនឹង ៖',
                 M(s3(15)), ints(1240, 120, 3600), M(r'\left(\dfrac{15\times16}{2}\right)^2=120^2=14400') + '។', 'Apply'))
    C.append(mcq('medium', 'sec1_formula', M(r'1^3+2^3+\dots+10^3') + ' ស្មើនឹង ៖',
                 M(s3(10)), ints(385, 3000, 3250), M(r'55^2=3025') + '។', 'Apply'))
    C.append(mcq('medium', 'sec3_sigma', 'ផលបូក ' + M(r'2+4+6+\dots+100') + ' សរសេរដោយស៊ិចម៉ាបាន ៖',
                 M(r'\sum_{k=1}^{50}2k'), [M(r'\sum_{k=1}^{100}2k'), M(r'\sum_{k=1}^{50}k'), M(r'\sum_{k=2}^{50}2k')],
                 M(r'2k') + ' ជាតួទូទៅ ហើយ ' + M('100=2\\times50') + ' ដូច្នេះ ' + M('k') + ' ពី ១ ដល់ ៥០។', 'Understand'))
    C.append(mcq('medium', 'sec3_sigma', M(r'\sum_{n=2}^{5}(2n+1)') + ' ស្មើនឹង ៖',
                 M(32), ints(35, 24, 27), M(r'5+7+9+11=32') + ' (ចាប់ពី ' + M('n=2') + ' មាន ៤ តួ)។', 'Apply'))
    C.append(mcq('medium', 'sec1_telesc', M(r'\dfrac{1}{1\cdot2}+\dfrac{1}{2\cdot3}+\dots+\dfrac{1}{9\cdot10}') + ' ស្មើនឹង ៖',
                 frac(F(9, 10)), [frac(F(10, 11)), frac(F(1, 10)), frac(F(8, 9))],
                 M(r'1-\dfrac{1}{10}=\dfrac{9}{10}') + ' ព្រោះ ' + M(r'\dfrac{1}{k(k+1)}=\dfrac1k-\dfrac1{k+1}') + '។', 'Apply'))
    C.append(with_img(mcq('medium', 'sec4_diff1', 'ស្វ៊ីត ' + M(r'1,3,7,13,21,31,\dots') + ' មានតួទូទៅ ' + M(r'a_n=n^2-n+1') + '។ តួទី ៧ ស្មើ ៖',
                 M(43), ints(41, 49, 57), M(r'7^2-7+1=43') + ' (ផលសងបន្ទាប់គឺ ' + M('12') + ' ហើយ ' + M('31+12=43') + ')។', 'Apply'), FIG_DIFF))
    C.append(mcq('medium', 'sec3_prop', 'បើ ' + M(r'\sum_{k=1}^{n}a_k=10') + ' និង ' + M(r'\sum_{k=1}^{n}b_k=7') + ' នោះ ' + M(r'\sum_{k=1}^{n}(2a_k-3b_k)') + ' ស្មើ ៖',
                 M(-1), ints(1, 41, -11), M(r'2\times10-3\times7=-1') + ' តាមលក្ខណៈលីនេអ៊ែរនៃស៊ិចម៉ា។', 'Apply'))

    C.append(mcq('medium', 'sec1_formula', M(r'\sum_{k=1}^{24}k^2') + ' ស្មើនឹង ៖',
                 M(s2(24)), ints(300, 14400, 4950), M(r'\dfrac{24\times25\times49}{6}=4900') + '។', 'Apply'))

    # ======================= MCQ hard (7) =======================
    C.append(mcq('hard', 'sec1_formula', M(r'12^3+13^3+\dots+50^3') + ' ស្មើនឹង ៖',
                 M(1621269), ints(1625625, 1616913, 1275), M(r'1275^2-66^2=1625625-4356=1621269') + '។', 'Analyze'))
    C.append(mcq('hard', 'sec3_prop', 'ដោយប្រើ ' + M(r'\sum_{k=1}^{n}(3+k)^2=\dfrac{n}{6}(2n^2+21n+73)') + ' តម្លៃនៅ ' + M(r'n=3') + ' គឺ ៖',
                 M(77), ints(54, 154, 49), M(r'\dfrac36(18+63+73)=77') + ' ពិនិត្យ ' + M(r'16+25+36=77') + '។', 'Analyze'))
    C.append(mcq('hard', 'sec1_formula', M(r'1\times2+2\times3+3\times4+\dots+28\times29') + ' ស្មើនឹង ៖',
                 M(8120), ints(8091, 8555, 4060), M(r'\dfrac{n(n+1)(n+2)}{3}=\dfrac{28\cdot29\cdot30}{3}=8120') + '។', 'Analyze'))
    C.append(mcq('hard', 'sec4_diff2', 'ស្វ៊ីត ' + M(r'1,5,14,30,55,\dots') + ' មានតួទី ' + M('n') + ' ជាផលបូកការេ ' + M(r'a_n=1^2+2^2+\dots+n^2') + '។ តួទី ៨ ស្មើ ៖',
                 M(204), ints(196, 225, 140), M(r'\dfrac{8\cdot9\cdot17}{6}=204') + '។', 'Analyze'))
    C.append(mcq('hard', 'sec4_diff2', 'ស្វ៊ីត ' + M(r'1,2,5,12,27,58,121,\dots') + ' មានតួទូទៅ ' + M(r'a_n=2^n-n') + '។ តួទី ៨ ស្មើ ៖',
                 M(248), ints(256, 250, 247), M(r'2^8-8=248') + ' (ផលសងលំដាប់ទី ២ គឺ ' + M(r'2^n') + ')។', 'Analyze'))
    C.append(mcq('hard', 'sec1_telesc', M(r'\sum_{k=1}^{n}\dfrac{1}{k(k+1)(k+2)}=\dfrac12\left(\dfrac12-\dfrac{1}{(n+1)(n+2)}\right)') + ' នៅ ' + M('n=3') + ' ស្មើ ៖',
                 frac(F(9, 40)), [frac(F(1, 4)), frac(F(27, 60)), frac(F(7, 20))],
                 M(r'\dfrac12\left(\dfrac12-\dfrac1{20}\right)=\dfrac{9}{40}') + ' ពិនិត្យ ' + M(r'\dfrac16+\dfrac1{24}+\dfrac1{60}=\dfrac{9}{40}') + '។', 'Analyze'))
    C.append(mcq('hard', 'sec1_formula', M(r'\sum_{k=12}^{24}k^2') + ' ស្មើនឹង ៖',
                 M(s2(24) - s2(11)), ints(s2(24), s2(24) - s2(12), 4900 + 506), M(r'4900-506=4394') + ' (ដក ' + M(r'\sum_{k=1}^{11}k^2') + ' មិនមែន ១២)។', 'Analyze'))

    # ======================= MCQ pisa (5) =======================
    C.append(mcq('pisa', 'sec1_formula', 'អ្នកលក់ផ្លែក្រូចរៀបជាពីរ៉ាមីតមានគ្រឹះការេ ៩×៩ ជាន់ទី ១ មាន ៨១ ផ្លែ ជាន់បន្ទាប់ ៦៤, ៤៩, ... រហូតដល់ ១ ផ្លែ ។ ផ្លែក្រូចទាំងអស់មាន ៖',
                 M(s2(9)), ints(s2(8), 405, 729), M(r'1^2+2^2+\dots+9^2=\dfrac{9\cdot10\cdot19}{6}=285') + '។', 'Evaluate'))
    C.append(mcq('pisa', 'sec1_formula', 'កុមារម្នាក់សន្សំលុយថ្ងៃទី ' + M('k') + ' បាន ' + M('1000k') + ' រៀល ក្នុងរយៈពេល ៣០ ថ្ងៃ ។ ចំនួនលុយសរុបគឺ ៖',
                 M(465000), ints(30000, 450000, 930000), M(r'1000\times\dfrac{30\cdot31}{2}=465000') + ' រៀល។', 'Evaluate'))
    C.append(mcq('pisa', 'sec1_formula', 'គ្រាប់បាល់រៀបជាពីរ៉ាមីតត្រីកោណ ជាន់ទី ' + M('k') + ' មាន ' + M(r'\dfrac{k(k+1)}{2}') + ' គ្រាប់ ។ ជាន់ ១០ ជាន់មានសរុប ៖',
                 M(220), ints(55, 385, 210), M(r'\sum\dfrac{k(k+1)}2=\dfrac{10\cdot11\cdot12}{6}=220') + '។', 'Evaluate'))
    C.append(mcq('pisa', 'sec1_formula', 'លំនាំ ១, ៨, ២៧, ៦៤, ១២៥ ជាគូបនៃ ១ ដល់ ៥ ។ ផលបូកទាំង ៥ ស្មើការេនៃចំនួនមួយ។ ចំនួននោះគឺ ៖',
                 M(15), ints(25, 55, 125), M(r'1+8+27+64+125=225=15^2') + '។', 'Evaluate'))
    C.append(mcq('pisa', 'sec1_telesc', 'អ្នករត់ម្នាក់រត់ជុំទី ' + M('k') + ' បានចម្ងាយ ' + M(r'\dfrac{1}{k(k+1)}') + ' នៃគន្លងរត់ទាំងមូល ។ បន្ទាប់ពី ៩៩ ជុំ អ្នកនោះបានរត់ប៉ុន្មានភាគនៃគន្លង ?',
                 frac(F(99, 100)), [frac(F(1, 100)), frac(F(98, 99)), frac(F(100, 101))],
                 M(r'1-\dfrac1{100}=\dfrac{99}{100}') + ' (ផលបូកកាត់គ្នាជាបន្តបន្ទាប់)។', 'Evaluate'))

    # ======================= Writing easy (1) =======================
    C.append(wr('easy', 'sec1_formula', 'សរសេរ ' + M(r'1^2+2^2+\dots+12^2') + ' ដោយស៊ិចម៉ា រួចគណនាតម្លៃ ។',
                [(M(r'1^2+2^2+\dots+12^2=\sum_{k=1}^{12}k^2') + '។', 1),
                 ('ប្រើរូបមន្ត ' + M(r'\dfrac{n(n+1)(2n+1)}{6}') + ' ជាមួយ ' + M('n=12') + '។', 1),
                 (M(r'\dfrac{12\times13\times25}{6}') + '។', 1),
                 (M(r'=2\times13\times25') + '។', 1),
                 (M(str(s2(12))) + '។', 1)], 'Apply'))

    # ======================= Writing medium (4) =======================
    C.append(wr('medium', 'sec3_prop', 'គណនា ' + M(r'\sum_{k=1}^{15}(k^2+2k)') + ' ។',
                [('បំបែក ' + M(r'\sum(k^2+2k)=\sum k^2+2\sum k') + '។', 1),
                 (M(r'\sum_{k=1}^{15}k^2=\dfrac{15\cdot16\cdot31}{6}=1240') + '។', 1),
                 (M(r'\sum_{k=1}^{15}k=120') + '។', 1),
                 (M(r'2\times120=240') + '។', 1),
                 (M(r'1240+240=1480') + '។', 1)], 'Apply'))
    C.append(wr('medium', 'sec4_diff1', 'កំណត់តួទី ' + M('n') + ' នៃស្វ៊ីត ' + M(r'3,5,9,15,23,\dots') + ' រួចរកតួទី ១០ ។',
                [('ផលសង ' + M(r'b_n:2,4,6,8,\dots') + ' ជាស្វ៊ីតនព្វន្ត ' + M(r'b_n=2n') + '។', 1),
                 (M(r'a_n=3+\sum_{k=1}^{n-1}2k') + '។', 1),
                 (M(r'=3+n(n-1)') + '។', 1),
                 (M(r'a_n=n^2-n+3') + ' (ពិនិត្យ ' + M('a_1=3') + ')។', 1),
                 (M(r'a_{10}=100-10+3=93') + '។', 1)], 'Apply'))
    C.append(wr('medium', 'sec1_telesc', 'គណនា ' + M(r'S=\dfrac{1}{1\cdot2}+\dfrac{1}{2\cdot3}+\dots+\dfrac{1}{19\cdot20}') + ' ។',
                [('ប្រើ ' + M(r'\dfrac{1}{k(k+1)}=\dfrac1k-\dfrac1{k+1}') + '។', 1),
                 ('សរសេរ ' + M(r'S=\left(1-\dfrac12\right)+\left(\dfrac12-\dfrac13\right)+\dots+\left(\dfrac1{19}-\dfrac1{20}\right)') + '។', 1),
                 ('តួកណ្ដាលកាត់គ្នាអស់ ។', 1),
                 (M(r'S=1-\dfrac1{20}') + '។', 1),
                 (M(r'S=\dfrac{19}{20}') + '។', 1)], 'Apply'))
    C.append(wr('medium', 'sec3_prop', 'គណនា ' + M(r'\sum_{k=1}^{10}(2k-1)^2') + ' ។',
                [('ពន្លាត ' + M(r'(2k-1)^2=4k^2-4k+1') + '។', 1),
                 (M(r'\sum=4\sum k^2-4\sum k+\sum1') + '។', 1),
                 (M(r'4\times385-4\times55+10') + '។', 1),
                 (M(r'1540-220+10') + '។', 1),
                 (M(str(sum((2 * k - 1) ** 2 for k in range(1, 11)))) + '។', 1)], 'Apply'))

    # ======================= Writing hard (4) =======================
    C.append(wr('hard', 'sec4_diff1', 'ស្វ៊ីត ' + M(r'2,3,6,11,18,\dots') + ' ។ (ក) កំណត់ ' + M('a_n') + ' (ខ) គណនា ' + M(r'S_n=a_1+\dots+a_n') + ' ។',
                [('ផលសង ' + M(r'b_n:1,3,5,7') + ' មាន ' + M(r'b_n=2n-1') + '។', 1),
                 (M(r'a_n=2+\sum_{k=1}^{n-1}(2k-1)=2+(n-1)^2=n^2-2n+3') + '។', 1),
                 (M(r'S_n=\sum k^2-2\sum k+3n') + '។', 1),
                 (M(r'=\dfrac{n(n+1)(2n+1)}{6}-n(n+1)+3n') + '។', 1),
                 (M(r'S_n=\dfrac{n}{6}(2n^2-3n+13)') + '។', 1)], 'Analyze'))
    C.append(wr('hard', 'sec3_prop', 'បង្ហាញថា ' + M(r'\sum_{k=1}^{n}k(k+1)=\dfrac{n(n+1)(n+2)}{3}') + ' ។',
                [(M(r'k(k+1)=k^2+k') + '។', 1),
                 (M(r'\sum k(k+1)=\sum k^2+\sum k') + '។', 1),
                 (M(r'=\dfrac{n(n+1)(2n+1)}{6}+\dfrac{n(n+1)}{2}') + '។', 1),
                 (M(r'=\dfrac{n(n+1)}{6}\bigl[(2n+1)+3\bigr]') + '។', 1),
                 (M(r'=\dfrac{n(n+1)(2n+4)}{6}=\dfrac{n(n+1)(n+2)}{3}') + '។', 1)], 'Analyze'))
    C.append(wr('hard', 'sec4_diff2', 'កំណត់តួទី ' + M('n') + ' នៃស្វ៊ីត ' + M(r'2,3,6,12,22,37,\dots') + ' ដោយប្រើផលសងលំដាប់ទី ២ ។',
                [(M(r'b_n:1,3,6,10,15') + ' និង ' + M(r'c_n:2,3,4,5') + '។', 1),
                 (M(r'c_n=n+1') + ' ជាស្វ៊ីតនព្វន្ត ' + M(r'c_1=2,\ d=1') + '។', 1),
                 (M(r'b_n=1+\sum_{k=1}^{n-1}(k+1)=\dfrac{n(n+1)}{2}') + '។', 1),
                 (M(r'a_n=2+\sum_{k=1}^{n-1}\dfrac{k(k+1)}{2}=2+\dfrac{(n-1)n(n+1)}{6}') + '។', 1),
                 ('ពិនិត្យ ' + M(r'a_6=2+\dfrac{5\cdot6\cdot7}{6}=37') + '។', 1)], 'Analyze'))
    C.append(wr('hard', 'sec4_diff1', 'ស្វ៊ីត ' + M(r'(a_n):p,q,p,q,p,q,\dots') + ' ។ កំណត់ ' + M('a_n') + ' ហើយគណនាផលបូក ' + M('2m') + ' តួដំបូង ។',
                [('ពេល ' + M('n') + ' សេស ' + M('a_n=p') + ' ពេល ' + M('n') + ' គូ ' + M('a_n=q') + '។', 1),
                 ('សរសេរ ' + M(r'a_n=\dfrac{p+q}{2}+(-1)^{n+1}\dfrac{p-q}{2}') + '។', 1),
                 ('ពិនិត្យ ' + M('n=1') + ' បាន ' + M('p') + ' ហើយ ' + M('n=2') + ' បាន ' + M('q') + '។', 1),
                 ('ក្នុង ' + M('2m') + ' តួមានគូ ' + M('(p,q)') + ' ចំនួន ' + M('m') + '។', 1),
                 (M(r'S_{2m}=m(p+q)') + '។', 1)], 'Analyze'))

    # ======================= Writing pisa (5) =======================
    C.append(wr('pisa', 'sec1_formula', 'អ្នកលក់ផ្លែឈើរៀបផ្លែក្រូចជាពីរ៉ាមីតមាន ១០ ជាន់ ដោយជាន់ទី ' + M('k') + ' (រាប់ពីកំពូល) មាន ' + M('k^2') + ' ផ្លែ ។ រកចំនួនផ្លែសរុប និងបើលក់ផ្លែមួយ ៥០០ រៀល តើបានប្រាក់ប៉ុន្មាន ?',
                [('ចំនួនផ្លែសរុប ' + M(r'1^2+2^2+\dots+10^2=\sum_{k=1}^{10}k^2') + '។', 1),
                 ('រូបមន្ត ' + M(r'\dfrac{n(n+1)(2n+1)}{6}') + '។', 1),
                 (M(r'\dfrac{10\times11\times21}{6}=385') + ' ផ្លែ។', 1),
                 (M(r'385\times500') + ' រៀល។', 1),
                 (M(str(385 * 500)) + ' រៀល។', 1)], 'Evaluate'))
    C.append(wr('pisa', 'sec1_formula', 'សិស្សម្នាក់សន្សំលុយថ្ងៃទី ' + M('k') + ' បាន ' + M('k^2') + ' រយរៀល ក្នុងរយៈពេល ១២ ថ្ងៃ ។ គណនាប្រាក់សរុបជារៀល ។',
                [('ប្រាក់សរុប ' + M(r'\sum_{k=1}^{12}k^2') + ' រយរៀល។', 1),
                 (M(r'\dfrac{12\times13\times25}{6}') + '។', 1),
                 (M('650') + ' រយរៀល។', 1),
                 (M(r'650\times100') + '។', 1),
                 (M('65\\,000') + ' រៀល។', 1)], 'Evaluate'))
    C.append(wr('pisa', 'sec1_telesc', 'ជាងកាត់ដេរម្នាក់ ក្នុងថ្ងៃទី ' + M('k') + ' បានដេរ ' + M(r'\dfrac{1}{k(k+1)}') + ' នៃការបញ្ជាទិញ ។ (ក) បន្ទាប់ពី ' + M('n') + ' ថ្ងៃ បានភាគប៉ុន្មាន? (ខ) តើត្រូវប៉ុន្មានថ្ងៃ ទើបបាន ' + M('99\\%') + ' ?',
                [(M(r'S_n=\sum_{k=1}^{n}\left(\dfrac1k-\dfrac1{k+1}\right)') + '។', 1),
                 ('កាត់គ្នា ' + M(r'S_n=1-\dfrac{1}{n+1}=\dfrac{n}{n+1}') + '។', 1),
                 (M(r'\dfrac{n}{n+1}=0.99') + '។', 1),
                 (M(r'n=0.99n+0.99\Rightarrow0.01n=0.99') + '។', 1),
                 (M(r'n=99') + ' ថ្ងៃ។', 1)], 'Evaluate'))
    C.append(wr('pisa', 'sec2_pattern', 'ប្រាសាទបុរាណមួយសាងសង់ជាជាន់ៗ ហើយចំនួនថ្មក្នុងជាន់ទី ' + M('k') + ' ជា ' + M('3k^2-3k+1') + ' (១, ៧, ១៩, ៣៧, ...) ។ រកចំនួនថ្មសរុបក្នុង ៦ ជាន់ ។',
                [('បួនជាន់ដំបូង ' + M('1,\\ 1+7=8,\\ 1+7+19=27') + '។', 1),
                 ('សង្កេតលំនាំ ' + M('1^3,2^3,3^3') + '។', 1),
                 (M(r'\sum_{k=1}^{n}(3k^2-3k+1)=n^3') + '។', 1),
                 ('ផ្ទៀងផ្ទាត់៖ ' + M(r'3\cdot\dfrac{n(n+1)(2n+1)}{6}-3\dfrac{n(n+1)}{2}+n=n^3') + '។', 1),
                 (M(r'n=6:\ 6^3=216') + ' ថ្ម។', 1)], 'Evaluate'))
    C.append(wr('pisa', 'sec4_diff2', 'ចំនួនការេសរុបក្នុងក្រឡាចត្រង្គ ' + M(r'n\times n') + ' គឺ ១, ៥, ១៤, ៣០, ៥៥, ... (ចំពោះ ' + M('n=1,2,3,\\dots') + ') ។ កំណត់ ' + M('a_n') + ' រួចរកចំនួនការេក្នុងក្រឡា ៨×៨ ។',
                [('ផលសង ' + M(r'b_n:4,9,16,25,\dots') + ' មាន ' + M(r'b_n=(n+1)^2') + '។', 1),
                 (M(r'a_n=1+\sum_{k=1}^{n-1}(k+1)^2=\sum_{j=1}^{n}j^2') + '។', 1),
                 (M(r'a_n=\dfrac{n(n+1)(2n+1)}{6}') + '។', 1),
                 (M(r'a_8=\dfrac{8\times9\times17}{6}') + '។', 1),
                 (M(str(s2(8))) + ' ការេ។', 1)], 'Evaluate'))

    bloom_for = {'easy': 'Understand', 'medium': 'Apply', 'hard': 'Analyze', 'pisa': 'Evaluate'}
    for q in C:
        q['bloom'] = q.get('bloom') or bloom_for[q['level']]
    return C
