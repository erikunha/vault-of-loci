"""Test for retention_report.py: it measures retention, transfer, calibration and the learned rule."""
import json
import subprocess
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "retention_report.py"
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


with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    ledger = root / "Attempts.jsonl"
    events = [
        # The objective was first studied 200 days ago. Every horizon counts from that day.
        event(event_id="study-recall", objective_id="o-recall", item_id="item-a", mode="study",
              occurred_at=days_ago(200), first_attempt_correct=None, confidence=None),
        # A recall four days after the study: too recent for any horizon.
        event(event_id="too-recent", occurred_at=days_ago(196), confidence=2),
        # Correct recalls 7, 30, 40, 50 and 90 days after the study.
        event(event_id="recall-07", occurred_at=days_ago(193), confidence=5),
        event(event_id="recall-30", occurred_at=days_ago(170), confidence=3),
        event(event_id="recall-40", occurred_at=days_ago(160), confidence=2),
        event(event_id="recall-50", occurred_at=days_ago(150), confidence=4),
        event(event_id="recall-90", occurred_at=days_ago(110), confidence=5),
        # A wrong recall with a hint: recorded, but it does not count.
        event(event_id="with-help", item_id="item-b", occurred_at=days_ago(100),
              first_attempt_correct=False, assistance="hint", hints_used=1),
        # A correct recall graded by an agent: recorded, but it does not count.
        event(event_id="agent-graded", item_id="item-c", occurred_at=days_ago(100),
              grading_method="agent_graded"),
        # Two events with an explicit probability, for the Brier score.
        event(event_id="prob-high", item_id="item-d", occurred_at=days_ago(120),
              first_attempt_correct=False, confidence=None, confidence_probability=0.9),
        event(event_id="prob-low", item_id="item-d", occurred_at=days_ago(118),
              confidence=None, confidence_probability=0.5),
        # A transfer task on an item the learner had never seen.
        event(event_id="apply-new", item_id="item-f", occurred_at=days_ago(140), mode="apply"),
        # A second objective, studied on the same day, with a transfer task of its own.
        event(event_id="study-apply", objective_id="o-apply", item_id="item-g", mode="study",
              occurred_at=days_ago(200), first_attempt_correct=None, confidence=None),
        event(event_id="apply-other", objective_id="o-apply", item_id="item-h", mode="apply",
              occurred_at=days_ago(100)),
    ]
    ledger.write_text("".join(json.dumps(item) + "\n" for item in events), encoding="utf-8")

    run = subprocess.run([sys.executable, "-I", str(SCRIPT), "--ledger", str(ledger), "--json"],
                         capture_output=True, text=True)
    assert run.returncode == 0, run.stderr
    report = json.loads(run.stdout)

    # Retention counts first attempts without help at each horizon, from the day the objective
    # was first studied.
    assert report["retention"]["7"] == {"correct": 6, "eligible": 7, "rate": 0.8571}, report["retention"]
    assert report["retention"]["30"] == {"correct": 5, "eligible": 6, "rate": 0.8333}, report["retention"]
    assert report["retention"]["90"] == {"correct": 1, "eligible": 1, "rate": 1.0}, report["retention"]

    # Transfer uses apply tasks, including one on an item never seen before.
    assert report["transfer"]["30"] == {"correct": 2, "eligible": 2, "rate": 1.0}, report["transfer"]
    assert report["transfer"]["90"] == {"correct": 1, "eligible": 1, "rate": 1.0}, report["transfer"]

    # The attempts that do not count are counted and named.
    assert report["excluded"]["help"] == 1, report["excluded"]
    assert report["excluded"]["agent_graded"] == 1, report["excluded"]
    assert report["excluded"]["too_recent"] == 1, report["excluded"]

    # Brier score: the explicit probabilities give 0.81 and 0.25, so the mean is 0.53.
    assert report["calibration"]["brier_explicit"] == 0.53, report["calibration"]
    assert report["calibration"]["n_explicit"] == 2, report["calibration"]
    # The 1 to 5 scale mapped to (confidence - 1) / 4 over the eight attempts with a confidence.
    assert report["calibration"]["n_ordinal"] == 8, report["calibration"]
    assert report["calibration"]["brier_ordinal"] == 0.2422, report["calibration"]

    # Learned means recalled twice on different days and used once in a task not seen.
    assert report["learned"] == ["o-recall"], report["learned"]

    # The exposure day is the day the objective was first studied.
    assert report["exposure"]["o-recall"] == days_ago(200), report["exposure"]

    text = subprocess.run([sys.executable, "-I", str(SCRIPT), "--ledger", str(ledger)],
                          capture_output=True, text=True)
    assert text.returncode == 0, text.stderr
    assert "Retention" in text.stdout, text.stdout
    assert "Transfer" in text.stdout, text.stdout
    assert "Calibration" in text.stdout, text.stdout
    assert "no eligible attempt" not in text.stdout, text.stdout
    assert "forecast is not a measurement" in text.stdout, text.stdout

    # A report of an empty ledger says so instead of failing.
    empty = root / "empty.jsonl"
    empty.write_text("", encoding="utf-8")
    blank = subprocess.run([sys.executable, "-I", str(SCRIPT), "--ledger", str(empty)],
                           capture_output=True, text=True)
    assert blank.returncode == 0, blank.stderr
    assert "no attempt recorded yet" in blank.stdout, blank.stdout

    # A report of one objective only leaves the other out.
    only = subprocess.run([sys.executable, "-I", str(SCRIPT), "--ledger", str(ledger),
                           "--objective", "o-apply", "--json"], capture_output=True, text=True)
    assert only.returncode == 0, only.stderr
    one = json.loads(only.stdout)
    assert one["objectives"] == ["o-apply"], one["objectives"]
    assert one["transfer"]["30"] == {"correct": 1, "eligible": 1, "rate": 1.0}, one["transfer"]

    # An attempt with no verdict says nothing about what was remembered. Counting it would print
    # a rate that no event supports.
    no_verdict = [
        event(event_id="n1", objective_id="o-none", item_id="item-n", mode="study",
              occurred_at=days_ago(100), first_attempt_correct=None, confidence=None),
        event(event_id="n2", objective_id="o-none", item_id="item-n", occurred_at=days_ago(30),
              first_attempt_correct=None),
    ]
    ledger.write_text("".join(json.dumps(item) + "\n" for item in no_verdict), encoding="utf-8")
    ungraded = subprocess.run([sys.executable, "-I", str(SCRIPT), "--ledger", str(ledger), "--json"],
                              capture_output=True, text=True)
    assert ungraded.returncode == 0, ungraded.stderr
    report = json.loads(ungraded.stdout)
    assert report["retention"]["7"]["eligible"] == 0, report["retention"]
    assert report["retention"]["7"]["rate"] is None, report["retention"]

    # An attempt the agent graded is evidence about the agent, not about the learner. It cannot
    # make an objective learned.
    by_agent = [
        event(event_id="g1", objective_id="o-agent", item_id="item-g", mode="study",
              occurred_at=days_ago(100), first_attempt_correct=None, confidence=None),
        event(event_id="g2", objective_id="o-agent", item_id="item-g", occurred_at=days_ago(30),
              grading_method="agent_graded"),
        event(event_id="g3", objective_id="o-agent", item_id="item-h", occurred_at=days_ago(22),
              grading_method="agent_graded"),
        event(event_id="g4", objective_id="o-agent", item_id="item-i", mode="apply",
              occurred_at=days_ago(15), grading_method="agent_graded"),
    ]
    ledger.write_text("".join(json.dumps(item) + "\n" for item in by_agent), encoding="utf-8")
    graded = subprocess.run([sys.executable, "-I", str(SCRIPT), "--ledger", str(ledger), "--json"],
                            capture_output=True, text=True)
    assert graded.returncode == 0, graded.stderr
    report = json.loads(graded.stdout)
    assert report["learned"] == [], report["learned"]
    assert report["excluded"]["agent_graded"] == 3, report["excluded"]

    # A ledger that holds events but no graded attempt is not a ledger with nothing in it. The
    # report says how many events there are, so the reader does not read "0 attempts" as "no
    # record at all".
    study_only = [
        event(event_id="s1", objective_id="o-study", item_id="item-s", mode="study",
              occurred_at=days_ago(100), first_attempt_correct=None, confidence=None),
        event(event_id="s2", objective_id="o-study", item_id="item-s2", mode="study",
              occurred_at=days_ago(50), first_attempt_correct=None, confidence=None),
    ]
    ledger.write_text("".join(json.dumps(item) + "\n" for item in study_only), encoding="utf-8")
    studied = subprocess.run([sys.executable, "-I", str(SCRIPT), "--ledger", str(ledger)],
                             capture_output=True, text=True)
    assert studied.returncode == 0, studied.stderr
    assert "events recorded: 2" in studied.stdout, studied.stdout
    assert "graded attempts: 0" in studied.stdout, studied.stdout
    assert "2 event(s) recorded, none of them a graded attempt yet" in studied.stdout, studied.stdout
    assert "no attempt recorded yet" not in studied.stdout, studied.stdout

print("ok: 30 checks")
