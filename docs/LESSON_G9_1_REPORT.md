# Grade 9 Lesson 1 «ចំនួនអសនិទាន» (2026-10-22)

## What Cursor built (kept)
- The Grade 9 pipeline: `public/data/lessons_g9.json`, the grade-9 branch in `teach-app/src/Lessons.jsx`, `'9-1'` in `BRANDED_LESSONS`, `tools/lesson9_1/{build.py, vis9.py}`.
- 128 slides: warm-up, 10 parts (square roots, cube roots, 3.1-3.6 radicals, exercises, PISA), summary; 11 computed figures with asserts and animations (`animate_deck`).

## What was missing or wrong, and what I did (all checked in the browser)
- **Layout (audit of every slide and every step):** exercise solutions 1-3 overflowed with text as small as 9 px; the squares/cubes tables and the farmers' table were 12-13 px.
  Now: compact 3-5 column grids, bigger tables. Result: 139 slides on screen, no overflow, no text under 17 px, no KaTeX errors.
- **Dropped from the book, now added:** Example 15, Example 22 (variables), the practice for division (4 items), the practice for 3.5 (5 items), items b and d of the 3.6 practice
  (the solutions were labelled a and c, silently skipping b and d), the full working of Example 21 (A-F were shown as bare results), and question 3 of every PISA task (plus the farmers' table).
- **Pictures:** root spiral was cut off (now fitted to its size), the cube-root picture had a misplaced index, numbers overlapped lines. New: the names of the parts of a radical (index, radical sign, radicand, exponent: the book's own figure), and why like radicals add (bars of length √2 laid end to end; √3 bars do not match).
- Removed two preview files that were left in `public/` (`_g9l1.html`, `_sheet91.html`).

## Errors in the source book (not copied; the slides show the checked value)
The printed answers in `solutions/SOL_L01.tex` disagree with the numbers (checked numerically):
- 3.2 practice (b): `∛5 / ∛0.2 = ∛25 ≈ 2.924`, the book prints 5 (5 is the answer of `∛25 / ∛0.2`, as in Example 13).
- 3.6 practice (b): `(3√2 + 2√3) / (√12 − √18) = −5 − 2√6 ≈ −9.90`, the book prints `−√6 − 3 ≈ −5.45`.
- 3.6 practice (d): `∛3 / (∛4 + ∛2) = (2∛6 − 2∛3 + ∛12)/6 ≈ 0.5065`, the book prints `(∛12 − ∛6)/2 ≈ 0.236`.
Please check these three in the printed book before teaching them.

## Not done / not verified
- **Exercises:** only difficulty level 1 (exercises 1-3) is in the deck. The book has levels 2 and 3 (about 40 more exercises: simplifying with letters, expanding products, rationalising, Pythagoras, the nested radical...). Not added.
- **Depth:** the book's «គិតមុនគូ» explanations and «ងាយយល់» boxes are shortened to the key steps in most examples; the full prose of every example is not reproduced.
- **Pictures:** 13 pictures for 138 slides. Parts 3.2 (division) and 3.4 (putting a number into the radical) have no picture; the book's tikz figures other than the radical anatomy were not redrawn.
- Looked at on screen: the square-root spiral, cube, compass construction of √2, √4·√9 area model, √18 squares, rationalising, radical anatomy, like radicals. Not looked at: the number-sets, garden square, √3 and ∛17 squeeze figures (they passed the overflow audit only).
- Not checked on a projector or phone. Khmer wording is the book's; I added none except slide titles like «ឈ្មោះផ្នែកនៃរ៉ាឌីកាល់» and «ប្រវែងដូចគ្នា ទើបបូកបាន».
- Maths: I read all 128 of Cursor's slides and checked every result I could by hand or by computation; the additions are asserted numerically in `build.py`. I did not independently prove the irrationality statements (they follow the book).

## Update 2026-10-22 (teaching-method additions)
- Every number and letter inside the pictures is now italic Times maths (mixed Khmer + maths labels use upright Khmer and italic maths).
- Added by me (not in the book): a map of the lesson (6 steps), a «ទាយសិន» predict slide, two «ពិត ឬ មិនពិត» checks (end of part 1 and before the exercises), a proof that √2 is irrational (extension),
  and an exit ticket. All their answers are asserted in `build.py`. Khmer wording for these slides is mine: please review.
- `docs/TEACHING_GUIDE_G9_L1.md`: the method, a 6-period plan, questions, misconceptions, differentiation, assessment.
- Audit again: 145 slides on screen, no overflow, no text under 17 px, no KaTeX errors. Looked at on screen: the map, the true/false check (3 answers revealed) and the proof slide.

## Update 2026-10-22 (ដើមការេ / ដើមគូប plants)
- Two new slides after the «រ៉ាឌីកាល់» intro of part 1 and before the cube table in part 2: a flower whose petals carry numbers and whose roots underground carry their roots (idea from the user's sketch; the drawing is my own).
  ដើមការេ: 9 → 3, 5 → √5, −4 → none (dashed root). ដើមគូប: 8 → 2, 17 → ∛17, −27 → −3. Roots appear one at a time. Values asserted in `plant()`.
- The Khmer sentences on these two slides are mine: please review. Audit: 147 slides on screen, no overflow, no text under 17 px, no maths errors. Not viewed: the root-by-root reveal steps one by one, projector/phone.

## Update 2026-10-22 (projector text size)
- Grade 9 Lesson 1 now uses a larger base text (`.ts-slide.ts-big`, ~40 px at 1920 px wide, was 28 px max). Only 9-1 (`BIG_TEXT_LESSONS` in teachshow.js): the Grade 7 decks were not re-audited at this size and keep the old size.
- Audit at 1920x873: 148 slides, no overflow, no text under 22 px. Not tested on a real projector.

## Update 2026-10-22 (rebuilt to follow the MoEYS textbook)
- Why: the first deck followed the long `L01_irrational_numbers.tex` (30 exercises, solutions, PISA) and had 147 slides: too many to teach. The textbook lesson 1 is 12 pages.
- Now: `tools/lesson9_1/build.py` follows the book (sections 1, 2, 3.1–3.6: every example, general rule, «លំហាត់គំរូ» and «ប្រតិបត្តិ», book wording): 73 slides on screen. Practice answers come with the → key (one by one). The old build is `build_full.py` (output `lesson1_full.js`, not loaded).
- Pictures: `tools/lesson9_1/vis_book.py`, all labels typeset with KaTeX in a `foreignObject` (radical bars, fractions, italic maths), nothing draws itself: pieces fade in with the reveal steps (`.ts-big` rules at the end of teachshow.css). Lessons part list (`lessons_g9.json`) has the 8 book sections.
- Differences from the book: the book prints 5/3 ≈ 1.66 and 2.77 and 15.6, 17.5 (truncated); the deck shows 5/3 ≈ 1.67, 25/9 ≈ 2.78, 2.5³ = 15.625, 2.6³ = 17.576 (rounded or exact). In 3.4 «ប្រតិបត្តិ» the book's first item (∛(1/3), no coefficient to insert) is omitted. The book's printed answer for 3.6 «ប្រតិបត្តិ» item 2 and 4 was not used; the values were checked numerically (−5−2√6 and (2∛6−2∛3+∛12)/6).
- Audit at 1920×873: 73 slides, no overflow, no text under 22 px, no KaTeX errors. Looked at on screen: map, garden, √3 line, radical parts, both plants, 3.1 picture, 3.3 picture, like radicals picture, a practice slide, a worked slide. Not looked at: every other slide, projector/phone.

## Update 2026-10-22 (exercise part)
- Part 9 «លំហាត់» added at the end (before the summary): level-one exercises of the lesson file `L01_irrational_numbers.tex` (ex. 1 roots of whole numbers, ex. 2 roots of fractions, ex. 3 simplify radicals). Problems on screen; one → shows all answers. Answers computed in build.py. The book itself has no end-of-lesson exercises; the level 2 and 3 exercises (about 27) and the PISA tasks are in the archived `lesson1_full.js` / the tex file, not in this deck.
- Audit at 1920 px: 76 slides, no overflow, no text under 22 px.
