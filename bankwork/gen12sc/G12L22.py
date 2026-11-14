"""Bank generator for Grade 12 Science — Lesson 22: ទ្រឹស្ដីបទបេយេស."""
from fractions import Fraction
from lib import mcq, wr

LESSON = 'ទ្រឹស្ដីបទបេយេស'
CHAPTER = 'ជំពូកទី 8 : ប្រូបាប'
TARGET = {
    ('mcq', 'easy'): 10, ('mcq', 'medium'): 14, ('mcq', 'hard'): 7, ('mcq', 'pisa'): 5,
    ('writing', 'easy'): 1, ('writing', 'medium'): 4, ('writing', 'hard'): 4, ('writing', 'pisa'): 5,
}

S1 = '១. រូបមន្តប្រូបាបសរុប'
S2 = '២. ទ្រឹស្តីបទបេយេស'
S3 = '៣. អនុវត្តន៍ក្នុងឧស្សាហកម្ម និងវេជ្ជសាស្ត្រ'


def writing(level, sec, stem, ans, sol, bloom=None):
    return wr(level, sec, stem, [(sol, 3), (f'ចម្លើយ៖ {ans}', 2)], bloom=bloom)


def svg_bayes_tree():
    w, h = 250, 145
    return (
        f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg">'
        f'<line x1="20" y1="72" x2="95" y2="38" stroke="#2b6cb0" stroke-width="1.8"/>'
        f'<line x1="20" y1="72" x2="95" y2="108" stroke="#c53030" stroke-width="1.8"/>'
        f'<line x1="95" y1="38" x2="180" y2="20" stroke="#2b6cb0" stroke-width="1.5"/>'
        f'<line x1="95" y1="38" x2="180" y2="56" stroke="#718096" stroke-width="1.5"/>'
        f'<line x1="95" y1="108" x2="180" y2="90" stroke="#c53030" stroke-width="1.5"/>'
        f'<line x1="95" y1="108" x2="180" y2="126" stroke="#718096" stroke-width="1.5"/>'
        f'<text x="45" y="48" font-size="10" fill="#2b6cb0">0.85</text>'
        f'<text x="45" y="102" font-size="10" fill="#c53030">0.15</text>'
        f'<text x="95" y="33" font-size="11" font-weight="bold">V</text>'
        f'<text x="95" y="122" font-size="11" font-weight="bold">V̄</text>'
        f'<text x="132" y="24" font-size="10">0.02</text>'
        f'<text x="132" y="55" font-size="10">0.98</text>'
        f'<text x="132" y="94" font-size="10">0.99</text>'
        f'<text x="132" y="125" font-size="10">0.01</text>'
        f'<text x="186" y="24" font-size="10">M</text>'
        f'<text x="186" y="60" font-size="10">M̄</text>'
        f'<text x="186" y="94" font-size="10">M</text>'
        f'<text x="186" y="130" font-size="10">M̄</text>'
        f'</svg>'
    )


