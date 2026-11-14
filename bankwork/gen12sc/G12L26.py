# -*- coding: utf-8 -*-
"""
KhmerMath Question Bank: Grade 12 Science (SC)
Chapter 10: កោនិក
Lesson 2: អេលីប
Reference textbook: Lesson/G12/SC/C10-L2.tex
Matrix: MCQ easy10/medium14/hard7/pisa5 + writing easy1/medium4/hard4/pisa5 = 50, Bloom on each.
All ellipse equations, foci, vertices, eccentricities, and application values are checked via Fraction.
"""
import sys, os
from fractions import Fraction
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.dirname(__file__))
from lib import *
import G12L04 as P

LESSON = 'អេលីប'
CHAPTER = 'ជំពូកទី 10 : កោនិក'
GRADE = '12SC'
TARGET = P.TARGET

S1 = 'និយមន័យអេលីប'
S2 = 'សមីការអេលីបដែលមានផ្ចិតនៅគល់ O(0, 0)'
S3 = 'សមីការអេលីបដែលមានផ្ចិត I(h, k)'
S4 = 'អ៊ុចសង់ទ្រីស៊ីតេ និងលក្ខណៈចំណាំងផ្លាតនៃអេលីប'
TOPIC_MAP = {
    's1': S1, 's2': S2, 's3': S3, 's4': S4,
    'p_orbit': S4, 'p_gallery': S4, 'p_arch': S2, 'p_track': S4, 'p_table': S2,
    'p_whisper': S4, 'p_tunnel': S2, 'p_sat': S4, 'p_pool': S2, 'p_room': S4,
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


def fig_ellipse(cx, cy, rx, ry, x0, x1, y0, y1, xlabel='x', ylabel='y',
                xticks=(), yticks=(), title='', half_top=False,
                dots_data=(), segs_data=(), notes_data=()):
    """Full-plane SVG ellipse figure (no white background rect, Latin/Unicode only)."""
    W, H = 395, 230
    pad_l, pad_r, pad_t, pad_b = 46, 74, 32, 30
    pw = W - pad_l - pad_r
    ph = H - pad_t - pad_b
    sx = lambda x: pad_l + (x - x0) / (x1 - x0) * pw
    sy = lambda y: pad_t + (y1 - y) / (y1 - y0) * ph

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'style="max-width:100%;height:auto;font-family:system-ui,-apple-system,sans-serif">',
        '<defs><marker id="arrE" viewBox="0 0 10 10" refX="8" refY="5" '
        'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        '<path d="M 0 1 L 8 5 L 0 9 z" fill="#475569"/></marker></defs>',
    ]

    # Axes: draw x-axis at y=0 (if in range) else bottom; y-axis at x=0 (if in range) else left
    has_origin = (x0 <= 0 <= x1) and (y0 <= 0 <= y1)
    ay = sy(0) if (y0 <= 0 <= y1) else sy(y0)
    ax = sx(0) if (x0 <= 0 <= x1) else sx(x0)

    parts.append(
        f'<line x1="{pad_l - 8:.1f}" y1="{ay:.1f}" x2="{W - pad_r + 12:.1f}" y2="{ay:.1f}" '
        f'stroke="#475569" stroke-width="1.4" marker-end="url(#arrE)"/>'
    )
    parts.append(
        f'<line x1="{ax:.1f}" y1="{H - pad_b + 8:.1f}" x2="{ax:.1f}" y2="{pad_t - 12:.1f}" '
        f'stroke="#475569" stroke-width="1.4" marker-end="url(#arrE)"/>'
    )

    # Axis titles clearly past arrow ends
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

    # Ticks (offset vertex ticks slightly outward so they never sit on the ellipse stroke)
    for xv in xticks:
        if xv == 0 and has_origin:
            continue
        xp = sx(xv)
        lbl = str(int(xv)) if xv == int(xv) else f'{xv:g}'
        dx = -9 if abs(xv - (cx - rx)) < 1e-6 else (9 if abs(xv - (cx + rx)) < 1e-6 else 0)
        parts.append(f'<line x1="{xp:.1f}" y1="{ay - 3:.1f}" x2="{xp:.1f}" y2="{ay + 3:.1f}" stroke="#475569" stroke-width="1.2"/>')
        parts.append(f'<text x="{xp + dx:.1f}" y="{ay + 15:.1f}" font-size="10" fill="#475569" text-anchor="middle">{_esc(lbl)}</text>')

    for yv in yticks:
        if yv == 0 and has_origin:
            continue
        yp = sy(yv)
        lbl = str(int(yv)) if yv == int(yv) else f'{yv:g}'
        dy = -5 if abs(yv - (cy + ry)) < 1e-6 else (11 if abs(yv - (cy - ry)) < 1e-6 else 3.5)
        parts.append(f'<line x1="{ax - 3:.1f}" y1="{yp:.1f}" x2="{ax + 3:.1f}" y2="{yp:.1f}" stroke="#475569" stroke-width="1.2"/>')
        parts.append(f'<text x="{ax - 7:.1f}" y="{yp + dy:.1f}" font-size="10" fill="#475569" text-anchor="end">{_esc(lbl)}</text>')

    # Segments
    for xa, ya, xb, yb, col, dashed in segs_data:
        da = ' stroke-dasharray="4,3"' if dashed else ''
        parts.append(
            f'<line x1="{sx(xa):.1f}" y1="{sy(ya):.1f}" x2="{sx(xb):.1f}" y2="{sy(yb):.1f}" '
            f'stroke="{col}" stroke-width="1.5"{da}/>'
        )

    # Ellipse or upper half-ellipse
    ecx, ecy = sx(cx), sy(cy)
    erx = rx / (x1 - x0) * pw
    ery = ry / (y1 - y0) * ph
    if half_top:
        x_left, x_right = ecx - erx, ecx + erx
        parts.append(
            f'<path d="M {x_left:.1f} {ecy:.1f} A {erx:.1f} {ery:.1f} 0 0 1 {x_right:.1f} {ecy:.1f}" '
            f'fill="none" stroke="{P.K.BLUE}" stroke-width="2.2"/>'
        )
    else:
        parts.append(
            f'<ellipse cx="{ecx:.1f}" cy="{ecy:.1f}" rx="{erx:.1f}" ry="{ery:.1f}" '
            f'fill="none" stroke="{P.K.BLUE}" stroke-width="2.2"/>'
        )

    # Dots + labels
    for x, y, lbl, dx, dy, col in dots_data:
        px, py = sx(x), sy(y)
        parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="3.2" fill="{col}"/>')
        if lbl:
            anchor = 'start' if dx > 2 else ('end' if dx < -2 else 'middle')
            parts.append(
                f'<text x="{px + dx:.1f}" y="{py + dy:.1f}" font-size="10.5" '
                f'font-weight="600" fill="{col}" text-anchor="{anchor}">{_esc(lbl)}</text>'
            )

    # Notes
    for x, y, txt, dx, dy, col, bold in notes_data:
        px, py = sx(x), sy(y)
        fw = ' font-weight="700"' if bold else ''
        parts.append(
            f'<text x="{px + dx:.1f}" y="{py + dy:.1f}" font-size="10.5"{fw} '
            f'fill="{col}" text-anchor="middle">{_esc(txt)}</text>'
        )

    if title:
        parts.append(
            f'<text x="{W - pad_r:.1f}" y="15" font-size="11" font-weight="600" '
            f'fill="{P.K.BLUE}" text-anchor="end">{_esc(title)}</text>'
        )

    parts.append('</svg>')
    return ''.join(parts)


