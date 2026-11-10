<!--
  Thanks for opening a pull request. The sections below help a reviewer understand it.

  Before you open it:

  1. Fork the repository and create your branch from `main`.
  2. Follow `AGENTS.md`: underscores in file names, the study layer order, verified references, no em dash or en dash.
  3. Open every reference you add. A reference you did not open is not verified.
  4. If you changed a script, add a test that fails without the change.
  5. Run `python3 -I 90_System/Scripts/run_checks.py` until every check passes.

  Learn more: [CONTRIBUTING.md](CONTRIBUTING.md) and [AGENTS.md](../AGENTS.md)

-->

## Summary

<!-- What changed and why. Two or three bullets: give the reviewer the context, do not restate the title. -->
<!-- Link the issues this resolves, e.g. "Closes #12" / "Fixes #12". Omit if there is none. -->

-

-

## Type of change

<!-- Conventional Commits types, plus what the change touches. -->

- [ ] `feat`: new functionality
- [ ] `fix`: bug fix
- [ ] `docs`: documentation only
- [ ] `test`: tests only
- [ ] `chore` / `ci`: non functional
- [ ] **breaking change**: describe the impact, the migration and the rollback in Summary

## Test plan

<!-- Show the work. Paste the command output. Assertions without evidence will be questioned. -->

- [ ] `python3 -I 90_System/Scripts/run_checks.py` passes (paste the last line)
- [ ] A changed script ships with a test that fails without the change
- [ ] New behaviour covered by tests
- [ ] Evidence attached where it applies (command output, before and after, note excerpt)
- [ ] One line added to `90_System/Agent_Log/YYYY-MM.md`

## Notes and structure

<!-- Delete this section when no note changed. -->

- [ ] File and folder names use underscores
- [ ] Study layer order follows `90_System/Specs/study_layer.json`
- [ ] Every reference was opened and carries a DOI, an arXiv ID or an official URL
- [ ] Flashcards carry a source and a unique question
- [ ] `INDEX.md` and `90_System/index.json` rebuilt with `build_index.py`
- [ ] No em dash, no en dash, no personal data

## Checklist

- [ ] Python standard library only
- [ ] No community plugin becomes a hard requirement
- [ ] Third party folders with a `.vendored` marker were not edited
- [ ] A skill keeps the Agent Skills spec: name, description, short `SKILL.md`
- [ ] Docs, specs and skills that describe the change are updated
- [ ] Reversible: a rollback path exists (revert SHA)
- [ ] Security impact considered (no secrets, no personal data)

## AI use

<!-- Pick one and keep it. -->

- [ ] No AI tool wrote any part of this change.
- [ ] An AI tool helped. I reviewed every line, opened every reference and can answer review comments myself.
- [ ] An agent opened this pull request. A person named here reviewed it and answers comments: @
