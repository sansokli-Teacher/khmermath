"""Geometry pictures for Grade 9 Lesson 13 «រង្វង់និងបន្ទាត់». Everything is computed from coordinates (nothing is traced from the book),
and the properties the lesson teaches are asserted for every figure: a tangent is perpendicular to its radius, equal chords are equidistant, tangents from a point are equal ...
Maths labels are typeset (KaTeX in a foreignObject); pieces appear with the slide's reveal steps (rvg) and fade in smoothly."""
import math, os, re, sys
HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, '..', 'lesson1'))
sys.path.insert(0, os.path.join(HERE, '..', 'lesson9_1'))
from lib import svg, rvg, T, line as _line
from vis_book import KT

_CUR = [None]      # the picture being built: every line, circle and label is registered in it so that labels can step aside (see Cv.out)

INK, BLUE, RED, GREEN, ORANGE, PURPLE, GREY = '#1f4a5f', '#1c7ed6', '#e03131', '#2f9e44', '#e8590c', '#ae3ec9', '#7d8791'
FILL = '#eef5fb'


def pol(c, r, deg):
    """point at distance r from c, angle deg counter-clockwise (screen y points down)"""
    a = math.radians(deg)
    return (c[0] + r * math.cos(a), c[1] - r * math.sin(a))


def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def mid(a, b):
    return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)


def unit(a, b):
    d = dist(a, b)
    return ((b[0] - a[0]) / d, (b[1] - a[1]) / d)


def foot(p, a, b):
    """foot of the perpendicular from p to the line ab"""
    ux, uy = unit(a, b)
    t = (p[0] - a[0]) * ux + (p[1] - a[1]) * uy
    return (a[0] + t * ux, a[1] + t * uy)


def near(a, b, tol=1e-6):
    return abs(a - b) <= tol * max(1, abs(b))


# ---------------------------------------------------------------- primitives (each returns svg text)
def _reg(**it):
    if _CUR[0] is not None:
        _CUR[0].items.append(it)


def circle(c, r, col=INK, w=5, fill='none'):
    if col != 'none' and w:
        _reg(k='circ', c=c, r=r)
    return f'<circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="{r:.1f}" fill="{fill}" stroke="{col}" stroke-width="{w}"/>'


def seg(a, b, col=INK, w=5, dash=''):
    _reg(k='seg', a=a, b=b)
    return _line(f'{a[0]:.1f}', f'{a[1]:.1f}', f'{b[0]:.1f}', f'{b[1]:.1f}', col, w, dash)


def ext(a, b, k0=0.0, k1=0.0):
    """the line through a and b, extended by k0 beyond a and k1 beyond b (as multiples of the length ab)"""
    ux, uy = unit(a, b)
    d = dist(a, b)
    return ((a[0] - ux * d * k0, a[1] - uy * d * k0), (b[0] + ux * d * k1, b[1] + uy * d * k1))


def dot(p, col=INK, r=6.5):
    _reg(k='pt', p=p, r=r)
    return f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="{r}" fill="{col}"/>'


def lab(p, tex, dx=0, dy=0, col=INK, size=40, w=150, maxr=66, anchor=None):
    """typeset label centred at p + (dx, dy); inside a picture it is only a placeholder: Cv.out() moves it a little if it would sit on a line or on another label"""
    if _CUR[0] is None:
        return KT(p[0] + dx, p[1] + dy, tex, size, col, w=w)
    cv = _CUR[0]
    i = sum(1 for it in cv.items if it['k'] == 'lab')
    cv.items.append(dict(k='lab', i=i, x=p[0] + dx, y=p[1] + dy, d=(dx, dy), tex=tex, size=size, col=col, w=w, maxr=maxr, anchor=anchor))
    return f'@@L{i}@@'


def _est_w(tex, size):
    """rough printed width of a KaTeX label (px), enough to keep labels off the lines"""
    t = re.sub(r'\\text\{([^}]*)\}', r'\1', tex).replace('\\ ', ' ').replace('^\\circ', '\u00b0').replace("'", '\u2032')
    t = re.sub(r'\\[a-zA-Z]+', 'x', t)
    t = re.sub(r'[{}^_]', '', t)
    return sum(0.34 if ch in ' .,\u2032\u00b0' else 0.64 for ch in t) * size


def poly(pts, fill, stroke='none', w=0, op=1):
    s = ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts)
    return f'<polygon points="{s}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" fill-opacity="{op}" stroke-linejoin="round"/>'


def rightmark(v, p1, p2, s=20, col=INK, w=3):
    """the little square of a right angle at v between the directions to p1 and p2"""
    u1, u2 = unit(v, p1), unit(v, p2)
    assert abs(u1[0] * u2[0] + u1[1] * u2[1]) < 1e-3, 'not a right angle'
    a = (v[0] + u1[0] * s, v[1] + u1[1] * s)
    b = (a[0] + u2[0] * s, a[1] + u2[1] * s)
    c = (v[0] + u2[0] * s, v[1] + u2[1] * s)
    _reg(k='seg', a=a, b=b)
    _reg(k='seg', a=b, b=c)
    return f'<polyline points="{a[0]:.1f},{a[1]:.1f} {b[0]:.1f},{b[1]:.1f} {c[0]:.1f},{c[1]:.1f}" fill="none" stroke="{col}" stroke-width="{w}"/>'


def tick(a, b, n=1, col=RED, size=11, w=4, at=0.5):
    """n small marks across segment ab (at = where along it, 0.5 = the middle); equal segments carry the same number of marks"""
    m, (ux, uy) = (a[0] + (b[0] - a[0]) * at, a[1] + (b[1] - a[1]) * at), unit(a, b)
    out = ''
    for k in range(n):
        o = (k - (n - 1) / 2) * 9
        cx, cy = m[0] + ux * o, m[1] + uy * o
        _reg(k='seg', a=(cx - uy * size, cy + ux * size), b=(cx + uy * size, cy - ux * size))
        out += _line(f'{cx - uy * size:.1f}', f'{cy + ux * size:.1f}', f'{cx + uy * size:.1f}', f'{cy - ux * size:.1f}', col, w)
    return out


def arc(v, a0, a1, r, col=ORANGE, w=4, fill=''):
    """arc around v from angle a0 to a1 (degrees, counter-clockwise on screen); fill = colour for a pie slice"""
    p0, p1 = pol(v, r, a0), pol(v, r, a1)
    large = 1 if (a1 - a0) % 360 > 180 else 0
    n_ = 10
    span = (a1 - a0) % 360
    for i in range(n_):
        _reg(k='seg', a=pol(v, r, a0 + span * i / n_), b=pol(v, r, a0 + span * (i + 1) / n_))
    d = f'M {p0[0]:.1f} {p0[1]:.1f} A {r} {r} 0 {large} 0 {p1[0]:.1f} {p1[1]:.1f}'
    if fill:
        return f'<path d="M {v[0]:.1f} {v[1]:.1f} L {p0[0]:.1f} {p0[1]:.1f} A {r} {r} 0 {large} 0 {p1[0]:.1f} {p1[1]:.1f} Z" fill="{fill}" fill-opacity=".35" stroke="{col}" stroke-width="{w}"/>'
    return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}"/>'


def angarc(v, p1, p2, r, col=ORANGE, w=5, fill=''):
    """the arc of the angle p1-v-p2 (always the short way round)"""
    a0, a1 = dir_deg(v, p1), dir_deg(v, p2)
    if (a1 - a0) % 360 > 180:
        a0, a1 = a1, a0
    return arc(v, a0, a1, r, col, w, fill)


def bis(v, p1, p2, r):
    """the point at distance r from v along the bisector of the angle p1-v-p2 (where its label goes)"""
    a0, a1 = dir_deg(v, p1), dir_deg(v, p2)
    if (a1 - a0) % 360 > 180:
        a0, a1 = a1, a0
    return pol(v, r, a0 + ((a1 - a0) % 360) / 2)


def angle_at(v, p1, p2):
    """the angle p1-v-p2 in degrees"""
    a = math.degrees(math.atan2(-(p1[1] - v[1]), p1[0] - v[0]))
    b = math.degrees(math.atan2(-(p2[1] - v[1]), p2[0] - v[0]))
    d = abs(a - b) % 360
    return min(d, 360 - d)


def dir_deg(v, p):
    return math.degrees(math.atan2(-(p[1] - v[1]), p[0] - v[0])) % 360


def tangent_pts(c, r, p):
    """the two points where the tangents from the outside point p touch the circle (c, r)"""
    d = dist(c, p)
    assert d > r
    base = dir_deg(c, p)
    a = math.degrees(math.acos(r / d))
    return pol(c, r, base + a), pol(c, r, base - a)


class Cv:
    def __init__(self, W=640, H=440, maxh='58vh'):
        self.W, self.H, self.maxh, self.parts, self.items, self._mark = W, H, maxh, [], [], 0
        _CUR[0] = self

    def add(self, g, step=0, until=None):
        win = (step, until if until else 10 ** 6)          # the steps during which this group is on screen
        for it in self.items[self._mark:]:
            it['win'] = win
        self._mark = len(self.items)
        self.parts.append(rvg(step, g, until) if (step or until) else g)
        return self

    def _place_labels(self, body):
        """a label keeps the spot it was given unless it would touch a line, a point or another label that is on screen at the same time;
        then it takes the nearest free spot (tried in rings around it), so no label ever sits on a line"""
        for it in self.items[self._mark:]:
            it['win'] = (0, 10 ** 6)
        obst = []
        for it in self.items:
            k = it['k']
            if k == 'seg':
                a, b = it['a'], it['b']
                n = max(1, int(dist(a, b) / 3))
                pts = [(a[0] + (b[0] - a[0]) * j / n, a[1] + (b[1] - a[1]) * j / n) for j in range(n + 1)]
            elif k == 'circ':
                c, r = it['c'], it['r']
                n = max(12, int(2 * math.pi * r / 3))
                pts = [(c[0] + r * math.cos(2 * math.pi * j / n), c[1] + r * math.sin(2 * math.pi * j / n)) for j in range(n)]
            elif k == 'pt':
                pts = [(it['p'][0] + dx_, it['p'][1] + dy_) for dx_ in (-it['r'], 0, it['r']) for dy_ in (-it['r'], 0, it['r'])]
            else:
                continue
            obst.append((pts, it['win']))
        labs = [it for it in self.items if it['k'] == 'lab']
        placed = []
        for L in labs:
            hw, hh = _est_w(L['tex'], L['size']) * .5 + 6, L['size'] * .36 + 6
            lo, hi = L['win']
            live = [pts for pts, (s0, u0) in obst if max(lo, s0) < min(hi, u0)]
            def cost(cx, cy):
                x0, x1, y0, y1 = cx - hw, cx + hw, cy - hh, cy + hh
                n = 0
                for pts in live:
                    for px, py in pts:
                        if x0 < px < x1 and y0 < py < y1:
                            n += 1
                for (ox0, ox1, oy0, oy1, (s0, u0)) in placed:
                    if max(lo, s0) < min(hi, u0) and x0 < ox1 + 3 and ox0 < x1 + 3 and y0 < oy1 + 3 and oy0 < y1 + 3:
                        n += 40
                if x0 < 2 or y0 < 2 or x1 > self.W - 2 or y1 > self.H - 2:
                    n += 400
                return n
            dx0, dy0 = L['d']
            best = (cost(L['x'], L['y']), 0, L['x'], L['y'])
            if best[0] > 0:
                base = math.atan2(dy0, dx0) if (dx0 or dy0) else 0
                for rad in [q_ for q_ in (10, 20, 30, 42, 54, 66) if q_ <= L['maxr']]:
                    for q in (0, 1, -1, 2, -2, 3, -3, 4):
                        ang = base + q * math.pi / 4
                        cx, cy = L['x'] + rad * math.cos(ang), L['y'] + rad * math.sin(ang)
                        c_ = cost(cx, cy)
                        if c_ * 100 + rad < best[0] * 100 + best[1]:
                            best = (c_, rad, cx, cy)
                    if best[0] == 0:
                        break
            L['final'], L['left'] = (best[2], best[3]), best[0]
            placed.append((best[2] - hw, best[2] + hw, best[3] - hh, best[3] + hh, L['win']))
            lead = ''
            if L['anchor'] is not None:                              # an angle label that had to move gets a thin leader back to its arc
                ax, ay = L['anchor']
                ddx, ddy = ax - best[2], ay - best[3]
                if math.hypot(ddx, ddy) > max(hw, hh) + 10:
                    k_ = min(hw / abs(ddx) if ddx else 9e9, hh / abs(ddy) if ddy else 9e9)
                    lead = _line(f'{best[2] + ddx * k_:.1f}', f'{best[3] + ddy * k_:.1f}', f'{ax:.1f}', f'{ay:.1f}', L['col'], 2)
            body = body.replace(f'@@L{L["i"]}@@', lead + KT(best[2], best[3], L['tex'], L['size'], L['col'], w=L['w']))
        self.unplaced = [(L['tex'], round(L['left'])) for L in labs if L['left']]
        return body

    def out(self):
        body = self._place_labels(''.join(self.parts))
        _CUR[0] = None
        if self.unplaced:
            print('  label left on a line:', self.unplaced)
        assert '@@L' not in body
        return svg(self.W, self.H, body, self.maxh)