def build_candidates():
    qs = []

    # =========================================================================
    # MCQ EASY (10)
    # =========================================================================
    # 1 (Remember)
    qs.append(mcq(
        'easy', S1,
        'បើ $A_1, A_2, \\dots, A_n$ បង្កើតជាចំណែកនៃលំហសំណាក $S$ តើរូបមន្តប្រូបាបសរុបនៃព្រឹត្តិការណ៍ $B$ គឺជាអ្វី?',
        r'$P(B) = \sum_{i=1}^{n} P(A_i) P(B \mid A_i)$',
        [r'$P(B) = \sum_{i=1}^{n} P(A_i \mid B)$', r'$P(B) = \prod_{i=1}^{n} P(A_i) P(B \mid A_i)$', r'$P(B) = \sum_{i=1}^{n} \frac{P(B \mid A_i)}{P(A_i)}$'],
        'តាមរូបមន្តប្រូបាបសរុប $P(B) = \\sum_{i=1}^{n} P(A_i)P(B \\mid A_i)$។',
        bloom='Remember',
    ))

    # 2 (Remember)
    qs.append(mcq(
        'easy', S2,
        'តាមទ្រឹស្តីបទបេយេស តើ $P(A_k \\mid B)$ ($P(B) > 0$) ស្មើនឹងអ្វី?',
        r'$\frac{P(A_k) P(B \mid A_k)}{\sum_{i=1}^{n} P(A_i) P(B \mid A_i)}$',
        [r'$\frac{P(A_k) P(A_k \mid B)}{P(B)}$', r'$\frac{P(B)}{P(A_k) P(B \mid A_k)}$', r'$P(A_k) + P(B \mid A_k)$'],
        'ទ្រឹស្តីបទបេយេស៖ $P(A_k \\mid B) = \\frac{P(A_k)P(B \\mid A_k)}{P(B)} = \\frac{P(A_k)P(B \\mid A_k)}{\\sum_{i=1}^n P(A_i)P(B \\mid A_i)}$។',
        bloom='Remember',
    ))

    # 3 (Understand)
    qs.append(mcq(
        'easy', S1,
        'បើ $A$ និង $\\overline{A}$ ជាព្រឹត្តិការណ៍ផ្ទុយគ្នា តើ $P(B)$ អាចសរសេរដូចម្តេច?',
        r'$P(A)P(B \mid A) + P(\overline{A})P(B \mid \overline{A})$',
        [r'$P(A) + P(\overline{A})$', r'$P(B \mid A) + P(B \mid \overline{A})$', r'$P(A)P(A \mid B) + P(\overline{A})P(\overline{A} \mid B)$'],
        'ដោយ $A$ និង $\\overline{A}$ ចែកលំហសំណាកជា 2 ផ្នែក នោះ $P(B) = P(A)P(B \\mid A) + P(\\overline{A})P(B \\mid \\overline{A})$។',
        bloom='Understand',
    ))

    # 4 (Apply)
    qs.append(mcq(
        'easy', S1,
        'គេមាន $P(A) = 0.4$, $P(B \\mid A) = 0.5$ និង $P(B \\mid \\overline{A}) = 0.2$ ។ គណនា $P(B)$ ។',
        r'$0.32$',
        [r'$0.70$', r'$0.20$', r'$0.42$'],
        '$P(B) = 0.4(0.5) + 0.6(0.2) = 0.20 + 0.12 = 0.32$។',
        bloom='Apply',
    ))

    # 5 (Apply)
    qs.append(mcq(
        'easy', S2,
        'គេមាន $P(A) = 0.4$, $P(B \\mid A) = 0.5$ និង $P(B) = 0.32$ ។ គណនា $P(A \\mid B)$ ។',
        r'$\frac{5}{8}$',
        [r'$\frac{3}{8}$', r'$\frac{1}{2}$', r'$\frac{2}{5}$'],
        '$P(A \\mid B) = \\frac{0.4 \\times 0.5}{0.32} = \\frac{0.20}{0.32} = \\frac{5}{8}$។',
        bloom='Apply',
    ))

    # 6 (Apply)
    svg6 = svg_bayes_tree()
    qs.append(mcq(
        'easy', S1,
        f'តាមដ្យាក្រាមដើមឈើខាងក្រោម គណនាប្រូបាប $P(V \\cap M)$ ។<br/>{svg6}',
        r'$0.017$',
        [r'$0.87$', r'$0.1485$', r'$0.17$'],
        '$P(V \\cap M) = P(V)P(M \\mid V) = 0.85 \\times 0.02 = 0.017$។',
        bloom='Apply',
    ))

    # 7 (Apply)
    qs.append(mcq(
        'easy', S1,
        'សំណួរពីជគណិត និងធរណីមាត្រមានប្រូបាបចាប់បានស្មើគ្នា ($0.5$) ។ សុខឆ្លើយត្រូវពីជគណិត $0.7$ និងធរណីមាត្រ $0.5$ ។ គណនាប្រូបាបដែលសុខឆ្លើយត្រូវ ។',
        r'$0.6$',
        [r'$0.5$', r'$0.7$', r'$0.35$'],
        '$P(\\text{ត្រូវ}) = 0.5(0.7) + 0.5(0.5) = 0.35 + 0.25 = 0.6$។',
        bloom='Apply',
    ))

    # 8 (Apply)
    qs.append(mcq(
        'easy', S2,
        'ក្នុងលំហាត់ខាងលើ ($P(\\text{Alg})=P(\\text{Geo})=0.5$, $P(\\text{ត្រូវ}|\\text{Alg})=0.7$, $P(\\text{ត្រូវ}|\\text{Geo})=0.5$) បើសុខឆ្លើយត្រូវ តើប្រូបាបដែលសំណួរនោះជាធរណីមាត្រស្មើប៉ុន្មាន?',
        r'$\frac{5}{12}$',
        [r'$\frac{7}{12}$', r'$\frac{1}{2}$', r'$\frac{1}{4}$'],
        '$P(\\text{Geo} \\mid \\text{ត្រូវ}) = \\frac{0.5 \\times 0.5}{0.6} = \\frac{0.25}{0.60} = \\frac{5}{12}$។',
        bloom='Apply',
    ))

    # 9 (Understand)
    qs.append(mcq(
        'easy', S2,
        'ក្នុងទ្រឹស្តីបទបេយេស ភាគបែង $\\sum_{i=1}^{n} P(A_i)P(B \\mid A_i)$ តំណាងឲ្យអ្វី?',
        r'ប្រូបាបសរុប $P(B)$',
        [r'ប្រូបាប $P(A_k)$', r'ប្រូបាប $P(A_k \cap B)$', r'ប្រូបាប $P(\overline{B})$'],
        'ភាគបែងក្នុងទ្រឹស្តីបទបេយេសគឺជាប្រូបាបសរុប $P(B)$។',
        bloom='Understand',
    ))

    # 10 (Apply)
    qs.append(mcq(
        'easy', S1,
        'កាក់ 100 កាក់មានកាក់ល្អ 25 ($P(C)=\\frac{1}{2}$) និងកាក់គ្មានលំនឹង 75 ($P(C)=\\frac{1}{3}$) ។ ចាប់កាក់មួយបោះ ។ គណនាប្រូបាបបានខាងលេខ $P(C)$ ។',
        r'$\frac{3}{8}$',
        [r'$\frac{1}{4}$', r'$\frac{1}{3}$', r'$\frac{5}{12}$'],
        '$P(C) = \\frac{1}{4}\\cdot\\frac{1}{2} + \\frac{3}{4}\\cdot\\frac{1}{3} = \\frac{1}{8} + \\frac{1}{4} = \\frac{3}{8}$។',
        bloom='Apply',
    ))

    # =========================================================================
    # MCQ MEDIUM (14)
    # =========================================================================
    # 11 (Apply) - Ex 1c: P(A | C) = (1/8) / (3/8) = 1/3
    qs.append(mcq(
        'medium', S2,
        'ថង់មានកាក់ល្អ 25 ($P(C)=\\frac{1}{2}$) និងកាក់ល្អៀង 75 ($P(C)=\\frac{1}{3}$) ។ បើបោះបានខាងលេខ ($C$) រកប្រូបាបដែលកាក់នោះជាកាក់ល្អ ($A$) ។',
        r'$\frac{1}{3}$',
        [r'$\frac{1}{4}$', r'$\frac{2}{3}$', r'$\frac{1}{8}$'],
        '$P(A \\mid C) = \\frac{P(A)P(C \\mid A)}{P(C)} = \\frac{1/8}{3/8} = \\frac{1}{3}$។',
        bloom='Apply',
    ))

    # 12 (Apply) - Village vaccination example: 85% V (2% M), 15% V' (99% M). P(M) = 0.017 + 0.1485 = 0.1655
    qs.append(mcq(
        'medium', S1,
        'ភូមិមួយមាន 85% ចាក់ថ្នាំបង្ការ (2% ឆ្លងជំងឺ) និង 15% មិនចាក់ (1% មិនឆ្លងជំងឺ) ។ គណនាប្រូបាបដែលអ្នកភូមិម្នាក់ឆ្លងជំងឺ ។',
        r'$0.1655$',
        [r'$0.0185$', r'$0.8345$', r'$0.1485$'],
        '$P(M) = 0.85(0.02) + 0.15(0.99) = 0.017 + 0.1485 = 0.1655$។',
        bloom='Apply',
    ))

    # 13 (Apply) - Machines B1(30%,2%), B2(45%,3%), B3(25%,2%). P(D) = 0.006+0.0135+0.005 = 0.0245
    qs.append(mcq(
        'medium', S3,
        'ម៉ាស៊ីន $B_1, B_2, B_3$ ផលិត 30%, 45%, 25% រៀងគ្នា ដោយមានអត្រាខូច 2%, 3%, 2% រៀងគ្នា ។ រកប្រូបាបដែលផលិតផលមួយខូច ។',
        r'$0.0245$',
        [r'$0.0700$', r'$0.0250$', r'$0.0135$'],
        '$P(D) = 0.30(0.02) + 0.45(0.03) + 0.25(0.02) = 0.006 + 0.0135 + 0.005 = 0.0245$។',
        bloom='Apply',
    ))

    # 14 (Apply) - Bayes on B3 | D: 0.005 / 0.0245 = 10/49
    qs.append(mcq(
        'medium', S3,
        'ក្នុងលំហាត់ម៉ាស៊ីន $B_1, B_2, B_3$ ខាងលើ បើចាប់បានផលិតផលខូច តើប្រូបាបដែលវាផលិតដោយម៉ាស៊ីន $B_3$ ស្មើនឹងប៉ុន្មាន?',
        r'$\frac{10}{49}$',
        [r'$\frac{12}{49}$', r'$\frac{27}{49}$', r'$\frac{1}{4}$'],
        '$P(B_3 \\mid D) = \\frac{0.0050}{0.0245} = \\frac{50}{245} = \\frac{10}{49}$។',
        bloom='Apply',
    ))

    # 15 (Apply) - Machines A(50%,3%), B(30%,4%), C(20%,4%). P(D) = 0.015 + 0.012 + 0.008 = 0.035
    qs.append(mcq(
        'medium', S3,
        'ម៉ាស៊ីន $A, B, C$ ផលិត 50%, 30%, 20% ដោយមានអត្រាខូច 3%, 4%, 4% រៀងគ្នា ។ គណនាប្រូបាបដែលផលិតផលចៃដន្យមួយខូច ។',
        r'$0.035$',
        [r'$0.110$', r'$0.037$', r'$0.040$'],
        '$P(D) = 0.50(0.03) + 0.30(0.04) + 0.20(0.04) = 0.015 + 0.012 + 0.008 = 0.035$។',
        bloom='Apply',
    ))

    # 16 (Apply) - Bayes on A | D for above: 0.015 / 0.035 = 3/7
    qs.append(mcq(
        'medium', S3,
        'ក្នុងលំហាត់ម៉ាស៊ីន $A(50\\%,3\\%), B(30\\%,4\\%), C(20\\%,4\\%)$ បើផលិតផលនោះខូច តើប្រូបាបដែលវាចេញពីម៉ាស៊ីន $A$ ស្មើប៉ុន្មាន?',
        r'$\frac{3}{7}$',
        [r'$\frac{1}{2}$', r'$\frac{12}{35}$', r'$\frac{8}{35}$'],
        '$P(A \\mid D) = \\frac{0.015}{0.035} = \\frac{15}{35} = \\frac{3}{7}$។',
        bloom='Apply',
    ))

    # 17 (Apply) - Ex 3a: A(40%,3%), B(35%,4%), C(25%,4%). P(D) = 0.012 + 0.014 + 0.010 = 0.036
    qs.append(mcq(
        'medium', S3,
        'ម៉ាស៊ីន $A, B, C$ ផលិត 40%, 35%, 25% ដោយមានអត្រាខូច 3%, 4%, 4% រៀងគ្នា ។ គណនាប្រូបាបដែលផលិតផលមួយខូច ។',
        r'$0.036$',
        [r'$0.035$', r'$0.038$', r'$0.012$'],
        '$P(D) = 0.40(0.03) + 0.35(0.04) + 0.25(0.04) = 0.012 + 0.014 + 0.010 = 0.036$។',
        bloom='Apply',
    ))

    # 18 (Apply) - Box 1 (3R, 2W), Box 2 (1R, 4W). Choose box equally likely, draw R -> P(Box 1 | R) = (3/10)/(4/10) = 3/4
    qs.append(mcq(
        'medium', S2,
        'ប្រអប់ $U_1$ មានប៊ូលក្រហម 3 ស 2 ។ ប្រអប់ $U_2$ មានប៊ូលក្រហម 1 ស 4 ។ ជ្រើសប្រអប់មួយដោយចៃដន្យ រួចចាប់បានប៊ូលក្រហម ។ រកប្រូបាបដែលប៊ូលនោះចេញពីប្រអប់ $U_1$ ។',
        r'$\frac{3}{4}$',
        [r'$\frac{1}{4}$', r'$\frac{3}{5}$', r'$\frac{1}{2}$'],
        '$P(U_1 \\mid R) = \\frac{0.5(3/5)}{0.5(3/5) + 0.5(1/5)} = \\frac{3}{3 + 1} = \\frac{3}{4}$។',
        bloom='Apply',
    ))

    # 19 (Analyze) - Urn: 1/3 chance to pick Urn A (4R, 2B), 2/3 chance to pick Urn B (2R, 4B). P(R) = (1/3)(2/3) + (2/3)(1/3) = 4/9
    qs.append(mcq(
        'medium', S1,
        'គេបោះគ្រាប់ឡុកឡាក់៖ បើចេញលេខ $1$ ឬ $2$ ចាប់ប៊ូលពីថង់ $A$ (ក្រហម 4, ខៀវ 2); បើចេញលេខ $3, 4, 5, 6$ ចាប់ពីថង់ $B$ (ក្រហម 2, ខៀវ 4) ។ គណនាប្រូបាបបានប៊ូលក្រហម ។',
        r'$\frac{4}{9}$',
        [r'$\frac{1}{2}$', r'$\frac{5}{9}$', r'$\frac{2}{9}$'],
        '$P(R) = \\frac{1}{3}\\cdot\\frac{4}{6} + \\frac{2}{3}\\cdot\\frac{2}{6} = \\frac{2}{9} + \\frac{2}{9} = \\frac{4}{9}$។',
        bloom='Analyze',
    ))

    # 20 (Analyze) - From Q19, P(Urn A | R) = (2/9)/(4/9) = 1/2
    qs.append(mcq(
        'medium', S2,
        'ក្នុងពិសោធន៍ខាងលើ ($P(A)=\\frac{1}{3}$ មាន $4R,2B$; $P(B)=\\frac{2}{3}$ មាន $2R,4B$) បើចាប់បានប៊ូលក្រហម រកប្រូបាបដែលវាបានមកពីថង់ $A$ ។',
        r'$\frac{1}{2}$',
        [r'$\frac{1}{3}$', r'$\frac{2}{3}$', r'$\frac{4}{9}$'],
        '$P(A \\mid R) = \\frac{2/9}{4/9} = \\frac{1}{2}$។',
        bloom='Analyze',
    ))

    # 21 (Apply) - P(A1)=0.2, P(A2)=0.3, P(A3)=0.5; P(B|A1)=0.1, P(B|A2)=0.2, P(B|A3)=0.4 -> P(B) = 0.02 + 0.06 + 0.20 = 0.28
    qs.append(mcq(
        'medium', S1,
        'គេមានចំណែក $A_1, A_2, A_3$ ដែល $P(A_1)=0.2, P(A_2)=0.3, P(A_3)=0.5$ ។ បើ $P(B\\mid A_1)=0.1, P(B\\mid A_2)=0.2, P(B\\mid A_3)=0.4$ គណនា $P(B)$ ។',
        r'$0.28$',
        [r'$0.70$', r'$0.20$', r'$0.34$'],
        '$P(B) = 0.2(0.1) + 0.3(0.2) + 0.5(0.4) = 0.02 + 0.06 + 0.20 = 0.28$។',
        bloom='Apply',
    ))

    # 22 (Apply) - From Q21, P(A2 | B) = 0.06 / 0.28 = 3/14
    qs.append(mcq(
        'medium', S2,
        'ក្នុងទិន្នន័យខាងលើ ($P(B)=0.28$, $P(A_2)=0.3$, $P(B\\mid A_2)=0.2$) គណនា $P(A_2 \\mid B)$ ។',
        r'$\frac{3}{14}$',
        [r'$\frac{5}{7}$', r'$\frac{1}{14}$', r'$\frac{3}{10}$'],
        '$P(A_2 \\mid B) = \\frac{0.3 \\times 0.2}{0.28} = \\frac{0.06}{0.28} = \\frac{3}{14}$។',
        bloom='Apply',
    ))

    # 23 (Analyze) - Two-stage ball transfer: Urn 1 (3R, 2B) -> move 1 ball to Urn 2 (2R, 3B), then draw 1 from Urn 2.
    # P(R2) = (3/5)*(3/6) + (2/5)*(2/6) = 9/30 + 4/30 = 13/30
    qs.append(mcq(
        'medium', S1,
        'ថង់ទី 1 មានប៊ូលក្រហម 3 ខៀវ 2 ។ ថង់ទី 2 មានប៊ូលក្រហម 2 ខៀវ 3 ។ ចាប់ 1 គ្រាប់ពីថង់ទី 1 ដាក់ចូលថង់ទី 2 រួចចាប់ 1 គ្រាប់ពីថង់ទី 2 ។ រកប្រូបាបដែលប៊ូលចាប់ពីថង់ទី 2 ពណ៌ក្រហម ។',
        r'$\frac{13}{30}$',
        [r'$\frac{1}{2}$', r'$\frac{2}{5}$', r'$\frac{7}{15}$'],
        '$P(R_2) = \\frac{3}{5}\\cdot\\frac{3}{6} + \\frac{2}{5}\\cdot\\frac{2}{6} = \\frac{9 + 4}{30} = \\frac{13}{30}$។',
        bloom='Analyze',
    ))

    # 24 (Analyze) - Bayes on Q23: P(R1 | R2) = (9/30)/(13/30) = 9/13
    qs.append(mcq(
        'medium', S2,
        'ក្នុងពិសោធន៍ផ្ទេរប៊ូលខាងលើ បើប៊ូលចាប់ចេញពីថង់ទី 2 ពណ៌ក្រហម តើប្រូបាបដែលប៊ូលផ្ទេរពីថង់ទី 1 ក៏ពណ៌ក្រហមដែរស្មើប៉ុន្មាន?',
        r'$\frac{9}{13}$',
        [r'$\frac{3}{5}$', r'$\frac{4}{13}$', r'$\frac{3}{10}$'],
        '$P(R_1 \\mid R_2) = \\frac{9/30}{13/30} = \\frac{9}{13}$។',
        bloom='Analyze',
    ))

    # =========================================================================
    # MCQ HARD (7)
    # =========================================================================
    # 25 (Analyze) - Village vaccination Bayes: P(V' | M) = 0.1485 / 0.1655 = 297/331
    qs.append(mcq(
        'hard', S3,
        'ភូមិមួយមាន 85% ចាក់ថ្នាំបង្ការ (2% ឆ្លងជំងឺ) និង 15% មិនចាក់ (99% ឆ្លងជំងឺ) ។ បើអ្នកភូមិម្នាក់ឆ្លងជំងឺ រកប្រូបាបដែលគាត់មិនបានចាក់ថ្នាំបង្ការ ។',
        r'$\frac{297}{331}$',
        [r'$\frac{34}{331}$', r'$\frac{15}{100}$', r'$\frac{297}{350}$'],
        '$P(\\overline{V} \\mid M) = \\frac{0.15(0.99)}{0.85(0.02) + 0.15(0.99)} = \\frac{0.1485}{0.1655} = \\frac{297}{331}$។',
        bloom='Analyze',
    ))

    # 26 (Analyze) - Medical test false positive: 1% sick, 99% healthy. Test+: 98% if sick, 5% if healthy.
    # P(Sick | +) = 0.0098 / (0.0098 + 0.0495) = 98 / 593
    qs.append(mcq(
        'hard', S3,
        '1% នៃប្រជាជនមានជំងឺ ។ តេស្តឲ្យលទ្ធផលវិជ្ជមាន 98% ចំពោះអ្នកឈឺ និង 5% ចំពោះអ្នកជា ។ បើមនុស្សម្នាក់តេស្តវិជ្ជមាន រកប្រូបាបដែលគាត់ពិតជាឈឺ ។',
        r'$\frac{98}{593}$',
        [r'$\frac{495}{593}$', r'$\frac{98}{100}$', r'$\frac{1}{5}$'],
        '$P(D \\mid +) = \\frac{0.01(0.98)}{0.01(0.98) + 0.99(0.05)} = \\frac{0.0098}{0.0593} = \\frac{98}{593}$។',
        bloom='Analyze',
    ))

    # 27 (Evaluate) - 3 chests: C1 (2G), C2 (1G, 1S), C3 (2S). Choose chest, draw 1 coin -> it's Gold. P(other is Gold) = P(C1 | G) = 2/3
    qs.append(mcq(
        'hard', S2,
        'មានប្រអប់ 3៖ ប្រអប់ទី 1 មានកាក់មាស 2, ប្រអប់ទី 2 មានមាស 1 ប្រាក់ 1, ប្រអប់ទី 3 មានប្រាក់ 2 ។ ជ្រើសប្រអប់មួយចាប់កាក់ 1 មកឃើញថាមាស ។ រកប្រូបាបដែលកាក់មួយទៀតក្នុងប្រអប់ដដែលជាមាសដែរ ។',
        r'$\frac{2}{3}$',
        [r'$\frac{1}{2}$', r'$\frac{1}{3}$', r'$\frac{3}{4}$'],
        'ករណីនេះសមមូលនឹង $P(C_1 \\mid G) = \\frac{(1/3)(1)}{(1/3)(1) + (1/3)(1/2) + 0} = \\frac{1}{3/2} = \\frac{2}{3}$។',
        bloom='Evaluate',
    ))

    # 28 (Analyze) - Ex 3b: 1500 defective items from A(40%,3%), B(35%,4%), C(25%,4%). How many from A? -> 500
    qs.append(mcq(
        'hard', S3,
        'ម៉ាស៊ីន $A, B, C$ ផលិត 40%, 35%, 25% ដោយមានអត្រាខូច 3%, 4%, 4% រៀងគ្នា ។ ក្នុងចំណោមវត្ថុខូចចំនួន $1500$ តើម៉ាស៊ីន $A$ ផលិតខូចចំនួនប៉ុន្មាន?',
        r'$500$',
        [r'$600$', r'$450$', r'$417$'],
        '$P(A \\mid D) = \\frac{0.012}{0.036} = \\frac{1}{3}$ ។ ដូច្នេះចំនួនខូចពី $A$ គឺ $1500 \\times \\frac{1}{3} = 500$។',
        bloom='Analyze',
    ))

    # 29 (Evaluate) - Email filter: 30% spam (80% has link), 70% ham (10% has link). P(spam | link) = 0.24 / (0.24 + 0.07) = 24/31
    qs.append(mcq(
        'hard', S3,
        '30% នៃអ៊ីមែលជា Spam (80% មានតំណភ្ជាប់) និង 70% ជាអ៊ីមែលធម្មតា (10% មានតំណភ្ជាប់) ។ បើអ៊ីមែលមួយមានតំណភ្ជាប់ រកប្រូបាបដែលវាជា Spam ។',
        r'$\frac{24}{31}$',
        [r'$\frac{7}{31}$', r'$\frac{4}{5}$', r'$\frac{24}{100}$'],
        '$P(\\text{Spam} \\mid \\text{Link}) = \\frac{0.30(0.80)}{0.30(0.80) + 0.70(0.10)} = \\frac{0.24}{0.31} = \\frac{24}{31}$។',
        bloom='Evaluate',
    ))

    # 30 (Analyze) - Multiple choice test: student knows answer with p=0.6, guesses among 4 choices with p=0.4 (1/4 correct).
    # P(knows | correct) = 0.6 / (0.6 + 0.4*0.25) = 0.6 / 0.7 = 6/7
    qs.append(mcq(
        'hard', S2,
        'សិស្សម្នាក់ចេះច្បាស់នូវសំណួរពហុជ្រើសរើស (មាន 4 ជម្រើស) ដោយប្រូបាប $0.6$ ហើយទាយចៃដន្យដោយប្រូបាប $0.4$ ។ បើគាត់ឆ្លើយត្រូវ រកប្រូបាបដែលគាត់ពិតជាចេះច្បាស់ ។',
        r'$\frac{6}{7}$',
        [r'$\frac{3}{5}$', r'$\frac{6}{10}$', r'$\frac{1}{7}$'],
        '$P(\\text{ចេះ} \\mid \\text{ត្រូវ}) = \\frac{0.6}{0.6 + 0.4 \\times 0.25} = \\frac{0.6}{0.7} = \\frac{6}{7}$។',
        bloom='Analyze',
    ))

    # 31 (Evaluate) - Coin tossed twice? No, 1 fair coin and 1 two-headed coin. Pick 1, toss twice -> both Heads.
    # P(2-headed | HH) = (0.5*1) / (0.5*1 + 0.5*0.25) = 1 / 1.25 = 4/5
    qs.append(mcq(
        'hard', S2,
        'ថង់មានកាក់ធម្មតា 1 និងកាក់ក្បាលទាំងសងខាង 1 ។ ជ្រើសកាក់ 1 បោះ 2 ដងឃើញចេញក្បាលទាំង 2 ដង ។ រកប្រូបាបដែលកាក់នោះជាកាក់ក្បាលទាំងសងខាង ។',
        r'$\frac{4}{5}$',
        [r'$\frac{2}{3}$', r'$\frac{1}{2}$', r'$\frac{3}{4}$'],
        '$P(\\text{ក្បាលទាំងពីរ} \\mid HH) = \\frac{0.5(1)}{0.5(1) + 0.5(0.25)} = \\frac{1}{1.25} = \\frac{4}{5}$។',
        bloom='Evaluate',
    ))

    # =========================================================================
    # MCQ PISA (5)
    # =========================================================================
    # 32 (Apply) - PISA: Ride-hailing cars: 70% Green (95% on time), 30% Blue (80% on time). P(on time) = 0.665 + 0.24 = 0.905
    qs.append(mcq(
        'pisa', S1,
        'ក្រុមហ៊ុនតាក់ស៊ីប្រើឡានបៃតង 70% (មកទាន់ពេល 95%) និងឡានខៀវ 30% (មកទាន់ពេល 80%) ។ រកប្រូបាបដែលតាក់ស៊ីចៃដន្យមួយមកទាន់ពេល ។',
        r'$0.905$',
        [r'$0.875$', r'$0.665$', r'$0.950$'],
        '$P(\\text{ទាន់ពេល}) = 0.70(0.95) + 0.30(0.80) = 0.665 + 0.240 = 0.905$។',
        bloom='Apply',
    ))

    # 33 (Analyze) - PISA: From Q32, if taxi was LATE (1 - 0.905 = 0.095), P(Blue | Late) = 0.30*0.20 / 0.095 = 0.06 / 0.095 = 12/19
    qs.append(mcq(
        'pisa', S2,
        'ក្នុងបញ្ហាតាក់ស៊ីខាងលើ (បៃតង 70% យឺត 5%; ខៀវ 30% យឺត 20%) បើតាក់ស៊ីមកយឺត រកប្រូបាបដែលវាជាឡានខៀវ ។',
        r'$\frac{12}{19}$',
        [r'$\frac{7}{19}$', r'$\frac{6}{10}$', r'$\frac{3}{10}$'],
        '$P(\\text{ខៀវ} \\mid \\text{យឺត}) = \\frac{0.30(0.20)}{0.70(0.05) + 0.30(0.20)} = \\frac{0.060}{0.095} = \\frac{12}{19}$។',
        bloom='Analyze',
    ))

    # 34 (Evaluate) - PISA: Airport security scanner: 2% carry restricted item (90% alarm), 98% don't (5% alarm).
    # P(Restricted | Alarm) = 0.018 / (0.018 + 0.049) = 18/67
    qs.append(mcq(
        'pisa', S3,
        'នៅព្រលានយន្តហោះ 2% នៃវ៉ាលីមានវត្ថុហាមឃាត់ (ម៉ាស៊ីនស្កេនរោទ៍ 90%) និង 98% គ្មានវត្ថុហាមឃាត់ (ម៉ាស៊ីនរោទ៍ច្រឡំ 5%) ។ បើម៉ាស៊ីនរោទ៍ រកប្រូបាបដែលវ៉ាលីនោះពិតជាមានវត្ថុហាមឃាត់ ។',
        r'$\frac{18}{67}$',
        [r'$\frac{49}{67}$', r'$\frac{9}{10}$', r'$\frac{18}{100}$'],
        '$P(R \\mid A) = \\frac{0.02(0.90)}{0.02(0.90) + 0.98(0.05)} = \\frac{0.018}{0.067} = \\frac{18}{67}$។',
        bloom='Evaluate',
    ))

    # 35 (Analyze) - PISA: Agricultural weather: El Nino 25% (drought prob 0.8), Normal 75% (drought prob 0.1).
    # P(El Nino | Drought) = 0.20 / (0.20 + 0.075) = 0.20 / 0.275 = 8/11
    qs.append(mcq(
        'pisa', S3,
        'ក្នុងតំបន់មួយ បាតុភូតអែលនីញ៉ូកើតមាន 25% នៃឆ្នាំ (ប្រូបាបរាំងស្ងួត $0.8$) និងឆ្នាំធម្មតា 75% (ប្រូបាបរាំងស្ងួត $0.1$) ។ បើឆ្នាំនេះរាំងស្ងួត រកប្រូបាបដែលបណ្តាលមកពីអែលនីញ៉ូ ។',
        r'$\frac{8}{11}$',
        [r'$\frac{3}{11}$', r'$\frac{4}{5}$', r'$\frac{1}{4}$'],
        '$P(E \\mid D) = \\frac{0.25(0.8)}{0.25(0.8) + 0.75(0.1)} = \\frac{0.200}{0.275} = \\frac{8}{11}$។',
        bloom='Analyze',
    ))

    # 36 (Create) - PISA: A factory wants P(Machine A | Defective) = 1/2. A produces p fraction with 2% defect, B produces (1-p) with 4% defect.
    # 0.02 p = 0.04 (1 - p) -> 0.06 p = 0.04 -> p = 2/3
    qs.append(mcq(
        'pisa', S3,
        'ម៉ាស៊ីន $A$ ផលិតសមាមាត្រ $p$ ដោយខូច 2% និងម៉ាស៊ីន $B$ ផលិត $(1-p)$ ដោយខូច 4% ។ កំណត់ $p$ ដើម្បីឲ្យបើជួបផលិតផលខូច ប្រូបាបដែលវាជាផលិតផលរបស់ម៉ាស៊ីន $A$ ស្មើ $\\frac{1}{2}$ ។',
        r'$p = \frac{2}{3}$',
        [r'$p = \frac{1}{2}$', r'$p = \frac{1}{3}$', r'$p = \frac{3}{4}$'],
        'ត្រូវការ $P(A \\cap D) = P(B \\cap D) \\iff 0.02p = 0.04(1 - p) \\iff 0.06p = 0.04 \\iff p = \\frac{2}{3}$។',
        bloom='Create',
    ))

    # =========================================================================
    # WRITING (14): 1 easy, 4 medium, 4 hard, 5 pisa
    # =========================================================================
    # 37 (Easy - Apply)
    qs.append(writing(
        'easy', S1,
        'គេមាន $P(A) = 0.3$, $P(B \\mid A) = 0.8$ និង $P(B \\mid \\overline{A}) = 0.4$ ។ គណនាប្រូបាបសរុប $P(B)$ ។',
        r'$0.52$',
        '$P(B) = 0.3(0.8) + 0.7(0.4) = 0.24 + 0.28 = 0.52$។',
        bloom='Apply',
    ))

    # 38 (Medium - Apply)
    qs.append(writing(
        'medium', S2,
        'ក្នុងទិន្នន័យ $P(A) = 0.3$, $P(B \\mid A) = 0.8$ និង $P(B \\mid \\overline{A}) = 0.4$ គណនា $P(A \\mid B)$ ។',
        r'$\frac{6}{13}$',
        '$P(B) = 0.52$ ដូច្នេះ $P(A \\mid B) = \\frac{0.24}{0.52} = \\frac{6}{13}$។',
        bloom='Apply',
    ))

    # 39 (Medium - Apply)
    qs.append(writing(
        'medium', S3,
        'ម៉ាស៊ីន $B_1, B_2, B_3$ ផលិត 30%, 45%, 25% រៀងគ្នា ដោយមានអត្រាខូច 2%, 3%, 2% រៀងគ្នា ។ គណនា $P(D)$ និង $P(B_2 \\mid D)$ ។',
        r'$P(D) = 0.0245,\; P(B_2 \mid D) = \frac{27}{49}$',
        '$P(D) = 0.006 + 0.0135 + 0.005 = 0.0245$ និង $P(B_2 \\mid D) = \\frac{0.0135}{0.0245} = \\frac{27}{49}$។',
        bloom='Apply',
    ))

    # 40 (Medium - Apply)
    qs.append(writing(
        'medium', S2,
        'ប្រអប់ $A$ មានប៊ូលស 4 ខ្មៅ 2 ។ ប្រអប់ $B$ មានប៊ូលស 3 ខ្មៅ 5 ។ ជ្រើសប្រអប់មួយដោយចៃដន្យ រួចចាប់ប៊ូល 1 គ្រាប់បានពណ៌ស ។ រកប្រូបាបដែលប៊ូលនោះចេញពីប្រអប់ $A$ ។',
        r'$\frac{16}{25}$',
        '$P(W) = \\frac{1}{2}\\cdot\\frac{4}{6} + \\frac{1}{2}\\cdot\\frac{3}{8} = \\frac{1}{3} + \\frac{3}{16} = \\frac{25}{48}$ ។ $P(A \\mid W) = \\frac{1/3}{25/48} = \\frac{16}{25}$។',
        bloom='Apply',
    ))

    # 41 (Medium - Analyze)
    qs.append(writing(
        'medium', S1,
        'កាក់ 100 កាក់មានកាក់ល្អ 25 ($P(C)=\\frac{1}{2}$) និងកាក់ល្អៀង 75 ($P(C)=\\frac{1}{3}$) ។ ចាប់កាក់មួយបោះ ។ គណនា $P(C)$ និង $P(B \\mid C)$ ដែល $B$ ជាកាក់ល្អៀង ។',
        r'$P(C) = \frac{3}{8},\; P(B \mid C) = \frac{2}{3}$',
        '$P(C) = \\frac{1}{4}\\cdot\\frac{1}{2} + \\frac{3}{4}\\cdot\\frac{1}{3} = \\frac{3}{8}$ និង $P(B \\mid C) = \\frac{1/4}{3/8} = \\frac{2}{3}$។',
        bloom='Analyze',
    ))

    # 42 (Hard - Analyze)
    qs.append(writing(
        'hard', S3,
        'ម៉ាស៊ីន $A, B, C$ ផលិត 50%, 30%, 20% ដោយខូច 3%, 4%, 4% រៀងគ្នា ។ បើផលិតផលចៃដន្យមួយខូច រកប្រូបាបដែលវាផលិតដោយម៉ាស៊ីន $A$, ម៉ាស៊ីន $B$ និងម៉ាស៊ីន $C$ ។',
        r'$P(A\mid D)=\frac{3}{7},\; P(B\mid D)=\frac{12}{35},\; P(C\mid D)=\frac{8}{35}$',
        '$P(D) = 0.015 + 0.012 + 0.008 = 0.035$ ។ ចែកនឹង $0.035$ បាន $\\frac{15}{35}=\\frac{3}{7}$, $\\frac{12}{35}$, $\\frac{8}{35}$។',
        bloom='Analyze',
    ))

    # 43 (Hard - Analyze)
    # Two-stage transfer: Box 1 (4R, 2B) -> move 1 to Box 2 (3R, 3B) -> draw 1 from Box 2 -> Red. Find P(R1 | R2).
    # P(R2) = (4/6)*(4/7) + (2/6)*(3/7) = 16/42 + 6/42 = 22/42 = 11/21. P(R1 | R2) = 16/22 = 8/11
    qs.append(writing(
        'hard', S2,
        'ប្រអប់ទី 1 មានប៊ូលក្រហម 4 ខៀវ 2 ។ ប្រអប់ទី 2 មានក្រហម 3 ខៀវ 3 ។ ចាប់ 1 គ្រាប់ពីប្រអប់ទី 1 ដាក់ចូលប្រអប់ទី 2 រួចចាប់ 1 គ្រាប់ពីប្រអប់ទី 2 ឃើញក្រហម ។ រកប្រូបាបដែលប៊ូលផ្ទេរពីប្រអប់ទី 1 ពណ៌ក្រហម ។',
        r'$\frac{8}{11}$',
        '$P(R_2) = \\frac{4}{6}\\cdot\\frac{4}{7} + \\frac{2}{6}\\cdot\\frac{3}{7} = \\frac{22}{42}$ ។ ដូច្នេះ $P(R_1 \\mid R_2) = \\frac{16/42}{22/42} = \\frac{8}{11}$។',
        bloom='Analyze',
    ))

    # 44 (Hard - Evaluate)
    # 3 bags: B1 (100% R), B2 (50% R), B3 (25% R). Pick bag, draw 2 with replacement -> both R. P(B1 | RR) = 1 / (1 + 1/4 + 1/16) = 16/21
    qs.append(writing(
        'hard', S2,
        'មានថង់ 3៖ ថង់ $B_1$ មានប៊ូលក្រហមសុទ្ធ, $B_2$ មានក្រហម $50\\%$, $B_3$ មានក្រហម $25\\%$ ។ ជ្រើសថង់ 1 ចាប់ប៊ូល 2 ដងដោយដាក់វិញ ឃើញក្រហមទាំង 2 ដង ។ រកប្រូបាបដែលវាជាថង់ $B_1$ ។',
        r'$\frac{16}{21}$',
        '$P(B_1 \\mid RR) = \\frac{1^2}{1^2 + (1/2)^2 + (1/4)^2} = \\frac{1}{1 + 1/4 + 1/16} = \\frac{16}{21}$។',
        bloom='Evaluate',
    ))

    # 45 (Hard - Create)
    # Student knows p=0.7, guesses among 5 choices with 0.3 (1/5 correct). Find P(knows | correct) and P(knows | wrong).
    # P(correct) = 0.7 + 0.3*0.2 = 0.76 -> P(knows | correct) = 0.7/0.76 = 35/38.
    qs.append(writing(
        'hard', S2,
        'សិស្សម្នាក់ចេះច្បាស់នូវសំណួរ 5 ជម្រើសដោយប្រូបាប $0.7$ និងទាយចៃដន្យដោយប្រូបាប $0.3$ ។ បើគាត់ឆ្លើយត្រូវ រកប្រូបាបដែលគាត់ពិតជាចេះច្បាស់ ។',
        r'$\frac{35}{38}$',
        '$P(\\text{ត្រូវ}) = 0.7 + 0.3\\left(\\frac{1}{5}\\right) = 0.76$ ។ ដូច្នេះ $P(\\text{ចេះ} \\mid \\text{ត្រូវ}) = \\frac{0.70}{0.76} = \\frac{35}{38}$។',
        bloom='Create',
    ))

    # 46 (PISA - Apply)
    # Vaccine: 80% vaccinated (5% sick), 20% unvaccinated (40% sick). P(Sick) and P(Unvax | Sick).
    # P(Sick) = 0.8*0.05 + 0.2*0.40 = 0.04 + 0.08 = 0.12. P(Unvax | Sick) = 0.08/0.12 = 2/3
    qs.append(writing(
        'pisa', S3,
        'ក្នុងសហគមន៍មួយ 80% បានចាក់វ៉ាក់សាំង (5% ឆ្លងជំងឺ) និង 20% មិនបានចាក់ (40% ឆ្លងជំងឺ) ។ បើអ្នកជំងឺម្នាក់ឆ្លងជំងឺ រកប្រូបាបដែលគាត់មិនបានចាក់វ៉ាក់សាំង ។',
        r'$\frac{2}{3}$',
        '$P(\\text{ឆ្លង}) = 0.8(0.05) + 0.2(0.40) = 0.12$ ។ $P(\\text{មិនចាក់} \\mid \\text{ឆ្លង}) = \\frac{0.08}{0.12} = \\frac{2}{3}$។',
        bloom='Apply',
    ))

    # 47 (PISA - Analyze)
    # 1500 defective items from Ex 3: A(40%,3%), B(35%,4%), C(25%,4%). Count from A, B, C.
    qs.append(writing(
        'pisa', S3,
        'ម៉ាស៊ីន $A, B, C$ ផលិត 40%, 35%, 25% ដោយខូច 3%, 4%, 4% រៀងគ្នា ។ ក្នុងចំណោមវត្ថុខូច 1500 គ្រឿង តើម៉ាស៊ីន $A, B, C$ នីមួយៗផលិតខូចប៉ុន្មានគ្រឿង (បង្គត់ជាចំនួនគត់)?',
        r'$A: 500,\; B: 583,\; C: 417$',
        '$P(A\\mid D)=\\frac{12}{36}$, $P(B\\mid D)=\\frac{14}{36}$, $P(C\\mid D)=\\frac{10}{36}$ ។ គុណនឹង $1500$ បាន $A=500, B\\approx 583, C\\approx 417$។',
        bloom='Analyze',
    ))

    # 48 (PISA - Evaluate)
    # Rapid COVID test: prevalence 4%, sensitivity 95%, specificity 90% (false positive 10%).
    # P(+) = 0.04*0.95 + 0.96*0.10 = 0.038 + 0.096 = 0.134. P(D | +) = 38/134 = 19/67
    qs.append(writing(
        'pisa', S3,
        'អត្រាជំងឺក្នុងសហគមន៍គឺ 4% ។ តេស្តរហ័សរកឃើញវិជ្ជមាន 95% ចំពោះអ្នកឈឺ និង 10% ចំពោះអ្នកជា ។ បើបុគ្គលម្នាក់តេស្តវិជ្ជមាន រកប្រូបាបដែលគាត់ពិតជាមានជំងឺ ។',
        r'$\frac{19}{67}$',
        '$P(+) = 0.04(0.95) + 0.96(0.10) = 0.038 + 0.096 = 0.134$ ។ $P(D \\mid +) = \\frac{0.038}{0.134} = \\frac{19}{67}$។',
        bloom='Evaluate',
    ))

    # 49 (PISA - Analyze)
    # Oil drilling: 30% chance oil exists. Test positive 85% if oil exists, 20% if no oil. Test is positive -> P(Oil | +) = 0.255 / (0.255 + 0.140) = 0.255/0.395 = 51/79
    qs.append(writing(
        'pisa', S2,
        'ក្រុមហ៊ុនរុករកប្រេងប៉ាន់ស្មានថាមានប្រេង 30% ។ ការស្ទង់ភូគព្ភសាស្ត្រផ្តល់សញ្ញាវិជ្ជមាន 85% បើមានប្រេង និង 20% បើគ្មានប្រេង ។ បើលទ្ធផលវិជ្ជមាន រកប្រូបាបដែលទីតាំងនោះពិតជាមានប្រេង ។',
        r'$\frac{51}{79}$',
        '$P(\\text{ប្រេង} \\mid +) = \\frac{0.30(0.85)}{0.30(0.85) + 0.70(0.20)} = \\frac{0.255}{0.395} = \\frac{51}{79}$។',
        bloom='Analyze',
    ))

    # 50 (PISA - Create)
    # Two-stage Bayes: Rare disease 1%, test 99% sens, 2% false pos. Patient tests positive TWICE independently.
    # P(D | ++) = 0.01*(0.99)^2 / (0.01*(0.99)^2 + 0.99*(0.02)^2) = 0.99 / (0.99 + 0.04) = 99/103
    qs.append(writing(
        'pisa', S3,
        'ជំងឺកម្រមួយកើតលើ 1% នៃប្រជាជន ។ តេស្តមានប្រូបាបវិជ្ជមាន 99% ចំពោះអ្នកឈឺ និង 2% ចំពោះអ្នកជា ។ បើអ្នកជំងឺតេស្ត 2 ដងឯករាជ្យគ្នា ហើយវិជ្ជមានទាំង 2 ដង រកប្រូបាបដែលគាត់ពិតជាឈឺ ។',
        r'$\frac{99}{103}$',
        '$P(D \\mid ++) = \\frac{0.01(0.99)^2}{0.01(0.99)^2 + 0.99(0.02)^2} = \\frac{0.99}{0.99 + 0.04} = \\frac{99}{103}$។',
        bloom='Create',
    ))

    return qs


def _verify_math():
    assert Fraction(1, 8) / Fraction(3, 8) == Fraction(1, 3)
    assert Fraction(25, 60) == Fraction(5, 12)
    assert abs(0.85 * 0.02 + 0.15 * 0.99 - 0.1655) < 1e-12
    assert Fraction(50, 245) == Fraction(10, 49)
    assert Fraction(15, 35) == Fraction(3, 7)
    assert Fraction(9, 30) + Fraction(4, 30) == Fraction(13, 30)
    assert Fraction(98, 593) + Fraction(495, 593) == 1
    assert Fraction(1, 1) / (Fraction(1, 1) + Fraction(1, 4) + Fraction(1, 16)) == Fraction(16, 21)
    assert Fraction(99, 103) == Fraction(1 * 99 * 99, 1 * 99 * 99 + 99 * 2 * 2)


cands = build_candidates


if __name__ == '__main__':
    _verify_math()
    qs = build_candidates()
    print(f'{LESSON}: built {len(qs)} candidates, verified')
