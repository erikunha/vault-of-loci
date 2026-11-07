# FAQ

## Do I need AI agents to use this vault?

No. Everything is plain Markdown and works in Obsidian alone. The agent files only matter if you use Claude Code, Codex, Gemini CLI, Copilot or Cursor.

## Do I need Python?

Only for the checks and the naming tool (Python 3.10 or later, standard library only). The vault itself does not need it.

## Which Obsidian version?

Obsidian 1.9 or later, because the dashboards use Bases.

## The community plugin is listed but not installed. Is that a bug?

No. Plugin code is not committed, so each copy installs its own. Spaced Repetition is the only community plugin the vault uses, and it is optional: open Settings, Community plugins, and install it to review flashcards. The vault opens and the dashboards work without it.

## Can I write my notes in another language?

Yes. Note text can be in any language. The study layer headings are fixed by the checks; the README section "Customize" lists every file to change if you rename them.

## Why underscores in file names?

Names without spaces work the same in links, URLs, shells and scripts. The title inside the note keeps spaces, and links show the readable name. Run `normalize_names.py --write` to fix names created by hand.

## Why does every note have flashcards?

Remembering by answering a question (retrieval practice) and spreading reviews over time (spacing) are two of the best supported study techniques. The guide `40_References/Guides/Studying_with_AI.md` explains the evidence.

## Will an agent just answer for me instead of teaching me?

The rules in `AGENTS.md` and the study guide ask agents to quiz you, explain your mistakes and cite sources. You stay in charge: ask for questions before asking for answers.

## Where do agents record what they did?

In `90_System/Agent_Log/YYYY-MM.md`, one line per task. Agents read the current month before starting.

## Can I delete the example course, concept and paper?

Yes. They only show the full note format. Run the checks after deleting them to catch broken links.

## How do I keep my copy up to date with the template?

A copy made with "Use this template" has no link to this repository. Read `CHANGELOG.md` and copy the changes you want, usually scripts, templates and specs.

## Can I keep my vault private?

Yes. Create your copy as a private repository, or keep it only on your machine. Never commit `.env` files or plugin `data.json` files; `.gitignore` and `.claude/settings.json` already guard against both.
