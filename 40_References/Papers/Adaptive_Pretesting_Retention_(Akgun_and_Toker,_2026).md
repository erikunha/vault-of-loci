---
type: reference
subtype: paper
year: 2026
authors: Akgun, Toker
venue: arXiv preprint 2606.22328
link: https://arxiv.org/abs/2606.22328
concepts: ["[[Retrieval_Practice|Retrieval practice]]"]
verified: true
checked: 2026-11-09
tags: [type/reference, flashcards]
---

# Do gains from generative AI-enabled adaptive pretesting persist? Evidence from a retention study (Akgun and Toker, 2026)

> [!tldr] In 3 lines
> Question: does the understanding you gain from an AI-assisted pretest survive when you are on your own for the rest of the course?
> Method: 89 undergraduates in one upper-division course, all given an adaptive AI-assisted pretest, then randomized for seven weeks to adaptive spaced retrieval, fixed spaced retrieval, or learner-directed AI-supported study.
> Result: an AI pretest raises understanding fast, but only structured retrieval keeps it seven weeks later, with posttest means of 78.19, 74.55 and 67.28.

## Study explanation

Pretesting is cheap and it feels good: you answer a few questions before the lesson, get a feeling for what you do not know, and the lesson lands better. The open question is what happens next. Akgun and Toker (2026) study a version of this that is now common: an AI-assisted adaptive pretest that finds the questions you are least prepared for and asks them. The paper is about persistence, and the answer is not the reassuring one. It is an arXiv preprint from June 2026 and has not been peer reviewed, so treat the result as an early signal rather than a settled finding.

The design has one common phase and then a fork. The sample is 89 undergraduates enrolled in a large upper-division course at a public research university. Every student completed an adaptive AI-assisted pretesting session, then received instruction, then took a baseline assessment. After that baseline, students were randomly assigned for seven weeks to one of three conditions: adaptive spaced retrieval practice, fixed spaced retrieval practice, or learner-directed AI-supported study. The first two are structured retrieval with different spacing schedules. The third is the free-form case, where the student decides what to study and uses AI as support.

A worked example with the reported numbers. Take the three posttest means. Adaptive spaced retrieval finished at 78.19 (SE 2.37), fixed spaced retrieval at 74.55 (SE 2.33), and learner-directed AI study at 67.28 (SE 2.12). Now compare the extremes. Adaptive spaced retrieval beat learner-directed AI-supported study with d = 0.92 and p = 0.003. In standard deviation terms, the adaptive group ended about 0.92 of a standard deviation above the free-form group, which is a large gap and the one clearly significant comparison in the study. But compare the two retrieval groups with each other: they did not differ significantly, p = 0.830. So the win in this trial is not a win for adaptive over fixed spacing. It is a win for structured retrieval over free-form AI study. And the middle comparison, fixed retrieval against learner-directed study, gave d = 0.57 with p = 0.071, short of the adjusted significance threshold the study used. One more detail cuts against the intuition that free-form AI study is efficient: observed practice effort was higher in the two retrieval conditions, so the students who did the better on the posttest also spent more time practicing.

The most common mistake is to read the title as "adaptive AI works". The adaptive scheduling did not separate the two retrieval groups. The second mistake is to read the adaptive pretest as the cause of the retention. Every student got the pretest, so it cannot explain the difference between the three conditions; what it does is raise initial understanding and hand the question over to the practice phase. The third mistake is to treat p = 0.071 as a null result for fixed retrieval against learner-directed study. It is a directionally clear difference that did not reach the adjusted threshold. The fourth is to assume the AI study group simply used the AI less or more; the note here reports effort, not use.

Two notes in this vault frame the result. [[Retrieval_Practice|Retrieval practice]] is the condition that held the gains: both retrieval groups practiced retrieval, and they finished ahead of the group that was free to choose its own study methods. [[Studying_with_AI|Studying with AI]] describes the protocol that matches the winning condition, where the AI asks, hints and corrects and you retrieve and explain, and it warns against the free-form use that corresponds to the learner-directed group here. The practical reading is narrow and useful: an AI pretest raises understanding fast, and what you do in the weeks after the pretest decides whether that understanding is still there seven weeks later.

## Key takeaways

- **Remember:** after a common AI-assisted adaptive pretest, students who did structured retrieval practice over seven weeks ended ahead of students who were free to direct their own AI-supported study, with posttest means of 78.19 (SE 2.37) for adaptive retrieval, 74.55 (SE 2.33) for fixed retrieval and 67.28 (SE 2.12) for learner-directed study, and d = 0.92 with p = 0.003 for the extreme comparison.
- **Common confusion:** people call this a win for adaptive AI, but adaptive and fixed spaced retrieval did not differ (p = 0.830). The tested difference is structured retrieval against free-form AI study.
- **Exercise:** design a one-week plan for a course you are taking, and mark every moment where you retrieve from memory rather than read the AI's answer.

## Results

| Condition | Posttest mean (SE) |
|---|---|
| Adaptive spaced retrieval | 78.19 (2.37) |
| Fixed spaced retrieval | 74.55 (2.33) |
| Learner-directed AI-supported study | 67.28 (2.12) |

| Comparison | Result |
|---|---|
| Adaptive spaced retrieval vs learner-directed AI study | d = 0.92, p = 0.003 |
| Adaptive spaced retrieval vs fixed spaced retrieval | not significant, p = 0.830 |
| Fixed spaced retrieval vs learner-directed AI study | d = 0.57, p = 0.071, short of the adjusted significance threshold |
| Observed practice effort | higher in the two retrieval conditions |

## Limitations

- arXiv preprint from June 2026, not peer reviewed.
- One course and one public research university, with 89 undergraduates.
- One course in one subject at one public research university, so the content is not general.
- Only three conditions, and no condition that separates the pretest effect from the practice effect on its own.
- The free-form AI condition was not monitored for how the AI was used, only for effort.
- Seven weeks is the only retention interval reported.
- Both retrieval conditions ended with higher means than the free-form group, but only the adaptive comparison reached significance, so the study does not isolate adaptive spacing as the active ingredient.

## Related

- [[Retrieval_Practice|Retrieval practice]]
- [[Studying_with_AI|Studying with AI]]

## Flashcards

How many students took part in Akgun and Toker (2026)?::89 undergraduates in a large upper-division course at a public research university.
What were the three seven-week conditions in Akgun and Toker (2026)?::Adaptive spaced retrieval, fixed spaced retrieval, and learner-directed AI-supported study.
What were the three posttest means in Akgun and Toker (2026)?::78.19 (SE 2.37) for adaptive spaced retrieval, 74.55 (SE 2.33) for fixed spaced retrieval, and 67.28 (SE 2.12) for learner-directed AI study.
How large was the gap between adaptive spaced retrieval and learner-directed AI study in Akgun and Toker (2026)?::d = 0.92 with p = 0.003.
Did adaptive and fixed spaced retrieval differ in Akgun and Toker (2026)?::No, the difference was not significant, with p = 0.830.
What did the study report about practice effort in Akgun and Toker (2026)?::Observed effort was higher in the two retrieval conditions than in learner-directed AI study.
In Akgun and Toker (2026), free-form AI study let the gains ==fade== over seven weeks, while structured retrieval held them.
What is the publication status of Akgun and Toker (2026)?::An arXiv preprint from June 2026 (arXiv:2606.22328), not peer reviewed.
