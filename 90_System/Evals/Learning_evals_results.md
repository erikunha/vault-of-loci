---
type: log
updated: 2026-11-13
tags: [type/log]
---

# Learning eval results

Each run follows [[Learning_evals|Learning eval]]: the agent answers a learner's question using the vault's own record, and a judge from another model family scores the reply from 0 to 2 against the rubric. The critical group is scenarios 1, 2, 3, 10 and 11, and the pass rule for that group is 8 of 10 with no 0 in any of them. The rule for a run of the whole benchmark asks for two things at once, 24 of 30 points and 8 of 10 in the critical group, The runs of 2026-11-10 cover the critical group only, so the rule that applies to them is the 8 of 10. The runs of 2026-11-12 cover all fifteen scenarios, so the full rule applies to them.

These runs use the learning ledger as the fixture. Each scenario writes a ledger with dated events into a fresh copy of the vault, so the agent reads a record the scenario controls and the real `50_Review/Attempts.jsonl` is never touched.

## 2026-11-12, all fifteen scenarios, three agents, three repeats each

Each agent ran all fifteen scenarios three times with the runner, each repeat in its own folder, and two judges of other families scored every transcript. These are the first runs of the whole benchmark, so the rule that applies is the full one: 24 of 30 and 8 of 10 in the critical group, with no 0 in scenarios 1, 2, 3, 10 or 11. Every number below was printed by `run_tutor_eval.py --summarize` and `--aggregate`. No person labeled the transcripts: every score comes from a model judge.

| Tutor (family, model) | Judges | Run folders |
|---|---|---|
| Claude Code (anthropic, claude-opus-5-5) | Codex (openai, gpt-6.1-sol) in `scores.json`; GLM (zhipu, glm-5.3) in `scores-judge-zhipu-glm.json` | `90_System/Evals/runs/2026-11-12-learning-claude-r1` to `-r3` |
| Codex CLI (openai, gpt-6.1-sol) | Claude (anthropic, claude-opus-5-5) in `scores.json`; GLM (zhipu, glm-5.3) in `scores-judge-zhipu-glm.json` | `2026-11-12-learning-codex-r1` to `-r3` |
| GLM through Claude Code (zhipu, glm-5.3) | Claude (anthropic, claude-opus-5-5) in `scores.json`; Codex (openai, gpt-6.1-sol) in `scores-judge-openai.json` | `2026-11-12-learning-glm-r1` to `-r3` |

Antigravity and Kimi did not run: Antigravity refused for quota (the CLI answered RESOURCE_EXHAUSTED), and Kimi was skipped because its monthly quota was used up. MiniMax started three repeats of each benchmark and was stopped when its weekly quota ran out (the CLI answered "Token Plan usage limit reached"); its partial runs are not kept.

| Tutor | Judge | Repeats (of 30) | Mean | Standard deviation | pass^1, pass^3 | Critical with no 0, k = 1, 3 | Verdicts |
|---|---|---|---|---|---|---|---|
| Claude Code | Codex | 15, 15, 14 | 14.67 | 0.58 | 0.3556, 0.2 | 0.8, 0.4 | fail 3 |
| Claude Code | GLM | 20, 23, 19 | 20.67 | 2.08 | 0.5111, 0.4 | 1.0, 1.0 | fail 3 |
| Codex | Claude | 11, 13, 14 | 12.67 | 1.53 | 0.2222, 0.1333 | 0.6, 0.6 | fail 3 |
| Codex | GLM | 17, 16, 18 | 17.0 | 1.0 | 0.3556, 0.2 | 0.8, 0.8 | fail 3 |
| GLM | Claude | 11, 16, 12 | 13.0 | 2.65 | 0.2667, 0.1333 | 0.6667, 0.6 | fail 3 |
| GLM | Codex | 10, 10, 9 | 9.67 | 0.58 | 0.1333, 0.0667 | 0.5333, 0.4 | fail 3 |

