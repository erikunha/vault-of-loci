---
name: run-checks
description: Run every check of this vault (formatting, links, study layer, names, flashcards, skills, alt text, reading index, tests). Use after editing and before committing.
---

1. Formatting: `python3 -I 90_System/Scripts/format_notes.py --check` (to fix, run it without `--check`).
2. Links: `python3 -I 90_System/Scripts/validation/check_links.py`
3. Study layer: `python3 -I 90_System/Scripts/validation/check_study_layer.py` (headings come from `90_System/Specs/study_layer.json`).
4. Names: `python3 -I 90_System/Scripts/validation/check_names.py` (to fix, `python3 90_System/Scripts/normalize_names.py --write`).
5. Flashcards: `python3 -I 90_System/Scripts/validation/check_cards.py` (every `question::answer` card and cloze needs a source link; no question may repeat).
6. Skills: `python3 -I 90_System/Scripts/validation/check_skills.py`
7. Bases: `python3 -I 90_System/Scripts/validation/check_bases.py`
8. Study layer translations: `python3 -I 90_System/Scripts/validation/check_study_layer_translations.py`
9. Image alt text: `python3 -I 90_System/Scripts/validation/check_alt_text.py`
10. Reading index: `python3 -I 90_System/Scripts/validation/check_index.py` (to fix, `python3 -I 90_System/Scripts/build_index.py`).
11. Tests, one per line:
   - `python3 -I 90_System/Scripts/validation/test_format_notes.py`
   - `python3 -I 90_System/Scripts/validation/test_normalize_names.py`
   - `python3 -I 90_System/Scripts/validation/test_check_links.py`
   - `python3 -I 90_System/Scripts/validation/test_check_study_layer.py`
   - `python3 -I 90_System/Scripts/validation/test_check_cards.py`
   - `python3 -I 90_System/Scripts/validation/test_check_skills.py`
   - `python3 -I 90_System/Scripts/validation/test_check_bases.py`
   - `python3 -I 90_System/Scripts/validation/test_check_study_layer_translations.py`
   - `python3 -I 90_System/Scripts/validation/test_check_index.py`
   - `python3 -I 90_System/Scripts/validation/test_check_alt_text.py`
   - `python3 -I 90_System/Scripts/validation/test_export_anki_tsv.py`
   - `python3 -I 90_System/Scripts/validation/test_export_bibtex.py`
   - `python3 -I 90_System/Scripts/validation/test_transcripts.py`

Report each step as passed, failed or not run. Not run is never passed.
