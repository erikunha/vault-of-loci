"""Add `## HH:MM:SS` headings to transcripts, about one every 10 minutes of speech.

A transcript has one line of speech per paragraph: `**[H:MM:SS] Speaker:** text` (or `**[H:MM:SS]** text`).
A heading goes before the first line and before the first line that starts at least 600 seconds after the
previous heading. The text never changes: remove the inserted lines and the file is byte for byte the same.
A transcript that already has a heading (`##` to `######` outside code) is left alone, so running again
changes nothing. A transcript with fewer than two possible headings is left alone. Line endings are kept.

Without files, it looks at every `transcripts/*.md` folder in the vault. Dry run unless `--write`.
`--report` edits nothing: it lists notes over 300 lines with no `##` heading, to fix by hand.

Usage: python3 -I 90_System/Scripts/transcript_sections.py [--write] [--root DIR] [files.md ...]
       python3 -I 90_System/Scripts/transcript_sections.py --report [--root DIR]
"""
import argparse
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STEP = 600
MAX_LINES = 300
SKIP = {"node_modules", "Templates", "dist", "build", "__pycache__"}
SPEECH = re.compile(r"\*\*\[(\d+):([0-5]\d):([0-5]\d)\]")
FENCE = re.compile(r"\s*(`{3,}|~{3,})")
HEADING = re.compile(r"#{2,6} ")


def notes(root):
    for dirpath, dirnames, filenames in os.walk(root):
        d = Path(dirpath)
        if (d / ".vendored").exists():
            dirnames[:] = []
            continue
        dirnames[:] = sorted(n for n in dirnames if not n.startswith(".") and n not in SKIP)
        for name in sorted(filenames):
            if name.endswith(".md") and not (d / name).is_symlink():
                yield d / name


def transcripts(root):
    return [p for p in notes(root) if p.parent.name == "transcripts"]


def body(lines):
    start = 0
    if lines and lines[0].rstrip("\r") == "---":
        end = next((k for k in range(1, len(lines)) if lines[k].rstrip("\r") == "---"), None)
        if end is not None:
            start = end + 1
    return range(start, len(lines))


def scan(lines):
    """(has_heading, speech): speech is a list of (line_index, seconds) outside code."""
    fence, has_heading, speech = None, False, []
    for i in body(lines):
        ln = lines[i].rstrip("\r")
        m = FENCE.match(ln)
        if fence:
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= fence[1] and ln.strip() == m.group(1):
                fence = None
            continue
        if m:
            fence = (m.group(1)[0], len(m.group(1)))
            continue
        if HEADING.match(ln):
            has_heading = True
            continue
        s = SPEECH.match(ln)
        if s:
            speech.append((i, int(s.group(1)) * 3600 + int(s.group(2)) * 60 + int(s.group(3))))
    return has_heading, speech


def hhmmss(s):
    return f"{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}"


def sections(text):
    """Return (new_text, headings_inserted)."""
    cr = "\r" if "\r\n" in text else ""
    lines = text.split("\n")
    has_heading, speech = scan(lines)
    if has_heading:
        return text, 0
    points, last = [], None
    for i, s in speech:
        if last is None or s - last >= STEP:
            points.append((i, s))
            last = s
    if len(points) < 2:
        return text, 0
    out, marks = [], dict(points)
    for i, ln in enumerate(lines):
        if i in marks:
            if out and out[-1].strip("\r"):
                out.append(cr)
            out.append(f"## {hhmmss(marks[i])}{cr}")
            out.append(cr)
        out.append(ln)
    return "\n".join(out), len(points)


def long_without_heading(root):
    found = []
    for p in notes(root):
        lines = p.read_text(encoding="utf-8", errors="replace").split("\n")
        if lines and lines[-1] == "":
            lines.pop()
        if len(lines) > MAX_LINES and not any(HEADING.match(lines[i]) for i in body(lines)):
            found.append((p, len(lines)))
    return found


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("files", nargs="*", help="transcripts (default: every transcripts/*.md)")
    ap.add_argument("--write", action="store_true", help="write; without it, dry run")
    ap.add_argument("--report", action="store_true", help="list long notes with no ## heading and exit")
    ap.add_argument("--root", default=str(ROOT), help="vault root (default: this script's vault)")
    args = ap.parse_args(argv)
    root = Path(args.root).resolve()
    if args.report:
        found = long_without_heading(root)
        print(f"notes over {MAX_LINES} lines with no ## heading: {len(found)}")
        for p, n in found:
            print(f"  {n:5d}  {p.relative_to(root)}")
        return 0
    targets = [Path(a).resolve() for a in args.files] or transcripts(root)
    total = 0
    for p in targets:
        new, n = sections(p.read_bytes().decode("utf-8"))
        label = p.relative_to(root) if root in p.parents else p
        if n:
            total += n
            if args.write:
                p.write_bytes(new.encode("utf-8"))
            print(f"{'written' if args.write else 'would write'}: {label} (+{n} headings)")
        else:
            print(f"unchanged: {label}")
    print(f"{total} headings {'inserted' if args.write else 'to insert (run with --write)'} in {len(targets)} transcripts")
    return 0


if __name__ == "__main__":
    sys.exit(main())
