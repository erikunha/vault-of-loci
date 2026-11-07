---
name: run-checks
description: Run every check of this vault (formatting, links, study layer, names, tests). Use after editing and before committing.
---

1. Formatting: `python3 -I 90_System/Scripts/format_notes.py --check` (to fix, run it without `--check`).
2. Links: `python3 -I 90_System/Scripts/validation/check_links.py`
3. Study layer: `python3 -I 90_System/Scripts/validation/check_study_layer.py`
4. Names: `python3 -I 90_System/Scripts/validation/check_names.py` (to fix, `python3 90_System/Scripts/normalize_names.py --write`).
5. Tests: `python3 -I 90_System/Scripts/validation/test_format_notes.py` and `python3 -I 90_System/Scripts/validation/test_normalize_names.py`.

Report each step as passed, failed or not run. Not run is never passed.
