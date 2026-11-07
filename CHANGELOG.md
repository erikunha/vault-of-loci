# Changelog

Notable changes to this template. Versions follow semantic versioning: a major version changes the folder layout or the note format, a minor version adds something, a patch fixes something.

## Unreleased

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
