---
name: run-checks
description: Run every check of this vault (formatting, links, study layer, names, flashcards, skills, alt text, reading index, tests). Use after editing and before committing.
---

Run every check with one command:

```bash
python3 -I 90_System/Scripts/run_checks.py
```

It runs `format_notes.py --check`, every `validation/check_*.py` and every `validation/test_*.py`, and prints passed or FAILED for each, with the last lines of a failure.

How to fix the usual failures:

- Formatting: `python3 -I 90_System/Scripts/format_notes.py` (without `--check`).
- Names: `python3 90_System/Scripts/normalize_names.py --write`.
- Reading index: `python3 -I 90_System/Scripts/build_index.py`.
- Flashcards: every `question::answer` card and cloze needs a source link; no question may repeat.
- Anything else: read the failing check's own message; `90_System/Specs/Tools.md` says what each check guards.

Report each check as passed, failed or not run. Not run is never passed.
