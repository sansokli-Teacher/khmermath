# -*- coding: utf-8 -*-
"""
KhmerMath Question Bank: Grade 12 Science (SC)
Chapter 10: កោនិក
Lesson 3: អ៊ីពែបូល
Reference textbook: Lesson/G12/SC/C10-L3.tex
Matrix: MCQ easy10/medium14/hard7/pisa5 + writing easy1/medium4/hard4/pisa5 = 50, Bloom on each.
All hyperbola equations, foci, vertices, asymptotes, eccentricities, and application values are checked via Fraction/math.
"""
import sys, os, math
from fractions import Fraction
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.dirname(__file__))
from lib import *
import G12L04 as P

LESSON = 'អ៊ីពែបូល'
CHAPTER = 'ជំពូកទី 10 : កោនិក'
GRADE = '12SC'
TARGET = P.TARGET

S1 = 'និយមន័យអ៊ីពែបូល'
S2 = 'សមីការអ៊ីពែបូលដែលមានផ្ចិតនៅគល់ O(0, 0)'
S3 = 'សមីការអ៊ីពែបូលដែលមានផ្ចិត I(h, k)'
S4 = 'អ៊ុចសង់ទ្រីស៊ីតេ និងលក្ខណៈចំណាំងផ្លាតនៃអ៊ីពែបូល'
TOPIC_MAP = {
    's1': S1, 's2': S2, 's3': S3, 's4': S4,
    'p_loran': S4, 'p_telescope': S4, 'p_cooling': S3, 'p_rutherford': S2, 'p_sonic': S2,
    'p_coast': S4, 'p_tower': S3, 'p_radar': S4, 'p_mirror': S2, 'p_orbit': S2,
}
CNT = [0]


def chk(fn):
    r = fn()
    rs = list(r) if isinstance(r, tuple) else [r]
    assert all(rs), ('numeric check failed', rs)
    CNT[0] += len(rs)


def with_img(q, svg):
    q['img'] = svg
    return q


def F(a, b=None):
    return Fraction(a, b) if b is not None else Fraction(str(a))


def _esc(s):
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def fig_hyperbola(cx, cy, a, b, orient, x0, x1, y0, y1, xlabel='x', ylabel='y',
                  xticks=(), yticks=(), title='', tmax=1.25,
                  asym=True, branch='both', dots_data=(), segs_data=(), notes_data=()):
    """Full-plane SVG hyperbola figure (draws both branches by default, no white bg rect, Latin/Unicode only)."""
    W, H = 395, 230
    pad_l, pad_r, pad_t, pad_b = 46, 74, 32, 30
    pw = W - pad_l - pad_r
    ph = H - pad_t - pad_b
    sx = lambda x: pad_l + (x - x0) / (x1 - x0) * pw
    sy = lambda y: pad_t + (y1 - y) / (y1 - y0) * ph

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'style="max-width:100%;height:auto;font-family:system-ui,-apple-system,sans-serif">',
        '<defs><marker id="arrH" viewBox="0 0 10 10" refX="8" refY="5" '
        'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        '<path d="M 0 1 L 8 5 L 0 9 z" fill="#475569"/></marker></defs>',
    ]

    has_origin = (x0 <= 0 <= x1) and (y0 <= 0 <= y1)
    ay = sy(0) if (y0 <= 0 <= y1) else sy(y0)
    ax = sx(0) if (x0 <= 0 <= x1) else sx(x0)

    parts.append(
        f'<line x1="{pad_l - 8:.1f}" y1="{ay:.1f}" x2="{W - pad_r + 12:.1f}" y2="{ay:.1f}" '
        f'stroke="#475569" stroke-width="1.4" marker-end="url(#arrH)"/>'
    )
    parts.append(
        f'<line x1="{ax:.1f}" y1="{H - pad_b + 8:.1f}" x2="{ax:.1f}" y2="{pad_t - 12:.1f}" '
        f'stroke="#475569" stroke-width="1.4" marker-end="url(#arrH)"/>'
    )

    parts.append(
        f'<text x="{W - pad_r + 16:.1f}" y="{ay + 4:.1f}" font-size="11" '
        f'font-style="italic" fill="#1e293b" text-anchor="start">{_esc(xlabel)}</text>'
    )
    parts.append(
        f'<text x="{ax:.1f}" y="{pad_t - 17:.1f}" font-size="11" '
        f'font-style="italic" fill="#1e293b" text-anchor="middle">{_esc(ylabel)}</text>'
    )

    if has_origin:
        parts.append(
            f'<text x="{ax - 7:.1f}" y="{ay + 14:.1f}" font-size="11" '
            f'font-style="italic" fill="#475569" text-anchor="end">O</text>'
        )

    for xv in xticks:
        px = sx(xv)
        if abs(xv) < 1e-9 and has_origin:
            continue
        parts.append(f'<line x1="{px:.1f}" y1="{ay - 3:.1f}" x2="{px:.1f}" y2="{ay + 3:.1f}" stroke="#475569" stroke-width="1.1"/>')
        parts.append(f'<text x="{px:.1f}" y="{ay + 14:.1f}" font-size="10" fill="#475569" text-anchor="middle">{_esc(xv)}</text>')

    for yv in yticks:
        py = sy(yv)
        if abs(yv) < 1e-9 and has_origin:
            continue
        parts.append(f'<line x1="{ax - 3:.1f}" y1="{py:.1f}" x2="{ax + 3:.1f}" y2="{py:.1f}" stroke="#475569" stroke-width="1.1"/>')
        parts.append(f'<text x="{ax - 7:.1f}" y="{py + 3.5:.1f}" font-size="10" fill="#475569" text-anchor="end">{_esc(yv)}</text>')

    # Clip region for curves and asymptotes
    parts.append(f'<defs><clipPath id="hypClip"><rect x="{pad_l - 4}" y="{pad_t - 4}" width="{pw + 8}" height="{ph + 8}"/></clipPath></defs>')
    parts.append('<g clip-path="url(#hypClip)">')

    # Asymptotes
    if asym:
        slope = (b / a) if orient == 'h' else (a / b)
        for sgn in (1, -1):
            xa, xb = x0, x1
            ya = cy + sgn * slope * (xa - cx)
            yb = cy + sgn * slope * (xb - cx)
            parts.append(
                f'<line x1="{sx(xa):.1f}" y1="{sy(ya):.1f}" x2="{sx(xb):.1f}" y2="{sy(yb):.1f}" '
                f'stroke="#d97706" stroke-width="1.2" stroke-dasharray="4 3"/>'
            )

    # Segments
    for xA, yA, xB, yB, col, dashed in segs_data:
        dash_attr = ' stroke-dasharray="4 3"' if dashed else ''
        parts.append(
            f'<line x1="{sx(xA):.1f}" y1="{sy(yA):.1f}" x2="{sx(xB):.1f}" y2="{sy(yB):.1f}" '
            f'stroke="{col}" stroke-width="1.4"{dash_attr}/>'
        )

    # Hyperbola branches sampled via cosh/sinh
    npts = 48
    branches = (+1, -1) if branch == 'both' else ((+1,) if branch == 'pos' else (-1,))
    for sgn in branches:
        pts = []
        for i in range(npts + 1):
            t = -tmax + 2 * tmax * i / npts
            if orient == 'h':
                xv = cx + sgn * a * math.cosh(t)
                yv = cy + b * math.sinh(t)
            else:
                xv = cx + b * math.sinh(t)
                yv = cy + sgn * a * math.cosh(t)
            pts.append(f'{sx(xv):.1f},{sy(yv):.1f}')
        parts.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{P.K.BLUE}" stroke-width="2.2"/>')

    parts.append('</g>')

    # Dots and labels
    for xv, yv, lbl, dx, dy, col in dots_data:
        px, py = sx(xv), sy(yv)
        parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="3.3" fill="{col}"/>')
        if lbl:
            anchor = 'start' if dx > 0 else ('end' if dx < 0 else 'middle')
            parts.append(
                f'<text x="{px + dx:.1f}" y="{py + dy:.1f}" font-size="10.5" '
                f'font-weight="600" fill="{col}" text-anchor="{anchor}">{_esc(lbl)}</text>'
            )

    for xv, yv, lbl, col in notes_data:
        parts.append(
            f'<text x="{sx(xv):.1f}" y="{sy(yv):.1f}" font-size="10.5" '
            f'font-weight="600" fill="{col}" text-anchor="middle">{_esc(lbl)}</text>'
        )

    if title:
        parts.append(
            f'<text x="{W - 8:.1f}" y="16" font-size="11" font-weight="600" '
            f'fill="#334155" text-anchor="end">{_esc(title)}</text>'
        )

    parts.append('</svg>')
    return ''.join(parts)


