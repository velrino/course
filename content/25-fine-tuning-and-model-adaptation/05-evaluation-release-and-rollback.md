# Evaluation, Release, and Rollback

## Learning objectives

Compare adapted and base models, document a release, detect regressions, and roll back the complete serving configuration.

## Comparative evaluation

Evaluate the adapted model against the base model and the strongest non-training baseline. Report uncertainty and per-slice results, not only one aggregate. Useful slices include input length, language, domain subtype, uncommon labels, adversarial phrasing, and cases requiring abstention.

Measure the property fine-tuning targeted and properties it could damage:

- task quality and schema adherence;
- unsupported claims and unsafe compliance;
- privacy or memorization probes;
- latency, throughput, memory, and artifact size;
- robustness to formatting and distribution shift;
- calibration or confidence behavior where used.

Inspect memorization by searching for suspicious overlap with training examples and testing canary strings placed only in controlled experiments. Never insert real secrets as canaries.

## Release package

A reproducible release identifies the base model revision, adapter checksum, tokenizer and chat template, inference settings, prompt wrapper, tool schemas, dataset card, evaluation report, model card, license analysis, and deployment environment. The unit of rollback is this complete package. Rolling back only adapter weights while leaving a changed tokenizer or prompt can preserve the failure.

Use a staged rollout with small traffic, clear alerts, and a kill switch. Define who can activate or disable the adapter. Preserve input privacy when logging and do not retain raw prompts by default.

## Free local practice

Create a model card for the hypothetical adapter from this module. Include intended use, out-of-scope use, training data summary, evaluation slices, limitations, ethical considerations, and rollback identifier. Build a release checklist and simulate rejecting a candidate because one safety slice regressed despite improved average task quality.

## Completion criteria

- Adapted, base, and non-training baselines use the same held-out evaluation.
- Safety and operational regressions have release thresholds.
- The complete serving package has an immutable version.
- A tested rollback and ownership path exists.

## References

- [Model Cards for Model Reporting](https://research.google/pubs/model-cards-for-model-reporting/)
- [Hugging Face model cards](https://huggingface.co/docs/hub/model-cards)
- [Hugging Face security guidance](https://huggingface.co/docs/hub/security)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
