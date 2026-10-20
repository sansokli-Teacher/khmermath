# Part 8 pictures (squares and cubes) drawn to IMAGE_STYLE_GUIDE.md:
# flat fills, thin dark outlines, no background, real dimension arrows, variables in italic serif, numbers/units in upright serif.
import math
from lib import esc, svg

INK = '#111827'          # outlines and numbers
RED = '#c92a2a'          # unknowns
SQ_FILL = '#cfe3f5'
TOP, LEFT, RIGHT = '#bfe0ff', '#7fb8ec', '#4f8fd0'        # three flat tones of the cube faces
UP = "'Times New Roman',serif"
IT = "'Mathcad UniMath Italic','Mathcad UniMath','Times New Roman',serif"


def txt(x, y, parts, size=28, fill=INK, anchor='middle', bold=False):
    """parts = [(text, kind)] with kind 'v' variable (italic), 'n' number / unit (upright), 'sup' superscript."""
    out = ''
    for t, k in parts:
        if k == 'v':
            out += f'<tspan font-family="{IT}" font-style="italic">{esc(t)}</tspan>'
        elif k == 'sup':
            out += f'<tspan font-family="{UP}" font-size="{int(size * .62)}" dy="{-int(size * .38)}">{esc(t)}</tspan><tspan dy="{int(size * .38)}"> </tspan>'
        else:
            out += f'<tspan font-family="{UP}" font-style="normal">{esc(t)}</tspan>'
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{700 if bold else 400}">{out}</text>'


def _arrow_head(x, y, ang, c=INK, s=10):
    a, b = ang + math.radians(150), ang - math.radians(150)
    return f'<polygon points="{x:.1f},{y:.1f} {x + s * math.cos(a):.1f},{y + s * math.sin(a):.1f} {x + s * math.cos(b):.1f},{y + s * math.sin(b):.1f}" fill="{c}"/>'


def dim_line(x1, y1, x2, y2, c=INK, w=2):
    """a dimension line: thin line with an arrow head at both ends and short ticks across the ends"""
    ang = math.atan2(y2 - y1, x2 - x1)
    nx, ny = -math.sin(ang) * 7, math.cos(ang) * 7
    body = f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"/>'
    body += _arrow_head(x1, y1, ang + math.pi, c) + _arrow_head(x2, y2, ang, c)
    body += f'<line x1="{x1 - nx:.1f}" y1="{y1 - ny:.1f}" x2="{x1 + nx:.1f}" y2="{y1 + ny:.1f}" stroke="{c}" stroke-width="{w}"/>'
    body += f'<line x1="{x2 - nx:.1f}" y1="{y2 - ny:.1f}" x2="{x2 + nx:.1f}" y2="{y2 + ny:.1f}" stroke="{c}" stroke-width="{w}"/>'
    return body


def _sq(x, y, s, n=None, fill=SQ_FILL):
    """a square, optionally cut into n x n cells; crisp corners and thin outlines"""
    b = f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="{fill}" stroke="{INK}" stroke-width="3"/>'
    if n:
        c = s / n
        for k in range(1, n):
            b += f'<line x1="{x + k * c:.1f}" y1="{y}" x2="{x + k * c:.1f}" y2="{y + s}" stroke="{INK}" stroke-width="1.5"/>'
            b += f'<line x1="{x}" y1="{y + k * c:.1f}" x2="{x + s}" y2="{y + k * c:.1f}" stroke="{INK}" stroke-width="1.5"/>'
    return b


def _poly(pts, fill, w=1.3):
    return f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="{fill}" stroke="{INK}" stroke-width="{w}" stroke-linejoin="round"/>'


