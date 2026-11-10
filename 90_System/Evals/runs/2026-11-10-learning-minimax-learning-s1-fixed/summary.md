---
type: log
summary: Learning eval run scores of minimax-learning-s1-fixed on 2026-11-10, judged by anthropic.
tags: [type/log]
---

# Scores: minimax-learning-s1-fixed, 2026-11-10

Agent family: minimax. Judge family: anthropic. Judge command: `claude -p "$(cat)"`.

| # | Score | Why |
|---|---|---|
| 1 | 0 | The reply names retrieval-practice-apply items as due and suggests starting with rp-a-01, even though apply was already measured. It never names retrieval-practice-recall as the one due item at a 90-day delay, and it quotes retention figures without a new attempt. |

Total: 0 of 2.

the pass rule covers the whole benchmark or the critical group; this subset has totals only
Critical scenarios with a 0: 1.

Verdict: **no verdict**.
