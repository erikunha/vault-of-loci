---
type: guide
topic: "Reading research papers in three passes and turning them into verified reference notes"
updated: 2026-11-07
tags: [type/guide, flashcards]
---

# Research reading pipeline

> [!tldr] In 3 lines
> Read a paper in up to three passes: a 5 to 10 minute scan, a careful read of up to an hour, and a re-creation of the work for the papers that matter most.
> Each pass ends with something you can check: the five Cs, a summary you can give someone else, the paper's structure rebuilt from memory.
> In this vault a paper becomes a reference note only after you open its DOI or arXiv page, and every claim you reuse cites that note.

## Study explanation

The problem is simple to state. A research track, or any track that leans on papers, puts tens of papers in front of you, and reading each one from the first word to the last is slow and leaves little behind. Keshav describes a method he used for years: read a paper in up to three passes, where each pass has its own goal and builds on the one before ([F1]).

The first pass takes about five to ten minutes. Read the title, the abstract and the introduction with care, then only the section and subsection headings, then the conclusions, and glance over the references. At the end you should answer the five Cs: the category of the paper (a measurement, an analysis, a prototype), its context (which papers and theory it builds on), whether its assumptions look correct, its main contributions, and whether it is clearly written. Many papers stop here, and that is a result, not a failure: you now know where the paper sits and whether it deserves more of your time.

The second pass takes up to an hour. Read with care but skip details such as proofs. Look hard at figures and graphs: are the axes labelled, are there error bars? Mark the references you have not read. The test of this pass is that you can summarize the main thrust of the paper, with its evidence, to someone else. If you cannot, Keshav lists three honest options: set the paper aside, come back after reading background material, or go on to the third pass.

The third pass is for the few papers your work depends on. Try to re-create the work in your head, making the same assumptions as the authors, and compare your version with theirs. That comparison shows the innovations and the hidden assumptions. It takes about four or five hours for a beginner and about one hour for an experienced reader. At the end you can rebuild the paper's structure from memory and name its strong and weak points.

A worked example. You start a research track on spaced repetition and find a paper on scheduling algorithms. First pass, eight minutes: it is an algorithm paper, it builds on earlier memory models, its assumptions look reasonable, its contribution is a scheduler, and it is clear. You decide it matters, so you do a second pass in fifty minutes, write a three-sentence summary closed book, and only then open the paper again to check it. Two of your sentences hold; one mixes up the training data with the test data. That gap becomes a card. The paper is central to your question, so a week later you do the third pass on its evaluation section only.

The most common mistake is to start at the first word and push through to the last. It feels thorough, but it spends an hour on papers that a ten-minute scan would have filtered out, and it gives you nothing to test yourself on. The second mistake is the opposite: summarizing from the abstract. The abstract is the authors' claim, not the evidence.

The method fits the rest of this vault. The closed-book summary after the second pass is [[Retrieval_Practice|retrieval practice]]: recalling it is what makes it last, and the check against the paper shows what you missed. For a whole literature survey, Keshav suggests finding a few recent highly cited papers, reading their related-work sections, and following the papers and venues they keep citing. [[Studying_with_AI|Studying with AI]] explains why the agent may find and summarize papers for you but should not write your closed-book summary. When you finish, `export_bibtex.py` turns your reference notes into a bibliography.

## Key takeaways

- **Remember:** one paper, up to three passes. Each pass has a stopping test: the five Cs, a summary someone else understands, the paper rebuilt from memory.
- **Common confusion:** a first pass is not skimming the abstract. It reads the introduction, headings and conclusions so you can judge the paper, not repeat its claim.
- **Exercise:** pick a paper you saved and never read. Give it a first pass with a timer set to ten minutes, then write the five Cs without looking.

## Pipeline in this vault

1. **First pass.** Fill the five Cs in a session note. Stop here if the paper does not serve the track.
2. **Verify.** Open the DOI or arXiv page yourself. The `process-paper` skill writes a reference note in `40_References/Papers/` with `verified: true` only after that check. No identifier, no note.
3. **Second pass.** Write the summary closed book, then check it against the paper. Each gap becomes a card with a link to the reference note.
4. **Third pass.** Only for papers your work depends on. Record the assumptions you challenged in the reference note.
5. **Survey.** For a research track, keep a `Synthesis_Matrix` in `practice/` (one row per paper, one column per question), filled from your passes, not from abstracts.
6. **Export.** `export_bibtex.py` writes BibTeX and CSL JSON from the reference notes.

## Flashcards

Source: [F1] Keshav (2007), https://doi.org/10.1145/1273445.1273458

What are the three passes of the three-pass method, in order?::A 5 to 10 minute scan, a careful read of up to an hour that skips proofs, and a re-creation of the work.
What are the five Cs at the end of the first pass?::Category, context, correctness, contributions and clarity.
What should you be able to do after the second pass?::Summarize the paper's main thrust, with its evidence, to someone else.
What is the key to the third pass?::Re-create the work with the authors' assumptions and compare your version with theirs.
How long does the third pass take, by Keshav's estimate?::About four or five hours for a beginner and about one hour for an experienced reader.
When should a reference note get `verified: true` in this vault?::Only after you opened its DOI or arXiv page yourself.
After the second pass you write the summary ==closed book==, then check it against the paper.

## Not verified

- The time estimates are Keshav's experience, not a measured study.
- The literature survey steps are summarized from the paper's short section 3 and were not tested here.

## Sources

- [F1] Keshav, S. (2007). How to read a paper. *ACM SIGCOMM Computer Communication Review*, 37(3), 83-84. doi:10.1145/1273445.1273458
