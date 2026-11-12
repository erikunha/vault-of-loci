---
type: log
summary: Learning eval run scores of claude-v2 on 2026-11-12, judged by openai.
tags: [type/log]
---

# Scores: claude-v2, 2026-11-12

Agent family: anthropic. Agent model: claude-opus-5-5. Judge family: openai. Judge model: gpt-6.1-sol. Judge command: `codex exec --skip-git-repo-check -`.

| # | Score | Checks | Why |
|---|---|---|---|
| 1 | 2 | passed | The reply names retrieval-practice-recall as due after 90 days and gives a new task with a confidence question. It correctly excludes retrieval-practice-apply and states no retention number. |
| 2 | 2 | passed | The tutor uses the learner’s record to set a new case and requests an attempt with confidence before giving any answer. The transcript shows neither repetition of the studied question nor an answer leak. |
| 3 | 2 | passed | The Pass rule is met: three clean recalls lead to a new application case, with success defined as choosing actions and justifying their effect. It asks for confidence without repeating the definition or leaking the answer. |
| 4 | 1 | passed | The tutor uses the record and offers two similar cases with confidence questions, but does not name the recurring confusion required by Pass. Neither Fail behavior occurs. |
| 5 | 0 | passed | The reply asks for a guess and confidence but only promises a worked example. The Fail rule applies: it quizzes with no worked example. |
| 6 | 2 | passed | The tutor uses the learner’s three clean recalls to choose an application test, provides no answer, and requests confidence from 1 to 5 before revealing anything. Grading awaits the learner’s response. |
| 7 | 2 | passed | The tutor uses the learner’s recorded misses to give a new case testing the same mechanism, asks for an attempt without notes and confidence, and gives no answer. |
| 8 | 2 | passed | The tutor names Alpha’s missing attempt record and works on Alpha first, as Pass requires. It neither starts Beta nor rewrites the concept map. |
| 9 | 0 | passed | The Fail rule applies because the tutor invents a different objective criterion instead of stating the registry’s “Apply the idea in a new case and say why it applies.” |
| 10 | 2 | passed | Meets Pass by citing the two clean recalls, distinguishing prediction from measurement, and offering a delayed assessment with confidence. It gives no measured retention percentage and leaks no answers. |
| 11 | 2 | passed | The tutor reads the ledger, identifies the two sure-and-wrong attempts, and shows the confidence-result gap with supported numbers. It asks for a percentage with the next answer before any reveal. |
| 12 | 1 | passed | The tutor correctly leaves route selection to the learner and reveals no items. It does not complete Pass: no palace note with Place, Item and Source is written, and no blank-item walk begins. |
| 13 | 0 | passed | The tutor never identifies the relation missing from the learner’s drawing or asks about that relation, so it does not perform the required comparison. |
| 14 | 1 | passed | The tutor checks the learner’s record and waits without leaking the answer, but does not state one premise or ask what changes and why, as Pass requires. |
| 15 | 2 | passed | The tutor uses the learner’s record, requests full, analogy, then shortest, and waits for all three before checking surviving relations. It asks for confidence and neither supplies the compression nor judges wording. |

Total: 21 of 30.
95% interval of the total: 15 to 27, over the 15 scored scenarios (bootstrap over scenarios, 10000 resamples, seed 20261109). The pass mark 24 is inside it: other scenarios of the same kind could move the verdict.
Coverage: 15 of 15 scenarios of the benchmark.

Pass rule: 24 of 30 and 8 of 10 in the critical group, no 0 in scenarios 1, 2, 3, 10, 11.
Critical scenarios with a 0: none.
Deterministic checks failed in scenarios: none. The checks are shown next to the score and do not change it.

Verdict: **fail**.

## Judges of this run

- `scores.json`: fail
- `scores-judge-zhipu-glm.json`: pass

- scores and scores-judge-zhipu-glm, 15 scenarios: percent agreement 0.6667, Cohen's kappa 0.2647, weighted kappa 0.2466.
- Krippendorff's alpha across the 2 judges: ordinal 0.289, nominal 0.2408.

Verdict of the run across its 2 judges: **contested**. One judge passes the run and another fails it.
