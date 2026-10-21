# The book exercises' solution slides arrive with the sub-questions (ក. ខ. គ. ...) nested inside one another and crammed on one slide
# at 9-15 px. This rebuilds each of them as clean slides: one group of sub-questions per slide, a readable size, and a (1/3) counter.
import re

MARK = '<li class="lab"><span class="lb">'
KH = '០១២៣៤៥៦៧៨៩'
VOID = {'br', 'img', 'hr'}


def kh(n):
    return ''.join(KH[int(c)] for c in str(n))


def tidy(html):
    """Close what was left open and drop closing tags that have nothing to close."""
    out, stack = [], []
    pos = 0
    for mt in re.finditer(r'<(/?)([a-zA-Z0-9]+)[^>]*?(/?)>', html):
        out.append(html[pos:mt.start()]); pos = mt.end()
        close, name, selfc = mt.group(1), mt.group(2).lower(), mt.group(3)
        if close:
            if name in stack:
                while stack:
                    top = stack.pop(); out.append('</%s>' % top)
                    if top == name: break
        else:
            out.append(mt.group(0))
            if name not in VOID and not selfc: stack.append(name)
    out.append(html[pos:])
    while stack: out.append('</%s>' % stack.pop())
    return ''.join(out)


def weight(s):
    return len(re.sub(r'<[^>]+>', '', s))


def split_solution(slide, limit=430):
    html = slide['html']
    if html.count(MARK) < 2: return [slide]
    head, *parts = html.split(MARK)
    h2 = re.search(r'<h2>(.*?)</h2>', head, re.S)
    title = re.sub(r'\s*<span class="ts-pg">.*?</span>', '', h2.group(1)).strip()
    kicker = re.search(r'<p class="ts-kicker">.*?</p>', head).group(0)
    intro = head[h2.end():] if h2 else ''
    bodies = []
    for ptxt in parts:
        lb, rest = ptxt.split('</span><div>', 1)
        rest = re.sub(r'(<ul class="ts-bullets">\s*)+$', '', rest.rstrip())
        bodies.append((lb, tidy(rest)))
    groups, cur, w = [], [], 0
    for b in bodies:
        wb = weight(b[1])
        if cur and w + wb > limit: groups.append(cur); cur, w = [], 0
        cur.append(b); w += wb
    if cur: groups.append(cur)
    out = []
    for gi, g in enumerate(groups):
        pg = '' if len(groups) == 1 else ' <span class="ts-pg">(%s/%s)</span>' % (kh(gi + 1), kh(len(groups)))
        lis = ''.join('%s%s</span><div>%s</div></li>' % (MARK, lb, body) for lb, body in g)
        out.append(dict(slide, html='%s<h2>%s%s</h2>%s<ul class="ts-bullets">%s</ul>' % (kicker, title, pg, tidy(intro) if gi == 0 else '', lis)))
    return out


def _title(slide):
    m = re.search(r'<h2>(.*?)</h2>', slide['html'], re.S)
    return re.sub(r'\s*<span class="ts-pg">.*?</span>', '', m.group(1)).strip() if m else ''


def rebuild(slides):
    """Join consecutive solution slides of one exercise, then lay them out again."""
    out, i = [], 0
    while i < len(slides):
        s = slides[i]
        if s['k'] != 'sol': out.append(s); i += 1; continue
        j, merged = i + 1, s
        while j < len(slides) and slides[j]['k'] == 'sol' and _title(slides[j]) == _title(s) and MARK in slides[j]['html']:
            merged = dict(merged, html=merged['html'] + MARK + slides[j]['html'].split(MARK, 1)[1])
            j += 1
        out.extend(split_solution(merged)); i = j
    return out
