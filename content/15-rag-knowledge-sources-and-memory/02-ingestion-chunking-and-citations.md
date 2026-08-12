# Ingestion, Chunking, and Citations

## Learning objectives

- Build a deterministic ingestion pipeline that preserves document meaning.
- Compare chunking strategies instead of choosing a size by intuition.
- Carry citation metadata from source file to final answer.

## Extraction is a data-quality problem

PDF text order, repeated headers, scanned pages, tables, and code blocks can all break naive extraction. Preserve both the raw artifact and a normalized representation. Record the extractor name and version, warnings, page or section boundaries, and a checksum. Never silently discard pages that produced no text; flag them for OCR or human review.

A chunk is the retriever's unit of evidence. Fixed-size chunks are simple but can cut a definition from its condition. Structure-aware chunks follow headings, paragraphs, list items, or code blocks and usually produce better citations. Overlap can restore nearby context, but excessive overlap creates near-duplicates and may crowd out diverse evidence.

Every chunk should have a stable identity and metadata such as:

```json
{
  "chunk_id": "guide-v3:s4:p2",
  "source_id": "guide-v3",
  "heading_path": ["Security", "Credentials"],
  "page": 17,
  "text": "...",
  "content_hash": "...",
  "effective_at": "2026-07-01",
  "audience": ["support"]
}
```

The final citation should be derived from this metadata, not invented by the model. Render a link, page, or section beside each supported claim. Keep the retrieved excerpt in traces so a reviewer can verify whether the citation actually entails the claim.

## Free local practice

Use plain Python and your local corpus from the previous lesson. Implement three splitters:

- approximately 800 characters with 120-character overlap;
- paragraph boundaries with a 1,200-character ceiling;
- heading-aware sections with oversized sections split by paragraph.

Create ten questions with a known supporting span. For each strategy, inspect the top five lexical matches using `sklearn.feature_extraction.text.TfidfVectorizer`, or implement a basic token-overlap score with the standard library. Record:

| question | expected chunk | found at rank | context complete | duplicate candidates |
|---|---|---:|---|---:|

`context complete` is a human judgment: does the retrieved chunk include the rule, its scope, and any important exception? Do not optimize only for rank. A tiny chunk may rank highly while omitting the exception that reverses the answer.

Add a citation renderer that produces a Markdown link whose label contains the title, section, and page and whose target is the canonical URL. Test it with a title containing punctuation and a source without page numbers. Reject records with no canonical locator.

## Completion criteria

- Ingestion is repeatable and retains raw source, normalized text, warnings, and hashes.
- At least three chunking strategies are evaluated on the same questions.
- Every indexed chunk has a stable ID and enough metadata to enforce access and render a citation.
- A reviewer can travel from an answer citation to the exact supporting source span.

## References

- [LangChain text splitters](https://docs.langchain.com/oss/python/integrations/splitters) - official implementation guidance for structure-aware splitting.
- [PyMuPDF text extraction recipes](https://pymupdf.readthedocs.io/en/latest/recipes-text.html) - extraction behavior and layout caveats for PDFs.
- [Tesseract user manual](https://tesseract-ocr.github.io/tessdoc/) - public documentation for local OCR.
- [scikit-learn text feature extraction](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction) - TF-IDF and bag-of-words retrieval primitives.
