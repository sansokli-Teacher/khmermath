# Pictures for Grade 9 Lesson 1 «ចំនួនអសនិទាន». Every length is computed; asserts check the geometry.
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lesson1'))
from lib import *

MATHFONT = "font-family=\"'Times New Roman','STIX Two Text','Cambria Math',serif\" font-style=\"italic\""


def M(x, y, t, size=28, fill=NAVY, anchor='middle', weight=700, halo=False):
    t = str(t).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    h = ' stroke="#fff" stroke-width="9" paint-order="stroke" stroke-linejoin="round"' if halo else ''     # a white outline so a number stays readable over lines
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}" {MATHFONT}{h}>{t}</text>'


def TMX(x, y, parts, size=30, fill=NAVY, anchor='middle', weight=700):
    """parts = [(text, is_math), ...]: Khmer words upright, every number, letter and sign in italic Times maths"""
    esc = lambda t: str(t).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    spans = ''.join((f'<tspan {MATHFONT} font-weight="600">{esc(t)}</tspan>' if is_m else esc(t)) + ' ' for t, is_m in parts)
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}" {FONT}>{spans}</text>'


def MIX(x, y, parts, size=34, fill=NAVY, anchor='middle', weight=700):
    """maths with units: parts = [(text, kind)], kind 'i' = italic Times (variables, numbers, signs), 'u' = upright Times (units such as m, cm), 'k' = Khmer words"""
    esc = lambda t: str(t).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    up = "font-family=\"'Times New Roman','STIX Two Text',serif\" font-style=\"normal\""
    out = ''
    for t, k in parts:
        out += (f'<tspan {MATHFONT} font-weight="600">{esc(t)}</tspan>' if k == 'i' else f'<tspan {up} font-weight="600">{esc(t)}</tspan>' if k == 'u' else esc(t))
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}" {FONT} xml:space="preserve">{out}</text>'


def poly(pts, fill, stroke='none', sw=0):
    p = ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts)
    return f'<polygon points="{p}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def _leg(a, b, fill, edge, w=12):
    ax, ay = a
    bx, by = b
    ang = math.atan2(by - ay, bx - ax)
    px, py = -math.sin(ang) * (w / 2), math.cos(ang) * (w / 2)
    return poly([(ax + px, ay + py), (bx + px, by + py), (bx - px, by - py), (ax - px, ay - py)], fill, edge, 1.4)


def compass_flat(L, H=150):
    """Needle tip at (0, 0), pencil tip at (L, 0), hinge above the midpoint. Returns (svg, bbox ymin, bbox ymax)."""
    hx, hy = L / 2, -H
    body = _leg((hx, hy), (0, 0), '#c5cdd6', '#6b7280') + _leg((hx, hy), (L, 0), '#c5cdd6', '#6b7280')
    body += poly([(-4, 0), (4, 0), (0, 18)], '#3d4349')
    body += poly([(L - 9, -30), (L + 9, -30), (L + 3, 2), (L - 3, 2)], '#ffd43b', '#a87a00', 1.5)
    body += poly([(L - 3, 0), (L + 3, 0), (L, 14)], '#222')
    body += f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="13" fill="#868e96" stroke="#495057" stroke-width="2"/>'
    body += f'<rect x="{hx - 5:.1f}" y="{hy - 48:.1f}" width="10" height="38" rx="4" fill="#adb5bd" stroke="#6b7280" stroke-width="1.4"/>'
    ymin, ymax = hy - 48, 18
    return body, ymin, ymax


def _rot_origin(ymin, ymax):
    """CSS fill-box percentage so rotation is about the needle (0, 0)."""
    return (0 - ymin) / (ymax - ymin) * 100


