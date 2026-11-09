"""Record one graded attempt in the learning ledger, the append-only history of what was learned.

The ledger is `50_Review/Attempts.jsonl`. This script appends one line and never edits an older
line, so the history of every attempt survives. The rules of a valid line live in
`learning_ledger.py`, and `retention_report.py` reads the same file to measure retention,
transfer and calibration.

An attempt is a first try at one item, with how many hints the learner took and how sure the
learner was. A study event records that the material was seen without grading it.

Usage: python3 -I 90_System/Scripts/record_attempt.py --objective ID --item ID --mode MODE
       [--correct | --incorrect] [--at ISO] [--confidence 1-5] [--probability 0-1]
       [--hints N] [--assistance LEVEL] [--grading METHOD] [--rubric VER] [--revision REV]
       [--minutes N] [--event-id ID] [--ledger PATH] [--objectives PATH]
       [--allow-unknown-objective] [--print]
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from learning_ledger import (  # noqa: E402
    LEDGER,
    OBJECTIVES,
    append_event,
    load_objectives,
    next_event_id,
    now_iso,
    read_ledger,
    validate_event,
)


def parse_args(argv):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--objective", required=True, help="id of the learning objective")
    ap.add_argument("--item", required=True, help="id of the question or task")
    ap.add_argument("--mode", required=True, help="study, recall, explain, apply or discriminate")
    ap.add_argument("--correct", action="store_true", help="the first attempt was right")
    ap.add_argument("--incorrect", action="store_true", help="the first attempt was wrong")
    ap.add_argument("--at", help="when it happened, ISO 8601 with an offset (default: now)")
    ap.add_argument("--confidence", type=int, help="how sure the learner was, from 1 to 5")
    ap.add_argument("--probability", type=float, help="chance of being right, from 0 to 1")
    ap.add_argument("--hints", type=int, default=0, help="how many hints the learner took")
    ap.add_argument("--assistance", default="none", help="none, hint, strong_hint, partial_example or answer")
    ap.add_argument("--grading", default="learner_confirmed", help="learner_confirmed or agent_graded")
    ap.add_argument("--rubric", default="v1", help="version of the rubric that graded the attempt")
    ap.add_argument("--revision", help="version of the material that was tested")
    ap.add_argument("--minutes", type=float, help="minutes spent on the attempt")
    ap.add_argument("--event-id", help="id of the line (default: built from today's date)")
    ap.add_argument("--ledger", type=Path, default=LEDGER, help="path of the ledger")
    ap.add_argument("--objectives", type=Path, default=OBJECTIVES, help="path of the objective registry")
    ap.add_argument("--allow-unknown-objective", action="store_true", help="do not check the registry")
    ap.add_argument("--print", dest="show", action="store_true", help="print the line as JSON")
    return ap.parse_args(argv)


def build_event(args, used_ids):
    """The event that the flags describe, or the reasons why there is none."""
    if args.correct and args.incorrect:
        return None, ["use --correct or --incorrect, not both"]
    graded = args.correct or args.incorrect
    event = {
        "event_id": args.event_id or next_event_id(used_ids),
        "objective_id": args.objective,
        "item_id": args.item,
        "occurred_at": args.at or now_iso(),
        "mode": args.mode,
        "first_attempt_correct": True if args.correct else (False if args.incorrect else None),
        "confidence": args.confidence,
        "confidence_probability": args.probability,
        "hints_used": args.hints,
        "assistance": args.assistance,
        "rubric_version": args.rubric,
        "grading_method": args.grading,
        "source_revision": args.revision,
        "duration_minutes": args.minutes,
    }
    if args.mode == "study":
        if graded:
            return None, ["a study event is not graded, so drop --correct and --incorrect"]
        event["first_attempt_correct"] = None
    elif not graded:
        return None, ["--correct or --incorrect is required for a graded mode"]
    return event, []


def main(argv=None):
    args = parse_args(argv)
    events, _ = read_ledger(args.ledger)
    used_ids = {event.get("event_id") for event in events}
    event, problems = build_event(args, used_ids)
    if event is None:
        for problem in problems:
            print("invalid attempt:", problem)
        return 1
    objectives = load_objectives(args.objectives)
    known = objectives or None
    problems = validate_event(event, known, used_ids, args.allow_unknown_objective)
    if problems:
        print("invalid attempt:")
        for problem in problems:
            print("  -", problem)
        return 1
    path = append_event(event, args.ledger)
    if args.show:
        print(json.dumps(event, ensure_ascii=False, sort_keys=True))
    verdict = "correct" if event["first_attempt_correct"] else ("wrong" if event["first_attempt_correct"] is False else "not graded")
    print(f"recorded {event['event_id']}  {event['objective_id']}  {event['item_id']}  {event['mode']}  {verdict}")
    print("ledger:", path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
