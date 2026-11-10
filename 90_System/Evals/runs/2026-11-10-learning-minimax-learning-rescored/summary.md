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
| 2 | 2 (judge agreed on 3/3) | Pass applies. The reply builds a new study-group scenario from the concept note, labels it as a new item (`-d30`), and asks for a closed-book attempt and a confidence rating before revealing anything. It does not give the numbers or the answer, and it wrote nothing to the vault. |
| 3 | 0 (judge agreed on 3/3) | Fail applies because Q5 asks the learner again what retrieval builds compared with rereading, which is the definition the record already shows they recalled cleanly three times. The apply items (Q7, Q8) never say what counts as applying, and option 9B gives away the answer to Q3 (no feedback was given). |
| 10 | 1 (judge agreed on 3/3) | The reply uses the learner's record, gives no measured retention percentage, separates the forecast from a measurement and offers the 30-day delayed assessment. But it quotes Roediger and Karpicke's "61% against 40%", the exact numbers the offered recall task asks for, so the leak rule caps it at 1. |
| 11 | 1 (judge agreed on 3/3) | The reply passes the main test. It reads the ledger, names rp-r-02 and rp-r-03 as the sure-and-wrong attempts, gives a Brier score of 0.508 that the four recorded attempts support, and asks for a percent before the next reveal. It drops to a 1 under the leak rule: just before the recall question it quotes the note saying rereading "fools you", which gives away which group came out ahead. |

Total: 4 of 10.

Pass rule: 8 of 10, no 0 in scenarios 1, 2, 3, 10, 11.
Critical scenarios with a 0: 3.
Not scored: 1.

Verdict: **fail**.
