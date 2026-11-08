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
- Say how AI was used. The pull request template asks whether an agent wrote the change and who reviewed it. A pull request opened by an agent with no person answering review comments is closed.
- No personal data, no em dash or en dash.

## What does not fit

- Personal material, as described above.
- Community plugins as hard requirements. The vault must open and pass its checks without them.
- Dependencies outside the Python standard library.
- Lists of links to other projects.

## Your first contribution

You can contribute a note without installing anything, from the GitHub website:

1. Pick an issue labeled [good first issue](https://github.com/erikunha/vault-of-loci/labels/good%20first%20issue), or open a "Content proposal" and wait for a yes.
2. Open the file you want to change on GitHub and click the pencil icon. GitHub makes a copy (a fork) for you. To add a note, open the folder and choose **Add file**.
3. Copy the shape from a template in `90_System/Templates/`, or from the example concept `20_Concepts/Retrieval_Practice.md`.
4. Click **Commit changes**, then **Create pull request**. Say what you changed and which sources you opened.
5. The checks run on your pull request. If one fails, the log names the file and the line; fix it in the same pull request, or ask in it for help.

For anything bigger, the steps below use a local copy.

## How to propose a change

1. Open an issue first for anything bigger than a typo, so we agree on the shape before you write it. For content, use the "Content proposal" form; comment on an open issue to claim it.
2. Fork the repository and make the change on a branch.
3. Follow `AGENTS.md`. The same rules apply to people and to agents: underscores in file names, the study layer order, verified references, no em dash or en dash.
4. Run every check and make sure all of them pass:

   ```bash
   python3 -I 90_System/Scripts/run_checks.py
   ```

   If `check_index.py` fails after a note edit, run `python3 -I 90_System/Scripts/build_index.py` and run the checks again.

5. A change to a script ships with a test that fails without the change and passes with it.
6. Open a pull request that says what changed, why, and which checks you ran. Its title becomes the line in the release notes, so write it for a reader: `feat: concept note on spacing`, not `update file`.

Nothing reaches `main` without a pull request, maintainers and bots included. A pull request merges only when the `vault` check passes and every review thread is resolved, and it lands as one squashed commit. Force pushes and deleting `main` are blocked.

## Commit messages

Use Conventional Commits: `feat:`, `fix:`, `docs:`, `test:`, `chore:`. Keep the subject under 72 characters.

## Third-party files

Folders with a `.vendored` file are copies of another project. Do not edit them here. To update one, copy the new version from its source and keep its `LICENSE`.

## License

By contributing you agree that your work is released under the MIT license in `LICENSE`.
