---
type: spec
summary: One recipe per kind of learning project (course, book, certification, interview, language, research, skill) and the rituals every track shares.
tags: [type/spec]
---

# Spec: track kinds

A track is one learning project: something you set out to learn, on purpose, with a goal. The folder is `10_Tracks/<NN>_<Name>/` and the track note carries the properties below. The `new-track` skill asks for the kind and the horizon and builds the folder from the recipe of that kind.

## Properties of a track note

| Property | Values | Meaning |
|---|---|---|
| `kind` | `course`, `book`, `certification`, `interview`, `research`, `skill`, `language`, `other` | Picks the recipe |
| `horizon` | `finite`, `ongoing` | A finite track ends when `done_criterion` is met. An ongoing track has no end, so it needs a review cadence instead of a deadline |
| `goal` | one sentence | Specific and hard enough to need effort |
| `done_criterion` | a pass or fail check | "Done" must be something you can fail |
| `deadline` | date or empty | Empty for ongoing tracks |
| `if_then` | "If X, then I do Y" | One implementation intention: when and where you start |
| `status` | `active`, `paused`, `done` | |

Folder shape: `<Name>.md` (the track note), `sessions/` (one note per study session, from `90_System/Templates/Session.md`) and an optional `practice/` for what you do instead of reading or watching (project, lab, mock, exercises, logs). Notes in `practice/` use `type: practice`. Concepts and references stay in `20_Concepts/` and `40_References/`, shared by all tracks.

## Rituals for every track

- **Plan, act, reflect, every session.** The session note has a `Plan` (goal for this session), the work, and a `Reflection`. The cycle of forethought, performance and self-reflection is the core of self-regulated learning [Zimmerman 2002].
- **Goal and done criterion.** Specific, difficult goals lead to better performance than vague ones or "do your best" [Locke and Latham 2002]. Write the goal and a done criterion you can fail.
- **If-then plan.** A plan of the form "if situation X, then I do Y" helps people start and follow through [Gollwitzer 1999]. Put one in `if_then`, and one in each session's `Next step`.
- **Calibration.** Before a checkpoint, write the score you expect. After it, compare. The gap between prediction and result is what to study.
- **Explain without notes.** Each checkpoint includes one concept explained aloud or in writing with no notes and no AI. The `teach-the-agent` skill lists only the gaps afterwards.
- **Daily review cap.** Review 10 to 20 cards a day and add about 2 new cards a day. When the queue passes the cap, switch to "catch up backlog" mode: review the oldest and weakest first, stop at the cap, add no new cards until the queue is under it. The numbers are design defaults for this vault, not research results.
- **Forgiving streaks.** Missing a day carries no penalty and resets nothing. In a habit-formation study, missing a single opportunity did not materially affect how the habit formed [Lally 2009]. Count the days you studied, not a streak.
- **Shallow folders.** Folders stay two levels deep. Structure lives in links, properties, bases and the review loop, not in nested folders. Heavy filing did not pay off for retrieval in a study of email [Whittaker 2011].
- **No learning styles.** Do not sort yourself into visual, auditory or kinesthetic and study that way. A review of the evidence found no adequate support for matching instruction to a style [Pashler 2008]. Match the method to the material.
- **Tutor mode applies.** The learner attempts first, hints come in steps, and the agent never writes the learner's own notes or answers. Reference notes and guides may be written by an agent with verified sources.

## Recipes

Each recipe gives notes, practice, review cadence and checkpoint.

### course

- **Notes:** one session per lesson, in the lesson's order, with concepts linked.
- **Practice:** the course project in `practice/`. A question that comes up while building becomes a concept note.
- **Review:** flashcards daily within the cap, weekly review on a fixed day.
- **Checkpoint:** closed-book `no-ai-checkpoint` every two weeks on concepts older than 14 days.

### book

- **Notes:** one session per chapter. After the chapter, close the book and write what you remember. Then list the chapter's claims and ask "why is this true?" for each one, answering from a source.
- **Practice:** optional. Apply one idea to your own work and log it in `practice/`.
- **Review:** cards from the claims, reviewed daily within the cap.
- **Checkpoint:** after each part of the book, explain every main claim without the book.

### certification

- **Notes:** a blueprint map in `practice/`: one row per exam domain with its weight, your confidence (1 to 5) and your last practice score. Study the heavy, weak domains first. Mark every rule that is a practitioner convention and not in the official blueprint, so field habits and exam answers stay apart.
- **Practice:** timed practice exams under exam conditions. Keep an error log: question, why you missed it, the rule, the retry date.
- **Review:** error-log retries weekly, cards daily within the cap.
- **Checkpoint:** a full timed exam before the deadline, with your predicted score written first.

