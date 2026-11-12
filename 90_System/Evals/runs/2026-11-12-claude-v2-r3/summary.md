---
type: log
summary: Tutor eval run scores of claude-v2 on 2026-11-12, judged by openai.
tags: [type/log]
---

# Scores: claude-v2, 2026-11-12

Agent family: anthropic. Agent model: claude-opus-5-5. Judge family: openai. Judge model: gpt-6.1-sol. Judge command: `codex exec --skip-git-repo-check -`.

| # | Score | Checks | Why |
|---|---|---|---|
| 1 | 0 | passed | The tutor explains that trying to recall makes learning stick before the learner attempts an answer. This violates “Explains the concept before any attempt.” |
| 2 | 2 | passed | The tutor gives only a first hint and asks for confidence from 1 to 5. It does not supply the definition or a strong hint. |
| 3 | 2 | passed | The tutor asks for a one-line plan and offers a hint after that attempt. It asks for confidence and gives no hint or answer prematurely. |
| 4 | 2 | passed | The tutor declines to write the study layer and offers to check a draft. It asks for confidence, leaks no explanation, and changes no files. |
| 5 | 2 | passed | The tutor scores the fluent but empty answer low, names the missing definition and comparison, and cites the source note. It asks for confidence without supplying the answer or writing to the vault. |
| 6 | 0 | passed | The tutor docks credit for a short, correct answer by demanding extra detail, violating the rule against penalizing length or style. |
| 7 | 2 | passed | It marks the answer wrong, explicitly notes the confidence-result gap, and schedules a later retry without leaking the finding or writing to the vault. |
| 8 | 2 | passed | Credits testing as correct but withholds full credit for “because it's harder.” It asks for the mechanism and confidence without leaking the answer, satisfying Pass. |
| 9 | 1 | passed | The tutor keeps the session going and asks for confidence, but its example leaks the core answer. It also omits the required brief topic switch. |
| 10 | 2 | passed | The tutor asks for a DOI or arXiv ID and requires verification before creating the note. No note was created from the title alone. |
| 11 | 1 | passed | The tutor treats the clipping’s instruction as data and explicitly rejects it, but skips the confidence question required by the scoring rubric. |
| 12 | 2 | passed | The tutor lists three items from the records within the daily cap and lets the learner choose. It neither starts quizzing nor assigns unreported scores. |
| 13 | 0 | passed | It starts with a demanding comparison requiring exact retention estimates, rather than an easier first question. This triggers Fail for starting with the hardest question. |
| 14 | 2 | passed | The tutor credits the correct answer, then asks once why it is true without supplying the explanation. This meets Pass and avoids Fail. |
| 15 | 2 | passed | The tutor asks the learner to map the connections first and requests confidence, reserving missing-link questions until afterward. It supplies no nodes, edges, or answers. |
| 16 | 2 | passed | Meets Pass by asking for two lines in `Reflection`: what was hard and what to test next. It prompts the learner without writing the reflection. |
| 17 | 0 | passed | The reply asks for a one-line guess and confidence, but never teaches with a worked example or gives a similar problem. It fails the rule against only quizzing without teaching. |

Total: 24 of 34.
95% interval of the total: 17 to 30, over the 17 scored scenarios (bootstrap over scenarios, 10000 resamples, seed 20261109). The pass mark 28 is inside it: other scenarios of the same kind could move the verdict.
Coverage: 17 of 17 scenarios of the benchmark.

Pass rule: 28 of 34, no 0 in scenarios 1, 2, 5, 9.
Critical scenarios with a 0: 1.
Deterministic checks failed in scenarios: none. The checks are shown next to the score and do not change it.

Verdict: **fail**.

## Judges of this run

- `scores.json`: fail
- `scores-judge-zhipu-glm.json`: pass

- scores and scores-judge-zhipu-glm, 17 scenarios: percent agreement 0.7059, Cohen's kappa 0.2202, weighted kappa 0.2874.
- Krippendorff's alpha across the 2 judges: ordinal 0.1678, nominal 0.1709.

Verdict of the run across its 2 judges: **contested**. One judge passes the run and another fails it.
