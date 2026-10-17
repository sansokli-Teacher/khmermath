from lib import *
import math

LESSON = 'ផលធៀបត្រីកោណមាត្រ'
CHAPTER = 'ជំពូកទី 5 : ផលធៀបត្រីកោណមាត្រ'

def with_img(q, svg):
    q['img'] = svg
    return q

# =========================================================================
# SVG Figures for Lesson 14
# =========================================================================

FIG_RIGHT_TRI_RATIO = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 360 220' width='360' height='220'>
  <rect width='360' height='220' fill='#ffffff'/>
  <!-- Right triangle ABC at C -->
  <polygon points='50,180 290,180 290,50' fill='#eff6ff' stroke='#1d4ed8' stroke-width='2.5'/>
  <!-- Right angle mark at C(290, 180) -->
  <polyline points='270,180 270,160 290,160' fill='none' stroke='#1e293b' stroke-width='2'/>
  <!-- Angle A arc at (50, 180) -->
  <path d='M 90,180 A 40,40 0 0,0 84,162' fill='none' stroke='#dc2626' stroke-width='2.5'/>
  <text x='96' y='170' font-family='serif' font-size='15' font-weight='bold' fill='#dc2626'>A</text>
  <!-- Vertices labels -->
  <text x='30' y='190' font-family='serif' font-size='16' font-weight='bold' fill='#1e293b'>A</text>
  <text x='298' y='190' font-family='serif' font-size='16' font-weight='bold' fill='#1e293b'>C</text>
  <text x='295' y='45' font-family='serif' font-size='16' font-weight='bold' fill='#1e293b'>B</text>
  <!-- Side labels -->
  <text x='150' y='200' font-family='Khmer OS Battambang,sans-serif' font-size='13' fill='#2563eb'>ជ្រុងជាប់ b = AC</text>
  <text x='305' y='120' font-family='Khmer OS Battambang,sans-serif' font-size='13' fill='#059669'>ជ្រុងឈម a = BC</text>
  <text x='130' y='105' font-family='Khmer OS Battambang,sans-serif' font-size='13' fill='#d97706'>អ៊ីប៉ូតេនុស c = AB</text>
</svg>"""

FIG_UNIT_CIRCLE = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 360 260' width='360' height='260'>
  <rect width='360' height='260' fill='#ffffff'/>
  <!-- Axes -->
  <line x1='30' y1='140' x2='330' y2='140' stroke='#334155' stroke-width='2'/>
  <polygon points='330,140 322,136 322,144' fill='#334155'/>
  <text x='335' y='144' font-family='serif' font-size='14' font-weight='bold' fill='#334155'>x (cos)</text>
  <line x1='180' y1='250' x2='180' y2='20' stroke='#334155' stroke-width='2'/>
  <polygon points='180,20 176,28 184,28' fill='#334155'/>
  <text x='185' y='16' font-family='serif' font-size='14' font-weight='bold' fill='#334155'>y (sin)</text>
  <text x='165' y='155' font-family='serif' font-size='13' fill='#64748b'>O</text>
  <!-- Unit circle R = 90px -->
  <circle cx='180' cy='140' r='90' fill='none' stroke='#94a3b8' stroke-width='2'/>
  <!-- Radius vector for angle alpha = 50 deg -> dx = 90*cos(50) = 57.8, dy = -90*sin(50) = -68.9 -->
  <line x1='180' y1='140' x2='238' y2='71' stroke='#2563eb' stroke-width='2.5'/>
  <circle cx='238' cy='71' r='4' fill='#2563eb'/>
  <text x='245' y='68' font-family='serif' font-size='13' font-weight='bold' fill='#2563eb'>M(cos α, sin α)</text>
  <!-- Projections -->
  <line x1='238' y1='71' x2='238' y2='140' stroke='#dc2626' stroke-width='1.5' stroke-dasharray='3,3'/>
  <line x1='238' y1='71' x2='180' y2='71' stroke='#059669' stroke-width='1.5' stroke-dasharray='3,3'/>
  <!-- Angle arc -->
  <path d='M 215,140 A 35,35 0 0,0 203,113' fill='none' stroke='#ea580c' stroke-width='2'/>
  <text x='218' y='126' font-family='serif' font-size='13' font-weight='bold' fill='#ea580c'>α</text>
  <!-- Intercept marks -->
  <text x='268' y='156' font-family='serif' font-size='12' fill='#64748b'>1</text>
  <text x='185' y='55' font-family='serif' font-size='12' fill='#64748b'>1</text>
  <text x='78' y='156' font-family='serif' font-size='12' fill='#64748b'>-1</text>
</svg>"""

FIG_SUPPLEMENTARY = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 360 220' width='360' height='220'>
  <rect width='360' height='220' fill='#ffffff'/>
  <!-- Axes -->
  <line x1='30' y1='130' x2='330' y2='130' stroke='#475569' stroke-width='2'/>
  <line x1='180' y1='210' x2='180' y2='20' stroke='#475569' stroke-width='2'/>
  <text x='335' y='134' font-family='serif' font-size='13' fill='#475569'>x</text>
  <text x='185' y='18' font-family='serif' font-size='13' fill='#475569'>y</text>
  <!-- Upper half circle R = 80 -->
  <path d='M 100,130 A 80,80 0 0,1 260,130' fill='none' stroke='#94a3b8' stroke-width='2'/>
  <!-- M(cos a, sin a) and M'(-cos a, sin a) for a = 45 deg -->
  <line x1='180' y1='130' x2='237' y2='73' stroke='#2563eb' stroke-width='2'/>
  <line x1='180' y1='130' x2='123' y2='73' stroke='#d97706' stroke-width='2'/>
  <line x1='123' y1='73' x2='237' y2='73' stroke='#dc2626' stroke-width='1.5' stroke-dasharray='3,3'/>
  <circle cx='237' cy='73' r='4' fill='#2563eb'/>
  <text x='243' y='72' font-family='serif' font-size='12' font-weight='bold' fill='#2563eb'>M(α)</text>
  <circle cx='123' cy='73' r='4' fill='#d97706'/>
  <text x='58' y='72' font-family='serif' font-size='12' font-weight='bold' fill='#d97706'>M'(180°-α)</text>
  <text x='125' y='60' font-family='Khmer OS Battambang,sans-serif' font-size='12' fill='#dc2626'>sin(180°-α) = sin α</text>
