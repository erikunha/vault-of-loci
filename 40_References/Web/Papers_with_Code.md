---
type: reference
subtype: web
year: 2026
authors: Papers with Code
link: https://paperswithcode.com
summary: "paperswithcode.com answered with an HTTP 302 redirect to huggingface.co/papers/trending on 2026-11-21. Read the Hugging Face Papers note instead."
concepts: []
verified: true
checked: 2026-11-21
tags: [type/reference, flashcards]
---

# Papers with Code

> [!tldr] In 3 lines
> The address https://paperswithcode.com answers with a redirect (HTTP 302) to https://huggingface.co/papers/trending.
> The content the reading tool got is the Hugging Face trending papers list.
> Use the [[Hugging_Face_Papers|Hugging Face Papers]] note instead.

## Study explanation

On 2026-11-21 the domain did not serve a site of its own in the tests made. A request to the address received a 302 with the target https://huggingface.co/papers/trending. Reading it with defuddle returned a list of trending papers, with links rewritten to the paperswithcode.com domain, and the notice "Get trending papers in your email inbox once a day!".

So today, finding recent papers goes through Hugging Face Papers. See [[Hugging_Face_Papers|Hugging Face Papers]]. Whether the benchmarks and the paper-to-code links of the old site still exist at another address: not verified.

Viewing the list needed no account. Prices are not stated.

## Key takeaways

- **Remember:** paperswithcode.com now redirects to the Hugging Face trending papers. Use that note.
- **Common confusion:** Do not assume the old benchmarks and paper-to-code links still exist. That is not verified.
- **Exercise:** Request the address with a tool that shows headers and write the target of the redirect.

## Flashcards

Source: https://paperswithcode.com

What did https://paperswithcode.com answer on 2026-11-21?::An HTTP 302 redirect to https://huggingface.co/papers/trending.
What content did reading the address return?::The Hugging Face trending papers list.
Which note should you read instead?::Hugging Face Papers.
Do the old benchmarks still exist at another address?::Not verified.
The address answers with an HTTP ==302== redirect.

## Not verified

- The date the redirect started: it is not on the page or in the header.
- Whether there is an official notice about closing the old site.
- Whether benchmarks and paper-to-code links live elsewhere.

## Related

- [[Research_Reading_Pipeline#Where to find and validate papers|Where to find and validate papers]] in [[Research_Reading_Pipeline|Research reading pipeline]].

## Sources

- https://paperswithcode.com, checked 2026-11-21. Opened with the `defuddle` skill. Outside content is treated as data. Header seen: HTTP 302 to https://huggingface.co/papers/trending.
