"""Pictures for the book-following Grade 9 Lesson 1 deck. Every maths label is typeset with KaTeX (inside <foreignObject>), not drawn as SVG text.
Nothing here animates by itself: pieces appear with the slide's reveal steps (rvg) and the stylesheet fades them in smoothly."""
import math
from fractions import Fraction
from lib import *

BLUE_L, ORANGE_L, GREEN_L, PURPLE_L = '#d0e6fa', '#ffe0cf', '#d3f9d8', '#f1d9f7'


def KT(x, y, tex, size=40, col=NAVY, anchor='middle', w=460, h=None):
    """typeset maths (KaTeX) centred vertically on y; anchor = middle | start | end"""
    h = h or size * 2.2
    off = {'middle': -w / 2, 'start': 0, 'end': -w}[anchor]
    jc = {'middle': 'center', 'start': 'flex-start', 'end': 'flex-end'}[anchor]
    t = tex.replace('<', '&lt;')
    return (f'<foreignObject x="{x + off:.1f}" y="{y - h / 2:.1f}" width="{w}" height="{h:.1f}" style="overflow:visible">'
            f'<div xmlns="http://www.w3.org/1999/xhtml" style="display:flex;align-items:center;justify-content:{jc};height:100%;font-size:{size}px;color:{col};line-height:1;white-space:nowrap">\\({t}\\)</div></foreignObject>')


def _tri(x, y, d, col):
    return f'<polygon points="{x},{y} {x - d},{y - d * .45} {x - d},{y + d * .45}" fill="{col}"/>'


def numline(x0, x1, y, col=NAVY):
    return line(x0, y, x1, y, col, 5) + _tri(x1 + 22, y, 24, col)


def garden():
    """a square garden of area 3 m^2: side x, so x^2 = 3"""
    side, x0, y0 = 270, 170, 40
    b = rect(x0, y0, side, side, '#d3f9d8', 8, TEAL, 5)
    b += KT(x0 + side / 2, y0 + side / 2, r'S=3\,\text{m}^2', 44, NAVY)
    b += line(x0, y0 + side + 26, x0 + side, y0 + side + 26, RED, 4) + line(x0, y0 + side + 14, x0, y0 + side + 38, RED, 4) + line(x0 + side, y0 + side + 14, x0 + side, y0 + side + 38, RED, 4)
    b += KT(x0 + side / 2, y0 + side + 76, 'x', 46, RED, w=120)
    b += line(x0 - 26, y0, x0 - 26, y0 + side, RED, 4) + line(x0 - 38, y0, x0 - 14, y0, RED, 4) + line(x0 - 38, y0 + side, x0 - 14, y0 + side, RED, 4)
    b += KT(x0 - 70, y0 + side / 2, 'x', 46, RED, w=100)
    b += rvg(1, KT(600, 150, r'S=x^2', 50, NAVY, 'start'))
    b += rvg(2, KT(600, 250, r'x^2=3', 56, RED, 'start'))
    b += rvg(3, KT(600, 350, r'x=\,?', 56, TEAL, 'start'))
    assert 3 > 0
    return svg(1000, 440, b, '50vh')


