"""Compare how sure you were with how you did, per concept, and list what is going stale.

Reads `confidence` (1 to 5), `score` (0 to 100, percent right on the first try) and `last_tested`
from every concept note, as the learner logged them after a checkpoint. Confidence 1 to 5 maps to
an expected 20 to 100 percent. A gap of 30 points or more is reported as over- or underconfident.
Concepts not tested for `--days` days are stale; concepts with no test are untested. Thresholds are
defaults to adjust, not research results. It reads only and never sets a property.

Usage: python3 -I 90_System/Scripts/calibration_report.py [--root PATH] [--days 30] [--gap 30]
"""
import argparse
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vault_notes import notes  # noqa: E402


def number(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def report(root, days, gap_limit):
    lines, gaps = [], []
    for rel, front, _ in notes(root):
        if front.get("type") != "concept":
            continue
        name, conf, score = rel.stem, number(front.get("confidence")), number(front.get("score"))
        tested = front.get("last_tested") or ""
        if conf is not None and score is not None:
            gap = conf * 20 - score
            gaps.append(gap)
            if gap >= gap_limit:
                lines.append(f"overconfident: {name}  (confidence {conf:g}, score {score:g})")
            elif gap <= -gap_limit:
                lines.append(f"underconfident: {name}  (confidence {conf:g}, score {score:g})")
        if not tested:
            lines.append(f"untested: {name}")
        else:
            try:
                old = (date.today() - date.fromisoformat(str(tested)[:10])).days
            except ValueError:
                old = None
            if old is not None and old > days:
                lines.append(f"stale: {name}  (last tested {old} days ago)")
    if gaps:
        mean = sum(gaps) / len(gaps)
        lines.append(f"mean gap: {mean:+.0f} points over {len(gaps)} concepts (positive means overconfident)")
    return lines


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--gap", type=int, default=30)
    args = ap.parse_args()
    print("\n".join(report(args.root, args.days, args.gap)) or "no concept has a logged test yet")


if __name__ == "__main__":
    main()
