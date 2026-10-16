"""python3 build.py [L01 L02 ...]  → out/g8_new_<lessons>.sql (INSERTs) + a coverage report.
Each gen/Lxx.py defines LESSON (exact lesson name in the bank) and cands() -> list of candidates (see lib.py)."""
import json, sys, importlib, collections
from lib import *

TARGET = {('mcq', 'easy'): 10, ('mcq', 'medium'): 14, ('mcq', 'hard'): 7, ('mcq', 'pisa'): 5,
          ('writing', 'easy'): 1, ('writing', 'medium'): 4, ('writing', 'hard'): 4, ('writing', 'pisa'): 5}
BASE_ORDER = 7900      # grade 8 rows start well above the grade 7 / 9 ones (max order_no 3876 when this started)
existing = [q for q in json.load(open('existing_g8_none.json')) if not q['cancelled']]

def cells(lesson):
    c = collections.Counter((q['kind'], q['level']) for q in existing if q['lesson'] == lesson)
    return c

def main(names):
    order = BASE_ORDER
    sql = []; report = []; made = set()
    for nm in names:
        mod = importlib.import_module('gen8.' + nm)
        order = BASE_ORDER + int(nm[3:]) * 100
        lesson = mod.LESSON
        have = cells(lesson); total_have = sum(have.values())
        cands = mod.cands()
        seen = {norm(q['stem_text']) for q in existing if q['lesson'] == lesson}
        pool = collections.defaultdict(list)
        for c in cands:
            k = norm(c['stem'])
            if k in seen: report.append(f'{nm}: duplicate stem skipped: {c["stem"][:50]}'); continue
            seen.add(k); pool[(c['kind'], c['level'])].append(c)
        picked = []
        for cell, tgt in TARGET.items():
            need = max(0, tgt - have.get(cell, 0))
            if total_have >= 50: need = 0
            lst = pool.get(cell, [])
            bysec = collections.defaultdict(list)
            for c in lst: bysec[c['sec']].append(c)
            got = []
            while len(got) < need and any(bysec.values()):
                for s in list(bysec):
                    if bysec[s] and len(got) < need: got.append(bysec[s].pop(0))
            if len(got) < need: report.append(f'{nm}: SHORT {cell}: need {need}, have {len(got)} (candidates {len(lst)})')
            picked += got
        for c in picked:
            c['stem'] = sepnum(c['stem']); c['sol'] = sepnum(c['sol'] or '')
            if c['kind'] == 'mcq': c['options'] = [sepnum(o) for o in c['options']]
            order += 1
            ikey = 'NULL'
            if c.get('img'):
                import base64, hashlib as _h
                k = 'g8-' + _h.md5(c['img'].encode()).hexdigest()[:10] + '.svg'
                if k not in made:
                    made.add(k)
                    sql.append("INSERT OR REPLACE INTO images (key, content_type, data_base64, created_at) VALUES ('%s', 'image/svg+xml', '%s', datetime('now'));" % (k, base64.b64encode(c['img'].encode()).decode()))
                ikey = "'" + k + "'"
            if c['kind'] == 'mcq':
                opts, ci = place(c['options'], c['stem'])
                oj = json.dumps(opts, ensure_ascii=False)
            else:
                opts, ci, oj = [], 0, '[]'
            sql.append("INSERT INTO test_questions (test_id, order_no, stem_text, image_key, options_json, correct_index, alt_correct_index, points, kind, solution_text, topic, level, shuffle, grade, lesson, params, cancelled) VALUES (10, %d, %s, %s, %s, %d, NULL, %s, %s, %s, %s, %s, %d, '8', %s, NULL, 0);" % (
                order, sqlq(c['stem']), ikey, sqlq(oj), ci, 5 if c['kind'] == 'writing' else POINTS[c['level']], sqlq(c['kind']), sqlq(c['sol'] or None), sqlq(lesson), sqlq(c['level']), 1 if c['kind'] == 'mcq' else 0, sqlq(lesson)))
        report.append(f'{nm} {lesson}: had {total_have}, adding {len(picked)} -> {total_have + len(picked)}')
        have2 = have + collections.Counter((c['kind'], c['level']) for c in picked)
        report.append('   final cells: ' + ', '.join(f'{k[0][0]}/{k[1][0]}={v}' for k, v in sorted(have2.items())))
    out = 'out/g8_new_' + '_'.join(names) + '.sql'
    open(out, 'w', encoding='utf-8').write('\n'.join(sql) + '\n')
    print('\n'.join(report)); print('wrote', out, len(sql), 'rows')

if __name__ == '__main__':
    main(sys.argv[1:])
