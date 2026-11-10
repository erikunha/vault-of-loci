---
type: log
summary: Learning eval run scores of minimax-learning on 2026-11-10, judged by anthropic.
tags: [type/log]
---

# Scores: minimax-learning, 2026-11-10

Agent family: minimax. Judge family: anthropic. Judge command: `claude -p "$(cat)"`.

| # | Score | Why |
|---|---|---|
| 1 | 2 (judge agreed on 3/3) | The reply uses the ledger to name retrieval-practice-recall as the due objective, gives the 90-day delay, and sets a new closed-book task, so it meets Pass. It does not leak the percentages, it asks for confidence, it records nothing before the learner confirms, and it states no retention number for retrieval-practice-apply, so nothing in Fail or the score-1 conditions applies. |
| 2 | 2 (judge agreed on 3/3) | The tutor used the learner's record and wrote a new item (`-d30`), not a repeat of `rp-r-01`. It asked for a closed-book attempt with a confidence rating before giving any answer, leaked nothing, and recorded nothing without confirmation, which meets Pass and avoids every Fail condition. |
| 3 | 0 (judge agreed on 2/3) | The Fail rule decided it. Q2 asks again what the note says testing is for besides measuring learning, which is the core definition the learner already recalled three times. Q4–Q6 do ask for application in new cases, but the reply never says what counts as applying the idea, so Pass is not met either. |
| 10 | 1 (judge agreed on 3/3) | The reply uses the record, says a forecast is not a measurement, and offers the delayed 30-day test, so it avoids Fail. It loses a point under the leak rule because it gives the 61% versus 40% figures that item `rp-r-01` asks the learner to recall in that test. |
| 11 | 1 (judge agreed on 3/3) | The reply reads the ledger, correctly names rp-r-02 and rp-r-03 (10-31) as sure and wrong, and asks for a percent before the next reveal; its Brier score of 0.508 matches the ledger. Under the leak rule it scores 1, because it gives away the one-week result (61% vs 40%) that the learner was supposed to recall. |

Total: 6 of 10.

Pass rule: 8 of 10, no 0 in scenarios 1, 2, 3, 10, 11.
Critical scenarios with a 0: 3.

Verdict: **fail**.
