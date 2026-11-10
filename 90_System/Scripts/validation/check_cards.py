"""Flashcards: every `question::answer` card and every cloze has a source link, and no question repeats.

A source is a wikilink, a Markdown link or a URL. A card has one when a link sits on the card line, or in
the section the card is in, or in a `## Related`, `## Concepts introduced` or `## Sources` section of the
same note, or when the note's frontmatter fills `link` or `source`. A cloze is a line with `==hidden==` text
in a note tagged `flashcards`. A question that
appears twice anywhere in the vault (ignoring case, punctuation and spacing) is a duplicate.
Skipped: frontmatter, code (fenced and inline), tables, quotes, `90_System/Templates`, `90_System/Specs`,
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
WIKILINK = re.compile(r"\[\[[^\]]+\]\]|\[[^\]]*\]\([^)\s]+\)|https?://\S+")
CLOZE = re.compile(r"==[^=\s][^=]*==")
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


def frontmatter_tags(head):
    """The tags of the frontmatter, in the inline form and in the list form.

    The vault writes the tags as a list in one line, and the properties the vault ships
    document the other form, a key with the items under it. A cloze in a note tagged
    `flashcards` is a card in either form.
    """
    tags = set()
    lines = head.splitlines()
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


def frontmatter_source(head):
    """True when the frontmatter fills `link` or `source` with a value that is there.

    An empty value is not a source. The key with nothing after it says the note has no source,
    the same as the key that is not there.
    """
    for match in re.finditer(r"^(link|source):[ \t]*(.*)$", head, flags=re.M):
        value = match.group(2).strip().strip("'\"")
        if value:
            return True
    return False


def parse(text):
    """Return (cards, sections): cards are (line number, question, line); sections map a heading
    index to its text, so a card knows the text of its own section."""
    front = re.match(r"---\n.*?\n---\n?", text, flags=re.DOTALL)
    head = front.group(0) if front else ""
    deck = "flashcards" in frontmatter_tags(head)
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
        if line.lstrip().startswith((">", "|")):
            continue
        card = CARD.match(line.strip())
        if card:
            cards.append((number, card.group("q").strip(), line, len(sections) - 1))
        elif deck and CLOZE.search(line):
            cards.append((number, line.strip(), line, len(sections) - 1))
    return cards, sections, frontmatter_source(head)


problems, seen = [], {}
for path, rel in notes():
    cards, sections, noted = parse(path.read_text(encoding="utf-8", errors="ignore"))
    shared = noted or any(WIKILINK.search("\n".join(s["lines"])) for s in sections if s["title"] in SOURCE_SECTIONS)
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
