# Grounded Generation and RAG Evaluation

## Learning objectives

- Separate retrieval quality from answer correctness and groundedness.
- Design prompts and output schemas that make evidence use inspectable.
- Build a reproducible evaluation set without a paid judge model.

## Evidence before eloquence

A grounded answer makes only claims supported by retrieved evidence, distinguishes source statements from inference, cites the supporting passage, and abstains when evidence is insufficient or conflicting. Prompt wording helps, but enforcement also belongs in code: constrain the context, require structured citations, validate cited chunk IDs, and reject citations not present in the retrieval result.

Use an output shape such as:

```json
{
  "answer": "...",
  "claims": [
    {"text": "...", "chunk_ids": ["policy-v2:s3"], "support": "direct"}
  ],
  "status": "answered"
}
```

Allowed statuses might be `answered`, `insufficient_evidence`, and `conflicting_sources`. This makes abstention a valid product behavior rather than a model failure.

Evaluate layers separately. Retrieval evaluation asks whether the right evidence appeared. Generation evaluation asks whether claims are entailed by that evidence, answer the question, include necessary qualifications, and avoid unsupported additions. End-to-end correctness alone hides the cause: a model might know an answer without using the source, or a perfect source might be ignored.

## Free local practice

Create 25 cases in `rag-eval.jsonl`. Each record should include question, expected chunk IDs, key answer facts, forbidden claims, and expected status. Include:

- direct fact lookup;
- a question requiring two sources;
- a source with an exception;
- conflicting versions where the effective date matters;
- an unanswerable question;
- an attempted instruction embedded inside a retrieved document.

Run a local model through Ollama if your machine permits, or evaluate previously generated answers. Implement deterministic checks in Python:

1. all cited IDs were actually retrieved;
2. expected IDs appeared within `k`;
3. key facts are present after lowercase/whitespace normalization;
4. forbidden claims are absent;
5. unsupported questions return the expected abstention status.

Then perform blinded human review with a 0-2 rubric for correctness, groundedness, completeness, citation accuracy, and clarity. Randomize labels `A` and `B` when comparing two configurations. Save the prompt, corpus hash, model/version, temperature, random seed where supported, and code commit. A result without configuration provenance cannot support a release decision.

## Completion criteria

- The dataset contains at least six distinct failure modes, not only easy fact questions.
- Retrieval and generation metrics are reported separately.
- The validator rejects a fabricated citation ID.
- A second reviewer can reproduce the run or evaluate stored outputs with the same rubric.

## References

- [RAGAS metrics concepts](https://docs.ragas.io/en/stable/concepts/metrics/) - decomposition of retrieval and response quality.
- [MLflow evaluation datasets](https://mlflow.org/docs/latest/genai/datasets/) - golden sets, regression cases, and dataset lifecycle.
- [NIST GenAI Profile](https://doi.org/10.6028/NIST.AI.600-1) - confabulation measurement and structured testing guidance.
- [Ollama API documentation](https://docs.ollama.com/api/introduction) - local model API for optional generation runs.
