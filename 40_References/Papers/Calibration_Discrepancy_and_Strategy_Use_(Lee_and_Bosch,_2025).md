---
type: reference
subtype: paper
year: 2025
authors: HaeJin Lee, Nigel Bosch
venue: International Journal of Artificial Intelligence in Education, 35, 3746-3779
doi: 10.1007/s40593-025-00514-5
link: https://link.springer.com/article/10.1007/s40593-025-00514-5
concepts: ["[[Retrieval_Practice|Retrieval practice]]"]
verified: true
checked: 2026-11-09
tags: [type/reference, flashcards]
---

# Calibration discrepancy predicts students' subsequent metacognitive strategy use in computer-based learning environments (Lee and Bosch, 2025)

> [!tldr] In 3 lines
> Question: do students who overestimate how much they know engage less in learning strategies afterwards?
> Method: 210 college students worked in a computer-based learning environment, and their pretest judgment was compared with their pretest score, then both were used as predictors of how they behaved during the session.
> Result: overestimating students spent less time on preparatory actions before quizzes, with a coefficient of b = -9.100 (p < .001), and their own pretest judgment predicted that behaviour better than the score they actually earned.

## Study explanation

Knowing that you are wrong about your own learning is useful only if you can act on it. Lee and Bosch (2025) look at the moment where that should happen: after a pretest, when a student has both a score and a memory of how they answered, and before the learning session that follows. Their question is whether a student who overestimated their pretest performance changes behaviour in a way that costs them the session.

The study ran with 210 college students in a computer-based learning environment. Each student took a pretest and, alongside it, a retrospective judgment of their own performance. Calibration discrepancy is the difference between the two: a positive value means the student expected more than they got, which is overconfidence, and a negative value means they expected less, which is underconfidence. The researchers then used two linear regressions to ask whether that discrepancy predicted how much the student engaged in two kinds of activity during the session, coherent quiz activity and coherent reading.

A worked example with the reported numbers. Start with the descriptive picture: initial performance averaged 54.9 percent, the pretest retrospective judgment averaged 55.7 percent, and the calibration discrepancy averaged 0.796 percentage points with a standard deviation of 20.6, so the average student was slightly accurate and the group spread widely on both sides. Now take the first regression. The coefficient on the calibration discrepancy was b = -9.100 with beta = -0.283, p < .001 and a 95 percent confidence interval from -13.308 to -4.890. Read that carefully: the further above their score a student estimated, the less time that student spent preparing before a quiz. The effect is not negligible and not enormous: R squared was 0.080, adjusted R squared 0.076, and f squared 0.087, so calibration discrepancy accounted for about 8 percent of the variance in that engagement.

The result that should change a tool is the second one. The students' pretest retrospective judgment predicted their engagement in coherent quiz activity with b = -9.841, p < .001, a stronger negative predictor than the discrepancy itself, and it did so where the actual pretest score did not predict it at all. The judgment carried information the score did not. In the vault's terms, the prediction is a signal, and the score alone is not. One more result fits in the same frame: engaging in repeated quiz-taking was a significant negative predictor of changes in metacognitive judgment, with b = -1.792 and p = .036, so students who kept re-quizzing tended to adjust their judgments more conservatively.

The most common mistake is to read this as proof that fixing calibration improves learning. It does not show that. The outcome is behaviour during a session, not a learning gain, and the design is observational for the engagement part. What it shows is that overconfidence and the low strategic engagement that goes with it travel together, and that the learner's own prediction is the part that carries the information. The second mistake is to apply the coefficients to a single learner as if they were a target. A coefficient of -9.100 was estimated in a group of 210 students in one computer-based environment; for one person it is a reason to look at the gap, not a number to hit.

Two notes in this vault connect. [[Retrieval_Practice|Retrieval practice]] is where the score that anchors the judgment comes from, and this paper assumes that score exists and is trustworthy. [[Studying_with_AI|Studying with AI]] is where the practical consequence lands: an assistant that asks the learner to predict and then shows them the gap has a way to see overconfidence before it costs a session, which is exactly the signal this study says matters.

## Key takeaways

- **Remember:** in 210 college students, overestimating pretest performance predicted less time spent on preparatory actions before quizzes, b = -9.100 with p < .001, and the learner's own judgment predicted that engagement better than the score they earned.
- **Common confusion:** people treat this as evidence that correcting calibration improves learning. The outcome measured is engagement during a session, not a learning gain, and the coefficients are group averages.
- **Exercise:** explain in two sentences why the pretest judgment predicting engagement, while the score did not, matters for a tool that asks the learner to predict before they answer.

## Results

| Quantity | Value |
|---|---|
| Participants | 210 college students |
| Initial performance, mean and standard deviation | 54.9 percent, 19.0 |
| Pretest retrospective judgment, mean and standard deviation | 55.7 percent, 20.2 |
| Pretest calibration discrepancy, mean and standard deviation | 0.796 percentage points, 20.6 |
| Final performance, mean | 69.5 percent |
| Calibration discrepancy as predictor of coherent quiz engagement | b = -9.100, beta = -0.283, p < .001, 95% CI -13.308 to -4.890 |
| Variance explained by that predictor | R squared 0.080, adjusted R squared 0.076, f squared 0.087 |
| Pretest retrospective judgment as predictor | b = -9.841, p < .001, 95% CI -14.663 to -5.019 |
| Repeated quiz-taking as predictor of change in judgment | b = -1.792, p = .036 |

## Limitations

- The outcome is engagement in learning activities during one session, not a measured learning gain.
- College students in a single computer-based learning environment.
- Correlational relationships between the judgment and the later behaviour, with no intervention on the judgment.
- Group level coefficients, which do not transfer to a single learner as a target value.

## Related

- [[Retrieval_Practice|Retrieval practice]]
- [[Studying_with_AI|Studying with AI]]

## Flashcards

How many students took part in Lee and Bosch (2025)?::210 college students in a computer-based learning environment.
What does a positive calibration discrepancy mean in Lee and Bosch (2025)?::The student expected more than they actually scored, which is overconfidence.
What happened to preparatory actions before quizzes when a student overestimated?::They engaged less in them, with b = -9.100 and p < .001.
What did the pretest retrospective judgment predict in Lee and Bosch (2025)?::Engagement in coherent quiz activity, with b = -9.841 and p < .001.
Did the actual pretest score predict strategy engagement in Lee and Bosch (2025)?::No, the judgment predicted it where the score did not.
What is the outcome measured in Lee and Bosch (2025)?::Engagement in learning activities during the session, and not a learning gain.
