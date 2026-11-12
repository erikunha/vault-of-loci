---
type: log
summary: Learning eval run of glm-r3 on 2026-11-12: what was run and how.
tags: [type/log]
---

# Learning eval run: glm-r3, 2026-11-12

- Agent: glm-r3 (family: zhipu).
- Command: `glm -p --setting-sources project,local --model opus`. The prompt goes to the command on stdin.
- Scenarios run: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15.
- Started 2026-11-12T14:51:02+00:00, finished 2026-11-12T15:12:57+00:00.
- Each scenario ran in a fresh copy of the vault without `.git` and without `90_System/Evals`; the real vault was not changed.
- Vault instructions pasted into the prompt: no.
- Files: `transcript.jsonl` (one record per message), `transcript.md` (readable), `run.json` (settings), `scoring_sheet.md` (for a person), and `scores.json` and `summary.md` once a judge has scored the run.

## Notes

Repeat 3 of 3. GLM Coding Plan through Claude Code (the glm wrapper, model glm-5.3) with --setting-sources project,local, so the user hooks and settings of the machine are left out; the user memory files still load.
