"""Suggested answer time for every game question (public/data/teamgame_g7.json) -> out/game_question_timers.csv + a printed summary.
time = reading + thinking/working + answering, x level factor + figure; then snapped to a few easy tiers."""
import json, re, csv, statistics as st, collections
d = json.load(open('../public/data/teamgame_g7.json'))
TIERS = [15, 20, 30, 45, 60, 90, 120, 150, 180]
LV = {'easy': 0.85, 'medium': 1.0, 'hard': 1.3, 'pisa': 1.5}
clean = lambda s: re.sub(r'\\(?:text|mathrm)\{([^}]*)\}', r'\1', re.sub(r'\\[()\[\]]', '', s or ''))
def steps(sol):
    s = sol or ''
    return s.count('=') + 0.5 * len(re.findall(r'\\(?:times|div|frac|sqrt|cdot|pm)|[+×÷]', s))
def suggest(q):
    qt = clean(q['q']); read = 0.09 * len(qt)
    mcq = bool(q.get('o'))
    if mcq: read += 0.05 * sum(len(clean(o)) for o in q['o'])
    n = steps(q.get('s'))
    work = 6 if n == 0 else 10 + 7 * min(n, 8)
    ans = 3 if mcq else 6
    t = (read + work + ans) * LV.get(q['lv'], 1.0) + (8 if q.get('f') else 0)
    t = max(15, min(180, t))
    return round(t), min(TIERS, key=lambda x: abs(x - t))
rows = []
for L in d['lessons']:
    for i, q in enumerate(L['qs']):
        raw, tier = suggest(q)
        rows.append({'lesson': L['n'], 'grade': L.get('g', 7), 'title': L['title'], 'i': i + 1, 'level': q['lv'], 'type': 'MCQ' if q.get('o') else 'OPEN', 'figure': int(bool(q.get('f'))), 'chars': len(clean(q['q'])), 'steps': steps(q.get('s')), 'raw_s': raw, 'suggest_s': tier, 'question': clean(q['q'])[:80]})
with open('out/game_question_timers.csv', 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(len(rows), 'questions')
c = collections.Counter(r['suggest_s'] for r in rows)
print('tiers:', {k: f"{c[k]} ({100*c[k]//len(rows)}%)" for k in sorted(c)})
for key in ('level', 'type'):
    g = collections.defaultdict(list)
    for r in rows: g[r[key]].append(r['suggest_s'])
    print(key, {k: f"{st.mean(v):.0f}s avg, median {st.median(v):.0f}, n={len(v)}" for k, v in g.items()})
g = collections.defaultdict(list)
for r in rows: g[r['grade']].append(r['suggest_s'])
print('grade', {k: f"{st.mean(v):.0f}s" for k, v in sorted(g.items())})
print('overall avg', round(st.mean(r['suggest_s'] for r in rows)), 'median', st.median(r['suggest_s'] for r in rows))
for t in (15, 30, 60, 120):
    ex = [r for r in rows if r['suggest_s'] == t][:2]
    for r in ex: print(f"  {t}s  [{r['level']}/{r['type']}/steps {r['steps']}] {r['question']}")
