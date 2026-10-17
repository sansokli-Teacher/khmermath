from lib import *
import math

LESSON = 'ការអនុវត្តផលធៀបត្រីកោណ'
CHAPTER = 'ជំពូកទី 5 : ផលធៀបត្រីកោណមាត្រ'

def with_img(q, svg):
    q['img'] = svg
    return q

# =========================================================================
# SVG Figures for Lesson 15
# =========================================================================

FIG_SINE_RULE = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 360 250' width='360' height='250'>
  <rect width='360' height='250' fill='#ffffff'/>
  <!-- Circumcircle Center (180, 130), R = 90 -->
  <circle cx='180' cy='130' r='90' fill='#f8fafc' stroke='#64748b' stroke-width='1.5' stroke-dasharray='4,3'/>
  <!-- Center O -->
  <circle cx='180' cy='130' r='3.5' fill='#64748b'/>
  <text x='185' y='125' font-family='serif' font-size='12' fill='#64748b'>O</text>
  <!-- Inscribed triangle ABC: A=(180, 40), B=(95, 160), C=(255, 175) -->
  <polygon points='180,40 95,160 255,175' fill='#eff6ff' stroke='#1d4ed8' stroke-width='2.5'/>
  <!-- Vertices -->
  <text x='175' y='32' font-family='serif' font-size='15' font-weight='bold' fill='#1e293b'>A</text>
  <text x='78' y='170' font-family='serif' font-size='15' font-weight='bold' fill='#1e293b'>B</text>
  <text x='262' y='185' font-family='serif' font-size='15' font-weight='bold' fill='#1e293b'>C</text>
  <!-- Side a opposite A -->
  <text x='175' y='190' font-family='serif' font-size='14' font-weight='bold' fill='#dc2626'>a</text>
  <text x='225' y='100' font-family='serif' font-size='14' font-weight='bold' fill='#059669'>b</text>
  <text x='125' y='95' font-family='serif' font-size='14' font-weight='bold' fill='#d97706'>c</text>
  <!-- Law of sines formula note -->
  <text x='70' y='235' font-family='serif' font-size='13' font-weight='bold' fill='#1d4ed8'>a/sin A = b/sin B = c/sin C = 2R</text>
</svg>"""

FIG_COSINE_RULE = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 360 220' width='360' height='220'>
  <rect width='360' height='220' fill='#ffffff'/>
  <!-- Triangle ABC: A=(60, 170), B=(300, 170), C=(150, 50) -->
  <polygon points='60,170 300,170 150,50' fill='#f0fdf4' stroke='#15803d' stroke-width='2.5'/>
  <!-- Altitude CH from C to AB: H=(150, 170) -->
  <line x1='150' y1='50' x2='150' y2='170' stroke='#dc2626' stroke-width='1.5' stroke-dasharray='4,3'/>
  <polyline points='150,155 165,155 165,170' fill='none' stroke='#dc2626' stroke-width='1.5'/>
  <text x='155' y='115' font-family='serif' font-size='13' font-weight='bold' fill='#dc2626'>h</text>
  <!-- Vertices -->
  <text x='42' y='180' font-family='serif' font-size='15' font-weight='bold' fill='#1e293b'>A</text>
  <text x='308' y='180' font-family='serif' font-size='15' font-weight='bold' fill='#1e293b'>B</text>
  <text x='145' y='42' font-family='serif' font-size='15' font-weight='bold' fill='#1e293b'>C</text>
  <!-- Sides -->
  <text x='235' y='105' font-family='serif' font-size='14' font-weight='bold' fill='#1e293b'>a</text>
  <text x='95' y='105' font-family='serif' font-size='14' font-weight='bold' fill='#1e293b'>b</text>
  <text x='180' y='188' font-family='serif' font-size='14' font-weight='bold' fill='#1e293b'>c</text>
  <!-- Formula -->
  <text x='80' y='210' font-family='serif' font-size='13' font-weight='bold' fill='#15803d'>a² = b² + c² - 2bc cos A</text>
</svg>"""

FIG_AREA_SINE = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 360 210' width='360' height='210'>
  <rect width='360' height='210' fill='#ffffff'/>
  <!-- Triangle with base BC: C=(60, 160), B=(280, 160), A=(140, 50) -->
  <polygon points='60,160 280,160 140,50' fill='#fffbeb' stroke='#b45309' stroke-width='2.5'/>
  <!-- Altitude AH: H=(140, 160) -->
  <line x1='140' y1='50' x2='140' y2='160' stroke='#dc2626' stroke-width='1.5' stroke-dasharray='3,3'/>
  <polyline points='140,145 155,145 155,160' fill='none' stroke='#dc2626' stroke-width='1.5'/>
  <!-- Angle C arc -->
  <path d='M 95,160 A 35,35 0 0,0 87,133' fill='none' stroke='#ea580c' stroke-width='2.5'/>
  <text x='96' y='145' font-family='serif' font-size='14' font-weight='bold' fill='#ea580c'>C</text>
  <!-- Vertices -->
  <text x='42' y='170' font-family='serif' font-size='15' font-weight='bold' fill='#1e293b'>C</text>
  <text x='288' y='170' font-family='serif' font-size='15' font-weight='bold' fill='#1e293b'>B</text>
  <text x='135' y='42' font-family='serif' font-size='15' font-weight='bold' fill='#1e293b'>A</text>
  <!-- Sides -->
  <text x='170' y='178' font-family='serif' font-size='13' font-weight='bold' fill='#1e293b'>a</text>
  <text x='90' y='100' font-family='serif' font-size='13' font-weight='bold' fill='#1e293b'>b</text>
  <!-- Formula -->
  <text x='110' y='200' font-family='serif' font-size='14' font-weight='bold' fill='#b45309'>S = ½ a b sin C</text>
</svg>"""

FIG_HERON = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 360 210' width='360' height='210'>
  <rect width='360' height='210' fill='#ffffff'/>
  <!-- Triangle with sides 13, 14, 15: C=(50, 160), B=(260, 160), A=(140, 50) -->
  <polygon points='50,160 260,160 140,50' fill='#eff6ff' stroke='#2563eb' stroke-width='2.5'/>
  <!-- Vertices -->
  <text x='35' y='170' font-family='serif' font-size='14' font-weight='bold' fill='#1e293b'>C</text>
  <text x='268' y='170' font-family='serif' font-size='14' font-weight='bold' fill='#1e293b'>B</text>
  <text x='135' y='42' font-family='serif' font-size='14' font-weight='bold' fill='#1e293b'>A</text>
  <!-- Side values -->
  <text x='150' y='180' font-family='serif' font-size='13' font-weight='bold' fill='#2563eb'>a = 14</text>
  <text x='78' y='100' font-family='serif' font-size='13' font-weight='bold' fill='#2563eb'>b = 15</text>
  <text x='208' y='100' font-family='serif' font-size='13' font-weight='bold' fill='#2563eb'>c = 13</text>
  <!-- Heron Note -->
  <text x='65' y='202' font-family='Khmer OS Battambang,sans-serif' font-size='12' fill='#1e293b'>p = 21 នាំឱ្យ S = √(21·7·6·8) = 84</text>
</svg>"""

