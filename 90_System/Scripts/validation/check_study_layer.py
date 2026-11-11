"""Study layer in concept, reference and guide notes.

Rule (90_System/Specs/Study_layer.md): every concept, reference and guide note in 20_Concepts and
40_References has the explanation heading as its first ## section and the takeaways heading right
after it. A note with another `type` (for example a track or a log) is not checked.
The headings, the checked types and the folders live in 90_System/Specs/study_layer.json; without that
file the built-in values apply. Exits 1 on any note that lacks the layer or has it out of order, and on
an invalid study_layer.json.

Usage: python3 -I 90_System/Scripts/validation/check_study_layer.py [root]
"""
import json
import re
import sys
from pathlib import Path

VAULT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[3]
CONFIG = VAULT / "90_System" / "Specs" / "study_layer.json"
DEFAULTS = {
    "explanation": "## Study explanation",
    "takeaways": "## Key takeaways",
    "checked_types": ["concept", "reference", "guide"],
    "folders": ["20_Concepts", "40_References"],
}


def load_config():
    """Built-in values overridden by study_layer.json. Raises ValueError with a readable reason."""
    config = dict(DEFAULTS)
    if not CONFIG.is_file():
        return config
    try:
        data = json.loads(CONFIG.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise ValueError(f"cannot read study_layer.json: {error}") from error
    if not isinstance(data, dict):
        raise ValueError("study_layer.json must hold one JSON object")
    for key, default in DEFAULTS.items():
        if key not in data:
            continue
        value = data[key]
        ok = isinstance(value, str) if isinstance(default, str) else (
            isinstance(value, list) and all(isinstance(v, str) for v in value))
        if not ok or not value:
            raise ValueError(f"study_layer.json: {key} must be a non-empty {'string' if isinstance(default, str) else 'list of strings'}")
        config[key] = value
    return config


try:
    CONFIG_VALUES = load_config()
except ValueError as error:
    print(error)
    print("study layer problems: 1")
    sys.exit(1)
EXPLAIN, TAKEAWAYS = CONFIG_VALUES["explanation"], CONFIG_VALUES["takeaways"]
CHECKED_TYPES = set(CONFIG_VALUES["checked_types"])


def note_type(head):
    """The `type` of a note, in the inline form and in the list form.

    The type is one value. A note that writes it as a list is read from the first item, and
    the comparison with the checked types ignores the case, so a note that writes "Concept"
    is a concept note and not a note of another type.
    """
    lines = head.splitlines()
    for index, line in enumerate(lines):
        match = re.match(r"^type:[ \t]*(.*)$", line)
        if not match:
            continue
        value = match.group(1).strip().strip("'\"")
        if value:
            return value
        for follow in lines[index + 1:]:
            item = re.match(r"^[ \t]*-[ \t]*(.*)$", follow)
            if not item:
                break
            value = item.group(1).strip().strip("'\"")
            if value:
                return value
    return ""


def problem(text):
    """None when the note is fine, else a short reason."""
    front = re.match(r"---\n(.*?)\n---", text, flags=re.DOTALL)
    head = front.group(1) if front else ""
    kind = note_type(head)
    # A note with another type (a track or a log, for example) is not checked. A note without
    # frontmatter and a note without a type are checked, because there is no type to skip.
    if kind and kind.casefold() not in CHECKED_TYPES:
        return None
    body = re.sub(r"(?ms)^(`{3,}|~{3,}).*?^\1\s*$", "", text[front.end():] if front else text)
    sections = re.findall(r"(?m)^## .*$", body)
    if EXPLAIN not in sections:
        return "missing"
    if sections[:2] != [EXPLAIN, TAKEAWAYS]:
        return "out of order"
    # The first item of the order is the callout of three lines, right after the title.
    head = body.split("## ", 1)[0]
    if not re.search(r"(?m)^>\s*\[!tldr\]", head):
        return "no tldr callout"
    return None


bad = []
for folder in CONFIG_VALUES["folders"]:
    for p in sorted((VAULT / folder).rglob("*.md")):
        reason = problem(p.read_text(encoding="utf-8"))
        if reason:
            bad.append((reason, p.relative_to(VAULT)))
for reason, path in bad:
    print(f"study layer {reason}:", path)
print("study layer problems:", len(bad))
sys.exit(1 if bad else 0)
