"""Bank generator for Grade 12 Science — Lesson 18: មាសូលីតនិងប្រវែងធ្នូ."""
import math
import mpmath as mp
from lib import mcq, wr

LESSON = 'មាសូលីតនិងប្រវែងធ្នូ'
CHAPTER = 'ជំពូកទី 6 : អាំងតេក្រាល'
TARGET = {
    ('mcq', 'easy'): 10, ('mcq', 'medium'): 14, ('mcq', 'hard'): 7, ('mcq', 'pisa'): 5,
    ('writing', 'easy'): 1, ('writing', 'medium'): 4, ('writing', 'hard'): 4, ('writing', 'pisa'): 5,
}

S1 = '១. មាឌសូលីតបរិវត្តជុំវិញអ័ក្ស Ox'
S2 = '២. មាឌសូលីតបរិវត្តជុំវិញអ័ក្ស Oy'
S3 = '៣. ប្រវែងធ្នូនៃក្រាប'


def writing(level, sec, stem, ans, sol, bloom=None):
    return wr(level, sec, stem, [(sol, 3), (f'ចម្លើយ៖ {ans}', 2)], bloom=bloom)


def svg_solid_ox(pts, x0, x1, lbl='y = f(x)'):
    w, h = 240, 150
    ox, oy = 35, 80
    sx, sy = 36, 22
    top = ' '.join(f'{ox + x * sx:.1f},{oy - y * sy:.1f}' for x, y in pts)
    bot = ' '.join(f'{ox + x * sx:.1f},{oy + y * sy:.1f}' for x, y in reversed(pts))
    r_end = abs(pts[-1][1]) * sy
    return (
        f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg">'
        f'<line x1="15" y1="{oy}" x2="225" y2="{oy}" stroke="#4a5568" stroke-width="1.2"/>'
        f'<line x1="{ox}" y1="10" x2="{ox}" y2="142" stroke="#4a5568" stroke-width="1.2"/>'
        f'<polygon points="{top} {bot}" fill="#bee3f8" fill-opacity="0.65" stroke="none"/>'
        f'<polyline points="{top}" fill="none" stroke="#2b6cb0" stroke-width="2"/>'
        f'<polyline points="{bot}" fill="none" stroke="#2b6cb0" stroke-width="1.5" stroke-dasharray="3,2"/>'
        f'<ellipse cx="{ox + x1 * sx:.1f}" cy="{oy}" rx="7" ry="{max(r_end, 4):.1f}" fill="#90cdf4" fill-opacity="0.7" stroke="#2b6cb0" stroke-width="1.4"/>'
        f'<text x="218" y="{oy - 5}" font-size="11">x</text>'
        f'<text x="{ox + 5}" y="18" font-size="11">y</text>'
        f'<text x="145" y="22" font-size="10" fill="#2b6cb0">{lbl}</text>'
        f'</svg>'
    )


def svg_arc(pts, lbl='y = f(x)'):
    w, h = 240, 145
    ox, oy = 35, 118
    sx, sy = 38, 22
    pstr = ' '.join(f'{ox + x * sx:.1f},{oy - y * sy:.1f}' for x, y in pts)
    return (
        f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg">'
        f'<line x1="15" y1="{oy}" x2="225" y2="{oy}" stroke="#4a5568" stroke-width="1.2"/>'
        f'<line x1="{ox}" y1="10" x2="{ox}" y2="138" stroke="#4a5568" stroke-width="1.2"/>'
        f'<polyline points="{pstr}" fill="none" stroke="#c53030" stroke-width="2.2"/>'
        f'<text x="218" y="{oy - 5}" font-size="11">x</text>'
        f'<text x="{ox + 5}" y="18" font-size="11">y</text>'
        f'<text x="135" y="24" font-size="10" fill="#c53030">{lbl}</text>'
        f'</svg>'
    )


