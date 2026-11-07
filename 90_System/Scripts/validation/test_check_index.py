"""Reading index tests (build_index.py, check_index.py and the hook) on throwaway vaults: summary
(frontmatter, tldr callout, first paragraph, cut at 200), headings with line numbers, exclusions,
determinism, stale-index detection and a hook that never blocks.
Run: python3 -I 90_System/Scripts/validation/test_check_index.py"""
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parent
REAL_ROOT = SCRIPTS.parents[1]
BUILD = SCRIPTS / "build_index.py"
CHECK = HERE / "check_index.py"
FORMATTER = SCRIPTS / "format_notes.py"
HOOK = REAL_ROOT / ".claude" / "hooks" / "format_note.py"
INDEX_JSON = Path("90_System") / "index.json"
checks = 0


def check(cond, message):
    global checks
    assert cond, message
    checks += 1


def run(script, *args, stdin=None):
    return subprocess.run([sys.executable, "-I", str(script), *args], capture_output=True, text=True, input=stdin)


def write(root, rel, body):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


NOTE_A = """---
type: concept
summary: "Summary from the frontmatter."
---

# Note A

> [!tldr] In 3 lines
> Callout summary that loses.

Paragraph that loses.

## Section one

Text.

```bash
# comment that is not a heading
```

### Sub
"""
NOTE_B = "---\ntype: reference\n---\n\n# Note B\n\n> [!tldr] In 3 lines\n> First.\n> Second.\n\nParagraph that loses.\n"
NOTE_C = (
    "# Note C\n\n> [!abstract] Header\n\n- list item\n\nFirst line with [[Other|label]] and **bold**\n"
    "continues here \u2014 no dash.\n\nSecond paragraph.\n"
)
NOTE_D = "# Note D\n\n" + ("word " * 60).strip() + "\n"
NOTE_E = "Loose text at the start, no title.\n"
NOTE_N = "---\ntype: guide\n---\n\n# Note N\n\nFolder content.\n"
NOTE_G = "# Note G\n\n[![checks](https://example.org/b.svg)](https://example.org) ![logo](logo.png)\n\nReal first paragraph.\n"
NOTE_F = "# Note F\n\n~~~\n## fake heading\n~~~\n\n$$\n## math line\n$$\n\n## Real heading\n\nBody.\n"


def vault():
    tmp = tempfile.TemporaryDirectory()
    root = Path(tmp.name)
    write(root, "a_frontmatter.md", NOTE_A)
    write(root, "b_callout.md", NOTE_B)
    write(root, "c_paragraph.md", NOTE_C)
    write(root, "d_long.md", NOTE_D)
    write(root, "e_no_title.md", NOTE_E)
    write(root, "f_fences.md", NOTE_F)
    write(root, "g_badges.md", NOTE_G)
    write(root, "90_System/Templates/T.md", "---\ntype: concept\n---\n\n# Template marker\n")
    write(root, "folder/n.md", NOTE_N)
    write(root, ".git/x.md", "# git\n")
    write(root, ".obsidian/y.md", "# obsidian\n")
    write(root, ".hidden/h.md", "# hidden\n")
    write(root, "node_modules/p/x.md", "# package\n")
    write(root, "vendor/.vendored", "")
    write(root, "vendor/z.md", "# third party\n")
    write(root, "lab/dist/o.md", "# output\n")
    write(root, "INDEX.md", "# stale index marker\n")
    (root / "linked.md").symlink_to(root / "a_frontmatter.md")
    return tmp, root


def load(root):
    return {n["path"]: n for n in json.loads((root / INDEX_JSON).read_text(encoding="utf-8"))}


