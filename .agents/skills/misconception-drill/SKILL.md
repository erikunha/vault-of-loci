---
name: misconception-drill
description: Write two items that look alike for a confusion the learner keeps making, one where each idea applies, and log the pair in 50_Review/Misconceptions.md after the learner confirms it; use it when the learner keeps mixing two ideas, and it writes a file, so run it only when asked.
disable-model-invocation: true
---

Tutor mode: the learner attempts first and before the key is shown. The agent never writes the
learner's own answer, never writes the learner's notes and never picks the answer for them.
Hints come one step at a time and only after an attempt: hint, strong hint, partial example,
answer. Confidence from 1 to 5 is asked before the reveal. The agent never grades an attempt the
learner did not confirm.

1. Run the report and read the first confusion.

```bash
python3 -I 90_System/Scripts/misconception_report.py
```

2. Read the line for that confusion. It gives the objective, how many times it was wrong, how many
   of those needed help, the items involved and the open mistakes from `50_Review/Mistakes.md`
   that name it.
3. Read the concept notes of the two ideas and the sources they cite. The report says the
   exercise to build: two items that look alike.
4. Write the two items. They look alike on the surface, so the learner cannot tell them by the
   words. One item is a case where the first idea applies and the other is a case where the
   second idea applies. Say which idea applies and why is the learner's job, not the agent's.
5. Give the learner both items and wait. Do not show the key and do not say which one applies
   before the learner answers.
6. If the learner asks for help, use the hint ladder one step at a time: hint, strong hint,
   partial example, answer. Never skip a step.
7. Ask for confidence from 1 to 5 before the reveal. Then reveal the key and grade the learner's
   words against the concept notes and the sources.
8. Log the pair in `50_Review/Misconceptions.md`, under the confusion log, in the format the file
   describes: `YYYY-MM-DD, [[Objective_id|Objective]]: I answered X, but it is Y. I mix up X and
   Y. Open.` Write the entry only after the learner confirms it. The agent never writes the
   learner's own answer in the entry, so the learner gives the words for it.
9. Close a confusion only when the learner tells the two apart without help more than once. A
   right answer right after the hint ladder does not close it. When it is closed, mark it
   `closed YYYY-MM-DD` in the log.
10. Do not edit concept notes and do not add flashcards here. Offer the `mistake-review` skill
    when the learner wants a corrected card.

```bash
python3 -I 90_System/Scripts/misconception_report.py --min-wrong 2
python3 -I 90_System/Scripts/misconception_report.py --json
```
