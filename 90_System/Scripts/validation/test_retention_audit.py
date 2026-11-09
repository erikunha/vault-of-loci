"""Test for retention_audit.py and audit.py: what was measured, what is due, what was never tested."""
import json
import subprocess
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "retention_audit.py"
TODAY = date.today()


def days_ago(days):
    return (TODAY - timedelta(days=days)).isoformat()


def event(**fields):
    base = {
        "event_id": "attempt-test",
        "objective_id": "o-one",
        "item_id": "item-a",
        "occurred_at": days_ago(1),
        "mode": "recall",
        "first_attempt_correct": True,
        "confidence": 4,
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


def run(root, *flags):
    return subprocess.run([sys.executable, "-I", str(SCRIPT), "--ledger", str(root / "Attempts.jsonl"), *flags],
                          capture_output=True, text=True)


with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    ledger = root / "Attempts.jsonl"
    events = [
        # Studied 100 days ago, clean attempts at 7 and 30 days: those horizons are measured
        # and the 90 day one is still waiting.
        event(event_id="s1", objective_id="o-one", item_id="item-a", mode="study",
              occurred_at=days_ago(100), first_attempt_correct=None, confidence=None),
        event(event_id="a1", objective_id="o-one", item_id="item-a", occurred_at=days_ago(93)),
        event(event_id="a2", objective_id="o-one", item_id="item-a", occurred_at=days_ago(70)),
        # Studied and never tested.
        event(event_id="s2", objective_id="o-two", item_id="item-b", mode="study",
              occurred_at=days_ago(10), first_attempt_correct=None, confidence=None),
        # Tested only with a hint.
        event(event_id="h1", objective_id="o-three", item_id="item-c", occurred_at=days_ago(12),
              first_attempt_correct=False, assistance="hint", hints_used=1),
    ]
    ledger.write_text("".join(json.dumps(item) + "\n" for item in events), encoding="utf-8")

    out = run(root, "--json")
    assert out.returncode == 0, out.stderr
    report = json.loads(out.stdout)
    rows = {row["objective_id"]: row for row in report["audit"]["objectives"]}
    assert rows["o-one"]["status"] == "due at 90 days", rows["o-one"]
    assert rows["o-one"]["retention"]["30"]["eligible"] == 1, rows["o-one"]
    assert rows["o-two"]["status"] == "never tested", rows["o-two"]
    assert rows["o-three"]["status"] == "only tested with help", rows["o-three"]
    assert {row["objective_id"] for row in report["audit"]["untested"]} == {"o-two", "o-three"}, report["audit"]
    assert [row["objective_id"] for row in report["audit"]["due"]] == ["o-one"], report["audit"]

    plan = report["plan"]
    assert len(plan) == 1, plan
    assert plan[0]["objective_id"] == "o-one", plan
    assert plan[0]["horizon"] == 90, plan
    assert plan[0]["example_item"] == "o-one-d90", plan

    text = run(root)
    assert "Due now: a delayed attempt is missing" in text.stdout, text.stdout
    assert "o-one at 90 days" in text.stdout, text.stdout
    assert "Never measured without help" in text.stdout, text.stdout

    # An empty ledger says so instead of failing.
    empty = root / "empty.jsonl"
    empty.write_text("", encoding="utf-8")
    blank = run(root.replace(root / "Attempts.jsonl") if False else root)
    ledger.write_text("", encoding="utf-8")
    nothing = run(root)
    assert nothing.returncode == 0, nothing.stderr
    assert "the ledger is empty" in nothing.stdout, nothing.stdout

    # A ledger with every horizon measured reports nothing due.
    measured = [
        event(event_id="m1", objective_id="o-full", item_id="item-m", mode="study",
              occurred_at=days_ago(200), first_attempt_correct=None, confidence=None),
        event(event_id="m2", objective_id="o-full", item_id="item-m", occurred_at=days_ago(193)),
        event(event_id="m3", objective_id="o-full", item_id="item-m", occurred_at=days_ago(170)),
        event(event_id="m4", objective_id="o-full", item_id="item-m", occurred_at=days_ago(110)),
    ]
    ledger.write_text("".join(json.dumps(item) + "\n" for item in measured), encoding="utf-8")
    done = run(root)
    assert "Nothing is due" in done.stdout, done.stdout
print("ok: 12 checks")
