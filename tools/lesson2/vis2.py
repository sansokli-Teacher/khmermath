# Pictures for the hand-designed Grade 7 Lesson 2 deck (divisibility, divisors and multiples, primes, factor trees, GCD, LCM).
import math, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lesson1'))
from lib import *


# ---------------------------------------------------------------- digit boxes
def digits(num, hi=(), color=GOLD, size=86, gap=12, base=BLUE, steps=None, maxh='18vh', fg_hi='#1b2733'):
    """The digits of a number in boxes. hi = positions counted from the right (0 = units) to highlight.
    steps = {position_from_right: step} makes those boxes appear one by one."""
    s = str(num)
    n = len(s)
    W = n * (size + gap) + gap
    b = ''
    for i, ch in enumerate(s):
        pos = n - 1 - i
        x = gap + i * (size + gap)
        on = pos in hi
        body = rect(x, 10, size, size + 14, color if on else base, 16) + T(x + size / 2, 10 + size * 0.78, ch, int(size * 0.72), fg_hi if on else '#fff')
        b += rvg(steps[pos], body) if steps and pos in steps else body
    return svg(W, size + 34, b, maxh)


def digsum(num, step0=0, color=ORANGE):
    """digits joined by + and then the sum; the sum line is a reveal step (step0+1)."""
    s = str(num)
    tot = sum(int(c) for c in s)
    size, gap = 74, 10
    n = len(s)
    W = n * (size + 46) + 140 + (len(str(tot)) * 50)
    b = ''
    x = 20
    for i, ch in enumerate(s):
        b += rect(x, 14, size, size + 10, BLUE, 14) + T(x + size / 2, 14 + size * 0.78, ch, 54, '#fff')
        x += size
        if i < n - 1:
            b += T(x + 23, 14 + size * 0.78, '+', 46, RED)
            x += 46
    body = T(x + 40, 14 + size * 0.78, '=', 46, NAVY) + rect(x + 74, 8, 24 + len(str(tot)) * 46, size + 22, color, 16) + T(x + 74 + (24 + len(str(tot)) * 46) / 2, 14 + size * 0.8, tot, 56, '#1b2733')
    b += rvg(step0 + 1, body) if step0 is not None else body
    return svg(x + 74 + 24 + len(str(tot)) * 46 + 20, size + 36, b, '17vh'), tot


# ---------------------------------------------------------------- sieve of Eratosthenes
def sieve(upto=50, cols=10, final=False):
    """1..upto in a grid. Steps: 1 cross out the multiples of 2, 2 of 3, 3 of 5, 4 of 7, 5 the primes light up.
    final=True draws only the finished picture (primes lit, the rest dimmed) with no steps."""
    rows = math.ceil(upto / cols)
    cw, ch = 96, 74
    W, H = cols * cw + 20, rows * ch + 20
    is_p = lambda k: k > 1 and all(k % d for d in range(2, int(k ** .5) + 1))
    crossed = {}
    for stp, pr in enumerate((2, 3, 5, 7), 1):
        for k in range(pr * pr if pr > 2 else 4, upto + 1, pr):
            if k > 1 and k not in crossed and k % pr == 0 and k != pr:
                crossed[k] = stp
    layers = {s: '' for s in range(0, 6)}
    base = ''
    for k in range(1, upto + 1):
        r, c = divmod(k - 1, cols)
        x, y = 10 + c * cw, 10 + r * ch
        cx, cy = x + cw / 2, y + ch / 2 + 11
        cell = rect(x + 3, y + 3, cw - 6, ch - 6, '#eef3f8', 12)
        txt = T(cx, cy, k, 34, NAVY)
        base += cell + txt
        if final:
            if is_p(k):
                base += rect(x + 3, y + 3, cw - 6, ch - 6, GREEN, 12) + T(cx, cy, k, 34, '#fff')
            else:
                base += rect(x + 3, y + 3, cw - 6, ch - 6, '#dfe5ea', 12, '#dfe5ea', 0) + T(cx, cy, k, 34, '#aab4be')
            continue
        if k == 1:
            layers[0] += rect(x + 3, y + 3, cw - 6, ch - 6, '#cfd6dd', 12) + T(cx, cy, 1, 34, '#8795a3')
        if k in crossed:
            layers[crossed[k]] += rect(x + 3, y + 3, cw - 6, ch - 6, '#dfe5ea', 12) + T(cx, cy, k, 34, '#aab4be') + line(x + 14, y + 12, x + cw - 14, y + ch - 12, RED, 4)
        if (k in (2, 3, 5, 7)):
            layers[crossed.get(k, 0) or {2: 1, 3: 2, 5: 3, 7: 4}[k]] += rect(x + 3, y + 3, cw - 6, ch - 6, GOLD, 12) + T(cx, cy, k, 34, '#1b2733')
        if is_p(k):
            layers[5] += rect(x + 3, y + 3, cw - 6, ch - 6, GREEN, 12) + T(cx, cy, k, 34, '#fff')
    out = base + layers[0]
    if not final:
        for s in range(1, 6):
            out += rvg(s, layers[s])
    return svg(W, H, out, '47vh')


