"""Keep the contributors table in the READMEs, in the All Contributors format.

`.all-contributorsrc` (the format of the All Contributors spec) lists every contributor and the kinds
of contribution: content, translation, ideas, review, docs, code and more. This script adds every
commit author from the GitHub API (bots left out) with `code`, keeps the entries added by hand, and
writes a table between the ALL-CONTRIBUTORS-LIST markers of each file in `files`: a 100 px avatar
(fetched at 200 px, so it stays sharp), the name, and one emoji per kind of contribution. People
with more kinds come first. A second run with the same data changes nothing.

To credit someone who did not commit (an idea, a review, a translation check), add an entry to
`.all-contributorsrc` by hand and run the script. `.github/workflows/contributors.yml` runs it on
every push to main and weekly.

Usage: python3 -I 90_System/Scripts/update_contributors.py [--repo owner/name]
       python3 -I 90_System/Scripts/update_contributors.py --from-json api.json --users-json users.json   (offline)
"""
import argparse
import json
import os
import re
import urllib.request
from html import escape
from pathlib import Path

START = "<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->"
END = "<!-- ALL-CONTRIBUTORS-LIST:END -->"
KINDS = {
    "content": ("🖋", "Content"), "doc": ("📖", "Documentation"), "translation": ("🌍", "Translation"),
    "research": ("🔬", "Research"), "ideas": ("🤔", "Ideas, Planning, & Feedback"), "review": ("👀", "Reviewed Pull Requests"),
    "bug": ("🐛", "Bug reports"), "question": ("💬", "Answering Questions"), "example": ("💡", "Examples"),
    "code": ("💻", "Code"), "test": ("⚠️", "Tests"), "infra": ("🚇", "Infrastructure"), "maintenance": ("🚧", "Maintenance"),
    "tutorial": ("✅", "Tutorials"), "design": ("🎨", "Design"), "a11y": ("♿", "Accessibility"),
}


def api(url):
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "vault-of-loci"})
    if os.environ.get("GITHUB_TOKEN"):
        req.add_header("Authorization", f"Bearer {os.environ['GITHUB_TOKEN']}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def merge(rc, authors, users):
    people = {c["login"]: c for c in rc["contributors"]}
    for a in authors:
        if a.get("type") == "Bot" or a["login"].endswith("[bot]"):
            continue
        entry = people.get(a["login"])
        if entry is None:
            info = users(a["login"])
            entry = {"login": a["login"], "name": info.get("name") or a["login"], "avatar_url": a["avatar_url"],
                     "profile": info.get("blog") or a["html_url"], "contributions": []}
            rc["contributors"].append(entry)
            people[a["login"]] = entry
        if "code" not in entry["contributions"]:
            entry["contributions"].append("code")
    return rc


def cell(c, repo, width):
    sep = "&" if "?" in c["avatar_url"] else "?"
    badges = []
    for kind in c["contributions"]:
        emoji, title = KINDS.get(kind, ("✨", kind))
        href = f"https://github.com/{repo}/commits?author={c['login']}" if kind in ("code", "doc", "test") else f"#{kind}-{c['login']}"
        badges.append(f'<a href="{escape(href)}" title="{escape(title)}">{emoji}</a>')
    return (f'      <td align="center" valign="top" width="{width}"><a href="{escape(c["profile"])}">'
            f'<img src="{escape(c["avatar_url"])}{sep}s=200" width="100px;" alt="{escape(c["name"])}"/>'
            f'<br /><sub><b>{escape(c["name"])}</b></sub></a><br />{" ".join(badges)}</td>')


def table(rc, repo):
    per = rc.get("contributorsPerLine", 7)
    width = f"{100 / per:.2f}%"
    people = sorted(rc["contributors"], key=lambda c: (-len(c["contributions"]), c["name"].lower()))
    rows = []
    for i in range(0, len(people), per):
        rows.append("    <tr>\n" + "\n".join(cell(c, repo, width) for c in people[i:i + per]) + "\n    </tr>")
    return (START + "\n<!-- prettier-ignore-start -->\n<!-- markdownlint-disable -->\n<table>\n  <tbody>\n"
            + "\n".join(rows) + "\n  </tbody>\n</table>\n\n<!-- markdownlint-restore -->\n<!-- prettier-ignore-end -->\n\n" + END)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    ap.add_argument("--repo", default="erikunha/vault-of-loci")
    ap.add_argument("--from-json", type=Path, help="commit authors from a saved API answer (offline)")
    ap.add_argument("--users-json", type=Path, help="user profiles from a file (offline)")
    args = ap.parse_args()
    rc_path = args.root / ".all-contributorsrc"
    rc = json.loads(rc_path.read_text(encoding="utf-8"))
    authors = json.loads(args.from_json.read_text(encoding="utf-8")) if args.from_json else api(f"https://api.github.com/repos/{args.repo}/contributors?per_page=100")
    saved = json.loads(args.users_json.read_text(encoding="utf-8")) if args.users_json else None
    users = (lambda login: saved.get(login, {})) if saved is not None else (lambda login: api(f"https://api.github.com/users/{login}"))
    rc = merge(rc, authors, users)
    new_rc = json.dumps(rc, indent=2, ensure_ascii=False) + "\n"
    if new_rc != rc_path.read_text(encoding="utf-8"):
        rc_path.write_text(new_rc, encoding="utf-8")
        print("updated: .all-contributorsrc")
    block = table(rc, args.repo)
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
    for name in rc.get("files", ["README.md"]):
        path = args.root / name
        text = path.read_text(encoding="utf-8")
        updated = pattern.sub(lambda m: block, text)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
        print(("updated: " if updated != text else "unchanged: ") + name)


if __name__ == "__main__":
    main()
