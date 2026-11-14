"""Bank generator for Grade 12 Science — Lesson 17: ផ្ទៃក្រឡានៃផ្ទៃប្លង់."""
import math
from fractions import Fraction
import mpmath as mp
from lib import mcq, wr

LESSON = 'ផ្ទៃក្រឡានៃផ្ទៃប្លង់'
CHAPTER = 'ជំពូកទី 6 : អាំងតេក្រាល'
TARGET = {
    ('mcq', 'easy'): 10, ('mcq', 'medium'): 14, ('mcq', 'hard'): 7, ('mcq', 'pisa'): 5,
    ('writing', 'easy'): 1, ('writing', 'medium'): 4, ('writing', 'hard'): 4, ('writing', 'pisa'): 5,
}

S1 = '១. ផលបូកចតុកោណកែង និងទ្រឹស្តីបទគ្រឹះ'
S2 = '២. ផ្ទៃក្រឡាខណ្ឌដោយក្រាប និងអ័ក្សអាប់ស៊ីស'
S3 = '៣. ផ្ទៃក្រឡាខណ្ឌដោយខ្សែកោងពីរ'


def writing(level, sec, stem, ans, sol, bloom=None):
    return wr(level, sec, stem, [(sol, 3), (f'ចម្លើយ៖ {ans}', 2)], bloom=bloom)


def svg_area_axis(curve_pts, x0, x1, label_f='y = f(x)', a_lbl='a', b_lbl='b', neg=False):
    w, h = 240, 150
    ox, oy = 35, 115
    sx, sy = 34, 24
    if neg:
        oy = 40
    pts_str = ' '.join(f'{ox + x * sx:.1f},{oy - y * sy:.1f}' for x, y in curve_pts)
    poly_pts = f'{ox + x0 * sx:.1f},{oy} ' + pts_str + f' {ox + x1 * sx:.1f},{oy}'
    fill = '#fed7d7' if neg else '#bee3f8'
    stroke = '#c53030' if neg else '#2b6cb0'
    return (
        f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg">'
        f'<line x1="15" y1="{oy}" x2="225" y2="{oy}" stroke="#4a5568" stroke-width="1.2"/>'
        f'<line x1="{ox}" y1="10" x2="{ox}" y2="140" stroke="#4a5568" stroke-width="1.2"/>'
        f'<polygon points="{poly_pts}" fill="{fill}" fill-opacity="0.7" stroke="none"/>'
        f'<polyline points="{pts_str}" fill="none" stroke="{stroke}" stroke-width="2"/>'
        f'<line x1="{ox + x0 * sx:.1f}" y1="{oy}" x2="{ox + x0 * sx:.1f}" y2="{oy - curve_pts[0][1] * sy:.1f}" stroke="#718096" stroke-dasharray="3,2"/>'
        f'<line x1="{ox + x1 * sx:.1f}" y1="{oy}" x2="{ox + x1 * sx:.1f}" y2="{oy - curve_pts[-1][1] * sy:.1f}" stroke="#718096" stroke-dasharray="3,2"/>'
        f'<text x="{ox + x0 * sx:.1f}" y="{oy + 13}" font-size="11" text-anchor="middle">{a_lbl}</text>'
        f'<text x="{ox + x1 * sx:.1f}" y="{oy + 13}" font-size="11" text-anchor="middle">{b_lbl}</text>'
        f'<text x="218" y="{oy - 5}" font-size="11">x</text>'
        f'<text x="{ox + 5}" y="18" font-size="11">y</text>'
        f'<text x="155" y="25" font-size="11" fill="{stroke}">{label_f}</text>'
        f'</svg>'
    )


def svg_riemann(rects, curve_pts, title='Riemann Sum'):
    w, h = 240, 150
    ox, oy = 32, 122
    sx, sy = 36, 22
    rect_els = ''.join(
        f'<rect x="{ox + xl * sx:.1f}" y="{oy - ht * sy:.1f}" width="{(xr - xl) * sx:.1f}" '
        f'height="{ht * sy:.1f}" fill="#90cdf4" fill-opacity="0.55" stroke="#2b6cb0" stroke-width="1"/>'
        for xl, xr, ht in rects
    )
    pts_str = ' '.join(f'{ox + x * sx:.1f},{oy - y * sy:.1f}' for x, y in curve_pts)
    return (
        f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg">'
        f'<line x1="15" y1="{oy}" x2="225" y2="{oy}" stroke="#4a5568" stroke-width="1.2"/>'
        f'<line x1="{ox}" y1="10" x2="{ox}" y2="140" stroke="#4a5568" stroke-width="1.2"/>'
        f'{rect_els}'
        f'<polyline points="{pts_str}" fill="none" stroke="#c53030" stroke-width="2"/>'
        f'<text x="218" y="{oy - 5}" font-size="11">x</text>'
        f'<text x="{ox + 5}" y="18" font-size="11">y</text>'
        f'<text x="140" y="20" font-size="10" fill="#2d3748">{title}</text>'
        f'</svg>'
    )


def svg_two_curves(pts_top, pts_bot, x0, x1, lbl_f='f(x)', lbl_g='g(x)'):
    w, h = 240, 150
    ox, oy = 40, 120
    sx, sy = 34, 22
    top_str = ' '.join(f'{ox + x * sx:.1f},{oy - y * sy:.1f}' for x, y in pts_top)
    bot_rev = ' '.join(f'{ox + x * sx:.1f},{oy - y * sy:.1f}' for x, y in reversed(pts_bot))
    bot_str = ' '.join(f'{ox + x * sx:.1f},{oy - y * sy:.1f}' for x, y in pts_bot)
    return (
        f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg">'
        f'<line x1="15" y1="{oy}" x2="225" y2="{oy}" stroke="#4a5568" stroke-width="1.2"/>'
        f'<line x1="{ox}" y1="10" x2="{ox}" y2="140" stroke="#4a5568" stroke-width="1.2"/>'
        f'<polygon points="{top_str} {bot_rev}" fill="#c6f6d5" fill-opacity="0.7" stroke="none"/>'
        f'<polyline points="{top_str}" fill="none" stroke="#2b6cb0" stroke-width="2"/>'
        f'<polyline points="{bot_str}" fill="none" stroke="#c53030" stroke-width="2"/>'
        f'<text x="150" y="24" font-size="10" fill="#2b6cb0">{lbl_f}</text>'
        f'<text x="150" y="38" font-size="10" fill="#c53030">{lbl_g}</text>'
        f'<text x="218" y="{oy - 5}" font-size="11">x</text>'
        f'<text x="{ox + 5}" y="18" font-size="11">y</text>'
        f'</svg>'
    )


