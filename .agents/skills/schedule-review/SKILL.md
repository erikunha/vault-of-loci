---
name: schedule-review
description: Run the ranked review plan for today from the learning ledger, tell the learner which items are worth another try and why, work through them one by one with the hint ladder and confidence check, and record every confirmed attempt in the ledger. Use when the learner asks what to study today. Writes a file, so only run when asked.
disable-model-invocation: true
---

Tutor mode: the learner attempts first. The agent never writes the learner's notes, answers or
guesses. Hints come one step at a time and only after an attempt. Confidence from 1 to 5 is asked
before any reveal. The agent never grades an attempt the learner did not confirm.

1. Run the plan for today and read it. The plan says which items are worth another try and why, in
   the order to do them.

```bash
python3 -I 90_System/Scripts/schedule_review.py
```

2. Tell the learner the items in the order of the plan, each with the reason the plan gives. Say in
   one line that the priority is a ranking for the day and not a probability of remembering, and
   that the measured numbers live in `retention_report.py`.

```bash
python3 -I 90_System/Scripts/retention_report.py
```

3. Ask the learner how many of the items to do. A day is 10 to 20 reviews with about 2 new cards.
   When the plan says catch-up mode, the queue is over the cap, so no new cards are added until the
   queue is under it. To plan one objective only, or to see the plan as data:

```bash
python3 -I 90_System/Scripts/schedule_review.py --objective <id>
python3 -I 90_System/Scripts/schedule_review.py --cap 15 --new 2
python3 -I 90_System/Scripts/schedule_review.py --json
```

4. For each item, in the order of the plan, read the source note and ask the question. Wait for the
   learner's answer. Say nothing about the content before the answer: no excerpt, no summary, no
   hint.
5. If the answer is wrong, or the learner asks to try again, use the hint ladder one step at a time:
   hint, strong hint, partial example, answer. Never skip a step.
6. Ask for confidence from 1 to 5 before the reveal. Then reveal and grade the learner's words
   against the source and the rubric.
7. Record the attempt only after the learner confirms the result. Use the item id and the mode from
   the plan. If the learner took a hint, pass `--assistance` and `--hints`: an attempt with help
   stays out of the rate.

```bash
python3 -I 90_System/Scripts/record_attempt.py --objective <id> --item <id> --mode <mode> \
  --correct --confidence <1-5> [--hints <n>] [--assistance <level>] [--grading <method>] \
  [--rubric <ver>] [--revision <rev>] [--minutes <n>] [--at <iso>] [--probability <0-1>]
```

8. Show the learner the line that was written and the item left in the plan. Never edit or delete a
   line of the ledger.
