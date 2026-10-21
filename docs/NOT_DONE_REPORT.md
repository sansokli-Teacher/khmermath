# Exam system: what is NOT done or NOT verified (2026-10-21)

## Cannot be done from here (needs you)
1. **Test on real phones.** Long-press no longer counts as an incident, a resized window (keyboard) no longer counts as split view, Khmer dates, and the 10/5/1-minute banner were checked in code and tests only. Have 3-4 students try a short practice exam on their own phones.
2. **Telegram alert.** The error alert and the backup messages need `telegram_token` and `telegram_chat_id` set in admin settings. If they are empty, alerts go nowhere. I could not check them without reading secrets.
3. **First real pre-exam backup.** The 10-minute cron fires (confirmed 10:40 UTC, outcome ok) but has never had an exam to back up. After your next scheduled exam, look in the audit log for `pre-exam <id>`.
4. **Birth dates.** The ID-only warning and the bulk date entry exist, but only you know the students' real birth dates. Until they are entered and the check is switched on, a student can still log in as another student.
5. **GitHub.** Code is on branch `exam-khmer` of sansokli-Teacher/khmermath (main untouched). A separate repo for it would be cleaner; I cannot create one without a GitHub login.

## Built but not clicked through in a browser
- Lock beep + message, bulk birth-date dialog, and the class results Excel were syntax-checked and deployed but I did not click through them on the live teacher page (needs a teacher login). Try each once.

## Deliberately not built
- **One-click "cancel question" from the analysis screen.** Cancelling changes every student's score, so it stays in the question editor with its checkbox, where it is deliberate.
- **Excel export of per-student timelines.** The timeline is shown on screen per student; no file export.
- **Automatic smoke test before deploy.** `npm run deploy` runs the 55 tests first, but the smoke test needs a local server (`wrangler dev`, then `npm run smoke`), so it is still manual. Note: `npm run deploy` did not reach `wrangler deploy` once today; deploy with `npx wrangler deploy` after `npm test` until that is looked at.

## Known leftovers
- Game-bank hints contain bare LaTeX (unused, so nothing shows wrong).
- Bank repair covered the 102 known damaged rows; any damage that predates the guard in other tables was not scanned.
