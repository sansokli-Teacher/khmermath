"""G11 Lesson 3 — ស្វ៊ីតធរណីមាត្រ (geometric sequences)."""
from lib import M, mcq, wr

LESSON = 'ស្វ៊ីតធរណីមាត្រ'
CHAPTER = 'ជំពូកទី 1 : ស្វ៊ីតនិងអនុមានរួមគណិតវិទ្យា'


def with_img(q, svg):
    q['img'] = svg
    return q


def writing(level, sec, stem, steps):
    return wr(level, sec, stem, steps)


FIG_GP_RATIO = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 520 140' width='520' height='140'>
  <circle cx='50' cy='62' r='22' fill='#dbeafe' stroke='#1e40af' stroke-width='1.6'/>
  <text x='50' y='68' text-anchor='middle' font-family='Times New Roman, serif' font-size='18' fill='#1e40af'>2</text>
  <path d='M 78 62 L 118 62' stroke='#dc2626' stroke-width='1.8' marker-end='url(#arr)'/>
  <text x='98' y='50' text-anchor='middle' font-family='Times New Roman, serif' font-size='13' fill='#dc2626'>×3</text>
  <circle cx='148' cy='62' r='22' fill='#dbeafe' stroke='#1e40af' stroke-width='1.6'/>
  <text x='148' y='68' text-anchor='middle' font-family='Times New Roman, serif' font-size='18' fill='#1e40af'>6</text>
  <path d='M 176 62 L 216 62' stroke='#dc2626' stroke-width='1.8' marker-end='url(#arr)'/>
  <text x='196' y='50' text-anchor='middle' font-family='Times New Roman, serif' font-size='13' fill='#dc2626'>×3</text>
  <circle cx='246' cy='62' r='22' fill='#dbeafe' stroke='#1e40af' stroke-width='1.6'/>
  <text x='246' y='68' text-anchor='middle' font-family='Times New Roman, serif' font-size='18' fill='#1e40af'>18</text>
  <path d='M 274 62 L 314 62' stroke='#dc2626' stroke-width='1.8' marker-end='url(#arr)'/>
  <text x='294' y='50' text-anchor='middle' font-family='Times New Roman, serif' font-size='13' fill='#dc2626'>×3</text>
  <circle cx='344' cy='62' r='22' fill='#dbeafe' stroke='#1e40af' stroke-width='1.6'/>
  <text x='344' y='68' text-anchor='middle' font-family='Times New Roman, serif' font-size='18' fill='#1e40af'>54</text>
  <path d='M 372 62 L 412 62' stroke='#dc2626' stroke-width='1.8' marker-end='url(#arr)'/>
  <text x='392' y='50' text-anchor='middle' font-family='Times New Roman, serif' font-size='13' fill='#dc2626'>×3</text>
  <circle cx='442' cy='62' r='22' fill='#dbeafe' stroke='#1e40af' stroke-width='1.6'/>
  <text x='442' y='68' text-anchor='middle' font-family='Times New Roman, serif' font-size='18' fill='#1e40af'>162</text>
  <defs><marker id='arr' markerWidth='8' markerHeight='8' refX='7' refY='4' orient='auto'><polygon points='0,0 8,4 0,8' fill='#dc2626'/></marker></defs>
  <text x='260' y='118' text-anchor='middle' font-family='Times New Roman, serif' font-size='13' fill='#334155'>ស្វ៊ីតធរណីមាត្រ ៖ សមាមាត្ររួម <tspan font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic'>q</tspan> = 3</text>
</svg>"""

FIG_EQUIDISTANT = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 520 150' width='520' height='150'>
  <text x='260' y='28' text-anchor='middle' font-family='Times New Roman, serif' font-size='14' fill='#334155'>ពាក្យស្មើចម្ងាយពីចុងស្វ៊ីត ៖ ផលគុណស្មើគ្នា</text>
  <rect x='30' y='48' width='70' height='42' rx='6' fill='#dbeafe' stroke='#1e40af' stroke-width='1.5'/>
  <text x='65' y='75' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='16' fill='#1e40af'>a<tspan font-size='11' dy='3'>1</tspan></text>
  <rect x='130' y='48' width='70' height='42' rx='6' fill='#e0e7ff' stroke='#4338ca' stroke-width='1.5'/>
  <text x='165' y='75' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='16' fill='#4338ca'>a<tspan font-size='11' dy='3'>p</tspan></text>
  <text x='230' y='75' text-anchor='middle' font-family='Times New Roman, serif' font-size='18' fill='#64748b'>⋯</text>
  <rect x='260' y='48' width='90' height='42' rx='6' fill='#e0e7ff' stroke='#4338ca' stroke-width='1.5'/>
  <text x='305' y='75' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='15' fill='#4338ca'>a<tspan font-size='11' dy='3'>n−p+1</tspan></text>
  <rect x='380' y='48' width='70' height='42' rx='6' fill='#dbeafe' stroke='#1e40af' stroke-width='1.5'/>
  <text x='415' y='75' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='16' fill='#1e40af'>a<tspan font-size='11' dy='3'>n</tspan></text>
  <text x='260' y='128' text-anchor='middle' font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic' font-size='16' fill='#b91c1c'>a<tspan font-size='11' dy='3'>p</tspan><tspan dy='-3'> · a</tspan><tspan font-size='11' dy='3'>n−p+1</tspan><tspan dy='-3'> = a</tspan><tspan font-size='11' dy='3'>1</tspan><tspan dy='-3'> · a</tspan><tspan font-size='11' dy='3'>n</tspan></text>
</svg>"""

