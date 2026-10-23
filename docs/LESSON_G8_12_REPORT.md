# Grade 8 · Lesson 12 «ការប្រៀបធៀបត្រីកោណ» — teaching-mode deck

Built `python3 tools/lesson8_12/build.py` → `public/js/slides/g8/lesson12.js` (71 slides; 72 in the player with the branded first slide).
Pictures: `tools/lesson8_12/geo8.py` on top of the Grade 9 engine (`tools/lesson9_13/geo13.py`); formula-book colours (blue outlines, red dashed helpers, red ticks/arcs).
Preview: `tools/lesson8_12/preview.py` writes `public/_g8_sheet.html` (all steps showing, 1920×1080 proportions) — delete before deploying.

Wiring: `public/data/lessons_g8.json` (lesson list, only lesson 12 for now), `teach-app/src/Lessons.jsx` (grade 8 list + deck loader), `teachshow.js` (`8-12` in BRANDED_LESSONS and BIG_TEXT_LESSONS).

## Source and order
MoEYS Grade 8 textbook, lesson 12, pp. 141-157 (scan `Lesson/G8/មេរៀនទី១២ការប្រៀបធៀបត្រីកោណMath4You.pdf`, pages 154-157 read from the scan; pp. 141-153 from `lesson12.tex`).
Same teaching order as the author's class slides (ESC_មេរៀនទី១២-01 / -02): construction → superposition → theorem → សម្មតិកម្ម/សន្និដ្ឋាន/វិបាក → worked example → practice.

1. ត្រីកោណប៉ុនគ្នា: 1.1 definition · 1.2.1 ម.ជ.ម · 1.2.2 ជ.ម.ជ · 1.2.3 ជ.ជ.ជ · 1.3.1 អ.ម · 1.3.2 អ.ជ្រ · summary table
2. មេដ្យាទ័រនៃអង្កត់និងត្រីកោណសមបាត
3. វិសមភាពក្នុងត្រីកោណ (angles/sides; triangle inequality with the four sticks)
4. ការប្រៀបធៀបអង្កត់ (4.1, 4.2, 4.3)

## Added for teaching flow (not in the book)
Lesson map, recall slide, 1.2 overview cards, the summary table of five cases, the end summary. The ម.ជ.ម practice «∠ABC=∠AED, AB=AE» follows the author's class slide (the transcript read «BC=DE», which cannot give a solution).
Section 4.2 of the transcript was missing; the scan shows it is «ប្រៀបធៀបអង្កត់ទ្រេតនិងអង្កត់កែង» (hypotenuse longest).

## Not done
The 34 exercises of pp. 157-162 (only the figure descriptions were available, no statements); lessons other than 12 for Grade 8 still open as a board with one slide per part (or are not listed).
