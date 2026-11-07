"""Test for export_anki_tsv.py."""
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "export_anki_tsv.py"
NOTE = """---
type: concept
---

# Spacing

## Flashcards

What is spacing?::Reviewing over time with `gap > 1`, see [[Spacing_Paper|the paper]].
Run `SELECT id::text FROM t` here.
Spacing beats ==massed== practice for ==long-term== retention.

```
Not a card::inside a fence
```
"""

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    (root / "10_Tracks" / "01_Bio" / "sessions").mkdir(parents=True)
    (root / "10_Tracks" / "01_Bio" / "sessions" / "S1.md").write_text(NOTE, encoding="utf-8")
    (root / "90_System" / "Templates").mkdir(parents=True)
    (root / "90_System" / "Templates" / "T.md").write_text("Template q::a\n", encoding="utf-8")
    out = root / "cards.tsv"
    run = subprocess.run([sys.executable, "-I", str(SCRIPT), "--root", str(root)], capture_output=True, text=True)
    assert run.returncode == 0, run.stderr
    assert not out.exists(), "dry run writes nothing"
    subprocess.run([sys.executable, "-I", str(SCRIPT), "--root", str(root), "--out", str(out)], check=True, capture_output=True)
    lines = out.read_text(encoding="utf-8").splitlines()
    rows = [line.split("\t") for line in lines if not line.startswith("#")]
    assert lines[0] == "#separator:tab", "Anki header first"
    assert len(rows) == 2, f"two cards, templates and fences skipped: {rows}"
    assert rows[0] == ["Basic", "Vault of Loci::01_Bio", "What is spacing?", "Reviewing over time with `gap > 1`, see the paper.", "S1"], rows[0]
    assert rows[1][0] == "Cloze" and "{{c1::massed}}" in rows[1][2] and "{{c2::long-term}}" in rows[1][2], rows[1]
print("ok: 6 checks")
