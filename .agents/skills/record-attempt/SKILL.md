---
name: record-attempt
description: Record a graded attempt in the learning ledger with the mode, the verdict, the hints taken and the learner's confidence, so retention and transfer can be measured later. Use when the learner finishes a recall, an explanation, an application or a discrimination task and confirms the result. Writes a file, so only run when asked.
disable-model-invocation: true
---

Tutor mode: the learner attempts first, and the agent never writes a verdict the learner did not
confirm. One event is written per attempt, and the ledger is appended, never edited.

1. Find the objective. Read `90_System/Objectives.json` and pick the objective the attempt belongs
   to. If none fits, ask the learner what the task was trying to make them able to do, write the
   criterion in one sentence, and add the objective to the registry before going on.
2. Use the mode of the attempt: recall, explain, apply or discriminate. A `study` event records
   that the material was seen and is not graded. `record_attempt.py` refuses a study event with a
   verdict, so use the right mode.
3. Keep the item id stable. The same id must mean the same question or task every time, because
   the report compares an attempt with what was done before.
4. Record the first try only. If the learner took a hint, pass `--assistance` and `--hints`. A
   hint is neither a pass nor a fail: the event is kept and the report leaves it out of the rate.
5. Ask for the confidence from 1 to 5 before the feedback, as the tutor rules say. If the learner
   gives a chance in percent instead, pass `--probability` too.
6. Grade as the learner confirmed it. When the learner asked the agent to grade and accepted the
   verdict, pass `--grading agent_graded`. The report keeps those attempts out of the rates and
   counts them separately.
7. Write the event:

```bash
python3 -I 90_System/Scripts/record_attempt.py --objective <id> --item <id> --mode <mode> \
  --correct --confidence <1-5>
```

8. Show the learner the line that was written. Offer `retention_report.py` when the learner
   wants to see what the ledger says so far. Never edit or delete a line of the ledger.

The schema and the metrics live in `90_System/Evals/Learning_outcomes.md`.
