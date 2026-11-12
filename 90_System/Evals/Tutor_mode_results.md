---
type: log
updated: 2026-11-12
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

### Uncertainty, judge agreement and checks

The same scores, recomputed by `run_tutor_eval.py --summarize` with no new model call. The interval is the middle 95% of 10000 bootstrap totals over the 17 scenarios, seed 20261109.

| Tutor | Judge | Score | 95% interval | Verdict of the judge |
|---|---|---|---|---|
| agy | kimi | 30 of 34 | 25 to 34 | fail |
| agy | MiniMax | 30 of 34 | 26 to 33 | pass |
| MiniMax | agy | 16 of 34 | 10 to 23 | fail |
| MiniMax | kimi | 19 of 34 | 12 to 26 | fail |

| Run | Percent agreement | Cohen's kappa | Weighted kappa | Krippendorff's alpha (ordinal, nominal) | Verdict of the run |
|---|---|---|---|---|---|
| `2026-11-09-agy` | 0.7647 | 0.3131 | 0.5072 | 0.5024, 0.3231 | **contested** |
| `2026-11-09-minimax` | 0.7059 | 0.5641 | 0.8019 | 0.8039, 0.5669 | fail |

- **The agy verdict is contested.** The two judges give the same total and split on pass and fail, and the pass mark 28 is inside both intervals. Quote it as "30 of 34, contested", not as a pass or a fail.
- **Paired difference under one judge family.** `--compare` of `2026-11-09-agy/scores.json` and `2026-11-09-minimax/scores-judge-kimi.json`, both judged by kimi: agy minus MiniMax is 11 points over 17 scenarios, 95% interval 3 to 19; agy higher in 7 scenarios, MiniMax higher in 1, the same in 9. It is one run of each agent, and neither run recorded the version hashes, so the comparison assumes both used the same scenarios, rubric and judge prompt. The scenario file did not change between the two runs.
- **Checks without a model.** The agy run passes every check. The MiniMax run fails the write check in scenario 4 (`20_Concepts/Spacing.md`, the course note and a session note), scenario 10 (`40_References/Papers/Adaptive_Memory_Replay_(Smith_et_al.,_2024).md`) and scenario 16 (`50_Review/Daily/2026-11-09.md` and `50_Review/Mistakes.md`). Its quiz files in `50_Review/Quizzes/` were asked for and pass. The checks are shown next to the scores and do not change them.
- **No person labeled the transcripts.** Every score here comes from a model judge.

### Limits of these runs

- One run per agent, one date, one set of transcripts. Nothing here says how the same agent behaves on another day.
- The MiniMax run reads `AGENTS.md` from the vault copy. The agy run runs in the delegated print mode of the Antigravity CLI, which is what lets it read the notes; without that mode the CLI's PreToolUse hook refuses the reads and the run measures the hook, not the agent.
- The MiniMax Code CLI exits 70 when its runtime shutdown misses the deadline. The answer is still on disk, so the run used a wrapper that reads it from the diagnostics folder. The wrapper is `90_System/Evals/mcode-tutor.sh`.
- Only the tutor's own family was ruled out as judge. A judge from the same company but a different model would be weaker than one from another family.

## 2026-11-12, three agents, three repeats each, two judges of other families

Each agent ran the seventeen scenarios three times with the runner, each repeat in its own folder, and each transcript was scored by two judges, neither of the agent's family. Every number below was printed by `run_tutor_eval.py --summarize` and `--aggregate`. No person labeled the transcripts: every score comes from a model judge.

| Tutor (family, model) | Judges | Run folders |
|---|---|---|
| Claude Code (anthropic, claude-opus-5-5) | Codex (openai, gpt-6.1-sol) in `scores.json`; GLM (zhipu, glm-5.3) in `scores-judge-zhipu-glm.json` | `90_System/Evals/runs/2026-11-12-claude-r1` to `-r3` |
| Codex CLI (openai, gpt-6.1-sol) | Claude (anthropic, claude-opus-5-5) in `scores.json`; GLM (zhipu, glm-5.3) in `scores-judge-zhipu-glm.json` | `2026-11-12-codex-r1` to `-r3` |
| GLM through Claude Code (zhipu, glm-5.3) | Claude (anthropic, claude-opus-5-5) in `scores.json`; Codex (openai, gpt-6.1-sol) in `scores-judge-openai.json` | `2026-11-12-glm-r1` to `-r3` |

Antigravity and Kimi did not run: Antigravity refused for quota (the CLI answered RESOURCE_EXHAUSTED), and Kimi was skipped because its monthly quota was used up. MiniMax started three repeats of each benchmark and was stopped when its weekly quota ran out (the CLI answered "Token Plan usage limit reached"); its partial runs are not kept.

### Totals of the three repeats

| Tutor | Judge | Repeats (of 34) | Mean | Standard deviation | Verdicts |
|---|---|---|---|---|---|
| Claude Code | Codex | 15, 14, 15 | 14.67 | 0.58 | fail 3 |
| Claude Code | GLM | 23, 25, 24 | 24.0 | 1.0 | fail 3 |
| Codex | Claude | 25, 25, 22 | 24.0 | 1.73 | fail 3 |
| Codex | GLM | 23, 23, 24 | 23.33 | 0.58 | fail 3 |
| GLM | Claude | 24, 22, 19 | 21.67 | 2.52 | fail 3 |
| GLM | Codex | 16, 14, 15 | 15.0 | 1.0 | fail 3 |

