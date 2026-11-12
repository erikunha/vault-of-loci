---
type: log
summary: Learning eval run scores of glm-v2 on 2026-11-12, judged by openai.
tags: [type/log]
---

# Scores: glm-v2, 2026-11-12

Agent family: zhipu. Agent model: glm-5.3. Judge family: openai. Judge model: gpt-6.1-sol. Judge command: `codex exec --skip-git-repo-check -`.

| # | Score | Checks | Why |
|---|---|---|---|
| 1 | 0 | passed | The Fail rule applies because the reply names retrieval-practice-apply as due even though it was already measured. It also misses the required 90-day delay for retrieval-practice-recall. |
| 2 | 2 | passed | The tutor uses the learner’s recall record to give a new application task and asks for an attempt and confidence before any answer. This meets Pass without repeating the studied question or leaking the answer. |
| 3 | 0 | passed | Pass requires applying the idea to an unseen case. The tutor instead asks about an experiment’s results; describing a future application task does not satisfy that requirement. |
| 4 | 2 | passed | It uses the three wrong recalls to drill retrieval practice versus rereading with two similar items, asking which applies, why, and confidence. It neither repeats the card nor recommends more reading. |
| 5 | 0 | passed | The tutor asks for a guess and confidence but provides no worked example or similar problem. This meets the Fail rule for quizzing with no worked example. |
| 6 | 2 | passed | The tutor uses the recall record to select an application test, requests confidence from 1 to 5, and gives no answer or worked example. It sets source-based grading criteria; grading awaits the learner’s attempt. |
| 7 | 2 | passed | The tutor uses the learner’s record, presents a new case testing the same mechanism, and asks for recall without notes plus confidence. It neither repeats the question verbatim nor gives the answer. |
| 8 | 2 | passed | The tutor names Alpha as missing from the learner’s record and works on Alpha first. It neither starts Beta nor rewrites the concept map. |
| 9 | 0 | passed | The Fail rule applies: the tutor invents a night-before-a-test criterion and attributes it to the registry instead of stating the actual criterion. |
| 10 | 1 | FAILED: a reply contains '61%' (turn 2); a reply contains '40%' (turn 2) | The tutor uses the record, distinguishes a forecast from measurement, and offers a delayed assessment with confidence. But it leaks the exact numbers the learner must recall, which scores 1. |
| 11 | 2 | FAILED: a reply contains '40%' (turn 2) | Meets Pass: reads the ledger, shows the confidence-result gap, names both sure-and-wrong attempts, and requests a percentage before the next reveal. No Fail condition is shown. |
| 12 | 1 | passed | The tutor leaves place selection to the learner and reveals no items, but does not request one familiar place per item or write the required Place, Item, and Source note. |
| 13 | 2 | passed | The tutor uses the learner’s drawing, identifies only the missing relation, and asks about its direction and purpose. It neither supplies the relation nor redraws the diagram. |
| 14 | 1 | passed | The tutor moves toward a counterfactual exercise but never states a premise or asks what changes and why. It leaks no counterfactual and accepts no repetition. |
| 15 | 2 | passed | The tutor checks the learner’s record, requests all three versions in order, and waits. It asks for confidence and focuses on preserving relations without supplying the shortest version. |

Total: 19 of 30.
95% interval of the total: 12 to 25, over the 15 scored scenarios (bootstrap over scenarios, 10000 resamples, seed 20261109). The pass mark 24 is inside it: other scenarios of the same kind could move the verdict.
Coverage: 15 of 15 scenarios of the benchmark.

Pass rule: 24 of 30 and 8 of 10 in the critical group, no 0 in scenarios 1, 2, 3, 10, 11.
Critical scenarios with a 0: 1, 3.
Deterministic checks failed in scenarios: 10, 11. The checks are shown next to the score and do not change it.

Verdict: **fail**.

## Judges of this run

- `scores.json`: fail
- `scores-judge-openai.json`: fail

- scores and scores-judge-openai, 15 scenarios: percent agreement 0.8, Cohen's kappa 0.6739, weighted kappa 0.6809.
- Krippendorff's alpha across the 2 judges: ordinal 0.7102, nominal 0.6801.

Verdict of the run across its 2 judges: **fail**.
