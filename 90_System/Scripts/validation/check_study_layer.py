"""Study layer in concept, reference and guide notes.

Rule (90_System/Specs/Study_layer.md): every concept, reference and guide note in 20_Concepts and
40_References has "## Study explanation" as its first ## section and "## Key takeaways" right
after it. A note with another `type` (for example a course or a log) is not checked.
Exits 1 on any note that lacks the layer or has it out of order.

Usage: python3 -I 90_System/Scripts/validation/check_study_layer.py [root]
"""
import re
import sys
from pathlib import Path

VAULT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[3]
EXPLAIN, TAKEAWAYS = "## Study explanation", "## Key takeaways"
CHECKED_TYPES = {"concept", "reference", "guide"}


def problem(text):
    """None when the note is fine, else a short reason."""
    front = re.match(r"---\n(.*?)\n---", text, flags=re.DOTALL)
    kind = re.search(r"(?m)^type:\s*(\S+)", front.group(1)) if front else None
    if kind and kind.group(1) not in CHECKED_TYPES:
        return None
    body = re.sub(r"(?ms)^(`{3,}|~{3,}).*?^\1\s*$", "", text[front.end():] if front else text)
    sections = re.findall(r"(?m)^## .*$", body)
    if EXPLAIN not in sections:
        return "missing"
    return None if sections[:2] == [EXPLAIN, TAKEAWAYS] else "out of order"


bad = []
for folder in ("20_Concepts", "40_References"):
    for p in sorted((VAULT / folder).rglob("*.md")):
        reason = problem(p.read_text(encoding="utf-8"))
        if reason:
            bad.append((reason, p.relative_to(VAULT)))
for reason, path in bad:
    print(f"study layer {reason}:", path)
print("study layer problems:", len(bad))
sys.exit(1 if bad else 0)
