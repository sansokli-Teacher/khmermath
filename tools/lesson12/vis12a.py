# Lesson 12 pictures, part 1: real objects (drawn as shaded vector illustrations) and the exact geometry figures built from them.
# Every position is computed from coordinates; labels use the italic Times maths style (M) like the maths on the slide.
import math, os, sys
HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, '..', 'lesson3'))
from vis3 import *          # NL, M, sg, ... and lesson1 lib (T, circ, rect, line, arrow, rvg, svg, fig, ...)

_ID = [0]


def uid(p='g'):
    _ID[0] += 1
    return f'{p}{_ID[0]}'


def svgd(w, h, body, maxh='46vh', defs=''):
    return f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" style="max-height:{maxh}" role="img"><defs>{defs}</defs>{body}</svg>'


def lg(i, stops, x1=0, y1=0, x2=1, y2=0):
    s = ''.join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    return f'<linearGradient id="{i}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{s}</linearGradient>'


def rg(i, stops, cx=.4, cy=.35, r=.7):
    s = ''.join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    return f'<radialGradient id="{i}" cx="{cx}" cy="{cy}" r="{r}">{s}</radialGradient>'


def poly(pts, fill, stroke='none', sw=0, extra=''):
    return f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" {extra}/>'


def dot(x, y, col=NAVY, r=8):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{col}" stroke="#fff" stroke-width="2.5"/>'


def TM(x, y, khmer, math_, size=34, fill=NAVY, anchor='middle'):
    """Khmer text followed by maths: the Khmer stays upright, the letters are italic Times"""
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="700" {FONT}>{khmer} '
            f'<tspan {MATHFONT} font-weight="600">{math_}</tspan></text>')


def lab(x, y, t, col=NAVY, size=34, anchor='middle'):
    return M(x, y, t, size, col, anchor, 600)


def dline(x1, y1, x2, y2, col=NAVY, w=4, arrows=True, ext=0):
    """a straight line drawn past its two points, with an arrowhead at each end (a line has no ends)"""
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1
    ux, uy = dx / L, dy / L
    a, b = (x1 - ux * ext, y1 - uy * ext), (x2 + ux * ext, y2 + uy * ext)
    out = f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>'
    if arrows:
        for (px, py), s in ((b, 1), (a, -1)):
            hx, hy = px - s * ux * 16, py - s * uy * 16
            nx, ny = -uy * 8, ux * 8
            out += f'<polygon points="{px:.1f},{py:.1f} {hx+nx:.1f},{hy+ny:.1f} {hx-nx:.1f},{hy-ny:.1f}" fill="{col}"/>'
    return out


def ray(ox, oy, tx, ty, col, w=7):
    """a half-line from its origin (dot) through the direction of (tx, ty), with an arrowhead"""
    dx, dy = tx - ox, ty - oy
    L = math.hypot(dx, dy) or 1
    ux, uy = dx / L, dy / L
    hx, hy = tx - ux * 18, ty - uy * 18
    nx, ny = -uy * 10, ux * 10
    return (f'<line x1="{ox:.1f}" y1="{oy:.1f}" x2="{hx:.1f}" y2="{hy:.1f}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>'
            f'<polygon points="{tx:.1f},{ty:.1f} {hx+nx:.1f},{hy+ny:.1f} {hx-nx:.1f},{hy-ny:.1f}" fill="{col}"/>')


