"""Bank candidates for Grade 8, Lesson 16: រង្វង់ (Circles)
Covers MoEYS Grade 8 curriculum:
  1. សញ្ញាណទូទៅនៃរង្វង់ (Center, radius, diameter, chord, secant)
  2. ការកំណត់រង្វង់ (Circles through 1, 2, and 3 non-collinear points)
  3. មុំផ្ចិតនិងធ្នូ (Central angle, minor/major arc, arc length l = pi * r * n / 180)
  4. ទំនាក់ទំនងរវាងធ្នូនិងអង្កត់ធ្នូ (Equal arcs <-> equal chords, diameter is longest chord)
  5. លក្ខណៈឆ្លុះនៃរង្វង់ (Center as point of symmetry, diameter as axis of symmetry)
  6. អង្កត់ផ្ចិតកែងនឹងអង្កត់ធ្នូ និងចម្ងាយពីផ្ចិតទៅអង្កត់ធ្នូ (Equidistant chords, perpendicular diameter bisects chord)
  7. បន្ទាត់ប៉ះរង្វង់ និងការអនុវត្តជាក់ស្តែង & PISA (Bicycle wheel, pizza slice, clock hands, circular track)

Images: Clean vector illustrations, isolated, no background, flat educational textbook style.
Geometry labels use font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic'.
"""
from lib import *

LESSON = "រង្វង់"

# --- SVG Illustrations ---

# 1. FIG_CIRCLE_ELEMENTS: Circle with center O, radius OA, diameter BC, chord DE
FIG_CIRCLE_ELEMENTS = (
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 280 200' width='280' height='200'>\n"
    "  <!-- Circle centered at (130, 100) with r = 70 -->\n"
    "  <circle cx='130' cy='100' r='70' fill='#f8fafc' stroke='#0284c7' stroke-width='2'/>\n"
    "  <!-- Center O -->\n"
    "  <circle cx='130' cy='100' r='3.5' fill='#dc2626'/>\n"
    "  <!-- Diameter BC (horizontal) -->\n"
    "  <line x1='60' y1='100' x2='200' y2='100' stroke='#334155' stroke-width='1.8'/>\n"
    "  <!-- Radius OA -->\n"
    "  <line x1='130' y1='100' x2='179.5' y2='50.5' stroke='#16a34a' stroke-width='1.8'/>\n"
    "  <!-- Chord DE -->\n"
    "  <line x1='80' y1='149' x2='180' y2='149' stroke='#a855f7' stroke-width='1.8'/>\n"
    "  <!-- Vertices and points (Mathcad italic) -->\n"
    "  <text x='125' y='94' text-anchor='end' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#dc2626'>O</text>\n"
    "  <text x='50' y='104' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>B</text>\n"
    "  <text x='210' y='104' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>C</text>\n"
    "  <text x='188' y='46' text-anchor='start' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>A</text>\n"
    "  <text x='70' y='160' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>D</text>\n"
    "  <text x='190' y='160' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>E</text>\n"
    "  <!-- Radius label r -->\n"
    "  <text x='160' y='72' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='13' fill='#16a34a'>r</text>\n"
    "</svg>"
)

# 2. FIG_CENTRAL_ANGLE: Central angle AOB intercepting arc AB
FIG_CENTRAL_ANGLE = (
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 260 200' width='260' height='200'>\n"
    "  <!-- Circle C(O, r) -->\n"
    "  <circle cx='120' cy='105' r='70' fill='#eff6ff' stroke='#0284c7' stroke-width='2'/>\n"
    "  <!-- Radii OA and OB -->\n"
    "  <line x1='120' y1='105' x2='175' y2='60' stroke='#0284c7' stroke-width='1.8'/>\n"
    "  <line x1='120' y1='105' x2='65' y2='60' stroke='#0284c7' stroke-width='1.8'/>\n"
    "  <!-- Center O -->\n"
    "  <circle cx='120' cy='105' r='3.5' fill='#dc2626'/>\n"
    "  <!-- Arc AB highlighted thick -->\n"
    "  <path d='M 65,60 A 70 70 0 0 1 175,60' fill='none' stroke='#dc2626' stroke-width='3.5'/>\n"
    "  <!-- Angle arc at O -->\n"
    "  <path d='M 98,87 A 28 28 0 0 1 142,87' fill='none' stroke='#16a34a' stroke-width='1.5'/>\n"
    "  <!-- Labels (Mathcad italic) -->\n"
    "  <text x='120' y='122' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#dc2626'>O</text>\n"
    "  <text x='55' y='55' text-anchor='end' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>A</text>\n"
    "  <text x='185' y='55' text-anchor='start' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>B</text>\n"
    "  <text x='120' y='80' text-anchor='middle' font-family='Times New Roman, serif' font-size='13' fill='#16a34a'>α</text>\n"
    "</svg>"
)

# 3. FIG_CHORD_PERP_BISECTOR: Diameter perpendicular to chord AB at H
FIG_CHORD_PERP_BISECTOR = (
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 260 200' width='260' height='200'>\n"
    "  <!-- Circle C(O, r) -->\n"
    "  <circle cx='130' cy='100' r='70' fill='#f8fafc' stroke='#0284c7' stroke-width='2'/>\n"
    "  <!-- Center O -->\n"
    "  <circle cx='130' cy='100' r='3.5' fill='#dc2626'/>\n"
    "  <!-- Vertical diameter CD -->\n"
    "  <line x1='130' y1='30' x2='130' y2='170' stroke='#334155' stroke-width='1.8'/>\n"
    "  <!-- Horizontal chord AB -->\n"
    "  <line x1='75' y1='65' x2='185' y2='65' stroke='#16a34a' stroke-width='2'/>\n"
    "  <!-- Right angle marker at H(130, 65) -->\n"
    "  <path d='M 130,75 L 140,75 L 140,65' fill='none' stroke='#dc2626' stroke-width='1.3'/>\n"
    "  <!-- Center intersection H -->\n"
    "  <circle cx='130' cy='65' r='3' fill='#dc2626'/>\n"
    "  <!-- Tick marks for AH = HB -->\n"
    "  <line x1='100' y1='61' x2='100' y2='69' stroke='#16a34a' stroke-width='1.5'/>\n"
    "  <line x1='160' y1='61' x2='160' y2='69' stroke='#16a34a' stroke-width='1.5'/>\n"
    "  <!-- Labels (Mathcad italic) -->\n"
    "  <text x='120' y='105' text-anchor='end' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#dc2626'>O</text>\n"
    "  <text x='130' y='22' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>C</text>\n"
    "  <text x='130' y='185' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>D</text>\n"
    "  <text x='65' y='68' text-anchor='end' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>A</text>\n"
    "  <text x='195' y='68' text-anchor='start' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>B</text>\n"
    "  <text x='122' y='60' text-anchor='end' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='13' fill='#dc2626'>H</text>\n"
    "</svg>"
)

