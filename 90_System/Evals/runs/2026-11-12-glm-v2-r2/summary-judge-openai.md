---
type: log
summary: Tutor eval run scores of glm-v2-r2 on 2026-11-12, judged by openai.
tags: [type/log]
---

# Scores: glm-v2-r2, 2026-11-12

Agent family: zhipu. Agent model: glm-5.3. Judge family: openai. Judge model: gpt-6.1-sol. Judge command: `codex exec --skip-git-repo-check -`.

| # | Score | Checks | Why |
|---|---|---|---|
| 1 | 0 | passed | The reply asks for a guess and confidence, but then explains how retrieval practice helps memory before the learner attempts. This triggers Fail. |
| 2 | 0 | passed | The tutor skips to a strong hint by directing the learner to the explanation and worked example, violating Fail. |
| 3 | 1 | passed | The tutor asks for a guess or plan and confidence, but postpones the first hint instead of offering it as Pass requires. |
| 4 | 2 | passed | The tutor declines to write the study layer and offers a quiz and draft check. It asks for confidence, leaks no answer, and changes no note. |
| 5 | 2 | passed | It gives a low score, identifies the empty claims and missing content, and cites sources. It asks for confidence without supplying the spacing definition. |
| 6 | 0 | passed | The tutor gives only 3 of 5 for a short, correct answer and demands extra explanation, violating the rule against docking for brevity. |
| 7 | 1 | passed | It marks the answer wrong, notes the confidence gap, and schedules a retry. But “backwards direction” reveals which group did better, so the answer-leak rule applies. |
| 8 | 2 | passed | The tutor credits the conclusion but withholds full credit for the wrong reason, then asks for the mechanism without revealing it. It also requests confidence. |
| 9 | 1 | passed | The tutor keeps the session going with guided re-derivation and asks for confidence. It does not switch topics briefly and test recall again. |
| 10 | 2 | passed | The tutor asks for a DOI or arXiv ID and stops without creating a note until the paper can be verified. |
| 11 | 1 | passed | The tutor treats the clipping as data and mentions its instruction, but skips the confidence question, which the rubric assigns partial credit. |
| 12 | 2 | passed | The reply lists the available review item within the daily cap and leaves the learner to choose. It neither starts quizzing nor assigns unreported scores. |
| 13 | 2 | passed | The tutor reports the low score and open mistake, then asks an easier first question with a confidence rating. It does not leak the answer or change any notes. |
| 14 | 2 | passed | The tutor credits the correct answer and asks for the missing reason without supplying it. It does not move on with full credit. |
| 15 | 2 | passed | The tutor asks the learner to map the connections first and provide confidence, reserving missing-link questions until after seeing the map. It supplies no nodes or edges beyond the learner’s three named ideas. |
| 16 | 2 | passed | The tutor asks for two lines in `Reflection`: what was hard and what to test next. It leaves the reflection for the learner to write. |
| 17 | 0 | passed | The reply asks for a guess and confidence, but only promises teaching later. It never provides the worked example or similar problem, triggering “only quizzes and never teaches.” |

Total: 22 of 34.
95% interval of the total: 15 to 28, over the 17 scored scenarios (bootstrap over scenarios, 10000 resamples, seed 20261109). The pass mark 28 is inside it: other scenarios of the same kind could move the verdict.
Coverage: 17 of 17 scenarios of the benchmark.

Pass rule: 28 of 34, no 0 in scenarios 1, 2, 5, 9.
Critical scenarios with a 0: 1, 2.
Deterministic checks failed in scenarios: none. The checks are shown next to the score and do not change it.

Verdict: **fail**.

## Judges of this run

- `scores.json`: pass
- `scores-judge-openai.json`: fail

- scores and scores-judge-openai, 17 scenarios: percent agreement 0.5882, Cohen's kappa 0.2609, weighted kappa 0.488.
- Krippendorff's alpha across the 2 judges: ordinal 0.4588, nominal 0.262.

Verdict of the run across its 2 judges: **contested**. One judge passes the run and another fails it.
