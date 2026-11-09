---
name: error-recovery
description: Take an item whose last attempt was wrong and write a variation of the same task under the id the plan prints, so the learner works with the idea and not with the memory of the sentence, then record the graded attempt in the learning ledger; use it when a mistake was never recovered, and it writes a file, so run it only when asked.
disable-model-invocation: true
---

Tutor mode: the learner attempts first and without notes. The agent never writes the learner's
notes or answers. Hints come one step at a time and only after an attempt: hint, strong hint,
partial example, answer. Confidence from 1 to 5 is asked before the reveal. The agent never
grades an attempt the learner did not confirm.

1. Run the list of errors and read it.

```bash
python3 -I 90_System/Scripts/schedule_review.py --errors
```

2. Take the first item. Each line gives the objective, the item id, how many attempts it had and
   when the last one happened. It also gives the id a variation of the task must carry, for
   example `item-a-v2`.
3. Read the original item and the source note behind it. Find the mechanism the item tests: the
   rule, the contrast, the step that makes the answer right.
4. Write the variation. It keeps the same mechanism and changes the surface: new numbers, a new
   context, a different wording, a different order. The learner must work with the idea and not
   with the memory of the sentence. Give the variation the id the plan printed.
5. Give the variation and wait. Say nothing about the content before the attempt: no excerpt, no
   summary, no hint.
6. If the answer is wrong, or the learner asks to try again, use the hint ladder one step at a
   time: hint, strong hint, partial example, answer. Never skip a step.
7. Ask for confidence from 1 to 5 before the reveal. Then reveal and grade the learner's words
   against the source.
8. Record the attempt with the id of the variation, not with the id of the original item.

```bash
python3 -I 90_System/Scripts/record_attempt.py --objective <id> --item <id> --mode <mode> \
  [--correct|--incorrect] [--at <iso>] --confidence <1-5> [--probability <0-1>] [--hints <n>] \
  [--assistance <level>] [--grading <method>] [--rubric <ver>] [--revision <rev>] [--minutes <n>]
```

9. A mistake is closed only after a correct recall later, without help. A right answer right
   after the hint ladder does not close it. When the learner gets it right later without help,
   mark the entry `closed YYYY-MM-DD` in `50_Review/Mistakes.md`.
10. Show the learner the line that was written. Never edit or delete a line of the ledger.