FIG_CHESS = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 280 280' width='280' height='280'>
  <rect x='24' y='24' width='232' height='232' fill='none' stroke='#1e293b' stroke-width='2'/>
  <g fill='#1e293b'>
    <rect x='53' y='24' width='29' height='29'/>
    <rect x='111' y='24' width='29' height='29'/>
    <rect x='169' y='24' width='29' height='29'/>
    <rect x='227' y='24' width='29' height='29'/>
    <rect x='24' y='53' width='29' height='29'/>
    <rect x='82' y='53' width='29' height='29'/>
    <rect x='140' y='53' width='29' height='29'/>
    <rect x='198' y='53' width='29' height='29'/>
    <rect x='53' y='82' width='29' height='29'/>
    <rect x='111' y='82' width='29' height='29'/>
    <rect x='169' y='82' width='29' height='29'/>
    <rect x='227' y='82' width='29' height='29'/>
    <rect x='24' y='111' width='29' height='29'/>
    <rect x='82' y='111' width='29' height='29'/>
    <rect x='140' y='111' width='29' height='29'/>
    <rect x='198' y='111' width='29' height='29'/>
    <rect x='53' y='140' width='29' height='29'/>
    <rect x='111' y='140' width='29' height='29'/>
    <rect x='169' y='140' width='29' height='29'/>
    <rect x='227' y='140' width='29' height='29'/>
    <rect x='24' y='169' width='29' height='29'/>
    <rect x='82' y='169' width='29' height='29'/>
    <rect x='140' y='169' width='29' height='29'/>
    <rect x='198' y='169' width='29' height='29'/>
    <rect x='53' y='198' width='29' height='29'/>
    <rect x='111' y='198' width='29' height='29'/>
    <rect x='169' y='198' width='29' height='29'/>
    <rect x='227' y='198' width='29' height='29'/>
    <rect x='24' y='227' width='29' height='29'/>
    <rect x='82' y='227' width='29' height='29'/>
    <rect x='140' y='227' width='29' height='29'/>
    <rect x='198' y='227' width='29' height='29'/>
  </g>
  <text x='38' y='44' font-family='Times New Roman, serif' font-size='11' fill='#b91c1c'>1</text>
  <text x='67' y='44' font-family='Times New Roman, serif' font-size='11' fill='#f8fafc'>2</text>
  <text x='96' y='44' font-family='Times New Roman, serif' font-size='11' fill='#b91c1c'>4</text>
  <text x='125' y='44' font-family='Times New Roman, serif' font-size='11' fill='#f8fafc'>8</text>
  <text x='140' y='268' text-anchor='middle' font-family='Times New Roman, serif' font-size='12' fill='#334155'>៦៤ ប្រឡោះ ៖ ១, ២, ៤, …, ២<tspan baseline-shift='super' font-size='9'>៦៣</tspan></text>
</svg>"""

FIG_PENDULUM = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 420 220' width='420' height='220'>
  <circle cx='210' cy='28' r='6' fill='#1e293b'/>
  <path d='M 210 28 L 80 170' stroke='#334155' stroke-width='1.6'/>
  <path d='M 210 28 L 210 178' stroke='#94a3b8' stroke-width='1.2' stroke-dasharray='4,3'/>
  <path d='M 210 28 L 340 170' stroke='#334155' stroke-width='1.6'/>
  <path d='M 80 170 A 175 175 0 0 0 340 170' fill='none' stroke='#2563eb' stroke-width='1.8'/>
  <circle cx='80' cy='170' r='10' fill='#ef4444' stroke='#b91c1c' stroke-width='1.4'/>
  <circle cx='340' cy='170' r='10' fill='#ef4444' stroke='#b91c1c' stroke-width='1.4'/>
  <line x1='80' y1='188' x2='210' y2='188' stroke='#dc2626' stroke-width='1.4'/>
  <text x='145' y='208' text-anchor='middle' font-family='Times New Roman, serif' font-size='13' fill='#dc2626'>18 cm</text>
  <text x='210' y='18' text-anchor='middle' font-family='Times New Roman, serif' font-size='12' fill='#334155'>ប៉ោលយោល ៖ ទំហំកាត់ 5% រាល់លើក</text>
</svg>"""

FIG_BOUNCE = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 480 200' width='480' height='200'>
  <line x1='20' y1='178' x2='460' y2='178' stroke='#334155' stroke-width='2.4'/>
  <circle cx='60' cy='28' r='9' fill='#ef4444' stroke='#b91c1c' stroke-width='1.4'/>
  <path d='M 60 37 L 60 169' stroke='#ef4444' stroke-width='1.5' stroke-dasharray='4,3'/>
  <text x='72' y='36' font-family='Times New Roman, serif' font-size='12' fill='#b91c1c'>24 dm</text>
  <path d='M 60 169 Q 130 40 200 169' fill='none' stroke='#2563eb' stroke-width='1.8'/>
  <path d='M 200 169 Q 250 70 300 169' fill='none' stroke='#0284c7' stroke-width='1.6'/>
  <path d='M 300 169 Q 335 100 370 169' fill='none' stroke='#0891b2' stroke-width='1.5'/>
  <path d='M 370 169 Q 395 125 420 169' fill='none' stroke='#0e7490' stroke-width='1.4'/>
  <text x='240' y='22' text-anchor='middle' font-family='Times New Roman, serif' font-size='13' fill='#334155'>ប៉ោល ៖ ធ្នូដំបូង 24 dm, q = 0.8</text>
