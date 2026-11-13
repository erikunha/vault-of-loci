"""Test that every criterion a learning scenario quotes is the one the agent will read.

A scenario tells the judge what the vault holds before the conversation. When it quotes a
criterion, the agent reads `90_System/Objectives.json` in its copy of the vault: the file the
scenario writes in its setup, or else the real one. A quote that is not in that file makes the
judge call a correct reply invented. This test fails on any quoted criterion that is not in the
objectives the scenario uses, and on an objective id paired with another objective's criterion.
"""
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SCENARIOS = REPO / "90_System" / "Evals" / "learning_scenarios.json"
OBJECTIVES_REL = "90_System/Objectives.json"
WRITE_FILE = "write_file"
TEXT_FIELDS = ("setup_description", "pass", "fail")

# `retrieval-practice-apply with the criterion "..."` names the id; `the criterion "..."` does not.
QUOTE = re.compile(r'(?:([a-z0-9]+(?:-[a-z0-9]+)+)\s+with\s+)?the\s+criterion\s+"([^"]+)"', re.IGNORECASE)


def objectives_for(scenario, real_objectives):
    """{id: criterion} of the objectives file the agent reads in this scenario."""
    data = real_objectives
    for op in scenario.get("setup", []):
        if op.get("op") == WRITE_FILE and op.get("path") == OBJECTIVES_REL:
            data = json.loads(op["content"])
    return {o["id"]: o["criterion"] for o in data["objectives"]}


def quotes_in(scenario):
    texts = [scenario.get(field, "") for field in TEXT_FIELDS] + list(scenario.get("scorer_notes", []))
    return [found for text in texts for found in QUOTE.findall(text)]


def problems_in(scenario, real_objectives):
    criteria = objectives_for(scenario, real_objectives)
    problems = []
    for objective_id, quoted in quotes_in(scenario):
        if quoted not in criteria.values():
            problems.append(f"scenario {scenario['id']}: criterion \"{quoted}\" is not in {OBJECTIVES_REL}")
        if objective_id and criteria.get(objective_id) != quoted:
            problems.append(f"scenario {scenario['id']}: {objective_id} does not hold \"{quoted}\"")
    return problems


def main():
    real = json.loads((REPO / OBJECTIVES_REL).read_text(encoding="utf-8"))
    data = json.loads(SCENARIOS.read_text(encoding="utf-8"))
    checks = 0

    quoted = 0
    for scenario in data["scenarios"]:
        problems = problems_in(scenario, real)
        assert not problems, "\n".join(problems)
        quoted += len(quotes_in(scenario))
        checks += 1
    assert quoted >= 1, "no learning scenario quotes a criterion, so this test checks nothing"
    checks += 1

    # The quote that made scenario 9 fail its judges must be caught.
    stale = {"id": 9, "setup": [], "pass": "", "fail": "",
             "setup_description": "The objective registry holds retrieval-practice-apply with the criterion "
                                  '"Apply the idea in a new case and say why it applies".'}
    assert len(problems_in(stale, real)) == 2, problems_in(stale, real)
    checks += 1

    # A real criterion under the wrong id is caught too.
    recall = next(o["criterion"] for o in real["objectives"] if o["id"] == "retrieval-practice-recall")
    swapped = dict(stale, setup_description=f'It holds retrieval-practice-apply with the criterion "{recall}".')
    assert problems_in(swapped, real) == [f'scenario 9: retrieval-practice-apply does not hold "{recall}"']
    checks += 1

    # A scenario that writes its own objectives file is checked against that file, not the real one.
    fixture = {"version": "v1", "objectives": [{"id": "alpha-apply", "criterion": "Use Alpha on a new case."}]}
    own = {"id": 99, "pass": "", "fail": "",
           "setup": [{"op": WRITE_FILE, "path": OBJECTIVES_REL, "content": json.dumps(fixture)}],
           "setup_description": 'The registry holds alpha-apply with the criterion "Use Alpha on a new case."'}
    assert problems_in(own, real) == [], problems_in(own, real)
    assert problems_in(dict(own, setup=[]), real), "the fixture criterion is not in the real registry"
    checks += 1

    print(f"ok: {checks} checks")


if __name__ == "__main__":
    main()
