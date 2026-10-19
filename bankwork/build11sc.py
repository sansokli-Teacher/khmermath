"""python3 build11sc.py [G11L01 ...]  → out/g11sc_new_<lessons>.sql (INSERTs) + a coverage report.
Each gen11sc/G11Lxx.py defines LESSON and cands() -> list of candidates (see lib.py)."""
import json, sys, importlib, collections, os
from lib import *

TARGET = {('mcq', 'easy'): 10, ('mcq', 'medium'): 14, ('mcq', 'hard'): 7, ('mcq', 'pisa'): 5,
          ('writing', 'easy'): 1, ('writing', 'medium'): 4, ('writing', 'hard'): 4, ('writing', 'pisa'): 5}
BASE_ORDER = 13000

CHAPTER_MAP = {
    # ជំពូកទី 1 : ស្វ៊ីតនិងអនុមានរួមគណិតវិទ្យា
    'ស្វ៊ីតចំនួនពិត': 'ជំពូកទី 1 : ស្វ៊ីតនិងអនុមានរួមគណិតវិទ្យា',
    'ស្វ៊ីតនព្វន្ត': 'ជំពូកទី 1 : ស្វ៊ីតនិងអនុមានរួមគណិតវិទ្យា',
    'ស្វ៊ីតធរណីមាត្រ': 'ជំពូកទី 1 : ស្វ៊ីតនិងអនុមានរួមគណិតវិទ្យា',
    'ផលបូកតួនៃស្វ៊ីតផ្សេងៗ': 'ជំពូកទី 1 : ស្វ៊ីតនិងអនុមានរួមគណិតវិទ្យា',
    'ទំនាក់ទំនងតួនៃស្វ៊ីត': 'ជំពូកទី 1 : ស្វ៊ីតនិងអនុមានរួមគណិតវិទ្យា',
    'វិធានអនុមានរួមគណិតវិទ្យា': 'ជំពូកទី 1 : ស្វ៊ីតនិងអនុមានរួមគណិតវិទ្យា',

    # ជំពូកទី 2 : អនុគមន៍អិចស្ប៉ូណង់ស្យែលនិងអនុគមន៍លោការីត
    'អនុគមន៍អិចស្ប៉ូណង់ស្យែល': 'ជំពូកទី 2 : អនុគមន៍អិចស្ប៉ូណង់ស្យែលនិងអនុគមន៍លោការីត',
    'អនុគមន៍លោការីត': 'ជំពូកទី 2 : អនុគមន៍អិចស្ប៉ូណង់ស្យែលនិងអនុគមន៍លោការីត',

    # ជំពូកទី 3 : អនុគមន៍ត្រីកោណមាត្រ
    'អនុគមន៍ត្រីកោណមាត្រ': 'ជំពូកទី 3 : អនុគមន៍ត្រីកោណមាត្រ',
    'រូបមន្តត្រីកោណមាត្រ': 'ជំពូកទី 3 : អនុគមន៍ត្រីកោណមាត្រ',
    'អនុគមន៍ច្រាសនៃអនុគមន៍ត្រីកោណមាត្រ': 'ជំពូកទី 3 : អនុគមន៍ត្រីកោណមាត្រ',
    'សមីការនិងវិសមីការត្រីកោណមាត្រ': 'ជំពូកទី 3 : អនុគមន៍ត្រីកោណមាត្រ',
    'សមីការនិងវិសមីការត្រីកោណមាត្រផ្សេងទៀត': 'ជំពូកទី 3 : អនុគមន៍ត្រីកោណមាត្រ',

    # ជំពូកទី 4 : ម៉ាទ្រីស ដេទែរមីណង់ និងបំប្លែងលីនេអ៊ែរ
    'ម៉ាទ្រីស': 'ជំពូកទី 4 : ម៉ាទ្រីស ដេទែរមីណង់ និងបំប្លែងលីនេអ៊ែរ',
    'ដេទែរមីណង់': 'ជំពូកទី 4 : ម៉ាទ្រីស ដេទែរមីណង់ និងបំប្លែងលីនេអ៊ែរ',
    'ការបំប្លែងលីនេអ៊ែរ': 'ជំពូកទី 4 : ម៉ាទ្រីស ដេទែរមីណង់ និងបំប្លែងលីនេអ៊ែរ',

    # ជំពូកទី 5 : លីមីតនិងដេរីវេ
    'លីមីតនិងដេរីវេ': 'ជំពូកទី 5 : លីមីតនិងដេរីវេ',
    'អនុវត្តនៃដេរីវេ': 'ជំពូកទី 5 : លីមីតនិងដេរីវេ',
    'អថេរភាពនិងក្រាបនៃអនុគមន៍': 'ជំពូកទី 5 : លីមីតនិងដេរីវេ',
    'អនុវត្តន៍ដេរីវេចំពោះសមីការនិងវិសមីការ': 'ជំពូកទី 5 : លីមីតនិងដេរីវេ',

    # ជំពូកទី 6 : ចម្ងាស់ បន្សំ និងប្រូបាប
    'ចម្ងាស់': 'ជំពូកទី 6 : ចម្ងាស់ បន្សំ និងប្រូបាប',
    'បន្សំ': 'ជំពូកទី 6 : ចម្ងាស់ បន្សំ និងប្រូបាប',
    'ប្រូបាប': 'ជំពូកទី 6 : ចម្ងាស់ បន្សំ និងប្រូបាប',

    # ជំពូកទី 7 : ស្ថិតិ
    'រង្វាស់ទីតាំងនៃទិន្នន័យ': 'ជំពូកទី 7 : ស្ថិតិ',
    'រង្វាស់នៃគម្លាត': 'ជំពូកទី 7 : ស្ថិតិ',

    # ជំពូកទី 8 : ធរណីមាត្រក្នុងលំហ
    'រូបធរណីមាត្រក្នុងលំហ': 'ជំពូកទី 8 : ធរណីមាត្រក្នុងលំហ',
    'បន្ទាត់និងប្លង់ស្របក្នុងលំហ': 'ជំពូកទី 8 : ធរណីមាត្រក្នុងលំហ',
    'ភាពអរតូកូណាល់ក្នុងលំហ': 'ជំពូកទី 8 : ធរណីមាត្រក្នុងលំហ',
    'តម្រង់ទិស': 'តម្រង់ទិសសិស្ស NGS ២០២៦-២០២៧',
    'បទបញ្ជាផ្ទៃក្នុង': 'តម្រង់ទិសសិស្ស NGS ២០២៦-២០២៧',
}