# ---------------------------------------------------------------- sets ℕ ⊂ ℤ ⊂ ℚ ⊂ ℝ
def number_sets():
    """Nested sets. √2 sits in ℝ and outside ℚ. Irrationality of √2 is the parity argument, not a decimal."""
    # If √2 = p/q in lowest terms then p² = 2q², so p is even, p = 2k, then q² = 2k², so q is even: contradiction.
    for q in range(1, 30):
        for p in range(1, int(q * math.sqrt(2)) + 3):
            if math.gcd(p, q) == 1:
                assert p * p != 2 * q * q
    b = rect(40, 30, 920, 400, '#e7f5ff', 28, BLUE, 4)
    b += rect(70, 70, 620, 320, '#d3f9d8', 24, GREEN, 4)
    b += rect(100, 120, 400, 230, '#fff3bf', 22, GOLD, 4)
    b += rect(130, 175, 220, 140, '#ffd8a8', 18, ORANGE, 4)
    b += M(240, 250, 'ℕ', 36, ORANGE)
    b += M(430, 200, 'ℤ', 36, '#e67700')
    b += M(560, 120, 'ℚ', 36, GREEN)
    b += M(860, 70, 'ℝ', 36, BLUE)
    b += M(820, 230, '√2', 40, RED)
    b += M(800, 290, 'π', 40, PURPLE)
    b += T(800, 360, 'អសនិទាន', 28, RED)
    return svg(1000, 460, b, '46vh')


# ---------------------------------------------------------------- square of area 3 m² (the garden that opens the lesson)
def garden_square():
    """a square garden of area 3 m^2: its side x satisfies x^2 = 3, so x = sqrt 3 (a length is positive) = 1.73... m"""
    assert 1.73 ** 2 < 3 < 1.74 ** 2 and abs(math.sqrt(3) ** 2 - 3) < 1e-12
    side, x0, y0 = 270, 150, 60
    b = rect(x0, y0, side, side, '#d3f9d8', 8, TEAL, 5)
    b += MIX(x0 + side / 2, y0 + side / 2 + 14, [('S = 3 ', 'i'), ('m', 'u'), ('²', 'u')], 40, NAVY)
    # the side is x: marked on the bottom edge and on the left edge
    b += line(x0, y0 + side + 26, x0 + side, y0 + side + 26, RED, 4) + line(x0, y0 + side + 14, x0, y0 + side + 38, RED, 4) + line(x0 + side, y0 + side + 14, x0 + side, y0 + side + 38, RED, 4)
    b += M(x0 + side / 2, y0 + side + 76, 'x', 42, RED)
    b += line(x0 - 26, y0, x0 - 26, y0 + side, RED, 4) + line(x0 - 38, y0, x0 - 14, y0, RED, 4) + line(x0 - 38, y0 + side, x0 - 14, y0 + side, RED, 4)
    b += M(x0 - 60, y0 + side / 2 + 14, 'x', 42, RED)
    b += rvg(1, MIX(560, 150, [('S = x²  ', 'i'), ('→', 'i'), ('  x² = 3', 'i')], 44, NAVY, 'start'))
    b += rvg(2, MIX(560, 240, [('x = √3 ', 'i'), ('  (x > 0)', 'i')], 44, RED, 'start'))
    b += rvg(3, MIX(560, 330, [('√3 ≈ 1.73 ', 'i'), ('m', 'u')], 44, TEAL, 'start'))
    return svg(1000, 440, b, '46vh')




