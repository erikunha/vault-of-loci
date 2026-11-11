"""Writing rules of the vault that no other check enforces.

The AGENTS.md says: no em dash and no en dash, no Dataview or Templater syntax, and never
`end` as a node id in a Mermaid diagram. The other checks look at names, links, cards and the
study layer, so these three rules had nothing behind them.

The files that are not the vault's own prose are skipped: a folder with a `.vendored` marker is
a third party copy, a clipping is text pasted from the web, and the transcripts of the eval runs
are the record of what a model said. A dash inside a code block, inside a code span or inside a
URL is part of the example and not part of the prose.

The fences follow the CommonMark rules: a fence closes with the same character and with at least
the length of the one that opened it, and a fence that never closes is a problem of its own.

Usage: python3 -I 90_System/Scripts/validation/check_writing.py [root]   (exits 1 on any problem)
"""
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[3]
SKIP_DIRS = {".obsidian", "node_modules", ".git", ".trash", ".venv", ".smart-env", ".claude"}
# The run folders hold what a model said, and a clipping is text from the web.
SKIP_PREFIXES = ("90_System/Evals/runs/", "00_Inbox/Clippings/")
# The dash, the horizontal bar that looks like one, and the two ways of writing it in HTML.
DASHES = re.compile("[—–―]|&(?:mdash|ndash|#8212|#8211|#x2014|#x2013);")
# A quote marker and a list marker may come in front of a fence or of a line of a diagram. The
# quote marker takes one space with it at most, so the indent of a code block inside a quote stays.
QUOTE = re.compile(r"^\s{0,3}(?:>[ \t]?)*")
CONTAINER = re.compile(r"^\s{0,3}(?:>[ \t]?)*(?:[-*+]\s+)?")
FENCE = re.compile(CONTAINER.pattern + r"(`{3,}|~{3,})\s*(\S*)")
# A code span with any number of backticks, a URL, and a line indented as a code block.
INLINE_CODE = re.compile(r"(`+).*?\1")
URL = re.compile(r"https?://\S+")
INDENTED_CODE = re.compile(r"^\s{4,}|^\t")
# A block that asks for Dataview or Templater runs code the vault does not ship.
TEMPLATES = ("dataview", "dataviewjs", "templater")
# `end` closes a subgraph, so a line that is only `end` is fine. A node named `end` breaks the
# diagram, and that is a node the line starts with or a node an arrow points at.
MERMAID_END = re.compile(
    r"^\s*end(?=\s*[\[({]|\s*(?:-->|---|==>|-\.->|<--))"
    r"|(?:-->|---|==>|-\.->|<--)\s*end\b"
)


def vendored(path):
    return any((parent / ".vendored").exists() for parent in path.parents if parent >= root)


def notes():
    for path in sorted(root.rglob("*.md")):
        relative = path.relative_to(root)
        if SKIP_DIRS.intersection(relative.parts):
            continue
        if relative.as_posix().startswith(SKIP_PREFIXES) or vendored(path):
            continue
        yield path, relative


def prose(line):
    """The line without the parts that are not prose."""
    return INLINE_CODE.sub("", URL.sub("", line))


def indented(line):
    """True when the line is code: indented as a block, also inside a quote."""
    return bool(INDENTED_CODE.match(line) or INDENTED_CODE.match(QUOTE.sub("", line, count=1)))


problems = []
for path, relative in notes():
    inside = None
    for number, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), start=1):
        marker = FENCE.match(line)
        if inside is None:
            if marker:
                fence, info = marker.group(1), marker.group(2).lower()
                inside = (fence[0], len(fence), info)
                if info in TEMPLATES:
                    problems.append(f"dataview or templater block: {relative}:{number}")
            elif not indented(line) and DASHES.search(prose(line)):
                problems.append(f"em dash or en dash: {relative}:{number}")
            continue
        if marker and marker.group(1)[0] == inside[0] and len(marker.group(1)) >= inside[1] and not marker.group(2):
            inside = None
        elif inside[2] == "mermaid" and MERMAID_END.search(CONTAINER.sub("", line, count=1)):
            problems.append(f"end as a node id: {relative}:{number}")
    if inside is not None:
        problems.append(f"a fence that is never closed: {relative}")
for problem in problems:
    print(problem)
print("writing problems:", len(problems))
sys.exit(1 if problems else 0)
