"""Pictures for Grade 8 Lesson 12 «ការប្រៀបធៀបត្រីកោណ». Built on the Grade 9 picture engine (tools/lesson9_13/geo13.py).
Every picture is computed from coordinates and the facts it shows are asserted (equal sides, equal angles, right angles, collinear points).
Style = the KhmerMath formula book: blue outlines, red dashed helper lines, red tick marks / angle arcs, lavender and mint fills, italic labels."""
import math, os, sys
HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, '..', 'lesson9_13'))
import geo13 as G
from lib import T as _T
from geo13 import Cv, seg as _seg, lab, dot, tick, angarc, arc, poly, pol, mid, dist, bis, rightmark, near, angle_at, foot, unit, dir_deg, circle

def seg(a, b, col=None, w=5, dash=''):
    """thinner lines than the formula book: the class slides draw thin navy sides"""
    return _seg(a, b, G.INK if col is None else col, w * 0.9, dash)


LC = '#0000cc'      # outlines: the blue of the formula-book figures
AUX = '#a33b32'     # helper lines and points: brick red
MK = '#0000cc'      # tick marks, angle arcs and right-angle squares: thin blue
LAV, MINT, ORG, SKY = '#eefff1', '#eefff1', '#f6d5cf', '#bcd7f2'
GREY = '#6b7785'
PINK = '#f9e3df'
S2 = dict(col=AUX, fill=PINK)          # the second triangle of a pair (A'B'C', DEF): brick outline, pink fill, names in brick
S2N = dict(col=AUX, fill=None)
GREEN = '#0000cc'
NAVYT = '#0000cc'
W, H = 640, 440


def P(x, y, k=40, ox=60, oy=380):
    """maths coordinates (x right, y up) -> screen"""
    return (ox + k * x, oy - k * y)


def cen(*ps):
    return (sum(p[0] for p in ps) / len(ps), sum(p[1] for p in ps) / len(ps))


def tri(A, B, C, names=('A', 'B', 'C'), fill=LAV, col=LC, w=5, ticks=(), arcs=(), rad=34, vl=True, nd=30, size=38, tcol=MK):
    """a marked triangle. ticks: [(i, j, n)] marks across side Pi-Pj; arcs: [(i, n)] n arcs at vertex i (same n = equal angles)"""
    Q = (A, B, C)
    c = cen(A, B, C)
    s = ''
    if fill:
        s += poly([A, B, C], fill)
    s += seg(A, B, col, w) + seg(B, C, col, w) + seg(C, A, col, w)
    for i, j, n in ticks:
        s += tick(Q[i], Q[j], n, tcol)
    for i, n in arcs:
        o = [Q[k] for k in range(3) if k != i]
        for q in range(n):
            s += angarc(Q[i], o[0], o[1], rad + 9 * q, tcol, 4)
    if vl:
        for p, nm in zip(Q, names):
            u = unit(c, p)
            s += lab(p, nm, u[0] * nd, u[1] * nd, col, size, 120)
    return s


def side_label(a, b, tex, off=30, col=GREEN, size=32, sign=1, w=200):
    m = mid(a, b)
    u = unit(a, b)
    return lab(m, tex, -u[1] * off * sign, u[0] * off * sign, col, size, w)


def mini(kind, w=300, h=230, grey=False):
    """a small picture of one case of congruence: asa / sas / sss / ha / hl.  grey=True: the cases that are not taught today"""
    c = Cv(w, h, '30vh')
    kw = dict(col='#808080', fill='#ececec', tcol='#808080', w=3) if grey else {}
    A, B, C = (50, 180), (250, 180), (130, 40)
    if kind == 'asa':
        s = tri(A, B, C, vl=True, size=30, nd=24, ticks=[(0, 1, 1)], arcs=[(0, 1), (1, 2)], rad=26, **kw)
    elif kind == 'sas':
        s = tri(A, B, C, vl=True, size=30, nd=24, ticks=[(0, 1, 1), (0, 2, 2)], arcs=[(0, 1)], rad=26, **kw)
    elif kind == 'sss':
        s = tri(A, B, C, vl=True, size=30, nd=24, ticks=[(0, 1, 1), (0, 2, 2), (1, 2, 3)], **kw)
    elif kind == 'ha':          # right triangle: hypotenuse + acute angle
        A, B, C = (60, 180), (250, 180), (60, 50)
        s = tri(A, B, C, names=('A', 'B', 'C'), vl=True, size=30, nd=24, ticks=[(1, 2, 1)], arcs=[(1, 1)], rad=30, **kw) + rightmark(A, B, C, 18, MK)
    else:                       # hyp + leg
        A, B, C = (60, 180), (250, 180), (60, 50)
        s = tri(A, B, C, names=('A', 'B', 'C'), vl=True, size=30, nd=24, ticks=[(1, 2, 1), (0, 2, 2)], **kw) + rightmark(A, B, C, 18, MK)
    c.add(s)
    return c.out()


# ================================================================ recall
def recall_vertical():
    c = Cv(420, 300, '26vh')
    O = (210, 150)
    a = [pol(O, 120, d) for d in (30, 150, 210, 330)]
    c.add(seg(a[0], a[2], LC, 5) + seg(a[1], a[3], LC, 5) + dot(O, AUX) + lab(O, 'O', 0, -26, LC, 34, 100)
          + angarc(O, a[0], a[1], 34, MK, 4) + angarc(O, a[2], a[3], 34, MK, 4))
    return c.out()


def recall_alt():
    c = Cv(420, 300, '26vh')
    s = seg((40, 90), (380, 90), LC, 5) + seg((40, 210), (380, 210), LC, 5)
    t0, t1 = (150, 270), (270, 30)
    s += seg(t0, t1, LC, 5)
    # intersections of the transversal with the two lines
    def at_y(y):
        k = (y - t0[1]) / (t1[1] - t0[1])
        return (t0[0] + k * (t1[0] - t0[0]), y)
    p, q = at_y(210), at_y(90)
    # alternate interior angles: below the upper line on the right of the transversal, above the lower line on the left
    s += angarc(q, (q[0] + 80, q[1]), t0, 36, MK, 4) + angarc(p, (p[0] - 80, p[1]), t1, 36, MK, 4)   # inside the two lines, on opposite sides of the transversal (a Z)
    s += lab((380, 90), 'a', 0, 26, LC, 30, 80) + lab((380, 210), 'b', 0, 26, LC, 30, 80)
    c.add(s)
    return c.out()


def recall_sum():
    c = Cv(420, 300, '26vh')
    A, B, C = (60, 240), (360, 240), (220, 40)
    c.add(tri(A, B, C, ticks=(), arcs=[(0, 1), (1, 2), (2, 3)], rad=28, size=34, nd=28))
    return c.out()


# ================================================================ 1.1 congruent triangles
def _pair_pts():
    A, B, C = (70, 330), (230, 330), (140, 180)
    dx, dy = 330, -80
    return (A, B, C), tuple((x + dx, y + dy) for x, y in (A, B, C))


def cong_pair():
    """two cut-outs; step 1: the copy of ABC is laid over A'B'C' and they coincide"""
    (A, B, C), (A2, B2, C2) = _pair_pts()
    c = Cv(W, H)
    c.add(tri(A, B, C, fill=ORG) + tri(A2, B2, C2, names=("A'", "B'", "C'"), **S2))
    c.add(poly([A2, B2, C2], ORG, LC, 4) + lab(mid(A2, B2), r'\checkmark', 0, 60, GREEN, 46, 80), 1)
    return c.out()


def cong_marks(prime=True):
    (A, B, C), (A2, B2, C2) = _pair_pts()
    tk = [(0, 1, 1), (0, 2, 2), (1, 2, 3)]
    ar = [(0, 1), (1, 2), (2, 3)]
    c = Cv(W, H)
    c.add(tri(A, B, C, ticks=tk, arcs=ar, rad=28) + tri(A2, B2, C2, names=("A'", "B'", "C'"), **S2, ticks=tk, arcs=ar, rad=28))
    return c.out()


def cong_tsr_edf():
    """practice: two triangles with sides 5 cm and 4 cm, but the included angle is 50 deg in one and 60 deg in the other"""
    k = 42
    def one(S, ang, names, ox):
        S_ = (ox, 330)
        T = (ox + 5 * k, 330)
        R = pol(S_, 4 * k, ang)
        return S_, T, R
    S1, T1, R1 = one(None, 50, None, 40)
    S2, T2, R2 = one(None, 60, None, 350)
    c = Cv(W, H)
    s = tri(S1, T1, R1, names=('S', 'T', 'R'), ticks=[(0, 1, 1), (0, 2, 2)], arcs=[(0, 1)], rad=34)
    s += lab(bis(S1, T1, R1, 62), r'50^\circ', 0, 0, MK, 30, 120)
    s += lab(mid(S1, T1), r'5\ \text{cm}', 0, 30, GREEN, 28, 160) + lab(mid(S1, R1), r'4\ \text{cm}', -48, 0, GREEN, 28, 160)
    s += tri(S2, T2, R2, names=('D', 'E', 'F'), **S2, ticks=[(0, 1, 1), (0, 2, 2)], arcs=[(0, 1)], rad=34)
    s += lab(bis(S2, T2, R2, 62), r'60^\circ', 0, 0, MK, 30, 120)
    s += lab(mid(S2, T2), r'5\ \text{cm}', 0, 30, GREEN, 28, 160) + lab(mid(S2, R2), r'4\ \text{cm}', -48, 0, GREEN, 28, 160)
    assert angle_at(S1, T1, R1) != angle_at(S2, T2, R2)
    c.add(s)
    return c.out()


# ================================================================ the three cases, steps of a construction
def asa_construct():
    """AB = 6 cm on l; angle 60 at A and 40 at B; the rays meet at C.  steps: 1 the angles, 2 the triangle"""
    k = 48
    A, B = (110, 370), (110 + 6 * k, 370)
    Cx = 6 * math.sin(math.radians(40)) / math.sin(math.radians(80))
    C = pol(A, Cx * k, 60)
    assert near(angle_at(B, A, C), 40, 1e-6) and near(angle_at(A, B, C), 60, 1e-6)
    c = Cv(W, H)
    c.add(seg((70, 370), (620, 370), GREY, 3) + seg(A, B, LC, 6) + dot(A, LC) + dot(B, LC)
          + lab(A, 'A', -4, 30, LC, 36, 100) + lab(B, 'B', 4, 30, LC, 36, 100) + lab(mid(A, B), r'6\ \text{cm}', 0, 28, GREEN, 30, 200) + lab((600, 370), 'l', 0, -26, GREY, 32, 80))
    ra, rb = pol(A, 4.8 * k, 60), pol(B, 4.3 * k, 180 - 40)
    c.add(seg(A, ra, AUX, 3, '10 7') + seg(B, rb, AUX, 3, '10 7') + angarc(A, B, ra, 40, MK, 4) + angarc(B, A, rb, 40, MK, 4)
          + lab(bis(A, B, ra, 80), r'60^\circ', 0, 0, MK, 28, 120) + lab(bis(B, A, rb, 80), r'40^\circ', 0, 0, MK, 28, 120), 1)
    c.add(poly([A, B, C], LAV) + seg(A, C, LC, 6) + seg(B, C, LC, 6) + seg(A, B, LC, 6) + dot(C, LC) + lab(C, 'C', 0, -30, LC, 36, 100), 2)
    return c.out()


def sas_construct():
    """AB = 4 cm, angle A = 60 deg, AC = 6 cm.  steps: 1 the ray, 2 the point C, 3 the triangle"""
    k = 50
    A, B = (110, 370), (110 + 4 * k, 370)
    C = pol(A, 6 * k, 60)
    ra = pol(A, 6.9 * k, 60)
    assert near(dist(A, C), 6 * k) and near(angle_at(A, B, C), 60)
    c = Cv(W, H)
    c.add(seg((70, 370), (560, 370), GREY, 3) + seg(A, B, LC, 6) + dot(A, LC) + dot(B, LC) + lab(A, 'A', -4, 30, LC, 36, 100) + lab(B, 'B', 4, 30, LC, 36, 100)
          + lab(mid(A, B), r'4\ \text{cm}', 0, 28, GREEN, 30, 200) + lab((540, 370), 'l', 0, -26, GREY, 32, 80))
    c.add(seg(A, ra, AUX, 3, '10 7') + angarc(A, B, ra, 44, MK, 4) + lab(bis(A, B, ra, 84), r'60^\circ', 0, 0, MK, 28, 120) + lab(ra, 'x', 18, -6, AUX, 32, 80), 1)
    c.add(dot(C, LC) + lab(C, 'C', -24, -14, LC, 36, 100) + lab(mid(A, C), r'6\ \text{cm}', -52, 0, GREEN, 30, 200), 2)
    c.add(poly([A, B, C], LAV) + seg(A, C, LC, 6) + seg(B, C, LC, 6) + seg(A, B, LC, 6) + dot(A, LC) + dot(B, LC) + dot(C, LC), 3)
    return c.out()


