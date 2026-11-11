"""Export reference notes to BibTeX and CSL JSON for Zotero, Pandoc or LaTeX.

Reads every note with `type: reference` and uses its frontmatter: `subtype` (paper, book,
repository, web), `authors`, `year`, `venue`, `doi`, `arxiv`, `link`,
`verified`. The title is the note's `# heading` without a trailing `(Author, year)`. A note with `verified: false` gets
`note = {not verified}`, in the BibTeX and in the CSL JSON. Keys are the first author's last name plus the year.

The authors are separated by a comma and by " and ". A name is either a surname alone
("Mawson") or a full name ("Henry L. Roediger III"). The form "Surname, Given name" is one
author, and it is read when the part before the comma is a surname alone and the part after it
is a given name: an initial ("J.") or a name of two or more words ("Henry L."). Two surnames
side by side are two authors, so "Goncalves, Muniz and Jaeger" is three people and not two.
A given name of one word is read as another author, and a surname with a particle
("van der Waals") is read as a full name. The same list of authors goes to the BibTeX and to
the CSL JSON.

In the CSL JSON every author carries a family name and, when the note has one, a given name.
A name of one part is a family name alone. Zotero reads a `literal` name as an institution and
does not parse it, so a person never goes out as a `literal`. The suffix of a name goes with the
given name, because Zotero has no field of its own for it.

In the BibTeX the name is the surname first and then the given name, the form every reader of
BibTeX understands. The surname of "Henry L. Roediger III" is Roediger, and the last word of a
name is not the surname.

Dry run by default: prints the BibTeX. `--out refs.bib` and `--csl-out refs.json` write files.

Usage: python3 -I 90_System/Scripts/export_bibtex.py [--root DIR] [--out refs.bib] [--csl-out refs.json]
"""
import argparse
import json
import re
from pathlib import Path

KINDS = {"paper": ("article", "article-journal"), "book": ("book", "book")}
SUFFIXES = {"jr", "jr.", "sr", "sr.", "ii", "ii.", "iii", "iii.", "iv", "iv."}


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


def is_initial(word):
    """Whether a word is an initial, the way a name writes a given name short."""
    bare = word.rstrip(".")
    return len(bare) == 1 and bare.isalpha()


def is_given(part):
    """Whether the part after a comma carries a given name instead of another author.

    A given name shows up as an initial ("J.") or as a name of two or more words ("Henry L.").
    A surname alone ("Muniz") is another author, because the vault lists surnames side by side.
    """
    words = part.split()
    if any(is_initial(word) for word in words):
        return True
    return len(words) > 1


def given_of(part):
    """The given name of a name written "Surname, Given name", and its suffix."""
    words = part.split()
    suffix = ""
    while words and words[-1].casefold() in SUFFIXES:
        suffix = words.pop()
    return " ".join(words), suffix


def split_name(text):
    """A name into a family name, a given name and a suffix.

    A name written "Given name Surname" carries the surname last, and a name of one word is a
    surname alone. The suffix of a name is not part of it.
    """
    words = text.split()
    suffix_words = []
    while words and words[-1].casefold() in SUFFIXES:
        suffix_words.insert(0, words.pop())
    suffix = " ".join(suffix_words)
    if not words:
        return {"family": text.strip(), "given": "", "suffix": suffix}
    if len(words) == 1:
        return {"family": words[0], "given": "", "suffix": suffix}
    return {"family": words[-1], "given": " ".join(words[:-1]), "suffix": suffix}


def listed_author(item):
    """One author of a list, where the item already says which name it is.

    A list gives the authors one by one, so a comma inside an item separates the surname from
    the given name and never two authors.
    """
    if "," in item:
        family, _, rest = item.partition(",")
        given, suffix = given_of(rest.strip())
        return {"family": family.strip(), "given": given, "suffix": suffix}
    return split_name(item)


