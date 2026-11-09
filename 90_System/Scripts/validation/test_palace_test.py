"""Test for palace_test.py: the route of a memory palace and the ids the ledger uses."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "palace_test.py"

NOTE = """---
type: review
tags: [type/review]
---

# Home route

| Place | Item | Source |
|---|---|---|
| Front door | First step | [[Source_One]] |
| Kitchen | Second step | [[Source_Two]] |
| Garden | Third step | |
| Garage | Fourth step | [[Source_Four]] |
"""

EMPTY_NOTE = """---
type: review
tags: [type/review]
---

# Empty route

| Place | Item | Source |
|---|---|---|
"""


def run(note, *flags):
    return subprocess.run([sys.executable, "-I", str(SCRIPT), "--palace", str(note), *flags],
                          capture_output=True, text=True)


with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    note = root / "Home_Route.md"
    note.write_text(NOTE, encoding="utf-8")
    empty = root / "Empty_Route.md"
    empty.write_text(EMPTY_NOTE, encoding="utf-8")
    ledger = root / "Attempts.jsonl"
    ledger.write_text("", encoding="utf-8")

    # The route keeps the order of the table.
    out = run(note, "--ledger", str(ledger))
    assert out.returncode == 0, out.stderr
    text = out.stdout
    assert "Front door" in text, text
    positions = [text.index("Front door"), text.index("Kitchen"), text.index("Garden"),
                 text.index("Garage")]
    assert positions == sorted(positions), positions

    # The item is not printed, the learner has to recall it.
    assert "First step" not in text, text
    assert "Second step" not in text, text

    # The item comes only when the agent asks for it.
    revealed = run(note, "--with-items", "--ledger", str(ledger))
    assert revealed.returncode == 0, revealed.stderr
    assert "First step" in revealed.stdout, revealed.stdout

    # The cap keeps only the first places of the route.
    capped = run(note, "--places", "2", "--ledger", str(ledger))
    assert capped.returncode == 0, capped.stderr
    assert "Front door" in capped.stdout, capped.stdout
    assert "Kitchen" in capped.stdout, capped.stdout
    assert "Garden" not in capped.stdout, capped.stdout
    assert "Garage" not in capped.stdout, capped.stdout

    # The start moves the walk along the route.
    started = run(note, "--start", "3", "--ledger", str(ledger))
    assert started.returncode == 0, started.stderr
    assert "Front door" not in started.stdout, started.stdout
    assert "Kitchen" not in started.stdout, started.stdout
    assert "Garden" in started.stdout, started.stdout
    assert "Garage" in started.stdout, started.stdout

    # The start and the cap work together.
    both = run(note, "--start", "2", "--places", "2", "--ledger", str(ledger))
    assert both.returncode == 0, both.stderr
    assert "Kitchen" in both.stdout, both.stdout
    assert "Garden" in both.stdout, both.stdout
    assert "Garage" not in both.stdout, both.stdout

    # The JSON output carries the ids.
    report = json.loads(run(note, "--ledger", str(ledger), "--json").stdout)
    assert report["palace"] == "home-route", report
    assert report["objective_id"] == "palace-home-route", report
    assert report["total_places"] == 4, report
    assert len(report["places"]) == 4, report
    assert [row["place"] for row in report["places"]] == ["Front door", "Kitchen", "Garden",
                                                          "Garage"], report
    for row in report["places"]:
        assert row["item_id"] == f"palace-home-route-{row['number']}", row
    assert report["places"][0]["item_id"] == "palace-home-route-1", report
    assert "item" not in report["places"][0], report

    # The JSON output carries the item only when the agent asks for it.
    with_items = json.loads(run(note, "--with-items", "--ledger", str(ledger), "--json").stdout)
    assert with_items["places"][0]["item"] == "First step", with_items

    # The JSON output keeps the order and the cap.
    small = json.loads(run(note, "--places", "1", "--ledger", str(ledger), "--json").stdout)
    assert small["shown"] == 1, small
    assert small["places"][0]["place"] == "Front door", small
    assert small["total_places"] == 4, small

    # The JSON output starts where the walk starts.
    later = json.loads(run(note, "--start", "3", "--ledger", str(ledger), "--json").stdout)
    assert later["places"][0]["number"] == 3, later
    assert later["places"][0]["item_id"] == "palace-home-route-3", later

    # A palace with an empty table has no places and says so.
    blank = run(empty, "--ledger", str(ledger))
    assert blank.returncode == 0, blank.stderr
    assert "no places yet" in blank.stdout, blank.stdout
    blank_json = json.loads(run(empty, "--ledger", str(ledger), "--json").stdout)
    assert blank_json["total_places"] == 0, blank_json
    assert blank_json["places"] == [], blank_json
    assert blank_json["objective_id"] == "palace-empty-route", blank_json

    # The ledger counts the attempts of each place.
    events = [
        {"event_id": "a1", "objective_id": "palace-home-route", "item_id": "palace-home-route-1",
         "occurred_at": "2026-11-01T10:00:00-03:00", "mode": "recall", "first_attempt_correct": True,
         "confidence": 4, "confidence_probability": None, "hints_used": 0, "assistance": "none",
         "rubric_version": "v1", "grading_method": "learner_confirmed", "source_revision": None,
         "duration_minutes": 3},
        {"event_id": "a2", "objective_id": "palace-home-route", "item_id": "palace-home-route-1",
         "occurred_at": "2026-11-02T10:00:00-03:00", "mode": "recall", "first_attempt_correct": False,
         "confidence": 2, "confidence_probability": None, "hints_used": 1, "assistance": "hint",
         "rubric_version": "v1", "grading_method": "learner_confirmed", "source_revision": None,
         "duration_minutes": 3},
    ]
    ledger.write_text("".join(json.dumps(event) + "\n" for event in events), encoding="utf-8")
    counted = json.loads(run(note, "--ledger", str(ledger), "--json").stdout)
    first = counted["places"][0]
    assert first["attempts"] == 2, first
    assert first["clean_attempts"] == 1, first
    assert counted["places"][1]["attempts"] == 0, counted["places"][1]

    # A note that is not there is reported, not a crash.
    missing = run(root / "No_Route.md", "--ledger", str(ledger))
    assert missing.returncode == 1, missing.stdout
    assert "palace not found" in missing.stdout, missing.stdout

print("ok: 13 checks")