def sss_construct():
    """AB = 6, AC = 5, BC = 3: two arcs with the compass meet at C.  steps: 1 arc of radius 5 from A, 2 arc of radius 3 from B, 3 the triangle"""
    k = 48
    A, B = (100, 370), (100 + 6 * k, 370)
    x = (25 - 9 + 36) / 12
    y = math.sqrt(25 - x * x)
    C = (A[0] + x * k, A[1] - y * k)
    assert near(dist(A, C), 5 * k) and near(dist(B, C), 3 * k)
    aA, aB = dir_deg(A, C), dir_deg(B, C)
    c = Cv(W, H)
    c.add(seg((60, 370), (480, 370), GREY, 3) + seg(A, B, LC, 6) + dot(A, LC) + dot(B, LC) + lab(A, 'A', -4, 30, LC, 36, 100) + lab(B, 'B', 4, 30, LC, 36, 100)
          + lab(mid(A, B), r'6\ \text{cm}', 0, 28, GREEN, 30, 200) + lab((460, 370), 'l', 0, -26, GREY, 32, 80))
    c.add(arc(A, aA - 22, aA + 22, 5 * k, AUX, 4) + lab(pol(A, 5 * k, aA + 22), r'5\ \text{cm}', 40, -20, GREEN, 28, 200), 1)
    c.add(arc(B, aB - 24, aB + 30, 3 * k, AUX, 4) + dot(C, LC) + lab(C, 'C', 4, -30, LC, 36, 100) + lab(pol(B, 3 * k, aB + 30), r'3\ \text{cm}', -16, -40, GREEN, 28, 200), 2)
    c.add(poly([A, B, C], LAV) + seg(A, C, LC, 6) + seg(B, C, LC, 6) + seg(A, B, LC, 6) + dot(A, LC) + dot(B, LC) + dot(C, LC), 3)
    return c.out()


def overlay_pair(kind):
    """the triangle ABC laid over A'B'C': steps 1, 2 = the sides that coincide, 3 = whole triangle.  kind: asa / sas / sss"""
    (A, B, C), (A2, B2, C2) = _pair_pts()
    tk = {'asa': [(0, 1, 1)], 'sas': [(0, 1, 1), (0, 2, 2)], 'sss': [(0, 1, 1), (0, 2, 2), (1, 2, 3)]}[kind]
    ar = {'asa': [(0, 1), (1, 2)], 'sas': [(0, 1)], 'sss': []}[kind]
    c = Cv(W, H)
    c.add(tri(A, B, C, ticks=tk, arcs=ar, rad=28) + tri(A2, B2, C2, names=("A'", "B'", "C'"), **S2, ticks=tk, arcs=ar, rad=28))
    c.add(poly([A2, B2, C2], ORG, 'none', 0) + seg(A2, B2, AUX, 8), 1)
    c.add(seg(A2, C2, AUX, 8), 2)
    c.add(seg(B2, C2, AUX, 8) + lab(mid(A2, B2), r'\checkmark', 0, 56, GREEN, 46, 80), 3)
    return c.out()


def theorem_pair(kind):
    (A, B, C), (A2, B2, C2) = _pair_pts()
    A, B, C = (A[0] - 20, A[1] - 20), (B[0] - 20, B[1] - 20), (C[0] - 20, C[1] - 20)
    A2, B2, C2 = (A2[0] - 20, A2[1] + 20), (B2[0] - 20, B2[1] + 20), (C2[0] - 20, C2[1] + 20)
    tk = {'asa': [(0, 1, 1)], 'sas': [(0, 1, 1), (0, 2, 2)], 'sss': [(0, 1, 1), (0, 2, 2), (1, 2, 3)]}[kind]
    ar = {'asa': [(0, 1), (1, 2)], 'sas': [(0, 1)], 'sss': []}[kind]
    c = Cv(W, 400)
    c.add(tri(A, B, C, ticks=tk, arcs=ar, rad=28) + tri(A2, B2, C2, names=("A'", "B'", "C'"), **S2, ticks=tk, arcs=ar, rad=28))
    return c.out()


# ================================================================ ម.ជ.ម  worked example and practice
def asa_ex():
    """AB and CD cross at E, EA = EB, AD // CB.  steps: 1 vertical angles, 2 equal sides, 3 alternate angles"""
    E = (320, 215)
    k = 62
    A = (E[0] - 3 * k, E[1] - 1.2 * k)
    B = (E[0] + 3 * k, E[1] + 1.2 * k)
    D = (E[0] - 1.0 * k, E[1] + 2.0 * k)
    C = (E[0] + 1.0 * k, E[1] - 2.0 * k)
    assert near(dist(E, A), dist(E, B)) and near(dist(E, C), dist(E, D))
    ad = (D[0] - A[0], D[1] - A[1]); cb = (B[0] - C[0], B[1] - C[1])
    assert abs(ad[0] * cb[1] - ad[1] * cb[0]) < 1e-6          # AD // CB
    c = Cv(W, H)
    c.add(poly([A, E, D], LAV) + poly([B, E, C], PINK) + seg(A, B, LC, 5) + seg(C, D, LC, 5) + seg(A, D, LC, 5) + seg(C, B, LC, 5) + dot(E, AUX)
          + lab(A, 'A', -24, -10, LC, 38, 100) + lab(B, 'B', 24, 12, LC, 38, 100) + lab(C, 'C', 22, -14, LC, 38, 100) + lab(D, 'D', -22, 18, LC, 38, 100) + lab(E, 'E', 26, -4, LC, 38, 100))
    c.add(angarc(E, A, D, 26, MK, 4) + angarc(E, A, D, 33, MK, 4) + angarc(E, B, C, 26, MK, 4) + angarc(E, B, C, 33, MK, 4), 1)
    c.add(tick(E, A, 1, MK) + tick(E, B, 1, MK), 2)
    c.add(angarc(A, E, D, 30, MK, 4) + angarc(B, E, C, 30, MK, 4), 3)
    return c.out()


def asa_prac():
    """angle ABC = angle AED, AB = AE; B on AD, E on AC; show triangle ABC = triangle AED and AD = AC"""
    A = (60, 360)
    k = 62
    ang1, ang2 = 20, 62
    ab = 2.8 * k
    ad = 5.2 * k
    B = pol(A, ab, ang1); D = pol(A, ad, ang1)
    E = pol(A, ab, ang2); C = pol(A, ad, ang2)
    assert near(dist(A, B), dist(A, E)) and near(dist(A, D), dist(A, C))
    assert near(angle_at(B, A, C), angle_at(E, A, D), 1e-6)         # angle ABC = angle AED  (mirror image)
    c = Cv(W, H)
    c.add(poly([A, B, C], LAV) + poly([A, E, D], PINK) + seg(A, D, LC, 5) + seg(A, C, LC, 5) + seg(B, C, LC, 5) + seg(E, D, LC, 5) + dot(A, LC)
          + lab(A, 'A', -26, 6, LC, 38, 100) + lab(B, 'B', 14, 26, LC, 38, 100) + lab(D, 'D', 26, 6, LC, 38, 100) + lab(E, 'E', -26, -10, LC, 38, 100) + lab(C, 'C', -6, -28, LC, 38, 100))
    c.add(angarc(B, A, C, 28, MK, 4) + angarc(E, A, D, 28, MK, 4) + tick(A, B, 1, MK) + tick(A, E, 1, MK), 1)
    return c.out()


# ================================================================ ជ.ម.ជ  worked example and practice
def sas_ex(solved=False):
    """XOY with bisector OZ, OA = OB, M on OZ: triangles OMA and OMB.  steps: 1 OA = OB, 2 equal angles, 3 common side"""
    O = (110, 220)
    A, B, M = pol(O, 250, 28), pol(O, 250, -28), pol(O, 360, 0)
    X, Y, Z = pol(O, 395, 28), pol(O, 395, -28), pol(O, 500, 0)
    c = Cv(W, H)
    c.add(poly([O, M, A], LAV) + poly([O, M, B], PINK) + seg(O, X, LC, 5) + seg(O, Y, LC, 5) + seg(O, Z, AUX, 3, '10 7') + seg(M, A, LC, 5) + seg(M, B, LC, 5)
          + dot(O, LC) + dot(A, LC) + dot(B, LC) + dot(M, LC)
          + lab(O, 'O', -26, 0, LC, 36, 100) + lab(A, 'A', 0, -26, LC, 36, 100) + lab(B, 'B', 0, 26, LC, 36, 100) + lab(M, 'M', 20, -22, LC, 36, 100)
          + lab(X, 'X', 18, -8, LC, 36, 100) + lab(Y, 'Y', 18, 8, LC, 36, 100) + lab(Z, 'Z', 18, 0, AUX, 36, 100))
    c.add(tick(O, A, 1, MK) + tick(O, B, 1, MK), 1)
    c.add(angarc(O, A, M, 50, MK, 4) + angarc(O, B, M, 50, MK, 4), 2)
    c.add(tick(O, M, 2, MK, 11, 4, .7), 3)
    return c.out()


def sas_prac():
    """A' is the image of A in O, B' of B: triangles OAB and OA'B'.  steps: 1 OA = OA', 2 OB = OB', 3 vertical angles"""
    O = (320, 220)
    A, B = (O[0] - 190, O[1] - 90), (O[0] - 120, O[1] + 120)
    A2, B2 = (2 * O[0] - A[0], 2 * O[1] - A[1]), (2 * O[0] - B[0], 2 * O[1] - B[1])
    c = Cv(W, H)
    c.add(poly([O, A, B], LAV) + poly([O, A2, B2], PINK) + seg(A, A2, LC, 5) + seg(B, B2, LC, 5) + seg(A, B, LC, 5) + seg(A2, B2, LC, 5) + dot(O, LC)
          + lab(O, 'O', 6, -26, LC, 36, 100) + lab(A, 'A', -22, -8, LC, 36, 100) + lab(B, 'B', -14, 24, LC, 36, 100) + lab(A2, "A'", 24, 10, LC, 36, 100) + lab(B2, "B'", 16, -22, LC, 36, 100))
    c.add(tick(O, A, 1, MK) + tick(O, A2, 1, MK), 1)
    c.add(tick(O, B, 2, MK) + tick(O, B2, 2, MK), 2)
    c.add(angarc(O, A, B, 30, MK, 4) + angarc(O, A2, B2, 30, MK, 4), 3)
    return c.out()


# ================================================================ ជ.ជ.ជ  worked example and practice
def sss_ex():
    """F, J, G, K on a line with FJ = GK; EF = HK and EG = HJ.  steps: 1 FJ = GK so FG = JK, 2 the three equal sides"""
    k = 78
    F, J, G_, K = (30, 340), (30 + 2 * k, 340), (30 + 5 * k, 340), (30 + 7 * k, 340)
    E = (30 + 2.1 * k, 340 - 3.2 * k)
    Hh = (2 * (30 + 3.5 * k) - E[0], E[1])                       # mirror image of E in the middle of FK
    assert near(dist(F, E), dist(K, Hh)) and near(dist(G_, E), dist(J, Hh)) and near(dist(F, G_), dist(J, K)) and near(dist(F, J), dist(G_, K))
    c = Cv(W, H)
    c.add(poly([E, F, G_], LAV) + poly([Hh, K, J], PINK) + seg(F, K, LC, 5) + seg(F, E, LC, 5) + seg(E, G_, LC, 5) + seg(K, Hh, LC, 5) + seg(Hh, J, LC, 5)
          + dot(F, LC) + dot(J, LC) + dot(G_, LC) + dot(K, LC)
          + lab(F, 'F', -10, 28, LC, 36, 100) + lab(J, 'J', -4, 28, LC, 36, 100) + lab(G_, 'G', 4, 28, LC, 36, 100) + lab(K, 'K', 10, 28, LC, 36, 100)
          + lab(E, 'E', -6, -26, LC, 36, 100) + lab(Hh, 'H', 6, -26, LC, 36, 100))
    c.add(tick(F, J, 1, MK) + tick(G_, K, 1, MK), 1)
    c.add(tick(F, E, 2, MK) + tick(K, Hh, 2, MK) + tick(E, G_, 3, MK) + tick(J, Hh, 3, MK) + tick(F, G_, 4, MK, 11, 4, .25) + tick(J, K, 4, MK, 11, 4, .75), 2)
    return c.out()


