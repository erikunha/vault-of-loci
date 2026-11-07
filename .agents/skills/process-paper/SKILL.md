---
name: process-paper
description: Turn a paper into a verified reference note in 40_References/Papers with the study layer. Use when the user adds or asks about a paper. Writes files, so only run when asked.
---

1. Verify the paper exists: arXiv ID, DOI or publisher page. If it cannot be verified, stop and say so.
2. File name: `Short_Title_(Author_et_al.,_YYYY).md`.
3. Frontmatter: `type: reference`, `subtype: paper`, `year`, `authors`, `link`, `arxiv` or `doi`, `venue`, `concepts`, `verified: true`, `checked: YYYY-MM-DD`, `tags: [type/reference, flashcards]`.
4. Body: `> [!tldr] In 3 lines`, `## Study explanation`, `## Key takeaways`, then problem, method, results with numbers from the paper, limitations, and how it connects to the concepts.
5. Numbers come from the paper's own tables. Mark anything not checked as "not verified".
6. Run `run-checks` and add a line to `90_System/Agent_Log/YYYY-MM.md`.