# ================================================================ 1.1 a line from the centre, perpendicular to a chord
def chord_perp(show_fold=True):
    """circle O, chord AB, OM perpendicular to AB at M: M is the midpoint. steps: 1 the perpendicular, 2 equal halves"""
    O, r = (320, 215), 170
    d = 80
    half = math.sqrt(r * r - d * d)
    M = (O[0], O[1] + d)
    A, B = (M[0] - half, M[1]), (M[0] + half, M[1])
    assert near(dist(O, A), r) and near(dist(O, B), r) and near(dist(A, M), dist(M, B))
    c = Cv(640, 440)
    c.add(circle(O, r, fill=FILL) + seg(A, B, INK, 6) + dot(O) + dot(A) + dot(B) + lab(O, 'O', -26, -22) + lab(A, 'A', -30, 6) + lab(B, 'B', 30, 6))
    c.add(seg(O, M, BLUE, 4, '10 7') + dot(M, BLUE) + rightmark(M, O, B, 20, BLUE) + lab(M, 'M', 28, 28, BLUE), 1)
    c.add(tick(A, M, 1, RED) + tick(M, B, 1, RED), 2)
    return c.out()


def chord_perp_ex(ab_label='10', find='AC', pt='C'):
    """book example 1: chord AB = 10 cm, OC perpendicular to AB at C"""
    O, r = (320, 210), 165
    d = 70
    half = math.sqrt(r * r - d * d)
    C = (O[0], O[1] + d)
    A, B = (C[0] - half, C[1]), (C[0] + half, C[1])
    c = Cv(640, 440)
    c.add(circle(O, r, fill=FILL) + seg(A, B, INK, 6) + dot(O) + dot(A) + dot(B) + lab(O, 'O', -24, -22) + lab(A, 'A', -30, 4) + lab(B, 'B', 30, 4))
    c.add(seg(O, C, BLUE, 4, '10 7') + dot(C, BLUE) + rightmark(C, O, B, 20, BLUE) + lab(C, 'C', 26, -22, BLUE), 1)
    c.add(lab(mid(A, B), r'10\ \text{cm}', 0, 46, GREEN, 36, 220), 0)
    c.add(tick(A, C, 1, RED, 11, 4, .75) + tick(C, B, 1, RED, 11, 4, .25) + lab(mid(A, C), r'?', 0, -28, RED, 44), 2)
    return c.out()


def chord_ex2():
    """book example 2: OM = 5, OB = 7, find AB (Pythagoras in triangle OMB)"""
    u = 24
    O, r = (320, 200), 7 * u
    M = (O[0], O[1] + 5 * u)
    hb = math.sqrt(r * r - (5 * u) ** 2)
    A, B = (M[0] - hb, M[1]), (M[0] + hb, M[1])
    assert near(hb / u, math.sqrt(24))
    c = Cv(640, 440)
    c.add(circle(O, r, fill=FILL) + seg(A, B, INK, 6) + dot(O) + dot(A) + dot(B) + lab(O, 'O', -26, -22) + lab(A, 'A', -30, 4) + lab(B, 'B', 30, 4))
    c.add(poly([O, M, B], '#ffe3a3', op=.55) + seg(O, M, BLUE, 5) + seg(O, B, BLUE, 5) + seg(M, B, BLUE, 5) + dot(M, BLUE) + rightmark(M, O, B, 20, BLUE) + lab(M, 'M', -26, 30, BLUE)
          + lab(mid(O, M), r'5\ \text{cm}', -62, 0, BLUE, 34, 200) + lab(mid(O, B), r'7\ \text{cm}', 56, -24, BLUE, 34, 200), 1)
    c.add(lab(mid(M, B), r'?', 0, 28, RED, 44), 2)
    return c.out()


def chord_ex3():
    """book example 3: angle OXY = 30, angle XOY = 60, XZ = 32; so angle OYX = 90 and Y is the midpoint of XZ"""
    O, r = (240, 220), 170
    Y = (O[0] + r * math.cos(math.radians(60)), O[1])
    X = (Y[0], O[1] - r * math.sin(math.radians(60)))
    Z = (Y[0], O[1] + r * math.sin(math.radians(60)))
    assert near(angle_at(O, X, Y), 60) and near(angle_at(X, O, Y), 30) and near(dist(X, Y), dist(Y, Z))
    c = Cv(640, 440)
    c.add(circle(O, r, fill=FILL) + seg(X, Z, INK, 6) + seg(O, X, INK, 5) + dot(O) + dot(X) + dot(Z) + lab(O, 'O', -26, 0) + lab(X, 'X', 8, -28) + lab(Z, 'Z', 8, 30)
          + lab(mid(X, Z), r'32\ \text{cm}', 100, 0, GREEN, 34, 220))
    c.add(angarc(X, O, Y, 46, BLUE) + lab(X, r'30^\circ', -62, 62, BLUE, 30, 130) + angarc(O, X, Y, 50, ORANGE) + lab(bis(O, X, Y, 82), r'60^\circ', 0, 0, ORANGE, 26, 120), 1)
    c.add(seg(O, Y, BLUE, 4, '10 7') + dot(Y, BLUE) + rightmark(Y, O, X, 20, BLUE) + lab(Y, 'Y', -22, 26, BLUE), 2)
    c.add(tick(X, Y, 1, RED, 11, 4, .5) + tick(Y, Z, 1, RED, 11, 4, .5), 3)
    return c.out()


def chord_prac1():
    """practice: AB = 25, BQ = 6.5 (perpendiculars from O to the chords BA and BC); find AP and BC"""
    O, r = (320, 215), 170
    k = 2 * r * 0.9 / 25
    ab, bc = 25 * k, 13 * k
    dA, dC = 2 * math.degrees(math.asin(ab / (2 * r))), 2 * math.degrees(math.asin(bc / (2 * r)))
    angB = 215
    B = pol(O, r, angB)
    A, C = pol(O, r, angB + dA), pol(O, r, angB - dC)
    P, Q = mid(A, B), mid(B, C)
    assert near(dist(A, B) / dist(B, C), 25 / 13, 1e-6)
    cv = Cv(640, 440)
    cv.add(circle(O, r, fill=FILL) + seg(A, B, INK, 6) + seg(B, C, INK, 6) + dot(O) + dot(A) + dot(B) + dot(C) + lab(O, 'O', 24, -8) + lab(A, 'A', 28, 4) + lab(B, 'B', -28, 14) + lab(C, 'C', -14, -30))
    cv.add(seg(O, P, BLUE, 4, '10 7') + seg(O, Q, BLUE, 4, '10 7') + dot(P, BLUE) + dot(Q, BLUE) + rightmark(P, O, A, 18, BLUE) + rightmark(Q, O, C, 18, BLUE) + lab(P, 'P', 8, 30, BLUE) + lab(Q, 'Q', 26, -20, BLUE), 1)
    cv.add(lab(A, r'25\ \text{cm}', 20, 56, GREEN, 30, 200) + lab(mid(B, Q), r'6.5\ \text{cm}', -90, -2, GREEN, 30, 200), 0)
    return cv.out()


# ================================================================ 1.2 equal chords
def equal_chords():
    """circle O (r = 4 cm), equal chords AB and CD, their distances OM and ON are equal. steps: 1 the distances, 2 equal marks"""
    O, r = (320, 215), 170
    d = 85
    half = math.sqrt(r * r - d * d)
    M, N = pol(O, d, 190), pol(O, d, 350)
    def chord(Mp, ang):
        t = ang + 90
        e = (math.cos(math.radians(t)), -math.sin(math.radians(t)))
        return (Mp[0] + e[0] * half, Mp[1] + e[1] * half), (Mp[0] - e[0] * half, Mp[1] - e[1] * half)
    A, B = chord(M, 190)
    C, D = chord(N, 350)
    assert near(dist(A, B), dist(C, D)) and near(dist(O, M), dist(O, N)) and near(dist(O, A), r) and near(dist(O, D), r)
    c = Cv(640, 440)
    c.add(circle(O, r, fill=FILL) + seg(A, B, INK, 6) + seg(C, D, INK, 6) + dot(O) + dot(A) + dot(B) + dot(C) + dot(D) + lab(O, 'O', 4, -26)
          + lab(A, 'A', -4, -28) + lab(B, 'B', -8, 30) + lab(C, 'C', 8, 30) + lab(D, 'D', 6, -28) + tick(A, B, 2, RED, 11, 4, .8) + tick(C, D, 2, RED, 11, 4, .8))
    c.add(seg(O, M, BLUE, 4, '10 7') + seg(O, N, BLUE, 4, '10 7') + dot(M, BLUE) + dot(N, BLUE) + rightmark(M, O, A, 18, BLUE) + rightmark(N, O, C, 18, BLUE) + lab(M, 'M', -30, 0, BLUE) + lab(N, 'N', 30, 0, BLUE), 1)
    c.add(tick(O, M, 1, GREEN, 12, 5) + tick(O, N, 1, GREEN, 12, 5), 2)
    return c.out()


