"""Read, check and measure the learning ledger: the append-only record of the learner's attempts.

The ledger is `50_Review/Attempts.jsonl`. One line is one JSON object and one graded attempt at
one item. `record_attempt.py` appends to it and `retention_report.py` reads it. This module holds
the event schema, the checks and the metrics, so both scripts use the same rules.

A line looks like this:
{"event_id": "attempt-2026-11-09-001", "objective_id": "retrieval-practice-recall",
 "item_id": "retrieval-practice-recall-01", "occurred_at": "2026-11-09T18:00:00-03:00",
 "mode": "recall", "first_attempt_correct": true, "confidence": 4,
 "confidence_probability": 0.75, "hints_used": 0, "assistance": "none",
 "rubric_version": "v1", "grading_method": "learner_confirmed", "source_revision": null,
 "duration_minutes": 12}

Fields:
- event_id: unique id of the line.
- objective_id: id of the learning objective, listed in `90_System/Objectives.json`.
- item_id: id of the question or task. The same id must mean the same task every time.
- occurred_at: ISO 8601 with an offset, for example 2026-11-09T18:00:00-03:00.
- mode: study, recall, explain, apply or discriminate.
- first_attempt_correct: true, false, or null for a study event that was not graded.
- confidence: 1 to 5, the scale the tutor asks for, or null.
- confidence_probability: 0 to 1, when the learner gave a probability, or null.
- hints_used: how many hints the learner took.
- assistance: none, hint, strong_hint, partial_example or answer.
- rubric_version: which rubric graded the attempt.
- grading_method: learner_confirmed or agent_graded.
- source_revision: which version of the material was tested.
- duration_minutes: minutes spent, or null.

Only a first attempt with assistance none and grading_method learner_confirmed counts for
retention and transfer. Anything else is recorded, and the report says it was excluded and why.
"""
import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

VAULT = Path(__file__).resolve().parents[2]
LEDGER = VAULT / "50_Review" / "Attempts.jsonl"
OBJECTIVES = VAULT / "90_System" / "Objectives.json"

MODES = ("study", "recall", "explain", "apply", "discriminate")
ASSISTANCE = ("none", "hint", "strong_hint", "partial_example", "answer")
GRADING = ("learner_confirmed", "agent_graded")
RETENTION_MODES = ("recall", "explain")
TRANSFER_MODES = ("apply", "discriminate")
HORIZONS = (7, 30, 90)
REQUIRED = ("event_id", "objective_id", "item_id", "occurred_at", "mode")


def now_iso():
    """The current local time with an offset, in the format the ledger uses."""
    return datetime.now().astimezone().replace(microsecond=0).isoformat()


def parse_when(value):
    """The date of an ISO 8601 timestamp, or None when it cannot be read."""
    try:
        return datetime.fromisoformat(str(value)).date()
    except (TypeError, ValueError):
        return None


def parse_moment(value):
    """The instant of an ISO 8601 timestamp with an offset, or None when there is no such thing.

    The date of a timestamp and the instant it points at are two different things. An attempt at
    2026-11-11T02:00:00+14:00 is the same moment as 2026-11-10T09:00:00-03:00, and the second one
    is already here. Comparing the dates of the two would call the first one a future attempt.
    """
    try:
        moment = datetime.fromisoformat(str(value))
    except (TypeError, ValueError):
        return None
    return moment if moment.tzinfo is not None else None


def sort_by_moment(events):
    """The events in the order they happened.

    The timestamp is a text with an offset, and two events written in different offsets do not
    sort by their text: 2026-11-08T08:00:00-05:00 is one hour later than
    2026-11-08T09:00:00-03:00. The instant decides the order, and the text is the tie break.
    """
    def key(event):
        moment = parse_moment(event.get("occurred_at"))
        return (moment if moment is not None else datetime.min.replace(tzinfo=timezone.utc),
                str(event.get("occurred_at")), str(event.get("event_id")))

    return sorted(events, key=key)


def next_event_id(existing):
    """An event id that is not in `existing`, built from today's date."""
    today = date.today().isoformat()
    numbers = []
    for event_id in existing:
        if event_id.startswith(f"attempt-{today}-"):
            tail = event_id.rsplit("-", 1)[-1]
            if tail.isdigit():
                numbers.append(int(tail))
    return f"attempt-{today}-{(max(numbers) + 1 if numbers else 1):03d}"


