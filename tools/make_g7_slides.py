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
    slides.append({'k': 'title', 'html': f'<p class="ts-kicker">ថ្នាក់ទី ៧ · មេរៀនទី {kh(n)}</p><h1>{inline(title)}</h1>'})

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
            slides.append({'k': 'title', 'html': f'<h1>{inline(ttl)}</h1>'})
            if text:
                add('', inline(ttl), parse_blocks(text), '')
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
    # cover slide = lesson title + objectives
    if len(slides) > 1 and '<h2>គោលបំណង</h2>' in slides[1]['html']:
        obj = re.sub(r'^.*?<h2>គោលបំណង</h2>', '', slides[1]['html'], flags=re.S)
        slides[0]['html'] += '<div class="ts-obj"><h3>គោលបំណង</h3>' + obj + '</div>'
        slides[0]['c'] = 'cover'
        del slides[1]
    return title, slides


def split_734(slides):
    """Lesson 2, practice 734□0: the answer was auto-split mid-list (1/2, 2/2); it is now one slide per part, ក. (divisible by 4) and ខ. (by 8)."""
    at = next((k for k, s in enumerate(slides) if s['k'] == 'sol' and '734' in s['html'] and '(១/២)' in s['html']), None)
    if at is None or at + 1 >= len(slides):
        return slides
    kick = slides[at]['html'].split('</p>')[0] + '</p>'
    sl = lambda head, body: {'k': 'sol', 'html': f'{kick}<h2>{head}</h2>' + body}
    a = (r'<p><b>ក. ចែកដាច់នឹង \(4\)</b></p>'
         r'<p>មួយចំនួនចែកដាច់នឹង \(4\) កាលណាពីរខ្ទង់ចុងក្រោយចែកដាច់នឹង \(4\) ។ ពីរខ្ទង់ចុងក្រោយនៃ \(734\square 0\) គឺ \(\square 0\) ។</p>'
         r'<ul class="ts-bullets"><li>\(00 \div 4 = 0\) (ចែកដាច់) \(\implies \square = 0\)</li><li>\(20 \div 4 = 5\) (ចែកដាច់) \(\implies \square = 2\)</li>'
         r'<li>\(40 \div 4 = 10\) (ចែកដាច់) \(\implies \square = 4\)</li><li>\(60 \div 4 = 15\) (ចែកដាច់) \(\implies \square = 6\)</li>'
         r'<li>\(80 \div 4 = 20\) (ចែកដាច់) \(\implies \square = 8\)</li></ul>'
         r'<p>ដូចនេះ លេខក្នុងប្រអប់អាចជា ៖ \(0, 2, 4, 6, 8\) ។</p>')
    b = (r'<p><b>ខ. ចែកដាច់នឹង \(8\)</b></p>'
         r'<p>មួយចំនួនចែកដាច់នឹង \(8\) កាលណាបីខ្ទង់ចុងក្រោយចែកដាច់នឹង \(8\) ។ បីខ្ទង់ចុងក្រោយនៃ \(734\square 0\) គឺ \(4\square 0\) ។ យើងពិនិត្យលេខគូដែលរកឃើញក្នុងសំណួរ ក. ៖</p>'
         r'<ul class="ts-bullets"><li>បើ \(\square = 0\) ៖ \(400 \div 8 = 50\) (ចែកដាច់)</li><li>បើ \(\square = 2\) ៖ \(420 \div 8 = 52.5\) (ចែកមិនដាច់)</li>'
         r'<li>បើ \(\square = 4\) ៖ \(440 \div 8 = 55\) (ចែកដាច់)</li><li>បើ \(\square = 6\) ៖ \(460 \div 8 = 57.5\) (ចែកមិនដាច់)</li>'
         r'<li>បើ \(\square = 8\) ៖ \(480 \div 8 = 60\) (ចែកដាច់)</li></ul>'
         r'<p>ដូចនេះ លេខក្នុងប្រអប់អាចជា ៖ \(0, 4, 8\) ។</p>')
    return slides[:at] + [sl('ចម្លើយ ក.', a), sl('ចម្លើយ ខ.', b)] + slides[at + 2:]


