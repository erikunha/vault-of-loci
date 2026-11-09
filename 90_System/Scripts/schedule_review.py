"""Print the review plan for today, from the attempts in the learning ledger.

The plan comes from `scheduler.py`, which reads the ledger and ranks what is worth another try.
The number in the plan is a priority for the day, not a probability of remembering. A forecast
is not a measurement, and `retention_report.py` is where the measured numbers live.

The rules of the vault set the shape of the plan: a day is 10 to 20 reviews with about 2 new
cards, and when the queue is longer than the cap the oldest and weakest come first with no new
cards until the queue is under it.

Usage: python3 -I 90_System/Scripts/schedule_review.py [--ledger PATH] [--cap 15] [--new 2]
       [--objective ID] [--recovery] [--json]
"""
import argparse
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from learning_ledger import LEDGER, read_ledger  # noqa: E402
from scheduler import DAILY_CAP, NEW_PER_DAY, plan, recovery_plan  # noqa: E402


def parse_args(argv):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--ledger", type=Path, default=LEDGER, help="path of the ledger")
    ap.add_argument("--cap", type=int, default=DAILY_CAP, help="reviews per day (10 to 20)")
    ap.add_argument("--new", type=int, default=NEW_PER_DAY, help="new cards per day (about 2)")
    ap.add_argument("--objective", help="plan only this objective")
    ap.add_argument("--recovery", action="store_true", help="the diagnostic after a break")
    ap.add_argument("--json", dest="as_json", action="store_true", help="print the plan as JSON")
    return ap.parse_args(argv)


def describe(entry):
    """One line of the plan."""
    where = f"{entry['objective_id']} / {entry['item_id'] or 'new item'}"
    mode = entry["mode"] or "recall"
    return (f"{where:<52} {mode:<13} priority {entry['priority']:<6} "
            f"strength {entry['strength']:<6} {entry['why']}")


def main(argv=None):
    args = parse_args(argv)
    events, problems = read_ledger(args.ledger)
    if args.objective:
        events = [event for event in events if str(event.get("objective_id")) == args.objective]
    if args.recovery:
        recovery = recovery_plan(events, today=date.today())
        if recovery is None:
            print("no break to recover from: the last attempt is recent.")
            return 0
        if args.as_json:
            print(json.dumps(recovery, ensure_ascii=False, indent=2, sort_keys=True))
            return 0
        print(f"Recovery after {recovery['days_away']} days away")
        print(f"backlog: {recovery['backlog']} items, and this is not the whole queue")
        for number, entry in enumerate(recovery["entries"], start=1):
            print(f" {number}. {describe(entry)}")
        print(recovery["why"])
        return 0
    ranked = plan(events, cap=args.cap, new_per_day=args.new, today=date.today())
    if args.as_json:
        print(json.dumps(ranked, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    print(f"Review plan for {date.today().isoformat()}")
    print(f"backlog: {ranked['backlog']} items   cap: {ranked['cap']} reviews   "
          f"new per day: {ranked['new_per_day']}")
    away = ranked["days_since_last"]
    print("days since the last attempt: " + ("none yet" if away is None else str(away)))
    if ranked["catch_up"]:
        print("catch-up mode: the queue is over the cap, so no new cards until it is under it.")
    if not ranked["entries"]:
        print("nothing to review yet: the ledger has no attempt.")
        return 0
    print()
    for number, entry in enumerate(ranked["entries"], start=1):
        print(f" {number}. {describe(entry)}")
    print()
    print("The priority is a ranking for the day, not a probability of remembering.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
