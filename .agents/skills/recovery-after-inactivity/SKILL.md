---
name: recovery-after-inactivity
description: Run the short diagnostic the vault keeps for a break of 14 days or more without an attempt, work a few items with the learner, then report the length of the break and offer the plan for the next days without calling the backlog a debt. Use when the learner comes back after time away. Writes a file, so only run when asked.
disable-model-invocation: true
---

Tutor mode: the learner attempts first. The agent never writes the learner's notes, answers or
guesses. Hints come one step at a time and only after an attempt. Confidence from 1 to 5 is asked
before any reveal. The agent never grades an attempt the learner did not confirm.

1. Run the diagnostic for a return after a break. A break is 14 days or more without an attempt.

```bash
python3 -I 90_System/Scripts/schedule_review.py --recovery
```

2. If the script says there is no break to recover from, the last attempt is recent. Run the normal
   plan for the day instead and follow the `schedule-review` skill.

3. Run the small diagnostic. It prints the days away, the number of items waiting, and a few items
   to do. One of them is an explanation and one is an application when the record has them. Do not
   dump the queue and do not print the whole backlog to the learner.
4. Ask the learner which of the diagnostic items to start with. For each one, read the source note
   and ask the question. Wait for the learner's answer. Say nothing about the content before the
   answer: no excerpt, no summary, no hint.
5. If the answer is wrong, or the learner asks to try again, use the hint ladder one step at a time:
   hint, strong hint, partial example, answer. Never skip a step.
6. Ask for confidence from 1 to 5 before the reveal. Then reveal and grade the learner's words
   against the source and the rubric.
7. Record the attempt only after the learner confirms the result. Use the item id and the mode from
   the diagnostic. If the learner took a hint, pass `--assistance` and `--hints`: an attempt with
   help stays out of the rate.

```bash
python3 -I 90_System/Scripts/record_attempt.py --objective <id> --item <id> --mode <mode> \
  --correct --confidence <1-5> [--hints <n>] [--assistance <level>] [--grading <method>] \
  [--rubric <ver>] [--revision <rev>] [--minutes <n>] [--at <iso>] [--probability <0-1>]
```

8. After the diagnostic, say how long the break was and how many items are waiting. Offer the plan
   for the next days, with the daily cap and about 2 new cards:

```bash
python3 -I 90_System/Scripts/schedule_review.py
python3 -I 90_System/Scripts/schedule_review.py --cap 15 --new 2
```

9. Do not present the waiting items as a debt. Do not say the learner is behind or that the break
   cost anything. Missing days carry no penalty and no streak resets. Show the plan and let the
   learner choose where to start.
