# Pictures for the hand-designed Grade 7 Lesson 3 deck (relative integers). Same helpers and colours as Lessons 1-2.
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lesson1'))
from lib import *

POS, NEG = BLUE, RED


def sg(v):
    """a number as it is written in the book: a real minus sign for negatives"""
    return str(v).replace('-', '−')


def sgn(v):
    return ('+' + str(v)) if v > 0 else sg(v)


class NL:
    """A number line drawn in an SVG of width w. X(v) is the x position of value v."""

    def __init__(s, lo, hi, w=1000, y=110, left=80, right=80):
        s.lo, s.hi, s.w, s.y, s.x0, s.x1 = lo, hi, w, y, left, w - right

    def X(s, v):
        return s.x0 + (v - s.lo) / (s.hi - s.lo) * (s.x1 - s.x0)

    def base(s, every=1, numbers=True, size=28):
        y = s.y
        b = line(s.x0 - 34, y, s.x1 + 34, y, NAVY, 5)
        b += f'<polygon points="{s.x1+52},{y} {s.x1+30},{y-11} {s.x1+30},{y+11}" fill="{NAVY}"/>'
        for v in range(s.lo, s.hi + 1):
            b += line(s.X(v), y - 12, s.X(v), y + 12, NAVY, 3)
            if numbers and (v - s.lo) % every == 0:
                b += T(s.X(v), y + 50, sg(v), size, NEG if v < 0 else POS if v > 0 else NAVY)
        return b

    def pt(s, v, col, r=15, label=None, dy=-38, size=30):
        b = circ(s.X(v), s.y, r, col, '#fff', 3)
        if label:
            b += T(s.X(v), s.y + dy, label, size, col)
        return b

    def hop(s, a, b_, col, text='', h=64, below=False, size=26, w=5):
        """an arrow that jumps from a to b_ above (or below) the line"""
        xa, xb, y = s.X(a), s.X(b_), s.y
        sgn_ = 1 if below else -1
        ya = y + sgn_ * 6
        cx, cy = (xa + xb) / 2, y + sgn_ * 2 * h
        d = f'M {xa} {ya} Q {cx} {cy} {xb} {ya}'
        ang = math.atan2(ya - cy, xb - cx)                      # direction at the end of the curve
        hx, hy = xb - 16 * math.cos(ang), ya - 16 * math.sin(ang)
        px, py = -math.sin(ang) * 9, math.cos(ang) * 9
        out = f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>'
        out += f'<polygon points="{xb},{ya} {hx+px},{hy+py} {hx-px},{hy-py}" fill="{col}"/>'
        if text:
            out += T(cx, y + sgn_ * (h + 14) + (14 if below else -4), text, size, col)
        return out

    def brace(s, a, b_, col, text, up=True, size=26):
        """a straight dimension bar with end ticks and its label (a distance)"""
        xa, xb, y = s.X(a), s.X(b_), s.y + (-74 if up else 96)
        out = line(xa, y, xb, y, col, 5) + line(xa, y - 10, xa, y + 10, col, 5) + line(xb, y - 10, xb, y + 10, col, 5)
        out += T((xa + xb) / 2, y + (-16 if up else 36), text, size, col)
        return out


