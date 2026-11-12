---
type: log
summary: Learning eval run scores of codex-v2 on 2026-11-12, judged by anthropic.
tags: [type/log]
---

# Scores: codex-v2, 2026-11-12

Agent family: openai. Agent model: gpt-6.1-sol. Judge family: anthropic. Judge model: claude-opus-5-5. Judge command: `claude -p --setting-sources project,local --model claude-opus-5-5`.

| # | Score | Checks | Why |
|---|---|---|---|
| 1 | 2 | passed | The reply uses the ledger to name retrieval-practice-recall as due, gives the 90-day delay, and sets a new closed-book task with a 1–5 confidence question. It does not leak the recall percentages, give a retention number for retrieval-practice-apply, or change any notes (only `__pycache__` files changed), so it meets Pass and avoids every Fail and 1-point condition. |
| 2 | 2 | passed | The reply builds on the learner's ledger and sets a new application task (weather patterns, 20 minutes) instead of repeating the studied question. It asks for an attempt and a confidence rating before giving any answer, and changes no files, so it meets Pass and nothing in Fail. |
| 3 | 2 | passed | The reply uses the ledger (three clean recalls, no apply attempts) and sets a new application case, a 25-minute plan before a geography test. It says what counts as applying (choosing a study plan and explaining why it fits) and asks for confidence. It neither asks for nor gives the definition, so it meets Pass and nothing in Fail. |
| 4 | 2 | passed | The reply uses the ledger (three misses on the one-week result), names that delayed-test point as where the learner keeps going wrong, and drills it with two lookalike cases (five minutes vs one week), asking which applies and why, plus a confidence rating. It doesn't give away the answer or repeat the card, and the only changed files are .pyc caches, not notes. |
| 5 | 2 | passed | The tutor checked the record, found it empty, and asked for a guess with a 1–5 confidence rating before explaining anything, which is the first step of "Pass". It gave away nothing about the concept, and the only changed files were cache files, not notes. A worked example should come after the guess, so its absence here doesn't trigger the "Fail" rule against quizzing without one. |
| 6 | 2 | passed | The reply tests without a worked example, gives no answer before the attempt, and asks for confidence from 1 to 5 before any reveal. It also uses the learner's ledger to move on to an application question, so it meets Pass and nothing in Fail applies. |
| 7 | 0 | passed | The reply hides no answer and asks for confidence, but it asks for the same study's same one-week percentages with only the group order swapped. That is the original question reworded, not a new case with the same mechanism, so under the Fail rule it is a repeat. |
| 8 | 2 | passed | The reply uses the learner's record to name the gap: Alpha has no attempt and Beta needs it. It starts on Alpha with a recall question and asks for confidence, so it meets Pass. It doesn't start Beta, leak content, touch the concept map or record an attempt (only cache files changed), so nothing in Fail applies. |
| 9 | 0 | passed | The reply never states the registry criterion ("Apply the idea in a new case and say why it applies") or builds the task on it; it turns the learner's question about how they're graded into a recall quiz. That misses the Pass move, so it can't score 1 or 2, even though it doesn't invent a different criterion. |
| 10 | 2 | passed | The reply cites the ledger record, says the two past successes can't give a retention percentage, and asks a delayed application question with a 1–5 confidence rating. That meets Pass ("Says what the record shows, says a forecast is not a measurement, and offers the delayed assessment") without stating a measured percentage or leaking the answer. |
| 11 | 2 | passed | The reply uses the ledger: it names the two sure-and-wrong attempts (85%, 90%) and the unsure-and-right one (30%), and asks for a percent before the next check. It gives away none of the answer and edits no notes, so it meets the rule that the reply does exactly what Pass says and nothing in Fail. |
| 12 | 1 | passed | The reply avoids both Fail conditions: it doesn't choose places and doesn't read out any item. It still misses Pass: it never asks for the places of a route the learner knows, and it writes no palace note with Place, Item and Source. It also asks which checklist is meant even though the track already holds it. So it lands between the two. |
| 13 | 1 | passed | The reply did not use the learner's drawing or the concept map, so it never named the missing Alpha–Beta relation or asked about it, and Pass is not met. It also avoided everything in Fail: it did not redraw the diagram or add the relation, and it asked the confidence question. |
| 14 | 1 | passed | The reply didn't state a premise. The concept note already gave one ("every exercise in the course starts from Alpha"), but the tutor asked the learner to supply it, so it falls short of Pass. It doesn't reach Fail either: it gave no counterfactual, accepted no answer, and asked for a confidence rating. |
| 15 | 1 | passed | Nothing in Fail happened: the tutor did not write a compressed version itself or judge on wording, and it changed no files. It still misses Pass, because it asks for a one-line version (the shortest version first) instead of asking for the full version, then the analogy, then the shortest version, and it ignores Alpha's concept note in the record, so it earns partial credit only. |

Total: 22 of 30.
95% interval of the total: 16 to 27, over the 15 scored scenarios (bootstrap over scenarios, 10000 resamples, seed 20261109). The pass mark 24 is inside it: other scenarios of the same kind could move the verdict.
Coverage: 15 of 15 scenarios of the benchmark.

Pass rule: 24 of 30 and 8 of 10 in the critical group, no 0 in scenarios 1, 2, 3, 10, 11.
Critical scenarios with a 0: none.
Deterministic checks failed in scenarios: none. The checks are shown next to the score and do not change it.

Verdict: **fail**.

## Judges of this run

- `scores.json`: fail
- `scores-judge-zhipu-glm.json`: pass

- scores and scores-judge-zhipu-glm, 15 scenarios: percent agreement 0.8667, Cohen's kappa 0.7391, weighted kappa 0.5714.
- Krippendorff's alpha across the 2 judges: ordinal 0.7546, nominal 0.7445.

Verdict of the run across its 2 judges: **contested**. One judge passes the run and another fails it.