| Run | Judge A, total and 95% interval | Judge B, total and 95% interval | Percent | Kappa | Weighted kappa | Alpha ordinal, nominal |
|---|---|---|---|---|---|---|
| learning-claude-r1 | Codex 15 (9 to 21) | GLM 20 (15 to 25) | 0.8 | 0.7 | 0.5263 | 0.547, 0.7031 |
| learning-claude-r2 | Codex 15 (8 to 22) | GLM 23 (18 to 27) | 0.6 | 0.4 | 0.4545 | 0.4788, 0.3808 |
| learning-claude-r3 | Codex 14 (8 to 21) | GLM 19 (13 to 25) | 0.8 | 0.7039 | 0.582 | 0.5901, 0.7071 |
| learning-codex-r1 | Claude 11 (6 to 16) | GLM 17 (11 to 22) | 0.6667 | 0.4932 | 0.5312 | 0.5152, 0.4948 |
| learning-codex-r2 | Claude 13 (7 to 19) | GLM 16 (10 to 22) | 0.7333 | 0.6026 | 0.6367 | 0.646, 0.612 |
| learning-codex-r3 | Claude 14 (8 to 20) | GLM 18 (12 to 24) | 0.6667 | 0.5 | 0.5652 | 0.5587, 0.5101 |
| learning-glm-r1 | Claude 11 (5 to 17) | Codex 10 (5 to 15) | 0.8667 | 0.7857 | 0.6939 | 0.7067, 0.7921 |
| learning-glm-r2 | Claude 16 (10 to 22) | Codex 10 (5 to 16) | 0.6667 | 0.513 | 0.3226 | 0.3155, 0.5101 |
| learning-glm-r3 | Claude 12 (6 to 18) | Codex 9 (4 to 15) | 0.8667 | 0.7872 | 0.6988 | 0.7067, 0.7921 |

No run is contested: both judges fail every run.

### What these runs show

- **No agent passes the learning benchmark.** The highest total is 23 of 30, by GLM judging a Claude Code repeat; the mark is 24. Every one of the eighteen judgements is a fail.
- **The judge again moves the total more than the repeat.** Claude Code is 14 to 15 under Codex and 19 to 23 under GLM. The standard deviation across the repeats is at most 2.65 points.
- **The judges agree more here than on the tutor benchmark.** Kappa runs from 0.4 to 0.7872, and no pair reaches 0.80.
- **The leak check fired on GLM as tutor.** In repeats 1 and 2, the reply to scenario 10 handed over the 61% and the 40% of the one week result, the figures the offered recall asks for. No tutor wrote a file the learner did not ask for.

### Limits of these runs

- Three repeats per agent, one day, one machine. The CLIs ran with the configuration described in the tutor results of the same day.
- The judges are models. No person read the transcripts to check a score.

## 2026-11-12, the same runs again after the tutor rules changed

The same two pull requests as in [[Tutor_mode_results|Tutor mode eval results]], #41 (d528173) and #42 (a0d504e), changed `AGENTS.md`, the `quiz` skill, and after the first rerun the `counterfactual` and `memory-palace` skills. The scenarios, the rubric, the judge prompt and the pass rule did not change; the recorded hashes match and `--compare` accepted every pair. Claude Code, Codex and GLM ran all fifteen scenarios three times after each change, with the same commands, flags and judges as the first runs. The folders are `90_System/Evals/runs/2026-11-12-learning-<agent>-v2-r<n>` (after #41) and `-v3-r<n>` (after #42). Every total, interval, kappa and pass^k was printed by `run_tutor_eval.py`. The per-scenario table is the plain average of the scores in the summaries. No person labeled the transcripts.

### What the losses were

The scenarios with the lowest mean were 4 (0.06 of 2), 7 (0.17), 3 (0.33), 12 (0.50), 2 (0.72) and 8 (0.94). Two causes explain most of them:

- **The record was not read.** Codex answered "the record is empty" on a ledger with three wrong attempts (4), three clean recalls (3) and two wrong attempts on one item (7), and asked the learner to paste a checklist that the track holds (12). `AGENTS.md` named the concept note and `Mistakes.md` as the record, and not `50_Review/Attempts.jsonl`.
- **The skills that hold the steps never started.** They write files, so agents do not start them on their own: `misconception-drill` (4), `error-recovery` (7), `retention-audit` (2), `dependency-check` (8), `memory-palace` (12). Without the steps, agents repeated the studied question (2, 3, 4, 7) or started Beta (8).

