"""Helpers to author Grade 7 question-bank questions with computed answers.
A candidate is a dict: kind 'mcq'|'writing', level 'easy|medium|hard|pisa', sec (section tag), stem, options (mcq: correct first, wrongs after), sol.
build.py picks candidates to fill each lesson to 50 (mcq/writing × level matrix) and writes SQL."""
import re, hashlib, random
from fractions import Fraction

def M(x): return '\\(' + str(x) + '\\)'
def D(x):  # display math inline for long expressions
    return '\\(' + str(x) + '\\)'

def num(n, dec=None):
    """1234567 -> 1\\,234\\,567 (the book writes thousands with a thin space), decimals keep their point."""
    if isinstance(n, Fraction):
        n = float(n)
    if isinstance(n, float) and n == int(n) and dec is None: n = int(n)
    s = (f'{n:.{dec}f}' if dec is not None else str(n))
    neg = s.startswith('-'); s = s.lstrip('-')
    ip, _, fp = s.partition('.')
    if len(ip) >= 4: ip = '\\,'.join([ip[max(0, i - 3):i] for i in range(len(ip), 0, -3)][::-1])
    return ('-' if neg else '') + ip + ('.' + fp if fp else '')

def frac(a, b=None):
    if b is None: f = Fraction(a)
    else: f = Fraction(a, b)
    if f.denominator == 1: return str(f.numerator)
    s = '-' if f < 0 else ''
    return f'{s}\\dfrac{{{abs(f.numerator)}}}{{{f.denominator}}}'

POINTS = {'easy': 1, 'medium': 2, 'hard': 3, 'pisa': 3}

def Q(kind, level, sec, stem, correct=None, wrongs=None, sol='', steps=None):
    """mcq: correct + 3 wrongs (strings, already LaTeX-wrapped).  writing: steps = [(text, points)] summing to 5."""
    d = dict(kind=kind, level=level, sec=sec, stem=stem.strip())
    if kind == 'mcq':
        assert correct is not None and wrongs and len(wrongs) >= 3, stem
        opts = [str(correct)] + [str(w) for w in wrongs]
        seen = []; 
        for o in opts:
            assert o not in seen, ('duplicate option', stem, opts); seen.append(o)
        d['options'] = opts[:4]; d['sol'] = sol
    else:
        assert steps and sum(p for _, p in steps) == 5, ('writing points must sum to 5', stem, steps)
        d['sol'] = '\n'.join(f'{t} ({p} ពិន្ទុ)' for t, p in steps)
    return d

def mcq(level, sec, stem, correct, wrongs, sol=''): return Q('mcq', level, sec, stem, correct, wrongs, sol)
def wr(level, sec, stem, steps): return Q('writing', level, sec, stem, steps=steps)

def norm(s): return re.sub(r'\s+', '', re.sub(r'\\[,; ]|\\text\{[^}]*\}', '', s or ''))

def place(cands_mcq_options, key):
    """deterministic shuffle: returns (options, correct_index)."""
    rnd = random.Random(int(hashlib.md5(key.encode()).hexdigest()[:8], 16))
    idx = list(range(len(cands_mcq_options))); rnd.shuffle(idx)
    opts = [cands_mcq_options[i] for i in idx]
    return opts, idx.index(0)

def sqlq(v):
    if v is None: return 'NULL'
    if isinstance(v, (int, float)): return str(v)
    return "'" + str(v).replace("'", "''") + "'"


_NUM = re.compile(r'(?<![\d.,\\])(\d{4,})(?![\d])')
def sepnum(txt):
    """inside \\( ... \\): 1234567 -> 1\\,234\\,567 ; decimals keep their fractional part untouched."""
    def fix_math(m):
        body = m.group(1)
        def num_rep(n):
            digits = n.group(1)
            # leave the fractional part of decimals alone (a digit run that follows a point)
            start = n.start(1)
            if start > 0 and body[start - 1] == '.': return digits
            return '\\,'.join([digits[max(0, i - 3):i] for i in range(len(digits), 0, -3)][::-1])
        return '\\(' + _NUM.sub(num_rep, body) + '\\)'
    return re.sub(r'\\\((.*?)\\\)', fix_math, txt, flags=re.S)

def wrongs_int(ans, cand, k=3, fmt=None):
    """k distinct wrong integers: first the sensible ones in `cand`, then ans±1, ±2, ... as filler."""
    fmt = fmt or (lambda x: M(x))
    out = []
    for c in list(cand) + [ans + d for d in (1, -1, 2, -2, 3, -3, 10, -10)]:
        if c != ans and c not in out: out.append(c)
        if len(out) == k: break
    return [fmt(x) for x in out]