def verdict_of(event):
    """The verdict of an attempt: True, False, or None when the event carries no verdict.

    A verdict that is neither true nor false is not a verdict, so it reads as none. A line
    that writes the word "false" says nothing about what was remembered, and counting it as
    a success would print a rate that no event supports.
    """
    value = event.get("first_attempt_correct")
    return value if isinstance(value, bool) else None


def load_objectives(path=OBJECTIVES):
    """The objective registry as a dict of id to objective, or an empty dict when it is missing."""
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    if not isinstance(data, dict):
        return {}
    entries = data.get("objectives")
    if not isinstance(entries, list):
        return {}
    return {str(item["id"]): item for item in entries if isinstance(item, dict) and item.get("id")}


def validate_event(event, known_objectives=None, used_ids=(), allow_unknown_objective=False):
    """The list of reasons the event is not valid. An empty list means the event is good."""
    problems = []
    for field in REQUIRED:
        if event.get(field) in (None, ""):
            problems.append(f"{field} is required")
    if event.get("mode") not in MODES:
        problems.append(f"mode must be one of {', '.join(MODES)}")
    if event.get("assistance") not in ASSISTANCE:
        problems.append(f"assistance must be one of {', '.join(ASSISTANCE)}")
    if event.get("grading_method") not in GRADING:
        problems.append(f"grading_method must be one of {', '.join(GRADING)}")
    correct = event.get("first_attempt_correct")
    if event.get("mode") == "study":
        if correct is not None:
            problems.append("a study event is not graded, so first_attempt_correct must be null")
    elif not isinstance(correct, bool):
        problems.append("first_attempt_correct must be true or false for a graded mode")
    confidence = event.get("confidence")
    if confidence is not None and not (isinstance(confidence, int) and not isinstance(confidence, bool)
                                       and 1 <= confidence <= 5):
        problems.append("confidence must be an integer from 1 to 5, or null")
    probability = event.get("confidence_probability")
    if probability is not None and not (isinstance(probability, (int, float)) and not isinstance(probability, bool)
                                        and 0 <= probability <= 1):
        problems.append("confidence_probability must be a number from 0 to 1, or null")
    hints = event.get("hints_used", 0)
    if not isinstance(hints, int) or hints < 0:
        problems.append("hints_used must be 0 or more")
    if hints and event.get("assistance") == "none":
        problems.append("assistance none with hints used is a contradiction")
    minutes = event.get("duration_minutes")
    if minutes is not None and (not isinstance(minutes, (int, float)) or minutes < 0):
        problems.append("duration_minutes must be 0 or more, or null")
    moment = parse_moment(event.get("occurred_at"))
    if moment is None:
        problems.append("occurred_at must be an ISO 8601 timestamp with an offset")
    elif moment > datetime.now().astimezone():
        problems.append("occurred_at is in the future")
    if known_objectives is not None and not allow_unknown_objective:
        if event.get("objective_id") not in known_objectives:
            problems.append(f"objective {event.get('objective_id')!r} is not in the objective registry")
    if event.get("event_id") in used_ids:
        problems.append(f"event_id {event.get('event_id')!r} is already in the ledger")
    return problems


def problem_lines(problems):
    """The lines that tell the reader which lines of the ledger could not be read.

    Every report that reads the ledger shows these, so a line that could not be parsed never
    disappears silently and the report never counts an attempt that was not read.
    """
    if not problems:
        return []
    return ["", "Ledger lines that could not be read:"] + [f"  - {problem}" for problem in problems]


def read_ledger(path=LEDGER):
    """The events of the ledger and the problems of the lines that could not be read.

    A file that is not there is a problem of its own: an empty ledger and a ledger that could not
    be opened are two different things, and a report that says the same about both hides one.
    """
    events, problems = [], []
    try:
        text = Path(path).read_text(encoding="utf-8")
    except OSError as problem:
        problems.append(f"the ledger file could not be read: {problem}")
        return events, problems
    for number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except ValueError:
            problems.append(f"line {number}: not valid JSON")
            continue
        if not isinstance(event, dict):
            problems.append(f"line {number}: not a JSON object")
            continue
        if event.get("first_attempt_correct") is not None and not isinstance(event.get("first_attempt_correct"), bool):
            problems.append(f"line {number}: first_attempt_correct is not true or false")
        event["_line"] = number
        events.append(event)
    events = sort_by_moment(events)
    return events, problems


