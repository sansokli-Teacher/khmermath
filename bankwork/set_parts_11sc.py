"""One-off: give the Grade 11 SC questions of lessons 3-8, 17, 26-28 their lesson PART in test_questions.topic.

    npx wrangler d1 execute exam-khmer --remote --json --command "SELECT id, lesson, topic, order_no, stem_text FROM test_questions WHERE grade='11SC' ..." > rows.json
    python3 set_parts_11sc.py rows.json            # writes out/g11sc_parts_update.sql and prints a per-part count
    npx wrangler d1 execute exam-khmer --remote --file out/g11sc_parts_update.sql

Lessons 3-8 and 17 are mapped from the question's sec tag (gen11sc/parts.py).  Lessons 26-28 carry fine-grained
free-text tags, so each question was classified by reading its stem; those ids are listed below.
Rollback: UPDATE test_questions SET topic = lesson WHERE grade='11SC' AND lesson IN (...)."""
import json, sys, collections, importlib
sys.path.insert(0, '.'); sys.path.insert(0, 'gen11sc')
from lib import norm, sepnum, sqlq
import parts

R = lambda *spans: [i for a, b in spans for i in range(a, b + 1)]

# ---- lesson 26 (ids 5034-5083): part 1 drawing, 2 basic properties, 3 positions -------------------------
P26 = {
    1: [5035, 5036, 5042, 5043],
    2: [5034, 5041, 5037, 5045, 5050, 5072, 5077, 5044, 5049, 5053, 5060, 5070, 5071,
        5047, 5052, 5055, 5057, 5061, 5063, 5064, 5074, 5075, 5078, 5065, 5066, 5079, 5082, 5083],
    3: [5038, 5039, 5040, 5046, 5048, 5051, 5054, 5056, 5058, 5059, 5062, 5073, 5076, 5067, 5068, 5069, 5080, 5081],
}
# ---- lesson 27 (ids 5084-5133): part 1 parallel lines, 2 line // plane, 3 parallel planes ---------------
P27 = {
    1: [5084, 5085, 5089, 5094, 5098, 5100, 5103, 5108, 5111, 5120, 5121, 5125, 5126, 5128],
    2: [5086, 5090, 5095, 5097, 5101, 5105, 5112, 5114, 5122, 5115, 5118],
    3: [5087, 5088, 5091, 5092, 5093, 5096, 5099, 5102, 5104, 5106, 5107, 5109, 5110, 5113, 5123, 5124, 5127,
        5116, 5117, 5119, 5129, 5130, 5131, 5132, 5133],
}
# ---- lesson 28 (ids 5134-5183): 7 parts ----------------------------------------------------------------
P28 = {
    1: [5139, 5142, 5146, 5147, 5154, 5155, 5156, 5158, 5163, 5164, 5169, 5172, 5176, 5182],
    2: [5134, 5148, 5157, 5160, 5177],
    3: [5135, 5140, 5143, 5144, 5145, 5149, 5159, 5165, 5166, 5170, 5171, 5175, 5178, 5179, 5183],
    4: [5136, 5150, 5173, 5180],
    5: [5137, 5162],
    6: [5151],
    7: [5138, 5141, 5152, 5153, 5161, 5167, 5168, 5174, 5181],
}
MANUAL = {26: (P26, R((5034, 5083))), 27: (P27, R((5084, 5133))), 28: (P28, R((5134, 5183)))}
for n, (pm, want) in MANUAL.items():
    got = sorted(i for v in pm.values() for i in v)
    assert got == want, (n, 'ids missing/duplicated', set(want) ^ set(got), len(got), len(want))

rows = json.load(open(sys.argv[1]))[0]['results']
by_lesson = collections.defaultdict(list)
for r in rows:
    by_lesson[r['lesson']].append(r)

sql, counts, problems = [], collections.Counter(), []
for n, (lname, titles) in sorted(parts.PARTS.items()):
    sub = by_lesson.get(lname, [])
    if not sub:
        problems.append(f'lesson {n} {lname}: no rows'); continue
    if n in MANUAL:
        id2part = {i: k for k, ids in MANUAL[n][0].items() for i in ids}
        for r in sub:
            k = id2part.get(r['id'])
            if k is None: problems.append(f'lesson {n}: id {r["id"]} has no part'); continue
            sql.append("UPDATE test_questions SET topic = %s WHERE id = %d AND grade = '11SC' AND lesson = %s;" % (sqlq(titles[k - 1]), r['id'], sqlq(lname)))
            counts[(n, titles[k - 1])] += 1
    else:
        m = importlib.import_module('G11L%02d' % n)
        sec = {norm(sepnum(c['stem'])): c['sec'] for c in m.cands()}
        for r in sub:
            s_ = sec.get(norm(r['stem_text']))
            if s_ is None: problems.append(f'lesson {n}: id {r["id"]} not matched'); continue
            t = parts.part_title(n, s_)
            sql.append("UPDATE test_questions SET topic = %s WHERE id = %d AND grade = '11SC' AND lesson = %s;" % (sqlq(t), r['id'], sqlq(lname)))
            counts[(n, t)] += 1

assert not problems, problems
open('out/g11sc_parts_update.sql', 'w', encoding='utf-8').write('\n'.join(sql) + '\n')
for n, (lname, titles) in sorted(parts.PARTS.items()):
    print(f'L{n:02d} {lname}')
    for t in titles:
        print(f'    {counts[(n, t)]:3d}  {t}')
print(len(sql), 'updates')
