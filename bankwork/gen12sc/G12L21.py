"""Bank generator for Grade 12 Science — Lesson 21: ប្រូបាបមានលក្ខខណ្ឌ."""
from fractions import Fraction
import mpmath as mp
from lib import mcq, wr

LESSON = 'ប្រូបាបមានលក្ខខណ្ឌ'
CHAPTER = 'ជំពូកទី 8 : ប្រូបាប'
TARGET = {
    ('mcq', 'easy'): 10, ('mcq', 'medium'): 14, ('mcq', 'hard'): 7, ('mcq', 'pisa'): 5,
    ('writing', 'easy'): 1, ('writing', 'medium'): 4, ('writing', 'hard'): 4, ('writing', 'pisa'): 5,
}

S1 = '១. ប្រូបាបនៃព្រឹត្តិការណ៍ និងប្រូបាបមានលក្ខខណ្ឌ'
S2 = '២. ដ្យាក្រាមដើមឈើ និងរូបមន្តផលគុណប្រូបាប'
S3 = '៣. ព្រឹត្តិការណ៍មិនអាស្រ័យគ្នា និងចំណោទអនុវត្តន៍'


def writing(level, sec, stem, ans, sol, bloom=None):
    return wr(level, sec, stem, [(sol, 3), (f'ចម្លើយ៖ {ans}', 2)], bloom=bloom)