def build_candidates():
    qs = []

    # =========================================================================
    # MCQ EASY (10): Remember & Understand
    # =========================================================================
    # 1 (Remember)
    qs.append(mcq(
        'easy', S2,
        'បើអនុគមន៍ $f$ ជាប់ និង $f(x) \\ge 0$ លើចន្លោះ $[a, b]$ តើផ្ទៃក្រឡា $A$ ខណ្ឌដោយក្រាប $y=f(x)$ អ័ក្ស $Ox$ និងបន្ទាត់ $x=a, x=b$ កំណត់ដោយរូបមន្តណា?',
        r'$A = \int_a^b f(x)\,dx$',
        [r'$A = -\int_a^b f(x)\,dx$', r'$A = \int_b^a f(x)\,dx$', r'$A = f(b) - f(a)$'],
        'តាមនិយមន័យ បើ $f(x) \\ge 0$ លើ $[a,b]$ នោះ $A = \\int_a^b f(x)\\,dx$។',
        bloom='Remember',
    ))

    # 2 (Remember)
    qs.append(mcq(
        'easy', S2,
        'បើអនុគមន៍ $f$ ជាប់ និង $f(x) \\le 0$ លើចន្លោះ $[a, b]$ តើផ្ទៃក្រឡា $A$ ខណ្ឌដោយក្រាប $y=f(x)$ អ័ក្ស $Ox$ និងបន្ទាត់ $x=a, x=b$ ស្មើនឹងអ្វី?',
        r'$A = -\int_a^b f(x)\,dx$',
        [r'$A = \int_a^b f(x)\,dx$', r'$A = \int_a^b (f(x))^2\,dx$', r'$A = 0$'],
        'ដោយសារ $f(x) \\le 0$ លើ $[a,b]$ នោះ $|f(x)| = -f(x)$ ដូច្នេះ $A = -\\int_a^b f(x)\\,dx$។',
        bloom='Remember',
    ))

    # 3 (Remember)
    qs.append(mcq(
        'easy', S3,
        'បើ $f$ និង $g$ ជាប់ ហើយ $f(x) \\ge g(x)$ លើ $[a, b]$ តើផ្ទៃក្រឡា $A$ ចន្លោះក្រាប $y=f(x)$ និង $y=g(x)$ ពី $x=a$ ដល់ $x=b$ ស្មើនឹងអ្វី?',
        r'$A = \int_a^b (f(x) - g(x))\,dx$',
        [r'$A = \int_a^b (f(x) + g(x))\,dx$', r'$A = \int_a^b (g(x) - f(x))\,dx$', r'$A = \int_a^b f(x)g(x)\,dx$'],
        'ផ្ទៃក្រឡាចន្លោះក្រាបលើ និងក្រាបក្រោមគឺ $A = \\int_a^b [f(x) - g(x)]\\,dx$។',
        bloom='Remember',
    ))

    # 4 (Understand)
    qs.append(mcq(
        'easy', S1,
        'តាមទ្រឹស្តីបទគ្រឹះនៃកាល់គុលអាំងតេក្រាល បើ $A(x) = \\int_a^x f(t)\\,dt$ ដែល $f$ ជាប់លើ $[a, b]$ នោះ $A\'(x)$ ស្មើនឹងអ្វី?',
        r'$f(x)$',
        [r'$f\'(x)$', r'$f(x) - f(a)$', r'$0$'],
        'ដេរីវេនៃអនុគមន៍ផ្ទៃក្រឡា $A(x) = \\int_a^x f(t)\\,dt$ គឺ $A\'(x) = f(x)$។',
        bloom='Understand',
    ))

    # 5 (Apply)
    qs.append(mcq(
        'easy', S2,
        'គណនាផ្ទៃក្រឡាខណ្ឌដោយក្រាប $y = 2x$ អ័ក្ស $Ox$ និងបន្ទាត់ $x = 0, x = 3$ ។',
        r'$9$',
        [r'$6$', r'$3$', r'$18$'],
        'លើ $[0, 3]$ យើងមាន $2x \\ge 0$ ដូច្នេះ $A = \\int_0^3 2x\\,dx = [x^2]_0^3 = 9$។',
        bloom='Apply',
    ))

    # 6 (Apply)
    qs.append(mcq(
        'easy', S2,
        'គណនាផ្ទៃក្រឡាខណ្ឌដោយក្រាប $y = x^2$ អ័ក្ស $Ox$ និងបន្ទាត់ $x = 0, x = 3$ ។',
        r'$9$',
        [r'$3$', r'$27$', r'$\frac{9}{2}$'],
        '$A = \\int_0^3 x^2\\,dx = \\left[\\frac{x^3}{3}\\right]_0^3 = \\frac{27}{3} = 9$។',
        bloom='Apply',
    ))

    # 7 (Understand)
    svg7 = svg_area_axis([(x, -0.5 * x) for x in [0, 1, 2, 3, 4]], 0, 4, label_f='y = f(x)', a_lbl='a', b_lbl='b', neg=True)
    qs.append(mcq(
        'easy', S2,
        f'ពិនិត្យក្រាបខាងក្រោមដែល $f(x) < 0$ លើ $[a, b]$ ។ បើ $\\int_a^b f(x)\\,dx = -7$ តើផ្ទៃក្រឡាផ្នែកលាបពណ៌ស្មើនឹងប៉ុន្មាន?<br/>{svg7}',
        r'$7$',
        [r'$-7$', r'$0$', r'$14$'],
        'ផ្ទៃក្រឡាជាចំនួនវិជ្ជមានជានិច្ច៖ $A = -\\int_a^b f(x)\\,dx = -(-7) = 7$។',
        bloom='Understand',
    ))

    # 8 (Apply)
    qs.append(mcq(
        'easy', S1,
        'គេចែកចន្លោះ $[0, 4]$ ជា $n = 4$ ចន្លោះរងស្មើគ្នា ដើម្បីគណនាផលបូករីម៉ាន់នៃ $f(x) = x + 1$ ។ តើប្រវែង $\\Delta x$ នៃចន្លោះរងនីមួយៗស្មើនឹងប៉ុន្មាន?',
        r'$1$',
        [r'$4$', r'$0.5$', r'$2$'],
        '$\\Delta x = \\frac{b - a}{n} = \\frac{4 - 0}{4} = 1$។',
        bloom='Apply',
    ))

    # 9 (Apply)
    qs.append(mcq(
        'easy', S2,
        'គណនាផ្ទៃក្រឡាខណ្ឌដោយក្រាប $y = e^x$ អ័ក្ស $Ox$ និងបន្ទាត់ $x = 0, x = 1$ ។',
        r'$e - 1$',
        [r'$e$', r'$e + 1$', r'$1$'],
        '$A = \\int_0^1 e^x\\,dx = [e^x]_0^1 = e - 1$។',
        bloom='Apply',
    ))

    # 10 (Understand)
    qs.append(mcq(
        'easy', S3,
        'ដើម្បីរកផ្ទៃក្រឡាខណ្ឌដោយប៉ារ៉ាបូល $y = x^2$ និងបន្ទាត់ $y = x$ តើត្រូវរកកូអរដោនេអាប់ស៊ីសនៃចំណុចប្រសព្វជាមុនសិន។ តើចំណុចប្រសព្វមានអាប់ស៊ីសណាខ្លះ?',
        r'$x = 0$ និង $x = 1$',
        [r'$x = -1$ និង $x = 1$', r'$x = 0$ និង $x = 2$', r'$x = 1$ និង $x = 2$'],
        'ដោះស្រាយ $x^2 = x \\iff x(x - 1) = 0 \\iff x = 0$ ឬ $x = 1$។',
        bloom='Understand',
    ))

    # =========================================================================
    # MCQ MEDIUM (14): Apply & Analyze
    # =========================================================================
    # 11 (Apply) - Riemann left sum
    # f(x) = x^2 + 1 on [0, 2], n = 2 -> dx = 1, left: f(0)*1 + f(1)*1 = 1 + 2 = 3
    svg11 = svg_riemann([(0, 1, 1), (1, 2, 2)], [(0.2 * i, (0.2 * i)**2 + 1) for i in range(11)], 'f(x)=x^2+1')
    qs.append(mcq(
        'medium', S1,
        f'គណនាផលបូកចតុកោណកែងខាងក្រោម (ចុងខាងឆ្វេង) សម្រាប់ $f(x) = x^2 + 1$ លើ $[0, 2]$ ដោយចែកជា $n = 2$ ចន្លោះរងស្មើគ្នា។<br/>{svg11}',
        r'$3$',
        [r'$7$', r'$5$', r'$4.5$'],
        '$\\Delta x = \\frac{2-0}{2} = 1$ ។ ផលបូកចុងខាងឆ្វេង $= [f(0) + f(1)] \\cdot 1 = (1 + 2) \\cdot 1 = 3$។',
        bloom='Apply',
    ))

    # 12 (Apply) - Riemann right sum
    # f(x) = 2x + 1 on [1, 3], n = 2 -> dx = 1, right: f(2)*1 + f(3)*1 = 5 + 7 = 12
    qs.append(mcq(
        'medium', S1,
        'គណនាផលបូករីម៉ាន់ដោយប្រើចុងខាងស្តាំនៃចន្លោះរង សម្រាប់ $f(x) = 2x + 1$ លើ $[1, 3]$ ជាមួយ $n = 2$ ចន្លោះរងស្មើគ្នា។',
        r'$12$',
        [r'$8$', r'$10$', r'$14$'],
        '$\\Delta x = \\frac{3-1}{2} = 1$ ។ ចុងខាងស្តាំគឺ $x_1 = 2, x_2 = 3$ ដូច្នេះ $S = [f(2) + f(3)] \\cdot 1 = 5 + 7 = 12$។',
        bloom='Apply',
    ))

    # 13 (Apply) - Riemann midpoint
    # f(x) = x^2 on [0, 2], n = 2 -> dx = 1, midpoints 0.5, 1.5 -> (0.25 + 2.25)*1 = 2.5
    qs.append(mcq(
        'medium', S1,
        'គណនាផលបូកចតុកោណកែងតាមចំណុចកណ្តាលនៃចន្លោះរង សម្រាប់ $f(x) = x^2$ លើ $[0, 2]$ ជាមួយ $n = 2$ ចន្លោះរងស្មើគ្នា។',
        r'$2.5$',
        [r'$1$', r'$5$', r'$3$'],
        '$\\Delta x = 1$ ។ ចំណុចកណ្តាលគឺ $0.5$ និង $1.5$ ។ $S_{\\text{mid}} = (0.5^2 + 1.5^2)\\cdot 1 = 0.25 + 2.25 = 2.5$។',
        bloom='Apply',
    ))

    # 14 (Apply) - f(x) = 4 - x^2 on [-2, 2]
    svg14 = svg_area_axis([(x, 4 - x**2) for x in [-2 + 0.4 * i for i in range(11)]], -2, 2, label_f='y = 4 - x^2', a_lbl='-2', b_lbl='2')
    qs.append(mcq(
        'medium', S2,
        f'គណនាផ្ទៃក្រឡាខណ្ឌដោយក្រាប $y = 4 - x^2$ និងអ័ក្សអាប់ស៊ីសលើ $[-2, 2]$ ។<br/>{svg14}',
        r'$\frac{32}{3}$',
        [r'$\frac{16}{3}$', r'$8$', r'$\frac{64}{3}$'],
        '$A = \\int_{-2}^2 (4 - x^2)\\,dx = 2\\left[4x - \\frac{x^3}{3}\\right]_0^2 = 2\\left(8 - \\frac{8}{3}\\right) = \\frac{32}{3}$។',
        bloom='Apply',
    ))

    # 15 (Apply) - negative curve y = x^2 - 4 on [-2, 2]
    qs.append(mcq(
        'medium', S2,
        'គណនាផ្ទៃក្រឡាខណ្ឌដោយក្រាប $y = x^2 - 4$ និងអ័ក្ស $Ox$ ពី $x = -2$ ដល់ $x = 2$ ។',
        r'$\frac{32}{3}$',
        [r'$-\frac{32}{3}$', r'$\frac{16}{3}$', r'$0$'],
        'លើ $[-2, 2]$ យើងមាន $x^2 - 4 \\le 0$ ដូច្នេះ $A = -\\int_{-2}^2 (x^2 - 4)\\,dx = \\frac{32}{3}$។',
        bloom='Apply',
    ))

    # 16 (Apply) - y = -sqrt(x-2) on [2, 6]
    qs.append(mcq(
        'medium', S2,
        'គណនាផ្ទៃក្រឡាខណ្ឌដោយក្រាប $y = -\\sqrt{x - 2}$ អ័ក្ស $Ox$ និងបន្ទាត់ $x = 2, x = 6$ ។',
        r'$\frac{16}{3}$',
        [r'$-\frac{16}{3}$', r'$\frac{8}{3}$', r'$8$'],
        '$A = -\\int_2^6 (-\\sqrt{x-2})\\,dx = \\left[\\frac{2}{3}(x-2)^{3/2}\\right]_2^6 = \\frac{2}{3}(8) = \\frac{16}{3}$។',
        bloom='Apply',
    ))

    # 17 (Apply) - y = 1/x on [1, e^2]
    qs.append(mcq(
        'medium', S2,
        'គណនាផ្ទៃក្រឡាខណ្ឌដោយក្រាប $y = \\frac{3}{x}$ អ័ក្ស $Ox$ និងបន្ទាត់ $x = 1, x = 5$ ។',
        r'$3\ln 5$',
        [r'$\ln 5$', r'$3\ln 4$', r'$\frac{12}{5}$'],
        '$A = \\int_1^5 \\frac{3}{x}\\,dx = [3\\ln x]_1^5 = 3\\ln 5$។',
        bloom='Apply',
    ))

    # 18 (Apply) - y = sin x on [0, pi]
    qs.append(mcq(
        'medium', S2,
        'គណនាផ្ទៃក្រឡាខណ្ឌដោយក្រាប $y = \\sin x$ និងអ័ក្ស $Ox$ លើចន្លោះ $[0, \\pi]$ ។',
        r'$2$',
        [r'$0$', r'$1$', r'$4$'],
        '$A = \\int_0^{\\pi} \\sin x\\,dx = [-\\cos x]_0^{\\pi} = -(-1) - (-1) = 2$។',
        bloom='Apply',
    ))

    # 19 (Analyze) - sign change y = x on [-1, 2]
    # int_{-1}^0 (-x)dx + int_0^2 x dx = 1/2 + 2 = 5/2
    qs.append(mcq(
        'medium', S2,
        'គណនាផ្ទៃក្រឡាខណ្ឌដោយក្រាប $y = x$ អ័ក្ស $Ox$ និងបន្ទាត់ $x = -1, x = 2$ ។',
        r'$\frac{5}{2}$',
        [r'$\frac{3}{2}$', r'$2$', r'$3$'],
        'ក្រាបកាត់អ័ក្ស $Ox$ ត្រង់ $x = 0$ ។ $A = -\\int_{-1}^0 x\\,dx + \\int_0^2 x\\,dx = \\frac{1}{2} + 2 = \\frac{5}{2}$។',
        bloom='Analyze',
    ))

    # 20 (Apply) - two curves y = x and y = x^2
    svg20 = svg_two_curves(
        [(0.2 * i, 0.2 * i) for i in range(6)],
        [(0.2 * i, (0.2 * i)**2) for i in range(6)],
        0, 1, 'y = x', 'y = x^2'
    )
    qs.append(mcq(
        'medium', S3,
        f'គណនាផ្ទៃក្រឡាខណ្ឌដោយបន្ទាត់ $y = x$ និងប៉ារ៉ាបូល $y = x^2$ ។<br/>{svg20}',
        r'$\frac{1}{6}$',
        [r'$\frac{1}{3}$', r'$\frac{1}{2}$', r'$\frac{1}{12}$'],
        'លើ $[0, 1]$ យើងមាន $x \\ge x^2$ ដូច្នេះ $A = \\int_0^1 (x - x^2)\\,dx = \\left[\\frac{x^2}{2} - \\frac{x^3}{3}\\right]_0^1 = \\frac{1}{6}$។',
        bloom='Apply',
    ))

    # 21 (Apply) - two curves y = 4 - x^2/2 and y = x on [0, 2]
    qs.append(mcq(
        'medium', S3,
        'គណនាផ្ទៃក្រឡាខណ្ឌដោយក្រាប $y = 4 - \\frac{x^2}{2}$ បន្ទាត់ $y = x$ និងអ័ក្ស $Oy$ លើ $[0, 2]$ ។',
        r'$\frac{14}{3}$',
        [r'$\frac{10}{3}$', r'$6$', r'$\frac{8}{3}$'],
        '$A = \\int_0^2 \\left(4 - \\frac{x^2}{2} - x\\right)dx = \\left[4x - \\frac{x^3}{6} - \\frac{x^2}{2}\\right]_0^2 = 8 - \\frac{4}{3} - 2 = \\frac{14}{3}$។',
        bloom='Apply',
    ))

    # 22 (Apply) - two curves y = x^2 + 2x and y = x + 2
    # roots: x^2 + x - 2 = 0 -> x = -2, 1. int_{-2}^1 (2 - x - x^2) dx = 9/2
    qs.append(mcq(
        'medium', S3,
        'គណនាផ្ទៃក្រឡាខណ្ឌដោយប៉ារ៉ាបូល $P: y = x^2 + 2x$ និងបន្ទាត់ $d: y = x + 2$ ។',
        r'$\frac{9}{2}$',
        [r'$\frac{7}{2}$', r'$9$', r'$\frac{5}{2}$'],
        'ចំណុចប្រសព្វ៖ $x^2 + 2x = x + 2 \\iff x = -2$ ឬ $x = 1$ ។ $A = \\int_{-2}^1 (x + 2 - x^2 - 2x)\\,dx = \\frac{9}{2}$។',
        bloom='Apply',
    ))

    # 23 (Analyze) - sign change y = 4 - x^2 on [-2, 3]
    # int_{-2}^2 (4-x^2)dx + int_2^3 (x^2-4)dx = 32/3 + (9-12 - (8/3-8)) = 32/3 + 7/3 = 39/3 = 13
    qs.append(mcq(
        'medium', S2,
        'គណនាផ្ទៃក្រឡាខណ្ឌដោយក្រាប $y = 4 - x^2$ និងអ័ក្ស $Ox$ លើចន្លោះ $[-2, 3]$ ។',
        r'$13$',
        [r'$\frac{25}{3}$', r'$\frac{32}{3}$', r'$11$'],
        'លើ $[-2, 2]$ ក្រាបនៅលើ $Ox$ ($A_1 = \\frac{32}{3}$) និងលើ $[2, 3]$ នៅក្រោម $Ox$ ($A_2 = \\int_2^3 (x^2 - 4)\\,dx = \\frac{7}{3}$) ។ សរុប $A = 13$។',
        bloom='Analyze',
    ))

    # 24 (Analyze) - compare Riemann approximations
    qs.append(mcq(
        'medium', S1,
        'សម្រាប់អនុគមន៍កើន និងវិជ្ជមាន $f$ លើ $[a, b]$ តើផលបូករីម៉ាន់តាមចុងខាងឆ្វេង $S_L$ ផលបូកតាមចុងខាងស្តាំ $S_R$ និងផ្ទៃក្រឡាពិត $A$ មានទំនាក់ទំនងដូចម្តេច?',
        r'$S_L \le A \le S_R$',
        [r'$S_R \le A \le S_L$', r'$A \le S_L \le S_R$', r'$S_L = A = S_R$'],
        'ដោយ $f$ កើន កម្ពស់ចតុកោណកែងខាងឆ្វេងតិចជាងឬស្មើ $f(x)$ ហើយខាងស្តាំធំជាងឬស្មើ $f(x)$ ដូច្នេះ $S_L \\le A \\le S_R$។',
        bloom='Analyze',
    ))

    # =========================================================================
    # MCQ HARD (7): Analyze & Evaluate
    # =========================================================================
    # 25 (Analyze) - two crossing curves: y = x^2 - 3x + 2 and y = x - 1 on [0, 2]
    # f - g = x^2 - 4x + 3 = (x-1)(x-3), root at x=1 on [0,2].
    # int_0^1 (x^2-4x+3)dx + int_1^2 (-x^2+4x-3)dx = (1/3 - 2 + 3) + [(-8/3+8-6) - (-1/3+2-3)] = 4/3 + (-2/3 + 4/3) = 2
    qs.append(mcq(
        'hard', S3,
        'គណនាផ្ទៃក្រឡាខណ្ឌដោយប៉ារ៉ាបូល $P: y = x^2 - 3x + 2$ បន្ទាត់ $d: y = x - 1$ និងបន្ទាត់ $x = 0, x = 2$ ។',
        r'$2$',
        [r'$\frac{2}{3}$', r'$\frac{4}{3}$', r'$\frac{8}{3}$'],
        '$P$ និង $d$ កាត់គ្នាត្រង់ $x = 1$ ។ $A = \\int_0^1 (x^2 - 4x + 3)\\,dx + \\int_1^2 (-x^2 + 4x - 3)\\,dx = \\frac{4}{3} + \\frac{2}{3} = 2$។',
        bloom='Analyze',
    ))

    # 26 (Analyze) - y = x^3 - x and Ox on [-1, 1]
    # odd function: 2 * int_0^1 (x - x^3) dx = 2 * (1/2 - 1/4) = 1/2
    qs.append(mcq(
        'hard', S2,
        'គណនាផ្ទៃក្រឡាខណ្ឌដោយក្រាប $y = x^3 - x$ និងអ័ក្ស $Ox$ លើ $[-1, 1]$ ។',
        r'$\frac{1}{2}$',
        [r'$0$', r'$1$', r'$\frac{1}{4}$'],
        'ក្រាបកាត់ $Ox$ ត្រង់ $-1, 0, 1$ ។ ដោយភាពសេស $A = 2\\int_0^1 (x - x^3)\\,dx = 2\\left(\\frac{1}{2} - \\frac{1}{4}\\right) = \\frac{1}{2}$។',
        bloom='Analyze',
    ))

    # 27 (Analyze) - y = x^2 and y = 2x - x^2
    # 2x^2 - 2x = 0 -> x = 0, 1. int_0^1 (2x - 2x^2) dx = 1 - 2/3 = 1/3
    qs.append(mcq(
        'hard', S3,
        'គណនាផ្ទៃក្រឡាខណ្ឌដោយប៉ារ៉ាបូលពីរ $y = x^2$ និង $y = 2x - x^2$ ។',
        r'$\frac{1}{3}$',
        [r'$\frac{2}{3}$', r'$\frac{1}{6}$', r'$1$'],
        'ចំណុចប្រសព្វ៖ $x^2 = 2x - x^2 \\iff x = 0, 1$ ។ $A = \\int_0^1 (2x - 2x^2)\\,dx = 1 - \\frac{2}{3} = \\frac{1}{3}$។',
        bloom='Analyze',
    ))

    # 28 (Analyze) - y = sqrt(x) and y = x^2
    # int_0^1 (sqrt(x) - x^2) dx = 2/3 - 1/3 = 1/3
    qs.append(mcq(
        'hard', S3,
        'គណនាផ្ទៃក្រឡាខណ្ឌដោយក្រាប $y = \\sqrt{x}$ និង $y = x^2$ ។',
        r'$\frac{1}{3}$',
        [r'$\frac{2}{3}$', r'$\frac{1}{6}$', r'$\frac{1}{2}$'],
        'លើ $[0, 1]$ យើងមាន $\\sqrt{x} \\ge x^2$ ដូច្នេះ $A = \\int_0^1 (\\sqrt{x} - x^2)\\,dx = \\frac{2}{3} - \\frac{1}{3} = \\frac{1}{3}$។',
        bloom='Analyze',
    ))

    # 29 (Evaluate) - parameter k such that area under y = kx^2 on [0, 2] equals 16
    # int_0^2 kx^2 dx = 8k/3 = 16 -> k = 6
    qs.append(mcq(
        'hard', S2,
        'កំណត់តម្លៃថេរវិជ្ជមាន $k$ ដើម្បីឲ្យផ្ទៃក្រឡាខណ្ឌដោយក្រាប $y = kx^2$ អ័ក្ស $Ox$ និងបន្ទាត់ $x = 0, x = 2$ ស្មើនឹង $16$ ។',
        r'$k = 6$',
        [r'$k = 3$', r'$k = 4$', r'$k = 8$'],
        '$A = \\int_0^2 kx^2\\,dx = \\frac{8k}{3} = 16 \\implies k = 6$។',
        bloom='Evaluate',
    ))

    # 30 (Analyze) - y = 1/x and y = 5/2 - x -> x = 1/2, 2
    # int_{1/2}^2 (5/2 - x - 1/x) dx = [5x/2 - x^2/2 - ln x]_{1/2}^2 = (5 - 2 - ln 2) - (5/4 - 1/8 - ln(1/2)) = 3 - 9/8 - 2 ln 2 = 15/8 - 2 ln 2
    qs.append(mcq(
        'hard', S3,
        'គណនាផ្ទៃក្រឡាខណ្ឌដោយអ៊ីពែរបូល $y = \\frac{1}{x}$ និងបន្ទាត់ $y = \\frac{5}{2} - x$ ។',
        r'$\frac{15}{8} - 2\ln 2$',
        [r'$\frac{15}{8} - \ln 2$', r'$\frac{9}{8} - 2\ln 2$', r'$\frac{15}{8} + 2\ln 2$'],
        'ចំណុចប្រសព្វគឺ $x = \\frac{1}{2}$ និង $x = 2$ ។ $A = \\int_{1/2}^2 \\left(\\frac{5}{2} - x - \\frac{1}{x}\\right)dx = \\frac{15}{8} - 2\\ln 2$។',
        bloom='Analyze',
    ))

    # 31 (Evaluate) - tangent to y = e^x at x = 0: y = x + 1, area between e^x, y=x+1, and x=1
    # int_0^1 (e^x - x - 1) dx = [e^x - x^2/2 - x]_0^1 = (e - 3/2) - 1 = e - 5/2
    qs.append(mcq(
        'hard', S3,
        'បន្ទាត់ប៉ះនឹងក្រាប $y = e^x$ ត្រង់ $x = 0$ គឺ $y = x + 1$ ។ គណនាផ្ទៃក្រឡាខណ្ឌដោយក្រាប $y = e^x$ បន្ទាត់ប៉ះនេះ និងបន្ទាត់ $x = 1$ ។',
        r'$e - \frac{5}{2}$',
        [r'$e - \frac{3}{2}$', r'$e - 2$', r'$e - 1$'],
        '$A = \\int_0^1 (e^x - x - 1)\\,dx = \\left[e^x - \\frac{x^2}{2} - x\\right]_0^1 = e - \\frac{3}{2} - 1 = e - \\frac{5}{2}$។',
        bloom='Evaluate',
    ))

    # =========================================================================
    # MCQ PISA (5): Analyze, Evaluate, Create (Real-world contexts)
    # =========================================================================
    # 32 (Analyze) - PISA: land parcel bounded by river curve y = 6x - x^2 (in 10m units) and road y = 0
    # int_0^6 (6x - x^2) dx = 108 - 72 = 36 (in 100 m^2 units -> 3600 m^2)
    qs.append(mcq(
        'pisa', S2,
        'ដីស្រែមួយកន្លែងខណ្ឌដោយផ្លូវត្រង់ (អ័ក្ស $Ox$) និងព្រែកកោងតាមសមីការ $y = 6x - x^2$ (គិតជាឯកតា $10\\,\\text{m}$) ។ តើផ្ទៃដីស្រែនេះមានទំហំប៉ុន្មានម៉ែត្រការ៉េ?',
        r'$3600\,\text{m}^2$',
        [r'$36\,\text{m}^2$', r'$360\,\text{m}^2$', r'$7200\,\text{m}^2$'],
        'ក្រាបកាត់អ័ក្ស $Ox$ ត្រង់ $x = 0$ និង $x = 6$ ។ $A = \\int_0^6 (6x - x^2)\\,dx = 36$ ឯកតាផ្ទៃ $= 36 \\times 100 = 3600\\,\\text{m}^2$។',
        bloom='Analyze',
    ))

    # 33 (Apply) - PISA: parabolic arch bridge opening y = 9 - x^2 (meters), width 6m, height 9m
    # int_{-3}^3 (9 - x^2) dx = 2*(27 - 9) = 36 m^2
    qs.append(mcq(
        'pisa', S2,
        'ក្លោងទ្វារស្ពានរាងប៉ារ៉ាបូលមានសមីការ $y = 9 - x^2$ (គិតជាម៉ែត្រ) ដែល $y=0$ ជាផ្ទៃទឹក។ គណនាផ្ទៃមុខកាត់នៃចន្លោះក្រោមក្លោងទ្វារនេះ។',
        r'$36\,\text{m}^2$',
        [r'$27\,\text{m}^2$', r'$54\,\text{m}^2$', r'$18\,\text{m}^2$'],
        'ជើងក្លោងទ្វារស្ថិតត្រង់ $x = -3$ និង $x = 3$ ។ $A = \\int_{-3}^3 (9 - x^2)\\,dx = 2\\left[9x - \\frac{x^3}{3}\\right]_0^3 = 36\\,\\text{m}^2$។',
        bloom='Apply',
    ))

    # 34 (Evaluate) - PISA: Solar panel roof cross-section / Riemann approximation from table
    # t = 0, 2, 4, 6 hours; P(t) = 0, 3, 5, 2 kW. Left Riemann sum with dt = 2: (0+3+5)*2 = 16 kWh
    qs.append(mcq(
        'pisa', S1,
        'តារាងបង្ហាញអានុភាព $P(t)$ ($\text{kW}$) នៃផ្ទាំងសូឡាតាមម៉ោង $t$៖ $P(0)=0,\\; P(2)=3,\\; P(4)=5,\\; P(6)=2$ ។ គណនាថាមពលប្រហែល (ជា $\\text{kWh}$) លើ $[0, 6]$ ដោយប្រើផលបូករីម៉ាន់ចុងខាងឆ្វេងជាមួយ $n = 3$ ។',
        r'$16\,\text{kWh}$',
        [r'$20\,\text{kWh}$', r'$10\,\text{kWh}$', r'$8\,\text{kWh}$'],
        '$\\Delta t = \\frac{6-0}{3} = 2$ ។ $E \\approx [P(0) + P(2) + P(4)] \\cdot 2 = (0 + 3 + 5) \\cdot 2 = 16\\,\\text{kWh}$។',
        bloom='Evaluate',
    ))

    # 35 (Analyze) - PISA: Design of a leaf-shaped logo between y = x^2 and y = sqrt(x) scaled by 10 cm
    # area = 1/3 * 100 cm^2
    qs.append(mcq(
        'pisa', S3,
        'និមិត្តសញ្ញាស្លឹកឈើមួយរចនាឡើងរវាងក្រាប $y = \\sqrt{x}$ និង $y = x^2$ (ដោយ $1$ ឯកតា $= 6\\,\\text{cm}$) ។ តើផ្ទៃក្រឡានៃនិមិត្តសញ្ញានេះស្មើនឹងប៉ុន្មាន $\\text{cm}^2$?',
        r'$12\,\text{cm}^2$',
        [r'$2\,\text{cm}^2$', r'$6\,\text{cm}^2$', r'$24\,\text{cm}^2$'],
        'ផ្ទៃក្រឡាក្នុងប្លង់គោលគឺ $\\int_0^1 (\\sqrt{x} - x^2)\\,dx = \\frac{1}{3}$ ឯកតា។ ដោយ $1$ ឯកតាផ្ទៃ $= 6^2 = 36\\,\\text{cm}^2$ នោះ $A = \\frac{36}{3} = 12\\,\\text{cm}^2$។',
        bloom='Analyze',
    ))

    # 36 (Create) - PISA: bisecting area under y = 3x^2 on [0, 2] by vertical line x = c
    # int_0^2 3x^2 dx = 8 -> int_0^c 3x^2 dx = c^3 = 4 -> c = cbrt(4)
    qs.append(mcq(
        'pisa', S2,
        'វិស្វករម្នាក់ចង់បែងចែកផ្ទៃកញ្ចក់រាងក្រោមក្រាប $y = 3x^2$ លើ $[0, 2]$ ជាពីរផ្នែកមានផ្ទៃក្រឡាស្មើគ្នាដោយបន្ទាត់ឈរ $x = c$ ។ តើ $c$ មានតម្លៃស្មើប៉ុន្មាន?',
        r'$\sqrt[3]{4}$',
        [r'$1$', r'$\sqrt{2}$', r'$\frac{3}{2}$'],
        'ផ្ទៃសរុបគឺ $\\int_0^2 3x^2\\,dx = 8$ ។ ត្រូវរក $c$ ដែល $\\int_0^c 3x^2\\,dx = c^3 = 4 \\implies c = \\sqrt[3]{4}$។',
        bloom='Create',
    ))

    # =========================================================================
    # WRITING (14): 1 easy, 4 medium, 4 hard, 5 pisa
    # =========================================================================
    # 37 (Easy - Apply)
    qs.append(writing(
        'easy', S2,
        'គណនាផ្ទៃក្រឡាខណ្ឌដោយក្រាប $y = 3x^2 + 1$ អ័ក្ស $Ox$ និងបន្ទាត់ $x = 0, x = 2$ ។',
        r'$10$',
        '$A = \\int_0^2 (3x^2 + 1)\\,dx = [x^3 + x]_0^2 = 8 + 2 = 10$។',
        bloom='Apply',
    ))

    # 38 (Medium - Apply)
    # y = 5x - x^2 and Ox -> roots 0, 5 -> 125/6
    qs.append(writing(
        'medium', S2,
        'គណនាផ្ទៃក្រឡាខណ្ឌដោយប៉ារ៉ាបូល $y = 5x - x^2$ និងអ័ក្ស $Ox$ ។',
        r'$\frac{125}{6}$',
        'ចំណុចប្រសព្វនឹង $Ox$ គឺ $x = 0$ និង $x = 5$ ។ $A = \\int_0^5 (5x - x^2)\\,dx = \\left[\\frac{5x^2}{2} - \\frac{x^3}{3}\\right]_0^5 = \\frac{125}{2} - \\frac{125}{3} = \\frac{125}{6}$។',
        bloom='Apply',
    ))

    # 39 (Medium - Apply)
    # Riemann midpoint for f(x) = 1/x on [1, 3], n=4 -> dx = 0.5, midpoints 1.25, 1.75, 2.25, 2.75
    # 0.5*(4/5 + 4/7 + 4/9 + 4/11) = 2*(1/5+1/7+1/9+1/11) = 2*(693+495+385+315)/3465 = 2*1888/3465 = 3776/3465
    # Simpler: f(x) = x^2 + 1 on [0, 3], n=3 -> dx=1, midpoints 0.5, 1.5, 2.5 -> (1.25 + 3.25 + 7.25)*1 = 11.75 = 47/4
    qs.append(writing(
        'medium', S1,
        'គណនាផលបូកចតុកោណកែងតាមចំណុចកណ្តាលនៃចន្លោះរង សម្រាប់ $f(x) = x^2 + 1$ លើ $[0, 3]$ ជាមួយ $n = 3$ ចន្លោះរងស្មើគ្នា។',
        r'$\frac{47}{4}$',
        '$\\Delta x = 1$ ។ ចំណុចកណ្តាលគឺ $0.5, 1.5, 2.5$ ។ $S_{\\text{mid}} = (1.25 + 3.25 + 7.25)\\cdot 1 = 11.75 = \\frac{47}{4}$។',
        bloom='Apply',
    ))

    # 40 (Medium - Apply)
    # y = x^2 - 4x + 3 and y = -x^2 + 2x + 3 -> 2x^2 - 6x = 0 -> x = 0, 3 -> int_0^3 (6x - 2x^2) dx = 27 - 18 = 9
    qs.append(writing(
        'medium', S3,
        'គណនាផ្ទៃក្រឡាខណ្ឌដោយប៉ារ៉ាបូលពីរ $y = x^2 - 4x + 3$ និង $y = -x^2 + 2x + 3$ ។',
        r'$9$',
        'ដោះស្រាយ $x^2 - 4x + 3 = -x^2 + 2x + 3 \\iff 2x(x - 3) = 0 \\implies x = 0, 3$ ។ $A = \\int_0^3 (6x - 2x^2)\\,dx = \\left[3x^2 - \\frac{2x^3}{3}\\right]_0^3 = 27 - 18 = 9$។',
        bloom='Apply',
    ))

    # 41 (Medium - Analyze)
    # y = e^x - 1 on [-1, 1] -> crosses at x=0: int_{-1}^0 (1 - e^x) dx + int_0^1 (e^x - 1) dx = (1 - (1 - 1/e)) + (e - 1 - 1) = e + 1/e - 2
    qs.append(writing(
        'medium', S2,
        'គណនាផ្ទៃក្រឡាខណ្ឌដោយក្រាប $y = e^x - 1$ អ័ក្ស $Ox$ និងបន្ទាត់ $x = -1, x = 1$ ។',
        r'$e + \frac{1}{e} - 2$',
        'ក្រាបកាត់ $Ox$ ត្រង់ $x = 0$ ។ $A = \\int_{-1}^0 (1 - e^x)\\,dx + \\int_0^1 (e^x - 1)\\,dx = \\frac{1}{e} + (e - 2) = e + \\frac{1}{e} - 2$។',
        bloom='Analyze',
    ))

    # 42 (Hard - Analyze)
    # y = x^3 - 4x and y = 0 on [-2, 2] -> 2 * int_0^2 (4x - x^3) dx = 2 * (8 - 4) = 8
    qs.append(writing(
        'hard', S2,
        'គណនាផ្ទៃក្រឡាខណ្ឌដោយក្រាប $y = x^3 - 4x$ និងអ័ក្ស $Ox$ ។',
        r'$8$',
        'ចំណុចប្រសព្វនឹង $Ox$ គឺ $x = -2, 0, 2$ ។ ដោយភាពសេស $A = 2\\int_0^2 (4x - x^3)\\,dx = 2\\left[2x^2 - \\frac{x^4}{4}\\right]_0^2 = 2(8 - 4) = 8$។',
        bloom='Analyze',
    ))

    # 43 (Hard - Analyze)
    # y = cos x and y = sin x on [0, pi/2] -> intersect at pi/4.
    # int_0^{pi/4} (cos x - sin x) dx + int_{pi/4}^{pi/2} (sin x - cos x) dx = (sqrt(2)-1) + (sqrt(2)-1) = 2(sqrt(2)-1)
    qs.append(writing(
        'hard', S3,
        'គណនាផ្ទៃក្រឡាខណ្ឌដោយក្រាប $y = \\cos x$ ក្រាប $y = \\sin x$ និងបន្ទាត់ $x = 0, x = \\frac{\\pi}{2}$ ។',
        r'$2\sqrt{2} - 2$',
        'ក្រាបកាត់គ្នាត្រង់ $x = \\frac{\\pi}{4}$ ។ $A = \\int_0^{\\pi/4} (\\cos x - \\sin x)\\,dx + \\int_{\\pi/4}^{\\pi/2} (\\sin x - \\cos x)\\,dx = 2(\\sqrt{2} - 1)$។',
        bloom='Analyze',
    ))

    # 44 (Hard - Evaluate)
    # Tangent to y = ln x at x = e is y = x/e. Area between y = ln x, y = x/e, and x = 1.
    # int_1^e (x/e - ln x) dx = [x^2/(2e) - x ln x + x]_1^e = (e/2 - e + e) - (1/(2e) - 0 + 1) = e/2 - 1/(2e) - 1
    qs.append(writing(
        'hard', S3,
        'រកសមីការបន្ទាត់ប៉ះ $l$ នឹងក្រាប $y = \\ln x$ ត្រង់ចំណុច $P(e, 1)$ រួចគណនាផ្ទៃក្រឡាខណ្ឌដោយក្រាប $y = \\ln x$ បន្ទាត់ $l$ និងបន្ទាត់ $x = 1$ ។',
        r'$\frac{e}{2} - \frac{1}{2e} - 1$',
        'បន្ទាត់ប៉ះត្រង់ $P(e, 1)$ គឺ $y = \\frac{x}{e}$ ។ $A = \\int_1^e \\left(\\frac{x}{e} - \\ln x\\right)dx = \\left[\\frac{x^2}{2e} - x\\ln x + x\\right]_1^e = \\frac{e}{2} - \\frac{1}{2e} - 1$។',
        bloom='Evaluate',
    ))

    # 45 (Hard - Create)
    # Find k > 0 such that area bounded by y = x^2 and y = kx equals 9/2.
    # int_0^k (kx - x^2) dx = k^3/6 = 9/2 -> k^3 = 27 -> k = 3
    qs.append(writing(
        'hard', S3,
        'កំណត់តម្លៃថេរវិជ្ជមាន $k$ ដើម្បីឲ្យផ្ទៃក្រឡាខណ្ឌដោយប៉ារ៉ាបូល $y = x^2$ និងបន្ទាត់ $y = kx$ ស្មើនឹង $\\frac{9}{2}$ ។',
        r'$k = 3$',
        'ចំណុចប្រសព្វគឺ $x = 0, k$ ។ $A = \\int_0^k (kx - x^2)\\,dx = \\frac{k^3}{6} = \\frac{9}{2} \\implies k^3 = 27 \\implies k = 3$។',
        bloom='Create',
    ))

    # 46 (PISA - Apply)
    # Parabolic solar reflector cross section y = x^2/4 and y = 4 -> x in [-4, 4]
    # int_{-4}^4 (4 - x^2/4) dx = 2*(16 - 16/3) = 64/3
    qs.append(writing(
        'pisa', S3,
        'មុខកាត់នៃចានទទួលកាំរស្មីព្រះអាទិត្យមួយខណ្ឌដោយប៉ារ៉ាបូល $y = \\frac{x^2}{4}$ និងគែមលើ $y = 4$ (គិតជាដេស៊ីម៉ែត្រ) ។ គណនាផ្ទៃមុខកាត់នៃចន្លោះចាននេះ។',
        r'$\frac{64}{3}\,\text{dm}^2$',
        'ចំណុចប្រសព្វគឺ $x = \\pm 4$ ។ $A = \\int_{-4}^4 \\left(4 - \\frac{x^2}{4}\\right)dx = 2\\left[4x - \\frac{x^3}{12}\\right]_0^4 = \\frac{64}{3}\\,\\text{dm}^2$។',
        bloom='Apply',
    ))

    # 47 (PISA - Analyze)
    # Velocity-time graph: v(t) = 12t - 3t^2 (m/s) for t in [0, 4] -> distance = int_0^4 (12t - 3t^2) dt = 96 - 64 = 32 m
    qs.append(writing(
        'pisa', S2,
        'រថយន្តមួយធ្វើដំណើរដោយល្បឿន $v(t) = 12t - 3t^2$ ($\text{m/s}$) ចាប់ពី $t = 0$ ដល់ $t = 4$ វិនាទី។ គណនាចម្ងាយចរសរុប (ស្មើនឹងផ្ទៃក្រឡាក្រោមក្រាបល្បឿន)។',
        r'$32\,\text{m}$',
        'លើ $[0, 4]$ យើងមាន $v(t) \\ge 0$ ដូច្នេះ $d = \\int_0^4 (12t - 3t^2)\\,dt = [6t^2 - t^3]_0^4 = 96 - 64 = 32\\,\\text{m}$។',
        bloom='Analyze',
    ))

    # 48 (PISA - Evaluate)
    # Inequality of wealth / Gini-like area: Lorenz curve L(x) = x^3 on [0, 1], line y = x.
    # Area between y=x and y=x^3 is int_0^1 (x - x^3) dx = 1/2 - 1/4 = 1/4. Gini = 2 * (1/4) = 1/2.
    qs.append(writing(
        'pisa', S3,
        'ក្នុងសេដ្ឋកិច្ច ខ្សែកោងឡូរ៉ង់តាងដោយ $L(x) = x^3$ លើ $[0, 1]$ និងបន្ទាត់សមភាព $y = x$ ។ គណនាផ្ទៃក្រឡា $A$ ចន្លោះ $y = x$ និង $L(x)$ រួចទាញរកមេគុណជីនី $G = 2A$ ។',
        r'$A = \frac{1}{4},\; G = \frac{1}{2}$',
        '$A = \\int_0^1 (x - x^3)\\,dx = \\left[\\frac{x^2}{2} - \\frac{x^4}{4}\\right]_0^1 = \\frac{1}{4}$ និង $G = 2A = \\frac{1}{2}$។',
        bloom='Evaluate',
    ))

    # 49 (PISA - Analyze)
    # Lake depth profile / area between y = 2*sin(pi*x/4) and y = 0 on [0, 4] (units in 10m -> 100 m^2)
    # int_0^4 2*sin(pi*x/4) dx = [-8/pi * cos(pi*x/4)]_0^4 = 16/pi units -> 1600/pi m^2
    # Cleaner without pi in denominator: gate arch y = 4 - x^2 and inner arch y = 1 - x^2/4 on [-2, 2]
    # int_{-2}^2 ((4-x^2) - (1-x^2/4)) dx = int_{-2}^2 (3 - 3x^2/4) dx = 2*(6 - 2) = 8 m^2
    qs.append(writing(
        'pisa', S3,
        'ជញ្ជាំងក្លោងទ្វារមួយខណ្ឌនៅខាងលើដោយប៉ារ៉ាបូល $y = 4 - x^2$ និងខាងក្រោមដោយប៉ារ៉ាបូល $y = 1 - \\frac{x^2}{4}$ លើ $[-2, 2]$ (គិតជាម៉ែត្រ) ។ គណនាផ្ទៃក្រឡាជញ្ជាំងក្លោងទ្វារនេះ។',
        r'$8\,\text{m}^2$',
        '$A = \\int_{-2}^2 \\left[(4 - x^2) - \\left(1 - \\frac{x^2}{4}\\right)\\right]dx = 2\\int_0^2 \\left(3 - \\frac{3x^2}{4}\\right)dx = 2\\left[3x - \\frac{x^3}{4}\\right]_0^2 = 8\\,\\text{m}^2$។',
        bloom='Analyze',
    ))

    # 50 (PISA - Create)
    # Split region bounded by y = 4 - x^2 and Ox (area 32/3) by horizontal line y = h? Or vertical line?
    # Simpler exact: horizontal line y = c splits area between y = x^2 and y = 4 into two equal areas.
    # Total area = int_{-2}^2 (4 - x^2) dx = 32/3. Area below y=c: 2*int_0^{sqrt(c)} (c - x^2) dx = 4/3 * c^{3/2} = 16/3 -> c^{3/2} = 4 -> c = 4^{2/3} = 2*cbrt(2)
    qs.append(writing(
        'pisa', S3,
        'គេមានផ្ទៃបន្ទះលោហៈខណ្ឌដោយ $y = x^2$ និងបន្ទាត់ $y = 4$ ។ គេចង់កាត់បន្ទះនេះដោយបន្ទាត់ដេក $y = c$ ($0 < c < 4$) ដើម្បីឲ្យផ្នែកខាងក្រោមមានផ្ទៃក្រឡាស្មើពាក់កណ្តាលនៃផ្ទៃសរុប។ កំណត់តម្លៃ $c$ ។',
        r'$c = 2\sqrt[3]{2}$',
        'ផ្ទៃសរុបគឺ $\\int_{-2}^2 (4 - x^2)\\,dx = \\frac{32}{3}$ ។ ផ្ទៃខាងក្រោម $y=c$ គឺ $\\int_{-\\sqrt{c}}^{\\sqrt{c}} (c - x^2)\\,dx = \\frac{4}{3}c^{3/2} = \\frac{16}{3} \\implies c^{3/2} = 4 \\implies c = 4^{2/3} = 2\\sqrt[3]{2}$។',
        bloom='Create',
    ))

    return qs