existing = []

def cells(lesson):
    c = collections.Counter((q['kind'], q['level']) for q in existing if q.get('lesson') == lesson)
    return c

def main(names):
    order = BASE_ORDER
    sql = []; report = []; made = set()
    os.makedirs('out', exist_ok=True)
    for nm in names:
        mod = importlib.import_module('gen11sc.' + nm)
        # Parse lesson number from name, e.g. G11L01 -> 1
        les_idx = int(nm.split('L')[-1]) if 'L' in nm else 1
        order = BASE_ORDER + les_idx * 100
        lesson = mod.LESSON
        target = getattr(mod, 'TARGET', TARGET)
        grade = getattr(mod, 'GRADE', '11SC')
        have = cells(lesson); total_have = sum(have.values())
        cands = mod.cands()
        seen = {norm(q['stem_text']) for q in existing if q.get('lesson') == lesson}
        pool = collections.defaultdict(list)
        for c in cands:
            k = norm(c['stem'])
            if k in seen:
                report.append(f'{nm}: duplicate stem skipped: {c["stem"][:50]}')
                continue
            seen.add(k)
            pool[(c['kind'], c['level'])].append(c)
        picked = []
        for cell, tgt in target.items():
            need = max(0, tgt - have.get(cell, 0))
            if total_have >= 50:
                need = 0
            lst = pool.get(cell, [])
            bysec = collections.defaultdict(list)
            for c in lst:
                bysec[c['sec']].append(c)
            got = []
            while len(got) < need and any(bysec.values()):
                for s in list(bysec):
                    if bysec[s] and len(got) < need:
                        got.append(bysec[s].pop(0))
            if len(got) < need:
                report.append(f'{nm}: SHORT {cell}: need {need}, have {len(got)} (candidates {len(lst)})')
            picked += got
        for c in picked:
            c['stem'] = sepnum(c['stem'])
            c['sol'] = sepnum(c['sol'] or '')
            if c['kind'] == 'mcq':
                c['options'] = [sepnum(o) for o in c['options']]
            order += 1
            ikey = 'NULL'
            if c.get('img'):
                import base64, hashlib as _h
                k = 'g11sc-' + _h.md5(c['img'].encode()).hexdigest()[:10] + '.svg'
                if k not in made:
                    made.add(k)
                    sql.append("INSERT OR REPLACE INTO images (key, content_type, data_base64, created_at) VALUES ('%s', 'image/svg+xml', '%s', datetime('now'));" % (k, base64.b64encode(c['img'].encode()).decode()))
                ikey = "'" + k + "'"
            if c['kind'] == 'mcq':
                opts, ci = place(c['options'], c['stem'])
                oj = json.dumps(opts, ensure_ascii=False)
            else:
                opts, ci, oj = [], 0, '[]'
            chapter = getattr(mod, 'CHAPTER', None) or CHAPTER_MAP.get(lesson)
            sql.append("INSERT INTO test_questions (test_id, order_no, stem_text, image_key, options_json, correct_index, alt_correct_index, points, kind, solution_text, topic, level, shuffle, grade, lesson, chapter, params, cancelled) VALUES (10, %d, %s, %s, %s, %d, NULL, %s, %s, %s, %s, %s, %d, %s, %s, %s, NULL, 0);" % (
                order, sqlq(c['stem']), ikey, sqlq(oj), ci, 5 if c['kind'] == 'writing' else POINTS[c['level']], sqlq(c['kind']), sqlq(c['sol'] or None), sqlq(lesson), sqlq(c['level']), 1 if c['kind'] == 'mcq' else 0, sqlq(grade), sqlq(lesson), sqlq(chapter)))
        report.append(f'{nm} {lesson}: had {total_have}, adding {len(picked)} -> {total_have + len(picked)}')
        have2 = have + collections.Counter((c['kind'], c['level']) for c in picked)
        report.append('   final cells: ' + ', '.join(f'{k[0][0]}/{k[1][0]}={v}' for k, v in sorted(have2.items())))
    out = 'out/g11sc_new_' + '_'.join(names) + '.sql'
    open(out, 'w', encoding='utf-8').write('\n'.join(sql) + '\n')
    print('\n'.join(report))
    print('wrote', out, len(sql), 'rows')

if __name__ == '__main__':
    main(sys.argv[1:])
