---
name: review-queue
description: List what is next to review from the note frontmatter and the Obsidian Bases (weakest concepts, concepts not tested in 14 days, unresolved links), within a daily review cap and with a catch-up mode for a backlog, optionally for one track. Use when the learner asks what to review next or which concept is weakest or overdue. Reads by default and sets properties only on request.
disable-model-invocation: true
---

Tutor mode: this skill lists; the learner decides and attempts. It never answers questions, writes the study layer or sets a score the learner did not report.

## With the Obsidian CLI

Needs the app running and Obsidian 1.12.7 or later. Check with `obsidian help`; if the command fails, use the file fallback.

```bash
obsidian base:query path="90_System/Bases/Weakest.base" format=json
obsidian base:query path="90_System/Bases/Interleave.base" format=json
obsidian base:query path="90_System/Bases/Progress.base" view="Review next" format=json
obsidian unresolved
```

`INDEX.md` links every note, so `obsidian orphans` lists nothing useful here. Set a property only when the learner reports the value:

```bash
obsidian property:set name="last_tested" value="2026-11-07" file="Retrieval_Practice"
```

Parameter names can change between releases: `obsidian help base:query` is the reference.

## From files

Read the frontmatter of each note in `20_Concepts` (never `.env` or plugin `data.json`). Sort by `score` ascending, then `last_tested` ascending; empty values come first. The "Review next" view of `Progress.base` ranks by (5 - confidence) x (days since last test + 1), so a weak concept not seen for a while comes first; an untested concept counts as 30 days. For one track, keep the concepts whose `tracks` property links to it. Find unresolved links with `check_links.py`.

## Calibration and staleness

`python3 -I 90_System/Scripts/calibration_report.py` lists concepts where the learner's confidence and score are 30 points or more apart, concepts not tested for 30 days and concepts never tested. Put the overconfident ones first: they feel known and are not.

## Daily cap and backlog

A day's flashcard work is 10 to 20 reviews and about 2 new cards (defaults from `90_System/Specs/Track_kinds.md`, not research results). Ask the learner how many cards are due.

- Due at or under the cap: normal review, new cards allowed.
- Due over the cap: catch-up mode. Review the oldest and weakest first, stop at the cap, add no new cards until the queue is under it. Missed days carry no penalty and no streak resets.

## Output

At most 5 concepts, each with `score`, `last_tested` and `confidence`. Mix categories: take the weakest first, then alternate categories (interleaving). Say whether today is normal or catch-up mode. End with one suggestion: `no-ai-checkpoint` for the list, or `mistake-review` when `50_Review/Mistakes.md` has open entries.
