---
type: reference
subtype: paper
year: 2025
authors: Srinivasa, Che, Zhang, Mares, Hernandez, Park, Lee, Mangialardi, Ng, Cardona, Gunjal, He, Liu and Xing
venue: arXiv preprint 2510.02663
link: https://arxiv.org/abs/2510.02663
concepts: ["[[Retrieval_Practice|Retrieval practice]]"]
verified: true
checked: 2026-11-10
tags: [type/reference, flashcards]
---

# TutorBench: a benchmark to assess tutoring capabilities of large language models (Srinivasa et al., 2025)

> [!tldr] In 3 lines
> Question: how well do frontier models actually tutor, judged on what a tutor is supposed to do?
> Method: 1,490 conversations written by human experts, each with its own rubric, graded by an LLM judge with those rubrics.
> Result: no frontier model scores above 56 percent, and every one of them passes fewer than 60 percent of the criteria about guiding, diagnosing and supporting a student.

## Study explanation

Most evaluations of a study assistant ask whether the model can answer. TutorBench asks a harder question: can it tutor. The benchmark treats tutoring as three concrete jobs. The first is adaptive explanation, where the model has to notice what the student does not understand from the way the student phrases the follow-up, and explain the missing piece rather than the whole topic again. The second is feedback on the student's own work, which means reading a solution, finding the error and saying what to do next. The third is active learning support, which is the one that matters most for this vault: the student has a partially correct answer and the model has to give a hint that moves them one step without giving the answer away.

The design decision that matters for how this vault's own benchmark is built is the rubric. Every sample carries a rubric written by a human expert, and the rubric for one sample is self-contained, mutually exclusive and verifiable. Self-contained means the judge can decide from the rubric alone, without knowing the rest of the dataset. Mutually exclusive means one reply cannot satisfy two criteria at once, so the judge is not scoring the same behaviour twice. Verifiable means a person reading the transcript could reach the same verdict, which is the difference between a measurement and an impression.

The results are the reason to read the paper. Sixteen frontier models were evaluated and none reached 56 percent. Every model passed less than 60 percent of the rubric criteria that describe the core tutoring skills: guiding the student, diagnosing the error and supporting the next step. The families differ from each other in a useful way, since the Claude models were the strongest at active learning support and the weakest at the other two tasks. That is a warning for a vault like this one: passing the tutor-mode rules is not the same as being good at tutoring, and the two have to be measured separately.

## Key takeaways

- **Remember:** the best frontier model scored 55.65 percent on TutorBench, and every model passed fewer than 60 percent of the criteria about guiding, diagnosing and supporting a student.
- **Common confusion:** a model can follow tutor rules and still be a weak tutor. Rules adherence and pedagogical quality are different measurements.
- **Exercise:** take one reply from this vault's tutor eval and check it against three criteria from TutorBench: does it name the student's misconception, does it give one step forward, does it avoid giving the answer.

## Results

| Quantity | Value |
|---|---|
| Samples, written by human experts | 1,490 |
| Curriculum | high school and AP level |
| Tutoring tasks | adaptive explanation, feedback assessment, active learning support |
| Rubrics | sample-specific, self-contained, mutually exclusive, verifiable |
| Models evaluated | 16 frontier LLMs |
| Best overall score | 55.65 percent (Claude Opus 4.1 Thinking), with 55.33 percent for the second |
| Pass rate on the core tutoring criteria | below 60 percent for every model |
| Judge | Claude Sonnet 4, applied to the sample rubric |
| Agreement of the judge with human ratings | 0.78, against 0.75 between the human experts themselves |
| Family difference | Claude models strongest on active learning, weakest on the other two |

## Limitations

- The subject matter is school and AP mathematics, not software engineering or any other professional domain.
- The judge is a model, not a person, so the paper's rubric verdicts carry the same kind of limitation this vault records for its own judge. The judge is Claude Sonnet 4, and the Claude models are among the ones being scored.
- The judge's agreement with human ratings is 0.78, and the agreement between the 69 human experts with each other is 0.75, measured on 250 samples. The judge is close to the human level, but it is still a model reading a rubric.
- The benchmark says nothing about whether a learner retained anything. It measures the assistant's behaviour, not the learner's outcome.

## Related

- [[Retrieval_Practice|Retrieval practice]]
- [[Studying_with_AI|Studying with AI]]

## Flashcards

What are the three tutoring tasks in TutorBench?::Adaptive explanation, feedback on the student's own work, and active learning support through hints.
How many samples does TutorBench have, and who wrote them?::1,490, written by human experts.
What was the best score any frontier model got on TutorBench?::55.65 percent, and no model passed 60 percent of the core tutoring criteria.
What does the rubric of a sample in TutorBench have to satisfy?::It has to be self-contained, mutually exclusive and verifiable.
What does TutorBench not measure?::Whether the learner retained anything. It measures the assistant's behaviour.
