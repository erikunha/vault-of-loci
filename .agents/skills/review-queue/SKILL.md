---
name: review-queue
description: List what to review next (weakest concepts, concepts not tested in 14 days, unresolved links, orphan notes) with the Obsidian CLI, or from files when the app is not running. Use when the learner asks what to study today. Reads by default and sets properties only on request.
disable-model-invocation: true
---

Tutor mode: this skill lists; the learner decides and attempts. It never answers questions, writes the study layer or sets a score the learner did not report.

## With the Obsidian CLI

Needs the app running and Obsidian 1.12.7 or later. Check with `obsidian help`; if the command fails, use the file fallback.

```bash
obsidian base:query path="90_System/Bases/Weakest.base" format=json
obsidian base:query path="90_System/Bases/Interleave.base" format=json
obsidian unresolved
obsidian orphans
```

Set a property only when the learner reports the value:

```bash
obsidian property:set name="last_tested" value="2026-11-07" file="Retrieval_Practice"
```

Parameter names can change between releases: `obsidian help base:query` is the reference.

## From files

Read the frontmatter of each note in `20_Concepts` (never `.env` or plugin `data.json`). Sort by `score` ascending, then `last_tested` ascending; empty values come first. Find unresolved links with `check_links.py`.

## Output

At most 5 concepts, each with `score`, `last_tested` and `confidence`. Mix categories: take the weakest first, then alternate categories (interleaving). End with one suggestion: `no-ai-checkpoint` for the list, or `mistake-review` when `50_Review/Mistakes.md` has open entries.
