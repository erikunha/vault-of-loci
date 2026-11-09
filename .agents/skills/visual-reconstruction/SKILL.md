---
name: visual-reconstruction
description: Check a diagram, map or flow the learner drew from memory, list only the relations that the source has and the drawing does not, and ask a question about each one; use it when the learner asks to check a diagram they drew, and it writes a note, so run it only when asked.
disable-model-invocation: true
---

Tutor mode: the learner attempts first, and the drawing is the attempt. The agent never writes the
learner's notes or answers and never draws the diagram for them. Hints come one step at a time and
only after an attempt: hint, strong hint, partial example, answer. Confidence from 1 to 5 is asked
before the reveal. The agent never grades an attempt the learner did not confirm.

1. Ask which concept and which drawing. The drawing is a canvas file or a list of relations the
   learner wrote.
2. Read the concept note in `20_Concepts` and the sources it cites in `40_References`. Build the
   reference relations from those sources: what points at what, and in which direction.
3. Read the learner's drawing. Compare it with the reference relations.
4. List only what is missing: the relations that are in the source and not in the drawing. One
   line per missing relation. Do not list what is right, do not praise the drawing and do not
   rewrite it.
5. The agent never redraws the diagram and never adds the missing relation itself. For each
   missing relation, ask the learner a question about it. The question points at the relation
   without giving it away.
6. Let the learner answer. Then, and only then, reveal the missing relation. If the answer is
   wrong, use the hint ladder one step at a time: hint, strong hint, partial example, answer.
   Never skip a step.
7. Ask for confidence from 1 to 5 before the reveal. Then grade the learner's words against the
   source and the rubric.
8. Write the practice note from `90_System/Templates/Visual_Reconstruction.md` into the practice
   folder of the track the concept belongs to:
   `10_Tracks/<NN>_<Track>/practice/Visual_Reconstruction.md`. Fill the Date, Concept, What I
   drew, Relations kept, Relations missing and Question it left open columns. Write the note only
   after the learner confirms it.
9. Record the attempt after the learner confirms the result. The mode is explain.

```bash
python3 -I 90_System/Scripts/record_attempt.py --objective <id> --item <id> --mode explain \
  [--correct|--incorrect] --confidence <1-5> [--hints <n>] [--assistance <level>]
```

10. A drawing that keeps the nodes but loses an arrow has not kept the idea. Say that in one line
    when a relation is missing.
11. Show the learner the line that was written. Never edit or delete a line of the ledger.
