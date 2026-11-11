"""Measure how well the learner's confidence tracks the result.

The ledger is `50_Review/Attempts.jsonl`, written by `record_attempt.py`. This module holds the
calibration numbers, so `calibration_coach.py` only reads and prints them.

Calibration asks one question: when the learner said how sure they were, how close was that to
what happened. It measures the gap between the confidence and the result. It does not measure
what was learned. A small number of attempts says nothing, so every number here comes with its
count.

The attempts that count are the ones the other reports use: a first attempt, without help,
graded by the learner. An attempt with help, or graded by an agent, is recorded and left out.

Two numbers come out of it:

- the Brier score with an explicit probability, the mean of (probability minus what happened)
  squared. Lower is better.
- the Brier score with the 1 to 5 scale, where the scale is mapped to a probability by
  (confidence - 1) / 4. That mapping is an approximation of an ordinal scale, so the number is
  an approximation too.

An attempt that has both a probability and a confidence counts in the explicit group only, so the
two groups stay separate.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from learning_ledger import now_iso, verdict_of  # noqa: E402

POPULATION = "first attempt, no help, graded by the learner"
SCALE = "(confidence - 1) / 4"
CONFIDENT_AT = 0.8
UNSURE_AT = 0.4
DEFAULT_BINS = 5


def counting_attempts(events):
    """The attempts the calibration numbers use: a first attempt, without help, graded by the learner."""
    out = []
    for event in events:
        if event.get("mode") == "study":
            continue
        if not isinstance(event.get("first_attempt_correct"), bool):
            continue
        if event.get("assistance") != "none":
            continue
        if event.get("grading_method") != "learner_confirmed":
            continue
        out.append(event)
    return out


def explicit_probability(event):
    """The probability the learner gave, or None when there is none."""
    probability = event.get("confidence_probability")
    if isinstance(probability, (int, float)) and not isinstance(probability, bool):
        return float(probability)
    return None


def scale_probability(event):
    """The probability of the 1 to 5 scale, mapped by (confidence - 1) / 4, or None."""
    confidence = event.get("confidence")
    if isinstance(confidence, int) and not isinstance(confidence, bool) and 1 <= confidence <= 5:
        return (confidence - 1) / 4
    return None


def outcome(event):
    """What happened in one attempt: 1.0 when the answer was right, 0.0 when it was wrong."""
    return 1.0 if verdict_of(event) else 0.0


def brier(pairs):
    """The mean of (probability minus what happened) squared, or None when there is no pair."""
    if not pairs:
        return None
    return round(sum((p - y) ** 2 for p, y in pairs) / len(pairs), 4)


def bin_rows(predictions, bins):
    """The predictions split into bins, with the number of attempts and the share that were right."""
    rows = []
    for index in range(bins):
        low = index / bins
        high = (index + 1) / bins
        inside = [(p, y, source) for p, y, source in predictions
                  if low <= p < high or (index == bins - 1 and p >= high)]
        correct = sum(1 for _, y, _ in inside if y == 1.0)
        rows.append({
            "range": f"{low:.1f}-{high:.1f}",
            "low": round(low, 4),
            "high": round(high, 4),
            "attempts": len(inside),
            "correct": correct,
            "rate": round(correct / len(inside), 4) if inside else None,
            "from_scale": sum(1 for _, _, source in inside if source == "scale"),
        })
    return rows


def _case(event, probability, source):
    """One attempt as the coach shows it."""
    return {
        "event_id": event.get("event_id"),
        "objective_id": event.get("objective_id"),
        "item_id": event.get("item_id"),
        "occurred_at": event.get("occurred_at"),
        "probability": probability,
        "source": source,
        "confidence": event.get("confidence"),
        "correct": event.get("first_attempt_correct"),
    }


def calibration_of(events, bins=DEFAULT_BINS):
    """The calibration numbers of one group of attempts."""
    counted = counting_attempts(events)
    explicit, ordinal, predictions = [], [], []
    confident_and_wrong, unsure_and_right = [], []
    for event in counted:
        what_happened = outcome(event)
        given = explicit_probability(event)
        if given is not None:
            explicit.append((given, what_happened))
            predictions.append((given, what_happened, "explicit"))
            probability, source = given, "explicit"
        else:
            mapped = scale_probability(event)
            if mapped is None:
                continue
            ordinal.append((mapped, what_happened))
            predictions.append((mapped, what_happened, "scale"))
            probability, source = mapped, "scale"
        if probability >= CONFIDENT_AT and what_happened == 0.0:
            confident_and_wrong.append(_case(event, probability, source))
        if probability <= UNSURE_AT and what_happened == 1.0:
            unsure_and_right.append(_case(event, probability, source))
    return {
        "attempts": len(counted),
        "brier_explicit": brier(explicit),
        "n_explicit": len(explicit),
        "brier_ordinal": brier(ordinal),
        "n_ordinal": len(ordinal),
        "scale_ordinal": SCALE,
        "predictions_from_explicit": sum(1 for _, _, source in predictions if source == "explicit"),
        "predictions_from_scale": sum(1 for _, _, source in predictions if source == "scale"),
        "reliability": bin_rows(predictions, bins),
        "confident_and_wrong": confident_and_wrong,
        "unsure_and_right": unsure_and_right,
    }


def excluded_counts(events):
    """The attempts left out of the numbers, and why."""
    counts = {"help": 0, "agent_graded": 0, "not_graded": 0}
    for event in events:
        if event.get("mode") == "study" or not isinstance(event.get("first_attempt_correct"), bool):
            counts["not_graded"] += 1
        elif event.get("assistance") != "none":
            counts["help"] += 1
        elif event.get("grading_method") != "learner_confirmed":
            counts["agent_graded"] += 1
    return counts


def coach_report(events, bins=DEFAULT_BINS, objective=None, ledger=None):
    """The whole calibration report: the overall numbers and the numbers per objective."""
    counted = counting_attempts(events)
    objectives = sorted({str(event.get("objective_id")) for event in counted})
    report = {
        "generated": now_iso(),
        "bins": bins,
        "objective": objective,
        "ledger": str(ledger) if ledger else None,
        "population": POPULATION,
        "attempts": len(counted),
        "overall": calibration_of(counted, bins),
        "objectives": {},
        "excluded": excluded_counts(events),
    }
    for name in objectives:
        subset = [event for event in counted if str(event.get("objective_id")) == name]
        report["objectives"][name] = calibration_of(subset, bins)
    return report


if __name__ == "__main__":
    print(__doc__)
    sys.exit(0)
