---
type: spec
tags: [type/spec]
---

# Spec: the learning interventions, what each one does and what it does not claim

## Why this spec exists

`90_System/Evals/Learning_outcomes.md` defines the record: the ledger, the objectives, the
metrics. This spec defines what the vault does with that record. Each intervention has a name, a
command, the evidence behind it, and a line saying what it does not prove.

The rule that holds for all of them: the vault measures the learner, not the agent. The tutor
eval in `90_System/Evals/Tutor_mode.md` tests the agent. These interventions test the person.

## The interventions

| Name | What it does | Evidence | What it does not claim |
|---|---|---|---|
| Adaptive review plan | Ranks what to review today from the attempts in the ledger | Spacing beats massing in classrooms, d = 0.54 ([[Distributed_Practice_in_Classrooms_(Mawson_and_Kang,_2025)\|Mawson and Kang 2025]]) | The ranking is a priority for the day, not a probability of remembering |
| Delayed retention assessment | Says which objectives passed 7, 30 or 90 days without an attempt without help, and asks for one | Retrieval practice helped retention in real classrooms, g = 0.37 ([[Retrieval_Spacing_and_Interleaving_in_Classrooms_(Ruitenburg_et_al.,_2026)\|Ruitenburg et al. 2026]]) | A delay that was never measured is unknown retention, not retention that failed |
| Recovery after inactivity | After 14 days away, runs a short diagnostic instead of the whole backlog | The effect of a strategy depends on the context and on how the practice was structured ([[Retrieval_Practice_vs_Elaborative_Encoding_(Goncalves_et_al.,_2025)\|Gonçalves et al. 2025]]) | A backlog is not a debt, and a cold start is not failure |

## Adaptive review plan

`schedule_review.py` reads the ledger and ranks the items worth another try.

- strength starts at 0.5, because nothing is known before the first attempt. A correct try adds
  40% of what is missing, a wrong one removes 40% of what is there.
- priority is (1 - strength) times (1 + days since the last attempt / 30). Weak and stale first.
- an item whose last attempt was wrong is doubled, because a mistake that was never recovered is
  the most useful thing to revisit.
- the day holds 15 reviews and about 2 new cards. When the queue is over the cap the oldest and
  weakest come first and no new cards are added until the queue is under it.

Decisions and alternatives:

| Decision | The alternative | Why this one |
|---|---|---|
| A transparent formula | FSRS, with stability and difficulty per item | FSRS predicts the next review for a card. The vault has objectives and tasks, not cards, and the plugin already runs FSRS for the flashcards. A second scheduler would predict twice |
| A priority, never a probability | A "chance of remembering" per item | The spec for the outcomes says a forecast is not a measurement. A number that looks like a probability would be read as one |
| The ledger, not the plugin schedule | Read the Spaced Repetition plugin data | The safety rules forbid every agent from reading plugin data files. The ledger is the vault's own record |
| Wrong last attempt doubled | Every item weighted the same | A mistake that was never recovered is the strongest signal that something is not learned yet |

## Delayed retention assessment

`retention_audit.py` reports the objectives that owe a delayed attempt. An objective is due when
a horizon passed with no attempt without help and graded by the learner.

The horizons are 7, 30 and 90 days, counted from the day the objective was first studied. These
are product decisions about when the learner wants the knowledge back, not a research result for
every material: the right interval depends on how long the knowledge has to last
([[Distributed_Practice_in_Classrooms_(Mawson_and_Kang,_2025)\|Mawson and Kang 2025]]).

A delayed attempt needs a task the learner has not seen. The agent writes it from the objective
note and its sources, and the item id carries the horizon, for example `o-one-d90`. The attempt
goes back into the ledger, and `retention_report.py` then has a measured number at that horizon.

Decisions and alternatives:

| Decision | The alternative | Why this one |
|---|---|---|
| A new task, not the same one | Repeat the studied item | The point is to measure the memory of the idea, not the memory of the wording |
| The delay is counted from the first study | Counted from the last attempt | Counting from the last attempt would make every horizon unreachable |
| An attempt with a hint stays out of the rate | Counted as a failure | An attempt with a hint measures the hint. The event is kept and the rate leaves it out |
| The horizon decides what is due, not a score | A low score makes an objective due | A low score says the learner missed it now. A horizon says the delay has arrived. They are different questions |

## Recovery after inactivity

After 14 days away, the vault runs a short diagnostic instead of the whole queue: the weakest
items, one explanation and one application, at most five. The learner then decides whether to
do the full plan for the next days.

The design follows the evidence that a free session with an assistant is not the same as a
structured one: in a seven-week study with the same model for everyone, the group whose practice
asked for real retrieval and refused easy answers kept more of the material than the group left
to direct its own study ([[Adaptive_Pretesting_Retention_(Akgun_and_Toker,_2026)\|Akgun and
Toker 2026]], a preprint, so early evidence). The lesson for the vault is the same one the tutor
mode already teaches: structure decides, not the presence of the AI.

Decisions and alternatives:

| Decision | The alternative | Why this one |
|---|---|---|
| A diagnostic of at most five items | The whole backlog | The queue after a break is long and the memory is cold. A long session is where people stop |
| The break is not a debt | A message about how much is waiting | The vault counts the days you studied, not a streak, and a backlog is work, not a debt |
| The learner decides the next days | The agent decides | The learner owns the routine. The agent lists and the learner chooses |

## What this phase does not do

- It does not schedule cards. The Spaced Repetition plugin already reviews the flashcards, and
  the vault only lists it as optional.
- It does not decide what the learner learned. It ranks and it asks. The verdict belongs to the
  learner.
- It does not compare the learner with a control group. One learner over months is exploratory
  evidence, and no number here supports a causal claim about the product.
