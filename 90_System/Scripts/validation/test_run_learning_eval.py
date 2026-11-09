"""Test for the learning benchmark: the scenarios, the dated setup and the run it produces.

The tutor eval is covered by test_run_tutor_eval.py. This one checks the second benchmark: the
scenarios match the Markdown table, the setup ages the learner's record with real dates, and the
runner keeps the two benchmarks apart.
"""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
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

# The token in a setup becomes a real date.
filled = mod.fill_dates("{\"occurred_at\": \"{{today-30}}\"}")
check("{{" not in filled, f"the date token is filled: {filled}")
check(mod.fill_dates("{{today-30}}") != mod.fill_dates("{{today-31}}"), "each age gives its own date")


def make_vault(base):
    root = base / "vault"
    (root / "90_System" / "Evals").mkdir(parents=True)
    (root / "90_System" / "Evals" / "learning_scenarios.json").write_text(SCENARIOS.read_text(encoding="utf-8"), encoding="utf-8")
    (root / "90_System" / "Evals" / "Learning_evals.md").write_text(markdown, encoding="utf-8")
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
print(f"ok: {checks} checks")
