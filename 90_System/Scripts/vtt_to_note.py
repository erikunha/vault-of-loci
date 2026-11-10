"""Turn a WebVTT or SRT subtitle file into a transcript note the vault can read by section.

Each cue becomes one paragraph `**[H:MM:SS] Speaker:** text` (the speaker comes from a `<v Name>` tag
or a `Name:` prefix, and is left out when there is none). A caption that begins with a word of the
caption and a colon, "Note: the spacing effect...", is not a speaker, and the word stays in the
text. Consecutive cues from the same speaker are
merged until a sentence ends. Then `transcript_sections.py` adds a `## HH:MM:SS` heading about every
10 minutes, so an agent can read one range at a time through `index.json`.

The note goes to `10_Tracks/<track>/transcripts/<name>.md` with `type: transcript`. Dry run unless
`--write`; an existing note is never overwritten.

Usage: python3 -I 90_System/Scripts/vtt_to_note.py FILE.vtt --track 01_Example_Course [--title T] [--source URL] [--write]
"""
import argparse
import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TIME = re.compile(r"(?:(\d+):)?(\d{1,2}):(\d{2})[.,]\d{3}\s+-->")
VOICE = re.compile(r"^<v(?:\.[^ >]*)?\s+([^>]+)>")
PREFIX = re.compile(r"^([A-Z][\w .'-]{0,40}):\s+")
TAG = re.compile(r"<[^>]+>")
# The words a caption can begin with, before a colon, that are not the name of a speaker.
CAPTION_WORDS = {"note", "example", "warning", "chapter", "tip", "important", "summary",
                 "conclusion", "remember", "careful", "attention", "beware", "sorry", "well"}


def load_sections():
    spec = importlib.util.spec_from_file_location("transcript_sections", Path(__file__).with_name("transcript_sections.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sections


def cues(text):
    for block in re.split(r"\r?\n\s*\r?\n", text.replace("\ufeff", "")):
        lines = [l.strip() for l in block.strip().splitlines()]
        idx = next((i for i, l in enumerate(lines) if TIME.match(l)), None)
        if idx is None:
            continue
        h, m, s = TIME.match(lines[idx]).groups()
        seconds = int(h or 0) * 3600 + int(m) * 60 + int(s)
        raw = " ".join(lines[idx + 1:])
        speaker = ""
        v = VOICE.match(raw) or PREFIX.match(raw)
        if v:
            name = v.group(1).strip()
            # A word of the caption is not a speaker, and it stays in the text of the cue.
            if not (PREFIX.match(raw) and name.casefold() in CAPTION_WORDS):
                speaker, raw = name, raw[v.end():]
        words = " ".join(TAG.sub("", raw).split())
        if words:
            yield seconds, speaker, words


def paragraphs(items):
    merged = []
    for seconds, speaker, words in items:
        if merged and merged[-1][1] == speaker and not merged[-1][2].endswith((".", "?", "!")):
            merged[-1][2] += " " + words
        else:
            merged.append([seconds, speaker, words])
    out = []
    for seconds, speaker, words in merged:
        stamp = f"{seconds // 3600}:{seconds % 3600 // 60:02d}:{seconds % 60:02d}"
        out.append(f"**[{stamp}] {speaker}:** {words}" if speaker else f"**[{stamp}]** {words}")
    return out


def note(title, source, paras):
    head = ["---", "type: transcript", f"source: {source}" if source else "source:", "tags: [type/transcript]", "---", "", f"# {title}", ""]
    return "\n".join(head + "\n\n".join(paras).split("\n")) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("file", type=Path)
    ap.add_argument("--track", required=True, help="track folder name in 10_Tracks")
    ap.add_argument("--title", help="note title (default: file name)")
    ap.add_argument("--source", default="", help="URL or citation of the recording")
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args(argv)
    title = args.title or args.file.stem.replace("_", " ")
    paras = paragraphs(cues(args.file.read_text(encoding="utf-8", errors="replace")))
    text, headings = load_sections()(note(title, args.source, paras))
    name = re.sub(r"\s+", "_", title.strip()) + ".md"
    target = args.root / "10_Tracks" / args.track / "transcripts" / name
    print(f"{len(paras)} paragraphs, {headings} headings: {target.relative_to(args.root)}")
    if not args.write:
        print("\n".join(text.splitlines()[:12]))
        return 0
    if not (args.root / "10_Tracks" / args.track).is_dir():
        print("no such track:", args.track)
        return 1
    if target.exists():
        print("exists, not overwritten:", target)
        return 1
    target.parent.mkdir(exist_ok=True)
    target.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
