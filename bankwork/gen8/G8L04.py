from lib import *
from fractions import Fraction as F
import math
LESSON = 'រង្វាស់រង្វាល់'
PI = F(314, 100)

def trim(x, nd=6):
    s = f'{float(x):.{nd}f}'.rstrip('0').rstrip('.')
    return s
def N(x, nd=4):
    s = trim(x, nd)
    return num(float(s), None) if False else _grp(s)
def _grp(s):
    neg = s.startswith('-'); s = s.lstrip('-')
    ip, _, fp = s.partition('.')
    if len(ip) >= 4: ip = '\\,'.join([ip[max(0, i - 3):i] for i in range(len(ip), 0, -3)][::-1])
    return ('-' if neg else '') + ip + ('.' + fp if fp else '')
def U(x, u, nd=4): return M(N(x, nd) + '\\ \\text{' + u + '}')
def _unit(u):
    import re
    return '\\text{' + re.sub(r'\^(\d)', '', u) + '}' + ''.join('^{%s}' % d for d in re.findall(r'\^(\d)', u))
def sci(x, u='', nd=6):
    x = F(x); e = 0
    while x >= 10: x /= 10; e += 1
    while x < 1: x *= 10; e -= 1
    return M(trim(x, nd) + '\\times10^{' + str(e) + '}' + ('\\ ' + _unit(u) if u else ''))
def Wsci(ans, cand, u):
    out = []
    for c in cand:
        t = sci(c, u)
        if t != sci(ans, u) and t not in out: out.append(t)
    return out[:3]
def Wu(ans, cand, u, nd=4):
    out = []
    for c in cand:
        t = U(c, u, nd)
        if t != U(ans, u, nd) and t not in out: out.append(t)
    k = 2
    while len(out) < 3:
        t = U(F(ans) * (10 + k) / 10, u, nd); k += 1
        if t != U(ans, u, nd) and t not in out: out.append(t)
    return out[:3]
def area(d_m): return PI * F(d_m) ** 2 / 4
def vol(d_m, l_m): return area(d_m) * l_m
MM = F(1, 1000)

# ---------------- figures ----------------
def _t(x, y, s, a='middle', kh=False, sz=13):
    if kh: st = f"font-family='Khmer OS Battambang,Noto Sans Khmer,serif' font-style='normal' font-size='{sz}'"
    else: st = f"font-family='Times New Roman,serif' font-style='italic' font-size='{sz}'"
    return f"<text x='{x}' y='{y}' text-anchor='{a}' {st} fill='#111'>{s}</text>"
def svg(w, h, body): return f"<svg xmlns='http://www.w3.org/2000/svg' width='{w}' height='{h}' viewBox='0 0 {w} {h}'><rect width='{w}' height='{h}' fill='white'/>{body}</svg>"
ST = "fill='#eef3ff' stroke='#1d2540' stroke-width='1.6'"
LN = "stroke='#1d2540' stroke-width='1.4' fill='none'"
def fig_circle(label):
    return svg(150, 130, f"<circle cx='75' cy='60' r='45' {ST}/><line x1='30' y1='60' x2='120' y2='60' {LN} stroke-dasharray='4 3'/>" + _t(75, 48, label) + _t(75, 122, 'មុខកាត់ស៊ីឡាំង', kh=True, sz=12))
def fig_cyl(dlabel, llabel):
    return svg(260, 120,
        f"<ellipse cx='40' cy='55' rx='14' ry='30' {ST}/><rect x='40' y='25' width='170' height='60' fill='#eef3ff' stroke='none'/>"
        f"<line x1='40' y1='25' x2='210' y2='25' {LN}/><line x1='40' y1='85' x2='210' y2='85' {LN}/>"
        f"<ellipse cx='210' cy='55' rx='14' ry='30' {ST}/><ellipse cx='40' cy='55' rx='14' ry='30' fill='none' stroke='#1d2540' stroke-width='1.6'/>"
        f"<line x1='26' y1='55' x2='54' y2='55' {LN} stroke-dasharray='3 2'/>" + _t(40, 100, dlabel, 'middle') .replace("y='100'", "y='102'") + _t(125, 20, llabel))
def fig_box(a, b, c):
    # a = long edge (front, bottom), b = vertical edge, c = depth edge (slanted)
    return svg(270, 130,
        f"<polygon points='20,100 200,100 200,50 20,50' {ST}/><polygon points='20,50 200,50 230,25 50,25' fill='#dfe8ff' stroke='#1d2540' stroke-width='1.6'/>"
        f"<polygon points='200,100 230,75 230,25 200,50' fill='#cfdcff' stroke='#1d2540' stroke-width='1.6'/>"
        + _t(110, 119, a) + _t(236, 55, b, 'start') + _t(103, 17, c).replace("x='103'", "x='125'").replace("y='17'", "y='19'"))
def fig_sheet(w, h):
    return svg(210, 195, f"<rect x='14' y='8' width='110' height='155' {ST} rx='1'/>" + _t(69, 182, w) + _t(132, 90, h, 'start'))
def fig_route(km, v1, v2):
    return svg(330, 110,
        f"<line x1='30' y1='60' x2='300' y2='60' {LN}/><circle cx='30' cy='60' r='5' fill='#1d2540'/><circle cx='300' cy='60' r='5' fill='#1d2540'/>"
        f"<line x1='36' y1='44' x2='120' y2='44' stroke='#c0392b' stroke-width='1.8'/><polygon points='120,40 130,44 120,48' fill='#c0392b'/>"
        f"<line x1='294' y1='78' x2='210' y2='78' stroke='#2563eb' stroke-width='1.8'/><polygon points='210,74 200,78 210,82' fill='#2563eb'/>"
        + _t(30, 90, 'បាត់ដំបង', kh=True, sz=12) + _t(300, 100, 'ភ្នំពេញ', kh=True, sz=12) + _t(165, 56, km).replace("y='56'", "y='36'") .replace("x='165'", "x='165'")
        + _t(78, 28, v1) + _t(250, 100, v2))

