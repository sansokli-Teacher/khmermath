#!/usr/bin/env python3
"""Build classroom slide decks for Grade 7 lessons 2-22 from Lesson/G7/lessonN.tex.

  python3 tools/make_g7_slides.py [path/to/Lesson/G7]

Writes public/js/slides/g7/lessonN.js (window.TEACH_SLIDES['7-N']) and public/data/lessons_g7.json.
Lesson 1 keeps its hand-made deck (public/js/slides/g7l01.js).
"""
import json
import os
import re
import sys

SRC = sys.argv[1] if len(sys.argv) > 1 else '/Users/koemsreang/PISA_Math_2026-new/Lesson/G7'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'public')
KH = '០១២៣៤៥៦៧៨៩'
kh = lambda n: re.sub(r'\d', lambda m: KH[int(m.group())], str(n))

PAGE_LIMIT = 620     # rough visible characters per slide before it is split
MERGE_LIMIT = 420    # consecutive short examples are merged onto one slide

KEY_WORDS = ('ជាទូទៅ', 'និយមន័យ', 'ទ្រឹស្តីបទ', 'លក្ខណៈ', 'ច្បាប់', 'សម្គាល់', 'ចំណាំ', 'រូបមន្ត', 'សរុប', 'សេចក្តីសង្ខេប', 'វិធី')
EX_WORDS = ('ឧទាហរណ៍',)
PRAC_WORDS = ('លំហាត់គំរូ', 'ប្រតិបត្តិ', 'សកម្មភាព', 'បញ្ហា')
SOL_WORDS = ('ដំណោះស្រាយ', 'ចម្លើយ', 'ចំលើយ')


# ---------------------------------------------------------------- LaTeX helpers
def strip_comments(s):
    out = []
    for line in s.split('\n'):
        m = re.search(r'(?<!\\)%', line)
        out.append(line[:m.start()] if m else line)
    return '\n'.join(out)


def match_brace(s, i):
    """s[i] == '{' -> index of the matching '}'."""
    d = 0
    for j in range(i, len(s)):
        c = s[j]
        if c == '\\':
            continue
        if c == '{' and s[j - 1] != '\\':
            d += 1
        elif c == '}' and s[j - 1] != '\\':
            d -= 1
            if d == 0:
                return j
    return len(s) - 1


def find_env_end(s, start, name):
    """start is the index just after '\\begin{name}'. Returns index of the matching '\\end{name}'."""
    d = 1
    for m in re.finditer(r'\\(begin|end)\{' + re.escape(name) + r'\}', s[start:]):
        d += 1 if m.group(1) == 'begin' else -1
        if d == 0:
            return start + m.start()
    return len(s)


def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


MATH_RE = re.compile(r'\$\$((?:\\.|[^\\])+?)\$\$|\\\[(.+?)\\\]|\$((?:\\.|[^\\$])+)\$', re.S)


def math_html(m):
    disp = m.group(1) if m.group(1) is not None else m.group(2)
    if disp is not None:
        return '\\[' + esc(disp.strip()) + '\\]'
    return '\\(' + esc(m.group(3).strip()) + '\\)'


def inline(text):
    """Inline LaTeX (no block environments) -> HTML."""
    parts, last = [], 0
    for m in MATH_RE.finditer(text):
        parts.append(('t', text[last:m.start()]))
        parts.append(('m', math_html(m)))
        last = m.end()
    parts.append(('t', text[last:]))
    out = []
    for kind, p in parts:
        if kind == 'm':
            out.append(p)
            continue
        p = esc(p)
        p = re.sub(r'\\textbf\{', '<b>', p)
        p = re.sub(r'\\(?:textit|emph)\{', '<i>', p)
        p = re.sub(r'\\underline\{', '<u>', p)
        # close the braces opened above (they are balanced in the sources)
        out.append(close_tags(p))
    return ''.join(out)


