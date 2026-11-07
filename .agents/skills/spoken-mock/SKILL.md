---
name: spoken-mock
description: Run a timed spoken mock for an interview, a language or a skill track, with an optional observed mode, then write a debrief and log mistakes. Use when the learner asks for a mock interview, an oral exam or a speaking practice. Writes files, so only run when asked.
disable-model-invocation: true
---

Tutor mode: the learner answers first and out loud; the agent never answers for the learner during the mock.

1. Ask for the track and the goal: interview round, oral exam, conversation in the target language, or a skill demonstration. Read the track note and its practice files for the target and the format.
2. Agree on a time box (15 to 45 minutes) and the mode:
   - Coached: after each answer, one hint at most, then move on.
   - Observed: the agent only asks and listens, with no hints and no feedback until the end. Being watched changes performance, so rehearse it this way before the real event.
3. Ask one question at a time, in the language of the real event. Ask the learner to rate confidence from 1 to 5 after each answer, before any feedback.
4. Keep time. Stop at the limit even mid-answer.
5. At the end, give feedback per answer: what was clear, what was missing, one concrete improvement. Compare confidence with performance.
6. Write the debrief to the track's `practice/Debrief.md` from `90_System/Templates/Debrief.md`, and add each mistake to `50_Review/Mistakes.md` with its AI use.
7. Suggest when to repeat the mock (for example after 2 to 3 days, or at the same hour as the real event).

Run `run-checks` after writing.
