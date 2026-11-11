"""Writing rule check tests on throwaway vaults: em dash, en dash, Dataview, Templater and the
node id `end` in a Mermaid diagram.
Run: python3 -I 90_System/Scripts/validation/test_check_writing.py"""
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "check_writing.py"
checks = 0


def run(files):
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for name, text in files.items():
            (root / name).parent.mkdir(parents=True, exist_ok=True)
            (root / name).write_text(text, encoding="utf-8")
        r = subprocess.run([sys.executable, "-I", str(SCRIPT), str(root)], capture_output=True, text=True)
        return r.returncode, r.stdout


def check(cond, message):
    global checks
    assert cond, message
    checks += 1


code, out = run({"A.md": "# A note\n\nPlain words.\n"})
check(code == 0, f"a note without the rules: {out}")

code, out = run({"A.md": "# A note\n\nA word — another word.\n"})
check(code == 1 and "em dash or en dash" in out, f"an em dash: {out}")

code, out = run({"A.md": "# A note\n\nA word – another word.\n"})
check(code == 1 and "em dash or en dash" in out, f"an en dash: {out}")

code, out = run({"A.md": "# A note\n\nA word ― another word.\n"})
check(code == 1 and "em dash or en dash" in out, f"a horizontal bar: {out}")

code, out = run({"A.md": "# A note\n\nA word &#8212; another word.\n"})
check(code == 1 and "em dash or en dash" in out, f"an em dash written as an entity: {out}")

code, out = run({"A.md": "# A note\n\nA dash inside `code — here` is not prose.\n"})
check(code == 0, f"a dash in inline code: {out}")

code, out = run({"A.md": "# A note\n\nA dash inside ``code — here`` is not prose.\n"})
check(code == 0, f"a dash in a code span with two backticks: {out}")

code, out = run({"A.md": "# A note\n\n```\ncode — here\n```\n"})
check(code == 0, f"a dash inside a code block: {out}")

code, out = run({"A.md": "# A note\n\n````\n```\ncode — here\n```\n````\n"})
check(code == 0, f"a fence inside a fence does not close it: {out}")

code, out = run({"A.md": "# A note\n\n```\n~~~\ncode — here\n~~~\n```\n"})
check(code == 0, f"a fence of another kind does not close it: {out}")

code, out = run({"A.md": "# A note\n\n```\n```python\ncode — here\n```\n"})
check(code == 0, f"a fence with an info string does not close the block: {out}")

code, out = run({"A.md": "# A note\n\n    code — here\n"})
check(code == 0, f"a dash in an indented code block: {out}")

code, out = run({"A.md": "# A note\n\n>     code — here\n"})
check(code == 0, f"a dash in an indented code block inside a quote: {out}")

code, out = run({"A.md": "# A note\n\n```\ncode — here\n```\n", ".obsidian/plugin.md": "A word — another word.\n"})
check(code == 0, f"a tool folder is not the vault's own prose: {out}")

code, out = run({"A.md": "# A note\n\nA link to https://example.org/a—b and its text.\n"})
check(code == 0, f"a dash in a URL: {out}")

code, out = run({"A.md": "# A note\n\n| a | b |\n|---|---|\n| one — two | three |\n"})
check(code == 1 and "em dash or en dash" in out, f"a dash in a table cell is prose: {out}")

code, out = run({"A.md": "---\ntitle: A note — with a dash\n---\n\n# A note\n"})
check(code == 1 and "em dash or en dash" in out, f"a dash in the frontmatter: {out}")

code, out = run({"A.md": "# A note\n\n```dataview\nTABLE file.name\n```\n"})
check(code == 1 and "dataview or templater" in out, f"a dataview block: {out}")

code, out = run({"A.md": "# A note\n\n```templater\n<% tp.file.title %>\n```\n"})
check(code == 1 and "dataview or templater" in out, f"a templater block: {out}")

code, out = run({"A.md": "# A note\n\n```dataviewjs\nreturn 1\n```\n"})
check(code == 1 and "dataview or templater" in out, f"a dataviewjs block: {out}")

code, out = run({"A.md": "# A note\n\n> ```dataview\n> TABLE file.name\n> ```\n"})
check(code == 1 and "dataview or templater" in out, f"a dataview block in a quote: {out}")

code, out = run({"A.md": "# A note\n\n- ```dataview\n  TABLE file.name\n  ```\n"})
check(code == 1 and "dataview or templater" in out, f"a dataview block in a list: {out}")

code, out = run({"A.md": "# A note\n\n```mermaid\nflowchart LR\n  end[\"A node called end\"] --> B\n```\n"})
check(code == 1 and "end as a node id" in out, f"a node named end: {out}")

code, out = run({"A.md": "# A note\n\n```mermaid\nflowchart LR\n  A --> end\n```\n"})
check(code == 1 and "end as a node id" in out, f"an arrow to a node named end: {out}")

code, out = run({"A.md": "# A note\n\n> ```mermaid\n> flowchart LR\n>   end --> B\n> ```\n"})
check(code == 1 and "end as a node id" in out, f"a node named end in a quoted diagram: {out}")

code, out = run({"A.md": "# A note\n\n```mermaid\nflowchart LR\n  end --> B\n```\n"})
check(
    code == 1 and "A.md:5" in out and out.strip().splitlines()[-1] == "writing problems: 1",
    f"the problem of the diagram names its line and its count: {out}",
)

code, out = run({"A.md": "# A note\n\n```mermaid\nflowchart LR\n  subgraph one\n  A --> B\n  end\n```\n"})
check(code == 0, f"the end of a subgraph is not a node: {out}")

code, out = run({"A.md": "# A note\n\n```mermaid\nflowchart LR\n  A --> B\n  end \n```\n"})
check(code == 0, f"the end of a subgraph with a space: {out}")

code, out = run({"A.md": "# A note\n\n```mermaid\nflowchart LR\n  A == end == B\n```\n"})
check(code == 0, f"end between two equals signs is a label: {out}")

code, out = run({"A.md": "# A note\n\n```mermaid\nflowchart LR\n  A --> B\n"})
check(code == 1 and "never closed" in out, f"a fence that is never closed: {out}")

code, out = run({"Vendor/.vendored": "", "Vendor/A.md": "# A note\n\nA word — another word.\n"})
check(code == 0, f"a vendored folder is a third party copy: {out}")

code, out = run({"90_System/Evals/runs/2026-11-10-run/transcript.md": "A word — another word.\n"})
check(code == 0, f"the transcripts are the record of what a model said: {out}")

code, out = run({"00_Inbox/Clippings/2026-11-10-web.md": "A word — another word.\n"})
check(code == 0, f"a clipping is text pasted from the web: {out}")

code, out = run({"A.md": "", "B.md": "# No newline at the end"})
check(code == 0, f"an empty file and a file without a newline: {out}")

code, out = run({"A.md": "# A note\n\nA word — another word.\n", "B.md": "# Another\n\nA word – another word.\n"})
check(
    code == 1
    and "A.md:3" in out
    and "B.md:3" in out
    and out.strip().splitlines()[-1] == "writing problems: 2",
    f"every problem is named with its file, its line and its count: {out}",
)

print("ok:", checks, "checks")