# ---------------------------------------------------------------- √2 on the number line, compass at every step
def sqrt2_compass():
    """Right triangle with legs 1 and 1. The compass carries the hypotenuse onto the number line."""
    unit = 168
    R = unit * math.sqrt(2)
    assert abs(R * R - 2 * unit * unit) < 1e-6
    assert unit < R < 2 * unit
    x0, y = 150, 360
    x1 = x0 + unit
    topx, topy = x1, y - unit
    x2 = x0 + R
    k = 's2'
    comp, ymin, ymax = compass_flat(unit, 128)
    oy = _rot_origin(ymin, ymax)
    compR, yminR, ymaxR = compass_flat(R, 128)
    oyR = _rot_origin(yminR, ymaxR)
    arc = R * math.radians(45)
    # arc from the top of the hypotenuse down onto the line (45° of the circle)
    a0 = math.radians(-45)
    sx, sy = x0 + R * math.cos(a0), y + R * math.sin(a0)
    assert abs(sx - topx) < 1e-6 and abs(sy - topy) < 1e-6
    css = (f'@keyframes {k}a{{from{{transform:rotate(-8deg)}}to{{transform:rotate(0deg)}}}}'
           f'@keyframes {k}b{{from{{transform:rotate(-70deg)}}to{{transform:rotate(-90deg)}}}}'
           f'@keyframes {k}c{{from{{transform:rotate(-45deg)}}to{{transform:rotate(0deg)}}}}'
           f'@keyframes {k}d{{from{{stroke-dashoffset:{arc + 8:.0f}}}to{{stroke-dashoffset:0}}}}')
    b = f'<style>{css}</style>'
    # number line 0, 1, 2, 3
    b += line(x0 - 30, y, x0 + 3.35 * unit, y, NAVY, 5)
    b += f'<polygon points="{x0 + 3.5 * unit},{y} {x0 + 3.32 * unit},{y - 11} {x0 + 3.32 * unit},{y + 11}" fill="{NAVY}"/>'
    for n, lab in ((0, '0'), (1, '1'), (2, '2'), (3, '3')):
        b += line(x0 + n * unit, y - 12, x0 + n * unit, y + 12, NAVY, 3)
        b += M(x0 + n * unit, y + 48, lab, 30, NAVY)
    # step 1: compass measures the unit on the line
    b += rvg(1, f'<g transform="translate({x0} {y})"><g class="pen-swing" style="transform-box:fill-box;transform-origin:0% {oy:.2f}%;animation:{k}a 1.6s ease-in-out both">{comp}</g></g>'
             + line(x0, y, x1, y, BLUE, 8)
             + TMX(700, 70, [('១. វាស់ប្រវែង', False), ('1', True)], 30, RED, 'start'), until=2)
    # step 2: same opening, needle at 1, swing up to the perpendicular
    b += rvg(2, line(x1, y, x1, topy, ORANGE, 8)
             + f'<g transform="translate({x1} {y})"><g class="pen-swing" style="transform-box:fill-box;transform-origin:0% {oy:.2f}%;animation:{k}b 1.8s ease-in-out both">{comp}</g></g>'
             + M(x1 + 28, (y + topy) / 2, '1', 32, ORANGE, 'start')
             + TMX(700, 70, [('២. គូសជ្រុងកែងប្រវែង', False), ('1', True)], 30, RED, 'start'), until=3)
    # the triangle stays
    b += rvg(3, line(x0, y, x1, y, BLUE, 8) + line(x1, y, x1, topy, ORANGE, 8)
             + line(x0, y, topx, topy, RED, 8)
             + rect(x1 - 22, y - 22, 22, 22, 'none', 0, ORANGE, 3)
             + M((x0 + topx) / 2 - 28, (y + topy) / 2 - 8, '√2', 34, RED)
             + f'<path class="pen-arc" d="M {sx:.1f} {sy:.1f} A {R:.1f} {R:.1f} 0 0 1 {x2:.1f} {y:.1f}" fill="none" stroke="#222" stroke-width="4" stroke-linecap="round" style="stroke-dasharray:{arc + 8:.0f};animation:{k}d 2.2s ease-in-out both"/>'
             + f'<g transform="translate({x0} {y})"><g class="pen-swing" style="transform-box:fill-box;transform-origin:0% {oyR:.2f}%;animation:{k}c 2.2s ease-in-out both">{compR}</g></g>'
             + T(700, 70, '៣. វាស់អ៊ីប៉ូតេនុស ទៅលើបន្ទាត់', 28, RED, 'start'), until=4)
    b += rvg(4, line(x0, y, x1, y, BLUE, 8) + line(x1, y, x1, topy, ORANGE, 8)
             + line(x0, y, topx, topy, RED, 7)
             + rect(x1 - 22, y - 22, 22, 22, 'none', 0, ORANGE, 3)
             + M((x0 + topx) / 2 - 28, (y + topy) / 2 - 8, '√2', 34, RED)
             + f'<path d="M {sx:.1f} {sy:.1f} A {R:.1f} {R:.1f} 0 0 1 {x2:.1f} {y:.1f}" fill="none" stroke="#222" stroke-width="3" stroke-linecap="round"/>'
             + circ(x2, y, 11, RED, '#fff', 3)
             + M(x2, y - 28, '√2', 34, RED)
             + TMX(700, 70, [('√2', True), ('នៅចន្លោះ', False), ('1', True), ('និង', False), ('2', True)], 30, RED, 'start'))
    return svg(1000, 460, b, '50vh')


