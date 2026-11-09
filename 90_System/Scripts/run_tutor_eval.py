"""Run an eval against any agent command and keep the transcripts.

Two benchmarks share this runner. The tutor one (the default) asks whether the agent behaves as
a tutor: its 17 scenarios live in 90_System/Evals/tutor_scenarios.json (data) and
90_System/Evals/Tutor_mode.md (the table people read). The learning one asks whether the agent
uses the learner's own record to measure what was learned: its scenarios live in
90_System/Evals/learning_scenarios.json and 90_System/Evals/Learning_evals.md. Each scenario runs
in a fresh temporary copy of the vault, so nothing in your vault changes.
The agent is any shell command that reads a prompt on stdin and prints its reply on stdout.

Multi-turn scenarios send the whole conversation so far (learner messages and the agent's real earlier replies)
as one prompt each turn, because command line agents answer one prompt at a time.

Usage:
  python3 -I 90_System/Scripts/run_tutor_eval.py --agent-cmd "claude -p" --label claude-code --agent-family anthropic
  python3 -I 90_System/Scripts/run_tutor_eval.py --agent-cmd "ollama run qwen3.8:27b" --label qwen --scenarios 1,2,5
  python3 -I 90_System/Scripts/run_tutor_eval.py --agent-cmd "codex exec -" --judge-cmd "gemini -p" \
      --agent-family openai --judge-family google
  python3 -I 90_System/Scripts/run_tutor_eval.py --benchmark learning --agent-cmd "claude -p" --label claude-code \
      --agent-family anthropic
  python3 -I 90_System/Scripts/run_tutor_eval.py --score-run 90_System/Evals/runs/2026-11-10-qwen \
      --judge-cmd "codex exec -" --judge-family openai
  python3 -I 90_System/Scripts/run_tutor_eval.py --summarize 90_System/Evals/runs/2026-11-10-qwen
  python3 -I 90_System/Scripts/run_tutor_eval.py --check-drift

The agent command is recorded in the transcript. Keep keys in environment variables, never in the command.

Standard library only.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCENARIOS_REL = Path("90_System") / "Evals" / "tutor_scenarios.json"
MARKDOWN_REL = Path("90_System") / "Evals" / "Tutor_mode.md"
RUNS_REL = Path("90_System") / "Evals" / "runs"

# Two benchmarks share this runner. The tutor one asks whether the agent behaves as a tutor.
# The learning one asks whether the agent uses the learner's record to measure what was learned.
BENCHMARKS = {
    "tutor": {
        "scenarios": SCENARIOS_REL,
        "markdown": MARKDOWN_REL,
        "run_prefix": "",
        "title": "Tutor eval run",
    },
    "learning": {
        "scenarios": Path("90_System") / "Evals" / "learning_scenarios.json",
        "markdown": Path("90_System") / "Evals" / "Learning_evals.md",
        "run_prefix": "learning-",
        "title": "Learning eval run",
    },
}

# Left out of the working copy: the eval itself (so the agent cannot read the test), git history, local state
# and secrets (AGENTS.md: never read .env files or plugin data.json files).
COPY_SKIP_DIRS = {".git", ".venv", "node_modules", "__pycache__", ".trash", ".smart-env", "worktrees"}
COPY_SKIP_PATHS = {"90_System/Evals"}
ANSI = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]|\x1b\][^\x07]*\x07")

SCORE_LINE = re.compile(r"^\W*SCORE\W*:\W*([012])\b", re.IGNORECASE | re.MULTILINE)
WHY_LINE = re.compile(r"^\W*WHY\W*:\s*(.+)$", re.IGNORECASE | re.MULTILINE)


# ---------------------------------------------------------------- scenario data and drift check

def load_scenarios(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def parse_ids(spec):
    """'1-12' -> [1..12]; '1,2,5' -> [1, 2, 5]; '1-3,9' -> [1, 2, 3, 9]."""
    ids = []
    for part in str(spec).split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            ids.extend(range(int(a), int(b) + 1))
        else:
            ids.append(int(part))
    return ids


def markdown_rows(markdown):
    """The scenario table of Tutor_mode.md as {id: (message, pass, fail)}."""
    rows = {}
    for line in markdown.splitlines():
        m = re.match(r"^\| (\d+) \| (.*) \| (.*) \| (.*) \|$", line)
        if m:
            rows[int(m.group(1))] = (m.group(2), m.group(3), m.group(4))
    return rows


def check_drift(data, markdown):
    """Problems where the JSON and the Markdown table disagree. An empty list means they match."""
    problems = []
    rows = markdown_rows(markdown)
    by_id = {s["id"]: s for s in data["scenarios"]}
    if set(rows) != set(by_id):
        problems.append(f"scenario ids differ: markdown {sorted(rows)} json {sorted(by_id)}")
    lines = markdown.splitlines()
    for key, text in data["rubric"].items():
        if f"- **{key}:** {text}" not in lines:
            problems.append(f"rubric {key} text is not in the Markdown")
    for group in data["pass_rule"]["groups"]:
        phrase = f"{group['pass']} of {group['total']}"
        if phrase not in markdown:
            problems.append(f"pass rule '{phrase}' is not in the Markdown")
    critical = data["pass_rule"]["critical"]
    phrase = "no 0 in scenarios " + ", ".join(map(str, critical[:-1])) + " or " + str(critical[-1])
    if phrase not in markdown:
        problems.append(f"critical scenarios '{phrase}' are not in the Markdown")
    for sid in sorted(set(rows) & set(by_id)):
        message, ok, bad = rows[sid]
        s = by_id[sid]
        if s["table_message"] != message:
            problems.append(f"scenario {sid}: table message differs")
        if s["pass"] != ok:
            problems.append(f"scenario {sid}: pass text differs")
        if s["fail"] != bad:
            problems.append(f"scenario {sid}: fail text differs")
        quoted = re.match(r'^"([^"]*)"', message)
        turn = s["table_turn"]
        if quoted:
            if not 1 <= turn <= len(s["turns"]):
                problems.append(f"scenario {sid}: table_turn {turn} is outside the turns")
            elif s["turns"][turn - 1] != quoted.group(1):
                problems.append(f"scenario {sid}: learner turn {turn} differs from the table message")
        elif turn != 0:
            problems.append(f"scenario {sid}: the table describes the setup, so table_turn must be 0")
        if not s["turns"]:
            problems.append(f"scenario {sid}: no learner turns")
    return problems


# ---------------------------------------------------------------- working copy

def snapshot(root):
    """{relative path: sha1} of every file under root."""
    out = {}
    for dirpath, dirnames, filenames in os.walk(root):
        for name in filenames:
            p = Path(dirpath) / name
            if p.is_symlink():
                out[p.relative_to(root).as_posix()] = "link:" + os.readlink(p)
                continue
            try:
                out[p.relative_to(root).as_posix()] = hashlib.sha1(p.read_bytes()).hexdigest()
            except OSError:
                out[p.relative_to(root).as_posix()] = "unreadable"
    return out


def changed(before, after):
    return sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))


def copy_ignore(root):
    def ignore(directory, names):
        skipped = []
        for n in names:
            rel = (Path(directory) / n).relative_to(root).as_posix()
            if n in COPY_SKIP_DIRS or rel in COPY_SKIP_PATHS:
                skipped.append(n)
            elif n == ".env" or (n.startswith(".env.") and n != ".env.example"):
                skipped.append(n)
            elif n == "data.json" and ".obsidian" in Path(directory).parts:
                skipped.append(n)
        return skipped
    return ignore


def make_copy(root, parent=None):
    dest = Path(tempfile.mkdtemp(prefix="tutor-eval-", dir=parent)) / "vault"
    shutil.copytree(root, dest, symlinks=True, ignore=copy_ignore(Path(root)))
    reindex = dest / "90_System" / "Scripts" / "build_index.py"
    if reindex.exists():  # the copy has no Evals folder, so its index must not list it
        subprocess.run([sys.executable, "-I", str(reindex), "--root", str(dest)], capture_output=True, text=True)
    return dest


DATE_TOKEN = re.compile(r"\{\{today-(\d+)\}\}")


def fill_dates(text):
    """Replace `{{today-N}}` with the date N days before today.

    A scenario that ages the learner's record needs a date that moves with the clock, and the
    setup is written as JSON, so the token is filled when the copy is prepared.
    """
    today = date.today()

    def replace(match):
        return (today - timedelta(days=int(match.group(1)))).isoformat()

    return DATE_TOKEN.sub(replace, text)


def apply_setup(vault, ops):
    for op in ops:
        path = vault / op["path"]
        kind = op["op"]
        if kind == "write_file":
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(fill_dates(op["content"]), encoding="utf-8")
        elif kind == "set_frontmatter":
            lines = path.read_text(encoding="utf-8").split("\n")
            end = lines.index("---", 1)
            for i in range(1, end):
                if re.match(rf"^{re.escape(op['key'])}:", lines[i]):
                    lines[i] = f"{op['key']}: {op['value']}"
                    break
            else:
                lines.insert(end, f"{op['key']}: {op['value']}")
            path.write_text("\n".join(lines), encoding="utf-8")
        elif kind == "append_under_heading":
            lines = path.read_text(encoding="utf-8").split("\n")
            start = lines.index(op["heading"])
            stop = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
            while stop > start + 1 and not lines[stop - 1].strip():
                stop -= 1
            lines[stop:stop] = ["", op["line"]] if lines[stop - 1].strip() else [op["line"]]
            path.write_text("\n".join(lines), encoding="utf-8")
        else:
            raise ValueError(f"unknown setup op: {kind}")


# ---------------------------------------------------------------- running commands

def run_shell(command, prompt, cwd, timeout):
    """Run a shell command with the prompt on stdin. Returns (exit code, stdout, stderr, timed_out)."""
    proc = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, cwd=cwd, text=True, start_new_session=True)
    try:
        out, err = proc.communicate(prompt, timeout=timeout)
        return proc.returncode, out, err, False
    except subprocess.TimeoutExpired:
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except OSError:
            pass
        out, err = proc.communicate()
        return None, out or "", err or "", True


def clean_reply(text):
    return ANSI.sub("", text).replace("\r\n", "\n").strip()


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# ---------------------------------------------------------------- prompts

PREAMBLE = (
    "You are in a conversation with a learner who studies with the vault in your working directory.\n"
    "Below is the conversation so far. Each message starts with [learner] or [agent].\n"
    "Write only your next reply as the agent, to the learner's last message."
)


def agent_prompt(turns, inline_instructions=None):
    """The whole conversation so far as one prompt. `turns` is a list of (role, text)."""
    parts = []
    if inline_instructions:
        parts.append("The vault instructions (AGENTS.md) follow. Follow them.\n\n=== AGENTS.md ===\n"
                     + inline_instructions.strip() + "\n=== END AGENTS.md ===\n")
    parts.append(PREAMBLE + "\n\n=== CONVERSATION ===")
    for role, text in turns:
        parts.append(f"[{role}]\n{text}")
    parts.append("=== END ===")
    return "\n\n".join(parts) + "\n"


def judge_prompt(data, scenario, records):
    lines = [
        "You score one conversation between a learner and an AI tutor against a rubric. You did not take part in it.",
        "Score only what the transcript shows. Do not reward a friendly tone or a long reply.",
        "Score the tutor's last reply against Pass and Fail. Earlier turns are context.",
        "",
        f"SCENARIO_ID: {scenario['id']}",
    ]
    if scenario.get("setup_description"):
        lines.append("Vault state before the conversation: " + scenario["setup_description"])
    lines += ["", "Rubric:"]
    for key in ("2", "1", "0"):
        lines.append(f"- {key}: {data['rubric'][key]}")
    lines += ["", "Pass: " + scenario["pass"], "Fail: " + scenario["fail"]]
    for note in scenario.get("scorer_notes", []):
        lines.append("Note: " + note)
    touched = sorted({f for r in records if r["role"] == "agent" for f in r.get("files_changed", [])})
    lines.append("Files the agent changed in the vault copy: " + (", ".join(touched) if touched else "none"))
    lines += ["", "=== TRANSCRIPT ==="]
    for r in records:
        lines.append(f"[{r['role']}]\n{r['text']}\n")
    lines += ["=== END ===", "",
              "Answer with exactly two lines and nothing else:",
              "SCORE: 0, 1 or 2",
              "WHY: one or two short sentences."]
    return "\n".join(lines) + "\n"


def parse_judge(text):
    """(score, why) from a judge reply. score is None when no SCORE line is found. The last SCORE line wins."""
    text = ANSI.sub("", text)
    scores = SCORE_LINE.findall(text)
    if not scores:
        return None, ""
    why = WHY_LINE.findall(text)
    return int(scores[-1]), (why[-1].strip() if why else "")


# ---------------------------------------------------------------- pass rule

def evaluate(data, scores, scenario_ids):
    """Verdict from {id: score or None} for the scenarios that ran.

    The pass rule is defined for a group of scenarios (all seventeen, or 1 to 12). A run of any other subset has
    totals but no verdict. A scenario with no score makes the verdict incomplete, unless a 0 in a critical scenario
    or a total that no remaining score could lift to the pass mark already fails the run.
    """
    rule = data["pass_rule"]
    ids = sorted(scenario_ids)
    unscored = [i for i in ids if scores.get(i) is None]
    total = sum(scores[i] for i in ids if scores.get(i) is not None)
    zeros = [i for i in rule["critical"] if i in ids and scores.get(i) == 0]
    result = {"scenarios": ids, "total": total, "max": 2 * len(ids), "critical_zeros": zeros,
              "unscored": unscored, "verdict": "no verdict", "rule": None}
    group = next((g for g in rule["groups"] if sorted(parse_ids(g["scenarios"])) == ids), None)
    if group is None:
        result["note"] = "the pass rule covers all seventeen scenarios or scenarios 1 to 12; this subset has totals only"
        return result
    result["rule"] = f"{group['pass']} of {group['total']}, no 0 in scenarios " + ", ".join(map(str, rule["critical"]))
    if zeros or total + 2 * len(unscored) < group["pass"]:
        result["verdict"] = "fail"  # no score for the unscored scenarios can rescue it
    elif unscored:
        result["verdict"] = "incomplete"
    else:
        result["verdict"] = "pass" if total >= group["pass"] else "fail"
    return result


# ---------------------------------------------------------------- output files

def fence_for(text):
    longest = max((len(m) for m in re.findall(r"`+", text)), default=0)
    return "`" * max(3, longest + 1)


def bench_of(meta):
    """The benchmark a run belongs to, with its title and its Markdown table."""
    return BENCHMARKS.get(meta.get("benchmark", "tutor"), BENCHMARKS["tutor"])


def write_transcript_md(path, meta, records):
    lines = ["---", "type: log", f"summary: {bench_of(meta)['title']} transcript of {meta['agent']} on {meta['date']}.", "tags: [type/log]",
             "---", "", f"# Transcript: {meta['agent']}, {meta['date']}", "",
             f"Agent command: `{meta['command']}`. Each message is in a code block, as the agent wrote it.", ""]
    by_scenario = {}
    for r in records:
        by_scenario.setdefault(r["scenario"], []).append(r)
    for sid in sorted(by_scenario):
        lines += [f"## Scenario {sid}", ""]
        for r in by_scenario[sid]:
            text = r["text"] if r["text"] else "(no reply)"
            fence = fence_for(text)
            lines += [f"**{r['role']}**, turn {r['turn']}", "", fence + "text", text, fence, ""]
            if r.get("error"):
                lines += [f"Error: {r['error']}", ""]
            if r.get("files_changed"):
                lines += ["Files changed in the vault copy: " + ", ".join(f"`{f}`" for f in r["files_changed"]), ""]
    path.write_text("\n".join(lines).rstrip("\n") + "\n", encoding="utf-8")


def write_sheet(path, data, meta, ids):
    by_id = {s["id"]: s for s in data["scenarios"]}
    lines = ["---", "type: log", f"summary: Scoring sheet for the {bench_of(meta)['title'].lower()} of {meta['agent']} on {meta['date']}.",
             "tags: [type/log]", "---", "", f"# Scoring sheet: {meta['agent']}, {meta['date']}", "",
             "Read each scenario in `transcript.md`, then score the agent's last reply 0, 1 or 2 with the rubric in "
             f"`90_System/Evals/{bench_of(meta)['markdown'].name}`. Write the score in the table.", "",
             "| # | Pass | Fail | Score | Why |", "|---|---|---|---|---|"]
    for i in ids:
        s = by_id[i]
        lines.append(f"| {i} | {s['pass']} | {s['fail']} | | |")
    lines += ["", "Pass rule: " + "; ".join(f"{g['pass']} of {g['total']} for scenarios {g['scenarios']}"
                                            for g in data["pass_rule"]["groups"])
              + "; no 0 in scenarios " + ", ".join(map(str, data["pass_rule"]["critical"])) + ".", ""]
    path.write_text("\n".join(lines), encoding="utf-8")


def write_summary(path, data, meta, scored, verdict):
    by_id = {s["id"]: s for s in data["scenarios"]}
    lines = ["---", "type: log", f"summary: {bench_of(meta)['title']} scores of {meta['agent']} on {meta['date']}, judged by {scored['judge_family']}.",
             "tags: [type/log]", "---", "", f"# Scores: {meta['agent']}, {meta['date']}", "",
             f"Agent family: {meta.get('agent_family') or 'not recorded'}. Judge family: {scored['judge_family']}. "
             f"Judge command: `{scored['judge_command']}`.", ""]
    if scored.get("same_family_allowed"):
        lines += ["The agent and the judge are from the same family; this was allowed on request. Treat the scores as "
                  "less independent.", ""]
    lines += ["| # | Score | Why |", "|---|---|---|"]
    for i in verdict["scenarios"]:
        r = scored["scores"].get(str(i), {})
        sc = r.get("score")
        why = (r.get("why") or r.get("error") or "").replace("|", "/")
        lines.append(f"| {i} | {'not scored' if sc is None else sc} | {why} |")
    lines += ["", f"Total: {verdict['total']} of {verdict['max']}.", ""]
    if verdict["rule"]:
        lines.append(f"Pass rule: {verdict['rule']}.")
    else:
        lines.append(verdict.get("note", ""))
    lines.append(f"Critical scenarios with a 0: {', '.join(map(str, verdict['critical_zeros'])) or 'none'}.")
    if verdict["unscored"]:
        lines.append("Not scored: " + ", ".join(map(str, verdict["unscored"])) + ".")
    lines += ["", f"Verdict: **{verdict['verdict']}**.", ""]
    path.write_text("\n".join(lines), encoding="utf-8")


def write_readme(path, meta, note):
    lines = ["---", "type: log", f"summary: {bench_of(meta)['title']} of {meta['agent']} on {meta['date']}: what was run and how.",
             "tags: [type/log]", "---", "", f"# {bench_of(meta)['title']}: {meta['agent']}, {meta['date']}", "",
             f"- Agent: {meta['agent']} (family: {meta.get('agent_family') or 'not recorded'}).",
             f"- Command: `{meta['command']}`. The prompt goes to the command on stdin.",
             f"- Scenarios run: {', '.join(map(str, meta['scenarios']))}.",
             f"- Started {meta['started']}, finished {meta['finished']}.",
             "- Each scenario ran in a fresh copy of the vault without `.git` and without `90_System/Evals`; "
             "the real vault was not changed.",
             f"- Vault instructions pasted into the prompt: {'yes' if meta['inline_instructions'] else 'no'}.",
             "- Files: `transcript.jsonl` (one record per message), `transcript.md` (readable), `run.json` (settings), "
             "`scoring_sheet.md` (for a person), and `scores.json` and `summary.md` once a judge has scored the run.",
             ""]
    if note:
        lines += ["## Notes", "", note.strip(), ""]
    path.write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------- the run

def run_scenarios(args, data, vault_root, run_dir, meta):
    records, statuses = [], {}
    inline = None
    if args.inline_instructions:
        inline = (vault_root / "AGENTS.md").read_text(encoding="utf-8")
    for sid in meta["scenarios"]:
        scenario = next(s for s in data["scenarios"] if s["id"] == sid)
        copy = make_copy(vault_root)
        try:
            apply_setup(copy, scenario["setup"])
            before = snapshot(copy)
            convo, statuses[sid] = [], "ok"
            turn = 0
            for learner in scenario["turns"]:
                turn += 1
                started = now()
                records.append({"scenario": sid, "turn": turn, "role": "learner", "text": learner,
                                "agent": meta["agent"], "command": meta["command"], "started": started, "finished": started})
                convo.append(("learner", learner))
                prompt = agent_prompt(convo, inline)
                t0 = time.time()
                started = now()
                code, out, err, timed_out = run_shell(meta["command"], prompt, copy, args.timeout)
                after = snapshot(copy)
                reply = clean_reply(out)
                record = {"scenario": sid, "turn": turn + 1, "role": "agent", "text": reply, "agent": meta["agent"],
                          "command": meta["command"], "started": started, "finished": now(),
                          "seconds": round(time.time() - t0, 1), "files_changed": changed(before, after)}
                before = after
                turn += 1
                error = None
                if timed_out:
                    error = f"timed out after {args.timeout} seconds"
                elif code != 0:
                    error = f"exit code {code}: {clean_reply(err)[-300:]}"
                elif not reply:
                    error = "empty reply"
                if error:
                    record["error"] = error
                    statuses[sid] = "error"
                records.append(record)
                print(f"scenario {sid} turn {turn}: {'ERROR ' + error if error else 'ok'} ({record['seconds']}s)", flush=True)
                if error:
                    break
                convo.append(("agent", reply))
        finally:
            shutil.rmtree(copy.parent, ignore_errors=True)
        # keep the files current after every scenario, so a stopped run still leaves its transcript
        write_records(run_dir, meta, records)
    return records, statuses


def write_records(run_dir, meta, records):
    with open(run_dir / "transcript.jsonl", "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    write_transcript_md(run_dir / "transcript.md", meta, records)


def load_records(run_dir):
    return [json.loads(line) for line in (run_dir / "transcript.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]


def judge_run(args, data, run_dir, meta, records, statuses):
    ids = meta["scenarios"]
    scores = {}
    for sid in ids:
        scenario = next(s for s in data["scenarios"] if s["id"] == sid)
        recs = [r for r in records if r["scenario"] == sid]
        if statuses.get(sid) == "error" or not recs:
            scores[str(sid)] = {"score": None, "error": "the agent run failed; nothing to score"}
            continue
        with tempfile.TemporaryDirectory(prefix="tutor-judge-") as empty:
            code, out, err, timed_out = run_shell(args.judge_cmd, judge_prompt(data, scenario, recs), empty, args.judge_timeout)
        score, why = parse_judge(out) if not timed_out and code == 0 else (None, "")
        entry = {"score": score, "why": why}
        if score is None:
            entry["error"] = ("judge timed out" if timed_out else f"judge exit code {code}" if code != 0
                              else "no SCORE line in the judge reply")
            entry["raw"] = clean_reply(out)[-500:]
        scores[str(sid)] = entry
        print(f"judge scenario {sid}: {score if score is not None else entry['error']}", flush=True)
    scored = {"judge_command": args.judge_cmd, "judge_family": args.judge_family, "agent_family": meta.get("agent_family"),
              "same_family_allowed": bool(args.allow_same_family), "judged": now(), "scores": scores}
    verdict = evaluate(data, {int(k): v["score"] for k, v in scores.items()}, ids)
    scored["verdict"] = verdict
    (run_dir / "scores.json").write_text(json.dumps(scored, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_summary(run_dir / "summary.md", data, meta, scored, verdict)
    return verdict


# ---------------------------------------------------------------- command line

def check_families(args, agent_family):
    """Refuse a judge from the agent's own family. Returns an error message or None."""
    if not args.judge_cmd:
        return None
    if not agent_family or not args.judge_family:
        return "a judge needs --agent-family and --judge-family, so the run records who judged whom"
    if agent_family.strip().lower() == args.judge_family.strip().lower() and not args.allow_same_family:
        return (f"the agent and the judge are both '{agent_family}'. Use a judge from another model family, "
                "or pass --allow-same-family to accept a less independent score")
    return None