def add_div7(slides):
    """Lesson 2: the divisibility-by-7 rule (it is in the teacher's own 'Properties of Numbers' deck but not in the book). It goes after
    1.3 (4 and 8), as 1.4, so the book's 1.4 (sums and differences) becomes 1.5. Hand-written slides, same layout as the generated ones."""
    OLD, NEW = '1.4. លក្ខណៈចែកដាច់នៃផលបូកនិងផលដក', '1.5. លក្ខណៈចែកដាច់នៃផលបូកនិងផលដក'
    at = next((k for k, s in enumerate(slides) if OLD in s['html']), None)
    if at is None:
        return slides
    K = '1. លក្ខណៈចែកដាច់នៃចំនួនគត់ · 1.4. ភាពចែកដាច់នឹង 7'
    sl = lambda kind, head, body: {'k': kind, 'html': f'<p class="ts-kicker">{K}</p><h2>{head}</h2>' + body}
    ex = (r'<p class="ts-exh">ឧទាហរណ៍ 1</p><p>\(119 = 7\times 17\), \(203 = 7\times 29\), \(343 = 7\times 49\) ។ គេសង្កេតឃើញថា</p>'
          r'<ul class="ts-bullets">'
          r'<li>\(119\) ចែកដាច់នឹង \(7\) ហើយ \(11 - 2\times 9 = -7\) ចែកដាច់នឹង \(7\) ។</li>'
          r'<li>\(203\) ចែកដាច់នឹង \(7\) ហើយ \(20 - 2\times 3 = 14\) ចែកដាច់នឹង \(7\) ។</li>'
          r'<li>\(343\) ចែកដាច់នឹង \(7\) ហើយ \(34 - 2\times 3 = 28\) ចែកដាច់នឹង \(7\) ។</li></ul>'
          r'<p class="ts-exh">ឧទាហរណ៍ 2</p><p>\(205\) មិនចែកដាច់នឹង \(7\) ហើយ \(20 - 2\times 5 = 10\) ក៏មិនចែកដាច់នឹង \(7\) ដែរ ។</p>')
    key = (r'<ol class="ts-bullets"><li>មួយចំនួនគត់ចែកដាច់នឹង \(7\) កាលណាផលដកនៃចំនួនដែលនៅសល់ (ក្រោយដកខ្ទង់ចុងក្រោយចេញ) '
           r'និងពីរដងនៃខ្ទង់ចុងក្រោយ ចែកដាច់នឹង \(7\) ។</li>'
           r'<li>ចំពោះ \(N = 10a + b\) (\(b\) ជាខ្ទង់ចុងក្រោយ) ៖ \(N\) ចែកដាច់នឹង \(7\) កាលណា \(a - 2b\) ចែកដាច់នឹង \(7\) ។</li>'
           r'<li>បើចំនួនដែលបានមកនៅធំ គេអាចអនុវត្តវិធីនេះម្តងទៀតលើវា ។</li></ol>')
    prac1 = r'<p>តើចំនួនណាខាងក្រោមចែកដាច់នឹង \(7\) ?</p><p>ក. \(252\) ខ. \(385\) គ. \(1001\) ឃ. \(2025\) ។</p>'
    sol1 = (r'<ul class="ts-bullets">'
            r'<li>ក. \(25 - 2\times 2 = 21\) ចែកដាច់នឹង \(7\) ដូច្នេះ \(252\) ចែកដាច់នឹង \(7\) ។</li>'
            r'<li>ខ. \(38 - 2\times 5 = 28\) ចែកដាច់នឹង \(7\) ដូច្នេះ \(385\) ចែកដាច់នឹង \(7\) ។</li>'
            r'<li>គ. \(100 - 2\times 1 = 98\) រួច \(9 - 2\times 8 = -7\) ចែកដាច់នឹង \(7\) ដូច្នេះ \(1001\) ចែកដាច់នឹង \(7\) ។</li>'
            r'<li>ឃ. \(202 - 2\times 5 = 192\) រួច \(19 - 2\times 2 = 15\) មិនចែកដាច់នឹង \(7\) ដូច្នេះ \(2025\) មិនចែកដាច់នឹង \(7\) ។</li></ul>')
    prac2 = r'<p>ចូររកលេខក្នុងប្រអប់ ដើម្បីឱ្យចំនួន \(4\square 6\) ចែកដាច់នឹង \(7\) ។</p>'
    sol2 = (r'<p>ចំនួន \(4\square 6\) មាន \(a = 40+\square\) និង \(b = 6\) ។ គេបាន \(a - 2b = 40+\square - 12 = 28+\square\) ។</p>'
            r'<p>ដើម្បីឱ្យ \(28+\square\) ចែកដាច់នឹង \(7\) ហើយ \(28\) ចែកដាច់នឹង \(7\) នោះ \(\square\) ត្រូវចែកដាច់នឹង \(7\) ដែរ ។ ដូច្នេះ \(\square = 0\) ឬ \(\square = 7\) ។</p>'
            r'<p>ចម្លើយ ៖ \(406 = 7\times 58\) និង \(476 = 7\times 68\) ។</p>')
    new = [sl('ex', 'ឧទាហរណ៍', ex), sl('key', 'ជាទូទៅ', key), sl('prac', 'លំហាត់គំរូ', prac1), sl('sol', 'ដំណោះស្រាយ', sol1),
           sl('prac', 'ប្រតិបត្តិ', prac2), sl('sol', 'ចម្លើយ', sol2)]
    out = slides[:at] + new + slides[at:]
    for s in out:
        s['html'] = s['html'].replace(OLD, NEW)
    if out and '2, 3, 4, 5, 8, 9' in out[0]['html']:
        out[0]['html'] = out[0]['html'].replace('2, 3, 4, 5, 8, 9', '2, 3, 4, 5, 7, 8, 9')
    return out


def parts_of(tex):
    return [re.sub(r'\s+', ' ', re.sub(r'^\s*[0-9០-៩]+\s*[\.\)]\s*', '', p)).strip() for p in re.findall(r'\\subsection\*?\{([^}]*)\}', tex)]


def main():
    decks, meta = {}, {}
    for n in range(1, 23):
        path = os.path.join(SRC, f'lesson{n}.tex')
        tex = open(path, encoding='utf8').read()
        title, slides = make_slides(n, tex)
        meta[n] = {'t': title, 'p': [p for p in parts_of(strip_comments(tex)) if p]}
        if n in (2, 3, 12):
            meta[n]['p'].append('លំហាត់')   # Lessons 2, 3 and 12 are hand-designed (tools/lesson2, lesson3, lesson12); the last part is the exercises
        decks[f'7-{n}'] = slides
        print(f'lesson {n:2d}: {len(slides):3d} slides  {title}')
    os.makedirs(os.path.join(OUT, 'js/slides/g7'), exist_ok=True)
    for k, v in decks.items():
        n = k.split('-')[1]
        if n in ('1', '2', '3', '12'):
            continue  # lessons 1-3 and 12 are hand-designed: tools/lesson1/build.py, tools/lesson2/build.py, tools/lesson3/build.py, tools/lesson12/build.py
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
