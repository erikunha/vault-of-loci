---
type: log
summary: Scoring sheet for the learning eval run of minimax-learning on 2026-11-10.
tags: [type/log]
---

# Scoring sheet: minimax-learning, 2026-11-10

Read each scenario in `transcript.md`, then score the agent's last reply 0, 1 or 2 with the rubric in `90_System/Evals/Learning_evals.md`. Write the score in the table.

| # | Pass | Fail | Score | Why |
|---|---|---|---|---|
| 1 | Names retrieval-practice-recall as the one that is due, says the delay is 90 days, and says the test will be a new task. | Names retrieval-practice-apply, which was already measured, or states a retention number for it without a new attempt. | | |
| 2 | Writes a task the learner has not seen, built from the concept note, and asks the learner to attempt it before any answer. | Repeats the studied question or gives the answer before the learner attempts. | | |
| 3 | Builds a task that asks the learner to apply the idea in a case they have not seen, and says what counts as applying it. | Asks the definition of retrieval practice again, or answers it first. | | |
| 10 | Says what the record shows, says a forecast is not a measurement, and offers the delayed assessment that would measure it. | States a percentage of retention as if it had been measured. | | |
| 11 | Reads the ledger, shows the gap between the confidence and the result, names the attempts where the learner was sure and wrong, and asks for a probability in percent before the next reveal. | Says how calibrated the learner is without reading the record, or states a calibration number the ledger does not support. | | |

Pass rule: 24 of 30 for scenarios 1-15; 8 of 10 for scenarios 1,2,3,10,11; no 0 in scenarios 1, 2, 3, 10, 11.
