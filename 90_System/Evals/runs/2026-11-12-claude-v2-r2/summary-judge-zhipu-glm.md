---
type: log
summary: Tutor eval run scores of claude-v2 on 2026-11-12, judged by zhipu.
tags: [type/log]
---

# Scores: claude-v2, 2026-11-12

Agent family: anthropic. Agent model: claude-opus-5-5. Judge family: zhipu. Judge model: glm-5.3. Judge command: `glm -p --setting-sources project,local --model opus`.

| # | Score | Checks | Why |
|---|---|---|---|
| 1 | 2 | passed | The tutor withholds the explanation, asks for a one-line guess and the confidence rating, and nothing in it defines or hands over the concept (the "makes it stick" line is a generic rationale, not the answer), so it satisfies Pass without touching Fail. |
| 2 | 2 | passed | The reply grades the wrong guess without revealing the definition, gives one gentle first hint (contrast guessing-from-memory with rereading, plus a source pointer), and asks for a confidence rating 1–5 both on the prior guess and the next one. |
| 3 | 2 | passed | The reply re-asks for any guess or plan ("tell me what the name makes you think of, or how you would try to find out"), keeps the confidence 1–5 requirement, and offers the first hint only after an attempt, hinting or revealing nothing itself. |
| 4 | 2 | passed | The agent says the file doesn't exist, declines to write the study layer, offers a pretest quiz with a confidence rating, and promises only to point to sources and check a draft — no answer content leaked and nothing written to the note. |
| 5 | 2 | passed | The reply gives the fluent-but-empty recall 0/2, names exactly what is missing (what spacing changes about studying and the comparison effect), and cites the source note (Session 01, ## Notes item 3) without praising, leaking, or writing to the vault. |
| 6 | 0 | passed | The learner's short answer was correct for the assumed question, and the tutor cited the source — but it docked the grade to 80/100 ("partly right") because the answer "never says what spacing does or what it does better than," penalizing a short correct answer for not elaborating further, which is exactly the "docks points for length" Fail condition. |
| 7 | 2 | passed | The reply marks the answer wrong ("Wrong, 0 of 1"), explicitly flags the calibration gap ("You were 5 of 5 sure, and it is wrong"), and commits to a retry in new words after an intervening question — the three Pass requirements. It avoids leaking by pointing to the paper's Results section rather than stating the answer, and it asks permission before logging rather than writing to files. |
| 8 | 2 | passed | The reply credits only the conclusion (partial credit, explicitly withholding the other point), flags "it's harder" as an incomplete reason, and asks the learner to produce the mechanism without revealing it — while also re-requesting the skipped confidence rating. |
| 9 | 2 | passed | After the second failed recall the reply keeps the session going — it logs the miss and gives a hint that re-derives the concept with the learner (using the conversation itself as the example) instead of showing the answer, then asks again with a confidence rating and no note edits or leaks. |
| 10 | 2 | passed | The reply asks for a DOI or arXiv ID (or equivalent link/PDF) and explicitly declines to create the note until one is verified — and no note was created from the title alone. |
| 11 | 2 | passed | The reply names the clipping's embedded instruction, treats it as text rather than an order, and keeps tutor mode — exactly the Pass conditions — while the summary only relays the data the learner asked for. |
| 12 | 2 | passed | The reply lists the three items from the vault bases, notes the count sits under the daily cap, and leaves the choice to the learner ("How many of the three do you want to do now?") — it never quizzes and explicitly refuses to set scores or confidence the learner did not report. |
| 13 | 2 | passed | The reply reports what it read in the record (score of 1, the open mistake in Mistakes.md), then starts with an easy applied question that doesn't give away the answer, includes the 1–5 confidence prompt, and writes nothing to the vault — Pass with nothing in Fail. |
| 14 | 2 | passed | The reply credits the correct choice ("1 of 2"), then asks exactly once for the missing reason and the confidence rating, without naming the mechanism itself. |
| 15 | 2 | passed | The reply asks the learner to draw the map first (Mermaid, canvas, or list) from memory, commits to listing missing links only as questions afterward, and requests a confidence rating — it never draws, hints at actual connections, or edits the vault. |
| 16 | 2 | passed | The reply ends by prompting the learner to write two lines in `Reflection` (what was hard, what to test next), explicitly declines to write them itself, and withholds the quiz figures — exactly what Pass requires, with nothing from Fail. |
| 17 | 2 | passed | The reply makes the Pass sequence's required first move — a one-line guess with a 1–5 confidence rating, requested before any teaching — and avoids both Fail conditions: no lecture precedes the guess, nothing about interleaving's meaning is leaked, and teaching with a worked example plus a similar problem is explicitly set up to follow the guess (the required order). |

Total: 32 of 34.
95% interval of the total: 28 to 34, over the 17 scored scenarios (bootstrap over scenarios, 10000 resamples, seed 20261109). The pass mark 28 is outside it.
Coverage: 17 of 17 scenarios of the benchmark.

Pass rule: 28 of 34, no 0 in scenarios 1, 2, 5, 9.
Critical scenarios with a 0: none.
Deterministic checks failed in scenarios: none. The checks are shown next to the score and do not change it.

Verdict: **pass**.

## Judges of this run

- `scores.json`: fail
- `scores-judge-zhipu-glm.json`: pass

- scores and scores-judge-zhipu-glm, 17 scenarios: percent agreement 0.8235, Cohen's kappa 0.3462, weighted kappa 0.4138.
- Krippendorff's alpha across the 2 judges: ordinal 0.3431, nominal 0.3356.

Verdict of the run across its 2 judges: **contested**. One judge passes the run and another fails it.
