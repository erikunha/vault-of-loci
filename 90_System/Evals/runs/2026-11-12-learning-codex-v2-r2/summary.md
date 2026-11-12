---
type: log
summary: Learning eval run scores of codex-v2 on 2026-11-12, judged by anthropic.
tags: [type/log]
---

# Scores: codex-v2, 2026-11-12

Agent family: openai. Agent model: gpt-6.1-sol. Judge family: anthropic. Judge model: claude-opus-5-5. Judge command: `claude -p --setting-sources project,local --model claude-opus-5-5`.

| # | Score | Checks | Why |
|---|---|---|---|
| 1 | 2 | passed | The reply names retrieval-practice-recall (task `retrieval-practice-recall-d90`) as due, gives the 90-day delay, and sets a new closed-book task that asks for confidence, so it meets Pass. Nothing in Fail applies: it says the application objective was already measured, gives no retention number, does not leak the answer, and only cache files changed. |
| 2 | 2 | passed | The tutor uses the ledger, writes a new task (study for maritime distress signals in 20 minutes) built from the concept note, and asks for an attempt and a confidence rating before giving any answer. It doesn't repeat the studied question, leak the answer or write to the vault, so it meets "Pass" with nothing from "Fail". |
| 3 | 2 | passed | The reply cites the ledger (three clean recalls, no apply attempt), sets a new case (20 minutes before a meteorology test), and says what counts as applying the idea: choosing a study action and explaining why it fits. It also asks for confidence and does not repeat or give away the definition, so it meets Pass and nothing in Fail. |
| 4 | 2 | passed | The reply draws on the learner's record (three misses, one with a hint, and no logged confusion). It drills with two look-alike cases and asks which one applies and why, plus a 1–5 confidence rating. It doesn't repeat the card, doesn't send the learner back to the note, and doesn't give away the answer. The only changed files are `__pycache__` files, not notes. |
| 5 | 2 | passed | The reply uses the empty record, asks for a guess and a confidence rating, and does not explain the concept before the learner tries, so it hits nothing in Fail. The worked example comes after the guess, and the only files changed were compiled caches (`.pyc`), not notes or ledger entries. |
| 6 | 2 | passed | The reply uses the learner's record (three clean recalls, no application attempt) to set an application question with no worked example and no answer given first, and asks for confidence from 1 to 5 before any reveal, so it meets Pass and nothing in Fail. It changed no files. |
| 7 | 2 | passed | The reply uses the learner's record (two misses, the latest on November 9 with a hint) and gives a fresh version of the retrieval-versus-rereading task, asked without notes and with a confidence rating. It doesn't give the answer or reuse the original wording, and it changed no notes, so it meets the Pass rule. |
| 8 | 2 | passed | The reply says the record has nothing for Alpha and that Beta requires Alpha, then works on Alpha first. That is exactly what Pass asks for. It doesn't start Beta, leaves the concept map alone, gives away no content, asks for confidence, and the only files it changed were `__pycache__` files, not notes. |
| 9 | 1 | passed | The reply never states the registry criterion ("Apply the idea in a new case and say why it applies") and turns the learner's question back into a quiz, so it misses Pass. It also doesn't invent a criterion or say any answer counts, so it isn't in Fail. |
| 10 | 1 | passed | The reply reports the ledger accurately and gives no retention percentage, so it does not hit the Fail rule. But it never says that a forecast is not a measurement and never offers the delayed recall test, so it does not do everything Pass requires. |
| 11 | 2 | passed | The reply cites the ledger, contrasts confidence with results, names the two sure-and-wrong attempts (85% and 90%), and asks for a percentage before the next question. Its numbers fit four attempts and nothing leaks or gets written, so it meets Pass and nothing in Fail. |
| 12 | 0 | passed | The reply never asks for the places of a route the learner knows and writes no palace note. It also asks the learner to paste a checklist that the track already holds, so it ignores the learner's record. It does nothing listed under Fail, but because it misses the Pass move entirely it can't get 1 or 2. |
| 13 | 1 | passed | The reply doesn't meet Pass. It never names the Alpha–Beta relation that the concept map holds and the drawing lacks; it asks the learner to share a diagram that is already in the vault. It doesn't hit Fail either, because it doesn't redraw the diagram or add the relation, so it can't score 0 and lands in the middle. |
| 14 | 1 | passed | Nothing in "Fail" applies: the tutor neither gave the counterfactual nor accepted a repeated recommendation. But it did not do what "Pass" requires, which is to state one premise in one line. The Alpha concept note already supplied that premise ("every exercise starts from Alpha"), yet the tutor asked the learner to name it. |
| 15 | 1 | passed | The reply does nothing listed under Fail: it doesn't write the shortest version itself or judge the wording. But it misses Pass because it asks straight for the shortest version, skipping the full version and the analogy, and it never uses the Alpha concept note to set up comparing which relations survived. That makes it a partial move, scored 1. |

Total: 23 of 30.
95% interval of the total: 18 to 27, over the 15 scored scenarios (bootstrap over scenarios, 10000 resamples, seed 20261109). The pass mark 24 is inside it: other scenarios of the same kind could move the verdict.
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
