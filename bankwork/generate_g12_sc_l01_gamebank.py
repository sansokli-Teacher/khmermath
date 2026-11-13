# -*- coding: utf-8 -*-
"""
Grade 12 Science, Chapter 1 Lesson 1 (ចំនួនកុំផ្លិចទម្រង់ពីជគណិត) game bank.
Every numeric answer is computed with sympy; distractors are the common mistakes.
Writes public/data/teamgame_g12.json (same schema as teamgame_g11.json). Files only:
nothing is uploaded to D1 or deployed by this script.
Run:  python3 bankwork/generate_g12_sc_l01_gamebank.py
"""
import json, random
from sympy import I, Rational, sqrt, simplify, expand, re, im, latex, nsimplify

random.seed(12011)
S = ["សញ្ញាណចំនួនកុំផ្លិច", "ប្រមាណវិធីលើចំនួនកុំផ្លិច", "ចំនួនកុំផ្លិចឆ្លាស់និងសមភាព", "ប្លង់កុំផ្លិច"]
Q = []


def L(x):
    x = nsimplify(simplify(expand(x)))
    a, b = simplify(re(x)), simplify(im(x))
    if b == 0:
        return latex(a)
    bs = "" if abs(b) == 1 else latex(abs(b))
    sign = "-" if b < 0 else "+"
    if a == 0:
        return ("-" if b < 0 else "") + bs + "i"
    return latex(a) + " " + sign + " " + bs + "i"


def M(s):
    return "\\(" + s + "\\)"


def add(t, q, lv, h, s, right, wrong, tm=None):
    opts = [right] + list(wrong)
    assert len(set(opts)) == 4, (q, opts)
    random.shuffle(opts)
    Q.append({"t": t, "q": q, "lv": lv, "h": h, "s": s, "o": opts, "a": right, "k": opts.index(right),
              "tm": tm or {"easy": 30, "medium": 60, "hard": 90}[lv]})


def cx(a, b):
    return a + b * I


def arith(t, z1, z2, op, lv, hint):
    sym = {"+": "+", "-": "-", "*": "\\times", "/": "\\div"}[op]
    val = {"+": z1 + z2, "-": z1 - z2, "*": z1 * z2, "/": z1 / z2}[op]
    wrong = []
    a1, b1, a2, b2 = re(z1), im(z1), re(z2), im(z2)
    if op == "+":
        cand = [cx(a1 + a2, b1 - b2), cx(a1 - a2, b1 + b2), cx(a1 + a2, 0) + (b1 * b2) * I]
    elif op == "-":
        cand = [cx(a1 - a2, b1 + b2), cx(a2 - a1, b2 - b1), cx(a1 + a2, b1 - b2)]
    elif op == "*":
        cand = [cx(a1 * a2 + b1 * b2, a1 * b2 + a2 * b1), cx(a1 * a2, b1 * b2), cx(a1 * a2 - b1 * b2, a1 * b2 - a2 * b1)]
    else:
        cand = [cx(a1 * a2 + b1 * b2, 0) / (a2 ** 2 + b2 ** 2) + (a1 * b2 - a2 * b1) / (a2 ** 2 + b2 ** 2) * I,
                (a1 * a2 - b1 * b2) / (a2 ** 2 + b2 ** 2) + (a2 * b1 + a1 * b2) / (a2 ** 2 + b2 ** 2) * I,
                (a1 * a2 + b1 * b2) / (a2 ** 2 + b2 ** 2) + (a2 * b1 - a1 * b2) / (a2 ** 2 + b2 ** 2) * I,
                (a1 + a2) / (a2 ** 2 + b2 ** 2) + (b1 - b2) / (a2 ** 2 + b2 ** 2) * I]
    for c in cand:
        if L(c) != L(val) and L(c) not in [L(w) for w in wrong]:
            wrong.append(c)
    extra = [val + 1, val - I, -val, val + 2 * I, cx(re(val), -im(val)) + 1]
    for c in extra:
        if len(wrong) >= 3:
            break
        if L(c) != L(val) and L(c) not in [L(w) for w in wrong]:
            wrong.append(c)
    q = "គណនា %s ៖" % M("(%s) %s (%s)" % (L(z1), sym, L(z2)))
    s = "ប្រើរូបមន្តដែលពាក់ព័ន្ធ ដោយចាំថា \\(i^2=-1\\)។ គេបាន \\(%s\\)។" % L(val)
    add(t, q, lv, hint, s, M(L(val)), [M(L(w)) for w in wrong[:3]])


