---
type: log
summary: Learning eval run scores of codex-v2 on 2026-11-12, judged by zhipu.
tags: [type/log]
---

# Scores: codex-v2, 2026-11-12

Agent family: openai. Agent model: gpt-6.1-sol. Judge family: zhipu. Judge model: glm-5.3. Judge command: `glm -p --setting-sources project,local --model opus`.

| # | Score | Checks | Why |
|---|---|---|---|
| 1 | 2 | passed | The reply names retrieval-practice-recall as due, states the 90-day horizon, and poses a new closed-book task with a confidence prompt, without leaking the recall percentages or naming apply as due. |
| 2 | 2 | passed | The reply draws on the ledger (two clean recalls, no application attempt), poses a new unseen application task built from the concept note, and demands an unaided attempt with a confidence rating before any answer — no leak, no repeated question, no vault writes. |
| 3 | 2 | passed | The reply uses the ledger's record (three clean recalls, no apply attempts) to skip re-quizzing the definition and instead poses a novel application task — planning study time for an unseen geography test — states what counts as applying it, asks for a confidence rating, and leaks nothing. |
| 4 | 2 | passed | The reply draws on the ledger (three misses on the one-week result) to target the learner's specific confusion, then drills it with two look-alike cases (test at 5 minutes vs. one week) asking which group wins and why, plus a 1–5 confidence rating — no answer leaked, no card repeated, no note-editing beyond incidental .pyc cache. |
| 5 | 2 | passed | The tutor checked the ledger and found it empty, then asked for a guess with a confidence rating before any explanation — exactly the Pass protocol's first step, with no leak, no premature concept explanation, and no unconfirmed attempt recorded (the worked example correctly waits for the learner's guess, so nothing in Fail applies). |
| 6 | 2 | passed | The reply uses the ledger (three clean recalls, no application attempt) to escalate to an application test, poses it without a worked example, and asks for a 1–5 confidence rating before any reveal — the Pass conditions — while never giving the answer or logging an attempt. |
| 7 | 2 | passed | The reply reads and cites the learner's ledger, then poses a variation of the missed task (flipping the group order in rp-r-01-v1) with the same mechanism, asks for a no-notes attempt including a 1–5 confidence rating, and neither repeats the original wording nor gives the answer. |
| 8 | 2 | passed | The reply uses the learner's record (ledger, notes, mistake log), names the gap — "no record for Alpha" and "Beta requires Alpha" — and works on Alpha first with a recall guess plus confidence question, without leaking Alpha's content or rewriting the map; the changed files are only __pycache__ artifacts, not vault writes. |
| 9 | 1 | passed | The reply uses the learner's record and asks a confidence question, but it never states the registry criterion ("Apply the idea in a new case and say why it applies") or says the task is built on it — the core of Pass — though it invents no other criterion and doesn't say any answer counts. |
| 10 | 2 | passed | The reply states exactly what the ledger shows, explicitly says retention at 30 days is unknown (a forecast, not a measurement — no percentage given), and offers the due delayed assessment with a confidence question, without leaking any content the learner must recall. |
| 11 | 2 | passed | The reply reads the ledger and matches it (85%/90% sure-and-wrong vs. 30% unsure-but-right), names the sure-and-wrong attempts, shows the gap, and asks for a 0–100% probability before the next check, with no leak, no unsupported calibration number, and no unconfirmed attempt recorded (the five-entries/four-graded-attempts distinction is stated, not contradicted). |
| 12 | 1 | passed | The reply checks the learner's record and asks for a recall guess with confidence without leaking anything or choosing places itself (nothing in Fail), but it never asks for the places of a route the learner knows or writes the palace note with Place, Item and Source, so it does not complete what Pass requires. |
| 13 | 1 | passed | The reply avoids every Fail item (no redraw, no leaking the missing relation, and it asks the confidence question), but it never does what Pass requires — it doesn't use the learner's record to name the relation the concept map holds and the drawing lacks, stalling on clarifying questions instead. |
| 14 | 1 | passed | The reply checks the learner's record, withholds the counterfactual, and asks for a one-line answer with confidence — but it never states a premise in one line as Pass requires, instead asking the learner to supply the concept and premise themselves. |
| 15 | 1 | passed | The reply checks the learner's record, names the compression-challenge exercise, asks the confidence question, and leaks nothing (no Fail clause). But it stops at "which idea?" plus a one-line explanation — it never asks for the full version, the analogy, and the shortest version in that order, so it doesn't do exactly what Pass says. |

Total: 25 of 30.
95% interval of the total: 21 to 28, over the 15 scored scenarios (bootstrap over scenarios, 10000 resamples, seed 20261109). The pass mark 24 is inside it: other scenarios of the same kind could move the verdict.
Coverage: 15 of 15 scenarios of the benchmark.

Pass rule: 24 of 30 and 8 of 10 in the critical group, no 0 in scenarios 1, 2, 3, 10, 11.
Critical scenarios with a 0: none.
Deterministic checks failed in scenarios: none. The checks are shown next to the score and do not change it.

Verdict: **pass**.

## Judges of this run

- `scores.json`: fail
- `scores-judge-zhipu-glm.json`: pass

- scores and scores-judge-zhipu-glm, 15 scenarios: percent agreement 0.8667, Cohen's kappa 0.7391, weighted kappa 0.5714.
- Krippendorff's alpha across the 2 judges: ordinal 0.7546, nominal 0.7445.

Verdict of the run across its 2 judges: **contested**. One judge passes the run and another fails it.
