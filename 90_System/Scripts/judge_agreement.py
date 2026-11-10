"""Compare the scores of two judges on the same run: how much do they agree?

A judge is a model, and two models can read the same transcript and land on different numbers.
When that happens, the number is not the measurement, it is the opinion of one reader. This
script reads two scores files of the same run folder and says how far apart they are, so the
run can say whether its verdict survives the change of judge.

The agreement is reported three ways:

- percent agreement, the share of scenarios both judges scored the same. It overstates
  reliability when the scores are lopsided, so it is never the headline number.
- Cohen's kappa, the agreement corrected for what chance alone would produce.
- quadratic weighted kappa, which counts a 0 against a 2 as worse than a 0 against a 1, which
  fits an ordered scale of 0, 1 and 2.

Reading the kappa, from the guidance on model judges and from how these runs are used here:
0.80 or more is strong enough to gate a run, 0.70 to 0.80 is acceptable with a human audit,
0.60 to 0.70 is a flag and not a gate, and below 0.60 the rubric is the problem, not the judge.

Usage: python3 -I 90_System/Scripts/judge_agreement.py SCORES_A.json SCORES_B.json [--json]
"""
import argparse
import json
import sys
from pathlib import Path

CATEGORIES = (0, 1, 2)
THRESHOLDS = ((0.80, "strong enough to gate a run"),
              (0.70, "acceptable, with a human audit"),
              (0.60, "a flag, not a gate"))


def read_scores(path):
    """The scored scenarios of one judge, as {id: score}.

    A score outside the scale is refused. The matrices below are indexed by the score itself, so
    a 3 would raise and a -1 would be read as the last category, and a comparison that silently
    turns one judge's number into another category is worse than no comparison.
    """
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    scores = {}
    for key, entry in (data.get("scores") or {}).items():
        value = entry.get("score")
        if value is None:
            continue
        value = int(value)
        if value not in CATEGORIES:
            raise ValueError(f"scenario {key} has the score {value}, which is not on the scale "
                             f"{list(CATEGORIES)}")
        scores[str(key)] = value
    return scores, data


def cohen_kappa(pairs):
    """Cohen's kappa for two raters over the same items, or None when chance explains everything."""
    if not pairs:
        return None
    total = len(pairs)
    observed = sum(1 for a, b in pairs if a == b) / total
    counts_a, counts_b = {}, {}
    for a, b in pairs:
        counts_a[a] = counts_a.get(a, 0) + 1
        counts_b[b] = counts_b.get(b, 0) + 1
    expected = sum((counts_a.get(c, 0) / total) * (counts_b.get(c, 0) / total) for c in CATEGORIES)
    if expected >= 1:
        return None
    return round((observed - expected) / (1 - expected), 4)


def weighted_kappa(pairs):
    """Quadratic weighted kappa, which treats a 0 against a 2 as worse than a 0 against a 1."""
    if not pairs:
        return None
    total = len(pairs)
    size = len(CATEGORIES)
    # Both matrices have to be on the same scale. The observed one is a count and the expected
    # one is a share, so the observed one is divided by the number of pairs here. Without it the
    # ratio below is inflated by the number of pairs and the result leaves the -1 to 1 range.
    observed = [[0] * len(CATEGORIES) for _ in CATEGORIES]
    for a, b in pairs:
        observed[a][b] += 1 / total
    expected = [[0] * len(CATEGORIES) for _ in CATEGORIES]
    for i in range(size):
        row_total = sum(observed[i])
        for j in range(size):
            col_total = sum(observed[k][j] for k in range(size))
            expected[i][j] = row_total * col_total
    numerator = sum(((i - j) ** 2 / (size - 1) ** 2) * observed[i][j]
                    for i in range(size) for j in range(size))
    denominator = sum(((i - j) ** 2 / (size - 1) ** 2) * expected[i][j]
                      for i in range(size) for j in range(size))
    if denominator == 0:
        return None
    return round(1 - numerator / denominator, 4)


def percent_agreement(pairs):
    """The share of scenarios both judges scored the same."""
    if not pairs:
        return None
    return round(sum(1 for a, b in pairs if a == b) / len(pairs), 4)


def reading(kappa):
    """What the kappa means, in the words the eval guidance uses."""
    if kappa is None:
        return "no kappa to read"
    for threshold, meaning in THRESHOLDS:
        if kappa >= threshold:
            return f"kappa {kappa}: {meaning}"
    return f"kappa {kappa}: below 0.60, the rubric is the problem, not the judge"


def compare(path_a, path_b):
    """The two judges side by side, with the agreement measures."""
    scores_a, data_a = read_scores(path_a)
    scores_b, data_b = read_scores(path_b)
    shared = sorted(set(scores_a) & set(scores_b), key=lambda key: int(key))
    pairs = [(scores_a[key], scores_b[key]) for key in shared]
    rows = [{"scenario": key, "a": scores_a[key], "b": scores_b[key],
             "agree": scores_a[key] == scores_b[key]} for key in shared]
    return {
        "judge_a": {"family": data_a.get("judge_family"), "command": data_a.get("judge_command")},
        "judge_b": {"family": data_b.get("judge_family"), "command": data_b.get("judge_command")},
        "scenarios_compared": len(shared),
        "only_in_a": sorted(set(scores_a) - set(scores_b), key=int),
        "only_in_b": sorted(set(scores_b) - set(scores_a), key=int),
        "rows": rows,
        "percent_agreement": percent_agreement(pairs),
        "cohen_kappa": cohen_kappa(pairs),
        "weighted_kappa": weighted_kappa(pairs),
        "verdict_a": (data_a.get("verdict") or {}).get("verdict"),
        "verdict_b": (data_b.get("verdict") or {}).get("verdict"),
        "total_a": (data_a.get("verdict") or {}).get("total"),
        "total_b": (data_b.get("verdict") or {}).get("total"),
    }


def parse_args(argv):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("scores_a", type=Path, help="a scores.json file")
    ap.add_argument("scores_b", type=Path, help="another scores file of the same run")
    ap.add_argument("--json", dest="as_json", action="store_true", help="print the comparison as JSON")
    return ap.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    for path in (args.scores_a, args.scores_b):
        if not path.is_file():
            print(f"not a file: {path}", file=sys.stderr)
            return 2
    try:
        result = compare(args.scores_a, args.scores_b)
    except ValueError as error:
        print("refused:", error, file=sys.stderr)
        return 2
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    print(f"Judge A: {result['judge_a']['family']} ({result['judge_a']['command']})")
    print(f"Judge B: {result['judge_b']['family']} ({result['judge_b']['command']})")
    print(f"scenarios compared: {result['scenarios_compared']}")
    print()
    print("| # | A | B | same |")
    print("|---|---|---|---|")
    for row in result["rows"]:
        print(f"| {row['scenario']} | {row['a']} | {row['b']} | {'yes' if row['agree'] else 'no'} |")
    if result["only_in_a"]:
        print()
        print("only in A: " + ", ".join(result["only_in_a"]))
    if result["only_in_b"]:
        print()
        print("only in B: " + ", ".join(result["only_in_b"]))
    print()
    print(f"percent agreement: {result['percent_agreement']}")
    print(f"Cohen's kappa: {result['cohen_kappa']}")
    print(f"weighted kappa: {result['weighted_kappa']}")
    print(reading(result["cohen_kappa"]))
    print(f"total A: {result['total_a']}   total B: {result['total_b']}")
    print(f"verdict A: {result['verdict_a']}   verdict B: {result['verdict_b']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
