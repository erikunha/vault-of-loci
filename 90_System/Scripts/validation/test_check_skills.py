"""Skill check tests on throwaway vaults (Agent Skills spec): name matches the folder, lowercase letters,
digits and single hyphens, at most 64 characters; description present and at most 1024 characters.
Run: python3 -I 90_System/Scripts/validation/test_check_skills.py"""
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "check_skills.py"
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


def skill(name, description="Does one thing. Use when asked.", extra=""):
    return f"---\nname: {name}\ndescription: {description}\n{extra}---\n\nBody.\n"


def path(folder):
    return f".agents/skills/{folder}/SKILL.md"


code, out = run({path("good-skill"): skill("good-skill")})
check(code == 0, f"valid skill: {out}")

code, out = run({path("good-skill"): skill("good-skill", extra="disable-model-invocation: true\n")})
check(code == 0, f"extra keys are allowed: {out}")

code, out = run({path("good-skill"): skill("other-name")})
check(code == 1 and "does not match" in out, f"name differs from the folder: {out}")

for bad in ("Bad-Skill", "bad_skill", "-bad", "bad-", "bad--skill", "bad skill"):
    code, out = run({path(bad): skill(bad)})
    check(code == 1 and "name" in out, f"invalid name {bad!r}: {out}")

long_name = "a" * 65
code, out = run({path(long_name): skill(long_name)})
check(code == 1 and "64" in out, f"name over 64 characters: {out}")
code, out = run({path("a" * 64): skill("a" * 64)})
check(code == 0, f"name of exactly 64 characters: {out}")

code, out = run({path("good-skill"): "---\nname: good-skill\n---\n\nBody.\n"})
check(code == 1 and "description" in out, f"missing description: {out}")

code, out = run({path("good-skill"): skill("good-skill", description="")})
check(code == 1 and "description" in out, f"empty description: {out}")

code, out = run({path("good-skill"): skill("good-skill", description="x" * 1025)})
check(code == 1 and "1024" in out, f"description over 1024: {out}")
code, out = run({path("good-skill"): skill("good-skill", description="x" * 1024)})
check(code == 0, f"description of exactly 1024: {out}")

code, out = run({path("good-skill"): "# No frontmatter\n"})
check(code == 1 and "frontmatter" in out, f"no frontmatter: {out}")

code, out = run({path("good-skill"): "---\nname: good-skill\ndescription: >\n  A folded\n  description.\n---\n"})
check(code == 0, f"folded description: {out}")

code, out = run({path("good-skill"): '---\nname: "good-skill"\ndescription: \'Quoted: value\'\n---\n'})
check(code == 0, f"quoted values: {out}")

code, out = run({".agents/skills/empty-folder/notes.md": "x\n"})
check(code == 1 and "SKILL.md" in out, f"a skill folder without SKILL.md: {out}")

code, out = run({"README.md": "no skills here\n"})
check(code == 0, f"a vault without skills passes: {out}")

print("ok:", checks, "checks")
