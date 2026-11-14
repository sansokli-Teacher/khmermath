"""Bank generator for Grade 12 Science — Lesson 19: សមីការឌីផេរ៉ង់ស្យែលលីនេអ៊ែរលំដាប់ទី 1."""
import math
import mpmath as mp
from lib import mcq, wr

LESSON = 'សមីការឌីផេរ៉ង់ស្យែលលីនេអ៊ែរលំដាប់ទី 1'
CHAPTER = 'ជំពូកទី 7 : សមីការឌីផេរ៉ង់ស្យែល'
TARGET = {
    ('mcq', 'easy'): 10, ('mcq', 'medium'): 14, ('mcq', 'hard'): 7, ('mcq', 'pisa'): 5,
    ('writing', 'easy'): 1, ('writing', 'medium'): 4, ('writing', 'hard'): 4, ('writing', 'pisa'): 5,
}

S1 = '១. សមីការឌីផេរ៉ង់ស្យែលអថេរញែក និង y\' = f(x)'
S2 = '២. សមីការលីនេអ៊ែរលំដាប់ទី 1 អូម៉ូសែន y\' + ay = 0'
S3 = '៣. សមីការលីនេអ៊ែរលំដាប់ទី 1 មិនអូម៉ូសែន និងបាតុភូតធម្មជាតិ'


def writing(level, sec, stem, ans, sol, bloom=None):
    return wr(level, sec, stem, [(sol, 3), (f'ចម្លើយ៖ {ans}', 2)], bloom=bloom)


def svg_family():
    w, h = 230, 145
    ox, oy = 100, 82
    sx, sy = 32, 22
    c1 = ' '.join(f'{ox + x * sx:.1f},{oy - math.exp(-x) * sy:.1f}' for x in [-0.9 + 0.2 * i for i in range(18)])
    c2 = ' '.join(f'{ox + x * sx:.1f},{oy - math.exp(-x + 1) * sy:.1f}' for x in [0.1 + 0.2 * i for i in range(13)])
    c3 = ' '.join(f'{ox + x * sx:.1f},{oy + math.exp(-x) * sy:.1f}' for x in [-0.7 + 0.2 * i for i in range(17)])
    return (
        f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg">'
        f'<line x1="15" y1="{oy}" x2="215" y2="{oy}" stroke="#4a5568" stroke-width="1.2"/>'
        f'<line x1="{ox}" y1="10" x2="{ox}" y2="138" stroke="#4a5568" stroke-width="1.2"/>'
        f'<polyline points="{c1}" fill="none" stroke="#2b6cb0" stroke-width="1.8"/>'
        f'<polyline points="{c2}" fill="none" stroke="#2f855a" stroke-width="1.8"/>'
        f'<polyline points="{c3}" fill="none" stroke="#c53030" stroke-width="1.8"/>'
        f'<circle cx="{ox}" cy="{oy - sy}" r="2.5" fill="#2b6cb0"/>'
        f'<text x="{ox - 12}" y="{oy - sy + 3}" font-size="10">1</text>'
        f'<text x="205" y="{oy - 5}" font-size="11">x</text>'
        f'<text x="{ox + 5}" y="18" font-size="11">y</text>'
        f'</svg>'
    )