def build_candidates():
    qs = []

    # =========================================================================
    # MCQ EASY (10)
    # =========================================================================
    # 1 (Remember)
    qs.append(mcq(
        'easy', S1,
        'បើផ្ទៃខណ្ឌដោយក្រាប $y = f(x) \\ge 0$ អ័ក្ស $Ox$ និងបន្ទាត់ $x = a, x = b$ វិលជុំវិញអ័ក្ស $Ox$ តើមាឌសូលីតបរិវត្តកំណត់ដោយរូបមន្តណា?',
        r'$V = \pi \int_a^b [f(x)]^2 \, dx$',
        [r'$V = \int_a^b f(x) \, dx$', r'$V = 2\pi \int_a^b f(x) \, dx$', r'$V = \pi \int_a^b f(x) \, dx$'],
        'មាឌសូលីតបរិវត្តជុំវិញអ័ក្ស $Ox$ គឺ $V = \\pi \\int_a^b [f(x)]^2 \\, dx$។',
        bloom='Remember',
    ))

    # 2 (Remember)
    qs.append(mcq(
        'easy', S2,
        'បើផ្ទៃខណ្ឌដោយក្រាប $x = g(y)$ អ័ក្ស $Oy$ និងបន្ទាត់ដេក $y = c, y = d$ វិលជុំវិញអ័ក្ស $Oy$ តើមាឌសូលីតបរិវត្តស្មើនឹងអ្វី?',
        r'$V = \pi \int_c^d [g(y)]^2 \, dy$',
        [r'$V = \pi \int_c^d g(y) \, dy$', r'$V = 2\pi \int_c^d [g(y)]^2 \, dy$', r'$V = \int_c^d [g(y)]^2 \, dy$'],
        'រង្វិលជុំវិញអ័ក្ស $Oy$ ប្រើរូបមន្ត $V = \\pi \\int_c^d [g(y)]^2 \\, dy$។',
        bloom='Remember',
    ))

    # 3 (Remember)
    qs.append(mcq(
        'easy', S3,
        'តើប្រវែងធ្នូ $L$ នៃក្រាប $y = f(x)$ ពី $x = a$ ដល់ $x = b$ កំណត់ដោយរូបមន្តណា?',
        r'$L = \int_a^b \sqrt{1 + [f\'(x)]^2} \, dx$',
        [r'$L = \int_a^b \sqrt{1 + [f(x)]^2} \, dx$', r'$L = \int_a^b (1 + [f\'(x)]^2) \, dx$', r'$L = \pi \int_a^b \sqrt{1 + [f\'(x)]^2} \, dx$'],
        'រូបមន្តប្រវែងធ្នូគឺ $L = \\int_a^b \\sqrt{1 + [f\'(x)]^2} \\, dx$។',
        bloom='Remember',
    ))

    # 4 (Understand)
    qs.append(mcq(
        'easy', S1,
        'មុខកាត់ឈរកាត់តាម $x$ នៃសូលីតបរិវត្តជុំវិញអ័ក្ស $Ox$ ក្រោមក្រាប $y = f(x)$ មានរាងជាថាសកាំ $R = f(x)$ ។ តើផ្ទៃក្រឡាមុខកាត់ $\\mathcal{A}(x)$ ស្មើនឹងអ្វី?',
        r'$\pi [f(x)]^2$',
        [r'$2\pi f(x)$', r'$\pi f(x)$', r'$[f(x)]^2$'],
        'ថាសកាំ $f(x)$ មានផ្ទៃក្រឡា $\\mathcal{A}(x) = \\pi R^2 = \\pi [f(x)]^2$។',
        bloom='Understand',
    ))

    # 5 (Apply)
    svg5 = svg_solid_ox([(0.25 * i, 2) for i in range(13)], 0, 3, 'y = 2')
    qs.append(mcq(
        'easy', S1,
        f'គណនាមាឌសូលីតបរិវត្តដែលបានពីរង្វិលផ្ទៃក្រឡាខណ្ឌដោយ $y = 2$, $Ox$ និង $x = 0, x = 3$ ជុំវិញអ័ក្ស $Ox$ ។<br/>{svg5}',
        r'$12\pi$',
        [r'$6\pi$', r'$4\pi$', r'$24\pi$'],
        '$V = \\pi \\int_0^3 2^2 \\, dx = \\pi [4x]_0^3 = 12\\pi$។',
        bloom='Apply',
    ))

    # 6 (Apply)
    qs.append(mcq(
        'easy', S1,
        'គណនាមាឌសូលីតបរិវត្តកំណត់បានពីរង្វិលជុំវិញអ័ក្ស $Ox$ នៃផ្ទៃខណ្ឌដោយ $y = x$, $Ox$ លើ $[0, 3]$ ។',
        r'$9\pi$',
        [r'$3\pi$', r'$\frac{9\pi}{2}$', r'$27\pi$'],
        '$V = \\pi \\int_0^3 x^2 \\, dx = \\pi \\left[\\frac{x^3}{3}\\right]_0^3 = 9\\pi$។',
        bloom='Apply',
    ))

    # 7 (Apply)
    qs.append(mcq(
        'easy', S1,
        'គណនាមាឌសូលីតបរិវត្តកំណត់បានពីរង្វិលជុំវិញអ័ក្ស $Ox$ នៃផ្ទៃខណ្ឌដោយ $y = \\sqrt{x}$, $Ox$ លើ $[0, 4]$ ។',
        r'$8\pi$',
        [r'$4\pi$', r'$16\pi$', r'$\frac{16\pi}{3}$'],
        '$V = \\pi \\int_0^4 (\\sqrt{x})^2 \\, dx = \\pi \\int_0^4 x \\, dx = \\pi \\left[\\frac{x^2}{2}\\right]_0^4 = 8\\pi$។',
        bloom='Apply',
    ))

    # 8 (Apply)
    qs.append(mcq(
        'easy', S3,
        'គណនាប្រវែងធ្នូនៃបន្ទាត់ $y = 3x + 1$ លើចន្លោះ $[0, 2]$ ។',
        r'$2\sqrt{10}$',
        [r'$\sqrt{10}$', r'$6$', r'$2\sqrt{5}$'],
        '$y\' = 3 \\implies L = \\int_0^2 \\sqrt{1 + 3^2}\\,dx = 2\\sqrt{10}$។',
        bloom='Apply',
    ))

    # 9 (Understand)
    qs.append(mcq(
        'easy', S1,
        'បើផ្ទៃនៅចន្លោះក្រាបពីរ $f(x) \\ge g(x) \\ge 0$ លើ $[a, b]$ វិលជុំវិញអ័ក្ស $Ox$ តើមាឌសូលីតបរិវត្តស្មើនឹងអ្វី?',
        r'$\pi \int_a^b \left([f(x)]^2 - [g(x)]^2\right)dx$',
        [r'$\pi \int_a^b [f(x) - g(x)]^2 \, dx$', r'$\pi \int_a^b (f(x) - g(x)) \, dx$', r'$\pi \int_a^b \left([g(x)]^2 - [f(x)]^2\right)dx$'],
        'មាឌចន្លោះក្រាបពីរគឺ $V = V_{\\text{ក្រៅ}} - V_{\\text{ក្នុង}} = \\pi\\int_a^b ([f(x)]^2 - [g(x)]^2)\\,dx$។',
        bloom='Understand',
    ))

    # 10 (Apply)
    qs.append(mcq(
        'easy', S2,
        'គណនាមាឌសូលីតបរិវត្តកំណត់បានពីរង្វិលជុំវិញអ័ក្ស $Oy$ នៃផ្ទៃខណ្ឌដោយ $x = \\sqrt{y}$, $Oy$ លើ $[0, 2]$ ។',
        r'$2\pi$',
        [r'$4\pi$', r'$\pi$', r'$\frac{8\pi}{3}$'],
        '$V = \\pi \\int_0^2 (\\sqrt{y})^2 \\, dy = \\pi \\int_0^2 y \\, dy = 2\\pi$។',
        bloom='Apply',
    ))

    # =========================================================================
    # MCQ MEDIUM (14)
    # =========================================================================
    # 11 (Apply) - y = x^2 on [0, 2] around Ox
    qs.append(mcq(
        'medium', S1,
        'គណនាមាឌសូលីតបរិវត្តកំណត់បានពីរង្វិលជុំវិញអ័ក្ស $Ox$ នៃផ្ទៃខណ្ឌដោយ $y = x^2$, $Ox$ លើ $[0, 2]$ ។',
        r'$\frac{32\pi}{5}$',
        [r'$\frac{16\pi}{5}$', r'$\frac{8\pi}{3}$', r'$8\pi$'],
        '$V = \\pi \\int_0^2 (x^2)^2 \\, dx = \\pi \\left[\\frac{x^5}{5}\\right]_0^2 = \\frac{32\\pi}{5}$។',
        bloom='Apply',
    ))

    # 12 (Apply) - y = 2x + 1 on [1, 3] around Ox -> 158*pi/3
    qs.append(mcq(
        'medium', S1,
        'គណនាមាឌសូលីតបរិវត្តកំណត់បានពីរង្វិលជុំវិញអ័ក្ស $Ox$ នៃផ្ទៃខណ្ឌដោយ $y = 2x + 1$, $Ox$ និង $x = 1, x = 3$ ។',
        r'$\frac{158\pi}{3}$',
        [r'$\frac{152\pi}{3}$', r'$52\pi$', r'$\frac{343\pi}{6}$'],
        '$V = \\pi \\int_1^3 (2x+1)^2\\,dx = \\pi \\left[\\frac{(2x+1)^3}{6}\\right]_1^3 = \\frac{343 - 27}{6}\\pi = \\frac{158\\pi}{3}$។',
        bloom='Apply',
    ))

    # 13 (Apply) - y = sqrt(x - 3) on [4, 9] around Ox -> 35*pi/2
    qs.append(mcq(
        'medium', S1,
        'គណនាមាឌសូលីតបរិវត្តកំណត់បានពីរង្វិលជុំវិញអ័ក្ស $Ox$ នៃផ្ទៃខណ្ឌដោយ $y = \\sqrt{x - 3}$, $Ox$ ពី $x = 4$ ទៅ $x = 9$ ។',
        r'$\frac{35\pi}{2}$',
        [r'$18\pi$', r'$\frac{25\pi}{2}$', r'$15\pi$'],
        '$V = \\pi \\int_4^9 (x - 3)\\,dx = \\pi \\left[\\frac{(x-3)^2}{2}\\right]_4^9 = \\pi\\left(18 - \\frac{1}{2}\\right) = \\frac{35\\pi}{2}$។',
        bloom='Apply',
    ))

    # 14 (Apply) - y = e^x on [0, 1] around Ox
    qs.append(mcq(
        'medium', S1,
        'គណនាមាឌសូលីតបរិវត្តកំណត់បានពីរង្វិលជុំវិញអ័ក្ស $Ox$ នៃផ្ទៃខណ្ឌដោយ $y = e^x$, $Ox$ លើ $[0, 1]$ ។',
        r'$\frac{\pi}{2}(e^2 - 1)$',
        [r'$\pi(e^2 - 1)$', r'$\pi(e - 1)$', r'$\frac{\pi}{2}e^2$'],
        '$V = \\pi \\int_0^1 e^{2x}\\,dx = \\pi \\left[\\frac{e^{2x}}{2}\\right]_0^1 = \\frac{\\pi}{2}(e^2 - 1)$។',
        bloom='Apply',
    ))

    # 15 (Apply) - two curves y = sqrt(x) and y = x^2 around Ox -> 3*pi/10
    qs.append(mcq(
        'medium', S1,
        'គណនាមាឌសូលីតបរិវត្តកំណត់បានពីរង្វិលជុំវិញអ័ក្ស $Ox$ នៃផ្ទៃខណ្ឌដោយ $f(x) = \\sqrt{x}$ និង $g(x) = x^2$ លើ $[0, 1]$ ។',
        r'$\frac{3\pi}{10}$',
        [r'$\frac{7\pi}{10}$', r'$\frac{\pi}{3}$', r'$\frac{\pi}{5}$'],
        '$V = \\pi \\int_0^1 (x - x^4)\\,dx = \\pi \\left(\\frac{1}{2} - \\frac{1}{5}\\right) = \\frac{3\\pi}{10}$។',
        bloom='Apply',
    ))

    # 16 (Apply) - two curves y = x^2 and y = 4x - x^2 around Ox -> 32*pi/3
    qs.append(mcq(
        'medium', S1,
        'គណនាមាឌសូលីតបរិវត្តកំណត់បានពីរង្វិលជុំវិញអ័ក្ស $Ox$ នៃផ្ទៃខណ្ឌដោយ $f(x) = x^2$ និង $g(x) = 4x - x^2$ ។',
        r'$\frac{32\pi}{3}$',
        [r'$\frac{16\pi}{3}$', r'$\frac{64\pi}{3}$', r'$8\pi$'],
        'ចំណុចប្រសព្វគឺ $x = 0, 2$ ។ $V = \\pi \\int_0^2 [(4x-x^2)^2 - x^4]\\,dx = \\pi \\int_0^2 (16x^2 - 8x^3)\\,dx = \\frac{32\\pi}{3}$។',
        bloom='Apply',
    ))

    # 17 (Apply) - Oy rotation: y = sqrt(3 - x) on [0, sqrt(3)] -> 24*pi*sqrt(3)/5
    qs.append(mcq(
        'medium', S2,
        'គណនាមាឌសូលីតបរិវត្តកំណត់បានពីរង្វិលជុំវិញអ័ក្ស $Oy$ នៃផ្ទៃខណ្ឌដោយ $y = \\sqrt{3 - x}$, $Oy$ និង $Ox$ លើ $0 \\le y \\le \\sqrt{3}$ ។',
        r'$\frac{24\pi\sqrt{3}}{5}$',
        [r'$\frac{12\pi\sqrt{3}}{5}$', r'$\frac{9\pi\sqrt{3}}{5}$', r'$3\pi\sqrt{3}$'],
        '$x = 3 - y^2 \\implies V = \\pi \\int_0^{\\sqrt{3}} (3 - y^2)^2\\,dy = \\pi \\left[9y - 2y^3 + \\frac{y^5}{5}\\right]_0^{\\sqrt{3}} = \\frac{24\\pi\\sqrt{3}}{5}$។',
        bloom='Apply',
    ))

    # 18 (Apply) - Oy rotation: y = x^2 on [0, 4] -> x = sqrt(y), pi * int_0^4 y dy = 8*pi
    qs.append(mcq(
        'medium', S2,
        'គណនាមាឌសូលីតបរិវត្តកំណត់បានពីរង្វិលជុំវិញអ័ក្ស $Oy$ នៃផ្ទៃខណ្ឌដោយប៉ារ៉ាបូល $y = x^2$ ($x \\ge 0$) អ័ក្ស $Oy$ និងបន្ទាត់ $y = 4$ ។',
        r'$8\pi$',
        [r'$4\pi$', r'$16\pi$', r'$\frac{32\pi}{5}$'],
        '$x = \\sqrt{y} \\implies V = \\pi \\int_0^4 (\\sqrt{y})^2\\,dy = \\pi \\left[\\frac{y^2}{2}\\right]_0^4 = 8\\pi$។',
        bloom='Apply',
    ))

    # 19 (Apply) - Oy rotation: y = x^3 on [0, 8] -> x = y^{1/3}, pi * int_0^8 y^{2/3} dy = pi * [3/5 y^{5/3}]_0^8 = 96*pi/5
    qs.append(mcq(
        'medium', S2,
        'គណនាមាឌសូលីតបរិវត្តកំណត់បានពីរង្វិលជុំវិញអ័ក្ស $Oy$ នៃផ្ទៃខណ្ឌដោយ $y = x^3$, $Oy$ និង $y = 8$ ។',
        r'$\frac{96\pi}{5}$',
        [r'$\frac{64\pi}{5}$', r'$\frac{48\pi}{5}$', r'$16\pi$'],
        '$x = y^{1/3} \\implies V = \\pi \\int_0^8 y^{2/3}\\,dy = \\pi \\left[\\frac{3}{5}y^{5/3}\\right]_0^8 = \\frac{3}{5}(32)\\pi = \\frac{96\\pi}{5}$។',
        bloom='Apply',
    ))

    # 20 (Apply) - arc length y = 4*sqrt(2)/3 * x^{3/2} - 1 on [0, 1] -> 13/6
    svg20 = svg_arc([(0.2 * i, 1.8856 * (0.2 * i)**1.5 - 1) for i in range(6)], 'y = (4√2/3)x^{3/2} - 1')
    qs.append(mcq(
        'medium', S3,
        f'គណនាប្រវែងធ្នូនៃក្រាប $y = \\frac{{4\\sqrt{{2}}}}{{3}}x^{{\\frac{{3}}{{2}}}} - 1$ នៅចន្លោះ $x = 0$ និង $x = 1$ ។<br/>{svg20}',
        r'$\frac{13}{6}$',
        [r'$\frac{13}{3}$', r'$\frac{7}{6}$', r'$\frac{9}{4}$'],
        '$y\' = 2\\sqrt{2}\\sqrt{x} \\implies 1 + (y\')^2 = 1 + 8x$ ។ $L = \\int_0^1 \\sqrt{1 + 8x}\\,dx = \\frac{1}{12}(27 - 1) = \\frac{13}{6}$។',
        bloom='Apply',
    ))

    # 21 (Apply) - arc length y = 2/3 * x^{3/2} on [0, 3] -> y' = sqrt(x), int_0^3 sqrt(1+x) dx = 2/3*(8 - 1) = 14/3
    qs.append(mcq(
        'medium', S3,
        'គណនាប្រវែងធ្នូនៃក្រាប $y = \\frac{2}{3}x^{\\frac{3}{2}}$ ពី $x = 0$ ដល់ $x = 3$ ។',
        r'$\frac{14}{3}$',
        [r'$\frac{16}{3}$', r'$4$', r'$\frac{7}{3}$'],
        '$y\' = \\sqrt{x} \\implies L = \\int_0^3 \\sqrt{1 + x}\\,dx = \\left[\\frac{2}{3}(1+x)^{3/2}\\right]_0^3 = \\frac{2}{3}(8 - 1) = \\frac{14}{3}$។',
        bloom='Apply',
    ))

    # 22 (Apply) - arc length y = 1/3 * (x^2 + 2)^{3/2} on [0, 3] -> 12
    qs.append(mcq(
        'medium', S3,
        'គណនាប្រវែងធ្នូនៃក្រាប $y = \\frac{1}{3}(x^2 + 2)^{\\frac{3}{2}}$ ពី $x = 0$ ដល់ $x = 3$ ។',
        r'$12$',
        [r'$6$', r'$9$', r'$15$'],
        '$y\' = x\\sqrt{x^2 + 2} \\implies 1 + (y\')^2 = (x^2 + 1)^2$ ។ $L = \\int_0^3 (x^2 + 1)\\,dx = \\left[\\frac{x^3}{3} + x\\right]_0^3 = 9 + 3 = 12$។',
        bloom='Apply',
    ))

    # 23 (Analyze) - y = 1/cos x on [0, pi/4] around Ox -> pi * int_0^{pi/4} sec^2 x dx = pi * [tan x]_0^{pi/4} = pi
    qs.append(mcq(
        'medium', S1,
        'គណនាមាឌសូលីតបរិវត្តកំណត់បានពីរង្វិលជុំវិញអ័ក្ស $Ox$ នៃផ្ទៃខណ្ឌដោយក្រាប $y = \\frac{1}{\\cos x}$ អ័ក្ស $Ox$ និង $x = 0, x = \\frac{\\pi}{4}$ ។',
        r'$\pi$',
        [r'$\frac{\pi}{2}$', r'$2\pi$', r'$\frac{\pi}{4}$'],
        '$V = \\pi \\int_0^{\\pi/4} \\frac{1}{\\cos^2 x}\\,dx = \\pi [\\tan x]_0^{\\pi/4} = \\pi$។',
        bloom='Analyze',
    ))

    # 24 (Analyze) - cone volume from y = (r/h)x on [0, h] around Ox -> 1/3 pi r^2 h
    qs.append(mcq(
        'medium', S1,
        'ផ្ទៃត្រីកោណខណ្ឌដោយបន្ទាត់ $y = \\frac{r}{h}x$, $Ox$ និង $x = h$ ($r, h > 0$) វិលជុំវិញអ័ក្ស $Ox$ បង្កើតបានជាកោណ។ តើមាឌកោណនោះស្មើនឹងអ្វី?',
        r'$\frac{1}{3}\pi r^2 h$',
        [r'$\pi r^2 h$', r'$\frac{1}{2}\pi r^2 h$', r'$\frac{2}{3}\pi r^2 h$'],
        '$V = \\pi \\int_0^h \\frac{r^2}{h^2}x^2\\,dx = \\pi \\frac{r^2}{h^2}\\cdot \\frac{h^3}{3} = \\frac{1}{3}\\pi r^2 h$។',
        bloom='Analyze',
    ))

    # =========================================================================
    # MCQ HARD (7)
    # =========================================================================
    # 25 (Analyze) - y = x^2 + 1 on [0, 3] around Ox -> 348*pi/5
    qs.append(mcq(
        'hard', S1,
        'គណនាមាឌសូលីតបរិវត្តកំណត់បានពីរង្វិលជុំវិញអ័ក្ស $Ox$ នៃផ្ទៃខណ្ឌដោយ $y = x^2 + 1$, $Ox$ លើ $[0, 3]$ ។',
        r'$\frac{348\pi}{5}$',
        [r'$\frac{243\pi}{5}$', r'$\frac{318\pi}{5}$', r'$70\pi$'],
        '$V = \\pi \\int_0^3 (x^4 + 2x^2 + 1)\\,dx = \\pi\\left(\\frac{243}{5} + 18 + 3\\right) = \\frac{348\\pi}{5}$។',
        bloom='Analyze',
    ))

    # 26 (Analyze) - y = 4 - x^2 and y = 2 - x on [-1, 2] around Ox -> 108*pi/5
    qs.append(mcq(
        'hard', S1,
        'គណនាមាឌសូលីតបរិវត្តកំណត់បានពីរង្វិលជុំវិញអ័ក្ស $Ox$ នៃផ្ទៃខណ្ឌដោយ $f(x) = 4 - x^2$ និង $g(x) = 2 - x$ លើ $[-1, 2]$ ។',
        r'$\frac{108\pi}{5}$',
        [r'$\frac{54\pi}{5}$', r'$\frac{108\pi}{3}$', r'$21\pi$'],
        '$V = \\pi \\int_{-1}^2 [(4-x^2)^2 - (2-x)^2]\\,dx = \\frac{108\\pi}{5}$។',
        bloom='Analyze',
    ))

    # 27 (Analyze) - arc length y = x^3/3 + 1/(4x) on [1, 3] -> 53/6
    qs.append(mcq(
        'hard', S3,
        'គណនាប្រវែងធ្នូនៃក្រាប $y = \\frac{x^3}{3} + \\frac{1}{4x}$ ពី $x = 1$ ទៅ $x = 3$ ។',
        r'$\frac{53}{6}$',
        [r'$\frac{55}{6}$', r'$\frac{26}{3}$', r'$9$'],
        '$y\' = x^2 - \\frac{1}{4x^2} \\implies 1 + (y\')^2 = \\left(x^2 + \\frac{1}{4x^2}\\right)^2$ ។ $L = \\int_1^3 \\left(x^2 + \\frac{1}{4x^2}\\right)dx = \\frac{53}{6}$។',
        bloom='Analyze',
    ))

    # 28 (Evaluate) - find a > 5/9 such that arc length of y = x^{3/2} on [5/9, a] is 7 -> a = 32/9
    qs.append(mcq(
        'hard', S3,
        'តាង $L(a)$ ជាប្រវែងធ្នូនៃក្រាប $y = x^{\\frac{3}{2}}$ ពី $x = \\frac{5}{9}$ ដល់ $x = a$ ($a \\ge \\frac{5}{9}$) ។ បើ $L(a) = 7$ តើ $a$ ស្មើនឹងប៉ុន្មាន?',
        r'$\frac{32}{9}$',
        [r'$\frac{16}{9}$', r'$4$', r'$\frac{28}{9}$'],
        '$L(a) = \\frac{8}{27}\\left(1 + \\frac{9}{4}a\\right)^{3/2} - 1 = 7 \\implies \\left(1 + \\frac{9}{4}a\\right)^{3/2} = 27 \\implies 1 + \\frac{9}{4}a = 9 \\implies a = \\frac{32}{9}$។',
        bloom='Evaluate',
    ))

    # 29 (Analyze) - y = e^x and tangent at (1, e): y = ex on [0, 1] around Ox -> (e^2 - 3)/6 * pi
    qs.append(mcq(
        'hard', S1,
        'គណនាមាឌសូលីតបរិវត្តកំណត់បានពីរង្វិលជុំវិញអ័ក្ស $Ox$ នៃផ្ទៃខណ្ឌដោយក្រាប $y = e^x$ និងបន្ទាត់ប៉ះ $y = ex$ លើ $[0, 1]$ ។',
        r'$\frac{e^2 - 3}{6}\pi$',
        [r'$\frac{e^2 - 1}{2}\pi$', r'$\frac{e^2 - 3}{3}\pi$', r'$\frac{e^2 - 2}{6}\pi$'],
        '$V = \\pi \\int_0^1 (e^{2x} - e^2 x^2)\\,dx = \\pi\\left[\\frac{e^{2x}}{2} - \\frac{e^2 x^3}{3}\\right]_0^1 = \\pi\\left(\\frac{e^2}{6} - \\frac{1}{2}\\right) = \\frac{e^2 - 3}{6}\\pi$។',
        bloom='Analyze',
    ))

    # 30 (Analyze) - y = ln x on [0, 1] around Oy -> x = e^y, V = pi * int_0^1 e^{2y} dy = pi/2*(e^2 - 1)
    qs.append(mcq(
        'hard', S2,
        'គណនាមាឌសូលីតបរិវត្តកំណត់បានពីរង្វិលជុំវិញអ័ក្ស $Oy$ នៃផ្ទៃខណ្ឌដោយក្រាប $y = \\ln x$, អ័ក្ស $Oy$ និងបន្ទាត់ $y = 0, y = 1$ ។',
        r'$\frac{\pi}{2}(e^2 - 1)$',
        [r'$\pi(e - 1)$', r'$\pi(e^2 - 1)$', r'$\frac{\pi}{2}(e - 1)$'],
        '$y = \\ln x \\iff x = e^y$ ។ $V = \\pi \\int_0^1 (e^y)^2\\,dy = \\frac{\\pi}{2}(e^2 - 1)$។',
        bloom='Analyze',
    ))

    # 31 (Evaluate) - hemisphere / bowl with y = sqrt(25 - x^2) on [0, 5] around Oy -> x^2 = 25 - y^2, V = pi * int_0^5 (25-y^2) dy = 250*pi/3
    qs.append(mcq(
        'hard', S2,
        'ផ្ទៃខណ្ឌដោយខ្សែកោង $y = \\sqrt{25 - x^2}$ ($x \\ge 0$) អ័ក្ស $Ox$ និង $Oy$ វិលជុំវិញអ័ក្ស $Oy$ បង្កើតបានជាកន្លះស្វ៊ែរ។ គណនាមាឌរបស់វា។',
        r'$\frac{250\pi}{3}$',
        [r'$\frac{500\pi}{3}$', r'$\frac{125\pi}{3}$', r'$125\pi$'],
        '$x^2 = 25 - y^2 \\implies V = \\pi \\int_0^5 (25 - y^2)\\,dy = \\pi\\left(125 - \\frac{125}{3}\\right) = \\frac{250\\pi}{3}$។',
        bloom='Evaluate',
    ))

    # =========================================================================
    # MCQ PISA (5)
    # =========================================================================
    # 32 (Apply) - PISA: Vase shaped by y = 2 + sin(x) or simpler y = 1 + x/2 on [0, 4] around Ox (frustum)
    # pi * int_0^4 (1 + x/2)^2 dx = pi * [2/3 * (1 + x/2)^3]_0^4 = 2*pi/3 * (27 - 1) = 52*pi/3
    qs.append(mcq(
        'pisa', S1,
        'ថូផ្កាមួយរាងជាកោណកាត់ ដែលបង្កើតពីរង្វិលបន្ទាត់ $y = 1 + \\frac{x}{2}$ ($0 \\le x \\le 4$, គិតជា $\\text{dm}$) ជុំវិញអ័ក្ស $Ox$ ។ តើថូផ្កានេះមានចំណុះប៉ុន្មានលីត្រ ($1\\,\\text{dm}^3 = 1\\,\\text{L}$)?',
        r'$\frac{52\pi}{3}\,\text{L}$',
        [r'$\frac{26\pi}{3}\,\text{L}$', r'$18\pi\,\text{L}$', r'$\frac{54\pi}{3}\,\text{L}$'],
        '$V = \\pi \\int_0^4 \\left(1 + \\frac{x}{2}\\right)^2 dx = \\frac{2\\pi}{3}\\left[\\left(1+\\frac{x}{2}\\right)^3\\right]_0^4 = \\frac{52\\pi}{3}\\,\\text{L}$។',
        bloom='Apply',
    ))

    # 33 (Analyze) - PISA: Parabolic bowl y = x^2 (m) filled to height y = 2 around Oy -> pi * int_0^2 y dy = 2*pi m^3
    qs.append(mcq(
        'pisa', S2,
        'អាងទឹករាងប៉ារ៉ាបូលូអ៊ីតបង្កើតពីរង្វិលក្រាប $y = x^2$ ជុំវិញអ័ក្ស $Oy$ (គិតជាម៉ែត្រ) ។ បើចាក់ទឹកពេញដល់កម្ពស់ $y = 2\\,\\text{m}$ តើមាឌទឹកក្នុងអាងស្មើនឹងប៉ុន្មាន?',
        r'$2\pi\,\text{m}^3$',
        [r'$4\pi\,\text{m}^3$', r'$\pi\,\text{m}^3$', r'$\frac{8\pi}{3}\,\text{m}^3$'],
        '$x^2 = y \\implies V = \\pi \\int_0^2 y\\,dy = \\pi \\left[\\frac{y^2}{2}\\right]_0^2 = 2\\pi\\,\\text{m}^3$។',
        bloom='Analyze',
    ))

    # 34 (Analyze) - PISA: Suspension bridge cable approximated by y = 2/3 * x^{3/2} on [0, 8] (units in 10m)
    # L = [2/3 * (1+x)^{3/2}]_0^8 = 2/3*(27 - 1) = 52/3
    qs.append(mcq(
        'pisa', S3,
        'ខ្សែរ៉កកោងមួយមានរាងតាមសមីការ $y = \\frac{2}{3}x^{\\frac{3}{2}}$ លើ $[0, 8]$ (គិតជាម៉ែត្រ) ។ គណនាប្រវែងសរុបនៃខ្សែរ៉កនេះ។',
        r'$\frac{52}{3}\,\text{m}$',
        [r'$\frac{26}{3}\,\text{m}$', r'$18\,\text{m}$', r'$\frac{54}{3}\,\text{m}$'],
        '$y\' = \\sqrt{x} \\implies L = \\int_0^8 \\sqrt{1 + x}\\,dx = \\frac{2}{3}(9^{3/2} - 1) = \\frac{52}{3}\\,\\text{m}$។',
        bloom='Analyze',
    ))

    # 35 (Evaluate) - PISA: Comparing cylinder vs cone vs paraboloid of same base radius R and height H
    # V_cyl = pi R^2 H, V_parab = 1/2 pi R^2 H, V_cone = 1/3 pi R^2 H
    qs.append(mcq(
        'pisa', S1,
        'កែវរាងស៊ីឡាំង កែវរាងប៉ារ៉ាបូលូអ៊ីត ($y = R\\sqrt{x/H}$) និងកែវរាងកោណ ($y = Rx/H$) មានកាំមាត់ $R$ និងកម្ពស់ $H$ ដូចគ្នា។ តើផលធៀបមាឌ $V_{\\text{ស៊ីឡាំង}} : V_{\\text{ប៉ារ៉ាបូលូអ៊ីត}} : V_{\\text{កោណ}}$ ស្មើនឹងប៉ុន្មាន?',
        r'$6 : 3 : 2$',
        [r'$3 : 2 : 1$', r'$4 : 2 : 1$', r'$6 : 4 : 2$'],
        '$V_{\\text{ស៊ីឡាំង}} = \\pi R^2 H$, $V_{\\text{ប៉ារ៉ា}} = \\frac{1}{2}\\pi R^2 H$, $V_{\\text{កោណ}} = \\frac{1}{3}\\pi R^2 H$ ។ គុណនឹង $6$ បាន $6 : 3 : 2$។',
        bloom='Evaluate',
    ))

    # 36 (Create) - PISA: Water height h in paraboloid y = x^2 around Oy so volume is half of full height y = 4
    # Full V = 8*pi -> half V = 4*pi -> pi * h^2 / 2 = 4*pi -> h^2 = 8 -> h = 2*sqrt(2)
    qs.append(mcq(
        'pisa', S2,
        'ពែងរាងប៉ារ៉ាបូលូអ៊ីត $y = x^2$ ជុំវិញអ័ក្ស $Oy$ មានកម្ពស់ពេញ $y = 4$ ។ តើត្រូវចាក់ទឹកដល់កម្ពស់ $y = h$ ប៉ុន្មានដើម្បីឲ្យបានមាឌទឹកស្មើពាក់កណ្តាលនៃមាឌពេញ?',
        r'$2\sqrt{2}$',
        [r'$2$', r'$\sqrt{2}$', r'$3$'],
        'មាឌពេញគឺ $\\pi\\int_0^4 y\\,dy = 8\\pi$ ។ ពាក់កណ្តាលគឺ $4\\pi = \\pi\\int_0^h y\\,dy = \\frac{\\pi h^2}{2} \\implies h^2 = 8 \\implies h = 2\\sqrt{2}$។',
        bloom='Create',
    ))

    # =========================================================================
    # WRITING (14): 1 easy, 4 medium, 4 hard, 5 pisa
    # =========================================================================
    # 37 (Easy - Apply)
    qs.append(writing(
        'easy', S1,
        'គណនាមាឌសូលីតបរិវត្តកំណត់បានពីរង្វិលជុំវិញអ័ក្ស $Ox$ នៃផ្ទៃខណ្ឌដោយក្រាប $y = 3x$ អ័ក្ស $Ox$ និងបន្ទាត់ $x = 0, x = 2$ ។',
        r'$24\pi$',
        '$V = \\pi \\int_0^2 (3x)^2\\,dx = \\pi \\int_0^2 9x^2\\,dx = \\pi [3x^3]_0^2 = 24\\pi$។',
        bloom='Apply',
    ))

    # 38 (Medium - Apply)
    # y = 4 - x^2 on [-2, 2] around Ox -> 512*pi/15
    qs.append(writing(
        'medium', S1,
        'គណនាមាឌសូលីតបរិវត្តកំណត់បានពីរង្វិលជុំវិញអ័ក្ស $Ox$ នៃផ្ទៃខណ្ឌដោយ $y = 4 - x^2$ និងអ័ក្ស $Ox$ លើ $[-2, 2]$ ។',
        r'$\frac{512\pi}{15}$',
        '$V = \\pi \\int_{-2}^2 (4 - x^2)^2\\,dx = 2\\pi \\int_0^2 (16 - 8x^2 + x^4)\\,dx = 2\\pi\\left(32 - \\frac{64}{3} + \\frac{32}{5}\\right) = \\frac{512\\pi}{15}$។',
        bloom='Apply',
    ))

    # 39 (Medium - Apply)
    # y = x^2 - 2x + 3 and y = 9 - x around Ox -> 250*pi
    qs.append(writing(
        'medium', S1,
        'គណនាមាឌសូលីតបរិវត្តកំណត់បានពីរង្វិលជុំវិញអ័ក្ស $Ox$ នៃផ្ទៃខណ្ឌដោយ $f(x) = x^2 - 2x + 3$ និង $g(x) = 9 - x$ ។',
        r'$250\pi$',
        'ចំណុចប្រសព្វគឺ $x = -2, 3$ ។ $V = \\pi \\int_{-2}^3 [(9-x)^2 - (x^2-2x+3)^2]\\,dx = 250\\pi$។',
        bloom='Apply',
    ))

    # 40 (Medium - Apply)
    # Oy rotation: x = 2*sqrt(y) on [0, 3] -> V = pi * int_0^3 4y dy = 18*pi
    qs.append(writing(
        'medium', S2,
        'គណនាមាឌសូលីតបរិវត្តកំណត់បានពីរង្វិលជុំវិញអ័ក្ស $Oy$ នៃផ្ទៃខណ្ឌដោយក្រាប $y = \\frac{x^2}{4}$ ($x \\ge 0$) អ័ក្ស $Oy$ និងបន្ទាត់ $y = 3$ ។',
        r'$18\pi$',
        '$x^2 = 4y \\implies V = \\pi \\int_0^3 4y\\,dy = \\pi [2y^2]_0^3 = 18\\pi$។',
        bloom='Apply',
    ))

    # 41 (Medium - Apply)
    # arc length y = 2/3 * (x - 1)^{3/2} on [1, 4] -> y' = sqrt(x-1), int_1^4 sqrt(x) dx = 2/3*(8 - 1) = 14/3
    qs.append(writing(
        'medium', S3,
        'គណនាប្រវែងធ្នូនៃក្រាប $y = \\frac{2}{3}(x - 1)^{\\frac{3}{2}}$ ពី $x = 1$ ទៅ $x = 4$ ។',
        r'$\frac{14}{3}$',
        '$y\' = \\sqrt{x - 1} \\implies 1 + (y\')^2 = x$ ។ $L = \\int_1^4 \\sqrt{x}\\,dx = \\left[\\frac{2}{3}x^{3/2}\\right]_1^4 = \\frac{14}{3}$។',
        bloom='Apply',
    ))

    # 42 (Hard - Analyze)
    # y = x^2 + 1 and y = -x + 3 on [-2, 1] around Ox -> 351*pi/15 = 117*pi/5
    qs.append(writing(
        'hard', S1,
        'គណនាមាឌសូលីតបរិវត្តកំណត់បានពីរង្វិលជុំវិញអ័ក្ស $Ox$ នៃផ្ទៃខណ្ឌដោយ $f(x) = x^2 + 1$ និង $g(x) = -x + 3$ លើ $[-2, 1]$ ។',
        r'$\frac{117\pi}{5}$',
        '$V = \\pi \\int_{-2}^1 [(-x+3)^2 - (x^2+1)^2]\\,dx = \\frac{351\\pi}{15} = \\frac{117\\pi}{5}$។',
        bloom='Analyze',
    ))

    # 43 (Hard - Analyze)
    # arc length y = x^4/8 + 1/(4x^2) on [1, 2] -> y' = x^3/2 - 1/(2x^3), 1 + (y')^2 = (x^3/2 + 1/(2x^3))^2
    # int_1^2 (x^3/2 + 1/(2x^3)) dx = [x^4/8 - 1/(4x^2)]_1^2 = (2 - 1/16) - (1/8 - 1/4) = 31/16 + 1/8 = 33/16
    qs.append(writing(
        'hard', S3,
        'គណនាប្រវែងធ្នូនៃក្រាប $y = \\frac{x^4}{8} + \\frac{1}{4x^2}$ ពី $x = 1$ ទៅ $x = 2$ ។',
        r'$\frac{33}{16}$',
        '$y\' = \\frac{x^3}{2} - \\frac{1}{2x^3} \\implies 1 + (y\')^2 = \\left(\\frac{x^3}{2} + \\frac{1}{2x^3}\\right)^2$ ។ $L = \\int_1^2 \\left(\\frac{x^3}{2} + \\frac{1}{2x^3}\\right)dx = \\left[\\frac{x^4}{8} - \\frac{1}{4x^2}\\right]_1^2 = \\frac{33}{16}$។',
        bloom='Analyze',
    ))

    # 44 (Hard - Evaluate)
    # y = sin x on [0, pi] around Ox -> pi * int_0^pi sin^2 x dx = pi * pi/2 = pi^2/2
    qs.append(writing(
        'hard', S1,
        'គណនាមាឌសូលីតបរិវត្តកំណត់បានពីរង្វិលជុំវិញអ័ក្ស $Ox$ នៃផ្ទៃខណ្ឌដោយក្រាប $y = \\sin x$ និងអ័ក្ស $Ox$ លើ $[0, \\pi]$ ។',
        r'$\frac{\pi^2}{2}$',
        '$V = \\pi \\int_0^{\\pi} \\sin^2 x\\,dx = \\frac{\\pi}{2} \\int_0^{\\pi} (1 - \\cos 2x)\\,dx = \\frac{\\pi}{2}\\left[x - \\frac{\\sin 2x}{2}\\right]_0^{\\pi} = \\frac{\\pi^2}{2}$។',
        bloom='Evaluate',
    ))

    # 45 (Hard - Create)
    # Determine k > 0 such that revolving y = kx around Ox on [0, 3] gives V = 36*pi -> pi*k^2*9 = 36*pi -> k = 2
    qs.append(writing(
        'hard', S1,
        'កំណត់តម្លៃថេរវិជ្ជមាន $k$ ដើម្បីឲ្យមាឌសូលីតបរិវត្តដែលបានពីរង្វិលផ្ទៃក្រោម $y = kx$ លើ $[0, 3]$ ជុំវិញអ័ក្ស $Ox$ ស្មើនឹង $36\\pi$ ។',
        r'$k = 2$',
        '$V = \\pi \\int_0^3 k^2 x^2\\,dx = 9\\pi k^2 = 36\\pi \\implies k^2 = 4 \\implies k = 2$។',
        bloom='Create',
    ))

    # 46 (PISA - Apply)
    # Rocket nose cone: y = 2*sqrt(x) (dm) on [0, 4] around Ox -> V = pi * int_0^4 4x dx = 32*pi dm^3
    qs.append(writing(
        'pisa', S1,
        'ក្បាលគ្រាប់រ៉ុក្កែតគំរូមួយមានរាងជាសូលីតបរិវត្តកើតពីរង្វិលក្រាប $y = 2\\sqrt{x}$ ($0 \\le x \\le 4$, គិតជា $\\text{dm}$) ជុំវិញអ័ក្ស $Ox$ ។ គណនាមាឌនៃក្បាលរ៉ុក្កែតនេះ។',
        r'$32\pi\,\text{dm}^3$',
        '$V = \\pi \\int_0^4 (2\\sqrt{x})^2\\,dx = \\pi \\int_0^4 4x\\,dx = \\pi [2x^2]_0^4 = 32\\pi\\,\\text{dm}^3$។',
        bloom='Apply',
    ))

    # 47 (PISA - Analyze)
    # Torus-like / napkin ring: sphere radius 5 with cylindrical hole radius 3 drilled along x-axis -> x in [-4, 4]
    # V = pi * int_{-4}^4 ((25 - x^2) - 9) dx = pi * int_{-4}^4 (16 - x^2) dx = 2*pi*(64 - 64/3) = 256*pi/3
    qs.append(writing(
        'pisa', S1,
        'គេខួងរន្ធស៊ីឡាំងកាំ $3\\,\\text{cm}$ កាត់តាមផ្ចិតនៃស្វ៊ែរឈើកាំ $5\\,\\text{cm}$ តាមអ័ក្ស $Ox$ (ដែន $x \\in [-4, 4]$) ។ គណនាមាឌឈើដែលនៅសល់។',
        r'$\frac{256\pi}{3}\,\text{cm}^3$',
        '$V = \\pi \\int_{-4}^4 [(25 - x^2) - 3^2]\\,dx = 2\\pi \\int_0^4 (16 - x^2)\\,dx = 2\\pi\\left(64 - \\frac{64}{3}\\right) = \\frac{256\\pi}{3}\\,\\text{cm}^3$។',
        bloom='Analyze',
    ))

    # 48 (PISA - Evaluate)
    # Catenary / hanging cable y = 1/2*(e^x + e^{-x}) on [0, 1] -> L = sinh(1) = (e - 1/e)/2
    qs.append(writing(
        'pisa', S3,
        'ខ្សែភ្លើងយោលមួយមានសមីការ $y = \\frac{1}{2}(e^x + e^{-x})$ លើចន្លោះ $[0, 1]$ (គិតជាម៉ែត្រ) ។ គណនាប្រវែងពិតប្រាកដនៃខ្សែភ្លើងនេះ។',
        r'$\frac{e - e^{-1}}{2}\,\text{m}$',
        '$y\' = \\frac{1}{2}(e^x - e^{-x}) \\implies 1 + (y\')^2 = \\left(\\frac{e^x + e^{-x}}{2}\\right)^2$ ។ $L = \\int_0^1 \\frac{e^x + e^{-x}}{2}\\,dx = \\left[\\frac{e^x - e^{-x}}{2}\\right]_0^1 = \\frac{e - e^{-1}}{2}\\,\\text{m}$។',
        bloom='Evaluate',
    ))

    # 49 (PISA - Analyze)
    # Cooling tower / hourglass shape x = 1 + y^2/4 on [-2, 2] around Oy -> V = pi * int_{-2}^2 (1 + y^2/4)^2 dy = 2*pi*(2 + 2/3*8/4 + 1/16*32/5)
    # Let's compute: (1 + y^2/2 + y^4/16) from -2 to 2: 2*(2 + 8/6 + 32/80) = 2*(2 + 4/3 + 2/5) = 2*(30+20+6)/15 = 112*pi/15
    qs.append(writing(
        'pisa', S2,
        'ប៉មត្រជាក់រោងចក្រមួយមានរាងជាសូលីតបរិវត្តកើតពីរង្វិលខ្សែកោង $x = 1 + \\frac{y^2}{4}$ ($-2 \\le y \\le 2$, គិតជាដេកាម៉ែត្រ) ជុំវិញអ័ក្ស $Oy$ ។ គណនាមាឌខាងក្នុងប៉មនេះ។',
        r'$\frac{112\pi}{15}\,\text{dam}^3$',
        '$V = 2\\pi \\int_0^2 \\left(1 + \\frac{y^2}{2} + \\frac{y^4}{16}\\right)dy = 2\\pi\\left(2 + \\frac{4}{3} + \\frac{2}{5}\\right) = \\frac{112\\pi}{15}\\,\\text{dam}^3$។',
        bloom='Analyze',
    ))

    # 50 (PISA - Create)
    # Design a water tank by rotating y = k*sqrt(x) on [0, 9] around Ox so capacity is 81*pi -> pi * k^2 * 81/2 = 81*pi -> k = sqrt(2)
    qs.append(writing(
        'pisa', S1,
        'វិស្វករម្នាក់រចនាធុងទឹករាងប៉ារ៉ាបូលូអ៊ីតដោយបង្វិលក្រាប $y = k\\sqrt{x}$ ($0 \\le x \\le 9$, គិតជា $\\text{dm}$) ជុំវិញអ័ក្ស $Ox$ ។ កំណត់តម្លៃ $k > 0$ ដើម្បីឲ្យធុងមានចំណុះ $81\\pi\\,\\text{L}$ ។',
        r'$k = \sqrt{2}$',
        '$V = \\pi \\int_0^9 k^2 x\\,dx = \\frac{81}{2}\\pi k^2 = 81\\pi \\implies k^2 = 2 \\implies k = \\sqrt{2}$។',
        bloom='Create',
    ))

    return qs


