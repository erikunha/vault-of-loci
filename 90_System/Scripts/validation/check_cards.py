"""Flashcards: every `question::answer` card has a source link and no question repeats.

A card has a source when a wikilink sits on the card line, or in the section the card is in, or in a
`## Related`, `## Concepts introduced` or `## Sources` section of the same note. A question that
appears twice anywhere in the vault (ignoring case, punctuation and spacing) is a duplicate.
Skipped: frontmatter, code (fenced and inline), `90_System/Templates`, `90_System/Specs`,
`90_System/Agent_Log`, folders with a `.vendored` file and tool folders.

Usage: python3 -I 90_System/Scripts/validation/check_cards.py [root]   (exits 1 on any problem)
"""
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[3]
SKIP_DIRS = {".obsidian", "node_modules", ".git", ".trash", ".venv", ".smart-env", ".claude", ".agents"}
SKIP_PREFIXES = ("90_System/Templates/", "90_System/Specs/", "90_System/Agent_Log/")
SOURCE_SECTIONS = {"related", "concepts introduced", "sources"}
WIKILINK = re.compile(r"\[\[[^\]]+\]\]")
CARD = re.compile(r"^(?:[-*+]\s+|\d+[.)]\s+)?(?P<q>[^:#>|`][^:]*?(?::(?!:)[^:]*?)*?)::(?P<a>.*\S.*)$")


def vendored(path):
    return any((parent / ".vendored").exists() for parent in path.parents if parent >= root)


def notes():
    for p in sorted(root.rglob("*.md")):
        rel = p.relative_to(root)
        if SKIP_DIRS.intersection(rel.parts) or rel.as_posix().startswith(SKIP_PREFIXES) or vendored(p):
            continue
        yield p, rel


def normalize(question):
    question = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]", r"\1", question)
    return " ".join(re.sub(r"[^\w\s]", " ", question.casefold()).split())


def parse(text):
    """Return (cards, sections): cards are (line number, question, line); sections map a heading
    index to its text, so a card knows the text of its own section."""
    front = re.match(r"---\n.*?\n---\n?", text, flags=re.DOTALL)
    skipped = text[: front.end()].count("\n") if front else 0
    lines = text.splitlines()[skipped:]
    sections, cards, fence = [{"title": "", "lines": []}], [], None
    for offset, raw in enumerate(lines):
        number = skipped + offset + 1
        marker = re.match(r"\s*(`{3,}|~{3,})", raw)
        if marker:
            fence = None if fence == marker.group(1)[0] else (fence or marker.group(1)[0])
            continue
        if fence:
            continue
        line = re.sub(r"`[^`\n]*`", "", raw)
        heading = re.match(r"#{1,6}\s+(.*?)\s*$", line)
        if heading:
            sections.append({"title": heading.group(1).strip().casefold(), "lines": []})
            continue
        sections[-1]["lines"].append(line)
        card = CARD.match(line.strip())
        if card:
            cards.append((number, card.group("q").strip(), line, len(sections) - 1))
    return cards, sections


problems, seen = [], {}
for path, rel in notes():
    cards, sections = parse(path.read_text(encoding="utf-8", errors="ignore"))
    shared = any(WIKILINK.search("\n".join(s["lines"])) for s in sections if s["title"] in SOURCE_SECTIONS)
    for number, question, line, index in cards:
        where = f"{rel}:{number}"
        if not (WIKILINK.search(line) or shared or WIKILINK.search("\n".join(sections[index]["lines"]))):
            problems.append(f"no source link: {where}: {question}")
        key = normalize(question)
        if key in seen:
            problems.append(f"duplicate question: {where} repeats {seen[key]}: {question}")
        else:
            seen[key] = where
for problem in problems:
    print(problem)
print("flashcard problems:", len(problems))
sys.exit(1 if problems else 0)