# ================================================================== real objects
def box3d(x, y, w, h, d, base='#c9955c', i=None):
    """a cardboard box (rectangular prism) with its tape; (x, y) is the front-bottom-left corner"""
    i = i or uid('bx')
    dx, dy = d * .8, -d * .5
    front = [(x, y), (x + w, y), (x + w, y - h), (x, y - h)]
    top = [(x, y - h), (x + w, y - h), (x + w + dx, y - h + dy), (x + dx, y - h + dy)]
    side = [(x + w, y), (x + w + dx, y + dy), (x + w + dx, y - h + dy), (x + w, y - h)]
    defs = lg(i + 'f', [(0, '#d9a96f'), (1, '#b98448')], 0, 0, 0, 1) + lg(i + 't', [(0, '#f0c58c'), (1, '#dcae74')], 0, 0, 1, 1) + lg(i + 's', [(0, '#a8763d'), (1, '#8d6130')], 0, 0, 1, 1)
    b = f'<ellipse cx="{x + w/2 + dx/2:.0f}" cy="{y + 14:.0f}" rx="{w * .8:.0f}" ry="14" fill="#000" opacity=".16"/>'
    b += poly(front, f'url(#{i}f)', '#7a5224', 2) + poly(side, f'url(#{i}s)', '#7a5224', 2) + poly(top, f'url(#{i}t)', '#7a5224', 2)
    # packing tape across the top and down the front
    tw = w * .16
    b += poly([(x + w/2 - tw/2, y - h), (x + w/2 + tw/2, y - h), (x + w/2 + tw/2 + dx, y - h + dy), (x + w/2 - tw/2 + dx, y - h + dy)], '#e8d9b0', '#b5a06a', 1)
    b += poly([(x + w/2 - tw/2, y - h), (x + w/2 + tw/2, y - h), (x + w/2 + tw/2, y - h*.7), (x + w/2 - tw/2, y - h*.7)], '#e8d9b0', '#b5a06a', 1)
    return b, defs


def can3d(cx, y, rx, h, i=None, body=('#c9ccd1', '#f5f6f8', '#9aa0a8'), band='#d9480f'):
    """a tin can (cylinder); (cx, y) is the centre of the bottom ellipse"""
    i = i or uid('cn')
    ry = rx * .32
    defs = lg(i + 'b', [(0, body[2]), (.3, body[1]), (.55, body[0]), (1, body[2])]) + rg(i + 't', [(0, '#ffffff'), (1, '#c8ccd2')], .45, .4, .8)
    b = f'<ellipse cx="{cx}" cy="{y + ry*.5:.0f}" rx="{rx * 1.1:.0f}" ry="{ry*.9:.0f}" fill="#000" opacity=".16"/>'
    b += f'<path d="M {cx-rx} {y-h} L {cx-rx} {y} A {rx} {ry} 0 0 0 {cx+rx} {y} L {cx+rx} {y-h} Z" fill="url(#{i}b)" stroke="#7b828b" stroke-width="2"/>'
    b += f'<path d="M {cx-rx} {y-h*.62} L {cx-rx} {y-h*.28} A {rx} {ry} 0 0 0 {cx+rx} {y-h*.28} L {cx+rx} {y-h*.62} A {rx} {ry} 0 0 1 {cx-rx} {y-h*.62} Z" fill="{band}" opacity=".9"/>'
    b += f'<ellipse cx="{cx}" cy="{y-h}" rx="{rx}" ry="{ry}" fill="url(#{i}t)" stroke="#7b828b" stroke-width="2"/>'
    b += f'<ellipse cx="{cx}" cy="{y-h}" rx="{rx*.78:.0f}" ry="{ry*.78:.0f}" fill="none" stroke="#9aa0a8" stroke-width="1.5"/>'
    return b, defs


def pyramid3d(cx, y, w, h, i=None):
    """a square pyramid on sand-coloured stone"""
    i = i or uid('py')
    hw, dp = w / 2, w * .22
    A, B, C, Dd = (cx - hw, y), (cx + hw * .8, y + dp * .5), (cx + hw, y - dp * .3), (cx - hw * .15, y - dp)   # base corners: front-left, front-right..., see below
    apex = (cx + hw * .08, y - h)
    # visible faces: front-left face (A, B, apex) and right face (B, C, apex)
    defs = lg(i + 'a', [(0, '#f0cf8a'), (1, '#d9ae5e')], 0, 0, 1, 1) + lg(i + 'c', [(0, '#c99a4b'), (1, '#a67a32')], 0, 0, 1, 1)
    b = f'<ellipse cx="{cx + 20}" cy="{y + dp*.5 + 12:.0f}" rx="{w * .62:.0f}" ry="16" fill="#000" opacity=".15"/>'
    b += poly([A, B, apex], f'url(#{i}a)', '#8a6420', 2) + poly([B, C, apex], f'url(#{i}c)', '#8a6420', 2)
    for k in range(1, 6):                                                # courses of stone
        t = k / 6
        for (P, Q) in ((A, apex), (B, apex), (C, apex)):
            pass
        pl, pr = (A[0] + (apex[0] - A[0]) * t, A[1] + (apex[1] - A[1]) * t), (B[0] + (apex[0] - B[0]) * t, B[1] + (apex[1] - B[1]) * t)
        b += f'<line x1="{pl[0]:.1f}" y1="{pl[1]:.1f}" x2="{pr[0]:.1f}" y2="{pr[1]:.1f}" stroke="#b48a3e" stroke-width="1.2" opacity=".6"/>'
        ql, qr = pr, (C[0] + (apex[0] - C[0]) * t, C[1] + (apex[1] - C[1]) * t)
        b += f'<line x1="{ql[0]:.1f}" y1="{ql[1]:.1f}" x2="{qr[0]:.1f}" y2="{qr[1]:.1f}" stroke="#8d6a2c" stroke-width="1.2" opacity=".6"/>'
    return b, defs


