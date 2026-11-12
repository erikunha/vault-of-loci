---
type: log
updated: 2026-11-12
tags: [type/log]
---

# Learning eval results

Each run follows [[Learning_evals|Learning eval]]: the agent answers a learner's question using the vault's own record, and a judge from another model family scores the reply from 0 to 2 against the rubric. The critical group is scenarios 1, 2, 3, 10 and 11, and the pass rule for that group is 8 of 10 with no 0 in any of them. The rule for a run of the whole benchmark asks for two things at once, 24 of 30 points and 8 of 10 in the critical group, and the runs here cover the critical group only, so the rule that applies to them is the 8 of 10.

These runs use the learning ledger as the fixture. Each scenario writes a ledger with dated events into a fresh copy of the vault, so the agent reads a record the scenario controls and the real `50_Review/Attempts.jsonl` is never touched.

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
- Only the critical group ran. The other ten scenarios of the benchmark are untested here.
