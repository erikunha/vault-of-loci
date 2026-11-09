"""Find the objectives that owe a transfer task, and describe what the task must ask.

A recall says the learner can reproduce an idea. A transfer says the learner can use it in a
case they have not seen. The two are measured apart, because the evidence says the first does
not bring the second: in authentic classrooms, retrieval practice helped retention but not
comprehension or transfer.

So this module looks for objectives the learner has studied and never applied, and hands the
agent what it needs to write the task: the objective, its criterion, the note it belongs to,
and an item id that carries the number of tasks already written for it.

Standard library only.
"""
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from learning_ledger import TRANSFER_MODES, load_objectives, parse_when  # noqa: E402
from scheduler import clean_attempts  # noqa: E402


def transfer_attempts(events, objective):
    """The clean attempts of one objective that applied the idea in a task."""
    return [event for event in clean_attempts(events)
            if event.get("objective_id") == objective
            and event.get("mode") in TRANSFER_MODES]


def tasks_written(events, objective):
    """The transfer tasks of one objective, including the ones that needed help.

    A task that was attempted with help was still seen, so the next task gets the next number.
    """
    return [event for event in events
            if event.get("objective_id") == objective
            and event.get("mode") in TRANSFER_MODES
            and event.get("grading_method") == "learner_confirmed"]


def studied_objectives(events):
    """The objectives the learner has already seen, with the day it happened."""
    seen = {}
    for event in events:
        objective = event.get("objective_id")
        when = parse_when(event.get("occurred_at"))
        if objective is None or when is None:
            continue
        if objective not in seen or when < seen[objective]:
            seen[objective] = when
    return seen


def transfer_status(events, objectives=None, today=None):
    """For every objective, what was applied and what was not."""
    today = today or date.today()
    objectives = objectives or {}
    seen = studied_objectives(events)
    rows = []
    for objective in sorted(seen):
        applied = transfer_attempts(events, objective)
        written = tasks_written(events, objective)
        registry = objectives.get(objective, {})
        last = applied[-1]["occurred_at"] if applied else None
        rows.append({
            "objective_id": objective,
            "concept": registry.get("concept"),
            "criterion": registry.get("criterion"),
            "first_seen": seen[objective].isoformat(),
            "transfer_attempts": len(applied),
            "tasks_written": len(written),
            "last_transfer": last,
            "days_since_transfer": (today - parse_when(last)).days if parse_when(last) else None,
            "needs_transfer": not applied,
        })
    return rows


def transfer_plan(events, objectives=None, today=None, limit=None):
    """The objectives that owe a transfer task, with the id the new task must carry."""
    rows = transfer_status(events, objectives, today)
    plan = []
    for row in rows:
        if not row["needs_transfer"]:
            continue
        number = row["tasks_written"] + 1
        plan.append({
            "objective_id": row["objective_id"],
            "concept": row["concept"],
            "criterion": row["criterion"],
            "first_seen": row["first_seen"],
            "item_id": f"{row['objective_id']}-t{number}",
            "mode": "apply",
            "rubric": {
                "2": "the learner applies the idea to the new case and says why it applies",
                "1": "the right idea for the wrong reason, or the right reason without the application",
                "0": "the definition repeated, or an answer that does not use the idea",
            },
            "why": "the idea was studied and never applied in a task the learner had not seen",
        })
    if limit:
        plan = plan[:limit]
    return plan


if __name__ == "__main__":
    print(__doc__)
    sys.exit(0)
