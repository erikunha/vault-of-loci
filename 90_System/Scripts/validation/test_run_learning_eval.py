"""Test for the learning benchmark: the scenarios, the dated setup and the run it produces.

The tutor eval is covered by test_run_tutor_eval.py. This one checks the second benchmark: the
scenarios match the Markdown table, the setup ages the learner's record with real dates, and the
runner keeps the two benchmarks apart.
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SCRIPT = REPO / "90_System" / "Scripts" / "run_tutor_eval.py"
SCENARIOS = REPO / "90_System" / "Evals" / "learning_scenarios.json"
MARKDOWN = REPO / "90_System" / "Evals" / "Learning_evals.md"

spec = importlib.util.spec_from_file_location("run_tutor_eval", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

checks = 0


def check(condition, message):
    global checks
    assert condition, message
    checks += 1


FAKE_AGENT = """import sys
sys.stdin.read()
print("I read the record and here is what I would do.")
"""

# A judge that gives a different number on every call, so the repeatability check has something
# to measure. The counter lives in a file next to the script.
FAKE_JUDGE = """import sys, os, pathlib
sys.stdin.read()
counter = pathlib.Path(__file__).with_suffix(".count")
count = int(counter.read_text()) if counter.exists() else 0
counter.write_text(str(count + 1))
print("WHY: the reply is off the rubric.")
print("SCORE: " + str(count % 3))
"""

# A judge that writes down the prompt it received, so the test can see which rubric it was given.
# The prompts are appended, because one run sends one prompt per scenario.
PROBE_JUDGE = """import sys, pathlib
prompt = sys.stdin.read()
path = pathlib.Path(__file__).with_suffix(".prompt")
with path.open("a") as handle:
    handle.write(prompt + "\\n=== NEXT ===\\n")
