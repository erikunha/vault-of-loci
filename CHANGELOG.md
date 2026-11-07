# Changelog

Notable changes to this template. Versions follow semantic versioning: a major version changes the folder layout or the note format, a minor version adds something, a patch fixes something.

## Unreleased

### Added

- Contributions of reusable content are welcome: a content-type table, the line between reusable and personal, a quality bar, a "Content proposal" issue form and a Contributors section.
- `spoken-mock` skill (timed spoken mock, coached or observed) and a `Debrief` template.
- The mistakes log records how AI was involved (scaffold, substitute, none) and closes a mistake only after an unaided correct retry.
- Practice kits per kind in `90_System/Templates/Practice/` (blueprint map, problem log, input log, output sample, synthesis matrix, attempt log, checkpoints, 48-hour plan); `new-track` copies the right kit, and both example tracks show a filled checkpoint.
- `study_layer.pt-BR.json` and `check_study_layer_translations.py`.

### Fixed

- Bases no longer list the note templates as tracks, sessions, concepts or references. `check_bases.py` guards it.
- `new-track`, `new-concept-note`, `process-paper` and `process-web` had no explicit-use setting; they now run only when asked.

### Changed

- The graph opens zoomed in, with labels, and the README shows the vault in Obsidian.
- The README replaces the agent diagram and file table with a "Supported agents" matrix: rules file, skills, hooks, MCP config and ignore or permissions for Claude Code, Codex, Antigravity CLI, Gemini CLI, Copilot, Cursor and OpenCode, plus a short diagram and a way to check that an agent loaded the rules. Gemini CLI is noted as available only with enterprise licences and paid API keys since 2026-06-18. `llms.txt` is described as an optional index that no major agent reads automatically.
- Skills that write files carry `disable-model-invocation: true` (enforced in Claude Code and Cursor) and `agents/openai.yaml` with `allow_implicit_invocation: false` (enforced in Codex). `check_skills.py` fails a skill that sets the first without the second, with tests.
- The FAQ answer on secrets is rewritten: what `permissions.deny` covers in Claude Code, why the sandbox is the real guard and is not on by default, a Codex deny-read example, and the limits of ignore files. New answers: "Studying privately with a local model" and "AI inside Obsidian".

### Added

- `.cursorignore` and `.geminiignore`: keep `.env`, `.env.*` and plugin `data.json` out of Cursor and Gemini CLI context. A terminal command or a tool can still read them.

## 0.2.0 (2026-11-07)

The vault now supports learning anything, not only courses. The folder layout changes, so see "Upgrading from 0.1.0" below.

### Changed

- `10_Courses` is now `10_Tracks`. A track is a learning project with a `kind` (course, book, certification, interview, research, skill, language or other), a `horizon` (finite or ongoing), a `goal`, a `done_criterion`, a `deadline`, an `if_then` plan and a `status`.
- `lessons/` is now `sessions/` and `project/` is now `practice/` (optional: project, lab, mock, exercises, logs). The `Lesson` template is now `Session`, with `Pretest`, `Plan`, `Notes`, `Recall without notes`, `Reflection`, `AI use` (scaffold or substitute) and `Next step`. The `Course` template is now the generic `Track` template.
- The concept properties `courses` and `lessons` are now `tracks` and `sessions`. Note types `course` and `lesson` are now `track` and `session`; new type `practice`.
- Skill `new-course` is now `new-track`: it asks for the kind and the horizon and builds the folder from the recipe in `Track_kinds.md`.
- Base `Lessons` is now `Sessions`; new base `Tracks` (kind, horizon, deadline, status), embedded in `00_Home.md`. The graph colors and the folder icon follow the new names.
- `AGENTS.md` is shorter: the folder map is gone (the README keeps the one structure table), and a new "How to read this vault" section tells agents to read `INDEX.md` first, open only the section they need and never read a file over 300 lines whole. Tutor mode applies to the learner's own notes; reference notes and guides may be written by an agent with verified sources.
- The study layer headings, checked types and folders are read from `90_System/Specs/study_layer.json` by `check_study_layer.py`; the README "Customize" section points to that one file.
- The example course moved into `10_Tracks/01_Example_Course` with a session, and `10_Tracks/02_Example_Book` shows a book track with one chapter session.
- The `Checkpoint` template asks for a predicted score and a calibration line and has an "explain without notes" round. The `Weekly_Review` template mentions the daily review cap, the backlog mode and forgiving streaks.
- `review-queue` honors a daily review cap (10 to 20 reviews, about 2 new cards) with a "catch up backlog" mode. `no-ai-checkpoint` asks for a predicted score and can run for one track.
- GitHub Actions in `checks.yml` are pinned to commit SHAs.
- README floor: Obsidian 1.9 for Bases, 1.12.7 only for the optional CLI skills.

