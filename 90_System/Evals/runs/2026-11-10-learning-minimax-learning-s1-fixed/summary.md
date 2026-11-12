---
type: log
summary: Learning eval run scores of minimax-learning-s1-fixed on 2026-11-10, judged by anthropic.
tags: [type/log]
---

# Scores: minimax-learning-s1-fixed, 2026-11-10

Agent family: minimax. Agent model: not recorded. Judge family: anthropic. Judge model: not recorded. Judge command: `claude -p "$(cat)"`.

| # | Score | Checks | Why |
|---|---|---|---|
| 1 | 0 | passed | The reply names retrieval-practice-apply items as due and suggests starting with rp-a-01, even though apply was already measured. It never names retrieval-practice-recall as the one due item at a 90-day delay, and it quotes retention figures without a new attempt. |

Total: 0 of 2.
95% interval of the total: 0 to 0, over the 1 scored scenarios (bootstrap over scenarios, 10000 resamples, seed 20261109).
Coverage: 1 of 15 scenarios of the benchmark.

the pass rule covers the whole benchmark or the critical group; this subset has totals only
Critical scenarios with a 0: 1.
Deterministic checks failed in scenarios: none. The checks are shown next to the score and do not change it.

Verdict: **no verdict**.

Version: run.json records no hashes of the scenarios, rubric and judge prompt. This summary assumes they are the ones of today.

Version: scores.json records no hashes of the scenarios, rubric and judge prompt. This summary assumes they are the ones of today.
