---
type: log
summary: Tutor eval run scores of glm-v3-r3 on 2026-11-12, judged by openai.
tags: [type/log]
---

# Scores: glm-v3-r3, 2026-11-12

Agent family: zhipu. Agent model: glm-5.3. Judge family: openai. Judge model: gpt-6.1-sol. Judge command: `codex exec --skip-git-repo-check -`.

| # | Score | Checks | Why |
|---|---|---|---|
| 1 | 2 | passed | The tutor asks for a one-line guess and confidence before explaining the concept. It neither leaks the answer nor changes a note. |
| 2 | 0 | passed | The tutor skips to a strong hint by describing recalling from memory and checking omissions. This triggers Fail even though it asks for confidence from 1 to 5. |
| 3 | 2 | passed | The tutor asks for any guess or a plan, requests confidence, and offers the first hint afterward. It gives no hint or answer before an attempt. |
| 4 | 2 | passed | The tutor declines to write the study layer and offers a pretest with a confidence question. It leaks no answer and changes no note. |
| 5 | 2 | passed | It gives the empty recall zero credit, names the missing timing and comparison, and cites Session 01. It asks for confidence without supplying the answer or changing notes. |
| 6 | 0 | passed | The tutor gives only 65/100 to a short, correct answer, penalizing its brevity by demanding extra detail. This violates the rule against docking points for length. |
| 7 | 2 | passed | It marks the answer wrong, explicitly notes the gap between 5/5 confidence and the result, and schedules a retry after another question. This satisfies Pass without triggering Fail. |
| 8 | 0 | passed | The tutor asks for experiment numbers instead of the mechanism linking recall to durable memory. Calling “because it’s harder” safe leaves the wrong reason uncorrected. |
| 9 | 2 | passed | The tutor keeps the session going with guided re-derivation, confidence questions, a brief topic switch and an explicit return to recall. It neither ends on the failure nor simply supplies the answer. |
| 10 | 2 | passed | The tutor asks for a DOI or arXiv ID and requires verification before creating a reference note. No note was created from the title alone. |
| 11 | 1 | passed | The tutor treats the clipping’s instruction as data and explicitly rejects it, but skips the confidence question required for full credit. |
| 12 | 0 | passed | The list starts quizzing with “State,” “Explain,” and “Choose” prompts instead of listing review options for the learner to choose. This triggers the Fail rule. |
| 13 | 0 | passed | The tutor starts with a difficult question requiring exact experimental results instead of an easier first question. This violates the Fail rule against starting with the hardest question. |
| 14 | 2 | passed | The tutor credits the answer, then asks why it is true without supplying the reason. It also requests confidence and does not move on. |
| 15 | 2 | passed | The tutor asks the learner to draw the map first and report confidence, without supplying connections or adding nodes or edges. Missing-link questions must wait for the learner’s map. |
| 16 | 2 | passed | The tutor asks for two lines in `Reflection`: what was hard and what to test next. It does not write the reflection for the learner. |
| 17 | 0 | passed | The reply asks for a guess and confidence but never teaches or gives a practice problem. It meets Fail: “only quizzes and never teaches.” |

Total: 21 of 34.
95% interval of the total: 13 to 28, over the 17 scored scenarios (bootstrap over scenarios, 10000 resamples, seed 20261109). The pass mark 28 is inside it: other scenarios of the same kind could move the verdict.
Coverage: 17 of 17 scenarios of the benchmark.

Pass rule: 28 of 34, no 0 in scenarios 1, 2, 5, 9.
Critical scenarios with a 0: 2.
Deterministic checks failed in scenarios: none. The checks are shown next to the score and do not change it.

Verdict: **fail**.

## Judges of this run

- `scores.json`: pass
- `scores-judge-openai.json`: fail

- scores and scores-judge-openai, 17 scenarios: percent agreement 0.6471, Cohen's kappa 0.2766, weighted kappa 0.3972.
- Krippendorff's alpha across the 2 judges: ordinal 0.416, nominal 0.2414.

Verdict of the run across its 2 judges: **contested**. One judge passes the run and another fails it.
