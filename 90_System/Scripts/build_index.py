"""Build the reading index for agents: INDEX.md (root) and 90_System/index.json.

Usage: python3 -I 90_System/Scripts/build_index.py [--check] [--root FOLDER]

INDEX.md has one line per note, grouped by folder: wikilink with a readable name, type, line count and
a summary of at most 200 characters. index.json has, per note: path, type, title, summary, lines and
headings (level, text, line), so an agent can open one section by line range instead of the whole file.

Summary, in this order: the `summary` frontmatter property, the body of the `[!tldr]` callout, the first
paragraph after the title (before the next heading).

Left out: folders that start with a dot, node_modules, dist, build, coverage, __pycache__, the templates
folder, folders with a `.vendored` marker, symbolic links and the root INDEX.md. The output is deterministic. With --check
nothing is written: exit 1 if either file would change.
"""
import argparse
import json
import os
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKIP_DIRS = {"node_modules", "dist", "build", "coverage", "__pycache__"}
SKIP_PATHS = {"90_System/Templates"}
INDEX_MD = "INDEX.md"
INDEX_JSON = Path("90_System") / "index.json"
SUMMARY_MAX = 200
FENCE = re.compile(r"\s*(`{3,}|~{3,})")
HEADING = re.compile(r"(#{1,6}) +(.+?)(?: +#+)?\s*$")
TLDR = re.compile(r"(?i)>\s*\[!tldr\][+-]?\s*(.*)$")
LIST_ITEM = re.compile(r"\s*([-*+]|\d+[.)]) ")


def find_notes(root):
    found = []
    for dirpath, dirnames, filenames in os.walk(root):
        d = Path(dirpath)
        if (d / ".vendored").exists():
            dirnames[:] = []
            continue
        dirnames[:] = sorted(
            n for n in dirnames
            if not n.startswith(".") and n not in SKIP_DIRS and (d / n).relative_to(root).as_posix() not in SKIP_PATHS
        )
        for name in sorted(filenames):
            p = d / name
            if name.endswith(".md") and not p.is_symlink() and not (d == root and name == INDEX_MD):
                found.append(p)
    return found


def properties(lines):
    """First-level frontmatter keys. A plain value loses its quotes; an indented block becomes one line."""
    props, current = {}, None
    for ln in lines:
        m = re.match(r"([A-Za-z_][\w-]*):\s*(.*)$", ln)
        if m:
            current = m.group(1)
            props[current] = m.group(2).strip()
        elif current and ln[:1] in (" ", "\t"):
            props[current] = (props[current] + " " + ln.strip()).strip()
    for k, v in props.items():
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
            v = v[1:-1].replace('\\"', '"')
        props[k] = re.sub(r"^[>|][+-]?\s*", "", v)
    return props


def clean(s):
    """Summary text: no markup, no dashes, no `::` or #tag that Obsidian would read as a card or a tag."""
    s = re.sub(r"<!--.*?-->", "", s)
    s = re.sub(r"!\[\[[^\]]*\]\]", "", s)
    s = re.sub(r"!\[[^\]]*\]\((?:[^()\s]|\([^()\s]*\))*\)", "", s)
    s = re.sub(r"\[\[[^\]|]*\|([^\]]*)\]\]", r"\1", s)
    s = re.sub(r"\[\[([^\]]*)\]\]", lambda m: m.group(1).split("/")[-1], s)
    s = re.sub(r"\[([^\]]*)\]\((?:[^()\s]|\([^()\s]*\))*\)", r"\1", s)
    s = s.replace("**", "").replace("~~", "").replace("==", "").replace("`", "")
    s = re.sub(r"(?<!\w)\*(\S|\S.*?\S)\*(?!\w)", r"\1", s)
    s = s.replace(" \u2014 ", ", ").replace(" \u2013 ", ", ").replace(" -- ", ", ")
    s = s.replace("\u2014", "-").replace("\u2013", "-").replace("::", ": ")
    s = re.sub(r"(^|\s)#(?=\w)", r"\1", s)
    s = re.sub(r"\s+", " ", s).strip()
    if len(s) > SUMMARY_MAX:
        s = s[: SUMMARY_MAX - 1].rstrip() + "…"
    return s


def not_paragraph(ln):
    s = ln.strip()
    return (
        not s
        or s.startswith((">", "|", "![[", "<", "%%", "$$", "#"))
        or bool(LIST_ITEM.match(ln))
        or bool(re.fullmatch(r"(-{3,}|\*{3,}|_{3,})", s))
    )