</svg>"""

FIG_SPECIAL_ANGLES = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 360 200' width='360' height='200'>
  <rect width='360' height='200' fill='#ffffff'/>
  <!-- 30-60-90 Triangle -->
  <polygon points='50,170 230,170 230,66' fill='#eff6ff' stroke='#2563eb' stroke-width='2'/>
  <polyline points='215,170 215,155 230,155' fill='none' stroke='#1e293b' stroke-width='1.5'/>
  <!-- 30 deg at (50, 170) -->
  <text x='85' y='163' font-family='serif' font-size='13' font-weight='bold' fill='#dc2626'>30°</text>
  <!-- 60 deg at (230, 66) -->
  <text x='210' y='95' font-family='serif' font-size='13' font-weight='bold' fill='#059669'>60°</text>
  <!-- Lengths -->
  <text x='130' y='188' font-family='serif' font-size='13' fill='#1e293b'>√3</text>
  <text x='240' y='125' font-family='serif' font-size='13' fill='#1e293b'>1</text>
  <text x='125' y='110' font-family='serif' font-size='13' fill='#1e293b'>2</text>
</svg>"""

FIG_ELEVATION_BASIC = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 360 210' width='360' height='210'>
  <rect width='360' height='210' fill='#ffffff'/>
  <!-- Ground -->
  <line x1='30' y1='170' x2='330' y2='170' stroke='#475569' stroke-width='2'/>
  <!-- Tower -->
  <rect x='280' y='40' width='25' height='130' fill='#cbd5e1' stroke='#334155' stroke-width='2'/>
  <!-- Line of sight -->
  <line x1='60' y1='170' x2='280' y2='40' stroke='#dc2626' stroke-width='2.5' stroke-dasharray='5,3'/>
  <!-- Angle arc -->
  <path d='M 100,170 A 40,40 0 0,0 95,149' fill='none' stroke='#2563eb' stroke-width='2'/>
  <text x='105' y='160' font-family='serif' font-size='14' font-weight='bold' fill='#2563eb'>θ</text>
  <!-- Labels -->
  <text x='40' y='190' font-family='Khmer OS Battambang,sans-serif' font-size='12' fill='#1e293b'>អ្នកសង្កេត</text>
  <text x='150' y='190' font-family='Khmer OS Battambang,sans-serif' font-size='12' fill='#1e293b'>ចម្ងាយផ្តេក d</text>
  <text x='295' y='105' font-family='Khmer OS Battambang,sans-serif' font-size='12' fill='#1e293b'>កម្ពស់ h</text>
