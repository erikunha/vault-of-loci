"""AGENTS.md keeps the tutor-mode rules the eval in 90_System/Evals/Tutor_mode.md tests.

Each rule is matched by a phrase, so rewording is free but deleting a rule fails. The "just tell me"
rule exists because an agent explained a concept before any attempt when the learner asked it to.
"""
from pathlib import Path

TEXT = (Path(__file__).resolve().parents[3] / "AGENTS.md").read_text(encoding="utf-8").lower()
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
}
missing = [name for name, phrase in RULES.items() if phrase not in TEXT]
assert not missing, f"AGENTS.md lost tutor-mode rules: {missing}"
print(f"ok: {len(RULES)} rules")
