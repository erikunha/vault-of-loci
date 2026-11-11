---
type: log
summary: Learning eval run transcript of minimax-learning on 2026-11-10.
tags: [type/log]
---

# Transcript: minimax-learning, 2026-11-10

Agent command: `90_System/Evals/runs/2026-11-09-minimax/mcode-tutor.sh`. Each message is in a code block, as the agent wrote it.

## Scenario 1

**learner**, turn 1

```text
Which of my topics is due for a delayed test?
```

**agent**, turn 2

```text
(no reply)
```

Error: timed out after 600 seconds

Files changed in the vault copy: `50_Review/Delayed_Tests_2026-11-10.md`, `90_System/Agent_Log/2026-11.md`, `90_System/Scripts/__pycache__/audit.cpython-315.pyc`, `90_System/Scripts/__pycache__/calibration.cpython-315.pyc`, `90_System/Scripts/__pycache__/dependencies.cpython-315.pyc`, `90_System/Scripts/__pycache__/format_notes.cpython-315.pyc`, `90_System/Scripts/__pycache__/learning_ledger.cpython-315.pyc`, `90_System/Scripts/__pycache__/misconceptions.cpython-315.pyc`, `90_System/Scripts/__pycache__/palace.cpython-315.pyc`, `90_System/Scripts/__pycache__/run_tutor_eval.cpython-315.pyc`, `90_System/Scripts/__pycache__/scheduler.cpython-315.pyc`, `90_System/Scripts/__pycache__/transcript_sections.cpython-315.pyc`, `90_System/Scripts/__pycache__/transfer.cpython-315.pyc`, `90_System/Scripts/__pycache__/vault_notes.cpython-315.pyc`, `90_System/index.json`, `INDEX.md`

## Scenario 2

**learner**, turn 1

```text
Give me a delayed test on retrieval practice.
```

**agent**, turn 2

```text
**What I read in your record:** `20_Concepts/Retrieval_Practice.md` has empty `score` and `last_tested`, `50_Review/Mistakes.md` has no entry for it, and the ledger has two clean attempts on item `rp-r-01`, the last on 2026-08-02. Correct me if that is wrong.

**Why this test now:** the audit says `retrieval-practice-recall` is due at the 30-day horizon (first seen 2026-07-13). The delay has arrived, but what you retained at 30 days is still unknown until you attempt it. An attempt that takes a hint stays out of the rate, so if you want it counted, answer closed book.

**Delayed test — item `retrieval-practice-recall-d30`, mode: recall**

Your study group has a midterm in a week. Two members have the same plan: reread the chapter three times before bed, because the pages feel familiar and the session feels productive. A third member closes the chapter, writes what they remember on a blank sheet, then checks the notes. You have to settle the argument with evidence, not vibes.

Write, from memory and with no note open: after one week, what did each group remember in the classic experiment on testing against rereading? Give both numbers and say which group came out ahead. Two or three sentences is enough. Then add one sentence on why the group's own feeling of "I know this" could not have told them who would win.

Two rules for the attempt: no note, no hint, no lookup before you answer. Take a hint only if you want one, and I will give it one step at a time, but the attempt then leaves the rate. When you have written it, tell me your confidence from 1 (guess) to 5 (certain) and I will reveal and grade against the source.
```

Files changed in the vault copy: `90_System/Scripts/__pycache__/audit.cpython-315.pyc`, `90_System/Scripts/__pycache__/learning_ledger.cpython-315.pyc`, `90_System/Scripts/__pycache__/scheduler.cpython-315.pyc`

## Scenario 3

**learner**, turn 1

```text
Quiz me on retrieval practice.
```

**agent**, turn 2