def solids():
    """slide 1.1: a box, a tin can and a pyramid: solid shapes of everyday life"""
    b1, d1 = box3d(60, 330, 200, 130, 120)
    b2, d2 = can3d(520, 330, 95, 200)
    b3, d3 = pyramid3d(790, 330, 230, 230)
    body = b1 + b2 + b3
    body += T(180, 400, 'ប្រលេពីប៉ែតកែង', 34, NAVY) + T(520, 400, 'ស៊ីឡាំង', 34, NAVY) + T(800, 400, 'ពីរ៉ាមីត', 34, NAVY)
    return svgd(1000, 430, body, '52vh', d1 + d2 + d3)


# ------------------------------------------------------------------ points
def point_notations():
    """the four ways the book writes a point: a dot A, a cross B, a dot H on a curve, a dot C on a line"""
    b = dot(120, 120, NAVY, 10) + lab(150, 100, 'A', NAVY, 44, 'start')
    b += line(330, 100, 370, 140, NAVY, 5) + line(370, 100, 330, 140, NAVY, 5) + lab(396, 100, 'B', NAVY, 44, 'start')
    b += f'<path d="M 540 150 Q 600 60 700 120" fill="none" stroke="{NAVY}" stroke-width="4"/>' + dot(612, 100, RED, 10) + lab(612, 66, 'H', RED, 44)
    b += line(780, 120, 960, 120, NAVY, 4) + dot(870, 120, GREEN, 10) + lab(870, 90, 'C', GREEN, 44)
    return svgd(1000, 190, b, '28vh')


def pencil_dot():
    """a sharp pencil tip touching paper leaves a mark: a point (shaded illustration)"""
    i = uid('pc')
    defs = lg(i + 'w', [(0, '#f6d9a8'), (1, '#d9b27a')], 0, 0, 0, 1) + lg(i + 'y', [(0, '#ffe066'), (.5, '#ffd43b'), (1, '#e8a900')], 0, 0, 0, 1)
    b = poly([(80, 330), (860, 330), (940, 250), (160, 250)], '#fff', '#c9ced6', 2) + poly([(80, 330), (860, 330), (860, 342), (80, 342)], '#d5dbe3')   # sheet of paper
    # pencil, tip at (520, 262), leaning to the upper right
    ang = math.radians(-62)
    def P(u, v):
        ca, sa = math.cos(ang), math.sin(ang)
        return (520 + u * ca - v * sa, 292 + u * sa + v * ca)
    cone = [P(0, 0), P(70, -22), P(70, 22)]
    body = [P(70, -22), P(250, -22), P(250, 22), P(70, 22)]
    b += poly(body, f'url(#{i}y)', '#a87a00', 2) + poly(cone, f'url(#{i}w)', '#a88255', 2)
    b += poly([P(0, 0), P(24, -8), P(24, 8)], '#3b3b3b')
    b += poly([P(250, -22), P(292, -22), P(292, 22), P(250, 22)], '#e8a0a8', '#b86070', 2)
    b += dot(520, 292, '#111', 6)
    b += rvg(1, arrow(720, 190, 548, 280, RED, 5) + T(730, 176, 'ស្នាមចុច = ចំណុច', 34, RED, 'start'))
    return svgd(1000, 340, b, '44vh', defs)


