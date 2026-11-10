"""Every base that filters by note type also excludes the templates folder.

Templates carry real `type` values, so a base without the exclusion lists the
template itself as a track, session or concept. A view that filters by type counts as
much as a filter that applies to the whole base. Exits 1 on any such base.

Usage: python3 -I 90_System/Scripts/validation/check_bases.py [vault_root]
"""
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[3]
TEMPLATES = "90_System/Templates"


def filters_by_type(text):
    """True when the text filters the notes by their type."""
    return bool(re.search(r"\btype\s*==", text))


def excludes_templates(text):
    """True when the text leaves the templates folder out.

    The rule is the exclusion, not the exact spelling of it. `!file.inFolder(...)`,
    `file.inFolder(...) == false`, `file.inFolder(...) != true` and `not:` over the same
    call all keep the templates out of the base.
    """
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if "file.inFolder" not in line or TEMPLATES not in line:
            continue
        if re.search(r"!\s*file\.inFolder", line):
            return True
        if re.search(r"file\.inFolder[^)]*\)\s*==\s*false", line):
            return True
        if re.search(r"file\.inFolder[^)]*\)\s*!=\s*true", line):
            return True
        # `not:` over the call, on the same line or on the line above it.
        if re.search(r"not:\s*file\.inFolder", line):
            return True
        previous = lines[index - 1] if index else ""
        if re.search(r"not:\s*$", previous):
            return True
    return False


def problems(root: Path) -> list[str]:
    bad = []
    for base in sorted(root.rglob("*.base")):
        if ".git" in base.parts or ".obsidian" in base.parts:
            continue
        text = base.read_text(encoding="utf-8")
        if filters_by_type(text) and not excludes_templates(text):
            bad.append(str(base.relative_to(root)))
    return bad


if __name__ == "__main__":
    found = problems(ROOT)
    for f in found:
        print("lists templates:", f)
    print("base problems:", len(found))
    sys.exit(1 if found else 0)
