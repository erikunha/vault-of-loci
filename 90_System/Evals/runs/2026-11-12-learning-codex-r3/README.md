---
type: log
summary: Learning eval run of codex-r3 on 2026-11-12: what was run and how.
tags: [type/log]
---

# Learning eval run: codex-r3, 2026-11-12

- Agent: codex-r3 (family: openai).
- Command: `codex exec --skip-git-repo-check -`. The prompt goes to the command on stdin.
- Scenarios run: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15.
- Started 2026-11-12T13:56:25+00:00, finished 2026-11-12T14:05:33+00:00.
- Each scenario ran in a fresh copy of the vault without `.git` and without `90_System/Evals`; the real vault was not changed.
- Vault instructions pasted into the prompt: no.
- Files: `transcript.jsonl` (one record per message), `transcript.md` (readable), `run.json` (settings), `scoring_sheet.md` (for a person), and `scores.json` and `summary.md` once a judge has scored the run.

## Notes

Repeat 3 of 3. Codex CLI with the user configuration of the machine (model gpt-6.1-sol, reasoning effort medium, from config.toml).
