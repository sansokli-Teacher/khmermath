"""Repairs the math in the static game bank (public/data/teamgame_g7.json):
 0. an escaped prime (M\\') is a plain prime (M') — KaTeX rejects the escaped one;
 1. control characters left by lost backslashes (\\a \\b \\t \\v \\f: \\alpha, \\bar, \\tan, \\text, \\times, \\frac ...) are turned back into the backslash + letter;
 2. solutions that write math without \\( \\) (e.g. "\\sin A = \\dfrac{a}{c}") get their math runs wrapped, so the teacher does not see raw code.
Idempotent: run it again and nothing changes."""
import json, re, sys, os
P = os.path.join(os.path.dirname(__file__), '..', 'public', 'data', 'teamgame_g7.json')
CTL = {'\x07': '\\a', '\x08': '\\b', '\x09': '\\t', '\x0b': '\\v', '\x0c': '\\f', '\x0d': '\\r'}
fix_ctl = lambda s: re.sub("\\\\'", "'", re.sub('[\x07\x08\x09\x0b\x0c\x0d]', lambda m: CTL[m.group(0)], s)) if isinstance(s, str) else s
# a run of math: LaTeX commands, \text{...} groups (may hold Khmer), and plain ASCII math characters
RUN = re.compile(r'(?:\\text\{[^{}]*\}|\\[A-Za-z]+|[A-Za-z0-9\s{}^_=+\-*/().,|<>!\'&:;\[\]%])+')
DELIM = re.compile(r'(\\\(.*?\\\)|\\\[.*?\\\])', re.S)
def wrap_bare(s):
    if not isinstance(s, str): return s
    out = []
    for part in DELIM.split(s):
        if DELIM.fullmatch(part) or not re.search(r'\\[A-Za-z]+', part):
            out.append(part); continue
        def rep(m):
            run = m.group(0)
            if not re.search(r'\\[A-Za-z]+', run): return run
            lead = len(run) - len(run.lstrip()); trail = len(run) - len(run.rstrip())
            core = run.strip()
            return run[:lead] + '\\(' + core + '\\)' + (run[len(run) - trail:] if trail else '')
        out.append(RUN.sub(rep, part))
    return ''.join(out)
# one solution mixes Khmer subscripts into bare math; it is written out by hand
SPECIAL = {(326, 19): 'ផលធៀបក្រឡាផ្ទៃ៖ \\(S_{\\text{ពិត}} = S_{\\text{ប្លង់}} \\times 100^2 = 30 \\times 10000\\text{ cm}^2 = 300000\\text{ cm}^2 = 30\\text{ m}^2\\) (ព្រោះ \\(1\\text{ m}^2 = 10000\\text{ cm}^2\\))។'}
d = json.load(open(P, encoding='utf-8'))
n_ctl = n_wrap = 0
for L in d['lessons']:
    for qi, q in enumerate(L['qs']):
        for f in ('q', 'a', 's', 'h', 't'):
            if f in q:
                v = fix_ctl(q[f])
                if f == 's' and (L['n'], qi) in SPECIAL and 'S_{ពិត}' in v: v = SPECIAL[(L['n'], qi)]
                if v != q[f]: n_ctl += 1
                if f == 's':
                    w = wrap_bare(v)
                    if w != v: n_wrap += 1
                    v = w
                q[f] = v
        if q.get('o'):
            new = [fix_ctl(o) for o in q['o']]
            if new != q['o']: n_ctl += 1
            q['o'] = new
json.dump(d, open(P, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('control characters repaired in', n_ctl, 'fields; solutions wrapped:', n_wrap)
