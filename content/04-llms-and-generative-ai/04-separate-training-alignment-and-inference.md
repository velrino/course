# Separate Training, Alignment, and Inference

## Learning objectives

By the end of this lesson, you will be able to:

- distinguish pretraining, fine-tuning, preference optimization, retrieval, and prompting;
- explain how decoding changes output without retraining a model;
- reason about temperature, sampling, and reproducibility; and
- identify why fluent generations can still be unsupported.

## Different interventions change different layers

**Pretraining** adjusts many model parameters using a broad predictive objective over large datasets. **Instruction tuning** fine-tunes a pretrained model on examples of instructions and desired responses. **Preference optimization** uses comparative or reward signals to push behavior toward selected preferences. Other fine-tuning adapts behavior to a domain or task.

By contrast:

- **prompting** changes request-time instructions and examples;
- **retrieval-augmented generation** supplies external evidence at request time;
- **tools** let an application obtain data or perform actions; and
- **decoding settings** choose how to sample from output probabilities.

These do not mean the base model "learned" the supplied facts into its parameters. Keeping the distinction clear makes updates and failures easier to locate.

## Inference converts probabilities into output

At each step, a model produces scores for possible next tokens. A decoding method converts them to a selection.

- Greedy decoding chooses the highest-scoring token each time.
- Sampling draws from a distribution and can produce varied outputs.
- Temperature rescales logits before normalization; lower values usually concentrate probability, while higher values flatten it.
- Top-k sampling limits candidates to the highest `k` scores.
- Top-p sampling selects the smallest high-probability set whose cumulative mass reaches `p`.

Provider parameters differ. Read the documentation for the actual runtime. A fixed seed can improve repeatability in some systems but is not a universal guarantee across hardware, versions, batching, or provider updates.

## Why hallucinations occur

Next-token likelihood is not a truth-checking objective. A model can produce a plausible continuation when the request lacks evidence, when training patterns conflict, or when retrieved material is irrelevant. Instruction tuning may make the answer more useful, but it does not turn generated claims into database lookups.

Mitigations belong to a system:

- narrow the task;
- supply authoritative context;
- require traceable citations to that context;
- use tools for current or exact data;
- validate structured fields;
- permit abstention and escalation; and
- evaluate on adversarial and missing-evidence cases.

## Free local practice

Simulate temperature on fixed logits:

```bash
python3 - <<'PY'
from math import exp

logits = {"tool": 2.0, "answer": 1.0, "stop": 0.5}
for temperature in [0.25, 0.7, 1.0, 2.0]:
    scaled = {key: value / temperature for key, value in logits.items()}
    total = sum(exp(value) for value in scaled.values())
    probabilities = {key: round(exp(value) / total, 3) for key, value in scaled.items()}
    print(temperature, probabilities)
PY
```

Predict the direction of change before running it. Explain why temperature `0` cannot be implemented by literal division and is usually treated as a special deterministic mode. Then classify five application changes as training-time or request-time interventions.

## Completion criteria

- [ ] You distinguish parameter updates from request-time context.
- [ ] You explain greedy, temperature, top-k, and top-p decoding.
- [ ] You ran the simulation and interpreted the probability changes.
- [ ] You can state why fluent generation does not imply factual support.
- [ ] Your mitigation plan includes grounding, validation, abstention, and evaluation.

## References

- [Training Language Models to Follow Instructions with Human Feedback](https://arxiv.org/abs/2203.02155) - original InstructGPT paper describing supervised fine-tuning and reinforcement learning from human feedback.
- [Generation Strategies](https://huggingface.co/docs/transformers/generation_strategies) - official open-source documentation for greedy decoding, sampling, beams, constraints, and related settings.
- [LLMs: Fine-Tuning, Distillation, and Prompt Engineering](https://developers.google.com/machine-learning/crash-course/llm/tuning) - free comparison of ways to adapt LLM behavior and efficiency.
- [NIST Generative AI Profile](https://doi.org/10.6028/NIST.AI.600-1) - primary public guidance on risks and mitigations including confabulation and information integrity.

## Continue

Next: [Run and Evaluate a Small Local Model](05-run-and-evaluate-a-small-local-model.md)
