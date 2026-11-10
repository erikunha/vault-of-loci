---
type: log
summary: Tutor eval run of minimax on 2026-11-09: what was run and how.
tags: [type/log]
---

# Tutor eval run: minimax, 2026-11-09

- Agent: minimax (family: minimax).
- Command: `90_System/Evals/mcode-tutor.sh` (that day it ran from a copy in `/tmp/mcodew/`). The prompt goes to the command on stdin.
- Scenarios run: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17.
- Started 2026-11-09T19:32:30+00:00, finished 2026-11-09T20:29:14+00:00.
- Each scenario ran in a fresh copy of the vault without `.git` and without `90_System/Evals`; the real vault was not changed.
- Vault instructions pasted into the prompt: no.
- Files: `transcript.jsonl` (one record per message), `transcript.md` (readable), `run.json` (settings), `scoring_sheet.md` (for a person), and `scores.json` and `summary.md` once a judge has scored the run.

## Notes

Tutor: MiniMax Code CLI (mcode exec) through the wrapper `90_System/Evals/mcode-tutor.sh`, because the CLI exits 70 when its runtime shutdown misses the deadline; the wrapper reads the final message from the diagnostics folder.

Judges: agy (Antigravity CLI, family google) wrote `scores.json` and `summary.md`. kimi (family moonshot) wrote `scores-judge-kimi.json` and `summary-judge-kimi.md`. Neither judge shares the tutor's family.

The agent changed files in the vault copy. The runner recorded which ones; the transcripts show them per turn.