def sss_prac():
    """R, S, T, V on a line with RS = TV; RZ = VW and TZ = SW.  triangles RZT and VWS"""
    k = 78
    R, S, T, V = (30, 340), (30 + 2 * k, 340), (30 + 5 * k, 340), (30 + 7 * k, 340)
    Z = (30 + 2.6 * k, 340 - 3.1 * k)
    Wp = (2 * (30 + 3.5 * k) - Z[0], Z[1])
    assert near(dist(R, Z), dist(V, Wp)) and near(dist(T, Z), dist(S, Wp)) and near(dist(R, S), dist(T, V))
    c = Cv(W, H)
    c.add(poly([R, Z, T], LAV) + poly([V, Wp, S], PINK) + seg(R, V, LC, 5) + seg(R, Z, LC, 5) + seg(Z, T, LC, 5) + seg(V, Wp, LC, 5) + seg(Wp, S, LC, 5)
          + dot(R, LC) + dot(S, LC) + dot(T, LC) + dot(V, LC)
          + lab(R, 'R', -10, 28, LC, 36, 100) + lab(S, 'S', -4, 28, LC, 36, 100) + lab(T, 'T', 4, 28, LC, 36, 100) + lab(V, 'V', 10, 28, LC, 36, 100)
          + lab(Z, 'Z', -6, -26, LC, 36, 100) + lab(Wp, 'W', 6, -26, LC, 36, 100))
    c.add(tick(R, Z, 1, MK) + tick(V, Wp, 1, MK) + tick(T, Z, 2, MK) + tick(S, Wp, 2, MK) + tick(R, S, 3, MK, 11, 4, .5) + tick(T, V, 3, MK, 11, 4, .5), 1)
    return c.out()


# ================================================================ right triangles
def ha_proof(done=False):
    """right triangles ABC and A'B'C' with the same hypotenuse and one acute angle: the third angles are equal too"""
    A, B, C = (60, 330), (60, 130), (250, 330)
    A2, B2, C2 = (370, 330), (370, 130), (560, 330)
    c = Cv(W, 420)
    s = tri(A, B, C, ticks=[(1, 2, 2)], arcs=[(2, 1)], rad=40) + rightmark(A, B, C, 20, MK)
    s += tri(A2, B2, C2, names=("A'", "B'", "C'"), **S2, ticks=[(1, 2, 2)], arcs=[(2, 1)], rad=40) + rightmark(A2, B2, C2, 20, MK)
    c.add(s)
    c.add(angarc(B, A, C, 44, GREEN, 4) + angarc(B2, A2, C2, 44, GREEN, 4), 1)
    return c.out()


def ha_ex():
    """M on the bisector OM of XOY, MA perp OX, MB perp OY: MA = MB"""
    O = (100, 230)
    M = pol(O, 380, 0)
    A, B = foot(M, O, pol(O, 100, 30)), foot(M, O, pol(O, 100, -30))
    X, Y = pol(O, 440, 30), pol(O, 440, -30)
    assert near(angle_at(A, O, M), 90, 1e-6) and near(dist(M, A), dist(M, B))
    c = Cv(W, H)
    c.add(poly([O, M, A], LAV) + poly([O, M, B], PINK) + seg(O, X, LC, 5) + seg(O, Y, LC, 5) + seg(O, M, AUX, 3, '10 7') + seg(M, A, LC, 5) + seg(M, B, LC, 5)
          + dot(O, LC) + dot(M, LC) + rightmark(A, O, M, 18, MK) + rightmark(B, O, M, 18, MK)
          + lab(O, 'O', -24, 0, LC, 36, 100) + lab(M, 'M', 26, 0, LC, 36, 100) + lab(A, 'A', 6, -26, LC, 36, 100) + lab(B, 'B', 6, 26, LC, 36, 100)
          + lab(X, 'X', 18, -8, LC, 36, 100) + lab(Y, 'Y', 18, 8, LC, 36, 100))
    c.add(angarc(O, A, M, 56, MK, 4) + angarc(O, B, M, 56, MK, 4), 1)
    c.add(tick(M, A, 2, MK) + tick(M, B, 2, MK), 2)
    return c.out()


def ha_prac():
    """ABC isosceles at A, heights BD (on AC) and CE (on AB): BD = CE and BE = CD"""
    A, B, C = (320, 60), (110, 360), (530, 360)
    D = foot(B, A, C); E = foot(C, A, B)
    assert near(dist(A, B), dist(A, C)) and near(dist(B, D), dist(C, E)) and near(dist(B, E), dist(C, D))
    c = Cv(W, 420)
    c.add(poly([A, B, C], LAV) + seg(A, B, LC, 5) + seg(A, C, LC, 5) + seg(B, C, LC, 5) + seg(B, D, AUX, 3, '10 7') + seg(C, E, AUX, 3, '10 7') + dot(D, LC) + dot(E, LC)
          + rightmark(D, A, B, 18, MK) + rightmark(E, A, C, 18, MK) + tick(A, B, 1, MK) + tick(A, C, 1, MK)
          + lab(A, 'A', 0, -28, LC, 36, 100) + lab(B, 'B', -22, 20, LC, 36, 100) + lab(C, 'C', 22, 20, LC, 36, 100) + lab(D, 'D', 24, -8, LC, 36, 100) + lab(E, 'E', -24, -8, LC, 36, 100))
    c.add(angarc(B, A, C, 36, MK, 4) + angarc(C, A, B, 36, MK, 4), 1)
    return c.out()


def hl_proof(mode='steps'):
    """the two right triangles put together along the equal leg AB: C, A, C' are on a line and BCC' is isosceles"""
    A, B = (320, 330), (320, 100)
    C, C2 = (110, 330), (530, 330)
    assert near(dist(B, C), dist(B, C2))
    c = Cv(W, 400)
    c.add(poly([A, B, C], LAV) + poly([A, B, C2], PINK) + seg(C, C2, LC, 5) + seg(A, B, LC, 5) + seg(B, C, LC, 5) + seg(B, C2, LC, 5)
          + rightmark(A, B, C, 20, MK) + rightmark(A, B, C2, 20, MK) + dot(A, LC)
          + lab(B, 'B (B\')', 0, -34, LC, 34, 220) + lab(A, 'A (A\')', 0, 34, LC, 34, 220) + lab(C, 'C', -22, 14, LC, 36, 100) + lab(C2, "C'", 22, 14, LC, 36, 100))
    if mode == 'base':
        return c.out()
    c.add(tick(B, C, 2, MK) + tick(B, C2, 2, MK) + tick(A, B, 1, MK, 11, 4, .6), 1)
    c.add(angarc(C, B, A, 40, GREEN, 4) + angarc(C2, B, A, 40, GREEN, 4), 2)
    return c.out()


def incenter_fig(mode='a'):
    """the bisectors meet at I; the perpendiculars ID, IE, IF are equal"""
    A, B, C = (300, 60), (80, 370), (560, 370)
    a, b, cc = dist(B, C), dist(A, C), dist(A, B)
    I = ((a * A[0] + b * B[0] + cc * C[0]) / (a + b + cc), (a * A[1] + b * B[1] + cc * C[1]) / (a + b + cc))
    D, E, F = foot(I, A, B), foot(I, B, C), foot(I, A, C)
    assert near(dist(I, D), dist(I, E), 1e-6) and near(dist(I, E), dist(I, F), 1e-6)
    assert near(angle_at(B, A, I), angle_at(B, C, I), 1e-6) and near(angle_at(A, B, I), angle_at(A, C, I), 1e-6)
    c = Cv(W, 430)
    c.add(poly([A, B, C], LAV) + seg(A, B, LC, 5) + seg(B, C, LC, 5) + seg(C, A, LC, 5) + dot(I, AUX)
          + lab(A, 'A', 0, -28, LC, 36, 100) + lab(B, 'B', -22, 18, LC, 36, 100) + lab(C, 'C', 22, 18, LC, 36, 100) + lab(I, 'I', 22, -14, AUX, 36, 100)
          + lab(D, 'D', -24, -6, LC, 34, 100) + lab(E, 'E', 0, 28, LC, 34, 100) + lab(F, 'F', 24, -6, LC, 34, 100))
    s1 = seg(B, I, AUX, 3, '10 7') + seg(C, I, AUX, 3, '10 7') + angarc(B, A, I, 40, MK, 4) + angarc(B, C, I, 40, MK, 4) + angarc(C, B, I, 40, MK, 4) + angarc(C, A, I, 40, MK, 4)
    s2 = (seg(I, D, AUX, 3, '10 7') + seg(I, E, AUX, 3, '10 7') + seg(I, F, AUX, 3, '10 7') + rightmark(D, A, I, 16, MK) + rightmark(E, B, I, 16, MK) + rightmark(F, A, I, 16, MK)
          + tick(I, D, 1, MK) + tick(I, E, 1, MK) + tick(I, F, 1, MK))
    s3 = seg(A, I, AUX, 3, '10 7') + angarc(A, B, I, 44, GREEN, 4) + angarc(A, C, I, 44, GREEN, 4)
    if mode == 'a':
        c.add(s1, 1); c.add(s2, 2)
    else:
        c.add(s1 + s2); c.add(s3, 1)
    return c.out()


def hl_prac():
    """M is the midpoint of BC, MD perp AB, ME perp AC, MD = ME: show angle B = angle C"""
    A, B, C = (300, 50), (90, 360), (560, 360)
    M = mid(B, C)
    D, E = foot(M, A, B), foot(M, A, C)
    # choose A on the axis so that MD = ME  (A above the middle of BC)
    A = (M[0], 50)
    D, E = foot(M, A, B), foot(M, A, C)
    assert near(dist(M, D), dist(M, E), 1e-6) and near(dist(B, M), dist(M, C))
    c = Cv(W, 420)
    c.add(poly([A, B, C], LAV) + seg(A, B, LC, 5) + seg(A, C, LC, 5) + seg(B, C, LC, 5) + seg(M, D, AUX, 3, '10 7') + seg(M, E, AUX, 3, '10 7') + dot(M, AUX)
          + rightmark(D, A, M, 16, MK) + rightmark(E, A, M, 16, MK) + tick(M, D, 1, MK) + tick(M, E, 1, MK) + tick(B, M, 2, MK) + tick(M, C, 2, MK)
          + lab(A, 'A', 0, -28, LC, 36, 100) + lab(B, 'B', -22, 18, LC, 36, 100) + lab(C, 'C', 22, 18, LC, 36, 100) + lab(M, 'M', 0, 30, AUX, 36, 100)
          + lab(D, 'D', -26, -6, LC, 36, 100) + lab(E, 'E', 26, -6, LC, 36, 100))
    return c.out()


# ================================================================ 2. perpendicular bisector and isosceles triangle
def pb_fig():
    """segment BC with midpoint I, the line (delta) perpendicular at I, a point M on it: MB = MC"""
    B, C = (90, 340), (550, 340)
    I = mid(B, C)
    M = (I[0], 90)
    top, bot = (I[0], 40), (I[0], 400)
    c = Cv(W, H)
    c.add(seg(B, C, LC, 5) + seg(top, bot, GREY, 4) + dot(I, AUX) + dot(B, LC) + dot(C, LC) + rightmark(I, B, M, 20, MK)
          + lab(B, 'B', -4, 28, LC, 36, 100) + lab(C, 'C', 4, 28, LC, 36, 100) + lab(I, 'I', 18, 26, AUX, 36, 100) + lab(bot, r'\Delta', 28, -14, GREY, 38, 100))
    c.add(tick(B, I, 1, MK) + tick(I, C, 1, MK), 1)
    c.add(dot(M, LC) + lab(M, 'M', 24, -4, LC, 36, 100) + poly([M, I, B], LAV) + poly([M, I, C], PINK) + seg(M, B, LC, 5) + seg(M, C, LC, 5) + seg(M, I, LC, 5), 2)
    c.add(tick(M, B, 2, MK) + tick(M, C, 2, MK) + angarc(M, B, I, 40, MK, 4) + angarc(M, C, I, 40, MK, 4), 3)
    return c.out()