def chord_dist_ex1():
    """r = 5, chord 8: the distance from O is 3"""
    u = 30
    O, r = (320, 200), 5 * u
    M = (O[0], O[1] + 3 * u)
    A, B = (M[0] - 4 * u, M[1]), (M[0] + 4 * u, M[1])
    assert near(dist(O, B), r)
    c = Cv(640, 440)
    c.add(circle(O, r, fill=FILL) + seg(A, B, INK, 6) + dot(O) + dot(A) + dot(B) + lab(O, 'O', -26, -20) + lab(A, 'A', -30, 4) + lab(B, 'B', 30, 4) + lab(B, r'8\ \text{cm}', -64, 54, GREEN, 32, 200))
    c.add(poly([O, M, B], '#ffe3a3', op=.55) + seg(O, M, BLUE, 5) + seg(O, B, BLUE, 5) + dot(M, BLUE) + rightmark(M, O, B, 20, BLUE) + lab(M, 'M', -26, 26, BLUE)
          + lab(mid(O, B), r'5', 26, -20, BLUE, 38, 80) + lab(mid(M, B), r'4', 0, 26, BLUE, 36, 80), 1)
    c.add(lab(mid(O, M), r'?', -34, 0, RED, 44), 2)
    return c.out()


def chord_dist_ex2():
    """r = 5, PQ = RS = 6: OX = OY = 4"""
    u = 32
    O, r = (330, 215), 5 * u
    X, Y = (O[0], O[1] - 4 * u), (O[0] - 4 * u, O[1])
    P, Q = (X[0] - 3 * u, X[1]), (X[0] + 3 * u, X[1])
    S, R = (Y[0], Y[1] - 3 * u), (Y[0], Y[1] + 3 * u)
    assert near(dist(O, P), r) and near(dist(O, S), r) and near(dist(P, Q), dist(S, R))
    c = Cv(640, 440)
    c.add(circle(O, r, fill=FILL) + seg(P, Q, INK, 6) + seg(S, R, INK, 6) + dot(O) + dot(P) + dot(Q) + dot(S) + dot(R) + lab(O, 'O', 24, 20)
          + lab(P, 'P', -6, -28) + lab(Q, 'Q', 8, -28) + lab(S, 'S', -30, -6) + lab(R, 'R', -26, 24) + tick(P, Q, 2, RED, 11, 4, .8) + tick(S, R, 2, RED, 11, 4, .2))
    c.add(seg(O, X, BLUE, 4, '10 7') + seg(O, Y, BLUE, 4, '10 7') + seg(O, P, BLUE, 3, '4 5') + dot(X, BLUE) + dot(Y, BLUE) + rightmark(X, O, Q, 18, BLUE) + rightmark(Y, O, R, 18, BLUE)
          + lab(X, 'X', -24, 24, BLUE) + lab(Y, 'Y', 24, 28, BLUE) + lab(mid(O, P), r'5', -4, -4, BLUE, 34, 80), 1)
    c.add(lab(mid(O, X), r'?', 28, 0, RED, 44, 80) + lab(mid(O, Y), r'?', 0, -26, RED, 44, 80), 2)
    return c.out()


def chord_dist_ex3():
    """r = 10, PR = QS, OC = 6 (C and D are the feet of the perpendiculars): OD = 6, PR = 16"""
    u = 17
    O, r = (330, 215), 10 * u
    C, D = pol(O, 6 * u, 200), pol(O, 6 * u, 80)
    def chord(F, ang, half):
        t = ang + 90
        e = (math.cos(math.radians(t)), -math.sin(math.radians(t)))
        return (F[0] - e[0] * half, F[1] - e[1] * half), (F[0] + e[0] * half, F[1] + e[1] * half)
    half = 8 * u
    P, R = chord(C, 200, half)
    Q, S = chord(D, 80, half)
    assert near(dist(O, P), r) and near(dist(O, S), r) and near(dist(P, R), dist(Q, S))
    c = Cv(640, 440)
    c.add(circle(O, r, fill=FILL) + seg(P, R, INK, 6) + seg(Q, S, INK, 6) + dot(O) + dot(P) + dot(R) + dot(Q) + dot(S) + lab(O, 'O', 22, 18)
          + lab(P, 'P', -22, -18) + lab(R, 'R', -22, 22) + lab(Q, 'Q', -26, -8) + lab(S, 'S', 28, -8) + tick(P, R, 2, RED, 11, 4, .15) + tick(Q, S, 2, RED, 11, 4, .15))
    c.add(seg(O, C, BLUE, 4, '10 7') + dot(C, BLUE) + rightmark(C, O, P, 16, BLUE) + lab(C, 'C', -26, 0, BLUE) + lab(mid(O, C), r'6', 4, 26, BLUE, 34, 80)
          + seg(O, D, BLUE, 4, '10 7') + dot(D, BLUE) + rightmark(D, O, Q, 16, BLUE) + lab(D, 'D', 26, 8, BLUE), 1)
    c.add(lab(mid(O, D), r'?', -28, 0, RED, 44, 80), 2)
    return c.out()


def chord_prac2():
    """practice: OA = OB = 5.5 (distances from O to chords NM and NP), MN = 9: NP = 9"""
    O, r = (320, 215), 170
    k = 2 * r * 0.85 / 9
    mn = 9 * k
    dn = 2 * math.degrees(math.asin(mn / (2 * r)))
    angN = 200
    N = pol(O, r, angN)
    M, Pp = pol(O, r, angN + dn), pol(O, r, angN - dn)
    A, B = mid(N, M), mid(N, Pp)
    assert near(dist(O, A), dist(O, B)) and near(dist(N, M), dist(N, Pp))
    c = Cv(640, 440)
    c.add(circle(O, r, fill=FILL) + seg(N, M, INK, 6) + seg(N, Pp, INK, 6) + dot(O) + dot(N) + dot(M) + dot(Pp) + lab(O, 'O', 30, -2) + lab(N, 'N', -30, 0) + lab(M, 'M', 6, -30) + lab(Pp, 'P', 6, 32))
    c.add(seg(O, A, BLUE, 4, '10 7') + seg(O, B, BLUE, 4, '10 7') + dot(A, BLUE) + dot(B, BLUE) + rightmark(A, O, M, 16, BLUE) + rightmark(B, O, Pp, 16, BLUE)
          + lab(A, 'A', -4, 30, BLUE) + lab(B, 'B', -4, -30, BLUE) + lab(mid(O, A), r'5.5', 30, 20, BLUE, 28, 90) + lab(mid(O, B), r'5.5', 30, -20, BLUE, 28, 90) + lab(mid(N, M), r'9', 30, 12, GREEN, 32, 70), 1)
    return c.out()


# ================================================================ 2. the tangent
def tangent_slide():
    """the line l moves down from the diameter AB: A and B come closer and meet at M; l touches the circle. One position per step."""
    O, r = (330, 210), 150
    c = Cv(700, 450)
    c.add(circle(O, r, fill=FILL) + dot(O) + lab(O, 'O', -24, -20))
    ys = [0, 70, 112, 140, r]
    names = ['', '', '', '', 'M']
    for k, dy in enumerate(ys):
        y = O[1] + dy
        half = math.sqrt(max(0, r * r - dy * dy))
        A, B = (O[0] - half, y), (O[0] + half, y)
        L0, L1 = (O[0] - 230, y), (O[0] + 230, y)
        g = seg(L0, L1, BLUE if k < 4 else RED, 5) + (dot(A, ORANGE, 8) + dot(B, ORANGE, 8) if k < 4 else dot((O[0], y), RED, 9))
        if k == 0:
            g += lab(A, 'A', -26, -22, ORANGE) + lab(B, 'B', 26, -22, ORANGE)
        g += lab(L1, 'l', 20, 4, BLUE if k < 4 else RED, 38, 60)
        if k == 4:
            M = (O[0], y)
            g += lab(M, 'M', 0, 30, RED, 40) + rightmark(M, O, L1, 20, RED) + seg(O, M, RED, 3, '8 6')
        c.add(g, k + 1, k + 2 if k < 4 else None)
    return c.out()


def tangent_TA():
    """book exercise: TA is tangent at T, OT = TA: the triangle OTA has angles 90, 45, 45"""
    O, r = (260, 190), 140
    T = (O[0] + r * math.cos(math.radians(-25)), O[1] - r * math.sin(math.radians(-25)))
    tdir = (-(T[1] - O[1]) / r, (T[0] - O[0]) / r)
    A = (T[0] + tdir[0] * r, T[1] + tdir[1] * r)
    assert abs((A[0] - T[0]) * (T[0] - O[0]) + (A[1] - T[1]) * (T[1] - O[1])) < 1e-6 and near(dist(T, A), dist(O, T))
    assert near(angle_at(O, T, A), 45) and near(angle_at(A, T, O), 45)
    c = Cv(640, 440)
    L0, L1 = ext(T, A, 1.1, .5)
    c.add(circle(O, r, fill=FILL) + seg(L0, L1, BLUE, 5) + seg(O, T, INK, 5) + dot(O) + dot(T, RED) + dot(A) + lab(O, 'O', -26, -18) + lab(T, 'T', 24, -24, RED) + lab(A, 'A', 22, 18))
    c.add(rightmark(T, O, A, 22, RED) + tick(O, T, 1, GREEN) + tick(T, A, 1, GREEN) + seg(O, A, INK, 5), 1)
    c.add(angarc(O, T, A, 52, ORANGE) + lab(bis(O, T, A, 86), r'45^\circ', 0, 0, ORANGE, 26, 120) + angarc(A, T, O, 52, ORANGE) + lab(bis(A, T, O, 90), r'45^\circ', 0, 0, ORANGE, 26, 120), 2)
    return c.out()


# ================================================================ 3. properties of the tangent
def tangent_parallel_chord():
    """book example 1: EF tangent at C, AB parallel to EF: C is the midpoint of the arc AB"""
    O, r = (320, 200), 150
    C = (O[0], O[1] + r)
    d = 80
    h = math.sqrt(r * r - (r - d) ** 2)
    A, B = (O[0] - h, C[1] - d), (O[0] + h, C[1] - d)
    N = (O[0], C[1] - d)
    assert near(dist(O, A), r) and near(dist(O, B), r)
    c = Cv(640, 440)
    c.add(circle(O, r, fill=FILL) + seg((C[0] - 250, C[1]), (C[0] + 250, C[1]), BLUE, 5) + seg(A, B, INK, 5) + dot(O) + dot(A) + dot(B) + dot(C, RED)
          + lab(O, 'O', -26, -22) + lab(A, 'A', -28, -10) + lab(B, 'B', 28, -10) + lab(C, 'C', 0, 32, RED) + lab((C[0] - 250, C[1]), 'E', 0, 28, BLUE, 38, 60) + lab((C[0] + 250, C[1]), 'F', 0, 28, BLUE, 38, 60))
    c.add(seg(O, C, RED, 4, '10 7') + rightmark(C, O, (C[0] + 50, C[1]), 20, RED) + rightmark(N, O, B, 18, RED), 1)
    c.add(arc(O, dir_deg(O, A), dir_deg(O, C), r + 14, GREEN, 7) + arc(O, dir_deg(O, C), dir_deg(O, B), r + 14, GREEN, 7), 2)
    return c.out()


