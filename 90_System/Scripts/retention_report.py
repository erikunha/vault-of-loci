"""Report what the learning ledger shows: retention, transfer, calibration and what was learned.

The ledger is `50_Review/Attempts.jsonl`, written by `record_attempt.py`. This script only reads
it. A retention number at a horizon counts first attempts, without help, graded by the learner,
made that many days or more after the item was first seen. Transfer is the same, with an apply
or discriminate task instead of a recall.

A forecast is not a measurement, so nothing here predicts retention. Every number is what the
learner already did.

Usage: python3 -I 90_System/Scripts/retention_report.py [--ledger PATH] [--horizons 7,30,90]
       [--objective ID] [--json]
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from learning_ledger import (  # noqa: E402
    LEDGER,
    HORIZONS,
    by_objective,
    metrics,
    now_iso,
    read_ledger,
)


def parse_horizons(value):
    """The horizons to report, as a list of days."""
    try:
        horizons = sorted({int(part) for part in str(value).split(",") if part.strip()})
    except ValueError:
        raise ValueError(f"horizons must be days separated by commas, for example 7,30,90: {value!r}")
    if not horizons or horizons[0] < 0:
        raise ValueError("horizons must be 0 or more days")
    return horizons


def parse_args(argv):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--ledger", type=Path, default=LEDGER, help="path of the ledger")
    ap.add_argument("--horizons", default=",".join(str(h) for h in HORIZONS), help="days, for example 7,30,90")
    ap.add_argument("--objective", help="report only this objective")
    ap.add_argument("--json", dest="as_json", action="store_true", help="print the report as JSON")
    return ap.parse_args(argv)


def percent(rate):
    return "no eligible attempt" if rate is None else f"{round(rate * 100)}%"


def lines(report, events, problems, horizons, objective=None):
    """The report as text."""
    out = []
    out.append("Learning retention report")
    out.append(f"generated: {now_iso()}")
    if objective:
        out.append(f"objective: {objective}")
    out.append(f"attempts recorded: {report['attempts']}   items: {report['items']}   objectives: {len(report['objectives'])}")
    if problems:
        out.append("")
        out.append("Ledger lines that could not be read:")
        for problem in problems:
            out.append(f"  - {problem}")
    if not report["attempts"]:
        out.append("")
        out.append("no attempt recorded yet. Run record_attempt.py after a graded attempt.")
        return out
    out.append("")
    out.append("Retention: first attempt, no help, graded by the learner")
    out.append("  horizon    correct/eligible    rate")
    for horizon in horizons:
        row = report["retention"].get(str(horizon), {"correct": 0, "eligible": 0, "rate": None})
        out.append(f"  {horizon:>3} days    {row['correct']}/{row['eligible']}".ljust(42) + f"{percent(row['rate'])}")
    out.append("")
    out.append("Transfer: first attempt, no help, graded by the learner")
    out.append("  horizon    correct/eligible    rate")
    for horizon in horizons:
        row = report["transfer"].get(str(horizon), {"correct": 0, "eligible": 0, "rate": None})
        out.append(f"  {horizon:>3} days    {row['correct']}/{row['eligible']}".ljust(42) + f"{percent(row['rate'])}")
    calibration = report["calibration"]
    out.append("")
    out.append("Calibration")
    if calibration["brier_explicit"] is None:
        out.append("  Brier score with an explicit probability: no attempt with a probability yet")
    else:
        out.append(f"  Brier score with an explicit probability: {calibration['brier_explicit']} (n={calibration['n_explicit']}, lower is better)")
    if calibration["brier_ordinal"] is None:
        out.append("  Brier score with confidence 1 to 5: no attempt with a confidence yet")
    else:
        out.append(f"  Brier score with confidence 1 to 5: {calibration['brier_ordinal']} (n={calibration['n_ordinal']}, lower is better)")
        out.append(f"    the 1 to 5 scale was mapped to a probability by {calibration['scale_ordinal']}, so this is an approximation")
    out.append("")
    out.append("Learned: recalled twice on different days and used once in a new task")
    if report["learned"]:
        for name in report["learned"]:
            out.append(f"  {name}")
    else:
        out.append("  no objective meets the rule yet")
    excluded = report["excluded"]
    out.append("")
    out.append("Not counted in the metrics above")
    out.append(f"  {excluded['help']} attempt(s) with help")
    out.append(f"  {excluded['agent_graded']} attempt(s) graded by an agent")
    out.append(f"  {excluded['too_recent']} attempt(s) too recent for the shortest horizon")
    if report["inferred_exposure"]:
        out.append(f"  {report['inferred_exposure']} item(s) have no study event, so their first attempt set the exposure day")
    out.append("")
    out.append("A forecast is not a measurement, so no predicted retention is shown here.")
    return out


def main(argv=None):
    args = parse_args(argv)
    try:
        horizons = parse_horizons(args.horizons)
    except ValueError as error:
        print("invalid horizons:", error)
        return 1
    events, problems = read_ledger(args.ledger)
    if args.objective:
        events = [event for event in events if str(event.get("objective_id")) == args.objective]
    report = metrics(events, horizons)
    if args.as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    for line in lines(report, events, problems, horizons, args.objective):
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
