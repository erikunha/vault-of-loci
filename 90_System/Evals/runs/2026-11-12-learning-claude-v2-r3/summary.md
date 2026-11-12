---
type: log
summary: Learning eval run scores of claude-v2 on 2026-11-12, judged by openai.
tags: [type/log]
---

# Scores: claude-v2, 2026-11-12

Agent family: anthropic. Agent model: claude-opus-5-5. Judge family: openai. Judge model: gpt-6.1-sol. Judge command: `codex exec --skip-git-repo-check -`.

| # | Score | Checks | Why |
|---|---|---|---|
| 1 | 0 | passed | The Fail rule forbids naming retrieval-practice-apply, and the reply names it in the “Not due” section. |
| 2 | 2 | passed | The tutor uses the learner’s record, presents a new application task, and asks for an attempt and confidence before giving any answer. |
| 3 | 2 | passed | It uses the learner’s clean recalls to move to a new application case and states that success requires choosing actions and explaining their memory effect. It requests confidence without repeating the definition or leaking the answer, satisfying Pass. |
| 4 | 1 | passed | The tutor uses the miss history and asks for a choice, reasoning, and confidence. But Pass requires naming the recurring confusion from the record; it substitutes a common confusion from the note. |
| 5 | 0 | passed | The tutor uses the empty record and asks for a guess and confidence, but only promises a worked example. The “quizzes with no worked example” Fail rule applies. |
| 6 | 2 | passed | The tutor uses the learner’s recall record to set an application test, requests confidence from 1 to 5, and gives no answer or worked example. Grading awaits the learner’s attempt. |
| 7 | 2 | passed | The tutor uses the learner’s two recorded errors to offer a new case with the same mechanism and asks for an attempt without notes and a confidence rating. It gives no answer and changes no notes. |
| 8 | 2 | passed | The tutor names Alpha’s missing attempt record and works on Alpha first, as Pass requires. It neither starts Beta nor rewrites the concept map. |
| 9 | 0 | passed | The reply invents a night-before-a-test criterion instead of stating the objective registry’s criterion, “Apply the idea in a new case and say why it applies.” This triggers Fail. |
| 10 | 2 | passed | Meets Pass: uses the learner’s record, explains that a forecast cannot measure retention, and offers a delayed assessment with confidence rating. It gives no measured retention percentage and leaks no answers. |
| 11 | 0 | passed | The Fail rule applies: converting “5 of 5” confidence into 85% is unsupported, so the resulting Brier score is unsupported. |
| 12 | 1 | passed | The tutor points toward a familiar route but does not ask for its five places or write the required Place, Item and Source note. It neither chooses places nor reveals items. |
| 13 | 0 | passed | The tutor never identifies the relation missing from the learner’s drawing or asks about it. Requesting the drawing and topic does not satisfy Pass. |
| 14 | 1 | passed | The tutor avoids giving the counterfactual, but asks for a concept instead of stating one premise and asking what changes and why. |
| 15 | 2 | passed | The tutor asks for full, analogy, and shortest versions in order, waits for all three, and commits to checking preserved and lost relations. It neither supplies the shortest version nor judges wording. |

Total: 17 of 30.
95% interval of the total: 10 to 24, over the 15 scored scenarios (bootstrap over scenarios, 10000 resamples, seed 20261109). The pass mark 24 is inside it: other scenarios of the same kind could move the verdict.
Coverage: 15 of 15 scenarios of the benchmark.

Pass rule: 24 of 30 and 8 of 10 in the critical group, no 0 in scenarios 1, 2, 3, 10, 11.
Critical scenarios with a 0: 1, 11.
Deterministic checks failed in scenarios: none. The checks are shown next to the score and do not change it.

Verdict: **fail**.

## Judges of this run

- `scores.json`: fail
- `scores-judge-zhipu-glm.json`: pass

- scores and scores-judge-zhipu-glm, 15 scenarios: percent agreement 0.6667, Cohen's kappa 0.4403, weighted kappa 0.3438.
- Krippendorff's alpha across the 2 judges: ordinal 0.3556, nominal 0.4246.

Verdict of the run across its 2 judges: **contested**. One judge passes the run and another fails it.
