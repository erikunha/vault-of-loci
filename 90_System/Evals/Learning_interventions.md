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
| Calibration coach | Reads the ledger and shows how well the learner's confidence tracks the result, then asks for a probability before the next reveal | Metacognitive questioning improved performance and calibration over six sessions ([[Metacognitive_Questions_and_Judgment_of_Learning_(Michalsky_and_Bakrish,_2024)\|Michalsky and Bakrish 2024]]), and overestimating students engaged less in metacognitive strategies ([[Calibration_Discrepancy_and_Strategy_Use_(Lee_and_Bosch,_2025)\|Lee and Bosch 2025]]) | A Brier score measures the gap between confidence and outcome, not what was learned |
| Memory palace | Turns ordered material into a route of places the learner picks, then walks the route and records each place on its own | The method of loci beat rehearsal for serial recall with d = 0.88, with the evidence rated low to very low ([[Method_of_Loci_Meta_Analysis_(Ondrej,_2025)\|Ondrej 2025]]) | A palace is an encoding for ordered material, and its evidence is weaker than the evidence for retrieval practice |
| Visual reconstruction | Compares the diagram the learner drew with the source and names only the relations that are missing | Drawing support helped only when it facilitated integration, g = 0.35 against g = -0.15 ([[Drawing_to_Learn_Meta_Analysis_(Leutner_and_Biele,_2025)\|Leutner and Biele 2025]]) | The integration step is where the effect sits, and g = 0.35 is a small to moderate advantage |
| Counterfactual | Changes one premise of a concept and asks what changes, so the answer is about the mechanism | The vault's own rule: after a correct answer, ask once why it is true, the mechanism, principle or evidence behind it (`AGENTS.md`) | A mechanism the learner cannot name has not been shown |
| Compression challenge | Asks for the concept three times, in full, as an analogy and as the shortest version that holds, then lists the relations that survived and the ones that did not | Retrieval practice helped retention, g = 0.37, but not comprehension or transfer, g = 0.20 and 0.40 ([[Retrieval_Spacing_and_Interleaving_in_Classrooms_(Ruitenburg_et_al.,_2026)\|Ruitenburg et al. 2026]]) | A short version that drops a relation is a different claim, not a summary |

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

Its 15 scenarios live in `90_System/Evals/learning_scenarios.json`, the table people read is
`90_System/Evals/Learning_evals.md`, and the runner is the same one, with `--benchmark learning`.
Each scenario runs in a fresh copy of the vault with a ledger that already holds the learner's
history, so the agent has to read the record to answer. Five scenarios are critical: the wrong
objective, a task the learner had already seen, a recall dressed up as a transfer, a retention
number that nobody measured, or a calibration verdict that nobody computed.

What it does not claim: a model judge is not a person, and the scenarios test the agent, not the
learner. The learner's own retention is measured by the ledger, over real days.

## Calibration coach

`calibration_coach.py` reads the ledger and reports how well the learner's confidence tracks the
result. The numbers are the Brier score with an explicit probability, the Brier score with the 1 to
5 scale mapped to a probability, a reliability table with the attempts and the share that were
right, and the sharpest cases: the attempts where the learner was sure and wrong, and the attempts
where the learner was unsure and right.

The population is the one population of the vault: a first attempt, without help, graded by the
learner. Attempts with help, attempts graded by an agent and attempts that were never graded are
counted apart and left out of the numbers, and the report says how many.

The skill then asks for a probability from 0 to 100 before the next reveal, and records it with
`--probability`. The reason is in the record: the learner's own judgment predicted later strategy
use where the actual score did not ([[Calibration_Discrepancy_and_Strategy_Use_(Lee_and_Bosch,_2025)\|Lee and Bosch 2025]]),
and asking a question inside the material improved calibration over six sessions
([[Metacognitive_Questions_and_Judgment_of_Learning_(Michalsky_and_Bakrish,_2024)\|Michalsky and Bakrish 2024]]).

Two reports exist and they are not the same report. `calibration_report.py` reads the frontmatter
of the concept notes, which the checkpoint skill fills in, and answers what the learner wrote down
about a concept. `calibration_coach.py` reads every graded attempt in the ledger and answers how
the confidence behaved. The ledger is the record the metrics use.

Decisions and alternatives:

| Decision | The alternative | Why this one |
|---|---|---|
| The gap between confidence and outcome | The calibration discrepancy of a predicted score against the score earned | The ledger already holds the confidence of each attempt and whether it was right. A predicted score is another field for the learner to fill in, and a badly filled field is a number nobody can trust |
| Every number printed with its count | One score for the whole record | A Brier score over three attempts says nothing, so the report prints the count next to the number and says that a bin with a few attempts means nothing |
| The 1 to 5 scale mapped to a probability, and named as an approximation | Treat the scale as a probability | The scale is ordinal. The mapping is an approximation, and the report says so on the line under the number |
| The coach asks for a probability, it never gives one | The agent tells the learner how calibrated they are | The learner sees the gap between their own two numbers. The agent does not produce the judgment |
| The prediction decides what is asked next, never what is claimed | Use the prediction to rank what to study | A number that predicts is not a number that measured, and the retention report keeps the two apart |

## Memory palace

`palace.py` reads a palace note and `palace_test.py` walks it. The palace note lives in
`50_Review/Palaces/<Name>.md` and holds one table with the columns Place, Item and Source. The
rows of the table are the route, in walking order.

The ids come from the name of the note: the objective is `palace-<name>` and a place is the item
`palace-<name>-<place number>`. Each place is recorded on its own, so a route of twelve places
gives twelve data points and the learner can see which place broke.