def cands():
    C = []
    # ============ 1. ផ្ទៃក្រឡានិងមាឌ ============
    C.append(mcq('easy', 'units', M('1\\ \\text{mm}') + ' ស្មើនឹងប៉ុន្មានម៉ែត្រ?', M('10^{-3}\\ \\text{m}'), [M('10^{-2}\\ \\text{m}'), M('10^{3}\\ \\text{m}'), M('10^{-1}\\ \\text{m}')], M('1\\ \\text{mm} = 0.001\\ \\text{m}') + '។'))
    C.append(mcq('easy', 'units', M('1\\ \\text{cm}') + ' ស្មើនឹងប៉ុន្មានម៉ែត្រ?', M('10^{-2}\\ \\text{m}'), [M('10^{-3}\\ \\text{m}'), M('10^{2}\\ \\text{m}'), M('10^{-1}\\ \\text{m}')], M('1\\ \\text{cm} = 0.01\\ \\text{m}') + '។'))
    C.append(mcq('easy', 'units', 'រូបមន្តផ្ទៃក្រឡាមុខកាត់ស៊ីឡាំងដែលមានអង្កត់ផ្ចិត ' + M('d') + ' គឺ៖', M('\\mathcal{A} = \\dfrac{\\pi d^2}{4}'), [M('\\mathcal{A} = \\pi d^2'), M('\\mathcal{A} = \\dfrac{\\pi d}{4}'), M('\\mathcal{A} = 2\\pi d')], 'មុខកាត់ជារង្វង់ ' + M('\\mathcal{A} = \\pi r^2 = \\dfrac{\\pi d^2}{4}') + '។'))
    C.append(mcq('easy', 'units', 'មាឌស៊ីឡាំងមានអង្កត់ផ្ចិត ' + M('d') + ' និងប្រវែង ' + M('l') + ' គឺ៖', M('V = \\dfrac{\\pi d^2}{4} \\times l'), [M('V = \\pi d \\times l'), M('V = \\dfrac{\\pi d^2}{4} + l'), M('V = \\dfrac{\\pi d}{4} \\times l')], 'មាឌ = ផ្ទៃក្រឡាមុខកាត់ × ប្រវែង។'))
    C.append(mcq('easy', 'units', 'ដែក ' + M(6) + ' លី មានន័យថាដែកមានអង្កត់ផ្ចិត៖', M('6\\ \\text{mm}'), [M('6\\ \\text{cm}'), M('0.6\\ \\text{mm}'), M('12\\ \\text{mm}')], M('1') + ' លី ' + M('= 1\\ \\text{mm}') + '។'))
    C.append(mcq('easy', 'mass', 'ក្រដាស ' + M('80\\ \\text{g/m}^2') + ' មានន័យថា៖', 'ក្រដាស ' + M('1\\ \\text{m}^2') + ' មានម៉ាស ' + M('80\\ \\text{g}'), ['ក្រដាស ' + M('80\\ \\text{m}^2') + ' មានម៉ាស ' + M('1\\ \\text{g}'), 'ក្រដាស ១ សន្លឹកមានម៉ាស ' + M('80\\ \\text{g}'), 'កម្រាស់ក្រដាស ' + M('80\\ \\text{mm}')], 'ម៉ាសធៀបនឹងផ្ទៃក្រឡាគឺម៉ាសក្នុង ' + M('1\\ \\text{m}^2') + '។'))
    C.append(mcq('easy', 'mass', M('1\\ \\text{g/cm}^3') + ' ស្មើនឹងប៉ុន្មាន ' + M('\\text{kg/m}^3') + '?', M('1000\\ \\text{kg/m}^3'), [M('1\\ \\text{kg/m}^3'), M('0.001\\ \\text{kg/m}^3'), M('100\\ \\text{kg/m}^3')], M('\\dfrac{10^{-3}\\ \\text{kg}}{(10^{-2}\\ \\text{m})^3} = 1000\\ \\text{kg/m}^3') + '។'))
    C.append(mcq('easy', 'mass', 'ម៉ាសមាឌនៃដែកគឺ ' + M('7.874\\ \\text{g/cm}^3') + '។ គិតជា ' + M('\\text{kg/m}^3') + ' ស្មើ៖', M('7\\,874\\ \\text{kg/m}^3'), [M('787.4\\ \\text{kg/m}^3'), M('7.874\\ \\text{kg/m}^3'), M('78\\,740\\ \\text{kg/m}^3')], M('7.874 \\times 1000 = 7\\,874') + '។'))
    C.append(mcq('easy', 'speed', 'រូបមន្តល្បឿនមធ្យមគឺ៖', M('v = \\dfrac{d}{t}'), [M('v = d \\times t'), M('v = \\dfrac{t}{d}'), M('v = d + t')], 'ល្បឿន = ចម្ងាយចរ ÷ រយៈពេល។'))
    C.append(mcq('easy', 'speed', 'រថភ្លើងធ្វើដំណើរ ' + M(3) + ' ម៉ោង ដោយល្បឿន ' + M('30\\ \\text{km/h}') + '។ ចម្ងាយចរ៖', M('90\\ \\text{km}'), [M('10\\ \\text{km}'), M('33\\ \\text{km}'), M('27\\ \\text{km}')], M('30 \\times 3 = 90') + '។'))
    C.append(mcq('easy', 'speed', 'ពីងពាងរត់ ' + M('20\\ \\text{cm}') + ' ក្នុង ' + M('5\\ \\text{s}') + '។ ល្បឿនមធ្យមគឺ៖', M('4\\ \\text{cm/s}'), [M('100\\ \\text{cm/s}'), M('0.25\\ \\text{cm/s}'), M('15\\ \\text{cm/s}')], M('\\dfrac{20}{5} = 4') + '។'))
    for (dmm) in ('1.5', '2.5', '0.2', '1.2', '2'):
        d = F(dmm) * MM; A = area(d)
        C.append(with_img(mcq('medium', 'area', 'ខ្សែភ្លើងរាងស៊ីឡាំងមានអង្កត់ផ្ចិត ' + M(dmm + '\\ \\text{mm}') + '។ គណនាផ្ទៃក្រឡាមុខកាត់គិតជា ' + M('\\text{m}^2') + ' (យក ' + M('\\pi = 3.14') + ')៖', sci(A, '\\text{m}^2'.replace('\\text{', '').replace('}', '') if False else 'm^2'), Wsci(A, [A * 10, A / 10, PI * d * d, A * 4, A * 1000], 'm^2'),
                                   M('\\mathcal{A} = \\dfrac{3.14 \\times (' + dmm + '\\times10^{-3})^2}{4}') + ' ' + M('= ' + trim(A * 10 ** 6, 8) + '\\times10^{-6}\\ \\text{m}^2') + '។'), fig_circle('d = ' + dmm + ' mm')))
    for (dmm, l) in ((6, 12), (16, 12), (12, 12), (24, 10), (7, 9)):
        d = F(dmm) * MM; V = vol(d, l)
        C.append(with_img(mcq('medium', 'volume', 'សរសៃដែកមានអង្កត់ផ្ចិត ' + M(f'{dmm}\\ \\text{{mm}}') + ' ប្រវែង ' + M(f'{l}\\ \\text{{m}}') + '។ មាឌគិតជា ' + M('\\text{m}^3') + ' (យក ' + M('\\pi = 3.14') + ')៖', sci(V, 'm^3'), Wsci(V, [V * 10, V / 10, V * 4, V * 1000, V / 1000], 'm^3'),
                                   M('V = \\dfrac{3.14 \\times ' + str(dmm * dmm) + '\\times10^{-6}}{4} \\times ' + str(l) + ' = ' + trim(V * 10 ** 6, 5) + '\\times10^{-6}\\ \\text{m}^3') + '។'), fig_cyl(f'd = {dmm} mm', f'l = {l} m')))
    A = area(F(2) * MM)
    C.append(mcq('medium', 'area', 'ខ្សែភ្លើងអង្កត់ផ្ចិត ' + M('2\\ \\text{mm}') + '។ គណនាផ្ទៃក្រឡាមុខកាត់គិតជា ' + M('\\text{m}^2') + '៖', sci(A, 'm^2'), Wsci(A, [A * 10, A / 10, A * 4], 'm^2'), M('d^2 = 4\\times10^{-6}') + ' ; ' + M('\\mathcal{A} = 3.14 \\times 10^{-6}') + '។'))
    C.append(mcq('hard', 'area', 'ខ្សែភ្លើងមួយមានផ្ទៃក្រឡាមុខកាត់ ' + M('\\dfrac{\\pi}{4} \\times 10^{-6}\\ \\text{m}^2') + '។ អង្កត់ផ្ចិតគឺ៖', M('1\\ \\text{mm}'), [M('2\\ \\text{mm}'), M('0.1\\ \\text{mm}'), M('10\\ \\text{mm}')], M('d = \\sqrt{\\dfrac{4\\mathcal{A}}{\\pi}} = \\sqrt{10^{-6}} = 10^{-3}\\ \\text{m}') + '។'))
    V = vol(F(2, 100), 200)
    C.append(mcq('medium', 'volume', 'ខ្សែភ្លើងអង្កត់ផ្ចិត ' + M('2\\ \\text{cm}') + ' ប្រវែង ' + M('200\\ \\text{m}') + '។ មាឌគិតជា ' + M('\\text{m}^3') + ' (' + M('\\pi = 3.14') + ')៖', M('0.0628\\ \\text{m}^3'), [M('0.628\\ \\text{m}^3'), M('0.00628\\ \\text{m}^3'), M('0.2512\\ \\text{m}^3')], M('d = 0.02\\ \\text{m}') + ' ; ' + M('V = 3.14 \\times 10^{-4} \\times 200 = 0.0628') + '។'))
    # wood beam
    C.append(with_img(mcq('medium', 'volume', 'ឈើជ្រុងមួយដើមមានមុខកាត់ ' + M('4\\ \\text{cm} \\times 8\\ \\text{cm}') + ' និងប្រវែង ' + M('4.5\\ \\text{m}') + '។ មាឌ ' + M(1) + ' ដើម៖', M('0.0144\\ \\text{m}^3'), [M('0.144\\ \\text{m}^3'), M('144\\ \\text{m}^3'), M('0.00144\\ \\text{m}^3')], M('0.04 \\times 0.08 \\times 4.5 = 0.0144') + '។'), fig_box('4.5 m', '8 cm', '4 cm')))
    C.append(with_img(mcq('hard', 'volume', 'ឈើជ្រុងមួយដើមមានមុខកាត់ ' + M('4\\ \\text{cm} \\times 8\\ \\text{cm}') + ' ប្រវែង ' + M('4.5\\ \\text{m}') + '។ ទិញ ' + M(50) + ' ដើម ឈើ ' + M('1\\ \\text{m}^3') + ' ថ្លៃ ' + M('1\\,200\\,000') + ' ៛។ ត្រូវចំណាយ៖', M('864\\,000') + ' ៛', [M('86\\,400') + ' ៛', M('8\\,640\\,000') + ' ៛', M('17\\,280') + ' ៛'], M('V = 50 \\times 0.0144 = 0.72\\ \\text{m}^3') + ' ; ' + M('0.72 \\times 1\\,200\\,000 = 864\\,000') + '។'), fig_box('4.5 m', '8 cm', '4 cm')))
    # ============ 2. ម៉ាស ============
    A4 = F(210, 1000) * F(297, 1000)
    C.append(with_img(mcq('medium', 'mass', 'ក្រដាសខ្នាត ' + M('210\\ \\text{mm} \\times 297\\ \\text{mm}') + '។ ផ្ទៃក្រឡា ១ សន្លឹកគិតជា ' + M('\\text{m}^2') + '៖', M('0.06237\\ \\text{m}^2'), [M('0.6237\\ \\text{m}^2'), M('62\\,370\\ \\text{m}^2'), M('0.006237\\ \\text{m}^2')], M('0.210 \\times 0.297 = 0.06237') + '។'), fig_sheet('210 mm', '297 mm')))
    m1 = A4 * 80
    C.append(with_img(mcq('medium', 'mass', 'ក្រដាសខ្នាត ' + M('210\\ \\text{mm} \\times 297\\ \\text{mm}') + ' ម៉ាសធៀបនឹងផ្ទៃក្រឡា ' + M('80\\ \\text{g/m}^2') + '។ ម៉ាស ១ សន្លឹក៖', M('4.9896\\ \\text{g}'), [M('49.896\\ \\text{g}'), M('0.49896\\ \\text{g}'), M('4989.6\\ \\text{g}')], M('0.06237 \\times 80 = 4.9896') + '។'), fig_sheet('210 mm', '297 mm')))
    C.append(mcq('hard', 'mass', 'ក្រដាសរ៉ាម ១ ដុំមាន ' + M(500) + ' សន្លឹក ខ្នាត ' + M('210\\ \\text{mm}\\times297\\ \\text{mm}') + ' ម៉ាសធៀបនឹងផ្ទៃក្រឡា ' + M('80\\ \\text{g/m}^2') + '។ ម៉ាសរ៉ាមមួយប្រហែល៖', M('2.5\\ \\text{kg}'), [M('25\\ \\text{kg}'), M('0.25\\ \\text{kg}'), M('4.99\\ \\text{kg}')], M('500 \\times 4.9896\\ \\text{g} = 2\\,494.8\\ \\text{g} \\approx 2.5\\ \\text{kg}') + '។'))
    M2 = F(2 * 1000, 1) * 0 + (31185 * 1 / F(1000)) * F(104, 100) * 70
    C.append(mcq('hard', 'mass', 'ក្រដាសដើមម៉ាស ' + M('70\\ \\text{g/m}^2') + ' កាត់ជារ៉ាម ខ្នាត ' + M('210\\ \\text{mm}\\times297\\ \\text{mm}') + ' (' + M(500) + ' សន្លឹក) ខាតចំនៀរ ' + M('4\\%') + ' (ផ្ទៃខាតបូកបន្ថែម ' + M('4\\%') + ' នៃផ្ទៃរ៉ាម)។ ម៉ាសក្រដាសត្រូវប្រើ ១ រ៉ាមប្រហែល៖', M('2.3\\ \\text{kg}'), [M('2.2\\ \\text{kg}'), M('3.2\\ \\text{kg}'), M('2.8\\ \\text{kg}')], M('31.185 \\times 1.04 = 32.4324\\ \\text{m}^2') + ' ; ' + M('\\times 70 = 2\\,270.268\\ \\text{g} \\approx 2.3\\ \\text{kg}') + '។'))
    for (dm, name) in ((10, '១០'), (12, '១២'), (14, '១៤')):
        mm = vol(F(dm) * MM, 12) * 7874
        C.append(with_img(mcq('hard' if dm == 14 else 'medium', 'mass', 'ដែក ' + M(dm) + ' លី ប្រវែង ' + M('12\\ \\text{m}') + ' ម៉ាសមាឌ ' + M('7\\,874\\ \\text{kg/m}^3') + ' (' + M('\\pi=3.14') + ')។ ម៉ាសប្រហែល៖', U(mm, 'kg', 1), Wu(mm, [mm * 10, mm / 10, mm * 4, mm / 4], 'kg', 1),
                                   M('m = \\dfrac{3.14 \\times ' + str(dm * dm) + '\\times10^{-6}}{4} \\times 12 \\times 7874 \\approx ' + trim(mm, 1) + '\\ \\text{kg}') + '។'), fig_cyl(f'{dm} លី', 'l = 12 m').replace('>' + f'{dm} លី<', '>' + f'd = {dm} mm<')))
    C.append(mcq('hard', 'mass', 'ដែក ' + M(10) + ' លីមួយដើមមានម៉ាស ' + M('7.4\\ \\text{kg}') + '។ ដែក ' + M(16) + ' លី (ប្រវែងដូចគ្នា) មានម៉ាស៖', M('18.944\\ \\text{kg}'), [M('11.84\\ \\text{kg}'), M('12.8\\ \\text{kg}'), M('4.625\\ \\text{kg}')], 'ម៉ាសសមាមាត្រនឹង ' + M('d^2') + ' ៖ ' + M('7.4 \\times 1.6^2 = 18.944') + '។'))
    cu = vol(F(25, 10) * MM, 100) * 8940
    C.append(mcq('hard', 'mass', 'ខ្សែស្ពាន់ប្រវែង ' + M('100\\ \\text{m}') + ' អង្កត់ផ្ចិត ' + M('2.5\\ \\text{mm}') + ' ម៉ាសមាឌ ' + M('8.94\\ \\text{g/cm}^3') + '។ ម៉ាសប្រហែល៖', U(cu, 'kg', 3), Wu(cu, [cu * 10, cu / 10, cu * 4], 'kg', 3), M('V = 490.625\\ \\text{cm}^3') + ' ; ' + M('m = 490.625 \\times 8.94 = 4\\,386.19\\ \\text{g}') + '។'))
    # ============ 3. ល្បឿន ============
    C.append(mcq('easy', 'speed', 'ទោចក្រយានយន្តរត់ ' + M('108\\ \\text{km}') + ' ក្នុង ' + M('2.25\\ \\text{h}') + '។ ល្បឿនមធ្យម៖', M('48\\ \\text{km/h}'), [M('243\\ \\text{km/h}'), M('54\\ \\text{km/h}'), M('36\\ \\text{km/h}')], M('108 \\div 2.25 = 48') + '។'))
    C.append(mcq('medium', 'speed', M('2\\ \\text{h}\\ 15\\ \\text{mn}') + ' ស្មើនឹងប៉ុន្មានម៉ោង?', M('2.25\\ \\text{h}'), [M('2.15\\ \\text{h}'), M('2.5\\ \\text{h}'), M('135\\ \\text{h}')], M('2 + \\dfrac{15}{60} = 2.25') + '។'))
    C.append(mcq('medium', 'speed', M('6\\ \\text{m/s}') + ' ស្មើនឹងប៉ុន្មាន ' + M('\\text{km/h}') + '?', M('21.6\\ \\text{km/h}'), [M('6\\ \\text{km/h}'), M('1.67\\ \\text{km/h}'), M('216\\ \\text{km/h}')], M('6 \\times 3.6 = 21.6') + '។'))
    C.append(mcq('medium', 'speed', 'សំឡេងធ្វើដំណើរ ' + M('343\\ \\text{m/s}') + '។ ក្នុង ' + M('1') + ' នាទី សំឡេងធ្វើដំណើរបាន៖', M('20.58\\ \\text{km}'), [M('343\\ \\text{km}'), M('5.72\\ \\text{km}'), M('2.058\\ \\text{km}')], M('343 \\times 60 = 20\\,580\\ \\text{m}') + '។'))
    for (d, v) in ((1700, 575), ):
        pass
    C.append(mcq('medium', 'speed', 'សុខារត់ក្នុងល្បឿន ' + M('8\\ \\text{m/s}') + ' ចម្ងាយ ' + M('2\\ \\text{km}') + '។ ត្រូវចំណាយពេល៖', M('250\\ \\text{s}'), [M('16\\ \\text{s}'), M('0.004\\ \\text{s}'), M('2\\,000\\ \\text{s}')], M('t = \\dfrac{2000}{8} = 250\\ \\text{s} = 4\\ \\text{mn}\\ 10\\ \\text{s}') + '។'))
    C.append(mcq('medium', 'speed', 'រថយន្តផ្លាស់ទី ' + M('2.4\\ \\text{km}') + ' ក្នុង ' + M(120) + ' នាទី។ ល្បឿនមធ្យម៖', M('1.2\\ \\text{km/h}'), [M('0.02\\ \\text{km/h}'), M('120\\ \\text{km/h}'), M('2.4\\ \\text{km/h}')], M('120\\ \\text{mn} = 2\\ \\text{h}') + ' ; ' + M('\\dfrac{2.4}{2} = 1.2') + '។'))
    C.append(mcq('hard', 'speed', 'វិបុលជិះកង់ ' + M('26\\ \\text{km}') + ' ក្នុង ' + M('41\\ \\text{mn}\\ 52\\ \\text{s}') + '។ ល្បឿនមធ្យមប្រហែល៖', M('37.26\\ \\text{km/h}'), [M('0.62\\ \\text{km/h}'), M('26.6\\ \\text{km/h}'), M('45.1\\ \\text{km/h}')], M('2512\\ \\text{s} = \\dfrac{157}{225}\\ \\text{h}') + ' ; ' + M('26 \\times \\dfrac{225}{157} \\approx 37.26') + '។'))
    C.append(mcq('hard', 'speed', 'យន្តហោះហោះ ' + M('575\\ \\text{km/h}') + ' ចម្ងាយ ' + M('1\\,700\\ \\text{km}') + '។ រយៈពេលប្រហែល៖', M('2\\ \\text{h}\\ 57\\ \\text{mn}'), [M('3\\ \\text{h}\\ 30\\ \\text{mn}'), M('2\\ \\text{h}\\ 22\\ \\text{mn}'), M('2\\ \\text{h}\\ 9\\ \\text{mn}')], M('\\dfrac{1\\,700}{575} = \\dfrac{68}{23} \\approx 2.9565\\ \\text{h}') + '។'))
    C.append(with_img(mcq('hard', 'speed', 'រថភ្លើងចេញពីបាត់ដំបង (ល្បឿន ' + M('60\\ \\text{km/h}') + ') ម៉ូតូចេញពីភ្នំពេញ (ល្បឿន ' + M('40\\ \\text{km/h}') + ') ក្នុងម៉ោងដូចគ្នា ចម្ងាយ ' + M('291\\ \\text{km}') + '។ ពួកគេជួបគ្នាក្រោយ៖', M('2.91\\ \\text{h}'), [M('4.85\\ \\text{h}'), M('7.275\\ \\text{h}'), M('5.82\\ \\text{h}')], 'ល្បឿនរួម ' + M('100\\ \\text{km/h}') + ' ; ' + M('t = \\dfrac{291}{100} = 2.91') + '។'), fig_route('291 km', '60 km/h', '40 km/h')))
    C.append(mcq('hard', 'speed', 'រតនាដើរ ' + M('800\\ \\text{m}') + ' ដោយល្បឿន ' + M('5\\ \\text{km/h}') + '។ រយៈពេលដើរ៖', M('9.6\\ \\text{mn}'), [M('16\\ \\text{mn}'), M('0.16\\ \\text{mn}'), M('6.25\\ \\text{mn}')], M('t = \\dfrac{0.8}{5} = 0.16\\ \\text{h} = 9.6\\ \\text{mn}') + '។'))
    # PISA
    C.append(mcq('pisa', 'pisa', 'ពពកមួយរសាត់ពីព្រះសីហនុមកភ្នំពេញ ចម្ងាយ ' + M('230\\ \\text{km}') + ' ខ្យល់ល្បឿន ' + M('6\\ \\text{m/s}') + '។ រយៈពេលប្រហែល៖', M('10\\ \\text{h}\\ 39\\ \\text{mn}'), [M('38.3\\ \\text{h}'), M('1\\ \\text{h}\\ 39\\ \\text{mn}'), M('13\\ \\text{h}\\ 50\\ \\text{mn}')], M('6\\ \\text{m/s} = 21.6\\ \\text{km/h}') + ' ; ' + M('\\dfrac{230}{21.6} \\approx 10.65\\ \\text{h}') + '។'))
    C.append(mcq('pisa', 'pisa', 'រតនាត្រូវដល់សាលា ' + M('15') + ' នាទីមុន ' + M('7\\ \\text{h}\\ 00') + '។ ផ្ទះឆ្ងាយ ' + M('800\\ \\text{m}') + ' ដើរ ' + M('5\\ \\text{km/h}') + '។ ត្រូវចេញពីផ្ទះនៅម៉ោង៖', M('6\\ \\text{h}\\ 35\\ \\text{mn}\\ 24\\ \\text{s}'), [M('6\\ \\text{h}\\ 50\\ \\text{mn}'), M('6\\ \\text{h}\\ 45\\ \\text{mn}'), M('6\\ \\text{h}\\ 29\\ \\text{mn}')], M('6\\ \\text{h}\\ 45 - 9\\ \\text{mn}\\ 36\\ \\text{s}') + '។'))
    C.append(mcq('pisa', 'pisa', 'សៀវភៅមួយក្បាល ' + M(100) + ' ទំព័រ ខ្នាត ' + M('148\\ \\text{mm}\\times210\\ \\text{mm}') + ' ម៉ាសក្រដាសសាច់ក្នុង ' + M('70\\ \\text{g/m}^2') + ' (ទំព័រ ' + M(100) + ' = ' + M(50) + ' សន្លឹក ' + M('= 50\\times 0.03108\\ \\text{m}^2') + ')។ ម៉ាសសាច់ក្នុង ១ ក្បាល៖', M('108.78\\ \\text{g}'), [M('217.56\\ \\text{g}'), M('10.878\\ \\text{g}'), M('155.4\\ \\text{g}')], M('50 \\times 0.03108 \\times 70 = 108.78') + '។'))
    C.append(mcq('pisa', 'pisa', 'ដែក ' + M(6) + ' លី ' + M(200) + ' ដើម និងដែក ' + M(10) + ' លី ' + M(20) + ' ដើម (ប្រវែង ' + M('12\\ \\text{m}') + ' ម្នាក់ៗ ម៉ាសមាឌ ' + M('7\\,874\\ \\text{kg/m}^3') + ') ម៉ាសសរុបប្រហែល (ឱ្យជិត ' + M('1') + ' kg)៖', M('682\\ \\text{kg}'), [M('820\\ \\text{kg}'), M('534\\ \\text{kg}'), M('148\\ \\text{kg}')], M('200 \\times 2.670 + 20 \\times 7.417 = 534.04 + 148.35 = 682.4') + '។'))
    C.append(mcq('pisa', 'pisa', 'ផ្គរលាន់ឮក្រោយផ្លេកបន្ទោរ ' + M(15) + ' វិនាទី។ បើសំឡេងធ្វើដំណើរ ' + M('343\\ \\text{m/s}') + ' ផ្លេកបន្ទោរនៅឆ្ងាយ៖', M('5.145\\ \\text{km}'), [M('22.9\\ \\text{km}'), M('51.45\\ \\text{km}'), M('0.5145\\ \\text{km}')], M('d = 343 \\times 15 = 5\\,145\\ \\text{m}') + '។'))
    # ============ WRITING ============
    def Sx(v, nd=6): return trim(v, nd)
    A15 = area(F('1.5') * MM)
    C.append(with_img(wr('easy', 'area', 'គណនាផ្ទៃក្រឡាមុខកាត់ខ្សែភ្លើងអង្កត់ផ្ចិត ក. ' + M('d = 1.5\\ \\text{mm}') + ' ខ. ' + M('d = 2\\ \\text{mm}') + ' គិតជា ' + M('\\text{m}^2') + ' (' + M('\\pi = 3.14') + ')។', [
        ('រូបមន្ត ' + M('\\mathcal{A} = \\dfrac{\\pi d^2}{4}'), 1), ('ក. ' + M('d = 1.5 \\times 10^{-3}\\ \\text{m}') + ' ; ' + M('d^2 = 2.25\\times10^{-6}'), 1), (M('\\mathcal{A} = \\dfrac{3.14 \\times 2.25\\times10^{-6}}{4} = 1.76625\\times10^{-6}\\ \\text{m}^2'), 1), ('ខ. ' + M('d^2 = 4\\times10^{-6}'), 1), (M('\\mathcal{A} = 3.14\\times10^{-6}\\ \\text{m}^2'), 1)]), fig_circle('d')))
    C.append(wr('medium', 'volume', 'គណនាមាឌសរសៃដែកគិតជា ' + M('\\text{m}^3') + ' ក. ' + M('d = 6\\ \\text{mm},\\ l = 12\\ \\text{m}') + ' ខ. ' + M('d = 16\\ \\text{mm},\\ l = 12\\ \\text{m}') + ' (' + M('\\pi = 3.14') + ')។', [
        ('រូបមន្ត ' + M('V = \\dfrac{\\pi d^2}{4} l'), 1), ('ក. ' + M('\\dfrac{3.14 \\times 36\\times10^{-6}}{4} \\times 12'), 1), (M('= 339.12\\times10^{-6} = 3.3912\\times10^{-4}\\ \\text{m}^3'), 1), ('ខ. ' + M('\\dfrac{3.14 \\times 256\\times10^{-6}}{4} \\times 12'), 1), (M('= 2.41152\\times10^{-3}\\ \\text{m}^3'), 1)]))
    C.append(wr('medium', 'volume', 'ឈើជ្រុងមួយដើមមានមុខកាត់ ' + M('4\\ \\text{cm} \\times 8\\ \\text{cm}') + ' ប្រវែង ' + M('4.5\\ \\text{m}') + '។ ទិញ ' + M(50) + ' ដើម ឈើ ' + M('1\\ \\text{m}^3') + ' ថ្លៃ ' + M('1\\,200\\,000') + ' ៛។ ត្រូវចំណាយប៉ុន្មាន?', [
        ('ប្តូរខ្នាត ' + M('4\\ \\text{cm} = 0.04\\ \\text{m}') + ' ; ' + M('8\\ \\text{cm} = 0.08\\ \\text{m}'), 1), ('មាឌ ១ ដើម ' + M('0.04 \\times 0.08 \\times 4.5 = 0.0144\\ \\text{m}^3'), 1), ('មាឌ ' + M(50) + ' ដើម ' + M('50 \\times 0.0144 = 0.72\\ \\text{m}^3'), 1), (M('0.72 \\times 1\\,200\\,000'), 1), (M('= 864\\,000') + ' ៛', 1)]))
    C.append(with_img(wr('medium', 'mass', 'ក្រដាសរ៉ាម ' + M(500) + ' សន្លឹក ខ្នាត ' + M('210\\ \\text{mm}\\times297\\ \\text{mm}') + ' ម៉ាសធៀបនឹងផ្ទៃក្រឡា ' + M('80\\ \\text{g/m}^2') + '។ គណនាម៉ាស ១ សន្លឹក និងម៉ាសរ៉ាម ១ ដុំ។', [
        ('ផ្ទៃក្រឡា ១ សន្លឹក ' + M('0.210 \\times 0.297 = 0.06237\\ \\text{m}^2'), 1), ('ម៉ាស ១ សន្លឹក ' + M('0.06237 \\times 80 = 4.9896\\ \\text{g}'), 2), ('ម៉ាស ' + M(500) + ' សន្លឹក ' + M('500 \\times 4.9896 = 2\\,494.8\\ \\text{g}'), 1), (M('\\approx 2.5\\ \\text{kg}'), 1)]), fig_sheet('210 mm', '297 mm')))
    C.append(wr('medium', 'speed', 'ក. រថភ្លើងធ្វើដំណើរ ' + M(3) + ' ម៉ោង ល្បឿន ' + M('30\\ \\text{km/h}') + ' ចម្ងាយប៉ុន្មាន? ខ. ដោយល្បឿនដដែល ធ្វើដំណើរ ' + M('500\\ \\text{m}') + ' ប្រើពេលប៉ុន្មាន?', [
        ('ក. ' + M('d = v \\times t = 30 \\times 3'), 1), (M('= 90\\ \\text{km}'), 1), ('ខ. ' + M('500\\ \\text{m} = 0.5\\ \\text{km}'), 1), (M('t = \\dfrac{0.5}{30} = \\dfrac{1}{60}\\ \\text{h}'), 1), (M('= 1\\ \\text{mn} = 60\\ \\text{s}'), 1)]))
    C.append(wr('hard', 'mass', 'ដែក ' + M(10) + ' លីមួយដើមមានម៉ាស ' + M('7.4\\ \\text{kg}') + '។ រកម៉ាសដែក ' + M(16) + ' លី (ប្រវែងដូចគ្នា ម៉ាសមាឌដូចគ្នា)។', [
        ('ម៉ាសសមាមាត្រនឹងផ្ទៃក្រឡាមុខកាត់ ឬ ' + M('d^2'), 1), (M('\\dfrac{m_{16}}{m_{10}} = \\left(\\dfrac{16}{10}\\right)^2 = 2.56'), 2), (M('m_{16} = 2.56 \\times 7.4'), 1), (M('= 18.944\\ \\text{kg}'), 1)]))
    C.append(wr('hard', 'mass', 'ខ្សែស្ពាន់ប្រវែង ' + M('100\\ \\text{m}') + ' មុខកាត់អង្កត់ផ្ចិត ' + M('2.5\\ \\text{mm}') + ' ម៉ាសមាឌ ' + M('8.94\\ \\text{g/cm}^3') + '។ គណនាម៉ាស (' + M('\\pi = 3.14') + ')។', [
        ('ប្តូរខ្នាត ' + M('d = 0.25\\ \\text{cm}') + ' ; ' + M('l = 10\\,000\\ \\text{cm}'), 1), (M('V = \\dfrac{3.14 \\times 0.25^2}{4} \\times 10\\,000'), 1), (M('= 490.625\\ \\text{cm}^3'), 1), (M('m = 490.625 \\times 8.94 = 4\\,386.19\\ \\text{g}'), 1), (M('\\approx 4.39\\ \\text{kg}'), 1)]))
    C.append(wr('hard', 'speed', 'វិបុលជិះកង់ ' + M('26\\ \\text{km}') + ' ក្នុងរយៈពេល ' + M('41\\ \\text{mn}\\ 52\\ \\text{s}') + '។ រកល្បឿនមធ្យមគិតជា ' + M('\\text{km/h}') + '។', [
        ('ប្តូរជាវិនាទី ' + M('41 \\times 60 + 52 = 2\\,512\\ \\text{s}'), 1), ('ប្តូរជាម៉ោង ' + M('\\dfrac{2\\,512}{3\\,600} = \\dfrac{157}{225}\\ \\text{h}'), 1), (M('v = \\dfrac{26}{157/225} = \\dfrac{26 \\times 225}{157}'), 2), (M('\\approx 37.26\\ \\text{km/h}'), 1)]))
    C.append(wr('hard', 'speed', 'រតនានៅចម្ងាយ ' + M('800\\ \\text{m}') + ' ពីសាលា ដើរល្បឿន ' + M('5\\ \\text{km/h}') + '។ ត្រូវដល់សាលា ' + M(15) + ' នាទីមុនម៉ោង ' + M('7\\ \\text{h}\\ 00') + '។ ត្រូវចេញពីផ្ទះម៉ោងប៉ុន្មាន?', [
        ('ចម្ងាយ ' + M('0.8\\ \\text{km}'), 1), ('រយៈពេលដើរ ' + M('t = \\dfrac{0.8}{5} = 0.16\\ \\text{h} = 9.6\\ \\text{mn} = 9\\ \\text{mn}\\ 36\\ \\text{s}'), 2), ('ម៉ោងត្រូវដល់ ' + M('7\\ \\text{h}\\ 00 - 15\\ \\text{mn} = 6\\ \\text{h}\\ 45\\ \\text{mn}'), 1), ('ម៉ោងចេញ ' + M('6\\ \\text{h}\\ 45\\ \\text{mn} - 9\\ \\text{mn}\\ 36\\ \\text{s} = 6\\ \\text{h}\\ 35\\ \\text{mn}\\ 24\\ \\text{s}'), 1)]))
    C.append(with_img(wr('hard', 'speed', 'ម៉ោង ' + M('7\\ \\text{h}\\ 00') + ' សុខាជិះរថភ្លើងពីបាត់ដំបងមកភ្នំពេញ (' + M('291\\ \\text{km}') + ') ល្បឿន ' + M('60\\ \\text{km/h}') + ' ហើយមករាជិះម៉ូតូពីភ្នំពេញមកបាត់ដំបង ល្បឿន ' + M('40\\ \\text{km/h}') + ' ចេញម៉ោងដូចគ្នា។ ពួកគេជួបគ្នាម៉ោងប៉ុន្មាន?', [
        ('ល្បឿនរួម ' + M('60 + 40 = 100\\ \\text{km/h}'), 1), (M('t = \\dfrac{291}{100} = 2.91\\ \\text{h}'), 1), (M('2.91\\ \\text{h} = 2\\ \\text{h}\\ 54.6\\ \\text{mn} = 2\\ \\text{h}\\ 54\\ \\text{mn}\\ 36\\ \\text{s}'), 1), (M('7\\ \\text{h}\\ 00 + 2\\ \\text{h}\\ 54\\ \\text{mn}\\ 36\\ \\text{s}'), 1), (M('= 9\\ \\text{h}\\ 54\\ \\text{mn}\\ 36\\ \\text{s}'), 1)]), fig_route('291 km', '60 km/h', '40 km/h')))
    # PISA writing
    C.append(wr('pisa', 'pisa', 'ដែក ' + M(10) + ' លី ' + M(12) + ' លី និង ' + M(14) + ' លី ប្រវែង ' + M('12\\ \\text{m}') + ' ម៉ាសមាឌ ' + M('7\\,874\\ \\text{kg/m}^3') + ' (' + M('\\pi = 3.14') + ')។ គណនាម៉ាសដែកមួយដើមនីមួយៗ (ទសភាគ ១ ខ្ទង់)។', [
        ('រូបមន្ត ' + M('m = \\dfrac{\\pi d^2}{4} \\cdot l \\cdot \\mu'), 1), ('ដែក ១០ លី ' + M('d = 0.01\\ \\text{m}') + ' ' + M('m \\approx 7.4\\ \\text{kg}'), 1), ('ដែក ១២ លី ' + M('d = 0.012\\ \\text{m}') + ' ' + M('m \\approx 10.7\\ \\text{kg}'), 1), ('ដែក ១៤ លី ' + M('d = 0.014\\ \\text{m}') + ' ' + M('m \\approx 14.5\\ \\text{kg}'), 1), ('បង្ហាញការជំនួស ' + M('\\dfrac{3.14 \\times 144\\times10^{-6}}{4} \\times 12 \\times 7874'), 1)]))
    C.append(wr('pisa', 'pisa', 'ពូសុខទិញដែក ' + M(6) + ' លី ' + M(200) + ' ដើម និងដែក ' + M(10) + ' លី ' + M(20) + ' ដើម ប្រវែង ' + M('12\\ \\text{m}') + ' ម្នាក់ៗ។ ដែក ' + M('1\\ \\text{kg}') + ' ថ្លៃ ' + M('2\\,800') + ' ៛ ម៉ាសមាឌ ' + M('7\\,874\\ \\text{kg/m}^3') + '។ គណនាប្រាក់ត្រូវចំណាយ (' + M('\\pi=3.14') + ')។', [
        ('ម៉ាសដែក ៦ លី ១ ដើម ' + M('\\dfrac{3.14 \\times 36\\times10^{-6}}{4} \\times 12 \\times 7874 \\approx 2.67\\ \\text{kg}'), 1), (M('200 \\times 2.670 = 534.04\\ \\text{kg}'), 1), ('ម៉ាសដែក ១០ លី ២០ ដើម ' + M('20 \\times 7.417 = 148.35\\ \\text{kg}'), 1), ('ម៉ាសសរុប ' + M('682.4\\ \\text{kg}'), 1), (M('682.4 \\times 2\\,800 \\approx 1\\,910\\,700') + ' ៛', 1)]))
    C.append(wr('pisa', 'pisa', 'ក្រដាសខ្នាតធំ ' + M('80\\ \\text{g/m}^2') + ' កាត់ជារ៉ាម ' + M('210\\ \\text{mm}\\times297\\ \\text{mm}') + ' (' + M(500) + ' សន្លឹក) ខាតចំនៀរ ' + M('4\\%') + ' (បន្ថែម ' + M('4\\%') + ' លើម៉ាសរ៉ាម)។ ក. រកម៉ាសរ៉ាម ១ ដុំ។ ខ. រកម៉ាសក្រដាសត្រូវការសម្រាប់ ១ រ៉ាម។', [
        ('ក. ' + M('500 \\times 0.06237 \\times 0.080 = 2.4948\\ \\text{kg}'), 2), ('ខ. ខាត ' + M('4\\%') + ' ' + M('2.4948 \\times 1.04'), 2), (M('= 2.594592\\ \\text{kg} \\approx 2.6\\ \\text{kg}'), 1)]))
    C.append(wr('pisa', 'pisa', 'សៀវភៅមួយក្បាល ' + M(100) + ' ទំព័រ ខ្នាត ' + M('148\\ \\text{mm}\\times210\\ \\text{mm}') + ' សាច់ក្នុងក្រដាស ' + M('70\\ \\text{g/m}^2') + ' (' + M(50) + ' សន្លឹក) ក្របក្រដាស ' + M('150\\ \\text{g/m}^2') + ' (សន្លឹក ១ ទំហំពីរទំព័រ)។ គណនាម៉ាសក្រដាសសរុបក្នុង ១ ក្បាល។', [
        ('ផ្ទៃក្រឡា ១ ទំព័រ ' + M('0.148 \\times 0.210 = 0.03108\\ \\text{m}^2'), 1), ('សាច់ក្នុង ' + M('50 \\times 0.03108 \\times 70 = 108.78\\ \\text{g}'), 2), ('ក្រប ' + M('2 \\times 0.03108 \\times 150 = 9.324\\ \\text{g}'), 1), (M('108.78 + 9.324 = 118.104\\ \\text{g}'), 1)]))
    C.append(wr('pisa', 'pisa', 'ក. ពពកមួយរសាត់ពីព្រះសីហនុមកភ្នំពេញ ចម្ងាយ ' + M('230\\ \\text{km}') + ' ខ្យល់ល្បឿន ' + M('6\\ \\text{m/s}') + '។ ប្តូរល្បឿនជា ' + M('\\text{km/h}') + ' រួចរករយៈពេល។', [
        ('ប្តូរល្បឿន ' + M('6\\ \\text{m/s} = 6 \\times 3.6 = 21.6\\ \\text{km/h}'), 2), ('រយៈពេល ' + M('t = \\dfrac{d}{v} = \\dfrac{230}{21.6} = \\dfrac{575}{54}\\ \\text{h}'), 1), (M('= 10\\dfrac{35}{54}\\ \\text{h} \\approx 10\\ \\text{h}\\ 39\\ \\text{mn}'), 2)]))
    return C

def with_img(q, s): q['img'] = s; return q
