"""Read a memory palace note and give back the route of places, in walking order.

A palace is a route of familiar places. Each place holds one item. The learner walks the route in
the mind and says the item at each place, in the order of the route.

The palace note lives in `50_Review/Palaces/<Name>.md` and holds one table:

| Place | Item | Source |
|---|---|---|
| Front door | The first step | [[Source_Note]] |

The rows of the table are the route, in walking order. The number of a place is its position in
that order, and the ids the ledger uses are built from the name of the note:
- objective id: `palace-<name>`
- item id: `palace-<name>-<place number>`

The name is the file name of the note without the extension, lowercased, with the spaces and the
underscores turned into hyphens. `Home_Route.md` gives the name `home-route`, so the objective is
`palace-home-route` and the third place is the item `palace-home-route-3`.

This module holds the reading, the ids and the selection. `palace_test.py` prints the route.

Standard library only.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from learning_ledger import read_ledger  # noqa: E402
from scheduler import clean_attempts  # noqa: E402

VAULT = Path(__file__).resolve().parents[2]
LEDGER = VAULT / "50_Review" / "Attempts.jsonl"
PALACE_DIR = VAULT / "50_Review" / "Palaces"


def slug(name):
    """The name of a palace as an id: lowercase, with hyphens between the words."""
    text = str(name).strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def objective_id(name):
    """The ledger objective of a palace: `palace-<name>`."""
    return f"palace-{slug(name)}"


def item_id(name, number):
    """The ledger item of one place: `palace-<name>-<place number>`."""
    return f"{objective_id(name)}-{number}"


def _cells(line):
    """The cells of one Markdown table row, or None when the line is not a table row.

    A wikilink inside a cell carries its alias as `[[Note|Note one]]` or `[[Note\\|Note one]]`,
    and the pipe between them is not a column separator. A cell that ends with an escaped pipe
    keeps the backslash, so the link still reads as one link.
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


def _is_separator(cells):
    """True when the row is the `|---|---|` line under a header."""
    if not cells:
        return False
    return all(re.fullmatch(r":?-{2,}:?", cell) for cell in cells)


def parse_places(text):
    """The places of a palace note, in the order of the table.

    The table is the one whose header holds the columns `Place` and `Item`. Rows with an empty
    place are skipped, and the number of a place is its position among the rows that remain. That
    is the rule the vault documents: the number of a place is its position in the route.
    """
    places = []
    header = None
    for line in text.splitlines():
        cells = _cells(line)
        if cells is None:
            if header is not None:
                break
            continue
        if header is None:
            names = [cell.lower() for cell in cells]
            if "place" in names and "item" in names:
                header = names
            continue
        if _is_separator(cells):
            continue
        row = {name: cells[index] if index < len(cells) else "" for index, name in enumerate(header)}
        place = row.get("place", "").strip()
        if not place:
            continue
        places.append({
            "number": len(places) + 1,
            "place": place,
            "item": row.get("item", "").strip(),
            "source": row.get("source", "").strip(),
        })
    return places


def read_palace(path):
    """The palace of one note: its name, its objective id and its places in walking order."""
    note = Path(path)
    if not note.is_file():
        raise FileNotFoundError(f"palace note not found: {note}")
    text = note.read_text(encoding="utf-8")
    name = slug(note.stem)
    return {
        "name": name,
        "title": note.stem,
        "path": str(note),
        "objective_id": objective_id(name),
        "places": parse_places(text),
    }


def select_places(places, start=1, limit=None):
    """The places of the route that this walk covers, in walking order.

    `start` is the number of the first place, counted from 1, and `limit` caps how many places
    the walk takes. A place before the start is not part of the walk.
    """
    first = max(1, int(start or 1))
    chosen = [place for place in places if place["number"] >= first]
    if limit:
        chosen = chosen[:int(limit)]
    return chosen


def attempts_by_item(events, objective):
    """How many attempts the ledger holds for each item of one objective.

    Every attempt is counted, and the clean ones are counted apart: graded on the first try,
    without help, confirmed by the learner.
    """
    clean = {event.get("event_id") for event in clean_attempts(events)
             if event.get("objective_id") == objective}
    counts = {}
    for event in events:
        if event.get("objective_id") != objective:
            continue
        key = event.get("item_id")
        row = counts.setdefault(key, {"attempts": 0, "clean_attempts": 0})
        row["attempts"] += 1
        if event.get("event_id") in clean:
            row["clean_attempts"] += 1
    return counts


if __name__ == "__main__":
    print(__doc__)
    sys.exit(0)
