# Source and Reference Policy

## Objectives

Judge sources by what they can establish, keep fast-changing instructions maintainable, and avoid treating marketing material as technical evidence.

## Source hierarchy

Use the strongest available source for each kind of claim:

1. Laws, regulations, and standards: the issuing authority or official publication.
2. Software behavior and APIs: version-matched official documentation and source repository.
3. Research claims: the original paper, dataset card, or benchmark report.
4. Operational techniques: maintained engineering guides with explicit assumptions and examples.
5. Tutorials and commentary: useful for alternative explanations, but verify commands and claims upstream.

Vendor documentation reliably describes a vendor's interface, not whether that interface is the best choice. A framework quickstart proves that a happy-path example exists; it does not prove production reliability, security, or return on investment.

## Reading a reference

Record the page title, organization or authors, URL, access date, and the exact claim it supports. Check version selectors, deprecation banners, licensing, prerequisites, and whether an example sends data to a third party. For a research paper, inspect the task definition, comparison baseline, data, metric, limitations, and whether the result transfers to your use case.

## Link maintenance

Each lesson links directly to references rather than search-result pages. When a link breaks:

1. Search the same official domain for the page title.
2. Prefer a current canonical page over an unofficial mirror.
3. Update commands only after testing them.
4. Note a meaningful semantic change in the learning journal.

Do not silently replace an original paper with a blog summary. Both may be linked when the summary helps comprehension, but their roles differ.

## Practice

Select one technical claim from an AI tutorial. Trace it to official documentation or an original paper. Write a short source note explaining what the stronger reference supports, what it does not support, and whether the tutorial omitted a version or constraint.

## Completion criteria

- You can classify a source by the claim it is qualified to support.
- Your source note distinguishes documented behavior from marketing or inference.
- You checked date, version, prerequisites, and license where relevant.

## References

- [Digital Object Identifier Foundation: DOI Handbook](https://www.doi.org/doi-handbook/)
- [GitHub Docs: About CITATION files](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files)
- [Hugging Face: Model Cards](https://huggingface.co/docs/hub/model-cards)
- [Hugging Face: Dataset Cards](https://huggingface.co/docs/hub/datasets-cards)
