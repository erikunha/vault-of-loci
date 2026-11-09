"""Build a zip of the vault without the example tracks, ready to open in Obsidian.

Copies every file git tracks, leaves out the example tracks, their canvases, the repository-only
files (`.github/`, `.githooks/`, `README.md`) and the tutor eval transcripts (`90_System/Evals/runs/`), and removes the links that pointed to what was left out: list
entries in the frontmatter, the link markup in the text (its label stays), and lines of `llms.txt`.
Then it rebuilds the index and runs the format check and every `check_*.py` inside the copy, and
writes the zip only if all of them pass. The release workflow attaches the zip to each release.

Usage: python3 -I 90_System/Scripts/build_blank_vault.py --out vault-of-loci-blank.zip
"""
import argparse
import os
import re
import stat
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NAME = "vault-of-loci"
LEFT_OUT = ("10_Tracks/01_Example_Course/", "10_Tracks/02_Example_Book/", "30_Maps/Example_Course.canvas",
            "30_Maps/Example_Book.canvas", ".github/", ".githooks/", "README.md", "90_System/Evals/runs/")


def tracked(root):
    run = subprocess.run(["git", "-C", str(root), "ls-files", "-z"], capture_output=True, text=True, check=True)
    return [f for f in run.stdout.split("\0") if f]


def unlink(text, removed):
    """Drop frontmatter list entries that link to a removed note, and keep only the label of other such links."""
    names = "|".join(re.escape(n) for n in sorted(removed, key=len, reverse=True))
    entry = re.compile(rf'"\[\[(?:{names})(?:[|#][^\]]*)?\]\]",?\s*')
    if text.startswith("---\n"):
        end = text.index("\n---", 4)
        head = entry.sub("", text[:end])
        head = re.sub(r",\s*\]", "]", head)
        text = head + text[end:]
    link = re.compile(rf"\[\[(?:{names})(?:#[^\]|]*)?(?:\|([^\]]*))?\]\]")
    return link.sub(lambda m: m.group(1) or m.group(0)[2:-2].split("#")[0], text)


def walk(top):
    """Every file and symlink under top, without following symlinked folders."""
    for here, dirs, names in os.walk(top):
        for d in list(dirs):
            if (Path(here) / d).is_symlink():
                dirs.remove(d)
                yield Path(here) / d
        for n in names:
            yield Path(here) / n


def build(out):
    files = [f for f in tracked(ROOT) if not f.startswith(LEFT_OUT)]
    removed = {Path(f).stem for f in tracked(ROOT) if f.startswith(LEFT_OUT[:4]) and f.endswith((".md", ".canvas"))}
    with tempfile.TemporaryDirectory() as tmp:
        vault = Path(tmp) / NAME
        for f in files:
            (vault / f).parent.mkdir(parents=True, exist_ok=True)
            if (ROOT / f).is_symlink():
                os.symlink(os.readlink(ROOT / f), vault / f)
            else:
                shutil.copy2(ROOT / f, vault / f)
        for path in vault.rglob("*.md"):
            if path.is_symlink() or any(p.is_symlink() for p in path.relative_to(vault).parents if p != Path(".") and (vault / p).is_symlink()):
                continue
            text = path.read_text(encoding="utf-8")
            new = unlink(text, removed)
            if new != text:
                path.write_text(new, encoding="utf-8")
        llms = vault / "llms.txt"
        if llms.exists():
            lines = llms.read_text(encoding="utf-8").splitlines(keepends=True)
            llms.write_text("".join(l for l in lines if not any(p in l for p in LEFT_OUT)), encoding="utf-8")
        scripts = vault / "90_System" / "Scripts"
        subprocess.run([sys.executable, "-I", str(scripts / "build_index.py")], check=True, capture_output=True)
        steps = [[str(scripts / "format_notes.py"), "--check"]] + [[str(p)] for p in sorted((scripts / "validation").glob("check_*.py"))]
        failed = 0
        for args in steps:
            run = subprocess.run([sys.executable, "-I", *args], capture_output=True, text=True, cwd=vault)
            name = Path(args[0]).name
            print(("passed: " if run.returncode == 0 else "FAILED: ") + name)
            if run.returncode:
                failed += 1
                print("    " + "\n    ".join((run.stdout + run.stderr).strip().splitlines()[-6:]))
        if failed:
            return 1
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
            for path in walk(vault):
                arc = str(path.relative_to(vault.parent))
                if path.is_symlink():
                    info = zipfile.ZipInfo(arc)
                    info.external_attr = (stat.S_IFLNK | 0o755) << 16
                    z.writestr(info, os.readlink(path))
                else:
                    z.write(path, arc)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", type=Path, required=True)
    sys.exit(build(ap.parse_args().out.resolve()))