def two_tangents(show_chord=False, angle_B=None, mark='all', P_dist=None):
    """tangents AB and AC from the outside point A to the circle O (touching at B and C)"""
    O, r = (190, 215), 130
    A = (O[0] + (P_dist if P_dist else 330), O[1])
    B, C = tangent_pts(O, r, A)
    if B[1] > C[1]:
        B, C = C, B
    assert abs((B[0] - A[0]) * (B[0] - O[0]) + (B[1] - A[1]) * (B[1] - O[1])) < 1e-4 and near(dist(A, B), dist(A, C))
    return O, r, A, B, C


def tangents_slide():
    """book example 2 / rule: AB = AC, angle BAO = angle OAC, angle BOA = angle AOC. steps: 1 radii + right angles, 2 equal tangents, 3 the angles"""
    O, r, A, B, C = two_tangents()
    c = Cv(700, 440)
    L0, L1 = ext(A, B, 0.0, 0.35)
    M0, M1 = ext(A, C, 0.0, 0.35)
    c.add(circle(O, r, fill=FILL) + seg(A, L1, INK, 5) + seg(A, M1, INK, 5) + dot(O) + dot(A) + dot(B, RED) + dot(C, RED) + lab(O, 'O', -22, -4) + lab(A, 'A', 30, 0) + lab(B, 'B', 4, -28, RED) + lab(C, 'C', 4, 30, RED))
    c.add(seg(O, B, BLUE, 4) + seg(O, C, BLUE, 4) + rightmark(B, O, A, 20, BLUE) + rightmark(C, O, A, 20, BLUE) + tick(O, B, 1, BLUE) + tick(O, C, 1, BLUE), 1)
    c.add(seg(O, A, INK, 4, '10 7') + tick(A, B, 2, RED) + tick(A, C, 2, RED), 2)
    c.add(angarc(A, B, O, 74, ORANGE, 4) + angarc(A, O, C, 74, ORANGE, 4) + angarc(O, B, A, 50, GREEN, 4) + angarc(O, A, C, 50, GREEN, 4), 3)
    return c.out()


def two_tangents_ex1():
    """exercise: PA, PB tangents, angle ABP = 63: find AOB and AOP"""
    O, r = (170, 215), 130
    half_p = (180 - 2 * 63) / 2.0                       # angle APB = 54, half of it = 27
    d = r / math.sin(math.radians(half_p))
    P = (O[0] + d, O[1])
    A, B = tangent_pts(O, r, P)
    if A[1] > B[1]:
        A, B = B, A
    assert near(angle_at(B, A, P), 63, 1e-4) and near(angle_at(O, A, B), 126, 1e-4) and near(angle_at(O, A, P), 63, 1e-4)
    c = Cv(700, 440)
    ex1, ex2 = ext(P, A, 0, .25), ext(P, B, 0, .25)
    c.add(circle(O, r, fill=FILL) + seg(P, ex1[1], INK, 5) + seg(P, ex2[1], INK, 5) + seg(A, B, INK, 5) + dot(O) + dot(P) + dot(A) + dot(B) + lab(O, 'O', -20, 4) + lab(P, 'P', 28, 0) + lab(A, 'A', 6, -28) + lab(B, 'B', 6, 30))
    c.add(angarc(B, A, P, 44, ORANGE, 5) + lab(bis(B, A, P, 78), r'63^\circ', 0, 0, ORANGE, 28, 120), 0)
    c.add(seg(O, A, BLUE, 4) + seg(O, B, BLUE, 4) + rightmark(B, O, P, 18, BLUE) + rightmark(A, O, P, 18, BLUE), 1)
    c.add(seg(O, P, INK, 4, '10 7') + angarc(O, A, B, 24, GREEN, 5) + lab(O, r'?', 42, -18, RED, 34, 60), 2)
    return c.out()


def two_tangents_ex2():
    """exercise: TA, TB tangents, r = 9, angle ATB = 110: angle AOB = 70 and the sector AOB"""
    O, r = (170, 215), 140
    half_t = 55.0
    d = r / math.sin(math.radians(half_t))
    Tp = (O[0] + d, O[1])
    A, B = tangent_pts(O, r, Tp)
    if A[1] > B[1]:
        A, B = B, A
    assert near(angle_at(O, A, B), 70, 1e-4) and near(angle_at(Tp, A, B), 110, 1e-4)
    c = Cv(700, 440)
    e1, e2 = ext(Tp, A, 0, .22), ext(Tp, B, 0, .22)
    c.add(circle(O, r, fill=FILL) + seg(Tp, e1[1], INK, 5) + seg(Tp, e2[1], INK, 5) + dot(O) + dot(Tp) + dot(A) + dot(B) + lab(O, 'O', -22, 4) + lab(Tp, 'T', 28, 0) + lab(A, 'A', 4, -28) + lab(B, 'B', 4, 30)
          + lab(mid(O, A), r'9\ \text{cm}', -48, -18, GREEN, 28, 180))
    c.add(angarc(Tp, A, B, 56, ORANGE, 5) + lab(Tp, r'110^\circ', 74, 0, ORANGE, 28, 150), 0)
    c.add(seg(O, A, BLUE, 4) + seg(O, B, BLUE, 4) + rightmark(A, O, Tp, 18, BLUE) + rightmark(B, O, Tp, 18, BLUE), 1)
    c.add(angarc(O, A, B, r - 6, PURPLE, 4, fill=PURPLE) + lab(bis(O, A, B, 70), r'70^\circ', 0, 0, PURPLE, 28, 130), 2)
    return c.out()


def tangents_practice():
    """practice: ST and RT tangents, ST = RT = 20, TQ = 10 (Q on the circle on the line TO): the radius is 15"""
    u = 8
    r = 15 * u
    O = (400, 215)
    Tp = (O[0] - (r + 10 * u), O[1])
    A, B = tangent_pts(O, r, Tp)
    if A[1] > B[1]:
        A, B = B, A
    assert near(dist(Tp, A) / u, 20, 1e-6)
    Q = (O[0] - r, O[1])
    c = Cv(700, 440)
    e1, e2 = ext(Tp, A, 0, .2), ext(Tp, B, 0, .2)
    c.add(circle(O, r, fill=FILL) + seg(Tp, e1[1], INK, 5) + seg(Tp, e2[1], INK, 5) + seg(Tp, O, INK, 5) + dot(O) + dot(Tp) + dot(A) + dot(B) + dot(Q, RED)
          + lab(O, 'O', 24, -4) + lab(Tp, 'T', -26, 0) + lab(A, 'S', 4, -28) + lab(B, 'R', 4, 30) + lab(Q, 'Q', 22, -24, RED)
          + lab(mid(Tp, A), r'20', -22, -26, GREEN, 32, 80) + lab(mid(Tp, Q), r'10', 0, 28, GREEN, 32, 80))
    c.add(seg(O, A, BLUE, 4) + seg(O, B, BLUE, 4) + rightmark(A, O, Tp, 18, BLUE) + rightmark(B, O, Tp, 18, BLUE) + lab(mid(O, A), r'r', 18, -20, RED, 36, 60), 1)
    return c.out()


# ================================================================ 4. a quadrilateral around a circle
def circ_quad(show_equal=True):
    """ABCD with all four sides tangent to the circle (at P on AB, Q on BC, R on CD, S on DA)"""
    O, r = (320, 215), 130
    angP, angQ, angR, angS = 195, 270, 25, 100
    def vertex(a, b):
        mid_a = (a + b) / 2.0
        k = r / math.cos(math.radians((b - a) / 2.0))
        return pol(O, k, mid_a)
    P, Q, R, S = pol(O, r, angP), pol(O, r, angQ), pol(O, r, angR), pol(O, r, angS)
    A = vertex(angS, angP)
    B = vertex(angP, angQ)
    C = vertex(angQ, angR + 360)
    D = vertex(angR, angS)
    for (V, T1) in ((A, P), (A, S), (B, P), (B, Q), (C, Q), (C, R), (D, R), (D, S)):
        assert abs((V[0] - T1[0]) * (T1[0] - O[0]) + (V[1] - T1[1]) * (T1[1] - O[1])) < 1e-3
    assert near(dist(A, B) + dist(C, D), dist(A, D) + dist(B, C), 1e-6)
    c = Cv(700, 450)
    c.add(poly([A, B, C, D], 'none', INK, 5) + circle(O, r, fill=FILL) + dot(O) + lab(O, 'O', 16, -20)
          + dot(P, RED) + dot(Q, RED) + dot(R, RED) + dot(S, RED) + lab(A, 'A', -24, -14) + lab(B, 'B', -22, 20) + lab(C, 'C', 24, 20) + lab(D, 'D', 20, -22)
          + lab(P, 'P', -26, 2, RED) + lab(Q, 'Q', 0, 26, RED) + lab(R, 'R', 24, 0, RED) + lab(S, 'S', -2, -24, RED))
    c.add(''.join(seg(O, X, BLUE, 3, '8 6') + rightmark(X, O, V, 14, BLUE) for X, V in ((P, B), (Q, C), (R, D), (S, A))), 1)
    if show_equal:
        c.add(tick(A, P, 1, GREEN) + tick(A, S, 1, GREEN) + tick(B, P, 2, ORANGE) + tick(B, Q, 2, ORANGE) + tick(C, Q, 3, PURPLE) + tick(C, R, 3, PURPLE) + tick(D, R, 4, RED, 11, 4) + tick(D, S, 4, RED, 11, 4), 2)
    return c.out()


def incircle_isosceles():
    """practice: ABC isosceles with vertex A, circle touching AC at P, AB at Q, BC at R: BR = RC"""
    O, r = (420, 215), 105
    R = (O[0] + r, O[1])
    A = (O[0] - 280, O[1])
    P, Q = tangent_pts(O, r, A)
    if P[1] > Q[1]:
        P, Q = Q, P
    def hit(Tp):                                           # the tangent from A through Tp meets the vertical line x = R.x
        t = (R[0] - A[0]) / (Tp[0] - A[0])
        return (R[0], A[1] + t * (Tp[1] - A[1]))
    C, B = hit(P), hit(Q)
    assert near(dist(A, B), dist(A, C)) and near(dist(B, R), dist(R, C)) and near(dist(A, P), dist(A, Q))
    c = Cv(700, 450)
    c.add(poly([A, B, C], 'none', INK, 5) + circle(O, r, fill=FILL) + dot(O) + dot(P, RED) + dot(Q, RED) + dot(R, RED) + lab(A, 'A', -24, 0) + lab(B, 'B', 22, 22) + lab(C, 'C', 22, -22)
          + lab(P, 'P', -2, -26, RED) + lab(Q, 'Q', -2, 28, RED) + lab(R, 'R', 26, 0, RED))
    c.add(tick(A, P, 1, GREEN) + tick(A, Q, 1, GREEN), 1)
    c.add(tick(B, R, 2, ORANGE) + tick(R, C, 2, ORANGE), 2)
    return c.out()


