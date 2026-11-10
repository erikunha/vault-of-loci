---
type: reference
subtype: paper
year: 2023
authors: Zheng, Chiang, Sheng, Zhuang, Wu, Zhuang, Lin, Li, Li, Xing, Zhang, Gonzalez and Stoica
venue: NeurIPS 2023 Datasets and Benchmarks Track, arXiv preprint 2306.05685
link: https://arxiv.org/abs/2306.05685
concepts: ["[[Retrieval_Practice|Retrieval practice]]"]
verified: true
checked: 2026-11-10
tags: [type/reference, flashcards]
---

# Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena (Zheng et al., 2023)

> [!tldr] In 3 lines
> Question: can a model judge the quality of another model's open-ended answer well enough to stand in for a human?
> Method: MT-bench, a multi-turn question set, and Chatbot Arena, where people compare two assistants blind, with 3 thousand expert votes and 30 thousand conversations with human preferences.
> Result: a strong judge agrees with human preferences more than 80 percent of the time, the same level of agreement humans reach with each other, but only when its known biases are controlled.

## Study explanation

This is the paper that made the LLM judge a normal tool instead of a hack, and the vault uses the same idea: an eval run scores transcripts with a model from another family and records who judged what. The paper does two things. It builds MT-bench, a multi-turn question set, and it uses Chatbot Arena, where people compare two assistants blind. The judges read an open-ended answer and give a score, and the paper measures how close that score lands to what humans think.

The part that matters most for a study vault is the list of ways a judge goes wrong. There are three named biases. Position bias is the judge preferring whichever answer it saw first. Verbosity bias is the judge preferring the longer answer, even when the shorter one is the correct one. Self-enhancement bias is the model favouring its own style. The paper also names limited reasoning ability, which is not a bias but a ceiling. Each of these has a practical consequence for a rubric. If the rubric does not say that length is not quality, a judge will reward length. If the rubric asks for something the model cannot check, the judge will invent a reason to score it. And a judge that shares a family with the agent it scores will lean toward its own style, which is why this vault refuses a judge from the agent's own family.

The result that justifies the practice is the agreement number. A strong judge reaches over 80 percent agreement with human preferences, and the paper reports that this is the same level of agreement that humans reach with each other. That is a calibration point: the judge is not a person, but at the level of agreement it is a competent second reader, not a source of truth.

## Key takeaways

- **Remember:** a strong LLM judge agrees with human preferences more than 80 percent of the time, which is the same level of agreement humans have with each other.
- **Common confusion:** a judge is not automatically fair. It has position bias, verbosity bias and self-enhancement bias, and a rubric that does not control for them will drift.
- **Exercise:** take the rubric of one eval scenario and add one line about length not being quality. That single line removes the most common source of a wrong score.

## Results

| Quantity | Value |
|---|---|
| MT-bench | 80 two-turn open-ended questions for multi-turn conversation and instruction following |
| Chatbot Arena | blind human preference comparison |
| Public data | the MT-bench questions, 3 thousand expert votes and 30 thousand conversations with human preferences |
| Judge | GPT-4, with position swaps to control the order of the answers |
| Judge agreement with human preferences | over 80 percent |
| Human agreement with each other | the same level |
| Named biases | position, verbosity, self-enhancement |
| Named ceiling | limited reasoning ability of the judge |

## Limitations

- The paper is from 2023 and the judges it used are older than the ones available now, so the agreement numbers are a floor, not a current measurement.
- Agreement with human preference is not agreement with pedagogical quality. A judge can prefer a well-written answer that teaches nothing.
- The mitigations are described in general terms, and this vault only applies the ones that fit a local, file-based eval: a judge from another model family, an explicit rubric, and the reason next to every score.
- The paper does not give a threshold for when a judge is good enough to gate a release. That threshold is a decision a team has to make and defend.

## Related

- [[Retrieval_Practice|Retrieval practice]]
- [[Studying_with_AI|Studying with AI]]

## Flashcards

What are the three biases named in Zheng et al. (2023)?::Position bias, verbosity bias and self-enhancement bias.
How well does a strong LLM judge agree with human preferences in that paper?::More than 80 percent, the same level of agreement humans reach with each other.
What does the verbosity bias do to a judge?::Makes it prefer the longer answer even when the shorter one is the correct one.
Why does this vault refuse a judge from the agent's own family?::Self-enhancement bias: the judge leans toward answers that look like its own style.