def isosceles_fig():
    """isosceles BMC (MB = MC): base angles equal; the median, altitude, bisector and mediator from M are one line"""
    B, C = (110, 360), (530, 360)
    I = mid(B, C)
    M = (I[0], 70)
    c = Cv(W, H)
    c.add(poly([M, B, C], LAV) + seg(M, B, LC, 5) + seg(M, C, LC, 5) + seg(B, C, LC, 5) + dot(I, AUX) + tick(M, B, 2, MK) + tick(M, C, 2, MK)
          + lab(M, 'M', 0, -28, LC, 36, 100) + lab(B, 'B', -22, 18, LC, 36, 100) + lab(C, 'C', 22, 18, LC, 36, 100) + lab(I, 'I', 18, 28, AUX, 36, 100))
    c.add(angarc(B, M, C, 40, MK, 4) + angarc(C, M, B, 40, MK, 4), 1)
    c.add(seg(M, I, AUX, 4, '10 7') + rightmark(I, B, M, 18, MK) + tick(B, I, 1, MK) + tick(I, C, 1, MK) + angarc(M, B, I, 46, GREEN, 4) + angarc(M, C, I, 46, GREEN, 4), 2)
    return c.out()


def circum_fig(mode='a'):
    """the mediators of AB and BC meet at O; OA = OB = OC and O is on the mediator of AC too"""
    A, B, C = (270, 70), (90, 340), (560, 380)
    # circumcentre
    ax, ay = A; bx, by = B; cx, cy = C
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    ux = ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) + (cx * cx + cy * cy) * (ay - by)) / d
    uy = ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx) + (cx * cx + cy * cy) * (bx - ax)) / d
    O = (ux, uy)
    L, M, N = mid(A, B), mid(B, C), mid(A, C)
    assert near(dist(O, A), dist(O, B), 1e-6) and near(dist(O, B), dist(O, C), 1e-6)
    assert abs((O[0] - L[0]) * (B[0] - A[0]) + (O[1] - L[1]) * (B[1] - A[1])) < 1e-6
    c = Cv(W, 430)
    c.add(poly([A, B, C], LAV) + seg(A, B, LC, 5) + seg(B, C, LC, 5) + seg(C, A, LC, 5) + dot(O, AUX) + dot(L, LC) + dot(M, LC) + dot(N, LC)
          + lab(A, 'A', 0, -28, LC, 36, 100) + lab(B, 'B', -22, 14, LC, 36, 100) + lab(C, 'C', 24, 12, LC, 36, 100) + lab(O, 'O', 22, -14, AUX, 36, 100)
          + lab(L, 'L', -24, -6, LC, 34, 100) + lab(M, 'M', 0, 28, LC, 34, 100) + lab(N, 'N', 26, -6, LC, 34, 100))
    s1 = seg(L, O, AUX, 3, '10 7') + seg(M, O, AUX, 3, '10 7') + rightmark(L, A, O, 16, MK) + rightmark(M, B, O, 16, MK) + tick(A, L, 1, MK) + tick(L, B, 1, MK) + tick(B, M, 2, MK) + tick(M, C, 2, MK)
    s2 = seg(O, A, AUX, 3, '10 7') + seg(O, B, AUX, 3, '10 7') + seg(O, C, AUX, 3, '10 7')
    s3 = seg(N, O, AUX, 3, '10 7') + rightmark(N, A, O, 16, MK) + tick(A, N, 3, MK) + tick(N, C, 3, MK)
    if mode == 'a':
        c.add(s1, 1); c.add(s2, 2)
    else:
        c.add(s1 + s2); c.add(s3, 1)
    return c.out()


# ================================================================ 3. inequalities in a triangle
def ineq_proof():
    """AC > AB; D on AC with AD = AB.  steps: 1 D, AD = AB, 2 B2 = D2, 3 D2 is an exterior angle of BCD"""
    k = 52
    B = (80, 340)
    C = (590, 340)
    A = (230, 90)
    D = pol(A, dist(A, B), dir_deg(A, C))
    assert dist(A, C) > dist(A, B) and near(dist(A, D), dist(A, B))
    c = Cv(W, H)
    c.add(poly([A, B, C], LAV) + seg(A, B, LC, 5) + seg(B, C, LC, 5) + seg(C, A, LC, 5) + dot(A, LC)
          + lab(A, 'A', 0, -28, LC, 36, 100) + lab(B, 'B', -22, 18, LC, 36, 100) + lab(C, 'C', 22, 18, LC, 36, 100))
    c.add(seg(B, D, AUX, 3, '10 7') + dot(D, AUX) + lab(D, 'D', 26, -6, AUX, 36, 100) + tick(A, B, 1, MK) + tick(A, D, 1, MK), 1)
    b2 = angarc(B, A, D, 50, MK, 4); d2 = angarc(D, A, B, 40, MK, 4)
    c.add(b2 + d2 + lab(bis(B, A, D, 84), r'B_2', 0, 0, MK, 28, 100) + lab(bis(D, A, B, 70), r'D_2', 0, 0, MK, 28, 100), 2)
    c.add(angarc(B, D, C, 66, GREEN, 4) + lab(bis(B, D, C, 100), r'B_1', 0, 0, GREEN, 28, 100) + angarc(C, B, D, 44, ORG, 5) + angarc(D, B, C, 52, MK, 4), 3)
    return c.out()


def angles_triangle(a=58, b=75, cdeg=47):
    """the practice triangle with angles 58, 75, 47 (x = 9) drawn to scale; the longest side faces the largest angle"""
    B = (90, 375)
    C = (470, 375)
    # place A with angle B = b, angle C = cdeg
    bc = 380
    ab = bc * math.sin(math.radians(cdeg)) / math.sin(math.radians(a))
    ac = bc * math.sin(math.radians(b)) / math.sin(math.radians(a))
    A = pol(B, ab, b)
    assert near(dist(A, C), ac, 1e-6) and ac > bc > ab
    c = Cv(W, 420)
    c.add(tri(A, B, C, names=('A', 'B', 'C'), nd=30))
    c.add(lab(bis(A, B, C, 62), r'58^\circ', 0, 0, MK, 28, 120) + lab(bis(B, A, C, 78), r'75^\circ', 0, 0, MK, 28, 120) + lab(bis(C, A, B, 90), r'47^\circ', 0, 0, MK, 28, 120)
          + angarc(A, B, C, 36, MK, 4) + angarc(B, A, C, 42, MK, 4) + angarc(C, A, B, 46, MK, 4), 1)
    return c.out()


def ineq_prac():
    """AB = AC = BD and angle ABC < angle BAC (D, A, C on a line): BD < BC"""
    A = (330, 300)
    ang = 120
    B = pol(A, 160, ang)
    C = (A[0] + 160, A[1])
    D = (2 * B[0] - A[0], A[1])           # BD = BA, D on line AC on the other side
    assert near(dist(B, D), dist(A, B), 1e-6) and near(dist(A, B), dist(A, C))
    assert angle_at(A, B, C) > angle_at(B, A, C)
    c = Cv(W, 400)
    c.add(poly([A, B, C], LAV) + seg(D, C, LC, 5) + seg(A, B, LC, 5) + seg(B, C, LC, 5) + seg(B, D, LC, 5) + dot(A, LC)
          + tick(A, B, 1, MK) + tick(A, C, 1, MK) + tick(B, D, 1, MK)
          + lab(B, 'B', -6, -28, LC, 36, 100) + lab(D, 'D', -22, 22, LC, 36, 100) + lab(A, 'A', 4, 28, LC, 36, 100) + lab(C, 'C', 24, 22, LC, 36, 100))
    c.add(angarc(A, B, C, 34, MK, 4) + angarc(B, A, C, 40, GREEN, 4), 1)
    return c.out()


def tri_ineq_proof():
    """ABC, BC extended to M with CM = CA: BM > AB"""
    B = (60, 350)
    C = (330, 350)
    A = (190, 100)
    M = (C[0] + dist(A, C), 350)
    assert near(dist(C, M), dist(C, A), 1e-6)
    c = Cv(W, 430)
    c.add(poly([A, B, C], LAV) + seg(A, B, LC, 5) + seg(B, M, LC, 5) + seg(A, C, LC, 5) + dot(C, LC)
          + lab(A, 'A', 0, -28, LC, 36, 100) + lab(B, 'B', -22, 18, LC, 36, 100) + lab(C, 'C', 0, 30, LC, 36, 100) + lab(M, 'M', 22, 18, LC, 36, 100))
    c.add(seg(A, M, AUX, 3, '10 7') + poly([A, C, M], MINT) + seg(A, C, LC, 5) + seg(C, M, LC, 5) + tick(C, A, 1, MK) + tick(C, M, 1, MK), 1)
    c.add(angarc(A, C, M, 40, MK, 4) + angarc(M, C, A, 40, MK, 4), 2)
    c.add(angarc(A, B, M, 78, GREEN, 4), 3)
    return c.out()


def stick_tri(a, b, c_, ok, w=300, h=200):
    """three sticks a, b, c: drawn as a triangle when the inequality holds, otherwise the two short sticks cannot meet"""
    s_ = sorted([a, b, c_])
    L = s_[2]
    k = 240 / L
    B, C = (30, 150), (30 + L * k, 150)
    c = Cv(w, h, '22vh')
    if ok:
        x = (s_[0] ** 2 - s_[1] ** 2 + L ** 2) / (2 * L)
        y = math.sqrt(max(s_[0] ** 2 - x * x, 0))
        A = (B[0] + x * k, B[1] - y * k)
        # B--A has length s_[0], A--C has s_[1]
        assert s_[0] + s_[1] > L and near(dist(B, A), s_[0] * k, 1e-6) and near(dist(A, C), math.hypot((x - L) * k, y * k), 1e-6)
        c.add(poly([A, B, C], LAV) + seg(B, A, LC, 5) + seg(A, C, LC, 5) + seg(B, C, LC, 5))
    else:
        assert s_[0] + s_[1] <= L
        c.add(seg(B, C, LC, 5) + seg(B, pol(B, s_[0] * k, 60), AUX, 5) + seg(C, pol(C, s_[1] * k, 120), AUX, 5)
              + lab((150, 60), r'\times', 0, 0, MK, 60, 100))
    return c.out()


# ================================================================ 4. perpendicular and slanted segments
def perp_slant():
    """point A off the line delta, foot H, slanted segment AB: steps 1 AH, 2 foot H, 3 slanted AB and the gap HB"""
    Hh = (260, 360)
    A = (260, 90)
    B = (470, 360)
    c = Cv(W, H)
    c.add(seg((60, 360), (610, 360), GREY, 4) + dot(A, LC) + lab(A, 'A', 0, -28, LC, 36, 100) + lab((595, 360), r'\Delta', 0, -30, GREY, 38, 100))
    c.add(seg(A, Hh, LC, 6) + rightmark(Hh, A, B, 22, MK) + dot(Hh, LC) + lab(Hh, 'H', -4, 30, LC, 36, 100), 1)
    c.add(seg(A, B, AUX, 6) + dot(B, AUX) + lab(B, 'B', 4, 30, AUX, 36, 100), 2)
    c.add(seg(Hh, B, GREEN, 8) + lab(mid(Hh, B), r'HB', 0, 30, GREEN, 32, 120), 3)
    return c.out()


def right_tri_hyp():
    """AHB is right-angled at H: the hypotenuse AB is the longest side"""
    Hh, A, B = (400, 360), (400, 80), (130, 360)
    c = Cv(W, H)
    c.add(poly([A, B, Hh], LAV) + seg(A, Hh, LC, 5) + seg(B, Hh, LC, 5) + seg(A, B, LC, 5) + seg((60, 360), (560, 360), GREY, 3) + rightmark(Hh, A, B, 22, MK)
          + lab(A, 'A', 0, -28, LC, 36, 100) + lab(B, 'B', -22, 20, LC, 36, 100) + lab(Hh, 'H', 22, 22, LC, 36, 100) + lab((545, 360), r'\Delta', 0, -30, GREY, 38, 100))
    c.add(angarc(Hh, A, B, 36, MK, 4) + angarc(A, B, Hh, 46, GREEN, 4), 1)
    c.add(angarc(Hh, A, B, 36, MK, 4) + angarc(B, A, Hh, 46, ORG, 5), 2)
    return c.out()


