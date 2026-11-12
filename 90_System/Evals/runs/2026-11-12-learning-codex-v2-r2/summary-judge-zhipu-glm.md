---
type: log
summary: Learning eval run scores of codex-v2 on 2026-11-12, judged by zhipu.
tags: [type/log]
---

# Scores: codex-v2, 2026-11-12

Agent family: openai. Agent model: gpt-6.1-sol. Judge family: zhipu. Judge model: glm-5.3. Judge command: `glm -p --setting-sources project,local --model opus`.

| # | Score | Checks | Why |
|---|---|---|---|
| 1 | 2 | passed | The reply names retrieval-practice-recall as the objective due (naming the task `retrieval-practice-recall-d90` and excluding the already-measured apply objective), states the 90-day delay, and sets a new closed-book task with a confidence question — and it states no retention number for retrieval-practice-apply nor leaks the answer. |
| 2 | 2 | passed | The reply reads the ledger accurately (two clean recalls, last Aug 4, no application attempt), poses an unseen application task built on the retrieval-practice note without hinting the answer, and asks for an unaided attempt with a 1–5 confidence rating before any answer is given. |
| 3 | 2 | passed | The reply reads the ledger (three recalls, no apply attempt) and builds a novel application task — choosing how to spend 20 minutes before a meteorology test — while stating what counts as applying it and asking for a confidence rating, without re-asking or answering the definition. |
| 4 | 2 | passed | The reply works from the learner's ledger (three misses, no recorded mistake to explain the confusion), drills that recurring confusion with two lookalike cases asking which applies and why, and asks for a confidence rating — without revealing which case is correct, repeating the card, or pointing back to the note. |
| 5 | 1 | passed | The reply uses the empty record correctly and makes the right opening move — guess first, with a confidence scale, no leak and no concept explanation — but as the transcript's last word it never delivers the worked example from the note and the similar problem that Pass requires when the record is empty. |
| 6 | 2 | passed | The reply uses the ledger (three clean recalls → escalate to application) and tests without a worked example, asking for confidence 1–5 before any reveal, and no answer content or record-writing leaked. |
| 7 | 2 | passed | The reply uses the learner's record, poses a fresh variation of the missed item, asks for a no-notes attempt with a confidence rating, and neither leaks the answer nor writes to the ledger or logs an unconfirmed attempt. |
| 8 | 2 | passed | The reply uses the ledger (empty, no Alpha attempt), names the gap — Alpha is missing — and works on Alpha first because Beta requires it, asking for an unaided guess with a confidence rating; it doesn't start Beta, rewrite the concept map, or leak the answer. |
| 9 | 1 | passed | The reply uses the learner's record and asks for a guess plus confidence without leaking the answer, but it never states the registry criterion ("Apply the idea in a new case and say why it applies") or that the task is built on it, so it falls short of Pass; it invents no other criterion and doesn't say any answer counts, so Fail isn't triggered. |
| 10 | 1 | passed | The reply reads the record accurately, says a forecast is not a measurement, and asks the confidence question without leaking anything — but it only notes "there is no recorded 30-day test"; it never actually offers the delayed assessment that Pass requires. |
| 11 | 2 | passed | The reply reads the ledger, names the sure-and-wrong attempts (85% and 90% incorrect) against the 30%-confident correct one, and asks for a percent prediction before the next reveal; every number matches the record, nothing is leaked, and no note or unconfirmed attempt was written. |
| 12 | 1 | passed | The tutor checks the learner's record (empty ledger and mistake log), names the skill, and asks the confidence question without leaking any item or choosing places itself — the right move. But it stops at clarifying which checklist to use; it never asks for the places of a route the learner knows, one per item, and no palace note with Place/Item/Source was written, so it falls short of Pass. |
| 13 | 1 | passed | The reply avoids Fail (it redraws nothing and adds no relation) and does ask for confidence, but it never names the relation the concept map holds and the drawing lacks, nor asks a question about it — it defers to asking which concept and for the canvas path, so it only partially does what Pass requires. |
| 14 | 1 | passed | The reply reads the learner's record and asks a confidence-rated "what changes and why" question without leaking the counterfactual, but it never states one premise in one line as Pass requires — it bounces identifying the premise back to the learner instead of stating it (e.g., Alpha's premise from the vault). |
| 15 | 1 | passed | The tutor made the right move — it checked the record, chose the compression-challenge, asked the learner to produce the shortest version with a confidence rating, and wrote no version itself, so nothing in Fail applies. But it only requested the shortest version, not the full version, then the analogy, then the shortest version in that order, so it cannot yet list which relations survived. |

Total: 23 of 30.
95% interval of the total: 19 to 27, over the 15 scored scenarios (bootstrap over scenarios, 10000 resamples, seed 20261109). The pass mark 24 is inside it: other scenarios of the same kind could move the verdict.
Coverage: 15 of 15 scenarios of the benchmark.

Pass rule: 24 of 30 and 8 of 10 in the critical group, no 0 in scenarios 1, 2, 3, 10, 11.
Critical scenarios with a 0: none.
Deterministic checks failed in scenarios: none. The checks are shown next to the score and do not change it.

Verdict: **fail**.

## Judges of this run

- `scores.json`: fail
- `scores-judge-zhipu-glm.json`: fail

- scores and scores-judge-zhipu-glm, 15 scenarios: percent agreement 0.8667, Cohen's kappa 0.7458, weighted kappa 0.7887.
- Krippendorff's alpha across the 2 judges: ordinal 0.8561, nominal 0.7511.

Verdict of the run across its 2 judges: **fail**.
