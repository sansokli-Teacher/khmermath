# -*- coding: utf-8 -*-
"""python3 gamebank_from_set.py G12L01 501 12 1  -> replaces lesson <n>=501 (grade 12, d=1) in public/data/teamgame_g7.json
with the MCQs of the gen12sc set that have NO image (the team game cannot show figures).
Same answer-position balancing idea as build12sc.py; only that lesson is touched, the file stays minified."""
import sys, json, importlib, random, hashlib, collections
sys.path.insert(0, '.')
name, n, g, d = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
mod = importlib.import_module('gen12sc.' + name)
TM = {'easy': 30, 'medium': 60, 'hard': 90, 'pisa': 90}
LV = {'easy': 'easy', 'medium': 'medium', 'hard': 'hard', 'pisa': 'hard'}
mc = [q for q in mod.cands() if q['kind'] == 'mcq' and not q.get('img')]
seq = [i % 4 for i in range(len(mc))]
random.Random(int(hashlib.md5(name.encode()).hexdigest()[:8], 16)).shuffle(seq)
out = []
for q, t in zip(mc, seq):
    rnd = random.Random(int(hashlib.md5((q['stem'] + '|g').encode()).hexdigest()[:8], 16))
    rest = list(range(1, 4)); rnd.shuffle(rest)
    order = rest[:t] + [0] + rest[t:]
    o = [q['options'][i] for i in order]
    out.append({'t': mod.TOPIC_MAP[q['sec']], 'q': q['stem'], 'lv': LV[q['level']], 'h': '', 's': q['sol'], 'o': o, 'a': q['options'][0], 'k': t, 'tm': TM[q['level']]})
for q in out:
    assert q['o'][q['k']] == q['a'] and len(set(q['o'])) == 4
path = 'public/data/teamgame_g7.json'
data = json.load(open(path, encoding='utf-8'))
cur = [l for l in data['lessons'] if l.get('n') == n and l.get('g') == g]
assert len(cur) <= 1, 'lesson found more than once'
if cur:
    title = cur[0]['title']
    new = dict(cur[0], q=out, qs=out)
    data['lessons'] = [new if (l.get('n') == n and l.get('g') == g) else l for l in data['lessons']]
else:                                    # a lesson that is not in the game bank yet: add it
    title = mod.LESSON
    data['lessons'].append({'n': n, 'g': g, 'd': d, 'title': title, 't': title, 'q': out, 'qs': out})
json.dump(data, open(path, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('lesson', n, title, ':', len(out), 'questions;', dict(collections.Counter(q['t'] for q in out)), '; positions', dict(sorted(collections.Counter(q['k'] for q in out).items())))
