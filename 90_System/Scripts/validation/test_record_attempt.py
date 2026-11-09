"""Test for record_attempt.py: it appends one valid line to the ledger and refuses a bad one."""
import json
import subprocess
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "record_attempt.py"
YESTERDAY = (date.today() - timedelta(days=1)).isoformat()
TOMORROW = (date.today() + timedelta(days=1)).isoformat()

OBJECTIVES = {
    "version": "v1",
    "objectives": [
        {"id": "retrieval-practice-recall", "concept": "Retrieval_Practice", "mode": "recall",
         "criterion": "State the one week result.", "rubric_version": "v1"}
    ],
}


def run(root, *flags):
    """Run the script against a temporary ledger and objective registry."""
    return subprocess.run(
        [sys.executable, "-I", str(SCRIPT), "--ledger", str(root / "Attempts.jsonl"),
         "--objectives", str(root / "Objectives.json"), *flags],
        capture_output=True, text=True)


with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    (root / "Objectives.json").write_text(json.dumps(OBJECTIVES), encoding="utf-8")
    ledger = root / "Attempts.jsonl"

    ok = run(root, "--objective", "retrieval-practice-recall", "--item", "item-01",
             "--mode", "recall", "--correct", "--at", YESTERDAY, "--confidence", "4")
    assert ok.returncode == 0, ok.stdout + ok.stderr
    assert "recorded" in ok.stdout, ok.stdout
    lines = ledger.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1, "one line is appended: " + ok.stdout
    event = json.loads(lines[0])
    assert event["objective_id"] == "retrieval-practice-recall", event
    assert event["first_attempt_correct"] is True, event
    assert event["assistance"] == "none", event
    assert event["grading_method"] == "learner_confirmed", event
    assert event["confidence"] == 4, event
    assert event["event_id"], "the event gets an id: " + ok.stdout

    unknown = run(root, "--objective", "not-in-the-registry", "--item", "item-02",
                  "--mode", "recall", "--correct", "--at", YESTERDAY)
    assert unknown.returncode == 1, "an unknown objective is refused: " + unknown.stdout
    assert "objective registry" in unknown.stdout, unknown.stdout
    assert len(ledger.read_text(encoding="utf-8").splitlines()) == 1, "a refused attempt writes nothing"

    allowed = run(root, "--objective", "not-in-the-registry", "--item", "item-02",
                  "--mode", "recall", "--correct", "--at", YESTERDAY, "--allow-unknown-objective")
    assert allowed.returncode == 0, allowed.stdout + allowed.stderr

    ungraded = run(root, "--objective", "retrieval-practice-recall", "--item", "item-03",
                   "--mode", "recall", "--at", YESTERDAY)
    assert ungraded.returncode == 1, "a graded mode needs a verdict: " + ungraded.stdout
    assert "--correct or --incorrect" in ungraded.stdout, ungraded.stdout

    study = run(root, "--objective", "retrieval-practice-recall", "--item", "item-04",
                "--mode", "study", "--at", YESTERDAY)
    assert study.returncode == 0, study.stdout + study.stderr
    assert json.loads(ledger.read_text(encoding="utf-8").splitlines()[-1])["first_attempt_correct"] is None

    graded_study = run(root, "--objective", "retrieval-practice-recall", "--item", "item-05",
                       "--mode", "study", "--correct", "--at", YESTERDAY)
    assert graded_study.returncode == 1, "a study event is not graded: " + graded_study.stdout

    contradiction = run(root, "--objective", "retrieval-practice-recall", "--item", "item-06",
                        "--mode", "recall", "--correct", "--hints", "2", "--at", YESTERDAY)
    assert contradiction.returncode == 1, "hints with no assistance is refused: " + contradiction.stdout
    assert "contradiction" in contradiction.stdout, contradiction.stdout

    future = run(root, "--objective", "retrieval-practice-recall", "--item", "item-07",
                 "--mode", "recall", "--correct", "--at", TOMORROW)
    assert future.returncode == 1, "an attempt in the future is refused: " + future.stdout

    duplicate = run(root, "--objective", "retrieval-practice-recall", "--item", "item-01",
                    "--mode", "recall", "--correct", "--at", YESTERDAY, "--event-id", event["event_id"])
    assert duplicate.returncode == 1, "the same event id twice is refused: " + duplicate.stdout
    assert "already in the ledger" in duplicate.stdout, duplicate.stdout

    bad_confidence = run(root, "--objective", "retrieval-practice-recall", "--item", "item-08",
                         "--mode", "recall", "--correct", "--at", YESTERDAY, "--confidence", "6")
    assert bad_confidence.returncode == 1, "confidence outside 1 to 5 is refused: " + bad_confidence.stdout

    bad_probability = run(root, "--objective", "retrieval-practice-recall", "--item", "item-09",
                          "--mode", "recall", "--correct", "--at", YESTERDAY, "--probability", "1.5")
    assert bad_probability.returncode == 1, "a probability outside 0 to 1 is refused: " + bad_probability.stdout

    both = run(root, "--objective", "retrieval-practice-recall", "--item", "item-10",
               "--mode", "recall", "--correct", "--incorrect", "--at", YESTERDAY)
    assert both.returncode == 1, "two verdicts at once is refused: " + both.stdout

    counted = len(ledger.read_text(encoding="utf-8").splitlines())
    assert counted == 3, f"only the three valid attempts were written, found {counted}"
print("ok: 13 checks")
