"""Shared reader for the report scripts: every note with its path, frontmatter and outgoing wikilinks.

Standard library only. Skips tool folders, templates and generated files. Frontmatter is read as simple
`key: value` lines; a value in brackets becomes a list.
"""
import re
from pathlib import Path

SKIP = {".obsidian", ".git", ".github", ".githooks", ".trash", ".venv", ".smart-env", ".claude", ".agents", "node_modules"}
LINK = re.compile(r"\[\[([^\]|#^]+)")


def parse_front(text):
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end < 0:
        return {}, text
    front = {}
    for line in text[4:end].splitlines():
        m = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if not m:
            continue
        value = m.group(2).strip()
        if value.startswith("[") and value.endswith("]"):
            value = [v.strip().strip('"') for v in value[1:-1].split(",") if v.strip()]
        else:
            value = value.strip('"')
        front[m.group(1)] = value
    return front, text[end + 4:]


def notes(root):
    for path in sorted(Path(root).rglob("*.md")):
        rel = path.relative_to(root)
        if SKIP.intersection(rel.parts) or rel.parts[:2] in (("90_System", "Templates"), ("90_System", "Agent_Log")):
            continue
        if rel.name in ("INDEX.md", "README.md"):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        front, body = parse_front(text)
        links = {m.group(1).strip().split("/")[-1] for m in LINK.finditer(text)}
        yield rel, front, links
