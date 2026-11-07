# FAQ

## Do I need AI agents to use this vault?

No. Everything is plain Markdown and works in Obsidian alone. The agent files only matter if you use Claude Code, Codex, Gemini CLI, Copilot or Cursor.

## Do I need Python?

Only for the checks and the naming tool (Python 3.10 or later, standard library only). The vault itself does not need it.

## Which Obsidian version?

Obsidian 1.9 or later, because the dashboards use Bases. The optional `review-queue` skill uses the Obsidian CLI and needs Obsidian 1.12.7 or later with the app running; without it, the skill reads the files.

## The community plugin is listed but not installed. Is that a bug?

No. Plugin code is not committed, so each copy installs its own. Spaced Repetition is the only community plugin the vault uses, and it is optional: open Settings, Community plugins, and install it to review flashcards. The vault opens and the dashboards work without it.

## Can I write my notes in another language?

Yes. Note text can be in any language. The study layer headings are fixed by the checks; the README section "Customize" lists every file to change if you rename them.

## Why underscores in file names?

Names without spaces work the same in links, URLs, shells and scripts. The title inside the note keeps spaces, and links show the readable name. Run `normalize_names.py --write` to fix names created by hand.

## Why does every note have flashcards?

Remembering by answering a question (retrieval practice) and spreading reviews over time (spacing) are two of the best supported study techniques. The guide `40_References/Guides/Studying_with_AI.md` explains the evidence.

## Will an agent just answer for me instead of teaching me?

Not if it follows tutor mode, which `AGENTS.md` and the skills require: you attempt first, hints come in steps (hint, strong hint, partial example, answer) only after an attempt, you rate confidence from 1 to 5 before the reveal, and the agent never writes your study layer or your answers. You stay in charge: ask for questions before asking for answers.

## Where do agents record what they did?

In `90_System/Agent_Log/YYYY-MM.md`, one line per task. Agents read the current month before starting.

## Can I delete the example course, concept and paper?

Yes. They only show the full note format. Run the checks after deleting them to catch broken links.

## How do I keep my copy up to date with the template?

A copy made with "Use this template" has no link to this repository. Read `CHANGELOG.md` and copy the changes you want, usually scripts, templates and specs.

## Can I keep my vault private?

Yes. Create your copy as a private repository, or keep it only on your machine. Never commit `.env` files or plugin `data.json` files; `.gitignore` and `.claude/settings.json` already guard against both.

## What are the checkpoint, pretest and mistake skills?

Skills for agents that follow tutor mode. `pretest` writes questions you guess before a lesson. `no-ai-checkpoint` quizzes you closed book on concepts older than 14 days and logs `last_tested` and `score`. `teach-the-agent` lists the gaps in your explanation. `mistake-review` turns logged mistakes into corrected cards with a source. `review-queue` lists what to study next. The guide `40_References/Guides/Studying_with_AI.md` has the protocol and the evidence.

## Should I switch the Spaced Repetition plugin to FSRS?

It is optional. The plugin offers FSRS since version 1.15.0. Back up the vault and the plugin's `data.json` first, then pick FSRS in the plugin settings. The FSRS benchmark measures how well an algorithm predicts recall, not how much you learn. The guide has the steps.

## Does the vault ship an MCP server configuration for Obsidian?

No. An Obsidian MCP server usually needs an API key from a community plugin, and a key must never be committed to a shared repository. It would also repeat what the Obsidian CLI (1.12.7 or later) and plain file access already give an agent, and it adds a tool that reads note text, which is a place for injected instructions to enter. The vault must work without community plugins. If you want one, add a configuration in your own copy with the key in an environment variable that stays out of Git, and keep it out of the shared template.
