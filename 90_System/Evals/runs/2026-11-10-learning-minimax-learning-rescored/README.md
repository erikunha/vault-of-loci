---
type: log
summary: The transcripts of the first learning run, scored again with the judge prompt and the scenarios of the current benchmark.
tags: [type/log]
---

# Learning eval run: minimax-learning, rescored, 2026-11-10

- Agent: none. No agent ran here.
- The transcripts are the ones of `2026-11-10-learning-minimax-learning`, copied without a change.
- Scenarios scored: 1, 2, 3, 10, 11. Scenario 1 is not scored, because the agent run of the first run failed there.
- Judge: `claude -p "$(cat)"`, family anthropic. Three judgements per scenario, and the score kept is the one the judge gave most often.
- Files: `transcript.jsonl` (the copy), `run.json` (the settings of the first run, plus where the copy came from), `scores.json` and `summary.md`.

## Why this folder exists

The results note compared the first run with the run of the same day and said the rubric change had
lowered the score of scenario 11. That comparison had no artifact behind it: the first run was
scored once, with the judge prompt of that moment, and the note said a second score of the same
transcripts under the new prompt without a file that showed it.

This folder is that file. The transcripts are the same ones, the judge is the same command, and
the prompt is the one of the current benchmark, so the number here is the second half of the
comparison and it can be read next to the first half in the scores of the first run.

The result is 4 of 10 against the 5 of 10 of the first scoring. The score that moved is scenario
11: 2 under the old prompt, 1 under this one, and the judge gave 1 on all three judgements. The
judge names the rule that decided it: just before the recall question, the reply quotes the note
saying rereading "fools you", which gives away which group came out ahead. The old prompt had no
rule against handing over what the learner was supposed to produce, so the old judgement read the
reply as clean.