def analyze(p, root):
    text = p.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    props, start = {}, 0
    if lines and lines[0].rstrip() == "---":
        end = next((k for k in range(1, len(lines)) if lines[k].rstrip() == "---"), None)
        if end is not None:
            props, start = properties(lines[1:end]), end + 1

    visible, headings, fence, math = [], [], None, False
    for i in range(start, len(lines)):
        ln = lines[i]
        if fence:
            if re.fullmatch(rf"\s*{re.escape(fence[0])}{{{fence[1]},}}\s*", ln):
                fence = None
            continue
        if math:
            math = "$$" not in ln
            continue
        m = FENCE.match(ln)
        if m:
            fence = (m.group(1)[0], len(m.group(1)))
            continue
        if ln.strip().startswith("$$") and not (len(ln.strip()) > 2 and ln.strip().endswith("$$")):
            math = True
            continue
        visible.append((i, ln))
        h = HEADING.fullmatch(ln)
        if h:
            headings.append({"level": len(h.group(1)), "text": h.group(2).strip(), "line": i + 1})

    h1 = next((h for h in headings if h["level"] == 1), None)
    title = h1["text"] if h1 else p.stem.replace("_", " ")

    summary = clean(props.get("summary", ""))
    if not summary:
        for k, (_, ln) in enumerate(visible):
            if not TLDR.fullmatch(ln):
                continue
            body = []
            for _, following in visible[k + 1:]:
                if not following.startswith(">"):
                    break
                body.append(re.sub(r"^[-*]\s+", "", following.lstrip(">").strip()))
            summary = clean(" ".join(b for b in body if b))
            break
    if not summary:
        parts = []
        after_title = h1["line"] - 1 if h1 else -1
        for i, ln in visible:
            if i <= after_title:
                continue
            if HEADING.fullmatch(ln):
                break
            if not_paragraph(ln):
                summary = clean(" ".join(parts))
                if summary:
                    break
                parts = []
                continue
            parts.append(ln.strip())
        summary = summary or clean(" ".join(parts))

    return {
        "path": p.relative_to(root).as_posix(),
        "type": props.get("type", ""),
        "title": title,
        "summary": summary,
        "lines": len(lines),
        "headings": headings,
    }


def sort_key(n):
    folder = n["path"].rpartition("/")[0]
    return (unicodedata.normalize("NFC", folder), unicodedata.normalize("NFC", n["path"]), n["path"])


def label(n):
    stem = n["path"].rpartition("/")[2][: -len(".md")]
    folder = n["path"].rpartition("/")[0].rpartition("/")[2]
    if stem == "README" and folder:
        return f"{folder} README"
    return stem.replace("_", " ")


def render_md(notes):
    out = [
        "---",
        "type: index",
        "tags: [type/index]",
        "---",
        "",
        "# Vault index",
        "",
        "Generated by `90_System/Scripts/build_index.py`. Do not edit by hand. Each line has the note, its type, "
        "its line count and its summary. The headings of every note, with line numbers, are in "
        "`90_System/index.json`.",
    ]
    current = None
    for n in notes:
        folder = n["path"].rpartition("/")[0]
        if folder != current:
            out += ["", f"## {folder or '(root)'}", ""]
            current = folder
        target = n["path"][: -len(".md")]
        count = f"{n['lines']} line" + ("" if n["lines"] == 1 else "s")
        line = f"- [[{target}|{clean(label(n))}]] · {n['type'] or 'no type'} · {count}"
        if n["summary"]:
            line += f" · {n['summary']}"
        out.append(line)
    return "\n".join(out) + "\n"


def render_json(notes):
    return "[\n" + ",\n".join(json.dumps(n, ensure_ascii=False) for n in notes) + "\n]\n"


def build(root):
    notes = sorted((analyze(p, root) for p in find_notes(root)), key=sort_key)
    return notes, {INDEX_MD: render_md(notes), INDEX_JSON.as_posix(): render_json(notes)}


def update(root=ROOT):
    """Write the files that changed and return their names."""
    _, outputs = build(Path(root))
    written = []
    for rel, content in outputs.items():
        dest = Path(root) / rel
        data = content.encode("utf-8")
        if not dest.is_file() or dest.read_bytes() != data:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
            written.append(rel)
    return written


def main(argv=None):
    ap = argparse.ArgumentParser(description="Build INDEX.md and 90_System/index.json.")
    ap.add_argument("--check", action="store_true", help="write nothing; exit 1 if the files would change")
    ap.add_argument("--root", default=str(ROOT), help="vault folder (default: the one holding this script)")
    args = ap.parse_args(argv)
    root = Path(args.root).resolve()
    if args.check:
        notes, outputs = build(root)
        stale = [
            rel for rel, content in outputs.items()
            if not (root / rel).is_file() or (root / rel).read_bytes() != content.encode("utf-8")
        ]
        if stale:
            print("index out of date: " + ", ".join(stale))
            print("run: python3 -I 90_System/Scripts/build_index.py")
            return 1
        print(f"index current: {len(notes)} notes")
        return 0
    written = update(root)
    print("index built: " + (", ".join(written) if written else "no changes"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
