# -*- coding: utf-8 -*-
"""Small SVG toolkit for question-bank figures that follow IMAGE_STYLE_GUIDE.md:
transparent background (no <rect fill=white/>), thin uniform lines, flat colours,
variables / points in Mathcad UniMath italic, numbers and units in upright Times.

plane(...)  draws a coordinate plane (complex plane) with points, vectors, segments, polygons, arcs and notes.
Coordinates are in math units; the toolkit converts to pixels (y points up)."""
import math

ITALIC = "font-family='Mathcad UniMath, Times New Roman, serif' font-style='italic'"
UPRIGHT = "font-family='Times New Roman, serif'"
INK, GRID, AXIS = '#1e293b', '#e2e8f0', '#475569'
BLUE, RED, GREEN, AMBER, PURPLE = '#2563eb', '#dc2626', '#16a34a', '#d97706', '#7c3aed'


def _lab(text, x, y, anchor='middle', size=17, color=INK, italic=True, weight='normal'):
    """text with optional subscript: 'M_1' -> M with subscript 1, 'z̅' kept as given."""
    fam = ITALIC if italic else UPRIGHT
    if '_' in text:
        base, sub = text.split('_', 1)
        return ("<text x='%.1f' y='%.1f' text-anchor='%s' %s font-size='%d' fill='%s' font-weight='%s'>%s"
                "<tspan font-size='%d' dy='4'>%s</tspan></text>") % (x, y, anchor, fam, size, color, weight, base, int(size * 0.7), sub)
    return "<text x='%.1f' y='%.1f' text-anchor='%s' %s font-size='%d' fill='%s' font-weight='%s'>%s</text>" % (x, y, anchor, fam, size, color, weight, text)


