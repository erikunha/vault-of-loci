"""Test for schedule_review.py and scheduler.py: the plan ranks the right items for the right reason."""
import json
import subprocess
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "schedule_review.py"
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
        # A solid item: two correct tries, one of them recent.
        event(event_id="a1", item_id="item-a", occurred_at=days_ago(40), confidence=5),
        event(event_id="a2", item_id="item-a", occurred_at=days_ago(3), confidence=5),
        # An item whose last try was wrong, recent.
        event(event_id="b1", item_id="item-b", occurred_at=days_ago(2), first_attempt_correct=False, confidence=2),
        # An item that was right long ago and never came back.
        event(event_id="c1", item_id="item-c", occurred_at=days_ago(75), confidence=4),
        # An item that only ever had a hint.
        event(event_id="d1", item_id="item-d", occurred_at=days_ago(2), first_attempt_correct=False,
              assistance="hint", hints_used=1),
        # An objective that was studied and never tested without help.
        event(event_id="e1", objective_id="o-two", item_id="item-e", occurred_at=days_ago(6),
              first_attempt_correct=False, assistance="strong_hint", hints_used=1),
        # An objective that was only studied, with no attempt at all.
        event(event_id="t1", objective_id="o-three", item_id="item-f", mode="study", occurred_at=days_ago(9),
              first_attempt_correct=None, confidence=None),
    ]
    ledger.write_text("".join(json.dumps(item) + "\n" for item in events), encoding="utf-8")

    out = run(root, "--json")
    assert out.returncode == 0, out.stderr
    plan = json.loads(out.stdout)
    entries = {entry["item_id"] or entry["objective_id"]: entry for entry in plan["entries"]}
    assert "item-b" in entries, plan["entries"]
    assert "the last attempt was wrong" in entries["item-b"]["why"], entries["item-b"]
    assert entries["item-b"]["priority"] > entries["item-a"]["priority"], "a wrong last try comes first"
    assert "not seen for 75 days" in entries["item-c"]["why"], entries["item-c"]
    assert entries["item-c"]["priority"] > entries["item-a"]["priority"], "the stale item comes before the solid one"
    assert entries["item-a"]["strength"] > 0.8, entries["item-a"]
    # The item that only had a hint is still in the plan: it needs a clean attempt.
    assert "item-d" in entries, entries
    assert "every attempt so far needed help" in entries["item-d"]["why"], entries["item-d"]
    # An objective that was only studied and never attempted shows up as a new item.
    assert any(entry["new"] and entry["objective_id"] == "o-three" for entry in plan["entries"]), plan["entries"]
    assert plan["days_since_last"] == 2, plan["days_since_last"]

    # The cap holds, and catch-up mode stops the new cards.
    many = [event(event_id=f"x{n}", item_id=f"item-x{n}", occurred_at=days_ago(n + 1)) for n in range(30)]
    ledger.write_text("".join(json.dumps(item) + "\n" for item in many), encoding="utf-8")
    capped = json.loads(run(root, "--json", "--cap", "5").stdout)
    assert capped["catch_up"] is True, capped
    assert len([entry for entry in capped["entries"] if not entry["new"]]) == 5, capped["entries"]
    assert not [entry for entry in capped["entries"] if entry["new"]], "no new cards in catch-up mode"

    # A short queue keeps the new cards.
    short = [event(event_id="s1", item_id="item-s1", occurred_at=days_ago(2)),
             event(event_id="s2", objective_id="o-new", item_id="item-s2", mode="study", occurred_at=days_ago(3),
                   first_attempt_correct=None, confidence=None)]
    ledger.write_text("".join(json.dumps(item) + "\n" for item in short), encoding="utf-8")
    small = json.loads(run(root, "--json").stdout)
    assert small["catch_up"] is False, small
    assert [entry for entry in small["entries"] if entry["new"]], small["entries"]

    # After a break the recovery plan is a short diagnostic, not the whole queue.
    away = [event(event_id="r1", item_id="item-r1", occurred_at=days_ago(40)),
            event(event_id="r2", item_id="item-r2", occurred_at=days_ago(41), first_attempt_correct=False)]
    ledger.write_text("".join(json.dumps(item) + "\n" for item in away), encoding="utf-8")
    recovery = run(root, "--recovery", "--json")
    assert recovery.returncode == 0, recovery.stderr
    plan_back = json.loads(recovery.stdout)
    assert plan_back["days_away"] == 40, plan_back
    assert len(plan_back["entries"]) <= 5, plan_back
    text = run(root, "--recovery")
    assert "Recovery after 40 days away" in text.stdout, text.stdout

    # A recent attempt means there is no break to recover from.
    ledger.write_text(json.dumps(event(event_id="n1", occurred_at=days_ago(1))) + "\n", encoding="utf-8")
    fresh = run(root, "--recovery")
    assert "no break to recover from" in fresh.stdout, fresh.stdout
print("ok: 15 checks")
