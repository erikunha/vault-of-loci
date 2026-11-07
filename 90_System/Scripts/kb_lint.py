"""Report notes that need attention: orphans, unused or unverified references, concepts in no track,
open questions and unprocessed clippings older than a set number of days.

A report, not a gate: it prints one line per finding and never edits a note, so it is safe on the
learner's own notes. `--strict` exits 1 when anything is found. Links from `INDEX.md` do not count,
since it links every note. The age limits are defaults to adjust, not research results.

Usage: python3 -I 90_System/Scripts/kb_lint.py [--root PATH] [--days 30] [--clip-days 14] [--strict]
"""
import argparse
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vault_notes import notes  # noqa: E402

LEAF_TYPES = {"home", "log", "index", "review", "daily", "debrief", "spec", "guide", "track", "question", "clipping", "transcript", "practice"}


def age(value):
    try:
        return (date.today() - date.fromisoformat(str(value)[:10])).days
    except ValueError:
        return None


def lint(root, days, clip_days):
    found = []
    all_notes = list(notes(root))
    inbound = {}
    for rel, front, links in all_notes:
        for name in links:
            inbound.setdefault(name, set()).add(rel.stem)
    for rel, front, links in all_notes:
        kind = front.get("type", "")
        sources = inbound.get(rel.stem, set()) - {rel.stem}
        if kind and not sources and kind not in LEAF_TYPES:
            found.append(f"orphan: {rel}  (no note links to it)")
        if kind == "concept" and not front.get("tracks"):
            found.append(f"no track: {rel}  (fill `tracks` or archive it)")
        if kind == "reference":
            if not sources:
                found.append(f"unused reference: {rel}  (no concept or session cites it)")
            if str(front.get("verified", "")).lower() != "true":
                found.append(f"unverified reference: {rel}  (open the source, then set `verified: true`)")
        if kind == "question" and front.get("status", "open") == "open" and (age(front.get("date")) or 0) > days:
            found.append(f"open question: {rel}  (older than {days} days)")
        if kind == "clipping" and str(front.get("processed", "false")).lower() != "true" and (age(front.get("clipped")) or 0) > clip_days:
            found.append(f"unprocessed clipping: {rel}  (older than {clip_days} days; turn it into a reference or delete it)")
    return found


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--clip-days", type=int, default=14)
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()
    found = lint(args.root, args.days, args.clip_days)
    print("\n".join(found) if found else "nothing to report")
    return 1 if args.strict and found else 0


if __name__ == "__main__":
    sys.exit(main())