# ---------------------------------------------------------------- a square of area 2, its side laid onto the line
def square_area2():
    u = 150
    side = u * math.sqrt(2)
    assert abs((side / u) ** 2 - 2) < 1e-9
    x, y = 80, 40
    # the side drops onto the number line (pen-glide). --dx/--dy are the start offset.
    yline = 400
    xmark = 80
    dx, dy = x - xmark, (y + side) - yline
    b = rect(x, y, side, side, '#d0ebff', 6, BLUE, 5)
    b += M(x + side / 2, y + side / 2, '2', 40, NAVY)
    b += M(x + side / 2, y - 12, '√2', 32, RED)
    b += f'<g class="pen-glide" style="--dx:{dx:.1f}px;--dy:{dy:.1f}px;animation:penIn 1.8s ease-in-out both">'
    b += line(xmark, yline, xmark + side, yline, RED, 8) + '</g>'
    b += line(40, yline, 920, yline, NAVY, 4)
    b += M(xmark, yline + 40, '0', 28, NAVY)
    b += M(xmark + side, yline + 40, '√2', 30, RED)
    b += M(xmark + 2 * u, yline + 40, '2', 28, NAVY)
    b += line(xmark + 2 * u, yline - 10, xmark + 2 * u, yline + 10, NAVY, 3)
    return svg(1000, 470, b, '46vh')


# ---------------------------------------------------------------- √3 squeezed between integers
def squeeze_sqrt3():
    """1² < 3 < 2² and 1.7² < 3 < 1.8², so √3 is between those bounds. Squares use fractions, not a decimal guess."""
    from fractions import Fraction
    assert 1 ** 2 < 3 < 2 ** 2
    assert Fraction('1.7') ** 2 == Fraction(289, 100) < 3
    assert Fraction('1.8') ** 2 == Fraction(324, 100) > 3
    # place 1 at x=80, 2 at x=860. √3 is not drawn from a float approximation of the root:
    # it sits in the open interval (1.7, 1.8), drawn at the midpoint of that tenth.
    x_of = lambda t: 80 + (t - 1) * (860 - 80)
    p17, p18 = float(Fraction('1.7')), float(Fraction('1.8'))
    mid = (p17 + p18) / 2
    assert p17 < mid < p18
    y = 150
    b = line(40, y, 960, y, NAVY, 5)
    b += f'<polygon points="980,{y} 956,{y-11} 956,{y+11}" fill="{NAVY}"/>'
    for t, lab, col in ((1, '1', NAVY), (2, '2', NAVY)):
        b += line(x_of(t), y - 14, x_of(t), y + 14, NAVY, 4)
        b += M(x_of(t), y + 52, lab, 32, col)
    for t, lab, col in ((p17, '1.7', BLUE), (p18, '1.8', ORANGE)):
        b += line(x_of(t), y - 18, x_of(t), y + 18, col, 4)
        b += M(x_of(t), y - 28, lab, 30, col)
    b += circ(x_of(mid), y, 12, RED, '#fff', 3)
    b += M(x_of(mid), y + 52, '√3', 32, RED)
    b += M(500, 40, '1.7² = 2.89 < 3 < 3.24 = 1.8²', 32, NAVY)
    return svg(1000, 250, b, '30vh')


# ---------------------------------------------------------------- spiral of roots √2 … √5
def _spiral_pts(n=5):
    """P0 = (1,0), P1 = (1,1), then each next point is 1 unit from the last, 90° from the direction toward the origin.
    Distance from the origin of P_k is √(k+1)."""
    P = [(1.0, 0.0), (1.0, 1.0)]
    assert abs(math.hypot(*P[0]) ** 2 - 1) < 1e-9
    assert abs(math.hypot(*P[1]) ** 2 - 2) < 1e-9
    for k in range(2, n):
        ax, ay = P[-1]
        vx, vy = -ax, -ay
        rx, ry = -vy, vx
        L = math.hypot(rx, ry)
        nx, ny = ax + rx / L, ay + ry / L
        P.append((nx, ny))
        assert abs(math.hypot(nx, ny) ** 2 - (k + 1)) < 1e-8
    return P