def plane(xr, yr, unit=36, pts=(), vecs=(), segs=(), polys=(), arcs=(), notes=(), bands=(), grid=True, ticks=True,
          xlabel='x', ylabel='y', pad=24, tick_every=1, unit_circle=None, circles=()):
    """pts   : (x, y, label, dx, dy, color)            a dot with a label offset (dx, dy) in px
       vecs  : (x0, y0, x1, y1, color, dashed)         arrow
       segs  : (x0, y0, x1, y1, color, dashed)         plain segment
       polys : ([(x, y), ...], stroke, fill_or_None, dashed)
       arcs  : (cx, cy, r, a0_deg, a1_deg, color)      circular arc in math units, counter-clockwise
       notes : (x, y, text, dx, dy, color, italic)     free text next to a math coordinate
       bands : (y0, y1, color, opacity)                a horizontal strip (a river)
       circles: (cx, cy, r, color, dashed)             circle in math units
    """
    (x0, x1), (y0, y1) = xr, yr
    W = (x1 - x0) * unit + 2 * pad
    H = (y1 - y0) * unit + 2 * pad

    def px(x): return pad + (x - x0) * unit

    def py(y): return pad + (y1 - y) * unit

    o = ["<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d'>" % (W, H, W, H),
         "<defs>"]
    for name, col in [('a', INK), ('b', BLUE), ('r', RED), ('g', GREEN), ('m', AMBER), ('p', PURPLE), ('x', AXIS)]:
        o.append("<marker id='h%s' viewBox='0 0 10 10' refX='8.5' refY='5' markerWidth='7' markerHeight='7' orient='auto-start-reverse'>"
                 "<path d='M 0 1 L 9 5 L 0 9 z' fill='%s'/></marker>" % (name, col))
    o.append("</defs>")
    cmap = {INK: 'a', BLUE: 'b', RED: 'r', GREEN: 'g', AMBER: 'm', PURPLE: 'p', AXIS: 'x'}

    for (b0, b1, col, op) in bands:
        o.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s' opacity='%.2f'/>" % (px(x0), py(b1), (x1 - x0) * unit, (b1 - b0) * unit, col, op))
    if grid:
        for gx in range(int(math.ceil(x0)), int(math.floor(x1)) + 1):
            o.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>" % (px(gx), py(y0), px(gx), py(y1), GRID))
        for gy in range(int(math.ceil(y0)), int(math.floor(y1)) + 1):
            o.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>" % (px(x0), py(gy), px(x1), py(gy), GRID))
    # axes
    ax_y = py(0) if y0 <= 0 <= y1 else py(y0)
    ax_x = px(0) if x0 <= 0 <= x1 else px(x0)
    o.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.6' marker-end='url(#hx)'/>" % (px(x0) - 6, ax_y, px(x1) + 4, ax_y, AXIS))
    o.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.6' marker-end='url(#hx)'/>" % (ax_x, py(y0) + 6, ax_x, py(y1) - 4, AXIS))
    o.append(_lab(xlabel, px(x1) + 2, ax_y + 18, size=16))
    o.append(_lab(ylabel, ax_x - 12, py(y1) + 2, size=16))
    o.append(_lab('O', ax_x - 9, ax_y + 17, size=16))
    if ticks:
        for tx in range(int(math.ceil(x0)), int(math.floor(x1)) + 1):
            if tx != 0 and tx % tick_every == 0:
                o.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.2'/>" % (px(tx), ax_y - 3, px(tx), ax_y + 3, AXIS))
                o.append(_lab(str(tx), px(tx), ax_y + 17, size=13, color=AXIS, italic=False))
        for ty in range(int(math.ceil(y0)), int(math.floor(y1)) + 1):
            if ty != 0 and ty % tick_every == 0:
                o.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.2'/>" % (ax_x - 3, py(ty), ax_x + 3, py(ty), AXIS))
                o.append(_lab(str(ty), ax_x - 7, py(ty) + 4, anchor='end', size=13, color=AXIS, italic=False))
    for (cx, cy, r, col, dashed) in circles:
        o.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='none' stroke='%s' stroke-width='1.8'%s/>" % (px(cx), py(cy), r * unit, col, " stroke-dasharray='5 4'" if dashed else ''))
    for (pts_, stroke, fill, dashed) in polys:
        d = ' '.join("%.1f,%.1f" % (px(x), py(y)) for x, y in pts_)
        o.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='1.8'%s/>" % (d, fill or 'none', stroke, " stroke-dasharray='5 4'" if dashed else ''))
    for (sx, sy, ex, ey, col, dashed) in segs:
        o.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.8'%s/>" % (px(sx), py(sy), px(ex), py(ey), col, " stroke-dasharray='5 4'" if dashed else ''))
    for (cx, cy, r, a0, a1, col) in arcs:
        sx, sy = px(cx + r * math.cos(math.radians(a0))), py(cy + r * math.sin(math.radians(a0)))
        ex, ey = px(cx + r * math.cos(math.radians(a1))), py(cy + r * math.sin(math.radians(a1)))
        large = 1 if (a1 - a0) % 360 > 180 else 0
        o.append("<path d='M %.1f %.1f A %.1f %.1f 0 %d 0 %.1f %.1f' fill='none' stroke='%s' stroke-width='1.8'/>" % (sx, sy, r * unit, r * unit, large, ex, ey, col))
    for (sx, sy, ex, ey, col, dashed) in vecs:
        o.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.2' marker-end='url(#h%s)'%s/>" % (
            px(sx), py(sy), px(ex), py(ey), col, cmap.get(col, 'a'), " stroke-dasharray='6 4'" if dashed else ''))
    for (x, y, label, dx, dy, col) in pts:
        o.append("<circle cx='%.1f' cy='%.1f' r='4' fill='%s'/>" % (px(x), py(y), col))
        if label:
            o.append(_lab(label, px(x) + dx, py(y) + dy, size=18, color=INK))
    for (x, y, text, dx, dy, col, ital) in notes:
        o.append(_lab(text, px(x) + dx, py(y) + dy, size=15, color=col, italic=ital))
    o.append("</svg>")
    return '\n'.join(o)


def dashed_to_axes(x, y, color=AXIS):
    """dashed projections of the point (x, y) onto both axes, as `segs` entries."""
    return [(x, 0, x, y, color, True), (0, y, x, y, color, True)]
