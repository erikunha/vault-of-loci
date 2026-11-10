"""Export the vault's flashcards to a TSV file that Anki imports.

Cards are `question::answer` lines and cloze lines with `==hidden==` text, the same
format `check_cards.py` reads: a cloze is a card in a note tagged `flashcards`. Each card goes to a deck named after its track
(`Vault of Loci::<track folder>`) or after its top folder for shared notes. Wikilinks
become their readable text. A `::` inside inline code does not make a card. Notes in templates, specs and tool folders are skipped.

Dry run by default: prints a summary and the first lines. `--out FILE` writes the file,
which Anki opens with File > Import (the header lines set the note type, deck and tags).

Usage: python3 -I 90_System/Scripts/export_anki_tsv.py [--root DIR] [--out cards.tsv]
"""
import argparse
import re
from pathlib import Path

SKIP_DIRS = {".obsidian", "node_modules", ".git", ".trash", ".venv", ".claude", ".agents"}
SKIP_PREFIXES = ("90_System/Templates/", "90_System/Specs/", "90_System/Agent_Log/")
CARD = re.compile(r"^(?:[-*+]\s+|\d+[.)]\s+)?(?P<q>[^:#>|`][^:]*?(?::(?!:)[^:]*?)*?)::(?P<a>.*\S.*)$")
CLOZE = re.compile(r"==([^=]+)==")
LINK = re.compile(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]")
FENCE = re.compile(r"^(`{3,}|~{3,})")
DECK = "Vault of Loci"


def clean(text):
    return " ".join(LINK.sub(r"\1", text).replace("\t", " ").split())


def deck(rel):
    parts = rel.parts
    if parts[0] == "10_Tracks" and len(parts) > 2:
        return f"{DECK}::{parts[1]}"
    return f"{DECK}::{parts[0]}"


def body(text):
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            return text[end + 4:]
    return text


def tags_of(text):
    """The tags of the frontmatter, in the inline form and in the list form."""
    tags = set()
    lines = text.splitlines()
    for index, line in enumerate(lines):
        match = re.match(r"^tags:[ \t]*(.*)$", line)
        if not match:
            continue
        value = match.group(1).strip()
        if value.startswith("[") and value.endswith("]"):
            tags.update(item.strip().strip("'\"") for item in value[1:-1].split(","))
        elif value:
            tags.add(value.strip("'\""))
        else:
            for follow in lines[index + 1:]:
                item = re.match(r"^[ \t]*-[ \t]*(.*)$", follow)
                if not item:
                    break
                tags.add(item.group(1).strip().strip("'\""))
    return tags


def cards(root):
    for path in sorted(root.rglob("*.md")):
        rel = path.relative_to(root)
        if SKIP_DIRS.intersection(rel.parts) or rel.as_posix().startswith(SKIP_PREFIXES):
            continue
        if any((p / ".vendored").exists() for p in path.parents if p >= root):
            continue
        tag = re.sub(r"[^\w-]", "_", path.stem)
        text = path.read_text(encoding="utf-8")
        # A cloze is a card in a note tagged `flashcards`, the same rule `check_cards.py` reads.
        deck_of_clozes = "flashcards" in tags_of(text)
        fenced = False
        for line in body(text).splitlines():
            if FENCE.match(line.strip()):
                fenced = not fenced
                continue
            if fenced:
                continue
            line = line.strip()
            masked = re.sub(r"`[^`\n]*`", lambda c: "x" * len(c[0]), line)
            m = CARD.match(masked)
            if m:
                yield "Basic", deck(rel), clean(line[m.start("q"):m.end("q")]), clean(line[m.start("a"):m.end("a")]), tag
            elif deck_of_clozes and CLOZE.search(line) and not line.lstrip().startswith((">", "|", "#")):
                count = iter(range(1, 100))
                cloze = CLOZE.sub(lambda c: "{{c%d::%s}}" % (next(count), c[1]), line)
                yield "Cloze", deck(rel), clean(re.sub(r"^\s*[-*+]\s+", "", cloze)), "", tag


def render(rows):
    head = ["#separator:tab", "#html:false", "#notetype column:1", "#deck column:2", "#tags column:5"]
    return "\n".join(head + ["\t".join(r) for r in rows]) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--out", type=Path, help="write the TSV here (default: dry run)")
    args = parser.parse_args()
    rows = list(cards(args.root))
    text = render(rows)
    basic = sum(r[0] == "Basic" for r in rows)
    print(f"cards: {len(rows)} ({basic} basic, {len(rows) - basic} cloze) in {len({r[1] for r in rows})} decks")
    if args.out:
        args.out.write_text(text, encoding="utf-8")
        print("written:", args.out)
    else:
        print("\n".join(text.splitlines()[5:10]))


if __name__ == "__main__":
    main()
