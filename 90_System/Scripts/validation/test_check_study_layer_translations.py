"""Test for check_study_layer_translations.py."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "check_study_layer_translations.py"


def run(root: Path) -> int:
    return subprocess.run([sys.executable, "-I", str(SCRIPT), str(root)], capture_output=True).returncode


with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    specs = root / "90_System" / "Specs"
    specs.mkdir(parents=True)
    (specs / "study_layer.json").write_text(json.dumps({"explanation": "a", "takeaways": "b"}), encoding="utf-8")
    assert run(root) == 0, "no translations is fine"
    (specs / "study_layer.xx.json").write_text(json.dumps({"explanation": "c", "takeaways": "d"}), encoding="utf-8")
    assert run(root) == 0, "same keys pass"
    (specs / "study_layer.yy.json").write_text(json.dumps({"explanation": "c"}), encoding="utf-8")
    assert run(root) == 1, "missing key fails"
    (specs / "study_layer.yy.json").write_text("{not json", encoding="utf-8")
    assert run(root) == 1, "invalid JSON fails"
print("ok: 4 checks")