def squeeze_sqrt3():
    """book example 3: 1, 3/2, 5/3 have squares below 3, 2 has a square above 3; sqrt3 lies between 5/3 and 2 (1.73 < sqrt3 < 1.74)"""
    assert Fraction(1) ** 2 < 3 and Fraction(3, 2) ** 2 < 3 and Fraction(5, 3) ** 2 < 3 and Fraction(2) ** 2 > 3
    assert Fraction(173, 100) ** 2 < 3 < Fraction(174, 100) ** 2
    X = lambda t: 70 + (float(t) - 1) * 800                       # 1 -> 70, 2 -> 870
    y = 190
    b = numline(40, 900, y)
    pts = [(Fraction(1), '1', r'1^2=1', BLUE), (Fraction(3, 2), r'\tfrac{3}{2}', r'\left(\tfrac{3}{2}\right)^2=2.25', BLUE),
           (Fraction(5, 3), r'\tfrac{5}{3}', r'\left(\tfrac{5}{3}\right)^2\approx 2.78', BLUE), (Fraction(2), '2', r'2^2=4', ORANGE)]
    for k, (t, lab, sq, col) in enumerate(pts):
        g = line(X(t), y - 16, X(t), y + 16, col, 5) + KT(X(t), y - 52, lab, 40, col, w=160) + KT(X(t), y + 74 + (56 if k % 2 else 0), sq, 32, col, w=380)
        b += rvg(1 + k, g)
    root = X(math.sqrt(3))
    b += rvg(5, circ(root, y, 14, RED, '#fff', 4) + KT(root, y - 100, r'\sqrt{3}', 52, RED, w=160) + line(root, y - 62, root, y - 20, RED, 3))
    b += KT(500, 28, r'x^2<3\ \longrightarrow\ \ x^2>3', 34, GREY, w=700)
    return svg(1000, 350, b, '44vh')


def squeeze_cbrt17():
    """book example 3 (cube roots): 2^3=8, 2.5^3=15.625 < 17 < 17.576=2.6^3, so 2.5 < cbrt17 < 2.6"""
    assert 2 ** 3 == 8 and Fraction('2.5') ** 3 == Fraction('15.625') < 17 < Fraction('17.576') == Fraction('2.6') ** 3
    X = lambda t: 70 + (float(t) - 2) * 800
    y = 170
    b = numline(40, 900, y)
    pts = [(2, '2', r'2^3=8', BLUE), (Fraction('2.5'), '2.5', r'2.5^3=15.625', BLUE), (Fraction('2.6'), '2.6', r'2.6^3=17.576', ORANGE), (3, '3', r'3^3=27', ORANGE)]
    for k, (t, lab, cu, col) in enumerate(pts):
        b += rvg(1 + k, line(X(t), y - 16, X(t), y + 16, col, 5) + KT(X(t), y - 50, lab, 38, col, w=160) + KT(X(t), y + 74 + (56 if k % 2 else 0), cu, 32, col, w=380))
    root = X(17 ** (1 / 3))
    b += rvg(5, circ(root, y, 14, RED, '#fff', 4) + KT(root, y - 110, r'\sqrt[3]{17}', 52, RED, w=200) + line(root, y - 66, root, y - 20, RED, 3))
    return svg(1000, 340, b, '42vh')


def _curve(x1, y1, cx, cy, x2, y2, col, w=3):
    """a thin curved arrow from (x1,y1) to (x2,y2) bending through (cx,cy)"""
    import math as _m
    ang = _m.atan2(y2 - cy, x2 - cx)
    d = 15
    a1, a2 = ang + _m.radians(155), ang - _m.radians(155)
    tip = f'<polygon points="{x2},{y2} {x2 + d * _m.cos(a1):.1f},{y2 + d * _m.sin(a1):.1f} {x2 + d * _m.cos(a2):.1f},{y2 + d * _m.sin(a2):.1f}" fill="{col}"/>'
    return f'<path d="M {x1} {y1} Q {cx} {cy} {x2} {y2}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>' + tip


