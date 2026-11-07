---
type: review
tags: [type/review, flashcards]
---

# Mistakes

> [!tldr] Errors worth keeping
> Log each wrong answer with the concept it belongs to. Correct it yourself first, then turn it into a card with a source.

## How to use

1. Log a mistake: date, concept link, what you answered, what was right, why you went wrong, and the kind of error (`knowledge`: you did not know it; `reasoning`: you knew the facts but drew the wrong conclusion; `execution`: right plan, wrong steps; `careless`: you knew it and slipped), and how AI was involved: `scaffold` (you tried and the agent gave a hint), `substitute` (the agent did the part that teaches) or `none`.
2. Write the correction without looking. The `mistake-review` skill checks it against the source and drafts the card; you edit it.
3. Close a mistake only after you get it right later without help, from memory. Mark it `closed YYYY-MM-DD`.
4. Each card ends with a link to its source note. `check_cards.py` fails a card without one and a question that appears twice in the vault.

## Mistake log

Format of one entry: `YYYY-MM-DD, [[Concept_Name|Concept name]]: I answered X. The answer is Y. I went wrong because Z. Kind: reasoning. AI: none. Open.`

## Corrected cards
