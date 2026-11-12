---
type: log
summary: Learning eval run scores of minimax-learning on 2026-11-10, judged by anthropic.
tags: [type/log]
---

# Scores: minimax-learning, 2026-11-10

Agent family: minimax. Agent model: not recorded. Judge family: anthropic. Judge model: not recorded. Judge command: `claude --model sonnet -p "$(cat)"`.

| # | Score | Checks | Why |
|---|---|---|---|
| 1 | 2 | passed | The reply names retrieval-practice-recall as due at 90 days and treats retrieval-practice-apply as already measured, with no retention number for it. It poses a fresh closed-book task, asks for confidence, and records nothing until the learner confirms, though it never literally says "new task". |
| 2 | 2 | passed | The tutor read the ledger, then wrote a new item (`retrieval-practice-recall-d30`) instead of repeating `rp-r-01`. It asked for a closed-book attempt and a 1-5 confidence rating before any answer, and it will record only after the learner confirms. It leaks no numbers or group answers, and the only files it changed were `__pycache__` files, not notes. |
| 3 | 0 | passed | The reply is a quiz of recall and explanation items (research details, meta-analysis numbers, multiple choice with options carrying answers), not a task applying retrieval practice to an unseen case, and it states no apply criteria. Q4 is the closest to apply, but it is a described-plan question, not a built apply task with what counts as applying it. |
| 10 | 1 | FAILED: a reply contains '61%' (turn 2); a reply contains '40%' (turn 2) | The reply uses the ledger, says a forecast is not a measurement, and offers the delayed 30-day assessment. It also states the 61% vs 40% one-week figures, which are the numbers the learner must recall in that assessment, so it leaks part of the answer. |
| 11 | 1 | FAILED: a reply contains '61%' (turn 2); a reply contains '40%' (turn 2) | The reply read the ledger, showed the confidence-versus-result gap, named rp-r-02 and rp-r-03 as sure and wrong, asked for a percent probability, and its Brier score of 0.5081 checks out against the four attempts. It leaks the answer to the recall item, though. It states that one week later testing won "61% to 40%", and those are the numbers the learner was meant to recall, so it falls under the rubric's leak rule for a 1. |

Total: 6 of 10.
95% interval of the total: 3 to 9, over the 5 scored scenarios (bootstrap over scenarios, 10000 resamples, seed 20261109). The pass mark 8 is inside it: other scenarios of the same kind could move the verdict.
Coverage: 5 of 15 scenarios of the benchmark.

Pass rule: 8 of 10, no 0 in scenarios 1, 2, 3, 10, 11.
Critical scenarios with a 0: 3.
Deterministic checks failed in scenarios: 10, 11. The checks are shown next to the score and do not change it.

Verdict: **fail**.

## Judges of this run

- `scores.json`: fail
- `scores-judge-anthropic-sonnet.json`: fail

- scores and scores-judge-anthropic-sonnet, 5 scenarios: percent agreement 1.0, Cohen's kappa 1.0, weighted kappa 1.0.
- Krippendorff's alpha across the 2 judges: ordinal 1.0, nominal 1.0.

Verdict of the run across its 2 judges: **fail**.

Version: run.json records no hashes of the scenarios, rubric and judge prompt. This summary assumes they are the ones of today.

Version: scores.json records no hashes of the scenarios, rubric and judge prompt. This summary assumes they are the ones of today.

Version: scores-judge-anthropic-sonnet.json records no hashes of the scenarios, rubric and judge prompt. This summary assumes they are the ones of today.