def _verify_math():
    mp.mp.dps = 30
    tol = mp.mpf('1e-11')
    # Q12: pi * int_1^3 (2x+1)^2 dx = 158*pi/3
    assert abs(mp.pi * mp.quad(lambda x: (2 * x + 1)**2, [1, 3]) - mp.mpf(158) * mp.pi / 3) < tol
    # Q16: pi * int_0^2 ((4x-x^2)^2 - x^4) dx = 32*pi/3
    assert abs(mp.pi * mp.quad(lambda x: (4 * x - x**2)**2 - x**4, [0, 2]) - mp.mpf(32) * mp.pi / 3) < tol
    # Q17: pi * int_0^{sqrt(3)} (3 - y^2)^2 dy = 24*pi*sqrt(3)/5
    assert abs(mp.pi * mp.quad(lambda y: (3 - y**2)**2, [0, mp.sqrt(3)]) - mp.mpf(24) * mp.pi * mp.sqrt(3) / 5) < tol
    # Q20: int_0^1 sqrt(1 + 8x) dx = 13/6
    assert abs(mp.quad(lambda x: mp.sqrt(1 + 8 * x), [0, 1]) - mp.mpf(13) / 6) < tol
    # Q22: int_0^3 (x^2 + 1) dx = 12
    assert abs(mp.quad(lambda x: x**2 + 1, [0, 3]) - mp.mpf(12)) < tol
    # Q26: pi * int_{-1}^2 ((4-x^2)^2 - (2-x)^2) dx = 108*pi/5
    assert abs(mp.pi * mp.quad(lambda x: (4 - x**2)**2 - (2 - x)**2, [-1, 2]) - mp.mpf(108) * mp.pi / 5) < tol
    # Q27: int_1^3 sqrt(1 + (x^2 - 1/(4x^2))^2) dx = 53/6
    assert abs(mp.quad(lambda x: mp.sqrt(1 + (x**2 - 1 / (4 * x**2))**2), [1, 3]) - mp.mpf(53) / 6) < tol
    # Q29: pi * int_0^1 (exp(2x) - (e*x)^2) dx = (e^2 - 3)/6 * pi
    assert abs(mp.pi * mp.quad(lambda x: mp.exp(2 * x) - (mp.e * x)**2, [0, 1]) - (mp.e**2 - 3) / 6 * mp.pi) < tol
    # Q39: 250*pi
    assert abs(mp.pi * mp.quad(lambda x: (9 - x)**2 - (x**2 - 2 * x + 3)**2, [-2, 3]) - 250 * mp.pi) < tol
    # Q42: 117*pi/5
    assert abs(mp.pi * mp.quad(lambda x: (-x + 3)**2 - (x**2 + 1)**2, [-2, 1]) - mp.mpf(117) * mp.pi / 5) < tol
    # Q43: 33/16
    assert abs(mp.quad(lambda x: mp.sqrt(1 + (x**3 / 2 - 1 / (2 * x**3))**2), [1, 2]) - mp.mpf(33) / 16) < tol
    # Q49: 112*pi/15
    assert abs(mp.pi * mp.quad(lambda y: (1 + y**2 / 4)**2, [-2, 2]) - mp.mpf(112) * mp.pi / 15) < tol


cands = build_candidates


if __name__ == '__main__':
    _verify_math()
    qs = build_candidates()
    print(f'{LESSON}: built {len(qs)} candidates, mpmath verified')
