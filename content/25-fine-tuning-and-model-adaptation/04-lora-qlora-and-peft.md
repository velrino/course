# LoRA, QLoRA, and PEFT

## Learning objectives

Explain parameter-efficient fine-tuning, reason about LoRA configuration, and understand what quantization changes in QLoRA.

## Parameter-efficient adaptation

Full fine-tuning updates all model parameters and requires optimizer state and gradients at that scale. Parameter-efficient fine-tuning, or PEFT, keeps the base model frozen and trains a much smaller set of parameters.

Low-Rank Adaptation, or LoRA, inserts trainable low-rank matrices into selected layers. Important settings include:

- `r`: rank and therefore adapter capacity;
- `lora_alpha`: scaling applied to the update;
- `target_modules`: layers receiving adapters;
- `lora_dropout`: regularization during training;
- `modules_to_save`: any additional modules trained and stored.

A higher rank increases trainable parameters but does not guarantee better generalization. Target-module names differ by architecture, so inspect the model rather than copying a configuration blindly.

QLoRA stores the frozen base model in a low-bit quantized representation while training LoRA adapters. This reduces memory requirements but adds quantization and compatibility choices. It does not make all models trainable on all computers. Estimate memory, start with a small model, and verify that the hardware and library versions support the selected data types.

## Adapter lifecycle

An adapter depends on a specific base model and configuration. Record both. Test loading, unloading, switching, and merging behavior. Merging may simplify inference but produces a new weight artifact that requires its own storage, license review, evaluation, and rollback plan.

## Free local practice

Choose a small model architecture and calculate the number of parameters added by rank-`r` matrices for two target projections. Compare ranks 4, 8, and 16. Create a PEFT configuration and inspect the reported trainable parameter count without completing a long training run. Explain why that count is smaller than total model parameters and what it does not say about runtime memory.

## Completion criteria

- You can explain LoRA without saying it compresses the training dataset.
- Target modules are based on the actual architecture.
- Base model, adapter, tokenizer, and configuration are versioned together.
- QLoRA resource and compatibility limits are documented.

## References

- [Hugging Face PEFT integration](https://huggingface.co/docs/transformers/peft)
- [Hugging Face PEFT LoRA reference](https://huggingface.co/docs/peft/main/package_reference/lora)
- [LoRA paper](https://arxiv.org/abs/2106.09685)
- [QLoRA paper](https://arxiv.org/abs/2305.14314)
