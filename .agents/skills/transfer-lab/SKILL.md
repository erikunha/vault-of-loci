---
name: transfer-lab
description: Write a transfer task for an objective that was studied but never applied, put it in the track's practice note with the item id and the rubric from the lab, and record the graded attempt in the learning ledger; use it when the learner wants to practise applying an idea instead of repeating it, and it writes a file, so run it only when asked.
disable-model-invocation: true
---

Tutor mode: the learner attempts first and without notes. The agent never writes the learner's
notes or answers. Hints come one step at a time and only after an attempt: hint, strong hint,
partial example, answer. Confidence from 1 to 5 is asked before the reveal. The agent never
grades an attempt the learner did not confirm.

1. Run the lab and read the first objective that owes a task.

```bash
python3 -I 90_System/Scripts/transfer_lab.py
```

2. Read the objective line under "Tasks to write". It gives the concept note the objective belongs
   to, the criterion that decides what counts, the item id the new task must carry, the mode and
   the rubric with its three levels.
3. Read the concept note and the sources it cites. The concept note is in `20_Concepts` and the
   sources are in `40_References`.
4. Write the task. It is a case the learner has not seen, built from the criterion and from the
   concept note and its sources. Never build it from the example that was studied. The task asks
   the learner to apply the idea to the new case and to say why it applies.
5. Put the task in the practice note of the track the concept belongs to:
   `10_Tracks/<NN>_<Track>/practice/Transfer_Lab.md`. The track is the one the concept note lists
   in its `tracks` property. If the file does not exist yet, copy
   `90_System/Templates/Practice/Transfer_Lab.md` into the practice folder of that track. Fill the
   Date, Objective and Task columns. Leave the Notes column empty for the learner. After the
   learner confirms the result, fill the Criterion met column with the level of the rubric.
6. Give the task and wait. Say nothing about the content before the attempt: no excerpt, no
   summary, no hint.
7. If the answer is wrong, or the learner asks to try again, use the hint ladder one step at a
   time: hint, strong hint, partial example, answer. Never skip a step.
8. Ask for confidence from 1 to 5 before the reveal. Then reveal and grade the learner's words
   with the rubric the lab printed.
9. Record the attempt only after the learner confirms the result. Use the item id and the mode the
   lab printed. If the learner took a hint, pass `--assistance` and `--hints`: a task with a hint
   stays out of the transfer rate.

```bash
python3 -I 90_System/Scripts/record_attempt.py --objective <id> --item <id> --mode <mode> \
  [--correct|--incorrect] [--at <iso>] --confidence <1-5> [--probability <0-1>] [--hints <n>] \
  [--assistance <level>] [--grading <method>] [--rubric <ver>] [--revision <rev>] [--minutes <n>]
```

10. An attempt that repeats the definition instead of applying it does not count as a transfer.
    The rubric level is 0 and the objective still owes a task. Say that in one line.
11. Show the learner the line that was written. Never edit or delete a line of the ledger.
