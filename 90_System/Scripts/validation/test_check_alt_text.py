"""Test for check_alt_text.py."""
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "check_alt_text.py"


def run(root: Path, text: str) -> int:
    (root / "n.md").write_text(text, encoding="utf-8")
    return subprocess.run([sys.executable, "-I", str(SCRIPT), str(root)], capture_output=True).returncode


with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    assert run(root, "![[map.png]]\n") == 1, "wiki image without alt fails"
    assert run(root, "![[map.png|300]]\n") == 1, "a width is not alt text"
    assert run(root, "![[map.png|Map of the track]]\n") == 0, "wiki image with alt passes"
    assert run(root, "![](a.jpg)\n") == 1, "markdown image without alt fails"
    assert run(root, "![A chart](a.jpg)\n") == 0, "markdown image with alt passes"
    assert run(root, "| ![[a.png\\|]] |\n") == 1, "escaped pipe in a table, empty alt fails"
    assert run(root, "| ![[a.png\\|A map]] |\n") == 0, "escaped pipe in a table with alt passes"
    assert run(root, "Example: `![[a.png|400]]`\n\n```\n![[b.png]]\n```\n") == 0, "inline and fenced code are not images"
    assert run(root, "![[Other_Note]]\n") == 0, "note embeds are not images"
print("ok: 9 checks")
