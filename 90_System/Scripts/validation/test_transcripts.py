"""Tests for transcript_sections.py and vtt_to_note.py."""
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]


def run(*args):
    return subprocess.run([sys.executable, "-I", *map(str, args)], capture_output=True, text=True)


speech = "\n\n".join(f"**[0:{m:02d}:00] Ana:** line {m}." for m in range(0, 25, 5))
transcript = f"---\ntype: transcript\n---\n\n# Talk\n\n{speech}\n"

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    folder = root / "10_Tracks" / "01_T" / "transcripts"
    folder.mkdir(parents=True)
    note = folder / "Talk.md"
    note.write_text(transcript, encoding="utf-8")
    assert run(SCRIPTS / "transcript_sections.py", "--root", root).returncode == 0
    assert note.read_text(encoding="utf-8") == transcript, "dry run writes nothing"
    run(SCRIPTS / "transcript_sections.py", "--root", root, "--write")
    new = note.read_text(encoding="utf-8")
    assert [l for l in new.splitlines() if l.startswith("## ")] == ["## 00:00:00", "## 00:10:00", "## 00:20:00"], new
    stripped = "\n".join(l for l in new.split("\n") if not l.startswith("## "))
    assert stripped.replace("\n\n\n\n", "\n\n").replace("\n\n\n", "\n\n") == transcript, "text unchanged apart from headings"
    run(SCRIPTS / "transcript_sections.py", "--root", root, "--write")
    assert note.read_text(encoding="utf-8") == new, "second run changes nothing"

    vtt = root / "lesson.vtt"
    vtt.write_text("WEBVTT\n\n1\n00:00:01.000 --> 00:00:03.000\n<v Ana>Hello and\n\n2\n00:00:03.000 --> 00:00:05.000\n<v Ana>welcome.\n\n"
                   "3\n00:11:00.000 --> 00:11:02.000\nBob: A question?\n\n"
                   "3b\n00:12:00.000 --> 00:12:02.000\nBob: An answer.\n\n"
                   "4\n00:22:00.000 --> 00:22:02.000\nThanks.\n", encoding="utf-8")
    out = run(SCRIPTS / "vtt_to_note.py", vtt, "--track", "01_T", "--root", root, "--write")
    assert out.returncode == 0, out.stdout + out.stderr
    made = (folder / "lesson.md").read_text(encoding="utf-8")
    assert "**[0:00:01] Ana:** Hello and welcome." in made, made
    assert "**[0:11:00] Bob:** A question?" in made and "**[0:22:00]** Thanks." in made, made
    caption = root / "caption.vtt"
    caption.write_text("WEBVTT\n\n1\n00:00:01.000 --> 00:00:03.000\nNote: the spacing effect is about one day.\n\n"
                        "2\n00:00:04.000 --> 00:00:06.000\nNote: the effect is about one day.\n\n", encoding="utf-8")
    run(SCRIPTS / "vtt_to_note.py", caption, "--track", "01_T", "--root", root, "--write")
    note_text = (folder / "caption.md").read_text(encoding="utf-8")
    assert "Note: the spacing effect" in note_text, note_text
    assert "**[0:00:01] Note:**" not in note_text, note_text
    assert "## 00:00:01" in made and "## 00:11:00" in made and "type: transcript" in made, made
    assert run(SCRIPTS / "vtt_to_note.py", vtt, "--track", "01_T", "--root", root, "--write").returncode == 1, "never overwrite"
print("ok: 9 checks")
