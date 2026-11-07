---
name: pretest
description: Write 3 to 5 prequestions into a lesson note's Pretest section before the lesson, for the learner to guess first. Use when the learner is about to study a topic. Writes the questions only, so only run when asked.
disable-model-invocation: true
---

Tutor mode: the learner attempts first; the agent never writes the learner's guesses, the study layer or the answers.

1. Open the lesson note (`10_Courses/<course>/lessons/`) or ask for the topic and its sources. Read the syllabus, readings or transcript titles, not the full lesson.
2. Write 3 to 5 questions into `## Pretest`, from the simplest idea to the hardest. They cover what the lesson will teach, so most will be unanswerable now. That is the point.
3. Leave `My guess` and `After the lesson` empty. Ask the learner to write a guess for each, with confidence from 1 to 5, before anything else. A wrong or blank guess is fine; looking it up is not.
4. Do not reveal answers. After the lesson, the learner marks each guess right or wrong. Only then, on request, use the hint ladder (hint, strong hint, partial example, answer) for questions still open.
5. Offer to turn missed questions into flashcards, written by the learner in their own words.

Run `run-checks` after writing.
