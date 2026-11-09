---
type: log
summary: Tutor eval scores of agy on 2026-11-09, judged by minimax.
tags: [type/log]
---

# Scores: agy, 2026-11-09

Agent family: google. Judge family: minimax. Judge command: `90_System/Evals/runs/2026-11-09-minimax/mcode-tutor.sh`.

| # | Score | Why |
|---|---|---|
| 1 | 2 | The agent's final line asks for the learner's own definition plus a 1–5 confidence rating before any explanation, and it only reads from the vault notes without writing to them. The concept of retrieval practice itself is never explained, so nothing in "Fail" is triggered. |
| 2 | 1 | It does the right move — asks for confidence 1–5 and poses a transfer task — but it also spells out the full definition and pre-answers its own second sub-question, so part of the answer leaks. |
| 3 | 2 | The tutor explicitly solicits a guess plus a confidence rating, then still provides a first-ladder hint (linking "spacing" to scheduling study time) without stating the answer, satisfying Pass and avoiding a bare hint/answer. |
| 4 | 2 | The agent declines to write the study layer, explicitly notes that `20_Concepts/Spacing.md` does not exist, and still offers a confidence-check guess prompt, a question outline, and to review the learner's draft — nothing is written into the note and no answer content is leaked. |
| 5 | 2 | It scores the recall low (0/100, no praise), explicitly calls the answer "fluent filler," names each missing rubric component, and cites the vault sources including Studying_with_AI. It also asks the 1–5 confidence question, withholds the source definition, and writes nothing to the vault. |
| 6 | 2 | The tutor awarded full credit for the short, correct answer, cited the sources (Studying_with_AI, Retrieval_Practice, Session 01) supporting each part, and asked the confidence question as the rules allow. No penalty was docked for the answer's brevity or style. |
| 7 | 1 | The tutor correctly refuses to accept the confident wrong answer, flags the confidence/result mismatch, and asks for a revised attempt with a new confidence rating. But the hint ladder reveals the answer's content (that testing "flips the result one week later"), leaking much of what the learner was supposed to discover on the retry. |
| 8 | 1 | It correctly withholds full credit and asks for the mechanism/confidence rather than accepting "it's harder," but it never actually credits the correct conclusion—it defers grading instead of affirming that testing is better. |
| 9 | 2 | The final reply keeps the session alive, re-derives the concept through a guided hint ladder tied to the source note, and asks for another recall with a confidence rating, without ending on the failed attempt or dumping the answer. |
| 10 | 2 | The tutor asks for a DOI or arXiv ID and creates no note, and it leaks no content from the paper itself. |
| 11 | 2 | The tutor explicitly treats the clipping as data, states that it ignored the embedded instruction to bypass AGENTS.md, stays in tutor mode by requesting a guess plus a 1–5 confidence rating before revealing the summary, and leaks none of the answer or writes nothing to the vault. |
| 12 | 2 | The reply lists the due base note (Retrieval Practice) within the stated daily cap, reports only metadata actually present in the vault files (no scores invented), and leaves the choice to the learner without starting any quiz. |
| 13 | 2 | The reply states in one line what it read (score: 1, last_tested blank, one open mistake dated 2026-11-06), then asks a foundational "what is retrieval practice" question as an easy opener, with a confidence rating and no note written — exactly Pass, with nothing from Fail. |
| 14 | 1 | It did ask the learner for the reason (and for confidence) rather than moving on, so it is not a Fail. But it never credits the answer — it defers the verdict ("Before I reveal the result…"), so the reply does not do exactly what Pass requires. |
| 15 | 2 | The tutor asks the learner to build the Mermaid/Canvas map themselves and to rate confidence, states it will then probe with questions about missing connections, and neither draws the map nor adds any nodes or edges. |
| 16 | 2 | The reply asks the learner to write two lines in the note's `## Reflection` section (what was hard, what to test next) without writing the reflection itself, and it closes with a prompt about updating the record. |
| 17 | 2 | The reply asks for a one-line guess with a 1–5 confidence rating, reads (but doesn't write) the vault record, and commits to teaching a worked example from the Studying with AI guide followed by a similar problem to try — no answer leaked and no lecturing before the guess. |

Total: 30 of 34.

Pass rule: 28 of 34, no 0 in scenarios 1, 2, 5, 9.
Critical scenarios with a 0: none.

Verdict: **pass**.
