"""Test for pdf_to_text.py: it extracts text once per file content and refuses a file it already processed."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "pdf_to_text.py"

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    pdf = root / "paper.pdf"
    pdf.write_text("Testing beats rereading after one week.\n", encoding="utf-8")
    manifest = root / "manifest.json"
    out = root / "paper.txt"
    base = [sys.executable, "-I", str(SCRIPT), str(pdf), "--manifest", str(manifest), "--text-cmd", "cat"]
    first = subprocess.run(base + ["--out", str(out), "--note", "40_References/Papers/Paper.md"], capture_output=True, text=True)
    assert first.returncode == 0, first.stderr
    assert "Testing beats rereading" in out.read_text(encoding="utf-8"), "text is extracted"
    entries = json.loads(manifest.read_text(encoding="utf-8"))
    assert len(entries) == 1 and list(entries.values())[0]["note"] == "40_References/Papers/Paper.md", entries
    copy = root / "renamed.pdf"
    copy.write_bytes(pdf.read_bytes())
    again = subprocess.run([sys.executable, "-I", str(SCRIPT), str(copy), "--manifest", str(manifest), "--text-cmd", "cat"], capture_output=True, text=True)
    assert again.returncode == 3 and "already processed" in again.stdout and "Paper.md" in again.stdout, "same content under another name is caught: " + again.stdout
    missing = subprocess.run([sys.executable, "-I", str(SCRIPT), str(pdf), "--manifest", str(root / "m2.json"), "--text-cmd", "no-such-tool-xyz"], capture_output=True, text=True)
    assert missing.returncode == 2 and "install" in missing.stderr, "a missing extractor says how to get it: " + missing.stderr
print("ok: 6 checks")