def first_exposure(events):
    """The day each objective and each item was first seen.

    The objective day is the day the material of that objective was first seen, and it is what
    the retention and transfer horizons count from. The item day is the day one specific task
    was first seen. A task with no study event gets its first graded attempt as its day.
    """
    objectives, items, inferred = {}, {}, set()
    for event in events:
        when = parse_when(event.get("occurred_at"))
        if when is None:
            continue
        objective = event.get("objective_id")
        if objective is not None:
            if objective not in objectives or when < objectives[objective]:
                objectives[objective] = when
        key = (objective, event.get("item_id"))
        if event.get("mode") == "study":
            if key not in items or when < items[key]:
                items[key] = when
        elif key not in items:
            items[key] = when
            inferred.add(key)
    return objectives, items, inferred


def _rate(numerator, denominator):
    return round(numerator / denominator, 4) if denominator else None


def _brier(pairs):
    if not pairs:
        return None
    return round(sum((p - y) ** 2 for p, y in pairs) / len(pairs), 4)


def learned_objectives(events):
    """The objectives that meet the rule the vault already states: recalled twice on different
    days without notes, and used once in a task the learner had not seen.

    The rule lives in `90_System/Specs/Track_kinds.md`. Here it is computed from the ledger. Only
    an attempt the learner confirmed counts, the same as in the metrics: an attempt the agent
    graded is evidence about the agent, not about the learner.
    """
    by_objective = {}
    for event in events:
        by_objective.setdefault(event.get("objective_id"), []).append(event)
    learned = []
    for objective, items in sorted(by_objective.items(), key=lambda pair: str(pair[0])):
        recall_days, novel_use = set(), False
        seen_items = set()
        for event in sort_by_moment(items):
            item_id = event.get("item_id")
            correct = event.get("first_attempt_correct") is True
            helped = event.get("assistance") != "none"
            graded_by_agent = event.get("grading_method") != "learner_confirmed"
            if event.get("mode") in RETENTION_MODES and correct and not helped and not graded_by_agent:
                when = parse_when(event.get("occurred_at"))
                if when:
                    recall_days.add(when)
            if event.get("mode") in TRANSFER_MODES and correct and not helped and not graded_by_agent and item_id not in seen_items:
                novel_use = True
            seen_items.add(item_id)
        if len(recall_days) >= 2 and novel_use:
            learned.append(objective)
    return learned


def in_current_series(event, objectives):
    """True when the attempt belongs to the series of the rubric that grades the objective now.

    A new rubric version starts a new series and never mixes with the old one, so an attempt
    graded by an older rubric is not part of the rate of the current one. An objective that is
    not in the registry is not filtered: the registry is what says which rubric is current.
    """
    entry = objectives.get(str(event.get("objective_id")))
    if not entry:
        return True
    current = entry.get("rubric_version")
    if not current:
        return True
    return str(event.get("rubric_version")) == str(current)


