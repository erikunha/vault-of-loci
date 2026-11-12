---
type: log
summary: Learning eval run scores of glm-v2 on 2026-11-12, judged by anthropic.
tags: [type/log]
---

# Scores: glm-v2, 2026-11-12

Agent family: zhipu. Agent model: glm-5.3. Judge family: anthropic. Judge model: claude-opus-5-5. Judge command: `claude -p --setting-sources project,local --model claude-opus-5-5`.

| # | Score | Checks | Why |
|---|---|---|---|
| 1 | 2 | passed | The reply names `retrieval-practice-recall` as the one objective due, gives the delay as 90 days and sets it as a new, closed-book task. It also asks for a confidence rating and does not give away the answer. Nothing in Fail applies: it says `retrieval-practice-apply` was already measured, gives no retention number without a new attempt, and wrote nothing to the vault. |
| 2 | 2 | passed | The reply uses the learner's record (two clean recalls, last one 100 days ago) and sets a new application task they have not seen, instead of repeating the recall question. It asks for an attempt and a confidence rating before giving any answer, and no vault files were changed. |
| 3 | 2 | passed | The tutor used the learner's record (three clean recalls, no apply attempt), so it skipped the definition and set an application task. The task is a new case, and the reply says what counts as applying the idea, asks for confidence and gives away no part of the answer, so it meets Pass and nothing in Fail. |
| 4 | 2 | passed | The reply uses the ledger (three wrong recalls, falling confidence), names the recurring confusion (immediate vs. delayed test), and drills it with two look-alike cases, asking who scores higher and why plus a confidence rating. It doesn't say which method wins, changed no files, and will log only after the learner confirms, so it meets Pass and nothing in Fail. |
| 5 | 2 | passed | It read the empty record, asked for a guess with a 1–5 confidence rating, and explained nothing before the attempt. That is the first step "Pass" asks for; nothing in "Fail" happened, nothing leaked, and no note was written. |
| 6 | 2 | passed | The reply uses the learner's record to pick untested objectives. It asks a recall question with no worked example and gives no answer, and it asks for confidence from 1 to 5 before any reveal. Nothing in Fail applies. |
| 7 | 1 | passed | Pass requires a new case with the same mechanism, but this only rewords the same 2006 experiment; the fill-in template also gives away part of the answer (the one-week delay and the two-group structure). It isn't a Fail, because the wording differs and the answer isn't given, and it does use the record and asks for confidence. |
| 8 | 2 | passed | The reply uses the record (the ledger has no Alpha attempt, and the map says Beta needs Alpha), names the gap, and starts on Alpha with a recall prompt and a confidence question. It doesn't leak the answer, start Beta, or change any files, so it meets Pass and nothing in Fail. |
| 9 | 0 | passed | The reply attributes a different criterion to the objective registry (`90_System/Objectives.json`), "choose what to do the night before a test in a new subject and say why", when the registry's criterion is "Apply the idea in a new case and say why it applies". That counts as inventing a different criterion, which the Fail rule names. |
| 10 | 1 | passed | The reply reports the ledger accurately and states no measured retention percentage, so nothing in Fail applies. It still falls short of Pass: it never clearly says a forecast is not a measurement, and the delayed check it offers is an untested "apply" task instead of the 30-day recall test it says is due, so it would not measure what the learner asked about. |
| 11 | 2 | passed | The reply reads the ledger, shows the gap between confidence and result, names both sure-and-wrong attempts, and commits to asking for a percent before the next question. Its Brier figure is consistent with the stated confidences, and it changed no notes, so it meets Pass and nothing in Fail. |
| 12 | 2 | passed | The reply asks the learner for five places on a route they know, one per step and in walking order, and it does not pick the places itself. Its examples ("rooms in your home or stops on your way to work") are only kinds of place. It does not read out any of the five steps. Holding off on the palace note fits this turn because the learner has not given any places yet. Nothing in "Fail" applies. |
| 13 | 2 | passed | The reply uses the learner's record, names only the missing relation between Alpha and Beta without saying what it is, asks a question about it plus the confidence question, and does not redraw the diagram, so it meets Pass and nothing in Fail. |
| 14 | 2 | passed | The reply checks the learner's record and states one premise in one line. It asks what changes and why, asks for a 1–5 confidence, and stops to wait without giving the counterfactual, so it meets Pass and nothing in Fail. |
| 15 | 2 | passed | The reply checks the learner's record, then asks for the full version, the analogy and the shortest version in that order, plus a confidence rating, and waits for all three. It does not write a compression itself, gives away no relations of Alpha and changes no notes, so the Pass rule holds and nothing in Fail applies. |

Total: 26 of 30.
95% interval of the total: 21 to 30, over the 15 scored scenarios (bootstrap over scenarios, 10000 resamples, seed 20261109). The pass mark 24 is inside it: other scenarios of the same kind could move the verdict.
Coverage: 15 of 15 scenarios of the benchmark.

Pass rule: 24 of 30 and 8 of 10 in the critical group, no 0 in scenarios 1, 2, 3, 10, 11.
Critical scenarios with a 0: none.
Deterministic checks failed in scenarios: none. The checks are shown next to the score and do not change it.

Verdict: **pass**.

## Judges of this run

- `scores.json`: pass
- `scores-judge-openai.json`: fail

- scores and scores-judge-openai, 15 scenarios: percent agreement 0.6, Cohen's kappa 0.1743, weighted kappa 0.3571.
- Krippendorff's alpha across the 2 judges: ordinal 0.2947, nominal 0.1675.

Verdict of the run across its 2 judges: **contested**. One judge passes the run and another fails it.
