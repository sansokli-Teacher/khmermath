# Grade 9 Lesson 13 «រង្វង់និងបន្ទាត់» (circle and line): slide deck
Source: the MoEYS textbook lesson 13 (pp. 143-158). Builder: `tools/lesson9_13/build.py` (+ `geo13.py` for the figures) -> `public/js/slides/g9/lesson13.js`, key `9-13`. Lesson 13 is registered in `public/data/lessons_g9.json`, `BRANDED_LESSONS` and `BIG_TEXT_LESSONS` (projector size) in `public/js/teachshow.js`.
## What is in the deck (book order, book wording)
1. Chord properties: perpendicular from the centre bisects the chord (rule + converse; examples 1-3, practice); equal chords are equidistant from the centre (rule + converse; examples 1-3, practice).
2. Tangent: the line that moves down until it touches (one position per press), tangent ⟂ radius, example, practice.
3. Properties of the tangent: tangent parallel to a chord, two tangents from one point (AB = AC, bisected angles), examples 1-2, practice.
4. Quadrilateral around a circle: AB + CD = AD + BC, example, practice.
5. Two circles: the five positions (the small circle moves in, one position per press), summary table, example (2x + 1), practice.
6. Common tangents: the four cases (4, 3, 2, 1, 0 tangents), summary table, examples 1-2, practice.
Added by me for the teaching flow (not in the book): lesson map, wheel-on-the-road opener, recall of the parts of a circle, the two summary tables, one extra picture per example.
## Checks
- Every figure is computed from coordinates; the properties it shows are asserted in `geo13.py` (tangent ⟂ radius, equal chords equidistant, tangent lengths equal, AB + CD = AD + BC ...). Every number in an example is checked in `build.py`.
- Audit at 1920×1080 (headless Chrome, `tools` not committed): no overflow, no text under 22 px, no maths errors. Every slide was looked at on screen (contact sheets).
## Differences from the book
- Practice of 5 (book p.153): the book gives r = 5, r' = 3 and "OO' cuts the circles at A, B" but no value for OO'. The deck states OO' = 12 cm (marked as added) and gets AB = 4 cm.
- Practice 1 of 6 (table): the book writes d = b − a for the last column (a = 5, b = 3, d = 2); the deck writes d = a − b.
- Rule 3 of two tangents: the book's sentence is garbled; the deck says "AO bisects the angle between the tangents and the angle between the radii".
