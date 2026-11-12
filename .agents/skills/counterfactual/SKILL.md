---
name: counterfactual
description: Ask the learner what would change if one premise of a concept changed, so the answer is about the mechanism and not a repeated recommendation, then grade it against the source and record the attempt; use it when the learner wants to understand a concept deeper, and it writes a note, so run it only when asked.
disable-model-invocation: true
---

Tutor mode: the learner attempts first and without notes. The agent never writes the learner's
notes or answers. Hints come one step at a time and only after an attempt: hint, strong hint,
partial example, answer. Confidence from 1 to 5 is asked before the reveal. The agent never
grades an attempt the learner did not confirm.

1. Take the concept the learner names. If they name none, take the concept of the open note or the weakest one in the record, and say which. Do not ask the learner to choose one.
2. Read the concept note in `20_Concepts` and the sources it cites in `40_References`.
3. Pick one premise from the concept note yourself, in the same reply as step 1: a precondition the idea depends on, a limit, an
   assumption it rests on. State the counterfactual in one line: "if this premise were not true,
   what would change?"
4. Ask what changes and why. The learner answers first, without notes. Wait for the answer.
5. If the answer only repeats the recommendation, say that the recommendation repeating is not an
   answer and ask for the mechanism instead of giving the answer: which step breaks, and what
   follows from that.
6. Grade the learner's words against the source and the rubric, not against how the conversation
   went. A fluent answer that never names the mechanism gets no credit.
7. If the answer is wrong, or the learner asks to try again, use the hint ladder one step at a
   time: hint, strong hint, partial example, answer. Never skip a step.
8. Ask for confidence from 1 to 5 before the reveal. Then reveal what the source says the
   mechanism is.
9. Write the practice note from `90_System/Templates/Counterfactual.md` into the practice folder
   of the track the concept belongs to:
   `10_Tracks/<NN>_<Track>/practice/Counterfactual.md`. Fill the Date, Concept, Premise changed,
   What changes and Why columns. Write the note only after the learner confirms it.
10. Record the attempt after the learner confirms the result. The mode is apply.

```bash
python3 -I 90_System/Scripts/record_attempt.py --objective <id> --item <id> --mode apply \
  [--correct|--incorrect] --confidence <1-5> [--hints <n>] [--assistance <level>]
```

11. Show the learner the line that was written. Never edit or delete a line of the ledger.
