"""Formatter tests. Run: python3 -I 90_System/Scripts/validation/test_format_notes.py"""
import importlib.util
import tempfile
from pathlib import Path

spec = importlib.util.spec_from_file_location("fmt", Path(__file__).resolve().parents[1] / "format_notes.py")
fmt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fmt)

cases = {
    "paragraph after callout leaves the callout": ("> [!tldr] Summary\n> line\nLoose text", "> [!tldr] Summary\n> line\n\nLoose text\n"),
    "heading gets blank lines around it": ("text\n## Title\n- item", "text\n\n## Title\n\n- item\n"),
    "hr after paragraph is not a setext heading": ("text\n---\nmore", "text\n\n---\n\nmore\n"),
    "list items stay together": ("- a\n- b\n- c", "- a\n- b\n- c\n"),
    "frontmatter untouched": ("---\na: 1\n---\n# T\ntext", "---\na: 1\n---\n# T\n\ntext\n"),
    "code fence content untouched": ("text\n```\n# not a heading\n\n\nx\n```\nafter", "text\n\n```\n# not a heading\n\n\nx\n```\n\nafter\n"),
}
for name, (given, expected) in cases.items():
    got = fmt.format_text(given)
    assert got == expected, f"{name}: {got!r}"
    assert fmt.format_text(got) == got, f"{name}: not idempotent"

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    (root / "skill" / "refs").mkdir(parents=True)
    (root / "skill" / ".vendored").write_text("source: test\n")
    messy = "text\n## Title\n- item"
    (root / "skill" / "refs" / "a.md").write_text(messy)
    (root / "note.md").write_text(messy)
    fmt.format_vault(root=root)
    assert (root / "skill" / "refs" / "a.md").read_text() == messy, "rewrote a vendored file"
    assert (root / "note.md").read_text() != messy, "skipped an own note"
print("ok:", len(cases) + 2, "checks")
