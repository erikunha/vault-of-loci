---
type: spec
tags: [type/spec]
---

# Spec: learning outcomes, the attempt ledger and what the vault must prove

## Why this spec exists

The vault has one evaluation: `90_System/Evals/Tutor_mode.md`. It asks whether an agent follows
the tutor rules: attempt first, hint ladder, confidence before the reveal, no answer without a
try. The 17 scenarios and the runs in `90_System/Evals/runs/` measure the behavior of the agent
and the behavior of the judge. They say nothing about the learner.

That gap is the main one in the product. A tutor can obey every rule and the learner can still
forget the material a month later. The rules are the product. The retention is the outcome.

So the vault needs a second kind of evidence: a record of what the learner actually did, over
time, without notes, and a way to measure it. This spec defines that record, the metrics and
the limits.

## What the tutor eval measures, and what it does not

| The tutor eval measures | The tutor eval does not measure |
|---|---|
| Whether the agent asked before answering | Whether the learner kept the knowledge |
| Whether the hint ladder was respected | Whether the learner understood the mechanism |
| Whether confidence was asked before the reveal | Whether the learner can apply the idea elsewhere |
| Whether the agent wrote in the learner's notes | Whether the learner's recall improved |

Both matter and they are not the same measurement. A change to the rules changes the left
column. A change to the study flow changes the right column. They need separate instruments.

## Three outcomes, with working definitions

- **Retention**: the learner recovers the content later, without notes, on the first try.
  Measured as R7, R30 and R90.
- **Comprehension**: the learner explains the mechanism, the relations and the causes, and not
  only the definition. Measured by the rubric of the explain mode.
- **Transfer**: the learner applies the idea in a task that was not seen before, in a context
  that was not told in advance. Measured as T30 and T90.

Retention is the requirement. Comprehension and transfer are the harder part, and the evidence
is thinner: a classroom meta-analysis of 53 studies found that retrieval practice helped
retention but not comprehension or transfer
([[Retrieval_Spacing_and_Interleaving_in_Classrooms_(Ruitenburg_et_al.,_2026)|Ruitenburg et al. 2026]]).
A vault that only measures retention would repeat the mistake the research warns about.

## Learning objectives

An objective is one thing the learner should be able to do, with the criterion that says done.
Objectives live in `90_System/Objectives.json`, one registry for the whole vault:

```json
{
  "id": "retrieval-practice-recall",
  "concept": "Retrieval_Practice",
  "mode": "recall",
  "criterion": "State the one week retention result of testing against rereading, with both numbers, without looking.",
  "rubric_version": "v1"
}
```

- `id`: stable. It never changes, so the history of an objective stays comparable over time.
- `concept`: the note the objective belongs to.
- `mode`: recall, explain, apply or discriminate. It is the default mode for the attempts.
- `criterion`: what "done" means, in one sentence, written so a second person could grade it.
- `rubric_version`: which rubric graded the attempts. A new rubric version starts a new series
  and never mixes with the old one.

## The ledger

The ledger is `50_Review/Attempts.jsonl`: one JSON object per line, one line per graded
attempt, appended and never edited. `record_attempt.py` writes it, `retention_report.py` reads
it, and the schema lives in `90_System/Scripts/learning_ledger.py`.

| Field | Meaning |
|---|---|
| `event_id` | unique id of the line |
| `objective_id` | the objective the attempt belongs to |
| `item_id` | the question or task. The same id means the same task every time |
| `occurred_at` | ISO 8601 with an offset, for example 2026-11-09T18:00:00-03:00 |
| `mode` | study, recall, explain, apply or discriminate |
| `first_attempt_correct` | true, false, or null for a study event that was not graded |
| `confidence` | 1 to 5, the scale the tutor asks for, or null |
| `confidence_probability` | 0 to 1, when the learner gave a chance, or null |
| `hints_used` | how many hints the learner took |
| `assistance` | none, hint, strong_hint, partial_example or answer |
| `rubric_version` | which rubric graded the attempt |
| `grading_method` | learner_confirmed or agent_graded |
| `source_revision` | which version of the material was tested |
| `duration_minutes` | minutes spent, or null |

`mode: study` records that the material was seen, without grading it. It sets the day the
objective was first studied, which is where the horizons count from.

The ledger is in the repository on purpose. The metrics are only auditable when the events that
produced them travel with the code that reads them. The vault has one learner, so the events
are study data and not personal data about other people.

## The metrics

Every metric below describes the same population: a first attempt, without help, graded by the
learner. Anything else is recorded, counted and named in the report as excluded, with the
reason.

- **R(h)**, retention at horizon h, with h in 7, 30 and 90 days: the share of eligible attempts
  that were right on the first try, where an eligible attempt happened h days or more after the
  objective was first studied. The report always shows the numerator and the denominator.
- **T(h)**, transfer at horizon h: the same, with apply or discriminate attempts instead of
  recall and explain.