# ---------------------------------------------------------------- divisor pairs
def pair_arcs(n, divs, colors=None):
    """divisors of n in a row, the pairs d x (n/d) joined by arcs (the outer pair is the highest); pair k appears at step k."""
    k = len(divs)
    W = k * 120 + 60
    X = lambda i: 60 + i * 120
    colors = colors or [BLUE, ORANGE, GREEN, PURPLE, RED]
    npair = k // 2
    base, rad = 70 + npair * 62 + 30, 40            # circles sit at y = base
    H = base + rad + 14
    b = ''.join(circ(X(i), base, rad, '#f4f8fb', NAVY, 3) + T(X(i), base + 14, d, 38, NAVY) for i, d in enumerate(divs))
    y0 = base - rad
    for i in range(npair):
        j = k - 1 - i
        col = colors[i % len(colors)]
        a, c = X(i), X(j)
        peak = 34 + (npair - 1 - i) * 0 + i * 62      # outer pair (i = 0) is the highest, inner pairs lower
        cy = 2 * peak - y0
        arc = f'<path d="M{a} {y0} Q{(a + c) / 2} {cy} {c} {y0}" fill="none" stroke="{col}" stroke-width="5" stroke-linecap="round"/>'
        lab = T((a + c) / 2, peak - 10, f'{divs[i]}×{divs[j]}={n}', 30, col)
        circs = circ(a, base, rad, col, '#fff', 3) + T(a, base + 14, divs[i], 38, '#fff') + circ(c, base, rad, col, '#fff', 3) + T(c, base + 14, divs[j], 38, '#fff')
        b += rvg(i + 1, arc + lab + circs)
    return svg(W, H, b, '34vh')


# ---------------------------------------------------------------- array of dots / rectangles
def arrays(n, pairs):
    """n written as rows x columns rectangles; pair k appears at step k+1 (the first is visible at once)."""
    out = ''
    x = 20
    H = 0
    for idx, (r, c) in enumerate(pairs):
        cell = 22 if max(r, c) <= 9 else 14
        w, h = c * (cell + 4) + 4, r * (cell + 4) + 4
        body = ''.join(rect(x + 4 + j * (cell + 4), 40 + 4 + i * (cell + 4), cell, cell, [BLUE, ORANGE, GREEN, PURPLE][idx % 4], 5) for i in range(r) for j in range(c))
        body += T(x + w / 2, 30, f'{r}×{c}', 28, NAVY)
        out += rvg(idx, body) if idx else body
        x += w + 40
        H = max(H, h + 60)
    return svg(x, H, out, '30vh')