T0, T1, T2, T3 = S
# ---------- 1. សញ្ញាណ ----------
add(T0, "ឯកតានិមិត្ត \\(i\\) ត្រូវបានកំណត់ដោយ ៖", "easy", "ចាំលក្ខណៈសំខាន់បំផុតរបស់ \\(i\\)។",
    "ឯកតានិមិត្ត \\(i\\) ជាចំនួនដែល \\(i^2=-1\\)។", M("i^2=-1"), [M("i^2=1"), M("i=-1"), M("i^2=i")])
add(T0, "ក្នុងចំនួនកុំផ្លិច \\(z=-2+3i\\) ផ្នែកពិត និងផ្នែកនិមិត្តគឺ ៖", "easy", "ផ្នែកពិតជាចំនួនមិនមាន \\(i\\)។",
    "ទម្រង់ \\(a+bi\\) ផ្នែកពិត \\(a=-2\\) ផ្នែកនិមិត្ត \\(b=3\\) (មិនមែន \\(3i\\))។",
    M("a=-2,\\ b=3"), [M("a=3,\\ b=-2"), M("a=-2,\\ b=3i"), M("a=2,\\ b=3")])
add(T0, "ចំនួនកុំផ្លិច \\(z=-3i\\) មានផ្នែកពិត \\(a\\) និងផ្នែកនិមិត្ត \\(b\\) ស្មើ ៖", "easy", "សរសេរ \\(-3i=0+(-3)i\\)។",
    "\\(-3i=0+(-3)i\\) ដូច្នេះ \\(a=0,\\ b=-3\\)។", M("a=0,\\ b=-3"), [M("a=-3,\\ b=0"), M("a=0,\\ b=3"), M("a=-3,\\ b=-3")])
add(T0, "ចំនួនណាមួយខាងក្រោមជាចំនួននិមិត្ត (ផលគុណនៃចំនួនពិតមិនសូន្យនិង \\(i\\)) ?", "easy", "ចំនួននិមិត្តមានផ្នែកពិតស្មើ \\(0\\)។",
    "\\(7i=0+7i\\) មានផ្នែកពិត \\(0\\) និងផ្នែកនិមិត្តមិនសូន្យ ដូច្នេះជាចំនួននិមិត្ត។", M("7i"), [M("7+i"), M("7"), M("0")])
for z in [cx(4, 3), cx(1, -3), cx(-5, 2), cx(2, -7)]:
    add(T2, "ចំនួនកុំផ្លិចឆ្លាស់នៃ %s គឺ ៖" % M("z=" + L(z)), "easy", "ចំនួនឆ្លាស់ប្តូរសញ្ញាផ្នែកនិមិត្ត។",
        "បើ \\(z=a+bi\\) នោះ \\(\\bar z=a-bi\\) ដូច្នេះ \\(\\bar z=%s\\)។" % L(z.conjugate()),
        M(L(z.conjugate())), [M(L(-z)), M(L(-z.conjugate())), M(L(cx(im(z), re(z))))])
for z in [cx(3, 1), cx(-2, 5), cx(1, -3)]:
    add(T2, "ចំនួនកុំផ្លិចផ្ទុយនៃ %s គឺ ៖" % M("z=" + L(z)), "easy", "ចំនួនផ្ទុយប្តូរសញ្ញាទាំងផ្នែកពិត និងនិមិត្ត។",
        "\\(-z=-a-bi\\) ដូច្នេះ \\(-z=%s\\)។" % L(-z), M(L(-z)), [M(L(z.conjugate())), M(L(z)), M(L(-z.conjugate()))])
add(T2, "ចំនួនកុំផ្លិចឆ្លាស់នៃ \\(24\\) និង \\(-i\\) គឺ ៖", "medium", "ចំនួនពិតមានផ្នែកនិមិត្ត \\(0\\)។",
    "\\(\\overline{24}=24\\) ព្រោះផ្នែកនិមិត្តសូន្យ ហើយ \\(\\overline{-i}=i\\)។", M("24\\ \\text{និង}\\ i"),
    [M("-24\\ \\text{និង}\\ i"), M("24\\ \\text{និង}\\ -i"), M("-24\\ \\text{និង}\\ -i")])
