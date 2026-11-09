"""Test for dependency_check.py: the prerequisites of a concept and the gaps that come before it."""
import json
import subprocess
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "dependency_check.py"
TODAY = date.today()


def days_ago(days):
    return (TODAY - timedelta(days=days)).isoformat()


def event(**fields):
    base = {
        "event_id": "attempt-test",
        "objective_id": "alpha-recall",
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


CONCEPT_MAP = """---
type: practice
track: "[[Track]]"
tags: [type/practice]
---

# Concept map

| Order | Concept | Needs first | Threshold | Status |
|---|---|---|---|---|
| 1 | [[Alpha\\|Alpha]] | none |  | in progress |
| 2 | [[Beta\\|Beta]] | [[Alpha\\|Alpha]] |  | in progress |
"""

CANVAS = {
    "nodes": [
        {"id": "n1", "type": "file", "file": "20_Concepts/Alpha.md"},
        {"id": "n2", "type": "file", "file": "20_Concepts/Beta.md"},
    ],
    "edges": [{"id": "e1", "fromNode": "n1", "toNode": "n2"}],
}

OBJECTIVES = {
    "version": "v1",
    "objectives": [
        {"id": "alpha-recall", "concept": "Alpha", "mode": "recall", "criterion": "c", "rubric_version": "v1"},
        {"id": "beta-apply", "concept": "Beta", "mode": "apply", "criterion": "c", "rubric_version": "v1"},
    ],
}


def run(root, *flags):
    return subprocess.run([sys.executable, "-I", str(SCRIPT), "--ledger", str(root / "Attempts.jsonl"),
                           "--root", str(root), "--objectives", str(root / "Objectives.json"), *flags],
                          capture_output=True, text=True)


with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    (root / "Objectives.json").write_text(json.dumps(OBJECTIVES), encoding="utf-8")
    (root / "20_Concepts").mkdir()
    (root / "20_Concepts" / "Alpha.md").write_text("# Alpha\n", encoding="utf-8")
    (root / "20_Concepts" / "Beta.md").write_text("# Beta\n", encoding="utf-8")
    (root / "10_Tracks" / "T" / "practice").mkdir(parents=True)
    (root / "10_Tracks" / "T" / "practice" / "Concept_Map.md").write_text(CONCEPT_MAP, encoding="utf-8")
    (root / "30_Maps").mkdir()
    (root / "30_Maps" / "Track.canvas").write_text(json.dumps(CANVAS), encoding="utf-8")
    ledger = root / "Attempts.jsonl"

    # Alpha was never tested: Beta has a gap.
    ledger.write_text("", encoding="utf-8")
    out = run(root, "--json")
    assert out.returncode == 0, out.stderr
    report = json.loads(out.stdout)
    rows = {row["concept"]: row for row in report["concepts"]}
    assert rows["Beta"]["prerequisites"] == ["Alpha"], rows["Beta"]
    assert rows["Beta"]["ready"] is False, rows["Beta"]
    assert rows["Beta"]["gaps"][0]["state"] == "never studied", rows["Beta"]

    # Alpha was tested and right: Beta is ready.
    ledger.write_text(json.dumps(event(event_id="a1")) + "\n", encoding="utf-8")
    ready = json.loads(run(root, "--json").stdout)
    rows = {row["concept"]: row for row in ready["concepts"]}
    assert rows["Beta"]["ready"] is True, rows["Beta"]
    assert rows["Beta"]["gaps"] == [], rows["Beta"]

    # Alpha was tested and wrong: the gap is back.
    ledger.write_text(json.dumps(event(event_id="a2", first_attempt_correct=False)) + "\n", encoding="utf-8")
    wrong = json.loads(run(root, "--json").stdout)
    rows = {row["concept"]: row for row in wrong["concepts"]}
    assert rows["Beta"]["ready"] is False, rows["Beta"]
    assert rows["Beta"]["gaps"][0]["state"] == "last attempt was wrong", rows["Beta"]

    # Only one concept can be checked at a time.
    only = json.loads(run(root, "--json", "--target", "Beta").stdout)
    assert [row["concept"] for row in only["concepts"]] == ["Beta"], only["concepts"]

    text = run(root)
    assert "Prerequisite check" in text.stdout, text.stdout
    assert "needs Alpha" in text.stdout, text.stdout
print("ok: 12 checks")
