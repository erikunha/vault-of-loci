---
name: new-concept-note
description: Create or deepen a concept note in 20_Concepts following the study layer spec. Use when a session, paper, book or question introduces a concept worth its own note. Writes files, so only run when asked.
disable-model-invocation: true
---

1. Check `20_Concepts/` first: one idea per note. If the concept exists, extend it instead of creating another.
2. File name: the concept name with underscores (`Retrieval_Practice.md`); the `# Title` keeps spaces.
3. Frontmatter: `type: concept`, `category`, `tracks`, `sessions`, `aliases`, `tags: [type/concept, flashcards]`.
4. Follow `90_System/Specs/Study_layer.md` (headings in `90_System/Specs/study_layer.json`): `> [!tldr] In 3 lines`, then the explanation section (400 to 900 words of prose) and the takeaways section, then the rest. Tutor mode: concept notes are the learner's own notes, so create the structure and leave the study layer and the cards for the learner to write. Draft them only when the learner asks, say it is a draft, and have the learner edit every card.
5. Every claim from a session cites its source (transcript timestamp, chapter or page); every outside claim cites a note in `40_References/`. Never invent a reference.
6. Add 5 to 8 flashcards `question::answer`, one cloze with `==gap==`.
7. Run `run-checks` and add a line to `90_System/Agent_Log/YYYY-MM.md`.