</svg>"""

# =========================================================================
# Candidates Generator for G10L14
# =========================================================================

def cands():
    C = []

    # ---------------------------------------------------------------------
    # MCQ Easy (Target: 10)
    # ---------------------------------------------------------------------
    C.append(with_img(
        mcq('easy', 'def',
            'ក្នុងត្រីកោណកែង ' + M(r'ABC') + ' កែងត្រង់ ' + M(r'C') + ' តើផលធៀបត្រីកោណមាត្រ ' + M(r'\sin A') + ' ស្មើនឹងអ្វី?',
            M(r'\dfrac{BC}{AB}'),
            [M(r'\dfrac{AC}{AB}'), M(r'\dfrac{BC}{AC}'), M(r'\dfrac{AC}{BC}')],
            r'\sin A = \frac{BC}{AB}'
        ),
        FIG_RIGHT_TRI_RATIO
    ))

    C.append(mcq('easy', 'def',
        'ក្នុងត្រីកោណកែង ' + M(r'ABC') + ' កែងត្រង់ ' + M(r'C') + ' តើផលធៀបត្រីកោណមាត្រ ' + M(r'\cos A') + ' ស្មើនឹងអ្វី?',
        M(r'\dfrac{AC}{AB}'),
        [M(r'\dfrac{BC}{AB}'), M(r'\dfrac{BC}{AC}'), M(r'\dfrac{AB}{AC}')],
        r'\cos A = \frac{AC}{AB}'
    ))

    C.append(mcq('easy', 'def',
        'ក្នុងត្រីកោណកែង ' + M(r'ABC') + ' កែងត្រង់ ' + M(r'C') + ' តើផលធៀបត្រីកោណមាត្រ ' + M(r'\tan A') + ' ស្មើនឹងអ្វី?',
        M(r'\dfrac{BC}{AC}'),
        [M(r'\dfrac{AC}{BC}'), M(r'\dfrac{BC}{AB}'), M(r'\dfrac{AC}{AB}')],
        r'\tan A = \frac{BC}{AC}'
    ))

    C.append(mcq('easy', 'special',
        'តើតម្លៃនៃ ' + M(r'\sin 30^\circ') + ' ស្មើនឹងប៉ុន្មាន?',
        M(r'\dfrac{1}{2}'),
        [M(r'\dfrac{\sqrt{3}}{2}'), M(r'\dfrac{\sqrt{2}}{2}'), M(r'1')],
        r'\sin 30^\circ = \frac{1}{2}'
    ))

    C.append(mcq('easy', 'special',
        'តើតម្លៃនៃ ' + M(r'\cos 60^\circ') + ' ស្មើនឹងប៉ុន្មាន?',
        M(r'\dfrac{1}{2}'),
        [M(r'\dfrac{\sqrt{3}}{2}'), M(r'\dfrac{\sqrt{2}}{2}'), M(r'0')],
        r'\cos 60^\circ = \frac{1}{2}'
    ))

    C.append(mcq('easy', 'special',
        'តើតម្លៃនៃ ' + M(r'\tan 45^\circ') + ' ស្មើនឹងប៉ុន្មាន?',
        M(r'1'),
        [M(r'\dfrac{\sqrt{3}}{3}'), M(r'\sqrt{3}'), M(r'0')],
        r'\tan 45^\circ = 1'
    ))

    C.append(mcq('easy', 'identity',
        'ចំពោះគ្រប់មុំស្រួច ' + M(r'\alpha') + ' តើរូបមន្តគ្រឹះត្រីកោណមាត្រមួយណាត្រឹមត្រូវ?',
        M(r'\sin^2 \alpha + \cos^2 \alpha = 1'),
        [M(r'\sin^2 \alpha - \cos^2 \alpha = 1'), M(r'\sin \alpha + \cos \alpha = 1'), M(r'\tan^2 \alpha + \cot^2 \alpha = 1')],
        r'\sin^2 \alpha + \cos^2 \alpha = 1'
    ))

    C.append(with_img(
        mcq('easy', 'circle',
            'នៅលើរង្វង់ត្រីកោណមាត្រ ចំណុច ' + M(r'M(\alpha)') + ' មានកូអរដោនេ ' + M(r'(x, y)') + '។ តើអាប់ស៊ីស ' + M(r'x') + ' តំណាងឱ្យផលធៀបអ្វី?',
            M(r'\cos \alpha'),
            [M(r'\sin \alpha'), M(r'\tan \alpha'), M(r'\cot \alpha')],
            r'x = \cos \alpha'
        ),
        FIG_UNIT_CIRCLE
    ))

    C.append(mcq('easy', 'supp',
        'តើតម្លៃនៃ ' + M(r'\sin 150^\circ') + ' ស្មើនឹងប៉ុន្មាន?',
        M(r'\dfrac{1}{2}'),
        [M(r'-\dfrac{1}{2}'), M(r'\dfrac{\sqrt{3}}{2}'), M(r'-\dfrac{\sqrt{3}}{2}')],
        r'\sin 150^\circ = \sin(180^\circ - 30^\circ) = \sin 30^\circ = \frac{1}{2}'
    ))

    C.append(mcq('easy', 'ratio',
        'បើ ' + M(r'\sin \alpha = \dfrac{3}{5}') + ' និង ' + M(r'0^\circ < \alpha < 90^\circ') + ' នោះ ' + M(r'\cos \alpha') + ' ស្មើនឹង ៖',
        M(r'\dfrac{4}{5}'),
        [M(r'\dfrac{2}{5}'), M(r'\dfrac{3}{4}'), M(r'\dfrac{5}{4}')],
        r'\cos \alpha = \sqrt{1 - \frac{9}{25}} = \frac{4}{5}'
    ))

    # ---------------------------------------------------------------------
    # MCQ Medium (Target: 14)
    # ---------------------------------------------------------------------
    C.append(mcq('medium', 'triangle',
        'ក្នុងត្រីកោណកែង ' + M(r'ABC') + ' កែងត្រង់ ' + M(r'C') + ' មាន ' + M(r'AC = 6\text{ cm}') + ' និង ' + M(r'BC = 8\text{ cm}') + '។ គណនា ' + M(r'\sin A') + '។',
        M(r'\dfrac{4}{5}'),
        [M(r'\dfrac{3}{5}'), M(r'\dfrac{4}{3}'), M(r'\dfrac{3}{4}')],
        r'AB = 10 \implies \sin A = \frac{8}{10} = \frac{4}{5}'
    ))

    C.append(mcq('medium', 'triangle',
        'ក្នុងត្រីកោណកែង ' + M(r'ABC') + ' កែងត្រង់ ' + M(r'C') + ' មាន ' + M(r'AC = 5\text{ cm}') + ' និង ' + M(r'AB = 13\text{ cm}') + '។ គណនា ' + M(r'\tan A') + '។',
        M(r'\dfrac{12}{5}'),
        [M(r'\dfrac{5}{12}'), M(r'\dfrac{12}{13}'), M(r'\dfrac{5}{13}')],
        r'BC = 12 \implies \tan A = \frac{12}{5}'
    ))

    C.append(mcq('medium', 'calc',
        'គណនាតម្លៃនៃកន្សោម ' + M(r'A = 2\sin 30^\circ + 4\cos 60^\circ - \tan 45^\circ') + '។',
        M(r'2'),
        [M(r'1'), M(r'3'), M(r'0')],
        r'A = 2(1/2) + 4(1/2) - 1 = 1 + 2 - 1 = 2'
    ))

    C.append(mcq('medium', 'calc',
        'គណនាតម្លៃនៃកន្សោម ' + M(r'B = \sin^2 35^\circ + \sin^2 55^\circ + \tan 20^\circ \cot 20^\circ') + '។',
        M(r'2'),
        [M(r'1'), M(r'0'), M(r'3')],
        r'B = 1 + 1 = 2'
    ))

    C.append(mcq('medium', 'identity',
        'បើ ' + M(r'\tan \alpha = 3') + ' នោះ ' + M(r'\cos^2 \alpha') + ' មានតម្លៃស្មើនឹង ៖',
        M(r'\dfrac{1}{10}'),
        [M(r'\dfrac{9}{10}'), M(r'\dfrac{1}{4}'), M(r'\dfrac{1}{9}')],
        r'1 + \tan^2 \alpha = \frac{1}{\cos^2 \alpha} \implies \cos^2 \alpha = \frac{1}{10}'
    ))

    C.append(with_img(
        mcq('medium', 'supp',
            'តើតម្លៃនៃ ' + M(r'\cos 120^\circ') + ' ស្មើនឹងប៉ុន្មាន?',
            M(r'-\dfrac{1}{2}'),
            [M(r'\dfrac{1}{2}'), M(r'-\dfrac{\sqrt{3}}{2}'), M(r'\dfrac{\sqrt{3}}{2}')],
            r'\cos 120^\circ = -\cos 60^\circ = -1/2'
        ),
        FIG_SUPPLEMENTARY
    ))

    C.append(mcq('medium', 'supp',
        'តើតម្លៃនៃ ' + M(r'\tan 135^\circ') + ' ស្មើនឹងប៉ុន្មាន?',
        M(r'-1'),
        [M(r'1'), M(r'-\sqrt{3}'), M(r'-\dfrac{\sqrt{3}}{3}')],
        r'\tan 135^\circ = -\tan 45^\circ = -1'
    ))

    C.append(mcq('medium', 'supp',
        'តើតម្លៃនៃ ' + M(r'\sin 135^\circ') + ' ស្មើនឹងប៉ុន្មាន?',
        M(r'\dfrac{\sqrt{2}}{2}'),
        [M(r'-\dfrac{\sqrt{2}}{2}'), M(r'\dfrac{1}{2}'), M(r'\dfrac{\sqrt{3}}{2}')],
        r'\sin 135^\circ = \sin 45^\circ = \frac{\sqrt{2}}{2}'
    ))

    C.append(mcq('medium', 'identity',
        'បើ ' + M(r'\tan \alpha = 2') + ' គណនាតម្លៃនៃកន្សោម ' + M(r'E = \dfrac{\sin \alpha + 3\cos \alpha}{2\sin \alpha - \cos \alpha}') + '។',
        M(r'\dfrac{5}{3}'),
        [M(r'\dfrac{7}{3}'), M(r'1'), M(r'2')],
        r'E = \frac{\tan \alpha + 3}{2\tan \alpha - 1} = \frac{2 + 3}{4 - 1} = \frac{5}{3}'
    ))

    C.append(mcq('medium', 'triangle',
        'ក្នុងត្រីកោណកែង ' + M(r'ABC') + ' កែងត្រង់ ' + M(r'C') + ' មាន ' + M(r'\angle A = 30^\circ') + ' និងអ៊ីប៉ូតេនុស ' + M(r'AB = 12\text{ cm}') + '។ រកប្រវែងជ្រុង ' + M(r'BC') + '។',
        M(r'6\text{ cm}'),
        [M(r'6\sqrt{3}\text{ cm}'), M(r'4\text{ cm}'), M(r'8\text{ cm}')],
        r'BC = 12 \sin 30^\circ = 6\text{ cm}'
    ))

    C.append(mcq('medium', 'applied',
        'ជណ្តើរមួយមានប្រវែង ' + M(r'5\text{ m}') + ' ផ្អែកលើជញ្ជាំងកែងនឹងដី ដោយបង្កើតបានមុំ ' + M(r'60^\circ') + ' ធៀបនឹងដីរាបស្មើ។ តើចុងជណ្តើរខាងលើឡើងដល់កម្ពស់ប៉ុន្មាននៅលើជញ្ជាំង?',
        M(r'\dfrac{5\sqrt{3}}{2}\text{ m}'),
        [M(r'2.5\text{ m}'), M(r'5\text{ m}'), M(r'5\sqrt{3}\text{ m}')],
        r'h = 5 \sin 60^\circ = \frac{5\sqrt{3}}{2}\text{ m}'
    ))

    C.append(mcq('medium', 'identity',
        'សម្រួលកន្សោម ' + M(r'P = (\sin \alpha + \cos \alpha)^2 + (\sin \alpha - \cos \alpha)^2') + '។',
        M(r'2'),
        [M(r'1'), M(r'4\sin \alpha \cos \alpha'), M(r'0')],
        r'P = (1 + 2\sin \alpha \cos \alpha) + (1 - 2\sin \alpha \cos \alpha) = 2'
    ))

    C.append(mcq('medium', 'identity',
        'សម្រួលកន្សោម ' + M(r'Q = \dfrac{1}{1 + \sin \alpha} + \dfrac{1}{1 - \sin \alpha}') + '។',
        M(r'\dfrac{2}{\cos^2 \alpha}'),
        [M(r'\dfrac{2}{\sin^2 \alpha}'), M(r'\dfrac{2}{1 - \sin \alpha}'), M(r'\dfrac{1}{\cos^2 \alpha}')],
        r'Q = \frac{2}{1 - \sin^2 \alpha} = \frac{2}{\cos^2 \alpha}'
    ))

    C.append(mcq('medium', 'circle',
        'ចំពោះមុំទាល ' + M(r'90^\circ < \alpha < 180^\circ') + ' តើសញ្ញានៃផលធៀបត្រីកោណមាត្រមួយណាត្រឹមត្រូវ?',
        M(r'\sin \alpha > 0,\; \cos \alpha < 0,\; \tan \alpha < 0'),
        [M(r'\sin \alpha < 0,\; \cos \alpha < 0,\; \tan \alpha > 0'),
         M(r'\sin \alpha > 0,\; \cos \alpha > 0,\; \tan \alpha > 0'),
         M(r'\sin \alpha < 0,\; \cos \alpha > 0,\; \tan \alpha < 0')],
        r'\sin \alpha > 0,\; \cos \alpha < 0,\; \tan \alpha < 0'
    ))

    # ---------------------------------------------------------------------
    # MCQ Hard (Target: 7)
    # ---------------------------------------------------------------------
    C.append(mcq('hard', 'algebra',
        'គេឱ្យ ' + M(r'\sin \alpha + \cos \alpha = \dfrac{7}{5}') + '។ គណនាតម្លៃនៃ ' + M(r'\sin \alpha \cos \alpha') + '។',
        M(r'\dfrac{12}{25}'),
        [M(r'\dfrac{24}{25}'), M(r'\dfrac{6}{25}'), M(r'\dfrac{7}{25}')],
        r'1 + 2\sin \alpha \cos \alpha = 49/25 \implies \sin \alpha \cos \alpha = 12/25'
    ))

    C.append(mcq('hard', 'algebra',
        'គេឱ្យ ' + M(r'\tan \alpha + \cot \alpha = 3') + '។ គណនាតម្លៃនៃ ' + M(r'\tan^2 \alpha + \cot^2 \alpha') + '។',
        M(r'7'),
        [M(r'9'), M(r'11'), M(r'5')],
        r'\tan^2 \alpha + \cot^2 \alpha = 3^2 - 2 = 7'
    ))

    C.append(mcq('hard', 'equation',
        'ដោះស្រាយសមីការ ' + M(r'2\sin^2 x - 3\sin x + 1 = 0') + ' ចំពោះមុំស្រួច ' + M(r'0^\circ \le x \le 90^\circ') + '។',
        M(r'x = 30^\circ \text{ ឬ } x = 90^\circ'),
        [M(r'x = 60^\circ \text{ ឬ } x = 90^\circ'), M(r'x = 45^\circ \text{ ឬ } x = 30^\circ'), M(r'x = 30^\circ \text{ តែមួយគត់}')],
        r'\sin x = 1/2 \implies x = 30^\circ; \sin x = 1 \implies x = 90^\circ'
    ))

    C.append(mcq('hard', 'supp',
        'បើ ' + M(r'\sin \alpha = \dfrac{3}{5}') + ' និង ' + M(r'90^\circ < \alpha < 180^\circ') + ' នោះតម្លៃនៃ ' + M(r'\cos \alpha') + ' និង ' + M(r'\tan \alpha') + ' ស្មើនឹង ៖',
        M(r'\cos \alpha = -\dfrac{4}{5},\; \tan \alpha = -\dfrac{3}{4}'),
        [M(r'\cos \alpha = \dfrac{4}{5},\; \tan \alpha = \dfrac{3}{4}'),
         M(r'\cos \alpha = -\dfrac{4}{5},\; \tan \alpha = \dfrac{3}{4}'),
         M(r'\cos \alpha = -\dfrac{3}{4},\; \tan \alpha = -\dfrac{4}{3}')],
        r'\cos \alpha = -4/5, \tan \alpha = -3/4'
    ))

    C.append(mcq('hard', 'algebra',
        'សម្រួលកន្សោម ' + M(r'M = \sqrt{\sin^4 \alpha + 4\cos^2 \alpha} + \sqrt{\cos^4 \alpha + 4\sin^2 \alpha}') + '។',
        M(r'3'),
        [M(r'1'), M(r'2'), M(r'4')],
        r'(2 - \sin^2 \alpha) + (2 - \cos^2 \alpha) = 4 - 1 = 3'
    ))

    C.append(mcq('hard', 'algebra',
        'គេឱ្យ ' + M(r'\sin \alpha - \cos \alpha = \dfrac{1}{3}') + '។ គណនាតម្លៃនៃ ' + M(r'\sin \alpha \cos \alpha') + '។',
        M(r'\dfrac{4}{9}'),
        [M(r'\dfrac{8}{9}'), M(r'\dfrac{2}{9}'), M(r'\dfrac{1}{9}')],
        r'1 - 2\sin \alpha \cos \alpha = 1/9 \implies \sin \alpha \cos \alpha = 4/9'
    ))

    C.append(mcq('hard', 'relation',
        'បំបាត់ ' + M(r'\alpha') + ' ពីប្រព័ន្ធ ' + M(r'x = 3 + 2\cos \alpha,\; y = -1 + 2\sin \alpha') + '។',
        M(r'(x - 3)^2 + (y + 1)^2 = 4'),
        [M(r'(x + 3)^2 + (y - 1)^2 = 4'), M(r'(x - 3)^2 + (y + 1)^2 = 2'), M(r'(x - 3)^2 - (y + 1)^2 = 4')],
        r'(x - 3)^2 + (y + 1)^2 = 4'
    ))

    # ---------------------------------------------------------------------
    # MCQ PISA (Target: 5)
    # ---------------------------------------------------------------------
    C.append(with_img(
        mcq('pisa', 'pisa',
            'បង្គោលទង់ជាតិមួយមានកម្ពស់ ' + M(r'8\text{ m}') + ' ចោលស្រមោលលើដីរាបស្មើមានប្រវែង ' + M(r'8\sqrt{3}\text{ m}') + '។ តើមុំងើបនៃព្រះអាទិត្យធៀបនឹងដីរាបស្មើស្មើនឹងប៉ុន្មាន?',
            M(r'30^\circ'),
            [M(r'45^\circ'), M(r'60^\circ'), M(r'75^\circ')],
            r'\tan \theta = 1/\sqrt{3} \implies \theta = 30^\circ'
        ),
        FIG_ELEVATION_BASIC
    ))

    C.append(mcq('pisa', 'pisa',
        'ផ្លូវជម្រាលសម្រាប់ជនពិការត្រូវសាងសង់ដោយមុំជម្រាលមិនឱ្យលើសពី ' + M(r'5^\circ') + ' ឡើយ។ បើកម្រិតកម្ពស់មាត់ទ្វារធៀបនឹងដីគឺ ' + M(r'0.6\text{ m}') + ' គណនាប្រវែងជម្រាល ' + M(r'L') + ' យ៉ាងតិចបំផុត (យក ' + M(r'\sin 5^\circ \approx 0.0872') + ')។',
        M(r'\approx 6.88\text{ m}'),
        [M(r'\approx 5.25\text{ m}'), M(r'\approx 8.40\text{ m}'), M(r'\approx 4.50\text{ m}')],
        r'L = 0.6 / 0.0872 \approx 6.88\text{ m}'
    ))

    C.append(mcq('pisa', 'pisa',
        'សុភ័ក្ត្របង្ហោះខ្លែងមួយដោយប្រើខ្សែប្រវែង ' + M(r'100\text{ m}') + ' តឹងត្រង់ ដោយបង្កើតបានមុំ ' + M(r'45^\circ') + ' ធៀបនឹងដីរាបស្មើ។ បើដៃគាត់កាន់ខ្សែខ្លែងខ្ពស់ពីដី ' + M(r'1.2\text{ m}') + ' តើខ្លែងកំពុងហោះនៅកម្ពស់ប៉ុន្មានពីដី? (យក ' + M(r'\sqrt{2} \approx 1.414') + ')',
        M(r'\approx 71.9\text{ m}'),
        [M(r'\approx 70.7\text{ m}'), M(r'\approx 85.2\text{ m}'), M(r'\approx 65.5\text{ m}')],
        r'h = 100 \times \frac{\sqrt{2}}{2} + 1.2 \approx 71.9\text{ m}'
    ))

    C.append(mcq('pisa', 'pisa',
        'ផ្ទាំងសូឡាមួយប្រវែង ' + M(r'2.0\text{ m}') + ' តាមបណ្តោយជម្រាល ត្រូវបានដំឡើងទ្រេតមុំ ' + M(r'15^\circ') + ' ធៀបនឹងដំបូលរាបស្មើ។ គណនាកម្ពស់បញ្ឈរនៃគែមខាងលើធៀបនឹងបាតក្រោម (យក ' + M(r'\sin 15^\circ \approx 0.2588') + ')។',
        M(r'\approx 51.8\text{ cm}'),
        [M(r'\approx 45.0\text{ cm}'), M(r'\approx 62.4\text{ cm}'), M(r'\approx 38.6\text{ cm}')],
        r'h = 2.0 \times 0.2588 = 0.5176\text{ m} \approx 51.8\text{ cm}'
    ))

    C.append(mcq('pisa', 'pisa',
        'ដ្រូនមួយកំពុងហោះត្រង់ពីលើចំណុច ' + M(r'H') + ' លើដីនៅកម្ពស់ ' + M(r'60\text{ m}') + '។ អ្នកបញ្ជាឈរនៅចំណុច ' + M(r'P') + ' លើដីសម្លឹងមើលដ្រូនឃើញមុំងើប ' + M(r'60^\circ') + '។ គណនាចម្ងាយខ្សែភ្នែកពីអ្នកបញ្ជាទៅដ្រូន។',
        M(r'40\sqrt{3}\text{ m}'),
        [M(r'30\sqrt{3}\text{ m}'), M(r'120\text{ m}'), M(r'60\sqrt{3}\text{ m}')],
        r'd = 60 / \sin 60^\circ = 40\sqrt{3}\text{ m}'
    ))

    # ---------------------------------------------------------------------
    # Writing Easy (Target: 1)
    # ---------------------------------------------------------------------
    C.append(wr(
        'easy', 'triangle',
        'ក្នុងត្រីកោណកែង ' + M(r'ABC') + ' កែងត្រង់ ' + M(r'C') + ' មានរង្វាស់ជ្រុង ' + M(r'BC = 5\text{ cm}') + ' និង ' + M(r'AC = 12\text{ cm}') + '។\n'
        'ក. គណនាប្រវែងអ៊ីប៉ូតេនុស ' + M(r'AB') + '។\n'
        'ខ. គណនាផលធៀបត្រីកោណមាត្រទាំងបួននៃមុំ ' + M(r'A') + ' (' + M(r'\sin A, \cos A, \tan A, \cot A') + ')។',
        [
            ('អនុវត្តទ្រឹស្តីបទពីតាករ: AB = sqrt(AC^2 + BC^2) = sqrt(144 + 25) = sqrt(169) = 13 cm', 1.5),
            ('គណនា sin A = BC / AB = 5 / 13', 1),
            ('គណនា cos A = AC / AB = 12 / 13', 1),
            ('គណនា tan A = BC / AC = 5 / 12', 1),
            ('គណនា cot A = AC / BC = 12 / 5', 0.5)
        ]
    ))

    # ---------------------------------------------------------------------
    # Writing Medium (Target: 4)
    # ---------------------------------------------------------------------
    C.append(wr(
        'medium', 'identity',
        'គេឱ្យ ' + M(r'\cos \alpha = -\dfrac{3}{5}') + ' ដោយដឹងថា ' + M(r'90^\circ < \alpha < 180^\circ') + '។\n'
        'ក. គណនាតម្លៃនៃ ' + M(r'\sin \alpha') + ', ' + M(r'\tan \alpha') + ' និង ' + M(r'\cot \alpha') + '។\n'
        'ខ. គណនាតម្លៃនៃកន្សោម ' + M(r'A = \dfrac{\sin \alpha - 2\cos \alpha}{\tan \alpha + \cot \alpha}') + '។',
        [
            ('គណនា sin α: ក្នុងកាដ្រង់ទី 2, sin α > 0 នាំឱ្យ sin α = sqrt(1 - (-3/5)^2) = sqrt(16/25) = 4/5', 1.5),
            ('គណនា tan α = sin α / cos α = (4/5) / (-3/5) = -4/3 និង cot α = -3/4', 1),
            ('គណនាភាគយក: sin α - 2 cos α = 4/5 - 2(-3/5) = 4/5 + 6/5 = 10/5 = 2', 1),
            ('គណនាភាគបែង: tan α + cot α = -4/3 - 3/4 = (-16 - 9) / 12 = -25/12', 1),
            ('សន្និដ្ឋានតម្លៃ A = 2 / (-25/12) = -24/25', 0.5)
        ]
    ))

    C.append(wr(
        'medium', 'calc',
        'គណនាតម្លៃប្រាកដនៃកន្សោមត្រីកោណមាត្រខាងក្រោម ៖\n'
        + M(r'M = 4\cos^2 30^\circ - 3\tan 45^\circ + 2\sin 60^\circ \tan 30^\circ - \cos 180^\circ') + '។',
        [
            ('ជំនួស cos 30° = sqrt(3)/2 នាំឱ្យ 4 cos^2 30° = 4(3/4) = 3', 1.5),
            ('ជំនួស tan 45° = 1 នាំឱ្យ -3 tan 45° = -3', 1),
            ('ជំនួស sin 60° = sqrt(3)/2 និង tan 30° = sqrt(3)/3 នាំឱ្យ 2(sqrt(3)/2)(sqrt(3)/3) = 1', 1),
            ('ជំនួស cos 180° = -1 នាំឱ្យ -cos 180° = -(-1) = 1', 1),
            ('បូកបញ្ចូលគ្នា: M = 3 - 3 + 1 + 1 = 2', 0.5)
        ]
    ))

    C.append(wr(
        'medium', 'proof',
        'ក. ស្រាយបញ្ជាក់សមភាពត្រីកោណមាត្រ ៖ ' + M(r'\dfrac{1 - \cos \alpha}{\sin \alpha} = \dfrac{\sin \alpha}{1 + \cos \alpha}') + '។\n'
        'ខ. ទាញរកតម្លៃសម្រួលនៃកន្សោម ' + M(r'S = \dfrac{1 - \cos \alpha}{\sin \alpha} + \dfrac{\sin \alpha}{1 - \cos \alpha}') + '។',
        [
            ('គុណខ្វែងត្រួតពិនិត្យ: (1 - cos α)(1 + cos α) = 1 - cos^2 α', 1),
            ('ប្រើរូបមន្តគ្រឹះ 1 - cos^2 α = sin^2 α = sin α * sin α នាំឱ្យសមភាពទីមួយពិត', 1.5),
            ('តម្រូវភាគបែងកន្សោម S: ភាគបែងរួមគឺ sin α (1 - cos α)', 1),
            ('គណនាភាគយក: (1 - cos α)^2 + sin^2 α = 1 - 2cos α + cos^2 α + sin^2 α = 2 - 2cos α = 2(1 - cos α)', 1),
            ('សម្រួលតួ (1 - cos α): S = 2(1 - cos α) / [sin α (1 - cos α)] = 2 / sin α', 0.5)
        ]
    ))

    C.append(wr(
        'medium', 'triangle',
        'ក្នុងត្រីកោណកែង ' + M(r'ABC') + ' កែងត្រង់ ' + M(r'C') + ' មាន ' + M(r'AB = 10\text{ cm}') + ' និងមុំ ' + M(r'\angle A = 30^\circ') + '។\n'
        'ក. គណនាប្រវែងជ្រុង ' + M(r'BC') + ' និង ' + M(r'AC') + '។\n'
        'ខ. គណនាប្រវែងកម្ពស់ ' + M(r'CH') + ' គូសចេញពីកំពូល ' + M(r'C') + ' មកលើអ៊ីប៉ូតេនុស ' + M(r'AB') + '។',
        [
            ('គណនា BC = AB * sin 30° = 10 * (1/2) = 5 cm', 1.5),
            ('គណនា AC = AB * cos 30° = 10 * (sqrt(3)/2) = 5 sqrt(3) cm', 1.5),
            ('ប្រើរូបមន្តផ្ទៃក្រឡា: S = (1/2) * AC * BC = (1/2) * CH * AB', 1),
            ('ទាញរក CH = (AC * BC) / AB = (5 * 5 sqrt(3)) / 10 = 2.5 sqrt(3) cm (ឬ 5 sqrt(3)/2 cm)', 1)
        ]
    ))

    # ---------------------------------------------------------------------
    # Writing Hard (Target: 4)
    # ---------------------------------------------------------------------
    C.append(wr(
        'hard', 'algebra',
        'គេឱ្យ ' + M(r'\sin \alpha + \cos \alpha = \sqrt{2}') + '។\n'
        'ក. គណនាតម្លៃនៃ ' + M(r'\sin \alpha \cos \alpha') + '។\n'
        'ខ. គណនាតម្លៃនៃ ' + M(r'\sin^3 \alpha + \cos^3 \alpha') + ' និង ' + M(r'\sin^4 \alpha + \cos^4 \alpha') + '។',
        [
            ('លើកជាការេ: (sin α + cos α)^2 = 1 + 2 sin α cos α = (sqrt(2))^2 = 2', 1),
            ('ទាញរក sin α cos α = (2 - 1)/2 = 1/2', 1),
            ('ប្រើរូបមន្ត a^3 + b^3 = (a + b)(a^2 - ab + b^2) = (sqrt(2))(1 - 1/2) = sqrt(2)/2', 1.5),
            ('ប្រើរូបមន្ត a^4 + b^4 = (a^2 + b^2)^2 - 2a^2 b^2 = 1^2 - 2(1/2)^2 = 1 - 1/2 = 1/2', 1),
            ('សន្និដ្ឋាន: sin α cos α = 1/2, sin^3 α + cos^3 α = sqrt(2)/2, sin^4 α + cos^4 α = 1/2', 0.5)
        ]
    ))

    C.append(wr(
        'hard', 'equation',
        'ដោះស្រាយសមីការត្រីកោណមាត្រខាងក្រោមចំពោះមុំ ' + M(r'\alpha \in [0^\circ, 180^\circ]') + ' ៖\n'
        + M(r'2\cos^2 \alpha - 3\cos \alpha + 1 = 0') + '។',
        [
            ('កំណត់អថេរជំនួយ t = cos α ដែល -1 <= t <= 1: 2t^2 - 3t + 1 = 0', 1.5),
            ('រកឫសសមីការដឺក្រេទី 2: មាន a + b + c = 2 - 3 + 1 = 0 នាំឱ្យ t_1 = 1, t_2 = 1/2', 1.5),
            ('ករណី t = 1: cos α = 1 នាំឱ្យ α = 0°', 1),
            ('ករណី t = 1/2: cos α = 1/2 នាំឱ្យ α = 60°', 1)
        ]
    ))

    C.append(wr(
        'hard', 'triangle',
        'ត្រីកោណកែង ' + M(r'ABC') + ' មួយកែងត្រង់ ' + M(r'A') + ' មានមុំ ' + M(r'\angle B = 60^\circ') + ' និងបរិមាត្រស្មើនឹង ' + M(r'6 + 2\sqrt{3}\text{ cm}') + '។\n'
        'រកប្រវែងជ្រុងទាំងបី ' + M(r'a, b, c') + ' នៃត្រីកោណនេះ។',
        [
            ('តាមអនុគមន៍ត្រីកោណមាត្រក្នុងត្រីកោណកែង: b = AC = a * sin 60° = a * sqrt(3)/2', 1.5),
            ('ជ្រុង c = AB = a * cos 60° = a * (1/2)', 1),
            ('សរសេរសមីការបរិមាត្រ: a + b + c = a + a/2 + a*sqrt(3)/2 = a(3 + sqrt(3))/2 = 6 + 2 sqrt(3)', 1),
            ('ទាញរក a: a = 2 * 2(3 + sqrt(3)) / (3 + sqrt(3)) = 4 cm', 1),
            ('សន្និដ្ឋាន: a = 4 cm, b = 2 sqrt(3) cm, c = 2 cm', 0.5)
        ]
    ))

    C.append(wr(
        'hard', 'proof',
        'ស្រាយបញ្ជាក់ថាចំពោះគ្រប់មុំស្រួច ' + M(r'\alpha') + ' ដែល ' + M(r'\alpha \ne 45^\circ') + ' ៖\n'
        + M(r'\dfrac{1}{1 - \tan \alpha} - \dfrac{1}{1 + \tan \alpha} = \dfrac{2\tan \alpha}{1 - \tan^2 \alpha}') + '។',
        [
            ('សរសេរភាគបែងរួមនៃអង្គខាងឆ្វេង: (1 - tan α)(1 + tan α) = 1 - tan^2 α', 1.5),
            ('តម្រូវភាគបែង: ភាគយក = (1 + tan α) - (1 - tan α)', 1.5),
            ('គណនាបង្រួមភាគយក: 1 + tan α - 1 + tan α = 2 tan α', 1),
            ('ទាញបានអង្គខាងឆ្វេង = 2 tan α / (1 - tan^2 α) = អង្គខាងស្តាំ (ពិត)', 1)
        ]
    ))

    # ---------------------------------------------------------------------
    # Writing PISA (Target: 5)
    # ---------------------------------------------------------------------
    C.append(wr(
        'pisa', 'pisa',
        'សិស្សម្នាក់ចង់វាស់កម្ពស់អគារសិក្សាដោយប្រើឧបករណ៍ក្លីណូម៉ែត្រ (Clinometer)។\n'
        'គាត់ឈរនៅចម្ងាយ ' + M(r'30\text{ m}') + ' ពីជើងអគារ ហើយមើលទៅកំពូលអគារឃើញមុំងើប ' + M(r'30^\circ') + '។ កម្ពស់ពីដីទៅដល់ភ្នែកគាត់គឺ ' + M(r'1.5\text{ m}') + '។\n'
        'ក. សរសេរទំនាក់ទំនងត្រីកោណមាត្រកំណត់កម្ពស់ផ្នែកខាងលើ ' + M(r'h_1') + ' ធៀបនឹងកម្ពស់ភ្នែក។\n'
        'ខ. គណនាកម្ពស់សរុបនៃអគារសិក្សានោះ (យក ' + M(r'\sqrt{3} \approx 1.732') + ')។',
        [
            ('កំណត់គំរូធរណីមាត្រ: ត្រីកោណកែងមានជ្រុងជាប់ d = 30 m មុំងើប θ = 30° និងជ្រុងឈម h_1', 1.5),
            ('សរសេររូបមន្ត: tan 30° = h_1 / d នាំឱ្យ h_1 = d * tan 30°', 1),
            ('គណនា h_1 = 30 * (sqrt(3)/3) = 10 sqrt(3) ≈ 10 * 1.732 = 17.32 m', 1),
            ('គណនាកម្ពស់សរុប: H = h_1 + h_ភ្នែក = 17.32 + 1.5 = 18.82 m', 1),
            ('សន្និដ្ឋានថាអគារសិក្សាមានកម្ពស់ប្រហែល 18.82 ម៉ែត្រ', 0.5)
        ]
    ))

    C.append(wr(
        'pisa', 'pisa',
        'ប៉មទូរគមនាគមន៍មួយត្រូវបានទប់លំនឹងដោយខ្សែខ្សែកាបដែកចំនួន 3 ខ្សែភ្ជាប់ពីកំពូលប៉មមកដី។\n'
        'ខ្សែនីមួយៗត្រូវបានបោះយុថ្កានៅលើដីចម្ងាយ ' + M(r'24\text{ m}') + ' ពីជើងប៉ម ហើយបង្កើតបានមុំ ' + M(r'60^\circ') + ' ជាមួយដីរាបស្មើ។\n'
        'ក. គណនាកម្ពស់នៃប៉មទូរគមនាគមន៍ (គិតជា ' + M(r'\text{m}') + ')។\n'
        'ខ. គណនាប្រវែងខ្សែខ្សែកាបនីមួយៗ និងប្រវែងខ្សែកាបសរុបដែលត្រូវប្រើសម្រាប់ខ្សែទាំង 3។',
        [
            ('គណនាកម្ពស់ប៉ម: tan 60° = h / 24 នាំឱ្យ h = 24 * tan 60° = 24 sqrt(3) m (≈ 41.57 m)', 1.5),
            ('គណនាប្រវែងខ្សែនីមួយៗ L: cos 60° = 24 / L នាំឱ្យ L = 24 / cos 60°', 1.5),
            ('គណនា L = 24 / (1/2) = 48 m', 1),
            ('គណនាប្រវែងខ្សែកាបសរុបសម្រាប់ 3 ខ្សែ: L_សរុប = 3 * 48 = 144 m', 1)
        ]
    ))

    C.append(wr(
        'pisa', 'pisa',
        'អ្នកយាមបង្គោលភ្លើងហ្វារម្នាក់ស្ថិតនៅលើកំពូលច្រាំងថ្មចោទកម្ពស់ ' + M(r'50\text{ m}') + ' ពីនីវ៉ូទឹកសមុទ្រ។ គាត់សម្លឹងឃើញទូកនេសាទមួយដោយមុំទម្លាក់ ' + M(r'30^\circ') + '។\n'
        'ក. ពន្យល់អំពីទំនាក់ទំនងរវាងមុំទម្លាក់ពីបង្គោលភ្លើងហ្វារ និងមុំងើបពីទូកមកបង្គោលភ្លើងហ្វារ។\n'
        'ខ. គណនាចម្ងាយផ្តេកពីទូកនេសាទមកជើងច្រាំងថ្មចោទ (យក ' + M(r'\sqrt{3} \approx 1.732') + ')។',
        [
            ('ពន្យល់: មុំទម្លាក់និងមុំងើបជាមុំឆ្លាស់ក្នុងរវាងបន្ទាត់ផ្តេកស្របគ្នា ដូច្នេះមុំទាំងពីរមានទំហំស្មើគ្នាគឺ 30°', 1.5),
            ('កំណត់ទំនាក់ទំនងត្រីកោណមាត្រ: tan 30° = h / d ដែល h = 50 m ជាកម្ពស់ និង d ជាចម្ងាយផ្តេក', 1),
            ('ទាញរក d = h / tan 30° = 50 / (sqrt(3)/3) = 50 sqrt(3) m', 1.5),
            ('គណនាតម្លៃលេខ: d ≈ 50 * 1.732 = 86.6 m', 1)
        ]
    ))

    C.append(wr(
        'pisa', 'pisa',
        'ផ្លូវឡើងភ្នំមួយមានជម្រាលថេរដោយបង្កើតបានមុំ ' + M(r'18^\circ') + ' ធៀបនឹងប្លង់ដេក។\n'
        'ក. បើអ្នកឡើងភ្នំដើរបានចម្ងាយ ' + M(r'1,500\text{ m}') + ' តាមផ្លូវជម្រាល តើគាត់បានឡើងកម្ពស់បញ្ឈរបានប៉ុន្មានម៉ែត្រ? (យក ' + M(r'\sin 18^\circ \approx 0.3090') + ')\n'
        'ខ. បើគាត់ចង់ឡើងដល់កំពូលភ្នំដែលមានកម្ពស់បញ្ឈរ ' + M(r'618\text{ m}') + ' ខ្ពស់ជាងចំណុចចាប់ផ្តើម តើគាត់ត្រូវដើរតាមផ្លូវជម្រាលនេះចម្ងាយប៉ុន្មានម៉ែត្រ?',
        [
            ('សរសេរទំនាក់ទំនងកម្ពស់: h = L * sin 18° ដែល L ជាចម្ងាយតាមជម្រាល', 1.5),
            ('គណនាផ្នែក ក: h = 1500 * 0.3090 = 463.5 m', 1.5),
            ('សរសេរទំនាក់ទំនងរកចម្ងាយ: L_top = H / sin 18° = 618 / 0.3090', 1),
            ('គណនាផ្នែក ខ: L_top = 2000 m (ឬ 2 km)', 1)
        ]
    ))

    C.append(wr(
        'pisa', 'pisa',
        'បាល់ឡុងហោះមួយកំពុងហោះលើអាកាស។ អ្នកសង្កេតពីរនាក់ឈរនៅចំណុច ' + M(r'A') + ' និង ' + M(r'B') + ' លើដីរាបស្មើចម្ងាយ ' + M(r'1,000\text{ m}') + ' ពីគ្នា ដោយបាល់ឡុងស្ថិតនៅចន្លោះអ្នកទាំងពីរក្នុងប្លង់បញ្ឈរតែមួយ។\n'
        'អ្នកនៅ ' + M(r'A') + ' មើលឃើញបាល់ឡុងដោយមុំងើប ' + M(r'45^\circ') + ' រីឯអ្នកនៅ ' + M(r'B') + ' មើលឃើញដោយមុំងើប ' + M(r'60^\circ') + '។\n'
        'ក. តាង ' + M(r'h') + ' ជាកម្ពស់បាល់ឡុងពីដី។ បង្ហាញទំនាក់ទំនងរវាងចម្ងាយ ' + M(r'AB') + ' និងកម្ពស់ ' + M(r'h') + '។\n'
        'ខ. គណនាកម្ពស់ ' + M(r'h') + ' នៃបាល់ឡុង (យក ' + M(r'\sqrt{3} \approx 1.732') + ')។',
        [
            ('តាង H ជាចំណុចលើដីចំពីក្រោមបាល់ឡុង: AH = h / tan 45° = h, BH = h / tan 60° = h / sqrt(3)', 1.5),
            ('សរសេរសមីការចម្ងាយសរុប: AB = AH + BH = h + h / sqrt(3) = h(1 + 1/sqrt(3)) = 1000 m', 1),
            ('ទាញរក h: h(sqrt(3) + 1)/sqrt(3) = 1000 នាំឱ្យ h = 1000 sqrt(3) / (sqrt(3) + 1)', 1),
            ('បំបាត់រ៉ាឌីកាល់: h = 1000 sqrt(3)(sqrt(3) - 1) / 2 = 500(3 - sqrt(3)) ≈ 500(3 - 1.732) = 500(1.268) = 634 m', 1),
            ('សន្និដ្ឋានថាកម្ពស់បាល់ឡុងគឺប្រហែល 634 ម៉ែត្រ', 0.5)
        ]
    ))

    return C
