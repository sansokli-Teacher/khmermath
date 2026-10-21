# Grade 7 Lesson 2 slide enhancement (2026-10-21)

## Audit (stepping through every slide in a local copy)
- 117 authored slides, grew to about 126 on screen because the engine auto-splits overflowing slides.
- The exercise part (part 7) was the problem: solutions carried 150-330 words at 9-15 px.
- Cause: in the book exercises, sub-questions (ក. ខ. គ. ឃ.) were nested inside one another in the HTML, so each solution slide
  was a single cramped block with a growing indent.
- The page counter «(១/២)» was white on a white slide, so it was invisible.

## Changed
- tools/lesson2/tidy_sol.py rebuilds the exercise solutions: balanced HTML, one group of sub-questions per slide, «(១/៣)» counters.
  Exercise 1 solutions are now 3 clean slides, exercise 7 is 3, and so on. Authored slides 117 -> 123.
- The counter is now readable on light slides (teachshow.css).
- Cache tags bumped so browsers load the new deck (lesson file and teach app).

## Checked on screen (desktop browser, local copy)
Ex 4 (part 1), Ex 5, Ex 7 (part 1), the prime sieve table, and the answer slide for 1.3 "ចែកដាច់នឹង 4" read well.

## Not done
- Not checked on a projector or phone; only a desktop browser.
- Not every one of the 126 slides was looked at: the audit measured them all, but I viewed only the worst and a few others.
- No new interactive quizzes or new pictures were added. The deck already has the Spin and Timer tools.
- A few answer slides (ចម្លើយ ក./ខ., sieve) still carry 110+ words; they render at 19-22 px and I judged them readable.
