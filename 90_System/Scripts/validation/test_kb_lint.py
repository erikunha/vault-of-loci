"""Test for kb_lint.py: it reports orphans, unused references, concepts outside any track and stale inbox items."""
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "kb_lint.py"


def write(root, rel, text):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    write(root, "00_Home.md", "---\ntype: home\n---\n[[Linked]]\n")
    write(root, "20_Concepts/Linked.md", "---\ntype: concept\ntracks: [\"[[T]]\"]\n---\n[[Used_Paper]]\n")
    write(root, "20_Concepts/Lonely.md", "---\ntype: concept\ntracks: []\n---\ntext\n")
    write(root, "40_References/Papers/Used_Paper.md", "---\ntype: reference\nverified: true\n---\n")
    write(root, "40_References/Papers/Unused_Paper.md", "---\ntype: reference\nverified: false\n---\n")
    write(root, "00_Inbox/Old_Question.md", "---\ntype: question\nstatus: open\ndate: 2020-01-01\n---\n")
    write(root, "00_Inbox/Clippings/Old_Clip.md", "---\ntype: clipping\nprocessed: false\nclipped: 2020-01-01\n---\n")
    write(root, "INDEX.md", "[[Lonely]] [[Unused_Paper]] [[Old_Question]] [[Old_Clip]]\n")
    run = subprocess.run([sys.executable, "-I", str(SCRIPT), "--root", str(root)], capture_output=True, text=True)
    out = run.stdout
    assert run.returncode == 0, "a report, not a gate: " + run.stderr
    assert "orphan: 20_Concepts/Lonely.md" in out, "INDEX.md links do not count, so Lonely is an orphan: " + out
    assert "no track: 20_Concepts/Lonely.md" in out and "no track: 20_Concepts/Linked.md" not in out, out
    assert "unused reference: 40_References/Papers/Unused_Paper.md" in out, out
    assert "unverified reference: 40_References/Papers/Unused_Paper.md" in out, out
    assert "open question" in out and "Old_Question" in out, out
    assert "unprocessed clipping" in out and "Old_Clip" in out, out
    assert "Used_Paper.md" not in out, "a linked, verified reference is fine: " + out
    strict = subprocess.run([sys.executable, "-I", str(SCRIPT), "--root", str(root), "--strict"], capture_output=True, text=True)
    assert strict.returncode == 1, "--strict fails when something is reported"
print("ok: 9 checks")
