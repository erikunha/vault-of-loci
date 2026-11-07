# Contributing

Thanks for helping. This template should stay small, plain Markdown and easy to adapt, so every change is judged by one question: does it help someone learn better with this vault?

## What fits

Reusable material is welcome: anything that helps another learner and stays correct when copied into someone else's vault.

| Content | Shape it needs |
|---|---|
| General concept note (a study technique, a learning-science idea) | `90_System/Templates/Concept.md`: study layer, flashcards with sources, verified references |
| Reference note (paper, book, official guide) | `90_System/Templates/Reference.md`, with a DOI, arXiv ID or official URL you opened |
| Recipe and practice kit for a kind of learning project | a section in `90_System/Specs/Track_kinds.md` and templates in `90_System/Templates/Practice/` |
| Example track | a folder in `10_Tracks/` with a track note, at least one session and a practice file, marked as an example |
| Guide | `40_References/Guides/`, study layer format |
| Study layer translation | `90_System/Specs/study_layer.<language>.json` with the same keys as `study_layer.json` |
| Skill | `.agents/skills/<name>/SKILL.md` following the Agent Skills spec, tutor mode, `disable-model-invocation` and `agents/openai.yaml` if it writes files |
| Tutor-mode scenario | a row in `90_System/Evals/Tutor_mode.md` with the expected agent behavior |
| Tooling | fixes and new checks in `90_System/Scripts`, standard library only, with a test |

### Reusable or personal

Reusable content teaches without your history: nothing in it identifies you, your school or your employer. Personal content stays in your own copy: your sessions, answers, grades, checkpoints, mistakes, interview details, employer or school names, and anything private. The line exists for privacy and because personal notes do not help someone else learn.

### Quality bar

- Every factual claim has a source you opened yourself (DOI, arXiv ID or official URL). Anything you did not read is marked "not verified".
- Concept, reference and guide notes carry the full study layer and pass every check.
- Examples are generic. A sample source that stands in for a real one says so.
- Skills follow the Agent Skills spec: the name matches the folder, the description has at most 1024 characters, and `SKILL.md` stays short.
- You can explain every line you submit. Drafts written with AI help are fine when you verified every source and say so in the pull request.
- No personal data, no em dash or en dash.

## What does not fit

- Personal material, as described above.
- Community plugins as hard requirements. The vault must open and pass its checks without them.
- Dependencies outside the Python standard library.
- Lists of links to other projects.

## How to propose a change

1. Open an issue first for anything bigger than a typo, so we agree on the shape before you write it. For content, use the "Content proposal" form; comment on an open issue to claim it.
2. Fork the repository and make the change on a branch.
3. Follow `AGENTS.md`. The same rules apply to people and to agents: underscores in file names, the study layer order, verified references, no em dash or en dash.
4. Run every check and make sure all of them pass (`check_index.py` fails after a note edit until you run `python3 -I 90_System/Scripts/build_index.py`):

   ```bash
   python3 -I 90_System/Scripts/format_notes.py --check
   python3 -I 90_System/Scripts/validation/check_links.py
   python3 -I 90_System/Scripts/validation/check_study_layer.py
   python3 -I 90_System/Scripts/validation/check_names.py
   python3 -I 90_System/Scripts/validation/check_cards.py
   python3 -I 90_System/Scripts/validation/check_skills.py
   python3 -I 90_System/Scripts/validation/check_bases.py
   python3 -I 90_System/Scripts/validation/check_study_layer_translations.py
   python3 -I 90_System/Scripts/validation/check_alt_text.py
   python3 -I 90_System/Scripts/validation/check_index.py
   python3 -I 90_System/Scripts/validation/test_format_notes.py
   python3 -I 90_System/Scripts/validation/test_normalize_names.py
   python3 -I 90_System/Scripts/validation/test_check_links.py
   python3 -I 90_System/Scripts/validation/test_check_study_layer.py
   python3 -I 90_System/Scripts/validation/test_check_cards.py
   python3 -I 90_System/Scripts/validation/test_check_skills.py
   python3 -I 90_System/Scripts/validation/test_check_bases.py
   python3 -I 90_System/Scripts/validation/test_check_study_layer_translations.py
   python3 -I 90_System/Scripts/validation/test_check_index.py
   python3 -I 90_System/Scripts/validation/test_check_alt_text.py
   python3 -I 90_System/Scripts/validation/test_export_anki_tsv.py
   python3 -I 90_System/Scripts/validation/test_export_bibtex.py
   ```

5. A change to a script ships with a test that fails without the change and passes with it.
6. Add a line under `Unreleased` in `CHANGELOG.md`.
7. Open a pull request that says what changed, why, and which checks you ran.

## Commit messages

Use Conventional Commits: `feat:`, `fix:`, `docs:`, `test:`, `chore:`. Keep the subject under 72 characters.

## Third-party files

Folders with a `.vendored` file are copies of another project. Do not edit them here. To update one, copy the new version from its source and keep its `LICENSE`.

## Recognition

Every merged contribution is credited in the Contributors section of `README.md`.

## License

By contributing you agree that your work is released under the MIT license in `LICENSE`.