def close_tags(p):
    res, stack, i = [], [], 0
    while i < len(p):
        if p.startswith('<b>', i):
            stack.append('b'); res.append('<b>'); i += 3
        elif p.startswith('<i>', i):
            stack.append('i'); res.append('<i>'); i += 3
        elif p.startswith('<u>', i):
            stack.append('u'); res.append('<u>'); i += 3
        elif p[i] == '{':
            stack.append(None); i += 1
        elif p[i] == '}':
            t = stack.pop() if stack else None
            if t:
                res.append(f'</{t}>')
            i += 1
        else:
            res.append(p[i]); i += 1
    while stack:
        t = stack.pop()
        if t:
            res.append(f'</{t}>')
    s = ''.join(res)
    s = s.replace('\\\\', '<br>').replace('\\%', '%').replace('\\&amp;', '&amp;').replace('\\_', '_').replace('\\#', '#')
    s = s.replace('~', '&nbsp;').replace('\\ ', ' ')
    s = re.sub(r'\\(?:quad|qquad)\b', '&emsp;', s)
    s = re.sub(r'\\ldots|\\dots', '…', s)
    s = re.sub(r'\\(?:hfill|noindent|centering|par|smallskip|medskip|bigskip|newpage|clearpage|raggedright|small|large|Large|normalsize|footnotesize)\b\s*', '', s)
    s = re.sub(r'\\(?:vspace|hspace|setlength|label)\*?\{[^}]*\}', '', s)
    s = re.sub(r'\\[a-zA-Z]+\*?(?![a-zA-Z])', '', s) if '\\(' not in s and '\\[' not in s else strip_unknown_outside_math(s)
    return s


def strip_unknown_outside_math(s):
    out, i = [], 0
    while i < len(s):
        if s.startswith('\\(', i) or s.startswith('\\[', i):
            end = s.find('\\)' if s[i + 1] == '(' else '\\]', i + 2)
            end = len(s) if end < 0 else end + 2
            out.append(s[i:end]); i = end
        else:
            j = i
            while j < len(s) and not (s.startswith('\\(', j) or s.startswith('\\[', j)):
                j += 1
            out.append(re.sub(r'\\[a-zA-Z]+\*?(?![a-zA-Z])', '', s[i:j])); i = j
    return ''.join(out)


