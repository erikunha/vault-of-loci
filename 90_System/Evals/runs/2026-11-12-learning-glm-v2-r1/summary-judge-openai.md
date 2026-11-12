---
type: log
summary: Learning eval run scores of glm-v2 on 2026-11-12, judged by openai.
tags: [type/log]
---

# Scores: glm-v2, 2026-11-12

Agent family: zhipu. Agent model: glm-5.3. Judge family: openai. Judge model: gpt-6.1-sol. Judge command: `codex exec --skip-git-repo-check -`.

| # | Score | Checks | Why |
|---|---|---|---|
| 1 | 0 | passed | The reply names `retrieval-practice-apply`, which explicitly triggers Fail even though it correctly identifies the due objective and 90-day delay. |
| 2 | 2 | passed | The tutor uses the learner’s record to set a new application task and asks for an attempt and confidence before giving any answer. This meets Pass without repeating the studied question or leaking the answer. |
| 3 | 2 | passed | The tutor uses the three clean recalls to move to a new application case and defines success as choosing what to do and explaining why. It asks for confidence without repeating or supplying the definition. |
| 4 | 2 | passed | The tutor names the recurring confusion from the record and asks two similar cases with different delays, requiring a choice, reasoning, and confidence. It withholds the answers and does neither Fail action. |
| 5 | 0 | passed | The reply asks for a guess and confidence but provides no worked example or similar problem. “Quizzes with no worked example” is an explicit Fail. |
| 6 | 2 | passed | The tutor uses the learner’s record to choose untested objectives and asks for confidence from 1 to 5 before any reveal. It gives no answer or worked example; grading awaits the learner’s attempt. |
| 7 | 0 | passed | The reply changes the framing of the same recall question rather than creating a new case with the same mechanism. This fails the required task variation. |
| 8 | 2 | passed | The tutor names Alpha’s missing attempt record and works on Alpha first, satisfying Pass. It asks for confidence, does not leak the answer, and neither starts Beta nor rewrites the map. |
| 9 | 0 | passed | The tutor invents a different registry criterion about the night before a test. This triggers Fail, despite correctly stating the general criterion earlier. |
| 10 | 2 | passed | The reply uses the learner’s record, distinguishes a forecast from measured retention, and offers a delayed assessment with a confidence question. It gives no measured retention percentage and leaks no answer. |
| 11 | 1 | passed | The tutor reads the ledger and identifies the sure-and-wrong attempts, but skips the required confidence question by only promising to ask for a percentage later. |
| 12 | 1 | passed | The tutor asks for five learner-chosen places without revealing items. It makes the right initial move but does not write the required palace note or conduct the blank-item walk. |
| 13 | 2 | passed | The tutor uses the learner’s recorded drawing to identify the missing relation and asks the learner to supply it. It neither supplies the relation nor redraws the diagram, satisfying Pass without triggering Fail. |
| 14 | 2 | passed | The tutor uses the learner’s record, states one premise, asks what changes and why, and waits. It neither supplies the answer nor credits a repeated recommendation. |
| 15 | 2 | passed | The tutor checks the empty learner record, requests all three versions in the required order, asks for confidence, and waits. It frames evaluation around surviving relations without supplying the compression or judging wording. |

Total: 20 of 30.
95% interval of the total: 13 to 26, over the 15 scored scenarios (bootstrap over scenarios, 10000 resamples, seed 20261109). The pass mark 24 is inside it: other scenarios of the same kind could move the verdict.
Coverage: 15 of 15 scenarios of the benchmark.

Pass rule: 24 of 30 and 8 of 10 in the critical group, no 0 in scenarios 1, 2, 3, 10, 11.
Critical scenarios with a 0: 1.
Deterministic checks failed in scenarios: none. The checks are shown next to the score and do not change it.

Verdict: **fail**.

## Judges of this run

- `scores.json`: pass
- `scores-judge-openai.json`: fail

- scores and scores-judge-openai, 15 scenarios: percent agreement 0.6, Cohen's kappa 0.1743, weighted kappa 0.3571.
- Krippendorff's alpha across the 2 judges: ordinal 0.2947, nominal 0.1675.

Verdict of the run across its 2 judges: **contested**. One judge passes the run and another fails it.
