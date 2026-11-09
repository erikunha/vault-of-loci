"""Audit the learning ledger: which objectives owe a delayed attempt, and which were never tested.

The audit reads the ledger and says what is missing. It never grades and never writes. The
delayed attempt itself is made by the learner and the agent, and the result goes back into the
ledger with `record_attempt.py`.

The horizons are 7, 30 and 90 days by default, counted from the day the objective was first
studied. An objective that passed a horizon without an attempt without help is due: the delay
has arrived and nothing was measured there.

Usage: python3 -I 90_System/Scripts/retention_audit.py [--ledger PATH] [--horizons 7,30,90]
       [--json] [--plan]
"""
import argparse
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from audit import audit, delayed_plan  # noqa: E402
from learning_ledger import HORIZONS, LEDGER, read_ledger  # noqa: E402


def parse_horizons(value):
    """The horizons to audit, as a list of days."""
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
    ap.add_argument("--plan", action="store_true", help="print only what is due")
    ap.add_argument("--json", dest="as_json", action="store_true", help="print the audit as JSON")
    return ap.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    try:
        horizons = parse_horizons(args.horizons)
    except ValueError as error:
        print("invalid horizons:", error)
        return 1
    events, problems = read_ledger(args.ledger)
    report = audit(events, horizons, date.today())
    plan_rows = delayed_plan(events, horizons, date.today())
    if args.as_json:
        print(json.dumps({"audit": report, "plan": plan_rows}, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    print(f"Retention audit for {date.today().isoformat()}")
    print(f"horizons: {', '.join(str(h) for h in horizons)} days")
    if problems:
        print()
        print("Ledger lines that could not be read:")
        for problem in problems:
            print(f"  - {problem}")
    if not report["objectives"]:
        print()
        print("the ledger is empty: nothing has been studied yet.")
        return 0
    print()
    print("objective                       attempts  clean  last attempt        status")
    for row in report["objectives"]:
        print(f"{row['objective_id']:<30} {row['attempts']:>8} {row['clean_attempts']:>6}  "
              f"{str(row['last_attempt'] or 'never'):<19} {row['status']}")
    if report["untested"]:
        print()
        print("Never measured without help:")
        for row in report["untested"]:
            print(f"  - {row['objective_id']} ({row['status']})")
    if plan_rows:
        print()
        print("Due now: a delayed attempt is missing")
        for row in plan_rows:
            print(f"  - {row['objective_id']} at {row['horizon']} days, first seen {row['first_seen']}. "
                  f"item id for the new task: {row['example_item']}")
        print()
        print("A delayed attempt needs a task the learner has not seen, written from the objective.")
    else:
        print()
        print("Nothing is due: every objective that could be measured was measured.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
