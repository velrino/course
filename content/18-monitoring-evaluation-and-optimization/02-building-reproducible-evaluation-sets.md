# Building Reproducible Evaluation Sets

## Learning objectives

- Build representative, adversarial, and regression evaluation slices.
- Write deterministic and human/LLM-assisted scorers with explicit rubrics.
- Preserve enough provenance to reproduce a comparison.

## An evaluation set is a maintained product asset

Start with the product decision: what must be true before release? Convert real tasks and failure modes into cases. A useful suite includes common traffic, critical workflows, long-tail inputs, unsupported requests, attacks, languages, tool failures, and cases found in production. Avoid random examples that are easy to collect but unrelated to impact.

Store structured fields: stable case ID, input, permitted context, expected facts or actions, prohibited outputs/actions, rubric, tags, source provenance, author, creation date, and review status. Keep the test input immutable; corrections create a version. Separate a development set used during iteration from a held-out set used for release decisions.

Prefer deterministic scorers when a requirement is computable: JSON schema validity, exact tool/arguments, numeric tolerance, citation membership, maximum latency, absence of secrets, or expected abstention. Human rubrics handle contextual quality. Model-based judges scale review but can be biased by verbosity, position, prompt, and shared model errors. Calibrate them against blinded expert labels and report agreement, not only judge scores.

Reproducibility requires dataset version/hash, application commit, prompt and policy versions, model identifier, decoding settings, retriever/index version, tool fixtures, dependency lock, seed where honored, timestamp, and raw outputs. Hosted models may change behind a stable name; store provider snapshots when available and retain outputs for re-scoring.

## Free local practice

Create 40 JSON Lines cases for a fictional support assistant. Allocate explicit slices: 15 routine, 5 policy exceptions, 5 insufficient evidence, 5 tool calls, 5 privacy/security, and 5 malformed or multilingual. Write the expected outcome before generating responses.

Implement scorers in Python for schema validity, correct status, required facts, forbidden phrases, correct tool call, allowed citations, and latency budget. Then create a 0-2 human rubric for correctness, completeness, groundedness, and harm. Score ten cases twice in blinded random order and compare your own consistency.

Create a manifest with SHA-256 of dataset and outputs plus all configuration fields above. Change one prompt, run both versions on the same cases, and report paired differences per slice. Never claim improvement from a different case sample.

## Completion criteria

- The dataset covers named product risks and includes held-out cases.
- Expected outcomes predate model outputs and have reviewer/source provenance.
- Deterministic checks run automatically; subjective scoring uses an anchored rubric.
- A manifest lets another person identify the exact data, code, model, prompt, and outputs.

## References

- [MLflow evaluation datasets](https://mlflow.org/docs/latest/genai/datasets/) - golden sets, production-derived cases, and versioned evaluation records.
- [MLflow code-based scorers](https://mlflow.org/docs/latest/genai/eval-monitor/scorers/custom/) - deterministic custom evaluation functions.
- [G-Eval paper](https://arxiv.org/abs/2303.16634) - primary research on model-based evaluation with structured criteria.
- [Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena](https://arxiv.org/abs/2306.05685) - primary evidence and documented judge biases.
