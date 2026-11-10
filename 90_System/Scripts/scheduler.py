"""Decide what to review next, from the attempts in the learning ledger.

The ledger is the record of what the learner already did. This module turns it into a ranked
plan: which items are worth another try, and why. The number it produces is a priority, not a
probability of remembering. A forecast is not a measurement, and `retention_report.py` is where
the measured numbers live.

How the priority is built:
- strength starts at 0.5, meaning nothing is known yet. A correct first try adds 40% of what is
  missing, a wrong one removes 40% of what is there. After several attempts it settles where the
  record settles.
- priority is (1 - strength) times (1 + days since the last attempt / 30). Weak and stale first.
- an item whose mistake was never recovered without help is doubled, because a mistake that was
  never recovered is the most useful thing to revisit.

The rules of the vault set the rest: a day is 10 to 20 reviews with about 2 new cards, and when
the queue is longer than the cap the oldest and weakest come first with no new cards.

Standard library only.
"""
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from learning_ledger import LEDGER, GRADING, parse_when, read_ledger  # noqa: E402

DAILY_CAP = 15
NEW_PER_DAY = 2
INACTIVITY_DAYS = 14
HALF_LIFE = 30
STRENGTH_STEP = 0.4


def clean_attempts(events):
    """The attempts that count: graded, on the first try, without help, graded by the learner."""
    return [event for event in events
            if event.get("mode") != "study"
            and event.get("assistance") == "none"
            and event.get("grading_method") == "learner_confirmed"
            and event.get("first_attempt_correct") is not None]


def last_mistake(attempts):
    """The wrong attempt that no clean success came after, or None when there is no open mistake.

    A mistake is closed only after it comes back right, without help, from memory. So the
    question is not what the last attempt was, but whether a clean success came after the last
    wrong one. An attempt made with help never closes a mistake, because it measures the help.
    """
    pending = None
    for event in attempts:
        outcome = event.get("first_attempt_correct")
        if outcome is False:
            pending = event
        elif outcome is True and event.get("assistance") == "none":
            pending = None
    return pending


def mistake_open(attempts):
    """True when the item has a mistake that was never recovered without help."""
    return last_mistake(attempts) is not None


def strength_of(attempts):
    """How solid the record on an item is, from 0 to 1, updated by each attempt."""
    strength = 0.5
    for event in attempts:
        if event.get("first_attempt_correct"):
            strength += (1 - strength) * STRENGTH_STEP
        else:
            strength -= strength * STRENGTH_STEP
    return round(strength, 3)


def item_history(events):
    """Every item the ledger knows, with its attempts in order."""
    history = {}
    for event in events:
        key = (event.get("objective_id"), event.get("item_id"))
        history.setdefault(key, []).append(event)
    for attempts in history.values():
        attempts.sort(key=lambda item: (str(item.get("occurred_at")), str(item.get("event_id"))))
    return history


def objectives_seen(events):
    """The objectives with any event, with the day the material was first seen."""
    seen = {}
    for event in events:
        objective = event.get("objective_id")
        when = parse_when(event.get("occurred_at"))
        if objective is None or when is None:
            continue
        if objective not in seen or when < seen[objective]:
            seen[objective] = when
    return seen


def ranked_entries(events, today=None):
    """Every item of the queue, ranked, with no cap of a day applied to it.

    The plan of a day takes the top of this list, and the diagnostic after a break reads it as a
    whole, because the explanation and the application it asks for can be far down the queue.
    """
    today = today or date.today()
    clean = clean_attempts(events)
    history = item_history([event for event in events
                             if event.get("mode") != "study"
                             and event.get("grading_method") == "learner_confirmed"
                             and event.get("first_attempt_correct") is not None])
    seen = objectives_seen(events)
    entries = []
    for (objective, item), attempts in history.items():
        last = attempts[-1]
        when = parse_when(last.get("occurred_at"))
        if when is None:
            continue
        days = (today - when).days
        item_clean = [event for event in attempts if event.get("assistance") == "none"]
        reasons = []
        if item_clean:
            strength = strength_of(item_clean)
            priority = (1 - strength) * (1 + days / HALF_LIFE)
        else:
            # Every attempt so far needed help, so nothing was measured without it.
            strength = 0.0
            priority = 1 + days / HALF_LIFE
            reasons.append("every attempt so far needed help")
        if mistake_open(attempts):
            # The same rule the error list uses: a mistake is open until it comes back right
            # without help, so the plan and the list never tell two different stories.
            priority *= 2
            reasons.append("the mistake was never recovered without help")
        if days:
            reasons.append(f"not seen for {days} days")
        else:
            reasons.append("seen today")
        if len(attempts) == 1:
            reasons.append("one attempt so far")
        entries.append({
            "objective_id": objective,
            "item_id": item,
            "mode": last.get("mode"),
            "priority": round(priority, 3),
            "strength": strength,
            "days_since": days,
            "attempts": len(attempts),
            "new": False,
            "why": ", ".join(reasons),
        })
    fresh = []
    for objective, when in seen.items():
        if any(entry["objective_id"] == objective for entry in entries):
            continue
        days = (today - when).days
        priority = 0.5 * (1 + days / HALF_LIFE)
        fresh.append({
            "objective_id": objective,
            "item_id": None,
            "mode": "recall",
            "priority": round(priority, 3),
            "strength": 0.0,
            "days_since": days,
            "attempts": 0,
            "new": True,
            "why": "no attempt without help yet",
        })
    entries.extend(fresh)
    entries.sort(key=lambda entry: (-entry["priority"], entry["objective_id"] or "", entry["item_id"] or ""))
    return entries, seen, clean