def tabular_html(body):
    body = re.sub(r'\\(?:hline|cline\{[^}]*\})', '', body)
    rows = [r.strip() for r in re.split(r'\\\\', body) if r.strip()]
    trs = []
    for r in rows:
        cells = [c.strip() for c in re.split(r'(?<!\\)&', r)]
        trs.append('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in cells) + '</tr>')
    return '<table class="ts-table">' + ''.join(trs) + '</table>'


def parse_blocks(s):
    """LaTeX fragment -> list of HTML blocks (paragraphs, lists, tables)."""
    s = s.strip()
    blocks, i, buf = [], 0, []

    def flush():
        txt = '\n'.join(buf).strip()
        buf.clear()
        if not txt:
            return
        for para in re.split(r'\n\s*\n', txt):
            para = para.strip()
            if not para:
                continue
            # mask math across the whole paragraph first ($$ ... $$ blocks span several lines)
            stash = []

            def mask(m, stash=stash):
                stash.append(math_html(m))
                return f'@@M{len(stash) - 1}@@'
            para = MATH_RE.sub(mask, para)
            lines = []
            for ln in para.split('\n'):
                ln = ln.strip()
                if re.match(r'^[ក-អ]\.\s|^\d+\)\s|^\([ក-អ0-9]+\)\s', ln) and lines:
                    lines.append('<br>' + inline(ln))
                else:
                    lines.append(inline(ln))
            h = ' '.join(lines).strip()
            h = re.sub(r'@@M(\d+)@@', lambda m: stash[int(m.group(1))], h)
            if h:
                blocks.append(f'<p>{h}</p>')

    while i < len(s):
        m = re.compile(r'\\begin\{(itemize|enumerate|quote|center|tabular|tabularx|table|solution)\}(\{[^}]*\})?').search(s, i)
        if not m:
            buf.append(s[i:]); break
        buf.append(s[i:m.start()])
        name = m.group(1)
        body_start = m.end()
        end = find_env_end(s, body_start, name)
        body = s[body_start:end]
        flush()
        if name in ('itemize', 'enumerate'):
            blocks.append(list_html(body, name))
        elif name == 'quote':
            blocks.append('<blockquote>' + ''.join(parse_blocks(body)) + '</blockquote>')
        elif name in ('center', 'table', 'solution'):
            body = re.sub(r'\\caption\{[^}]*\}', '', body)
            blocks.extend(parse_blocks(body))
        else:  # tabular / tabularx
            if name == 'tabularx':
                body = re.sub(r'^\{[^}]*\}', '', body.strip())
            body = re.sub(r'^\{[^}]*\}', '', body.strip())
            blocks.append(tabular_html(body))
        i = end + len('\\end{' + name + '}')
    flush()
    return blocks


def split_items(body):
    """Split a list body into [(label, text)] at top-level \\item."""
    items, depth, last_start, label = [], 0, None, None
    pos = [(m.start(), m.end(), m.group(1)) for m in re.finditer(r'\\item(?:\[([^\]]*)\])?', body)]
    # keep only depth-0 items
    keep = []
    for st, en, lab in pos:
        pre = body[:st]
        d = len(re.findall(r'\\begin\{(?:itemize|enumerate)\}', pre)) - len(re.findall(r'\\end\{(?:itemize|enumerate)\}', pre))
        if d == 0:
            keep.append((st, en, lab))
    for k, (st, en, lab) in enumerate(keep):
        nxt = keep[k + 1][0] if k + 1 < len(keep) else len(body)
        items.append((lab, body[en:nxt].strip()))
    return items


def list_html(body, kind):
    items = split_items(body)
    lis = []
    for lab, txt in items:
        inner = ''.join(parse_blocks(txt))
        inner = re.sub(r'^<p>(.*)</p>$', r'\1', inner, flags=re.S) if inner.count('<p>') == 1 and inner.startswith('<p>') and inner.endswith('</p>') else inner
        if lab:
            lis.append(f'<li class="lab"><span class="lb">{inline(lab)}</span><div>{inner}</div></li>')
        else:
            lis.append(f'<li>{inner}</li>')
    tag = 'ol' if kind == 'enumerate' else 'ul'
    cls = ' class="ts-bullets"' if tag == 'ul' else ' class="ts-bullets"'
    return f'<{tag}{cls}>' + ''.join(lis) + f'</{tag}>'


# ---------------------------------------------------------------- lesson structure
def top_level_units(tex):
    """Split the body into [(kind, title, text)] at depth-0 headings / bold markers."""
    lines = tex.split('\n')
    units, cur, depth = [], None, 0

    def new(kind, title, first=''):
        nonlocal cur
        cur = {'kind': kind, 'title': title, 'lines': [first] if first else []}
        units.append(cur)

    new('intro', '')
    for ln in lines:
        st = ln.strip()
        if depth == 0:
            m = re.match(r'\\(section|subsection|subsubsection)\*?\{(.*)\}\s*$', st)
            if m:
                new(m.group(1), m.group(2).strip())
                continue
            m = re.match(r'\\textbf\{([^}]*)\}\s*(.*)$', st)
            if m and (m.group(1).strip().rstrip('៖: ').split(' ')[0] in
                      EX_WORDS + KEY_WORDS + PRAC_WORDS + SOL_WORDS or m.group(1).strip().startswith(EX_WORDS + PRAC_WORDS + SOL_WORDS)):
                new('chunk', m.group(1).strip().rstrip('៖: ').strip(), m.group(2))
                continue
        depth += len(re.findall(r'\\begin\{(?:itemize|enumerate|solution|quote|center|tabular|tabularx|table)\}', ln))
        depth -= len(re.findall(r'\\end\{(?:itemize|enumerate|solution|quote|center|tabular|tabularx|table)\}', ln))
        if depth < 0:
            depth = 0
        cur['lines'].append(ln)
    for u in units:
        u['text'] = '\n'.join(u['lines']).strip()
    return units


def classify(title):
    t = title.strip()
    if t.startswith(SOL_WORDS):
        return 'sol'
    if t.startswith(PRAC_WORDS):
        return 'prac'
    if t.startswith(EX_WORDS):
        return 'ex'
    return 'key'


def vis_len(html):
    t = re.sub(r'<[^>]+>', '', html)
    t = re.sub(r'\\\((.*?)\\\)|\\\[(.*?)\\\]', lambda m: 'x' * int(len(m.group(1) or m.group(2)) * 0.5), t, flags=re.S)
    return len(t)


def paginate(blocks):
    """Pack HTML blocks into pages; split oversized lists item by item."""
    flat = []
    for b in blocks:
        if vis_len(b) > PAGE_LIMIT and b[:3] in ('<ol', '<ul'):
            tag = 'ol' if b.startswith('<ol') else 'ul'
            items = re.findall(r'<li.*?</li>', b, flags=re.S)
            n = 0
            for it in items:
                n += 1
                start = f' start="{n}"' if tag == 'ol' else ''
                flat.append(f'<{tag} class="ts-bullets"{start}>{it}</{tag}>')
        else:
            flat.append(b)
    pages, cur, size = [], [], 0
    for b in flat:
        l = vis_len(b)
        if cur and size + l > PAGE_LIMIT:
            pages.append(cur); cur, size = [], 0
        cur.append(b); size += l
    if cur:
        pages.append(cur)
    return pages or [[]]


def make_slides(n, tex):
    tex = strip_comments(tex)
    m = re.search(r'\\chapter\*?\{([^}]*)\}', tex)
    title = re.sub(r'^មេរៀនទី\s*\S+\s*[:៖]\s*', '', m.group(1)).strip() if m else f'មេរៀនទី {n}'
    tex = re.sub(r'\\chapter\*?\{[^}]*\}', '', tex)
    units = top_level_units(tex)
    slides = []
    sec_titles = [u['title'] for u in units if u['kind'] == 'subsection']
    slides.append({'k': 'title', 'html': f'<p class="ts-kicker">ថ្នាក់ទី ៧ · មេរៀនទី {kh(n)}</p><h1>{inline(title)}</h1><p class="ts-sub">{kh(len(sec_titles))} ផ្នែក</p>'})

    sec = sub = ''
    mode = 'lesson'

    def add(kind, head, blocks, kicker):
        pages = paginate(blocks)
        for pi, pg in enumerate(pages):
            h = head + (f' <span class="ts-pg">({kh(pi + 1)}/{kh(len(pages))})</span>' if len(pages) > 1 else '')
            slides.append({'k': kind, 'html': f'<p class="ts-kicker">{kicker}</p><h2>{h}</h2>' + ''.join(pg)})

    pending_ex = []   # merged short examples

    def flush_ex():
        nonlocal pending_ex
        if len(pending_ex) == 1:
            t, b = pending_ex[0]
            add('ex', inline(t), b, kicker_of())
            pending_ex = []
        if pending_ex:
            blocks = []
            for t, b in pending_ex:
                blocks.append(f'<p class="ts-exh">{inline(t)}</p>')
                blocks.extend(b)
            add('ex', 'ឧទាហរណ៍', blocks, kicker_of())
            pending_ex = []

    def kicker_of():
        k = inline(sec)
        return k + (f' · {inline(sub)}' if sub else '')

    for u in units:
        kind, ttl, text = u['kind'], u['title'], u['text']
        if kind == 'section':
            flush_ex()
            sec, sub = ttl, ''
            mode = 'ex' if 'លំហាត់' in ttl else 'lesson'
            if mode == 'ex':
                slides.append({'k': 'title', 'html': f'<p class="ts-kicker">មេរៀនទី {kh(n)}</p><h1>លំហាត់</h1><p class="ts-sub">{inline(title)}</p>'})
                body = text
                for blk in re.finditer(r'\\begin\{(enumerate|itemize)\}', body):
                    end = find_env_end(body, blk.end(), blk.group(1))
                    items = split_items(body[blk.end():end])
                    for qi, (lab, it) in enumerate(items, 1):
                        sm = re.search(r'\\begin\{solution\}', it)
                        if sm:
                            qtxt = it[:sm.start()]
                            send = find_env_end(it, sm.end(), 'solution')
                            stxt = it[sm.end():send]
                            after = it[send + len('\\end{solution}'):]
                            qtxt += after
                        else:
                            qtxt, stxt = it, ''
                        add('prac', f'លំហាត់ទី {kh(qi)}', parse_blocks(qtxt), kicker_of() or 'លំហាត់')
                        if stxt.strip():
                            add('sol', f'ដំណោះស្រាយ លំហាត់ទី {kh(qi)}', parse_blocks(stxt), 'ចម្លើយ')
                    break
                continue
            continue
        if mode == 'ex':
            continue
        if kind == 'subsection':
            flush_ex()
            sec, sub = ttl, ''
            slides.append({'k': 'title', 'html': f'<p class="ts-kicker">ផ្នែក</p><h1>{inline(ttl)}</h1>'})
            if text:
                add('', inline(ttl), parse_blocks(text), 'ផ្នែក')
            continue
        if kind == 'subsubsection':
            flush_ex()
            sub = ttl
            if text:
                add('', inline(ttl), parse_blocks(text), kicker_of())
            continue
        if kind == 'intro':
            if text and not re.match(r'^\s*$', text):
                add('key', 'គោលបំណង', parse_blocks(re.sub(r'^\\textbf\{[^}]*\}', '', text)), f'មេរៀនទី {kh(n)}')
            continue
        # a marked chunk
        c = classify(ttl)
        blocks = parse_blocks(text)
        if c == 'ex':
            if vis_len(''.join(blocks)) < MERGE_LIMIT:
                if sum(vis_len(''.join(b)) for _, b in pending_ex) + vis_len(''.join(blocks)) > MERGE_LIMIT * 1.4:
                    flush_ex()
                pending_ex.append((ttl, blocks))
                continue
            flush_ex()
            add('ex', inline(ttl), blocks, kicker_of())
            continue
        flush_ex()
        head = inline(ttl)
        add({'key': 'key', 'prac': 'prac', 'sol': 'sol'}[c], head, blocks or [''], kicker_of())
    flush_ex()
    slides.append({'k': 'title', 'html': f'<p class="ts-kicker">មេរៀនទី {kh(n)}</p><h1>ចប់មេរៀន</h1><p class="ts-sub">{inline(title)}</p>'})
    return title, slides


def parts_of(tex):
    return [re.sub(r'\s+', ' ', re.sub(r'^\s*[0-9០-៩]+\s*[\.\)]\s*', '', p)).strip() for p in re.findall(r'\\subsection\*?\{([^}]*)\}', tex)]


def main():
    decks, meta = {}, {}
    for n in range(1, 23):
        path = os.path.join(SRC, f'lesson{n}.tex')
        tex = open(path, encoding='utf8').read()
        title, slides = make_slides(n, tex)
        meta[n] = {'t': title, 'p': [p for p in parts_of(strip_comments(tex)) if p]}
        decks[f'7-{n}'] = slides
        print(f'lesson {n:2d}: {len(slides):3d} slides  {title}')
    os.makedirs(os.path.join(OUT, 'js/slides/g7'), exist_ok=True)
    for k, v in decks.items():
        n = k.split('-')[1]
        if n == '1':
            hp = os.path.join(OUT, 'js/slides/g7l01.js')
            head = ''.join(open(hp, encoding='utf8').read().split('\nwindow.TEACH_SLIDES')[0])
            open(hp, 'w', encoding='utf8').write(head + "\n\n// Slides generated by tools/make_g7_slides.py from Lesson/G7/lesson1.tex — do not edit by hand.\n"
                + "window.TEACH_SLIDES = window.TEACH_SLIDES || {};\n" + f"window.TEACH_SLIDES['7-1'] = {json.dumps(v, ensure_ascii=False)};\n")
            continue
        js = ('// Generated by tools/make_g7_slides.py from Lesson/G7/lesson%s.tex — do not edit by hand.\n' % n
              + "window.TEACH_SLIDES = window.TEACH_SLIDES || {};\n"
              + f"window.TEACH_SLIDES['{k}'] = {json.dumps(v, ensure_ascii=False)};\n")
        open(os.path.join(OUT, f'js/slides/g7/lesson{n}.js'), 'w', encoding='utf8').write(js)
    json.dump(meta, open(os.path.join(OUT, 'data/lessons_g7.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