# ---------------------------------------------------------------- multiples on a strip
def mult_strip(a, b, upto, ca=BLUE, cb=ORANGE, steps=True):
    """two rows of numbers: multiples of a and of b up to `upto`; the common ones are lit gold at the last step."""
    N = upto
    W = 1100
    ya, yb = 70, 190
    body_a = body_b = ''
    common = ''
    out = line(20, ya + 36, W - 10, ya + 36, '#cfd6dd', 3) + line(20, yb + 36, W - 10, yb + 36, '#cfd6dd', 3)
    out += T(14, ya - 14, f'ពហុគុណនៃ {a}', 30, ca, 'start') + T(14, yb - 14, f'ពហុគុណនៃ {b}', 30, cb, 'start')
    for k in range(a, N + 1, a):
        body_a += circ(10 + k * (W - 60) / N, ya + 36, 22, ca, '#fff', 3) + T(10 + k * (W - 60) / N, ya + 45, k, 22, '#fff')
    for k in range(b, N + 1, b):
        body_b += circ(10 + k * (W - 60) / N, yb + 36, 22, cb, '#fff', 3) + T(10 + k * (W - 60) / N, yb + 45, k, 22, '#fff')
    for k in range(1, N + 1):
        if k % a == 0 and k % b == 0:
            x = 10 + k * (W - 60) / N
            common += line(x, ya + 60, x, yb + 12, GOLD, 5) + circ(x, ya + 36, 28, GOLD, '#fff', 4) + T(x, ya + 46, k, 26, '#1b2733') + circ(x, yb + 36, 28, GOLD, '#fff', 4) + T(x, yb + 46, k, 26, '#1b2733')
    out += (rvg(1, body_a) if steps else body_a) + (rvg(2, body_b) if steps else body_b) + (rvg(3, common) if steps else common)
    return svg(W, 270, out, '36vh')


