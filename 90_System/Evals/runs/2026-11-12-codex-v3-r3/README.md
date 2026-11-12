---
type: log
summary: Tutor eval run of codex-v3-r3 on 2026-11-12: what was run and how.
tags: [type/log]
---

# Tutor eval run: codex-v3-r3, 2026-11-12

- Agent: codex-v3-r3 (family: openai).
- Command: `codex exec --skip-git-repo-check -`. The prompt goes to the command on stdin.
- Scenarios run: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17.
- Started 2026-11-12T18:09:48+00:00, finished 2026-11-12T18:26:16+00:00.
- Each scenario ran in a fresh copy of the vault without `.git` and without `90_System/Evals`; the real vault was not changed.
- Vault instructions pasted into the prompt: no.
- Files: `transcript.jsonl` (one record per message), `transcript.md` (readable), `run.json` (settings), `scoring_sheet.md` (for a person), and `scores.json` and `summary.md` once a judge has scored the run.

## Notes

Repeat 3 of 3 after the tutor rules of PR 41 and PR 42. Same CLIs, flags and judges as the 2026-11-12 runs.