def night_sky_dot():
    b = f'<rect x="40" y="10" width="920" height="250" rx="22" fill="#0d2447"/>'
    import random
    rr = random.Random(12)
    for _ in range(46):
        b += f'<circle cx="{rr.randint(70,930)}" cy="{rr.randint(30,240)}" r="{rr.choice([1.5,2,2.5,3])}" fill="#fff" opacity="{rr.choice([.5,.7,.9])}"/>'
    b += rvg(1, f'<circle cx="500" cy="120" r="34" fill="#ffd43b" opacity=".18"/><circle cx="500" cy="120" r="10" fill="#fff6bf"/>' + T(500, 200, 'ផ្កាយនៅលើមេឃ', 32, '#ffe9a8'))
    return svgd(1000, 270, b, '34vh')


# ------------------------------------------------------------------ the 6 flowers on 4 rows of 3
def _isect(l1, l2):
    (a, b), (c, d) = l1, l2
    x1, y1 = a
    x2, y2 = b
    x3, y3 = c
    x4, y4 = d
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / den
    py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / den
    return px, py


FLOWER_LINES = [((150, 330), (550, 330)), ((330, 60), (470, 360)), ((390, 40), (210, 360)), ((90, 90), (600, 330))]   # 4 lines, 6 crossing points, 3 on each line (checked below)


def flower_points():
    pts = {}
    for (i, j) in ((0, 1), (0, 2), (1, 2), (0, 3), (1, 3), (2, 3)):
        pts[(i, j)] = _isect(FLOWER_LINES[i], FLOWER_LINES[j])
    return pts


def flower(x, y, col='#e64980'):
    b = ''
    for k in range(6):
        a = k * math.pi / 3
        b += f'<circle cx="{x + 13*math.cos(a):.1f}" cy="{y + 13*math.sin(a):.1f}" r="9" fill="{col}" stroke="#a61e4d" stroke-width="1"/>'
    return b + f'<circle cx="{x}" cy="{y}" r="7" fill="#ffd43b" stroke="#e8a900" stroke-width="1"/>'


def flower_lines():
    pts = flower_points()
    # every line must carry exactly 3 of the 6 points (the book's 4 rows of 3), and the 6 points must be distinct
    for li in range(4):
        assert sum(1 for k in pts if li in k) == 3
    assert len({(round(x), round(y)) for x, y in pts.values()}) == 6
    names = dict(zip(sorted(pts), 'ABCDEF'))
    body = ''
    cols = [BLUE, GREEN, ORANGE, PURPLE]
    for li, (a, b_) in enumerate(FLOWER_LINES):
        body += rvg(li + 1, dline(a[0], a[1], b_[0], b_[1], cols[li], 4, True, 40))
    for k, (x, y) in pts.items():
        body += rvg(5, flower(x, y) + lab(x + 28, y - 16, names[k], NAVY, 34, 'start'))
    return svgd(720, 440, f'<g transform="translate(0 30)">{body}</g>', '56vh'), names, pts


