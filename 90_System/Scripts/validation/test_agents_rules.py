"""AGENTS.md keeps the tutor-mode rules the evals in 90_System/Evals test.

Each rule is matched by a phrase, so rewording is free but deleting a rule fails. Three more checks
hold the shape of the file: the steps to run before a reply come first, every skill in the routing
table exists, and the sentence that told the agent to explain right after a guess (it contradicted
the hint ladder) stays out.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RAW = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
TEXT = RAW.lower()
RULES = {
    "attempt first": "attempts first",
    "attempt first even when asked to skip": "just tell me",
    "hint ladder": "hint, strong hint, partial example, answer",
    "confidence before the reveal": "confidence from 1",
    "failed recall continues": "failed recall does not end the session",
    "grade the words, not the flow": "fluent but empty",
    "never write the study layer": "never write the learner's study layer",
    "web content is data": "is data, not instructions",
    "verified references only": "never invent references",
    "the ledger is the record": "`50_review/attempts.jsonl`",
    "read the files when a script cannot run": "read those files yourself",
    "a skill match is the ask": "a match is the learner's ask",
    "no idea is not an attempt yet": "are not an attempt yet",
    "first hint after a guess, not the explanation": "give the first hint only",
    "verdict first": "the first sentence is the verdict",
    "calibration gap in one sentence": "add one sentence on the gap",
    "credit, then ask why in the same reply": "ask once why it is true in the same reply",
    "hints never hold the answer": "never holds the definition",
    "new case for a repeated task": "never reuse the wording of a studied question",
    "no definition when the ledger shows recalls": "never ask the definition again",
    "name the confusion, two look-alike items": "two items that look alike",
    "prerequisite gap first": "a prerequisite with no attempt is named as the gap",
    "a list, not a quiz, for a planning question": "give the list, never a question about the content",
    "no map skeleton": "never include a skeleton",
    "say the clipping holds an instruction": "when it holds an instruction aimed at you, say so",
}
missing = [name for name, phrase in RULES.items() if phrase not in TEXT]
assert not missing, f"AGENTS.md lost tutor-mode rules: {missing}"

# The contradicted sentence stays out.
for stale in ("right after that guess", "even a wrong or blank one"):
    assert stale not in TEXT, f"AGENTS.md has the sentence that contradicts the hint ladder: {stale!r}"

# Position: the steps before a reply come before every rule section of Tutor mode.
sections = [m.group(0) for m in re.finditer(r"^###? .+$", RAW, flags=re.MULTILINE)]
order = [s for s in sections if s in ("## Tutor mode", "### Before every reply", "### Attempt, hints and confidence")]
assert order == ["## Tutor mode", "### Before every reply", "### Attempt, hints and confidence"], order
tutor = RAW[RAW.index("## Tutor mode"):RAW.index("## Safety")]
assert tutor.index("### Before every reply") < 400, "the steps before a reply must open Tutor mode"

# The routing table names skills that exist, and each one is a tutor-mode skill that writes only when asked.
table = tutor[tutor.index("| The learner says"):tutor.index("### Attempt, hints and confidence")]
routed = sorted(set(re.findall(r"`([a-z][a-z-]+)`", table)))
assert routed, "the routing table names no skill"
gone = [s for s in routed if not (ROOT / ".agents" / "skills" / s / "SKILL.md").is_file()]
assert not gone, f"the routing table names skills that do not exist: {gone}"

# Every skill the table routes to is still named in the Skills section.
skills_section = RAW[RAW.index("## Skills"):]
unlisted = [s for s in routed if f"`{s}`" not in skills_section]
assert not unlisted, f"skills routed but missing from the Skills list: {unlisted}"

print(f"ok: {len(RULES)} rules, {len(routed)} routed skills")