FIG_RIVER_SURVEY = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 360 220' width='360' height='220'>
  <rect width='360' height='220' fill='#ffffff'/>
  <!-- River water zone -->
  <path d='M 0,80 Q 180,95 360,80 L 360,140 Q 180,155 0,140 Z' fill='#e0f2fe'/>
  <text x='150' y='115' font-family='Khmer OS Battambang,sans-serif' font-size='12' fill='#0284c7'>ទន្លេ</text>
  <!-- Bank line 1 and 2 -->
  <path d='M 0,80 Q 180,95 360,80' fill='none' stroke='#38bdf8' stroke-width='2'/>
  <path d='M 0,140 Q 180,155 360,140' fill='none' stroke='#38bdf8' stroke-width='2'/>
  <!-- Stations A and B on south bank -->
  <circle cx='80' cy='180' r='4' fill='#dc2626'/>
  <text x='75' y='200' font-family='serif' font-size='14' font-weight='bold' fill='#dc2626'>A</text>
  <circle cx='240' cy='180' r='4' fill='#dc2626'/>
  <text x='235' y='200' font-family='serif' font-size='14' font-weight='bold' fill='#dc2626'>B</text>
  <line x1='80' y1='180' x2='240' y2='180' stroke='#334155' stroke-width='2'/>
  <text x='150' y='200' font-family='serif' font-size='12' fill='#334155'>d = 80m</text>
  <!-- Landmark C on north bank -->
  <circle cx='180' cy='45' r='4' fill='#059669'/>
  <text x='175' y='38' font-family='serif' font-size='14' font-weight='bold' fill='#059669'>C</text>
  <!-- Sighting lines -->
  <line x1='80' y1='180' x2='180' y2='45' stroke='#dc2626' stroke-width='1.5' stroke-dasharray='4,3'/>
  <line x1='240' y1='180' x2='180' y2='45' stroke='#dc2626' stroke-width='1.5' stroke-dasharray='4,3'/>