def split_group(group):
    """The authors of one group, the part of the note that sits between two " and ".

    A comma separates two authors, unless the part before it is a surname alone and the part
    after it is a given name, because then the two are one author written "Surname, Given name".
    """
    parts = [part.strip() for part in group.split(",") if part.strip()]
    authors = []
    index = 0
    while index < len(parts):
        part = parts[index]
        if index + 1 < len(parts) and len(part.split()) == 1 and is_given(parts[index + 1]):
            given, suffix = given_of(parts[index + 1])
            authors.append({"family": part, "given": given, "suffix": suffix})
            index += 2
            continue
        authors.append(split_name(part))
        index += 1
    return authors


def authors_of(value):
    """The authors of a reference, in the order the note writes them.

    The vault separates the authors with a comma and with " and ". A name is either a surname
    alone or a full name, and the form "Surname, Given name" is one author. The same list goes
    to the BibTeX and to the CSL JSON, so the two never name a different set of people.
    """
    value = str(value).strip()
    if value.startswith("["):
        try:
            items = json.loads(value)
        except ValueError:
            items = []
        if isinstance(items, list) and items:
            return [listed_author(str(item).strip().strip("'").strip('"')) for item in items if str(item).strip()]
    authors = []
    for group in re.split(r"\s+and\s+", value):
        authors.extend(split_group(group))
    return authors


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
        base = re.sub(r"\W", "", authors[0]["family"] if authors else path.stem).lower() + year
        key, n = base, 1
        while key in keys:
            n += 1
            key = f"{base}{chr(96 + n)}"
        keys.add(key)
        entries.append({"key": key, "title": title, "authors": authors, "year": year, "meta": meta})
    return entries


def bibtex_name(author):
    """The name of an author in the BibTeX form, the surname first and then the given name.

    BibTeX reads the last word of a name as the surname, so "Henry L. Roediger III" would make
    "III" the surname of the entry, and LaTeX and Pandoc would print "III, H. L. R.". The
    surname first keeps the readers in agreement. A name of one part is a surname alone, because
    BibTeX reads a name that ends with a comma as an error.
    """
    given = " ".join(part for part in (author["given"], author["suffix"]) if part)
    return f'{author["family"]}, {given}' if given else author["family"]


def bibtex(entry):
    meta = entry["meta"]
    kind = KINDS.get(meta.get("subtype"), ("misc", "webpage"))[0]
    fields = {"title": "{" + entry["title"] + "}", "author": " and ".join(bibtex_name(a) for a in entry["authors"]), "year": entry["year"]}
    if meta.get("venue"):
        fields["journal" if kind == "article" else "publisher" if kind == "book" else "howpublished"] = meta["venue"]
    fields["doi"] = meta.get("doi", "")
    fields["eprint"] = meta.get("arxiv", "")
    fields["url"] = meta.get("link", "")
    if meta.get("verified") == "false":
        fields["note"] = "not verified"
    body = ",\n".join(f"  {k} = {{{v}}}" for k, v in fields.items() if v)
    return f"@{kind}{{{entry['key']},\n{body}\n}}"


def csl_name(author):
    """A name for the CSL JSON, with a family name and, when there is one, a given name.

    Zotero reads a `literal` name as an institution and does not parse it, so a person needs a
    family name. A name of one part is a family name alone.
    """
    name = {"family": author["family"]}
    given = " ".join(part for part in (author["given"], author["suffix"]) if part)
    if given:
        name["given"] = given
    return name


def csl(entry):
    meta = entry["meta"]
    item = {"id": entry["key"], "type": KINDS.get(meta.get("subtype"), ("misc", "webpage"))[1], "title": entry["title"]}
    item["author"] = [csl_name(a) for a in entry["authors"]]
    if entry["year"].isdigit():
        item["issued"] = {"date-parts": [[int(entry["year"])]]}
    for src, dst in (("venue", "container-title"), ("doi", "DOI"), ("link", "URL")):
        if meta.get(src):
            item[dst] = meta[src]
    if meta.get("verified") == "false":
        item["note"] = "not verified"
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
