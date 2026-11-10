"""Export reference notes to BibTeX and CSL JSON for Zotero, Pandoc or LaTeX.

Reads every note with `type: reference` and uses its frontmatter: `subtype` (paper, book,
repository, web), `authors`, `year`, `venue`, `doi`, `arxiv`, `link`,
`verified`. The title is the note's `# heading` without a trailing `(Author, year)`. A note with `verified: false` gets
`note = {not verified}`. Keys are the first author's last name plus the year.

The authors are separated by a comma and by " and ". A name written with a comma inside it,
"Surname, Given name", is one author, and the vault writes that form when the name is the first
of a pair joined by " and ". The same list of authors goes to the BibTeX and to the CSL JSON.

Dry run by default: prints the BibTeX. `--out refs.bib` and `--csl-out refs.json` write files.

Usage: python3 -I 90_System/Scripts/export_bibtex.py [--root DIR] [--out refs.bib] [--csl-out refs.json]
"""
import argparse
import json
import re
from pathlib import Path

KINDS = {"paper": ("article", "article-journal"), "book": ("book", "book")}
SUFFIXES = {"jr", "jr.", "sr", "sr.", "ii", "iii", "iv"}


def frontmatter(text):
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    data = {}
    for line in text[4:end].splitlines():
        m = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if m:
            data[m[1]] = m[2].strip().strip('"')
    return data, text[end + 4:]


def authors_of(value):
    """The authors of a reference, in the order the note writes them.

    The vault separates the authors with a comma and with " and ". A name written with a comma
    inside it, "Surname, Given name", is one author, and the vault writes that form when the
    name is the first of a pair joined by " and ". The same list goes to the BibTeX and to the
    CSL JSON, so the two never name a different set of people.
    """
    value = str(value).strip()
    if value.startswith("["):
        try:
            items = json.loads(value)
        except ValueError:
            items = []
        if isinstance(items, list) and items:
            return [str(item).strip().strip("'\"") for item in items if str(item).strip()]
    groups = [group.strip() for group in re.split(r"\s+and\s+", value) if group.strip()]
    authors = []
    for number, group in enumerate(groups):
        parts = [part.strip() for part in group.split(",") if part.strip()]
        if len(parts) == 2 and number == 0 and len(groups) > 1:
            authors.append(f"{parts[0]}, {parts[1]}")
        else:
            authors.extend(parts)
    return authors


def last_name(author):
    """The surname of an author, the way the key of the entry is built from it.

    A name written "Surname, Given name" carries the surname first, and a name written
    "Given name Surname" carries it last. The suffix of a name is not part of it.
    """
    name = str(author).split(",")[0].strip()
    words = [w for w in name.split() if w.casefold() not in SUFFIXES]
    return words[-1] if words else "anon"


def references(root):
    entries, keys = [], set()
    for path in sorted((root / "40_References").rglob("*.md")):
        meta, body = frontmatter(path.read_text(encoding="utf-8"))
        if meta.get("type") != "reference":
            continue
        title = next((l[2:].strip() for l in body.splitlines() if l.startswith("# ")), path.stem)
        title = re.sub(r"\s*\([^()]*,\s*\d{4}\)$", "", title)
        authors = authors_of(meta.get("authors", ""))
        year = meta.get("year", "")
        base = re.sub(r"\W", "", last_name(authors[0]) if authors else path.stem).lower() + year
        key, n = base, 1
        while key in keys:
            n += 1
            key = f"{base}{chr(96 + n)}"
        keys.add(key)
        entries.append({"key": key, "title": title, "authors": authors, "year": year, "meta": meta})
    return entries


def bibtex(entry):
    meta = entry["meta"]
    kind = KINDS.get(meta.get("subtype"), ("misc", "webpage"))[0]
    fields = {"title": "{" + entry["title"] + "}", "author": " and ".join(entry["authors"]), "year": entry["year"]}
    if meta.get("venue"):
        fields["journal" if kind == "article" else "publisher" if kind == "book" else "howpublished"] = meta["venue"]
    fields["doi"] = meta.get("doi", "")
    fields["eprint"] = meta.get("arxiv", "")
    fields["url"] = meta.get("link", "")
    if meta.get("verified") == "false":
        fields["note"] = "not verified"
    body = ",\n".join(f"  {k} = {{{v}}}" for k, v in fields.items() if v)
    return f"@{kind}{{{entry['key']},\n{body}\n}}"


def csl(entry):
    meta = entry["meta"]
    item = {"id": entry["key"], "type": KINDS.get(meta.get("subtype"), ("misc", "webpage"))[1], "title": entry["title"]}
    item["author"] = [{"literal": a} for a in entry["authors"]]
    if entry["year"].isdigit():
        item["issued"] = {"date-parts": [[int(entry["year"])]]}
    for src, dst in (("venue", "container-title"), ("doi", "DOI"), ("link", "URL")):
        if meta.get(src):
            item[dst] = meta[src]
    return item


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--out", type=Path, help="write BibTeX here")
    parser.add_argument("--csl-out", type=Path, help="write CSL JSON here")
    args = parser.parse_args()
    entries = references(args.root)
    bib = "\n\n".join(bibtex(e) for e in entries) + "\n"
    print(f"references: {len(entries)}")
    if args.out:
        args.out.write_text(bib, encoding="utf-8")
        print("written:", args.out)
    if args.csl_out:
        args.csl_out.write_text(json.dumps([csl(e) for e in entries], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("written:", args.csl_out)
    if not args.out and not args.csl_out:
        print(bib, end="")


if __name__ == "__main__":
    main()
