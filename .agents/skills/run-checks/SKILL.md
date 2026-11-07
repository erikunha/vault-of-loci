---
name: run-checks
description: Run every check of this vault (formatting, links, study layer, names, flashcards, skills, reading index, tests). Use after editing and before committing.
---

1. Formatting: `python3 -I 90_System/Scripts/format_notes.py --check` (to fix, run it without `--check`).
2. Links: `python3 -I 90_System/Scripts/validation/check_links.py`
3. Study layer: `python3 -I 90_System/Scripts/validation/check_study_layer.py` (headings come from `90_System/Specs/study_layer.json`).
4. Names: `python3 -I 90_System/Scripts/validation/check_names.py` (to fix, `python3 90_System/Scripts/normalize_names.py --write`).
5. Flashcards: `python3 -I 90_System/Scripts/validation/check_cards.py` (every `question::answer` card needs a source wikilink; no question may repeat).
6. Skills: `python3 -I 90_System/Scripts/validation/check_skills.py`
7. Bases: `python3 -I 90_System/Scripts/validation/check_bases.py`
8. Reading index: `python3 -I 90_System/Scripts/validation/check_index.py` (to fix, `python3 -I 90_System/Scripts/build_index.py`).
9. Tests, one per line:
   - `python3 -I 90_System/Scripts/validation/test_format_notes.py`
   - `python3 -I 90_System/Scripts/validation/test_normalize_names.py`
   - `python3 -I 90_System/Scripts/validation/test_check_links.py`
   - `python3 -I 90_System/Scripts/validation/test_check_study_layer.py`
   - `python3 -I 90_System/Scripts/validation/test_check_cards.py`
   - `python3 -I 90_System/Scripts/validation/test_check_skills.py`
   - `python3 -I 90_System/Scripts/validation/test_check_bases.py`
   - `python3 -I 90_System/Scripts/validation/test_check_index.py`

Report each step as passed, failed or not run. Not run is never passed.
