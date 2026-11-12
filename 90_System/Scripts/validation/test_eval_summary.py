"""Test for the summary of run_tutor_eval.py: interval, checks, judges, contested verdict and version.

The committed runs are copied to a temp folder and summarised there, so the real run folders are
not touched. The agy run of 2026-11-09 has two judges that give the same 30 of 34 and split on
the verdict, so its run verdict is contested.
"""
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SCRIPT = REPO / "90_System" / "Scripts" / "run_tutor_eval.py"
EVALS = REPO / "90_System" / "Evals"
RUNS = EVALS / "runs"

spec = importlib.util.spec_from_file_location("run_tutor_eval", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

checks = 0


def check(condition, message):
    global checks
    assert condition, message
    checks += 1


def run(*args):
    return subprocess.run([sys.executable, "-I", str(SCRIPT), *map(str, args)], capture_output=True, text=True, timeout=300)


# The blank vault that ships on a release has no run folders, so the parts that read them are
# skipped there; in the repository they always run.
HAVE_RUNS = (RUNS / "2026-11-09-agy").is_dir()

tutor = json.loads((EVALS / "tutor_scenarios.json").read_text(encoding="utf-8"))
learning = json.loads((EVALS / "learning_scenarios.json").read_text(encoding="utf-8"))

# ---------------------------------------------------------------- the version hashes

version = mod.benchmark_version(tutor)
check(set(version) == set(mod.VERSION_KEYS) and all(len(v) == 64 for v in version.values()), version)
check(mod.benchmark_version(json.loads(json.dumps(tutor))) == version, "the same benchmark gives the same hashes")
changed = json.loads(json.dumps(tutor))
changed["scenarios"][4]["pass"] = changed["scenarios"][4]["pass"].replace("low", "lower")
moved = mod.benchmark_version(changed)
check(moved["rubric_sha256"] != version["rubric_sha256"] and moved["judge_prompt_sha256"] != version["judge_prompt_sha256"]
      and moved["scenarios_sha256"] == version["scenarios_sha256"], "one word of a Pass changes the rubric and the judge prompt")
changed = json.loads(json.dumps(tutor))
changed["scenarios"][0]["turns"][0] = "Explain it."
check(mod.benchmark_version(changed)["scenarios_sha256"] != version["scenarios_sha256"], "a learner turn changes the scenarios")
changed = json.loads(json.dumps(tutor))
changed["scenarios"][0]["checks"]["asks_confidence"] = True
check([k for k in mod.VERSION_KEYS if mod.benchmark_version(changed)[k] != version[k]] == ["checks_sha256"],
      "a check changes only the checks hash")
check(mod.benchmark_version(learning) != version, "the two benchmarks have different hashes")
check(mod.version_problems("a", version, "b", version) == ([], []), "same versions, no problem")
check(mod.version_problems("a", None, "b", version) == ([], ["a"]), "a run that records no version is named")
check(mod.version_problems("a", version, "b", moved)[0] == ["rubric differs between a and b", "judge_prompt differs between a and b"],
      mod.version_problems("a", version, "b", moved))

# ---------------------------------------------------------------- the drift check knows the checks field

broken = json.loads(json.dumps(tutor))
del broken["scenarios"][2]["checks"]
markdown = (EVALS / "Tutor_mode.md").read_text(encoding="utf-8")
check("scenario 3: no checks field" in mod.check_drift(broken, markdown), "a scenario without checks is drift")
broken["scenarios"][2]["checks"] = {"forbid_writes": ["50_Review/"], "nope": True}
check("scenario 3: unknown check 'nope'" in mod.check_drift(broken, markdown), "an unknown check is drift")

with tempfile.TemporaryDirectory() as tmp:
    base = Path(tmp)
    if HAVE_RUNS:
        for name in ("2026-11-09-agy", "2026-11-09-minimax", "2026-11-10-learning-minimax-learning-v2"):
            shutil.copytree(RUNS / name, base / name)
        agy, minimax, v2 = base / "2026-11-09-agy", base / "2026-11-09-minimax", base / "2026-11-10-learning-minimax-learning-v2"

        # ------------------------------------------------------------ summaries of the committed runs

        out = run("--summarize", agy)
        check(out.returncode == 0, out.stderr)
        check("scores.json: total 30 of 34, 95% interval 25 to 34 (n=17); verdict: fail" in out.stdout, out.stdout)
        check("scores-judge-minimax.json: total 30 of 34, 95% interval 26 to 33 (n=17); verdict: pass" in out.stdout, out.stdout)
        check("percent 0.7647, kappa 0.3131, weighted kappa 0.5072" in out.stdout, out.stdout)
        check("run verdict across 2 judges: contested" in out.stdout, out.stdout)
        check("records no hashes" in out.stdout, "a run made before the hashes says so")
        summary = (agy / "summary.md").read_text(encoding="utf-8")
        check("Verdict of the run across its 2 judges: **contested**." in summary, summary)
        check("| # | Score | Checks | Why |" in summary and "Coverage: 17 of 17 scenarios" in summary, summary)
        check("The pass mark 28 is inside it" in summary, summary)
        second = (agy / "summary-judge-minimax.md").read_text(encoding="utf-8")
        check("Verdict: **pass**." in second and "**contested**" in second, "the second judge has its own summary")
        scored = json.loads((agy / "scores.json").read_text(encoding="utf-8"))
        check(scored["run_verdict"]["run_verdict"] == "contested" and scored["interval"]["low"] == 25, scored.get("run_verdict"))

        out = run("--summarize", minimax)
        check(out.returncode == 0 and "run verdict across 2 judges: fail" in out.stdout, out.stdout + out.stderr)
        check("scenario 4: wrote 10_Tracks/01_Example_Course/Example_Course.md" in out.stdout
              and "wrote 40_References/Papers/Adaptive_Memory_Replay_(Smith_et_al.,_2024).md" in out.stdout, out.stdout)
        check("FAILED: wrote" in (minimax / "summary.md").read_text(encoding="utf-8"), "the summary shows the failed check")

        out = run("--summarize", v2)
        check(out.returncode == 0 and "Coverage: 5 of 15 scenarios" in (v2 / "summary.md").read_text(encoding="utf-8"),
              out.stdout + out.stderr)
        check("run verdict across 2 judges: fail" in out.stdout and "alpha ordinal 1.0" in out.stdout, out.stdout)

        # ------------------------------------------------------------ a recorded version is enforced

        meta = json.loads((agy / "run.json").read_text(encoding="utf-8"))
        meta["version"] = mod.benchmark_version(tutor)
        (agy / "run.json").write_text(json.dumps(meta), encoding="utf-8")
        out = run("--summarize", agy)
        check(out.returncode == 0 and "run.json records no hashes" not in out.stdout, out.stdout + out.stderr)
        meta["version"]["rubric_sha256"] = "0" * 64
        (agy / "run.json").write_text(json.dumps(meta), encoding="utf-8")
        out = run("--summarize", agy)
        check(out.returncode == 2 and "refused: rubric differs between run.json and the benchmark today" in out.stderr,
              out.stdout + out.stderr)
        out = run("--summarize", agy, "--force")
        check(out.returncode == 0 and "Forced over a version difference" in (agy / "summary.md").read_text(encoding="utf-8"),
              out.stdout + out.stderr)

        # ------------------------------------------------------------ paired difference of two runs

        out = run("--compare", agy / "scores.json", minimax / "scores-judge-kimi.json")
        check(out.returncode == 0, out.stderr)
        check("paired difference A minus B over 17 scenarios: 11" in out.stdout, out.stdout)
        check("records no version" in out.stdout, "the run with no version is named")
        out = run("--compare", agy, minimax)
        check(out.returncode == 0 and "judges of different families" in out.stdout, out.stdout + out.stderr)
        meta_b = json.loads((minimax / "run.json").read_text(encoding="utf-8"))
        meta_b["version"] = mod.benchmark_version(tutor)
        (minimax / "run.json").write_text(json.dumps(meta_b), encoding="utf-8")
        out = run("--compare", agy, minimax)
        check(out.returncode == 2 and "rubric differs" in out.stderr, out.stdout + out.stderr)
        check(run("--compare", agy, minimax, "--force").returncode == 0, "--force compares anyway")
        check(run("--compare", agy, v2).returncode == 2, "two benchmarks are not compared")

    # ------------------------------------------------------------ a new run records version and model

    vault = base / "vault"
    (vault / "90_System" / "Evals").mkdir(parents=True)
    shutil.copy(EVALS / "tutor_scenarios.json", vault / "90_System" / "Evals")
    shutil.copy(EVALS / "Tutor_mode.md", vault / "90_System" / "Evals")
    (vault / "AGENTS.md").write_text("# AGENTS.md\n", encoding="utf-8")
    agent = base / "agent.py"
    agent.write_text("import sys\nsys.stdin.read()\nopen('20_Concepts_note.md', 'w').write('x')\n"
                     "print('Guess first. How confident are you, 1 to 5?')\n", encoding="utf-8")
    judge = base / "judge.py"
    judge.write_text("import sys\nsys.stdin.read()\nprint('WHY: fine, see [[Note|Name]].')\nprint('SCORE: 2')\n", encoding="utf-8")
    out = run("--root", vault, "--date", "2026-01-02", "--label", "fake", "--scenarios", "2",
              "--agent-cmd", f"{sys.executable} {agent}", "--agent-family", "a", "--agent-model", "model-a",
              "--judge-cmd", f"{sys.executable} {judge}", "--judge-family", "b", "--judge-model", "model-b")
    check(out.returncode == 0, out.stdout + out.stderr)
    run_dir = vault / "90_System" / "Evals" / "runs" / "2026-01-02-fake"
    meta = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
    check(meta["agent_model"] == "model-a" and meta["version"] == mod.benchmark_version(tutor), meta)
    scored = json.loads((run_dir / "scores.json").read_text(encoding="utf-8"))
    check(scored["judge_model"] == "model-b" and scored["version"] == meta["version"], scored)
    check(scored["checks"] == {"2": {"passed": True, "failures": []}}, scored["checks"])
    summary_text = (run_dir / "summary.md").read_text(encoding="utf-8")
    check("[[Note\\|Name]]" in summary_text and "[[Note/Name]]" not in summary_text,
          "a pipe inside a table cell is escaped, so a wikilink in a judge reason still names its note")
    check(scored["interval"]["total"] == 2 and "Agent model: model-a" in (run_dir / "summary.md").read_text(encoding="utf-8"),
          "the summary names the models")

print(f"ok: {checks} checks")
