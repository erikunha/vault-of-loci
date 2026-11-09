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
| Transfer lab | Finds the objectives that were studied and never applied, and describes the task that is owed | Retrieval practice helped retention but not comprehension or transfer ([[Retrieval_Spacing_and_Interleaving_in_Classrooms_(Ruitenburg_et_al.,_2026)\|Ruitenburg et al. 2026]]) | A recall that sounds like an application is not a transfer |
| Misconception engine | Finds the objectives that were wrong more than once, and asks for two items that look alike | Interleaving helps, and its effect depends on the feedback ([[Retrieval_Spacing_and_Interleaving_in_Classrooms_(Ruitenburg_et_al.,_2026)\|Ruitenburg et al. 2026]]) | A report of a pattern is not a diagnosis of the reason |
| Adaptive scaffolding | Gives a worked example to a beginner and takes the steps away as the record rises | The vault's own tutor rule: teach a new learner, do not only test, and drop the steps as the score rises (`AGENTS.md`) | Scaffolding that stays when it is not needed can hurt someone who already knows the topic |
| Error recovery | Re-presents a mistake as a variation of the same task, until it comes back without help | The vault's own rule: close a mistake only after it comes back right, without help, from memory (`50_Review/Mistakes.md`) | A recovered mistake is one clean attempt, not a closed topic |
| Dependency check | Joins the prerequisite map of the tracks with the ledger and names the gaps | The vault's own rule: a concept map orders concepts by necessity, not by chapter (`10_Tracks/*/practice/Concept_Map.md`) | A gap in a prerequisite is an explanation, not a guarantee of the result |
| Learning eval | Runs the agent against scenarios where the record decides the right answer | The learner measured at 7, 30 and 90 days is the only way to know ([[Learning_evals\|Learning eval]]) | A model judge is not a person |

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

## Transfer lab

`transfer_lab.py` lists the objectives that were studied and never applied in a task, and hands
the agent what it needs to write one: the objective, the criterion that decides what counts, the
concept note it belongs to, and the item id the task must carry, for example
`retrieval-practice-apply-t1`.

A transfer task needs a case the learner has not seen. The task goes in the practice note of the
track, `practice/Transfer_Lab.md`, and the result goes back into the ledger with the mode
`apply`.

Why it matters: in authentic classrooms, retrieval practice helped retention but not
comprehension or transfer
([[Retrieval_Spacing_and_Interleaving_in_Classrooms_(Ruitenburg_et_al.,_2026)|Ruitenburg et al.
2026]]). A vault that only measures recall would score itself on the half the evidence supports.

Decisions and alternatives:

| Decision | The alternative | Why this one |
|---|---|---|
| Transfer is its own mode, separate from recall | Score an apply attempt as a recall | The two answer different questions, and the record has to keep them apart |
| The task needs a new case | The same question, asked again | A new case measures the idea. The same wording measures the memory of a sentence |
| The criterion comes from the objective registry | The agent invents the bar | A criterion another person could apply is what makes two attempts comparable |
| The rubric has three levels | Correct or wrong | "The right idea for the wrong reason" is a different gap from not knowing the idea |

## Misconception engine

`misconception_report.py` groups the wrong attempts by objective and lists the ones that were
wrong more than once, with the open mistakes from `50_Review/Mistakes.md` that name them.

A wrong answer once is noise. The same objective wrong again is a confusion, and repeating the
same card does not fix it: it needs two items that look alike, so the learner has to say which one
applies and why. That is what the drill in `50_Review/Misconceptions.md` is for.

Decisions and alternatives:

| Decision | The alternative | Why this one |
|---|---|---|
| A pattern of wrong answers, not a guess about the reason | The agent diagnoses the misconception | The ledger holds what was wrong, not why. The reason comes from the learner |
| Two items that look alike | The same card again | Discriminating is what separates two ideas that keep mixing |
| The report lists, the learner decides | The agent writes the confusion | The log is the learner's, like `50_Review/Mistakes.md` |
| Open mistakes from the log are shown next to the pattern | The report ignores them | The learner's own words about the mistake are better evidence than a counter |

