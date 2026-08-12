# Understand Transformers and Attention

## Learning objectives

By the end of this lesson, you will be able to:

- describe the main information flow through a Transformer;
- explain queries, keys, values, and attention weights conceptually;
- distinguish encoder, decoder, and encoder-decoder patterns; and
- identify context-window and attention limitations.

## The Transformer processes relationships among tokens

A Transformer begins with token representations plus position information. Each layer combines two major operations:

- an attention sublayer mixes information across token positions; and
- a feed-forward sublayer transforms each position's representation.

Residual connections and normalization support stable deep training. Stacking layers lets representations incorporate increasingly contextual relationships. The original Transformer replaced recurrent sequence processing with attention-based computation that can be parallelized during training.

## Query, key, and value are learned projections

For each token representation, the layer produces:

- a **query** describing what information the current position seeks;
- a **key** describing how a source position can be matched; and
- a **value** containing information to combine if selected.

The system scores a query against keys, scales the scores, applies softmax, and uses the resulting weights to take a weighted combination of values. Multiple attention heads learn different projections in parallel.

"Attention means explanation" is too strong. Attention weights show a computational interaction in a layer; they do not by themselves prove a human-interpretable reason for the final answer.

## Architecture patterns

- **Encoder-only:** builds contextual representations of supplied input; common for classification and extraction.
- **Decoder-only:** predicts tokens autoregressively, with masking that prevents a position from seeing future tokens; common for general text generation.
- **Encoder-decoder:** encodes an input sequence and generates a conditioned output; common for translation and structured transformation.

Product names do not reliably reveal architecture. Consult the model card or technical report.

## Context is finite and selective

A context window bounds how much tokenized input and output can participate in one request. A large advertised limit does not mean every detail is recalled equally or that filling it is wise. More context raises compute and may introduce irrelevant or conflicting evidence. Traditional full attention also grows quadratically with sequence length, motivating efficient alternatives.

## Free local practice

Run a toy attention calculation:

```bash
python3 - <<'PY'
from math import exp

query = [1.0, 0.0]
keys = [[1.0, 0.0], [0.0, 1.0], [0.7, 0.3]]
values = [[10.0, 0.0], [0.0, 10.0], [6.0, 4.0]]

scores = [sum(a * b for a, b in zip(query, key)) for key in keys]
weights = [exp(score) / sum(exp(s) for s in scores) for score in scores]
output = [sum(weight * value[i] for weight, value in zip(weights, values)) for i in range(2)]

print("scores", scores)
print("weights", [round(value, 3) for value in weights])
print("output", [round(value, 3) for value in output])
PY
```

Calculate the dot-product scores by hand first. Change the query to `[0.0, 1.0]`, predict which value contributes most, and verify. Record what this toy omits: learned projections, scaling, masks, multiple heads, batching, positional information, and stacked layers.

## Completion criteria

- [ ] You can trace tokens through representations, attention, feed-forward layers, and output prediction.
- [ ] You correctly explain the different roles of query, key, and value.
- [ ] You distinguish the three common architecture patterns.
- [ ] You completed and modified the toy attention calculation.
- [ ] You name at least two reasons a larger context window does not guarantee a better answer.

## References

- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) - original paper introducing the Transformer architecture.
- [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/) - free visual walkthrough that complements the original paper.
- [What Is a Large Language Model?](https://developers.google.com/machine-learning/crash-course/llm/transformers) - official free explanation of Transformers, self-attention, training, and limitations.
- [Hugging Face: How Do Transformers Work?](https://huggingface.co/learn/llm-course/en/chapter1/4) - free course lesson comparing encoder, decoder, and sequence-to-sequence models.

## Continue

Next: [Separate Training, Alignment, and Inference](04-separate-training-alignment-and-inference.md)
