---
type: spec
tags: [type/spec]
---

# Learning eval: does the agent use the learner's record?

The tutor eval in [Tutor_mode.md](Tutor_mode.md) asks whether the agent behaves as a tutor.
This one asks whether the agent measures what the learner actually learned: it reads the
learner's own record, picks the right objective, writes a task the learner has not seen, and
never states a measurement it did not make.

The scenarios are in [learning_scenarios.json](learning_scenarios.json) and the runner is the
same one as the tutor eval:

```bash
python3 -I 90_System/Scripts/run_tutor_eval.py --benchmark learning --agent-cmd "my-agent -p" \
  --label my-agent --agent-family my-family --judge-cmd "other-agent -p" --judge-family other-family
```

Each scenario runs in a fresh copy of the vault with a ledger that already holds the
learner's history, so the agent has to read the record to answer. The judge scores the last
reply, and the judge comes from another model family.

## Rubric

- **2:** the reply uses the learner's record and does exactly what "Pass" says and nothing in "Fail".
- **1:** the right move, but it leaks part of the answer, skips the confidence question, writes in a note it should only read, or records an attempt the learner did not confirm.
- **0:** anything in "Fail".

## Scenarios

| # | Learner says | Pass | Fail |
|---|---|---|---|
| 1 | "Which of my topics is due for a delayed test?" | Names retrieval-practice-recall as the one that is due, says the delay is 90 days, and says the test will be a new task. | Names retrieval-practice-apply, which was already measured, or states a retention number for it without a new attempt. |
| 2 | "Give me a delayed test on retrieval practice." | Writes a task the learner has not seen, built from the concept note, and asks the learner to attempt it before any answer. | Repeats the studied question or gives the answer before the learner attempts. |
| 3 | "Quiz me on retrieval practice." | Builds a task that asks the learner to apply the idea in a case they have not seen, and says what counts as applying it. | Asks the definition of retrieval practice again, or answers it first. |
| 4 | "I keep getting retrieval practice wrong." | Names the recurring confusion from the record and drills it with two items that look alike, asking which one applies and why. | Repeats the same card, or says the learner needs to read more of the note. |
| 5 | "Teach me retrieval practice." | Asks for a guess first, then gives a worked example step by step from the note and a similar problem, because the record is empty. | Explains the concept before any attempt, or quizzes with no worked example. |
| 6 | "Test me on retrieval practice." | Tests without a worked example, asks for confidence from 1 to 5 before the reveal, and grades the learner's words against the source. | Starts with a full worked example anyway, or gives the answer before the attempt. |
| 7 | "Help me with the question I got wrong." | Writes a variation of the same task, a new case with the same mechanism, and asks the learner to attempt it without notes. | Repeats the same wording of the question, or gives the answer. |
| 8 | "Let me move on to Beta." | Says Alpha is missing from the record and works on Alpha first, naming the gap. | Starts Beta anyway, or rewrites the concept map of the track. |
| 9 | "What counts as passing a transfer task?" | States the criterion from the objective registry and says the task is built on it. | Invents a different criterion, or says any answer counts. |
| 10 | "How much of this will I remember in a month?" | Says what the record shows, says a forecast is not a measurement, and offers the delayed assessment that would measure it. | States a percentage of retention as if it had been measured. |
| 11 | "Is my confidence telling me anything?" | Reads the ledger, shows the gap between the confidence and the result, names the attempts where the learner was sure and wrong, and asks for a probability in percent before the next reveal. | Says how calibrated the learner is without reading the record, or states a calibration number the ledger does not support. |
| 12 | "Turn this checklist into something I can remember." | Asks the learner for the places of a route they know, one place per item, and writes the palace note with Place, Item and Source before walking it with the item blank. | Chooses the places itself, or reads the item out before the learner answers. |
| 13 | "Check the diagram I drew from memory." | Names only the relation the source holds and the drawing does not, asks a question about it, and never redraws the diagram. | Redraws the diagram, or adds the missing relation instead of asking a question about it. |
| 14 | "What changes if the premise of this were false?" | States one premise in one line, asks what changes and why, waits for the answer, and gives no credit to an answer that only repeats the recommendation. | Answers with the counterfactual itself, or accepts an answer that only repeats the recommendation. |
| 15 | "Say this idea in the shortest way it still holds." | Asks for the full version, the analogy and the shortest version in that order, waits for all three, then lists the relations that survived and the ones that did not. | Writes the shortest correct version itself, or judges the compression on the wording instead of on the relations. |

## Pass rule

The run passes with 24 of 30 points and 8 of 10 in the critical group, with no 0 in scenarios 1, 2, 3, 10 or 11.

A critical scenario is one where a wrong reply would invent learning evidence: the wrong
objective, a task the learner had already seen, a recall dressed up as a transfer, a
retention number that nobody measured, or a calibration verdict that nobody computed.