def root_spiral():
    """the spiral of square roots: triangles with a leg of 1; the hypotenuses are sqrt2, sqrt3, 2, sqrt5. The picture is fitted to its own size."""
    P = _spiral_pts(5)
    O0 = (0.0, 0.0)
    xs = [q[0] for q in P] + [0.0]
    ys = [q[1] for q in P] + [0.0]
    W, H, pad = 1000, 560, 70
    s = min((W - 2 * pad) / (max(xs) - min(xs)), (H - 2 * pad - 20) / (max(ys) - min(ys)))
    ox = pad + (W - 2 * pad - s * (max(xs) - min(xs))) / 2 - min(xs) * s
    oy = H - pad - 10 + min(ys) * s
    X = lambda q: (ox + q[0] * s, oy - q[1] * s)
    O = X(O0)
    pts = [X(q) for q in P]
    cols = [TEAL, '#1c7ed6', '#2f9e44', '#f08c00', '#ae3ec9']
    b = ''
    for i in range(len(pts) - 1):                                    # the outer sides, each of length 1
        b += rvg(i + 1, line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], ORANGE, 5))
    b += line(O[0], O[1], pts[0][0], pts[0][1], ORANGE, 5) + M((O[0] + pts[0][0]) / 2, O[1] + 40, '1', 30, ORANGE)
    labs = {1: '√2', 2: '√3', 3: '√4 = 2', 4: '√5'}
    for i in range(len(pts)):
        g = line(O[0], O[1], pts[i][0], pts[i][1], cols[i], 5) + circ(pts[i][0], pts[i][1], 8, cols[i])
        if i:
            mx, my = (O[0] + pts[i][0]) / 2, (O[1] + pts[i][1]) / 2
            dx, dy = pts[i][1] - O[1], -(pts[i][0] - O[0])
            ln = math.hypot(dx, dy) or 1
            g += M(mx + dx / ln * 34, my + dy / ln * 34, labs[i], 30, cols[i], halo=True)
        b += rvg(i, g) if i else g
    b += circ(O[0], O[1], 8, NAVY)
    return svg(W, H, b, '52vh')




# ---------------------------------------------------------------- one cube, volume 64, edge 4
def cube64():
    """a cube of volume 64: every edge x, x^3 = 64, x = cube root of 64 = 4"""
    assert 4 ** 3 == 64
    F = [(90, 190), (350, 190), (350, 450), (90, 450)]
    top = [(90, 190), (350, 190), (430, 130), (170, 130)]
    right = [(350, 190), (430, 130), (430, 390), (350, 450)]
    b = poly(top, '#b2f2bb', TEAL, 4) + poly(right, '#8ce99a', TEAL, 4) + poly(F, '#d3f9d8', TEAL, 4)
    b += M(220, 335, 'V = 64', 40, NAVY)
    b += rvg(1, M(220, 490, 'x', 38, RED) + M(462, 300, 'x', 38, RED, 'start') + M(60, 330, 'x', 38, RED, 'end'))
    b += rvg(2, M(700, 260, 'x³ = 64', 44, NAVY, 'start') + M(700, 330, 'x = ∛64 = 4', 44, RED, 'start'))
    return svg(1000, 540, b, '48vh')




# ---------------------------------------------------------------- area model √4 · √9 = √36
def area_product():
    assert 2 * 3 == 6 and 4 * 9 == 36 and 6 * 6 == 36
    # width 2 units, height 3 units, cell 70
    c = 78
    x, y = 80, 40
    b = ''
    for i in range(3):
        for j in range(2):
            b += rect(x + j * c, y + i * c, c - 6, c - 6, '#d0ebff', 6, BLUE, 3)
    b += M(x + c - 3, y + 1.5 * c + 14, '6', 44, NAVY, halo=True)
    b += M(x + c, y + 3 * c + 36, '√4 = 2', 30, BLUE)
    b += M(x + 2 * c + 20, y + 1.5 * c, '√9 = 3', 30, TEAL, 'start')
    b += M(620, 160, '√4 × √9', 36, NAVY, 'start')
    b += M(620, 220, '= √36', 36, NAVY, 'start')
    b += M(620, 280, '= 6', 36, RED, 'start')
    return svg(1000, 360, b, '40vh')


