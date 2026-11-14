"""python3 build11sc_extra.py <d1_export.json>  ->  out/g11sc_extra_parts.sql

Adds gen11sc/extra_parts.py questions (topic = part title) so every Grade 11 SC lesson part has >= MIN questions.
<d1_export.json> = wrangler --json export of: SELECT id, lesson, topic, order_no, stem_text FROM test_questions WHERE grade='11SC'"""
import json, sys, collections, base64, hashlib, importlib
sys.path.insert(0, '.'); sys.path.insert(0, 'gen11sc')
from lib import norm, sepnum, sqlq, place, POINTS
import build11sc, extra_parts, parts

MIN = 10
START = {3: 13361, 4: 13461, 8: 13861, 26: 15661, 28: 15861}      # first free order_no after each lesson's block
rows = json.load(open(sys.argv[1]))[0]['results']
have = collections.Counter((r['lesson'], r['topic']) for r in rows)
seen = {norm(r['stem_text']) for r in rows}
used_orders = {r['order_no'] for r in rows}
sql, made, add = [], set(), collections.Counter()
for n, cs in extra_parts.cands().items():
    lname = parts.PARTS[n][0]
    mod = importlib.import_module('G11L%02d' % n)
    chapter = getattr(mod, 'CHAPTER', None) or build11sc.CHAPTER_MAP.get(lname)
    order = START[n]
    for c in cs:
        k = norm(sepnum(c['stem']))
        assert k not in seen, ('duplicate stem', c['stem'][:60]); seen.add(k)
        while order in used_orders: order += 1
        used_orders.add(order)
        stem = sepnum(c['stem']); sol = sepnum(c['sol'] or '')
        ikey = 'NULL'
        if c.get('img'):
            key = 'g11sc-' + hashlib.md5(c['img'].encode()).hexdigest()[:10] + '.svg'
            if key not in made:
                made.add(key)
                sql.append("INSERT OR REPLACE INTO images (key, content_type, data_base64, created_at) VALUES ('%s', 'image/svg+xml', '%s', datetime('now'));" % (key, base64.b64encode(c['img'].encode()).decode()))
            ikey = "'" + key + "'"
        if c['kind'] == 'mcq':
            options, ci = place([sepnum(o) for o in c['options']], stem)
            oj = json.dumps(options, ensure_ascii=False)
        else:
            ci, oj = 0, '[]'
        sql.append("INSERT INTO test_questions (test_id, order_no, stem_text, image_key, options_json, correct_index, alt_correct_index, points, kind, solution_text, topic, level, shuffle, grade, lesson, chapter, params, cancelled, bloom) VALUES (10, %d, %s, %s, %s, %d, NULL, %d, %s, %s, %s, %s, %d, '11SC', %s, %s, NULL, 0, %s);" % (
            order, sqlq(stem), ikey, sqlq(oj), ci, 5 if c['kind'] == 'writing' else POINTS[c['level']], sqlq(c['kind']), sqlq(sol or None),
            sqlq(c['part']), sqlq(c['level']), 1 if c['kind'] == 'mcq' else 0, sqlq(lname), sqlq(chapter), sqlq(c.get('bloom') or {'easy': 'Understand', 'medium': 'Apply', 'hard': 'Analyze', 'pisa': 'Evaluate'}[c['level']])))
        add[(lname, c['part'])] += 1
bad = []
for n, (lname, titles) in sorted(parts.PARTS.items()):
    print(f'L{n:02d} {lname}')
    for t in titles:
        tot = have[(lname, t)] + add[(lname, t)]
        print(f'   {have[(lname, t)]:3d} + {add[(lname, t)]:2d} = {tot:3d}  {t}')
        if tot < MIN: bad.append((lname, t, tot))
print('Lessons 1-2 parts unchanged (all >= 10).')
open('out/g11sc_extra_parts.sql', 'w', encoding='utf-8').write('\n'.join(sql) + '\n')
print(sum(add.values()), 'new questions;', len(made), 'images; wrote out/g11sc_extra_parts.sql')
assert not bad, ('parts still below %d' % MIN, bad)
