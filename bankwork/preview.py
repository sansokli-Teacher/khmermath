import re,sys,json
sql=open(sys.argv[1],encoding='utf-8').read()
import sqlite3
con=sqlite3.connect(':memory:')
con.execute("CREATE TABLE test_questions (id INTEGER PRIMARY KEY AUTOINCREMENT, test_id, order_no, stem_text, image_key, options_json, correct_index, alt_correct_index, points, kind, solution_text, topic, level, shuffle, grade, lesson, params, cancelled)")
con.executescript(sql)
for r in con.execute("select kind,level,stem_text,options_json,correct_index,solution_text from test_questions order by id"):
    k,l,st,oj,ci,sol=r; o=json.loads(oj)
    print(f"[{k[0]}/{l[0]}] {st}")
    if k=='mcq': print('   ',' | '.join(('*' if i==ci else '')+x for i,x in enumerate(o)))
    if sol: print('   sol:',sol.replace('\n',' / ')[:260])
