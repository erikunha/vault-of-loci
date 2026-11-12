---
type: log
summary: Learning eval run scores of codex-v2 on 2026-11-12, judged by zhipu.
tags: [type/log]
---

# Scores: codex-v2, 2026-11-12

Agent family: openai. Agent model: gpt-6.1-sol. Judge family: zhipu. Judge model: glm-5.3. Judge command: `glm -p --setting-sources project,local --model opus`.

| # | Score | Checks | Why |
|---|---|---|---|
| 1 | 2 | passed | The reply names `retrieval-practice-recall` as the objective that owes the test, states the 90-day delay, and frames the test as a new applied task with a confidence prompt; it explicitly notes apply is already measured without giving a retention number, and only incidental __pycache__ files changed (no attempt recorded, no leak). |
| 2 | 2 | passed | The reply builds an unseen application task from the concept note, asks the learner to attempt it before any answer, includes the 1–5 confidence prompt, and leaks nothing — it also correctly grounds the delay in the ledger's two clean recalls. |
| 3 | 2 | passed | The reply uses the ledger (three clean recalls, no apply attempts) to build a novel transfer task — budget 25 minutes before tomorrow's first-aid test — states what counts as applying it (a plan plus a why), and asks for confidence, without re-asking or answering the definition. |
| 4 | 2 | passed | The reply draws on the ledger record (three misses, blank concept fields, no logged mistakes) and drills the confusion with two look-alike scenarios asking which applies and why, plus a confidence rating — it doesn't repeat the card, tell the learner to reread the note, or leak the answer. |
| 5 | 2 | passed | The reply reads the learner's empty record, asks for a guess with a confidence rating before explaining anything, and sets up the worked example that Pass calls for — no leak, no pre-explanation, no unconfirmed attempt recorded. |
| 6 | 2 | passed | The reply tests with a fresh application scenario and no worked example, asks for confidence 1–5 before any reveal, cites the source for grading, and builds the question from the ledger record without writing to it or leaking the answer. |
| 7 | 2 | passed | The reply poses a reworded variant of the missed item (bar-chart framing of the same result) "From memory" — i.e., without notes — asks for a confidence rating, gives no part of the answer, and records no unconfirmed attempt (only incidental .pyc files changed). |
| 8 | 2 | passed | The reply reads the learner's record, names Alpha as the missing prerequisite before Beta, redirects work to Alpha first, and asks for an unaided recall with a confidence rating — exactly what Pass requires, with no leak, no map rewrite, and no unconfirmed attempt logged. |
| 9 | 1 | passed | The reply checks the learner's record and asks for a guess with confidence (no leak, no invented criterion, never says any answer counts), so it avoids Fail — but it never states the registry criterion ("Apply the idea in a new case and say why it applies") or that the transfer task is built on it, so it falls short of Pass. |
| 10 | 2 | passed | The reply reports what the ledger actually shows (two clean recalls, blank fields), explicitly refuses to state a retention percentage because it is unmeasured, and offers an unaided delayed retrieval question with a confidence rating — no leak, no writes, no recorded attempt. |
| 11 | 2 | passed | The reply reads the ledger, lays out the confidence-vs-result gaps (85%/90% wrong, 30% right), names the sure-and-wrong attempts, and asks for a 0–100% probability before the next reveal — exactly what Pass requires, with no leak, no unsupported calibration claim, and no unconfirmed attempt recorded. |
| 12 | 1 | passed | The reply uses the learner's record and starts the right move — reading the ledger, asking for a from-memory guess with confidence, leaking nothing from Fail — but it never asks the learner for route places nor writes the palace note with Place/Item/Source, so it falls short of exactly what Pass requires. |
| 13 | 1 | passed | The reply consults the learner's record, asks a question with a confidence scale, and neither redraws the diagram nor leaks the missing relation — but it never names the relation the source holds and the drawing lacks, so it falls short of exactly what Pass requires. |
| 14 | 1 | passed | The reply reads the learner's record (attempts ledger, mistake log) and asks a what-changes-and-why question with a confidence rating, committing nothing in Fail — but it never states a premise in one line itself (e.g., the Alpha premise from the vault); it deflects that job back to the learner, so it does not do exactly what Pass says. |
| 15 | 1 | passed | The reply uses the learner's record and avoids both Fail conditions (no version written by the tutor, no wording-based judgment), but it only asks which idea plus a one-line guess with confidence — it never requests the full version, the analogy, and the shortest version in that order, so it does not execute the Pass sequence. |

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

- scores and scores-judge-zhipu-glm, 15 scenarios: percent agreement 0.6667, Cohen's kappa 0.4231, weighted kappa 0.52.
- Krippendorff's alpha across the 2 judges: ordinal 0.6406, nominal 0.4153.

Verdict of the run across its 2 judges: **contested**. One judge passes the run and another fails it.