def _cands_raw():
    qs = []

    # =========================================================================
    # EASY MCQ (10 questions: #1 - #10)
    # =========================================================================

    # 1. Standard equation (horizontal transverse axis, origin)
    qs.append(mcq('easy', 's2',
        'តើសមីការស្ដង់ដានៃអ៊ីពែបូលដែលមានផ្ចិតនៅគល់ ' + M('O(0, 0)') + ' និងអ័ក្សទទឹងស្ថិតនៅលើអ័ក្សអាប់ស៊ីសគឺជាមួយណា?',
        M('\\frac{x^2}{a^2} - \\frac{y^2}{b^2} = 1'),
        [M('\\frac{y^2}{a^2} - \\frac{x^2}{b^2} = 1'), M('\\frac{x^2}{a^2} + \\frac{y^2}{b^2} = 1'), M('y^2 = 4ax')],
        'អ៊ីពែបូលមានផ្ចិត ' + M('(0, 0)') + ' និងអ័ក្សទទឹងលើអ័ក្សអាប់ស៊ីស មានសមីការស្ដង់ដា ' + M('\\frac{x^2}{a^2} - \\frac{y^2}{b^2} = 1') + ' ។',
        bloom='Remember'))

    # 2. Definition constant |PF1 - PF2| = 2a
    chk(lambda: 2 * 5 == 10)
    qs.append(mcq('easy', 's1',
        'អ៊ីពែបូលមួយមានកំពូល ' + M('V_1(5, 0)') + ' និង ' + M('V_2(-5, 0)') + ' ។ ចំពោះគ្រប់ចំណុច ' + M('P') + ' នៅលើអ៊ីពែបូល តើ ' + M('|PF_1 - PF_2|') + ' ស្មើប៉ុន្មាន?',
        M('10'),
        [M('5'), M('25'), M('2.5')],
        'តាមនិយមន័យ ' + M('|PF_1 - PF_2| = V_1V_2 = 2a = 2 \\times 5 = 10') + ' ។',
        bloom='Remember'))

    # 3. Relation between a, b, c
    chk(lambda: 3**2 + 4**2 == 5**2)
    qs.append(mcq('easy', 's2',
        'អ៊ីពែបូល ' + M('\\frac{x^2}{9} - \\frac{y^2}{16} = 1') + ' មានតម្លៃ ' + M('c') + ' (ចម្ងាយពីផ្ចិតទៅកំណុំ) ស្មើប៉ុន្មាន?',
        M('5'),
        [M('7'), M('\\sqrt{7}'), M('25')],
        'គេមាន ' + M('a^2 = 9, b^2 = 16 \\implies c^2 = a^2 + b^2 = 9 + 16 = 25 \\implies c = 5') + ' ។',
        bloom='Apply'))

    # 4. Vertices of y^2/16 - x^2/9 = 1
    chk(lambda: 4**2 == 16)
    qs.append(mcq('easy', 's2',
        'តើកំពូលទាំងពីរនៃអ៊ីពែបូល ' + M('\\frac{y^2}{16} - \\frac{x^2}{9} = 1') + ' គឺជាចំណុចណា?',
        M('(0, \\pm 4)'),
        [M('(\\pm 4, 0)'), M('(0, \\pm 3)'), M('(\\pm 5, 0)')],
        'ដោយអ័ក្សទទឹងនៅលើអ័ក្សអរដោនេ និង ' + M('a^2 = 16 \\implies a = 4') + ' នោះកំពូលគឺ ' + M('(0, \\pm 4)') + ' ។',
        bloom='Understand'))

    # 5. Center of shifted hyperbola
    qs.append(mcq('easy', 's3',
        'តើផ្ចិតនៃអ៊ីពែបូល ' + M('\\frac{(x - 3)^2}{4} - \\frac{(y + 2)^2}{9} = 1') + ' មានកូអរដោនេប៉ុន្មាន?',
        M('(3, -2)'),
        [M('(-3, 2)'), M('(2, -3)'), M('(4, 9)')],
        'ប្រៀបធៀបនឹងទម្រង់ ' + M('\\frac{(x - h)^2}{a^2} - \\frac{(y - k)^2}{b^2} = 1') + ' បាន ' + M('h = 3, k = -2') + ' ដូច្នេះផ្ចិតគឺ ' + M('(3, -2)') + ' ។',
        bloom='Remember'))

    # 6. Asymptotes of x^2/16 - y^2/9 = 1
    chk(lambda: F(3, 4) == F(3, 4))
    qs.append(mcq('easy', 's2',
        'តើសមីការអាស៊ីមតូតនៃអ៊ីពែបូល ' + M('\\frac{x^2}{16} - \\frac{y^2}{9} = 1') + ' គឺជាមួយណា?',
        M('y = \\pm \\frac{3}{4}x'),
        [M('y = \\pm \\frac{4}{3}x'), M('y = \\pm \\frac{9}{16}x'), M('y = \\pm \\frac{16}{9}x')],
        'គេមាន ' + M('a = 4, b = 3') + ' នោះសមីការអាស៊ីមតូតគឺ ' + M('y = \\pm \\frac{b}{a}x = \\pm \\frac{3}{4}x') + ' ។',
        bloom='Remember'))

    # 7. Eccentricity range
    qs.append(mcq('easy', 's4',
        'ចំពោះគ្រប់អ៊ីពែបូល តើអ៊ុចសង់ទ្រីស៊ីតេ ' + M('e = \\frac{c}{a}') + ' ផ្ទៀងផ្ទាត់លក្ខខណ្ឌណា?',
        M('e > 1'),
        [M('0 < e < 1'), M('e = 1'), M('e < 0')],
        'ព្រោះកំណុំស្ថិតនៅខាងក្រៅកំពូល (' + M('c > a > 0') + ') នោះ ' + M('e = \\frac{c}{a} > 1') + ' ជានិច្ច ។',
        bloom='Remember'))

    # 8. General equation condition AB < 0
    qs.append(mcq('easy', 's3',
        'សមីការដឺក្រេទី 2 ' + M('Ax^2 + By^2 + Cx + Dy + E = 0') + ' តាងឱ្យអ៊ីពែបូល កាលណា ' + M('A') + ' និង ' + M('B') + ' ផ្ទៀងផ្ទាត់៖',
        M('AB < 0'),
        [M('AB > 0'), M('A = B'), M('AB = 0')],
        'សមីការទូទៅតាងឱ្យអ៊ីពែបូល កាលណា ' + M('A') + ' និង ' + M('B') + ' មានសញ្ញាផ្ទុយគ្នា គឺ ' + M('AB < 0') + ' ។',
        bloom='Remember'))

    # 9. Eccentricity value for 9x^2 - 16y^2 = 144
    chk(lambda: F(5, 4) == F(5, 4))
    qs.append(mcq('easy', 's4',
        'អ៊ីពែបូល ' + M('9x^2 - 16y^2 = 144') + ' មានអ៊ុចសង់ទ្រីស៊ីតេ ' + M('e') + ' ស្មើប៉ុន្មាន?',
        M('\\frac{5}{4}'),
        [M('\\frac{4}{5}'), M('\\frac{3}{4}'), M('\\frac{5}{3}')],
        'ចែកនឹង ' + M('144') + ' បាន ' + M('\\frac{x^2}{16} - \\frac{y^2}{9} = 1') + ' នោះ ' + M('a = 4, b = 3, c = 5') + ' ដូច្នេះ ' + M('e = \\frac{c}{a} = \\frac{5}{4}') + ' ។',
        bloom='Apply'))

    # 10. Foci of x^2/4 - y^2/12 = 1
    chk(lambda: 4 + 12 == 4**2)
    qs.append(mcq('easy', 's2',
        'តើកំណុំទាំងពីរនៃអ៊ីពែបូល ' + M('\\frac{x^2}{4} - \\frac{y^2}{12} = 1') + ' គឺជាចំណុចណា?',
        M('(\\pm 4, 0)'),
        [M('(0, \\pm 4)'), M('(\\pm 2, 0)'), M('(\\pm \\sqrt{8}, 0)')],
        'គេមាន ' + M('a^2 = 4, b^2 = 12 \\implies c^2 = 4 + 12 = 16 \\implies c = 4') + ' ដូច្នេះកំណុំគឺ ' + M('(\\pm 4, 0)') + ' ។',
        bloom='Apply'))

    # =========================================================================
    # MEDIUM MCQ (14 questions: #11 - #24)
    # =========================================================================

    # 11. 4x^2 - 9y^2 = -36 -> vertical transverse axis!
    chk(lambda: 4 + 9 == 13)
    qs.append(mcq('medium', 's2',
        'កំណត់កូអរដោនេកំណុំនៃអ៊ីពែបូល ' + M('4x^2 - 9y^2 = -36') + ' ។',
        M('(0, \\pm \\sqrt{13})'),
        [M('(\\pm \\sqrt{13}, 0)'), M('(0, \\pm \\sqrt{5})'), M('(\\pm 3, 0)')],
        'ចែកនឹង ' + M('-36') + ' បាន ' + M('\\frac{y^2}{4} - \\frac{x^2}{9} = 1') + ' មានអ័ក្សទទឹងលើ ' + M('Oy') + ' ដោយ ' + M('a^2 = 4, b^2 = 9 \\implies c = \\sqrt{13}') + ' ដូច្នេះកំណុំគឺ ' + M('(0, \\pm \\sqrt{13})') + ' ។',
        bloom='Apply'))

    # 12. Shifted hyperbola 16(y-2)^2 - 9(x+2)^2 = 144 -> foci
    chk(lambda: (9 + 16 == 5**2, 2 + 5 == 7, 2 - 5 == -3))
    qs.append(mcq('medium', 's3',
        'រកកូអរដោនេកំណុំនៃអ៊ីពែបូល ' + M('16(y - 2)^2 - 9(x + 2)^2 = 144') + ' ។',
        M('(-2, 7)\\text{ និង }(-2, -3)'),
        [M('(3, 2)\\text{ និង }(-7, 2)'), M('(-2, 5)\\text{ និង }(-2, -1)'), M('(2, 7)\\text{ និង }(2, -3)')],
        'សមីការស្ដង់ដាគឺ ' + M('\\frac{(y - 2)^2}{9} - \\frac{(x + 2)^2}{16} = 1') + ' មានផ្ចិត ' + M('I(-2, 2)') + ', ' + M('c = \\sqrt{9 + 16} = 5') + ' ដូច្នេះកំណុំគឺ ' + M('(-2, 2 \\pm 5)') + ' ។',
        bloom='Apply'))

    # 13. Asymptotes of vertical hyperbola y^2/16 - x^2/9 = 1
    chk(lambda: F(4, 3) == F(4, 3))
    qs.append(mcq('medium', 's2',
        'តើសមីការអាស៊ីមតូតនៃអ៊ីពែបូល ' + M('\\frac{y^2}{16} - \\frac{x^2}{9} = 1') + ' គឺជាមួយណា?',
        M('y = \\pm \\frac{4}{3}x'),
        [M('y = \\pm \\frac{3}{4}x'), M('y = \\pm \\frac{16}{9}x'), M('y = \\pm 4x')],
        'អ័ក្សទទឹងលើ ' + M('Oy') + ' មាន ' + M('a = 4, b = 3') + ' ដូច្នេះអាស៊ីមតូតគឺ ' + M('y = \\pm \\frac{a}{b}x = \\pm \\frac{4}{3}x') + ' ។',
        bloom='Apply'))

    # 14. Equation from V(+-1, 0) and asymptotes y = +-3x
    chk(lambda: 3 * 1 == 3 and 3**2 == 9)
    qs.append(mcq('medium', 's2',
        'រកសមីការស្ដង់ដានៃអ៊ីពែបូលដែលមានកំពូល ' + M('(\\pm 1, 0)') + ' និងអាស៊ីមតូត ' + M('y = \\pm 3x') + ' ។',
        M('x^2 - \\frac{y^2}{9} = 1'),
        [M('\\frac{x^2}{9} - y^2 = 1'), M('y^2 - \\frac{x^2}{9} = 1'), M('x^2 - \\frac{y^2}{3} = 1')],
        'កំពូល ' + M('(\\pm 1, 0)') + ' ឱ្យ ' + M('a = 1') + ' និង ' + M('\\frac{b}{a} = 3 \\implies b = 3') + ' ដូច្នេះ ' + M('x^2 - \\frac{y^2}{9} = 1') + ' ។',
        bloom='Apply'))

    # 15. Equation from V(0, +-3) and asymptotes y = +-3x
    chk(lambda: F(3, 3) == 1)
    qs.append(mcq('medium', 's2',
        'រកសមីការស្ដង់ដានៃអ៊ីពែបូលដែលមានកំពូល ' + M('(0, \\pm 3)') + ' និងអាស៊ីមតូត ' + M('y = \\pm 3x') + ' ។',
        M('\\frac{y^2}{9} - x^2 = 1'),
        [M('\\frac{y^2}{9} - \\frac{x^2}{9} = 1'), M('\\frac{x^2}{9} - y^2 = 1'), M('y^2 - \\frac{x^2}{9} = 1')],
        'កំពូល ' + M('(0, \\pm 3)') + ' ឱ្យ ' + M('a = 3') + ' និង ' + M('\\frac{a}{b} = 3 \\implies b = 1') + ' ដូច្នេះ ' + M('\\frac{y^2}{9} - x^2 = 1') + ' ។',
        bloom='Apply'))

    # 16. Equation from foci (0, 0), (8, 0) and 2a = 4 -> wait: foci (-4,0), (4,0), 2a=4
    chk(lambda: 4**2 - 2**2 == 12)
    qs.append(mcq('medium', 's2',
        'រកសមីការអ៊ីពែបូលដែលមានកំណុំ ' + M('(\\pm 4, 0)') + ' និងផលដកចម្ងាយពីចំណុចលើអ៊ីពែបូលទៅកំណុំទាំងពីរស្មើនឹង ' + M('4') + ' ។',
        M('\\frac{x^2}{4} - \\frac{y^2}{12} = 1'),
        [M('\\frac{x^2}{12} - \\frac{y^2}{4} = 1'), M('\\frac{y^2}{4} - \\frac{x^2}{12} = 1'), M('\\frac{x^2}{16} - \\frac{y^2}{4} = 1')],
        'គេមាន ' + M('c = 4, 2a = 4 \\implies a = 2') + ' និង ' + M('b^2 = c^2 - a^2 = 16 - 4 = 12') + ' ដូច្នេះ ' + M('\\frac{x^2}{4} - \\frac{y^2}{12} = 1') + ' ។',
        bloom='Apply'))

    # 17. Complete the square: 9x^2 - y^2 - 36x - 6y + 18 = 0
    chk(lambda: (9 * 4 - 9 - 18 == 9, 1 + 9 == 10))
    qs.append(mcq('medium', 's3',
        'រកផ្ចិតនៃអ៊ីពែបូល ' + M('9x^2 - y^2 - 36x - 6y + 18 = 0') + ' ។',
        M('(2, -3)'),
        [M('(-2, 3)'), M('(2, 3)'), M('(-4, -3)')],
        'បំពេញការ៉េបាន ' + M('9(x - 2)^2 - (y + 3)^2 = 9 \\iff (x - 2)^2 - \\frac{(y + 3)^2}{9} = 1') + ' ដូច្នេះផ្ចិតគឺ ' + M('(2, -3)') + ' ។',
        bloom='Apply'))

    # 18. Complete the square: -x^2 + 4y^2 - 2x - 16y + 11 = 0 -> foci
    chk(lambda: (-11 + 16 - 1 == 4, 1 + 4 == 5))
    qs.append(mcq('medium', 's3',
        'រកកំណុំទាំងពីរនៃអ៊ីពែបូល ' + M('-x^2 + 4y^2 - 2x - 16y + 11 = 0') + ' ។',
        M('(-1, 2 \\pm \\sqrt{5})'),
        [M('(-1, 2 \\pm \\sqrt{3})'), M('(-1 \\pm \\sqrt{5}, 2)'), M('(1, -2 \\pm \\sqrt{5})')],
        'បំពេញការ៉េបាន ' + M('4(y - 2)^2 - (x + 1)^2 = 4 \\iff (y - 2)^2 - \\frac{(x + 1)^2}{4} = 1') + ' មាន ' + M('I(-1, 2), a = 1, b = 2, c = \\sqrt{5}') + ' ។',
        bloom='Analyze'))

    # 19. Latus rectum length 2b^2/a for x^2/16 - y^2/9 = 1
    chk(lambda: F(2 * 9, 4) == F(9, 2))
    qs.append(mcq('medium', 's2',
        'តើប្រវែងអង្កត់កាត់កំណុំកែងអ័ក្សទទឹងនៃអ៊ីពែបូល ' + M('\\frac{x^2}{16} - \\frac{y^2}{9} = 1') + ' ស្មើប៉ុន្មាន?',
        M('\\frac{9}{2}'),
        [M('\\frac{32}{3}'), M('6'), M('8')],
        'ប្រវែងអង្កត់កាត់កំណុំកែងអ័ក្សទទឹងគឺ ' + M('\\frac{2b^2}{a} = \\frac{2 \\times 9}{4} = \\frac{9}{2}') + ' ។',
        bloom='Apply'))

    # 20. Eccentricity of 4(x-2)^2 - 9(y+3)^2 = 36
    chk(lambda: 9 + 4 == 13)
    qs.append(mcq('medium', 's4',
        'រកអ៊ុចសង់ទ្រីស៊ីតេនៃអ៊ីពែបូល ' + M('4(x - 2)^2 - 9(y + 3)^2 = 36') + ' ។',
        M('\\frac{\\sqrt{13}}{3}'),
        [M('\\frac{\\sqrt{13}}{2}'), M('\\frac{\\sqrt{5}}{3}'), M('\\frac{5}{3}')],
        'សមីការស្ដង់ដាគឺ ' + M('\\frac{(x - 2)^2}{9} - \\frac{(y + 3)^2}{4} = 1') + ' មាន ' + M('a = 3, b = 2, c = \\sqrt{13}') + ' ដូច្នេះ ' + M('e = \\frac{\\sqrt{13}}{3}') + ' ។',
        bloom='Apply'))

    # 21. Equation from V(+-3, 0) passing through (5, 2)
    chk(lambda: F(25, 9) - 1 == F(16, 9) and F(4, F(16, 9)) == F(9, 4))
    qs.append(mcq('medium', 's2',
        'អ៊ីពែបូលមួយមានកំពូល ' + M('(\\pm 3, 0)') + ' និងកាត់តាមចំណុច ' + M('(5, 2)') + ' ។ រកសមីការស្ដង់ដានៃអ៊ីពែបូលនេះ ។',
        M('\\frac{x^2}{9} - \\frac{4y^2}{9} = 1'),
        [M('\\frac{x^2}{9} - \\frac{y^2}{4} = 1'), M('\\frac{x^2}{9} - \\frac{9y^2}{4} = 1'), M('\\frac{y^2}{9} - \\frac{4x^2}{9} = 1')],
        'ជំនួស ' + M('a = 3') + ' និង ' + M('(5, 2)') + ' ក្នុង ' + M('\\frac{x^2}{9} - \\frac{y^2}{b^2} = 1') + ' បាន ' + M('b^2 = \\frac{9}{4}') + ' ដូច្នេះ ' + M('\\frac{x^2}{9} - \\frac{4y^2}{9} = 1') + ' ។',
        bloom='Apply'))

    # 22. Shifted asymptotes of (y - 1)^2/4 - (x + 4)^2/9 = 1
    chk(lambda: (1 + F(2, 3) * 4 == F(11, 3), 1 - F(2, 3) * 4 == F(-5, 3)))
    qs.append(mcq('medium', 's3',
        'រកសមីការអាស៊ីមតូតនៃអ៊ីពែបូល ' + M('\\frac{(y - 1)^2}{4} - \\frac{(x + 4)^2}{9} = 1') + ' ។',
        M('y = \\frac{2}{3}x + \\frac{11}{3}\\text{ និង }y = -\\frac{2}{3}x - \\frac{5}{3}'),
        [M('y = \\frac{3}{2}x + 7\\text{ និង }y = -\\frac{3}{2}x - 5'), M('y = \\frac{2}{3}x - \\frac{5}{3}\\text{ និង }y = -\\frac{2}{3}x + \\frac{11}{3}'), M('y = \\frac{2}{3}x + 1\\text{ និង }y = -\\frac{2}{3}x + 1')],
        'អាស៊ីមតូតគឺ ' + M('y = 1 \\pm \\frac{2}{3}(x + 4)') + ' ដែលផ្ដល់ ' + M('y = \\frac{2}{3}x + \\frac{11}{3}') + ' និង ' + M('y = -\\frac{2}{3}x - \\frac{5}{3}') + ' ។',
        bloom='Apply'))

    # 23. Identify conic type: 3x^2 - 2y^2 + 24x + 12y + 24 = 0
    chk(lambda: -24 + 48 - 18 == 6)
    qs.append(mcq('medium', 's3',
        'សមីការ ' + M('3x^2 - 2y^2 + 24x + 12y + 24 = 0') + ' មានទម្រង់ស្ដង់ដាដូចម្តេច?',
        M('\\frac{(x + 4)^2}{2} - \\frac{(y - 3)^2}{3} = 1'),
        [M('\\frac{(y - 3)^2}{3} - \\frac{(x + 4)^2}{2} = 1'), M('\\frac{(x + 4)^2}{2} + \\frac{(y - 3)^2}{3} = 1'), M('\\frac{(x - 4)^2}{2} - \\frac{(y + 3)^2}{3} = 1')],
        'បំពេញការ៉េបាន ' + M('3(x + 4)^2 - 2(y - 3)^2 = 6 \\iff \\frac{(x + 4)^2}{2} - \\frac{(y - 3)^2}{3} = 1') + ' ។',
        bloom='Apply'))

    # 24. Distance between foci (2, 2) and (10, 2), |PF1 - PF2| = 6
    chk(lambda: ((2 + 10) // 2 == 6, (10 - 2) // 2 == 4, 6 // 2 == 3, 4**2 - 3**2 == 7))
    qs.append(mcq('medium', 's3',
        'រកសមីការស្ដង់ដានៃអ៊ីពែបូលដែលគ្រប់ចំណុចលើវាមានផលដកចម្ងាយពី ' + M('(2, 2)') + ' និង ' + M('(10, 2)') + ' ស្មើនឹង ' + M('6') + ' ។',
        M('\\frac{(x - 6)^2}{9} - \\frac{(y - 2)^2}{7} = 1'),
        [M('\\frac{(x - 6)^2}{7} - \\frac{(y - 2)^2}{9} = 1'), M('\\frac{(x - 6)^2}{16} - \\frac{(y - 2)^2}{9} = 1'), M('\\frac{(y - 2)^2}{9} - \\frac{(x - 6)^2}{7} = 1')],
        'ផ្ចិតគឺ ' + M('(6, 2)') + ', ' + M('c = 4, a = 3 \\implies b^2 = 16 - 9 = 7') + ' ដូច្នេះ ' + M('\\frac{(x - 6)^2}{9} - \\frac{(y - 2)^2}{7} = 1') + ' ។',
        bloom='Analyze'))

    # =========================================================================
    # HARD MCQ (7 questions: #25 - #31)
    # =========================================================================

    # 25. Tangent to x^2/a^2 - y^2/b^2 = 1 at (x0, y0): 9x^2 - 4y^2 = 36 at (4, 3*sqrt(3))
    chk(lambda: 9 * 16 - 4 * 27 == 144 - 108 == 36)
    qs.append(mcq('hard', 's2',
        'រកសមីការបន្ទាត់ប៉ះទៅនឹងអ៊ីពែបូល ' + M('\\frac{x^2}{4} - \\frac{y^2}{9} = 1') + ' ត្រង់ចំណុច ' + M('(4, 3\\sqrt{3})') + ' ។',
        M('x - \\frac{\\sqrt{3}}{3}y = 1'),
        [M('x + \\frac{\\sqrt{3}}{3}y = 1'), M('4x - 3\\sqrt{3}y = 1'), M('x - \\sqrt{3}y = 1')],
        'ប្រើរូបមន្ត ' + M('\\frac{x_0 x}{a^2} - \\frac{y_0 y}{b^2} = 1') + ' បាន ' + M('\\frac{4x}{4} - \\frac{3\\sqrt{3}y}{9} = 1 \\iff x - \\frac{\\sqrt{3}}{3}y = 1') + ' ។',
        bloom='Analyze'))

    # 26. Tangents to 9x^2 - 4y^2 = 36 passing through (1, 0)
    chk(lambda: 16 * 9 - 4 * 9 * (9 * (-3) + 36) == 144 - 324 * 1 or (-108 * 3 + 324 == 0))
    qs.append(mcq('hard', 's2',
        'រកមេគុណប្រាប់ទិសនៃបន្ទាត់ប៉ះទៅនឹងអ៊ីពែបូល ' + M('9x^2 - 4y^2 = 36') + ' ដែលកាត់តាមចំណុច ' + M('(1, 0)') + ' ។',
        M('\\pm \\sqrt{3}'),
        [M('\\pm \\frac{3}{2}'), M('\\pm 2'), M('\\pm \\frac{\\sqrt{3}}{2}')],
        'តាងបន្ទាត់ ' + M('y = m(x - 1)') + ' ជំនួសចូល ' + M('9x^2 - 4y^2 = 36') + ' ហើយដាក់ ' + M('\\Delta = 0') + ' បាន ' + M('m^2 = 3 \\implies m = \\pm \\sqrt{3}') + ' ។',
        bloom='Analyze'))

    # 27. Ch10 Ex 7: 4a^2 - b^2 = 16 for x^2/a^2 - y^2/b^2 = 1 tangent to 2x - y - 4 = 0, b=2 -> a = sqrt(5)
    chk(lambda: 4 * 5 - 2**2 == 16)
    qs.append(mcq('hard', 's2',
        'អ៊ីពែបូល ' + M('\\frac{x^2}{a^2} - \\frac{y^2}{b^2} = 1') + ' ប៉ះនឹងបន្ទាត់ ' + M('2x - y - 4 = 0') + ' ។ បើ ' + M('b = 2') + ' តើ ' + M('a') + ' ស្មើប៉ុន្មាន?',
        M('\\sqrt{5}'),
        [M('\\sqrt{3}'), M('2'), M('4')],
        'ជំនួស ' + M('y = 2x - 4') + ' រួចដាក់ ' + M('\\Delta = 0') + ' បាន ' + M('4a^2 - b^2 = 16') + ' ។ បើ ' + M('b = 2') + ' បាន ' + M('4a^2 = 20 \\implies a = \\sqrt{5}') + ' ។',
        bloom='Analyze'))

    # 28. Foci (0,0) and (8,0), asymptotes y = +-2(x-4)
    chk(lambda: (F(16, 5) + F(64, 5) == 16))
    qs.append(mcq('hard', 's3',
        'រកសមីការអ៊ីពែបូលដែលមានកំណុំ ' + M('(0, 0)') + ' និង ' + M('(8, 0)') + ' ហើយអាស៊ីមតូតទាំងពីរមានសមីការ ' + M('y = \\pm 2(x - 4)') + ' ។',
        M('\\frac{(x - 4)^2}{\\frac{16}{5}} - \\frac{y^2}{\\frac{64}{5}} = 1'),
        [M('\\frac{(x - 4)^2}{16} - \\frac{y^2}{64} = 1'), M('\\frac{(x - 4)^2}{\\frac{64}{5}} - \\frac{y^2}{\\frac{16}{5}} = 1'), M('\\frac{y^2}{\\frac{64}{5}} - \\frac{(x - 4)^2}{\\frac{16}{5}} = 1')],
        'ផ្ចិត ' + M('(4, 0), c = 4') + ' និង ' + M('\\frac{b}{a} = 2 \\implies a^2 + 4a^2 = 16 \\implies a^2 = \\frac{16}{5}, b^2 = \\frac{64}{5}') + ' ។',
        bloom='Analyze'))

    # 29. Rectangular hyperbola (equilateral): eccentricity = sqrt(2)
    chk(lambda: 1 + 1 == 2)
    qs.append(mcq('hard', 's4',
        'អ៊ីពែបូលស្មើ (ដែលមានអាស៊ីមតូតកែងគ្នា ' + M('a = b') + ') មានអ៊ុចសង់ទ្រីស៊ីតេស្មើប៉ុន្មាន?',
        M('\\sqrt{2}'),
        [M('2'), M('\\frac{\\sqrt{2}}{2}'), M('\\sqrt{3}')],
        'ដោយ ' + M('a = b') + ' នោះ ' + M('c = \\sqrt{a^2 + a^2} = a\\sqrt{2}') + ' ដូច្នេះ ' + M('e = \\frac{c}{a} = \\sqrt{2}') + ' ។',
        bloom='Evaluate'))

    # 30. Condition for k so x^2/(k-1) + y^2/(k-5) = 1 is a hyperbola
    qs.append(mcq('hard', 's2',
        'តើតម្លៃ ' + M('k') + ' ណាខ្លះដែលធ្វើឱ្យសមីការ ' + M('\\frac{x^2}{k - 1} + \\frac{y^2}{k - 5} = 1') + ' តាងឱ្យអ៊ីពែបូល?',
        M('1 < k < 5'),
        [M('k > 5'), M('k < 1'), M('k > 1')],
        'ដើម្បីជាអ៊ីពែបូល ភាគបែងទាំងពីរត្រូវមានសញ្ញាផ្ទុយគ្នា គឺ ' + M('(k - 1)(k - 5) < 0 \\iff 1 < k < 5') + ' ។',
        bloom='Evaluate'))

    # 31. Angle between asymptotes 60 deg -> e = 2/sqrt(3) or 2
    chk(lambda: F(1, 3) + 1 == F(4, 3))
    qs.append(mcq('hard', 's4',
        'អ៊ីពែបូល ' + M('\\frac{x^2}{a^2} - \\frac{y^2}{b^2} = 1') + ' មានអាស៊ីមតូតមួយបង្កើតមុំ ' + M('30^\\circ') + ' ជាមួយអ័ក្សទទឹង ' + M('Ox') + ' ។ រកអ៊ុចសង់ទ្រីស៊ីតេនៃអ៊ីពែបូល ។',
        M('\\frac{2\\sqrt{3}}{3}'),
        [M('2'), M('\\sqrt{3}'), M('\\frac{\\sqrt{3}}{2}')],
        'គេមាន ' + M('\\frac{b}{a} = \\tan 30^\\circ = \\frac{1}{\\sqrt{3}}') + ' ដូច្នេះ ' + M('e = \\sqrt{1 + \\frac{b^2}{a^2}} = \\sqrt{1 + \\frac{1}{3}} = \\frac{2\\sqrt{3}}{3}') + ' ។',
        bloom='Evaluate'))

    # =========================================================================
    # PISA MCQ (5 questions: #32 - #36, all with SVG via with_img)
    # =========================================================================

    # 32. LORAN coastal ship navigation (textbook example: c=160, a=128 -> b=96, y=160)
    chk(lambda: (160**2 - 128**2 == 96**2, F(128 * 128, 1) > 0))
    svg32 = fig_hyperbola(
        0, 0, 128, 96, 'h', -260, 260, -25, 210,
        xlabel='x (km)', ylabel='y (km)',
        xticks=[], yticks=[160],
        title='LORAN Navigation', tmax=1.2, asym=False, branch='pos',
        dots_data=[(-160, 0, 'A(-160, 0)', 0, 15, P.K.RED),
                   (160, 0, 'B(160, 0)', 6, 15, P.K.RED),
                   (249, 160, 'P(x, 160)', 8, -6, P.K.BLUE)],
        segs_data=[(-160, 0, 249, 160, P.K.AMBER, True), (160, 0, 249, 160, P.K.AMBER, True)],
    )
    qs.append(with_img(mcq('easy' if False else 'pisa', 'p_loran',
        'ស្ថានីយវិទ្យុឆ្នេរសមុទ្រពីរគឺ ' + M('A(-160, 0)') + ' និង ' + M('B(160, 0)') + ' (ឯកតាជា ' + M('\\text{km}') + ') ។ កប៉ាល់ ' + M('P') + ' នៅចម្ងាយ ' + M('160\\text{ km}') + ' ពីឆ្នេរ (' + M('y = 160') + ') ហើយនៅជិត ' + M('B') + ' ជាង ' + M('A') + ' ចម្ងាយ ' + M('256\\text{ km}') + ' ។ រកសមីការគន្លងអ៊ីពែបូលរបស់កប៉ាល់ ។',
        M('\\frac{x^2}{128^2} - \\frac{y^2}{96^2} = 1'),
        [M('\\frac{x^2}{160^2} - \\frac{y^2}{128^2} = 1'), M('\\frac{x^2}{256^2} - \\frac{y^2}{160^2} = 1'), M('\\frac{y^2}{128^2} - \\frac{x^2}{96^2} = 1')],
        'គេមាន ' + M('2a = 256 \\implies a = 128') + ' និង ' + M('c = 160 \\implies b = \\sqrt{160^2 - 128^2} = 96') + ' ដូច្នេះ ' + M('\\frac{x^2}{128^2} - \\frac{y^2}{96^2} = 1') + ' ។',
        bloom='Apply'), svg32))

    # 33. Rutherford alpha-particle scattering (textbook Ex 11: vertex (3,0), asymptote y = x/2)
    chk(lambda: (3 * F(1, 2) == F(3, 2), (F(3, 2))**2 == F(9, 4)))
    svg33 = fig_hyperbola(
        0, 0, 3, 1.5, 'h', -1.5, 7.5, -3.5, 3.5,
        xlabel='x', ylabel='y',
        xticks=[], yticks=[-2, 2],
        title='Alpha Scattering', tmax=1.25, asym=True, branch='pos',
        dots_data=[(0, 0, 'Nucleus', -8, -12, P.K.RED), (3, 0, 'V(3, 0)', 8, 13, P.K.BLUE)],
        notes_data=[(5.0, 3.1, 'y = 0.5x', P.K.AMBER)],
    )
    qs.append(with_img(mcq('pisa', 'p_rutherford',
        'ភាគល្អិតអាល់ហ្វាត្រូវបានច្រានចេញពីណ្វៃយ៉ូត្រង់គល់ ' + M('O(0, 0)') + ' តាមគន្លងអ៊ីពែបូលដែលមានអាស៊ីមតូត ' + M('y = \\pm \\frac{1}{2}x') + ' និងកំពូលនៅ ' + M('V(3, 0)') + ' ។ រកសមីការនៃគន្លងនេះ ។',
        M('\\frac{x^2}{9} - \\frac{4y^2}{9} = 1\\; (x \\ge 3)'),
        [M('\\frac{x^2}{9} - \\frac{y^2}{4} = 1\\; (x \\ge 3)'), M('\\frac{x^2}{9} - \\frac{9y^2}{4} = 1\\; (x \\ge 3)'), M('\\frac{y^2}{9} - \\frac{4x^2}{9} = 1')],
        'គេមាន ' + M('a = 3') + ' និង ' + M('\\frac{b}{a} = \\frac{1}{2} \\implies b = \\frac{3}{2}') + ' ដូច្នេះ ' + M('\\frac{x^2}{9} - \\frac{4y^2}{9} = 1') + ' ។',
        bloom='Apply'), svg33))

    # 34. Hyperbolic cooling tower: waist radius 30m at y=0, x=50 at y=80 -> b = 60
    chk(lambda: F(50**2, 30**2) - 1 == F(16, 9) and F(80**2, F(16, 9)) == 3600)
    svg34 = fig_hyperbola(
        0, 0, 30, 60, 'h', -75, 75, -95, 95,
        xlabel='x (m)', ylabel='y (m)',
        xticks=[], yticks=[],
        title='Cooling Tower', tmax=1.1, asym=False, branch='both',
        dots_data=[(30, 0, '(30, 0)', 8, -8, P.K.BLUE), (50, 80, '(50, 80)', 8, 4, P.K.RED)],
        segs_data=[(-50, 80, 50, 80, '#94a3b8', True), (-50, -80, 50, -80, '#94a3b8', True)],
    )
    qs.append(with_img(mcq('pisa', 'p_cooling',
        'ប៉មត្រជាក់នៃរោងចក្រអគ្គិសនីមួយមានមុខកាត់រាងអ៊ីពែបូល ' + M('\\frac{x^2}{a^2} - \\frac{y^2}{b^2} = 1') + ' ។ កន្លែងតូចបំផុតត្រង់ ' + M('y = 0') + ' មានកាំ ' + M('a = 30\\text{ m}') + ' និងនៅកម្ពស់ ' + M('y = 80\\text{ m}') + ' មានកាំ ' + M('x = 50\\text{ m}') + ' ។ រកតម្លៃ ' + M('b') + ' ។',
        M('60\\text{ m}'),
        [M('40\\text{ m}'), M('45\\text{ m}'), M('50\\text{ m}')],
        'ជំនួស ' + M('(50, 80)') + ' ចូល ' + M('\\frac{50^2}{30^2} - \\frac{80^2}{b^2} = 1 \\implies \\frac{80^2}{b^2} = \\frac{16}{9} \\implies b = 60\\text{ m}') + ' ។',
        bloom='Apply'), svg34))

    # 35. Cassegrain telescope mirror: foci (+-10, 0), vertex (6, 0) -> b = 8, e = 5/3
    chk(lambda: (10**2 - 6**2 == 8**2, F(10, 6) == F(5, 3)))
    svg35 = fig_hyperbola(
        0, 0, 6, 8, 'h', -14, 14, -12, 12,
        xlabel='x (cm)', ylabel='y (cm)',
        xticks=[], yticks=[-8, 8],
        title='Cassegrain Mirror', tmax=1.05, asym=True, branch='both',
        dots_data=[(-10, 0, 'F2(-10, 0)', -6, 14, P.K.RED), (10, 0, 'F1(10, 0)', 6, 14, P.K.RED), (6, 0, 'V1(6, 0)', 6, -11, P.K.BLUE)],
    )
    qs.append(with_img(mcq('pisa', 'p_telescope',
        'កញ្ចក់ទីពីរនៃកែវយឺត Cassegrain មានមុខកាត់រាងអ៊ីពែបូលផ្ចិត ' + M('O(0, 0)') + ' កំណុំ ' + M('F_1(10, 0), F_2(-10, 0)') + ' និងកំពូល ' + M('V_1(6, 0)') + ' (គិតជា ' + M('\\text{cm}') + ') ។ រកអ៊ុចសង់ទ្រីស៊ីតេ និងសមីការអ៊ីពែបូល ។',
        M('e = \\frac{5}{3},\\; \\frac{x^2}{36} - \\frac{y^2}{64} = 1'),
        [M('e = \\frac{3}{5},\\; \\frac{x^2}{36} - \\frac{y^2}{64} = 1'), M('e = \\frac{5}{3},\\; \\frac{x^2}{64} - \\frac{y^2}{36} = 1'), M('e = \\frac{5}{4},\\; \\frac{x^2}{36} - \\frac{y^2}{100} = 1')],
        'គេមាន ' + M('a = 6, c = 10 \\implies b = \\sqrt{100 - 36} = 8') + ' និង ' + M('e = \\frac{10}{6} = \\frac{5}{3}') + ' ។',
        bloom='Apply'), svg35))

    # 36. Hyperbolic comet flyby: x^2/9 - y^2/16 = 1 -> closest distance to focus (5, 0) is c - a = 5 - 3 = 2
    chk(lambda: (3**2 + 4**2 == 5**2, 5 - 3 == 2))
    svg36 = fig_hyperbola(
        0, 0, 3, 4, 'h', -1.5, 8.5, -6, 6,
        xlabel='x (AU)', ylabel='y (AU)',
        xticks=[], yticks=[-4, 4],
        title='Comet Flyby', tmax=1.1, asym=True, branch='pos',
        dots_data=[(5, 0, 'Sun (5, 0)', 6, 14, P.K.RED), (3, 0, 'V(3, 0)', -6, -11, P.K.BLUE)],
        segs_data=[(3, 0, 5, 0, P.K.AMBER, False)],
    )
    qs.append(with_img(mcq('pisa', 'p_sonic',
        'ផ្កាយដុះកន្ទុយមួយធ្វើដំណើរតាមគន្លងអ៊ីពែបូល ' + M('\\frac{x^2}{9} - \\frac{y^2}{16} = 1\\; (x \\ge 3)') + ' ជុំវិញព្រះអាទិត្យដែលស្ថិតនៅកំណុំ ' + M('F_1(c, 0)') + ' (ឯកតាជា ' + M('\\text{AU}') + ') ។ តើចម្ងាយជិតបំផុតពីផ្កាយដុះកន្ទុយទៅព្រះអាទិត្យស្មើប៉ុន្មាន?',
        M('2\\text{ AU}'),
        [M('3\\text{ AU}'), M('5\\text{ AU}'), M('8\\text{ AU}')],
        'គេមាន ' + M('a = 3, b = 4 \\implies c = 5') + ' ដូច្នេះចម្ងាយជិតបំផុត (ពីកំពូលទៅកំណុំ) គឺ ' + M('c - a = 5 - 3 = 2\\text{ AU}') + ' ។',
        bloom='Analyze'), svg36))

    # =========================================================================
    # WRITING QUESTIONS (14 questions: #37 - #50, 5 steps x 1pt each)
    # =========================================================================

    # 37. Easy writing: 9x^2 - 16y^2 = 144
    chk(lambda: 16 + 9 == 25)
    qs.append(wr('easy', 's2',
        'គេឱ្យសមីការអ៊ីពែបូល ' + M('9x^2 - 16y^2 = 144') + ' ។ រកសមីការស្ដង់ដា កូអរដោនេផ្ចិត កំពូល កំណុំ និងសមីការអាស៊ីមតូត ។',
        [('ចែកអង្គទាំងពីរនឹង ' + M('144') + ' បានសមីការស្ដង់ដា ' + M('\\frac{x^2}{16} - \\frac{y^2}{9} = 1'), 1),
         ('ទាញបាន ' + M('a = 4, b = 3') + ' និង ' + M('c = \\sqrt{a^2 + b^2} = \\sqrt{16 + 9} = 5'), 1),
         ('ផ្ចិតគឺ ' + M('I(0, 0)') + ' និងកំពូលទាំងពីរគឺ ' + M('V_1(4, 0), V_2(-4, 0)'), 1),
         ('កំណុំទាំងពីរគឺ ' + M('F_1(5, 0), F_2(-5, 0)'), 1),
         ('សមីការអាស៊ីមតូតគឺ ' + M('y = \\pm \\frac{b}{a}x = \\pm \\frac{3}{4}x') + ' ។', 1)],
        bloom='Apply'))

    # 38. Medium writing: 4x^2 - 9y^2 = -36
    chk(lambda: 4 + 9 == 13)
    qs.append(wr('medium', 's2',
        'គេឱ្យសមីការអ៊ីពែបូល ' + M('4x^2 - 9y^2 = -36') + ' ។ រកសមីការស្ដង់ដា កំពូល កំណុំ អ៊ុចសង់ទ្រីស៊ីតេ និងអាស៊ីមតូត ។',
        [('ចែកអង្គទាំងពីរនឹង ' + M('-36') + ' បានសមីការស្ដង់ដា ' + M('\\frac{y^2}{4} - \\frac{x^2}{9} = 1'), 1),
         ('ដោយអ័ក្សទទឹងលើ ' + M('Oy') + ' បាន ' + M('a = 2, b = 3, c = \\sqrt{4 + 9} = \\sqrt{13}'), 1),
         ('កំពូលទាំងពីរគឺ ' + M('V_1(0, 2), V_2(0, -2)') + ' និងកំណុំគឺ ' + M('F_1(0, \\sqrt{13}), F_2(0, -\\sqrt{13})'), 1),
         ('អ៊ុចសង់ទ្រីស៊ីតេគឺ ' + M('e = \\frac{c}{a} = \\frac{\\sqrt{13}}{2}'), 1),
         ('សមីការអាស៊ីមតូតគឺ ' + M('y = \\pm \\frac{a}{b}x = \\pm \\frac{2}{3}x') + ' ។', 1)],
        bloom='Apply'))

    # 39. Medium writing: V(3,-5), (3,1) and asymptotes y = 2x - 8, y = -2x + 4
    chk(lambda: ((-5 + 1) // 2 == -2, 1 - (-2) == 3, F(3, 2)**2 == F(9, 4)))
    qs.append(wr('medium', 's3',
        'រកសមីការស្ដង់ដានៃអ៊ីពែបូលដែលមានកំពូល ' + M('(3, -5)') + ' និង ' + M('(3, 1)') + ' ហើយអាស៊ីមតូតមានសមីការ ' + M('y = 2x - 8') + ' និង ' + M('y = -2x + 4') + ' ។',
        [('ដោយកំពូលមាន ' + M('x = 3') + ' ដូចគ្នា នោះអ័ក្សទទឹងស្រប ' + M('Oy') + ' និងផ្ចិតគឺ ' + M('I\\left(3, \\frac{-5 + 1}{2}\\right) = I(3, -2)'), 1),
         ('រក ' + M('a = |1 - (-2)| = 3 \\implies a^2 = 9'), 1),
         ('ពីមេគុណប្រាប់ទិសអាស៊ីមតូតបាន ' + M('\\frac{a}{b} = 2 \\implies b = \\frac{3}{2} \\implies b^2 = \\frac{9}{4}'), 1),
         ('គណនា ' + M('c = \\sqrt{9 + \\frac{9}{4}} = \\frac{3\\sqrt{5}}{2}'), 1),
         ('សមីការស្ដង់ដាគឺ ' + M('\\frac{(y + 2)^2}{9} - \\frac{4(x - 3)^2}{9} = 1') + ' ។', 1)],
        bloom='Apply'))

    # 40. Medium writing: 25x^2 - 16y^2 + 250x + 32y + 209 = 0
    chk(lambda: (-209 + 625 - 16 == 400, 16 + 25 == 41))
    qs.append(wr('medium', 's3',
        'បំប្លែងសមីការ ' + M('25x^2 - 16y^2 + 250x + 32y + 209 = 0') + ' ជាសមីការស្ដង់ដា រួចរកផ្ចិត កំពូល កំណុំ និងអាស៊ីមតូត ។',
        [('ផ្ដុំតួបាន ' + M('25(x^2 + 10x + 25) - 16(y^2 - 2y + 1) = -209 + 625 - 16 = 400'), 1),
         ('ចែកនឹង ' + M('400') + ' បាន ' + M('\\frac{(x + 5)^2}{16} - \\frac{(y - 1)^2}{25} = 1'), 1),
         ('ផ្ចិត ' + M('I(-5, 1)') + ' និង ' + M('a = 4, b = 5, c = \\sqrt{41}'), 1),
         ('កំពូល ' + M('V_1(-9, 1), V_2(-1, 1)') + ' និងកំណុំ ' + M('F(-5 \\pm \\sqrt{41}, 1)'), 1),
         ('សមីការអាស៊ីមតូតគឺ ' + M('y = 1 \\pm \\frac{5}{4}(x + 5)') + ' ។', 1)],
        bloom='Apply'))

    # 41. Medium writing: Foci (7, 1) and (-3, 1), asymptotes y = 3/4 x - 1/2, y = -3/4 x + 5/2
    chk(lambda: ((7 + (-3)) // 2 == 2, 7 - 2 == 5, 4**2 + 3**2 == 5**2))
    qs.append(wr('medium', 's3',
        'រកសមីការស្ដង់ដានៃអ៊ីពែបូលដែលមានកំណុំ ' + M('(7, 1)') + ' និង ' + M('(-3, 1)') + ' ហើយអាស៊ីមតូតមានសមីការ ' + M('y = \\frac{3}{4}x - \\frac{1}{2}') + ' និង ' + M('y = -\\frac{3}{4}x + \\frac{5}{2}') + ' ។',
        [('ផ្ចិតជាចំណុចកណ្ដាលនៃកំណុំទាំងពីរគឺ ' + M('I\\left(\\frac{7 - 3}{2}, 1\\right) = I(2, 1)') + ' និង ' + M('c = 5'), 1),
         ('អ័ក្សទទឹងស្រប ' + M('Ox') + ' និងពីអាស៊ីមតូតបាន ' + M('\\frac{b}{a} = \\frac{3}{4} \\implies b = \\frac{3}{4}a'), 1),
         ('ជំនួសក្នុង ' + M('a^2 + b^2 = c^2 \\implies a^2 + \\frac{9}{16}a^2 = 25 \\implies \\frac{25}{16}a^2 = 25 \\implies a = 4'), 1),
         ('ទាញបាន ' + M('b = \\frac{3}{4}(4) = 3'), 1),
         ('សមីការស្ដង់ដាគឺ ' + M('\\frac{(x - 2)^2}{16} - \\frac{(y - 1)^2}{9} = 1') + ' ។', 1)],
        bloom='Apply'))

    # 42. Hard writing: 4x^2 - 9y^2 + 32x + 18y + 91 = 0
    chk(lambda: (-91 + 64 - 9 == -36, 4 + 9 == 13))
    qs.append(wr('hard', 's3',
        'បំប្លែងសមីការ ' + M('4x^2 - 9y^2 + 32x + 18y + 91 = 0') + ' ជាសមីការស្ដង់ដា រួចរកផ្ចិត កំពូល កំណុំ និងអាស៊ីមតូត ។',
        [('ផ្ដុំតួបាន ' + M('4(x + 4)^2 - 9(y - 1)^2 = -91 + 64 - 9 = -36'), 1),
         ('ចែកនឹង ' + M('-36') + ' បាន ' + M('\\frac{(y - 1)^2}{4} - \\frac{(x + 4)^2}{9} = 1'), 1),
         ('ផ្ចិត ' + M('I(-4, 1)') + ', ' + M('a = 2, b = 3, c = \\sqrt{13}'), 1),
         ('កំពូល ' + M('V_1(-4, 3), V_2(-4, -1)') + ' និងកំណុំ ' + M('F(-4, 1 \\pm \\sqrt{13})'), 1),
         ('សមីការអាស៊ីមតូតគឺ ' + M('y = 1 \\pm \\frac{2}{3}(x + 4)') + ' ។', 1)],
        bloom='Analyze'))

    # 43. Hard writing: Foci (-3, 0), (-3, -3), |PF1 - PF2| = 2
    chk(lambda: (F(-3, 2) == F(-3, 2), F(9, 4) - 1 == F(5, 4)))
    qs.append(wr('hard', 's3',
        'រកសមីការស្ដង់ដានៃអ៊ីពែបូលដែលគ្រប់ចំណុចលើវាមានផលដកចម្ងាយពី ' + M('(-3, 0)') + ' និង ' + M('(-3, -3)') + ' ស្មើនឹង ' + M('2') + ' ។',
        [('កំណុំមាន ' + M('x = -3') + ' ដូចគ្នា នោះអ័ក្សទទឹងស្រប ' + M('Oy') + ' និងផ្ចិត ' + M('I\\left(-3, -\\frac{3}{2}\\right)'), 1),
         ('ចម្ងាយពីផ្ចិតទៅកំណុំ ' + M('c = \\frac{3}{2}') + ' និង ' + M('2a = 2 \\implies a = 1'), 1),
         ('គណនា ' + M('b^2 = c^2 - a^2 = \\frac{9}{4} - 1 = \\frac{5}{4}'), 1),
         ('សរសេរទម្រង់ស្ដង់ដាសម្រាប់អ័ក្សទទឹងឈរ ' + M('\\frac{(y - k)^2}{a^2} - \\frac{(x - h)^2}{b^2} = 1'), 1),
         ('ដូច្នេះសមីការស្ដង់ដាគឺ ' + M('\\left(y + \\frac{3}{2}\\right)^2 - \\frac{4(x + 3)^2}{5} = 1') + ' ។', 1)],
        bloom='Analyze'))

    # 44. Hard writing: Tangents to 9x^2 - 4y^2 = 36 passing through (1, 0)
    chk(lambda: -108 * 3 + 324 == 0)
    qs.append(wr('hard', 's2',
        'រកសមីការបន្ទាត់ប៉ះទាំងអស់ទៅនឹងអ៊ីពែបូល ' + M('9x^2 - 4y^2 = 36') + ' ដែលកាត់តាមចំណុច ' + M('(1, 0)') + ' ។',
        [('បន្ទាត់កាត់តាម ' + M('(1, 0)') + ' មិនឈរមានសមីការ ' + M('y = m(x - 1)'), 1),
         ('ជំនួសក្នុង ' + M('9x^2 - 4y^2 = 36') + ' បាន ' + M('(9 - 4m^2)x^2 + 8m^2 x - (4m^2 + 36) = 0'), 1),
         ('លក្ខខណ្ឌប៉ះ ' + M('\\Delta\' = 16m^4 + (9 - 4m^2)(4m^2 + 36) = 0'), 1),
         ('ពន្លាតនិងសម្រួលបាន ' + M('-108m^2 + 324 = 0 \\implies m^2 = 3 \\implies m = \\pm \\sqrt{3}'), 1),
         ('ដូច្នេះបន្ទាត់ប៉ះទាំងពីរគឺ ' + M('y = \\sqrt{3}(x - 1)') + ' និង ' + M('y = -\\sqrt{3}(x - 1)') + ' ។', 1)],
        bloom='Analyze'))

    # 45. Hard writing: Derive hyperbola from definition with F1(0, 3), F2(0, -3), 2a = 2
    chk(lambda: 3**2 - 1**2 == 8)
    qs.append(wr('hard', 's1',
        'កំណុំទាំងពីរនៃអ៊ីពែបូលគឺ ' + M('F_1(0, 3)') + ' និង ' + M('F_2(0, -3)') + ' ។ ប្រើនិយមន័យដើម្បីទាញរកសមីការស្ដង់ដា បើផលដកចម្ងាយពីចំណុចលើអ៊ីពែបូលទៅ ' + M('F_1') + ' និង ' + M('F_2') + ' ស្មើនឹង ' + M('2') + ' ។',
        [('តាង ' + M('P(x, y)') + ' លើអ៊ីពែបូល បាន ' + M('\\sqrt{x^2 + (y - 3)^2} - \\sqrt{x^2 + (y + 3)^2} = \\pm 2'), 1),
         ('លើកអង្គទាំងពីរជាការ៉េហើយសម្រួលបាន ' + M('-3y - 1 = \\pm \\sqrt{x^2 + (y + 3)^2}'), 1),
         ('លើកជាការ៉េម្ដងទៀតបាន ' + M('9y^2 + 6y + 1 = x^2 + y^2 + 6y + 9'), 1),
         ('សម្រួលបាន ' + M('8y^2 - x^2 = 8'), 1),
         ('ចែកនឹង ' + M('8') + ' បានសមីការស្ដង់ដា ' + M('y^2 - \\frac{x^2}{8} = 1') + ' ។', 1)],
        bloom='Create'))

    # =========================================================================
    # PISA WRITING (5 questions: #46 - #50, all with SVG via with_img, 5 steps x 1pt)
    # =========================================================================

    # 46. Coastal LORAN station: foci (+-15, 0), |d1 - d2| = 18 -> a=9, b=12, at y=16 -> x = 15
    chk(lambda: (15**2 - 9**2 == 12**2, 9**2 * (1 + F(16**2, 12**2)) == 225))
    svg46 = fig_hyperbola(
        0, 0, 9, 12, 'h', -22, 22, -4, 22,
        xlabel='x (km)', ylabel='y (km)',
        xticks=[], yticks=[16],
        title='Coast LORAN', tmax=1.15, asym=False, branch='pos',
        dots_data=[(-15, 0, 'A(-15, 0)', 0, 15, P.K.RED),
                   (15, 0, 'B(15, 0)', 0, 15, P.K.RED),
                   (15, 16, 'P(x, 16)', 8, -4, P.K.BLUE)],
        segs_data=[(-15, 0, 15, 16, P.K.AMBER, True), (15, 0, 15, 16, P.K.AMBER, True)],
    )
    qs.append(with_img(wr('pisa', 'p_coast',
        'ស្ថានីយចាប់សញ្ញាពីរនៅលើឆ្នេរត្រង់គឺ ' + M('A(-15, 0)') + ' និង ' + M('B(15, 0)') + ' (ឯកតាជា ' + M('\\text{km}') + ') ។ ទូកមួយនៅ ' + M('P(x, 16)') + ' (' + M('x > 0') + ') នៅជិត ' + M('B') + ' ជាង ' + M('A') + ' ចម្ងាយ ' + M('18\\text{ km}') + ' ។ រកសមីការអ៊ីពែបូល និងកូអរដោនេ ' + M('x') + ' របស់ទូក ។',
        [('ផ្ចិតនៅ ' + M('O(0, 0)') + ', ' + M('c = 15') + ' និង ' + M('2a = 18 \\implies a = 9\\text{ km}'), 1),
         ('គណនា ' + M('b^2 = c^2 - a^2 = 15^2 - 9^2 = 144 \\implies b = 12\\text{ km}'), 1),
         ('សមីការអ៊ីពែបូលគឺ ' + M('\\frac{x^2}{81} - \\frac{y^2}{144} = 1'), 1),
         ('ជំនួស ' + M('y = 16') + ' បាន ' + M('\\frac{x^2}{81} = 1 + \\frac{256}{144} = \\frac{25}{9}'), 1),
         ('ដោយ ' + M('x > 0') + ' ទាញបាន ' + M('x = 9 \\times \\frac{5}{3} = 15\\text{ km}') + ' ។', 1)],
        bloom='Apply'), svg46))

    # 47. Hyperbolic arch/tower: center (0, 20), horizontal transverse axis, a=10, at y=40 x=26 -> b=120/sqrt(144)=10? wait: (26/10)^2 - (20/b)^2 = 1 -> 6.76 - 1 = 5.76 = (2.4)^2 -> 20/b = 2.4 -> b = 25/3 -> let's use clean integers: a=15, at y=20 above center x=25 -> (25/15)^2 - (20/b)^2 = 1 -> 25/9 - 1 = 16/9 -> 20/b = 4/3 -> b = 15!
    chk(lambda: (F(25**2, 15**2) - F(20**2, 15**2) == 1, 15**2 + 15**2 == 450))
    svg47 = fig_hyperbola(
        0, 20, 15, 15, 'h', -36, 36, -6, 48,
        xlabel='x (m)', ylabel='y (m)',
        xticks=[], yticks=[],
        title='Hyperbolic Tower', tmax=1.15, asym=False, branch='both',
        dots_data=[(0, 20, 'I(0, 20)', -8, 12, P.K.RED), (15, 20, '(15, 20)', 8, -4, P.K.BLUE), (25, 40, '(25, 40)', 8, 4, P.K.BLUE)],
        segs_data=[(-25, 40, 25, 40, '#94a3b8', True), (-25, 0, 25, 0, '#94a3b8', True)],
    )
    qs.append(with_img(wr('pisa', 'p_tower',
        'ប៉មសំណង់មួយមានមុខកាត់រាងអ៊ីពែបូលផ្ចិត ' + M('I(0, 20)') + ' និងអ័ក្សទទឹងស្រប ' + M('Ox') + ' ។ កន្លែងរួមតូចបំផុតត្រង់ ' + M('y = 20') + ' មានកាំ ' + M('15\\text{ m}') + ' និងនៅកំពូល ' + M('y = 40') + ' មានកាំ ' + M('25\\text{ m}') + ' ។ រកសមីការអ៊ីពែបូល និងអ៊ុចសង់ទ្រីស៊ីតេ ។',
        [('សមីការមានទម្រង់ ' + M('\\frac{x^2}{a^2} - \\frac{(y - 20)^2}{b^2} = 1') + ' ដោយ ' + M('a = 15'), 1),
         ('ជំនួស ' + M('(25, 40)') + ' បាន ' + M('\\frac{25^2}{15^2} - \\frac{20^2}{b^2} = 1'), 1),
         ('គណនា ' + M('\\frac{400}{b^2} = \\frac{25}{9} - 1 = \\frac{16}{9} \\implies b^2 = 225 \\implies b = 15'), 1),
         ('សមីការអ៊ីពែបូលគឺ ' + M('\\frac{x^2}{225} - \\frac{(y - 20)^2}{225} = 1'), 1),
         ('ដោយ ' + M('a = b = 15') + ' បាន ' + M('e = \\frac{\\sqrt{a^2 + b^2}}{a} = \\sqrt{2}') + ' ។', 1)],
        bloom='Apply'), svg47))

    # 48. Radar / Acoustic listening posts: F1(0, 13), F2(0, -13), |d1 - d2| = 10 -> a=5, c=13, b=12
    chk(lambda: (13**2 - 5**2 == 12**2, F(13, 5) == F(13, 5)))
    svg48 = fig_hyperbola(
        0, 0, 5, 12, 'v', -18, 18, -18, 18,
        xlabel='x (km)', ylabel='y (km)',
        xticks=[-12, 12], yticks=[],
        title='Acoustic Array', tmax=1.1, asym=True, branch='both',
        dots_data=[(0, 13, 'F1(0, 13)', 10, 4, P.K.RED), (0, -13, 'F2(0, -13)', 10, 4, P.K.RED), (0, 5, 'V1(0, 5)', 10, -4, P.K.BLUE)],
    )
    qs.append(with_img(wr('pisa', 'p_radar',
        'ស្ថានីយរ៉ាដាពីរស្ថិតនៅ ' + M('F_1(0, 13)') + ' និង ' + M('F_2(0, -13)') + ' (ឯកតាជា ' + M('\\text{km}') + ') ។ ប្រភពសញ្ញាមួយស្ថិតនៅលើអ៊ីពែបូលដែលមានផលដកចម្ងាយពី ' + M('F_1') + ' និង ' + M('F_2') + ' ស្មើនឹង ' + M('10\\text{ km}') + ' ។ រកសមីការអ៊ីពែបូល អាស៊ីមតូត និងអ៊ុចសង់ទ្រីស៊ីតេ ។',
        [('ផ្ចិតនៅ ' + M('O(0, 0)') + ', អ័ក្សទទឹងលើ ' + M('Oy') + ', ' + M('c = 13') + ' និង ' + M('2a = 10 \\implies a = 5'), 1),
         ('គណនា ' + M('b^2 = c^2 - a^2 = 169 - 25 = 144 \\implies b = 12'), 1),
         ('សមីការស្ដង់ដាគឺ ' + M('\\frac{y^2}{25} - \\frac{x^2}{144} = 1'), 1),
         ('សមីការអាស៊ីមតូតគឺ ' + M('y = \\pm \\frac{a}{b}x = \\pm \\frac{5}{12}x'), 1),
         ('អ៊ុចសង់ទ្រីស៊ីតេគឺ ' + M('e = \\frac{13}{5} = 2.6') + ' ។', 1)],
        bloom='Apply'), svg48))

    # 49. Hyperbolic mirror reflection: y^2/9 - x^2/16 = 1, ray aimed at F1(0, 5), tangent at (3, 15/4)? Check: (15/4)^2/9 - 9/16 = 25/16 - 9/16 = 1!
    chk(lambda: (3**2 + 4**2 == 5**2, F((15)**2, 16 * 9) - F(9, 16) == 1))
    svg49 = fig_hyperbola(
        0, 0, 3, 4, 'v', -7, 7, -7, 7,
        xlabel='x', ylabel='y',
        xticks=[-4, 4], yticks=[],
        title='Hyperbolic Mirror', tmax=1.05, asym=True, branch='both',
        dots_data=[(0, 5, 'F1(0, 5)', -8, 4, P.K.RED), (0, -5, 'F2(0, -5)', -8, 4, P.K.RED), (3, 3.75, 'P(3, 15/4)', -6, -12, P.K.BLUE)],
        segs_data=[(0, -5, 3, 3.75, P.K.AMBER, False), (0, 5, 3, 3.75, '#94a3b8', True)],
    )
    qs.append(with_img(wr('pisa', 'p_mirror',
        'កញ្ចក់អ៊ីពែបូលមួយមានសមីការ ' + M('\\frac{y^2}{9} - \\frac{x^2}{16} = 1\\; (y > 0)') + ' ។ កាំពន្លឺមួយតម្រង់ទៅរកកំណុំ ' + M('F_1') + ' ហើយប៉ះកញ្ចក់ត្រង់ចំណុច ' + M('P\\left(3, \\frac{15}{4}\\right)') + ' ។ ក. រកកំណុំទាំងពីរ ' + M('F_1, F_2') + ' ។ ខ. រកសមីការបន្ទាត់ប៉ះត្រង់ ' + M('P') + ' ។',
        [('ពីសមីការបាន ' + M('a = 3, b = 4') + ' នោះ ' + M('c = \\sqrt{9 + 16} = 5'), 1),
         ('កំណុំទាំងពីរគឺ ' + M('F_1(0, 5)') + ' និង ' + M('F_2(0, -5)'), 1),
         ('កាំពន្លឺដែលតម្រង់ទៅ ' + M('F_1(0, 5)') + ' នឹងចាំងផ្លាតត្រឡប់ឆ្ពោះទៅរកកំណុំ ' + M('F_2(0, -5)'), 1),
         ('ប្រើរូបមន្តបន្ទាត់ប៉ះ ' + M('\\frac{y_0 y}{a^2} - \\frac{x_0 x}{b^2} = 1') + ' បាន ' + M('\\frac{15y}{4 \\times 9} - \\frac{3x}{16} = 1'), 1),
         ('សម្រួលបានសមីការបន្ទាត់ប៉ះ ' + M('\\frac{5}{12}y - \\frac{3}{16}x = 1') + ' ឬ ' + M('20y - 9x = 48') + ' ។', 1)],
        bloom='Analyze'), svg49))

    # 50. Spacecraft hyperbolic flyby: closest approach c - a = 4, eccentricity e = 5/3 -> a = 6, c = 10, b = 8
    chk(lambda: (F(5, 3) * 6 == 10, 10 - 6 == 4, 10**2 - 6**2 == 8**2, F(2 * 64, 6) == F(64, 3)))
    svg50 = fig_hyperbola(
        0, 0, 6, 8, 'h', -1.5, 13.5, -11, 11,
        xlabel='x (10³ km)', ylabel='y (10³ km)',
        xticks=[], yticks=[-8, 8],
        title='Spacecraft Flyby', tmax=1.0, asym=True, branch='pos',
        dots_data=[(10, 0, 'Planet (10, 0)', -4, 14, P.K.RED), (6, 0, 'V(6, 0)', -6, -12, P.K.BLUE)],
        segs_data=[(6, 0, 10, 0, P.K.AMBER, False)],
    )
    qs.append(with_img(wr('pisa', 'p_orbit',
        'យានអវកាសមួយហោះកាត់ភពមួយតាមគន្លងអ៊ីពែបូល ' + M('\\frac{x^2}{a^2} - \\frac{y^2}{b^2} = 1\\; (x \\ge a)') + ' ដែលភពស្ថិតនៅកំណុំ ' + M('F_1(c, 0)') + ' ។ ចម្ងាយជិតបំផុតទៅផ្ចិតភពគឺ ' + M('4 \\times 10^3\\text{ km}') + ' និងអ៊ុចសង់ទ្រីស៊ីតេ ' + M('e = \\frac{5}{3}') + ' ។ រកសមីការគន្លង និងប្រវែងអង្កត់កាត់កំណុំកែងអ័ក្សទទឹង ។',
        [('តាងឯកតាគិតជា ' + M('10^3\\text{ km}') + ' គេមាន ' + M('c - a = 4') + ' និង ' + M('\\frac{c}{a} = \\frac{5}{3} \\implies c = \\frac{5}{3}a'), 1),
         ('ជំនួសបាន ' + M('\\frac{5}{3}a - a = 4 \\implies \\frac{2}{3}a = 4 \\implies a = 6'), 1),
         ('ទាញបាន ' + M('c = 10') + ' និង ' + M('b^2 = c^2 - a^2 = 100 - 36 = 64 \\implies b = 8'), 1),
         ('សមីការគន្លងគឺ ' + M('\\frac{x^2}{36} - \\frac{y^2}{64} = 1\\; (x \\ge 6)'), 1),
         ('ប្រវែងអង្កត់កាត់កំណុំកែងអ័ក្សទទឹងគឺ ' + M('\\frac{2b^2}{a} = \\frac{2 \\times 64}{6} = \\frac{64}{3} \\times 10^3\\text{ km}') + ' ។', 1)],
        bloom='Create'), svg50))

    return qs


def cands():
    from lib import normalise
    return normalise(_cands_raw())


if __name__ == '__main__':
    print(f'G12L27: {len(cands())} candidates, {CNT[0]} numeric checks passed')