# ------------------------------------------------------------------ 1. notation
def thermometer():
    top, bot = 60, 400
    Y = lambda t: top + (60 - t) / 120 * (bot - top)
    b = f'<rect x="190" y="{top-30}" width="780" height="{Y(0)-top+30}" fill="#fff1e6"/><rect x="190" y="{Y(0)}" width="780" height="{bot-Y(0)+30}" fill="#e7f1ff"/>'
    b += T(950, Y(20) + 10, 'លើសូន្យ', 32, ORANGE, 'end') + T(950, Y(-20) + 10, 'ក្រោមសូន្យ', 32, BLUE, 'end')
    b += f'<rect x="107" y="{top-24}" width="46" height="{bot-top+48}" rx="23" fill="#fff" stroke="{NAVY}" stroke-width="4"/>'
    b += f'<circle cx="130" cy="{bot+54}" r="40" fill="{BLUE}" stroke="{NAVY}" stroke-width="4"/>'
    b += rvg(0, f'<rect x="122" y="{Y(-60)}" width="16" height="{bot+54-Y(-60)}" fill="{BLUE}"/>', until=3)
    b += rvg(3, f'<rect x="122" y="{Y(40)}" width="16" height="{bot+54-Y(40)}" fill="{RED}"/>')
    for t in range(-60, 61, 20):
        b += line(190, Y(t), 214, Y(t), NAVY, 3) + T(228, Y(t) + 10, sg(t), 28, NEG if t < 0 else POS if t > 0 else NAVY, 'start')
    b += line(190, Y(0), 970, Y(0), NAVY, 3, '10 8')
    b += rvg(1, line(330, Y(-60), 520, Y(-60), NEG, 4) + T(540, Y(-60) + 14, '−60°C', 48, NEG, 'start'))
    b += rvg(2, T(540, Y(-60) + 54, '៦០ អង្សាក្រោមសូន្យ', 28, NAVY, 'start'))
    b += rvg(3, line(330, Y(40), 520, Y(40), POS, 4) + T(540, Y(40) + 14, '+40°C', 48, POS, 'start') + T(540, Y(40) + 54, '៤០ អង្សាលើសូន្យ', 28, NAVY, 'start'))
    return svg(1000, 520, b, '56vh')




def number_line_concept():
    nl = NL(-5, 5, y=120)
    b = rect(nl.X(-5), 112, nl.X(0) - nl.X(-5), 16, '#ffd6d6', 8) + rect(nl.X(0), 112, nl.X(5) - nl.X(0), 16, '#d3e6ff', 8)
    b += nl.base() + nl.pt(0, NAVY, 17, 'គល់ 0', -40, 28)
    b += rvg(1, T(nl.X(-2.5), 44, 'ចំនួនអវិជ្ជមាន', 30, NEG) + T(nl.X(2.5), 44, 'ចំនួនវិជ្ជមាន', 30, POS))
    b += rvg(2, arrow(nl.X(1), 196, nl.X(4.6), 196, GREEN, 5) + T(nl.X(2.8), 236, 'ទិសដៅវិជ្ជមាន (ទៅខាងស្តាំ)', 26, GREEN))
    b += rvg(3, arrow(nl.X(-1), 196, nl.X(-4.6), 196, ORANGE, 5) + T(nl.X(-2.8), 236, 'ទៅខាងឆ្វេង', 26, ORANGE))
    return svg(1000, 260, b, '40vh')


# ------------------------------------------------------------------ 2. absolute value and order
def abs_distance():
    nl = NL(-3, 3, y=150)
    b = nl.base(size=32) + nl.brace(-3, 0, NEG, 'ចម្ងាយ 3 ឯកតា') + nl.brace(0, 3, POS, 'ចម្ងាយ 3 ឯកតា')
    b += nl.pt(-3, NEG) + nl.pt(3, POS) + nl.pt(0, NAVY)
    b += rvg(1, T(nl.X(-1.5), 250, '|−3| = 3', 40, NEG) + T(nl.X(1.5), 250, '|3| = 3', 40, POS))
    return svg(1000, 290, b, '46vh')


def order_line():
    nl = NL(-4, 4, y=140)
    b = nl.base(size=32) + nl.pt(2, POS, 15) + nl.pt(4, POS, 15) + nl.pt(-4, NEG, 15) + nl.pt(-2, NEG, 15)
    b += rvg(1, nl.hop(2, 4, GREEN, '2 < 4', 58, size=30))
    b += rvg(2, nl.hop(-4, -2, GREEN, '−4 < −2', 58, size=30))
    b += rvg(3, arrow(nl.X(-3.4), 240, nl.X(3.4), 240, NAVY, 5) + T(500, 284, 'ចំនួនកាន់តែទៅខាងស្តាំ កាន់តែធំ', 28, NAVY))
    return svg(1000, 300, b, '46vh')


