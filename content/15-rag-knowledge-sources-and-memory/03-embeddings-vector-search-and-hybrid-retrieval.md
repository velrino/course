# Embeddings, Vector Search, and Hybrid Retrieval

## Learning objectives

- Distinguish lexical, dense, filtered, hybrid, and reranked retrieval.
- Select retrieval settings with labeled queries and recall measurements.
- Run a small vector index locally without exposing it to a network.

## Retrieval methods solve different failures

Lexical search rewards shared terms and is strong for product codes, names, quotations, and exact error messages. Dense embeddings place semantically related text near each other, helping when the question and source use different wording. Neither dominates every dataset. Hybrid retrieval combines candidate lists, often with reciprocal rank fusion (RRF), then an optional reranker scores the best candidates more carefully.

Similarity is not authorization. Apply tenant, classification, language, and effective-date filters as part of the query. In approximate vector search, filters and index settings interact; measure the actual results rather than assuming `top_k=5` is sufficient.

Use retrieval metrics independently from answer quality. For a question with one or more relevant chunks:

- `hit@k`: at least one relevant chunk appears in the first `k`.
- `recall@k`: fraction of all labeled relevant chunks retrieved.
- reciprocal rank: `1 / rank` of the first relevant result.
- latency percentiles: p50 and p95, not only the average.

## Free local practice

Create an isolated environment and install `qdrant-client`, `fastembed`, and `rank-bm25`. Use Qdrant's in-process local mode so no service or account is required:

```python
from qdrant_client import QdrantClient

client = QdrantClient(path="./vector-data")
```

Index your chunks with a local embedding supported by FastEmbed. Store `source_id`, `audience`, and `effective_at` as payload. Build four retrievers over the same corpus:

1. BM25 only.
2. Dense similarity only.
3. Dense similarity with an audience filter.
4. BM25 plus dense results fused by RRF, where a document's contribution is `1 / (60 + rank)`.

Label 15 queries, deliberately including identifiers, paraphrases, ambiguous wording, and one question outside the corpus. Save the query set as JSON Lines. Measure `hit@3`, `recall@5`, mean reciprocal rank, and p95 latency. Inspect every miss and assign a reason: absent knowledge, poor chunk, vocabulary mismatch, filter error, embedding weakness, or insufficient candidate count.

The out-of-corpus query should not be treated as a retrieval success just because some nearest neighbor always exists. Add a conservative evidence threshold or a second-stage relevance check, then verify that it abstains.

## Completion criteria

- The same labeled dataset compares four retrieval configurations.
- Access metadata is tested with a query that must not return a restricted chunk.
- Metrics and per-query results are saved with configuration and model identifiers.
- The system abstains on at least one deliberately unsupported question.

## References

- [Qdrant local quickstart](https://qdrant.tech/documentation/quick-start/) - local deployment, insertion, queries, and filters.
- [Qdrant hybrid and multi-stage queries](https://qdrant.tech/documentation/search/hybrid-queries/) - dense/sparse fusion and reranking patterns.
- [Qdrant filtering](https://qdrant.tech/documentation/concepts/filtering/) - payload conditions used for scoped retrieval.
- [Sentence Transformers semantic search](https://www.sbert.net/examples/sentence_transformer/applications/semantic-search/README.html) - bi-encoder retrieval and corpus/query encoding.
- [FAISS documentation](https://faiss.ai/) - algorithms and tradeoffs for local similarity search.
