# Pilot checklist — one low-stakes quiz on real phones

Do this once before any exam that counts. Use a 10–15 minute quiz, one class, a teacher walking the room.

## Before
- [ ] Readiness checklist (📋) is all green on the session.
- [ ] Integrity mode: start with **⚠ warn** (not 🔒 lock) so nobody is locked out while you learn how phones behave.
- [ ] Tell students: use Chrome or Safari (not the browser inside Telegram/Facebook), charge the phone, close other apps, turn off AI assistants / Circle-to-Search.
- [ ] 5 questions with a diagram, 1 with variants (🎲), 1 writing question, explanations written on at least 2.

## During — write down what you see
- [ ] How many students start within the first minute? Anyone stuck at the PIN?
- [ ] Does the **fullscreen** prompt appear on Android? iPhone (it won't — that is expected)? iPad?
- [ ] Pull the notification bar down on one phone: is it counted? (should be logged, not counted if < 2 s)
- [ ] One student switches app for 10 s: shield shown, warning on return, timeline entry for the teacher?
- [ ] One student turns on airplane mode for 1 minute, answers 2 questions, turns it back on: banner shown, answers uploaded?
- [ ] One student opens the quiz on a second phone: refused, and visible in the timeline?
- [ ] Watermark readable in a screenshot but not distracting?
- [ ] Does anything on the screen look wrong on the smallest phone in the room?

## After
- [ ] Mark the writing question with the ✎ grid. Time it.
- [ ] 👁 Preview, publish, check one student's report on their phone (explanations visible).
- [ ] 🖨 Class report prints on one page.
- [ ] Settings → ♻ restore **verify** (dry run) works, and ✅ backup check is green.

## Load test (before the pilot, from a laptop)
```sh
TEACHER_USER=owner TEACHER_PASS=... node test/load.mjs https://exam.khmermath.org 40
```
Creates a scratch class "LOAD-xx" with 40 students and a 20-question test, runs them all at once, prints latencies and any errors, then deletes everything it created. Run it at a quiet time.
