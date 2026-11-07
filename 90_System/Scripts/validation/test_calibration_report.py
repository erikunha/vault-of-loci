"""Test for calibration_report.py: it compares confidence with score and lists stale and untested concepts."""
import subprocess
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "calibration_report.py"
recent = (date.today() - timedelta(days=3)).isoformat()


def concept(root, name, **props):
    front = "".join(f"{k}: {v}\n" for k, v in props.items())
    (root / "20_Concepts" / f"{name}.md").write_text(f"---\ntype: concept\n{front}---\n", encoding="utf-8")


with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    (root / "20_Concepts").mkdir()
    concept(root, "Sure_Wrong", confidence=5, score=40, last_tested=recent)
    concept(root, "Unsure_Right", confidence=1, score=90, last_tested=recent)
    concept(root, "Calibrated", confidence=4, score=80, last_tested=recent)
    concept(root, "Old", confidence=3, score=60, last_tested="2020-01-01")
    concept(root, "Never")
    run = subprocess.run([sys.executable, "-I", str(SCRIPT), "--root", str(root)], capture_output=True, text=True)
    out = run.stdout
    assert run.returncode == 0, run.stderr
    assert "overconfident: Sure_Wrong" in out, out
    assert "underconfident: Unsure_Right" in out, out
    assert "Calibrated" not in out.split("stale")[0], "a calibrated concept is not flagged: " + out
    assert "stale: Old" in out, out
    assert "untested: Never" in out, out
    assert "mean gap" in out, "an overall calibration line is printed: " + out
print("ok: 7 checks")