# ================================================================ 5. two circles
def two_circles(d, r=110, r2=60, show='d', cx=190, cy=215, w=700):
    """circles O (r) and O' (r2) with distance d between the centres"""
    O, O2 = (cx, cy), (cx + d, cy)
    g = circle(O, r, INK, 5, FILL) + circle(O2, r2, BLUE, 5, '#fdf0e6') + dot(O) + dot(O2, BLUE) + lab(O, 'O', -22, 20) + lab(O2, "O'", 8, 24, BLUE, 34, 80)
    return g, O, O2


def positions_slide():
    """the five positions of two circles; the small circle moves in, one position per step"""
    r, r2 = 120, 62
    cx, cy = 210, 225
    cases = [(r + r2 + 80, 'd>r+r\'', 'រង្វង់គ្មានចំណុចរួម'), (r + r2, 'd=r+r\'', 'រង្វង់ប៉ះក្រៅ (មានចំណុចរួមមួយ)'), (r + r2 - 55, "r-r'<d<r+r'", 'រង្វង់កាត់គ្នាត្រង់ពីរចំណុច'),
             (r - r2, "d=r-r'", 'រង្វង់ប៉ះក្នុង (មានចំណុចរួមមួយ)'), (r - r2 - 38, "d<r-r'", 'រង្វង់តូចនៅក្នុងរង្វង់ធំ (គ្មានចំណុចរួម)')]
    c = Cv(780, 450)
    c.add(circle((cx, cy), r, INK, 5, FILL) + dot((cx, cy)) + lab((cx, cy), 'O', -2, 28, INK, 34, 70))
    for k, (d, cond, name) in enumerate(cases):
        O2 = (cx + d, cy)
        g = circle(O2, r2, BLUE, 5, 'rgba(255,224,204,.55)') + dot(O2, BLUE) + lab(O2, "O'", 4, 28, BLUE, 32, 70)
        g += seg((cx, cy), O2, RED, 3, '8 6') if d > 0 else ''
        if k in (1, 3):
            T_ = (cx + r, cy) if k == 1 else (cx + r, cy)
            g += dot((cx + (r if True else 0), cy), RED, 9)
        c.add(g, k + 1, k + 2 if k < 4 else None)
    return c.out(), cases


def common_tangent_lines(c1, r1, c2, r2):
    """the common tangents of two circles: 'ext' (both circles on the same side) and 'int' (opposite sides); each as (touch point 1, touch point 2)"""
    D = (c2[0] - c1[0], c2[1] - c1[1])
    d = math.hypot(*D)
    phi = math.atan2(D[1], D[0])
    out = {'ext': [], 'int': []}
    for kind, k in (('ext', r2 - r1), ('int', -(r1 + r2))):
        if abs(k) > d + 1e-9:
            continue
        al = math.acos(max(-1, min(1, k / d)))
        for s in ((1, -1) if abs(al) > 1e-9 and abs(al - math.pi) > 1e-9 else (1,)):
            n = (math.cos(phi + s * al), math.sin(phi + s * al))
            cc = n[0] * c1[0] + n[1] * c1[1] - r1
            t1 = (c1[0] - r1 * n[0], c1[1] - r1 * n[1])
            sgn = 1 if kind == 'ext' else -1
            t2 = (c2[0] - sgn * r2 * n[0], c2[1] - sgn * r2 * n[1])
            assert abs((t1[0] - c1[0]) * (t2[0] - t1[0]) + (t1[1] - c1[1]) * (t2[1] - t1[1])) < 1e-3 * d * r1
            out[kind].append((t1, t2, (-n[1], n[0])))
    return out


def common_tangents_fig(d, r=100, r2=58, cx=210, cy=215, w=700, show_int=True, show_ext=True, step_ext=0, step_int=0):
    c1, c2 = (cx, cy), (cx + d, cy)
    near_ = d < 70
    o1, o2 = ((-34, 30), (34, 30)) if near_ else ((-2, 24), (4, 24))
    ct = common_tangent_lines(c1, r, c2, r2)
    cv = Cv(w, 440)
    cv.add(circle(c1, r, INK, 5, FILL) + circle(c2, r2, INK, 5, '#fdf0e6') + dot(c1) + dot(c2) + lab(c1, 'O', o1[0], o1[1], INK, 32, 70) + lab(c2, "O'", o2[0], o2[1], INK, 30, 70))
    def tline(t1, t2, dv):
        if dist(t1, t2) > 1e-6:
            return ext(t1, t2, 0.6, 0.6)
        return (t1[0] - dv[0] * 190, t1[1] - dv[1] * 190), (t1[0] + dv[0] * 190, t1[1] + dv[1] * 190)
    if show_ext:
        g = ''
        for t1, t2, dv in ct['ext']:
            a, b = tline(t1, t2, dv)
            g += seg(a, b, BLUE, 4) + dot(t1, BLUE, 7) + dot(t2, BLUE, 7)
        cv.add(g, step_ext)
    if show_int:
        g = ''
        for t1, t2, dv in ct['int']:
            a, b = tline(t1, t2, dv)
            g += seg(a, b, RED, 4) + dot(t1, RED, 7) + dot(t2, RED, 7)
        cv.add(g, step_int)
    return cv.out(), ct


def common_tangent_ex2():
    """book example 2: XY is the internal common tangent (touching O at Y and O' at X); XS tangent to O, YT tangent to O': XS = YT"""
    R1, R2 = 120, 62
    c1, c2 = (190, 215), (190 + 330, 215)
    ct = common_tangent_lines(c1, R1, c2, R2)
    # the internal tangent that goes up to the right
    best = None
    for t1, t2, _dv in ct['int']:
        if t2[1] < t1[1]:
            best = (t1, t2)
    Y, X = best
    S = [p for p in tangent_pts(c1, R1, X) if dist(p, Y) > 1][0]
    Tt = [p for p in tangent_pts(c2, R2, Y) if dist(p, X) > 1][0]
    assert near(dist(X, S), dist(X, Y), 1e-6) and near(dist(Y, Tt), dist(Y, X), 1e-6) and near(dist(X, S), dist(Y, Tt), 1e-6)
    c = Cv(780, 450)
    a, b = ext(Y, X, 0.35, 0.35)
    sa, sb = ext(X, S, 0.25, 0.25)
    ta, tb = ext(Y, Tt, 0.2, 0.2)
    c.add(circle(c1, R1, INK, 5, FILL) + circle(c2, R2, INK, 5, '#fdf0e6') + dot(c1) + dot(c2) + lab(c1, 'O', -26, 6) + lab(c2, "O'", 24, 8, INK, 32, 70))
    c.add(seg(a, b, BLUE, 5) + dot(X, RED) + dot(Y, RED) + lab(X, 'X', 14, -26, RED) + lab(Y, 'Y', -8, 30, RED) + seg(c1, Y, GREY, 3, '8 6') + seg(c2, X, GREY, 3, '8 6') + rightmark(Y, c1, X, 16, GREY) + rightmark(X, c2, Y, 16, GREY), 1)
    c.add(seg(sa, sb, GREEN, 5) + dot(S, GREEN) + lab(S, 'S', 0, -26, GREEN) + seg(c1, S, GREY, 3, '8 6') + rightmark(S, c1, X, 16, GREY), 2)
    c.add(seg(ta, tb, ORANGE, 5) + dot(Tt, ORANGE) + lab(Tt, 'T', 0, 28, ORANGE) + seg(c2, Tt, GREY, 3, '8 6') + rightmark(Tt, c2, Y, 16, GREY), 3)
    return c.out()


def tangent_circles_prac():
    """practice: d = 4 (tangent outside: r + r' = 4) and d = 1 (tangent inside: r - r' = 1): r = 2.5, r' = 1.5"""
    u = 44
    r, r2 = 2.5 * u, 1.5 * u
    c = Cv(860, 330)
    O1 = (150, 165)
    O2 = (O1[0] + 4 * u, 165)
    assert near(dist(O1, O2), r + r2)
    c.add(circle(O1, r, INK, 5, FILL) + circle(O2, r2, BLUE, 5, '#fdf0e6') + dot(O1) + dot(O2, BLUE) + seg(O1, O2, RED, 4) + lab(O1, 'O', -6, 24) + lab(O2, "O'", 6, 24, BLUE, 30, 70) + lab(mid(O1, O2), r'4', 0, -22, RED, 34, 60))
    P1 = (600, 165)
    P2 = (P1[0] + 1 * u, 165)
    assert near(dist(P1, P2), r - r2)
    c.add(circle(P1, r, INK, 5, FILL) + circle(P2, r2, BLUE, 5, '#fdf0e6') + dot(P1) + dot(P2, BLUE) + seg(P1, P2, RED, 4) + lab(P1, 'O', -22, 24) + lab(P2, "O'", 26, 24, BLUE, 30, 70) + lab(mid(P1, P2), r'1', 0, -22, RED, 34, 60), 0)
    return c.out()


def circle_tangent_demo_wheel():
    """the opening picture: a wheel on the road (the road touches the wheel at one point)"""
    O, r = (330, 190), 130
    c = Cv(700, 400)
    road_y = O[1] + r
    c.add(poly([(20, road_y), (680, road_y), (680, 390), (20, 390)], '#e9d8b4') + seg((20, road_y), (680, road_y), RED, 6))
    c.add(circle(O, r, INK, 8, '#ffffff') + circle(O, 30, INK, 6, '#dfe9f2') + ''.join(seg(O, pol(O, r, a), INK, 4) for a in range(0, 360, 45)) + dot(O))
    M = (O[0], road_y)
    c.add(dot(M, RED, 10) + lab(M, 'M', 0, 40, RED) + rightmark(M, O, (M[0] + 40, M[1]), 22, RED) + seg(O, M, RED, 3, '8 6'), 1)
    return c.out()


# ================================================================ extra pictures
def vocab():
    """recall: centre, radius, chord, diameter, and a point on the circle"""
    O, r = (330, 215), 165
    A, Bb = pol(O, r, 35), pol(O, r, 215)
    C, D = pol(O, r, 160), pol(O, r, 85)       # a chord well away from the centre: not a diameter
    c = Cv(720, 450)
    c.add(circle(O, r, fill=FILL) + dot(O) + lab(O, 'O', -22, 22))
    R_ = pol(O, r, 0)
    c.add(seg(O, R_, RED, 5) + dot(R_, RED) + T(O[0] + 90, O[1] - 16, 'កាំ', 30, RED), 1)
    c.add(seg(Bb, A, BLUE, 5) + dot(A, BLUE) + dot(Bb, BLUE) + lab(A, 'A', 22, -22, BLUE) + lab(Bb, 'B', -24, 22, BLUE), 2)
    c.add(seg(C, D, GREEN, 5) + dot(C, GREEN) + dot(D, GREEN) + lab(C, 'C', -26, -8, GREEN) + lab(D, 'D', 10, -28, GREEN), 3)
    return c.out()


