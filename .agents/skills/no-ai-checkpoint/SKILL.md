---
name: no-ai-checkpoint
description: Run a closed-book quiz on concepts the learner last studied more than 14 days ago, then log the score per concept in last_tested and score. Use when the learner asks for a checkpoint or a no-AI test. Writes properties, so only run when asked.
disable-model-invocation: true
---

Tutor mode: the learner answers first; the agent never shows an answer, a note excerpt or a summary before the attempt, and never writes the learner's study layer or answers.

1. Pick concepts: notes in `20_Concepts` whose `last_tested` is empty or older than 14 days (the review-queue skill lists them; 14 days is a default, not a research number). Take at most 5, weakest `score` first.
2. For each concept, ask 3 questions from its flashcards and Key takeaways, at least one that applies the idea to a new situation. One question at a time. The learner works closed book: no notes, no AI help.
3. After each answer, before any feedback, ask for confidence from 1 (guess) to 5 (certain). Then reveal and grade against the note.
4. If an answer is wrong, use the hint ladder only when the learner asks to try again: hint, strong hint, partial example, answer. Never skip a step.
5. Score per concept is the percentage of questions right on the first attempt, 0 to 100. Show the learner the gap between confidence and score; that gap is what to study.
6. Write only these properties on the concept, after the learner agrees: `last_tested: YYYY-MM-DD`, `score: <0-100>`, `confidence: <average, 1-5>`. Use `obsidian property:set` when the app runs, else edit the frontmatter. Optionally save the session from `90_System/Templates/Checkpoint.md`; the learner fills the answer columns.
7. Offer to add each missed question to `50_Review/Mistakes.md` through the mistake-review skill.

Run `run-checks` after writing. Do not touch `## Study explanation`, `## Key takeaways` or the flashcards.