def _verify_math():
    mp.mp.dps = 30
    tol = mp.mpf('1e-12')
    # Check Q14: int_{-2}^2 (4 - x^2) dx = 32/3
    assert abs(mp.quad(lambda x: 4 - x**2, [-2, 2]) - mp.mpf(32) / 3) < tol
    # Check Q16: int_2^6 sqrt(x-2) dx = 16/3
    assert abs(mp.quad(lambda x: mp.sqrt(x - 2), [2, 6]) - mp.mpf(16) / 3) < tol
    # Check Q21: int_0^2 (4 - x^2/2 - x) dx = 14/3
    assert abs(mp.quad(lambda x: 4 - x**2 / 2 - x, [0, 2]) - mp.mpf(14) / 3) < tol
    # Check Q22: int_{-2}^1 (x + 2 - x^2 - 2x) dx = 9/2
    assert abs(mp.quad(lambda x: x + 2 - x**2 - 2 * x, [-2, 1]) - mp.mpf(9) / 2) < tol
    # Check Q23: int_{-2}^2 (4-x^2) dx + int_2^3 (x^2-4) dx = 13
    assert abs(mp.quad(lambda x: abs(4 - x**2), [-2, 2, 3]) - mp.mpf(13)) < tol
    # Check Q25: int_0^2 |x^2 - 4x + 3| dx = 2
    assert abs(mp.quad(lambda x: abs(x**2 - 4 * x + 3), [0, 1, 2]) - mp.mpf(2)) < tol
    # Check Q30: int_{0.5}^2 (5/2 - x - 1/x) dx = 15/8 - 2 ln 2
    assert abs(mp.quad(lambda x: mp.mpf(5) / 2 - x - 1 / x, [mp.mpf(1) / 2, 2]) - (mp.mpf(15) / 8 - 2 * mp.log(2))) < tol
    # Check Q31: int_0^1 (e^x - x - 1) dx = e - 5/2
    assert abs(mp.quad(lambda x: mp.exp(x) - x - 1, [0, 1]) - (mp.e - mp.mpf(5) / 2)) < tol
    # Check Q40: int_0^3 (6x - 2x^2) dx = 9
    assert abs(mp.quad(lambda x: 6 * x - 2 * x**2, [0, 3]) - mp.mpf(9)) < tol
    # Check Q41: int_{-1}^1 |e^x - 1| dx = e + 1/e - 2
    assert abs(mp.quad(lambda x: abs(mp.exp(x) - 1), [-1, 0, 1]) - (mp.e + 1 / mp.e - 2)) < tol
    # Check Q44: int_1^e (x/e - ln x) dx = e/2 - 1/(2e) - 1
    assert abs(mp.quad(lambda x: x / mp.e - mp.log(x), [1, mp.e]) - (mp.e / 2 - 1 / (2 * mp.e) - 1)) < tol
    # Check Q49: int_{-2}^2 ((4-x^2)-(1-x^2/4)) dx = 8
    assert abs(mp.quad(lambda x: (4 - x**2) - (1 - x**2 / 4), [-2, 2]) - mp.mpf(8)) < tol


cands = build_candidates


if __name__ == '__main__':
    _verify_math()
    qs = build_candidates()
    print(f'{LESSON}: built {len(qs)} candidates, mpmath verified')
