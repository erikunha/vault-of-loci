"""Normalize-names tests on throwaway git repos: renames files and folders, rewrites links
(wikilinks, Markdown with %20 and parentheses, canvas and base paths), keeps labels, skips
vendored folders, renames untracked files, is idempotent.
Run: python3 -I 90_System/Scripts/validation/test_normalize_names.py"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "normalize_names.py"
checks = 0


def vault(files, add=True):
    """Throwaway git repo holding the script and `files` (path -> text); returns (root, run)."""
    tmp = tempfile.TemporaryDirectory()
    root = Path(tmp.name)
    (root / "90_System" / "Scripts").mkdir(parents=True)
    shutil.copy(SCRIPT, root / "90_System" / "Scripts" / "normalize_names.py")
    for name, text in files.items():
        (root / name).parent.mkdir(parents=True, exist_ok=True)
        (root / name).write_text(text)
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    if add:
        subprocess.run(["git", "add", "-A"], cwd=root, check=True)
    cmd = [sys.executable, "-I", str(root / "90_System" / "Scripts" / "normalize_names.py"), "--write"]

    def run():
        return subprocess.run(cmd, cwd=root, capture_output=True, text=True)

    run.tmp = tmp
    return root, run


def check(cond, message):
    global checks
    assert cond, message
    checks += 1


# 1. file rename, wikilinks, labels, Markdown link, idempotence
root, run = vault({
    "My Note.md": "# My Note\n",
    "index.md": "See [[My Note]] and [[My Note|label]] and [x](My%20Note.md).\n",
})
r = run()
check(r.returncode == 0, r.stderr)
check((root / "My_Note.md").exists() and not (root / "My Note.md").exists(), "file not renamed")
index = (root / "index.md").read_text()
check("[[My_Note|My Note]]" in index, index)
check("[[My_Note|label]]" in index, index)
check("(My_Note.md)" in index, index)
again = run().stdout
check("to rename: 0" in again and "files with rewritten links: 0" in again, again)

# 2. folders with spaces, deepest first, links with folder paths
root, run = vault({
    "My Folder/Deep Dir/Some Note.md": "# Some Note\n",
    "My Folder/Other.md": "# Other\n",
    "index.md": (
        "[[My Folder/Deep Dir/Some Note]] [[My Folder/Other]] "
        "[a](My%20Folder/Deep%20Dir/Some%20Note.md) [b](My%20Folder/Other.md)\n"
    ),
    "map.canvas": '{"nodes":[{"type":"file","file":"My Folder/Deep Dir/Some Note.md"}]}\n',
    "view.base": 'views: [{"path": "My Folder/Other.md"}]\n',
})
r = run()
check(r.returncode == 0, r.stderr)
check((root / "My_Folder" / "Deep_Dir" / "Some_Note.md").exists(), "nested folders not renamed")
check(not (root / "My Folder").exists(), "old folder still there")
index = (root / "index.md").read_text()
check("[[My_Folder/Deep_Dir/Some_Note|Some Note]]" in index, index)
check("[[My_Folder/Other|Other]]" in index, index)
check("(My_Folder/Deep_Dir/Some_Note.md)" in index, index)
check("(My_Folder/Other.md)" in index, index)
check('"file":"My_Folder/Deep_Dir/Some_Note.md"' in (root / "map.canvas").read_text().replace(" ", ""), "canvas path")
check('"My_Folder/Other.md"' in (root / "view.base").read_text(), "base path")
again = run().stdout
check("to rename: 0" in again and "files with rewritten links: 0" in again, again)

# 3. Markdown link targets with parentheses
root, run = vault({
    "Paper (2006).md": "# Paper\n",
    "index.md": "[p](Paper%20(2006).md) and [q](Paper_(2006).md)\n",
})
r = run()
check(r.returncode == 0, r.stderr)
check((root / "Paper_(2006).md").exists(), "file with parentheses not renamed")
check((root / "index.md").read_text() == "[p](Paper_(2006).md) and [q](Paper_(2006).md)\n", (root / "index.md").read_text())

# 4. vendored folders are left alone
root, run = vault({
    "skill/.vendored": "source: test\n",
    "skill/My Ref.md": "# Ref\n[[My Ref]]\n",
    "Third Party/.vendored": "source: test\n",
    "Third Party/a.md": "# a\n",
    "own.md": "# own\n",
})
r = run()
check(r.returncode == 0, r.stderr)
check((root / "skill" / "My Ref.md").exists(), "renamed a vendored file")
check((root / "skill" / "My Ref.md").read_text() == "# Ref\n[[My Ref]]\n", "rewrote a vendored file")
check((root / "Third Party" / "a.md").exists(), "renamed a vendored folder")

# 5. a wikilink with the extension of the note, and a base that filters by folder
root, run = vault({
    "My Folder/My Note.md": "# My Note\n",
    "index.md": "[[My Folder/My Note.md]] and [[My Folder/My Note]]\n",
    "view.base": 'filters:\n  and:\n    - file.inFolder("My Folder")\n',
})
r = run()
check(r.returncode == 0, r.stderr)
index = (root / "index.md").read_text()
check("[[My_Folder/My_Note.md|My Note.md]]" in index, index)
check("[[My_Folder/My_Note|My Note]]" in index, index)
check('file.inFolder("My_Folder")' in (root / "view.base").read_text(), (root / "view.base").read_text())

# 6. untracked files are renamed without git mv
root, run = vault({"Loose Note.md": "# Loose\n", "index.md": "[[Loose Note]]\n"}, add=False)
r = run()
check(r.returncode == 0, r.stderr)
check((root / "Loose_Note.md").exists() and not (root / "Loose Note.md").exists(), "untracked file not renamed")
check("[[Loose_Note|Loose Note]]" in (root / "index.md").read_text(), "untracked link not rewritten")
print("ok:", checks, "checks")
