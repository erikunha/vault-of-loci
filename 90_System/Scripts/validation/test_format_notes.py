"""Formatter tests. Run: python3 -I 90_System/Scripts/validation/test_format_notes.py"""
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

FORMATTER = Path(__file__).resolve().parents[1] / "format_notes.py"
HOOK = Path(__file__).resolve().parents[3] / ".claude" / "hooks" / "format_note.py"
spec = importlib.util.spec_from_file_location("fmt", FORMATTER)
fmt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fmt)

cases = {
    "paragraph after callout leaves the callout": ("> [!tldr] Summary\n> line\nLoose text", "> [!tldr] Summary\n> line\n\nLoose text\n"),
    "heading gets blank lines around it": ("text\n## Title\n- item", "text\n\n## Title\n\n- item\n"),
    "hr after paragraph is not a setext heading": ("text\n---\nmore", "text\n\n---\n\nmore\n"),
    "list items stay together": ("- a\n- b\n- c", "- a\n- b\n- c\n"),
    "frontmatter untouched": ("---\na: 1\n---\n# T\ntext", "---\na: 1\n---\n\n# T\n\ntext\n"),
    "frontmatter that never closes is left alone": ("---\na: 1\n# T\ntext", "---\na: 1\n# T\ntext"),
    "a hard break in a list item is kept": ("- one  \n  two\n", "- one  \n  two\n"),
    "code fence content untouched": ("text\n```\n# not a heading\n\n\nx\n```\nafter", "text\n\n```\n# not a heading\n\n\nx\n```\n\nafter\n"),
    "math block content untouched": ("text\n$$\n# not a heading\n\n\nx\n$$\nafter", "text\n\n$$\n# not a heading\n\n\nx\n$$\n\nafter\n"),
    "one-line math block stays one block": ("text\n$$x^2$$\nafter", "text\n\n$$x^2$$\n\nafter\n"),
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

# the Claude hook formats only notes inside its own vault, and not vendored ones
with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as outside:
    root = Path(tmp)
    hooks = root / ".claude" / "hooks"
    hooks.mkdir(parents=True)
    (root / "90_System" / "Scripts").mkdir(parents=True)
    shutil.copy(HOOK, hooks / "format_note.py")
    shutil.copy(FORMATTER, root / "90_System" / "Scripts" / "format_notes.py")
    (root / "vendor").mkdir()
    (root / "vendor" / ".vendored").write_text("source: test\n")
    (root / ".agents" / "skills" / "own").mkdir(parents=True)
    messy = "text\n## Title\n- item"
    paths = {
        "inside": root / "note.md",
        "vendored": root / "vendor" / "a.md",
        "agents": root / ".agents" / "skills" / "own" / "SKILL.md",
        "outside": Path(outside) / "other.md",
    }
    for path in paths.values():
        path.write_text(messy)
        subprocess.run([sys.executable, "-I", str(hooks / "format_note.py")], check=True,
                       input=json.dumps({"tool_input": {"file_path": str(path)}}), text=True)
    assert paths["inside"].read_text() != messy, "hook skipped a note in the vault"
    assert paths["agents"].read_text() != messy, "hook skipped an own note under .agents"
    assert paths["vendored"].read_text() == messy, "hook rewrote a vendored file"
    assert paths["outside"].read_text() == messy, "hook rewrote a file outside the vault"
print("ok:", len(cases) + 6, "checks")
