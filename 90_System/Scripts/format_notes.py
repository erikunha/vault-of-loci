"""Normalize note spacing: one blank line between blocks of different kinds.

Usage: python3 -I 90_System/Scripts/format_notes.py [--check]

Rules (outside frontmatter, code fences and $$ math blocks):
- headings, callouts, tables, horizontal rules, code fences and math blocks are separated from neighbors by one blank line;
- lists and paragraphs are separated by one blank line (indented lines right after an item continue it);
- consecutive lines of the same kind (list items, callout lines, table rows, a paragraph) stay together;
- two or more blank lines collapse into one.
A paragraph glued to a callout renders inside the callout; the separation fixes that.
Folders containing a `.vendored` marker hold third-party files and are left untouched.
"""
import re
import sys
from pathlib import Path

VAULT = Path(__file__).resolve().parents[2]
SKIP = {".claude", ".obsidian", ".venv", "node_modules", ".git", ".trash", ".smart-env"}


def kind(line, previous):
    s = line.strip()
    if not s:
        return "blank"
    if re.match(r"#{1,6} ", line):
        return "heading"
    if line.startswith(">"):
        return "callout"
    if s.startswith("|"):
        return "table"
    if re.fullmatch(r"(-{3,}|\*{3,}|_{3,})", s):
        return "hr"
    if re.match(r"\s*([-*+]|\d+[.)]) ", line):
        return "list"
    if line[:1] in (" ", "\t") and previous in ("list", "cont"):
        return "cont"
    return "paragraph"


def needs_gap(a, b):
    if a == b:
        return a in ("heading", "hr", "code")
    return not {a, b} <= {"list", "cont"}


def format_text(text):
    lines = text.split("\n")
    out, i = [], 0
    if lines and lines[0] == "---":
        end = next((k for k in range(1, len(lines)) if lines[k] == "---"), None)
        if end is not None:
            out, i = lines[: end + 1], end + 1
    prev = "start"
    while i < len(lines):
        ln = lines[i]
        fence = re.match(r"\s*(`{3,}|~{3,})", ln)
        if fence:
            mark = fence.group(1)
            indented = ln[:1] in (" ", "\t") and prev in ("list", "cont")
            k = "cont" if indented else "code"
            if out and out[-1].strip() and prev != "start" and needs_gap(prev, k):
                out.append("")
            out.append(ln)
            i += 1
            while i < len(lines):
                out.append(lines[i])
                if lines[i].strip().startswith(mark[0] * len(mark)) and lines[i].strip().strip(mark[0]) == "":
                    break
                i += 1
            i += 1
            prev = k
            continue
        if ln.strip().startswith("$$"):
            indented = ln[:1] in (" ", "\t") and prev in ("list", "cont")
            k = "cont" if indented else "code"
            if out and out[-1].strip() and prev != "start" and needs_gap(prev, k):
                out.append("")
            out.append(ln)
            closed = len(ln.strip()) > 2 and ln.strip().endswith("$$")
            i += 1
            while not closed and i < len(lines):
                out.append(lines[i])
                closed = lines[i].strip().endswith("$$")
                i += 1
            prev = k
            continue
        k = kind(ln, prev)
        if k == "blank":
            if out and out[-1].strip():
                out.append("")
        else:
            if out and out[-1].strip() and prev != "start" and needs_gap(prev, k):
                out.append("")
            out.append(ln.rstrip() if k != "paragraph" or not ln.endswith("  ") else ln)
            prev = k
        i += 1
    while out and not out[-1].strip():
        out.pop()
    return "\n".join(out) + "\n"


def is_vendored(path, root):
    """Third-party file: some folder above it holds a .vendored marker."""
    return any((d / ".vendored").exists() for d in path.parents if d == root or root in d.parents)


def notes(root=VAULT):
    for p in root.rglob("*.md"):
        if not SKIP.intersection(p.relative_to(root).parts) and not is_vendored(p, root):
            yield p


def format_vault(root=VAULT, check=False):
    changed = []
    for p in notes(Path(root)):
        text = p.read_text(encoding="utf-8")
        new = format_text(text)
        if new != text:
            changed.append(p)
            if not check:
                p.write_text(new, encoding="utf-8")
    return changed


if __name__ == "__main__":
    check = "--check" in sys.argv
    changed = format_vault(check=check)
    for p in changed:
        print(" ", p.relative_to(VAULT))
    print("need formatting:" if check else "formatted:", len(changed))
    sys.exit(1 if check and changed else 0)
