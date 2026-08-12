# Assessment and Evidence

## Objectives

Evaluate progress using observable work rather than attendance, confidence, or a model's polished prose.

## Module score

Score each module out of 100:

| Evidence | Points |
|---|---:|
| Retrieval check completed without notes | 10 |
| Lesson practices and small exercises | 20 |
| Independent module artifact | 30 |
| Normal, edge, misuse, and failure tests | 25 |
| Reflection, limitations, and source notes | 15 |

A score of 70 is a useful advancement threshold, but apply two additional rules:

- All safety-critical tests must pass even when the numerical score exceeds 70.
- An artifact that cannot be reproduced from its instructions is incomplete.

## Evidence package

For each module, keep:

```text
module-evidence/
  artifact/
  test-results/
  decision-record.md
  reflection.md
```

The decision record should state the problem, alternatives considered, chosen approach, assumptions, and consequences. The reflection should identify at least one failure or incorrect assumption. A perfect-looking report with no observed failure is usually evidence that testing was too narrow.

## Evaluation dataset discipline

Agent and model tests need versioned cases. Each case should include an input, relevant context, expected properties, prohibited outcomes, and a reason the case matters. Separate development cases from final evaluation cases. Otherwise repeated prompt editing can overfit the test set while creating the illusion of general improvement.

Use multiple measures. Task success alone can hide unsafe tool calls; zero tool errors can hide a system that refuses every task. Record quality, safety, latency, and resource use separately, then define release thresholds before seeing final results.

## Practice

Create a five-case evaluation set for your running business process. Include one routine case, one missing-data case, one conflicting-instruction case, one malicious or irrelevant input, and one external-system failure. Define expected properties without prescribing exact prose.

## Completion criteria

- You have a scoring sheet and evidence directory convention.
- Your evaluation cases include edge, misuse, and infrastructure failures.
- Release thresholds were written before the final run.
- Another learner could inspect the evidence and reproduce your conclusion.

## References

- [NIST AI Resource Center: Testing, Evaluation, Verification, and Validation](https://airc.nist.gov/)
- [Google Rules of Machine Learning](https://developers.google.com/machine-learning/guides/rules-of-ml)
- [Model Cards for Model Reporting](https://research.google/pubs/model-cards-for-model-reporting/)