# ---------------------------------------------------------------- √18 = 3√2 as nine squares of area 2
def simplify_18():
    assert 9 * 2 == 18 and 3 * 3 == 9
    c = 78
    x, y = 60, 50
    b = ''
    for i in range(3):
        for j in range(3):
            b += rect(x + j * c, y + i * c, c - 6, c - 6, '#fff3bf', 6, GOLD, 3)
            b += M(x + j * c + (c - 6) / 2, y + i * c + (c - 6) / 2 + 8, '2', 26, NAVY)
    b += M(x + 1.5 * c, y + 3 * c + 28, '3√2', 32, RED)
    b += M(x - 16, y + 1.5 * c, '3√2', 32, RED, 'end')
    b += M(620, 140, '√18 = √(9 × 2)', 32, NAVY, 'start')
    b += M(620, 200, '= 3√2', 36, RED, 'start')
    b += TMX(620, 270, [('ផ្ទៃ', False), ('9 × 2 = 18', True)], 30, TEAL, 'start')
    return svg(1000, 380, b, '42vh')


# ---------------------------------------------------------------- rationalise 3/√2 step by step
def rationalise_steps():
    assert 2 > 0
    # three stacked states; reveal shows one at a time
    def frac(cx, num, den, col=NAVY):
        return (M(cx, 70, num, 36, col) + line(cx - 70, 88, cx + 70, 88, col, 4) + M(cx, 130, den, 36, col))
    b = rvg(0, frac(180, '3', '√2', RED) + T(180, 200, 'ដើម', 26, RED))
    b += rvg(1, M(400, 100, '×', 40, NAVY) + frac(560, '√2', '√2', TEAL) + TMX(560, 200, [('គុណនឹង', False), ('√2', True)], 28, TEAL), until=2)
    b += rvg(2, frac(780, '3√2', '2', GREEN) + T(780, 200, 'បាន', 26, GREEN))
    return svg(1000, 250, b, '32vh')


# ---------------------------------------------------------------- cube roots squeezed: 2³ < 17 < 3³
def squeeze_cbrt17():
    assert 2 ** 3 == 8 < 17 < 27 == 3 ** 3
    y = 120
    xs = {2: 180, 3: 780}
    b = line(60, y, 940, y, NAVY, 5)
    b += f'<polygon points="960,{y} 936,{y-11} 936,{y+11}" fill="{NAVY}"/>'
    b += line(xs[2], y - 14, xs[2], y + 14, NAVY, 4) + M(xs[2], y + 50, '2', 32, NAVY)
    b += line(xs[3], y - 14, xs[3], y + 14, NAVY, 4) + M(xs[3], y + 50, '3', 32, NAVY)
    mid = (xs[2] + xs[3]) / 2
    b += circ(mid, y, 12, RED, '#fff', 3) + M(mid - 22, y - 46, '3', 18, RED) + M(mid + 8, y - 26, '√17', 30, RED)
    b += M(500, 40, '2³ = 8 < 17 < 27 = 3³', 34, NAVY)
    return svg(1000, 220, b, '28vh')


PREVIEW = ['number_sets', 'garden_square', 'sqrt2_compass', 'square_area2', 'squeeze_sqrt3', 'root_spiral', 'cube64', 'area_product', 'simplify_18', 'rationalise_steps', 'squeeze_cbrt17']


# ---------------------------------------------------------------- the parts of a radical (the book's own figure: index, radical sign, radicand, exponent)
def radical_anatomy():
    """the n-th root of a^m with its four named parts: the radical sign is drawn by hand (check mark and bar), so each part has its own place"""
    OR, TE, GR = '#e8590c', TEAL, GREY
    b = f'<path d="M 390 262 L 408 250 L 436 322 L 470 196 L 690 196" fill="none" stroke="{GR}" stroke-width="9" stroke-linejoin="round" stroke-linecap="round"/>'
    b += M(560, 300, 'a', 120, TE, 'middle', 700) + M(640, 240, 'm', 64, OR, 'middle', 700) + M(432, 222, 'n', 60, OR, 'middle', 700)
    parts = [('សន្ទស្សន៍', OR, (200, 90), (418, 192)), ('និទស្សន្ត', OR, (840, 90), (650, 215)),
             ('សញ្ញារ៉ាឌីកាល់', GR, (200, 410), (440, 300)), ('រ៉ាឌីកង់', TE, (820, 410), (590, 322))]
    for k, (name, col, (tx, ty), (px, py)) in enumerate(parts):
        b += rvg(k + 1, T(tx, ty, name, 38, col) + arrow(tx + (70 if tx < 500 else -70), ty + (14 if ty < 200 else -40), px, py, col, 5))
    return svg(1000, 470, b, '52vh')




