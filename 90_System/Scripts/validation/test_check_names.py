"""Naming check tests on throwaway vaults: spaces in file and folder names, and the vault it reads.
Run: python3 -I 90_System/Scripts/validation/test_check_names.py"""
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "check_names.py"
checks = 0


def run(files):
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for name in files:
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("x\n", encoding="utf-8")
        r = subprocess.run([sys.executable, "-I", str(SCRIPT), str(root)], capture_output=True, text=True)
        return r.returncode, r.stdout


def check(cond, message):
    global checks
    assert cond, message
    checks += 1


code, out = run(["Good_Name.md"])
check(code == 0, f"a name without spaces passes: {out}")

code, out = run(["Bad Name.md"])
check(code == 1 and "Bad Name.md" in out, f"a file with a space fails: {out}")

code, out = run(["My Folder/Note.md"])
check(code == 1 and "My Folder" in out, f"a folder with a space fails: {out}")

code, out = run([".git/Some File.md"])
check(code == 0, f"the folders the check skips are skipped: {out}")

print("ok:", checks, "checks")