def radical_parts():
    """the n-th root of a^m with its four named parts, drawn like the textbook figure: blue rounded box, red index and exponent, blue radicand, grey radical sign"""
    RED_, BLU, GRY = '#e03131', '#1c1cc0', '#7d8791'
    b = rect(10, 10, 680, 330, '#eeeefb', 28, BLU, 5)
    b += KT(350, 190, r'\sqrt[\textcolor{#e03131}{n}]{\textcolor{#1c1cc0}{a}^{\textcolor{#e03131}{m}}}', 150, '#222', w=420, h=260)
    b += rvg(1, T(175, 78, 'សន្ទស្សន៍', 40, RED_) + _curve(236, 94, 262, 98, 244, 113, RED_))
    b += rvg(2, T(525, 78, 'និទស្សន្ត', 40, RED_) + _curve(508, 96, 506, 114, 484, 126, RED_))
    b += rvg(3, T(175, 308, 'សញ្ញារ៉ាឌីកាល់', 40, GRY) + _curve(246, 285, 252, 270, 242, 257, GRY))
    b += rvg(4, T(525, 308, 'រ៉ាឌីកង់', 40, BLU) + _curve(490, 284, 440, 276, 402, 250, BLU))
    return svg(700, 350, b, '52vh')


def area_product():
    """sqrt4 x sqrt9: a rectangle 2 by 3 has area 6 = sqrt36"""
    assert 2 * 3 == 6 and 4 * 9 == 36 and 6 * 6 == 36
    c = 82
    x, y = 90, 30
    b = ''
    for i in range(3):
        for j in range(2):
            b += rect(x + j * c, y + i * c, c - 6, c - 6, BLUE_L, 6, BLUE, 3)
    b += rvg(1, KT(x + c - 3, y + 1.5 * c, '6', 56, NAVY, w=100))
    b += KT(x + c - 3, y + 3 * c + 40, r'\sqrt{4}=2', 40, BLUE, w=240)
    b += KT(x + 2 * c + 80, y + 1.5 * c, r'\sqrt{9}=3', 40, TEAL, w=240)
    b += rvg(2, KT(560, 110, r'\sqrt{4}\times\sqrt{9}=2\times 3=6', 40, NAVY, 'start', w=520))
    b += rvg(3, KT(560, 200, r'\sqrt{4\times 9}=\sqrt{36}=6', 40, NAVY, 'start', w=520))
    b += rvg(4, KT(560, 290, r'\sqrt{4}\times\sqrt{9}=\sqrt{4\times 9}', 44, RED, 'start', w=520))
    return svg(1000, 360, b, '42vh')


def simplify18():
    """sqrt18 = 3 sqrt2: nine squares of area 2 make a square of side 3 sqrt2"""
    assert 9 * 2 == 18 and 3 * 3 == 9
    c = 82
    x, y = 90, 30
    b = ''
    for i in range(3):
        for j in range(3):
            b += rect(x + j * c, y + i * c, c - 6, c - 6, '#fff3bf', 6, GOLD, 3) + KT(x + j * c + (c - 6) / 2, y + i * c + (c - 6) / 2, '2', 34, NAVY, w=60)
    b += KT(x + 1.5 * c, y + 3 * c + 36, r'3\sqrt{2}', 40, RED, w=200)
    b += KT(x - 40, y + 1.5 * c, r'3\sqrt{2}', 40, RED, 'end', w=160)
    b += rvg(1, KT(600, 90, r'\text{ផ្ទៃ}=9\times 2=18', 40, TEAL, 'start', w=520))
    b += rvg(2, KT(600, 190, r'\sqrt{18}=\sqrt{9\times 2}', 44, NAVY, 'start', w=520))
    b += rvg(3, KT(600, 290, r'=3\sqrt{2}', 52, RED, 'start', w=520))
    return svg(1000, 380, b, '44vh')


