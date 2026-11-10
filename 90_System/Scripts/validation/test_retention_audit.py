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


def run_with_objectives(root, objectives, *flags):
    return subprocess.run([sys.executable, "-I", str(SCRIPT), "--ledger", str(root / "Attempts.jsonl"),
                           "--objectives", str(objectives), *flags],
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

    # An objective measured only by transfer is not due. An attempt at a horizon counts whether it
    # was a recall, an explain, an apply or a discriminate. Before the fix this read "due at 7
    # days" forever, because the decision looked only at the retention column.
    transfer_only = [
        event(event_id="t1", objective_id="o-apply", item_id="item-t", mode="study",
              occurred_at=days_ago(200), first_attempt_correct=None, confidence=None),
        event(event_id="t2", objective_id="o-apply", item_id="item-t", mode="apply", occurred_at=days_ago(193)),
        event(event_id="t3", objective_id="o-apply", item_id="item-t", mode="apply", occurred_at=days_ago(170)),
        event(event_id="t4", objective_id="o-apply", item_id="item-t", mode="apply", occurred_at=days_ago(110)),
    ]
    ledger.write_text("".join(json.dumps(item) + "\n" for item in transfer_only), encoding="utf-8")
    only = run(root, "--json")
    assert only.returncode == 0, only.stderr
    only_report = json.loads(only.stdout)
    only_rows = {row["objective_id"]: row for row in only_report["audit"]["objectives"]}
    assert only_rows["o-apply"]["status"] == "measured", only_rows["o-apply"]
    # An attempt counts for every horizon it reached, so the attempt 90 days after exposure is
    # eligible at 7, 30 and 90 days.
    assert only_rows["o-apply"]["transfer"]["7"]["eligible"] == 3, only_rows["o-apply"]
    assert only_rows["o-apply"]["transfer"]["90"]["eligible"] == 1, only_rows["o-apply"]
    assert only_rows["o-apply"]["retention"]["7"]["eligible"] == 0, only_rows["o-apply"]
    assert only_report["audit"]["due"] == [], only_report["audit"]
    assert only_report["plan"] == [], only_report["plan"]

    # A horizon that has not arrived yet is not owed. The objective was studied five days ago and
    # tested, so the 7 day horizon is still two days away. Before this, the audit said "due at 7
    # days" about a delay that had not even started.
    soon = [
        event(event_id="n1", objective_id="o-soon", item_id="item-n", mode="study",
              occurred_at=days_ago(5), first_attempt_correct=None, confidence=None),
        event(event_id="n2", objective_id="o-soon", item_id="item-n", occurred_at=days_ago(3)),
    ]
    ledger.write_text("".join(json.dumps(item) + "\n" for item in soon), encoding="utf-8")
    early = run(root, "--json")
    assert early.returncode == 0, early.stderr
    early_report = json.loads(early.stdout)
    early_rows = {row["objective_id"]: row for row in early_report["audit"]["objectives"]}
    assert early_rows["o-soon"]["status"] == "not due yet: the 7 day horizon arrives in 2 days", early_rows["o-soon"]
    assert early_rows["o-soon"]["days_since_exposure"] == 5, early_rows["o-soon"]
    assert early_report["audit"]["due"] == [], early_report["audit"]
    assert early_report["plan"] == [], early_report["plan"]

    # An attempt graded by the agent is not the same as an attempt made with help. The learner has
    # to confirm the grade, so this objective is not measured either, but the next step is
    # different: the learner has to say whether the answer was right.
    agent_graded = [
        event(event_id="g1", objective_id="o-agent", item_id="item-g", mode="study",
              occurred_at=days_ago(100), first_attempt_correct=None, confidence=None),
        event(event_id="g2", objective_id="o-agent", item_id="item-g", occurred_at=days_ago(93),
              grading_method="agent_graded"),
    ]
    ledger.write_text("".join(json.dumps(item) + "\n" for item in agent_graded), encoding="utf-8")
    graded = run(root, "--json")
    assert graded.returncode == 0, graded.stderr
    graded_report = json.loads(graded.stdout)
    graded_rows = {row["objective_id"]: row for row in graded_report["audit"]["objectives"]}
    assert graded_rows["o-agent"]["status"] == "only graded by the agent", graded_rows["o-agent"]
    assert {row["objective_id"] for row in graded_report["audit"]["untested"]} == {"o-agent"}, graded_report["audit"]

    # An objective registered and never studied does not appear in the audit at all, so the audit
    # names it separately instead of leaving the learner to think there is nothing to do.
    registry = root / "Objectives.json"
    registry.write_text(json.dumps({"version": "v1", "objectives": [
        {"id": "o-never", "concept": "C", "mode": "recall", "criterion": "State the one result."},
        {"id": "o-agent", "concept": "C", "mode": "recall", "criterion": "State the other result."},
    ]}), encoding="utf-8")
    named = run_with_objectives(root, registry)
    assert named.returncode == 0, named.stderr
    assert "Registered as a learning objective, with no attempt in the ledger" in named.stdout, named.stdout
    assert "o-never" in named.stdout, named.stdout
    assert "o-agent" not in named.stdout.split("Registered as a learning objective")[1], named.stdout

    # "Nothing is due" is not the same as "everything was measured". A ledger where nothing was
    # tested owes nothing at a horizon, and saying it was measured would be the one thing the
    # audit must never say.
    never_tested = [
        event(event_id="u1", objective_id="o-untouched", item_id="item-u", mode="study",
              occurred_at=days_ago(3), first_attempt_correct=None, confidence=None),
    ]
    ledger.write_text("".join(json.dumps(item) + "\n" for item in never_tested), encoding="utf-8")
    untouched = run(root)
    assert untouched.returncode == 0, untouched.stderr
    assert "Nothing is due" in untouched.stdout, untouched.stdout
    assert "every objective that could be measured was measured" not in untouched.stdout, untouched.stdout
    assert "Nothing was measured at any horizon either" in untouched.stdout, untouched.stdout

    # A ledger where a horizon really was measured keeps the old sentence.
    fully_measured = [
        event(event_id="m1", objective_id="o-done", item_id="item-d", mode="study",
              occurred_at=days_ago(200), first_attempt_correct=None, confidence=None),
        event(event_id="m2", objective_id="o-done", item_id="item-d", occurred_at=days_ago(193)),
        event(event_id="m3", objective_id="o-done", item_id="item-d", occurred_at=days_ago(170)),
        event(event_id="m4", objective_id="o-done", item_id="item-d", occurred_at=days_ago(110)),
    ]
    ledger.write_text("".join(json.dumps(item) + "\n" for item in fully_measured), encoding="utf-8")
    done = run(root)
    assert done.returncode == 0, done.stderr
    assert "every objective that could be measured was measured" in done.stdout, done.stdout

    # A ledger with one measured objective and one that was never tested is not a ledger where
    # everything was measured. The audit says how many of each, and does not claim the rest.
    mixed = fully_measured + [
        event(event_id="x1", objective_id="o-untouched", item_id="item-x", mode="study",
              occurred_at=days_ago(3), first_attempt_correct=None, confidence=None),
    ]
    ledger.write_text("".join(json.dumps(item) + "\n" for item in mixed), encoding="utf-8")
    partly = run(root)
    assert partly.returncode == 0, partly.stderr
    assert "every objective that could be measured was measured" not in partly.stdout, partly.stdout
    assert "1 of 2 objectives were measured" in partly.stdout, partly.stdout

    # An empty ledger still names the objectives that are registered and were never studied.
    ledger.write_text("", encoding="utf-8")
    empty_registry = run_with_objectives(root, registry)
    assert empty_registry.returncode == 0, empty_registry.stderr
    assert "the ledger is empty" in empty_registry.stdout, empty_registry.stdout
    assert "Registered as a learning objective, with no attempt in the ledger" in empty_registry.stdout, empty_registry.stdout
    assert "o-never" in empty_registry.stdout, empty_registry.stdout

    # The JSON output carries the same list. With an empty ledger both registered objectives are
    # absent from it, so both are named.
    empty_json = run_with_objectives(root, registry, "--json")
    assert empty_json.returncode == 0, empty_json.stderr
    empty_report = json.loads(empty_json.stdout)
    assert [entry["id"] for entry in empty_report["registered_without_events"]] == ["o-agent", "o-never"], empty_report
    assert empty_report["registered_without_events"][1]["criterion"] == "State the one result.", empty_report

print("ok: 47 checks")