- **Calibration**: the Brier score, the mean of (probability of being right minus what happened)
  squared ([[Brier_Score_(Brier,_1950)\|Brier 1950]]). Lower is better. Two numbers are shown: one when the learner gave a probability, and
  one when the learner only gave the 1 to 5 scale, which is mapped to a probability by
  (confidence - 1) / 4. The second is an approximation and says so.
- **Learned**: the rule the vault already states in `90_System/Specs/Track_kinds.md`, now
  computed from the ledger. Recalled twice on different days without notes, and used once in a
  task the learner had not seen.

Nothing here is a forecast. A scheduler may predict that a card will be forgotten tomorrow. A
prediction is not a measurement, and the report never shows one as retention.

## Decisions, and what was chosen instead

| Decision | The alternative | Why this one |
|---|---|---|
| One JSONL file, appended | One note per attempt | A note per attempt is readable but heavy to diff and hard to aggregate. The ledger is read by a script, not by eye |
| Exposure counted per objective | Exposure counted per item | A transfer task is new by definition, so per item exposure would put every transfer attempt on day zero and no transfer would ever count |
| One confidence scale, 1 to 5 | Only a probability from 0 to 1 | The tutor already asks for 1 to 5 and the learner answers in that scale. Both are stored: the scale always, the probability when the learner gives one |
| Attempts with help are excluded | Count them as failures | An attempt with a hint measures the hint, not the memory. They are recorded and counted, never folded into the rate |
| Agent graded attempts are excluded | Count them as the learner confirmed | The tutor rules forbid the agent from setting a score the learner did not report. The ledger keeps that rule in the numbers |
| Retention, transfer and calibration over the same population | Each metric over its own population | One population makes the numbers comparable and stops the report from mixing easier tasks with harder ones |
| Horizons of 7, 30 and 90 days | The interval that a scheduler would choose | A horizon is a product decision about when the learner wants the knowledge back, not a research result for every material |
| The ledger lives in the repository | The ledger ignored by Git | The metrics are auditable only when the events travel with the code. The vault has one learner |

## What this phase does not do

- It does not schedule reviews. The scheduler is a later phase, and the vault already documents
  FSRS in [[Studying_with_AI|Studying with AI]], including the warning that a better forecast is
  not proof of more learning.
- It does not grade for the learner. The agent can propose a verdict, but the event says
  `learner_confirmed` only when the learner confirmed it.
- It does not judge the content of a card. `check_cards.py` checks that a card has a source and
  is not repeated. Whether the answer is factually right is still a human call.
- It does not measure a single learner against a control group. One learner over months is
  exploratory evidence. It cannot support a causal claim about the product.
- It does not build a dashboard, a database or a service. The repo stays local files, Python and
  Obsidian.

## The evidence behind the choices

- Retrieval practice, spaced practice and interleaving work in real classrooms, with smaller and
  more conditional effects than in the lab: g = 0.37 for retrieval, g = 0.20 for spacing and
  g = 0.40 for interleaving, over 53 studies and 7,303 students
  ([[Retrieval_Spacing_and_Interleaving_in_Classrooms_(Ruitenburg_et_al.,_2026)|Ruitenburg et al. 2026]]).
- Retrieval only beats elaborate study by a small margin, g = 0.14, and the margin depends on
  feedback: with feedback g = 0.50, without it the elaborate study wins
  ([[Retrieval_Practice_vs_Elaborative_Encoding_(Goncalves_et_al.,_2025)|Gonçalves et al. 2025]]).
- Spacing beats massing in classrooms, d = 0.54, with heterogeneity of 92 percent
  ([[Distributed_Practice_in_Classrooms_(Mawson_and_Kang,_2025)|Mawson and Kang 2025]]).
- AI used to explain and to search raised the test score by 0.27 standard deviations
  ([[Learning_Impact_of_Generative_AI_(Contractor_and_Reyes,_2026)|Contractor and Reyes 2026]]),
  while a course-integrated AI tutor lowered final grades by 0.37 standard deviations and
  classroom participation by 0.90
  ([[Course_Integrated_AI_Tutoring_(Liu_et_al.,_2026)|Liu et al. 2026]]). The structure of the
  tutor decides, not the presence of the AI.
- The method of loci shows d = 0.88 for immediate serial recall, with the certainty of the
  evidence rated low
  ([[Method_of_Loci_Meta_Analysis_(Ondrej,_2025)|Ondřej 2025]]). The vault is named after it and
  has no workflow for it yet.

## How to use it

```bash
# after a graded attempt
python3 -I 90_System/Scripts/record_attempt.py --objective retrieval-practice-recall \
  --item retrieval-practice-recall-01 --mode recall --correct --confidence 4

# what the ledger shows
python3 -I 90_System/Scripts/retention_report.py
python3 -I 90_System/Scripts/retention_report.py --objective retrieval-practice-recall --json
```

The `record-attempt` skill does the same thing from a tutoring session.
