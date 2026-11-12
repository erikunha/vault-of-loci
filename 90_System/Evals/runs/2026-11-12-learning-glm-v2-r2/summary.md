---
type: log
summary: Learning eval run scores of glm-v2 on 2026-11-12, judged by anthropic.
tags: [type/log]
---

# Scores: glm-v2, 2026-11-12

Agent family: zhipu. Agent model: glm-5.3. Judge family: anthropic. Judge model: claude-opus-5-5. Judge command: `claude -p --setting-sources project,local --model claude-opus-5-5`.

| # | Score | Checks | Why |
|---|---|---|---|
| 1 | 2 | passed | The reply names retrieval-practice-recall as the objective that is due, gives the 90-day delay, and sets a new closed-book task with a 1–5 confidence question. It avoids every Fail condition: it does not leak the answer, gives no retention number for retrieval-practice-apply (which it marks as already measured), and records nothing. |
| 2 | 2 | passed | The reply builds a new transfer case from the concept note's experiment, without repeating the studied question or giving the winner or the one-week figures. It asks for a closed-book attempt with a 1–5 confidence and writes nothing to the vault, so it meets Pass and nothing in Fail. |
| 3 | 1 | passed | The reply uses the record and doesn't ask for the definition again, so it avoids Fail. But it doesn't meet Pass: it describes what applying would mean and then asks an explain question about the 2006 study, not an apply task in a new case. Its question also gives away the study's result (rereading ahead at five minutes, reversed a week later) and miscounts the record as 4 recalls when the vault holds 3, so it scores 1 rather than 2. |
| 4 | 2 | passed | The reply cites the three wrong recalls from the learner's record and names the rereading-versus-retrieval confusion; the record doesn't hold the learner's answers, so it says it took that confusion from the source note. It then drills two look-alike cases, asks which one is retrieval practice and why, and asks for a confidence rating, without giving the key, repeating the card, sending the learner back to the note, or writing to any file. |
| 5 | 2 | passed | The tutor read the empty record and asked for a guess with a confidence rating before explaining anything, which is the first step Pass requires; the worked example belongs after the guess. It gave away nothing and wrote no files, so neither Fail rule applies. |
| 6 | 2 | passed | Under the Pass rule, the tutor uses the learner's record to skip re-asking recall and tests without a worked example or the answer. It asks for a 1–5 confidence before any reveal, and nothing in Fail applies. The premise that the winner changes with delay restates a fact the learner has already recalled, so it is not a leak; saying four events instead of three is a small misread that the rubric doesn't penalize. |
| 7 | 2 | passed | The reply uses the learner's record and gives a new case with the same mechanism (Maria rereads, Jonas recalls without feedback). It asks for an attempt without notes and a confidence rating, without giving the answer or the percentages, so it meets Pass and nothing in Fail. |
| 8 | 2 | passed | The reply reads the record, says Alpha has no attempt even though the concept map puts it before Beta, and starts Alpha with a pretest and a confidence question. It does not start Beta, leak the answer, or edit any file, so it meets Pass with nothing from Fail. |
| 9 | 0 | passed | The registry criterion is "Apply the idea in a new case and say why it applies," but the reply names a different one as the criterion for the current objective ("choose what to do the night before a test in a new subject and say why, using the effect"). That counts as inventing a different criterion, which is a Fail. It also never says the task is built on the registry criterion. |
| 10 | 2 | passed | The reply reports what the record shows: two clean recalls, a longest verified delay of 10 days, and nothing tested at 30 days. It says the 30-day retention stays unknown until tested rather than guessed, and offers the delayed closed-book test with a confidence question. It gives no retention percentage and does not leak the experiment's numbers. |
| 11 | 2 | passed | The reply reads the ledger, gives figures the ledger supports (3 sure attempts with 1 right, Brier about 0.51), and names the two sure-and-wrong attempts (11-02 and 10-28) plus the unsure-and-right one. It asks for a percent probability before the next reveal and leaks nothing, writes nothing and records nothing, so it meets Pass with nothing from Fail. |
| 12 | 1 | passed | It avoids both Fail conditions: it neither picks the places nor reads out any item. But it asks the learner which checklist they mean when the track already holds the five-step one, and it never asks for one place per item. The right move is only partly done, so it misses Pass. |
| 13 | 1 | passed | The reply reads the record, asks for confidence, and neither redraws the diagram nor adds the relation, so the Fail rule does not apply. But it never names the missing Alpha–Beta relation or asks about it, so it does not meet Pass. It asks which drawing to check even though it had already found the logged one. |
| 14 | 1 | passed | Nothing in Fail happened: the tutor gave no counterfactual and credited no answer. But it never stated a premise in one line or asked what changes. It asked the learner to choose between Alpha and Retrieval practice, even though the Alpha note's premise ("every exercise starts from Alpha") was right there. So it doesn't fully meet Pass. |
| 15 | 2 | passed | The tutor checked the learner's record and asked for the full version, the analogy and the shortest version in that order, all in one reply, plus a confidence for each. It wrote no compression itself and leaked nothing, which is what Pass asks for; listing the surviving relations correctly waits for the learner's answers. |

Total: 24 of 30.
95% interval of the total: 19 to 28, over the 15 scored scenarios (bootstrap over scenarios, 10000 resamples, seed 20261109). The pass mark 24 is inside it: other scenarios of the same kind could move the verdict.
Coverage: 15 of 15 scenarios of the benchmark.

Pass rule: 24 of 30 and 8 of 10 in the critical group, no 0 in scenarios 1, 2, 3, 10, 11.
Critical scenarios with a 0: none.
Deterministic checks failed in scenarios: none. The checks are shown next to the score and do not change it.

Verdict: **pass**.

## Judges of this run

- `scores.json`: pass
- `scores-judge-openai.json`: fail

- scores and scores-judge-openai, 15 scenarios: percent agreement 0.8, Cohen's kappa 0.6591, weighted kappa 0.4444.
- Krippendorff's alpha across the 2 judges: ordinal 0.4937, nominal 0.6615.

Verdict of the run across its 2 judges: **contested**. One judge passes the run and another fails it.
