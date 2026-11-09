"""Walk a memory palace: the route of places, in order, with the item left blank.

A palace is a route of familiar places and each place holds one item. The learner walks the route
in the mind and says the item at each place. So this script prints the places and leaves the item
blank, and the agent asks one place at a time, in walking order.

The palace note is `50_Review/Palaces/<Name>.md` and its table has the columns Place, Item and
Source. The rows of that table are the route. The objective id of the palace is `palace-<name>`
and the item id of a place is `palace-<name>-<place number>`, so each place is recorded on its
own with `record_attempt.py --objective palace-<name> --item palace-<name>-<n> --mode recall`.

Usage: python3 -I 90_System/Scripts/palace_test.py --palace PATH [--places N] [--start N]
       [--ledger PATH] [--with-items] [--json]

The item of a place is not printed by default, in the text output and in the JSON output. The item
is what the learner has to recall. `--with-items` adds the item, for the agent that checks what
the learner said.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from learning_ledger import read_ledger  # noqa: E402
from palace import (  # noqa: E402
    LEDGER,
    attempts_by_item,
    item_id,
    read_palace,
    select_places,
)


def parse_args(argv):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--palace", type=Path, required=True, help="path of the palace note")
    ap.add_argument("--places", type=int, help="how many places of the route to show")
    ap.add_argument("--start", type=int, default=1, help="number of the first place to show")
    ap.add_argument("--ledger", type=Path, default=LEDGER, help="path of the ledger")
    ap.add_argument("--with-items", dest="with_items", action="store_true",
                    help="print the item of each place")
    ap.add_argument("--json", dest="as_json", action="store_true", help="print the route as JSON")
    return ap.parse_args(argv)


def build_route(args):
    """The route of the palace, the places this walk covers and the ledger counts of each."""
    palace = read_palace(args.palace)
    places = select_places(palace["places"], args.start, args.places)
    events, _ = read_ledger(args.ledger)
    counts = attempts_by_item(events, palace["objective_id"])
    rows = []
    for place in places:
        key = item_id(palace["name"], place["number"])
        seen = counts.get(key, {"attempts": 0, "clean_attempts": 0})
        row = {
            "number": place["number"],
            "place": place["place"],
            "item_id": key,
            "source": place["source"],
            "attempts": seen["attempts"],
            "clean_attempts": seen["clean_attempts"],
        }
        if args.with_items:
            row["item"] = place["item"]
        rows.append(row)
    return palace, rows


def main(argv=None):
    args = parse_args(argv)
    try:
        palace, rows = build_route(args)
    except FileNotFoundError as problem:
        print(f"palace not found: {problem}")
        return 1
    if args.as_json:
        print(json.dumps({
            "palace": palace["name"],
            "title": palace["title"],
            "objective_id": palace["objective_id"],
            "total_places": len(palace["places"]),
            "shown": len(rows),
            "start": args.start,
            "places": rows,
        }, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    print(f"Palace: {palace['name']}")
    print(f"Objective id: {palace['objective_id']}")
    if not palace["places"]:
        print()
        print("this palace has no places yet. Fill the table in the note first.")
        return 0
    if not rows:
        print()
        print(f"no place starts at {args.start}. The route has {len(palace['places'])} places.")
        return 0
    width = max(len(row["place"]) for row in rows)
    print()
    print(f"  {'#':>3}  {'place':<{width}}  {'item id':<{max(len(row['item_id']) for row in rows)}}  item")
    for row in rows:
        item = row.get("item", "")
        print(f"  {row['number']:>3}  {row['place']:<{width}}  {row['item_id']:<{max(len(r['item_id']) for r in rows)}}  {item}".rstrip())
    print()
    if args.with_items:
        print("The item is shown, so you can check what the learner said. Ask one place at a time,")
        print("in walking order, and record each place with the item id of that place.")
    else:
        print("The item is blank on purpose. Ask one place at a time, in walking order, and let the")
        print("learner say the item. Record each place with the item id of that place.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
