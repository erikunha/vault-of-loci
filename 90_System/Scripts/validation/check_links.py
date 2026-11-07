"""Broken links: wikilinks by name, relative Markdown links to .md files, and obsidian://
links to another vault that sits in the same parent folder as this one.

Usage: python3 -I 90_System/Scripts/validation/check_links.py [root]   (exits 1 on any broken link)
"""
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[3]
SKIP = {".obsidian", "node_modules", ".git", ".trash", ".venv", ".smart-env", ".claude", ".agents"}
files = [p for p in root.rglob("*") if p.is_file() and not SKIP.intersection(p.relative_to(root).parts)]
names = {unicodedata.normalize("NFC", n) for p in files
         for n in (p.stem, p.name, str(p.relative_to(root).with_suffix("")))}
broken = []
for p in files:
    if p.suffix != ".md":
        continue
    t = re.sub(r"```.*?```", "", p.read_text(errors="ignore"), flags=re.DOTALL)
    t = re.sub(r"`[^`\n]*`", "", t)
    for m in re.finditer(r"\[\[([^\]|#^]+)", t):
        n = unicodedata.normalize("NFC", m.group(1).strip().replace("\\", ""))
        if n and n not in names:
            broken.append((p, n))
    for m in re.finditer(r"\]\(([^)\s]+?\.md)(?:#[^)]*)?\)", t):
        target = unquote(m.group(1))
        if "://" not in target and not (p.parent / target).resolve().exists():
            broken.append((p, target))
    for m in re.finditer(r"obsidian://open\?[^\s)\]>\"']+", t):
        q = parse_qs(urlsplit(m.group(0)).query)
        vault, file = (q.get("vault") or [""])[0], (q.get("file") or [""])[0]
        other = root.parent / vault
        if vault and file and other.is_dir():
            target = unicodedata.normalize("NFC", file)
            if not any((other / c).exists() for c in (target, target + ".md")):
                broken.append((p, f"{vault}:{file}"))
print("broken:", len(broken))
for p, n in broken[:30]:
    print(" ", p.relative_to(root), "->", n)
sys.exit(1 if broken else 0)