</svg>"""


def cands():
    C = []

    # ----- MCQ easy -----
    C.append(mcq(
        'easy', 'sec1_def',
        'ស្វ៊ីតចំនួនពិតមួយជាស្វ៊ីតធរណីមាត្រ នៅពេលដែលមានចំនួនពិត ' + M(r'q') + ' មិនសូន្យ ដែលគ្រប់ពាក្យបន្ទាប់គឺស្មើនឹងពាក្យមុនគុណនឹង ៖',
        M(r'q'),
        [M(r'd'), M(r'q+d'), M(r'n')],
        'តាមនិយមន័យ ស្វ៊ីតធរណីមាត្រមានសមាមាត្ររួម ' + M(r'q') + ' ដែល ' + M(r'a_{n+1}=a_n q') + '។'
    ))
    C.append(with_img(mcq(
        'easy', 'sec1_def',
        'សមាមាត្ររួមនៃស្វ៊ីត ' + M(r'2,6,18,54,162,\ldots') + ' គឺ ៖',
        M(r'3'),
        [M(r'2'), M(r'4'), M(r'6')],
        M(r'q=a_{n+1}/a_n=6/2=3') + '។ ពាក្យបន្ទាប់គុណនឹង ៣ ដដែល។'
    ), FIG_GP_RATIO))
    C.append(mcq(
        'easy', 'sec1_ratio',
        'ប្រសិនបើ ' + M(r'(a_n)') + ' ជាស្វ៊ីតធរណីមាត្រ នោះសមាមាត្ររួមគឺ ៖',
        M(r'q=\dfrac{a_{n+1}}{a_n}'),
        [
            M(r'q=a_{n+1}-a_n'),
            M(r'q=\dfrac{a_n}{a_{n+1}}'),
            M(r'q=a_n a_{n+1}')
        ],
        'សមាមាត្ររួមជាផលធ្លាក់នៃពាក្យបន្ទាប់ចែកពាក្យមុន។'
    ))
    C.append(mcq(
        'easy', 'sec2_term',
        'ពាក្យទូទៅនៃស្វ៊ីតធរណីមាត្រដែលមានពាក្យទី១ ' + M(r'a_1') + ' និងសមាមាត្ររួម ' + M(r'q') + ' គឺ ៖',
        M(r'a_n=a_1 q^{n-1}'),
        [
            M(r'a_n=a_1+(n-1)q'),
            M(r'a_n=a_1 q^n'),
            M(r'a_n=a_1+(n)q')
        ],
        'ពាក្យទី ' + M(r'n') + ' បានមកពីគុណ ' + M(r'a_1') + ' នឹង ' + M(r'q') + ' ចំនួន ' + M(r'n-1') + ' ដង។'
    ))
    C.append(mcq(
        'easy', 'sec2_term',
        'ស្វ៊ីត ' + M(r'6,12,24,48,\ldots') + ' មានសមាមាត្ររួម ៖',
        M(r'2'),
        [M(r'6'), M(r'12'), M(r'1/2')],
        M(r'12/6=24/12=2') + '។'
    ))
    C.append(mcq(
        'easy', 'sec2_term',
        'ពាក្យទូទៅនៃស្វ៊ីត ' + M(r'3,12,48,192,\ldots') + ' គឺ ៖',
        M(r'a_n=3\cdot 4^{n-1}'),
        [
            M(r'a_n=3\cdot 4^n'),
            M(r'a_n=3+(n-1)4'),
            M(r'a_n=4\cdot 3^{n-1}')
        ],
        M(r'q=12/3=4') + ' ដូច្នេះ ' + M(r'a_n=3\cdot 4^{n-1}') + '។'
    ))
    C.append(mcq(
        'easy', 'sec3_mean',
        'មធ្យមធរណីមាត្រនៃចំនួនវិជ្ជមាន ' + M(r'4') + ' និង ' + M(r'9') + ' គឺ ៖',
        M(r'6'),
        [M(r'6.5'), M(r'13'), M(r'36')],
        M(r'\sqrt{4\cdot 9}=\sqrt{36}=6') + '។'
    ))
    C.append(mcq(
        'easy', 'sec4_sum',
        'ផលបូក ' + M(r'1+2+4+8+16+32+64') + ' ស្មើនឹង ៖',
        M(r'127'),
        [M(r'64'), M(r'128'), M(r'63')],
        M(r'S_n=a_1(q^n-1)/(q-1)=1(2^7-1)/(2-1)=127') + '។'
    ))
    C.append(mcq(
        'easy', 'sec5_inf',
        'ស្វ៊ីតធរណីមាត្រមានផលបូកអនន្ត នៅពេល ៖',
        M(r'|q|<1'),
        [M(r'|q|>1'), M(r'q=1'), M(r'q=-1')],
        'លក្ខខណ្ឌរួមគ្នានៃផលបូកអនន្តគឺ ' + M(r'|q|<1') + '។'
    ))
    C.append(mcq(
        'easy', 'sec5_inf',
        'បើ ' + M(r'|q|<1') + ' ផលបូកអនន្តនៃស្វ៊ីតធរណីមាត្រគឺ ៖',
        M(r'S_\infty=\dfrac{a_1}{1-q}'),
        [
            M(r'S_\infty=a_1(1-q)'),
            M(r'S_\infty=\dfrac{a_1}{q-1}'),
            M(r'S_\infty=a_1 q')
        ],
        'រូបមន្តស្តង់ដារ ' + M(r'S_\infty=a_1/(1-q)') + ' នៅពេល ' + M(r'|q|<1') + '។'
    ))
    C.append(mcq(
        'easy', 'sec1_def',
        'ក្នុងស្វ៊ីតនព្វន្តភាព ភាពខុសគ្នារវាងពាក្យបន្ទាប់គ្នាថេរ។ ក្នុងស្វ៊ីតធរណីមាត្រ អ្វីដែលថេរគឺ ៖',
        'ផលធ្លាក់នៃពាក្យបន្ទាប់ចែកពាក្យមុន',
        ['ផលបូកនៃពាក្យបន្ទាប់គ្នា', 'ភាពខុសគ្នានៃពាក្យបន្ទាប់គ្នា', 'ផលបូកនៃពាក្យទី១ និងពាក្យចុង'],
        'ស្វ៊ីតធរណីមាត្រមានសមាមាត្ររួមថេរ ' + M(r'q=a_{n+1}/a_n') + '។'
    ))
    C.append(mcq(
        'easy', 'sec4_sum',
        'រូបមន្តផលបូក ' + M(r'n') + ' ពាក្យដំបូងនៃស្វ៊ីតធរណីមាត្រ (' + M(r'q\neq 1') + ') គឺ ៖',
        M(r'S_n=\dfrac{a_1(q^n-1)}{q-1}'),
        [
            M(r'S_n=\dfrac{n}{2}(2a_1+(n-1)q)'),
            M(r'S_n=a_1 q^n'),
            M(r'S_n=n a_1 q')
        ],
        'នេះជារូបមន្តស្តង់ដារនៃផលបូកស្វ៊ីតធរណីមាត្រ។'
    ))

    # ----- MCQ medium -----
    C.append(mcq(
        'medium', 'sec2_term',
        'ក្នុងស្វ៊ីត ' + M(r'6,12,24,48,\ldots') + ' ពាក្យទី ១៤ គឺ ៖',
        M(r'49152'),
        [M(r'24576'), M(r'98304'), M(r'12288')],
        M(r'a_{14}=6\cdot 2^{13}=6\cdot 8192=49152') + '។'
    ))
    C.append(mcq(
        'medium', 'sec2_term',
        'ក្នុងស្វ៊ីត ' + M(r'6,12,24,48,\ldots') + ' ពាក្យ ' + M(r'384') + ' ជាពាក្យទី ៖',
        M(r'7'),
        [M(r'6'), M(r'8'), M(r'9')],
        M(r'6\cdot 2^{n-1}=384\Rightarrow 2^{n-1}=64=2^6\Rightarrow n=7') + '។'
    ))
    C.append(mcq(
        'medium', 'sec2_term',
        'ក្នុងស្វ៊ីត ' + M(r'3,12,48,192,\ldots') + ' ពាក្យទី ៩ គឺ ៖',
        M(r'196608'),
        [M(r'49152'), M(r'65536'), M(r'786432')],
        M(r'a_9=3\cdot 4^{8}=3\cdot 65536=196608') + '។'
    ))
    C.append(mcq(
        'medium', 'sec2_term',
        'ក្នុងស្វ៊ីត ' + M(r'3,12,48,192,\ldots') + ' ពាក្យ ' + M(r'12288') + ' ជាពាក្យទី ៖',
        M(r'7'),
        [M(r'5'), M(r'6'), M(r'8')],
        M(r'3\cdot 4^{n-1}=12288\Rightarrow 4^{n-1}=4096=4^6\Rightarrow n=7') + '។'
    ))
    C.append(mcq(
        'medium', 'sec3_insert',
        'ត្រូវបន្ថែមចំនួន ' + M(r'x') + ' លើពាក្យនីមួយនៃ ' + M(r'3,24,94') + ' ដើម្បីបានស្វ៊ីតធរណីមាត្រ។ តម្លៃ ' + M(r'x') + ' គឺ ៖',
        M(r'6'),
        [M(r'3'), M(r'4'), M(r'8')],
        M(r'(24+x)^2=(3+x)(94+x)\Rightarrow 294=49x\Rightarrow x=6') + '។'
    ))
    C.append(mcq(
        'medium', 'sec2_term',
        'ស្វ៊ីតធរណីមាត្រមួយមាន ' + M(r'a_3=4') + ' និង ' + M(r'a_5=36') + '។ សមាមាត្ររួមអាចជា ៖',
        M(r'\pm 3'),
        [M(r'\pm 2'), M(r'\pm 6'), M(r'\pm 9')],
        M(r'a_5/a_3=q^2=9\Rightarrow q=\pm 3') + '។'
    ))
    C.append(mcq(
        'medium', 'sec2_term',
        'បើ ' + M(r'a_3=4') + ' និង ' + M(r'a_5=36') + ' ក្នុងស្វ៊ីតធរណីមាត្រ នោះ ' + M(r'a_1') + ' គឺ ៖',
        M(r'\dfrac{4}{9}'),
        [M(r'4'), M(r'\dfrac{4}{3}'), M(r'12')],
        M(r'a_1=a_3/q^2=4/9') + ' សម្រាប់ទាំង ' + M(r'q=3') + ' និង ' + M(r'q=-3') + '។'
    ))
    C.append(mcq(
        'medium', 'sec4_sum',
        'ផលបូក ' + M(r'7') + ' ពាក្យដំបូងនៃ ' + M(r'5+10+20+\cdots') + ' គឺ ៖',
        M(r'635'),
        [M(r'320'), M(r'640'), M(r'315')],
        M(r'S_7=5(2^7-1)/(2-1)=5\cdot 127=635') + '។'
    ))
    C.append(mcq(
        'medium', 'sec4_sum',
        'ផលបូក ' + M(r'2+6+18+\cdots+1458') + ' គឺ ៖',
        M(r'2186'),
        [M(r'1458'), M(r'2187'), M(r'1093')],
        M(r'a_n=2\cdot 3^{n-1}=1458\Rightarrow 3^{n-1}=729=3^6\Rightarrow n=7') +
        '។ ' + M(r'S_7=2(3^7-1)/(3-1)=2187-1=2186') + '។'
    ))
    C.append(mcq(
        'medium', 'sec2_term',
        'ក្នុងស្វ៊ីត ' + M(r'6,3,1.5,\ldots') + ' ពាក្យទី ៧ គឺ ៖',
        M(r'\dfrac{3}{32}'),
        [M(r'\dfrac{3}{16}'), M(r'\dfrac{3}{64}'), M(r'\dfrac{6}{32}')],
        M(r'a_7=6\cdot(1/2)^6=6/64=3/32') + '។'
    ))
    C.append(mcq(
        'medium', 'sec4_sum',
        'ផលបូក ' + M(r'7') + ' ពាក្យដំបូងនៃ ' + M(r'6+3+1.5+\cdots') + ' គឺ ៖',
        M(r'\dfrac{381}{32}'),
        [M(r'\dfrac{381}{16}'), M(r'\dfrac{63}{8}'), M(r'12')],
        M(r'S_7=6\bigl((1/2)^7-1\bigr)/(1/2-1)=381/32') + '។'
    ))
    C.append(mcq(
        'medium', 'sec5_inf',
        'ផលបូកអនន្ត ' + M(r'6+2+\dfrac{2}{3}+\dfrac{2}{9}+\cdots') + ' ស្មើនឹង ៖',
        M(r'9'),
        [M(r'8'), M(r'12'), M(r'6')],
        M(r'a_1=6') + ', ' + M(r'q=1/3') + '។ ' + M(r'S_\infty=6/(1-1/3)=9') + '។'
    ))
    C.append(mcq(
        'medium', 'sec5_inf',
        'ផលបូកអនន្ត ' + M(r'16+12+9+\cdots') + ' គឺ ៖',
        M(r'64'),
        [M(r'48'), M(r'36'), M(r'32')],
        M(r'q=12/16=3/4') + ' ហើយ ' + M(r'S_\infty=16/(1-3/4)=64') + '។'
    ))
    C.append(mcq(
        'medium', 'sec5_inf',
        'ប្រភាគទសភាគ ' + M(r'0.\overline{235}') + ' ស្មើនឹង ៖',
        M(r'\dfrac{235}{999}'),
        [M(r'\dfrac{235}{1000}'), M(r'\dfrac{235}{99}'), M(r'\dfrac{23}{99}')],
        M(r'0.\overline{235}=235/10^3+235/10^6+\cdots=(235/1000)/(1-1/1000)=235/999') + '។'
    ))
    C.append(mcq(
        'medium', 'sec5_inf',
        'ប្រភាគទសភាគ ' + M(r'4.\overline{57}') + ' ស្មើនឹង ៖',
        M(r'\dfrac{453}{99}'),
        [M(r'\dfrac{457}{99}'), M(r'\dfrac{57}{99}'), M(r'\dfrac{4}{57}')],
        M(r'4.\overline{57}=4+57/99=396/99+57/99=453/99') + '។'
    ))
    C.append(with_img(mcq(
        'medium', 'sec3_mean',
        'ក្នុងស្វ៊ីតធរណីមាត្រមាន ' + M(r'n') + ' ពាក្យ ផលគុណនៃពាក្យស្មើចម្ងាយពីចុងស្វ៊ីតស្មើនឹង ៖',
        M(r'a_1 a_n'),
        [M(r'a_1+a_n'), M(r'a_n/a_1'), M(r'n a_1')],
        M(r'a_p a_{n-p+1}=a_1 a_n') + '។'
    ), FIG_EQUIDISTANT))
    C.append(mcq(
        'medium', 'sec4_sum',
        'បើ ' + M(r'q=1') + ' នោះផលបូក ' + M(r'n') + ' ពាក្យដំបូងនៃស្វ៊ីតធរណីមាត្រគឺ ៖',
        M(r'S_n=n a_1'),
        [M(r'S_n=a_1'), M(r'S_n=a_1(q^n-1)'), M(r'S_n=0')],
        'ពេល ' + M(r'q=1') + ' ពាក្យទាំងអស់ស្មើ ' + M(r'a_1') + ' ដូច្នេះ ' + M(r'S_n=n a_1') + '។'
    ))

    # ----- MCQ hard -----
    C.append(mcq(
        'hard', 'sec2_term',
        'ក្នុងស្វ៊ីត ' + M(r'1,2,4,8,\ldots') + ' ពាក្យ ' + M(r'8192') + ' ជាពាក្យទី ៖',
        M(r'14'),
        [M(r'12'), M(r'13'), M(r'15')],
        M(r'2^{n-1}=8192=2^{13}\Rightarrow n=14') + '។'
    ))
    C.append(mcq(
        'hard', 'sec2_term',
        'ក្នុងស្វ៊ីត ' + M(r'20,10,5,\ldots') + ' ពាក្យ ' + M(r'5/256') + ' ជាពាក្យទី ៖',
        M(r'12'),
        [M(r'8'), M(r'10'), M(r'16')],
        M(r'20\cdot(1/2)^{n-1}=5/256\Rightarrow 2^{4-n}=2^{-8}\Rightarrow n=12') + '។'
    ))
    C.append(mcq(
        'hard', 'sec2_term',
        'ស្វ៊ីតធរណីមាត្រមាន ' + M(r'a_3=18') + ' និង ' + M(r'a_7=1458') + ' (' + M(r'q>0') + ')។ ពាក្យទី ១០ គឺ ៖',
        M(r'39366'),
        [M(r'13122'), M(r'4374'), M(r'19683')],
        M(r'q^4=1458/18=81\Rightarrow q=3') + '។ ' + M(r'a_1=18/9=2') +
        '។ ' + M(r'a_{10}=2\cdot 3^9=39366') + '។'
    ))
    C.append(mcq(
        'hard', 'sec2_term',
        'ស្វ៊ីតធរណីមាត្រមាន ' + M(r'a_3=20') + ' និង ' + M(r'a_6=1280') + ' (' + M(r'q>0') + ')។ ពាក្យទី១ គឺ ៖',
        M(r'\dfrac{5}{4}'),
        [M(r'5'), M(r'4'), M(r'\dfrac{5}{16}')],
        M(r'q^3=1280/20=64\Rightarrow q=4') + '។ ' + M(r'a_1=20/16=5/4') + '។'
    ))
    C.append(mcq(
        'hard', 'sec4_sum',
        'ស្វ៊ីតធរណីមាត្រមាន ' + M(r'a_1=3') + ' និង ' + M(r'S_3=21') + ' (' + M(r'q>0') + ')។ ផលបូក ' + M(r'S_7') + ' គឺ ៖',
        M(r'381'),
        [M(r'255'), M(r'192'), M(r'765')],
        M(r'(q^2+q+1)=7\Rightarrow q=2') + '។ ' + M(r'S_7=3(2^7-1)=381') + '។'
    ))
    C.append(mcq(
        'hard', 'sec4_sum',
        'ផលបូក ' + M(r'48+24+12+\cdots+3/8') + ' គឺ ៖',
        M(r'\dfrac{765}{8}'),
        [M(r'96'), M(r'\dfrac{381}{4}'), M(r'48')],
        M(r'n=8') + ' និង ' + M(r'S_8=48\bigl(1-(1/2)^8\bigr)/(1/2)=765/8') + '។'
    ))
    C.append(mcq(
        'hard', 'sec5_inf',
        'ស្វ៊ីតធរណីមាត្រមាន ' + M(r'a_2=-9') + ' និង ' + M(r'a_5=1/3') + '។ ផលបូកអនន្តគឺ ៖',
        M(r'\dfrac{81}{4}'),
        [M(r'27'), M(r'\dfrac{27}{4}'), M(r'-9')],
        M(r'q^3=-1/27\Rightarrow q=-1/3') + '។ ' + M(r'a_1=27') +
        '។ ' + M(r'S_\infty=27/(1+1/3)=81/4') + '។'
    ))
    C.append(mcq(
        'hard', 'sec5_inf',
        'បើ ' + M(r'a_1=5') + ' និង ' + M(r'S_\infty=15') + ' នោះសមាមាត្ររួមគឺ ៖',
        M(r'\dfrac{2}{3}'),
        [M(r'\dfrac{1}{3}'), M(r'\dfrac{3}{5}'), M(r'\dfrac{1}{5}')],
        M(r'5/(1-q)=15\Rightarrow 1-q=1/3\Rightarrow q=2/3') + '។'
    ))
    C.append(mcq(
        'hard', 'sec5_inf',
        'បើ ' + M(r'S_2=16') + ' និង ' + M(r'S_\infty=25') + ' (' + M(r'q>0') + ') នោះ ' + M(r'a_1') + ' គឺ ៖',
        M(r'10'),
        [M(r'8'), M(r'16'), M(r'25')],
        M(r'a_1/(1-q)=25') + ' និង ' + M(r'a_1(1+q)=16') +
        ' ឲ្យ ' + M(r'q=3/5') + ' និង ' + M(r'a_1=10') + '។'
    ))

    # ----- MCQ pisa -----
    C.append(mcq(
        'pisa', 'sec2_pop',
        'ប្រជាជនប្រទេសមួយឆ្នាំ ២០០០ មាន ២ លាននាក់ ហើយកើន ៤% រាល់ឆ្នាំ។ ចំនួនប្រជាជនឆ្នាំ ២០០៩ ជិតបំផុតនឹង ៖',
        '២.៨៥ លាននាក់',
        ['២.៧២ លាននាក់', '៣.១២ លាននាក់', '២.៤០ លាននាក់'],
        M(r'a_{10}=2\cdot(1.04)^9\approx 2.8466') + ' លាននាក់។'
    ))
    C.append(with_img(mcq(
        'pisa', 'sec4_chess',
        'លើក្តារអុក ៦៤ ប្រឡោះ ដាក់ស្រូវ ១ គ្រាប់លើប្រឡោះទី១ រួចគុណ ២ រាល់ប្រឡោះបន្ទាប់។ ចំនួនស្រូវសរុបគឺ ៖',
        M(r'2^{64}-1'),
        [M(r'2^{64}'), M(r'64\cdot 2'), M(r'2^{63}')],
        M(r'S_{64}=1(2^{64}-1)/(2-1)=2^{64}-1') + '។'
    ), FIG_CHESS))
    C.append(with_img(mcq(
        'pisa', 'sec2_pend',
        'ប៉ោលមានទំហំដំបូង ១៨ cm ហើយកាត់ចុះ ៥% រាល់លើក។ ទំហំលើកទី ១០ ជិតបំផុតនឹង ៖',
        '១១.៣ cm',
        ['១៣.៥ cm', '៩.០ cm', '១៧.១ cm'],
        M(r'a_{10}=18\cdot(0.95)^9\approx 11.34') + ' cm។'
    ), FIG_PENDULUM))
    C.append(with_img(mcq(
        'pisa', 'sec5_bounce',
        'ប៉ោលយោលដំបូងបានធ្នូ ២៤ dm រួចប្រវែងធ្នូថយ ២០% រាល់លើក។ ប្រវែងគន្លងសរុបរហូតឈប់គឺ ៖',
        M(r'120') + ' dm',
        [M(r'96') + ' dm', M(r'48') + ' dm', M(r'240') + ' dm'],
        M(r'a_1=24') + ', ' + M(r'q=0.8') + '។ ' + M(r'S_\infty=24/(1-0.8)=120') + ' dm។'
    ), FIG_BOUNCE))
    C.append(mcq(
        'pisa', 'sec2_bank',
        'ដាក់ប្រាក់ ១០០ ០០០ រៀល ផ្តល់ការប្រាក់ ៦% ក្នុងមួយឆ្នាំ (រួមប្រាក់)។ ប្រាក់សរុបក្រោយ ' + M(r'n') + ' ឆ្នាំគឺ ៖',
        M(r'100000\cdot(1.06)^n'),
        [
            M(r'100000+6000n'),
            M(r'100000\cdot(0.06)^n'),
            M(r'100000\cdot 1.06 n')
        ],
        'ការប្រាក់រួមគឺស្វ៊ីតធរណីមាត្រ ' + M(r'a_n=a_0(1+r)^n') + '។'
    ))
    C.append(mcq(
        'pisa', 'sec4_pend',
        'ប៉ោលមានទំហំ ១៨ cm កាត់ ៥% រាល់លើក។ ផលបូកទំហំ ១៥ លើកដំបូងជិតបំផុតនឹង ៖',
        '១៩៣ cm',
        ['២៧០ cm', '១២០ cm', '១៨ cm'],
        M(r'S_{15}=18(1-0.95^{15})/(1-0.95)\approx 193.2') + ' cm។'
    ))

    # ----- Writing easy -----
    C.append(writing(
        'easy', 'sec1_def',
        'និយមន័យស្វ៊ីតធរណីមាត្រ រួមនឹងរូបមន្តពាក្យទូទៅ និងផលបូក ' + M(r'n') + ' ពាក្យ។',
        [
            ('ស្វ៊ីតធរណីមាត្រមានសមាមាត្ររួមថេរ ' + M(r'q=a_{n+1}/a_n\neq 0') + '។', 1),
            ('ពាក្យទូទៅ ៖ ' + M(r'a_n=a_1 q^{n-1}') + '។', 1),
            ('ផលបូក ៖ ' + M(r'S_n=a_1(q^n-1)/(q-1)') + ' បើ ' + M(r'q\neq 1') + '។', 1),
            ('បើ ' + M(r'q=1') + ' នោះ ' + M(r'S_n=n a_1') + '។', 1),
            ('បើ ' + M(r'|q|<1') + ' មានផលបូកអនន្ត ' + M(r'S_\infty=a_1/(1-q)') + '។', 1),
        ]
    ))

    # ----- Writing medium -----
    C.append(writing(
        'medium', 'sec2_term',
        'រកពាក្យទី ១៤ និងលំដាប់នៃពាក្យ ៣៨៤ ក្នុងស្វ៊ីត ' + M(r'6,12,24,48,\ldots') + '។',
        [
            ('កំណត់ ' + M(r'q=12/6=2') + '។', 1),
            ('សរសេរ ' + M(r'a_n=6\cdot 2^{n-1}') + '។', 1),
            (M(r'a_{14}=6\cdot 2^{13}=6\cdot 8192=49152') + '។', 1),
            (M(r'6\cdot 2^{n-1}=384\Rightarrow 2^{n-1}=64=2^6') + '។', 1),
            ('ដូច្នេះ ' + M(r'n=7') + '។', 1),
        ]
    ))
    C.append(writing(
        'medium', 'sec3_insert',
        'រក ' + M(r'x') + ' ដែលបន្ថែមលើ ' + M(r'3,24,94') + ' ឲ្យបានស្វ៊ីតធរណីមាត្រ។',
        [
            ('លក្ខខណ្ឌ ៖ ' + M(r'(24+x)^2=(3+x)(94+x)') + '។', 1),
            ('ពន្លាត ៖ ' + M(r'576+48x+x^2=282+97x+x^2') + '។', 1),
            (M(r'294=49x') + '។', 1),
            (M(r'x=6') + '។', 1),
            ('ស្វ៊ីតថ្មី ៖ ' + M(r'9,30,100') + '។', 1),
        ]
    ))
    C.append(writing(
        'medium', 'sec4_sum',
        'គណនា ' + M(r'S_7') + ' នៃ ' + M(r'5+10+20+\cdots') + ' និងផលបូក ' + M(r'2+6+18+\cdots+1458') + '។',
        [
            ('ស្វ៊ីតទី១ ៖ ' + M(r'a_1=5') + ', ' + M(r'q=2') + '។', 1),
            (M(r'S_7=5(2^7-1)=635') + '។', 1),
            (M(r'2\cdot 3^{n-1}=1458\Rightarrow 3^{n-1}=729=3^6\Rightarrow n=7') + '។', 1),
            (M(r'S_7=2(3^7-1)/2=2186') + '។', 1),
            ('សន្និដ្ឋានផលបូកទាំងពីរ ៖ ៦៣៥ និង ២១៨៦។', 1),
        ]
    ))
    C.append(writing(
        'medium', 'sec5_inf',
        'បង្ហាញថា ' + M(r'0.\overline{235}=235/999') + ' ដោយប្រើផលបូកអនន្ត។',
        [
            (M(r'0.\overline{235}=235/10^3+235/10^6+\cdots') + '។', 1),
            (M(r'a_1=235/1000') + ', ' + M(r'q=1/1000') + '។', 1),
            ('ពិនិត្យ ' + M(r'|q|<1') + '។', 1),
            (M(r'S=a_1/(1-q)=(235/1000)/(999/1000)') + '។', 1),
            (M(r'S=235/999') + '។', 1),
        ]
    ))
    C.append(writing(
        'medium', 'sec2_term',
        'ស្វ៊ីតធរណីមាត្រមាន ' + M(r'a_3=4') + ' និង ' + M(r'a_5=36') + '។ រក ' + M(r'q') + ' និង ' + M(r'a_1') + '។',
        [
            (M(r'a_5/a_3=q^2=36/4=9') + '។', 1),
            (M(r'q=\pm 3') + '។', 1),
            (M(r'a_3=a_1 q^2') + '។', 1),
            (M(r'a_1=4/9') + '។', 1),
            ('ពាក្យទូទៅ ៖ ' + M(r'a_n=(4/9)(\pm 3)^{n-1}') + '។', 1),
        ]
    ))

    # ----- Writing hard -----
    C.append(writing(
        'hard', 'sec4_sum',
        'ស្វ៊ីតមាន ' + M(r'a_1=3') + ' និង ' + M(r'S_3=21') + ' (' + M(r'q>0') + ')។ រក ' + M(r'q') + ' និង ' + M(r'S_7') + '។',
        [
            (M(r'S_3=3(q^2+q+1)=21') + '។', 1),
            (M(r'q^2+q-6=0') + '។', 1),
            (M(r'(q+3)(q-2)=0') + ' និង ' + M(r'q>0\Rightarrow q=2') + '។', 1),
            (M(r'S_7=3(2^7-1)/(2-1)') + '។', 1),
            (M(r'S_7=381') + '។', 1),
        ]
    ))
    C.append(writing(
        'hard', 'sec5_inf',
        'ស្វ៊ីតមាន ' + M(r'a_2=-9') + ' និង ' + M(r'a_5=1/3') + '។ រក ' + M(r'q') + ', ' + M(r'a_1') + ' និង ' + M(r'S_\infty') + '។',
        [
            (M(r'q^3=a_5/a_2=(1/3)/(-9)=-1/27') + '។', 1),
            (M(r'q=-1/3') + '។', 1),
            (M(r'a_1=a_2/q=27') + '។', 1),
            ('ពិនិត្យ ' + M(r'|q|<1') + '។', 1),
            (M(r'S_\infty=27/(1+1/3)=81/4') + '។', 1),
        ]
    ))
    C.append(writing(
        'hard', 'sec4_sum',
        'គណនាផលបូក ' + M(r'48+24+12+\cdots+3/8') + '។',
        [
            (M(r'q=24/48=1/2') + '។', 1),
            (M(r'48\cdot(1/2)^{n-1}=3/8') + '។', 1),
            (M(r'n=8') + '។', 1),
            (M(r'S_8=48(1-2^{-8})/(1/2)') + '។', 1),
            (M(r'S_8=765/8') + '។', 1),
        ]
    ))
    C.append(writing(
        'hard', 'sec5_inf',
        'រក ' + M(r'a_1') + ' និង ' + M(r'q') + ' បើ ' + M(r'S_2=16') + ' និង ' + M(r'S_\infty=25') + ' (' + M(r'q>0') + ')។',
        [
            (M(r'a_1(1+q)=16') + '។', 1),
            (M(r'a_1/(1-q)=25') + '។', 1),
            (M(r'25(1-q^2)=16') + '។', 1),
            (M(r'q=3/5') + '។', 1),
            (M(r'a_1=10') + '។', 1),
        ]
    ))
    C.append(writing(
        'hard', 'sec2_term',
        'ស្វ៊ីតមាន ' + M(r'a_3=18') + ' និង ' + M(r'a_7=1458') + ' (' + M(r'q>0') + ')។ រក ' + M(r'a_{10}') + '។',
        [
            (M(r'q^4=1458/18=81') + '។', 1),
            (M(r'q=3') + '។', 1),
            (M(r'a_1=18/9=2') + '។', 1),
            (M(r'a_{10}=2\cdot 3^9') + '។', 1),
            (M(r'a_{10}=39366') + '។', 1),
        ]
    ))

    # ----- Writing pisa -----
    C.append(writing(
        'pisa', 'sec2_pop',
        'ប្រជាជនឆ្នាំ ២០០០ មាន ២ លាននាក់ កើន ៤% រាល់ឆ្នាំ។ សរសេររូបមន្ត ' + M(r'a_n') + ' ហើយគណនាឆ្នាំ ២០០៩។',
        [
            ('ឆ្នាំ ២០០០ ជាពាក្យទី១ ៖ ' + M(r'a_1=2') + ' លាននាក់។', 1),
            (M(r'q=1.04') + '។', 1),
            (M(r'a_n=2\cdot(1.04)^{n-1}') + '។', 1),
            ('ឆ្នាំ ២០០៩ ជាពាក្យទី១០។', 1),
            (M(r'a_{10}=2\cdot(1.04)^9\approx 2.85') + ' លាននាក់។', 1),
        ]
    ))
    C.append(writing(
        'pisa', 'sec4_chess',
        'ពន្យល់ចំនួនស្រូវសរុបលើក្តារអុក ៦៤ ប្រឡោះ (១, ២, ៤, …)។',
        [
            (M(r'a_1=1') + ', ' + M(r'q=2') + ', ' + M(r'n=64') + '។', 1),
            (M(r'a_n=2^{n-1}') + '។', 1),
            (M(r'S_{64}=(2^{64}-1)/(2-1)') + '។', 1),
            (M(r'S_{64}=2^{64}-1=18446744073709551615') + ' គ្រាប់។', 1),
            ('ប្រៀបធៀបនឹងទិន្នផលស្រូវកម្ពុជា ' + M(r'5\times 10^6') + ' តោនក្នុងមួយឆ្នាំ។', 1),
        ]
    ))
    C.append(writing(
        'pisa', 'sec5_bounce',
        'ប៉ោលយោលដំបូងបានធ្នូ ២៤ dm រួចប្រវែងធ្នូថយ ២០% រាល់លើក។ រកប្រវែងគន្លងសរុបរហូតឈប់។',
        [
            (M(r'a_1=24') + ' dm។', 1),
            (M(r'q=80\%=0.8') + '។', 1),
            ('ពិនិត្យ ' + M(r'|q|<1') + '។', 1),
            (M(r'S_\infty=24/(1-0.8)') + '។', 1),
            (M(r'S_\infty=120') + ' dm។', 1),
        ]
    ))
    C.append(writing(
        'pisa', 'sec2_bank',
        'ដាក់ប្រាក់ ១០០ ០០០ រៀល ការប្រាក់រួម ៦% ក្នុងមួយឆ្នាំ។ សរសេរប្រាក់ក្រោយ ' + M(r'n') + ' ឆ្នាំ និងក្រោយ ៥ ឆ្នាំ។',
        [
            ('ដើមទុន ' + M(r'A_0=100000') + ' រៀល។', 1),
            (M(r'q=1.06') + '។', 1),
            (M(r'A_n=100000\cdot(1.06)^n') + '។', 1),
            (M(r'A_5=100000\cdot(1.06)^5') + '។', 1),
            (M(r'A_5\approx 133822.56') + ' រៀល។', 1),
        ]
    ))
    C.append(writing(
        'pisa', 'sec2_pend',
        'ប៉ោលទំហំដំបូង ១៨ cm កាត់ ៥% រាល់លើក។ រកទំហំលើកទី១០ និងផលបូក ១៥ លើកដំបូង។',
        [
            (M(r'a_n=18\cdot(0.95)^{n-1}') + '។', 1),
            (M(r'a_{10}=18\cdot(0.95)^9') + '។', 1),
            (M(r'a_{10}\approx 11.34') + ' cm។', 1),
            (M(r'S_{15}=18(1-0.95^{15})/0.05') + '។', 1),
            (M(r'S_{15}\approx 193.2') + ' cm។', 1),
        ]
    ))
    C.append(writing(
        'pisa', 'sec5_inf',
        'សរសេរ ' + M(r'4.\overline{57}') + ' ជាប្រភាគដោយប្រើស្វ៊ីតធរណីមាត្រអនន្ត។',
        [
            (M(r'4.\overline{57}=4+0.\overline{57}') + '។', 1),
            (M(r'0.\overline{57}=57/99') + '។', 1),
            (M(r'4+57/99=396/99+57/99') + '។', 1),
            (M(r'453/99') + '។', 1),
            (M(r'151/33') + '។', 1),
        ]
    ))

    return C