## Adaptive scaffolding

The vault already says it in `AGENTS.md`: teach a new learner, do not only test. When the record
is empty or low, the agent follows the guess with a worked example from a source note, step by
step, then a similar problem for the learner. When the learner gets it right, the steps come off:
fewer steps, then no steps, then a new case.

The record decides when. The plan says how strong the record is, and the strengths come from the
attempts, so the scaffolding follows the evidence instead of the impression of the conversation.

Decisions and alternatives:

| Decision | The alternative | Why this one |
|---|---|---|
| The record decides the amount of help | The agent decides from the conversation | The conversation feels fluent even when nothing was learned |
| The steps come off as the record rises | The steps stay | What helps a beginner can hinder someone who already knows the topic, and the vault says so |
| A worked example comes from a source note | The agent explains from memory | The rule of the vault is that outside claims cite a note |

## Error recovery

`schedule_review.py --errors` lists the items whose last attempt was wrong, each with the id a
variation of the task must carry, for example `rp-r-01-v2`. The variation keeps the mechanism and
changes the surface, so the learner works with the idea and not with the memory of the sentence.

A mistake is closed only after it comes back right, without help, from memory. That is the rule
the vault already had in `50_Review/Mistakes.md`, and now the ledger can show it.

Decisions and alternatives:

| Decision | The alternative | Why this one |
|---|---|---|
| A variation of the same task | The same task again | The second try should test the idea, not the wording |
| The mistake stays open until a clean success | Close it after the correction is written | Writing the correction is not remembering it |
| The plan doubles the priority of a wrong last attempt | Weight every item the same | A mistake that was never recovered is the most useful thing to revisit |

## Dependency check

`dependency_check.py` reads what must be understood before what, from the concept map of each
track and from the edges of the canvases, and joins it with the ledger. A prerequisite is a gap
when it was never tested without help, when the last attempt was wrong, or when it has not been
tested for a while.

Decisions and alternatives:

| Decision | The alternative | Why this one |
|---|---|---|
| The map comes from the learner | The agent writes the map | The map is the learner's plan of what needs what, like the practice notes |
| The gap names the prerequisite | The agent says the concept is not ready | Naming the missing piece is what the learner can work on |
| Gaps come from the ledger | The agent guesses | A guess about what the learner does not know is exactly what this vault refuses to do |

## The learning eval

The tutor eval asks whether the agent behaves as a tutor. The learning eval asks whether the
agent uses the learner's own record: it reads the ledger, picks the objective that is really due,
writes a task the learner has not seen, and never states a measurement it did not make.

Its 10 scenarios live in `90_System/Evals/learning_scenarios.json`, the table people read is
`90_System/Evals/Learning_evals.md`, and the runner is the same one, with `--benchmark learning`.
Each scenario runs in a fresh copy of the vault with a ledger that already holds the learner's
history, so the agent has to read the record to answer. Four scenarios are critical: the wrong
objective, a task the learner had already seen, a recall dressed up as a transfer, or a retention
number that nobody measured.

What it does not claim: a model judge is not a person, and the scenarios test the agent, not the
learner. The learner's own retention is measured by the ledger, over real days.

## What these phases do not do

- It does not schedule cards. The Spaced Repetition plugin already reviews the flashcards, and
  the vault only lists it as optional.
- It does not decide what the learner learned. It ranks, it asks and it lists. The verdict belongs
  to the learner.
- It does not compare the learner with a control group. One learner over months is exploratory
  evidence, and no number here supports a causal claim about the product.
- It does not diagnose why an answer was wrong. The record holds what happened, not the reason.
- It does not promise that the interventions work. They are the ones the evidence points at,
  applied to one learner, with the limits written next to each one.
