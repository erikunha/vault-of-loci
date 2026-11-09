---
name: calibration-coach
description: Read the learning ledger and show the learner how well their confidence matches the result, then ask for a probability from 0 to 100 before the next reveal and record it; use it when the learner asks whether their confidence is telling them anything, and it writes to the ledger, so run it only when asked.
disable-model-invocation: true
---

Tutor mode: the learner attempts first, and the agent never writes the learner's notes or answers.
Hints come one step at a time and only after an attempt: hint, strong hint, partial example, answer.
Confidence is asked before the reveal. The agent never grades an attempt the learner did not confirm.

The question this skill answers: is the confidence telling the learner anything? The coach measures
the gap between how sure the learner was and what happened. It does not measure what was learned.

1. Run the coach and read the report. It shows the Brier score with an explicit probability, the
   Brier score with the 1 to 5 scale, the reliability table and the sharpest cases.

```bash
python3 -I 90_System/Scripts/calibration_coach.py
```

2. For one objective, or as JSON to read the numbers closely:

```bash
python3 -I 90_System/Scripts/calibration_coach.py --objective <id>
python3 -I 90_System/Scripts/calibration_coach.py --json
```

3. Say in one line what the gap means for what to study next. Being sure and wrong is a different
   gap from being unsure and right:
   - Sure and wrong: the material is not where the learner thinks it is. Reread the concept note of
     that objective and test it again.
   - Unsure and right: the knowledge is there and the confidence is behind it. Keep the same
     material, use it again later, and let the confidence come up on its own.
   - Many bins with few attempts: the ledger is too small to say anything. Keep going and read it
     again later.
4. From the next reveal on, ask for a probability from 0 to 100 instead of only the 1 to 5 scale,
   and keep asking for the 1 to 5 scale as well. Say that a number in percent is what makes the gap
   visible. Do not explain the concept while asking.
5. Record each attempt with the probability the learner gave. The learner confirms the result
   first. A percentage from 0 to 100 becomes a number from 0 to 1, so 70 becomes 0.7.

```bash
python3 -I 90_System/Scripts/record_attempt.py --objective <id> --item <id> --mode <mode> \
  --correct --confidence <1-5> --probability <0-1>
```

6. Show the learner the line that was written. Never edit or delete a line of the ledger, and never
   write the learner's answers, guesses or notes.