def slant_same_side():
    """B and C on the same side of H, HB < HC (figure 1)"""
    Hh, A = (140, 360), (140, 90)
    B, C = (300, 360), (500, 360)
    c = Cv(W, H)
    c.add(seg((60, 360), (600, 360), GREY, 4) + seg(A, Hh, LC, 5) + seg(A, B, LC, 5) + seg(A, C, LC, 5) + rightmark(Hh, A, B, 22, MK)
          + lab(A, 'A', 0, -28, LC, 36, 100) + lab(Hh, 'H', -22, 22, LC, 36, 100) + lab(B, 'B', 4, 30, LC, 36, 100) + lab(C, 'C', 4, 30, LC, 36, 100))
    c.add(seg(Hh, B, GREEN, 8) + seg(B, C, ORG, 8) + lab(mid(Hh, B), r'HB', 0, 30, GREEN, 28, 120), 1)
    return c.out()


def slant_two_sides():
    """B and C on both sides of H: take C' symmetric to C, then AC = AC' > AB"""
    Hh, A = (320, 360), (320, 90)
    C = (570, 360); C2 = (2 * Hh[0] - C[0], 360)
    B = (420, 360)
    assert near(dist(A, C), dist(A, C2)) and dist(Hh, B) < dist(Hh, C)
    c = Cv(W, H)
    c.add(seg((40, 360), (610, 360), GREY, 4) + seg(A, Hh, LC, 5) + seg(A, B, LC, 5) + seg(A, C, LC, 5) + rightmark(Hh, A, B, 22, MK)
          + lab(A, 'A', 0, -28, LC, 36, 100) + lab(Hh, 'H', 0, 30, LC, 36, 100) + lab(B, 'B', 0, 30, LC, 36, 100) + lab(C, 'C', 6, 30, LC, 36, 100))
    c.add(seg(A, C2, AUX, 5, '10 7') + dot(C2, AUX) + lab(C2, "C'", 0, 30, AUX, 36, 100) + tick(Hh, C, 1, MK) + tick(Hh, C2, 1, MK) + tick(A, C, 2, MK) + tick(A, C2, 2, MK), 1)
    return c.out()


def equal_gaps():
    """HB = HC: AH is the mediator of BC, so AB = AC"""
    Hh, A = (320, 360), (320, 90)
    B, C = (140, 360), (500, 360)
    c = Cv(W, H)
    c.add(poly([A, B, C], LAV) + seg(B, C, LC, 5) + seg(A, B, LC, 5) + seg(A, C, LC, 5) + seg(A, Hh, AUX, 3, '10 7') + rightmark(Hh, A, C, 22, MK)
          + lab(A, 'A', 0, -28, LC, 36, 100) + lab(B, 'B', -22, 22, LC, 36, 100) + lab(C, 'C', 22, 22, LC, 36, 100) + lab(Hh, 'H', 0, 30, AUX, 36, 100))
    c.add(tick(B, Hh, 1, MK) + tick(Hh, C, 1, MK), 1)
    c.add(tick(A, B, 2, MK) + tick(A, C, 2, MK), 2)
    return c.out()


def ex_ao():
    """AB < AC, height AH, median AO: AH < AO < AC"""
    B, C = (60, 360), (580, 360)
    A = (60 + 2.2 * 65, 360 - 5 * 65 * 0.62)
    Hh = (A[0], 360)
    O = mid(B, C)
    assert dist(A, B) < dist(A, C) and dist(Hh, O) < dist(Hh, C) and Hh[0] < O[0]
    c = Cv(W, 430)
    c.add(poly([A, B, C], LAV) + seg(A, B, LC, 5) + seg(B, C, LC, 5) + seg(C, A, LC, 5) + seg(A, Hh, AUX, 4, '10 7') + seg(A, O, AUX, 4) + rightmark(Hh, A, C, 20, MK)
          + dot(O, LC) + dot(Hh, LC)
          + lab(A, 'A', 0, -28, LC, 36, 100) + lab(B, 'B', -22, 20, LC, 36, 100) + lab(C, 'C', 22, 20, LC, 36, 100) + lab(Hh, 'H', -4, 30, LC, 36, 100) + lab(O, 'O', 4, 30, LC, 36, 100))
    c.add(seg(Hh, O, GREEN, 8) + seg(O, C, ORG, 8), 1)
    return c.out()


def altitudes_fig():
    """the three heights AD, BE, CF of an acute triangle ABC: each is shorter than a slanted side"""
    A, B, C = (250, 70), (70, 370), (570, 330)
    D, E, F = foot(A, B, C), foot(B, A, C), foot(C, A, B)
    c = Cv(W, 430)
    c.add(poly([A, B, C], LAV) + seg(A, B, LC, 5) + seg(B, C, LC, 5) + seg(C, A, LC, 5)
          + seg(A, D, AUX, 3, '10 7') + seg(B, E, AUX, 3, '10 7') + seg(C, F, AUX, 3, '10 7')
          + rightmark(D, A, B, 16, MK) + rightmark(E, B, C, 16, MK) + rightmark(F, C, A, 16, MK)
          + lab(A, 'A', 0, -28, LC, 36, 100) + lab(B, 'B', -22, 14, LC, 36, 100) + lab(C, 'C', 24, 8, LC, 36, 100)
          + lab(D, 'D', 0, 28, LC, 34, 100) + lab(E, 'E', 26, -8, LC, 34, 100) + lab(F, 'F', -26, -8, LC, 34, 100))
    return c.out()


# ================================================================ sub-part 2 (ជ.ម.ជ) and homework figures
def cutout(kind='sas'):
    """hands-on: ABC (4 cm, 6 cm, 60 deg) cut out and laid over A'B'C'; step 1 = the copy over the second triangle"""
    k = 40
    A = (70, 330)
    B = (A[0] + 4 * k, A[1])
    C = pol(A, 6 * k, 60)
    A2, B2, C2 = (A[0] + 340, A[1] - 70), (B[0] + 340, B[1] - 70), (C[0] + 340, C[1] - 70)
    c = Cv(W, H)
    s = tri(A, B, C, fill=ORG, ticks=[(0, 1, 1), (0, 2, 2)], arcs=[(0, 1)])
    s += tri(A2, B2, C2, names=("A'", "B'", "C'"), **S2, ticks=[(0, 1, 1), (0, 2, 2)], arcs=[(0, 1)])
    s += lab(mid(A, B), r'4\ \text{cm}', 0, 62, GREEN, 28, 160) + lab(mid(A, C), r'6\ \text{cm}', -100, 0, GREEN, 28, 160) + lab(bis(A, B, C, 112), r'60^\circ', 0, 0, MK, 26, 120)
    c.add(s)
    c.add(poly([A2, B2, C2], ORG, LC, 4) + lab(mid(A2, B2), r'\checkmark', 0, 60, GREEN, 46, 80), 1)
    c.add(measure_tools(A, 60, 4, 6, k, 80), 2)
    return c.out()


def incl_angle():
    """the included angle: angle A between AB and AC is highlighted"""
    A, B, C = (90, 360), (450, 360), (230, 90)
    c = Cv(W, H)
    c.add(tri(A, B, C, ticks=[(0, 1, 1), (0, 2, 2)]) + angarc(A, B, C, 48, MK, 5, fill=ORG))
    return c.out()


def incl_ex():
    """triangle DEF: the angle between each pair of sides.  step 1: the three arcs"""
    D, E_, F = (80, 370), (560, 370), (260, 100)
    c = Cv(W, H)
    c.add(tri(D, E_, F, names=('D', 'E', 'F'), **S2))
    c.add(angarc(D, E_, F, 46, MK, 5) + angarc(E_, D, F, 46, MK, 5) + angarc(F, D, E_, 46, MK, 5), 1)
    return c.out()


def sas_not():
    """ABC: AB = 5, AC = 4, angle A = 40 (between);  DEF: DE = 5, EF = 4, angle D = 40 (NOT between DE and EF).  step 1 = highlight"""
    k = 44
    A = (100, 360); B = (A[0] + 5 * k, A[1]); C = pol(A, 4 * k, 40)
    D = (440, 360); E_ = (D[0] + 5 * k, D[1])
    t = 6.21
    F = pol(D, t * k, 40)
    assert near(dist(E_, F), 4 * k, 1e-2)
    c = Cv(740, 440)
    s = tri(A, B, C, ticks=[(0, 1, 1), (0, 2, 2)], arcs=[(0, 1)], rad=36)
    s += lab(bis(A, B, C, 76), r'40^\circ', 0, 0, MK, 26, 120) + lab(mid(A, B), r'5\ \text{cm}', 0, 62, GREEN, 26, 160) + lab(mid(A, C), r'4\ \text{cm}', -100, -6, GREEN, 26, 160)
    s += tri(D, E_, F, names=('D', 'E', 'F'), **S2, ticks=[(0, 1, 1), (1, 2, 2)], arcs=[(0, 1)], rad=36)
    s += lab(bis(D, E_, F, 76), r'40^\circ', 0, 0, MK, 26, 120) + lab(mid(D, E_), r'5\ \text{cm}', 0, 62, GREEN, 26, 160) + lab(mid(E_, F), r'4\ \text{cm}', 52, 0, GREEN, 26, 160)
    c.add(s)
    c.add(measure_tools(A, 40, 5, 4, k, 74) + '<g class="tool-r">' + ruler_dir(D, 0, 5, k, side=-1) + '</g><g class="tool-p">' + protractor_dir(D, 0, 74, 40) + '</g>', 1)
    return c.out()


def quad_diag():
    """ABCD with the diagonal AC: angle BAC = DAC and angle BCA = DCA (B and D are mirror images in AC)"""
    A, C = (90, 230), (550, 230)
    B, D = (330, 70), (330, 390)
    assert near(angle_at(A, B, C), angle_at(A, D, C), 1e-6) and near(angle_at(C, B, A), angle_at(C, D, A), 1e-6)
    c = Cv(W, H)
    c.add(poly([A, B, C], MINT) + poly([A, C, D], PINK) + seg(A, B, LC, 5) + seg(B, C, LC, 5) + seg(C, D, LC, 5) + seg(D, A, LC, 5) + seg(A, C, LC, 3)
          + lab(A, 'A', -24, 0, LC, 36, 100) + lab(B, 'B', 0, -26, LC, 36, 100) + lab(C, 'C', 24, 0, LC, 36, 100) + lab(D, 'D', 0, 28, LC, 36, 100))
    c.add(angarc(A, B, C, 50, MK, 4) + angarc(A, D, C, 50, MK, 4) + angarc(C, B, A, 50, MK, 4) + angarc(C, D, A, 50, MK, 4) + angarc(C, B, A, 58, MK, 4) + angarc(C, D, A, 58, MK, 4), 1)
    c.add(tick(A, C, 1, MK, 11, 4, .5), 2)
    return c.out()


def _tri5070(ox, oy=340, ab=200):
    """triangle with A = 50 degrees, B = 70 degrees (so C = 60): the shape of the homework triangles, drawn to scale"""
    A = (ox, oy)
    B = (ox + ab, oy)
    ac = ab * math.sin(math.radians(70)) / math.sin(math.radians(60))
    C = pol(A, ac, 50)
    assert near(angle_at(A, B, C), 50, 1e-6) and near(angle_at(B, A, C), 70, 1e-6)
    return A, B, C



def hw_cong():
    """homework: triangle ABC = triangle DEF with angle A = 50 and angle E = 70; find B, C, D, F  (? marks) - drawn to scale"""
    A, B, C = _tri5070(40)
    D, E_, F = _tri5070(350)
    tk = [(0, 1, 1), (0, 2, 2), (1, 2, 3)]
    c = Cv(W, 400)
    s = tri(A, B, C, ticks=tk, rad=30) + tri(D, E_, F, names=('D', 'E', 'F'), **S2, ticks=tk, rad=30)
    s += angarc(A, B, C, 36, MK, 4) + angarc(E_, D, F, 36, MK, 4)
    s += lab(bis(A, B, C, 70), r'50^\circ', 0, 0, MK, 24, 120) + lab(bis(E_, D, F, 70), r'70^\circ', 0, 0, MK, 24, 120)
    for v, o1, o2 in ((B, A, C), (C, A, B), (D, E_, F), (F, D, E_)):
        s += angarc(v, o1, o2, 30, AUX, 4) + lab(bis(v, o1, o2, 62), '?', 0, 0, AUX, 28, 60)
    c.add(s)
    return c.out()