def tangent_rule():
    """the tangent at M is perpendicular to the radius OM"""
    O, r = (330, 190), 140
    M = (O[0], O[1] + r)
    c = Cv(700, 420)
    c.add(circle(O, r, fill=FILL) + dot(O) + lab(O, 'O', -2, -26) + seg((M[0] - 250, M[1]), (M[0] + 250, M[1]), BLUE, 5) + lab((M[0] + 250, M[1]), 'l', 4, -22, BLUE, 38, 60))
    c.add(seg(O, M, RED, 4, '10 7') + dot(M, RED, 9) + lab(M, 'M', 0, 38, RED) + rightmark(M, O, (M[0] + 40, M[1]), 22, RED), 1)
    return c.out()


def tangent_prac():
    """practice: radius 2, AB tangent at B, AB = OB, the line AO meets the circle at C: AC = AO - 2 = 2 sqrt 2 - 2"""
    u = 70
    O, r = (420, 190), 2 * u
    A = (O[0] - 2 * math.sqrt(2) * u * math.cos(math.radians(45)) * 1, O[1] + 2 * math.sqrt(2) * u * math.sin(math.radians(45)))
    B = (O[0], O[1] + r)
    C = pol(O, r, 225)
    assert near(dist(A, B), r) and near(dist(O, A), 2 * math.sqrt(2) * u) and abs((A[0] - B[0]) * (B[0] - O[0]) + (A[1] - B[1]) * (B[1] - O[1])) < 1e-6
    assert near(dist(A, O) - dist(O, C), dist(A, C)) and dist(A, C) < dist(A, O)
    c = Cv(700, 420)
    L0, L1 = ext(A, B, 0.15, 0.5)
    c.add(circle(O, r, fill=FILL) + seg(L0, L1, BLUE, 5) + seg(A, O, INK, 5) + dot(O) + dot(A) + dot(B, RED) + dot(C, RED) + lab(O, 'O', 24, -14) + lab(A, 'A', -26, 6) + lab(B, 'B', 4, 34, RED) + lab(C, 'C', -4, -28, RED) + lab(mid(O, B), r'2', 24, 0, GREEN, 34, 60))
    c.add(seg(O, B, INK, 4) + rightmark(B, O, A, 20, RED) + tick(A, B, 1, GREEN) + tick(O, B, 1, GREEN), 1)
    return c.out()


# ================================================================ the book's exercises (p.156-158)
def _tang_line(T, O, k0=.5, k1=.9):
    """the tangent at T (perpendicular to OT), as two end points"""
    r = dist(O, T)
    tx, ty = -(T[1] - O[1]) / r, (T[0] - O[0]) / r
    return (T[0] - tx * r * k0, T[1] - ty * r * k0), (T[0] + tx * r * k1, T[1] + ty * r * k1), (tx, ty)


def _ang_lab(v, p1, p2, rad, tex, col, lr=None, size=26):
    return angarc(v, p1, p2, rad, col, 4) + lab(bis(v, p1, p2, lr or rad + 30), tex, 0, 0, col, size, 130, maxr=60, anchor=bis(v, p1, p2, rad))


def ex1(k):
    """exercise 1 (k = 'a'..'f'): PT is tangent at T; find the angles marked a, b, c"""
    O, r = (180, 150), 100
    if k == 'b':
        O = (190, 190)
    c = Cv(380, 340, '40vh')
    base = lambda: circle(O, r, fill=FILL) + dot(O) + lab(O, 'O', 4, -22, INK, 30, 60)
    if k == 'a':
        T = pol(O, r, 235)
        P = pol(O, r / math.cos(math.radians(50)), 285)
        a, b, ux = _tang_line(T, O, .55, .0)
        assert near(angle_at(O, T, P), 50, 1e-6) and near(angle_at(P, T, O), 40, 1e-6)
        L0, L1 = ext(T, P, .5, .0)
        c.add(base() + seg(L0, P, INK, 5) + seg(O, T, INK, 5) + seg(O, P, INK, 5) + dot(T, RED) + lab(T, 'T', -22, 8, RED, 30, 60) + lab(P, 'P', 22, 8, INK, 30, 60)
              + rightmark(T, O, P, 16, RED) + _ang_lab(O, T, P, 34, r'50^\circ', ORANGE, 62, 24) + _ang_lab(P, T, O, 40, r'a^\circ', RED, 66, 28))
    elif k == 'b':
        T = pol(O, r, 128)
        a_, b_, (tx, ty) = _tang_line(T, O)
        P = (T[0] + tx * r, T[1] + ty * r)
        if P[0] < T[0]:
            P = (T[0] - tx * r, T[1] - ty * r)
        assert near(dist(O, T), dist(T, P)) and near(angle_at(T, O, P), 90) and near(angle_at(O, T, P), 45) and near(angle_at(P, O, T), 45)
        L0, L1 = ext(T, P, 1.0, .0)
        c.add(base() + seg(L0, P, INK, 5) + seg(O, T, INK, 5) + seg(O, P, INK, 5) + dot(T, RED) + lab(T, 'T', -20, -18, RED, 30, 60) + lab(P, 'P', 20, -6, INK, 30, 60)
              + tick(O, T, 1, GREEN) + tick(T, P, 1, GREEN) + rightmark(T, O, P, 16, RED) + _ang_lab(T, O, P, 26, r'a^\circ', RED, 52, 26) + _ang_lab(O, T, P, 36, r'b^\circ', RED, 66, 26))
    elif k == 'c':
        T = pol(O, r, 300)
        a_, b_, (tx, ty) = _tang_line(T, O)
        w = unit(T, O)
        u = (tx, ty) if (tx * 1 + ty * -1) > 0 else (-tx, -ty)          # towards the up-right side
        P = (T[0] + u[0] * r * 1.0, T[1] + u[1] * r * 1.0)
        ch = (math.cos(math.radians(40)) * w[0] + math.sin(math.radians(40)) * u[0], math.cos(math.radians(40)) * w[1] + math.sin(math.radians(40)) * u[1])
        Q = (T[0] + ch[0] * 2 * r * math.cos(math.radians(40)), T[1] + ch[1] * 2 * r * math.cos(math.radians(40)))
        assert near(dist(O, Q), r, 1e-6) and near(angle_at(T, O, Q), 40, 1e-6) and near(angle_at(T, Q, P), 50, 1e-6)
        L0 = (T[0] - u[0] * r * .8, T[1] - u[1] * r * .8)
        c.add(base() + seg(L0, P, INK, 5) + seg(O, T, INK, 5) + seg(T, Q, INK, 5) + dot(T, RED) + lab(T, 'T', 18, 24, RED, 30, 60) + lab(P, 'P', 22, 0, INK, 30, 60)
              + rightmark(T, O, P, 16, RED) + _ang_lab(T, O, Q, 36, r'40^\circ', ORANGE, 64, 22) + _ang_lab(T, Q, P, 44, r'b^\circ', RED, 74, 26))
    elif k == 'd':
        T = pol(O, r, 235)
        S = pol(O, r, 305)
        a_, b_, (tx, ty) = _tang_line(T, O)
        u = (tx, ty) if (tx * 1 + ty * 1) > 0 else (-tx, -ty)           # down-right
        P = (T[0] + u[0] * r * .8, T[1] + u[1] * r * .8)
        assert near(angle_at(T, S, P), 35, 1e-6) and near(angle_at(T, O, S), 55, 1e-6) and near(angle_at(O, T, S), 70, 1e-6)
        L0 = (T[0] - u[0] * r * .6, T[1] - u[1] * r * .6)
        c.add(base() + seg(L0, P, INK, 5) + seg(O, T, INK, 5) + seg(O, S, INK, 5) + seg(T, S, INK, 5) + dot(T, RED) + dot(S) + lab(T, 'T', -22, 4, RED, 30, 60) + lab(S, 'S', 22, 14, INK, 30, 60) + lab(P, 'P', 18, 12, INK, 30, 60)
              + _ang_lab(T, S, P, 34, r'35^\circ', ORANGE, 64, 22) + _ang_lab(T, O, S, 36, r'a^\circ', RED, 60, 26) + _ang_lab(O, T, S, 34, r'b^\circ', RED, 58, 26))
    elif k == 'e':
        O2 = (250, 120)
        ang_op = 194
        T = pol(O2, r, ang_op + 65)
        P = pol(O2, r / math.cos(math.radians(65)), ang_op)
        E = pol(O2, r, ang_op)
        assert near(angle_at(O2, T, P), 65, 1e-6) and near(angle_at(P, O2, T), 25, 1e-6) and near(angle_at(T, O2, E), 57.5, 1e-6) and near(angle_at(T, E, P), 32.5, 1e-6)
        c = Cv(420, 340, '34vh')
        c.add(circle(O2, r, fill=FILL) + dot(O2) + lab(O2, 'O', 24, -20, INK, 30, 60) + seg(P, O2, INK, 5) + seg(P, T, INK, 5) + seg(O2, T, INK, 5) + seg(E, T, INK, 5) + dot(T, RED) + dot(E)
              + lab(T, 'T', 10, 26, RED, 30, 60) + lab(P, 'P', -22, 0, INK, 30, 60) + _ang_lab(O2, T, P, 30, r'65^\circ', ORANGE, 58, 22) + _ang_lab(P, O2, T, 60, r'a^\circ', RED, 96, 26)
              + _ang_lab(T, O2, E, 32, r'b^\circ', RED, 54, 24) + _ang_lab(T, E, P, 46, r'c^\circ', RED, 74, 24))
    else:
        Oc = (180, 150)
        Tt, Aa = pol(Oc, r, 315), pol(Oc, r, 135)
        P = pol(Oc, r / math.cos(math.radians(50)), 5)
        Bb = pol(Oc, r, 185)
        assert near(angle_at(Oc, Tt, P), 50, 1e-6) and near(angle_at(P, Tt, Oc), 40, 1e-6) and near(angle_at(Aa, Oc, Bb), 65, 1e-6) and near(angle_at(Oc, Aa, P), 130, 1e-6)
        a_, b_, (tx, ty) = _tang_line(Tt, Oc, .7, .0)
        c.add(circle(Oc, r, fill=FILL) + dot(Oc) + lab(Oc, 'O', 18, 22, INK, 28, 60) + seg(Aa, Tt, INK, 5) + seg(Bb, P, INK, 5) + seg(Aa, Bb, INK, 5) + seg(a_, P, INK, 4) if False else
              circle(Oc, r, fill=FILL) + dot(Oc) + lab(Oc, 'O', 18, 22, INK, 28, 60) + seg(Aa, Tt, INK, 5) + seg(Bb, P, INK, 5) + seg(Aa, Bb, INK, 5) + seg((Tt[0] - (P[0] - Tt[0]) * .5, Tt[1] - (P[1] - Tt[1]) * .5), P, INK, 4)
              + dot(Tt, RED) + lab(Tt, 'T', 16, 20, RED, 30, 60) + lab(Aa, 'A', -14, -24, INK, 30, 60) + lab(Bb, 'B', -24, 8, INK, 30, 60) + lab(P, 'P', 22, -8, INK, 30, 60)
              + _ang_lab(Oc, Aa, P, 26, r'130^\circ', ORANGE, 70, 20) + _ang_lab(Bb, Aa, Oc, 34, r'a^\circ', RED, 52, 26) + _ang_lab(P, Tt, Oc, 40, r'b^\circ', RED, 62, 26))
    return c.out()


