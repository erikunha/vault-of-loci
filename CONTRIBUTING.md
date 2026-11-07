# Contributing

Thanks for helping. This template should stay small, plain Markdown and easy to adapt, so every change is judged by one question: does it help someone study better with this vault?

## What fits

- Fixes to the checks, the naming tool, the formatter or the hook.
- Clearer templates, specs, skills or guides.
- Better example notes that show the full note format.
- New checks that catch a real mistake in notes, links or names.

## What does not fit

- Personal notes or course content. Keep those in your own copy.
- Community plugins as hard requirements. The vault must open and pass its checks without them.
- Dependencies outside the Python standard library.
- Lists of links to other projects.

## How to propose a change

1. Open an issue first for anything bigger than a typo, so we agree on the shape before you write it.
2. Fork the repository and make the change on a branch.
3. Follow `AGENTS.md`. The same rules apply to people and to agents: underscores in file names, the study layer order, verified references, no em dash or en dash.
4. Run every check and make sure all of them pass:

   ```bash
   python3 -I 90_System/Scripts/format_notes.py --check
   python3 -I 90_System/Scripts/validation/check_links.py
   python3 -I 90_System/Scripts/validation/check_study_layer.py
   python3 -I 90_System/Scripts/validation/check_names.py
   python3 -I 90_System/Scripts/validation/test_format_notes.py
   python3 -I 90_System/Scripts/validation/test_normalize_names.py
   python3 -I 90_System/Scripts/validation/test_check_links.py
   python3 -I 90_System/Scripts/validation/test_check_study_layer.py
   ```

5. A change to a script ships with a test that fails without the change and passes with it.
6. Add a line under `Unreleased` in `CHANGELOG.md`.
7. Open a pull request that says what changed, why, and which checks you ran.

## Commit messages

Use Conventional Commits: `feat:`, `fix:`, `docs:`, `test:`, `chore:`. Keep the subject under 72 characters.

## Third-party files

Folders with a `.vendored` file are copies of another project. Do not edit them here. To update one, copy the new version from its source and keep its `LICENSE`.

## License

By contributing you agree that your work is released under the MIT license in `LICENSE`.
