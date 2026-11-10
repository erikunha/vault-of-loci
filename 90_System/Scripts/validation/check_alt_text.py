"""Every image embedded in a note has alternative text.

Accepts ![[image.png|alt text]] (or with \\| inside a table) and ![alt text](image.png). A Markdown
image with a title, ![alt text](image.png "Figure 1"), and one with the target in angle brackets,
![alt text](<image.png>), are read too. Inline and fenced code are skipped. Notes embedded with
![[Note]] (no image extension) are not images and are ignored. Exits 1 on any image
without alt text.

Usage: python3 -I 90_System/Scripts/validation/check_alt_text.py [vault_root]
"""
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[3]
IMAGE = r"\.(png|jpe?g|gif|svg|webp|avif|bmp)"
WIKI = re.compile(r"!\[\[([^\]|\\]+?" + IMAGE + r")(\\?\|[^\]]*)?\]\]", re.I)
MD = re.compile(r"!\[([^\]]*)\]\(\s*<?([^)\s>]+?" + IMAGE + r")>?(?:\s+\"[^\"]*\")?\s*\)", re.I)
SKIP = {".git", ".obsidian", ".agents", ".claude", "node_modules"}


def problems(root: Path) -> list[str]:
    found = []
    for note in sorted(root.rglob("*.md")):
        if SKIP.intersection(note.relative_to(root).parts):
            continue
        text = note.read_text(encoding="utf-8")
        text = re.sub(r"(?ms)^\s*(`{3,}|~{3,}).*?^\s*\1\s*$", "", text)
        text = re.sub(r"`[^`\n]*`", "", text)
        for m in WIKI.finditer(text):
            alt = (m.group(3) or "").lstrip("\\|").strip()
            if not alt or alt.isdigit():
                found.append(f"{note.relative_to(root)}: {m.group(1)}")
        for m in MD.finditer(text):
            if not m.group(1).strip():
                found.append(f"{note.relative_to(root)}: {m.group(2)}")
    return found


if __name__ == "__main__":
    found = problems(ROOT)
    for item in found:
        print("no alt text:", item)
    print("images without alt text:", len(found))
    sys.exit(1 if found else 0)
