---
name: new-concept-note
description: Create or deepen a concept note in 20_Concepts following the study layer spec. Use when a lesson, paper or question introduces a concept worth its own note. Writes files, so only run when asked.
---

1. Check `20_Concepts/` first: one idea per note. If the concept exists, extend it instead of creating another.
2. File name: the concept name with underscores (`Retrieval_Practice.md`); the `# Title` keeps spaces.
3. Frontmatter: `type: concept`, `category`, `courses`, `lessons`, `aliases`, `tags: [type/concept, flashcards]`.
4. Follow `90_System/Specs/Study_layer.md`: `> [!tldr] In 3 lines`, then `## Study explanation` (400 to 900 words of prose) and `## Key takeaways`, then the rest.
5. Every claim from a lesson cites its transcript timestamp; every outside claim cites a note in `40_References/`. Never invent a reference.
6. Add 5 to 8 flashcards `question::answer`, one cloze with `==gap==`.
7. Run `run-checks` and add a line to `90_System/Agent_Log/YYYY-MM.md`.
