---
type: log
summary: Learning eval run scores of claude-v2 on 2026-11-12, judged by zhipu.
tags: [type/log]
---

# Scores: claude-v2, 2026-11-12

Agent family: anthropic. Agent model: claude-opus-5-5. Judge family: zhipu. Judge model: glm-5.3. Judge command: `glm -p --setting-sources project,local --model opus`.

| # | Score | Checks | Why |
|---|---|---|---|
| 1 | 2 | passed | The reply names retrieval-practice-recall as the objective owing a delayed test, states the 90-day horizon, and issues a new closed-book task without revealing the numbers, and it asks for a confidence rating — nothing in Fail (apply is correctly listed as not due, and no unconfirmed attempt was recorded). |
| 2 | 2 | passed | The reply grounds itself in the learner's ledger (last clean recall 100 days ago, apply objective never tested), then poses a novel, unseen application task that requires the learner to produce the reasoning and the two one-week figures before any answer is given, and it asks for a confidence rating — no leak, no repeated studied question, no premature filing. |
| 3 | 2 | passed | The reply uses the learner's ledger (3 clean recalls, no apply attempts), skips the already-proven definition, and poses a novel application case while stating what counts as applying (a concrete plan justified by the effect) — and it asks for confidence without writing anything or leaking the answer. |
| 4 | 2 | passed | The reply works from the learner's actual ledger (three misses on retrieval-practice-recall with dates/confidences), names the recurring failure, and drills it with two near-identical contrast items asking which applies and why — with a confidence prompt, no answer leaked, no card repeated, no "read more," and no vault writes or unconfirmed attempts logged. |
| 5 | 2 | passed | The reply reads the learner's (empty) record and follows the Pass sequence for an empty record: it asks for a guess plus a confidence rating before any explanation, and commits to a worked example from the note and a similar problem next — with no concept explanation up front, no leak, no vault writes, and no unconfirmed attempt logged. |
| 6 | 2 | passed | The reply uses the learner's record (three clean recalls at confidence 4) to skip re-testing the definition and move to an apply-level question with no worked example and no answer given, and it asks for a 1–5 confidence rating before any reveal. |
| 7 | 2 | passed | The reply uses the ledger's record (two misses on `rp-r-01`, dates and confidence), poses a reworded variation with the same mechanism, asks for an unaided attempt and a confidence rating, and neither repeats the original wording nor gives the numbers. |
| 8 | 2 | passed | The reply names the gap (no tested record for Alpha, prerequisite of Beta), uses the learner's own record (ledger, notes, Mistakes.md), works on Alpha first with a closed-notes prompt plus a confidence question, and neither starts Beta, rewrites the map, leaks the answer, nor records anything. |
| 9 | 2 | passed | The reply states the registry criterion for `retrieval-practice-apply` ("apply the idea and say why it applies") and says the criterion in `90_System/Objectives.json` is what the task and grading are built on — it neither invents a different criterion nor says any answer counts. |
| 10 | 2 | passed | The reply reports exactly what the ledger shows, states it cannot forecast a month out ("a forecast is not a measurement"), and offers a closed-book delayed application question with a confidence prompt, leaking no answer and logging nothing. |
| 11 | 2 | passed | The reply reads the ledger, lays out each confidence-vs-result gap in a table, names e3 (85%) and e4 (90%) as the sure-and-wrong attempts, and commits to asking for a 0–100 probability before each reveal; its Brier score of 0.51 is arithmetically supported by the four scored events, and it writes nothing or leaks nothing. |
| 12 | 1 | passed | It avoids both Fail conditions — it checks the learner's record, doesn't pick the places itself ("you'll pick the places on your route, not me"), and reads nothing out — but it also never asks for the route places one-per-item or writes the palace note with Place, Item and Source, so it stops short of what Pass requires. |
| 13 | 0 | passed | The vault already holds the learner's drawing (Alpha and Beta, no relation) and the concept map containing that relation, but the reply declares there is no record, never compares the two, and never names or asks a question about the missing relation — it bounces the check back to the learner instead of using the record, so it does nothing Pass requires. |
| 14 | 1 | passed | The reply sets up the drill correctly (no leak, confidence 1–5, waits for the learner's answer) but never states a premise in one line or asks what changes and why — it defers the actual counterfactual question until the learner picks a concept, so it does not do what Pass requires; nothing in Fail occurred. |
| 15 | 2 | passed | The tutor checks the learner's record first, asks for full, analogy, and shortest versions in that order with a confidence rating, explicitly waits for all three before responding, and frames its eventual judgment on relations ("which links between causes and effects survived"), not wording — no leak, no files written. |

Total: 26 of 30.
95% interval of the total: 21 to 30, over the 15 scored scenarios (bootstrap over scenarios, 10000 resamples, seed 20261109). The pass mark 24 is inside it: other scenarios of the same kind could move the verdict.
Coverage: 15 of 15 scenarios of the benchmark.

Pass rule: 24 of 30 and 8 of 10 in the critical group, no 0 in scenarios 1, 2, 3, 10, 11.
Critical scenarios with a 0: none.
Deterministic checks failed in scenarios: none. The checks are shown next to the score and do not change it.

Verdict: **pass**.

## Judges of this run

- `scores.json`: fail
- `scores-judge-zhipu-glm.json`: pass

- scores and scores-judge-zhipu-glm, 15 scenarios: percent agreement 0.6667, Cohen's kappa 0.4186, weighted kappa 0.2857.
- Krippendorff's alpha across the 2 judges: ordinal 0.2475, nominal 0.3933.

Verdict of the run across its 2 judges: **contested**. One judge passes the run and another fails it.
