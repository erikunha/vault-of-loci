"""Search the vault by relevance and return where the answer is, not the answer.

Splits every note into sections at its headings and ranks them with BM25, a standard word-relevance
score, using the standard library only: no embeddings, no service, no network. Each result is
`path:line  heading  (score)`, so the learner or the agent opens the source and reads it. In tutor
mode an agent runs it to find sources after the learner's attempt, never to answer for them.

Usage: python3 -I 90_System/Scripts/search_vault.py "spaced review" [--top 10] [--root PATH]
"""
import argparse
import math
import re
import unicodedata
from collections import Counter
from pathlib import Path

SKIP = {".obsidian", ".git", ".trash", ".venv", ".smart-env", ".claude", ".agents", "node_modules"}
WORD = re.compile(r"[a-z0-9]+")
STOP = set("a an and are as at be by for from has have how in is it its of on or that the this to was what when where which who why with you your".split())


def words(text):
    text = unicodedata.normalize("NFKD", text.lower())
    text = "".join(c for c in text if not unicodedata.combining(c))
    return [w for w in WORD.findall(text) if w not in STOP]


def sections(root):
    for path in sorted(root.rglob("*.md")):
        rel = path.relative_to(root)
        if SKIP.intersection(rel.parts) or rel.name == "INDEX.md" or rel.parts[:2] == ("90_System", "Templates"):
            continue
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        start, heading, body, in_front = 1, path.stem, [], lines[:1] == ["---"]
        for number, line in enumerate(lines, 1):
            if in_front:
                if number > 1 and line == "---":
                    in_front = False
                continue
            if line.startswith("#"):
                if body:
                    yield str(rel), start, heading, body
                start, heading, body = number, line.lstrip("#").strip(), [line]
            else:
                body.append(line)
        if body:
            yield str(rel), start, heading, body


def search(root, query, top):
    docs = [(path, line, heading, Counter(words(" ".join(body) + " " + heading + " " + path))) for path, line, heading, body in sections(root)]
    if not docs:
        return []
    avg = sum(sum(c.values()) for *_, c in docs) / len(docs)
    terms = words(query)
    df = {t: sum(1 for *_, c in docs if t in c) for t in terms}
    scored = []
    for path, line, heading, counts in docs:
        length, score = sum(counts.values()), 0.0
        for t in terms:
            f = counts.get(t, 0)
            if f:
                idf = math.log(1 + (len(docs) - df[t] + 0.5) / (df[t] + 0.5))
                score += idf * f * 2.2 / (f + 1.2 * (0.25 + 0.75 * length / avg))
        if score > 0:
            scored.append((score, path, line, heading))
    return sorted(scored, key=lambda s: (-s[0], s[1], s[2]))[:top]


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("query")
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    args = ap.parse_args()
    results = search(args.root, args.query, args.top)
    if not results:
        print("no match")
    for score, path, line, heading in results:
        print(f"{path}:{line}  {heading}  ({score:.2f})")


if __name__ == "__main__":
    main()
