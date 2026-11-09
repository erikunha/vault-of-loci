"""Find the recurring confusions in the attempt ledger, and the exercises that would separate them.

A wrong answer once is noise. The same objective wrong again and again is a confusion, and a
confusion is not fixed by repeating the same card: it needs two items that look alike, so the
learner has to say which one applies and why.

This module groups the wrong attempts by objective, counts them, and lists the open mistakes the
learner logged in `50_Review/Mistakes.md`. It never grades and never writes. The skill uses the
list to propose a discriminating exercise, and the learner decides.

Standard library only.
"""
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from learning_ledger import parse_when  # noqa: E402
from scheduler import clean_attempts  # noqa: E402

MISTAKES = Path(__file__).resolve().parents[2] / "50_Review" / "Mistakes.md"
ENTRY = re.compile(r"^(?P<date>\d{4}-\d{2}-\d{2}),\s*\[\[(?P<concept>[^\]|]+)(?:\|[^\]]*)?\]\]:\s*(?P<rest>.*)$")
KINDS = ("knowledge", "reasoning", "execution", "careless")
AI_ROLES = ("scaffold", "substitute", "none")


def wrong_attempts(events):
    """The attempts that were wrong, with the objective and the day."""
    wrong = []
    for event in events:
        if event.get("mode") == "study":
            continue
        if event.get("first_attempt_correct") is not False:
            continue
        wrong.append(event)
    wrong.sort(key=lambda event: (str(event.get("occurred_at")), str(event.get("event_id"))))
    return wrong


def open_mistakes(path=MISTAKES):
    """The mistakes the learner logged and has not closed yet."""
    try:
        text = Path(path).read_text(encoding="utf-8")
    except OSError:
        return []
    mistakes = []
    for line in text.splitlines():
        match = ENTRY.match(line.strip())
        if not match:
            continue
        rest = match.group("rest")
        if re.search(r"\bclosed\b", rest):
            continue
        kind = next((k for k in KINDS if re.search(rf"\b{k}\b", rest)), None)
        role = next((a for a in AI_ROLES if re.search(rf"\b{a}\b", rest)), None)
        mistakes.append({
            "date": match.group("date"),
            "concept": match.group("concept").strip(),
            "kind": kind,
            "ai": role,
            "text": rest,
        })
    return mistakes


def same_name(left, right):
    """True when two names point at the same thing, ignoring case, spaces and punctuation."""
    def norm(text):
        return re.sub(r"[^a-z0-9]", "", str(text).lower())
    left, right = norm(left), norm(right)
    return bool(left) and bool(right) and (left in right or right in left)


def confusions(events, mistakes=None, min_wrong=2, today=None):
    """The objectives that were wrong more than once, with the open mistakes that name them."""
    today = today or date.today()
    mistakes = mistakes if mistakes is not None else open_mistakes()
    grouped = {}
    for event in wrong_attempts(events):
        grouped.setdefault(event.get("objective_id"), []).append(event)
    rows = []
    for objective, attempts in sorted(grouped.items(), key=lambda pair: str(pair[0])):
        if len(attempts) < min_wrong:
            continue
        helped = [event for event in attempts if event.get("assistance") != "none"]
        last = attempts[-1]
        when = parse_when(last.get("occurred_at"))
        rows.append({
            "objective_id": objective,
            "wrong": len(attempts),
            "wrong_with_help": len(helped),
            "first_wrong": attempts[0].get("occurred_at"),
            "last_wrong": last.get("occurred_at"),
            "days_since": (today - when).days if when else None,
            "items": sorted({str(event.get("item_id")) for event in attempts}),
            "open_mistakes": [mistake for mistake in mistakes
                              if same_name(objective, mistake["concept"])],
            "exercise": "two items that look alike: the learner says which one applies and why",
        })
    rows.sort(key=lambda row: (-row["wrong"], -(row["days_since"] or 0)))
    return rows


if __name__ == "__main__":
    print(__doc__)
    sys.exit(0)