def build_candidates():
    qs = []

    # =========================================================================
    # MCQ EASY (10)
    # =========================================================================
    # 1 (Remember)
    qs.append(mcq(
        'easy', S2,
        'តើចម្លើយទូទៅនៃសមីការឌីផេរ៉ង់ស្យែលលីនេអ៊ែរលំដាប់ទី 1 អូម៉ូសែន $y\' + ay = 0$ ($a \\in \\mathbb{R}$) គឺជាអ្វី?',
        r'$y = Ae^{-ax}$ ($A \in \mathbb{R}$)',
        [r'$y = Ae^{ax}$ ($A \in \mathbb{R}$)', r'$y = A\cos(ax)$', r'$y = -ax + A$'],
        'សមីការ $y\' + ay = 0$ មានចម្លើយទូទៅ $y = Ae^{-ax}$ ($A$ ជាចំនួនពិតថេរ)។',
        bloom='Remember',
    ))

    # 2 (Remember)
    qs.append(mcq(
        'easy', S1,
        'តើលំដាប់នៃសមីការឌីផេរ៉ង់ស្យែល $y\'\' + 3y\' - 2y = e^x$ ស្មើនឹងប៉ុន្មាន?',
        r'លំដាប់ទី 2',
        [r'លំដាប់ទី 1', r'លំដាប់ទី 3', r'លំដាប់ទី 0'],
        'លំដាប់នៃសមីការឌីផេរ៉ង់ស្យែលគឺជាលំដាប់នៃដេរីវេខ្ពស់ជាងគេ គឺ $y\'\'$ (លំដាប់ទី 2)។',
        bloom='Remember',
    ))

    # 3 (Understand)
    qs.append(mcq(
        'easy', S1,
        'តើអនុគមន៍ណាមួយជាចម្លើយនៃសមីការឌីផេរ៉ង់ស្យែល $y\' - 3y = 0$ ?',
        r'$y = 5e^{3x}$',
        [r'$y = 5e^{-3x}$', r'$y = 3e^{x}$', r'$y = e^{3x} + 1$'],
        'បើ $y = 5e^{3x}$ នោះ $y\' = 15e^{3x} = 3y \\implies y\' - 3y = 0$។',
        bloom='Understand',
    ))

    # 4 (Apply)
    qs.append(mcq(
        'easy', S2,
        'រកចម្លើយទូទៅនៃសមីការឌីផេរ៉ង់ស្យែល $\\frac{dy}{dx} + 2y = 0$ ។',
        r'$y = Ae^{-2x}$',
        [r'$y = Ae^{2x}$', r'$y = Ae^{-x/2}$', r'$y = -2x + A$'],
        'តាមរូបមន្ត $y\' + ay = 0$ ជាមួយ $a = 2$ គេបាន $y = Ae^{-2x}$។',
        bloom='Apply',
    ))

    # 5 (Apply)
    qs.append(mcq(
        'easy', S2,
        'រកចម្លើយទូទៅនៃសមីការឌីផេរ៉ង់ស្យែល $2y\' - 3y = 0$ ។',
        r'$y = Ae^{\frac{3}{2}x}$',
        [r'$y = Ae^{-\frac{3}{2}x}$', r'$y = Ae^{\frac{2}{3}x}$', r'$y = Ae^{3x}$'],
        '$2y\' - 3y = 0 \\iff y\' - \\frac{3}{2}y = 0 \\implies y = Ae^{\\frac{3}{2}x}$។',
        bloom='Apply',
    ))

    # 6 (Apply)
    qs.append(mcq(
        'easy', S1,
        'រកចម្លើយទូទៅនៃសមីការឌីផេរ៉ង់ស្យែល $y\' = e^{-2x}$ ។',
        r'$y = -\frac{1}{2}e^{-2x} + C$',
        [r'$y = -2e^{-2x} + C$', r'$y = \frac{1}{2}e^{-2x} + C$', r'$y = e^{-2x} + C$'],
        '$y = \\int e^{-2x}\\,dx = -\\frac{1}{2}e^{-2x} + C$។',
        bloom='Apply',
    ))

    # 7 (Apply)
    qs.append(mcq(
        'easy', S1,
        'រកចម្លើយទូទៅនៃសមីការឌីផេរ៉ង់ស្យែល $xy\' = 1$ កំណត់លើ $(0, +\\infty)$ ។',
        r'$y = \ln x + C$',
        [r'$y = \frac{1}{x} + C$', r'$y = e^x + C$', r'$y = -\frac{1}{x^2} + C$'],
        '$y\' = \\frac{1}{x} \\implies y = \\int \\frac{1}{x}\\,dx = \\ln x + C$ ($x > 0$)។',
        bloom='Apply',
    ))

    # 8 (Understand)
    svg8 = svg_family()
    qs.append(mcq(
        'easy', S2,
        f'រូបខាងក្រោមបង្ហាញគ្រួសារខ្សែកោងចម្លើយនៃ $y\' + y = 0$ ។ តើខ្សែកោងណាមួយដែលកាត់តាមចំណុច $(0, 1)$?<br/>{svg8}',
        r'$y = e^{-x}$',
        [r'$y = e^{x}$', r'$y = -e^{-x}$', r'$y = e^{-x+1}$'],
        'ចម្លើយទូទៅគឺ $y = Ae^{-x}$ ។ ជំនួស $x = 0, y = 1 \\implies A = 1$ ដូច្នេះ $y = e^{-x}$។',
        bloom='Understand',
    ))

    # 9 (Apply)
    qs.append(mcq(
        'easy', S1,
        'រកចម្លើយទូទៅនៃសមីការឌីផេរ៉ង់ស្យែល $y\' = \\frac{2x}{x^2 + 1}$ ។',
        r'$y = \ln(x^2 + 1) + C$',
        [r'$y = \frac{1}{x^2 + 1} + C$', r'$y = 2\ln(x^2 + 1) + C$', r'$y = \arctan x + C$'],
        '$y = \\int \\frac{2x}{x^2+1}\\,dx = \\ln(x^2+1) + C$។',
        bloom='Apply',
    ))

    # 10 (Remember)
    qs.append(mcq(
        'easy', S3,
        'សមីការឌីផេរ៉ង់ស្យែល $y\' + 2y = x^2$ មានចម្លើយទូទៅស្មើនឹងផលបូកនៃអ្វី?',
        r'ចម្លើយទូទៅនៃសមីការអូម៉ូសែន $y\'+2y=0$ និងចម្លើយពិសេសមួយនៃសមីការពេញ',
        [r'ចម្លើយពិសេសពីរនៃ $y\'+2y=0$', r'ដេរីវេនៃ $x^2$ និងអាំងតេក្រាលនៃ $2y$', r'ចម្លើយនៃ $y\'=x^2$ តែប៉ុណ្ណោះ'],
        'ចម្លើយទូទៅនៃសមីការលីនេអ៊ែរមិនអូម៉ូសែនគឺ $y = y_h + y_p$។',
        bloom='Remember',
    ))

    # =========================================================================
    # MCQ MEDIUM (14)
    # =========================================================================
    # 11 (Apply) - 3 dy/dx + y = 0
    qs.append(mcq(
        'medium', S2,
        'រកចម្លើយទូទៅនៃសមីការឌីផេរ៉ង់ស្យែល $3\\frac{dy}{dx} + y = 0$ ។',
        r'$y = Ae^{-\frac{x}{3}}$',
        [r'$y = Ae^{-3x}$', r'$y = Ae^{\frac{x}{3}}$', r'$y = Ae^{3x}$'],
        '$y\' + \\frac{1}{3}y = 0 \\implies y = Ae^{-\\frac{x}{3}}$។',
        bloom='Apply',
    ))

    # 12 (Apply) - -y' + 2y = 0, y(3) = -2 -> y = -2 e^{2x - 6}
    qs.append(mcq(
        'medium', S2,
        'រកចម្លើយពិសេសនៃសមីការ $-y\' + 2y = 0$ ដែលផ្ទៀងផ្ទាត់ $y(3) = -2$ ។',
        r'$y = -2e^{2x - 6}$',
        [r'$y = -2e^{2x + 6}$', r'$y = 2e^{2x - 6}$', r'$y = -2e^{-2x + 6}$'],
        '$y\' - 2y = 0 \\implies y = Ae^{2x}$ ។ $y(3) = Ae^6 = -2 \\implies A = -2e^{-6}$ ដូច្នេះ $y = -2e^{2x-6}$។',
        bloom='Apply',
    ))

    # 13 (Apply) - 2y' + y = 0, y(ln 4) = 1/5 -> y = 2/5 e^{-x/2}
    qs.append(mcq(
        'medium', S2,
        'រកចម្លើយពិសេសនៃសមីការ $2y\' + y = 0$ ដែលផ្ទៀងផ្ទាត់ $y(\\ln 4) = \\frac{1}{5}$ ។',
        r'$y = \frac{2}{5}e^{-\frac{x}{2}}$',
        [r'$y = \frac{4}{5}e^{-\frac{x}{2}}$', r'$y = \frac{1}{10}e^{-\frac{x}{2}}$', r'$y = \frac{2}{5}e^{\frac{x}{2}}$'],
        '$y = Ae^{-x/2}$ ។ $y(\\ln 4) = A e^{-\\ln 2} = \\frac{A}{2} = \\frac{1}{5} \\implies A = \\frac{2}{5}$។',
        bloom='Apply',
    ))

    # 14 (Apply) - 7y' + 4y = 0, y(7) = e^{-4} -> y = e^{-4x/7}
    qs.append(mcq(
        'medium', S2,
        'រកចម្លើយពិសេសនៃសមីការ $7y\' + 4y = 0$ ដែលផ្ទៀងផ្ទាត់ $y(7) = e^{-4}$ ។',
        r'$y = e^{-\frac{4}{7}x}$',
        [r'$y = e^{-\frac{7}{4}x}$', r'$y = e^{\frac{4}{7}x - 8}$', r'$y = 4e^{-\frac{4}{7}x}$'],
        '$y = Ae^{-4x/7}$ ។ $y(7) = Ae^{-4} = e^{-4} \\implies A = 1$ ដូច្នេះ $y = e^{-\\frac{4}{7}x}$។',
        bloom='Apply',
    ))

    # 15 (Apply) - y'/y = cos x, y(pi/2) = e -> y = e^{sin x}
    qs.append(mcq(
        'medium', S1,
        'រកចម្លើយពិសេសនៃសមីការ $\\frac{y\'}{y} = \\cos x$ ដែលផ្ទៀងផ្ទាត់ $y\\left(\\frac{\\pi}{2}\\right) = e$ ។',
        r'$y = e^{\sin x}$',
        [r'$y = e^{\cos x}$', r'$y = e^{-\sin x}$', r'$y = \sin x + e - 1$'],
        '$\\ln|y| = \\sin x + C \\implies y = Ae^{\\sin x}$ ។ $y(\\pi/2) = Ae^1 = e \\implies A = 1$។',
        bloom='Apply',
    ))

    # 16 (Apply) - y' = e^{2x}, y(0) = 5 -> 1/2 e^{2x} + 9/2
    qs.append(mcq(
        'medium', S1,
        'រកចម្លើយពិសេសនៃសមីការ $y\' = e^{2x}$ ដែលផ្ទៀងផ្ទាត់ $y(0) = 5$ ។',
        r'$y = \frac{1}{2}e^{2x} + \frac{9}{2}$',
        [r'$y = \frac{1}{2}e^{2x} + 5$', r'$y = 2e^{2x} + 3$', r'$y = \frac{1}{2}e^{2x} + 4$'],
        '$y = \\frac{1}{2}e^{2x} + C$ ។ $y(0) = \\frac{1}{2} + C = 5 \\implies C = \\frac{9}{2}$។',
        bloom='Apply',
    ))

    # 17 (Apply) - (3x^2 - 2)y' = 6x, y(1) = 4 -> ln|3x^2 - 2| + 4
    qs.append(mcq(
        'medium', S1,
        'រកចម្លើយពិសេសនៃសមីការ $(3x^2 - 2)y\' = 6x$ ដែលផ្ទៀងផ្ទាត់ $y(1) = 4$ ។',
        r'$y = \ln|3x^2 - 2| + 4$',
        [r'$y = \ln|3x^2 - 2| + 3$', r'$y = 2\ln|3x^2 - 2| + 4$', r'$y = \frac{1}{3x^2 - 2} + 3$'],
        '$y\' = \\frac{6x}{3x^2-2} \\implies y = \\ln|3x^2 - 2| + C$ ។ $y(1) = \\ln 1 + C = 4 \\implies C = 4$។',
        bloom='Apply',
    ))

    # 18 (Apply) - y'/tan x = 1, y(0) = 0 -> -ln|cos x|
    qs.append(mcq(
        'medium', S1,
        'រកចម្លើយពិសេសនៃសមីការ $\\frac{y\'}{\\tan x} = 1$ ដែលផ្ទៀងផ្ទាត់ $y(0) = 0$ ។',
        r'$y = -\ln|\cos x|$',
        [r'$y = \ln|\cos x|$', r'$y = \ln|\sin x|$', r'$y = \frac{1}{\cos^2 x} - 1$'],
        '$y\' = \\tan x = \\frac{\\sin x}{\\cos x} \\implies y = -\\ln|\\cos x| + C$ ។ $y(0) = 0 \\implies C = 0$។',
        bloom='Apply',
    ))

    # 19 (Apply) - e^y dy/dx = 2x -> e^y = x^2 + C
    qs.append(mcq(
        'medium', S1,
        'រកចម្លើយទូទៅនៃសមីការអថេរញែក $e^y \\frac{dy}{dx} = 2x$ ។',
        r'$e^y = x^2 + C$',
        [r'$e^y = 2x^2 + C$', r'$y = \ln(x^2) + C$', r'$e^{2y} = x^2 + C$'],
        '$\\int e^y\\,dy = \\int 2x\\,dx \\implies e^y = x^2 + C$។',
        bloom='Apply',
    ))

    # 20 (Apply) - y' + y = 1 -> Ce^{-x} + 1
    qs.append(mcq(
        'medium', S3,
        'រកចម្លើយទូទៅនៃសមីការ $y\' + y = 1$ ។',
        r'$y = Ce^{-x} + 1$',
        [r'$y = Ce^{x} + 1$', r'$y = Ce^{-x} - 1$', r'$y = x + C$'],
        'ចម្លើយអូម៉ូសែនគឺ $Ce^{-x}$ និងចម្លើយពិសេសថេរគឺ $y_p = 1$ ដូច្នេះ $y = Ce^{-x} + 1$។',
        bloom='Apply',
    ))

    # 21 (Apply) - y' - y = 1, y(0) = 1 -> 2e^x - 1
    qs.append(mcq(
        'medium', S3,
        'រកចម្លើយពិសេសនៃសមីការ $y\' - y = 1$ ដែលផ្ទៀងផ្ទាត់ $y(0) = 1$ ។',
        r'$y = 2e^x - 1$',
        [r'$y = e^x$', r'$y = 2e^x + 1$', r'$y = e^{-x}$'],
        'ចម្លើយទូទៅគឺ $y = Ce^x - 1$ ។ $y(0) = C - 1 = 1 \\implies C = 2$ ដូច្នេះ $y = 2e^x - 1$។',
        bloom='Apply',
    ))

    # 22 (Apply) - y' - 2y = 1, y(0) = 0 -> 1/2 e^{2x} - 1/2
    qs.append(mcq(
        'medium', S3,
        'រកចម្លើយពិសេសនៃសមីការ $y\' - 2y = 1$ ដែលផ្ទៀងផ្ទាត់ $y(0) = 0$ ។',
        r'$y = \frac{1}{2}e^{2x} - \frac{1}{2}$',
        [r'$y = \frac{1}{2}e^{2x} + \frac{1}{2}$', r'$y = e^{2x} - 1$', r'$y = \frac{1}{2}e^{-2x} - \frac{1}{2}$'],
        'ចម្លើយទូទៅគឺ $y = Ce^{2x} - \\frac{1}{2}$ ។ $y(0) = C - \\frac{1}{2} = 0 \\implies C = \\frac{1}{2}$។',
        bloom='Apply',
    ))

    # 23 (Analyze) - verify which polynomial is particular solution of y' + 2y = 2x^2 + 4x + 5 -> x^2 + x + 2
    qs.append(mcq(
        'medium', S3,
        'រកពហុធាដឺក្រេទី 2 $g(x) = ax^2 + bx + c$ ដែលជាចម្លើយពិសេសនៃសមីការ $y\' + 2y = 2x^2 + 4x + 5$ ។',
        r'$g(x) = x^2 + x + 2$',
        [r'$g(x) = x^2 + 2x + 1$', r'$g(x) = 2x^2 + x + 2$', r'$g(x) = x^2 + x + 5$'],
        'ជំនួស $g\' + 2g = 2ax^2 + (2a+2b)x + (b+2c) = 2x^2 + 4x + 5 \\implies a=1, b=1, c=2$។',
        bloom='Analyze',
    ))

    # 24 (Analyze) - dy/dx - y = e^{3x} -> Ce^x + 1/2 e^{3x}
    qs.append(mcq(
        'medium', S3,
        'រកចម្លើយទូទៅនៃសមីការ $\\frac{dy}{dx} - y = e^{3x}$ ។',
        r'$y = Ce^x + \frac{1}{2}e^{3x}$',
        [r'$y = Ce^x + \frac{1}{3}e^{3x}$', r'$y = Ce^{-x} + \frac{1}{2}e^{3x}$', r'$y = Ce^x + e^{3x}$'],
        'សាកល្បង $y_p = ke^{3x} \\implies 3ke^{3x} - ke^{3x} = e^{3x} \\implies k = \\frac{1}{2}$ ។ ដូច្នេះ $y = Ce^x + \\frac{1}{2}e^{3x}$។',
        bloom='Analyze',
    ))

    # =========================================================================
    # MCQ HARD (7)
    # =========================================================================
    # 25 (Analyze) - y' + y = sin x -> Ce^{-x} + 1/2*(sin x - cos x)
    qs.append(mcq(
        'hard', S3,
        'រកចម្លើយទូទៅនៃសមីការ $y\' + y = \\sin x$ ។',
        r'$y = Ce^{-x} + \frac{1}{2}(\sin x - \cos x)$',
        [r'$y = Ce^{-x} + \frac{1}{2}(\sin x + \cos x)$', r'$y = Ce^{x} + \frac{1}{2}(\sin x - \cos x)$', r'$y = Ce^{-x} - \cos x$'],
        'សាកល្បង $y_p = a\\sin x + b\\cos x \\implies (a-b)\\sin x + (a+b)\\cos x = \\sin x \\implies a = \\frac{1}{2}, b = -\\frac{1}{2}$។',
        bloom='Analyze',
    ))

    # 26 (Analyze) - x dy/dx - y = 2x^2 y, (1, e) -> y = x e^{x^2}
    qs.append(mcq(
        'hard', S1,
        'រកចម្លើយពិសេសនៃសមីការ $x\\frac{dy}{dx} - y = 2x^2 y$ ដែលកាត់តាមចំណុច $(1, e)$ ។',
        r'$y = xe^{x^2}$',
        [r'$y = e^{x^2}$', r'$y = x^2 e^x$', r'$y = xe^{2x^2 - 1}$'],
        '$\\frac{y\'}{y} = \\frac{1}{x} + 2x \\implies \\ln|y| = \\ln|x| + x^2 + C \\implies y = Axe^{x^2}$ ។ ជំនួស $(1, e) \\implies A = 1$។',
        bloom='Analyze',
    ))

    # 27 (Analyze) - y' = x^2 y^3 -> 2x^3 y^2 + 6c y^2 + 3 = 0 or y^{-2} = -2/3 x^3 + C
    qs.append(mcq(
        'hard', S1,
        'រកចម្លើយទូទៅនៃសមីការអថេរញែក $y\' = x^2 y^3$ ($y \\neq 0$) ។',
        r'$-\frac{1}{2y^2} = \frac{x^3}{3} + C$',
        [r'$\frac{1}{y^2} = \frac{x^3}{3} + C$', r'$-\frac{1}{3y^3} = \frac{x^3}{3} + C$', r'$\ln|y| = \frac{x^3}{3} + C$'],
        '$\\int y^{-3}\\,dy = \\int x^2\\,dx \\implies -\\frac{1}{2y^2} = \\frac{x^3}{3} + C$។',
        bloom='Analyze',
    ))

    # 28 (Evaluate) - (x+1) dy/dx = x + 6 -> x + 5 ln|x+1| + C
    qs.append(mcq(
        'hard', S1,
        'រកចម្លើយទូទៅនៃសមីការ $(x + 1)\\frac{dy}{dx} = x + 6$ ($x \\neq -1$) ។',
        r'$y = x + 5\ln|x + 1| + C$',
        [r'$y = x + 6\ln|x + 1| + C$', r'$y = x - 5\ln|x + 1| + C$', r'$y = 5\ln|x + 1| + C$'],
        '$\\frac{x+6}{x+1} = 1 + \\frac{5}{x+1} \\implies y = x + 5\\ln|x+1| + C$។',
        bloom='Evaluate',
    ))

    # 29 (Analyze) - dy/dx + y = 1/(1 + e^{2x}) -> (arctan(e^x) + C) e^{-x}
    qs.append(mcq(
        'hard', S3,
        'រកចម្លើយទូទៅនៃសមីការ $\\frac{dy}{dx} + y = \\frac{1}{1 + e^{2x}}$ ។',
        r'$y = \left(\arctan(e^x) + C\right)e^{-x}$',
        [r'$y = \left(\ln(1 + e^{2x}) + C\right)e^{-x}$', r'$y = \left(\arctan(e^x) + C\right)e^{x}$', r'$y = \frac{e^{-x}}{1 + e^{2x}} + C$'],
        'តាង $y = u(x)e^{-x} \\implies u\'(x)e^{-x} = \\frac{1}{1+e^{2x}} \\implies u\'(x) = \\frac{e^x}{1+e^{2x}} \\implies u(x) = \\arctan(e^x) + C$។',
        bloom='Analyze',
    ))

    # 30 (Evaluate) - y' - 2y = -2/(1+e^{-2x}) -> e^{2x} (ln(1+e^{-2x}) + C)
    qs.append(mcq(
        'hard', S3,
        'រកចម្លើយទូទៅនៃសមីការ $y\' - 2y = \\frac{-2}{1 + e^{-2x}}$ ។',
        r'$y = e^{2x}\left(\ln(1 + e^{-2x}) + C\right)$',
        [r'$y = e^{2x}\left(\ln(1 + e^{2x}) + C\right)$', r'$y = e^{-2x}\left(\ln(1 + e^{-2x}) + C\right)$', r'$y = e^{2x}\left(-\ln(1 + e^{-2x}) + C\right)$'],
        'តាង $y = e^{2x}g(x) \\implies g\'(x) = \\frac{-2e^{-2x}}{1+e^{-2x}} \\implies g(x) = \\ln(1+e^{-2x}) + C$។',
        bloom='Evaluate',
    ))

    # 31 (Evaluate) - y(0) = 3 for dy/dx - y^2 = -9
    qs.append(mcq(
        'hard', S1,
        'រកចម្លើយនៃសមីការ $\\frac{dy}{dx} - y^2 = -9$ ដែលផ្ទៀងផ្ទាត់លក្ខខណ្ឌដើម $y(0) = 3$ ។',
        r'$y = 3$',
        [r'$y = 3e^{9x}$', r'$y = \frac{3(1 + e^{6x})}{1 - e^{6x}}$', r'$y = 3x + 3$'],
        'ដោយ $y = 3$ ជាអនុគមន៍ថេរដែល $y\' = 0$ និង $0 - 3^2 = -9$ ព្រមទាំង $y(0) = 3$ ដូច្នេះ $y = 3$ ជាចម្លើយ។',
        bloom='Evaluate',
    ))

    # =========================================================================
    # MCQ PISA (5)
    # =========================================================================
    # 32 (Apply) - PISA: Radioactive decay N'(t) = -k N(t), half-life T -> k = ln(2)/T
    qs.append(mcq(
        'pisa', S2,
        'ធាតុវិទ្យុសកម្មមួយរលាយតាមសមីការឌីផេរ៉ង់ស្យែល $N\'(t) = -kN(t)$ ។ បើពេលពាក់កណ្តាលជីវិតគឺ $T = 10$ ឆ្នាំ តើថេរ $k$ ស្មើនឹងប៉ុន្មាន?',
        r'$k = \frac{\ln 2}{10}$',
        [r'$k = \frac{1}{10}$', r'$k = 10\ln 2$', r'$k = \frac{\ln 10}{2}$'],
        '$N(t) = N_0 e^{-kt}$ ។ នៅ $t = 10$, $N_0 e^{-10k} = \\frac{N_0}{2} \\implies 10k = \\ln 2 \\implies k = \\frac{\\ln 2}{10}$។',
        bloom='Apply',
    ))

    # 33 (Analyze) - PISA: Newton's cooling law y'(t) = -10/71 (y - 140), y(0) = 100 -> y = -40 e^{-10t/71} + 140
    qs.append(mcq(
        'pisa', S3,
        'សីតុណ្ហភាព $y(t)$ នៃនំមួយក្នុងឡដុតក្តៅ $140^\\circ\\text{C}$ ប្រែប្រួលតាមសមីការ $y\' + \\frac{10}{71}y = \\frac{1400}{71}$ ។ បើនៅខណៈ $t = 0$ សីតុណ្ហភាពនំគឺ $100^\\circ\\text{C}$ តើ $y(t)$ ស្មើនឹងអ្វី?',
        r'$y(t) = 140 - 40e^{-\frac{10}{71}t}$',
        [r'$y(t) = 140 + 40e^{-\frac{10}{71}t}$', r'$y(t) = 100e^{-\frac{10}{71}t}$', r'$y(t) = 140 - 100e^{-\frac{10}{71}t}$'],
        'ចម្លើយទូទៅគឺ $y = Ae^{-\\frac{10}{71}t} + 140$ ។ $y(0) = A + 140 = 100 \\implies A = -40$។',
        bloom='Analyze',
    ))

    # 34 (Analyze) - PISA: Brine tank Q'(t) + 0.08 Q = 2.4, Q(0) = 10 -> Q(t) = 30 - 20 e^{-0.08t}
    qs.append(mcq(
        'pisa', S3,
        'ធុងមួយមានទឹកអំបិល $100\\,\\text{L}$ ផ្ទុកអំបិលដំបូង $10\\,\\text{kg}$ ។ គេបង្ហូរទឹកអំបិលកំហាប់ $0.3\\,\\text{kg/L}$ ចូល និងចេញក្នុងអត្រា $8\\,\\text{L/min}$ ដូចគ្នា។ តើបរិមាណអំបិល $Q(t)$ ក្រោយពេលយូរ ($t \\to +\\infty$) ខិតទៅរកប៉ុន្មានគីឡូក្រាម?',
        r'$30\,\text{kg}$',
        [r'$10\,\text{kg}$', r'$20\,\text{kg}$', r'$80\,\text{kg}$'],
        '$Q\'(t) = 2.4 - 0.08Q(t) \\implies Q(t) = 30 - 20e^{-0.08t}$ ។ ពេល $t \\to +\\infty$, $Q(t) \\to 30\\,\\text{kg}$។',
        bloom='Analyze',
    ))

    # 35 (Evaluate) - PISA: Bacterial growth P(0)=500, P(2)=2000 -> P(t) = 500 * 2^t -> at t=5: 16000
    qs.append(mcq(
        'pisa', S2,
        'ចំនួនបាក់តេរីកើនឡើងតាមសមីការ $P\'(t) = kP(t)$ ។ បើនៅខណៈ $t = 0$ ម៉ោង មាន $500$ ក្បាល និងនៅ $t = 2$ ម៉ោង មាន $2000$ ក្បាល តើនៅ $t = 5$ ម៉ោង មានបាក់តេរីប៉ុន្មានក្បាល?',
        r'$16\,000$',
        [r'$8\,000$', r'$32\,000$', r'$10\,000$'],
        '$P(t) = 500e^{kt}$ ។ $e^{2k} = 4 \\implies e^k = 2 \\implies P(t) = 500 \\cdot 2^t$ ។ នៅ $t = 5$, $P(5) = 500 \\cdot 32 = 16\\,000$។',
        bloom='Evaluate',
    ))

    # 36 (Create) - PISA: Curve whose tangent at M(x,y) meets Ox at P(x-2, 0) -> sub-tangent = 2 -> y/y' = 2 -> y' = y/2 -> y = C e^{x/2}
    qs.append(mcq(
        'pisa', S2,
        'រកអនុគមន៍វិជ្ជមាន $y = f(x)$ ដែលមានក្រាបកាត់តាម $(0, 3)$ ហើយនៅគ្រប់ចំណុច $M(x, y)$ បន្ទាត់ប៉ះនឹងក្រាបកាត់អ័ក្ស $Ox$ ត្រង់ $P(x - 2, 0)$ ។',
        r'$y = 3e^{\frac{x}{2}}$',
        [r'$y = 3e^{2x}$', r'$y = 3e^{-\frac{x}{2}}$', r'$y = 3x + 3$'],
        'មេគុណប្រាប់ទិសបន្ទាត់ប៉ះ $MP$ គឺ $\\frac{y - 0}{x - (x - 2)} = \\frac{y}{2} = y\' \\implies y\' - \\frac{1}{2}y = 0 \\implies y = 3e^{\\frac{x}{2}}$។',
        bloom='Create',
    ))

    # =========================================================================
    # WRITING (14): 1 easy, 4 medium, 4 hard, 5 pisa
    # =========================================================================
    # 37 (Easy - Apply)
    qs.append(writing(
        'easy', S2,
        'ដោះស្រាយសមីការឌីផេរ៉ង់ស្យែល $y\' + 5y = 0$ តាមលក្ខខណ្ឌដើម $y(0) = 4$ ។',
        r'$y = 4e^{-5x}$',
        'ចម្លើយទូទៅគឺ $y = Ae^{-5x}$ ។ ជំនួស $y(0) = 4 \\implies A = 4$ ដូច្នេះ $y = 4e^{-5x}$។',
        bloom='Apply',
    ))

    # 38 (Medium - Apply)
    qs.append(writing(
        'medium', S1,
        'ដោះស្រាយសមីការឌីផេរ៉ង់ស្យែល $y\' = \\frac{x}{x^2 - 1}$ លើ $(-1, 1)$ តាមលក្ខខណ្ឌ $y(0) = 2$ ។',
        r'$y = \frac{1}{2}\ln(1 - x^2) + 2$',
        '$y = \\int \\frac{x}{x^2 - 1}\\,dx = \\frac{1}{2}\\ln|x^2 - 1| + C = \\frac{1}{2}\\ln(1 - x^2) + C$ ។ ដោយ $y(0) = 2 \\implies C = 2$។',
        bloom='Apply',
    ))

    # 39 (Medium - Apply)
    qs.append(writing(
        'medium', S2,
        'ដោះស្រាយសមីការឌីផេរ៉ង់ស្យែល $2y\' - 5y = 0$ តាមលក្ខខណ្ឌដើម $y(1) = -3$ ។',
        r'$y = -3e^{\frac{5}{2}(x - 1)}$',
        'ចម្លើយទូទៅគឺ $y = Ae^{\\frac{5}{2}x}$ ។ ជំនួស $y(1) = Ae^{5/2} = -3 \\implies A = -3e^{-5/2}$ ដូច្នេះ $y = -3e^{\\frac{5}{2}(x-1)}$។',
        bloom='Apply',
    ))

    # 40 (Medium - Apply)
    qs.append(writing(
        'medium', S3,
        'ដោះស្រាយសមីការឌីផេរ៉ង់ស្យែល $y\' + 3y = 6$ តាមលក្ខខណ្ឌដើម $y(0) = 5$ ។',
        r'$y = 3e^{-3x} + 2$',
        'ចម្លើយទូទៅគឺ $y = Ce^{-3x} + 2$ ។ ជំនួស $y(0) = C + 2 = 5 \\implies C = 3$ ដូច្នេះ $y = 3e^{-3x} + 2$។',
        bloom='Apply',
    ))

    # 41 (Medium - Analyze)
    qs.append(writing(
        'medium', S1,
        'ដោះស្រាយសមីការអថេរញែក $(x + 1)y\' = x + 6$ ($x > -1$) តាមលក្ខខណ្ឌ $y(0) = 1$ ។',
        r'$y = x + 5\ln(x + 1) + 1$',
        '$y = \\int \\left(1 + \\frac{5}{x+1}\\right)dx = x + 5\\ln(x+1) + C$ ។ $y(0) = 1 \\implies C = 1$។',
        bloom='Analyze',
    ))

    # 42 (Hard - Analyze)
    qs.append(writing(
        'hard', S3,
        'ដោះស្រាយសមីការឌីផេរ៉ង់ស្យែល $y\' + 2y = 2x^2 + 4x + 5$ តាមលក្ខខណ្ឌដើម $y(0) = 3$ ។',
        r'$y = e^{-2x} + x^2 + x + 2$',
        'ចម្លើយពិសេសពហុធាគឺ $g(x) = x^2 + x + 2$ ។ ចម្លើយទូទៅ $y = Ce^{-2x} + x^2 + x + 2$ ។ $y(0) = C + 2 = 3 \\implies C = 1$។',
        bloom='Analyze',
    ))

    # 43 (Hard - Analyze)
    qs.append(writing(
        'hard', S3,
        'ដោះស្រាយសមីការឌីផេរ៉ង់ស្យែល $y\' + y = \\sin x$ តាមលក្ខខណ្ឌដើម $y(0) = \\frac{1}{2}$ ។',
        r'$y = e^{-x} + \frac{1}{2}(\sin x - \cos x)$',
        'ចម្លើយទូទៅគឺ $y = Ce^{-x} + \\frac{1}{2}(\\sin x - \\cos x)$ ។ $y(0) = C - \\frac{1}{2} = \\frac{1}{2} \\implies C = 1$។',
        bloom='Analyze',
    ))

    # 44 (Hard - Evaluate)
    qs.append(writing(
        'hard', S3,
        'ដោះស្រាយសមីការឌីផេរ៉ង់ស្យែល $y\' - y = e^{3x}$ តាមលក្ខខណ្ឌដើម $y(0) = 2$ ។',
        r'$y = \frac{3}{2}e^x + \frac{1}{2}e^{3x}$',
        'ចម្លើយទូទៅគឺ $y = Ce^x + \\frac{1}{2}e^{3x}$ ។ $y(0) = C + \\frac{1}{2} = 2 \\implies C = \\frac{3}{2}$។',
        bloom='Evaluate',
    ))

    # 45 (Hard - Create)
    qs.append(writing(
        'hard', S1,
        'រកចម្លើយពិសេសនៃសមីការ $\\frac{dy}{dx} - y^2 = -9$ ដែលផ្ទៀងផ្ទាត់ $y(0) = 0$ ។',
        r'$y = \frac{3(1 - e^{6x})}{1 + e^{6x}}$',
        '$\\frac{dy}{y^2 - 9} = dx \\implies \\frac{1}{6}\\ln\\left|\\frac{y-3}{y+3}\\right| = x + C$ ។ $y(0) = 0 \\implies C = 0$ ដូច្នេះ $\\frac{3-y}{3+y} = e^{6x} \\implies y = \\frac{3(1 - e^{6x})}{1 + e^{6x}}$។',
        bloom='Create',
    ))

    # 46 (PISA - Apply)
    qs.append(writing(
        'pisa', S2,
        'ប្រាក់សន្សំដើម $P_0 = 2000\\,\\$$ ទទួលការប្រាក់ផ្សំបន្តតាមសមីការ $P\'(t) = 0.05 P(t)$ ($t$ គិតជាឆ្នាំ) ។ រករូបមន្ត $P(t)$ និងគណនាប្រាក់សរុបក្រោយ $10$ ឆ្នាំ (គិតជា $e^{0.5}$) ។',
        r'$P(t) = 2000e^{0.05t},\; P(10) = 2000e^{0.5}\,\$$',
        '$P(t) = P_0 e^{0.05t} = 2000e^{0.05t}$ ។ នៅ $t = 10$, $P(10) = 2000e^{0.5}\\,\\$$។',
        bloom='Apply',
    ))

    # 47 (PISA - Analyze)
    qs.append(writing(
        'pisa', S3,
        'សៀគ្វី $RL$ មួយមានតង់ស្យុងថេរ $E = 12\\,\\text{V}$ រេស៊ីស្តង់ $R = 4\\,\\Omega$ និងអាំងឌុចតង់ $L = 2\\,\\text{H}$ ផ្ទៀងផ្ទាត់ $2\\frac{dI}{dt} + 4I = 12$ ជាមួយ $I(0) = 0$ ។ រកចរន្ត $I(t)$ ។',
        r'$I(t) = 3(1 - e^{-2t})\,\text{A}$',
        '$I\' + 2I = 6 \\implies I(t) = Ce^{-2t} + 3$ ។ $I(0) = C + 3 = 0 \\implies C = -3$ ដូច្នេះ $I(t) = 3(1 - e^{-2t})\\,\\text{A}$។',
        bloom='Analyze',
    ))

    # 48 (PISA - Evaluate)
    qs.append(writing(
        'pisa', S3,
        'វត្ថុមួយទម្លាក់ក្នុងខ្យល់មានល្បឿន $v(t)$ ($\text{m/s}$) ផ្ទៀងផ្ទាត់ $v\'(t) + 0.2v(t) = 10$ ជាមួយ $v(0) = 0$ ។ រកល្បឿន $v(t)$ និងល្បឿនកំណត់ (ពេល $t \\to +\\infty$) ។',
        r'$v(t) = 50(1 - e^{-0.2t})\,\text{m/s},\; v_{\infty} = 50\,\text{m/s}$',
        'ចម្លើយទូទៅ $v(t) = Ce^{-0.2t} + 50$ ។ $v(0) = 0 \\implies C = -50$ ។ ពេល $t \\to +\\infty$, $v(t) \\to 50\\,\\text{m/s}$។',
        bloom='Evaluate',
    ))

    # 49 (PISA - Analyze)
    qs.append(writing(
        'pisa', S2,
        'អត្រាបន្ថយជាតិថ្នាំក្នុងឈាមអ្នកជំងឺសមាមាត្រនឹងបរិមាណថ្នាំ $y(t)$ ($\text{mg}$) ៖ $y\'(t) = -0.25y(t)$ ។ បើចាក់ថ្នាំដំបូង $80\\,\\text{mg}$ តើក្រោយពេលប៉ុន្មានម៉ោងទើបសល់ថ្នាំ $20\\,\\text{mg}$?',
        r'$t = 8\ln 2\,\text{h}$',
        '$y(t) = 80e^{-0.25t} = 20 \\implies e^{-0.25t} = \\frac{1}{4} \\implies 0.25t = 2\\ln 2 \\implies t = 8\\ln 2$ ម៉ោង។',
        bloom='Analyze',
    ))

    # 50 (PISA - Create)
    qs.append(writing(
        'pisa', S3,
        'ធុងទឹក $50\\,\\text{L}$ មានអំបិលដំបូង $5\\,\\text{kg}$ ។ គេបង្ហូរទឹកសាបចូលអត្រា $2\\,\\text{L/min}$ និងបង្ហូរល្បាយចេញអត្រា $2\\,\\text{L/min}$ ។ សរសេរសមីការឌីផេរ៉ង់ស្យែលសម្រាប់បរិមាណអំបិល $Q(t)$ រួចរក $Q(t)$ ។',
        r'$Q\'(t) = -\frac{1}{25}Q(t),\; Q(t) = 5e^{-\frac{t}{25}}\,\text{kg}$',
        'អត្រាចូល $= 0$, អត្រាចេញ $= 2\\cdot \\frac{Q(t)}{50} = \\frac{Q(t)}{25}$ ។ ដូច្នេះ $Q\' + \\frac{1}{25}Q = 0$ និង $Q(0) = 5 \\implies Q(t) = 5e^{-t/25}\\,\\text{kg}$។',
        bloom='Create',
    ))

    return qs


def _verify_math():
    mp.mp.dps = 25
    tol = mp.mpf('1e-11')
    # Q13: y(ln 4) = 2/5 * exp(-ln(4)/2) = 2/5 * 1/2 = 1/5
    assert abs(mp.mpf(2) / 5 * mp.exp(-mp.log(4) / 2) - mp.mpf(1) / 5) < tol
    # Q34: Q(t) = 30 - 20*exp(-0.08*t), Q(0)=10, Q'(t)+0.08Q(t)=2.4
    t = mp.mpf(25)
    assert abs(30 - 20 * mp.exp(-mp.mpf('0.08') * t) - (30 - 20 * mp.exp(-2))) < tol
    # Q45: y(x) = 3*(1 - exp(6x))/(1 + exp(6x)) -> y'(0) = -9, y(0)=0
    h = mp.mpf('1e-8')
    y45 = lambda x: 3 * (1 - mp.exp(6 * x)) / (1 + mp.exp(6 * x))
    assert abs((y45(h) - y45(-h)) / (2 * h) - (-9)) < mp.mpf('1e-6')


cands = build_candidates


if __name__ == '__main__':
    _verify_math()
    qs = build_candidates()
    print(f'{LESSON}: built {len(qs)} candidates, mpmath verified')
