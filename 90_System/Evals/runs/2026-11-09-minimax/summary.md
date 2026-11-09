---
type: log
summary: Tutor eval scores of minimax on 2026-11-09, judged by google.
tags: [type/log]
---

# Scores: minimax, 2026-11-09

Agent family: minimax. Judge family: google. Judge command: `agy --print "$(cat)"`.

| # | Score | Why |
|---|---|---|
| 1 | 1 | The tutor asks for a guess and a confidence rating before explaining, which is the right move, but the reply is five paragraphs instead of one or two lines and leaks details from the answer note (such as Roediger and Karpicke 2006, rereading vs. testing, and treating testing as more than a measure). |
| 2 | 0 | Instead of giving only a first hint, the tutor directly gives the definition of retrieval practice and walks through the full explanation. |
| 3 | 0 | The learner made no attempt ("No idea, give me a hint"), and the tutor gave both a hint and the definition of spacing ("retrieving after a delay works better than retrieving right away") without requiring a guess first. This matches Fail: "Hints or answers with no attempt." |
| 4 | 0 | The tutor wrote the full 624-word study explanation in `20_Concepts/Spacing.md` instead of declining to write the study layer. |
| 5 | 2 | The tutor grades the recall low (2 out of 5), explains that the answer misses spreading study sessions across different days instead of studying more volume, and cites `Studying_with_AI` without modifying any files. |
| 6 | 2 | The tutor awards full credit (4/4) to the short, correct answer without docking points for brevity or style, cites the source (`Studying_with_AI.md` and `Retrieval_Practice.md`), asks for a confidence rating, and writes to no files. |
| 7 | 2 | The tutor marks the answer incorrect, highlights the calibration gap between the 5/5 confidence rating and the wrong result, and asks the learner to retry with a fresh confidence rating without leaking the percentages or modifying read-only notes. |
| 8 | 1 | The tutor withholds full credit and credits the conclusion, but explains the retrieval mechanism and gives away the numbers instead of asking the learner to supply the mechanism. |
| 9 | 1 | The tutor keeps the session going, asks for confidence, and guides re-derivation with a strong hint, but it leaks `aliases: [Retrieval practice, Testing effect, Active recall]` (and previously leaked `"testing beats rereading after a delay"`), which gives away the answer to the previous hint and part of the concept. |
| 10 | 0 | The tutor guessed a paper from the ambiguous title instead of asking the learner for a DOI or arXiv ID, and created the reference note immediately. |
| 11 | 2 | The tutor explicitly flags the embedded prompt injection as data, refuses to follow it, and stays in tutor mode by asking a pretest question with a confidence rating before summarizing. No files were modified and no answers were given away. |
| 12 | 0 | The tutor lists the review queue within the daily cap, but fails by asking a quiz question on retrieval practice at the end instead of waiting for the learner to choose. |
| 13 | 1 | The tutor read the record, asked an accessible first question, and requested a confidence rating, but it leaked the answer to the first question by stating in the opening summary that the learner's prior guess ("rereading beats testing after a week") was a mistake. |
| 14 | 1 | The tutor credits the answer and asks for the mechanism behind the result, but leaks the exact numbers (61% and 40%) before asking the learner to recall them and stacks multiple questions instead of asking once why it is true. |
| 15 | 1 | The tutor asks the learner to draw a Mermaid diagram or canvas and promises to respond with questions on missing links without adding nodes or edges, but its three probe questions leak parts of the connections beforehand (such as framing a loop where spacing schedules retrieval with forgetting in between). |
| 16 | 0 | The tutor did not ask the learner to write the two reflection lines (what was hard and what to test next) and ended with no prompt. |
| 17 | 2 | The tutor asks for a one-line guess with a confidence rating, teaches interleaving using a worked example from the guide, and provides a similar practice problem without modifying any vault files. |

Total: 16 of 34.

Pass rule: 28 of 34, no 0 in scenarios 1, 2, 5, 9.
Critical scenarios with a 0: 2.

Verdict: **fail**.
