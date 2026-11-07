"""Naming standard: underscores instead of spaces in file and folder names.

Renames every file and folder with a space in its name, deepest first (git mv for tracked
paths, a plain rename for untracked ones), and rewrites references: wikilinks (including
folder paths), Markdown links (with %20, parentheses allowed) and paths in .canvas and .base files.
Folders that hold a `.vendored` marker, and everything under them, are third-party and left alone.
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


def vendored(p):
    """Third-party path: it or a folder above it holds a .vendored marker."""
    return any((d / ".vendored").exists() for d in [p, *p.parents] if d.is_dir() and (d == VAULT or VAULT in d.parents))


def paths():
    for p in VAULT.rglob("*"):
        if not SKIP.intersection(p.relative_to(VAULT).parts) and not vendored(p):
            yield p


def files():
    for p in paths():
        if p.is_file():
            yield p


def rename(old, new):
    tracked = subprocess.run(["git", "-C", str(VAULT), "ls-files", "--error-unmatch", str(old)],
                             capture_output=True).returncode == 0
    if tracked:
        subprocess.run(["git", "-C", str(VAULT), "mv", str(old), str(new)], check=True)
    else:
        old.rename(new)


def key(name):
    """Name as a wikilink shows it: no .md, extension kept for attachments, NFC."""
    name = unicodedata.normalize("NFC", name)
    return name[:-3] if name.endswith(".md") else name


all_paths = [(q, q.is_dir()) for q in paths()]
targets = {}
for p, _ in all_paths:
    if " " in p.name:
        new = p.with_name(p.name.replace(" ", "_"))
        if new.exists() or new in targets.values():
            sys.exit(f"collision: {p.relative_to(VAULT)} -> {new.name} already exists")
        targets[p] = new
for p in sorted(targets, key=lambda q: len(q.parts), reverse=True):
    if WRITE:
        rename(p, targets[p])
print("to rename:", len(targets))

after = [(targets.get(q, q), is_dir) for q, is_dir in all_paths]
existing = {key(n.name) for n, is_dir in after if not is_dir}
folders = {n.name for n, is_dir in after if is_dir}


def resolves(name, known=None):
    name = unicodedata.normalize("NFC", name)
    known = existing if known is None else known
    return name not in known and name.replace(" ", "_") in known


def fix_folders(folder):
    """Rewrite each folder segment of a path that was renamed."""
    segments = [unicodedata.normalize("NFC", s).replace(" ", "_") if resolves(s, folders) else s
                for s in folder.split("/")]
    return "/".join(segments)


WIKI = re.compile(r"(!?)\[\[([^\]|#^]+?)(\\?)([#^][^\]|]*)?(\\?\|[^\]]*)?\]\]")


def fix_wiki(m):
    embed, target, bar, anchor, label = m.groups()
    folder, _, base = target.rpartition("/")
    base = base.strip()
    new_folder = fix_folders(folder) if folder else folder
    new_base = unicodedata.normalize("NFC", base).replace(" ", "_") if resolves(base) else base
    if new_folder == folder and new_base == base:
        return m.group(0)
    new = (new_folder + "/" if folder else "") + new_base
    if not label and not embed:
        label = ("\\|" if bar else "|") + base
        bar = ""
    return f"{embed}[[{new}{bar}{anchor or ''}{label or ''}]]"


def fix_path(value):
    raw = unquote(value)
    folder, _, base = raw.rpartition("/")
    new_folder = fix_folders(folder) if folder else folder
    new_base = base
    if " " in base and resolves(key(base)):
        new_base = key(base).replace(" ", "_") + base[len(key(base)):]
    if new_folder == folder and new_base == base:
        return value
    new = (new_folder + "/" if folder else "") + new_base
    return quote(new, safe="/#:()") if "%" in value else new


MDLINK = re.compile(r"(\]\()((?:[^()\s]|\([^()\s]*\))+)(\))")
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