class Iso:
    """isometric cube of n x n x n small cubes; i runs down-right, j down-left, k up. Every point is inside the frame."""
    def __init__(self, n, size, ox=0, oy=0):
        c, s = math.cos(math.radians(30)), math.sin(math.radians(30))
        self.n, self.size, self.c, self.s = n, size, c, s
        self.ux, self.uy, self.vx, self.vy = size * c, size * s, -size * c, size * s
        self.ox = ox + n * size * c
        self.oy = oy + n * size
        self.W, self.H = 2 * n * size * c, 2 * n * size            # exact bounding box of the drawing

    def P(self, i, j, k):
        return (self.ox + i * self.ux + j * self.vx, self.oy + i * self.uy + j * self.vy - k * self.size)

    def body(self):
        n, P, b = self.n, self.P, ''
        for i in range(n):
            for j in range(n):
                b += _poly([P(i, j, n), P(i + 1, j, n), P(i + 1, j + 1, n), P(i, j + 1, n)], TOP)
        for i in range(n):
            for k in range(n):
                b += _poly([P(i, n, k), P(i + 1, n, k), P(i + 1, n, k + 1), P(i, n, k + 1)], LEFT)
        for j in range(n):
            for k in range(n):
                b += _poly([P(n, j, k), P(n, j + 1, k), P(n, j + 1, k + 1), P(n, j, k + 1)], RIGHT)
        top, front_top = [P(0, 0, n), P(n, 0, n), P(n, n, n), P(0, n, n)], None
        hexa = [P(0, 0, n), P(n, 0, n), P(n, 0, 0), P(n, n, 0), P(0, n, 0), P(0, n, n)]
        b += f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in hexa)}" fill="none" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
        b += f'<polyline points="{P(0, n, n)[0]:.1f},{P(0, n, n)[1]:.1f} {P(n, n, n)[0]:.1f},{P(n, n, n)[1]:.1f} {P(n, 0, n)[0]:.1f},{P(n, 0, n)[1]:.1f}" fill="none" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
        b += f'<line x1="{P(n, n, n)[0]:.1f}" y1="{P(n, n, n)[1]:.1f}" x2="{P(n, n, 0)[0]:.1f}" y2="{P(n, n, 0)[1]:.1f}" stroke="{INK}" stroke-width="3"/>'
        return b

    def edge_dim(self, p0, p1, parts, off=30, size=26, color=INK):
        """dimension line parallel to the edge p0-p1, pushed `off` px away from the cube (away from its centre), with its label"""
        (x0, y0), (x1, y1) = p0, p1
        cx, cy = self.ox, self.oy - self.n * self.size / 2          # the cube's centre
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        dx, dy = x1 - x0, y1 - y0
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / ln, dx / ln
        if (mx - cx) * nx + (my - cy) * ny < 0:
            nx, ny = -nx, -ny
        a = (x0 + nx * off, y0 + ny * off)
        b = (x1 + nx * off, y1 + ny * off)
        out = dim_line(a[0], a[1], b[0], b[1], color)
        lx, ly = (a[0] + b[0]) / 2 + nx * (size * .9), (a[1] + b[1]) / 2 + ny * (size * .9) + size * .35
        anchor = 'start' if nx > .5 else ('end' if nx < -.5 else 'middle')
        return out + txt(lx, ly, parts, size, color, anchor)


def num(t):
    return [(t, 'n')]


def cube_fig(n, size, edge_label, maxh='32vh'):
    """a cube with its three visible edge sizes written on dimension lines (e.g. [('3','n'),(' dm','n')])"""
    m = 120
    iso = Iso(n, size, ox=m, oy=30)
    L, B, R = iso.P(0, n, 0), iso.P(n, n, 0), iso.P(n, 0, 0)
    body = iso.body()
    body += iso.edge_dim(L, B, edge_label, size=32) + iso.edge_dim(B, R, edge_label, size=32)
    body += iso.edge_dim(R, iso.P(n, 0, n), edge_label, off=34, size=32)
    W, H = int(iso.W + 2 * m), int(iso.H + 30 + 85)
    return svg(W, H, body, maxh)


def square_fig(n, label, cell=44, maxh='34vh'):
    """an n x n square cut into cells, its side written on two dimension lines"""
    s = n * cell
    X, Y = 70, 30
    b = _sq(X, Y, s, n)
    b += dim_line(X, Y + s + 28, X + s, Y + s + 28) + txt(X + s / 2, Y + s + 28 + 34, label, 28)
    b += dim_line(X + s + 28, Y, X + s + 28, Y + s) + txt(X + s + 28 + 16, Y + s / 2 + 10, label, 28, anchor='start')
    return svg(int(X + s + 28 + 130), int(Y + s + 28 + 50), b, maxh)


def square_area_fig(side_label, area_parts, maxh='34vh'):
    """a plain square with its area inside and its side on two dimension lines"""
    s, X, Y = 220, 70, 30
    b = _sq(X, Y, s)
    b += txt(X + s / 2, Y + s / 2 + 10, area_parts, 32, anchor='middle')
    b += dim_line(X, Y + s + 28, X + s, Y + s + 28) + txt(X + s / 2, Y + s + 28 + 34, side_label, 28)
    b += dim_line(X + s + 28, Y, X + s + 28, Y + s) + txt(X + s + 28 + 16, Y + s / 2 + 10, side_label, 28, anchor='start')
    return svg(int(X + s + 28 + 130), int(Y + s + 28 + 50), b, maxh)


def intro_fig(maxh='40vh'):
    """a square of area 100 cm2 and a cube of volume 27 dm3: both sides unknown (a = ?)"""
    q = [('a', 'v'), (' = ?', 'n')]
    s, X, Y = 200, 60, 40
    b = _sq(X, Y, s)
    b += txt(X + s / 2, Y + s / 2 + 10, [('A', 'v'), (' = 100 cm', 'n'), ('2', 'sup')], 30)
    b += dim_line(X, Y + s + 28, X + s, Y + s + 28, RED) + txt(X + s / 2, Y + s + 28 + 34, q, 28, RED)
    b += dim_line(X + s + 28, Y, X + s + 28, Y + s, RED) + txt(X + s + 28 + 14, Y + s / 2 + 10, q, 28, RED, 'start')
    iso = Iso(3, 46, ox=520, oy=Y - 10)
    b += iso.body() + iso.edge_dim(iso.P(0, 3, 0), iso.P(3, 3, 0), q, color=RED)
    b += txt(iso.ox, (Y - 10) + iso.H + 66, [('V', 'v'), (' = 27 dm', 'n'), ('3', 'sup')], 30)
    return svg(760, int((Y - 10) + iso.H + 90), b, maxh)