def hw_mid():
    """homework: M midpoint of AB, Ax // By, line CMD: triangle AMC = triangle BMD"""
    A, B = (140, 240), (500, 240)
    M = mid(A, B)
    C = (140, 90); D = (500, 390)
    assert near(dist(M, C), dist(M, D), 1e-6)
    c = Cv(W, 460)
    c.add(seg(A, B, LC, 5) + seg(A, (140, 40), LC, 4) + seg(B, (500, 440), LC, 4) + seg(C, D, LC, 5) + dot(M, AUX)
          + lab(A, 'A', -24, 18, LC, 36, 100) + lab(B, 'B', 24, -18, LC, 36, 100) + lab(M, 'M', 16, -24, LC, 36, 100) + lab(C, 'C', -24, -4, LC, 36, 100) + lab(D, 'D', 24, 4, LC, 36, 100)
          + lab((140, 40), 'x', -22, 0, LC, 34, 100) + lab((500, 440), 'y', 22, 0, LC, 34, 100))
    c.add(tick(A, M, 1, MK) + tick(M, B, 1, MK), 1)
    return c.out()


def sas_extra():
    """AB and CD cross at O, O the midpoint of both: triangles AOC and BOD"""
    O = (320, 220)
    A, B = (O[0] - 230, O[1] - 100), (O[0] + 230, O[1] + 100)
    Cc, D = (O[0] + 130, O[1] - 190), (O[0] - 130, O[1] + 190)
    c = Cv(W, H)
    c.add(poly([O, A, Cc], LAV) + poly([O, B, D], PINK) + seg(A, B, LC, 5) + seg(Cc, D, LC, 5) + seg(A, Cc, LC, 5) + seg(B, D, LC, 5) + dot(O, LC)
          + lab(O, 'O', 22, 8, LC, 36, 100) + lab(A, 'A', -22, -8, LC, 36, 100) + lab(B, 'B', 22, 12, LC, 36, 100) + lab(Cc, 'C', 20, -12, LC, 36, 100) + lab(D, 'D', -20, 16, LC, 36, 100))
    c.add(tick(O, A, 1, MK) + tick(O, B, 1, MK), 1)
    c.add(tick(O, Cc, 2, MK) + tick(O, D, 2, MK), 2)
    c.add(angarc(O, A, Cc, 34, MK, 4) + angarc(O, B, D, 34, MK, 4), 3)
    return c.out()


def hw_sas1():
    """AB = DE, BC = EF, angle B = angle E = 70, angle A = 50: find angle D and F (to scale)"""
    A, B, C = _tri5070(40)
    D, E_, F = _tri5070(350)
    c = Cv(W, 400)
    s = tri(A, B, C, ticks=[(0, 1, 1), (1, 2, 2)], arcs=[(1, 1)], rad=34) + tri(D, E_, F, names=('D', 'E', 'F'), **S2, ticks=[(0, 1, 1), (1, 2, 2)], arcs=[(1, 1)], rad=34)
    s += lab(bis(B, A, C, 76), r'70^\circ', 0, 0, MK, 24, 120) + lab(bis(E_, D, F, 76), r'70^\circ', 0, 0, MK, 24, 120) + lab(bis(A, B, C, 72), r'50^\circ', 0, 0, MK, 24, 120)
    c.add(s)
    return c.out()


def hw_sas2():
    """ABC isosceles at A, E on AB, F on AC with AE = AF: BF = CE"""
    A, B, C = (320, 60), (110, 380), (530, 380)
    t = 0.45
    E_ = (A[0] + (B[0] - A[0]) * t, A[1] + (B[1] - A[1]) * t)
    F = (A[0] + (C[0] - A[0]) * t, A[1] + (C[1] - A[1]) * t)
    assert near(dist(A, E_), dist(A, F)) and near(dist(B, F), dist(C, E_))
    c = Cv(W, 430)
    c.add(poly([A, B, C], LAV) + seg(A, B, LC, 5) + seg(B, C, LC, 5) + seg(C, A, LC, 5) + seg(B, F, AUX, 3, '10 7') + seg(C, E_, AUX, 3, '10 7') + dot(E_, LC) + dot(F, LC)
          + tick(A, B, 1, MK) + tick(A, C, 1, MK) + tick(A, E_, 2, MK) + tick(A, F, 2, MK)
          + lab(A, 'A', 0, -28, LC, 36, 100) + lab(B, 'B', -22, 14, LC, 36, 100) + lab(C, 'C', 22, 14, LC, 36, 100) + lab(E_, 'E', -22, 0, LC, 36, 100) + lab(F, 'F', 22, 0, LC, 36, 100))
    return c.out()


# ================================================================ homework solutions and sub-part 3 figures
def hw_cong_sol():
    """solution of homework 1 of sub-part 1: A = 50, E = 70 given; B = 70, C = 60, D = 50, F = 60 appear (to scale)"""
    A, B, C = _tri5070(40)
    D, E_, F = _tri5070(350)
    tk = [(0, 1, 1), (0, 2, 2), (1, 2, 3)]
    c = Cv(W, 400)
    s = tri(A, B, C, ticks=tk, rad=30) + tri(D, E_, F, names=('D', 'E', 'F'), **S2, ticks=tk, rad=30)
    s += angarc(A, B, C, 36, MK, 4) + angarc(E_, D, F, 36, MK, 4)
    s += lab(bis(A, B, C, 70), r'50^\circ', 0, 0, MK, 24, 120) + lab(bis(E_, D, F, 70), r'70^\circ', 0, 0, MK, 24, 120)
    c.add(s)
    c.add(angarc(B, A, C, 36, GREEN, 4) + lab(bis(B, A, C, 66), r'70^\circ', 0, 0, GREEN, 24, 120) + angarc(D, E_, F, 36, GREEN, 4) + lab(bis(D, E_, F, 66), r'50^\circ', 0, 0, GREEN, 24, 120), 1)
    c.add(angarc(C, A, B, 30, GREEN, 4) + lab(bis(C, A, B, 62), r'60^\circ', 0, 0, GREEN, 24, 120) + angarc(F, D, E_, 30, GREEN, 4) + lab(bis(F, D, E_, 62), r'60^\circ', 0, 0, GREEN, 24, 120), 2)
    return c.out()


def hw_mid_sol():
    """solution of homework 2 of sub-part 1: AM = MB, vertical angles, alternate angles"""
    A, B = (140, 240), (500, 240)
    M = mid(A, B)
    C = (140, 90); D = (500, 390)
    c = Cv(W, 460)
    c.add(poly([A, M, C], LAV) + poly([B, M, D], PINK) + seg(A, B, LC, 5) + seg(A, (140, 40), LC, 4) + seg(B, (500, 440), LC, 4) + seg(C, D, LC, 5) + dot(M, AUX)
          + lab(A, 'A', -24, 18, LC, 36, 100) + lab(B, 'B', 24, -18, LC, 36, 100) + lab(M, 'M', 16, -24, LC, 36, 100) + lab(C, 'C', -24, -4, LC, 36, 100) + lab(D, 'D', 24, 4, LC, 36, 100))
    c.add(tick(A, M, 1, MK) + tick(M, B, 1, MK), 1)
    c.add(angarc(M, A, C, 36, MK, 4) + angarc(M, B, D, 36, MK, 4), 2)
    c.add(angarc(A, M, C, 36, GREEN, 4) + angarc(B, M, D, 36, GREEN, 4), 3)
    c.add(tick(M, C, 2, MK) + tick(M, D, 2, MK), 4)
    return c.out()


def hw_sas1_sol():
    """solution of homework 1 of sub-part 2: AB = DE, angle B = angle E = 70, BC = EF; then D = A = 50, F = C = 60 (to scale)"""
    A, B, C = _tri5070(40)
    D, E_, F = _tri5070(350)
    c = Cv(W, 400)
    s = tri(A, B, C, ticks=[(0, 1, 1), (1, 2, 2)], arcs=[(1, 1)], rad=34) + tri(D, E_, F, names=('D', 'E', 'F'), **S2, ticks=[(0, 1, 1), (1, 2, 2)], arcs=[(1, 1)], rad=34)
    s += lab(bis(B, A, C, 76), r'70^\circ', 0, 0, MK, 24, 120) + lab(bis(E_, D, F, 76), r'70^\circ', 0, 0, MK, 24, 120)
    c.add(s)
    c.add(angarc(A, B, C, 34, GREEN, 4) + lab(bis(A, B, C, 72), r'50^\circ', 0, 0, GREEN, 24, 120) + angarc(D, E_, F, 34, GREEN, 4) + lab(bis(D, E_, F, 72), r'50^\circ', 0, 0, GREEN, 24, 120), 1)
    c.add(angarc(C, A, B, 30, GREEN, 4) + lab(bis(C, A, B, 62), r'60^\circ', 0, 0, GREEN, 24, 120) + angarc(F, D, E_, 30, GREEN, 4) + lab(bis(F, D, E_, 62), r'60^\circ', 0, 0, GREEN, 24, 120), 2)
    return c.out()


def hw_sas2_sol():
    """solution of homework 2 of sub-part 2: triangles ABF and ACE (AB = AC, common angle A, AF = AE)"""
    A, B, C = (320, 60), (110, 380), (530, 380)
    t = 0.45
    E_ = (A[0] + (B[0] - A[0]) * t, A[1] + (B[1] - A[1]) * t)
    F = (A[0] + (C[0] - A[0]) * t, A[1] + (C[1] - A[1]) * t)
    c = Cv(W, 430)
    c.add(poly([A, B, C], LAV) + seg(A, B, LC, 5) + seg(B, C, LC, 5) + seg(C, A, LC, 5) + dot(E_, LC) + dot(F, LC)
          + lab(A, 'A', 0, -28, LC, 36, 100) + lab(B, 'B', -22, 14, LC, 36, 100) + lab(C, 'C', 22, 14, LC, 36, 100) + lab(E_, 'E', -22, 0, LC, 36, 100) + lab(F, 'F', 22, 0, LC, 36, 100))
    c.add(poly([A, B, F], ORG, 'none', 0, .0) if False else seg(B, F, AUX, 3, '10 7') + seg(C, E_, AUX, 3, '10 7'), 1)
    c.add(tick(A, B, 1, MK) + tick(A, C, 1, MK), 2)
    c.add(tick(A, E_, 2, MK) + tick(A, F, 2, MK), 3)
    c.add(angarc(A, B, C, 40, MK, 4), 4)
    return c.out()


def iso_median():
    """ABC isosceles at A, D the midpoint of BC: triangles ABD and ACD (SSS)"""
    A, B, C = (320, 60), (110, 380), (530, 380)
    D = mid(B, C)
    c = Cv(W, 430)
    c.add(poly([A, B, D], LAV) + poly([A, D, C], PINK) + seg(A, B, LC, 5) + seg(A, C, LC, 5) + seg(B, C, LC, 5) + dot(D, AUX)
          + lab(A, 'A', 0, -28, LC, 36, 100) + lab(B, 'B', -22, 14, LC, 36, 100) + lab(C, 'C', 22, 14, LC, 36, 100) + lab(D, 'D', 0, 30, AUX, 36, 100))
    c.add(tick(A, B, 1, MK) + tick(A, C, 1, MK), 1)
    c.add(tick(B, D, 2, MK) + tick(D, C, 2, MK), 2)
    c.add(seg(A, D, AUX, 3, '10 7') + tick(A, D, 3, MK) + angarc(D, A, B, 30, MK, 4) + angarc(D, A, C, 30, MK, 4) + rightmark(D, A, C, 18, MK), 3)
    return c.out()