# ------------------------------------------------------------------ 3. opposite numbers and plotting points
def opposite_line():
    nl = NL(-3, 3, y=250)
    b = line(nl.X(0), 24, nl.X(0), 320, GREY, 3, '8 8') + nl.base(size=34)
    for k, v in enumerate((1, 2, 3)):
        col = [TEAL, ORANGE, PURPLE][k]
        b += rvg(k + 1, nl.hop(-v, v, col, '', 40 + v * 34, w=5))
        b += rvg(k + 1, T(500, 365, f'{sg(-v)}  ជាចំនួនផ្ទុយនៃ  {v}', 36, col), until=k + 2)       # one caption at a time, under the line
    b += nl.pt(-1, NEG) + nl.pt(1, POS) + nl.pt(-2, NEG) + nl.pt(2, POS) + nl.pt(-3, NEG) + nl.pt(3, POS) + nl.pt(0, NAVY, 14)
    return svg(1000, 390, b, '50vh')




def plot_points(points, lo, hi, labelmap=None, with_axis_name=True, steps=True):
    """points: {'A': 4, 'B': -3}; the points appear one by one"""
    nl = NL(lo, hi, y=130)
    b = nl.base(size=32)
    cols = {'A': ORANGE, 'B': PURPLE, 'C': GREEN, 'D': RED}
    for k, (name, v) in enumerate(points.items()):
        g = nl.pt(v, cols.get(name, BLUE), 16) + T(nl.X(v), 66, f'{name}({sg(v)})', 36, cols.get(name, BLUE))
        b += rvg(k + 1, g) if steps else g
    b += T(nl.x0 - 50, 190, "x'", 32, GREY) + T(nl.x1 + 50, 190, 'x', 32, GREY)
    return svg(1000, 230, b, '40vh')


# ------------------------------------------------------------------ 4. addition and subtraction with marbles
def marble(x, y, sign, r=23, fade=False, dashed=False):
    col = POS if sign > 0 else NEG
    op = ' opacity=".28"' if fade else ''
    st = f' stroke="{col}" stroke-width="3" stroke-dasharray="5 4"' if dashed else ''
    fill = '#fff' if dashed else col
    sym = col if dashed else '#fff'
    return f'<g{op}>' + f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"{st}/>' + T(x, y + 10, '+' if sign > 0 else '−', 32, sym, weight=800) + '</g>'


def row(n, sign, x, y, gap=58, **k):
    return ''.join(marble(x + i * gap, y, sign, **k) for i in range(n)), x + n * gap


def marbles_add(a, b_):
    """a + b_ with both groups of the same sign: they simply join"""
    sa = 1 if a > 0 else -1
    na, nb = abs(a), abs(b_)
    sb = 1 if b_ > 0 else -1
    g1, e1 = row(na, sa, 60, 60)
    g2, e2 = row(nb, sb, e1 + 70, 60)
    out = g1 + T(e1 + 22, 72, '+', 44, NAVY) + g2
    tot, _ = row(na + nb, sa, 60, 160)
    out += rvg(1, tot + T(60 + (na + nb) * 58 + 10, 172, f'= {na+nb} គ្រាប់', 30, NAVY, 'start'))
    return out


def addition_same(a, b_):
    """slide figure: marbles above, number line below, for a + b_ (same sign)"""
    s = a + b_
    lo, hi = (0, s) if s > 0 else (s, 0)
    nl = NL(lo, hi, y=330, w=820, left=110, right=110)
    body = marbles_add(a, b_)
    body += nl.base(size=30)
    col1, col2 = (POS, GREEN) if a > 0 else (NEG, ORANGE)
    body += rvg(2, nl.hop(0, a, col1, sgn(a), 60, size=30) + nl.pt(0, NAVY, 13))
    body += rvg(3, nl.hop(a, s, col2, sgn(b_), 60, size=30) + nl.pt(s, col2, 15))
    return svg(820, 410, body, '50vh')


