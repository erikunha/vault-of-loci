"""Flashcard check tests on throwaway vaults: source link, duplicates, skipped places.
Run: python3 -I 90_System/Scripts/validation/test_check_cards.py"""
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "check_cards.py"
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


def note(body, kind="concept"):
    return f"---\ntype: {kind}\n---\n\n# T\n\n## Study explanation\n\ntext\n\n{body}"


code, out = run({"20_Concepts/A.md": note("## Flashcards\n\nWhat is X?::A thing, see [[Source_A|source]].\n")})
check(code == 0, f"inline source link: {out}")

code, out = run({"20_Concepts/A.md": note("## Flashcards\n\nSource: [[Source_A|source]]\n\nWhat is X?::A thing.\n")})
check(code == 0, f"source link in the flashcards section: {out}")

code, out = run({"20_Concepts/A.md": note("## Related\n\n- [[Source_A]]\n\n## Flashcards\n\nWhat is X?::A thing.\n")})
check(code == 0, f"source link in the Related section: {out}")

code, out = run({"20_Concepts/A.md": note("## Flashcards\n\nWhat is X?::A thing.\n")})
check(code == 1 and "no source link" in out and "A.md:" in out, f"card without a source: {out}")

code, out = run({"20_Concepts/A.md": note("## Study notes\n\nSee [[Elsewhere]].\n\n## Flashcards\n\n- What is X?::A thing.\n")})
check(code == 1 and "no source link" in out, f"link in an unrelated section, list card: {out}")

code, out = run({
    "20_Concepts/A.md": note("## Flashcards\n\nWhat is X?::A, see [[S]].\n"),
    "20_Concepts/B.md": note("## Flashcards\n\n  what is   X ?::B, see [[S]].\n"),
})
check(code == 1 and "duplicate question" in out, f"duplicate across notes: {out}")

code, out = run({"20_Concepts/A.md": note("## Flashcards\n\nWhat is X?::A, see [[S]].\nWhat is X?::Again [[S]].\n")})
check(code == 1 and "duplicate question" in out, f"duplicate in one note: {out}")

code, out = run({
    "20_Concepts/A.md": note("## Flashcards\n\nWhat is X?::A, see [[S]].\nWhat is Y?::B, see [[S]].\n"),
})
check(code == 0, f"distinct questions: {out}")

code, out = run({
    "90_System/Templates/Concept.md": "## Flashcards\n\nquestion::answer\n",
    "90_System/Specs/S.md": "## Flashcards\n\nquestion::answer\n",
    "README.md": "Write `question::answer` cards.\n\n```\nq::a\n```\n",
})
check(code == 0, f"templates, specs, inline code and fences skipped: {out}")

code, out = run({
    "20_Concepts/A.md": note("## Flashcards\n\nWhat is X?::A, see [[S]].\n"),
    "Vendor/.vendored": "",
    "Vendor/B.md": "## Flashcards\n\nWhat is X?::B\n",
})
check(code == 0, f"vendored folder skipped: {out}")

code, out = run({"20_Concepts/A.md": "---\nstatus:: draft\n---\n\n# T\n\nWhat?::\n"})
check(code == 0, f"frontmatter and empty answers are not cards: {out}")

code, out = run({"20_Concepts/A.md": note("## Flashcards\n\nWhat is X?::A thing, see [the paper](https://doi.org/10.1/x).\n")})
check(code == 0, f"a Markdown link or URL is a source: {out}")

code, out = run({"40_References/P.md": "---\ntype: reference\nlink: https://example.org/p\n---\n\n# P\n\nWhat does P show?::That Y.\n"})
check(code == 0, f"a filled link property is the source of the whole note: {out}")

code, out = run({"20_Concepts/A.md": "---\ntype: concept\ntags: [flashcards]\n---\n\n# T\n\n## Flashcards\n\nSpacing beats ==massed== practice.\n"})
check(code == 1 and "no source link" in out, f"a cloze needs a source too: {out}")

code, out = run({"20_Concepts/A.md": "---\ntype: concept\n---\n\n# T\n\nThis is ==important== prose.\n"})
check(code == 0, f"highlights outside a flashcards note are not clozes: {out}")

code, out = run({"20_Concepts/A.md": note("| What?::table | x |\n\n> What?::quote\n")})
check(code == 0, f"tables and quotes are not cards: {out}")


code, out = run({"20_Concepts/A.md": "---\ntype: concept\ntags:\n  - flashcards\n---\n\n# T\n\n## Flashcards\n\nSpacing beats ==massed== practice.\n"})
check(code == 1 and "no source link" in out, f"a cloze in a note with the tags in a list needs a source: {out}")

code, out = run({"40_References/P.md": "---\ntype: reference\nlink: \"\"\n---\n\n# P\n\nWhat does P show?::That Y.\n"})
check(code == 1 and "no source link" in out, f"an empty link property is not a source: {out}")

print("ok:", checks, "checks")
