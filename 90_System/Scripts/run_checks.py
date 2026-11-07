"""Run every check of this vault in one command and report each one.

Runs `format_notes.py --check`, then every `validation/check_*.py`, then every `validation/test_*.py`,
in name order. A new check or test is picked up by its file name, with no list to update. Each line
says passed or FAILED; a failed one prints its last output lines. Exits 1 if any fails.

Usage: python3 -I 90_System/Scripts/run_checks.py [--quiet]
"""
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
VALIDATION = SCRIPTS / "validation"


def steps():
    yield "format_notes.py --check", [str(SCRIPTS / "format_notes.py"), "--check"]
    for prefix in ("check_", "test_"):
        for path in sorted(VALIDATION.glob(prefix + "*.py")):
            yield path.name, [str(path)]


def main():
    quiet = "--quiet" in sys.argv
    passed = failed = 0
    for name, args in steps():
        run = subprocess.run([sys.executable, "-I", *args], capture_output=True, text=True)
        if run.returncode == 0:
            passed += 1
            print(f"passed: {name}")
        else:
            failed += 1
            print(f"FAILED: {name}")
            if not quiet:
                tail = (run.stdout + run.stderr).strip().splitlines()[-8:]
                print("\n".join("    " + line for line in tail))
    print(f"{passed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
