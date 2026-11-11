"""Audit the learning ledger: what was measured, what is due, and what was never tested.

The ledger is the record of what the learner did. This module asks two questions of it: which
objectives still have a horizon waiting for them, and which ones have never been tested at all.
The horizons are 7, 30 and 90 days by default, and they count from the day the objective was
first studied.

The audit never invents an assessment. It says which objectives need a delayed attempt, so the
learner and the agent can make one, and the result goes back into the ledger.

Standard library only.
"""
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from learning_ledger import HORIZONS, metrics, parse_when  # noqa: E402
from scheduler import clean_attempts, days_since_last, objectives_seen  # noqa: E402


def audit(events, horizons=HORIZONS, today=None, objectives=None):
    """The state of every objective the ledger knows about."""
    today = today or date.today()
    seen = objectives_seen(events)
    report = {"objectives": [], "horizons": list(horizons)}
    for objective in sorted(seen):
        subset = [event for event in events if event.get("objective_id") == objective]
        clean = clean_attempts(subset)
        graded = [event for event in subset if event.get("mode") != "study"]
        helped = [event for event in graded if event.get("assistance") != "none"]
        measured = metrics(subset, horizons, objectives)
        days = days_since_last(subset, today)
        exposed = (today - seen[objective]).days
        if not graded:
            status = "never tested"
        elif not clean:
            # Two different reasons why nothing counts, and they lead to different next steps.
            status = "only tested with help" if helped else "only graded by the agent"
        else:
            status = "measured"
            for horizon in horizons:
                # An attempt at a horizon counts whether it was a recall, an explain, an apply or a
                # discriminate. Reading only the retention column left an objective measured by
                # transfer alone permanently "due at 7 days", because it has no recall rows.
                retention = measured["retention"].get(str(horizon), {})
                transfer = measured["transfer"].get(str(horizon), {})
                if retention.get("eligible", 0) == 0 and transfer.get("eligible", 0) == 0:
                    # A horizon that has not arrived yet is not owed. The delay is still to come.
                    if exposed >= horizon:
                        status = f"due at {horizon} days"
                    else:
                        status = (f"not due yet: the {horizon} day horizon arrives "
                                  f"in {horizon - exposed} days")
                    break
        report["objectives"].append({
            "objective_id": objective,
            "first_seen": seen[objective].isoformat(),
            "attempts": len(graded),
            "clean_attempts": len(clean),
            "days_since": days,
            "days_since_exposure": exposed,
            "status": status,
            "retention": measured["retention"],
            "transfer": measured["transfer"],
            "last_attempt": measured["last_attempt"],
        })
    report["due"] = [row for row in report["objectives"] if row["status"].startswith("due")]
    report["untested"] = [row for row in report["objectives"]
                          if row["status"] in ("never tested", "only tested with help",
                                                "only graded by the agent")]
    return report


def equivalent_item(item_id, horizon):
    """The id of the new task for a delayed attempt.

    A delayed attempt needs a task the learner has not seen, so the id carries the objective
    and the horizon, for example `o-one-d90`. The agent writes the task from the objective and
    the ledger keeps the id, so the same task is never written twice.
    """
    return f"{item_id}-d{horizon}"


def delayed_plan(events, horizons=HORIZONS, today=None, objectives=None):
    """The objectives that owe a delayed attempt, with the horizon each one owes."""
    report = audit(events, horizons, today, objectives)
    plan = []
    for row in report["due"]:
        horizon = int(row["status"].split()[2])
        plan.append({
            "objective_id": row["objective_id"],
            "horizon": horizon,
            "first_seen": row["first_seen"],
            "days_since": row["days_since"],
            "example_item": equivalent_item(row["objective_id"], horizon),
            "why": f"no attempt without help {horizon} days after the material was first seen",
        })
    return plan


if __name__ == "__main__":
    print(__doc__)
    sys.exit(0)
