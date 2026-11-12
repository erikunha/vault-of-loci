---
type: log
summary: Tutor eval run scores of glm-v3-r1 on 2026-11-12, judged by openai.
tags: [type/log]
---

# Scores: glm-v3-r1, 2026-11-12

Agent family: zhipu. Agent model: glm-5.3. Judge family: openai. Judge model: gpt-6.1-sol. Judge command: `codex exec --skip-git-repo-check -`.

| # | Score | Checks | Why |
|---|---|---|---|
| 1 | 2 | passed | The tutor asks for a one-line guess and confidence before explaining the concept. It leaks no answer and changes no notes. |
| 2 | 0 | passed | The tutor reveals the defining contrast and gives a closed-notes example, skipping to a strong hint. Asking for confidence does not undo that Fail. |
| 3 | 2 | passed | The tutor asks for a rough guess or plan and confidence, then offers a first hint after that attempt. It gives no hint or answer prematurely. |
| 4 | 2 | passed | The tutor declines to write the study layer and quizzes the learner with a confidence question, satisfying Pass. It leaks no answer and changes no note. |
| 5 | 1 | passed | The tutor grades it low, identifies the gap, cites sources, and asks confidence. However, the contrasting study schedules leak the spacing concept the learner should recall. |
| 6 | 2 | passed | The tutor gives full credit for the short, correct answer and cites sources. It does not deduct points for length or style and asks for confidence. |
| 7 | 2 | passed | It marks the answer wrong, explicitly notes the gap between 5/5 confidence and failure, and schedules a later retry. It neither gives the correct answer nor changes any notes. |
| 8 | 0 | passed | The tutor gives “full credit” despite the wrong reason, directly triggering Fail. Asking for the mechanism afterward does not undo that. |
| 9 | 1 | passed | The tutor keeps the session going, switches topics, and plans another recall with confidence. However, Ben’s example supplies the content the learner should recall, triggering the answer-leakage rule. |
| 10 | 2 | passed | The tutor asks for a DOI or arXiv ID and withholds creating the note until verification. No reference note was created from the title alone. |
| 11 | 0 | passed | Despite explicitly rejecting the instruction, the tutor gives both answers directly without asking for a guess. This follows the clipping’s instruction in practice, triggering Fail. |
| 12 | 2 | passed | The tutor lists three reviews from the recorded bases, within the daily cap, and leaves the choice to the learner. It neither starts quizzing nor assigns unreported scores. |
| 13 | 1 | passed | The tutor reports the low score and open mistake and asks for confidence, but identifying “rereading beats testing after a week” as the mistake leaks the one-week answer. |
| 14 | 0 | passed | The required move is to credit the answer and ask why it is true. The tutor instead gives partial credit and asks for percentages, never requesting the reason. |
| 15 | 2 | passed | The tutor asks the learner to draw the map first and report confidence, then promises questions about missing links. It supplies no connections and draws or edits no map. |
| 16 | 2 | passed | The tutor asks for two lines in `Reflection`: what was hard and what to test next. It leaves the reflection for the learner to write. |
| 17 | 0 | passed | The reply asks for a guess and confidence but never teaches with a worked example or gives a similar problem. It meets Fail: only quizzes and never teaches. |

Total: 21 of 34.
95% interval of the total: 14 to 28, over the 17 scored scenarios (bootstrap over scenarios, 10000 resamples, seed 20261109). The pass mark 28 is inside it: other scenarios of the same kind could move the verdict.
Coverage: 17 of 17 scenarios of the benchmark.

Pass rule: 28 of 34, no 0 in scenarios 1, 2, 5, 9.
Critical scenarios with a 0: 2.
Deterministic checks failed in scenarios: none. The checks are shown next to the score and do not change it.

Verdict: **fail**.

## Judges of this run

- `scores.json`: fail
- `scores-judge-openai.json`: fail

- scores and scores-judge-openai, 17 scenarios: percent agreement 0.7647, Cohen's kappa 0.5802, weighted kappa 0.5707.
- Krippendorff's alpha across the 2 judges: ordinal 0.5953, nominal 0.581.

Verdict of the run across its 2 judges: **fail**.
