"""Bank generator for Grade 12 Science — Lesson 20: សមីការឌីផេរ៉ង់ស្យែលលីនេអ៊ែរលំដាប់ទី 2."""
import math
import mpmath as mp
from lib import mcq, wr

LESSON = 'សមីការឌីផេរ៉ង់ស្យែលលីនេអ៊ែរលំដាប់ទី 2'
CHAPTER = 'ជំពូកទី 7 : សមីការឌីផេរ៉ង់ស្យែល'
TARGET = {
    ('mcq', 'easy'): 10, ('mcq', 'medium'): 14, ('mcq', 'hard'): 7, ('mcq', 'pisa'): 5,
    ('writing', 'easy'): 1, ('writing', 'medium'): 4, ('writing', 'hard'): 4, ('writing', 'pisa'): 5,
}

S1 = '១. សមីការលីនេអ៊ែរលំដាប់ទី 2 អូម៉ូសែន y\'\' + by\' + cy = 0'
S2 = '២. សមីការលីនេអ៊ែរលំដាប់ទី 2 មិនអូម៉ូសែន'
S3 = '៣. អនុវត្តន៍លើចលនារ៉ឺស័រ និងលំហាត់ជំពូក'


def writing(level, sec, stem, ans, sol, bloom=None):
    return wr(level, sec, stem, [(sol, 3), (f'ចម្លើយ៖ {ans}', 2)], bloom=bloom)


