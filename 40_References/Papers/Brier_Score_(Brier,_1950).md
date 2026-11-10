---
type: reference
subtype: paper
year: 1950
authors: Glenn W. Brier
venue: Monthly Weather Review, 78(1), 1-3
doi: 10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2
link: https://doi.org/10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2
concepts: ["[[Retrieval_Practice|Retrieval practice]]"]
verified: false
checked: 2026-11-09
tags: [type/reference, flashcards]
---

# Verification of forecasts expressed in terms of probability (Brier, 1950)

> [!tldr] In 3 lines
> Question: how do you score a forecast that states a probability instead of a yes or no?
> Method: the paper proposes a single number for a set of probability forecasts, and separates the part that comes from how well the forecasts were calibrated from the part that comes from how uncertain the events were.
> Result: the score is the mean squared difference between the stated probability and what happened, so a confident and wrong forecast is punished more than an uncertain and wrong one.

## Study explanation

The vault reports a number called the Brier score whenever it compares what the learner said with
what happened. That name comes from this paper, which asks a practical question about weather
forecasting: a forecaster who says "70 percent" should be scored differently from one who says
"yes" or "no", and the score has to reward being right about how sure you were.

What I checked and what I did not. The metadata of the paper are verified: the Crossref record
and the Semantic Scholar record agree on the author, the title, the journal, the volume, the
issue, the pages, the year and the DOI, and the DOI resolves. I could not open the full text: the
publisher's page refused the request and the abstract is withheld at the publisher, so the
formula below is the definition this vault implements, and any claim about the paper's own
argument beyond that is marked as not verified.

The score the vault computes is the mean of the squared difference between the probability the
learner stated and the outcome, where the outcome is 1 when the attempt was right and 0 when it
was wrong. So a learner who says 0.9 and is right scores 0.01 on that attempt, and a learner who
says 0.9 and is wrong scores 0.81. That is the whole reason the number is useful here: a
confident mistake costs far more than an uncertain mistake, and the two cannot cancel each other
out the way they would in a plain count of right answers.

A worked example with numbers from this vault. Take two attempts. In the first, the learner says
0.8 and is right: the error is 0.2, squared to 0.04. In the second, the learner says 0.2 and is
right: the error is 0.8, squared to 0.64. The mean of the two squares is 0.34. A learner who was
right both times scores worse on this measure than one who was right once and unsure the other
time, and that is on purpose. The measure is about the confidence being honest, not about the
score being high.

The most common mistake is to read the Brier score as a measure of learning. It is not. It is a
measure of how close a stated probability was to the outcome, and a learner can be perfectly
calibrated and know nothing: say 0.0 and be wrong every time, and the score stays at zero. The
second mistake is to compare scores across different numbers of attempts. The mean is more stable
than a sum, but a score over three attempts and a score over three hundred are not the same
evidence, which is why the vault prints the count next to every number.

The paper's own framing is a forecast verification problem, and that is worth keeping in mind:
the score was built for weather forecasts, where the outcome is known after the fact. The vault
uses it for a learner's confidence before a reveal, where the outcome is also known after the
fact. What this vault does not claim is that the original decomposition of the score into
reliability and uncertainty carries over unchanged to a learner's confidence: that is not
verified here.

Two notes in this vault connect. [[Retrieval_Practice|Retrieval practice]] is the practice that
produces the outcomes the score is compared against. [[Studying_with_AI|Studying with AI]] is
where the learner-facing protocol lives, including the confidence question before the reveal that
gives the score something to measure.

## Key takeaways

- **Remember:** the Brier score is the mean squared difference between a stated probability and
  what happened, so a confident mistake costs more than an uncertain one.
- **Common confusion:** people read it as a measure of learning. It measures the honesty of the
  confidence, and a learner who is always unsure and always wrong can score perfectly.
- **Exercise:** compute the score for two attempts, one at probability 0.9 and right, one at
  probability 0.4 and right, and say which learner the measure prefers.

## Results

| Quantity | Value |
|---|---|
| Paper | Brier (1950), Monthly Weather Review, 78(1), 1-3 |
| Score in this vault | mean of (probability minus outcome) squared, outcome 1 or 0 |
| Best possible score | 0 |
| Metadata | verified through Crossref and Semantic Scholar |
| Full text | not opened, the publisher refused the request and the abstract is withheld |

## Limitations

- The full text was not opened, so what the paper argues beyond the definition above is not
  verified here.
- The paper scores weather forecasts. Applying the score to a learner's confidence is this
  vault's own use, and the paper does not study learners.
- The score says nothing about what was learned, only about how close the confidence was to the
  outcome.

## Related

- [[Retrieval_Practice|Retrieval practice]]
- [[Studying_with_AI|Studying with AI]]

## Flashcards

What does the Brier score compare?::The probability that was stated with what actually happened.
What happens to the score when a confident forecast is wrong?::It rises steeply, because the difference between the probability and the outcome is squared.
Is the Brier score a measure of learning?::No. It measures how close the stated confidence was to the outcome, and a learner who is always unsure and always wrong can score zero.
What does the Brier score measure in this vault?::The mean of the squared difference between the confidence the learner gave and whether the attempt was right.