### Totals of the three repeats

| Tutor | Judge | Version | Repeats (of 30) | Mean | Standard deviation | Verdicts | pass^1, pass^3 | Critical with no 0, k = 1, 3 |
|---|---|---|---|---|---|---|---|---|
| Claude Code | Codex | before | 15, 15, 14 | 14.67 | 0.58 | fail 3 | 0.3556, 0.2 | 0.8, 0.4 |
| Claude Code | Codex | after #41 | 21, 18, 17 | 18.67 | 2.08 | fail 3 | 0.5111, 0.4667 | 0.8, 0.6 |
| Claude Code | Codex | after #42 | 21, 20, 21 | 20.67 | 0.58 | fail 3 | 0.5778, 0.4667 | 0.8667, 0.8 |
| Claude Code | GLM | before | 20, 23, 19 | 20.67 | 2.08 | fail 3 | 0.5111, 0.4 | 1.0, 1.0 |
| Claude Code | GLM | after #41 | 28, 26, 25 | 26.33 | 1.53 | pass 3 | 0.8, 0.7333 | 1.0, 1.0 |
| Claude Code | GLM | after #42 | 28, 24, 27 | 26.33 | 2.08 | incomplete 1, pass 2 | 0.8444, 0.7333 | 1.0, 1.0 |
| Codex | Claude | before | 11, 13, 14 | 12.67 | 1.53 | fail 3 | 0.2222, 0.1333 | 0.6, 0.6 |
| Codex | Claude | after #41 | 22, 23, 19 | 21.33 | 2.08 | fail 3 | 0.5778, 0.5333 | 1.0, 1.0 |
| Codex | Claude | after #42 | 24, 20, 22 | 22.0 | 2.0 | fail 2, pass 1 | 0.5778, 0.4 | 1.0, 1.0 |
| Codex | GLM | before | 17, 16, 18 | 17.0 | 1.0 | fail 3 | 0.3556, 0.2 | 0.8, 0.8 |
| Codex | GLM | after #41 | 25, 23, 25 | 24.33 | 1.15 | fail 1, pass 2 | 0.6222, 0.5333 | 1.0, 1.0 |
| Codex | GLM | after #42 | 21, 25, 27 | 24.33 | 3.06 | fail 1, pass 2 | 0.7333, 0.5333 | 1.0, 1.0 |
| GLM | Claude | before | 11, 16, 12 | 13.0 | 2.65 | fail 3 | 0.2667, 0.1333 | 0.6667, 0.6 |
| GLM | Claude | after #41 | 26, 24, 21 | 23.67 | 2.52 | fail 1, pass 2 | 0.6667, 0.4667 | 0.9333, 0.8 |
| GLM | Claude | after #42 | 23, 23, 23 | 23.0 | 0.0 | fail 2, incomplete 1 | 0.7111, 0.5333 | 0.8, 0.6 |
| GLM | Codex | before | 10, 10, 9 | 9.67 | 0.58 | fail 3 | 0.1333, 0.0667 | 0.5333, 0.4 |
| GLM | Codex | after #41 | 20, 19, 19 | 19.33 | 0.58 | fail 3 | 0.5333, 0.2667 | 0.7333, 0.6 |
| GLM | Codex | after #42 | 19, 18, 19 | 18.67 | 0.58 | fail 3 | 0.5333, 0.3333 | 0.7333, 0.4 |

A run passes only when every judge passes it. No run passed under both judges, in any of the three sets. Where the verdict says "incomplete", a scenario has no score from a judge or the agent run failed (see the limits).

### Judges of each run

After #41:

| Run | Judge A, total and 95% interval | Judge B, total and 95% interval | Percent | Kappa | Weighted kappa | Alpha ordinal, nominal | Verdict of the run |
|---|---|---|---|---|---|---|---|
| learning-claude-v2-r1 | Codex 21 (15 to 27) | GLM 28 (25 to 30) | 0.6667 | 0.2647 | 0.2466 | 0.289, 0.2408 | contested |
| learning-claude-v2-r2 | Codex 18 (11 to 24) | GLM 26 (21 to 30) | 0.6667 | 0.4186 | 0.2857 | 0.2475, 0.3933 | contested |
| learning-claude-v2-r3 | Codex 17 (10 to 24) | GLM 25 (20 to 29) | 0.6667 | 0.4403 | 0.3438 | 0.3556, 0.4246 | contested |
| learning-codex-v2-r1 | Claude 22 (16 to 27) | GLM 25 (21 to 28) | 0.8667 | 0.7391 | 0.5714 | 0.7546, 0.7445 | contested |
| learning-codex-v2-r2 | Claude 23 (18 to 27) | GLM 23 (19 to 27) | 0.8667 | 0.7458 | 0.7887 | 0.8561, 0.7511 | fail |
| learning-codex-v2-r3 | Claude 19 (12 to 25) | GLM 25 (21 to 28) | 0.6667 | 0.4231 | 0.52 | 0.6406, 0.4153 | contested |
| learning-glm-v2-r1 | Claude 26 (21 to 30) | Codex 20 (13 to 26) | 0.6 | 0.1743 | 0.3571 | 0.2947, 0.1675 | contested |
| learning-glm-v2-r2 | Claude 24 (19 to 28) | Codex 19 (13 to 25) | 0.8 | 0.6591 | 0.4444 | 0.4937, 0.6615 | contested |
| learning-glm-v2-r3 | Claude 21 (15 to 26) | Codex 19 (12 to 25) | 0.8 | 0.6739 | 0.6809 | 0.7102, 0.6801 | fail |

After #42:

| Run | Judge A, total and 95% interval | Judge B, total and 95% interval | Percent | Kappa | Weighted kappa | Alpha ordinal, nominal | Verdict of the run |
|---|---|---|---|---|---|---|---|
| learning-claude-v3-r1 | Codex 21 (15 to 26) | GLM 28 (24 to 30) | 0.6 | 0.1892 | 0.3836 | 0.1282, 0.089 | contested |
| learning-claude-v3-r2 | Codex 20 (13 to 26) | GLM 24 (19 to 28), 14 scored | 0.7143 | 0.44 | 0.4531 | 0.4841, 0.4346 | incomplete |
| learning-claude-v3-r3 | Codex 21 (15 to 27) | GLM 27 (22 to 30) | 0.6667 | 0.2647 | 0.5122 | 0.4194, 0.2448 | contested |
| learning-codex-v3-r1 | Claude 24 (19 to 28) | GLM 21 (15 to 26), 14 scored | 0.7143 | 0.4455 | 0.4615 | 0.4306, 0.4627 | contested |
| learning-codex-v3-r2 | Claude 20 (14 to 26) | GLM 25 (20 to 29) | 0.6 | 0.2623 | 0.449 | 0.3837, 0.2658 | contested |
| learning-codex-v3-r3 | Claude 22 (17 to 26) | GLM 27 (22 to 30) | 0.5333 | 0.0789 | -0.1017 | -0.1104, 0.0 | contested |
| learning-glm-v3-r1 | Claude 23 (17 to 28) | Codex 19 (12 to 25), 14 scored | 0.8571 | 0.6818 | 0.5912 | 0.6207, 0.686 | fail |
| learning-glm-v3-r2 | Claude 23 (17 to 28) | Codex 18 (11 to 24), 14 scored | 0.7857 | 0.5714 | 0.5468 | 0.5313, 0.5714 | fail |
| learning-glm-v3-r3 | Claude 23 (18 to 27) | Codex 19 (13 to 24), 14 scored | 0.7857 | 0.6147 | 0.5579 | 0.5536, 0.6161 | incomplete |

### Paired differences

`--compare` of the same repeat after and before, same judge file, A minus B, over the fifteen scenarios (a scenario one side did not score is left out).

After #42 minus the first runs:

| Tutor | Judge | Difference per repeat (r1, r2, r3) | 95% interval per repeat | New higher, old higher, same per repeat |
|---|---|---|---|---|
| Claude Code | Codex | 6, 5, 7 | -3 to 14; -4 to 14; -1 to 15 | 7/3/5; 5/3/7; 7/2/6 |
| Claude Code | GLM | 8, 3, 8 | 0 to 15; -5 to 10; 0 to 16 | 8/1/6; 6/3/5; 8/2/5 |
| Codex | Claude | 13, 7, 8 | 6 to 20; -1 to 15; 1 to 15 | 9/1/5; 6/3/6; 7/2/6 |
| Codex | GLM | 4, 9, 9 | -3 to 11; 2 to 16; 3 to 16 | 6/2/6; 7/1/7; 7/1/7 |
| GLM | Claude | 12, 7, 12 | 3 to 20; 1 to 13; 5 to 19 | 10/2/2; 6/1/7; 10/2/2 |
| GLM | Codex | 9, 8, 11 | 0 to 18; 0 to 16; 4 to 18 | 9/3/2; 8/2/4; 10/2/2 |

After #42 minus after #41:

| Tutor | Judge | Difference per repeat (r1, r2, r3) | 95% interval per repeat | New higher, old higher, same per repeat |
|---|---|---|---|---|
| Claude Code | Codex | 0, 2, 4 | -4 to 4; -2 to 6; 0 to 9 | 2/2/11; 3/1/11; 3/0/12 |
| Claude Code | GLM | 0, 0, 2 | -5 to 4; -6 to 5; -2 to 6 | 2/1/12; 3/2/9; 3/1/11 |
| Codex | Claude | 2, -3, 3 | -3 to 8; -10 to 4; -2 to 9 | 3/2/10; 3/6/6; 4/2/9 |
| Codex | GLM | -3, 2, 2 | -8 to 2; -5 to 8; -4 to 7 | 1/3/10; 5/2/8; 4/1/10 |
| GLM | Claude | -1, 1, 2 | -7 to 4; -3 to 5; -3 to 7 | 2/2/10; 3/2/9; 4/2/8 |
| GLM | Codex | 1, 0, 0 | -6 to 7; -7 to 7; -4 to 4 | 3/2/9; 3/3/8; 2/2/10 |

### Per scenario

Mean of the scores of three agents, two judges and three repeats (up to 18 scores per cell; a scenario a judge did not score, or an agent run that failed, is left out).

| # | Learner says | before | after #41 | after #42 |
|---|---|---|---|---|
| 1 | "Which of my topics is due for a delayed test?" | 1.44 | 1.33 | 1.19 |
| 2 | "Give me a delayed test on retrieval practice." | 0.72 | 2.00 | 2.00 |
| 3 | "Quiz me on retrieval practice." | 0.33 | 1.72 | 1.67 |
| 4 | "I keep getting retrieval practice wrong." | 0.06 | 1.78 | 1.57 |
| 5 | "Teach me retrieval practice." | 1.22 | 1.28 | 1.00 |
| 6 | "Test me on retrieval practice." | 1.33 | 2.00 | 2.00 |
| 7 | "Help me with the question I got wrong." | 0.17 | 1.56 | 1.50 |
| 8 | "Let me move on to Beta." | 0.94 | 2.00 | 2.00 |
| 9 | "What counts as passing a transfer task?" | 1.22 | 0.44 | 0.22 |
| 10 | "How much of this will I remember in a month?" | 1.56 | 1.67 | 1.89 |
| 11 | "Is my confidence telling me anything?" | 1.83 | 1.78 | 1.61 |
| 12 | "Turn this checklist into something I can remember." | 0.50 | 1.06 | 1.82 |
| 13 | "Check the diagram I drew from memory." | 1.33 | 0.94 | 1.61 |
| 14 | "What changes if the premise of this were false?" | 0.94 | 1.11 | 1.50 |
| 15 | "Say this idea in the shortest way it still holds." | 1.00 | 1.61 | 1.61 |

### What these runs show

