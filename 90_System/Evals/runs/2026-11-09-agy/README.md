---
type: log
summary: Tutor eval run of agy on 2026-11-09: what was run and how.
tags: [type/log]
---

# Tutor eval run: agy, 2026-11-09

- Agent: agy (family: google).
- Command: `AI_DEV_RUNTIME_AGY_DELEGATED=1 agy --print "$(cat)"`. The prompt goes to the command on stdin.
- Scenarios run: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17.
- Started 2026-11-09T20:47:25+00:00, finished 2026-11-09T21:12:30+00:00.
- Each scenario ran in a fresh copy of the vault without `.git` and without `90_System/Evals`; the real vault was not changed.
- Vault instructions pasted into the prompt: no.
- Files: `transcript.jsonl` (one record per message), `transcript.md` (readable), `run.json` (settings), `scoring_sheet.md` (for a person), and `scores.json` and `summary.md` once a judge has scored the run.

## Notes

Tutor: agy (Antigravity CLI) in the delegated print mode (`AI_DEV_RUNTIME_AGY_DELEGATED=1`), so the PreToolUse guard allows ordinary reads inside the vault copy. In the plain print mode the agent cannot read the notes and the run measures the hook instead of the agent.

Judges: kimi (family moonshot) wrote `scores.json` and `summary.md`. MiniMax (family minimax) wrote `scores-judge-minimax.json` and `summary-judge-minimax.md`. Neither judge shares the tutor's family.

The agent changed no file in the vault copy. The two judges differ in scenario 2, which decides the verdict; read both summaries.
