# Section 4 pictures that are revealed step by step (data-step / data-until, see lib.rvg / lib.capstack)
from lib import *

TENS, ONES = BLUE, ORANGE


def regroup_52_27():
    """52 - 27 with place-value blocks: why we borrow."""
    b = T(170, 40, 'ដប់', 28, TENS) + T(555, 40, 'រាយ', 28, ONES)
    # five tens rods; the 5th one is broken up at step 1
    def rod(x, extra=''):
        r = rect(x, 60, 34, 140, TENS, 6)
        r += ''.join(line(x + 3, 60 + k * 14, x + 31, 60 + k * 14, '#fff', 2) for k in range(1, 10))
        return r + extra
    for i in range(5):
        x = 50 + i * 52
        b += rvg(0, rod(x), until=1) if i == 4 else rod(x)
    b += rvg(1, rect(258, 56, 42, 148, 'none', 8, GOLD, 4).replace('stroke-width="4"', 'stroke-width="4" stroke-dasharray="10 6"')
             + arrow(304, 130, 408, 112, GOLD, 5))
    def cube(k):
        x, y = 420 + (k % 6) * 46, 60 + (k // 6) * 46
        return rect(x, y, 34, 34, ONES, 6) + circ(x + 10, y + 10, 4, '#fff').replace('fill="#fff"', 'fill="#fff" opacity=".55"')
    for k in range(12):
        b += cube(k) if k < 2 else rvg(1, cube(k))
    # step 2: cross out 7 ones; step 3: cross out 2 tens; step 4: ring what is left
    cross = lambda x, y, w, h: line(x, y, x + w, y + h, RED, 6) + line(x, y + h, x + w, y, RED, 6)
    b += rvg(2, ''.join(cross(420 + (k % 6) * 46, 60 + (k // 6) * 46, 34, 34) for k in range(7)))
    b += rvg(3, ''.join(cross(50 + i * 52, 60, 34, 140) for i in range(2)))
    # what is left: tens rods 3 and 4 (the 5th was broken up) and the last five ones
    b += rvg(4, rect(146, 52, 102, 156, 'none', 14, GREEN, 6) + rect(458, 98, 5 * 46, 46, 'none', 12, GREEN, 6))
    fg = fig(svg(1000, 230, b, '32vh'))
    caps = capstack([
        (0, 1, '52 = ៥ ដប់ + ២ រាយ ។ ត្រូវដក 27 = ២ ដប់ + ៧ រាយ'),
        (1, 2, '២ រាយ មិនគ្រប់ដក ៧ រាយ → ' + hl('ខ្ចី ១ ដប់ = ១០ រាយ', GOLD) + ' ។ ឥឡូវមាន ៤ ដប់ និង ១២ រាយ'),
        (2, 3, 'ដក ៧ រាយ ចេញ → នៅសល់ ៥ រាយ'),
        (3, 4, 'ដក ២ ដប់ ចេញ → នៅសល់ ២ ដប់'),
        (4, None, 'នៅសល់ ២ ដប់ និង ៥ រាយ ដូចនេះ ' + hl(m('52-27=25'), GREEN)),
    ])
    return fg + caps


def jump_48_29():
    """48 + 29 by jumping +30 then back -1."""
    import math
    x = lambda v: 60 + (v - 46) * 26
    y0 = 200
    b = line(60, y0, 960, y0, NAVY, 5)
    for v in range(46, 81):
        b += line(x(v), y0 - (12 if v % 5 == 0 else 7), x(v), y0 + (12 if v % 5 == 0 else 7), NAVY, 3)
        if v % 5 == 0:
            b += T(x(v), y0 + 48, v, 26, NAVY)
    b += circ(x(48), y0, 13, BLUE, '#fff', 3) + T(x(48), y0 - 30, '48', 32, BLUE)
    # the +30 hop: a quadratic arc with a proper arrow head along its end tangent
    sx, sy, ex, ey = x(48), y0 - 16, x(78), y0 - 16
    cx, cy = (sx + ex) / 2, 24
    ang = math.atan2(ey - cy, ex - cx)
    hx, hy = ex - 22 * math.cos(ang), ey - 22 * math.sin(ang)
    nx, ny = -math.sin(ang) * 11, math.cos(ang) * 11
    b += rvg(1, f'<path d="M{sx} {sy} Q{cx} {cy} {hx:.1f} {hy:.1f}" fill="none" stroke="{ORANGE}" stroke-width="7" stroke-linecap="round"/>'
                f'<polygon points="{ex},{ey} {hx+nx:.1f},{hy+ny:.1f} {hx-nx:.1f},{hy-ny:.1f}" fill="{ORANGE}"/>'
             + T(cx, 78, '+30', 42, ORANGE) + circ(x(78), y0, 11, ORANGE, '#fff', 3) + T(x(78) + 18, y0 - 34, '78', 30, ORANGE, 'start'))
    # the -1 hop back, drawn under the line, and the answer point
    b += rvg(2, f'<path d="M{x(78)} {y0+22} Q{(x(78)+x(77))/2} {y0+84} {x(77)} {y0+22}" fill="none" stroke="{RED}" stroke-width="6" stroke-linecap="round"/>'
             + T((x(78) + x(77)) / 2, y0 + 118, '−1', 36, RED) + circ(x(77), y0, 14, GREEN, '#fff', 4) + T(x(77) - 20, y0 - 34, '77', 34, GREEN, 'end'))
    b += rvg(3, rect(x(77) - 56, 8, 160, 58, '#d3f9d8', 14, GREEN, 4) + T(x(77) + 24, 50, '= 77', 40, GREEN))
    fg = fig(svg(1000, 330, b, '38vh'))
    caps = capstack([
        (0, 1, 'គណនា ' + m('48+29') + ' ។ ចំនួន ' + m('29') + ' ជិត ' + m('30') + ' ដូចនេះ លោត ' + m('+30') + ' ងាយជាង'),
        (1, 2, 'លោត ' + hl(m('+30'), ORANGE) + ' ពី ' + m('48') + ' ទៅដល់ ' + m('78')),
        (2, 3, 'លោតលើស ១ ហើយ → ត្រឡប់មកវិញ ' + hl(m('-1'), RED) + ' ទៅ ' + m('77')),
        (3, None, m('48+29 = 48+30-1 = 77')),
    ])
    return fg + caps


def estimate_check():
    """Check 735 + 196 by rounding."""
    top = p('គណនា ' + m('735+196') + ' ។ ពិនិត្យចម្លើយដោយប៉ាន់ស្មាន ៖')
    s1 = rvd(1, '<span class="stepcard a">735 ≈ 700</span><span class="stepcard a">196 ≈ 200</span><div style="font-size:.8em;opacity:.8">បង្កត់ទៅរយជិតបំផុត</div>')
    s2 = rvd(2, '<span class="stepcard b">700 + 200 = 900</span><div style="font-size:.8em;opacity:.8">ចម្លើយពិតត្រូវនៅជិត ' + m('900') + '</div>')
    s3 = rvd(3, '<span class="stepcard ok">931 ✔ ជិត 900</span><span class="stepcard no">831 ✘ ឆ្ងាយពី 900 → ពិនិត្យលេខទុកម្តងទៀត</span>')
    return top + '<div style="text-align:center">' + s1 + s2 + s3 + '</div>'


def area_23_14():
    """23 x 14 as the area of a rectangle cut into four."""
    X, Y, wa, wb, ha, hb = 120, 70, 480, 72, 200, 80
    # whole-rectangle sizes sit outside, on a thin bracket; the pieces' sizes sit just beside the rectangle
    b = (line(X, 30, X + wa + wb, 30, NAVY, 3) + line(X, 22, X, 38, NAVY, 3) + line(X + wa + wb, 22, X + wa + wb, 38, NAVY, 3)
         + T(X + (wa + wb) / 2, 20, '23', 30, NAVY) + line(30, Y, 30, Y + ha + hb, NAVY, 3) + line(22, Y, 38, Y, NAVY, 3)
         + line(22, Y + ha + hb, 38, Y + ha + hb, NAVY, 3) + T(12, Y + (ha + hb) / 2 + 10, '14', 30, NAVY, 'start'))
    b += rect(X, Y, wa + wb, ha + hb, 'none', 4, NAVY, 5)
    b += rvg(1, line(X + wa, Y - 6, X + wa, Y + ha + hb, NAVY, 3, '10 7') + line(X - 6, Y + ha, X + wa + wb, Y + ha, NAVY, 3, '10 7')
             + T(X + wa / 2, Y - 12, '20', 26, BLUE) + T(X + wa + wb / 2, Y - 12, '3', 26, ORANGE)
             + T(X - 20, Y + ha / 2 + 8, '10', 26, BLUE) + T(X - 20, Y + ha + hb / 2 + 8, '4', 26, GREEN))
    b += rvg(2, rect(X + 3, Y + 3, wa - 6, ha - 6, '#cfe3f5', 8) + T(X + wa / 2, Y + ha / 2 + 12, '20 × 10 = 200', 38, BLUE))
    b += rvg(3, rect(X + wa + 3, Y + 3, wb - 6, ha - 6, '#ffe8b3', 8) + T(X + wa + wb / 2, Y + ha / 2 + 10, '30', 32, ORANGE)
             + rect(X + 3, Y + ha + 3, wa - 6, hb - 6, '#cdeed3', 8) + T(X + wa / 2, Y + ha + hb / 2 + 12, '20 × 4 = 80', 34, GREEN))
    b += rvg(4, rect(X + wa + 3, Y + ha + 3, wb - 6, hb - 6, '#e7d5f3', 8) + T(X + wa + wb / 2, Y + ha + hb / 2 + 10, '12', 30, PURPLE))
    px = 730
    b += rvg(2, T(px + 110, 90, 'ផលបូកផ្នែកៗ', 26, NAVY) + T(px + 190, 150, '200', 36, BLUE, 'end'))
    b += rvg(3, T(px + 190, 200, '+  30', 36, ORANGE, 'end') + T(px + 190, 250, '+  80', 36, GREEN, 'end'))
    b += rvg(4, T(px + 190, 300, '+  12', 36, PURPLE, 'end'))
    b += rvg(5, line(px + 20, 318, px + 200, 318, NAVY, 4) + T(px + 190, 362, '= 322', 44, RED, 'end'))
    fg = fig(svg(1000, 380, b, '42vh'))
    caps = capstack([
        (0, 1, 'គណនា ' + m('23\\times 14') + ' ដោយគិតជាផ្ទៃចតុកោណកែងមានទទឹង ' + m('23') + ' កម្ពស់ ' + m('14')),
        (1, 2, 'បំបែក ' + m('23=20+3') + ' និង ' + m('14=10+4') + ' → ចតុកោណកែងតូចៗ ៤'),
        (2, 3, m('20\\times 10=200')),
        (3, 4, m('3\\times 10=30') + ' និង ' + m('20\\times 4=80')),
        (4, 5, m('3\\times 4=12')),
        (5, None, m('23\\times 14 = 200+30+80+12 = 322')),
    ])
    return fg + caps


def chunk_6645_15():
    """6645 / 15 in chunks: how many 15s fit?"""
    rows = [(400, 6000, 645, BLUE), (40, 600, 45, TEAL), (3, 45, 0, GREEN)]
    b = ''
    for k, (q, prod, rest, col) in enumerate(rows):
        y = 14 + k * 78
        prev = 6645 if k == 0 else rows[k - 1][2]
        b += rvg(k + 1, rect(30, y, 380, 62, col, 16) + T(220, y + 43, f'15 × {q} = {prod}', 34, '#fff')
                 + arrow(420, y + 31, 520, y + 31, NAVY, 5)
                 + T(540, y + 43, f'{prev} − {prod} = {rest}', 34, NAVY, 'start'))
    b += rvg(4, rect(30, 250, 940, 66, '#d3f9d8', 18, GREEN, 5) + T(500, 295, '400 + 40 + 3 = 443', 40, GREEN))
    fg = fig(svg(1000, 330, b, '40vh'))
    top = p('ចែក ' + m('6645\\div 15') + ' ជាដំណាក់កាល — រកមើលថា មាន ' + m('15') + ' ប៉ុន្មានក្នុង ' + m('6645'))
    caps = capstack([
        (0, 1, 'ចាប់ផ្តើមពី ' + m('6645') + ' ហើយដកចេញដងធំៗសិន'),
        (1, 2, m('15\\times 400=6000') + ' ចូលក្នុង ' + m('6645') + ' បាន → នៅសល់ ' + m('645')),
        (2, 3, m('15\\times 40=600') + ' ចូលក្នុង ' + m('645') + ' បាន → នៅសល់ ' + m('45')),
        (3, 4, m('15\\times 3=45') + ' ចូលក្នុង ' + m('45') + ' ពិតប្រាកដ → នៅសល់ ' + m('0')),
        (4, None, 'ដូចនេះ ' + hl(m('6645\\div 15=443'), GREEN) + ' — វិធីចែកឈរធ្វើដូចគ្នានេះ តែសរសេរខ្លីជាង'),
    ])
    return top + fg + caps
