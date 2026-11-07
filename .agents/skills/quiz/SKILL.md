---
name: quiz
description: Write a quiz into 50_Review/Quizzes from the vault's own sources (concept, reference and session notes), with the answer key kept apart and revealed only after the learner answers and rates confidence. Use when the learner asks to be quizzed on a track or topic. Writes a file, so only run when asked.
disable-model-invocation: true
---

Tutor mode: the learner answers first and rates confidence from 1 to 5 before any answer is shown. The agent never writes the learner's answers.

1. Pick 5 to 10 concepts for the track or topic, weakest and least recently tested first (`calibration_report.py`, `Progress.base`). Mix categories.
2. Read each concept's study layer and the references it cites. Every question comes from a note in the vault and names it; never from memory.
3. Write `50_Review/Quizzes/<Topic>_YYYY-MM-DD.md` with `type: review`, a `## Questions` section and a `## Answer key` section inside a folded callout (`> [!answer]- Answer key`). Order: open recall questions first, then application, then at most a few multiple-choice questions whose wrong options are real misconceptions, not jokes. No hints inside the questions.
4. Each question has an empty `My answer:` line and `Confidence (1 to 5):`. Leave them for the learner.
5. Show nothing from the key until the learner has answered and rated confidence. Then grade against the source and a rubric: fluent but empty gets no credit, short and correct gets full credit, right answer for the wrong reason gets part.
6. For each miss, offer `mistake-review`. Ask the learner whether to log the score in the concept (`score`, `confidence`, `last_tested`); set it only with their yes.
