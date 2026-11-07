---
name: mistake-review
description: Turn logged mistakes in 50_Review/Mistakes.md into corrected flashcards with a source link, after the learner attempts the correction. Use when the learner asks to review or convert mistakes. Writes only to Mistakes.md, so only run when asked.
disable-model-invocation: true
---

Tutor mode: the learner attempts the correction first; the agent never writes the learner's study layer (concept notes, takeaways, their own cards) or their answers.

1. Read `50_Review/Mistakes.md`. List open entries that have no corrected card yet. Each entry records AI use: `scaffold`, `substitute` or `none`; if it is missing, ask the learner and add it.
2. For each entry, show only the question and the learner's wrong answer. Ask the learner to write the correct answer and why they went wrong, with confidence from 1 to 5. Use the hint ladder only after that attempt: hint, strong hint, partial example, answer.
3. Check the learner's correction against the concept note and its cited source in `40_References`. If the vault has no source, say "not verified" and do not invent one.
4. Draft one card per entry under `## Corrected cards` in `Mistakes.md`: `question::answer [[Source_Note|source]]`. Phrase it as an application when possible (a new situation, not the definition). Mark the draft `(draft)` until the learner edits it in their own words.
5. Never repeat a question already in the vault: run `check_cards.py` and fix a duplicate by merging.
6. Close an entry (`closed YYYY-MM-DD`) only after the learner answers it right later, without help and from memory; a correct answer right after the hint ladder does not close it.
7. Do not edit concept notes. Suggest which concept to reread, closed-book first.

Run `run-checks` after writing.