</svg>"""

# =========================================================================
# Candidates Generator for G10L15
# =========================================================================

def cands():
    C = []

    # ---------------------------------------------------------------------
    # MCQ Easy (Target: 10)
    # ---------------------------------------------------------------------
    C.append(with_img(
        mcq('easy', 'sines',
            'ក្នុងគ្រប់ត្រីកោណ ' + M(r'ABC') + ' ដែលមានកាំរង្វង់ចារឹកក្រៅ ' + M(r'R') + ' តើរូបមន្តទ្រឹស្តីបទស៊ីនុសមួយណាត្រឹមត្រូវ?',
            M(r'\dfrac{a}{\sin A} = \dfrac{b}{\sin B} = \dfrac{c}{\sin C} = 2R'),
            [M(r'\dfrac{a}{\sin A} = \dfrac{b}{\sin B} = \dfrac{c}{\sin C} = R'),
             M(r'\dfrac{\sin A}{a} = \dfrac{\sin B}{b} = \dfrac{\sin C}{c} = 2R'),
             M(r'a \sin A = b \sin B = c \sin C = 2R')],
            r'\frac{a}{\sin A} = \frac{b}{\sin B} = \frac{c}{\sin C} = 2R'
        ),
        FIG_SINE_RULE
    ))

    C.append(with_img(
        mcq('easy', 'cosines',
            'ក្នុងត្រីកោណ ' + M(r'ABC') + ' តើរូបមន្តទ្រឹស្តីបទកូស៊ីនុសសម្រាប់ជ្រុង ' + M(r'a') + ' មួយណាត្រឹមត្រូវ?',
            M(r'a^2 = b^2 + c^2 - 2bc \cos A'),
            [M(r'a^2 = b^2 + c^2 + 2bc \cos A'),
             M(r'a^2 = b^2 - c^2 - 2bc \cos A'),
             M(r'a^2 = (b + c)^2 - 2bc \cos A')],
            r'a^2 = b^2 + c^2 - 2bc \cos A'
        ),
        FIG_COSINE_RULE
    ))

    C.append(with_img(
        mcq('easy', 'area',
            'រូបមន្តផ្ទៃក្រឡាត្រីកោណ ' + M(r'ABC') + ' តាមប្រវែងជ្រុងពីរ ' + M(r'a, b') + ' និងមុំកៀប ' + M(r'C') + ' គឺ ៖',
            M(r'S = \dfrac{1}{2}ab \sin C'),
            [M(r'S = ab \sin C'), M(r'S = \dfrac{1}{2}ab \cos C'), M(r'S = \dfrac{1}{2}(a + b)\sin C')],
            r'S = \frac{1}{2}ab \sin C'
        ),
        FIG_AREA_SINE
    ))

    C.append(mcq('easy', 'area',
        'រូបមន្តហេរ៉ុង (Heron) សម្រាប់គណនាផ្ទៃក្រឡាត្រីកោណតាមកន្លះបរិមាត្រ ' + M(r'p') + ' គឺ ៖',
        M(r'S = \sqrt{p(p - a)(p - b)(p - c)}'),
        [M(r'S = \sqrt{(p - a)(p - b)(p - c)}'),
         M(r'S = p\sqrt{(p - a)(p - b)(p - c)}'),
         M(r'S = \sqrt{p(a + b + c)}')],
        r'S = \sqrt{p(p-a)(p-b)(p-c)} \text{ ដែល } p = \frac{a+b+c}{2}'
    ))

    C.append(mcq('easy', 'sines',
        'ក្នុងត្រីកោណ ' + M(r'ABC') + ' មាន ' + M(r'a = 6\text{ cm}') + ' និង ' + M(r'\sin A = \dfrac{1}{2}') + '។ គណនាកាំ ' + M(r'R') + ' នៃរង្វង់ចារឹកក្រៅត្រីកោណ។',
        M(r'6\text{ cm}'),
        [M(r'12\text{ cm}'), M(r'3\text{ cm}'), M(r'24\text{ cm}')],
        r'2R = \frac{a}{\sin A} = \frac{6}{1/2} = 12 \implies R = 6\text{ cm}'
    ))

    C.append(mcq('easy', 'cosines',
        'ក្នុងត្រីកោណ ' + M(r'ABC') + ' បើស្គាល់ប្រវែងជ្រុងទាំងបី ' + M(r'a, b, c') + ' តើយើងគួរប្រើទ្រឹស្តីបទអ្វីដើម្បីគណនារង្វាស់មុំ?',
        M(r'\text{ទ្រឹស្តីបទកូស៊ីនុស}'),
        [M(r'\text{ទ្រឹស្តីបទតាល់ស}'), M(r'\text{រូបមន្តហេរ៉ុង}'), M(r'\text{ទ្រឹស្តីបទពីតាករតែមួយមុខ}')],
        r'\cos A = \frac{b^2 + c^2 - a^2}{2bc}'
    ))

    C.append(mcq('easy', 'area',
        'ត្រីកោណមួយមានកន្លះបរិមាត្រ ' + M(r'p = 10\text{ cm}') + ' និងកាំរង្វង់ចារឹកក្នុង ' + M(r'r = 3\text{ cm}') + '។ គណនាផ្ទៃក្រឡាត្រីកោណនោះ។',
        M(r'30\text{ cm}^2'),
        [M(r'15\text{ cm}^2'), M(r'60\text{ cm}^2'), M(r'20\text{ cm}^2')],
        r'S = pr = 10 \times 3 = 30\text{ cm}^2'
    ))

    C.append(mcq('easy', 'triangle',
        'ក្នុងត្រីកោណ ' + M(r'ABC') + ' មាន ' + M(r'\angle A = 45^\circ') + ' និង ' + M(r'\angle B = 75^\circ') + '។ តើមុំ ' + M(r'\angle C') + ' មានរង្វាស់ស្មើនឹងប៉ុន្មាន?',
        M(r'60^\circ'),
        [M(r'50^\circ'), M(r'70^\circ'), M(r'80^\circ')],
        r'\angle C = 180^\circ - (45^\circ + 75^\circ) = 60^\circ'
    ))

    C.append(mcq('easy', 'area',
        'ក្នុងត្រីកោណ ' + M(r'ABC') + ' មាន ' + M(r'a = 8\text{ cm},\; b = 10\text{ cm}') + ' និង ' + M(r'\angle C = 30^\circ') + '។ គណនាផ្ទៃក្រឡា ' + M(r'S') + '។',
        M(r'20\text{ cm}^2'),
        [M(r'40\text{ cm}^2'), M(r'20\sqrt{3}\text{ cm}^2'), M(r'10\text{ cm}^2')],
        r'S = \frac{1}{2}(8)(10)\sin 30^\circ = 40 \times \frac{1}{2} = 20\text{ cm}^2'
    ))

    C.append(mcq('easy', 'area',
        'រូបមន្តផ្ទៃក្រឡាត្រីកោណ ' + M(r'ABC') + ' តាមប្រវែងជ្រុងទាំងបី និងកាំ ' + M(r'R') + ' នៃរង្វង់ចារឹកក្រៅគឺ ៖',
        M(r'S = \dfrac{abc}{4R}'),
        [M(r'S = \dfrac{abc}{2R}'), M(r'S = \dfrac{abc}{R}'), M(r'S = \dfrac{4R}{abc}')],
        r'S = \frac{abc}{4R}'
    ))

    # ---------------------------------------------------------------------
    # MCQ Medium (Target: 14)
    # ---------------------------------------------------------------------
    C.append(mcq('medium', 'sines',
        'ក្នុងត្រីកោណ ' + M(r'ABC') + ' មាន ' + M(r'\angle A = 30^\circ,\; \angle B = 45^\circ') + ' និងជ្រុង ' + M(r'a = 8\text{ cm}') + '។ គណនាប្រវែងជ្រុង ' + M(r'b') + '។',
        M(r'8\sqrt{2}\text{ cm}'),
        [M(r'4\sqrt{2}\text{ cm}'), M(r'8\sqrt{3}\text{ cm}'), M(r'16\text{ cm}')],
        r'\frac{b}{\sin 45^\circ} = \frac{8}{\sin 30^\circ} \implies b = \frac{8 \times \frac{\sqrt{2}}{2}}{\frac{1}{2}} = 8\sqrt{2}\text{ cm}'
    ))

    C.append(mcq('medium', 'cosines',
        'ក្នុងត្រីកោណ ' + M(r'ABC') + ' មាន ' + M(r'b = 6\text{ cm},\; c = 10\text{ cm}') + ' និង ' + M(r'\angle A = 60^\circ') + '។ គណនាប្រវែងជ្រុង ' + M(r'a') + '។',
        M(r'2\sqrt{19}\text{ cm}'),
        [M(r'14\text{ cm}'), M(r'\sqrt{136}\text{ cm}'), M(r'8\text{ cm}')],
        r'a^2 = 36 + 100 - 2(6)(10)\cos 60^\circ = 136 - 60 = 76 \implies a = \sqrt{76} = 2\sqrt{19}\text{ cm}'
    ))

    C.append(mcq('medium', 'cosines',
        'ក្នុងត្រីកោណ ' + M(r'ABC') + ' មានរង្វាស់ជ្រុង ' + M(r'a = 5,\; b = 7,\; c = 8') + '។ គណនាតម្លៃនៃ ' + M(r'\cos C') + '។',
        M(r'\dfrac{1}{7}'),
        [M(r'\dfrac{2}{7}'), M(r'\dfrac{3}{7}'), M(r'\dfrac{1}{5}')],
        r'\cos C = \frac{5^2 + 7^2 - 8^2}{2(5)(7)} = \frac{25 + 49 - 64}{70} = \frac{10}{70} = \frac{1}{7}'
    ))

    C.append(with_img(
        mcq('medium', 'heron',
            'ត្រីកោណមួយមានប្រវែងជ្រុងទាំងបី ' + M(r'a = 13,\; b = 14,\; c = 15') + '។ គណនាផ្ទៃក្រឡា ' + M(r'S') + ' នៃត្រីកោណនេះ។',
            M(r'84'),
            [M(r'90'), M(r'80'), M(r'96')],
            r'p = \frac{13+14+15}{2} = 21; S = \sqrt{21 \times 8 \times 7 \times 6} = \sqrt{7056} = 84'
        ),
        FIG_HERON
    ))

    C.append(mcq('medium', 'sines',
        'ក្នុងត្រីកោណ ' + M(r'ABC') + ' មាន ' + M(r'a = 10\text{ cm}') + ' និង ' + M(r'\angle A = 45^\circ') + '។ គណនាកាំ ' + M(r'R') + ' នៃរង្វង់ចារឹកក្រៅត្រីកោណ។',
        M(r'5\sqrt{2}\text{ cm}'),
        [M(r'10\sqrt{2}\text{ cm}'), M(r'10\text{ cm}'), M(r'5\text{ cm}')],
        r'2R = \frac{10}{\sin 45^\circ} = \frac{10}{\sqrt{2}/2} = 10\sqrt{2} \implies R = 5\sqrt{2}\text{ cm}'
    ))

    C.append(mcq('medium', 'area',
        'ក្នុងត្រីកោណ ' + M(r'ABC') + ' មាន ' + M(r'a = 6\text{ cm},\; b = 8\text{ cm}') + ' និងផ្ទៃក្រឡា ' + M(r'S = 12\sqrt{3}\text{ cm}^2') + '។ រកទំហំមុំស្រួច ' + M(r'\angle C') + '។',
        M(r'60^\circ'),
        [M(r'30^\circ'), M(r'45^\circ'), M(r'75^\circ')],
        r'S = \frac{1}{2}ab \sin C = 24 \sin C = 12\sqrt{3} \implies \sin C = \frac{\sqrt{3}}{2} \implies C = 60^\circ'
    ))

    C.append(mcq('medium', 'cosines',
        'ក្នុងត្រីកោណ ' + M(r'ABC') + ' មានជ្រុង ' + M(r'a = 7,\; b = 5,\; c = 6') + '។ គណនា ' + M(r'\cos A') + '។',
        M(r'\dfrac{1}{5}'),
        [M(r'\dfrac{2}{5}'), M(r'\dfrac{1}{6}'), M(r'\dfrac{3}{10}')],
        r'\cos A = \frac{b^2 + c^2 - a^2}{2bc} = \frac{25 + 36 - 49}{60} = \frac{12}{60} = \frac{1}{5}'
    ))

    C.append(mcq('medium', 'area',
        'ត្រីកោណមួយមានបរិមាត្រ ' + M(r'36\text{ cm}') + ' និងផ្ទៃក្រឡា ' + M(r'54\text{ cm}^2') + '។ គណនាកាំ ' + M(r'r') + ' នៃរង្វង់ចារឹកក្នុងត្រីកោណ។',
        M(r'3\text{ cm}'),
        [M(r'1.5\text{ cm}'), M(r'4.5\text{ cm}'), M(r'6\text{ cm}')],
        r'p = 36/2 = 18\text{ cm} \implies r = \frac{S}{p} = \frac{54}{18} = 3\text{ cm}'
    ))

    C.append(mcq('medium', 'triangle',
        'ត្រីកោណ ' + M(r'ABC') + ' មួយមានប្រវែងជ្រុង ' + M(r'a = 4\text{ cm},\; b = 4\sqrt{3}\text{ cm},\; c = 8\text{ cm}') + '។ តើ ' + M(r'\triangle ABC') + ' ជាត្រីកោណប្រភេទអ្វី?',
        M(r'\text{ត្រីកោណកែងត្រង់ } C'),
        [M(r'\text{ត្រីកោណកែងត្រង់ } A'), M(r'\text{ត្រីកោណសម័ង្ស}'), M(r'\text{ត្រីកោណសមបាត}')],
        r'a^2 + b^2 = 16 + 48 = 64 = c^2 \implies \text{កែងត្រង់ } C'
    ))

    C.append(mcq('medium', 'sines',
        'ក្នុងត្រីកោណ ' + M(r'ABC') + ' មាន ' + M(r'\angle B = 60^\circ,\; \angle C = 45^\circ') + ' និង ' + M(r'b = 6\text{ cm}') + '។ គណនាប្រវែងជ្រុង ' + M(r'c') + '។',
        M(r'2\sqrt{6}\text{ cm}'),
        [M(r'3\sqrt{2}\text{ cm}'), M(r'3\sqrt{6}\text{ cm}'), M(r'4\sqrt{2}\text{ cm}')],
        r'c = \frac{b \sin 45^\circ}{\sin 60^\circ} = \frac{6 \times (\sqrt{2}/2)}{\sqrt{3}/2} = \frac{6\sqrt{2}}{\sqrt{3}} = 2\sqrt{6}\text{ cm}'
    ))

    C.append(mcq('medium', 'cosines',
        'ក្នុងត្រីកោណ ' + M(r'ABC') + ' មាន ' + M(r'a = 4,\; b = 6') + ' និងមុំទាល ' + M(r'\angle C = 120^\circ') + '។ គណនាប្រវែងជ្រុង ' + M(r'c') + '។',
        M(r'2\sqrt{19}'),
        [M(r'\sqrt{52}'), M(r'10'), M(r'2\sqrt{7}')],
        r'c^2 = 16 + 36 - 2(4)(6)\cos 120^\circ = 52 - 48(-1/2) = 52 + 24 = 76 \implies c = 2\sqrt{19}'
    ))

    C.append(mcq('medium', 'area',
        'ប្រលេឡូក្រាម ' + M(r'ABCD') + ' មួយមានជ្រុងពីរជាប់គ្នា ' + M(r'AB = 6\text{ cm},\; AD = 8\text{ cm}') + ' និងមុំ ' + M(r'\angle A = 60^\circ') + '។ គណនាផ្ទៃក្រឡាប្រលេឡូក្រាមនោះ។',
        M(r'24\sqrt{3}\text{ cm}^2'),
        [M(r'48\text{ cm}^2'), M(r'12\sqrt{3}\text{ cm}^2'), M(r'24\text{ cm}^2')],
        r'S = AB \times AD \times \sin A = 6 \times 8 \times \frac{\sqrt{3}}{2} = 24\sqrt{3}\text{ cm}^2'
    ))

    C.append(mcq('medium', 'heron',
        'ត្រីកោណមួយមានប្រវែងជ្រុង ' + M(r'a = 7,\; b = 8,\; c = 9') + '។ គណនាផ្ទៃក្រឡា ' + M(r'S') + ' នៃត្រីកោណនេះ។',
        M(r'12\sqrt{5}'),
        [M(r'24\sqrt{5}'), M(r'15\sqrt{3}'), M(r'28')],
        r'p = 12; S = \sqrt{12(5)(4)(3)} = \sqrt{720} = 12\sqrt{5}'
    ))

    C.append(mcq('medium', 'applied',
        'អ្នកវាស់ដីម្នាក់ចង់រកចម្ងាយឆ្លងកាត់ស្រះទឹកពីចំណុច ' + M(r'A') + ' ទៅ ' + M(r'B') + '។ គាត់ឈរនៅចំណុច ' + M(r'C') + ' ហើយវាស់បាន ' + M(r'CA = 50\text{ m},\; CB = 70\text{ m}') + ' និងមុំ ' + M(r'\angle ACB = 60^\circ') + '។ គណនាចម្ងាយ ' + M(r'AB') + '។',
        M(r'10\sqrt{39}\text{ m}'),
        [M(r'60\text{ m}'), M(r'10\sqrt{74}\text{ m}'), M(r'65\text{ m}')],
        r'c^2 = 2500 + 4900 - 2(50)(70)(0.5) = 7400 - 3500 = 3900 \implies c = 10\sqrt{39}\text{ m}'
    ))

    # ---------------------------------------------------------------------
    # MCQ Hard (Target: 7)
    # ---------------------------------------------------------------------
    C.append(mcq('hard', 'cosines',
        'ក្នុងត្រីកោណ ' + M(r'ABC') + ' បើគេមានទំនាក់ទំនង ' + M(r'a^2 = b^2 + c^2 + bc') + ' នោះរង្វាស់មុំ ' + M(r'\angle A') + ' ស្មើនឹង ៖',
        M(r'120^\circ'),
        [M(r'60^\circ'), M(r'150^\circ'), M(r'135^\circ')],
        r'-2bc \cos A = bc \implies \cos A = -1/2 \implies A = 120^\circ'
    ))

    C.append(mcq('hard', 'sines',
        'ក្នុងត្រីកោណ ' + M(r'ABC') + ' បើគេមាន ' + M(r'\dfrac{a}{\cos A} = \dfrac{b}{\cos B}') + ' នោះ ' + M(r'\triangle ABC') + ' ជាត្រីកោណអ្វី?',
        M(r'\text{ត្រីកោណសមបាតដែលមាន } a = b'),
        [M(r'\text{ត្រីកោណសម័ង្ស}'), M(r'\text{ត្រីកោណកែង}'), M(r'\text{ត្រីកោណមិនអាចកំណត់បាន}')],
        r'\frac{2R\sin A}{\cos A} = \frac{2R\sin B}{\cos B} \implies \tan A = \tan B \implies A = B \implies a = b'
    ))

    C.append(mcq('hard', 'circum',
        'ត្រីកោណ ' + M(r'ABC') + ' មានជ្រុង ' + M(r'a = 13,\; b = 14,\; c = 15') + ' និងផ្ទៃក្រឡា ' + M(r'S = 84') + '។ គណនាកាំ ' + M(r'R') + ' នៃរង្វង់ចារឹកក្រៅត្រីកោណ។',
        M(r'\dfrac{65}{8}'),
        [M(r'\dfrac{65}{4}'), M(r'8'), M(r'\dfrac{35}{4}')],
        r'R = \frac{abc}{4S} = \frac{13 \times 14 \times 15}{4 \times 84} = \frac{2730}{336} = \frac{65}{8} = 8.125'
    ))

    C.append(mcq('hard', 'area',
        'ក្នុងត្រីកោណ ' + M(r'ABC') + ' មាន ' + M(r'b = 8,\; c = 5') + ' និងផ្ទៃក្រឡា ' + M(r'S = 10\sqrt{3}') + '។ បើមុំ ' + M(r'\angle A') + ' ជាមុំទាល ចូរគណនាប្រវែងជ្រុង ' + M(r'a') + '។',
        M(r'\sqrt{129}'),
        [M(r'\sqrt{49} = 7'), M(r'\sqrt{89}'), M(r'\sqrt{109}')],
        r'S = 20\sin A = 10\sqrt{3} \implies \sin A = \sqrt{3}/2 \implies A = 120^\circ \implies a^2 = 64 + 25 - 2(40)(-1/2) = 129 \implies a = \sqrt{129}'
    ))

    C.append(mcq('hard', 'median',
        'ក្នុងត្រីកោណ ' + M(r'ABC') + ' មាន ' + M(r'a = 6,\; b = 8,\; c = 10') + '។ គណនាប្រវែងមេដ្យាន ' + M(r'm_a') + ' គូសចេញពីកំពូល ' + M(r'A') + ' ទៅកាន់ជ្រុង ' + M(r'a') + '។',
        M(r'\sqrt{73}'),
        [M(r'5'), M(r'\sqrt{85}'), M(r'2\sqrt{17}')],
        r'm_a^2 = \frac{2b^2 + 2c^2 - a^2}{4} = \frac{2(64) + 2(100) - 36}{4} = \frac{292}{4} = 73 \implies m_a = \sqrt{73}'
    ))

    C.append(mcq('hard', 'bisector',
        'ក្នុងត្រីកោណ ' + M(r'ABC') + ' មាន ' + M(r'\angle A = 60^\circ,\; b = 5,\; c = 8') + '។ គណនាប្រវែងកន្លះបន្ទាត់ពុះមុំក្នុង ' + M(r'l_A') + '។',
        M(r'\dfrac{40\sqrt{3}}{13}'),
        [M(r'\dfrac{20\sqrt{3}}{13}'), M(r'\dfrac{40}{13}'), M(r'\dfrac{80\sqrt{3}}{13}')],
        r'l_A = \frac{2bc\cos(A/2)}{b + c} = \frac{2(5)(8)\cos 30^\circ}{13} = \frac{80 \times \frac{\sqrt{3}}{2}}{13} = \frac{40\sqrt{3}}{13}'
    ))

    C.append(mcq('hard', 'cosines',
        'ក្នុងត្រីកោណ ' + M(r'ABC') + ' បើ ' + M(r'\cos A = \dfrac{4}{5},\; \cos B = \dfrac{12}{13}') + ' (មុំស្រួចទាំងពីរ) នោះតម្លៃនៃ ' + M(r'\sin C') + ' ស្មើនឹង ៖',
        M(r'\dfrac{56}{65}'),
        [M(r'\dfrac{33}{65}'), M(r'\dfrac{63}{65}'), M(r'\dfrac{16}{65}')],
        r'\sin A = 3/5, \sin B = 5/13 \implies \sin C = \sin(A+B) = \sin A \cos B + \cos A \sin B = (3/5)(12/13) + (4/5)(5/13) = 56/65'
    ))

    # ---------------------------------------------------------------------
    # MCQ PISA (Target: 5)
    # ---------------------------------------------------------------------
    C.append(with_img(
        mcq('pisa', 'pisa',
            'ចំណុច ' + M(r'A') + ' និង ' + M(r'B') + ' ស្ថិតនៅត្រើយម្ខាងនៃទន្លេមានចម្ងាយ ' + M(r'100\text{ m}') + ' ពីគ្នា។ ដើមឈើ ' + M(r'C') + ' មួយស្ថិតនៅត្រើយម្ខាងទៀត។ អ្នកវាស់ដីវាស់ឃើញ ' + M(r'\angle CAB = 60^\circ') + ' និង ' + M(r'\angle CBA = 45^\circ') + '។ គណនាចម្ងាយ ' + M(r'AC') + ' (យក ' + M(r'\sin 75^\circ \approx 0.966,\; \sin 45^\circ \approx 0.707') + ')។',
            M(r'\approx 73.2\text{ m}'),
            [M(r'\approx 81.6\text{ m}'), M(r'\approx 65.4\text{ m}'), M(r'\approx 92.5\text{ m}')],
            r'\angle C = 180^\circ - (60^\circ + 45^\circ) = 75^\circ \implies AC = \frac{100 \sin 45^\circ}{\sin 75^\circ} \approx \frac{70.7}{0.966} \approx 73.2\text{ m}'
        ),
        FIG_RIVER_SURVEY
    ))

    C.append(mcq('pisa', 'pisa',
        'ស្ថានីយឆ្នេរពីរ ' + M(r'A') + ' និង ' + M(r'B') + ' ស្ថិតនៅចម្ងាយ ' + M(r'30\text{ km}') + ' ពីគ្នា។ ស្ថានីយទាំងពីរទទួលបានសញ្ញាអាសន្នពីកប៉ាល់ ' + M(r'S') + ' ដោយវាស់បានមុំ ' + M(r'\angle SAB = 45^\circ') + ' និង ' + M(r'\angle SBA = 60^\circ') + '។ គណនាចម្ងាយពីស្ថានីយ ' + M(r'A') + ' ទៅកាន់កប៉ាល់ ' + M(r'S') + ' (យក ' + M(r'\sin 60^\circ \approx 0.866,\; \sin 75^\circ \approx 0.966') + ')។',
        M(r'\approx 26.9\text{ km}'),
        [M(r'\approx 22.5\text{ km}'), M(r'\approx 31.2\text{ km}'), M(r'\approx 19.8\text{ km}')],
        r'\angle S = 75^\circ \implies SA = \frac{30 \sin 60^\circ}{\sin 75^\circ} \approx \frac{30 \times 0.866}{0.966} \approx 26.9\text{ km}'
    ))

    C.append(mcq('pisa', 'pisa',
        'កសិករម្នាក់មានដីស្រែរាងត្រីកោណដែលមានជ្រុងជាប់ថ្នល់ពីរប្រវែង ' + M(r'60\text{ m}') + ' និង ' + M(r'80\text{ m}') + ' ដោយផ្គុំបានមុំ ' + M(r'60^\circ') + ' នៅត្រង់ផ្លូវបំបែក។ គណនាផ្ទៃក្រឡាដីស្រែនោះ (យក ' + M(r'\sqrt{3} \approx 1.732') + ')។',
        M(r'\approx 2,078\text{ m}^2'),
        [M(r'\approx 2,400\text{ m}^2'), M(r'\approx 1,850\text{ m}^2'), M(r'\approx 3,120\text{ m}^2')],
        r'S = \frac{1}{2}(60)(80)\sin 60^\circ = 2400 \times \frac{\sqrt{3}}{2} = 1200\sqrt{3} \approx 1200 \times 1.732 = 2078.4\text{ m}^2'
    ))

    C.append(mcq('pisa', 'pisa',
        'ប៉មសង្កេតការណ៍ភ្លើងព្រៃពីរ ' + M(r'T_1') + ' និង ' + M(r'T_2') + ' មានចម្ងាយ ' + M(r'10\text{ km}') + ' ពីគ្នា។ ប៉មទាំងពីរប្រទះឃើញផ្សែងភ្លើងនៅចំណុច ' + M(r'F') + ' ដោយវាស់បានមុំ ' + M(r'\angle T_2 T_1 F = 40^\circ') + ' និង ' + M(r'\angle T_1 T_2 F = 70^\circ') + '។ តើផ្សែងភ្លើងនោះនៅឆ្ងាយពីប៉ម ' + M(r'T_1') + ' ប៉ុន្មានគីឡូម៉ែត្រ?',
        M(r'10\text{ km}'),
        [M(r'8\text{ km}'), M(r'12\text{ km}'), M(r'14.5\text{ km}')],
        r'\angle F = 180^\circ - (40^\circ + 70^\circ) = 70^\circ \implies \angle T_2 = \angle F = 70^\circ \implies \triangle T_1 T_2 F \text{ សមបាត } \implies T_1 F = T_1 T_2 = 10\text{ km}'
    ))

    C.append(mcq('pisa', 'pisa',
        'អ្នកវាស់ដីម្នាក់វាស់មុំងើបទៅកាន់កំពូលភ្នំពីចំណុច ' + M(r'A') + ' ឃើញមុំ ' + M(r'30^\circ') + '។ គាត់ដើរទៅមុខតាមដីរាបស្មើចម្ងាយ ' + M(r'400\text{ m}') + ' ដល់ចំណុច ' + M(r'B') + ' ហើយវាស់មុំងើបឃើញ ' + M(r'45^\circ') + '។ គណនាកម្ពស់ភ្នំនោះ (យក ' + M(r'\sqrt{3} \approx 1.732') + ')។',
        M(r'\approx 546\text{ m}'),
        [M(r'\approx 400\text{ m}'), M(r'\approx 625\text{ m}'), M(r'\approx 480\text{ m}')],
        r'h = \frac{400}{\cot 30^\circ - \cot 45^\circ} = \frac{400}{\sqrt{3} - 1} = \frac{400(\sqrt{3} + 1)}{2} = 200(1.732 + 1) = 546.4\text{ m}'
    ))

    # ---------------------------------------------------------------------
    # Writing Easy (Target: 1)
    # ---------------------------------------------------------------------
    C.append(wr(
        'easy', 'cosines',
        'ក្នុងត្រីកោណ ' + M(r'ABC') + ' មាន ' + M(r'b = 6\text{ cm},\; c = 10\text{ cm}') + ' និងមុំកៀប ' + M(r'\angle A = 60^\circ') + '។\n'
        'ក. អនុវត្តទ្រឹស្តីបទកូស៊ីនុសដើម្បីគណនាប្រវែងជ្រុង ' + M(r'a') + '។\n'
        'ខ. គណនាផ្ទៃក្រឡា ' + M(r'S') + ' នៃត្រីកោណ ' + M(r'ABC') + '។',
        [
            ('សរសេររូបមន្តទ្រឹស្តីបទកូស៊ីនុស: a^2 = b^2 + c^2 - 2bc cos A', 1.5),
            ('ជំនួសតម្លៃលេខ: a^2 = 6^2 + 10^2 - 2(6)(10) cos 60° = 36 + 100 - 120(1/2) = 136 - 60 = 76', 1),
            ('ទាញរកប្រវែងជ្រុង a = sqrt(76) = 2 sqrt(19) cm', 1),
            ('សរសេររូបមន្តផ្ទៃក្រឡា: S = (1/2) bc sin A = (1/2)(6)(10) sin 60°', 1),
            ('គណនាផ្ទៃក្រឡា S = 30 * (sqrt(3)/2) = 15 sqrt(3) cm^2', 0.5)
        ]
    ))

    # ---------------------------------------------------------------------
    # Writing Medium (Target: 4)
    # ---------------------------------------------------------------------
    C.append(wr(
        'medium', 'sines',
        'ក្នុងត្រីកោណ ' + M(r'ABC') + ' មាន ' + M(r'\angle A = 45^\circ,\; \angle B = 60^\circ') + ' និងជ្រុង ' + M(r'a = 10\text{ cm}') + '។\n'
        'ក. គណនារង្វាស់មុំ ' + M(r'\angle C') + '។\n'
        'ខ. អនុវត្តទ្រឹស្តីបទស៊ីនុសដើម្បីគណនាប្រវែងជ្រុង ' + M(r'b') + '។\n'
        'គ. គណនាកាំ ' + M(r'R') + ' នៃរង្វង់ចារឹកក្រៅត្រីកោណ ' + M(r'ABC') + '។',
        [
            ('គណនាមុំ C: C = 180° - (45° + 60°) = 75°', 1),
            ('សរសេរទ្រឹស្តីបទស៊ីនុស: b / sin B = a / sin A', 1),
            ('ទាញរក b = (a * sin 60°) / sin 45° = 10 * (sqrt(3)/2) / (sqrt(2)/2) = 10 sqrt(3) / sqrt(2) = 5 sqrt(6) cm', 1.5),
            ('គណនាកាំ R: 2R = a / sin A = 10 / (sqrt(2)/2) = 10 sqrt(2)', 1),
            ('សន្និដ្ឋាន R = 5 sqrt(2) cm', 0.5)
        ]
    ))

    C.append(wr(
        'medium', 'heron',
        'ត្រីកោណ ' + M(r'ABC') + ' មួយមានប្រវែងជ្រុងទាំងបី ' + M(r'a = 7\text{ cm},\; b = 8\text{ cm},\; c = 9\text{ cm}') + '។\n'
        'ក. គណនាកន្លះបរិមាត្រ ' + M(r'p') + ' នៃត្រីកោណ។\n'
        'ខ. ប្រើរូបមន្តហេរ៉ុងដើម្បីគណនាផ្ទៃក្រឡា ' + M(r'S') + ' នៃត្រីកោណ។\n'
        'គ. គណនាកាំ ' + M(r'r') + ' នៃរង្វង់ចារឹកក្នុងត្រីកោណនេះ។',
        [
            ('គណនាកន្លះបរិមាត្រ: p = (7 + 8 + 9) / 2 = 24 / 2 = 12 cm', 1.5),
            ('គណនាកត្តា: p - a = 5, p - b = 4, p - c = 3', 1),
            ('អនុវត្តរូបមន្តហេរ៉ុង: S = sqrt(12 * 5 * 4 * 3) = sqrt(720) = 12 sqrt(5) cm^2', 1.5),
            ('គណនាកាំរង្វង់ចារឹកក្នុង r = S / p = 12 sqrt(5) / 12 = sqrt(5) cm', 1)
        ]
    ))

    C.append(wr(
        'medium', 'cosines',
        'ក្នុងត្រីកោណ ' + M(r'ABC') + ' មាន ' + M(r'b = 8\text{ cm},\; c = 6\text{ cm}') + ' និងមុំ ' + M(r'\angle A = 120^\circ') + '។\n'
        'ក. គណនាប្រវែងជ្រុង ' + M(r'a') + '។\n'
        'ខ. គណនាផ្ទៃក្រឡា ' + M(r'S') + ' នៃត្រីកោណ ' + M(r'ABC') + '។\n'
        'គ. គណនាប្រវែងកម្ពស់ ' + M(r'h_a') + ' គូសចេញពីកំពូល ' + M(r'A') + ' មកលើជ្រុង ' + M(r'a') + '។',
        [
            ('គណនា a^2 = 8^2 + 6^2 - 2(8)(6) cos 120° = 64 + 36 - 96(-1/2) = 100 + 48 = 148', 1.5),
            ('ទាញរក a = sqrt(148) = 2 sqrt(37) cm', 1),
            ('គណនាផ្ទៃក្រឡា S = (1/2) bc sin 120° = (1/2)(8)(6)(sqrt(3)/2) = 12 sqrt(3) cm^2', 1.5),
            ('គណនាកម្ពស់ h_a = 2S / a = 24 sqrt(3) / (2 sqrt(37)) = 12 sqrt(3) / sqrt(37) = 12 sqrt(111)/37 cm', 1)
        ]
    ))

    C.append(wr(
        'medium', 'area',
        'ដីចម្ការមួយមានរាងជាចតុកោណ ' + M(r'ABCD') + ' ត្រូវបានពុះចែកជាពីរត្រីកោណដោយអង្កត់ទ្រូង ' + M(r'AC') + '។\n'
        'គេដឹងថា ៖ ក្នុង ' + M(r'\triangle ABC') + ' មាន ' + M(r'AB = 40\text{ m},\; BC = 60\text{ m},\; \angle B = 60^\circ') + ';\n'
        'ក្នុង ' + M(r'\triangle ACD') + ' មាន ' + M(r'CD = 50\text{ m},\; AD = 30\text{ m},\; \angle D = 60^\circ') + '។\n'
        'គណនាផ្ទៃក្រឡាសរុបនៃដីចម្ការនោះ (យក ' + M(r'\sqrt{3} \approx 1.732') + ')។',
        [
            ('គណនាផ្ទៃក្រឡា S_1 នៃ ត្រីកោណ ABC: S_1 = (1/2) * 40 * 60 * sin 60° = 1200 * (sqrt(3)/2) = 600 sqrt(3) m^2', 1.5),
            ('គណនាផ្ទៃក្រឡា S_2 នៃ ត្រីកោណ ACD: S_2 = (1/2) * 50 * 30 * sin 60° = 750 * (sqrt(3)/2) = 375 sqrt(3) m^2', 1.5),
            ('គណនាផ្ទៃក្រឡាសរុប: S = S_1 + S_2 = 600 sqrt(3) + 375 sqrt(3) = 975 sqrt(3) m^2', 1),
            ('គណនាតម្លៃលេខ: S ≈ 975 * 1.732 = 1,688.7 m^2', 1)
        ]
    ))

    # ---------------------------------------------------------------------
    # Writing Hard (Target: 4)
    # ---------------------------------------------------------------------
    C.append(wr(
        'hard', 'proof',
        'ក្នុងគ្រប់ត្រីកោណ ' + M(r'ABC') + ' ស្រាយបញ្ជាក់រូបមន្តម៉ូលវ៉េដ (Mollweide\'s formula) ៖\n'
        + M(r'\dfrac{a + b}{c} = \dfrac{\cos\dfrac{A - B}{2}}{\sin\dfrac{C}{2}') + '។',
        [
            ('ប្រើទ្រឹស្តីបទស៊ីនុស a = 2R sin A, b = 2R sin B, c = 2R sin C: (a + b)/c = (sin A + sin B) / sin C', 1.5),
            ('បំប្លែងផលបូកទៅជាផលគុណ: sin A + sin B = 2 sin((A+B)/2) cos((A-B)/2)', 1.5),
            ('ដោយ A + B + C = 180° នាំឱ្យ (A+B)/2 = 90° - C/2 ដូច្នេះ sin((A+B)/2) = cos(C/2)', 1),
            ('សរសេរ sin C = 2 sin(C/2) cos(C/2) ហើយសម្រួល 2 cos(C/2) នាំឱ្យបានសមភាពពិត', 1)
        ]
    ))

    C.append(wr(
        'hard', 'heron',
        'ត្រីកោណ ' + M(r'ABC') + ' មានរង្វាស់ជ្រុងទាំងបី ' + M(r'a = 13,\; b = 14,\; c = 15') + '។\n'
        'ក. គណនាផ្ទៃក្រឡា ' + M(r'S') + ' និងកាំ ' + M(r'R') + ' នៃរង្វង់ចារឹកក្រៅត្រីកោណ។\n'
        'ខ. គណនាប្រវែងកម្ពស់ ' + M(r'h_a') + ' និងប្រវែងមេដ្យាន ' + M(r'm_a') + ' គូសទៅលើជ្រុង ' + M(r'a') + '។',
        [
            ('គណនា p = 21, S = sqrt(21 * 8 * 7 * 6) = 84', 1),
            ('គណនា R = abc / (4S) = (13 * 14 * 15) / (4 * 84) = 2730 / 336 = 65/8 = 8.125', 1),
            ('គណនាកម្ពស់ h_a = 2S / a = 2(84) / 14 = 168 / 14 = 12 (ជ្រុង a=14)', 1.5),
            ('គណនាមេដ្យាន m_a: m_a^2 = (2b^2 + 2c^2 - a^2)/4 = (2(225) + 2(169) - 196)/4 = (450 + 338 - 196)/4 = 592/4 = 148', 1),
            ('សន្និដ្ឋាន m_a = sqrt(148) = 2 sqrt(37)', 0.5)
        ]
    ))

    C.append(wr(
        'hard', 'cosines',
        'ក្នុងត្រីកោណ ' + M(r'ABC') + ' មានជ្រុង ' + M(r'a = 8\text{ cm},\; b = 10\text{ cm}') + ' និង ' + M(r'\cos C = \dfrac{1}{4}') + '។\n'
        'ក. គណនាប្រវែងជ្រុង ' + M(r'c') + '។\n'
        'ខ. គណនា ' + M(r'\sin C') + ' រួចទាញរកផ្ទៃក្រឡា ' + M(r'S') + ' នៃត្រីកោណ។\n'
        'គ. គណនាកាំ ' + M(r'R') + ' នៃរង្វង់ចារឹកក្រៅត្រីកោណ ' + M(r'ABC') + '។',
        [
            ('អនុវត្តទ្រឹស្តីបទកូស៊ីនុស: c^2 = 8^2 + 10^2 - 2(8)(10)(1/4) = 64 + 100 - 40 = 124 នាំឱ្យ c = sqrt(124) = 2 sqrt(31) cm', 1.5),
            ('គណនា sin C = sqrt(1 - (1/4)^2) = sqrt(15)/4', 1),
            ('គណនាផ្ទៃក្រឡា S = (1/2) ab sin C = (1/2)(8)(10)(sqrt(15)/4) = 10 sqrt(15) cm^2', 1),
            ('គណនាកាំ R = c / (2 sin C) = (2 sqrt(31)) / (2 * sqrt(15)/4) = 4 sqrt(31) / sqrt(15) = 4 sqrt(465)/15 cm', 1.5)
        ]
    ))

    C.append(wr(
        'hard', 'proof',
        'ក្នុងត្រីកោណ ' + M(r'ABC') + ' គេឱ្យទំនាក់ទំនងរវាងមុំ ៖ ' + M(r'\sin^2 A + \sin^2 B = \sin^2 C') + '។\n'
        'ក. ដោយប្រើទ្រឹស្តីបទស៊ីនុស ចូរស្រាយបញ្ជាក់ថា ' + M(r'\triangle ABC') + ' ជាត្រីកោណកែង។\n'
        'ខ. បើគេដឹងបន្ថែមថា ' + M(r'a = 6\text{ cm}') + ' និង ' + M(r'b = 8\text{ cm}') + ' គណនាកាំ ' + M(r'R') + ' និងកាំ ' + M(r'r') + '។',
        [
            ('ជំនួស sin A = a/2R, sin B = b/2R, sin C = c/2R នាំឱ្យ (a/2R)^2 + (b/2R)^2 = (c/2R)^2', 1.5),
            ('សម្រួល 4R^2 បាន a^2 + b^2 = c^2 តាមច្រាសទ្រឹស្តីបទពីតាករ ត្រីកោណ ABC កែងត្រង់ C', 1),
            ('គណនាអ៊ីប៉ូតេនុស c = sqrt(6^2 + 8^2) = 10 cm នាំឱ្យកាំ R = c/2 = 5 cm', 1),
            ('គណនាកាំរង្វង់ចារឹកក្នុង r = (a + b - c)/2 = (6 + 8 - 10)/2 = 2 cm', 1.5)
        ]
    ))

    # ---------------------------------------------------------------------
    # Writing PISA (Target: 5)
    # ---------------------------------------------------------------------
    C.append(wr(
        'pisa', 'pisa',
        'អ្នកវាស់ដីពីរនាក់ឈរនៅត្រើយម្ខាងនៃទន្លេត្រង់ចំណុច ' + M(r'A') + ' និង ' + M(r'B') + ' ដែលមានចម្ងាយ ' + M(r'80\text{ m}') + ' ពីគ្នា។ ពួកគេសម្លឹងមើលបង្គោល ' + M(r'C') + ' នៅត្រើយម្ខាងទៀត ដោយវាស់បានមុំ ' + M(r'\angle CAB = 75^\circ') + ' និង ' + M(r'\angle CBA = 60^\circ') + '។\n'
        'ក. គណនារង្វាស់មុំ ' + M(r'\angle ACB') + '។\n'
        'ខ. គណនាចម្ងាយ ' + M(r'AC') + ' ពីចំណុច ' + M(r'A') + ' ទៅបង្គោល ' + M(r'C') + ' (យក ' + M(r'\sqrt{2} \approx 1.414,\; \sqrt{3} \approx 1.732') + ')។\n'
        'គ. គណនាទទឹងទន្លេ (ចម្ងាយកែងពី ' + M(r'C') + ' មកខ្សែបន្ទាត់ ' + M(r'AB') + ')។',
        [
            ('គណនាមុំ ACB: C = 180° - (75° + 60°) = 45°', 1),
            ('អនុវត្តទ្រឹស្តីបទស៊ីនុស: AC / sin 60° = AB / sin 45° នាំឱ្យ AC = 80 * (sqrt(3)/2) / (sqrt(2)/2) = 80 sqrt(3)/sqrt(2) = 40 sqrt(6) m', 1.5),
            ('គណនាតម្លៃលេខ AC ≈ 40 * 2.449 = 97.96 m', 0.5),
            ('គណនាទទឹងទន្លេ h: h = AC * sin 75° ដោយ sin 75° = (sqrt(6) + sqrt(2))/4', 1),
            ('គណនា h = 40 sqrt(6) * (sqrt(6) + sqrt(2))/4 = 10(6 + 2 sqrt(3)) = 60 + 20 sqrt(3) ≈ 60 + 34.64 = 94.64 m', 1)
        ]
    ))

    C.append(wr(
        'pisa', 'pisa',
        'ស្ថានីយបញ្ជូនសញ្ញាទូរស័ព្ទចំនួនបី ' + M(r'A, B, C') + ' បង្កើតបានជាតំបន់ត្រីកោណគ្របដណ្តប់សញ្ញា ដោយមានចម្ងាយ ' + M(r'AB = 12\text{ km},\; BC = 15\text{ km},\; AC = 9\text{ km}') + '។\n'
        'ក. ផ្ទៀងផ្ទាត់ថាតើ ' + M(r'\triangle ABC') + ' ជាត្រីកោណកែងឬទេ?\n'
        'ខ. គណនាផ្ទៃក្រឡាតំបន់គ្របដណ្តប់សញ្ញា ' + M(r'S') + ' នៃត្រីកោណនេះ។\n'
        'គ. គេចង់ដំឡើងអង់តែនមេមួយនៅចំណុច ' + M(r'O') + ' ដែលនៅស្មើចម្ងាយពីស្ថានីយទាំងបី។ គណនាចម្ងាយ ' + M(r'R') + ' ពីអង់តែនមេទៅស្ថានីយនីមួយៗ។',
        [
            ('ពិនិត្យលក្ខណៈពីតាករ: 9^2 + 12^2 = 81 + 144 = 225 = 15^2 នាំឱ្យត្រីកោណ ABC កែងត្រង់ A', 1.5),
            ('គណនាផ្ទៃក្រឡា: S = (1/2) * AC * AB = (1/2) * 9 * 12 = 54 km^2', 1.5),
            ('កំណត់ទីតាំងអង់តែនមេ: ចំណុចស្មើចម្ងាយពីកំពូលទាំងបីគឺជាផ្ចិតរង្វង់ចារឹកក្រៅ O', 1),
            ('ក្នុងត្រីកោណកែង O ជាចំណុចកណ្តាលអ៊ីប៉ូតេនុស BC នាំឱ្យ R = BC / 2 = 15 / 2 = 7.5 km', 1)
        ]
    ))

    C.append(wr(
        'pisa', 'pisa',
        'យន្តហោះមួយហោះចេញពីទីក្រុង ' + M(r'A') + ' ឆ្ពោះទៅទីក្រុង ' + M(r'B') + ' ដែលនៅចម្ងាយ ' + M(r'300\text{ km}') + ' ត្រង់ទិសខាងកើត។\n'
        'ដើម្បីគេចពីពពកព្យុះ អ្នកបើកបរបានបង្វែរទិសងាក ' + M(r'20^\circ') + ' ធៀបនឹងផ្លូវដើម ហើយហោះបានចម្ងាយ ' + M(r'150\text{ km}') + ' ដល់ចំណុច ' + M(r'C') + ' រួចហើយបត់ឆ្ពោះត្រង់ទៅទីក្រុង ' + M(r'B') + ' វិញ។\n'
        'ក. សរសេររូបមន្តទ្រឹស្តីបទកូស៊ីនុសកំណត់ចម្ងាយ ' + M(r'CB') + '។\n'
        'ខ. គណនាចម្ងាយ ' + M(r'CB') + ' ដែលនៅសល់ (យក ' + M(r'\cos 20^\circ \approx 0.9397') + ')។\n'
        'គ. គណនាចម្ងាយបន្ថែមដែលយន្តហោះត្រូវហោះលើសពីផ្លូវត្រង់ដើម។',
        [
            ('សរសេរទ្រឹស្តីបទកូស៊ីនុសក្នុងត្រីកោណ ABC: CB^2 = AC^2 + AB^2 - 2(AC)(AB) cos 20°', 1.5),
            ('ជំនួសតម្លៃលេខ: CB^2 = 150^2 + 300^2 - 2(150)(300)(0.9397) = 22500 + 90000 - 90000(0.9397) = 112500 - 84573 = 27927', 1.5),
            ('ទាញរក CB = sqrt(27927) ≈ 167.1 km', 1),
            ('គណនាចម្ងាយបន្ថែម: d_បន្ថែម = (AC + CB) - AB = (150 + 167.1) - 300 = 317.1 - 300 = 17.1 km', 1)
        ]
    ))

    C.append(wr(
        'pisa', 'pisa',
        'កសិករម្នាក់ចង់ទិញដីចម្ការរាងត្រីកោណមួយកន្លែងដែលមានប្រវែងព្រំដីទាំងបីជ្រុង ' + M(r'a = 35\text{ m},\; b = 40\text{ m},\; c = 45\text{ m}') + '។\n'
        'ក. គណនាកន្លះបរិមាត្រ ' + M(r'p') + ' នៃដីចម្ការ។\n'
        'ខ. គណនាផ្ទៃក្រឡា ' + M(r'S') + ' នៃដីនោះតាមរូបមន្តហេរ៉ុង (គិតជា ' + M(r'\text{m}^2') + ')។\n'
        'គ. បើតម្លៃដីក្នុងតំបន់នោះគឺ 50 ដុល្លារក្នុងមួយម៉ែត្រការ៉េ គណនាតម្លៃប៉ាន់ស្មាននៃដីចម្ការនេះ (យក ' + M(r'\sqrt{2} \approx 1.414') + ')។',
        [
            ('គណនាកន្លះបរិមាត្រ: p = (35 + 40 + 45) / 2 = 120 / 2 = 60 m', 1),
            ('គណនាបណ្តាកត្តា: p - a = 25, p - b = 20, p - c = 15', 1),
            ('អនុវត្តរូបមន្តហេរ៉ុង: S = sqrt(60 * 25 * 20 * 15) = sqrt(450,000) = 300 sqrt(5) m^2 (ឬ sqrt(60*25*20*15) = sqrt(450000) = 670.82 m^2)', 1.5),
            ('គណនាតម្លៃលេខផ្ទៃក្រឡា: S ≈ 300 * 2.236 = 670.8 m^2', 0.5),
            ('គណនាតម្លៃដីសរុប: តម្លៃ = 670.8 * 50 = 33,540 ដុល្លារ', 1)
        ]
    ))

    C.append(wr(
        'pisa', 'pisa',
        'កប៉ាល់ដឹកទំនិញមួយសង្កេតឃើញបង្គោលភ្លើងហ្វារពីរ ' + M(r'L_1') + ' និង ' + M(r'L_2') + ' នៅលើកោះពីរផ្សេងគ្នាដែលមានចម្ងាយ ' + M(r'18\text{ km}') + ' ពីគ្នា។\n'
        'ពីកប៉ាល់ ' + M(r'S') + ' គេវាស់ឃើញមុំ ' + M(r'\angle L_1 S L_2 = 60^\circ') + ' ហើយចម្ងាយពីកប៉ាល់ទៅ ' + M(r'L_1') + ' គឺ ' + M(r'12\text{ km}') + '។\n'
        'ក. តាង ' + M(r'x = S L_2') + ' (គិតជា ' + M(r'\text{km}') + ')។ សរសេរសមីការដឺក្រេទី 2 កំណត់ ' + M(r'x') + ' តាមទ្រឹស្តីបទកូស៊ីនុស។\n'
        'ខ. ដោះស្រាយសមីការដើម្បីរកចម្ងាយ ' + M(r'x') + '។\n'
        'គ. គណនាផ្ទៃក្រឡានៃត្រីកោណ ' + M(r'S L_1 L_2') + '។',
        [
            ('អនុវត្តទ្រឹស្តីបទកូស៊ីនុស: L_1 L_2^2 = S L_1^2 + x^2 - 2(S L_1)(x) cos 60°', 1),
            ('ជំនួសតម្លៃលេខ: 18^2 = 12^2 + x^2 - 2(12)(x)(1/2) នាំឱ្យ 324 = 144 + x^2 - 12x', 1),
            ('សរសេរសមីការទូទៅ: x^2 - 12x - 180 = 0', 0.5),
            ('ដោះស្រាយសមីការ: Delta\' = 36 + 180 = 216 នាំឱ្យ x = 6 + sqrt(216) = 6 + 6 sqrt(6) ≈ 6 + 14.7 = 20.7 km (យក x > 0)', 1.5),
            ('គណនាផ្ទៃក្រឡា: S = (1/2) * 12 * (6 + 6 sqrt(6)) * sin 60° = 6(6 + 6 sqrt(6)) * (sqrt(3)/2) = 18 sqrt(3) + 18 sqrt(18) = 18 sqrt(3) + 54 sqrt(2) ≈ 107.5 km^2', 1)
        ]
    ))

    return C
