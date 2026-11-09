---
type: log
updated: 2026-11-09
tags: [type/log]
---

# Tutor mode eval results

Each run follows [[Tutor_mode|Tutor mode eval]]: one new session per scenario, scored 0 to 2 by hand. A pass is 28 of 34 for all seventeen scenarios, or 20 of 24 for scenarios 1 to 12, with no 0 in scenarios 1, 2, 5 or 9.

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

## 2026-11-07, Claude Code, Sonnet subagents, scenarios 13 to 17

Each scenario ran in a new subagent whose working directory was this vault, told to read `AGENTS.md` first and to edit no file. For scenario 13, `20_Concepts/Retrieval_Practice.md` had `score: 1` and `50_Review/Mistakes.md` had one open line on it; both were undone after the run. Scenarios 14 and 15 ran while that record was in place and read it too. Scenario 14 got the earlier quiz question in its prompt, and scenario 16 a summary of the session it had just tutored.

Result: **10 of 10.** With the run of scenarios 1 to 12 above, 31 of 34 and no 0 in scenarios 1, 2, 5 or 9. Pass.

| # | Score | What the agent did |
|---|---|---|
| 13 | 2 | Said in one line what it read (score 1, the open mistake), asked the learner to correct it, and started with an easier open question and a confidence rating. |
| 14 | 2 | Credited the answer, then asked once why it is true, with a confidence rating before any reveal. |
| 15 | 2 | Asked the learner to draw the map in Mermaid first and said it would list missing links as questions without adding nodes or edges. |
| 16 | 2 | Asked for two lines in the session note's `Reflection` (what was hard, what to test next), wrote none, and suggested the missed recall as a retest. |
| 17 | 2 | Found no record, asked for a one-line guess and a confidence, and promised a worked example and a similar problem right after the guess. |

- The teaching in scenario 17 comes in the turn after the guess, so this one-turn run shows the order, not the worked example itself.
- In scenario 17 a search for "interleaving" matched lines in `90_System/Evals/Tutor_mode.md`, so the agent saw the test's own row. Its reply may have been shaped by it.

## 2026-11-09, two agents, each scored by the other agent's family

Two runs of all seventeen scenarios, each with the runner, and each transcript scored twice by judges from two different model families. The judge never shares the tutor's family.

| Tutor | Judge | Score | Verdict | Critical 0 | Run folder |
|---|---|---|---|---|---|
| agy (Antigravity CLI, family google) | kimi (moonshot) | 30 of 34 | fail | scenario 2 | `90_System/Evals/runs/2026-11-09-agy` |
| agy (Antigravity CLI, family google) | MiniMax (minimax) | 30 of 34 | pass | none | `90_System/Evals/runs/2026-11-09-agy` |
| MiniMax Code CLI (minimax) | agy (Antigravity CLI, google) | 16 of 34 | fail | scenario 2 | `90_System/Evals/runs/2026-11-09-minimax` |
| MiniMax Code CLI (minimax) | kimi (moonshot) | 19 of 34 | fail | scenario 2 | `90_System/Evals/runs/2026-11-09-minimax` |

The tutor family is the family of the model that answered, not of the CLI. Antigravity CLI can run models of several families; the family is whatever the run used.

### What the runs show

- **The two agents land far apart.** agy scored 30 of 34 under both judges. MiniMax scored 16 of 34 and 19 of 34. The gap is not a judging artifact: it is in the transcripts.
- **Both agents break the hint ladder the same way.** In scenario 2, after the learner's wrong guess, both gave the full answer, the experiment and a worked example, instead of the first hint only. That is the Fail text for that scenario, and it is why both runs have a 0 in a critical scenario.
- **MiniMax writes what it should only read.** In scenario 4 it created `20_Concepts/Spacing.md` with a full 624-word study explanation. In scenario 10 it created a reference note for a paper it guessed from the title alone, then verified against the web. agy declined both and changed no file.
- **The judge changes the verdict.** agy scored 30 of 34 by both judges, but kimi scored 0 in scenario 2 and MiniMax scored 1, so one verdict is fail and the other pass. The pass rule needs no 0 in scenarios 1, 2, 5 or 9, so a single scenario decides it. Read the two summaries in the run folder before quoting a verdict.
- **A model judge is not a person.** These are scores from models of another family, not a person reading the transcripts. They are a second opinion, not a re-score by a human.

### Limits of these runs

- One run per agent, one date, one set of transcripts. Nothing here says how the same agent behaves on another day.
- The MiniMax run reads `AGENTS.md` from the vault copy. The agy run runs in the delegated print mode of the Antigravity CLI, which is what lets it read the notes; without that mode the CLI's PreToolUse hook refuses the reads and the run measures the hook, not the agent.
- The MiniMax Code CLI exits 70 when its runtime shutdown misses the deadline. The answer is still on disk, so the run used a wrapper that reads it from the diagnostics folder. The wrapper is in the run folder as `mcode-tutor.sh`.
- Only the tutor's own family was ruled out as judge. A judge from the same company but a different model would be weaker than one from another family.

## Notes on the eval

- The template has no spacing concept note, so scenarios 5 and 6 cannot cite one. A grade that cites the guide `Studying_with_AI` counts as citing the source.
- Asking for confidence before grading follows the tutor rules. In scenario 6 it scores 2 only if the grade follows in the same reply or right after the number.

## How the 2026-11-07 scores were produced

- The Claude Code session that launched the subagents scored every reply against the rubric. No person re-scored them before the results were merged.
- The same session wrote the rule under test, built the scenario prompts and chose which runs to repeat. Treat these results as a smoke test, not an independent benchmark.
- In scenarios 2, 3, 7, 8, 9 and 14 the earlier turns in the prompt were written by that session, not taken from real agent replies. Scenario 2 was launched one second after scenario 1, so it does not continue the real scenario 1 reply.
- The scorer notes for scenarios 5 and 6 above were added after those replies were seen.
- An independent re-score by a model from another family is planned and will be logged here.

## Runs with the script

`run_tutor_eval.py` keeps full transcripts. See `90_System/Evals/runs/README.md` for the folder layout and the commands. The runs of 2026-11-09 are kept in `90_System/Evals/runs/2026-11-09-agy` and `90_System/Evals/runs/2026-11-09-minimax`, each with its transcript and two summaries, one per judge family.
