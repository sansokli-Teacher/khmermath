#!/usr/bin/env python3
"""List the geometric constructions of khmermath.org/construct for the student page.
Reads ../KhmerMath_Site/site/construct/*.html (the built site), writes public/data/construct_index.json:
  { "base": "https://khmermath.org/construct/",
    "lessons": { "7": { "12": [ {"f": "g7-l12-measure.html", "t": "វាស់អង្កត់ដោយបន្ទាត់"}, ... ] }, "8": {...}, "9": {...} },
    "general": [ {"f": "board.html", "t": "ក្ដារខៀនធរណីមាត្រ"}, ... ] }
Run again when constructions are added or renamed."""
import glob, json, os, re

SRC = os.path.join(os.path.dirname(__file__), '..', '..', 'KhmerMath_Site', 'site', 'construct')
OUT = os.path.join(os.path.dirname(__file__), '..', 'public', 'data', 'construct_index.json')
KH = '០១២៣៤៥៦៧៨៩'
SKIP = {'index.html'}          # the menu page itself
FIRST = ['board.html']         # shown first among the general ones

def title(path):
    t = re.search(r'<title>([^<]*)</title>', open(path, encoding='utf-8').read())
    t = (t.group(1) if t else '').split(' — ')[0].strip()
    return re.sub(r'^របៀបគូសរូប៖\s*', '', t)

lessons, general = {}, []
for p in sorted(glob.glob(os.path.join(SRC, '*.html'))):
    f = os.path.basename(p)
    if f in SKIP:
        continue
    item = {'f': f, 't': title(p)}
    m = re.match(r'g(\d)-l(\d+)-', f)
    if m:
        lessons.setdefault(m.group(1), {}).setdefault(str(int(m.group(2))), []).append(item)
    else:
        general.append(item)
general.sort(key=lambda x: (x['f'] not in FIRST, x['t']))
for g in lessons:
    lessons[g] = dict(sorted(lessons[g].items(), key=lambda kv: int(kv[0])))
os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump({'base': 'https://khmermath.org/construct/', 'lessons': lessons, 'general': general}, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('lessons:', {g: sum(len(v) for v in d.values()) for g, d in lessons.items()}, 'general:', len(general))
