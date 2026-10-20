# Work log — 19 October 2026

Live site: https://exam.khmermath.org  
Teacher: https://exam.khmermath.org/teacher  
Worker: Cloudflare `exam-khmer` + D1 `exam-khmer`. Deploy with `npx wrangler@4.151.1 deploy`.

Git: one commit today (`3ebe728` Add NGS orientation banks and games for grades 7–12). Teaching-mode work is **deployed live** but **not committed** yet.

---

## 1. NGS orientation banks and games (committed)

Chapter **តម្រង់ទិសសិស្ស NGS ២០២៦-២០២៧** is its own bank panel (not mixed into class 12). Questions were built from the two direction files (orientation + internal rules), MCQ only, no Khmer colon `៖`. Banks and classroom games use the same items.

- Labels for **class 7–12**.
- Grew each bank toward 100 questions, then synced again after many deletions in តម្រង់ទិស.
- Last live counts: **តម្រង់ទិស ~33**, **បទបញ្ជាផ្ទៃក្នុង 100**.
- Games updated from remaining bank items (`teamgame_g7.json` and copies for other grades).

### Bank tools

- **Delete question bank** for owner and admin (`POST /api/bank/delete`; staff can also delete a bank row).
- NGS **lesson sidebar stays sticky** while scrolling the bank.
- Smaller **sticky action bar**.
- **Create test** shows total questions and total scores in the modal and in the test title.

---

## 2. Teaching mode (deployed, not committed)

Default teacher dashboard is unchanged. Top-right **បង្រៀន** switch (night-mode style) turns on a teaching overlay (`body.teach-mode`, remembered in `exam_teach_mode`).

- Switch uses **vanishIn / vanishOut**.
- Dark classroom stage, hero, glass class cards.
- Class grid + tools below: name wheel, card/wheel/boat games, live quiz, bingo.
- **← ថ្នាក់** goes back from an in-dashboard tool.

How to open the new work: turn **បង្រៀន** on, then click a class card.

### Name wheel (កង់ចាប់ឈ្មោះ)

- Default: spin **individual students**.
- Under the class dropdown: **Spin** and **Group** tabs.
- Group count default **6**. Left wheel stays students (group-label swap was rolled back).
- Smaller wheel; fullscreen has an **✕**.
- Optional song mode (ticks stay the default when song is off):
  - `/audio/kamlang-chet.mp3` — កម្លាំងចិត្តក្នុងការប្រឡង
  - `/audio/kamlang-siksa.mp3` — កម្លាំងចិត្តសិក្សា

### Attendance

Click a class in teaching mode → attendance list for that session.

- Marks: **OK** (present, default), **A** (absent), **L** (late), plus notes.
- List does **not** reload on each mark. Save with **ចុះវត្តមាន**.
- API: `GET/POST /api/attendance`. New D1 table `attendance` (schema `2026-10-19-att`).

### Slideshow (Grade 7 Lesson 1)

PowerPoint-style slides for integers, with pen / highlighter / eraser.

On the slideshow:

- Name spin about **¼** of the slide, movable (not fullscreen).
- Timer (time and size).
- Math calculator.
- All of those popups are movable / resizable.

Files: `public/js/teachroom.js`, `public/js/teachshow.js`, `public/js/slides/g7l01.js`, `public/css/teachshow.css`, `src/api/attendance.js`.

---

## 3. Cache / “refresh still looks the same”

The home teacher screen is meant to look the same. Attendance and slides only appear after **បង្រៀន** → click a class.

Also fixed stale HTML:

- `/teacher` and `/teacher.html` run through the Worker first (`run_worker_first` in `wrangler.toml`).
- Response header `Cache-Control: no-store`.
- Asset query `?v=20261019t` on teacher JS/CSS.

Latest Worker version after that fix: `c32e8d63-5288-42d7-a822-78f84c2e1bdb`.

---

## 4. Still uncommitted in the working tree

Teaching mode, attendance, wheel songs, teachshow, plus other WIP not part of today’s teaching request (G11 L02/L03 generators, signup tests, schema/package.json extras). Do not commit unless asked.

---

## 20 October 2026 — Teaching mode rebuilt in React

- New app in `teach-app/` (Vite + React), built into `public/teach/` → https://exam.khmermath.org/teach/. Rebuild with `npm run build:teach`, then deploy.
- The **បង្រៀន** switch on the dashboard now opens `/teach/`. `/teacher?classic=1` keeps the old dashboard (the wheel/live tiles link there with `&tool=`).
- Home: class cards on top, game mode below. Click a class → វត្តមាន (pop-up), ស្លាយមេរៀន (all 22 G7 lessons → parts), កង់ចាប់ឈ្មោះ (full screen).
- Lesson parts come from `public/data/lessons_g7.json` (section titles of Lesson/G7/lessonN.tex). Only lesson 1 has a real deck; other lessons get one drawable board slide per part.
- Fixed: slide math lost its backslashes (template literals → `String.raw`); slideshow widgets no longer all open at start.
- Fixed: login/forgot-password could be shadowed by another account's free-text contact.

- Slides for G7 lessons 2–22 generated from `Lesson/G7/lessonN.tex`: `python3 tools/make_g7_slides.py` → `public/js/slides/g7/lessonN.js` (loaded on demand) + `public/data/lessons_g7.json`. Lesson 1 stays hand-made. Re-run after editing a lesson .tex. All 1,719 slides checked in-browser for KaTeX errors / stray LaTeX (0). Geometry lessons have no figures (the .tex has none) — draw with the pen.