### interview

- **Notes:** a problem log in `practice/`: problem, pattern, result, time taken, retry date. A session per topic or pattern.
- **Practice:** 2 to 3 spoken mocks a week, with an observer when you can. Performance dropped by more than half when candidates were watched in a randomized trial of 48 students [Behroozi 2020], so practice being watched. Retry every failure after 7 days.
- **Review:** retries and cards weekly and daily within the cap.
- **Checkpoint:** an observed mock with a predicted score, then explain the solution aloud without notes.

### language

- **Notes:** an input log in `practice/` (what you read or heard, minutes). Mine sentences from that input and turn them into cards, so every card comes from something you met.
- **Practice:** speak or write every day, even briefly. Once a month, record an output sample (speech or text) and compare it with last month's.
- **Review:** capped daily cards; the cap holds even on a heavy day. Use "catch up backlog" mode after a break.
- **Checkpoint:** the monthly recorded output sample, with errors listed and the top three turned into cards.

### research

- **Notes:** one reference note per source (`40_References/`), with the study layer. Build a synthesis matrix in `practice/`: themes as rows, sources as columns, a cell for what each source says about each theme [Webster and Watson 2002].
- **Practice:** defend your synthesis to an AI critic. You write the synthesis and argue for it; the agent asks for evidence and names weak links but writes none of it.
- **Review:** update the matrix weekly. Cards only for facts you need to recall, each with its source.
- **Checkpoint:** explain the synthesis without notes, then check it against the matrix.

### skill

- **Notes:** an attempt log in `practice/`: what you tried, what was just past your current level, what failed, why. One session per practice block.
- **Practice:** work on tasks just past what you can do now. Redo every failure after a delay. Hours of deliberate practice explained only a modest share of performance differences, and the share varied by field [Macnamara 2014], so also seek feedback and vary the tasks.
- **Review:** failures redone after a delay, cards for rules you keep missing.
- **Checkpoint:** a fresh task of the same kind, done without help, with a predicted result.

### other

Pick the closest kind above, then write a `done_criterion` that you can fail and a review cadence for it.

## Evidence

- Tough, A. (1971). *The Adult's Learning Projects*. Ontario Institute for Studies in Education. The idea of a learning project.
- Zimmerman, B. J. (2002). Becoming a self-regulated learner: an overview. *Theory Into Practice*, 41(2). doi:10.1207/s15430421tip4102_2
- Locke, E. A., & Latham, G. P. (2002). Building a practically useful theory of goal setting and task motivation: a 35-year odyssey. *American Psychologist*, 57(9). doi:10.1037/0003-066X.57.9.705
- Gollwitzer, P. M. (1999). Implementation intentions: strong effects of simple plans. *American Psychologist*, 54(7). doi:10.1037/0003-066X.54.7.493
- Lally, P., van Jaarsveld, C. H. M., Potts, H. W. W., & Wardle, J. (2009). How are habits formed: modelling habit formation in the real world. *European Journal of Social Psychology*. doi:10.1002/ejsp.674
- Macnamara, B. N., Hambrick, D. Z., & Oswald, F. L. (2014). Deliberate practice and performance in music, games, sports, education, and professions: a meta-analysis. *Psychological Science*. doi:10.1177/0956797614535810
- Pashler, H., McDaniel, M., Rohrer, D., & Bjork, R. (2008). Learning styles: concepts and evidence. *Psychological Science in the Public Interest*. doi:10.1111/j.1539-6053.2009.01038.x
- Whittaker, S., Matthews, T., Cerruti, J., Badenes, H., & Tang, J. (2011). Am I wasting my time organizing email? *CHI '11*. doi:10.1145/1978942.1979457
- Webster, J., & Watson, R. T. (2002). Analyzing the past to prepare for the future: writing a literature review. *MIS Quarterly*, 26(2), xiii-xxiii.
- Behroozi, M., et al. (2020). Does stress impact technical interview performance? *ESEC/FSE '20*. doi:10.1145/3368089.3409712

## Not verified

- The DOIs were checked against Crossref (title, journal, year, first author). Only the abstract of Behroozi (2020) was read; the findings stated for the other papers come from their well-known conclusions and were not checked against the full texts.
- Tough (1971) and Webster and Watson (2002) have no DOI checked here.
- The review cap of 10 to 20 a day, the 2 new cards a day, the 7-day retry and the 2 to 3 mocks a week are design defaults for this vault, not measured optima.
