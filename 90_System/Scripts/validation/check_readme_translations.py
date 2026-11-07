"""Every translated README (README.<lang>.md) keeps up with README.md.

A translation must have the same number of `##` and `###` headings, mention every file, path and
script that README.md shows in inline code (any token with a `.` or a `/`), link to README.md, and be
linked from README.md. The wording is free. Exits 1 on any drift.

Usage: python3 -I 90_System/Scripts/validation/check_readme_translations.py [vault_root]
"""
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[3]
CODE = re.compile(r"`([^`\n]+)`")
FENCE = re.compile(r"(?ms)^```.*?^```")


def headings(text, level):
    return len(re.findall(rf"(?m)^{'#' * level} ", FENCE.sub("", text)))


def paths(text):
    return {c for c in CODE.findall(FENCE.sub("", text)) if re.fullmatch(r"[\w./<>@-]+", c) and ("." in c or "/" in c)}


def problems(root):
    found = []
    english = (root / "README.md").read_text(encoding="utf-8")
    for tr in sorted(root.glob("README.*.md")):
        text = tr.read_text(encoding="utf-8")
        for level in (2, 3):
            if headings(text, level) != headings(english, level):
                found.append(f"{tr.name}: {headings(text, level)} level-{level} headings, README.md has {headings(english, level)}")
        missing = sorted(paths(english) - paths(text))
        if missing:
            found.append(f"{tr.name}: missing {', '.join(missing)}")
        if "](README.md)" not in text:
            found.append(f"{tr.name}: no link back to README.md")
        if f"]({tr.name})" not in english:
            found.append(f"README.md: no link to {tr.name}")
    return found


if __name__ == "__main__":
    found = problems(ROOT)
    for f in found:
        print(f)
    print("README translation problems:", len(found))
    sys.exit(1 if found else 0)