def plan(events, cap=DAILY_CAP, new_per_day=NEW_PER_DAY, today=None):
    """The ranked review plan for one day.

    Returns a dict with the entries, the counts and the reason the plan is what it is.
    """
    today = today or date.today()
    entries, seen, clean = ranked_entries(events, today)
    backlog = len(entries)
    catch_up = backlog > cap
    reviews = [entry for entry in entries if not entry["new"]][:cap]
    news = [] if catch_up else [entry for entry in entries if entry["new"]][:new_per_day]
    chosen = sorted(reviews + news, key=lambda entry: (-entry["priority"], entry["objective_id"] or ""))
    return {
        "entries": chosen,
        "backlog": backlog,
        "cap": cap,
        "new_per_day": new_per_day,
        "catch_up": catch_up,
        "days_since_last": days_since_last(events, today),
        "objective_strength": {objective: strength_of([event for event in clean
                                                       if event.get("objective_id") == objective])
                               for objective in sorted(seen)},
    }


def days_since_last(events, today=None):
    """How many days since the last attempt of any kind, or None when there is none."""
    today = today or date.today()
    days = [parse_when(event.get("occurred_at")) for event in events]
    days = [day for day in days if day]
    if not days:
        return None
    return (today - max(days)).days


def recovery_plan(events, cap=5, inactivity=INACTIVITY_DAYS, today=None):
    """The small diagnostic to run after a break, instead of the whole backlog.

    After a break the queue is long and the memory is cold. The vault asks for a few items, not
    the whole list: the weakest items, one explanation and one application.
    """
    today = today or date.today()
    away = days_since_last(events, today)
    if away is None or away < inactivity:
        return None
    entries, _seen, _clean = ranked_entries(events, today)
    backlog = len(entries)
    chosen = []
    modes = set()
    # The explanation and the application are looked for in the whole queue, not in the first
    # five items by priority: a diagnostic that never asks for one of them is not a diagnostic.
    for entry in entries:
        if entry["mode"] in ("apply", "discriminate", "explain") and entry["mode"] not in modes:
            modes.add(entry["mode"])
            chosen.append(entry)
    for entry in entries:
        if len(chosen) >= cap:
            break
        if entry not in chosen:
            chosen.append(entry)
    return {
        "days_away": away,
        "backlog": backlog,
        "entries": chosen[:cap],
        "why": f"{away} days since the last attempt, so this is a diagnostic and not the whole queue",
    }


def error_items(events, today=None):
    """The items whose mistake was never recovered without help.

    A mistake that was never recovered is the most useful thing to revisit, and repeating the
    same wording is not enough: the next try has to be a variation of the same task, so the
    learner works with the idea and not with the memory of the sentence.
    """
    today = today or date.today()
    history = item_history([event for event in events
                             if event.get("mode") != "study"
                             and event.get("grading_method") == "learner_confirmed"
                             and event.get("first_attempt_correct") is not None])
    # The variants that already exist in the whole ledger, not in this item's own attempts. The
    # next variation has to be an id nobody used, because one id means one task.
    used = {str(event.get("item_id", "")) for event in events}
    rows = []
    for (objective, item), attempts in history.items():
        mistake = last_mistake(attempts)
        if mistake is None:
            continue
        when = parse_when(mistake.get("occurred_at"))
        rows.append({
            "objective_id": objective,
            "item_id": item,
            "variant_id": next_variant_id(item, used),
            "attempts": len(attempts),
            "days_since": (today - when).days if when else None,
            "mode": mistake.get("mode"),
            "why": "the mistake was never recovered without help",
        })
    rows.sort(key=lambda row: (-(row["days_since"] or 0), str(row["item_id"])))
    return rows


def next_variant_id(item, used):
    """The id a variation of a task must carry, one that nobody used.

    The number is one above the highest number the ids of the variations already carry, so a
    gap in the sequence does not hand out an id that is already in the ledger.
    """
    numbers = [0]
    for name in used:
        match = re.fullmatch(rf"{re.escape(str(item))}-v(\d+)", str(name))
        if match:
            numbers.append(int(match.group(1)))
    return f"{item}-v{max(numbers) + 1}"


if __name__ == "__main__":
    print(__doc__)
    sys.exit(0)