# ---------------------------------------------------------------- like radicals: pieces of the same length add, pieces of different lengths do not
def like_radicals():
    """3 sqrt2 + 4 sqrt2 = 7 sqrt2 as bars of length sqrt2 laid end to end; sqrt3 bars are a different length, so 3 sqrt2 + 4 sqrt3 stays as it is"""
    u2, u3 = math.sqrt(2) * 70, math.sqrt(3) * 70
    assert abs(7 * u2 - (3 * u2 + 4 * u2)) < 1e-9 and abs(u3 - u2) > 10
    x0, y = 60, 90
    b = ''
    for i in range(3):
        b += rvg(1, rect(x0 + i * u2, y, u2 - 4, 44, '#d0ebff', 6, BLUE, 3))
    for i in range(4):
        b += rvg(2, rect(x0 + (3 + i) * u2, y, u2 - 4, 44, '#ffe3b3', 6, ORANGE, 3))
    b += rvg(1, M(x0 + 1.5 * u2, y - 14, '3√2', 34, BLUE)) + rvg(2, M(x0 + 5 * u2, y - 14, '4√2', 34, ORANGE))
    b += rvg(3, line(x0, y + 96, x0 + 7 * u2 - 4, y + 96, RED, 6) + M(x0 + 3.5 * u2, y + 150, '3√2 + 4√2 = 7√2', 40, RED))
    y2 = y + 220
    for i in range(3):
        b += rvg(4, rect(x0 + i * u2, y2, u2 - 4, 44, '#d0ebff', 6, BLUE, 3))
    for i in range(4):
        b += rvg(4, rect(x0 + 3 * u2 + i * u3, y2, u3 - 4, 44, '#d3f9d8', 6, GREEN, 3))
    b += rvg(4, M(x0 + 1.5 * u2, y2 - 14, '3√2', 34, BLUE) + M(x0 + 3 * u2 + 2 * u3, y2 - 14, '4√3', 34, GREEN))
    b += rvg(5, M(500, y2 + 100, 'ប្រវែងខុសគ្នា → បូកមិនបាន', 34, NAVY).replace('font-style="italic"', ''))
    return svg(1000, 470, b, '52vh')


# ---------------------------------------------------------------- the map of the lesson: six steps, each builds on the one before
def lesson_map():
    boxes = [('1', '√a', 'ឫសការេ និងចំនួនអសនិទាន', '#1c7ed6'), ('2', '∛a', 'ឫសគូប', '#2b8a87'), ('3', '√a · √b = √ab', 'គុណ និងចែករ៉ាឌីកាល់', '#2f9e44'),
             ('4', '3√2 = √18', 'បញ្ចេញ និងបញ្ចូល', '#f08c00'), ('5', '3√2 + 4√2', 'បូក និងដក', '#e8590c'), ('6', '1/√2 = √2/2', 'បំបាត់រ៉ាឌីកាល់ពីភាគបែង', '#ae3ec9')]
    b = ''
    pos = [(60, 70), (370, 70), (680, 70), (680, 270), (370, 270), (60, 270)]       # a snake: left to right, then back
    for k, ((no, expr, name, col), (x, y)) in enumerate(zip(boxes, pos)):
        g = rect(x, y, 260, 150, '#fff', 20, col, 5) + circ(x + 34, y + 34, 22, col) + M(x + 34, y + 44, no, 30, '#fff')
        g += M(x + 130, y + 88, expr, 38, col) + T(x + 130, y + 132, name, 22, NAVY)
        b += rvg(k, g) if k else g
    for k, (a, c) in enumerate(((0, 1), (1, 2), (2, 3), (3, 4), (4, 5))):
        (x1, y1), (x2, y2) = pos[a], pos[c]
        if y1 == y2:
            xa, xb = (x1 + 262, x2 - 2) if x2 > x1 else (x1 - 2, x2 + 262)
            b += rvg(k + 1, arrow(xa, y1 + 75, xb, y2 + 75, GREY, 6))
        else:
            b += rvg(k + 1, arrow(x1 + 130, y1 + 152, x2 + 130, y2 - 2, GREY, 6))
    return svg(1000, 470, b, '56vh')
