"""Naming standard: underscores instead of spaces in file and folder names.

Renames (git mv) every file with a space in its name and rewrites references:
wikilinks, Markdown links (with %20) and paths in .canvas and .base files.
A wikilink without a label gets the old name as its label, so the rendered text does not change.
Idempotent: it also fixes links that still point to the spaced form of a file
that already uses underscores. Names are compared in Unicode NFC.

Usage: python3 90_System/Scripts/normalize_names.py [--write]
Without --write it only reports what it would do.
"""
import re
import subprocess
import sys
import unicodedata
from pathlib import Path
from urllib.parse import quote, unquote

VAULT = Path(__file__).resolve().parents[2]
SKIP = {".git", ".obsidian", ".venv", "node_modules", ".smart-env", ".trash", ".claude"}
TEXT = {".md", ".canvas", ".base", ".txt"}
WRITE = "--write" in sys.argv


def files():
    for p in VAULT.rglob("*"):
        if p.is_file() and not SKIP.intersection(p.relative_to(VAULT).parts):
            yield p


def key(name):
    """Name as a wikilink shows it: no .md, extension kept for attachments, NFC."""
    name = unicodedata.normalize("NFC", name)
    return name[:-3] if name.endswith(".md") else name


targets = {}
for p in files():
    if " " in p.name:
        new = p.with_name(p.name.replace(" ", "_"))
        if new.exists() or new in targets.values():
            sys.exit(f"collision: {p.relative_to(VAULT)} -> {new.name} already exists")
        targets[p] = new
for p, new in targets.items():
    if WRITE:
        subprocess.run(["git", "-C", str(VAULT), "mv", str(p), str(new)], check=True)
print("to rename:", len(targets))

existing = {key(p.name) for p in (list(files()) if WRITE else [targets.get(q, q) for q in files()])}


def resolves(name):
    name = unicodedata.normalize("NFC", name)
    return name not in existing and name.replace(" ", "_") in existing


WIKI = re.compile(r"(!?)\[\[([^\]|#^]+?)(\\?)([#^][^\]|]*)?(\\?\|[^\]]*)?\]\]")


def fix_wiki(m):
    embed, target, bar, anchor, label = m.groups()
    folder, _, base = target.rpartition("/")
    base = base.strip()
    if not resolves(base):
        return m.group(0)
    new = (folder + "/" if folder else "") + unicodedata.normalize("NFC", base).replace(" ", "_")
    if not label and not embed:
        label = ("\\|" if bar else "|") + base
        bar = ""
    return f"{embed}[[{new}{bar}{anchor or ''}{label or ''}]]"


def fix_path(value):
    raw = unquote(value)
    folder, _, base = raw.rpartition("/")
    if " " not in base or not resolves(key(base)):
        return value
    ext = base[len(key(base)):]
    new = (folder + "/" if folder else "") + key(base).replace(" ", "_") + ext
    return quote(new, safe="/#:") if "%" in value else new


MDLINK = re.compile(r"(\]\()([^)\s]+)(\))")
JSONPATH = re.compile(r'("(?:file|path)"\s*:\s*")([^"]+)(")')

touched = 0
for p in files():
    if p.suffix not in TEXT:
        continue
    t = p.read_text(encoding="utf-8")
    n = WIKI.sub(fix_wiki, t)
    n = MDLINK.sub(lambda m: m.group(1) + fix_path(m.group(2)) + m.group(3), n)
    n = JSONPATH.sub(lambda m: m.group(1) + fix_path(m.group(2)) + m.group(3), n)
    if n != t:
        touched += 1
        if WRITE:
            p.write_text(n, encoding="utf-8")
print("files with rewritten links:", touched)
