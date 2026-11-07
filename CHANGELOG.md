# Changelog

Notable changes to this template. Versions follow semantic versioning: a major version changes the folder layout or the note format, a minor version adds something, a patch fixes something.

## Unreleased

- Tutor mode: learner attempts first, hint ladder (hint, strong hint, partial example, answer) after an attempt, confidence from 1 to 5 before the reveal, and agents never write the study layer or the learner's answers.
- Skills `no-ai-checkpoint`, `pretest`, `teach-the-agent`, `mistake-review` and `review-queue`.
- The lesson template has a `Pretest` section; the concept template has `last_tested`, `score` and `confidence` and an apply-type flashcard example. New `Checkpoint` template and `50_Review/Mistakes.md`.
- Bases `Weakest` and `Interleave`, embedded in `00_Home.md`.
- `check_cards.py` fails a flashcard without a source link and a question that appears twice, with `test_check_cards.py`; added to CI, the pull request template and `run-checks`.
- `Studying_with_AI` rewritten around tutor mode and new evidence, with an FSRS section.
- Property types for `last_tested`, `score` and `confidence`.
- The FAQ explains why the template ships no MCP configuration.
- The naming tool now renames folders with spaces too (deepest first), rewrites links that contain folder paths, skips `.vendored` folders and renames untracked files without git.
- The naming tool and the link check accept parentheses in Markdown link targets.
- The link check also scans `llms.txt`.
- The formatter leaves `$$` math blocks untouched.
- The Claude Code hook formats only notes inside the vault and skips `.vendored` folders.
- The study layer check now fails a concept, reference or guide note that has no `## Study explanation`.
- Guides use `type: guide` and no longer appear in the references base.
- The course template lists lessons and concepts by hand instead of embedding unfiltered bases.
- The lesson and concept templates carry the `flashcards` and `cat/<category>` tags.
- Spaced Repetition is the only listed community plugin, and it is optional. Obsidian 1.9 or later is required for Bases.
- The example concept, paper and repository guide now follow the study layer spec, with flashcards.
- `.gitkeep` files keep the empty folders in the template.
- Tests for the link check and the study layer check.

## 0.1.0 (2026-11-07)

### Added

- Vault layout: `00_Inbox`, `10_Courses`, `20_Concepts`, `30_Maps`, `40_References`, `50_Review`, `90_System`.
- Study layer in concept, reference and guide notes (`## Study explanation`, `## Key takeaways`, flashcards), with its spec in `90_System/Specs/Study_layer.md`.
- Templates for course, lesson, concept, reference and weekly review; bases for concepts, lessons and references.
- Example course, lesson, concept and paper that show the full note format.
- Guides on studying with AI and on repository and documentation patterns for AI.
- Agent files: `AGENTS.md` as the single source of rules, `CLAUDE.md` and `GEMINI.md` importing it, Copilot instructions, `llms.txt`.
- Project skills `new-course`, `new-concept-note`, `process-paper`, `run-checks`, plus five vendored Obsidian skills.
- Agent log in `90_System/Agent_Log/`.
- Checks: note formatting, links (including `obsidian://`), study layer order, file names; tests for the formatter and the naming tool; GitHub Actions workflow.
- Naming tool that renames files with spaces and rewrites every link.
- Claude Code hook that formats every note an agent edits, and settings that block reading `.env` and plugin `data.json`.
- Community files: `CONTRIBUTING.md`, `CHANGELOG.md`, `FAQ.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, issue and pull request templates, Dependabot for actions, `CODEOWNERS`.