```text
Quiz written and checked. Here's what I read first, so you can correct me.

**Your record:** the ledger (`50_Review/Attempts.jsonl`) shows three correct recalls of retrieval practice at confidence 4, most recently 2026-10-31. The concept note has no `score` yet, `50_Review/Mistakes.md` is empty, and your session 01 pretest was wrong at confidence 4. Since the recall facts are solid and the explain/apply objectives in `90_System/Objectives.json` have never been tested, I pushed the difficulty up rather than repeating the numbers.

**Answer every question in your own words, then rate confidence 1 to 5 for each one.** Don't peek at the key. The full quiz with the key folded away lives in [Retrieval_practice_2026-11-10.md](/private/var/folders/qg/mdb1x_fn2gz_mczmdjm4bv8m0000gn/T/tutor-eval-qetvh1_l/vault/50_Review/Quizzes/Retrieval_practice_2026-11-10.md).

### Recall

1. *(Roediger and Karpicke, 2006)* State the one week retention result: what percentage did the group that tested itself recall, what percentage did the rereaders recall, and which method won?

2. *(Roediger and Karpicke, 2006)* State the 5 minute result with both numbers, and say what happened to the order of the two conditions by one week.

3. *(Roediger and Karpicke, 2006)* What did the researchers do about feedback after the memory tests, and what does that rule out as the source of the benefit?

4. *(Studying with AI)* Dunlosky and colleagues rated ten techniques students commonly use. Which two got the top utility rating, and which techniques got a low rating?

5. *(Retrieval practice)* What does rereading build, and what does retrieval build? Why does rereading feel good while you are doing it?

### Explain

6. *(Retrieval practice + Roediger and Karpicke, 2006)* Explain why the result can point one way after 5 minutes and the other way after one week. Say what the difference between the two readings is.

### Apply

7. *(Retrieval practice)* You have an exam tomorrow in a new subject and you feel ready after rereading. Describe step by step the plan you would follow instead, and say which part of the plan creates the learning.

8. *(Retrieval practice)* You did a recall attempt on a chapter and found three gaps, for example that you forgot that indexes slow down inserts. What do you do with each gap, and how does that connect to spacing?

### Multiple choice

9. *(Roediger and Karpicke, 2006)* What does the 2006 paper actually establish?
   - A. Rereading is useless, so you can skip the first read of a text.
   - B. Free recall tests produced more durable memory than repeated reading in that setting, and the effect appeared even though no feedback was given.
   - C. Testing helps only if you are told about your mistakes afterwards.
   - D. Rereading and testing end up with the same retention once you account for familiarity.

10. *(Studying with AI)* You did practice problems with an unrestricted chatbot and beat a classmate who did not use AI on practice. What does the evidence say to expect on the exam without AI, and what was different about the tutor version of the chatbot?
    - A. You learned more, so you should do fine without it.
    - B. Practice gains did not carry over: the unrestricted group scored 17% below the no AI group on the exam, while the hint based tutor version tied it.
    - C. It means you will do fine on the exam if you use the chatbot during it.
    - D. Nothing. Practice scores never predict exam scores.

Reply with your answers and a confidence rating per question (for example `1. 61% testing, 40% rereading, testing won. Confidence 4`). I'll grade against the source notes, not against how chatty this feels. For anything you miss I'll offer a mistake review, and I'll only write `score` and `last_tested` into the concept note if you say yes.
```

Files changed in the vault copy: `50_Review/Quizzes/Retrieval_practice_2026-11-10.md`, `90_System/Agent_Log/2026-11.md`, `90_System/Scripts/__pycache__/audit.cpython-315.pyc`, `90_System/Scripts/__pycache__/calibration.cpython-315.pyc`, `90_System/Scripts/__pycache__/dependencies.cpython-315.pyc`, `90_System/Scripts/__pycache__/format_notes.cpython-315.pyc`, `90_System/Scripts/__pycache__/learning_ledger.cpython-315.pyc`, `90_System/Scripts/__pycache__/misconceptions.cpython-315.pyc`, `90_System/Scripts/__pycache__/palace.cpython-315.pyc`, `90_System/Scripts/__pycache__/run_tutor_eval.cpython-315.pyc`, `90_System/Scripts/__pycache__/scheduler.cpython-315.pyc`, `90_System/Scripts/__pycache__/transcript_sections.cpython-315.pyc`, `90_System/Scripts/__pycache__/transfer.cpython-315.pyc`, `90_System/Scripts/__pycache__/vault_notes.cpython-315.pyc`, `90_System/index.json`, `INDEX.md`

## Scenario 10

**learner**, turn 1

```text
How much of this will I remember in a month?
```

**agent**, turn 2

````text
I read your record before answering: `50_Review/Attempts.jsonl` (3 events, all for `retrieval-practice-recall` / `rp-r-01`), your session note `session-01-how-memory-works.md`, and the `Retrieval_Practice` concept note. Correct me if I have that wrong.

## The honest answer: nobody can tell you yet, and that includes me

I will not give you a percentage, because the measurement that would produce one was never taken. Today is 2026-11-10. Your material was first seen 2026-09-11. The 30 day attempt became due on 2026-10-11 and has never happened.

What your record actually contains:

| Horizon | Measured result | Attempts |
|---|---|---|
| 7 days | 100% correct | 2 of 2, no hints, you graded them |
| 30 days | no eligible attempt | 0 |
| 90 days | no eligible attempt | 0 |

Days since your last attempt: 40. The scheduler puts the item at strength 0.82 and priority 0.42. Do not read that 0.42 as a probability of remembering. The script says so itself: the priority is a ranking for today, not a forecast.

Two caveats that make "2 of 2" softer than it sounds. Both attempts are `learner_confirmed`, you graded yourself, and your session note says your free recall from memory was missing the numbers from the experiment. The numbers are the entire criterion for this objective, so the 100% is generous. And your pretest guessed rereading with confidence 4, then was wrong.

## What the research in your vault puts a ceiling on

The direction is solid and consistent. Retrieval practice g = 0.37 across 120 effect sizes and 3,391 participants (Ruitenburg et al., 2026). Structured retrieval beat free-form AI study after seven weeks, 78.19 and 74.55 against 67.28 (Akgun and Toker, 2026). One week after testing, 61% against 40% for rereading (Roediger and Karpicke, 2006).

