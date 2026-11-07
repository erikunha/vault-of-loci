"""Normalize-names test on a throwaway git repo: renames, rewrites links, keeps labels, is idempotent.
Run: python3 -I 90_System/Scripts/validation/test_normalize_names.py"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "normalize_names.py"
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    (root / "90_System" / "Scripts").mkdir(parents=True)
    shutil.copy(SCRIPT, root / "90_System" / "Scripts" / "normalize_names.py")
    (root / "My Note.md").write_text("# My Note\n")
    (root / "index.md").write_text("See [[My Note]] and [[My Note|label]] and [x](My%20Note.md).\n")
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "add", "-A"], cwd=root, check=True)
    run = [sys.executable, "-I", str(root / "90_System" / "Scripts" / "normalize_names.py"), "--write"]
    subprocess.run(run, cwd=root, check=True, capture_output=True)
    assert (root / "My_Note.md").exists() and not (root / "My Note.md").exists()
    index = (root / "index.md").read_text()
    assert "[[My_Note|My Note]]" in index, index
    assert "[[My_Note|label]]" in index, index
    assert "(My_Note.md)" in index, index
    again = subprocess.run(run, cwd=root, check=True, capture_output=True, text=True).stdout
    assert "to rename: 0" in again and "files with rewritten links: 0" in again, again
print("ok: rename, links, labels, idempotent")
