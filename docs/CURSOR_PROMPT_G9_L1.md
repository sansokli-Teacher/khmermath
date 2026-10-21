# Prompt for Cursor: Grade 9, Lesson 1 «ចំនួនអសនិទាន» teaching slides

Paste everything below the line into Cursor (agent mode), with the folder `~/Exam_Khmer` open.

---

You are building the classroom slideshow for **Grade 9, Lesson 1 «ចំនួនអសនិទាន» (irrational numbers and radicals)** for a Cambodian maths teacher. It must be as good as the Grade 7 decks already built in this repo (Lessons 2, 3 and 12). Do NOT deploy, do NOT `git push`, do NOT touch secrets or `wrangler.toml`, and do not change other lessons. Stop when done and write the report.

## 1. Read first (do not edit)
- `tools/lesson3/build.py`, `tools/lesson3/vis3.py`: a finished deck: how pictures, reveal steps and exercises are assembled.
- `tools/lesson12/{build.py, animate.py, vis12a.py, vis12b.py, preview.py}`: figures with checks, animations (`pen-*` classes), construction with a compass.
- `tools/lesson1/lib.py`: helpers (`svg, fig, T, circ, line, arrow, rvg, rvd, slide, key, ex, prac, sol, stepify`). `tools/lesson2/tidy_sol.py`: splits long solutions.
- `public/js/teachshow.js` (reveal steps `data-step`, `BRANDED_LESSONS`) and `public/css/teachshow.css` (animation classes).
- `docs/LESSON_G7_3_REPORT.md`, `docs/LESSON_G7_12_REPORT.md`: how the work was checked and what was not verified.

## 2. Source of the content
- Main text: `~/PISA_Math_2026-new/Lesson/G9/G9_Math_Modern/lessons/L01_irrational_numbers.tex` (3830 lines). Sections: ១ ឫសការេ និងចំនួនអសនិទាន; ២ ឫសគូប; ៣ ប្រមាណវិធីលើរ៉ាឌីកាល់ (៣.១ គុណ, ៣.២ ចែក, ៣.៣ បញ្ចេញមួយចំនួនពីរ៉ាឌីកាល់, ៣.៤ បញ្ចូលមួយចំនួនក្នុងរ៉ាឌីកាល់, ៣.៥ បូក/ដក, ៣.៦ បំបាត់រ៉ាឌីកាល់ពីភាគបែង); practice (`practicebox`, from line ~1716); PISA section (line ~3793).
- The textbook PDF `~/PISA_Math_2026-new/Lesson/G9/គណិតវិទ្យា_ថ្នាក់ទី៩3.pdf` may be used only to CHECK figures. Never copy or publish its pictures (MoEYS copyright).
- Keep the book's Khmer wording and numbers exactly. List every Khmer sentence you add yourself in the report. Latin digits inside formulas as in the source.

## 3. Grade 9 has no pipeline yet: add it (small, careful changes)
1. `public/data/lessons_g9.json`: `{"1": {"t": "ចំនួនអសនិទាន", "p": ["<part 1 title>", "...", "លំហាត់"]}}` (same shape as `lessons_g7.json`; last part = the exercises).
2. `teach-app/src/Lessons.jsx`: for grade `'9'` fetch `lessons_g9.json`, and when a lesson is opened load `/js/slides/g9/lesson${n}.js?v=<new version>`. Mirror the grade-7 logic (`hasDeck`, `loadScript`, the part-board fallback). Then `npm run build:teach`.
3. `public/js/teachshow.js`: add `'9-1'` to `BRANDED_LESSONS` (adds the school intro slide). Bump the `teachshow.js?v=` tag in `public/teacher.html` and `teach-app/src/Lessons.jsx`; bump `teachshow.css?v=` if you edit the CSS.
4. Builder: `tools/lesson9_1/{build.py, vis9.py}` writing `public/js/slides/g9/lesson1.js` as `window.TEACH_SLIDES['9-1'] = [...]`. There is no tex-to-slides generator for Grade 9: author the slides in Python with the `lib.py` helpers, taking the text from the tex.

## 4. Deck structure (copy the Grade 7 pattern)
- Cover with the objectives; each part opens with a title slide `<h1>N. title</h1>` (the part board finds parts by this) and a picture.
- Definitions/rules in `key` slides, worked examples in `ex` slides with reveal steps, practice (`prac`) then solutions (`sol`, stepified; use `tidy_sol.rebuild` for multi-part solutions).
- Last numbered part «លំហាត់» (the PISA section may be its own part). End with a summary slide and the closing slide (`<h1>ចប់មេរៀន</h1>`).
- Several short slides are better than one crowded slide. No slide may overflow.

## 5. Pictures (draw them; do not leave placeholders)
Exact SVG built from coordinates, every number computed in Python with `assert`s (use `math`/`fractions`; verify claims such as "irrational" with a proof argument or a known fact, never by decimals). Ideas: the right triangle with legs 1 and 1 and the compass arc that marks √2 on the number line (a construction that shows the compass at every step, like slide ៥១ of Lesson 12); a unit square of area 2; the sets of numbers (ℕ ⊂ ℤ ⊂ ℚ ⊂ ℝ) with the irrationals outside ℚ; square roots squeezed between integers; a cube and its cube root; area models for √a·√b and for simplifying radicals; rationalising the denominator step by step.
Style rules: numbers and letters in pictures use the italic Times helper `M()` (not plain text); Khmer text uses `T()`; teacher-friendly big text (at least 17 px on screen); constructions always show the tool.

## 6. Animation
Run the finished deck through `tools/lesson12/animate.py` (`animate_deck`), as Lesson 3 does. Add hand-made animation where it teaches (the compass arc swinging onto the number line, a side of a square being laid onto the line). Use only the `pen-*` CSS classes already in `teachshow.css` (add new ones there if needed, and keep the `.rv-hide [class*="pen-"] { animation: none }` rule working).

## 7. Checks you must run (and report)
- `python3 tools/lesson9_1/build.py`; a contact sheet of all figures (copy `tools/lesson12/preview.py`) and look at it.
- Local test: `npx wrangler dev --local --port 8799 --env-file <dev.vars>`; open the lesson in the teaching mode and step through EVERY slide and EVERY reveal step. Measure: no overflow (`scrollHeight > clientHeight`), no text under 17 px, no figure under 170 px high, no figure/text pair that was auto-split into two slides without a reason.
- `npm test` must still pass (55 tests).
- Compare each figure with the textbook PDF pages (private reference only).

## 8. Report
Write `docs/LESSON_G9_1_REPORT.md`: what you built (files, slide counts), how each part was checked, the Khmer text you added, and an honest list of what was NOT verified (projector/phone, slides you did not view, anything you were unsure about in the maths). Do not claim anything you did not test.