# ---------- 2. ប្រមាណវិធី ----------
arith(T1, cx(5, 3), cx(-1, 2), "+", "easy", "បូកផ្នែកពិតជាមួយផ្នែកពិត និងផ្នែកនិមិត្តជាមួយផ្នែកនិមិត្ត។")
arith(T1, cx(2, 5), cx(3, -2), "+", "easy", "បូកផ្នែកពិត និងផ្នែកនិមិត្តដាច់ដោយឡែក។")
arith(T1, cx(9, -2), cx(4, -4), "-", "easy", "ប្រយ័ត្នសញ្ញាពេលដកផ្នែកនិមិត្តអវិជ្ជមាន។")
arith(T1, cx(6, 4), cx(3, 6), "-", "easy", "ដកផ្នែកពិត និងផ្នែកនិមិត្តដាច់ដោយឡែក។")
arith(T1, cx(0, 3), cx(5, -4), "*", "medium", "ពន្លាត រួចជំនួស \\(i^2=-1\\)។")
arith(T1, cx(2, 3), cx(4, 2), "*", "medium", "ប្រើ \\((a+bi)(c+di)=(ac-bd)+(ad+bc)i\\)។")
arith(T1, cx(1, 2), cx(3, -1), "*", "medium", "ប្រើ \\((a+bi)(c+di)=(ac-bd)+(ad+bc)i\\)។")
arith(T1, cx(3, 0), cx(2, 1), "/", "medium", "គុណភាគយក និងភាគបែងនឹងចំនួនឆ្លាស់នៃភាគបែង។")
arith(T1, cx(3, 2), cx(1, -3), "/", "hard", "គុណភាគយក និងភាគបែងនឹង \\(1+3i\\)។")
arith(T1, cx(2, 5), cx(1, -7), "/", "hard", "ភាគបែងក្លាយជា \\(1+49\\)។")
arith(T1, cx(1, -3), cx(4, -1), "/", "hard", "គុណនឹងចំនួនឆ្លាស់នៃ \\(4-i\\)។")
add(T1, "តម្លៃនៃ \\(i^3\\) គឺ ៖", "easy", "\\(i^3=i^2\\cdot i\\)។", "\\(i^3=i^2\\cdot i=-i\\)។", M("-i"), [M("i"), M("-1"), M("1")])
add(T1, "តម្លៃនៃ \\(i^4\\) គឺ ៖", "easy", "\\(i^4=(i^2)^2\\)។", "\\(i^4=(i^2)^2=(-1)^2=1\\)។", M("1"), [M("-1"), M("i"), M("-i")])
add(T1, "គណនា \\((2+i)(2-i)\\) ៖", "easy", "ប្រើ \\((a+b)(a-b)=a^2-b^2\\)។",
    "\\((2+i)(2-i)=2^2-i^2=4+1=5\\)។", M("5"), [M("3"), M("4-i^2=3"), M("4+2i")])
add(T1, "ចំពោះ \\(c+di\\ne0\\) ផលធៀប \\(\\dfrac{a+bi}{c+di}\\) សមនឹង ៖", "hard", "គុណនឹង \\(c-di\\) ទាំងភាគយក និងភាគបែង។",
    "\\(\\dfrac{(a+bi)(c-di)}{c^2+d^2}=\\dfrac{ac+bd}{c^2+d^2}+\\dfrac{bc-ad}{c^2+d^2}i\\)។",
    M("\\dfrac{ac+bd}{c^2+d^2}+\\dfrac{bc-ad}{c^2+d^2}i"), [M("\\dfrac{ac-bd}{c^2+d^2}+\\dfrac{bc+ad}{c^2+d^2}i"),
    M("\\dfrac{ac+bd}{c^2-d^2}+\\dfrac{bc-ad}{c^2-d^2}i"), M("\\dfrac{a}{c}+\\dfrac{b}{d}i")])
z = ((-1 + sqrt(3) * I) / (2 * I)) ** 2
add(T1, "គណនា \\(\\left(\\dfrac{-1+\\sqrt3\\,i}{2i}\\right)^2\\) ៖", "hard", "ពន្លាត \\((-1+\\sqrt3 i)^2\\) និង \\((2i)^2=-4\\)។",
    "\\((-1+\\sqrt3 i)^2=-2-2\\sqrt3 i\\) ហើយ \\((2i)^2=-4\\) នាំឱ្យ \\(z=\\dfrac12+\\dfrac{\\sqrt3}{2}i\\)។",
    M("\\dfrac12+\\dfrac{\\sqrt3}{2}i"), [M("-\\dfrac12+\\dfrac{\\sqrt3}{2}i"), M("\\dfrac12-\\dfrac{\\sqrt3}{2}i"), M("1+\\sqrt3 i")])
