"""Test for judge_agreement.py: how far apart two judges are on the same run."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "judge_agreement.py"


def scores_file(path, scores, family, total=None, verdict=None):
    payload = {
        "judge_command": f"{family}-judge",
        "judge_family": family,
        "scores": {key: {"score": value, "why": ""} for key, value in scores.items()},
        "verdict": {"verdict": verdict, "total": total},
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    a = scores_file(root / "scores.json", {"1": 0, "2": 1, "3": 2, "4": 1}, "alpha", 4, "fail")
    b = scores_file(root / "scores-judge-beta.json", {"1": 0, "2": 1, "3": 2, "4": 2}, "beta", 5, "fail")
    c = scores_file(root / "scores-judge-gamma.json", {"1": 2, "2": 2, "3": 0}, "gamma")
    # A judge that scored scenario 4 and not scenario 3, the other way round from gamma.
    e = scores_file(root / "scores-judge-epsilon.json", {"1": 0, "2": 1, "4": 2}, "epsilon")

    out = subprocess.run([sys.executable, "-I", str(SCRIPT), str(a), str(b), "--json"],
                         capture_output=True, text=True)
    assert out.returncode == 0, out.stderr
    result = json.loads(out.stdout)
    assert result["scenarios_compared"] == 4, result
    assert result["only_in_a"] == [] and result["only_in_b"] == [], result
    assert result["percent_agreement"] == 0.75, result
    # Three of four agree; chance agreement is 0.3125, so kappa is (0.75 - 0.3125) / 0.6875.
    assert abs(result["cohen_kappa"] - 0.6364) < 0.001, result
    # The only disagreement is a 1 against a 2. The quadratic weights count that disagreement as
    # a quarter of the distance of a 0 against a 2, so the weighted kappa sits above the plain one.
    assert abs(result["weighted_kappa"] - 0.8) < 0.001, result
    assert result["verdict_a"] == "fail" and result["verdict_b"] == "fail", result

    # A judge that scored every scenario the other way round.
    d = scores_file(root / "scores-judge-delta.json", {"1": 2, "2": 2, "3": 0, "4": 0}, "delta")
    out = subprocess.run([sys.executable, "-I", str(SCRIPT), str(a), str(d), "--json"],
                         capture_output=True, text=True)
    assert out.returncode == 0, out.stderr
    flipped = json.loads(out.stdout)
    assert flipped["percent_agreement"] == 0.0, flipped
    assert flipped["cohen_kappa"] is not None and flipped["cohen_kappa"] < 0, flipped
    # A kappa cannot leave the -1 to 1 range, whichever way the two judges disagree.
    assert -1 <= flipped["weighted_kappa"] <= 1, flipped

    # Scenarios only one judge scored are named, not silently dropped.
    out = subprocess.run([sys.executable, "-I", str(SCRIPT), str(c), str(e), "--json"],
                         capture_output=True, text=True)
    assert out.returncode == 0, out.stderr
    partial = json.loads(out.stdout)
    assert partial["scenarios_compared"] == 2, partial
    assert partial["only_in_a"] == ["3"], partial
    assert partial["only_in_b"] == ["4"], partial

    # The plain output says what the kappa means.
    text = subprocess.run([sys.executable, "-I", str(SCRIPT), str(a), str(b)],
                          capture_output=True, text=True)
    assert text.returncode == 0, text.stderr
    assert "percent agreement: 0.75" in text.stdout, text.stdout
    assert "kappa" in text.stdout, text.stdout

    # A missing file is refused instead of crashing.
    missing = subprocess.run([sys.executable, "-I", str(SCRIPT), str(a), str(root / "nope.json")],
                             capture_output=True, text=True)
    assert missing.returncode == 2, missing

    # A score outside the 0 to 2 scale is refused. The matrices are indexed by the score, so a 3
    # would raise and a -1 would be read as the last category.
    off_scale = scores_file(root / "scores-off-scale.json", {"1": 0, "2": 3, "3": 1, "4": 1}, "off")
    broken = subprocess.run([sys.executable, "-I", str(SCRIPT), str(off_scale), str(b), "--json"],
                            capture_output=True, text=True)
    assert broken.returncode == 2, broken
    assert "refused" in broken.stderr, broken.stderr
    assert "Traceback" not in broken.stderr, broken.stderr
    negative = scores_file(root / "scores-negative.json", {"1": -1, "2": 1, "3": 1, "4": 1}, "neg")
    broken = subprocess.run([sys.executable, "-I", str(SCRIPT), str(negative), str(b), "--json"],
                            capture_output=True, text=True)
    assert broken.returncode == 2, broken
    assert "refused" in broken.stderr, broken.stderr
    # A score between two categories is refused too: it is not rounded into one of them.
    half = scores_file(root / "scores-half.json", {"1": 1.5, "2": 1, "3": 1, "4": 1}, "half")
    broken = subprocess.run([sys.executable, "-I", str(SCRIPT), str(half), str(b), "--json"],
                            capture_output=True, text=True)
    assert broken.returncode == 2, broken
    assert "refused" in broken.stderr, broken.stderr
    assert "Traceback" not in broken.stderr, broken.stderr
print("ok: 24 checks")
