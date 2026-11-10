"""INDEX.md and 90_System/index.json match the notes in the vault.

Runs `build_index.py --check`: exit 1 when the index does not hold what the notes say, which is
when a note was created, removed, or changed in a way the index shows, such as its type, its
summary or its length. An edit that leaves the index the same is not a stale index.
To fix: python3 -I 90_System/Scripts/build_index.py
Usage: python3 -I 90_System/Scripts/validation/check_index.py [root]"""
import subprocess
import sys
from pathlib import Path

BUILD = Path(__file__).resolve().parents[1] / "build_index.py"
cmd = [sys.executable, "-I", str(BUILD), "--check"]
if len(sys.argv) > 1:
    cmd += ["--root", sys.argv[1]]
sys.exit(subprocess.run(cmd).returncode)
