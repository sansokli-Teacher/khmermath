# Helpers for the hand-designed Grade 7 Lesson 1 deck: small SVG/HTML pictures and slide builders.
import html as _h

NAVY, TEAL, GOLD, RED, BLUE, GREEN, PURPLE, ORANGE, GREY = '#1f4a5f', '#2b8f87', '#f0a30a', '#e03131', '#1c7ed6', '#2f9e44', '#ae3ec9', '#f08c00', '#8795a3'
FONT = "font-family=\"'Kantumruy Pro','Times New Roman',serif\""


def kh(n):
    return str(n).translate(str.maketrans('0123456789', '០១២៣៤៥៦៧៨៩'))


def esc(t):
    return _h.escape(str(t), quote=False)


def m(tex):            # inline maths
    return '\\(' + tex + '\\)'


def dm(tex):           # display maths
    return '<div class="dm">\\[' + tex + '\\]</div>'


def p(t, cls=''):
    return f'<p class="{cls}">{t}</p>' if cls else f'<p>{t}</p>'


def ul(items, cls='ts-bullets'):
    return f'<ul class="{cls}">' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'


def ol(items, cls='ts-bullets'):
    return f'<ol class="{cls}">' + ''.join(f'<li>{i}</li>' for i in items) + '</ol>'


def chip(t, color=NAVY, fg='#fff'):
    return f'<span class="chip" style="background:{color};color:{fg}">{t}</span>'


def hl(t, color=RED):  # coloured emphasis
    return f'<b style="color:{color}">{t}</b>'


def svg(w, h, body, maxh='34vh'):
    return f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" style="max-height:{maxh}" role="img">{body}</svg>'


def fig(s, cap=''):
    return f'<div class="fig">{s}' + (f'<div class="cap">{cap}</div>' if cap else '') + '</div>'


def cols(*parts):
    return '<div class="cols">' + ''.join(f'<div>{x}</div>' for x in parts) + '</div>'


def T(x, y, t, size=26, fill=NAVY, anchor='middle', weight=700, extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}" {FONT} {extra}>{esc(t)}</text>'


def circ(x, y, r, fill, stroke='none', sw=0):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def rect(x, y, w, h, fill, r=0, stroke='none', sw=0):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def line(x1, y1, x2, y2, c=NAVY, w=3, dash=''):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"{d}/>'


def arrow(x1, y1, x2, y2, c=NAVY, w=4):
    import math
    a = math.atan2(y2 - y1, x2 - x1)
    hx, hy = x2 - 14 * math.cos(a), y2 - 14 * math.sin(a)
    px, py = -math.sin(a) * 8, math.cos(a) * 8
    return line(x1, y1, hx, hy, c, w) + f'<polygon points="{x2},{y2} {hx+px},{hy+py} {hx-px},{hy-py}" fill="{c}"/>'


# ---------------------------------------------------------------- number line
def numline(lo, hi, w=1000, h=130, pts=None, segs=None, above=None, below=None, every=1, y=78, arrow_l=False, mid=None):
    """pts {value: colour}; segs [(a, b, colour)] thick bars; above {value: text}; below {value: text}."""
    x0, x1 = 60, w - 60
    X = lambda v: x0 + (v - lo) / (hi - lo) * (x1 - x0)
    b = line(x0 - (28 if arrow_l else 0), y, x1 + 24, y, NAVY, 5)
    b += f'<polygon points="{x1+40},{y} {x1+18},{y-11} {x1+18},{y+11}" fill="{NAVY}"/>'
    if arrow_l:
        b += f'<polygon points="{x0-44},{y} {x0-22},{y-11} {x0-22},{y+11}" fill="{NAVY}"/>'
    for a, c, col in (segs or []):
        b += rect(X(a), y - 9, X(c) - X(a), 18, col, 9)
    for v in range(lo, hi + 1):
        big = (v - lo) % every == 0
        b += line(X(v), y - 11, X(v), y + 11, NAVY, 3)
        if big:
            b += T(X(v), y + 46, v, 27, NAVY if not (pts and v in pts) else pts[v], weight=700)
    for v, col in (pts or {}).items():
        b += circ(X(v), y, 14, col, '#fff', 3)
    for v, t in (above or {}).items():
        b += T(X(v), y - 30, t, 26, RED)
    for v, t in (below or {}).items():
        b += T(X(v), y + 84, t, 24, TEAL)
    return svg(w, h + (36 if below else 0), b)


