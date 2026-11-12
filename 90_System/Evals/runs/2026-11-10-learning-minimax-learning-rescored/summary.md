---
type: log
summary: Learning eval run scores of minimax-learning on 2026-11-10, judged by anthropic.
tags: [type/log]
---

# Scores: minimax-learning, 2026-11-10

Agent family: minimax. Agent model: not recorded. Judge family: anthropic. Judge model: not recorded. Judge command: `claude -p "$(cat)"`.

| # | Score | Checks | Why |
|---|---|---|---|
| 1 | not scored | FAILED: wrote 50_Review/Delayed_Tests_2026-11-10.md | the agent run failed; nothing to score |
| 2 | 2 (judge agreed on 3/3) | passed | Pass applies. The reply builds a new study-group scenario from the concept note, labels it as a new item (`-d30`), and asks for a closed-book attempt and a confidence rating before revealing anything. It does not give the numbers or the answer, and it wrote nothing to the vault. |
| 3 | 0 (judge agreed on 3/3) | passed | Fail applies because Q5 asks the learner again what retrieval builds compared with rereading, which is the definition the record already shows they recalled cleanly three times. The apply items (Q7, Q8) never say what counts as applying, and option 9B gives away the answer to Q3 (no feedback was given). |
| 10 | 1 (judge agreed on 3/3) | FAILED: a reply contains '61%' (turn 2); a reply contains '40%' (turn 2) | The reply uses the learner's record, gives no measured retention percentage, separates the forecast from a measurement and offers the 30-day delayed assessment. But it quotes Roediger and Karpicke's "61% against 40%", the exact numbers the offered recall task asks for, so the leak rule caps it at 1. |
| 11 | 1 (judge agreed on 3/3) | passed | The reply passes the main test. It reads the ledger, names rp-r-02 and rp-r-03 as the sure-and-wrong attempts, gives a Brier score of 0.508 that the four recorded attempts support, and asks for a percent before the next reveal. It drops to a 1 under the leak rule: just before the recall question it quotes the note saying rereading "fools you", which gives away which group came out ahead. |

Total: 4 of 10.
95% interval of the total: 1 to 7, over the 4 scored scenarios (bootstrap over scenarios, 10000 resamples, seed 20261109). The pass mark 8 is outside it.
Coverage: 5 of 15 scenarios of the benchmark.

Pass rule: 8 of 10, no 0 in scenarios 1, 2, 3, 10, 11.
Critical scenarios with a 0: 3.
Not scored: 1.
Deterministic checks failed in scenarios: 1, 10. The checks are shown next to the score and do not change it.

Verdict: **fail**.

Version: run.json records no hashes of the scenarios, rubric and judge prompt. This summary assumes they are the ones of today.

Version: scores.json records no hashes of the scenarios, rubric and judge prompt. This summary assumes they are the ones of today.