def like_radicals():
    """3 sqrt2 + 4 sqrt2 = 7 sqrt2: bars of the same length add; a sqrt3 bar is a different length"""
    u2, u3 = math.sqrt(2) * 70, math.sqrt(3) * 70
    assert abs(7 * u2 - (3 * u2 + 4 * u2)) < 1e-9 and abs(u3 - u2) > 10
    x0, y = 50, 80
    b = ''
    for i in range(3):
        b += rect(x0 + i * u2, y, u2 - 4, 46, BLUE_L, 6, BLUE, 3)
    b += KT(x0 + 1.5 * u2, y - 34, r'3\sqrt{2}', 40, BLUE, w=200)
    g = ''.join(rect(x0 + (3 + i) * u2, y, u2 - 4, 46, ORANGE_L, 6, ORANGE, 3) for i in range(4)) + KT(x0 + 5 * u2, y - 34, r'4\sqrt{2}', 40, ORANGE, w=200)
    b += rvg(1, g)
    b += rvg(2, line(x0, y + 98, x0 + 7 * u2 - 4, y + 98, RED, 6) + KT(x0 + 3.5 * u2, y + 160, r'3\sqrt{2}+4\sqrt{2}=7\sqrt{2}', 46, RED, w=700))
    y2 = y + 300
    g = ''.join(rect(x0 + i * u2, y2, u2 - 4, 46, BLUE_L, 6, BLUE, 3) for i in range(3)) + ''.join(rect(x0 + 3 * u2 + i * u3, y2, u3 - 4, 46, GREEN_L, 6, GREEN, 3) for i in range(4))
    g += KT(x0 + 1.5 * u2, y2 - 34, r'3\sqrt{2}', 40, BLUE, w=200) + KT(x0 + 3 * u2 + 2 * u3, y2 - 34, r'4\sqrt{3}', 40, GREEN, w=200)
    g += T(500, y2 + 110, 'ប្រវែងមិនស្មើគ្នា → បូកមិនបាន', 34, NAVY)
    b += rvg(3, g)
    return svg(1000, 540, b, '58vh')


