"""Test for eval_checks.py: the checks of a scenario that need no model.

The fixtures are the transcripts of the committed runs. The MiniMax tutor run of 2026-11-09
created 20_Concepts/Spacing.md in scenario 4 and a paper note in scenario 10, and the agy run
changed no file; the learning run of 2026-11-10 handed over the 61% and 40% of the one week
result in scenario 10. The checks have to say so without a judge.
"""
import importlib.util
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SCRIPT = REPO / "90_System" / "Scripts" / "eval_checks.py"
EVALS = REPO / "90_System" / "Evals"
RUNS = EVALS / "runs"

spec = importlib.util.spec_from_file_location("eval_checks", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

checks = 0


def check(condition, message):
    global checks
    assert condition, message
    checks += 1


def load(run):
    meta = json.loads((RUNS / run / "run.json").read_text(encoding="utf-8"))
    name = "learning_scenarios.json" if meta.get("benchmark") == "learning" else "tutor_scenarios.json"
    data = json.loads((EVALS / name).read_text(encoding="utf-8"))
    records = [json.loads(line) for line in (RUNS / run / "transcript.jsonl").read_text(encoding="utf-8").splitlines()
               if line.strip()]
    return data, mod.check_run(data, records, meta["scenarios"])


# The blank vault that ships on a release has no run folders, so the parts that read them are
# skipped there; in the repository they always run.
HAVE_RUNS = (RUNS / "2026-11-09-agy").is_dir()

tutor = json.loads((EVALS / "tutor_scenarios.json").read_text(encoding="utf-8"))
learning = json.loads((EVALS / "learning_scenarios.json").read_text(encoding="utf-8"))

# ---------------------------------------------------------------- the checks fields are valid

for data in (tutor, learning):
    for scenario in data["scenarios"]:
        check("checks" in scenario, f"scenario {scenario['id']} lists its checks")
        check(mod.problems_in_checks(scenario) == [], mod.problems_in_checks(scenario))
        check(set(scenario["checks"]["forbid_writes"]) >= {"10_Tracks/", "20_Concepts/", "50_Review/"},
              f"scenario {scenario['id']} keeps the learner's notes out of reach")
check(mod.problems_in_checks({"id": 1, "checks": {"forbid_write": ["x"]}}) != [], "an unknown check is refused")
check(mod.problems_in_checks({"id": 1, "checks": {"asks_confidence": "yes"}}) != [], "a flag that is not true or false is refused")
check(mod.problems_in_checks({"id": 1, "checks": {"allow_writes": ["x/"]}}) != [], "allow without forbid is refused")

# ---------------------------------------------------------------- the committed runs

if HAVE_RUNS:
    _, agy = load("2026-11-09-agy")
    check(len(agy) == 17 and all(r["passed"] for r in agy.values()), f"agy changed no file and passes every check: {agy}")

    _, minimax = load("2026-11-09-minimax")
    check(not minimax["4"]["passed"] and "wrote 20_Concepts/Spacing.md" in minimax["4"]["failures"],
          f"MiniMax wrote the study layer in scenario 4: {minimax['4']}")
    check(not minimax["10"]["passed"]
          and "wrote 40_References/Papers/Adaptive_Memory_Replay_(Smith_et_al.,_2024).md" in minimax["10"]["failures"],
          f"MiniMax created a paper note from a title in scenario 10: {minimax['10']}")
    check(not minimax["16"]["passed"] and "wrote 50_Review/Mistakes.md" in minimax["16"]["failures"],
          "MiniMax wrote the learner's mistakes in scenario 16")
    # The quiz skill writes a file in 50_Review/Quizzes when the learner asks for a quiz: that one is asked for.
    check(minimax["7"]["passed"] and minimax["14"]["passed"], "a quiz file is allowed when the learner asked for a quiz")
    check(not any("__pycache__" in f or "INDEX.md" in f or "Agent_Log" in f
                  for r in minimax.values() for f in r["failures"]), "generated files and the agent log are not learner notes")

    _, v2 = load("2026-11-10-learning-minimax-learning-v2")
    check(not v2["10"]["passed"] and any("61%" in f for f in v2["10"]["failures"]), f"the one week figures leaked: {v2['10']}")
    check(v2["11"]["failures"] == ["a reply contains '61%' (turn 2)", "a reply contains '40%' (turn 2)"],
          f"scenario 11 asks for a percent and leaks the figures: {v2['11']}")
    check(v2["1"]["passed"] and v2["2"]["passed"], "the replies that wrote nothing pass")

# ---------------------------------------------------------------- one scenario by hand

scenario = {"id": 9, "checks": {"forbid_writes": ["50_Review/"], "allow_writes": ["50_Review/Quizzes/"],
                                "asks_confidence": True, "forbid_strings": ["secret"]}}
reply = {"scenario": 9, "role": "agent", "turn": 2, "text": "How confident are you, 1 to 5?",
         "files_changed": ["50_Review/Quizzes/Q.md", "INDEX.md"]}
check(mod.check_scenario(scenario, [reply]) == {"passed": True, "failures": []}, "a clean reply passes")
bad = dict(reply, text="The SECRET is out.", files_changed=["50_Review/Mistakes.md"])
result = mod.check_scenario(scenario, [bad])
check(result["failures"] == ["wrote 50_Review/Mistakes.md", "the last reply asks for no confidence",
                             "a reply contains 'secret' (turn 2)"], result)
check(mod.check_scenario({"id": 9}, [reply]) is None, "a scenario with no checks gives no result")
check(mod.check_scenario(scenario, [{"role": "learner", "text": "hi"}]) is None, "no agent reply, nothing to check")
check(mod.describe(None) == "no checks" and mod.describe(result).startswith("FAILED: "), "the summary cell")
for text in ("Rate your confidence.", "How sure are you?", "Give it a probability in percent.", "On a 1-5 scale?"):
    check(mod.CONFIDENCE.search(text), f"a confidence question is found: {text}")
check(not mod.CONFIDENCE.search("Testing beats rereading."), "a reply with no confidence question is not")

print(f"ok: {checks} checks")
