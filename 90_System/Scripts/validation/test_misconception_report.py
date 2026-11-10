"""Test for misconception_report.py: the recurring confusions and the open mistakes that name them."""
import json
import subprocess
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "misconception_report.py"
TODAY = date.today()


def days_ago(days):
    return (TODAY - timedelta(days=days)).isoformat()


def event(**fields):
    base = {
        "event_id": "attempt-test",
        "objective_id": "retrieval-practice-recall",
        "item_id": "item-a",
        "occurred_at": days_ago(1),
        "mode": "recall",
        "first_attempt_correct": False,
        "confidence": 2,
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


MISTAKES = """---
type: review
tags: [type/review, flashcards]
---

# Mistakes

## Mistake log

2026-11-01, [[Retrieval_Practice|Retrieval practice]]: I answered that rereading wins. The answer is that testing wins after a week. I went wrong because I mixed the five minute result with the week result. Kind: reasoning. AI: none. Open.
2026-10-20, [[Retrieval_Practice|Retrieval practice]]: I answered that the agent should answer. The answer is that the agent asks first. Kind: knowledge. AI: scaffold. Open.
2026-10-01, [[Retrieval_Practice|Retrieval practice]]: I answered wrong again. Kind: knowledge. AI: none. closed 2026-10-10.
"""


def run(root, *flags):
    return subprocess.run([sys.executable, "-I", str(SCRIPT), "--ledger", str(root / "Attempts.jsonl"),
                           "--mistakes", str(root / "Mistakes.md"), *flags],
                          capture_output=True, text=True)


with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    (root / "Mistakes.md").write_text(MISTAKES, encoding="utf-8")
    ledger = root / "Attempts.jsonl"
    events = [
        event(event_id="w1", occurred_at=days_ago(20)),
        event(event_id="w2", occurred_at=days_ago(3)),
        # A different objective, wrong only once: noise, not a confusion.
        event(event_id="w3", objective_id="other-objective", occurred_at=days_ago(4)),
        # An attempt with help still counts as a wrong answer.
        event(event_id="w4", objective_id="retrieval-practice-recall", occurred_at=days_ago(2),
              assistance="hint", hints_used=1),
    ]
    ledger.write_text("".join(json.dumps(item) + "\n" for item in events), encoding="utf-8")

    out = run(root, "--json")
    assert out.returncode == 0, out.stderr
    report = json.loads(out.stdout)
    rows = report["confusions"]
    assert len(rows) == 1, rows
    row = rows[0]
    assert row["objective_id"] == "retrieval-practice-recall", row
    assert row["wrong"] == 3, row
    assert row["wrong_with_help"] == 1, row
    assert len(row["open_mistakes"]) == 2, row
    assert report["open_mistakes"] == 2, report

    # One wrong attempt is noise.
    ledger.write_text(json.dumps(events[2]) + "\n", encoding="utf-8")
    quiet = json.loads(run(root, "--json").stdout)
    assert not quiet["confusions"], quiet

    text = run(root)
    assert "Misconception report" in text.stdout, text.stdout
    assert "open mistakes in the log: 2" in text.stdout, text.stdout

    ledger.write_text("".join(json.dumps(item) + "\n" for item in events), encoding="utf-8")
    listed = run(root)
    assert "retrieval-practice-recall" in listed.stdout, listed.stdout
    assert "two items that look alike" in listed.stdout, listed.stdout

    # An attempt the agent graded is not the learner's mistake, so it does not count.
    graded = [event(event_id="g1", grading_method="agent_graded"),
              event(event_id="g2", grading_method="agent_graded", occurred_at=days_ago(2))]
    ledger.write_text("".join(json.dumps(item) + "\n" for item in graded), encoding="utf-8")
    only_graded = json.loads(run(root, "--json").stdout)
    assert not only_graded["confusions"], only_graded

    # A line that could not be read is reported, not dropped in silence.
    ledger.write_text("{not json\n" + json.dumps(events[0]) + "\n", encoding="utf-8")
    corrupt = json.loads(run(root, "--json").stdout)
    assert corrupt["problems"], corrupt
    assert "not valid JSON" in corrupt["problems"][0], corrupt["problems"]

    # A mistakes note that is not there is a problem, not a log with no open mistake.
    missing_note = root / "No_Mistakes.md"
    ledger.write_text(json.dumps(events[0]) + "\n", encoding="utf-8")
    absent = subprocess.run([sys.executable, "-I", str(SCRIPT), "--ledger", str(ledger),
                              "--mistakes", str(missing_note), "--json"],
                             capture_output=True, text=True)
    assert absent.returncode == 0, absent.stderr
    absent_report = json.loads(absent.stdout)
    assert absent_report["problems"], absent_report
    assert "mistakes note" in absent_report["problems"][0], absent_report["problems"]
print("ok: 18 checks")
