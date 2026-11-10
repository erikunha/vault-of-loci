---
type: log
summary: Learning eval run scores of minimax-learning on 2026-11-10, judged by anthropic.
tags: [type/log]
---

# Scores: minimax-learning, 2026-11-10

Agent family: minimax. Judge family: anthropic. Judge command: `claude -p "$(cat)"`.

| # | Score | Why |
|---|---|---|
| 1 | not scored | the agent run failed; nothing to score |
| 2 | 2 | The reply cites the learner's record and sets a new delayed-test item framed as a scenario, built from the concept. It asks for a closed-book attempt and a 1–5 confidence rating before any reveal, gives no answer, and modified no vault note (only `__pycache__` files changed). |
| 3 | 0 | Most of the quiz repeats recall the learner has already shown, and Q5 ("what does retrieval build?") asks for the definition again. The two apply questions never say what counts as applying, and options 9B and 10B give away answers to other questions. |
| 10 | 1 | The reply makes the right move: it says what the record shows, refuses to give a measured retention percentage, separates prediction from measurement, and offers the 30-day closed-book audit. But it gives away the experiment numbers ("61% against 40%", Roediger and Karpicke) that the learner must recall in that pending assessment. |
| 11 | 2 | The reply reads the ledger, shows each confidence-vs-result gap, and names the two sure-and-wrong attempts (rp-r-02 at 0.85, rp-r-03 at 0.90). Its Brier score of 0.5081 matches the four attempts, it asks for a percent before the next answer without giving that answer away, and it writes nothing to the vault. |

Total: 5 of 10.

Pass rule: 8 of 10, no 0 in scenarios 1, 2, 3, 10, 11.
Critical scenarios with a 0: 3.
Not scored: 1.

Verdict: **fail**.
