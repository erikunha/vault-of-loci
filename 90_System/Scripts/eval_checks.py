"""Deterministic checks of an eval scenario: what a rule can see without a model.

A judge reads the transcript and gives 0, 1 or 2. Some of what it reads does not need a reader:
which files the agent changed, whether a reply asks for a confidence, whether a reply hands over
a number the learner was supposed to recall. Each scenario of `tutor_scenarios.json` and
`learning_scenarios.json` lists those in a `checks` field, and this module evaluates them on the
transcript of a run. The result is shown next to the judge score. It does not change the score
or the verdict.

The checks a scenario can list:

- `forbid_writes`: path prefixes the agent may not create, change or delete during the scenario.
  The files come from the `files_changed` record the runner keeps for every agent turn.
- `allow_writes`: path prefixes inside a forbidden area that the learner's message asked for,
  such as the quiz file the `quiz` skill writes when the learner asks for a quiz.
- `asks_confidence`: the last agent reply asks for a confidence (1 to 5, or a probability).
- `forbid_strings`: text that no agent reply of the scenario may contain.

The write rule comes from AGENTS.md, Tutor mode: in `10_Tracks/`, `20_Concepts/` and
`50_Review/` the agent writes only what the learner asked for. `90_System/Evals/Tutor_mode.md`
states it for the scenarios.

Standard library only.
"""
import re

CHECK_KEYS = ("forbid_writes", "allow_writes", "asks_confidence", "forbid_strings")
CONFIDENCE = re.compile(
    r"confiden|how sure|how certain|\b1\s*(?:to|-|–)\s*5\b|probabilit|in percent|what percent|\d+\s*%\s*sure",
    re.IGNORECASE)


def problems_in_checks(scenario):
    """Why the `checks` field of a scenario cannot be read, as a list of lines."""
    checks = scenario.get("checks")
    if checks is None:
        return []
    sid = scenario.get("id")
    if not isinstance(checks, dict):
        return [f"scenario {sid}: checks is not an object"]
    bad = [f"scenario {sid}: unknown check '{key}'" for key in checks if key not in CHECK_KEYS]
    for key in ("forbid_writes", "allow_writes", "forbid_strings"):
        value = checks.get(key, [])
        if not isinstance(value, list) or not all(isinstance(v, str) and v for v in value):
            bad.append(f"scenario {sid}: {key} is not a list of text")
    if "asks_confidence" in checks and not isinstance(checks["asks_confidence"], bool):
        bad.append(f"scenario {sid}: asks_confidence is not true or false")
    if checks.get("allow_writes") and not checks.get("forbid_writes"):
        bad.append(f"scenario {sid}: allow_writes without forbid_writes allows nothing")
    return bad


def forbidden_writes(checks, paths):
    """The paths a scenario's checks forbid, in order."""
    forbid = checks.get("forbid_writes", [])
    allow = checks.get("allow_writes", [])
    return [p for p in paths
            if any(p.startswith(f) for f in forbid) and not any(p.startswith(a) for a in allow)]


def check_scenario(scenario, records):
    """The checks of one scenario on its records: {"passed": bool, "failures": [...]}, or None.

    None means the scenario lists no checks, or the agent gave no reply to check.
    """
    checks = scenario.get("checks")
    replies = [r for r in records if r.get("role") == "agent"]
    if not checks or not replies:
        return None
    failures = []
    touched = sorted({f for r in replies for f in r.get("files_changed", [])})
    for path in forbidden_writes(checks, touched):
        failures.append(f"wrote {path}")
    if checks.get("asks_confidence") and not CONFIDENCE.search(replies[-1].get("text") or ""):
        failures.append("the last reply asks for no confidence")
    for text in checks.get("forbid_strings", []):
        turns = [r.get("turn") for r in replies if text.lower() in (r.get("text") or "").lower()]
        if turns:
            failures.append(f"a reply contains '{text}' (turn {', '.join(map(str, turns))})")
    return {"passed": not failures, "failures": failures}


def check_run(data, records, ids):
    """The checks of every scenario of a run that lists checks, as {"<id>": result}."""
    by_id = {s["id"]: s for s in data["scenarios"]}
    out = {}
    for sid in ids:
        scenario = by_id.get(sid)
        if scenario is None:
            continue
        result = check_scenario(scenario, [r for r in records if r.get("scenario") == sid])
        if result is not None:
            out[str(sid)] = result
    return out


def describe(result):
    """One cell of the summary table for the checks of a scenario."""
    if result is None:
        return "no checks"
    return "passed" if result["passed"] else "FAILED: " + "; ".join(result["failures"])
