---
type: log
summary: Learning eval run of glm-v3-r1 on 2026-11-12: what was run and how.
tags: [type/log]
---

# Learning eval run: glm-v3-r1, 2026-11-12

- Agent: glm-v3-r1 (family: zhipu).
- Command: `glm -p --setting-sources project,local --model opus`. The prompt goes to the command on stdin.
- Scenarios run: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15.
- Started 2026-11-12T19:11:39+00:00, finished 2026-11-12T19:34:44+00:00.
- Each scenario ran in a fresh copy of the vault without `.git` and without `90_System/Evals`; the real vault was not changed.
- Vault instructions pasted into the prompt: no.
- Files: `transcript.jsonl` (one record per message), `transcript.md` (readable), `run.json` (settings), `scoring_sheet.md` (for a person), and `scores.json` and `summary.md` once a judge has scored the run.

## Notes

Repeat 1 of 3 after the tutor rules of PR 41 and PR 42. Same CLIs, flags and judges as the 2026-11-12 runs.