### Added

- `90_System/Specs/Track_kinds.md`: one recipe per kind of track (notes, practice, review cadence, checkpoint) and the rituals every track shares: plan-act-reflect, goals with a done criterion, if-then plans, calibration, explain without notes, a daily review cap, forgiving streaks, shallow folders and no learning styles, with the evidence.
- Reading index for agents: `90_System/Scripts/build_index.py` writes `INDEX.md` (one line per note: link, type, line count, summary of at most 200 characters) and `90_System/index.json` (every heading with its line number). Templates are left out of it. `check_index.py` fails when they are stale, with `test_check_index.py`. The Claude Code hook rebuilds the index after formatting a note. `llms.txt` links `INDEX.md`.
- `check_skills.py` checks the Agent Skills spec (name matches the folder, lowercase letters, digits and hyphens up to 64 characters, description up to 1024), with `test_check_skills.py`.
- Skill `process-web` saves a fetched web page as a reference note with a summary and headings, so a URL is fetched once.
- FAQ: what you can learn, updating your copy against a release tag, what an agent sends to its provider, offline use, streaks, learning styles, and why no MCP configuration ships.
- Tutor mode: learner attempts first, hint ladder (hint, strong hint, partial example, answer) after an attempt, confidence from 1 to 5 before the reveal, and agents never write the study layer or the learner's answers.
- Skills `no-ai-checkpoint`, `pretest`, `teach-the-agent`, `mistake-review` and `review-queue`.
- The session template has a `Pretest` section; the concept template has `last_tested`, `score` and `confidence` and an apply-type flashcard example. New `Checkpoint` template and `50_Review/Mistakes.md`.
- Bases `Weakest` and `Interleave`, embedded in `00_Home.md`.
- `check_cards.py` fails a flashcard without a source link and a question that appears twice, with `test_check_cards.py`; added to CI, the pull request template and `run-checks`.
- `Studying_with_AI` rewritten around tutor mode and new evidence, with an FSRS section.
- Property types for `last_tested`, `score`, `confidence` and the track properties.
- `.gitkeep` files keep the empty folders in the template.
- Tests for the link check and the study layer check.

### Fixed

- The naming tool now renames folders with spaces too (deepest first), rewrites links that contain folder paths, skips `.vendored` folders and renames untracked files without git.
- The naming tool and the link check accept parentheses in Markdown link targets.
- The link check also scans `llms.txt`.
- The formatter leaves `$$` math blocks untouched.
- The Claude Code hook formats only notes inside the vault and skips `.vendored` folders.
- The study layer check now fails a concept, reference or guide note that has no `## Study explanation`.
- Guides use `type: guide` and no longer appear in the references base.
- The course template lists lessons and concepts by hand instead of embedding unfiltered bases.
- The lesson and concept templates carry the `flashcards` and `cat/<category>` tags.
- Spaced Repetition is the only listed community plugin, and it is optional.
- The example concept, paper and repository guide now follow the study layer spec, with flashcards. The repository guide reports the AGENTS.md study as finding no general gain and no help from overviews.

### Upgrading from 0.1.0

1. Rename `10_Courses` to `10_Tracks`, each `lessons/` to `sessions/` and each `project/` to `practice/` (use `git mv`).
2. In track notes set `type: track` and add `kind`, `horizon`, `goal`, `done_criterion`, `deadline`, `if_then`; drop `period`.
3. In session notes set `type: session`, rename `course` to `track` and `lesson` to `session`, and replace the tag `type/lesson` with `type/session`.
4. In concept notes rename `courses` to `tracks` and `lessons` to `sessions`.
5. Copy the new scripts, templates, bases, skills, `.claude/hooks/format_note.py` and `90_System/Specs`, run `python3 -I 90_System/Scripts/build_index.py`, then run every check.

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
