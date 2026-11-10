"""Study layer check tests on throwaway vaults: missing layer, wrong order, other types skipped.
Run: python3 -I 90_System/Scripts/validation/test_check_study_layer.py"""
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "check_study_layer.py"
GOOD = "## Study explanation\n\ntext\n\n## Key takeaways\n\n- x\n\n## Flashcards\n"
checks = 0


def run(files):
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for name, text in files.items():
            (root / name).parent.mkdir(parents=True, exist_ok=True)
            (root / name).write_text(text, encoding="utf-8")
        for folder in ("20_Concepts", "40_References"):
            (root / folder).mkdir(exist_ok=True)
        r = subprocess.run([sys.executable, "-I", str(SCRIPT), str(root)], capture_output=True, text=True)
        return r.returncode, r.stdout


def check(cond, message):
    global checks
    assert cond, message
    checks += 1


def note(kind, body):
    return f"---\ntype: {kind}\n---\n\n# T\n\n> [!tldr] In 3 lines\n> x\n\n{body}"


for kind, folder in (("concept", "20_Concepts"), ("reference", "40_References/Papers"), ("guide", "40_References/Guides")):
    code, out = run({f"{folder}/A.md": note(kind, GOOD)})
    check(code == 0, f"{kind} with the layer: {out}")
    code, out = run({f"{folder}/A.md": note(kind, "## Details\n\ntext\n")})
    check(code == 1 and "missing" in out, f"{kind} without the layer: {out}")
    code, out = run({f"{folder}/A.md": note(kind, "## Key takeaways\n\n- x\n\n## Study explanation\n\ntext\n")})
    check(code == 1 and "out of order" in out, f"{kind} out of order: {out}")
    code, out = run({f"{folder}/A.md": note(kind, "## Study explanation\n\ntext\n\n## Details\n\n## Key takeaways\n")})
    check(code == 1 and "out of order" in out, f"{kind} takeaways not second: {out}")
code, out = run({"20_Concepts/A.md": "# No frontmatter\n\n## Details\n"})
check(code == 1 and "missing" in out, f"no frontmatter: {out}")
code, out = run({"40_References/A.md": note("log", "## Details\n")})
check(code == 0, f"other type skipped: {out}")
code, out = run({"20_Concepts/A.md": note("concept", "```\n## Study explanation\n```\n\n## Details\n")})
check(code == 1 and "missing" in out, f"heading inside a code fence: {out}")
CONFIG = "90_System/Specs/study_layer.json"
PT = "## Explicacao\n\ntexto\n\n## Pontos\n\n- x\n"
cfg = '{"explanation": "## Explicacao", "takeaways": "## Pontos"}'
code, out = run({"20_Concepts/A.md": note("concept", PT), CONFIG: cfg})
check(code == 0, f"headings read from study_layer.json: {out}")
code, out = run({"20_Concepts/A.md": note("concept", GOOD), CONFIG: cfg})
check(code == 1 and "missing" in out, f"default headings fail when the file renames them: {out}")
code, out = run({"20_Concepts/A.md": note("concept", PT)})
check(code == 1 and "missing" in out, f"without the file the built-in headings apply: {out}")
code, out = run({"20_Concepts/A.md": note("concept", GOOD), CONFIG: "{not json"})
check(code == 1 and "study_layer.json" in out, f"invalid json is reported: {out}")
code, out = run({"20_Concepts/A.md": note("concept", GOOD), CONFIG: '{"explanation": 3}'})
check(code == 1 and "study_layer.json" in out, f"wrong value type is reported: {out}")
code, out = run({"20_Concepts/A.md": note("log", "## Details\n"), CONFIG: '{"checked_types": ["log"]}'})
check(code == 1 and "missing" in out, f"checked_types from the file: {out}")
code, out = run({"20_Concepts/A.md": note("concept", "## Details\n"), CONFIG: '{"checked_types": ["log"]}'})
check(code == 0, f"a type outside checked_types is skipped: {out}")
code, out = run({"20_Concepts/A.md": '---\ntype: "concept"\n---\n\n# T\n\n> [!tldr] In 3 lines\n> x\n\n## Details\n'})
check(code == 1 and "missing" in out, f"a quoted type is the type it quotes: {out}")
code, out = run({"20_Concepts/A.md": '---\ntype: concept\n---\n\n# T\n\n## Study explanation\n\ntext\n\n## Key takeaways\n\n- x\n'})
check(code == 1 and "tldr" in out, f"the callout of three lines is part of the order: {out}")
print("ok:", checks, "checks")
