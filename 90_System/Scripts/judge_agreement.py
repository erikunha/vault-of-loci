"""Compare the scores of two or more judges on the same run: how much do they agree?

A judge is a model, and two models can read the same transcript and land on different numbers.
When that happens, the number is not the measurement, it is the opinion of one reader. This
script reads two or more scores files of the same run folder and says how far apart they are, so
the run can say whether its verdict survives the change of judge. When one judge passes the run
and another fails it, the verdict of the run is "contested".

The agreement is reported four ways:

- percent agreement, the share of scenarios both judges scored the same. It overstates
  reliability when the scores are lopsided, so it is never the headline number.
- Cohen's kappa, the agreement corrected for what chance alone would produce.
- quadratic weighted kappa, which counts a 0 against a 2 as worse than a 0 against a 1, which
  fits an ordered scale of 0, 1 and 2.
- Krippendorff's alpha, ordinal and nominal, across all the judges at once, with a scenario that
  one judge did not score left out of that judge's pairs (eval_stats.py).

Reading the kappa is a rule of thumb of this vault, not a published standard: 0.80 or more is
strong enough to gate a run, 0.70 to 0.80 is acceptable with a human audit, 0.60 to 0.70 is a
flag and not a gate, and below 0.60 the rubric is the problem, not the judge. With 17 scenarios
or fewer a kappa moves a lot with one score, so the percent agreement is printed next to it.

Usage: python3 -I 90_System/Scripts/judge_agreement.py SCORES_A.json SCORES_B.json [SCORES_C.json ...] [--json]
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import eval_stats  # noqa: E402

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
        if isinstance(value, float) and value.is_integer():
            value = int(value)
        if isinstance(value, bool) or not isinstance(value, int) or value not in CATEGORIES:
            raise ValueError(f"scenario {key} has the score {value!r}, which is not on the scale "
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


def run_verdict(verdicts):
    """The verdict of the run across its judges: contested when one passes it and one fails it."""
    decided = {v for v in verdicts if v is not None}
    if {"pass", "fail"} <= decided:
        return "contested"
    if len(decided) == 1 and None not in verdicts:
        return decided.pop()
    return "incomplete"


def compare_many(paths):
    """Every judge against every other, Krippendorff's alpha across all, and the run verdict."""
    loaded = [read_scores(path) for path in paths]
    ids = sorted({key for scores, _ in loaded for key in scores}, key=int)
    units = [[scores.get(key) for scores, _ in loaded] for key in ids]
    pairs = []
    for a in range(len(paths)):
        for b in range(a + 1, len(paths)):
            pair = compare(paths[a], paths[b])
            pairs.append({"a": str(paths[a]), "b": str(paths[b]),
                          **{k: pair[k] for k in ("scenarios_compared", "percent_agreement", "cohen_kappa",
                                                  "weighted_kappa")}})
    verdicts = [(data.get("verdict") or {}).get("verdict") for _, data in loaded]
    return {
        "judges": [{"file": str(path), "family": data.get("judge_family"), "command": data.get("judge_command"),
                    "verdict": verdict, "total": (data.get("verdict") or {}).get("total")}
                   for path, (_, data), verdict in zip(paths, loaded, verdicts)],
        "rows": [{"scenario": key, "scores": [scores.get(key) for scores, _ in loaded]} for key in ids],
        "pairs": pairs,
        "alpha_ordinal": eval_stats.krippendorff_alpha(units, "ordinal"),
        "alpha_nominal": eval_stats.krippendorff_alpha(units, "nominal"),
        "run_verdict": run_verdict(verdicts),
    }


def parse_args(argv):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("scores", type=Path, nargs="+", help="two or more scores files of the same run")
    ap.add_argument("--json", dest="as_json", action="store_true", help="print the comparison as JSON")
    return ap.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    if len(args.scores) < 2:
        print("give two or more scores files", file=sys.stderr)
        return 2
    for path in args.scores:
        if not path.is_file():
            print(f"not a file: {path}", file=sys.stderr)
            return 2
    try:
        many = compare_many(args.scores)
        result = compare(args.scores[0], args.scores[1])
    except ValueError as error:
        print("refused:", error, file=sys.stderr)
        return 2
    result.update({k: many[k] for k in ("alpha_ordinal", "alpha_nominal", "run_verdict")})
    if len(args.scores) > 2:
        return print_many(many, args.as_json)
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
    print(f"Krippendorff's alpha: ordinal {result['alpha_ordinal']}, nominal {result['alpha_nominal']}")
    print(f"run verdict across the judges: {result['run_verdict']}")
    return 0


def print_many(many, as_json):
    if as_json:
        print(json.dumps(many, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    for i, judge in enumerate(many["judges"], 1):
        print(f"Judge {i}: {judge['family']} ({judge['file']}), total {judge['total']}, verdict {judge['verdict']}")
    print()
    print("| # | " + " | ".join(str(i) for i in range(1, len(many["judges"]) + 1)) + " |")
    print("|---|" + "---|" * len(many["judges"]))
    for row in many["rows"]:
        print(f"| {row['scenario']} | " + " | ".join("-" if s is None else str(s) for s in row["scores"]) + " |")
    print()
    for pair in many["pairs"]:
        print(f"{pair['a']} vs {pair['b']}: percent {pair['percent_agreement']}, kappa {pair['cohen_kappa']}, "
              f"weighted kappa {pair['weighted_kappa']} ({pair['scenarios_compared']} scenarios)")
    print(f"Krippendorff's alpha: ordinal {many['alpha_ordinal']}, nominal {many['alpha_nominal']}")
    print(f"run verdict across the judges: {many['run_verdict']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
