# Capstone: Evidence-Grounded RAG Assistant

## Objective

Build a retrieval assistant over a small public document collection that preserves provenance, abstains when evidence is absent, and resists instructions embedded in source content.

## Scenario

Use public policy, product manual, or standards documents with clear reuse rights. Users ask questions; the system retrieves passages and produces a concise answer with source identifiers. It must distinguish "not found in the collection" from "false."

## Required system

- Manifest containing document source, version, license, checksum, and access class.
- Reproducible parsing, chunking, and indexing pipeline.
- Baseline lexical search and one semantic or hybrid retriever.
- Access filter applied before context reaches the model.
- Prompt boundary labeling retrieved text as untrusted data.
- Answer schema containing response, cited passage identifiers, and abstention reason.
- Index refresh and deletion procedure.

The required version may use an extractive template rather than a hosted model. Model generation is an optional adapter.

## Evaluation

Write at least 50 questions: answerable, unanswerable, ambiguous, conflicting, outdated-version, cross-document, exact-identifier, and adversarial-instruction cases. Measure retrieval recall at `k`, citation correctness, claim support, abstention quality, access-control violations, latency, and index freshness.

Compare chunk sizes and lexical versus semantic retrieval without changing the evaluation set. Inspect false positives and false negatives. Do not use a model judge as the only ground-truth reviewer.

## Deliverables

- Corpus manifest and dataset card.
- Ingestion and retrieval code or workflow.
- Baselines, experiment log, evaluation set, and report.
- Threat model, system card, and deletion test.
- Demonstration of supported answer, abstention, conflict, and blocked injection.

## Completion criteria

- Every answer claim maps to a retrieved passage.
- Unavailable evidence causes abstention, not invention.
- Embedded instructions cannot change system policy or tools.
- Deleting a document removes it from retrieval and derived stores.

## References

- [Retrieval-Augmented Generation paper](https://arxiv.org/abs/2005.11401)
- [Sentence Transformers semantic search](https://www.sbert.net/examples/sentence_transformer/applications/semantic-search/README.html)
- [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/)
