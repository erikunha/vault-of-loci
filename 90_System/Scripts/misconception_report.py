"""Print the recurring confusions in the ledger, and the exercises that would separate them.

A wrong answer once is noise. The same objective wrong again is a confusion, and repeating the
same card does not fix it: it needs two items that look alike, so the learner has to say which
one applies and why.

The report only lists. The skill proposes the exercise and the learner decides what goes into
`50_Review/Misconceptions.md`.

Usage: python3 -I 90_System/Scripts/misconception_report.py [--ledger PATH] [--mistakes PATH]
       [--min-wrong 2] [--json]
"""
import argparse
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from learning_ledger import LEDGER, problem_lines, read_ledger  # noqa: E402
from misconceptions import MISTAKES, confusions, open_mistakes  # noqa: E402


def parse_args(argv):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--ledger", type=Path, default=LEDGER, help="path of the ledger")
    ap.add_argument("--mistakes", type=Path, default=MISTAKES, help="path of the mistakes note")
    ap.add_argument("--min-wrong", type=int, default=2, help="how many wrong attempts make a confusion")
    ap.add_argument("--json", dest="as_json", action="store_true", help="print the report as JSON")
    return ap.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    events, problems = read_ledger(args.ledger)
    mistakes, note_problems = open_mistakes(args.mistakes)
    problems = problems + note_problems
    rows = confusions(events, mistakes, args.min_wrong, date.today())
    if args.as_json:
        print(json.dumps({"confusions": rows, "open_mistakes": len(mistakes),
                          "problems": problems},
                         ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    print("Misconception report")
    print(f"open mistakes in the log: {len(mistakes)}")
    for line in problem_lines(problems):
        print(line)
    if not rows:
        print("no objective was wrong more than once.")
        return 0
    print()
    for row in rows:
        print(f"{row['objective_id']}")
        print(f"  wrong {row['wrong']} time(s), {row['wrong_with_help']} with help, "
              f"last {row['last_wrong']} ({row['days_since']} days ago)")
        print(f"  items: {', '.join(row['items'])}")
        for mistake in row["open_mistakes"]:
            print(f"  open mistake from {mistake['date']}: kind {mistake['kind']}, AI {mistake['ai']}")
        print(f"  exercise: {row['exercise']}")
        print()
    print("A confusion is not fixed by repeating the same card. It needs two items that look alike.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
