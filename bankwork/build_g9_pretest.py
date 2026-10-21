"""Grade 9 pre-test (60 min) built from the Grade 8 bank snapshot (existing_g8_20261021.json) -> out/g9_pretest_from_g8.sql + out/g9_pretest_preview.md
30 MCQ (2 pts each, spread over all 19 Grade 8 lessons, 2 from the 11 lessons Grade 9 leans on most, easy/medium) + 2 writing (5 pts each).
Creates ONE ordinary (non-bank) draft test owned by the owner account, with copies of the chosen questions."""
import json
rows_all = json.load(open('existing_g8_20261021.json'))
ok = [r for r in rows_all if not r['image_key'] and not r['params'] and not r['cancelled']]
TWO = ['ចំនួនសនិទាន', 'ស្វ័យគុណ', 'កន្សោមពីជគណិត', 'កន្សោមសនិទាន', 'សមីការដឺក្រេទី ១ មានមួយអញ្ញាត', 'វិសមីការដឺក្រេទី ១ មានមួយអញ្ញាត',
       'ប្លង់កូអរដោនេនិងក្រាប', 'ទ្រឹស្តីបទពីតាក័រ', 'ចតុកោណ', 'រង្វង់', 'ទំហំសមាមាត្រនិងភាគរយ']
lessons = sorted({r['lesson'] for r in ok})
MCQ = []
for L in lessons:
    pool = sorted((r for r in ok if r['lesson'] == L and r['kind'] == 'mcq' and r['level'] in ('easy', 'medium')), key=lambda r: r['id'])
    mid = [r for r in pool if r['level'] == 'medium']; easy = [r for r in pool if r['level'] == 'easy']
    pick = ([easy[len(easy) // 2], mid[len(mid) // 2]] if L in TWO else [mid[len(mid) // 2]])
    MCQ += [r['id'] for r in pick]
assert len(MCQ) == 30, len(MCQ)
WRITING = [2872, 0]
pyth = [r for r in ok if r['kind'] == 'writing' and r['lesson'] == 'ទ្រឹស្តីបទពីតាក័រ' and r['level'] == 'medium']
WRITING[1] = pyth[len(pyth) // 2]['id']
TITLE = 'តេស្តបុរេ ថ្នាក់ទី៩ (ពីមេរៀនថ្នាក់ទី៨) — ៦០ នាទី'
by = {q['id']: q for q in ok}
rows = [dict(by[i]) for i in MCQ + WRITING]
for r in rows:
    if r['kind'] == 'mcq': r['points'] = 2      # 30 x 2 + 2 x 5 = 70
assert [r['kind'] for r in rows] == ['mcq'] * 30 + ['writing'] * 2
q = lambda s: 'NULL' if s is None else "'" + str(s).replace("'", "''") + "'"
sql = [f"INSERT INTO tests (title, status, owner_id, is_bank, is_sample) VALUES ({q(TITLE)}, 'draft', (SELECT id FROM teachers WHERE role = 'owner' ORDER BY id LIMIT 1), 0, 0);"]
for n, r in enumerate(rows, 1):
    sql.append("INSERT INTO test_questions (test_id, order_no, stem_text, image_key, options_json, correct_index, alt_correct_index, points, kind, solution_text, topic, level, shuffle, grade, lesson, params, cancelled) VALUES "
               f"((SELECT MAX(id) FROM tests WHERE title = {q(TITLE)}), {n}, {q(r['stem_text'])}, NULL, {q(r['options_json'])}, {r['correct_index']}, NULL, {r['points']}, {q(r['kind'])}, {q(r['solution_text'])}, {q(r['topic'])}, {q(r['level'])}, {r['shuffle']}, {q(r['grade'])}, {q(r['lesson'])}, NULL, 0);")
open('out/g9_pretest_from_g8.sql', 'w', encoding='utf-8').write('\n'.join(sql) + '\n')
mp = sum(r['points'] for r in rows if r['kind'] == 'mcq'); wp = sum(r['points'] for r in rows if r['kind'] == 'writing')
md = [f'# {TITLE}', f'MCQ {len(MCQ)} ({mp} pts) + writing {len(WRITING)} ({wp} pts) = {mp + wp} pts\n']
for n, r in enumerate(rows, 1):
    o = json.loads(r['options_json'])
    md.append(f"{n}. [{r['lesson']} · {r['level']} · {r['points']}pt · bank id {r['id']}] {r['stem_text']}")
    for i, t in enumerate(o): md.append(f"   - {'ABCD'[i]}{' ✔' if i == r['correct_index'] else ''}. {t}")
    if r['kind'] == 'writing': md.append('   - rubric: ' + (r['solution_text'] or '').replace('\n', ' / '))
open('out/g9_pretest_preview.md', 'w', encoding='utf-8').write('\n'.join(md) + '\n')
print(len(rows), 'questions', mp, wp, mp + wp)
