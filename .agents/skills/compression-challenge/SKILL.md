---
name: compression-challenge
description: Ask the learner for a concept three times, in full, as an analogy and as the shortest version that still holds, list the relations that survived and the ones that did not, and record the attempt; use it when the learner wants to test whether an idea survives being shortened, and it writes a file, so run it only when asked.
disable-model-invocation: true
---

Tutor mode: the learner attempts first and the agent never interrupts. The agent never rewrites the
learner's versions and never writes the learner's notes or answers. Hints come one step at a time
and only after an attempt: hint, strong hint, partial example, answer. Confidence from 1 to 5 is
asked before the reveal. The agent never grades an attempt the learner did not confirm.

The rule of this exercise: a short version that keeps the causal relations and drops the examples
is a good compression. A short version that drops a relation is not a summary, it is a different
claim.

1. The learner picks a concept they have studied. Read the concept note in `20_Concepts` and the
   sources it cites in `40_References`. Note the relations of the concept: what causes what, what
   depends on what, and what breaks when a part is missing.
2. Ask for the three versions, in this order, and do not interrupt:

   - the full version, as the learner would explain it from the notes;
   - the analogy, the same idea in terms of something else;
   - the shortest version that still holds.

   Wait for all three before saying anything about them.
3. List which relations of the concept survived in the shortest version and which did not. Use the
   concept note and its sources to decide. Name each relation in plain words. Only list what is
   missing. Do not write a shorter version for the learner and do not edit the words they used.
4. Ask the learner to put the missing relation back in their own words. One relation at a time.
5. Record the attempt only after the learner confirms the result. The mode is `explain`, because
   the exercise asks for the mechanism and not only the definition.

```bash
python3 -I 90_System/Scripts/record_attempt.py --objective <id> --item <id> --mode explain \
  [--correct|--incorrect] --confidence <1-5> [--probability <0-1>] [--hints <n>] \
  [--assistance <level>] [--grading <method>]
```

6. A compression that loses a relation is not a wrong answer, it is a different claim. So it goes
   to the mistakes log and not to a card about the definition. Ask the learner for the words of
   the relation they put back, then add the entry to `50_Review/Mistakes.md` in the format that
   file describes, with the kind of error `reasoning` and the AI use `none`:

```text
YYYY-MM-DD, [[Concept_Name|Concept name]]: I answered X. The answer is Y. I went wrong because Z. Kind: reasoning. AI: none. Open.
```

7. Keep the three versions in the compression note of the track. If there is no note yet, copy
   `90_System/Templates/Compression_Challenge.md` into `10_Tracks/<NN>_<Track>/practice/` and fill
   the Date, Concept, Relations kept and Relations lost columns. The three version columns stay
   in the learner's words.
8. Show the learner the line that was written. Never edit or delete a line of the ledger.
