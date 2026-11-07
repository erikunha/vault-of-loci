"""Every base that filters by note type also excludes the templates folder.

Templates carry real `type` values, so a base without the exclusion lists the
template itself as a track, session or concept. Exits 1 on any such base.

Usage: python3 -I 90_System/Scripts/validation/check_bases.py [vault_root]
"""
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[3]
EXCLUDE = '!file.inFolder("90_System/Templates")'


def problems(root: Path) -> list[str]:
    bad = []
    for base in sorted(root.rglob("*.base")):
        if ".git" in base.parts or ".obsidian" in base.parts:
            continue
        text = base.read_text(encoding="utf-8")
        head = text.split("\nviews:", 1)[0]
        if re.search(r"\btype\s*==", head) and EXCLUDE not in head:
            bad.append(str(base.relative_to(root)))
    return bad


if __name__ == "__main__":
    found = problems(ROOT)
    for f in found:
        print("lists templates:", f)
    print("base problems:", len(found))
    sys.exit(1 if found else 0)