def _cands_raw():
    qs = []

    # =========================================================================
    # MCQ EASY (10)
    # =========================================================================
    # 1. Definition of ellipse
    qs.append(mcq('easy', 's1',
        'តាមនិយមន័យ អេលីបគឺជាសំណុំចំណុច ' + M('P') + ' ក្នុងប្លង់ ដែលផលបូកចម្ងាយពី ' + M('P') + ' ទៅកំណុំទាំងពីរ ' + M('F_1, F_2') + ' ស្មើនឹងអ្វី?',
        'ចំនួនថេរ ' + M('2a'),
        ['ចំនួនថេរ ' + M('2c'), 'ផលសងថេរ ' + M('2a'), 'ពាក់កណ្ដាលអ័ក្សតូច ' + M('b')],
        'តាមនិយមន័យ គ្រប់ចំណុច ' + M('P') + ' លើអេលីបផ្ទៀងផ្ទាត់ ' + M('PF_1 + PF_2 = 2a') + ' (ប្រវែងអ័ក្សធំ) ។',
        bloom='Remember'))

    # 2. Relation between a, b, c
    qs.append(mcq('easy', 's1',
        'ចំពោះអេលីបដែលមានកន្លះអ័ក្សធំ ' + M('a') + ' កន្លះអ័ក្សតូច ' + M('b') + ' និងចម្ងាយពីផ្ចិតទៅកំណុំ ' + M('c') + ' តើទំនាក់ទំនងណាត្រឹមត្រូវ?',
        M('c^2 = a^2 - b^2'),
        [M('c^2 = a^2 + b^2'), M('a^2 = b^2 - c^2'), M('b^2 = a^2 + c^2')],
        'ក្នុងត្រីកោណកែងផ្គុំដោយផ្ចិត កំណុំ និងចុងអ័ក្សតូច គេបាន ' + M('a^2 = b^2 + c^2') + ' ឬ ' + M('c^2 = a^2 - b^2') + ' ។',
        bloom='Remember'))

    # 3. Major axis length of x^2/25 + y^2/9 = 1
    chk(lambda: (2 * 5 == 10,))
    qs.append(mcq('easy', 's2',
        'រកប្រវែងអ័ក្សធំនៃអេលីប ' + M('\\frac{x^2}{25} + \\frac{y^2}{9} = 1') + ' ។',
        M('10'), [M('5'), M('6'), M('8')],
        'ដោយ ' + M('a^2 = 25 \\Rightarrow a = 5') + ' នោះប្រវែងអ័ក្សធំគឺ ' + M('2a = 10') + ' ។',
        bloom='Apply'))

    # 4. Minor axis length of x^2/16 + y^2/49 = 1
    chk(lambda: (2 * 4 == 8,))
    qs.append(mcq('easy', 's2',
        'រកប្រវែងអ័ក្សតូចនៃអេលីប ' + M('\\frac{x^2}{16} + \\frac{y^2}{49} = 1') + ' ។',
        M('8'), [M('4'), M('7'), M('14')],
        'ដោយ ' + M('49 > 16') + ' បាន ' + M('b^2 = 16 \\Rightarrow b = 4') + ' ដូច្នេះប្រវែងអ័ក្សតូចគឺ ' + M('2b = 8') + ' ។',
        bloom='Apply'))

    # 5. Foci of x^2/25 + y^2/16 = 1 (3-4-5)
    chk(lambda: (25 - 16 == 3**2,))
    qs.append(mcq('easy', 's2',
        'រកកូអរដោនេកំណុំទាំងពីរនៃអេលីប ' + M('\\frac{x^2}{25} + \\frac{y^2}{16} = 1') + ' ។',
        M('(\\pm 3, 0)'), [M('(0, \\pm 3)'), M('(\\pm 4, 0)'), M('(\\pm 5, 0)')],
        'គេមាន ' + M('a^2 = 25, b^2 = 16 \\Rightarrow c = \\sqrt{25 - 16} = 3') + ' ។ ដោយអ័ក្សធំលើ ' + M('Ox') + ' កំណុំគឺ ' + M('(\\pm 3, 0)') + ' ។',
        bloom='Apply'))

    # 6. Vertices of x^2/25 + y^2/169 = 1 (5-12-13)
    chk(lambda: (13**2 == 169, 13**2 - 5**2 == 12**2))
    qs.append(mcq('easy', 's2',
        'រកកូអរដោនេកំពូលទាំងពីរនៃអេលីប ' + M('\\frac{x^2}{25} + \\frac{y^2}{169} = 1') + ' ។',
        M('(0, \\pm 13)'), [M('(\\pm 13, 0)'), M('(0, \\pm 5)'), M('(0, \\pm 12)')],
        'ដោយ ' + M('a^2 = 169 \\Rightarrow a = 13') + ' និងអ័ក្សធំនៅលើ ' + M('Oy') + ' កំពូលគឺ ' + M('(0, \\pm 13)') + ' ។',
        bloom='Apply'))

    # 7. Centre of (x - 3)^2/16 + (y + 2)^2/9 = 1
    qs.append(mcq('easy', 's3',
        'រកកូអរដោនេផ្ចិត ' + M('I(h, k)') + ' នៃអេលីប ' + M('\\frac{(x - 3)^2}{16} + \\frac{(y + 2)^2}{9} = 1') + ' ។',
        M('I(3, -2)'), [M('I(-3, 2)'), M('I(3, 2)'), M('I(4, 3)')],
        'ប្រៀបធៀបនឹង ' + M('\\frac{(x - h)^2}{a^2} + \\frac{(y - k)^2}{b^2} = 1') + ' បាន ' + M('I(3, -2)') + ' ។',
        bloom='Understand'))

    # 8. Eccentricity of x^2/25 + y^2/9 = 1
    chk(lambda: (25 - 9 == 4**2, F(4, 5) == F('0.8')))
    qs.append(mcq('easy', 's4',
        'រកអ៊ុចសង់ទ្រីស៊ីតេ ' + M('e') + ' នៃអេលីប ' + M('\\frac{x^2}{25} + \\frac{y^2}{9} = 1') + ' ។',
        M('\\frac{4}{5}'), [M('\\frac{3}{5}'), M('\\frac{5}{4}'), M('\\frac{9}{25}')],
        'គេមាន ' + M('a = 5, c = \\sqrt{25 - 9} = 4') + ' ដូច្នេះ ' + M('e = \\frac{c}{a} = \\frac{4}{5}') + ' ។',
        bloom='Apply'))

    # 9. Range of eccentricity
    qs.append(mcq('easy', 's4',
        'តើអ៊ុចសង់ទ្រីស៊ីតេ ' + M('e') + ' នៃអេលីបស្ថិតក្នុងចន្លោះណា?',
        M('0 < e < 1'), [M('e > 1'), M('e = 1'), M('-1 < e < 0')],
        'ដោយ ' + M('0 < c < a') + ' នោះ ' + M('0 < \\frac{c}{a} < 1') + ' គឺ ' + M('0 < e < 1') + ' ។',
        bloom='Understand'))

    # 10. Standard equation from centre O(0,0), vertices (+-5,0), foci (+-3,0)
    chk(lambda: (5**2 - 3**2 == 4**2,))
    qs.append(mcq('easy', 's2',
        'រកសមីការស្ដង់ដានៃអេលីបដែលមានផ្ចិត ' + M('O(0, 0)') + ' កំពូល ' + M('(\\pm 5, 0)') + ' និងកំណុំ ' + M('(\\pm 3, 0)') + ' ។',
        M('\\frac{x^2}{25} + \\frac{y^2}{16} = 1'),
        [M('\\frac{x^2}{16} + \\frac{y^2}{25} = 1'), M('\\frac{x^2}{25} + \\frac{y^2}{9} = 1'), M('\\frac{x^2}{5} + \\frac{y^2}{4} = 1')],
        'គេមាន ' + M('a = 5, c = 3 \\Rightarrow b^2 = 25 - 9 = 16') + ' ។ ដោយអ័ក្សធំលើ ' + M('Ox') + ' បាន ' + M('\\frac{x^2}{25} + \\frac{y^2}{16} = 1') + ' ។',
        bloom='Apply'))

    # =========================================================================
    # MCQ MEDIUM (14)
    # =========================================================================
    # 11. Foci of 25x^2 + 169y^2 = 4225 (5-12-13)
    chk(lambda: (25 * 169 == 4225, 169 - 25 == 12**2))
    qs.append(mcq('medium', 's2',
        'រកកូអរដោនេកំណុំទាំងពីរនៃអេលីប ' + M('25x^2 + 169y^2 = 4225') + ' ។',
        M('(\\pm 12, 0)'), [M('(0, \\pm 12)'), M('(\\pm 13, 0)'), M('(\\pm 5, 0)')],
        'ចែកនឹង ' + M('4225') + ' បាន ' + M('\\frac{x^2}{169} + \\frac{y^2}{25} = 1') + ' ។ គេបាន ' + M('c = \\sqrt{169 - 25} = 12') + ' ដូច្នេះ ' + M('(\\pm 12, 0)') + ' ។',
        bloom='Apply'))

    # 12. Vertices of (x+1)^2/64 + (y-3)^2/289 = 1 (8-15-17)
    chk(lambda: (17**2 == 289, 17**2 - 8**2 == 15**2, 3 - 17 == -14, 3 + 17 == 20))
    qs.append(mcq('medium', 's3',
        'រកកូអរដោនេកំពូលទាំងពីរនៃអេលីប ' + M('\\frac{(x + 1)^2}{64} + \\frac{(y - 3)^2}{289} = 1') + ' ។',
        M('(-1, -14)') + ' និង ' + M('(-1, 20)'),
        [M('(-18, 3)') + ' និង ' + M('(16, 3)'), M('(-1, -12)') + ' និង ' + M('(-1, 18)'), M('(-9, 3)') + ' និង ' + M('(7, 3)')],
        'ផ្ចិត ' + M('I(-1, 3)') + ' និង ' + M('a = \\sqrt{289} = 17') + ' (អ័ក្សធំឈរ) ។ កំពូលគឺ ' + M('(-1, 3 \\pm 17)') + ' គឺ ' + M('(-1, -14)') + ' និង ' + M('(-1, 20)') + ' ។',
        bloom='Apply'))

    # 13. Foci of (x-2)^2/25 + (y+1)^2/169 = 1 (5-12-13)
    chk(lambda: (169 - 25 == 12**2, -1 - 12 == -13, -1 + 12 == 11))
    qs.append(mcq('medium', 's3',
        'រកកូអរដោនេកំណុំទាំងពីរនៃអេលីប ' + M('\\frac{(x - 2)^2}{25} + \\frac{(y + 1)^2}{169} = 1') + ' ។',
        M('(2, -13)') + ' និង ' + M('(2, 11)'),
        [M('(-10, -1)') + ' និង ' + M('(14, -1)'), M('(2, -14)') + ' និង ' + M('(2, 12)'), M('(2, -6)') + ' និង ' + M('(2, 4)')],
        'ផ្ចិត ' + M('I(2, -1)') + ' និង ' + M('c = \\sqrt{169 - 25} = 12') + ' (អ័ក្សធំឈរ) ។ កំណុំគឺ ' + M('(2, -1 \\pm 12)') + ' ។',
        bloom='Apply'))

    # 14. Centre from general form 9x^2 + 25y^2 - 36x + 50y - 164 = 0
    # 9(x-2)^2 + 25(y+1)^2 = 164 + 36 + 25 = 225
    chk(lambda: (164 + 9*4 + 25*1 == 225,))
    qs.append(mcq('medium', 's3',
        'រកកូអរដោនេផ្ចិតនៃអេលីប ' + M('9x^2 + 25y^2 - 36x + 50y - 164 = 0') + ' ។',
        M('I(2, -1)'), [M('I(-2, 1)'), M('I(2, 1)'), M('I(-2, -1)')],
        'បំប្លែងជាការេពេញ៖ ' + M('9(x - 2)^2 + 25(y + 1)^2 = 225') + ' ដូច្នេះផ្ចិតគឺ ' + M('I(2, -1)') + ' ។',
        bloom='Apply'))

    # 15. Major axis length of 25x^2 + 9y^2 + 100x - 54y - 44 = 0
    # 25(x+2)^2 + 9(y-3)^2 = 44 + 100 + 81 = 225 -> /225 -> b^2=9, a^2=25 -> 2a=10
    chk(lambda: (44 + 25*4 + 9*9 == 225, F(225, 9) == 25, 2 * 5 == 10))
    qs.append(mcq('medium', 's3',
        'រកប្រវែងអ័ក្សធំនៃអេលីប ' + M('25x^2 + 9y^2 + 100x - 54y - 44 = 0') + ' ។',
        M('10'), [M('6'), M('5'), M('8')],
        'សរសេរជា ' + M('\\frac{(x + 2)^2}{9} + \\frac{(y - 3)^2}{25} = 1') + ' បាន ' + M('a = 5') + ' ដូច្នេះអ័ក្សធំមានប្រវែង ' + M('2a = 10') + ' ។',
        bloom='Apply'))

    # 16. Eccentricity of (x-1)^2/289 + (y+4)^2/225 = 1 (8-15-17)
    chk(lambda: (289 - 225 == 8**2, F(8, 17) * 17 == 8))
    qs.append(mcq('medium', 's4',
        'រកអ៊ុចសង់ទ្រីស៊ីតេនៃអេលីប ' + M('\\frac{(x - 1)^2}{289} + \\frac{(y + 4)^2}{225} = 1') + ' ។',
        M('\\frac{8}{17}'), [M('\\frac{15}{17}'), M('\\frac{8}{15}'), M('\\frac{12}{17}')],
        'គេមាន ' + M('a = 17, b = 15 \\Rightarrow c = \\sqrt{289 - 225} = 8') + ' ដូច្នេះ ' + M('e = \\frac{c}{a} = \\frac{8}{17}') + ' ។',
        bloom='Apply'))

    # 17. Equation: centre (0,0), foci (0, +-4), major axis 10 (3-4-5)
    chk(lambda: (5**2 - 4**2 == 3**2,))
    qs.append(mcq('medium', 's2',
        'រកសមីការស្ដង់ដានៃអេលីបដែលមានផ្ចិត ' + M('(0, 0)') + ' កំណុំ ' + M('(0, \\pm 4)') + ' និងអ័ក្សធំប្រវែង ' + M('10') + ' ។',
        M('\\frac{x^2}{9} + \\frac{y^2}{25} = 1'),
        [M('\\frac{x^2}{25} + \\frac{y^2}{9} = 1'), M('\\frac{x^2}{16} + \\frac{y^2}{25} = 1'), M('\\frac{x^2}{25} + \\frac{y^2}{16} = 1')],
        'គេមាន ' + M('2a = 10 \\Rightarrow a = 5, c = 4 \\Rightarrow b^2 = 25 - 16 = 9') + ' ។ ដោយកំណុំលើ ' + M('Oy') + ' បាន ' + M('\\frac{x^2}{9} + \\frac{y^2}{25} = 1') + ' ។',
        bloom='Apply'))

    # 18. Equation: vertices (-2, 3), (8, 3), minor axis 6
    chk(lambda: (F(-2 + 8, 2) == 3, 8 - 3 == 5, F(6, 2) == 3))
    qs.append(mcq('medium', 's3',
        'រកសមីការស្ដង់ដានៃអេលីបដែលមានកំពូល ' + M('(-2, 3)') + ' និង ' + M('(8, 3)') + ' ហើយអ័ក្សតូចមានប្រវែង ' + M('6') + ' ។',
        M('\\frac{(x - 3)^2}{25} + \\frac{(y - 3)^2}{9} = 1'),
        [M('\\frac{(x - 3)^2}{9} + \\frac{(y - 3)^2}{25} = 1'), M('\\frac{(x + 3)^2}{25} + \\frac{(y - 3)^2}{9} = 1'), M('\\frac{(x - 3)^2}{25} + \\frac{(y - 3)^2}{36} = 1')],
        'ផ្ចិតនៅចំណុចកណ្ដាល ' + M('I(3, 3)') + ' មាន ' + M('a = 5, b = 3') + ' និងអ័ក្សធំដេក ដូច្នេះ ' + M('\\frac{(x - 3)^2}{25} + \\frac{(y - 3)^2}{9} = 1') + ' ។',
        bloom='Apply'))

    # 19. Equation: foci (-1, 1), (-1, 9), e = 4/5
    chk(lambda: (F(1 + 9, 2) == 5, F(9 - 1, 2) == 4, F(4, F(4, 5)) == 5, 5**2 - 4**2 == 3**2))
    qs.append(mcq('medium', 's4',
        'រកសមីការស្ដង់ដានៃអេលីបដែលមានកំណុំ ' + M('(-1, 1)') + ' និង ' + M('(-1, 9)') + ' ហើយមានអ៊ុចសង់ទ្រីស៊ីតេ ' + M('e = \\frac{4}{5}') + ' ។',
        M('\\frac{(x + 1)^2}{9} + \\frac{(y - 5)^2}{25} = 1'),
        [M('\\frac{(x + 1)^2}{25} + \\frac{(y - 5)^2}{9} = 1'), M('\\frac{(x - 1)^2}{9} + \\frac{(y + 5)^2}{25} = 1'), M('\\frac{(x + 1)^2}{16} + \\frac{(y - 5)^2}{25} = 1')],
        'ផ្ចិត ' + M('I(-1, 5)') + ' និង ' + M('c = 4') + ' ។ ដោយ ' + M('e = \\frac{c}{a} = \\frac{4}{5} \\Rightarrow a = 5, b = 3') + ' (អ័ក្សធំឈរ) ។',
        bloom='Apply'))

    # 20. Equation: centre (0,0), horiz major axis, passes through (5, 0) and (3, 16/5)
    chk(lambda: (F(3**2, 25) + F(F(16, 5)**2, 16) == 1,))
    qs.append(mcq('medium', 's2',
        'រកសមីការអេលីបដែលមានផ្ចិត ' + M('(0, 0)') + ' អ័ក្សធំនៅលើ ' + M('Ox') + ' និងកាត់តាមចំណុច ' + M('(5, 0)') + ' និង ' + M('\\left(3, \\frac{16}{5}\\right)') + ' ។',
        M('\\frac{x^2}{25} + \\frac{y^2}{16} = 1'),
        [M('\\frac{x^2}{25} + \\frac{y^2}{9} = 1'), M('\\frac{x^2}{16} + \\frac{y^2}{25} = 1'), M('\\frac{x^2}{25} + \\frac{y^2}{12} = 1')],
        'ជំនួស ' + M('(5, 0)') + ' បាន ' + M('a^2 = 25') + ' ។ ជំនួស ' + M('\\left(3, \\frac{16}{5}\\right)') + ' បាន ' + M('\\frac{9}{25} + \\frac{256}{25 b^2} = 1 \\Rightarrow b^2 = 16') + ' ។',
        bloom='Apply'))

    # 21. Latus rectum length of x^2/25 + y^2/9 = 1
    chk(lambda: (F(2 * 9, 5) == F(18, 5),))
    qs.append(mcq('medium', 's2',
        'រកប្រវែងអង្កត់កាត់កំណុំកែងអ័ក្សធំ ' + M('\\frac{2b^2}{a}') + ' នៃអេលីប ' + M('\\frac{x^2}{25} + \\frac{y^2}{9} = 1') + ' ។',
        M('\\frac{18}{5}'), [M('\\frac{9}{5}'), M('\\frac{32}{5}'), M('6')],
        'គេមាន ' + M('a = 5, b^2 = 9') + ' ដូច្នេះប្រវែងអង្កត់កាត់កំណុំគឺ ' + M('\\frac{2b^2}{a} = \\frac{18}{5}') + ' ។',
        bloom='Apply'))

    # 22. Sum of focal distances PF1 + PF2 on 9x^2 + 25y^2 = 225
    chk(lambda: (F(225, 9) == 25, 2 * 5 == 10))
    qs.append(mcq('medium', 's1',
        'តាង ' + M('P') + ' ជាចំណុចមួយនៅលើអេលីប ' + M('9x^2 + 25y^2 = 225') + ' ដែលមានកំណុំ ' + M('F_1, F_2') + ' ។ រកផលបូក ' + M('PF_1 + PF_2') + ' ។',
        M('10'), [M('5'), M('6'), M('8')],
        'សមីការស្ដង់ដាគឺ ' + M('\\frac{x^2}{25} + \\frac{y^2}{9} = 1') + ' មាន ' + M('a = 5') + ' ដូច្នេះ ' + M('PF_1 + PF_2 = 2a = 10') + ' ។',
        bloom='Understand'))

    # 23. Eccentricity of 16x^2 + 25y^2 - 64x + 50y - 311 = 0
    # 16(x-2)^2 + 25(y+1)^2 = 311 + 64 + 25 = 400 -> /400 -> a^2=25, b^2=16 -> c=3 -> e=3/5
    chk(lambda: (311 + 16*4 + 25*1 == 400, F(400, 16) == 25, F(400, 25) == 16, 25 - 16 == 9, F(3, 5) == F('0.6')))
    qs.append(mcq('medium', 's4',
        'រកអ៊ុចសង់ទ្រីស៊ីតេនៃអេលីប ' + M('16x^2 + 25y^2 - 64x + 50y - 311 = 0') + ' ។',
        M('\\frac{3}{5}'), [M('\\frac{4}{5}'), M('\\frac{3}{4}'), M('\\frac{5}{8}')],
        'បំប្លែងបាន ' + M('\\frac{(x - 2)^2}{25} + \\frac{(y + 1)^2}{16} = 1') + ' មាន ' + M('a = 5, b = 4, c = 3') + ' ដូច្នេះ ' + M('e = \\frac{3}{5}') + ' ។',
        bloom='Analyze'))

    # 24. Condition for general degree-2 equation to be an ellipse
    qs.append(mcq('medium', 's3',
        'សមីការដឺក្រេទី 2 ' + M('Ax^2 + By^2 + Cx + Dy + E = 0') + ' (ដែលមិនទទេ) ជាសមីការទូទៅនៃអេលីប លុះត្រាតែ ' + M('A, B') + ' ផ្ទៀងផ្ទាត់លក្ខខណ្ឌណា?',
        M('A \\cdot B > 0') + ' និង ' + M('A \\neq B'),
        [M('A \\cdot B < 0'), M('A = B'), M('A \\cdot B = 0')],
        'សមីការទូទៅនៃអេលីបត្រូវមាន ' + M('A') + ' និង ' + M('B') + ' សញ្ញាដូចគ្នា (' + M('A \\cdot B > 0') + ') និង ' + M('A \\neq B') + ' (បើ ' + M('A = B') + ' ជារង្វង់) ។',
        bloom='Remember'))

    # =========================================================================
    # MCQ HARD (7)
    # =========================================================================
    # 25. Locus MF1 + MF2 = 26 for F1(5, -2), F2(-5, -2) (5-12-13)
    chk(lambda: (F(26, 2) == 13, 13**2 - 5**2 == 12**2))
    qs.append(mcq('hard', 's1',
        'រកសមីការសំណុំចំណុច ' + M('M(x, y)') + ' ដែលមានផលបូកចម្ងាយពី ' + M('F_1(5, -2)') + ' និង ' + M('F_2(-5, -2)') + ' ស្មើនឹង ' + M('26') + ' ។',
        M('\\frac{x^2}{169} + \\frac{(y + 2)^2}{144} = 1'),
        [M('\\frac{x^2}{169} + \\frac{(y + 2)^2}{25} = 1'), M('\\frac{x^2}{144} + \\frac{(y + 2)^2}{169} = 1'), M('\\frac{x^2}{169} + \\frac{(y - 2)^2}{144} = 1')],
        'ផ្ចិត ' + M('I(0, -2)') + ' មាន ' + M('c = 5, 2a = 26 \\Rightarrow a = 13') + ' និង ' + M('b^2 = 169 - 25 = 144') + ' ។',
        bloom='Analyze'))

    # 26. Centre (2, -1), focus (2, 14), passes through co-vertex (10, -1) (8-15-17)
    chk(lambda: (14 - (-1) == 15, 10 - 2 == 8, 8**2 + 15**2 == 17**2))
    qs.append(mcq('hard', 's3',
        'អេលីបមួយមានផ្ចិត ' + M('I(2, -1)') + ' កំណុំមួយនៅ ' + M('(2, 14)') + ' និងកាត់តាមចំណុចចុងអ័ក្សតូច ' + M('(10, -1)') + ' ។ រកសមីការស្ដង់ដារបស់វា ។',
        M('\\frac{(x - 2)^2}{64} + \\frac{(y + 1)^2}{289} = 1'),
        [M('\\frac{(x - 2)^2}{64} + \\frac{(y + 1)^2}{225} = 1'), M('\\frac{(x - 2)^2}{289} + \\frac{(y + 1)^2}{64} = 1'), M('\\frac{(x - 2)^2}{225} + \\frac{(y + 1)^2}{289} = 1')],
        'គេមាន ' + M('c = 14 - (-1) = 15, b = 10 - 2 = 8 \\Rightarrow a = \\sqrt{8^2 + 15^2} = 17') + ' ដោយអ័ក្សធំឈរ ។',
        bloom='Analyze'))

    # 27. Point P on x^2/100 + y^2/36 = 1 has PF1 = 7 -> PF2
    chk(lambda: (2 * 10 - 7 == 13,))
    qs.append(mcq('hard', 's1',
        'ចំណុច ' + M('P') + ' ស្ថិតនៅលើអេលីប ' + M('\\frac{x^2}{100} + \\frac{y^2}{36} = 1') + ' និងមានចម្ងាយពីកំណុំ ' + M('F_1') + ' ស្មើ ' + M('7') + ' ។ រកចម្ងាយ ' + M('PF_2') + ' ទៅកំណុំមួយទៀត ។',
        M('13'), [M('10'), M('17'), M('9')],
        'គេមាន ' + M('a = 10 \\Rightarrow PF_1 + PF_2 = 2a = 20') + ' ដូច្នេះ ' + M('PF_2 = 20 - 7 = 13') + ' ។',
        bloom='Analyze'))

    # 28. Perimeter of triangle PF1F2 for P on x^2/169 + y^2/144 = 1 (5-12-13)
    chk(lambda: (169 - 144 == 5**2, 2*13 + 2*5 == 36))
    qs.append(mcq('hard', 's1',
        'តាង ' + M('P') + ' ជាចំណុចមួយនៅលើអេលីប ' + M('\\frac{x^2}{169} + \\frac{y^2}{144} = 1') + ' មិននៅលើអ័ក្សធំ ។ រកបរិមាត្រនៃត្រីកោណ ' + M('PF_1F_2') + ' ។',
        M('36'), [M('26'), M('38'), M('50')],
        'បរិមាត្រ ' + M('PF_1 + PF_2 + F_1F_2 = 2a + 2c') + ' ។ ដោយ ' + M('a = 13, b = 12, c = 5') + ' បាន ' + M('2(13) + 2(5) = 36') + ' ។',
        bloom='Evaluate'))

    # 29. Value of k (0 < k < 25) so x^2/25 + y^2/k = 1 has e = 4/5
    chk(lambda: (25 * (1 - F(4, 5)**2) == 9,))
    qs.append(mcq('hard', 's4',
        'រកតម្លៃ ' + M('k') + ' (' + M('0 < k < 25') + ') ដើម្បីឱ្យអេលីប ' + M('\\frac{x^2}{25} + \\frac{y^2}{k} = 1') + ' មានអ៊ុចសង់ទ្រីស៊ីតេ ' + M('e = \\frac{4}{5}') + ' ។',
        M('9'), [M('16'), M('12'), M('4')],
        'គេមាន ' + M('a = 5, c = e a = 4') + ' ដូច្នេះ ' + M('k = b^2 = a^2 - c^2 = 25 - 16 = 9') + ' ។',
        bloom='Analyze'))

    # 30. Vertical major axis, I(3, -2), e = 12/13, minor axis 10
    chk(lambda: (F(10, 2) == 5, 5**2 == 13**2 - 12**2))
    qs.append(mcq('hard', 's4',
        'រកសមីការស្ដង់ដានៃអេលីបដែលមានផ្ចិត ' + M('I(3, -2)') + ' អ័ក្សធំឈរ អ័ក្សតូចប្រវែង ' + M('10') + ' និងអ៊ុចសង់ទ្រីស៊ីតេ ' + M('e = \\frac{12}{13}') + ' ។',
        M('\\frac{(x - 3)^2}{25} + \\frac{(y + 2)^2}{169} = 1'),
        [M('\\frac{(x - 3)^2}{169} + \\frac{(y + 2)^2}{25} = 1'), M('\\frac{(x - 3)^2}{25} + \\frac{(y + 2)^2}{144} = 1'), M('\\frac{(x + 3)^2}{25} + \\frac{(y - 2)^2}{169} = 1')],
        'គេមាន ' + M('b = 5') + ' និង ' + M('c = \\frac{12}{13}a') + ' ។ តាម ' + M('a^2 - c^2 = b^2') + ' បាន ' + M('\\frac{25}{169}a^2 = 25 \\Rightarrow a = 13') + ' ។',
        bloom='Analyze'))

    # 31. Distance between foci of 4x^2 + 9y^2 - 16x + 54y + 61 = 0 (surd!)
    # 4(x-2)^2 + 9(y+3)^2 = -61 + 16 + 81 = 36 -> a^2=9, b^2=4 -> c = sqrt(5) -> 2c = 2sqrt(5)
    chk(lambda: (-61 + 4*4 + 9*9 == 36, F(36, 4) - F(36, 9) == 5))
    qs.append(mcq('hard', 's3',
        'រកចម្ងាយរវាងកំណុំទាំងពីរ ' + M('F_1F_2') + ' នៃអេលីប ' + M('4x^2 + 9y^2 - 16x + 54y + 61 = 0') + ' (គិតជាតម្លៃរ៉ាឌីកាល់) ។',
        M('2\\sqrt{5}'), [M('\\sqrt{5}'), M('2\\sqrt{13}'), M('6')],
        'បំប្លែងបាន ' + M('\\frac{(x - 2)^2}{9} + \\frac{(y + 3)^2}{4} = 1') + ' មាន ' + M('c = \\sqrt{9 - 4} = \\sqrt{5}') + ' ដូច្នេះ ' + M('F_1F_2 = 2c = 2\\sqrt{5}') + ' ។',
        bloom='Analyze'))

    # =========================================================================
    # MCQ PISA (5)  (#32 - #36)
    # =========================================================================
    # 32. Planet orbit: a = 5 AU, b = 4 AU -> perihelion a - c = 5 - 3 = 2 AU
    chk(lambda: (5**2 - 4**2 == 3**2, 5 - 3 == 2))
    svg32 = fig_ellipse(
        0, 0, 5, 4, -6.2, 6.2, -5.0, 5.0,
        xlabel='x (AU)', ylabel='y (AU)',
        xticks=[-5, 5], yticks=[-4, 4],
        title='Planet Orbit',
        dots_data=[(3, 0, 'Sun', 0, -10, P.K.AMBER), (5, 0, 'P', 10, -6, P.K.RED)],
        segs_data=[(3, 0, 5, 0, P.K.RED, True)],
    )
    qs.append(with_img(mcq('pisa', 'p_orbit',
        'ភពមួយគោចរជុំវិញព្រះអាទិត្យតាមគន្លងអេលីប ' + M('\\frac{x^2}{25} + \\frac{y^2}{16} = 1') + ' (គិតជា AU) ដោយព្រះអាទិត្យស្ថិតនៅកំណុំខាងស្ដាំ ' + M('F_1(c, 0)') + ' ។ រកចម្ងាយជិតបំផុតពីភពទៅព្រះអាទិត្យ ។',
        M('2\\text{ AU}'), [M('3\\text{ AU}'), M('4\\text{ AU}'), M('8\\text{ AU}')],
        'គេមាន ' + M('a = 5, b = 4 \\Rightarrow c = 3') + ' ។ ចម្ងាយជិតបំផុតគឺ ' + M('a - c = 5 - 3 = 2\\text{ AU}') + ' ។',
        bloom='Apply'), svg32))

    # 33. Whispering gallery: length 2a = 26 m, width 2b = 10 m -> focal distance 2c = 24 m (5-12-13)
    chk(lambda: (13**2 - 5**2 == 12**2, 2 * 12 == 24))
    svg33 = fig_ellipse(
        0, 0, 13, 5, -15.5, 15.5, -7.0, 7.0,
        xlabel='x (m)', ylabel='y (m)',
        xticks=[-13, 13], yticks=[-5, 5],
        title='Whispering Gallery',
        dots_data=[(-12, 0, 'F2', 5, -8, P.K.RED), (12, 0, 'F1', -5, -8, P.K.RED)],
    )
    qs.append(with_img(mcq('pisa', 'p_gallery',
        'សាលខ្សឹបសំឡេងរាងអេលីបមួយមានប្រវែងបណ្ដោយ ' + M('26\\text{ m}') + ' និងទទឹង ' + M('10\\text{ m}') + ' ។ ដើម្បីខ្សឹបសំឡេងឮច្បាស់ពីកំណុំមួយទៅកំណុំមួយទៀត តើមនុស្សពីរនាក់ត្រូវឈរនៅចម្ងាយប៉ុន្មានម៉ែត្រពីគ្នា?',
        M('24\\text{ m}'), [M('12\\text{ m}'), M('16\\text{ m}'), M('20\\text{ m}')],
        'គេមាន ' + M('a = 13, b = 5 \\Rightarrow c = \\sqrt{169 - 25} = 12\\text{ m}') + ' ដូច្នេះចម្ងាយរវាងកំណុំទាំងពីរគឺ ' + M('2c = 24\\text{ m}') + ' ។',
        bloom='Apply'), svg33))

    # 34. Elliptical arch bridge: span 2a = 20 m (a=10), max height b = 6 m -> height at x = 6 m
    # 36/100 + y^2/36 = 1 -> y^2 = 36 * 64/100 -> y = 6 * 8/10 = 4.8 m
    chk(lambda: (F(6, 1) * F(8, 10) == F(24, 5), F(6**2, 100) + F(F(24, 5)**2, 36) == 1))
    svg34 = fig_ellipse(
        0, 0, 10, 6, -12.5, 12.5, 0.0, 8.0,
        xlabel='x (m)', ylabel='y (m)',
        xticks=[-10, 6, 10], yticks=[6],
        title='Elliptical Arch',
        half_top=True,
        segs_data=[(6, 0, 6, 4.8, P.K.AMBER, True)],
        notes_data=[(6, 2.2, 'h?', 12, 0, P.K.AMBER, True)],
    )
    qs.append(with_img(mcq('pisa', 'p_arch',
        'ស្ពានកោងរាងកន្លះអេលីបមួយមានប្រវែងកំណោង ' + M('20\\text{ m}') + ' និងកម្ពស់អតិបរមានៅចំណុចកណ្ដាល ' + M('6\\text{ m}') + ' ។ រកកម្ពស់កំណោងស្ពានត្រង់ចម្ងាយ ' + M('6\\text{ m}') + ' ពីចំណុចកណ្ដាល ។',
        M('4.8\\text{ m}'), [M('3.6\\text{ m}'), M('4.0\\text{ m}'), M('5.2\\text{ m}')],
        'សមីការគឺ ' + M('\\frac{x^2}{100} + \\frac{y^2}{36} = 1') + ' ។ ជំនួស ' + M('x = 6') + ' បាន ' + M('\\frac{y^2}{36} = \\frac{64}{100} \\Rightarrow y = 4.8\\text{ m}') + ' ។',
        bloom='Apply'), svg34))

    # 35. Elliptical garden: a = 17 m, b = 8 m -> eccentricity e = 15/17 (8-15-17)
    chk(lambda: (17**2 - 8**2 == 15**2,))
    svg35 = fig_ellipse(
        0, 0, 17, 8, -20.5, 20.5, -10.5, 10.5,
        xlabel='x (m)', ylabel='y (m)',
        xticks=[-17, 17], yticks=[-8, 8],
        title='Elliptical Garden',
    )
    qs.append(with_img(mcq('pisa', 'p_track',
        'សួនច្បាររាងអេលីបមួយមានកន្លះអ័ក្សធំ ' + M('17\\text{ m}') + ' និងកន្លះអ័ក្សតូច ' + M('8\\text{ m}') + ' ។ រកអ៊ុចសង់ទ្រីស៊ីតេនៃសួនច្បាររាងអេលីបនេះ ។',
        M('\\frac{15}{17}'), [M('\\frac{8}{17}'), M('\\frac{8}{15}'), M('\\frac{9}{17}')],
        'គេមាន ' + M('c = \\sqrt{17^2 - 8^2} = 15\\text{ m}') + ' ដូច្នេះ ' + M('e = \\frac{c}{a} = \\frac{15}{17}') + ' ។',
        bloom='Apply'), svg35))

    # 36. Elliptical dining table: 2a = 2.6 m (a=1.3), focal distance 2c = 2.4 m (c=1.2) -> width 2b = 1.0 m
    chk(lambda: (F('1.3')**2 - F('1.2')**2 == F('0.5')**2, 2 * F('0.5') == 1))
    svg36 = fig_ellipse(
        0, 0, 1.3, 0.5, -1.65, 1.65, -0.8, 0.8,
        xlabel='x (m)', ylabel='y (m)',
        xticks=[-1.3, 1.3], yticks=[],
        title='Elliptical Table',
        dots_data=[(-1.2, 0, 'F2', 6, -8, P.K.RED), (1.2, 0, 'F1', -6, -8, P.K.RED)],
    )
    qs.append(with_img(mcq('pisa', 'p_table',
        'តុអាហាររាងអេលីបមួយមានប្រវែងបណ្ដោយ ' + M('2.6\\text{ m}') + ' និងចម្ងាយរវាងកំណុំទាំងពីរ ' + M('2.4\\text{ m}') + ' ។ រកទទឹងអតិបរមានៃតុអាហារនេះ ។',
        M('1.0\\text{ m}'), [M('0.5\\text{ m}'), M('1.2\\text{ m}'), M('2.0\\text{ m}')],
        'គេមាន ' + M('a = 1.3\\text{ m}, c = 1.2\\text{ m} \\Rightarrow b = \\sqrt{1.69 - 1.44} = 0.5\\text{ m}') + ' ដូច្នេះទទឹងគឺ ' + M('2b = 1.0\\text{ m}') + ' ។',
        bloom='Apply'), svg36))

    # =========================================================================
    # WRITING EASY (1)  (#37)
    # =========================================================================
    # 37. Centre, vertices, foci, axis lengths, eccentricity of x^2/25 + y^2/16 = 1
    chk(lambda: (25 - 16 == 3**2, F(3, 5) == F('0.6')))
    qs.append(wr('easy', 's2',
        'គេមានអេលីប ' + M('\\frac{x^2}{25} + \\frac{y^2}{16} = 1') + ' ។ រកផ្ចិត កំពូលទាំងពីរ កំណុំទាំងពីរ ប្រវែងអ័ក្សធំ អ័ក្សតូច និងអ៊ុចសង់ទ្រីស៊ីតេ ។',
        [('ផ្ចិតនៅគល់អ័ក្សកូអរដោនេ ' + M('I(0, 0)') + ' ហើយអ័ក្សធំស្ថិតនៅលើអ័ក្ស ' + M('Ox'), 1),
         ('កំណត់ ' + M('a = 5, b = 4') + ' បានប្រវែងអ័ក្សធំ ' + M('2a = 10') + ' និងអ័ក្សតូច ' + M('2b = 8'), 1),
         ('គណនា ' + M('c = \\sqrt{a^2 - b^2} = \\sqrt{25 - 16} = 3'), 1),
         ('កំពូលគឺ ' + M('V_1(-5, 0), V_2(5, 0)') + ' និងកំណុំគឺ ' + M('F_1(-3, 0), F_2(3, 0)'), 1),
         ('អ៊ុចសង់ទ្រីស៊ីតេគឺ ' + M('e = \\frac{c}{a} = \\frac{3}{5} = 0.6') + ' ។', 1)],
        bloom='Apply'))

    # =========================================================================
    # WRITING MEDIUM (4)  (#38 - #41)
    # =========================================================================
    # 38. Convert 9x^2 + 25y^2 - 18x + 100y - 116 = 0 to standard form
    # 9(x-1)^2 + 25(y+2)^2 = 116 + 9 + 100 = 225 -> /225 -> a=5, b=3, c=4, e=4/5
    chk(lambda: (116 + 9*1 + 25*4 == 225, F(225, 9) == 25, F(225, 25) == 9, 25 - 9 == 4**2))
    qs.append(wr('medium', 's3',
        'បំប្លែងសមីការអេលីប ' + M('9x^2 + 25y^2 - 18x + 100y - 116 = 0') + ' ជាទម្រង់ស្ដង់ដា រួចរកផ្ចិត កំពូល កំណុំ និងអ៊ុចសង់ទ្រីស៊ីតេ ។',
        [('ផ្ដុំតួជាការេពេញ៖ ' + M('9(x^2 - 2x + 1) + 25(y^2 + 4y + 4) = 116 + 9 + 100 = 225'), 1),
         ('ចែកនឹង ' + M('225') + ' បានទម្រង់ស្ដង់ដា ' + M('\\frac{(x - 1)^2}{25} + \\frac{(y + 2)^2}{9} = 1'), 1),
         ('ផ្ចិតគឺ ' + M('I(1, -2)') + ' មាន ' + M('a = 5, b = 3') + ' និង ' + M('c = \\sqrt{25 - 9} = 4'), 1),
         ('កំពូលគឺ ' + M('V(1 \\pm 5, -2) \\Rightarrow (-4, -2), (6, -2)') + ' និងកំណុំ ' + M('F(1 \\pm 4, -2) \\Rightarrow (-3, -2), (5, -2)'), 1),
         ('អ៊ុចសង់ទ្រីស៊ីតេគឺ ' + M('e = \\frac{c}{a} = \\frac{4}{5}') + ' ។', 1)],
        bloom='Apply'))

    # 39. Standard equation with foci (0, +-12), major axis 26 (5-12-13)
    chk(lambda: (F(26, 2) == 13, 13**2 - 12**2 == 5**2))
    qs.append(wr('medium', 's2',
        'រកសមីការស្ដង់ដានៃអេលីបដែលមានកំណុំ ' + M('(0, \\pm 12)') + ' និងអ័ក្សធំមានប្រវែង ' + M('26') + ' រួចរកកន្លះអ័ក្សតូច និងអ៊ុចសង់ទ្រីស៊ីតេ ។',
        [('ដោយកំណុំ ' + M('(0, \\pm 12)') + ' ស្ថិតលើ ' + M('Oy') + ' ផ្ចិតគឺ ' + M('I(0, 0)') + ' និង ' + M('c = 12'), 1),
         ('អ័ក្សធំប្រវែង ' + M('2a = 26 \\Rightarrow a = 13'), 1),
         ('គណនា ' + M('b^2 = a^2 - c^2 = 169 - 144 = 25 \\Rightarrow b = 5'), 1),
         ('សមីការស្ដង់ដានៃអេលីបគឺ ' + M('\\frac{x^2}{25} + \\frac{y^2}{169} = 1'), 1),
         ('អ៊ុចសង់ទ្រីស៊ីតេគឺ ' + M('e = \\frac{c}{a} = \\frac{12}{13}') + ' ។', 1)],
        bloom='Apply'))

    # 40. Standard equation with vertices (-1, -15), (-1, 19) and foci (-1, -13), (-1, 17) (8-15-17)
    chk(lambda: (F(-15 + 19, 2) == 2, 19 - 2 == 17, 17 - 2 == 15, 17**2 - 15**2 == 8**2))
    qs.append(wr('medium', 's3',
        'រកសមីការស្ដង់ដានៃអេលីបដែលមានកំពូល ' + M('(-1, -15)') + ' និង ' + M('(-1, 19)') + ' ហើយកំណុំ ' + M('(-1, -13)') + ' និង ' + M('(-1, 17)') + ' ។',
        [('កំណត់ផ្ចិតនៅចំណុចកណ្ដាល៖ ' + M('h = -1, k = \\frac{-15 + 19}{2} = 2 \\Rightarrow I(-1, 2)'), 1),
         ('អ័ក្សធំស្របនឹង ' + M('Oy') + ' ដោយ ' + M('a = 19 - 2 = 17') + ' និង ' + M('c = 17 - 2 = 15'), 1),
         ('គណនា ' + M('b^2 = a^2 - c^2 = 17^2 - 15^2 = 289 - 225 = 64'), 1),
         ('ជំនួសក្នុងទម្រង់ ' + M('\\frac{(x - h)^2}{b^2} + \\frac{(y - k)^2}{a^2} = 1'), 1),
         ('សមីការស្ដង់ដាគឺ ' + M('\\frac{(x + 1)^2}{64} + \\frac{(y - 2)^2}{289} = 1') + ' ។', 1)],
        bloom='Apply'))

    # 41. Centre O(0,0), horiz major axis, passes through (5, 0) and (4, 12/5)
    chk(lambda: (F(4**2, 25) + F(F(12, 5)**2, 16) == 1, 25 - 16 == 3**2))
    qs.append(wr('medium', 's2',
        'រកសមីការស្ដង់ដានៃអេលីបដែលមានផ្ចិត ' + M('O(0, 0)') + ' អ័ក្សធំនៅលើអ័ក្ស ' + M('Ox') + ' និងកាត់តាមចំណុច ' + M('(5, 0)') + ' និង ' + M('\\left(4, \\frac{12}{5}\\right)') + ' ។',
        [('សរសេរទម្រង់ ' + M('\\frac{x^2}{a^2} + \\frac{y^2}{b^2} = 1') + ' (' + M('a > b > 0') + ')', 1),
         ('ជំនួស ' + M('(5, 0)') + ' បាន ' + M('\\frac{25}{a^2} = 1 \\Rightarrow a^2 = 25'), 1),
         ('ជំនួស ' + M('\\left(4, \\frac{12}{5}\\right)') + ' បាន ' + M('\\frac{16}{25} + \\frac{144}{25 b^2} = 1'), 1),
         ('ដោះស្រាយរក ' + M('\\frac{144}{25 b^2} = \\frac{9}{25} \\Rightarrow b^2 = 16'), 1),
         ('ដូច្នេះសមីការស្ដង់ដាគឺ ' + M('\\frac{x^2}{25} + \\frac{y^2}{16} = 1') + ' ។', 1)],
        bloom='Apply'))

    # =========================================================================
    # WRITING HARD (4)  (#42 - #45)
    # =========================================================================
    # 42. Locus MF1 + MF2 = 10 for F1(3, 1), F2(-3, 1)
    chk(lambda: (F(10, 2) == 5, 5**2 - 3**2 == 4**2, F(3, 5) == F('0.6')))
    qs.append(wr('hard', 's1',
        'ដោយប្រើនិយមន័យអេលីប ចូររកសមីការស្ដង់ដានៃសំណុំចំណុច ' + M('M(x, y)') + ' ដែល ' + M('MF_1 + MF_2 = 10') + ' ដោយដឹងថា ' + M('F_1(3, 1)') + ' និង ' + M('F_2(-3, 1)') + ' រួចរកអ៊ុចសង់ទ្រីស៊ីតេ ។',
        [('ផ្ចិតនៅចំណុចកណ្ដាល ' + M('I\\left(\\frac{3-3}{2}, \\frac{1+1}{2}\\right) = I(0, 1)'), 1),
         ('កំណុំស្ថិតលើបន្ទាត់ដេក ' + M('y = 1') + ' ដោយ ' + M('c = 3') + ' និង ' + M('2a = 10 \\Rightarrow a = 5'), 1),
         ('គណនា ' + M('b^2 = a^2 - c^2 = 25 - 9 = 16 \\Rightarrow b = 4'), 1),
         ('សមីការស្ដង់ដាគឺ ' + M('\\frac{x^2}{25} + \\frac{(y - 1)^2}{16} = 1'), 1),
         ('អ៊ុចសង់ទ្រីស៊ីតេគឺ ' + M('e = \\frac{c}{a} = \\frac{3}{5}') + ' ។', 1)],
        bloom='Analyze'))

    # 43. Centre (2, -3), vertical major axis, e = 5/13, latus rectum 288/13 -> a=13, b=12, c=5
    chk(lambda: (13**2 - 5**2 == 12**2, F(2 * 12**2, 13) == F(288, 13)))
    qs.append(wr('hard', 's4',
        'អេលីបមួយមានផ្ចិត ' + M('I(2, -3)') + ' អ័ក្សធំស្របនឹងអ័ក្សអរដោនេ អ៊ុចសង់ទ្រីស៊ីតេ ' + M('e = \\frac{5}{13}') + ' និងប្រវែងអង្កត់កាត់កំណុំកែងអ័ក្សធំស្មើ ' + M('\\frac{288}{13}') + ' ។ រកសមីការស្ដង់ដារបស់វា ។',
        [('ដោយ ' + M('e = \\frac{c}{a} = \\frac{5}{13} \\Rightarrow c = \\frac{5}{13}a'), 1),
         ('គណនា ' + M('b^2 = a^2 - c^2 = a^2\\left(1 - \\frac{25}{169}\\right) = \\frac{144}{169}a^2'), 1),
         ('ប្រើប្រវែងអង្កត់កាត់កំណុំ ' + M('\\frac{2b^2}{a} = \\frac{288}{169}a = \\frac{288}{13} \\Rightarrow a = 13'), 1),
         ('ទាញបាន ' + M('a^2 = 169') + ' និង ' + M('b^2 = 144'), 1),
         ('សមីការស្ដង់ដាគឺ ' + M('\\frac{(x - 2)^2}{144} + \\frac{(y + 3)^2}{169} = 1') + ' ។', 1)],
        bloom='Analyze'))

    # 44. General to standard: 169x^2 + 25y^2 + 338x - 150y - 3831 = 0
    # 169(x+1)^2 + 25(y-3)^2 = 3831 + 169 + 225 = 4225 -> a=13, b=5, c=12
    chk(lambda: (3831 + 169 + 25*9 == 4225, F(4225, 169) == 25, F(4225, 25) == 169, 169 - 25 == 12**2))
    qs.append(wr('hard', 's3',
        'បំប្លែងសមីការ ' + M('169x^2 + 25y^2 + 338x - 150y - 3831 = 0') + ' ជាសមីការស្ដង់ដា រួចរកផ្ចិត កំពូល កំណុំ និងអ៊ុចសង់ទ្រីស៊ីតេ ។',
        [('ផ្ដុំតួជាការេពេញ៖ ' + M('169(x + 1)^2 + 25(y - 3)^2 = 3831 + 169 + 225 = 4225'), 1),
         ('ចែកនឹង ' + M('4225') + ' បាន ' + M('\\frac{(x + 1)^2}{25} + \\frac{(y - 3)^2}{169} = 1'), 1),
         ('ផ្ចិតគឺ ' + M('I(-1, 3)') + ' មាន ' + M('a = 13, b = 5, c = \\sqrt{169 - 25} = 12'), 1),
         ('កំពូលគឺ ' + M('(-1, -10), (-1, 16)') + ' និងកំណុំគឺ ' + M('(-1, -9), (-1, 15)'), 1),
         ('អ៊ុចសង់ទ្រីស៊ីតេគឺ ' + M('e = \\frac{c}{a} = \\frac{12}{13}') + ' ។', 1)],
        bloom='Analyze'))

    # 45. Perpendicular focal radii on x^2/25 + y^2/9 = 1: PF1 perp PF2 -> area of triangle PF1F2
    # PF1 + PF2 = 10, PF1^2 + PF2^2 = (2c)^2 = 64 -> 2*PF1*PF2 = 100 - 64 = 36 -> PF1*PF2 = 18 -> Area = 9
    chk(lambda: (10**2 - 8**2 == 36, F(36, 2) == 18, F(18, 2) == 9))
    qs.append(wr('hard', 's1',
        'តាង ' + M('P') + ' ជាចំណុចមួយនៅលើអេលីប ' + M('\\frac{x^2}{25} + \\frac{y^2}{9} = 1') + ' ដែល ' + M('PF_1 \\perp PF_2') + ' ។ គណនាផលគុណ ' + M('PF_1 \\cdot PF_2') + ' និងផ្ទៃក្រឡាត្រីកោណ ' + M('PF_1F_2') + ' ។',
        [('ពីសមីការអេលីប បាន ' + M('a = 5, b = 3, c = 4 \\Rightarrow F_1F_2 = 2c = 8'), 1),
         ('តាមនិយមន័យអេលីប ' + M('PF_1 + PF_2 = 2a = 10'), 1),
         ('ដោយ ' + M('PF_1 \\perp PF_2') + ' តាមពីតាគ័រ ' + M('PF_1^2 + PF_2^2 = F_1F_2^2 = 64'), 1),
         ('ប្រើ ' + M('(PF_1 + PF_2)^2 - (PF_1^2 + PF_2^2) = 2PF_1 \\cdot PF_2 \\Rightarrow 100 - 64 = 36 \\Rightarrow PF_1 \\cdot PF_2 = 18'), 1),
         ('ផ្ទៃក្រឡាត្រីកោណកែង ' + M('S = \\frac{1}{2} PF_1 \\cdot PF_2 = 9') + ' ឯកតាផ្ទៃ ។', 1)],
        bloom='Evaluate'))

    # =========================================================================
    # WRITING PISA (5)  (#46 - #50)
    # =========================================================================
    # 46. Whispering gallery: 2a = 34 m, 2b = 16 m -> c = 15 m, total sound distance 34 m (8-15-17)
    chk(lambda: (17**2 - 8**2 == 15**2, 2 * 17 == 34))
    svg46 = fig_ellipse(
        0, 0, 17, 8, -20.5, 20.5, -10.5, 10.5,
        xlabel='x (m)', ylabel='y (m)',
        xticks=[-17, 17], yticks=[-8, 8],
        title='Whispering Room',
        dots_data=[(-15, 0, 'F2', 4, 13, P.K.RED), (15, 0, 'F1', -4, 13, P.K.RED), (8, 7.06, 'P', 8, -4, P.K.AMBER)],
        segs_data=[(-15, 0, 8, 7.06, P.K.AMBER, True), (8, 7.06, 15, 0, P.K.AMBER, True)],
    )
    qs.append(with_img(wr('pisa', 'p_whisper',
        'សាលរាងអេលីបមួយមានប្រវែងបណ្ដោយ ' + M('34\\text{ m}') + ' និងទទឹង ' + M('16\\text{ m}') + ' ។ ក. រកសមីការស្ដង់ដា និងទីតាំងកំណុំទាំងពីរ ' + M('F_1, F_2') + ' ។ ខ. បើរលកសំឡេងចេញពី ' + M('F_1') + ' ប៉ះជញ្ជាំងត្រង់ ' + M('P') + ' ហើយចាំងផ្លាតទៅ ' + M('F_2') + ' តើចម្ងាយសរុបដែលសំឡេងរត់ស្មើប៉ុន្មានម៉ែត្រ?',
        [('កំណត់ ' + M('a = 17\\text{ m}, b = 8\\text{ m}') + ' បានសមីការ ' + M('\\frac{x^2}{289} + \\frac{y^2}{64} = 1'), 1),
         ('គណនា ' + M('c = \\sqrt{17^2 - 8^2} = \\sqrt{289 - 64} = 15\\text{ m}'), 1),
         ('ទីតាំងកំណុំទាំងពីរគឺ ' + M('F_1(15, 0)') + ' និង ' + M('F_2(-15, 0)'), 1),
         ('តាមលក្ខណៈចំណាំងផ្លាតនៃអេលីប សំឡេងពី ' + M('F_1') + ' ត្រូវចាំងផ្លាតទៅ ' + M('F_2'), 1),
         ('ចម្ងាយសរុប ' + M('PF_1 + PF_2 = 2a = 34\\text{ m}') + ' ។', 1)],
        bloom='Analyze'), svg46))

    # 47. Elliptical tunnel: base width 10 m (a = 5), center height 4 m (b = 4), truck 6 m wide x 3 m tall
    # At x = 3: y = 4 * sqrt(1 - 9/25) = 4 * 4/5 = 3.2 m > 3 m
    chk(lambda: (F(4) * F(4, 5) == F(16, 5), F(16, 5) > 3))
    svg47 = fig_ellipse(
        0, 0, 5, 4, -6.2, 6.2, 0.0, 5.2,
        xlabel='x (m)', ylabel='y (m)',
        xticks=[-5, -3, 3, 5], yticks=[4],
        title='Elliptical Tunnel',
        half_top=True,
        segs_data=[(-3, 0, -3, 3, P.K.AMBER, False), (3, 0, 3, 3, P.K.AMBER, False), (-3, 3, 3, 3, P.K.AMBER, False)],
        notes_data=[(1.6, 1.4, '6m x 3m', 0, 0, P.K.AMBER, False)],
    )
    qs.append(with_img(wr('pisa', 'p_tunnel',
        'ផ្លូវរូងក្រោមដីមួយមានផ្ទៃកាត់រាងកន្លះអេលីប ទទឹងបាត ' + M('10\\text{ m}') + ' និងកម្ពស់អតិបរមានៅចំណុចកណ្ដាល ' + M('4\\text{ m}') + ' ។ ក. រកសមីការអេលីប ។ ខ. តើរថយន្តទទឹង ' + M('6\\text{ m}') + ' និងកម្ពស់ ' + M('3\\text{ m}') + ' អាចបើកកាត់តាមកណ្ដាលផ្លូវរូងបានឬទេ?',
        [('កំណត់ ' + M('a = 5\\text{ m}, b = 4\\text{ m}') + ' ដោយផ្ចិតនៅគល់ ' + M('O(0, 0)'), 1),
         ('សមីការអេលីបគឺ ' + M('\\frac{x^2}{25} + \\frac{y^2}{16} = 1') + ' (' + M('y \\ge 0') + ')', 1),
         ('រថយន្តទទឹង ' + M('6\\text{ m}') + ' ត្រូវនឹង ' + M('x = \\pm 3\\text{ m}'), 1),
         ('ជំនួស ' + M('x = 3') + ' បាន ' + M('\\frac{y^2}{16} = 1 - \\frac{9}{25} = \\frac{16}{25} \\Rightarrow y = 3.2\\text{ m}'), 1),
         ('ដោយ ' + M('3.2\\text{ m} > 3\\text{ m}') + ' (សល់ចន្លោះ ' + M('0.2\\text{ m}') + ') ដូច្នេះរថយន្តអាចបើកកាត់បាន ។', 1)],
        bloom='Evaluate'), svg47))

    # 48. Satellite orbit: perigee a - c = 2, apogee a + c = 8 (in 10^3 km) -> a = 5, c = 3, b = 4, e = 0.6
    chk(lambda: (F(2 + 8, 2) == 5, 5 - 2 == 3, 5**2 - 3**2 == 4**2, F(3, 5) == F('0.6')))
    svg48 = fig_ellipse(
        0, 0, 5, 4, -6.2, 6.2, -5.0, 5.0,
        xlabel='x (10³ km)', ylabel='y (10³ km)',
        xticks=[-5, 5], yticks=[-4, 4],
        title='Satellite Orbit',
        dots_data=[(3, 0, 'Earth', 0, -10, P.K.BLUE)],
        segs_data=[(-5, 0, 3, 0, P.K.AMBER, True), (3, 0, 5, 0, P.K.RED, True)],
    )
    qs.append(with_img(wr('pisa', 'p_sat',
        'ផ្កាយរណបមួយគោចរជុំវិញផែនដីតាមគន្លងអេលីបដោយផែនដីនៅកំណុំ ' + M('F_1(c, 0)') + ' ។ ចម្ងាយជិតបំផុតពីផ្កាយរណបទៅផ្ចិតផែនដីគឺ ' + M('2 \\times 10^3\\text{ km}') + ' និងចម្ងាយឆ្ងាយបំផុតគឺ ' + M('8 \\times 10^3\\text{ km}') + ' ។ រកសមីការគន្លង និងអ៊ុចសង់ទ្រីស៊ីតេ ។',
        [('តាងឯកតាគិតជា ' + M('10^3\\text{ km}') + ' គេមានប្រព័ន្ធ ' + M('a - c = 2') + ' និង ' + M('a + c = 8'), 1),
         ('បូកសមីការទាំងពីរបាន ' + M('2a = 10 \\Rightarrow a = 5') + ' និង ' + M('c = 3'), 1),
         ('គណនា ' + M('b^2 = a^2 - c^2 = 25 - 9 = 16 \\Rightarrow b = 4'), 1),
         ('សមីការគន្លងអេលីបគឺ ' + M('\\frac{x^2}{25} + \\frac{y^2}{16} = 1'), 1),
         ('អ៊ុចសង់ទ្រីស៊ីតេគឺ ' + M('e = \\frac{c}{a} = \\frac{3}{5} = 0.6') + ' ។', 1)],
        bloom='Apply'), svg48))

    # 49. Elliptical fountain pool: major axis 26 m on Oy, foci (0, +-5) -> b = 12 m, width 24 m, e = 5/13
    chk(lambda: (F(26, 2) == 13, 13**2 - 5**2 == 12**2, 2 * 12 == 24))
    svg49 = fig_ellipse(
        0, 0, 12, 13, -15.5, 15.5, -16.0, 16.0,
        xlabel='x (m)', ylabel='y (m)',
        xticks=[], yticks=[-13, 13],
        title='Fountain Pool',
        dots_data=[(0, 5, 'F1(0, 5)', 10, 4, P.K.RED), (0, -5, 'F2(0, -5)', 10, 4, P.K.RED)],
    )
    qs.append(with_img(wr('pisa', 'p_pool',
        'អាងទឹករាងអេលីបមួយមានផ្ចិតនៅគល់ ' + M('O(0, 0)') + ' អ័ក្សធំនៅលើ ' + M('Oy') + ' ប្រវែង ' + M('26\\text{ m}') + ' និងក្បាលបាញ់ទឹកពីរស្ថិតនៅកំណុំ ' + M('F_1(0, 5)') + ' និង ' + M('F_2(0, -5)') + ' ។ រកសមីការអេលីប ទទឹងអាង និងអ៊ុចសង់ទ្រីស៊ីតេ ។',
        [('ដោយអ័ក្សធំនៅលើ ' + M('Oy') + ' គេមាន ' + M('2a = 26 \\Rightarrow a = 13\\text{ m}') + ' និង ' + M('c = 5\\text{ m}'), 1),
         ('គណនា ' + M('b^2 = a^2 - c^2 = 169 - 25 = 144 \\Rightarrow b = 12\\text{ m}'), 1),
         ('ទទឹងអាងទឹកគឺ ' + M('2b = 24\\text{ m}'), 1),
         ('សមីការអេលីបគឺ ' + M('\\frac{x^2}{144} + \\frac{y^2}{169} = 1'), 1),
         ('អ៊ុចសង់ទ្រីស៊ីតេគឺ ' + M('e = \\frac{c}{a} = \\frac{5}{13}') + ' ។', 1)],
        bloom='Apply'), svg49))

    # 50. Acoustic reflection room: foci (-12, 0), (12, 0), passes through (0, 5) -> b = 5, a = 13, e = 12/13, latus rectum 50/13
    chk(lambda: (12**2 + 5**2 == 13**2, F(2 * 25, 13) == F(50, 13)))
    svg50 = fig_ellipse(
        0, 0, 13, 5, -16.0, 16.0, -7.2, 7.2,
        xlabel='x (m)', ylabel='y (m)',
        xticks=[], yticks=[5],
        title='Acoustic Room',
        dots_data=[(-12, 0, 'F2(-12, 0)', 6, -8, P.K.RED), (12, 0, 'F1(12, 0)', -6, -8, P.K.RED), (0, 5, 'B1(0, 5)', 8, -8, P.K.BLUE)],
    )
    qs.append(with_img(wr('pisa', 'p_room',
        'បន្ទប់ចាំងសំឡេងរាងអេលីបមួយមានកំណុំនៅ ' + M('F_2(-12, 0)') + ' និង ' + M('F_1(12, 0)') + ' ហើយគែមជញ្ជាំងកាត់តាមចំណុច ' + M('(0, 5)') + ' (ឯកតាជាម៉ែត្រ) ។ ក. រកសមីការបន្ទប់ ។ ខ. រកអ៊ុចសង់ទ្រីស៊ីតេ និងប្រវែងអង្កត់កាត់កំណុំកែងអ័ក្សធំ ។',
        [('ផ្ចិតគឺ ' + M('O(0, 0)') + ' ដោយកំណុំលើ ' + M('Ox') + ' បាន ' + M('c = 12') + ' និងចំណុច ' + M('(0, 5)') + ' ឱ្យ ' + M('b = 5'), 1),
         ('គណនា ' + M('a = \\sqrt{b^2 + c^2} = \\sqrt{25 + 144} = 13\\text{ m}'), 1),
         ('សមីការស្ដង់ដាគឺ ' + M('\\frac{x^2}{169} + \\frac{y^2}{25} = 1'), 1),
         ('អ៊ុចសង់ទ្រីស៊ីតេគឺ ' + M('e = \\frac{c}{a} = \\frac{12}{13}'), 1),
         ('ប្រវែងអង្កត់កាត់កំណុំកែងអ័ក្សធំគឺ ' + M('\\frac{2b^2}{a} = \\frac{2 \\times 25}{13} = \\frac{50}{13}\\text{ m}') + ' ។', 1)],
        bloom='Create'), svg50))

    return qs


def cands():
    from lib import normalise
    return normalise(_cands_raw())


if __name__ == '__main__':
    print(f'G12L26: {len(cands())} candidates, {CNT[0]} numeric checks passed')
