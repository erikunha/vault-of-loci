"""Test for record_attempt.py: it appends one valid line to the ledger and refuses a bad one."""
import json
import subprocess
import sys
import tempfile
from datetime import date, datetime, timedelta
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "record_attempt.py"
# The ledger schema asks for an ISO 8601 timestamp with an offset, so the test uses one.
OFFSET = datetime.now().astimezone().strftime("%z")
OFFSET = OFFSET[:3] + ":" + OFFSET[3:]
YESTERDAY = f"{(date.today() - timedelta(days=1)).isoformat()}T10:00:00{OFFSET}"
TOMORROW = f"{(date.today() + timedelta(days=1)).isoformat()}T10:00:00{OFFSET}"
NO_OFFSET = (date.today() - timedelta(days=1)).isoformat() + "T10:00:00"

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

    # The schema asks for a timestamp with an offset, so one without it is refused.
    naive = run(root, "--objective", "retrieval-practice-recall", "--item", "item-08",
                "--mode", "recall", "--correct", "--at", NO_OFFSET)
    assert naive.returncode == 1, "a timestamp without an offset is refused: " + naive.stdout
    assert "with an offset" in naive.stdout, naive.stdout

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
    # A registry that cannot be read turns the check that the objective exists off, so the
    # attempt is refused instead of being recorded under a name that does not exist.
    missing = subprocess.run(
        [sys.executable, "-I", str(SCRIPT), "--ledger", str(root / "Attempts.jsonl"),
         "--objectives", str(root / "NoRegistry.json"), "--objective", "typo-not-real",
         "--item", "item-11", "--mode", "recall", "--correct", "--at", YESTERDAY],
        capture_output=True, text=True)
    assert missing.returncode == 1, missing.stdout + missing.stderr
    assert "objective registry could not be read" in missing.stdout, missing.stdout

    allowed = subprocess.run(
        [sys.executable, "-I", str(SCRIPT), "--ledger", str(root / "Attempts.jsonl"),
         "--objectives", str(root / "NoRegistry.json"), "--objective", "typo-not-real",
         "--item", "item-12", "--mode", "recall", "--correct", "--at", YESTERDAY,
         "--allow-unknown-objective"],
        capture_output=True, text=True)
    assert allowed.returncode == 0, allowed.stdout + allowed.stderr

print("ok: 15 checks")
