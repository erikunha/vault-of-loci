---
type: spec
summary: The scripts that ship with the vault (checks, naming, transcripts, maps, export) and how to customize language, kinds, categories, folders and agents.
tags: [type/spec]
---

# Tools and customization

Every script uses the Python 3.10+ standard library only. Scripts that write files print a dry run unless you pass `--write` or an output file.

## Checks

One command runs them all and reports each one as passed or FAILED:

```bash
python3 -I 90_System/Scripts/run_checks.py
```

It runs `format_notes.py --check`, then every `validation/check_*.py`, then every `validation/test_*.py`. A new check is picked up by its file name. The same command runs on every push in `.github/workflows/checks.yml`.

| Check | What it guards |
|---|---|
| `format_notes.py --check` | Spacing in every note |
| `check_links.py` | Wikilinks, Markdown links, `obsidian://` links, `README.md` and `llms.txt` |
| `check_study_layer.py` | The study layer is present and in order |
| `check_names.py` | No spaces in file and folder names |
| `check_cards.py` | Every card and cloze has a source link, and no question repeats |
| `check_skills.py` | Skill files follow the Agent Skills spec |
| `check_bases.py` | Bases never list the note templates |
| `check_study_layer_translations.py` | Translations keep the same keys |
| `check_alt_text.py` | Every image has alt text |
| `check_readme_translations.py` | Each translated README keeps the same headings and file names as `README.md` |
| `check_index.py` | `INDEX.md` and `index.json` are current |
| `test_*.py` | Each script above and below has a test |

If `check_index.py` fails, rebuild the index with `python3 -I 90_System/Scripts/build_index.py`. The Claude Code hook does it after each note edit. To catch a stale index before it reaches a commit, enable the pre-commit hook once per clone: `git config core.hooksPath .githooks`.

## Contributors table

`.all-contributorsrc` lists every contributor and the kinds of contribution, in the [All Contributors](https://allcontributors.org) format. `update_contributors.py` adds each commit author of the GitHub repository (bots left out) with `code`, keeps the entries added by hand, and writes a table between the `ALL-CONTRIBUTORS-LIST` markers of each file in `files`: a 100 px avatar fetched at 200 px, the name, and one emoji per kind. People with more kinds come first. To credit a contribution that is not a commit, add the person or the kind to `.all-contributorsrc` and run the script. `.github/workflows/contributors.yml` runs it on every push to `main` and every Monday, and commits only when something changed.

## Naming

File and folder names use underscores instead of spaces (`Retrieval_Practice.md`). The title inside the note keeps spaces, and links show the readable name: `[[Retrieval_Practice|Retrieval practice]]`. To fix names created by hand (files and folders, deepest first; folders marked `.vendored` are skipped):

```bash
python3 90_System/Scripts/normalize_names.py          # dry run
python3 90_System/Scripts/normalize_names.py --write  # rename (git mv when tracked) and rewrite every link
```

## Transcripts

A lecture, talk or video with subtitles becomes a note an agent can read by section:

```bash
python3 -I 90_System/Scripts/vtt_to_note.py talk.vtt --track 01_Example_Course --write   # WebVTT or SRT to 10_Tracks/<track>/transcripts/
python3 -I 90_System/Scripts/transcript_sections.py --write   # a ## HH:MM:SS heading about every 10 minutes
python3 -I 90_System/Scripts/transcript_sections.py --report  # notes over 300 lines with no heading
```

## Maps

```bash
python3 -I 90_System/Scripts/build_canvas.py --write   # 30_Maps/<Track>.canvas: track, practice files, sessions and the concepts they link
```

## Export

```bash
python3 -I 90_System/Scripts/export_anki_tsv.py --out cards.tsv   # cards and clozes for Anki (File > Import), one deck per track
python3 -I 90_System/Scripts/export_bibtex.py --out refs.bib --csl-out refs.json   # reference notes for Zotero, Pandoc or LaTeX
```

## Customize

- **Language.** The study layer headings are set in one file, `90_System/Specs/study_layer.json`, which `check_study_layer.py` reads. A Portuguese version ships as `study_layer.pt-BR.json`: copy it over `study_layer.json` to switch. Change them there, then in the `Concept` and `Reference` templates, in `90_System/Specs/Study_layer.md` and in the existing notes. Note text can be in any language.
- **Track kinds.** Recipes live in `90_System/Specs/Track_kinds.md`; the `new-track` skill reads them. Edit a recipe or add a kind there.
- **Concept categories.** Each category is a `cat/<name>` tag with a color in `.obsidian/graph.json` and `.obsidian/snippets/study-vault.css`. Add or rename them in both places.
- **Folders.** The numbered top folders are referenced by `llms.txt`, the skills and the checks (the bases filter by the `type` property, not by folder). Rename one and run the checks to find what still points to the old name.
- **Agents.** Add rules to `AGENTS.md` only. `CLAUDE.md` and `GEMINI.md` stay as one import line. Add other secret paths to `.cursorignore`, `.geminiignore` and `.claude/settings.json`.