# ---------------------------------------------------------------- dot arrays and objects
def grid(r, c, cell=36, color=BLUE, gap=6, split=None, colors=None):
    """r x c block of squares; split=k colours the first k columns differently (distributive law)."""
    W, H = c * (cell + gap) + gap, r * (cell + gap) + gap
    b = ''
    for i in range(r):
        for j in range(c):
            col = color
            if split is not None and j >= split:
                col = (colors or [BLUE, ORANGE])[1]
            elif split is not None:
                col = (colors or [BLUE, ORANGE])[0]
            b += rect(gap + j * (cell + gap), gap + i * (cell + gap), cell, cell, col, 7)
    return W, H, b


def pair_dots(n, odd_leftover=False, cell=44):
    """n dots drawn in pairs; used for even / odd."""
    b = ''
    for k in range(n):
        gx = (k // 2) * (cell * 2 + 22)
        x = gx + (k % 2) * (cell + 6) + 24
        left = odd_leftover and k == n - 1
        b += circ(x, 40, 18, RED if left else BLUE)
    pairs = n // 2
    for g in range(pairs):
        gx = g * (cell * 2 + 22) + 6
        b += rect(gx, 14, cell * 2 + 8, 52, 'none', 26, TEAL, 3)
    return (n // 2 + 1) * (cell * 2 + 22) + 10, 82, b


def loaf(x, y, slices=3, w=170):
    b = rect(x, y, w, 70, '#d9a05b', 34, '#a8702f', 4)
    for k in range(1, slices):
        b += line(x + k * w / slices, y + 6, x + k * w / slices, y + 64, '#a8702f', 4)
    return b


def mango(x, y, r=26):
    return circ(x, y, r, PURPLE, '#6f2a82', 3) + f'<path d="M{x-12} {y-r+4} q12 -14 24 0 q-12 8 -24 0z" fill="{GREEN}"/>'


def marble(x, y, c, r=14):
    return circ(x, y, r, c) + circ(x - 4, y - 4, 4, '#fff') .replace('fill="#fff"', 'fill="#fff" opacity=".6"')


# ---------------------------------------------------------------- bar model (part-whole)
def barmodel(total, a, b_, w=980, labels=('', '', ''), colors=(BLUE, ORANGE), unknown=None):
    """total on top; a and b below; unknown 0 / 1 -> shows ? on that part"""
    f = a / total
    wa = (w - 80) * f
    wb = (w - 80) - wa
    s = rect(40, 20, w - 80, 70, '#dfe9f1', 14, NAVY, 4) + T(w / 2, 66, total if unknown != 'total' else '?', 34, NAVY)
    s += rect(40, 120, wa, 70, colors[0], 14) + T(40 + wa / 2, 166, a if unknown != 0 else '?', 34, '#fff')
    s += rect(40 + wa, 120, wb, 70, colors[1], 14) + T(40 + wa + wb / 2, 166, b_ if unknown != 1 else '?', 34, '#fff')
    s += f'<path d="M40 100 v12 M{w-40} 100 v12" stroke="{NAVY}" stroke-width="3"/>'
    if labels[0]:
        s += T(w / 2, 14, labels[0], 22, TEAL)
    return svg(w, 210, s)


# ---------------------------------------------------------------- isometric cube
def iso_cube(n, size=34, color_top='#7fc4ff', color_l='#4a9ee0', color_r='#2c7fc2'):
    import math
    c30, s30 = math.cos(math.radians(30)), math.sin(math.radians(30))
    ux, uy = size * c30, size * s30      # step along the right axis (screen)
    vx, vy = -size * c30, size * s30     # step along the left axis
    wz = size                            # up
    ox = n * size * c30 + 20
    oy = n * size + 20
    P = lambda i, j, k: (ox + i * ux + j * vx, oy + i * uy + j * vy - k * wz)
    b = ''
    # top face (k = n)
    for i in range(n):
        for j in range(n):
            pts = [P(i, j, n), P(i + 1, j, n), P(i + 1, j + 1, n), P(i, j + 1, n)]
            b += f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="{color_top}" stroke="#fff" stroke-width="2"/>'
    # right face (j = n)
    for i in range(n):
        for k in range(n):
            pts = [P(i, n, k), P(i + 1, n, k), P(i + 1, n, k + 1), P(i, n, k + 1)]
            b += f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="{color_r}" stroke="#fff" stroke-width="2"/>'
    # left face (i = n)
    for j in range(n):
        for k in range(n):
            pts = [P(n, j, k), P(n, j + 1, k), P(n, j + 1, k + 1), P(n, j, k + 1)]
            b += f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="{color_l}" stroke="#fff" stroke-width="2"/>'
    W = int(2 * n * size * c30 + 40)
    H = int(n * size * (1 + s30) + 44)
    return W, H, b


# ---------------------------------------------------------------- column arithmetic (HTML)
def _digits(x):
    return [int(d) for d in str(x)]


def addcol(nums, show_carry=True):
    """column addition with the carried digits written above."""
    res = sum(nums)
    n = len(str(res))
    rows = [str(x).rjust(n) for x in nums]
    carry = [0] * (n + 1)
    c = 0
    carries = [''] * n
    for pos in range(n - 1, -1, -1):
        s = c + sum(int(r[pos]) for r in rows if r[pos] != ' ')
        c = s // 10
        if pos - 1 >= 0 and c:
            carries[pos - 1] = str(c)
    h = '<table class="col">'
    if show_carry:
        h += '<tr class="carry"><td></td>' + ''.join(f'<td>{x}</td>' for x in carries) + '</tr>'
    for k, r in enumerate(rows):
        h += '<tr><td class="op">' + ('+' if k == len(rows) - 1 and len(rows) > 1 else '') + '</td>' + ''.join(f'<td>{ch.strip()}</td>' for ch in r) + '</tr>'
    rs = str(res).rjust(n)
    h += '<tr class="sum"><td></td>' + ''.join(f'<td>{ch.strip()}</td>' for ch in rs) + '</tr></table>'
    return h


def subcol(a, b):
    """column subtraction with borrowing shown (+10 on the borrower, -1 on the lender)."""
    res = a - b
    n = len(str(a))
    A, B = str(a).rjust(n), str(b).rjust(n)
    plus10 = [''] * n
    minus1 = [''] * n
    borrow = 0
    for pos in range(n - 1, -1, -1):
        top = int(A[pos]) - borrow
        bot = int(B[pos]) if B[pos] != ' ' else 0
        if top < bot:
            plus10[pos] = '+10'
            if pos - 1 >= 0:
                minus1[pos - 1] = '−1'
            borrow = 1
        else:
            borrow = 0
    h = '<table class="col"><tr class="carry"><td></td>' + ''.join(f'<td class="bw">{x}</td>' for x in plus10) + '</tr>'
    h += '<tr class="carry"><td></td>' + ''.join(f'<td class="bw2">{x}</td>' for x in minus1) + '</tr>'
    h += '<tr><td class="op"></td>' + ''.join(f'<td>{ch.strip()}</td>' for ch in A) + '</tr>'
    h += '<tr><td class="op">−</td>' + ''.join(f'<td>{ch.strip()}</td>' for ch in B) + '</tr>'
    rs = str(res).rjust(n)
    h += '<tr class="sum"><td></td>' + ''.join(f'<td>{ch.strip()}</td>' for ch in rs) + '</tr></table>'
    return h


# ---------------------------------------------------------------- place-value chart
PV_NAMES = ['លាន', 'រយពាន់', 'ដប់ពាន់', 'ពាន់', 'រយ', 'ដប់', 'រាយ']


def pvchart(num, mark=None, color=GOLD):
    """place-value chart of an integer; mark = index (from the right, 0 = units) to highlight"""
    ds = list(str(num))
    n = len(ds)
    names = PV_NAMES[-n:] if n <= 7 else PV_NAMES
    h = '<table class="pv"><tr>' + ''.join(f'<th>{names[i]}</th>' for i in range(n)) + '</tr><tr>'
    for i, d in enumerate(ds):
        idx = n - 1 - i
        st = f' style="background:{color};color:#1b2733"' if mark is not None and idx == mark else ''
        h += f'<td{st}>{d}</td>'
    return h + '</tr></table>'


# ---------------------------------------------------------------- slides
def slide(kick=None, h2=None, body='', k=None, c=None):
    html = ''
    if kick:
        html += f'<p class="ts-kicker">{kick}</p>'
    if h2:
        html += f'<h2>{h2}</h2>'
    html += body
    d = {'html': html}
    if k:
        d['k'] = k
    if c:
        d['c'] = c
    return d


def part(n, title, hook=''):
    return {'k': 'title', 'html': f'<p class="ts-kicker">ផ្នែក</p><h1>{n}. {title}</h1>{hook}'}


def key(kick, title, body):
    return slide(kick, title, body, k='key')


def ex(kick, title, body):
    return slide(kick, title, body, k='ex')


def prac(kick, title, body):
    return slide(kick, title, body, k='prac')


def sol(kick, title, body):
    return slide(kick, title, body, k='sol')


# ---------------------------------------------------------------- step-by-step reveal (see public/js/teachshow.js)
import re as _re


def rvg(n, body, until=None):
    """SVG group that appears at step n (0 = visible from the start) and optionally disappears again at step `until`."""
    a = (f' data-step="{n}"' if n else '') + (f' data-until="{until}"' if until else '')
    return f'<g class="rv"{a}>{body}</g>'


def rvd(n, html, cls=''):
    """HTML block that appears at step n."""
    c = ('rv ' + cls).strip()
    return f'<div class="{c}" data-step="{n}">{html}</div>'


_TAG = _re.compile(r'<(/?)(p|div|table|tr|td|th|ul|ol|li|span|svg|b|i|g|h2|h3|blockquote|thead|tbody|mark)(\s[^>]*?)?(/?)>')


def _top_level(body):
    """Split an HTML string into its top-level blocks; None when the markup is not balanced (then it is left alone)."""
    parts, depth, start = [], 0, 0
    for mt in _TAG.finditer(body):
        close, selfc = mt.group(1) == '/', mt.group(4) == '/'
        if selfc:
            continue
        if not close:
            if depth == 0 and body[start:mt.start()].strip():
                return None                        # loose text between blocks
            depth += 1
        else:
            depth -= 1
            if depth < 0:
                return None
            if depth == 0:
                parts.append(body[start:mt.end()])
                start = mt.end()
    if depth != 0 or body[start:].strip():
        return None
    return parts


_LIST = _re.compile(r'^(<(?:ul|ol)(?:\s[^>]*)?>)(.*)(</(?:ul|ol)>)$', _re.S)


def stepify(d, keep_first=True, min_units=2):
    """Turn a slide's blocks (after the kicker and heading) into reveal steps: the first block stays visible,
    every later block - or every later bullet of a list - is shown by the next press of →.
    Slides that already have steps, or markup we cannot split safely, are left alone."""
    html = d['html']
    if 'data-step' in html:
        return d
    head = _re.match(r'^(<p class="ts-kicker">.*?</p>)?(<h2>.*?</h2>)?', html, _re.S).group(0)
    blocks = _top_level(html[len(head):])
    if not blocks:
        return d
    units = []                                   # ('block', html) or ('list', open, [li...], close)
    for b in blocks:
        ml = _LIST.match(b)
        lis = _top_level(ml.group(2)) if ml else None
        if ml and lis and all(x.startswith('<li') for x in lis):
            units.append(('list', ml.group(1), lis, ml.group(3)))
        else:
            units.append(('block', b))
    if sum(len(u[2]) if u[0] == 'list' else 1 for u in units) < min_units:
        return d
    out, n, first = [], 0, True
    for u in units:
        if u[0] == 'block':
            if first and keep_first:
                out.append(u[1])
            else:
                n += 1
                out.append(f'<div class="rv" data-step="{n}">{u[1]}</div>')
            first = False
        else:
            row = []
            for li in u[2]:
                if first and keep_first:
                    row.append(li)
                else:
                    n += 1
                    row.append(li.replace('<li', f'<li data-step="{n}"', 1))
                first = False
            out.append(u[1] + ''.join(row) + u[3])
    return {**d, 'html': head + ''.join(out)}


def capstack(items):
    """One caption position whose text changes with the steps: items = [(step, until_or_None, html)].
    All captions share a single grid cell, so the slide keeps a fixed height and nothing jumps."""
    out = ''
    for n, u, h in items:
        a = (f' data-step="{n}"' if n else '') + (f' data-until="{u}"' if u else '')
        out += f'<div class="rv"{a}>{h}</div>'
    return f'<div class="capstack">{out}</div>'
