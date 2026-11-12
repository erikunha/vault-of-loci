---
type: log
summary: Learning eval run scores of claude-v2 on 2026-11-12, judged by openai.
tags: [type/log]
---

# Scores: claude-v2, 2026-11-12

Agent family: anthropic. Agent model: claude-opus-5-5. Judge family: openai. Judge model: gpt-6.1-sol. Judge command: `codex exec --skip-git-repo-check -`.

| # | Score | Checks | Why |
|---|---|---|---|
| 1 | 0 | passed | The Fail rule applies because the reply names retrieval-practice-apply, even though it labels it “Not due.” |
| 2 | 2 | passed | The tutor uses the learner’s record to set a new application task and requests an attempt and confidence before giving any answer, satisfying Pass. |
| 3 | 2 | passed | The tutor uses the three clean recalls to move to a new application case and defines what counts as applying it. It asks for confidence without repeating or revealing the definition. |
| 4 | 1 | passed | The tutor uses the record and asks for a contrast with reasons and confidence, but does not name the recurring confusion required by Pass. Neither Fail condition occurs. |
| 5 | 0 | passed | The tutor asks for a guess and confidence but only promises a worked example. The Fail rule applies because it quizzes with no worked example. |
| 6 | 2 | passed | The tutor uses the learner’s recall record to choose an application test, gives no answer or worked example, and asks for confidence from 1 to 5. Source-based grading awaits the learner’s attempt. |
| 7 | 2 | passed | The tutor uses the recorded misses to offer a new case testing the same mechanism and requests recall without notes plus confidence. It gives no answer and changes no files. |
| 8 | 2 | passed | The tutor names Alpha’s missing attempt record and works on Alpha first, satisfying Pass. It asks for confidence without leaking content, starting Beta, or rewriting the concept map. |
| 9 | 0 | passed | The tutor invents a registry criterion about choosing what to do the night before a test. This triggers Fail: inventing a different criterion. |
| 10 | 2 | passed | Meets Pass by citing the two clean recalls and 40-day gap, distinguishing a forecast from measurement, and offering a delayed assessment with confidence. It gives no retention percentage and leaks no answer. |
| 11 | 1 | passed | The tutor uses the ledger and names the sure-and-wrong attempts, but only promises to ask for a percentage later. Skipping the actual confidence question earns 1. |
| 12 | 1 | passed | The tutor leaves route selection to the learner and reveals no items, but does not ask for one familiar place per item or create the required Place, Item and Source note. |
| 13 | 0 | passed | The tutor does not identify the relation missing from the drawing or ask about it, as Pass requires. It asks for information instead of comparing the learner’s drawing with the source. |
| 14 | 1 | passed | The tutor waits without revealing the counterfactual, but asks for a concept instead of stating one premise and asking what changes and why. |
| 15 | 2 | passed | The tutor requests full, analogy, and shortest versions in order, asks for confidence, and waits for all three before checking surviving relations. It neither supplies the shortest version nor judges wording. |

Total: 18 of 30.
95% interval of the total: 11 to 24, over the 15 scored scenarios (bootstrap over scenarios, 10000 resamples, seed 20261109). The pass mark 24 is inside it: other scenarios of the same kind could move the verdict.
Coverage: 15 of 15 scenarios of the benchmark.

Pass rule: 24 of 30 and 8 of 10 in the critical group, no 0 in scenarios 1, 2, 3, 10, 11.
Critical scenarios with a 0: 1.
Deterministic checks failed in scenarios: none. The checks are shown next to the score and do not change it.

Verdict: **fail**.

## Judges of this run

- `scores.json`: fail
- `scores-judge-zhipu-glm.json`: pass

- scores and scores-judge-zhipu-glm, 15 scenarios: percent agreement 0.6667, Cohen's kappa 0.4186, weighted kappa 0.2857.
- Krippendorff's alpha across the 2 judges: ordinal 0.2475, nominal 0.3933.

Verdict of the run across its 2 judges: **contested**. One judge passes the run and another fails it.