# ---------------------------------------------------------------- Venn diagram of divisors
def venn(la, lb, common, na, nb, g, ca=BLUE, cb=ORANGE):
    """Venn diagram of two lists of divisors. The numbers only in A / only in B are always there; the common ones appear at step 1,
    the biggest common one (g) is ringed in gold at step 2."""
    W, H = 1000, 400
    out = (f'<circle cx="390" cy="215" r="185" fill="{ca}" fill-opacity=".16" stroke="{ca}" stroke-width="5"/>'
           f'<circle cx="610" cy="215" r="185" fill="{cb}" fill-opacity=".16" stroke="{cb}" stroke-width="5"/>')
    out += T(300, 24, na, 28, ca) + T(700, 24, nb, 28, cb)
    ra = [x for x in la if x not in common]
    rb = [x for x in lb if x not in common]
    for i, v in enumerate(ra):
        out += T(262 + (i % 2) * 82, 150 + (i // 2) * 62, v, 36, ca)
    for i, v in enumerate(rb):
        out += T(676 + (i % 2) * 82, 150 + (i // 2) * 62, v, 36, cb)
    com, ring = '', ''
    for i, v in enumerate(common):
        x, y = 462 + (i % 2) * 76, 160 + (i // 2) * 68
        com += T(x, y, v, 40, RED)
        if v == g:
            ring = rect(x - 36, y - 40, 72, 58, GOLD, 28, '#fff', 3) + T(x, y, v, 42, '#1b2733')
    out += rvg(1, com) + rvg(2, ring)
    return svg(W, H, out, '36vh')


# ---------------------------------------------------------------- tilings
def tiles_gcd(W=126, Hh=90, s=18, maxh='30vh'):
    """a W x H rectangle cut into squares of side s: the rectangle first, then the squares (step 1), then the count (step 2)."""
    sc = 7.6
    pw, ph = W * sc, Hh * sc
    x0, y0 = 70, 40
    out = rect(x0, y0, pw, ph, '#eaf2fa', 4, NAVY, 5) + T(x0 + pw / 2, y0 - 12, f'{W} cm', 28, NAVY) + T(x0 - 14, y0 + ph / 2, f'{Hh} cm', 28, NAVY, 'end')
    sq = ''
    nx, ny = W // s, Hh // s
    for i in range(ny):
        for j in range(nx):
            sq += rect(x0 + j * s * sc + 3, y0 + i * s * sc + 3, s * sc - 6, s * sc - 6, [BLUE, TEAL, ORANGE][(i + j) % 3], 8)
    out += rvg(1, sq) + rvg(2, T(x0 + pw / 2, y0 + ph / 2 + 12, f'{s} cm', 36, '#fff'))
    return svg(x0 + pw + 40, y0 + ph + 30, out, maxh)


def tiles_lcm(a=12, b=9, side=36, maxh='32vh'):
    """small a x b cards laid in the same direction until they make a square: the cards first, the square outline at the end."""
    sc = 9
    nx, ny = side // a, side // b
    x0, y0 = 40, 20
    out = ''
    for i in range(ny):
        for j in range(nx):
            out += rect(x0 + j * a * sc + 3, y0 + i * b * sc + 3, a * sc - 6, b * sc - 6, [BLUE, TEAL, ORANGE, PURPLE][(i * nx + j) % 4], 6)
    out += rvg(1, rect(x0, y0, side * sc, side * sc, 'none', 0, RED, 6) + T(x0 + side * sc / 2, y0 + side * sc + 38, f'{side} cm', 32, RED))
    out += T(x0 + a * sc / 2, y0 + b * sc / 2 + 10, f'{a}×{b}', 26, '#fff')
    return svg(x0 * 2 + side * sc, y0 + side * sc + 60, out, maxh)


# ---------------------------------------------------------------- factor tree
def factor_tree(tree, maxh='38vh', first_step=1):
    """tree = (n, [child, child]) ; leaves are prime. A level appears at each step; prime leaves are coloured."""
    def leaves(t):
        return 1 if not t[1] else sum(leaves(c) for c in t[1])
    def depth(t):
        return 0 if not t[1] else 1 + max(depth(c) for c in t[1])
    total, d = leaves(tree), depth(tree)
    cw, lv = 200, 124
    W, H = total * cw + 40, (d + 1) * lv + 24
    nodes, edges = {}, {}
    pos = [0]
    def place(t, level):
        if not t[1]:
            x = 20 + pos[0] * cw + cw / 2
            pos[0] += 1
        else:
            xs = [place(c, level + 1) for c in t[1]]
            x = sum(xs) / len(xs)
            for cx, c in zip(xs, t[1]):
                edges.setdefault(level + 1, []).append((x, level, cx, c))
        nodes.setdefault(level, []).append((x, t))
        return x
    place(tree, 0)
    out = ''
    for lvl in range(d + 1):
        body = ''
        for (x1, l1, x2, c) in edges.get(lvl, []):
            body += line(x1, 24 + l1 * lv + 52, x2, 24 + lvl * lv - 2, '#8795a3', 5)
        for x, t in nodes.get(lvl, []):
            prime = not t[1]
            body += circ(x, 24 + lvl * lv + 22, 50, GREEN if prime else '#eef3f8', '#fff' if prime else NAVY, 5) + T(x, 24 + lvl * lv + 38, t[0], 48, '#fff' if prime else NAVY)
        out += rvg(first_step + lvl - 1, body) if lvl else body
    return svg(W, H, out, maxh)


def ladder(n, primes, step0=1):
    """division ladder as HTML: each row  value | prime  appears at its own step."""
    rows = []
    v = n
    for i, pr in enumerate(primes):
        rows.append((v, pr))
        v //= pr
    rows.append((1, ''))
    h = '<div class="ladder">'
    for i, (a, pr) in enumerate(rows):
        st = f' data-step="{step0 + i}"' if (step0 + i) else ''
        h += f'<div class="lr rv"{st}><span class="lv">{a}</span><span class="lp">{pr}</span></div>'
    return h + '</div>'