- **Every agent and judge pair rose.** The mean total, of 30, went from 14.67 to 20.67 (Claude Code, Codex judge), 20.67 to 26.33 (Claude Code, GLM judge), 12.67 to 22.0 (Codex, Claude judge), 17.0 to 24.33 (Codex, GLM judge), 13.0 to 23.0 (GLM, Claude judge) and 9.67 to 18.67 (GLM, Codex judge). Of the 18 run verdicts by judge file, none passed before, 7 passed after #41 and 5 after #42.
- **The largest gains are the scenarios the skills carry:** 4 (0.06 to 1.57), 7 (0.17 to 1.50), 3 (0.33 to 1.67), 2 (0.72 to 2.00), 8 (0.94 to 2.00) and 12 (0.50 to 1.82).
- **Scenario 9 got worse, and the cause was the scenario.** Its setup said the objective registry holds the criterion "Apply the idea in a new case and say why it applies". The registry in `90_System/Objectives.json` holds "Choose what to do the night before a test in a new subject and say why, using the effect.", and the scenario writes nothing to it. After the rules said to quote the registry word for word, agents quoted the real one and both judges called it invented (0.44 after #41, 0.22 after #42). The setup now quotes the criterion the registry holds, and `test_learning_objectives.py` fails when a learning scenario quotes a criterion that is not in the objectives file it uses. The scenario 9 scores in these tables were taken with the old setup. Scenario 9 has not run again: on 2026-11-13 Codex refused for its weekly limit (reset 2026-11-18) and GLM for its weekly limit (reset 2026-11-19), so no tutor other than Claude Code could run and no judge of another family could score Claude Code.
- **Scenarios 1 and 5 stay near 1.** The Codex judge fails a reply that lists `retrieval-practice-apply` even as "not due", and fails a first reply that promises the worked example instead of giving it with the guess.
- **The leak check fired on GLM as tutor.** The 61% and the 40% appeared in scenarios 10 and 11 of `learning-glm-v2-r3` and in scenario 11 of `learning-glm-v3-r1`. No tutor wrote a file the learner did not ask for.
- **The gains after #42 are inside the noise.** The difference of a repeat against the same repeat after #41 runs from -3 to +4 points, and every interval includes zero.

### Limits of these runs

- **The rules were written after reading these scenarios.** The gain is the repair of known failures, not evidence for scenarios nobody has written yet.
- Three repeats per agent, one day, one machine, the CLIs as installed.
- The GLM tutor failed to answer one scenario in each of the three repeats after #42 (scenario 4 in `learning-glm-v3-r1` and `-r2`, scenario 1 in `-r3`): the CLI exited with code 1. Those runs have 14 of 15 scenarios scored under both judges, and their totals are over 14.
- The GLM judge gave no score to scenario 6 of `learning-claude-v3-r2` and to scenario 12 of `learning-codex-v3-r1`.
- Antigravity, MiniMax and Kimi did not run, for the reasons given in the tutor results.
- The judges are models. No person read the transcripts to check a score.

## 2026-11-10, MiniMax Code CLI, Claude as the judge

The agent was the MiniMax Code CLI through the wrapper `mcode-tutor.sh`, and the judge was Claude (`claude -p`). The agent family is minimax and the judge family is anthropic, so the judge never shared a family with the agent.

Result: **6 of 10, with a 0 in scenario 3. Fail.** The rule needs 8 of 10 and no 0 in the critical group, so scenario 3 decides the verdict on its own.

| # | Score | Judge agreed | What the agent did |
|---|---|---|---|
| 1 | 2 | 3 of 3 | Named `retrieval-practice-recall` as the one due, said the delay is 90 days, gave the new item id `retrieval-practice-recall-d90`, and said the delay arrived but the retention at that horizon is still unknown. It also named the objective registered with no attempt, which the old run never mentioned. |
| 2 | 2 | 3 of 3 | Wrote a new task on the item id `retrieval-practice-recall-d30`, asked for a closed book attempt, and asked for a confidence before any reveal. |
| 3 | 0 | 2 of 3 | Built a quiz of eight questions. It asked again what testing is for besides measuring learning, which the learner had already recalled three times, and it never said what counts as applying the idea. |
| 10 | 1 | 3 of 3 | Said nobody has measured it, said a forecast is not a measurement, and offered the delayed 30 day assessment. It loses the point for handing over the 61% against 40% figures the assessment asks the learner to recall. |
| 11 | 1 | 3 of 3 | Read the ledger, gave the confidence against result table, named the two sure-and-wrong attempts and the Brier score of 0.508, and asked for a percent. It loses the point for quoting the one week result just before offering the closed book question that asks for it. |

The run folder is `90_System/Evals/runs/2026-11-10-learning-minimax-learning-v2`, with the transcript, the scores and the summary.

### What changed against the first run

The first run of this benchmark scored 5 of 10 and never finished scenario 1, so it was compared twice: with the old transcripts and the old rubric, and with the old transcripts and the new rubric. Both halves of the comparison have a file behind them. The first is `runs/2026-11-10-learning-minimax-learning/scores.json`: one judgement per scenario, with the judge prompt of that moment. The second is `runs/2026-11-10-learning-minimax-learning-rescored/scores.json`: the same transcripts, scored again with the prompt and the scenarios of the current benchmark, three judgements per scenario.

| Run | 1 | 2 | 3 | 10 | 11 | Total |
|---|---|---|---|---|---|---|
| First run, old rubric | not scored | 2 | 0 | 1 | 2 | 5 of 10 |
| First run, new rubric | not scored | 2 | 0 | 1 | 1 | 4 of 10 |
| This run, new rubric | 2 | 2 | 0 | 1 | 1 | 6 of 10 |

Reading the table:

- **The rubric change lowered one score on the same transcripts.** Scenario 11 was 2 under the old rubric and 1 under the new one, on the same reply. The judge that scored it again named the rule that decided it: just before the recall question, the reply quotes the note saying rereading "fools you", which gives away which group came out ahead. The old prompt had no rule against handing over what the learner was supposed to produce, so the old judgement read the reply as clean. The new prompt has one, and the judge applied it on all three judgements. This is a fairer reading of the same behaviour, not a different behaviour. The reply of this run leaked in another way: it gave the one week result itself, the 61% against 40%, and lost the point for that. The reply of the first run never gave those numbers.
- **The product change moved scenario 1 from missing to 2.** The first run never finished scenario 1: the agent run timed out, there is no score for it, and that is why the table above says "not scored". The retry of that scenario, in `runs/2026-11-10-learning-minimax-learning-s1-fixed`, is the one the judge scored 0: the reply answered the question with the review plan, which lists the apply items, and the rubric asks for the 90 day recall item. Three changes fixed that: the audit now says a horizon that has not arrived is not due, `AGENTS.md` and the two skills now say which script answers which question, and the audit names the objectives that are registered with no event at all. The agent now answers with the audit and names the right objective, the right horizon and the right new item id.
- **Scenario 3 is still 0.** It was 0 under both rubrics and on both transcripts. The judge agreed on 0 in the three judgements of the re-scored transcript, and on the transcript of this run it gave 0 twice and 1 once. The agent builds a quiz that asks again what the learner has already shown, and it does not say what counts as applying the idea. Nothing in the product changed this, and the rubric was not loosened to move it.

### Two judges on the same run

The same run was scored twice, by two different Claude models. Codex had no quota until 2026-11-11, Kimi's monthly quota was spent and Antigravity was rate limited, so the two judges are both from the anthropic family. The scores of the first judge are in `scores.json` and the scores of the second in `scores-judge-anthropic-sonnet.json`, next to them in the run folder.

| Scenario | Judge A (opus) | Judge B (sonnet) | Same |
|---|---|---|---|
| 1 | 2 | 2 | yes |
| 2 | 2 | 2 | yes |
| 3 | 0 | 0 | yes |
| 10 | 1 | 1 | yes |
| 11 | 1 | 1 | yes |

Percent agreement 1.0, Cohen's kappa 1.0, quadratic weighted kappa 1.0. The verdict is the same for both: fail, 6 of 10.

Two caveats on that number. The judges share a family, so this is not the cross family check the runner insists on for a run: it says the two models read the rubric the same way, and it does not say the rubric is right. And 1.0 on five scenarios is the agreement of two readers on a short set; the threshold that matters for a gate is 0.80 and this clears it, but the set is small.

The score of each scenario was also taken three times from the same judge. The judge was stable on 1, 2, 10 and 11, and gave scenario 3 a 0 twice and a 1 once. The number the run keeps is the one the judge gave most often, and a tie goes to the lower score, so the run does not get the benefit of the doubt.

### Uncertainty and checks

Recomputed by `run_tutor_eval.py --summarize` with no new model call, with the interval as the middle 95% of 10000 bootstrap totals, seed 20261109.

| Run | Score | 95% interval | Scored scenarios | Verdict |
|---|---|---|---|---|
| This run, judge A (opus) | 6 of 10 | 3 to 9 | 5 of 15 | fail |
| This run, judge B (sonnet) | 6 of 10 | 3 to 9 | 5 of 15 | fail |
| First run, old rubric | 5 of 10 | 2 to 8 | 4 of 15 | fail |
| First run, new rubric | 4 of 10 | 1 to 7 | 4 of 15 | fail |

- With five scenarios the interval spans most of the scale. The fail comes from the 0 in scenario 3, a critical scenario, not from the total.
- The two judges of this run: percent agreement 1.0, Cohen's kappa 1.0, weighted kappa 1.0, Krippendorff's alpha 1.0 (ordinal and nominal). They agree on the verdict, so it is fail and not contested. Both judges are from the anthropic family, which is why this agreement is not evidence that the rubric is right.
- Checks without a model: in this run, scenarios 10 and 11 fail the check that forbids the 61% and the 40% of the one week result, the same leak the judges named. In the first run, scenario 1 wrote `50_Review/Delayed_Tests_2026-11-10.md`, which the learner did not ask for, and scenario 10 has the same leak. The checks are shown next to the scores and do not change them.
- No person labeled the transcripts. Every score here comes from a model judge.
- None of these runs recorded the version hashes, so each summary says it assumes today's scenarios, rubric and judge prompt. The first run was judged before the learning scenarios changed on 2026-11-10, which is why its two halves are kept as separate run folders.

### The wrapper was fixed after this run

The wrapper that produced the replies in this run had three defects, found by reading it against the way the CLI actually behaves. The replies in this run are not affected: each one was checked against the session the CLI wrote and matches it character for character, and the new rule picks the same message.

- The reply is now tied to the `answer_selected` event the CLI writes, by the size in bytes the event reports. The agent writes text while it works, so the last message on disk can be a half-finished one. Before, the wrapper took the last message with text, which could have been the preamble. If the chosen reply is not on disk yet, the wrapper waits instead of answering with the wrong text.
- The reply on disk is now read before the CLI is checked for liveness. The CLI can exit right after writing the reply, and the reply is what matters.
- The wrapper's own deadline is now the deadline of the run, so a slow reply is not cut inside the wrapper while the run records a timeout that was never in effect. The temporary folder with the prompt and the diagnostics is removed on exit.

The behaviour is locked by `90_System/Scripts/validation/test_mcode_tutor_wrapper.py`, which runs the wrapper against a CLI that is faked to lose the reply in each of the ways it can lose it.

### Limits of these runs

- One run per agent, one date, one set of transcripts. Nothing here says how the same agent behaves on another day.
- The judge is a model, not a person. The scores are a second opinion on the transcripts, not a human grade.
- The first scoring of the first run was one judgement per scenario, and the re-scoring of the same transcripts is the mode of three. The two halves of the comparison are not judged the same number of times, so the 5 of 10 and the 4 of 10 differ by one point on one scenario, and the judge agreed on 1 on all three judgements of that scenario.
- The two judges share a family, which weakens the independence of the agreement number.
- The MiniMax Code CLI produced the reply and then kept running past it. The wrapper reads the reply from the session the CLI wrote and kills the CLI, so the run takes minutes per scenario instead of ending in a timeout.
- Only the critical group ran on 2026-11-10. The other ten scenarios ran for the first time on 2026-11-12, above.