def svg_tree():
    w, h = 250, 145
    return (
        f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg">'
        f'<line x1="20" y1="72" x2="95" y2="38" stroke="#2b6cb0" stroke-width="1.8"/>'
        f'<line x1="20" y1="72" x2="95" y2="108" stroke="#c53030" stroke-width="1.8"/>'
        f'<line x1="95" y1="38" x2="180" y2="20" stroke="#2b6cb0" stroke-width="1.5"/>'
        f'<line x1="95" y1="38" x2="180" y2="56" stroke="#718096" stroke-width="1.5"/>'
        f'<line x1="95" y1="108" x2="180" y2="90" stroke="#c53030" stroke-width="1.5"/>'
        f'<line x1="95" y1="108" x2="180" y2="126" stroke="#718096" stroke-width="1.5"/>'
        f'<text x="48" y="48" font-size="10" fill="#2b6cb0">0.45</text>'
        f'<text x="48" y="102" font-size="10" fill="#c53030">0.55</text>'
        f'<text x="95" y="33" font-size="11" font-weight="bold">F</text>'
        f'<text x="95" y="122" font-size="11" font-weight="bold">B</text>'
        f'<text x="132" y="24" font-size="10">0.30</text>'
        f'<text x="132" y="55" font-size="10">0.70</text>'
        f'<text x="132" y="94" font-size="10">0.60</text>'
        f'<text x="132" y="125" font-size="10">0.40</text>'
        f'<text x="186" y="24" font-size="10">C</text>'
        f'<text x="186" y="60" font-size="10">C̄</text>'
        f'<text x="186" y="94" font-size="10">C</text>'
        f'<text x="186" y="130" font-size="10">C̄</text>'
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
        'បើ $A$ និង $B$ ជាព្រឹត្តិការណ៍ពីរដែល $P(B) > 0$ តើប្រូបាបមានលក្ខខណ្ឌ $P(A \\mid B)$ កំណត់ដោយរូបមន្តណា?',
        r'$P(A \mid B) = \frac{P(A \cap B)}{P(B)}$',
        [r'$P(A \mid B) = \frac{P(A \cap B)}{P(A)}$', r'$P(A \mid B) = \frac{P(A \cup B)}{P(B)}$', r'$P(A \mid B) = P(A) \cdot P(B)$'],
        'តាមនិយមន័យ ប្រូបាបនៃ $A$ កាលណាដឹង $B$ កើតឡើងគឺ $P(A \\mid B) = \\frac{P(A \\cap B)}{P(B)}$។',
        bloom='Remember',
    ))

    # 2 (Remember)
    qs.append(mcq(
        'easy', S3,
        'តើព្រឹត្តិការណ៍ពីរ $A$ និង $B$ មិនអាស្រ័យគ្នា លុះត្រាតែលក្ខខណ្ឌណាពិត?',
        r'$P(A \cap B) = P(A) \cdot P(B)$',
        [r'$P(A \cap B) = 0$', r'$P(A \cup B) = P(A) + P(B)$', r'$P(A \mid B) = 0$'],
        'ព្រឹត្តិការណ៍ $A$ និង $B$ មិនអាស្រ័យគ្នា លុះត្រាតែ $P(A \\cap B) = P(A) \\cdot P(B)$។',
        bloom='Remember',
    ))

    # 3 (Apply)
    qs.append(mcq(
        'easy', S1,
        'គេមាន $P(A) = \\frac{1}{2}$, $P(B) = \\frac{1}{3}$ និង $P(A \\cap B) = \\frac{1}{4}$ ។ គណនា $P(A \\mid B)$ ។',
        r'$\frac{3}{4}$',
        [r'$\frac{1}{2}$', r'$\frac{1}{12}$', r'$\frac{2}{3}$'],
        '$P(A \\mid B) = \\frac{P(A \\cap B)}{P(B)} = \\frac{1/4}{1/3} = \\frac{3}{4}$។',
        bloom='Apply',
    ))

    # 4 (Apply)
    qs.append(mcq(
        'easy', S1,
        'គេមាន $P(A) = \\frac{1}{2}$, $P(B) = \\frac{1}{3}$ និង $P(A \\cap B) = \\frac{1}{4}$ ។ គណនា $P(B \\mid A)$ ។',
        r'$\frac{1}{2}$',
        [r'$\frac{3}{4}$', r'$\frac{1}{3}$', r'$\frac{1}{6}$'],
        '$P(B \\mid A) = \\frac{P(A \\cap B)}{P(A)} = \\frac{1/4}{1/2} = \\frac{1}{2}$។',
        bloom='Apply',
    ))

    # 5 (Apply)
    qs.append(mcq(
        'easy', S3,
        'បើ $A$ និង $B$ ជាព្រឹត្តិការណ៍មិនអាស្រ័យគ្នាដែល $P(A) = 0.4$ និង $P(B) = 0.5$ តើ $P(A \\cap B)$ ស្មើនឹងប៉ុន្មាន?',
        r'$0.20$',
        [r'$0.90$', r'$0.10$', r'$0.80$'],
        'ដោយ $A, B$ មិនអាស្រ័យគ្នា $P(A \\cap B) = 0.4 \\times 0.5 = 0.20$។',
        bloom='Apply',
    ))

    # 6 (Understand)
    qs.append(mcq(
        'easy', S3,
        'បើ $A$ និង $B$ មិនអាស្រ័យគ្នា ហើយ $P(A) = 0.6$ តើ $P(A \\mid B)$ ស្មើនឹងប៉ុន្មាន?',
        r'$0.6$',
        [r'$0.4$', r'$0$', r'$1$'],
        'ដោយ $A, B$ មិនអាស្រ័យគ្នា ការកើតឡើងនៃ $B$ មិនប៉ះពាល់ប្រូបាបនៃ $A$ ទេ ដូច្នេះ $P(A \\mid B) = P(A) = 0.6$។',
        bloom='Understand',
    ))

    # 7 (Apply)
    qs.append(mcq(
        'easy', S2,
        'បើ $P(A) = 0.6$ និង $P(B \\mid A) = 0.5$ តើ $P(A \\cap B)$ ស្មើនឹងប៉ុន្មាន?',
        r'$0.30$',
        [r'$1.10$', r'$0.10$', r'$0.83$'],
        '$P(A \\cap B) = P(A) \\cdot P(B \\mid A) = 0.6 \\times 0.5 = 0.30$។',
        bloom='Apply',
    ))

    # 8 (Understand)
    svg8 = svg_tree()
    qs.append(mcq(
        'easy', S2,
        f'ពិនិត្យដ្យាក្រាមដើមឈើខាងក្រោម ។ គណនា $P(F \\cap C)$ ។<br/>{svg8}',
        r'$0.135$',
        [r'$0.75$', r'$0.315$', r'$0.330$'],
        '$P(F \\cap C) = P(F) \\cdot P(C \\mid F) = 0.45 \\times 0.30 = 0.135$។',
        bloom='Understand',
    ))

    # 9 (Apply)
    qs.append(mcq(
        'easy', S1,
        'គេបោះគ្រាប់ឡុកឡាក់ត្រឹមត្រូវមួយ ១ ដង ។ តាង $A$ ជាព្រឹត្តិការណ៍ «ចេញលេខគូ» និង $B$ ជាព្រឹត្តិការណ៍ «ចេញលេខធំជាង 3» ។ គណនា $P(A \\mid B)$ ។',
        r'$\frac{2}{3}$',
        [r'$\frac{1}{2}$', r'$\frac{1}{3}$', r'$\frac{1}{6}$'],
        '$B = \\{4, 5, 6\\}$ និង $A \\cap B = \\{4, 6\\}$ ដូច្នេះ $P(A \\mid B) = \\frac{2}{3}$។',
        bloom='Apply',
    ))

    # 10 (Remember)
    qs.append(mcq(
        'easy', S1,
        'ដើម្បីកំណត់ប្រូបាបប្រសព្វ $P(A \\cap B) = P(B) \\cdot P(A \\mid B)$ តើលក្ខខណ្ឌចាំបាច់លើ $P(B)$ គឺជាអ្វី?',
        r'$P(B) > 0$',
        [r'$P(B) = 0$', r'$P(B) = 1$', r'$P(B) < 0$'],
        'ដើម្បីកំណត់ $P(A \\mid B) = \\frac{P(A \\cap B)}{P(B)}$ ត្រូវតែមាន $P(B) > 0$។',
        bloom='Remember',
    ))

    # =========================================================================
    # MCQ MEDIUM (14)
    # =========================================================================
    # 11 (Apply) - Ex 1: 2 dice, different faces -> one is 1 -> 10/30 = 1/3
    qs.append(mcq(
        'medium', S1,
        'គេបោះគ្រាប់ឡុកឡាក់ 2 គ្រាប់ខុសគ្នា ។ រកប្រូបាបដែលគ្រាប់ឡុកឡាក់មួយចេញលេខ $1$ ដោយដឹងថាគ្រាប់ឡុកឡាក់ទាំង 2 ចេញលេខខុសគ្នា ។',
        r'$\frac{1}{3}$',
        [r'$\frac{1}{6}$', r'$\frac{11}{36}$', r'$\frac{5}{18}$'],
        'ករណីលេខខុសគ្នាមាន $30$ ករណី ហើយក្នុងនោះមាន $10$ ករណីមានលេខ $1$ ។ ដូច្នេះ $P = \\frac{10}{30} = \\frac{1}{3}$។',
        bloom='Apply',
    ))

    # 12 (Apply) - Ex 3: Math/English satisfaction table -> 55/125 = 11/25
    qs.append(mcq(
        'medium', S1,
        'ក្នុងការស្ទាបស្ទង់មនុស្ស 200 នាក់៖ ជំនាញគណិតវិទ្យាមាន 55 នាក់ពេញចិត្ត និង 70 នាក់មិនពេញចិត្ត; ជំនាញអង់គ្លេសមាន 35 នាក់ពេញចិត្ត និង 40 នាក់មិនពេញចិត្ត ។ បើជ្រើសបានអ្នកជំនាញគណិតវិទ្យា តើប្រូបាបដែលគាត់ពេញចិត្តស្មើប៉ុន្មាន?',
        r'$\frac{11}{25}$',
        [r'$\frac{11}{40}$', r'$\frac{9}{20}$', r'$\frac{7}{15}$'],
        '$P(\\text{ពេញចិត្ត} \\mid \\text{គណិត}) = \\frac{55}{55 + 70} = \\frac{55}{125} = \\frac{11}{25}$។',
        bloom='Apply',
    ))

    # 13 (Apply) - Ex 4a: 8 black, 5 white, 3 green (16 total), 2 without replacement -> both black = 7/30
    qs.append(mcq(
        'medium', S2,
        'ប្រអប់មួយមានថាសខ្មៅ 8, ស 5 និងបៃតង 3 ។ គេចាប់យក 2 ថាសម្តងមួយៗដោយមិនដាក់វិញ ។ រកប្រូបាបដើម្បីបានថាសទាំងពីរពណ៌ខ្មៅ ។',
        r'$\frac{7}{30}$',
        [r'$\frac{1}{4}$', r'$\frac{1}{12}$', r'$\frac{4}{15}$'],
        '$P = \\frac{8}{16} \\times \\frac{7}{15} = \\frac{7}{30}$។',
        bloom='Apply',
    ))

    # 14 (Apply) - Ex 4c: 1st white, 2nd green = (5/16)*(3/15) = 1/16
    qs.append(mcq(
        'medium', S2,
        'ប្រអប់មួយមានថាសខ្មៅ 8, ស 5 និងបៃតង 3 ។ គេចាប់យក 2 ថាសម្តងមួយៗដោយមិនដាក់វិញ ។ រកប្រូបាបដើម្បីបានទី 1 ពណ៌ស និងទី 2 ពណ៌បៃតង ។',
        r'$\frac{1}{16}$',
        [r'$\frac{15}{256}$', r'$\frac{1}{12}$', r'$\frac{3}{32}$'],
        '$P = \\frac{5}{16} \\times \\frac{3}{15} = \\frac{1}{16}$។',
        bloom='Apply',
    ))

    # 15 (Apply) - Ex 6: 18 people (8 women: 5 coffee; 10 men: 8 coffee). P(woman or coffee) = 16/18 = 8/9
    qs.append(mcq(
        'medium', S1,
        'ក្នុងមនុស្ស 18 នាក់ មានស្ត្រី 8 នាក់ (5 នាក់ចូលចិត្តកាហ្វេ) និងបុរស 10 នាក់ (8 នាក់ចូលចិត្តកាហ្វេ) ។ ជ្រើសមនុស្សម្នាក់ដោយចៃដន្យ ។ រកប្រូបាបដែលគាត់ជាស្ត្រី ឬចូលចិត្តកាហ្វេ ។',
        r'$\frac{8}{9}$',
        [r'$\frac{13}{18}$', r'$\frac{7}{9}$', r'$\frac{5}{9}$'],
        '$n(W \\cup C) = n(W) + n(C) - n(W \\cap C) = 8 + 13 - 5 = 16$ ។ ដូច្នេះ $P = \\frac{16}{18} = \\frac{8}{9}$។',
        bloom='Apply',
    ))

    # 16 (Apply) - Ex 9f: 840 students, M=(80 D, 460 IT -> 540), F=(160 D, 140 IT -> 300). P(IT | M) = 460/540 = 23/27
    qs.append(mcq(
        'medium', S1,
        'និស្សិត 840 នាក់៖ ប្រុស 540 នាក់ (ឌីហ្សាញ 80, គ្រប់គ្រងព័ត៌មាន 460) និងស្រី 300 នាក់ (ឌីហ្សាញ 160, គ្រប់គ្រងព័ត៌មាន 140) ។ បើជ្រើសបាននិស្សិតប្រុស រកប្រូបាបដែលគាត់រៀនគ្រប់គ្រងព័ត៌មាន ។',
        r'$\frac{23}{27}$',
        [r'$\frac{23}{42}$', r'$\frac{4}{27}$', r'$\frac{9}{14}$'],
        '$P(\\text{IT} \\mid \\text{ប្រុស}) = \\frac{460}{540} = \\frac{23}{27}$។',
        bloom='Apply',
    ))

    # 17 (Apply) - Ex 8b: P(boy)=0.54, P(girl)=0.46. Two children, one boy one girl -> 2*0.54*0.46 = 0.4968
    qs.append(mcq(
        'medium', S3,
        'ឧបមាថាកំណើតប្រុសមានប្រូបាប $0.54$ និងស្រី $0.46$ ដោយឯករាជ្យ ។ គូស្រករមួយមានកូន 2 នាក់ ។ គណនាប្រូបាបដែលបានកូនប្រុសមួយ និងស្រីមួយ ។',
        r'$0.4968$',
        [r'$0.2484$', r'$0.2916$', r'$0.2116$'],
        '$P = P(BG) + P(GB) = 2(0.54)(0.46) = 0.4968$។',
        bloom='Apply',
    ))

    # 18 (Apply) - P(A) = 0.5, P(B) = 0.6, P(A U B) = 0.8 -> P(A and B) = 0.3 -> P(A|B) = 0.3/0.6 = 0.5
    qs.append(mcq(
        'medium', S1,
        'គេមាន $P(A) = 0.5$, $P(B) = 0.6$ និង $P(A \\cup B) = 0.8$ ។ គណនា $P(A \\mid B)$ ។',
        r'$0.5$',
        [r'$0.6$', r'$0.3$', r'$0.8$'],
        '$P(A \\cap B) = 0.5 + 0.6 - 0.8 = 0.3$ ។ ដូច្នេះ $P(A \\mid B) = \\frac{0.3}{0.6} = 0.5$។',
        bloom='Apply',
    ))

    # 19 (Analyze) - 200 students: 90 F (27 univ), 110 M (66 univ). P(univ | F) = 27/90 = 0.3
    qs.append(mcq(
        'medium', S1,
        'សិស្សចប់វិទ្យាល័យ 200 នាក់មានស្រី 90 នាក់ (27 នាក់បន្តឧត្តមសិក្សា) និងប្រុស 110 នាក់ (66 នាក់បន្តឧត្តមសិក្សា) ។ រកប្រូបាបដែលសិស្សម្នាក់បន្តឧត្តមសិក្សា បើដឹងថាគាត់ជាសិស្សស្រី ។',
        r'$0.30$',
        [r'$0.135$', r'$0.60$', r'$0.27$'],
        '$P(\\text{ឧត្តម} \\mid \\text{ស្រី}) = \\frac{27}{90} = 0.30$។',
        bloom='Analyze',
    ))

    # 20 (Apply) - 3 white, 2 black balls with replacement. Both white -> (3/5)^2 = 9/25
    qs.append(mcq(
        'medium', S3,
        'ថង់មួយមានប៊ូលស 3 និងប៊ូលខ្មៅ 2 ។ គេចាប់ប៊ូល 2 ដងម្តងមួយៗដោយដាក់វិញ ។ រកប្រូបាបដែលបានប៊ូលសទាំង 2 ដង ។',
        r'$\frac{9}{25}$',
        [r'$\frac{3}{10}$', r'$\frac{6}{25}$', r'$\frac{4}{25}$'],
        'ដោយដាក់វិញ ព្រឹត្តិការណ៍ទាំងពីរមិនអាស្រ័យគ្នា៖ $P = \\frac{3}{5} \\times \\frac{3}{5} = \\frac{9}{25}$។',
        bloom='Apply',
    ))

    # 21 (Analyze) - Ex 7: 2 dice (x, y), x^2 < 4y -> 17/36
    qs.append(mcq(
        'medium', S1,
        'គេបោះគ្រាប់ឡុកឡាក់ 2 គ្រាប់ព្រមគ្នា តាង $x$ ជាលេខលើគ្រាប់ទី 1 និង $y$ ជាលេខលើគ្រាប់ទី 2 ។ រកប្រូបាបដែល $x^2 < 4y$ ។',
        r'$\frac{17}{36}$',
        [r'$\frac{1}{2}$', r'$\frac{5}{12}$', r'$\frac{4}{9}$'],
        'មាន 17 គូ $(x,y)$ ផ្ទៀងផ្ទាត់ $x^2 < 4y$ ($x=1$: 6 គូ, $x=2$: 5 គូ, $x=3$: 4 គូ, $x=4$: 2 គូ) ដូច្នេះ $P = \\frac{17}{36}$។',
        bloom='Analyze',
    ))

    # 22 (Apply) - 12 items (4 defective), draw 2 without replacement -> both good: C(8,2)/C(12,2) = 28/66 = 14/33
    qs.append(mcq(
        'medium', S2,
        'ទំនិញ 12 មុខមាន 4 មុខខូច ។ គេជ្រើសរើស 2 មុខដោយចៃដន្យមិនដាក់វិញ ។ គណនាប្រូបាបដែលទំនិញទាំង 2 មុខជាទំនិញល្អ ។',
        r'$\frac{14}{33}$',
        [r'$\frac{1}{11}$', r'$\frac{16}{33}$', r'$\frac{4}{9}$'],
        '$P = \\frac{8}{12} \\times \\frac{7}{11} = \\frac{14}{33}$។',
        bloom='Apply',
    ))

    # 23 (Analyze) - check independence: P(A)=1/2, P(B)=1/3, P(A and B)=1/4
    qs.append(mcq(
        'medium', S3,
        'គេមាន $P(A) = \\frac{1}{2}$, $P(B) = \\frac{1}{3}$ និង $P(A \\cap B) = \\frac{1}{4}$ ។ តើព្រឹត្តិការណ៍ $A$ និង $B$ ដូចម្តេច?',
        r'អាស្រ័យគ្នា ព្រោះ $P(A \cap B) \neq P(A)P(B)$',
        [r'មិនអាស្រ័យគ្នា ព្រោះ $P(A \cap B) = P(A)P(B)$', r'មិនចុះសម្រុងគ្នា ព្រោះ $P(A \cap B) = 0$', r'ផ្ទុយគ្នា ព្រោះ $P(A) + P(B) < 1$'],
        '$P(A)P(B) = \\frac{1}{6} \\neq \\frac{1}{4} = P(A \\cap B)$ ដូច្នេះ $A$ និង $B$ អាស្រ័យគ្នា។',
        bloom='Analyze',
    ))

    # 24 (Apply) - P(A|B) = 0.4, P(B) = 0.5, P(A) = 0.3 -> P(B|A) = 0.2/0.3 = 2/3
    qs.append(mcq(
        'medium', S1,
        'គេមាន $P(A) = 0.3$, $P(B) = 0.5$ និង $P(A \\mid B) = 0.4$ ។ គណនា $P(B \\mid A)$ ។',
        r'$\frac{2}{3}$',
        [r'$\frac{3}{5}$', r'$\frac{1}{5}$', r'$\frac{4}{5}$'],
        '$P(A \\cap B) = P(B)P(A \\mid B) = 0.5 \\times 0.4 = 0.2$ ។ ដូច្នេះ $P(B \\mid A) = \\frac{0.2}{0.3} = \\frac{2}{3}$។',
        bloom='Apply',
    ))

    # =========================================================================
    # MCQ HARD (7)
    # =========================================================================
    # 25 (Analyze) - Ex 2a: 5 Red, 1 Black, draw 3 without replacement. P(A|B) = 4/5
    qs.append(mcq(
        'hard', S1,
        'ថង់មួយមានប៊ូលក្រហម 5 និងប៊ូលខ្មៅ 1 ។ គេចាប់ម្តងមួយៗ 3 ដងដោយមិនដាក់វិញ ។ តាង $A$: «លើកទី 1 ក្រហម», $B$: «លើកទី 2 ក្រហម» ។ គណនា $P(A \\mid B)$ ។',
        r'$\frac{4}{5}$',
        [r'$\frac{5}{6}$', r'$\frac{2}{3}$', r'$\frac{3}{4}$'],
        '$P(A \\cap B) = \\frac{5}{6}\\cdot\\frac{4}{5} = \\frac{2}{3}$ និង $P(B) = \\frac{5}{6}$ ដូច្នេះ $P(A \\mid B) = \\frac{2/3}{5/6} = \\frac{4}{5}$។',
        bloom='Analyze',
    ))

    # 26 (Analyze) - Ex 2a: same setup, P(A|C) where C = 3rd is Black -> 1
    qs.append(mcq(
        'hard', S1,
        'ថង់មួយមានប៊ូលក្រហម 5 និងប៊ូលខ្មៅ 1 ។ ចាប់ម្តងមួយៗ 3 ដងមិនដាក់វិញ ។ តាង $A$: «លើកទី 1 ក្រហម», $C$: «លើកទី 3 ខ្មៅ» ។ គណនា $P(A \\mid C)$ ។',
        r'$1$',
        [r'$\frac{5}{6}$', r'$\frac{4}{5}$', r'$\frac{1}{6}$'],
        'ដោយមានប៊ូលខ្មៅតែ 1 គ្រាប់ បើលើកទី 3 ចាប់បានខ្មៅ នោះលើកទី 1 ប្រាកដជាចាប់បានក្រហម ដូច្នេះ $P(A \\mid C) = 1$។',
        bloom='Analyze',
    ))

    # 27 (Analyze) - Village vaccination: 78% vaccinated (4% infected), 22% unvaccinated (2% NOT infected -> 98% infected).
    # P(infected) = 0.78*0.04 + 0.22*0.98 = 0.0312 + 0.2156 = 0.2468
    qs.append(mcq(
        'hard', S2,
        'ក្នុងភូមិមួយ 78% ចាក់ថ្នាំបង្ការ (ក្នុងនោះ 4% ឆ្លងជំងឺ) និង 22% មិនចាក់ថ្នាំបង្ការ (ក្នុងនោះ 2% មិនឆ្លងជំងឺ) ។ រកប្រូបាបដែលអ្នកភូមិម្នាក់ឆ្លងជំងឺ ។',
        r'$0.2468$',
        [r'$0.0356$', r'$0.7532$', r'$0.2156$'],
        '$P(\\text{ឆ្លង}) = 0.78 \\times 0.04 + 0.22 \\times 0.98 = 0.0312 + 0.2156 = 0.2468$។',
        bloom='Analyze',
    ))

    # 28 (Evaluate) - P(A | B) = 0.6, P(A | B') = 0.2, P(B) = 0.3 -> P(A) = 0.3*0.6 + 0.7*0.2 = 0.18 + 0.14 = 0.32
    qs.append(mcq(
        'hard', S2,
        'គេមាន $P(B) = 0.3$, $P(A \\mid B) = 0.6$ និង $P(A \\mid \\overline{B}) = 0.2$ ។ គណនា $P(A)$ ។',
        r'$0.32$',
        [r'$0.40$', r'$0.18$', r'$0.44$'],
        '$P(A) = P(B)P(A \\mid B) + P(\\overline{B})P(A \\mid \\overline{B}) = 0.3(0.6) + 0.7(0.2) = 0.32$។',
        bloom='Evaluate',
    ))

    # 29 (Analyze) - Two cards drawn from 52 without replacement -> P(2nd Ace | 1st Ace) = 3/51 = 1/17
    qs.append(mcq(
        'hard', S1,
        'គេចាប់សន្លឹកបៀ 2 សន្លឹកម្តងមួយៗដោយមិនដាក់វិញពីបៀ 52 សន្លឹក ។ គណនាប្រូបាបដែលសន្លឹកទី 2 ជាអាត់ ($A$) ដោយដឹងថាសន្លឹកទី 1 ជាអាត់ ។',
        r'$\frac{1}{17}$',
        [r'$\frac{1}{13}$', r'$\frac{3}{52}$', r'$\frac{4}{51}$'],
        'ក្រោយចាប់អាត់ 1 សន្លឹក នៅសល់ 51 សន្លឹកដែលមានអាត់ 3 សន្លឹក ដូច្នេះ $P = \\frac{3}{51} = \\frac{1}{17}$។',
        bloom='Analyze',
    ))

    # 30 (Evaluate) - Independent A, B with P(A) = 0.4, P(A U B) = 0.7 -> 0.4 + P(B) - 0.4*P(B) = 0.7 -> 0.6 P(B) = 0.3 -> P(B) = 0.5
    qs.append(mcq(
        'hard', S3,
        'តាង $A$ និង $B$ ជាព្រឹត្តិការណ៍មិនអាស្រ័យគ្នា ។ បើ $P(A) = 0.4$ និង $P(A \\cup B) = 0.7$ តើ $P(B)$ ស្មើនឹងប៉ុន្មាន?',
        r'$0.5$',
        [r'$0.3$', r'$0.6$', r'$0.4$'],
        '$0.7 = 0.4 + P(B) - 0.4P(B) \\implies 0.6P(B) = 0.3 \\implies P(B) = 0.5$។',
        bloom='Evaluate',
    ))

    # 31 (Evaluate) - 2 dice sum is 8, P(at least one 3 | sum=8) -> sum=8: (2,6),(3,5),(4,4),(5,3),(6,2) [5 ways], with 3: 2 ways -> 2/5
    qs.append(mcq(
        'hard', S1,
        'គេបោះគ្រាប់ឡុកឡាក់ 2 គ្រាប់ព្រមគ្នា ។ បើដឹងថាផលបូកលេខលើមុខទាំងពីរស្មើ $8$ រកប្រូបាបដែលយ៉ាងហោចណាស់មានគ្រាប់មួយចេញលេខ $3$ ។',
        r'$\frac{2}{5}$',
        [r'$\frac{1}{5}$', r'$\frac{1}{3}$', r'$\frac{11}{36}$'],
        'ករណីផលបូកស្មើ $8$ មាន $5$ ករណី៖ $(2,6),(3,5),(4,4),(5,3),(6,2)$ ។ ក្នុងនោះមាន $2$ ករណីមានលេខ $3$ ដូច្នេះ $P = \\frac{2}{5}$។',
        bloom='Evaluate',
    ))

    # =========================================================================
    # MCQ PISA (5)
    # =========================================================================
    # 32 (Apply) - PISA: Medical test: 5% have disease, test sensitivity 90%, false positive 10%. P(Test+ | Disease) = 0.90 -> P(D and +) = 0.045
    qs.append(mcq(
        'pisa', S2,
        'ជំងឺម្យ៉ាងកើតលើ 5% នៃប្រជាជន ។ តេស្តរកជំងឺផ្តល់លទ្ធផលវិជ្ជមានត្រឹមត្រូវ 90% ចំពោះអ្នកមានជំងឺ ។ តើប្រូបាបដែលមនុស្សម្នាក់មានជំងឺផង និងតេស្តវិជ្ជមានផង ស្មើនឹងប៉ុន្មាន?',
        r'$0.045$',
        [r'$0.05$', r'$0.90$', r'$0.45$'],
        '$P(D \\cap T^+) = P(D) \\cdot P(T^+ \\mid D) = 0.05 \\times 0.90 = 0.045$។',
        bloom='Apply',
    ))

    # 33 (Analyze) - PISA: Weather forecast: P(Rain) = 0.30, P(Traffic | Rain) = 0.80, P(Traffic | No Rain) = 0.20 -> P(Traffic) = 0.24 + 0.14 = 0.38
    qs.append(mcq(
        'pisa', S2,
        'ប្រូបាបដែលភ្លៀងធ្លាក់ថ្ងៃនេះគឺ $0.30$ ។ បើភ្លៀង ប្រូបាបស្ទះចរាចរណ៍គឺ $0.80$; បើមិនភ្លៀង ប្រូបាបស្ទះចរាចរណ៍គឺ $0.20$ ។ រកប្រូបាបសរុបដែលស្ទះចរាចរណ៍ថ្ងៃនេះ ។',
        r'$0.38$',
        [r'$0.50$', r'$0.24$', r'$0.44$'],
        '$P(\\text{ស្ទះ}) = 0.30(0.80) + 0.70(0.20) = 0.24 + 0.14 = 0.38$។',
        bloom='Analyze',
    ))

    # 34 (Evaluate) - PISA: Two factory machines A (60%, 2% defect) and B (40%, 5% defect). P(defect) = 0.012 + 0.020 = 0.032
    qs.append(mcq(
        'pisa', S2,
        'រោងចក្រមួយមានម៉ាស៊ីន $A$ ផលិត 60% នៃទិន្នផល (ខូច 2%) និងម៉ាស៊ីន $B$ ផលិត 40% (ខូច 5%) ។ រកប្រូបាបដែលផលិតផលចៃដន្យមួយខូចគុណភាព ។',
        r'$0.032$',
        [r'$0.035$', r'$0.070$', r'$0.020$'],
        '$P(\\text{ខូច}) = 0.60(0.02) + 0.40(0.05) = 0.012 + 0.020 = 0.032$។',
        bloom='Evaluate',
    ))

    # 35 (Analyze) - PISA: System of 2 independent backup servers, each fails with prob 0.1. Prob at least one works = 1 - 0.01 = 0.99
    qs.append(mcq(
        'pisa', S3,
        'ប្រព័ន្ធកុំព្យូទ័រមួយប្រើម៉ាស៊ីនមេ 2 ដំណើរការឯករាជ្យពីគ្នា ដែលម៉ាស៊ីននីមួយៗមានប្រូបាបខូច $0.1$ ។ គណនាប្រូបាបដែលយ៉ាងហោចណាស់មានម៉ាស៊ីនមេមួយដំណើរការល្អ ។',
        r'$0.99$',
        [r'$0.90$', r'$0.81$', r'$0.98$'],
        '$P(\\text{ទាំងពីរខូច}) = 0.1 \\times 0.1 = 0.01$ ដូច្នេះ $P(\\text{យ៉ាងតិច 1 ល្អ}) = 1 - 0.01 = 0.99$។',
        bloom='Analyze',
    ))

    # 36 (Create) - PISA: Urn with 4 red, n blue. Draw 2 without replacement, P(both red) = 2/15 -> (4/(4+n))*(3/(3+n)) = 2/15 -> (4+n)(3+n)=90 -> n=6
    qs.append(mcq(
        'pisa', S2,
        'ថង់មួយមានប៊ូលក្រហម 4 និងប៊ូលខៀវ $n$ ។ គេចាប់ 2 ប៊ូលមិនដាក់វិញ ។ បើប្រូបាបបានក្រហមទាំងពីរស្មើ $\\frac{2}{15}$ តើមានប៊ូលខៀវប៉ុន្មានគ្រាប់?',
        r'$6$',
        [r'$5$', r'$8$', r'$4$'],
        '$\\frac{4}{4+n} \\cdot \\frac{3}{3+n} = \\frac{2}{15} \\implies (4+n)(3+n) = 90 = 10 \\times 9 \\implies n = 6$។',
        bloom='Create',
    ))

    # =========================================================================
    # WRITING (14): 1 easy, 4 medium, 4 hard, 5 pisa
    # =========================================================================
    # 37 (Easy - Apply)
    qs.append(writing(
        'easy', S1,
        'គេមាន $P(A) = 0.6$, $P(B) = 0.5$ និង $P(A \\cap B) = 0.2$ ។ គណនា $P(A \\mid B)$ និង $P(B \\mid A)$ ។',
        r'$P(A \mid B) = 0.4,\; P(B \mid A) = \frac{1}{3}$',
        '$P(A \\mid B) = \\frac{0.2}{0.5} = 0.4$ និង $P(B \\mid A) = \\frac{0.2}{0.6} = \\frac{1}{3}$។',
        bloom='Apply',
    ))

    # 38 (Medium - Apply)
    qs.append(writing(
        'medium', S1,
        'និស្សិត 840 នាក់៖ ប្រុស 540 នាក់ (ឌីហ្សាញ 80, IT 460) និងស្រី 300 នាក់ (ឌីហ្សាញ 160, IT 140) ។ ជ្រើសម្នាក់ដោយចៃដន្យ ។ គណនាប្រូបាបដែលគាត់ជា៖ ក. និស្សិតប្រុស ឬ ស្រីរៀនឌីហ្សាញ ខ. និស្សិតប្រុស និងរៀនឌីហ្សាញ ។',
        r'ក. $\frac{5}{6}$, ខ. $\frac{2}{21}$',
        'ក. $P = \\frac{540 + 160}{840} = \\frac{700}{840} = \\frac{5}{6}$ ។ ខ. $P = \\frac{80}{840} = \\frac{2}{21}$។',
        bloom='Apply',
    ))

    # 39 (Medium - Apply)
    qs.append(writing(
        'medium', S2,
        'ប្រអប់មួយមានប៊ូលក្រហម 6 និងប៊ូលស 4 ។ គេចាប់ 2 ប៊ូលម្តងមួយៗដោយមិនដាក់វិញ ។ គណនាប្រូបាបដែលបានប៊ូលក្រហម 1 និងប៊ូលស 1 ។',
        r'$\frac{8}{15}$',
        '$P = \\frac{6}{10}\\cdot\\frac{4}{9} + \\frac{4}{10}\\cdot\\frac{6}{9} = \\frac{48}{90} = \\frac{8}{15}$។',
        bloom='Apply',
    ))

    # 40 (Medium - Apply)
    qs.append(writing(
        'medium', S3,
        'គេបោះគ្រាប់ឡុកឡាក់ត្រឹមត្រូវ 3 គ្រាប់ព្រមគ្នា ។ គណនាប្រូបាបដែលយ៉ាងហោចណាស់មានគ្រាប់មួយចេញលេខ $6$ ។',
        r'$\frac{91}{216}$',
        '$P(\\text{គ្មានលេខ }6) = \\left(\\frac{5}{6}\\right)^3 = \\frac{125}{216} \\implies P(\\text{យ៉ាងតិច 1}) = 1 - \\frac{125}{216} = \\frac{91}{216}$។',
        bloom='Apply',
    ))

    # 41 (Medium - Analyze)
    qs.append(writing(
        'medium', S1,
        'គេបោះកាក់ត្រឹមត្រូវ 3 ដង ។ រកប្រូបាបដែលចេញក្បាល ($H$) ទាំង 3 ដង ដោយដឹងថាយ៉ាងហោចណាស់មាន 2 ដងចេញក្បាល ។',
        r'$\frac{1}{4}$',
        'ករណី $H \\ge 2$ មាន $4$ ករណី៖ $HHH, HHT, HTH, THH$ ។ ករណី $HHH$ មាន $1$ ករណី ដូច្នេះ $P = \\frac{1}{4}$។',
        bloom='Analyze',
    ))

    # 42 (Hard - Analyze)
    # 2 boxes: Box1 (3R, 2B), Box2 (2R, 4B). Choose box equally likely, draw 1 ball. P(R) = 0.5*(3/5) + 0.5*(2/6) = 3/10 + 1/6 = 14/30 = 7/15
    qs.append(writing(
        'hard', S2,
        'ប្រអប់ទី 1 មានប៊ូលក្រហម 3, ខៀវ 2 ។ ប្រអប់ទី 2 មានប៊ូលក្រហម 2, ខៀវ 4 ។ គេជ្រើសប្រអប់មួយដោយចៃដន្យ រួចចាប់ប៊ូល 1 គ្រាប់ ។ គណនាប្រូបាបដែលបានប៊ូលក្រហម ។',
        r'$\frac{7}{15}$',
        '$P(R) = \\frac{1}{2}\\cdot\\frac{3}{5} + \\frac{1}{2}\\cdot\\frac{2}{6} = \\frac{3}{10} + \\frac{1}{6} = \\frac{14}{30} = \\frac{7}{15}$។',
        bloom='Analyze',
    ))

    # 43 (Hard - Analyze)
    # 5 Red, 1 Black, draw 3 without replacement. Show A and B are dependent and compute P(C | A and B).
    qs.append(writing(
        'hard', S3,
        'ថង់មួយមានប៊ូលក្រហម 5 និងខ្មៅ 1 ។ ចាប់ 3 ដងមិនដាក់វិញ ។ តាង $A$: ទី 1 ក្រហម, $B$: ទី 2 ក្រហម, $C$: ទី 3 ខ្មៅ ។ គណនា $P(C \\mid A \\cap B)$ និងបង្ហាញថា $A, B$ អាស្រ័យគ្នា ។',
        r'$P(C \mid A \cap B) = \frac{1}{4}$, $A$ និង $B$ អាស្រ័យគ្នា',
        'ក្រោយចាប់ក្រហម 2 គ្រាប់ នៅសល់ក្រហម 3 ខ្មៅ 1 ដូច្នេះ $P(C \\mid A \\cap B) = \\frac{1}{4}$ ។ $P(A \\cap B) = \\frac{2}{3} \\neq \\frac{5}{6}\\cdot\\frac{5}{6} = \\frac{25}{36}$ ដូច្នេះ $A, B$ អាស្រ័យគ្នា។',
        bloom='Analyze',
    ))

    # 44 (Hard - Evaluate)
    # Two shooters A and B hit target independently with prob 0.7 and 0.8. Find P(exactly one hits) and P(A hit | target hit).
    # P(hit) = 1 - 0.3*0.2 = 0.94. P(exactly one) = 0.7*0.2 + 0.3*0.8 = 0.38. P(A | hit) = 0.7/0.94 = 35/47
    qs.append(writing(
        'hard', S3,
        'អ្នកបាញ់ធ្នូ $A$ និង $B$ បាញ់ដោយឯករាជ្យ ដោយមានប្រូបាបត្រូវគោលដៅ $0.7$ និង $0.8$ រៀងគ្នា ។ គណនាប្រូបាបដែល៖ ក. ត្រូវគោលដៅតែម្នាក់គត់ ខ. គោលដៅត្រូវគ្រាប់ (យ៉ាងហោចណាស់ម្នាក់ត្រូវ) ។',
        r'ក. $0.38$, ខ. $0.94$',
        'ក. $0.7(0.2) + 0.3(0.8) = 0.38$ ។ ខ. $1 - (0.3)(0.2) = 1 - 0.06 = 0.94$។',
        bloom='Evaluate',
    ))

    # 45 (Hard - Create)
    # 12 items (4 defective), draw 2 without replacement. P(at least 1 defective) = 1 - 14/33 = 19/33
    qs.append(writing(
        'hard', S2,
        'ទំនិញ 12 មុខមាន 4 មុខខូច ។ គេជ្រើស 2 មុខដោយមិនដាក់វិញ ។ គណនាប្រូបាបដែលយ៉ាងហោចណាស់មានទំនិញ 1 មុខខូច ។',
        r'$\frac{19}{33}$',
        '$P(\\text{ល្អទាំង 2}) = \\frac{8}{12}\\cdot\\frac{7}{11} = \\frac{14}{33} \\implies P(\\text{យ៉ាងតិច 1 ខូច}) = 1 - \\frac{14}{33} = \\frac{19}{33}$។',
        bloom='Create',
    ))

    # 46 (PISA - Apply)
    # School survey: 45% girls (30% wear glasses), 55% boys (60% wear glasses). Find P(wears glasses).
    # 0.45*0.30 + 0.55*0.60 = 0.135 + 0.330 = 0.465
    qs.append(writing(
        'pisa', S2,
        'ក្នុងសាលាមួយមានសិស្សស្រី 45% (ក្នុងនោះ 30% ពាក់វ៉ែនតា) និងសិស្សប្រុស 55% (ក្នុងនោះ 60% ពាក់វ៉ែនតា) ។ រកប្រូបាបដែលសិស្សចៃដន្យម្នាក់ពាក់វ៉ែនតា ។',
        r'$0.465$',
        '$P(\\text{វ៉ែនតា}) = 0.45(0.30) + 0.55(0.60) = 0.135 + 0.330 = 0.465$។',
        bloom='Apply',
    ))

    # 47 (PISA - Analyze)
    # Quality control: Lot of 20 phones has 3 defective. Inspector tests 2 without replacement; lot accepted if both pass.
    # P(accepted) = (17/20)*(16/19) = 68/95
    qs.append(writing(
        'pisa', S2,
        'ប្រអប់ទូរស័ព្ទ 20 គ្រឿងមាន 3 គ្រឿងខូច ។ អ្នកត្រួតពិនិត្យតេស្ត 2 គ្រឿងដោយមិនដាក់វិញ ហើយអនុញ្ញាតលក់បើទាំង 2 គ្រឿងល្អ ។ គណនាប្រូបាបដែលប្រអប់នេះត្រូវបានអនុញ្ញាតលក់ ។',
        r'$\frac{68}{95}$',
        '$P = \\frac{17}{20} \\times \\frac{16}{19} = \\frac{68}{95}$។',
        bloom='Analyze',
    ))

    # 48 (PISA - Evaluate)
    # Email spam filter: 40% of emails are spam. 85% of spam contains "FREE", 5% of non-spam contains "FREE".
    # P("FREE") = 0.40*0.85 + 0.60*0.05 = 0.34 + 0.03 = 0.37
    qs.append(writing(
        'pisa', S2,
        '40% នៃអ៊ីមែលជាសារឥតបានការ (Spam) ។ ក្នុងចំណោម Spam មាន 85% ផ្ទុកពាក្យ «FREE» និងក្នុងចំណោមអ៊ីមែលធម្មតាមាន 5% ផ្ទុកពាក្យ «FREE» ។ គណនាប្រូបាបដែលអ៊ីមែលចៃដន្យមួយផ្ទុកពាក្យ «FREE» ។',
        r'$0.37$',
        '$P(\\text{FREE}) = 0.40(0.85) + 0.60(0.05) = 0.34 + 0.03 = 0.37$។',
        bloom='Evaluate',
    ))

    # 49 (PISA - Analyze)
    # 3 traffic lights independent, each green with prob 0.7. Find P(all green) and P(stop at least once).
    qs.append(writing(
        'pisa', S3,
        'អ្នកបើកបរម្នាក់ឆ្លងភ្លើងស្តុប 3 កន្លែងឯករាជ្យពីគ្នា ដែលភ្លើងនីមួយៗមានប្រូបាបពណ៌បៃតងស្មើ $0.7$ ។ គណនាប្រូបាបដែលគាត់ត្រូវឈប់យ៉ាងហោចណាស់ ១ ដង ។',
        r'$0.657$',
        '$P(\\text{បៃតងទាំង 3}) = 0.7^3 = 0.343 \\implies P(\\text{ឈប់យ៉ាងតិច 1}) = 1 - 0.343 = 0.657$។',
        bloom='Analyze',
    ))

    # 50 (PISA - Create)
    # Disease 2%, test sensitivity 95%, false positive 4%. Find P(Test+) and check if P(Disease | Test+) > 0.5?
    # P(Test+) = 0.02*0.95 + 0.98*0.04 = 0.019 + 0.0392 = 0.0582. P(D|+) = 0.019/0.0582 ~ 0.326 < 0.5
    qs.append(writing(
        'pisa', S2,
        '2% នៃប្រជាជនមានជំងឺ ។ តេស្តមានប្រូបាបវិជ្ជមាន 95% ចំពោះអ្នកឈឺ និង 4% ចំពោះអ្នកជា ។ គណនាប្រូបាបតេស្តវិជ្ជមាន $P(T^+)$ និងពន្យល់ថាតើអ្នកតេស្តវិជ្ជមានម្នាក់មានឱកាសឈឺលើសពី 50% ឬទេ?',
        r'$P(T^+) = 0.0582$, មិនលើសពី 50% ទេ',
        '$P(T^+) = 0.02(0.95) + 0.98(0.04) = 0.019 + 0.0392 = 0.0582$ ។ ដោយ $P(D \\cap T^+) = 0.019 < \\frac{0.0582}{2}$ នោះ $P(D \\mid T^+) \\approx 32.6\\% < 50\\%$។',
        bloom='Create',
    ))

    return qs


def _verify_math():
    assert Fraction(10, 30) == Fraction(1, 3)
    assert Fraction(55, 125) == Fraction(11, 25)
    assert Fraction(8, 16) * Fraction(7, 15) == Fraction(7, 30)
    assert Fraction(460, 540) == Fraction(23, 27)
    assert sum(1 for x in range(1, 7) for y in range(1, 7) if x * x < 4 * y) == 17
    assert abs(0.45 * 0.30 + 0.55 * 0.60 - 0.465) < 1e-12
    assert abs(0.02 * 0.95 + 0.98 * 0.04 - 0.0582) < 1e-12


cands = build_candidates


if __name__ == '__main__':
    _verify_math()
    qs = build_candidates()
    print(f'{LESSON}: built {len(qs)} candidates, verified')
