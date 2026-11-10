---
type: reference
subtype: paper
year: 2026
authors: Mussabayev, Zavertyaev, Parpulov and Savchenko
venue: arXiv preprint 2610.23612
link: https://arxiv.org/abs/2610.23612
concepts: ["[[Retrieval_Practice|Retrieval practice]]"]
verified: true
checked: 2026-11-10
tags: [type/reference, flashcards]
---

# SIT-Eval: situation-based interactive turn-by-turn evaluation of conversational agents (Mussabayev et al., 2026)

> [!tldr] In 3 lines
> Question: does a single aggregate score hide how an agent behaves in the rare situations that actually break it?
> Method: desired behaviour written as situational rules, an interlocutor that samples a situation per turn, and a judge that scores the reply against every rule that applies to that situation.
> Result: models with almost the same overall score differ wildly rule by rule, and clarifying ambiguity is the weakest rule for essentially every model (2 to 47%, average 11%).

## Study explanation

The problem this paper names is one this vault ran into for real. A run gives one number, and the number hides which behaviour failed. An agent can look acceptable overall while failing in the one situation that matters, and the aggregate will not show it. The fix the paper proposes is to stop scoring the agent in general and start scoring it in situations.

The formalisation is simple enough to reuse. Desired behaviour becomes a set of rules of the form "if the situation is P, follow rules Q". At every turn, an interlocutor draws a situation uniformly and plays it. The judge then applies every rule that is relevant to the situation the agent actually faced, which means a rule does not count against an agent that was never in the situation it governs. The judge is validated against human-checked golden dialogues, which is the step that separates this from a plausible-sounding setup.

Two results matter for a study vault. The first is that aggregate scores hide things: eight models over 1,292 turns showed large differences in per-rule adherence among models that scored almost the same overall. The second is that clarifying ambiguity is where nearly all of them fail. The paper reports low adherence to rule 4 across the board, from 2 to 47% and 11% on average, and rule-level tables show some models are weakest on a different rule altogether. Socratic questioning is named in the paper's abstract as a shared weak point, but the paper's own tables rank it third-lowest of seven categories on average, with problem conclusion often lower. For this vault, the ambiguity result lands right on the tutor mode, which asks for a guess before any hint and asks why once after a correct answer. Those are exactly the behaviours that a rule-following agent has the easiest time pretending to do and the hardest time doing well.

There is one framing idea in the paper worth keeping even for a single learner. Rare situations are a safety gap, because an event that is unlikely in a demo becomes a frequent failure at production scale. A vault used daily for months will eventually hit the odd case, and the eval has to cover it.

## Key takeaways

- **Remember:** models with nearly identical overall scores can differ widely rule by rule, so a single aggregate hides the failure modes.
- **Common confusion:** that an agent which satisfies the rules most of the time is reliable. The rare situation is where it breaks.
- **Exercise:** write one rule for this vault in the form "if the learner asks for the answer, then ask for a guess first", and check which of the eval scenarios put the agent in that situation.

## Results

| Quantity | Value |
|---|---|
| Behaviour model | situational rules: if situation is P, follow rules Q |
| Interlocutor | samples a situation uniformly and plays it at every turn |
| Judge | context-aware, applies every rule valid for that situation |
| Judge validation | 500 golden dialogues from Claude Sonnet 4.5, 100 sampled, 3 human experts, 1,292 turn-level items, 0.85% judged noisy |
| Judge accuracy | 84.4% (2,655 of 3,145), 34.4 points above chance, Cohen's h = 0.76 |
| Models evaluated | 8 |
| Turns evaluated | 1,292 |
| Weakest rule for nearly every model | ambiguity clarification (rule 4), 2 to 47%, average 11% |
| Weakest category on average | problem conclusion 0.49, then distraction 0.56, then Socratic questioning 0.68 |

## Limitations

- The agents evaluated are chat models in a scripted setup, not coding agents inside a file-based vault, so the failure modes may not transfer one to one.
- The paper's own limitations: sampling one situation per turn fragments the dialogue, and ecological validity was not validated; the 12 rules are Western-Socratic in origin; some situation-rule pairs have only 50 examples; it measures adherence, not learning gains.
- The situations are sampled uniformly by a model, so an unmodelled situation is simply not tested.
- The paper is internally inconsistent on benchmark size, citing 170 problems in one place and 100 in another, and gives the 1,292 turn count only in the abstract and introduction.
- Nothing in it measures a learner. It measures the agent.

## Related

- [[Retrieval_Practice|Retrieval practice]]
- [[Studying_with_AI|Studying with AI]]

## Flashcards

How does SIT-Eval write down the behaviour it wants?::As situational rules: if the situation is P, follow rules Q.
What did SIT-Eval find about aggregate scores?::Models with almost the same overall score vary a lot rule by rule, so the aggregate hides the failure modes.
What is the behaviour nearly every model in SIT-Eval was worst at?::Clarifying ambiguity, rule 4, with adherence between 2 and 47% and 11% on average.
How is the SIT-Eval judge validated?::Against golden dialogues generated with Claude Sonnet 4.5, with a 100-dialogue sample annotated by 3 human experts over 1,292 turn-level items, 0.85% noisy, giving the judge 84.4% accuracy.
