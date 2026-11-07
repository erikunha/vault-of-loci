"""Test for check_readme_translations.py."""
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "check_readme_translations.py"
EN = "# T\n\n**English** · [Português](README.pt-BR.md)\n\n## A\n\nRun `run_checks.py` and read `90_System/Specs/Tools.md`.\n\n## B\n\n### C\n"
PT = "# T\n\n[English](README.md) · **Português**\n\n## A\n\nRode `run_checks.py` e leia `90_System/Specs/Tools.md`.\n\n## B\n\n### C\n"


def run(en, pt):
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "README.md").write_text(en, encoding="utf-8")
        if pt is not None:
            (root / "README.pt-BR.md").write_text(pt, encoding="utf-8")
        return subprocess.run([sys.executable, "-I", str(SCRIPT), str(root)], capture_output=True, text=True)


assert run(EN, PT).returncode == 0, "matching translation passes"
assert run(EN, None).returncode == 0, "no translation, nothing to check"
r = run(EN.replace("## B", "## B\n\n## New"), PT)
assert r.returncode == 1 and "headings" in r.stdout, r.stdout
r = run(EN.replace("`run_checks.py`", "`run_checks.py` and `new_tool.py`"), PT)
assert r.returncode == 1 and "new_tool.py" in r.stdout, r.stdout
r = run(EN, PT.replace("[English](README.md) · ", ""))
assert r.returncode == 1 and "link" in r.stdout, r.stdout
r = run(EN.replace(" · [Português](README.pt-BR.md)", ""), PT)
assert r.returncode == 1 and "link" in r.stdout, r.stdout
print("ok: 6 checks")
