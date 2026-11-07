---
name: pretest
description: Write 3 to 5 prequestions into a session note's Pretest section before the session, for the learner to guess first. Use when the learner is about to study a topic. Writes the questions only, so only run when asked.
disable-model-invocation: true
---

Tutor mode: the learner attempts first; the agent never writes the learner's guesses, the study layer or the answers.

1. Open the session note (`10_Tracks/<track>/sessions/`) or ask for the topic and its sources. Read the syllabus, chapter titles, blueprint or transcript titles, not the full material.
2. Write 3 to 5 questions into `## Pretest`, from the simplest idea to the hardest. They cover what the session will teach, so most will be unanswerable now. That is the point.
3. Leave `My guess` and `After the session` empty. Ask the learner to write a guess for each, with confidence from 1 to 5, before anything else. A wrong or blank guess is fine; looking it up is not.
4. Do not reveal answers. After the session, the learner marks each guess right or wrong. Only then, on request, use the hint ladder (hint, strong hint, partial example, answer) for questions still open.
5. Offer to turn missed questions into flashcards, written by the learner in their own words.

Run `run-checks` after writing.