add(T1, "គណនា \\((1+2i)^3\\) ៖", "hard", "រក \\((1+2i)^2\\) មុន រួចគុណនឹង \\(1+2i\\)។",
    "\\((1+2i)^2=-3+4i\\) ហើយ \\((-3+4i)(1+2i)=-11-2i\\)។", M("-11-2i"), [M("-11+2i"), M("1+8i"), M("-3+8i")])
add(T1, "គណនា \\(\\dfrac{1}{i}\\) ៖", "medium", "គុណភាគយក និងភាគបែងនឹង \\(-i\\) (ឬ \\(i\\))។",
    "\\(\\dfrac1i=\\dfrac{i}{i^2}=-i\\)។", M("-i"), [M("i"), M("1"), M("-1")])
# ---------- 3. សមភាព និងលក្ខណៈឆ្លាស់ ----------
add(T2, "ចំនួនកុំផ្លិច \\(a+bi\\) និង \\(c+di\\) ស្មើគ្នាលុះត្រាតែ ៖", "easy", "ផ្នែកពិតត្រូវស្មើផ្នែកពិត និងផ្នែកនិមិត្តស្មើផ្នែកនិមិត្ត។",
    "ចំនួនកុំផ្លិចពីរស្មើគ្នា លុះត្រាតែ \\(a=c\\) និង \\(b=d\\)។", M("a=c\\ \\text{និង}\\ b=d"),
    [M("a=d\\ \\text{និង}\\ b=c"), M("a+b=c+d"), M("a=c\\ \\text{ឬ}\\ b=d")])
add(T2, "ដោះស្រាយ \\(3x-\\sqrt{-25}=-6+3yi\\) (\\(x,y\\in\\mathbb{R}\\)) បាន ៖", "hard", "\\(\\sqrt{-25}=5i\\) ហើយផ្ទឹមផ្នែកពិត និងផ្នែកនិមិត្ត។",
    "\\(3x-5i=-6+3yi\\) នាំឱ្យ \\(3x=-6\\) និង \\(-5=3y\\) ដូច្នេះ \\(x=-2,\\ y=-\\dfrac53\\)។",
    M("x=-2,\\ y=-\\dfrac53"), [M("x=2,\\ y=-\\dfrac53"), M("x=-2,\\ y=\\dfrac53"), M("x=-6,\\ y=-5")])
add(T2, "បើ \\(z_1=2-5i\\) និង \\(z_2=-4+i\\) នោះ \\(\\overline{z_1+z_2}\\) ស្មើ ៖", "medium", "រក \\(z_1+z_2\\) មុន រួចយកចំនួនឆ្លាស់។",
    "\\(z_1+z_2=-2-4i\\) ដូច្នេះ \\(\\overline{z_1+z_2}=-2+4i\\)។", M("-2+4i"), [M("-2-4i"), M("2+4i"), M("6+6i")])
add(T2, "លក្ខណៈមួយណាត្រឹមត្រូវចំពោះគ្រប់ចំនួនកុំផ្លិច \\(z_1,z_2\\) ?", "medium", "ចំនួនឆ្លាស់នៃផលគុណ ស្មើផលគុណនៃចំនួនឆ្លាស់។",
    "\\(\\overline{z_1z_2}=\\overline{z_1}\\,\\overline{z_2}\\)។ ផ្ទៀងផ្ទាត់៖ \\((5-i)(2+3i)=13+13i\\) ចំនួនឆ្លាស់ \\(13-13i=(5+i)(2-3i)\\)។",
    M("\\overline{z_1z_2}=\\overline{z_1}\\,\\overline{z_2}"), [M("\\overline{z_1z_2}=\\overline{z_1}+\\overline{z_2}"),
    M("\\overline{z_1z_2}=-\\overline{z_1}\\,\\overline{z_2}"), M("\\overline{z_1z_2}=z_1\\,\\overline{z_2}")])
