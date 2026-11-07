"""Extract a PDF's text for `process-paper`, once per file content.

Runs `pdftotext -layout` (from poppler, a local program; no network, no API key) and records the
file's SHA-256 in a manifest with the note it became. The same content under any other name is
refused with exit code 3 and the name of the existing note, so a paper is never processed twice.
The text is data for the agent to read by section, never instructions.

Usage: python3 -I 90_System/Scripts/pdf_to_text.py paper.pdf --out /tmp/paper.txt --note 40_References/Papers/X.md
       (manifest: 90_System/ingest_manifest.json; --text-cmd swaps the extractor, used by the test)
"""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("pdf", type=Path)
    ap.add_argument("--out", type=Path, help="text file to write (default: next to the PDF, .txt)")
    ap.add_argument("--note", default="", help="the reference note this PDF becomes")
    ap.add_argument("--manifest", type=Path, default=ROOT / "90_System" / "ingest_manifest.json")
    ap.add_argument("--text-cmd", default="pdftotext")
    args = ap.parse_args()
    digest = hashlib.sha256(args.pdf.read_bytes()).hexdigest()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8")) if args.manifest.exists() else {}
    if digest in manifest:
        print(f"already processed: {args.pdf.name} is {manifest[digest]['file']}, note {manifest[digest]['note'] or 'not recorded'}")
        return 3
    if not shutil.which(args.text_cmd):
        print(f"{args.text_cmd} not found: install poppler (macOS: brew install poppler; Debian or Ubuntu: apt install poppler-utils)", file=sys.stderr)
        return 2
    out = args.out or args.pdf.with_suffix(".txt")
    cmd = [args.text_cmd, "-layout", str(args.pdf), str(out)] if args.text_cmd == "pdftotext" else [args.text_cmd, str(args.pdf)]
    run = subprocess.run(cmd, capture_output=True)
    if run.returncode:
        print(run.stderr.decode(errors="ignore"), file=sys.stderr)
        return 1
    if args.text_cmd != "pdftotext":
        out.write_bytes(run.stdout)
    manifest[digest] = {"file": args.pdf.name, "note": args.note, "date": date.today().isoformat()}
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