The number is not transportable to you. The distributed practice review is d = 0.54 with heterogeneity I² = 92%, so the studies in that pool disagree almost completely, and longer retention intervals went with *larger* effects. Same in Akgun and Toker: seven weeks is the only interval reported. Nothing in this vault measures 30 days for you specifically.

## Two things worth doing

Your question is a judgment of learning, and the way it gets useful is by committing to a number now and checking it later. So: **before we test, what percentage do you predict for the one week retention result with both numbers, 30 days from now?** Give me a percent, and a confidence from 1 to 5 on that percent being right.

Then we can settle it by measurement instead of prediction. Your 30 day attempt is due and missing. The audit has it queued:

```
objective: retrieval-practice-recall, due at 30 days
new item id: retrieval-practice-recall-d30
mode: recall
```

Say the word and I run the `retention-audit` skill: I write a closed book task you have not seen, built from the objective and its sources, you answer it without notes, rate confidence 1 to 5, and only then do I grade it against the source and record the attempt. That one attempt gives you the real number for the 30 day horizon, and the gap between your predicted percent and the result is the calibration signal that tells you whether to trust your own judgment next time.
````

Files changed in the vault copy: `90_System/Scripts/__pycache__/audit.cpython-315.pyc`, `90_System/Scripts/__pycache__/learning_ledger.cpython-315.pyc`, `90_System/Scripts/__pycache__/scheduler.cpython-315.pyc`

## Scenario 11

**learner**, turn 1

```text
Is my confidence telling me anything?
```

**agent**, turn 2

```text
I read the ledger, the concept note, and the mistakes log, then ran the vault's calibration coach. Here's what your confidence is doing.

## Short answer

For now, it's pointing the wrong way, but the sample is too small to call it a fact.

What I read: the concept note [[Retrieval_Practice|Retrieval practice]] has an empty `score` and `last_tested`, and `50_Review/Mistakes.md` has no entries, so the ledger `50_Review/Attempts.jsonl` is your only record. It holds 4 graded attempts, all on one objective, `retrieval-practice-recall`. Correct me if that misses something you remember.

## The numbers

| Date | Item | Probability | Result | Gap |
|---|---|---|---|---|
| 2026-10-21 | rp-r-01 | 0.90 | right | -0.10 |
| 2026-10-26 | rp-r-02 | 0.85 | wrong | +0.85 |
| 2026-10-31 | rp-r-03 | 0.90 | wrong | +0.90 |
| 2026-11-05 | rp-r-03 | 0.30 | right | -0.70 |

Brier score with an explicit probability: **0.5081** (n=4). The Brier score on the 1 to 5 scale alone has no attempts, because all four counted attempts also carried a percent, and the coach keeps the two groups separate. One earlier attempt from 2026-10-11 is a study event with no verdict, so it stays out.

Here is the shape worth noticing. In the 0.8 to 1.0 bin you were right once out of three, and both misses sat at 0.85 and 0.90. Your one attempt at 0.30 was right. Same item, rp-r-03: wrong at 0.90 on Oct 31, right at 0.30 on Nov 5. Across four attempts your confidence ran backwards from the result.

## What that means for what to study next

The coach's rule for sure and wrong is: the material is not where you think it is, so reread the concept note and test it again. That is exactly the failure your own concept note warns about. It says rereading "feels better in the moment, which is exactly why it fools you", and that familiarity feels like knowing but is not recall. Your pretest in [[session-01-how-memory-works|Session 01]] went the same way, confidence 4 and wrong.

The honest caveat: 4 attempts, one objective, one bin. That is a signal with a direction, not a verdict. It is enough to change how you answer the next question, not enough to say you are a chronic overconfident learner.

The 30-day delayed attempt also falls due today. The audit says first seen 2026-10-11, so 30 days lands on today, item id `retrieval-practice-recall-d30`. I did not write it to a file, since you asked a question rather than a task. Here it is, closed book.

## Next attempt, closed book

A friend says rereading a chapter the night before a test is the safest use of the time. Using the study in your notes, say what it predicts for the rereading group and for the group that tested itself at one week, with both numbers, and say which group came out ahead.

Before you answer, give me two numbers: your confidence from 1 (guess) to 5 (certain), and a percentage from 0 to 100. The percent is the one that makes the gap visible, and from here on I will ask for both. Then write your answer in your own words, and tell me how it went so I can record it in the ledger.
```

Files changed in the vault copy: `90_System/Scripts/__pycache__/audit.cpython-315.pyc`, `90_System/Scripts/__pycache__/calibration.cpython-315.pyc`, `90_System/Scripts/__pycache__/learning_ledger.cpython-315.pyc`, `90_System/Scripts/__pycache__/scheduler.cpython-315.pyc`
