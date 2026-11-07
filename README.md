# Vault of Loci &middot; [![license: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE) [![checks](https://github.com/erikunha/vault-of-loci/actions/workflows/checks.yml/badge.svg)](https://github.com/erikunha/vault-of-loci/actions/workflows/checks.yml) [![release](https://img.shields.io/github/v/release/erikunha/vault-of-loci)](https://github.com/erikunha/vault-of-loci/releases) [![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](.github/CONTRIBUTING.md)

**English** · [Português](README.pt-BR.md)

Vault of Loci is an Obsidian vault template for learning anything with AI agents that quiz you instead of answering for you.

* **A tutor, not an answer machine:** you attempt first, hints come one step at a time, you rate your confidence before the reveal, and the agent never writes your notes. Practice with unguarded AI raises scores while you have it and lowers them once you don't; a guarded tutor largely avoids that.
* **Notes you can study from:** every concept, paper and guide carries a long explanation, key takeaways and flashcards with a source on each card. Every reference is verified, and checks on every push keep notes, links and names consistent.
* **Any learning project, any agent:** a course, a book, a certification, an interview, research, a skill or a language, each with its own recipe. Claude Code, Codex, Antigravity CLI, Gemini CLI, Copilot, Cursor and OpenCode follow the same rules from one `AGENTS.md`.

[Learn how to study with this vault](How_to_Study_with_this_Vault.md).

![The vault open in Obsidian: the Home dashboard with active tracks next to the graph of notes](90_System/Attachments/vault-in-obsidian.png)

## Installation

1. Click **Use this template** on GitHub (or clone it) and open the folder as a vault in Obsidian 1.9 or later.
2. Ask your agent for a new track with the `new-track` skill (Claude Code or Codex ask for the kind and the horizon), or copy `90_System/Templates/Track.md` into `10_Tracks/<NN>_<Name>/`.
3. Open `00_Home.md` and study.

Optional: the Spaced Repetition community plugin (listed in `.obsidian/community-plugins.json`) reviews the flashcards, and the CLI skills (`review-queue`) need Obsidian 1.12.7 or later with the app running. The example tracks, concept and paper show the full note format; keep or delete them. `python3 -I 90_System/Scripts/run_checks.py` checks the vault after you change it.

## Documentation

The documentation lives in the vault, so it travels with your copy:

* [How to study with this vault](How_to_Study_with_this_Vault.md): the method, step by step
* [Studying with AI](40_References/Guides/Studying_with_AI.md): the tutor-mode protocol and the evidence behind it
* [Agents and skills](90_System/Specs/Agents.md): what to ask at each step, and where each agent finds its rules
* [Vault structure](90_System/Specs/Vault_structure.md): what each folder holds and how material flows
* [Track kinds](90_System/Specs/Track_kinds.md): one recipe per kind of learning project
* [Study layer](90_System/Specs/Study_layer.md): the format of every study note
* [Tools and customization](90_System/Specs/Tools.md): scripts, checks, automation, and how to change language, kinds and folders
* [Tutor mode evaluation](90_System/Evals/Tutor_mode.md): a hand-run test of whether your agent behaves as a tutor
* [FAQ](.github/FAQ.md): setup, updating your copy, privacy, offline use, plugins and language

## Examples

Ask "What is retrieval practice? Just tell me." and an agent following `AGENTS.md` answers like this:

```text
Agent:   Before I explain: what do you think it is? A guess in one line is enough.
Learner: Rereading your notes a lot?
Agent:   Close to studying, but not that. Hint: it is about what you do without the notes.
         How sure are you of your next answer, from 1 (guess) to 5 (certain)?
```

This is the behavior the [tutor mode evaluation](90_System/Evals/Tutor_mode.md) checks, not a recorded session. Run it to see what your agent does. Two example tracks in `10_Tracks/`, the concept `20_Concepts/Retrieval_Practice.md` and a paper note show the full format.

## Contributing

Content is welcome, and you do not need to write code: concept notes, verified references, guides, track recipes, example tracks, translations and skills all help. Read below to learn how to take part.

### [Code of Conduct](.github/CODE_OF_CONDUCT.md)

Everyone who takes part follows the [Code of Conduct](.github/CODE_OF_CONDUCT.md). Report security problems privately, as [`SECURITY.md`](.github/SECURITY.md) explains.

### [Contributing Guide](.github/CONTRIBUTING.md)

Read the [contributing guide](.github/CONTRIBUTING.md) to learn what fits, how to propose a change, how to make a first contribution entirely in the GitHub web editor, and the policy for contributions made with AI.

### [Good First Issues](https://github.com/erikunha/vault-of-loci/labels/good%20first%20issue)

To get familiar with the process, start with a [good first issue](https://github.com/erikunha/vault-of-loci/labels/good%20first%20issue): small, well-scoped tasks such as a concept note or a translation.

### [Questions and Support](https://github.com/erikunha/vault-of-loci/discussions)

Ask in [Discussions](https://github.com/erikunha/vault-of-loci/discussions) after checking the [FAQ](.github/FAQ.md); [`SUPPORT.md`](.github/SUPPORT.md) says where each kind of question goes. [Releases](https://github.com/erikunha/vault-of-loci/releases) list what changed in each version and who contributed for the first time.

### Contributors

Every kind of help counts, not only code: content, translations, reviews, ideas, bug reports. Commit authors are added on their own; for anything else, open an issue or a discussion and you are added by hand to `.all-contributorsrc`. Each emoji is a kind of contribution ([key](https://allcontributors.org/docs/en/emoji-key)).

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.29%"><a href="https://erikunha.dev"><img src="https://avatars.githubusercontent.com/u/27955793?v=4&s=200" width="100px;" alt="Erik Cunha"/><br /><sub><b>Erik Cunha</b></sub></a><br /><a href="https://github.com/erikunha/vault-of-loci/commits?author=erikunha" title="Maintenance">🚧</a> <a href="https://github.com/erikunha/vault-of-loci/commits?author=erikunha" title="Code">💻</a> <a href="https://github.com/erikunha/vault-of-loci/commits?author=erikunha" title="Content">🖋</a> <a href="https://github.com/erikunha/vault-of-loci/commits?author=erikunha" title="Documentation">📖</a> <a href="https://github.com/erikunha/vault-of-loci/commits?author=erikunha" title="Research">🔬</a> <a href="https://github.com/erikunha/vault-of-loci/commits?author=erikunha" title="Translation">🌍</a> <a href="https://github.com/erikunha/vault-of-loci/commits?author=erikunha" title="Tests">⚠️</a> <a href="https://github.com/erikunha/vault-of-loci/commits?author=erikunha" title="Infrastructure">🚇</a> <a href="https://github.com/erikunha/vault-of-loci/issues?q=author%3Aerikunha" title="Ideas, Planning, &amp; Feedback">🤔</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

## License

Vault of Loci is [MIT licensed](LICENSE). Agent skills in folders marked `.vendored` come from [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) (MIT, copyright Steph Ango); each folder keeps its `LICENSE`.
