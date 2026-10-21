# Adds the common animations to every picture of a deck: lines and curves draw themselves, points pop in, arrowheads appear when the line reaches them.
# Pure post-processing of the SVG text: an element that already carries a class with «pen-» (the hand-made animations) is left alone, and so is a dashed line.
import math, re

_TAG = re.compile(r'<(line|path|circle|polygon)\b([^>]*?)(/?)>')


def _num(attrs, name, default=0.0):
    m = re.search(r'\b%s="(-?[\d.]+)"' % name, attrs)
    return float(m.group(1)) if m else default


def _path_len(d):
    """an upper bound for the length of a path made of M, L, Q and A commands (so the dash covers the whole line)"""
    toks = re.findall(r'[MLQAZ]|-?\d*\.?\d+', d)
    i, cur, total = 0, (0.0, 0.0), 0.0
    while i < len(toks):
        c = toks[i]; i += 1
        if c == 'M':
            cur = (float(toks[i]), float(toks[i + 1])); i += 2
        elif c == 'L':
            p = (float(toks[i]), float(toks[i + 1])); i += 2; total += math.dist(cur, p); cur = p
        elif c == 'Q':
            q, p = (float(toks[i]), float(toks[i + 1])), (float(toks[i + 2]), float(toks[i + 3])); i += 4; total += math.dist(cur, q) + math.dist(q, p); cur = p
        elif c == 'A':
            p = (float(toks[i + 5]), float(toks[i + 6])); i += 7; total += math.dist(cur, p) * 1.6; cur = p
    return total


def animate(svg):
    n = [0]

    def sub(m):
        tag, attrs, close = m.group(1), m.group(2), m.group(3)
        if 'pen-' in attrs or 'class=' in attrs:
            return m.group(0)
        k = n[0]; n[0] += 1
        delay = (k % 10) * 0.07
        if tag == 'line':
            if 'stroke-dasharray' in attrs or _num(attrs, 'stroke-width', 1) < 3:
                return m.group(0)
            L = math.hypot(_num(attrs, 'x2') - _num(attrs, 'x1'), _num(attrs, 'y2') - _num(attrs, 'y1')) * 1.05 + 2
        elif tag == 'path':
            d = re.search(r'\bd="([^"]*)"', attrs)
            if not d or 'fill="none"' not in attrs or 'stroke-dasharray' in attrs or _num(attrs, 'stroke-width', 1) < 3 or 'style=' in attrs:
                return m.group(0)
            L = _path_len(d.group(1)) * 1.05 + 2
        elif tag == 'circle':
            r = _num(attrs, 'r')
            if r > 20 or r < 4 or 'fill="none"' in attrs or 'opacity' in attrs or 'style=' in attrs:
                return m.group(0)
            return f'<{tag} class="pen-pop" style="--d:{0.35 + delay:.2f}s"{attrs}{close}>'
        else:                                                           # polygon: only the small triangles (arrowheads)
            pts = re.search(r'points="([^"]*)"', attrs)
            if not pts or 'style=' in attrs:
                return m.group(0)
            xy = [float(v) for v in re.findall(r'-?\d*\.?\d+', pts.group(1))]
            if len(xy) != 6 or (max(xy[0::2]) - min(xy[0::2])) > 26 or (max(xy[1::2]) - min(xy[1::2])) > 26:
                return m.group(0)
            return f'<{tag} class="pen-late" style="animation:penLate .25s ease-out {0.55 + delay:.2f}s both"{attrs}{close}>'
        return f'<{tag} class="pen-on" style="stroke-dasharray:{L:.0f};animation:penDraw .75s ease-out {delay:.2f}s both"{attrs}{close}>'

    return _TAG.sub(sub, svg)


def animate_deck(slides):
    """animate every <svg> in a list of slide dicts (returns new dicts)"""
    out = []
    for sl in slides:
        h = sl['html']
        if '<svg' in h:
            h = re.sub(r'<svg.*?</svg>', lambda m: animate(m.group(0)), h, flags=re.S)
        out.append(dict(sl, html=h))
    return out
