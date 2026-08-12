# Supervised Fine-Tuning

## Learning objectives

Explain the supervised fine-tuning loop, choose basic training controls, and recognize overfitting without requiring access to a large GPU.

## What training changes

Supervised fine-tuning presents input-target examples and updates model parameters to reduce prediction loss on the target tokens. Tokenization converts text to identifiers; batching groups examples; backpropagation computes gradients; an optimizer updates trainable parameters. An epoch is one pass over the training data.

Important controls include learning rate, effective batch size, number of epochs, sequence length, warmup, regularization, and checkpoint frequency. More training is not automatically better. A small or repetitive dataset can reduce training loss while worsening unseen examples or erasing useful general behavior.

## Experimental discipline

Freeze the base-model identifier, revision, tokenizer, chat template, dataset version, seed, package versions, and configuration. Evaluate the untouched base model and every candidate using the same held-out cases. Track training and validation loss, but use task-specific and safety measures for the final decision.

Inspect how the training library masks tokens. Some instruction-tuning setups compute loss only on assistant output, while others include prompts. An incorrect chat template or loss mask can train the model on control tokens and user text in unintended ways.

## A resource-safe path

You can learn the mechanics using a very small public model and tiny synthetic dataset. The goal is to observe data loading, tokenization, a training step, checkpointing, and evaluation, not to produce a useful general assistant. Stop if your hardware overheats, swaps heavily, or cannot complete the run safely. Reading logs and calculating shapes is valid practice when training hardware is unavailable.

Never publish a trained checkpoint until you have reviewed the base model license, dataset rights, generated samples, and leakage risks.

## Free local practice

Write a training plan before running anything. Include a base model small enough for the available environment, dataset and split versions, maximum runtime, stop conditions, two hyperparameter configurations, and the frozen evaluation command. If compute is available, run one short experiment. Otherwise, inspect an official training example and annotate each configuration field with its effect and risk.

## Completion criteria

- The base model and data revisions are pinned.
- The evaluation set remains untouched by training decisions.
- Stop conditions cover overfitting and resource exhaustion.
- Task and safety evaluation accompany loss curves.

## References

- [Hugging Face Transformers training guide](https://huggingface.co/docs/transformers/training)
- [Hugging Face TRL SFT Trainer](https://huggingface.co/docs/trl/sft_trainer)
- [Hugging Face tokenizers documentation](https://huggingface.co/docs/tokenizers/)
