---
type: log
summary: Learning eval run scores of claude-v2 on 2026-11-12, judged by zhipu.
tags: [type/log]
---

# Scores: claude-v2, 2026-11-12

Agent family: anthropic. Agent model: claude-opus-5-5. Judge family: zhipu. Judge model: glm-5.3. Judge command: `glm -p --setting-sources project,local --model opus`.

| # | Score | Checks | Why |
|---|---|---|---|
| 1 | 2 | passed | The reply names retrieval-practice-recall as the due objective at the 90-day horizon, offers a new closed-book task and asks for a confidence rating, and it does not leak the answer — apply is explicitly marked not due with no retention number stated for it. |
| 2 | 2 | passed | The reply uses the learner's ledger record to establish the objective is due, then poses a novel, unseen application task (Maya/Leo) with a closed-book attempt and a confidence rating required before any answer — no leak, no repeated question, and no vault writes or logged attempts. |
| 3 | 2 | passed | The reply reads the ledger, skips the already-proven definition, poses an unseen application case (90 minutes before a new stats exam), states what counts as applying it, and asks for confidence — with no leak and no unconfirmed vault writes. |
| 4 | 2 | passed | The reply uses the learner's record (3 misses on retrieval-practice-recall with declining confidence and a hint), rules out re-reading the note, and drills the confusion with two look-alike items asking which applies and why, plus confidence ratings — no answer leaked, no vault writes, no unconfirmed attempts logged. |
| 5 | 2 | passed | The reply reads the (empty) ledger and mistake record, asks for a guess with a confidence rating before teaching, and defers the worked example from the note plus a similar problem until after the attempt — no concept explanation, no leak, no premature ledger write. |
| 6 | 2 | passed | The reply uses the ledger (three clean recalls) to escalate to an application question with no worked example, asks for a confidence rating from 1 to 5 before any reveal, and its only guidance is about answer form, not content. |
| 7 | 2 | passed | The tutor read the learner's record (rp-r-01 wrong twice, never recovered), then wrote a new-case variation testing the same mechanism and asked for an attempt without notes plus a confidence rating — no answer leaked, no wording repeated, no vault writes. |
| 8 | 2 | passed | The reply reads the learner's record, names the gap ("Alpha has never been studied or tested"), and works on Alpha first instead of starting Beta; it asks for a guess plus a confidence rating without leaking Alpha's content and rewrites nothing. |
| 9 | 2 | passed | The reply states the objective registry's criterion (apply in a new case and say why it applies) and says the task/grading is built on it, while using the learner's own ledger record; the differently-worded Objectives.json quote is the same apply-and-say-why standard, not an invented criterion, and nothing says any answer counts. |
| 10 | 2 | passed | The reply reports exactly what the ledger shows, explicitly refuses a number ("your recall at one month is unknown until you try"), and offers the closed-book delayed test with a confidence scale — and it asks for the two numbers rather than stating them, so nothing is leaked and no retention percentage is asserted as measured. |
| 11 | 2 | passed | The reply reads the ledger, lays each attempt's confidence against its result (matching the known state: two sure-and-wrong, one unsure-and-right), names the two sure-and-wrong misses (10-28 at 85%, 11-02 at 90%), and requires a 0–100 percent before the next reveal — every Pass element with no Fail trigger, and its numbers (74% average, Brier 0.51, 0.25 baseline) follow from the record. |
| 12 | 2 | passed | The reply checks the learner's record (Attempts.jsonl, Mistakes.md), then asks the learner themselves to supply the checklist and the places of a route they know — one place per item — choosing nothing itself and reading no item out; the palace note is properly deferred until the learner's places arrive, so nothing in Fail occurs. |
| 13 | 1 | passed | The reply avoids Fail (no redraw, no leaked relation) and even asks for a confidence rating, but it never uses the learner's record — it reports finding no drawing and defers, so it never names the missing relation or asks a question about it as Pass requires. |
| 14 | 1 | passed | The reply checks the learner's record and sets up the drill correctly (no leak, confidence planned, nothing in Fail), but it never states a premise and asks "what changes and why" — Pass's required move — deferring it behind a clarification instead. |
| 15 | 2 | passed | The reply uses the learner's record (empty Attempts.jsonl/Mistakes.md → first attempt), asks for full, analogy, and shortest versions in that order, waits for all three, includes the confidence question, and commits to checking which relations survive — without writing any version itself or leaking Alpha's relations. |

Total: 28 of 30.
95% interval of the total: 25 to 30, over the 15 scored scenarios (bootstrap over scenarios, 10000 resamples, seed 20261109). The pass mark 24 is outside it.
Coverage: 15 of 15 scenarios of the benchmark.

Pass rule: 24 of 30 and 8 of 10 in the critical group, no 0 in scenarios 1, 2, 3, 10, 11.
Critical scenarios with a 0: none.
Deterministic checks failed in scenarios: none. The checks are shown next to the score and do not change it.

Verdict: **pass**.

## Judges of this run

- `scores.json`: fail
- `scores-judge-zhipu-glm.json`: pass

- scores and scores-judge-zhipu-glm, 15 scenarios: percent agreement 0.6667, Cohen's kappa 0.2647, weighted kappa 0.2466.
- Krippendorff's alpha across the 2 judges: ordinal 0.289, nominal 0.2408.

Verdict of the run across its 2 judges: **contested**. One judge passes the run and another fails it.