EX1_ANS = {'a': r'a=90^\circ-50^\circ=40^\circ', 'b': r'a=90^\circ\ ,\ b=45^\circ', 'c': r'b=90^\circ-40^\circ=50^\circ', 'd': r'a=90^\circ-35^\circ=55^\circ\ ,\ b=180^\circ-2\times 55^\circ=70^\circ',
           'e': r'a=25^\circ\ ,\ b=57.5^\circ\ ,\ c=32.5^\circ', 'f': r'b=40^\circ\ ,\ a=65^\circ'}


def ex2(k):
    """exercise 2: tangents PT and PV from P; find the unknown angles"""
    r = {'a': 54, 'b': 88, 'c': 66, 'd': 100}[k]
    O = (90, 150)
    c = Cv(480, 300, '40vh')
    half = {'a': 11, 'b': 21, 'c': 12.5, 'd': 21}[k]
    if k in 'abc':
        half_p = {'a': 11, 'b': 21, 'c': 12.5}[k]
        d = r / math.sin(math.radians(half_p))
        P = (O[0] + d, O[1])
        T, V = tangent_pts(O, r, P)
        if T[1] > V[1]:
            T, V = V, T
        g = circle(O, r, fill=FILL) + dot(O) + lab(O, 'O', -22, 2, INK, 28, 60) + seg(P, ext(P, T, 0, .02)[1], INK, 5) + seg(P, ext(P, V, 0, .02)[1], INK, 5) + dot(T) + dot(V) + dot(P) \
            + lab(T, 'T', 4, -24, INK, 28, 60) + lab(V, 'V', 4, 26, INK, 28, 60) + lab(P, 'P', 22, 0, INK, 28, 60)
        if k == 'a':
            assert near(angle_at(P, T, V), 22) and near(angle_at(O, T, P), 79, 1e-6)
            g += seg(O, T, INK, 4) + seg(O, V, INK, 4) + seg(O, P, INK, 4) + _ang_lab(P, T, V, 44, r'22^\circ', ORANGE, 76, 22) + _ang_lab(O, T, P, 30, r'a^\circ', RED, 50, 24) + _ang_lab(O, P, V, 36, r'b^\circ', RED, 58, 24) + _ang_lab(P, O, V, 70, r'c^\circ', RED, 100, 24)
        elif k == 'b':
            assert near(angle_at(P, T, V), 42) and near(angle_at(O, T, V), 138, 1e-6)
            g += seg(O, T, INK, 4) + seg(O, V, INK, 4) + _ang_lab(P, T, V, 44, r'42^\circ', ORANGE, 76, 22) + _ang_lab(T, O, P, 24, r'c^\circ', RED, 46, 24) + _ang_lab(V, O, P, 24, r'a^\circ', RED, 46, 24) + _ang_lab(O, T, V, 24, r'b^\circ', RED, 48, 24)
        else:
            assert near(angle_at(P, T, V), 25) and near(angle_at(O, T, V), 155, 1e-6)
            g += seg(O, T, INK, 4) + seg(O, V, INK, 4) + seg(T, V, INK, 4) + _ang_lab(P, T, V, 44, r'25^\circ', ORANGE, 76, 22) + _ang_lab(T, O, V, 24, r'a^\circ', RED, 48, 22) + _ang_lab(O, T, V, 24, r'b^\circ', RED, 56, 24) + _ang_lab(V, O, T, 24, r'c^\circ', RED, 48, 22)
        c.add(g)
    else:
        O = (130, 150)
        d = r / math.sin(math.radians(21))
        P = (O[0] + d, O[1])
        T = tangent_pts(O, r, P)[0]
        if T[1] > O[1]:
            T = tangent_pts(O, r, P)[1]
        X = (O[0] - r, O[1])
        assert near(angle_at(P, T, O), 21, 1e-6) and near(angle_at(O, T, P), 69, 1e-6) and near(angle_at(X, O, T), 34.5, 1e-6) and near(angle_at(T, X, O), 34.5, 1e-6)
        c = Cv(580, 300, '40vh')
        c.add(circle(O, r, fill=FILL) + dot(O) + lab(O, 'O', 6, 24, INK, 28, 60) + seg(X, P, INK, 5) + seg(P, ext(P, T, 0, .02)[1], INK, 5) + seg(O, T, INK, 4) + seg(X, T, INK, 4) + dot(T) + dot(X) + dot(P)
              + lab(T, 'T', 8, -24, INK, 28, 60) + lab(X, 'X', -24, 4, INK, 28, 60) + lab(P, 'P', 22, 0, INK, 28, 60)
              + _ang_lab(P, T, O, 56, r'21^\circ', ORANGE, 90, 22) + _ang_lab(O, T, P, 30, r'a^\circ', RED, 52, 24) + _ang_lab(T, X, O, 36, r'b^\circ', RED, 60, 24) + _ang_lab(X, T, O, 36, r'c^\circ', RED, 62, 24))
    return c.out()


EX2_ANS = {'a': r'a=b=79^\circ\ ,\ c=11^\circ', 'b': r'a=c=90^\circ\ ,\ b=138^\circ', 'c': r'a=c=12.5^\circ\ ,\ b=155^\circ', 'd': r'a=69^\circ\ ,\ b=c=34.5^\circ'}


def ex3(k):
    """exercise 3: tangents PA, PB; find r (k = 'a') or d (k = 'b')"""
    if k == 'a':
        u = 8
        O, r = (150, 150), 8 * u
        P = (O[0] + 17 * u, O[1])
        A, B = tangent_pts(O, r, P)
        if A[1] > B[1]:
            A, B = B, A
        assert near(dist(P, A) / u, 15, 1e-6)
        c = Cv(520, 300, '42vh')
        c.add(circle(O, r, fill=FILL) + dot(O) + lab(O, 'O', -22, 6, INK, 28, 60) + seg(P, A, INK, 5) + seg(P, B, INK, 5) + seg(O, P, INK, 5) + seg(O, A, INK, 4) + seg(O, B, INK, 4) + dot(A) + dot(B) + dot(P)
              + lab(A, 'A', 6, -24, INK, 28, 60) + lab(B, 'B', 6, 26, INK, 28, 60) + lab(P, 'P', 22, 0, INK, 28, 60) + lab(mid(O, P), r'17', 0, -20, GREEN, 30, 60) + lab(mid(P, B), r'15', 8, 26, GREEN, 30, 60) + lab(mid(O, B), r'r', -20, 4, RED, 30, 60)
              + rightmark(A, O, P, 14, RED) + rightmark(B, O, P, 14, RED))
    else:
        u = 12
        O, r = (400, 150), 5 * u
        P = (O[0] - 13 * u, O[1])
        A, B = tangent_pts(O, r, P)
        if A[1] > B[1]:
            A, B = B, A
        assert near(dist(P, A) / u, 12, 1e-6)
        N = (O[0] - r, O[1])
        c = Cv(520, 300, '42vh')
        c.add(circle(O, r, fill=FILL) + dot(O) + lab(O, 'O', 24, 4, INK, 28, 60) + seg(P, A, INK, 5) + seg(P, B, INK, 5) + seg(O, A, INK, 4) + seg(O, B, INK, 4) + dot(A) + dot(B) + dot(P)
              + lab(A, 'A', 4, -24, INK, 28, 60) + lab(B, 'B', 4, 26, INK, 28, 60) + lab(P, 'P', -22, 0, INK, 28, 60) + lab(mid(P, A), r'12', -8, -24, GREEN, 30, 60) + lab(mid(O, A), r'5', 18, -14, GREEN, 30, 60)
              + rightmark(A, O, P, 14, RED) + seg(P, N, RED, 4, '8 6') + lab(mid(P, N), r'd', 0, 24, RED, 30, 60) + dot(N, RED))
    return c.out()


def kite_fig(r_, tl, P_dir=0, labels=('P', 'A', 'B'), lens=None, extra='', maxh='42vh'):
    """tangents PA, PB (P on the right, or the left when P_dir = 180) and the radii OA, OB; tl = tangent length (units), r_ = radius (units); u = pixels per unit"""
    u = lens
    O = (260 if P_dir == 0 else 380, 170)
    r = r_ * u
    d = math.hypot(r_, tl) * u
    P = (O[0] + d, O[1]) if P_dir == 0 else (O[0] - d, O[1])
    A, B = tangent_pts(O, r, P)
    if A[1] > B[1]:
        A, B = B, A
    return O, r, P, A, B


def ex4():
    """OA = 2, PB = 9: b = 9, c = 2, perimeter 22, area 18"""
    u = 24
    O, r, P, A, B = kite_fig(2, 9, 180, lens=u)
    assert near(dist(P, A) / u, 9, 1e-6) and near(dist(O, B) / u, 2, 1e-6)
    c = Cv(640, 340, '36vh')
    c.add(circle(O, r, fill=FILL) + dot(O) + lab(O, 'O', 20, 4, INK, 28, 60) + seg(P, ext(P, A, 0, .12)[1], INK, 5) + seg(P, ext(P, B, 0, .12)[1], INK, 5) + seg(O, A, INK, 4) + seg(O, B, INK, 4) + dot(A) + dot(B) + dot(P)
          + lab(A, 'A', 8, -24, INK, 28, 60) + lab(B, 'B', 8, 26, INK, 28, 60) + lab(P, 'P', -22, 0, INK, 28, 60) + lab(mid(P, A), r'b', -4, -24, RED, 30, 60) + lab(mid(P, B), r'9', -4, 26, GREEN, 30, 60)
          + lab(mid(O, A), r'2', 22, -4, GREEN, 30, 60) + lab(mid(O, B), r'c', 22, 4, RED, 30, 60) + rightmark(A, O, P, 12, RED) + rightmark(B, O, P, 12, RED))
    return c.out()


def ex5():
    """right triangle ABC (right angle at B), incircle; AF = 10, DB = 5, EC = 15: AB = 15, BC = 20, AC = 25, area 150"""
    u = 15
    B = (60, 280)
    A = (60, 280 - 15 * u)
    C = (60 + 20 * u, 280)
    I = (B[0] + 5 * u, B[1] - 5 * u)
    D, E = (B[0], I[1]), (I[0], B[1])
    F = foot(I, A, C)
    assert near(dist(I, F), 5 * u, 1e-6) and near(dist(A, F) / u, 10, 1e-6) and near(dist(C, F) / u, 15, 1e-6)
    c = Cv(420, 330, '40vh')
    c.add(poly([A, B, C], 'none', INK, 5) + circle(I, 5 * u, fill=FILL) + dot(I) + dot(D, RED) + dot(E, RED) + dot(F, RED) + lab(A, 'A', 0, -26) + lab(B, 'B', -24, 20) + lab(C, 'C', 24, 8)
          + lab(D, 'D', -24, 0, RED, 28, 60) + lab(E, 'E', 0, 24, RED, 28, 60) + lab(F, 'F', 22, -10, RED, 28, 60) + rightmark(B, A, C, 16, INK)
          + lab(mid(A, F), r'10', 28, 10, GREEN, 28, 60) + lab(mid(D, B), r'5', -22, 0, GREEN, 28, 60) + lab(mid(E, C), r'15', 0, 24, GREEN, 28, 60))
    return c.out()


