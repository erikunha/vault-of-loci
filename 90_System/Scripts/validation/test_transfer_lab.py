"""Test for transfer_lab.py: the objectives that owe a transfer task, and the id the task carries."""
import json
import subprocess
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "transfer_lab.py"
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


OBJECTIVES = {
    "version": "v1",
    "objectives": [
        {"id": "o-one", "concept": "Retrieval_Practice", "mode": "recall",
         "criterion": "State the one week result.", "rubric_version": "v1"},
        {"id": "o-two", "concept": "Other_Concept", "mode": "apply",
         "criterion": "Apply the idea in a new case.", "rubric_version": "v1"},
    ],
}


def run(root, *flags):
    return subprocess.run([sys.executable, "-I", str(SCRIPT), "--ledger", str(root / "Attempts.jsonl"),
                           "--objectives", str(root / "Objectives.json"), *flags],
                          capture_output=True, text=True)


with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    (root / "Objectives.json").write_text(json.dumps(OBJECTIVES), encoding="utf-8")
    ledger = root / "Attempts.jsonl"
    events = [
        # Studied and recalled, never applied.
        event(event_id="s1", objective_id="o-one", item_id="item-a", mode="study",
              occurred_at=days_ago(40), first_attempt_correct=None, confidence=None),
        event(event_id="r1", objective_id="o-one", item_id="item-a", occurred_at=days_ago(20)),
        # Studied and applied twice already.
        event(event_id="s2", objective_id="o-two", item_id="item-b", mode="study",
              occurred_at=days_ago(60), first_attempt_correct=None, confidence=None),
        event(event_id="p1", objective_id="o-two", item_id="item-b", mode="apply", occurred_at=days_ago(30)),
        event(event_id="p2", objective_id="o-two", item_id="item-b-t1", mode="apply", occurred_at=days_ago(10)),
    ]
    ledger.write_text("".join(json.dumps(item) + "\n" for item in events), encoding="utf-8")

    out = run(root, "--json")
    assert out.returncode == 0, out.stderr
    report = json.loads(out.stdout)
    status = {row["objective_id"]: row for row in report["status"]}
    assert status["o-one"]["needs_transfer"] is True, status["o-one"]
    assert status["o-two"]["needs_transfer"] is False, status["o-two"]
    assert status["o-two"]["transfer_attempts"] == 2, status["o-two"]

    plan = report["plan"]
    assert len(plan) == 1, plan
    row = plan[0]
    assert row["objective_id"] == "o-one", row
    assert row["item_id"] == "o-one-t1", row
    assert row["criterion"] == "State the one week result.", row
    assert row["concept"] == "Retrieval_Practice", row
    assert row["rubric"]["2"], row

    text = run(root)
    assert "Tasks to write" in text.stdout, text.stdout
    assert "item id: o-one-t1" in text.stdout, text.stdout
    assert "o-two" in text.stdout, text.stdout

    # A second transfer task carries the next number, even when the first one needed help.
    helped_apply = [event(event_id="h1", objective_id="o-three", item_id="item-c", mode="apply",
                           first_attempt_correct=False, assistance="hint", hints_used=1,
                           occurred_at=days_ago(5))]
    ledger.write_text(json.dumps(helped_apply[0]) + "\n", encoding="utf-8")
    again = json.loads(run(root, "--json").stdout)
    assert again["plan"][0]["item_id"] == "o-three-t2", again["plan"]
    assert again["plan"][0]["objective_id"] == "o-three", again["plan"]

    # An objective that applied the idea cleanly owes nothing.
    events.append(event(event_id="p3", objective_id="o-one", item_id="item-a-t1", mode="apply",
                        occurred_at=days_ago(5)))
    ledger.write_text("".join(json.dumps(item) + "\n" for item in events), encoding="utf-8")
    measured = json.loads(run(root, "--json").stdout)
    assert not [row for row in measured["plan"] if row["objective_id"] == "o-one"], measured["plan"]

    # An objective that was only studied with help still owes a transfer.
    helped = [event(event_id="h2", objective_id="o-four", item_id="item-d", mode="recall",
                    first_attempt_correct=False, assistance="hint", hints_used=1, occurred_at=days_ago(3))]
    ledger.write_text(json.dumps(helped[0]) + "\n", encoding="utf-8")
    only = json.loads(run(root, "--json").stdout)
    assert only["plan"][0]["objective_id"] == "o-four", only["plan"]

    # A task the agent graded still holds its id, so the next task cannot be handed the same id.
    graded = [event(event_id="g1", objective_id="o-five", item_id="o-five-t1", mode="apply",
                    grading_method="agent_graded", occurred_at=days_ago(2))]
    ledger.write_text(json.dumps(graded[0]) + "\n", encoding="utf-8")
    after_graded = json.loads(run(root, "--json").stdout)
    assert after_graded["plan"][0]["item_id"] == "o-five-t2", after_graded["plan"]

    # The same task attempted twice is one task, so the next number does not skip one.
    twice = [event(event_id="t1", objective_id="o-six", item_id="o-six-t1", mode="apply",
                   first_attempt_correct=False, assistance="hint", hints_used=1, occurred_at=days_ago(4)),
             event(event_id="t2", objective_id="o-six", item_id="o-six-t1", mode="apply",
                   first_attempt_correct=False, assistance="hint", hints_used=1, occurred_at=days_ago(2))]
    ledger.write_text("".join(json.dumps(item) + "\n" for item in twice), encoding="utf-8")
    after_twice = json.loads(run(root, "--json").stdout)
    assert after_twice["plan"][0]["item_id"] == "o-six-t2", after_twice["plan"]

    # A line that could not be read is reported, not dropped in silence.
    ledger.write_text("{not json\n" + json.dumps(graded[0]) + "\n", encoding="utf-8")
    corrupt = json.loads(run(root, "--json").stdout)
    assert corrupt["problems"], corrupt
    assert "not valid JSON" in corrupt["problems"][0], corrupt["problems"]
    corrupt_text = run(root)
    assert "could not be read" in corrupt_text.stdout, corrupt_text.stdout

    # A ledger that is not there is a problem, not an empty ledger.
    missing = subprocess.run([sys.executable, "-I", str(SCRIPT), "--ledger", str(root / "No_Ledger.jsonl"),
                               "--objectives", str(root / "Objectives.json")],
                              capture_output=True, text=True)
    assert missing.returncode == 0, missing.stderr
    assert "could not be read" in missing.stdout, missing.stdout
print("ok: 19 checks")
