---
name: dependency-check
description: Check the prerequisites of a concept against the ledger before the learner moves on, say in one line which prerequisite is missing, and work on that one first; use it before the learner starts a new concept, and it writes a file, so run it only when asked.
disable-model-invocation: true
---

Tutor mode: the learner attempts first and without notes. The agent never writes the learner's
notes or answers. Hints come one step at a time and only after an attempt: hint, strong hint,
partial example, answer. Confidence from 1 to 5 is asked before the reveal. The agent never
grades an attempt the learner did not confirm.

1. Run the check and read it.

```bash
python3 -I 90_System/Scripts/dependency_check.py
```

2. Read the map. The script reads the "Needs first" column of the concept map of each track
   (`10_Tracks/<NN>_<Track>/practice/Concept_Map.md`) and the edges of the canvases in `30_Maps`,
   then joins them with the ledger. For each concept it prints the prerequisites and the state of
   each one: `never studied`, `only tested with help`, `last attempt was wrong`, `not tested for N
   days` or `ok`. A concept with a gap is not ready.

```bash
python3 -I 90_System/Scripts/dependency_check.py --target <name>
python3 -I 90_System/Scripts/dependency_check.py --json
```

3. If there is a gap, say in one line which prerequisite is missing. Then work on that
   prerequisite first and leave the new concept for later. Do not move on to the new concept while
   a gap is open.
4. Work the prerequisite the way the record asks for it. A prerequisite that was never studied or
   was only tested with help is taught with a worked example from a source note, step by step,
   then a similar problem for the learner. A prerequisite whose last attempt was wrong is
   practised with a variation of the same task.
5. If the answer is wrong, or the learner asks to try again, use the hint ladder one step at a
   time: hint, strong hint, partial example, answer. Never skip a step.
6. Ask for confidence from 1 to 5 before the reveal. Then reveal and grade the learner's words
   against the source.
7. Record each attempt only after the learner confirms the result. Use the item id and the mode of
   the item. If the learner took a hint, pass `--assistance` and `--hints`: an attempt with help
   stays out of the rate.

```bash
python3 -I 90_System/Scripts/record_attempt.py --objective <id> --item <id> --mode <mode> \
  [--correct|--incorrect] [--at <iso>] --confidence <1-5> [--probability <0-1>] [--hints <n>] \
  [--assistance <level>] [--grading <method>] [--rubric <ver>] [--revision <rev>] [--minutes <n>]
```

8. Run the check again when the prerequisite is done, and say whether the new concept is ready.
9. Never rewrite the concept map of the track. The map belongs to the learner. Point at the gap
   and let the learner change the map.
10. Show the learner every line that was written. Never edit or delete a line of the ledger.
