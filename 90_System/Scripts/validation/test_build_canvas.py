"""Test for build_canvas.py."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "build_canvas.py"

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    track = root / "10_Tracks" / "01_Bio"
    (track / "sessions").mkdir(parents=True)
    (track / "practice").mkdir()
    (root / "20_Concepts").mkdir()
    (track / "Bio.md").write_text("---\ntype: track\n---\n\n# Bio\n", encoding="utf-8")
    (track / "practice" / "Checkpoints.md").write_text("# C\n", encoding="utf-8")
    (track / "sessions" / "session-01-cells.md").write_text("See [[Cell|cell]] and [[Cell]] and [[Missing]].\n", encoding="utf-8")
    (track / "sessions" / "session-02-dna.md").write_text("See [[Cell]] and [[DNA#Shape|the helix]].\n", encoding="utf-8")
    for name in ("Cell", "DNA"):
        (root / "20_Concepts" / f"{name}.md").write_text(f"# {name}\n", encoding="utf-8")
    out = root / "30_Maps" / "Bio.canvas"
    subprocess.run([sys.executable, "-I", str(SCRIPT), "--root", str(root)], check=True, capture_output=True)
    assert not out.exists(), "dry run writes nothing"
    subprocess.run([sys.executable, "-I", str(SCRIPT), "--root", str(root), "--write"], check=True, capture_output=True)
    data = json.loads(out.read_text(encoding="utf-8"))
    files = [n["file"] for n in data["nodes"]]
    assert files.count("20_Concepts/Cell.md") == 1, "a concept appears once"
    assert "20_Concepts/DNA.md" in files and not any("Missing" in f for f in files), files
    ids = {n["id"] for n in data["nodes"]}
    assert all(e["fromNode"] in ids and e["toNode"] in ids for e in data["edges"]), "edges point to nodes"
    assert len(data["edges"]) == 5, f"2 track-session, 3 session-concept, no duplicates: {data['edges']}"
    first = out.read_text(encoding="utf-8")
    subprocess.run([sys.executable, "-I", str(SCRIPT), "--root", str(root), "--write"], check=True, capture_output=True)
    assert out.read_text(encoding="utf-8") == first, "rebuilding gives the same file"
print("ok: 6 checks")
