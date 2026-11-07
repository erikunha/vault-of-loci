---
type: spec
tags: [type/spec]
---

# Spec: the study layer

Every concept, reference and guide note is study material, not just an index entry.

## Order

1. `> [!tldr] In 3 lines` right after the title.
2. `## Study explanation`: the first `##` section.
3. `## Key takeaways`: right after it.
4. Everything else (details, tables, related notes, flashcards, sources).

`90_System/Scripts/validation/check_study_layer.py` enforces this order.

## Study explanation

Prose in paragraphs, 400 to 900 words, the way a good teacher explains to someone who can code but met the topic last week. It includes:

- the problem the idea solves;
- one worked example from start to finish;
- the most common mistake and why it happens;
- how it connects to two other notes.

## Key takeaways

- **Remember:** two or three sentences.
- **Common confusion:** what people mix it up with.
- **Exercise:** a task to do without looking.

## Flashcards

5 to 8 cards `question::answer`, at least one cloze with `==gap==`. Write them yourself, or edit every card an AI drafts.
