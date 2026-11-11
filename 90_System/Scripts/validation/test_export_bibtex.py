"""Test for export_bibtex.py.

The fixtures are the shapes the vault writes in the `authors` property: a list of surnames
side by side, a full name with the surname last, the form "Surname, Given name" and a list
in JSON. Run: python3 -I 90_System/Scripts/validation/test_export_bibtex.py
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "export_bibtex.py"
checks = 0


def check(cond, message):
    global checks
    assert cond, message
    checks += 1


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
NOTES = {
    "Paper.md": PAPER,
    "Book.md": BOOK,
    "Guide.md": "---\ntype: guide\n---\n\n# Guide\n",
    # Two surnames joined by " and ".
    "Pair.md": "---\ntype: reference\nsubtype: paper\nyear: 2025\nauthors: Mawson and Kang\n---\n\n# A paper\n",
    # A list in JSON gives the authors one by one.
    "List.md": "---\ntype: reference\nsubtype: paper\nyear: 2024\nauthors: [\"Smith, J.\", \"Doe, A.\"]\n---\n\n# Another\n",
    # The vault lists surnames side by side, so this paper has three authors.
    "Three.md": "---\ntype: reference\nsubtype: paper\nyear: 2025\nauthors: Goncalves, Muniz and Jaeger\n---\n\n# Three authors\n",
    # Two surnames side by side, and not one name with the surname first.
    "Two.md": "---\ntype: reference\nsubtype: paper\nyear: 2026\nauthors: Akgun, Toker\n---\n\n# Two authors\n",
    # The form "Surname, Given name", in the second position of the pair too.
    "Reversed.md": "---\ntype: reference\nsubtype: paper\nyear: 2001\nauthors: Roediger, Henry L. and Karpicke, Jeffrey D.\n---\n\n# Reversed\n",
    # The same form, with two pairs in one group and no " and ".
    "Pairs.md": "---\ntype: reference\nsubtype: paper\nyear: 2002\nauthors: Roediger, Henry L., Karpicke, Jeffrey D.\n---\n\n# Two pairs\n",
    # The form "Surname, Given name" with a given name of one initial.
    "Initial.md": "---\ntype: reference\nsubtype: paper\nyear: 2003\nauthors: Smith, J.\n---\n\n# An initial\n",
    # The same form, with a suffix after the given name.
    "Suffix.md": "---\ntype: reference\nsubtype: paper\nyear: 2004\nauthors: Smith, John III.\n---\n\n# A suffix\n",
    # A list of surnames with the last one joined by " and ".
    "Four.md": "---\ntype: reference\nsubtype: paper\nyear: 2023\nauthors: Zheng, Chiang, Sheng and Stoica\n---\n\n# Four\n",
}

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    refs = root / "40_References"
    refs.mkdir()
    for name, note in NOTES.items():
        (refs / name).write_text(note, encoding="utf-8")
    bib, cslf = root / "r.bib", root / "r.json"
    subprocess.run([sys.executable, "-I", str(SCRIPT), "--root", str(root), "--out", str(bib), "--csl-out", str(cslf)], check=True, capture_output=True)
    text = bib.read_text(encoding="utf-8")
    items = json.loads(cslf.read_text(encoding="utf-8"))
    by_id = {i["id"]: i for i in items}

    check("@article{roediger2006," in text, "suffix III is not a last name")
    check("author = {Roediger, Henry L. III and Karpicke, Jeffrey D.}" in text, "the surname comes first: " + text)
    check("doi = {10.1111/j.1467-9280.2006.01693.x}" in text, text)
    check("@book{brown2014," in text and "note = {not verified}" in text, text)
    check("author = {Brown, Peter C.}" in text, "the name of a single author keeps the given name")
    check(not any(i["title"] == "Guide" for i in items), "guides are not references")
    check({i["id"] for i in items} == {
        "roediger2006", "brown2014", "mawson2025", "smith2024", "goncalves2025", "akgun2026",
        "roediger2001", "roediger2002", "smith2003", "smith2004", "zheng2023",
    }, sorted(by_id))
    check(by_id["roediger2006"]["DOI"].startswith("10."), by_id["roediger2006"])

    # Zotero reads a `literal` name as an institution and does not parse it, so a person
    # needs a family name in the CSL JSON.
    check(not any("literal" in name for item in items for name in item["author"]), "no author goes out as a literal")
    for item in items:
        check(bool(item["author"]), item)
        check(all("family" in name for name in item["author"]), item)

    # The key is the first author, and the two outputs name the same people.
    check("@article{mawson2025," in text, "the key is the first author")
    check("author = {Mawson and Kang}" in text, text)
    check(by_id["mawson2025"]["author"] == [{"family": "Mawson"}, {"family": "Kang"}], by_id["mawson2025"])

    # A full name gives the family name and the given name, and the suffix apart.
    check(by_id["roediger2006"]["author"] == [
        {"family": "Roediger", "given": "Henry L. III"},
        {"family": "Karpicke", "given": "Jeffrey D."},
    ], by_id["roediger2006"])
    check(by_id["brown2014"]["author"] == [{"family": "Brown", "given": "Peter C."}], by_id["brown2014"])

    # A reference that was not verified says so in the CSL JSON too.
    check(by_id["brown2014"]["note"] == "not verified", by_id["brown2014"])
    check("note" not in by_id["roediger2006"], by_id["roediger2006"])

    # A list gives the authors one by one, so a comma inside an item is a surname and a given name.
    check(by_id["smith2024"]["author"] == [
        {"family": "Smith", "given": "J."},
        {"family": "Doe", "given": "A."},
    ], by_id["smith2024"])
    check("author = {Smith, J. and Doe, A.}" in text, text)

    # Surnames side by side are authors side by side, and not one name with the surname first.
    check("author = {Goncalves and Muniz and Jaeger}" in text, text)
    check(by_id["goncalves2025"]["author"] == [
        {"family": "Goncalves"}, {"family": "Muniz"}, {"family": "Jaeger"},
    ], by_id["goncalves2025"])
    check("author = {Akgun and Toker}" in text, text)
    check(by_id["akgun2026"]["author"] == [{"family": "Akgun"}, {"family": "Toker"}], by_id["akgun2026"])

    # The form "Surname, Given name" is one author, in any position of the pair.
    check("author = {Roediger, Henry L. and Karpicke, Jeffrey D.}" in text, text)
    check(by_id["roediger2001"]["author"] == [
        {"family": "Roediger", "given": "Henry L."},
        {"family": "Karpicke", "given": "Jeffrey D."},
    ], by_id["roediger2001"])

    # The same form, with two pairs in one group and no " and ".
    check("author = {Roediger, Henry L. and Karpicke, Jeffrey D.}" in text, text)
    check(by_id["roediger2002"]["author"] == [
        {"family": "Roediger", "given": "Henry L."},
        {"family": "Karpicke", "given": "Jeffrey D."},
    ], by_id["roediger2002"])

    # A given name of one initial is a given name, and the suffix goes apart from it.
    check("author = {Smith, J.}" in text, text)
    check(by_id["smith2003"]["author"] == [{"family": "Smith", "given": "J."}], by_id["smith2003"])
    check(by_id["smith2004"]["author"] == [{"family": "Smith", "given": "John III."}], by_id["smith2004"])

    # A list of surnames keeps every surname, and the last one joined by " and ".
    check("author = {Zheng and Chiang and Sheng and Stoica}" in text, text)
    check(by_id["zheng2023"]["author"] == [
        {"family": "Zheng"}, {"family": "Chiang"}, {"family": "Sheng"}, {"family": "Stoica"},
    ], by_id["zheng2023"])

    # The BibTeX and the CSL JSON never name a different set of people.
    for item in items:
        block = next(b for b in text.split("\n\n") if f"{{{item['id']}," in b)
        line = next(l for l in block.splitlines() if l.strip().startswith("author = "))
        names = [n.strip() for n in line.split("=", 1)[1].strip().strip("{}").split(" and ")]
        check(len(names) == len(item["author"]), (item["id"], line, item["author"]))
        for name, author in zip(names, item["author"]):
            check(author["family"] in name, (item["id"], name, author))
            if author.get("given"):
                check(author["given"] in name, (item["id"], name, author))
print("ok:", checks, "checks")
