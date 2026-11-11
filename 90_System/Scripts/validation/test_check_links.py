"""Link-check tests on throwaway vaults: llms.txt and README.md are scanned, parentheses in
Markdown targets work, a broken target fails the check.
Run: python3 -I 90_System/Scripts/validation/test_check_links.py"""
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "check_links.py"
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


code, out = run({"Note.md": "# Note\n", "README.md": "[ok](Note.md)\n"})
check(code == 0, out)
code, out = run({"Note.md": "# Note\n", "llms.txt": "- [Note](Note.md)\n"})
check(code == 0, out)
code, out = run({"README.md": "[gone](Missing.md)\n"})
check(code == 1 and "Missing.md" in out, out)
code, out = run({"llms.txt": "- [gone](Missing.md)\n"})
check(code == 1 and "llms.txt" in out, out)
code, out = run({"Paper_(a,_2006).md": "# P\n", "llms.txt": "- [P](Paper_(a,_2006).md)\n"})
check(code == 0, out)
code, out = run({"llms.txt": "- [P](Paper_(a,_2006).md)\n"})
check(code == 1 and "Paper_(a,_2006).md" in out, out)
code, out = run({"Nöte.md": "# Nöte\n", "README.md": "[[Nöte]] [[Nöte|x]] [[Gone]]\n"})
check(code == 1 and "Gone" in out and out.count("->") == 1, out)
code, out = run({"README.md": '[gone](Missing.md "A title")\n'})
check(code == 1 and "Missing.md" in out, out)
code, out = run({"Note.md": "# Note\n", "README.md": "[ok](Note.md \"A title\")\n"})
check(code == 0, out)
code, out = run({"script.py": "print(1)\n", "README.md": "[[script]]\n"})
check(code == 1 and "script" in out, out)
code, out = run({"script.py": "print(1)\n", "README.md": "[[script.py]]\n"})
check(code == 0, out)
code, out = run({"README.md": "~~~\n[[Gone]]\n~~~\n"})
check(code == 0, f"a link inside a tilde fence is an example: {out}")
code, out = run({"README.md": "```\n[[Gone]]\n```\n"})
check(code == 0, f"a link inside a backtick fence is an example: {out}")
code, out = run({"README.md": "~~~\n[[Gone]]\n~~~\n\n[[Also_Gone]]\n"})
check(code == 1 and out.count("->") == 1 and "Also_Gone" in out, f"the fence is skipped and the text around it is not: {out}")
print("ok:", checks, "checks")
