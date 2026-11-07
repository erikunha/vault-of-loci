"""Write the contributors grid into every README that has the markers.

Reads the contributors of the GitHub repository (most contributions first, bots left out) and
writes a row of sharp avatars between `<!-- contributors:start -->` and `<!-- contributors:end -->`
in README.md and each README.<lang>.md. Avatars are requested at 160 px and shown at 80 px, so
they stay sharp on high-density screens. Only the block between the markers changes, and a second
run with the same contributors changes nothing. `.github/workflows/contributors.yml` runs it.

Usage: python3 -I 90_System/Scripts/update_contributors.py [--repo owner/name] [--from-json api.json]
"""
import argparse
import json
import os
import re
import urllib.request
from html import escape
from pathlib import Path

START, END = "<!-- contributors:start -->", "<!-- contributors:end -->"


def fetch(repo):
    req = urllib.request.Request(f"https://api.github.com/repos/{repo}/contributors?per_page=100",
                                 headers={"Accept": "application/vnd.github+json", "User-Agent": "vault-of-loci"})
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def block(people):
    cells = []
    for p in people:
        if p.get("type") == "Bot" or p["login"].endswith("[bot]"):
            continue
        login = escape(p["login"])
        sep = "&" if "?" in p["avatar_url"] else "?"
        cells.append(f'<a href="{escape(p["html_url"])}"><img src="{escape(p["avatar_url"])}{sep}s=160" width="80" height="80" alt="{login}" title="{login}" /></a>')
    return START + "\n" + "\n".join(cells) + "\n" + END


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    ap.add_argument("--repo", default="erikunha/vault-of-loci")
    ap.add_argument("--from-json", type=Path, help="read the API answer from a file instead of the network")
    args = ap.parse_args()
    people = json.loads(args.from_json.read_text(encoding="utf-8")) if args.from_json else fetch(args.repo)
    new = block(people)
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
    for readme in sorted(args.root.glob("README*.md")):
        text = readme.read_text(encoding="utf-8")
        if START not in text:
            continue
        updated = pattern.sub(lambda m: new, text)
        if updated != text:
            readme.write_text(updated, encoding="utf-8")
            print("updated:", readme.name)
        else:
            print("unchanged:", readme.name)


if __name__ == "__main__":
    main()