print("WHY: the probe says so.")
print("SCORE: 1")
"""

# A judge whose reason names the score it gave. The run keeps one score, so it has to keep the
# reason of that score and not the reason of another number the judge gave.
REASONING_JUDGE = """import sys, pathlib
sys.stdin.read()
counter = pathlib.Path(__file__).with_suffix(".count")
count = int(counter.read_text()) if counter.exists() else 0
counter.write_text(str(count + 1))
score = [2, 1, 1][count % 3]
print("WHY: reason for " + str(score))
print("SCORE: " + str(score))
"""

# A judge that never gives a number.
SILENT_JUDGE = """import sys
sys.stdin.read()
print("I am thinking about it.")
"""


# When the judge gives different numbers on the same transcript, the run takes the one it gave
# most often. A tie goes to the lower score, so an unsure judge does not give the run the
# benefit of the doubt.
check(mod.modal_score([1, 2, 2]) == 2, "the most frequent score wins")
check(mod.modal_score([1, 2]) == 1, "a tie goes to the lower score")
check(mod.modal_score([]) is None, "no score is no score")
check(mod.modal_score([None, None]) is None, "no usable score is no score")
check(mod.modal_score([0, 0, 1]) == 0, "the mode wins even when it is the low score")


data = json.loads(SCENARIOS.read_text(encoding="utf-8"))
markdown = MARKDOWN.read_text(encoding="utf-8")
check(mod.check_drift(data, markdown) == [], f"learning_scenarios.json differs from Learning_evals.md: {mod.check_drift(data, markdown)}")
check([s["id"] for s in data["scenarios"]] == list(range(1, 16)), "fifteen scenarios, ids 1 to 15")
check(data["pass_rule"]["critical"] == [1, 2, 3, 10, 11], "scenarios 1, 2, 3, 10 and 11 are critical")
check(data["pass_rule"]["groups"][0]["total"] == 30, "the whole benchmark is worth 30 points")
check(data["pass_rule"]["groups"][1]["scenarios"] == "1,2,3,10,11", "the critical group is 1, 2, 3, 10 and 11")
check(all(s["turns"] for s in data["scenarios"]), "every scenario has a learner turn")
check(all(s["setup_description"] for s in data["scenarios"]), "every scenario says what the record holds")
check("tutor" in mod.BENCHMARKS and "learning" in mod.BENCHMARKS, "the runner knows both benchmarks")
check(mod.BENCHMARKS["tutor"]["run_prefix"] == "", "the tutor run folders keep their name")
check(mod.BENCHMARKS["learning"]["run_prefix"] == "learning-", "the learning run folders are named apart")

# The pass rule has two conditions and both have to hold: 24 of 30 points and 8 of 10 in the
# critical group, with no 0 in scenarios 1, 2, 3, 10 or 11 (Learning_evals.md). A run that meets
# one and misses the other does not pass.
everyone = list(range(1, 16))
check(mod.critical_mark(data["pass_rule"]) == data["pass_rule"]["groups"][1],
      "the critical group has a mark of its own")
all_two = {i: 2 for i in everyone}
result = mod.evaluate(data, all_two, everyone)
check(result["verdict"] == "pass" and result["total"] == 30, f"30 of 30 passes: {result}")
check("24 of 30" in result["rule"] and "8 of 10" in result["rule"],
      f"the rule states both conditions: {result['rule']}")
# 24 of 30 points, but only 5 of 10 in the critical group: the total is met and the critical
# group is not, so the run fails.
low_critical = {i: 2 for i in everyone}
for i in (1, 2, 3, 10, 11):
    low_critical[i] = 1
low_critical[15] = 1
result = mod.evaluate(data, low_critical, everyone)
check(result["total"] == 24, f"the total is 24: {result}")
check(result["verdict"] == "fail", f"24 of 30 with 5 of 10 in the critical group fails: {result}")
# 24 of 30 points and 8 of 10 in the critical group: both are met, so the run passes.
both = {i: 2 for i in everyone}
for i in (10, 11):
    both[i] = 1
for i in (4, 5, 6, 7):
    both[i] = 1
result = mod.evaluate(data, both, everyone)
check(result["total"] == 24, f"the total is 24: {result}")
check(result["verdict"] == "pass", f"24 of 30 with 8 of 10 in the critical group passes: {result}")
# The critical group alone is still judged by its own mark of 8 of 10.
critical_only = [1, 2, 3, 10, 11]
result = mod.evaluate(data, {i: 2 for i in critical_only}, critical_only)
check(result["verdict"] == "pass" and result["rule"] == "8 of 10, no 0 in scenarios 1, 2, 3, 10, 11",
      f"the critical group on its own: {result}")
# A 0 in a critical scenario still fails the run even with 29 of 30.
check(mod.evaluate(data, {**all_two, **{3: 0}}, everyone)["verdict"] == "fail",
      "a 0 in a critical scenario fails even with 29 of 30")

# The judge has to name the benchmark it is scoring. The two benchmarks in this repo share the
# same 0 to 2 scale, and a judge reading the wrong rubric scores the wrong thing.
check("Benchmark: " in mod.judge_prompt(data, data["scenarios"][0], []),
      "the judge prompt names the benchmark")
check("Length is not quality" in mod.judge_prompt(data, data["scenarios"][0], []),
      "the judge prompt says that length is not quality")
prompt = mod.judge_prompt(data, data["scenarios"][0], [])
check(prompt.index("WHY:") < prompt.index("SCORE:"), "the judge answers why before the score")
check(mod.parse_judge("WHY: because\nSCORE: 2") == (2, "because"), "the judge reply is parsed")

# The token in a setup becomes a real date.
filled = mod.fill_dates("{\"occurred_at\": \"{{today-30}}\"}")
check("{{" not in filled, f"the date token is filled: {filled}")
check(mod.fill_dates("{{today-30}}") != mod.fill_dates("{{today-31}}"), "each age gives its own date")

# Scenario 1 asks the agent which objective is due and at which horizon. The rubric names a
# horizon, so the audit has to give the same answer on the same ledger, or the benchmark
# penalises the agent for the number the vault itself produces.
audit_spec = importlib.util.spec_from_file_location("audit", REPO / "90_System" / "Scripts" / "audit.py")
audit_mod = importlib.util.module_from_spec(audit_spec)
audit_spec.loader.exec_module(audit_mod)
scenario_one = [s for s in data["scenarios"] if s["id"] == 1][0]
fixture_events = []
for op in scenario_one["setup"]:
    if op.get("op") == "write_file":
        for line in op["content"].splitlines():
            if line.strip():
                fixture_events.append(json.loads(mod.fill_dates(line)))
report = audit_mod.audit(fixture_events, (7, 30, 90), date.today())
rows = {row["objective_id"]: row for row in report["objectives"]}
check(rows["retrieval-practice-recall"]["status"] == "due at 90 days",
      f"the audit says the recall objective is due at 90 days: {rows['retrieval-practice-recall']}")
check("90 days" in scenario_one["pass"], f"the rubric asks for that horizon: {scenario_one['pass']}")
check(rows["retrieval-practice-apply"]["status"] == "measured",
      f"the apply objective was measured at 7, 30 and 90 days: {rows['retrieval-practice-apply']}")
check([row["objective_id"] for row in report["due"]] == ["retrieval-practice-recall"],
      f"only the recall objective is due: {report['due']}")


# Scoring a run has to use the benchmark the run belongs to. The flag is only the default: with
# the tutor rubric the judge quotes rules from the other benchmark and scores the wrong thing.
learn_bench, learn_data = mod.benchmark_of_run({"benchmark": "learning"}, REPO, mod.BENCHMARKS["tutor"])
check(learn_bench["run_prefix"] == "learning-", f"the run folder decides the benchmark: {learn_bench}")
check(learn_data["scenarios"][0]["pass"] == data["scenarios"][0]["pass"],
      "a learning run is scored with the learning scenarios")
tutor_data = json.loads((REPO / "90_System" / "Evals" / "tutor_scenarios.json").read_text(encoding="utf-8"))
check(learn_data["scenarios"][0]["pass"] != tutor_data["scenarios"][0]["pass"],
      "the two benchmarks do not share the same rubric")
tutor_bench, tutor_loaded = mod.benchmark_of_run({"benchmark": "tutor"}, REPO, mod.BENCHMARKS["tutor"])
check(tutor_loaded["scenarios"][0]["pass"] == tutor_data["scenarios"][0]["pass"],
      "a tutor run is scored with the tutor scenarios")

# A run.json with no benchmark field takes the fallback, the same way an unknown name does.
missing_bench, missing_loaded = mod.benchmark_of_run({}, REPO, mod.BENCHMARKS["learning"])
check(missing_bench["run_prefix"] == "learning-", f"a run with no benchmark takes the fallback: {missing_bench}")
unknown_bench, unknown_loaded = mod.benchmark_of_run({"benchmark": "nope"}, REPO, mod.BENCHMARKS["learning"])
check(unknown_bench["run_prefix"] == "learning-", f"an unknown benchmark takes the fallback: {unknown_bench}")
check(mod.benchmark_problem({"benchmark": "nope"}) is not None, "an unknown benchmark is refused")
check(mod.benchmark_problem({"benchmark": "learning"}) is None, "a known benchmark is accepted")
check(mod.benchmark_problem({}) is None, "a run with no benchmark field is not refused")


def make_vault(base):
    root = base / "vault"
    (root / "90_System" / "Evals").mkdir(parents=True)
    (root / "90_System" / "Evals" / "learning_scenarios.json").write_text(SCENARIOS.read_text(encoding="utf-8"), encoding="utf-8")
    (root / "90_System" / "Evals" / "Learning_evals.md").write_text(markdown, encoding="utf-8")
    # The tutor benchmark is here too, so a scoring path that picks the wrong benchmark fails on
    # the rubric it hands to the judge and not on a file that is missing.
    tutor_scenarios = REPO / "90_System" / "Evals" / "tutor_scenarios.json"
    tutor_markdown = REPO / "90_System" / "Evals" / "Tutor_mode.md"
    (root / "90_System" / "Evals" / "tutor_scenarios.json").write_text(tutor_scenarios.read_text(encoding="utf-8"), encoding="utf-8")
    (root / "90_System" / "Evals" / "Tutor_mode.md").write_text(tutor_markdown.read_text(encoding="utf-8"), encoding="utf-8")
    (root / "20_Concepts").mkdir()
    (root / "20_Concepts" / "Retrieval_Practice.md").write_text(
        "---\ntype: concept\nlast_tested:\nscore:\nconfidence:\n---\n\n# Retrieval practice\n", encoding="utf-8")
    (root / "50_Review").mkdir()
    (root / "50_Review" / "Attempts.jsonl").write_text("", encoding="utf-8")
    (root / "10_Tracks" / "01_Example_Course" / "practice").mkdir(parents=True)
    (root / "AGENTS.md").write_text("# AGENTS.md\n\nThe learner attempts first.\n", encoding="utf-8")
    (root / "00_Home.md").write_text("# Home\n", encoding="utf-8")
    (root / ".git").mkdir()
    (root / ".git" / "HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")
    return root


with tempfile.TemporaryDirectory() as tmp:
    base = Path(tmp)
    agent = base / "agent.py"
    agent.write_text(FAKE_AGENT, encoding="utf-8")
    root = make_vault(base)

    run = subprocess.run([sys.executable, "-I", str(SCRIPT), "--root", str(root), "--date", "2026-01-02",
                          "--benchmark", "learning", "--agent-cmd", f"{sys.executable} {agent}",
                          "--label", "fake", "--agent-family", "test", "--scenarios", "1,2"],
                         capture_output=True, text=True, env=os.environ, timeout=300)
    check(run.returncode == 0, f"the learning run finishes: {run.stdout} {run.stderr}")
    run_dir = root / "90_System" / "Evals" / "runs" / "2026-01-02-learning-fake"
    check(run_dir.is_dir(), f"the run folder is named apart from the tutor runs: {run_dir}")
    meta = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
    check(meta["benchmark"] == "learning", meta)
    check(meta["scenarios"] == [1, 2], meta)
    transcript = (run_dir / "transcript.jsonl").read_text(encoding="utf-8")
    check("Which of my topics is due for a delayed test?" in transcript, "the learner turn is in the transcript")
    check("I read the record" in transcript, "the agent reply is in the transcript")
    check((run_dir / "scoring_sheet.md").is_file(), "the scoring sheet is there")
    sheet = (run_dir / "scoring_sheet.md").read_text(encoding="utf-8")
    check("Learning_evals.md" in sheet, f"the sheet points at the learning table: {sheet[:200]}")

    # The setup wrote a ledger with real dates, and the real vault was not changed.
    check("{{today-" not in transcript, "no date token leaked into the run")
    check((root / "50_Review" / "Attempts.jsonl").read_text(encoding="utf-8") == "",
          "the real vault keeps its own ledger")

    # Scoring the same run three times with an unstable judge says how unstable it was.
    judge = base / "judge.py"
    judge.write_text(FAKE_JUDGE, encoding="utf-8")
    repeat = subprocess.run([sys.executable, "-I", str(SCRIPT), "--root", str(root), "--date", "2026-01-02",
                             "--benchmark", "learning", "--score-run", str(run_dir),
                             "--judge-cmd", f"{sys.executable} {judge}", "--judge-family", "other",
                             "--judge-repeats", "3", "--force"],
                            capture_output=True, text=True, env=os.environ, timeout=300)
    check(repeat.returncode == 0, f"the repeated scoring finishes: {repeat.stdout} {repeat.stderr}")
    scores = json.loads((run_dir / "scores.json").read_text(encoding="utf-8"))
    entry = scores["scores"]["1"]
    check(entry.get("repeats") == [0, 1, 2], f"the three judgements are kept: {entry}")
    check(entry.get("consistent") == "1/3", f"the agreement of the judge is written: {entry}")
    check(entry["score"] == 0, f"the tie goes to the lower score: {entry}")
    summary = (run_dir / "summary.md").read_text(encoding="utf-8")
    check("judge agreed on 1/3" in summary, f"the summary says how stable the judge was: {summary}")

    # The run folder decides the benchmark, not the flag. A judge that writes down the prompt it
    # received shows which rubric it was given: the learning one for a learning run, even when the
    # flag on the command line says tutor. This drives the real --score-run and --summarize
    # paths, so removing the call sites that pick the benchmark breaks this test.
    probe = base / "probe.py"
    probe.write_text(PROBE_JUDGE, encoding="utf-8")
    (base / "probe.prompt").unlink(missing_ok=True)
    probe_run = subprocess.run([sys.executable, "-I", str(SCRIPT), "--root", str(root), "--date", "2026-01-02",
                                "--benchmark", "tutor", "--score-run", str(run_dir),
                                "--judge-cmd", f"{sys.executable} {probe}", "--judge-family", "other",
                                "--force"],
                               capture_output=True, text=True, env=os.environ, timeout=300)
    check(probe_run.returncode == 0, f"the probe judge scores the run: {probe_run.stdout} {probe_run.stderr}")
    sent = (base / "probe.prompt").read_text(encoding="utf-8")
    check(data["scenarios"][0]["pass"] in sent,
          "the judge of a learning run gets the learning rubric, not the tutor one")
    check(tutor_data["scenarios"][0]["pass"] not in sent,
          "the tutor rubric did not leak into the judge of a learning run")

    # --summarize rebuilds the verdict from the scores and the same benchmark.
    (base / "probe.prompt").unlink(missing_ok=True)
    again = subprocess.run([sys.executable, "-I", str(SCRIPT), "--root", str(root), "--date", "2026-01-02",
                            "--benchmark", "tutor", "--summarize", str(run_dir)],
                           capture_output=True, text=True, env=os.environ, timeout=300)
    check(again.returncode == 0, f"the summary is rebuilt: {again.stdout} {again.stderr}")
    check((run_dir / "summary.md").is_file(), "the summary is there")

    # A run folder that claims a benchmark that does not exist is refused instead of being scored
    # with the benchmark of the flag.
    broken = root / "90_System" / "Evals" / "runs" / "2026-01-02-learning-broken"
    shutil.copytree(run_dir, broken)
    broken_meta = json.loads((broken / "run.json").read_text(encoding="utf-8"))
    broken_meta["benchmark"] = "nope"
    (broken / "run.json").write_text(json.dumps(broken_meta, indent=2), encoding="utf-8")
    refused = subprocess.run([sys.executable, "-I", str(SCRIPT), "--root", str(root), "--date", "2026-01-02",
                              "--benchmark", "tutor", "--score-run", str(broken),
                              "--judge-cmd", f"{sys.executable} {probe}", "--judge-family", "other",
                              "--force"],
                             capture_output=True, text=True, env=os.environ, timeout=300)
    check(refused.returncode == 2, f"an unknown benchmark in run.json is refused: {refused.stdout} {refused.stderr}")
    check("refused" in refused.stderr, f"the refusal says why: {refused.stderr}")

    # A run folder with no benchmark at all is scored with the benchmark of the flag, and the
    # operator is told, because that is the case where the wrong rubric can reach the judge.
    legacy = root / "90_System" / "Evals" / "runs" / "2026-01-02-learning-legacy"
    shutil.copytree(run_dir, legacy)
    legacy_meta = json.loads((legacy / "run.json").read_text(encoding="utf-8"))
    del legacy_meta["benchmark"]
    (legacy / "run.json").write_text(json.dumps(legacy_meta, indent=2), encoding="utf-8")
    legacy_run = subprocess.run([sys.executable, "-I", str(SCRIPT), "--root", str(root), "--date", "2026-01-02",
                                 "--benchmark", "tutor", "--score-run", str(legacy),
                                 "--judge-cmd", f"{sys.executable} {probe}", "--judge-family", "other",
                                 "--force"],
                                capture_output=True, text=True, env=os.environ, timeout=300)
    check(legacy_run.returncode == 0, f"a run folder with no benchmark is still scored: {legacy_run.stdout} {legacy_run.stderr}")
    check("does not record a benchmark" in legacy_run.stderr,
          f"the fallback is said out loud: {legacy_run.stderr}")

    # A scenario that the benchmark does not have is refused instead of raising.
    alien = root / "90_System" / "Evals" / "runs" / "2026-01-02-learning-alien"
    shutil.copytree(run_dir, alien)
    alien_meta = json.loads((alien / "run.json").read_text(encoding="utf-8"))
    alien_meta["scenarios"] = [99]
    (alien / "run.json").write_text(json.dumps(alien_meta, indent=2), encoding="utf-8")
    alien_run = subprocess.run([sys.executable, "-I", str(SCRIPT), "--root", str(root), "--date", "2026-01-02",
                                "--benchmark", "learning", "--score-run", str(alien),
                                "--judge-cmd", f"{sys.executable} {probe}", "--judge-family", "other",
                                "--force"],
                               capture_output=True, text=True, env=os.environ, timeout=300)
    check(alien_run.returncode == 2, f"a scenario outside the benchmark is refused: {alien_run.stdout} {alien_run.stderr}")
    check("Traceback" not in alien_run.stderr, f"the refusal is clean: {alien_run.stderr}")

    # A run folder with no scores to summarise is refused instead of raising.
    empty_run = root / "90_System" / "Evals" / "runs" / "2026-01-02-learning-empty"
    empty_run.mkdir(parents=True)
    (empty_run / "run.json").write_text(json.dumps(alien_meta, indent=2), encoding="utf-8")
    empty_summary = subprocess.run([sys.executable, "-I", str(SCRIPT), "--root", str(root), "--date", "2026-01-02",
                                    "--benchmark", "learning", "--summarize", str(empty_run)],
                                   capture_output=True, text=True, env=os.environ, timeout=300)
    check(empty_summary.returncode == 2, f"a run folder with no scores is refused: {empty_summary.stdout} {empty_summary.stderr}")
    check("Traceback" not in empty_summary.stderr, f"the refusal is clean: {empty_summary.stderr}")

    # A run folder that is missing a file the path needs is refused with a message, not a traceback.
    # --score-run with no run.json.
    no_meta = root / "90_System" / "Evals" / "runs" / "2026-01-02-learning-no-meta"
    no_meta.mkdir(parents=True)
    no_meta_run = subprocess.run([sys.executable, "-I", str(SCRIPT), "--root", str(root), "--date", "2026-01-02",
                                  "--benchmark", "learning", "--score-run", str(no_meta),
                                  "--judge-cmd", f"{sys.executable} {probe}", "--judge-family", "other"],
                                 capture_output=True, text=True, env=os.environ, timeout=300)
    check(no_meta_run.returncode == 1, f"a run folder with no run.json is refused: {no_meta_run.stdout} {no_meta_run.stderr}")
    check("Traceback" not in no_meta_run.stderr, f"the refusal is clean: {no_meta_run.stderr}")
    check("run.json" in no_meta_run.stderr and str(no_meta) in no_meta_run.stderr,
          f"the refusal names what is missing and the path: {no_meta_run.stderr}")

    # --summarize with no run.json.
    no_meta_summary = root / "90_System" / "Evals" / "runs" / "2026-01-02-learning-no-meta-sum"
    no_meta_summary.mkdir(parents=True)
    (no_meta_summary / "scores.json").write_text(json.dumps({"scores": {}}), encoding="utf-8")
    no_meta_sum = subprocess.run([sys.executable, "-I", str(SCRIPT), "--root", str(root), "--date", "2026-01-02",
                                  "--benchmark", "learning", "--summarize", str(no_meta_summary)],
                                 capture_output=True, text=True, env=os.environ, timeout=300)
    check(no_meta_sum.returncode == 1, f"--summarize with no run.json is refused: {no_meta_sum.stdout} {no_meta_sum.stderr}")
    check("Traceback" not in no_meta_sum.stderr, f"the refusal is clean: {no_meta_sum.stderr}")
    check("run.json" in no_meta_sum.stderr and str(no_meta_summary) in no_meta_sum.stderr,
          f"the refusal names what is missing and the path: {no_meta_sum.stderr}")

    # --summarize with a scores.json that holds no scores.
    empty_scores = root / "90_System" / "Evals" / "runs" / "2026-01-02-learning-empty-scores"
    empty_scores.mkdir(parents=True)
    (empty_scores / "run.json").write_text(json.dumps(alien_meta, indent=2), encoding="utf-8")
    (empty_scores / "scores.json").write_text(json.dumps({"judge_family": "other"}), encoding="utf-8")
    empty_scores_run = subprocess.run([sys.executable, "-I", str(SCRIPT), "--root", str(root), "--date", "2026-01-02",
                                       "--benchmark", "learning", "--summarize", str(empty_scores)],
                                      capture_output=True, text=True, env=os.environ, timeout=300)
    check(empty_scores_run.returncode == 1, f"a scores.json with no scores is refused: {empty_scores_run.stdout} {empty_scores_run.stderr}")
    check("Traceback" not in empty_scores_run.stderr, f"the refusal is clean: {empty_scores_run.stderr}")
    check("scores.json" in empty_scores_run.stderr and str(empty_scores) in empty_scores_run.stderr,
          f"the refusal names what is missing and the path: {empty_scores_run.stderr}")

    # --summarize with a score outside the scale of 0, 1 or 2. The run must refuse it, and it
    # must not print a total that no scenario can hold.
    off_scale = root / "90_System" / "Evals" / "runs" / "2026-01-02-learning-off-scale"
    off_scale.mkdir(parents=True)
    (off_scale / "run.json").write_text(json.dumps(alien_meta, indent=2), encoding="utf-8")
    (off_scale / "scores.json").write_text(json.dumps(
        {"judge_family": "other", "scores": {"99": {"score": 13, "why": "edited by hand"}}}), encoding="utf-8")
    off_scale_run = subprocess.run([sys.executable, "-I", str(SCRIPT), "--root", str(root), "--date", "2026-01-02",
                                   "--benchmark", "learning", "--summarize", str(off_scale)],
                                  capture_output=True, text=True, env=os.environ, timeout=300)
    check(off_scale_run.returncode == 1, f"a score outside the scale is refused: {off_scale_run.stdout} {off_scale_run.stderr}")
    check("Traceback" not in off_scale_run.stderr, f"the refusal is clean: {off_scale_run.stderr}")
    check("13 of 10" not in off_scale_run.stdout, f"no total outside the scale: {off_scale_run.stdout}")

    # --summarize with a run.json that is not valid JSON.
    broken_json = root / "90_System" / "Evals" / "runs" / "2026-01-02-learning-broken-json"
    broken_json.mkdir(parents=True)
    (broken_json / "run.json").write_text("{not json", encoding="utf-8")
    (broken_json / "scores.json").write_text(json.dumps({"scores": {"99": {"score": 1}}}), encoding="utf-8")
    broken_json_run = subprocess.run([sys.executable, "-I", str(SCRIPT), "--root", str(root), "--date", "2026-01-02",
                                      "--benchmark", "learning", "--summarize", str(broken_json)],
                                     capture_output=True, text=True, env=os.environ, timeout=300)
    check(broken_json_run.returncode == 1, f"a run.json that is not JSON is refused: {broken_json_run.stdout} {broken_json_run.stderr}")
    check("Traceback" not in broken_json_run.stderr, f"the refusal is clean: {broken_json_run.stderr}")
    check("run.json" in broken_json_run.stderr, f"the refusal names the file: {broken_json_run.stderr}")

    # --score-run with no transcript.jsonl.
    no_transcript = root / "90_System" / "Evals" / "runs" / "2026-01-02-learning-no-transcript"
    no_transcript.mkdir(parents=True)
    (no_transcript / "run.json").write_text(json.dumps(alien_meta, indent=2), encoding="utf-8")
    no_transcript_run = subprocess.run([sys.executable, "-I", str(SCRIPT), "--root", str(root), "--date", "2026-01-02",
                                        "--benchmark", "learning", "--score-run", str(no_transcript),
                                        "--judge-cmd", f"{sys.executable} {probe}", "--judge-family", "other"],
                                       capture_output=True, text=True, env=os.environ, timeout=300)
    check(no_transcript_run.returncode == 1, f"a run folder with no transcript is refused: {no_transcript_run.stdout} {no_transcript_run.stderr}")
    check("Traceback" not in no_transcript_run.stderr, f"the refusal is clean: {no_transcript_run.stderr}")
    check("transcript.jsonl" in no_transcript_run.stderr and str(no_transcript) in no_transcript_run.stderr,
          f"the refusal names what is missing and the path: {no_transcript_run.stderr}")

    # The reason kept is the reason of the score kept.
    reasoner = base / "reasoner.py"
    reasoner.write_text(REASONING_JUDGE, encoding="utf-8")
    (base / "reasoner.count").unlink(missing_ok=True)
    reason_run = subprocess.run([sys.executable, "-I", str(SCRIPT), "--root", str(root), "--date", "2026-01-02",
                                 "--benchmark", "learning", "--score-run", str(run_dir),
                                 "--judge-cmd", f"{sys.executable} {reasoner}", "--judge-family", "other",
                                 "--judge-repeats", "3", "--force"],
                                capture_output=True, text=True, env=os.environ, timeout=300)
    check(reason_run.returncode == 0, f"the repeated scoring finishes: {reason_run.stdout} {reason_run.stderr}")
    reason_scores = json.loads((run_dir / "scores.json").read_text(encoding="utf-8"))
    reason_entry = reason_scores["scores"]["1"]
    check(reason_entry["score"] == 1, f"the mode wins: {reason_entry}")
    check(reason_entry["why"] == "reason for 1", f"the reason is the reason of the score kept: {reason_entry}")

    # A judge that gives no number is not agreement. It must not report that it agreed.
    silent = base / "silent.py"
    silent.write_text(SILENT_JUDGE, encoding="utf-8")
    silent_run = subprocess.run([sys.executable, "-I", str(SCRIPT), "--root", str(root), "--date", "2026-01-02",
                                 "--benchmark", "learning", "--score-run", str(run_dir),
                                 "--judge-cmd", f"{sys.executable} {silent}", "--judge-family", "other",
                                 "--judge-repeats", "2", "--force"],
                                capture_output=True, text=True, env=os.environ, timeout=300)
    check(silent_run.returncode == 0, f"the silent judge does not crash the run: {silent_run.stdout} {silent_run.stderr}")
    silent_scores = json.loads((run_dir / "scores.json").read_text(encoding="utf-8"))
    silent_entry = silent_scores["scores"]["1"]
    check(silent_entry["score"] is None, f"no number means no score: {silent_entry}")
    check("consistent" not in silent_entry, f"a judge that said nothing did not agree: {silent_entry}")
    silent_summary = (run_dir / "summary.md").read_text(encoding="utf-8")
    check("judge agreed on" not in silent_summary, f"the summary does not claim agreement: {silent_summary}")
print(f"ok: {checks} checks")