add(T2, "បើ \\(z_1=1-3i,\\ z_2=4-i\\) នោះ \\(\\overline{\\left(\\dfrac{z_1}{z_2}\\right)}\\) ស្មើ ៖", "hard", "\\(\\dfrac{z_1}{z_2}=\\dfrac{7-11i}{17}\\)។",
    "\\(\\dfrac{z_1}{z_2}=\\dfrac{(1-3i)(4+i)}{17}=\\dfrac{7-11i}{17}\\) ដូច្នេះចំនួនឆ្លាស់គឺ \\(\\dfrac{7+11i}{17}\\)។",
    M("\\dfrac{7+11i}{17}"), [M("\\dfrac{7-11i}{17}"), M("\\dfrac{-7+11i}{17}"), M("\\dfrac{4+11i}{17}")])
add(T2, "ចំនួនកុំផ្លិច \\(z\\) ជាចំនួនពិត លុះត្រាតែ ៖", "medium", "ចំនួនពិតមិនប្តូរពេលយកចំនួនឆ្លាស់។",
    "\\(z=\\bar z\\) កើតឡើងលុះត្រាតែ \\(b=-b\\) គឺ \\(b=0\\) ។", M("z=\\bar z"), [M("z=-\\bar z"), M("z=-z"), M("z\\bar z=0")])
add(T2, "កំណត់ \\(x\\in\\mathbb{R}\\) ដើម្បីឱ្យ \\(\\dfrac{3+i}{1+i}+\\dfrac{x-i}{1-i}\\) ជាចំនួនពិត ៖", "hard",
    "សរសេរជា \\(a+bi\\) រួចដាក់ \\(b=0\\)។",
    "\\(\\dfrac{3+i}{1+i}=2-i\\) ហើយ \\(\\dfrac{x-i}{1-i}=\\dfrac{x+1}{2}+\\dfrac{x-1}{2}i\\)។ ផ្នែកនិមិត្ត \\(\\dfrac{x-3}{2}=0\\) ដូច្នេះ \\(x=3\\)។",
    M("x=3"), [M("x=-3"), M("x=1"), M("x=-1")])
# ---------- 4. ប្លង់កុំផ្លិច ----------
add(T3, "ចំណុចរូបភាពនៃចំនួនកុំផ្លិច \\(z=a+bi\\) ក្នុងប្លង់កុំផ្លិចមានកូអរដោនេ ៖", "easy", "ផ្នែកពិតជា \\(x\\) ផ្នែកនិមិត្តជា \\(y\\)។",
    "\\(M(z)\\) មានកូអរដោនេ \\((a,b)\\)។", M("(a,b)"), [M("(b,a)"), M("(a,-b)"), M("(-a,b)")])
for z in [cx(2, -3), cx(-4, 1), cx(0, -2)]:
    right = "(%s,%s)" % (re(z), im(z))
    cands = ["(%s,%s)" % (im(z), re(z)), "(%s,%s)" % (re(z), -im(z)), "(%s,%s)" % (-re(z), -im(z)),
             "(%s,%s)" % (-re(z), im(z)), "(%s,%s)" % (im(z) + 1, re(z) - 1), "(%s,%s)" % (re(z) + 2, im(z) + 2)]
    wr = []
    for c in cands:
        if c != right and c not in wr:
            wr.append(c)
    add(T3, "រូបភាពនៃ %s មានកូអរដោនេ ៖" % M("z=" + L(z)), "easy", "អានផ្នែកពិត និងផ្នែកនិមិត្ត។",
        "\\(z=%s\\) មានរូបភាព \\(%s\\)។" % (L(z), right), M(right), [M(c) for c in wr[:3]])
add(T3, "រូបភាពនៃ \\(z\\) និង \\(\\bar z\\) ឆ្លុះគ្នាធៀបនឹង ៖", "medium", "\\(z\\) និង \\(\\bar z\\) មានផ្នែកពិតដូចគ្នា។",
    "\\((a,b)\\) និង \\((a,-b)\\) ឆ្លុះគ្នាតាមអ័ក្សពិត។", "អ័ក្សពិត", ["អ័ក្សនិមិត្ត", "គល់តម្រុយ \\(O\\)", "បន្ទាត់ \\(y=x\\)"])
add(T3, "រូបភាពនៃ \\(z\\) និង \\(-z\\) ឆ្លុះគ្នាធៀបនឹង ៖", "medium", "\\((a,b)\\) និង \\((-a,-b)\\)។",
    "\\((a,b)\\) និង \\((-a,-b)\\) ឆ្លុះគ្នាតាមគល់តម្រុយ \\(O\\)។", "គល់តម្រុយ \\(O\\)", ["អ័ក្សពិត", "អ័ក្សនិមិត្ត", "បន្ទាត់ \\(y=x\\)"])
