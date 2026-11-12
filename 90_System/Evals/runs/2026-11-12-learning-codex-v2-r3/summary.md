---
type: log
summary: Learning eval run scores of codex-v2 on 2026-11-12, judged by anthropic.
tags: [type/log]
---

# Scores: codex-v2, 2026-11-12

Agent family: openai. Agent model: gpt-6.1-sol. Judge family: anthropic. Judge model: claude-opus-5-5. Judge command: `claude -p --setting-sources project,local --model claude-opus-5-5`.

| # | Score | Checks | Why |
|---|---|---|---|
| 1 | 2 | passed | The reply names `retrieval-practice-recall` as the objective that is due, gives the 90-day delay and sets a new task (the safety-course case), which is everything Pass asks for. It also asks for confidence, gives no answer or retention number for apply, and changed only `__pycache__` files, so none of the 1-point deductions apply. |
| 2 | 2 | passed | The tutor uses the ledger's record of two clean recalls, sets a new transfer task built from the concept note (weather forecasting), and asks for an attempt and a confidence rating without giving the answer. Under the rule that a reply which does exactly what Pass says and nothing in Fail scores 2, it scores 2. |
| 3 | 2 | passed | The reply uses the ledger, sets an unseen case (first-aid test tomorrow, 25 minutes tonight), says what counts as applying the idea and asks for confidence, so it meets Pass. It doesn't ask for or give the definition, doesn't leak the answer and changes no files. |
| 4 | 2 | passed | The reply cites the learner's record (three misses on the one-week result, no mistakes logged), then drills with two look-alike items (summary with the passage visible vs. hidden), asks which one applies and why, and asks for confidence. It does not repeat the card or send the learner back to the note. It reveals no answer, and the only changed files are caches, so no note was edited and no attempt was recorded. |
| 5 | 2 | passed | The reply cites the empty record, asks for a guess and a 1–5 confidence rating before explaining anything, and says a worked example comes next. That is the correct first step under Pass, and it doesn't hit Fail: no explanation before the attempt, nothing leaked, only cache files changed and no attempt recorded. |
| 6 | 2 | passed | The reply uses the ledger, poses a fresh application question with no worked example, gives no answer away and asks for confidence from 1 to 5 before any reveal, so it meets "Pass" and triggers nothing in "Fail". Grading against the source has to wait for the learner's answer, and the vault was not changed. |
| 7 | 0 | passed | The reply re-asks the original question in a bar-chart frame: it wants the same one-week rereading and testing percentages from the same study. Pass requires a new case built on the same mechanism, so this counts as repeating the question under Fail, even though it gives no answer and does ask for confidence. |
| 8 | 2 | passed | The reply uses the learner's record, says Alpha is the missing prerequisite for Beta, and starts on Alpha with a recall question plus a confidence rating. It doesn't start Beta, leak the answer or edit any notes (the only changed files are Python bytecode caches), so it meets Pass and nothing in Fail. |
| 9 | 0 | passed | The reply never checks the objective registry or states its criterion ("Apply the idea in a new case and say why it applies"); it asks the learner to guess it, so it misses Pass. It doesn't invent a criterion, but without the Pass move it can't get the 2 or the 1 ("right move") score. |
| 10 | 1 | passed | No retention percentage is stated as if measured, so the Fail rule is not triggered, and the reply correctly reports the record and says 30-day retention is unmeasured. But it never frames a forecast as distinct from a measurement, and it asks a generic transfer question instead of explicitly offering the delayed assessment that would measure retention, so it only partly meets Pass. |
| 11 | 2 | passed | The reply uses the ledger: it names the two sure-and-wrong attempts (85% and 90%) and the unsure-but-right one (30%), and asks for a percent probability before the next answer. It states no calibration number the record doesn't support, leaks nothing, and changed only cache files, so it meets Pass and nothing in Fail. |
| 12 | 1 | passed | The reply doesn't hit anything in Fail: it neither picks the places nor reads the items out. But it misses Pass, because it never asks for the places of a route the learner knows. It also asks which checklist when the track already holds it, so it's only partly the right move. |
| 13 | 0 | passed | The reply hits nothing in Fail, since it neither redraws the diagram nor adds the relation, but it also misses Pass: it never reads the drawing already in the vault, never names the Alpha–Beta relation the concept map holds, and asks for the canvas path instead of asking about that relation. That is not the right move with a minor flaw, so the 1 band does not apply. |
| 14 | 1 | passed | The reply avoids both Fail conditions (it gives no counterfactual and credits nothing) and asks for confidence. But Pass requires the tutor to state one premise in one line, and it asked the learner to name one instead, even though the Alpha note supplied it, so it cannot earn a 2. |
| 15 | 0 | passed | The reply asks for a one-line guess and a confidence rating, which jumps straight to the shortest version. It never asks for the full version and the analogy in the required order, and it ignores Alpha's concept note, whose relations are what the compression should be checked against. That is not the Pass move, so it can't earn 2, and it isn't the right move with a minor flaw, so it can't earn 1. |

Total: 19 of 30.
95% interval of the total: 12 to 25, over the 15 scored scenarios (bootstrap over scenarios, 10000 resamples, seed 20261109). The pass mark 24 is inside it: other scenarios of the same kind could move the verdict.
Coverage: 15 of 15 scenarios of the benchmark.

Pass rule: 24 of 30 and 8 of 10 in the critical group, no 0 in scenarios 1, 2, 3, 10, 11.
Critical scenarios with a 0: none.
Deterministic checks failed in scenarios: none. The checks are shown next to the score and do not change it.

Verdict: **fail**.

## Judges of this run

- `scores.json`: fail
- `scores-judge-zhipu-glm.json`: pass

- scores and scores-judge-zhipu-glm, 15 scenarios: percent agreement 0.6667, Cohen's kappa 0.4231, weighted kappa 0.52.
- Krippendorff's alpha across the 2 judges: ordinal 0.6406, nominal 0.4153.

Verdict of the run across its 2 judges: **contested**. One judge passes the run and another fails it.