Every run fails: no total reaches 28, and no judge gave a pass.

| Tutor | Judge | pass^1 | pass^2 | pass^3 | Critical scenarios with no 0, k = 1, 2, 3 |
|---|---|---|---|---|---|
| Claude Code | Codex | 0.2353 | 0.1961 | 0.1765 | 0.75, 0.75, 0.75 |
| Claude Code | GLM | 0.549 | 0.4902 | 0.4706 | 0.75, 0.75, 0.75 |
| Codex | Claude | 0.4706 | 0.4314 | 0.4118 | 1.0, 1.0, 1.0 |
| Codex | GLM | 0.4706 | 0.4314 | 0.4118 | 0.9167, 0.8333, 0.75 |
| GLM | Claude | 0.4314 | 0.3333 | 0.2941 | 0.75, 0.75, 0.75 |
| GLM | Codex | 0.2157 | 0.1373 | 0.1176 | 0.6667, 0.5833, 0.5 |

pass^k is the chance that k repeats drawn from the three all score 2 on a scenario, averaged over the seventeen.

### Judges of each run

| Run | Judge A, total and 95% interval | Judge B, total and 95% interval | Percent | Kappa | Weighted kappa | Alpha ordinal, nominal |
|---|---|---|---|---|---|---|
| claude-r1 | Codex 15 (8 to 22) | GLM 23 (17 to 28) | 0.5882 | 0.405 | 0.3166 | 0.2874, 0.3937 |
| claude-r2 | Codex 14 (8 to 20) | GLM 25 (19 to 30) | 0.5294 | 0.3366 | 0.3417 | 0.2615, 0.3034 |
| claude-r3 | Codex 15 (9 to 21) | GLM 24 (17 to 30) | 0.5294 | 0.3462 | 0.2494 | 0.1728, 0.2997 |
| codex-r1 | Claude 25 (21 to 29) | GLM 23 (17 to 28) | 0.7647 | 0.5802 | 0.6762 | 0.7476, 0.5875 |
| codex-r2 | Claude 25 (20 to 30) | GLM 23 (18 to 28), 16 scored | 0.9375 | 0.8865 | 0.9167 | 0.898, 0.8897 |
| codex-r3 | Claude 22 (17 to 27) | GLM 24 (19 to 29) | 0.8235 | 0.6946 | 0.5678 | 0.5952, 0.7027 |
| glm-r1 | Claude 24 (18 to 29) | Codex 16 (11 to 21) | 0.6471 | 0.4742 | 0.3625 | 0.2878, 0.45 |
| glm-r2 | Claude 22 (16 to 27) | Codex 14 (8 to 20) | 0.5882 | 0.3802 | 0.1905 | 0.1269, 0.3723 |
| glm-r3 | Claude 19 (13 to 25) | Codex 15 (8 to 22) | 0.6471 | 0.4796 | 0.466 | 0.4706, 0.4857 |

No run is contested: both judges fail every run. In `codex-r2` the GLM judge gave no score for one scenario, so its total is over 16 scenarios.

### What these runs show

- **The judge moves the total more than the repeat does.** Claude Code scored 14 to 15 under the Codex judge and 23 to 25 under the GLM judge, on the same transcripts. GLM as tutor scored 14 to 16 under Codex and 19 to 24 under Claude. Across the repeats, the standard deviation is at most 2.52 points; between the two judges of one run, the gap reaches 11 points.
- **The Codex judge is the strict one.** It gave the two lowest means (14.67 for Claude Code, 15.0 for GLM). The agreement of Codex with the other judges is low: kappa 0.3366 to 0.4796. The two judges of the Codex runs, Claude and GLM, agree more: kappa 0.5802 to 0.8865.
- **Only Codex as tutor kept every critical scenario above 0 under one judge.** Under the Claude judge it scored no 0 in scenarios 1, 2, 5 or 9 in all three repeats. Under GLM, one repeat had a 0 there.
- **The checks found no forbidden write.** No tutor wrote in `10_Tracks/`, `20_Concepts/` or `50_Review/`, and every scenario 2 reply asked for a confidence.
- **The kappa readings are below the gate.** Of nine judge pairs, one (codex-r2, 0.8865) reaches the 0.80 that this vault treats as strong enough to gate a run. A verdict here is the verdict of a judge, and the low agreement says the rubric leaves room for two readings.

### Limits of these runs

- Three repeats per agent, one day, one machine. Each repeat is a fresh copy of the vault, so the repeats share no memory of each other.
- Claude Code and GLM ran with `--setting-sources project,local`, which leaves out the user hooks and settings of the machine. The user memory files (`~/.claude/CLAUDE.md` and its rules) still load, and they hold instructions for this machine's development work, not for tutoring. Codex ran with the user configuration of the machine. The tutors and the judges are the CLIs as installed here, not bare models.
- The judges are models. No person read the transcripts to check a score.

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
