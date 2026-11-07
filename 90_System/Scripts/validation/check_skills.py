"""Skills follow the Agent Skills specification.

Every folder in .agents/skills has a SKILL.md whose frontmatter has:
- name: the folder name, 1 to 64 characters, lowercase letters, digits and single hyphens, not starting
  or ending with a hyphen;
- description: not empty, at most 1024 characters.
Other keys (license, compatibility, tool settings) are not checked.

Usage: python3 -I 90_System/Scripts/validation/check_skills.py [root]   (exits 1 on any problem)
"""
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[3]
NAME = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*")
NAME_MAX, DESCRIPTION_MAX = 64, 1024


def frontmatter(text):
    """Top-level keys of the frontmatter, or None when there is none. Quotes are removed and a folded
    or literal block (`>` or `|`) is joined into one line."""
    m = re.match(r"---\n(.*?)\n---", text, flags=re.DOTALL)
    if not m:
        return None
    props, current = {}, None
    for line in m.group(1).split("\n"):
        key = re.match(r"([A-Za-z_][\w-]*):\s*(.*)$", line)
        if key:
            current = key.group(1)
            props[current] = key.group(2).strip()
        elif current and line[:1] in (" ", "\t"):
            props[current] = (props[current] + " " + line.strip()).strip()
    for k, v in props.items():
        v = re.sub(r"^[>|][+-]?\s*", "", v)
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
            v = v[1:-1]
        props[k] = v
    return props


def problems_in(folder):
    skill = folder / "SKILL.md"
    if not skill.is_file():
        return ["no SKILL.md"]
    props = frontmatter(skill.read_text(encoding="utf-8", errors="replace"))
    if props is None:
        return ["no frontmatter"]
    found = []
    name = props.get("name", "")
    if not name:
        found.append("name is missing")
    else:
        if len(name) > NAME_MAX:
            found.append(f"name has {len(name)} characters, the limit is {NAME_MAX}")
        if not NAME.fullmatch(name):
            found.append(f"name {name!r} must be lowercase letters, digits and single hyphens")
        if name != folder.name:
            found.append(f"name {name!r} does not match the folder {folder.name!r}")
    if not NAME.fullmatch(folder.name) or len(folder.name) > NAME_MAX:
        found.append(f"folder name {folder.name!r} is not a valid skill name")
    description = props.get("description", "")
    if not description:
        found.append("description is missing or empty")
    elif len(description) > DESCRIPTION_MAX:
        found.append(f"description has {len(description)} characters, the limit is {DESCRIPTION_MAX}")
    return found


bad = []
skills = root / ".agents" / "skills"
for folder in sorted(p for p in skills.iterdir() if p.is_dir()) if skills.is_dir() else []:
    for reason in problems_in(folder):
        bad.append((folder.relative_to(root), reason))
for folder, reason in bad:
    print(f"skill problem: {folder}: {reason}")
print("skill problems:", len(bad))
sys.exit(1 if bad else 0)
