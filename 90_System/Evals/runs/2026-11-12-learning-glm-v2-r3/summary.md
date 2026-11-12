---
type: log
summary: Learning eval run scores of glm-v2 on 2026-11-12, judged by anthropic.
tags: [type/log]
---

# Scores: glm-v2, 2026-11-12

Agent family: zhipu. Agent model: glm-5.3. Judge family: anthropic. Judge model: claude-opus-5-5. Judge command: `claude -p --setting-sources project,local --model claude-opus-5-5`.

| # | Score | Checks | Why |
|---|---|---|---|
| 1 | 0 | passed | The reply lists retrieval-practice-apply as due, but the ledger shows it was already measured at 7, 30 and 90 days, which is the Fail condition. It also gives the delay for recall as 7 and 30 days, not 90 days. |
| 2 | 2 | passed | The reply uses the ledger to show the test is due, then sets a new case instead of repeating the studied question and asks the learner to attempt it with a confidence rating before giving any answer. It never names or explains the technique, and it changed no files, so nothing in Fail applies. |
| 3 | 1 | passed | The reply uses the record, asks no definition question and says what counts as applying, so it avoids Fail. But Question 1 is about the original Roediger and Karpicke 2006 study rather than a case the learner hasn't seen, and the linked note title "Test-Enhanced Learning" gives part of the answer away, so it misses Pass. |
| 4 | 2 | passed | The reply uses the learner's record (three wrong recalls, with dates and confidences) and frames the confusion as retrieval practice versus rereading. It drills that with two look-alike items, asks which idea applies and why, asks for confidence, withholds the key and writes nothing, so it meets Pass and avoids Fail. |
| 5 | 2 | passed | The tutor read the empty record and asked for a one-line guess with a 1–5 confidence rating. It gave no explanation, leaked nothing and wrote nothing. Pass puts the guess first, so holding the worked example until the learner answers is correct, and Fail's "quizzes with no worked example" does not apply because the tutor says it will teach next. |
| 6 | 2 | passed | The reply tests straight away with a new application case, gives no worked example and no answer, and asks for confidence from 1 to 5 before any reveal, so nothing in "Fail" applies. It uses the learner's record and writes to no note. It does say there are four recalls when the vault holds three, but the rubric does not take a point off for that. |
| 7 | 1 | passed | It asks for confidence, is meant to be done without notes, and changes no files, but it isn't a new case with the same mechanism: it asks for the same 2006 experiment's figures again. The friend's claim also hints that the answer is the opposite, which partly leaks it. |
| 8 | 2 | passed | The reply uses the record: the ledger is empty and Alpha has no score or entry, so it names Alpha as the open gap and holds Beta. It starts on Alpha with a recall question and a 1–5 confidence rating, gives away nothing, and changes no files, so it meets Pass and nothing in Fail. |
| 9 | 0 | passed | The Fail rule decided it. The reply says the registry criterion for `retrieval-practice-apply` is "choose what to do the night before a test in a new subject and say why, using the effect", but the registry actually says "Apply the idea in a new case and say why it applies". The real wording only shows up as a rubric level credited to `transfer.py`, and the reply never says the task is built on the registry criterion. |
| 10 | 1 | FAILED: a reply contains '61%' (turn 2); a reply contains '40%' (turn 2) | The reply uses the ledger, says a forecast is not a measurement, offers the delayed test and asks for confidence. It loses a point under the leak rule: it quotes "61% against 40% a week out", which are the exact two numbers the offered assessment asks the learner to recall. |
| 11 | 2 | FAILED: a reply contains '40%' (turn 2) | The reply reads the ledger, shows that confidence and results point opposite ways, names both sure-and-wrong attempts (rp-r-02 at 85%, rp-r-03 at 90%) and asks for a 0–100 percent before the next reveal. Its Brier score of 0.51 fits the recorded attempts, and it leaks no answer and writes nothing, so the Pass rule is fully met with nothing from Fail. |
| 12 | 1 | passed | Nothing in Fail happened: the tutor did not choose the places or read out any item. It still missed Pass, because it never found the checklist that the track holds, did not ask for the route's places and wrote no palace note (Place/Item/Source), so it is only partly the right move. |
| 13 | 2 | passed | The reply uses the learner's record and names only the missing Alpha–Beta relation without giving its content. It then asks about the relation's direction and reason and asks for a confidence rating. It never redraws the diagram and changes no files, so it meets Pass and nothing in Fail. |
| 14 | 1 | passed | The reply doesn't hit either Fail condition: it neither gives the counterfactual nor accepts a repeated recommendation, and it does check the learner's record. But it never states a premise in one line or asks what changes and why. Instead it delays with a clarifying question even though the vault has only one concept note, so it misses the Pass move and earns 1, not 2. |
| 15 | 2 | passed | The reply checks the record, asks for the full version, the analogy and the shortest version in that order, waits for all three, and asks for a confidence rating. It also says it will judge by the relations, not the wording, and it neither writes a compression itself nor changes any file, so nothing in "Fail" applies. |

Total: 21 of 30.
95% interval of the total: 15 to 26, over the 15 scored scenarios (bootstrap over scenarios, 10000 resamples, seed 20261109). The pass mark 24 is inside it: other scenarios of the same kind could move the verdict.
Coverage: 15 of 15 scenarios of the benchmark.

Pass rule: 24 of 30 and 8 of 10 in the critical group, no 0 in scenarios 1, 2, 3, 10, 11.
Critical scenarios with a 0: 1.
Deterministic checks failed in scenarios: 10, 11. The checks are shown next to the score and do not change it.

Verdict: **fail**.

## Judges of this run

- `scores.json`: fail
- `scores-judge-openai.json`: fail

- scores and scores-judge-openai, 15 scenarios: percent agreement 0.8, Cohen's kappa 0.6739, weighted kappa 0.6809.
- Krippendorff's alpha across the 2 judges: ordinal 0.7102, nominal 0.6801.

Verdict of the run across its 2 judges: **fail**.
