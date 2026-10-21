# Device testing report, 2026-10-21 (session 14)

## What the testing recorded (from exam_events, session 14, about 10:54-11:07 UTC)
- 10 `start` events (the page was opened/resumed 10 times), 3 `locked`
- 14 `tab_hidden` (8 counted as incidents), 5 `window_blur` (2 counted)
- 3 `fullscreen_exit` (1 counted), 1 `fullscreen_enter` — fullscreen was left and re-entered during the test
- 4 `devtools` (2 counted), 1 `second_tab` — desktop testing with the developer tools open and a second tab
- 2 offline / 2 online — connection dropped briefly, recovered
- Earlier exam (session 13, morning): 37 `window_blur`, only 3 counted; 8 `fullscreen_enter` — the 
  false-alarm fixes (long-press, window height) were deployed after that exam, so they have not been
  exercised by a real class yet.

## Read-out
- The locks in session 14 came from tab switching, devtools and exiting fullscreen. Those are real incidents
  for a desktop tester, not false alarms. The phone-specific false alarms cannot be judged from this data,
  because no event shows a phone `contextmenu` or `split_view` at all (nothing counted, as intended).
- Fullscreen exits are the most frequent real trigger on phones: a swipe from the edge leaves fullscreen.

## Changed (deployed)
- Phone full screen: viewport-fit=cover, safe-area padding for the notch and home bar, dynamic viewport height.
- ⛶ button in the exam toolbar (Android Chrome) to enter or leave fullscreen.
- iPhone Safari cannot go fullscreen from a web page: a one-time hint explains «បន្ថែមទៅអេក្រង់ដើម»;
  the installed app opens without browser bars (manifest display_override: fullscreen).

## Not verified
- None of the above was seen on a real phone. I only checked the page loads without errors and the button,
  meta tag and padding exist (desktop browser, local server).
- iPhone: fullscreen from the web is not possible; the home-screen route is the only option.
- Who tested and on which devices is not recorded, so per-device conclusions cannot be drawn.
