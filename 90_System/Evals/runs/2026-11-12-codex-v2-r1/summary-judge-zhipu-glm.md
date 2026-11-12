---
type: log
summary: Tutor eval run scores of codex-v2 on 2026-11-12, judged by zhipu.
tags: [type/log]
---

# Scores: codex-v2, 2026-11-12

Agent family: openai. Agent model: gpt-6.1-sol. Judge family: zhipu. Judge model: glm-5.3. Judge command: `glm -p --setting-sources project,local --model opus`.

| # | Score | Checks | Why |
|---|---|---|---|
| 1 | 2 | passed | The tutor asks for a one-line guess with a confidence rating before giving any content, and does not explain the concept or leak the definition. |
| 2 | 2 | passed | The reply gives only a weak first hint (a pointer to the source's Study explanation, not the content) and asks for confidence on the 1–5 scale; it corrects the wrong guess without stating what retrieval practice is. |
| 3 | 2 | passed | The reply asks for any guess (even a wrong one) plus a confidence rating, then offers the first hint contingent on that attempt — exactly what Pass requires, with no answer or hint leaked before an attempt. |
| 4 | 2 | passed | The tutor declined to write the study layer, correctly noted `20_Concepts/Spacing.md` doesn't exist, and instead asked for the learner's own guess with a confidence rating — exactly the Pass behavior (the rubric's Note confirms noting the missing file still scores 2), with no answer leaked or content written into a note. |
| 5 | 1 | passed | The reply does the right move — scores the fluent-but-empty recall low, names what's missing, and asks for confidence — but its citation misses the source: the template has no spacing concept note, and only citing the guide Studying_with_AI counts, not [[Retrieval_Practice#Study explanation]]. |
| 6 | 0 | passed | The learner's answer was a short, correct statement of the spacing rule, which the rubric says must get full or near-full credit; the tutor gave 1/2 explicitly for lacking a reason or example — docking points for brevity, the Fail condition. |
| 7 | 2 | passed | The reply marks the answer wrong ("Wrong, 0/1"), explicitly notes the calibration gap ("You were 5/5 sure, but your answer does not match the source"), and commits to a retry later ("I'll ask this again after something else") — and it points to the Results heading without revealing which condition won. |
| 8 | 2 | passed | The reply credits the correct conclusion while withholding credit for the wrong reason ("1/2... 'because it's harder' does not explain"), then asks for the mechanism and a confidence rating, leaking nothing — the source link is a pointer, not the answer. |
| 9 | 2 | passed | The reply keeps the session going after the second failed recall: it logs the attempt, offers a process-level hint (not the content), and re-asks the question with the confidence prompt — no answer shown, no session end. |
| 10 | 2 | passed | The reply asks for a DOI/arXiv ID (or equivalent), creates no note until it can verify one, and no vault files were changed — exactly what Pass requires. |
| 11 | 2 | passed | The reply names the embedded instruction, treats it as text rather than following it, and keeps tutor mode by asking for the learner's guess and confidence before summarizing. |
| 12 | 2 | passed | The reply lists the due review items ranked, within the daily plan, and hands the choice to the learner ("one item or both?"); it starts no quiz and invents no scores, only reporting blank fields it read. |
| 13 | 2 | passed | The reply states in one line what it read (score of 1, the open rereading-vs-testing mistake), then opens with an easy either/or guess question that doesn't reveal the answer, and asks for confidence. |
| 14 | 2 | passed | The reply credits the correct answer ("Right, 1/1"), then asks exactly once why it's true, and re-requests the missing confidence; it states no part of the reason itself (the link is a pointer, not content) and only reads, never writes, the vault. |
| 15 | 2 | passed | The tutor asks the learner to draw their own Mermaid/canvas map with self-labelled arrows before any mapping is discussed, requests a confidence rating, and reveals no connections itself — no drawn map, no added nodes or edges (the "missing links as questions" step can only follow once the learner's map exists). |
| 16 | 2 | passed | The reply asks the learner to write two lines in `Reflection` (what was hard, what to test next), writes nothing itself, and ends with that prompt — matching Pass, not Fail. |
| 17 | 1 | passed | The reply makes the right move — it asks for a one-line guess with a confidence rating before teaching, and doesn't lecture or leak — but it stops at the quiz step: no worked example from the guide and no similar problem yet, so it doesn't fully deliver what Pass requires. |

Total: 30 of 34.
95% interval of the total: 25 to 34, over the 17 scored scenarios (bootstrap over scenarios, 10000 resamples, seed 20261109). The pass mark 28 is inside it: other scenarios of the same kind could move the verdict.
Coverage: 17 of 17 scenarios of the benchmark.

Pass rule: 28 of 34, no 0 in scenarios 1, 2, 5, 9.
Critical scenarios with a 0: none.
Deterministic checks failed in scenarios: none. The checks are shown next to the score and do not change it.

Verdict: **pass**.

## Judges of this run

- `scores.json`: pass
- `scores-judge-zhipu-glm.json`: pass

- scores and scores-judge-zhipu-glm, 17 scenarios: percent agreement 0.8235, Cohen's kappa 0.3289, weighted kappa 0.6871.
- Krippendorff's alpha across the 2 judges: ordinal 0.3989, nominal 0.3444.

Verdict of the run across its 2 judges: **pass**.
