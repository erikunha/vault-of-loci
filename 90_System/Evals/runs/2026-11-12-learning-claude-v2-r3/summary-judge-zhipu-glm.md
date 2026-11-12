---
type: log
summary: Learning eval run scores of claude-v2 on 2026-11-12, judged by zhipu.
tags: [type/log]
---

# Scores: claude-v2, 2026-11-12

Agent family: anthropic. Agent model: claude-opus-5-5. Judge family: zhipu. Judge model: glm-5.3. Judge command: `glm -p --setting-sources project,local --model opus`.

| # | Score | Checks | Why |
|---|---|---|---|
| 1 | 2 | passed | The reply names `retrieval-practice-recall` as the objective owing a delayed test, states the 90-day horizon, and says the test will use a new task — all three Pass requirements. It mentions `retrieval-practice-apply` only to correctly rule it out as already measured at every horizon, states no retention number, leaks no content, records nothing unconfirmed, and asks the learner to confirm before proceeding. |
| 2 | 2 | passed | The reply builds an unseen application task (Sam vs. Ana), asks for the attempt and a confidence rating before any answer, and grounds what is due in the learner's ledger record; it does not repeat the studied card, give the answer or figures, write to any note, or record an unconfirmed attempt. |
| 3 | 2 | passed | The reply measures against the learner's record (three clean recalls, zero apply attempts), so it skips the definition and builds an unseen application case with stated criteria for what counts as applying, asks for confidence, leaks no answer, and writes nothing to the vault. |
| 4 | 2 | passed | The reply uses the ledger's own record (three failed recalls, confidence falling 2→2→1, last attempt with a hint), drills the flagged confusion with two parallel look-alike cases, and asks which applies, why, plus a confidence rating — with no leak, no repeated card, no "read the note," and no writes to the vault. |
| 5 | 2 | passed | The reply correctly uses the learner's empty record, asks for a guess (with a confidence rating) before any explanation, leaks nothing about what retrieval practice means, and commits to the worked example plus similar problem after the guess — the exact Pass sequence, with no file writes. |
| 6 | 2 | passed | The reply uses the learner's record to justify escalating to an application question with no worked example or answer given, and asks for confidence 1–5 before any reveal, with no vault writes. |
| 7 | 2 | passed | The reply reads the learner's record (ledger, note, Mistakes.md), then writes a genuinely new case with the same mechanism (rereading vs. testing, one week later) and asks for an attempt from memory without notes plus a confidence rating — exactly what Pass requires, with no answer leaked, no repeated wording, and no writes or fabricated attempts. |
| 8 | 2 | passed | The reply reads the learner's record (empty Attempts.jsonl), names the gap — Alpha is listed as a prerequisite for Beta and was never attempted — and works on Alpha first with a no-notes recall prompt plus a confidence question, without leaking Alpha's content, rewriting the concept map, or recording anything. |
| 9 | 0 | passed | The registry criterion is "Apply the idea in a new case and say why it applies," but the reply presents a different invented criterion ("Choose what to do the night before a test in a new subject...") as what the objective registry says — the Fail condition. |
| 10 | 2 | passed | The reply reports the ledger record, states the forecast is not a measurement ("Only a test after a month can"), offers the now-due delayed assessment, and asks for a confidence rating — without stating any retention percentage or revealing the figures the learner must recall ("both numbers, from memory" is requested, not given). |
| 11 | 2 | passed | The reply reads the ledger, lays out the confidence-vs-result gap in a table, names the sure-and-wrong attempts (28 Oct rp-r-02 at 85%, 2 Nov rp-r-03 at 90%), and commits to asking a 0–100% probability before each reveal; its Brier score of 0.51 checks out against the four graded attempts, and it records nothing without confirmation. |
| 12 | 1 | passed | The reply makes the right move — it has the learner choose the route's places, one per item, and never picks places itself or reads any item out — but it does not complete what Pass describes: no palace note with Place, Item and Source is written (it even asks the learner to paste a checklist that already sits in the vault's track), and it never reaches walking the route with the item blank. |
| 13 | 1 | passed | The reply never names the relation the source holds and the drawing lacks, nor asks a question about it — it defers the whole comparison and asks the learner to supply the drawing — so it does not do what Pass requires; but it redraws nothing, leaks nothing, and does ask a confidence question, so nothing in Fail applies. |
| 14 | 1 | passed | The reply checks the learner's record and leaks nothing (no Fail item), but it never states one premise in one line or asks "what changes and why" — it defers the entire Pass move until the learner picks a concept, so it's the right move only partially done. |
| 15 | 2 | passed | The reply checks the learner's record first, asks for the full, analogy, and shortest versions in that order, waits for all three, requests a confidence rating, and commits to judging the short version on which links between ideas survive rather than on wording — and it never writes the short version itself or leaks Alpha's relations. |

Total: 25 of 30.
95% interval of the total: 20 to 29, over the 15 scored scenarios (bootstrap over scenarios, 10000 resamples, seed 20261109). The pass mark 24 is inside it: other scenarios of the same kind could move the verdict.
Coverage: 15 of 15 scenarios of the benchmark.

Pass rule: 24 of 30 and 8 of 10 in the critical group, no 0 in scenarios 1, 2, 3, 10, 11.
Critical scenarios with a 0: none.
Deterministic checks failed in scenarios: none. The checks are shown next to the score and do not change it.

Verdict: **pass**.

## Judges of this run

- `scores.json`: fail
- `scores-judge-zhipu-glm.json`: pass

- scores and scores-judge-zhipu-glm, 15 scenarios: percent agreement 0.6667, Cohen's kappa 0.4403, weighted kappa 0.3438.
- Krippendorff's alpha across the 2 judges: ordinal 0.3556, nominal 0.4246.

Verdict of the run across its 2 judges: **contested**. One judge passes the run and another fails it.
