---
type: log
summary: Where tutor eval runs are kept, how a run folder is named, and the exact commands to run the eval and score it.
tags: [type/log]
---

# Tutor eval runs

Each run of `90_System/Scripts/run_tutor_eval.py` writes one folder here, named `<YYYY-MM-DD>-<label>`, with the prefix of the benchmark in the label: a run of the learning benchmark is `<YYYY-MM-DD>-learning-<label>`. The runs of 2026-11-09 are `2026-11-09-agy` and `2026-11-09-minimax`, and they are kept in the repository; a vault that starts empty has no run folder yet. Run the commands below from the root of the vault, then commit the folder you want to keep.

A run folder holds:

- `transcript.jsonl`: one record per message (scenario, turn, role, text, agent, command, times, files the agent changed).
- `transcript.md`: the same transcript, readable.
- `run.json` and `README.md`: the settings and a short description of the run.
- `scoring_sheet.md`: a table a person fills in.
- `scores.json` and `summary.md`: written when a judge scores the run. The runner writes one pair of files. A second judge is scored by hand: its scores are saved next to them as `scores-judge-<judge>.json`, with the family and the model of the judge, so two judges of the same family do not share one name, and `judge_agreement.py` compares the two files.

The scenarios, the rubric and the pass rule are in [[Tutor_mode|Tutor mode eval]]. Results are summarized in [[Tutor_mode_results|Tutor mode eval results]].

## Run it against an agent

The runner starts the agent you name, so run it yourself. Each command sends the conversation to the agent on standard input. The flags for `agy` and `kimi` follow their `--help`; check them against your version. The `agy` and `kimi` commands below are the ones the runs of 2026-11-09 used.

```bash
# Claude Code
python3 -I 90_System/Scripts/run_tutor_eval.py --label claude-code --agent-family anthropic --agent-cmd "claude -p"

# Codex (the vault copy has no .git, so skip that check)
python3 -I 90_System/Scripts/run_tutor_eval.py --label codex --agent-family openai --agent-cmd "codex exec --skip-git-repo-check -"

# Antigravity (set --agent-family to the family of the model you pick)
python3 -I 90_System/Scripts/run_tutor_eval.py --label agy --agent-family google --agent-cmd 'agy -p "$(cat)"'

# Kimi
python3 -I 90_System/Scripts/run_tutor_eval.py --label kimi --agent-family moonshot --agent-cmd 'kimi -p "$(cat)"'
```

Add `--scenarios 1,2,5` to try a few scenarios first, or `--dry-run` to print the prompts and run nothing. Without a judge, score the run by hand with `scoring_sheet.md`.

Two things changed in the runs of 2026-11-09, both about the CLI rather than the model:

- **Antigravity needs the delegated print mode to read the vault.** In the plain print mode its PreToolUse hook refuses to read files inside the vault copy, so the agent answers from the prompt alone and the run measures the hook. `AI_DEV_RUNTIME_AGY_DELEGATED=1` is the mode that lets ordinary reads through. The run of 2026-11-09 used it.
- **The MiniMax Code CLI can lose the answer on exit.** When its runtime shutdown misses the deadline it exits 70 and prints nothing, even though the reply was produced. The wrapper `90_System/Evals/mcode-tutor.sh` runs the CLI with `--diagnostics-dir` and prints the message it finds there. Use it as `--agent-cmd` or as `--judge-cmd`.

## Add a judge from another family

The judge must come from a different model family than the agent. The runner refuses a run when `--agent-family` and `--judge-family` match, unless you pass `--allow-same-family`. The judge reads the rubric and the transcript on standard input and answers `SCORE: 0|1|2` and `WHY: ...`.

For an agent from Anthropic, use a judge that is not from Anthropic:

```bash
# in the same command as the run
python3 -I 90_System/Scripts/run_tutor_eval.py --label claude-code --agent-family anthropic --agent-cmd "claude -p" \
  --judge-cmd "codex exec --skip-git-repo-check -" --judge-family openai

# or score a run you already have
python3 -I 90_System/Scripts/run_tutor_eval.py --score-run 90_System/Evals/runs/<date>-claude-code \
  --judge-cmd 'kimi -p "$(cat)"' --judge-family moonshot
```

Any command that reads a prompt on standard input works as a judge, for example `codex exec --skip-git-repo-check -`, `kimi -p "$(cat)"` or `agy -p "$(cat)"` with a model of another family. A small judge can time out or misread a case; read a few scores against the transcript before relying on them. To fix a score, edit `scores.json` and run `--summarize 90_System/Evals/runs/<date>-<label>`.