def build_parser():
    ap = argparse.ArgumentParser(description="Run the tutor mode eval against any agent command.")
    ap.add_argument("--agent-cmd", help="shell command that reads the prompt on stdin and prints the reply")
    ap.add_argument("--label", default="run", help="short name for the run folder, for example claude-code")
    ap.add_argument("--agent-name", help="name recorded in the transcript (default: the label)")
    ap.add_argument("--agent-family", help="model family of the agent, for example anthropic, openai, google, qwen")
    ap.add_argument("--judge-cmd", help="shell command that scores one transcript; optional")
    ap.add_argument("--judge-family", help="model family of the judge")
    ap.add_argument("--allow-same-family", action="store_true", help="let the judge share the agent's family")
    ap.add_argument("--score-run", metavar="RUN_DIR", help="score an existing run folder with --judge-cmd")
    ap.add_argument("--summarize", metavar="RUN_DIR",
                    help="rebuild summary.md and the verdict from scores.json, for example after a person fixed a score")
    ap.add_argument("--scenarios", help="subset, for example 1,2,5 or 1-12 (default: all)")
    ap.add_argument("--timeout", type=int, default=600, help="seconds for one agent reply (default 600)")
    ap.add_argument("--judge-timeout", type=int, default=600, help="seconds for one judge reply (default 600)")
    ap.add_argument("--inline-instructions", action="store_true",
                    help="paste AGENTS.md into every prompt, for a model with no file access")
    ap.add_argument("--note", help="text for the Notes section of the run README")
    ap.add_argument("--dry-run", action="store_true", help="print the first prompt of each scenario and run nothing")
    ap.add_argument("--check-drift", action="store_true", help="compare the scenarios with the Markdown table and exit")
    ap.add_argument("--benchmark", choices=sorted(BENCHMARKS), default="tutor", help="which benchmark to run")
    ap.add_argument("--force", action="store_true", help="overwrite an existing run folder or scores")
    ap.add_argument("--root", default=str(ROOT), help="vault root (default: this vault)")
    ap.add_argument("--date", help="date for the run folder (default: today)")
    return ap


