"""Extra Grade 11 SC questions so that every lesson PART has at least 10 questions.

Only the thin parts get new questions.  cands() returns {lesson_no: [candidate, ...]}; every candidate carries
its part title in c['part'].  Geometry answers are computed from coordinates (a unit cube A(0,0,0) B(1,0,0)
C(1,1,0) D(0,1,0) E(0,0,1) F(1,0,1) G(1,1,1) H(0,1,1)) so none of them is typed by hand."""
from fractions import Fraction as F
from math import acos, atan, degrees, sqrt, log, log10, e
from lib import M, mcq, wr
import parts as P

L = {n: P.PARTS[n][1] for n in P.PARTS}          # lesson no -> part titles


def with_img(q, svg):
    q['img'] = svg
    return q


def opts(*xs): return [M(str(x)) for x in xs]


# ---------------------------------------------------------------- geometry helpers --------------------------------
CUBE = dict(A=(0, 0, 0), B=(1, 0, 0), C=(1, 1, 0), D=(0, 1, 0), E=(0, 0, 1), F=(1, 0, 1), G=(1, 1, 1), H=(0, 1, 1))


def sub(p, q): return tuple(a - b for a, b in zip(p, q))
def dot(u, v): return sum(a * b for a, b in zip(u, v))
def cross(u, v): return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
def norm(u): return sqrt(dot(u, u))


def plane_normal(a, b, c): return cross(sub(b, a), sub(c, a))


def plane_angle(p1, p2):
    """dihedral angle (degrees, 0..90) between planes given as three cube-vertex names each."""
    n1 = plane_normal(*[CUBE[k] for k in p1[:3]]); n2 = plane_normal(*[CUBE[k] for k in p2[:3]])
    return degrees(acos(min(1.0, abs(dot(n1, n2)) / (norm(n1) * norm(n2)))))


def line_angle(l1, l2):
    u = sub(CUBE[l1[1]], CUBE[l1[0]]); v = sub(CUBE[l2[1]], CUBE[l2[0]])
    return degrees(acos(min(1.0, abs(dot(u, v)) / (norm(u) * norm(v)))))


def deg(x):
    r = round(x)
    return '%d^\\circ' % r if abs(x - r) < 1e-6 else '%.2f^\\circ' % x


# sanity checks of the geometry the questions rely on
assert abs(plane_angle('ABGH', 'ABCD') - 45) < 1e-9
assert abs(plane_angle('ACH', 'ABCD') - degrees(acos(1 / sqrt(3)))) < 1e-9
assert abs(plane_angle('ACGE', 'BDHF') - 90) < 1e-9
assert abs(plane_angle('ACGE', 'ABFE') - 45) < 1e-9
assert abs(plane_angle('ABFE', 'ABCD') - 90) < 1e-9
assert abs(line_angle('AF', 'AH') - 60) < 1e-9 and abs(line_angle('AE', 'BC') - 90) < 1e-9 and abs(line_angle('AC', 'BD') - 90) < 1e-9
assert abs(degrees(acos(F(1, 3))) - 70.5288) < 1e-3
# cube claims used for the 'which plane is perpendicular to ABCD' question: only ABFE of the offered planes is
assert abs(plane_angle('ABFE', 'ABCD') - 90) < 1e-9 and abs(plane_angle('EFGH', 'ABCD')) < 1e-9
assert abs(plane_angle('ACH', 'ABCD') - 90) > 1 and abs(plane_angle('BDE', 'ABCD') - 90) > 1
assert abs(plane_angle('ACGE', 'ABCD') - 90) < 1e-9   # (not offered as a distractor)

# ---------------------------------------------------------------- figures ----------------------------------------------
FIG_CUBE = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 180' width='200' height='180'>"
            "<g stroke='#1e3a8a' stroke-width='2' fill='none'>"
            "<rect x='40' y='70' width='80' height='80'/>"
            "<path d='M120 70 L150 40 L70 40 L40 70 M150 40 L150 120 L120 150'/></g>"
            "<g stroke='#64748b' stroke-width='1.5' stroke-dasharray='5,4' fill='none'><path d='M40 150 L70 120 L150 120 M70 120 L70 40'/></g>"
            "<g font-family='Times New Roman, serif' font-size='13' fill='#0f172a'>"
            "<text x='26' y='163'>A</text><text x='122' y='165'>B</text><text x='154' y='128'>C</text><text x='55' y='123'>D</text>"
            "<text x='26' y='70'>E</text><text x='122' y='68'>F</text><text x='154' y='42'>G</text><text x='56' y='38'>H</text></g></svg>")
FIG_PYR = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 220 190' width='220' height='190'>"
           "<g stroke='#1e3a8a' stroke-width='2' fill='none'><path d='M30 150 L130 150 L180 115 M30 150 L100 25 L130 150 M100 25 L180 115'/></g>"
           "<g stroke='#64748b' stroke-width='1.5' stroke-dasharray='5,4' fill='none'><path d='M30 150 L80 115 L180 115 M80 115 L100 25 M105 132 L100 25'/></g>"
           "<g font-family='Times New Roman, serif' font-size='13' fill='#0f172a'>"
           "<text x='15' y='160'>A</text><text x='128' y='168'>B</text><text x='184' y='120'>C</text><text x='66' y='113'>D</text>"
           "<text x='96' y='18'>S</text><text x='108' y='140'>O</text></g></svg>")


