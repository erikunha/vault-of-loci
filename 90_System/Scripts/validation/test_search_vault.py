"""Test for search_vault.py: ranks sections by relevance and returns where they are, not their text."""
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "search_vault.py"

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    (root / "20_Concepts").mkdir()
    (root / "20_Concepts" / "Spacing.md").write_text("---\ntype: concept\n---\n\n# Spacing\n\n## Study explanation\n\nSpacing spreads review sessions over days. Spacing beats massing.\n\n## Key takeaways\n\nShort.\n", encoding="utf-8")
    (root / "20_Concepts" / "Interleaving.md").write_text("# Interleaving\n\nMix problem types in one session. Review once.\n", encoding="utf-8")
    (root / "90_System" / "Templates").mkdir(parents=True)
    (root / "90_System" / "Templates" / "Concept.md").write_text("spacing review spacing review\n", encoding="utf-8")
    (root / ".obsidian").mkdir()
    (root / ".obsidian" / "x.md").write_text("spacing spacing spacing\n", encoding="utf-8")
    run = subprocess.run([sys.executable, "-I", str(SCRIPT), "spacing review", "--root", str(root), "--top", "2"], capture_output=True, text=True)
    assert run.returncode == 0, run.stderr
    lines = run.stdout.strip().splitlines()
    assert lines[0].startswith("20_Concepts/Spacing.md:7 "), f"best section first, with its line: {lines}"
    assert "Study explanation" in lines[0], "the heading of the section is shown"
    assert "beats massing" not in run.stdout, "it points to the place, it does not print the text"
    assert ".obsidian" not in run.stdout and "Templates" not in run.stdout, "tool folders and templates are skipped"
    assert len(lines) <= 2, "--top limits the results"
    none = subprocess.run([sys.executable, "-I", str(SCRIPT), "photosynthesis", "--root", str(root)], capture_output=True, text=True)
    assert none.returncode == 0 and "no match" in none.stdout, none.stdout
    # A note whose name holds the word is not a note that talks about it.
    (root / "20_Concepts" / "photosynthesis_notes.md").write_text("# Other\n\nNothing about review here.\n", encoding="utf-8")
    name_only = subprocess.run([sys.executable, "-I", str(SCRIPT), "photosynthesis", "--root", str(root)], capture_output=True, text=True)
    assert name_only.returncode == 0 and "no match" in name_only.stdout, name_only.stdout
    # A note with frontmatter and no heading points at the first line of the body.
    (root / "20_Concepts" / "Plain.md").write_text("---\ntype: concept\n---\n\nSpacing spreads review sessions.\n", encoding="utf-8")
    plain = subprocess.run([sys.executable, "-I", str(SCRIPT), "spacing", "--root", str(root)], capture_output=True, text=True)
    assert "20_Concepts/Plain.md:4 " in plain.stdout, plain.stdout
print("ok: 8 checks")