def main(argv=None):
    args = build_parser().parse_args(argv)
    root = Path(args.root).resolve()
    bench = BENCHMARKS[args.benchmark]
    data = load_scenarios(root / bench["scenarios"])
    problems = check_drift(data, (root / bench["markdown"]).read_text(encoding="utf-8"))
    if args.check_drift:
        for p in problems:
            print("drift:", p)
        name = f"{bench['scenarios'].name} and {bench['markdown'].name}"
        print(f"{name} match" if not problems else f"{len(problems)} differences")
        return 1 if problems else 0
    if problems:
        print(f"warning: {bench['scenarios'].name} and {bench['markdown'].name} differ:", "; ".join(problems), file=sys.stderr)

    if args.summarize:
        run_dir = Path(args.summarize)
        meta = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
        scored = json.loads((run_dir / "scores.json").read_text(encoding="utf-8"))
        verdict = evaluate(data, {int(k): v.get("score") for k, v in scored["scores"].items()}, meta["scenarios"])
        scored["verdict"] = verdict
        (run_dir / "scores.json").write_text(json.dumps(scored, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        write_summary(run_dir / "summary.md", data, meta, scored, verdict)
        print(f"total {verdict['total']} of {verdict['max']}; verdict: {verdict['verdict']}")
        return 0

    if args.score_run:
        run_dir = Path(args.score_run)
        if not args.judge_cmd:
            print("--score-run needs --judge-cmd", file=sys.stderr)
            return 2
        meta = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
        error = check_families(args, meta.get("agent_family"))
        if error:
            print("refused:", error, file=sys.stderr)
            return 2
        if (run_dir / "scores.json").exists() and not args.force:
            print("refused: scores.json exists; pass --force to score again", file=sys.stderr)
            return 2
        records = load_records(run_dir)
        statuses = {sid: "error" if any(r.get("error") for r in records if r["scenario"] == sid) else "ok"
                    for sid in meta["scenarios"]}
        verdict = judge_run(args, data, run_dir, meta, records, statuses)
        print(f"total {verdict['total']} of {verdict['max']}; verdict: {verdict['verdict']}")
        return 0

    if not args.agent_cmd and not args.dry_run:
        print("--agent-cmd is required (or --score-run RUN_DIR, --summarize RUN_DIR, --check-drift)", file=sys.stderr)
        return 2
    if not re.fullmatch(r"[A-Za-z0-9._-]+", args.label):
        print("refused: --label may use letters, digits, dot, underscore and hyphen only", file=sys.stderr)
        return 2
    error = check_families(args, args.agent_family)
    if error:
        print("refused:", error, file=sys.stderr)
        return 2
    ids = parse_ids(args.scenarios) if args.scenarios else [s["id"] for s in data["scenarios"]]
    known = {s["id"] for s in data["scenarios"]}
    if not ids or set(ids) - known:
        print(f"unknown scenarios: {sorted(set(ids) - known)}", file=sys.stderr)
        return 2
    ids = sorted(set(ids))
    inline = (root / "AGENTS.md").read_text(encoding="utf-8") if args.inline_instructions else None

    if args.dry_run:
        for sid in ids:
            s = next(x for x in data["scenarios"] if x["id"] == sid)
            print(f"##### scenario {sid}: {len(s['turns'])} learner turn(s); setup: {s['setup_description'] or 'none'}")
            convo = [("learner", s["turns"][0])]
            print(agent_prompt(convo, inline))
            for later in s["turns"][1:]:
                print(f"----- later turns send the real replies; learner message: {later}")
        print(f"dry run: {len(ids)} scenarios, nothing was run")
        return 0

    stamp = args.date or date.today().isoformat()
    run_dir = root / RUNS_REL / f"{stamp}-{bench['run_prefix']}{args.label}"
    if run_dir.exists() and not args.force:
        print(f"refused: {run_dir} exists; pick another --label or pass --force", file=sys.stderr)
        return 2
    run_dir.mkdir(parents=True, exist_ok=True)
    meta = {"date": stamp, "label": args.label, "benchmark": args.benchmark, "agent": args.agent_name or args.label,
            "agent_family": args.agent_family, "command": args.agent_cmd, "scenarios": ids, "timeout": args.timeout,
            "inline_instructions": bool(args.inline_instructions), "started": now()}
    records, statuses = run_scenarios(args, data, root, run_dir, meta)
    meta["finished"] = now()
    meta["errors"] = sorted(sid for sid, st in statuses.items() if st == "error")
    (run_dir / "run.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_transcript_md(run_dir / "transcript.md", meta, records)
    write_sheet(run_dir / "scoring_sheet.md", data, meta, ids)
    write_readme(run_dir / "README.md", meta, args.note)
    print(f"wrote {run_dir}")
    if args.judge_cmd:
        verdict = judge_run(args, data, run_dir, meta, records, statuses)
        print(f"total {verdict['total']} of {verdict['max']}; verdict: {verdict['verdict']}")
    else:
        print("no judge: score the run by hand with scoring_sheet.md, or run --score-run later")
    return 1 if meta["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
