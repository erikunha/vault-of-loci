---
type: log
summary: Learning eval run of minimax-learning-s1 on 2026-11-10: what was run and how.
tags: [type/log]
---

# Learning eval run: minimax-learning-s1, 2026-11-10

- Agent: minimax-learning-s1 (family: minimax).
- Command: `90_System/Evals/mcode-tutor.sh`. The prompt goes to the command on stdin.
- Scenarios run: 1.
- Started 2026-11-10T12:22:37+00:00, finished 2026-11-10T12:27:33+00:00.
- Each scenario ran in a fresh copy of the vault without `.git` and without `90_System/Evals`; the real vault was not changed.
- Vault instructions pasted into the prompt: no.
- Files: `transcript.jsonl` (one record per message), `transcript.md` (readable), `run.json` (settings), `scoring_sheet.md` (for a person), and `scores.json` and `summary.md` once a judge has scored the run.

## Notes

Retry of scenario 1, the critical one, after a 600s timeout.

This transcript was produced before the scenario 1 fixture was fixed, so it is kept as the evidence that found the mismatch, not as a scoreable run. The fixture encoded the clean recalls as 110 and 100 days ago, so the vault audit answered "due at 30 days" while the rubric asked for 90. The agent named the right objective and the right new task, and its answer was right for the ledger it read. The scoreable run is in `../2026-11-10-learning-minimax-learning-s1-fixed`.
