"""Read the prerequisite map of the vault and check it against what the learner actually did.

The vault already says what must be understood before what, in the concept map of each track
(`10_Tracks/*/practice/Concept_Map.md`) and in the edges of the canvases in `30_Maps/`. This
module reads both, then asks the ledger what state each prerequisite is in.

A prerequisite is a gap when it was never tested without help, when the mistake was never recovered,
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
from scheduler import clean_attempts, days_since_last, mistake_open  # noqa: E402

VAULT = Path(__file__).resolve().parents[2]
CONCEPT_DIR = "20_Concepts"
LINK = re.compile(r"\[\[([^\]|\\]+)(?:\\?\|[^\]]*)?\]\]")


def split_cells(line):
    """The cells of a Markdown table row, keeping the pipes that belong to a wikilink.

    A wikilink inside a table cell carries its alias as `[[Note|Note one]]` or as
    `[[Note\\|Note one]]`, and the pipe between them is not a column separator. A cell that ends
    with an escaped pipe keeps the backslash, so the link still reads as one link.
    """
    text = line.strip()
    if not text.startswith("|"):
        return None
    # The pipe that opens the row and the one that closes it are not separators.
    text = text[1:]
    if text.endswith("|"):
        text = text[:-1]
    cells, current, depth, index = [], "", 0, 0
    while index < len(text):
        char = text[index]
        if text.startswith("[[", index):
            depth += 1
            current += "[["
            index += 2
            continue
        if text.startswith("]]", index) and depth:
            depth -= 1
            current += "]]"
            index += 2
            continue
        if char == "|" and not depth and not (index and text[index - 1] == "\\"):
            cells.append(current)
            current = ""
            index += 1
            continue
        current += char
        index += 1
    cells.append(current)
    return [cell.strip() for cell in cells]


def cell_links(text):
    """The wikilink targets of a table cell."""
    return [match.strip() for match in LINK.findall(text)]


def same_concept(left, right):
    """True when two names point at the same concept.

    The comparison ignores case and the separators a name may carry, so "Retrieval Practice" and
    "Retrieval_Practice" are the same concept. It compares the words and not the letters, so
    "Practice" is not a name of "Retrieval_Practice".
    """
    def words(text):
        return [word for word in re.split(r"[^a-z0-9]+", str(text).lower()) if word]
    return words(left) == words(right)


def concept_key(name):
    """The key that groups two spellings of the same concept.

    The map of a track and the canvas of a track may write the same concept with different
    separators, "Retrieval Practice" in one and "Retrieval_Practice" in the other. Grouping by
    the key keeps them in one row, with the prerequisites of both.
    """
    return tuple(word for word in re.split(r"[^a-z0-9]+", str(name).lower()) if word)


def concept_maps(root=VAULT):
    """The prerequisite pairs written in the concept map of every track.

    The columns are read by their names, taken from the header of the table, so the map does not
    have to put the order in a number and does not have to keep the columns in one order.
    """
    pairs = []
    for path in sorted(Path(root).glob("10_Tracks/*/practice/Concept_Map.md")):
        header = None
        for line in path.read_text(encoding="utf-8").splitlines():
            cells = split_cells(line)
            if cells is None:
                header = None
                continue
            names = [cell.lower() for cell in cells]
            if header is None:
                if "concept" in names and any(name.startswith("needs") for name in names):
                    header = names
                continue
            if all(re.fullmatch(r":?-{2,}:?", cell) for cell in cells):
                continue
            concept_at = header.index("concept")
            needs_at = next(i for i, name in enumerate(header) if name.startswith("needs"))
            if concept_at >= len(cells) or needs_at >= len(cells):
                continue
            concepts = cell_links(cells[concept_at])
            needs = cell_links(cells[needs_at])
            if not concepts:
                continue
            for prerequisite in needs:
                if prerequisite.lower() == "none":
                    continue
                pairs.append({"concept": concepts[0], "needs": [prerequisite], "source": path.name})
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
                "needs": [Path(source_file).stem],
                "source": path.name,
            })
    return pairs


def prerequisites(root=VAULT):
    """Every prerequisite pair the vault knows, from the maps and the canvases.

    A pair the map and the canvas both declare is kept once, even when the two spell the
    concept differently, because they are the same dependency.
    """
    pairs = concept_maps(root) + canvas_pairs(root)
    unique = {}
    for pair in pairs:
        key = (concept_key(pair["concept"]), tuple(concept_key(need) for need in pair["needs"]))
        unique.setdefault(key, pair)
    return list(unique.values())


def state_of(concept, events, objectives, today=None):
    """How the learner stands on one concept, from the ledger."""
    today = today or date.today()
    ids = [objective for objective, entry in objectives.items()
           if same_concept(entry.get("concept", ""), concept)]
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
    if mistake_open(graded):
        state = "mistake not recovered"
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
    grouped = {}
    for pair in pairs:
        grouped.setdefault(concept_key(pair["concept"]), []).append(pair)
    rows = []
    for group in sorted(grouped.values(), key=lambda group: concept_key(group[0]["concept"])):
        concept = group[0]["concept"]
        if target and not same_concept(concept, target):
            continue
        needs = []
        for pair in group:
            for need in pair["needs"]:
                if not any(same_concept(need, known) for known in needs):
                    needs.append(need)
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