def cands():
    out = {n: [] for n in (3, 4, 8, 26, 28)}

    def add(n, part_no, q):
        q['part'] = L[n][part_no - 1]
        out[n].append(q)

    # ================= Lesson 3 -- part 1: និយមន័យស្វ៊ីតធរណីមាត្រ (+6) =================
    add(3, 1, mcq('easy', 'x', 'ស្វ៊ីតណាមួយខាងក្រោមជាស្វ៊ីតធរណីមាត្រ ?', M('3,6,12,24,\\ldots'),
                  [M('2,4,6,8,\\ldots'), M('1,4,9,16,\\ldots'), M('1,1,2,3,\\ldots')],
                  'ផលធៀបនៃតួជាប់គ្នាថេរ ' + M('6/3=12/6=24/12=2') + '។', 'Understand'))
    add(3, 1, mcq('easy', 'x', 'សមាមាត្ររួម ' + M('q') + ' នៃស្វ៊ីត ' + M('5,-10,20,-40,\\ldots') + ' គឺ ៖', M('-2'), opts(2, -5, 5),
                  M('q=\\dfrac{-10}{5}=-2') + '។', 'Apply'))
    add(3, 1, mcq('medium', 'x', 'សមាមាត្ររួមនៃស្វ៊ីត ' + M('81,27,9,3,\\ldots') + ' គឺ ៖', M(r'\dfrac13'), [M('3'), M('-3'), M(r'-\dfrac13')],
                  M('q=\\dfrac{27}{81}=\\dfrac13') + '។', 'Apply'))
    add(3, 1, mcq('medium', 'x', 'ស្វ៊ីតដែលតួទី ' + M('n') + ' កំណត់ដោយ ' + M('a_n=3n+1') + ' មិនមែនជាស្វ៊ីតធរណីមាត្រ ព្រោះ ៖',
                  'ផលធៀបតួជាប់គ្នាមិនថេរ', ['ផលសងតួជាប់គ្នាមិនថេរ', 'ស្វ៊ីតមានតួអវិជ្ជមាន', 'ស្វ៊ីតជាស្វ៊ីតកើន'],
                  M('a_1=4,a_2=7,a_3=10:\\ \\tfrac74\\ne\\tfrac{10}7') + '។', 'Analyze'))
    add(3, 1, mcq('hard', 'x', 'ស្វ៊ីតមួយមាន ' + M('a_n=3\\cdot2^{n+1}') + '។ តួទី ១ និងសមាមាត្ររួមគឺ ៖', M('a_1=12,\\ q=2'),
                  [M('a_1=6,\\ q=2'), M('a_1=12,\\ q=3'), M('a_1=3,\\ q=2')],
                  M('a_1=3\\cdot2^2=12') + ' ហើយ ' + M('\\tfrac{a_{n+1}}{a_n}=2') + '។', 'Analyze'))
    add(3, 1, wr('medium', 'x', 'បង្ហាញថាស្វ៊ីត ' + M('a_n=3\\cdot2^n') + ' ជាស្វ៊ីតធរណីមាត្រ រួចរក ' + M('q') + ' និង ' + M('a_1') + '។',
                 [('គណនា ' + M(r'\dfrac{a_{n+1}}{a_n}=\dfrac{3\cdot2^{n+1}}{3\cdot2^n}') + '។', 1), (M('=2') + ' ជាចំនួនថេរមិនសូន្យ។', 1),
                  ('ដូច្នេះជាស្វ៊ីតធរណីមាត្រ។', 1), (M('q=2') + '។', 1), (M('a_1=3\\cdot2^1=6') + '។', 1)], 'Apply'))

    # ================= Lesson 3 -- part 3: ផលគុណតួស្មើចម្ងាយពីតួចុង (+6) =================
    add(3, 3, mcq('easy', 'x', 'ក្នុងស្វ៊ីតធរណីមាត្រ ' + M('a_1,a_2,\\ldots,a_n') + ' ផលគុណតួស្មើចម្ងាយពីតួចុង គឺ ៖', M('a_1a_n=a_2a_{n-1}'),
                  [M('a_1+a_n=a_2+a_{n-1}'), M('a_1a_n=a_2a_n'), M('a_1a_2=a_{n-1}a_n')], 'តួស្មើចម្ងាយពីចុងមានផលគុណស្មើគ្នា។', 'Remember'))
    add(3, 3, mcq('easy', 'x', 'ស្វ៊ីតធរណីមាត្រ ' + M('2,6,18,54,162') + '។ ' + M('a_1\\times a_5') + ' ស្មើ ៖', M(2 * 162),
                  opts(164, 108, 972), M('2\\times162=324=6\\times54=a_2a_4') + '។', 'Apply'))
    add(3, 3, mcq('medium', 'x', 'មធ្យមធរណីមាត្រវិជ្ជមានរវាង ' + M('4') + ' និង ' + M('9') + ' គឺ ៖', M('6'), opts('6.5', 12, 36), M('b^2=4\\times9=36\\Rightarrow b=6') + '។', 'Apply'))
    add(3, 3, mcq('medium', 'x', 'បីចំនួន ' + M('3,b,12') + ' ជាស្វ៊ីតធរណីមាត្រ។ ' + M('b') + ' ស្មើ ៖', M('6') + ' ឬ ' + M('-6'),
                  [M('7.5'), M('6') + ' តែប៉ុណ្ណោះ', M('4') + ' ឬ ' + M('-4')], M('b^2=3\\times12=36\\Rightarrow b=\\pm6') + '។', 'Apply'))
    add(3, 3, mcq('hard', 'x', 'ស្វ៊ីតធរណីមាត្រមាន ' + M('a_3=4') + ' និង ' + M('a_5=36') + '។ ' + M('a_4') + ' អាចស្មើ ៖', M('12') + ' ឬ ' + M('-12'),
                  [M('20'), M('12') + ' តែប៉ុណ្ណោះ', M('16')], M('a_4^2=a_3a_5=144\\Rightarrow a_4=\\pm12') + '។', 'Analyze'))
    add(3, 3, wr('medium', 'x', 'បីចំនួន ' + M('2,x,50') + ' ជាស្វ៊ីតធរណីមាត្រ ។ រក ' + M('x') + ' និង ' + M('q') + '។',
                 [('ប្រើ ' + M('x^2=2\\times50') + '។', 1), (M('x^2=100') + '។', 1), (M('x=10') + ' ឬ ' + M('x=-10') + '។', 1),
                  ('បើ ' + M('x=10') + ' ៖ ' + M('q=\\dfrac{10}{2}=5') + '។', 1), ('បើ ' + M('x=-10') + ' ៖ ' + M('q=-5') + '។', 1)], 'Apply'))

    # ================= Lesson 4 -- part 2: គណនាផលបូកតាមលំនាំគំរូ (+7) =================
    add(4, 2, mcq('easy', 'x', M('1+3+5+\\dots+(2n-1)') + ' ចំពោះ ' + M('n=25') + ' ស្មើ ៖', M(25 ** 2), opts(50, 325, 650), M('n^2=625') + '។', 'Apply'))
    add(4, 2, mcq('easy', 'x', M('1+3+5+\\dots+99') + ' ស្មើ ៖', M(50 ** 2), opts(99, 2475, 5000), 'មាន ៥០ តួ ៖ ' + M('50^2=2500') + '។', 'Apply'))
    add(4, 2, mcq('easy', 'x', M('2+4+6+\\dots+2n') + ' ចំពោះ ' + M('n=15') + ' ស្មើ ៖', M(15 * 16), opts(225, 120, 30), M('n(n+1)=15\\times16=240') + '។', 'Apply'))
    add(4, 2, mcq('medium', 'x', M('2+4+6+\\dots+100') + ' ស្មើ ៖', M(sum(range(2, 101, 2))), opts(2500, 5050, 5100), 'មាន ៥០ តួ ៖ ' + M('50\\times51=2550') + '។', 'Apply'))
    add(4, 2, mcq('medium', 'x', 'ផលបូក ៤០ ចំនួនគូវិជ្ជមានដំបូង ស្មើ ៖', M(40 * 41), opts(1600, 820, 1680), M('n(n+1)=40\\times41=1640') + '។', 'Apply'))
    add(4, 2, mcq('medium', 'x', 'លំនាំ ' + M('1=1,\\ 1+8=9,\\ 1+8+27=36') + ' ឱ្យ ' + M('1^3+2^3+\\dots+n^3') + ' ។ ចំពោះ ' + M('n=10') + ' ស្មើ ៖', M(55 ** 2),
                  opts(385, 550, 3025 + 55), M('\\left[\\dfrac{n(n+1)}2\\right]^2=55^2=3025') + '។', 'Analyze'))
    add(4, 2, wr('hard', 'x', 'សង្កេតលំនាំ ' + M('1=1,\\ 1+5=6,\\ 1+5+9=15,\\ 1+5+9+13=28') + ' ។ កំណត់ផលបូក ' + M('n') + ' តួដំបូងនៃស្វ៊ីត ' + M('1,5,9,13,\\ldots') + ' រួចគណនាចំពោះ ' + M('n=20') + '។',
                 [('ផលបូក ' + M('1,6,15,28') + ' សរសេរជា ' + M('1\\times1,\\ 2\\times3,\\ 3\\times5,\\ 4\\times7') + '។', 1),
                  ('លំនាំ ' + M('S_n=n(2n-1)') + '។', 1), ('ផ្ទៀងផ្ទាត់ ' + M('S_4=4\\times7=28') + '។', 1),
                  ('ពិនិត្យតាមរូបមន្តនព្វន្ត ' + M('S_n=\\dfrac n2[2+4(n-1)]=n(2n-1)') + '។', 1), (M('S_{20}=20\\times39=780') + '។', 1)], 'Analyze'))

    # ================= Lesson 4 -- part 4: កំណត់តួទី n តាមផលសងតួ (+1) =================
    add(4, 4, mcq('medium', 'x', 'ស្វ៊ីត ' + M('2,5,10,17,26,\\ldots') + ' មានផលសងលំដាប់ទី ១ គឺ ' + M('3,5,7,9') + ' ។ តួទី ៨ ស្មើ ៖', M(65), opts(50, 64, 82),
                  M('a_n=n^2+1\\Rightarrow a_8=65') + ' (ផលសងបន្ទាប់ ' + M('11,13,15') + ')។', 'Apply'))

    # ================= Lesson 8 -- part 2: ការរំកិល និងការឆ្លុះក្រាបលោការីត (+8) =================
    add(8, 2, mcq('easy', 'x', 'ដែនកំណត់នៃអនុគមន៍ ' + M(r'y=\log_3(x+3)') + ' គឺ ៖', M('x>-3'), [M('x>3'), M('x>0'), M('x\\ne-3')], M('x+3>0') + '។', 'Understand'))
    add(8, 2, mcq('easy', 'x', 'អាស៊ីមតូតឈរនៃក្រាប ' + M(r'y=\log_3(x+3)') + ' គឺបន្ទាត់ ៖', M('x=-3'), [M('x=3'), M('y=-3'), M('x=0')], 'ក្រាបរំកិល ' + M('\\log_3x') + ' ទៅឆ្វេង ៣។', 'Understand'))
    add(8, 2, mcq('easy', 'x', 'ក្រាប ' + M(r'y=\log_7x+3') + ' បានមកពីក្រាប ' + M(r'y=\log_7x') + ' ដោយ ៖', 'រំកិលឡើងលើ ៣ ឯកតា', ['រំកិលទៅស្តាំ ៣ ឯកតា', 'រំកិលទៅឆ្វេង ៣ ឯកតា', 'រំកិលចុះក្រោម ៣ ឯកតា'],
                  M('+3') + ' នៅខាងក្រៅលោការីតរំកិលស្របអ័ក្ស ' + M('Oy') + '។', 'Understand'))
    add(8, 2, mcq('medium', 'x', 'ក្រាប ' + M(r'y=-\log_7x') + ' បានមកពីក្រាប ' + M(r'y=\log_7x') + ' ដោយ ៖', 'ឆ្លុះធៀបនឹងអ័ក្ស ' + M('Ox'), ['ឆ្លុះធៀបនឹងអ័ក្ស ' + M('Oy'), 'ឆ្លុះធៀបនឹងបន្ទាត់ ' + M('y=x'), 'រំកិលចុះក្រោម ១ ឯកតា'],
                  'ប្តូរសញ្ញា ' + M('y') + ' ឆ្លុះធៀបអ័ក្ស ' + M('Ox') + '។', 'Understand'))
    add(8, 2, mcq('medium', 'x', 'ក្រាបនៃ ' + M(r'y=\log_3(x-2)') + ' កាត់អ័ក្ស ' + M('Ox') + ' ត្រង់ចំណុច ៖', M('(3,0)'), [M('(1,0)'), M('(2,0)'), M('(0,3)')], M('\\log_3(x-2)=0\\Rightarrow x-2=1\\Rightarrow x=3') + '។', 'Apply'))
    add(8, 2, mcq('medium', 'x', 'ដែនកំណត់នៃ ' + M(r'y=\log_2(x-1)^2') + ' គឺ ៖', M('x\\ne1'), [M('x>1'), M('x>0'), M('x\\in\\mathbb{R}')], M('(x-1)^2>0\\Rightarrow x\\ne1') + '។', 'Analyze'))
    add(8, 2, mcq('hard', 'x', 'ក្រាបនៃ ' + M(r'y=2-\log_2x^2') + ' កាត់អ័ក្ស ' + M('Ox') + ' ត្រង់ ' + M('x') + ' ស្មើ ៖', M('x=2') + ' ឬ ' + M('x=-2'),
                  [M('x=2') + ' តែប៉ុណ្ណោះ', M('x=4') + ' ឬ ' + M('x=-4'), M('x=1') + ' ឬ ' + M('x=-1')], M('\\log_2x^2=2\\Rightarrow x^2=4\\Rightarrow x=\\pm2') + '។', 'Analyze'))
    add(8, 2, wr('medium', 'x', 'សង់តារាងតម្លៃ និងពន្យល់ក្រាប ' + M(r'y=-2+\log_3x') + '។',
                 [('ដែនកំណត់ ' + M('x>0') + '។', 1), ('តារាង ' + M('x=\\tfrac13,1,3,9') + ' ឱ្យ ' + M('\\log_3x=-1,0,1,2') + '។', 1),
                  (M('y=-3,-2,-1,0') + '។', 1), ('ក្រាបរំកិល ' + M('\\log_3x') + ' ចុះក្រោម ២ ឯកតា។', 1), ('ក្រាបកាត់អ័ក្ស ' + M('Ox') + ' ត្រង់ ' + M('(9,0)') + '។', 1)], 'Apply'))

    # ================= Lesson 8 -- part 3: រូបមន្តប្តូរគោល (+5) =================
    add(8, 3, mcq('easy', 'x', M(r'\log_ab\times\log_ba') + ' ស្មើនឹង ៖', M('1'), opts(0, 'a', 'ab'), M(r'\log_ba=\dfrac1{\log_ab}') + '។', 'Understand'))
    add(8, 3, mcq('medium', 'x', M(r'\log_8 32') + ' ស្មើនឹង ៖', M(r'\dfrac53'), [M(r'\dfrac35'), M('4'), M('3')], M(r'\dfrac{\log_232}{\log_28}=\dfrac53') + '។', 'Apply'))
    add(8, 3, mcq('medium', 'x', M(r'\log_4 8') + ' ស្មើនឹង ៖', M(r'\dfrac32'), [M(r'\dfrac23'), M('2'), M('4')], M(r'\dfrac{\log_28}{\log_24}=\dfrac32') + '។', 'Apply'))
    add(8, 3, mcq('medium', 'x', M(r'\log_{25}125') + ' ស្មើនឹង ៖', M(r'\dfrac32'), [M(r'\dfrac23'), M('5'), M('3')], M(r'\dfrac{\log_5125}{\log_525}=\dfrac32') + '។', 'Apply'))
    add(8, 3, mcq('hard', 'x', M(r'\log_25\times\log_58') + ' ស្មើនឹង ៖', M('3'), opts(40, 13, 1), M(r'\dfrac{\log5}{\log2}\cdot\dfrac{\log8}{\log5}=\log_28=3') + '។', 'Analyze'))

    # ================= Lesson 8 -- part 5: លោការីតគោល 10 និងលោការីតនេពែ (+8) =================
    add(8, 5, mcq('easy', 'x', M(r'\log1000') + ' ស្មើនឹង ៖', M('3'), opts(1, 10, 100), M('10^3=1000') + '។', 'Apply'))
    add(8, 5, mcq('easy', 'x', M(r'\log0.01') + ' ស្មើនឹង ៖', M('-2'), opts(2, -1, 0.01), M('10^{-2}=0.01') + '។', 'Apply'))
    add(8, 5, mcq('easy', 'x', M(r'\ln e^5') + ' ស្មើនឹង ៖', M('5'), opts('e', 'e^5', 1), M(r'\ln e^x=x') + '។', 'Apply'))
    add(8, 5, mcq('easy', 'x', M(r'\ln1') + ' ស្មើនឹង ៖', M('0'), opts(1, 'e', -1), M('e^0=1') + '។', 'Remember'))
    add(8, 5, mcq('medium', 'x', M('10^x=7') + ' មានចម្លើយ ៖', M('x=\\log7\\approx%.3f' % log10(7)), [M('x=\\ln7\\approx1.946'), M('x=\\dfrac7{10}'), M('x=7^{10}')], M('x=\\log_{10}7') + '។', 'Apply'))
    add(8, 5, mcq('medium', 'x', M('e^x=5') + ' មានចម្លើយ ៖', M('x=\\ln5\\approx%.3f' % log(5)), [M('x=\\log5\\approx0.699'), M('x=\\dfrac5e'), M('x=5^e')], M('x=\\log_e5=\\ln5') + '។', 'Apply'))
    add(8, 5, mcq('medium', 'x', M(r'\log2+\log5') + ' ស្មើនឹង ៖', M('1'), opts(7, 10, 0), M(r'\log(2\times5)=\log10=1') + '។', 'Apply'))
    x_ = (log(20) + 1) / 3
    add(8, 5, wr('medium', 'x', 'ដោះស្រាយសមីការ ' + M('e^{3x-1}=20') + '។',
                 [('យក ' + M('\\ln') + ' ទាំងពីរអង្គ ៖ ' + M('3x-1=\\ln20') + '។', 1), (M('3x=\\ln20+1') + '។', 1), (M('x=\\dfrac{\\ln20+1}{3}') + '។', 1),
                  (M('\\ln20\\approx%.4f' % log(20)) + '។', 1), (M('x\\approx%.3f' % x_) + '។', 1)], 'Apply'))

    # ================= Lesson 26 -- part 1: ការគូសរូបក្នុងលំហនៅលើប្លង់ (+6) =================
    add(26, 1, with_img(mcq('easy', 'x', 'ក្នុងរូបគូបគូសលើប្លង់ ទ្រនុងដែលត្រូវបាំងគូសដោយ ៖', 'បន្ទាត់ដាច់ៗ', ['បន្ទាត់ជាប់ក្រាស់', 'បន្ទាត់ពណ៌ក្រហម', 'មិនគូស'],
                       'ទ្រនុងដែលមើលឃើញគូសជាប់ ទ្រនុងដែលបាំងគូសដាច់ៗ។', 'Remember'), FIG_CUBE))
    add(26, 1, mcq('easy', 'x', 'បន្ទាត់ស្របគ្នាក្នុងលំហ ត្រូវគូសនៅលើប្លង់ដោយ ៖', 'បន្ទាត់ស្របគ្នា', ['បន្ទាត់កែងគ្នា', 'បន្ទាត់កាត់គ្នា', 'បន្ទាត់ប្រវែងស្មើគ្នា'],
                  'ភាពស្របរក្សាក្នុងការគូស។', 'Remember'))
    add(26, 1, with_img(mcq('easy', 'x', 'ក្នុងរូបគូប មុខពីមុខ ' + M('ABFE') + ' ដែលមើលចំពីមុខ មានរាង ៖', 'ការេដើម', ['ប្រលេឡូក្រាម', 'ត្រីកោណ', 'ចតុកោណព្នាយ'],
                       'មុខដែលមើលចំពីមុខរក្សារាងដើម។', 'Understand'), FIG_CUBE))
    add(26, 1, with_img(mcq('medium', 'x', 'ក្នុងរូបគូប មុខចំហៀង ' + M('BCGF') + ' ត្រូវគូសជា ៖', 'ប្រលេឡូក្រាម', ['ការេ', 'រង្វង់', 'ត្រីកោណសមបាត'],
                       'មុំត្រូវខុសពីទម្រង់ដើម ហើយទ្រនុងខ្លះអាចខុសប្រវែងពិត។', 'Understand'), FIG_CUBE))
    add(26, 1, mcq('medium', 'x', 'ការបង្វិលត្រីកោណកែងមួយជុំវិញជ្រុងជាប់មុំកែង ' + M('360^\\circ') + ' បង្កើតបានសូលីត ៖', 'កោណ', ['ស៊ីឡាំង', 'គូប', 'ពីរ៉ាមីត'],
                  'ជ្រុងបំព្រួញបង្កើតផ្ទៃកោណ។', 'Understand'))
    add(26, 1, wr('hard', 'x', 'ពន្យល់ពីរបៀបគូសរូបគូប ' + M('ABCD.EFGH') + ' លើប្លង់ ដោយប្រើគោលការណ៍ស្របគ្នា និងបន្ទាត់ដាច់ៗ។',
                  [('គូសមុខពីមុខ ' + M('ABFE') + ' ជាការេដើម។', 1), ('គូសមុខក្រោយ ' + M('DCGH') + ' ជាការេដូចគ្នា រំកិលតាមទិសទ្រេត។', 1),
                   ('ភ្ជាប់ទ្រនុងស្របគ្នា ' + M('AD,BC,FG,EH') + ' ដោយបន្ទាត់ស្របគ្នា។', 1), ('ទ្រនុងដែលបាំង ' + M('AD,DC,DH') + ' គូសដាច់ៗ។', 1),
                   ('មុខចំហៀងត្រូវតាងដោយប្រលេឡូក្រាម ហើយប្រវែងអាចខុសពិត។', 1)], 'Apply'))

    # ================= Lesson 28 -- part 2: បន្ទាត់អរតូកូណាល់ (+5) =================
    add(28, 2, mcq('easy', 'x', 'បន្ទាត់ពីរក្នុងលំហអរតូកូណាល់គ្នា កាលណា ៖', 'មុំរវាងបន្ទាត់ទាំងពីរជាមុំកែង', ['បន្ទាត់ទាំងពីរស្របគ្នា', 'បន្ទាត់ទាំងពីរកាត់គ្នាតែប៉ុណ្ណោះ', 'បន្ទាត់ទាំងពីរមានប្រវែងស្មើគ្នា'],
                  'តាមនិយមន័យ។', 'Remember'))
    add(28, 2, mcq('easy', 'x', 'បើ ' + M('a\\perp d') + ' និង ' + M('a\\parallel b') + ' នោះ ៖', M('b\\perp d'), [M('b\\parallel d'), M('a\\perp b'), M('b\\cap d=\\emptyset')], 'វិបាកនៃអរតូកូណាល់។', 'Understand'))
    add(28, 2, mcq('medium', 'x', 'ក្នុងគូប ' + M('ABCD.EFGH') + ' មុំរវាងបន្ទាត់ ' + M('AE') + ' និង ' + M('BC') + ' គឺ ៖', M(deg(line_angle('AE', 'BC'))), [M('45^\\circ'), M('60^\\circ'), M('0^\\circ')],
                  M('AE\\parallel BF,\\ BF\\perp BC') + ' ដូច្នេះ ' + M('AE\\perp BC') + '។', 'Apply'))
    add(28, 2, mcq('medium', 'x', 'ក្នុងគូប ' + M('ABCD.EFGH') + ' មុំរវាងអង្កត់ទ្រូងមុខ ' + M('AF') + ' និង ' + M('AH') + ' គឺ ៖', M(deg(line_angle('AF', 'AH'))), [M('45^\\circ'), M('90^\\circ'), M('30^\\circ')],
                  M('FH=AF=AH') + ' ជាត្រីកោណសម័ង្ស ' + M('\\Rightarrow60^\\circ') + '។', 'Apply'))
    add(28, 2, mcq('hard', 'x', 'ចតុមុខ ' + M('OABC') + ' មាន ' + M('OA,OB,OC') + ' កែងគ្នាពីរៗត្រង់ ' + M('O') + '។ គូបន្ទាត់ណាមួយអរតូកូណាល់គ្នា ?', M('OA') + ' និង ' + M('BC'),
                  [M('AB') + ' និង ' + M('OC'), M('AB') + ' និង ' + M('AC'), M('OA') + ' និង ' + M('AB')],
                  M('OA\\perp OB,\\ OA\\perp OC\\Rightarrow OA\\perp(OBC)') + ' ដូច្នេះ ' + M('OA\\perp BC') + '។', 'Analyze'))

    # ================= Lesson 28 -- part 4: ប្លង់មេដ្យាទ័រ (+6) =================
    add(28, 4, mcq('easy', 'x', 'ប្លង់មេដ្យាទ័រនៃអង្កត់ ' + M('[AB]') + ' គឺប្លង់ដែល ៖', 'កែងនឹង ' + M('AB') + ' ត្រង់ចំណុចកណ្តាល', ['ស្របនឹង ' + M('AB'), 'កាត់ ' + M('AB') + ' ត្រង់ចំណុច ' + M('A'), 'ផ្ទុកអង្កត់ ' + M('AB')],
                  'តាមនិយមន័យ។', 'Remember'))
    add(28, 4, mcq('easy', 'x', 'បើ ' + M('C') + ' ជាចំណុចក្នុងប្លង់មេដ្យាទ័រនៃ ' + M('[AB]') + ' នោះ ៖', M('CA=CB'), [M('CA=AB'), M('CA>CB'), M('CA+CB=AB')], 'ចំណុចក្នុងប្លង់មេដ្យាទ័រស្មើចម្ងាយពី ' + M('A') + ' និង ' + M('B') + '។', 'Understand'))
    add(28, 4, mcq('medium', 'x', 'ក្នុងតម្រុយ ' + M('A(0,0,0)') + ' ' + M('B(4,0,0)') + '។ សមីការប្លង់មេដ្យាទ័រនៃ ' + M('[AB]') + ' គឺ ៖', M('x=2'), [M('x=4'), M('y=2'), M('x=0')], 'ត្រូវកែងនឹង ' + M('AB') + ' ត្រង់ចំណុចកណ្តាល ' + M('(2,0,0)') + '។', 'Apply'))
    add(28, 4, mcq('medium', 'x', 'ក្នុងតម្រុយ ' + M('A(1,2,3)') + ' ' + M('B(3,2,-1)') + '។ សមីការប្លង់មេដ្យាទ័រនៃ ' + M('[AB]') + ' គឺ ៖', M('x-2z=0'), [M('x+2z=0'), M('2x-4z=1'), M('x-2z=2')],
                  M('MA^2=MB^2') + ' ឱ្យ ' + M('4x-8z=0') + ' ពោលគឺ ' + M('x-2z=0') + ' (កាត់ចំណុចកណ្តាល ' + M('(2,2,1)') + ')។', 'Apply'))
    add(28, 4, mcq('medium', 'x', 'ក្នុងគូប ' + M('ABCD.EFGH') + ' ប្លង់មេដ្យាទ័រនៃអង្កត់ ' + M('[AE]') + ' គឺប្លង់ ៖', 'ស្របនឹងប្លង់ ' + M('ABCD') + ' ហើយកាត់ត្រង់កណ្តាលកម្ពស់', ['ស្របនឹងប្លង់ ' + M('ABFE'), 'ដូចប្លង់ ' + M('EFGH'), 'កាត់តាម ' + M('A') + ' និង ' + M('E')],
                  M('AE\\perp(ABCD)') + ' ដូច្នេះប្លង់កែងនឹង ' + M('AE') + ' ជាប្លង់ស្របនឹង ' + M('ABCD') + ' ត្រង់ ' + M('z=\\tfrac12') + '។', 'Apply'))
    add(28, 4, wr('hard', 'x', 'រកសមីការប្លង់មេដ្យាទ័រនៃអង្កត់ ' + M('[AB]') + ' ដែល ' + M('A(1,0,2)') + ' និង ' + M('B(-1,2,0)') + '។',
                  [('ចំណុច ' + M('M(x,y,z)') + ' ក្នុងប្លង់ ' + M('\\iff MA=MB') + '។', 1), (M('(x-1)^2+y^2+(z-2)^2=(x+1)^2+(y-2)^2+z^2') + '។', 1),
                   (M('-2x-4z+5=2x-4y+5') + '។', 1), (M('-4x+4y-4z=0\\Rightarrow x-y+z=0') + '។', 1),
                   ('ពិនិត្យ ចំណុចកណ្តាល ' + M('(0,1,1)') + ' ផ្ទៀងផ្ទាត់ ' + M('0-1+1=0') + '។', 1)], 'Analyze'))

    # ================= Lesson 28 -- part 5: ប្លង់កែង (+8) =================
    add(28, 5, mcq('easy', 'x', 'ប្លង់ ' + M('P') + ' កែងនឹងប្លង់ ' + M('Q') + ' កាលណា ៖', M('P') + ' មានបន្ទាត់មួយកែងនឹង ' + M('Q'), [M('P') + ' ស្របនឹង ' + M('Q'), M('P') + ' និង ' + M('Q') + ' គ្មានចំណុចរួម', M('P') + ' មានបន្ទាត់ស្របនឹង ' + M('Q')],
                  'និយមន័យប្លង់កែង។', 'Remember'))
    add(28, 5, mcq('easy', 'x', 'បើ ' + M('d\\perp P') + ' និង ' + M('d\\subset Q') + ' នោះ ៖', M('Q\\perp P'), [M('Q\\parallel P'), M('Q=P'), M('Q\\cap P=\\emptyset')], 'ប្លង់ ' + M('Q') + ' ផ្ទុកបន្ទាត់កែងនឹង ' + M('P') + '។', 'Understand'))
    add(28, 5, with_img(mcq('medium', 'x', 'ក្នុងគូប ' + M('ABCD.EFGH') + ' ប្លង់ណាកែងនឹងប្លង់ ' + M('ABCD') + ' ?', M('ABFE'), [M('EFGH'), M('ACH'), M('BDE')],
                       M('AE\\perp(ABCD)') + ' ហើយ ' + M('AE\\subset(ABFE)') + '។ ' + M('EFGH\\parallel ABCD') + ' មិនកែង។', 'Apply'), FIG_CUBE))
    add(28, 5, mcq('medium', 'x', 'ក្នុងគូប ' + M('ABCD.EFGH') + ' មុំរវាងប្លង់ ' + M('ACGE') + ' និង ' + M('BDHF') + ' គឺ ៖', M(deg(plane_angle('ACGE', 'BDHF'))), [M('45^\\circ'), M('60^\\circ'), M('0^\\circ')],
                  M('AC\\perp BD') + ' និង ' + M('AC\\perp BF') + ' នាំឱ្យ ' + M('AC\\perp(BDHF)') + ' ដូច្នេះប្លង់ទាំងពីរកែងគ្នា។', 'Apply'))
    add(28, 5, mcq('medium', 'x', 'បើ ' + M('P\\perp R') + ' និង ' + M('R\\parallel Q') + ' នោះ ៖', M('P\\perp Q'), [M('P\\parallel Q'), M('P=Q'), M('P') + ' បង្កើតមុំ ' + M('45^\\circ') + ' នឹង ' + M('Q')], 'លក្ខណៈ (ខ) នៃប្លង់កែង។', 'Understand'))
    add(28, 5, mcq('medium', 'x', 'ពីរ៉ាមីត ' + M('S.ABCD') + ' មាន ' + M('SA\\perp(ABCD)') + '។ ប្លង់ណាកែងនឹងប្លង់បាត ?', M('SAB'), [M('SBC'), M('SCD'), M('SBD')],
                  M('SA\\subset(SAB)') + ' និង ' + M('SA\\perp(ABCD)') + ' ដូច្នេះ ' + M('(SAB)\\perp(ABCD)') + ' (ប្លង់ ' + M('SBC,SCD,SBD') + ' មិនផ្ទុក ' + M('SA') + ')។', 'Apply'))
    add(28, 5, mcq('hard', 'x', 'បើ ' + M('d\\perp P') + ' និង ' + M('d\\perp Q') + ' នោះប្លង់ ' + M('P') + ' និង ' + M('Q') + ' ៖', 'ស្របគ្នា ឬត្រូវគ្នា', ['កែងគ្នា', 'កាត់គ្នាតាមបន្ទាត់ ' + M('d'), 'កាត់គ្នាជាមុំ ' + M('45^\\circ')],
                  'ប្លង់ពីរកែងនឹងបន្ទាត់តែមួយ ស្របគ្នា។', 'Analyze'))
    add(28, 5, wr('hard', 'x', 'ពីរ៉ាមីត ' + M('S.ABCD') + ' មានបាត ' + M('ABCD') + ' ជាចតុកោណកែង និង ' + M('SA\\perp(ABCD)') + '។ ស្រាយថា ' + M('(SAB)\\perp(SAD)') + '។',
                  [(M('SA\\perp(ABCD)\\Rightarrow SA\\perp AB') + '។', 1), (M('ABCD') + ' ជាចតុកោណកែង ' + M('\\Rightarrow AB\\perp AD') + '។', 1),
                   (M('AB\\perp SA') + ' និង ' + M('AB\\perp AD') + ' ដែល ' + M('SA,AD\\subset(SAD)') + ' កាត់គ្នា។', 1), (M('\\Rightarrow AB\\perp(SAD)') + '។', 1),
                   (M('AB\\subset(SAB)') + ' ដូច្នេះ ' + M('(SAB)\\perp(SAD)') + '។', 1)], 'Analyze'))

    # ================= Lesson 28 -- part 6: មុំដែលបង្កើតឡើងដោយប្លង់ពីរ (+9) =================
    add(28, 6, mcq('easy', 'x', 'មុំរវាងប្លង់ពីរ ស្មើនឹងមុំរវាងបន្ទាត់ពីរ ដែល ៖', 'នៅក្នុងប្លង់នីមួយៗ ហើយកែងនឹងបន្ទាត់ប្រសព្វត្រង់ចំណុចតែមួយ',
                  ['ស្របនឹងបន្ទាត់ប្រសព្វ', 'ស្របគ្នា', 'កាត់បន្ទាត់ប្រសព្វត្រង់ចំណុចខុសគ្នា'], 'ជ្រើស ' + M('OA,OB\\perp d') + ' ត្រង់ ' + M('O') + '។', 'Remember'))
    add(28, 6, mcq('easy', 'x', 'ប្លង់ពីរកែងគ្នា បង្កើតមុំរវាងប្លង់ស្មើ ៖', M('90^\\circ'), [M('0^\\circ'), M('45^\\circ'), M('180^\\circ')], 'តាមនិយមន័យប្លង់កែង។', 'Remember'))
    add(28, 6, mcq('easy', 'x', 'ប្លង់ពីរស្របគ្នា បង្កើតមុំរវាងប្លង់ស្មើ ៖', M('0^\\circ'), [M('90^\\circ'), M('45^\\circ'), M('180^\\circ')], 'ប្លង់ស្របគ្នាមានទិសដូចគ្នា។', 'Understand'))
    add(28, 6, with_img(mcq('medium', 'x', 'ក្នុងគូប ' + M('ABCD.EFGH') + ' មុំរវាងប្លង់ ' + M('ABGH') + ' និង ' + M('ABCD') + ' គឺ ៖', M(deg(plane_angle('ABGH', 'ABCD'))), [M('30^\\circ'), M('60^\\circ'), M('90^\\circ')],
                        M('AB') + ' ជាបន្ទាត់ប្រសព្វ ' + M('AD\\perp AB,\\ AH\\perp AB') + ' ហើយ ' + M('\\angle DAH=45^\\circ') + '។', 'Apply'), FIG_CUBE))
    ang = plane_angle('ACH', 'ABCD')
    add(28, 6, with_img(mcq('medium', 'x', 'ក្នុងគូប ' + M('ABCD.EFGH') + ' មុំ ' + M('\\alpha') + ' រវាងប្លង់ ' + M('ACH') + ' និង ' + M('ABCD') + ' មាន ' + M('\\cos\\alpha') + ' ស្មើ ៖', M(r'\dfrac1{\sqrt3}'),
                        [M(r'\dfrac1{\sqrt2}'), M(r'\dfrac12'), M(r'\dfrac{\sqrt3}2')], 'ធ្វើជាមួយវ៉ិចទ័រណរម៉ាល់ ' + M('(1,-1,1)') + ' និង ' + M('(0,0,1)') + ' ៖ ' + M('\\alpha\\approx%s' % deg(ang)) + '។', 'Analyze'), FIG_CUBE))
    a_ = degrees(atan(F(3, 4)))
    add(28, 6, with_img(mcq('medium', 'x', 'ពីរ៉ាមីតនិយ័តបាតការេជ្រុង ' + M('8\\text{ cm}') + ' កម្ពស់ ' + M('3\\text{ cm}') + '។ មុំរវាងមុខចំហៀងនិងបាតមាន ' + M('\\tan') + ' ស្មើ ៖', M(r'\dfrac34'),
                        [M(r'\dfrac43'), M(r'\dfrac38'), M(r'\dfrac83')], 'ត្រូវប្រើ ' + M('OM=4') + ' (កន្លះជ្រុង) ហើយ ' + M('\\tan\\alpha=\\dfrac{SO}{OM}=\\dfrac34') + ' ដូច្នេះ ' + M('\\alpha\\approx%s' % deg(a_)) + '។', 'Apply'), FIG_PYR))
    d_t = degrees(acos(F(1, 3)))
    add(28, 6, mcq('hard', 'x', 'មុំរវាងមុខពីរនៃចតុមុខនិយ័ត មាន ' + M('\\cos') + ' ស្មើ ៖', M(r'\dfrac13'), [M(r'\dfrac12'), M(r'\dfrac{\sqrt3}3'), M(r'\dfrac{1}{\sqrt3}')],
                  M('\\cos\\alpha=\\dfrac{1}{3}') + ' ដូច្នេះ ' + M('\\alpha\\approx%s' % deg(d_t)) + '។', 'Analyze'))
    add(28, 6, mcq('hard', 'x', 'ក្នុងគូប ' + M('ABCD.EFGH') + ' មុំរវាងប្លង់ ' + M('ACGE') + ' និង ' + M('ABFE') + ' គឺ ៖', M(deg(plane_angle('ACGE', 'ABFE'))), [M('30^\\circ'), M('60^\\circ'), M('90^\\circ')],
                  M('AE') + ' ជាបន្ទាត់ប្រសព្វ ' + M('AB\\perp AE,\\ AC') + ' ក្នុង ' + M('ACGE') + ' កែងនឹង ' + M('AE') + ' ដូច្នេះមុំ ' + M('\\angle BAC=45^\\circ') + '។', 'Analyze'))
    add(28, 6, with_img(wr('hard', 'x', 'ពីរ៉ាមីតនិយ័ត ' + M('S.ABCD') + ' បាតការេជ្រុង ' + M('6\\text{ cm}') + ' កម្ពស់ ' + M('SO=4\\text{ cm}') + '។ រកមុំរវាងប្លង់ ' + M('SBC') + ' និង ' + M('ABCD') + '។',
                           [('យក ' + M('M') + ' ជាចំណុចកណ្តាល ' + M('BC') + ' ៖ ' + M('OM\\perp BC') + ' និង ' + M('SM\\perp BC') + '។', 1), ('ដូច្នេះមុំរវាងប្លង់ជា ' + M('\\angle SMO=\\alpha') + '។', 1),
                            (M('OM=3,\\ SO=4') + ' ឱ្យ ' + M('SM=5') + '។', 1), (M('\\tan\\alpha=\\dfrac43,\\ \\cos\\alpha=\\dfrac35') + '។', 1),
                            (M('\\alpha\\approx%s' % deg(degrees(atan(F(4, 3))))) + '។', 1)], 'Analyze'), FIG_PYR))

    # ================= Lesson 28 -- part 7: ចំណោលកែង (+1) =================
    add(28, 7, mcq('medium', 'x', 'អង្កត់ ' + M('AB=12\\text{ cm}') + ' បង្កើតមុំ ' + M('60^\\circ') + ' ជាមួយប្លង់ ' + M('(P)') + '។ ប្រវែងចំណោលកែង ' + M("A'B'") + ' លើ ' + M('(P)') + ' គឺ ៖', M('6\\text{ cm}'),
                  [M('6\\sqrt3\\text{ cm}'), M('12\\text{ cm}'), M('4\\sqrt3\\text{ cm}')], M("A'B'=AB\\cos60^\\circ=12\\times\\tfrac12=6") + '។', 'Apply'))

    return out
