"""Test for build_blank_vault.py: the blank vault has no example tracks, no dangling links, and passes the checks."""
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "90_System" / "Scripts" / "build_blank_vault.py"

with tempfile.TemporaryDirectory() as tmp:
    out = Path(tmp) / "blank.zip"
    run = subprocess.run([sys.executable, "-I", str(SCRIPT), "--out", str(out)], capture_output=True, text=True)
    assert run.returncode == 0, run.stdout + run.stderr
    names = zipfile.ZipFile(out).namelist()
    top = {n.split("/")[0] for n in names}
    assert top == {"vault-of-loci"}, f"one top folder: {top}"
    files = {n.split("/", 1)[1] for n in names if not n.endswith("/")}
    assert not any("Example_" in f for f in files), "example tracks and their canvases are left out"
    assert not any(f.startswith((".github/", ".githooks/", ".git/")) for f in files), "repository files are left out"
    assert not any(f.startswith("90_System/Evals/runs/") for f in files), "tutor eval transcripts are left out"
    for kept in ("AGENTS.md", "00_Home.md", "20_Concepts/Retrieval_Practice.md", "90_System/Templates/Track.md",
                 ".obsidian/core-plugins.json", "90_System/Scripts/run_checks.py"):
        assert kept in files, f"{kept} is kept"
    vault = Path(tmp) / "x"
    zipfile.ZipFile(out).extractall(vault)
    concept = (vault / "vault-of-loci" / "20_Concepts" / "Retrieval_Practice.md").read_text(encoding="utf-8")
    assert "Example_Course" not in concept and "Example_Book" not in concept, "links to removed notes are gone"
    llms = (vault / "vault-of-loci" / "llms.txt").read_text(encoding="utf-8")
    assert "Example_Course" not in llms and "Example_Book" not in llms, "llms.txt lists no removed note"
    assert "passed" in run.stdout and "FAILED" not in run.stdout, run.stdout
print("ok: 9 checks")