# ------------------------------------------------------------------ lines
def ruler_pencil_line():
    """a ruler and a pencil: moving the pencil tip along the ruler draws a straight line d"""
    i = uid('rl')
    defs = lg(i + 'r', [(0, '#fff3bf'), (1, '#f1d570')], 0, 0, 0, 1) + lg(i + 'y', [(0, '#ffe066'), (.5, '#ffd43b'), (1, '#e8a900')], 0, 0, 0, 1)
    b = poly([(40, 250), (960, 250), (960, 300), (40, 300)], '#fff', '#c9ced6', 2)                # paper
    b += poly([(120, 120), (900, 120), (900, 176), (120, 176)], f'url(#{i}r)', '#b08d1a', 2)       # ruler
    for k in range(0, 79):
        x = 130 + k * 10
        h = 22 if k % 10 == 0 else 14 if k % 5 == 0 else 8
        b += f'<line x1="{x}" y1="120" x2="{x}" y2="{120 + h}" stroke="#5c4a00" stroke-width="1.4"/>'
        if k % 10 == 0:
            b += M(x, 160, k // 10, 18, '#5c4a00', 'middle', 600)
    b += line(150, 188, 640, 188, NAVY, 5)                                                         # the drawn line
    b += poly([(640, 188), (680, 150), (700, 164), (656, 196)], '#e9d4a8', '#9c7a3c', 1.5) + poly([(680, 150), (790, 40), (812, 64), (700, 164)], f'url(#{i}y)', '#a87a00', 2) + poly([(640, 188), (652, 183), (656, 196)], '#333')
    b += lab(812, 205, 'd', RED, 44) if False else ''
    b += lab(180, 222, '(d)', RED, 40, 'start')
    return svgd(1000, 330, b, '44vh', defs)


def string_tight():
    """two pins A and B and two threads of different colour, pulled tight: they lie on each other (one line through A and B)"""
    i = uid('st')
    defs = rg(i + 'p', [(0, '#fff'), (.5, '#c0c6cf'), (1, '#6b7280')], .35, .3, .8) + lg(i + 'w', [(0, '#d9a066'), (1, '#b97a3c')], 0, 0, 0, 1)
    b = poly([(40, 60), (960, 60), (960, 290), (40, 290)], f'url(#{i}w)', '#7a5224', 3)            # wooden board
    A, B = (210, 190), (790, 190)
    b += f'<path d="M {A[0]} {A[1]} Q 500 {250} {B[0]} {B[1]}" fill="none" stroke="{RED}" stroke-width="6"/>'                                  # slack red thread
    b += rvg(0, f'<path d="M {A[0]} {A[1]} Q 500 130 {B[0]} {B[1]}" fill="none" stroke="{BLUE}" stroke-width="6"/>', until=1)               # slack blue thread
    b += rvg(1, line(A[0], A[1], B[0], B[1], BLUE, 6) + line(A[0], A[1] + 1, B[0], B[1] + 1, RED, 6))                                         # pulled tight: both lie on one line
    b = b.replace(f'<path d="M {A[0]} {A[1]} Q 500 250 {B[0]} {B[1]}" fill="none" stroke="{RED}" stroke-width="6"/>', rvg(0, f'<path d="M {A[0]} {A[1]} Q 500 250 {B[0]} {B[1]}" fill="none" stroke="{RED}" stroke-width="6"/>', until=1))
    for P, nm in ((A, 'A'), (B, 'B')):
        b += f'<circle cx="{P[0]}" cy="{P[1]}" r="17" fill="url(#{i}p)" stroke="#4b5563" stroke-width="2"/>' + lab(P[0], P[1] - 34, nm, NAVY, 42)
    b += rvg(1, arrow(120, 120, 70, 120, GREY, 5) + arrow(880, 120, 930, 120, GREY, 5) + T(500, 250, 'ខ្សែអំបោះត្រួតស៊ីគ្នា', 32, NAVY))
    return svgd(1000, 320, b, '44vh', defs)


def line_with_points(on, above=None, below=None, name='d', lo=80, hi=920, y=170, xs=None):
    """a line `name` through the points in `on` (left to right); `above` / `below` are points off the line"""
    n = len(on)
    xs = xs or [lo + 60 + k * (hi - lo - 120) / (n - 1) for k in range(n)]
    b = dline(lo - 20, y, hi + 20, y, NAVY, 5, True) + lab(hi - 10, y + 54, name, RED, 40)
    for nm, x in zip(on, xs):
        b += dot(x, y, BLUE, 10) + lab(x, y + 56, nm, NAVY, 38)
    for nm, k in (above or {}).items():
        b += dot(xs[k], y - 100, ORANGE, 10) + lab(xs[k] + 30, y - 100, nm, ORANGE, 38, 'start')
    for nm, k in (below or {}).items():
        b += dot(xs[k], y + 110, GREEN, 10) + lab(xs[k] + 30, y + 118, nm, GREEN, 38, 'start')
    return svgd(1000, 300, b, '40vh')


# ------------------------------------------------------------------ rays
def ray_pair(M_label='M', left='x', right='y', step=True):
    y = 150
    xm = 500
    b = dline(60, y, 940, y, GREY, 3, False)
    b += rvg(1, ray(xm, y, 90, y, ORANGE) + lab(70, y - 26, left, ORANGE, 40) + T(250, y + 70, 'កន្លះបន្ទាត់ ' + '', 28, ORANGE))
    b += rvg(2, ray(xm, y, 910, y, GREEN) + lab(930, y - 26, right, GREEN, 40))
    b += dot(xm, y, NAVY, 11) + lab(xm, y + 56, M_label, NAVY, 40)
    b += rvg(1, lab(280, y - 24, M_label + left, ORANGE, 36)) + rvg(2, lab(720, y - 24, M_label + right, GREEN, 36))
    return svgd(1000, 230, b, '34vh')


def rays_two_points(p='A', q='D', x='x', y_='y'):
    """x, A, D, y on a line: A and D each cut the line into two rays; the four rays Ax Ay Dx Dy"""
    y = 190
    xa, xd = 360, 640
    b = dline(60, y, 940, y, GREY, 3, False) + lab(60, y + 54, x, NAVY, 38) + lab(940, y + 54, y_, NAVY, 38)
    b += rvg(1, ray(xa, y - 12, 80, y - 12, ORANGE, 6) + lab(210, y - 38, p + x, ORANGE, 34))
    b += rvg(2, ray(xa, y - 12, 920, y - 12, GREEN, 6) + lab(560, y - 38, p + y_, GREEN, 34))
    b += rvg(3, ray(xd, y + 14, 80, y + 14, PURPLE, 6) + lab(210, y + 56, q + x, PURPLE, 34))
    b += rvg(4, ray(xd, y + 14, 920, y + 14, RED, 6) + lab(800, y + 56, q + y_, RED, 34))
    b += dot(xa, y, NAVY, 10) + lab(xa, y + 100, p, NAVY, 38) + dot(xd, y, NAVY, 10) + lab(xd, y + 100, q, NAVY, 38)
    return svgd(1000, 310, b, '40vh')


def crossing_lines():
    """lines AB and EF cross at O: O is the origin of four rays OA, OB, OE, OF (O lies exactly between A and B, and between E and F)"""
    O = (500, 190)
    ux, uy = 0.96, 0.2
    vx, vy = 0.8, -0.6
    A, B = (O[0] - 340 * ux, O[1] - 340 * uy), (O[0] + 340 * ux, O[1] + 340 * uy)
    E, F = (O[0] - 220 * vx, O[1] - 220 * vy), (O[0] + 220 * vx, O[1] + 220 * vy)
    b = dline(A[0], A[1], B[0], B[1], GREY, 3, False) + dline(E[0], E[1], F[0], F[1], GREY, 3, False)
    for k, (nm, P, col, lx, ly) in enumerate((('A', A, ORANGE, -26, -14), ('B', B, GREEN, 18, 8), ('E', E, PURPLE, -14, 34), ('F', F, RED, 12, -8))):
        mid = ((O[0] + P[0]) / 2, (O[1] + P[1]) / 2)
        dxr, dyr = P[0] - O[0], P[1] - O[1]
        ln = math.hypot(dxr, dyr)
        nx, ny = -dyr / ln * 30, dxr / ln * 30                  # a step to the side of the ray, so the name never lies on it
        b += rvg(k + 1, ray(O[0], O[1], P[0], P[1], col, 6) + lab(P[0] + lx, P[1] + ly, nm, col, 40) + lab(mid[0] + nx, mid[1] + ny + 10, 'O' + nm, col, 30))
    b += dot(O[0], O[1], NAVY, 11) + lab(O[0] + 4, O[1] + 46, 'O', NAVY, 40)
    return svgd(1000, 380, b, '46vh')


def eight_rays():
    """A, B, C, D on a line: every point is the origin of two rays (one row of two arrows per point): 4 x 2 = 8"""
    y = 70
    xs = [200, 400, 600, 800]
    b = dline(60, y, 940, y, GREY, 4, False)
    cols = [ORANGE, GREEN, PURPLE, RED]
    for k, (nm, x) in enumerate(zip('ABCD', xs)):
        ry = 140 + k * 44
        b += dot(x, y, NAVY, 10) + lab(x, y - 24, nm, NAVY, 38)
        b += rvg(k + 1, line(x, y + 10, x, ry, cols[k], 2, '4 5') + ray(x, ry, 80, ry, cols[k], 6) + ray(x, ry, 920, ry, cols[k], 6)
                 + lab(x - 56, ry - 10, nm + 'x', cols[k], 28) + lab(x + 56, ry - 10, nm + 'y', cols[k], 28))
    b += rvg(5, T(500, 352, '4 × 2 = 8 កន្លះបន្ទាត់', 40, NAVY))
    return svgd(1000, 380, b, '46vh')


# ------------------------------------------------------------------ planes
def _par(x, y, w, h, sk=70):
    """a plane drawn as a parallelogram: (x, y) is the bottom-left corner"""
    return [(x, y), (x + w, y), (x + w + sk, y - h), (x + sk, y - h)]


def plane_with_line():
    i = uid('pl')
    defs = lg(i, [(0, '#dbe9ff'), (1, '#b6d0f5')], 0, 0, 1, 1)
    P = _par(130, 280, 600, 190, 90)
    b = poly(P, f'url(#{i})', BLUE, 3) + lab(780, 100, 'P', BLUE, 46)
    d = ((250, 220), (640, 150))
    b += line(d[0][0], d[0][1], d[1][0], d[1][1], RED, 5) + lab(660, 140, 'd', RED, 40)
    m = (450, 186)
    b += dot(m[0], m[1], NAVY, 10) + lab(m[0], m[1] - 22, 'M', NAVY, 38)
    b += rvg(1, T(500, 330, 'M ∈ d ⟹ M ∈ P', 38, NAVY).replace('font-weight="700"', 'font-weight="700" font-style="italic"'))
    return svgd(1000, 350, b, '46vh', defs)


def plane_half_planes():
    i1, i2 = uid('h1'), uid('h2')
    defs = lg(i1, [(0, '#ffe3e3'), (1, '#ffc9c9')], 0, 0, 1, 1) + lg(i2, [(0, '#d3f9d8'), (1, '#b2f2bb')], 0, 0, 1, 1)
    # the plane P with the line xy dividing it in two (the line runs from the front edge to the back edge)
    sk, w, h, x0, y0 = 90, 640, 200, 130, 290
    fx, bx = x0 + w * .45, x0 + sk + w * .55                       # where the line meets the front and the back edge
    left = [(x0, y0), (fx, y0), (bx, y0 - h), (x0 + sk, y0 - h)]
    right = [(fx, y0), (x0 + w, y0), (x0 + w + sk, y0 - h), (bx, y0 - h)]
    b = poly(left, f'url(#{i1})', '#c2255c', 2) + poly(right, f'url(#{i2})', '#2b8a3e', 2)
    b += dline(fx - 20, y0 + 34, bx + 20, y0 - h - 34, NAVY, 5, True) + lab(fx - 36, y0 + 64, 'x', NAVY, 40) + lab(bx + 44, y0 - h - 30, 'y', NAVY, 40)
    b += lab(240, 190, '(I)', '#c2255c', 52) + lab(640, 190, '(II)', '#2b8a3e', 52) + lab(810, 80, 'P', BLUE, 46)
    return svgd(1000, 430, f'<g transform="translate(0 30)">{b}</g>', '48vh', defs)


def plane_SABC(step_planes=True):
    """a point S above the plane P and three points A, B, C of P (not on one line); the three new planes SAB, SBC, SAC"""
    # 3D coordinates (x right, y away, z up); the oblique view puts the back (y big) up and to the right
    A, B, C, S = (0, 0, 0), (420, 0, 0), (300, 190, 0), (160, 70, 250)
    def pr(p):
        x, y, z = p
        return (170 + x + y * 0.55, 330 - y * 0.42 - z)
    a, b_, c, s = pr(A), pr(B), pr(C), pr(S)
    i = uid('sp')
    defs = lg(i, [(0, '#dbe9ff'), (1, '#b6d0f5')], 0, 0, 1, 1)
    plane = [pr((-80, -60, 0)), pr((560, -60, 0)), pr((560 + 90, 300, 0)), pr((-80 + 90, 300, 0))]
    body = poly(plane, f'url(#{i})', BLUE, 3) + lab(plane[0][0] + 24, plane[0][1] - 14, 'P', BLUE, 44, 'start')
    faces = [('SAB', (s, a, b_), '#ff8787'), ('SBC', (s, b_, c), '#69db7c'), ('SAC', (s, a, c), '#ffd43b')]
    for k, (nm, tri, col) in enumerate(faces):
        body += rvg(k + 2, poly(list(tri), col, NAVY, 2, 'fill-opacity=".45"'))
    # edges: AB and BC in front of the plane are solid; AC and the base triangle are all in P, so draw the triangle solid
    body += line(a[0], a[1], b_[0], b_[1], NAVY, 4) + line(b_[0], b_[1], c[0], c[1], NAVY, 4) + line(a[0], a[1], c[0], c[1], NAVY, 4)
    for q in (a, b_, c):
        body += line(s[0], s[1], q[0], q[1], NAVY, 4)
    for nm, q, dx, dy in (('A', a, -26, 12), ('B', b_, 20, 12), ('C', c, 18, -10), ('S', s, 0, -20)):
        body += dot(q[0], q[1], RED if nm == 'S' else BLUE, 9) + lab(q[0] + dx, q[1] + dy, nm, NAVY, 38)
    for k, (nm, tri, col) in enumerate(faces):
        body += rvg(k + 2, lab(780, 120 + k * 56, 'ប្លង់ ' + nm, '#7d4f00' if col == '#ffd43b' else NAVY, 34, 'start'), until=None) if False else ''
    body += rvg(2, TM(760, 90, 'ប្លង់', 'SAB', 34, '#c92a2a', 'start')) + rvg(3, TM(760, 140, 'ប្លង់', 'SBC', 34, '#2b8a3e', 'start')) + rvg(4, TM(760, 190, 'ប្លង់', 'SAC', 34, '#a66c00', 'start'))
    return svgd(1000, 380, body, '48vh', defs)


def surfaces_room():
    """everyday planes: table top, wall, whiteboard, water; the sheet slides on the table and always covers itself"""
    i = uid('rm')
    defs = lg(i + 't', [(0, '#b5753a'), (1, '#8c5524')], 0, 0, 0, 1) + lg(i + 'w', [(0, '#e7f5ff'), (1, '#c5e1f5')], 0, 0, 0, 1) + lg(i + 'b', [(0, '#ffffff'), (1, '#e9ecef')], 0, 0, 1, 1) + lg(i + 'a', [(0, '#74c0fc'), (1, '#1c7ed6')], 0, 0, 0, 1)
    b = f'<rect x="30" y="20" width="940" height="300" rx="18" fill="url(#{i}w)"/>'
    b += poly([(80, 90), (330, 90), (330, 200), (80, 200)], f'url(#{i}b)', '#8d99a6', 5) + f'<rect x="80" y="200" width="250" height="10" fill="#6b7785"/>' + ''.join(f'<path d="M {110} {120 + j*26} h {120 + (j%2)*50}" stroke="#4263eb" stroke-width="3" opacity=".55" stroke-linecap="round"/>' for j in range(3)) + T(205, 260, 'ក្តារខៀន', 28, NAVY)
    b += ''.join(poly(q, '#6b3f16') for q in ([(410, 252), (424, 252), (424, 296), (410, 296)], [(676, 252), (690, 252), (690, 296), (676, 296)], [(500, 200), (512, 200), (512, 232), (500, 232)], [(740, 200), (752, 200), (752, 232), (740, 232)]))
    b += poly([(400, 250), (700, 250), (760, 200), (460, 200)], f'url(#{i}t)', '#6b3f16', 3) + T(580, 316, 'ផ្ទៃតុ', 28, NAVY)
    b += rvg(1, poly([(470, 238), (560, 238), (600, 206), (510, 206)], '#fff', '#adb5bd', 2) + arrow(540, 222, 640, 222, RED, 4))
    b += f'<rect x="790" y="140" width="150" height="90" rx="8" fill="url(#{i}a)"/>' + ''.join(f'<path d="M {800 + k*10} {160 + j*24} q 14 -6 28 0 t 28 0" fill="none" stroke="#fff" stroke-width="2" opacity=".55"/>' for j in range(3) for k in (0, 5)) + T(865, 260, 'ផ្ទៃទឹក', 28, NAVY)
    return svgd(1000, 330, b, '44vh', defs)


PREVIEW = ['solids', 'point_notations', 'pencil_dot', 'night_sky_dot', 'flower_lines', 'ruler_pencil_line', 'string_tight', 'ray_pair', 'rays_two_points', 'crossing_lines', 'eight_rays',
           'plane_with_line', 'plane_half_planes', 'plane_SABC', 'surfaces_room']
