"""Study layer position in concept, reference and guide notes.

Rule (90_System/Specs/Study_layer.md): when a note has "## Study explanation", it is the
first ## section and "## Key takeaways" comes right after. Exits 1 on any note out of order.
"""
import re
import sys
from pathlib import Path

VAULT = Path(__file__).resolve().parents[3]
EXPLAIN, TAKEAWAYS = "## Study explanation", "## Key takeaways"


def out_of_order(text):
    sections = re.findall(r"(?m)^## .*$", text)
    return EXPLAIN in sections and sections[:2] != [EXPLAIN, TAKEAWAYS]


bad = [p.relative_to(VAULT) for folder in ("20_Concepts", "40_References")
       for p in sorted((VAULT / folder).rglob("*.md")) if out_of_order(p.read_text(encoding="utf-8"))]
for b in bad:
    print("out of order:", b)
print("study layer out of order:", len(bad))
sys.exit(1 if bad else 0)
