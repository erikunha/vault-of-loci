"""Test for export_bibtex.py."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "export_bibtex.py"
PAPER = """---
type: reference
subtype: paper
year: 2006
authors: Henry L. Roediger III, Jeffrey D. Karpicke
venue: Psychological Science
doi: 10.1111/j.1467-9280.2006.01693.x
verified: true
---

# Test-enhanced learning
"""
BOOK = """---
type: reference
subtype: book
year: 2014
authors: Peter C. Brown
verified: false
---

# Make It Stick
"""

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    refs = root / "40_References"
    refs.mkdir()
    (refs / "Paper.md").write_text(PAPER, encoding="utf-8")
    (refs / "Book.md").write_text(BOOK, encoding="utf-8")
    (refs / "Guide.md").write_text("---\ntype: guide\n---\n\n# Guide\n", encoding="utf-8")
    bib, cslf = root / "r.bib", root / "r.json"
    subprocess.run([sys.executable, "-I", str(SCRIPT), "--root", str(root), "--out", str(bib), "--csl-out", str(cslf)], check=True, capture_output=True)
    text = bib.read_text(encoding="utf-8")
    assert "@article{roediger2006," in text, "suffix III is not a last name"
    assert "author = {Henry L. Roediger III and Jeffrey D. Karpicke}" in text, text
    assert "doi = {10.1111/j.1467-9280.2006.01693.x}" in text, text
    assert "@book{brown2014," in text and "note = {not verified}" in text, text
    assert "Guide" not in text, "guides are not references"
    items = json.loads(cslf.read_text(encoding="utf-8"))
    assert {i["id"] for i in items} == {"roediger2006", "brown2014"} and items[1]["DOI"].startswith("10."), items

    # The key is the first author, and the two outputs name the same people.
    (refs / "Pair.md").write_text(
        "---\ntype: reference\nsubtype: paper\nyear: 2025\nauthors: Mawson and Kang\n---\n\n# A paper\n", encoding="utf-8")
    (refs / "List.md").write_text(
        "---\ntype: reference\nsubtype: paper\nyear: 2024\nauthors: [\"Smith, J.\", \"Doe, A.\"]\n---\n\n# Another\n", encoding="utf-8")
    subprocess.run([sys.executable, "-I", str(SCRIPT), "--root", str(root), "--out", str(bib), "--csl-out", str(cslf)], check=True, capture_output=True)
    text = bib.read_text(encoding="utf-8")
    assert "@article{mawson2025," in text, "the key is the first author"
    assert "author = {Mawson and Kang}" in text, text
    items = json.loads(cslf.read_text(encoding="utf-8"))
    pair = [i for i in items if i["id"] == "mawson2025"][0]
    assert [a["literal"] for a in pair["author"]] == ["Mawson", "Kang"], pair
    listed = [i for i in items if i["id"].startswith("smith")][0]
    assert [a["literal"] for a in listed["author"]] == ["Smith, J.", "Doe, A."], listed
    assert "author = {Smith, J. and Doe, A.}" in text, text
print("ok: 10 checks")
