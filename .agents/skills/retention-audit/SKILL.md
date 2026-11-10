---
name: retention-audit
description: Audit the learning ledger for objectives that passed the 7, 30 and 90 day horizons with no attempt without help, write a new closed book task for each one that is due, and record the confirmed attempt. Use when the learner asks what is due for a delayed test. Writes a file, so only run when asked.
disable-model-invocation: true
---

Tutor mode: the learner attempts first, closed book. The agent never writes the learner's notes,
answers or guesses. Hints come one step at a time and only after an attempt. Confidence from 1 to 5
is asked before any reveal. The agent never grades an attempt the learner did not confirm.

This skill answers "what is due for a delayed test". It does not answer "what should I study
today", which is `schedule_review.py`. The two sound alike and give different answers: this one
names the objective that passed a 7, 30 or 90 day horizon with no attempt without help, and the
other ranks what is worth another try. If the learner asked what to study today, use the other
skill.

1. Run the audit and read it. It reports the objectives that passed a horizon with no attempt
   without help, and the objectives that were never tested.

```bash
python3 -I 90_System/Scripts/retention_audit.py
```

2. Tell the learner which objectives are due. Say in one line that the delay has arrived but the
   retention at that horizon is still unknown until the attempt happens, and that an attempt with a
   hint stays out of the rate. To see only what is due, to change the horizons, or to see the audit
   as data:

```bash
python3 -I 90_System/Scripts/retention_audit.py --plan
python3 -I 90_System/Scripts/retention_audit.py --horizons 7,30,90
python3 -I 90_System/Scripts/retention_audit.py --json
```

3. For each objective that is due, write a new task the learner has not seen. Build it from the
   objective note and the sources it cites in the vault. Never reuse the example that was studied,
   and never take the task from memory of the conversation.
4. Use the item id the audit prints for that objective, and the mode of the objective from
   `90_System/Objectives.json`.
5. Give the task to the learner and wait. The attempt is closed book: no notes, no excerpt, no
   summary before the answer. If the learner asks for help after the attempt, use the hint ladder
   one step at a time: hint, strong hint, partial example, answer. Never skip a step.
6. Grade the learner's words against the source and the rubric. Ask for confidence from 1 to 5
   before the reveal.
7. Record the attempt only after the learner confirms the result, with the item id the audit
   printed. If the learner took a hint, pass `--assistance` and `--hints`: an attempt with help
   stays out of the rate.

```bash
python3 -I 90_System/Scripts/record_attempt.py --objective <id> --item <id> --mode <mode> \
  --correct --confidence <1-5> [--hints <n>] [--assistance <level>] [--grading <method>] \
  [--rubric <ver>] [--revision <rev>] [--minutes <n>] [--at <iso>] [--probability <0-1>]
```

8. Show the learner the line that was written. Never edit or delete a line of the ledger.
