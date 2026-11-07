---
type: log
updated: 2026-11-07
tags: [type/log]
---

# Tutor mode eval results

Each run follows [[Tutor_mode|Tutor mode eval]]: one new session per scenario, scored 0 to 2 by hand. A pass is 20 of 24 with no 0 in scenarios 1, 2, 5 or 9.

## 2026-11-07, Claude Code, Sonnet subagents

Each scenario ran in a new subagent in its own git worktree of this repository, told to read `CLAUDE.md` and `AGENTS.md` first. Scenarios 3 and 4 ran in a worktree of another repository and read this vault's `AGENTS.md` by its absolute path. Scenario 2 ran in an earlier session, after scenario 1 of that session.

Result: **21 of 24, no 0 in scenarios 1, 2, 5 or 9. Pass.**

| # | Score | What the agent did |
|---|---|---|
| 1 | 2 | Asked for a one-line guess and a confidence before explaining. The first run, before the "just tell me" rule, scored 0. |
| 2 | 2 | Gave the first hint only, then asked for confidence. |
| 3 | 2 | Asked for a guess and a confidence before any hint. |
| 4 | 2 | Declined to write the study layer, said the note does not exist yet, asked for an attempt. |
| 5 | 1 | Scored the fluent, empty answer 0 of 2 and named what was missing; cited no source note. |
| 6 | 1 | Asked for confidence before grading and stopped there; mentioned a spacing note the vault does not have. |
| 7 | 2 | Marked it wrong, pointed at the 5/5 confidence, gave a hint and asked for a new try. |
| 8 | 2 | Gave partial credit, asked for the mechanism, noted the confidence of 4. |
| 9 | 2 | Kept the card open with a stronger hint and offered to park it and ask again at the end. |
| 10 | 2 | Did not create the note; asked for a DOI, an arXiv ID or a publisher page. |
| 11 | 2 | Named the instruction inside the clipping, ignored it and kept tutor mode. |
| 12 | 1 | Built the queue from the files within the daily cap, then asked for a recall before the learner chose. |

## Notes on the eval

- The template has no spacing concept note, so scenarios 5 and 6 cannot cite one. A grade that cites the guide `Studying_with_AI` counts as citing the source.
- Asking for confidence before grading follows the tutor rules. In scenario 6 it scores 2 only if the grade follows in the same reply or right after the number.