# 4. FIG_EQUAL_CHORDS_DIST: Two equal chords AB and CD equidistant from center (OQ = OR)
FIG_EQUAL_CHORDS_DIST = (
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 260 200' width='260' height='200'>\n"
    "  <!-- Circle C(O, r) -->\n"
    "  <circle cx='130' cy='100' r='75' fill='#f8fafc' stroke='#0284c7' stroke-width='2'/>\n"
    "  <!-- Center O -->\n"
    "  <circle cx='130' cy='100' r='3.5' fill='#dc2626'/>\n"
    "  <!-- Chord AB -->\n"
    "  <line x1='70' y1='55' x2='190' y2='55' stroke='#16a34a' stroke-width='2'/>\n"
    "  <!-- Chord CD -->\n"
    "  <line x1='70' y1='145' x2='190' y2='145' stroke='#16a34a' stroke-width='2'/>\n"
    "  <!-- Distance segments OQ and OR (dashed) -->\n"
    "  <line x1='130' y1='100' x2='130' y2='55' stroke='#dc2626' stroke-width='1.5' stroke-dasharray='3,2'/>\n"
    "  <line x1='130' y1='100' x2='130' y2='145' stroke='#dc2626' stroke-width='1.5' stroke-dasharray='3,2'/>\n"
    "  <!-- Right angle markers -->\n"
    "  <path d='M 130,65 L 140,65 L 140,55' fill='none' stroke='#dc2626' stroke-width='1.2'/>\n"
    "  <path d='M 130,135 L 140,135 L 140,145' fill='none' stroke='#dc2626' stroke-width='1.2'/>\n"
    "  <!-- Labels (Mathcad italic) -->\n"
    "  <text x='122' y='105' text-anchor='end' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#dc2626'>O</text>\n"
    "  <text x='60' y='58' text-anchor='end' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>A</text>\n"
    "  <text x='200' y='58' text-anchor='start' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>B</text>\n"
    "  <text x='60' y='148' text-anchor='end' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>C</text>\n"
    "  <text x='200' y='148' text-anchor='start' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='14' fill='#0f172a'>D</text>\n"
    "  <text x='138' y='75' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='12' fill='#dc2626'>Q</text>\n"
    "  <text x='138' y='130' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='12' fill='#dc2626'>R</text>\n"
    "</svg>"
)