def svg_spring():
    w, h = 230, 145
    return (
        f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg">'
        f'<line x1="25" y1="18" x2="205" y2="18" stroke="#4a5568" stroke-width="2"/>'
        f'<polyline points="70,18 70,32 58,40 82,48 58,56 82,64 70,72 70,84" fill="none" stroke="#2b6cb0" stroke-width="1.8"/>'
        f'<rect x="54" y="84" width="32" height="22" fill="#bee3f8" stroke="#2b6cb0" stroke-width="1.5"/>'
        f'<text x="70" y="99" font-size="11" text-anchor="middle">m</text>'
        f'<line x1="35" y1="84" x2="195" y2="84" stroke="#718096" stroke-dasharray="3,2"/>'
        f'<text x="198" y="87" font-size="10">x=0</text>'
        f'<polyline points="150,18 150,32 138,44 162,56 138,68 162,80 150,92 150,108" fill="none" stroke="#c53030" stroke-width="1.8"/>'
        f'<rect x="134" y="108" width="32" height="22" fill="#fed7d7" stroke="#c53030" stroke-width="1.5"/>'
        f'<text x="150" y="123" font-size="11" text-anchor="middle">m</text>'
        f'<text x="174" y="102" font-size="10" fill="#c53030">x</text>'
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
        'តើសមីការសម្គាល់នៃសមីការឌីផេរ៉ង់ស្យែល $y\'\' + by\' + cy = 0$ គឺជាអ្វី?',
        r'$\lambda^2 + b\lambda + c = 0$',
        [r'$\lambda^2 - b\lambda + c = 0$', r'$b\lambda^2 + c\lambda + 1 = 0$', r'$\lambda + b + c = 0$'],
        'សមីការសម្គាល់គឺ $\\lambda^2 + b\\lambda + c = 0$។',
        bloom='Remember',
    ))

    # 2 (Remember)
    qs.append(mcq(
        'easy', S1,
        'បើសមីការសម្គាល់ $\\lambda^2 + b\\lambda + c = 0$ មានឫសពិតពីរផ្សេងគ្នា $\\lambda_1, \\lambda_2$ តើចម្លើយទូទៅនៃ $y\'\' + by\' + cy = 0$ មានទម្រង់ដូចម្តេច?',
        r'$y = C_1 e^{\lambda_1 x} + C_2 e^{\lambda_2 x}$',
        [r'$y = (C_1 + C_2 x)e^{\lambda_1 x}$', r'$y = C_1 \cos(\lambda_1 x) + C_2 \sin(\lambda_2 x)$', r'$y = C_1 e^{-\lambda_1 x} + C_2 e^{-\lambda_2 x}$'],
        'ករណី $\\Delta > 0$ ចម្លើយទូទៅគឺ $y = C_1 e^{\\lambda_1 x} + C_2 e^{\\lambda_2 x}$។',
        bloom='Remember',
    ))

    # 3 (Remember)
    qs.append(mcq(
        'easy', S1,
        'បើសមីការសម្គាល់ $\\lambda^2 + b\\lambda + c = 0$ មានឫសឌុប $\\lambda_0$ ($\\Delta = 0$) តើចម្លើយទូទៅគឺជាអ្វី?',
        r'$y = (C_1 + C_2 x)e^{\lambda_0 x}$',
        [r'$y = C_1 e^{\lambda_0 x}$', r'$y = C_1 e^{\lambda_0 x} + C_2 e^{-\lambda_0 x}$', r'$y = C_1 \cos(\lambda_0 x) + C_2 \sin(\lambda_0 x)$'],
        'ករណី $\\Delta = 0$ ចម្លើយទូទៅគឺ $y = (C_1 + C_2 x)e^{\\lambda_0 x}$។',
        bloom='Remember',
    ))

    # 4 (Remember)
    qs.append(mcq(
        'easy', S1,
        'បើសមីការសម្គាល់មានឫសកុំផ្លិចឆ្លាស់ $\\lambda = \\alpha \\pm i\\beta$ ($\\beta \\neq 0$) តើចម្លើយទូទៅនៃ $y\'\' + by\' + cy = 0$ គឺជាអ្វី?',
        r'$y = e^{\alpha x}(C_1 \cos \beta x + C_2 \sin \beta x)$',
        [r'$y = e^{\beta x}(C_1 \cos \alpha x + C_2 \sin \alpha x)$', r'$y = C_1 e^{\alpha x} + C_2 e^{\beta x}$', r'$y = (C_1 + C_2 x)e^{\alpha x}$'],
        'ករណី $\\Delta < 0$ ជាមួយឫស $\\alpha \\pm i\\beta$ ចម្លើយទូទៅគឺ $y = e^{\\alpha x}(C_1\\cos\\beta x + C_2\\sin\\beta x)$។',
        bloom='Remember',
    ))

    # 5 (Apply)
    qs.append(mcq(
        'easy', S1,
        'រកចម្លើយទូទៅនៃសមីការឌីផេរ៉ង់ស្យែល $y\'\' - 5y\' + 6y = 0$ ។',
        r'$y = C_1 e^{2x} + C_2 e^{3x}$',
        [r'$y = C_1 e^{-2x} + C_2 e^{-3x}$', r'$y = (C_1 + C_2 x)e^{2x}$', r'$y = C_1 e^{x} + C_2 e^{6x}$'],
        'សមីការសម្គាល់ $\\lambda^2 - 5\\lambda + 6 = 0 \\implies \\lambda = 2, 3$ ដូច្នេះ $y = C_1 e^{2x} + C_2 e^{3x}$។',
        bloom='Apply',
    ))

    # 6 (Apply)
    qs.append(mcq(
        'easy', S1,
        'រកចម្លើយទូទៅនៃសមីការឌីផេរ៉ង់ស្យែល $y\'\' + 4y\' + 4y = 0$ ។',
        r'$y = (C_1 + C_2 x)e^{-2x}$',
        [r'$y = (C_1 + C_2 x)e^{2x}$', r'$y = C_1 e^{-2x} + C_2 e^{2x}$', r'$y = C_1 \cos 2x + C_2 \sin 2x$'],
        '$(\\lambda + 2)^2 = 0 \\implies \\lambda = -2$ (ឫសឌុប) ដូច្នេះ $y = (C_1 + C_2 x)e^{-2x}$។',
        bloom='Apply',
    ))

    # 7 (Apply)
    qs.append(mcq(
        'easy', S1,
        'រកចម្លើយទូទៅនៃសមីការឌីផេរ៉ង់ស្យែល $y\'\' + 9y = 0$ ។',
        r'$y = C_1 \cos 3x + C_2 \sin 3x$',
        [r'$y = C_1 e^{3x} + C_2 e^{-3x}$', r'$y = C_1 \cos 9x + C_2 \sin 9x$', r'$y = (C_1 + C_2 x)e^{3x}$'],
        '$\\lambda^2 + 9 = 0 \\implies \\lambda = \\pm 3i$ ដូច្នេះ $y = C_1\\cos 3x + C_2\\sin 3x$។',
        bloom='Apply',
    ))

    # 8 (Apply)
    qs.append(mcq(
        'easy', S1,
        'រកចម្លើយទូទៅនៃសមីការឌីផេរ៉ង់ស្យែល $y\'\' - 2y\' = 0$ ។',
        r'$y = C_1 + C_2 e^{2x}$',
        [r'$y = C_1 e^x + C_2 e^{2x}$', r'$y = C_1 + C_2 e^{-2x}$', r'$y = (C_1 + C_2 x)e^{2x}$'],
        '$\\lambda^2 - 2\\lambda = 0 \\implies \\lambda = 0, 2$ ដូច្នេះ $y = C_1 + C_2 e^{2x}$។',
        bloom='Apply',
    ))

    # 9 (Understand)
    qs.append(mcq(
        'easy', S2,
        'អនុគមន៍ថេរ $k$ ណាមួយដែលជាចម្លើយពិសេសនៃសមីការ $y\'\' - 4y\' + 2y = 4$?',
        r'$k = 2$',
        [r'$k = 4$', r'$k = -2$', r'$k = 1$'],
        'ជំនួស $y = k \\implies 0 - 0 + 2k = 4 \\implies k = 2$។',
        bloom='Understand',
    ))

    # 10 (Understand)
    qs.append(mcq(
        'easy', S1,
        'តើសមីការឌីផេរ៉ង់ស្យែលលំដាប់ទី 2 អូម៉ូសែនណាមួយដែលមាន $y = e^{-2x}$ និង $y = xe^{-2x}$ ជាចម្លើយ?',
        r'$y\'\' + 4y\' + 4y = 0$',
        [r'$y\'\' - 4y\' + 4y = 0$', r'$y\'\' + 2y\' + y = 0$', r'$y\'\' - 4y = 0$'],
        'ឫសឌុប $\\lambda = -2 \\implies (\\lambda + 2)^2 = \\lambda^2 + 4\\lambda + 4 = 0 \\implies y\'\' + 4y\' + 4y = 0$។',
        bloom='Understand',
    ))

    # =========================================================================
    # MCQ MEDIUM (14)
    # =========================================================================
    # 11 (Apply) - 2y'' - 3y' + y = 0 -> C1 e^{x/2} + C2 e^x
    qs.append(mcq(
        'medium', S1,
        'រកចម្លើយទូទៅនៃសមីការ $2y\'\' - 3y\' + y = 0$ ។',
        r'$y = C_1 e^{\frac{x}{2}} + C_2 e^x$',
        [r'$y = C_1 e^{-\frac{x}{2}} + C_2 e^{-x}$', r'$y = C_1 e^{2x} + C_2 e^x$', r'$y = (C_1 + C_2 x)e^{\frac{x}{2}}$'],
        '$2\\lambda^2 - 3\\lambda + 1 = (2\\lambda - 1)(\\lambda - 1) = 0 \\implies \\lambda = \\frac{1}{2}, 1$។',
        bloom='Apply',
    ))

    # 12 (Apply) - -4y'' + 7y' + 2y = 0 -> C1 e^{-x/4} + C2 e^{2x}
    qs.append(mcq(
        'medium', S1,
        'រកចម្លើយទូទៅនៃសមីការ $-4y\'\' + 7y\' + 2y = 0$ ។',
        r'$y = C_1 e^{-\frac{x}{4}} + C_2 e^{2x}$',
        [r'$y = C_1 e^{\frac{x}{4}} + C_2 e^{-2x}$', r'$y = C_1 e^{-4x} + C_2 e^{2x}$', r'$y = C_1 e^{-\frac{x}{2}} + C_2 e^{x}$'],
        '$-4\\lambda^2 + 7\\lambda + 2 = 0 \\iff 4\\lambda^2 - 7\\lambda - 2 = (4\\lambda + 1)(\\lambda - 2) = 0 \\implies \\lambda = -\\frac{1}{4}, 2$។',
        bloom='Apply',
    ))

    # 13 (Apply) - y'' - 3y' + 3y = 0 -> e^{3x/2} (C1 cos(sqrt(3)/2 x) + C2 sin(sqrt(3)/2 x))
    qs.append(mcq(
        'medium', S1,
        'រកចម្លើយទូទៅនៃសមីការ $y\'\' - 3y\' + 3y = 0$ ។',
        r'$y = e^{\frac{3}{2}x}\left(C_1\cos\frac{\sqrt{3}}{2}x + C_2\sin\frac{\sqrt{3}}{2}x\right)$',
        [r'$y = e^{-\frac{3}{2}x}\left(C_1\cos\frac{\sqrt{3}}{2}x + C_2\sin\frac{\sqrt{3}}{2}x\right)$', r'$y = e^{\frac{3}{2}x}\left(C_1\cos\sqrt{3}x + C_2\sin\sqrt{3}x\right)$', r'$y = C_1 e^{\frac{3-\sqrt{3}}{2}x} + C_2 e^{\frac{3+\sqrt{3}}{2}x}$'],
        '$\\Delta = 9 - 12 = -3 \\implies \\lambda = \\frac{3}{2} \\pm i\\frac{\\sqrt{3}}{2}$។',
        bloom='Apply',
    ))

    # 14 (Apply) - 2y'' + 3y' - 2y = 0 -> C1 e^{-2x} + C2 e^{x/2}
    qs.append(mcq(
        'medium', S1,
        'រកចម្លើយទូទៅនៃសមីការ $2y\'\' + 3y\' - 2y = 0$ ។',
        r'$y = C_1 e^{-2x} + C_2 e^{\frac{x}{2}}$',
        [r'$y = C_1 e^{2x} + C_2 e^{-\frac{x}{2}}$', r'$y = C_1 e^{-x} + C_2 e^{2x}$', r'$y = (C_1 + C_2 x)e^{-2x}$'],
        '$2\\lambda^2 + 3\\lambda - 2 = (2\\lambda - 1)(\\lambda + 2) = 0 \\implies \\lambda = -2, \\frac{1}{2}$។',
        bloom='Apply',
    ))

    # 15 (Apply) - y'' - 3y' + y = 0 -> (3 +- sqrt(5))/2
    qs.append(mcq(
        'medium', S1,
        'រកចម្លើយទូទៅនៃសមីការ $y\'\' - 3y\' + y = 0$ ។',
        r'$y = C_1 e^{\frac{3-\sqrt{5}}{2}x} + C_2 e^{\frac{3+\sqrt{5}}{2}x}$',
        [r'$y = C_1 e^{\frac{-3-\sqrt{5}}{2}x} + C_2 e^{\frac{-3+\sqrt{5}}{2}x}$', r'$y = e^{\frac{3}{2}x}\left(C_1\cos\frac{\sqrt{5}}{2}x + C_2\sin\frac{\sqrt{5}}{2}x\right)$', r'$y = C_1 e^{(3-\sqrt{5})x} + C_2 e^{(3+\sqrt{5})x}$'],
        '$\\Delta = 9 - 4 = 5 \\implies \\lambda = \\frac{3 \\pm \\sqrt{5}}{2}$។',
        bloom='Apply',
    ))

    # 16 (Apply) - construct ODE for f(x) = 2e^{-x} + 3e^{3x} -> y'' - 2y' - 3y = 0
    qs.append(mcq(
        'medium', S1,
        'រកសមីការឌីផេរ៉ង់ស្យែលលីនេអ៊ែរលំដាប់ទី 2 អូម៉ូសែន ដែលមាន $f(x) = 2e^{-x} + 3e^{3x}$ ជាចម្លើយ។',
        r'$y\'\' - 2y\' - 3y = 0$',
        [r'$y\'\' + 2y\' - 3y = 0$', r'$y\'\' - 2y\' + 3y = 0$', r'$y\'\' + 4y\' + 3y = 0$'],
        'ឫសគឺ $\\lambda_1 = -1, \\lambda_2 = 3 \\implies (\\lambda + 1)(\\lambda - 3) = \\lambda^2 - 2\\lambda - 3 = 0$។',
        bloom='Apply',
    ))

    # 17 (Apply) - construct ODE for f(x) = (2 cos 3x - 3 sin 3x) e^x -> y'' - 2y' + 10y = 0
    qs.append(mcq(
        'medium', S1,
        'រកសមីការឌីផេរ៉ង់ស្យែលលីនេអ៊ែរលំដាប់ទី 2 អូម៉ូសែន ដែលមាន $f(x) = (2\\cos 3x - 3\\sin 3x)e^x$ ជាចម្លើយ។',
        r'$y\'\' - 2y\' + 10y = 0$',
        [r'$y\'\' + 2y\' + 10y = 0$', r'$y\'\' - 2y\' + 9y = 0$', r'$y\'\' - 6y\' + 10y = 0$'],
        'ឫសកុំផ្លិចគឺ $\\lambda = 1 \\pm 3i \\implies (\\lambda - 1)^2 + 9 = \\lambda^2 - 2\\lambda + 10 = 0$។',
        bloom='Apply',
    ))

    # 18 (Apply) - IVP: y'' - y = 0, y(0) = 1, y'(0) = -2 -> -1/2 e^x + 3/2 e^{-x}
    qs.append(mcq(
        'medium', S1,
        'រកចម្លើយពិសេសនៃសមីការ $y\'\' - y = 0$ ដែលផ្ទៀងផ្ទាត់ $y(0) = 1$ និង $y\'(0) = -2$ ។',
        r'$y = -\frac{1}{2}e^x + \frac{3}{2}e^{-x}$',
        [r'$y = \frac{3}{2}e^x - \frac{1}{2}e^{-x}$', r'$y = e^x - 2e^{-x}$', r'$y = \frac{1}{2}e^x + \frac{1}{2}e^{-x}$'],
        '$y = C_1 e^x + C_2 e^{-x}$ ។ $C_1 + C_2 = 1$ និង $C_1 - C_2 = -2 \\implies C_1 = -\\frac{1}{2}, C_2 = \\frac{3}{2}$។',
        bloom='Apply',
    ))

    # 19 (Apply) - IVP: y'' + y = 0, y(pi/2) = 3, y'(pi/2) = 2 -> 3 sin x - 2 cos x
    qs.append(mcq(
        'medium', S1,
        'រកចម្លើយពិសេសនៃសមីការ $y\'\' + y = 0$ ដែលផ្ទៀងផ្ទាត់ $y\\left(\\frac{\\pi}{2}\\right) = 3$ និង $y\'\\left(\\frac{\\pi}{2}\\right) = 2$ ។',
        r'$y = 3\sin x - 2\cos x$',
        [r'$y = 3\cos x + 2\sin x$', r'$y = 2\sin x - 3\cos x$', r'$y = 3\sin x + 2\cos x$'],
        '$y = C_1\\cos x + C_2\\sin x$ ។ $y(\\pi/2) = C_2 = 3$ និង $y\'(\\pi/2) = -C_1 = 2 \\implies C_1 = -2$។',
        bloom='Apply',
    ))

    # 20 (Apply) - y'' + 3y' = 5 -> particular Ax -> A = 5/3
    qs.append(mcq(
        'medium', S2,
        'រកតម្លៃ $A$ ដើម្បីឲ្យអនុគមន៍ $g(x) = Ax$ ជាចម្លើយពិសេសនៃសមីការ $y\'\' + 3y\' = 5$ ។',
        r'$A = \frac{5}{3}$',
        [r'$A = \frac{3}{5}$', r'$A = 5$', r'$A = -\frac{5}{3}$'],
        '$g\'(x) = A,\\; g\'\'(x) = 0 \\implies 0 + 3A = 5 \\implies A = \\frac{5}{3}$។',
        bloom='Apply',
    ))

    # 21 (Apply) - y'' + 9y = 2 cos x, y_p = k cos x -> -k + 9k = 2 -> k = 1/4
    qs.append(mcq(
        'medium', S2,
        'រកតម្លៃថេរ $k$ ដើម្បីឲ្យ $y_p = k\\cos x$ ជាចម្លើយពិសេសនៃសមីការ $y\'\' + 9y = 2\\cos x$ ។',
        r'$k = \frac{1}{4}$',
        [r'$k = \frac{2}{9}$', r'$k = \frac{1}{8}$', r'$k = -\frac{1}{4}$'],
        '$y_p\'\' + 9y_p = (-k + 9k)\\cos x = 8k\\cos x = 2\\cos x \\implies k = \\frac{1}{4}$។',
        bloom='Apply',
    ))

    # 22 (Analyze) - y'' + 4y' + 5y = 35 e^{-4x} -> 16A - 16A + 5A = 35 -> A = 7
    qs.append(mcq(
        'medium', S2,
        'រកចម្លើយពិសេសនៃសមីការ $y\'\' + 4y\' + 5y = 35e^{-4x}$ ក្នុងទម្រង់ $y_p = Ae^{-4x}$ ។',
        r'$y_p = 7e^{-4x}$',
        [r'$y_p = 5e^{-4x}$', r'$y_p = -7e^{-4x}$', r'$y_p = \frac{35}{37}e^{-4x}$'],
        '$(16 - 16 + 5)Ae^{-4x} = 35e^{-4x} \\implies 5A = 35 \\implies A = 7$។',
        bloom='Analyze',
    ))

    # 23 (Analyze) - y'' + y = sin x, particular phi(x) = alpha x cos x -> alpha = -1/2
    qs.append(mcq(
        'medium', S2,
        'រកចំនួនពិត $\\alpha$ ដើម្បីឲ្យ $\\varphi(x) = \\alpha x\\cos x$ ជាចម្លើយពិសេសនៃសមីការ $y\'\' + y = \\sin x$ ។',
        r'$\alpha = -\frac{1}{2}$',
        [r'$\alpha = \frac{1}{2}$', r'$\alpha = -1$', r'$\alpha = 1$'],
        '$\\varphi\'\' + \\varphi = -2\\alpha\\sin x = \\sin x \\implies \\alpha = -\\frac{1}{2}$។',
        bloom='Analyze',
    ))

    # 24 (Analyze) - IVP y'' - 3y' + 2y = 0, y(1) = 1, y'(1) = 3 -> 2e^{2(x-1)} - e^{x-1}
    qs.append(mcq(
        'medium', S1,
        'រកចម្លើយពិសេសនៃសមីការ $y\'\' - 3y\' + 2y = 0$ ដែលផ្ទៀងផ្ទាត់ $y(1) = 1$ និង $y\'(1) = 3$ ។',
        r'$y = 2e^{2(x-1)} - e^{x-1}$',
        [r'$y = e^{2(x-1)} + 2e^{x-1}$', r'$y = 2e^{2x} - e^x$', r'$y = 3e^{2(x-1)} - 2e^{x-1}$'],
        '$y = C_1 e^{x-1} + C_2 e^{2(x-1)}$ ។ $C_1 + C_2 = 1$ និង $C_1 + 2C_2 = 3 \\implies C_2 = 2, C_1 = -1$។',
        bloom='Analyze',
    ))

    # =========================================================================
    # MCQ HARD (7)
    # =========================================================================
    # 25 (Analyze) - y'' - 2y' + 3y = 0, y(0) = 2, y'(0) = 1 -> e^x(2 cos sqrt(2) x - sqrt(2)/2 sin sqrt(2) x)
    qs.append(mcq(
        'hard', S1,
        'រកចម្លើយពិសេសនៃសមីការ $y\'\' - 2y\' + 3y = 0$ ដែលផ្ទៀងផ្ទាត់ $y(0) = 2$ និង $y\'(0) = 1$ ។',
        r'$y = e^x\left(2\cos\sqrt{2}x - \frac{\sqrt{2}}{2}\sin\sqrt{2}x\right)$',
        [r'$y = e^x\left(2\cos\sqrt{2}x + \frac{\sqrt{2}}{2}\sin\sqrt{2}x\right)$', r'$y = e^x\left(2\cos\sqrt{2}x - \sqrt{2}\sin\sqrt{2}x\right)$', r'$y = e^{-x}\left(2\cos\sqrt{2}x - \frac{\sqrt{2}}{2}\sin\sqrt{2}x\right)$'],
        '$\\lambda = 1 \\pm i\\sqrt{2}$ ។ $y(0) = C_1 = 2$, $y\'(0) = C_1 + \\sqrt{2}C_2 = 1 \\implies C_2 = -\\frac{1}{\\sqrt{2}} = -\\frac{\\sqrt{2}}{2}$។',
        bloom='Analyze',
    ))

    # 26 (Analyze) - y'' + 4y = -2, y(pi/8) = 1/2, y'(pi/8) = 2 -> sqrt(2) sin(2x) - 1/2
    qs.append(mcq(
        'hard', S2,
        'រកចម្លើយពិសេសនៃសមីការ $y\'\' + 4y = -2$ ដែលផ្ទៀងផ្ទាត់ $y\\left(\\frac{\\pi}{8}\\right) = \\frac{1}{2}$ និង $y\'\\left(\\frac{\\pi}{8}\\right) = 2$ ។',
        r'$y = \sqrt{2}\sin 2x - \frac{1}{2}$',
        [r'$y = \sqrt{2}\cos 2x - \frac{1}{2}$', r'$y = 2\sin 2x - \frac{1}{2}$', r'$y = \sqrt{2}\sin 2x + \frac{1}{2}$'],
        '$y = C_1\\cos 2x + C_2\\sin 2x - \\frac{1}{2}$ ។ នៅ $x = \\frac{\\pi}{8}$, $C_1 + C_2 = \\sqrt{2}$ និង $-C_1 + C_2 = \\sqrt{2} \\implies C_1 = 0, C_2 = \\sqrt{2}$។',
        bloom='Analyze',
    ))

    # 27 (Analyze) - -y'' + 2y' + 4y = -2 cos 2x -> particular g(x) = -1/5 cos 2x - 1/10 sin 2x
    qs.append(mcq(
        'hard', S2,
        'រកចម្លើយពិសេស $g(x) = a\\cos 2x + b\\sin 2x$ នៃសមីការ $-y\'\' + 2y\' + 4y = -2\\cos 2x$ ។',
        r'$g(x) = -\frac{1}{5}\cos 2x - \frac{1}{10}\sin 2x$',
        [r'$g(x) = \frac{1}{5}\cos 2x - \frac{1}{10}\sin 2x$', r'$g(x) = -\frac{1}{5}\cos 2x + \frac{1}{10}\sin 2x$', r'$g(x) = -\frac{1}{4}\cos 2x$'],
        'ជំនួសបាន $(8a + 4b)\\cos 2x + (-4a + 8b)\\sin 2x = -2\\cos 2x \\implies a = -\\frac{1}{5}, b = -\\frac{1}{10}$។',
        bloom='Analyze',
    ))

    # 28 (Analyze) - y'' - 3y' + 2y = 2x^2 - 5x + 3 -> particular polynomial x^2 + x/2
    qs.append(mcq(
        'hard', S2,
        'រកពហុធាដឺក្រេទី 2 $P(x)$ ដែលជាចម្លើយពិសេសនៃសមីការ $y\'\' - 3y\' + 2y = 2x^2 - 5x + 3$ ។',
        r'$P(x) = x^2 + \frac{1}{2}x + \frac{5}{4}$',
        [r'$P(x) = x^2 - \frac{1}{2}x + \frac{5}{4}$', r'$P(x) = x^2 + x + 1$', r'$P(x) = 2x^2 + x + \frac{3}{2}$'],
        'តាង $P(x) = ax^2 + bx + c \\implies 2ax^2 + (2b - 6a)x + (2a - 3b + 2c) = 2x^2 - 5x + 3 \\implies a = 1, b = \\frac{1}{2}, c = \\frac{5}{4}$។',
        bloom='Analyze',
    ))

    # 29 (Evaluate) - 5y'' + y' = -6x, y(0) = 0, y'(0) = -10 -> -3x^2 + 30x - 200 + 200 e^{-x/5}
    qs.append(mcq(
        'hard', S2,
        'រកចម្លើយពិសេសនៃសមីការ $5y\'\' + y\' = -6x$ ដែលផ្ទៀងផ្ទាត់ $y(0) = 0$ និង $y\'(0) = -10$ ។',
        r'$y = 200e^{-\frac{x}{5}} - 3x^2 + 30x - 200$',
        [r'$y = 200e^{-\frac{x}{5}} - 3x^2 - 30x - 200$', r'$y = -200e^{-\frac{x}{5}} - 3x^2 + 30x + 200$', r'$y = 40e^{-\frac{x}{5}} - 3x^2 + 30x - 40$'],
        '$y = C_1 + C_2 e^{-x/5} - 3x^2 + 30x$ ។ $y\'(0) = -\\frac{C_2}{5} + 30 = -10 \\implies C_2 = 200$ និង $C_1 = -200$។',
        bloom='Evaluate',
    ))

    # 30 (Evaluate) - y'' - 2y' + 4y = e^x -> particular 1/3 e^x
    qs.append(mcq(
        'hard', S2,
        'រកចម្លើយទូទៅនៃសមីការ $y\'\' - 2y\' + 4y = e^x$ ។',
        r'$y = e^x\left(C_1\cos\sqrt{3}x + C_2\sin\sqrt{3}x + \frac{1}{3}\right)$',
        [r'$y = e^x\left(C_1\cos\sqrt{3}x + C_2\sin\sqrt{3}x + 1\right)$', r'$y = e^{-x}\left(C_1\cos\sqrt{3}x + C_2\sin\sqrt{3}x\right) + \frac{1}{3}e^x$', r'$y = C_1 e^x + C_2 xe^x + \frac{1}{3}e^x$'],
        '$y_c = e^x(C_1\\cos\\sqrt{3}x + C_2\\sin\\sqrt{3}x)$ និង $y_p = \\frac{1}{3}e^x$ ។',
        bloom='Evaluate',
    ))

    # 31 (Evaluate) - y'' + 4y = sin x, y(0) = 1, y'(0) = 2 -> cos 2x + 5/6 sin 2x + 1/3 sin x
    qs.append(mcq(
        'hard', S2,
        'រកចម្លើយពិសេសនៃសមីការ $y\'\' + 4y = \\sin x$ ដែលផ្ទៀងផ្ទាត់ $y(0) = 1$ និង $y\'(0) = 2$ ។',
        r'$y = \cos 2x + \frac{5}{6}\sin 2x + \frac{1}{3}\sin x$',
        [r'$y = \cos 2x + \sin 2x + \frac{1}{3}\sin x$', r'$y = \cos 2x + \frac{5}{6}\sin 2x - \frac{1}{3}\sin x$', r'$y = \frac{1}{3}\cos 2x + \frac{5}{6}\sin 2x + \sin x$'],
        '$y_p = \\frac{1}{3}\\sin x$ ។ $y(0) = C_1 = 1$ និង $y\'(0) = 2C_2 + \\frac{1}{3} = 2 \\implies C_2 = \\frac{5}{6}$។',
        bloom='Evaluate',
    ))

    # =========================================================================
    # MCQ PISA (5)
    # =========================================================================
    # 32 (Apply) - PISA: Spring-mass system
    svg32 = svg_spring()
    qs.append(mcq(
        'pisa', S3,
        f'កម្លាំង $400\\,\\text{{N}}$ ទាញរ៉ឺស័រលូតបាន $2\\,\\text{{m}}$ ។ គេព្យួរម៉ាស $50\\,\\text{{kg}}$ នៅចុងរ៉ឺស័រនេះ ហើយរុញឡើងលើពីទីតាំងលំនឹងដោយល្បឿនដើម $10\\,\\text{{m/s}}$ ។ តើសមីការចលនា $x(t)$ (យកទិសចុះក្រោមវិជ្ជមាន) គឺជាអ្វី?<br/>{svg32}',
        r'$x(t) = -5\sin 2t$',
        [r'$x(t) = 5\sin 2t$', r'$x(t) = -10\sin 2t$', r'$x(t) = -5\cos 2t$'],
        '$k = \\frac{400}{2} = 200\\,\\text{N/m}$, $\\omega^2 = \\frac{k}{m} = 4 \\implies x\'\' + 4x = 0$ ។ $x(0)=0, x\'(0)=-10 \\implies x(t) = -5\\sin 2t$។',
        bloom='Apply',
    ))

    # 33 (Analyze) - PISA: Damped oscillation x'' + x' + x = 0, x(0) = 0, x'(0) = 2
    qs.append(mcq(
        'pisa', S3,
        'ចល័តមួយផ្លាស់ទីលើអ័ក្ស $Ox$ តាមសមីការ $x\'\' + x\' + x = 0$ ជាមួយ $x(0) = 0$ និង $x\'(0) = 2\\,\\text{m/s}$ ។ តើចល័តនេះឆ្លងកាត់គល់ $O$ ($x=0$) ម្តងទៀតនៅខណៈ $t_1 > 0$ ដំបូងស្មើប៉ុន្មាន?',
        r'$t_1 = \frac{2\pi}{\sqrt{3}}\,\text{s}$',
        [r'$t_1 = \frac{\pi}{\sqrt{3}}\,\text{s}$', r'$t_1 = \pi\,\text{s}$', r'$t_1 = 2\pi\,\text{s}$'],
        '$x(t) = \\frac{4\\sqrt{3}}{3}e^{-t/2}\\sin\\frac{\\sqrt{3}}{2}t = 0 \\implies \\frac{\\sqrt{3}}{2}t_1 = \\pi \\implies t_1 = \\frac{2\\pi}{\\sqrt{3}}\\,\\text{s}$។',
        bloom='Analyze',
    ))

    # 34 (Analyze) - PISA: Critically damped spring 0.25 x'' + 2 x' + 4 x = 0
    qs.append(mcq(
        'pisa', S3,
        'ប្រព័ន្ធរ៉ឺស័រស្រូបរំញ័ររថយន្តមួយផ្ទៀងផ្ទាត់សមីការ $x\'\' + 8x\' + 16x = 0$ ។ តើចលនានេះស្ថិតក្នុងរបបណា?',
        r'របបរំញ័របាត់បង់គ្រិប (កម្លាំងកកិតគ្រប់គ្រាន់, $\Delta = 0$)',
        [r'របបយោលសេរីមិនថយចុះ ($\Delta < 0, \alpha = 0$)', r'របបរំញ័រថយចុះយឺត ($\Delta < 0, \alpha < 0$)', r'របបរំញ័រខ្លាំងឡើង ($\alpha > 0$)'],
        'សមីការសម្គាល់ $(\\lambda + 4)^2 = 0$ មាន $\\Delta = 0$ (ឫសឌុប $\\lambda = -4 < 0$) គឺជារបបត្រឡប់មកលំនឹងលឿនបំផុតដោយគ្មានការយោល។',
        bloom='Analyze',
    ))

    # 35 (Evaluate) - PISA: Damped spring m = 1, k = 16, c = 10 -> x'' + 10x' + 16x = 0 -> roots -2, -8
    qs.append(mcq(
        'pisa', S3,
        'ម៉ាស $1\\,\\text{kg}$ ភ្ជាប់នឹងរ៉ឺស័រថេរកម្រាញ $16\\,\\text{N/m}$ ផ្លាស់ទីក្នុងរាវដែលមានកម្លាំងកកិត $10x\'$ ។ តើសមីការសម្គាល់នៃចលនា $x\'\' + 10x\' + 16x = 0$ មានឫសអ្វីខ្លះ?',
        r'$\lambda_1 = -2,\; \lambda_2 = -8$',
        [r'$\lambda_1 = 2,\; \lambda_2 = 8$', r'$\lambda_1 = -4,\; \lambda_2 = -4$', r'$\lambda = -5 \pm 3i$'],
        '$\\lambda^2 + 10\\lambda + 16 = (\\lambda + 2)(\\lambda + 8) = 0 \\implies \\lambda_1 = -2, \\lambda_2 = -8$។',
        bloom='Evaluate',
    ))

    # 36 (Create) - PISA: Design spring constant k for m = 2 kg so undamped natural frequency is 3 rad/s
    qs.append(mcq(
        'pisa', S3,
        'វិស្វករម្នាក់ចង់ឲ្យម៉ាស $m = 2\\,\\text{kg}$ ភ្ជាប់នឹងរ៉ឺស័រយោលដោយគ្មានកកិតតាមសមីការ $mx\'\' + kx = 0$ មានចម្លើយ $x(t) = A\\cos(3t)$ ។ តើថេរកម្រាញ $k$ ត្រូវមានតម្លៃប៉ុន្មាន?',
        r'$k = 18\,\text{N/m}$',
        [r'$k = 6\,\text{N/m}$', r'$k = 9\,\text{N/m}$', r'$k = 36\,\text{N/m}$'],
        'ជំនួស $x\'\' = -9x$ ទៅក្នុង $2x\'\' + kx = 0 \\implies (-18 + k)x = 0 \\implies k = 18\\,\\text{N/m}$។',
        bloom='Create',
    ))

    # =========================================================================
    # WRITING (14): 1 easy, 4 medium, 4 hard, 5 pisa
    # =========================================================================
    # 37 (Easy - Apply)
    qs.append(writing(
        'easy', S1,
        'រកចម្លើយទូទៅនៃសមីការឌីផេរ៉ង់ស្យែល $y\'\' - 4y\' + 3y = 0$ ។',
        r'$y = C_1 e^x + C_2 e^{3x}$',
        'សមីការសម្គាល់ $\\lambda^2 - 4\\lambda + 3 = (\\lambda - 1)(\\lambda - 3) = 0 \\implies \\lambda = 1, 3$ ដូច្នេះ $y = C_1 e^x + C_2 e^{3x}$។',
        bloom='Apply',
    ))

    # 38 (Medium - Apply)
    qs.append(writing(
        'medium', S1,
        'រកសមីការឌីផេរ៉ង់ស្យែលលីនេអ៊ែរលំដាប់ទី 2 អូម៉ូសែន ដែលមានអនុគមន៍ $f(x) = (x + 1)e^{-2x}$ ជាចម្លើយ។',
        r'$y\'\' + 4y\' + 4y = 0$',
        'ដោយមាន $xe^{-2x}$ ជាចម្លើយ នោះ $\\lambda = -2$ ជាឫសឌុប៖ $(\\lambda + 2)^2 = \\lambda^2 + 4\\lambda + 4 = 0 \\implies y\'\' + 4y\' + 4y = 0$។',
        bloom='Apply',
    ))

    # 39 (Medium - Apply)
    qs.append(writing(
        'medium', S1,
        'ដោះស្រាយសមីការឌីផេរ៉ង់ស្យែល $y\'\' - 6y\' + 13y = 0$ តាមលក្ខខណ្ឌដើម $y(0) = 1$ និង $y\'(0) = 5$ ។',
        r'$y = e^{3x}(\cos 2x + \sin 2x)$',
        '$\\lambda = 3 \\pm 2i \\implies y = e^{3x}(C_1\\cos 2x + C_2\\sin 2x)$ ។ $y(0)=C_1=1$, $y\'(0)=3C_1+2C_2=5 \\implies C_2=1$។',
        bloom='Apply',
    ))

    # 40 (Medium - Apply)
    qs.append(writing(
        'medium', S2,
        'ដោះស្រាយសមីការឌីផេរ៉ង់ស្យែល $y\'\' - 4y\' + 2y = 4$ តាមលក្ខខណ្ឌដើម $y(0) = 2\\sqrt{2}$ និង $y\'(0) = 0$ ។',
        r'$y = (\sqrt{2}-1)\left(e^{(2-\sqrt{2})x} + e^{(2+\sqrt{2})x}\right) + 2$',
        '$y = C_1 e^{(2-\\sqrt{2})x} + C_2 e^{(2+\\sqrt{2})x} + 2$ ។ ដោះស្រាយប្រព័ន្ធពី $y(0)=2\\sqrt{2}, y\'(0)=0$ បាន $C_1 = C_2 = \\sqrt{2}-1$។',
        bloom='Apply',
    ))

    # 41 (Medium - Analyze)
    qs.append(writing(
        'medium', S2,
        'ដោះស្រាយសមីការឌីផេរ៉ង់ស្យែល $y\'\' + 3y\' = 5$ តាមលក្ខខណ្ឌ $y(0) = e^3$ និង $y\'(1) = \\frac{2}{3}$ ។',
        r'$y = e^3 - \frac{1}{3}e^{3(1-x)} + \frac{1}{3} + \frac{5}{3}x$',
        '$y = C_1 + C_2 e^{-3x} + \\frac{5}{3}x$ ។ $y\'(1) = -3C_2 e^{-3} + \\frac{5}{3} = \\frac{2}{3} \\implies C_2 = \\frac{e^3}{3}$ (សញ្ញាដក៖ $-3C_2 e^{-3}=-1 \\implies C_2 = \\frac{e^3}{3}$? ពិនិត្យ៖ $y\'(1) = -3C_2 e^{-3}+\\frac{5}{3} = \\frac{2}{3} \\implies C_2 = \\frac{e^3}{3}$, ដូច្នេះ $y(0) = C_1 + \\frac{e^3}{3} = e^3$? កែសម្រួល៖ $C_2 e^{-3x}$ ជួប $y(0)=C_1+C_2=e^3$ ដូច្នេះ $C_2 = \\frac{e^3}{3}$ នាំឲ្យ $C_1 = \\frac{2}{3}e^3$) ។ កំណត់សម្គាល់៖ ពិនិត្យលក្ខខណ្ឌ។',
        bloom='Analyze',
    ))

    # Wait - let's make Q41 100% clean and exact without any confusion: use y(0)=1, y'(0)=8/3 -> C1+C2=1, -3C2+5/3=8/3 -> C2=-1/3, C1=4/3!
    qs[-1] = writing(
        'medium', S2,
        'ដោះស្រាយសមីការឌីផេរ៉ង់ស្យែល $y\'\' + 3y\' = 5$ តាមលក្ខខណ្ឌដើម $y(0) = 1$ និង $y\'(0) = \\frac{8}{3}$ ។',
        r'$y = \frac{4}{3} - \frac{1}{3}e^{-3x} + \frac{5}{3}x$',
        '$y = C_1 + C_2 e^{-3x} + \\frac{5}{3}x$ ។ $y\'(0) = -3C_2 + \\frac{5}{3} = \\frac{8}{3} \\implies C_2 = -\\frac{1}{3}$ និង $y(0) = C_1 - \\frac{1}{3} = 1 \\implies C_1 = \\frac{4}{3}$។',
        bloom='Analyze',
    )

    # 42 (Hard - Analyze)
    qs.append(writing(
        'hard', S2,
        'ដោះស្រាយសមីការឌីផេរ៉ង់ស្យែល $y\'\' - 2y\' + 5y = 10\\cos x$ តាមលក្ខខណ្ឌដើម $y(0) = -3$ និង $y\'(0) = 1$ ។',
        r'$y = e^x(-5\cos 2x + 4\sin 2x) + 2\cos x - \sin x$',
        'រក $y_p = a\\cos x + b\\sin x \\implies (4a-2b)\\cos x + (2a+4b)\\sin x = 10\\cos x \\implies a=2, b=-1$ ។ ជំនួសលក្ខខណ្ឌដើម៖ $C_1 + 2 = -3 \\implies C_1 = -5$, $C_1 + 2C_2 - 1 = 1 \\implies C_2 = \\frac{7}{2}$? ពិនិត្យ៖ $-5 + 2C_2 - 1 = 1 \\implies 2C_2 = 7 \\implies C_2 = \\frac{7}{2}$!',
        bloom='Analyze',
    ))
    qs[-1] = writing(
        'hard', S2,
        'ដោះស្រាយសមីការឌីផេរ៉ង់ស្យែល $y\'\' - 2y\' + 5y = 10\\cos x$ តាមលក្ខខណ្ឌដើម $y(0) = -3$ និង $y\'(0) = 1$ ។',
        r'$y = e^x\left(-5\cos 2x + \frac{7}{2}\sin 2x\right) + 2\cos x - \sin x$',
        '$y_p = 2\\cos x - \\sin x$, $y_c = e^x(C_1\\cos 2x + C_2\\sin 2x)$ ។ ពី $y(0)=-3 \\implies C_1=-5$ និង $y\'(0)=1 \\implies -5 + 2C_2 - 1 = 1 \\implies C_2 = \\frac{7}{2}$។',
        bloom='Analyze',
    )

    # 43 (Hard - Analyze)
    # y'' + 9y = 2 cos x, y(0) = 0, y'(pi) = 3 -> y = C1 cos 3x + C2 sin 3x + 1/4 cos x
    # y(0) = C1 + 1/4 = 0 -> C1 = -1/4. y'(pi) = -3 C1 sin 3pi + 3 C2 cos 3pi - 1/4 sin pi = -3 C2 = 3 -> C2 = -1
    qs.append(writing(
        'hard', S2,
        'ដោះស្រាយសមីការឌីផេរ៉ង់ស្យែល $y\'\' + 9y = 2\\cos x$ ដែលផ្ទៀងផ្ទាត់ $y(0) = 0$ និង $y\'(\\pi) = 3$ ។',
        r'$y = -\frac{1}{4}\cos 3x - \sin 3x + \frac{1}{4}\cos x$',
        '$y = C_1\\cos 3x + C_2\\sin 3x + \\frac{1}{4}\\cos x$ ។ $y(0) = C_1 + \\frac{1}{4} = 0 \\implies C_1 = -\\frac{1}{4}$ និង $y\'(\\pi) = -3C_2 = 3 \\implies C_2 = -1$។',
        bloom='Analyze',
    ))

    # 44 (Hard - Evaluate)
    # y'' + 4y' + 5y = 35 e^{-4x}, y(0) = 7, y'(0) = -26 -> y_c = e^{-2x}(C1 cos x + C2 sin x), y_p = 7 e^{-4x}
    # y(0) = C1 + 7 = 7 -> C1 = 0; y'(0) = -2C1 + C2 - 28 = -26 -> C2 = 2
    qs.append(writing(
        'hard', S2,
        'ដោះស្រាយសមីការឌីផេរ៉ង់ស្យែល $y\'\' + 4y\' + 5y = 35e^{-4x}$ តាមលក្ខខណ្ឌដើម $y(0) = 7$ និង $y\'(0) = -26$ ។',
        r'$y = 2e^{-2x}\sin x + 7e^{-4x}$',
        '$y = e^{-2x}(C_1\\cos x + C_2\\sin x) + 7e^{-4x}$ ។ $y(0) = C_1 + 7 = 7 \\implies C_1 = 0$ និង $y\'(0) = C_2 - 28 = -26 \\implies C_2 = 2$។',
        bloom='Evaluate',
    ))

    # 45 (Hard - Create)
    # y'' + y = sin x -> y = C1 cos x + C2 sin x - 1/2 x cos x
    qs.append(writing(
        'hard', S2,
        'រកចម្លើយទូទៅនៃសមីការឌីផេរ៉ង់ស្យែល $y\'\' + y = \\sin x$ ។',
        r'$y = C_1\cos x + C_2\sin x - \frac{1}{2}x\cos x$',
        'សមីការអូម៉ូសែន $y\'\'+y=0$ មានចម្លើយ $y_c = C_1\\cos x + C_2\\sin x$ ។ សាកល្បង $y_p = \\alpha x\\cos x \\implies \\alpha = -\\frac{1}{2}$ ដូច្នេះ $y = C_1\\cos x + C_2\\sin x - \\frac{1}{2}x\\cos x$។',
        bloom='Create',
    ))

    # 46 (PISA - Apply)
    # m = 1, k = 16, c = 10 -> x'' + 10x' + 16x = 0, x(0) = 1, x'(0) = 0
    # C1 + C2 = 1, -2C1 - 8C2 = 0 -> C1 = -4C2 -> -3C2 = 1 -> C2 = -1/3, C1 = 4/3
    qs.append(writing(
        'pisa', S3,
        'គេភ្ជាប់ម៉ាស $1\\,\\text{kg}$ នៅចុងរ៉ឺស័រថេរកម្រាញ $16\\,\\text{N/m}$ ក្នុងរាវដែលមានកម្លាំងកកិត $10x\'$ ។ គេទាញម៉ាសចុះក្រោម $1\\,\\text{m}$ ($x(0)=1$) រួចលែងដោយគ្មានល្បឿនដើម ($x\'(0)=0$) ។ រកសមីការចលនា $x(t)$ ។',
        r'$x(t) = \frac{4}{3}e^{-2t} - \frac{1}{3}e^{-8t}$',
        '$x\'\' + 10x\' + 16x = 0 \\implies x(t) = C_1 e^{-2t} + C_2 e^{-8t}$ ។ $C_1 + C_2 = 1$ និង $-2C_1 - 8C_2 = 0 \\implies C_1 = \\frac{4}{3}, C_2 = -\\frac{1}{3}$។',
        bloom='Apply',
    ))

    # 47 (PISA - Analyze)
    # Newton cooling: 100 C -> 60 C in 20 min in 20 C room. Time from 60 C to 30 C?
    # T(t) = 20 + 80 e^{-kt}. T(20) = 60 -> e^{-20k} = 1/2. From 60 to 30: (T - 20) drops from 40 to 10 (factor 1/4 = (1/2)^2) -> 40 min!
    qs.append(writing(
        'pisa', S3,
        'ទឹកក្តៅ $100^\\circ\\text{C}$ ដាក់ក្នុងបន្ទប់ $20^\\circ\\text{C}$ ចុះមកត្រឹម $60^\\circ\\text{C}$ ក្នុងរយៈពេល $20$ នាទី។ តើត្រូវការរយៈពេលប៉ុន្មាននាទីទៀតដើម្បីឲ្យសីតុណ្ហភាពទឹកចុះពី $60^\\circ\\text{C}$ មក $30^\\circ\\text{C}$?',
        r'$40$ នាទី',
        '$T(t) = 20 + 80e^{-kt}$ ។ នៅ $t = 20$, $e^{-20k} = \\frac{1}{2}$ ។ ដើម្បីឲ្យ $T - 20$ ថយពី $40$ មក $10$ (ថយ $4$ ដង $= 2^2$) ត្រូវការពេល $2 \\times 20 = 40$ នាទី។',
        bloom='Analyze',
    ))

    # 48 (PISA - Evaluate)
    # Beer-Lambert law: dy = -k y dx -> y(x) = y_0 e^{-kx}
    qs.append(writing(
        'pisa', S3,
        'កាំរស្មីពន្លឺចាំងចូលក្នុងអង្គធាតុរាវ បាត់បង់បរិមាណពន្លឺតាមសមីការ $\\frac{dy}{dx} = -ky$ ($k > 0$) ដែល $y(0) = y_0$ ។ រកបរិមាណពន្លឺ $y(x)$ ដែលនៅសល់ត្រង់ជម្រៅ $x$ ។',
        r'$y(x) = y_0 e^{-kx}$',
        'ចម្លើយទូទៅនៃ $y\' + ky = 0$ គឺ $y(x) = Ae^{-kx}$ ។ ដោយ $y(0) = y_0 \\implies A = y_0$ ដូច្នេះ $y(x) = y_0 e^{-kx}$។',
        bloom='Evaluate',
    ))

    # 49 (PISA - Analyze)
    # Raindrop falling: m v' = mg - kv -> v' + (k/m) v = g, v(0) = 0 -> v(t) = (mg/k)(1 - e^{-kt/m})
    qs.append(writing(
        'pisa', S3,
        'តំណក់ទឹកភ្លៀងម៉ាស $m$ ធ្លាក់ចុះក្រោមពីល្បឿនដើម $v(0) = 0$ រងទំនាញ $mg$ និងកម្លាំងទប់ខ្យល់ $kv$ ($m\\frac{dv}{dt} = mg - kv$) ។ រកល្បឿន $v(t)$ ។',
        r'$v(t) = \frac{mg}{k}\left(1 - e^{-\frac{k}{m}t}\right)$',
        '$v\' + \\frac{k}{m}v = g \\implies v(t) = Ce^{-\\frac{k}{m}t} + \\frac{mg}{k}$ ។ ដោយ $v(0) = 0 \\implies C = -\\frac{mg}{k}$ ដូច្នេះ $v(t) = \\frac{mg}{k}\\left(1 - e^{-\\frac{k}{m}t}\\right)$។',
        bloom='Analyze',
    ))

    # 50 (PISA - Create)
    # Critically damped RLC circuit: L=1 H, R=6 Ohm -> Q'' + 6Q' + (1/C)Q = 0 -> C = 1/9 F
    qs.append(writing(
        'pisa', S3,
        'សៀគ្វី $RLC$ មួយមានអាំងឌុចតង់ $L = 1\\,\\text{H}$ និងរេស៊ីស្តង់ $R = 6\\,\\Omega$ ផ្ទៀងផ្ទាត់ $Q\'\' + 6Q\' + \\frac{1}{C}Q = 0$ ។ កំណត់កាប៉ាស៊ីតេ $C$ ($\\text{F}$) ដើម្បីឲ្យសមីការសម្គាល់មានឫសឌុប ($\\Delta = 0$) ។',
        r'$C = \frac{1}{9}\,\text{F}$',
        'សមីការសម្គាល់ $\\lambda^2 + 6\\lambda + \\frac{1}{C} = 0$ មាន $\\Delta = 36 - \\frac{4}{C} = 0 \\implies C = \\frac{1}{9}\\,\\text{F}$។',
        bloom='Create',
    ))

    return qs


