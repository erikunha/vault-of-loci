"""Say how well the learner's confidence tracks the result, from the learning ledger.

The ledger is `50_Review/Attempts.jsonl`, written by `record_attempt.py`. This script only reads
it. It reports the Brier score with an explicit probability, the Brier score with the 1 to 5
scale, the reliability table and the sharpest cases: the attempts where the learner was sure and
wrong, and the attempts where the learner was unsure and right.

The numbers cover the attempts the other reports cover: a first attempt, without help, graded by
the learner. This is the gap between how sure the learner was and what happened. It does not
measure what was learned.

Usage: python3 -I 90_System/Scripts/calibration_coach.py [--ledger PATH] [--objective ID]
       [--bins 5] [--json]
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from calibration import (  # noqa: E402
    CONFIDENT_AT,
    DEFAULT_BINS,
    UNSURE_AT,
    coach_report,
)
from learning_ledger import LEDGER, read_ledger  # noqa: E402


def parse_bins(value):
    """The number of bins of the reliability table, as an int of 1 or more."""
    try:
        bins = int(value)
    except (TypeError, ValueError):
        raise ValueError(f"bins must be a whole number of 1 or more: {value!r}")
    if bins < 1:
        raise ValueError(f"bins must be 1 or more: {value!r}")
    return bins


def parse_args(argv):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--ledger", type=Path, default=LEDGER, help="path of the ledger")
    ap.add_argument("--objective", help="report only this objective")
    ap.add_argument("--bins", default=str(DEFAULT_BINS), help="number of bins of the reliability table")
    ap.add_argument("--json", dest="as_json", action="store_true", help="print the report as JSON")
    return ap.parse_args(argv)


def percent(rate):
    return "no attempt" if rate is None else f"{round(rate * 100)}%"


def score_line(label, score, count):
    """One Brier score as a line, or the reason there is none."""
    if score is None:
        return f"  {label}: no attempt with this kind of confidence yet"
    return f"  {label}: {score} (n={count}, lower is better)"


def section_lines(title, numbers):
    """The numbers of one group of attempts, as lines."""
    out = [title]
    out.append(score_line("Brier score with an explicit probability",
                          numbers["brier_explicit"], numbers["n_explicit"]))
    out.append(score_line("Brier score with the 1 to 5 scale",
                          numbers["brier_ordinal"], numbers["n_ordinal"]))
    if numbers["brier_ordinal"] is not None:
        out.append(f"    the 1 to 5 scale was mapped to a probability by {numbers['scale_ordinal']}, "
                   f"so this is an approximation of an ordinal scale")
    out.append("")
    out.append(f"  Reliability, {len(numbers['reliability'])} bins")
    out.append("    bin          attempts    right    share right")
    for row in numbers["reliability"]:
        out.append(f"    {row['range']}".ljust(24)
                   + f"{row['attempts']:>7}".ljust(14)
                   + f"{row['correct']:>6}".ljust(11)
                   + percent(row["rate"]))
    out.append("    a bin with only a few attempts means nothing")
    out.append("")
    out.append(f"  Sure and wrong (probability {CONFIDENT_AT} or more)")
    if numbers["confident_and_wrong"]:
        for case in numbers["confident_and_wrong"]:
            out.append(f"    {case['occurred_at']}  {case['objective_id']}  {case['item_id']}"
                       f"  probability {case['probability']:.2f}  wrong")
    else:
        out.append("    none")
    out.append("")
    out.append(f"  Unsure and right (probability {UNSURE_AT} or less)")
    if numbers["unsure_and_right"]:
        for case in numbers["unsure_and_right"]:
            out.append(f"    {case['occurred_at']}  {case['objective_id']}  {case['item_id']}"
                       f"  probability {case['probability']:.2f}  right")
    else:
        out.append("    none")
    return out


def lines(report, problems, objective=None):
    """The report as text."""
    out = []
    out.append("Calibration coach")
    out.append(f"generated: {report['generated']}")
    if objective:
        out.append(f"objective: {objective}")
    out.append(f"attempts counted: {report['attempts']}   ({report['population']})")
    if problems:
        out.append("")
        out.append("Ledger lines that could not be read:")
        for problem in problems:
            out.append(f"  - {problem}")
    if not report["attempts"]:
        out.append("")
        out.append("no attempt counted yet. Run record_attempt.py after a graded attempt.")
        return out
    out.append("")
    out.append("This measures the gap between how sure the learner was and what happened.")
    out.append("It does not measure what was learned.")
    out.append("")
    if objective:
        out.extend(section_lines(f"Objective {objective}", report["overall"]))
    else:
        out.extend(section_lines("Overall", report["overall"]))
        for name, numbers in report["objectives"].items():
            out.append("")
            out.extend(section_lines(f"Objective {name}", numbers))
    excluded = report["excluded"]
    out.append("")
    out.append("Not counted in the numbers above")
    out.append(f"  {excluded['help']} attempt(s) with help")
    out.append(f"  {excluded['agent_graded']} attempt(s) graded by an agent")
    out.append(f"  {excluded['not_graded']} attempt(s) not graded")
    return out


def main(argv=None):
    args = parse_args(argv)
    try:
        bins = parse_bins(args.bins)
    except ValueError as error:
        print("invalid bins:", error)
        return 1
    events, problems = read_ledger(args.ledger)
    if args.objective:
        events = [event for event in events if str(event.get("objective_id")) == args.objective]
    report = coach_report(events, bins, args.objective, args.ledger)
    if args.as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    for line in lines(report, problems, args.objective):
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
