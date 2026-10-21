# Lesson 12 pictures, part 2: segments (ruler, compass, sums and differences), the road and runners, and the exercise figures.
# Lengths in the pictures are to scale: every segment is placed with a unit scale and the numbers on it are asserted.
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from vis12a import *
from vis12a import _par, _isect
import itertools


def seg(x1, x2, y, col=NAVY, w=8, ends=True):
    b = f'<line x1="{x1:.1f}" y1="{y}" x2="{x2:.1f}" y2="{y}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>'
    if ends:
        b += dot(x1, y, col, 9) + dot(x2, y, col, 9)
    return b


def tick(x, y, col=NAVY, h=16, w=3):
    return f'<line x1="{x:.1f}" y1="{y-h}" x2="{x:.1f}" y2="{y+h}" stroke="{col}" stroke-width="{w}"/>'


def dim(x1, x2, y, text, col=NAVY, size=30, up=True):
    """a dimension bar with end ticks and a label: the length of a segment"""
    ty = y - 14 if up else y + 38
    return (f'<line x1="{x1:.1f}" y1="{y}" x2="{x2:.1f}" y2="{y}" stroke="{col}" stroke-width="4"/>' + tick(x1, y, col, 10, 4) + tick(x2, y, col, 10, 4)
            + M((x1 + x2) / 2, ty, text, size, col, 'middle', 600))


def at(x, y, name, col=NAVY, below=True, size=36):
    return dot(x, y, col, 9) + lab(x, y + (50 if below else -22), name, col, size)


# ================================================================== 2.1 constructing a segment
def segment_MN():
    y = 130
    b = dline(60, y, 940, y, GREY, 4, True) + lab(910, y + 56, 'l', GREY, 40)
    b += rvg(1, seg(300, 700, y, BLUE, 10, False) + at(300, y, 'M', BLUE) + at(700, y, 'N', BLUE) + lab(500, y - 26, 'MN', BLUE, 40))
    b += rvg(2, T(300, y + 130, 'ចុងអង្កត់ M', 28, BLUE, 'middle') + T(700, y + 130, 'ចុងអង្កត់ N', 28, BLUE, 'middle'))
    b += rvg(3, T(150, y - 40, 'ទម្រ', 30, GREY, 'middle') + arrow(150, y - 30, 150, y - 4, GREY, 3))
    return svgd(1000, 290, b, '40vh')


