"""Test for run_checks.py: it finds every check and test by name, runs each one and fails if any fails."""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "run_checks.py"


def make(root, failing=None):
    scripts = root / "90_System" / "Scripts"
    (scripts / "validation").mkdir(parents=True)
    shutil.copy(SCRIPT, scripts / "run_checks.py")
    (scripts / "format_notes.py").write_text("import sys\nsys.exit(0)\n", encoding="utf-8")
    for name in ("check_a.py", "check_b.py", "test_check_a.py", "helper.py"):
        code = "import sys\nsys.exit(1)\n" if name == failing else "print('fine')\n"
        (scripts / "validation" / name).write_text(code, encoding="utf-8")
    return subprocess.run([sys.executable, "-I", str(scripts / "run_checks.py")], capture_output=True, text=True)


with tempfile.TemporaryDirectory() as tmp:
    run = make(Path(tmp))
    assert run.returncode == 0, run.stdout + run.stderr
    assert "passed: format_notes.py --check" in run.stdout, run.stdout
    for name in ("check_a.py", "check_b.py", "test_check_a.py"):
        assert f"passed: {name}" in run.stdout, f"{name} found and run: {run.stdout}"
    assert "helper.py" not in run.stdout, "only check_*.py and test_*.py run"
    assert "4 passed, 0 failed" in run.stdout, run.stdout
with tempfile.TemporaryDirectory() as tmp:
    run = make(Path(tmp), failing="check_b.py")
    assert run.returncode == 1 and "FAILED: check_b.py" in run.stdout and "3 passed, 1 failed" in run.stdout, run.stdout
print("ok: 8 checks")
