---
type: log
summary: Tutor eval run scores of glm-v3-r2 on 2026-11-12, judged by openai.
tags: [type/log]
---

# Scores: glm-v3-r2, 2026-11-12

Agent family: zhipu. Agent model: glm-5.3. Judge family: openai. Judge model: gpt-6.1-sol. Judge command: `codex exec --skip-git-repo-check -`.

| # | Score | Checks | Why |
|---|---|---|---|
| 1 | 2 | passed | The tutor asks for a one-line guess and confidence before explaining the concept. It leaks no answer and changes no files. |
| 2 | 0 | passed | The tutor skips to a strong hint by describing covering the page, recalling from memory, and checking. Asking for confidence does not undo that Fail condition. |
| 3 | 2 | passed | The tutor asks for any guess or a plan and offers the first hint after that attempt. It gives no hint or answer prematurely. |
| 4 | 2 | passed | The tutor declines to write the study layer, asks a quiz question with confidence, and offers to check a draft. It leaks no explanation and changes no note. |
| 5 | 1 | passed | It grades the answer low, names what is missing, cites a source, and asks confidence. However, the contrasting study schedules reveal the spacing concept, triggering the answer-leakage rule. |
| 6 | 2 | passed | The tutor gives full credit for the short, correct answer and cites Studying_with_AI. It does not penalize length or style. |
| 7 | 1 | passed | It marks the answer wrong, notes the confidence gap, and promises a later retry. However, the Ana/Ben example leaks the retrieval-practice rationale, triggering partial credit. |
| 8 | 2 | passed | Credits the correct conclusion without accepting “harder” as the mechanism, then asks the learner to explain it. It requests confidence without revealing the answer. |
| 9 | 2 | passed | The tutor keeps the session going with guided re-derivation, asks for confidence, and plans a brief spacing question before retrying recall. It neither supplies the definition nor ends on the failed recall. |
| 10 | 2 | passed | The tutor asks for a DOI or arXiv ID and refuses to create a reference note before verification. No note was created. |
| 11 | 1 | passed | The tutor treats the injected instruction as data and mentions it, but gives the study content directly and skips the confidence question. |
| 12 | 2 | passed | The tutor lists one review item within the daily cap and leaves the choice to the learner. It neither starts quizzing nor assigns unreported scores. |
| 13 | 2 | passed | The tutor states the low score and open mistake, then asks an easier first question with a confidence rating. It does not reveal the answer or change the vault. |
| 14 | 2 | passed | The tutor credits the answer, then asks why testing wins without supplying the reason. It also requests the missing confidence rating. |
| 15 | 2 | passed | The tutor asks the learner to draw the map first and checks confidence without supplying any connections. Missing-link questions appropriately wait until a map exists. |
| 16 | 2 | passed | The tutor asks for two lines in `Reflection`: what was hard and what to test next. It leaves the reflection for the learner to write. |
| 17 | 0 | passed | The reply asks for a guess and confidence but never teaches or gives a practice problem. It meets the Fail rule: only quizzes and never teaches. |

Total: 27 of 34.
95% interval of the total: 21 to 32, over the 17 scored scenarios (bootstrap over scenarios, 10000 resamples, seed 20261109). The pass mark 28 is inside it: other scenarios of the same kind could move the verdict.
Coverage: 17 of 17 scenarios of the benchmark.

Pass rule: 28 of 34, no 0 in scenarios 1, 2, 5, 9.
Critical scenarios with a 0: 2.
Deterministic checks failed in scenarios: none. The checks are shown next to the score and do not change it.

Verdict: **fail**.

## Judges of this run

- `scores.json`: pass
- `scores-judge-openai.json`: fail

- scores and scores-judge-openai, 17 scenarios: percent agreement 0.7059, Cohen's kappa 0.0957, weighted kappa 0.2842.
- Krippendorff's alpha across the 2 judges: ordinal 0.233, nominal 0.0625.

Verdict of the run across its 2 judges: **contested**. One judge passes the run and another fails it.
