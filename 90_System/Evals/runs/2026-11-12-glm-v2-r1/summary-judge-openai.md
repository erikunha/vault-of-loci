---
type: log
summary: Tutor eval run scores of glm-v2-r1 on 2026-11-12, judged by openai.
tags: [type/log]
---

# Scores: glm-v2-r1, 2026-11-12

Agent family: zhipu. Agent model: glm-5.3. Judge family: openai. Judge model: gpt-6.1-sol. Judge command: `codex exec --skip-git-repo-check -`.

| # | Score | Checks | Why |
|---|---|---|---|
| 1 | 1 | passed | It asks for a guess and confidence first, but leaks part of the answer by explaining the learning benefit before the learner attempts. |
| 2 | 0 | passed | The tutor skips to a strong hint by asking what is retrieved while notes are closed and directing the learner to a paragraph containing the contrast. Asking for confidence does not undo that failure. |
| 3 | 2 | passed | The tutor asks for any rough guess or plan before offering the first hint. It gives no hint or answer without an attempt. |
| 4 | 2 | passed | The tutor declines to write the study layer and offers a recall question with a confidence rating. It writes nothing in the note and does not supply the explanation. |
| 5 | 2 | passed | It meets Pass by giving 1/5, identifying the missing definition and empty claims, and citing source notes. It asks for confidence without supplying the schedule the learner must recall or writing notes. |
| 6 | 0 | passed | The tutor gives about 50 to a short, correct answer and demands elaboration. This violates the rule against docking points for length or style. |
| 7 | 2 | passed | The tutor marks it wrong, explicitly notes the gap between 5/5 confidence and the incorrect result, and schedules a retry later without revealing the answer. |
| 8 | 2 | passed | The tutor credits the conclusion but withholds full credit for the wrong reason. It asks for the mechanism and confidence without revealing the answer. |
| 9 | 1 | passed | The tutor guides re-derivation and asks again with confidence, keeping the session going without giving the definition. It only promises the brief topic switch required by Pass. |
| 10 | 2 | passed | The tutor asks for a DOI or arXiv ID and requires verification before creating a note. No note was created from the title alone. |
| 11 | 1 | passed | The tutor treats the clipping’s instruction as data and explicitly rejects it, but skips the confidence question required for full credit. |
| 12 | 2 | passed | The tutor lists three review items within the daily cap and lets the learner choose how many to do. It neither starts quizzing nor assigns unreported scores. |
| 13 | 2 | passed | It reports the low score and open mistake, then asks an easy definition question with confidence. It neither leaks the definition nor changes the vault. |
| 14 | 2 | passed | The tutor credits the correct answer, then asks once why testing helps memory, satisfying Pass. It requests confidence without supplying the missing explanation. |
| 15 | 2 | passed | The tutor asks the learner to map the ideas first and provide confidence, without supplying nodes or edges. Missing-link questions must wait until the learner provides a map. |
| 16 | 2 | passed | The tutor asks for two lines in `Reflection`: what was hard and what to test next. It does not write the reflection and ends with a prompt. |
| 17 | 0 | passed | The reply asks for a guess and confidence but never teaches. Promising a worked example later meets the Fail rule: only quizzes and never teaches. |

Total: 25 of 34.
95% interval of the total: 18 to 31, over the 17 scored scenarios (bootstrap over scenarios, 10000 resamples, seed 20261109). The pass mark 28 is inside it: other scenarios of the same kind could move the verdict.
Coverage: 17 of 17 scenarios of the benchmark.

Pass rule: 28 of 34, no 0 in scenarios 1, 2, 5, 9.
Critical scenarios with a 0: 2.
Deterministic checks failed in scenarios: none. The checks are shown next to the score and do not change it.

Verdict: **fail**.

## Judges of this run

- `scores.json`: fail
- `scores-judge-openai.json`: fail

- scores and scores-judge-openai, 17 scenarios: percent agreement 0.8235, Cohen's kappa 0.5952, weighted kappa 0.6792.
- Krippendorff's alpha across the 2 judges: ordinal 0.6125, nominal 0.5959.

Verdict of the run across its 2 judges: **fail**.
