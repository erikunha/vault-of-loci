"""INDEX.md and 90_System/index.json match the notes in the vault.

Runs `build_index.py --check`: exit 1 when a note was created, removed or edited after the last build.
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