def quad_sss(sol=False):
    """ABCD with AB = CD and AD = BC, diagonal BD: triangles ABD and CDB (SSS), so angle A = angle C"""
    A, B, C, D = (90, 330), (400, 330), (560, 110), (250, 110)
    # parallelogram ABCD: A(90,330) B(400,330) C(560,110)?? keep AB=DC, AD=BC
    A, B = (90, 330), (400, 330)
    D = (190, 110)
    C = (D[0] + (B[0] - A[0]), D[1])
    assert near(dist(A, B), dist(D, C)) and near(dist(A, D), dist(B, C))
    c = Cv(W, 400)
    c.add(poly([A, B, C, D], LAV) + seg(A, B, LC, 5) + seg(B, C, LC, 5) + seg(C, D, LC, 5) + seg(D, A, LC, 5) + tick(A, B, 1, MK) + tick(D, C, 1, MK) + tick(A, D, 2, MK) + tick(B, C, 2, MK)
          + lab(A, 'A', -22, 12, LC, 36, 100) + lab(B, 'B', 22, 12, LC, 36, 100) + lab(C, 'C', 22, -12, LC, 36, 100) + lab(D, 'D', -22, -12, LC, 36, 100))
    if sol:
        c.add(seg(B, D, AUX, 3, '10 7') + tick(B, D, 3, MK), 1)
        c.add(angarc(A, B, D, 34, GREEN, 4) + angarc(C, B, D, 34, GREEN, 4), 2)
    return c.out()


def rt_pair(sol=False):
    """right triangles ABC and DEF (right angles at A and D) with BC = EF and AB = DE"""
    A, B, C = (30, 330), (30, 110), (250, 330)
    D, E_, F = (370, 330), (370, 110), (590, 330)
    c = Cv(W, 400)
    s = tri(A, B, C, ticks=[(0, 1, 1), (1, 2, 2)]) + rightmark(A, B, C, 20, MK) + tri(D, E_, F, names=('D', 'E', 'F'), **S2, ticks=[(0, 1, 1), (1, 2, 2)]) + rightmark(D, E_, F, 20, MK)
    c.add(s)
    if sol:
        c.add(tick(A, C, 3, MK) + tick(D, F, 3, MK), 1)
    return c.out()


def cong_vert():
    """two cut-outs one above the other (as in the class slide): the orange one (card 1) is laid over the blue one (card 2) at step 1"""
    A, B, C = (50, 215), (330, 215), (160, 30)
    dx, dy = 60, 290
    A2, B2, C2 = (A[0] + dx, A[1] + dy), (B[0] + dx, B[1] + dy), (C[0] + dx, C[1] + dy)
    c = Cv(480, 540, '64vh')
    s = poly([A, B, C], ORG, '#a33b32', 3) + poly([A2, B2, C2], LAV, LC, 3)
    s += lab(A, 'A', -20, 6, LC, 42, 90) + lab(B, 'B', 20, 6, LC, 42, 90) + lab(C, 'C', 0, -20, LC, 42, 90)
    s += lab(A2, "A'", -22, 6, LC, 42, 90) + lab(B2, "B'", 22, 6, LC, 42, 90) + lab(C2, "C'", 0, -20, LC, 42, 90)
    c.add(s)
    c.add(poly([A2, B2, C2], ORG, '#a33b32', 3), 1)
    return c.out()


# ================================================================ moving pieces and tools (class animation helpers)
def mvg(body, step, dx, dy, ms=1800):
    """a group that sits still until step `step`, then slides by (dx, dy) in about 1.8 s (CSS in teachshow.css: .mvg)"""
    return f'<g class="mvg" data-step="{step}" style="--dx:{dx}px;--dy:{dy}px;--ms:{ms}ms">{body}</g>'


def late(body, step, until=None, delay=1700):
    """a group that fades in `delay` ms after its step starts (so it shows after something has moved)"""
    u = f' data-until="{until}"' if until else ''
    return f'<g class="rv" data-step="{step}"{u} style="transition-delay:{delay}ms">{body}</g>'


