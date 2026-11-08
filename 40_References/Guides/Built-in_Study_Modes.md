---
type: guide
topic: "ChatGPT study mode, Claude learning mode and Gemini Guided Learning, and how this vault differs"
updated: 2026-11-07
tags: [type/guide, flashcards]
---

# Built-in study modes

> [!tldr] In 3 lines
> ChatGPT, Claude and Gemini each ship a mode that asks questions and guides step by step instead of handing over answers.
> Those modes live inside one product's chat; this vault keeps the rules, your notes, your cards and the review queue in your own Markdown files.
> They work well together: use a study mode for a conversation, and this vault for what you keep, review and test later.

## Study explanation

Three vendors added a tutoring mode to their chat apps in 2025. OpenAI introduced study mode in ChatGPT on 2025-07-29 for logged-in Free, Plus, Pro and Team users ([F1]). It combines Socratic questioning, hints and self-reflection prompts, organizes explanations in sections, checks knowledge with quizzes and open questions, adapts to the learner's level using memory from previous chats, and can be switched on and off during a conversation ([F1]). OpenAI says it runs on custom system instructions written with teachers and learning scientists, and that this can produce inconsistent behavior across conversations ([F1]).

Anthropic introduced Learning mode on 2025-04-02 as part of Claude for Education, for universities, inside Projects ([F2]). In it, Claude asks how the student would approach a problem, asks what evidence supports a conclusion, points to the core principles, and offers templates for papers and study guides ([F2]). Google introduced Guided Learning in the Gemini app on 2025-08-06 ([F3]). It asks probing questions, works through problems in stages, adds images, diagrams, videos and quizzes, and is built on LearnLM, a family of models fine-tuned for learning ([F3]).

The three share the core idea of this vault's tutor mode: the learner does the thinking and the AI guides. The difference is where the work lives. In a chat mode, the rules belong to the product and the conversation stays in that product. In this vault, the rules are a text file (`AGENTS.md`) that any supported agent reads, so changing agents keeps the same tutor. Your explanations, cards, mistakes and checkpoint results are notes you own, scheduled for review by the Spaced Repetition plugin or exported to Anki. Every reference must be opened and verified, and a hand-run test (`90_System/Evals/Tutor_mode.md`) checks whether your agent follows the rules.

Each feature of the three modes has a counterpart here, written as a rule in `AGENTS.md` so it works the same in any agent. Adapting to your level ([F1]) comes from your own record: the agent reads `score`, `last_tested` and the mistakes file, and says what it read. Self-reflection prompts ([F1]) become two lines you write in the session's `Reflection`. Asking what supports a conclusion ([F2]) becomes one "why" after a correct answer. Diagrams ([F3]) become a map you draw in Mermaid or a canvas, where the agent lists missing links instead of drawing for you. Two features are left out on purpose: switching the mode off mid-conversation ([F1]), because asking to skip the attempt is answered with "guess first, then the explanation"; and a model fine-tuned for teaching ([F3]), because the vault works with any model. The evidence for each rule is in `40_References/Guides/Studying_with_AI.md`.

## Key takeaways

- ChatGPT study mode (2025-07-29), Claude Learning mode (2025-04-02) and Gemini Guided Learning (2025-08-06) all guide with questions instead of answers.
- ChatGPT study mode runs on system instructions, so OpenAI warns its behavior can vary; this vault's tutor mode is also an instruction, and the eval measures how well an agent follows it.
- What this vault adds is persistence and portability: rules, notes, cards and review queue are your files and work with any supported agent.
- Level, reflection, "why" questions and diagrams are rules in `AGENTS.md`, built on your files, so no single product is needed.
- Using both is fine: a study mode for the conversation, the vault for retrieval practice and spaced review afterwards.

## Flashcards

Source: [F1] OpenAI (2025), [F2] Anthropic (2025), [F3] Google (2025).

When did OpenAI introduce study mode in ChatGPT?::2025-07-29, for logged-in Free, Plus, Pro and Team users.
What powers ChatGPT study mode, according to OpenAI?::Custom system instructions written with teachers, scientists and pedagogy experts.
Where does Claude's Learning mode run?::Inside Projects, as part of Claude for Education for universities.
What model family is Gemini Guided Learning built on?::LearnLM, models fine-tuned for learning.
What does this vault keep that a chat study mode does not?::The rules, notes, cards and review queue as your own files, usable with any supported agent.
Where does this vault's tutor get your level from?::Your own files: score and last_tested in concept notes and 50_Review/Mistakes.md, not a chat memory.
Chat study modes and this vault share one idea: the ==learner does the thinking== and the AI guides.

## Not verified

- Current availability by plan, country or age for each mode was not checked after the announcement dates; the help pages may have changed.
- No study of learning outcomes for any of the three modes was read for this guide.

## Sources

- [F1] OpenAI (2025-07-29). Introducing study mode. https://openai.com/index/chatgpt-study-mode/ (read in full 2026-11-07)
- [F2] Anthropic (2025-04-02). Introducing Claude for Education. https://www.anthropic.com/news/introducing-claude-for-education (read 2026-11-07)
- [F3] Google (2025-08-06). Guided Learning in Gemini: from answers to understanding. https://blog.google/products-and-platforms/products/education/guided-learning/ (read 2026-11-07)
