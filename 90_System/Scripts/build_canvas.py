"""Draw a JSON Canvas map for each track: the track note, its sessions and the concepts they link.

The canvas goes to `30_Maps/<Track_Name>.canvas` and opens in Obsidian's Canvas view. Sessions sit
in a column in session order; each concept a session links (a note in `20_Concepts/`) sits to the
right, with an arrow from every session that links it. Practice files sit under the track note.
The map is rebuilt from the notes each time, so edit the notes, not the canvas.

Dry run by default: prints what it would write. `--write` writes the files. `--track NAME` limits it to one track.

Usage: python3 -I 90_System/Scripts/build_canvas.py [--root DIR] [--track 01_Example_Course] [--write]
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

LINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
W, H, GAP = 320, 80, 40


def node_id(rel):
    return hashlib.sha1(rel.encode("utf-8")).hexdigest()[:16]


def node(rel, x, y, color=None):
    item = {"id": node_id(rel), "type": "file", "file": rel, "x": x, "y": y, "width": W, "height": H}
    if color:
        item["color"] = color
    return item


def canvas(root, track_dir):
    concepts = {p.stem: p for p in (root / "20_Concepts").glob("*.md")}
    track_note = track_dir / f"{track_dir.name.split('_', 1)[-1]}.md"
    if not track_note.exists():
        found = [p for p in track_dir.glob("*.md")]
        track_note = found[0] if found else None
    sessions = sorted((track_dir / "sessions").glob("*.md"))
    practice = sorted((track_dir / "practice").glob("*.md"))
    nodes, edges, placed = [], [], {}
    rel = lambda p: p.relative_to(root).as_posix()
    if track_note:
        nodes.append(node(rel(track_note), 0, 0, "4"))
    for i, p in enumerate(practice):
        nodes.append(node(rel(p), 0, (i + 1) * (H + GAP), "3"))
    for i, s in enumerate(sessions):
        y = i * (H + GAP)
        nodes.append(node(rel(s), W + 3 * GAP, y, "5"))
        if track_note:
            edges.append({"id": node_id(rel(track_note) + rel(s)), "fromNode": node_id(rel(track_note)), "toNode": node_id(rel(s))})
        for name in dict.fromkeys(LINK.findall(s.read_text(encoding="utf-8"))):
            # A link can name the concept with its folder, `[[20_Concepts/Alpha]]`, and that is
            # the same concept as `[[Alpha]]`.
            target = concepts.get(Path(name.strip()).name)
            if not target:
                continue
            key = rel(target)
            if key not in placed:
                placed[key] = len(placed)
                nodes.append(node(key, 2 * (W + 3 * GAP), placed[key] * (H + GAP), "6"))
            edges.append({"id": node_id(rel(s) + key), "fromNode": node_id(rel(s)), "toNode": node_id(key)})
    return {"nodes": nodes, "edges": edges}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    ap.add_argument("--track", help="track folder name in 10_Tracks")
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args(argv)
    tracks = sorted(p for p in (args.root / "10_Tracks").iterdir() if p.is_dir() and (not args.track or p.name == args.track))
    for track in tracks:
        data = canvas(args.root, track)
        out = args.root / "30_Maps" / f"{track.name.split('_', 1)[-1]}.canvas"
        text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
        print(f"{'written' if args.write else 'would write'}: {out.relative_to(args.root)} ({len(data['nodes'])} nodes, {len(data['edges'])} edges)")
        if args.write:
            out.parent.mkdir(exist_ok=True)
            out.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
