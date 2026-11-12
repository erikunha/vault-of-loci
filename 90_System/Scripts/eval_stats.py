"""How sure a benchmark total is, how two runs differ, and how much several judges agree.

A run of the tutor or the learning benchmark is a handful of scenarios, scored once. Its total
is one draw: other scenarios of the same kind would give another total. This module says how
wide that spread is, without a model and without any package outside the standard library.

- `bootstrap_total`: the 95% interval of a total, by resampling the scenarios with replacement.
  The seed is fixed, so the same scores always print the same interval.
- `paired_difference`: the difference between two runs on the scenarios both ran, with the
  interval of that difference. Pairing by scenario removes the part of the spread that comes
  from some scenarios being harder than others (Miller, 2024, arXiv:2411.00640).
- `krippendorff_alpha`: the agreement of two or more judges, corrected for chance, with missing
  scores allowed. The ordinal distance fits a scale of 0, 1 and 2 (Krippendorff, 2011,
  "Computing Krippendorff's Alpha-Reliability").

Standard library only.
"""
import random

RESAMPLES = 10000
SEED = 20261109
LEVEL = 0.95
METRICS = ("nominal", "ordinal", "interval")


def _bounds(values, level):
    """The percentile interval of a list of numbers, nearest rank."""
    ordered = sorted(values)
    last = len(ordered) - 1
    cut = int((1 - level) / 2 * last)
    return ordered[cut], ordered[last - cut]


def _resampled_sums(values, resamples, seed):
    rng = random.Random(seed)
    n = len(values)
    return [sum(values[rng.randrange(n)] for _ in range(n)) for _ in range(resamples)]


def bootstrap_total(scores, resamples=RESAMPLES, seed=SEED, level=LEVEL):
    """The total of `scores` and its bootstrap interval, or None when there is no score.

    `scores` is the list of scenario scores one judge gave; None (not scored) is left out. Each
    resample draws as many scenarios as were scored, with replacement, and sums them. The
    interval is the middle `level` of those sums.
    """
    scores = [s for s in scores if s is not None]
    if not scores:
        return None
    low, high = _bounds(_resampled_sums(scores, resamples, seed), level)
    return {"total": sum(scores), "n": len(scores), "low": low, "high": high, "level": level,
            "resamples": resamples, "seed": seed}


def paired_difference(scores_a, scores_b, resamples=RESAMPLES, seed=SEED, level=LEVEL):
    """The difference A minus B on the scenarios both scored, with its bootstrap interval.

    `scores_a` and `scores_b` are {scenario id: score}. A scenario that one side did not score
    is left out and named, so the difference is always between the same scenarios.
    """
    shared = sorted(k for k in set(scores_a) & set(scores_b)
                    if scores_a[k] is not None and scores_b[k] is not None)
    left_out = sorted(k for k in set(scores_a) | set(scores_b) if k not in shared)
    if not shared:
        return None
    diffs = [scores_a[k] - scores_b[k] for k in shared]
    low, high = _bounds(_resampled_sums(diffs, resamples, seed), level)
    return {"difference": sum(diffs), "n": len(diffs), "low": low, "high": high, "level": level,
            "scenarios": shared, "left_out": left_out, "resamples": resamples, "seed": seed,
            "a_higher": sum(1 for d in diffs if d > 0), "b_higher": sum(1 for d in diffs if d < 0),
            "same": sum(1 for d in diffs if d == 0)}


def krippendorff_alpha(units, metric="ordinal"):
    """Krippendorff's alpha for a list of units, each a list of the values the judges gave.

    A missing value is None. A unit with fewer than two values says nothing about agreement and
    is left out, as the method says. Returns None when there is nothing to compare or when every
    value is the same, because then no disagreement was possible and chance explains it all.
    """
    if metric not in METRICS:
        raise ValueError(f"unknown metric: {metric}")
    pairable = [[v for v in unit if v is not None] for unit in units]
    pairable = [unit for unit in pairable if len(unit) >= 2]
    values = sorted({v for unit in pairable for v in unit})
    if len(values) < 2:
        return None
    # The coincidence matrix: every ordered pair of values from different judges in one unit,
    # weighted by 1 / (values in the unit - 1).
    coincidence = {(c, k): 0.0 for c in values for k in values}
    for unit in pairable:
        weight = 1 / (len(unit) - 1)
        for i, c in enumerate(unit):
            for j, k in enumerate(unit):
                if i != j:
                    coincidence[(c, k)] += weight
    marginal = {c: sum(coincidence[(c, k)] for k in values) for c in values}
    total = sum(marginal.values())

    def distance(c, k):
        if metric == "nominal":
            return 0.0 if c == k else 1.0
        if metric == "interval":
            return float((c - k) ** 2)
        low, high = min(c, k), max(c, k)
        between = sum(marginal[g] for g in values if low <= g <= high)
        return (between - (marginal[c] + marginal[k]) / 2) ** 2

    observed = sum(coincidence[(c, k)] * distance(c, k) for c in values for k in values)
    expected = sum(marginal[c] * marginal[k] * distance(c, k) for c in values for k in values)
    if expected == 0:
        return None
    return round(1 - (total - 1) * observed / expected, 4)
