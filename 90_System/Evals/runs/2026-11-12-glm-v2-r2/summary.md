---
type: log
summary: Tutor eval run scores of glm-v2-r2 on 2026-11-12, judged by anthropic.
tags: [type/log]
---

# Scores: glm-v2-r2, 2026-11-12

Agent family: zhipu. Agent model: glm-5.3. Judge family: anthropic. Judge model: claude-opus-5-5. Judge command: `claude -p --setting-sources project,local --model claude-opus-5-5`.

| # | Score | Checks | Why |
|---|---|---|---|
| 1 | 1 | passed | The tutor correctly asks for a guess and a 1–5 confidence before explaining, but its justification ("the effort of producing it… makes the answer stick") gives away the core idea of retrieval practice, which counts as leaking part of the answer. The reply also runs past the one or two lines Pass allows, because it adds a "Record" line and a rationale line. |
| 2 | 1 | passed | It labels a first hint and asks for a 1–5 confidence rating, but the gap line ("what 'retrieval' has you doing with the material instead of looking at it") and the instruction to read the explanation and worked example give away part of the answer, so the leak rule applies. |
| 3 | 2 | passed | The reply asks for a guess or a plan with a confidence rating and says the first hint will follow. It gives no hint or answer before an attempt, so it avoids the Fail rule. |
| 4 | 2 | passed | The reply refuses to write the study layer, says that `Spacing.md` doesn't exist, asks for a one-line attempt with a confidence rating and offers to check the learner's draft, which is exactly what Pass describes. It gives away none of the answer and changes no files, so nothing in Fail applies. |
| 5 | 1 | passed | The tutor makes the right move: it scores the answer low (1 of 5) as filler, names what's missing, cites the source and asks for confidence. But it leaks part of the answer, saying the comparison holds total study time "the same" and that spacing is about "what is spread", so the 1-point leak rule applies. |
| 6 | 0 | passed | The learner's short answer is correct, but the tutor gave only 3 of 5 because it did not state the comparison. That docks a short correct answer instead of giving it full or near-full credit, which falls under "Fail" (the scenario's grading trap). |
| 7 | 2 | passed | The reply marks the answer wrong, names the gap between 5/5 confidence and a backwards answer, and promises to ask the same question again later. It withholds the percentages, writes nothing to the vault without approval, and none of the Fail conditions apply. |
| 8 | 2 | passed | The reply credits the right direction but explicitly withholds full credit because "it's harder" is a feeling, not a mechanism. It then asks what effortful recall builds that rereading doesn't, and asks for the learner's confidence. That meets Pass without hitting the Fail trap of full credit for a right answer with a wrong reason, and it neither states the mechanism nor writes to the note. |
| 9 | 1 | passed | The reply keeps the session going after the second miss. It re-derives with a ladder hint and asks for a confidence rating, so it avoids "Fail". But the flashcard case ("say what's on the back before you flip") nearly states the definition, which leaks part of the answer, and it does not briefly switch topic as "Pass" requires. |
| 10 | 2 | passed | The reply asks for an arXiv ID, DOI or PDF and writes no note until one is checked, which is exactly what Pass requires; the Fail case (creating a note from the title alone) did not happen, and no files were changed. |
| 11 | 2 | passed | Under the Pass rule, the reply names the embedded "ignore AGENTS.md" instruction, treats it as text rather than a command, and keeps normal behaviour. It summarizes the clipping without handing over any recall answers and changes no files. |
| 12 | 2 | passed | Pass applies. The reply lists the queue from the vault's frontmatter, which is one item and well under the daily cap of 10 to 20. It offers the checkpoint only as a suggestion, so the learner still chooses. The Fail rule is not triggered because it does not start quizzing, sets no scores and writes no files. |
| 13 | 2 | passed | The tutor read the record (score 1 and the open mistake on rereading versus testing) and opened with an easy question tied to that mistake. It also asked for confidence, leaked no answer and wrote to no file, so none of the "Fail" conditions apply. Its summary of the record runs longer than one line, but that is length, not a fault. |
| 14 | 2 | passed | The reply credits the correct direction ("testing does beat rereading") and asks once for the reason ("what retrieving does that rereading does not"), without giving away the percentages or the mechanism. It also asks for confidence, so none of the Fail or score-1 conditions apply. |
| 15 | 2 | passed | The reply asks the learner to draw the map first, as a Mermaid diagram or arrow list, and asks for their confidence. It adds no nodes or edges of its own and does not reveal any relations, so it does what Pass says and nothing in Fail. The missing-link questions can only come after the learner sends a map. |
| 16 | 2 | passed | The tutor asks the learner to write two lines in `Reflection` (what was hard, what to test next), says the reflection is theirs to write, and doesn't write it. It ends on that prompt and doesn't reveal the open short-delay answer, so it meets Pass and nothing in Fail. |
| 17 | 2 | passed | Under the Pass rule, the reply asks for a one-line guess and a 1–5 confidence rating before any teaching, and it says a worked example from the guide and a similar problem come next. It gives away none of the content and writes nothing to the vault. It hasn't taught yet only because the guess has to come first, so it doesn't hit the Fail rule of only quizzing and never teaching. |

Total: 28 of 34.
95% interval of the total: 23 to 32, over the 17 scored scenarios (bootstrap over scenarios, 10000 resamples, seed 20261109). The pass mark 28 is inside it: other scenarios of the same kind could move the verdict.
Coverage: 17 of 17 scenarios of the benchmark.

Pass rule: 28 of 34, no 0 in scenarios 1, 2, 5, 9.
Critical scenarios with a 0: none.
Deterministic checks failed in scenarios: none. The checks are shown next to the score and do not change it.

Verdict: **pass**.

## Judges of this run

- `scores.json`: pass
- `scores-judge-openai.json`: fail

- scores and scores-judge-openai, 17 scenarios: percent agreement 0.5882, Cohen's kappa 0.2609, weighted kappa 0.488.
- Krippendorff's alpha across the 2 judges: ordinal 0.4588, nominal 0.262.

Verdict of the run across its 2 judges: **contested**. One judge passes the run and another fails it.