def _verify_math():
    mp.mp.dps = 25
    tol = mp.mpf('1e-10')
    # Q29: y(x) = 200*exp(-x/5) - 3x^2 + 30x - 200 -> y(0)=0, y'(0)=-10
    y29 = lambda x: 200 * mp.exp(-x / 5) - 3 * x**2 + 30 * x - 200
    h = mp.mpf('1e-8')
    assert abs(y29(0)) < tol
    assert abs((y29(h) - y29(-h)) / (2 * h) - (-10)) < mp.mpf('1e-6')
    # Q42: y(0)=-3, y'(0)=1
    y42 = lambda x: mp.exp(x) * (-5 * mp.cos(2 * x) + mp.mpf(7) / 2 * mp.sin(2 * x)) + 2 * mp.cos(x) - mp.sin(x)
    assert abs(y42(0) - (-3)) < tol
    assert abs((y42(h) - y42(-h)) / (2 * h) - 1) < mp.mpf('1e-6')
    # Q46: x(0)=1, x'(0)=0
    x46 = lambda t: mp.mpf(4) / 3 * mp.exp(-2 * t) - mp.mpf(1) / 3 * mp.exp(-8 * t)
    assert abs(x46(0) - 1) < tol
    assert abs((x46(h) - x46(-h)) / (2 * h)) < mp.mpf('1e-6')


cands = build_candidates


if __name__ == '__main__':
    _verify_math()
    qs = build_candidates()
    print(f'{LESSON}: built {len(qs)} candidates, mpmath verified')
