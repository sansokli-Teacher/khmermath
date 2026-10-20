"""Grade 8 pre-test (60 min) built from the Grade 7 bank snapshot -> out/g8_pretest_from_g7.sql + out/g8_pretest_preview.md
Creates ONE ordinary (non-bank) test owned by the owner account, with copies of the chosen questions."""
import json
MCQ = [224, 239, 237, 481, 483, 576, 577, 1758, 504, 506, 1828, 1831, 1676, 1680, 553, 334, 300, 358, 382, 432]
WRITING = [567, 1744, 1904, 592, 394]
TITLE = 'តេស្តបុរេ ថ្នាក់ទី៨ (ពីមេរៀនថ្នាក់ទី៧) — ៦០ នាទី'
by = {q['id']: q for q in json.load(open('existing_g7_20261015.json'))}
rows = [by[i] for i in MCQ + WRITING]
assert all(not r['image_key'] and not r['params'] and not r['cancelled'] for r in rows)
for r in rows:
    if r['kind'] == 'mcq': r['points'] = 2      # every MCQ 2 pts -> 40 + 5x5 = 65
assert [r['kind'] for r in rows] == ['mcq'] * len(MCQ) + ['writing'] * len(WRITING)
q = lambda s: 'NULL' if s is None else "'" + str(s).replace("'", "''") + "'"
sql = [f"INSERT INTO tests (title, status, owner_id, is_bank, is_sample) VALUES ({q(TITLE)}, 'draft', (SELECT id FROM teachers WHERE role = 'owner' ORDER BY id LIMIT 1), 0, 0);"]
for n, r in enumerate(rows, 1):
    sql.append("INSERT INTO test_questions (test_id, order_no, stem_text, image_key, options_json, correct_index, alt_correct_index, points, kind, solution_text, topic, level, shuffle, grade, lesson, params, cancelled) VALUES "
               f"((SELECT MAX(id) FROM tests WHERE title = {q(TITLE)}), {n}, {q(r['stem_text'])}, NULL, {q(r['options_json'])}, {r['correct_index']}, NULL, {r['points']}, {q(r['kind'])}, {q(r['solution_text'])}, {q(r['topic'])}, {q(r['level'])}, {r['shuffle']}, {q(r['grade'])}, {q(r['lesson'])}, NULL, 0);")
open('out/g8_pretest_from_g7.sql', 'w', encoding='utf-8').write('\n'.join(sql) + '\n')
mp = sum(r['points'] for r in rows if r['kind'] == 'mcq'); wp = sum(r['points'] for r in rows if r['kind'] == 'writing')
md = [f'# {TITLE}', f'MCQ {len(MCQ)} ({mp} pts) + writing {len(WRITING)} ({wp} pts) = {mp + wp} pts\n']
for n, r in enumerate(rows, 1):
    o = json.loads(r['options_json'])
    md.append(f"{n}. [{r['lesson']} · {r['level']} · {r['points']}pt · bank id {r['id']}] {r['stem_text']}")
    for i, t in enumerate(o): md.append(f"   - {'ABCD'[i]}{' ✔' if i == r['correct_index'] else ''}. {t}")
    if r['kind'] == 'writing': md.append('   - rubric: ' + (r['solution_text'] or '').replace('\n', ' / '))
open('out/g8_pretest_preview.md', 'w', encoding='utf-8').write('\n'.join(md) + '\n')
print(len(rows), 'questions', mp, wp, mp + wp)
