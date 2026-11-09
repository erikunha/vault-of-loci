"""Test for calibration_coach.py: it measures how well the confidence tracks the result."""
import json
import subprocess
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "calibration_coach.py"
TODAY = date.today()


def days_ago(days):
    return (TODAY - timedelta(days=days)).isoformat()


def event(**fields):
    base = {
        "event_id": "attempt-test",
        "objective_id": "o-recall",
        "item_id": "item-a",
        "occurred_at": days_ago(1),
        "mode": "recall",
        "first_attempt_correct": True,
        "confidence": 3,
        "confidence_probability": None,
        "hints_used": 0,
        "assistance": "none",
        "rubric_version": "v1",
        "grading_method": "learner_confirmed",
        "source_revision": None,
        "duration_minutes": 5,
    }
    base.update(fields)
    return base


def run(ledger, *extra):
    """The coach on a ledger, as JSON."""
    result = subprocess.run([sys.executable, "-I", str(SCRIPT), "--ledger", str(ledger), "--json"]
                            + list(extra), capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    ledger = root / "Attempts.jsonl"
    events = [
        # Two attempts with an explicit probability: 0.9 and wrong, 0.1 and right.
        event(event_id="p-high-wrong", item_id="item-a", occurred_at=days_ago(10),
              first_attempt_correct=False, confidence=None, confidence_probability=0.9),
        event(event_id="p-low-right", item_id="item-b", occurred_at=days_ago(9),
              confidence=None, confidence_probability=0.1),
        # Two attempts with the 1 to 5 scale only: confidence 5 and wrong, confidence 1 and right.
        event(event_id="c-five-wrong", item_id="item-c", occurred_at=days_ago(8),
              first_attempt_correct=False, confidence=5),
        event(event_id="c-one-right", item_id="item-d", occurred_at=days_ago(7), confidence=1),
        # A sure and wrong attempt in another objective.
        event(event_id="other-sure-wrong", objective_id="o-apply", item_id="item-e",
              occurred_at=days_ago(6), first_attempt_correct=False, confidence=5),
        # Not counted: a wrong attempt with a hint.
        event(event_id="with-help", item_id="item-f", occurred_at=days_ago(5),
              first_attempt_correct=False, confidence=5, assistance="hint", hints_used=1),
        # Not counted: an attempt graded by an agent.
        event(event_id="agent-graded", item_id="item-g", occurred_at=days_ago(4),
              grading_method="agent_graded", confidence=1),
        # Not counted: a study event.
        event(event_id="study", item_id="item-h", occurred_at=days_ago(3), mode="study",
              first_attempt_correct=None, confidence=None),
    ]
    ledger.write_text("".join(json.dumps(item) + "\n" for item in events), encoding="utf-8")

    report = run(ledger)

    # Five attempts count: the two with help, the one graded by an agent and the study are out.
    assert report["attempts"] == 5, report["attempts"]
    assert report["excluded"] == {"help": 1, "agent_graded": 1, "not_graded": 1}, report["excluded"]

    # The Brier score with an explicit probability: (0.9 - 0)^2 and (0.1 - 1)^2 give 0.81 and 0.81,
    # so the mean is 0.81.
    assert report["overall"]["brier_explicit"] == 0.81, report["overall"]
    assert report["overall"]["n_explicit"] == 2, report["overall"]

    # The Brier score with the 1 to 5 scale: confidence 5 maps to 1.0 and confidence 1 to 0.0,
    # so the two errors are 1.0 and 1.0 and the mean is 1.0.
    assert report["overall"]["brier_ordinal"] == 1.0, report["overall"]
    assert report["overall"]["n_ordinal"] == 3, report["overall"]
    assert report["overall"]["scale_ordinal"] == "(confidence - 1) / 4", report["overall"]

    # The reliability table splits the five predictions into five bins.
    bins = report["overall"]["reliability"]
    assert len(bins) == 5, bins
    assert [row["attempts"] for row in bins] == [2, 0, 0, 0, 3], bins
    assert bins[0]["rate"] == 1.0, bins
    assert bins[4]["attempts"] == 3 and bins[4]["correct"] == 0, bins

    # The sharpest cases: sure and wrong, and unsure and right.
    sure = report["overall"]["confident_and_wrong"]
    assert [case["event_id"] for case in sure] == ["p-high-wrong", "c-five-wrong", "other-sure-wrong"], sure
    unsure = report["overall"]["unsure_and_right"]
    assert [case["event_id"] for case in unsure] == ["p-low-right", "c-one-right"], unsure

    # The numbers per objective.
    assert sorted(report["objectives"]) == ["o-apply", "o-recall"], report["objectives"]
    assert report["objectives"]["o-apply"]["attempts"] == 1, report["objectives"]
    assert report["objectives"]["o-recall"]["attempts"] == 4, report["objectives"]

    # One objective only.
    one = run(ledger, "--objective", "o-apply")
    assert list(one["objectives"]) == ["o-apply"], one["objectives"]
    assert one["attempts"] == 1, one["attempts"]
    assert one["objective"] == "o-apply", one["objective"]

    # The text report of one objective shows that objective and no other.
    only = subprocess.run([sys.executable, "-I", str(SCRIPT), "--ledger", str(ledger),
                           "--objective", "o-apply"], capture_output=True, text=True)
    assert only.returncode == 0, only.stderr
    assert "objective: o-apply" in only.stdout, only.stdout
    assert "Objective o-recall" not in only.stdout, only.stdout

    # The number of bins can change.
    fewer = run(ledger, "--bins", "2")
    assert len(fewer["overall"]["reliability"]) == 2, fewer["overall"]["reliability"]

    # A ledger with no attempt says so instead of failing.
    empty = root / "empty.jsonl"
    empty.write_text("", encoding="utf-8")
    blank = subprocess.run([sys.executable, "-I", str(SCRIPT), "--ledger", str(empty)],
                           capture_output=True, text=True)
    assert blank.returncode == 0, blank.stderr
    assert "no attempt counted yet" in blank.stdout, blank.stdout

    # The text report says what it measures and what it does not.
    text = subprocess.run([sys.executable, "-I", str(SCRIPT), "--ledger", str(ledger)],
                          capture_output=True, text=True)
    assert text.returncode == 0, text.stderr
    assert "Calibration coach" in text.stdout, text.stdout
    assert "gap between how sure the learner was and what happened" in text.stdout, text.stdout
    assert "does not measure what was learned" in text.stdout, text.stdout
    assert "approximation of an ordinal scale" in text.stdout, text.stdout
    assert "a bin with only a few attempts means nothing" in text.stdout, text.stdout
    assert "Sure and wrong" in text.stdout, text.stdout
    assert "Unsure and right" in text.stdout, text.stdout

    # A bad number of bins exits 1.
    bad = subprocess.run([sys.executable, "-I", str(SCRIPT), "--ledger", str(ledger), "--bins", "0"],
                         capture_output=True, text=True)
    assert bad.returncode == 1, bad.stdout
    assert "invalid bins" in bad.stdout, bad.stdout
print("ok: 36 checks")