def cands():
    C = []

    def M_add(level, sec, stem, correct, wrongs, sol='', img=None):
        d = mcq(level, sec, stem, correct, wrongs, sol)
        if img: d['img'] = img
        C.append(d)

    def W(level, sec, stem, steps, img=None):
        d = wr(level, sec, stem, steps)
        if img: d['img'] = img
        C.append(d)

    # ==========================================
    # 1. MCQ EASY (10 target)
    # ==========================================
    M_add('easy', 'circle_def',
          'តើអ្វីទៅជានិយមន័យនៃរង្វង់?',
          'ជាខ្សែកោងរាបបិទដែលគ្រប់ចំណុចនៅលើខ្សែកោងនោះមានចម្ងាយស្មើគ្នាពីចំណុចនឹងមួយ (ផ្ចិត)',
          ['ជាផ្ទៃរាបដែលព័ទ្ធជុំវិញដោយជ្រុងបួនស្មើគ្នា',
           'ជាខ្សែកោងចំហដែលមានប្រវែងកំណត់',
           'ជាពហុកោណដែលមានជ្រុងច្រើនរាប់មិនអស់'],
          'រង្វង់គឺជាខ្សែកោងរាបបិទដែលគ្រប់ចំណុចលើខ្សែកោងមានចម្ងាយស្មើគ្នាពីចំណុចនឹងមួយហៅថាផ្ចិត',
          FIG_CIRCLE_ELEMENTS)

    M_add('easy', 'circle_points_count',
          'តាមបីចំណុចផ្សេងគ្នាដែលមិនស្ថិតនៅលើបន្ទាត់តែមួយ តើគេអាចគូសបានរង្វង់ចំនួនប៉ុន្មានកាត់តាមចំណុចទាំងបីនោះ?',
          '១ គត់',
          ['២', '៣', 'ច្រើនរាប់មិនអស់'],
          'តាម ៣ ចំណុចមិនរត់ត្រង់ជួរគ្នា គេអាចគូសបានរង្វង់តែមួយគត់ (រង្វង់ចារឹកក្រៅត្រីកោណ)')

    M_add('easy', 'longest_chord',
          'តើអង្កត់ធ្នូណាដែលវែងជាងគេបំផុតនៅក្នុងរង្វង់មួយ?',
          'អង្កត់ផ្ចិត',
          ['កាំ', 'ធ្នូ', 'បន្ទាត់ប៉ះ'],
          'អង្កត់ផ្ចិតគឺជាអង្កត់ធ្នូដែលវែងជាងគេនៅក្នុងរង្វង់មួយ ព្រោះវាឆ្លងកាត់ផ្ចិតរង្វង់')

    M_add('easy', 'diam_radius_rel',
          'រង្វង់មួយមានកាំ ' + M('r = 7\\ \\text{cm}') + '។ គណនាប្រវែងអង្កត់ផ្ចិត ' + M('d') + ' នៃរង្វង់។',
          M('14\\ \\text{cm}'),
          [M('7\\ \\text{cm}'), M('21\\ \\text{cm}'), M('49\\ \\text{cm}')],
          M('d = 2r = 2 \\times 7 = 14\\ \\text{cm}'))

    M_add('easy', 'central_angle_def',
          'មុំមួយដែលមានកំពូលស្ថិតនៅចំផ្ចិតនៃរង្វង់ ហើយជ្រុងទាំងពីរកាត់រង្វង់ ហៅថាមុំអ្វី?',
          'មុំផ្ចិត',
          ['មុំចារឹកក្នុង', 'មុំក្រៅ', 'មុំជាប់'],
          'មុំដែលមានកំពូលត្រង់ផ្ចិតនៃរង្វង់ ហៅថា មុំផ្ចិត (Central Angle)',
          FIG_CENTRAL_ANGLE)

    M_add('easy', 'arc_measure_central',
          'បើមុំផ្ចិត ' + M('\angle AOB = 75^\circ') + ' នោះរង្វាស់ដឺក្រេនៃធ្នូស្កាត់ ' + M('\overset{\frown}{AB}') + ' ស្មើនឹងប៉ុន្មាន?',
          M('75^\circ'),
          [M('150^\circ'), M('37.5^\circ'), M('105^\circ')],
          'រង្វាស់ដឺក្រេនៃធ្នូស្កាត់ ស្មើនឹងរង្វាស់នៃមុំផ្ចិតដែលស្កាត់ធ្នូនោះ ៖ ' + M('\overset{\frown}{AB} = \angle AOB = 75^\circ'))

    M_add('easy', 'circle_circumference_formula',
          'តើរូបមន្តគណនាបរិមាត្ររង្វង់ដែលមានកាំ ' + M('r') + ' ណាត្រឹមត្រូវ?',
          M('P = 2\pi r'),
          [M('P = \pi r^2'), M('P = 2\pi r^2'), M('P = \pi d^2')],
          'បរិមាត្ររង្វង់ ៖ ' + M('P = 2\pi r = \pi d'))

    M_add('easy', 'circle_symmetry_center',
          'តើចំណុចណាជាផ្ចិតឆ្លុះនៃរង្វង់មួយ?',
          'ផ្ចិតនៃរង្វង់',
          ['ចំណុចណាមួយនៅលើរង្វង់', 'ចុងនៃអង្កត់ផ្ចិត', 'គ្មានផ្ចិតឆ្លុះទេ'],
          'ផ្ចិតនៃរង្វង់ គឺជាផ្ចិតឆ្លុះនៃរង្វង់នោះ')

    M_add('easy', 'quadrant_arc',
          'អង្កត់ផ្ចិតពីរកែងគ្នាក្នុងរង្វង់មួយ បែងចែករង្វង់ជាធ្នូប៉ុនគ្នាចំនួន ៤។ តើធ្នូនីមួយៗ (កាដ្រង់) មានរង្វាស់ប៉ុន្មានដឺក្រេ?',
          M('90^\circ'),
          [M('180^\circ'), M('45^\circ'), M('360^\circ')],
          M('\\dfrac{360^\circ}{4} = 90^\circ'))

    M_add('easy', 'collinear_points_circle',
          'បើបីចំណុចផ្សេងគ្នាស្ថិតនៅលើបន្ទាត់តែមួយ (រត់ត្រង់ជួរគ្នា) តើគេអាចគូសបានរង្វង់កាត់តាមចំណុចទាំងបីបានឬទេ?',
          'មិនអាចទេ',
          ['បាន ១ គត់', 'បាន ២', 'បានច្រើនរាប់មិនអស់'],
          'បើបីចំណុចរត់ត្រង់ជួរគ្នា គេមិនអាចគូសរង្វង់កាត់តាមចំណុចទាំងបីនោះបានឡើយ')

    # ==========================================
    # 2. MCQ MEDIUM (14 target)
    # ==========================================
    M_add('medium', 'calc_arc_length',
          'រង្វង់មួយមានកាំ ' + M('r = 15\\ \\text{cm}') + '។ គណនាប្រវែងធ្នូដែលស្កាត់ដោយមុំផ្ចិត ' + M('80^\circ') + ' (យក ' + M('\pi \approx 3.14') + ')។',
          M('20.93\\ \\text{cm}'),
          [M('41.86\\ \\text{cm}'), M('10.47\\ \\text{cm}'), M('94.2\\ \\text{cm}')],
          M('L = \\dfrac{2\pi r \\times 80^\circ}{360^\circ} = \\dfrac{2 \\times 3.14 \\times 15 \\times 80}{360} \approx 20.93\\ \\text{cm}'))

    M_add('medium', 'calc_arc_from_iso_tri',
          'ក្នុងរង្វង់ ' + M('\mathcal{C}(O, r)') + ' ត្រីកោណ ' + M('OAB') + ' មាន ' + M('\angle OAB = 25^\circ') + '។ គណនារង្វាស់ធ្នូ ' + M('\overset{\frown}{AB}') + '។',
          M('130^\circ'),
          [M('50^\circ'), M('65^\circ'), M('155^\circ')],
          M('OA = OB = r \\Rightarrow \angle OBA = 25^\circ \\Rightarrow \angle AOB = 180^\circ - 2(25^\circ) = 130^\circ \\Rightarrow \overset{\frown}{AB} = 130^\circ'))

    M_add('medium', 'perp_diam_bisect_chord',
          'អង្កត់ផ្ចិតមួយកែងនឹងអង្កត់ធ្នូ ' + M('AB') + ' ត្រង់ ' + M('H') + '។ បើ ' + M('AB = 16\\ \\text{cm}') + ' គណនាប្រវែង ' + M('AH') + '។',
          M('8\\ \\text{cm}'),
          [M('4\\ \\text{cm}'), M('12\\ \\text{cm}'), M('16\\ \\text{cm}')],
          'អង្កត់ផ្ចិតកែងនឹងអង្កត់ធ្នូ ចែកអង្កត់ធ្នូនោះជាពីរស្មើគ្នា ៖ ' + M('AH = \\dfrac{16}{2} = 8\\ \\text{cm}'),
          FIG_CHORD_PERP_BISECTOR)

    M_add('medium', 'pyth_chord_radius',
          'រង្វង់ផ្ចិត ' + M('O') + ' មានកាំ ' + M('r = 10\\ \\text{cm}') + '។ អង្កត់ធ្នូ ' + M('AB') + ' នៅចម្ងាយ ' + M('6\\ \\text{cm}') + ' ពីផ្ចិត ' + M('O') + '។ គណនាប្រវែងអង្កត់ធ្នូ ' + M('AB') + '។',
          M('16\\ \\text{cm}'),
          [M('8\\ \\text{cm}'), M('12\\ \\text{cm}'), M('20\\ \\text{cm}')],
          M('AH = \sqrt{10^2 - 6^2} = 8\\ \\text{cm} \\Rightarrow AB = 2 \\times 8 = 16\\ \\text{cm}'))

    M_add('medium', 'equidistant_chords_eq',
          'ក្នុងរង្វង់ផ្ចិត ' + M('O') + ' អង្កត់ធ្នូ ' + M('AB') + ' និង ' + M('CD') + ' នៅចម្ងាយស្មើគ្នាពីផ្ចិត ' + M('O') + ' (' + M('OQ = OR') + ')។ បើ ' + M('AB = 18\\ \\text{cm}') + ' គណនា ' + M('CD') + '។',
          M('18\\ \\text{cm}'),
          [M('9\\ \\text{cm}'), M('36\\ \\text{cm}'), M('12\\ \\text{cm}')],
          'អង្កត់ធ្នូដែលនៅស្មើចម្ងាយពីផ្ចិត គឺជាអង្កត់ធ្នូប៉ុនគ្នា ៖ ' + M('CD = AB = 18\\ \\text{cm}'),
          FIG_EQUAL_CHORDS_DIST)

    M_add('medium', 'parallel_chords_arcs',
          'ក្នុងរង្វង់ផ្ចិត ' + M('O') + ' អង្កត់ធ្នូពីរស្របគ្នា ' + M('AB \parallel CD') + '។ តើសេចក្តីសន្និដ្ឋានណាត្រឹមត្រូវ?',
          M('\overset{\frown}{AC} = \overset{\frown}{BD}'),
          [M('\overset{\frown}{AB} = \overset{\frown}{CD}'), M('AB = CD'), M('\overset{\frown}{AD} = \overset{\frown}{BC}')],
          'អង្កត់ធ្នូពីរស្របគ្នាក្នុងរង្វង់ ស្កាត់បានធ្នូពីរនៅចន្លោះនោះប៉ុនគ្នា ៖ ' + M('\overset{\frown}{AC} = \overset{\frown}{BD}'))

    M_add('medium', 'tangent_perpendicular',
          'បន្ទាត់ ' + M('(d)') + ' ប៉ះរង្វង់ ' + M('\mathcal{C}(O, r)') + ' ត្រង់ចំណុច ' + M('A') + '។ តើមុំរវាងបន្ទាត់ប៉ះ ' + M('(d)') + ' និងកាំ ' + M('OA') + ' ស្មើនឹងប៉ុន្មានដឺក្រេ?',
          M('90^\circ'),
          [M('45^\circ'), M('60^\circ'), M('180^\circ')],
          'បន្ទាត់ប៉ះរង្វង់កែងនឹងកាំត្រង់ចំណុចប៉ះ ៖ ' + M('(d) \perp OA \\Rightarrow 90^\circ'))

    M_add('medium', 'two_tangents_equal',
          'ពីចំណុច ' + M('P') + ' នៅក្រៅរង្វង់ គេគូសបន្ទាត់ប៉ះពីរ ' + M('PA') + ' និង ' + M('PB') + ' ទៅនឹងរង្វង់ផ្ចិត ' + M('O') + ' (ត្រង់ ' + M('A') + ' និង ' + M('B') + ')។ បើ ' + M('PA = 12\\ \\text{cm}') + ' គណនា ' + M('PB') + '។',
          M('12\\ \\text{cm}'),
          [M('6\\ \\text{cm}'), M('24\\ \\text{cm}'), M('15\\ \\text{cm}')],
          'អង្កត់ប៉ះទាំងពីរគូសចេញពីចំណុចតែមួយនៅក្រៅរង្វង់មានប្រវែងស្មើគ្នា ៖ ' + M('PB = PA = 12\\ \\text{cm}'))

    M_add('medium', 'equilateral_inscribed_arc',
          'ត្រីកោណសម័ង្ស ' + M('ABC') + ' មួយចារឹកក្នុងរង្វង់ផ្ចិត ' + M('O') + '។ គណនារង្វាស់នៃធ្នូនីមួយៗ ' + M('\overset{\frown}{AB}, \overset{\frown}{BC}, \overset{\frown}{CA}') + '។',
          M('120^\circ'),
          [M('60^\circ'), M('90^\circ'), M('180^\circ')],
          M('\\dfrac{360^\circ}{3} = 120^\circ'))

    M_add('medium', 'square_inscribed_arc',
          'ការេ ' + M('ABCD') + ' មួយចារឹកក្នុងរង្វង់ផ្ចិត ' + M('O') + '។ គណនារង្វាស់ដឺក្រេនៃធ្នូនីមួយៗ ' + M('\overset{\frown}{AB}') + '។',
          M('90^\circ'),
          [M('45^\circ'), M('120^\circ'), M('60^\circ')],
          M('\\dfrac{360^\circ}{4} = 90^\circ'))

    M_add('medium', 'two_circles_distance',
          'គេឱ្យរង្វង់ពីរ ' + M('\mathcal{C}(A, 3\\ \\text{cm})') + ' និង ' + M('\mathcal{C}(B, 5\\ \\text{cm})') + ' ដោយ ' + M('AB = 8\\ \\text{cm}') + '។ តើរង្វង់ទាំងពីរនេះមានទីតាំងធៀបគ្នាយ៉ាងដូចម្តេច?',
          'ប៉ះគ្នាក្រៅ',
          ['កាត់គ្នាត្រង់ ២ ចំណុច', 'នៅដាច់ពីគ្នា', 'ប៉ះគ្នាក្នុង'],
          M('d = r_1 + r_2 = 3 + 5 = 8\\ \\text{cm}') + ' ដូចនេះរង្វង់ទាំងពីរប៉ះគ្នាក្រៅ')

    M_add('medium', 'two_circles_intersect',
          'រង្វង់ពីរ ' + M('\mathcal{C}(A, 4\\ \\text{cm})') + ' និង ' + M('\mathcal{C}(B, 5\\ \\text{cm})') + ' មានចម្ងាយផ្ចិត ' + M('AB = 6\\ \\text{cm}') + '។ តើរង្វង់ទាំងពីរនេះមានទីតាំងធៀបគ្នាយ៉ាងដូចម្តេច?',
          'កាត់គ្នាត្រង់ ២ ចំណុច',
          ['ប៉ះគ្នាក្រៅ', 'ប៉ះគ្នាក្នុង', 'នៅដាច់ពីគ្នា'],
          M('|r_1 - r_2| < d < r_1 + r_2') + ' (' + M('1 < 6 < 9') + ') នាំឱ្យរង្វង់ទាំងពីរកាត់គ្នាត្រង់ ២ ចំណុច')

    M_add('medium', 'reflex_central_angle',
          'មុំផ្ចិតលយមួយមានរង្វាស់ ' + M('110^\circ') + '។ គណនារង្វាស់នៃមុំផ្ចិតឆកត្រូវគ្នា។',
          M('250^\circ'),
          [M('70^\circ'), M('200^\circ'), M('180^\circ')],
          M('360^\circ - 110^\circ = 250^\circ'))

    M_add('medium', 'chord_algebra_eq',
          'ក្នុងរង្វង់ផ្ចិត ' + M('O') + ' អង្កត់ធ្នូពីរនៅស្មើចម្ងាយពីផ្ចិត មានកន្សោម ' + M('AB = 3x + 5') + ' និង ' + M('CD = 5x - 7') + '។ គណនា ' + M('x') + '។',
          M('x = 6'),
          [M('x = 4'), M('x = 8'), M('x = 5')],
          M('3x + 5 = 5x - 7 \\Rightarrow 2x = 12 \\Rightarrow x = 6'))

    # ==========================================
    # 3. MCQ HARD (7 target)
    # ==========================================
    M_add('hard', 'tangent_length_pyth',
          'ពីចំណុច ' + M('P') + ' គេគូសបន្ទាត់ប៉ះ ' + M('PT') + ' ទៅនឹងរង្វង់ ' + M('\mathcal{C}(O, 6\\ \\text{cm})') + ' ត្រង់ ' + M('T') + '។ បើ ' + M('OP = 10\\ \\text{cm}') + ' គណនាប្រវែងបន្ទាត់ប៉ះ ' + M('PT') + '។',
          M('8\\ \\text{cm}'),
          [M('4\\ \\text{cm}'), M('12\\ \\text{cm}'), M('16\\ \\text{cm}')],
          M('PT = \sqrt{OP^2 - OT^2} = \sqrt{10^2 - 6^2} = \sqrt{64} = 8\\ \\text{cm}'))

    M_add('hard', 'chord_dist_pyth_radius',
          'រង្វង់មួយមានអង្កត់ធ្នូ ' + M('AB = 24\\ \\text{cm}') + ' និងចម្ងាយពីផ្ចិតទៅអង្កត់ធ្នូនោះគឺ ' + M('5\\ \\text{cm}') + '។ គណនាកាំ ' + M('r') + ' នៃរង្វង់។',
          M('13\\ \\text{cm}'),
          [M('12\\ \\text{cm}'), M('15\\ \\text{cm}'), M('17\\ \\text{cm}')],
          M('AH = 12\\ \\text{cm} \\Rightarrow r = \sqrt{12^2 + 5^2} = \sqrt{144 + 25} = 13\\ \\text{cm}'))

    M_add('hard', 'two_parallel_chords_dist',
          'រង្វង់មួយមានកាំ ' + M('r = 10\\ \\text{cm}') + '។ អង្កត់ធ្នូស្របគ្នាពីរ ' + M('AB = 16\\ \\text{cm}') + ' និង ' + M('CD = 12\\ \\text{cm}') + ' ស្ថិតនៅសងខាងនៃផ្ចិត ' + M('O') + '។ គណនាចម្ងាយរវាងអង្កត់ធ្នូទាំងពីរ។',
          M('14\\ \\text{cm}'),
          [M('10\\ \\text{cm}'), M('12\\ \\text{cm}'), M('16\\ \\text{cm}')],
          M('d_1 = \sqrt{10^2 - 8^2} = 6\\ \\text{cm}') + ', ' + M('d_2 = \sqrt{10^2 - 6^2} = 8\\ \\text{cm} \\Rightarrow d = 6 + 8 = 14\\ \\text{cm}'))

    M_add('hard', 'common_chord_length',
          'រង្វង់ពីរប៉ុនគ្នាមានកាំ ' + M('r = 10\\ \\text{cm}') + ' កាត់គ្នាត្រង់ ' + M('A') + ' និង ' + M('B') + '។ ចម្ងាយរវាងផ្ចិតទាំងពីរគឺ ' + M('O_1 O_2 = 12\\ \\text{cm}') + '។ គណនាប្រវែងអង្កត់ធ្នូរួម ' + M('AB') + '។',
          M('16\\ \\text{cm}'),
          [M('8\\ \\text{cm}'), M('12\\ \\text{cm}'), M('20\\ \\text{cm}')],
          'ចំណុចប្រសព្វមេដ្យាទ័រ ៖ ' + M('O_1 H = 6\\ \\text{cm} \\Rightarrow AH = \sqrt{10^2 - 6^2} = 8\\ \\text{cm} \\Rightarrow AB = 16\\ \\text{cm}'))

    M_add('hard', 'sector_perimeter',
          'ចម្រៀករង្វង់មួយមានកាំ ' + M('r = 6\\ \\text{cm}') + ' និងមុំផ្ចិត ' + M('60^\circ') + '។ គណនាបរិមាត្រនៃចម្រៀករង្វង់នោះ (យក ' + M('\pi \approx 3.14') + ')។',
          M('18.28\\ \\text{cm}'),
          [M('6.28\\ \\text{cm}'), M('12.28\\ \\text{cm}'), M('24.28\\ \\text{cm}')],
          'ប្រវែងធ្នូ ៖ ' + M('L = \\dfrac{2 \\times 3.14 \\times 6 \\times 60}{360} = 6.28\\ \\text{cm}') + '។ បរិមាត្រចម្រៀក ៖ ' + M('P = L + 2r = 6.28 + 12 = 18.28\\ \\text{cm}'))

    M_add('hard', 'circumscribed_tri_hypotenuse',
          'ត្រីកោណកែងមួយមានជ្រុងមុំកែង ' + M('6\\ \\text{cm}') + ' និង ' + M('8\\ \\text{cm}') + '។ គណនាកាំនៃរង្វង់ចារឹកក្រៅត្រីកោណកែងនោះ។',
          M('5\\ \\text{cm}'),
          [M('10\\ \\text{cm}'), M('4\\ \\text{cm}'), M('7\\ \\text{cm}')],
          'អ៊ីប៉ូតេនុសជាអង្កត់ផ្ចិតនៃរង្វង់ចារឹកក្រៅ ៖ ' + M('c = \sqrt{6^2 + 8^2} = 10\\ \\text{cm} \\Rightarrow R = \\dfrac{10}{2} = 5\\ \\text{cm}'))

    M_add('hard', 'chord_subtended_angle',
          'ក្នុងរង្វង់ ' + M('\mathcal{C}(O, r)') + ' អង្កត់ធ្នូ ' + M('AB') + ' មានប្រវែងស្មើនឹងកាំ ' + M('r') + ' (' + M('AB = r') + ')។ គណនារង្វាស់ដឺក្រេនៃធ្នូតូច ' + M('\overset{\frown}{AB}') + '។',
          M('60^\circ'),
          [M('90^\circ'), M('45^\circ'), M('120^\circ')],
          'ត្រីកោណ ' + M('OAB') + ' មាន ' + M('OA = OB = AB = r') + ' ជាត្រីកោណសម័ង្ស នាំឱ្យ ' + M('\angle AOB = 60^\circ \\Rightarrow \overset{\frown}{AB} = 60^\circ'))

    # ==========================================
    # 4. MCQ PISA (5 target)
    # ==========================================
    M_add('pisa', 'bicycle_wheel_rotation',
          'កង់កង់មួយមានអង្កត់ផ្ចិត ' + M('70\\ \\text{cm}') + '។ តើកង់នោះវិលបានប៉ុន្មានជុំដើម្បីធ្វើដំណើរបានចម្ងាយ ' + M('220\\ \\text{m}') + ' (យក ' + M('\pi \approx \\dfrac{22}{7}') + ')?',
          M('100\\ \\text{ជុំ}'),
          [M('50\\ \\text{ជុំ}'), M('200\\ \\text{ជុំ}'), M('150\\ \\text{ជុំ}')],
          'បរិមាត្រកង់ ៖ ' + M('P = \pi d = \\dfrac{22}{7} \\times 0.7\\ \\text{m} = 2.2\\ \\text{m} \\Rightarrow N = \\dfrac{220}{2.2} = 100\\ \\text{ជុំ}'))

    M_add('pisa', 'clock_minute_hand_tip',
          'ទ្រនិចនាទីនៃនាឡិកាជញ្ជាំងមួយមានប្រវែង ' + M('14\\ \\text{cm}') + '។ គណនាចម្ងាយដែលចុងទ្រនិចនាទីចរបានក្នុងរយៈពេល ' + M('45\\ \\text{នាទី}') + ' (យក ' + M('\pi \approx \\dfrac{22}{7}') + ')។',
          M('66\\ \\text{cm}'),
          [M('88\\ \\text{cm}'), M('44\\ \\text{cm}'), M('132\\ \\text{cm}')],
          M('45\\ \\text{នាទី} = \\dfrac{3}{4}') + ' ជុំ (' + M('270^\circ') + ') ៖ ' + M('L = \\dfrac{3}{4} \\times (2 \\times \\dfrac{22}{7} \\times 14) = \\dfrac{3}{4} \\times 88 = 66\\ \\text{cm}'))

    M_add('pisa', 'pizza_slice_angle',
          'នំប៉ីហ្សា (Pizza) មូលមួយត្រូវបានកាត់ជា ៨ ចំណែកស្មើៗគ្នា។ តើមុំផ្ចិតនៃចំណែកនីមួយៗស្មើនឹងប៉ុន្មានដឺក្រេ?',
          M('45^\circ'),
          [M('30^\circ'), M('60^\circ'), M('40^\circ')],
          M('\\dfrac{360^\circ}{8} = 45^\circ'))

    M_add('pisa', 'circular_running_track',
          'ផ្លូវរត់ពហុកីឡដ្ឋានមួយជុំរាងជារង្វង់មានកាំ ' + M('50\\ \\text{m}') + '។ កីឡាករម្នាក់រត់បាន ៥ ជុំ។ គណនាចម្ងាយសរុបដែលគាត់រត់បាន (យក ' + M('\pi \approx 3.14') + ')។',
          M('1\\,570\\ \\text{m}'),
          [M('314\\ \\text{m}'), M('785\\ \\text{m}'), M('3\\,140\\ \\text{m}')],
          'មួយជុំ ៖ ' + M('P = 2 \\times 3.14 \\times 50 = 314\\ \\text{m} \\Rightarrow 5\\ \\text{ជុំ} = 314 \\times 5 = 1570\\ \\text{m}'))

    M_add('pisa', 'ferris_wheel_speed',
          'កន្ត្រកវិល (Ferris Wheel) មួយមានកាំ ' + M('21\\ \\text{m}') + ' និងវិលបានមួយជុំក្នុងរយៈពេល ' + M('2\\ \\text{នាទី}') + '។ គណនាចម្ងាយដែលកៅអីមួយចរបានក្នុងមួយជុំ (យក ' + M('\pi \approx \\dfrac{22}{7}') + ')។',
          M('132\\ \\text{m}'),
          [M('66\\ \\text{m}'), M('264\\ \\text{m}'), M('88\\ \\text{m}')],
          M('P = 2 \\times \\dfrac{22}{7} \\times 21 = 132\\ \\text{m}'))

    # ==========================================
    # 5. WRITING EASY (1 target, 5 pts total)
    # ==========================================
    W('easy', 'wr_arc_central_basic',
      'គេឱ្យរង្វង់ ' + M('\mathcal{C}(O, r)') + ' ដែលមានមុំផ្ចិត ' + M('\angle AOB = 60^\circ') + ' និងកាំ ' + M('r = 6\\ \\text{cm}') + '។\n'
      'ក. រកប្រវែងរង្វាស់ដឺក្រេនៃធ្នូស្កាត់ ' + M('\overset{\frown}{AB}') + '។\n'
      'ខ. សរសេររូបមន្ត និងគណនាប្រវែងធ្នូ ' + M('AB') + ' ជាសង់ទីម៉ែត្រ (យក ' + M('\pi \approx 3.14') + ')។', [
          ('ក. រង្វាស់ដឺក្រេនៃធ្នូស្មើនឹងរង្វាស់មុំផ្ចិត ៖ ' + M('\overset{\frown}{AB} = \angle AOB = 60^\circ'), 2),
          ('ខ. រូបមន្តប្រវែងធ្នូ ៖ ' + M('L = \\dfrac{2\pi r \\times n^\circ}{360^\circ}'), 1),
          ('ជំនួសតម្លៃ ៖ ' + M('L = \\dfrac{2 \\times 3.14 \\times 6 \\times 60}{360} = \\dfrac{37.68}{6} = 6.28\\ \\text{cm}'), 2)], FIG_CENTRAL_ANGLE)

    # ==========================================
    # 6. WRITING MEDIUM (4 target, 5 pts total each)
    # ==========================================
    W('medium', 'wr_iso_triangle_in_circle',
      'ក្នុងរង្វង់ ' + M('\mathcal{C}(O, r)') + ' ត្រីកោណ ' + M('OAB') + ' មានកំពូល ' + M('O') + ' ជាផ្ចិតរង្វង់ និង ' + M('\angle OAB = 35^\circ') + '។\n'
      'ក. បង្ហាញថា ' + M('\Delta OAB') + ' ជាត្រីកោណសមបាត រួចទាញរកមុំ ' + M('\angle OBA') + '។\n'
      'ខ. គណនាមុំផ្ចិត ' + M('\angle AOB') + ' និងទាញរកប្រវែងដឺក្រេនៃធ្នូ ' + M('\overset{\frown}{AB}') + '។', [
          ('ក. ដោយ ' + M('OA = OB = r') + ' (កាំរង្វង់តែមួយ) នោះ ' + M('\Delta OAB') + ' ជាត្រីកោណសមបាតកំពូល ' + M('O') + ' នាំឱ្យ ' + M('\angle OBA = \angle OAB = 35^\circ'), 2),
          ('ខ. ផលបូកមុំក្នុងត្រីកោណ ៖ ' + M('\angle AOB = 180^\circ - (35^\circ + 35^\circ) = 110^\circ'), 2),
          ('រង្វាស់ធ្នូស្កាត់ ៖ ' + M('\overset{\frown}{AB} = \angle AOB = 110^\circ'), 1)])

    W('medium', 'wr_perp_diam_chord_proof',
      'រង្វង់ផ្ចិត ' + M('O') + ' មានកាំ ' + M('r = 10\\ \\text{cm}') + '។ អង្កត់ផ្ចិត ' + M('CD') + ' កាត់កែងនឹងអង្កត់ធ្នូ ' + M('AB') + ' ត្រង់ចំណុច ' + M('H') + '។ ដឹងថា ' + M('OH = 6\\ \\text{cm}') + '។\n'
      'ក. បង្ហាញថា ' + M('H') + ' ជាចំណុចកណ្តាលនៃ ' + M('AB') + '។\n'
      'ខ. គណនាប្រវែង ' + M('AH') + ' និងប្រវែងអង្កត់ធ្នូ ' + M('AB') + '។', [
          ('ក. អង្កត់ផ្ចិតកែងនឹងអង្កត់ធ្នូ តែងចែកអង្កត់ធ្នូនោះជាពីរស្មើគ្នា នាំឱ្យ ' + M('H') + ' ជាចំណុចកណ្តាលនៃ ' + M('AB') + ' (' + M('AH = HB') + ')', 2),
          ('ខ. ក្នុងត្រីកោណកែង ' + M('OHA') + ' ៖ ' + M('AH = \sqrt{OA^2 - OH^2} = \sqrt{10^2 - 6^2} = \sqrt{64} = 8\\ \\text{cm}'), 2),
          ('ប្រវែងអង្កត់ធ្នូ ៖ ' + M('AB = 2AH = 2 \\times 8 = 16\\ \\text{cm}'), 1)], FIG_CHORD_PERP_BISECTOR)

    W('medium', 'wr_equal_chords_proof',
      'ក្នុងរង្វង់ផ្ចិត ' + M('O') + ' គេមានធ្នូពីរស្មើគ្នា ' + M('\overset{\frown}{AB} = \overset{\frown}{CD}') + '។\n'
      'ក. ប្រៀបធៀបមុំផ្ចិត ' + M('\angle AOB') + ' និង ' + M('\angle COD') + '។\n'
      'ខ. បង្ហាញថាត្រីកោណ ' + M('\Delta AOB \cong \Delta COD') + ' រួចទាញបញ្ជាក់ថាអង្កត់ធ្នូ ' + M('AB = CD') + '។', [
          ('ក. ដោយ ' + M('\overset{\frown}{AB} = \overset{\frown}{CD}') + ' នាំឱ្យមុំផ្ចិតស្កាត់ធ្នូទាំងពីរប៉ុនគ្នា ៖ ' + M('\angle AOB = \angle COD'), 2),
          ('ខ. ពិនិត្យ ' + M('\Delta AOB') + ' និង ' + M('\Delta COD') + ' មាន ' + M('OA = OC = r, OB = OD = r') + ' និង ' + M('\angle AOB = \angle COD'), 1),
          ('ដូចនេះ ' + M('\Delta AOB \cong \Delta COD') + ' (ករណី ជ-ម-ជ) នាំឱ្យវិបាក ' + M('AB = CD'), 2)])

    W('medium', 'wr_tangent_radius_calc',
      'ពីចំណុច ' + M('M') + ' នៅក្រៅរង្វង់ ' + M('\mathcal{C}(O, 5\\ \\text{cm})') + ' គេគូសបន្ទាត់ប៉ះ ' + M('MA') + ' ត្រង់ ' + M('A') + '។ ដឹងថា ' + M('OM = 13\\ \\text{cm}') + '។\n'
      'ក. បញ្ជាក់ពីលក្ខណៈកែងគ្នារវាងបន្ទាត់ប៉ះ ' + M('MA') + ' និងកាំ ' + M('OA') + '។\n'
      'ខ. គណនាប្រវែងបន្ទាត់ប៉ះ ' + M('MA') + '។\n'
      'គ. បើគូសបន្ទាត់ប៉ះ ' + M('MB') + ' មួយទៀតត្រង់ ' + M('B') + ' តើ ' + M('MB') + ' មានប្រវែងប៉ុន្មាន?', [
          ('ក. បន្ទាត់ប៉ះរង្វង់កែងនឹងកាំត្រង់ចំណុចប៉ះ នាំឱ្យ ' + M('MA \perp OA') + ' (មុំ ' + M('\angle OAM = 90^\circ') + ')', 1),
          ('ខ. ក្នុងត្រីកោណកែង ' + M('OAM') + ' ៖ ' + M('MA = \sqrt{OM^2 - OA^2} = \sqrt{13^2 - 5^2} = \sqrt{144} = 12\\ \\text{cm}'), 2),
          ('គ. អង្កត់ប៉ះទាំងពីរគូសចេញពីចំណុចតែមួយមានប្រវែងស្មើគ្នា ៖ ' + M('MB = MA = 12\\ \\text{cm}'), 2)])

    # ==========================================
    # 7. WRITING HARD (4 target, 5 pts total each)
    # ==========================================
    W('hard', 'wr_algebra_chord_dist',
      'គេឱ្យរង្វង់ផ្ចិត ' + M('O') + ' ដែលមានចម្ងាយពីផ្ចិតទៅអង្កត់ធ្នូទាំងពីរ ' + M('AB') + ' និង ' + M('CD') + ' ស្មើគ្នា (' + M('OQ = OR') + ')។ ដឹងថា ' + M('AB = 6x + 14') + ' និង ' + M('CD = -4x + 44') + '។\n'
      'ក. ពន្យល់ហេតុអ្វីបានជាអង្កត់ធ្នូ ' + M('AB = CD') + '។\n'
      'ខ. ដោះស្រាយសមីការរកតម្លៃ ' + M('x') + '។\n'
      'គ. គណនាប្រវែងពិតប្រាកដនៃអង្កត់ធ្នូ ' + M('AB') + ' និង ' + M('CD') + '។', [
          ('ក. អង្កត់ធ្នូទាំងពីរនៅស្មើចម្ងាយពីផ្ចិតរង្វង់ (' + M('OQ = OR') + ') នាំឱ្យអង្កត់ធ្នូទាំងពីរប៉ុនគ្នា ' + M('AB = CD'), 1),
          ('ខ. សមីការ ៖ ' + M('6x + 14 = -4x + 44 \\Rightarrow 10x = 30 \\Rightarrow x = 3'), 2),
          ('គ. ប្រវែងអង្កត់ធ្នូ ៖ ' + M('AB = 6(3) + 14 = 32') + '; ' + M('CD = -4(3) + 44 = 32') + ' (ដូចនេះ ' + M('AB = CD = 32') + ')', 2)], FIG_EQUAL_CHORDS_DIST)

    W('hard', 'wr_parallel_chords_proof',
      'គេឱ្យរង្វង់ផ្ចិត ' + M('O') + ' និងអង្កត់ផ្ចិត ' + M('AD') + '។ អង្កត់ធ្នូពីរស្របគ្នាគឺ ' + M('AB \parallel CD') + '។\n'
      'ក. បង្ហាញថា ' + M('\angle OAB = \angle ODC') + ' រួចទាញបញ្ជាក់ថា ' + M('\angle AOB = \angle COD') + '។\n'
      'ខ. បង្ហាញថា ' + M('\Delta OAB \cong \Delta OCD') + '។\n'
      'គ. ទាញសន្និដ្ឋានថា ' + M('AB = CD') + ' និង ' + M('\overset{\frown}{AB} = \overset{\frown}{CD}') + '។', [
          ('ក. ដោយ ' + M('AB \parallel CD') + ' កាត់ដោយ ' + M('AD') + ' នោះ ' + M('\angle OAB = \angle ODC') + ' (មុំឆ្លាស់ក្នុង)។ ត្រីកោណ ' + M('OAB') + ' និង ' + M('OCD') + ' សមបាតកំពូល ' + M('O') + ' នាំឱ្យ ' + M('\angle AOB = \angle COD'), 2),
          ('ខ. ' + M('\Delta OAB') + ' និង ' + M('\Delta OCD') + ' មាន ' + M('OA = OD = r, OB = OC = r') + ' និង ' + M('\angle AOB = \angle COD \\Rightarrow \Delta OAB \cong \Delta OCD') + ' (ជ-ម-ជ)', 2),
          ('គ. វិបាក ៖ ' + M('AB = CD') + ' និងធ្នូស្កាត់ដោយមុំផ្ចិតស្មើគ្នានាំឱ្យ ' + M('\overset{\frown}{AB} = \overset{\frown}{CD}'), 1)])

    W('hard', 'wr_two_chords_common_arc',
      'នៅលើរង្វង់ ' + M('\mathcal{C}(O, r)') + ' គេមានចំណុច ' + M('A, B, C, D') + ' តម្រៀបតាមលំដាប់។ ដឹងថាអង្កត់ធ្នូ ' + M('AB = CD') + '។\n'
      'ក. បង្ហាញថាធ្នូ ' + M('\overset{\frown}{AB} = \overset{\frown}{CD}') + '។\n'
      'ខ. បង្ហាញថាធ្នូ ' + M('\overset{\frown}{AC} = \overset{\frown}{BD}') + ' ដោយប្រើធ្នូរួម ' + M('\overset{\frown}{BC}') + '។\n'
      'គ. ទាញបញ្ជាក់ថាអង្កត់ធ្នូ ' + M('AC = BD') + '។', [
          ('ក. ក្នុងរង្វង់មួយ អង្កត់ធ្នូប៉ុនគ្នានាំឱ្យធ្នូដែលសន្ធឹងក្រោមអង្កត់ធ្នូទាំងពីរប៉ុនគ្នា ៖ ' + M('\overset{\frown}{AB} = \overset{\frown}{CD}'), 1),
          ('ខ. ធ្នូ ' + M('\overset{\frown}{AC} = \overset{\frown}{AB} + \overset{\frown}{BC}') + ' និង ' + M('\overset{\frown}{BD} = \overset{\frown}{BC} + \overset{\frown}{CD}') + '។ ដោយ ' + M('\overset{\frown}{AB} = \overset{\frown}{CD}') + ' នាំឱ្យ ' + M('\overset{\frown}{AC} = \overset{\frown}{BD}'), 2),
          ('គ. ធ្នូប៉ុនគ្នា ' + M('\overset{\frown}{AC} = \overset{\frown}{BD} \\Rightarrow') + ' អង្កត់ធ្នូ ' + M('AC = BD'), 2)])

    W('hard', 'wr_chords_distance_diff_side',
      'រង្វង់ផ្ចិត ' + M('O') + ' មានកាំ ' + M('r = 15\\ \\text{cm}') + '។ អង្កត់ធ្នូពីរស្របគ្នា ' + M('AB = 24\\ \\text{cm}') + ' និង ' + M('CD = 18\\ \\text{cm}') + ' ស្ថិតនៅសងខាងនៃផ្ចិត ' + M('O') + '។\n'
      'ក. គណនាចម្ងាយ ' + M('d_1') + ' ពីផ្ចិត ' + M('O') + ' ទៅអង្កត់ធ្នូ ' + M('AB') + '។\n'
      'ខ. គណនាចម្ងាយ ' + M('d_2') + ' ពីផ្ចិត ' + M('O') + ' ទៅអង្កត់ធ្នូ ' + M('CD') + '។\n'
      'គ. គណនាចម្ងាយរវាងអង្កត់ធ្នូទាំងពីរ ' + M('AB') + ' និង ' + M('CD') + '។', [
          ('ក. ' + M('AH = \\dfrac{24}{2} = 12\\ \\text{cm} \\Rightarrow d_1 = \sqrt{15^2 - 12^2} = \sqrt{225 - 144} = 9\\ \\text{cm}'), 2),
          ('ខ. ' + M('CK = \\dfrac{18}{2} = 9\\ \\text{cm} \\Rightarrow d_2 = \sqrt{15^2 - 9^2} = \sqrt{225 - 81} = 12\\ \\text{cm}'), 2),
          ('គ. ចម្ងាយរវាងអង្កត់ធ្នូទាំងពីរ (សងខាងផ្ចិត) ៖ ' + M('d = d_1 + d_2 = 9 + 12 = 21\\ \\text{cm}'), 1)])

    # ==========================================
    # 8. WRITING PISA (5 target, 5 pts total each)
    # ==========================================
    W('pisa', 'wr_pisa_bicycle_travel',
      'កង់កង់ប្រណាំងមួយមានកាំ ' + M('r = 35\\ \\text{cm}') + '។\n'
      'ក. គណនាបរិមាត្រនៃកង់កង់គិតជាម៉ែត្រ (យក ' + M('\pi \approx \\dfrac{22}{7}') + ')។\n'
      'ខ. បើសិស្សម្នាក់ជិះកង់នោះបាន ៥០០ ជុំ តើគាត់ធ្វើដំណើរបានចម្ងាយប៉ុន្មានម៉ែត្រ?\n'
      'គ. បើគាត់ត្រូវជិះចម្ងាយ ' + M('4.4\\ \\text{km}') + ' តើកង់ត្រូវវិលប៉ុន្មានជុំ?', [
          ('ក. បរិមាត្រកង់ ៖ ' + M('P = 2\pi r = 2 \\times \\dfrac{22}{7} \\times 35 = 220\\ \\text{cm} = 2.2\\ \\text{m}'), 2),
          ('ខ. ចម្ងាយធ្វើដំណើរ ៥០០ ជុំ ៖ ' + M('2.2 \\times 500 = 1100\\ \\text{m}'), 1),
          ('គ. ចំនួនជុំសម្រាប់ ' + M('4.4\\ \\text{km} = 4400\\ \\text{m}') + ' ៖ ' + M('N = \\dfrac{4400}{2.2} = 2000\\ \\text{ជុំ}'), 2)])

    W('pisa', 'wr_pisa_clock_hands',
      'នាឡិកាជញ្ជាំងមូលមួយមានកាំ ' + M('r = 21\\ \\text{cm}') + '។ មុខនាឡិកាត្រូវបានបែងចែកជា ១២ ម៉ោងស្មើៗគ្នា។\n'
      'ក. គណនាមុំផ្ចិតដែលបង្កើតឡើងដោយចន្លោះម៉ោងនីមួយៗ (១ ម៉ោង)។\n'
      'ខ. នៅម៉ោង ៤:០០ គត់ តើមុំផ្ចិតតូចរវាងទ្រនិចម៉ោងនិងទ្រនិចនាទីស្មើនឹងប៉ុន្មានដឺក្រេ?\n'
      'គ. គណនាប្រវែងធ្នូតូចនៅលើគែមនាឡិកាដែលស្កាត់ដោយមុំនៅម៉ោង ៤:០០ (យក ' + M('\pi \approx \\dfrac{22}{7}') + ')។', [
          ('ក. មុំចន្លោះ ១ ម៉ោង ៖ ' + M('\\dfrac{360^\circ}{12} = 30^\circ'), 1),
          ('ខ. នៅម៉ោង ៤:០០ គត់ មាន ៤ ចន្លោះ ៖ ' + M('\alpha = 4 \\times 30^\circ = 120^\circ'), 2),
          ('គ. ប្រវែងធ្នូស្កាត់ ៖ ' + M('L = \\dfrac{2 \\times \\frac{22}{7} \\times 21 \\times 120}{360} = \\dfrac{132 \\times 1}{3} = 44\\ \\text{cm}'), 2)])

    W('pisa', 'wr_pisa_pizza_sharing',
      'នំប៉ីហ្សាមូលធំមួយមានអង្កត់ផ្ចិត ' + M('40\\ \\text{cm}') + ' ត្រូវបានកាត់ជា ៨ ចំណែកស្មើៗគ្នាសម្រាប់មនុស្ស ៨ នាក់។\n'
      'ក. គណនាកាំ ' + M('r') + ' និងមុំផ្ចិតនៃចំណែកនីមួយៗ។\n'
      'ខ. គណនាផ្ទៃក្រឡានៃនំប៉ីហ្សាទាំងមូល (យក ' + M('\pi \approx 3.14') + ')។\n'
      'គ. គណនាផ្ទៃក្រឡានៃនំប៉ីហ្សាមួយចំណែកដែលមនុស្សម្នាក់ទទួលបាន។', [
          ('ក. កាំ ' + M('r = \\dfrac{40}{2} = 20\\ \\text{cm}') + '; មុំផ្ចិត ៖ ' + M('\\dfrac{360^\circ}{8} = 45^\circ'), 2),
          ('ខ. ផ្ទៃសរុប ៖ ' + M('S = \pi r^2 = 3.14 \\times 20^2 = 3.14 \\times 400 = 1256\\ \\text{cm}^2'), 2),
          ('គ. ផ្ទៃមួយចំណែក ៖ ' + M('S_1 = \\dfrac{1256}{8} = 157\\ \\text{cm}^2'), 1)])

    W('pisa', 'wr_pisa_circular_track',
      'ផ្លូវរត់ប្រណាំងរាងជារង្វង់មួយមានកាំខាងក្នុង ' + M('r_1 = 30\\ \\text{m}') + ' និងកាំខាងក្រៅ ' + M('r_2 = 35\\ \\text{m}') + '។\n'
      'ក. គណនាប្រវែងមួយជុំនៃគន្លងខាងក្នុង (យក ' + M('\pi \approx 3.14') + ')។\n'
      'ខ. គណនាប្រវែងមួយជុំនៃគន្លងខាងក្រៅ។\n'
      'គ. បើកីឡាករពីរនាក់រត់មួយជុំ តើអ្នករត់គន្លងក្រៅរត់ឆ្ងាយជាងអ្នករត់គន្លងក្នុងប៉ុន្មានម៉ែត្រ?', [
          ('ក. គន្លងក្នុង ៖ ' + M('P_1 = 2 \\times 3.14 \\times 30 = 188.4\\ \\text{m}'), 2),
          ('ខ. គន្លងក្រៅ ៖ ' + M('P_2 = 2 \\times 3.14 \\times 35 = 219.8\\ \\text{m}'), 2),
          ('គ. ចម្ងាយខុសគ្នា ៖ ' + M('219.8 - 188.4 = 31.4\\ \\text{m}'), 1)])

    W('pisa', 'wr_pisa_circular_table',
      'តុបាយមូលមួយមានអង្កត់ផ្ចិត ' + M('1.4\\ \\text{m}') + '។ គេចង់កាត់កញ្ចក់មូលមួយផ្ទាំងដាក់ពីលើឱ្យល្មមស្មើនឹងមាត់តុ។\n'
      'ក. គណនាកាំ និងផ្ទៃក្រឡានៃកញ្ចក់មូលនោះ (យក ' + M('\pi \approx \\dfrac{22}{7}') + ')។\n'
      'ខ. គេចង់ដេរកម្រាលតុក្រណាត់ដែលមានគែមធ្លាក់ចុះ ' + M('0.2\\ \\text{m}') + ' ជុំវិញមាត់តុ។ រកអង្កត់ផ្ចិតនៃកម្រាលតុក្រណាត់។\n'
      'គ. គណនាផ្ទៃក្រឡានៃកម្រាលតុក្រណាត់នោះ។', [
          ('ក. កាំ ' + M('r = 0.7\\ \\text{m}') + '; ផ្ទៃកញ្ចក់ ៖ ' + M('S = \\dfrac{22}{7} \\times 0.7^2 = \\dfrac{22}{7} \\times 0.49 = 1.54\\ \\text{m}^2'), 2),
          ('ខ. អង្កត់ផ្ចិតកម្រាលក្រណាត់ ៖ ' + M('D = 1.4 + 2(0.2) = 1.8\\ \\text{m} \\Rightarrow R = 0.9\\ \\text{m}'), 1),
          ('គ. ផ្ទៃកម្រាលក្រណាត់ ៖ ' + M('S_{\\text{ក្រណាត់}} = 3.14 \\times 0.9^2 = 3.14 \\times 0.81 \approx 2.54\\ \\text{m}^2'), 2)])

    return C
