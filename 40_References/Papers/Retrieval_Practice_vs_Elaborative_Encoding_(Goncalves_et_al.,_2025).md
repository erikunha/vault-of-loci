---
type: reference
subtype: paper
year: 2025
authors: Goncalves, Muniz and Jaeger
venue: Educational Psychology Review, 37, article 100
doi: 10.1007/s10648-025-10076-6
link: https://link.springer.com/article/10.1007/s10648-025-10076-6
concepts: ["[[Retrieval_Practice|Retrieval practice]]"]
verified: true
checked: 2026-11-09
tags: [type/reference, flashcards]
---

# Retrieval practice vs elaborative encoding (Goncalves et al., 2025)

> [!tldr] In 3 lines
> Question: when retrieval practice and elaborative encoding are compared head to head, which one wins?
> Method: systematic review and meta-analysis of 44 empirical studies that directly compared the two, yielding 142 relevant comparisons.
> Result: retrieval practice wins by a small margin overall (g = 0.14), and the margin depends on corrective feedback (g = 0.50).

## Study explanation

Most advice for learning new material comes in two families. One family says make it meaningful: connect the new idea to what you already know, build a concept map, explain it out loud to someone. The other says pull it out of your head: close the book and answer a question. For decades each family had its own body of evidence, and both worked. A person who can code but met the topic last week faces a real problem here, because both methods look reasonable and the literature does not say which one to pick. Goncalves, Muniz and Jaeger (2025) resolved the problem by pooling only the studies where the two were compared directly.

The method is a systematic review and meta-analysis restricted to direct comparisons: 44 empirical studies that put retrieval practice against an elaborative condition, yielding 142 relevant comparisons. The restriction is the point of the paper. Separate meta-analyses of retrieval practice and of elaborative encoding both find positive effects, and that tells you nothing about the head to head case, because the two literatures were built on different materials, different learners and different tests.

The headline number is small. Retrieval practice had a small but statistically significant overall advantage over elaborative conditions, g = 0.14. Read that carefully: g = 0.14 means the retrieval group scored 0.14 standard deviations higher, on average, on the outcome the test used. It is a real edge and a narrow one. The moderators then do the interesting work. Free recall beat cued recall as the retrieval format, g = 0.23. And the advantage was conditional on the provision of corrective feedback, g = 0.50. When feedback was unavailable, elaborative encoding became more beneficial than retrieval.

A worked example. You are learning how HTTP caching works for the first time. Your plan is to build a concept map of cache headers, expiry rules, validators and CDN edges. That is elaborative encoding, and it is a good plan on its own terms. The retrieval plan is to close the tab and write down, from memory, how a max-age response header changes browser behavior and what a not-modified response means. According to this meta-analysis, the second plan wins only if you then check your answer and correct it. Without the correction step, the elaborative plan, the concept map, is at least as good. And the retrieval advantage concentrates in exactly the comparison that fits you: concept mapping and group discussions are the elaborative tasks where retrieval came out ahead, while against the remaining elaborative tasks the two were indistinguishable.

The most common mistake is to read g = 0.14 as "retrieval beats everything", or to read "retrieval beats elaborative encoding" with the condition dropped. The mistake happens because the headline sentence travels and the conditions do not. The authors' own conclusion runs in the opposite direction from the usual slogan: the positive effects of retrieval are significantly diminished relative to elaborative encoding tasks known for decades to benefit retention. In other words, retrieval is not a replacement for meaningful study. It is a replacement for passive rereading, and it works best as a partner for elaborative techniques when feedback is part of the loop.

Two connections. [[Retrieval_Practice|Retrieval practice]] in this vault is framed against rereading, and this paper says that framing is right: the real comparison is retrieval against passive study, not retrieval against good conceptual study. That is also why the exercise in the concept note ends with checking your gaps, because feedback is the condition that carries the advantage. [[Studying_with_AI|Studying with AI]] uses an AI assistant as a feedback machine: the assistant can correct a wrong answer immediately, which is the condition under which retrieval looks strongest here. That makes an assistant well suited to the retrieval loop, but it also means you must do the recall attempt first and take the correction second, otherwise the assistant did the elaborative part and you did no retrieval practice at all.

Keep the limits in mind. The evidence base is 44 studies and 142 comparisons, the overall effect is small, and the feedback finding is a moderator rather than a separate well powered analysis. The paper says the retrieval advantage is conditional, not universal.

## Key takeaways

- **Remember:** in direct comparisons retrieval practice beats elaborative conditions by a small margin, g = 0.14. The margin grows to g = 0.50 when corrective feedback is provided, and it disappears when feedback is missing.
- **Common confusion:** retrieval practice and elaborative encoding are treated as rivals, but the review finds they are close to interchangeable, with the edge depending on format and feedback rather than on which family the method belongs to.
- **Exercise:** write two short study plans for the same new topic, one retrieval based and one elaborative, and add the correction step to the retrieval one. Decide which you will use and where the feedback comes from.

## Results

| Comparison | Result |
|---|---|
| Retrieval practice vs elaborative conditions, overall | small but significant advantage, g = 0.14 |
| Free recall vs cued recall | advantage for free recall, g = 0.23 |
| When corrective feedback was provided | g = 0.50 |
| When feedback was unavailable | elaborative encoding became more beneficial than retrieval |
| Vs concept mapping and group discussions | retrieval practice benefited |
| Vs the remaining elaborative tasks | effects were indistinguishable |

| Coverage | Count |
|---|---|
| Empirical studies directly comparing the two | 44 |
| Relevant comparisons extracted | 142 |

## Limitations

- The overall advantage is small, and the authors conclude the positive effects of retrieval are significantly diminished relative to elaborative encoding tasks known for decades to benefit retention.
- The larger effect under corrective feedback is conditional, so it does not describe retrieval without feedback.
- The benefit was restricted to comparisons with concept mapping and group discussions, and was indistinguishable against the remaining elaborative tasks.
- The review contains 44 studies and 142 comparisons, so the moderator estimates rest on relatively few cases per cell.
- No claim here covers what happens with spaced sessions over long periods, since that was not part of the compared conditions.

## Related

- [[Retrieval_Practice|Retrieval practice]]
- [[Studying_with_AI|Studying with AI]]

## Flashcards

How many studies and comparisons did Goncalves et al. (2025) review?::44 empirical studies that directly compared retrieval practice with elaborative conditions, yielding 142 relevant comparisons.
What was the overall advantage of retrieval practice over elaborative encoding?::Small but statistically significant, g = 0.14.
Which retrieval format showed the larger advantage?::Free recall over cued recall, g = 0.23.
Which condition strengthened the retrieval advantage?::The provision of corrective feedback, g = 0.50.
Against which elaborative tasks did retrieval practice clearly win?::Concept mapping and group discussions.
What happened to elaborative encoding when feedback was unavailable?::Elaborative encoding became more beneficial than retrieval.
Retrieval practice beats elaborative encoding by a ==small margin==, and only when feedback is present.
