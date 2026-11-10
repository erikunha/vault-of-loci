"""Test for check_bases.py: a type-filtered base must exclude the templates folder."""
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "check_bases.py"


def run(root: Path) -> int:
    return subprocess.run([sys.executable, "-I", str(SCRIPT), str(root)], capture_output=True).returncode


with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    base = root / "90_System" / "Bases" / "T.base"
    base.parent.mkdir(parents=True)
    base.write_text('filters:\n  and:\n    - type == "track"\nviews:\n  - type: table\n', encoding="utf-8")
    assert run(root) == 1, "base without the exclusion must fail"
    base.write_text('filters:\n  and:\n    - type == "track"\n    - \'!file.inFolder("90_System/Templates")\'\nviews:\n  - type: table\n', encoding="utf-8")
    assert run(root) == 0, "base with the exclusion must pass"
    base.write_text('filters:\n  and:\n    - file.hasTag("x")\nviews:\n  - type: table\n', encoding="utf-8")
    assert run(root) == 0, "base without a type filter is out of scope"
    base.write_text('filters:\n  and:\n    - file.hasTag("type/track")\nviews:\n  - type: table\n    filters:\n      and:\n        - type == "track"\n', encoding="utf-8")
    assert run(root) == 1, "a view that filters by type needs the exclusion too"
    base.write_text('filters:\n  and:\n    - type == "track"\n    - file.inFolder("90_System/Templates") == false\nviews:\n  - type: table\n', encoding="utf-8")
    assert run(root) == 0, "the exclusion in another form still excludes the templates"
    base.write_text('filters:\n  and:\n    - type == "track"\n    - not:\n        - file.inFolder("90_System/Templates")\nviews:\n  - type: table\n', encoding="utf-8")
    assert run(root) == 0, "the exclusion under not: still excludes the templates"
print("ok: 6 checks")