tmp, root = vault()
with tmp:
    r = run(BUILD, "--root", str(root))
    check(r.returncode == 0, f"build failed: {r.returncode}\n{r.stdout}{r.stderr}")
    notes = load(root)
    expected = {"a_frontmatter.md", "b_callout.md", "c_paragraph.md", "d_long.md", "e_no_title.md", "f_fences.md",
                "g_badges.md", "folder/n.md"}
    check(set(notes) == expected, f"indexed notes: {sorted(notes)}")

    a = notes["a_frontmatter.md"]
    check(a["summary"] == "Summary from the frontmatter.", f"frontmatter wins: {a['summary']!r}")
    check(a["type"] == "concept" and a["title"] == "Note A" and a["lines"] == 21, a)
    check(
        a["headings"] == [
            {"level": 1, "text": "Note A", "line": 6},
            {"level": 2, "text": "Section one", "line": 13},
            {"level": 3, "text": "Sub", "line": 21},
        ],
        f"headings with line numbers, none from inside code: {a['headings']}",
    )

    check(notes["b_callout.md"]["summary"] == "First. Second.", notes["b_callout.md"]["summary"])
    check(notes["b_callout.md"]["type"] == "reference", "type read from frontmatter")

    c = notes["c_paragraph.md"]["summary"]
    check(c == "First line with label and bold continues here, no dash.", f"first paragraph: {c!r}")

    d = notes["d_long.md"]["summary"]
    check(len(d) == 200 and d.endswith("…"), f"cut at 200: {len(d)} {d[-5:]!r}")

    e = notes["e_no_title.md"]
    check(e["title"] == "e no title" and e["summary"] == "Loose text at the start, no title." and e["headings"] == [], e)
    check(e["type"] == "", e)

    f = notes["f_fences.md"]
    check([h["text"] for h in f["headings"]] == ["Note F", "Real heading"], f"fences and math skipped: {f['headings']}")

    check(notes["g_badges.md"]["summary"] == "Real first paragraph.", f"badge and image lines skipped: {notes['g_badges.md']['summary']!r}")

    md = (root / "INDEX.md").read_text(encoding="utf-8")
    for piece in ("[[a_frontmatter|a frontmatter]]", "[[folder/n|n]]", "## folder", "## (root)",
                  " · concept · 21 lines · Summary from the frontmatter.",
                  " · no type · 1 line · Loose text"):
        check(piece in md, f"missing {piece!r} in\n{md}")
    for absent in ("stale index marker", "third party", "# package", "# output", "# hidden", "linked", "\u2014", "\u2013", "Template marker"):
        check(absent not in md, f"must not appear: {absent!r}")
    check("[[INDEX" not in md and "INDEX.md" not in "".join(notes), "INDEX.md stays out of its own index")

    spec = importlib.util.spec_from_file_location("format_notes", FORMATTER)
    fmt = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fmt)
    check(fmt.format_text(md) == md, "INDEX.md must already be in the formatter's output form")

    before = ((root / "INDEX.md").read_bytes(), (root / INDEX_JSON).read_bytes())
    check(run(BUILD, "--root", str(root)).returncode == 0, "second build")
    after = ((root / "INDEX.md").read_bytes(), (root / INDEX_JSON).read_bytes())
    check(before == after, "building twice must give the same bytes")

    r = run(BUILD, "--check", "--root", str(root))
    check(r.returncode == 0, f"a current index must pass: {r.stdout}{r.stderr}")
    r = run(CHECK, str(root))
    check(r.returncode == 0, f"check_index on a current index: {r.stdout}{r.stderr}")

    write(root, "b_callout.md", NOTE_B + "\nNew line.\n")
    r = run(BUILD, "--check", "--root", str(root))
    check(r.returncode == 1 and "out of date" in r.stdout, f"edited note: {r.returncode} {r.stdout}")
    check((root / "INDEX.md").read_bytes() == before[0], "--check must not write")
    r = run(CHECK, str(root))
    check(r.returncode == 1 and "out of date" in r.stdout, f"check_index on a stale index: {r.stdout}{r.stderr}")
    check(run(BUILD, "--root", str(root)).returncode == 0, "rebuild")
    check(run(CHECK, str(root)).returncode == 0, "check after rebuild")

    write(root, "new.md", "# New\n\nText.\n")
    check(run(CHECK, str(root)).returncode == 1, "a new note makes the index stale")
    check(run(BUILD, "--root", str(root)).returncode == 0, "rebuild")
    (root / "new.md").unlink()
    check(run(CHECK, str(root)).returncode == 1, "a removed note makes the index stale")
    check(run(BUILD, "--root", str(root)).returncode == 0, "rebuild")
    (root / INDEX_JSON).unlink()
    check(run(CHECK, str(root)).returncode == 1, "a missing index.json is stale")


def hook_vault(with_build):
    tmp = tempfile.TemporaryDirectory()
    root = Path(tmp.name)
    (root / ".claude" / "hooks").mkdir(parents=True)
    (root / "90_System" / "Scripts").mkdir(parents=True)
    shutil.copy(HOOK, root / ".claude" / "hooks" / "format_note.py")
    shutil.copy(FORMATTER, root / "90_System" / "Scripts" / "format_notes.py")
    if with_build:
        shutil.copy(BUILD, root / "90_System" / "Scripts" / "build_index.py")
    return tmp, root


def fire(root, target):
    payload = json.dumps({"tool_input": {"file_path": str(target)}})
    return run(root / ".claude" / "hooks" / "format_note.py", stdin=payload)


tmp, root = hook_vault(True)
with tmp:
    note = write(root, "note.md", "# T\ntext\n## S\n")
    r = fire(root, note)
    check(r.returncode == 0, f"hook: {r.stdout}{r.stderr}")
    check(note.read_text(encoding="utf-8") == "# T\n\ntext\n\n## S\n", "the hook still formats")
    md = (root / "INDEX.md").read_text(encoding="utf-8")
    check("[[note|note]]" in md and "text" in md, f"the hook regenerates the index:\n{md}")
    check(load(root)["note.md"]["headings"][1] == {"level": 2, "text": "S", "line": 5}, "json regenerated")
    outside = write(Path(tempfile.gettempdir()), "note_outside_the_vault.md", "# F\ntext\n")
    try:
        before = (root / "INDEX.md").read_bytes()
        check(fire(root, outside).returncode == 0, "outside file")
        check((root / "INDEX.md").read_bytes() == before and outside.read_text(encoding="utf-8") == "# F\ntext\n",
              "a file outside the vault is left alone")
    finally:
        outside.unlink()
    check(run(root / ".claude" / "hooks" / "format_note.py", stdin="garbage{").returncode == 0, "bad input never blocks")

tmp, root = hook_vault(False)
with tmp:
    note = write(root, "note.md", "# T\ntext\n")
    check(fire(root, note).returncode == 0, "without build_index the hook does not block")
    check(note.read_text(encoding="utf-8") == "# T\n\ntext\n", "and it still formats")
    check(not (root / "INDEX.md").exists(), "and writes no index")

print("ok:", checks, "checks")
