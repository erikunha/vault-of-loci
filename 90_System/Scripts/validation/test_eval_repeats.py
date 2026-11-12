"""Test for the repeats of run_tutor_eval.py: --agent-repeats, --judge-name and --aggregate.

A fake agent and a fake judge (small Python scripts) stand in for the models, so no quota is
spent. The judge gives a score that depends on the run folder, so the repeats differ the way
real repeats do.
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

spec = importlib.util.spec_from_file_location("run_tutor_eval", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

checks = 0


def check(condition, message):
    global checks
    assert condition, message
    checks += 1


# ---------------------------------------------------------------- pass^k by hand

T, F = True, False
trials = [[T, T, T], [T, F, T], [F, F, F]]
# One scenario always succeeds, one succeeds 2 times in 3, one never: C(c, k) / C(3, k), then the mean.
check(mod.pass_hat_k(trials, 1) == round((1 + 2 / 3 + 0) / 3, 4), mod.pass_hat_k(trials, 1))
check(mod.pass_hat_k(trials, 2) == round((1 + 1 / 3 + 0) / 3, 4), mod.pass_hat_k(trials, 2))
check(mod.pass_hat_k(trials, 3) == round(1 / 3, 4), mod.pass_hat_k(trials, 3))
check(mod.pass_hat_k(trials, 4) is None and mod.pass_hat_k([], 1) is None, "k above the trials gives nothing")

AGENT = "import sys\nsys.stdin.read()\nprint('Guess first. How confident are you, 1 to 5?')\n"
# The judge gives 2, except scenario 2 when BAD is set, which gets a 0.
JUDGE = '''import os, re, sys
prompt = sys.stdin.read()
sid = int(re.search(r"SCENARIO_ID: (\\d+)", prompt).group(1))
score = int(os.environ.get("SCORE", "2"))
if sid == 2 and os.environ.get("BAD"):
    score = 0
print("WHY: fake.")
print(f"SCORE: {score}")
'''


def run(root, *args, env=None):
    import os
    return subprocess.run([sys.executable, "-I", str(SCRIPT), "--root", str(root), "--date", "2026-01-02", *map(str, args)],
                          capture_output=True, text=True, timeout=300, env={**os.environ, **(env or {})})


with tempfile.TemporaryDirectory() as tmp:
    base = Path(tmp)
    vault = base / "vault"
    (vault / "90_System" / "Evals").mkdir(parents=True)
    shutil.copy(EVALS / "tutor_scenarios.json", vault / "90_System" / "Evals")
    shutil.copy(EVALS / "Tutor_mode.md", vault / "90_System" / "Evals")
    (vault / "AGENTS.md").write_text("# AGENTS.md\n", encoding="utf-8")
    # The files the setup of scenarios 11 and 13 edits.
    (vault / "20_Concepts").mkdir()
    (vault / "20_Concepts" / "Retrieval_Practice.md").write_text("---\ntype: concept\nscore:\n---\n\n# Retrieval practice\n",
                                                                 encoding="utf-8")
    (vault / "50_Review").mkdir()
    (vault / "50_Review" / "Mistakes.md").write_text("---\ntype: review\n---\n\n# Mistakes\n\n## Mistake log\n\n## Corrected cards\n",
                                                     encoding="utf-8")
    (vault / "00_Inbox" / "Clippings").mkdir(parents=True)
    agent, judge = base / "agent.py", base / "judge.py"
    agent.write_text(AGENT, encoding="utf-8")
    judge.write_text(JUDGE, encoding="utf-8")
    runs = vault / "90_System" / "Evals" / "runs"

    # ------------------------------------------------------------ three repeats, judged
    out = run(vault, "--label", "fake", "--scenarios", "1-17", "--agent-repeats", "3",
              "--agent-cmd", f"{sys.executable} {agent}", "--agent-family", "a", "--agent-model", "m",
              "--judge-cmd", f"{sys.executable} {judge}", "--judge-family", "b")
    check(out.returncode == 0, out.stdout + out.stderr)
    folders = [runs / f"2026-01-02-fake-r{n}" for n in (1, 2, 3)]
    check(all((f / "scores.json").exists() for f in folders), "every repeat has its folder and scores")
    meta = json.loads((folders[1] / "run.json").read_text(encoding="utf-8"))
    check(meta["repeat"] == 2 and meta["repeats"] == 3 and meta["label"] == "fake-r2", meta)
    check("aggregate of the repeats:" in out.stdout and "mean total 34" in out.stdout and "pass^3 1.0" in out.stdout,
          out.stdout)

    # an existing folder stops every repeat before the first one runs
    again = run(vault, "--label", "fake", "--agent-repeats", "2", "--agent-cmd", f"{sys.executable} {agent}")
    check(again.returncode == 2 and "exists" in again.stderr, again.stderr)
    check(run(vault, "--label", "x", "--agent-repeats", "0", "--agent-cmd", "true").returncode == 2, "zero repeats is refused")

    # ------------------------------------------------------------ a named second judge
    out = run(vault, "--score-run", folders[0], "--judge-cmd", f"{sys.executable} {judge}", "--judge-family", "c",
              "--judge-name", "c", env={"BAD": "1"})
    check(out.returncode == 0, out.stdout + out.stderr)
    second = json.loads((folders[0] / "scores-judge-c.json").read_text(encoding="utf-8"))
    check(second["scores"]["2"]["score"] == 0 and second["judge_family"] == "c", second["scores"]["2"])
    first = json.loads((folders[0] / "scores.json").read_text(encoding="utf-8"))
    check(first["scores"]["2"]["score"] == 2, "the first judge's file is untouched")
    check("run verdict across 2 judges: contested" in out.stdout, out.stdout)
    check((folders[0] / "summary-judge-c.md").exists(), "the named judge has its own summary")
    check(run(vault, "--score-run", folders[0], "--judge-cmd", "true", "--judge-family", "c",
              "--judge-name", "c").returncode == 2, "a named judge does not overwrite its file without --force")
    check(run(vault, "--score-run", folders[0], "--judge-cmd", "true", "--judge-family", "c",
              "--judge-name", "../x").returncode == 2, "a judge name cannot leave the folder")
    for f in folders[1:]:
        run(vault, "--score-run", f, "--judge-cmd", f"{sys.executable} {judge}", "--judge-family", "c", "--judge-name", "c")

    # ------------------------------------------------------------ aggregate over the named judge
    out = run(vault, "--aggregate", *folders, "--judge-name", "c")
    check(out.returncode == 0, out.stdout + out.stderr)
    check("totals" not in out.stderr and "fake-r1: total 32 of 34; verdict fail" in out.stdout, out.stdout)
    check("mean total 33.33, standard deviation 1.15, lowest 32, highest 34" in out.stdout, out.stdout)
    check("verdicts: fail 1, pass 2" in out.stdout, out.stdout)
    # Scenario 2 scored 2 in two runs of three: pass^1 = (16 + 2/3) / 17, pass^3 = 16 / 17.
    check(f"pass^1 {round((16 + 2 / 3) / 17, 4)}" in out.stdout and f"pass^3 {round(16 / 17, 4)}" in out.stdout, out.stdout)
    check("critical scenarios 1, 2, 5, 9 with no 0 in every one of k runs: k=1 0.9167, k=2 0.8333, k=3 0.75" in out.stdout,
          out.stdout)
    check("scenarios whose score changed between runs: 2" in out.stdout, out.stdout)

    # a version that differs is refused, unless forced
    meta = json.loads((folders[2] / "run.json").read_text(encoding="utf-8"))
    meta["version"]["rubric_sha256"] = "0" * 64
    (folders[2] / "run.json").write_text(json.dumps(meta), encoding="utf-8")
    out = run(vault, "--aggregate", *folders)
    check(out.returncode == 2 and "rubric differs" in out.stderr, out.stdout + out.stderr)
    check(run(vault, "--aggregate", *folders, "--force").returncode == 0, "--force aggregates anyway")
    check(run(vault, "--aggregate", folders[0], base).returncode == 1, "a folder with no run.json is refused")

print(f"ok: {checks} checks")
