---
name: vault-search
description: Find which notes and sections in the vault talk about a topic, ranked by relevance, with python3 -I 90_System/Scripts/search_vault.py (BM25, standard library, offline). Returns locations to open, never answers. Use when the learner or the agent needs the source for a question, after the learner's attempt.
---

Tutor mode: search finds sources; it does not answer. Before the learner has attempted a question, do not search for its answer.

1. Run `python3 -I 90_System/Scripts/search_vault.py "<words>" --top 10`. Use the learner's own words first, then synonyms.
2. Each result is `path:line  heading  (score)`. Open the section from that line, not the whole file, and say which note and heading it came from.
3. If nothing matches, say so and offer `process-web` or `process-paper` to add a verified source. Do not fill the gap from memory.
