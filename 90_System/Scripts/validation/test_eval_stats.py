"""Test for eval_stats.py: the interval of a total, the paired difference and Krippendorff's alpha.

The fixtures are the scores the judges of the runs of 2026-11-09 gave, as committed in the run
folders, and the worked example of Krippendorff (2011), whose values are published.
"""
import importlib.util
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SCRIPT = REPO / "90_System" / "Scripts" / "eval_stats.py"
RUNS = REPO / "90_System" / "Evals" / "runs"

spec = importlib.util.spec_from_file_location("eval_stats", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

checks = 0


def check(condition, message):
    global checks
    assert condition, message
    checks += 1


def scores(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    return {int(k): v["score"] for k, v in data["scores"].items()}


# The blank vault that ships on a release has no run folders, so the parts that read them are
# skipped there; in the repository they always run.
HAVE_RUNS = (RUNS / "2026-11-09-agy").is_dir()
if HAVE_RUNS:
    agy_kimi = scores(RUNS / "2026-11-09-agy" / "scores.json")
    minimax_kimi = scores(RUNS / "2026-11-09-minimax" / "scores-judge-kimi.json")
else:
    # The same scores, written out, so the interval is still checked without the run folders.
    agy_kimi = dict(zip(range(1, 18), [1, 0, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]))
    minimax_kimi = None

# ---------------------------------------------------------------- the interval of a total

result = mod.bootstrap_total(list(agy_kimi.values()))
check(result["total"] == 30 and result["n"] == 17, f"the total and n of the agy run: {result}")
check((result["low"], result["high"]) == (25, 34), f"the interval of 30 of 34 is 25 to 34 at the fixed seed: {result}")
check(mod.bootstrap_total(list(agy_kimi.values())) == result, "the same scores and seed give the same interval")
# Another seed moves each bound by at most one point: the interval is a property of the scores,
# not of the seed.
for seed in range(5):
    other = mod.bootstrap_total(list(agy_kimi.values()), seed=seed)
    check(abs(other["low"] - result["low"]) <= 1 and abs(other["high"] - result["high"]) <= 1,
          f"seed {seed} moves a bound by more than one point: {other}")
check(result["low"] <= result["total"] <= result["high"], "the total is inside its interval")
check(mod.bootstrap_total([None, None]) is None, "no scored scenario, no interval")
check(mod.bootstrap_total([2, None, 0])["n"] == 2, "an unscored scenario is left out of n")
same = mod.bootstrap_total([1, 1, 1, 1])
check((same["low"], same["high"]) == (4, 4), "scores that never vary give an interval of one point")

# ---------------------------------------------------------------- paired difference

if HAVE_RUNS:
    diff = mod.paired_difference(agy_kimi, minimax_kimi)
    check(diff["difference"] == 30 - 19 and diff["n"] == 17, f"agy minus MiniMax under the same judge family: {diff}")
    check(diff["low"] <= diff["difference"] <= diff["high"], "the difference is inside its interval")
    check(diff["a_higher"] + diff["b_higher"] + diff["same"] == 17, "every scenario is counted once")
partial = mod.paired_difference({1: 2, 2: 1, 3: None}, {1: 0, 2: 1, 4: 2})
check(partial["scenarios"] == [1, 2] and partial["left_out"] == [3, 4] and partial["difference"] == 2,
      f"a scenario one side did not score is left out and named: {partial}")
check(mod.paired_difference({1: None}, {2: 1}) is None, "nothing shared, no difference")

# ---------------------------------------------------------------- Krippendorff's alpha

# Krippendorff (2011), "Computing Krippendorff's Alpha-Reliability", the example with four
# observers, twelve units and missing values: nominal 0.743, ordinal 0.815, interval 0.849.
N = None
example = list(zip([1, 2, 3, 3, 2, 1, 4, 1, 2, N, N, N],
                   [1, 2, 3, 3, 2, 2, 4, 1, 2, 5, N, 3],
                   [N, 3, 3, 3, 2, 3, 4, 2, 2, 5, 1, N],
                   [1, 2, 3, 3, 2, 4, 4, 1, 2, 5, 1, N]))
check(round(mod.krippendorff_alpha(example, "nominal"), 3) == 0.743, mod.krippendorff_alpha(example, "nominal"))
check(round(mod.krippendorff_alpha(example, "ordinal"), 3) == 0.815, mod.krippendorff_alpha(example, "ordinal"))
check(round(mod.krippendorff_alpha(example, "interval"), 3) == 0.849, mod.krippendorff_alpha(example, "interval"))
check(mod.krippendorff_alpha([[0, 0], [1, 1], [2, 2]]) == 1.0, "full agreement is 1")
check(mod.krippendorff_alpha([[1, 1], [1, 1]]) is None, "one value everywhere leaves nothing to compare")
check(mod.krippendorff_alpha([[1, None], [2]]) is None, "units with one value are left out")
# By hand, nominal, two judges: units (0,0), (1,1), (0,1). Coincidences: 0-0 = 2, 1-1 = 2, 0-1 = 1
# and 1-0 = 1, so n_0 = n_1 = 3 and n = 6. Observed disagreement 2, expected 2 * 3 * 3 / 5 = 3.6,
# alpha = 1 - 2 / 3.6 = 0.4444.
check(mod.krippendorff_alpha([[0, 0], [1, 1], [0, 1]], "nominal") == 0.4444,
      mod.krippendorff_alpha([[0, 0], [1, 1], [0, 1]], "nominal"))
try:
    mod.krippendorff_alpha(example, "ratio")
    check(False, "an unknown metric is refused")
except ValueError:
    checks += 1

print(f"ok: {checks} checks")