The script prints the places with the item blank, because the item is what the learner has to
recall. The `--with-items` flag shows the item, and it is used after the learner has answered, to
check the answer against the note.

The evidence is the weakest of the interventions here. The method of loci beat rehearsal for
ordered serial recall with a pooled d of 0.88, but the same review rated the certainty of the
evidence low to very low, with 89.2 percent of the experiments at high risk of bias and two
corrections that disagree with each other
([[Method_of_Loci_Meta_Analysis_(Ondrej,_2025)\|Ondrej 2025]]). The outcome is ordered recall, not
understanding, and the review contains nothing about an AI assistant in the loop.

Decisions and alternatives:

| Decision | The alternative | Why this one |
|---|---|---|
| The learner picks the places | The agent builds the palace | Only the learner knows which route is vivid. A palace of places the agent chose is a list of images, not a route |
| One attempt per place | One attempt for the whole route | A route of twelve places gives one number and hides which place broke |
| The item is blank in the output | The script prints the whole table | Printing the table turns the walk into a reading task |
| The palace is an optional encoding for ordered material | The palace as the way to study everything | The evidence is about ordered serial recall, with low certainty, and the outcome is not understanding |
| One thing per place | A sentence per place | One item per place is what the place can hold as a picture |

## Visual reconstruction

The learner rebuilds a diagram, a map or a flow from memory. The agent compares it with the
source and names only the relations that the source has and the drawing does not, one line for
each, and asks a question about each one. The agent never redraws the diagram and never adds the
relation itself.

This is the shape the drawing evidence supports. In the meta-analysis of drawing to learn, drawing
support in general did not change learning outcomes. What did work was support that helped the
student integrate the picture with the words, with g = 0.35 for comprehension against g = -0.15 and
not significant for the support without integration
([[Drawing_to_Learn_Meta_Analysis_(Leutner_and_Biele,_2025)\|Leutner and Biele 2025]]). The
comparison between two representations is the step that does the work, so the step is the one the
learner takes.

The missing relations are what the next attempt is built from, and the practice note keeps the
drawing, the relations that survived and the relations that did not.

Decisions and alternatives:

| Decision | The alternative | Why this one |
|---|---|---|
| The drawing is from memory, with the source out of sight | Redraw with the source next to it | There is nothing to reconstruct when the answer is on the page |
| The learner compares, or the agent compares and asks | The agent grades the drawing | The comparison is where the effect is. An agent that grades the drawing removes the step that does the work |
| Only what is missing is named | A full correction of the drawing | A drawing that keeps the nodes and loses an arrow has not kept the idea, and that is the only thing the agent has to say |
| The missing relations become questions | The agent adds the relation | A question the learner answers is an attempt. A relation the agent adds is a note the learner does not own |

## Counterfactual

The agent picks one premise from the concept note, a precondition, a limit or an assumption, and
states the counterfactual in one line: if this premise were not true, what would change? The
learner answers first, without notes. An answer that only repeats the recommendation does not
count, and the agent asks for the mechanism instead: which step breaks, and what follows from
that.

The mode is apply, and the answer is graded against the source and the rubric, not against how the
conversation went. The rule it follows is the vault's own: after a correct answer, ask once why it
is true, the mechanism, the principle or the evidence behind it, and a right answer with a wrong
or missing reason gets partial credit (`AGENTS.md`).

Decisions and alternatives:

| Decision | The alternative | Why this one |
|---|---|---|
| One premise, changed | Ask what the concept means | Changing a premise exposes the mechanism. Asking for the definition again tests the wording |
| The answer has to name the mechanism | Accept a fluent answer | A fluent answer that never names the mechanism gets no credit, and the vault grades the words against the source |
| The agent asks and waits | The agent answers with the counterfactual | The learner attempts first, so the counterfactual has to be the learner's own |
| The premise comes from the concept note | The agent invents a premise | The premise has to be one the idea really rests on, and the note is where the learner wrote it down |

## Compression challenge

The learner says the same idea three times: in full, as an analogy, and as the shortest version
that still holds. Then the agent lists the relations that survived and the ones that did not, and
the learner puts the missing relation back in their own words.

The rule is that a short version that keeps the causal relations and drops the examples is a good
compression, and a short version that drops a relation is not a summary but a different claim.

The evidence is a gap in the evidence for retrieval practice. Retrieval practice helped retention
in real classrooms, g = 0.37, but the same review found it did not help comprehension or
transfer, g = 0.20 and 0.40
([[Retrieval_Spacing_and_Interleaving_in_Classrooms_(Ruitenburg_et_al.,_2026)\|Ruitenburg et al. 2026]]).
Compression is the part that tests the relations, so it is the part that recall alone does not do.

Decisions and alternatives:

| Decision | The alternative | Why this one |
|---|---|---|
| Three versions, in this order | One short version | The full version and the analogy show which relations were there to lose |
| The agent lists what is missing and the learner puts it back | The agent writes the shortest correct version | A version the learner wrote is an attempt, and a version the agent wrote is a note |
| A lost relation goes to the mistakes log | It becomes a card about the definition | A card about the definition trains the wording. The relation is what was lost |
| The mode is explain | The mode is recall | The exercise asks for the mechanism and not only the definition |

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
- It does not correct the learner's calibration. The coach shows the gap between what the learner
  said and what happened, and it asks for a probability.
- It does not build a palace for material that is not ordered, and it does not claim that a palace
  teaches anything.
- It does not draw. The visual reconstruction names the relations that are missing and asks a
  question about each one.