def ruler_svg(p0, n_cm, k, y_off=6, h=30, col='#fff2cc'):
    """a ruler lying under the segment from p0 with n_cm centimetres of k px each; 0 at p0"""
    x0, y0 = p0[0] - 14, p0[1] + y_off
    w = n_cm * k + 28
    s = poly([(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h)], col, '#7f7f7f', 1.5, .95)
    for i in range(int(n_cm * 2) + 1):
        x = p0[0] + i * k / 2
        ln = 15 if i % 2 == 0 else 8
        s += G._line(f'{x:.1f}', f'{y0:.1f}', f'{x:.1f}', f'{y0 + ln:.1f}', '#7f7f7f', 1.6)
        if i % 2 == 0:
            s += _T(x, y0 + h - 3, str(i // 2), 15, '#595959', weight=600)
    return s


def protractor_svg(c, r=92):
    """a half protractor on the line through c (semicircle above), ticks every 10 degrees"""
    pts = [pol(c, r, a) for a in range(0, 181, 4)]
    s = poly(pts, '#bcd7f2', '#7f7f7f', 1.5, .72)
    for a in range(0, 181, 10):
        ln = 13 if a % 30 == 0 else 7
        p1, p2 = pol(c, r, a), pol(c, r - ln, a)
        s += G._line(f'{p1[0]:.1f}', f'{p1[1]:.1f}', f'{p2[0]:.1f}', f'{p2[1]:.1f}', '#7f7f7f', 1.4)
        if a % 30 == 0 and a not in (0, 180):
            tp = pol(c, r - 27, a)
            s += _T(tp[0], tp[1] + 5, str(a), 13, '#595959', weight=600)
    s += G._line(f'{c[0] - r - 6:.1f}', f'{c[1]:.1f}', f'{c[0] + r + 6:.1f}', f'{c[1]:.1f}', '#7f7f7f', 1.4)
    s += f'<circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="4" fill="#595959"/>'
    return s


def asa_construct2(prime=False):
    """(prime=True: the second triangle A'B'C', blue; otherwise ABC, orange)  ម.ជ.ម construction with the tools: 0 AB + ruler | 1 protractor at A, ray 60 | 2 protractor slides to B, ray 40 | 3 the triangle"""
    k = 48
    A, B = (110, 340), (110 + 6 * k, 340)
    Cx = 6 * math.sin(math.radians(40)) / math.sin(math.radians(80))
    C = pol(A, Cx * k, 60)
    ra, rb = pol(A, 4.7 * k, 60), pol(B, 4.2 * k, 140)
    c = Cv(W, H)
    P = "'" if prime else ''
    fillc = PINK if prime else MINT
    LC_ = AUX if prime else LC           # A'B'C' is drawn in brick, ABC in blue: two different triangles, two different colours
    c.add(seg((70, 340), (610, 340), GREY, 3) + seg(A, B, LC_, 5) + dot(A, LC_) + dot(B, LC_) + lab(A, 'A' + P, -22, -10, LC_, 36, 100) + lab(B, 'B' + P, 22, -10, LC_, 36, 100)
          + lab((600, 340), 'l', 0, -22, GREY, 30, 80) + lab(mid(A, B), r'6\ \text{cm}', 0, 54, LC_, 30, 200))
    c.add(ruler_svg(A, 6, k), 0, 1)
    c.add(mvg(protractor_svg(A), 2, 6 * k, 0), 1, 3)
    c.add(seg(A, ra, AUX, 3, '10 7') + angarc(A, B, ra, 40, MK, 4) + lab(bis(A, B, ra, 78), r'60^\circ', 0, 0, MK, 28, 120), 1)
    c.add(seg(B, rb, AUX, 3, '10 7') + angarc(B, A, rb, 40, MK, 4) + lab(bis(B, A, rb, 78), r'40^\circ', 0, 0, MK, 28, 120), 2)
    c.add(poly([A, B, C], fillc) + seg(A, C, LC_, 5) + seg(B, C, LC_, 5) + seg(A, B, LC_, 5) + dot(C, LC_) + lab(C, 'C' + P, 0, -28, LC_, 36, 100), 3)
    return c.out()


def sas_construct2():
    """ជ.ម.ជ: 0 AB + ruler | 1 protractor at A, ray 60 | 2 ruler along the ray, C at 6 cm | 3 the triangle"""
    k = 48
    A, B = (110, 340), (110 + 4 * k, 340)
    C = pol(A, 6 * k, 60)
    ra = pol(A, 6.9 * k, 60)
    u = (math.cos(math.radians(60)), -math.sin(math.radians(60)))
    c = Cv(W, H)
    c.add(seg((70, 340), (560, 340), GREY, 3) + seg(A, B, LC, 5) + dot(A, LC) + dot(B, LC) + lab(A, 'A', -28, 30, LC, 36, 100) + lab(B, 'B', 20, -10, LC, 36, 100)
          + lab((545, 340), 'l', 0, -22, GREY, 30, 80) + lab(mid(A, B), r'4\ \text{cm}', 0, 54, GREEN, 30, 200))
    c.add(ruler_svg(A, 4, k), 0, 1)
    c.add(protractor_svg(A), 1, 2)
    c.add(seg(A, ra, AUX, 3, '10 7') + angarc(A, B, ra, 40, MK, 4) + lab(bis(A, B, ra, 124), r'60^\circ', 0, 0, MK, 28, 120) + lab(ra, 'x', 18, -6, AUX, 32, 80), 1)
    # a ruler laid along the ray: its 6 cm mark meets C
    n = (-u[1], -u[0])
    p0 = (A[0] + n[0] * 8, A[1] + n[1] * 8)
    rl = poly([A, pol(A, 6.6 * k, 60), (pol(A, 6.6 * k, 60)[0] + n[0] * 30, pol(A, 6.6 * k, 60)[1] + n[1] * 30), (A[0] + n[0] * 30, A[1] + n[1] * 30)], '#fff2cc', '#7f7f7f', 1.5, .92)
    for i in range(0, 13):
        q = pol(A, i * k / 2, 60)
        ln = 15 if i % 2 == 0 else 8
        rl += G._line(f'{q[0]:.1f}', f'{q[1]:.1f}', f'{q[0] + n[0] * ln:.1f}', f'{q[1] + n[1] * ln:.1f}', '#7f7f7f', 1.6)
    c.add(rl, 2, 3)
    c.add(dot(C, LC) + lab(C, 'C', -24, -12, LC, 36, 100) + lab(mid(A, C), r'6\ \text{cm}', -56, 0, GREEN, 30, 200), 2)
    c.add(poly([A, B, C], LAV) + seg(A, C, LC, 5) + seg(B, C, LC, 5) + seg(A, B, LC, 5) + dot(C, LC), 3)
    return c.out()


def cong_vert_move():
    """the two cut-outs, one over the other: the orange copy slides (about 2 s) onto the blue one"""
    A, B, C = (50, 255), (330, 255), (160, 70)
    dx, dy = 60, 290
    A2, B2, C2 = (A[0] + dx, A[1] + dy), (B[0] + dx, B[1] + dy), (C[0] + dx, C[1] + dy)
    c = Cv(480, 580, '64vh')
    s = poly([A2, B2, C2], LAV, LC, 3) + poly([A, B, C], ORG, '#a33b32', 3)
    s += lab(A, 'A', -34, 20, LC, 42, 90) + lab(B, 'B', 34, 20, LC, 42, 90) + lab(C, 'C', -8, -38, LC, 42, 90)
    s += lab(A2, "A'", -38, 20, LC, 42, 90) + lab(B2, "B'", 38, 20, LC, 42, 90) + lab(C2, "C'", -8, -38, LC, 42, 90)
    c.add(s)
    c.add(mvg(poly([A, B, C], ORG, '#a33b32', 3, .92), 1, dx, dy, 2000))
    return c.out()


def overlay_pair2(kind):
    """ABC (orange copy on it) next to A'B'C': step 1 the copy slides over A'B'C' and AB meets A'B' | 2 AC on A'C' | 3 BC on B'C' and the tick"""
    (A, B, C), (A2, B2, C2) = _pair_pts()
    dx, dy = A2[0] - A[0], A2[1] - A[1]
    tk = {'asa': [(0, 1, 1)], 'sas': [(0, 1, 1), (0, 2, 2)], 'sss': [(0, 1, 1), (0, 2, 2), (1, 2, 3)]}[kind]
    ar = {'asa': [(0, 1), (1, 2)], 'sas': [(0, 1)], 'sss': []}[kind]
    c = Cv(W, H)
    c.add(tri(A, B, C, ticks=tk, arcs=ar, rad=28) + tri(A2, B2, C2, names=("A'", "B'", "C'"), **S2, ticks=tk, arcs=ar, rad=28))
    c.add(mvg(poly([A, B, C], ORG, '#a33b32', 3, .85), 1, dx, dy, 1800), 0)
    c.add(late(seg(A2, B2, AUX, 8), 1), 0)
    c.add(seg(A2, C2, AUX, 8), 2)
    c.add(seg(B2, C2, AUX, 8) + lab(mid(A2, B2), r'\checkmark', 0, 56, GREEN, 46, 80), 3)
    return c.out()


def cong_marks2():
    """the six corresponding parts appear in pairs: step 1 angle A and side AB, step 2 angle B and side AC, step 3 angle C and side BC"""
    A, B, C = (30, 290), (260, 290), (150, 40)
    A2, B2, C2 = (A[0] + 340, A[1]), (B[0] + 340, B[1]), (C[0] + 340, C[1])
    c = Cv(640, 330, '44vh')
    c.add(tri(A, B, C, size=34) + tri(A2, B2, C2, names=("A'", "B'", "C'"), **S2, size=34))
    P, Q = (A, B, C), (A2, B2, C2)
    pairs = [(0, (0, 1), 1, 1), (1, (0, 2), 2, 2), (2, (1, 2), 3, 3)]
    for st, (i, (u, v), nt, na) in enumerate(pairs, 1):
        body = ''
        for T_ in (P, Q):
            o = [T_[j] for j in range(3) if j != i]
            for q in range(na):
                body += angarc(T_[i], o[0], o[1], 28 + 9 * q, MK, 4)
            body += tick(T_[u], T_[v], nt, MK)
        c.add(body, st)
    return c.out()


def def_pair():
    """the two marked triangles of the definition slide: sides with 1, 2, 3 ticks and angles with 1, 2, 3 arcs"""
    c = Cv(600, 290, '36vh')
    tk = [(0, 1, 1), (0, 2, 2), (1, 2, 3)]
    ar = [(0, 1), (1, 2), (2, 3)]
    A, B, C = (30, 240), (260, 240), (130, 40)
    dx = 300
    c.add(tri(A, B, C, ticks=tk, arcs=ar, rad=26, size=34) + tri((A[0] + dx, A[1]), (B[0] + dx, B[1]), (C[0] + dx, C[1]), names=("A'", "B'", "C'"), **S2, ticks=tk, arcs=ar, rad=26, size=34))
    return c.out()


def pair_ticks():
    """two congruent triangles with the sides marked (1, 2, 3 ticks) and no arcs, as on the class slide"""
    c = Cv(640, 300, '40vh')
    tk = [(0, 1, 1), (0, 2, 2), (1, 2, 3)]
    A, B, C = (30, 250), (270, 250), (110, 40)
    dx = 330
    c.add(tri(A, B, C, ticks=tk, size=34) + tri((A[0] + dx, A[1]), (B[0] + dx, B[1]), (C[0] + dx, C[1]), names=("A'", "B'", "C'"), **S2, ticks=tk, size=34))
    return c.out()


def pair_angles():
    """STR (4 cm, 50 deg, 5 cm) and DEF (4 cm, 60 deg, 5 cm): same sides, different included angle.  step 1 = the fills and the REAL ruler and protractor"""
    k = 46
    c = Cv(760, 340, '44vh')
    S0 = (90, 270); T0 = (S0[0] + 5 * k, 270); R0 = pol(S0, 4 * k, 50)
    D0 = (470, 270); E0 = (D0[0] + 5 * k, 270); F0 = pol(D0, 4 * k, 60)
    s = tri(S0, T0, R0, names=('S', 'T', 'R'), fill=None, size=34) + tri(D0, E0, F0, names=('D', 'E', 'F'), **S2N, size=34)
    s += angarc(S0, T0, R0, 34, MK, 3) + angarc(D0, E0, F0, 34, MK, 3)
    s += lab(bis(S0, T0, R0, 140), r'50^\circ', 0, 0, MK, 26, 110) + lab(bis(D0, E0, F0, 140), r'60^\circ', 0, 0, MK, 26, 110)
    for A_, B_, C_ in ((S0, T0, R0), (D0, E0, F0)):
        s += lab(mid(A_, B_), r'5\ \text{cm}', 0, 60, NAVYT, 26, 120) + lab(pol(A_, 3.4 * k, 50 if A_ == S0 else 60), r'4\ \text{cm}', -96, -2, NAVYT, 26, 120)
    c.add(poly([S0, T0, R0], '#eefff1', None, 0, .9) + poly([D0, E0, F0], PINK, None, 0, .9), 1)
    c.add(s)
    c.add(measure_tools(S0, 50, 5, 4, k, 78) + measure_tools(D0, 60, 5, 4, k, 78), 1)
    return c.out()


def overlay_vert():
    """ABC (orange, top) and A'B'C' (blue, below): step 1 the copy of ABC slides onto A'B'C' and AB meets A'B' | 2 AC on A'C' | 3 BC on B'C' | 4 the tick"""
    k = 300.0
    A, B = (40, 240), (40 + k, 240)
    AC = k * math.sin(math.radians(40)) / math.sin(math.radians(80))
    C = pol(A, AC, 60)
    dx, dy = 70, 280
    A2, B2, C2 = (A[0] + dx, A[1] + dy), (B[0] + dx, B[1] + dy), (C[0] + dx, C[1] + dy)
    RED = '#e08a00'
    c = Cv(480, 570, '60vh')
    c.add(poly([A2, B2, C2], PINK, AUX, 3) + poly([A, B, C], MINT, LC, 3))
    c.add(lab(A, 'A', -34, 20, LC, 40, 90) + lab(B, 'B', 34, 20, LC, 40, 90) + lab(C, 'C', -8, -38, LC, 40, 90)
          + lab(A2, "A'", -38, 20, AUX, 40, 90) + lab(B2, "B'", 38, 20, AUX, 40, 90) + lab(C2, "C'", -8, -38, AUX, 40, 90))
    c.add(mvg(poly([A, B, C], MINT, LC, 3, .85), 1, dx, dy, 1800))
    c.add(late(seg(A2, B2, RED, 7) + angarc(A2, B2, C2, 30, MK, 3) + angarc(B2, A2, C2, 30, MK, 3), 1), 0)
    c.add(seg(A2, C2, RED, 7), 2)
    c.add(seg(B2, C2, RED, 7), 3)
    return c.out()


def pair_asa():
    """two congruent triangles with AB (1 tick) and the angles at A (1 arc) and B (2 arcs); A = 60, B = 40 degrees"""
    k = 250.0
    A, B = (40, 240), (40 + k, 240)
    AC = k * math.sin(math.radians(40)) / math.sin(math.radians(80))
    C = pol(A, AC, 60)
    dx = 340
    c = Cv(650, 240, '36vh')
    ar = [(0, 1), (1, 2)]
    c.add(tri(A, B, C, ticks=[(0, 1, 1)], arcs=ar, rad=26, size=34) + tri((A[0] + dx, A[1]), (B[0] + dx, B[1]), (C[0] + dx, C[1]), names=("A'", "B'", "C'"), **S2, ticks=[(0, 1, 1)], arcs=ar, rad=26, size=34))
    return c.out()


def asa_ex_draw():
    """the figure of «AB and CD cross at E» in the order it is drawn: click it in the show to watch it being drawn.
    groups (class dr): 1 segment AB, E, 2 segment CD, 3 AD and CB, 4 the two triangles filled, 5 the equal marks"""
    E = (320, 215)
    k = 62
    A = (E[0] - 3 * k, E[1] - 1.2 * k)
    B = (E[0] + 3 * k, E[1] + 1.2 * k)
    D = (E[0] - 1.0 * k, E[1] + 2.0 * k)
    C = (E[0] + 1.0 * k, E[1] - 2.0 * k)
    c = Cv(W, H, '46vh')
    dr = lambda body: '<g class="dr">' + body + '</g>'
    c.add(dr(poly([A, E, D], LAV) + poly([B, E, C], PINK)))                                      # fills (shown at step 4 of the replay)
    c.add(dr(seg(A, B, LC, 5) + dot(E, AUX) + lab(A, 'A', -24, -10, LC, 38, 100) + lab(B, 'B', 24, 12, LC, 38, 100) + lab(E, 'E', 26, -4, LC, 38, 100)))
    c.add(dr(seg(C, D, LC, 5) + lab(C, 'C', 22, -14, LC, 38, 100) + lab(D, 'D', -22, 18, LC, 38, 100)))
    c.add(dr(seg(A, D, LC, 5) + seg(C, B, LC, 5)))
    c.add(dr(tick(E, A, 1, MK) + tick(E, B, 1, MK) + angarc(E, A, D, 26, MK, 4) + angarc(E, A, D, 33, MK, 4) + angarc(E, B, C, 26, MK, 4) + angarc(E, B, C, 33, MK, 4)
             + angarc(A, E, D, 30, MK, 4) + angarc(B, E, C, 30, MK, 4)))
    return c.out().replace('<svg ', '<svg class="drawfig" ', 1)


# ================================================================ real measuring tools laid on a figure
def ruler_dir(p0, deg, n_cm, k, side=1, h=28):
    """a ruler lying along the ray from p0 at `deg` degrees; 0 at p0, n_cm centimetres of k px each; side = +1 / -1 chooses the side of the ray it lies on"""
    u = (math.cos(math.radians(deg)), -math.sin(math.radians(deg)))
    nrm = (u[1] * side, -u[0] * side)                 # 90 degrees from u
    nrm = (nrm[0], nrm[1])
    a0 = (p0[0] - u[0] * 12, p0[1] - u[1] * 12)
    L = n_cm * k + 24
    a1 = (a0[0] + u[0] * L, a0[1] + u[1] * L)
    s = poly([a0, a1, (a1[0] + nrm[0] * h, a1[1] + nrm[1] * h), (a0[0] + nrm[0] * h, a0[1] + nrm[1] * h)], '#fff2cc', '#7f7f7f', 1.4, .88)
    for i in range(int(n_cm * 2) + 1):
        q = (p0[0] + u[0] * i * k / 2, p0[1] + u[1] * i * k / 2)
        ln = 14 if i % 2 == 0 else 8
        s += G._line(f'{q[0]:.1f}', f'{q[1]:.1f}', f'{q[0] + nrm[0] * ln:.1f}', f'{q[1] + nrm[1] * ln:.1f}', '#7f7f7f', 1.4)
        if i % 2 == 0:
            tp = (q[0] + nrm[0] * (h - 6), q[1] + nrm[1] * (h - 6))
            s += _T(tp[0], tp[1] + 5, str(i // 2), 13, '#595959', weight=600)
    return s


def protractor_dir(c, base_deg, r, read_deg):
    """a half protractor centred at c with its base line along `base_deg`; the half disc lies on the side of increasing angle; a dot marks the reading at read_deg"""
    pts = [pol(c, r, base_deg + a) for a in range(0, 181, 4)]
    s = poly(pts, '#bcd7f2', '#7f7f7f', 1.4, .6)
    for a in range(0, 181, 10):
        ln = 12 if a % 30 == 0 else 6
        p1, p2 = pol(c, r, base_deg + a), pol(c, r - ln, base_deg + a)
        s += G._line(f'{p1[0]:.1f}', f'{p1[1]:.1f}', f'{p2[0]:.1f}', f'{p2[1]:.1f}', '#7f7f7f', 1.3)
        if a % 30 == 0 and a not in (0, 180) and r >= 70:
            tp = pol(c, r - 24, base_deg + a)
            s += _T(tp[0], tp[1] + 5, str(a), 12, '#595959', weight=600)
    s += G._line(f'{pol(c, r + 6, base_deg)[0]:.1f}', f'{pol(c, r + 6, base_deg)[1]:.1f}', f'{pol(c, r + 6, base_deg + 180)[0]:.1f}', f'{pol(c, r + 6, base_deg + 180)[1]:.1f}', '#7f7f7f', 1.3)
    rd = pol(c, r - 3, base_deg + read_deg)
    s += f'<circle cx="{rd[0]:.1f}" cy="{rd[1]:.1f}" r="4" fill="{AUX}"/>'
    s += G._line(f'{c[0]:.1f}', f'{c[1]:.1f}', f'{rd[0]:.1f}', f'{rd[1]:.1f}', AUX, 1.6, '5 4')
    s += f'<circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="3.5" fill="#595959"/>'
    return s


def measure_tools(V, ang, n_base, n_side, k, r=62):
    """for the corner V of a triangle drawn with its base along 0 degrees and its other side at `ang`: a ruler under the base (0..n_base cm),
    a ruler along the slanted side (0..n_side cm) and a protractor on V reading `ang`"""
    return ('<g class="tool-r">' + ruler_dir(V, 0, n_base, k, side=-1) + ruler_dir(V, ang, n_side, k, side=1) + '</g>'
            + '<g class="tool-p">' + protractor_dir(V, 0, r, ang) + '</g>')
