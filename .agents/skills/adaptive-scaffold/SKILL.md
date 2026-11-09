---
name: adaptive-scaffold
description: Read the record of an objective and teach it with a worked example and a similar problem when the learner is new to the topic or keeps failing on it, then drop the steps as the record rises; use it when the learner does not know a topic yet or keeps getting it wrong, and it writes a file, so run it only when asked.
disable-model-invocation: true
---

Tutor mode: the learner attempts first, and a guess comes before any help. The agent never writes
the learner's notes or answers. Hints come one step at a time and only after an attempt: hint,
strong hint, partial example, answer. Confidence from 1 to 5 is asked before the reveal. The agent
never grades an attempt the learner did not confirm.

The rule of the vault: teach a new learner, do not only test.

1. Read the record of the objective. The report shows what was attempted and how it went, and the
   plan shows the item due for this objective.

```bash
python3 -I 90_System/Scripts/retention_report.py
python3 -I 90_System/Scripts/schedule_review.py --objective <id>
```

2. Say in one line what the record says, so the learner can correct it. Then choose the level of
   support:
   - The record is empty, or the last attempt was wrong: teach.
   - The record shows correct attempts: ask straight away, with no worked example.
3. When you teach, follow the guess with a worked example from a source note, step by step. Use
   the concept note in `20_Concepts` and the sources it cites in `40_References`. Then give a
   similar problem for the learner, and only then a second try. The learner works on the similar
   problem before the second try, not after.
4. When the learner gets it right, the steps come off: fewer steps, then no steps, then a new
   case. What helps a beginner can hinder someone who already knows the topic. The scaffolding is
   dropped as the record rises and is never kept forever.
5. If the answer is wrong, or the learner asks to try again, use the hint ladder one step at a
   time: hint, strong hint, partial example, answer. Never skip a step.
6. Ask for confidence from 1 to 5 before the reveal. Then reveal and grade the learner's words
   against the source.
7. Record the attempt only after the learner confirms the result. Use the item id and the mode of
   the item. If the learner took a hint or a worked example, pass `--assistance` and `--hints`: an
   attempt with help stays out of the rate.

```bash
python3 -I 90_System/Scripts/record_attempt.py --objective <id> --item <id> --mode <mode> \
  [--correct|--incorrect] [--at <iso>] --confidence <1-5> [--probability <0-1>] [--hints <n>] \
  [--assistance <level>] [--grading <method>] [--rubric <ver>] [--revision <rev>] [--minutes <n>]
```

8. Show the learner the line that was written. Do not edit the concept note and do not write the
   learner's study layer. Never edit or delete a line of the ledger.
