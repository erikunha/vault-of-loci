"""Print the transfer lab: the objectives that were studied and never applied in a new task.

The lab does not write the task. It says which objective owes one, what the task must ask, with
which criterion and which item id, so that the task is new and the record keeps the same id
every time.

Usage: python3 -I 90_System/Scripts/transfer_lab.py [--ledger PATH] [--objectives PATH]
       [--limit N] [--json]
"""
import argparse
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from learning_ledger import LEDGER, OBJECTIVES, load_objectives, problem_lines, read_ledger  # noqa: E402
from transfer import transfer_plan, transfer_status  # noqa: E402


def parse_args(argv):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--ledger", type=Path, default=LEDGER, help="path of the ledger")
    ap.add_argument("--objectives", type=Path, default=OBJECTIVES, help="path of the objective registry")
    ap.add_argument("--limit", type=int, help="how many tasks to show")
    ap.add_argument("--json", dest="as_json", action="store_true", help="print the plan as JSON")
    return ap.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    events, problems = read_ledger(args.ledger)
    objectives = load_objectives(args.objectives)
    status = transfer_status(events, objectives, date.today())
    plan = transfer_plan(events, objectives, date.today(), args.limit)
    if args.as_json:
        print(json.dumps({"status": status, "plan": plan, "problems": problems},
                         ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    print("Transfer lab")
    for line in problem_lines(problems):
        print(line)
    if not status:
        print("no objective has been studied yet.")
        return 0
    print()
    print("objective                       applied  last transfer")
    for row in status:
        print(f"{row['objective_id']:<30} {row['transfer_attempts']:>7}  {row['last_transfer'] or 'never'}")
    if not plan:
        print()
        print("every studied objective has been applied in a task at least once.")
        return 0
    print()
    print("Tasks to write")
    for row in plan:
        print()
        print(f"  objective: {row['objective_id']}")
        print(f"  concept: {row['concept'] or 'not in the registry'}")
        print(f"  criterion: {row['criterion'] or 'not in the registry'}")
        print(f"  item id: {row['item_id']}")
        print(f"  mode: {row['mode']}")
        print("  rubric:")
        for key in ("2", "1", "0"):
            print(f"    {key}: {row['rubric'][key]}")
    print()
    print("A transfer task needs a case the learner has not seen, and the criterion decides what counts.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
