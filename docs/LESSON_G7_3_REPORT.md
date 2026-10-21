# Grade 7 Lesson 3 «ចំនួនគត់រ៉ឺឡាទីប» + pen upgrade (2026-10-21)

## Pen («full write») — public/js/teachshow.js
- Pressure: a pen's line is thinner or thicker with pressure (mouse and touch keep a fixed width).
- Smooth: strokes are curves through the points, not straight segments; all coalesced pen samples are kept.
- Faster: finished strokes are painted once into a cache; only the stroke being drawn is repainted.
- Palm rejection: a touch within 2.5 s of the pen is ignored; another pointer cannot bend a stroke in progress.
- Eraser end and the pen's side button erase (any tool); eraser ring shows the size; `[` `]` change it (6-60 px).
- Not done: shape snapping (you did not choose it).

## Lesson 3 deck — tools/lesson3 (build.py, vis3.py, base_deck.json)
- Kept the book's text (frozen from lesson3.tex); added the 16 figures the .tex only describes in «% Diagram:» notes:
  thermometer, number line, |a| distances, order on the line, opposites, points A/B, marbles + number-line hops for
  3+4 and (−4)+(−1), zero pairs for 4+(−2), pulling marbles out for 4−2 and (−8)−(−2), 6−(−3) with zero pairs,
  plus the week profit/loss bars, sign grids (× and ÷), an order-of-operations ladder with a worked example.
- Rewrote the dense slides: addition rules, subtraction rule, exercise 2 (points and lengths), exercise solutions
  (clean split slides, same splitter as Lesson 2).
- 137 -> 160 authored slides (165 on screen incl. the school slide and auto-splits). Every number in the pictures is
  computed in Python with asserts; the book's own examples are used wherever they exist.
- «8. លំហាត់» is now a numbered part, so the part board opens it. Lesson 3 gets the school / teacher intro slide.
- Audit (every slide stepped): no overflow, no text under 17 px.

## Added by me, not in the book — please confirm you want them
- «តើហេតុអ្វី (−)×(−) = (+) ?» pattern slide (−3 × 3, 2, 1, 0, −1, −2).
- The worked order-of-operations example 6 + 4 × (8 − 5) ÷ 2 = 12 and the 3-step ladder.
- Wording I wrote: ទែម៉ូម៉ែត្រ, ទិសដៅវិជ្ជមាន, «ជាចំនួនផ្ទុយនៃ», «ចំនួនកាន់តែទៅខាងស្តាំ កាន់តែធំ», «យកចេញ». Check against MoEYS terms.

## Not verified / not done
- Wacom pressure, side button, eraser end and palm rejection are untested on real hardware (tested with synthetic pen events only).
- Not checked on a projector or phone; desktop browser only. I looked at about 20 of the 165 slides; the rest were measured, not viewed.
- Part 7 (profit/loss word problems) has no new pictures; its text slides are the book's.
- The multiplication pattern slide is my addition and uses Latin digits like the rest of the maths.
