"""Part (section) titles for each Grade 11 SC lesson, and how a question's `sec` tag maps to a part.

The question bank stores the part in test_questions.topic (Lessons 1-2 already did this by hand); this module is
the single source of truth for the other lessons.  Part titles are the lesson's own section headings from the
textbook / site lesson.  build11sc.py calls topic_for() so every newly built lesson gets its parts automatically.

A lesson that is not listed here keeps topic = lesson name (the old behaviour).
"""

# lesson file number -> (lesson name in D1, [part titles in textbook order])
PARTS = {
    3: ('ស្វ៊ីតធរណីមាត្រ', [
        'និយមន័យស្វ៊ីតធរណីមាត្រ',
        'តួទី n នៃស្វ៊ីតធរណីមាត្រ',
        'ផលគុណតួស្មើចម្ងាយពីតួចុង',
        'ផលបូក n តួដំបូងនៃស្វ៊ីតធរណីមាត្រ',
        'ស្វ៊ីតធរណីមាត្រអនន្តតួ']),
    4: ('ផលបូកតួនៃស្វ៊ីតផ្សេងៗ', [
        'របៀបគណនាផលបូក',
        'គណនាផលបូកតាមលំនាំគំរូ',
        'និមិត្តសញ្ញា Σ សម្រាប់ផលបូកនៃស្វ៊ីត',
        'កំណត់តួទី n តាមផលសងតួនៃស្វ៊ីត']),
    5: ('ទំនាក់ទំនងតួនៃស្វ៊ីត', [
        'កំណត់តួទី n ដោយប្រើស្វ៊ីតជំនួយ',
        'ទំនាក់ទំនងរវាងតួ និងផលបូកតួនៃស្វ៊ីត',
        'ទំនាក់ទំនងកំណើនលំដាប់ពីរ']),
    6: ('វិធានអនុមានរួមគណិតវិទ្យា', [
        'គោលការណ៍នៃវិធានអនុមានរួមគណិតវិទ្យា',
        'ទ្រឹស្តីបទទ្វេធា']),
    7: ('អនុគមន៍អិចស្ប៉ូណង់ស្យែល', [
        'អនុគមន៍អិចស្ប៉ូណង់ស្យែល',
        'សមីការនិងវិសមីការអិចស្ប៉ូណង់ស្យែល',
        'ការអនុវត្តអនុគមន៍អិចស្ប៉ូណង់ស្យែល']),
    8: ('អនុគមន៍លោការីត', [
        'ក្រាបនៃអនុគមន៍លោការីត',
        'ការរំកិល និងការឆ្លុះក្រាបលោការីត',
        'រូបមន្តប្តូរគោល',
        'សមីការនិងវិសមីការលោការីត',
        'លោការីតគោល 10 និងលោការីតនេពែ',
        'ការអនុវត្តលើអនុគមន៍លោការីត']),
    17: ('លីមីតនិងដេរីវេ', ['លីមីត', 'ដេរីវេ']),
    26: ('រូបធរណីមាត្រក្នុងលំហ', [
        'ការគូសរូបក្នុងលំហនៅលើប្លង់',
        'លក្ខណៈគ្រឹះនៃធរណីមាត្រក្នុងលំហ',
        'ទីតាំងរវាងបន្ទាត់និងប្លង់ក្នុងលំហ']),
    27: ('បន្ទាត់និងប្លង់ស្របក្នុងលំហ', ['បន្ទាត់ស្របគ្នា', 'បន្ទាត់ស្របនឹងប្លង់', 'ប្លង់ស្របគ្នា']),
    28: ('ភាពអរតូកូណាល់ក្នុងលំហ', [
        'រូបមន្តផ្ទៃក្រឡានិងមាឌនៃសូលីត',
        'បន្ទាត់អរតូកូណាល់',
        'បន្ទាត់កែងនឹងប្លង់',
        'ប្លង់មេដ្យាទ័រ',
        'ប្លង់កែង',
        'មុំដែលបង្កើតឡើងដោយប្លង់ពីរ',
        'ចំណោលកែង']),
}

# sec tag -> 1-based part number, for the lessons whose generator uses 'secN_*' tags.
SEC_PART = {
    3: lambda s: int(s[3]),                      # sec1_.. sec5_..  -> part 1..5 (same numbering as the textbook)
    4: {'sec1_formula': 1, 'sec1_telesc': 1, 'sec2_pattern': 2, 'sec3_sigma': 3, 'sec3_prop': 3, 'sec4_diff1': 4, 'sec4_diff2': 4},
    5: {'sec1_aux': 1, 'sec2_sn': 2, 'sec3_second': 3},
    6: {'sec1_induction': 1, 'sec2_binom': 2},
    7: lambda s: int(s[3]),                      # sec1_def/sec1_graph -> 1, sec2_eq/sec2_ineq -> 2, sec3_apply -> 3
    8: lambda s: int(s[3]),                      # sec1_* .. sec6_apply -> part 1..6
    17: lambda s: 1 if 'លីមីត' in s else 2,      # the free-text tags that mention លីមីត are limits, the rest are derivatives
}


def part_title(lesson_no, sec):
    """Return the part title for a question with this sec tag, or None if the lesson has no sec rule."""
    if lesson_no not in PARTS or lesson_no not in SEC_PART:
        return None
    rule = SEC_PART[lesson_no]
    k = rule(sec) if callable(rule) else rule[sec]
    return PARTS[lesson_no][1][k - 1]


def topic_for(module_name, sec, lesson):
    """Topic to store for a question: its part title if known, else the lesson name."""
    try:
        n = int(module_name.split('L')[-1])
    except ValueError:
        return lesson
    try:
        t = part_title(n, sec)
    except (KeyError, IndexError, ValueError):
        t = None
    return t or lesson
