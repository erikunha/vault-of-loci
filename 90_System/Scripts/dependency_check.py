"""Print the prerequisite gaps: what has to be understood before what, and where the learner is.

The vault says what must come first, in the concept map of each track and in the edges of the
canvases. This script joins that map with the ledger and shows the gaps: a prerequisite that was
never tested without help, whose last attempt was wrong, or that has not been tested for a while.

Usage: python3 -I 90_System/Scripts/dependency_check.py [--target NAME] [--ledger PATH]
       [--root PATH] [--json]
"""
import argparse
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dependencies import VAULT, gap_report  # noqa: E402
from learning_ledger import LEDGER, OBJECTIVES, load_objectives, read_ledger  # noqa: E402


def parse_args(argv):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--target", help="check one concept, by name")
    ap.add_argument("--ledger", type=Path, default=LEDGER, help="path of the ledger")
    ap.add_argument("--root", type=Path, default=VAULT, help="path of the vault")
    ap.add_argument("--objectives", type=Path, default=OBJECTIVES, help="path of the objective registry")
    ap.add_argument("--json", dest="as_json", action="store_true", help="print the report as JSON")
    return ap.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    events, _ = read_ledger(args.ledger)
    rows = gap_report(events, args.root, args.target, load_objectives(args.objectives), date.today())
    if args.as_json:
        print(json.dumps({"concepts": rows}, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    print("Prerequisite check")
    if not rows:
        print("the vault has no concept map with prerequisites yet.")
        return 0
    print()
    for row in rows:
        state = "ready" if row["ready"] else "has a gap"
        print(f"{row['concept']} ({state})")
        for need in row["states"]:
            print(f"  needs {need['concept']}: {need['state']} ({need['clean']} clean attempt(s))")
        if row["gaps"]:
            print("  fix the gap before this concept")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