def zero_pairs_add(np_, nn):
    """np_ plus marbles + nn minus marbles: the pairs +/− cancel (zero pairs)"""
    pairs = min(np_, nn)
    left, extra = np_ - pairs, nn - pairs
    x = 60
    b, _ = row(left, 1, x, 70)
    x2 = x + left * 58 + (14 if left else 0)
    for i in range(pairs):
        b += marble(x2 + i * 130, 70, 1) + marble(x2 + i * 130 + 58, 70, -1)
    ring = ''.join(f'<rect x="{x2 + i*130 - 34}" y="28" width="126" height="84" rx="42" fill="none" stroke="{GOLD}" stroke-width="4" stroke-dasharray="9 6"/>' for i in range(pairs))
    b += rvg(1, ring + T(x2 + pairs * 130 / 2 - 20, 150, f'គូសូន្យ {pairs} គូ', 30, GOLD))
    if extra:
        eg, _ = row(extra, -1, x2 + pairs * 130, 70)
        b += eg
    res, sign = (left, 1) if left else (extra, -1)
    rg, _ = row(res, sign, 230, 240)
    b += rvg(2, T(60, 252, 'សល់ ៖', 30, GREY, 'start') + rg + T(230 + res * 58 + 10, 252, f'= {sgn(res if sign > 0 else -res)}', 40, POS if sign > 0 else NEG, 'start'))
    return svg(820, 300, b, '42vh')




def subtract_box(total, take, sign, y0=60):
    """a box of `total` marbles with `take` of them pulled out"""
    w = total * 58 + 30
    keep = total - take
    out = f'<rect x="40" y="{y0-44}" width="{w}" height="88" rx="16" fill="none" stroke="{NAVY}" stroke-width="4"/>'
    for i in range(keep):
        out += marble(70 + i * 58, y0, sign)
    col = POS if sign > 0 else NEG
    for i in range(keep, total):
        out += rvg(0, marble(70 + i * 58, y0, sign), until=1)
        out += rvg(1, f'<circle cx="{70 + i*58}" cy="{y0}" r="23" fill="none" stroke="{col}" stroke-width="2" stroke-dasharray="4 5" opacity=".5"/>')
        out += rvg(1, marble(40 + w + 130 + (i - keep) * 58, y0, sign))
    out += rvg(1, arrow(40 + w + 6, y0, 40 + w + 100, y0, GREY, 4) + T(40 + w + 130, y0 + 62, f'យកចេញ {take} គ្រាប់', 26, GREY, 'start'))
    return out




def subtract_two():
    b = subtract_box(4, 2, 1, 70) + rvg(2, T(1180, 86, '4 − 2 = 2', 42, POS, 'end'))
    b += subtract_box(8, 2, -1, 230) + rvg(2, T(1180, 246, '(−8) − (−2) = −6', 42, NEG, 'end'))
    return svg(1200, 320, b, '46vh')




def subtract_zero_pairs():
    """6 − (−3): 6 plus marbles, add 3 zero pairs, take the 3 minus marbles out, 9 plus marbles remain"""
    g6, _ = row(6, 1, 60, 60)
    b = g6
    x = 60 + 6 * 58 + 20
    pairs = ''.join(marble(x + i * 130, 60, 1, dashed=True) + marble(x + i * 130 + 58, 60, -1) for i in range(3))
    ring = ''.join(f'<rect x="{x + i*130 - 34}" y="22" width="126" height="76" rx="38" fill="none" stroke="{GOLD}" stroke-width="4" stroke-dasharray="9 6"/>' for i in range(3))
    b += rvg(1, pairs + ring + T(x + 190, 148, 'បន្ថែមគូសូន្យ 3 គូ', 28, GOLD))
    cross = ''.join(f'<line x1="{x + i*130 + 58 - 22}" y1="38" x2="{x + i*130 + 58 + 22}" y2="82" stroke="{GREY}" stroke-width="5"/>' for i in range(3))
    b += rvg(2, cross + T(x + 190, 196, 'យកឃ្លីដក 3 គ្រាប់ចេញ', 28, GREY))
    r9, _ = row(9, 1, 60, 280)
    b += rvg(3, r9 + T(60 + 9 * 58 + 20, 292, '= 9', 44, POS, 'start'))
    return svg(1100, 340, b, '42vh')