def metrics(events, horizons=HORIZONS, objectives=None):
    """Retention, transfer, calibration and the learned rule, for every objective and overall.

    A retention attempt at horizon h is a recall or explain attempt, on the first try, with no
    help, graded by the learner, made h days or more after the objective was first seen. Transfer is
    the same, with an apply or discriminate task instead. An attempt with no verdict says nothing
    about what was remembered, so it is not eligible for any horizon. An attempt graded by an
    older rubric is not part of the current series of the objective, so it is not eligible either.
    """
    registry = load_objectives() if objectives is None else objectives
    exposure, item_days, inferred = first_exposure(events)
    shortest = min(horizons) if horizons else None
    graded = [event for event in events if event.get("mode") != "study"]
    objectives = sorted({str(event.get("objective_id")) for event in events})
    report = {
        "events": len(events),
        "attempts": len(graded),
        "items": len({event.get("item_id") for event in events}),
        "objectives": objectives,
        "retention": {},
        "transfer": {},
        "calibration": {},
        "learned": learned_objectives(events),
        "exposure": {str(name): day.isoformat() for name, day in exposure.items()},
        "excluded": {"help": 0, "agent_graded": 0, "too_recent": 0, "other_rubric": 0},
        "inferred_exposure": len(inferred),
    }
    for horizon in horizons:
        for label, modes in (("retention", RETENTION_MODES), ("transfer", TRANSFER_MODES)):
            correct = eligible = 0
            for event in graded:
                if event.get("mode") not in modes:
                    continue
                if event.get("assistance") != "none":
                    continue
                if event.get("grading_method") != "learner_confirmed":
                    continue
                verdict = verdict_of(event)
                if verdict is None:
                    # A graded attempt with no verdict says nothing about what was remembered.
                    # Counting it would print a rate that no event supports.
                    continue
                if not in_current_series(event, registry):
                    # An attempt graded by an older rubric is another series, and the series
                    # never mix.
                    continue
                key = event.get("objective_id")
                first = exposure.get(key)
                when = parse_when(event.get("occurred_at"))
                if first is None or when is None:
                    continue
                if (when - first).days < horizon:
                    continue
                eligible += 1
                correct += 1 if verdict else 0
            report[label][str(horizon)] = {"correct": correct, "eligible": eligible, "rate": _rate(correct, eligible)}
    for event in graded:
        if event.get("assistance") != "none":
            report["excluded"]["help"] += 1
        elif event.get("grading_method") != "learner_confirmed":
            report["excluded"]["agent_graded"] += 1
        elif not in_current_series(event, registry):
            report["excluded"]["other_rubric"] += 1
        else:
            first = exposure.get(event.get("objective_id"))
            when = parse_when(event.get("occurred_at"))
            if shortest is not None and first is not None and when is not None and (when - first).days < shortest:
                report["excluded"]["too_recent"] += 1
    explicit, ordinal = [], []
    for event in graded:
        outcome = verdict_of(event)
        if outcome is None:
            continue
        if event.get("assistance") != "none" or event.get("grading_method") != "learner_confirmed":
            continue
        probability = event.get("confidence_probability")
        confidence = event.get("confidence")
        # A boolean is not a number here: `true` is not a probability of 1 and not a confidence
        # of 1. The calibration module reads the same two fields the same way.
        if isinstance(probability, (int, float)) and not isinstance(probability, bool):
            explicit.append((float(probability), 1.0 if outcome else 0.0))
        elif isinstance(confidence, int) and not isinstance(confidence, bool) and 1 <= confidence <= 5:
            ordinal.append(((confidence - 1) / 4, 1.0 if outcome else 0.0))
    report["calibration"] = {
        "brier_explicit": _brier(explicit),
        "n_explicit": len(explicit),
        "brier_ordinal": _brier(ordinal),
        "n_ordinal": len(ordinal),
        "scale_ordinal": "(confidence - 1) / 4",
    }
    last = [parse_when(event.get("occurred_at")) for event in graded]
    last = [day for day in last if day]
    report["last_attempt"] = max(last).isoformat() if last else None
    return report


def by_objective(events, horizons=HORIZONS, objectives=None):
    """The same metrics, one entry per objective."""
    names = sorted({str(event.get("objective_id")) for event in events})
    registry = load_objectives() if objectives is None else objectives
    result = {}
    for objective in names:
        subset = [event for event in events if str(event.get("objective_id")) == objective]
        result[objective] = metrics(subset, horizons, registry)
    return result


def days_since(value, today=None):
    """The number of days between a date and today, or None when the date cannot be read."""
    when = parse_when(value)
    if when is None:
        return None
    return ((today or date.today()) - when).days


def append_event(event, path=LEDGER):
    """Add one event to the end of the ledger and return the path."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    line = {key: value for key, value in event.items() if not key.startswith("_")}
    with target.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(line, ensure_ascii=False, sort_keys=True) + "\n")
    return target


if __name__ == "__main__":
    print(__doc__)
    sys.exit(0)
