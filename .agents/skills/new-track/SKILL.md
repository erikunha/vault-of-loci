---
name: new-track
description: Create a new learning track in this vault (course, book, certification, interview, research, skill, language or other) from the recipe of its kind. Asks for the kind and the horizon. Use when the user starts learning something. Writes files, so only run when asked.
---

Tutor mode: the goal, the done criterion and the if-then plan are the learner's words. Ask for them and write what the learner says; do not invent them.

1. Ask only for what is missing: the track name; the kind (`course`, `book`, `certification`, `interview`, `research`, `skill`, `language`, `other`); the horizon (`finite` ends when the done criterion is met, `ongoing` has no end); the goal; a `done_criterion` that can be failed; the `deadline` (finite only); one `if_then` plan ("If X, then I do Y").
2. Read the recipe for that kind in `90_System/Specs/Track_kinds.md`.
3. Create the folder `10_Tracks/<NN>_<Track_Name>/` with underscores instead of spaces; `NN` is the next free number.
4. Create `<Track_Name>.md` from `90_System/Templates/Track.md` with `type: track`, `kind`, `horizon`, `goal`, `done_criterion`, `deadline`, `if_then`, `status: active` and `order`. Fill `## Setup` and `## Review cadence` from the recipe.
5. Create `sessions/` (sessions come from `90_System/Templates/Session.md`, named `session-NN-<slug>.md`) and `practice/`. For the kinds that keep a log, add the starter note to `practice/` with `type: practice`, `track: "[[<Track_Name>]]"`, `tags: [type/practice]` and a table with the columns the recipe names:
   - `certification`: blueprint map (domain, weight, confidence, last score) and error log.
   - `interview`: problem log (problem, pattern, result, time, retry date).
   - `language`: input log (date, what, minutes) and mined sentences.
   - `research`: synthesis matrix (themes as rows, sources as columns).
   - `skill`: attempt log (attempt, what was hard, result, redo date).
   - `course` and `book`: only a `.gitkeep` in `practice/`.
6. The track appears in `00_Home.md` through `Tracks.base`; nothing to add by hand.
7. Run the `run-checks` skill and report each check as passed, failed or not run.
8. Add one line to `90_System/Agent_Log/YYYY-MM.md`.
