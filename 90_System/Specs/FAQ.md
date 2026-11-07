---
type: spec
summary: Common questions about setup, updating your copy, privacy, offline use, plugins, language and agents.
tags: [type/spec]
---

# FAQ

## What can I learn with it?

Anything you can set a goal for: a course, a book, a certification, an interview, research, a skill or a language. Each learning project is a track with a kind, a goal and a done criterion, and `90_System/Specs/Track_kinds.md` has one recipe per kind. Ask for the `new-track` skill, or copy `90_System/Templates/Track.md`. A kind that is missing can start as `other` with a done criterion you can fail.

## Where can I ask a question or show what I built?

In [GitHub Discussions](https://github.com/erikunha/vault-of-loci/discussions): Q&A for questions, Ideas for proposals you want to talk through, Show and tell for your own vault. Bugs go in an issue, with the steps and the output. You can write in Portuguese or English.

## Do I need AI agents to use this vault?

No. Everything is plain Markdown and works in Obsidian alone. The agent files only matter if you use an agent such as Claude Code, Codex, Antigravity CLI, Gemini CLI, Copilot, Cursor or OpenCode. The README table "Supported agents" lists what each one reads.

## Do I need Python?

Only for the checks, the naming tool and the index builder (Python 3.10 or later, standard library only). The vault itself does not need it.

## Which Obsidian version?

Obsidian 1.9 or later, because the dashboards use Bases. Obsidian 1.12.7 or later is needed only for the optional skills that call the Obsidian CLI (`review-queue`), with the app running; without it, the skill reads the files.

## The community plugin is listed but not installed. Is that a bug?

No. Plugin code is not committed, so each copy installs its own. Spaced Repetition is the only community plugin the vault uses, and it is optional: open Settings, Community plugins, and install it to review flashcards. The vault opens and the dashboards work without it.

## Can I write my notes in another language?

Yes. Note text can be in any language. The study layer headings are set in `90_System/Specs/study_layer.json`; [Tools and customization](Tools.md#customize) lists what to change if you rename them. A Portuguese version ships ready: copy `study_layer.pt-BR.json` over `study_layer.json`. To add another language, create `study_layer.<language>.json` with the same keys; `check_study_layer_translations.py` checks them.

## Why underscores in file names?

Names without spaces work the same in links, URLs, shells and scripts. The title inside the note keeps spaces, and links show the readable name. Run `normalize_names.py --write` to fix names created by hand.

## Why does every note have flashcards?

Remembering by answering a question (retrieval practice) and spreading reviews over time (spacing) are two of the best supported study techniques. The guide `40_References/Guides/Studying_with_AI.md` explains the evidence.

## Will an agent just answer for me instead of teaching me?

Not if it follows tutor mode, which `AGENTS.md` and the skills require: you attempt first, hints come in steps (hint, strong hint, partial example, answer) only after an attempt, you rate confidence from 1 to 5 before the reveal, and the agent never writes your study layer or your answers. You stay in charge: ask for questions before asking for answers. Tutor mode is an instruction, and an agent can still ignore it. In Claude Code the vault adds a lock: every edit in your own notes (`10_Tracks/`, `20_Concepts/`, `50_Review/`) asks you first, unless you run it in a mode that skips permission prompts. Other agents have no such setting here. To see how well your agent follows the rules, run the twelve scenarios in `90_System/Evals/Tutor_mode.md`.

## How does an agent find the right note without reading everything?

Through the generated index. `INDEX.md` has one line per note (type, line count, summary) and `90_System/index.json` lists every heading with its line number, so an agent reads the index and then only the line range it needs. The Claude Code hook rebuilds both after each note edit; `check_index.py` fails when they are out of date, and `python3 -I 90_System/Scripts/build_index.py` fixes it.

## Where do agents record what they did?

In `90_System/Agent_Log/YYYY-MM.md`, one line per task. Agents read the current month before starting.

## Can I delete the example tracks, concept and paper?

Yes. They only show the full note format. Run the checks after deleting them to catch broken links, then rebuild the index with `python3 -I 90_System/Scripts/build_index.py`.

## Updating your copy

A copy made with "Use this template" has no link to this repository, so compare against a release instead of merging.

1. Add this repository as a remote named `template` and fetch its tags: `git fetch template --tags`.
2. Find the release you copied from (the release whose date is closest before your copy, on the Releases page) and the latest tag with `git tag --list --sort=-v:refname`.
3. See what changed in the files you share with the template: `git diff <old-tag> <latest-tag> -- 90_System/Scripts 90_System/Specs 90_System/Templates .agents .claude .github AGENTS.md`.
4. Apply what you want. For a file you never customized, `git checkout <latest-tag> -- <path>` copies it. For one you changed, merge by hand.
5. Read the release notes of each version first (Releases page): a layout change such as 0.2.0 lists the renames to make in your notes. Then run every check and `build_index.py`.

Your notes in `10_Tracks/`, `20_Concepts/`, `40_References/` and `50_Review/` are not in that diff.

## Can I keep my vault private?

Yes. Create your copy as a private repository, or keep it only on your machine. Never commit `.env` files or plugin `data.json` files; `.gitignore` already keeps them out of Git. Keeping them out of an agent's view is a separate matter, covered in the next answer.

## Does the vault keep secrets away from agents?

Only partly, and the strength depends on the agent.

- **Claude Code.** The `permissions.deny` rules in `.claude/settings.json` cover its file tools and simple shell reads, but not every command a shell can run. The real guard is the sandbox (`sandbox.enabled`). It is off by default, and the template does not turn it on, because it can block hooks and commands you rely on. The sandbox covers shell commands only. Turn it on in your own settings if you keep secrets in the vault. See https://code.claude.com/docs/en/sandboxing.
- **Codex.** In a trusted project, `.codex/config.toml` can deny reads of matching files. This example follows https://developers.openai.com/codex/permissions; check that page for the current syntax before you rely on it:

  ```toml
  default_permissions = "vault"

  [permissions.vault.filesystem]
  ":minimal" = "read"

  [permissions.vault.filesystem.":workspace_roots"]
  "." = "write"
  "**/.env" = "deny"
  "**/.env.*" = "deny"
  ```

  Codex ignores project `.codex/` files in an untrusted project, so this protects nothing there.
- **Cursor and Gemini CLI.** `.cursorignore` and `.geminiignore` list `.env`, `.env.*` and plugin `data.json`. They keep those files out of context, but a terminal command or a tool can still read them. Cursor says so for its terminal and MCP tools.
- **Other agents** rely on the rule in `AGENTS.md` and on what you choose to put in the vault. Do not keep a secret in a vault you open with an agent.

## What does an agent send to its provider?

Whatever it reads. When an agent opens a note, or `INDEX.md` with its summaries, that text goes to the provider of the model it runs on. Private notes and exam material belong in a vault you only open with a local model, or without an agent. The deny rules and ignore files keep secrets out, not note text. Read your provider's data terms before you point an agent at notes you cannot share.

## Studying privately with a local model

A local model keeps your notes on your machine. Two ways to run Claude Code against one:

- **Ollama.** Run `ollama launch claude`, or set `ANTHROPIC_BASE_URL=http://localhost:11434` (with `ANTHROPIC_AUTH_TOKEN=ollama` and an empty `ANTHROPIC_API_KEY`) and start `claude --model <model>`. Give the model a context window of 64k tokens or more, or the rules and the index will not fit. See https://docs.ollama.com/integrations/claude-code.
- **LM Studio.** Its local server answers Anthropic-style requests at `/v1/messages`. Set `ANTHROPIC_BASE_URL=http://localhost:1234` (no `/v1`) and `ANTHROPIC_AUTH_TOKEN=lmstudio`, then start `claude --model <model>`. See https://lmstudio.ai/docs/developer/anthropic-compat.

A small local model follows the tutor-mode rules less reliably than a large one, so check its first answers. Keep private notes out of any vault you also open with a cloud agent: the agent sends what it reads.

## AI inside Obsidian

Community plugins can put a model inside Obsidian itself. They fall into three groups:

- Chat with a local or OpenAI-compatible model, in a side panel.
- Local semantic search, which builds embeddings of your notes on your machine.
- A local REST API for the vault, which MCP servers build on.

Before you install one, check that it is still maintained and what it sends where: a plugin that calls a cloud model sends the note text it reads, like any cloud agent. The vault works without them (see the answer on community plugins), and the skills here need none.

## Does it work offline?

The vault does: Obsidian, the Markdown notes, the bases, the Spaced Repetition plugin and the Python checks need no network. Agents need a network unless they run a local model. The `defuddle` skill and any link you open need one too. Notes saved in `40_References/Web` stay readable offline.

## Do I lose a streak when I skip a day?

There is no streak counter. Missing a day costs nothing, and the weekly review asks how many days you studied, not whether the chain broke. A backlog is handled by the "catch up backlog" mode in `review-queue`, not by catching up all at once.

## Should I study in my learning style?

No. The evidence does not support matching teaching to visual, auditory or kinesthetic styles. Match the method to the material. The rituals in `90_System/Specs/Track_kinds.md` list the evidence.

## What are the checkpoint, pretest and mistake skills?

Skills for agents that follow tutor mode. `pretest` writes questions you guess before a session. `no-ai-checkpoint` quizzes you closed book on concepts older than 14 days and logs `last_tested` and `score`. `teach-the-agent` lists the gaps in your explanation. `mistake-review` turns logged mistakes into corrected cards with a source. `review-queue` lists what to study next. The guide `40_References/Guides/Studying_with_AI.md` has the protocol and the evidence.

## Should I switch the Spaced Repetition plugin to FSRS?

It is optional. The plugin offers FSRS since version 1.15.0. Back up the vault and the plugin's `data.json` first, then pick FSRS in the plugin settings. The FSRS benchmark measures how well an algorithm predicts recall, not how much you learn. The guide has the steps.

## Can I review the cards in Anki or cite the references in Zotero?

Yes. `export_anki_tsv.py --out cards.tsv` writes every card and cloze to a file Anki imports with File > Import, one deck per track; the header lines set the note type, deck and tags. `export_bibtex.py --out refs.bib --csl-out refs.json` turns the reference notes into BibTeX and CSL JSON, which Zotero, Pandoc and LaTeX read. A reference with `verified: false` is exported with the note "not verified". The vault stays the source; export again after you edit.

## Does the vault ship an MCP server configuration for Obsidian?

No. MCP is optional here, and none is shipped. The servers for Obsidian either need an API key from a community plugin, and a key must never be committed to a shared repository, or they repeat what the Obsidian CLI (1.12.7 or later) and plain file access already give an agent. A server also adds a tool that reads note text, which is a place for injected instructions to enter. The vault must work without community plugins. If you want one, add a configuration in your own copy with the key in an environment variable that stays out of Git, and keep it out of the shared template.
