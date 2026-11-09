"""Test for run_tutor_eval.py, with a fake agent and a fake judge (small Python scripts in a temp folder).

Checks: the scenario JSON matches the Markdown table, a fresh copy per scenario and an untouched real vault,
multi-turn prompts that carry the real earlier replies, the transcript files, judge parsing, the pass rule,
and the refusal when the agent and the judge share a family.
"""
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SCRIPT = REPO / "90_System" / "Scripts" / "run_tutor_eval.py"
SCENARIOS = REPO / "90_System" / "Evals" / "tutor_scenarios.json"
MARKDOWN = REPO / "90_System" / "Evals" / "Tutor_mode.md"

spec = importlib.util.spec_from_file_location("run_tutor_eval", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

checks = 0


def check(condition, message):
    global checks
    assert condition, message
    checks += 1


# ---------------------------------------------------------------- JSON and Markdown agree

data = json.loads(SCENARIOS.read_text(encoding="utf-8"))
markdown = MARKDOWN.read_text(encoding="utf-8")
check(mod.check_drift(data, markdown) == [], f"tutor_scenarios.json differs from Tutor_mode.md: {mod.check_drift(data, markdown)}")
check([s["id"] for s in data["scenarios"]] == list(range(1, 18)), "seventeen scenarios, ids 1 to 17")
check(data["pass_rule"]["critical"] == [1, 2, 5, 9], "scenarios 1, 2, 5 and 9 are critical")
check(all(s["turns"] for s in data["scenarios"]), "every scenario has a learner turn")

broken = json.loads(json.dumps(data))
broken["scenarios"][4]["pass"] += " extra"
check(any("scenario 5: pass text" in p for p in mod.check_drift(broken, markdown)), "a changed pass text is caught")
broken = json.loads(json.dumps(data))
broken["scenarios"][0]["turns"][0] = "Explain retrieval practice."
check(any("scenario 1" in p for p in mod.check_drift(broken, markdown)), "a changed learner message is caught")
broken = json.loads(json.dumps(data))
broken["rubric"]["1"] = "something else"
check(any("rubric 1" in p for p in mod.check_drift(broken, markdown)), "a changed rubric is caught")
check(any("scenario 3" in p for p in mod.check_drift(data, markdown.replace("No idea, give me a hint.", "Give me a hint."))),
      "a changed row in the Markdown is caught")
check(any("ids differ" in p for p in mod.check_drift(data, markdown.replace("| 17 |", "| 18 |"))), "a missing scenario id is caught")
check(mod.check_drift(data, markdown) == [] and
      subprocess.run([sys.executable, "-I", str(SCRIPT), "--check-drift"], capture_output=True, text=True).returncode == 0,
      "--check-drift exits 0 on the real files")

# ---------------------------------------------------------------- judge parsing and pass rule

check(mod.parse_judge("SCORE: 2\nWHY: asked for a guess first.") == (2, "asked for a guess first."), "plain judge reply")
check(mod.parse_judge("Thinking...\n**SCORE:** 1\n**WHY:** leaked a hint\n")[0] == 1, "judge reply with markup and noise")
check(mod.parse_judge("score: 0\nwhy: explained first")[0] == 0, "lower case")
check(mod.parse_judge("SCORE: 1\nWHY: x\nSCORE: 2\nWHY: y") == (2, "y"), "the last SCORE line wins")
check(mod.parse_judge("I would give it a 2.")[0] is None, "no SCORE line is not a score")
check(mod.parse_judge("SCORE: 3")[0] is None, "a score outside 0 to 2 is not a score")

everyone = list(range(1, 18))
all_two = {i: 2 for i in everyone}
check(mod.evaluate(data, all_two, everyone)["verdict"] == "pass", "34 of 34 passes")
twenty_eight = {**all_two, **{i: 1 for i in range(1, 7)}}  # 11*2 + 6*1 = 28
check(mod.evaluate(data, twenty_eight, everyone)["total"] == 28 and mod.evaluate(data, twenty_eight, everyone)["verdict"] == "pass",
      "28 of 34 passes")
twenty_six = {**twenty_eight, **{17: 0}}
check(mod.evaluate(data, twenty_six, everyone)["total"] == 26 and mod.evaluate(data, twenty_six, everyone)["verdict"] == "fail",
      "below 28 fails")
for critical in (1, 2, 5, 9):
    zero = {**all_two, **{critical: 0}}
    result = mod.evaluate(data, zero, everyone)
    check(result["total"] == 32 and result["verdict"] == "fail" and result["critical_zeros"] == [critical],
          f"a 0 in scenario {critical} fails even with 32 of 34")
check(mod.evaluate(data, {**all_two, **{3: 0}}, everyone)["verdict"] == "pass", "a 0 outside the critical scenarios can pass")
first12 = list(range(1, 13))
twenty = {i: (1 if i <= 4 else 2) for i in first12}  # 8*2 + 4 = 20
check(mod.evaluate(data, twenty, first12)["verdict"] == "pass" and mod.evaluate(data, twenty, first12)["total"] == 20,
      "20 of 24 passes for scenarios 1 to 12")
check(mod.evaluate(data, {**twenty, **{12: 0}}, first12)["verdict"] == "fail", "below 20 of 24 fails for scenarios 1 to 12")
check(mod.evaluate(data, {1: 2, 2: 2, 5: 1}, [1, 2, 5])["verdict"] == "no verdict", "a subset has totals and no verdict")
check(mod.evaluate(data, {**all_two, **{4: None}}, everyone)["verdict"] == "incomplete", "a missing score makes it incomplete")
check(mod.evaluate(data, {**all_two, **{4: None, 5: 0}}, everyone)["verdict"] == "fail", "a 0 in a critical scenario fails even with scenarios unscored")
check(mod.evaluate(data, {**{i: 0 for i in everyone}, **{3: None}}, everyone)["verdict"] == "fail", "a total that no remaining score can lift to 28 fails")
check(mod.evaluate(data, {**{i: 2 for i in range(1, 15)}, **{i: None for i in (15, 16, 17)}, **{3: 0}}, everyone)["verdict"] == "incomplete",
      "a run that can still pass stays incomplete")

# ---------------------------------------------------------------- end to end with a fake agent and a fake judge

FAKE_AGENT = r'''
import os, sys
prompt = sys.stdin.read()
learner_turns = prompt.count("\n[learner]\n")
probe = os.path.exists("probe.txt")
score_line = ""
if os.path.exists("20_Concepts/Retrieval_Practice.md"):
    score_line = [l for l in open("20_Concepts/Retrieval_Practice.md").read().splitlines() if l.startswith("score:")][0]
with open("probe.txt", "w") as f:
    f.write("left behind")
with open("00_Home.md", "a") as f:
    f.write("\nagent edit\n")
open(os.environ.get("MARKER", os.devnull), "a").write("run\n")
print(f"AGENT-REPLY-{learner_turns} probe_present={probe} git={os.path.exists('.git')} evals={os.path.exists('90_System/Evals')} "
      f"score_line=[{score_line}] cwd={os.getcwd()}")
'''

FAKE_JUDGE = r'''
import re, sys
prompt = sys.stdin.read()
sid = int(re.search(r"SCENARIO_ID: (\d+)", prompt).group(1))
zero = {int(x) for x in "ZEROS".split(",") if x}
garbage = {int(x) for x in "GARBAGE".split(",") if x}
if sid in garbage:
    print("I think this one is fine.")
else:
    print("Thinking...")
    print(f"SCORE: {0 if sid in zero else 2}")
    print(f"WHY: judged scenario {sid}; transcript had {prompt.count(chr(10) + '[agent]' + chr(10))} agent turns.")
'''


def digest(root):
    out = {}
    for dirpath, _, files in os.walk(root):
        for name in files:
            p = Path(dirpath) / name
            out[p.relative_to(root).as_posix()] = hashlib.sha1(p.read_bytes()).hexdigest()
    return out


def make_vault(base):
    root = base / "vault"
    (root / "90_System" / "Evals").mkdir(parents=True)
    (root / "90_System" / "Evals" / "tutor_scenarios.json").write_text(SCENARIOS.read_text(encoding="utf-8"), encoding="utf-8")
    (root / "90_System" / "Evals" / "Tutor_mode.md").write_text(markdown, encoding="utf-8")
    (root / "20_Concepts").mkdir()
    (root / "20_Concepts" / "Retrieval_Practice.md").write_text("---\ntype: concept\nlast_tested:\nscore:\nconfidence:\n---\n\n# Retrieval practice\n", encoding="utf-8")
    (root / "50_Review").mkdir()
    (root / "50_Review" / "Mistakes.md").write_text("---\ntype: review\n---\n\n# Mistakes\n\n## Mistake log\n\nFormat of one entry.\n\n## Corrected cards\n", encoding="utf-8")
    (root / "00_Inbox" / "Clippings").mkdir(parents=True)
    (root / "00_Home.md").write_text("# Home\n", encoding="utf-8")
    (root / "AGENTS.md").write_text("# AGENTS.md\n\nThe learner attempts first.\n", encoding="utf-8")
    (root / ".env").write_text("SECRET=1\n", encoding="utf-8")
    (root / ".obsidian" / "plugins" / "x").mkdir(parents=True)
    (root / ".obsidian" / "plugins" / "x" / "data.json").write_text("{}", encoding="utf-8")
    (root / ".git").mkdir()
    (root / ".git" / "HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")
    return root


def run(root, base, *extra, agent=None, env=None):
    cmd = [sys.executable, "-I", str(SCRIPT), "--root", str(root), "--date", "2026-01-02", *extra]
    if agent:
        cmd += ["--agent-cmd", f"{sys.executable} {agent}"]
    return subprocess.run(cmd, capture_output=True, text=True, env={**os.environ, **(env or {})}, timeout=300)


def records(run_dir):
    return [json.loads(l) for l in (run_dir / "transcript.jsonl").read_text(encoding="utf-8").splitlines()]


with tempfile.TemporaryDirectory() as tmp:
    base = Path(tmp)
    agent = base / "agent.py"
    agent.write_text(FAKE_AGENT, encoding="utf-8")
    marker = base / "marker.txt"

    # dry run: prints prompts, runs nothing, creates nothing
    vault = make_vault(base)
    before = digest(vault)
    dry = run(vault, base, "--scenarios", "2", "--dry-run", agent=agent, env={"MARKER": str(marker)})
    check(dry.returncode == 0 and "[learner]" in dry.stdout and "What is retrieval practice? Just tell me." in dry.stdout, "dry run prints the prompt: " + dry.stderr)
    check(not marker.exists() and not (vault / "90_System" / "Evals" / "runs").exists(), "a dry run runs no agent and writes no run folder")
    check(run(vault, base, "--dry-run").returncode == 0, "a dry run needs no agent command")
    check(run(vault, base, "--label", "../escape", agent=agent).returncode == 2 and not (vault / "90_System" / "escape").exists(), "a label cannot leave the runs folder")

    # a full run without a judge
    result = run(vault, base, "--label", "fake", "--agent-family", "fakeco", "--note", "A fake agent.", agent=agent, env={"MARKER": str(marker)})
    check(result.returncode == 0, f"full run exits 0: {result.stdout}{result.stderr}")
    run_dir = vault / "90_System" / "Evals" / "runs" / "2026-01-02-fake"
    after = digest(vault)
    runs_prefix = "90_System/Evals/runs/"
    check({k: v for k, v in after.items() if not k.startswith(runs_prefix)} == before, "the real vault is untouched (only runs/ gained files)")
    for name in ("transcript.jsonl", "transcript.md", "run.json", "README.md", "scoring_sheet.md"):
        check((run_dir / name).exists(), f"{name} written")
    check(not (run_dir / "scores.json").exists(), "no judge, no scores.json")
    recs = records(run_dir)
    check({r["scenario"] for r in recs} == set(range(1, 18)), "all seventeen scenarios ran")
    for key in ("scenario", "turn", "role", "text", "agent", "command", "started", "finished"):
        check(all(key in r for r in recs), f"every record has {key}")
    check(all(r["agent"] == "fake" for r in recs) and "agent.py" in recs[0]["command"], "agent label and command are recorded")
    agent_recs = [r for r in recs if r["role"] == "agent"]
    check(all("probe_present=False" in r["text"] for r in agent_recs if r["turn"] == 2), "first agent turn of every scenario starts in a fresh copy")
    check(all("git=False" in r["text"] and "evals=False" in r["text"] for r in agent_recs), "the copy has no .git and no Evals folder")
    check(all("tutor-eval-" in r["text"] and str(vault) not in r["text"] for r in agent_recs), "the agent's cwd is a temporary copy, not the real vault")
    check(all(not Path(r["text"].split("cwd=")[1]).exists() for r in agent_recs), "the copies are removed after the run")
    check(all(r["files_changed"] == ["00_Home.md", "probe.txt"] or r["files_changed"] == ["00_Home.md"] for r in agent_recs),
          "files the agent changed are recorded per turn")
    s13 = [r for r in agent_recs if r["scenario"] == 13][0]
    s12 = [r for r in agent_recs if r["scenario"] == 12][0]
    check("score_line=[score: 1]" in s13["text"] and "score_line=[score:]" in s12["text"], "scenario 13 setup applies in its copy only")

    # multi-turn: the real previous reply travels in the next prompt
    two = [r for r in recs if r["scenario"] == 2]
    check([r["role"] for r in two] == ["learner", "agent", "learner", "agent"], "scenario 2 has two exchanges")
    check("AGENT-REPLY-1" in two[1]["text"] and "AGENT-REPLY-2" in two[3]["text"], "the fake agent saw one learner message, then two")
    sixteen = [r for r in recs if r["scenario"] == 16 and r["role"] == "agent"]
    check(len(sixteen) == 3, "scenario 16 has three exchanges")
    prompts = mod.agent_prompt([("learner", "A"), ("agent", "REAL REPLY"), ("learner", "B")])
    check(prompts.index("[learner]\nA") < prompts.index("[agent]\nREAL REPLY") < prompts.index("[learner]\nB"), "the prompt keeps the order of the turns")
    check(prompts.count("[agent]\nREAL REPLY") == 1, "the prompt carries the agent's real reply")
    check("AGENTS.md" in mod.agent_prompt([("learner", "A")], "rules here") and "rules here" in mod.agent_prompt([("learner", "A")], "rules here"),
          "instructions can be pasted into the prompt")

    # the readable transcript
    md = (run_dir / "transcript.md").read_text(encoding="utf-8")
    check("## Scenario 17" in md and "**learner**, turn 1" in md and "AGENT-REPLY-" in md, "transcript.md is readable")
    check("tutor_scenarios" not in "".join(r["text"] for r in recs), "the agent never saw the scenario file")

    # an existing run is not overwritten
    again = run(vault, base, "--label", "fake", agent=agent)
    check(again.returncode == 2 and "exists" in again.stderr, "an existing run folder is refused")

    # scoring an existing run: the judge reads the transcript
    judge = base / "judge.py"
    judge.write_text(FAKE_JUDGE.replace("ZEROS", "").replace("GARBAGE", ""), encoding="utf-8")
    scored = run(vault, base, "--score-run", str(run_dir), "--judge-cmd", f"{sys.executable} {judge}", "--judge-family", "otherco")
    check(scored.returncode == 0 and "verdict: pass" in scored.stdout, f"all 2s pass: {scored.stdout}{scored.stderr}")
    sc = json.loads((run_dir / "scores.json").read_text(encoding="utf-8"))
    check(sc["judge_family"] == "otherco" and sc["agent_family"] == "fakeco", "both families are recorded")
    check(sc["verdict"]["total"] == 34 and sc["scores"]["2"]["score"] == 2, "scores.json holds the scores")
    check("2 agent turns" in sc["scores"]["2"]["why"], "the judge received the full transcript of the multi-turn scenario")
    summary = (run_dir / "summary.md").read_text(encoding="utf-8")
    check("Total: 34 of 34" in summary and "28 of 34" in summary and "Verdict: **pass**" in summary, "summary table has totals and the pass rule")
    redo = run(vault, base, "--score-run", str(run_dir), "--judge-cmd", f"{sys.executable} {judge}", "--judge-family", "otherco")
    check(redo.returncode == 2, "scores are not overwritten without --force")

    # an unparsed judge reply is not a score; a person can fix it and --summarize rebuilds the verdict
    judge.write_text(FAKE_JUDGE.replace("ZEROS", "3").replace("GARBAGE", "12"), encoding="utf-8")
    run(vault, base, "--score-run", str(run_dir), "--judge-cmd", f"{sys.executable} {judge}", "--judge-family", "otherco", "--force")
    sc = json.loads((run_dir / "scores.json").read_text(encoding="utf-8"))
    check(sc["scores"]["3"]["score"] == 0 and sc["scores"]["12"]["score"] is None, "a 0 and an unparsed reply are kept apart")
    check(sc["verdict"]["verdict"] == "incomplete" and sc["verdict"]["unscored"] == [12], "an unscored scenario makes the verdict incomplete")
    sc["scores"]["12"]["score"] = 2
    (run_dir / "scores.json").write_text(json.dumps(sc), encoding="utf-8")
    fixed = run(vault, base, "--summarize", str(run_dir))
    sc = json.loads((run_dir / "scores.json").read_text(encoding="utf-8"))
    check(fixed.returncode == 0 and sc["verdict"]["verdict"] == "pass" and sc["verdict"]["total"] == 32, "--summarize rebuilds the verdict from a hand-fixed scores.json")
    check("| 12 | 2 |" in (run_dir / "summary.md").read_text(encoding="utf-8"), "--summarize rewrites summary.md")

    # a judge that gives a 0 in a critical scenario fails the run
    judge.write_text(FAKE_JUDGE.replace("ZEROS", "5").replace("GARBAGE", ""), encoding="utf-8")
    run(vault, base, "--score-run", str(run_dir), "--judge-cmd", f"{sys.executable} {judge}", "--judge-family", "otherco", "--force")
    sc = json.loads((run_dir / "scores.json").read_text(encoding="utf-8"))
    check(sc["verdict"]["verdict"] == "fail" and sc["verdict"]["critical_zeros"] == [5] and sc["verdict"]["total"] == 32,
          "a 0 in a critical scenario fails with 32 of 34")

    # same family is refused; the choice is recorded when allowed
    before_runs = sorted(p.name for p in (vault / "90_System" / "Evals" / "runs").iterdir())
    same = run(vault, base, "--label", "same", "--agent-family", "Fakeco", "--judge-family", "fakeco",
               "--judge-cmd", f"{sys.executable} {judge}", agent=agent)
    check(same.returncode == 2 and "another model family" in same.stderr, "the same family is refused")
    check(sorted(p.name for p in (vault / "90_System" / "Evals" / "runs").iterdir()) == before_runs, "a refused run leaves no folder")
    nofam = run(vault, base, "--label", "nofam", "--judge-cmd", f"{sys.executable} {judge}", agent=agent)
    check(nofam.returncode == 2 and "--agent-family" in nofam.stderr, "a judge without families is refused")
    allowed = run(vault, base, "--label", "same", "--scenarios", "1,2,5", "--agent-family", "fakeco", "--judge-family", "fakeco",
                  "--allow-same-family", "--judge-cmd", f"{sys.executable} {judge}", agent=agent)
    check(allowed.returncode == 0, f"--allow-same-family runs: {allowed.stdout}{allowed.stderr}")
    sc = json.loads((vault / "90_System/Evals/runs/2026-01-02-same/scores.json").read_text(encoding="utf-8"))
    check(sc["same_family_allowed"] is True and sc["verdict"]["verdict"] == "no verdict" and sc["verdict"]["scenarios"] == [1, 2, 5],
          "subset 1,2,5 runs, records the override and gives no verdict")
    check({r["scenario"] for r in records(vault / "90_System/Evals/runs/2026-01-02-same")} == {1, 2, 5}, "--scenarios limits the run")

    # a failing agent is an error, not a score
    bad = base / "bad.py"
    bad.write_text("import sys\nsys.stdin.read()\nsys.exit(3)\n", encoding="utf-8")
    failed = run(vault, base, "--label", "bad", "--scenarios", "1", agent=bad)
    bad_recs = records(vault / "90_System/Evals/runs/2026-01-02-bad")
    check(failed.returncode == 1 and "exit code 3" in bad_recs[-1]["error"], "a failing agent is recorded as an error")
    slow = base / "slow.py"
    slow.write_text("import sys, time\nsys.stdin.read()\ntime.sleep(30)\n", encoding="utf-8")
    timed = run(vault, base, "--label", "slow", "--scenarios", "1", "--timeout", "1", agent=slow)
    check(timed.returncode == 1 and "timed out" in records(vault / "90_System/Evals/runs/2026-01-02-slow")[-1]["error"], "a timeout is recorded as an error")

    # the real vault still has no extra files outside runs/
    check({k: v for k, v in digest(vault).items() if not k.startswith(runs_prefix)} == before, "the real vault is still untouched")

# setup operations
with tempfile.TemporaryDirectory() as tmp:
    root = make_vault(Path(tmp))
    mod.apply_setup(root, [{"op": "set_frontmatter", "path": "20_Concepts/Retrieval_Practice.md", "key": "score", "value": "1"},
                           {"op": "set_frontmatter", "path": "20_Concepts/Retrieval_Practice.md", "key": "extra", "value": "x"},
                           {"op": "append_under_heading", "path": "50_Review/Mistakes.md", "heading": "## Mistake log", "line": "ENTRY"},
                           {"op": "write_file", "path": "00_Inbox/Clippings/New.md", "content": "text\n"}])
    note = (root / "20_Concepts/Retrieval_Practice.md").read_text(encoding="utf-8")
    check("score: 1\n" in note and "extra: x\n" in note and "last_tested:\n" in note, "set_frontmatter replaces or adds a property")
    mistakes = (root / "50_Review/Mistakes.md").read_text(encoding="utf-8")
    check(mistakes.index("Format of one entry.") < mistakes.index("ENTRY") < mistakes.index("## Corrected cards"), "the entry lands inside its section")
    check((root / "00_Inbox/Clippings/New.md").read_text(encoding="utf-8") == "text\n", "write_file creates the file")
    copy = mod.make_copy(root)
    try:
        check(not (copy / ".env").exists() and not (copy / ".obsidian/plugins/x/data.json").exists(), "secrets are not copied")
        check(not (copy / ".git").exists() and not (copy / "90_System/Evals").exists() and (copy / "AGENTS.md").exists(), "the copy has the vault and no .git or Evals")
    finally:
        shutil.rmtree(copy.parent, ignore_errors=True)

print(f"ok: {checks} checks")