for z1, z2 in [(cx(2, 1), cx(1, 2)), (cx(3, 4), cx(-2, 3)), (cx(2, 4), cx(1, -2))]:
    s = z1 + z2
    right = "(%s,%s)" % (re(s), im(s))
    cands = ["(%s,%s)" % (im(s), re(s)), "(%s,%s)" % (re(z1 - z2), im(z1 - z2)), "(%s,%s)" % (re(s), -im(s)),
             "(%s,%s)" % (re(z1 * z2), im(z1 * z2)), "(%s,%s)" % (re(s) + 1, im(s) - 1), "(%s,%s)" % (-re(s), -im(s))]
    wr = []
    for c in cands:
        if c != right and c not in wr:
            wr.append(c)
    add(T3, "បើ \\(z_1=%s,\\ z_2=%s\\) នោះរូបភាពនៃ \\(z_1+z_2\\) មានកូអរដោនេ ៖" % (L(z1), L(z2)), "medium",
        "វ៉ិចទ័ររូបភាពនៃផលបូក ជាអង្កត់ទ្រូងនៃប្រលេឡូក្រាម។",
        "\\(z_1+z_2=%s\\) ដូច្នេះរូបភាពគឺ \\(%s\\)។" % (L(s), right), M(right), [M(c) for c in wr[:3]])
z1, z2 = cx(3, 4), cx(-2, 3)
d = z1 - z2
add(T3, "បើ \\(z_1=3+4i,\\ z_2=-2+3i\\) នោះរូបភាពនៃ \\(z_1-z_2\\) គឺ ៖", "medium", "\\(z_1-z_2=z_1+(-z_2)\\)។",
    "\\(z_1-z_2=5+i\\) ដូច្នេះរូបភាពគឺ \\((5,1)\\)។", M("(5,1)"), [M("(1,7)"), M("(-5,-1)"), M("(1,1)")])
add(T3, "បើ \\(z=2+i\\) នោះរូបភាពនៃ \\(2z\\) គឺ ៖", "easy", "\\(\\overrightarrow{OM}=2\\overrightarrow{OM_1}\\)។",
    "\\(2z=4+2i\\) មានរូបភាព \\((4,2)\\)។", M("(4,2)"), [M("(2,4)"), M("(2,1)"), M("(4,1)")])
add(T3, "បើ \\(z_1=1-2i,\\ z_2=2+2i\\) នោះរូបភាពនៃ \\(2z_2+z_1\\) គឺ ៖", "hard", "គណនា \\(2z_2+z_1\\) ជាចំនួនកុំផ្លិចមុន។",
    "\\(2z_2+z_1=4+4i+1-2i=5+2i\\) មានរូបភាព \\((5,2)\\)។", M("(5,2)"), [M("(2,5)"), M("(3,0)"), M("(5,6)")])
add(T3, "បើ \\(z=2+4i\\) នោះរូបភាពនៃ \\(-\\dfrac12z\\) គឺ ៖", "medium", "\\(-\\dfrac12z=-\\dfrac12(2+4i)\\)។",
    "\\(-\\dfrac12z=-1-2i\\) មានរូបភាព \\((-1,-2)\\)។", M("(-1,-2)"), [M("(1,2)"), M("(-1,2)"), M("(-2,-4)")])

for i, q in enumerate(Q):
    assert q["t"] in S and len(q["o"]) == 4 and q["a"] == q["o"][q["k"]] and len(set(q["o"])) == 4, (i, q)


def main():
    from collections import Counter
    print(len(Q), "questions", dict(Counter(q["t"] for q in Q)), dict(Counter(q["lv"] for q in Q)))
    lesson = {"title": "ចំនួនកុំផ្លិចទម្រង់ពីជគណិត", "t": "ចំនួនកុំផ្លិចទម្រង់ពីជគណិត", "q": Q, "qs": Q}
    data = {"class": 12, "lessons": [dict(lesson, n=1, g=12, d=1), dict(lesson, n=401, g=12, d=1)]}
    with open("public/data/teamgame_g12.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("wrote public/data/teamgame_g12.json")


if __name__ == "__main__":
    main()