# ------------------------------------------------------------------ 5. multiplication / division sign rules
def sign_grid(op='×'):
    LP, LN = '#8ec5ff', '#ff9b9b'                       # light tints: this picture sits on the dark «key» panel
    b = T(130, 70, op, 52, '#fff') + T(330, 70, '( + )', 44, LP) + T(540, 70, '( − )', 44, LN)
    b += T(130, 178, '( + )', 44, LP) + T(130, 300, '( − )', 44, LN)
    cells = [(330, 178, '+', GREEN, 1), (540, 178, '−', RED, 2), (330, 300, '−', RED, 3), (540, 300, '+', GREEN, 4)]
    for x, y, sym, col, st in cells:
        b += rvg(st, rect(x - 92, y - 58, 184, 108, col, 20) + T(x, y + 22, sym, 76, '#fff', weight=800))
    b += rvg(5, rect(700, 118, 290, 76, '#e6f7ec', 14, GREEN, 3) + T(845, 168, 'សញ្ញាដូចគ្នា → +', 32, '#1b6b2f')
             + rect(700, 240, 290, 76, '#ffe9e9', 14, RED, 3) + T(845, 290, 'សញ្ញាផ្ទុយគ្នា → −', 32, '#a61e1e'))
    return svg(1000, 350, b, '48vh')


def pattern_mult():
    rows = [(3, -9), (2, -6), (1, -3), (0, 0), (-1, 3), (-2, 6)]
    b = ''
    for i, (k, v) in enumerate(rows):
        y = 40 + i * 62
        col = NEG if v < 0 else NAVY if v == 0 else POS
        line_ = f'(−3) × {sg(k)} = {sg(v)}'
        g = T(300, y + 14, line_, 38, col, 'middle')
        if i:
            g += T(500, y - 14, '+3', 30, GREEN, 'start') + f'<polygon points="478,{y-34} 490,{y-12} 466,{y-12}" fill="{GREEN}"/>'
        b += rvg(i + 1, g)
    b += rvg(7, rect(60, 40 + 4 * 62 - 28, 480, 124, 'none', 12, GOLD, 5))
    return svg(760, 440, b, '50vh')


# ------------------------------------------------------------------ 6. order of operations
def order_ladder():
    b = ''
    steps = [(RED, '១', 'វង់ក្រចក  ( )  [ ]', 'ធ្វើក្នុងវង់ក្រចកមុន'), (BLUE, '២', 'គុណ  ×   ចែក  ÷', 'ពីឆ្វេងទៅស្តាំ'), (GREEN, '៣', 'បូក  +   ដក  −', 'ពីឆ្វេងទៅស្តាំ')]
    for i, (col, n, t, sub) in enumerate(steps):
        y = 20 + i * 96
        b += rvg(i + 1, rect(30 + i * 40, y, 700 - i * 40, 78, col, 16) + T(80 + i * 40, y + 52, n, 44, '#fff', 'middle') + T(130 + i * 40, y + 36, t, 32, '#fff', 'start') + T(130 + i * 40, y + 66, sub, 22, '#fff', 'start', 500))
    return svg(760, 320, b, '40vh')


# ------------------------------------------------------------------ 1. profit and loss of one week (the book's table, drawn as bars)
def week_chart():
    days = [('ចន្ទ', -4), ('អង្គារ', 2), ('ពុធ', 3), ('ព្រហស្បតិ៍', -2), ('សុក្រ', -3), ('សៅរ៍', 5), ('អាទិត្យ', 7)]
    y0, unit, x0, gap, bw = 200, 22, 70, 130, 84
    b = line(30, y0, 970, y0, NAVY, 4)
    for k, (name, v) in enumerate(days):
        x = x0 + k * gap
        col = GREEN if v > 0 else RED
        top = y0 - v * unit if v > 0 else y0
        h = abs(v) * unit
        b += rect(x, top, bw, h, col, 8)
        b += T(x + bw / 2, (y0 - v * unit - 12) if v > 0 else (y0 - v * unit + 38), sgn(v), 36, col)
        b += T(x + bw / 2, 372, name, 26, NAVY)
        if name in ('ព្រហស្បតិ៍', 'សៅរ៍'):
            b += rvg(1, f'<rect x="{x-14}" y="30" width="{bw+28}" height="360" rx="18" fill="none" stroke="{GOLD}" stroke-width="5" stroke-dasharray="10 7"/>')
    b += rvg(2, T(x0 + 3 * gap + bw / 2, 436, 'ខាត 2 ម៉ឺនរៀល', 30, RED) + T(x0 + 5 * gap + bw / 2, 436, 'ចំណេញ 5 ម៉ឺនរៀល', 30, GREEN))
    b += T(30, 60, 'ម៉ឺនរៀល', 24, GREY, 'start')
    return svg(1000, 460, b, '50vh')
