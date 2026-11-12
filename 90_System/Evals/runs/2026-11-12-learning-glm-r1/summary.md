---
type: log
summary: Learning eval run scores of glm-r1 on 2026-11-12, judged by anthropic.
tags: [type/log]
---

# Scores: glm-r1, 2026-11-12

Agent family: zhipu. Agent model: glm-5.3. Judge family: anthropic. Judge model: claude-opus-5-5. Judge command: `claude -p --setting-sources project,local --model claude-opus-5-5`.

| # | Score | Checks | Why |
|---|---|---|---|
| 1 | 2 | passed | The reply names retrieval-practice-recall as the objective that is due, gives the 90-day horizon, and says the test will be a new task the learner has not seen. It lists retrieval-practice-apply only as already measured, gives no retention number, does not reveal the answer, and changes no files. |
| 2 | 0 | passed | The questions only ask the learner to restate the concept note: the definition, the Roediger and Karpicke numbers, and why rereading feels effective. That is the studied recall question for `retrieval-practice-recall`, not a new task built from the note. The Fail rule "repeats the studied question" applies, even though nothing was leaked and the confidence question was asked. |
| 3 | 0 | passed | The reply asks for the definition of retrieval practice again, which is listed under Fail. It also ignores the learner's record of three clean recalls and treats the learner as having none, instead of setting an apply task in a new case. |
| 4 | 0 | passed | The reply uses the ledger, but it never names a recurring confusion or drills it with two look-alike items. Instead it gives an easier version of the same card and plans to walk the learner back through the source note, which is the Fail case of repeating the card and pointing them back to the note. |
| 5 | 2 | passed | The reply checks the empty record and asks for a guess with a 1–5 confidence before explaining anything, which is the "guess first" step that Pass requires. The worked example belongs after the guess, so it doesn't fall under "quizzes with no worked example", and nothing is leaked or written to the vault. |
| 6 | 1 | passed | The reply avoids both Fail conditions. It gives no worked example, holds back the answer and asks for confidence from 1 to 5. A 2 also requires using the learner's record, and the reply contradicts it: it calls this a first test with no history, but the ledger shows three clean correct recalls, the last one yesterday. |
| 7 | 0 | passed | The tutor read the learner's record, but then asked the same question again in nearly the same words instead of writing a new case with the same mechanism, and the Fail rule says repeating the question scores 0. |
| 8 | 0 | passed | The tutor started Beta with a pretest and never said that Alpha, which the concept map lists as Beta's prerequisite, has no attempt in the ledger. That matches the Fail rule "Starts Beta anyway". |
| 9 | 0 | passed | The Fail rule decided it. The registry's criterion for retrieval-practice-apply is "Apply the idea in a new case and say why it applies", but the reply quotes a different one ("choose what to do the night before a test in a new subject…") as the registry text, and it says the task is built from the concept note rather than from the criterion. |
| 10 | 1 | FAILED: a reply contains '61%' (turn 2); a reply contains '40%' (turn 2) | The reply gives no measured retention percentage, so it avoids the Fail. It drops to 1 because it misreports the record as empty when the ledger holds two clean recalls (the last 40 days ago), and it hands over the exact 61%/40% figures that its own baseline question then asks the learner to recall, which the leak rule penalises. |
| 11 | 1 | passed | The reply reads the ledger, shows the gap between confidence and results, names the confident misses (rp-r-02 and rp-r-03), and its Brier score of about 0.51 matches the record, so nothing in Fail applies. It loses a point under the "skips the confidence question" rule: it asks for a 1–5 rating before the next reveal, not a probability in percent. |
| 12 | 1 | passed | Nothing in Fail applies: the tutor says the learner picks the places and doesn't read out any step. But it doesn't do what Pass says either, because it asks for a recall attempt and a confidence rating and offers an alternative, without asking for the route's places now. So it can't score 2. |
| 13 | 2 | passed | The reply names only the missing Alpha–Beta link and asks about it as a question with both options open, plus a confidence question. It doesn't redraw the diagram, add the relation, or write to any note, so it meets Pass and nothing in Fail. |
| 14 | 1 | passed | The reply makes no Fail move, since it neither answers the counterfactual nor accepts a bare repeat of the recommendation. But Pass needs one premise stated in one line from the learner's record, and the tutor asked which concept was meant instead of stating "every exercise in the course starts from Alpha" from the Alpha note, so it is the right move but falls short of 2. |
| 15 | 0 | passed | The reply asks only for the one-line version and skips the full version and the analogy, so it misses the Pass sequence. It also promises to give its own shortest version next, which is the Fail move ("writes the shortest correct version itself"). |

Total: 11 of 30.
95% interval of the total: 5 to 17, over the 15 scored scenarios (bootstrap over scenarios, 10000 resamples, seed 20261109). The pass mark 24 is outside it.
Coverage: 15 of 15 scenarios of the benchmark.

Pass rule: 24 of 30 and 8 of 10 in the critical group, no 0 in scenarios 1, 2, 3, 10, 11.
Critical scenarios with a 0: 2, 3.
Deterministic checks failed in scenarios: 10. The checks are shown next to the score and do not change it.

Verdict: **fail**.

## Judges of this run

- `scores.json`: fail
- `scores-judge-openai.json`: fail

- scores and scores-judge-openai, 15 scenarios: percent agreement 0.8667, Cohen's kappa 0.7857, weighted kappa 0.6939.
- Krippendorff's alpha across the 2 judges: ordinal 0.7067, nominal 0.7921.

Verdict of the run across its 2 judges: **fail**.
