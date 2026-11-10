"""Read the prerequisite map of the vault and check it against what the learner actually did.

The vault already says what must be understood before what, in the concept map of each track
(`10_Tracks/*/practice/Concept_Map.md`) and in the edges of the canvases in `30_Maps/`. This
module reads both, then asks the ledger what state each prerequisite is in.

A prerequisite is a gap when it was never tested without help, when the last attempt was wrong,
or when it has not been tested for a while. The point is to stop before the concept that needs
it, instead of finding out at the end that the gap was there all along.

Standard library only.
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from learning_ledger import load_objectives, parse_when  # noqa: E402
from scheduler import clean_attempts, days_since_last  # noqa: E402

VAULT = Path(__file__).resolve().parents[2]
CONCEPT_DIR = "20_Concepts"
ROW = re.compile(r"^\|\s*\d+\s*\|")
LINK = re.compile(r"\[\[([^\]|\\]+)(?:\\?\|[^\]]*)?\]\]")


def cell_links(text):
    """The wikilink targets of a table cell."""
    return [match.strip() for match in LINK.findall(text)]


def concept_maps(root=VAULT):
    """The prerequisite pairs written in the concept map of every track."""
    pairs = []
    for path in sorted(Path(root).glob("10_Tracks/*/practice/Concept_Map.md")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if not ROW.match(line.strip()):
                continue
            cells = re.split(r"(?<!\\)\|", line.strip())
            if len(cells) < 4:
                continue
            concepts = cell_links(cells[2])
            needs = cell_links(cells[3])
            if not concepts:
                continue
            for prerequisite in needs:
                if prerequisite.lower() == "none":
                    continue
                pairs.append({"concept": concepts[0], "needs": prerequisite, "source": path.name})
    return pairs


def canvas_pairs(root=VAULT):
    """The prerequisite pairs written in the edges of the canvases."""
    pairs = []
    for path in sorted(Path(root).glob("30_Maps/*.canvas")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        nodes = {node.get("id"): node for node in data.get("nodes", [])}
        for edge in data.get("edges", []):
            source = nodes.get(edge.get("fromNode"), {})
            target = nodes.get(edge.get("toNode"), {})
            source_file = str(source.get("file", ""))
            target_file = str(target.get("file", ""))
            if not source_file.startswith(CONCEPT_DIR) or not target_file.startswith(CONCEPT_DIR):
                continue
            pairs.append({
                "concept": Path(target_file).stem,
                "needs": Path(source_file).stem,
                "source": path.name,
            })
    return pairs


def prerequisites(root=VAULT):
    """Every prerequisite pair the vault knows, from the maps and the canvases."""
    pairs = concept_maps(root) + canvas_pairs(root)
    unique = {}
    for pair in pairs:
        key = (pair["concept"], pair["needs"])
        unique.setdefault(key, pair)
    return list(unique.values())


def state_of(concept, events, objectives, today=None):
    """How the learner stands on one concept, from the ledger."""
    today = today or date.today()
    ids = [objective for objective, entry in objectives.items()
           if str(entry.get("concept", "")).lower() == concept.lower()]
    subset = [event for event in events if event.get("objective_id") in ids]
    clean = clean_attempts(subset)
    if not subset:
        return {"concept": concept, "state": "never studied", "attempts": 0, "clean": 0}
    graded = [event for event in subset if event.get("mode") != "study"]
    if not graded:
        # The material was seen but no attempt was made, so nobody graded anything.
        return {"concept": concept, "state": "never tested", "attempts": len(subset), "clean": 0}
    if not clean:
        helped = [event for event in graded if event.get("assistance") != "none"]
        state = "only tested with help" if helped else "only graded by the agent"
        return {"concept": concept, "state": state, "attempts": len(subset), "clean": 0}
    last = clean[-1]
    when = parse_when(last.get("occurred_at"))
    days = (today - when).days if when else None
    if last.get("first_attempt_correct") is False:
        state = "last attempt was wrong"
    elif days is not None and days > 30:
        state = f"not tested for {days} days"
    else:
        state = "ok"
    return {"concept": concept, "state": state, "attempts": len(subset), "clean": len(clean),
            "last_attempt": last.get("occurred_at"), "days_since": days}


def gap_report(events, root=VAULT, target=None, objectives=None, today=None):
    """The prerequisites of the concepts, with the gaps that come before them."""
    today = today or date.today()
    objectives = objectives if objectives is not None else load_objectives()
    pairs = prerequisites(root)
    rows = []
    for concept in sorted({pair["concept"] for pair in pairs}):
        if target and concept.lower() != target.lower():
            continue
        needs = sorted({pair["needs"] for pair in pairs if pair["concept"] == concept})
        states = [state_of(need, events, objectives, today) for need in needs]
        gaps = [state for state in states if state["state"] != "ok"]
        rows.append({
            "concept": concept,
            "prerequisites": needs,
            "states": states,
            "gaps": gaps,
            "ready": not gaps,
        })
    return rows


if __name__ == "__main__":
    print(__doc__)
    sys.exit(0)