def ruler_measure(length_cm=8, total=10):
    """a ruler 0..10 cm: A is at 0 and B at 8: AB = 8 cm (millimetre ticks are exact)"""
    sc, x0, ry = 84, 80, 170                           # 84 px per cm
    i = uid('rm')
    defs = lg(i, [(0, '#fff3bf'), (1, '#f1d570')], 0, 0, 0, 1)
    X = lambda cm: x0 + cm * sc
    b = poly([(X(-.4), ry), (X(total + .4), ry), (X(total + .4), ry + 70), (X(-.4), ry + 70)], f'url(#{i})', '#b08d1a', 2)
    for mm in range(0, total * 10 + 1):
        x = X(mm / 10)
        h = 30 if mm % 10 == 0 else 20 if mm % 5 == 0 else 12
        b += f'<line x1="{x:.1f}" y1="{ry}" x2="{x:.1f}" y2="{ry + h}" stroke="#4a3b00" stroke-width="{2 if mm % 10 == 0 else 1.2}"/>'
        if mm % 10 == 0:
            b += M(x, ry + 58, mm // 10, 24, '#4a3b00', 'middle', 600)
    b += M(X(total + .1), ry + 84, 'cm', 22, '#4a3b00', 'end', 600)
    y = 100
    xa, xb = X(0), X(length_cm)
    b += f'<line x1="{xa}" y1="{y + 8}" x2="{xa}" y2="{ry}" stroke="{ORANGE}" stroke-width="2" stroke-dasharray="5 4"/><line x1="{xb}" y1="{y + 8}" x2="{xb}" y2="{ry + 30}" stroke="{ORANGE}" stroke-width="2" stroke-dasharray="5 4"/>'
    b += seg(xa, xb, y, BLUE, 8) + lab(xa, y - 24, 'A', BLUE, 40) + lab(xb, y - 24, 'B', BLUE, 40)
    b += rvg(1, M((xa + xb) / 2, y - 34, f'AB = {length_cm} cm', 40, RED, 'middle', 700))
    return svgd(1000, 290, b, '40vh', defs)


def _leg(h, f, col1, col2, w=11):
    """one leg of the compass from the hinge h to the foot f (a thin tapered metal bar)"""
    dx, dy = f[0] - h[0], f[1] - h[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L * w / 2, dx / L * w / 2
    return poly([(h[0] + nx, h[1] + ny), (f[0] + nx * .2, f[1] + ny * .2), (f[0] - nx * .2, f[1] - ny * .2), (h[0] - nx, h[1] - ny)], col1, col2, 1.5)


def compass(left_foot, opening, h=190, pencil_right=True):
    """a drawing compass: needle foot at left_foot, pencil foot `opening` px to the right, both on the same horizontal line"""
    lx, ly = left_foot
    rx = lx + opening
    hx, hy = lx + opening / 2, ly - h
    b = _leg((hx, hy), (lx, ly), '#aeb5be', '#6b7280') + _leg((hx, hy), (rx, ly), '#aeb5be', '#6b7280')
    b += poly([(lx - 3, ly), (lx + 3, ly), (lx, ly + 16)], '#444')                                        # steel needle
    b += poly([(rx - 8, ly - 26), (rx + 8, ly - 26), (rx + 2, ly + 2), (rx - 2, ly + 2)], '#ffd43b', '#a87a00', 1.5) + poly([(rx - 2, ly), (rx + 2, ly), (rx, ly + 12)], '#222')
    b += f'<circle cx="{hx}" cy="{hy}" r="13" fill="#868e96" stroke="#495057" stroke-width="2"/><rect x="{hx - 5}" y="{hy - 46}" width="10" height="36" rx="4" fill="#adb5bd" stroke="#6b7280" stroke-width="1.5"/>'
    return b


def compass_transfer():
    """the book's three steps: (1) open the compass to AB, (2) put the needle on A' of line xy, (3) mark B' with the pencil foot"""
    L = 190
    b = ''
    # panel 1: the segment AB and the compass opened to its length
    y1 = 270
    b += seg(60, 60 + L, y1, BLUE, 7) + lab(60, y1 + 54, 'A', BLUE, 36) + lab(60 + L, y1 + 54, 'B', BLUE, 36) + compass((60, y1), L, 170)
    b += lab(160, 360, '(1)', RED, 34)
    # panel 2: the line xy, A' marked, the compass needle on A'
    px = 380
    b += dline(px - 30, y1, px + 280, y1, GREY, 4, False) + lab(px - 24, y1 + 50, 'x', GREY, 34) + lab(px + 276, y1 + 50, 'y', GREY, 34)
    b += dot(px + 20, y1, BLUE, 9) + lab(px + 20, y1 + 54, "A'", BLUE, 36) + compass((px + 20, y1), L, 170)
    b += lab(px + 120, 360, '(2)', RED, 34)
    # panel 3: the pencil foot marks B' on xy; A'B' = AB
    qx = 710
    b += dline(qx - 30, y1, qx + 280, y1, GREY, 4, False) + lab(qx - 24, y1 + 50, 'x', GREY, 34) + lab(qx + 276, y1 + 50, 'y', GREY, 34)
    b += seg(qx + 20, qx + 20 + L, y1, GREEN, 7) + lab(qx + 20, y1 + 54, "A'", GREEN, 36) + lab(qx + 20 + L, y1 + 54, "B'", GREEN, 36)
    b += f'<path d="M {qx + 20 + L} {y1 - 24} Q {qx + 20 + L + 10} {y1} {qx + 20 + L} {y1 + 24}" fill="none" stroke="#222" stroke-width="3"/>' + lab(qx + 130, 360, '(3)', RED, 34)
    return svgd(1000, 380, b, '48vh')


def polygons_segments():
    """points 2, 3, 4, 5 joined two by two: 1, 3, 6 and 10 segments"""
    def reg(n, cx, cy, r, rot=-90):
        return [(cx + r * math.cos(math.radians(rot + k * 360 / n)), cy + r * math.sin(math.radians(rot + k * 360 / n))) for k in range(n)]
    b = ''
    cols = [BLUE, GREEN, ORANGE, RED]
    for k, n in enumerate((2, 3, 4, 5)):
        cx, cy = 130 + k * 245, 150
        pts = reg(n, cx, cy, 90, -90 if n != 4 else -45) if n > 2 else [(cx - 80, cy), (cx + 80, cy)]
        edges = list(itertools.combinations(range(n), 2))
        assert len(edges) == n * (n - 1) // 2 == [1, 3, 6, 10][k]
        g = ''.join(line(pts[i][0], pts[i][1], pts[j][0], pts[j][1], cols[k], 4) for i, j in edges)
        g += ''.join(dot(x, y, NAVY, 8) + M(x + (x - cx) * .28 + (0 if n > 2 else (-18 if x < cx else 18)), y + (y - cy) * .28 + 12, i + 1, 28, NAVY, 'middle', 600) for i, (x, y) in enumerate(pts))
        b += rvg(k + 1, g + M(cx, 300, f'{n} ចំណុច → {len(edges)} អង្កត់'.replace(' ចំណុច', ''), 1, NAVY) if False else g + T(cx, 300, f'ចំណុច {n} → អង្កត់ {len(edges)}', 28, cols[k]))
    return svgd(1000, 330, b, '44vh')


# ================================================================== 2.2 comparing two segments
def superpose(equal=True):
    """AB and CD are put on a line xy with A on C: if B falls on D they are equal; if D falls between A and B, CD is shorter"""
    la = 300
    lc = 300 if equal else 190
    b = seg(80, 80 + la, 70, BLUE, 8) + lab(80, 40, 'A', BLUE, 36) + lab(80 + la, 40, 'B', BLUE, 36)
    b += seg(540, 540 + lc, 70, GREEN, 8) + lab(540, 40, 'C', GREEN, 36) + lab(540 + lc, 40, 'D', GREEN, 36)
    y = 220
    b += dline(60, y, 940, y, GREY, 4, True) + lab(70, y + 54, 'x', GREY, 36) + lab(930, y + 54, 'y', GREY, 36)
    b += rvg(1, seg(200, 200 + la, y - 14, BLUE, 8, False) + lab(200, y - 34, 'A', BLUE, 34, 'end') + lab(200 + la, y - 34, 'B', BLUE, 34))
    b += rvg(2, seg(200, 200 + lc, y + 16, GREEN, 8, False) + lab(200, y + 56, 'C(A)', GREEN, 30, 'end') + lab(200 + lc, y + 56, 'D', GREEN, 34, 'middle')
             + (lab(200 + la + 10, y + 56, 'B', BLUE, 34, 'start') if not equal else ''))
    b += rvg(3, M(500, 330, 'AB = CD' if equal else 'CD < AB', 44, RED, 'middle', 700))
    return svgd(1000, 360, b, '46vh')


def four_points(pos, show=('braces',), unit=60, x0=140, y=170, steps=True):
    """A, B, C, D on a line xy at the given positions (to scale)"""
    X = lambda v: x0 + v * unit
    b = dline(60, y, 940, y, GREY, 4, True) + lab(75, y + 54, 'x', GREY, 34) + lab(925, y + 54, 'y', GREY, 34)
    for nm, v in zip('ABCD', pos):
        b += at(X(v), y, nm, NAVY)
    return b, X


def compare_ab_cd():
    """the sample exercise: AB = CD (checked with the compass); AC = AB + BC and BD = BC + CD, so AC = BD"""
    pos = (0, 4, 13, 17)                                   # the book's figure: AB = CD, BC more than twice AB
    assert pos[1] - pos[0] == pos[3] - pos[2] == 4
    b, X = four_points(pos, unit=48, x0=100)
    y = 170
    b += rvg(1, dim(X(0), X(4), y - 56, 'AB', BLUE, 32) + dim(X(13), X(17), y - 56, 'CD', GREEN, 32))
    b += rvg(2, dim(X(0), X(13), y + 84, 'AC = AB + BC', PURPLE, 30, up=False) + dim(X(4), X(17), y + 160, 'BD = BC + CD', ORANGE, 30, up=False))
    b += rvg(3, M(500, 400, 'AB = CD  ⟹  AC = BD', 42, RED, 'middle', 700))
    return svgd(1000, 430, b, '46vh')


def compare_practice():
    """AB < BC, CD > BC, AC > CD (points at 0, 3, 7, 12)"""
    pos = (0, 2, 6, 10.4)                                  # the book's figure: AB : BC : CD = 1 : 2 : 2.1
    AB, BC, CD, AC = 2, 4, 4.4, 6
    assert (pos[1] - pos[0], pos[2] - pos[1], round(pos[3] - pos[2], 6), pos[2] - pos[0]) == (AB, BC, CD, AC) and AB < BC < CD < AC
    b, X = four_points(pos, unit=76, x0=100)
    y = 170
    b += rvg(1, dim(X(0), X(2), y - 56, 'AB', BLUE, 30) + dim(X(2), X(6), y - 56, 'BC', ORANGE, 30) + dim(X(6), X(10.4), y - 56, 'CD', GREEN, 30))
    b += rvg(2, M(300, 340, 'AB < BC', 38, BLUE, 'middle', 700) + M(700, 340, 'CD > BC', 38, GREEN, 'middle', 700))
    b += rvg(3, dim(X(0), X(6), y + 84, 'AC', PURPLE, 30, up=False) + M(500, 420, 'AC > CD', 40, PURPLE, 'middle', 700))
    return svgd(1000, 450, b, '48vh')


# ================================================================== 2.3 adding and subtracting segments
def sum_segments():
    """AB, CD and EF put end to end on one line give the segment AF: AF = AB + BD + DF"""
    a, c, e = 150, 230, 180                                           # lengths in px
    b = seg(80, 80 + a, 50, BLUE, 8) + lab(80, 30, 'A', BLUE, 32) + lab(80 + a, 30, 'B', BLUE, 32)
    b += seg(400, 400 + c, 50, GREEN, 8) + lab(400, 30, 'C', GREEN, 32) + lab(400 + c, 30, 'D', GREEN, 32)
    b += seg(740, 740 + e, 50, ORANGE, 8) + lab(740, 30, 'E', ORANGE, 32) + lab(740 + e, 30, 'F', ORANGE, 32)
    y = 200
    x = 100
    b += dline(60, y, 940, y, GREY, 3, True)
    b += rvg(1, seg(x, x + a, y, BLUE, 8, False) + at(x, y, 'A', BLUE) + at(x + a, y, 'B', BLUE))
    b += rvg(2, seg(x + a, x + a + c, y, GREEN, 8, False) + at(x + a + c, y, 'D', GREEN))
    b += rvg(3, seg(x + a + c, x + a + c + e, y, ORANGE, 8, False) + at(x + a + c + e, y, 'F', ORANGE))
    b += rvg(4, dim(x, x + a + c + e, y - 54, 'AF = AB + BD + DF', RED, 34))
    return svgd(1000, 300, b, '40vh')


def diff_segments():
    """CD put on AB with C on A: DB = AB - CD"""
    a, c = 400, 230
    y = 120
    b = seg(120, 120 + a, y, BLUE, 8, False) + dot(120, y, BLUE, 9) + lab(120, y - 26, 'A(C)', BLUE, 36) + at(120 + a, y, 'B', BLUE)
    b += rvg(1, seg(120, 120 + c, y + 40, GREEN, 8, False) + dot(120 + c, y, GREEN, 9) + lab(120 + c, y - 26, 'D', GREEN, 36))
    b += rvg(2, seg(120 + c, 120 + a, y + 80, RED, 10, False) + dim(120 + c, 120 + a, y + 130, 'DB = AB − CD', RED, 34, up=False))
    return svgd(1000, 290, b, '38vh')


def _athlete(x, y, col, sc=1.0, leg=0):
    """a runner (shaded vector): head, torso, arms and legs mid-stride; (x, y) is where the feet touch the track"""
    s = sc
    b = f'<ellipse cx="{x}" cy="{y + 2}" rx="{26 * s:.0f}" ry="{6 * s:.0f}" fill="#000" opacity=".2"/>'
    hip = (x, y - 52 * s)
    sh = (x + 6 * s, y - 100 * s)
    b += line(hip[0], hip[1], x - 26 * s, y - 20 * s, '#2d3748', 9 * s)                                  # back leg
    b += line(x - 26 * s, y - 20 * s, x - 38 * s, y - 2 * s, '#2d3748', 8 * s)
    b += line(hip[0], hip[1], x + 22 * s, y - 28 * s, '#2d3748', 9 * s) + line(x + 22 * s, y - 28 * s, x + 18 * s, y - 2 * s, '#2d3748', 8 * s)    # front leg
    b += line(hip[0], hip[1], sh[0], sh[1], col, 22 * s)                                                 # torso
    b += line(sh[0], sh[1] + 6 * s, x - 20 * s, y - 78 * s, '#c08a5b', 7 * s) + line(sh[0], sh[1] + 6 * s, x + 28 * s, y - 84 * s, '#c08a5b', 7 * s)   # arms
    b += f'<circle cx="{sh[0] + 4 * s:.1f}" cy="{sh[1] - 16 * s:.1f}" r="{13 * s:.1f}" fill="#e0b48a" stroke="#a3764a" stroke-width="1.5"/>'
    return b


def runners_track():
    """three runners A, B, C run one after another (a relay): AB = 576 m, BC = 648 m, CD = 835 m: to scale"""
    AB, BC, CD = 576, 648, 835
    assert AB + BC + CD == 2059
    sc = 0.4
    x0, y = 90, 190
    X = [x0, x0 + AB * sc, x0 + (AB + BC) * sc, x0 + (AB + BC + CD) * sc]
    b = poly([(40, y), (960, y), (960, y + 30), (40, y + 30)], '#d9480f', None, 0) + f'<line x1="40" y1="{y + 15}" x2="960" y2="{y + 15}" stroke="#fff" stroke-width="2" stroke-dasharray="14 10" opacity=".7"/>'
    cols = [BLUE, GREEN, PURPLE, RED]
    for k, nm in enumerate('ABCD'):
        b += _athlete(X[k], y, cols[k], 0.8) if k < 3 else ''
        b += lab(X[k], y + 78, nm, NAVY, 38)
    for k in (0, 3):                                                                                   # the start and the finish flags
        fx = X[k] - 44 if k == 0 else X[k]
        b += line(fx, y, fx, y - 150, '#444', 5) + poly([(fx, y - 150), (fx + (62 if k == 0 else -62), y - 132), (fx, y - 114)], '#fcc419' if k == 0 else RED, '#444', 1.5)
    b += rvg(1, dim(X[0], X[1], y - 170, '576 m', BLUE, 32) + dim(X[1], X[2], y - 170, '648 m', GREEN, 32) + dim(X[2], X[3], y - 170, '835 m', PURPLE, 32))
    b += rvg(2, dim(X[0], X[3], y + 118, 'AD = 576 + 648 + 835 = 2 059 m', RED, 34, up=False))
    return svgd(1000, 380, f'<g transform="translate(0 30)">{b}</g>', '48vh')


# ================================================================== 2.4 multiplying and dividing a segment
def multiples():
    """AF is five equal segments: AF = 5 x AB; PQ = 4 AB, so AB = PQ / 4"""
    u = 120
    b = seg(80, 80 + u, 40, BLUE, 9) + lab(80, 24, 'A', BLUE, 34) + lab(80 + u, 24, 'B', BLUE, 34)
    y = 140
    names = 'ABCDEF'
    cols = [BLUE, GREEN, ORANGE, PURPLE, RED]
    for k in range(5):
        b += rvg(k + 1, seg(80 + k * u, 80 + (k + 1) * u, y, cols[k], 9, False))
    for k, nm in enumerate(names):
        b += dot(80 + k * u, y, NAVY, 8) + lab(80 + k * u, y + 46, nm, NAVY, 34)
    b += rvg(6, dim(80, 80 + 5 * u, y - 40, 'AF = 5 × AB', RED, 36))
    y2 = 300
    b += seg(80, 80 + u, y2 - 60, BLUE, 9) + lab(80, y2 - 82, 'A', BLUE, 30) + lab(80 + u, y2 - 82, 'B', BLUE, 30)
    for k in range(4):
        b += rvg(7, seg(80 + k * u, 80 + (k + 1) * u, y2, cols[k], 9, False))
    b += rvg(7, dot(80, y2, NAVY, 8) + dot(80 + 4 * u, y2, NAVY, 8) + lab(80, y2 + 46, 'P', NAVY, 34) + lab(80 + 4 * u, y2 + 46, 'Q', NAVY, 34))
    b += rvg(8, dim(80, 80 + 4 * u, y2 - 40, 'PQ = 4 × AB', RED, 36) + M(500, 396, 'AB = PQ ÷ 4 = PQ / 4', 38, NAVY, 'middle', 700))
    return svgd(1000, 420, b, '50vh')


def quarters():
    """I is the middle of AB, J the middle of AI, K the middle of IB: four equal parts; JK is half of AB"""
    u = 200
    x0, y = 100, 150
    pts = {'A': 0, 'J': 1, 'I': 2, 'K': 3, 'B': 4}
    b = seg(x0, x0 + 4 * u, y, GREY, 6, False)
    cols = [BLUE, GREEN, ORANGE, PURPLE]
    for k in range(4):
        b += rvg(1, seg(x0 + k * u, x0 + (k + 1) * u, y, cols[k], 10, False))
    for nm, v in pts.items():
        b += dot(x0 + v * u, y, NAVY, 10) + lab(x0 + v * u, y + 54, nm, NAVY, 38)
    b += rvg(2, dim(x0, x0 + 4 * u, y - 60, 'AB = 4 AJ = 2 AI', RED, 32))
    b += rvg(3, dim(x0 + u, x0 + 3 * u, y + 100, 'JK = AB / 2', GREEN, 34, up=False))
    return svgd(1000, 300, b, '40vh')


def _wheel(cx, cy, r, spokes=12, tire='#222'):
    b = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{tire}" stroke-width="{max(4, r * .12):.1f}"/><circle cx="{cx}" cy="{cy}" r="{r * .88:.1f}" fill="none" stroke="#adb5bd" stroke-width="1.5"/>'
    for k in range(spokes):
        a = k * 2 * math.pi / spokes
        b += f'<line x1="{cx}" y1="{cy}" x2="{cx + r * .88 * math.cos(a):.1f}" y2="{cy + r * .88 * math.sin(a):.1f}" stroke="#ced4da" stroke-width="1.2"/>'
    return b + f'<circle cx="{cx}" cy="{cy}" r="{r * .12:.1f}" fill="#495057"/>'


def bicycle(x, y, col=BLUE, flip=False):
    """a bicycle with a rider, wheels on the ground at y"""
    r = 36
    wx1, wx2 = x - 56, x + 56
    wy = y - r
    b = _wheel(wx1, wy, r) + _wheel(wx2, wy, r)
    top = (x + 4, wy - 46)
    b += f'<path d="M {wx1} {wy} L {x - 10} {wy - 44} L {wx2 - 8} {wy - 50} L {wx2} {wy} M {x - 10} {wy - 44} L {x + 8} {wy} L {wx1} {wy}" fill="none" stroke="{col}" stroke-width="6" stroke-linejoin="round"/>'
    b += line(wx2 - 8, wy - 50, wx2 - 14, wy - 70, '#444', 5) + line(wx2 - 20, wy - 72, wx2 - 4, wy - 72, '#444', 5) + line(x - 10, wy - 44, x - 14, wy - 56, '#444', 5) + line(x - 24, wy - 57, x - 4, wy - 57, '#222', 7)
    b += line(x - 14, wy - 60, x - 4, wy - 104, '#e8590c', 15) + f'<circle cx="{x - 1}" cy="{wy - 120}" r="12" fill="#e0b48a" stroke="#a3764a" stroke-width="1.5"/>' + line(x - 6, wy - 98, wx2 - 14, wy - 74, '#c08a5b', 6)
    b += line(x - 12, wy - 56, x + 6, wy - 22, '#2d3748', 8) + line(x + 6, wy - 22, x + 4, wy - 4, '#2d3748', 7)
    return b


def motorbike(x, y, col=RED):
    r = 40
    wx1, wx2 = x - 72, x + 72
    wy = y - r
    b = _wheel(wx1, wy, r, 14, '#1f1f1f') + _wheel(wx2, wy, r, 14, '#1f1f1f')
    b += f'<path d="M {wx1} {wy} L {x - 36} {wy - 54} L {x + 30} {wy - 54} L {x + 50} {wy - 6} L {wx2} {wy}" fill="none" stroke="#555" stroke-width="7" stroke-linejoin="round"/>'
    b += poly([(x - 44, wy - 56), (x + 28, wy - 56), (x + 40, wy - 22), (x - 20, wy - 14), (x - 52, wy - 30)], col, '#7a0f0f', 2)
    b += poly([(x - 60, wy - 64), (x + 8, wy - 64), (x + 8, wy - 72), (x - 60, wy - 72)], '#222')
    b += line(wx2 + 6, wy - 18, wx2 - 16, wy - 60, '#555', 7) + line(wx2 - 26, wy - 66, wx2 - 4, wy - 62, '#222', 7) + f'<circle cx="{wx2 + 2}" cy="{wy - 28}" r="9" fill="#ffe066" stroke="#a87a00" stroke-width="1.5"/>'
    b += line(x - 26, wy - 78, x - 12, wy - 126, '#1c7ed6', 17) + f'<circle cx="{x - 8}" cy="{wy - 144}" r="14" fill="#e0b48a" stroke="#a3764a" stroke-width="1.5"/><path d="M {x - 22} {wy - 148} a 15 15 0 0 1 30 0 z" fill="#c92a2a"/>' + line(x - 14, wy - 112, wx2 - 24, wy - 66, '#c08a5b', 6)
    b += line(x - 22, wy - 70, x + 6, wy - 30, '#2d3748', 9) + line(x + 6, wy - 30, x + 2, wy - 8, '#2d3748', 8)
    return b


def road_meeting():
    """a cyclist leaves village A, a motorcyclist leaves village B; they meet when the motorcyclist has gone 3x and the cyclist x: x + 3x = 24.6 km"""
    total, x_ = 24.6, 24.6 / 4
    assert abs(x_ - 6.15) < 1e-9 and abs(3 * x_ - 18.45) < 1e-9 and abs(x_ + 3 * x_ - total) < 1e-9
    sc = 800 / total                                                    # px per km
    xa, xb = 100, 100 + total * sc
    xm = xa + x_ * sc
    y = 210
    b = poly([(40, y), (960, y), (960, y + 36), (40, y + 36)], '#5f6b76') + f'<line x1="40" y1="{y + 18}" x2="960" y2="{y + 18}" stroke="#ffd43b" stroke-width="3" stroke-dasharray="26 18"/>'
    for nm, x, col in (('A', xa, BLUE), ('B', xb, RED)):                                    # the two villages: a little house and a tree
        b += poly([(x - 34, y - 6), (x + 34, y - 6), (x + 34, y - 52), (x - 34, y - 52)], '#f1e0b0', '#a3874a', 2) + poly([(x - 42, y - 52), (x + 42, y - 52), (x, y - 92)], col, '#444', 2)
        b += lab(x, y + 80, 'ភូមិ ' + nm, NAVY, 28) if False else TM(x, y + 82, 'ភូមិ', nm, 32, NAVY)
    b += bicycle(xm - 135, y, BLUE) + motorbike(xm + 135, y, RED)
    b += rvg(1, dim(xa, xm, y - 170, 'x', BLUE, 36) + dim(xm, xb, y - 170, '3x', RED, 36))
    b += rvg(2, dim(xa, xb, y - 230, 'x + 3x = 24.6 km', NAVY, 34))
    b += rvg(3, M(500, y + 140, '4x = 24.6  ⟹  x = 6.15 km,  3x = 18.45 km', 34, RED, 'middle', 700))
    return svgd(1000, 410, f'<g transform="translate(0 20)">{b}</g>', '50vh')


def road_two_thirds():
    """practice 2: the meeting point is 2/3 of AB from A, so 1/3 of AB = 8 km: AB = 24 km"""
    AB, third = 24, 8
    assert third * 3 == AB
    sc = 800 / AB
    x0, y = 100, 150
    b = seg(x0, x0 + AB * sc, y, GREY, 6, False)
    cols = [BLUE, BLUE, RED]
    for k in range(3):
        b += seg(x0 + k * third * sc, x0 + (k + 1) * third * sc, y, cols[k], 10, False)
    for nm, v in (('A', 0), ('M', 16), ('B', 24)):
        b += dot(x0 + v * sc, y, NAVY, 10) + lab(x0 + v * sc, y + 54, nm, NAVY, 38)
    b += rvg(1, dim(x0, x0 + 16 * sc, y - 56, '2/3 AB', BLUE, 32) + dim(x0 + 16 * sc, x0 + 24 * sc, y - 56, '1/3 AB = 8 km', RED, 32))
    b += rvg(2, M(500, 270, 'AB = 8 × 3 = 24 km', 40, RED, 'middle', 700))
    return svgd(1000, 310, b, '40vh')


# ================================================================== exercises
def ex1_three_lines():
    A, B, C = (230, 300), (640, 300), (430, 90)
    b = ''
    for k, (P, Q, col) in enumerate(((A, B, BLUE), (B, C, GREEN), (A, C, ORANGE))):
        b += rvg(k + 1, dline(P[0], P[1], Q[0], Q[1], col, 5, True, 110))
    for nm, P, dx, dy in (('A', A, -30, 14), ('B', B, 26, 14), ('C', C, 0, -24)):
        b += dot(P[0], P[1], RED, 11) + lab(P[0] + dx, P[1] + dy, nm, NAVY, 40)
    b += rvg(4, TM(430, 392, 'បន្ទាត់ ៣ ៖', 'AB, BC, AC', 32, NAVY))
    return svgd(860, 430, b, '46vh')


def ex2_equal_segments():
    L = 200
    b = seg(80, 80 + L, 80, GREEN, 9) + T(80 + L / 2, 54, 'អង្កត់ស្គាល់', 28, GREEN)
    y = 190
    xa = 500
    b += dline(60, y, 940, y, GREY, 4, True) + at(xa, y, 'A', NAVY)
    b += rvg(1, f'<path d="M {xa + L} {y - 30} Q {xa + L + 14} {y} {xa + L} {y + 30}" fill="none" stroke="#222" stroke-width="3"/>' + seg(xa, xa + L, y - 18, BLUE, 8, False) + lab(xa + L, y + 56, 'B', BLUE, 36))
    b += rvg(2, f'<path d="M {xa - L} {y - 30} Q {xa - L - 14} {y} {xa - L} {y + 30}" fill="none" stroke="#222" stroke-width="3"/>' + seg(xa - L, xa, y - 18, RED, 8, False) + lab(xa - L, y + 56, "B'", RED, 36))
    b += rvg(3, M(500, 300, "AB = AB'", 42, NAVY, 'middle', 700))
    return svgd(1000, 330, b, '42vh')


def ball3d(cx, cy, r, i=None):
    i = i or uid('bl')
    defs = rg(i, [(0, '#ffffff'), (.35, '#74c0fc'), (1, '#1864ab')], .35, .3, .85)
    return f'<ellipse cx="{cx}" cy="{cy + r + 12}" rx="{r * .9:.0f}" ry="14" fill="#000" opacity=".18"/><circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{i})" stroke="#0b3d73" stroke-width="2"/>', defs


def ex3_sphere_rod():
    """a steel rod pierces a ball at A and B: the rod is not on the surface of the ball; a line through two points of a plane lies in the plane"""
    bl, d1 = ball3d(250, 190, 120)
    A, B = (186, 120), (322, 262)
    b = bl
    # the rod: the part outside the ball is solid steel; the part inside is hidden
    b += dline(100, 40, 400, 340, '#868e96', 14, False) if False else ''
    ux, uy = (B[0] - A[0]), (B[1] - A[1])
    L = math.hypot(ux, uy)
    ux, uy = ux / L, uy / L
    o1, o2 = (A[0] - ux * 110, A[1] - uy * 110), (B[0] + ux * 110, B[1] + uy * 110)
    b += line(o1[0], o1[1], A[0], A[1], '#adb5bd', 11) + line(B[0], B[1], o2[0], o2[1], '#adb5bd', 11)
    b += f'<line x1="{A[0]}" y1="{A[1]}" x2="{B[0]}" y2="{B[1]}" stroke="#e9ecef" stroke-width="4" stroke-dasharray="8 7" opacity=".8"/>'
    b += dot(A[0], A[1], RED, 9) + lab(A[0] - 34, A[1] - 6, 'A', RED, 38) + dot(B[0], B[1], RED, 9) + lab(B[0] + 40, B[1] + 10, 'B', RED, 38)
    # right: a plane with a line through two of its points: the line lies in the plane
    i = uid('ep')
    defs = d1 + lg(i, [(0, '#dbe9ff'), (1, '#b6d0f5')], 0, 0, 1, 1)
    P = _par(560, 290, 340, 150, 70)
    b += poly(P, f'url(#{i})', BLUE, 3) + lab(930, 150, 'P', BLUE, 42)
    a, c = (640, 230), (820, 170)
    b += dline(a[0], a[1], c[0], c[1], RED, 5, True, 30) + dot(a[0], a[1], NAVY, 9) + dot(c[0], c[1], NAVY, 9) + lab(a[0] - 4, a[1] + 40, 'A', NAVY, 34) + lab(c[0] + 6, c[1] - 20, 'B', NAVY, 34)
    b += T(250, 410, 'ដែកមិនស្ថិតក្នុងផ្ទៃបាល់', 28, NAVY) + T(750, 410, 'បន្ទាត់ស្ថិតក្នុងប្លង់', 28, NAVY)
    return svgd(1000, 440, b, '52vh', defs)


def ex4_sum_difference():
    """a + b and a - b with the compass: arcs of radius b from B on both sides"""
    a, bb = 260, 150
    b = seg(60, 60 + a, 40, BLUE, 8) + lab(60 + a / 2, 22, 'a', BLUE, 32) + seg(500, 500 + bb, 40, GREEN, 8) + lab(500 + bb / 2, 22, 'b', GREEN, 32)
    y = 160
    xa = 120
    b += dline(60, y, 940, y, GREY, 4, True) + at(xa, y, 'A', NAVY)
    b += seg(xa, xa + a, y - 16, BLUE, 8, False) + at(xa + a, y, 'B', BLUE)
    b += rvg(1, f'<path d="M {xa + a + bb} {y - 26} Q {xa + a + bb + 14} {y} {xa + a + bb} {y + 26}" fill="none" stroke="#222" stroke-width="3"/>' + seg(xa + a, xa + a + bb, y - 16, GREEN, 8, False) + lab(xa + a + bb, y + 56, 'C', GREEN, 36))
    b += rvg(2, dim(xa, xa + a + bb, y + 100, 'AC = AB + BC = a + b', RED, 32, up=False))
    y2 = 400
    b += dline(60, y2, 940, y2, GREY, 4, True) + at(xa, y2, 'A', NAVY) + seg(xa, xa + a, y2 - 16, BLUE, 8, False) + at(xa + a, y2, 'B', BLUE)
    b += rvg(3, f'<path d="M {xa + a - bb} {y2 - 26} Q {xa + a - bb - 14} {y2} {xa + a - bb} {y2 + 26}" fill="none" stroke="#222" stroke-width="3"/>' + seg(xa + a - bb, xa + a, y2 + 18, GREEN, 8, False) + lab(xa + a - bb, y2 + 56, 'C', GREEN, 36))
    b += rvg(4, dim(xa, xa + a - bb, y2 + 100, 'AC = AB − BC = a − b', RED, 32, up=False))
    return svgd(1000, 560, b, '56vh')


def ex5_midpoints():
    MN, MI, NI = 18, 7, 11
    assert MI + NI == MN
    A_, B_ = MI / 2, MI + NI / 2
    assert B_ - A_ == 9 == MN / 2
    sc, x0, y = 46, 100, 150
    X = lambda v: x0 + v * sc
    b = seg(X(0), X(MN), y, GREY, 7, False) + dim(X(0), X(MN), y - 60, 'MN = 18 cm', NAVY, 32)
    for nm, v, col in (('M', 0, NAVY), ('A', A_, GREEN), ('I', MI, RED), ('B', B_, GREEN), ('N', MN, NAVY)):
        b += at(X(v), y, nm, col)
    b += rvg(1, dim(X(0), X(MI), y + 100, 'MI', BLUE, 28, up=False) + dim(X(MI), X(MN), y + 100, 'NI', ORANGE, 28, up=False))
    b += rvg(2, dim(X(A_), X(B_), y + 168, 'AB = MN / 2 = 9 cm', RED, 32, up=False))
    return svgd(1000, 400, b, '46vh')


def ex6_ab_2bc():
    BC, AB = 6, 12
    assert AB == 2 * BC and AB + BC == 18
    sc, x0, y = 40, 120, 150
    X = lambda v: x0 + v * sc
    b = dline(60, y, 940, y, GREY, 4, True) + lab(75, y + 54, 'x', GREY, 34) + lab(925, y + 54, 'y', GREY, 34)
    b += seg(X(0), X(12), y - 14, BLUE, 8, False) + seg(X(12), X(18), y - 14, ORANGE, 8, False)
    for nm, v in (('A', 0), ('B', 12), ('C', 18)):
        b += at(X(v), y, nm, NAVY)
    b += rvg(1, dim(X(0), X(12), y - 64, 'AB = 2 BC = 12 cm', BLUE, 30) + dim(X(12), X(18), y - 64, 'BC = 6 cm', ORANGE, 30))
    b += rvg(2, dim(X(0), X(18), y + 104, 'AC = 18 cm', RED, 32, up=False))
    return svgd(1000, 300, b, '40vh')


def ex7_four_points():
    AB, BC, CD = 3, 5, 3
    assert (AB + BC, BC + CD) == (8, 8)
    sc, x0, y = 66, 160, 160
    X = lambda v: x0 + v * sc
    pts = [0, 3, 8, 11]
    b = dline(60, y, 940, y, GREY, 4, True) + lab(75, y + 54, 'Δ', GREY, 34)
    for nm, v in zip('ABCD', pts):
        b += at(X(v), y, nm, NAVY)
    b += rvg(1, dim(X(0), X(3), y - 56, '3 cm', BLUE, 28) + dim(X(3), X(8), y - 56, '5 cm', ORANGE, 28) + dim(X(8), X(11), y - 56, '3 cm', GREEN, 28))
    b += rvg(2, dim(X(0), X(8), y + 100, 'AC = 8 cm', PURPLE, 30, up=False) + dim(X(3), X(11), y + 160, 'BD = 8 cm', RED, 30, up=False))
    return svgd(1000, 400, b, '46vh')


def ex8_difference_twice():
    """MN and PQ are both CD - AB: AB is put on CD from one end, then from the other end: the two remainders are equal"""
    ab, cd = 200, 460
    x0 = 120
    b = seg(60, 60 + ab, 40, BLUE, 8) + lab(60 + ab / 2, 22, 'AB', BLUE, 30)
    y = 160
    b += dline(60, y, 940, y, GREY, 4, True) + lab(75, y + 54, 'x', GREY, 34) + lab(925, y + 54, 'y', GREY, 34)
    b += seg(x0, x0 + cd, y, GREEN, 8, False) + at(x0, y, 'C', GREEN) + at(x0 + cd, y, 'D', GREEN)
    b += rvg(1, seg(x0, x0 + ab, y - 18, BLUE, 8, False) + seg(x0 + ab, x0 + cd, y + 20, RED, 10, False) + dot(x0 + ab, y, RED, 9) + lab(x0 + ab, y - 36, 'M', RED, 34) + lab((x0 + ab + x0 + cd) / 2, y + 66, 'MN', RED, 32))
    b += rvg(2, seg(x0 + cd - ab, x0 + cd, y - 18, BLUE, 8, False) + seg(x0, x0 + cd - ab, y + 110, ORANGE, 10, False) + lab((x0 + x0 + cd - ab) / 2, y + 156, 'PQ', ORANGE, 32))
    b += rvg(3, M(500, 380, 'PQ = MN = CD − AB', 40, NAVY, 'middle', 700))
    return svgd(1000, 420, b, '46vh')


def ex9_spool_needle():
    """a spool of wire and a sewing needle 35 mm long: 52.50 m = 52 500 mm; 52 500 / 35 = 1 500 needles; with 20% spoiled: 42 000 / 35 = 1 200"""
    assert 52500 / 35 == 1500 and 52500 * 0.8 == 42000 and 42000 / 35 == 1200
    i = uid('sp')
    defs = lg(i + 'w', [(0, '#b87333'), (.5, '#f0b27a'), (1, '#8a5a24')]) + lg(i + 'f', [(0, '#e9ecef'), (.5, '#ffffff'), (1, '#adb5bd')])
    cx, cy = 230, 200
    b = f'<ellipse cx="{cx}" cy="{cy + 120}" rx="150" ry="16" fill="#000" opacity=".16"/>'
    b += f'<rect x="{cx - 120}" y="{cy - 80}" width="240" height="200" rx="14" fill="url(#{i}w)" stroke="#6b3f16" stroke-width="2"/>'
    for k in range(18):
        b += f'<path d="M {cx - 118} {cy - 76 + k * 11} q 118 14 236 0" fill="none" stroke="#8a5a24" stroke-width="1.6" opacity=".7"/>'
    b += f'<rect x="{cx - 140}" y="{cy - 90}" width="280" height="20" rx="8" fill="url(#{i}f)" stroke="#868e96" stroke-width="2"/><rect x="{cx - 140}" y="{cy + 110}" width="280" height="20" rx="8" fill="url(#{i}f)" stroke="#868e96" stroke-width="2"/>'
    b += T(cx, 372, 'ខ្សែលួស 52.50 m', 28, NAVY)
    # a needle drawn to scale next to a ruler: 35 mm
    nx0, ny = 520, 130
    sc = 12                                                                                     # px per mm
    b += poly([(nx0 - 16, ny + 70), (nx0 + 35 * sc + 16, ny + 70), (nx0 + 35 * sc + 16, ny + 120), (nx0 - 16, ny + 120)], '#fff3bf', '#b08d1a', 2)
    for mm in range(0, 36):
        x = nx0 + mm * sc
        h = 24 if mm % 10 == 0 else 16 if mm % 5 == 0 else 10
        b += f'<line x1="{x}" y1="{ny + 70}" x2="{x}" y2="{ny + 70 + h}" stroke="#4a3b00" stroke-width="1.4"/>' + (M(x, ny + 112, mm, 18, '#4a3b00', 'middle', 600) if mm % 5 == 0 else '')
    b += f'<path d="M {nx0} {ny + 20} L {nx0 + 35 * sc - 20} {ny + 14} L {nx0 + 35 * sc} {ny + 16} L {nx0 + 35 * sc - 20} {ny + 22} Z" fill="url(#{i}f)" stroke="#6b7280" stroke-width="1.5"/>'
    b += f'<ellipse cx="{nx0 + 20}" cy="{ny + 18}" rx="5" ry="2.6" fill="#fff" stroke="#6b7280" stroke-width="1.2"/>'
    b += dim(nx0, nx0 + 35 * sc, ny - 20, '35 mm', RED, 30)
    b += rvg(1, M(700, 330, '52 500 ÷ 35 = 1 500', 36, GREEN, 'middle', 700))
    b += rvg(2, M(700, 376, '(52 500 × 80/100) ÷ 35 = 1 200', 32, ORANGE, 'middle', 700))
    return svgd(1000, 410, b, '48vh', defs)


def snail(x, y, s=1.0):
    """a garden snail (shell spiral, soft body)"""
    b = f'<path d="M {x - 34 * s} {y} q 10 {-14 * s} {30 * s} {-8 * s} q {34 * s} {-4 * s} {52 * s} {2 * s} q {10 * s} {6 * s} 0 {12 * s} z" fill="#d9b38c" stroke="#8c6a4a" stroke-width="1.5"/>'
    b += f'<line x1="{x - 28 * s}" y1="{y - 6 * s}" x2="{x - 36 * s}" y2="{y - 22 * s}" stroke="#8c6a4a" stroke-width="2"/><line x1="{x - 22 * s}" y1="{y - 6 * s}" x2="{x - 24 * s}" y2="{y - 24 * s}" stroke="#8c6a4a" stroke-width="2"/>'
    b += f'<circle cx="{x + 4 * s}" cy="{y - 18 * s}" r="{22 * s}" fill="#c0702e" stroke="#7a4217" stroke-width="2"/><path d="M {x + 4 * s} {y - 18 * s} m {-3 * s} {0} a {7 * s} {7 * s} 0 1 1 {12 * s} {2 * s} a {13 * s} {13 * s} 0 1 1 {-24 * s} {-4 * s}" fill="none" stroke="#7a4217" stroke-width="2"/>'
    return b


def ex10_snail_well():
    """a well 8 m deep; the snail climbs 4 m at night and slips 2 m by day: out in 3 nights"""
    depth = 8
    sc = 36                                                       # px per metre
    x0, ytop = 120, 70
    ybot = ytop + depth * sc
    i = uid('wl')
    defs = lg(i, [(0, '#7b6f62'), (1, '#4a4036')], 1, 0, 0, 0)
    b = f'<rect x="{x0}" y="{ytop}" width="170" height="{depth * sc}" fill="url(#{i})" stroke="#2b2118" stroke-width="3"/>'
    for r in range(depth * 2):
        for c in range(3):
            b += f'<rect x="{x0 + c * 56 + (28 if r % 2 else 0) - 28}" y="{ytop + r * (sc / 2)}" width="56" height="{sc / 2}" fill="none" stroke="#2b2118" stroke-width="1" opacity=".35"/>'
    b += f'<rect x="{x0 - 14}" y="{ytop - 14}" width="198" height="14" fill="#8d99a6" stroke="#495057" stroke-width="2"/>'
    for m in range(depth + 1):
        y = ybot - m * sc
        b += line(x0 + 170, y, x0 + 196, y, NAVY, 3) + M(x0 + 214, y + 8, f'{m} m', 22, NAVY, 'start', 600)
    steps = [(4, 'ក្រោយយប់ទី ១ ៖ 4 m'), (2, 'ថ្ងៃ ៖ 2 m'), (6, 'ក្រោយយប់ទី ២ ៖ 6 m'), (4, 'ថ្ងៃ ៖ 4 m'), (8, 'ក្រោយយប់ទី ៣ ៖ 8 m')]
    heights = [4, 2, 6, 4, 8]
    assert heights == [4, 4 - 2, 4 - 2 + 4, 6 - 2, 8]
    for k, ((h, txt)) in enumerate(steps):
        y = ybot - h * sc
        prev = heights[k - 1] if k else 0
        last = k == len(steps) - 1
        b += rvg(k + 1, line(x0 + 85, ybot - prev * sc, x0 + 85, y, GREEN if h >= prev else RED, 5) + snail(x0 + 85, y, .9), until=None if last else k + 2)     # the snail is where it is now, not everywhere it has been
        b += rvg(k + 1, T(560, 120 + k * 52, txt, 30, GREEN if k % 2 == 0 else RED, 'start'))
    b += rvg(5, T(560, 120 + 5 * 52 + 20, 'ឡើងផុតក្នុង ៣ យប់', 34, NAVY, 'start'))
    return svgd(1000, 420, b, '52vh', defs)


def pentagram():
    """a regular pentagram: 5 tips and 5 inner crossing points = 10 trees; 5 lines of 4 trees"""
    cx, cy, R = 500, 215, 190
    tips = [(cx + R * math.cos(math.radians(-90 + k * 72)), cy + R * math.sin(math.radians(-90 + k * 72))) for k in range(5)]
    lines = [(tips[k], tips[(k + 2) % 5]) for k in range(5)]
    inner = set()
    for (a, b_), (c, d) in itertools.combinations(lines, 2):
        try:
            p = _isect((a, b_), (c, d))
        except ZeroDivisionError:
            continue
        # a crossing counts when it is strictly inside both segments (the tips are shared ends)
        def inside(P, Q, X):
            t = ((X[0] - P[0]) * (Q[0] - P[0]) + (X[1] - P[1]) * (Q[1] - P[1])) / ((Q[0] - P[0]) ** 2 + (Q[1] - P[1]) ** 2)
            return 0.01 < t < 0.99
        if inside(a, b_, p) and inside(c, d, p):
            inner.add((round(p[0], 3), round(p[1], 3)))
    assert len(inner) == 5
    pts = list(tips) + [tuple(p) for p in inner]
    for (a, b_) in lines:                                                  # each line carries exactly 4 of the 10 points
        n = sum(1 for p in pts if abs((b_[0] - a[0]) * (p[1] - a[1]) - (b_[1] - a[1]) * (p[0] - a[0])) < 0.5)
        assert n == 4, n
    cols = [BLUE, GREEN, ORANGE, PURPLE, RED]
    b = ''
    for k, (a, b_) in enumerate(lines):
        b += rvg(k + 1, line(a[0], a[1], b_[0], b_[1], cols[k], 4))
    for p in pts:
        b += flower(p[0], p[1], '#37b24d') if False else f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="11" fill="#2f9e44" stroke="#fff" stroke-width="3"/><circle cx="{p[0]:.1f}" cy="{p[1] - 4:.1f}" r="5" fill="#8ce99a"/>'
    b += rvg(6, TM(500, 440, 'ដើមមៀន ១០ ដើម ៖ ៥ ជួរ × ៤ ដើម', '', 32, NAVY))
    return svgd(1000, 470, b, '54vh')


def mid_example():
    """practice 2.3: AB = 12 cm, BC = 46 cm, M the middle of AB, N the middle of BC: MN = 6 + 23 = 29 cm"""
    AB, BC = 12, 46
    M_, N_ = AB / 2, AB + BC / 2
    assert (AB / 2 + BC / 2) == N_ - M_ == 29
    sc, x0, y = 14, 100, 160
    X = lambda v: x0 + v * sc
    b = dline(60, y, 940, y, GREY, 4, True) + lab(75, y + 54, 'x', GREY, 34) + lab(925, y + 54, 'y', GREY, 34)
    b += seg(X(0), X(AB), y - 12, BLUE, 8, False) + seg(X(AB), X(AB + BC), y - 12, ORANGE, 8, False)
    for nm, v, col in (('A', 0, NAVY), ('M', M_, RED), ('B', AB, NAVY), ('N', N_, RED), ('C', AB + BC, NAVY)):
        b += at(X(v), y, nm, col)
    b += rvg(1, dim(X(0), X(AB), y - 64, 'AB = 12 cm', BLUE, 28) + dim(X(AB), X(AB + BC), y - 64, 'BC = 46 cm', ORANGE, 28))
    b += rvg(2, dim(X(M_), X(AB), y + 104, 'MB = 6', RED, 28, up=False) + dim(X(AB), X(N_), y + 104, 'BN = 23', RED, 28, up=False))
    b += rvg(3, dim(X(M_), X(N_), y + 168, 'MN = 6 + 23 = 29 cm', GREEN, 32, up=False))
    return svgd(1000, 380, b, '46vh')


def xyz_example():
    """practice 2.4: XY = 8 cm, XZ = 20 cm, S the middle of YZ: YZ = 12, YS = 6, XS = 14 = (XY + XZ) / 2"""
    XY, XZ = 8, 20
    YZ = XZ - XY
    XS = XY + YZ / 2
    assert (YZ, XS) == (12, 14) and XS == (XY + XZ) / 2
    sc, x0, y = 34, 120, 160
    X = lambda v: x0 + v * sc
    b = dline(60, y, 940, y, GREY, 4, True) + lab(75, y + 54, 'Δ', GREY, 34)
    b += seg(X(0), X(XY), y - 12, BLUE, 8, False) + seg(X(XY), X(XS), y - 12, GREEN, 8, False) + seg(X(XS), X(XZ), y - 12, ORANGE, 8, False)
    for nm, v, col in (('X', 0, NAVY), ('Y', XY, NAVY), ('S', XS, RED), ('Z', XZ, NAVY)):
        b += at(X(v), y, nm, col)
    b += rvg(1, dim(X(0), X(XY), y - 64, 'XY = 8 cm', BLUE, 28) + dim(X(0), X(XZ), y - 118, 'XZ = 20 cm', NAVY, 28))
    b += rvg(2, dim(X(XY), X(XZ), y + 104, 'YZ = 20 − 8 = 12 cm', PURPLE, 28, up=False))
    b += rvg(3, dim(X(XY), X(XS), y + 160, 'YS = 6', GREEN, 28, up=False) + dim(X(0), X(XS), y + 214, 'XS = 8 + 6 = 14 cm', RED, 32, up=False))
    return svgd(1000, 470, b, '50vh')


PREVIEW = ['mid_example', 'xyz_example', 'segment_MN', 'ruler_measure', 'compass_transfer', 'polygons_segments', 'superpose', 'compare_ab_cd', 'compare_practice', 'sum_segments', 'diff_segments',
           'runners_track', 'multiples', 'quarters', 'road_meeting', 'road_two_thirds', 'ex1_three_lines', 'ex2_equal_segments', 'ex3_sphere_rod', 'ex4_sum_difference',
           'ex5_midpoints', 'ex6_ab_2bc', 'ex7_four_points', 'ex8_difference_twice', 'ex9_spool_needle', 'ex10_snail_well', 'pentagram']
