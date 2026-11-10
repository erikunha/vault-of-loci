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
    assert rows["Beta"]["gaps"][0]["state"] == "mistake not recovered", rows["Beta"]

    # Only one concept can be checked at a time.
    only = json.loads(run(root, "--json", "--target", "Beta").stdout)
    assert [row["concept"] for row in only["concepts"]] == ["Beta"], only["concepts"]

    text = run(root)
    assert "Prerequisite check" in text.stdout, text.stdout
    assert "needs Alpha" in text.stdout, text.stdout

    # A prerequisite that was studied but never attempted was graded by nobody, so it cannot be
    # called "only graded by the agent". The label is "never tested".
    ledger.write_text(json.dumps(event(event_id="s1", mode="study", first_attempt_correct=None,
                                       confidence=None)) + "\n", encoding="utf-8")
    studied = json.loads(run(root, "--json").stdout)
    rows = {row["concept"]: row for row in studied["concepts"]}
    assert rows["Beta"]["gaps"][0]["state"] == "never tested", rows["Beta"]

    # An attempt the agent graded is not the same as an attempt made with help, and the next step
    # is not the same either: the learner has to confirm the attempt.
    ledger.write_text(json.dumps(event(event_id="g1", grading_method="agent_graded")) + "\n", encoding="utf-8")
    graded = json.loads(run(root, "--json").stdout)
    rows = {row["concept"]: row for row in graded["concepts"]}
    assert rows["Beta"]["gaps"][0]["state"] == "only graded by the agent", rows["Beta"]

    ledger.write_text(json.dumps(event(event_id="h1", assistance="hint", hints_used=1,
                                       first_attempt_correct=False)) + "\n", encoding="utf-8")
    helped = json.loads(run(root, "--json").stdout)
    rows = {row["concept"]: row for row in helped["concepts"]}
    assert rows["Beta"]["gaps"][0]["state"] == "only tested with help", rows["Beta"]

    # The printed next step is different for each of the two reasons nothing counts.
    helped_text = run(root).stdout
    ledger.write_text(json.dumps(event(event_id="g2", grading_method="agent_graded")) + "\n", encoding="utf-8")
    graded_text = run(root).stdout
    assert "attempt the same task again, without help" in helped_text, helped_text
    assert "the learner has to confirm the attempt" not in helped_text, helped_text
    assert "the learner has to confirm the attempt" in graded_text, graded_text
    assert "attempt the same task again, without help" not in graded_text, graded_text

    # A concept named with spaces in the registry is the same concept as the one the map names
    # with underscores, so a clean attempt is not reported as "never studied".
    spaced_registry = root / "Objectives.json"
    registry = json.loads(spaced_registry.read_text(encoding="utf-8"))
    registry["objectives"][0]["concept"] = "Alpha Practice"
    spaced_registry.write_text(json.dumps(registry), encoding="utf-8")
    underscored = root / "10_Tracks" / "T" / "practice" / "Concept_Map.md"
    underscored.write_text(CONCEPT_MAP.replace("Alpha", "Alpha_Practice"), encoding="utf-8")
    # The canvas names the same concept, so the two sources declare one prerequisite and not two.
    canvas = root / "30_Maps" / "Track.canvas"
    spaced_canvas = json.loads(canvas.read_text(encoding="utf-8"))
    spaced_canvas["nodes"][0]["file"] = "20_Concepts/Alpha_Practice.md"
    canvas.write_text(json.dumps(spaced_canvas), encoding="utf-8")
    (root / "20_Concepts" / "Alpha_Practice.md").write_text("# Alpha Practice\n", encoding="utf-8")
    ledger.write_text(json.dumps(event(event_id="a3")) + "\n", encoding="utf-8")
    named = json.loads(run(root, "--json").stdout)
    rows = {row["concept"]: row for row in named["concepts"]}
    assert rows["Beta"]["prerequisites"] == ["Alpha_Practice"], rows["Beta"]
    assert rows["Beta"]["ready"] is True, rows["Beta"]
    assert rows["Beta"]["gaps"] == [], rows["Beta"]
    spaced_registry.write_text(json.dumps(OBJECTIVES), encoding="utf-8")
    underscored.write_text(CONCEPT_MAP, encoding="utf-8")
    canvas.write_text(json.dumps(CANVAS), encoding="utf-8")
    (root / "20_Concepts" / "Alpha_Practice.md").unlink()

    # The order column does not have to hold a number for the map to be read.
    letters = root / "10_Tracks" / "T" / "practice" / "Concept_Map.md"
    letters.write_text(CONCEPT_MAP.replace("| 1 |", "| A |").replace("| 2 |", "| B |"), encoding="utf-8")
    ordered = json.loads(run(root, "--json").stdout)
    rows = {row["concept"]: row for row in ordered["concepts"]}
    assert rows["Beta"]["prerequisites"] == ["Alpha"], rows["Beta"]

    # A target that no concept carries is said so, instead of saying the vault has no map.
    unmatched = run(root, "--target", "Nothing")
    assert "no concept named 'Nothing'" in unmatched.stdout, unmatched.stdout

    # The map and the canvas spell the same concept differently, one with a space and one with
    # an underscore. It is one concept, in one row, with the prerequisites of both sources, not
    # two half-informed rows.
    canvas = root / "30_Maps" / "Track.canvas"
    spelled = json.loads(json.dumps(CANVAS))
    spelled["nodes"][1]["file"] = "20_Concepts/Beta_Practice.md"
    canvas.write_text(json.dumps(spelled), encoding="utf-8")
    (root / "20_Concepts" / "Beta_Practice.md").write_text("# Beta Practice\n", encoding="utf-8")
    underscored.write_text(CONCEPT_MAP.replace("[[Beta\\|Beta]]", "[[Beta Practice\\|Beta Practice]]"),
                           encoding="utf-8")
    merged = json.loads(run(root, "--json").stdout)
    rows = {row["concept"]: row for row in merged["concepts"]}
    assert len(merged["concepts"]) == 1, merged["concepts"]
    assert rows["Beta Practice"]["prerequisites"] == ["Alpha"], rows["Beta Practice"]
    assert rows["Beta Practice"]["ready"] is True, rows["Beta Practice"]
    underscored.write_text(CONCEPT_MAP, encoding="utf-8")
    canvas.write_text(json.dumps(CANVAS), encoding="utf-8")
    (root / "20_Concepts" / "Beta_Practice.md").unlink()

    # A line that could not be read is reported, not dropped in silence.
    ledger.write_text("{not json\n" + json.dumps(event(event_id="a4")) + "\n", encoding="utf-8")
    corrupt = json.loads(run(root, "--json").stdout)
    assert corrupt["problems"], corrupt
    assert "not valid JSON" in corrupt["problems"][0], corrupt["problems"]
print("ok: 22 checks")