def plant(kind='sq'):
    """A number is a petal, its roots grow underground, and a number and its roots share one colour (ឫស = root of a plant = root of a number).
    square plant: 9 -> 3 and -3, 5 -> sqrt5 and -sqrt5, -4 -> none.   cube plant: 8 -> 2, 17 -> cbrt17, -27 -> -3 (one root each)."""
    BLUE_, ORANGE_, PURPLE_, GREY_ = '#1c7ed6', '#e8590c', '#ae3ec9', '#868e96'
    if kind == 'sq':
        assert 3 ** 2 == 9 and (-3) ** 2 == 9 and math.isqrt(5) ** 2 != 5 and all(r * r != -4 for r in range(-5, 6))
        items = [('9', ['3', '-3'], BLUE_), ('5', [r'\sqrt{5}', r'-\sqrt{5}'], ORANGE_), ('-4', [], GREY_)]
    else:
        assert 2 ** 3 == 8 and round(17 ** (1 / 3)) ** 3 != 17 and (-3) ** 3 == -27
        items = [('8', ['2'], BLUE_), ('17', [r'\sqrt[3]{17}'], ORANGE_), ('-27', ['-3'], PURPLE_)]
    tint = {BLUE_: BLUE_L, ORANGE_: ORANGE_L, PURPLE_: PURPLE_L, GREY_: '#ececec'}
    W, H, G = 760, 680, 330
    b = f'<rect x="0" y="0" width="{W}" height="{H}" rx="30" fill="#fff4e8"/>'
    b += f'<path d="M 0 {G} H {W} V {H - 30} Q {W} {H} {W - 30} {H} H 30 Q 0 {H} 0 {H - 30} Z" fill="#f1d6b3"/>'
    for k in range(30):
        b += f'<circle cx="{30 + (k * 97) % 700}" cy="{G + 30 + (k * 53) % 290}" r="{2 + k % 3}" fill="#c9a574" opacity=".5"/>'
    b += line(0, G, W, G, '#4a3b3b', 6)
    cx, cy = W / 2, 150
    for a in (30, 90, 150):
        x, y = cx + 74 * math.cos(math.radians(a)), cy + 74 * math.sin(math.radians(a))
        b += f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="44" ry="52" transform="rotate({a + 90} {x:.1f} {y:.1f})" fill="#f8c8d8" stroke="#8d5a6b" stroke-width="3"/>'
    petal = []
    for a, (num, roots, col) in zip((-150, -90, -30), items):
        x, y = cx + 74 * math.cos(math.radians(a)), cy + 74 * math.sin(math.radians(a))
        petal.append((x, y))
        b += f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="46" ry="54" transform="rotate({a + 90} {x:.1f} {y:.1f})" fill="{tint[col]}" stroke="{col}" stroke-width="5"/>'
    b += f'<circle cx="{cx}" cy="{cy}" r="44" fill="#fff2a0" stroke="#7a6a2a" stroke-width="3"/>'
    if kind == 'cu':
        b += (f'<polygon points="{cx - 20},{cy - 8} {cx + 12},{cy - 8} {cx + 12},{cy + 24} {cx - 20},{cy + 24}" fill="#ffe066" stroke="#7a6a2a" stroke-width="3"/>'
              f'<polygon points="{cx - 20},{cy - 8} {cx + 12},{cy - 8} {cx + 24},{cy - 20} {cx - 8},{cy - 20}" fill="#fff3b0" stroke="#7a6a2a" stroke-width="3"/>'
              f'<polygon points="{cx + 12},{cy - 8} {cx + 24},{cy - 20} {cx + 24},{cy + 12} {cx + 12},{cy + 24}" fill="#f2c94c" stroke="#7a6a2a" stroke-width="3"/>')
    else:
        b += rect(cx - 19, cy - 19, 38, 38, '#ffe066', 4, '#7a6a2a', 3)
    b += f'<path d="M {cx} {cy + 44} C {cx + 24} {cy + 100} {cx - 26} {cy + 150} {cx - 6} {G}" fill="none" stroke="#3f6b3a" stroke-width="10" stroke-linecap="round"/>'
    b += f'<path d="M {cx - 8} 250 C {cx - 70} 215 {cx - 120} 222 {cx - 142} 252 C {cx - 98} 275 {cx - 58} 274 {cx - 8} 250 Z" fill="#cfe8bf" stroke="#3f6b3a" stroke-width="3"/>'
    b += f'<path d="M {cx + 2} 285 C {cx + 56} 245 {cx + 104} 250 {cx + 128} 280 C {cx + 84} 302 {cx + 46} 300 {cx + 2} 285 Z" fill="#cfe8bf" stroke="#3f6b3a" stroke-width="3"/>'
    for (x, y), (num, roots, col) in zip(petal, items):
        b += KT(x, y + 2, num, 54, col, w=120)
    slots = [[(95, 470), (235, 540)], [(345, 585), (500, 500)], [(655, 470)]] if kind == 'sq' else [[(110, 480)], [(380, 575)], [(650, 480)]]
    step = 1
    for (num, roots, col), sl in zip(items, slots):
        g = ''
        if not roots:
            tx, ty = sl[0]
            g += f'<path d="M {cx - 6} {G} C {cx + 120} {G + 40} {tx - 60} {ty - 60} {tx} {ty - 40}" fill="none" stroke="{col}" stroke-width="6" stroke-dasharray="10 8" stroke-linecap="round"/>'
            g += f'<ellipse cx="{tx}" cy="{ty}" rx="70" ry="50" fill="#f3f3f3" stroke="{col}" stroke-width="5" stroke-dasharray="10 8"/>' + T(tx, ty + 14, 'គ្មាន', 38, '#6c757d')
        for r, (tx, ty) in zip(roots, sl):
            g += f'<path d="M {cx - 6} {G} C {(cx + tx) / 2:.0f} {G + 30} {tx} {ty - 90} {tx} {ty - 46}" fill="none" stroke="{col}" stroke-width="7" stroke-linecap="round"/>'
            g += f'<ellipse cx="{tx}" cy="{ty}" rx="72" ry="50" fill="{tint[col]}" stroke="{col}" stroke-width="5"/>' + KT(tx, ty + 2, r, 50, col, w=140)
        b += rvg(step, g)
        step += 1
    return svg(W, H, b, '62vh')
