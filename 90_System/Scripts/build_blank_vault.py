"""Build a zip of the vault without the example tracks, ready to open in Obsidian.

Copies every file git tracks, leaves out the example tracks, their canvases, the repository-only
files (`.github/`, `.githooks/`, `README.md`) and the transcripts of the eval runs, and removes the
links that pointed to what was left out: list entries in the frontmatter, the link markup in the
text (its label stays), and lines of `llms.txt`. Then it rebuilds the index and runs the format
check and every `check_*.py` and `test_*.py` inside the copy, and writes the zip only if all of
them pass. The release workflow attaches the zip to each release.

The copy is built from the git file list when there is a git repository, and from the disk when
there is not, so the script also works in the vault that ships to a learner and in a vault
downloaded as a zip.

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
# The example tracks and their canvases, the files that belong to the repository and not to the
# vault, and the transcripts of the eval runs.
EXAMPLE = ("10_Tracks/01_Example_Course/", "10_Tracks/02_Example_Book/", "30_Maps/Example_Course.canvas",
           "30_Maps/Example_Book.canvas")
REPO_ONLY = (".github/", ".githooks/", "README.md")
RUNS = "90_System/Evals/runs/"
# The instructions for running the eval travel with the vault. The run folders, which hold the
# transcripts, do not.
KEEPS = ("90_System/Evals/runs/README.md",)


def left_out(path):
    """Whether a file is left out of the blank vault."""
    if path.startswith(EXAMPLE) or path.startswith(REPO_ONLY):
        return True
    if path.startswith(RUNS) and path not in KEEPS:
        return True
    return False


def tracked(root):
    """The files of the vault, as git sees them, or as the disk does when there is no git.

    A vault downloaded as a zip has no .git, and the blank vault that ships to a learner has none
    either. Asking git for the file list in those copies raises, so the disk is walked instead.
    """
    run = subprocess.run(["git", "-C", str(root), "ls-files", "-z"], capture_output=True, text=True)
    if run.returncode == 0:
        return [f for f in run.stdout.split("\0") if f]
    files = []
    for path in walk(root):
        relative = path.relative_to(root)
        if relative.parts and relative.parts[0] == ".git":
            continue
        files.append(str(relative))
    return sorted(files)


def unlink(text, removed):
    """Drop frontmatter list entries that link to a removed note, and keep only the label of other such links."""
    if not removed:
        # Nothing was removed, so there is nothing to take out. Without this the pattern below
        # matches the empty placeholder "[[]]" that the templates carry and turns it into nothing.
        return text
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
    everything = tracked(ROOT)
    files = [f for f in everything if not left_out(f)]
    removed = {Path(f).stem for f in everything if f.startswith(EXAMPLE) and f.endswith((".md", ".canvas"))}
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
            llms.write_text("".join(l for l in lines if not any(p in l for p in EXAMPLE + REPO_ONLY)),
                            encoding="utf-8")
        scripts = vault / "90_System" / "Scripts"
        subprocess.run([sys.executable, "-I", str(scripts / "build_index.py")], check=True, capture_output=True)
        # The whole suite runs here, the checks and the tests, because the vault that ships has to
        # pass the same command its own AGENTS.md tells the agent to run. A copy that fails a test
        # is a broken copy. The test of this script is left out: it runs this script, so running it
        # here would build a vault inside a vault without end.
        steps = [[str(scripts / "format_notes.py"), "--check"]]
        steps += [[str(p)] for p in sorted((scripts / "validation").glob("check_*.py"))]
        steps += [[str(p)] for p in sorted((scripts / "validation").glob("test_*.py"))
                  if p.name != "test_build_blank_vault.py"]
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