def ex6():
    """r = 3, angle AOB = 140: the tangents meet at P (AP = r / tan 70 = 8.24 cm; the book prints 82.4)"""
    u = 40
    O, r = (150, 150), 3 * u
    half = 70.0
    d = r / math.cos(math.radians(half))
    P = (O[0] + d, O[1])
    A, B = tangent_pts(O, r, P)
    if A[1] > B[1]:
        A, B = B, A
    assert near(angle_at(O, A, B), 140, 1e-6)
    c = Cv(560, 300, '34vh')
    c.add(circle(O, r, fill=FILL) + dot(O) + lab(O, 'O', -22, 4, INK, 28, 60) + seg(P, ext(P, A, 0, .15)[1], INK, 5) + seg(P, ext(P, B, 0, .15)[1], INK, 5) + seg(O, A, INK, 4) + seg(O, B, INK, 4) + dot(A) + dot(B) + dot(P)
          + lab(A, 'A', 4, -24, INK, 28, 60) + lab(B, 'B', 4, 26, INK, 28, 60) + lab(P, 'P', 22, 0, INK, 28, 60) + lab(mid(O, A), r'3', -18, -6, GREEN, 28, 60) + lab(mid(P, A), r'82.4', 8, -26, GREEN, 28, 100)
          + _ang_lab(O, A, B, 26, r'140^\circ', ORANGE, 60, 22))
    return c.out()


def ex7(la='A', lb='B', tangent_len=20, tq=10, r_=15):
    u = 8
    r = r_ * u
    O = (330, 190)
    Tp = (O[0] - (r + tq * u), O[1])
    A, B = tangent_pts(O, r, Tp)
    if A[1] > B[1]:
        A, B = B, A
    Q = (O[0] - r, O[1])
    assert near(dist(Tp, A) / u, tangent_len, 1e-6)
    c = Cv(560, 340, '34vh')
    e1 = ext(Tp, A, 0, .2)[1]
    c.add(circle(O, r, fill=FILL) + dot(O) + lab(O, 'O', 22, 4, INK, 28, 60) + seg(Tp, e1, INK, 5) + seg(Tp, ext(Tp, B, 0, .2)[1], INK, 5) + seg(Tp, O, INK, 5) + seg(O, A, INK, 4) + seg(O, B, INK, 4) + dot(A) + dot(B) + dot(Q, RED) + dot(Tp)
          + lab(A, la, 4, -24, INK, 28, 60) + lab(B, lb, 4, 26, INK, 28, 60) + lab(Tp, 'T', -22, 4, INK, 28, 60) + lab(Q, 'Q', 22, -20, RED, 28, 60)
          + lab(mid(Tp, Q), r'10', 0, 26, GREEN, 28, 60) + lab(mid(Tp, A), r'20', -10, -26, GREEN, 28, 60) + rightmark(A, O, Tp, 14, RED) + rightmark(B, O, Tp, 14, RED))
    return c.out()


def ex8():
    """r = 4.5, TA = 9: perimeter 27, area 40.5"""
    u = 24
    O, r, P, A, B = kite_fig(4.5, 9, 0, lens=u)
    assert near(dist(P, A) / u, 9, 1e-6)
    c = Cv(620, 340, '36vh')
    c.add(circle(O, r, fill=FILL) + dot(O) + lab(O, 'O', -22, 4, INK, 28, 60) + seg(P, ext(P, A, 0, .15)[1], INK, 5) + seg(P, ext(P, B, 0, .15)[1], INK, 5) + seg(O, A, INK, 4) + seg(O, B, INK, 4) + seg(O, P, INK, 3, '8 6') + dot(A) + dot(B) + dot(P)
          + lab(A, 'A', 4, -24, INK, 28, 60) + lab(B, 'B', 4, 26, INK, 28, 60) + lab(P, 'T', 22, 0, INK, 28, 60) + lab(mid(O, A), r'4.5', -30, -6, GREEN, 28, 80) + lab(mid(P, A), r'9', 6, -24, GREEN, 28, 60))
    return c.out()


def ex9():
    """two circles of radius 4 with centres A and B, AB = 4: ABCD is a square of side 4 (area 16)"""
    u = 44
    A, B = (200, 260), (200 + 4 * u, 260)
    D, C = (A[0], A[1] - 4 * u), (B[0], B[1] - 4 * u)
    assert near(dist(A, B), 4 * u) and near(dist(A, D), 4 * u)
    c = Cv(680, 440, '42vh')
    c.add(circle(A, 4 * u, fill='#eef5fb') + circle(B, 4 * u, INK, 5, 'rgba(255,224,204,.35)') + poly([A, B, C, D], 'rgba(47,158,68,.18)', GREEN, 5) + dot(A) + dot(B) + dot(C) + dot(D)
          + lab(A, 'A', -22, 20, INK, 30, 60) + lab(B, 'B', 22, 20, INK, 30, 60) + lab(C, 'C', 4, -26, INK, 30, 60) + lab(D, 'D', -4, -26, INK, 30, 60)
          + rightmark(A, B, D, 18, INK) + rightmark(B, A, C, 18, INK) + rightmark(D, A, C, 18, INK) + rightmark(C, B, D, 18, INK) + lab(mid(A, B), r'4', 0, 24, GREEN, 30, 60))
    return c.out()


def ex10():
    """r = 5, angle ATB = 60: angle AOB = 120, sector area 26.2"""
    u = 24
    O, r = (330, 170), 5 * u
    d = r / math.sin(math.radians(30))
    Tp = (O[0] - d, O[1])
    A, B = tangent_pts(O, r, Tp)
    if A[1] > B[1]:
        A, B = B, A
    assert near(angle_at(O, A, B), 120, 1e-6) and near(angle_at(Tp, A, B), 60, 1e-6)
    c = Cv(640, 360, '36vh')
    c.add(circle(O, r, fill=FILL) + dot(O) + lab(O, 'O', 24, 4, INK, 28, 60) + seg(Tp, ext(Tp, A, 0, .15)[1], INK, 5) + seg(Tp, ext(Tp, B, 0, .15)[1], INK, 5) + seg(O, A, INK, 4) + seg(O, B, INK, 4) + dot(A) + dot(B) + dot(Tp)
          + lab(A, 'A', 4, -24, INK, 28, 60) + lab(B, 'B', 4, 26, INK, 28, 60) + lab(Tp, 'T', -22, 0, INK, 28, 60) + lab(mid(O, B), r'5', 22, 12, GREEN, 28, 60) + _ang_lab(Tp, A, B, 40, r'60^\circ', ORANGE, 72, 22)
          + angarc(O, A, B, 40, PURPLE, 4, fill=PURPLE))
    return c.out()


def ex11():
    """concentric circles 8 and 10, chord AB of the big one touches the small one at T: AB = 12"""
    u = 17
    O = (300, 190)
    T = (O[0] - 8 * u, O[1])
    half = math.sqrt(100 - 64) * u
    A, B = (T[0], T[1] - half), (T[0], T[1] + half)
    assert near(dist(O, A), 10 * u) and near(half / u, 6, 1e-6)
    c = Cv(620, 380, '38vh')
    c.add(circle(O, 10 * u, fill='#fdf0e6') + circle(O, 8 * u, INK, 5, FILL) + dot(O) + lab(O, 'O', 22, 4, INK, 28, 60) + seg(A, B, INK, 5) + seg(O, T, BLUE, 4, '8 6') + dot(T, RED) + dot(A) + dot(B)
          + lab(A, 'A', -4, -26, INK, 28, 60) + lab(B, 'B', -4, 28, INK, 28, 60) + lab(T, 'T', -24, 0, RED, 28, 60) + rightmark(T, O, A, 14, RED) + lab(mid(O, T), r'8', 0, -20, GREEN, 28, 60))
    return c.out()


def ex12():
    """circles O and O' touch at B; MA, MB, MC tangents: MA = MB = MC"""
    r1, r2 = 70, 100
    O = (180, 300)
    O2 = (O[0] + r1 + r2, 300 - (r2 - r1) * 0)
    B = (O[0] + r1, 300)
    M = (B[0], 60)
    A = [p for p in tangent_pts(O, r1, M)][0]
    A = min(tangent_pts(O, r1, M), key=lambda p: p[0])
    C = max(tangent_pts(O2, r2, M), key=lambda p: p[0])
    assert near(dist(M, A), dist(M, B), 1e-6) and near(dist(M, B), dist(M, C), 1e-6)
    c = Cv(640, 420, '40vh')
    c.add(circle(O, r1, fill=FILL) + circle(O2, r2, INK, 5, '#fdf0e6') + dot(O) + dot(O2) + lab(O, 'O', -2, 24, INK, 26, 60) + lab(O2, "O'", 2, 24, INK, 26, 60)
          + seg(ext(M, A, 0, .35)[0], ext(M, A, 0, .35)[1], INK, 5) + seg(M, ext(M, C, 0, .35)[1], INK, 5) + seg(M, (B[0], B[1] + 70), INK, 5) + dot(A, RED) + dot(B, RED) + dot(C, RED) + dot(M)
          + lab(M, 'M', 0, -22, INK, 30, 60) + lab(A, 'A', -22, -8, RED, 28, 60) + lab(B, 'B', 20, 10, RED, 28, 60) + lab(C, 'C', 22, -8, RED, 28, 60))
    c.add(tick(M, A, 1, GREEN) + tick(M, B, 1, GREEN) + tick(M, C, 1, GREEN), 1)
    return c.out()


def ex13():
    """EF, EG tangents to the circle H; J on EH; angle JEG = 22: EGH = 90, HGF = 22, FGE = 68"""
    u = 20
    H, r = (460, 170), 5 * u
    d = r / math.sin(math.radians(22))
    E = (H[0] - d, H[1])
    F, G = tangent_pts(H, r, E)
    if F[1] > G[1]:
        F, G = G, F
    J = foot(F, E, H)
    assert near(angle_at(G, E, H), 90, 1e-6) and near(angle_at(G, H, F), 22, 1e-6) and near(angle_at(G, F, E), 68, 1e-6) and near(dist(F, J), dist(J, G), 1e-6)
    c = Cv(680, 340, '34vh')
    c.add(circle(H, r, fill=FILL) + dot(H) + lab(H, 'H', 24, 4, INK, 28, 60) + seg(E, ext(E, F, 0, .12)[1], INK, 5) + seg(E, ext(E, G, 0, .12)[1], INK, 5) + seg(E, H, INK, 4) + seg(H, F, INK, 4) + seg(H, G, INK, 4) + seg(F, G, INK, 3, '8 6') + dot(E) + dot(F) + dot(G) + dot(J)
          + lab(E, 'E', -22, 0, INK, 28, 60) + lab(F, 'F', 4, -24, INK, 28, 60) + lab(G, 'G', 4, 26, INK, 28, 60) + lab(J, 'J', -14, -20, INK, 26, 60) + _ang_lab(E, G, H, 70, r'22^\circ', ORANGE, 104, 22))
    return c.out()
